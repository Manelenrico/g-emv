"""
Appraisal v2: affordances estáticas de proximidad (campos de distancia).

Hereda TODO de v1. Añade:
  - f⁺_F: hub propio visible en ventana → pF += A_F_HUB/(1+dist), cap a f_pos_target
  - f⁺_R: extractores de materiales visibles → pR += A_R_EXTRACTOR/(1+dist), cap
  - f⁺_R: tiles de energía solar visibles → pR += A_R_SOLAR/(1+dist), cap

Spec: [doc de diseño interna, no en el repo]
v1 intacta en appraisal/appraisal_v1.py (referencia).

INTOCABLE: motor/model.py. Política: greedy 1-paso exacto, sin lookahead.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from motor.model import (
    HP_EQ, HP_SCALE,
    ENERGY_EQ, ENERGY_SCALE,
    DEFAULT_CONFIG,
    State,
)

# Re-export everything from v1 for backward compatibility
from appraisal.appraisal_v1 import (
    AGENT_LOC, GLOBAL_LOC, PADDING_LOC,
    EGOCENTRIC_COLS, AGENT_ROW, AGENT_COL,
    FID_TAG, FID_INV_HP, FID_INV_ENERGY,
    FID_INV_OXYGEN, FID_INV_CARBON, FID_INV_GERMANIUM, FID_INV_SILICON,
    FID_TERRITORY_HERE,
    TAG_NET_CLIPS, TAG_NET_COGS,
    TAG_TEAM_CLIPS, TAG_TEAM_COGS,
    TAG_TYPE_AGENT, TAG_TYPE_JUNCTION,
    TERR_NEUTRAL, TERR_OWN, TERR_RIVAL,
    TERR_OWN_BONUS, TERR_RIVAL_PENALTY,
    MAT_SCALE_R, ALLY_WEIGHT, RIVAL_WEIGHT, JUNCTION_BONUS,
    Token, parse_tokens, get_scalar, get_multipart,
    loc_to_rowcol, cell_distance, social_weight, iter_spatial_locs,
)

# ── v2-only tag constants (from player_config.tags list) ────────────────────

TAG_TYPE_HUB: int                = 12
TAG_TYPE_CARBON_EXTRACTOR: int   = 10
TAG_TYPE_GERMANIUM_EXTRACTOR: int = 11
TAG_TYPE_OXYGEN_EXTRACTOR: int   = 15
TAG_TYPE_SILICON_EXTRACTOR: int  = 19

EXTRACTOR_TAGS: frozenset[int] = frozenset({
    TAG_TYPE_CARBON_EXTRACTOR,
    TAG_TYPE_GERMANIUM_EXTRACTOR,
    TAG_TYPE_OXYGEN_EXTRACTOR,
    TAG_TYPE_SILICON_EXTRACTOR,
})

FID_INV_SOLAR: int = 34   # energy solar value at spatial cells

# ── v2 affordance amplitudes (calibrated in spec, not iterated against B results)

# Hub proximity → f⁺_F.  Adjacent hub → 0.30 = TERR_OWN_BONUS (v1 territory bonus).
A_F_HUB: float = 0.60

# Material extractor proximity → f⁺_R.  Adjacent → 0.125 ≈ pR from 1 unit material.
A_R_EXTRACTOR: float = 0.25

# Solar tile proximity → f⁺_R.  Adjacent → 1.0 = half r_pos_target.  On tile → 2.0.
A_R_SOLAR: float = 2.0

# Cap thresholds (from DEFAULT_CONFIG)
_F_POS_TARGET: float = DEFAULT_CONFIG.f_pos_target  # 1.0
_R_POS_TARGET: float = DEFAULT_CONFIG.r_pos_target  # 2.0


# ════════════════════════════════════════════════════════════════════════════
# APPRAISAL v2
# ════════════════════════════════════════════════════════════════════════════

def appraise(
    observation_tokens: list[Token],
    team_side: str,
) -> State:
    """Map observation tokens → G-EMV State with v2 affordance signals.

    Inherits all v1 signals. Adds:
      pF += Σ A_F_HUB/(1+dist) over own hubs visible, capped at f_pos_target
      pR += Σ A_R_EXTRACTOR/(1+dist) over extractors visible, capped at r_pos_target
      pR += Σ A_R_SOLAR/(1+dist) over solar tiles visible, capped at r_pos_target
    """
    scalar_map, tag_map = parse_tokens(observation_tokens)

    own_team_tag   = TAG_TEAM_COGS  if team_side == "cogs" else TAG_TEAM_CLIPS
    own_net_tag    = TAG_NET_COGS   if team_side == "cogs" else TAG_NET_CLIPS
    rival_team_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
    rival_net_tag  = TAG_NET_CLIPS  if team_side == "cogs" else TAG_NET_COGS

    # ── F axis (v1 base) ──────────────────────────────────────────────────
    hp = get_multipart(scalar_map, AGENT_LOC, FID_INV_HP)
    pF = max(0.0, (hp - HP_EQ) / HP_SCALE)
    nF = max(0.0, (HP_EQ - hp) / HP_SCALE)

    terr = get_scalar(scalar_map, AGENT_LOC, FID_TERRITORY_HERE)
    if terr == TERR_OWN:
        pF += TERR_OWN_BONUS
    elif terr == TERR_RIVAL:
        nF += TERR_RIVAL_PENALTY

    # ── R axis (v1 base) ──────────────────────────────────────────────────
    energy = get_multipart(scalar_map, AGENT_LOC, FID_INV_ENERGY)
    pR = max(0.0, (energy - ENERGY_EQ) / ENERGY_SCALE)
    nR = max(0.0, (ENERGY_EQ - energy) / ENERGY_SCALE)

    total_mat = (
        get_multipart(scalar_map, AGENT_LOC, FID_INV_OXYGEN)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_CARBON)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_GERMANIUM)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_SILICON)
    )
    pR += math.sqrt(total_mat) / MAT_SCALE_R

    # ── S axis (v1, unchanged) ────────────────────────────────────────────
    pS = 0.0
    nS = 0.0

    # ── v2 affordance accumulators ────────────────────────────────────────
    pF_hub       = 0.0
    pR_extractor = 0.0
    pR_solar     = 0.0

    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())

        # ── Social (v1) ───────────────────────────────────────────────────
        if TAG_TYPE_AGENT in tags:
            w = social_weight(loc)
            if own_team_tag in tags:
                pS += ALLY_WEIGHT * w
            elif rival_team_tag in tags:
                nS += RIVAL_WEIGHT * w

        if TAG_TYPE_JUNCTION in tags:
            if own_net_tag in tags:
                pS += JUNCTION_BONUS
            elif rival_net_tag in tags:
                nS += JUNCTION_BONUS

        # ── v2: hub affordance (F+ field) ─────────────────────────────────
        if TAG_TYPE_HUB in tags and own_team_tag in tags:
            dist = cell_distance(loc)
            pF_hub += A_F_HUB / (1.0 + dist)

        # ── v2: material extractor affordance (R+ field) ──────────────────
        if tags & EXTRACTOR_TAGS:
            dist = cell_distance(loc)
            pR_extractor += A_R_EXTRACTOR / (1.0 + dist)

    # ── v2: solar tile affordance (R+ field, from scalar_map) ────────────
    for (loc, fid), val in scalar_map.items():
        if loc in (AGENT_LOC, GLOBAL_LOC, PADDING_LOC):
            continue
        if fid == FID_INV_SOLAR and val > 0:
            dist = cell_distance(loc)
            pR_solar += A_R_SOLAR / (1.0 + dist)

    # ── Apply affordances with cap ────────────────────────────────────────
    pF = min(pF + pF_hub, _F_POS_TARGET)
    pR = min(pR + pR_extractor + pR_solar, _R_POS_TARGET)

    return State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)


def appraise_with_debug(
    observation_tokens: list[Token],
    team_side: str,
) -> tuple[State, dict]:
    """Same as appraise() but also returns raw v2 affordance signals."""
    scalar_map, tag_map = parse_tokens(observation_tokens)

    own_team_tag   = TAG_TEAM_COGS  if team_side == "cogs" else TAG_TEAM_CLIPS
    own_net_tag    = TAG_NET_COGS   if team_side == "cogs" else TAG_NET_CLIPS
    rival_team_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
    rival_net_tag  = TAG_NET_CLIPS  if team_side == "cogs" else TAG_NET_COGS

    hp     = get_multipart(scalar_map, AGENT_LOC, FID_INV_HP)
    energy = get_multipart(scalar_map, AGENT_LOC, FID_INV_ENERGY)
    terr   = get_scalar(scalar_map, AGENT_LOC, FID_TERRITORY_HERE)
    total_mat = (
        get_multipart(scalar_map, AGENT_LOC, FID_INV_OXYGEN)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_CARBON)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_GERMANIUM)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_SILICON)
    )

    pF = max(0.0, (hp - HP_EQ) / HP_SCALE)
    nF = max(0.0, (HP_EQ - hp) / HP_SCALE)
    if terr == TERR_OWN:
        pF += TERR_OWN_BONUS
    elif terr == TERR_RIVAL:
        nF += TERR_RIVAL_PENALTY

    pR = max(0.0, (energy - ENERGY_EQ) / ENERGY_SCALE) + math.sqrt(total_mat) / MAT_SCALE_R
    nR = max(0.0, (ENERGY_EQ - energy) / ENERGY_SCALE)

    pS = nS = 0.0
    pF_hub = pR_extractor = pR_solar = 0.0
    own_hubs: list[tuple[int, float]] = []
    extractors: list[tuple[int, float]] = []
    solar_tiles: list[tuple[int, float]] = []

    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        if TAG_TYPE_AGENT in tags:
            w = social_weight(loc)
            if own_team_tag in tags:
                pS += ALLY_WEIGHT * w
            elif rival_team_tag in tags:
                nS += RIVAL_WEIGHT * w
        if TAG_TYPE_JUNCTION in tags:
            if own_net_tag in tags:
                pS += JUNCTION_BONUS
            elif rival_net_tag in tags:
                nS += JUNCTION_BONUS
        if TAG_TYPE_HUB in tags and own_team_tag in tags:
            dist = cell_distance(loc)
            contrib = A_F_HUB / (1.0 + dist)
            pF_hub += contrib
            own_hubs.append((loc, dist))
        if tags & EXTRACTOR_TAGS:
            dist = cell_distance(loc)
            contrib = A_R_EXTRACTOR / (1.0 + dist)
            pR_extractor += contrib
            extractors.append((loc, dist))

    for (loc, fid), val in scalar_map.items():
        if loc in (AGENT_LOC, GLOBAL_LOC, PADDING_LOC):
            continue
        if fid == FID_INV_SOLAR and val > 0:
            dist = cell_distance(loc)
            pR_solar += A_R_SOLAR / (1.0 + dist)
            solar_tiles.append((loc, dist))

    pF_capped = min(pF + pF_hub, _F_POS_TARGET)
    pR_capped = min(pR + pR_extractor + pR_solar, _R_POS_TARGET)

    state = State(pF=pF_capped, nF=nF, pR=pR_capped, nR=nR, pS=pS, nS=nS)
    debug = {
        "hp": hp, "energy": energy, "territory": terr, "total_mat": total_mat,
        "pF_v1": pF, "pF_hub": pF_hub, "pF_v2": pF_capped,
        "pR_v1": pR, "pR_extractor": pR_extractor, "pR_solar": pR_solar, "pR_v2": pR_capped,
        "own_hubs": own_hubs, "extractors": extractors, "solar_tiles": solar_tiles,
        "raw_nF": nF, "raw_nR": nR, "raw_pS": pS, "raw_nS": nS,
    }
    return state, debug

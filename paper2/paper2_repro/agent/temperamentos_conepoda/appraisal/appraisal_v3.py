"""
Appraisal v3: affordances condicionadas al déficit activo.

Hereda TODO de v2. Reemplaza los canales R de affordance por versiones
condicionadas al déficit actual del agente:

  - Canal energía: solar tiles × w_energy donde
      w_energy = max(0, (ENERGY_EQ − energy) / ENERGY_EQ)
    → atraen sólo cuando hay déficit de energía; saciadas en equilibrio.

  - Canal materiales: extractores × w_x por tipo donde
      w_x = max(0, protocol_input_x − held_x) / HUB_DEMAND_SCALE
    → atraen proporcional a la necesidad del hub menos lo que ya lleva el agente.

  - Parámetro s_scale (default 1.0): escala pS y nS para el barrido S/F
    de Bloque 3. El nominal (s_scale=1.0) reproduce el comportamiento estándar.

Spec: [doc de diseño interna, no en el repo]
v1/v2 intactas.

INTOCABLE: motor/model.py. Política: greedy 1-paso exacto, sin lookahead.
"""
from __future__ import annotations

import math
import os
import sys

# GEMV_CARGO ([doc de diseño interna, no en el repo]): forma de la RIQUEZA percibida (total_mat → pR).
#   v2 = todo el material poseído es riqueza (conducta actual, bit-exact).
#   v3 = el material DEMANDADO en tránsito NO es riqueza mientras haya demanda viva ("carga, no riqueza").
_CARGO: str = os.environ.get("GEMV_CARGO", "v2")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from motor.model import (
    HP_EQ, HP_SCALE,
    ENERGY_EQ, ENERGY_SCALE,
    DEFAULT_CONFIG,
    State,
)

# Re-export everything from v2 for backward compatibility
from appraisal.appraisal_v2 import (
    AGENT_LOC, GLOBAL_LOC, PADDING_LOC,
    EGOCENTRIC_COLS, AGENT_ROW, AGENT_COL,
    FID_TAG, FID_INV_HP, FID_INV_ENERGY,
    FID_INV_OXYGEN, FID_INV_CARBON, FID_INV_GERMANIUM, FID_INV_SILICON,
    FID_TERRITORY_HERE,
    TAG_NET_CLIPS, TAG_NET_COGS,
    TAG_TEAM_CLIPS, TAG_TEAM_COGS,
    TAG_TYPE_AGENT, TAG_TYPE_JUNCTION,
    TAG_TYPE_HUB,
    TAG_TYPE_CARBON_EXTRACTOR, TAG_TYPE_GERMANIUM_EXTRACTOR,
    TAG_TYPE_OXYGEN_EXTRACTOR, TAG_TYPE_SILICON_EXTRACTOR,
    EXTRACTOR_TAGS,
    FID_INV_SOLAR,
    TERR_NEUTRAL, TERR_OWN, TERR_RIVAL,
    TERR_OWN_BONUS, TERR_RIVAL_PENALTY,
    MAT_SCALE_R, ALLY_WEIGHT, RIVAL_WEIGHT, JUNCTION_BONUS,
    A_F_HUB,
    Token, parse_tokens, get_scalar, get_multipart,
    loc_to_rowcol, cell_distance, social_weight, iter_spatial_locs,
)

# ── protocol_input FIDs (at GLOBAL_LOC=254, normalization=100) ──────────────
# Verified from player_config obs_features (player_config.policy_env.obs_features)

FID_PROTOCOL_INPUT_OXYGEN:    int = 36
FID_PROTOCOL_INPUT_CARBON:    int = 37
FID_PROTOCOL_INPUT_GERMANIUM: int = 38
FID_PROTOCOL_INPUT_SILICON:   int = 39

HUB_DEMAND_SCALE: float = 100.0   # normalization of protocol_input values

# Extractor type → (inv fid, protocol_input fid)
EXTRACTOR_TYPE_INFO: dict[int, tuple[int, int]] = {
    TAG_TYPE_OXYGEN_EXTRACTOR:    (FID_INV_OXYGEN,    FID_PROTOCOL_INPUT_OXYGEN),
    TAG_TYPE_CARBON_EXTRACTOR:    (FID_INV_CARBON,    FID_PROTOCOL_INPUT_CARBON),
    TAG_TYPE_GERMANIUM_EXTRACTOR: (FID_INV_GERMANIUM, FID_PROTOCOL_INPUT_GERMANIUM),
    TAG_TYPE_SILICON_EXTRACTOR:   (FID_INV_SILICON,   FID_PROTOCOL_INPUT_SILICON),
}

# ── v3 channel amplitudes ────────────────────────────────────────────────────

# Energy channel: solar attraction weighted by energy deficit.
# Calibration: adjacent solar at energy=ENERGY_EQ/2 (w=0.5) → 0.5×4.0/2 = 1.0
# (same effective signal as v2's A_R_SOLAR=2.0 at dist=1 with weight=1.0 unconditioned)
A_R_ENERGY: float = 4.0

# Material channel: per-extractor-type attraction, weighted by material need.
# Calibration: same base as v2's A_R_EXTRACTOR; conditioning regulates magnitude.
A_R_MAT: float = 0.25

# Hub amplitude unchanged from v2
# A_F_HUB = 0.60 (imported from v2)

_F_POS_TARGET: float = DEFAULT_CONFIG.f_pos_target  # 1.0
_R_POS_TARGET: float = DEFAULT_CONFIG.r_pos_target  # 2.0


# ════════════════════════════════════════════════════════════════════════════
# APPRAISAL v3
# ════════════════════════════════════════════════════════════════════════════

def _wealth_mat(scalar_map: dict) -> int:
    """total_mat que alimenta pR (riqueza de material). CARGO=v3: excluye el material DEMANDADO en
    tránsito (demand_x>0) — es carga, no riqueza. CARGO=v2: suma todo (bit-exact). El orden y los tipos
    (int) son idénticos a la suma directa oxygen+carbon+germanium+silicon ⇒ v2 bit-exact."""
    total = 0
    for _tag_type, (inv_fid, proto_fid) in EXTRACTOR_TYPE_INFO.items():
        if _CARGO == "v3" and get_scalar(scalar_map, GLOBAL_LOC, proto_fid) > 0:
            continue  # carga en tránsito: no cuenta como riqueza propia mientras haya demanda viva
        total += get_multipart(scalar_map, AGENT_LOC, inv_fid)
    return total


def appraise(
    observation_tokens: list[Token],
    team_side: str,
    s_scale: float = 1.0,
    act_credit: float = 0.0,   # ignorado en v3 (uniformidad de firma con v4; el crédito del acto es de v4)
) -> State:
    """Map observation tokens → G-EMV State with v3 conditioned affordance signals.

    Inherits all v1 + v2 signals. Replaces v2 R-affordances with:
      pR += Σ A_R_ENERGY × w_energy / (1+dist) over solar tiles visible, capped
      pR += Σ A_R_MAT × w_x / (1+dist) over extractor-type-x visible, capped

    where:
      w_energy = max(0, (ENERGY_EQ - energy) / ENERGY_EQ)   [energy deficit ratio]
      w_x = max(0, demand_x - held_x) / HUB_DEMAND_SCALE    [per-material need]

    Args:
        observation_tokens: list of (packed_location, feature_id, value) tuples.
        team_side: "cogs" or "clips".
        s_scale: multiplier for social axis (pS, nS). Default 1.0 = nominal.
                 Used in Bloque 3 barrido S/F characterization.
    """
    scalar_map, tag_map = parse_tokens(observation_tokens)

    own_team_tag   = TAG_TEAM_COGS  if team_side == "cogs" else TAG_TEAM_CLIPS
    own_net_tag    = TAG_NET_COGS   if team_side == "cogs" else TAG_NET_CLIPS
    rival_team_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
    rival_net_tag  = TAG_NET_CLIPS  if team_side == "cogs" else TAG_NET_COGS

    # ── F axis (v1 base + v2 hub affordance) ─────────────────────────────
    hp = get_multipart(scalar_map, AGENT_LOC, FID_INV_HP)
    pF = max(0.0, (hp - HP_EQ) / HP_SCALE)
    nF = max(0.0, (HP_EQ - hp) / HP_SCALE)

    # FIX 2026-07-03 (saneamiento del sensor territorial): territory:here es un
    # token GLOBAL (GLOBAL_LOC=254), no de la celda del agente (AGENT_LOC=102).
    # Antes se leía en AGENT_LOC ⇒ terr=0 SIEMPRE ⇒ f⁺_F/f⁻_F territorial a cero
    # desde que existe el canal (v1). Ver [doc de diseño interna, no en el repo] / auditoria.
    terr = get_scalar(scalar_map, GLOBAL_LOC, FID_TERRITORY_HERE)
    if terr == TERR_OWN:
        pF += TERR_OWN_BONUS
    elif terr == TERR_RIVAL:
        nF += TERR_RIVAL_PENALTY

    # ── R axis (v1 base) ──────────────────────────────────────────────────
    energy = get_multipart(scalar_map, AGENT_LOC, FID_INV_ENERGY)
    pR = max(0.0, (energy - ENERGY_EQ) / ENERGY_SCALE)
    nR = max(0.0, (ENERGY_EQ - energy) / ENERGY_SCALE)

    total_mat = _wealth_mat(scalar_map)
    pR += math.sqrt(total_mat) / MAT_SCALE_R

    # ── v3: energy deficit weight ─────────────────────────────────────────
    w_energy = max(0.0, (ENERGY_EQ - energy) / ENERGY_EQ)

    # ── v3: per-material need weights ─────────────────────────────────────
    w_mat: dict[int, float] = {}
    for tag_type, (inv_fid, proto_fid) in EXTRACTOR_TYPE_INFO.items():
        demand = get_scalar(scalar_map, GLOBAL_LOC, proto_fid)
        held   = get_multipart(scalar_map, AGENT_LOC, inv_fid)
        w_mat[tag_type] = max(0.0, demand - held) / HUB_DEMAND_SCALE

    # ── Social + affordances (spatial scan) ───────────────────────────────
    pS = 0.0
    nS = 0.0
    pF_hub       = 0.0
    pR_energy    = 0.0
    pR_mat       = 0.0

    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        dist = cell_distance(loc)

        # Social (v1)
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

        # F affordance: hub (v2, unchanged)
        if TAG_TYPE_HUB in tags and own_team_tag in tags:
            pF_hub += A_F_HUB / (1.0 + dist)

        # R affordance: material extractors (v3: conditioned by w_mat)
        for tag_type in EXTRACTOR_TAGS:
            if tag_type in tags:
                pR_mat += A_R_MAT * w_mat.get(tag_type, 0.0) / (1.0 + dist)

    # R affordance: solar tiles (v3: conditioned by w_energy, from scalar_map)
    for (loc, fid), val in scalar_map.items():
        if loc in (AGENT_LOC, GLOBAL_LOC, PADDING_LOC):
            continue
        if fid == FID_INV_SOLAR and val > 0:
            dist = cell_distance(loc)
            pR_energy += A_R_ENERGY * w_energy / (1.0 + dist)

    # ── Apply affordances with caps ───────────────────────────────────────
    pF = min(pF + pF_hub, _F_POS_TARGET)
    pR = min(pR + pR_energy + pR_mat, _R_POS_TARGET)

    # ── Apply s_scale for barrido ─────────────────────────────────────────
    pS *= s_scale
    nS *= s_scale

    return State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)


def appraise_with_debug(
    observation_tokens: list[Token],
    team_side: str,
    s_scale: float = 1.0,
) -> tuple[State, dict]:
    """Same as appraise() but also returns raw v3 signals for inspection."""
    scalar_map, tag_map = parse_tokens(observation_tokens)

    own_team_tag   = TAG_TEAM_COGS  if team_side == "cogs" else TAG_TEAM_CLIPS
    own_net_tag    = TAG_NET_COGS   if team_side == "cogs" else TAG_NET_CLIPS
    rival_team_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
    rival_net_tag  = TAG_NET_CLIPS  if team_side == "cogs" else TAG_NET_COGS

    hp     = get_multipart(scalar_map, AGENT_LOC, FID_INV_HP)
    energy = get_multipart(scalar_map, AGENT_LOC, FID_INV_ENERGY)
    # FIX 2026-07-03: territory:here es GLOBAL (loc 254), no AGENT_LOC. Ver arriba.
    terr   = get_scalar(scalar_map, GLOBAL_LOC, FID_TERRITORY_HERE)
    total_mat = _wealth_mat(scalar_map)

    pF = max(0.0, (hp - HP_EQ) / HP_SCALE)
    nF = max(0.0, (HP_EQ - hp) / HP_SCALE)
    if terr == TERR_OWN:
        pF += TERR_OWN_BONUS
    elif terr == TERR_RIVAL:
        nF += TERR_RIVAL_PENALTY

    pR = max(0.0, (energy - ENERGY_EQ) / ENERGY_SCALE) + math.sqrt(total_mat) / MAT_SCALE_R
    nR = max(0.0, (ENERGY_EQ - energy) / ENERGY_SCALE)

    w_energy = max(0.0, (ENERGY_EQ - energy) / ENERGY_EQ)

    w_mat: dict[int, float] = {}
    demands: dict[int, int] = {}
    for tag_type, (inv_fid, proto_fid) in EXTRACTOR_TYPE_INFO.items():
        demand = get_scalar(scalar_map, GLOBAL_LOC, proto_fid)
        held   = get_multipart(scalar_map, AGENT_LOC, inv_fid)
        w_mat[tag_type] = max(0.0, demand - held) / HUB_DEMAND_SCALE
        demands[tag_type] = demand

    pS = nS = 0.0
    pF_hub = pR_energy = pR_mat = 0.0
    own_hubs:     list[tuple[int, float]] = []
    solar_tiles:  list[tuple[int, float]] = []
    extractors:   list[tuple[int, float, float]] = []  # (loc, dist, w_mat)

    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        dist = cell_distance(loc)

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
            contrib = A_F_HUB / (1.0 + dist)
            pF_hub += contrib
            own_hubs.append((loc, dist))

        for tag_type in EXTRACTOR_TAGS:
            if tag_type in tags:
                wt = w_mat.get(tag_type, 0.0)
                contrib = A_R_MAT * wt / (1.0 + dist)
                pR_mat += contrib
                extractors.append((loc, dist, wt))

    for (loc, fid), val in scalar_map.items():
        if loc in (AGENT_LOC, GLOBAL_LOC, PADDING_LOC):
            continue
        if fid == FID_INV_SOLAR and val > 0:
            dist = cell_distance(loc)
            contrib = A_R_ENERGY * w_energy / (1.0 + dist)
            pR_energy += contrib
            solar_tiles.append((loc, dist))

    pF_capped = min(pF + pF_hub, _F_POS_TARGET)
    pR_capped = min(pR + pR_energy + pR_mat, _R_POS_TARGET)

    state = State(
        pF=pF_capped, nF=nF,
        pR=pR_capped, nR=nR,
        pS=pS * s_scale, nS=nS * s_scale,
    )
    debug = {
        "hp": hp, "energy": energy, "territory": terr, "total_mat": total_mat,
        "w_energy": w_energy, "w_mat": w_mat, "demands": demands,
        "pF_v1": pF, "pF_hub": pF_hub, "pF_v3": pF_capped,
        "pR_v1": pR, "pR_energy": pR_energy, "pR_mat": pR_mat, "pR_v3": pR_capped,
        "own_hubs": own_hubs, "extractors": extractors, "solar_tiles": solar_tiles,
        "raw_nF": nF, "raw_nR": nR,
        "pS_raw": pS, "nS_raw": nS, "s_scale": s_scale,
    }
    return state, debug

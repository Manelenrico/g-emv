"""
Appraisal v1: observación Coworld → seis fuerzas G-EMV.

Función pura: sin estado entre ticks. Construye State directamente desde las seis
fuerzas (NO usa state_from_observables). Compatible con motor/model.py intocable.

Spec: [doc de diseño interna, no en el repo]
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Iterator

sys.path.insert(0, str(Path(__file__).parent.parent))
from motor.model import (
    HP_EQ, HP_SCALE,
    ENERGY_EQ, ENERGY_SCALE,
    State,
)


# ── Schema constants (frozen from player_config, machina_1) ─────────────────

AGENT_LOC: int = 102     # egocentric (6,6): 6×16 + 6
GLOBAL_LOC: int = 254
PADDING_LOC: int = 255
EGOCENTRIC_COLS: int = 16
AGENT_ROW: int = 6
AGENT_COL: int = 6

# Feature IDs
FID_TAG: int = 6
FID_INV_HP: int = 20        # p0; p1 at +1
FID_INV_ENERGY: int = 24    # p0; p1 at +1
FID_INV_OXYGEN: int = 12    # p0; p1 at +1
FID_INV_CARBON: int = 14
FID_INV_GERMANIUM: int = 16
FID_INV_SILICON: int = 18
FID_TERRITORY_HERE: int = 69

# Tag indices (from player_config.tags list)
TAG_NET_CLIPS: int = 4
TAG_NET_COGS: int = 5
TAG_TEAM_CLIPS: int = 6
TAG_TEAM_COGS: int = 7
TAG_TYPE_AGENT: int = 8
TAG_TYPE_JUNCTION: int = 13

# Territory:here encoding (egocentric assumption — verified in spec)
TERR_NEUTRAL: int = 0
TERR_OWN: int = 1
TERR_RIVAL: int = 2


# ── Calibration parameters (v1, frozen in spec) ─────────────────────────────

TERR_OWN_BONUS: float = 0.30
TERR_RIVAL_PENALTY: float = 0.50
MAT_SCALE_R: float = 8.0
ALLY_WEIGHT: float = 1.0
RIVAL_WEIGHT: float = 1.0
JUNCTION_BONUS: float = 0.30


# ── Token type ──────────────────────────────────────────────────────────────

Token = tuple[int, int, int]   # (packed_location, feature_id, value)


# ════════════════════════════════════════════════════════════════════════════
# DECODE UTILITIES  (pure, independently testable)
# ════════════════════════════════════════════════════════════════════════════

def parse_tokens(
    tokens: list[Token],
) -> tuple[dict[tuple[int, int], int], dict[int, set[int]]]:
    """Split raw tokens into scalar map and tag map.

    scalar_map: {(packed_loc, feature_id): value}
        Last token wins for the same key. Padding (loc=255) is dropped.
    tag_map: {packed_loc: set[tag_index]}
        All tag values at a location accumulated (feature_id=6 can repeat).
    """
    scalar_map: dict[tuple[int, int], int] = {}
    tag_map: dict[int, set[int]] = {}
    for loc, fid, val in tokens:
        if loc == PADDING_LOC:
            continue
        if fid == FID_TAG:
            tag_map.setdefault(loc, set()).add(val)
        else:
            scalar_map[(loc, fid)] = val
    return scalar_map, tag_map


def get_scalar(
    scalar_map: dict[tuple[int, int], int],
    loc: int,
    fid: int,
    default: int = 0,
) -> int:
    """Scalar feature value, defaulting to 0 (zero-without-token rule)."""
    return scalar_map.get((loc, fid), default)


def get_multipart(
    scalar_map: dict[tuple[int, int], int],
    loc: int,
    base_fid: int,
    n_parts: int = 2,
) -> int:
    """Reconstruct multi-part integer: value = Σ part_i × 256^i."""
    value = 0
    for i in range(n_parts):
        part = scalar_map.get((loc, base_fid + i), 0)
        value += part * (256 ** i)
    return value


def loc_to_rowcol(packed_loc: int) -> tuple[int, int]:
    """Decode packed_location to (row, col) for spatial tokens."""
    return divmod(packed_loc, EGOCENTRIC_COLS)


def cell_distance(packed_loc: int) -> float:
    """Euclidean distance from agent (6,6) to the cell at packed_loc."""
    row, col = loc_to_rowcol(packed_loc)
    return math.sqrt((row - AGENT_ROW) ** 2 + (col - AGENT_COL) ** 2)


def social_weight(packed_loc: int) -> float:
    """Social contribution weight. 1.0 at distance 0, ~0.10 at window edge."""
    return 1.0 / (1.0 + cell_distance(packed_loc))


def iter_spatial_locs(
    scalar_map: dict[tuple[int, int], int],
    tag_map: dict[int, set[int]],
) -> Iterator[int]:
    """All spatial packed_locations present in either map (excludes global/padding/agent)."""
    seen: set[int] = set()
    for (loc, _) in scalar_map:
        if loc not in (PADDING_LOC, GLOBAL_LOC, AGENT_LOC) and loc not in seen:
            seen.add(loc)
            yield loc
    for loc in tag_map:
        if loc not in (PADDING_LOC, GLOBAL_LOC, AGENT_LOC) and loc not in seen:
            seen.add(loc)
            yield loc


# ════════════════════════════════════════════════════════════════════════════
# APPRAISAL
# ════════════════════════════════════════════════════════════════════════════

def appraise(
    observation_tokens: list[Token],
    team_side: str,  # "cogs" or "clips"
) -> State:
    """Map observation tokens → G-EMV State(pF, nF, pR, nR, pS, nS).

    Pure function. No internal state between calls.
    Constructs State directly — does NOT call state_from_observables().

    Args:
        observation_tokens: list of (packed_location, feature_id, value) uint8 tuples.
        team_side: "cogs" or "clips" — the agent's team.

    Returns:
        State with six forces ≥ 0. Basal min and volume ceiling applied by State.__post_init__.
    """
    scalar_map, tag_map = parse_tokens(observation_tokens)

    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    own_net_tag = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
    rival_team_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
    rival_net_tag = TAG_NET_CLIPS if team_side == "cogs" else TAG_NET_COGS

    # ── F axis: physical ──────────────────────────────────────────────────
    hp = get_multipart(scalar_map, AGENT_LOC, FID_INV_HP)
    pF = max(0.0, (hp - HP_EQ) / HP_SCALE)
    nF = max(0.0, (HP_EQ - hp) / HP_SCALE)

    terr = get_scalar(scalar_map, AGENT_LOC, FID_TERRITORY_HERE)
    if terr == TERR_OWN:
        pF += TERR_OWN_BONUS
    elif terr == TERR_RIVAL:
        nF += TERR_RIVAL_PENALTY

    # ── R axis: resources ─────────────────────────────────────────────────
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

    # ── S axis: social ────────────────────────────────────────────────────
    pS = 0.0
    nS = 0.0

    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        if not tags:
            continue

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

    return State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)


def appraise_with_debug(
    observation_tokens: list[Token],
    team_side: str,
) -> tuple[State, dict]:
    """Same as appraise() but also returns raw signals for inspection."""
    scalar_map, tag_map = parse_tokens(observation_tokens)

    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    own_net_tag = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
    rival_team_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
    rival_net_tag = TAG_NET_CLIPS if team_side == "cogs" else TAG_NET_COGS

    hp = get_multipart(scalar_map, AGENT_LOC, FID_INV_HP)
    energy = get_multipart(scalar_map, AGENT_LOC, FID_INV_ENERGY)
    terr = get_scalar(scalar_map, AGENT_LOC, FID_TERRITORY_HERE)
    total_mat = (
        get_multipart(scalar_map, AGENT_LOC, FID_INV_OXYGEN)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_CARBON)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_GERMANIUM)
        + get_multipart(scalar_map, AGENT_LOC, FID_INV_SILICON)
    )

    allies: list[tuple[int, float]] = []
    rivals: list[tuple[int, float]] = []
    own_junctions: list[int] = []
    rival_junctions: list[int] = []

    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        if not tags:
            continue
        if TAG_TYPE_AGENT in tags:
            w = social_weight(loc)
            if own_team_tag in tags:
                allies.append((loc, w))
            elif rival_team_tag in tags:
                rivals.append((loc, w))
        if TAG_TYPE_JUNCTION in tags:
            if own_net_tag in tags:
                own_junctions.append(loc)
            elif rival_net_tag in tags:
                rival_junctions.append(loc)

    pF = max(0.0, (hp - HP_EQ) / HP_SCALE)
    nF = max(0.0, (HP_EQ - hp) / HP_SCALE)
    if terr == TERR_OWN:
        pF += TERR_OWN_BONUS
    elif terr == TERR_RIVAL:
        nF += TERR_RIVAL_PENALTY

    pR = max(0.0, (energy - ENERGY_EQ) / ENERGY_SCALE) + math.sqrt(total_mat) / MAT_SCALE_R
    nR = max(0.0, (ENERGY_EQ - energy) / ENERGY_SCALE)

    pS = sum(ALLY_WEIGHT * w for _, w in allies) + JUNCTION_BONUS * len(own_junctions)
    nS = sum(RIVAL_WEIGHT * w for _, w in rivals) + JUNCTION_BONUS * len(rival_junctions)

    state = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
    debug = {
        "hp": hp, "energy": energy, "territory": terr, "total_mat": total_mat,
        "allies": allies, "rivals": rivals,
        "own_junctions": own_junctions, "rival_junctions": rival_junctions,
        "raw_pF": pF, "raw_nF": nF, "raw_pR": pR, "raw_nR": nR,
        "raw_pS": pS, "raw_nS": nS,
    }
    return state, debug

"""
appraisal v_estantería — compresión multi-variable del dominio R.

GEMV_SHELF=OFF (default): bit-exact con appraisal_v4.
GEMV_SHELF=ON: modifica pR/nR con déficit del pantry del equipo (recurso extendido).

Spec: [doc de diseño interna, no en el repo]
Criterios: [doc de diseño interna, no en el repo]
motor/model.py INTOCABLE.
"""
from __future__ import annotations

from motor.model import State
from appraisal.appraisal_v4 import (
    appraise as _appraise_v4,
    SOCIAL_K, BETA_CARRY,
)
from appraisal.appraisal_v3 import (
    parse_tokens, get_scalar, get_multipart,
    GLOBAL_LOC, AGENT_LOC,
    TAG_TYPE_HUB, TAG_TEAM_COGS, TAG_TEAM_CLIPS,
    FID_INV_OXYGEN, FID_INV_CARBON, FID_INV_GERMANIUM, FID_INV_SILICON,
    iter_spatial_locs,
)
from appraisal.appraisal_v4 import (
    FID_TEAM_OXYGEN, FID_TEAM_CARBON, FID_TEAM_GERMANIUM, FID_TEAM_SILICON,
)

# ── Parameters declared in spec §9 — read-only, NOT to iterate against verdicts ──
HEART_COST: int   = 7     # heart.cost = {element: 7} in machina_1 — game constant
W_EXT:      float = 0.50  # per-element weight, team pantry (extended resource)
W_OWN:      float = 0.10  # per-element weight, agent inventory (gated by pantry scarcity)

# ── Eslabón 1 (GEMV_HEARTS) — balda de hearts en R. [doc de diseño interna, no en el repo] §1.1 ──
# hearts_conocidos = MIS hearts portados (inv:heart), único canal observable (no hay team:heart).
FID_INV_HEART: int = 22    # inv:heart p0 (LEÍDO del player_config en runtime; 22 = default adaptador)
W_HEARTS:      float = 2.40  # peer de la balda de despensa completa; anclado en la curva d(pos_R) (§1.2)
HEART_TARGET:  int   = 5     # dotación de arranque del juego (D3); cap por agente = 10

# ── Eslabón 4 (GEMV_MARCADOR) — balda TERRITORIAL de doble residencia (R + S). [doc de diseño interna, no en el repo] §1 ──
TAG_TYPE_JUNCTION: int = 13   # type:junction (LEÍDO del config)
TAG_NET_COGS:      int = 5    # net:cogs
TAG_NET_CLIPS:     int = 4    # net:clips
W_TERR_R:  float = 2.40  # hambre de territorio (R), peer de la balda de hearts (Manel firma antes del probe)
T_TERR:    int   = 1     # conocer 1 junction ganable = hambre plena
W_TERR_S:  float = 0.60  # el vínculo (S), subordinado al recurso
T_OURS:    int   = 3     # pertenencia satura a 3 junctions propias

# ── ESLABÓN DESPENSA (GEMV_DESPENSA) — dolor social por escasez del almacén común (receta del aligner). D1/D3 ──
ALIGNER_RECIPE: list  = [1, 3, 1, 1]  # [oxígeno×1, carbono×3, germanio×1, silicio×1] — 1 aligner, en orden _TEAM_FIDS
W_DESPENSA:     float = 0.30          # altura del dolor S de despensa (D3, firmada Manel 2026-07-26). Dolor =
                                      # (4·W)·worst²; máx (peor material a 0) = 4·W = 1.2 restado de pos_S.


def despensa_deficit_S(team_held, hub_vis_eff, recipe=ALIGNER_RECIPE, w=W_DESPENSA):
    """Dolor social (D1, CORRECCIÓN DE ESCALA firmada 2026-07-26): la cadena del aligner se BLOQUEA con que
    falte UN solo material, así que el dolor NO escala con el % medio que falta, sino con si la RECETA es
    fabricable: lo marca el material PEOR, no la media. Un material a 0 duele casi el máximo, igual que si
    faltara todo. worst = max_x max(0, 1 − held_x/need_x); dolor = ALTURA · worst², donde ALTURA = 4·w
    preserva la altura firmada (dolor de despensa VACÍA = 4·W = 1.2 con W=0.30, ⇒ el gate (d) cuerpo>despensa
    queda idéntico). 0 si el hub no es conocido (hub_vis_eff=False) o la receta es fabricable (worst=0, D2)."""
    if not hub_vis_eff:
        return 0.0
    worst = 0.0
    for held, need in zip(team_held, recipe):
        if need <= 0:
            continue
        sc = 1.0 - held / need   # escasez de ESTE material vs una receta (>0 si held<need)
        if sc > worst:
            worst = sc           # el peor material marca el déficit (cadena bloqueada por el más escaso)
    altura = 4.0 * w             # altura máx = 4·W (continuidad con la calibración firmada: máx 1.2)
    return altura * worst * worst


def territorial_RS(scalar_map, tag_map, team_side, remembered=None,
                   w_r=W_TERR_R, t_terr=T_TERR, w_s=W_TERR_S, t_ours=T_OURS):
    """Balda territorial (§1): déficit_R (hambre de ganar territorio) + bono_S (pertenencia).
    Contabilidad epistémica: junctions PERCIBIDAS (tokens) + RECORDADAS (remembered=[(loc,'ours'|'gain')]).
    n_gain = ganables (gris/enemiga); n_ours = nuestras (net propio)."""
    own_net = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
    n_gain = n_ours = 0
    seen = set()
    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        if TAG_TYPE_JUNCTION in tags:
            seen.add(loc)
            if own_net in tags:
                n_ours += 1
            else:
                n_gain += 1
    if remembered:                             # dueños de junctions RECORDADAS fuera de ventana
        for owner in remembered:               # (gemv_policy ya excluyó las percibidas)
            if owner == "ours":
                n_ours += 1
            else:
                n_gain += 1
    sc_g = min(1.0, n_gain / t_terr)
    deficit_R = w_r * sc_g * sc_g
    bono_S = w_s * min(1.0, n_ours / t_ours)
    return deficit_R, bono_S, n_gain, n_ours

_TEAM_FIDS: list[int] = [FID_TEAM_OXYGEN, FID_TEAM_CARBON, FID_TEAM_GERMANIUM, FID_TEAM_SILICON]
_OWN_FIDS:  list[int] = [FID_INV_OXYGEN,  FID_INV_CARBON,  FID_INV_GERMANIUM,  FID_INV_SILICON]


def shelf_deficit_R(
    team_held: list[float],
    own_held:  list[float],
    hub_in_window: bool,
    w_ext:      float = W_EXT,
    w_own:      float = W_OWN,
    heart_cost: int   = HEART_COST,
) -> float:
    """Shelf deficit term for the R axis (pure function, no tokens).

    Returns a non-negative value; this is SUBTRACTED from pos_R:
        new_pos_R = pos_R_v4 - deficit_R

    hub_in_window=False → 0.0 always (C3: pantry perceived only in window).

    For each element x:
      sc_ext_x  = max(0, 1 - team_x / HC)           [pantry scarcity, quadratic]
      sc_own_x  = max(0, 1 - own_x  / HC)           [own-inv scarcity]
      term_x    = W_EXT * sc_ext_x² + W_OWN * sc_own_x² * sc_ext_x
                  (own term gated by sc_ext: carries nothing if pantry is full)
    """
    if not hub_in_window:
        return 0.0
    deficit = 0.0
    for t, o in zip(team_held, own_held):
        sc_ext = max(0.0, 1.0 - t / heart_cost)
        sc_own = max(0.0, 1.0 - o / heart_cost)
        deficit += w_ext * sc_ext * sc_ext + w_own * sc_own * sc_own * sc_ext
    return deficit


def hearts_deficit_R(
    mis_hearts:  float,
    w_hearts:    float = W_HEARTS,
    heart_target: int  = HEART_TARGET,
) -> float:
    """Término de la balda de hearts para el eje R (§1.1). Pure function, no window-gating.

    sc_heart   = max(0, 1 − mis_hearts / HEART_TARGET)
    return       W_HEARTS · sc_heart²        (se SUMA al déficit de despensa, se resta de pos_R)

    mis_hearts = inv:heart portado por MÍ (único canal observable, §0). Siempre observable ⇒
    la urgencia de hearts viaja por construcción (no necesita pantry_mem).
    """
    sc = max(0.0, 1.0 - mis_hearts / heart_target)
    return w_hearts * sc * sc


def _hub_in_window(scalar_map: dict, tag_map: dict, own_team_tag: int) -> bool:
    """True if the agent's team hub is visible in the egocentric window."""
    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        if TAG_TYPE_HUB in tags and own_team_tag in tags:
            return True
    return False


def appraise_shelf(
    tokens,
    team_side:      str,
    shelf_on:       bool        = False,
    s_scale:        float       = 1.0,
    k:              float       = SOCIAL_K,
    beta:           float       = BETA_CARRY,
    act_credit:     float       = 0.0,
    pantry_memory:  dict | None = None,
    pantry_age:     float       = 0.0,
    pantry_decay_lambda: float  = 0.0,
    hearts_on:      bool        = False,
    w_hearts:       float       = W_HEARTS,
    heart_target:   int         = HEART_TARGET,
    marcador_on:    bool        = False,
    terr_remembered: list | None = None,
    despensa_on:    bool        = False,
    w_despensa:     float       = W_DESPENSA,
    hub_single_source: bool     = False,
    econ_const:     bool        = False,
) -> State:
    """v4 + shelf R modification.

    GEMV_SHELF=OFF (shelf_on=False, default): returns State identical to appraisal_v4.appraise.
    GEMV_SHELF=ON  (shelf_on=True):           modifies pR/nR with team-pantry deficit term.

    pantry_memory (GEMV_PANTRY_MEM=1): dict {FID_TEAM_*: float} with last observed
    pantry values. When hub is NOT in window but memory is valid (age already validated
    in gemv_policy), memory substitutes direct perception for the deficit computation.
    Perception ALWAYS wins when hub is visible (memory ignored). None = C3 original.

    All v4 parameters (k, beta, act_credit) pass through unchanged.
    """
    s = _appraise_v4(tokens, team_side, s_scale=s_scale, k=k, beta=beta, act_credit=act_credit)
    if not shelf_on:
        return s   # bit-exact: State unchanged

    scalar_map, tag_map = parse_tokens(tokens)
    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS

    hub_vis = _hub_in_window(scalar_map, tag_map, own_team_tag)

    mem_factor = 1.0   # atenuación del recuerdo (D3); 1.0 = percepción directa o v5
    if hub_vis:
        # Percepción directa manda — leer del token actual (factor 1, edad irrelevante)
        team_held = [get_scalar(scalar_map, GLOBAL_LOC, fid) for fid in _TEAM_FIDS]
        hub_vis_eff = True
    elif pantry_memory is not None:
        # Recuerdo — la urgencia viaja con el agente. v6/D3: el recuerdo DECAE con la edad
        # (exp(-λ·age)); v5: λ=0 ⇒ factor 1 (sin decaimiento, corte binario aguas arriba).
        team_held = [pantry_memory.get(fid, 0.0) for fid in _TEAM_FIDS]
        hub_vis_eff = True
        if pantry_decay_lambda > 0.0 and pantry_age > 0.0:
            import math as _m
            mem_factor = _m.exp(-pantry_decay_lambda * pantry_age)
    else:
        # Sin hub visible y sin memoria: C3 original (déficit = 0)
        team_held = [0.0] * len(_TEAM_FIDS)
        hub_vis_eff = False

    own_held  = [get_multipart(scalar_map, AGENT_LOC, fid) for fid in _OWN_FIDS]

    # Eslabón 1 — balda de hearts (§1.1): NO window-gated (mis hearts siempre observables).
    heart_def = 0.0
    if hearts_on:
        mis_hearts = get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART)
        heart_def = hearts_deficit_R(mis_hearts, w_hearts, heart_target)

    _shelf_R = shelf_deficit_R(team_held, own_held, hub_vis_eff) * mem_factor
    if (hub_single_source and despensa_on) or econ_const:
        _shelf_R = 0.0    # UNA FUENTE: la escasez del hub se retira del eje R en pie. HSS la deja en S (despensa);
                          # ECON_CONST (constitución) la deja SÓLO en el motor de abastecimiento (gain dirigida).
                          # El hambre PERSONAL en R (energía base v4 + hearts + territorial) queda intacta.
    deficit = _shelf_R + heart_def

    # Eslabón 4 — balda territorial (§1): déficit_R (ganar territorio) + bono_S (pertenencia).
    bono_S = 0.0
    if marcador_on:
        d_terr, bono_S, _ng, _no = territorial_RS(scalar_map, tag_map, team_side, remembered=terr_remembered)
        deficit += d_terr

    # ── ESLABÓN DESPENSA (D1): dolor S por escasez del almacén común vs la receta del aligner ──
    despensa_S = 0.0
    if despensa_on:
        despensa_S = despensa_deficit_S(team_held, hub_vis_eff, w=w_despensa) * mem_factor

    if deficit == 0.0 and bono_S == 0.0 and despensa_S == 0.0:
        return s

    pos_R_new = s.pR - s.nR - deficit   # current pos_R = pR - nR; apply deficit
    new_pR = max(0.0,  pos_R_new)
    new_nR = max(0.0, -pos_R_new)
    if bono_S != 0.0 or despensa_S != 0.0:  # S: pertenencia (+bono) y/o dolor de despensa (−despensa_S)
        pos_S_new = s.pS - s.nS + bono_S - despensa_S
        new_pS = max(0.0,  pos_S_new)
        new_nS = max(0.0, -pos_S_new)
    else:
        new_pS, new_nS = s.pS, s.nS
    return State(pF=s.pF, nF=s.nF, pR=new_pR, nR=new_nR, pS=new_pS, nS=new_nS)

"""
appraisal v4 — la vía social: la demanda del hub como carencia del vínculo (f⁻_S).

Spec: [doc de diseño interna, no en el repo]. Hereda appraisal_v3 sin cambios; SOLO añade un canal
que suma a nS (déficit social) según la demanda colectiva insatisfecha. model.py INTOCABLE.

Decisión de Manel: DEPOSITAR cierra la carencia (satisfactor primario); llevar material la cubre
una fracción β<1 (para que minar ya baje d dentro de H=4); el hub surtido es señal secundaria.

INTERRUPTORES: GEMV_APPRAISAL=4 activa v4; GEMV_SOCIAL_K=k (0 ⇒ ≡ v3 bit a bit).

NOTA (R0): en machina-1-daily all-cogs la demanda observada es 0 (ver [doc de diseño interna, no en el repo]), así que
el canal es inerte en vivo (≡v3). El diseño se valida en aislamiento con tests sintéticos.
"""
from __future__ import annotations

from motor.model import State
from appraisal.appraisal_v3 import (
    appraise as _appraise_v3,
    appraise_with_debug as _appraise_v3_debug,
    parse_tokens, get_scalar, get_multipart,
    GLOBAL_LOC, AGENT_LOC,
    FID_PROTOCOL_INPUT_OXYGEN, FID_PROTOCOL_INPUT_CARBON,
    FID_PROTOCOL_INPUT_GERMANIUM, FID_PROTOCOL_INPUT_SILICON,
    FID_INV_OXYGEN, FID_INV_CARBON, FID_INV_GERMANIUM, FID_INV_SILICON,
    HUB_DEMAND_SCALE,
)

# team:{resource} hub-inventory FIDs (de obs_features del player_config)
FID_TEAM_OXYGEN:    int = 60
FID_TEAM_CARBON:    int = 62
FID_TEAM_GERMANIUM: int = 64
FID_TEAM_SILICON:   int = 66

# material -> (proto_demand_fid, team_held_fid, agent_inv_fid)
_MAT_FIDS = {
    "oxygen":    (FID_PROTOCOL_INPUT_OXYGEN,    FID_TEAM_OXYGEN,    FID_INV_OXYGEN),
    "carbon":    (FID_PROTOCOL_INPUT_CARBON,    FID_TEAM_CARBON,    FID_INV_CARBON),
    "germanium": (FID_PROTOCOL_INPUT_GERMANIUM, FID_TEAM_GERMANIUM, FID_INV_GERMANIUM),
    "silicon":   (FID_PROTOCOL_INPUT_SILICON,   FID_TEAM_SILICON,   FID_INV_SILICON),
}

# Parámetros declarados en la spec (NO calibrados contra veredictos):
BETA_CARRY: float = 0.5    # fracción de cobertura al LLEVAR material demandado (depositar = 1.0)
# k fijado por la REGLA de escala: carencia normalizada máx (=1.0) -> señal ≈ margen real del eje S
# (~0.049 de d; [doc de diseño interna, no en el repo]). Con Δns≈0.15 la señal cae en esa banda y el óptimo
# efectivo de S (pos_S≈0.4) apenas se desplaza. (No calibrado contra veredictos; R0 lo hace inerte en vivo.)
SOCIAL_K:   float = 0.15
K_SEC:      float = 0.04   # peso de la señal secundaria (hub surtido), menor

# COBERTURA ([doc de diseño interna, no en el repo]): forma de saciar la carencia social.
#   v1_linear = affordance de proximidad (B) − sin acto (conducta actual, bit-exact).
#   v2_hybrid = A (acto/depósito, FIJO) + B=0 (sin proximidad) + C (posesión β, en social_deficit).
import os as _os
COVERAGE: str = _os.environ.get("GEMV_COVERAGE", "v1_linear")
# A_UNIT fijado por aritmética (spec §3): 0.330·A_UNIT ≥ 2·0.0237 ⇒ A_UNIT ≥ 0.1436; declarado 0.15
# (margen 2.09× sobre el gap territorial medido). NO se itera contra R2.
A_UNIT: float = 0.15
# acts_done viaja como TOKEN (AGENT_LOC, FID_ACTS_DONE, n): la política inyecta los depósitos reales; la
# transición del planificador lo incrementa al IMAGINAR un depósito. appraise lo lee ⇒ el crédito A del
# acto propaga por el horizonte SIN cambiar la estructura de búsqueda del planificador.
FID_ACTS_DONE: int = 250   # fid reservado (muy por encima de los fids del juego ~75)

# DEMANDA DERIVADA (cargo_v3 / fase competidor, decisión de Manel): en machina_1 la demanda global
# (protocol_input) es 0, pero el agente YA percibe `team:{elemento}` (stock del hub). La demanda del
# colectivo se DERIVA por inferencia perceptiva (misma familia que día/noche por delta solar; NO valor
# nuevo, NO recompensa): demanda_x = max(0, HEART_COST − team_held_x). Magnitud mínima: UNA receta de heart.
# GEMV_DEMAND_DERIVED default OFF ⇒ lee protocol_input como antes (bit-exact). Vía A (inyectar señal) DESCARTADA.
DEMAND_DERIVED: bool = _os.environ.get("GEMV_DEMAND_DERIVED", "0") == "1"
HEART_COST: int = 7        # heart.cost = {elemento: 7} (machina_1.configure); constante declarada del juego


def social_deficit(demands: dict, team_held: dict, agent_held: dict,
                   k: float = SOCIAL_K, beta: float = BETA_CARRY, k_sec: float = K_SEC) -> float:
    """f⁻_S por demanda colectiva insatisfecha (función pura, testeable en aislamiento).

    unsatisfied_x = max(0, demand_x - team_held_x - beta·agent_held_x)   [depositar sube team_held]
    f⁻_S = k · Σ unsatisfied_x / SCALE  +  k_sec · Σ max(0, demand_x - team_held_x) / SCALE
    """
    prim = 0.0
    sec = 0.0
    for x, d in demands.items():
        th = team_held.get(x, 0.0)
        ah = agent_held.get(x, 0.0)
        prim += max(0.0, d - th - beta * ah)
        sec += max(0.0, d - th)
    return (k * prim + k_sec * sec) / HUB_DEMAND_SCALE


def _read_resources(scalar_map: dict):
    demands, team_held, agent_held = {}, {}, {}
    for x, (proto_fid, team_fid, inv_fid) in _MAT_FIDS.items():
        team_held[x]  = get_scalar(scalar_map, GLOBAL_LOC, team_fid)
        agent_held[x] = get_multipart(scalar_map, AGENT_LOC, inv_fid)
        if DEMAND_DERIVED:
            # Inferencia perceptiva: la demanda = déficit real de UNA receta de heart (max(0, coste − stock)).
            demands[x] = max(0, HEART_COST - team_held[x])
        else:
            demands[x] = get_scalar(scalar_map, GLOBAL_LOC, proto_fid)
    return demands, team_held, agent_held


def social_affordance(tokens, team_side, s_scale: float = 1.0) -> float:
    """f de affordance social: la affordance de material de v3 (pR_mat) RE-RUTEADA al eje social.

    Opción A (decisión de Manel 2026-07-04): v3 ya computa pR_mat = Σ A_R_MAT·w_mat/(1+dist) sobre
    extractores percibidos en ventana — direccional (pesa por proximidad) y con puerta de demanda
    (w_mat = max(0, demand−held)/SCALE ⇒ 0 sin demanda). Pero lo suma a pR, que satura en tope 2.0
    en casa ⇒ enmascarado. Aquí lo LEEMOS (mismo A_R_MAT, mismo escaneo, NO se recalibra) para
    cubrir parcialmente la carencia en el canal social, que NO satura. Ver el satisfactor cerca es
    señal del MISMO eje (la demanda es hambre del vínculo, decisión de la 3d). Con demanda=0 ⇒
    w_mat=0 ⇒ pR_mat=0 ⇒ affordance social CERO: el extractor vuelve a ser objeto de R saciado (R3).
    """
    _, dbg = _appraise_v3_debug(tokens, team_side, s_scale=s_scale)
    return float(dbg.get("pR_mat", 0.0))


def appraise(tokens, team_side, s_scale: float = 1.0,
             k: float = SOCIAL_K, beta: float = BETA_CARRY, act_credit: float = 0.0) -> State:
    """v3 + canal social. Con k=0 devuelve EXACTAMENTE el State de v3 (gate).

    COVERAGE=v1_linear: la affordance de proximidad (B) cubre la carencia (conducta actual).
    COVERAGE=v2_hybrid: A (acto, `act_credit` pasado por la política) + B=0 + C (β en social_deficit).
    `act_credit` = A_UNIT·acts_done (gated demanda>0 por la política). Candado de frontera: con demanda 0,
    social_deficit=0 ⇒ nS_add=0 sea cual sea act_credit.
    """
    s = _appraise_v3(tokens, team_side, s_scale=s_scale)
    if k == 0.0:
        return s
    scalar_map, _ = parse_tokens(tokens)
    demands, team_held, agent_held = _read_resources(scalar_map)
    deficit = social_deficit(demands, team_held, agent_held, k=k, beta=beta)
    if COVERAGE == "v2_hybrid":
        # B=0 (sin proximidad). A = acto (token acts_done · A_UNIT + act_credit imaginado). C = β·held.
        # Candado de frontera: sin demanda no hay parte que hacer ⇒ el crédito A no aplica.
        acts_done = get_scalar(scalar_map, AGENT_LOC, FID_ACTS_DONE)
        credit = (A_UNIT * acts_done + act_credit) if any(d > 0 for d in demands.values()) else 0.0
        delta = max(0.0, deficit - credit)
    else:  # v1_linear (bit-exact): affordance de proximidad
        affordance = social_affordance(tokens, team_side, s_scale=s_scale)
        delta = max(0.0, deficit - beta * affordance)
    if delta == 0.0:
        return s
    return State(pF=s.pF, nF=s.nF, pR=s.pR, nR=s.nR, pS=s.pS, nS=s.nS + delta * s_scale)

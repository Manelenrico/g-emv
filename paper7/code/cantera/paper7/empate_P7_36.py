"""[P7-36, parte 1, banco] EN UN EMPATE, NO SE COGE: la simetrica de la regla de soltar de P7-10/P7-14b (`descubre_P7.desempate_sin_sitio`). Envoltorio de
`D.select_tiebreak`: si el minimo de la d terminal lo comparten (empate exacto, _TOL) `coger` y un candidato que no es coger, o si el paisaje es degenerado (spread <= eps),
`coger` sale del desempate (quedarse como se esta no cuesta un gesto; `noop` no puede ganar empates, N2a, y por eso coger ganaba). Si coger gana solo, gana. Mismo criterio de
empate que la regla de soltar, ningun numero nuevo. Solo para el banco (GEMV_P7_36_EMPATE=1); no se juega con ella. Se aplica DESPUES de las piezas del siete."""
import os
COGER = ("coger",)
ON = os.environ.get("GEMV_P7_36_EMPATE", "0") == "1"
E = {"veces": 0, "ticks": []}


def desempate_sin_coger(sel0):
    from planificador.planificador_v1 import TIEBREAK_EPS, _TOL
    def sel(action_names, preds, terminal, meta, *a, **kw):
        coger = [x for x in action_names if str(x) in COGER]
        if coger and len(coger) < len(action_names):
            vals = [terminal[x] for x in action_names]; mn = min(vals); eps = kw.get("eps", TIEBREAK_EPS)
            c1 = [x for x in action_names if terminal[x] <= mn + _TOL]
            if (max(vals) - mn <= eps) or (any(x in coger for x in c1) and any(x not in coger for x in c1)):
                resto = [x for x in action_names if x not in coger]; E["veces"] += 1
                return sel0(resto, {x: preds[x] for x in resto}, {x: terminal[x] for x in resto}, ({x: meta[x] for x in resto} if meta else meta), *a, **kw)
        return sel0(action_names, preds, terminal, meta, *a, **kw)
    sel._P7_36 = True
    return sel


def aplica(D):
    if not ON or getattr(D.select_tiebreak, "_P7_36", False): return {"P7_36_empate": ON}
    D.select_tiebreak = desempate_sin_coger(D.select_tiebreak); return {"P7_36_empate": True}

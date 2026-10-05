"""[P6-28] LA PREVISION: la escena prevista para el tic t + DELTA, cuando llegara la respuesta del razonador.
La hace el cuerpo con la imaginacion honesta de puerta6 (`puerta6_P6_15.rollout`: su propio decisor, tic a
tic, durante DELTA tics, desde la instantanea de la consulta), con las reglas de honestidad de esa imaginacion:
  · anillo: del calendario (`mundo.anillo_en(t)`, dentro de `foto_rapida` y de `proyectar_rapido`, que quema
    la casilla que queda fuera);
  · rivales: quietos donde se ven o se cuentan (`foto_rapida` comparte los `agents` de la observacion de la
    consulta; no se inventa ningun movimiento);
  · hermano: en la posicion de su ultimo parte (si lo hay; si se le ve, donde se le ve);
  · recursos: los conocidos (el suelo visto en la consulta, menos lo que el cuerpo imaginado coge).
Devuelve la observacion prevista (misma forma que una observacion real), los candidatos del cuerpo en esa
escena (para el relato del cinco) y el estado previsto (casilla, vida). La escena de texto es la de A8
(`texto_escena_P6_26.texto`) con una frase delante que dice que es la situacion prevista, el anillo y los
rivales a t + DELTA y lo reciente hasta la consulta. El plan del razonador parte de la casilla prevista
(`escena_traductor.pos`). DELTA se fija en el sello (retraso mediano de llegada medido en P6-27).
"""
from __future__ import annotations
import copy
import time
import os
import sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    if p not in sys.path:
        sys.path.insert(0, p)
import forma as F                                          # noqa: E402
import puerta6_P6_15 as P6                                 # noqa: E402
from alma import decisor_zs as D                           # noqa: E402
import texto_escena_P6_26 as TX                            # noqa: E402
VERSION = "prevision_P6_28 (P6-28): escena prevista a t+DELTA con la imaginacion honesta de puerta6 (rollout tic a tic); rivales quietos, hermano en su ultimo parte, anillo del calendario"
DELTA = int(os.environ.get("GEMV_PREVISION_DELTA", "94") or 94)      # [sello] retraso mediano de llegada en la serie de P6-27


def prever(alma, obs, mem, blo, t, delta=DELTA):
    """(obs_prevista, cands, info). `alma` es el espejo (mundo, tick, mem, bloqueos puestos)."""
    t0 = time.perf_counter()
    alma.tick = t; alma.mem = mem; alma.bloqueos = blo
    e0, suelo, _pisos = alma._contexto(obs, mem)
    snaps, n_dec = P6.rollout(obs, e0, t + delta, alma.mundo, mem, blo, suelo)
    e = snaps.get(t + delta) or snaps[max(snaps)]
    # el suelo que queda: lo conocido menos lo que el cuerpo imaginado cogio por el camino
    cogidos = set()
    for k in range(t, t + delta + 1):
        s = snaps.get(k) or {}
        for it in ((s.get("_hecho") or {}).get("cogido") or []):
            cogidos.add(tuple(s["pos"]))
    suelo_rest = [it for pos_, it in suelo.items() if tuple(pos_) not in cogidos]
    o2 = F.foto_rapida(obs, e, alma.mundo, t + delta, suelo_rest)
    o2 = copy.deepcopy(o2); o2["phase"] = "live"
    # el hermano, en la posicion de su ultimo parte (si lo hay y no se le ve)
    herm = getattr(alma.mundo, "teammate_slot", None); parte = getattr(alma, "parte_herm", None)
    ag = [dict(a) for a in (o2["visible"].get("agents") or [])]
    if parte and parte.get("pos") and not any(a.get("slot") == herm for a in ag):
        ag.append({"slot": herm, "pos": [int(parte["pos"][0]), int(parte["pos"][1])], "hp": parte.get("hp"), "team": (obs.get("you") or {}).get("team")})
    o2["visible"]["agents"] = ag
    # los candidatos del cuerpo en la escena prevista (para el relato del cinco)
    try:
        _ac, radio = D.decide(o2, alma.mundo, copy.deepcopy(mem), t + delta, copy.deepcopy(blo))
        cands = {k: (float(v["d"]) if isinstance(v, dict) and v.get("d") is not None else (float(v) if isinstance(v, (int, float)) else 0.0)) for k, v in (radio.get("candidatos") or {}).items()}
    except Exception:
        cands = {}
    info = {"delta": delta, "t_previsto": t + delta, "pos_prevista": [int(e["pos"][0]), int(e["pos"][1])], "hp_prevista": round(float(e["hp"]), 2), "pos_consulta": list((obs.get("you") or {}).get("pos") or ()),
            "hp_consulta": (obs.get("you") or {}).get("hp"), "decisiones": n_dec, "ms_prevision": round((time.perf_counter() - t0) * 1000.0, 2), "cogidos": len(cogidos), "arde_previsto": bool(o2["zone"].get("damage_per_s")) and (max(abs(e["pos"][0] - 24), abs(e["pos"][1] - 24)) > 0 and ((e["pos"][0] - 24) ** 2 + (e["pos"][1] - 24) ** 2) ** 0.5 > float(o2["zone"]["radius"] or 48))}
    return o2, cands, info


def frase(info):
    d = info["delta"]
    return (f"**ESTA ES LA SITUACION PREVISTA para el tic {info['t_previsto']}, dentro de {d} tics ({d / 24.0:.0f} s), que es cuando llegara tu respuesta.** "
            f"El cuerpo ha imaginado sus propios pasos hasta entonces con su decisor (ahora esta en ({info['pos_consulta'][0]},{info['pos_consulta'][1]}) con {info['hp_consulta']} de vida; "
            f"prevé estar en ({info['pos_prevista'][0]},{info['pos_prevista'][1]}) con {info['hp_prevista']:.0f}); los rivales se suponen quietos donde se ven o se cuentan; el hermano, donde dijo su ultimo parte; "
            f"el anillo, segun su calendario. Lo reciente es lo vivido hasta ahora. Tu plan debe partir de la casilla prevista.")


def texto28(alma, RT, V42, O, o_prev, cands, t, info, fases, hist, ult_e2, parte, plan_hermano):
    """La escena prevista: la frase, y la escena de A8 sobre la observacion prevista (anillo y rivales a t+DELTA; lo reciente, real hasta t)."""
    cuerpo = TX.texto(alma, RT, V42, O, o_prev, cands, info["t_previsto"], fases, hist, ult_e2, parte, plan_hermano)
    # el bloque de lo reciente lo calcula TX con el tick previsto: se sustituye por el real hasta la consulta
    rec_prev = TX.bloque_reciente(hist, info["t_previsto"]); rec_real = TX.bloque_reciente(hist, t)
    if rec_prev in cuerpo:
        cuerpo = cuerpo.replace(rec_prev, rec_real)
    return frase(info) + "\n\n" + cuerpo

"""[P6-18] COMPROMISO6b: VERSION NUEVA, DECLARADA, DE `compromiso6_P6_16` PARA EL PLAN
«IR Y QUEDARSE». `policy_forma._compromiso` y `compromiso6` no se tocan: esto es
`compromiso6` con DOS cambios y solo esos:

  (2') EL FIN DEL PLAN ES EL FINAL DE LA FASE, NO ESTAR A SALVO: la forma vive
       hasta el `warn` de la fase siguiente (o hasta que la puerta la cierra por
       sus puntos de control, `_revisa_vivas`), no se cumple al pisar la casilla.
  (5') ESTANDO A SALVO, EL PASO DE LA FORMA ES QUEDARSE: si la accion del cuerpo
       es un movimiento cuya casilla de llegada NO sigue a salvo (`Oraculo.a_salvo`
       en tic + 11), se emite `none` («sujeta»); los movimientos que se quedan
       dentro, los ataques, coger y usar pasan tal cual. Sin estar a salvo, se
       anda hacia el destino como en compromiso6 («obedece»).
Lo demas es compromiso6 literal: sin comprobacion de origen, ruptura (c) sin el
fuego del anillo, (b) no aplica, (a) veto vital, (d) vida/carencia, (e) rival
cerca, el enfriamiento, el coste, `D._a_json`.
"""
from __future__ import annotations
import os
import sys
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
from alma import policy_forma as PF                  # noqa: E402
from alma import decisor_zs as D                     # noqa: E402
import compromiso6_P6_16 as C6                       # noqa: E402

VERSION = "compromiso6b (P6-18): compromiso6 con fin = final de la fase y paso = quedarse (sujeta el movimiento que sale del circulo)"
log = PF.log
PASO = 11


def compromiso6b(alma, obs, accion, radio, orac):
    you = obs.get("you") or {}
    _r = alma._como_registro(obs)
    _p = tuple(you.get("pos") or ())
    nueva = {}
    for a in (_r.get("ve_agentes") or []):
        if a.get("pos") and _p:
            nueva[a.get("slot")] = max(abs(_p[0] - a["pos"][0]), abs(_p[1] - a["pos"][1]))
    _antes = alma.k_rival_dist
    alma.k_rival_dist = nueva
    if not alma.vivas:
        return accion
    fv = alma.vivas[0]
    if fv.estado != "aceptada":
        return accion
    dest = C6.destino_plan(fv)
    # (2') el fin: el final de la fase
    i = orac.fase_activa(alma.tick)
    fin = orac.fases[i + 1][0] if (i is not None and i + 1 < len(orac.fases)) else None
    if fin is not None and alma.tick >= fin:
        fv.estado = "cumplida"
        alma.vivas = [x for x in alma.vivas if x is not fv]
        alma._cierra(fv, mal=bool(fv.malos))
        alma.k6_cumplidas = getattr(alma, "k6_cumplidas", 0) + 1
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "cumplida", "por": "fin de fase", "pos": list(_p), "destino": (list(dest) if dest else None), "tics_viva": alma.tick - fv.nace})
        return accion
    if not _p:
        return accion
    salvo = orac.a_salvo(_p, alma.tick)
    mri = int(you.get("move_ready_in") or 0)
    if not salvo and mri > 0:
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "enfriamiento", "move_ready_in": mri})
        alma.k_enfria += 1
        return accion
    alma.k_rival_dist = _antes
    causa, det = C6.rupturas6(alma, obs, fv)
    alma.k_rival_dist = nueva
    if causa:
        alma.k_rupturas[causa] += 1
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "rompe", "causa": causa, "detalle": det, "a_salvo": salvo})
        return accion
    if not salvo:
        if dest is None:
            return accion
        try:
            nom = f"_FM_ir_{dest[0]}_{dest[1]}"
            vis = (obs.get("visible") or {})
            rec = {"tipo": "ir", "destino": dest, "cuerpos": frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos")), "recoger": alma.mem.objetos_vistos.get(dest)}
            acc2 = D._a_json(nom, rec, _p, alma.mundo, alma.mem, alma.tick)
        except Exception as ex:
            log({"k": "forma_error", "tick": alma.tick, "donde": "compromiso6b", "error": repr(ex)[:200]})
            return accion
        alma.k_obedece += 1
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "obedece", "paso": nom, "accion": acc2, "habria_ganado": radio.get("elegido"), "pos": list(_p), "destino": list(dest)})
        radio["elegido_cuerpo"] = radio.get("elegido"); radio["elegido"] = nom
        return acc2
    # (5') a salvo: sujetar el movimiento que sale del circulo
    if (accion or {}).get("do") == "move" and accion.get("dir") in D.DIRS:
        dx, dy = D.DIRS[accion["dir"]]
        q = (_p[0] + dx, _p[1] + dy)
        if not orac.a_salvo(q, alma.tick + PASO):
            alma.k6_sujeta = getattr(alma, "k6_sujeta", 0) + 1
            log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "sujeta", "habria_ganado": radio.get("elegido"), "hacia": list(q), "pos": list(_p)})
            radio["elegido_cuerpo"] = radio.get("elegido"); radio["elegido"] = "_FM_quedarse"
            return {"type": "action", "do": "none"}
    return accion

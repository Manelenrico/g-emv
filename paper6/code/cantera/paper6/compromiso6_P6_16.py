"""[P6-16] COMPROMISO6: VERSION NUEVA, DECLARADA, DEL COMPROMISO DE P5-8H.
`policy_forma._compromiso` (:1624) y `_rupturas` (:1563) NO se tocan: aqui va
una copia con lo que Manel fijo para el seis, y solo eso:

  1. SIN LA COMPROBACION DE ORIGEN: anda las formas de origen «consejero» (las
     del oraculo). La del cinco solo andaba las de «curiosidad».
  2. EL FIN DEL PLAN ES ESTAR A SALVO, NO VER: un viaje de curiosidad se cumple
     con la vista; un plan para salir del anillo se cumple cuando la casilla
     esta a salvo (dentro del radio de este tic Y del radio final de la fase
     activa, `oraculo_P6_14.Oraculo.a_salvo`) o al pisar el destino. Entonces
     la forma se cierra como «cumplida» y el cuerpo vuelve a lo suyo. Sin esto,
     el tramo `esperar` del plan (que existe para que la puerta mire el
     horizonte) tendria al cuerpo parado 100 tics en el destino.
  3. LA RUPTURA (c) «dano en el tic» NO cuenta el fuego del anillo (`source ==
     "zone"`): el plan es precisamente para salir del fuego. Cuenta el dano de
     agentes y proyectiles, como antes.
  4. LA RUPTURA (b) «veto duro: cubre el camino» no aplica: usa `k_camino`, el
     rodeo BFS del brazo K, que las formas del consejero no tienen.
  5. EL OBJETIVO ES EL DESTINO DEL TRAMO `ir` DEL PLAN, mientras el plan viva:
     `_revisa_vivas` avanza los puntos de control por tic (no por posicion), y
     tras el primero `destino_actual()` seria None; aqui se sigue andando al
     destino hasta el fin (2), la ruptura, o la caida de la forma.
Todo lo demas —(a) veto vital, (d) vida/carencia, (e) rival cerca, el
enfriamiento, el registro del coste, `D._a_json` para el paso— es la copia
literal. Mismo compromiso en A5v y A5h.
"""
from __future__ import annotations
import os
import sys
AQUI = os.path.dirname(os.path.abspath(__file__))
for _p in (AQUI, os.path.join(os.path.dirname(os.path.dirname(AQUI)), "cantera", "paper5"),
           os.path.join(os.path.dirname(os.path.dirname(AQUI)), "paintball")):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
from alma import policy_forma as PF                  # noqa: E402
from alma import decisor_zs as D                     # noqa: E402
from alma import appraisal_zs_v42_exp as A           # noqa: E402
import curiosidad_forma as CFM                       # noqa: E402

VERSION = "compromiso6 (P6-16): _compromiso de P5-8H sin comprobacion de origen; fin = a salvo; (c) sin fuego del anillo; (b) no aplica"
log = PF.log


def destino_plan(fv):
    """El destino del tramo `ir` del plan (el primero con destino)."""
    for tr in fv.tramos:
        if tr.get("destino"):
            return tuple(tr["destino"])
    return None


def rupturas6(alma, obs, fv):
    """Copia de `policy_forma._rupturas` con (b) fuera y (c) sin el anillo."""
    you = obs.get("you") or {}
    pos = tuple(you.get("pos") or ())
    if not pos:
        return "sin posicion", None
    r = alma._como_registro(obs)
    herm = alma.mundo.teammate_slot
    arms = CFM.armados(r, alma.mundo, herm)
    # (a) VETO VITAL
    for q, rg in arms:
        if max(abs(pos[0] - q[0]), abs(pos[1] - q[1])) <= rg:
            return "a) veto vital: armado a tiro", {"arma_en": list(q)}
    # (b) VETO DURO: no aplica (sin k_camino en las formas del consejero)
    # (c) DANO en el tic, SIN el fuego del anillo
    _dt = sum(float(x.get("amount") or 0) for x in (you.get("damage_taken") or [])
              if isinstance(x, dict) and str(x.get("source")) != "zone")
    if _dt > 0:
        return "c) dano recibido (no anillo)", {"dano": _dt}
    # (d) VIDA o CARENCIA
    hp = float(you.get("hp") or 100)
    if hp < 15:
        return "d) vida bajo 15", {"hp": hp}
    try:
        W = float(A.riqueza_W(you, alma.mundo)[0])
    except Exception:
        W = None
    if W is not None:
        w0 = getattr(fv, "W_nace", None)
        if w0 is not None and W < w0 - 1e-9:
            return "d) carencia sube (pierde de las manos)", {"W": W, "W0": w0}
    # (e) RIVAL CERCA
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") == herm or not a.get("pos"):
            continue
        q = tuple(a["pos"])
        d = max(abs(pos[0] - q[0]), abs(pos[1] - q[1]))
        if d <= 2:
            return "e) rival a 2 o menos", {"slot": a.get("slot"), "d": d}
        if d < 6 and CFM._alcance_de(alma.mundo, a) > 0:
            prev = (alma.k_rival_dist or {}).get(a.get("slot"))
            if prev is not None and d < prev:
                return "e) armado a menos de 6 y acercandose", \
                    {"slot": a.get("slot"), "d": d, "antes": prev}
    return None, None


def compromiso6(alma, obs, accion, radio, orac):
    """Con piernas listas y sin ruptura, se EJECUTA el paso de la forma."""
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
    dest = destino_plan(fv)
    # 2 · EL FIN: a salvo, o en el destino
    if _p and (orac.a_salvo(_p, alma.tick) or (dest is not None and _p == dest)):
        fv.estado = "cumplida"
        alma.vivas = [x for x in alma.vivas if x is not fv]
        alma._cierra(fv, mal=bool(fv.malos))
        alma.k6_cumplidas = getattr(alma, "k6_cumplidas", 0) + 1
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "cumplida",
             "por": ("destino" if dest is not None and _p == dest else "a salvo"),
             "pos": list(_p), "destino": (list(dest) if dest else None),
             "tics_viva": alma.tick - fv.nace})
        return accion
    if dest is None:
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "sin destino"})
        return accion
    mri = int(you.get("move_ready_in") or 0)
    if mri > 0:
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "enfriamiento",
             "move_ready_in": mri})
        alma.k_enfria += 1
        return accion
    alma.k_rival_dist = _antes          # (e) compara contra el tic previo
    causa, det = rupturas6(alma, obs, fv)
    alma.k_rival_dist = nueva
    if causa:
        alma.k_rupturas[causa] += 1
        log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "rompe",
             "causa": causa, "detalle": det})
        return accion
    # OBEDECE: se ejecuta el paso de la forma hacia el destino del plan
    try:
        nom = f"_FM_ir_{dest[0]}_{dest[1]}"
        vis = (obs.get("visible") or {})
        rec = {"tipo": "ir", "destino": dest,
               "cuerpos": frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos")),
               "recoger": alma.mem.objetos_vistos.get(dest)}
        acc2 = D._a_json(nom, rec, _p, alma.mundo, alma.mem, alma.tick)
    except Exception as ex:
        log({"k": "forma_error", "tick": alma.tick, "donde": "compromiso6", "error": repr(ex)[:200]})
        return accion
    _cds = {k: (v["d"] if isinstance(v, dict) else v) for k, v in (radio.get("candidatos") or {}).items()}
    d_forma = _cds.get(nom)
    d_gana = _cds.get(radio.get("elegido"))
    coste = ((d_forma - d_gana) if (d_forma is not None and d_gana is not None) else None)
    if coste is not None:
        alma.k_coste.append(coste)
    alma.k_obedece += 1
    log({"k": "compromiso6", "tick": alma.tick, "id": fv.id, "estado": "obedece", "paso": nom,
         "accion": acc2, "habria_ganado": radio.get("elegido"), "d_forma": d_forma, "d_ganador": d_gana,
         "coste": (round(coste, 5) if coste is not None else None), "pos": list(_p), "destino": list(dest)})
    radio["elegido_cuerpo"] = radio.get("elegido")
    radio["elegido"] = nom
    return acc2

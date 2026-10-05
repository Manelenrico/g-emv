"""[P6-23] COMPROMISO6c: VERSION NUEVA, DECLARADA, DE `compromiso6b_P6_18` CON EL VETO V2 DE
MANEL Y LA CUENTA JUSTA DEL ABANDONO (P6-20). `compromiso6b` no se toca. Cambios, y solo estos:

  (a') VER UN ARMA NO ROMPE. Las rupturas «a) veto vital: armado a tiro» y «e) armado a menos
       de 6 y acercandose» dejan de romper: ponen al cuerpo en ALERTA (se registra cuando cambia
       el conjunto de armados a tiro). Quedan «e) rival a 2 o menos» SOLO para rivales sin
       alcance (con V0, a) saltaba antes para los armados, asi que esta regla solo veia manos
       vacias: se declara y se mantiene igual) y «d) vida bajo 15 / carencia».
  (c') EL PRIMER GOLPE SUSPENDE, NO ROMPE. Un golpe de rival (`damage_taken` con `source`
       distinto de zone) con el plan vivo SUSPENDE el plan: manda la tabla del cuerpo (se
       devuelve su accion) hasta que pasan N = 96 tics sin golpe (cada golpe renueva); entonces
       el plan se REANUDA. Suspendido y a salvo, si la accion del cuerpo sale del circulo
       (casilla de llegada no a salvo en tick + 11) solo se deja salir si el dano esperado
       dentro (tabla arma x distancia de P6-19, `puerta6g_P6_19.dano_esperado` en la casilla
       actual, sobre los rivales vistos y contados) es mayor que el fuego de fuera (dps de la
       fase / tick_rate): «sale»; si no, se retiene (`none`): «retenido».
  (j)  LA CUENTA JUSTA. Desde una ruptura hasta volver a estar a salvo (desviado), el dano
       recibido (fuego y golpes) se apunta en `fv.dano_desviado`; `policy_pareja23._revisa_vivas`
       compara `hp + dano_desviado` con la vida proyectada menos 10. Los golpes recibidos
       siguiendo el plan o en suspension cuentan contra el plan (decision de metodo, P6-20 §3).
Lo demas es compromiso6b literal: fin = final de la fase (cumplida), enfriamiento, obedece
(anda hacia el destino con `D._a_json`), sujeta (a salvo, retiene el paso que sale), el coste.
"""
from __future__ import annotations
import os
import sys
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
from alma import policy_forma as PF                  # noqa: E402
from alma import decisor_zs as D                     # noqa: E402
from alma import appraisal_zs_v42_exp as A           # noqa: E402
import curiosidad_forma as CFM                       # noqa: E402
import compromiso6_P6_16 as C6                       # noqa: E402
import puerta6g_P6_19 as G                           # noqa: E402

VERSION = "compromiso6c (P6-23): compromiso6b + veto V2 (alerta al ver arma, suspension al primer golpe, N=96, sale solo si dentro se pierde mas) + cuenta justa"
log = PF.log
PASO = 11
N_REANUDA = 96
VIDA_MIN = 15.0


def _armados_a_tiro(alma, obs, pos):
    r = alma._como_registro(obs)
    herm = alma.mundo.teammate_slot
    out = []
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") == herm or not a.get("pos"):
            continue
        rg = CFM._alcance_de(alma.mundo, a)
        if rg > 0 and max(abs(pos[0] - a["pos"][0]), abs(pos[1] - a["pos"][1])) <= rg:
            out.append(int(a.get("slot")))
    return sorted(out)


def rupturas6c(alma, obs, fv):
    """Las rupturas que quedan: (d) vida / carencia y (e) rival SIN alcance a 2 o menos."""
    you = obs.get("you") or {}
    pos = tuple(you.get("pos") or ())
    if not pos:
        return "sin posicion", None
    hp = float(you.get("hp") or 100)
    if hp < VIDA_MIN:
        return "d) vida bajo 15", {"hp": hp}
    try:
        W = float(A.riqueza_W(you, alma.mundo)[0])
    except Exception:
        W = None
    if W is not None:
        w0 = getattr(fv, "W_nace", None)
        if w0 is not None and W < w0 - 1e-9:
            return "d) carencia sube (pierde de las manos)", {"W": W, "W0": w0}
    r = alma._como_registro(obs)
    herm = alma.mundo.teammate_slot
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") == herm or not a.get("pos"):
            continue
        q = tuple(a["pos"]); d = max(abs(pos[0] - q[0]), abs(pos[1] - q[1]))
        if d <= 2 and CFM._alcance_de(alma.mundo, a) <= 0:
            return "e) rival a 2 o menos", {"slot": a.get("slot"), "d": d}
    return None, None


def compromiso6c(alma, obs, accion, radio, orac):
    you = obs.get("you") or {}
    _p = tuple(you.get("pos") or ())
    if not alma.vivas:
        return accion
    fv = alma.vivas[0]
    if fv.estado != "aceptada":
        return accion
    t = alma.tick
    dest = C6.destino_plan(fv)
    # (2') el fin: el final de la fase
    i = orac.fase_activa(t)
    fin = orac.fases[i + 1][0] if (i is not None and i + 1 < len(orac.fases)) else None
    if fin is not None and t >= fin:
        fv.estado = "cumplida"
        alma.vivas = [x for x in alma.vivas if x is not fv]
        alma._cierra(fv, mal=bool(fv.malos))
        alma.k6_cumplidas = getattr(alma, "k6_cumplidas", 0) + 1
        log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "cumplida", "por": "fin de fase", "pos": list(_p), "destino": (list(dest) if dest else None), "tics_viva": t - fv.nace,
             "dano_desviado": round(getattr(fv, "dano_desviado", 0.0), 2), "suspensiones": getattr(fv, "n_susp", 0)})
        return accion
    if not _p:
        return accion
    salvo = orac.a_salvo(_p, t)
    # (j) la cuenta justa: el dano de los tics desviados (desde una ruptura hasta volver a estar a salvo)
    dano_tic = sum(float(x.get("amount") or 0) for x in (you.get("damage_taken") or []) if isinstance(x, dict))
    golpe = sum(float(x.get("amount") or 0) for x in (you.get("damage_taken") or []) if isinstance(x, dict) and str(x.get("source")) != "zone")
    if getattr(fv, "desviado", False):
        if salvo:
            fv.desviado = False
        else:
            fv.dano_desviado = getattr(fv, "dano_desviado", 0.0) + dano_tic
    # (a') la alerta: cambia el conjunto de armados a tiro
    arm = _armados_a_tiro(alma, obs, _p)
    if arm != getattr(fv, "alerta", []):
        if arm:
            log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "alerta", "armados_a_tiro": arm, "a_salvo": salvo})
            alma.k6_alertas = getattr(alma, "k6_alertas", 0) + 1
        fv.alerta = arm
    # (c') el primer golpe suspende; 96 tics sin golpe reanudan
    if golpe > 0:
        if not getattr(fv, "suspendida", False):
            fv.suspendida = True; fv.n_susp = getattr(fv, "n_susp", 0) + 1
            alma.k6_suspensiones = getattr(alma, "k6_suspensiones", 0) + 1
            log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "suspende", "golpe": golpe, "hp": you.get("hp"), "a_salvo": salvo, "pos": list(_p)})
        fv.ult_golpe = t
    elif getattr(fv, "suspendida", False) and t - getattr(fv, "ult_golpe", t) > N_REANUDA:
        fv.suspendida = False
        alma.k6_reanudaciones = getattr(alma, "k6_reanudaciones", 0) + 1
        log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "reanuda", "sin_golpe_desde": getattr(fv, "ult_golpe", None), "a_salvo": salvo, "pos": list(_p)})
    if getattr(fv, "suspendida", False):
        alma.k6_tics_suspendida = getattr(alma, "k6_tics_suspendida", 0) + 1
        # manda la tabla; sale del circulo solo si dentro se pierde mas que fuera
        if salvo and (accion or {}).get("do") == "move" and accion.get("dir") in D.DIRS:
            dx, dy = D.DIRS[accion["dir"]]; q = (_p[0] + dx, _p[1] + dy)
            if not orac.a_salvo(q, t + PASO):
                esp = G.dano_esperado(_p, obs, alma.mundo)
                fuego = float(orac.radio_dps(t)[1]) / float(alma.mundo.tick_rate)
                if esp > fuego:
                    alma.k6_sale = getattr(alma, "k6_sale", 0) + 1
                    log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "sale", "esperado_dentro": round(esp, 4), "fuego_fuera": round(fuego, 4), "hacia": list(q), "pos": list(_p)})
                    return accion
                alma.k6_retenido = getattr(alma, "k6_retenido", 0) + 1
                log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "retenido", "esperado_dentro": round(esp, 4), "fuego_fuera": round(fuego, 4), "hacia": list(q), "pos": list(_p), "habria_ganado": radio.get("elegido")})
                radio["elegido_cuerpo"] = radio.get("elegido"); radio["elegido"] = "_FM_retenido"
                return {"type": "action", "do": "none"}
        return accion
    mri = int(you.get("move_ready_in") or 0)
    if not salvo and mri > 0:
        log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "enfriamiento", "move_ready_in": mri})
        alma.k_enfria += 1
        return accion
    causa, det = rupturas6c(alma, obs, fv)
    if causa:
        alma.k_rupturas[causa] += 1
        fv.desviado = True
        log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "rompe", "causa": causa, "detalle": det, "a_salvo": salvo})
        return accion
    if not salvo:
        if dest is None:
            return accion
        try:
            nom = f"_FM_ir_{dest[0]}_{dest[1]}"
            vis = (obs.get("visible") or {})
            rec = {"tipo": "ir", "destino": dest, "cuerpos": frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos")), "recoger": alma.mem.objetos_vistos.get(dest)}
            acc2 = D._a_json(nom, rec, _p, alma.mundo, alma.mem, t)
        except Exception as ex:
            log({"k": "forma_error", "tick": t, "donde": "compromiso6c", "error": repr(ex)[:200]})
            return accion
        alma.k_obedece += 1
        log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "obedece", "paso": nom, "accion": acc2, "habria_ganado": radio.get("elegido"), "pos": list(_p), "destino": list(dest)})
        radio["elegido_cuerpo"] = radio.get("elegido"); radio["elegido"] = nom
        return acc2
    # (5') a salvo: sujetar el movimiento que sale del circulo
    if (accion or {}).get("do") == "move" and accion.get("dir") in D.DIRS:
        dx, dy = D.DIRS[accion["dir"]]
        q = (_p[0] + dx, _p[1] + dy)
        if not orac.a_salvo(q, t + PASO):
            alma.k6_sujeta = getattr(alma, "k6_sujeta", 0) + 1
            log({"k": "compromiso6", "tick": t, "id": fv.id, "estado": "sujeta", "habria_ganado": radio.get("elegido"), "hacia": list(q), "pos": list(_p)})
            radio["elegido_cuerpo"] = radio.get("elegido"); radio["elegido"] = "_FM_quedarse"
            return {"type": "action", "do": "none"}
    return accion

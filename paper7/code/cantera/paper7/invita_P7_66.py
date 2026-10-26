"""[P7-66] UNA INVITACION QUE APUNTA A UN SITIO, SEGUIBLE EN CALMA (decisiones de la mesa, 16-oct; GEMV_P7_66=1). Pieza nueva, enganchada DESPUES de invita_P7_54 (y de
P7-57/62/65, que no se tocan) y antes de rapido_P7_43. motor/model.py no se toca.
  (a) ACCION NUEVA del menu: IR_A_SITIO con `destino` [x, y] («ve a tal sitio, alli hay botiquines»; promesa recursos +1; cuerpo 0 y vinculo 0).
  (b) CANDIDATO: mientras una invitacion IR_A_SITIO esta activa, se anade a la lista del cuerpo el candidato `ir_sitio` = receta generica «ir» del decisor con ese destino (el
      cuerpo lo imagina y lo anda como ir_botin / ir_objeto / ir_centro, por el camino geodesico); se empareja con la invitacion en la lista de invita_P7_54 (E["cands"], E["match"]),
      asi la invitacion le anade a su foto imaginada la fila INVITACION-RECURSOS como a cualquier otra. No se anade si ya esta a <= 1 casilla del destino.
  (c) CALMA: la invitacion lleva calma5="CALMA5": solo esta activa (solo empuja) si no hay ningun rival visible a <= 5 casillas (ni ella ni su hermana cuentan) y ningun golpe en los 48
      tics anteriores. Se anade a la situacion de invita_P7_54 (IN.situacion / IN.cumple, por fuera, como P7-57 y P7-63).
  (d) JUICIO (solo recursos): aceptada (el cuerpo elige ir_sitio), se le quita a invita_P7_54 (que no la juzga: en su lista queda una «sombra» que la ve abierta y nunca juzga, como en
      juicio_P7_62) y la juzga esta pieza, tic a tic, en una ventana de 480 tics:
        LLEGADA = a <= 1 casilla del destino: acierto de recursos = 1 si ve un botiquin a <= 1 casilla del destino, 0 si no (la mentira falla en el acto);
                  confianza en recursos <- 0,7 c + 0,3 acierto; cuerpo y vinculo no se juzgan y su confianza no se toca.
        INTERRUMPIDA = antes de llegar aparece un rival a <= 5 casillas: no se juzga, no cambia la confianza; se cuenta aparte.
        NO LLEGO = pasan 480 tics sin llegar ni interrumpirse: no se juzga, no cambia la confianza; se cuenta aparte.
Registros: P7_66_arranque, P7_66_aceptada (destino, distancia), P7_66_llegada (acierto, botiquin visto, confianza antes / despues), P7_66_interrumpida, P7_66_no_llego, P7_66_cierre."""
import os
import descubre_P7 as X, nace_P7_23 as N, invita_P7_54 as IN
from alma import decisor_zs as D
ON = os.environ.get("GEMV_P7_66", "0") == "1"
ACCION = "IR_A_SITIO"; RIVAL_CALMA = 5; GOLPE_TICS = 48; VENTANA = 480; LLEGA = 1
E = {"abiertas": [], "calma": False, "pos": None, "rival_min": None, "kits": [], "n": {"aceptadas": 0, "llegadas": 0, "aciertos": 0, "interrumpidas": 0, "no_llego": 0}}


def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def lee_obs(obs, mundo, tick, slot):
    """lo que esta pieza necesita del tic: posicion, rival mas cercano (no ella ni su hermana), botiquines a la vista, calma"""
    you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); vis = obs.get("visible") or {}
    riv = [cheb(pos, tuple(a["pos"])) for a in (vis.get("agents") or []) if a.get("pos") and a.get("slot") not in (mundo.slot, mundo.teammate_slot)]
    kits = [tuple(it["pos"]) for it in (vis.get("items") or []) if it.get("pos") and it.get("id") == X.kit(mundo)]
    u = N.E.get("ultimo_dano"); golpe = bool(u is not None and 0 <= tick - u <= GOLPE_TICS)
    rmin = min(riv) if riv else None
    return pos, rmin, kits, (not (rmin is not None and rmin <= RIVAL_CALMA)) and not golpe


def juicio(a, tick, pos, rmin, kits):
    """-> ("llegada", acierto) | ("interrumpida", None) | ("no_llego", None) | None (sigue abierta). a: {"inv", "t0", "destino"}"""
    dest = tuple(a["destino"])
    if cheb(pos, dest) <= LLEGA: return "llegada", (1 if any(cheb(k, dest) <= LLEGA for k in kits) else 0)
    if rmin is not None and rmin <= RIVAL_CALMA: return "interrumpida", None
    if tick - a["t0"] >= VENTANA: return "no_llego", None
    return None


def sombra(a):
    return {"inv": a["inv"], "t0": 10 ** 9, "hp0": a.get("hp0"), "W0": None, "B0": None, "objeto": "__invita_P7_66__", "n_huellas0": 0, "_sombra66": True}


def aplica(clase, registra=None):
    if not ON: return {"P7_66": False}
    assert IN.ON, "P7-66 va sobre invita_P7_54"
    # (c) la calma en la situacion
    _os, _oc = IN.situacion, IN.cumple
    def situacion(self, obs, mundo, tick):
        s = _os(self, obs, mundo, tick); s["calma5"] = "CALMA5" if E["calma"] else "SIN_CALMA5"; return s
    def cumple(inv, s): return _oc(inv, s) and inv.get("calma5", "CUALQUIERA") in ("CUALQUIERA", s.get("calma5"))
    IN.situacion, IN.cumple = situacion, cumple
    # (b) el candidato ir_sitio, emparejado con su invitacion en la lista de invita_P7_54
    _oca = D.candidatos
    def _cands(obs, mundo, mem, tick, bloqueos=None):
        out = _oca(obs, mundo, mem, tick, bloqueos)
        pos = E["pos"]
        for inv in IN.E.get("activas") or []:
            if inv.get("accion") != ACCION or pos is None: continue
            dest = (int(inv["destino"][0]), int(inv["destino"][1]))
            if cheb(pos, dest) <= LLEGA or mundo.solido(dest[0], dest[1]): continue
            cuerpos = frozenset(tuple(a.get("pos") or ()) for a in ((obs.get("visible") or {}).get("agents") or []) if a.get("pos"))
            out = list(out); out.append(("ir_sitio", {"tipo": "ir", "destino": dest, "cuerpos": cuerpos}))
            IN.E["cands"].append("ir_sitio"); IN.E["match"][len(out) - 1] = inv
            break
        return out
    D.candidatos = _cands
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        E["abiertas"] = []; c = _oa(criatura, ruta, registra_)
        if registra_: registra_({"k": "P7_66_arranque", "slot": int(criatura), "invitaciones_sitio": [{"destino": i.get("destino"), "falsa": bool(i.get("falsa"))} for i in IN.E["inv"] if i.get("accion") == ACCION], "confianza": dict(IN.E["conf"])})
        return c
    X.arranca = arranca
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        mundo = self.mundo; tick = getattr(self, "tick", 0); live = mundo is not None and getattr(self, "phase", None) == "live"
        if live: E["pos"], E["rival_min"], E["kits"], E["calma"] = lee_obs(obs, mundo, tick, None)
        accion, radio = _d(self, obs)
        if not live or radio is None: return accion, radio
        # (d) las aceptadas pasan a esta pieza; en invita_P7_54 queda su sombra
        for a in [a for a in IN.E["abiertas"] if a["inv"].get("accion") == ACCION and not a.get("_sombra66")]:
            IN.E["abiertas"].remove(a); IN.E["abiertas"].append(sombra(a)); b = {"inv": a["inv"], "t0": a["t0"], "destino": tuple(a["inv"]["destino"])}; E["abiertas"].append(b); E["n"]["aceptadas"] += 1
            if registra: registra({"k": "P7_66_aceptada", "tick": tick, "n": a["inv"]["_k"], "falsa": bool(a["inv"].get("falsa")), "destino": list(b["destino"]), "distancia": cheb(E["pos"], b["destino"]), "confianza": dict(IN.E["conf"])})
        queda = []
        for a in E["abiertas"]:
            r = juicio(a, tick, E["pos"], E["rival_min"], E["kits"])
            if r is None: queda.append(a); continue
            IN.E["abiertas"] = [x for x in IN.E["abiertas"] if not (x.get("_sombra66") and x["inv"]["_k"] == a["inv"]["_k"])]
            que, ac = r; base = {"tick": tick, "n": a["inv"]["_k"], "falsa": bool(a["inv"].get("falsa")), "destino": list(a["destino"]), "t_aceptada": a["t0"], "tics": tick - a["t0"]}
            if que == "llegada":
                antes = dict(IN.E["conf"]); IN.E["conf"]["recursos"] = (1 - IN.ETA) * IN.E["conf"]["recursos"] + IN.ETA * ac      # solo recursos
                E["n"]["llegadas"] += 1; E["n"]["aciertos"] += ac
                if registra: registra({"k": "P7_66_llegada", **base, "acierto_recursos": ac, "botiquines_vistos": [list(k) for k in E["kits"]], "confianza_antes": antes, "confianza_despues": dict(IN.E["conf"])})
            elif que == "interrumpida":
                E["n"]["interrumpidas"] += 1
                if registra: registra({"k": "P7_66_interrumpida", **base, "rival_a": E["rival_min"], "distancia_al_destino": cheb(E["pos"], a["destino"])})
            else:
                E["n"]["no_llego"] += 1
                if registra: registra({"k": "P7_66_no_llego", **base, "distancia_al_destino": cheb(E["pos"], a["destino"])})
        E["abiertas"] = queda
        return accion, radio
    clase.decidir = decidir
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_66_cierre", "n": dict(E["n"]), "pendientes": len(E["abiertas"]), "confianza": dict(IN.E["conf"])})
        return _ot(registra_)
    X.termina = termina
    return {"P7_66": True}

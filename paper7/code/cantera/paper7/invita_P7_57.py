"""[P7-57] LA CONFIANZA EN LA RAZON TAMBIEN CON LO CONTADO (capitulo 5, la mentira; diseno de Manel). GEMV_P7_57=1, enganchada DESPUES de invita_P7_54 (que no se toca:
la serie 3 de P7-56 la usa). Dos cosas:
  (0) SITUACION "amenaza" (Manel, 13-oct): AMENAZA = rival a <= 4 casillas, fuego, o golpe recibido en los ultimos 48 tics (2 s); SIN "vida < 30" (usar el botiquin con poca vida
      y sin golpes es un consejo verdadero). La falsa la usa en vez de calma=PELIGRO (que en P7-33 incluye vida < 30).
  (1) SITUACION "vida": una invitacion puede llevar vida=HERIDA (activa solo con vida < 70) o SANA (>= 70); se anade al chequeo de situacion de invita_P7_54 (envolviendo
      IN.situacion e IN.cumple, que su decidir busca en el modulo en cada tic). La invitacion falsa del estafador la usa.
  (2) CONTRASTE CON LO CONTADO: cada recuerdo recibido de la hermana (contado por canal o noche, o visto) sobre una cosa que alguna invitacion cargada de mi razon promete en el
      CUERPO se compara con esa promesa: acierto = signo igual y |efecto contado| >= |promesa| / 2 (o los dos < 1); un recuerdo "al menos" (la vida toco techo) no puede
      desmentir una promesa mayor que su efecto y se salta. confianza.cuerpo <- c + eta x (acierto - c), con eta = 0,3 x min(1, 0,5 x intensidad x B) (Manel, 13-oct: lo contado pesa la mitad
      que lo vivido en la CONFIANZA; en las creencias sigue entrando con intensidad x B, como en P7-56, para que el campo sea comparable). Solo la dimension cuerpo. Cosa de cada accion: USAR/COGER_BOTIQUIN -> botiquin; USAR/COGER_RACION -> racion; EMPUNAR/COGER_RED -> red;
      PONERSE/COGER_CAMUFLAJE -> camuflaje.
Registros: P7_57_arranque, P7_57_contraste (objeto, via, efecto contado, peso, invitacion, promesa, acierto, eta, confianza antes/despues), P7_57_cierre."""
import os
import descubre_P7 as X, nace_P7_23 as N, nace_P7_33 as N33, invita_P7_54 as IN
ON = os.environ.get("GEMV_P7_57", "0") == "1"; HERIDA = 70.0; GOLPE_TICS = 48; ETA = 0.3; PESO_CONTADO = 0.5
E = {"vistos": set(), "n_contrastes": 0, "registra": None, "hp": 100.0}


def objeto_de(accion, mundo):
    return {"USAR_BOTIQUIN": X.kit(mundo), "COGER_BOTIQUIN": X.kit(mundo), "USAR_RACION": N.racion(mundo), "COGER_RACION": N.racion(mundo), "EMPUNAR_RED": N33.red(mundo), "COGER_RED": N33.red(mundo),
            "PONERSE_CAMUFLAJE": N33.camo(mundo), "COGER_CAMUFLAJE": N33.camo(mundo)}.get(accion)


def contrasta(c, mundo, tick, registra):
    """los recibidos nuevos (contado/visto) frente a las promesas de cuerpo de mis invitaciones cargadas"""
    if c is None or mundo is None or not IN.E["inv"]: return
    for o_, s_, r in c.recuerdos():
        if r.get("origen") not in ("contado", "visto") or r.get("corte"): continue
        k = (o_, r.get("via"), r.get("dia_emisora", r.get("dia")), r.get("tick_emisora", r.get("tick")))
        if k in E["vistos"]: continue
        E["vistos"].add(k); e = float((r.get("efecto") or {}).get("cuerpo") or 0.0); w = PESO_CONTADO * float(r.get("intensidad") or 0.0); eta = ETA * min(1.0, w)      # [Manel, 13-oct] lo contado pesa la mitad que lo vivido en la confianza
        juicios = []
        for inv in IN.E["inv"]:
            if objeto_de(inv["accion"], mundo) != o_: continue
            p = float(inv.get("cuerpo") or 0.0)
            if abs(p) < 1e-9 or (r.get("al_menos") and p > e): continue
            juicios.append((inv, p, 1 if (abs(e) < 1.0 and abs(p) < 1.0) or ((p > 0) == (e > 0) and abs(e) >= abs(p) / 2) else 0))
        if not juicios: continue
        ac = sum(j[2] for j in juicios) / len(juicios)          # UNA actualizacion por recuerdo recibido (si toca a varias invitaciones, la media de sus aciertos)
        antes = IN.E["conf"]["cuerpo"]; IN.E["conf"]["cuerpo"] = antes + eta * (ac - antes); E["n_contrastes"] += 1
        if registra: registra({"k": "P7_57_contraste", "tick": tick, "objeto": o_, "origen": r.get("origen"), "via": r.get("via"), "efecto_contado": round(e, 3), "peso": round(w, 3), "invitaciones": [j[0].get("_k") for j in juicios], "acciones": [j[0]["accion"] for j in juicios], "falsa": any(j[0].get("falsa") for j in juicios), "promesas": [j[1] for j in juicios], "acierto": round(ac, 3), "eta": round(eta, 3), "confianza_antes": round(antes, 4), "confianza_despues": round(IN.E["conf"]["cuerpo"], 4)})


def aplica(clase, registra=None):
    if not ON: return {"P7_57": False}
    assert IN.ON, "P7-57 va sobre invita_P7_54"
    E["registra"] = registra
    _os, _oc = IN.situacion, IN.cumple
    def situacion(self, obs, mundo, tick):
        s = _os(self, obs, mundo, tick); hp = float((obs.get("you") or {}).get("hp") or 0.0); E["hp"] = hp; s["vida"] = "HERIDA" if hp < HERIDA else "SANA"
        pel = N33.peligro_de(self, obs); golpe = (tick - int(N.E.get("ultimo_dano") or -10 ** 9)) <= GOLPE_TICS
        s["amenaza"] = "AMENAZA" if (pel.get("rival_a_4") or pel.get("fuego") or golpe) else "SIN_AMENAZA"; return s
    def cumple(inv, s): return _oc(inv, s) and inv.get("vida", "CUALQUIERA") in ("CUALQUIERA", s.get("vida")) and inv.get("amenaza", "CUALQUIERA") in ("CUALQUIERA", s.get("amenaza"))
    IN.situacion, IN.cumple = situacion, cumple
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        c = _oa(criatura, ruta, registra_); E["vistos"] = set()
        if registra_: registra_({"k": "P7_57_arranque", "slot": int(criatura), "invitaciones": len(IN.E["inv"]), "falsas": sum(1 for i in IN.E["inv"] if i.get("falsa")), "confianza": dict(IN.E["conf"])})
        return c
    X.arranca = arranca
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        accion, radio = _d(self, obs)
        if getattr(self, "phase", None) == "live" and self.mundo is not None:
            import hermanas_P7_48 as HE
            k = (HE.E["n"].get("canal", 0), HE.E["n"].get("noche", 0), HE.E["n"].get("visto", 0))
            if k != E.get("ult_n"): E["ult_n"] = k; contrasta(N.cuaderno(), self.mundo, self.tick, registra)
        return accion, radio
    clase.decidir = decidir
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_57_cierre", "contrastes": E["n_contrastes"], "confianza": dict(IN.E["conf"])})
        return _ot(registra_)
    X.termina = termina
    return {"P7_57": True, "herida_bajo": HERIDA}

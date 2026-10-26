"""[P7-62] EL JUICIO DE LA MENTIRA, ARREGLADO (metodo de la mesa; GEMV_P7_62=1). Pieza nueva, enganchada DESPUES de invita_P7_54 e invita_P7_57 (que no se tocan: P7-56 y P7-61
las usaron) y antes de rapido_P7_43. Tres arreglos:
  REGLA DEL MUNDO (Ari, 7-oct, zero-sum v0.1.19; Manel, 14-oct): el botiquin cura solo tras su canalizacion (use_ticks del catalogo del player_config: 48 tics = 2 s) sin recibir
  dano; cualquier golpe en la canalizacion la interrumpe (se puede reintentar: otro uso); la racion (use_ticks 24 = 1 s) NO la interrumpe el dano. Los use_ticks se LEEN del mundo
  (mundo.items), no se cablean; que cosa interrumpe el dano es la regla de Ari (solo el botiquin, por su id del mundo).
  (a) CURA CORTADA POR UN GOLPE = FALLO, EN EL MOMENTO. Las invitaciones de CURA (USAR_BOTIQUIN, USAR_RACION) aceptadas ya no las juzga invita_P7_54 (que saltaba el uso cortado y
      esperaba a la siguiente cura sin golpe): las juzga esta pieza con el PRIMER uso de esa cosa tras aceptar (huella con t0 >= tic de la aceptacion). Si es un botiquin y hubo un golpe
      DENTRO DE SU CANALIZACION (algun tic con dano en [t0, t0 + use_ticks], de los golpes que esta pieza apunta tic a tic), la cura se corto: acierto de cuerpo = 0 en ese tic
      (aunque la huella no lleve la marca de corte). Una racion no se corta por un golpe (regla del mundo). Se aplica a TODA invitacion de cura, no solo a la falsa: el cuerpo no puede saber cual es la falsa (declarado).
      Una huella marcada de corte sin golpe en la canalizacion (o de racion) no juzga: se espera al siguiente uso (como antes).
  (b) EL HUECO: si el uso no se corto, la cura se juzga contra el hueco disponible: acierto si cura al menos la mitad de min(promesa, 100 - vida al empezar el uso) (para la falsa,
      min(50, 100 - vida)); si el hueco es < 1 (ya estaba entera), no hay nada que juzgar en el cuerpo y cuenta como acierto si no bajo (como «las dos cosas < 1» de P7-54).
      Igual para toda invitacion de cura (declarado). Una promesa de cuerpo <= 0 y las dimensiones recursos y vinculo: regla de P7-54 sin cambio. Sin uso en 480 tics: cambio de vida
      (regla de P7-54), juzgado tambien contra el hueco de la vida al aceptar.
  (c) LO CONTADO SOLO EN SU SITUACION: el contraste con lo contado (invita_P7_57.contrasta, que se sustituye por fuera) solo junta un recuerdo recibido con una invitacion que pone
      condicion de amenaza (AMENAZA / SIN_AMENAZA: la falsa) si el recuerdo trae su amenaza y es la misma. La amenaza de un recuerdo es la de la falsa (rival a <= 4 casillas o fuego al
      empezar el uso, o golpe en los 48 tics anteriores), apuntada en su contexto al vivirlo (`contexto.amenaza`), y viaja: por el canal, en el caracter del golpe del M7 (0-3 = golpe +
      2 x amenaza, mismo largo; hermanas_P7_48.codifica/parsea se sustituyen por fuera) y por la noche, del cuaderno de la hermana. Un «visto» no trae la amenaza de la hermana (solo
      la de quien mira): para las invitaciones con condicion de amenaza no entra. Las invitaciones sin condicion de amenaza (las honestas) se contrastan como en P7-57.
Registros: P7_62_arranque, P7_62_evaluada (como P7_54_evaluada + fuente, hueco, vida al empezar, corte), P7_62_contraste (como P7_57_contraste + amenaza del recuerdo), P7_62_cierre."""
import json, os, re
import descubre_P7 as X, nace_P7_23 as N, nace_P7_33 as N33, invita_P7_54 as IN, invita_P7_57 as IC
ON = os.environ.get("GEMV_P7_62", "0") == "1"
CURAS = ("USAR_BOTIQUIN", "USAR_RACION"); VIDA_MAX = 100.0
E = {"abiertas": [], "golpes": [], "canal": {}, "interrumpe": set(), "amenaza_tic": None, "rival_fuego": False, "n": {"evaluadas": 0, "cortadas": 0, "hueco": 0, "sin_huella": 0, "contrastes": 0, "fuera_de_situacion": 0}, "hermana_cache": None}


# ── la amenaza de ahora (la de la falsa) ──
def amenaza_ahora(tick):
    u = N.E.get("ultimo_dano"); golpe = bool(u is not None and 0 <= tick - u <= IC.GOLPE_TICS)
    return bool((E["rival_fuego"] and E["amenaza_tic"] == tick) or golpe)


# ── (b) y (a): el juicio de una cura ──
def acierto_dim(p, v):
    """regla de P7-54 por dimension"""
    if abs(p) < 1e-9: return 1 if abs(v) < 1.0 else 0
    return 1 if (p > 0) == (v > 0) and abs(v) >= abs(p) / 2 else 0


def juzga_cuerpo(p, v, hp0):
    """(b) promesa de cura > 0: contra el hueco min(p, 100 - hp0); si no, la regla de P7-54."""
    if p <= 0: return acierto_dim(p, v), None
    hueco = max(0.0, VIDA_MAX - float(hp0)); obj = min(p, hueco)
    if obj < 1.0: return (1 if v > -1.0 else 0), round(obj, 3)
    return (1 if v >= obj / 2 else 0), round(obj, 3)


def cortada(h, golpes, canal, interrumpe):
    """regla del mundo: un uso de una cosa que el dano interrumpe se corta si hay un golpe en su canalizacion [t0, t0 + use_ticks]"""
    o = h.get("objeto"); t0 = int(h.get("t0") or 0); n = int(canal.get(o) or 0)
    return o in interrumpe and n > 0 and any(t0 <= g <= t0 + n for g in golpes)


def juicio(a, huellas, tick, hp, W, B, golpes=(), canal=None, interrumpe=None):
    """-> (vivido, acierto, fuente, extra) o None si aun no se puede juzgar. a: la abierta de invita_P7_54 (inv, t0, hp0, W0, B0, objeto, n_huellas0); golpes: tics con dano;
    canal: use_ticks por id del mundo; interrumpe: ids que el dano interrumpe (el botiquin)."""
    canal = E["canal"] if canal is None else canal; interrumpe = E["interrumpe"] if interrumpe is None else interrumpe
    p = {d: float(a["inv"].get(d) or 0.0) for d in ("cuerpo", "recursos", "vinculo")}
    for h in huellas[a.get("n_huellas0", 0):]:
        if (h.get("objeto") or a["objeto"]) != a["objeto"] or int(h.get("t0") or 0) < int(a["t0"]): continue
        h = dict(h, objeto=h.get("objeto") or a["objeto"]); golpe = cortada(h, golpes, canal, interrumpe)
        if h.get("corte") and not golpe: continue                                # marca de corte sin golpe en la canalizacion (o racion): no juzga, se espera al siguiente uso
        ef = h.get("efecto") or {}; viv = {"cuerpo": float(ef.get("cuerpo") or 0.0), "recursos": float(ef.get("recursos") or 0.0), "vinculo": float(ef.get("vinculo") or 0.0)}
        hp0 = float(h.get("hp0") if h.get("hp0") is not None else a["hp0"])
        if golpe:                                                                 # (a) golpe en la canalizacion: fallo en el cuerpo, en el momento
            ac = {"cuerpo": 0 if p["cuerpo"] > 0 else acierto_dim(p["cuerpo"], viv["cuerpo"]), "recursos": acierto_dim(p["recursos"], viv["recursos"]), "vinculo": acierto_dim(p["vinculo"], viv["vinculo"])}
            n = int(canal.get(h["objeto"]) or 0); g1 = min(g for g in golpes if int(h["t0"]) <= g <= int(h["t0"]) + n)
            return viv, ac, "cortada por golpe", {"hp0": hp0, "golpe_en_canal": g1 - int(h["t0"]), "canal": n, "marca_corte": bool(h.get("corte")), "hueco": None}
        c, obj = juzga_cuerpo(p["cuerpo"], viv["cuerpo"], hp0)
        return viv, {"cuerpo": c, "recursos": acierto_dim(p["recursos"], viv["recursos"]), "vinculo": acierto_dim(p["vinculo"], viv["vinculo"])}, "huella (hueco)", {"hp0": hp0, "hueco": obj}
    if tick - a["t0"] >= 2 * IN.VENT:
        viv = {"cuerpo": hp - a["hp0"], "recursos": (float(W) - float(a["W0"])) if (W is not None and a["W0"] is not None) else 0.0, "vinculo": (float(B) - float(a["B0"])) if (B is not None and a["B0"] is not None) else 0.0}
        c, obj = juzga_cuerpo(p["cuerpo"], viv["cuerpo"], a["hp0"])
        return viv, {"cuerpo": c, "recursos": acierto_dim(p["recursos"], viv["recursos"]), "vinculo": acierto_dim(p["vinculo"], viv["vinculo"])}, "sin huella (480 tics)", {"hp0": a["hp0"], "hueco": obj}
    return None


def sombra(a):
    """[P7-63, 14-oct] lo que queda en la lista de invita_P7_54 mientras esta pieza juzga una cura: la misma invitacion (para que invita_P7_54 no la vuelva a aceptar mientras sigue
    abierta, como antes), con un objeto que no existe y un t0 en el futuro (para que invita_P7_54 nunca la juzgue)."""
    return {"inv": a["inv"], "t0": 10 ** 9, "hp0": a.get("hp0"), "W0": None, "B0": None, "objeto": "__juicio_P7_62__", "n_huellas0": 0, "_sombra": True}


def mueve():
    """las curas recien aceptadas pasan de la lista de invita_P7_54 a la de esta pieza; en su sitio queda su sombra hasta que esta pieza las juzga"""
    for a in [a for a in IN.E["abiertas"] if a["inv"]["accion"] in CURAS and not a.get("_sombra")]:
        IN.E["abiertas"].remove(a); IN.E["abiertas"].append(sombra(a)); E["abiertas"].append(a)


def evalua(tick, hp, W, B, registra):
    queda = []
    for a in E["abiertas"]:
        r = juicio(a, X.ESTADO.get("huellas") or [], tick, hp, W, B, E["golpes"])
        if r is None: queda.append(a); continue
        IN.E["abiertas"] = [x for x in IN.E["abiertas"] if not (x.get("_sombra") and x["inv"]["_k"] == a["inv"]["_k"])]      # [P7-63] juzgada: fuera su sombra
        viv, ac, fuente, extra = r; antes = dict(IN.E["conf"])
        for dim in ("cuerpo", "recursos", "vinculo"): IN.E["conf"][dim] = (1 - IN.ETA) * IN.E["conf"][dim] + IN.ETA * ac[dim]
        IN.E["n"]["evaluadas"] += 1; E["n"]["evaluadas"] += 1; E["n"][{"cortada por golpe": "cortadas", "huella (hueco)": "hueco", "sin huella (480 tics)": "sin_huella"}[fuente]] += 1
        if registra: registra({"k": "P7_62_evaluada", "tick": tick, "n": a["inv"]["_k"], "accion": a["inv"]["accion"], "falsa": bool(a["inv"].get("falsa")), "fuente": fuente, "prometido": {d_: a["inv"].get(d_) for d_ in ("cuerpo", "recursos", "vinculo")},
                               "vivido": {k: round(v, 3) for k, v in viv.items()}, "acierto": ac, **extra, "t_aceptada": a["t0"], "confianza_antes": antes, "confianza_despues": dict(IN.E["conf"])})
    E["abiertas"] = queda


# ── (c) el contraste con lo contado, solo en su situacion ──
def amenaza_de(r):
    if r.get("origen") == "visto": return None
    v = (r.get("contexto") or {}).get("amenaza"); return None if v is None else bool(v)


def contrasta(c, mundo, tick, registra):
    """= invita_P7_57.contrasta + el filtro de situacion para las invitaciones con condicion de amenaza"""
    if c is None or mundo is None or not IN.E["inv"]: return
    for o_, s_, r in c.recuerdos():
        if r.get("origen") not in ("contado", "visto") or r.get("corte"): continue
        k = (o_, r.get("via"), r.get("dia_emisora", r.get("dia")), r.get("tick_emisora", r.get("tick")))
        if k in IC.E["vistos"]: continue
        IC.E["vistos"].add(k); e = float((r.get("efecto") or {}).get("cuerpo") or 0.0); w = IC.PESO_CONTADO * float(r.get("intensidad") or 0.0); eta = IC.ETA * min(1.0, w); am = amenaza_de(r)
        juicios = []; fuera = 0
        for inv in IN.E["inv"]:
            if IC.objeto_de(inv["accion"], mundo) != o_: continue
            p = float(inv.get("cuerpo") or 0.0)
            if abs(p) < 1e-9 or (r.get("al_menos") and p > e): continue
            cond = inv.get("amenaza", "CUALQUIERA")
            if cond != "CUALQUIERA" and (am is None or am != (cond == "AMENAZA")): fuera += 1; continue      # (c) otra situacion (o desconocida): no entra
            juicios.append((inv, p, 1 if (abs(e) < 1.0 and abs(p) < 1.0) or ((p > 0) == (e > 0) and abs(e) >= abs(p) / 2) else 0))
        E["n"]["fuera_de_situacion"] += fuera
        if not juicios: continue
        ac = sum(j[2] for j in juicios) / len(juicios)
        antes = IN.E["conf"]["cuerpo"]; IN.E["conf"]["cuerpo"] = antes + eta * (ac - antes); IC.E["n_contrastes"] += 1; E["n"]["contrastes"] += 1
        if registra: registra({"k": "P7_62_contraste", "tick": tick, "objeto": o_, "origen": r.get("origen"), "via": r.get("via"), "amenaza_recuerdo": am, "efecto_contado": round(e, 3), "peso": round(w, 3), "invitaciones": [j[0].get("_k") for j in juicios],
                               "acciones": [j[0]["accion"] for j in juicios], "falsa": any(j[0].get("falsa") for j in juicios), "promesas": [j[1] for j in juicios], "acierto": ac, "eta": round(eta, 4), "confianza_antes": round(antes, 4), "confianza_despues": round(IN.E["conf"]["cuerpo"], 4)})


# ── (c) la amenaza en el recuerdo y en el mensaje ──
def amenaza_noche(p, HE):
    """la amenaza de un recuerdo recibido de noche: la que la hermana apunto en su cuaderno (mismo objeto, dia y tic)"""
    if E["hermana_cache"] is None:
        E["hermana_cache"] = {}
        try:
            h = json.load(open(os.path.join(HE.E["cuaderno_dir"], f"cuaderno_P7_{HE.E['pareja']}.json")))
            for o, d in (h.get("objetos") or {}).items():
                for s_, L in (d.get("situaciones") or {}).items():
                    for q in L: E["hermana_cache"][(o, int(q.get("dia") or 0), int(q.get("tick") or 0))] = (q.get("contexto") or {}).get("amenaza")
        except Exception: pass
    return E["hermana_cache"].get((p["objeto"], int(p["dia_emisora"]), int(p["tick_emisora"])))


def _cod_parsea(HE):
    _cod, _par = HE.codifica, HE.parsea
    def codifica(r, slot):
        t = _cod(r, slot); ctx = r.get("contexto") or {}
        m = re.match(rf"^({HE.MARCA} P\d+ d\d+ t\d+ [brnc][df])([01])( .*)$", t)
        return (m.group(1) + str(int(m.group(2)) + (2 if ctx.get("amenaza") else 0)) + m.group(3)) if m else t
    def parsea(texto):
        if not isinstance(texto, str): return None
        m = re.match(rf"^({HE.MARCA} P\d+ d\d+ t\d+ [brnc][df])([0-3])( .*)$", texto)
        if not m: return _par(texto)
        g = int(m.group(2)); p = _par(m.group(1) + str(g % 2) + m.group(3))
        if p is not None: p["amenaza"] = g >= 2
        return p
    return codifica, parsea


def aplica(clase, registra=None):
    if not ON: return {"P7_62": False}
    assert IN.ON and IC.ON, "P7-62 va sobre invita_P7_54 e invita_P7_57"
    import hermanas_P7_48 as HE
    from recuerdo_P7_23 import CuadernoP23
    # (c) la amenaza en el contexto de lo vivido (al empezar el uso) y en el cuaderno
    _ca = N.contexto_ahora
    def contexto_ahora(mundo, pos, tick, _ca=_ca):
        d = _ca(mundo, pos, tick); d["amenaza"] = amenaza_ahora(tick); return d
    N.contexto_ahora = contexto_ahora
    _ap = CuadernoP23.apunta_P23
    def apunta_P23(self, objeto, contexto, foto, acciones, efecto, importancia, tick=None, al_menos=False, corte=False, _ap=_ap):
        r = _ap(self, objeto, contexto, foto, acciones, efecto, importancia, tick=tick, al_menos=al_menos, corte=corte)
        if isinstance(r, dict) and isinstance(contexto, dict) and "amenaza" in contexto: r.setdefault("contexto", {})["amenaza"] = bool(contexto["amenaza"])
        return r
    CuadernoP23.apunta_P23 = apunta_P23
    HE.codifica, HE.parsea = _cod_parsea(HE)
    _re = HE.recibe
    def recibe(c, p, via, B, tick, registra_, _re=_re):
        r = _re(c, p, via, B, tick, registra_)
        if not r: return r
        am = p.get("amenaza")
        if am is None and via == "noche": am = amenaza_noche(p, HE)              # la noche: del cuaderno de la hermana (el mismo recuerdo)
        if am is not None: r.setdefault("contexto", {})["amenaza"] = bool(am)
        return r
    HE.recibe = recibe
    IC.contrasta = contrasta
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        E["abiertas"] = []; E["golpes"] = []; E["hermana_cache"] = None; c = _oa(criatura, ruta, registra_)
        if registra_: registra_({"k": "P7_62_arranque", "slot": int(criatura), "curas": list(CURAS), "regla": "golpe en la canalizacion del botiquin (use_ticks del mundo) = cortada; la racion no se corta"})
        return c
    X.arranca = arranca
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        mundo = self.mundo; tick = getattr(self, "tick", 0); live = mundo is not None and getattr(self, "phase", None) == "live"
        if live:
            if not E["canal"]: E["canal"] = {i: int(getattr(it, "use_ticks", 0) or 0) for i, it in (getattr(mundo, "items", None) or {}).items()}; E["interrumpe"] = {X.kit(mundo)}
            if any(float(d.get("amount") or 0) > 0 for d in ((obs.get("you") or {}).get("damage_taken") or [])): E["golpes"].append(tick); E["golpes"] = E["golpes"][-400:]
            try: pel = N33.peligro_de(self, obs); E["rival_fuego"] = bool(pel.get("rival_a_4") or pel.get("fuego")); E["amenaza_tic"] = tick
            except Exception: E["rival_fuego"] = False
            mueve()                                                              # nunca las juzga invita_P7_54
        accion, radio = _d(self, obs)
        if live and radio is not None:
            mueve()
            you = obs.get("you") or {}; ah = (radio.get("ahora") or {}); evalua(tick, float(you.get("hp") or 0.0), ah.get("W"), ah.get("B"), registra)
        return accion, radio
    clase.decidir = decidir
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_62_cierre", "n": dict(E["n"]), "pendientes": len(E["abiertas"]), "confianza": dict(IN.E["conf"])})
        return _ot(registra_)
    X.termina = termina
    return {"P7_62": True, "curas": list(CURAS)}

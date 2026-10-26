"""[P7-63] LA SITUACION DE LA MENTIRA DE LA RACION (GEMV_P7_63=1), enganchada DESPUES de juicio_P7_62 (que no se toca) y antes de rapido_P7_43. El juicio de las curas es el de
P7-62 (regla del mundo de Ari; cura juzgada por el hueco: la falsa de la racion, +40 con vida < 60, necesita >= 20 y la racion da ~15). Esta pieza anade la situacion de la falsa:
  (1) SITUACION vida=HERIDA_60 / SANA_60 (vida < 60 / >= 60, ahora): se anade al chequeo de situacion de invita_P7_54 (envolviendo IN.situacion e IN.cumple por fuera, como P7-57).
  (2) LA VIDA AL EMPEZAR VIAJA CON EL RECUERDO: al vivir un uso se apunta `contexto.herida60` (vida < 60 al empezar), y viaja como la amenaza de P7-62: por el canal, en el mismo
      caracter del golpe del M7 (0-7 = golpe + 2 x amenaza + 4 x herida60, mismo largo; un M7 de P7-62 (0-3) o de antes (0/1) se lee con herida60 = False) y por la noche, del cuaderno
      de la hermana.
  (3) CONTRASTE DE LO CONTADO SOLO EN LA MISMA SITUACION: una invitacion con condicion vida=HERIDA_60 (la falsa) solo se contrasta con recuerdos de la hermana de usar esa cosa con
      vida < 60 (herida60 True); con vida >= 60 o sin apuntar, no entra; un «visto» (la vida es la de quien mira) tampoco (declarado). Las condiciones de amenaza siguen como en P7-62.
Registros: P7_63_arranque, P7_63_contraste (como P7_62_contraste + herida60 del recuerdo), P7_63_cierre."""
import json, os, re
import descubre_P7 as X, nace_P7_23 as N, invita_P7_54 as IN, invita_P7_57 as IC, juicio_P7_62 as J62
ON = os.environ.get("GEMV_P7_63", "0") == "1"
VIDA = 60.0
E = {"hp": 100.0, "hp_tic": None, "hermana_cache": None, "n": {"contrastes": 0, "fuera_de_situacion": 0}}


def vida60(hp): return "HERIDA_60" if float(hp) < VIDA else "SANA_60"


def cumple_vida(inv, s):
    v = inv.get("vida", "CUALQUIERA")
    return v not in ("HERIDA_60", "SANA_60") or s.get("vida60") == v


def situacion_de(r):
    """(amenaza, herida60) de un recuerdo recibido; None si no se sabe (visto, o sin apuntar)"""
    if r.get("origen") == "visto": return None, None
    c = r.get("contexto") or {}; a = c.get("amenaza"); h = c.get("herida60")
    return (None if a is None else bool(a)), (None if h is None else bool(h))


def entra(inv, r):
    """¿se contrasta este recuerdo con esta invitacion? solo si sus condiciones de situacion (amenaza, vida 60) coinciden con las del recuerdo"""
    am, he = situacion_de(r)
    ca = inv.get("amenaza", "CUALQUIERA")
    if ca != "CUALQUIERA" and (am is None or am != (ca == "AMENAZA")): return False
    cv = inv.get("vida", "CUALQUIERA")
    if cv in ("HERIDA_60", "SANA_60") and (he is None or he != (cv == "HERIDA_60")): return False
    return True


def contrasta(c, mundo, tick, registra):
    """= juicio_P7_62.contrasta con el filtro de situacion generalizado (amenaza y vida 60)"""
    if c is None or mundo is None or not IN.E["inv"]: return
    for o_, s_, r in c.recuerdos():
        if r.get("origen") not in ("contado", "visto") or r.get("corte"): continue
        k = (o_, r.get("via"), r.get("dia_emisora", r.get("dia")), r.get("tick_emisora", r.get("tick")))
        if k in IC.E["vistos"]: continue
        IC.E["vistos"].add(k); e = float((r.get("efecto") or {}).get("cuerpo") or 0.0); w = IC.PESO_CONTADO * float(r.get("intensidad") or 0.0); eta = IC.ETA * min(1.0, w); am, he = situacion_de(r)
        juicios = []; fuera = 0
        for inv in IN.E["inv"]:
            if IC.objeto_de(inv["accion"], mundo) != o_: continue
            p = float(inv.get("cuerpo") or 0.0)
            if abs(p) < 1e-9 or (r.get("al_menos") and p > e): continue
            if not entra(inv, r): fuera += 1; continue
            juicios.append((inv, p, 1 if (abs(e) < 1.0 and abs(p) < 1.0) or ((p > 0) == (e > 0) and abs(e) >= abs(p) / 2) else 0))
        E["n"]["fuera_de_situacion"] += fuera
        if not juicios: continue
        ac = sum(j[2] for j in juicios) / len(juicios)
        antes = IN.E["conf"]["cuerpo"]; IN.E["conf"]["cuerpo"] = antes + eta * (ac - antes); IC.E["n_contrastes"] += 1; E["n"]["contrastes"] += 1
        if registra: registra({"k": "P7_63_contraste", "tick": tick, "objeto": o_, "origen": r.get("origen"), "via": r.get("via"), "amenaza_recuerdo": am, "herida60_recuerdo": he, "efecto_contado": round(e, 3), "peso": round(w, 3),
                               "invitaciones": [j[0].get("_k") for j in juicios], "acciones": [j[0]["accion"] for j in juicios], "falsa": any(j[0].get("falsa") for j in juicios), "promesas": [j[1] for j in juicios], "acierto": ac,
                               "eta": round(eta, 4), "confianza_antes": round(antes, 4), "confianza_despues": round(IN.E["conf"]["cuerpo"], 4)})


def herida_noche(p, HE):
    """la herida60 de un recuerdo recibido de noche: la que la hermana apunto en su cuaderno (mismo objeto, dia y tic)"""
    if E["hermana_cache"] is None:
        E["hermana_cache"] = {}
        try:
            h = json.load(open(os.path.join(HE.E["cuaderno_dir"], f"cuaderno_P7_{HE.E['pareja']}.json")))
            for o, d in (h.get("objetos") or {}).items():
                for s_, L in (d.get("situaciones") or {}).items():
                    for q in L: E["hermana_cache"][(o, int(q.get("dia") or 0), int(q.get("tick") or 0))] = (q.get("contexto") or {}).get("herida60")
        except Exception: pass
    return E["hermana_cache"].get((p["objeto"], int(p["dia_emisora"]), int(p["tick_emisora"])))


def _cod_parsea(HE, cod62, par62):
    def codifica(r, slot):
        t = cod62(r, slot); ctx = r.get("contexto") or {}
        m = re.match(rf"^({HE.MARCA} P\d+ d\d+ t\d+ [brnc][df])([0-3])( .*)$", t)
        return (m.group(1) + str(int(m.group(2)) + (4 if ctx.get("herida60") else 0)) + m.group(3)) if m else t
    def parsea(texto):
        if not isinstance(texto, str): return None
        m = re.match(rf"^({HE.MARCA} P\d+ d\d+ t\d+ [brnc][df])([0-7])( .*)$", texto)
        if not m: return par62(texto)
        g = int(m.group(2)); p = par62(m.group(1) + str(g % 4) + m.group(3))
        if p is not None: p["herida60"] = g >= 4
        return p
    return codifica, parsea


def aplica(clase, registra=None):
    if not ON: return {"P7_63": False}
    assert J62.ON and IN.ON and IC.ON, "P7-63 va sobre juicio_P7_62 (y P7-54, P7-57)"
    import hermanas_P7_48 as HE
    from recuerdo_P7_23 import CuadernoP23
    # (1) la situacion vida 60
    _os, _oc = IN.situacion, IN.cumple
    def situacion(self, obs, mundo, tick):
        s = _os(self, obs, mundo, tick); s["vida60"] = vida60((obs.get("you") or {}).get("hp") or 0.0); return s
    def cumple(inv, s): return cumple_vida(inv, s) and _oc(dict(inv, vida="CUALQUIERA") if inv.get("vida") in ("HERIDA_60", "SANA_60") else inv, s)
    IN.situacion, IN.cumple = situacion, cumple
    # (2) la vida al empezar en el recuerdo, en el cuaderno, en el canal y en la noche
    _ca = N.contexto_ahora
    def contexto_ahora(mundo, pos, tick, _ca=_ca):
        d = _ca(mundo, pos, tick); d["herida60"] = bool(E["hp_tic"] == tick and E["hp"] < VIDA); return d
    N.contexto_ahora = contexto_ahora
    _ap = CuadernoP23.apunta_P23
    def apunta_P23(self, objeto, contexto, foto, acciones, efecto, importancia, tick=None, al_menos=False, corte=False, _ap=_ap):
        r = _ap(self, objeto, contexto, foto, acciones, efecto, importancia, tick=tick, al_menos=al_menos, corte=corte)
        if isinstance(r, dict) and isinstance(contexto, dict) and "herida60" in contexto: r.setdefault("contexto", {})["herida60"] = bool(contexto["herida60"])
        return r
    CuadernoP23.apunta_P23 = apunta_P23
    HE.codifica, HE.parsea = _cod_parsea(HE, HE.codifica, HE.parsea)
    _re = HE.recibe
    def recibe(c, p, via, B, tick, registra_, _re=_re):
        r = _re(c, p, via, B, tick, registra_)
        if not r: return r
        he = p.get("herida60")
        if he is None and via == "noche": he = herida_noche(p, HE)
        if he is not None: r.setdefault("contexto", {})["herida60"] = bool(he)
        return r
    HE.recibe = recibe
    # (3) el contraste
    IC.contrasta = contrasta
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        E["hermana_cache"] = None; c = _oa(criatura, ruta, registra_)
        if registra_: registra_({"k": "P7_63_arranque", "slot": int(criatura), "vida": VIDA, "falsas": sum(1 for i in IN.E["inv"] if i.get("falsa")), "con_vida60": sum(1 for i in IN.E["inv"] if i.get("vida") in ("HERIDA_60", "SANA_60"))})
        return c
    X.arranca = arranca
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        if self.mundo is not None and getattr(self, "phase", None) == "live": E["hp"] = float((obs.get("you") or {}).get("hp") or 0.0); E["hp_tic"] = getattr(self, "tick", 0)
        return _d(self, obs)
    clase.decidir = decidir
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_63_cierre", "n": dict(E["n"]), "confianza": dict(IN.E["conf"])})
        return _ot(registra_)
    X.termina = termina
    return {"P7_63": True, "vida": VIDA}

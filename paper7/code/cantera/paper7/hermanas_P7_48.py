"""[P7-48] LAS HERMANAS QUE SE CUENTAN LO APRENDIDO (capitulo 4; diseno de Manel, 12-oct-2026; construccion, sin sello). GEMV_P7_48 = comparte | solas.
Sobre P7-40 + la intensidad en su escala (escala_P7_48), ojos compartidos encendidos (GEMV_OJOS=1) en los DOS brazos; la unica diferencia entre brazos es compartir.
  PAREJA: una valiente (asiento par de la pareja) y una prudente (impar); caracter como en P7-42: solo en la cautela del probar (filo_P7_40.MIEDO; model.py no expone el miedo).
  Cada recuerdo lleva `origen`: vivido / visto / contado (y `via`: canal | noche; `de`: asiento; `B`: vinculo al recibirlo). PESO de un recuerdo recibido = intensidad
  (en su escala) x B (mem.roce_B, 0-1): nunca mas que el vivido.
  (a) MIRANDO: la hermana usa el botiquin (su parte E2 muestra un botiquin menos) o se pone el camuflaje (`body` a la vista): ventana = el parte anterior y los 4 partes
      siguientes (~100 tics); efecto cuerpo = hp maximo de la ventana - hp del parte anterior; se DESCARTA si en la ventana algun parte trae agresor (a != 0) o el hp baja
      entre partes (dano), si la hermana calla (sin parte en 96 tics), si el botiquin acabo en nuestro zurron (regalo) o si su vida estaba llena (soltar o dar, no usar). Situacion y foto emocional: las propias de la
      que mira; importancia = |delta malestar propio| en la ventana; acciones = lo que hacia la hermana (mano, cuerpo, channeling, distancia).
  (b) CANAL (de dia, al verse): cada recuerdo vivido nuevo se manda por `team` en un hueco del parte E2 (formato fijo M7, <= 120 ASCII, parser estricto; un M7 por cada E2:
      nunca dos seguidos, el parte no se pierde mas de 25 tics). (c) NOCHE (al arrancar): como mucho los 5 recuerdos vividos MAS INTENSOS de ayer de la hermana que no
      llegaron de dia, leidos de su cuaderno (misma carpeta), con el B del cierre de ayer (`B_cierre_P7_48` del cuaderno propio).
Registros: P7_48_arranque, P7_48_mensaje (enviado), P7_48_contado (recibido: canal | noche, con B y peso), P7_48_visto (apuntado | descartado), P7_48_mensaje_malo, P7_48_cierre."""
import json, os, re
import descubre_P7 as X, nace_P7_23 as N, nace_P7_33 as N33, recuerdo_P7_23 as RP, filo_P7_40 as FI, escala_P7_48 as ES
from cuaderno_P7 import DOMINIOS
MODO = os.environ.get("GEMV_P7_48", ""); ON = MODO in ("comparte", "solas"); COMPARTE = MODO == "comparte"
PAREJA_CAUTELA = os.environ.get("GEMV_P7_48_MIEDO_PAREJA", "1") == "1"
FUSION = os.environ.get("GEMV_P7_48_FUSION", "0") == "1"      # [P7-56] un uso = un recuerdo: el visto y el contado del mismo uso (misma hermana, mismo objeto, mismo dia de origen, |tic| <= 240) se funden en uno      # [P7-49a] con el mando de miedo (GEMV_P7_48_MIEDO_PAREJA=0) el caracter lo pone el mando, no la paridad de la cautela
VENTANA_PARTES = 4; CADUCIDAD = 96; NOCHE_MAX = 5; MARCA = "M7"
OBJ = {"first_aid": "b", "rations": "r", "net": "n", "camouflage": "c"}; OBJ_INV = {v: k for k, v in OBJ.items()}
ACC = {"noop": "N", "ir_objeto": "O", "coger": "C", "usar_botiquin": "B", "usar_racion": "R", "ir_curioso": "Q", "ir_azar": "Z", "ir_pareja": "P", "ir_centro": "T", "ir_botin": "L", "empunar": "E", "ponerse": "W", "dar": "D", "huir": "F"}
ACC_INV = {v: k for k, v in ACC.items()}
E = {"slot": None, "pareja": None, "registra": None, "dia": None, "B": 1.0, "pendientes": [], "enviados": set(), "recibidos": set(), "ultimo_fue_parte": True, "pareja_vista": False, "partes": [], "vigilias": [], "ult_body": None,
     "n": {"vivido": 0, "visto": 0, "visto_descartado": 0, "canal": 0, "noche": 0, "mensajes": 0, "malos": 0}, "descartes": {}, "obs": None, "mundo": None, "cuaderno_dir": None}


# ── el mensaje M7 ──
def _g(x, nd=4): return f"{round(float(x), nd):g}"
def cod_accion(a):
    a = str(a)
    if a in ACC: return ACC[a]
    if a.startswith("atacar"): return "A"
    if a.startswith(("move", "paso")): return "M"
    if a.startswith("hacer_sitio"): return "H"
    return "?"
def codifica(r, slot):
    acc = "".join(cod_accion(a) for a in (r.get("acciones") or [])[-4:]) or "?"
    f = r.get("foto") or {}; e = r["efecto"]; i = r["importancia"]; ctx = r.get("contexto") or {}
    return (f"{MARCA} P{slot} d{int(r['dia'])} t{int(r.get('tick') or 0)} {OBJ.get(r['_objeto'], '?')}{'d' if r['_sit'] == 'dentro' else 'f'}{'1' if ctx.get('golpeado_48') else '0'} "
            f"e{_g(e['cuerpo'])},{_g(e['recursos'])},{_g(e['vinculo'])} i{_g(i['cuerpo'])},{_g(i['recursos'])},{_g(i['vinculo'])} "
            f"f{_g(f.get('dolor_F', 0), 2)},{_g(f.get('dolor_R', 0), 2)},{_g(f.get('dolor_S', 0), 2)},{_g(f.get('positivo', 0), 2)},{_g(f.get('d', 0), 2)} a{acc} n{_g(r['intensidad'], 3)} m{'1' if r.get('al_menos') else '0'}")
_NUM = r"(-?\d+(?:\.\d+)?(?:e-?\d+)?)"
_RE = re.compile(rf"^{MARCA} P(\d+) d(\d+) t(\d+) ([brnc])([df])([01]) e{_NUM},{_NUM},{_NUM} i{_NUM},{_NUM},{_NUM} f{_NUM},{_NUM},{_NUM},{_NUM},{_NUM} a([A-Z?]{{1,4}}) n{_NUM} m([01])$")
def parsea(texto):
    if not isinstance(texto, str) or len(texto) > 120: return None
    m = _RE.match(texto)
    if not m: return None
    g = m.groups(); F = lambda k: float(g[k])
    return {"de": int(g[0]), "dia_emisora": int(g[1]), "tick_emisora": int(g[2]), "objeto": OBJ_INV[g[3]], "situacion": ("dentro" if g[4] == "d" else "fuera"), "golpeado_48": g[5] == "1",
            "efecto": {"cuerpo": F(6), "recursos": F(7), "vinculo": F(8)}, "importancia": {"cuerpo": F(9), "recursos": F(10), "vinculo": F(11)}, "foto": {"dolor_F": F(12), "dolor_R": F(13), "dolor_S": F(14), "positivo": F(15), "d": F(16)},
            "acciones": [ACC_INV.get(ch, ch) for ch in g[17]], "intensidad_emisora": F(18), "al_menos": g[19] == "1"}


# ── recibir: el recuerdo entra en el cuaderno con peso intensidad x B ──
def recibe(c, p, via, B, tick, registra):
    clave = (p["de"], p["dia_emisora"], p["tick_emisora"])
    if clave in E["recibidos"]: return None
    E["recibidos"].add(clave); w = round(float(p["intensidad_emisora"]) * float(B), 4)
    r = {"dia": c.dia_actual(), "tick": tick, "efecto": {d: round(float(p["efecto"].get(d) or 0.0), 4) for d in DOMINIOS}, "importancia": {d: round(float(p["importancia"].get(d) or 0.0), 4) for d in DOMINIOS},
         "intensidad": w, "creencia_antes": None, "al_menos": bool(p.get("al_menos")), "contexto": {"dentro": p["situacion"] == "dentro", "golpeado_48": bool(p.get("golpeado_48"))}, "foto": p.get("foto"), "acciones": list(p.get("acciones") or []),
         "corte": False, "origen": "contado", "via": via, "de": p["de"], "B": round(float(B), 4), "intensidad_emisora": float(p["intensidad_emisora"]), "dia_emisora": p["dia_emisora"], "tick_emisora": p["tick_emisora"]}
    if FUSION:
        for s_, L in c._obj(p["objeto"])["situaciones"].items():
            for q in list(L):
                if q.get("origen") == "visto" and q.get("de") == p["de"] and int(q.get("dia") or -1) == int(p["dia_emisora"]) and abs(int(q.get("tick") or 0) - int(p["tick_emisora"])) <= 240:
                    L.remove(q); r["confirmado_visto"] = True; E["n"]["fusionados"] = E["n"].get("fusionados", 0) + 1
    c._obj(p["objeto"])["situaciones"].setdefault(p["situacion"], []).append(r); E["n"][via] += 1
    if registra: registra({"k": "P7_48_contado", "tick": tick, "via": via, "de": p["de"], "objeto": p["objeto"], "situacion": p["situacion"], "B": r["B"], "intensidad_emisora": r["intensidad_emisora"], "peso": w, "dia_emisora": p["dia_emisora"], "tick_emisora": p["tick_emisora"], "efecto": r["efecto"]})
    return r


def parte_de(texto):
    """hp, botiquines, agresor del parte E1/E2 de la hermana (cabecera comun)."""
    m = re.match(r"^E[12] P(\d+) t(\d+) (\d+),(\d+) h(\d+(?:\.\d+)?) v([01]) b(\d+) a([01])", texto or "")
    return None if not m else {"slot": int(m.group(1)), "t": int(m.group(2)), "hp": float(m.group(5)), "b": int(m.group(7)), "a": m.group(8) == "1"}


def aplica(clase, registra=None):
    if not ON: return {"P7_48": False}
    assert os.environ.get("GEMV_P7_40") == "1" and ES.ON, "P7-48 va sobre P7-40 + escala_P7_48"
    assert (os.environ.get("GEMV_OJOS", "1") or "1") not in ("0", "", "no"), "P7-48: los ojos compartidos van encendidos en los dos brazos"
    E["registra"] = registra
    # la pareja: valiente (par) / prudente (impar), y la noche
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        E["slot"] = int(criatura); E["pareja"] = int(criatura) ^ 1
        if PAREJA_CAUTELA: FI.MIEDO = "valiente" if int(criatura) % 2 == 0 else "prudente"
        c = _oa(criatura, ruta, registra_); E["cuaderno_dir"] = os.path.dirname(os.path.abspath(ruta)) if ruta else None
        if c is not None:
            for o_, s_, r in c.recuerdos():
                r.setdefault("origen", "vivido")
                if r.get("origen") == "contado" and r.get("via") == "canal": E["recibidos"].add((r.get("de"), r.get("dia_emisora"), r.get("tick_emisora")))
            B_cierre = None
            try: B_cierre = (json.load(open(ruta)).get("B_cierre_P7_48") if ruta and os.path.exists(ruta) else None)
            except Exception: B_cierre = None
            noche = []
            if COMPARTE and E["cuaderno_dir"] and X.CUADERNO_ON and not X.BORRADO and B_cierre is not None:
                f = os.path.join(E["cuaderno_dir"], f"cuaderno_P7_{E['pareja']}.json")
                if os.path.exists(f):
                    try: h = json.load(open(f))
                    except Exception: h = {}
                    ayer = int(h.get("dia") or 0); cand = []
                    for o, d in (h.get("objetos") or {}).items():
                        for s_, L in (d.get("situaciones") or {}).items():
                            for r in L:
                                if r.get("corte") or r.get("origen", "vivido") != "vivido" or int(r.get("dia") or 0) != ayer: continue
                                if (E["pareja"], int(r["dia"]), int(r.get("tick") or 0)) in E["recibidos"]: continue
                                cand.append({"de": E["pareja"], "dia_emisora": int(r["dia"]), "tick_emisora": int(r.get("tick") or 0), "objeto": o, "situacion": s_, "golpeado_48": (r.get("contexto") or {}).get("golpeado_48"), "efecto": r["efecto"], "importancia": r["importancia"], "foto": r.get("foto"), "acciones": r.get("acciones"), "intensidad_emisora": float(r["intensidad"]), "al_menos": r.get("al_menos")})
                    for p in sorted(cand, key=lambda p: -p["intensidad_emisora"])[:NOCHE_MAX]:
                        if recibe(c, p, "noche", B_cierre, 0, registra_): noche.append((p["objeto"], p["intensidad_emisora"]))
            _v0 = c.volcado
            def volcado(_v0=_v0):
                d = _v0(); d["B_cierre_P7_48"] = round(float(E["B"]), 4); d["P7_48"] = {"modo": MODO, "n": E["n"], "descartes": E["descartes"], "miedo": FI.MIEDO}; return d
            c.volcado = volcado
            if registra_: registra_({"k": "P7_48_arranque", "modo": MODO, "slot": E["slot"], "pareja": E["pareja"], "miedo": FI.MIEDO, "B_cierre_ayer": B_cierre, "noche": noche, "ya_recibidos": len(E["recibidos"])})
        return c
    X.arranca = arranca
    # el canal: un M7 en un hueco del parte E2 (envuelve parte2.emite, que policy_pareja llama por modulo)
    try:
        import parte2 as P2
        _oe = P2.emite
        def emite(*a, **k):
            if COMPARTE and E["pendientes"] and E["ultimo_fue_parte"] and E["pareja_vista"]:
                r = E["pendientes"].pop(0); txt = codifica(r, E["slot"])
                if len(txt) <= 120 and parsea(txt) is not None:
                    E["ultimo_fue_parte"] = False; E["n"]["mensajes"] += 1; E["enviados"].add((int(r["dia"]), int(r.get("tick") or 0)))
                    if registra: registra({"k": "P7_48_mensaje", "tick": N.E.get("tick"), "texto": txt, "largo": len(txt)})
                    return txt
                E["n"]["malos"] += 1
                if registra: registra({"k": "P7_48_mensaje_malo", "tick": N.E.get("tick"), "texto": txt[:120], "largo": len(txt)})
            E["ultimo_fue_parte"] = True
            return _oe(*a, **k)
        P2.emite = emite; E["canal"] = True
    except Exception as ex:
        E["canal"] = repr(ex)[:120]
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        n0 = len(X.ESTADO.get("huellas") or [])
        accion, radio = _d(self, obs)
        c = N.cuaderno(); mundo = self.mundo
        if c is None or radio is None or getattr(self, "phase", None) != "live" or mundo is None: return accion, radio
        tick = self.tick; you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); mem = getattr(self, "mem", None)
        E["B"] = float(getattr(mem, "roce_B", E["B"]) or 0.0); B = E["B"]
        tm = getattr(mundo, "teammate_slot", None)
        if tm is not None and tm >= 0 and tm != E["pareja"]:
            if registra and not E.get("aviso_pareja"): registra({"k": "P7_48_aviso", "tick": tick, "nota": "teammate_slot distinto de la paridad", "teammate": tm, "paridad": E["pareja"]}); E["aviso_pareja"] = True
            E["pareja"] = tm
        ag = [a for a in ((obs.get("visible") or {}).get("agents") or []) if a.get("slot") == E["pareja"]]; E["pareja_vista"] = bool(ag)
        # vividos nuevos -> marca y cola del canal
        for h in (X.ESTADO.get("huellas") or [])[n0:]:
            obj = h.get("objeto") or X.kit(mundo); rec = [r for r in c.recuerdos_de(obj) if r.get("tick") == h.get("t0")]
            if not rec: continue
            r = rec[-1]; r.setdefault("origen", "vivido"); E["n"]["vivido"] += 1
            if not h.get("corte") and COMPARTE:
                sit = next((s_ for s_, L in c._obj(obj)["situaciones"].items() if r in L), "dentro"); E["pendientes"].append(dict(r, _objeto=obj, _sit=sit))
        # el canal: recibir
        for m in (obs.get("chat") or []):
            if m.get("channel") != "team" or m.get("from") != E["pareja"]: continue
            txt = m.get("text") or ""
            if txt.startswith(MARCA + " "):
                if not COMPARTE: continue
                p = parsea(txt)
                if p is None:
                    E["n"]["malos"] += 1
                    if registra: registra({"k": "P7_48_mensaje_malo", "tick": tick, "texto": txt[:120], "lado": "recibe"})
                    continue
                recibe(c, p, "canal", B, tick, registra)
            else:
                pt = parte_de(txt)
                if pt: E["partes"].append(pt)
        # mirando
        if COMPARTE: mira(self, obs, radio, c, mundo, tick, pos, ag, B, registra)
        return accion, radio
    clase.decidir = decidir
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_48_cierre", "modo": MODO, "n": E["n"], "descartes": E["descartes"], "B_cierre": round(E["B"], 4), "pendientes_sin_mandar": len(E["pendientes"]), "canal": E.get("canal")})
        return _ot(registra_)
    X.termina = termina
    return {"P7_48": MODO, "comparte": COMPARTE, "pareja_por_paridad": True}


def mira(self, obs, radio, c, mundo, tick, pos, ag, B, registra):
    """(a) MIRANDO: abre una vigilia cuando el parte de la hermana muestra un botiquin menos o su cuerpo a la vista cambia a camuflaje; la cierra a los 4 partes."""
    P = E["partes"]; mal = X.malestar_ejes(radio); foto = RP.foto_de_radio(radio) or N.E.get("foto") or {}; kit = X.kit(mundo); camo = N33.camo(mundo)
    mis_kits = N.unidades_de(obs.get("you") or {}, mundo, kit)
    a = ag[0] if ag else None; body = (a.get("body") or {}).get("id") if isinstance(a and a.get("body"), dict) else (a.get("body") if a else None)
    hacia = ([f"mano:{a.get('hand')}", f"cuerpo:{body}", "channeling" if a.get("channeling") else "quieta", f"dist:{max(abs(a['pos'][0] - pos[0]), abs(a['pos'][1] - pos[1]))}"] if a and a.get("pos") else ["hermana:no_a_la_vista"])
    # detecciones
    if len(P) >= 2 and P[-1]["t"] != E.get("ult_parte_visto") and P[-1]["b"] < P[-2]["b"]:
        E["ult_parte_visto"] = P[-1]["t"]; E["vigilias"].append({"objeto": kit, "t0": tick, "p0": P[-2], "i0": len(P) - 1, "mal0": mal, "foto": foto, "hacia": hacia, "kits0": mis_kits, "ctx": N.contexto_ahora(mundo, pos, tick)})
    if a is not None:
        if body == camo and E["ult_body"] not in (camo, None) or (body == camo and E["ult_body"] is None and tick > 0 and E.get("ult_body_visto") is not None):
            if P and not any(v["objeto"] == camo and tick - v["t0"] < 240 for v in E["vigilias"]):
                E["vigilias"].append({"objeto": camo, "t0": tick, "p0": P[-1], "i0": len(P), "mal0": mal, "foto": foto, "hacia": hacia, "kits0": mis_kits, "ctx": N.contexto_ahora(mundo, pos, tick)})
        E["ult_body"] = body; E["ult_body_visto"] = tick
    # cierres
    queda = []
    for v in E["vigilias"]:
        partes = P[v["i0"]:]
        if len(partes) < VENTANA_PARTES and tick - v["t0"] < CADUCIDAD + 25 * VENTANA_PARTES: queda.append(v); continue
        motivo = None
        if len(partes) < VENTANA_PARTES: motivo = "la hermana calla"
        elif any(p["a"] for p in [v["p0"]] + partes[:VENTANA_PARTES]): motivo = "agresor en la ventana"
        elif any(q["hp"] < p["hp"] for p, q in zip([v["p0"]] + partes[:VENTANA_PARTES], partes[:VENTANA_PARTES])): motivo = "dano en la ventana"
        elif v["objeto"] == kit and mis_kits > v["kits0"]: motivo = "el botiquin acabo en mi zurron (regalo)"
        elif v["objeto"] == kit and v["p0"]["hp"] >= 100.0: motivo = "un botiquin menos con la vida llena (lo solto o lo dio; el cuerpo no usa a tope)"
        if motivo:
            E["n"]["visto_descartado"] += 1; E["descartes"][motivo] = E["descartes"].get(motivo, 0) + 1
            if registra: registra({"k": "P7_48_visto", "tick": tick, "estado": "descartado", "objeto": v["objeto"], "motivo": motivo, "t0": v["t0"]})
            continue
        w = partes[:VENTANA_PARTES]; hp_max = max(p["hp"] for p in w); efecto = {"cuerpo": round(hp_max - v["p0"]["hp"], 4), "recursos": (-1.0 if v["objeto"] == kit else 0.0), "vinculo": 0.0}
        imp = {d: round(abs(mal.get(d, 0.0) - v["mal0"].get(d, 0.0)), 4) for d in DOMINIOS}; s = sum(imp.values()); inten, med, nv = ES.escala(c, s); peso = round(inten * B, 4)
        sit = "dentro" if v["ctx"].get("dentro") else "fuera"
        if FUSION:
            ya = next((q for s_, L in c._obj(v["objeto"])["situaciones"].items() for q in L if q.get("origen") == "contado" and q.get("de") == E["pareja"] and int(q.get("dia_emisora") or -1) == c.dia_actual() and abs(int(q.get("tick_emisora") or 0) - int(v["t0"])) <= 240), None)
            if ya is not None:
                ya["confirmado_visto"] = True; E["n"]["fusionados"] = E["n"].get("fusionados", 0) + 1
                if registra: registra({"k": "P7_48_visto", "tick": tick, "estado": "fusionado con el contado", "objeto": v["objeto"], "t0": v["t0"]})
                continue
        r = {"dia": c.dia_actual(), "tick": v["t0"], "efecto": efecto, "importancia": imp, "intensidad": peso, "creencia_antes": None, "al_menos": hp_max >= 100.0, "contexto": {"dentro": bool(v["ctx"].get("dentro")), "golpeado_48": bool(v["ctx"].get("golpeado_48"))},
             "foto": v["foto"], "acciones": v["hacia"], "corte": False, "origen": "visto", "de": E["pareja"], "B": round(B, 4), "intensidad_sin_B": round(inten, 4), "hp_hermana_antes": v["p0"]["hp"], "hp_hermana_max": hp_max}
        c._obj(v["objeto"])["situaciones"].setdefault(sit, []).append(r); E["n"]["visto"] += 1
        if registra: registra({"k": "P7_48_visto", "tick": tick, "estado": "apuntado", "objeto": v["objeto"], "situacion": sit, "efecto": efecto, "importancia": imp, "intensidad_sin_B": round(inten, 4), "B": round(B, 4), "peso": peso, "hacia": v["hacia"], "t0": v["t0"]})
    E["vigilias"] = queda

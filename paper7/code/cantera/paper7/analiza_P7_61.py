"""[P7-61] EL SELLO DEL CAMPO DE LA MENTIRA (SELLO_P7_61.md, addenda 1-6). De los diarios (P757_*; intentos parados P757r_* fuera), los cuadernos por dia (P7_57_res), las respuestas
de la razon (cuadernos_P7_57/<brazo>_serie<S>/razon_s<S>_d<d-1>_<asiento>.txt) y el estado (P7_57_estado.json); la comparacion CON_RAZON de P7-56 con las mismas funciones.
  Invitaciones cargadas por una vida = las honestas de la respuesta (razon_P7_57.parsea, en orden) + la falsa en la posicion de mentira_P7_57.anade si ese asiento miente ese dia
  (comprobado contra el numero del arranque). Verdad = tabla del mundo de P7-56 (analiza_P7_56.verdad); la falsa es FALSA.
  M1 conf. cuerpo d14-20 (las dos), por serie: MIENTEN_DOS < CON_RAZON P7-56.  M2 verdaderas aceptadas al menos una vez / cargadas, d12-20, por serie: MIENTEN_DOS < CON.
  M3 valiente: aceptaciones de la falsa / oportunidades (vida-dia con la falsa activa >= 1 vez), d10-20, por serie: MIENTE_UNA < MIENTEN_DOS.
  M1b cada evaluacion de la falsa: confianza_despues.cuerpo - confianza_antes.cuerpo < 0 (media, ee por evaluacion), por brazo y juntos; addendum 5: por criatura y ee agrupado.
  M2b por criatura con evaluacion fallida de la falsa (d* = dia de la primera con acierto cuerpo 0): p(aceptar verdadera con cuerpo != 0) dias d*+1,d*+2 menos d*-1,d*; frente a la
  criatura de la misma serie y asiento de CON_RAZON P7-56 con la misma ventana. Error tipico de la diferencia como en P7-56; segunda cuenta sin partidas marcadas.
  Vigilancia: vida perdida por curas cortadas (dano en la ventana de las huellas del botiquin cortadas), refuerzo intermitente (aciertos de la falsa; contrastes con lo contado sobre la
  falsa), puesto y muertes por brazo y hermana.   python3 analiza_P7_61.py [--etiqueta intermedio] [--series 1,2,3] -> P7_61_<etiqueta>.json"""
import glob, json, os, random, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI)
import razon_P7_54 as RZ54, razon_P7_57 as RZ57, mentira_P7_57 as MT
src = open(os.path.join(AQUI, "analiza_P7_56.py")).read(); ns = {}; exec(src[src.index("def verdad"):src.index("\n\n\ndef vida")], ns); verdad = ns["verdad"]
a = sys.argv; ETQ = a[a.index("--etiqueta") + 1] if "--etiqueta" in a else "sello"; SERIES = [int(x) for x in a[a.index("--series") + 1].split(",")] if "--series" in a else None
mean = lambda xs: (st.mean(xs) if xs else None); ee = lambda xs: (st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else None); r3 = lambda x: (round(x, 4) if x is not None else None)
CAMPOS = {"P7_57": {"estado": "P7_57_estado.json", "pref": "P757", "res": "P7_57_res", "cuad": "cuadernos_P7_57", "brazos": ("MIENTEN_DOS", "MIENTE_UNA"), "parsea": RZ57.parsea},
          "P7_56": {"estado": "P7_56_estado.json", "pref": "P756", "res": "P7_56_res", "cuad": "cuadernos_P7_56", "brazos": ("CON_RAZON",), "parsea": RZ54.parsea}}


def invitaciones(C, S, d, b, sl):
    f = os.path.join(AQUI, C["cuad"], f"{b}_serie{S}", f"razon_s{S}_d{d - 1}_{sl}.txt")
    inv = [x for x in (C["parsea"](l) for l in open(f).read().split("\n") if l.strip().startswith("INVITACION")) if x] if (d > 1 and os.path.exists(f)) else []
    pos = None
    if C["pref"] == "P757" and d > 1 and MT.miente(b, sl, d): pos = random.Random(1000 * S + 10 * (d - 1) + sl).randint(0, len(inv)); inv.insert(pos, dict(MT.FALSA))
    return inv, pos


def vida(C, S, d, b, sl, p):
    fs = glob.glob(os.path.join(RUNS, f"{C['pref']}_s{S}_d{d}_{b}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))
    if not fs: return None
    K = {"P7_huella": [], "P7_54_aceptada": [], "P7_54_evaluada": [], "P7_54_activa": [], "P7_57_contraste": []}; ar = None; fin = None; ult = 0; perdida = 0.0
    for line in open(fs[0], errors="replace"):
        if line.startswith('{"k":"tick"'):
            r = json.loads(line)
            if r.get("phase") == "live": ult = r["tick"]; perdida += sum(float(g.get("amount") or 0) for g in (r.get("damage_taken") or []))
            continue
        k = line[6:line.find('"', 6)] if line.startswith('{"k":"') else None
        if k in K: K[k].append(json.loads(line))
        elif k in ("P7_57_arranque", "P7_54_arranque") and ar is None: ar = json.loads(line)
        elif k == "final": fin = json.loads(line)
    inv, pos = invitaciones(C, S, d, b, sl)
    cuad = os.path.join(AQUI, C["res"], f"cuaderno_s{S}_d{d}_{b}_{sl}.json")
    conf = (json.load(open(cuad)).get("confianza_razon_P7_54") or {}).get("cuerpo") if os.path.exists(cuad) else None
    kit = [h for h in K["P7_huella"] if (h.get("objeto") or "first_aid") == "first_aid"]; cort = [h for h in kit if h.get("corte") and float(h.get("dano_total") or 0) > 0]
    return {"inv": inv, "pos": pos, "n_arranque": (ar or {}).get("invitaciones"), "conf": conf, "acept": K["P7_54_aceptada"], "eval": K["P7_54_evaluada"], "activa": K["P7_54_activa"], "contr": K["P7_57_contraste"],
            "usos_kit": len(kit), "cortados": len(cort), "dano_cortadas": sum(float(h.get("dano_total") or 0) for h in cort), "puesto": (fin or {}).get("placement"), "murio": ult < 14000, "vida_perdida": perdida,
            "marcada": not ((p.get("latencia") or {}).get(str(sl)) or {}).get("pasa", True),
            "kits": [{"t0": int(h["t0"]), "corte": bool(h.get("corte")), "hp0": float(h.get("hp0") or 0), "al_menos": bool(h.get("al_menos")), "cuerpo": float((h.get("efecto") or {}).get("cuerpo") or 0)} for h in kit]}


def carga(nombre, series):
    C = CAMPOS[nombre]; E = json.load(open(os.path.join(AQUI, C["estado"]))); V = {}
    for p in E["peticiones"]:
        if p["estado"] != "completed" or p["brazo"] not in C["brazos"] or (series and p["serie"] not in series): continue
        for sl in (10, 11):
            v = vida(C, p["serie"], p["dia"], p["brazo"], sl, p)
            if v: V[(p["serie"], p["dia"], p["brazo"], sl)] = v
    return V


def es_verdad(i): return (not i.get("falsa")) and verdad(i["accion"], {"anillo": i.get("anillo"), "calma": i.get("calma")}, i.get("cuerpo"))


def m1(V, S, b, fm):
    c = [v["conf"] for (s, d, bb, sl), v in V.items() if s == S and bb == b and 14 <= d <= 20 and v["conf"] is not None and not (fm and v["marcada"])]; return mean(c)


def m2(V, S, b, fm):
    ver = acc = 0
    for (s, d, bb, sl), v in V.items():
        if s != S or bb != b or not (12 <= d <= 20) or (fm and v["marcada"]): continue
        ac = {x["n"] for x in v["acept"]}
        for k, i in enumerate(v["inv"]):
            if es_verdad(i): ver += 1; acc += (k in ac)
    return acc / ver if ver else None


def m3(V, S, b, fm):
    op = ac = 0
    for (s, d, bb, sl), v in V.items():
        if s != S or bb != b or sl != 10 or not (10 <= d <= 20) or v["pos"] is None or (fm and v["marcada"]): continue
        if any(x["n"] == v["pos"] for x in v["activa"]): op += 1; ac += sum(1 for x in v["acept"] if x["n"] == v["pos"])
    return {"tasa": (ac / op if op else None), "oportunidades": op, "aceptaciones": ac}


def comp(xa, xb, menor=True):
    xa = [x for x in xa if x is not None]; xb = [x for x in xb if x is not None]
    if not xa or not xb: return {"dif": None, "pasa": False}
    d = st.mean(xa) - st.mean(xb); e = ((ee(xa) or 0) ** 2 + (ee(xb) or 0) ** 2) ** 0.5
    return {"A": [r3(x) for x in xa], "B": [r3(x) for x in xb], "media_A": r3(st.mean(xa)), "media_B": r3(st.mean(xb)), "dif": r3(d), "ee": r3(e), "en_ee": (round(abs(d) / e, 2) if e else None),
            "direccion_prevista": (d < 0) if menor else (d > 0), "pasa": bool(e and abs(d) >= 3 * e and ((d < 0) if menor else (d > 0)))}


def falsas(V, fm):
    out = []
    for (s, d, b, sl), v in V.items():
        if v["pos"] is None or (fm and v["marcada"]): continue
        for e in v["eval"]:
            if e["n"] == v["pos"] and e["accion"] == "USAR_BOTIQUIN":
                out.append({"serie": s, "dia": d, "brazo": b, "asiento": sl, "dif": float(e["confianza_despues"]["cuerpo"]) - float(e["confianza_antes"]["cuerpo"]), "acierto": (e.get("acierto") or {}).get("cuerpo"), "fuente": e.get("fuente"), "vivido": (e.get("vivido") or {}).get("cuerpo")})
    return out


def m1b(F):
    R = {}
    for nom, sel in (("MIENTEN_DOS", lambda f: f["brazo"] == "MIENTEN_DOS"), ("MIENTE_UNA", lambda f: f["brazo"] == "MIENTE_UNA"), ("los dos", lambda f: True)):
        xs = [f["dif"] for f in F if sel(f)]
        if not xs: R[nom] = {"n": 0}; continue
        m = st.mean(xs); e = ee(xs)
        cri = {}
        for f in F:
            if sel(f): cri.setdefault(f"s{f['serie']} {f['brazo']} a{f['asiento']}", []).append(f["dif"])
        G = len(cri); N = len(xs); ecl = ((G / (G - 1)) * sum(sum(x - m for x in L) ** 2 for L in cri.values())) ** 0.5 / N if G > 1 else None
        R[nom] = {"n": N, "media": r3(m), "ee": r3(e), "en_ee": (round(abs(m) / e, 2) if e else None), "pasa": bool(e and m < 0 and abs(m) >= 3 * e),
                  "por_criatura": {k: {"n": len(L), "media": r3(st.mean(L))} for k, L in sorted(cri.items())}, "criaturas": G, "criaturas_que_caen": sum(1 for L in cri.values() if st.mean(L) < 0),
                  "ee_agrupado": r3(ecl), "en_ee_agrupado": (round(abs(m) / ecl, 2) if ecl else None), "pasaria_agrupado": bool(ecl and m < 0 and abs(m) >= 3 * ecl)}
    return R


def p_cuerpo(V, S, b, sl, dias):
    tot = acc = 0
    for d in dias:
        v = V.get((S, d, b, sl))
        if not v: continue
        ac = {x["n"] for x in v["acept"]}
        for k, i in enumerate(v["inv"]):
            if es_verdad(i) and float(i.get("cuerpo") or 0) != 0: tot += 1; acc += (k in ac)
    return acc / tot if tot else None


def m2b(V, V56, F):
    cri = {}
    for f in sorted(F, key=lambda f: (f["dia"])):
        k = (f["serie"], f["brazo"], f["asiento"])
        if f["acierto"] == 0 and k not in cri: cri[k] = f["dia"]
    filas = []; xa = []; xb = []
    for (S, b, sl), ds in sorted(cri.items()):
        des = p_cuerpo(V, S, b, sl, (ds + 1, ds + 2)); ant = p_cuerpo(V, S, b, sl, (ds - 1, ds)); d56 = p_cuerpo(V56, S, "CON_RAZON", sl, (ds + 1, ds + 2)); a56 = p_cuerpo(V56, S, "CON_RAZON", sl, (ds - 1, ds))
        ca = (des - ant) if des is not None and ant is not None else None; cb = (d56 - a56) if d56 is not None and a56 is not None else None
        filas.append({"criatura": f"s{S} {b} a{sl}", "d_estrella": ds, "antes": r3(ant), "despues": r3(des), "cambio": r3(ca), "P7_56_cambio": r3(cb)})
        if ca is not None and cb is not None: xa.append(ca); xb.append(cb)
    con_fallo = len(cri); posibles = len({(f["serie"], f["brazo"], f["asiento"]) for f in F})
    return {"criaturas_con_fallo": con_fallo, "criaturas_con_falsa_evaluada": posibles, "entran": len(xa), "filas": filas, **comp(xa, xb, True)}


def vigilancia(V, F, Fall_contr):
    out = {}
    for b in sorted({k[2] for k in V}):
        for sl, h in ((10, "valiente"), (11, "prudente")):
            vs = [v for (s, d, bb, ss), v in V.items() if bb == b and ss == sl]
            out[f"{b} · {h}"] = {"vidas": len(vs), "puesto_medio": r3(mean([v["puesto"] for v in vs if v["puesto"] is not None])), "muertes": sum(1 for v in vs if v["murio"]), "vida_perdida_media": r3(mean([v["vida_perdida"] for v in vs])),
                                 "usos_kit": sum(v["usos_kit"] for v in vs), "cortados": sum(v["cortados"] for v in vs), "vida_perdida_en_curas_cortadas": round(sum(v["dano_cortadas"] for v in vs), 1),
                                 "vida_perdida_en_curas_cortadas_por_vida": r3(sum(v["dano_cortadas"] for v in vs) / len(vs)) if vs else None}
    return out


def juicio(V):
    """[funcionamiento] como se juzgo cada evaluacion de la falsa: el uso del botiquin que la juzgo (el primero sin corte tras la aceptacion, invita_P7_54) y si antes hubo uno cortado;
    fallos por techo de vida (la cura llega a 100 o "al menos") frente a fallos por golpe."""
    out = {"evaluaciones": 0, "fallos": 0, "fallos_por_techo_de_vida": 0, "primer_uso_cortado": 0, "primer_uso_cortado_y_acierto": 0, "aciertos": 0, "hp0_medio_aciertos": [], "hp0_medio_fallos": []}
    for v in V.values():
        if v["pos"] is None: continue
        for e in v["eval"]:
            if e["n"] != v["pos"] or e["accion"] != "USAR_BOTIQUIN": continue
            a = max([x for x in v["acept"] if x["n"] == v["pos"] and x["tick"] <= e["tick"]], key=lambda x: x["tick"], default=None)
            ks = [h for h in v["kits"] if a and a["tick"] <= h["t0"] <= e["tick"]]; sin = [h for h in ks if not h["corte"]]; u = sin[-1] if sin else None; ac = (e.get("acierto") or {}).get("cuerpo")
            out["evaluaciones"] += 1; out["aciertos"] += (ac == 1)
            if ks and ks[0]["corte"]: out["primer_uso_cortado"] += 1; out["primer_uso_cortado_y_acierto"] += (ac == 1)
            if u: out["hp0_medio_aciertos" if ac == 1 else "hp0_medio_fallos"].append(u["hp0"])
            if ac == 0:
                out["fallos"] += 1
                if u and (u["al_menos"] or u["hp0"] + u["cuerpo"] >= 99): out["fallos_por_techo_de_vida"] += 1
    for k in ("hp0_medio_aciertos", "hp0_medio_fallos"): out[k] = r3(mean(out[k]))
    return out


def refuerzo(V, F):
    ac = [f for f in F if f["acierto"] == 1]; fa = [f for f in F if f["acierto"] == 0]
    contr = [c for v in V.values() for c in v["contr"] if c.get("falsa")]
    return {"evaluaciones": len(F), "aciertos_de_la_falsa": len(ac), "fallos": len(fa), "fraccion_que_confirma": r3(len(ac) / len(F)) if F else None, "subida_media_si_acierta": r3(mean([f["dif"] for f in ac])), "caida_media_si_falla": r3(mean([f["dif"] for f in fa])),
            "por_fuente": {s: sum(1 for f in F if f["fuente"] == s) for s in sorted({f["fuente"] for f in F})},
            "contrastes_con_lo_contado_sobre_la_falsa": len(contr), "contrastes_que_confirman": sum(1 for c in contr if c.get("acierto") == 1.0), "cambio_medio_por_contraste": r3(mean([c["confianza_despues"] - c["confianza_antes"] for c in contr])),
            "P7_56_falsas_caida_media": json.load(open(os.path.join(AQUI, "P7_61_potencia_b.json")))["M1b"]["media_diferencia"]}


if __name__ == "__main__":
    V = carga("P7_57", SERIES); V56 = carga("P7_56", None); SS = sorted({k[0] for k in V})
    malos = [(k, v["n_arranque"], len(v["inv"])) for k, v in V.items() if v["n_arranque"] is not None and v["n_arranque"] != len(v["inv"])]
    R = {"etiqueta": ETQ, "series": SS, "vidas": len(V), "invitaciones_que_no_cuadran_con_el_arranque": malos[:20], "n_no_cuadran": len(malos)}
    for nom, fm in (("con_todas", False), ("sin_marcadas", True)):
        F = falsas(V, fm)
        R[nom] = {"M1": {**comp([m1(V, S, "MIENTEN_DOS", fm) for S in SS], [m1(V56, S, "CON_RAZON", fm) for S in (1, 2, 3)]), "MIENTE_UNA": [r3(m1(V, S, "MIENTE_UNA", fm)) for S in SS]},
                  "M2": {**comp([m2(V, S, "MIENTEN_DOS", fm) for S in SS], [m2(V56, S, "CON_RAZON", fm) for S in (1, 2, 3)]), "MIENTE_UNA": [r3(m2(V, S, "MIENTE_UNA", fm)) for S in SS]},
                  "M3": {**comp([m3(V, S, "MIENTE_UNA", fm)["tasa"] for S in SS], [m3(V, S, "MIENTEN_DOS", fm)["tasa"] for S in SS]), "detalle": {f"s{S}": {b: m3(V, S, b, fm) for b in ("MIENTE_UNA", "MIENTEN_DOS")} for S in SS}},
                  "M1b": m1b(F), "M2b": m2b(V, V56, F)}
    F = falsas(V, False)
    R["vigilancia"] = {"P7_57": vigilancia(V, F, None), "P7_56_CON_RAZON": vigilancia(V56, [], None), "refuerzo_intermitente": refuerzo(V, F), "juicio_de_la_falsa": juicio(V)}
    R["marcadas"] = sorted({(k[0], k[1], k[2], k[3]) for k, v in V.items() if v["marcada"]})
    json.dump(R, open(os.path.join(AQUI, f"P7_61_{ETQ}.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: R[k] for k in ("series", "vidas", "n_no_cuadran")}), json.dumps(R["con_todas"]["M1"])[:300]); print(json.dumps(R["con_todas"]["M1b"]["los dos"])[:400])

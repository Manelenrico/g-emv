"""[P7-50] EL SELLO DEL CAPITULO 4 EN PLATAFORMA (SELLO_P7_49.md + addendum), de una vez al acabar: de los cuadernos por dia (P7_50_res/cuaderno_s<S>_d<D>_<brazo>_<slot>.json),
los diarios (paintball/runs/P750_s<S>_d<D>_<brazo>_<semilla>/, dos asientos) y el estado (P7_50_estado.json: latencia, guarda). -> P7_50_sello.json
  S1 la hermana que menos prueba por si misma (en SOLAS, por serie: menos huellas vividas en los 20 dias; mismo asiento en COMPARTE): area bajo la curva de la creencia del
     botiquin (dentro, cuerpo; None = 0), d1-20; COMPARTE - SOLAS > 0 y >= 3 ee.
  S2 parecido: media de |c10 - c11| en d11-20 x cuatro objetos; COMPARTE < SOLAS y >= 3 ee.  S3 fraccion de huellas vividas a red + camuflaje (las dos juntas): COMPARTE < SOLAS y >= 3 ee.
  Vigilancia: pruebas por vida de valiente (10) y prudente (11); recibidos por origen por vida; contagio (recibidos cuyo signo del efecto del cuerpo contradice el real); puesto medio
  por hermana (partidas con corte fuera); latencia y marcadas. Segunda cuenta sin partidas marcadas.  python3 analiza_P7_50.py"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RES = os.path.join(AQUI, "P7_50_res"); RUNS = os.path.join(RAIZ, "paintball", "runs")
E = json.load(open(os.path.join(AQUI, "P7_50_estado.json"))); BRAZOS = ("COMPARTE", "SOLAS"); OBJ = ("first_aid", "rations", "net", "camouflage"); NOM = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}
SERIES = sorted({p["serie"] for p in E["peticiones"]})
ee = lambda xs: (st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else None); mean = lambda xs: (st.mean(xs) if xs else None)


def cre(c, o):
    x = ((c.get("creencias") or {}).get(o) or {}).get("dentro"); return float(x["cuerpo"]) if isinstance(x, dict) and x.get("cuerpo") is not None else 0.0


def cuaderno(S, d, b, sl):
    f = os.path.join(RES, f"cuaderno_s{S}_d{d}_{b}_{sl}.json"); return json.load(open(f)) if os.path.exists(f) else None


def diario(S, d, b, sl):
    p = next((p for p in E["peticiones"] if p["serie"] == S and p["dia"] == d and p["brazo"] == b), None)
    if not p: return None
    fs = glob.glob(os.path.join(RUNS, f"P750_s{S}_d{d}_{b}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))
    if not fs: return None
    H = []; REC = []; VIS = []; fin = None; corte = False
    for line in open(fs[0], errors="replace"):
        if line.startswith('{"k":"P7_huella"'): H.append(json.loads(line))
        elif line.startswith('{"k":"P7_48_contado"'): REC.append(json.loads(line))
        elif line.startswith('{"k":"P7_48_visto"'):
            r = json.loads(line)
            if r.get("estado") == "apuntado": VIS.append(r)
        elif line.startswith('{"k":"final"'): fin = json.loads(line)
    corte = any(os.path.basename(x).startswith("PARCIAL_") for x in glob.glob(os.path.join(RUNS, f"P750_s{S}_d{d}_{b}_{p['semilla']}", "*")))
    signo_real = {"first_aid": 1, "rations": 1, "net": 0, "camouflage": 0}
    def contradice(o, ef):
        e = float((ef or {}).get("cuerpo") or 0.0); return (e > 1.0) if signo_real.get(o, 0) == 0 else (e <= 0.0)
    cont = sum(1 for r in REC if contradice(r.get("objeto"), r.get("efecto"))) + sum(1 for r in VIS if contradice(r.get("objeto"), r.get("efecto")))
    return {"huellas": len(H), "huellas_inutil": sum(1 for h in H if (h.get("objeto") or "first_aid") in ("net", "camouflage")), "huellas_corte": sum(1 for h in H if h.get("corte")),
            "contado_canal": sum(1 for r in REC if r.get("via") == "canal"), "contado_noche": sum(1 for r in REC if r.get("via") == "noche"), "visto": len(VIS), "contagio": cont, "recibidos": len(REC) + len(VIS),
            "puesto": (fin or {}).get("placement"), "corte": corte, "marcada": not ((p.get("latencia") or {}).get(str(sl)) or {}).get("pasa", True), "latencia": (p.get("latencia") or {}).get(str(sl))}


def serie_brazo(S, b):
    out = {"dias": {}, "vidas": {}}
    for d in range(1, 21):
        cs = {sl: cuaderno(S, d, b, sl) for sl in (10, 11)}
        if any(c is None for c in cs.values()): continue
        out["dias"][d] = {"creencia_botiquin": {sl: cre(c, "first_aid") for sl, c in cs.items()}, "dif_objetos": [abs(cre(cs[10], o) - cre(cs[11], o)) for o in OBJ], "creencias": {sl: {NOM[o]: cre(c, o) for o in OBJ} for sl, c in cs.items()}}
        for sl in (10, 11):
            v = diario(S, d, b, sl)
            if v: out["vidas"][(d, sl)] = v
    return out


DATOS = {S: {b: serie_brazo(S, b) for b in BRAZOS} for S in SERIES}


def evalua(fuera_marcadas):
    def dias_validos(S):
        ds = set(range(1, 21))
        for b in BRAZOS:
            ds &= set(DATOS[S][b]["dias"])
            if fuera_marcadas: ds -= {d for (d, sl), v in DATOS[S][b]["vidas"].items() if v["marcada"]}
        return sorted(ds)
    S1 = {"COMPARTE": [], "SOLAS": [], "hermana": {}}; S2 = {"COMPARTE": [], "SOLAS": []}; S3 = {"COMPARTE": [], "SOLAS": []}; VIG = {}
    for S in SERIES:
        ds = dias_validos(S)
        if not ds: continue
        # la hermana que menos prueba, en SOLAS
        pru = {sl: sum(v["huellas"] for (d, s_), v in DATOS[S]["SOLAS"]["vidas"].items() if s_ == sl and d in ds) for sl in (10, 11)}
        menos = min(pru, key=pru.get); S1["hermana"][S] = {"asiento": menos, "pruebas_solas": pru}
        for b in BRAZOS:
            S1[b].append(sum(DATOS[S][b]["dias"][d]["creencia_botiquin"][menos] for d in ds))
            d11 = [d for d in ds if d >= 11]; S2[b].append(st.mean(x for d in d11 for x in DATOS[S][b]["dias"][d]["dif_objetos"]) if d11 else None)
            vs = [v for (d, sl), v in DATOS[S][b]["vidas"].items() if d in ds]; tot = sum(v["huellas"] for v in vs); S3[b].append((sum(v["huellas_inutil"] for v in vs) / tot) if tot else None)
            VIG[(S, b)] = {"dias_validos": len(ds), "pruebas_valiente": sum(v["huellas"] for (d, sl), v in DATOS[S][b]["vidas"].items() if sl == 10 and d in ds), "pruebas_prudente": sum(v["huellas"] for (d, sl), v in DATOS[S][b]["vidas"].items() if sl == 11 and d in ds),
                           "recibidos": {k: sum(v[k] for (d, sl), v in DATOS[S][b]["vidas"].items() if d in ds) for k in ("contado_canal", "contado_noche", "visto", "contagio", "recibidos")},
                           "puesto": {h: mean([v["puesto"] for (d, sl), v in DATOS[S][b]["vidas"].items() if sl == slh and d in ds and v["puesto"] is not None and not v["corte"]]) for h, slh in (("valiente", 10), ("prudente", 11))},
                           "marcadas": sum(1 for (d, sl), v in DATOS[S][b]["vidas"].items() if v["marcada"]), "creencia_botiquin_d20": {sl: DATOS[S][b]["dias"].get(20, {}).get("creencia_botiquin", {}).get(sl) for sl in (10, 11)}}
    def comp(xs_c, xs_s, menor):
        xc = [x for x in xs_c if x is not None]; xs = [x for x in xs_s if x is not None]
        if not xc or not xs: return {"dif": None}
        d = st.mean(xc) - st.mean(xs); e = (((ee(xc) or 0) ** 2 + (ee(xs) or 0) ** 2) ** 0.5); return {"COMPARTE": [round(x, 3) for x in xc], "SOLAS": [round(x, 3) for x in xs], "media_C": round(st.mean(xc), 3), "media_S": round(st.mean(xs), 3), "dif": round(d, 3), "ee": round(e, 3), "tres_veces": bool(e and abs(d) >= 3 * e), "direccion_ok": (d < 0) if menor else (d > 0), "pasa": bool(e and abs(d) >= 3 * e and ((d < 0) if menor else (d > 0)))}
    return {"S1": {**comp(S1["COMPARTE"], S1["SOLAS"], False), "hermana": {str(k): v for k, v in S1["hermana"].items()}}, "S2": comp(S2["COMPARTE"], S2["SOLAS"], True), "S3": comp(S3["COMPARTE"], S3["SOLAS"], True), "vigilancia": {f"s{S} {b}": v for (S, b), v in VIG.items()}}


R = {"series": SERIES, "con_todas": evalua(False), "sin_marcadas": evalua(True), "partidas": len([p for p in E["peticiones"] if p["estado"] == "completed"]), "marcadas": [(p["serie"], p["dia"], p["brazo"], sl) for p in E["peticiones"] for sl, g in (p.get("latencia") or {}).items() if not g.get("pasa")],
     "curvas": {f"s{S} {b}": {str(d): x["creencia_botiquin"] for d, x in DATOS[S][b]["dias"].items()} for S in SERIES for b in BRAZOS}}
json.dump(R, open(os.path.join(AQUI, "P7_50_sello.json"), "w"), ensure_ascii=False, indent=1)
for k in ("S1", "S2", "S3"): print(k, {kk: vv for kk, vv in R["con_todas"][k].items() if kk not in ("COMPARTE", "SOLAS")})
print("vigilancia", json.dumps(R["con_todas"]["vigilancia"], ensure_ascii=False)[:1500])

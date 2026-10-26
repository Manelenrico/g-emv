"""[P7-53] REVISION DE ARI AL CAPITULO 4, sobre los 240 diarios validos de P7-50 (coste cero):
  1. DOBLE CUENTA: un uso de la hermana que llego como "visto" (P7_48_visto apuntado: objeto, t0 = tic en que lo vi) y ademas como "contado" (P7_48_contado por canal o noche:
     objeto, dia_emisora, tick_emisora = el tic de la hermana al cerrar SU ventana). Fusion por evento: mismo objeto, misma hermana, |tick_emisora - t0| <= 240 (la ventana), mismo dia
     (canal) o el contado de noche del dia siguiente con dia_emisora = ese dia. Duplicados y peso extra (la segunda copia: intensidad x B) por brazo y hermana.
  2. DISTANCIA Y VINCULO: por brazo y hermana, distancia media a la hermana (social.dist_pareja, tics con las dos vivas), fraccion de tics con la hermana a la vista (social.pareja_vista),
     roce_B medio (social.B); peso medio de los recuerdos recibidos (peso = intensidad x B, de P7_48_contado y P7_48_visto).
  3. S1 releida: la hermana que menos prueba (de SOLAS, por serie), los pesos que recibio en COMPARTE frente a la otra, y la distancia.
  python3 analiza_P7_53.py -> P7_53_datos.json"""
import collections, glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
E = json.load(open(os.path.join(AQUI, "P7_50_estado.json"))); SE = json.load(open(os.path.join(AQUI, "P7_50_sello.json"))); VENT = 240
mean = lambda xs: (st.mean(xs) if xs else None)


def vida(f):
    T = 0; dist = []; vista = 0; B = []; VIS = []; REC = []; vivas = 0
    for line in open(f, errors="replace"):
        if line.startswith('{"k":"tick"'):
            r = json.loads(line)
            if r.get("phase") != "live": continue
            T += 1; s = r.get("social") or {}; B.append(float(s.get("B") or 0.0))
            if not r.get("pareja_muerta") and not s.get("pareja_muerta"):
                vivas += 1
                if s.get("dist_pareja") is not None: dist.append(float(s["dist_pareja"]))
                if s.get("pareja_vista"): vista += 1
        elif line.startswith('{"k":"P7_48_visto"'):
            r = json.loads(line)
            if r.get("estado") == "apuntado": VIS.append(r)
        elif line.startswith('{"k":"P7_48_contado"'): REC.append(json.loads(line))
    return {"tics": T, "tics_pareja_viva": vivas, "dist_media": mean(dist), "vista_frac": (vista / vivas if vivas else None), "B_medio": mean(B), "vistos": VIS, "contados": REC}


V = {}
for p in E["peticiones"]:
    if p["estado"] != "completed": continue
    c = glob.glob(os.path.join(RUNS, f"P750_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}"))
    if not c: continue
    for sl in (10, 11):
        fs = glob.glob(os.path.join(c[0], f"*policy_agent_{sl}.art.log"))
        if fs: V[(p["serie"], p["dia"], p["brazo"], sl)] = vida(fs[0])
# 1. doble cuenta
DUP = []
for (S, d, b, sl), v in V.items():
    if b != "COMPARTE": continue
    cont_hoy = [r for r in v["contados"] if r.get("via") == "canal" and r.get("dia_emisora") == d]
    manana = V.get((S, d + 1, b, sl)); cont_noche = [r for r in (manana or {}).get("contados", []) if r.get("via") == "noche" and r.get("dia_emisora") == d]
    for x in v["vistos"]:
        for r in cont_hoy + cont_noche:
            if r.get("objeto") == x.get("objeto") and abs(int(r.get("tick_emisora") or 0) - int(x.get("t0") or 0)) <= VENT:
                DUP.append({"serie": S, "dia": d, "asiento": sl, "objeto": x["objeto"], "t0_visto": x["t0"], "tick_hermana": r["tick_emisora"], "via": r["via"], "peso_visto": x.get("peso"), "peso_contado": r.get("peso"), "peso_extra": r.get("peso")}); break
por = collections.defaultdict(lambda: {"vidas": 0, "vistos": 0, "contados": 0, "duplicados": 0, "peso_extra": 0.0, "peso_recibido_total": 0.0, "n_recibidos": 0, "dist": [], "vista": [], "B": [], "pesos": []})
for (S, d, b, sl), v in V.items():
    g = por[(b, "valiente" if sl == 10 else "prudente")]; g["vidas"] += 1; g["vistos"] += len(v["vistos"]); g["contados"] += len(v["contados"])
    pesos = [float(r.get("peso") or 0) for r in v["contados"]] + [float(x.get("peso") or 0) for x in v["vistos"]]; g["pesos"] += pesos; g["peso_recibido_total"] += sum(pesos); g["n_recibidos"] += len(pesos)
    if v["dist_media"] is not None: g["dist"].append(v["dist_media"])
    if v["vista_frac"] is not None: g["vista"].append(v["vista_frac"])
    if v["B_medio"] is not None: g["B"].append(v["B_medio"])
for x in DUP: g = por[("COMPARTE", "valiente" if x["asiento"] == 10 else "prudente")]; g["duplicados"] += 1; g["peso_extra"] += float(x["peso_extra"] or 0)
RES = {f"{b} · {h}": {"vidas": g["vidas"], "vistos": g["vistos"], "contados": g["contados"], "recibidos": g["n_recibidos"], "duplicados": g["duplicados"], "peso_extra": round(g["peso_extra"], 3), "peso_recibido_total": round(g["peso_recibido_total"], 3), "peso_medio_recibido": (round(mean(g["pesos"]), 3) if g["pesos"] else None),
                       "dist_media": round(mean(g["dist"]), 2), "vista_frac": round(mean(g["vista"]), 3), "B_medio": round(mean(g["B"]), 3)} for (b, h), g in por.items()}
# 3. S1 releida: por serie, la hermana que menos prueba (de SOLAS), y en COMPARTE los pesos recibidos por cada hermana y su distancia
herm = SE["con_todas"]["S1"]["hermana"]; S1 = {}
for S in (1, 2, 3):
    k = str(S); menos = herm[k]["asiento"]; fila = {"hermana_que_menos_prueba": menos, "pruebas_solas": herm[k]["pruebas_solas"]}
    for sl in (10, 11):
        vs = [V[(S, d, "COMPARTE", sl)] for d in range(1, 21) if (S, d, "COMPARTE", sl) in V]
        pes = [float(r.get("peso") or 0) for v in vs for r in v["contados"]] + [float(x.get("peso") or 0) for v in vs for x in v["vistos"]]
        fila[f"a{sl}"] = {"recibidos": len(pes), "peso_total": round(sum(pes), 2), "peso_medio": (round(mean(pes), 3) if pes else None), "dist_media": round(mean([v["dist_media"] for v in vs if v["dist_media"] is not None]), 2), "B_medio": round(mean([v["B_medio"] for v in vs]), 3), "vista_frac": round(mean([v["vista_frac"] for v in vs if v["vista_frac"] is not None]), 3)}
    S1[k] = fila
R = {"por_brazo_hermana": RES, "duplicados": DUP, "S1": S1, "S1_sello": {k: v for k, v in SE["con_todas"]["S1"].items() if k != "hermana"}, "S2_sello": SE["con_todas"]["S2"], "vidas": len(V)}
json.dump(R, open(os.path.join(AQUI, "P7_53_datos.json"), "w"), ensure_ascii=False, indent=1)
for k, v in RES.items(): print(k, v)
print("duplicados", len(DUP), DUP[:3]); print("S1", json.dumps(S1, ensure_ascii=False)[:900])

"""[P7-65] = potencia_P7_63 con las predicciones de P7-65: L2 compara d15-20 con d8-11; L3 no se juzga (sin contraste: decision de Manel); L4 sobre las invitaciones VERDADERAS de COGER
(cualquier cosa) de la prudente. Cabecera de potencia_P7_63:
[P7-63] POTENCIA de L1-L4 con 3 series, con el ruido de las series 1-3 de P7-61 (mismo diseno de brazos; la falsa era otra: el botiquin en amenaza; sustituto declarado), con las funciones
de analiza_P7_61. Efecto minimo detectable a 3 ee.
  L1 (por evaluacion de la falsa): con la falsa de la racion, una evaluacion que falla baja la confianza en el cuerpo exactamente 0,3 x c (c <- 0,7 c + 0,3 x 0): la caida es segura
     por construccion siempre que la falsa falle; se calcula cuantas evaluaciones y criaturas con >= 3 harian falta con el ruido entre criaturas de P7-61 (diferencias de las que fallaron).
  L2 (misma criatura): fraccion de dias-oportunidad con la falsa aceptada al menos una vez, d15-20 menos d8-12, por criatura que miente (9 en 3 series): sd de la diferencia emparejada.
  L3 (por serie): aceptaciones de la falsa / oportunidades de la valiente, d10-20, MIENTE_UNA frente a MIENTEN_DOS (= M3 de P7-61).
  L4 (por serie): fraccion de invitaciones verdaderas con cuerpo != 0 aceptadas al menos una vez, d12-20, prudente de MIENTEN_DOS frente a prudente de MIENTE_UNA.
  python3 potencia_P7_63.py -> P7_65_potencia.json"""
import json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI); sys.argv = sys.argv[:1]
import analiza_P7_61 as A
V = A.carga("P7_57", [1, 2, 3]); r4 = lambda x: (round(x, 4) if x is not None else None)
def acepta_dias(S, b, sl, dias):
    op = ac = 0
    for d in dias:
        v = V.get((S, d, b, sl))
        if not v or v["pos"] is None: continue
        if any(x["n"] == v["pos"] for x in v["activa"]): op += 1; ac += any(x["n"] == v["pos"] for x in v["acept"])
    return (ac / op) if op else None, op
L2 = []
for S in (1, 2, 3):
    for b, sl in (("MIENTEN_DOS", 10), ("MIENTEN_DOS", 11), ("MIENTE_UNA", 10)):
        a, oa = acepta_dias(S, b, sl, range(8, 12)); z, oz = acepta_dias(S, b, sl, range(15, 21))
        L2.append({"criatura": f"s{S} {b} a{sl}", "d8_11": r4(a), "op_d8_11": oa, "d15_20": r4(z), "op_d15_20": oz, "dif": r4(z - a) if a is not None and z is not None else None})
dif = [x["dif"] for x in L2 if x["dif"] is not None]; sd2 = st.stdev(dif)
def m3(S, b):
    op = ac = 0
    for d in range(10, 21):
        v = V.get((S, d, b, 10))
        if v and v["pos"] is not None and any(x["n"] == v["pos"] for x in v["activa"]): op += 1; ac += sum(1 for x in v["acept"] if x["n"] == v["pos"])
    return ac / op if op else None
def l4(S, b):
    tot = acc = 0
    for d in range(12, 21):
        v = V.get((S, d, b, 11))
        if not v: continue
        ac = {x["n"] for x in v["acept"]}
        for k, i in enumerate(v["inv"]):
            if A.es_verdad(i) and str(i["accion"]).startswith("COGER_"): tot += 1; acc += (k in ac)
    return acc / tot if tot else None
def pot(xa, xb):
    sa, sb = st.stdev(xa), st.stdev(xb); e = math.sqrt(sa * sa / len(xa) + sb * sb / len(xb)); m = st.mean(xb)
    return {"A": [r4(x) for x in xa], "B": [r4(x) for x in xb], "sd_A": r4(sa), "sd_B": r4(sb), "ee_3_series": r4(e), "efecto_min_3ee": r4(3 * e), "efecto_min_pct_de_B": round(100 * 3 * e / m, 1) if m else None,
            "series_para_30pct": math.ceil(9 * (sa * sa + sb * sb) / (0.3 * m) ** 2) if m else None}
L3 = pot([m3(S, "MIENTE_UNA") for S in (1, 2, 3)], [m3(S, "MIENTEN_DOS") for S in (1, 2, 3)])
L4 = pot([l4(S, "MIENTEN_DOS") for S in (1, 2, 3)], [l4(S, "MIENTE_UNA") for S in (1, 2, 3)])
F = A.falsas(V, False); fallan = [f for f in F if f["acierto"] == 0]
cri = {}
for f in fallan: cri.setdefault((f["serie"], f["brazo"], f["asiento"]), []).append(f["dif"])
R = {"L1": {"regla": "una evaluacion que falla: c <- 0,7 c, caida = 0,3 c (> 0 si c > 0): segura por construccion si la falsa falla", "P7_61_fallos": len(fallan), "caida_media_si_falla": r4(st.mean([f["dif"] for f in fallan])),
            "sd": r4(st.stdev([f["dif"] for f in fallan])), "todas_caen": all(f["dif"] < 0 for f in fallan), "criaturas": len(cri), "media_por_criatura": {f"s{k[0]} {k[1]} a{k[2]}": r4(st.mean(v)) for k, v in cri.items()},
            "evaluaciones_para_3ee": math.ceil(9 * st.stdev([f["dif"] for f in fallan]) ** 2 / st.mean([f["dif"] for f in fallan]) ** 2)},
     "L2": {"criaturas": L2, "n": len(dif), "media_dif_P7_61": r4(st.mean(dif)), "sd_dif": r4(sd2), "ee_9_criaturas": r4(sd2 / 3), "efecto_min_3ee": r4(3 * sd2 / 3), "base_d8_11": r4(st.mean([x["d8_11"] for x in L2 if x["d8_11"] is not None]))},
     "L3": {"no_se_juzga": "sin contraste con lo contado (decision de Manel, 15-oct): L3 no tiene forma de medirse en este campo"}, "L4": L4}
json.dump(R, open(os.path.join(AQUI, "P7_65_potencia.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R.items(): print(k, {kk: vv for kk, vv in v.items() if kk not in ("criaturas", "media_por_criatura")})

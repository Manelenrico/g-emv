"""[P7-49] POTENCIA Y COSTE del campo del capitulo 4 con el ruido de P7-45 (SELLO_P7_49.md): de P7_42_datos.json (720 vidas, APRENDE_v / APRENDE_p: 12 criaturas, 6 parejas-serie)
  S1 area bajo la curva de la creencia del botiquin (d1-20) por criatura -> desviacion tipica entre criaturas;
  S2 parecido entre hermanas (|c10 - c11| en d11-20, cuatro objetos, media) por pareja-serie -> desviacion tipica entre las 6;
  S3 fraccion de pruebas a red + camuflaje (las dos juntas, d1-20) por pareja-serie -> desviacion tipica entre las 6.
Series necesarias (una observacion por serie y brazo) para que un efecto del 30 % y del 50 % de la media sea >= 3 errores tipicos: 3 x sd x sqrt(2 / n) <= efecto
-> n >= 18 sd^2 / efecto^2 (por brazo). Coste = 2 x 20 x n + 3.  python3 potencia_P7_49.py -> P7_49_potencia.json"""
import json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); V = [v for v in json.load(open(os.path.join(AQUI, "P7_42_datos.json"))) if not v.get("sin_diario") and v["variante"] in ("APRENDE_v", "APRENDE_p")]
OBJ = ("botiquin", "racion", "red", "camuflaje")
def cre(v, o): x = ((v.get("al_acabar") or {}).get(o) or {}).get("creencia"); return float(x) if x is not None else 0.0
S1 = []; S2 = []; S3 = []; PRU = {}
for var in ("APRENDE_v", "APRENDE_p"):
    for s in (1, 2, 3):
        vidas = {sl: sorted([v for v in V if v["variante"] == var and v["serie"] == s and v["asiento"] == sl], key=lambda v: v["dia"]) for sl in (10, 11)}
        for sl in (10, 11):
            S1.append(sum(cre(v, "botiquin") for v in vidas[sl])); PRU[(var, s, sl)] = sum(v.get("pruebas_dia") or 0 for v in vidas[sl])
        d = [abs(cre(a, o) - cre(b, o)) for a, b in zip(vidas[10], vidas[11]) if a["dia"] >= 11 for o in OBJ]; S2.append(st.mean(d) if d else None)
        pc = [v.get("pruebas_por_cosa") or {} for sl in (10, 11) for v in vidas[sl]]; tot = sum(sum(p.values()) for p in pc); inu = sum(p.get("red", 0) + p.get("camuflaje", 0) for p in pc); S3.append(inu / tot if tot else None)
S2 = [x for x in S2 if x is not None]; S3 = [x for x in S3 if x is not None]
def fila(nombre, xs):
    mu = st.mean(xs); sd = st.stdev(xs); out = {"n_obs": len(xs), "media": round(mu, 4), "sd": round(sd, 4), "valores": [round(x, 4) for x in xs]}
    for e in (0.3, 0.5):
        ef = e * mu; n = math.ceil(18 * sd * sd / (ef * ef)) if ef > 0 else None; out[f"series_{int(100 * e)}"] = n; out[f"coste_{int(100 * e)}"] = (2 * 20 * n + 3) if n else None
    # con 3 series por brazo: el efecto minimo detectable (3 ee) en % de la media
    for k_ in (2, 3, 5, 10): out[f"efecto_min_{k_}_series_pct"] = round(100 * 3 * sd * math.sqrt(2 / k_) / mu, 1) if mu else None
    return out
R = {"S1_area_botiquin": fila("S1", S1), "S2_parecido": fila("S2", S2), "S3_fraccion_inutil": fila("S3", S3), "pruebas_por_criatura": {f"{k[0]} s{k[1]} a{k[2]}": v for k, v in PRU.items()},
     "nota": "S1 usa la sd entre las 12 criaturas (la hermana que menos prueba es una por serie: una observacion por serie y brazo); S2 y S3 la sd entre las 6 parejas-serie"}
json.dump(R, open(os.path.join(AQUI, "P7_49_potencia.json"), "w"), ensure_ascii=False, indent=1)
for k in ("S1_area_botiquin", "S2_parecido", "S3_fraccion_inutil"): print(k, {kk: vv for kk, vv in R[k].items() if kk != "valores"})

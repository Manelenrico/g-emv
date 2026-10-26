"""[P7-8] LAS CINCO PREDICCIONES DEL SELLO, calculadas sobre P7_8_campo.json con las definiciones de SELLO_P7_8.md. -> P7_8_sello_resultado.json"""
import json, math, os, statistics, collections
AQUI = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(AQUI, "P7_8_campo.json")))
V = [v for v in C.values() if not v.get("sin_tics")]
def vidas(brazo, dias=None): return [v for v in V if v["brazo"] == brazo and (dias is None or v["dia"] in dias)]
D11 = set(range(11, 21))
def usos(v, cond): return sum(1 for u in v["usos"] if u["gastado"] and cond(u))
def media(xs): return statistics.mean(xs) if xs else None
R = {}
# P1
ign = {f"s{v['serie']}_{v['slot']}": (v.get("cuaderno") or {}).get("ignorancia") for v in vidas("APRENDE", {10})}
R["P1"] = {"ignorancia_dia10_APRENDE": ign, "bajo_0_3": sum(1 for x in ign.values() if x is not None and x < 0.3), "de": len(ign), "pasa": (sum(1 for x in ign.values() if x is not None and x < 0.3) >= 3) if len(ign) == 4 else None}
# P2, P3
alta = {b: media([usos(v, lambda u: u["hp0"] >= 80) for v in vidas(b, D11)]) for b in ("SUELO", "BORRADO", "APRENDE", "TECHO")}
baja = {b: media([usos(v, lambda u: u["hp0"] < 50) for v in vidas(b, D11)]) for b in ("SUELO", "BORRADO", "APRENDE", "TECHO")}
n11 = {b: len(vidas(b, D11)) for b in ("SUELO", "BORRADO", "APRENDE", "TECHO")}
R["P2"] = {"usos_vida_80_o_mas_por_vida_d11_20": alta, "vidas": n11, "pasa": (alta["APRENDE"] < alta["BORRADO"] / 2) if (alta["APRENDE"] is not None and alta["BORRADO"] is not None) else None}
R["P3"] = {"usos_vida_bajo_50_por_vida_d11_20": baja, "pasa_APRENDE_vs_TECHO": (baja["APRENDE"] >= baja["TECHO"] / 2) if (baja["APRENDE"] is not None and baja["TECHO"] is not None) else None, "pasa_SUELO_casi_cero": (baja["SUELO"] <= 0.1) if baja["SUELO"] is not None else None}
R["P3"]["pasa"] = (R["P3"]["pasa_APRENDE_vs_TECHO"] and R["P3"]["pasa_SUELO_casi_cero"]) if (R["P3"]["pasa_APRENDE_vs_TECHO"] is not None and R["P3"]["pasa_SUELO_casi_cero"] is not None) else None
# P4
fuera = {}
for b in ("SUELO", "BORRADO", "APRENDE", "TECHO"):
    us = [u for v in vidas(b, D11) for u in v["usos"] if u["gastado"]]
    fuera[b] = {"usos": len(us), "fuera": sum(1 for u in us if u["situacion"] == "fuera"), "proporcion": (sum(1 for u in us if u["situacion"] == "fuera") / len(us)) if us else None}
R["P4"] = {"fuera_d11_20": fuera, "pasa": (fuera["APRENDE"]["proporcion"] < fuera["TECHO"]["proporcion"]) if (fuera["APRENDE"]["proporcion"] is not None and fuera["TECHO"]["proporcion"] is not None) else None}
# P5: pares por (serie, dia, asiento)
def por_clave(b): return {(v["serie"], v["dia"], v["slot"]): v for v in vidas(b)}
P5 = {}; pasa5 = True; algun = False
for med in ("hp_final", "puesto"):
    for i, a in enumerate(("SUELO", "BORRADO", "APRENDE", "TECHO")):
        for b in ("SUELO", "BORRADO", "APRENDE", "TECHO")[i + 1:]:
            A, B = por_clave(a), por_clave(b); ks = sorted(set(A) & set(B))
            d = [float(A[k][med]) - float(B[k][med]) for k in ks if A[k][med] is not None and B[k][med] is not None]
            if len(d) >= 2:
                m = statistics.mean(d); se = statistics.stdev(d) / math.sqrt(len(d)); dentro = abs(m) <= 2 * se; algun = True; pasa5 = pasa5 and dentro
                P5[f"{med}:{a}-{b}"] = {"n": len(d), "media_dif": round(m, 3), "se": round(se, 3), "dentro_2se": dentro}
R["P5"] = {"pares": P5, "medias": {b: {"hp_final": media([float(v["hp_final"]) for v in vidas(b) if v["hp_final"] is not None]), "puesto": media([float(v["puesto"]) for v in vidas(b) if v["puesto"] is not None]), "n": len(vidas(b))} for b in ("SUELO", "BORRADO", "APRENDE", "TECHO")}, "pasa": pasa5 if algun else None}
R["resumen"] = {p: R[p]["pasa"] for p in ("P1", "P2", "P3", "P4", "P5")}
json.dump(R, open(os.path.join(AQUI, "P7_8_sello_resultado.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R["resumen"]), json.dumps({k: v for k, v in R.items() if k in ("P1", "P2", "P3", "P4")}, ensure_ascii=False)[:1500])

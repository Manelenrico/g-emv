"""[P7-10] LAS SEIS PREDICCIONES DEL SELLO, sobre P7_10_campo.json con las definiciones de SELLO_P7_10.md. -> P7_10_sello_resultado.json"""
import json, math, os, statistics
AQUI = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(AQUI, "P7_10_campo.json"))); V = [v for v in C.values() if not v.get("sin_tics")]
BR = ("SUELO", "BORRADO", "APRENDE", "TECHO")
def vidas(b, dias=None, serie=None, slot=None): return [v for v in V if v["brazo"] == b and (dias is None or v["dia"] in dias) and (serie is None or v["serie"] == serie) and (slot is None or v["slot"] == slot)]
def vidas_al_usar(vs): return [u["hp0"] for v in vs for u in v["usos"] if u["gastado"]]
def med(xs): return statistics.median(xs) if xs else None
def cre(v):
    c = ((v.get("cuaderno") or {}).get("creencias") or {}).get("first_aid") or {}; d = c.get("dentro")
    return (d.get("cuerpo") if isinstance(d, dict) else None)
R = {}
# P1
p1 = {}
for s in (1, 2):
    for sl in (10, 11):
        a, b = med(vidas_al_usar(vidas("APRENDE", range(1, 6), s, sl))), med(vidas_al_usar(vidas("APRENDE", range(16, 21), s, sl)))
        p1[f"s{s}_{sl}"] = {"mediana_vida_d1_5": a, "n_usos_d1_5": len(vidas_al_usar(vidas("APRENDE", range(1, 6), s, sl))), "mediana_vida_d16_20": b, "n_usos_d16_20": len(vidas_al_usar(vidas("APRENDE", range(16, 21), s, sl))), "cumple": (a is not None and b is not None and b < a)}
R["P1"] = {"criaturas": p1, "cumplen": sum(1 for x in p1.values() if x["cumple"]), "pasa": sum(1 for x in p1.values() if x["cumple"]) >= 3}
# P2
ma, mb = med(vidas_al_usar(vidas("APRENDE", range(11, 21)))), med(vidas_al_usar(vidas("BORRADO", range(11, 21))))
R["P2"] = {"mediana_vida_al_usar_d11_20": {"APRENDE": ma, "BORRADO": mb, "n_APRENDE": len(vidas_al_usar(vidas("APRENDE", range(11, 21)))), "n_BORRADO": len(vidas_al_usar(vidas("BORRADO", range(11, 21))))}, "pasa": (ma is not None and mb is not None and ma < mb)}
# P3, P4
p3 = {}; p4 = {}
for s in (1, 2):
    for sl in (10, 11):
        v5 = vidas("APRENDE", {5}, s, sl); v20 = vidas("APRENDE", {20}, s, sl)
        c5 = cre(v5[0]) if v5 else None; c20 = cre(v20[0]) if v20 else None
        p3[f"s{s}_{sl}"] = {"creencia_d5": c5, "creencia_d20": c20, "cumple": (c20 or 0) > (c5 or 0) if v20 else False}
        p4[f"s{s}_{sl}"] = {"creencia_final": c20, "cumple": (c20 is not None and c20 < 40) if v20 else False}
R["P3"] = {"criaturas": p3, "cumplen": sum(1 for x in p3.values() if x["cumple"]), "pasa": sum(1 for x in p3.values() if x["cumple"]) >= 3}
R["P4"] = {"criaturas": p4, "cumplen": sum(1 for x in p4.values() if x["cumple"]), "pasa": sum(1 for x in p4.values() if x["cumple"]) >= 3}
# P5
su = vidas("SUELO"); usos_suelo = sum(sum(1 for u in v["usos"] if u["gastado"]) for v in su) / len(su) if su else None
mt, ma5 = med(vidas_al_usar(vidas("TECHO", range(1, 6)))), med(vidas_al_usar(vidas("APRENDE", range(1, 6))))
R["P5"] = {"usos_por_vida_SUELO": usos_suelo, "vidas_SUELO": len(su), "mediana_vida_al_usar_d1_5": {"TECHO": mt, "APRENDE": ma5}, "pasa_suelo": (usos_suelo is not None and usos_suelo <= 0.1), "pasa_techo": (mt is not None and ma5 is not None and mt < ma5)}
R["P5"]["pasa"] = bool(R["P5"]["pasa_suelo"] and R["P5"]["pasa_techo"])
# P6
P6 = {}; ok6 = True; alg = False
def por_clave(b): return {(v["serie"], v["dia"], v["slot"]): v for v in vidas(b)}
for medida in ("hp_final", "puesto"):
    for i, a in enumerate(BR):
        for b in BR[i + 1:]:
            A, B_ = por_clave(a), por_clave(b); ks = sorted(set(A) & set(B_))
            d = [float(A[k][medida]) - float(B_[k][medida]) for k in ks if A[k][medida] is not None and B_[k][medida] is not None]
            if len(d) >= 2:
                m = statistics.mean(d); se = statistics.stdev(d) / math.sqrt(len(d)); dentro = abs(m) <= 2 * se; alg = True; ok6 = ok6 and dentro
                P6[f"{medida}:{a}-{b}"] = {"n": len(d), "media_dif": round(m, 3), "se": round(se, 3), "dentro_2se": dentro}
R["P6"] = {"pares": P6, "medias": {b: {"hp_final": (statistics.mean([float(v["hp_final"]) for v in vidas(b) if v["hp_final"] is not None]) if vidas(b) else None), "puesto": (statistics.mean([float(v["puesto"]) for v in vidas(b) if v["puesto"] is not None]) if vidas(b) else None), "n": len(vidas(b))} for b in BR}, "pasa": ok6 if alg else None}
R["resumen"] = {p: R[p]["pasa"] for p in ("P1", "P2", "P3", "P4", "P5", "P6")}
json.dump(R, open(os.path.join(AQUI, "P7_10_sello_resultado.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R["resumen"]))

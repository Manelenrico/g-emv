"""[P7-14] LAS CINCO PREGUNTAS DEL SELLO, sobre P7_14_campo.json (campo_P7_14.py) y P7_14_vidas.json (analiza_P7_14.py), con las definiciones de
SELLO_P7_14.md. Las referencias de P7-10 se leen de P7_11_vidas.json (no se copian a mano). -> P7_14_sello_resultado.json"""
import json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(AQUI, p)))
C = [v for v in J("P7_14_campo.json").values() if not v.get("sin_tics")]; V = list(J("P7_14_vidas.json").values()); V10 = [v for v in J("P7_11_vidas.json").values() if v["brazo"] == "APRENDE"]
def vidas(L, b, dias=None): return [v for v in L if v["brazo"] == b and (dias is None or v["dia"] in dias)]
med = lambda xs: (st.median(xs) if xs else None); R = {}
# Q1 (principal): APRENDE - BORRADO, emparejado por (serie, dia, asiento), puesto y vida al morir: |media| <= 2 se
q1 = {}; ok = True
for medida in ("puesto", "hp_final"):
    A = {(v["serie"], v["dia"], v["slot"]): v for v in vidas(C, "APRENDE")}; B = {(v["serie"], v["dia"], v["slot"]): v for v in vidas(C, "BORRADO")}
    d = [float(A[k][medida]) - float(B[k][medida]) for k in sorted(set(A) & set(B)) if A[k][medida] is not None and B[k][medida] is not None]
    m = st.mean(d); se = st.stdev(d) / math.sqrt(len(d)); dentro = abs(m) <= 2 * se; ok = ok and dentro
    q1[medida] = {"n": len(d), "media_APRENDE": round(st.mean(float(A[k][medida]) for k in A if A[k][medida] is not None), 3), "media_BORRADO": round(st.mean(float(B[k][medida]) for k in B if B[k][medida] is not None), 3), "media_dif": round(m, 3), "se": round(se, 3), "dentro_2se": dentro}
R["Q1"] = {**q1, "pasa": ok}
# Q2: regalos por vida de APRENDE <= 1/4 de los de P7-10; vueltos a coger por el mismo <= 1/10
ap = vidas(V, "APRENDE"); reg = sum(v["regala_n"] for v in ap) / len(ap); rec = sum(1 for v in ap for g in v["regala"] if g["destino"] == "lo recoge el mismo") / len(ap)
reg10 = sum(v["regala_n"] for v in V10) / len(V10); rec10 = sum(1 for v in V10 for g in v["regala"] if g["destino"] == "lo recoge el mismo") / len(V10)
R["Q2"] = {"vidas": len(ap), "regalos": sum(v["regala_n"] for v in ap), "regalos_por_vida": round(reg, 4), "P7_10_regalos_por_vida": round(reg10, 4), "tope_regalos_por_vida": round(reg10 / 4, 4),
           "vueltos_a_coger": sum(1 for v in ap for g in v["regala"] if g["destino"] == "lo recoge el mismo"), "vueltos_a_coger_por_vida": round(rec, 4), "P7_10_vueltos_por_vida": round(rec10, 4), "tope_vueltos_por_vida": round(rec10 / 10, 4),
           "pasa_regalos": reg <= reg10 / 4, "pasa_vueltos": rec <= rec10 / 10, "pasa": bool(reg <= reg10 / 4 and rec <= rec10 / 10)}
# Q3: parte de la vida yendo a por botiquines, dias 11-20: APRENDE no mayor que BORRADO
fr = lambda b: [v["contadores"].get("tics ir a por un botiquin", 0) / v["contadores"]["tics"] for v in vidas(V, b, range(11, 21))]
tc = lambda b: [v["contadores"].get("tics ir a por un botiquin", 0) for v in vidas(V, b, range(11, 21))]
R["Q3"] = {"parte_de_la_vida_APRENDE": round(st.mean(fr("APRENDE")), 5), "parte_de_la_vida_BORRADO": round(st.mean(fr("BORRADO")), 5), "tics_por_vida_APRENDE": round(st.mean(tc("APRENDE")), 1), "tics_por_vida_BORRADO": round(st.mean(tc("BORRADO")), 1),
           "n_APRENDE": len(fr("APRENDE")), "n_BORRADO": len(fr("BORRADO")), "pasa": st.mean(fr("APRENDE")) <= st.mean(fr("BORRADO"))}
# Q4: la creencia sube en 4 de 4 (dia 20 > dia 5; "no se" = 0) y, dias 11-20, APRENDE usa con menos vida que BORRADO
def cre(v):
    d = (((v.get("cuaderno") or {}).get("creencias") or {}).get("first_aid") or {}).get("dentro"); return d.get("cuerpo") if isinstance(d, dict) else None
cr = {}
for s in (1, 2):
    for sl in (10, 11):
        v5 = [v for v in vidas(C, "APRENDE", {5}) if v["serie"] == s and v["slot"] == sl]; v20 = [v for v in vidas(C, "APRENDE", {20}) if v["serie"] == s and v["slot"] == sl]
        c5 = cre(v5[0]) if v5 else None; c20 = cre(v20[0]) if v20 else None; cr[f"s{s}_{sl}"] = {"creencia_d5": c5, "creencia_d20": c20, "sube": bool(v20 and (c20 or 0) > (c5 or 0))}
hp = lambda b: [u["hp0"] for v in vidas(C, b, range(11, 21)) for u in v["usos"] if u["gastado"]]
R["Q4"] = {"criaturas": cr, "suben": sum(1 for x in cr.values() if x["sube"]), "pasa_creencia": sum(1 for x in cr.values() if x["sube"]) == 4,
           "mediana_vida_al_usar_d11_20": {"APRENDE": med(hp("APRENDE")), "BORRADO": med(hp("BORRADO")), "n_APRENDE": len(hp("APRENDE")), "n_BORRADO": len(hp("BORRADO"))},
           "pasa_vida": bool(hp("APRENDE") and hp("BORRADO") and med(hp("APRENDE")) < med(hp("BORRADO")))}
R["Q4"]["pasa"] = bool(R["Q4"]["pasa_creencia"] and R["Q4"]["pasa_vida"])
# Q5: cierres porque se lo dieron / cierres, los cuatro brazos juntos: < 1/5
ci = [c for v in V for c in v["cierres"]]; dados = sum(1 for c in ci if c["porque_se_lo_dieron"])
R["Q5"] = {"pedidos_abiertos": sum(v["pedidos_abiertos"] for v in V), "cerrados": len(ci), "porque_se_lo_dieron": dados, "fraccion": (round(dados / len(ci), 4) if ci else None),
           "por_brazo": {b: {"abiertos": sum(v["pedidos_abiertos"] for v in vidas(V, b)), "cerrados": sum(len(v["cierres"]) for v in vidas(V, b)), "porque_se_lo_dieron": sum(1 for v in vidas(V, b) for c in v["cierres"] if c["porque_se_lo_dieron"])} for b in ("ESPERANZA", "BORRADO", "APRENDE", "TECHO")},
           "pasa": bool(ci and dados / len(ci) < 0.2)}
R["resumen"] = {q: R[q]["pasa"] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")}
json.dump(R, open(os.path.join(AQUI, "P7_14_sello_resultado.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R["resumen"]))

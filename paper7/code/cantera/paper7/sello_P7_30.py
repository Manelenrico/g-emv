"""[P7-30] EL SELLO, evaluado una sola vez al final, desde P7_30_vidas.json -> P7_30_resumen.json. Definiciones: SELLO_P7_30.md (E1-E6 como en P7-24; E7 el cuanto; E8 no se hunde).
  python3 sello_P7_30.py"""
import collections, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); V = json.load(open(os.path.join(AQUI, "P7_30_vidas.json")))
L = [v for v in V.values() if not v.get("sin_diario")]
partidas_corte = sorted({(v["serie"], v["dia"], v["brazo"]) for v in V.values() if v.get("parcial") or v.get("sin_diario")})
# [P7-30, anadidos al sello] las partidas MARCADAS por la guarda de latencia (7 de BORRADO y s1 d2 APRENDE): el sello se evalua dos veces, con todas y quitandolas enteras
ES = json.load(open(os.path.join(AQUI, "P7_30_estado.json")))
partidas_marcadas = sorted({(p["serie"], p["dia"], p["brazo"]) for p in ES["peticiones"] for g in (p.get("latencia") or {}).values() if not g["pasa"]})
MARCADAS = set(partidas_marcadas)
def vidas(brazo, serie=None, slot=None, dias=None): return [v for v in L if v["brazo"] == brazo and (serie is None or v["serie"] == serie) and (slot is None or v["slot"] == slot) and (dias is None or v["dia"] in dias)]
R = {"partidas_con_corte": [list(x) for x in partidas_corte], "vidas_fuera_de_puesto": sum(1 for v in V.values() if (v["serie"], v["dia"], v["brazo"]) in partidas_corte), "partidas_marcadas": [list(x) for x in partidas_marcadas]}
# ── E1: descubre ──
e1 = {}
for s in (1, 2):
    for sl in (10, 11):
        vs = sorted(vidas("APRENDE", s, sl), key=lambda v: v["dia"]); d5 = next((v for v in vs if v["dia"] == 5), None); d10 = next((v for v in vs if v["dia"] == 10), None)
        firmes5 = {o: (d5["recuerdos_al_acabar"][o]["firmes"] if d5 else None) for o in ("botiquin", "racion")}
        ign10 = {o: (d10["al_acabar"][o]["ignorancia"] if d10 else None) for o in ("botiquin", "racion")}
        e1[f"s{s}_{sl}"] = {"firmes_al_acabar_el_dia_5": firmes5, "ignorancia_al_acabar_el_dia_10": ign10, "firme_de_los_dos_dia_5": bool(d5 and all((firmes5[o] or 0) >= 1 for o in firmes5)), "ignorancia_menor_0_3_dia_10": bool(d10 and all(ign10[o] is not None and ign10[o] < 0.3 for o in ign10))}
R["E1"] = {"criaturas": e1, "firme_de_los_dos_al_dia_5": sum(1 for x in e1.values() if x["firme_de_los_dos_dia_5"]), "ignorancia_menor_0_3_al_dia_10": sum(1 for x in e1.values() if x["ignorancia_menor_0_3_dia_10"])}
R["E1"]["pasa"] = R["E1"]["firme_de_los_dos_al_dia_5"] == 4 and R["E1"]["ignorancia_menor_0_3_al_dia_10"] >= 3
# ── E2: aprende a aprender; E3: que aprende antes ──
e2 = {}; e3 = {}
for s in (1, 2):
    for sl in (10, 11):
        vs = sorted(vidas("APRENDE", s, sl), key=lambda v: v["dia"]); acum = 0; contacto = {}; firme = {}
        for v in vs:
            for o in ("botiquin", "racion"):
                if o not in contacto and v["primer_contacto"][o] is not None: contacto[o] = acum + v["primer_contacto"][o]
                if o not in firme and v["primer_firme"][o] is not None: firme[o] = acum + v["primer_firme"][o]
            acum += v["tics"]
        tardas = {o: (firme[o] - contacto[o]) if (o in firme and o in contacto) else None for o in ("botiquin", "racion")}
        orden = sorted([o for o in firme], key=lambda o: firme[o])
        e2[f"s{s}_{sl}"] = {"contacto_acumulado": contacto, "primer_firme_acumulado": firme, "tarda_desde_el_contacto": tardas, "orden": orden, "el_segundo_tarda_menos": (len(orden) == 2 and tardas[orden[1]] is not None and tardas[orden[0]] is not None and tardas[orden[1]] < tardas[orden[0]])}
        # E3: el dia en que la creencia (con el neutro) llega al 80 %
        dr = next((v["dia"] for v in vs if max([x for x in v["al_acabar"]["racion"]["creencia"].values() if x is not None] or [0]) >= 0.8 * 15), None)
        dk = next((v["dia"] for v in vs if (v["al_acabar"]["botiquin"]["creencia"].get("dentro") or 0) >= 0.8 * 50), None)
        e3[f"s{s}_{sl}"] = {"dia_racion_12": dr, "dia_botiquin_dentro_40": dk, "racion_antes": (dr is not None and (dk is None or dr < dk))}
R["E2"] = {"criaturas": e2, "el_segundo_tarda_menos": sum(1 for x in e2.values() if x["el_segundo_tarda_menos"])}; R["E2"]["pasa"] = R["E2"]["el_segundo_tarda_menos"] >= 3
R["E3"] = {"criaturas": e3, "racion_antes": sum(1 for x in e3.values() if x["racion_antes"])}; R["E3"]["pasa"] = R["E3"]["racion_antes"] >= 3
# ── E4, E5 y la medida sin prediccion: puesto emparejado ──
def pares(bra, dias, excluir):
    out = []
    for s in (1, 2):
        for d in dias:
            if excluir and any((s, d, b) in partidas_corte for b in (bra, "TECHO") if True): pass
            for sl in (10, 11):
                a = next((v for v in L if v["brazo"] == bra and v["serie"] == s and v["dia"] == d and v["slot"] == sl), None); t = next((v for v in L if v["brazo"] == "TECHO" and v["serie"] == s and v["dia"] == d and v["slot"] == sl), None)
                if a is None or t is None or a.get("puesto") is None or t.get("puesto") is None: continue
                fuera = set(partidas_corte) | (MARCADAS if excluir == "marcadas" else set())
                if excluir and ((s, d, bra) in fuera or (s, d, "TECHO") in fuera): continue
                out.append(a["puesto"] - t["puesto"])
    return out
def resumen(x):
    if len(x) < 2: return {"n": len(x), "media": (x[0] if x else None), "ee": None}
    return {"n": len(x), "media": round(st.mean(x), 3), "ee": round(st.stdev(x) / len(x) ** 0.5, 3)}
R["puesto"] = {}
for bra in ("APRENDE", "BORRADO"):
    for ex, et in ((True, "excluyendo las partidas con corte"), (False, "sin excluir nada"), ("marcadas", "excluyendo cortes y marcadas")):
        p1 = resumen(pares(bra, range(1, 6), ex)); p2 = resumen(pares(bra, range(16, 21), ex))
        R["puesto"][f"{bra} - TECHO · {et}"] = {"dias 1-5": p1, "dias 16-20": p2}
def crit(bra, ex):
    et = {True: "excluyendo las partidas con corte", False: "sin excluir nada", "marcadas": "excluyendo cortes y marcadas"}[ex]
    p1 = R["puesto"][f"{bra} - TECHO · {et}"]["dias 1-5"]; p2 = R["puesto"][f"{bra} - TECHO · {et}"]["dias 16-20"]
    return p1, p2
p1, p2 = crit("APRENDE", True); R["E4"] = {"dias 1-5": p1, "dias 16-20": p2, "peor_por_mas_de_2_ee": bool(p1["ee"] and p1["media"] > 2 * p1["ee"]), "recupera_la_mitad": bool(p1["media"] is not None and p2["media"] is not None and p2["media"] <= 0.5 * p1["media"])}
R["E4"]["pasa"] = R["E4"]["peor_por_mas_de_2_ee"] and R["E4"]["recupera_la_mitad"]
q1, q2 = crit("BORRADO", True); R["E5"] = {"dias 1-5": q1, "dias 16-20": q2, "no_recupera": bool(q1["media"] is not None and q2["media"] is not None and q2["media"] >= 0.5 * q1["media"])}; R["E5"]["pasa"] = R["E5"]["no_recupera"]
p1s, p2s = crit("APRENDE", False); q1s, q2s = crit("BORRADO", False)
R["E4_sin_excluir"] = {"dias 1-5": p1s, "dias 16-20": p2s, "pasa": bool(p1s["ee"] and p1s["media"] > 2 * p1s["ee"] and p2s["media"] <= 0.5 * p1s["media"])}
R["E5_sin_excluir"] = {"dias 1-5": q1s, "dias 16-20": q2s, "pasa": bool(q2s["media"] is not None and q2s["media"] >= 0.5 * q1s["media"])}
p1m, p2m = crit("APRENDE", "marcadas"); q1m, q2m = crit("BORRADO", "marcadas")
R["E4_sin_marcadas"] = {"dias 1-5": p1m, "dias 16-20": p2m, "pasa": bool(p1m["ee"] and p1m["media"] > 2 * p1m["ee"] and p2m["media"] <= 0.5 * p1m["media"])}
R["E5_sin_marcadas"] = {"dias 1-5": q1m, "dias 16-20": q2m, "pasa": bool(q2m["media"] is not None and q1m["media"] is not None and q2m["media"] >= 0.5 * q1m["media"])}
# APRENDE frente a BORRADO (sin prediccion)
ab = []
for s in (1, 2):
    for d in range(1, 21):
        if (s, d, "APRENDE") in partidas_corte or (s, d, "BORRADO") in partidas_corte: continue
        for sl in (10, 11):
            a = next((v for v in L if v["brazo"] == "APRENDE" and v["serie"] == s and v["dia"] == d and v["slot"] == sl), None); b = next((v for v in L if v["brazo"] == "BORRADO" and v["serie"] == s and v["dia"] == d and v["slot"] == sl), None)
            if a and b and a.get("puesto") is not None and b.get("puesto") is not None: ab.append((d, a["puesto"] - b["puesto"]))
R["APRENDE - BORRADO"] = {"todos los dias": resumen([x for _, x in ab]), "dias 1-5": resumen([x for d, x in ab if d <= 5]), "dias 16-20": resumen([x for d, x in ab if d >= 16])}
# ── E6: vida al abrir el botiquin, dias 11-20 ──
hA = [h for v in vidas("APRENDE", dias=range(11, 21)) for h in v["aperturas_botiquin_hp"]]; hB = [h for v in vidas("BORRADO", dias=range(11, 21)) for h in v["aperturas_botiquin_hp"]]
R["E6"] = {"APRENDE": {"aperturas": len(hA), "mediana": (st.median(hA) if hA else None)}, "BORRADO": {"aperturas": len(hB), "mediana": (st.median(hB) if hB else None)}}
R["E6"]["pasa"] = bool(hA and hB and st.median(hA) < st.median(hB))
hAm = [h for v in vidas("APRENDE", dias=range(11, 21)) if (v["serie"], v["dia"], v["brazo"]) not in MARCADAS for h in v["aperturas_botiquin_hp"]]; hBm = [h for v in vidas("BORRADO", dias=range(11, 21)) if (v["serie"], v["dia"], v["brazo"]) not in MARCADAS for h in v["aperturas_botiquin_hp"]]
R["E6_sin_marcadas"] = {"APRENDE": {"aperturas": len(hAm), "mediana": (st.median(hAm) if hAm else None)}, "BORRADO": {"aperturas": len(hBm), "mediana": (st.median(hBm) if hBm else None)}, "pasa": bool(hAm and hBm and st.median(hAm) < st.median(hBm))}
# ── E7: el cuanto ──
e7 = {}
for s in (1, 2):
    for sl in (10, 11):
        d20 = next((v for v in vidas("APRENDE", s, sl) if v["dia"] == 20), None); cre = (d20["al_acabar"]["botiquin"]["creencia"].get("dentro") if d20 else None)
        e7[f"s{s}_{sl}"] = {"creencia_dentro_dia_20": cre, "llega_a_35": bool(cre is not None and cre >= 35.0)}
R["E7"] = {"criaturas": e7, "llegan_a_35": sum(1 for x in e7.values() if x["llega_a_35"])}; R["E7"]["pasa"] = R["E7"]["llegan_a_35"] >= 3
# ── E8: no se hunde (APRENDE - BORRADO, dias 16-20 frente a dias 1-5; excluyendo las partidas con corte, y tambien sin excluir) ──
def e8_de(excluir):
    ab_ = []; fuera = set(partidas_corte) | (MARCADAS if excluir == "marcadas" else set())
    for s in (1, 2):
        for d in range(1, 21):
            if excluir and ((s, d, "APRENDE") in fuera or (s, d, "BORRADO") in fuera): continue
            for sl in (10, 11):
                a = next((v for v in L if v["brazo"] == "APRENDE" and v["serie"] == s and v["dia"] == d and v["slot"] == sl), None); b = next((v for v in L if v["brazo"] == "BORRADO" and v["serie"] == s and v["dia"] == d and v["slot"] == sl), None)
                if a and b and a.get("puesto") is not None and b.get("puesto") is not None: ab_.append((d, a["puesto"] - b["puesto"]))
    p1 = resumen([x for d, x in ab_ if d <= 5]); p2 = resumen([x for d, x in ab_ if d >= 16])
    ee = ((p1["ee"] or 0) ** 2 + (p2["ee"] or 0) ** 2) ** 0.5 if (p1["ee"] is not None and p2["ee"] is not None) else None
    crece = (p2["media"] - p1["media"]) if (p1["media"] is not None and p2["media"] is not None) else None
    return {"dias 1-5": p1, "dias 16-20": p2, "crece": (round(crece, 3) if crece is not None else None), "ee_de_la_diferencia": (round(ee, 3) if ee is not None else None), "pasa": bool(crece is not None and ee is not None and crece <= 2 * ee)}
R["E8"] = e8_de(True); R["E8_sin_excluir"] = e8_de(False); R["E8_sin_marcadas"] = e8_de("marcadas")
# ── las medidas por dia, brazo y criatura (para las figuras y el informe) ──
R["por_vida"] = {k: {kk: v.get(kk) for kk in ("brazo", "serie", "dia", "slot", "tics", "puesto", "causa", "murio", "vida_al_morir", "primer_contacto", "primer_firme", "coge", "esperanza_aparece", "pedidos_abre", "regalos", "ir_curioso_tics", "ir_curioso_con_paso_listo", "tics_con_paso_listo", "parcial")} | {"usos": {o: {"n": len(u), "firmes": sum(1 for x in u if x["firme"]), "al_menos": sum(1 for x in u if x["al_menos"]), "cortes": sum(1 for x in u if not x["completado"]), "hp": [x["hp0"] for x in u]} for o, u in v["usos"].items()}, "creencia": {o: v["al_acabar"][o]["creencia"] for o in ("botiquin", "racion")}, "ignorancia": {o: v["al_acabar"][o]["ignorancia"] for o in ("botiquin", "racion")}, "ignorancia_cuanto": {o: v["al_acabar"][o]["ignorancia_cuanto"] for o in ("botiquin", "racion")}, "sabido_max": {o: v["al_acabar"][o]["sabido_max"] for o in ("botiquin", "racion")},
                       "cuenta_usos": v["cuenta_usos"], "aperturas_botiquin": v["aperturas_botiquin"], "latencia": {kk: v["latencia"][kk] for kk in ("ms_mediana", "ms_p95", "ms_max", "sobre_el_tic", "fraccion_sin_cuerpo", "pasa")}, "causas_de_corte": v["causas_de_corte"], "cuaderno_leido": v.get("cuaderno_leido")} for k, v in V.items() if not v.get("sin_diario")}
# la vida al abrir el botiquin cuando le pesa la curiosidad del cuanto (APRENDE, todos los dias), frente a las demas aperturas
apA = [a for v in vidas("APRENDE") for a in v["aperturas_botiquin"]]
R["cuanto_al_usar"] = {"aperturas": len(apA), "le_pesa": {"n": sum(1 for a in apA if a["le_pesa_el_cuanto"]), "vida_mediana": (st.median([a["hp"] for a in apA if a["le_pesa_el_cuanto"]]) if any(a["le_pesa_el_cuanto"] for a in apA) else None)}, "no_le_pesa_conocido": {"n": sum(1 for a in apA if a["conocido"] and not a["le_pesa_el_cuanto"]), "vida_mediana": (st.median([a["hp"] for a in apA if a["conocido"] and not a["le_pesa_el_cuanto"]]) if any(a["conocido"] and not a["le_pesa_el_cuanto"] for a in apA) else None)}, "sin_conocer": {"n": sum(1 for a in apA if not a["conocido"]), "vida_mediana": (st.median([a["hp"] for a in apA if not a["conocido"]]) if any(not a["conocido"] for a in apA) else None)}}
R["latencia_por_brazo"] = {b: {"vidas": len(vidas(b)), "ms_mediana_media": round(st.mean(v["latencia"]["ms_mediana"] for v in vidas(b) if v["latencia"]["ms_mediana"] is not None), 2), "ms_p95_max": max(v["latencia"]["ms_p95"] for v in vidas(b) if v["latencia"]["ms_p95"] is not None), "ms_max": max(v["latencia"]["ms_max"] for v in vidas(b) if v["latencia"]["ms_max"] is not None), "sobre_el_tic_media": round(st.mean(v["latencia"]["sobre_el_tic"] or 0 for v in vidas(b)), 4), "sin_cuerpo_media": round(st.mean(v["latencia"]["fraccion_sin_cuerpo"] for v in vidas(b)), 4), "no_pasan": sum(1 for v in vidas(b) if not v["latencia"]["pasa"])} for b in ("APRENDE", "BORRADO", "TECHO")}
# [P7-30, mesa punto 4] por vida: la fraccion de decisiones sobre el tic frente a su puesto y su muerte
def rangos(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k_ in range(i, j + 1): r[o[k_]] = (i + j) / 2
        i = j + 1
    return r
def spearman(x, y):
    if len(x) < 3: return None
    rx, ry = rangos(x), rangos(y); mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(num / den, 3) if den else None
R["lentas_vs_puesto"] = {}
for b in ("APRENDE", "BORRADO", "TECHO"):
    vs = [v for v in vidas(b) if v.get("puesto") is not None and (v["serie"], v["dia"], v["brazo"]) not in partidas_corte]
    x = [v["latencia"]["sobre_el_tic"] or 0.0 for v in vs]; y = [v["puesto"] for v in vs]; m_ = [1.0 if v["murio"] else 0.0 for v in vs]
    marc = [v for v in vs if not v["latencia"]["pasa"]]; resto = [v for v in vs if v["latencia"]["pasa"]]
    R["lentas_vs_puesto"][b] = {"vidas": len(vs), "spearman_sobre_el_tic_vs_puesto": spearman(x, y), "spearman_sobre_el_tic_vs_muere": spearman(x, m_),
                                "marcadas": {"n": len(marc), "puesto_medio": (round(st.mean(v["puesto"] for v in marc), 2) if marc else None), "mueren": sum(1 for v in marc if v["murio"]), "tic_muerte_mediana": (st.median([v["ultimo_tick"] for v in marc if v["murio"]]) if any(v["murio"] for v in marc) else None)},
                                "no_marcadas": {"n": len(resto), "puesto_medio": (round(st.mean(v["puesto"] for v in resto), 2) if resto else None), "mueren": sum(1 for v in resto if v["murio"]), "tic_muerte_mediana": (st.median([v["ultimo_tick"] for v in resto if v["murio"]]) if any(v["murio"] for v in resto) else None)},
                                "por_vida": sorted([{"serie": v["serie"], "dia": v["dia"], "asiento": v["slot"], "sobre_el_tic": v["latencia"]["sobre_el_tic"], "ms_mediana": v["latencia"]["ms_mediana"], "puesto": v["puesto"], "murio": v["murio"], "tic": v["ultimo_tick"]} for v in vs], key=lambda z: -(z["sobre_el_tic"] or 0))[:12]}
R["sello"] = {k: R[k]["pasa"] for k in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8")}
R["sello_sin_marcadas"] = {"E1": R["E1"]["pasa"], "E2": R["E2"]["pasa"], "E3": R["E3"]["pasa"], "E4": R["E4_sin_marcadas"]["pasa"], "E5": R["E5_sin_marcadas"]["pasa"], "E6": R["E6_sin_marcadas"]["pasa"], "E7": R["E7"]["pasa"], "E8": R["E8_sin_marcadas"]["pasa"]}
R["cambian_entre_las_dos_cuentas"] = [k for k in R["sello"] if R["sello"][k] != R["sello_sin_marcadas"][k]]
json.dump(R, open(os.path.join(AQUI, "P7_30_resumen.json"), "w"), ensure_ascii=False, indent=1)
print("partidas con corte", len(partidas_corte), partidas_corte); print("SELLO", R["sello"])
for k in ("E1", "E2", "E3", "E6"): print(k, {kk: vv for kk, vv in R[k].items() if kk != "criaturas"})
print("E4", R["E4"]); print("E5", R["E5"]); print("E4 sin excluir", R["E4_sin_excluir"]); print("E5 sin excluir", R["E5_sin_excluir"]); print("APRENDE - BORRADO", R["APRENDE - BORRADO"]); print("E7", {k: v for k, v in R["E7"].items() if k != "criaturas"}); print("E8", R["E8"]); print("E8 sin excluir", R["E8_sin_excluir"]); print("cuanto al usar", R["cuanto_al_usar"]); print("latencia", R["latencia_por_brazo"]); print("SELLO sin marcadas", R["sello_sin_marcadas"], "cambian:", R["cambian_entre_las_dos_cuentas"])

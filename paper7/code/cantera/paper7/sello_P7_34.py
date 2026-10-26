"""[P7-34] EL SELLO, evaluado UNA vez al acabar el campo, con las palabras de SELLO_P7_34.md (I1-I6), con dos cuentas: con todas las vidas (quitando solo las partidas con
corte de los puestos) y sin las partidas marcadas por la guarda de latencia. Lee P7_34_datos.json (analiza_P7_34.py) y P7_34_estado.json -> P7_34_sello.json.
  python3 sello_P7_34.py"""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
L = [v for v in json.load(open(os.path.join(AQUI, "P7_34_datos.json"))) if not v.get("sin_diario")]
ES = json.load(open(os.path.join(AQUI, "P7_34_estado.json"))) if os.path.exists(os.path.join(AQUI, "P7_34_estado.json")) else {}
CRIATURAS = [(s, sl) for s in (1, 2) for sl in (10, 11)]
partidas_corte = sorted({(v["serie"], v["dia"], v["brazo"]) for v in L if v.get("parcial")} | {(p["serie"], p["dia"], p["brazo"]) for p in ES.get("peticiones", []) if p.get("parcial")})      # con corte: diario parcial o asiento sin artefacto (estado del lanzador)
partidas_marcadas = sorted({(v["serie"], v["dia"], v["brazo"]) for v in L if not v["latencia"]["pasa"]})
MARCADAS = set(partidas_marcadas)


def vidas(brazo, serie=None, slot=None, dias=None, fuera=()):
    return [v for v in L if v["brazo"] == brazo and (serie is None or v["serie"] == serie) and (slot is None or v["asiento"] == slot) and (dias is None or v["dia"] in dias) and (v["serie"], v["dia"], v["brazo"]) not in fuera]


def pares(dias, fuera):
    """APRENDE - BORRADO en puesto, emparejado por serie, dia y asiento; media y error estandar."""
    d = []
    for s in (1, 2):
        for dia in dias:
            for sl in (10, 11):
                a = next((v for v in L if v["brazo"] == "APRENDE" and v["serie"] == s and v["dia"] == dia and v["asiento"] == sl), None); b = next((v for v in L if v["brazo"] == "BORRADO" and v["serie"] == s and v["dia"] == dia and v["asiento"] == sl), None)
                if not a or not b or a["puesto"] is None or b["puesto"] is None or (s, dia, "APRENDE") in fuera or (s, dia, "BORRADO") in fuera: continue
                d.append(a["puesto"] - b["puesto"])
    return {"n": len(d), "media": (round(st.mean(d), 3) if d else None), "ee": (round(st.stdev(d) / len(d) ** 0.5, 3) if len(d) > 1 else None)}


def evalua(fuera):
    R = {}
    # I1: al acabar el dia 5, cada criatura tiene >= 1 prueba de la red y >= 1 del camuflaje (huellas de los dias 1-5)
    i1 = {}
    for s, sl in CRIATURAS:
        vs = vidas("APRENDE", s, sl, range(1, 6), fuera); i1[f"s{s} a{sl}"] = {o: sum(v["pruebas"][o]["n"] for v in vs) for o in ("red", "camuflaje")}
    R["I1"] = {"pruebas_dias_1_5": i1, "pasa": all(x["red"] >= 1 and x["camuflaje"] >= 1 for x in i1.values())}
    # I2: dias 11-20, cogidas de red + camuflaje por vida de APRENDE <= 1/4 de las de TECHO y <= 1/4 de sus cogidas de botiquin + racion
    vA = vidas("APRENDE", dias=range(11, 21), fuera=fuera); vT = vidas("TECHO", dias=range(11, 21), fuera=fuera)
    inA = (st.mean(v["coge"]["red"] + v["coge"]["camuflaje"] for v in vA) if vA else None); inT = (st.mean(v["coge"]["red"] + v["coge"]["camuflaje"] for v in vT) if vT else None); utA = (st.mean(v["coge"]["botiquin"] + v["coge"]["racion"] for v in vA) if vA else None)
    R["I2"] = {"APRENDE_inutil_por_vida": (round(inA, 3) if inA is not None else None), "TECHO_inutil_por_vida": (round(inT, 3) if inT is not None else None), "APRENDE_util_por_vida": (round(utA, 3) if utA is not None else None), "n_APRENDE": len(vA), "n_TECHO": len(vT),
               "pasa": bool(inA is not None and inT is not None and utA is not None and inA <= 0.25 * inT and inA <= 0.25 * utA)}
    # I3: cuadernos del dia 20 de las 4: intensidad media de los recuerdos de red y camuflaje < 1/2 de la de botiquin y racion (sin cortes)
    iu = []; ii = []; det = {}
    for s, sl in CRIATURAS:
        v = next((v for v in vidas("APRENDE", s, sl, [20], fuera)), None)
        if not v: det[f"s{s} a{sl}"] = None; continue
        a = v["al_acabar"]; u = a["botiquin"]["intensidades"] + a["racion"]["intensidades"]; i_ = a["red"]["intensidades"] + a["camuflaje"]["intensidades"]; iu += u; ii += i_
        det[f"s{s} a{sl}"] = {"util": (round(st.mean(u), 4) if u else None), "n_util": len(u), "inutil": (round(st.mean(i_), 4) if i_ else None), "n_inutil": len(i_)}
    R["I3"] = {"por_criatura": det, "util_media": (round(st.mean(iu), 4) if iu else None), "inutil_media": (round(st.mean(ii), 4) if ii else None), "pasa": bool(iu and ii and st.mean(ii) < 0.5 * st.mean(iu))}
    # I4: en >= 2 de las 4 hay una prueba de red o camuflaje en un dia d sin contacto con esa cosa en d-5..d-1 (la del primer contacto de la criatura no cuenta)
    i4 = {}
    for s, sl in CRIATURAS:
        vs = {v["dia"]: v for v in vidas("APRENDE", s, sl, fuera=fuera)}; hechos = []
        for o in ("red", "camuflaje"):
            primero = min((d for d, v in vs.items() if v["contacto"][o] is not None), default=None)
            for d, v in sorted(vs.items()):
                if v["pruebas"][o]["n"] == 0 or d - 5 < 1 or primero is None or d <= primero: continue
                if all(dd in vs and vs[dd]["contacto"][o] is None for dd in range(d - 5, d)): hechos.append({"cosa": o, "dia": d, "pruebas": v["pruebas"][o]["n"]})
        i4[f"s{s} a{sl}"] = hechos
    R["I4"] = {"vueltas": i4, "criaturas_con_vuelta": sum(1 for h in i4.values() if h), "pasa": sum(1 for h in i4.values() if h) >= 2}
    # I5: creencia del botiquin dentro >= 30 el dia 20 en >= 3 de las 4; y dias 16-20 APRENDE - BORRADO no mayor que dias 1-5 por mas de 2 ee de la diferencia
    cre = {f"s{s} a{sl}": (next((v["al_acabar"]["botiquin"]["creencia_dentro"] for v in vidas("APRENDE", s, sl, [20], fuera)), None)) for s, sl in CRIATURAS}
    p1 = pares(range(1, 6), fuera); p2 = pares(range(16, 21), fuera)
    ee = ((p1["ee"] ** 2 + p2["ee"] ** 2) ** 0.5 if p1["ee"] is not None and p2["ee"] is not None else None)
    hunde = (p2["media"] - p1["media"] > 2 * ee) if (ee is not None and p1["media"] is not None and p2["media"] is not None) else None
    R["I5"] = {"creencia_botiquin_dia_20": cre, "llegan_a_30": sum(1 for c in cre.values() if c is not None and c >= 30), "APRENDE - BORRADO dias 1-5": p1, "APRENDE - BORRADO dias 16-20": p2, "ee_diferencia": (round(ee, 3) if ee is not None else None), "se_hunde": hunde,
               "pasa": bool(sum(1 for c in cre.values() if c is not None and c >= 30) >= 3 and hunde is False)}
    # I6: >= 80 % de las pruebas de red y camuflaje de APRENDE se abren en calma
    vA = vidas("APRENDE", fuera=fuera); n = sum(v["pruebas"][o]["aperturas"] for v in vA for o in ("red", "camuflaje")); calma = sum(v["pruebas"][o]["en_calma"] for v in vA for o in ("red", "camuflaje"))
    R["I6"] = {"aperturas": n, "en_calma": calma, "fraccion": (round(calma / n, 4) if n else None), "pasa": bool(n and calma / n >= 0.8)}
    R["sello"] = {k: R[k]["pasa"] for k in ("I1", "I2", "I3", "I4", "I5", "I6")}
    return R


R = {"partidas_con_corte": [list(x) for x in partidas_corte], "partidas_marcadas": [list(x) for x in partidas_marcadas], "vidas": len(L),
     "con_todas": evalua(set(partidas_corte)), "sin_marcadas": evalua(set(partidas_corte) | MARCADAS)}
R["cambian_entre_las_dos_cuentas"] = [k for k in R["con_todas"]["sello"] if R["con_todas"]["sello"][k] != R["sin_marcadas"]["sello"][k]]
# sin prediccion, solo medida: APRENDE - BORRADO y APRENDE - TECHO todos los dias
R["APRENDE - BORRADO todos los dias"] = pares(range(1, 21), set(partidas_corte))
json.dump(R, open(os.path.join(AQUI, "P7_34_sello.json"), "w"), ensure_ascii=False, indent=1)
print("vidas", len(L), "partidas con corte", partidas_corte, "marcadas", len(partidas_marcadas))
for cuenta in ("con_todas", "sin_marcadas"):
    print(cuenta, R[cuenta]["sello"])
    for k in ("I1", "I2", "I3", "I4", "I5", "I6"): print("  ", k, json.dumps({kk: vv for kk, vv in R[cuenta][k].items() if kk not in ("pruebas_dias_1_5", "por_criatura", "vueltas")}, ensure_ascii=False)[:400])
print("cambian", R["cambian_entre_las_dos_cuentas"])

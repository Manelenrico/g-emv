"""[P7-55] ¿CUANTO APRENDE CADA HERMANA DE LA OTRA? Sobre los cuadernos por dia de P7-50 (P7_50_res/cuaderno_s<S>_d<D>_<brazo>_<asiento>.json), coste cero.
  1. Fusion por evento: en cada cuaderno se quita la segunda copia de los "vistos" que llegaron tambien contados (misma hermana, mismo objeto, mismo dia de origen, |tic| <= 240).
  2. Por hermana de COMPARTE y dia: creencia (dentro, cuerpo; regla de CuadernoP29: sin cortes, neutro de peso 1, "al menos" solo si sube, OLVIDO 0,95 por dia) de los cuatro
     objetos (a) con todos los recuerdos deduplicados y (b) solo con los vividos. a - b = lo aprendido de la otra. Tambien (c) con todos SIN deduplicar (lo que el cuerpo creyo de verdad).
  3. Por hermana y serie: media de a - b por objeto (d1-20), fraccion de lo creido que viene de la otra (|a - b| / |a|, dias con a != 0), y "falso": dias en que lo recibido la llevo a
     creer algo falso (red o camuflaje: a > 5 con b <= 5; botiquin o racion: a <= 0 con b > 0).
  4. (b) de COMPARTE frente a las hermanas de SOLAS (todo vivido): area d1-20 y creencia al d20 del botiquin, y pruebas vividas por serie y hermana.
  python3 analiza_P7_55.py -> P7_55_datos.json"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(AQUI, "P7_50_res"); OLVIDO = 0.95; PESO_NEUTRO = 1.0; VENT = 240
OBJ = ("first_aid", "rations", "net", "camouflage"); NOM = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}; REAL = {"first_aid": 50.0, "rations": 15.0, "net": 0.0, "camouflage": 0.0}
SE = json.load(open(os.path.join(AQUI, "P7_50_sello.json")))["con_todas"]["vigilancia"]


def cuaderno(S, d, b, sl):
    f = os.path.join(RES, f"cuaderno_s{S}_d{d}_{b}_{sl}.json"); return json.load(open(f)) if os.path.exists(f) else None


def recuerdos(c):
    return [dict(r, _obj=o, _sit=s) for o, x in (c.get("objetos") or {}).items() for s, L in (x.get("situaciones") or {}).items() for r in L]


def dedup(recs):
    """quita los vistos que tienen un contado del mismo uso (mismo objeto, mismo dia de origen, |tic| <= 240)."""
    cont = [r for r in recs if r.get("origen") == "contado"]; out = []; quitados = 0
    for r in recs:
        if r.get("origen") == "visto" and any(q["_obj"] == r["_obj"] and int(q.get("dia_emisora") or -1) == int(r.get("dia") or -2) and abs(int(q.get("tick_emisora") or 0) - int(r.get("tick") or 0)) <= VENT for q in cont): quitados += 1; continue
        out.append(r)
    return out, quitados


def creencia(recs, obj, dia, filtro=None):
    rec = [r for r in recs if r["_obj"] == obj and r["_sit"] == "dentro" and not r.get("corte") and (filtro is None or filtro(r))]
    if not rec: return None
    num = 0.0; den = PESO_NEUTRO; techo = []
    for r in rec:
        w = float(r["intensidad"]) * (OLVIDO ** max(0, dia - int(r["dia"])))
        if r.get("al_menos"): techo.append((w, float(r["efecto"]["cuerpo"]))); continue
        num += w * float(r["efecto"]["cuerpo"]); den += w
    if techo:
        base = num / den if den > 0 else 0.0
        for w, e in techo:
            if e > base: num += w * e; den += w
    return num / den if den > 0 else None


R = {"por_hermana_serie": {}, "por_dia": {}, "falsos": [], "solas": {}, "quitados": 0}
for S in (1, 2, 3):
    for sl in (10, 11):
        h = "valiente" if sl == 10 else "prudente"; filas = []; falsos = []
        for d in range(1, 21):
            c = cuaderno(S, d, "COMPARTE", sl)
            if not c: continue
            recs = recuerdos(c); recs_d, q = dedup(recs); R["quitados"] += q; dia = d + 1
            fila = {"dia": d, "quitados_acumulados": q}
            for o in OBJ:
                a = creencia(recs_d, o, dia); b = creencia(recs_d, o, dia, lambda r: r.get("origen", "vivido") == "vivido"); c_ = creencia(recs, o, dia)
                fila[NOM[o]] = {"a_todos_dedup": a, "b_vividos": b, "c_todos_sin_dedup": c_, "n_vividos": sum(1 for r in recs_d if r["_obj"] == o and not r.get("corte") and r.get("origen", "vivido") == "vivido"), "n_recibidos": sum(1 for r in recs_d if r["_obj"] == o and not r.get("corte") and r.get("origen") in ("contado", "visto"))}
                a0 = a or 0.0; b0 = b or 0.0
                if (o in ("net", "camouflage") and a0 > 5.0 and b0 <= 5.0) or (o in ("first_aid", "rations") and a0 <= 0.0 and b0 > 0.0): falsos.append({"dia": d, "objeto": NOM[o], "a": round(a0, 2), "b": round(b0, 2)})
            filas.append(fila)
        R["por_dia"][f"s{S} a{sl}"] = filas
        res = {"hermana": h, "dias": len(filas)}
        for o in OBJ:
            nm = NOM[o]; dif = [((f[nm]["a_todos_dedup"] or 0.0) - (f[nm]["b_vividos"] or 0.0)) for f in filas]; fr = [abs(((f[nm]["a_todos_dedup"] or 0.0) - (f[nm]["b_vividos"] or 0.0))) / abs(f[nm]["a_todos_dedup"]) for f in filas if f[nm]["a_todos_dedup"]]
            res[nm] = {"a_d20": filas[-1][nm]["a_todos_dedup"] if filas else None, "b_d20": filas[-1][nm]["b_vividos"] if filas else None, "c_d20": filas[-1][nm]["c_todos_sin_dedup"] if filas else None, "dif_media": round(st.mean(dif), 3) if dif else None, "fraccion_de_la_otra": round(st.mean(fr), 3) if fr else None, "n_vividos_d20": filas[-1][nm]["n_vividos"] if filas else None, "n_recibidos_d20": filas[-1][nm]["n_recibidos"] if filas else None,
                       "area_a": round(sum((f[nm]["a_todos_dedup"] or 0.0) for f in filas), 1), "area_b": round(sum((f[nm]["b_vividos"] or 0.0) for f in filas), 1), "area_c": round(sum((f[nm]["c_todos_sin_dedup"] or 0.0) for f in filas), 1)}
        res["falsos"] = falsos; res["pruebas_vividas"] = SE[f"s{S} COMPARTE"]["pruebas_valiente" if sl == 10 else "pruebas_prudente"]
        R["por_hermana_serie"][f"s{S} a{sl}"] = res; R["falsos"] += [dict(x, serie=S, asiento=sl) for x in falsos]
        # SOLAS: la misma hermana, todo vivido
        filas_s = []
        for d in range(1, 21):
            c = cuaderno(S, d, "SOLAS", sl)
            if not c: continue
            recs = recuerdos(c); filas_s.append({"dia": d, **{NOM[o]: creencia(recs, o, d + 1) for o in OBJ}})
        R["solas"][f"s{S} a{sl}"] = {"hermana": h, **{NOM[o]: {"d20": filas_s[-1][NOM[o]] if filas_s else None, "area": round(sum((f[NOM[o]] or 0.0) for f in filas_s), 1)} for o in OBJ}, "pruebas_vividas": SE[f"s{S} SOLAS"]["pruebas_valiente" if sl == 10 else "pruebas_prudente"]}
json.dump(R, open(os.path.join(AQUI, "P7_55_datos.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R["por_hermana_serie"].items(): print(k, v["hermana"], {o: (v[o]["a_d20"] and round(v[o]["a_d20"], 1), v[o]["b_d20"] and round(v[o]["b_d20"], 1), v[o]["fraccion_de_la_otra"]) for o in NOM.values()}, "falsos", len(v["falsos"]), "pruebas", v["pruebas_vividas"], "solas b area", R["solas"][k]["botiquin"]["area"], "comparte b area", v["botiquin"]["area_b"])
print("vistos quitados (acumulados sobre los 120 cuadernos)", R["quitados"], "falsos", len(R["falsos"]))

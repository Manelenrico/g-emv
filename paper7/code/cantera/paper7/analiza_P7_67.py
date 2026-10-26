"""[P7-67, campo] GUION DE ANALISIS SELLADO (SELLO_P7_67.md; su md5 va en el sello). Lee P7_67F_estado.json y los diarios del campo (paintball/runs/P767F_*; el .art.log o, si no esta,
el .zip de la plataforma) y calcula P1, P2, P3, la robustez y lo descriptivo tal como los escribe el sello. Ninguna cifra a mano.
DEFINICIONES (las del sello):
  - criatura-dia: una hermana (asiento 10 u 11) en una partida completada (nivel, serie, dia, brazo).
  - OPORTUNIDAD: en ese dia, en algun tic vivo de los primeros 300 de la fase viva (el tramo), `ir_sitio` esta entre los candidatos del cuerpo (RADIOGRAFIA.candidatos). Antes de aceptar,
    invita_P7_67b solo lo ofrece en calma, en el tramo y con el destino a 8-15 de ella y de su hermana; despues de aceptar sigue ofrecido, pero aceptar ya exigio esa oferta: oportunidad
    = algun tic del tramo con `ir_sitio` ofrecido.
  - LLEGADA: ese dia hay un registro P7_66_llegada (llega al destino tras aceptar).
  - PAREJA = cadena (nivel, brazo, serie): las dos hermanas de esa serie. Fraccion de la pareja en un conjunto de dias = llegadas / oportunidades, sumando criatura-dias con oportunidad.
    A = dias 1-10, B = dias 11-20. Dia con oportunidad de la pareja = dia en que al menos una de las dos la tuvo. Entra si tiene >= 3 dias con oportunidad en A y >= 3 en B; si no,
    queda fuera y se cuenta.
  - P1: MIENTE (nivel 1), media de (B - A) por pareja < 0 a >= 3 errores estandar (sd / raiz(n), sd muestral).
  - P2: media(B - A) de MIENTE - media(B - A) de CONGELADA < 0 a >= 3 errores estandar (raiz(sd1^2/n1 + sd2^2/n2)).
  - P3 (enmienda 1 del sello): dias 1-5, fraccion por pareja con los brazos MIENTE y HONESTA de los niveles 1 (corazon, dias 1-5), 2, 3 y 14; regresion lineal por minimos cuadrados
    de la fraccion sobre ln(rivales activos) y una indicadora de brazo (HONESTA = 1), una fila por pareja; error estandar clasico de la pendiente de ln(rivales) (sigma^2 (X'X)^-1,
    sigma^2 = SSR / (n - 3)); pasa si esa pendiente < 0 a >= 3 errores estandar. Entra la pareja con >= 1 oportunidad en los dias 1-5.
  - P3b (enmienda 1): la misma regresion (con la indicadora de brazo), pero la variable de cada pareja es el numero medio de llegadas por dia en los dias 1-5 (llegadas de las dos
    hermanas ese dia, 0, 1 o 2; los dias sin oportunidad cuentan 0; la media sobre los dias 1-5 jugados). Entran todas las parejas con al menos una hermana viva al empezar el dia 1
    (= el dia 1 jugado). Por criatura: llegadas de la criatura por dia jugado.
  - Descriptivo (enmienda 1): fraccion de dias con oportunidad por nivel (criatura-dias de los dias 1-5 con oportunidad / criatura-dias), y por nivel y brazo.
  - Robustez: (i) sin las partidas marcadas por la guarda de latencia (una vida que no pasa marca la partida entera: fuera sus dos criaturas ese dia); (ii) la criatura como unidad
    (fracciones por criatura; entra con >= 3 dias con oportunidad propia en A y en B; en P3, con >= 1 oportunidad en los dias 1-5).
  - Descriptivo: HONESTA (B - A), la confianza dia a dia por brazo y dimension (la del arranque del dia, P7_54_arranque), las interrupciones por nivel y las muertes.
  python3 analiza_P7_67.py                      -> P7_67_analisis.json (el campo)
  python3 analiza_P7_67.py --prueba-bancos       -> P7_67_analisis_prueba_bancos.json (el banco de invita_P7_67b, tal cual: lo que no se puede calcular con 4 dias se dice)
  python3 analiza_P7_67.py --fontaneria          -> P7_67_analisis_fontaneria.json (PRUEBA DE FONTANERIA, no es un resultado: los dos bancos de P7-67 reetiquetados para pasar por todas
                                                    las ramas: A = dias 1-2, B = 3-4, >= 1 dia; HONESTA copiada como CONGELADA; el primer banco como nivel 2)"""
import glob, json, math, os, re, statistics as st, sys, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
EMPUJE = 300; HERMANAS = (10, 11); RIVALES = {"1": 1, "2": 2, "3": 3, "14": 14}; Z = 3.0
RX_TICK = re.compile(r'"tick":(\d+)')


def lineas(carpeta, slot):
    a = glob.glob(os.path.join(carpeta, f"*policy_agent_{slot}.art.log"))
    if a: yield from open(a[0], errors="replace"); return
    z = glob.glob(os.path.join(carpeta, f"*policy_agent_{slot}.zip"))
    if not z: raise FileNotFoundError(f"sin diario: {carpeta} asiento {slot}")
    with zipfile.ZipFile(z[0]) as Z_, Z_.open(Z_.namelist()[0]) as fh:
        for b in fh: yield b.decode(errors="replace")


def lee_dia(carpeta, slot):
    """-> oportunidad, aceptadas, llegadas (aciertos), interrumpidas, no_llego, confianza al arrancar y al cerrar, muerta"""
    tic0 = None; opo = False; r = {"aceptadas": 0, "llegadas": 0, "aciertos": 0, "interrumpidas": 0, "no_llego": 0, "conf_arranque": None, "conf_cierre": None, "muerta": False, "tic_oportunidad": None}
    for l in lineas(carpeta, slot):
        if l.startswith('{"k":"tick"'):
            if '"phase":"live"' not in l: continue
            t = int(RX_TICK.search(l).group(1))
            if tic0 is None: tic0 = t
            if not opo and t - tic0 < EMPUJE and '"ir_sitio"' in l:
                x = json.loads(l)
                if "ir_sitio" in ((x.get("RADIOGRAFIA") or {}).get("candidatos") or {}): opo = True; r["tic_oportunidad"] = t - tic0
            continue
        if not l.startswith('{"k":"'): continue
        k = l[6:l.index('"', 6)]
        if k == "P7_66_aceptada": r["aceptadas"] += 1
        elif k == "P7_66_llegada": r["llegadas"] += 1; r["aciertos"] += json.loads(l)["acierto_recursos"]
        elif k == "P7_66_interrumpida": r["interrumpidas"] += 1
        elif k == "P7_66_no_llego": r["no_llego"] += 1
        elif k == "P7_54_arranque": r["conf_arranque"] = json.loads(l).get("confianza")
        elif k == "P7_54_cierre": r["conf_cierre"] = json.loads(l).get("confianza")
        elif k == "final": r["muerta"] = json.loads(l).get("reason") == "eliminated"
    r["oportunidad"] = opo; r["llegada"] = r["llegadas"] > 0
    return r


def criatura_dias(fuentes):
    """fuentes: lista de (estado, carpeta_de(p), reetiqueta(p) -> lista de (nivel, serie, dia, brazo))"""
    CD = []
    for F, carpeta_de, etiqueta in fuentes:
        E = json.load(open(F))
        for p in E["peticiones"]:
            if p["estado"] != "completed": continue
            marcada = any(not g.get("pasa", True) for g in (p.get("latencia") or {}).values())
            car = carpeta_de(p)
            for sl in HERMANAS:
                r = lee_dia(car, sl)
                for (n, s, d, b) in etiqueta(p): CD.append(dict(r, nivel=n, serie=s, dia=d, brazo=b, slot=sl, marcada=marcada))
    return CD


def frac(cds):
    o = [c for c in cds if c["oportunidad"]]; return (sum(c["llegada"] for c in o) / len(o)) if o else None


def unidades(CD, nivel, brazo, dias_A, dias_B, min_dias, por_criatura=False):
    U = {}
    for c in CD:
        if c["nivel"] == nivel and c["brazo"] == brazo: U.setdefault((c["serie"], c["slot"]) if por_criatura else c["serie"], []).append(c)
    dentro, fuera = {}, []
    for u, cs in sorted(U.items()):
        a = [c for c in cs if c["dia"] in dias_A]; bb = [c for c in cs if c["dia"] in dias_B]
        dA = {c["dia"] for c in a if c["oportunidad"]}; dB = {c["dia"] for c in bb if c["oportunidad"]}
        if len(dA) >= min_dias and len(dB) >= min_dias: dentro[str(u)] = {"A": frac(a), "B": frac(bb), "B_menos_A": frac(bb) - frac(a), "dias_con_oportunidad_A": len(dA), "dias_con_oportunidad_B": len(dB)}
        else: fuera.append({"unidad": str(u), "dias_con_oportunidad_A": len(dA), "dias_con_oportunidad_B": len(dB)})
    return dentro, fuera


def media_ee(xs):
    if len(xs) < 2: return {"n": len(xs), "media": (xs[0] if xs else None), "sd": None, "ee": None}
    m = st.mean(xs); sd = st.stdev(xs); return {"n": len(xs), "media": m, "sd": sd, "ee": sd / math.sqrt(len(xs))}


def veredicto(est, ee):
    if est is None or ee is None: return {"veredicto": "NO CALCULABLE", "z": None}
    if ee == 0: return {"veredicto": "PASA" if est < 0 else "NO PASA", "z": None, "nota": "error estandar 0"}
    z = est / ee; return {"veredicto": "PASA" if (est < 0 and z <= -Z) else "NO PASA", "z": z}


def mco(filas):
    """minimos cuadrados con constante, ln(rivales) e indicadora de brazo -> (pendiente de ln(rivales), su error estandar clasico) o (None, None)"""
    X = [[1.0, r["x"], r["brazo_h"]] for r in filas]; y = [r["y"] for r in filas]; n, k = len(X), 3
    if n <= k or len({r["x"] for r in filas}) < 2 or len({r["brazo_h"] for r in filas}) < 2: return None, None
    A = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] + [1.0 if a == b else 0.0 for b in range(k)] for a in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(A[r][c]))
        if abs(A[p][c]) < 1e-12: return None, None
        A[c], A[p] = A[p], A[c]; v = A[c][c]; A[c] = [x / v for x in A[c]]
        for r in range(k):
            if r != c: f = A[r][c]; A[r] = [x - f * yv for x, yv in zip(A[r], A[c])]
    inv = [row[k:] for row in A]; Xy = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]; beta = [sum(inv[a][b] * Xy[b] for b in range(k)) for a in range(k)]
    ssr = sum((y[i] - sum(beta[a] * X[i][a] for a in range(k))) ** 2 for i in range(n)); s2 = ssr / (n - k)
    return beta[1], math.sqrt(s2 * inv[1][1]) if s2 * inv[1][1] > 0 else 0.0


def p3b(CD, dias, por_criatura=False, brazos=("MIENTE", "HONESTA")):
    filas = []
    for n in RIVALES:
        U = {}
        for c in CD:
            if c["nivel"] == n and c["brazo"] in brazos and c["dia"] in dias: U.setdefault((c["brazo"], c["serie"]) + ((c["slot"],) if por_criatura else ()), []).append(c)
        for u, cs in sorted(U.items()):
            jugados = sorted({c["dia"] for c in cs})
            if 1 not in jugados: continue
            filas.append({"nivel": n, "unidad": str(u), "x": math.log(RIVALES[n]), "brazo_h": 1.0 if u[0] == "HONESTA" else 0.0, "y": sum(c["llegada"] for c in cs) / len(jugados), "dias_jugados": len(jugados)})
    niveles = sorted({r["nivel"] for r in filas}, key=int); b, ee = mco(filas)
    return dict({"filas": len(filas), "niveles_con_datos": niveles, "por_nivel": {n: media_ee([r["y"] for r in filas if r["nivel"] == n]) for n in niveles}, "pendiente_ln_rivales": b, "ee": ee}, **veredicto(b, ee))


def p3(CD, dias, por_criatura=False, brazos=("MIENTE", "HONESTA")):
    filas = []; fuera = 0
    for n in RIVALES:
        U = {}
        for c in CD:
            if c["nivel"] == n and c["brazo"] in brazos and c["dia"] in dias: U.setdefault((c["brazo"], c["serie"]) + ((c["slot"],) if por_criatura else ()), []).append(c)
        for u, cs in sorted(U.items()):
            f = frac(cs)
            if f is None: fuera += 1; continue
            filas.append({"nivel": n, "unidad": str(u), "x": math.log(RIVALES[n]), "brazo_h": 1.0 if u[0] == "HONESTA" else 0.0, "y": f})
    niveles = sorted({r["nivel"] for r in filas}, key=int); b, ee = mco(filas)
    res = {"filas": len(filas), "fuera_sin_oportunidad": fuera, "niveles_con_datos": niveles, "por_nivel": {n: media_ee([r["y"] for r in filas if r["nivel"] == n]) for n in niveles}}
    return dict(res, pendiente=b, ee=ee, **veredicto(b, ee))


def todo(CD, dias_A, dias_B, min_dias, dias_P3):
    out = {}
    for etiqueta, cd, pc in (("principal", CD, False), ("robustez_sin_marcadas", [c for c in CD if not c["marcada"]], False), ("robustez_por_criatura", CD, True)):
        R = {}
        Um, fm = unidades(cd, "1", "MIENTE", dias_A, dias_B, min_dias, pc); Uc, fc = unidades(cd, "1", "CONGELADA", dias_A, dias_B, min_dias, pc); Uh, fh = unidades(cd, "1", "HONESTA", dias_A, dias_B, min_dias, pc)
        m = media_ee([u["B_menos_A"] for u in Um.values()]); c = media_ee([u["B_menos_A"] for u in Uc.values()])
        R["P1"] = dict(m, **veredicto(m["media"], m["ee"]), dentro=len(Um), fuera=len(fm), detalle_fuera=fm, unidades=Um)
        dif = None if (m["media"] is None or c["media"] is None) else m["media"] - c["media"]
        ee2 = None if (m["ee"] is None or c["ee"] is None) else math.sqrt(m["sd"] ** 2 / m["n"] + c["sd"] ** 2 / c["n"])
        R["P2"] = dict({"MIENTE": m, "CONGELADA": c, "diferencia": dif, "ee": ee2}, **veredicto(dif, ee2), dentro_CONGELADA=len(Uc), fuera_CONGELADA=len(fc), unidades_CONGELADA=Uc)
        R["P3"] = p3(cd, dias_P3, pc); R["P3b"] = p3b(cd, dias_P3, pc)
        R["descriptivo_HONESTA"] = dict(media_ee([u["B_menos_A"] for u in Uh.values()]), dentro=len(Uh), fuera=len(fh))
        out[etiqueta] = R
    # descriptivo
    conf = {}
    for c in CD:
        if c["nivel"] == "1" and c["conf_arranque"]:
            for dim, v in c["conf_arranque"].items(): conf.setdefault(c["brazo"], {}).setdefault(dim, {}).setdefault(c["dia"], []).append(v)
    out["confianza_dia_a_dia"] = {b: {dim: {d: round(st.mean(v), 4) for d, v in sorted(D_.items())} for dim, D_ in X.items()} for b, X in conf.items()}
    inte = {}
    for c in CD:
        if c["dia"] in dias_P3: x = inte.setdefault(c["nivel"], {"criatura_dias": 0, "oportunidades": 0, "aceptadas": 0, "interrumpidas": 0, "llegadas": 0}); x["criatura_dias"] += 1; x["oportunidades"] += c["oportunidad"]; x["aceptadas"] += c["aceptadas"]; x["interrumpidas"] += c["interrumpidas"]; x["llegadas"] += c["llegadas"]
    out["interrupciones_por_nivel_dias_P3"] = inte
    fo = {}
    for c in CD:
        if c["dia"] in dias_P3:
            for k in (c["nivel"], f"{c['nivel']}_{c['brazo']}"): x = fo.setdefault(k, [0, 0]); x[0] += c["oportunidad"]; x[1] += 1
    out["fraccion_dias_con_oportunidad_dias_P3"] = {k: {"con_oportunidad": a, "criatura_dias": b, "fraccion": a / b} for k, (a, b) in sorted(fo.items())}
    mu = {}
    for c in CD: x = mu.setdefault(f"n{c['nivel']}_{c['brazo']}", {"criatura_dias": 0, "muertas": 0}); x["criatura_dias"] += 1; x["muertas"] += c["muerta"]
    out["muertes"] = mu
    out["anomalias_llegada_sin_oportunidad"] = sum(1 for c in CD if c["llegada"] and not c["oportunidad"])
    out["criatura_dias"] = len(CD); out["marcadas"] = sum(1 for c in CD if c["marcada"]) // 2
    return out


def campo():
    car = lambda p: glob.glob(os.path.join(RUNS, f"P767F_n{p['nivel']}_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}"))[0]
    return criatura_dias([(os.path.join(AQUI, "P7_67F_estado.json"), car, lambda p: [(p["nivel"], p["serie"], p["dia"], p["brazo"])])])


def bancos(fontaneria):
    c2 = lambda p: glob.glob(os.path.join(RUNS, f"P767b_d{p['dia']}_{p['brazo']}_{p['semilla']}"))[0]
    c1 = lambda p: glob.glob(os.path.join(RUNS, f"P767_d{p['dia']}_{p['brazo']}_{p['semilla']}"))[0]
    if not fontaneria: return criatura_dias([(os.path.join(AQUI, "P7_67b_estado.json"), c2, lambda p: [("1", 1, p["dia"], p["brazo"])])])
    e2 = lambda p: [("1", 1, p["dia"], p["brazo"])] + ([("1", 1, p["dia"], "CONGELADA")] if p["brazo"] == "HONESTA" else [])
    e1 = lambda p: [("1", 2, p["dia"], p["brazo"]), ("2", 1, p["dia"], p["brazo"])] + ([("1", 2, p["dia"], "CONGELADA")] if p["brazo"] == "HONESTA" else [])
    return criatura_dias([(os.path.join(AQUI, "P7_67b_estado.json"), c2, e2), (os.path.join(AQUI, "P7_67_estado.json"), c1, e1)])


if __name__ == "__main__":
    a = sys.argv
    if "--prueba-bancos" in a: CD = bancos(False); R = todo(CD, set(range(1, 11)), set(range(11, 21)), 3, set(range(1, 6))); sal = "P7_67_analisis_prueba_bancos.json"
    elif "--fontaneria" in a: CD = bancos(True); R = todo(CD, {1, 2}, {3, 4}, 1, {1, 2, 3, 4, 5}); R["AVISO"] = "PRUEBA DE FONTANERIA: datos reetiquetados, no es un resultado"; sal = "P7_67_analisis_fontaneria.json"
    else: CD = campo(); R = todo(CD, set(range(1, 11)), set(range(11, 21)), 3, set(range(1, 6))); sal = "P7_67_analisis.json"
    R["criatura_dias_detalle"] = [{k: v for k, v in c.items() if k not in ("conf_cierre",)} for c in CD]
    json.dump(R, open(os.path.join(AQUI, sal), "w"), ensure_ascii=False, indent=1, default=str)
    for k in ("principal", "robustez_sin_marcadas", "robustez_por_criatura"):
        r = R[k]; print(k, "| P1", r["P1"]["veredicto"], r["P1"].get("media"), r["P1"].get("ee"), f"dentro {r['P1']['dentro']} fuera {r['P1']['fuera']}", "| P2", r["P2"]["veredicto"], r["P2"].get("diferencia"), r["P2"].get("ee"),
                         "| P3", r["P3"]["veredicto"], r["P3"].get("pendiente"), r["P3"].get("ee"), f"filas {r['P3']['filas']} niveles {r['P3']['niveles_con_datos']}", "| P3b", r["P3b"]["veredicto"], r["P3b"].get("pendiente_ln_rivales"), r["P3b"].get("ee"), f"filas {r['P3b']['filas']}")
    print("criatura-dias", R["criatura_dias"], "marcadas", R["marcadas"], "anomalias", R["anomalias_llegada_sin_oportunidad"], "->", sal)

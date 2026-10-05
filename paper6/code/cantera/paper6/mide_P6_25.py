"""[P6-25 · 2-5] LAS MEDIDAS: junta escenas, planes, juicios y gasto, y calcula lo que pide el encargo.
  2 · por modelo (oraculo, haiku, sonnet): cuantos planes acepta puerta6, la ganancia imaginada (ventaja),
      si el destino queda dentro del circulo al que va la fase (P6-21), los que no se pueden traducir, el
      tiempo de respuesta y el coste por llamada; emparejado por escena con el oraculo (tabla 2x2, McNemar exacto);
  3 · el retraso: los mismos planes juzgados con la instantanea de t+D (D = el retraso medido de esa llamada);
  4 · el bucle: la tasa de la 1a, 2a y 3a propuesta en las mismas escenas;
  5 · la pareja: coinciden en la zona (Chebyshev <= 3), lo aceptan las dos puertas, y el mensaje (<= 120, ASCII,
      y si cabe junto al E2 de ese instante en los 120 del canal).
Intervalos de Wilson al 95 %. SOLO LECTURA de los JSON de P6-25.
    python3 mide_P6_25.py    -> P6_25_medidas.json
"""
import collections, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
C = (24, 24)


def J(n):
    p = os.path.join(AQUI, n)
    return json.load(open(p)) if os.path.exists(p) else None


def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round(100 * (c - r) / d, 1), round(100 * (c + r) / d, 1)]


def pct(k, n):
    return {"k": k, "n": n, "pct": (round(100 * k / n, 1) if n else None), "ic95": wilson(k, n)}


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 4) if xs else None


def q(xs, p):
    xs = sorted(x for x in xs if x is not None)
    return round(xs[min(len(xs) - 1, int(p * len(xs)))], 4) if xs else None


def mcnemar(b, c):
    """Exacto (binomial) sobre los discordantes b (solo A) y c (solo B)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return round(min(1.0, 2 * sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n), 4)


E = J("P6_25_escenas.json"); G = J("P6_25_gasto.json") or {}
esc = {f"{e['carp']}_{e['slot']}_{e['tick']}": e for e in E["escenas"]}
propias = [k for k, e in esc.items() if e["propia"]]
OUT = {"nota": __doc__.split("\n")[0], "escenas": {"n": len(propias), "pareja": E["n_pareja"], "vidas": len(E["vidas"]), "repro": {"igual": sum(v["repro"].get("igual", 0) for v in E["vidas"]), "difiere": sum(v["repro"].get("difiere", 0) for v in E["vidas"])},
                                                    "largo_texto": {"mediana": mediana([len(esc[k]["texto"]) for k in propias]), "max": max(len(esc[k]["texto"]) for k in propias)}}}

# ── 2 · el primer plan, por modelo ──
JO = {j["id"]: j for j in (J("P6_25_juicios_oraculo.json") or {"juicios": []})["juicios"]}
PP = (J("P6_25_planes_primera.json") or {"planes": []})["planes"]; JP = (J("P6_25_juicios_primera.json") or {"juicios": []})["juicios"]
planes = {(p["id"], p["modelo"]): p for p in PP}; juicios = {(j["id"], j["modelo"]): j for j in JP}
modelos = sorted({p["modelo"] for p in PP})
res2 = {}
camp = {f"{c['carp']}_{c['slot']}_{c['tick']}": c for c in E["elegidas"]}
# el oraculo
jo = [JO[k] for k in propias if k in JO]
res2["oraculo"] = {"planes": len(jo), "acepta": pct(sum(1 for j in jo if j.get("veredicto") == "ok"), len(jo)), "veredictos": dict(collections.Counter(j.get("veredicto") for j in jo)),
                   "ventaja_aceptados_mediana": mediana([j["ventaja"] for j in jo if j.get("veredicto") == "ok"]), "ventaja_todos_mediana": mediana([j.get("ventaja") for j in jo if j.get("veredicto")]),
                   "dentro_futuro": pct(sum(1 for j in jo if j.get("dentro_futuro")), sum(1 for j in jo if j.get("dentro_futuro") is not None)), "a_salvo": pct(sum(1 for j in jo if j.get("a_salvo")), len(jo)),
                   "ms_juicio_mediana": mediana([j.get("ms") for j in jo]),
                   "campo_vs_banco": dict(collections.Counter(f"{camp.get(j['id'], {}).get('veredicto_campo')}->{j.get('veredicto')}" for j in jo)),
                   "campo_igual": pct(sum(1 for j in jo if camp.get(j["id"], {}).get("veredicto_campo") == j.get("veredicto")), sum(1 for j in jo if camp.get(j["id"], {}).get("veredicto_campo")))}
for m in modelos:
    ps = [planes[(k, m)] for k in propias if (k, m) in planes]; js = [juicios[(k, m)] for k in propias if (k, m) in juicios]
    con_plan = [p for p in ps if p.get("tramos")]
    ok = [j for j in js if j.get("veredicto") == "ok"]
    a = sum(1 for k in propias if JO.get(k, {}).get("veredicto") == "ok" and juicios.get((k, m), {}).get("veredicto") == "ok")
    b = sum(1 for k in propias if JO.get(k, {}).get("veredicto") == "ok" and juicios.get((k, m), {}).get("veredicto") != "ok")
    c = sum(1 for k in propias if JO.get(k, {}).get("veredicto") != "ok" and juicios.get((k, m), {}).get("veredicto") == "ok")
    d = len(propias) - a - b - c
    res2[m] = {"llamadas": len(ps), "errores_api": sum(1 for p in ps if p.get("error")), "no_parsea": sum(1 for p in ps if p.get("texto") is not False and not p.get("parsea") and not p.get("error")),
               "callar": sum(1 for p in ps if p.get("callar")), "intraducibles": pct(sum(1 for p in ps if p.get("intraducible")), sum(1 for p in ps if p.get("parsea"))), "con_plan": len(con_plan),
               "formas_dichas_media": round(st.mean([p.get("n_formas_dichas") or 0 for p in ps]), 2) if ps else None, "tramos_media": round(st.mean([len(p["tramos"]) for p in con_plan]), 2) if con_plan else None,
               "acepta_sobre_escenas": pct(len(ok), len(propias)), "acepta_sobre_planes": pct(len(ok), sum(1 for j in js if j.get("veredicto"))), "veredictos": dict(collections.Counter(j.get("veredicto") for j in js)),
               "ventaja_aceptados_mediana": mediana([j["ventaja"] for j in ok]), "ventaja_todos_mediana": mediana([j.get("ventaja") for j in js if j.get("veredicto")]),
               "dentro_futuro": pct(sum(1 for j in js if j.get("dentro_futuro")), sum(1 for j in js if j.get("dentro_futuro") is not None)), "a_salvo": pct(sum(1 for j in js if j.get("a_salvo")), sum(1 for j in js if j.get("veredicto"))),
               "ms_mediana": mediana([p.get("ms") for p in ps if not p.get("error")]), "ms_p90": q([p.get("ms") for p in ps if not p.get("error")], 0.9), "usd_por_llamada": (round(st.mean([p["usd"] for p in ps if p.get("usd") is not None]), 5) if ps else None),
               "usd_por_llamada_api": (G.get("modos") or G.get("por_brazo") or {}).get(f"primera/{m}", {}).get("usd_por_llamada"),
               "vs_oraculo_2x2": {"los_dos_ok": a, "solo_oraculo": b, "solo_razonador": c, "ninguno": d, "mcnemar_p": mcnemar(b, c)},
               "contra_mas_frecuente": dict(collections.Counter(j["contra"][0][0] for j in js if j.get("veredicto") in ("area", "vida") and j.get("contra")).most_common(6)),
               "por_dicho": dict(collections.Counter(mi.get("por") for p in con_plan for mi in (p.get("mitades") or [])).most_common(8))}
OUT["2_primer_plan"] = res2

# ── 3 · el retraso ──
res3 = {}
for m in modelos:
    JR = (J("P6_25_juicios_retraso_primera.json") or {"juicios": []})["juicios"]
    jr = {j["id"]: j for j in JR if j.get("modelo") == m}
    if not jr:
        continue
    con = [k for k in propias if k in jr and jr[k].get("veredicto")]
    sin = collections.Counter(jr[k].get("motivo") for k in propias if k in jr and not jr[k].get("veredicto"))
    ok_t = [k for k in con if juicios.get((k, m), {}).get("veredicto") == "ok"]
    res3[m] = {"retrasos_usados": dict(collections.Counter(jr[k].get("retraso") for k in con)), "juzgados_en_t_mas_D": len(con), "sin_instantanea": dict(sin),
               "ok_en_t_y_en_t_mas_D": pct(sum(1 for k in ok_t if jr[k]["veredicto"] == "ok"), len(ok_t)), "ok_en_t_mas_D_sobre_todos": pct(sum(1 for k in con if jr[k]["veredicto"] == "ok"), len(con)),
               "ok_en_t_sobre_los_mismos": pct(len(ok_t), len(con)), "rechazado_en_t_ok_en_t_mas_D": pct(sum(1 for k in con if k not in ok_t and jr[k]["veredicto"] == "ok"), len(con) - len(ok_t)),
               "ventaja_en_t_mas_D_de_los_ok_en_t_mediana": mediana([jr[k].get("ventaja") for k in ok_t])}
OUT["3_retraso"] = res3

# ── 4 · el bucle ──
res4 = {}
for m in modelos:
    P2 = (J("P6_25_planes_bucle2.json") or {"planes": []})["planes"]; J2 = {j["id"]: j for j in (J("P6_25_juicios_bucle2.json") or {"juicios": []})["juicios"] if j.get("modelo") == m}
    P3 = (J("P6_25_planes_bucle3.json") or {"planes": []})["planes"]; J3 = {j["id"]: j for j in (J("P6_25_juicios_bucle3.json") or {"juicios": []})["juicios"] if j.get("modelo") == m}
    ids2 = [p["id"] for p in P2 if p["modelo"] == m]; ids3 = [p["id"] for p in P3 if p["modelo"] == m]
    if not ids2:
        continue
    import razonador_P6_25 as RZ
    N = RZ.N_BUCLE
    sub = propias[:N]
    r1 = pct(sum(1 for k in sub if juicios.get((k, m), {}).get("veredicto") == "ok"), sum(1 for k in sub if juicios.get((k, m), {}).get("veredicto")))
    r2 = pct(sum(1 for k in ids2 if J2.get(k, {}).get("veredicto") == "ok"), sum(1 for k in ids2 if J2.get(k, {}).get("veredicto")))
    r3 = pct(sum(1 for k in ids3 if J3.get(k, {}).get("veredicto") == "ok"), sum(1 for k in ids3 if J3.get(k, {}).get("veredicto")))
    acum = {"1": sum(1 for k in sub if juicios.get((k, m), {}).get("veredicto") == "ok")}
    acum["1-2"] = acum["1"] + sum(1 for k in ids2 if J2.get(k, {}).get("veredicto") == "ok"); acum["1-3"] = acum["1-2"] + sum(1 for k in ids3 if J3.get(k, {}).get("veredicto") == "ok")
    res4[m] = {"escenas_del_bucle": len(sub), "primera": r1, "segunda (a los rechazados de la primera)": r2, "tercera (a los rechazados de la segunda)": r3,
               "escenas_con_algun_plan_aceptado_acumulado": {k: pct(v, len(sub)) for k, v in acum.items()},
               "sin_plan_2a": sum(1 for k in ids2 if not J2.get(k, {}).get("veredicto")), "sin_plan_3a": sum(1 for k in ids3 if not J3.get(k, {}).get("veredicto")),
               "cambia_destino_2a": pct(sum(1 for p in P2 if p["modelo"] == m and p.get("tramos") and p.get("previo") and [t.get("destino") for t in p["tramos"] if t.get("destino")][:1] != [t.get("destino") for t in p["previo"] if t.get("destino")][:1]), sum(1 for p in P2 if p["modelo"] == m and p.get("tramos"))),
               "ventaja_2a_mediana": mediana([J2[k].get("ventaja") for k in ids2 if J2.get(k, {}).get("veredicto")]), "ventaja_1a_mediana_mismas": mediana([juicios.get((k, m), {}).get("ventaja") for k in ids2 if juicios.get((k, m), {}).get("veredicto")])}
OUT["4_bucle"] = res4

# ── 5 · la pareja ──
res5 = {}
PR = (J("P6_25_planes_pareja.json") or {"planes": []})["planes"]; JR = {(j["id"], j["modelo"]): j for j in (J("P6_25_juicios_pareja.json") or {"juicios": []})["juicios"]}
for m in modelos:
    pares = collections.defaultdict(dict)
    for p in PR:
        if p["modelo"] == m:
            pares[p["par"]][p["id"]] = p
    if not pares:
        continue
    n = 0; zonas = 0; coinc = 0; dentro2 = 0; ok2 = 0; ok1 = 0; msgs = []; cabe = 0; cabe_e2 = 0; ascii_ = 0; con_msg = 0; dist = []
    for par, dd in pares.items():
        if len(dd) != 2:
            continue
        n += 1
        (ka, pa), (kb, pb) = list(dd.items())
        za, zb = pa.get("zona"), pb.get("zona")
        if isinstance(za, list) and isinstance(zb, list) and len(za) == 2 and len(zb) == 2:
            zonas += 1; ch = max(abs(za[0] - zb[0]), abs(za[1] - zb[1])); dist.append(ch); coinc += (ch <= 3)
            e = esc.get(ka); fases = E["fases"].get(e["carp"]) if e else None
            if fases:
                i = max((k for k, f in enumerate(fases) if e["tick"] >= f[0]), default=None); r1 = fases[i][4] if i is not None else None
                if r1 is not None and math.dist(za, C) <= r1 and math.dist(zb, C) <= r1:
                    dentro2 += 1
        va, vb = JR.get((ka, m), {}).get("veredicto"), JR.get((kb, m), {}).get("veredicto")
        ok2 += (va == "ok" and vb == "ok"); ok1 += (va == "ok" or vb == "ok")
        for k, p in ((ka, pa), (kb, pb)):
            msg = p.get("mensaje")
            if isinstance(msg, str) and msg:
                con_msg += 1; msgs.append(len(msg)); cabe += (len(msg) <= 120); ascii_ += all(0x20 <= ord(ch) <= 0x7E for ch in msg)
                e2 = (esc.get(k) or {}).get("ult_e2") or ""
                cabe_e2 += (len(e2) + 1 + len(msg) <= 120)
    res5[m] = {"pares": n, "con_zona_los_dos": zonas, "coinciden_zona (Chebyshev <= 3)": pct(coinc, zonas), "distancia_zonas_mediana": mediana(dist), "las_dos_zonas_dentro_del_circulo_futuro": pct(dentro2, zonas),
               "aceptan_las_dos_puertas": pct(ok2, n), "acepta_alguna": pct(ok1, n), "acepta_por_hermano": pct(sum(1 for (k, mm), j in JR.items() if mm == m and j.get("veredicto") == "ok"), sum(1 for (k, mm), j in JR.items() if mm == m and j.get("veredicto"))),
               "mensajes": {"n": con_msg, "largo_mediana": mediana(msgs), "largo_max": (max(msgs) if msgs else None), "caben_en_120": pct(cabe, con_msg), "ascii": pct(ascii_, con_msg), "caben_junto_al_E2_en_120": pct(cabe_e2, con_msg)}}
OUT["5_pareja"] = res5
OUT["gasto"] = {"total_usd": G.get("total_usd"), "llamadas": G.get("llamadas"), "por_modo": {k: {"llamadas": v.get("llamadas"), "usd": v.get("usd"), "usd_por_llamada": v.get("usd_por_llamada")} for k, v in (G.get("modos") or G.get("por_brazo") or {}).items()}}
json.dump(OUT, open(os.path.join(AQUI, "P6_25_medidas.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(OUT, ensure_ascii=False)[:6000])

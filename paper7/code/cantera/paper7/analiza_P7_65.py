"""[P7-65] EL SELLO DEL CAMPO DE LA MENTIRA DEL BOTIQUIN COGIDO (SELLO_P7_65.md: sello 762814d, addendum 1 b7a60d6, registros d78dfa6, 90b5bfa, daae543, 5df39ba, 03c2c1d).
No hubo guion de analisis sellado: este sigue el texto del sello y las decisiones de la mesa apuntadas en su registro ANTES de calcular.
  Datos: P7_65_estado.json (peticiones completadas, sin los intentos apartados; `mentiras` con brazo, asiento y posicion), diarios P765_* (P7_54_activa / aceptada / evaluada,
  P7_huella, tics), cuadernos por dia P7_65_res (confianza_razon_P7_54), respuestas de la razon cuadernos_P7_65/<brazo>_serie<S>/razon_s<S>_d<d-1>_<asiento>.txt.
  Invitaciones de una vida = las honestas de la respuesta (razon_P7_57.parsea, en orden) + la falsa en su posicion (estado `mentiras`), comprobadas contra P7_54_arranque.
  PRINCIPALES (a 3 ee): L1 (media de las 9 medias por criatura de despues - antes en cuerpo, ee = sd/raiz(9); aparte, CR1 agrupado), L2 (d15-20 - d8-11 por criatura que miente,
  emparejado), L2b (dias 10-20 - dia 8, emparejado; y la curva por fallos previos), L4 (por serie, prudentes: verdaderas de coger aceptadas / cargadas, d12-20, MIENTEN_DOS - MIENTE_UNA,
  ee = raiz(ee_A^2 + ee_B^2) como en P7-56/P7-61). Segunda cuenta sin la partida marcada entera. SECUNDARIOS: S1 (juicio estricto, decision de la mesa sobre la subida), S2.
  DESCRIPTIVO: confianza por brazo, hermana, dimension y dia (+ grafica), agarre, dias de abandono (definicion de la mesa), L3 descriptivo, vigilancia sellada.
  python3 analiza_P7_65.py -> P7_65_sello.json, P7_65_confianza.png"""
import glob, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI)
import razon_P7_57 as RZ, mentira_P7_65 as MT
src = open(os.path.join(AQUI, "analiza_P7_56.py")).read(); ns = {}; exec(src[src.index("def verdad"):src.index("\n\n\ndef vida")], ns); verdad = ns["verdad"]
E = json.load(open(os.path.join(AQUI, "P7_65_estado.json"))); SERIES = (1, 2, 3); BRAZOS = ("MIENTEN_DOS", "MIENTE_UNA"); HERMANA = {10: "valiente", 11: "prudente"}
MARCADA = (2, 20, "MIENTE_UNA")          # la partida marcada: fuera en la segunda cuenta, las dos hermanas (decision de la mesa)
POS = {(m["serie"], m["dia_noche"] + 1, m["brazo"], m["slot"]): m["posicion"] for m in E["mentiras"]}
r4 = lambda x: (round(x, 4) if isinstance(x, (int, float)) else x)
COGER = ("COGER_BOTIQUIN", "COGER_RACION", "COGER_RED", "COGER_CAMUFLAJE")


def invitaciones(S, d, b, sl):
    f = os.path.join(AQUI, "cuadernos_P7_65", f"{b}_serie{S}", f"razon_s{S}_d{d - 1}_{sl}.txt")
    inv = [x for x in (RZ.parsea(l) for l in open(f).read().split("\n") if l.strip().startswith("INVITACION")) if x] if (d > 1 and os.path.exists(f)) else []
    pos = POS.get((S, d, b, sl))
    if pos is not None: inv.insert(pos, dict(MT.FALSA))
    return inv, pos


def vida(p, sl):
    S, d, b = p["serie"], p["dia"], p["brazo"]
    fs = glob.glob(os.path.join(RUNS, f"P765_s{S}_d{d}_{b}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))
    if not fs: return None
    T = {}; act = {}; acc = {}; ev = []; huellas = []; arr = None; fin = None; ult = 0; golpes = {}
    for l in open(fs[0], errors="replace"):
        if l.startswith('{"k":"tick"'):
            r = json.loads(l)
            if r.get("phase") != "live": continue
            t = r["tick"]; ult = t
            T[t] = (float(r.get("hp") or 0), sum(int(it.get("n") or 1) for it in (r.get("pack") or []) if isinstance(it, dict) and it.get("id") == "first_aid"))
            g = sum(float(x.get("amount") or 0) for x in (r.get("damage_taken") or []))
            if g > 0: golpes[t] = g
        elif l.startswith('{"k":"P7_54_activa"'):
            a = json.loads(l); act.setdefault(a["n"], a["tick"])
        elif l.startswith('{"k":"P7_54_aceptada"'):
            a = json.loads(l); acc.setdefault(a["n"], []).append(a["tick"])
        elif l.startswith('{"k":"P7_54_evaluada"'): ev.append(json.loads(l))
        elif l.startswith('{"k":"P7_huella"'):
            h = json.loads(l)
            if (h.get("objeto") or "first_aid") == "first_aid": huellas.append(int(h["t0"]))
        elif l.startswith('{"k":"P7_54_arranque"') and arr is None: arr = json.loads(l)
        elif l.startswith('{"k":"final"'): fin = json.loads(l)
    inv, pos = invitaciones(S, d, b, sl)
    cu = os.path.join(AQUI, "P7_65_res", f"cuaderno_s{S}_d{d}_{b}_{sl}.json")
    conf = (json.load(open(cu)).get("confianza_razon_P7_54") or {}) if os.path.exists(cu) else {}
    return {"inv": inv, "pos": pos, "n_arranque": (arr or {}).get("invitaciones"), "T": T, "act": act, "acc": acc, "ev": ev, "huellas": sorted(huellas), "golpes": golpes,
            "conf": conf, "puesto": (fin or {}).get("placement"), "murio": ult < 14000}


V = {}
for p in E["peticiones"]:
    if p["estado"] != "completed" or p["serie"] not in SERIES: continue
    for sl in (10, 11):
        v = vida(p, sl)
        if v: V[(p["serie"], p["dia"], p["brazo"], sl)] = v
CRIATURAS = [(S, b, sl) for S in SERIES for b, sl in (("MIENTEN_DOS", 10), ("MIENTEN_DOS", 11), ("MIENTE_UNA", 10))]


def fuera(k, sin_marcada): return sin_marcada and (k[0], k[1], k[2]) == MARCADA
def falsas(sin_marcada):
    out = []
    for k, v in V.items():
        if v["pos"] is None or fuera(k, sin_marcada): continue
        for e in v["ev"]:
            if e["n"] == v["pos"]: out.append((k, v, e))
    return out
def es_op(v): return v["pos"] is not None and v["pos"] in v["act"]
def aceptada(v): return bool(v["acc"].get(v["pos"]))
def frac_dias(S, b, sl, dias, sin_marcada):
    op = ac = 0
    for d in dias:
        k = (S, d, b, sl); v = V.get(k)
        if not v or fuera(k, sin_marcada) or not es_op(v): continue
        op += 1; ac += aceptada(v)
    return (ac / op if op else None), op


def media_ee(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 2: return {"n": len(xs), "media": r4(st.mean(xs)) if xs else None, "ee": None}
    m = st.mean(xs); e = st.stdev(xs) / math.sqrt(len(xs)); return {"n": len(xs), "media": r4(m), "ee": r4(e), "en_ee": r4(abs(m) / e) if e else None, "valores": [r4(x) for x in xs]}
def veredicto(r, menor=True):
    if r.get("ee") in (None, 0) or r.get("media") is None: return "NO PASA"
    ok = (r["media"] < 0) if menor else (r["media"] > 0)
    return "PASA" if ok and abs(r["media"]) >= 3 * r["ee"] else "NO PASA"


def principales(sin_marcada):
    R = {}
    # L1
    F = falsas(sin_marcada); por = {}
    for k, v, e in F: por.setdefault((k[0], k[2], k[3]), []).append(float(e["confianza_despues"]["cuerpo"]) - float(e["confianza_antes"]["cuerpo"]))
    medias = [st.mean(por[c]) for c in CRIATURAS if c in por]
    L1 = media_ee(medias); L1["veredicto"] = veredicto(L1)
    L1["criaturas"] = {f"s{c[0]} {c[1]} {HERMANA[c[2]]}": {"evaluaciones": len(por.get(c, [])), "media": r4(st.mean(por[c])) if c in por else None} for c in CRIATURAS}
    con3 = [c for c in CRIATURAS if len(por.get(c, [])) >= 3]; L1["criaturas_con_3_o_mas"] = len(con3); L1["de_ellas_caen"] = sum(1 for c in con3 if st.mean(por[c]) < 0)
    todas = [x for c in por for x in por[c]]; N = len(todas); m = st.mean(todas); G = len(por)
    cr1 = math.sqrt((G / (G - 1)) * sum(sum(x - m for x in por[c]) ** 2 for c in por)) / N if G > 1 else None
    L1["robustez_b_CR1"] = {"evaluaciones": N, "media": r4(m), "ee": r4(cr1), "en_ee": r4(abs(m) / cr1) if cr1 else None, "seria": ("PASA" if cr1 and m < 0 and abs(m) >= 3 * cr1 else "NO PASA")}
    L1["evaluaciones"] = N; R["L1"] = L1
    # L2
    filas = []
    for c in CRIATURAS:
        a, oa = frac_dias(c[0], c[1], c[2], range(8, 12), sin_marcada); z, oz = frac_dias(c[0], c[1], c[2], range(15, 21), sin_marcada)
        filas.append({"criatura": f"s{c[0]} {c[1]} {HERMANA[c[2]]}", "d8_11": r4(a), "dias_op_d8_11": oa, "d15_20": r4(z), "dias_op_d15_20": oz, "diferencia": r4(z - a) if a is not None and z is not None else None})
    L2 = media_ee([f["diferencia"] for f in filas]); L2["veredicto"] = veredicto(L2); L2["criaturas"] = filas; R["L2"] = L2
    # L2b
    filas = []
    for c in CRIATURAS:
        k8 = (c[0], 8, c[1], c[2]); v8 = V.get(k8); d8 = (1.0 if aceptada(v8) else 0.0) if (v8 and not fuera(k8, sin_marcada) and es_op(v8)) else None
        z, oz = frac_dias(c[0], c[1], c[2], range(10, 21), sin_marcada)
        filas.append({"criatura": f"s{c[0]} {c[1]} {HERMANA[c[2]]}", "dia8": d8, "d10_20": r4(z), "dias_op_d10_20": oz, "diferencia": r4(z - d8) if d8 is not None and z is not None else None})
    L2b = media_ee([f["diferencia"] for f in filas]); L2b["veredicto"] = veredicto(L2b); L2b["criaturas"] = filas; R["L2b"] = L2b
    # L4
    def l4(S, b):
        tot = acc = 0
        for d in range(12, 21):
            k = (S, d, b, 11); v = V.get(k)
            if not v or fuera(k, sin_marcada): continue
            ac = set(n for n, ts in v["acc"].items() if ts)
            for i, inv in enumerate(v["inv"]):
                if inv.get("falsa") or inv["accion"] not in COGER: continue
                if verdad(inv["accion"], {"anillo": inv.get("anillo"), "calma": inv.get("calma")}, inv.get("cuerpo")): tot += 1; acc += (i in ac)
        return (acc / tot if tot else None), tot
    A = [l4(S, "MIENTEN_DOS") for S in SERIES]; B = [l4(S, "MIENTE_UNA") for S in SERIES]
    xa = [x for x, _ in A if x is not None]; xb = [x for x, _ in B if x is not None]
    ea = st.stdev(xa) / math.sqrt(len(xa)); eb = st.stdev(xb) / math.sqrt(len(xb)); dif = st.mean(xa) - st.mean(xb); e = math.sqrt(ea * ea + eb * eb)
    L4 = {"MIENTEN_DOS_prudente": [r4(x) for x in xa], "cargadas_A": [t for _, t in A], "MIENTE_UNA_prudente": [r4(x) for x in xb], "cargadas_B": [t for _, t in B],
          "media_A": r4(st.mean(xa)), "media_B": r4(st.mean(xb)), "media": r4(dif), "ee": r4(e), "en_ee": r4(abs(dif) / e) if e else None}
    L4["veredicto"] = veredicto(L4); R["L4"] = L4
    return R


def secundarios():
    """S1 y S2 (registro del 15-oct 22:15) con la medida de S1 decidida por la mesa (16-oct 13:55)."""
    F = falsas(False); s1_acierto = 0; sell_acierto = 0; sin_cogida = []; n = 0
    for k, v, e in F:
        n += 1; ac = (e.get("acierto") or {}).get("cuerpo") == 1; sell_acierto += ac
        ts_acc = [t for t in v["acc"].get(v["pos"], []) if t <= e["tick"]]; t0 = max(ts_acc) if ts_acc else None; t1 = e["tick"]
        ts = sorted(t for t in v["T"] if t0 is not None and t0 <= t <= t1); cog = None
        for a_, b_ in zip(ts, ts[1:]):
            if v["T"][b_][1] > v["T"][a_][1]: cog = b_; break
        if cog is None: sin_cogida.append((ac, e.get("fuente"))); continue
        uso = next((h for h in v["huellas"] if cog < h <= t1), None)
        antes = [t for t in ts if t < uso] if uso else ts; t_fin = max(antes) if antes else cog
        subida = v["T"][t_fin][0] - v["T"][cog][0]
        if subida >= 15: s1_acierto += 1
    return {"evaluaciones": n, "sellado": {"aciertos": sell_acierto, "fallos": n - sell_acierto, "fraccion_fallo": r4((n - sell_acierto) / n)},
            "S1_estricto": {"aciertos": s1_acierto, "fallos": n - s1_acierto, "fraccion_fallo": r4((n - s1_acierto) / n)},
            "S2_sin_cogida": {"evaluaciones": len(sin_cogida), "juzgadas_acierto": sum(1 for a, _ in sin_cogida if a), "juzgadas_fallo": sum(1 for a, _ in sin_cogida if not a),
                              "por_via": {f"{'acierto' if a else 'fallo'} · {'uso del botiquin' if f == 'huella' else f}": sum(1 for a2, f2 in sin_cogida if a2 == a and f2 == f) for a, f in sorted(set(sin_cogida), key=str)}}}


def descriptivo():
    D = {"confianza_por_dia": {}, "agarre_falsa": {}, "agarre_verdaderas": {}, "abandono": {}, "L3_descriptivo": {}, "vigilancia": {}}
    for b in BRAZOS:
        for sl in (10, 11):
            key = f"{b} · {HERMANA[sl]}"
            D["confianza_por_dia"][key] = {dim: [r4(st.mean([V[(S, d, b, sl)]["conf"].get(dim) for S in SERIES if (S, d, b, sl) in V and V[(S, d, b, sl)]["conf"].get(dim) is not None])) if any((S, d, b, sl) in V for S in SERIES) else None for d in range(1, 21)] for dim in ("cuerpo", "recursos", "vinculo")}
            if (b, sl) != ("MIENTE_UNA", 11):
                op = [V[(S, d, b, sl)] for S in SERIES for d in range(8, 21) if (S, d, b, sl) in V and es_op(V[(S, d, b, sl)])]
                D["agarre_falsa"][key] = {"dias_oportunidad": len(op), "aceptada": sum(aceptada(v) for v in op), "fraccion": r4(sum(aceptada(v) for v in op) / len(op)) if op else None}
            for tramo, dias in (("d1-7", range(1, 8)), ("d8-20", range(8, 21))):
                tot = acc = 0
                for S in SERIES:
                    for d in dias:
                        v = V.get((S, d, b, sl))
                        if not v: continue
                        ac = set(n for n, t in v["acc"].items() if t)
                        for i, inv in enumerate(v["inv"]):
                            if inv.get("falsa"): continue
                            if verdad(inv["accion"], {"anillo": inv.get("anillo"), "calma": inv.get("calma")}, inv.get("cuerpo")): tot += 1; acc += (i in ac)
                D["agarre_verdaderas"].setdefault(key, {})[tramo] = {"verdaderas_cargadas": tot, "aceptadas": acc, "fraccion": r4(acc / tot) if tot else None}
            vids = [V[(S, d, b, sl)] for S in SERIES for d in range(1, 21) if (S, d, b, sl) in V]
            D["vigilancia"][key] = {"vidas": len(vids), "puesto_medio": r4(st.mean([v["puesto"] for v in vids if v["puesto"] is not None])), "muertes": sum(v["murio"] for v in vids)}
    for c in CRIATURAS:
        dias = [d for d in range(8, 21) if (c[0], d, c[1], c[2]) in V and es_op(V[(c[0], d, c[1], c[2])])]
        acept = [d for d in dias if aceptada(V[(c[0], d, c[1], c[2])])]
        if not acept: dia = "nunca la acepto"
        elif acept[-1] == dias[-1]: dia = None
        else: dia = next(d for d in dias if d > acept[-1])
        D["abandono"][f"s{c[0]} {c[1]} {HERMANA[c[2]]}"] = {"dias_con_oportunidad": len(dias), "dias_aceptada": len(acept), "ultimo_dia_aceptada": acept[-1] if acept else None, "dia_de_abandono": dia if dia is not None else "sin abandono"}
    for b in BRAZOS:
        D["L3_descriptivo"][b] = [{"serie": S, **dict(zip(("fraccion", "dias_op"), frac_dias(S, b, 10, range(10, 21), False)))} for S in SERIES]
    # vigilancia sellada: golpes y vida perdida mientras va a por botiquines en amenaza (de la aceptacion de la falsa a la cogida o, si no la hay, a su evaluacion)
    for b, sl in (("MIENTEN_DOS", 10), ("MIENTEN_DOS", 11), ("MIENTE_UNA", 10)):
        ng = vida_p = 0; vent = 0
        for S in SERIES:
            for d in range(8, 21):
                v = V.get((S, d, b, sl))
                if not v or v["pos"] is None: continue
                evs = sorted(e["tick"] for e in v["ev"] if e["n"] == v["pos"])
                for t0 in v["acc"].get(v["pos"], []):
                    t1 = next((t for t in evs if t >= t0), None) or t0 + 480
                    ts = sorted(t for t in v["T"] if t0 <= t <= t1); fin = t1
                    for a_, b_ in zip(ts, ts[1:]):
                        if v["T"][b_][1] > v["T"][a_][1]: fin = b_; break
                    gs = [g for t, g in v["golpes"].items() if t0 <= t <= fin]; ng += len(gs); vida_p += sum(gs); vent += 1
        D["vigilancia"][f"{b} · {HERMANA[sl]}"].update({"ventanas_a_por_el_botiquin": vent, "golpes": ng, "vida_perdida": r4(vida_p), "golpes_por_ventana": r4(ng / vent) if vent else None})
    F = falsas(False)
    D["evaluaciones_por_fuente"] = {f"{f} · {'acierto' if a else 'fallo'}": sum(1 for _, _, e in F if e.get("fuente") == f and ((e.get("acierto") or {}).get("cuerpo") == 1) == a) for f in sorted({e.get("fuente") for _, _, e in F}) for a in (True, False)}
    # curva de L2b por fallos previos
    curva = {"por_dia": {t: [0, 0] for t in ("0", "1", "2", "3+")}, "aceptaciones_por_fallos_en_ese_momento": {t: 0 for t in ("0", "1", "2", "3+")}}
    tr = lambda n: "3+" if n >= 3 else str(n)
    for c in CRIATURAS:
        fallos = []
        for d in range(8, 21):
            v = V.get((c[0], d, c[1], c[2]))
            if v and v["pos"] is not None: fallos += [(d, e["tick"]) for e in v["ev"] if e["n"] == v["pos"] and (e.get("acierto") or {}).get("cuerpo") == 0]
        for d in range(8, 21):
            v = V.get((c[0], d, c[1], c[2]))
            if not v or not es_op(v): continue
            prev = sum(1 for dd, _ in fallos if dd < d); curva["por_dia"][tr(prev)][0] += 1; curva["por_dia"][tr(prev)][1] += aceptada(v)
            for t in v["acc"].get(v["pos"], []): curva["aceptaciones_por_fallos_en_ese_momento"][tr(sum(1 for dd, tt in fallos if dd < d or (dd == d and tt < t)))] += 1
    D["curva_L2b"] = {"por_dia": {t: {"dias_oportunidad": o, "aceptada": a, "fraccion": r4(a / o) if o else None} for t, (o, a) in curva["por_dia"].items()}, "aceptaciones_por_fallos_en_ese_momento": curva["aceptaciones_por_fallos_en_ese_momento"]}
    return D


def grafica(D):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True); dias = list(range(1, 21))
    est = {"MIENTEN_DOS · valiente": ("#c0392b", "-"), "MIENTEN_DOS · prudente": ("#c0392b", "--"), "MIENTE_UNA · valiente": ("#2c3e50", "-"), "MIENTE_UNA · prudente": ("#2c3e50", "--")}
    for i, dim in enumerate(("cuerpo", "recursos", "vinculo")):
        for k, (col, ls) in est.items(): ax[i].plot(dias, D["confianza_por_dia"][k][dim], color=col, ls=ls, lw=1.8, label=k + (" (razón honesta)" if k == "MIENTE_UNA · prudente" else ""))
        ax[i].axvline(7.5, color="#999", lw=0.8); ax[i].set_title(f"confianza en la razón · {dim}"); ax[i].set_xlabel("día (la falsa, desde el 8)"); ax[i].set_ylim(-0.02, 1.02); ax[i].set_xticks([1, 4, 8, 12, 16, 20]); ax[i].grid(alpha=0.25)
    ax[0].set_ylabel("media de las 3 series (cuaderno al cerrar el día)"); ax[0].legend(fontsize=8, loc="lower left")
    fig.tight_layout(); fig.savefig(os.path.join(AQUI, "P7_65_confianza.png"), dpi=130)


if __name__ == "__main__":
    malas = [(k, v["n_arranque"], len(v["inv"])) for k, v in V.items() if v["n_arranque"] is not None and v["n_arranque"] != len(v["inv"])]
    R = {"vidas": len(V), "invitaciones_que_no_cuadran_con_el_arranque": malas, "principal": principales(False), "sin_la_partida_marcada": principales(True), "secundarios": secundarios(),
         "noches_sin_razon": E.get("noches_sin_razon"), "reintentos": [(r["serie"], r["dia"], r["brazo"]) for r in E.get("reintentos", [])]}
    R["descriptivo"] = descriptivo(); grafica(R["descriptivo"])
    json.dump(R, open(os.path.join(AQUI, "P7_65_sello.json"), "w"), ensure_ascii=False, indent=1)
    for k in ("L1", "L2", "L2b", "L4"): print(k, R["principal"][k]["veredicto"], {x: R["principal"][k].get(x) for x in ("media", "ee", "en_ee", "n")}, "| sin marcada:", R["sin_la_partida_marcada"][k]["veredicto"])
    print("no cuadran:", len(malas))

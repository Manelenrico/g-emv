"""[P7-56] EL SELLO DEL PRIMER CAMPO DEL CAPITULO 5 (SELLO_P7_56.md), de una vez al acabar: de los diarios (P756_*), los cuadernos por dia (P7_56_res) y el estado (P7_56_estado.json).
  R1 fraccion de usos del botiquin (huellas vividas) cortados por un golpe (corte y dano_total > 0), por serie y brazo; CON < SIN y >= 3 ee.
  R2 verdad de cada invitacion evaluada por la TABLA DEL MUNDO del sello (accion x situacion x promesa de cuerpo); media de confianza_despues.cuerpo tras las evaluaciones de
     invitaciones VERDAD menos la de las FALSAS; > 0 y >= 3 ee (una observacion por evaluacion; tambien por criatura al d20).
  Vigilancia: pruebas "camuflaje + quieta" (huella de camuflaje con >= 24 tics sin cambiar de casilla dentro de la ventana) y golpes por minuto en ellas; aceptadas por tipo y accion;
  aceptadas que llegan a evaluarse por dia y hermana; puesto, vida perdida, muertes por hermana; confianza por dimension y dia (la del vinculo no informa: B saturado).
  Segunda cuenta sin partidas marcadas; solo dias validos en los dos brazos.  python3 analiza_P7_56.py -> P7_56_sello.json"""
import glob, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); RES = os.path.join(AQUI, "P7_56_res")
E = json.load(open(os.path.join(AQUI, "P7_56_estado.json"))); BRAZOS = ("CON_RAZON", "SIN_RAZON"); SERIES = sorted({p["serie"] for p in E["peticiones"]})
ee = lambda xs: (st.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else None); mean = lambda xs: (st.mean(xs) if xs else None)


def verdad(inv_accion, sit, prom):
    """la tabla del mundo del sello: VERDAD / FALSA de la promesa de cuerpo `prom` para la accion y la situacion (anillo, calma)."""
    a = inv_accion; p = float(prom or 0.0)
    if a == "USAR_BOTIQUIN": return p > 0 and (sit.get("calma") == "CALMA" or sit.get("anillo") == "DENTRO")
    if a == "USAR_RACION": return 0 < p <= 20
    if a in ("COGER_BOTIQUIN", "COGER_RACION"): return True            # 0 al coger; si promete > 0 se juzga por el uso posterior: se acepta como verdad si la vida lo uso (se informa aparte)
    if a in ("COGER_RED", "EMPUNAR_RED", "COGER_CAMUFLAJE", "PONERSE_CAMUFLAJE"): return p == 0
    if a == "DAR_BOTIQUIN_HERMANA": return p <= 0
    if a == "ACERCARSE_HERMANA": return p == 0
    if a == "QUEDARSE_QUIETA": return (p <= 0) if sit.get("anillo") == "DENTRO" else (p < 0 if sit.get("anillo") == "FUERA" else p <= 0)
    return False


def vida(S, d, b, sl, p):
    fs = glob.glob(os.path.join(RUNS, f"P756_s{S}_d{d}_{b}_{p['semilla']}", f"*policy_agent_{sl}.art.log"))
    if not fs: return None
    H = []; AC = []; EV = []; CI = None; AR = None; T = []; fin = None; perdida = 0.0
    for line in open(fs[0], errors="replace"):
        if line.startswith('{"k":"tick"'):
            r = json.loads(line)
            if r.get("phase") != "live": continue
            T.append((r["tick"], tuple(r.get("pos") or (0, 0)), sum(float(g.get("amount") or 0) for g in (r.get("damage_taken") or [])), (r.get("body") or {}).get("id") if isinstance(r.get("body"), dict) else r.get("body"))); perdida += T[-1][2]
        elif line.startswith('{"k":"P7_huella"'): H.append(json.loads(line))
        elif line.startswith('{"k":"P7_54_aceptada"'): AC.append(json.loads(line))
        elif line.startswith('{"k":"P7_54_evaluada"'): EV.append(json.loads(line))
        elif line.startswith('{"k":"P7_54_cierre"'): CI = json.loads(line)
        elif line.startswith('{"k":"P7_54_arranque"'): AR = json.loads(line)
        elif line.startswith('{"k":"final"'): fin = json.loads(line)
    kit = [h for h in H if (h.get("objeto") or "first_aid") == "first_aid"]; cort = [h for h in kit if h.get("corte") and float(h.get("dano_total") or 0) > 0]
    # camuflaje + quieta: huella de camuflaje con >= 24 tics sin cambiar de casilla dentro de la ventana; golpes por minuto en esas ventanas
    idx = {t[0]: i for i, t in enumerate(T)}; cq = []
    for h in H:
        if h.get("objeto") != "camouflage": continue
        i0 = idx.get(int(h["t0"])); i1 = idx.get(int(h.get("t_fin") or h["t0"]))
        if i0 is None or i1 is None: continue
        w = T[i0:i1 + 1]; quieta = any(all(w[j][1] == w[k][1] for k in range(j, min(j + 24, len(w)))) for j in range(0, max(1, len(w) - 23)))
        if quieta and len(w) >= 24: cq.append({"tics": len(w), "golpes_min": sum(1 for t in w if t[2] > 0) / (len(w) / 1440.0)})
    inv = {i["_k"] if "_k" in i else k: i for k, i in enumerate([])}  # (las invitaciones del dia viajan en la imagen; se leen del cuaderno de invitaciones)
    return {"usos_kit": len(kit), "cortados": len(cort), "aceptadas": AC, "evaluadas": EV, "cierre": CI, "arranque": AR, "puesto": (fin or {}).get("placement"), "murio": (T[-1][0] < 14000) if T else None, "vida_perdida": perdida, "camo_quieta": cq,
            "marcada": not ((p.get("latencia") or {}).get(str(sl)) or {}).get("pasa", True), "huellas": len(H), "huellas_inutil": sum(1 for h in H if h.get("objeto") in ("net", "camouflage"))}


def invitaciones(S, d, sl):
    """las invitaciones que esa vida cargo = las que la razon dejo la noche d-1 (respuesta guardada en cuadernos_P7_56/CON_RAZON_serie<S>/razon_s<S>_d<d-1>_<sl>.txt), en el mismo orden"""
    import razon_P7_54 as RZ
    f = os.path.join(AQUI, "cuadernos_P7_56", f"CON_RAZON_serie{S}", f"razon_s{S}_d{d - 1}_{sl}.txt")
    if not os.path.exists(f): return None
    lineas = [l.strip() for l in open(f).read().split("\n") if l.strip().startswith("INVITACION")]
    return [x for x in (RZ.parsea(l) for l in lineas) if x]


V = {}
for p in E["peticiones"]:
    if p["estado"] != "completed": continue
    for sl in (10, 11):
        v = vida(p["serie"], p["dia"], p["brazo"], sl, p)
        if v: V[(p["serie"], p["dia"], p["brazo"], sl)] = v


def evalua(fuera_marcadas):
    def dias_validos(S):
        ds = set(range(1, 21))
        for b in BRAZOS:
            ds &= {d for (s_, d, b_, sl) in V if s_ == S and b_ == b}
            if fuera_marcadas: ds -= {d for (s_, d, b_, sl), v in V.items() if s_ == S and b_ == b and v["marcada"]}
        return sorted(ds)
    R1 = {b: [] for b in BRAZOS}; R1n = {b: [] for b in BRAZOS}; VERD = []; FALS = []; VIG = {}
    for S in SERIES:
        ds = dias_validos(S)
        if not ds: continue
        for b in BRAZOS:
            vs = [v for (s_, d, b_, sl), v in V.items() if s_ == S and b_ == b and d in ds]; usos = sum(v["usos_kit"] for v in vs); cort = sum(v["cortados"] for v in vs)
            R1[b].append(cort / usos if usos else None); R1n[b].append((usos, cort))
            VIG[f"s{S} {b}"] = {"dias_validos": len(ds), "usos_kit": usos, "cortados": cort, "puesto": {h: mean([v["puesto"] for (s_, d, b_, sl), v in V.items() if s_ == S and b_ == b and d in ds and sl == slh and v["puesto"] is not None]) for h, slh in (("valiente", 10), ("prudente", 11))},
                                "vida_perdida": {h: mean([v["vida_perdida"] for (s_, d, b_, sl), v in V.items() if s_ == S and b_ == b and d in ds and sl == slh]) for h, slh in (("valiente", 10), ("prudente", 11))}, "muertes": {h: sum(1 for (s_, d, b_, sl), v in V.items() if s_ == S and b_ == b and d in ds and sl == slh and v["murio"]) for h, slh in (("valiente", 10), ("prudente", 11))},
                                "camo_quieta": {"ventanas": sum(len(v["camo_quieta"]) for v in vs), "golpes_min": mean([x["golpes_min"] for v in vs for x in v["camo_quieta"]])}, "huellas": sum(v["huellas"] for v in vs), "huellas_inutil": sum(v["huellas_inutil"] for v in vs), "marcadas": sum(1 for v in vs if v["marcada"])}
            if b == "CON_RAZON":
                ac = [a for v in vs for a in v["aceptadas"]]; ev = [e for v in vs for e in v["evaluadas"]]
                VIG[f"s{S} {b}"]["aceptadas"] = len(ac); VIG[f"s{S} {b}"]["evaluadas"] = len(ev); VIG[f"s{S} {b}"]["aceptadas_por_accion"] = {}; VIG[f"s{S} {b}"]["pendientes_al_cierre"] = sum((v["cierre"] or {}).get("pendientes", 0) for v in vs)
                for a in ac: VIG[f"s{S} {b}"]["aceptadas_por_accion"][a["accion"]] = VIG[f"s{S} {b}"]["aceptadas_por_accion"].get(a["accion"], 0) + 1
                VIG[f"s{S} {b}"]["confianza_d20"] = {sl: ((V.get((S, 20, b, sl)) or {}).get("cierre") or {}).get("confianza") for sl in (10, 11)}
                VIG[f"s{S} {b}"]["evaluadas_por_dia_hermana"] = {f"d{d} a{sl}": (len(V[(S, d, b, sl)]["aceptadas"]), len(V[(S, d, b, sl)]["evaluadas"])) for d in ds for sl in (10, 11) if (S, d, b, sl) in V}
                # R2: verdad por la tabla
                for (s_, d, b_, sl), v in V.items():
                    if not (s_ == S and b_ == b and d in ds): continue
                    inv = invitaciones(S, d, sl) or []
                    for e in v["evaluadas"]:
                        i = inv[e["n"]] if e["n"] < len(inv) else None; sit = {"anillo": (i or {}).get("anillo"), "calma": (i or {}).get("calma")}
                        vt = verdad(e["accion"], sit, (e.get("prometido") or {}).get("cuerpo")) if i else None
                        (VERD if vt else FALS).append(float((e.get("confianza_despues") or {}).get("cuerpo") or 0.0)) if vt is not None else None
    def comp(xc, xs, menor=True):
        xc = [x for x in xc if x is not None]; xs = [x for x in xs if x is not None]
        if not xc or not xs: return {"dif": None}
        d = st.mean(xc) - st.mean(xs); e = ((ee(xc) or 0) ** 2 + (ee(xs) or 0) ** 2) ** 0.5
        return {"CON": [round(x, 3) for x in xc], "SIN": [round(x, 3) for x in xs], "media_C": round(st.mean(xc), 3), "media_S": round(st.mean(xs), 3), "dif": round(d, 3), "ee": round(e, 3), "tres_veces": bool(e and abs(d) >= 3 * e), "direccion_ok": (d < 0) if menor else (d > 0), "pasa": bool(e and abs(d) >= 3 * e and ((d < 0) if menor else (d > 0)))}
    r2 = {"n_verdad": len(VERD), "n_falsa": len(FALS), "media_verdad": (round(st.mean(VERD), 3) if VERD else None), "media_falsa": (round(st.mean(FALS), 3) if FALS else None)}
    if VERD and FALS:
        d = st.mean(VERD) - st.mean(FALS); e = ((ee(VERD) or 0) ** 2 + (ee(FALS) or 0) ** 2) ** 0.5; r2.update({"dif": round(d, 3), "ee": round(e, 3), "tres_veces": bool(e and abs(d) >= 3 * e), "pasa": bool(e and d > 0 and d >= 3 * e)})
    else: r2.update({"dif": None, "pasa": False})
    return {"R1": {**comp(R1["CON_RAZON"], R1["SIN_RAZON"], True), "usos_cortes": R1n}, "R2": r2, "vigilancia": VIG}


R = {"series": SERIES, "con_todas": evalua(False), "sin_marcadas": evalua(True), "partidas": sum(1 for p in E["peticiones"] if p["estado"] == "completed"), "marcadas": [(p["serie"], p["dia"], p["brazo"], sl) for p in E["peticiones"] for sl, g in (p.get("latencia") or {}).items() if not g.get("pasa")],
     "razon": {"llamadas": len(E.get("razon", [])), "tokens_entrada": sum(r["tokens_entrada"] for r in E.get("razon", [])), "tokens_salida": sum(r["tokens_salida"] for r in E.get("razon", [])), "usd_supuesto": round(sum(r["usd_supuesto"] for r in E.get("razon", [])), 4), "por_serie": {S: round(sum(r["usd_supuesto"] for r in E.get("razon", []) if r["serie"] == S), 4) for S in SERIES}, "noches_sin_razon": E.get("noches_sin_razon", [])},
     "reintentos": len(E.get("reintentos", [])), "apartadas": len(E.get("apartadas", [])), "dias_perdidos": E.get("dias_perdidos", [])}
json.dump(R, open(os.path.join(AQUI, "P7_56_sello.json"), "w"), ensure_ascii=False, indent=1)
print("R1", {k: v for k, v in R["con_todas"]["R1"].items() if k not in ("CON", "SIN")}); print("R2", R["con_todas"]["R2"]); print("razon", R["razon"])
for k, v in R["con_todas"]["vigilancia"].items(): print(k, {kk: vv for kk, vv in v.items() if kk not in ("evaluadas_por_dia_hermana",)})

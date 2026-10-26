"""[P7-29] EL BANCO (molde de banco_P7_23 / banco_P7_28; UNA VIDA POR PROCESO; sin partidas ni llamadas). La pieza `nace_P7_29` enganchada despues de las tres del siete.
  python3 banco_P7_29.py --f1 [--hilos N]      F1: los 80 diarios de A4 con `apagado` (GEMV_P7=0) y con `TECHO` sin pedir (GEMV_P7_PIDE=0, como en banco_P7_23), GEMV_P7_29=1 -> P7_29_F1.json
  python3 banco_P7_29.py --cache [--hilos N]   la cache sola (arreglo 0) sobre las 16 vidas replicables de APRENDE de los dias 16-20 de P7-24: fidelidad bit a bit y
                                              tiempo de decision por tic antes / despues -> P7_29_cache.json
  python3 banco_P7_29.py --f2 [--hilos N]      F2: las mismas 16 vidas con los arreglos 1 y 2 (y la cache): el PRIMER instante en que cambia la decision, con lo que el
                                              diario hacia y lo que la replica hace; y la creencia del botiquin de las cuatro criaturas recalculada dia a dia sin los
                                              cortes (arreglo 3) desde los cuadernos de P7_24_res -> P7_29_F2.json
  python3 banco_P7_29.py --f3 [--hilos N]      F3: la curiosidad del cuanto sobre la vida s1 d20 asiento 10 de P7-24 (lleva dos botiquines todo el dia y no los usa):
                                              cuadernos (a) solo "al menos" del botiquin, (b) (a) + un recuerdo firme, (c) (a) + tres firmes, (d) el real del dia 19;
                                              por tic con el paso listo y botiquin en el zurron: lo elegido, la vida, la M del cuanto, d(usar_botiquin) -> P7_29_F3.json
  python3 banco_P7_29.py --vida CARP SLOT --brazo B --cuadernos DIR --salida F [--arreglos a,b,c] [--p29 0|1]
La replica sigue las observaciones del diario (lazo abierto): dice que elegiria el cuerpo en cada escena, no lo que habria pasado despues."""
import collections, copy, glob, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_29_tmp"); TODOS = ("cache", "curiosidad", "corte", "cuanto"); CAMPO = TODOS      # [P7-29b] la red de los muros se quito del todo; los resultados con ella (P7_29_F1/F2.json) son del commit f9a2e75
VIDAS_16_20 = [(f"P724_s{s}_d{d}_APRENDE", s, d, sl) for s in (1, 2) for d in range(16, 21) for sl in (10, 11) if (s, d, sl) not in ((1, 20, 11), (2, 18, 10), (2, 18, 11), (2, 20, 10))]   # las 4 parciales no traen player_config


def carpeta(pref): return os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", pref + "_*"))[0])


def vida(carp, slot, brazo, cuad, arreglos, p29, pide=1):
    os.environ["GEMV_P7_PIDE"] = str(pide); os.environ["GEMV_P7_PIDE2"] = str(pide); os.environ["GEMV_P7_NACE"] = "1"; os.environ["GEMV_P7_29"] = str(p29)
    if not carp.startswith(("P611", "P624")): os.environ["GEMV_OJOS"] = "0"
    import banco_P7_5 as B
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS[brazo].get(k, "0")
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    from alma import decisor_zs as D
    import descubre_P7 as X, pide_P7 as J, nace_P7_23 as N, nace_P7_29 as N29
    for k in TODOS: N29.E["arreglos"][k] = k in arreglos
    if "muros" in arreglos: raise SystemExit("la red de los muros se quito en P7-29b")
    HECHO = {}; REG = []; MS = []; CNT = collections.Counter()
    # el diario, para el seguimiento de cada tic
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]; DIA = {}
    for line in open(f, errors="replace"):
        if '"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "tick" and r.get("phase") == "live":
            n = collections.Counter()
            for s_ in (r.get("pack") or []):
                if s_: n[s_.get("id")] += int(s_.get("n") or 1)
            DIA[r["tick"]] = {"pos": tuple(r["pos"]), "hp": r.get("hp"), "listo": (r.get("move_ready_in") or 0) == 0, "bloqueado": r.get("action_result") == "blocked", "kits": n.get("first_aid", 0), "rac": n.get("rations", 0), "ms": (r.get("RADIOGRAFIA") or {}).get("ms")}
    _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); HECHO["J"] = J.aplica(clase, registra); HECHO["N"] = N.aplica(clase, registra); HECHO["29"] = N29.aplica(clase, registra)
        _oc = D.candidatos; _od = D.decide
        def _cands(obs, mundo, mem, tick, bloqueos=None):
            out = _oc(obs, mundo, mem, tick, bloqueos)
            cur = next((r for n_, r in out if n_ == "ir_curioso"), None); pos = tuple((obs.get("you") or {}).get("pos") or (0, 0))
            REG.append({"t": tick, "ir_curioso": ({"destino": list(cur.get("destino") or ()), "clase": cur.get("curioso") or ((cur.get("recoger") or [None])[0]), "dist": max(abs(cur["destino"][0] - pos[0]), abs(cur["destino"][1] - pos[1]))} if cur and cur.get("destino") else None)})
            return out
        def _dec(obs, mundo, mem, tick, bloqueos=None):
            t0 = time.perf_counter(); ac, ra = _od(obs, mundo, mem, tick, bloqueos); MS.append((time.perf_counter() - t0) * 1000.0)
            el = str(ra.get("elegido") or ""); CNT["tics"] += 1; C_ = ra.get("candidatos") or {}
            def fila(n_, f_):
                c_ = C_.get(n_); return ((c_.get("filas") or {}).get(f_) if isinstance(c_, dict) else None)
            if REG and REG[-1]["t"] == tick:
                REG[-1].update({"el": el, "hp": (obs.get("you") or {}).get("hp"), "kits": X.kits_en(obs.get("you") or {}, mundo), "R-CURIOSIDAD": fila(el, "R-CURIOSIDAD"), N29.FILA_CUANTO: fila(el, N29.FILA_CUANTO), "cuanto_en_usar": fila("usar_botiquin", N29.FILA_CUANTO), "cuanto": N29.E.get("ultimo_cuanto"),
                                "d": {k2: (v["d"] if isinstance(v, dict) else v) for k2, v in (ra.get("candidatos") or {}).items() if k2 in ("ir_curioso", "ir_objeto", "ir_centro", "ir_botin", "noop", "usar_botiquin", "usar_racion", "coger", el)}})
            return ac, ra
        D.candidatos = _cands; D.decide = _dec
        return h
    X.aplica = _aplica
    r = B.vida(carp, slot, brazo, cuad)
    for x in REG:
        d = DIA.get(x["t"]) or {}; x["diario"] = {"listo": d.get("listo"), "bloqueado": d.get("bloqueado"), "ms": d.get("ms")}
    c = X.ESTADO["cuaderno"]
    return {"carp": carp, "slot": slot, "brazo": brazo, "arreglos": sorted(arreglos), "p29": p29, "hecho": r["hecho"], "hecho_J": HECHO.get("J"), "hecho_N": HECHO.get("N"), "hecho_29": HECHO.get("29"), "tics": r["tics"], "fidelidad": r["fidelidad"], "desacuerdos": r["desacuerdos"],
            "ms_replica": {"mediana": (sorted(MS)[len(MS) // 2] if MS else None), "p90": (sorted(MS)[int(0.9 * len(MS))] if MS else None), "max": (max(MS) if MS else None), "n": len(MS)}, "desajustes": N29.E["desajustes"],
            "registros": REG, "huellas": r["huellas"], "errores": r["errores"], "cuaderno_fin": (c.volcado() if c is not None else None)}


def lanza(carp, slot, brazo, cuad, arreglos, p29, salida, pide=1):
    if os.path.exists(salida): os.remove(salida)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--brazo", brazo, "--cuadernos", cuad, "--arreglos", ",".join(arreglos), "--p29", str(p29), "--pide", str(pide), "--salida", salida], capture_output=True, text=True, timeout=7200)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": carp, "slot": slot, "brazo": brazo, "error": (r.stderr or r.stdout)[-800:]}


def resumen_fid(res):
    fid = collections.Counter(); des = []
    for r in res:
        if r.get("error"): fid["error"] += 1; continue
        fid.update(r["fidelidad"]); des += [{"vida": f"{r['carp']}/{r['slot']}", **d} for d in r["desacuerdos"][:5]]
    return dict(fid), des


def f1(hilos):
    vidas = [(os.path.basename(c), s) for pat in ("P611_t1_A4_*", "P611_t2_A4_*", "P624_t1_A4_*") for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))) for s in (10, 11) if glob.glob(os.path.join(c, f"*policy_agent_{s}.art.log"))]
    R = json.load(open(os.path.join(AQUI, "P7_29_F1.json"))) if os.path.exists(os.path.join(AQUI, "P7_29_F1.json")) else {}
    for brazo, arr, et in (("apagado", TODOS, "apagado"), ("TECHO", TODOS, "TECHO con la red de muros"), ("TECHO", CAMPO, "TECHO sin la red de muros")):
        if et in R and "--solo" in sys.argv and sys.argv[sys.argv.index("--solo") + 1] not in et: continue
        t0 = time.time(); cu = os.path.join(SAL, "cuad_f1_" + brazo); os.makedirs(cu, exist_ok=True)
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda v: lanza(v[0], v[1], brazo, cu, arr, 1, os.path.join(SAL, f"f1_{brazo}_{v[0]}_{v[1]}.json"), pide=0), vidas))
        fid, des = resumen_fid(res); ok = next((r for r in res if not r.get("error")), {})
        for r in res:
            if r.get("error"): print("  ERROR", r["carp"], r["slot"], r["error"][-300:], flush=True)
        R[et] = {"vidas": len(vidas), "arreglos": list(arr), "fidelidad": fid, "desacuerdos": des, "muros": sum(r.get("muros", 0) for r in res if not r.get("error")), "vidas_con_desacuerdo": sum(1 for r in res if not r.get("error") and r["desacuerdos"]), "segundos": round(time.time() - t0, 1), "hecho_29": ok.get("hecho_29")}
        print(f"F1 {et}: {fid} · {len(des)} desacuerdos (primeros) · muros {R[brazo]['muros']} · {R[brazo]['segundos']} s · P7-29 {ok.get('hecho_29')}", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_29_F1.json"), "w"), ensure_ascii=False, indent=1)


def cuadernos_del_dia_anterior(s, d, destino):
    shutil.rmtree(destino, ignore_errors=True); os.makedirs(destino)
    for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_24_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json"), os.path.join(destino, f"cuaderno_P7_{q}.json"))
    return destino


def corre_16_20(etiqueta, arreglos, p29, hilos):
    def una(v):
        pref, s, d, sl = v; f = os.path.join(SAL, f"{etiqueta}_s{s}_d{d}_{sl}.json")
        if "--reusa" in sys.argv and os.path.exists(f) and not json.load(open(f)).get("error"): return json.load(open(f))
        cu = cuadernos_del_dia_anterior(s, d, os.path.join(SAL, f"cuad_{etiqueta}_s{s}_d{d}_{sl}"))
        return lanza(carpeta(pref), sl, "APRENDE", cu, arreglos, p29, f)
    with ThreadPoolExecutor(hilos) as ex: return list(ex.map(una, VIDAS_16_20))


def cache(hilos):
    t0 = time.time(); R = {}
    for etiqueta, arr in (("sin_cache", ()), ("con_cache", ("cache",))):
        hechos = [os.path.join(SAL, f"{etiqueta}_s{s}_d{d}_{sl}.json") for _, s, d, sl in VIDAS_16_20]
        res = [json.load(open(f)) for f in hechos] if ("--reusa" in sys.argv and all(os.path.exists(f) for f in hechos) and not any(json.load(open(f)).get("error") for f in hechos)) else corre_16_20(etiqueta, arr, 1, hilos)
        fid, des = resumen_fid(res)
        R[etiqueta] = {"fidelidad": fid, "desacuerdos": des, "por_vida": [{k: r.get(k) for k in ("carp", "slot", "tics", "fidelidad", "ms_replica", "desajustes")} for r in res], "ms_mediana_de_medianas": (sorted(r["ms_replica"]["mediana"] for r in res if not r.get("error"))[len([r for r in res if not r.get("error")]) // 2] if any(not r.get("error") for r in res) else None)}
        for r in res:
            if r.get("error"): print("  ERROR", r["carp"], r["slot"], r["error"][-300:], flush=True)
        print(f"cache {etiqueta}: {fid} · ms mediana de medianas {R[etiqueta]['ms_mediana_de_medianas']} · {round(time.time() - t0)} s", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_29_cache.json"), "w"), ensure_ascii=False, indent=1)


def creencia_sin_cortes():
    """Arreglo 3 sobre los cuadernos del campo: la creencia del botiquin (dentro / fuera) con y sin los cortes, por criatura y dia."""
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    os.environ.setdefault("GEMV_P7", "1"); os.environ.setdefault("GEMV_P7_CUADERNO", "1"); os.environ.setdefault("GEMV_P7_NOVEDAD", "1"); os.environ.setdefault("GEMV_P7_NACE", "1"); os.environ.setdefault("GEMV_P7_29", "1")
    from recuerdo_P7_23 import CuadernoP23
    import nace_P7_29 as N29
    out = []
    for s in (1, 2):
        for sl in (10, 11):
            for d in range(1, 21):
                f = os.path.join(AQUI, "P7_24_res", f"cuaderno_s{s}_d{d}_APRENDE_{sl}.json")
                if not os.path.exists(f): continue
                c = CuadernoP23.lee(f, sl); con = {sit: c.creencia("first_aid", sit) for sit in ("dentro", "fuera")}
                c.__class__ = N29.CuadernoP29; N29.E["arreglos"]["corte"] = True; sin = {sit: c.creencia("first_aid", sit) for sit in ("dentro", "fuera")}
                rec = c.recuerdos_de("first_aid")
                out.append({"serie": s, "asiento": sl, "dia": d, "con_cortes": {k: (v or {}).get("cuerpo") for k, v in con.items()}, "sin_cortes": {k: (v or {}).get("cuerpo") for k, v in sin.items()}, "recuerdos": len(rec), "cortes": sum(1 for r in rec if r.get("corte")), "firmes": sum(1 for r in rec if not r.get("corte") and not r.get("al_menos")), "al_menos": sum(1 for r in rec if r.get("al_menos")),
                            "ignorancia": round(c.ignorancia("first_aid"), 4), "ignorancia_cuanto": round(c.ignorancia_cuanto("first_aid"), 4), "sabido_max": c.sabido_max("first_aid"), "racion": {"ignorancia_cuanto": round(c.ignorancia_cuanto("rations"), 4), "sabido_max": c.sabido_max("rations"), "sin_cortes_dentro": ((c.creencia("rations", "dentro") or {}).get("cuerpo"))}})
    return out


def f2(hilos):
    t0 = time.time(); res = corre_16_20("f2", ("cache", "curiosidad"), 1, hilos); res_m = corre_16_20("f2m", ("cache", "curiosidad", "muros"), 1, hilos); fid, _ = resumen_fid(res); vidas = []
    for r in res:
        if r.get("error"): print("  ERROR", r["carp"], r["slot"], r["error"][-300:], flush=True); vidas.append({"carp": r["carp"], "slot": r["slot"], "error": r["error"][-200:]}); continue
        des = r["desacuerdos"]; primero = des[0] if des else None; ctx = None
        if primero:
            x = next((x for x in r["registros"] if x["t"] == primero["t"]), None)
            if x: ctx = {k: x.get(k) for k in ("ir_curioso", "hp", "kits", "R-CURIOSIDAD", "d", "diario", "muros")}
        cur_dia = [x for x in r["registros"] if x.get("el") and x["ir_curioso"]]
        vidas.append({"carp": r["carp"], "slot": r["slot"], "tics": r["tics"], "fidelidad": r["fidelidad"], "primer_cambio": primero, "contexto_del_primer_cambio": ctx, "muros_aprendidos": r["muros"], "bloqueados_vistos": r["bloqueados_vistos"], "ms_replica": r["ms_replica"],
                      "cambios_totales": len(des), "cambios_desde_ir_curioso": sum(1 for d in des if d["diario"] == "ir_curioso"), "a_que_cambia": dict(collections.Counter(d["replica"] for d in des if d["diario"] == "ir_curioso").most_common(5)),
                      "ir_curioso_replica": sum(1 for x in r["registros"] if x.get("el") == "ir_curioso"), "R-CURIOSIDAD_max": max((x["R-CURIOSIDAD"] or 0) for x in r["registros"]) if r["registros"] else None})
    con_red = [{"carp": r.get("carp"), "slot": r.get("slot"), "muros_aprendidos": r.get("muros"), "primer_cambio": (r.get("desacuerdos") or [None])[0], "cambios_totales": len(r.get("desacuerdos") or []), "error": r.get("error")} for r in res_m]
    R = {"vidas": vidas, "fidelidad": fid, "con_la_red_de_muros": con_red, "creencia_sin_cortes": creencia_sin_cortes(), "segundos": round(time.time() - t0)}
    json.dump(R, open(os.path.join(AQUI, "P7_29_F2.json"), "w"), ensure_ascii=False, indent=1)
    print("F2", fid, "primeros cambios:", [(v.get("primer_cambio") or {}).get("t") for v in vidas], round(time.time() - t0), "s", flush=True)


def cuaderno_f3(destino, variante):
    """(a) solo 'al menos' del botiquin (30, 25, 20; el resto del cuaderno real del dia 19 de s1 asiento 10 sin recuerdos del botiquin); (b) (a) + un firme (45);
    (c) (a) + tres firmes (45, 40, 42); (d) el real."""
    from recuerdo_P7_23 import CuadernoP23
    shutil.rmtree(destino, ignore_errors=True); os.makedirs(destino)
    for q in (10, 11):
        f = os.path.join(AQUI, "P7_24_res", f"cuaderno_s1_d19_APRENDE_{q}.json"); c = CuadernoP23.lee(f, q)
        if variante != "d" and q == 10:
            c.objetos.pop("first_aid", None); c.dia -= 1          # los recuerdos nuevos se apuntan en el dia 19 y `escribe` vuelve a cerrar el dia
            foto = {"dolor_F": 0.8, "dolor_R": 0.5, "dolor_S": 0.4, "positivo": 0.2, "d": 3.5}; imp = {"cuerpo": -0.2, "recursos": 0.05, "vinculo": 0.0}
            for e in (30.0, 25.0, 20.0): c.apunta_P23("first_aid", {"dentro": True, "golpeado_48": True}, foto, ["noop"] * 4, {"cuerpo": e, "recursos": -1.0, "vinculo": 0.0}, imp, tick=100, al_menos=True)
            firmes = {"a": (), "b": (45.0,), "c": (45.0, 40.0, 42.0)}[variante]
            for e in firmes: c.apunta_P23("first_aid", {"dentro": True, "golpeado_48": True}, foto, ["noop"] * 4, {"cuerpo": e, "recursos": -1.0, "vinculo": 0.0}, imp, tick=200, al_menos=False)
            c.escribe(os.path.join(destino, f"cuaderno_P7_{q}.json"))
        else: shutil.copy(f, os.path.join(destino, f"cuaderno_P7_{q}.json"))
    return destino


def f3(hilos):
    t0 = time.time(); carp = carpeta("P724_s1_d20_APRENDE"); R = {}
    def una(v):
        f = os.path.join(SAL, f"f3_{v}.json")
        if "--reusa" in sys.argv and os.path.exists(f) and not json.load(open(f)).get("error"): return v, json.load(open(f))
        cu = cuaderno_f3(os.path.join(SAL, f"cuad_f3_{v}"), v); return v, lanza(carp, 10, "APRENDE", cu, CAMPO, 1, f)
    with ThreadPoolExecutor(min(hilos, 4)) as ex: res = dict(ex.map(una, ("a", "b", "c", "d")))
    for v, r in res.items():
        if r.get("error"): print("  ERROR", v, r["error"][-300:], flush=True); R[v] = {"error": r["error"][-300:]}; continue
        X_ = [x for x in r["registros"] if x.get("el") and (x.get("kits") or 0) >= 1]        # todos los tics con botiquin (usar no necesita el paso listo; durante el canal el candidato queda vetado)
        usa = [x for x in X_ if x["el"] == "usar_botiquin"]; ofrecido = [x for x in X_ if x["d"].get("usar_botiquin") is not None]
        R[v] = {"tics": r["tics"], "fidelidad": r["fidelidad"], "tics_listos_con_botiquin": len(X_), "tics_con_candidato_usar": len(ofrecido), "hp_con_candidato": sorted({int(x["hp"]) for x in ofrecido}), "elige_usar_botiquin": len(usa), "hp_al_elegir_usar": sorted(x["hp"] for x in usa), "primer_usar": (usa[0]["t"] if usa else None),
                "usar_cuando_se_ofrece": {str(int(x["hp"])): [sum(1 for y in ofrecido if int(y["hp"]) == int(x["hp"])), sum(1 for y in ofrecido if int(y["hp"]) == int(x["hp"]) and y["el"] == "usar_botiquin")] for x in ofrecido}, "d_usar_menos_elegido_cuando_se_ofrece": sorted(round((x["d"]["usar_botiquin"] or 0) - (x["d"].get(x["el"]) or 0), 4) for x in ofrecido),
                "fila_cuanto_en_usar_cuando_se_ofrece": sorted(round(x.get("cuanto_en_usar") or 0, 4) for x in ofrecido), "fila_cuanto_en_elegido_cuando_se_ofrece": sorted(round(x.get(FILA) or 0, 4) for x in ofrecido),
                "M_cuanto": {"mediana": (sorted(x[FILA] or 0 for x in X_)[len(X_) // 2] if X_ else None), "max": max((x[FILA] or 0) for x in X_) if X_ else None}, "M_curiosidad_mediana": (sorted(x["R-CURIOSIDAD"] or 0 for x in X_)[len(X_) // 2] if X_ else None),
                "cuanto_ejemplo": next((x["cuanto"] for x in X_ if x.get("cuanto")), None), "d_usar_menos_elegido_mediana": (sorted((x["d"].get("usar_botiquin") or 0) - (x["d"].get(x["el"]) or 0) for x in X_ if x["d"].get("usar_botiquin") is not None)[max(0, sum(1 for x in X_ if x["d"].get("usar_botiquin") is not None) // 2)] if any(x["d"].get("usar_botiquin") is not None for x in X_) else None),
                "hp_con_botiquin": {"min": min(x["hp"] for x in X_) if X_ else None, "mediana": (sorted(x["hp"] for x in X_)[len(X_) // 2] if X_ else None)}, "por_decena_de_vida": {str(dec): [sum(1 for y in X_ if int(y["hp"]) // 10 * 10 == dec), sum(1 for y in X_ if int(y["hp"]) // 10 * 10 == dec and y["el"] == "usar_botiquin")] for dec in sorted({int(x["hp"]) // 10 * 10 for x in X_})},
                "cuaderno_botiquin": ((r.get("cuaderno_fin") or {}).get("creencias") or {}).get("first_aid")}
        print("F3", v, {k: R[v][k] for k in ("tics_listos_con_botiquin", "elige_usar_botiquin", "hp_al_elegir_usar", "M_cuanto", "M_curiosidad_mediana", "hp_con_botiquin")}, flush=True)
    R["segundos"] = round(time.time() - t0); json.dump(R, open(os.path.join(AQUI, "P7_29_F3.json"), "w"), ensure_ascii=False, indent=1)


FILA = "R-CURIOSIDAD-CUANTO"
if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True); a = sys.argv
    hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4
    if "--vida" in a:
        i = a.index("--vida"); carp, slot = a[i + 1], int(a[i + 2]); brazo = a[a.index("--brazo") + 1]; cuad = a[a.index("--cuadernos") + 1]; salida = a[a.index("--salida") + 1]
        arreglos = tuple(x for x in (a[a.index("--arreglos") + 1] if "--arreglos" in a else ",".join(TODOS)).split(",") if x); p29 = int(a[a.index("--p29") + 1]) if "--p29" in a else 1; pide = int(a[a.index("--pide") + 1]) if "--pide" in a else 1
        json.dump(vida(carp, slot, brazo, cuad, arreglos, p29, pide), open(salida, "w"), ensure_ascii=False)
    elif "--f1" in a: f1(hilos)
    elif "--cache" in a: cache(hilos)
    elif "--f2" in a: f2(hilos)
    elif "--f3" in a: f3(hilos)

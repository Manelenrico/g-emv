"""[P7-41] COMPROBACION PREVIA EN LOCAL (coste cero) de la composicion del campo (`campo_P7_41`), una vida por proceso, lazo abierto sobre diarios de P7-34:
  (a) que SIN EMOCION corre (brazo SIN, GEMV_P7_NOVEDAD=0) con eps = 0, 0,05 y 0,2 y las dos personalidades;
  (b) que eps se cumple: proporcion real de monedas que salen si entre las oportunidades (y eps efectivo = eps x miedo);
  (c) que con eps = 0 no prueba nunca nada desconocido: 0 forzadas y 0 decisiones `coger` / `usar_*` de clase desconocida (veto);
  (d) que la latencia pasa la guarda: ms por decision de la replica (mediana, p95, max; fraccion sobre el tic de 41,67 ms) para APRENDE (P7-40 de campo) y SIN.
  python3 banco_P7_41.py [--hilos 6] -> P7_41_comprobacion.json
  python3 banco_P7_41.py --vida CARP SLOT --brazo B --eps E --miedo M --salida F"""
import glob, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_41_tmp"); TIC_MS = 1000.0 / 24.0


def vida(carp, slot, brazo, eps, miedo):
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import banco_P7_5 as B5
    base = B5.BRAZOS["APRENDE" if brazo.startswith("SIN") else brazo]
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = base.get(k, "0")
    if brazo.startswith("SIN"): os.environ["GEMV_P7_NOVEDAD"] = "0"
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "1"; os.environ["GEMV_P7_NACE"] = "1"; os.environ["GEMV_P7_29"] = "1"; os.environ["GEMV_P7_33"] = "1"; os.environ["GEMV_OJOS"] = "0"; os.environ["P7_33"] = "1"
    os.environ["GEMV_P7_BRAZO"] = brazo; os.environ["GEMV_P7_EPS"] = str(eps); os.environ["GEMV_P7_40_MIEDO"] = miedo; os.environ["GEMV_P7_41_SEMILLA"] = str(7 + slot)
    for k in ("GEMV_P7_43_CACHE", "GEMV_P7_43_MURO"): os.environ.setdefault(k, "0")           # [P7-43] los mandos vienen del entorno del que llama
    B5.BRAZOS["SIN"] = dict(B5.BRAZOS["APRENDE"], GEMV_P7_NOVEDAD="0")        # SIN EMOCION = APRENDE sin curiosidad (banco_P7_33.vida vuelve a poner el entorno del brazo)
    import banco_P7_33 as B33, nace_P7_33 as N33m, campo_P7_41 as C41, descubre_P7 as X
    cu = os.path.join(SAL, f"cu_{brazo}_{eps}_{miedo}_{os.path.basename(carp)}_{slot}"); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
    b = os.path.basename(carp).split("_"); s, d = int(b[1][1:]), int(b[2][1:])
    var = os.environ.get("P7_43_VARIANTE")          # [P7-43] replicas de las vidas del campo P7-42 (P741_*): el cuaderno del dia anterior de esa variante (P7_41_res)
    if d > 1 and brazo != "BORRADO":
        for q in (10, 11):
            src = os.path.join(AQUI, os.environ.get("P7_43_RES", "P7_41_res"), f"cuaderno_s{s}_d{d - 1}_{var}_{q}.json") if (var and os.path.basename(carp).startswith("P741")) else os.path.join(AQUI, "P7_34_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json")
            if os.path.exists(src): shutil.copy(src, os.path.join(cu, f"cuaderno_P7_{q}.json"))
    HECHO = {}; REGS = []; DIRR = {}
    _n33 = N33m.aplica
    def _n33_y_41(clase, registra=None):
        h = _n33(clase, registra)
        def reg(r):
            if isinstance(r, dict) and str(r.get("k", "")).startswith("P7_41"): REGS.append(r)
            if registra: registra(r)
        HECHO["41"] = C41.aplica(clase, reg)
        _odd = clase.decidir
        def _decidir(self, obs, _d=_odd):
            ac, ra = _d(self, obs)
            if ra is not None and getattr(self, "phase", None) == "live":
                acc = ac
                if isinstance(acc, str):
                    try: acc = json.loads(acc)
                    except Exception: acc = {}
                DIRR[self.tick] = (acc.get("dir") if isinstance(acc, dict) and acc.get("do") == "move" else None)
            return ac, ra
        clase.decidir = _decidir
        return h
    N33m.aplica = _n33_y_41
    r = B33.vida(carp, slot, "SIN" if brazo.startswith("SIN") else brazo, cu, ("cache", "curiosidad", "corte", "cuanto"), 1, 1)
    out = {"carp": os.path.basename(carp), "slot": slot, "brazo": brazo, "eps": eps, "miedo": miedo, "hecho_41": HECHO.get("41"), "tics": r["tics"], "fidelidad": r["fidelidad"], "ms": r.get("ms_replica"), "desajustes": r.get("desajustes"),
           "cache": os.environ.get("GEMV_P7_43_CACHE"), "muro": os.environ.get("GEMV_P7_43_MURO"), "elegidos": [(x["t"], x.get("el")) for x in r.get("registros", []) if "el" in x]}
    try:
        import rapido_P7_43 as RP43; out["P7_43"] = RP43.estado()
        import guarda_latencia_P7_29 as GL
        f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))[0]; DIR = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
        T = []
        for line in open(f, errors="replace"):
            if '"k":"tick"' not in line[:12]: continue
            r_ = json.loads(line)
            if r_.get("phase") == "live": T.append((r_["tick"], tuple(r_["pos"]), r_.get("action_result"), (r_.get("intencion") or {}).get("dir"), (r_.get("move_ready_in") or 0) == 0, [a for a in (r_.get("ve_agentes") or []) if a.get("pos")]))
        EL_ = dict(out["elegidos"]); listos = sum(1 for t in T if t[4]); prev = None; bloq_diario = 0; bloq_replica = 0; pos_despues = {}
        for t in T:
            if prev and t[2] == "blocked" and prev[3] in DIR:
                dx, dy = DIR[prev[3]]; hacia = (prev[1][0] + dx, prev[1][1] + dy)
                if not any(tuple(a["pos"]) == hacia for a in t[5]):
                    bloq_diario += 1
                    if DIRR.get(prev[0]) == prev[3]: bloq_replica += 1     # la replica emitio el MISMO paso (misma direccion) que el diario en ese tic: habria chocado igual
            prev = t
        marcas = out["P7_43"].get("marcados") or []; pisadas = 0
        for m in marcas:
            c = tuple(m["casilla"]); pisadas += int(any(t[1] == c for t in T if t[0] > m["tick"]))
        out["muestra_dir"] = [(t[0], t[3], DIRR.get(t[0]), EL_.get(t[0])) for t in T[900:912]]
        out["bloqueos"] = {"listos": listos, "diario_sin_cuerpo": bloq_diario, "diario_pct": round(100 * bloq_diario / max(1, listos), 2), "replica_mismo_paso": bloq_replica, "replica_pct": round(100 * bloq_replica / max(1, listos), 2), "marcas": len(marcas), "marcas_luego_pisadas": pisadas, "caducadas": out["P7_43"].get("caducadas")}
    except Exception as ex: out["bloqueos_error"] = repr(ex)[:200]
    if brazo.startswith("SIN"):
        import azar_P7_41 as AZ
        op = [x for x in REGS if x.get("momento") == "oportunidad"]; fz = [x for x in REGS if x.get("momento") == "forzada"]; fin = [x for x in REGS if x.get("momento") == "fin"]
        out["azar"] = {"oportunidades": len(op), "monedas_si": sum(1 for x in op if x.get("moneda")), "p_medio": (sum(x["p"] for x in op) / len(op) if op else None), "forzadas": len(fz), "fines": {k: sum(1 for x in fin if x.get("fin") == k) for k in ("cogida", "usada", "caduca")},
                       "momentos": AZ.E["momentos"], "monedas_momento": AZ.E["monedas_si"], "usos_propios": AZ.E["usos_propios"], "usos_propios_agrupados": (lambda T: sum(1 for i, (t, e) in enumerate(T) if i == 0 or t - T[i - 1][0] >= 240 or e != T[i - 1][1]))(sorted(AZ.E.get("usos_ticks", []))), "forzadas_conocida": sum(1 for x in fz if x.get("conocida")), "forzadas_por_tipo": {t: sum(1 for x in fz if x.get("tipo") == t) for t in ("ir", "usar")},
                       "vetos": AZ.E["vetos"], "elegidas_desconocidas_sin_forzar": AZ.E["elegidas_desconocidas"], "elegidas_detalle": [x for x in REGS if x.get("momento") == "elegida_desconocida"][:5], "por_objeto": {o: sum(1 for x in op if x.get("objeto") == o) for o in ("first_aid", "rations", "net", "camouflage")}}
    else:
        try:
            import filo_P7_40 as FI; out["P7_40"] = {"apuntes": len(FI.E["apuntes"]), "miedo": FI.MIEDO}
        except Exception: pass
    return out


def lanza(carp, slot, brazo, eps, miedo):
    salida = os.path.join(SAL, f"v_{brazo}_{eps}_{miedo}_{os.path.basename(carp)}_{slot}.json")
    if os.path.exists(salida): os.remove(salida)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--brazo", brazo, "--eps", str(eps), "--miedo", miedo, "--salida", salida], capture_output=True, text=True, timeout=3600)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": os.path.basename(carp), "slot": slot, "brazo": brazo, "eps": eps, "miedo": miedo, "error": (r.stderr or r.stdout)[-1200:]}


if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True)
    if "--vida" in a:
        i = a.index("--vida"); r = vida(a[i + 1], int(a[i + 2]), a[a.index("--brazo") + 1], float(a[a.index("--eps") + 1]), a[a.index("--miedo") + 1]); json.dump(r, open(a[a.index("--salida") + 1], "w"), ensure_ascii=False); sys.exit(0)
    hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 6
    if "--paradas" in a:
        vidas = [("P741p_s1_d14_APRENDE_v_*", 11, "APRENDE", "valiente", "APRENDE_v"), ("P741p_s1_d11_APRENDE_p_*", 10, "APRENDE", "prudente", "APRENDE_p"), ("P741p_s1_d10_SIN_*", 11, "SIN", "prudente", "SIN"),
                 ("P741p_s1_d11_BORRADO_p_*", 11, "BORRADO", "prudente", "BORRADO_p"), ("P741p_s1_d1_BORRADO_v_*", 10, "BORRADO", "valiente", "BORRADO_v"), ("P741p_s1_d9_BORRADO_p_*", 10, "BORRADO", "prudente", "BORRADO_p"), ("P741_s1_d5_TECHO_*", 10, "TECHO", "prudente", "TECHO")]
        R = []
        def una(args):
            pat, sl, brazo, miedo, var = args; carp = glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))[0]
            env = dict(os.environ, GEMV_P7_43_CACHE="1", GEMV_P7_43_MURO="1", P7_43_VARIANTE=var, P7_43_RES="P7_41_res_piloto"); salida = os.path.join(SAL, f"par_{var}_{sl}.json")
            if os.path.exists(salida): os.remove(salida)
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(sl), "--brazo", brazo, "--eps", "0.00019", "--miedo", miedo, "--salida", salida], capture_output=True, text=True, timeout=3600, env=env)
            return json.load(open(salida)) if os.path.exists(salida) else {"carp": pat, "error": (r.stderr or r.stdout)[-800:]}
        with ThreadPoolExecutor(hilos) as ex: R = list(ex.map(una, vidas))
        for r in R:
            if r.get("error"): print("ERROR", r["carp"], r["error"][-300:]); continue
            b = r.get("bloqueos") or {}; ms = r.get("ms") or {}
            print(r["carp"], r["slot"], f"diario bloqueada sin cuerpo {b.get('diario_pct')} % -> replica mismo paso {b.get('replica_pct')} % · marcas {b.get('marcas')} (luego pisadas {b.get('marcas_luego_pisadas')}, caducadas {b.get('caducadas')}) · ms mediana {ms.get('mediana') and round(ms['mediana'], 2)} p95 {ms.get('p95') and round(ms['p95'], 2)} max {ms.get('max') and round(ms['max'], 1)} sobre el tic {ms.get('n') and round(100 * sum(1 for _ in []) / 1, 2)}", r.get("bloqueos_error") or "")
        json.dump(R, open(os.path.join(AQUI, "P7_43_paradas.json"), "w"), ensure_ascii=False, indent=1); sys.exit(0)
    if "--identidad" in a:
        vidas = [("P741_s1_d14_APRENDE_v_*", 11, "APRENDE", "valiente", "APRENDE_v"), ("P741_s1_d11_APRENDE_p_*", 10, "APRENDE", "prudente", "APRENDE_p"), ("P741_s1_d10_SIN_*", 11, "SIN", "prudente", "SIN")]
        if "--mas" in a: vidas += [("P741_s1_d11_BORRADO_p_*", 11, "BORRADO", "prudente", "BORRADO_p"), ("P741_s1_d13_APRENDE_v_*", 10, "APRENDE", "valiente", "APRENDE_v"), ("P741_s1_d9_SIN_*", 10, "SIN", "prudente", "SIN")]
        R = []
        def una(args):
            pat, sl, brazo, miedo, var = args; carp = glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))[0]; out = {}
            for cache in ("0", "1"):
                env = dict(os.environ, GEMV_P7_43_CACHE=cache, GEMV_P7_43_MURO=os.environ.get("GEMV_P7_43_MURO", "0"), P7_43_VARIANTE=var)
                salida = os.path.join(SAL, f"id_{var}_{sl}_c{cache}.json")
                if os.path.exists(salida): os.remove(salida)
                r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(sl), "--brazo", brazo, "--eps", "0.00019", "--miedo", miedo, "--salida", salida], capture_output=True, text=True, timeout=3600, env=env)
                out[cache] = json.load(open(salida)) if os.path.exists(salida) else {"error": (r.stderr or r.stdout)[-800:]}
            a0, a1 = out["0"].get("elegidos") or [], out["1"].get("elegidos") or []
            dif = [(t0, e0, e1) for (t0, e0), (t1, e1) in zip(a0, a1) if e0 != e1]
            return {"vida": pat, "slot": sl, "n": min(len(a0), len(a1)), "distintas": len(dif) + abs(len(a0) - len(a1)), "primeras": dif[:5], "ms_sin": out["0"].get("ms"), "ms_con": out["1"].get("ms"), "cache": out["1"].get("P7_43"), "error": out["0"].get("error") or out["1"].get("error")}
        with ThreadPoolExecutor(hilos) as ex: R = list(ex.map(una, vidas))
        for r in R: print(r["vida"], r["slot"], "decisiones", r["n"], "DISTINTAS", r["distintas"], r["primeras"], "ms sin cache", r["ms_sin"] and round(r["ms_sin"]["mediana"], 2), "con", r["ms_con"] and round(r["ms_con"]["mediana"], 2), "p90", r["ms_con"] and round(r["ms_con"]["p90"], 2), "max", r["ms_con"] and round(r["ms_con"]["max"], 1), r["cache"] and {k: r["cache"][k] for k in ("aciertos", "fallos")}, r.get("error"))
        json.dump(R, open(os.path.join(AQUI, "P7_43_identidad.json"), "w"), ensure_ascii=False, indent=1); sys.exit(0)
    if "--calibra" in a:
        eps = float(a[a.index("--calibra") + 1]); miedo = a[a.index("--miedo") + 1] if "--miedo" in a else "prudente"
        vidas = sorted((c, sl) for c in glob.glob(os.path.join(RAIZ, "paintball", "runs", "P734_s*_d*_APRENDE_*")) for sl in (10, 11))
        t0 = time.time()
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda v: lanza(v[0], v[1], "SIN", eps, miedo), vidas))
        json.dump({"eps": eps, "miedo": miedo, "vidas": res, "segundos": round(time.time() - t0)}, open(os.path.join(AQUI, f"P7_42_calibracion_{eps}.json"), "w"), ensure_ascii=False, indent=1)
        ok = [r for r in res if not r.get("error")]; print(f"eps {eps}: {len(ok)} vidas ok, {len(res) - len(ok)} errores; momentos {sum(r['azar']['momentos'] for r in ok)}, monedas {sum(r['azar']['monedas_momento'] for r in ok)}, forzadas {sum(r['azar']['forzadas'] for r in ok)}, usos propios {sum(r['azar']['usos_propios'] for r in ok)} (agrupados a 240 tics {sum(r['azar']['usos_propios_agrupados'] for r in ok)}), elegidas desconocidas {sum(r['azar']['elegidas_desconocidas_sin_forzar'] for r in ok)}")
        sys.exit(0)
    vidas = [(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P734_s1_d{d}_APRENDE_*"))[0], sl) for d in (1, 10) for sl in (10, 11)]
    confs = [("APRENDE", 0.0, "prudente"), ("APRENDE", 0.0, "valiente"), ("BORRADO", 0.0, "prudente"), ("SIN", 0.0, "prudente"), ("SIN", 0.05, "prudente"), ("SIN", 0.2, "prudente"), ("SIN", 0.2, "valiente")]
    t0 = time.time()
    with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda x: lanza(x[0][0], x[0][1], *x[1]), [(v, c) for c in confs for v in vidas]))
    R = {"vidas": res, "segundos": round(time.time() - t0)}
    for r in res:
        ms = r.get("ms") or {}
        print(r["brazo"], r["eps"], r["miedo"], r["carp"], r["slot"], ("ERROR " + r["error"][-300:]) if r.get("error") else f"fid {r['fidelidad']} ms mediana {ms.get('mediana') and round(ms['mediana'], 2)} p90 {ms.get('p90') and round(ms['p90'], 1)} max {ms.get('max') and round(ms['max'], 1)} azar {r.get('azar')} P7_40 {r.get('P7_40')}", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_41_comprobacion.json"), "w"), ensure_ascii=False, indent=1)

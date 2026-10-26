"""[P7-38] EL BANCO = banco_P7_38 con la pieza `contrafactual_P7_38` (GEMV_P7_38 = A | off) en vez de la de P7-37; cadena por criatura (cuaderno + pistas del pasado viajan en la carpeta) y momentos.
[P7-37] EL BANCO (molde de banco_P7_36; una vida por proceso; lazo abierto: las obs son las del diario, las decisiones de la replica no cambian lo que pasa).
  --cadena [--hilos 4]   paso 1: las 4 criaturas de APRENDE de P7-34, cada una sus 20 dias EN CADENA (el cuaderno que escribe la replica del dia d, con las importancias
                         descontadas, es el que lee el dia d+1; `curiosa_P7_38` con GEMV_P7_38=descontada) -> P7_38_res/cuaderno_descontada_s<S>_d<D>_<asiento>.json
                         y P7_38_cadena.json (fidelidad, recuerdos descontados por vida).
  --momentos [--hilos 6] paso 2: las 80 vidas, cada una con el cuaderno descontado del dia anterior, bajo las cuatro lecturas (campo, descontada, C, C5): en los MOMENTOS
                         (los 71 tics en que el diario decidio coger una red o un camuflaje, P7_36_cogidas.json, y las aperturas de las pruebas de red y camuflaje,
                         P7_34_datos.json) que elige la replica y que curiosidad tiene cada clase; fidelidad al diario -> P7_38_momentos.json
  --vida CARP SLOT --variante V --cuadernos DIR --ticks t1,t2 --salida F
"""
import glob, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_38_tmp"); RES = os.path.join(AQUI, "P7_38_res"); VARIANTES = ("A",)


def vida(carp, slot, variante, cu, ticks):
    os.environ["GEMV_P7_38"] = variante; os.environ["P7_33"] = "1"
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import banco_P7_33 as B33, banco_P7_5 as B5
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B5.BRAZOS["APRENDE"].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "1"; os.environ["GEMV_P7_NACE"] = "1"; os.environ["GEMV_P7_29"] = "1"; os.environ["GEMV_P7_33"] = "1"; os.environ["GEMV_OJOS"] = "0"
    import descubre_P7 as X, contrafactual_P7_38 as CU
    CU.E["momentos"] = set(ticks); HECHO = {}; EL = {}
    DIARIO = {}
    for line in open(glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))[0], errors="replace"):
        if '"k":"tick"' not in line[:12]: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("phase") == "live": DIARIO[r["tick"]] = str((r.get("RADIOGRAFIA") or {}).get("elegido") or "")
    # la pieza de P7-38 se engancha POR FUERA de todas las del siete: banco_P7_33 encadena descubre, pedir, nacer, P7-29 y P7-33 en su `_aplica`, y la ultima es
    # `N33.aplica`; se envuelve esa (el atributo `aplica` del modulo nace_P7_33) para que la de P7-38 vea las ventanas de la red y el camuflaje, que se cierran en la de P7-33
    # (leccion de P7-37: enganchada por dentro, no veia esas ventanas; 4 recuerdos de red y camuflaje con dano conocido se quedaron sin descontar)
    import nace_P7_33 as N33m
    _n33 = N33m.aplica
    def _n33_y_38(clase, registra=None):
        h = _n33(clase, registra); HECHO["38"] = CU.aplica(clase, registra)
        _odd = clase.decidir
        def _decidir(self, obs, _d=_odd):
            ac, ra = _d(self, obs)
            if ra is not None and getattr(self, "phase", None) == "live": EL[self.tick] = str(ra.get("elegido") or "")
            return ac, ra
        clase.decidir = _decidir
        return h
    N33m.aplica = _n33_y_38            # banco_P7_33.vida importa nace_P7_33 dentro de la funcion y llama a N33.aplica al aplicar: ve este envoltorio
    r = B33.vida(carp, slot, "APRENDE", cu, ("cache", "curiosidad", "corte", "cuanto"), 1, 1)
    des = [{"t": t, "diario": e, "replica": EL.get(t)} for t, e in sorted(DIARIO.items()) if EL.get(t) is not None and EL.get(t) != e]
    return {"carp": os.path.basename(carp), "slot": slot, "variante": variante, "hecho_38": HECHO.get("38"), "tics": r["tics"], "fidelidad": r["fidelidad"], "desacuerdos": des, "contrafactual": {"n": CU.E["n_contrafactual"], "cualquiera": CU.E["n_cualquiera"], "sin_referencia": CU.E["n_sin_ref"]},
            "momentos": {str(t): {"diario": DIARIO.get(t), "replica": EL.get(t), **CU.E["anotado"].get(t, {})} for t in sorted(ticks)}, "cuaderno_fin": r.get("cuaderno_fin"), "desajustes": r.get("desajustes")}


def lanza(carp, slot, variante, cu, ticks, salida):
    if os.path.exists(salida): os.remove(salida)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--variante", variante, "--cuadernos", cu, "--ticks", ",".join(map(str, ticks)) or "-", "--salida", salida], capture_output=True, text=True, timeout=3600)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": os.path.basename(carp), "slot": slot, "variante": variante, "error": (r.stderr or r.stdout)[-800:]}


def carpeta(s, d): return glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P734_s{s}_d{d}_APRENDE_*"))[0]


def cadena(hilos):
    os.makedirs(RES, exist_ok=True)
    def una(cr):
        s, sl = cr; cu = os.path.join(SAL, f"cadena_s{s}_a{sl}"); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu); out = []
        for d in range(1, 21):
            r = lanza(carpeta(s, d), sl, "A", cu, [], os.path.join(SAL, f"cadena_s{s}_d{d}_a{sl}.json"))
            if r.get("error"): out.append({"dia": d, "error": r["error"]}); print(f"s{s} d{d} a{sl}: ERROR {r['error'][-300:]}", flush=True); break
            esc = os.path.join(cu, f"cuaderno_P7_{sl}.json")
            if os.path.exists(esc): shutil.copy(esc, os.path.join(RES, f"cuaderno_A_s{s}_d{d}_{sl}.json"))
            out.append({"dia": d, "fidelidad": r["fidelidad"], "contrafactual": r["contrafactual"], "desajustes": r.get("desajustes")}); print(f"s{s} d{d} a{sl}: {r['fidelidad']} contrafactual {r['contrafactual']}", flush=True)
        return (f"s{s} a{sl}", out)
    t0 = time.time()
    with ThreadPoolExecutor(hilos) as ex: res = dict(ex.map(una, [(1, 10), (1, 11), (2, 10), (2, 11)]))
    json.dump({"criaturas": res, "segundos": round(time.time() - t0)}, open(os.path.join(AQUI, "P7_38_cadena.json"), "w"), ensure_ascii=False, indent=1)
    print("cadena hecha en", round(time.time() - t0), "s")


def momentos(hilos):
    CG = json.load(open(os.path.join(AQUI, "P7_36_cogidas.json"))); D34 = [v for v in json.load(open(os.path.join(AQUI, "P7_34_datos.json"))) if not v.get("sin_diario") and v["brazo"] == "APRENDE"]
    T = {}
    for v in CG["vidas"]:
        if v["brazo"] == "APRENDE": T.setdefault((v["serie"], v["dia"], v["asiento"]), set()).update(x["tick_decide"] for x in v["cogidas"])
    for v in D34:
        for o in ("red", "camuflaje"): T.setdefault((v["serie"], v["dia"], v["asiento"]), set()).update(v["pruebas"][o]["t0"])
    vidas = sorted(T)
    def una(args):
        (s, d, sl), var = args; cu = os.path.join(SAL, f"mom_{var}_s{s}_d{d}_a{sl}"); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
        if d > 1:
            f = os.path.join(RES, f"cuaderno_A_s{s}_d{d - 1}_{sl}.json")
            if os.path.exists(f): shutil.copy(f, os.path.join(cu, f"cuaderno_P7_{sl}.json"))
        r = lanza(carpeta(s, d), sl, var, cu, sorted(T[(s, d, sl)]), os.path.join(SAL, f"mom_{var}_s{s}_d{d}_a{sl}.json")); r.pop("cuaderno_fin", None); r["serie"], r["dia"] = s, d; return r
    R = {}
    for var in VARIANTES:
        t0 = time.time()
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(una, [(v, var) for v in vidas]))
        R[var] = res; print(f"{var}: {len(res)} vidas en {time.time() - t0:.0f} s · errores {sum(1 for r in res if r.get('error'))} · fidelidad {sum(r.get('fidelidad', {}).get('igual', 0) for r in res)} igual / {sum(r.get('fidelidad', {}).get('difiere', 0) for r in res)} difiere", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_38_momentos.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True)
    if "--vida" in a:
        i = a.index("--vida"); tk = a[a.index("--ticks") + 1]; ticks = [int(x) for x in tk.split(",") if x not in ("", "-")]
        r = vida(a[i + 1], int(a[i + 2]), a[a.index("--variante") + 1], a[a.index("--cuadernos") + 1], ticks); json.dump(r, open(a[a.index("--salida") + 1], "w"), ensure_ascii=False); sys.exit(0)
    hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else (4 if "--cadena" in a else 6)
    if "--cadena" in a: cadena(hilos)
    elif "--momentos" in a: momentos(hilos)

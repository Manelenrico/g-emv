"""[P7-47] EL BANCO (coste cero; SELLO_P7_47.md): las 12 criaturas de APRENDE del campo P7-45 (3 series x 2 asientos x 2 personalidades), cada una sus 20 dias EN CADENA
HONESTA con P7-40 + `habitua_P7_47` (lazo abierto sobre los diarios P741_s*_d*_APRENDE_*; molde banco_P7_40 --cadena sobre banco_P7_41.vida = la composicion del campo).
Por vida: fidelidad al diario, el cuaderno que escribe la replica (-> P7_47_res/cuaderno_s<S>_d<D>_<var>_<asiento>.json), lo que manda al cierre (curiosidad A con h,
cautela 1, por clase), el estado de habituacion, y los MOMENTOS (tics en que el diario eligio `coger` con red o camuflaje a los pies + aperturas de pruebas de red y
camuflaje): que elige la replica y la curiosidad de cada clase.
  python3 banco_P7_47.py --cadena [--hilos 6]  -> P7_47_cadena.json
  python3 banco_P7_47.py --vida CARP SLOT --variante V --salida F"""
import glob, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_47_tmp"); RES = os.path.join(AQUI, "P7_47_res"); VARIANTES = ("APRENDE_v", "APRENDE_p"); MIEDO = {"APRENDE_v": "valiente", "APRENDE_p": "prudente"}
INUTIL = ("net", "camouflage")


def momentos_de(carp, slot):
    """tics en que el diario eligio `coger` con red o camuflaje a los pies, y aperturas (t0) de huellas de red o camuflaje."""
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))[0]; T = set(); H = set()
    for line in open(f, errors="replace"):
        if line.startswith('{"k":"tick"'):
            if '"elegido": "coger"' not in line and '"elegido":"coger"' not in line: continue
            try: r = json.loads(line)
            except Exception: continue
            if r.get("phase") != "live": continue
            pos = tuple(r.get("pos") or (0, 0))
            if any(it.get("id") in INUTIL and tuple(it.get("pos") or ()) == pos for it in (r.get("ve_items") or [])): T.add(r["tick"])
        elif line.startswith('{"k":"P7_huella"'):
            try: r = json.loads(line)
            except Exception: continue
            if r.get("objeto") in INUTIL: H.add(int(r["t0"]))
    return sorted(T), sorted(H)


def vida(carp, slot, var):
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    os.environ["GEMV_P7_47"] = "1"; os.environ["P7_43_VARIANTE"] = var; os.environ["P7_43_RES"] = os.path.relpath(RES, AQUI); os.environ["GEMV_P7_43_CACHE"] = "1"; os.environ["GEMV_P7_43_MURO"] = "1"
    os.environ["GEMV_P7_BRAZO"] = "APRENDE"; os.environ["GEMV_P7_40_MIEDO"] = MIEDO[var]
    cog, ap = momentos_de(carp, slot); ticks = sorted(set(cog) | set(ap))
    import banco_P7_41 as B41, campo_P7_41 as C41          # las piezas (descubre, filo, habitua...) leen el entorno al importarse: se importan DENTRO de aplica, cuando banco_P7_41 ya lo ha puesto
    HECHO = {}; M = {}
    _oc = C41.aplica
    def _c41_y_47(clase, registra=None):
        h = _oc(clase, registra)
        import filo_P7_40 as FI, habitua_P7_47 as HAB, descubre_P7 as X, nace_P7_33 as N33
        M.update(FI=FI, HAB=HAB, X=X, N33=N33); FI.E["momentos"] = set(ticks); HECHO["47"] = HAB.aplica(clase, registra); return h
    C41.aplica = _c41_y_47
    r = B41.vida(carp, slot, "APRENDE", 0, MIEDO[var])
    FI, HAB, X, N33 = M["FI"], M["HAB"], M["X"], M["N33"]
    c = X.ESTADO.get("cuaderno"); mundo = FI.E.get("mundo"); cierre = None
    if c is not None and mundo is not None:
        A = {o: FI.curiosidad(c, mundo, o, 1.0) for o in N33.cuatro(mundo)}; manda = max(A, key=A.get)
        cierre = {"A": {o: round(v, 5) for o, v in A.items()}, "manda": manda, "inutil_manda": manda in INUTIL, "h": HAB.h_todas(c.dia_actual()), "ignorancia": {o: round(float(c._ignorancia0(o)), 4) for o in N33.cuatro(mundo)} if hasattr(c, "_ignorancia0") else None,
                  "recuerdos": {o: len([q for q in c.recuerdos_de(o) if not q.get("corte")]) for o in N33.cuatro(mundo)}}
    b = os.path.basename(carp).split("_"); s, d = int(b[1][1:]), int(b[2][1:])
    cu = os.path.join(B41.SAL, f"cu_APRENDE_0_{MIEDO[var]}_{os.path.basename(carp)}_{slot}"); esc = os.path.join(cu, f"cuaderno_P7_{slot}.json")
    if os.path.exists(esc): os.makedirs(RES, exist_ok=True); shutil.copy(esc, os.path.join(RES, f"cuaderno_s{s}_d{d}_{var}_{slot}.json"))
    mom = {str(t): {"diario_coger": t in set(cog), "apertura": t in set(ap), **{k: v for k, v in (FI.E["anotado"].get(t) or {}).items() if k in ("elegido", "d_coger", "d_noop", "cautela", "clases")}} for t in ticks}
    return {"carp": os.path.basename(carp), "slot": slot, "variante": var, "serie": s, "dia": d, "hecho_47": HECHO.get("47"), "tics": r.get("tics"), "fidelidad": r.get("fidelidad"), "ms": r.get("ms"), "cierre": cierre, "habitua": HAB.estado(), "momentos": mom,
            "huellas_replica": [{k: h.get(k) for k in ("objeto", "t0", "t_fin", "corte", "al_menos")} for h in (X.ESTADO.get("huellas") or [])]}


def lanza(carp, slot, var, salida):
    if os.path.exists(salida): os.remove(salida)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--variante", var, "--salida", salida], capture_output=True, text=True, timeout=3600)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": os.path.basename(carp), "slot": slot, "variante": var, "error": (r.stderr or r.stdout)[-1200:]}


def carpeta(s, d, var): return glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P741_s{s}_d{d}_{var}_*"))[0]


def cadena(hilos):
    os.makedirs(RES, exist_ok=True)
    def una(cr):
        var, s, sl = cr; out = []
        for d in range(1, 21):
            r = lanza(carpeta(s, d, var), sl, var, os.path.join(SAL, f"cadena_{var}_s{s}_d{d}_a{sl}.json"))
            if r.get("error"): out.append({"dia": d, "error": r["error"]}); print(f"{var} s{s} d{d} a{sl}: ERROR {r['error'][-400:]}", flush=True); break
            out.append(r); ci = r.get("cierre") or {}
            print(f"{var} s{s} d{d} a{sl}: fid {r.get('fidelidad')} manda {ci.get('manda')} h {ci.get('h')} habitua {r.get('habitua', {}).get('n_habitua')} efecto {r.get('habitua', {}).get('n_efecto')} momentos {len(r.get('momentos') or {})}", flush=True)
        return (f"{var} s{s} a{sl}", out)
    t0 = time.time()
    with ThreadPoolExecutor(hilos) as ex: res = dict(ex.map(una, [(var, s, sl) for var in VARIANTES for s in (1, 2, 3) for sl in (10, 11)]))
    json.dump({"criaturas": res, "segundos": round(time.time() - t0)}, open(os.path.join(AQUI, "P7_47_cadena.json"), "w"), ensure_ascii=False, indent=1)
    print("cadena hecha en", round(time.time() - t0), "s")


if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True)
    if "--vida" in a:
        i = a.index("--vida"); r = vida(a[i + 1], int(a[i + 2]), a[a.index("--variante") + 1]); json.dump(r, open(a[a.index("--salida") + 1], "w"), ensure_ascii=False); sys.exit(0)
    hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 6
    if "--cadena" in a: cadena(hilos)

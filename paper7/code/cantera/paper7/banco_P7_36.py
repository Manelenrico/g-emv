"""[P7-36, parte 1, banco] Las 40 vidas de APRENDE de P7-34 replicadas (lazo abierto, molde de banco_P7_33.vida, una vida por proceso), dos veces: SIN la regla (la
replica de siempre: fidelidad al diario) y CON la regla "en un empate, no se coge" (`empate_P7_36`, GEMV_P7_36_EMPATE=1). En los tics en que el diario decidio coger
una red o un camuflaje (P7_36_cogidas.json, `tick_decide`): que elige la replica con la regla, y las filas de la foto de `coger` frente a la de `noop` (que fila hace que
coger gane por 0,00x). Cuenta cuantas cogidas desaparecen y cuantas otras decisiones cambian. -> P7_36_banco.json
  python3 banco_P7_36.py [--hilos N]
  python3 banco_P7_36.py --vida CARP SLOT --regla 0|1 --ticks t1,t2 --salida F        (una vida, un proceso)"""
import glob, json, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_36_tmp")


def vida(carp, slot, regla, ticks):
    os.environ["GEMV_P7_36_EMPATE"] = str(regla); os.environ["P7_33"] = "1"
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import banco_P7_33 as B33, banco_P7_5 as B5
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B5.BRAZOS["APRENDE"].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["GEMV_P7_PIDE2"] = "1"; os.environ["GEMV_P7_NACE"] = "1"; os.environ["GEMV_P7_29"] = "1"; os.environ["GEMV_P7_33"] = "1"; os.environ["GEMV_OJOS"] = "0"
    from alma import decisor_zs as D
    import empate_P7_36 as EM, descubre_P7 as X
    HECHO = {}; FOTOS = {}; EL = {}
    # el cuaderno del dia anterior (el que la criatura leyo ese dia), copia fresca: la replica lo reescribe al acabar
    b = os.path.basename(carp).split("_"); s, d = int(b[1][1:]), int(b[2][1:]); cu = os.path.join(SAL, f"cuad_{regla}_{os.path.basename(carp)}_{slot}"); shutil.rmtree(cu, ignore_errors=True); os.makedirs(cu)
    if d > 1:
        for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_34_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json"), os.path.join(cu, f"cuaderno_P7_{q}.json"))
    # lo elegido en el diario, tic a tic
    DIARIO = {}
    for line in open(glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))[0], errors="replace"):
        if '"k":"tick"' not in line[:12]: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("phase") == "live": DIARIO[r["tick"]] = str((r.get("RADIOGRAFIA") or {}).get("elegido") or "")
    _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); HECHO["empate"] = EM.aplica(D)        # (banco_P7_33 encadena despues pedir, nacer, P7-29 y P7-33; la regla solo toca D.select_tiebreak)
        _odd = clase.decidir
        def _decidir(self, obs, _d=_odd):
            # lo que EMITE la politica en cada tic vivo (no cada llamada interna a D.decide: el cuerpo vuelve a llamar a decide por otra via cada 48 tics)
            ac, ra = _d(self, obs)
            if ra is not None and getattr(self, "phase", None) == "live":
                tick = self.tick; EL[tick] = str(ra.get("elegido") or "")
                if tick in ticks:
                    C = ra.get("candidatos") or {}
                    def fila(n_): c_ = C.get(n_); return ((c_.get("filas") or {}) if isinstance(c_, dict) else {})
                    def dd(n_): c_ = C.get(n_); return (c_.get("d") if isinstance(c_, dict) else c_)
                    fc, fn = fila("coger"), fila("noop"); claves = sorted(set(fc) | set(fn))
                    FOTOS[tick] = {"elegido": ra.get("elegido"), "d_coger": dd("coger"), "d_noop": dd("noop"), "filas_distintas": {k: (round(fc.get(k, 0.0), 5), round(fn.get(k, 0.0), 5)) for k in claves if abs(fc.get(k, 0.0) - fn.get(k, 0.0)) > 1e-6}}
            return ac, ra
        clase.decidir = _decidir
        return h
    X.aplica = _aplica
    r = B33.vida(carp, slot, "APRENDE", cu, ("cache", "curiosidad", "corte", "cuanto"), 1, 1)
    des = [{"t": t, "diario": e, "replica": EL.get(t)} for t, e in sorted(DIARIO.items()) if EL.get(t) is not None and EL.get(t) != e]
    return {"carp": os.path.basename(carp), "slot": slot, "regla": regla, "empate": HECHO.get("empate"), "veces_regla": EM.E["veces"], "tics": r["tics"], "fidelidad": r["fidelidad"], "desacuerdos": des,
            "en_las_cogidas": {str(t): {"diario": DIARIO.get(t), "replica": EL.get(t), **FOTOS.get(t, {})} for t in sorted(ticks)}, "desajustes": r.get("desajustes")}


def lanza(carp, slot, regla, ticks):
    salida = os.path.join(SAL, f"v_{regla}_{os.path.basename(carp)}_{slot}.json")
    if os.path.exists(salida): os.remove(salida)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), "--regla", str(regla), "--ticks", ",".join(map(str, ticks)) or "-", "--salida", salida], capture_output=True, text=True, timeout=3600)
    return json.load(open(salida)) if os.path.exists(salida) else {"carp": os.path.basename(carp), "slot": slot, "regla": regla, "error": (r.stderr or r.stdout)[-800:]}


if __name__ == "__main__":
    a = sys.argv; os.makedirs(SAL, exist_ok=True)
    if "--vida" in a:
        i = a.index("--vida"); tk = a[a.index("--ticks") + 1]; ticks = set(int(x) for x in tk.split(",") if x not in ("", "-"))
        r = vida(a[i + 1], int(a[i + 2]), int(a[a.index("--regla") + 1]), ticks); json.dump(r, open(a[a.index("--salida") + 1], "w"), ensure_ascii=False); sys.exit(0)
    hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 6
    CG = json.load(open(os.path.join(AQUI, "P7_36_cogidas.json")))
    vidas = [(os.path.join(RAIZ, "paintball", "runs", v["carpeta"]), v["asiento"], sorted(x["tick_decide"] for x in v["cogidas"])) for v in CG["vidas"] if v["brazo"] == "APRENDE"]
    R = {}
    for regla in (0, 1):
        t0 = time.time()
        with ThreadPoolExecutor(hilos) as ex: res = list(ex.map(lambda v: lanza(v[0], v[1], regla, v[2]), vidas))
        R[f"regla_{regla}"] = {"vidas": res, "segundos": round(time.time() - t0, 1)}
        print(f"regla {regla}: {len(res)} vidas en {time.time() - t0:.0f} s · errores {sum(1 for r in res if r.get('error'))} · fidelidad {sum(r.get('fidelidad', {}).get('igual', 0) for r in res)} igual / {sum(r.get('fidelidad', {}).get('difiere', 0) for r in res)} difiere · regla aplicada {sum(r.get('veces_regla') or 0 for r in res)} veces", flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_36_banco.json"), "w"), ensure_ascii=False, indent=1)

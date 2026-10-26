"""[P7-15] QUE DECISIONES CAMBIA EL CUADERNO. Replica (molde de `banco_P7_5.py`, UN SUBPROCESO POR VIDA, sin partidas ni llamadas) de las 80 vidas
de APRENDE de P7-14b, tal como se jugaron (pedir encendido, ojos apagados, el cuaderno que leyo ese dia). En CADA tic el cuerpo decide dos veces
sobre la misma escena y la misma memoria:
  - con su cuaderno (la decision del campo; se comprueba contra el diario), y
  - con el cuaderno que tendria BORRADO ese dia: vacio al empezar la partida, es decir, solo con los recuerdos de HOY (los de dias anteriores
    quitados). Todo lo demas igual: la escena, la memoria de la partida (se decide sobre una copia, para no tocarla), el pedido, el codigo.
Se apunta cada tic en que las dos decisiones difieren. Es una comparacion tic a tic sobre la vida que se vivio: dice donde el cuaderno cambia la
decision, no lo que habria pasado despues.
  python3 banco_P7_15.py            -> P7_15_decisiones.json
  python3 banco_P7_15.py --vida CLAVE (una vida, un proceso)"""
import collections, copy, glob, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_15_tmp")
def una(s, d, sl):
    import banco_P7_5 as B
    carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P714b_s{s}_d{d}_APRENDE_*"))[0])
    cuad = os.path.join(SAL, f"cuad_s{s}_d{d}_{sl}"); shutil.rmtree(cuad, ignore_errors=True); os.makedirs(cuad)
    if d > 1:
        for q in (10, 11): shutil.copy(os.path.join(AQUI, "P7_14b_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json"), os.path.join(cuad, f"cuaderno_P7_{q}.json"))
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS["APRENDE"].get(k, "0")
    os.environ["GEMV_P7_PIDE"] = "1"; os.environ["CUADERNO_DIR"] = cuad; os.environ["GEMV_OJOS"] = "0"        # como se jugo P7-14b
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    import mide_P6_29 as M
    import descubre_P7 as X
    import pide_P7 as J
    from cuaderno_P7 import Cuaderno
    _ap0 = X.aplica
    def _aplica(clase, registra=None):
        h = _ap0(clase, registra); J.aplica(clase, registra); return h
    X.aplica = _aplica
    def de_hoy(c):
        """el cuaderno de BORRADO ese dia: solo los recuerdos de hoy"""
        c2 = Cuaderno(c.criatura); c2.dia = c.dia; hoy = c.dia_actual()
        for o, dd in c.objetos.items():
            sits = {st_: [r for r in rec if int(r["dia"]) == hoy] for st_, rec in (dd.get("situaciones") or {}).items()}
            sits = {st_: rec for st_, rec in sits.items() if rec}
            if sits: c2.objetos[o] = {"situaciones": sits}
        return c2
    DIF = []; CNT = collections.Counter(); _d0 = M._DEC0
    def _dec(obs, mundo, mem, tick, bloqueos=None):
        c = X.ESTADO["cuaderno"]; el2 = None
        if c is not None:
            c2 = de_hoy(c); k1 = X.k_ganas(mundo); X.ESTADO["cuaderno"] = c2
            try:
                k2 = X.k_ganas(mundo); _, ra2 = _d0(copy.deepcopy(obs), mundo, copy.deepcopy(mem), tick, copy.deepcopy(bloqueos)); el2 = ra2.get("elegido")
            finally: X.ESTADO["cuaderno"] = c
        ac, ra = _d0(obs, mundo, mem, tick, bloqueos)
        if c is not None:
            CNT["tics"] += 1
            if el2 != ra.get("elegido"):
                you = obs.get("you") or {}
                DIF.append({"t": tick, "con_cuaderno": ra.get("elegido"), "sin_los_dias_anteriores": el2, "hp": you.get("hp"), "botiquines": X.kits_en(you, mundo), "k_ganas": round(k1, 4), "k_ganas_de_hoy": round(k2, 4), "n_cand": ra.get("n_cand")})
        return ac, ra
    M._DEC0 = _dec
    r = B.vida(carp, sl, "APRENDE", cuad)
    return {"serie": s, "dia": d, "slot": sl, "tics": r["tics"], "tics_comparados": CNT["tics"], "fidelidad": r["fidelidad"], "errores": len(r["errores"]), "distintos": DIF}
if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True)
    if "--vida" in sys.argv:
        s, d, sl = (int(x) for x in sys.argv[sys.argv.index("--vida") + 1].split("_")); json.dump(una(s, d, sl), open(os.path.join(SAL, f"dec_{s}_{d}_{sl}.json"), "w"), ensure_ascii=False)
    else:
        claves = [f"{s}_{d}_{sl}" for s in (1, 2) for d in range(1, 21) for sl in (10, 11)]
        def lanza(k):
            f = os.path.join(SAL, f"dec_{k}.json")
            if os.path.exists(f): os.remove(f)
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", k], capture_output=True, text=True, timeout=3600)
            return json.load(open(f)) if os.path.exists(f) else {"clave": k, "error": (r.stderr or r.stdout)[-500:]}
        with ThreadPoolExecutor(8) as ex: R = list(ex.map(lanza, claves))
        err = [r for r in R if r.get("error")]
        if err: print("ERRORES", len(err), err[0]["clave"], err[0]["error"][-400:])
        json.dump([r for r in R if not r.get("error")], open(os.path.join(AQUI, "P7_15_decisiones.json"), "w"), ensure_ascii=False, indent=0)
        fid = collections.Counter()
        for r in R:
            for k_, n in (r.get("fidelidad") or {}).items(): fid[k_] += n
        print("vidas", len(R) - len(err), "· fidelidad de la decision del campo", dict(fid), "· tics comparados", sum(r.get("tics_comparados", 0) for r in R), "· tics con decision distinta", sum(len(r.get("distintos", [])) for r in R))

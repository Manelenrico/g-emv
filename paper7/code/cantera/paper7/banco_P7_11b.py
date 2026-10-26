"""[P7-11] LA FILA QUE PAGA CADA USO Y CADA REGALO. El diario guarda las filas de cada candidato solo uno de cada 24 tics; para leerlas en los tics
en que el cuerpo decidio usar o regalar un botiquin (lista de `P7_11_vidas.json`) se replica cada vida con el molde de `banco_P7_5.py` (UN
SUBPROCESO POR VIDA; sin partidas ni llamadas), con los interruptores de su brazo y, en APRENDE, el cuaderno que leyo ese dia (el de fin del dia
anterior de su serie en `P7_10_res/`; para el dia 4 de la serie 1, asiento 11, el rehecho que viajo). En esos tics se guarda lo que devuelve
`D.decide` entero (d, vida prevista y filas de cada candidato) y lo que cree el cuerpo (`k_creencia`, `k_ganas`, ignorancia, cura imaginada).
`descubre_P7.py` es el de hoy; los brazos fijos se jugaron con el del sello (ver informe, seccion 1).
  python3 banco_P7_11b.py                 -> P7_11_filas.json
  python3 banco_P7_11b.py --vida CLAVE    (un proceso: una vida)"""
import glob, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
SAL = os.path.join(AQUI, "_P7_11_tmp")
def tics_de(v): return sorted({u["decision"]["t"] for u in v["usos"] if u.get("decision")} | {g["t_dec"] for g in v["regala"]})
def una(clave):
    import banco_P7_5 as B
    V = json.load(open(os.path.join(AQUI, "P7_11_vidas.json"))); v = V[clave]; TICS = set(tics_de(v)); s, d, b, sl = v["serie"], v["dia"], v["brazo"], v["slot"]
    carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P710_s{s}_d{d}_{b}_*"))[0])
    cuad = os.path.join(SAL, "cuad_" + clave); shutil.rmtree(cuad, ignore_errors=True); os.makedirs(cuad)
    if b == "APRENDE" and d > 1:
        for q in (10, 11):
            limpio = os.path.join(AQUI, "P7_10_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}_limpio.json"); normal = os.path.join(AQUI, "P7_10_res", f"cuaderno_s{s}_d{d - 1}_APRENDE_{q}.json")
            shutil.copy(limpio if os.path.exists(limpio) else normal, os.path.join(cuad, f"cuaderno_P7_{q}.json"))
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO"): os.environ[k] = B.BRAZOS[b if b != "TECHO" else "TECHO_SITIO"].get(k, "0")
    os.environ["CUADERNO_DIR"] = cuad
    import mide_P6_29 as M
    import descubre_P7 as X
    REG = {}; _d0 = M._DEC0
    def _dec(obs, mundo, mem, tick, bloqueos=None):
        ac, ra = _d0(obs, mundo, mem, tick, bloqueos)
        if tick in TICS:
            uh = X.ESTADO.get("ultima_heal")
            REG[tick] = {"elegido": ra.get("elegido"), "candidatos": ra.get("candidatos"), "k_creencia": X.k_creencia(mundo), "k_ganas": X.k_ganas(mundo), "ignorancia": X.ignorancia_de(mundo),
                         "cura_imaginada": (uh[1] if (uh and uh[0] == tick) else None), "esperanza": X.esperanza_cuerpo(mundo), "cura_catalogo": X.cura_catalogo(mundo)}
        return ac, ra
    M._DEC0 = _dec
    r = B.vida(carp, sl, b if b != "TECHO" else "TECHO_SITIO", cuad)
    return {"clave": clave, "fidelidad": r["fidelidad"], "desacuerdos": len(r["desacuerdos"]), "errores": len(r["errores"]), "tics": {str(t): REG.get(t) for t in sorted(TICS)}}
if __name__ == "__main__":
    os.makedirs(SAL, exist_ok=True)
    if "--vida" in sys.argv:
        k = sys.argv[sys.argv.index("--vida") + 1]; json.dump(una(k), open(os.path.join(SAL, f"filas_{k}.json"), "w"), ensure_ascii=False)
    else:
        V = json.load(open(os.path.join(AQUI, "P7_11_vidas.json"))); claves = [k for k, v in V.items() if tics_de(v)]
        def lanza(k):
            f = os.path.join(SAL, f"filas_{k}.json")
            if os.path.exists(f): os.remove(f)
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", k], capture_output=True, text=True, timeout=1800)
            return json.load(open(f)) if os.path.exists(f) else {"clave": k, "error": (r.stderr or r.stdout)[-500:]}
        with ThreadPoolExecutor(8) as ex: R = list(ex.map(lanza, claves))
        json.dump({r["clave"]: r for r in R}, open(os.path.join(AQUI, "P7_11_filas.json"), "w"), ensure_ascii=False)
        import collections
        fid = collections.Counter()
        for r in R:
            for k_, n in (r.get("fidelidad") or {"ERROR": 1}).items(): fid[k_] += n
        print("vidas replicadas", len(R), "· errores", sum(1 for r in R if r.get("error")), "· fidelidad", dict(fid), "· vidas con algun desacuerdo", sum(1 for r in R if r.get("desacuerdos")))
        for r in R:
            if r.get("error"): print(r["clave"], r["error"][-300:]); break

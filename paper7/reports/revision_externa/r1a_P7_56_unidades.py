"""1a · R2 de P7-56 con otras unidades. Ejecuta la logica sellada de erratas_P7_56.py (lectura de diarios, verdad_sello, r2) sin su
escritura de P7_56_erratas.json, y recalcula el ee agrupando por criatura (serie, asiento) y por serie. Solo lectura."""
import json, math, os, statistics as st
from comun import P7
src = open(os.path.join(P7, "erratas_P7_56.py")).read()
src = src.replace("os.path.dirname(os.path.abspath(__file__))", repr(P7))
ns = {"__name__": "erratas_P7_56_revision"}; exec(src[:src.index("\nR = {")], ns)
filas, r2 = ns["filas"], ns["r2"]
def cl(F, clave, key):
    VE = [f for f in F if f[clave]]; FA = [f for f in F if not f[clave]]
    mV = st.mean([f["conf"] for f in VE]); mF = st.mean([f["conf"] for f in FA]); g = {}
    for f in VE: g[key(f)] = g.get(key(f), 0) + (f["conf"] - mV) / len(VE)
    for f in FA: g[key(f)] = g.get(key(f), 0) - (f["conf"] - mF) / len(FA)
    G = len(g); e = math.sqrt(G / (G - 1) * sum(x * x for x in g.values()))
    return {"dif": round(mV - mF, 4), "ee_agrupado": round(e, 4), "veces": round((mV - mF) / e, 1), "G": G}
def porunidad(F, clave, key):
    U = {}
    for f in F: U.setdefault(key(f), {"V": [], "F": []})["V" if f[clave] else "F"].append(f["conf"])
    d = [st.mean(u["V"]) - st.mean(u["F"]) for u in U.values() if u["V"] and u["F"]]
    m = st.mean(d); e = st.stdev(d) / math.sqrt(len(d))
    return {"dif_media": round(m, 4), "ee": round(e, 4), "veces": round(m / e, 1), "n": len(d),
            "detalle": {str(k): (len(u["V"]), len(u["F"]), round(st.mean(u["V"]), 3) if u["V"] else None, round(st.mean(u["F"]), 3) if u["F"] else None) for k, u in sorted(U.items())}}
for nombre, fm in (("con_todas", False), ("sin_marcadas", True)):
    F = filas(fm)
    for clave in ("sello", "original"):
        print(nombre, clave, "por evaluacion", {k: r2(F, clave)[k] for k in ("n_verdad", "n_falsa", "media_verdad", "media_falsa", "dif", "ee", "ee_veces")})
        print("   agrupado por criatura", cl(F, clave, lambda f: (f["S"], f["sl"])))
        print("   agrupado por serie   ", cl(F, clave, lambda f: f["S"]))
        print("   media por criatura   ", porunidad(F, clave, lambda f: (f["S"], f["sl"])))
        print("   media por serie      ", porunidad(F, clave, lambda f: f["S"]))

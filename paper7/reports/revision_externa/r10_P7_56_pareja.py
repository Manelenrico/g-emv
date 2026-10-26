"""10 · R2 de P7-56 (cuenta corregida, verdad_sello) con la PAREJA como unidad. En CON_RAZON cada serie es una pareja (asientos 10 y 11 en la misma partida
cada dia, y con los recuerdos compartidos): pareja = serie. Ejecuta la logica sellada de erratas_P7_56.py sin su escritura. Solo lectura."""
import json, math, os, statistics as st
from comun import P7
src = open(os.path.join(P7, "erratas_P7_56.py")).read().replace("os.path.dirname(os.path.abspath(__file__))", repr(P7))
ns = {"__name__": "erratas_P7_56_revision"}; exec(src[:src.index("\nR = {")], ns)
filas, V, E = ns["filas"], ns["V"], ns["E"]
# comprobacion: las dos hermanas de cada (serie, dia, CON_RAZON) salen de la misma partida (una peticion, una carpeta)
pet = [p for p in E["peticiones"] if p["brazo"] == "CON_RAZON" and p["estado"] == "completed"]
claves = [(p["serie"], p["dia"]) for p in pet]
print("partidas CON_RAZON completadas", len(pet), "| (serie, dia) repetidos", len(claves) - len(set(claves)),
      "| con las dos hermanas leidas", sum(1 for p in pet if (p["serie"], p["dia"], "CON_RAZON", 10) in V and (p["serie"], p["dia"], "CON_RAZON", 11) in V))
def t_p(t, df):
    # p de una cola de la t de Student (integracion numerica simple; df pequeno)
    import math
    f = lambda x: math.gamma((df + 1) / 2) / (math.sqrt(df * math.pi) * math.gamma(df / 2)) * (1 + x * x / df) ** (-(df + 1) / 2)
    n = 200000; hi = 2000.0; h = (hi - t) / n
    return sum(f(t + (i + .5) * h) for i in range(n)) * h
for nombre, fm in (("con_todas", False), ("sin_marcadas", True)):
    F = filas(fm); P = {}
    for f in F: P.setdefault(f["S"], {}).setdefault(f["sl"], {"V": [], "F": []})["V" if f["sello"] else "F"].append(f["conf"])
    # (i) pareja con sus evaluaciones juntas: media tras verdad - media tras falsa
    d1 = {S: st.mean(x for h in P[S].values() for x in h["V"]) - st.mean(x for h in P[S].values() for x in h["F"]) for S in P}
    # (ii) pareja como media de las diferencias de sus dos hermanas (cada hermana con verdad y falsa)
    d2 = {S: st.mean([st.mean(h["V"]) - st.mean(h["F"]) for h in P[S].values() if h["V"] and h["F"]]) for S in P}
    for etiqueta, d in (("evaluaciones de la pareja juntas", d1), ("media de las dos hermanas", d2)):
        xs = list(d.values()); m = st.mean(xs); e = st.stdev(xs) / math.sqrt(len(xs)); t = m / e
        print(nombre, "| pareja:", etiqueta, "| por pareja", {f"s{S}": round(v, 3) for S, v in sorted(d.items())},
              "| media", round(m, 3), "ee", round(e, 3), "veces", round(t, 2), "n", len(xs), "| p una cola (t, gl 2)", round(t_p(t, len(xs) - 1), 4))

"""[P7-45, encargo de Manel 11-oct] LA CURVA DE LATENCIA DE APRENDE PRUDENTE FRENTE AL CUADERNO, con las tres series (y, al lado, APRENDE valiente y SIN):
por dia y serie, mediana de ms por decision (media de los dos asientos), % de decisiones sobre el tic y tamano del cuaderno con el que arranca el dia (recuerdos + apuntes);
Spearman por serie y con las tres series juntas (n = 57 dias), y la pendiente de la recta de minimos cuadrados (ms por cada 100 apuntes). Lee P7_43_latencia_s{1,2,3}.json
(latencia_P7_43.py). -> P7_45_latencia.json y P7_45_latencia.png (matplotlib, de los datos crudos).  python3 latencia_P7_45.py"""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); CAD = ("APRENDE_p", "APRENDE_v", "SIN"); ET = {"APRENDE_p": "APRENDE prudente", "APRENDE_v": "APRENDE valiente", "SIN": "SIN EMOCIÓN"}
L = {S: json.load(open(os.path.join(AQUI, f"P7_43_latencia_s{S}.json"))) for S in (1, 2, 3)}


def rangos(v): s_ = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); [r.__setitem__(i, k) for k, i in enumerate(s_)]; return r
def spearman(x, y):
    if len(x) < 3: return None
    rx, ry = rangos(x), rangos(y); mx, my = st.mean(rx), st.mean(ry); num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(num / den, 2) if den else None
def pendiente(x, y):
    mx, my = st.mean(x), st.mean(y); den = sum((a - mx) ** 2 for a in x)
    return (sum((a - mx) * (b - my) for a, b in zip(x, y)) / den) if den else None


R = {}
for var in CAD:
    pts = []                                                     # (serie, dia, cuaderno, mediana, p95, sobre %)
    for S in (1, 2, 3):
        for d in range(2, 21):
            x = L[S]["por_dia"][var][str(d)]
            if x["mediana"] is None or x["recuerdos"] is None: continue
            pts.append((S, d, x["recuerdos"] + x["apuntes"], x["mediana"], x["p95"], x["sobre_pct"]))
    por_serie = {}
    for S in (1, 2, 3):
        p = [q for q in pts if q[0] == S]
        por_serie[S] = {"n": len(p), "spearman_mediana": spearman([q[2] for q in p], [q[3] for q in p]), "spearman_sobre": spearman([q[2] for q in p], [q[5] for q in p]),
                        "cuaderno_d2": (p[0][2] if p else None), "cuaderno_d20": (p[-1][2] if p else None), "mediana_min": (min(q[3] for q in p) if p else None), "mediana_max": (max(q[3] for q in p) if p else None)}
    pend = pendiente([q[2] for q in pts], [q[3] for q in pts])
    R[var] = {"n": len(pts), "por_serie": por_serie, "juntas": {"spearman_mediana": spearman([q[2] for q in pts], [q[3] for q in pts]), "spearman_sobre": spearman([q[2] for q in pts], [q[5] for q in pts]),
              "ms_por_100_apuntes": (round(100 * pend, 3) if pend is not None else None), "mediana_media": round(st.mean(q[3] for q in pts), 2), "sobre_media_pct": round(st.mean(q[5] for q in pts), 3),
              "dias_sobre_1pct": sum(1 for q in pts if q[5] >= 1.0)}, "puntos": pts}
json.dump(R, open(os.path.join(AQUI, "P7_45_latencia.json"), "w"), ensure_ascii=False, indent=1)
for var in CAD:
    r = R[var]; print(var, "n", r["n"], "juntas", r["juntas"], "por serie", {S: (v["spearman_mediana"], v["spearman_sobre"], v["cuaderno_d20"]) for S, v in r["por_serie"].items()})

import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(13, 4), sharey=True); mk = {1: "o", 2: "s", 3: "^"}
for i, var in enumerate(CAD):
    for S in (1, 2, 3):
        p = [q for q in R[var]["puntos"] if q[0] == S]
        ax[i].scatter([q[2] for q in p], [q[3] for q in p], marker=mk[S], s=28, alpha=0.75, label=f"serie {S}")
    ax[i].set_title(f"{ET[var]} · Spearman {R[var]['juntas']['spearman_mediana']} (n = {R[var]['n']})"); ax[i].set_xlabel("cuaderno al arrancar el día (recuerdos + apuntes)"); ax[i].grid(alpha=0.3)
ax[0].set_ylabel("mediana de ms por decisión (media de los 2 asientos)"); ax[0].legend()
fig.suptitle("P7-45 · latencia por día frente al tamaño del cuaderno, días 2-20 de las tres series (P7_43_latencia_s1-3.json)"); fig.tight_layout()
fig.savefig(os.path.join(AQUI, "P7_45_latencia.png"), dpi=110); print("P7_45_latencia.png")

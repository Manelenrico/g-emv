"""[P7-34] Las figuras del campo, de P7_34_datos.json (SELLO_P7_34.md, "Sin prediccion, solo medida"):
  P7_34_fig_cuatro.png   creencia, ignorancia y ganas (k) de las cuatro cosas por dia, APRENDE (media de las 4 criaturas; las que tienen valor ese dia), con BORRADO en punteado
  P7_34_fig_cogidas.png  cogidas de lo util (botiquin + racion) frente a lo inutil (red + camuflaje) por dia y brazo (media por vida del dia)
  P7_34_fig_puesto.png   el puesto por dia en los tres brazos (partidas con corte fuera)"""
import json, os, statistics as st
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__)); V = [v for v in json.load(open(os.path.join(AQUI, "P7_34_datos.json"))) if not v.get("sin_diario")]
COSAS = ("botiquin", "racion", "red", "camuflaje"); COL = {"botiquin": "#B22222", "racion": "#e6a000", "red": "#1f77b4", "camuflaje": "#2ca02c"}
corte = {(v["serie"], v["dia"], v["brazo"]) for v in V if v.get("parcial")}


def media_dia(brazo, dia, f):
    xs = [f(v) for v in V if v["brazo"] == brazo and v["dia"] == dia]; xs = [x for x in xs if x is not None]
    return st.mean(xs) if xs else None


def serie(brazo, f): return [(d, media_dia(brazo, d, f)) for d in range(1, 21)]
def pinta(ax, brazo, f, o, estilo):
    s = [(d, x) for d, x in serie(brazo, f) if x is not None]
    if s: ax.plot([d for d, _ in s], [x for _, x in s], estilo, ms=3, color=COL[o], lw=1.2 if brazo == "APRENDE" else 0.8, alpha=0.95 if brazo == "APRENDE" else 0.5, label=(f"{o}" if brazo == "APRENDE" else None))


fig, ax = plt.subplots(3, 1, figsize=(10, 9), dpi=110)
for o in COSAS:
    pinta(ax[0], "APRENDE", lambda v, o=o: v["al_acabar"][o]["creencia"], o, "-o"); pinta(ax[0], "BORRADO", lambda v, o=o: v["al_acabar"][o]["creencia"], o, ":s")
    pinta(ax[1], "APRENDE", lambda v, o=o: v["al_acabar"][o]["ignorancia"], o, "-o"); pinta(ax[1], "BORRADO", lambda v, o=o: v["al_acabar"][o]["ignorancia"], o, ":s")
    pinta(ax[2], "APRENDE", lambda v, o=o: ((v.get("k_al_acabar") or {}).get(o)), o, "-o"); pinta(ax[2], "BORRADO", lambda v, o=o: ((v.get("k_al_acabar") or {}).get(o)), o, ":s")
ax[0].axhline(0, color="#888", lw=0.6); ax[0].set_title("creencia de cada cosa al cerrar el día (cuerpo, sin cortes; APRENDE en trazo continuo, BORRADO punteado; media de las criaturas con valor)", fontsize=9)
ax[1].set_ylim(0, 1.02); ax[1].set_title("ignorancia al cerrar el día", fontsize=9); ax[2].set_ylim(bottom=0); ax[2].set_title("ganas (k) de cada cosa al cerrar el día (último registro P7_33_k)", fontsize=9)
for a in ax: a.set_xlim(0.5, 20.5)
ax[2].set_xlabel("día"); ax[0].legend(fontsize=7, ncol=4); fig.suptitle("P7-34 · las cuatro cosas, día a día", fontsize=10); fig.tight_layout(); fig.savefig(os.path.join(AQUI, "P7_34_fig_cuatro.png")); plt.close(fig)

fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), dpi=110, sharey=True)
for i, b in enumerate(("TECHO", "BORRADO", "APRENDE")):
    for et, f, c in (("útil (botiquín + ración)", lambda v: v["coge"]["botiquin"] + v["coge"]["racion"], "#B22222"), ("inútil (red + camuflaje)", lambda v: v["coge"]["red"] + v["coge"]["camuflaje"], "#1f77b4")):
        s = [(d, x) for d, x in serie(b, f) if x is not None]
        ax[i].plot([d for d, _ in s], [x for _, x in s], "-o", ms=3, color=c, label=et)
    ax[i].set_title(f"{b}: cogidas por vida y día", fontsize=9); ax[i].set_xlabel("día"); ax[i].set_xlim(0.5, 20.5)
ax[0].set_ylabel("cogidas por vida"); ax[0].legend(fontsize=7); fig.suptitle("P7-34 · lo útil frente a lo inútil", fontsize=10); fig.tight_layout(); fig.savefig(os.path.join(AQUI, "P7_34_fig_cogidas.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 4.2), dpi=110)
for b, c in (("TECHO", "#444"), ("BORRADO", "#1f77b4"), ("APRENDE", "#B22222")):
    xs = []; ys = []
    for d in range(1, 21):
        p = [v["puesto"] for v in V if v["brazo"] == b and v["dia"] == d and v.get("puesto") is not None and (v["serie"], d, b) not in corte]
        if p: xs.append(d); ys.append(st.mean(p))
    ax.plot(xs, ys, "-o", ms=4, color=c, label=f"{b} (media de las vidas del día)")
ax.set_xlabel("día"); ax.set_ylabel("puesto (1 mejor, 16 peor)"); ax.invert_yaxis(); ax.set_xlim(0.5, 20.5); ax.legend(fontsize=8); ax.set_title("P7-34 · el puesto por día en los tres brazos (las partidas con corte, fuera)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, "P7_34_fig_puesto.png")); plt.close(fig); print("figuras hechas")

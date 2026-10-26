"""[P7-30, copia de figuras_P7_24] Las figuras del campo, de P7_30_vidas.json: creencia e ignorancia de cada objeto por dia (APRENDE: las 4 criaturas; BORRADO: lo aprendido dentro del dia, por criatura)
y el puesto por dia en los tres brazos (media de las 4 vidas del dia; las partidas con corte, fuera). -> P7_30_fig_creencias.png, P7_30_fig_puesto.png"""
import json, os, statistics as st
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__)); V = json.load(open(os.path.join(AQUI, "P7_30_vidas.json"))); R = json.load(open(os.path.join(AQUI, "P7_30_resumen.json")))
corte = {tuple(x) for x in R["partidas_con_corte"]}
fig, ax = plt.subplots(2, 2, figsize=(11, 7.5), dpi=110); col = {"APRENDE": "#B22222", "BORRADO": "#1f77b4"}
for j, o in enumerate(("botiquin", "racion")):
    for b in ("APRENDE", "BORRADO"):
        for s in (1, 2):
            for sl in (10, 11):
                vs = sorted([v for v in V.values() if v["brazo"] == b and v["serie"] == s and v["slot"] == sl and not v.get("sin_diario")], key=lambda v: v["dia"])
                cre = [(v["dia"], ((v["al_acabar"][o]["creencia"].get("dentro") if o == "botiquin" else max([x for x in v["al_acabar"][o]["creencia"].values() if x is not None] or [None])) if v["al_acabar"][o]["creencia"] else None)) for v in vs]
                ign = [(v["dia"], v["al_acabar"][o]["ignorancia"]) for v in vs]
                ax[0][j].plot([d for d, c in cre if c is not None], [c for d, c in cre if c is not None], "-o" if b == "APRENDE" else ":s", ms=3, lw=1.2 if b == "APRENDE" else 0.8, color=col[b], alpha=0.9 if b == "APRENDE" else 0.6, label=f"{b} s{s}·{sl}")
                ax[1][j].plot([d for d, c in ign if c is not None], [c for d, c in ign if c is not None], "-o" if b == "APRENDE" else ":s", ms=3, lw=1.2 if b == "APRENDE" else 0.8, color=col[b], alpha=0.9 if b == "APRENDE" else 0.6)
    ax[0][j].axhline({"botiquin": 50, "racion": 15}[o], color="#888", lw=0.8, ls="--"); ax[0][j].axhline(0.8 * {"botiquin": 50, "racion": 15}[o], color="#bbb", lw=0.6, ls=":")
    ax[0][j].set_title(f"creencia del {o} al cerrar el día" + (" (dentro del círculo)" if o == "botiquin" else " (la mayor situación)"), fontsize=9); ax[1][j].set_title(f"ignorancia del {o} al cerrar el día", fontsize=9)
    ax[1][j].set_ylim(0, 1.02); ax[1][j].set_xlabel("día"); ax[0][j].set_xlim(0.5, 20.5); ax[1][j].set_xlim(0.5, 20.5)
ax[0][0].legend(fontsize=6, ncol=2); fig.suptitle("P7-24 · nacer sin saber: lo que aprende cada criatura, día a día (APRENDE: el cuaderno viaja; BORRADO: cada día desde cero)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, "P7_30_fig_creencias.png")); plt.close(fig)
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=110)
for b, c in (("TECHO", "#444"), ("BORRADO", "#1f77b4"), ("APRENDE", "#B22222")):
    xs = []; ys = []
    for d in range(1, 21):
        p = [v["puesto"] for v in V.values() if v["brazo"] == b and v["dia"] == d and v.get("puesto") is not None and (v["serie"], d, b) not in corte]
        if p: xs.append(d); ys.append(st.mean(p))
    ax.plot(xs, ys, "-o", ms=4, color=c, label=f"{b} (media de las vidas del día)")
ax.set_xlabel("día"); ax.set_ylabel("puesto (1 mejor, 16 peor)"); ax.invert_yaxis(); ax.set_xlim(0.5, 20.5); ax.legend(fontsize=8); ax.set_title("P7-24 · el puesto por día en los tres brazos (las partidas con corte, fuera)", fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, "P7_30_fig_puesto.png")); plt.close(fig); print("figuras hechas")

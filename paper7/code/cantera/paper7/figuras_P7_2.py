"""[P7-2] Figura de las curvas de la creencia: por objeto y situacion (6 paneles), los dos asientos en orden natural, la banda
(minimo-maximo de los 20 ordenes al azar), el techo (media real del diario para esa situacion y asiento) y el suelo (catalogo)."""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_2_curvas.json")))["principal"]
CLAVES = [("botiquin", "dentro", "botiquín, dentro del círculo"), ("botiquin", "fuera", "botiquín, fuera del círculo"), ("bow", "con municion", "arco, con munición"), ("bow", "sin municion", "arco, sin munición"), ("blowgun", "con municion", "cerbatana, con munición"), ("blowgun", "sin municion", "cerbatana, sin munición")]
COL = {10: "#B22222", 11: "#1f3a93"}
fig, axs = plt.subplots(3, 2, figsize=(7.2, 7.8), dpi=300); dias = list(range(1, 41))
for ax, (obj, sit, tit) in zip(axs.flat, CLAVES):
    for a in (10, 11):
        p = R[f"{obj}/{sit}/{a}"]
        ax.fill_between(dias, p["banda_p10"], p["banda_p90"], color=COL[a], alpha=0.12, lw=0)
        ax.plot(dias, p["curva_natural"], color=COL[a], lw=1.3, label=f"asiento {a} (orden natural; {p['experiencias_total']} experiencias)")
        if p["techo_media_real"] is not None: ax.axhline(p["techo_media_real"], color=COL[a], lw=0.8, ls=":", label=f"media real del diario, asiento {a}: {p['techo_media_real']:.1f}")
        for d, c in zip(dias, p["experiencias_por_dia"]):
            if c: ax.plot([d], [p["curva_natural"][d - 1]], marker="o", ms=2.2, color=COL[a], lw=0)
    ax.axhline(R[f"{obj}/{sit}/10"]["suelo_catalogo"], color="#444", lw=0.8, ls="--", label=f"catálogo: {R[f'{obj}/{sit}/10']['suelo_catalogo']:g}")
    ax.set_title(tit, fontsize=8, loc="left"); ax.set_xlim(1, 40); ax.set_ylim(bottom=0); ax.tick_params(labelsize=6.5); ax.set_xlabel("día (semilla, orden creciente)", fontsize=6.5); ax.set_ylabel("creencia (puntos)", fontsize=6.5)
    ax.legend(fontsize=5, loc="best", frameon=True, framealpha=0.85, edgecolor="none")
fig.text(0.01, 0.004, "Línea: creencia al acabar cada día (orden natural); puntos: días con experiencia; banda: mínimo-máximo de los 20 órdenes al azar (semilla de barajado %d).\nPunteado: media real del diario para esa situación y asiento; raya: el catálogo. Datos: P7_2_curvas.json." % json.load(open(os.path.join(AQUI, "P7_2_curvas.json")))["semilla_barajado"], fontsize=5.2, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(os.path.join(AQUI, "P7_2_curvas.png")); print("P7_2_curvas.png")

"""[P8] Prompt 171, figura 1: el mapa del valle, pulido. Es figura1_valle_170.py (el dibujo de valle_mapa.py, prompt 159, en el turno 0 de la sequía 30182)
con tres cambios: sin criaturas ni sus nombres (en el turno 0 dos de ellas, B2 y C1, están encima de la puerta de su casa y la tapan, y A2 queda pegada al
borde de la suya: se quitan las ocho, que es lo más limpio); las cuatro puertas de casa, más grandes, para que se vean; y todos los textos salen de
rotulos_figuras.csv (estilo_171). Mismo tamaño (14,2 × 9,6 pulgadas), 300 ppp.
   python3 figura1_valle_171.py [--idioma es] -> figuras_171/fig1_valle_es.png y .pdf"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_171 as S
import valle_mapa as VM
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
V, P0, MAT, ARB, COL, SEL, plt = VM.V, VM.P0, VM.MAT, VM.ARB, VM.COL, VM.SEL, S.plt
NOM = "fig1_valle"


if __name__ == "__main__":
    ID = S.idioma(); R = S.Rotulos(ID); R.comprueba(("fig1.", "separador"))
    assert P0["turno"] == 0 and SEL == 30182
    # las cuatro puertas, cada una en una casilla de su casa y en un lado distinto (lo que se dibuja)
    assert all(V.puerta_casa[c] in V.casa_celdas[c] for c in V.casa_celdas) and len(set(V.puerta_casa.values())) == 4
    plt.rcParams.update({"font.size": 12})
    fig, ax = plt.subplots(figsize=(14.2, 9.6)); ax.imshow(VM.G.fondo, origin="upper"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0.5, V.W + 0.5); ax.set_ylim(V.H + 0.5, 0.5)
    caja = dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85)
    def txt(x, y, s, fs=11): ax.text(x, y, s, ha="center", va="center", fontsize=fs, bbox=caja, zorder=6)
    for c, cel in V.casa_celdas.items():
        xs = [p[0] for p in cel]; ys = [p[1] for p in cel]; txt(sum(xs) / len(xs), min(ys) - 1.0, R("fig1.casa", c=c), fs=9.5)
    PUERTA = dict(marker="s", s=80, c="white", edgecolors="black", linewidths=1.4, zorder=7)
    for c, p in V.puerta_casa.items(): ax.scatter(*p, **PUERTA)
    al = sorted(V.almacen_celdas); txt(sum(p[0] for p in al) / len(al), max(p[1] for p in al) + 1.5, R("fig1.almacen"), fs=10)
    huertos = sorted({V.huerto_de[q] for q in V.plantas_pos})
    for h in huertos:
        qs = [q for q in V.plantas_pos if V.huerto_de[q] == h]; ax.scatter([q[0] for q in qs], [q[1] for q in qs], marker="*", s=70, c="#6b8e23", zorder=5)
    ax.scatter([m[0] for m in MAT], [m[1] for m in MAT], marker="o", s=34, c=["#2e7d32" if m[3] == "bosque" else "#8d6e63" for m in MAT], edgecolors="white", linewidths=0.6, zorder=5)
    ax.scatter([a[0] for a in ARB], [a[1] for a in ARB], marker="^", s=120, c="#c2185b", edgecolors="black", linewidths=0.6, zorder=5)
    for k, q in V.entrada_camino.items(): ax.scatter(*q, marker="X", s=90, c="black", zorder=5)
    a0 = min(V.aldea); lado = max(p[0] for p in V.aldea) - a0[0] + 1
    txt(a0[0] + lado / 2 - 0.5, a0[1] + 3.0, R("fig1.plaza"))
    txt(V.W / 2 + 0.5, 3.4, R("fig1.zona_salvaje"), fs=12); txt(12.5, 40.0, R("fig1.bosque"), fs=12); txt(V.W / 2 + 0.5, 10.5, R("fig1.camino"), fs=10)
    hs = sorted(V.plantas_pos); txt(hs[0][0] + 1.5, hs[0][1] - 2.2, R("fig1.huerto"), fs=10)
    for p in V.cfg["puertas"]:
        ax.scatter([c[0] for c in p["celdas"]], [c[1] for c in p["celdas"]], marker="s", s=30, c=COL["p"], edgecolors="black", linewidths=0.6, zorder=5)
    L = lambda k: R(f"fig1.ley.{k}")
    ley = [Patch(color=COL["s"], label=L("zona_salvaje")), Patch(color=COL["b"], label=L("bosque")), Patch(color=COL["c"], label=L("camino")), Patch(color=COL["a"], label=L("plaza")),
           Patch(color=COL["k"], label=L("casa")), Patch(color=COL["m"], label=L("almacen")), Patch(color=COL["h"], label=L("huerto")),
           Line2D([], [], marker="s", ls="", color="white", markeredgecolor="black", markeredgewidth=1.4, markersize=9, label=L("puerta_casa")),
           Line2D([], [], marker="s", ls="", color=COL["p"], markeredgecolor="black", label=L("puerta_valle")),
           Line2D([], [], marker="*", ls="", color="#6b8e23", markersize=11, label=L("planta")),
           Line2D([], [], marker="o", ls="", color="#2e7d32", label=L("matorral_bosque")), Line2D([], [], marker="o", ls="", color="#8d6e63", label=L("matorral_salvaje")),
           Line2D([], [], marker="^", ls="", color="#c2185b", markeredgecolor="black", markersize=10, label=L("arbol")),
           Line2D([], [], marker="X", ls="", color="black", markersize=9, label=L("entrada_bestia"))]
    ax.legend(handles=ley, loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False, fontsize=11)
    fig.text(0.02, 0.015, R("fig1.nota", w=V.W, h=V.H, s=SEL), fontsize=9.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); rutas = S.guarda(fig, NOM, ID)
    falta = sorted(c for c in R.T if c.startswith("fig1.") and c not in R.usadas); assert not falta, falta
    print("hecho", rutas, "puertas", dict(V.puerta_casa))

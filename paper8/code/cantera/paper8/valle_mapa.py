"""[P8] Prompt 159, parte 2: la figura del valle, un mapa fijo sin criaturas, con cada zona rotulada en español y una leyenda corta, en los colores de los GIF
(reserva_v1/gif_rg69.COL, importado). La rejilla, las casas, las puertas de casa, el almacén, las plantas del huerto, la plaza (la aldea), los caminos, las puertas
del mapa y las entradas de la bestia salen del mundo (valle/mundo.py, Valle._construye_mapa, con config_valle.json, que es la que se jugó: misma huella). Los
matorrales y los sitios de los dos árboles dulces los pone la semilla: aquí, los de la sequía 30182 (la partida de los GIF), leídos del primer turno de su
mundo.jsonl.gz.
   python3 valle_mapa.py -> figuras/valle_mapa.png y .pdf"""
import gzip, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [AQUI, os.path.join(AQUI, "reserva_v1")]
os.environ["ESCALERA_MODO"] = "experimento"
import gif_rg69 as G
import evalua_escalera_v6 as ES
import mundo as MU
plt = G.plt; COL = G.COL; SEL = 30182
V = MU.Valle()
P0 = json.loads(gzip.open(os.path.join(ES.E6.ruta(ES.PROTA, "sequia", SEL), "mundo.jsonl.gz"), "rt", encoding="utf-8").readline())
MAT = P0["objetos"]["matorrales"]; ARB = [a[:2] for a in P0["arboles"]]
NOM_CASA = {"A": "casa A", "B": "casa B", "C": "casa C", "D": "casa D"}


if __name__ == "__main__":
    plt.rcParams.update({"font.size": 12})
    fig, ax = plt.subplots(figsize=(13, 9.6)); ax.imshow(G.fondo, origin="upper"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0.5, V.W + 0.5); ax.set_ylim(V.H + 0.5, 0.5)
    caja = dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85); txt = lambda x, y, s, **k: ax.text(x, y, s, ha="center", va="center", fontsize=k.pop("fs", 11), bbox=caja, zorder=6, **k)
    for c, cel in V.casa_celdas.items():
        xs = [p[0] for p in cel]; ys = [p[1] for p in cel]; txt(sum(xs) / len(xs), min(ys) - 1.0, NOM_CASA[c], fs=9.5)
    for c, p in V.puerta_casa.items(): ax.scatter(*p, marker="s", s=34, c="white", edgecolors="black", linewidths=1.0, zorder=7)
    al = sorted(V.almacen_celdas); txt(sum(p[0] for p in al) / len(al), max(p[1] for p in al) + 1.5, "almacén", fs=10)
    for h in {V.huerto_de[q] for q in V.plantas_pos}:
        qs = [q for q in V.plantas_pos if V.huerto_de[q] == h]; ax.scatter([q[0] for q in qs], [q[1] for q in qs], marker="*", s=70, c="#6b8e23", zorder=5)
    ax.scatter([m[0] for m in MAT], [m[1] for m in MAT], marker="o", s=34, c=["#2e7d32" if m[3] == "bosque" else "#8d6e63" for m in MAT], edgecolors="white", linewidths=0.6, zorder=5)
    ax.scatter([a[0] for a in ARB], [a[1] for a in ARB], marker="^", s=120, c="#c2185b", edgecolors="black", linewidths=0.6, zorder=5)
    for k, q in V.entrada_camino.items(): ax.scatter(*q, marker="X", s=90, c="black", zorder=5)
    a0 = min(V.aldea); lado = max(p[0] for p in V.aldea) - a0[0] + 1
    txt(a0[0] + lado / 2 - 0.5, a0[1] + 3.0, "plaza", fs=11)
    txt(V.W / 2 + 0.5, 3.4, "zona salvaje", fs=12); txt(12.5, 40.0, "bosque", fs=12); txt(V.W / 2 + 0.5, 10.5, "camino", fs=10)
    hs = sorted(V.plantas_pos); txt(hs[0][0] + 1.5, hs[0][1] - 2.2, "huerto", fs=10)
    for p in V.cfg["puertas"]:
        q = p["celdas"][0]; ax.scatter([c[0] for c in p["celdas"]], [c[1] for c in p["celdas"]], marker="s", s=30, c=COL["p"], edgecolors="black", linewidths=0.6, zorder=5)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    ley = [Patch(color=COL["s"], label="zona salvaje"), Patch(color=COL["b"], label="bosque"), Patch(color=COL["c"], label="camino"), Patch(color=COL["a"], label="plaza"),
           Patch(color=COL["k"], label="casa"), Patch(color=COL["m"], label="almacén"), Patch(color=COL["h"], label="huerto"),
           Line2D([], [], marker="s", ls="", color="white", markeredgecolor="black", label="puerta de casa"), Line2D([], [], marker="s", ls="", color=COL["p"], markeredgecolor="black", label="puerta del valle"),
           Line2D([], [], marker="*", ls="", color="#6b8e23", markersize=11, label="planta del huerto"),
           Line2D([], [], marker="o", ls="", color="#2e7d32", label="matorral del bosque"), Line2D([], [], marker="o", ls="", color="#8d6e63", label="matorral salvaje"),
           Line2D([], [], marker="^", ls="", color="#c2185b", markeredgecolor="black", markersize=10, label="sitio de árbol dulce"),
           Line2D([], [], marker="X", ls="", color="black", markersize=9, label="entrada de la bestia")]
    ax.legend(handles=ley, loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False, fontsize=11)
    fig.text(0.02, 0.015, f"Matorrales y árboles: los de la semilla {SEL} (los pone la semilla); lo demás es igual en todas las partidas. Rejilla de {V.W} × {V.H} casillas.", fontsize=9.5)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    for ext in ("png", "pdf"): fig.savefig(os.path.join(AQUI, "figuras", f"valle_mapa.{ext}"), dpi=200)
    print(len(MAT), "matorrales,", {z: sum(1 for m in MAT if m[3] == z) for z in ("bosque", "salvaje")}, "árboles", ARB, "puertas", [p["id"] for p in V.cfg["puertas"]], "entradas", V.entrada_camino)

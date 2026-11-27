"""[P8] Prompt 154, parte 2 (solo lee): tres figuras fijas para la sección de la escalera. Los cinco mundos abajo y tres barras por mundo (RG69r+voz, S69+voz,
P69+voz): la media de las 40 semillas (30161-30200) y su intervalo del 95 % (bootstrap de 10.000 con semilla 8, evalua_experimento_v6.boot, sobre las 40 partidas).
Los valores por partida, de evalua_escalera_v6.una (sus piezas y su caché, sin cambiar nada).
  A: vivas el día 40 (de 8) · B: empujones a otra criatura por partida · C: felicidad de la aldea, de 0 a 100 (la medida × 100).
Los colores, los tres primeros de la paleta de categorías de la guía de figuras (pasan la prueba de daltonismo); cada barra lleva además su leyenda.
   python3 figuras_escalera_paper8.py -> figuras/escalera_{A_vivas,B_empujones,C_felicidad}.png y .pdf, salida/figuras_escalera_paper8.json"""
import json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
os.environ["ESCALERA_MODO"] = "experimento"
import evalua_escalera_v6 as ES
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
boot = ES.boot; MUNDOS = ES.MUNDOS; SEM = ES.SEM; JUG = ES.JUG
RÓTULO = {"RG69rvoz": "decide con el motor", "S69voz": "decide sumando", "P69voz": "decide con la posición"}
COLOR = {"RG69rvoz": "#2a78d6", "S69voz": "#eb6834", "P69voz": "#1baf7a"}
NOMBRE_MUNDO = {"abundancia": "abundancia", "normal": "normal", "sequia": "sequía", "sequia_dura": "sequía dura", "bestias_crian": "bestias que crían"}
FIG = (("A_vivas", "vivas", 1, "vivas el día 40 (de 8)"), ("B_empujones", "empujones", 1, "empujones por partida"), ("C_felicidad", "feliz", 100, "felicidad de la aldea (0 a 100)"))


if __name__ == "__main__":
    T = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]
    with Pool(10) as p: R = {(r["v"], r["mu"], r["s"]): r for r in p.map(ES.una, T, chunksize=2)}
    plt.rcParams.update({"font.size": 15, "axes.spines.top": False, "axes.spines.right": False})
    os.makedirs(os.path.join(AQUI, "figuras"), exist_ok=True); OUT = {}
    for nom, k, esc, eje in FIG:
        fig, ax = plt.subplots(figsize=(11, 5.8)); an = 0.26; OUT[nom] = {}
        for j, v in enumerate(JUG):
            B = [boot([R[(v, mu, s)][k] * esc for s in SEM]) for mu in MUNDOS]; OUT[nom][v] = dict(zip(MUNDOS, B))
            xs = [i + (j - 1) * (an + 0.02) for i in range(len(MUNDOS))]; m = [b["media"] for b in B]
            ax.bar(xs, m, width=an, color=COLOR[v], label=RÓTULO[v], zorder=3)
            ax.errorbar(xs, m, yerr=[[b["media"] - b["lo"] for b in B], [b["hi"] - b["media"] for b in B]], fmt="none", ecolor="#333333", elinewidth=1.4, capsize=4, zorder=4)
        ax.set_xticks(range(len(MUNDOS))); ax.set_xticklabels([NOMBRE_MUNDO[mu] for mu in MUNDOS]); ax.set_ylabel(eje); ax.set_ylim(bottom=0)
        if k == "feliz": ax.set_ylim(0, 100)
        if k == "vivas": ax.set_ylim(0, 8.6)
        ax.grid(axis="y", color="#dddddd", linewidth=0.8, zorder=0); ax.legend(frameon=False, fontsize=13, loc="upper right", ncol=3, bbox_to_anchor=(1, 1.12))
        fig.tight_layout()
        for ext in ("png", "pdf"): fig.savefig(os.path.join(AQUI, "figuras", f"escalera_{nom}.{ext}"), dpi=200)
        plt.close(fig)
    json.dump(OUT, open(os.path.join(AQUI, "salida", "figuras_escalera_paper8.json"), "w"), ensure_ascii=False, indent=1)
    for nom in OUT: print(nom, {v: {mu: round(b["media"], 2) for mu, b in OUT[nom][v].items()} for v in JUG})

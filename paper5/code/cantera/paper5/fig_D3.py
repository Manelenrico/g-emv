"""[P5-1 D3] La pelicula de cada vida: una figura por asiento-partida.

Cinco franjas: vida, W contra su objetivo, R-CARENCIA, las tres tensiones del
motor y la d. SOLO LECTURA de `D_series.json`.
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, RAIZ)
from motor.model import DEFAULT_CONFIG                      # noqa: E402
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from alma.appraisal_zs_v42_exp import W_TARGET              # noqa: E402

ACENTO = "#C4450B"
TINTA, GRIS, REJILLA = "#111111", "#6E6E6E", "#DDDDDD"
COL = {"F": "#0B3E49", "R": "#C9A227", "S": "#9E5C96"}
IGNICION, AVISO = 481, 7297


def dibuja(k, s, salida):
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"],
        "font.size": 7.5, "axes.edgecolor": GRIS, "text.color": TINTA,
        "axes.labelcolor": TINTA, "xtick.color": GRIS, "ytick.color": GRIS,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white"})
    t = [x["t"] for x in s]
    fig, ax = plt.subplots(5, 1, figsize=(6.69, 6.2), dpi=300, sharex=True,
                           gridspec_kw={"hspace": 0.45, "left": 0.095,
                                        "right": 0.985, "top": 0.90,
                                        "bottom": 0.075})
    ax[0].plot(t, [x["hp"] for x in s], color=TINTA, lw=0.8)
    ax[0].set_ylabel("vida"); ax[0].set_ylim(0, 105)
    ax[1].plot(t, [x["W"] for x in s], color=COL["R"], lw=0.8)
    ax[1].axhline(W_TARGET, color=GRIS, lw=0.8, ls=(0, (3, 2)))
    ax[1].annotate(f"lo que el cuerpo pide: {W_TARGET:.0f}", xy=(t[0], W_TARGET),
                   xytext=(2, 2), textcoords="offset points", fontsize=6.5,
                   color=GRIS)
    ax[1].set_ylabel("W\n(lo que lleva)"); ax[1].set_ylim(0, W_TARGET * 1.12)
    ax[2].plot(t, [x["R-CARENCIA"] for x in s], color=ACENTO, lw=0.8)
    ax[2].axhline(0.1, color=GRIS, lw=0.8, ls=(0, (1, 2)))
    ax[2].annotate("el suelo de la calma: 0,1", xy=(t[0], 0.1), xytext=(2, 3),
                   textcoords="offset points", fontsize=6.5, color=GRIS)
    ax[2].set_ylabel("carencia"); ax[2].set_ylim(0, 1.05)
    for e in ("F", "R", "S"):
        ax[3].plot(t, [x["n" + e] for x in s], color=COL[e], lw=0.7, label=e)
    ax[3].set_ylabel("tensión\n(lo que tira)")
    ax[3].legend(frameon=False, ncol=3, fontsize=6.5, loc="upper left",
                 bbox_to_anchor=(0.0, 1.30), borderaxespad=0.0)
    ax[4].plot(t, [x["d_estado"] for x in s], color=TINTA, lw=0.8,
               label="del estado de ahora")
    dd = [(x["t"], x["d_elegido"]) for x in s if x["d_elegido"] is not None]
    if dd:
        ax[4].plot([a for a, _ in dd], [b for _, b in dd], color=ACENTO,
                   lw=0.5, alpha=0.75, label="del futuro que elige")
    ax[4].set_ylabel("d"); ax[4].set_xlabel("instantes de partida (24 por segundo)")
    ax[4].legend(frameon=False, ncol=2, fontsize=6.5, loc="upper left",
                 bbox_to_anchor=(0.0, 1.30), borderaxespad=0.0)
    for a in ax:
        a.grid(axis="y", color=REJILLA, lw=0.4)
        a.set_axisbelow(True)
        for lado in ("top", "right"):
            a.spines[lado].set_visible(False)
        if AVISO >= t[0] and AVISO <= t[-1]:
            a.axvline(AVISO, color=GRIS, lw=0.7, ls=(0, (4, 3)))
    if AVISO >= t[0] and AVISO <= t[-1]:
        ax[0].annotate("avisa el anillo", xy=(AVISO, 100), xytext=(4, -8),
                       textcoords="offset points", fontsize=6.5, color=GRIS)
    part, asi = k.split("/")
    n = f"{len(s):,}".replace(",", ".")
    fig.suptitle(f"Una vida entera · {part.replace('P5_', 'partida ')}, "
                 f"asiento {asi} · {n} instantes vivos",
                 fontsize=10, x=0.012, ha="left", y=0.975)
    fig.text(0.012, 0.935,
             "del tic 481, cuando baja del pedestal, al último que vio · "
             "las tensiones son las del motor, reconstruidas del propio diario",
             fontsize=7, color=GRIS, ha="left")
    fig.savefig(salida)
    plt.close(fig)
    return salida


def main():
    S = json.load(open(os.path.join(AQUI, "D_series.json")))
    os.makedirs(os.path.join(AQUI, "figD"), exist_ok=True)
    for k, s in sorted(S.items()):
        nom = k.replace("/", "_a") + ".png"
        p = dibuja(k, s, os.path.join(AQUI, "figD", nom))
        print("escrito:", os.path.relpath(p, RAIZ), f"({len(s):,} puntos)")


if __name__ == "__main__":
    main()

"""[P8] Prompt 170: lo común de las cinco figuras del paper ocho (figura1_valle_170.py … figura5_tres_maneras_170.py). El estilo es el de
figuras_escalera_paper8.py (escalera_A_vivas, _B_empujones, _C_felicidad): letra 15, sin marco arriba ni a la derecha, rejilla horizontal gris, barras con su
intervalo del 95 % (E6.boot: bootstrap de 10.000 remuestreos con semilla 8 sobre las 40 partidas de cada mundo), leyenda arriba sin marco. Cambia el guardado:
PNG a 300 puntos por pulgada y PDF, en figuras/. Los colores de las tres maneras de decidir son los de la escalera (FE.COLOR): azul el motor, naranja la
suma, verde la posición. Al lado de cada figura, un .txt con los números que dibuja, de dónde sale cada uno y un pie propuesto."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
os.environ["ESCALERA_MODO"] = "experimento"
import figuras_escalera_paper8 as FE
ES = FE.ES; E6 = ES.E6; boot = ES.boot; plt = FE.plt; MUNDOS = ES.MUNDOS; SEM = ES.SEM; NOMBRE_MUNDO = FE.NOMBRE_MUNDO; DIA = E6.DIA
FIG = os.path.join(AQUI, "figuras"); DPI = 300
ROT = {"RG69rvoz": "la criatura completa", "tonto": "el tonto", "recolector": "el recolector", "RG68r": "la criatura de antes", "RG068r": "la gemela",
       "S69voz": "decide sumando", "P69voz": "decide con la posición"}
ROT_MANERA = dict(FE.RÓTULO)                    # «decide con el motor», «decide sumando», «decide con la posición»
COLOR = dict(FE.COLOR, tonto="#8a8984", recolector="#52514e", RG68r="#6250d6", RG068r="#e87ba4")
REJILLA = "#dddddd"
f1 = lambda x: f"{x:.1f}".replace(".", ","); f2 = lambda x: f"{x:.2f}".replace(".", ","); f3 = lambda x: f"{x:.3f}".replace(".", ",")
fb = lambda b, f=f2: f"{f(b['media'])} [{f(b['lo'])}, {f(b['hi'])}]"


def estilo():
    plt.rcParams.update({"font.size": 15, "axes.spines.top": False, "axes.spines.right": False})


def guarda(fig, nom):
    os.makedirs(FIG, exist_ok=True)
    for ext in ("png", "pdf"): fig.savefig(os.path.join(FIG, f"{nom}.{ext}"), dpi=DPI)
    plt.close(fig)


def barras(ax, val, jug, rot, ancho, mundos=MUNDOS):
    """val[(jugador, mundo)] = la lista de valores por partida; una barra por jugador y mundo, con su intervalo. Devuelve los boot."""
    out = {}; nj = len(jug)
    for j, v in enumerate(jug):
        B = [boot(val[(v, mu)]) for mu in mundos]; out[v] = dict(zip(mundos, B))
        xs = [i + (j - (nj - 1) / 2) * (ancho + 0.02) for i in range(len(mundos))]; m = [b["media"] for b in B]
        ax.bar(xs, m, width=ancho, color=COLOR[v], label=rot[v], zorder=3)
        ax.errorbar(xs, m, yerr=[[b["media"] - b["lo"] for b in B], [b["hi"] - b["media"] for b in B]], fmt="none", ecolor="#333333", elinewidth=1.4, capsize=3, zorder=4)
    ax.set_xticks(range(len(mundos))); ax.set_xticklabels([NOMBRE_MUNDO[mu] for mu in mundos])
    ax.grid(axis="y", color=REJILLA, linewidth=0.8, zorder=0)
    return out


def tabla_barras(out, jug, rot, f=f2, n=None):
    w = ["| mundo | " + " | ".join(rot[v] for v in jug) + " |", "|---|" + "---|" * len(jug)]
    for mu in next(iter(out.values())):
        w.append(f"| {NOMBRE_MUNDO[mu]} | " + " | ".join(fb(out[v][mu], f) for v in jug) + " |")
    return w


def escribe_txt(nom, lineas):
    open(os.path.join(FIG, f"{nom}.txt"), "w", encoding="utf-8").write("\n".join(lineas) + "\n")

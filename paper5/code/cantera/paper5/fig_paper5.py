"""[P5-FIG] Las cinco figuras del paper cinco, en español y en inglés.

SOLO LECTURA de los .json ya extraídos. PNG a 300 ppp, ancho de página A4.
Paleta Okabe-Ito (distinguible sin ver bien los colores) + estilos de línea
distintos, para que ninguna diferencia dependa SOLO del color.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SAL = "cantera/paper5/figuras_paper5"
ANCHO = 6.7                      # pulgadas: el ancho útil de una A4
PPP = 300
# Okabe-Ito
AZUL, NARANJA, VERDE = "#0072B2", "#E69F00", "#009E73"
ROSA, CIELO, BERMELLON = "#CC79A7", "#56B4E9", "#D55E00"
TINTA, GRIS, REJILLA = "#1A1A1A", "#6E6E6E", "#D9D9D9"

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9.5, "axes.titlesize": 10.5,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "legend.fontsize": 8.5,
    "axes.edgecolor": GRIS, "axes.labelcolor": TINTA, "text.color": TINTA,
    "xtick.color": GRIS, "ytick.color": GRIS, "figure.dpi": PPP,
    "savefig.dpi": PPP, "savefig.bbox": "tight", "savefig.pad_inches": 0.06,
})

L = {
 "es": {
  "instantes": "instantes de la partida",
  "vida": "vida que le queda",
  "falta": "lo que le falta\n(de 0 a 1)",
  "lejos": "lo lejos que está\nde su sitio",
  "mapa": "mapa que le queda\npor ver",
  "peligro": "amenaza que percibe\n(de 0 a 1)",
  "f1t": "Una vida entera del mundo lento",
  "f1s": "{n} instantes · nadie la toca hasta el instante {g} (siete minutos)\ny en ningún instante deja de faltarle algo",
  "quieta": "quieta al empezar",
  "anillo": "el anillo empieza a avisar",
  "primer": "primer golpe recibido",
  "f2t": "La forma de un plan real, punto por punto",
  "f2s": "plan del consejero · {a} · cuatro tramos\nlo que el cuerpo proyectó, y lo que pasó",
  "plan": "lo que proyectó SI SIGUE EL PLAN",
  "solo": "lo que proyectó SI SIGUE SOLO",
  "paso": "lo que pasó de verdad",
  "punto": "punto de control",
  "muere": "aquí abandona el plan",
  "mejor": "más abajo es mejor",
  "tramo": ["esperar 5 instantes", "ir a coger a (23,17)", "ir a coger a (22,22)", "usar lo cogido"],
  "f3t": "Seis mil instantes de calma sin mirar el mundo",
  "f3s": "{a}\nsin peligro ninguno y sin descubrir una casilla nueva,\ndel instante {i} al {f}",
  "meseta": "{n} instantes con el mapa clavado",
  "f4t": "Una vida del cuerpo curioso, con sus {n} viajes",
  "f4s": "{a} · cada franja es un viaje, coloreada por cómo acabó",
  "llega": "se completa (cobra lo prometido)",
  "atasca": "se atasca (3 pasos sin acercarse)",
  "f5t": "Lo que cada cuerpo llega a conocer del mundo",
  "f5s": "{na} vidas del cuerpo solo contra {nk} del cuerpo curioso · las cuarenta partidas\n(líneas finas: cada vida · línea gruesa: la mediana)",
  "solo_b": "cuerpo solo",
  "cur_b": "cuerpo curioso",
  "medsolo": "cuerpo solo · mediana",
  "medcur": "cuerpo curioso · mediana",
  "abajo": "más abajo = conoce más mundo",
 },
 "en": {
  "instantes": "instants of the game",
  "vida": "life left",
  "falta": "what it lacks\n(0 to 1)",
  "lejos": "how far it is\nfrom its place",
  "mapa": "map still\nunseen",
  "peligro": "threat it senses\n(0 to 1)",
  "f1t": "A whole life in the slow world",
  "f1s": "{n} instants · nobody touches it until instant {g} (seven minutes)\nand at no instant does it stop lacking something",
  "quieta": "still at the start",
  "anillo": "the ring starts warning",
  "primer": "first blow taken",
  "f2t": "The shape of a real plan, point by point",
  "f2s": "advisor's plan · {a} · four legs\nwhat the body projected, and what happened",
  "plan": "projected IF IT FOLLOWS THE PLAN",
  "solo": "projected IF IT GOES ALONE",
  "paso": "what actually happened",
  "punto": "checkpoint",
  "muere": "here it abandons the plan",
  "mejor": "lower is better",
  "tramo": ["wait 5 instants", "go pick up at (23,17)", "go pick up at (22,22)", "use what it picked"],
  "f3t": "Six thousand calm instants without looking at the world",
  "f3s": "{a}\nno threat at all and not one new square discovered,\nfrom instant {i} to {f}",
  "meseta": "{n} instants with the map frozen",
  "f4t": "A life of the curious body, with its {n} trips",
  "f4s": "{a} · each band is a trip, coloured by how it ended",
  "llega": "completes (collects what it promised)",
  "atasca": "gets stuck (3 steps without closing in)",
  "f5t": "How much of the world each body gets to know",
  "f5s": "{na} lives of the body alone against {nk} of the curious body · the forty games\n(thin lines: each life · thick line: the median)",
  "solo_b": "body alone",
  "cur_b": "curious body",
  "medsolo": "body alone · median",
  "medcur": "curious body · median",
  "abajo": "lower = knows more of the world",
 },
}


def mil(n, idi):
    """Separador de miles: punto en español, coma en inglés."""
    return f"{n:,}" if idi == "en" else f"{n:,}".replace(",", ".")


def limpia(ax):
    ax.grid(alpha=0.35, linewidth=0.5, color=REJILLA)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def guarda(fig, nom):
    p = os.path.join(SAL, nom)
    fig.savefig(p)
    plt.close(fig)
    print("  ", p)


# ══════════ 1 · una vida del mundo lento ══════════
D1 = json.load(open("cantera/paper5/FIG13_datos.json"))
for idi in ("es", "en"):
    t = L[idi]
    fig, ax = plt.subplots(3, 1, figsize=(ANCHO, 6.4), sharex=True)
    T = D1["T"]
    ax[0].plot(T, D1["hp"], color=AZUL, lw=1.4)
    ax[0].set_ylabel(t["vida"]); ax[0].set_ylim(-4, 126)
    ax[1].plot(T, [c if c is not None else float("nan") for c in D1["carencia"]],
               color=NARANJA, lw=1.4)
    ax[1].axhline(0, color=BERMELLON, lw=1.0, ls=":")
    ax[1].set_ylabel(t["falta"]); ax[1].set_ylim(-0.05, 1.08)
    ax[2].plot(T, [d if d is not None else float("nan") for d in D1["d"]],
               color=VERDE, lw=1.4)
    ax[2].set_ylabel(t["lejos"]); ax[2].set_xlabel(t["instantes"])
    g0 = D1["golpes"][0][0] if D1["golpes"] else None
    for a in ax:
        limpia(a)
        a.axvline(D1["freeze_ticks"], color=GRIS, lw=0.9, ls="--")
        a.axvline(D1["aviso_anillo"], color=ROSA, lw=1.1, ls="-.")
        if g0:
            a.axvline(g0, color=BERMELLON, lw=1.1, ls=(0, (3, 1, 1, 1)))
    ax[0].annotate(t["quieta"], xy=(D1["freeze_ticks"], 109), xytext=(900, 109),
                   fontsize=8, color=GRIS, va="bottom")
    ax[0].annotate(t["anillo"], xy=(D1["aviso_anillo"], 109),
                   xytext=(D1["aviso_anillo"] - 260, 109), fontsize=8,
                   color=ROSA, va="bottom", ha="right")
    if g0:
        ax[0].annotate(t["primer"], xy=(g0, 62), xytext=(g0 - 380, 42),
                       fontsize=8, color=BERMELLON, va="center", ha="right",
                       arrowprops=dict(arrowstyle="->", color=BERMELLON, lw=0.9))
    _a1 = D1["asiento"]
    _p1 = ("partida " if idi == "es" else "game ") + _a1.split("_")[3].split("/")[0] \
        + (" · asiento " if idi == "es" else " · seat ") + _a1.split("/")[1]
    fig.suptitle(t["f1t"] + " · " + _p1 + "\n" + t["f1s"].format(n=mil(len(T), idi), g=mil(g0, idi) if g0 else "—"),
                 fontsize=10.5, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    guarda(fig, f"fig1_una_vida_{idi}.png")


# ══════════ 2 · la forma de un plan real ══════════
D2 = json.load(open("cantera/paper5/FIG2_datos.json"))
for idi in ("es", "en"):
    t = L[idi]
    fig, ax = plt.subplots(figsize=(ANCHO, 4.3))
    n = len(D2["tics"])
    x = list(range(n))
    ax.plot(x, D2["cs"], color=GRIS, lw=2.0, ls="--", marker="s", ms=6,
            label=t["solo"], zorder=3)
    ax.plot(x, D2["cf"], color=AZUL, lw=2.2, ls="-", marker="o", ms=6,
            label=t["plan"], zorder=4)
    ax.plot(x, D2["real"], color=NARANJA, lw=2.2, ls="-.", marker="^", ms=7,
            label=t["paso"], zorder=5)
    # el tic en que abandona el plan, entre los puntos 1 y 2
    tc = (D2.get("caida") or {}).get("tick")
    if tc:
        tics = D2["tics"]
        for i in range(n - 1):
            if tics[i] <= tc <= tics[i + 1] and tics[i] != tics[i + 1]:
                fx = i + (tc - tics[i]) / (tics[i + 1] - tics[i])
                ax.axvline(fx, color=BERMELLON, lw=1.3, ls=":", zorder=2)
                # el rótulo, EN HORIZONTAL y a la derecha de la línea de
                # puntos, en la banda libre entre la curva azul (3,12) y la
                # gris (3,36): por ahí no pasa ninguna de las tres curvas y
                # no depende del largo del texto en cada idioma.
                ax.text(fx + 0.045, 3.245, t["muere"], fontsize=8,
                        color=BERMELLON, va="center", ha="left")
                break
    ax.set_xticks(x)
    ax.set_xticklabels([f"{t['punto']} {i}\n({tt})\n{t['tramo'][i]}"
                        for i, tt in enumerate(D2["tics"])], fontsize=7.6)
    ax.set_ylabel(t["lejos"])
    ax.annotate(t["mejor"], xy=(0.012, 0.06), xycoords="axes fraction",
                fontsize=8, color=GRIS, style="italic")
    limpia(ax)
    # la leyenda, al hueco libre de abajo a la derecha (entre 2,7 y 3,0):
    # por ahí no pasa ninguna de las tres curvas.
    ax.legend(frameon=False, loc="lower right", ncol=1,
              bbox_to_anchor=(1.0, 0.04))
    _a = D2["asiento"]
    _pl = ("partida " if idi == "es" else "game ") + _a.split("_")[3].split("/")[0] \
        + (" · asiento " if idi == "es" else " · seat ") + _a.split("/")[1]
    fig.suptitle(t["f2t"] + "\n" + t["f2s"].format(a=_pl),
                 fontsize=10.5, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    guarda(fig, f"fig2_forma_de_un_plan_{idi}.png")


# ══════════ 3 · la meseta de calma ══════════
for idi in ("es", "en"):
    t = L[idi]
    fig, ax = plt.subplots(2, 1, figsize=(ANCHO, 5.0), sharex=True)
    T, M = D1["T"], D1["meseta"]
    ax[0].plot(T, D1["ign"], color=AZUL, lw=1.6)
    ax[0].set_ylabel(t["mapa"])
    ax[1].plot(T, D1["amenaza"], color=BERMELLON, lw=1.2)
    ax[1].set_ylabel(t["peligro"]); ax[1].set_xlabel(t["instantes"])
    ax[1].set_ylim(-0.03, 1.05)
    for a in ax:
        limpia(a)
        a.axvspan(M["ini"], M["fin"], color=VERDE, alpha=0.16, zorder=0)
        a.axvline(M["ini"], color=VERDE, lw=1.1, ls="--")
        a.axvline(M["fin"], color=VERDE, lw=1.1, ls="--")
    ax[0].annotate(t["meseta"].format(n=mil(M["largo"], idi)),
                   xy=((M["ini"] + M["fin"]) / 2, M["valor"] + 0.018),
                   ha="center", fontsize=8.5, color="#0B6E4F")
    _a3 = D1["asiento"]
    _p3 = ("partida " if idi == "es" else "game ") + _a3.split("_")[3].split("/")[0] \
        + (" · asiento " if idi == "es" else " · seat ") + _a3.split("/")[1] \
        + (" · cuerpo solo" if idi == "es" else " · body alone")
    fig.suptitle(t["f3t"] + "\n" + t["f3s"].format(
        a=_p3, i=mil(M["ini"], idi), f=mil(M["fin"], idi)), fontsize=10.0, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.87])
    guarda(fig, f"fig3_meseta_de_calma_{idi}.png")


# ══════════ 4 y 5 · el cuerpo curioso ══════════
D45 = json.load(open("cantera/paper5/FIG45_datos.json"))
COL45 = {"completada": (VERDE, "llega"), "atasco": (NARANJA, "atasca")}
for idi in ("es", "en"):
    t = L[idi]
    F2 = D45["F2"]
    fig, ax = plt.subplots(figsize=(ANCHO, 4.0))
    ax.plot(F2["x"], F2["y"], color=AZUL, lw=1.8, zorder=4)
    vistos = set()
    for v in F2["viajes"]:
        cl, cv = next(((c, k) for k, (c, k) in COL45.items() if k in v["motivo"]
                       or (k == "completada" and "completada" in v["motivo"])),
                      (GRIS, None))
        for k, (c, et) in COL45.items():
            if k in v["motivo"]:
                cl, cv = c, et
                break
        ax.axvspan(v["t0"], max(v["t1"], v["t0"] + 8), color=cl, alpha=0.42,
                   zorder=1, label=(t[cv] if cv and cv not in vistos else None))
        if cv:
            vistos.add(cv)
    ax.set_xlabel(t["instantes"]); ax.set_ylabel(t["mapa"])
    limpia(ax)
    ax.legend(frameon=False, loc="upper right")
    fig.suptitle(t["f4t"].format(n=len(F2["viajes"])) + "\n"
                 + t["f4s"].format(a=("partida " if idi == "es" else "game ")
                 + F2["asiento"].split("_")[3].split("/")[0]
                 + (" · asiento " if idi == "es" else " · seat ")
                 + F2["asiento"].split("/")[1]), fontsize=10.5, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.87])
    guarda(fig, f"fig4_una_vida_curiosa_{idi}.png")

for idi in ("es", "en"):
    t = L[idi]
    F1 = D45["F1"]
    fig, ax = plt.subplots(figsize=(ANCHO, 4.4))
    for brazo, col, ls in (("A", GRIS, "-"), ("K", AZUL, "-")):
        for xs, ys in F1["curvas"][brazo]:
            ax.plot(xs, ys, color=col, alpha=0.16, lw=0.7, zorder=1)
    ax.plot(F1["medianas"]["A"]["x"], F1["medianas"]["A"]["y"], color=GRIS,
            lw=3.0, ls="--", zorder=5, label=t["medsolo"])
    ax.plot(F1["medianas"]["K"]["x"], F1["medianas"]["K"]["y"], color=AZUL,
            lw=3.0, ls="-", zorder=6, label=t["medcur"])
    ax.set_xlabel(t["instantes"]); ax.set_ylabel(t["mapa"])
    ax.annotate(t["abajo"], xy=(0.012, 0.05), xycoords="axes fraction",
                fontsize=8, color=GRIS, style="italic")
    limpia(ax)
    h = [Line2D([], [], color=GRIS, lw=0.9, alpha=0.5),
         Line2D([], [], color=AZUL, lw=0.9, alpha=0.5),
         Line2D([], [], color=GRIS, lw=3.0, ls="--"),
         Line2D([], [], color=AZUL, lw=3.0)]
    ax.legend(h, [t["solo_b"], t["cur_b"], t["medsolo"], t["medcur"]],
              frameon=False, loc="upper right", fontsize=8)
    fig.suptitle(t["f5t"] + "\n" + t["f5s"].format(na=F1["n_curvas"]["A"],
                 nk=F1["n_curvas"]["K"]), fontsize=10.5, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.86])
    guarda(fig, f"fig5_cuanto_mundo_conoce_{idi}.png")
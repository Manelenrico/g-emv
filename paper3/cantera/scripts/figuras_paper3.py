"""Figuras estaticas del paper tres (PROMPT del vigilante).

Misma herramienta y mismos datos que los GIF: reutiliza `gif_manada.diarios`,
`gif_manada.survival` y `gif_manada.vistos` — es decir, los dos diarios de la
pareja leidos con `pareja.lee`. NUNCA MettaScope. No toca `gif_manada.py`.

  fig1 — un fotograma de `ereq_292ee72d` (serie 66) a media partida.
  fig2 — tres fotogramas de `ereq_b915417a`, misma escala y mismo recorte.

Legibilidad en gris: los papeles se distinguen por FORMA ademas de por color
(circulo grande = pareja, triangulo = agresor, circulo pequeno = los demas,
cruz = venda), y todo lleva borde negro. Ancho de columna del paper dos
(`G-EMV_the_Hive_EN.pdf`, A4 a una columna): 424,8 pt = 5,90 in.

Uso:
  python3 paintball/figuras_paper3.py fig1 --out paper3/figuras/fig1_arena.png
  python3 paintball/figuras_paper3.py fig2 --out paper3/figuras/fig2_el_que_llega.png
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gif_manada import diarios, survival, vistos, OLVIDO

COL_IN = 5.90                 # ancho de columna del PDF del paper dos
DPI = 300
NARANJA = "#ff7f0e"
ROJO = "#d62728"
GRIS = "#9e9e9e"
VERDE = "#2e7d32"
AZUL = "#3d6fa8"
TINTA = "#111111"

FIG1_EP, FIG1_TIC = "ereq_292ee72d", 3029
FIG2_EP = "ereq_b915417a"
FIG2_TICS = (1704, 1706, 1760)
VENDA = (19, 21)              # la casilla del don


def base(ax, x0, x1, y0, y1, paso):
    ax.set_facecolor("white")
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)                      # y hacia abajo, como el mundo
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(TINTA); s.set_linewidth(1.0)
    for v in range(int(x0), int(x1) + 1, paso):
        ax.plot([v, v], [y0, y1], color="#e4e4e4", lw=0.4, zorder=0)
    for v in range(int(y0), int(y1) + 1, paso):
        ax.plot([x0, x1], [v, v], color="#e4e4e4", lw=0.4, zorder=0)


def memoria_hasta(R10, R11, t, surv):
    """Reproduce el estado de `vistos` avanzando desde el principio."""
    mem = {}
    v = {}
    t0 = min(min(R10 or {1: 0}), min(R11 or {1: 0}))
    for tt in range(t0, t + 1):
        v = vistos(R10, R11, tt, mem, surv)
    return v


def fig1(args):
    R10, R11 = diarios("manada2", FIG1_EP)
    surv = survival("manada2", FIG1_EP)
    t = args.tic
    v = memoria_hasta(R10, R11, t, surv)
    o = R10.get(t) or R11.get(t)
    z = (o or {}).get("zona") or {}
    c, rad = z.get("center"), z.get("radius")
    vivos = sum(1 for s in surv if s and s > t)
    print(f"  {FIG1_EP} t{t}: anillo centro {c} radio {rad} · {vivos} vivos · "
          f"{sum(1 for _p, f in v.values() if f)} asientos vistos ahora")

    fig, ax = plt.subplots(figsize=(COL_IN, COL_IN), dpi=DPI)
    fig.patch.set_facecolor("white")
    base(ax, 0, 48, 0, 48, 4)
    if c and rad:
        ax.add_patch(Rectangle((c[0] - rad, c[1] - rad), 2 * rad, 2 * rad,
                               fill=False, ec=AZUL, lw=1.8, zorder=1))
    for sl, (p, fresco) in sorted(v.items()):
        ax.plot(p[0], p[1], "o", ms=7, color=GRIS if fresco else "white",
                mec=TINTA, mew=.7, zorder=3)
        ax.annotate(str(sl), (p[0], p[1]), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=6.5,
                    color=TINTA, zorder=5)
    for R, sl in ((R10, 10), (R11, 11)):
        oo = R.get(t)
        if not oo:
            continue
        ax.plot(oo["pos"][0], oo["pos"][1], "o", ms=13, color=NARANJA,
                mec=TINTA, mew=1.0, zorder=4)
        ax.annotate(str(sl), (oo["pos"][0], oo["pos"][1]), xytext=(0, 11),
                    textcoords="offset points", ha="center", fontsize=8,
                    fontweight="bold", color=TINTA, zorder=6)
    ax.text(24, 1.6, "ZERO-SUM · ring · the pair", fontsize=8, color=TINTA,
            ha="center", va="top")
    fig.subplots_adjust(left=.01, right=.99, top=.99, bottom=.01)
    fig.savefig(args.out, dpi=DPI, facecolor="white")
    plt.close(fig)
    return t, rad, vivos


def fig2(args):
    R10, R11 = diarios("manada2", FIG2_EP)
    surv = survival("manada2", FIG2_EP)
    tics = FIG2_TICS
    # recorte comun: 10, 11, 12 y la venda en los tres tics, con margen
    xs, ys = [VENDA[0]], [VENDA[1]]
    for t in tics:
        for R in (R10, R11):
            o = R.get(t)
            if not o:
                continue
            xs.append(o["pos"][0]); ys.append(o["pos"][1])
            for a in (o.get("ve_agentes") or []):
                if a.get("slot") == 12:
                    xs.append(a["pos"][0]); ys.append(a["pos"][1])
    m = args.margen
    x0, y0 = min(xs) - m, min(ys) - m
    lado = max(max(xs) + m - x0, max(ys) + m - y0)
    x1, y1 = x0 + lado, y0 + lado
    print(f"  recorte comun x[{x0},{x1}] y[{y0},{y1}] (lado {lado})")

    alto = COL_IN / 3 + .42
    fig, axes = plt.subplots(1, 3, figsize=(COL_IN, alto), dpi=DPI)
    fig.patch.set_facecolor("white")
    for ax, t in zip(axes, tics):
        base(ax, x0, x1, y0, y1, 4)
        v = memoria_hasta(R10, R11, t, surv)
        # la venda: visible ahora, o ultima vista dentro de la ventana de olvido
        ult = None
        for tt in range(max(min(R10 or {1: 0}), t - OLVIDO), t + 1):
            for R in (R10, R11):
                for it in ((R.get(tt) or {}).get("ve_items") or []):
                    if it.get("id") == "first_aid" and tuple(it["pos"]) == VENDA:
                        ult = tt
        if ult is not None:
            ahora = ult == t
            # zorder alto a proposito: en t1706 la venda cae en la MISMA
            # casilla del hermano que la suelta, y debajo no se veria.
            ax.plot(VENDA[0], VENDA[1], "P", ms=8,
                    color=VERDE if ahora else "white", mec="white", mew=2.2,
                    zorder=8)
            ax.plot(VENDA[0], VENDA[1], "P", ms=8,
                    color=VERDE if ahora else "none", mec=VERDE, mew=1.4,
                    zorder=9)
        for sl, (p, fresco) in sorted(v.items()):
            if sl == 12:
                ax.plot(p[0], p[1], "^", ms=9, color=ROJO if fresco else "white",
                        mec=TINTA, mew=.8, zorder=4)
                ax.annotate("12", (p[0], p[1]), xytext=(0, 11),
                            textcoords="offset points", ha="center",
                            fontsize=6.5, color=TINTA, zorder=6)
            else:
                ax.plot(p[0], p[1], "o", ms=5, color=GRIS if fresco else "white",
                        mec=TINTA, mew=.6, zorder=3)
        for R, sl in ((R10, 10), (R11, 11)):
            oo = R.get(t)
            if not oo:
                continue
            ax.plot(oo["pos"][0], oo["pos"][1], "o", ms=11, color=NARANJA,
                    mec=TINTA, mew=.9, zorder=5)
            # la etiqueta se aparta DEL AGRESOR: sin esto, en t1704 el "100"
            # de a10 cae justo encima del triangulo del asiento 12.
            ag = v.get(12)
            dx, dy = 11, (10 if sl == 10 else -12)
            if ag:
                ax_, ay_ = ag[0]
                if ax_ >= oo["pos"][0]:
                    dx = -11
                dy = -13 if ay_ <= oo["pos"][1] else 12
                if sl == 11:
                    dy = -dy
            ax.annotate(f'{oo["hp"]:g}', (oo["pos"][0], oo["pos"][1]),
                        xytext=(dx, dy), textcoords="offset points",
                        ha="left" if dx > 0 else "right", va="center",
                        fontsize=7.5, fontweight="bold", color=TINTA,
                        zorder=10)
        ax.set_xlabel(f"t{t}", fontsize=8, color=TINTA, labelpad=3)
    fig.subplots_adjust(left=.01, right=.99, top=.97, bottom=.13, wspace=.06)
    fig.savefig(args.out, dpi=DPI, facecolor="white")
    plt.close(fig)
    return tics, (x0, x1, y0, y1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cual", choices=["fig1", "fig2"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--tic", type=int, default=FIG1_TIC)
    ap.add_argument("--margen", type=int, default=3)
    args = ap.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    if args.cual == "fig1":
        fig1(args)
    else:
        fig2(args)
    from PIL import Image
    im = Image.open(args.out)
    print(f"  {args.out}: {im.size} px · {im.info.get('dpi')} ppp · "
          f"{os.path.getsize(args.out)/1024:.0f} kB")


if __name__ == "__main__":
    main()

"""GIFs de la manada para el paper tres (PROMPT del vigilante).

Mismo estilo que `gemelos_gif.py` (matplotlib + PillowWriter, dpi 100, fondo
claro con marco). NO toca `gemelos_gif.py` ni `replay_gif.py`.

La diferencia de fondo con aquellos: alli la verdad venia del `.replay`; aqui
TODO sale de los dos diarios de la pareja (`pareja.lee`), porque de estas
tandas no hay replay guardado en local. Consecuencia declarada: los otros
catorce asientos solo se pintan cuando alguno de los dos los VE
(`ve_agentes`); nunca se inventa una posicion.

  gif1 — la partida entera, anillo incluido, rejilla 48x48.
  gif2 — una ventana corta a velocidad real, recortada a la accion.

Uso:
  python3 paintball/gif_manada.py gif1 --out paper3/gifs/gif_manada_anillo.gif
  python3 paintball/gif_manada.py gif2 --out paper3/gifs/gif_el_que_llega.gif
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from matplotlib.patches import Circle, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pareja import lee                      # el lector de la casa (bytes-repr)

RAIZ = Path(__file__).resolve().parent / "runs"
NARANJA = "#ff7f0e"          # los dos hermanos
ROJO = "#d62728"             # el agresor del gif2
GRIS = "#9e9e9e"             # los demas, cuando se ven
FONDO = "#f7f7f5"
TINTA = "#222222"
OLVIDO = 48                  # tics que se mantiene una posicion ya no vista


def diarios(serie: str, eid: str):
    """Los dos diarios de la pareja, indexados por tic. Devuelve (R10, R11)."""
    out = []
    for s in (10, 11):
        fs = sorted(glob.glob(str(RAIZ / serie / f"{eid}*" / f"a{s}" / "*.log")))
        if not fs:
            out.append({})
            continue
        out.append({r["tick"]: r for r in lee(fs[0]) if r.get("k") == "tick"})
    return out[0], out[1]


def survival(serie: str, eid: str):
    fs = glob.glob(str(RAIZ / serie / f"res_{eid}*.json"))
    if not fs:
        return [None] * 16
    return json.load(open(fs[0])).get("survival_ticks", [None] * 16)


def vistos(R10, R11, t, memoria, surv):
    """Union de `ve_agentes` de los dos diarios en el tic t, con olvido.

    Devuelve {slot: (pos, fresco)}. `fresco` False = visto hace <=OLVIDO tics
    (se pinta hueco). Los muertos (t >= survival_ticks) no se devuelven.
    """
    for R in (R10, R11):
        o = R.get(t)
        if not o:
            continue
        for a in (o.get("ve_agentes") or []):
            sl = a.get("slot")
            if sl in (10, 11) or sl is None:
                continue
            memoria[sl] = (tuple(a["pos"]), t)
    fuera = []
    out = {}
    for sl, (p, tv) in memoria.items():
        if t - tv > OLVIDO:
            fuera.append(sl)
            continue
        sv = surv[sl] if sl < len(surv) else None
        if sv is not None and t >= sv:          # muerto: no se pinta
            fuera.append(sl)
            continue
        out[sl] = (p, tv == t)
    for sl in fuera:
        memoria.pop(sl, None)
    return out


def marco(ax, x0, x1, y0, y1, rejilla):
    ax.set_facecolor(FONDO)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)                       # y hacia abajo, como el mundo
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(TINTA)
        s.set_linewidth(1.2)
    if rejilla:
        for v in range(int(x0), int(x1) + 1, 4):
            ax.plot([v, v], [y0, y1], color="#dddddd", lw=0.4, zorder=0)
        for v in range(int(y0), int(y1) + 1, 4):
            ax.plot([x0, x1], [v, v], color="#dddddd", lw=0.4, zorder=0)


def gif1(args):
    serie, eid = "manada2", "ereq_292ee72d"
    R10, R11 = diarios(serie, eid)
    surv = survival(serie, eid)
    tmin = min(min(R10 or {9e9: 0}), min(R11 or {9e9: 0}))
    tmax = max(max(R10 or {0: 0}), max(R11 or {0: 0}))
    # cotejo como en gemelos_gif.py: pareja_pos de a10 contra pos de a11
    com = ig = 0
    for t, o in R10.items():
        pp = (o.get("social") or {}).get("pareja_pos")
        if pp and t in R11:
            com += 1
            ig += 1 if tuple(pp) == tuple(R11[t]["pos"]) else 0
    print(f"  COTEJO pareja_pos(a10) vs pos(a11): {ig}/{com} tics coinciden")
    print(f"  tics {tmin}..{tmax}  ·  a10 {len(R10)} registros · a11 {len(R11)}")

    ticks = list(range(tmin, tmax + 1, args.paso))
    fig, ax = plt.subplots(figsize=(args.fig, args.fig), dpi=100)
    fig.patch.set_facecolor(FONDO)
    mem = {}
    w = PillowWriter(fps=args.fps)
    with w.saving(fig, args.out, dpi=100):
        for t in ticks:
            ax.clear()
            marco(ax, 0, 48, 0, 48, True)
            o = R10.get(t) or R11.get(t)
            z = (o or {}).get("zona") or {}
            c, rad = z.get("center"), z.get("radius")
            if c and rad:                       # anillo: caja de Chebyshev
                ax.add_patch(Rectangle((c[0] - rad, c[1] - rad), 2 * rad, 2 * rad,
                                       fill=False, ec="#4C78A8", lw=1.6,
                                       alpha=.9, zorder=1))
            for sl, (p, fresco) in vistos(R10, R11, t, mem, surv).items():
                ax.plot(p[0], p[1], "o", ms=5, color=GRIS if fresco else "none",
                        mec=GRIS, mew=1.0, alpha=.9 if fresco else .5, zorder=2)
            for R in (R10, R11):
                oo = R.get(t)
                if oo:
                    ax.plot(oo["pos"][0], oo["pos"][1], "o", ms=10,
                            color=NARANJA, mec="#7a3d00", mew=.8, zorder=4)
            ax.text(24, 1.4, "ZERO-SUM · 16 seats · the pair in orange · "
                    "others when seen", fontsize=5.8, color=TINTA,
                    va="top", ha="center")
            w.grab_frame(facecolor=FONDO)
    plt.close(fig)
    return tmin, tmax, len(ticks)


def gif2(args):
    serie, eid = "manada2", "ereq_b915417a"
    R10, R11 = diarios(serie, eid)
    surv = survival(serie, eid)
    t0, t1 = args.desde, args.hasta
    # recorte: caja de 10, 11 y 12 en la ventana, con margen
    xs, ys = [], []
    for R in (R10, R11):
        for t in range(t0, t1 + 1):
            o = R.get(t)
            if not o:
                continue
            xs.append(o["pos"][0]); ys.append(o["pos"][1])
            for a in (o.get("ve_agentes") or []):
                if a.get("slot") == 12:
                    xs.append(a["pos"][0]); ys.append(a["pos"][1])
    m = args.margen
    x0, x1 = min(xs) - m, max(xs) + m
    y0, y1 = min(ys) - m, max(ys) + m
    lado = max(x1 - x0, y1 - y0)
    x1, y1 = x0 + lado, y0 + lado
    print(f"  recorte x[{x0},{x1}] y[{y0},{y1}]")

    ticks = list(range(t0, t1 + 1, args.paso))
    fig, ax = plt.subplots(figsize=(args.fig, args.fig), dpi=100)
    fig.patch.set_facecolor(FONDO)
    mem = {}
    vendas = {}          # pos -> ultimo tic visto
    w = PillowWriter(fps=args.fps)
    with w.saving(fig, args.out, dpi=100):
        for t in ticks:
            ax.clear()
            marco(ax, x0, x1, y0, y1, True)
            # vendas en el suelo: aparecen cuando se ven y se borran al dejar de verse
            aqui = set()
            for R in (R10, R11):
                o = R.get(t)
                for it in ((o or {}).get("ve_items") or []):
                    if it.get("id") == "first_aid":
                        aqui.add(tuple(it["pos"]))
            vendas = {p: t for p in aqui}
            for p in vendas:
                ax.plot(p[0], p[1], "P", ms=9, color="#ffffff",
                        mec="#2e7d32", mew=1.8, zorder=3)
            for sl, (p, fresco) in vistos(R10, R11, t, mem, surv).items():
                col = ROJO if sl == 12 else GRIS
                ax.plot(p[0], p[1], "o", ms=9 if sl == 12 else 6,
                        color=col if fresco else "none", mec=col, mew=1.2,
                        alpha=.95 if fresco else .45, zorder=4)
                if sl == 12:
                    ax.text(p[0] + .45, p[1] - .45, "12", fontsize=7,
                            color=ROJO, zorder=6, fontweight="bold")
            for R in (R10, R11):
                oo = R.get(t)
                if not oo:
                    continue
                ax.plot(oo["pos"][0], oo["pos"][1], "o", ms=12, color=NARANJA,
                        mec="#7a3d00", mew=.9, zorder=5)
                ax.text(oo["pos"][0] + .5, oo["pos"][1] + .75,
                        f'{oo["hp"]:g}', fontsize=7.5, color="#7a3d00",
                        zorder=6, fontweight="bold")
            ax.text(x0 + .3, y0 + .9, "The one that arrives · ereq_b915417a",
                    fontsize=7.5, color=TINTA, va="top")
            w.grab_frame(facecolor=FONDO)
    plt.close(fig)
    return t0, t1, len(ticks)


def optimiza(path, colores):
    """Paleta reducida + optimize, SIN tocar el numero de fotogramas.

    MEDIDO: en estos dos GIF **empeora** (gif1: 416 kB -> 916 kB). Al
    recodificar cada fotograma entero se pierde el diff entre fotogramas que
    PillowWriter ya aplica, y eso pesa mas de lo que ahorra la paleta. Queda
    como palanca opt-in (`--colores N`, 0 = no tocar) y NO se usa: el tamano
    se paga con la figura, nunca con menos fotogramas.
    """
    from PIL import Image, ImageSequence
    im = Image.open(path)
    fr = [f.copy().convert("RGB").quantize(colors=colores, method=Image.MEDIANCUT)
          for f in ImageSequence.Iterator(im)]
    dur = im.info.get("duration", 83)
    fr[0].save(path, save_all=True, append_images=fr[1:], loop=0,
               duration=dur, optimize=True, disposal=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cual", choices=["gif1", "gif2"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--paso", type=int, default=None)
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--fig", type=float, default=4.4)
    ap.add_argument("--desde", type=int, default=1560)
    ap.add_argument("--hasta", type=int, default=1800)
    ap.add_argument("--margen", type=int, default=4)
    ap.add_argument("--colores", type=int, default=0,
                    help="0 = no recodificar (medido: recodificar ENGORDA)")
    args = ap.parse_args()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    if args.cual == "gif1":
        args.paso = args.paso or 24
        a, b, n = gif1(args)
    else:
        args.paso = args.paso or 2
        a, b, n = gif2(args)
    kb = os.path.getsize(args.out) / 1024
    if args.colores:
        optimiza(args.out, args.colores)
        kb = os.path.getsize(args.out) / 1024
    print(f"  {args.out}: tics {a}..{b} · {n} fotogramas · {kb:.0f} kB")


if __name__ == "__main__":
    main()

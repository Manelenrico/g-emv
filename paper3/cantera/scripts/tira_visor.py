"""Tira de cuatro capturas del visor de Softmax — figura 1 del paper tres.

Trabaja sobre COPIAS: las capturas de `paper3/figuras/visor/` no se tocan.

Cada captura se recorta al panel de juego (fuera el borde negro, el marcador
del top-izquierda, la linea de monedas y la barra de reproduccion) y se lleva a
un cuadrado centrado. Los cuatro cuadrados se montan en fila.

Las marcas de nuestros dos agentes NO se ponen a ojo: se calculan. La fortaleza
central es el patron de calibracion — su muro va de la casilla 20 a la 28 (9 de
lado, interior 7x7 = 49 celdas, `mundo_leido.camara_celdas`) y esta centrada en
(24,24) —, asi que de su caja en pixeles salen el centro y los px/casilla, y la
posicion de cada hermano viene de SU DIARIO en el tic correspondiente.

Uso: python3 paintball/tira_visor.py --out paper3/figuras/fig1_visor_tira.png
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gif_manada import diarios, survival

VISOR = Path(__file__).resolve().parent.parent / "paper3" / "figuras" / "visor"
COL_IN, DPI = 5.90, 300
NARANJA = "#ff7f0e"

# recorte del panel de juego en la captura original (x0, x1, y0, y1)
CROP = {"0m00": (198, 2774,  60, 2440),
        "1m11": (915, 3202, 380, 2340),
        "2m06": (876, 3163, 380, 2330),
        "3m54": (726, 3302, 380, 2440)}

# tiempo del visor -> tic (24 tics/s), y la fortaleza leida sobre el cuadrado
# ya normalizado a 900 px: (x0, x1, y0, y1) de su muro exterior
PANEL = [("0m00", "0:00",    1, (370, 555, 378, 565)),
         ("1m11", "1:11", 1704, (370, 555, 318, 505)),
         ("2m06", "2:06", 3024, (370, 565, 318, 512)),
         ("3m54", "3:54", 5616, None)]


def cuadrado(nombre):
    x0, x1, y0, y1 = CROP[nombre]
    im = Image.open(VISOR / f"visor_{nombre}.png").convert("RGB").crop((x0, y0, x1, y1))
    lado = min(im.width, im.height)
    cx, cy = im.width // 2, im.height // 2
    return im.crop((cx - lado // 2, cy - lado // 2,
                    cx - lado // 2 + lado, cy - lado // 2 + lado))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--serie", default="manada2")
    ap.add_argument("--ep", default="ereq_292ee72d")
    ap.add_argument("--rejilla", action="store_true",
                    help="monta en 2x2 en vez de en fila (misma calibracion)")
    ap.add_argument("--lw", type=float, default=None,
                    help="grosor del circulo en puntos (por defecto: 1.1 en "
                         "fila, 2.4 en 2x2 — se engorda el TRAZO, no el radio)")
    args = ap.parse_args()

    R10, R11 = diarios(args.serie, args.ep)
    surv = survival(args.serie, args.ep)
    N = 900                                    # lado normalizado de trabajo

    if args.rejilla:
        lado = (COL_IN - .10) / 2                 # dos columnas con margen fino
        fig, axes = plt.subplots(2, 2, figsize=(COL_IN, 2 * lado + .46), dpi=DPI)
        axes = axes.ravel()                       # 0:00 1:11 / 2:06 3:54
    else:
        fig, axes = plt.subplots(1, 4, figsize=(COL_IN, COL_IN / 4 + .30), dpi=DPI)
    lw = args.lw if args.lw else (2.4 if args.rejilla else 1.1)
    fig.patch.set_facecolor("white")
    for ax, (nom, etiqueta, tic, fort) in zip(axes, PANEL):
        sq = cuadrado(nom).resize((N, N), Image.LANCZOS)
        ax.imshow(sq)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#111111"); s.set_linewidth(.6)
        if fort:
            fx0, fx1, fy0, fy1 = fort
            cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
            pxt = max(fx1 - fx0, fy1 - fy0) / 9.0      # muro 20..28 = 9 casillas
            for R, sl in ((R10, 10), (R11, 11)):
                o = R.get(tic)
                if not o or (surv[sl] and tic >= surv[sl]):
                    continue                            # caido: sin marca
                gx, gy = o["pos"]
                x = cx + (gx + .5 - 24.5) * pxt
                y = cy + (gy + .5 - 24.5) * pxt
                ax.add_patch(plt.Circle((x, y), pxt * 1.15, fill=False,
                                        ec=NARANJA, lw=lw, zorder=5))
                print(f"  {nom} t{tic} asiento {sl} grid({gx},{gy}) -> ({x:.0f},{y:.0f})")
        else:
            vivos = [sl for sl in (10, 11) if surv[sl] and tic < surv[sl]]
            print(f"  {nom} t{tic}: caidos (survival 10={surv[10]}, 11={surv[11]})"
                  f" -> sin marca  {vivos}")
        ax.set_xlabel(etiqueta, fontsize=8, color="#111111", labelpad=3)
    if args.rejilla:
        fig.subplots_adjust(left=.005, right=.995, top=.99, bottom=.055,
                            wspace=.035, hspace=.10)
    else:
        fig.subplots_adjust(left=.005, right=.995, top=.985, bottom=.155,
                            wspace=.04)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=DPI, facecolor="white")
    plt.close(fig)
    im = Image.open(args.out)
    print(f"  {args.out}: {im.size} px · {os.path.getsize(args.out)/1024:.0f} kB")


if __name__ == "__main__":
    main()

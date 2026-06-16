"""
Figura: firmas de activación en la esfera de orientaciones G-EMV.

Lee attractor_signatures.json y genera una figura 3D mostrando las 3000 firmas
de respuesta normalizadas sobre la esfera unitaria. Los puntos se colorean por
polo más cercano. La densidad emerge del solapamiento natural de puntos.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # noqa: F401 (registro del proyector)
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.lines import Line2D
from pathlib import Path

# ─── Rutas ────────────────────────────────────────────────────────────────────
INFILE  = Path(__file__).parent / "attractor_signatures.json"
OUTFILE = Path(__file__).parent / "figures" / "exp_firmas_activacion_esfera.png"

# ─── Paleta: positivos = familia roja, negativos = familia gris ────────────────
# Positivos
C_POS_F = '#C0392B'   # rojo intenso       (+F)
C_POS_R = '#922B21'   # vino oscuro        (+R)
C_POS_S = '#E08070'   # salmón/terracota   (+S)
# Negativos
C_NEG_F = '#273746'   # gris muy oscuro    (-F)
C_NEG_R = '#717D7E'   # gris medio         (-R)
C_NEG_S = '#AAB7B8'   # gris plata         (-S)

POLE_META = {
    '+F': {'vec': np.array([ 1., 0., 0.]), 'color': C_POS_F},
    '+R': {'vec': np.array([ 0., 1., 0.]), 'color': C_POS_R},
    '+S': {'vec': np.array([ 0., 0., 1.]), 'color': C_POS_S},
    '-F': {'vec': np.array([-1., 0., 0.]), 'color': C_NEG_F},
    '-R': {'vec': np.array([ 0.,-1., 0.]), 'color': C_NEG_R},
    '-S': {'vec': np.array([ 0., 0.,-1.]), 'color': C_NEG_S},
}

POLE_KEYS  = list(POLE_META.keys())
POLE_VECS  = np.array([POLE_META[k]['vec'] for k in POLE_KEYS])  # (6, 3)
POLE_COLS  = [POLE_META[k]['color'] for k in POLE_KEYS]


def hex_to_rgba(hex_str: str, alpha: float) -> np.ndarray:
    r = int(hex_str[1:3], 16) / 255
    g = int(hex_str[3:5], 16) / 255
    b = int(hex_str[5:7], 16) / 255
    return np.array([r, g, b, alpha])


def main():
    # ── Carga ──────────────────────────────────────────────────────────────────
    with open(INFILE) as f:
        data = json.load(f)

    pts   = np.array([[p['sig_F'], p['sig_R'], p['sig_S']] for p in data['signatures']])
    types = np.array([p['type'] for p in data['signatures']])
    N     = len(pts)

    # Asignación de polo más cercano (coseno máximo con signo)
    dots         = pts @ POLE_VECS.T      # (N, 6)
    nearest_idx  = np.argmax(dots, axis=1)
    max_cos      = dots[np.arange(N), nearest_idx]

    # Cuenta de puntos por polo (para etiqueta de porcentaje en leyenda)
    pole_counts = {k: int((nearest_idx == i).sum()) for i, k in enumerate(POLE_KEYS)}

    # ── Figura ─────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(10, 8.5), facecolor='white')
    ax  = fig.add_subplot(111, projection='3d', facecolor='white')

    # ─ Esfera de referencia (superficie muy tenue) ────────────────────────────
    u_sp = np.linspace(0, 2 * np.pi, 60)
    v_sp = np.linspace(0, np.pi, 30)
    xs   = np.outer(np.cos(u_sp), np.sin(v_sp))
    ys   = np.outer(np.sin(u_sp), np.sin(v_sp))
    zs   = np.outer(np.ones_like(u_sp), np.cos(v_sp))
    ax.plot_surface(xs, ys, zs, color='#F0F0F0', alpha=0.09,
                    linewidth=0, antialiased=True, zorder=0)

    # ─ Círculos de referencia (3 planos coordenados) ─────────────────────────
    theta = np.linspace(0, 2 * np.pi, 200)
    zero  = np.zeros_like(theta)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    for x_, y_, z_ in [
        (cos_t, sin_t, zero),    # plano F-R (horizontal)
        (cos_t, zero,  sin_t),   # plano F-S
        (zero,  cos_t, sin_t),   # plano R-S
    ]:
        ax.plot(x_, y_, z_, color='#C8C8C8', linewidth=0.6, alpha=0.6, zorder=1)

    # ─ Puntos de firmas (solapamiento → densidad visual) ─────────────────────
    # Alpha fijo: la densidad emerge del solapamiento natural de 3000 puntos
    ALPHA_PT = 0.22
    SIZE_PT  = 6

    for gi, (pole_key, pole_color) in enumerate(zip(POLE_KEYS, POLE_COLS)):
        mask = nearest_idx == gi
        if not mask.any():
            continue
        sub = pts[mask]
        # RGBA por punto: mismo color, mismo alpha
        rgba = np.tile(hex_to_rgba(pole_color, ALPHA_PT), (mask.sum(), 1))
        ax.scatter(sub[:, 0], sub[:, 1], sub[:, 2],
                   c=rgba, s=SIZE_PT, linewidths=0,
                   depthshade=False, zorder=3)

    # ─ Marcadores de polos (solo el punto; la etiqueta se añade después en 2D) ─
    for pole_key, pmeta in POLE_META.items():
        pv = pmeta['vec']
        pc = pmeta['color']
        ax.scatter(*pv, c=pc, s=240, edgecolors='white',
                   linewidths=2.0, zorder=10, depthshade=False)

    # ─ Líneas de ejes (sin quiver para evitar artefactos de proyección) ───────
    AX_LEN   = 1.30
    AX_COLOR = '#BBBBBB'
    for dim, label, label_end in [
        (0, 'F', [ AX_LEN+0.20,  0,           0          ]),
        (1, 'R', [ 0,            AX_LEN+0.20,  0          ]),
        (2, 'S', [ 0,            0,            AX_LEN+0.20]),
    ]:
        # Línea desde -AX_LEN a +AX_LEN
        p0 = [0., 0., 0.]; p1 = [0., 0., 0.]
        p0[dim] = -AX_LEN;  p1[dim] = AX_LEN
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
                color=AX_COLOR, linewidth=0.7, alpha=0.6, zorder=1)
        ax.text(*label_end, label, color='#666666', fontsize=10,
                ha='center', va='center', fontweight='bold', zorder=12)

    # ─ Leyenda ───────────────────────────────────────────────────────────────
    legend_handles = []
    for pole_key, pmeta in POLE_META.items():
        n = pole_counts[pole_key]
        pct = 100 * n / N
        lbl = f'{pole_key}   {pct:.0f}%'
        legend_handles.append(
            Line2D([0], [0], marker='o', color='w',
                   markerfacecolor=pmeta['color'], markersize=9,
                   label=lbl)
        )
    ax.legend(handles=legend_handles, loc='upper left',
              bbox_to_anchor=(0.00, 1.02), fontsize=8.5,
              framealpha=0.92, edgecolor='#CCCCCC',
              title='Polo más cercano', title_fontsize=8.5,
              handletextpad=0.5, labelspacing=0.4)

    # ─ Encuadre y paneles ────────────────────────────────────────────────────
    ax.view_init(elev=22, azim=35)
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.12, 1.12)
    ax.set_zlim(-1.12, 1.12)

    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('none')
    ax.set_axis_off()

    # ─ Título y subtítulo ────────────────────────────────────────────────────
    fig.text(0.50, 0.96,
             'Firmas de activación — espacio de orientaciones G-EMV',
             ha='center', va='top', fontsize=12, color='#222222', fontweight='semibold')
    fig.text(0.50, 0.92,
             r'$n=3000$ perturbaciones (90% mezclas continuas, $\Delta\in[0.5,\,3.5]$) '
             '— 62.7% de las mezclas dentro de 30° de un polo puro (nulo: 40.2%)',
             ha='center', va='top', fontsize=8.5, color='#555555')

    # ─ Etiquetas de polo: proyección exacta 3D→2D→coordenadas figura ────────
    fig.canvas.draw()
    M = ax.get_proj()

    # Desplazamiento radial desde el centro de la figura (0.5, 0.5)
    pole_label_offset = {
        '+F': (-0.038, -0.026), '+R': (-0.010, -0.030),
        '+S': (+0.045, +0.006), '-F': (+0.032, +0.024),
        '-R': (-0.038, +0.012), '-S': (+0.040, -0.010),
    }

    LABEL_RADIUS = 1.30  # sobre la esfera unitaria, fuera del marcador (r=1)
    for pole_key, pmeta in POLE_META.items():
        pv = pmeta['vec']
        pc = pmeta['color']
        x2d, y2d, _ = proj_transform(
            pv[0]*LABEL_RADIUS, pv[1]*LABEL_RADIUS, pv[2]*LABEL_RADIUS, M)
        # transData lleva (x2d, y2d) a píxeles de pantalla; transFigure a fracción
        display_xy = ax.transData.transform((x2d, y2d))
        xf, yf    = fig.transFigure.inverted().transform(display_xy)
        ox, oy = pole_label_offset[pole_key]
        fig.text(xf + ox, yf + oy, pole_key,
                 color=pc, fontsize=9, fontweight='bold',
                 ha='center', va='center')

    # ─ Guarda ────────────────────────────────────────────────────────────────
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(OUTFILE, dpi=300, bbox_inches='tight', facecolor='white')
    print(f'Figura guardada: {OUTFILE}')
    print(f'Tamaño: {OUTFILE.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()

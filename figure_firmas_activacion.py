"""
Figure: activation signatures in the G-EMV orientation sphere.

Reads attractor_signatures.json and generates a 3D figure showing 3000 normalised
response signatures on the unit sphere. Points are coloured by nearest pole.
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # noqa: F401
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.lines import Line2D
from pathlib import Path

INFILE  = Path(__file__).parent / "attractor_signatures.json"
OUTFILE = Path(__file__).parent / "figures" / "exp_firmas_activacion_esfera.png"

C_POS_F = '#C0392B'
C_POS_R = '#922B21'
C_POS_S = '#E08070'
C_NEG_F = '#273746'
C_NEG_R = '#717D7E'
C_NEG_S = '#AAB7B8'

POLE_META = {
    '+F': {'vec': np.array([ 1., 0., 0.]), 'color': C_POS_F},
    '+R': {'vec': np.array([ 0., 1., 0.]), 'color': C_POS_R},
    '+S': {'vec': np.array([ 0., 0., 1.]), 'color': C_POS_S},
    '-F': {'vec': np.array([-1., 0., 0.]), 'color': C_NEG_F},
    '-R': {'vec': np.array([ 0.,-1., 0.]), 'color': C_NEG_R},
    '-S': {'vec': np.array([ 0., 0.,-1.]), 'color': C_NEG_S},
}

POLE_KEYS  = list(POLE_META.keys())
POLE_VECS  = np.array([POLE_META[k]['vec'] for k in POLE_KEYS])
POLE_COLS  = [POLE_META[k]['color'] for k in POLE_KEYS]


def hex_to_rgba(hex_str: str, alpha: float) -> np.ndarray:
    r = int(hex_str[1:3], 16) / 255
    g = int(hex_str[3:5], 16) / 255
    b = int(hex_str[5:7], 16) / 255
    return np.array([r, g, b, alpha])


def main():
    with open(INFILE) as f:
        data = json.load(f)

    pts   = np.array([[p['sig_F'], p['sig_R'], p['sig_S']] for p in data['signatures']])
    types = np.array([p['type'] for p in data['signatures']])
    N     = len(pts)

    dots         = pts @ POLE_VECS.T
    nearest_idx  = np.argmax(dots, axis=1)
    max_cos      = dots[np.arange(N), nearest_idx]

    pole_counts = {k: int((nearest_idx == i).sum()) for i, k in enumerate(POLE_KEYS)}

    fig = plt.figure(figsize=(10, 8.5), facecolor='white')
    ax  = fig.add_subplot(111, projection='3d', facecolor='white')

    u_sp = np.linspace(0, 2 * np.pi, 60)
    v_sp = np.linspace(0, np.pi, 30)
    xs   = np.outer(np.cos(u_sp), np.sin(v_sp))
    ys   = np.outer(np.sin(u_sp), np.sin(v_sp))
    zs   = np.outer(np.ones_like(u_sp), np.cos(v_sp))
    ax.plot_surface(xs, ys, zs, color='#F0F0F0', alpha=0.09,
                    linewidth=0, antialiased=True, zorder=0)

    theta = np.linspace(0, 2 * np.pi, 200)
    zero  = np.zeros_like(theta)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    for x_, y_, z_ in [
        (cos_t, sin_t, zero),
        (cos_t, zero,  sin_t),
        (zero,  cos_t, sin_t),
    ]:
        ax.plot(x_, y_, z_, color='#C8C8C8', linewidth=0.6, alpha=0.6, zorder=1)

    ALPHA_PT = 0.22
    SIZE_PT  = 6

    for gi, (pole_key, pole_color) in enumerate(zip(POLE_KEYS, POLE_COLS)):
        mask = nearest_idx == gi
        if not mask.any():
            continue
        sub = pts[mask]
        rgba = np.tile(hex_to_rgba(pole_color, ALPHA_PT), (mask.sum(), 1))
        ax.scatter(sub[:, 0], sub[:, 1], sub[:, 2],
                   c=rgba, s=SIZE_PT, linewidths=0,
                   depthshade=False, zorder=3)

    for pole_key, pmeta in POLE_META.items():
        pv = pmeta['vec']
        pc = pmeta['color']
        ax.scatter(*pv, c=pc, s=240, edgecolors='white',
                   linewidths=2.0, zorder=10, depthshade=False)

    AX_LEN   = 1.30
    AX_COLOR = '#BBBBBB'
    for dim, label, label_end in [
        (0, 'F', [ AX_LEN+0.20,  0,           0          ]),
        (1, 'R', [ 0,            AX_LEN+0.20,  0          ]),
        (2, 'S', [ 0,            0,            AX_LEN+0.20]),
    ]:
        p0 = [0., 0., 0.]; p1 = [0., 0., 0.]
        p0[dim] = -AX_LEN;  p1[dim] = AX_LEN
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
                color=AX_COLOR, linewidth=0.7, alpha=0.6, zorder=1)
        ax.text(*label_end, label, color='#666666', fontsize=10,
                ha='center', va='center', fontweight='bold', zorder=12)

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
              title='Nearest pole', title_fontsize=8.5,
              handletextpad=0.5, labelspacing=0.4)

    ax.view_init(elev=22, azim=35)
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.12, 1.12)
    ax.set_zlim(-1.12, 1.12)

    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('none')
    ax.set_axis_off()

    fig.text(0.50, 0.96,
             'Activation signatures — G-EMV orientation space',
             ha='center', va='top', fontsize=12, color='#222222', fontweight='semibold')
    fig.text(0.50, 0.92,
             r'$n=3000$ perturbations (90% continuous mixes, $\Delta\in[0.5,\,3.5]$) '
             '— 62.7% of mixes within 30° of a pure pole (null: 40.2%)',
             ha='center', va='top', fontsize=8.5, color='#555555')

    fig.canvas.draw()
    M = ax.get_proj()

    pole_label_offset = {
        '+F': (-0.038, -0.026), '+R': (-0.010, -0.030),
        '+S': (+0.045, +0.006), '-F': (+0.032, +0.024),
        '-R': (-0.038, +0.012), '-S': (+0.040, -0.010),
    }

    LABEL_RADIUS = 1.30
    for pole_key, pmeta in POLE_META.items():
        pv = pmeta['vec']
        pc = pmeta['color']
        x2d, y2d, _ = proj_transform(
            pv[0]*LABEL_RADIUS, pv[1]*LABEL_RADIUS, pv[2]*LABEL_RADIUS, M)
        display_xy = ax.transData.transform((x2d, y2d))
        xf, yf    = fig.transFigure.inverted().transform(display_xy)
        ox, oy = pole_label_offset[pole_key]
        fig.text(xf + ox, yf + oy, pole_key,
                 color=pc, fontsize=9, fontweight='bold',
                 ha='center', va='center')

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(OUTFILE, dpi=300, bbox_inches='tight', facecolor='white')
    print(f'Figure saved: {OUTFILE}')
    print(f'Size: {OUTFILE.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()

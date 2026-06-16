"""
Paper result figures — G-EMV model.

Generates five figures in paper style (white background, red/gray palette, 300 dpi):
  fig1_opportunity_blindness.png   — Opportunity blindness
  fig2_activation_optimum.png     — Activation optimum (Yerkes-Dodson)
  fig3_richness_recovery.png  — Orientation richness recovery
  fig4_social_typology.png      — Social typology (three phenotypes)
  fig5_proactivity.png          — Proactivity (decentering as exploration engine)
"""

from __future__ import annotations
import math, random, sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import model as M
from model import State, ModelConfig, DEFAULT_CONFIG, opponent_distance_obs as opp_dist_obs

FIGURES_DIR = Path(__file__).parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# ─── Palette ───────────────────────────────────────────────────────────────────
C_RED    = '#B23B33'
C_RED2   = '#D97070'
C_DKGRAY = '#3D3D3D'
C_MDGRAY = '#7A7A7A'
C_LTGRAY = '#BBBBBB'
C_SPINE  = '#CCCCCC'

ETA = 0.05

# ─── G-EMV dynamics ────────────────────────────────────────────────────────────

def gradient_step(s: State, cfg: ModelConfig = DEFAULT_CONFIG) -> State:
    dpos_F = s.pos_F - cfg.f_pos_target; dpos_R = s.pos_R - cfg.r_pos_target
    dpos_S = s.pos_S - cfg.s_pos_target
    dten_F = s.ten_F - cfg.f_ten_target; dten_R = s.ten_R - cfg.r_ten_target
    dten_S = s.ten_S - cfg.s_ten_target
    sqF = dpos_F**2; sqR = dpos_R**2; sqS = dpos_S**2
    C_F = cfg.sens_F*(sqR+sqS); C_R = cfg.sens_R*(sqF+sqS); C_S = cfg.sens_S*(sqF+sqR)
    W_F = cfg.sens_R*s.ten_R + cfg.sens_S*s.ten_S
    W_R = cfg.sens_F*s.ten_F + cfg.sens_S*s.ten_S
    W_S = cfg.sens_F*s.ten_F + cfg.sens_R*s.ten_R
    G_pF = 2*(cfg.w_f_pos+W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
    G_nF = -2*(cfg.w_f_pos+W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
    G_pR = 2*(cfg.w_r_pos+W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
    G_nR = -2*(cfg.w_r_pos+W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
    G_pS = 2*(cfg.w_s_pos+W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S
    G_nS = -2*(cfg.w_s_pos+W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S
    return State(
        pF=max(0.0, s.pF-ETA*G_pF), nF=max(0.0, s.nF-ETA*G_nF),
        pR=max(0.0, s.pR-ETA*G_pR), nR=max(0.0, s.nR-ETA*G_nR),
        pS=max(0.0, s.pS-ETA*G_pS), nS=max(0.0, s.nS-ETA*G_nS),
    )


def run_traj(init: State, n: int, cfg: ModelConfig = DEFAULT_CONFIG) -> list[State]:
    traj = [init]; s = init
    for _ in range(n):
        s = gradient_step(s, cfg); traj.append(s)
    return traj


# ─── Shared style ──────────────────────────────────────────────────────────────

def _style_ax(ax, title='', xlabel='', ylabel=''):
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_color(C_SPINE)
    ax.tick_params(colors='#555555', length=3)
    ax.grid(True, color='#EEEEEE', linewidth=0.8, zorder=0)
    if title:  ax.set_title(title, fontsize=10, color='#222222', pad=6)
    if xlabel: ax.set_xlabel(xlabel, fontsize=9, color='#444444')
    if ylabel: ax.set_ylabel(ylabel, fontsize=9, color='#444444')


def _save(fig, name: str):
    path = FIGURES_DIR / name
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  -> {path.name}  ({path.stat().st_size // 1024} KB)')


# ══════════════════════════════════════════════════════════════════════════════
# FIG 1 — Opportunity blindness
# ══════════════════════════════════════════════════════════════════════════════

def fig1_ceguera():
    cfg    = DEFAULT_CONFIG
    half_b = M.TEN_BASAL_MIN / 2.0
    DELTA  = 1.5
    N_FLAT = 6
    N_POST = 35

    calma = State(pF=1.0, nF=1.0, pR=half_b, nR=half_b, pS=half_b, nS=half_b)
    tenso = State(pF=3.8, nF=3.8, pR=half_b, nR=half_b, pS=half_b, nS=half_b)

    calma_stim = State(pF=calma.pF+DELTA, nF=calma.nF,
                       pR=calma.pR, nR=calma.nR, pS=calma.pS, nS=calma.nS)
    tenso_stim = State(pF=tenso.pF+DELTA, nF=tenso.nF,
                       pR=tenso.pR, nR=tenso.nR, pS=tenso.pS, nS=tenso.nS)

    calma_traj = run_traj(calma_stim, N_POST, cfg)
    tenso_traj = run_traj(tenso_stim, N_POST, cfg)

    steps_pre  = list(range(-N_FLAT, 1))
    steps_post = list(range(0, N_POST + 1))

    posF_c_pre  = [calma.pos_F] * (N_FLAT + 1)
    posF_t_pre  = [tenso.pos_F] * (N_FLAT + 1)
    posF_c_post = [s.pos_F for s in calma_traj]
    posF_t_post = [s.pos_F for s in tenso_traj]

    d_base_calma = M.opponent_distance(calma, cfg)
    d_base_tenso = M.opponent_distance(tenso, cfg)
    delta_d_calma = M.opponent_distance(calma_stim, cfg) - d_base_calma
    delta_d_tenso = M.opponent_distance(tenso_stim, cfg) - d_base_tenso
    dpF_calma     = calma_stim.pos_F - calma.pos_F
    dpF_tenso     = tenso_stim.pos_F - tenso.pos_F

    from matplotlib.patches import Patch

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), facecolor='white')
    fig.subplots_adjust(wspace=0.38)

    # Left panel: pos_F trajectory
    ax = axes[0]
    _style_ax(ax, 'pos_F after the opportunity  (δ = 1.5)',
              'Step  (0 = stimulus)', 'Physical position  pos_F')

    ax.axvspan(-N_FLAT, 0, color='#F5F5F5', zorder=0)
    ax.axvline(0, color=C_LTGRAY, linewidth=0.9, linestyle='--')
    ax.text(0.5, 0.03, 'stimulus', fontsize=7.5, color='#AAAAAA',
            transform=ax.get_xaxis_transform(), ha='left', va='bottom')

    ax.plot(steps_pre,  posF_c_pre,  color=C_RED,    linewidth=1.8, alpha=0.4, zorder=3)
    ax.plot(steps_post, posF_c_post, color=C_RED,    linewidth=2.4,
            label='Calm   (ten_F = 2.0)', zorder=4)
    ax.plot(steps_pre,  posF_t_pre,  color=C_DKGRAY, linewidth=1.8, alpha=0.4, zorder=3)
    ax.plot(steps_post, posF_t_post, color=C_DKGRAY, linewidth=2.4,
            label='Saturated (ten_F = 7.6)', zorder=4)

    ax.annotate(f'Δpos_F = +{dpF_calma:.2f}',
                xy=(0, calma_stim.pos_F), xytext=(5, calma_stim.pos_F + 0.12),
                fontsize=8.5, color=C_RED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.1))
    ax.annotate(f'+{dpF_tenso:.2f}',
                xy=(0, tenso_stim.pos_F), xytext=(5, tenso_stim.pos_F - 0.35),
                fontsize=8.5, color=C_DKGRAY, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=C_DKGRAY, lw=1.1))

    ax.axhline(cfg.f_pos_target, color=C_LTGRAY, linewidth=0.8, linestyle=':')
    ax.text(N_POST - 1, cfg.f_pos_target + 0.06, 'equilibrium',
            fontsize=7.5, color=C_LTGRAY, ha='right')
    ax.set_ylim(-0.15, 2.15)
    ax.legend(fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE, loc='upper right')

    # Right panel: comparative bar chart
    ax = axes[1]
    _style_ax(ax, 'Response magnitude to stimulus', '', '')

    x_pos = np.array([0.0, 1.25])
    bar_w = 0.44
    metric_labels = ['Δpos_F\n(perceived jump)', 'Δd\n(generated urgency)']
    calma_vals    = [dpF_calma,     delta_d_calma]
    tenso_vals    = [dpF_tenso,     delta_d_tenso]

    for xi, (lbl, vc, vt) in zip(x_pos, zip(metric_labels, calma_vals, tenso_vals)):
        ax.bar(xi - bar_w/2, vc, bar_w, color=C_RED,    alpha=0.88, zorder=3)
        ax.bar(xi + bar_w/2, vt, bar_w, color=C_DKGRAY, alpha=0.88, zorder=3)
        yoff = max(vc, vt) * 0.04
        ax.text(xi - bar_w/2, vc + yoff, f'{vc:.2f}',
                ha='center', va='bottom', fontsize=9.5, color=C_RED, fontweight='bold')
        ax.text(xi + bar_w/2, vt + yoff, f'{vt:.2f}',
                ha='center', va='bottom', fontsize=9.5, color=C_DKGRAY, fontweight='bold')
        ax.text(xi, -0.05, lbl, ha='center', fontsize=8.5, color='#444444',
                transform=ax.get_xaxis_transform(), va='top')

    ax.set_xlim(-0.55, 1.80)
    ymax = max(dpF_calma, delta_d_calma) * 1.30
    ax.set_ylim(0, ymax)
    ax.set_xticks([])
    ax.spines['bottom'].set_visible(False)

    ax.legend(handles=[Patch(color=C_RED,    label='Calm   (ten_F = 2.0)'),
                        Patch(color=C_DKGRAY, label='Saturated (ten_F = 7.6)')],
              fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE, loc='upper right')

    ratio_d = delta_d_calma / max(delta_d_tenso, 1e-9)
    ax.text(0.5, 0.98,
            f'Saturated: ×{ratio_d:.0f} less homeostatic urgency (Δd)',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=8, color='#555555', style='italic')

    fig.suptitle('Opportunity blindness', fontsize=12, color='#222222',
                 fontweight='semibold', y=1.01)
    _save(fig, 'fig1_opportunity_blindness.png')


# ══════════════════════════════════════════════════════════════════════════════
# FIG 2 — Activation optimum (Yerkes-Dodson)
# ══════════════════════════════════════════════════════════════════════════════

def fig2_optimo():
    cfg = DEFAULT_CONFIG
    DELTA, N_POST = 1.5, 80
    half_b = M.TEN_BASAL_MIN / 2.0

    ten_vals = np.linspace(1.5, 7.95, 35)
    delta_d_abs = []
    delta_d_rel = []
    peak_posF   = []

    for lv in ten_vals:
        half = lv / 2.0
        init = State(pF=half, nF=half, pR=half_b, nR=half_b, pS=half_b, nS=half_b)
        stim = State(pF=init.pF+DELTA, nF=init.nF, pR=init.pR,
                     nR=init.nR, pS=init.pS, nS=init.nS)
        d_base = M.opponent_distance(init, cfg)
        d_stim = M.opponent_distance(stim, cfg)
        traj = run_traj(stim, N_POST, cfg)
        peak = max(s.pos_F for s in traj)
        delta_d_abs.append(d_stim - d_base)
        delta_d_rel.append((d_stim - d_base) / d_base * 100)
        peak_posF.append(peak)

    best_idx = int(np.argmax(delta_d_abs))
    best_ten = ten_vals[best_idx]
    best_dd  = delta_d_abs[best_idx]

    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor='white')
    _style_ax(ax, 'Activation optimum for an opportunity stimulus (δ = 1.5)',
              'Baseline physical tension  ten_F', 'Homeostatic Δd (post − pre stimulus)')

    ax.axvspan(M.VOL_MAX - 1.5, M.VOL_MAX, color='#F5DCDC', alpha=0.5, zorder=0,
               label=f'Saturation zone (ten_F > {M.VOL_MAX-1.5})')
    ax.axvline(M.VOL_MAX, color=C_RED2, linewidth=0.8, linestyle=':')
    ax.text(M.VOL_MAX - 0.05, max(delta_d_abs)*0.98, f'VOL_MAX={M.VOL_MAX}',
            ha='right', fontsize=7.5, color=C_RED2, va='top')

    ax.plot(ten_vals, delta_d_abs, color=C_RED, linewidth=2.4, zorder=4)
    ax.fill_between(ten_vals, 0, delta_d_abs, color=C_RED, alpha=0.12, zorder=2)
    ax.axhline(0, color=C_LTGRAY, linewidth=0.8, linestyle='--')

    ax.scatter([best_ten], [best_dd], color=C_RED, s=80, zorder=6)
    ax.annotate(f'Peak: Δd={best_dd:.2f}\n(ten_F ≈ {best_ten:.1f})',
                xy=(best_ten, best_dd), xytext=(best_ten - 2.2, best_dd - 0.10),
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.2),
                fontsize=8.5, color=C_RED)

    for (tf, label, col) in [(2.0, 'Calm', C_RED), (7.6, 'Saturated', C_DKGRAY)]:
        half = tf / 2.0
        init = State(pF=half, nF=half, pR=half_b, nR=half_b, pS=half_b, nS=half_b)
        stim = State(pF=init.pF+DELTA, nF=init.nF, pR=init.pR,
                     nR=init.nR, pS=init.pS, nS=init.nS)
        dd = M.opponent_distance(stim, cfg) - M.opponent_distance(init, cfg)
        ax.scatter([tf], [dd], color=col, s=70, zorder=7, marker='D',
                   edgecolors='white', linewidths=0.8)
        ax.annotate(label, xy=(tf, dd), xytext=(tf+0.15, dd+0.04),
                    fontsize=8, color=col, va='bottom')

    ax.legend(fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE, loc='upper left')
    ax.set_xlim(1.0, 8.3)

    fig.suptitle('Activation optimum  —  Yerkes-Dodson curve of the G-EMV model',
                 fontsize=11, color='#222222', fontweight='semibold', y=1.01)
    _save(fig, 'fig2_activation_optimum.png')


# ══════════════════════════════════════════════════════════════════════════════
# FIG 3 — Orientation richness recovery
# ══════════════════════════════════════════════════════════════════════════════

def richness(s: State) -> float:
    basal = M.TEN_BASAL_MIN
    excs  = [max(0.0, t - basal) for t in (s.ten_F, s.ten_R, s.ten_S)]
    total = sum(excs)
    if total < 1e-12: return 1.0
    H = sum(-p*math.log(p) for e in excs if (p := e/total) > 1e-12)
    return H / math.log(3)


def fig3_riqueza():
    cfg = DEFAULT_CONFIG
    N_DYN = 80

    cepa = State(pF=3.5, nF=3.5,
                 pR=M.TEN_BASAL_MIN/2, nR=M.TEN_BASAL_MIN/2,
                 pS=M.TEN_BASAL_MIN/2, nS=M.TEN_BASAL_MIN/2)
    traj = run_traj(cepa, N_DYN, cfg)
    steps  = list(range(N_DYN+1))
    R_vals = [richness(s) for s in traj]
    tenF   = [s.ten_F for s in traj]
    tenR   = [s.ten_R for s in traj]
    tenS   = [s.ten_S for s in traj]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), facecolor='white')
    fig.subplots_adjust(wspace=0.35)

    # Left panel: richness index R(t)
    ax = axes[0]
    _style_ax(ax, 'Orientation richness R(t)',
              'Steps (no external stimulus)', 'Richness R  [0 = one axis, 1 = distributed]')
    ax.axhline(math.log(2)/math.log(3), color=C_LTGRAY, linewidth=0.8, linestyle=':',
               label='2 equal axes (R≈0.631)')
    ax.axhline(1.0, color=C_LTGRAY, linewidth=0.8, linestyle='--',
               label='Maximum richness (R=1)')
    ax.plot(steps, R_vals, color=C_RED, linewidth=2.4, zorder=4)
    ax.fill_between(steps, R_vals[0], R_vals, color=C_RED, alpha=0.12)

    ax.scatter([0], [R_vals[0]], color=C_DKGRAY, s=55, zorder=6,
               label='Start: R=0 (zeppelin)')
    ax.scatter([N_DYN], [R_vals[-1]], color=C_RED, s=55, zorder=6,
               label=f'End: R={R_vals[-1]:.2f}')
    ax.set_ylim(-0.04, 1.08)
    ax.legend(fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE, loc='lower right')

    # Right panel: tension evolution by axis
    ax = axes[1]
    _style_ax(ax, 'Tension redistribution by axis',
              'Steps', 'Tension ten_a')
    ax.plot(steps, tenF, color=C_RED, linewidth=2.2, label='ten_F  (physical)')
    ax.plot(steps, tenR, color=C_MDGRAY, linewidth=2.0, linestyle='--',
            label='ten_R  (resource)')
    ax.plot(steps, tenS, color=C_LTGRAY, linewidth=1.8, linestyle=':',
            label='ten_S  (social)')
    ax.axhline(M.TEN_BASAL_MIN, color='#EEEEEE', linewidth=0.8)
    ax.text(1, M.TEN_BASAL_MIN+0.04, 'TBM', fontsize=7, color=C_LTGRAY)
    ax.legend(fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE)

    fig.suptitle('Orientation richness recovery  —  coupling dynamics',
                 fontsize=11, color='#222222', fontweight='semibold', y=1.01)
    _save(fig, 'fig3_richness_recovery.png')


# ══════════════════════════════════════════════════════════════════════════════
# FIG 4 — Social typology (three phenotypes)
# ══════════════════════════════════════════════════════════════════════════════

def fig4_tipologia():
    GRID_B    = 20
    STEPS_B   = 300
    SOCIAL_R  = GRID_B // 2
    SOCIAL_C  = GRID_B // 2
    S_SIGMA   = 4.0
    S_MAX     = 1.5
    HP_B      = 90.0
    ENERGY_B  = 15.0

    _base = dict(
        f_pos_target=0.4, r_pos_target=1.0,
        f_ten_target=0.2, r_ten_target=0.2, s_ten_target=0.1,
        w_f_pos=1.0, w_r_pos=0.8,
        sens_F=0.0, sens_R=0.0, sens_S=0.0,
    )
    CFG_POS = ModelConfig(s_pos_target=+1.0, w_s_pos=0.8, **_base)
    CFG_NEU = ModelConfig(s_pos_target= 0.0, w_s_pos=0.0, **_base)
    CFG_NEG = ModelConfig(s_pos_target=-1.0, w_s_pos=0.8, **_base)

    def social_field(r, c):
        d = math.sqrt((r-SOCIAL_R)**2 + (c-SOCIAL_C)**2)
        return S_MAX * math.exp(-d / S_SIGMA)

    def dist_grid(r, c):
        return math.sqrt((r-SOCIAL_R)**2 + (c-SOCIAL_C)**2)

    def sim_b(cfg_b, seed):
        rng = random.Random(seed)
        r, c = 1, 1
        moves = [(0,0),(-1,0),(1,0),(0,-1),(0,1)]
        positions  = [(r, c)]
        dist_trace = [dist_grid(r, c)]
        s_trace    = [social_field(r, c)]

        for _ in range(STEPS_B):
            if cfg_b.w_s_pos == 0.0:
                dr, dc = rng.choice(moves)
            else:
                best_d, best_move = float('inf'), (0, 0)
                for dr, dc in moves:
                    nr = max(0, min(GRID_B-1, r+dr)); nc = max(0, min(GRID_B-1, c+dc))
                    ns = social_field(nr, nc)
                    d  = opp_dist_obs(HP_B, ENERGY_B, ns, cfg_b)
                    if d < best_d: best_d, best_move = d, (dr, dc)
                dr, dc = best_move
            r = max(0, min(GRID_B-1, r+dr)); c = max(0, min(GRID_B-1, c+dc))
            positions.append((r, c))
            dist_trace.append(dist_grid(r, c))
            s_trace.append(social_field(r, c))
        return {'positions': positions, 'dist_trace': dist_trace, 's_trace': s_trace}

    seed = 7
    res_pos = sim_b(CFG_POS, seed)
    res_neu = sim_b(CFG_NEU, seed)
    res_neg = sim_b(CFG_NEG, seed)

    steps = list(range(STEPS_B+1))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), facecolor='white')
    fig.subplots_adjust(wspace=0.38)

    # Left panel: trajectories on the grid
    ax = axes[0]
    _style_ax(ax, 'Trajectories in the social environment', 'Column', 'Row')
    labels_traj = ['Positive (seeks bond)', 'Neutral (indifferent)', 'Negative (avoids)']
    colors_traj = [C_RED, C_MDGRAY, C_DKGRAY]
    for res, label, col in zip([res_pos, res_neu, res_neg], labels_traj, colors_traj):
        rs = [p[0] for p in res['positions']]
        cs = [p[1] for p in res['positions']]
        ax.plot(cs, rs, color=col, alpha=0.7, linewidth=1.4, label=label)
        ax.scatter(cs[0],  rs[0],  color=col, marker='o', s=55, zorder=5, edgecolors='white', lw=0.8)
        ax.scatter(cs[-1], rs[-1], color=col, marker='^', s=70, zorder=5, edgecolors='white', lw=0.8)
    ax.scatter(SOCIAL_C, SOCIAL_R, color='#D4A017', marker='*', s=280, zorder=10,
               edgecolors='#888888', linewidth=0.8, label='Social stimulus')
    xs_g = np.arange(GRID_B); ys_g = np.arange(GRID_B)
    sf_map = np.array([[social_field(rr, cc) for cc in xs_g] for rr in ys_g])
    ax.contourf(xs_g, ys_g, sf_map, levels=5, cmap='Reds', alpha=0.10, zorder=0)
    ax.set_xlim(-0.5, GRID_B-0.5); ax.set_ylim(-0.5, GRID_B-0.5)
    ax.set_aspect('equal')
    ax.legend(fontsize=8, framealpha=0.9, edgecolor=C_SPINE, loc='upper right')

    # Right panel: social signal received s(t)
    ax = axes[1]
    _style_ax(ax, 'Social signal received  s(t)', 'Step',
              'Social signal  s  (0 = none, 1.5 = maximum)')
    for res, label, col in zip([res_pos, res_neu, res_neg], labels_traj, colors_traj):
        s_raw = res['s_trace']
        s_sm  = [float(np.mean(s_raw[max(0,i-25):i+1])) for i in range(len(s_raw))]
        ax.plot(steps, s_sm, color=col, linewidth=2.0, label=label, alpha=0.9)
    ax.axhline(0, color=C_LTGRAY, linewidth=0.7, linestyle='--')
    ax.set_ylim(-0.05, S_MAX * 1.15)
    ax.legend(fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE, loc='upper right')

    fig.suptitle('Social typology  —  three phenotypes by S-axis decentering',
                 fontsize=11, color='#222222', fontweight='semibold', y=1.01)
    _save(fig, 'fig4_social_typology.png')


# ══════════════════════════════════════════════════════════════════════════════
# FIG 5 — Proactivity (decentering as engine of exploration)
# ══════════════════════════════════════════════════════════════════════════════

def fig5_proactividad():
    GRID_A     = 10
    STEPS_A    = 500
    HP_DECAY   = 0.10
    ENERGY_DEC = 0.05
    MOVE_SCALE = 3.0
    WINDOW     = 20

    CFG_CENTRADO = ModelConfig(
        f_pos_target=0.0, r_pos_target=0.0, s_pos_target=0.0,
        f_ten_target=0.0, r_ten_target=0.0, s_ten_target=0.0,
        sens_F=0.0, sens_R=0.0, sens_S=0.0,
    )
    CFG_POSITIVO = ModelConfig(f_pos_target=1.0, r_pos_target=2.0, s_pos_target=0.8)
    CFG_NEGATIVO = ModelConfig(
        f_pos_target=-1.0, r_pos_target=-2.0, s_pos_target=-0.8,
        sens_F=0.0, sens_R=0.0, sens_S=0.0,
    )

    def sim_a(cfg_a, seed):
        rng = random.Random(seed)
        x, y = GRID_A//2, GRID_A//2
        hp = M.HP_EQ; energy = M.ENERGY_EQ; s_val = 0.0
        visited = {(x, y)}
        move_probs = []; distances = []
        for _ in range(STEPS_A):
            hp     = max(0.0, hp     - HP_DECAY)
            energy = max(0.0, energy - ENERGY_DEC)
            d = opp_dist_obs(hp, energy, s_val, cfg_a)
            prob = min(1.0, d / MOVE_SCALE)
            move_probs.append(prob); distances.append(d)
            if rng.random() < prob:
                dx, dy = rng.choice([(-1,0),(1,0),(0,-1),(0,1)])
                x = max(0, min(GRID_A-1, x+dx)); y = max(0, min(GRID_A-1, y+dy))
                visited.add((x, y))
        return {'visited': len(visited), 'move_probs': move_probs, 'distances': distances}

    seed = 42
    agents = [
        ('Positive (decentered +)', CFG_POSITIVO, C_RED),
        ('Centered (target = 0)',   CFG_CENTRADO, C_MDGRAY),
        ('Negative (decentered −)', CFG_NEGATIVO, C_DKGRAY),
    ]
    results = [(lbl, col, sim_a(cfg_a, seed)) for lbl, cfg_a, col in agents]

    def smooth(series, w=WINDOW):
        return [float(np.mean(series[max(0,i-w):i+1])) for i in range(len(series))]

    steps = list(range(STEPS_A))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), facecolor='white')
    fig.subplots_adjust(wspace=0.35)

    # Left panel: movement probability (moving average)
    ax = axes[0]
    _style_ax(ax, 'Motor activity (movement probability)',
              'Step', f'Movement prob. ({WINDOW}-step moving average)')
    ax.axvline(100, color=C_LTGRAY, linewidth=0.8, linestyle=':', alpha=0.7)
    ax.text(102, 0.06, 'step 100', fontsize=7.5, color=C_LTGRAY)
    for lbl, col, r in results:
        sm = smooth(r['move_probs'])
        ax.plot(steps, sm, color=col, linewidth=2.0, label=lbl, alpha=0.9)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE, loc='lower right')

    # Right panel: cumulative cells explored
    def sim_a_cumulative(cfg_a, seed):
        rng = random.Random(seed)
        x, y = GRID_A//2, GRID_A//2
        hp = M.HP_EQ; energy = M.ENERGY_EQ; s_val = 0.0
        visited = {(x, y)}; visited_by_step = [1]
        move_probs_list = []
        for _ in range(STEPS_A):
            hp     = max(0.0, hp     - HP_DECAY)
            energy = max(0.0, energy - ENERGY_DEC)
            d = opp_dist_obs(hp, energy, s_val, cfg_a)
            prob = min(1.0, d / MOVE_SCALE)
            move_probs_list.append(prob)
            if rng.random() < prob:
                dx, dy = rng.choice([(-1,0),(1,0),(0,-1),(0,1)])
                x = max(0, min(GRID_A-1, x+dx)); y = max(0, min(GRID_A-1, y+dy))
                visited.add((x, y))
            visited_by_step.append(len(visited))
        return visited_by_step, move_probs_list

    ax = axes[1]
    _style_ax(ax, 'Cumulative environment exploration', 'Step', 'Distinct cells visited')
    ax.axhline(GRID_A**2, color=C_LTGRAY, linewidth=0.8, linestyle='--')
    ax.text(10, GRID_A**2 + 0.5, f'Total cells ({GRID_A}×{GRID_A}={GRID_A**2})',
            fontsize=7.5, color=C_LTGRAY)

    steps_ext = list(range(STEPS_A+1))
    for lbl, col, cfg_a in [(a[0], a[2], a[1]) for a in agents]:
        visited_steps, _ = sim_a_cumulative(cfg_a, seed)
        ax.plot(steps_ext, visited_steps, color=col, linewidth=2.0, label=lbl, alpha=0.9)
        ax.text(STEPS_A + 2, visited_steps[-1], f'{visited_steps[-1]}',
                fontsize=8, color=col, va='center')

    ax.set_xlim(0, STEPS_A + 30)
    ax.set_ylim(0, GRID_A**2 + 5)
    ax.legend(fontsize=8.5, framealpha=0.9, edgecolor=C_SPINE, loc='lower right')

    fig.suptitle('Proactivity  —  decentering as an engine of exploration',
                 fontsize=11, color='#222222', fontweight='semibold', y=1.01)
    _save(fig, 'fig5_proactivity.png')


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('Generating English figures...')
    fig1_ceguera()
    fig2_optimo()
    fig3_riqueza()
    fig4_tipologia()
    fig5_proactividad()
    print('Done.')

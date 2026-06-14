"""
Variante del experimento dinámico: estímulo INMEDIATO (N_REPOSO=0).

Pregunta: cuando la tensión todavía está viva (sin tiempo para relajarse),
¿responden distinto CALMA (ten_F=2.0) y TENSO (ten_F=7.6) al estímulo?

Diferencia respecto al experimento anterior:
  - N_REPOSO=0: el estímulo se aplica directamente al estado inicial,
    con toda la diferencia de tensión intacta.
  - Se registra el TRANSITORIO completo: d paso a paso para todos los casos.

Misma dinámica (descenso de gradiente exacto de d²), mismos agentes,
mismos estímulos (PELIGRO δ en nF, OPORTUNIDAD δ en pF), mismas cuatro métricas.

Agentes:
  CALMA:  pF=1.0, nF=1.0  →  pos_F=0, ten_F=2.0
  TENSO:  pF=3.8, nF=3.8  →  pos_F=0, ten_F=7.6

Nota sobre VOL_MAX: el estímulo (δ=1.5) lleva a ten_F=9.1 en TENSO,
por encima del techo (8.0). __post_init__ aplica el techo asimétrico:
el excedente se recorta conservando la relación f⁺/f⁻ → ten_F=7.80,
pos_F se escala proporcionalmente (pos_F=-1.286 en lugar de -1.5).
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Tuple

try:
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

import model as M
from model import State, ModelConfig, DEFAULT_CONFIG

# ─── Parámetros ──────────────────────────────────────────────────────────────

ETA: float    = 0.05   # paso de descenso de gradiente (idéntico al original)
N_POST: int   = 80     # pasos tras el estímulo
DELTA: float  = 1.5    # magnitud del estímulo

THRESH_VEL: float = 0.02   # umbral de respuesta en pos_F
THRESH_REC: float = 0.05   # margen de recuperación en d

FIGURES_DIR = Path(__file__).parent / "figures"


# ─── Dinámica ─────────────────────────────────────────────────────────────────

def gradient_step(state: State, cfg: ModelConfig = DEFAULT_CONFIG) -> State:
    """Un paso de descenso de gradiente de d²(state, cfg).

    Gradiente exacto:
      ∂d²/∂f⁺_a = +2*(w_a^pos + W_a)*Δpos_a + 2*w_a^ten*Δten_a + C_a
      ∂d²/∂f⁻_a = -2*(w_a^pos + W_a)*Δpos_a + 2*w_a^ten*Δten_a + C_a
    """
    dpos_F = state.pos_F - cfg.f_pos_target
    dpos_R = state.pos_R - cfg.r_pos_target
    dpos_S = state.pos_S - cfg.s_pos_target
    dten_F = state.ten_F - cfg.f_ten_target
    dten_R = state.ten_R - cfg.r_ten_target
    dten_S = state.ten_S - cfg.s_ten_target

    sqF = dpos_F ** 2
    sqR = dpos_R ** 2
    sqS = dpos_S ** 2

    C_F = cfg.sens_F * (sqR + sqS)
    C_R = cfg.sens_R * (sqF + sqS)
    C_S = cfg.sens_S * (sqF + sqR)

    W_F = cfg.sens_R * state.ten_R + cfg.sens_S * state.ten_S
    W_R = cfg.sens_F * state.ten_F + cfg.sens_S * state.ten_S
    W_S = cfg.sens_F * state.ten_F + cfg.sens_R * state.ten_R

    G_pF = 2 * (cfg.w_f_pos + W_F) * dpos_F + 2 * cfg.w_f_ten * dten_F + C_F
    G_nF = -2 * (cfg.w_f_pos + W_F) * dpos_F + 2 * cfg.w_f_ten * dten_F + C_F
    G_pR = 2 * (cfg.w_r_pos + W_R) * dpos_R + 2 * cfg.w_r_ten * dten_R + C_R
    G_nR = -2 * (cfg.w_r_pos + W_R) * dpos_R + 2 * cfg.w_r_ten * dten_R + C_R
    G_pS = 2 * (cfg.w_s_pos + W_S) * dpos_S + 2 * cfg.w_s_ten * dten_S + C_S
    G_nS = -2 * (cfg.w_s_pos + W_S) * dpos_S + 2 * cfg.w_s_ten * dten_S + C_S

    return State(
        pF=max(0.0, state.pF - ETA * G_pF),
        nF=max(0.0, state.nF - ETA * G_nF),
        pR=max(0.0, state.pR - ETA * G_pR),
        nR=max(0.0, state.nR - ETA * G_nR),
        pS=max(0.0, state.pS - ETA * G_pS),
        nS=max(0.0, state.nS - ETA * G_nS),
    )


def run_trajectory(initial: State, n_steps: int,
                   cfg: ModelConfig = DEFAULT_CONFIG) -> List[State]:
    traj = [initial]
    s = initial
    for _ in range(n_steps):
        s = gradient_step(s, cfg)
        traj.append(s)
    return traj


# ─── Estímulos ───────────────────────────────────────────────────────────────

def apply_peligro(state: State) -> State:
    return State(pF=state.pF, nF=state.nF + DELTA,
                 pR=state.pR, nR=state.nR,
                 pS=state.pS, nS=state.nS)


def apply_oportunidad(state: State) -> State:
    return State(pF=state.pF + DELTA, nF=state.nF,
                 pR=state.pR, nR=state.nR,
                 pS=state.pS, nS=state.nS)


# ─── Métricas ─────────────────────────────────────────────────────────────────

def compute_metrics(pre_stim: State, post_traj: List[State],
                    cfg: ModelConfig = DEFAULT_CONFIG) -> dict:
    """
    pre_stim    = estado justo ANTES del estímulo (= inicial, puesto que N_REPOSO=0)
    post_traj   = lista de N_POST+1 estados; [0] es el estado inmediatamente
                  tras aplicar el estímulo (antes del primer paso de dinámica).
    """
    pos_F_base = pre_stim.pos_F
    d_base = M.opponent_distance(pre_stim, cfg)

    # 1. Velocidad: primer índice donde |pos_F - base| > THRESH_VEL
    velocidad = len(post_traj)
    for i, s in enumerate(post_traj):
        if abs(s.pos_F - pos_F_base) > THRESH_VEL:
            velocidad = i
            break

    # 2. Intensidad: mayor |Δpos_F| entre pasos consecutivos
    deltas = [abs(post_traj[i + 1].pos_F - post_traj[i].pos_F)
              for i in range(len(post_traj) - 1)]
    intensidad = max(deltas) if deltas else 0.0

    # 3. Propagación: cambio máximo acumulado en R y S
    max_dR = max(abs(s.pos_R - pre_stim.pos_R) for s in post_traj)
    max_dS = max(abs(s.pos_S - pre_stim.pos_S) for s in post_traj)
    propagacion = max_dR + max_dS

    # 4. Recuperación: primer i donde |d(i) - d_base| ≤ THRESH_REC
    recuperacion = len(post_traj)
    for i, s in enumerate(post_traj):
        if abs(M.opponent_distance(s, cfg) - d_base) <= THRESH_REC:
            recuperacion = i
            break

    return {
        "velocidad": velocidad,
        "intensidad": intensidad,
        "propagacion": propagacion,
        "recuperacion": recuperacion,
        "d_base": d_base,
        "d_stim": M.opponent_distance(post_traj[0], cfg),
        "d_final": M.opponent_distance(post_traj[-1], cfg),
    }


# ─── Transitorio ─────────────────────────────────────────────────────────────

def print_transitorio(label: str, pre_stim: State, post_traj: List[State],
                      cfg: ModelConfig = DEFAULT_CONFIG) -> None:
    checkpoints = [0, 1, 2, 3, 5, 8, 13, 20, 30, 50, 80]
    checkpoints = [t for t in checkpoints if t < len(post_traj)]
    d_base = M.opponent_distance(pre_stim, cfg)
    print(f"\n  Transitorio {label}  (d_base_pre={d_base:.3f})")
    print(f"  {'paso':>5}  {'d':>7}  {'pos_F':>7}  {'ten_F':>7}  {'pos_R':>7}  {'pos_S':>7}")
    print(f"  {'─'*47}")
    for t in checkpoints:
        s = post_traj[t]
        print(f"  {t:>5}  {M.opponent_distance(s, cfg):>7.3f}  "
              f"{s.pos_F:>7.3f}  {s.ten_F:>7.3f}  "
              f"{s.pos_R:>7.3f}  {s.pos_S:>7.3f}")


# ─── Experimento principal ───────────────────────────────────────────────────

def run_experiment() -> None:
    cfg = DEFAULT_CONFIG
    half_basal = M.TEN_BASAL_MIN / 2.0

    calma_0 = State(pF=1.0, nF=1.0,
                    pR=half_basal, nR=half_basal,
                    pS=half_basal, nS=half_basal)
    tenso_0 = State(pF=3.8, nF=3.8,
                    pR=half_basal, nR=half_basal,
                    pS=half_basal, nS=half_basal)

    print("\n═══════════════════════════════════════════════════════════════════")
    print("  Dinámica inmediata: CALMA vs. TENSO — estímulo sin reposo previo")
    print("═══════════════════════════════════════════════════════════════════")
    print(f"  η={ETA}, N_post={N_POST}, δ={DELTA}, N_reposo=0")
    print(f"  CALMA  inicial: pos_F={calma_0.pos_F:.3f}, ten_F={calma_0.ten_F:.3f}, "
          f"d={M.opponent_distance(calma_0, cfg):.3f}")
    print(f"  TENSO  inicial: pos_F={tenso_0.pos_F:.3f}, ten_F={tenso_0.ten_F:.3f}, "
          f"d={M.opponent_distance(tenso_0, cfg):.3f}")

    agents     = [("CALMA",  calma_0), ("TENSO", tenso_0)]
    stimuli    = [("PELIGRO", apply_peligro), ("OPORTUNIDAD", apply_oportunidad)]
    all_results: dict = {}

    for agent_name, init_state in agents:
        all_results[agent_name] = {}
        for stim_name, apply_stim in stimuli:
            stim_state = apply_stim(init_state)
            post_traj  = run_trajectory(stim_state, N_POST, cfg)
            metrics    = compute_metrics(init_state, post_traj, cfg)

            all_results[agent_name][stim_name] = {
                "init_state": init_state,
                "stim_state": stim_state,
                "post_traj":  post_traj,
                "metrics":    metrics,
            }

    # ── Impresión de resultados ───────────────────────────────────────────────

    for agent_name, init_state in agents:
        print(f"\n{'─'*67}")
        print(f"  Agente: {agent_name}")
        print(f"{'─'*67}")
        for stim_name, _ in stimuli:
            res     = all_results[agent_name][stim_name]
            m       = res["metrics"]
            stim_s  = res["stim_state"]

            print(f"\n  Estímulo: {stim_name}")
            print(f"    Estado inicial:     pos_F={init_state.pos_F:.3f}, "
                  f"ten_F={init_state.ten_F:.3f}, d={m['d_base']:.3f}")
            print(f"    Tras estímulo (t=0): pos_F={stim_s.pos_F:.3f}, "
                  f"ten_F={stim_s.ten_F:.3f}, d={m['d_stim']:.3f}  "
                  f"(Δd={m['d_stim']-m['d_base']:+.3f})")
            print(f"    d_final (paso {N_POST}):  {m['d_final']:.3f}")
            print(f"    1. Velocidad:       {m['velocidad']} pasos")
            print(f"    2. Intensidad:      {m['intensidad']:.4f} (max |Δpos_F|/paso)")
            print(f"    3. Propagación:     {m['propagacion']:.4f} (max ΔR + max ΔS)")
            print(f"    4. Recuperación:    {m['recuperacion']} pasos")

            print_transitorio(
                f"{agent_name}/{stim_name}",
                res["init_state"],
                res["post_traj"],
                cfg,
            )

    # ── Tabla comparativa ─────────────────────────────────────────────────────
    print(f"\n{'─'*67}")
    print("  Tabla comparativa")
    print(f"{'─'*67}")
    header = (f"  {'Métrica':<24} {'CALMA/PEL':>10} {'TENSO/PEL':>10}"
              f" {'CALMA/OPO':>10} {'TENSO/OPO':>10}")
    print(header)
    print("  " + "─" * 64)
    for key, label in [
        ("d_stim",       "d inmediata post-estím."),
        ("velocidad",    "Velocidad (pasos)"),
        ("intensidad",   "Intensidad"),
        ("propagacion",  "Propagación"),
        ("recuperacion", "Recuperación (pasos)"),
        ("d_final",      "d_final"),
    ]:
        vals = [
            all_results["CALMA"]["PELIGRO"]["metrics"][key],
            all_results["TENSO"]["PELIGRO"]["metrics"][key],
            all_results["CALMA"]["OPORTUNIDAD"]["metrics"][key],
            all_results["TENSO"]["OPORTUNIDAD"]["metrics"][key],
        ]
        if key in ("velocidad", "recuperacion"):
            row = [str(v) for v in vals]
        else:
            row = [f"{v:.4f}" for v in vals]
        print(f"  {label:<24} {row[0]:>10} {row[1]:>10} {row[2]:>10} {row[3]:>10}")

    if HAS_PLOT:
        _make_figures(all_results, cfg)
    else:
        print("\nAVISO: matplotlib no disponible, figuras omitidas.")


# ─── Figuras ──────────────────────────────────────────────────────────────────

def _make_figures(all_results: dict, cfg: ModelConfig) -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    colors  = {"CALMA": "#2c7bb6", "TENSO": "#d7191c"}
    t_steps = list(range(N_POST + 1))

    for stim_name in ("PELIGRO", "OPORTUNIDAD"):
        fig = plt.figure(figsize=(13, 10))
        fig.suptitle(
            f"Dinámica inmediata — Estímulo: {stim_name}  "
            f"(η={ETA}, δ={DELTA}, N_reposo=0)",
            fontsize=12,
        )
        gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.38, wspace=0.30)

        for col, agent_name in enumerate(("CALMA", "TENSO")):
            res   = all_results[agent_name][stim_name]
            traj  = res["post_traj"]
            c     = colors[agent_name]
            init  = res["init_state"]

            d_vals    = [M.opponent_distance(s, cfg) for s in traj]
            posF_vals = [s.pos_F for s in traj]
            tenF_vals = [s.ten_F for s in traj]
            posR_vals = [s.pos_R for s in traj]
            posS_vals = [s.pos_S for s in traj]

            # Panel 0: distancia homeostática completa
            ax0 = fig.add_subplot(gs[0, col])
            ax0.set_title(
                f"{agent_name}  (d_0={M.opponent_distance(init, cfg):.3f} → "
                f"d_estím={d_vals[0]:.3f})",
                fontsize=10,
            )
            ax0.axhline(M.opponent_distance(init, cfg), color="gray",
                        linestyle="--", alpha=0.5, label="d pre-estím")
            ax0.plot(t_steps, d_vals, color=c, linewidth=2)
            ax0.set_ylabel("d homeostática")
            ax0.legend(fontsize=8)
            ax0.grid(True, alpha=0.25)

            # Panel 1: pos_F y ten_F
            ax1 = fig.add_subplot(gs[1, col])
            ax1.plot(t_steps, posF_vals, color=c, linewidth=2, label="pos_F")
            ax1_r = ax1.twinx()
            ax1_r.plot(t_steps, tenF_vals, color=c, linewidth=1.5,
                       linestyle=":", alpha=0.6, label="ten_F")
            ax1.axhline(cfg.f_pos_target, color="gray", linestyle="--",
                        alpha=0.5, label=f"target pos_F={cfg.f_pos_target}")
            ax1.set_ylabel("pos_F")
            ax1_r.set_ylabel("ten_F", alpha=0.6)
            ax1.legend(loc="lower right", fontsize=8)
            ax1_r.legend(loc="upper right", fontsize=8)
            ax1.grid(True, alpha=0.25)

            # Panel 2: pos_R, pos_S (propagación)
            ax2 = fig.add_subplot(gs[2, col])
            ax2.plot(t_steps, posR_vals, color="#1a9641", linewidth=2, label="pos_R")
            ax2.plot(t_steps, posS_vals, color="#f4a800", linewidth=2, label="pos_S")
            ax2.axhline(cfg.r_pos_target, color="#1a9641", linestyle="--", alpha=0.4)
            ax2.axhline(cfg.s_pos_target, color="#f4a800", linestyle="--", alpha=0.4)
            ax2.set_ylabel("pos_R, pos_S")
            ax2.set_xlabel("Pasos post-estímulo")
            ax2.legend(fontsize=8)
            ax2.grid(True, alpha=0.25)

        fname = f"exp_dinamica_inm_{stim_name.lower()}.png"
        fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Guardado: figures/{fname}")

    # Figura extra: comparación directa CALMA vs TENSO en d (los 4 casos)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle("Transitorio d: CALMA vs. TENSO — comparación directa", fontsize=12)

    for col, stim_name in enumerate(("PELIGRO", "OPORTUNIDAD")):
        ax = axes[col]
        ax.set_title(stim_name, fontsize=11)
        for agent_name in ("CALMA", "TENSO"):
            traj   = all_results[agent_name][stim_name]["post_traj"]
            d_vals = [M.opponent_distance(s, cfg) for s in traj]
            init   = all_results[agent_name][stim_name]["init_state"]
            ax.axhline(M.opponent_distance(init, cfg),
                       color=colors[agent_name], linestyle=":", alpha=0.4)
            ax.plot(t_steps, d_vals,
                    color=colors[agent_name], linewidth=2, label=agent_name)
        ax.set_xlabel("Pasos post-estímulo")
        ax.set_ylabel("d homeostática")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fname = "exp_dinamica_inm_comparacion_d.png"
    fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: figures/{fname}")


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_experiment()

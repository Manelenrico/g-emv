"""
Experimento dinámico: CALMA vs. TENSIÓN CONTENIDA bajo estimulación.

Objetivo: ver si dos agentes con MISMA posición pero DISTINTA tensión (ten_F)
se comportan de forma diferente cuando el sistema EVOLUCIONA EN EL TIEMPO
con acoplamiento activado.

Dinámica: descenso de gradiente de d² respecto a las seis fuerzas.

  G_a^+ = 2*(w_a^pos + W_a)*Δpos_a + 2*w_a^ten*Δten_a + C_a
  G_a^- = -2*(w_a^pos + W_a)*Δpos_a + 2*w_a^ten*Δten_a + C_a
  f_a(t+1) = max(0, f_a(t) − η * G_a)

  Donde (derivados exactos de d²):
    W_a = Σ_{b≠a} sens_b · ten_b   (amplificación cruzada: la tensión de b
                                     acelera la corrección de a)
    C_a = sens_a · Σ_{b≠a} Δpos_b² (coste de arrastre: el déficit posicional
                                     de b se arrastra a a)

Dos agentes:
  CALMA:  pF=nF=1.0  →  pos_F=0, ten_F=2.0
  TENSO:  pF=nF=3.8  →  pos_F=0, ten_F=7.6
  (ambos parten de la misma posición; la diferencia es solo de tensión)

Dos fases:
  Fase 1 (reposo):   N_REPOSO=40 pasos — el sistema evoluciona libremente
  Fase 2 (estímulo): δ=1.5 en nF (PELIGRO) o en pF (OPORTUNIDAD) + 80 pasos

Cuatro métricas:
  1. Velocidad:    pasos hasta que |pos_F − pos_F_base| > THRESH_VEL
  2. Intensidad:   máximo |Δpos_F| en un solo paso
  3. Propagación:  cambio máximo acumulado en pos_R + pos_S (acoplamiento F→R,S)
  4. Recuperación: pasos hasta que d vuelve a ±THRESH_REC de d_pre-estímulo
"""

from __future__ import annotations
import math
from pathlib import Path
from typing import List

try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

import model as M
from model import State, ModelConfig, DEFAULT_CONFIG

# ─── Parámetros ──────────────────────────────────────────────────────────────

ETA: float    = 0.05   # paso de descenso de gradiente
N_REPOSO: int = 40     # pasos de reposo antes del estímulo
N_POST: int   = 80     # pasos tras el estímulo
DELTA: float  = 1.5    # magnitud del estímulo (δ añadido a nF o pF)

THRESH_VEL: float = 0.02   # umbral de respuesta en pos_F
THRESH_REC: float = 0.05   # margen para declarar recuperación (en unidades de d)

FIGURES_DIR = Path(__file__).parent / "figures"


# ─── Un paso de descenso de gradiente ────────────────────────────────────────

def gradient_step(state: State, cfg: ModelConfig = DEFAULT_CONFIG) -> State:
    """Descenso de gradiente de d²(state, cfg) con paso ETA.

    Gradiente exacto de d² = d_pos + d_ten + coupling:
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

    # Costes de arrastre: C_a = sens_a * Σ_{b≠a} Δpos_b²
    C_F = cfg.sens_F * (sqR + sqS)
    C_R = cfg.sens_R * (sqF + sqS)
    C_S = cfg.sens_S * (sqF + sqR)

    # Amplificación cruzada: W_a = Σ_{b≠a} sens_b * ten_b
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


def run_trajectory(initial: State, n_steps: int, cfg: ModelConfig = DEFAULT_CONFIG) -> List[State]:
    """n_steps pasos de gradiente. Devuelve lista de n_steps+1 estados (incluye initial)."""
    traj = [initial]
    s = initial
    for _ in range(n_steps):
        s = gradient_step(s, cfg)
        traj.append(s)
    return traj


# ─── Aplicar estímulos ───────────────────────────────────────────────────────

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
    """Cuatro métricas sobre la trayectoria post-estímulo.

    post_traj[0] = estado inmediatamente tras el estímulo (antes del primer paso).
    post_traj[i] = i pasos después del estímulo.
    """
    pos_F_base = pre_stim.pos_F
    d_base = M.opponent_distance(pre_stim, cfg)

    # 1. Velocidad: primer paso i donde |pos_F - base| > THRESH_VEL
    velocidad = len(post_traj)  # default: no respondió
    for i, s in enumerate(post_traj):
        if abs(s.pos_F - pos_F_base) > THRESH_VEL:
            velocidad = i
            break

    # 2. Intensidad: máximo |Δpos_F| entre pasos consecutivos
    deltas_posF = [abs(post_traj[i + 1].pos_F - post_traj[i].pos_F)
                   for i in range(len(post_traj) - 1)]
    intensidad = max(deltas_posF) if deltas_posF else 0.0

    # 3. Propagación: cambio máximo acumulado en R y S desde el pre-estímulo
    max_prop_R = max(abs(s.pos_R - pre_stim.pos_R) for s in post_traj)
    max_prop_S = max(abs(s.pos_S - pre_stim.pos_S) for s in post_traj)
    propagacion = max_prop_R + max_prop_S

    # 4. Recuperación: primer i donde |d(t) - d_base| ≤ THRESH_REC
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
    }


# ─── Verificación de estabilidad ─────────────────────────────────────────────

def verify_stability(traj: List[State], cfg: ModelConfig = DEFAULT_CONFIG) -> dict:
    """Cuenta pasos donde d sube (posibles oscilaciones) y registra d máxima."""
    dists = [M.opponent_distance(s, cfg) for s in traj]
    reversals = sum(1 for i in range(1, len(dists)) if dists[i] > dists[i - 1] + 1e-9)
    return {
        "max_d": max(dists),
        "final_d": dists[-1],
        "reversals": reversals,
    }


# ─── Experimento ─────────────────────────────────────────────────────────────

def run_experiment() -> None:
    cfg = DEFAULT_CONFIG
    half_basal = M.TEN_BASAL_MIN / 2.0

    # Estados iniciales: misma posición (pos_F=0), distinta tensión
    calma_0 = State(pF=1.0, nF=1.0,
                    pR=half_basal, nR=half_basal,
                    pS=half_basal, nS=half_basal)
    tenso_0 = State(pF=3.8, nF=3.8,
                    pR=half_basal, nR=half_basal,
                    pS=half_basal, nS=half_basal)

    print("\n═══════════════════════════════════════════════════════════════════")
    print("  Experimento dinámico: CALMA vs. TENSIÓN CONTENIDA bajo estímulo")
    print("═══════════════════════════════════════════════════════════════════")
    print(f"  η={ETA}, N_reposo={N_REPOSO}, N_post={N_POST}, δ={DELTA}")
    print(f"  CALMA  inicial: pos_F={calma_0.pos_F:.2f}, ten_F={calma_0.ten_F:.2f}, "
          f"d={M.opponent_distance(calma_0, cfg):.3f}")
    print(f"  TENSO  inicial: pos_F={tenso_0.pos_F:.2f}, ten_F={tenso_0.ten_F:.2f}, "
          f"d={M.opponent_distance(tenso_0, cfg):.3f}")

    # Verificación analítica de η
    # λ_max ≤ 2*(w_f_pos + W_F_max) + 2*w_f_ten
    # W_F_max conservador: R,S con ten=4 por coupling desde F (nunca llegan a más)
    W_F_upper = cfg.sens_R * 4.0 + cfg.sens_S * 4.0
    lam_max = 2 * (cfg.w_f_pos + W_F_upper) + 2 * cfg.w_f_ten
    eta_max = 1.0 / lam_max
    stable_str = "✓ ESTABLE" if ETA < eta_max else "✗ PELIGRO DE INESTABILIDAD"
    print(f"\n── Verificación η ───────────────────────────────────────────────")
    print(f"  λ_max (cota conservadora) ≈ {lam_max:.3f}  →  η_max ≈ {eta_max:.3f}")
    print(f"  η={ETA} {stable_str}")

    agents = [("CALMA", calma_0), ("TENSO", tenso_0)]
    stimuli = [("PELIGRO", apply_peligro), ("OPORTUNIDAD", apply_oportunidad)]

    all_results = {}

    for agent_name, init_state in agents:
        all_results[agent_name] = {}

        # Fase 1: reposo
        rest_traj = run_trajectory(init_state, N_REPOSO, cfg)
        pre_stim = rest_traj[-1]
        stab_rest = verify_stability(rest_traj, cfg)

        print(f"\n── {agent_name} ──────────────────────────────────────────────────────")
        print(f"  Pre-estímulo (paso {N_REPOSO}): "
              f"pos_F={pre_stim.pos_F:.3f}, ten_F={pre_stim.ten_F:.3f}, "
              f"pos_R={pre_stim.pos_R:.3f}, pos_S={pre_stim.pos_S:.3f}, "
              f"d={M.opponent_distance(pre_stim, cfg):.3f}")
        print(f"  Reposo — reversiones d: {stab_rest['reversals']}, "
              f"d_max={stab_rest['max_d']:.3f}, d_final={stab_rest['final_d']:.3f}")

        for stim_name, apply_stim in stimuli:
            stim_state = apply_stim(pre_stim)
            post_traj = run_trajectory(stim_state, N_POST, cfg)

            stab_post = verify_stability(post_traj, cfg)
            metrics = compute_metrics(pre_stim, post_traj, cfg)

            all_results[agent_name][stim_name] = {
                "rest_traj": rest_traj,
                "pre_stim": pre_stim,
                "stim_state": stim_state,
                "post_traj": post_traj,
                "metrics": metrics,
                "stab_post": stab_post,
            }

            print(f"\n  [{stim_name}]")
            print(f"    Inmediato tras estímulo: pos_F={stim_state.pos_F:.3f}, "
                  f"ten_F={stim_state.ten_F:.3f}, "
                  f"d={M.opponent_distance(stim_state, cfg):.3f}")
            print(f"    Estabilidad post: reversiones={stab_post['reversals']}, "
                  f"d_max={stab_post['max_d']:.3f}")
            print(f"    1. Velocidad:    {metrics['velocidad']} pasos")
            print(f"    2. Intensidad:   {metrics['intensidad']:.4f} (max |Δpos_F|/paso)")
            print(f"    3. Propagación:  {metrics['propagacion']:.4f} (max ΔR + max ΔS)")
            print(f"    4. Recuperación: {metrics['recuperacion']} pasos")

    # Tabla comparativa
    print("\n── Tabla comparativa ─────────────────────────────────────────────")
    header = f"  {'Métrica':<22} {'CALMA/PEL':>10} {'TENSO/PEL':>10} {'CALMA/OPO':>10} {'TENSO/OPO':>10}"
    print(header)
    print("  " + "─" * 62)
    for key, label in [
        ("velocidad",    "Velocidad (pasos)"),
        ("intensidad",   "Intensidad"),
        ("propagacion",  "Propagación"),
        ("recuperacion", "Recuperación (p)"),
    ]:
        vals = [
            all_results["CALMA"]["PELIGRO"]["metrics"][key],
            all_results["TENSO"]["PELIGRO"]["metrics"][key],
            all_results["CALMA"]["OPORTUNIDAD"]["metrics"][key],
            all_results["TENSO"]["OPORTUNIDAD"]["metrics"][key],
        ]
        if key in ("velocidad", "recuperacion"):
            fmt_vals = [str(v) for v in vals]
        else:
            fmt_vals = [f"{v:.4f}" for v in vals]
        print(f"  {label:<22} {fmt_vals[0]:>10} {fmt_vals[1]:>10} {fmt_vals[2]:>10} {fmt_vals[3]:>10}")

    if HAS_PLOT:
        _make_figures(all_results, cfg)
    else:
        print("\nAVISO: matplotlib no instalado, figuras omitidas.")


# ─── Figuras ─────────────────────────────────────────────────────────────────

def _make_figures(all_results: dict, cfg: ModelConfig) -> None:
    FIGURES_DIR.mkdir(exist_ok=True)

    colors = {"CALMA": "#2c7bb6", "TENSO": "#d7191c"}
    agent_names = ["CALMA", "TENSO"]

    for stim_name in ("PELIGRO", "OPORTUNIDAD"):
        fig, axes = plt.subplots(3, 2, figsize=(12, 9), sharex="col")
        fig.suptitle(
            f"Dinámica temporal — Estímulo: {stim_name}  "
            f"(η={ETA}, δ={DELTA}, N_reposo={N_REPOSO})",
            fontsize=12,
        )

        for col, agent_name in enumerate(agent_names):
            res = all_results[agent_name][stim_name]
            rest_traj = res["rest_traj"]
            post_traj = res["post_traj"]
            c = colors[agent_name]

            t_rest = list(range(len(rest_traj)))             # 0 .. N_REPOSO
            t_post = list(range(N_REPOSO, N_REPOSO + len(post_traj)))  # N_REPOSO .. N_REPOSO+N_POST

            d_rest = [M.opponent_distance(s, cfg) for s in rest_traj]
            d_post = [M.opponent_distance(s, cfg) for s in post_traj]

            posF_rest = [s.pos_F for s in rest_traj]
            posF_post = [s.pos_F for s in post_traj]
            posR_rest = [s.pos_R for s in rest_traj]
            posR_post = [s.pos_R for s in post_traj]
            posS_rest = [s.pos_S for s in rest_traj]
            posS_post = [s.pos_S for s in post_traj]

            axes[0, col].set_title(agent_name, fontsize=11)

            # Fila 0: distancia homeostática
            axes[0, col].plot(t_rest, d_rest, color=c, linewidth=2, label="reposo")
            axes[0, col].plot(t_post, d_post, color=c, linewidth=2, linestyle="--", label="post-estím.")
            axes[0, col].axvline(N_REPOSO, color="k", linestyle=":", alpha=0.6)
            axes[0, col].set_ylabel("d homeostática")
            axes[0, col].legend(fontsize=8)
            axes[0, col].grid(True, alpha=0.25)

            # Fila 1: pos_F (eje perturbado)
            axes[1, col].plot(t_rest, posF_rest, color=c, linewidth=2)
            axes[1, col].plot(t_post, posF_post, color=c, linewidth=2, linestyle="--")
            axes[1, col].axvline(N_REPOSO, color="k", linestyle=":", alpha=0.6)
            axes[1, col].axhline(cfg.f_pos_target, color="gray", linestyle="--",
                                 alpha=0.5, label=f"target={cfg.f_pos_target}")
            axes[1, col].set_ylabel("pos_F")
            axes[1, col].legend(fontsize=8)
            axes[1, col].grid(True, alpha=0.25)

            # Fila 2: pos_R, pos_S — propagación del acoplamiento
            axes[2, col].plot(t_rest, posR_rest, color="#1a9641", linewidth=2, label="pos_R")
            axes[2, col].plot(t_post, posR_post, color="#1a9641", linewidth=2, linestyle="--")
            axes[2, col].plot(t_rest, posS_rest, color="#f4a800", linewidth=2, label="pos_S")
            axes[2, col].plot(t_post, posS_post, color="#f4a800", linewidth=2, linestyle="--")
            axes[2, col].axvline(N_REPOSO, color="k", linestyle=":", alpha=0.6)
            axes[2, col].axhline(cfg.r_pos_target, color="#1a9641", linestyle="--", alpha=0.4)
            axes[2, col].axhline(cfg.s_pos_target, color="#f4a800", linestyle="--", alpha=0.4)
            axes[2, col].set_ylabel("pos_R, pos_S (propagación)")
            axes[2, col].set_xlabel("Pasos")
            axes[2, col].legend(fontsize=8)
            axes[2, col].grid(True, alpha=0.25)

        fig.tight_layout()
        fname = f"exp_dinamica_{stim_name.lower()}.png"
        fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Guardado: figures/{fname}")


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_experiment()

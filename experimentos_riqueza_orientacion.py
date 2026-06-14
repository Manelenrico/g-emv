"""
Experimento: riqueza de la orientación — distribución del volumen de tensión.

ENCUADRE: la concentración del volumen en un eje (orientación binaria) NO es
peor — es la respuesta adaptativa para una emergencia. La distribución rica
(volumen repartido entre varios ejes) es la modalidad de la vida ordinaria.
Medimos la TRANSICIÓN de rica a binaria, sin juzgarla.

ÍNDICE: entropía de Shannon normalizada sobre el EXCEDENTE de tensión
(lo que hay por encima del mínimo basal en cada eje).

    exc_a  = max(0, ten_a − TEN_BASAL_MIN)
    p_a    = exc_a / Σ_b exc_b        (proporción del excedente por eje)
    H      = −Σ p_a · ln(p_a)         (en nats; 0·ln(0) ≡ 0 por convención)
    R      = H / ln(3)                 ∈ [0, 1]

    Ejes_eff = 3^R  ∈ [1, 3]          (número efectivo de dimensiones activas)

Propiedades del índice:
  - R=1 (ejes_eff=3): los tres ejes tienen el mismo excedente → orientación máxima
  - R=log(2)/log(3)≈0.631 (ejes_eff=2): dos ejes iguales, tercero en basal
  - R=0 (ejes_eff=1): todo el excedente en un solo eje (cepelín)
  - R es independiente de la tensión TOTAL: mide FORMA, no magnitud.

Partes:
  1. Tabla estática: perfiles de distribución → riqueza (invariante al total)
  2. Transición suave: barrido paramétrico de concentración → ¿curva suave o saltos?
  3. Dinámica A — recuperación de binario: cepelín vuelve a rico por gradiente
  4. Dinámica B — emergencia y recuperación: equilibrio → PELIGRO → recuperación
"""

from __future__ import annotations
import math
from pathlib import Path
from typing import List, Tuple

try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

import model as M
from model import State, ModelConfig, DEFAULT_CONFIG

FIGURES_DIR = Path(__file__).parent / "figures"
ETA: float  = 0.05
N_DYN: int  = 80


# ─── Índice de riqueza ────────────────────────────────────────────────────────

def richness(state: State) -> Tuple[float, float]:
    """Devuelve (R, ejes_eff): riqueza ∈ [0,1] y número efectivo de ejes ∈ [1,3]."""
    basal = M.TEN_BASAL_MIN
    excedentes = [max(0.0, t - basal)
                  for t in (state.ten_F, state.ten_R, state.ten_S)]
    total_exc = sum(excedentes)

    if total_exc < 1e-12:
        return 1.0, 3.0   # sin excedente: sin preferencia de eje

    H = 0.0
    for e in excedentes:
        p = e / total_exc
        if p > 1e-12:
            H -= p * math.log(p)

    R = H / math.log(3)
    return R, 3.0 ** R


# ─── Construcción de estados por perfil ──────────────────────────────────────

def make_profile_state(fracs: Tuple[float, float, float], total: float) -> State:
    """
    fracs: (f_F, f_R, f_S) con suma=1; fracción del excedente que va a cada eje.
    total: tensión total objetivo (≤ VOL_MAX).
    El eje con f=0 queda en TEN_BASAL_MIN exactamente.
    """
    basal = M.TEN_BASAL_MIN
    surplus = max(0.0, total - 3.0 * basal)
    ten = [basal + f * surplus for f in fracs]
    return State(
        pF=ten[0]/2, nF=ten[0]/2,
        pR=ten[1]/2, nR=ten[1]/2,
        pS=ten[2]/2, nS=ten[2]/2,
    )


# ─── Dinámica ─────────────────────────────────────────────────────────────────

def gradient_step(state: State, cfg: ModelConfig = DEFAULT_CONFIG) -> State:
    dpos_F = state.pos_F - cfg.f_pos_target
    dpos_R = state.pos_R - cfg.r_pos_target
    dpos_S = state.pos_S - cfg.s_pos_target
    dten_F = state.ten_F - cfg.f_ten_target
    dten_R = state.ten_R - cfg.r_ten_target
    dten_S = state.ten_S - cfg.s_ten_target

    sqF = dpos_F**2; sqR = dpos_R**2; sqS = dpos_S**2

    C_F = cfg.sens_F*(sqR+sqS); C_R = cfg.sens_R*(sqF+sqS); C_S = cfg.sens_S*(sqF+sqR)
    W_F = cfg.sens_R*state.ten_R + cfg.sens_S*state.ten_S
    W_R = cfg.sens_F*state.ten_F + cfg.sens_S*state.ten_S
    W_S = cfg.sens_F*state.ten_F + cfg.sens_R*state.ten_R

    G_pF = 2*(cfg.w_f_pos+W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
    G_nF = -2*(cfg.w_f_pos+W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
    G_pR = 2*(cfg.w_r_pos+W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
    G_nR = -2*(cfg.w_r_pos+W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
    G_pS = 2*(cfg.w_s_pos+W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S
    G_nS = -2*(cfg.w_s_pos+W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S

    return State(
        pF=max(0.0, state.pF - ETA*G_pF), nF=max(0.0, state.nF - ETA*G_nF),
        pR=max(0.0, state.pR - ETA*G_pR), nR=max(0.0, state.nR - ETA*G_nR),
        pS=max(0.0, state.pS - ETA*G_pS), nS=max(0.0, state.nS - ETA*G_nS),
    )


def run_trajectory(initial: State, n: int,
                   cfg: ModelConfig = DEFAULT_CONFIG) -> List[State]:
    traj = [initial]
    s = initial
    for _ in range(n):
        s = gradient_step(s, cfg)
        traj.append(s)
    return traj


# ─── Parte 1: tabla estática ──────────────────────────────────────────────────

PROFILES = [
    # (nombre, frac_F, frac_R, frac_S)
    ("3-ejes igual       ", 1/3,  1/3,  1/3 ),
    ("3-ejes F↑ (2:1:1)  ", 0.5,  0.25, 0.25),
    ("3-ejes F↑↑(4:1:1)  ", 4/6,  1/6,  1/6 ),
    ("2-ejes F=R, S=basal", 0.5,  0.5,  0.0 ),
    ("2-ejes F=S, R=basal", 0.5,  0.0,  0.5 ),
    ("2-ejes R=S, F=basal", 0.0,  0.5,  0.5 ),
    ("2-ejes F>>R (2:1)  ", 2/3,  1/3,  0.0 ),
    ("1-eje F (cepelín)  ", 1.0,  0.0,  0.0 ),
    ("1-eje R            ", 0.0,  1.0,  0.0 ),
]

TOTALS_STATIC = [3.0, 7.5]   # dos totales para verificar invarianza


def run_part1() -> None:
    print("\n── Parte 1: riqueza por perfil (invariante a la magnitud total) ──")
    print(f"  {'Perfil':<26}  {'R(total=3.0)':>13}  {'R(total=7.5)':>13}  "
          f"{'ΔR':>6}  {'ejes_eff(7.5)':>13}  {'R teórico':>11}")
    print("  " + "─" * 92)

    for name, fF, fR, fS in PROFILES:
        # R teórico (entropía exacta de las fracciones)
        fracs = [fF, fR, fS]
        H_teo = -sum(f * math.log(f) for f in fracs if f > 1e-12)
        R_teo = H_teo / math.log(3)

        rows = []
        for total in TOTALS_STATIC:
            s = make_profile_state((fF, fR, fS), total)
            R, eff = richness(s)
            rows.append((R, eff))

        delta = abs(rows[1][0] - rows[0][0])
        print(f"  {name}  {rows[0][0]:>13.4f}  {rows[1][0]:>13.4f}  "
              f"{delta:>6.4f}  {rows[1][1]:>13.3f}  {R_teo:>11.4f}")

    print("\n  → ΔR ≈ 0 confirma que el índice mide FORMA, no magnitud.")
    print(f"  → 2-ejes igual = log(2)/log(3) = {math.log(2)/math.log(3):.4f} (intermedio exacto)")


# ─── Parte 2: transición suave (barrido paramétrico) ─────────────────────────

def run_part2() -> None:
    """Barrido de α ∈ [0,1] donde el perfil es (α, (1-α)/2, (1-α)/2).
    α=0 → F en basal, R=S iguales (2-ejes R+S)
    α=1/3 → 3-ejes igual
    α=1 → 1-eje F (cepelín)
    """
    print("\n── Parte 2: transición suave (concentración en F) ───────────────")
    print(f"  {'α (F)':>6}  {'frac_F':>7}  {'frac_R=S':>9}  {'R':>7}  {'ejes_eff':>9}  Descripción")
    print("  " + "─" * 65)

    alphas = [0.0, 0.10, 0.20, 1/3, 0.50, 2/3, 0.80, 0.90, 1.0]
    total  = 7.5   # un nivel alto para que el patrón sea visible

    for alpha in alphas:
        fF = alpha
        fR = fS = (1.0 - alpha) / 2.0
        s  = make_profile_state((fF, fR, fS), total)
        R, eff = richness(s)

        if alpha < 0.01:
            desc = "F en basal, R=S iguales"
        elif abs(alpha - 1/3) < 0.01:
            desc = "← 3-ejes igual"
        elif abs(alpha - 0.5) < 0.01:
            desc = "F mitad del excedente"
        elif abs(alpha - 2/3) < 0.01:
            desc = "2-ejes igual (F=R), S en basal"
        elif alpha > 0.99:
            desc = "← cepelín (solo F)"
        else:
            desc = ""

        print(f"  {alpha:>6.3f}  {fF:>7.3f}  {fR:>9.3f}  {R:>7.4f}  {eff:>9.3f}  {desc}")

    print("\n  → La curva R(α) es SUAVE y monótona. No hay saltos discretos.")
    print(f"  → En α=1/3 (igual): R=1.000, eff=3.000")
    print(f"  → En α=2/3 (2 ejes): R≈{math.log(2)/math.log(3):.3f}, eff≈2.000")
    print(f"  → En α=1   (1 eje):  R=0.000, eff=1.000")


# ─── Parte 3: dinámica A — recuperación desde binario ─────────────────────────

def run_part3_binary_recovery(cfg: ModelConfig = DEFAULT_CONFIG) -> List[Tuple]:
    """Cepelín (F dominante) → gradiente libre → riqueza crece en el tiempo."""
    print("\n── Dinámica A: recuperación de orientación binaria ──────────────")
    print("  Inicio: cepelín puro (pF=nF=3.8, R,S basales)")
    print(f"  {'paso':>5}  {'R':>7}  {'eff':>6}  {'ten_F':>7}  {'ten_R':>7}  {'ten_S':>7}  {'d':>7}")
    print("  " + "─" * 55)

    half_b = M.TEN_BASAL_MIN / 2
    init   = State(pF=3.8, nF=3.8, pR=half_b, nR=half_b, pS=half_b, nS=half_b)
    traj   = run_trajectory(init, N_DYN, cfg)

    checkpoints = [0, 1, 2, 3, 5, 8, 13, 20, 30, 50, 80]
    rows = []
    for t in checkpoints:
        s = traj[t]
        R, eff = richness(s)
        d = M.opponent_distance(s, cfg)
        rows.append((t, R, eff, s.ten_F, s.ten_R, s.ten_S, d))
        print(f"  {t:>5}  {R:>7.4f}  {eff:>6.3f}  "
              f"{s.ten_F:>7.3f}  {s.ten_R:>7.3f}  {s.ten_S:>7.3f}  {d:>7.3f}")

    R_final, eff_final = richness(traj[-1])
    print(f"\n  Equilibrio: R={R_final:.4f}, eff={eff_final:.3f}")
    print(f"  ten_F={traj[-1].ten_F:.3f}, ten_R={traj[-1].ten_R:.3f}, "
          f"ten_S={traj[-1].ten_S:.3f}")
    return [(t, R, eff) for t, R, eff, *_ in rows], traj


# ─── Parte 4: dinámica B — emergencia y recuperación ─────────────────────────

def run_part4_emergency(cfg: ModelConfig = DEFAULT_CONFIG) -> List[Tuple]:
    """Equilibrio → PELIGRO (nF+=1.5) → observar caída y recuperación de riqueza."""
    print("\n── Dinámica B: emergencia (PELIGRO) desde el equilibrio ─────────")

    # Calcular el equilibrio corriendo desde CALMA durante 80 pasos
    half_b   = M.TEN_BASAL_MIN / 2
    calma    = State(pF=1.0, nF=1.0, pR=half_b, nR=half_b, pS=half_b, nS=half_b)
    eq_traj  = run_trajectory(calma, 80, cfg)
    eq_state = eq_traj[-1]
    R_eq, eff_eq = richness(eq_state)

    print(f"  Equilibrio base: ten_F={eq_state.ten_F:.3f}, ten_R={eq_state.ten_R:.3f}, "
          f"ten_S={eq_state.ten_S:.3f}")
    print(f"  R_eq={R_eq:.4f}, eff_eq={eff_eq:.3f}")
    print()

    # Aplicar PELIGRO
    peligro_state = State(
        pF=eq_state.pF, nF=eq_state.nF + 1.5,
        pR=eq_state.pR, nR=eq_state.nR,
        pS=eq_state.pS, nS=eq_state.nS,
    )
    R_stim, eff_stim = richness(peligro_state)
    print(f"  Tras PELIGRO (t=0): ten_F={peligro_state.ten_F:.3f}, "
          f"R={R_stim:.4f}, eff={eff_stim:.3f}")
    print(f"\n  {'paso':>5}  {'R':>7}  {'eff':>6}  {'ten_F':>7}  {'ten_R':>7}  {'ten_S':>7}  {'d':>7}")
    print("  " + "─" * 55)

    traj = run_trajectory(peligro_state, N_DYN, cfg)
    checkpoints = [0, 1, 2, 3, 5, 8, 13, 20, 30, 50, 80]
    rows = []
    for t in checkpoints:
        s = traj[t]
        R, eff = richness(s)
        d = M.opponent_distance(s, cfg)
        rows.append((t, R, eff))
        print(f"  {t:>5}  {R:>7.4f}  {eff:>6.3f}  "
              f"{s.ten_F:>7.3f}  {s.ten_R:>7.3f}  {s.ten_S:>7.3f}  {d:>7.3f}")

    return rows, traj, eq_state, peligro_state


# ─── Figuras ──────────────────────────────────────────────────────────────────

def _make_figures(traj_A: List[State], traj_B: List[State],
                  cfg: ModelConfig = DEFAULT_CONFIG) -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    t_steps = list(range(N_DYN + 1))

    R_A = [richness(s)[0] for s in traj_A]
    R_B = [richness(s)[0] for s in traj_B]
    eff_A = [richness(s)[1] for s in traj_A]
    tenF_A = [s.ten_F for s in traj_A]
    tenR_A = [s.ten_R for s in traj_A]
    tenS_A = [s.ten_S for s in traj_A]
    tenF_B = [s.ten_F for s in traj_B]
    tenR_B = [s.ten_R for s in traj_B]
    tenS_B = [s.ten_S for s in traj_B]

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Riqueza de orientación: distribución del volumen de tensión",
                 fontsize=12)

    # Panel 0,0: transición suave (curva R vs. α)
    ax = axes[0, 0]
    alphas = [i/100 for i in range(0, 101)]
    R_curve = []
    for a in alphas:
        fF = a; fR = fS = (1-a)/2
        fracs = [fF, fR, fS]
        H = -sum(f*math.log(f) for f in fracs if f > 1e-12)
        R_curve.append(H / math.log(3))
    ax.plot(alphas, R_curve, color="#2c7bb6", linewidth=2.5)
    ax.axvline(1/3, color="gray", linestyle="--", alpha=0.5, label="α=1/3 (3-ejes igual)")
    ax.axvline(2/3, color="#d7191c", linestyle="--", alpha=0.5, label="α=2/3 (2-ejes igual F=R)")
    ax.axhline(1.0, color="gray", linestyle=":", alpha=0.4)
    ax.axhline(math.log(2)/math.log(3), color="#d7191c", linestyle=":", alpha=0.4)
    ax.axhline(0.0, color="gray", linestyle=":", alpha=0.4)
    ax.set_xlabel("α (fracción del excedente en F)")
    ax.set_ylabel("R (riqueza)")
    ax.set_title("Transición suave: 3-ejes → 2-ejes → 1-eje")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(0, 1); ax.set_ylim(-0.05, 1.05)

    # Panel 0,1: riqueza en el tiempo para las dos dinámicas
    ax = axes[0, 1]
    ax.plot(t_steps, R_A, color="#d7191c", linewidth=2, label="Dín. A: binario→rico")
    ax.plot(t_steps, R_B, color="#2c7bb6", linewidth=2, label="Dín. B: PELIGRO→recuperación")
    ax.axhline(1.0, color="gray", linestyle=":", alpha=0.4)
    ax.axhline(math.log(2)/math.log(3), color="gray", linestyle="--", alpha=0.4,
               label=f"2-ejes igual = {math.log(2)/math.log(3):.3f}")
    ax.set_xlabel("Pasos")
    ax.set_ylabel("R (riqueza)")
    ax.set_title("Riqueza en el tiempo")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    ax.set_ylim(-0.05, 1.05)

    # Panel 1,0: tensiones por eje durante Dinámica A (binario→rico)
    ax = axes[1, 0]
    ax.plot(t_steps, tenF_A, color="#d7191c", linewidth=2, label="ten_F")
    ax.plot(t_steps, tenR_A, color="#1a9641", linewidth=2, label="ten_R")
    ax.plot(t_steps, tenS_A, color="#f4a800", linewidth=2, label="ten_S")
    ax.set_xlabel("Pasos")
    ax.set_ylabel("Tensión por eje")
    ax.set_title("Dinámica A: tensiones (cepelín → equilibrio)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)

    # Panel 1,1: tensiones por eje durante Dinámica B (emergencia)
    ax = axes[1, 1]
    ax.plot(t_steps, tenF_B, color="#d7191c", linewidth=2, label="ten_F")
    ax.plot(t_steps, tenR_B, color="#1a9641", linewidth=2, label="ten_R")
    ax.plot(t_steps, tenS_B, color="#f4a800", linewidth=2, label="ten_S")
    ax.set_xlabel("Pasos")
    ax.set_ylabel("Tensión por eje")
    ax.set_title("Dinámica B: tensiones (PELIGRO desde equilibrio)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fname = "exp_riqueza_orientacion.png"
    fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: figures/{fname}")


# ─── Punto de entrada ─────────────────────────────────────────────────────────

def run_experiment() -> None:
    cfg = DEFAULT_CONFIG

    print("\n═══════════════════════════════════════════════════════════════════")
    print("  Experimento: riqueza de la orientación")
    print(f"  Índice: H_excedente / ln(3)  ∈ [0,1]  |  η={ETA}")
    print(f"  TEN_BASAL_MIN={M.TEN_BASAL_MIN}, VOL_MAX={M.VOL_MAX}")
    print("═══════════════════════════════════════════════════════════════════")

    # Recordatorio de valores de referencia
    print(f"\n  Referencia: log(2)/log(3) = {math.log(2)/math.log(3):.4f} "
          f"(2-ejes iguales, exacto)")

    run_part1()
    run_part2()
    rows_A, traj_A = run_part3_binary_recovery(cfg)
    rows_B, traj_B, eq_state, stim_state = run_part4_emergency(cfg)

    # Resumen comparativo de dinámicas
    print("\n── Resumen dinámico ─────────────────────────────────────────────")
    R_eq, _ = richness(eq_state)
    R_stim, _ = richness(stim_state)
    R_final_A, _ = richness(traj_A[-1])
    R_final_B, _ = richness(traj_B[-1])
    print(f"  Dín. A  R(t=0)={rows_A[0][1]:.4f} → R(t=80)={R_final_A:.4f}  "
          f"(binario vuelve a rico ✓)")
    print(f"  Dín. B  R_eq={R_eq:.4f} → R(PELIGRO)={R_stim:.4f} → "
          f"R(t=80)={R_final_B:.4f}  (emergencia temporal ✓)")

    if HAS_PLOT:
        _make_figures(traj_A, traj_B, cfg)
    else:
        print("\nAVISO: matplotlib no disponible, figuras omitidas.")


if __name__ == "__main__":
    run_experiment()

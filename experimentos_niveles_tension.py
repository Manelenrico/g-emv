"""
Barrido de niveles de tensión física: ¿la degradación del funcionamiento
es progresiva conforme ten_F se acerca al techo VOL_MAX?

Diseño:
  - Seis agentes idénticos excepto en ten_F (eje físico):
      ten_F ∈ {2.0, 4.0, 6.0, 7.0, 7.5, 7.9}
    Todos con pos_F=0 (f⁺=f⁻=ten_F/2), R y S en mínimo basal.
  - Estímulo inmediato (N_REPOSO=0): δ=1.5 en nF (PELIGRO) o pF (OPORTUNIDAD).
  - Acoplamiento encendido. Dinámica de descenso de gradiente, η=0.05.
  - N_POST=80 pasos post-estímulo.

Métricas por nivel:
  - d_base:          distancia homeostática antes del estímulo
  - d_stim:          distancia inmediatamente tras el estímulo
  - Δd_abs:          d_stim − d_base  (sensibilidad absoluta)
  - Δd_rel:          Δd_abs / d_base  (sensibilidad relativa)
  - δ_absorbido:     cuánto del δ=1.5 se absorbió (el resto rebotó en VOL_MAX)
  - propagacion:     cambio máximo en pos_R + pos_S durante el transitorio
  - intensidad:      máximo |Δpos_F| en un paso
  - t_mitad:         pasos hasta que d cae a la mitad de (d_stim − d_final)

Pregunta: ¿hay un óptimo tipo Yerkes-Dodson, o la degradación es monótona?
"""

from __future__ import annotations
import math
from pathlib import Path
from typing import List

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

import model as M
from model import State, ModelConfig, DEFAULT_CONFIG

# ─── Parámetros ──────────────────────────────────────────────────────────────

TEN_F_LEVELS = [2.0, 4.0, 6.0, 7.0, 7.5, 7.9]
DELTA: float  = 1.5
ETA: float    = 0.05
N_POST: int   = 80

FIGURES_DIR = Path(__file__).parent / "figures"

# Transitorio: pasos a mostrar en la tabla detallada
CHECKPOINTS = [0, 1, 2, 5, 10, 20, 40, 80]


# ─── Dinámica ─────────────────────────────────────────────────────────────────

def gradient_step(state: State, cfg: ModelConfig = DEFAULT_CONFIG) -> State:
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

    G_pF = 2*(cfg.w_f_pos + W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
    G_nF = -2*(cfg.w_f_pos + W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
    G_pR = 2*(cfg.w_r_pos + W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
    G_nR = -2*(cfg.w_r_pos + W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
    G_pS = 2*(cfg.w_s_pos + W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S
    G_nS = -2*(cfg.w_s_pos + W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S

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


# ─── Estado inicial para cada nivel ──────────────────────────────────────────

def make_agent(ten_f_target: float) -> State:
    """Agente con pos_F=0, ten_F≈ten_f_target (exacto si < VOL_MAX), R y S basales."""
    half = ten_f_target / 2.0
    return State(
        pF=half, nF=half,
        pR=M.TEN_BASAL_MIN / 2, nR=M.TEN_BASAL_MIN / 2,
        pS=M.TEN_BASAL_MIN / 2, nS=M.TEN_BASAL_MIN / 2,
    )


# ─── Estímulos ───────────────────────────────────────────────────────────────

def apply_peligro(state: State) -> State:
    return State(pF=state.pF, nF=state.nF + DELTA,
                 pR=state.pR, nR=state.nR, pS=state.pS, nS=state.nS)


def apply_oportunidad(state: State) -> State:
    return State(pF=state.pF + DELTA, nF=state.nF,
                 pR=state.pR, nR=state.nR, pS=state.pS, nS=state.nS)


# ─── Análisis VOL_MAX ─────────────────────────────────────────────────────────

def vol_analysis(init_state: State, stim_state: State) -> dict:
    """Cuánto del δ=1.5 se absorbió realmente en ten_F."""
    # El δ pretendido era DELTA; lo absorbido es cuánto subió ten_F
    delta_ten_F = stim_state.ten_F - init_state.ten_F
    absorbed   = round(delta_ten_F, 6)
    bounced    = round(DELTA - absorbed, 6)
    capped     = (init_state.ten_F + M.TEN_BASAL_MIN * 2 + DELTA) > M.VOL_MAX
    return {"absorbed": absorbed, "bounced": max(0.0, bounced), "capped": capped}


# ─── Métricas de trayectoria ─────────────────────────────────────────────────

def traj_metrics(init_state: State, stim_state: State,
                 traj: List[State], cfg: ModelConfig = DEFAULT_CONFIG) -> dict:
    d_base  = M.opponent_distance(init_state, cfg)
    d_stim  = M.opponent_distance(stim_state, cfg)
    d_final = M.opponent_distance(traj[-1], cfg)

    dists = [M.opponent_distance(s, cfg) for s in traj]

    # Intensidad: mayor |Δpos_F| en un paso
    intensidad = max(
        abs(traj[i+1].pos_F - traj[i].pos_F) for i in range(len(traj)-1)
    ) if len(traj) > 1 else 0.0

    # Propagación: suma de cambios máximos en R y S
    prop_R = max(abs(s.pos_R - init_state.pos_R) for s in traj)
    prop_S = max(abs(s.pos_S - init_state.pos_S) for s in traj)
    propagacion = prop_R + prop_S

    # t_mitad: pasos hasta que d baja a la mitad de (d_stim − d_final)
    target_mid = d_stim - (d_stim - d_final) / 2.0
    t_mitad = len(traj) - 1
    for i, d in enumerate(dists):
        if d <= target_mid:
            t_mitad = i
            break

    return {
        "d_base":       d_base,
        "d_stim":       d_stim,
        "delta_abs":    d_stim - d_base,
        "delta_rel":    (d_stim - d_base) / d_base if d_base > 0 else 0.0,
        "d_final":      d_final,
        "intensidad":   intensidad,
        "propagacion":  propagacion,
        "t_mitad":      t_mitad,
        "dists":        dists,
    }


# ─── Experimento ─────────────────────────────────────────────────────────────

def run_experiment() -> None:
    cfg = DEFAULT_CONFIG

    print("\n═══════════════════════════════════════════════════════════════════")
    print("  Barrido de niveles de tensión física")
    print("  ten_F ∈ [2.0, 4.0, 6.0, 7.0, 7.5, 7.9]  |  δ=1.5, η=0.05")
    print("═══════════════════════════════════════════════════════════════════")

    all_results = {}

    for ten_f_req in TEN_F_LEVELS:
        init   = make_agent(ten_f_req)
        ten_f_actual = init.ten_F  # puede diferir de ten_f_req si VOL_MAX cap
        d_base = M.opponent_distance(init, cfg)

        results_stim = {}
        for stim_name, apply_stim in [("PELIGRO", apply_peligro),
                                       ("OPORTUNIDAD", apply_oportunidad)]:
            stim_state = apply_stim(init)
            traj       = run_trajectory(stim_state, N_POST, cfg)
            vol        = vol_analysis(init, stim_state)
            metrics    = traj_metrics(init, stim_state, traj, cfg)
            results_stim[stim_name] = {"stim": stim_state, "traj": traj,
                                       "vol": vol, "metrics": metrics}

        all_results[ten_f_req] = {
            "init":        init,
            "ten_f_req":   ten_f_req,
            "ten_f_actual": ten_f_actual,
            "d_base":      d_base,
            "stims":       results_stim,
        }

    # ── Tabla principal ────────────────────────────────────────────────────
    print("\n── Tabla por nivel — Sensibilidad al estímulo ───────────────────")
    print(f"  VOL_MAX={M.VOL_MAX}, TEN_BASAL_MIN={M.TEN_BASAL_MIN}")
    print()

    hdr = (f"  {'ten_F_req':>9}  {'ten_F_real':>10}  {'d_base':>7}"
           f"  {'Δd_PEL':>8}  {'Δd_rel%_PEL':>12}"
           f"  {'Δd_OPO':>8}  {'Δd_rel%_OPO':>12}"
           f"  {'δ_abs':>6}  {'δ_reb':>6}")
    print(hdr)
    print("  " + "─" * 100)

    for lv in TEN_F_LEVELS:
        r    = all_results[lv]
        mp   = r["stims"]["PELIGRO"]["metrics"]
        mo   = r["stims"]["OPORTUNIDAD"]["metrics"]
        vp   = r["stims"]["PELIGRO"]["vol"]
        ten_actual = r["ten_f_actual"]
        cap_mark = "*" if abs(ten_actual - lv) > 0.01 else " "
        print(f"  {lv:>9.1f}  {ten_actual:>10.3f}{cap_mark}  {r['d_base']:>7.3f}"
              f"  {mp['delta_abs']:>8.4f}  {mp['delta_rel']*100:>11.2f}%"
              f"  {mo['delta_abs']:>8.4f}  {mo['delta_rel']*100:>11.2f}%"
              f"  {vp['absorbed']:>6.3f}  {vp['bounced']:>6.3f}")

    print("  (* = ten_F inicial cap al crear el State — ten_F_req > VOL_MAX - 0.2)")

    # ── Tabla propagación, intensidad, velocidad ───────────────────────────
    print("\n── Tabla por nivel — Propagación, Intensidad, Velocidad ─────────")
    hdr2 = (f"  {'ten_F_req':>9}"
            f"  {'prop_PEL':>9}  {'intens_PEL':>11}  {'t½_PEL':>7}"
            f"  {'prop_OPO':>9}  {'intens_OPO':>11}  {'t½_OPO':>7}")
    print(hdr2)
    print("  " + "─" * 80)
    for lv in TEN_F_LEVELS:
        mp = all_results[lv]["stims"]["PELIGRO"]["metrics"]
        mo = all_results[lv]["stims"]["OPORTUNIDAD"]["metrics"]
        print(f"  {lv:>9.1f}"
              f"  {mp['propagacion']:>9.4f}  {mp['intensidad']:>11.4f}  {mp['t_mitad']:>7}"
              f"  {mo['propagacion']:>9.4f}  {mo['intensidad']:>11.4f}  {mo['t_mitad']:>7}")

    # ── Transitorios de d ─────────────────────────────────────────────────
    print("\n── Transitorio de d — PELIGRO (pasos seleccionados) ────────────")
    chk = [t for t in CHECKPOINTS if t <= N_POST]
    header_t = f"  {'ten_F':>7}  " + "  ".join(f"t={t:>2}" for t in chk)
    print(header_t)
    print("  " + "─" * (9 + 7 * len(chk)))
    for lv in TEN_F_LEVELS:
        dists = all_results[lv]["stims"]["PELIGRO"]["metrics"]["dists"]
        row   = "  ".join(f"{dists[t]:>6.3f}" for t in chk)
        print(f"  {lv:>7.1f}  {row}")

    print("\n── Transitorio de d — OPORTUNIDAD (pasos seleccionados) ────────")
    print(header_t)
    print("  " + "─" * (9 + 7 * len(chk)))
    for lv in TEN_F_LEVELS:
        dists = all_results[lv]["stims"]["OPORTUNIDAD"]["metrics"]["dists"]
        row   = "  ".join(f"{dists[t]:>6.3f}" for t in chk)
        print(f"  {lv:>7.1f}  {row}")

    if HAS_PLOT:
        _make_figures(all_results, cfg)
    else:
        print("\nAVISO: matplotlib no disponible, figuras omitidas.")


# ─── Figuras ──────────────────────────────────────────────────────────────────

def _make_figures(all_results: dict, cfg: ModelConfig) -> None:
    FIGURES_DIR.mkdir(exist_ok=True)

    levels     = TEN_F_LEVELS
    t_steps    = list(range(N_POST + 1))
    palette    = plt.cm.plasma_r  # claro=baja tensión, oscuro=alta tensión
    colors     = [palette(i / (len(levels) - 1)) for i in range(len(levels))]

    # ─ Figura 1: transitorios de d para los dos estímulos ─────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(f"Transitorios d por nivel de ten_F  (δ={DELTA}, η={ETA})", fontsize=12)

    for col, stim_name in enumerate(("PELIGRO", "OPORTUNIDAD")):
        ax = axes[col]
        ax.set_title(stim_name, fontsize=11)
        for i, lv in enumerate(levels):
            dists = all_results[lv]["stims"][stim_name]["metrics"]["dists"]
            d_base = all_results[lv]["d_base"]
            label = f"ten_F={lv:.1f}"
            ax.axhline(d_base, color=colors[i], linestyle=":", alpha=0.3, linewidth=1)
            ax.plot(t_steps, dists, color=colors[i], linewidth=2, label=label)
        ax.set_xlabel("Pasos post-estímulo")
        ax.set_ylabel("d homeostática")
        ax.legend(fontsize=8, loc="upper right")
        ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fname = "exp_niveles_transitorios.png"
    fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: figures/{fname}")

    # ─ Figura 2: curvas de sensibilidad vs. ten_F ─────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.suptitle(f"Sensibilidad al estímulo vs. tensión base  (δ={DELTA})", fontsize=12)

    ten_vals    = [all_results[lv]["ten_f_actual"] for lv in levels]
    absorbed    = [all_results[lv]["stims"]["PELIGRO"]["vol"]["absorbed"] for lv in levels]
    bounced     = [all_results[lv]["stims"]["PELIGRO"]["vol"]["bounced"]  for lv in levels]

    d_base_vals = [all_results[lv]["d_base"] for lv in levels]

    delta_abs_p = [all_results[lv]["stims"]["PELIGRO"]["metrics"]["delta_abs"]    for lv in levels]
    delta_abs_o = [all_results[lv]["stims"]["OPORTUNIDAD"]["metrics"]["delta_abs"] for lv in levels]
    delta_rel_p = [all_results[lv]["stims"]["PELIGRO"]["metrics"]["delta_rel"]    for lv in levels]
    delta_rel_o = [all_results[lv]["stims"]["OPORTUNIDAD"]["metrics"]["delta_rel"] for lv in levels]
    prop_p = [all_results[lv]["stims"]["PELIGRO"]["metrics"]["propagacion"]    for lv in levels]
    prop_o = [all_results[lv]["stims"]["OPORTUNIDAD"]["metrics"]["propagacion"] for lv in levels]

    # Panel 0: Δd absoluta
    ax = axes[0, 0]
    ax.plot(ten_vals, delta_abs_p, "o-", color="#d7191c", linewidth=2, label="PELIGRO")
    ax.plot(ten_vals, delta_abs_o, "s--", color="#2c7bb6", linewidth=2, label="OPORTUNIDAD")
    ax.axvline(M.VOL_MAX - DELTA - M.TEN_BASAL_MIN * 2,
               color="gray", linestyle=":", alpha=0.6, label="inicio VOL_MAX cap")
    ax.set_xlabel("ten_F inicial")
    ax.set_ylabel("Δd absoluta (d_stim − d_base)")
    ax.set_title("Sensibilidad absoluta")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)

    # Panel 1: Δd relativa
    ax = axes[0, 1]
    ax.plot(ten_vals, [v * 100 for v in delta_rel_p], "o-", color="#d7191c",
            linewidth=2, label="PELIGRO")
    ax.plot(ten_vals, [v * 100 for v in delta_rel_o], "s--", color="#2c7bb6",
            linewidth=2, label="OPORTUNIDAD")
    ax.axvline(M.VOL_MAX - DELTA - M.TEN_BASAL_MIN * 2,
               color="gray", linestyle=":", alpha=0.6)
    ax.set_xlabel("ten_F inicial")
    ax.set_ylabel("Δd relativa (%)")
    ax.set_title("Sensibilidad relativa")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)

    # Panel 2: δ absorbido vs. rebotado
    ax = axes[1, 0]
    x = range(len(levels))
    bar_w = 0.35
    bars1 = ax.bar([xi - bar_w/2 for xi in x], absorbed, bar_w,
                   label="δ absorbido", color="#1a9641", alpha=0.8)
    bars2 = ax.bar([xi + bar_w/2 for xi in x], bounced, bar_w,
                   label="δ rebotado", color="#d7191c", alpha=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{lv:.1f}" for lv in levels])
    ax.set_xlabel("ten_F inicial (solicitada)")
    ax.set_ylabel("Unidades de δ")
    ax.set_title(f"Absorción vs. rebote VOL_MAX  (δ={DELTA})")
    ax.legend(fontsize=9)
    ax.axhline(DELTA, color="gray", linestyle="--", alpha=0.5, label="δ total")
    ax.grid(True, alpha=0.25, axis="y")

    # Panel 3: propagación a R,S
    ax = axes[1, 1]
    ax.plot(ten_vals, prop_p, "o-", color="#d7191c", linewidth=2, label="PELIGRO")
    ax.plot(ten_vals, prop_o, "s--", color="#2c7bb6", linewidth=2, label="OPORTUNIDAD")
    ax.axvline(M.VOL_MAX - DELTA - M.TEN_BASAL_MIN * 2,
               color="gray", linestyle=":", alpha=0.6, label="inicio VOL_MAX cap")
    ax.set_xlabel("ten_F inicial")
    ax.set_ylabel("max ΔR + max ΔS")
    ax.set_title("Propagación a R y S")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fname = "exp_niveles_sensibilidad.png"
    fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: figures/{fname}")


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_experiment()

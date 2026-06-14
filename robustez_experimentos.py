"""
Robustez de los dos experimentos centrales.

Experimento A — ceguera a la oportunidad:
  TENSO (ten_F=7.6) registra Δd_OPO≈+0.042 frente a CALMA Δd_OPO≈+0.628.
  Mecanismo propuesto: VOL_MAX satura la tensión de TENSO — el estímulo rebota.

Experimento B — óptimo dependiente del entorno:
  Δd_OPO tiene un pico en L=6.0 (ni demasiada ni poca tensión).
  Mecanismo propuesto: coupling amplifica (pendiente ascendente) +
  VOL_MAX recorta a L>6.3 (pendiente descendente) → pico en el umbral.

Tres pruebas por experimento:
  1. Estadística: 100 perturbaciones aleatorias de las condiciones iniciales.
  2. Ablación causal: VOL_MAX → ∞ (quitar el mecanismo propuesto).
  3. Calibraciones: barrer VOL_MAX ∈ [7.0,10.0], δ ∈ [0.5,2.5], sens_F ∈ [0.15,0.40].

MODELO: determinista — la "semilla" es el vector de perturbación de las fuerzas
iniciales (ε ~ N(0,σ) por fuerza, σ_F=0.05, σ_RS=0.01).
"""

from __future__ import annotations
import math
from pathlib import Path
from typing import List, Dict, Tuple

try:
    import numpy as np
    HAS_NP = True
except ImportError:
    HAS_NP = False

try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

import model as M
from model import State, ModelConfig, DEFAULT_CONFIG

FIGURES_DIR = Path(__file__).parent / "figures"

# ─── Parámetros base (idénticos a los experimentos originales) ────────────────
ETA       = 0.05
DELTA_NOM = 1.5            # delta nominal del estímulo
VOL_MAX_NOM = 8.0          # valor original de VOL_MAX

TEN_F_LEVELS = [2.0, 4.0, 6.0, 7.0, 7.5, 7.9]

CALMA_PF = CALMA_NF = 1.0
TENSO_PF = TENSO_NF = 3.8

N_SEEDS  = 100
SIGMA_F  = 0.05   # ruido absoluto en fuerzas del eje F
SIGMA_RS = 0.01   # ruido absoluto en fuerzas de R y S (basales, menor ruido)


# ─── Utilidad: parcheo temporal de VOL_MAX ───────────────────────────────────

class _PatchedVolMax:
    """Context manager que parchea M.VOL_MAX temporalmente."""
    def __init__(self, val: float) -> None: self.val = val
    def __enter__(self):
        self._old = M.VOL_MAX
        M.VOL_MAX = self.val
    def __exit__(self, *_):
        M.VOL_MAX = self._old

def patched_vol_max(val: float) -> _PatchedVolMax:
    return _PatchedVolMax(val)


# ─── Constructores de estado ──────────────────────────────────────────────────

def _make_state(pF, nF, pR=None, nR=None, pS=None, nS=None) -> State:
    b2 = M.TEN_BASAL_MIN / 2
    return State(pF=pF, nF=nF,
                 pR=pR if pR is not None else b2,
                 nR=nR if nR is not None else b2,
                 pS=pS if pS is not None else b2,
                 nS=nS if nS is not None else b2)

def _calma() -> State:  return _make_state(CALMA_PF, CALMA_NF)
def _tenso() -> State:  return _make_state(TENSO_PF, TENSO_NF)
def _level(lv: float) -> State: return _make_state(lv / 2, lv / 2)


# ─── Métrica base: Δd para OPORTUNIDAD (inmediata) ───────────────────────────

def delta_d_opo(init: State, delta: float = DELTA_NOM,
                cfg: ModelConfig = DEFAULT_CONFIG) -> float:
    """Δd = d_stim − d_base  al aplicar OPO = pF += delta."""
    stim = State(pF=init.pF + delta, nF=init.nF,
                 pR=init.pR, nR=init.nR, pS=init.pS, nS=init.nS)
    return M.opponent_distance(stim, cfg) - M.opponent_distance(init, cfg)


# ═══════════════════════════════════════════════════════════════════════════════
# PRUEBA 1 — Robustez estadística (perturbaciones aleatorias)
# ═══════════════════════════════════════════════════════════════════════════════

def run_test1() -> None:
    if not HAS_NP:
        print("  SKIP Test1: numpy no disponible.")
        return

    rng = np.random.default_rng(0)

    print("\n══ PRUEBA 1: Estadística (N=100 perturbaciones) ════════════════════")
    print(f"  Modelo determinista — 'semilla' = vector de ruido en fuerzas iniciales")
    print(f"  σ_F={SIGMA_F}  σ_RS={SIGMA_RS}  VOL_MAX={M.VOL_MAX}  δ={DELTA_NOM}")

    # ── Experimento A ─────────────────────────────────────────────────────────
    print("\n  ── Exp A: CALMA vs TENSO ─────────────────────────────────────────")

    dd_A: Dict[str, List[float]] = {"CALMA": [], "TENSO": []}
    for _ in range(N_SEEDS):
        for name, pf0 in [("CALMA", CALMA_PF), ("TENSO", TENSO_PF)]:
            b2 = M.TEN_BASAL_MIN / 2
            pF = max(0.0, pf0  + rng.normal(0, SIGMA_F))
            nF = max(0.0, pf0  + rng.normal(0, SIGMA_F))
            pR = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            nR = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            pS = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            nS = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            init = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
            dd_A[name].append(delta_d_opo(init))

    for name, dds in dd_A.items():
        arr = np.array(dds)
        print(f"  {name:<7}  Δd_OPO: μ={arr.mean():.4f}  σ={arr.std():.4f}  "
              f"[P5={np.percentile(arr, 5):.4f}, P95={np.percentile(arr, 95):.4f}]")

    dds_C = np.array(dd_A["CALMA"])
    dds_T = np.array(dd_A["TENSO"])
    frac_tenso_smaller = (dds_T < dds_C).mean()
    frac_tenso_blind   = (dds_T < 0.10).mean()   # "blind" = Δd < 10% of CALMA nom.
    print(f"\n  TENSO < CALMA en {frac_tenso_smaller*100:.1f}% de semillas  "
          f"(esperado: ~100%)")
    print(f"  TENSO Δd < 0.10 en {frac_tenso_blind*100:.1f}% de semillas  "
          f"(ceguera efectiva)")

    # ── Experimento B ─────────────────────────────────────────────────────────
    print("\n  ── Exp B: Barrido de niveles ─────────────────────────────────────")

    dd_B: Dict[float, List[float]] = {lv: [] for lv in TEN_F_LEVELS}
    peak_counts: Dict[float, int] = {lv: 0 for lv in TEN_F_LEVELS}

    for _ in range(N_SEEDS):
        per_seed = {}
        for lv in TEN_F_LEVELS:
            b2 = M.TEN_BASAL_MIN / 2
            half = lv / 2
            pF = max(0.0, half + rng.normal(0, SIGMA_F))
            nF = max(0.0, half + rng.normal(0, SIGMA_F))
            pR = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            nR = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            pS = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            nS = max(0.0, b2   + rng.normal(0, SIGMA_RS))
            init = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
            dd  = delta_d_opo(init)
            dd_B[lv].append(dd)
            per_seed[lv] = dd
        peak_lv = max(per_seed, key=per_seed.get)
        peak_counts[peak_lv] += 1

    print(f"  {'L':>5}  {'μ(Δd)':>8}  {'σ':>7}  {'P5':>7}  {'P95':>7}")
    print("  " + "─" * 42)
    for lv in TEN_F_LEVELS:
        arr = np.array(dd_B[lv])
        print(f"  {lv:>5.1f}  {arr.mean():>8.4f}  {arr.std():>7.4f}  "
              f"{np.percentile(arr, 5):>7.4f}  {np.percentile(arr, 95):>7.4f}")

    print(f"\n  Frecuencia de ser el nivel PICO en 100 semillas:")
    for lv, cnt in peak_counts.items():
        print(f"    L={lv:.1f}: {cnt:>3}/{N_SEEDS}  {'← PICO DOMINANTE' if cnt == max(peak_counts.values()) else ''}")


# ═══════════════════════════════════════════════════════════════════════════════
# PRUEBA 2 — Ablación causal (VOL_MAX → ∞)
# ═══════════════════════════════════════════════════════════════════════════════

def run_test2() -> None:
    print("\n══ PRUEBA 2: Ablación causal (VOL_MAX = 100 = sin techo) ═══════════")
    print(f"  Hipótesis causal: VOL_MAX es la causa de la ceguera (A) y del pico (B).")
    print(f"  Si al quitar VOL_MAX el fenómeno desaparece, la hipótesis se confirma.")

    # ── Experimento A ─────────────────────────────────────────────────────────
    print("\n  ── Exp A: CALMA vs TENSO ─────────────────────────────────────────")
    print(f"  {'Condición':<20}  {'Agente':<8}  {'d_base':>8}  {'d_stim':>8}  {'Δd':>8}")
    print("  " + "─" * 57)

    for label, vol_max in [("Original  (VM=8.0)", VOL_MAX_NOM),
                            ("Ablación  (VM=100)", 100.0)]:
        for name, init_fn in [("CALMA", _calma), ("TENSO", _tenso)]:
            with patched_vol_max(vol_max):
                init = init_fn()
                dd = delta_d_opo(init)
                stim = State(pF=init.pF + DELTA_NOM, nF=init.nF,
                             pR=init.pR, nR=init.nR, pS=init.pS, nS=init.nS)
                d_b = M.opponent_distance(init)
                d_s = M.opponent_distance(stim)
            print(f"  {label:<20}  {name:<8}  {d_b:>8.3f}  {d_s:>8.3f}  {dd:>8.4f}")
        print()

    print("  INTERPRETACIÓN:")
    print("  — Si ablación elimina la diferencia CALMA≫TENSO → VOL_MAX es la causa.")
    print("  — Si diferencia persiste → otra pieza también contribuye.")

    # ── Experimento B ─────────────────────────────────────────────────────────
    print("\n  ── Exp B: Barrido de niveles ─────────────────────────────────────")
    print(f"  {'L':>5}  {'Δd_OPO original':>17}  {'Δd_OPO ablación (VM=100)':>24}")
    print("  " + "─" * 50)

    orig_dds = {}
    abla_dds = {}
    for lv in TEN_F_LEVELS:
        with patched_vol_max(VOL_MAX_NOM):
            orig_dds[lv] = delta_d_opo(_level(lv))
        with patched_vol_max(100.0):
            abla_dds[lv] = delta_d_opo(_level(lv))

    for lv in TEN_F_LEVELS:
        print(f"  {lv:>5.1f}  {orig_dds[lv]:>17.4f}  {abla_dds[lv]:>24.4f}")

    orig_peak = max(orig_dds, key=orig_dds.get)
    abla_peak = max(abla_dds, key=abla_dds.get)
    print(f"\n  Pico ORIGINAL: L={orig_peak}  |  Pico ABLADO: L={abla_peak}")
    abla_monotone = all(abla_dds[TEN_F_LEVELS[i]] <= abla_dds[TEN_F_LEVELS[i+1]]
                        for i in range(len(TEN_F_LEVELS)-1))
    print(f"  Curva ablada monótona creciente: {'✓ SÍ' if abla_monotone else '✗ NO'}")


# ═══════════════════════════════════════════════════════════════════════════════
# PRUEBA 3 — Robustez a calibraciones
# ═══════════════════════════════════════════════════════════════════════════════

def run_test3() -> None:
    print("\n══ PRUEBA 3: Robustez a calibraciones ══════════════════════════════")

    # ── A: Barrer VOL_MAX ─────────────────────────────────────────────────────
    print("\n  ── Exp A: Variando VOL_MAX (δ=1.5, CALMA pF=nF=1.0, TENSO pF=nF=3.8) ──")
    vol_max_range = [7.0, 7.5, 8.0, 8.5, 9.0, 9.3, 10.0]
    print(f"  {'VOL_MAX':>8}  {'Δd CALMA':>10}  {'Δd TENSO':>10}  "
          f"{'Ratio T/C':>10}  {'TENSO cap':>10}")
    print("  " + "─" * 55)
    for vm in vol_max_range:
        with patched_vol_max(vm):
            c_init = _calma(); t_init = _tenso()
            dd_c = delta_d_opo(c_init)
            dd_t = delta_d_opo(t_init)
            # Verificar si TENSO se capó
            t_stim = State(pF=t_init.pF + DELTA_NOM, nF=t_init.nF,
                           pR=t_init.pR, nR=t_init.nR, pS=t_init.pS, nS=t_init.nS)
            capped = abs(t_stim.ten_F - (t_init.ten_F + DELTA_NOM)) > 0.001
        ratio = dd_t / dd_c if abs(dd_c) > 1e-6 else float("nan")
        print(f"  {vm:>8.1f}  {dd_c:>10.4f}  {dd_t:>10.4f}  "
              f"{ratio:>10.4f}  {'SÍ' if capped else 'NO':>10}")
    print(f"  Umbral teórico de cap: VM_cap = ten_F_TENSO + δ + 2·basal = "
          f"{TENSO_PF+TENSO_NF + DELTA_NOM + 2*M.TEN_BASAL_MIN:.2f}")

    # ── A: Barrer DELTA ───────────────────────────────────────────────────────
    print("\n  ── Exp A: Variando δ (VOL_MAX=8.0, agentes nominales) ──────────")
    delta_range = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5]
    print(f"  {'δ':>6}  {'Δd CALMA':>10}  {'Δd TENSO':>10}  "
          f"{'Ratio T/C':>10}  {'TENSO cap':>10}")
    print("  " + "─" * 55)
    for delta in delta_range:
        with patched_vol_max(VOL_MAX_NOM):
            c_init = _calma(); t_init = _tenso()
            dd_c = delta_d_opo(c_init, delta=delta)
            dd_t = delta_d_opo(t_init, delta=delta)
            t_stim = State(pF=t_init.pF + delta, nF=t_init.nF,
                           pR=t_init.pR, nR=t_init.nR, pS=t_init.pS, nS=t_init.nS)
            capped = abs(t_stim.ten_F - (t_init.ten_F + delta)) > 0.001
        ratio = dd_t / dd_c if abs(dd_c) > 1e-6 else float("nan")
        print(f"  {delta:>6.2f}  {dd_c:>10.4f}  {dd_t:>10.4f}  "
              f"{ratio:>10.4f}  {'SÍ' if capped else 'NO':>10}")

    # ── A: Barrer sens_F ──────────────────────────────────────────────────────
    print("\n  ── Exp A: Variando sens_F ±33% (VOL_MAX=8.0, δ=1.5) ────────────")
    sens_range = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
    print(f"  {'sens_F':>8}  {'Δd CALMA':>10}  {'Δd TENSO':>10}  {'Ratio T/C':>10}")
    print("  " + "─" * 42)
    for sf in sens_range:
        cfg = ModelConfig(sens_F=sf)
        with patched_vol_max(VOL_MAX_NOM):
            c_init = _calma(); t_init = _tenso()
            dd_c = delta_d_opo(c_init, cfg=cfg)
            dd_t = delta_d_opo(t_init, cfg=cfg)
        ratio = dd_t / dd_c if abs(dd_c) > 1e-6 else float("nan")
        print(f"  {sf:>8.2f}  {dd_c:>10.4f}  {dd_t:>10.4f}  {ratio:>10.4f}")

    # ── B: Barrer VOL_MAX ─────────────────────────────────────────────────────
    print("\n  ── Exp B: Variando VOL_MAX — ¿dónde está el pico? ──────────────")
    vol_max_range_B = [7.0, 7.5, 8.0, 8.5, 9.0, 10.0]
    print(f"  {'VM':>5}  " + "  ".join(f"{lv:>7.1f}" for lv in TEN_F_LEVELS)
          + "  PICO")
    print("  " + "─" * (7 + 10*len(TEN_F_LEVELS)))
    for vm in vol_max_range_B:
        row_dds = {}
        for lv in TEN_F_LEVELS:
            with patched_vol_max(vm):
                row_dds[lv] = delta_d_opo(_level(lv))
        peak_lv = max(row_dds, key=row_dds.get)
        vals = "  ".join(f"{row_dds[lv]:>7.4f}" for lv in TEN_F_LEVELS)
        print(f"  {vm:>5.1f}  {vals}  L={peak_lv}")

    # ── B: Barrer DELTA ───────────────────────────────────────────────────────
    print("\n  ── Exp B: Variando δ — ¿se desplaza el pico? ───────────────────")
    delta_range_B = [0.5, 1.0, 1.5, 2.0, 2.5]
    print(f"  {'δ':>5}  " + "  ".join(f"{lv:>7.1f}" for lv in TEN_F_LEVELS)
          + "  PICO")
    print("  " + "─" * (7 + 10*len(TEN_F_LEVELS)))
    for delta in delta_range_B:
        row_dds = {}
        for lv in TEN_F_LEVELS:
            with patched_vol_max(VOL_MAX_NOM):
                row_dds[lv] = delta_d_opo(_level(lv), delta=delta)
        peak_lv = max(row_dds, key=row_dds.get)
        vals = "  ".join(f"{row_dds[lv]:>7.4f}" for lv in TEN_F_LEVELS)
        print(f"  {delta:>5.2f}  {vals}  L={peak_lv}")


# ═══════════════════════════════════════════════════════════════════════════════
# Figuras
# ═══════════════════════════════════════════════════════════════════════════════

def _make_figures() -> None:
    if not (HAS_PLOT and HAS_NP):
        return
    FIGURES_DIR.mkdir(exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("Robustez de los experimentos centrales", fontsize=12)

    # Panel 0,0: Exp A — Δd_CALMA y Δd_TENSO vs. VOL_MAX
    ax = axes[0, 0]
    vm_vals  = [7.0, 7.5, 8.0, 8.5, 9.0, 9.3, 10.0]
    dd_c_vm, dd_t_vm = [], []
    for vm in vm_vals:
        with patched_vol_max(vm):
            dd_c_vm.append(delta_d_opo(_calma()))
            dd_t_vm.append(delta_d_opo(_tenso()))
    ax.plot(vm_vals, dd_c_vm, "o-", color="#2c7bb6", linewidth=2, label="CALMA")
    ax.plot(vm_vals, dd_t_vm, "s-", color="#d7191c", linewidth=2, label="TENSO")
    ax.axvline(TENSO_PF + TENSO_NF + DELTA_NOM + 2*M.TEN_BASAL_MIN,
               color="gray", linestyle="--", alpha=0.6, label="umbral cap TENSO")
    ax.set_xlabel("VOL_MAX"); ax.set_ylabel("Δd_OPO")
    ax.set_title("Exp A: sensibilidad a la oportunidad\nvs. VOL_MAX")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

    # Panel 0,1: Exp A — Δd vs. δ
    ax = axes[0, 1]
    delta_vals = [0.25, 0.5, 1.0, 1.5, 2.0, 2.5]
    dd_c_d, dd_t_d = [], []
    for d in delta_vals:
        with patched_vol_max(VOL_MAX_NOM):
            dd_c_d.append(delta_d_opo(_calma(), delta=d))
            dd_t_d.append(delta_d_opo(_tenso(), delta=d))
    ax.plot(delta_vals, dd_c_d, "o-", color="#2c7bb6", linewidth=2, label="CALMA")
    ax.plot(delta_vals, dd_t_d, "s-", color="#d7191c", linewidth=2, label="TENSO")
    ax.axvline(VOL_MAX_NOM - (TENSO_PF+TENSO_NF) - 2*M.TEN_BASAL_MIN,
               color="gray", linestyle="--", alpha=0.6, label="umbral cap")
    ax.set_xlabel("δ (magnitud del estímulo)"); ax.set_ylabel("Δd_OPO")
    ax.set_title("Exp A: robustez a δ")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

    # Panel 1,0: Exp B — curvas Δd_OPO vs L para múltiples VOL_MAX
    ax = axes[1, 0]
    palette = plt.cm.viridis
    vm_range_B = [7.0, 7.5, 8.0, 8.5, 9.0, 10.0]
    for i, vm in enumerate(vm_range_B):
        row = []
        for lv in TEN_F_LEVELS:
            with patched_vol_max(vm):
                row.append(delta_d_opo(_level(lv)))
        ax.plot(TEN_F_LEVELS, row, "o-", linewidth=1.8,
                color=palette(i / (len(vm_range_B)-1)),
                label=f"VM={vm:.1f}")
    ax.set_xlabel("ten_F inicial"); ax.set_ylabel("Δd_OPO")
    ax.set_title("Exp B: pico vs. VOL_MAX\n(el pico se desplaza con VM)")
    ax.legend(fontsize=7); ax.grid(True, alpha=0.25)

    # Panel 1,1: Exp B — curvas Δd_OPO vs L para múltiples δ
    ax = axes[1, 1]
    palette2 = plt.cm.plasma
    for i, d in enumerate([0.5, 1.0, 1.5, 2.0, 2.5]):
        row = []
        for lv in TEN_F_LEVELS:
            with patched_vol_max(VOL_MAX_NOM):
                row.append(delta_d_opo(_level(lv), delta=d))
        ax.plot(TEN_F_LEVELS, row, "o-", linewidth=1.8,
                color=palette2(i / 4), label=f"δ={d:.1f}")
    ax.set_xlabel("ten_F inicial"); ax.set_ylabel("Δd_OPO")
    ax.set_title("Exp B: pico vs. δ\n(δ mayor → pico se desplaza a L menor)")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fname = "robustez_experimentos.png"
    fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  Guardado: figures/{fname}")


# ─── Punto de entrada ─────────────────────────────────────────────────────────

def run_all() -> None:
    print("\n═══════════════════════════════════════════════════════════════════")
    print("  Robustez de los experimentos centrales A y B")
    print("═══════════════════════════════════════════════════════════════════")
    run_test1()
    run_test2()
    run_test3()
    _make_figures()
    print("\nListo.")


if __name__ == "__main__":
    run_all()

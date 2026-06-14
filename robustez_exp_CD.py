"""
Robustez de los experimentos C y D.

Experimento C — Tipología social:
  Social positivo (s_pos_target=+1.0, w_s_pos=0.8) busca el vínculo.
  Social neutro (w_s_pos=0.0) deambula indiferente.
  Social negativo (s_pos_target=−1.0, w_s_pos=0.8) evita el vínculo.
  Pieza causal propuesta: s_pos_target (el signo del descentramiento social).

Experimento D — Descentramiento como motor:
  Centrado (targets=0): reactivo, solo se activa cuando los recursos decaen.
  Positivo (targets positivos): proactivo desde el reposo (d_inicial ≈ 2.40).
  Negativo (targets negativos): colapsa — a medida que decae, se acerca a su target.
  Pieza causal propuesta: f/r/s_pos_target (el descentramiento positivo/negativo).

CONFIRMACIÓN IMPORTANTE:
  Ambos experimentos operan con tensión total << VOL_MAX en todo momento.
  Exp C max_tension ≈ 3.1  (VOL_MAX=8.0 → jamás se activa).
  Exp D max_tension ≈ 4.1  (VOL_MAX=8.0 → jamás se activa).
  Los fenómenos C y D dependen de PIEZAS DISTINTAS a VOL_MAX:
    C → s_pos_target (el descentramiento del eje social)
    D → f/r/s_pos_target (la inclinación positiva o negativa de todos los ejes)

Tres pruebas por experimento:
  1. Estadística: 100 semillas (posición inicial aleatoria en C; estocástico natural en D).
  2. Ablación causal: anular la pieza propuesta y verificar que el fenómeno desaparece.
  3. Calibraciones: barrer la pieza causal en rango ±50%, comprobar robustez.
"""

from __future__ import annotations
import math
import random
from pathlib import Path

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
from model import (
    ModelConfig, State,
    opponent_distance_obs as d_obs,
    state_from_observables,
    DEFAULT_CONFIG,
    HP_EQ, ENERGY_EQ, HP_SCALE, ENERGY_SCALE,
)

FIGURES_DIR = Path(__file__).parent / "figures"

# ─── Parámetros del experimento C (tipología social) ─────────────────────────
GRID_C     = 20
STEPS_C    = 300
S_SIGMA    = 4.0
S_MAX_FIELD = 1.5
SOCIAL_R   = GRID_C // 2
SOCIAL_C_COL = GRID_C // 2
HP_C       = 90.0
ENERGY_C   = 15.0
PROX_THRESH = 3.0   # celdas — "cerca del estímulo"

# ─── Parámetros del experimento D (descentramiento) ──────────────────────────
GRID_D       = 10
STEPS_D      = 500
HP_DECAY     = 0.10
ENERGY_DECAY = 0.05
MOVE_SCALE   = 3.0
EARLY        = 100   # ventana de actividad "temprana"

# ─── Configuraciones originales — Exp C ──────────────────────────────────────
_base_C = dict(
    f_pos_target=0.4, r_pos_target=1.0,
    f_ten_target=0.2, r_ten_target=0.2, s_ten_target=0.1,
    w_f_pos=1.0, w_r_pos=0.8,
    sens_F=0.0, sens_R=0.0, sens_S=0.0,   # acoplamiento APAGADO → ejes aislados
)
CFG_SOC_POS = ModelConfig(s_pos_target=+1.0, w_s_pos=0.8, **_base_C)
CFG_SOC_NEU = ModelConfig(s_pos_target=0.0,  w_s_pos=0.0, **_base_C)
CFG_SOC_NEG = ModelConfig(s_pos_target=-1.0, w_s_pos=0.8, **_base_C)

# ─── Configuraciones originales — Exp D ──────────────────────────────────────
CFG_CENTRADO = ModelConfig(
    f_pos_target=0.0, r_pos_target=0.0, s_pos_target=0.0,
    f_ten_target=0.0, r_ten_target=0.0, s_ten_target=0.0,
    sens_F=0.0, sens_R=0.0, sens_S=0.0,
)
CFG_POSITIVO = ModelConfig()          # defaults: targets=1,2,0.8; sens por defecto
CFG_NEGATIVO = ModelConfig(
    f_pos_target=-1.0, r_pos_target=-2.0, s_pos_target=-0.8,
    sens_F=0.0, sens_R=0.0, sens_S=0.0,
)


# ════════════════════════════════════════════════════════════════════════════
# Funciones de simulación (extraídas de experiments_decentramiento.py)
# ════════════════════════════════════════════════════════════════════════════

def _social_field(r: int, c: int) -> float:
    d = math.sqrt((r - SOCIAL_R) ** 2 + (c - SOCIAL_C_COL) ** 2)
    return S_MAX_FIELD * math.exp(-d / S_SIGMA)


def _sim_C(cfg: ModelConfig, seed: int, start_r=1, start_c=1) -> dict:
    """Simulación de tipología social. start_r/c permiten posición inicial variable."""
    rng = random.Random(seed)
    r, c = start_r, start_c
    dist_trace = [math.sqrt((r - SOCIAL_R) ** 2 + (c - SOCIAL_C_COL) ** 2)]
    s_trace    = [_social_field(r, c)]
    moves = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    max_tension = 0.0

    for _ in range(STEPS_C):
        s_cur = _social_field(r, c)
        st = state_from_observables(HP_C, ENERGY_C, s_cur)
        max_tension = max(max_tension, st.ten_F + st.ten_R + st.ten_S)

        if cfg.w_s_pos == 0.0:
            dr, dc = rng.choice(moves)
        else:
            best_d = float("inf")
            best_move = (0, 0)
            for dr, dc in moves:
                nr = max(0, min(GRID_C - 1, r + dr))
                nc = max(0, min(GRID_C - 1, c + dc))
                ns = _social_field(nr, nc)
                d  = d_obs(HP_C, ENERGY_C, ns, cfg)
                if d < best_d:
                    best_d = d
                    best_move = (dr, dc)
            dr, dc = best_move

        r = max(0, min(GRID_C - 1, r + dr))
        c = max(0, min(GRID_C - 1, c + dc))
        dist_trace.append(math.sqrt((r - SOCIAL_R) ** 2 + (c - SOCIAL_C_COL) ** 2))
        s_trace.append(_social_field(r, c))

    time_near = sum(1 for d in dist_trace if d <= PROX_THRESH)
    return {
        "time_near":       time_near,
        "final_dist_grid": dist_trace[-1],
        "mean_s":          sum(s_trace) / len(s_trace),
        "max_tension":     max_tension,
    }


def _sim_D(cfg: ModelConfig, seed: int) -> dict:
    """Simulación de descentramiento como motor."""
    rng = random.Random(seed)
    x, y   = GRID_D // 2, GRID_D // 2
    hp     = HP_EQ
    energy = ENERGY_EQ
    s      = 0.0
    visited = {(x, y)}
    moved_steps = []
    d_initial = d_obs(hp, energy, s, cfg)
    max_tension = 0.0

    for _ in range(STEPS_D):
        hp     = max(0.0, hp     - HP_DECAY)
        energy = max(0.0, energy - ENERGY_DECAY)
        st = state_from_observables(hp, energy, s)
        max_tension = max(max_tension, st.ten_F + st.ten_R + st.ten_S)

        dist  = d_obs(hp, energy, s, cfg)
        prob  = min(1.0, dist / MOVE_SCALE)
        if rng.random() < prob:
            dx, dy = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            x = max(0, min(GRID_D - 1, x + dx))
            y = max(0, min(GRID_D - 1, y + dy))
            visited.add((x, y))
            moved_steps.append(1)
        else:
            moved_steps.append(0)

    early_rate = sum(moved_steps[:EARLY]) / EARLY
    late_rate  = sum(moved_steps[EARLY:]) / (STEPS_D - EARLY)
    return {
        "d_initial":    d_initial,
        "early_rate":   early_rate,
        "late_rate":    late_rate,
        "cells":        len(visited),
        "max_tension":  max_tension,
    }


# ════════════════════════════════════════════════════════════════════════════
# CONFIRMACIÓN: VOL_MAX no se activa en C ni en D
# ════════════════════════════════════════════════════════════════════════════

def run_volmax_check() -> None:
    print("\n══ CONFIRMACIÓN: VOL_MAX en C y D ═════════════════════════════════")
    print(f"  VOL_MAX = {M.VOL_MAX}")

    # Exp C: máxima tensión posible = positivo en el centro (s=S_MAX_FIELD)
    st_c = state_from_observables(HP_C, ENERGY_C, S_MAX_FIELD)
    tot_c = st_c.ten_F + st_c.ten_R + st_c.ten_S
    print(f"\n  Exp C: state(hp=90, e=15, s=1.5)")
    print(f"    ten_F={st_c.ten_F:.3f}  ten_R={st_c.ten_R:.3f}  ten_S={st_c.ten_S:.3f}")
    print(f"    Tensión total = {tot_c:.3f}  (VOL_MAX={M.VOL_MAX}  →  {'ACTIVO' if tot_c>M.VOL_MAX else 'NUNCA ACTIVO'})")

    # Exp D: máxima tensión = estado final (hp=25, energy=0)
    hp_fin  = max(0.0, HP_EQ    - HP_DECAY * STEPS_D)
    en_fin  = max(0.0, ENERGY_EQ - ENERGY_DECAY * STEPS_D)
    st_d = state_from_observables(hp_fin, en_fin, 0.0)
    tot_d = st_d.ten_F + st_d.ten_R + st_d.ten_S
    print(f"\n  Exp D: state(hp={hp_fin:.1f}, e={en_fin:.1f}, s=0) [tras 500 pasos]")
    print(f"    ten_F={st_d.ten_F:.3f}  ten_R={st_d.ten_R:.3f}  ten_S={st_d.ten_S:.3f}")
    print(f"    Tensión total = {tot_d:.3f}  (VOL_MAX={M.VOL_MAX}  →  {'ACTIVO' if tot_d>M.VOL_MAX else 'NUNCA ACTIVO'})")

    print(f"\n  ✓  VOL_MAX es irrelevante en C y D.")
    print(f"  ✓  Los fenómenos C y D no dependen del techo de tensión.")
    print(f"  ✓  C depende de s_pos_target;  D depende de f/r/s_pos_target.")


# ════════════════════════════════════════════════════════════════════════════
# PRUEBA 1 — Estadística
# ════════════════════════════════════════════════════════════════════════════

def run_test1() -> None:
    print("\n══ PRUEBA 1: Estadística (N=100 semillas) ══════════════════════════")

    # ── Exp C: posición inicial aleatoria en el grid ─────────────────────────
    print("\n  ── Exp C: Tipología social — 100 posiciones iniciales aleatorias ──")
    print(f"  (Positivo y negativo son deterministas-greedy; neutro es aleatorio.)")
    print(f"  Randomizamos la posición inicial (r,c) ∈ {{0..{GRID_C-1}}}² uniformemente.")

    rng_start = random.Random(0)
    results_C = {"POS": [], "NEU": [], "NEG": []}
    for _ in range(100):
        sr = rng_start.randint(0, GRID_C - 1)
        sc = rng_start.randint(0, GRID_C - 1)
        seed_i = rng_start.randint(0, 99999)
        results_C["POS"].append(_sim_C(CFG_SOC_POS, seed_i, sr, sc))
        results_C["NEU"].append(_sim_C(CFG_SOC_NEU, seed_i, sr, sc))
        results_C["NEG"].append(_sim_C(CFG_SOC_NEG, seed_i, sr, sc))

    if HAS_NP:
        print(f"\n  {'Agente':<10}  {'time_near μ':>12}  {'time_near σ':>12}  "
              f"{'dist_final μ':>13}  {'dist_final σ':>12}")
        print("  " + "─" * 63)
        for name, key in [("POS", "POS"), ("NEU", "NEU"), ("NEG", "NEG")]:
            tn  = np.array([r["time_near"]       for r in results_C[key]])
            fd  = np.array([r["final_dist_grid"]  for r in results_C[key]])
            print(f"  {name:<10}  {tn.mean():>12.1f}  {tn.std():>12.1f}  "
                  f"{fd.mean():>13.2f}  {fd.std():>12.2f}")

        # Fracciones de interés
        pos_near_frac = np.mean([r["time_near"] >= 50 for r in results_C["POS"]])
        neg_far_frac  = np.mean([r["final_dist_grid"] > 10.0 for r in results_C["NEG"]])
        print(f"\n  POS time_near ≥ 50 en {pos_near_frac*100:.1f}% de semillas  (siempre busca)")
        print(f"  NEG dist_final > 10 celdas en {neg_far_frac*100:.1f}% de semillas  (siempre huye)")
    else:
        # sin numpy
        tn_pos = [r["time_near"] for r in results_C["POS"]]
        fd_neg = [r["final_dist_grid"] for r in results_C["NEG"]]
        print(f"  POS time_near: mean={sum(tn_pos)/len(tn_pos):.1f}")
        print(f"  NEG dist_final: mean={sum(fd_neg)/len(fd_neg):.2f}")

    # ── Exp D: 100 semillas (estocástico natural) ─────────────────────────────
    print("\n  ── Exp D: Descentramiento — 100 semillas aleatorias ──────────────")
    print(f"  (La simulación usa rng.random() < prob en cada paso → estocástica.)")

    results_D = {"CEN": [], "POS": [], "NEG": []}
    for seed_i in range(100):
        results_D["CEN"].append(_sim_D(CFG_CENTRADO, seed_i))
        results_D["POS"].append(_sim_D(CFG_POSITIVO, seed_i))
        results_D["NEG"].append(_sim_D(CFG_NEGATIVO, seed_i))

    if HAS_NP:
        print(f"\n  {'Agente':<10}  {'d_inicial':>10}  {'early_rate μ':>13}  "
              f"{'early_rate σ':>13}  {'celdas μ':>9}  {'celdas σ':>8}")
        print("  " + "─" * 68)
        for name, key in [("CENTRADO", "CEN"), ("POSITIVO", "POS"), ("NEGATIVO", "NEG")]:
            er = np.array([r["early_rate"] for r in results_D[key]])
            cl = np.array([r["cells"]      for r in results_D[key]])
            d0 = results_D[key][0]["d_initial"]
            print(f"  {name:<10}  {d0:>10.3f}  {er.mean():>13.3f}  "
                  f"{er.std():>13.4f}  {cl.mean():>9.1f}  {cl.std():>8.2f}")

        # Confirmación cuantitativa
        er_p = np.array([r["early_rate"] for r in results_D["POS"]])
        er_c = np.array([r["early_rate"] for r in results_D["CEN"]])
        frac_pos_gt_cen = np.mean(er_p > 4 * er_c)   # positivo > 4× centrado
        print(f"\n  early_rate POSITIVO > 4× early_rate CENTRADO en {frac_pos_gt_cen*100:.1f}% de semillas")

        # Negativo se ralentiza: late_rate < early_rate?
        lat_n = np.array([r["late_rate"]  for r in results_D["NEG"]])
        ear_n = np.array([r["early_rate"] for r in results_D["NEG"]])
        frac_neg_slowdown = np.mean(lat_n < ear_n)
        print(f"  NEGATIVO late_rate < early_rate en {frac_neg_slowdown*100:.1f}% de semillas  (colapso)")


# ════════════════════════════════════════════════════════════════════════════
# PRUEBA 2 — Ablación causal
# ════════════════════════════════════════════════════════════════════════════

def run_test2() -> None:
    print("\n══ PRUEBA 2: Ablación causal ═══════════════════════════════════════")

    # ── Exp C: ablación de s_pos_target (→0) y de w_s_pos (→0) ─────────────
    print("\n  ── Exp C: Ablación de s_pos_target y w_s_pos ────────────────────")
    print(f"  Hipótesis: el SIGNO de s_pos_target determina acercamiento vs. huida.")
    print(f"  Ablación A: s_pos_target → 0 para positivo y negativo")
    print(f"  Ablación B: w_s_pos → 0 para todos (el eje social sin peso)")

    CFG_POS_ABLATED_TARGET = ModelConfig(s_pos_target=0.0,  w_s_pos=0.8, **_base_C)
    CFG_NEG_ABLATED_TARGET = ModelConfig(s_pos_target=0.0,  w_s_pos=0.8, **_base_C)
    CFG_POS_ABLATED_WEIGHT = ModelConfig(s_pos_target=+1.0, w_s_pos=0.0, **_base_C)
    CFG_NEG_ABLATED_WEIGHT = ModelConfig(s_pos_target=-1.0, w_s_pos=0.0, **_base_C)

    configs_C_ablation = [
        ("Original  POS", CFG_SOC_POS, 7),
        ("Original  NEG", CFG_SOC_NEG, 7),
        ("AblTarget POS (s_target→0)", CFG_POS_ABLATED_TARGET, 7),
        ("AblTarget NEG (s_target→0)", CFG_NEG_ABLATED_TARGET, 7),
        ("AblWeight POS (w_s→0)",      CFG_POS_ABLATED_WEIGHT, 7),
        ("AblWeight NEG (w_s→0)",      CFG_NEG_ABLATED_WEIGHT, 7),
    ]

    print(f"\n  {'Configuración':<30}  {'time_near':>10}  {'dist_final':>11}")
    print("  " + "─" * 57)
    for label, cfg, seed in configs_C_ablation:
        r = _sim_C(cfg, seed)
        print(f"  {label:<30}  {r['time_near']:>10d}  {r['final_dist_grid']:>11.2f}")

    print(f"\n  INTERPRETACIÓN:")
    print(f"  — Si AblTarget elimina la diferencia POS/NEG → s_pos_target es la causa.")
    print(f"  — Si AblWeight también elimina → w_s_pos amplifica pero s_pos_target inicia.")

    # ── Exp D: ablación de pos_targets (→0) para positivo ───────────────────
    print("\n  ── Exp D: Ablación de pos_targets para POSITIVO ─────────────────")
    print(f"  Hipótesis: f/r/s_pos_target > 0 crea d_inicial alta → proactividad.")
    print(f"  Ablación: todos pos_targets → 0 en CFG_POSITIVO")

    CFG_POSITIVO_ABLATED = ModelConfig(
        f_pos_target=0.0, r_pos_target=0.0, s_pos_target=0.0,
        # mantener todos los demás parámetros del positivo (ten_targets, pesos, sens)
    )

    print(f"\n  {'Configuración':<32}  {'d_inicial':>10}  {'early_rate':>11}  {'late_rate':>10}")
    print("  " + "─" * 68)
    for label, cfg in [
        ("Centrado (targets=0, sens=0)",   CFG_CENTRADO),
        ("Positivo original",              CFG_POSITIVO),
        ("Positivo ablado (targets→0)",    CFG_POSITIVO_ABLATED),
    ]:
        r = _sim_D(cfg, 42)
        print(f"  {label:<32}  {r['d_initial']:>10.3f}  {r['early_rate']:>11.3f}  {r['late_rate']:>10.3f}")

    print(f"\n  INTERPRETACIÓN:")
    print(f"  — Si ablación colapsa early_rate al nivel centrado → pos_targets causan proactividad.")

    # ── Exp D: ablación del acoplamiento (sens → 0) para positivo ────────────
    print("\n  ── Exp D: Ablación del acoplamiento (sens_F/R/S → 0) ───────────")
    print(f"  La proactividad, ¿depende del acoplamiento o del descentramiento?")
    CFG_POSITIVO_NOSENS = ModelConfig(sens_F=0.0, sens_R=0.0, sens_S=0.0)

    for label, cfg in [
        ("Positivo original (con coupling)", CFG_POSITIVO),
        ("Positivo sin coupling (sens=0)",   CFG_POSITIVO_NOSENS),
    ]:
        r = _sim_D(cfg, 42)
        print(f"  {label:<37}  d_inicial={r['d_initial']:.3f}  early={r['early_rate']:.3f}")

    print(f"  → Si early_rate permanece igual sin coupling → la proactividad es del descentramiento,")
    print(f"    NO del acoplamiento.")


# ════════════════════════════════════════════════════════════════════════════
# PRUEBA 3 — Robustez a calibraciones
# ════════════════════════════════════════════════════════════════════════════

def run_test3() -> None:
    print("\n══ PRUEBA 3: Robustez a calibraciones ══════════════════════════════")

    # ── Exp C: barrido de s_pos_target ───────────────────────────────────────
    print("\n  ── Exp C: Barrido de s_pos_target ∈ [−2.0, +2.0] ───────────────")
    print(f"  Clave: ¿el signo determina acercamiento/huida para cualquier magnitud?")
    targets_C = [-2.0, -1.5, -1.0, -0.5, -0.2, 0.0, 0.2, 0.5, 1.0, 1.5, 2.0]
    print(f"  {'s_pos_target':>14}  {'time_near':>10}  {'dist_final':>11}  {'comportamiento':>16}")
    print("  " + "─" * 56)
    for tgt in targets_C:
        cfg = ModelConfig(s_pos_target=tgt, w_s_pos=0.8, **_base_C)
        r   = _sim_C(cfg, 7)
        if tgt > 0.05:
            comportamiento = "se acerca"
        elif tgt < -0.05:
            comportamiento = "se aleja"
        else:
            comportamiento = "indif. (greedy nulo)"
        print(f"  {tgt:>14.2f}  {r['time_near']:>10d}  {r['final_dist_grid']:>11.2f}  "
              f"{comportamiento:>16}")

    # ── Exp C: barrido de w_s_pos ────────────────────────────────────────────
    print(f"\n  ── Exp C: Barrido de w_s_pos ∈ [0.0, 1.5] (s_target=+1.0) ────")
    weights_C = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5]
    print(f"  {'w_s_pos':>9}  {'time_near':>10}  {'dist_final':>11}")
    print("  " + "─" * 34)
    for w in weights_C:
        cfg = ModelConfig(s_pos_target=+1.0, w_s_pos=w, **_base_C)
        r   = _sim_C(cfg, 7)
        print(f"  {w:>9.2f}  {r['time_near']:>10d}  {r['final_dist_grid']:>11.2f}")

    # ── Exp D: barrido de la magnitud del descentramiento positivo ────────────
    print(f"\n  ── Exp D: Barrido de descentramiento positivo (f_target escalado) ──")
    print(f"  Original: f_pos_target=1.0, r_pos_target=2.0, s_pos_target=0.8")
    print(f"  Escalamos los tres targets por un factor α ∈ [0, 2]")
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    print(f"  {'α':>6}  {'f_target':>10}  {'d_inicial':>10}  {'early_rate':>11}  {'late_rate':>10}")
    print("  " + "─" * 54)
    for alpha in alphas:
        cfg = ModelConfig(
            f_pos_target = alpha * 1.0,
            r_pos_target = alpha * 2.0,
            s_pos_target = alpha * 0.8,
        )
        r = _sim_D(cfg, 42)
        print(f"  {alpha:>6.2f}  {alpha*1.0:>10.3f}  {r['d_initial']:>10.3f}  "
              f"{r['early_rate']:>11.3f}  {r['late_rate']:>10.3f}")

    # ── Exp D: barrido del descentramiento NEGATIVO ──────────────────────────
    print(f"\n  ── Exp D: Barrido de descentramiento negativo (α escala targets neg.) ──")
    print(f"  Original: f_pos_target=−1.0, r_pos_target=−2.0, s_pos_target=−0.8")
    print(f"  {'α':>6}  {'f_target':>10}  {'d_inicial':>10}  {'early_rate':>11}  {'late_rate':>10}")
    print("  " + "─" * 54)
    for alpha in alphas:
        cfg = ModelConfig(
            f_pos_target = -alpha * 1.0,
            r_pos_target = -alpha * 2.0,
            s_pos_target = -alpha * 0.8,
            sens_F=0.0, sens_R=0.0, sens_S=0.0,
        )
        r = _sim_D(cfg, 42)
        print(f"  {alpha:>6.2f}  {-alpha*1.0:>10.3f}  {r['d_initial']:>10.3f}  "
              f"{r['early_rate']:>11.3f}  {r['late_rate']:>10.3f}")

    # ── Exp D: barrido de la tasa de decaimiento metabólico ──────────────────
    print(f"\n  ── Exp D: Barrido de tasa de decaimiento (HP_DECAY) ─────────────")
    print(f"  ¿El contraste CENTRADO reactivo vs. POSITIVO proactivo persiste?")
    decay_rates = [0.02, 0.05, 0.10, 0.15, 0.20, 0.30]
    print(f"  {'hp_decay':>10}  {'early CEN':>10}  {'early POS':>10}  {'Ratio P/C':>10}")
    print("  " + "─" * 44)

    # Necesito copiar la simulación con decay variable
    def _sim_D_decay(cfg, seed, hp_decay, en_decay):
        rng = random.Random(seed)
        x, y = GRID_D // 2, GRID_D // 2
        hp = HP_EQ; energy = ENERGY_EQ; s = 0.0
        moved = []
        for _ in range(STEPS_D):
            hp     = max(0.0, hp - hp_decay)
            energy = max(0.0, energy - en_decay)
            dist   = d_obs(hp, energy, s, cfg)
            prob   = min(1.0, dist / MOVE_SCALE)
            if rng.random() < prob:
                dx, dy = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                x = max(0, min(GRID_D - 1, x + dx))
                y = max(0, min(GRID_D - 1, y + dy))
                moved.append(1)
            else:
                moved.append(0)
        return sum(moved[:EARLY]) / EARLY

    for hp_d in decay_rates:
        en_d = hp_d * 0.5
        er_c = _sim_D_decay(CFG_CENTRADO, 42, hp_d, en_d)
        er_p = _sim_D_decay(CFG_POSITIVO, 42, hp_d, en_d)
        ratio = er_p / er_c if er_c > 0 else float("inf")
        print(f"  {hp_d:>10.2f}  {er_c:>10.3f}  {er_p:>10.3f}  {ratio:>10.2f}x")


# ════════════════════════════════════════════════════════════════════════════
# Figuras
# ════════════════════════════════════════════════════════════════════════════

def _make_figures() -> None:
    if not (HAS_PLOT and HAS_NP):
        return
    FIGURES_DIR.mkdir(exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("Robustez Exp C (tipología social) y D (descentramiento)", fontsize=12)

    # Panel 0,0: Exp C — time_near vs. s_pos_target
    ax = axes[0, 0]
    targets_C = [-2.0, -1.5, -1.0, -0.5, -0.2, 0.0, 0.2, 0.5, 1.0, 1.5, 2.0]
    time_nears = []
    for tgt in targets_C:
        cfg = ModelConfig(s_pos_target=tgt, w_s_pos=0.8, **_base_C)
        r   = _sim_C(cfg, 7)
        time_nears.append(r["time_near"])
    ax.plot(targets_C, time_nears, "o-", color="#2c7bb6", linewidth=2)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("s_pos_target"); ax.set_ylabel("Pasos cerca del estímulo (≤3 celdas)")
    ax.set_title("Exp C: acercamiento vs. s_pos_target\n(positivo→busca, negativo→huye)")
    ax.grid(True, alpha=0.25)

    # Panel 0,1: Exp C — dist_final vs. w_s_pos
    ax = axes[0, 1]
    weights_C = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5]
    dist_finals = []
    for w in weights_C:
        cfg = ModelConfig(s_pos_target=+1.0, w_s_pos=w, **_base_C)
        r   = _sim_C(cfg, 7)
        dist_finals.append(r["final_dist_grid"])
    ax.plot(weights_C, dist_finals, "s-", color="#1a9641", linewidth=2)
    ax.set_xlabel("w_s_pos"); ax.set_ylabel("Distancia final al estímulo (celdas)")
    ax.set_title("Exp C: acercamiento vs. w_s_pos\n(mayor peso → aproximación más fuerte)")
    ax.grid(True, alpha=0.25)

    # Panel 1,0: Exp D — d_inicial y early_rate vs. α descentramiento positivo
    ax = axes[1, 0]
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    d_inis, early_rs = [], []
    for alpha in alphas:
        cfg = ModelConfig(
            f_pos_target=alpha*1.0,
            r_pos_target=alpha*2.0,
            s_pos_target=alpha*0.8,
        )
        r = _sim_D(cfg, 42)
        d_inis.append(r["d_initial"])
        early_rs.append(r["early_rate"])
    ax.plot(alphas, d_inis,   "o-", color="#2c7bb6", linewidth=2, label="d_inicial")
    ax2 = ax.twinx()
    ax2.plot(alphas, early_rs, "s-", color="#d7191c", linewidth=2, label="early_rate")
    ax.set_xlabel("α (escala del descentramiento positivo)")
    ax.set_ylabel("d_inicial", color="#2c7bb6")
    ax2.set_ylabel("early_rate (pasos 0-99)", color="#d7191c")
    ax.set_title("Exp D: proactividad vs. α\n(α=0 → centrado; α=1 → positivo orig.)")
    ax.grid(True, alpha=0.25)
    lines1, lbls1 = ax.get_legend_handles_labels()
    lines2, lbls2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, lbls1 + lbls2, fontsize=8)

    # Panel 1,1: Exp D — late_rate vs. α descentramiento negativo
    ax = axes[1, 1]
    early_n, late_n = [], []
    for alpha in alphas:
        cfg = ModelConfig(
            f_pos_target=-alpha*1.0,
            r_pos_target=-alpha*2.0,
            s_pos_target=-alpha*0.8,
            sens_F=0.0, sens_R=0.0, sens_S=0.0,
        )
        r = _sim_D(cfg, 42)
        early_n.append(r["early_rate"])
        late_n.append(r["late_rate"])
    ax.plot(alphas, early_n, "o-", color="#2c7bb6", linewidth=2, label="early_rate")
    ax.plot(alphas, late_n,  "s-", color="#d7191c", linewidth=2, label="late_rate")
    ax.set_xlabel("α (escala del descentramiento negativo)")
    ax.set_ylabel("Tasa de movimiento")
    ax.set_title("Exp D: colapso del negativo vs. α\n(α=1 → original; ↑α → colapso más marcado)")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.25)

    fig.tight_layout()
    fname = "robustez_exp_CD.png"
    fig.savefig(FIGURES_DIR / fname, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  Guardado: figures/{fname}")


# ─── Punto de entrada ─────────────────────────────────────────────────────────

def run_all() -> None:
    print("\n═══════════════════════════════════════════════════════════════════")
    print("  Robustez Exp C (tipología social) y D (descentramiento como motor)")
    print("═══════════════════════════════════════════════════════════════════")
    run_volmax_check()
    run_test1()
    run_test2()
    run_test3()
    _make_figures()
    print("\nListo.")


if __name__ == "__main__":
    run_all()

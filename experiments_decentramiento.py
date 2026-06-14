"""
Experimentos de descentramiento: la inclinación positiva como motor de vida.

PRINCIPIO TEÓRICO (justificado, no arbitrario)
===============================================
Los tres ejes (F físico, R recursos, S social) nacen descentrados hacia el polo
positivo. Esta inclinación no es arbitraria:

  - El eje FÍSICO es el MÁS DESCENTRADO porque su pérdida es IRREVERSIBLE y
    TERMINAL: la muerte elimina también los ejes R y S. No hay segunda oportunidad
    para los otros motivos si el físico colapsa. Por eso su target posicional está
    en el máximo alcanzable (f_pos_target = 1.0).

  - Los ejes R (recursos) y S (social) tienen descentramiento moderado. El daño en
    estos ejes es recuperable: los recursos pueden regenerarse, los vínculos
    repararse. Por eso su importancia en la ecuación de distancia es menor que la
    del eje físico, aunque también están descentrados positivamente.

  - Un agente CENTRADO (target = 0 en todos los ejes) tiene distancia cero en el
    equilibrio: sin urgencia, sin movimiento, sin vida.

  - Un agente NEGATIVAMENTE DESCENTRADO (target negativo) es atraído hacia el daño,
    la pérdida y el aislamiento: el perfil del instinto de muerte.

Experimento A: el descentramiento como motor en entorno vacío.
Experimento B: tipología conductual por descentramiento del eje social.
"""

from __future__ import annotations
import random
import math
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("AVISO: pip install numpy matplotlib")

import model as M
from model import ModelConfig, opponent_distance_obs as opponent_distance

FIGURES_DIR = Path(__file__).parent / "figures"

# ────────────────────────────────────────────────────────────────────────────
# Configuraciones de agentes (descentramiento)
# ────────────────────────────────────────────────────────────────────────────

# CENTRADO: el equilibrio es el ideal. Distancia = 0 cuando hp=HP_EQ, energy=ENERGY_EQ.
# Se anulan también los targets de tensión: en equilibrio la tensión es 0 = target → dist=0.
CFG_CENTRADO = ModelConfig(
    f_pos_target=0.0, r_pos_target=0.0, s_pos_target=0.0,
    f_ten_target=0.0, r_ten_target=0.0, s_ten_target=0.0,
    f_coupling=0.0,
)

# POSITIVO: inclinación hacia integridad, recursos y vínculos.
# Físico más descentrado porque su pérdida es irreversible y terminal.
CFG_POSITIVO = ModelConfig(
    f_pos_target=1.0,   # hp máxima (irreversible si se pierde)
    r_pos_target=2.0,   # energía máxima (recuperable)
    s_pos_target=0.8,   # vínculo social moderado (recuperable)
    f_coupling=0.5,
)

# NEGATIVO: inclinación hacia daño, pérdida y aislamiento.
# Espejo del positivo: busca lo que el positivo huye.
CFG_NEGATIVO = ModelConfig(
    f_pos_target=-1.0,
    r_pos_target=-2.0,
    s_pos_target=-0.8,
    f_coupling=0.0,  # sin acoplamiento: no hay urgencia cruzada bajo amenaza
)


# ════════════════════════════════════════════════════════════════════════════
# EXPERIMENTO A — El descentramiento como motor en entorno vacío
# ════════════════════════════════════════════════════════════════════════════

GRID_A      = 10
STEPS_A     = 500
HP_DECAY    = 0.10   # coste metabólico por paso (igual para todos)
ENERGY_DECAY = 0.05  # ídem
MOVE_SCALE  = 3.0    # distancia donde prob(moverse)=1.0


def _sim_agent_a(cfg: ModelConfig, seed: int, label: str) -> dict:
    rng = random.Random(seed)
    x, y  = GRID_A // 2, GRID_A // 2
    hp    = M.HP_EQ
    energy = M.ENERGY_EQ
    s     = 0.0

    visited   = {(x, y)}
    visit_map = [[0] * GRID_A for _ in range(GRID_A)]
    visit_map[x][y] += 1
    distances  = []
    move_probs = []
    moved_steps = []   # 1 si se movió en este paso, 0 si no

    for _ in range(STEPS_A):
        # Decaimiento metabólico idéntico para los tres agentes (entorno vacío)
        hp     = max(0.0, hp     - HP_DECAY)
        energy = max(0.0, energy - ENERGY_DECAY)

        dist = opponent_distance(hp, energy, s, cfg)
        distances.append(dist)
        prob = min(1.0, dist / MOVE_SCALE)
        move_probs.append(prob)

        if rng.random() < prob:
            dx, dy = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            x = max(0, min(GRID_A - 1, x + dx))
            y = max(0, min(GRID_A - 1, y + dy))
            visited.add((x, y))
            visit_map[x][y] += 1
            moved_steps.append(1)
        else:
            moved_steps.append(0)

    return {
        "label":         label,
        "cells_visited": len(visited),
        "distances":     distances,
        "move_probs":    move_probs,
        "moved_steps":   moved_steps,
        "visit_map":     visit_map,
    }


def run_exp_a() -> None:
    """Entorno vacío 10×10, 500 pasos. Tres agentes, mismo metabolismo."""
    seed = 42
    results = [
        _sim_agent_a(CFG_CENTRADO, seed, "Centrado (target=0)"),
        _sim_agent_a(CFG_POSITIVO, seed, "Positivo (target max)"),
        _sim_agent_a(CFG_NEGATIVO, seed, "Negativo (target min)"),
    ]

    EARLY = 100   # ventana para medir actividad "temprana"

    print("\n══ Experimento A: Descentramiento como motor ═══════════════════")
    for r in results:
        early_rate = sum(r["moved_steps"][:EARLY]) / EARLY
        late_rate  = sum(r["moved_steps"][EARLY:]) / (STEPS_A - EARLY)
        print(f"  {r['label']}")
        print(f"    Celdas distintas visitadas : {r['cells_visited']:>4d} / {GRID_A**2}")
        print(f"    Distancia inicial / final  : {r['distances'][0]:.3f} → {r['distances'][-1]:.3f}")
        print(f"    Tasa movimiento pasos 0-99 : {early_rate:.3f}  (TARDÍO si < positivo)")
        print(f"    Tasa movimiento pasos 100+ : {late_rate:.3f}")

    # Predicciones
    cells = [r["cells_visited"] for r in results]
    c_idx, p_idx, n_idx = 0, 1, 2
    c_early = sum(results[c_idx]["moved_steps"][:EARLY]) / EARLY
    p_early = sum(results[p_idx]["moved_steps"][:EARLY]) / EARLY
    pred_reactive = c_early < p_early * 0.5   # centrado mucho menos activo en etapa temprana
    pred_active   = cells[p_idx] > cells[n_idx]
    pred_decrease = results[n_idx]["move_probs"][-1] < results[n_idx]["move_probs"][0]
    print(f"\n  Predicción CENTRADO reactivo (no proactivo) : {'✓' if pred_reactive else '✗'} "
          f"(tasas early: centrado={c_early:.3f} vs positivo={p_early:.3f})")
    print(f"  Predicción POSITIVO más activo total       : {'✓' if pred_active else '✗'} "
          f"({cells[p_idx]} vs {cells[n_idx]} celdas)")
    print(f"  Predicción NEGATIVO se ralentiza           : {'✓' if pred_decrease else '✗'} "
          f"(prob: {results[n_idx]['move_probs'][0]:.3f} → {results[n_idx]['move_probs'][-1]:.3f})")

    if not HAS_PLOT:
        return

    colors = ["#777777", "#2c7bb6", "#d7191c"]
    labels = [r["label"] for r in results]
    steps  = list(range(STEPS_A))

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle("Exp A: Descentramiento como motor de vida (entorno vacío)", fontsize=12)

    # Panel 1: actividad por ventana de 25 pasos — revela CUÁNDO actúa cada agente
    W = 25
    n_windows = STEPS_A // W
    window_centers = [W * i + W // 2 for i in range(n_windows)]
    for r, color in zip(results, colors):
        act = [sum(r["moved_steps"][W*i:W*(i+1)]) / W for i in range(n_windows)]
        axes[0].plot(window_centers, act, color=color, label=r["label"], linewidth=2)
    axes[0].set_xlabel("Paso")
    axes[0].set_ylabel("Tasa de movimiento (ventana 25 pasos)")
    axes[0].set_title("Actividad temporal: ¿cuándo actúa cada agente?")
    axes[0].set_ylim(0, 1.05)
    axes[0].legend(fontsize=8)
    axes[0].axvline(EARLY, color="gray", linestyle=":", alpha=0.5)
    axes[0].grid(True, alpha=0.2)

    # Panel 2: distancia al objetivo en el tiempo
    for r, color in zip(results, colors):
        axes[1].plot(steps, r["distances"], color=color, label=r["label"], linewidth=1.5, alpha=0.8)
    axes[1].set_xlabel("Paso")
    axes[1].set_ylabel("Distancia homeostática (urgencia)")
    axes[1].set_title("Urgencia a lo largo del tiempo")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.2)

    # Panel 3: probabilidad de movimiento (promedio móvil de 20 pasos)
    def smooth(series, w=20):
        return [sum(series[max(0, i-w):i+1]) / (min(i+1, w+1))
                for i in range(len(series))]

    for r, color in zip(results, colors):
        axes[2].plot(steps, smooth(r["move_probs"]), color=color, label=r["label"], linewidth=1.5)
    axes[2].set_xlabel("Paso")
    axes[2].set_ylabel("Prob. movimiento (media móvil 20 pasos)")
    axes[2].set_title("Actividad temporal")
    axes[2].legend(fontsize=8)
    axes[2].set_ylim(0, 1.05)
    axes[2].grid(True, alpha=0.2)

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / "expA_descentramiento_motor.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Guardado: figures/expA_descentramiento_motor.png")


# ════════════════════════════════════════════════════════════════════════════
# EXPERIMENTO B — Tipología social por descentramiento del eje S
# ════════════════════════════════════════════════════════════════════════════

GRID_B        = 20
STEPS_B       = 300
SOCIAL_R      = GRID_B // 2   # fila del estímulo social
SOCIAL_C      = GRID_B // 2   # columna del estímulo social
S_SIGMA       = 4.0    # radio del campo social (celdas): cuanto menor, más puntual
S_MAX_FIELD   = 1.5    # s máxima en el centro del campo

# Estado físico y material fijo (entorno sin amenazas ni escasez)
HP_B      = 90.0
ENERGY_B  = 15.0

# Configuraciones para Exp B: solo varía el eje social
# Los ejes F y R están fijos y cómodos
_base = dict(
    f_pos_target=0.4, r_pos_target=1.0,   # moderadamente positivos (cómodo)
    f_ten_target=0.2, r_ten_target=0.2, s_ten_target=0.1,
    w_f_pos=1.0, w_r_pos=0.8,
    f_coupling=0.0,
)

# Social POSITIVO: busca el vínculo
CFG_SOC_POS = ModelConfig(s_pos_target=+1.0, w_s_pos=0.8, **_base)

# Social NEUTRO: indiferente (peso social = 0)
CFG_SOC_NEU = ModelConfig(s_pos_target=0.0, w_s_pos=0.0, **_base)

# Social NEGATIVO: evita/daña el vínculo — perfil psicopático
CFG_SOC_NEG = ModelConfig(s_pos_target=-1.0, w_s_pos=0.8, **_base)


def _dist_to_social(r: int, c: int) -> float:
    return math.sqrt((r - SOCIAL_R) ** 2 + (c - SOCIAL_C) ** 2)


def _social_field(r: int, c: int) -> float:
    """
    Campo social continuo: s = S_MAX_FIELD · exp(−d / S_SIGMA).
    Crea un gradiente suave que el agente puede seguir de forma greedy.
    Cero lejos del estímulo; máximo en el centro.
    """
    return S_MAX_FIELD * math.exp(-_dist_to_social(r, c) / S_SIGMA)


def _sim_agent_b(cfg: ModelConfig, seed: int, label: str) -> dict:
    rng = random.Random(seed)
    # Empieza en esquina opuesta al estímulo
    r, c = 1, 1

    positions  = [(r, c)]
    s_trace    = [_social_field(r, c)]
    dist_trace = [_dist_to_social(r, c)]

    # Candidatos de movimiento (incluye quedarse)
    moves = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

    for _ in range(STEPS_B):
        # s determinado por el campo en la posición actual
        s_current = _social_field(r, c)

        if cfg.w_s_pos == 0.0:
            # Neutro: paseo aleatorio (el campo social no afecta su distancia)
            dr, dc = rng.choice(moves)
        else:
            # Greedy: elige el movimiento que minimiza la distancia homeostática
            # El campo social crea un gradiente que el agente puede seguir
            best_d = float("inf")
            best_move = (0, 0)
            for dr, dc in moves:
                nr = max(0, min(GRID_B - 1, r + dr))
                nc = max(0, min(GRID_B - 1, c + dc))
                ns = _social_field(nr, nc)
                d  = opponent_distance(HP_B, ENERGY_B, ns, cfg)
                if d < best_d:
                    best_d    = d
                    best_move = (dr, dc)
            dr, dc = best_move

        r = max(0, min(GRID_B - 1, r + dr))
        c = max(0, min(GRID_B - 1, c + dc))

        positions.append((r, c))
        s_trace.append(_social_field(r, c))
        dist_trace.append(_dist_to_social(r, c))

    return {
        "label":      label,
        "positions":  positions,
        "s_trace":    s_trace,
        "dist_trace": dist_trace,
    }


def run_exp_b() -> None:
    """
    Un solo estímulo social en el centro del grid.
    Tres agentes difieren solo en s_pos_target.
    """
    seed = 7
    configs = [
        (CFG_SOC_POS, "Social positivo (busca vínculo)"),
        (CFG_SOC_NEU, "Social neutro (indiferente)"),
        (CFG_SOC_NEG, "Social negativo (evita vínculo)"),
    ]
    results = [_sim_agent_b(cfg, seed, label) for cfg, label in configs]

    PROX_THRESH = 3.0   # celdas — "cerca del estímulo"

    print("\n══ Experimento B: Tipología social ════════════════════════════")
    for r in results:
        time_near = sum(1 for d in r["dist_trace"] if d <= PROX_THRESH)
        mean_s = sum(r["s_trace"]) / len(r["s_trace"])
        final_dist_grid = r["dist_trace"][-1]
        print(f"  {r['label']}")
        print(f"    Pasos dentro de {PROX_THRESH:.0f} celdas del punto : {time_near:>4d} / {STEPS_B}")
        print(f"    s medio                               : {mean_s:>6.3f}")
        print(f"    Distancia grid al punto (final)       : {final_dist_grid:.2f} celdas")

    # Verificar predicciones
    d_pos_final = results[0]["dist_trace"][-1]
    d_neg_final = results[2]["dist_trace"][-1]
    t_pos_near  = sum(1 for d in results[0]["dist_trace"] if d <= PROX_THRESH)
    pred_approach  = d_pos_final < 5.0            # positivo termina cerca
    pred_avoidance = d_neg_final > d_pos_final    # negativo termina más lejos

    print(f"\n  Predicción positivo SE ACERCA  : {'✓' if pred_approach  else '✗'} "
          f"(dist final = {d_pos_final:.1f} celdas, {t_pos_near} pasos cercanos)")
    print(f"  Predicción negativo SE ALEJA   : {'✓' if pred_avoidance else '✗'} "
          f"(dist final pos={d_pos_final:.1f} neg={d_neg_final:.1f})")

    if not HAS_PLOT:
        return

    colors_b = ["#2c7bb6", "#777777", "#d7191c"]
    steps  = list(range(STEPS_B + 1))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Exp B: Tipología por descentramiento del eje social", fontsize=12)

    # Panel 1: trayectorias en el grid
    ax = axes[0]
    for r, color in zip(results, colors_b):
        rs = [p[0] for p in r["positions"]]
        cs = [p[1] for p in r["positions"]]
        ax.plot(cs, rs, color=color, alpha=0.6, linewidth=1.2, label=r["label"])
        ax.scatter(cs[0], rs[0], color=color, marker="o", s=60, zorder=5)
        ax.scatter(cs[-1], rs[-1], color=color, marker="^", s=80, zorder=5)

    # Estímulo social
    ax.scatter(SOCIAL_C, SOCIAL_R, color="gold", marker="*", s=300, zorder=10,
               edgecolors="black", linewidth=0.8, label="Estímulo social")
    ax.set_xlim(-0.5, GRID_B - 0.5)
    ax.set_ylim(-0.5, GRID_B - 0.5)
    ax.set_aspect("equal")
    ax.set_xlabel("Columna")
    ax.set_ylabel("Fila")
    ax.set_title("Trayectorias (○ inicio, △ fin)")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.2)

    # Panel 2: valor s a lo largo del tiempo
    ax = axes[1]
    for r, color in zip(results, colors_b):
        ax.plot(steps, r["s_trace"], color=color, label=r["label"], linewidth=1.8, alpha=0.85)
    ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("Paso")
    ax.set_ylabel("Estado social (s)")
    ax.set_title("Evolución del estado social")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / "expB_tipologia_social.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Guardado: figures/expB_tipologia_social.png")


# ────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═══════════════════════════════════════════════════════════════════")
    print("  Experimentos de descentramiento")
    print("═══════════════════════════════════════════════════════════════════")
    run_exp_a()
    run_exp_b()
    print("\nListo. Figuras en: figures/")

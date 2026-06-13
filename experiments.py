"""
Experimentos: fenómenos emergentes del modelo de fuerzas oponentes.

Experimento 1 — Fenotipos explorador vs. apático
  Varía F_TEN_TARGET y R_TEN_TARGET. Alto → explorador; bajo → apático.

Experimento 2 — Aburrimiento asintótico
  Con estado físico y material estable, la tensión cae → distancia sube → el
  agente busca estimulación aunque no haya necesidad homeostática.

Experimento 3 — Curiosidad push-pull
  Un estímulo novedoso sube ambas fuerzas (p y n) simultáneamente → tensión
  alta + posición neutra → atractivo mientras tensión < target.

Produce figuras en ./figures/
"""

from __future__ import annotations
import math
import sys
from pathlib import Path

try:
    import numpy as np
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("numpy/matplotlib no instalados — ejecuta: pip install numpy matplotlib")

import model as M


def run_exp1_phenotypes() -> None:
    """Distancia vs nivel de energía para explorador (ten_target alto) y apático (bajo)."""
    energies = [e / 10 for e in range(0, 201)]  # 0 a 20

    configs = [
        ("Explorador",  0.60, 0.60),   # target de tensión alto → quiere más estimulación
        ("Apático",     0.05, 0.05),   # target de tensión bajo → se conforma con poco
    ]

    if not HAS_PLOT:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    for label, f_ten, r_ten in configs:
        M.F_TEN_TARGET = f_ten
        M.R_TEN_TARGET = r_ten
        dists = [M.opponent_distance(75.0, e, 0.5) for e in energies]
        ax.plot(energies, dists, label=label, linewidth=2)

    # Restaurar defaults
    M.F_TEN_TARGET = 0.30
    M.R_TEN_TARGET = 0.30

    ax.set_xlabel("Energía (recursos)")
    ax.set_ylabel("Distancia homeostática (urgencia)")
    ax.set_title("Experimento 1: Fenotipos explorador vs. apático")
    ax.legend()
    ax.grid(True, alpha=0.3)
    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/exp1_phenotypes.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Guardado: figures/exp1_phenotypes.png")


def run_exp2_boredom() -> None:
    """Tensión cae con el tiempo sin eventos → distancia sube (aburrimiento)."""
    # Simula un agente en reposo: hp=100, energy=20, s=0.5 estable
    # La tensión decae exponencialmente simulando ausencia de estimulación
    steps = list(range(60))
    ten_decay = [0.5 * math.exp(-t / 15) + 0.01 for t in steps]
    distances = []
    for ten in ten_decay:
        hp_sim    = M.HP_EQ    + ten * M.HP_SCALE
        energy_sim = M.ENERGY_EQ + ten * M.ENERGY_SCALE
        distances.append(M.opponent_distance(min(hp_sim, M.HP_CAP),
                                             min(energy_sim, M.ENERGY_CAP), 0.5))

    if not HAS_PLOT:
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    ax1.plot(steps, ten_decay, color="steelblue", linewidth=2)
    ax1.axhline(M.F_TEN_TARGET, color="steelblue", linestyle="--", alpha=0.6,
                label=f"target tensión = {M.F_TEN_TARGET}")
    ax1.set_ylabel("Tensión (f+ + f-)")
    ax1.set_title("Experimento 2: Aburrimiento asintótico")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(steps, distances, color="tomato", linewidth=2)
    ax2.set_xlabel("Pasos en reposo")
    ax2.set_ylabel("Distancia homeostática")
    ax2.grid(True, alpha=0.3)

    Path("figures").mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig("figures/exp2_boredom.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Guardado: figures/exp2_boredom.png")


def run_exp3_curiosity() -> None:
    """Push-pull: estímulo novedoso sube ambas fuerzas → atractivo hasta cierto arousal."""
    # Muestra distancia en función del nivel de novedad (sube ambas fuerzas juntas)
    novelty_levels = [n / 100 for n in range(0, 101)]
    distances_low_ten  = []   # partiendo de tensión baja (aburrido)
    distances_high_ten = []   # partiendo de tensión alta (ya activado)

    for nov in novelty_levels:
        # Bajo: tensión baja → novedad es atractiva (baja distancia)
        hp_low  = M.HP_EQ + 0.1 * M.HP_SCALE
        en_low  = M.ENERGY_EQ + 0.1 * M.ENERGY_SCALE
        s_low   = 0.1 + nov * 0.5    # novedad sube S (contacto social) moderadamente
        distances_low_ten.append(M.opponent_distance(hp_low, en_low, s_low))

        # Alto: tensión ya alta → novedad adicional es repulsiva (sube distancia)
        hp_high  = M.HP_EQ + 0.8 * M.HP_SCALE
        en_high  = M.ENERGY_EQ + 0.8 * M.ENERGY_SCALE
        s_high   = 0.8 + nov * 0.5
        distances_high_ten.append(M.opponent_distance(
            min(hp_high, M.HP_CAP), min(en_high, M.ENERGY_CAP), s_high))

    if not HAS_PLOT:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(novelty_levels, distances_low_ten,
            label="Partiendo de tensión baja (aburrido)", linewidth=2, color="green")
    ax.plot(novelty_levels, distances_high_ten,
            label="Partiendo de tensión alta (activado)", linewidth=2, color="orange")
    ax.set_xlabel("Nivel de novedad del estímulo")
    ax.set_ylabel("Distancia homeostática (urgencia)")
    ax.set_title("Experimento 3: Curiosidad push-pull")
    ax.legend()
    ax.grid(True, alpha=0.3)

    Path("figures").mkdir(exist_ok=True)
    fig.savefig("figures/exp3_curiosity.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Guardado: figures/exp3_curiosity.png")


if __name__ == "__main__":
    print("Ejecutando experimentos...")
    run_exp1_phenotypes()
    run_exp2_boredom()
    run_exp3_curiosity()
    print("Listo. Revisa la carpeta figures/")

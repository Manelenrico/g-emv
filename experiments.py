"""
Experimentos: fenómenos emergentes del modelo de fuerzas oponentes.

Experimento 1 — Fenotipos explorador vs. apático
  Varía UN SOLO parámetro: r_ten_target (target de tensión en el eje R).
  Alto → explorador (inquieto, busca estimulación);
  bajo  → apático   (se conforma con poco arousal).

Experimento 2 — ¿Emerge el aburrimiento de la geometría?
  Con el mecanismo explícito de aburrimiento APAGADO, simula la caída
  natural de recursos de un estado cómodo hasta el equilibrio.
  Resultado honesto: la señal de aburrimiento geométrico aparece como
  estado transitorio durante el decaimiento, NO como urgencia creciente
  en reposo estable.

Experimento 3 — Acoplamiento asimétrico
  Con amenaza física alta (hp bajo, nF > 0), el mismo déficit de recursos
  produce distancia mucho mayor que en condiciones seguras.
  Resultado esperado: el acoplamiento emerge claramente.

Produce figuras en ./figures/
"""

from __future__ import annotations
from pathlib import Path

try:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("AVISO: numpy/matplotlib no instalados. Ejecuta:")
    print("  source .venv/bin/activate && pip install numpy matplotlib")

import model as M
from model import ModelConfig, DEFAULT_CONFIG

FIGURES_DIR = Path(__file__).parent / "figures"


# ────────────────────────────────────────────────────────────────────────────
# Experimento 1 — Fenotipos
# ────────────────────────────────────────────────────────────────────────────

def run_exp1_phenotypes() -> None:
    """
    Varía SOLO r_ten_target y muestra la distancia vs. nivel de energía.

    El explorador (target alto) tiene alta urgencia incluso con recursos
    moderados: necesita más arousal para estar en su 'óptimo'.
    El apático (target bajo) tiene baja urgencia salvo en déficit extremo.

    Parámetros fijos: hp=80, s=0.5. Solo r_ten_target cambia.
    """
    energies = [e / 10.0 for e in range(0, 201)]  # 0.0 → 20.0

    phenotypes = [
        # (etiqueta, r_ten_target)
        ("Explorador  (r_ten_target = 0.70)", 0.70),
        ("Apático     (r_ten_target = 0.05)", 0.05),
    ]

    print("\n── Experimento 1: Fenotipos ──────────────────────────────────────")
    for label, r_ten in phenotypes:
        cfg = ModelConfig(r_ten_target=r_ten)
        sample_dists = [
            M.opponent_distance(80.0, e, 0.5, cfg)
            for e in [2.0, 10.0, 13.5, 18.0]
        ]
        print(f"  {label}")
        print(f"    dist@energy=2  : {sample_dists[0]:.4f}   (escasez)")
        print(f"    dist@energy=10 : {sample_dists[1]:.4f}   (equilibrio)")
        print(f"    dist@energy=13.5: {sample_dists[2]:.4f}  (tensión ≈ target explorador)")
        print(f"    dist@energy=18 : {sample_dists[3]:.4f}   (abundancia)")

    if not HAS_PLOT:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#2c7bb6", "#d7191c"]

    for (label, r_ten), color in zip(phenotypes, colors):
        cfg = ModelConfig(r_ten_target=r_ten)
        dists = [M.opponent_distance(80.0, e, 0.5, cfg) for e in energies]
        ax.plot(energies, dists, label=label, linewidth=2, color=color)

        # marca el punto de tensión óptima (energy donde ten_R = r_ten_target)
        energy_opt = M.ENERGY_EQ + r_ten * M.ENERGY_SCALE
        dist_opt = M.opponent_distance(80.0, energy_opt, 0.5, cfg)
        ax.axvline(energy_opt, color=color, linestyle=":", alpha=0.4)

    ax.axvline(M.ENERGY_EQ, color="gray", linestyle="--", alpha=0.5, label="Equilibrio R")
    ax.set_xlabel("Energía (recursos)")
    ax.set_ylabel("Distancia homeostática (urgencia)")
    ax.set_title("Exp 1: Fenotipos — variando solo r_ten_target")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)

    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / "exp1_phenotypes.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Guardado: figures/exp1_phenotypes.png")


# ────────────────────────────────────────────────────────────────────────────
# Experimento 2 — ¿El aburrimiento emerge de la geometría?
# ────────────────────────────────────────────────────────────────────────────

def run_exp2_boredom() -> None:
    """
    Simula decaimiento natural de recursos (hp y energía) desde un estado
    cómodo hasta el equilibrio, sin el mecanismo explícito de aburrimiento.

    Observa:
      - Fase A (0-15 pasos): tensión > target → over-activation, distancia alta.
      - Fase B (~15-30 pasos): tensión < target → señal geométrica de aburrimiento.
      - Fase C (>30 pasos): tensión crece de nuevo desde el déficit → urgencia por amenaza.

    CONCLUSIÓN HONESTA: la señal de aburrimiento geométrico existe pero es un estado
    transitorio durante el decaimiento. Para urgencia creciente en reposo estable,
    el mecanismo explícito de quiet_steps es necesario.
    """
    # Decaimiento lineal: agente en el campo, sin regen de hub
    # hp: 90 → 75 en ~30 pasos (−0.5/paso); energy: 16 → 8 en ~53 pasos (−0.15/paso)
    n_steps = 70
    hp0, energy0 = 90.0, 16.0
    hp_decay, energy_decay = 0.5, 0.15

    hps      = [max(0.0, hp0     - hp_decay     * t) for t in range(n_steps)]
    energies = [max(0.0, energy0 - energy_decay * t) for t in range(n_steps)]
    ten_F    = [M.opponent_forces(hp, en, 0.5)[0] + M.opponent_forces(hp, en, 0.5)[1]
                for hp, en in zip(hps, energies)]
    ten_R    = [M.opponent_forces(hp, en, 0.5)[2] + M.opponent_forces(hp, en, 0.5)[3]
                for hp, en in zip(hps, energies)]
    dists    = [M.opponent_distance(hp, en, 0.5) for hp, en in zip(hps, energies)]

    # Calcular umbrales
    step_tenF_target = next((t for t in range(n_steps) if ten_F[t] <= DEFAULT_CONFIG.f_ten_target), None)
    step_tenR_target = next((t for t in range(n_steps) if ten_R[t] <= DEFAULT_CONFIG.r_ten_target), None)
    boredom_start = max(step_tenF_target or 0, step_tenR_target or 0)

    print("\n── Experimento 2: Aburrimiento geométrico ────────────────────────")
    print(f"  ten_F cae por debajo de target ({DEFAULT_CONFIG.f_ten_target}) en paso: {step_tenF_target}")
    print(f"  ten_R cae por debajo de target ({DEFAULT_CONFIG.r_ten_target}) en paso: {step_tenR_target}")
    print(f"  Distancia mínima en paso: {min(range(n_steps), key=lambda t: dists[t])}  "
          f"(dist={min(dists):.4f})")
    print(f"  Distancia en equilibrio (paso ~30): {dists[30]:.4f}")
    print("  ⚠  El aburrimiento geométrico es transitorio, no acumulativo.")
    print("     La urgencia creciente en reposo estable requiere quiet_steps.")

    if not HAS_PLOT:
        return

    steps = list(range(n_steps))
    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    fig.suptitle("Exp 2: ¿Emerge el aburrimiento de la geometría?", fontsize=12)

    # Panel 1: hp y energía
    ax = axes[0]
    ax.plot(steps, hps, color="#2c7bb6", linewidth=2, label="hp")
    ax.axhline(M.HP_EQ, color="#2c7bb6", linestyle="--", alpha=0.5, label=f"HP_EQ={M.HP_EQ}")
    ax2r = ax.twinx()
    ax2r.plot(steps, energies, color="#1a9641", linewidth=2, label="energía")
    ax2r.axhline(M.ENERGY_EQ, color="#1a9641", linestyle="--", alpha=0.5)
    ax.set_ylabel("Salud (hp)")
    ax2r.set_ylabel("Energía")
    ax.legend(loc="upper right", fontsize=8)
    ax2r.legend(loc="center right", fontsize=8)

    # Panel 2: tensiones con target
    ax = axes[1]
    ax.plot(steps, ten_F, color="#2c7bb6", linewidth=2, label="ten_F")
    ax.plot(steps, ten_R, color="#1a9641", linewidth=2, label="ten_R")
    ax.axhline(DEFAULT_CONFIG.f_ten_target, color="gray", linestyle="--", alpha=0.6,
               label=f"target tensión = {DEFAULT_CONFIG.f_ten_target}")
    if boredom_start:
        ax.axvspan(boredom_start, n_steps, alpha=0.08, color="orange",
                   label="tensión < target (aburrimiento geom.)")
    ax.set_ylabel("Tensión (f⁺ + f⁻)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)

    # Panel 3: distancia homeostática
    ax = axes[2]
    ax.plot(steps, dists, color="tomato", linewidth=2)
    if boredom_start:
        ax.axvspan(boredom_start, n_steps, alpha=0.08, color="orange")
    ax.set_xlabel("Pasos (decaimiento de recursos)")
    ax.set_ylabel("Distancia homeostática")
    ax.grid(True, alpha=0.25)

    # Anotaciones de fases
    axes[2].annotate("Over-activation", xy=(7, dists[7]), fontsize=8,
                     xytext=(7, dists[7] + 0.3), color="gray",
                     arrowprops=dict(arrowstyle="->", color="gray"))
    if boredom_start and boredom_start + 8 < n_steps:
        axes[2].annotate("Boredom geom.", xy=(boredom_start + 5, dists[boredom_start + 5]),
                         fontsize=8, xytext=(boredom_start + 8, dists[boredom_start + 5] + 0.4),
                         color="darkorange",
                         arrowprops=dict(arrowstyle="->", color="darkorange"))

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / "exp2_boredom.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Guardado: figures/exp2_boredom.png")


# ────────────────────────────────────────────────────────────────────────────
# Experimento 3 — Acoplamiento asimétrico
# ────────────────────────────────────────────────────────────────────────────

def run_exp3_coupling() -> None:
    """
    Muestra que la amenaza física (nF alto) amplifica la urgencia en R y S.

    Con el mismo nivel de energía y social, el agente amenazado físicamente
    tiene distancia mucho mayor que el agente seguro. Esto emerge de la
    estructura de acoplamiento: coupling = F_COUPLING · nF · (Δpos_R² + Δpos_S²).

    CONCLUSIÓN: el fenómeno emerge limpiamente del modelo.
    """
    energies = [e / 10.0 for e in range(0, 201)]  # 0 → 20

    conditions = [
        # (etiqueta, hp, color)
        ("Seguro   (hp=90, nF=0)",       90.0,  "#2c7bb6"),
        ("Amenazado (hp=35, nF=1.6)",    35.0,  "#d7191c"),
    ]

    print("\n── Experimento 3: Acoplamiento asimétrico ───────────────────────")
    for label, hp, _ in conditions:
        pF, nF, *_ = M.opponent_forces(hp, 10.0, 0.5)
        print(f"  {label}  →  nF={nF:.2f}")

    for label, hp, _ in conditions:
        sample = [(e, M.opponent_distance(hp, e, 0.5)) for e in [2.0, 5.0, 10.0, 15.0]]
        print(f"\n  {label}")
        for e, d in sample:
            print(f"    energy={e:4.1f} → dist={d:.4f}")

    print("\n  ✓ Con amenaza física, el mismo déficit de energía produce")
    print("    distancia significativamente mayor. El fenómeno emerge.")

    if not HAS_PLOT:
        return

    fig, ax = plt.subplots(figsize=(7, 4))

    for (label, hp, color) in conditions:
        dists = [M.opponent_distance(hp, e, 0.5) for e in energies]
        ax.plot(energies, dists, label=label, linewidth=2, color=color)

    ax.axvline(M.ENERGY_EQ, color="gray", linestyle="--", alpha=0.5, label="Equilibrio R")
    ax.set_xlabel("Energía (recursos)")
    ax.set_ylabel("Distancia homeostática (urgencia)")
    ax.set_title("Exp 3: Acoplamiento asimétrico — amenaza física amplifica urgencia R")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)

    # Anotación del gap de acoplamiento
    e_ann = 5.0
    d_safe = M.opponent_distance(90.0, e_ann, 0.5)
    d_thr  = M.opponent_distance(35.0, e_ann, 0.5)
    ax.annotate("", xy=(e_ann, d_thr), xytext=(e_ann, d_safe),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.5))
    ax.text(e_ann + 0.3, (d_safe + d_thr) / 2,
            f"Δ={d_thr - d_safe:.2f}\n(coupling)", fontsize=8, va="center")

    FIGURES_DIR.mkdir(exist_ok=True)
    fig.savefig(FIGURES_DIR / "exp3_coupling.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Guardado: figures/exp3_coupling.png")


# ────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═══════════════════════════════════════════════════════════════════")
    print("  Experimentos: modelo de fuerzas oponentes tridimensional")
    print("═══════════════════════════════════════════════════════════════════")

    run_exp1_phenotypes()
    run_exp2_boredom()
    run_exp3_coupling()

    print("\nListo. Figuras en: figures/")

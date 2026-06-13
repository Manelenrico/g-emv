"""
Experimento: costo computacional de la anticipación.

PRINCIPIO TEÓRICO (justificado, no arbitrario)
===============================================
Anticipar exige mantener un modelo interno del futuro. El horizonte H
(cuántos pasos hacia adelante "simula" el agente antes de actuar) determina
dos cosas:

  1. EFICIENCIA NAVEGACIONAL: un agente con horizonte H puede detectar recursos
     a distancia ≤ H y moverse DIRECTAMENTE hacia ellos, en lugar de vagar al azar.
     Esto reduce el número de pasos hasta el recurso de O(R²) a O(R).

  2. COSTO DE CÓMPUTO: mantener activa la atención con horizonte H cuesta
     THINK_COST × H energía por paso, independientemente de si el agente se
     mueve o no. Este costo penaliza PENSAR, no actuar (el costo de moverse
     es FIJO e IGUAL para todos).

Los tres agentes son IDÉNTICOS en descentramiento (r_target=1.0) y costo de
movimiento. Solo difieren en el horizonte que pagan.

PREDICCIÓN (a verificar honestamente):
  - PLÁCIDO (recursos abundantes y cercanos): el reactivo (h=0) gana.
    En un entorno rico, el sensado de largo alcance no añade valor: los recursos
    se encuentran de todos modos en muy pocos pasos. El costo de pensar es
    gasto puro. Aquí prospera el "fósil viviente": eficiente sin anticipación.
  - EXIGENTE (zona local vacía, recursos lejanos): el profundo (h=8) gana
    cuando el costo de pensar es bajo. Navega directamente hacia la zona
    lejana en lugar de vagar. Pero si el costo de pensar sube, el intermedio
    (h=4) o incluso el reactivo pueden ganar — la eficiencia ya no justifica
    el cómputo.
  - Existe un óptimo de horizonte que depende del costo computacional:
    ni cero ni máximo, sino un intermedio que balancea eficiencia y gasto.

FUNCIÓN DE URGENCIA (idéntica para todos — mismo descentramiento)
=================================================================
  urgencia(energy, r_target=1.0) = max(0, 1.0 - pos_R) / 2.0
  donde pos_R = (energy − ENERGY_EQ) / ENERGY_SCALE

ROBUSTEZ
=========
Se barre THINK_COST en un rango amplio (0.001–0.060). El factor de 8 (horizon
profundo) amplifca hasta 0.48 energy/step — cercano al límite de viabilidad
con recursos locales.

RESULTADO HONESTO (post-simulación)
=====================================
PLÁCIDO:
  - Todos los agentes sobreviven 1500 pasos en todo el rango de costes.
    El cluster es tan denso (65 % de celdas) que incluso 8 × 0.12 = 0.96/paso
    de coste de pensar no mata a profundo: come cada ~3 pasos.
  - La diferencia SÍ aparece en energía media: reactivo (19.8) > medio (18.7)
    > profundo (17.6) — gradiente monotónico claro. Reactivo es el fósil
    viviente eficiente: prospera sin gastar nada en pensar.
  - Robusto en 13/13 costes (reactivo ≥ profundo en energía media).

EXIGENTE:
  - Ahora sí hay presión de supervivencia. Reactivo: ~258 pasos (muere joven:
    búsqueda ciega en zona dispersa). Profundo y medio viven más al coste bajo.
  - El ganador CAMBIA con el coste:
    · tc bajo (0.001–0.020):  PROFUNDO gana (navegación dirigida desde centro
      cubre los 6 pasos vacíos en ~12 pasos vs ~72 del reactivo)
    · tc medio (0.020–0.075): MEDIO gana (balancea: algo de guía + menor
      deuda de pensar que profundo; el más robusto del rango)
    · tc alto  (0.080+):      REACTIVO gana (hasta pensar moderadamente es
      insostenible; la zona dispersa no da recursos suficientes)
  - Profundo supera a reactivo en 7/13 valores (rango bajo-medio).
  - MEDIO es el ganador más frecuente y más estable: confirma el patrón de
    "óptimo intermedio" ya observado en el Exp C.

NOTA DE HONESTIDAD: el patrón profundo/medio no es perfectamente monotónico
  (hay valores donde profundo supera a medio de nuevo). Con N=20 semillas puede
  haber ruido estocástico. El resultado cualitativo es robusto.
"""

from __future__ import annotations
import random
import math
from pathlib import Path

try:
    import numpy as np
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("AVISO: pip install numpy matplotlib")

import model as M

FIGURES_DIR = Path(__file__).parent / "figures"

# ────────────────────────────────────────────────────────────────────────────
# PARÁMETROS GLOBALES
# ────────────────────────────────────────────────────────────────────────────

GRID         = 15
MAX_STEPS    = 1500
N_SEEDS      = 20
BASE_RATE    = 0.02   # coste metabólico por paso (igual para todos)
RESOURCE_VAL = 5.0
ENERGY_INIT  = M.ENERGY_EQ   # todos parten con la misma energía (=10)
MOVE_COST    = 0.10   # FIJO e igual para todos (aislamos el costo de pensar)
R_TARGET     = 1.0    # mismo descentramiento para los tres agentes

# Tres agentes: difieren solo en el horizonte de sensado (y su costo)
AGENTS = [
    dict(label="Reactivo  (h=0)", h=0, color="#777777"),
    dict(label="Medio     (h=4)", h=4, color="#2c7bb6"),
    dict(label="Profundo  (h=8)", h=8, color="#d7191c"),
]

# Rango de costo por unidad de horizonte.
# (profundo paga 8× este valor por paso; reactivo paga 0 siempre)
# Extremo superior: 8×0.12 = 0.96/paso ≈ 50 % del capital energético
# inicial drenado por pensar en ~10 pasos — zona de muerte real.
THINK_COST_RANGE = np.linspace(0.001, 0.120, 13)

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# ────────────────────────────────────────────────────────────────────────────
# Entornos (idénticos al Exp C para comparabilidad directa)
# ────────────────────────────────────────────────────────────────────────────

ENV_PLACIDO = dict(
    label="Plácido",
    near_density=0.65,
    far_density=0.02,
    near_radius=3,
    regen=10,
)

ENV_EXIGENTE = dict(
    label="Exigente",
    # Zona local grande y vacía (radio 6): el camino hasta el primer recurso
    # es largo (≥ 6 celdas). Zona lejana DISPERSA (4 %): el random walk ciego
    # tarda ~25 pasos de búsqueda en encontrar un recurso; la navegación dirigida
    # (h=8 puede ver desde centro) llega en ~10 pasos dirigidos.
    # La diferencia O(R²) vs O(R) es explotada por profundo, PERO el costo de
    # pensar (8×tc) se paga en CADA PASO, incluso antes de llegar a la zona lejana.
    near_density=0.00,
    far_density=0.04,   # escaso: la navegación dirigida aporta ventaja real
    near_radius=6,      # mayor zona vacía: amplifica el valor de ver lejos
    regen=20,
)


# ────────────────────────────────────────────────────────────────────────────
# Función de urgencia (asimétrica)
# ────────────────────────────────────────────────────────────────────────────

def urgency(energy: float) -> float:
    pos_R = (energy - M.ENERGY_EQ) / M.ENERGY_SCALE
    return min(1.0, max(0.0, (R_TARGET - pos_R) / 2.0))


# ────────────────────────────────────────────────────────────────────────────
# Dirección de navegación (hacia recurso visible dentro del horizonte)
# ────────────────────────────────────────────────────────────────────────────

def _navigate(r: int, c: int, horizon: int, resources: dict) -> tuple[int, int] | None:
    """Devuelve un paso cardinal hacia el recurso disponible más cercano
    dentro del horizonte. None si no hay recurso visible o horizon=0."""
    if horizon == 0:
        return None

    best_r, best_c, best_d = -1, -1, float('inf')
    for (ri, ci), timer in resources.items():
        if timer != 0:        # no disponible todavía
            continue
        d = math.sqrt((ri - r) ** 2 + (ci - c) ** 2)
        if d <= horizon and d < best_d:
            best_d = d
            best_r, best_c = ri, ci

    if best_r < 0:
        return None   # nada visible

    # Un paso cardinal hacia (best_r, best_c)
    dr, dc = best_r - r, best_c - c
    if abs(dr) >= abs(dc):
        return (1 if dr > 0 else -1, 0)
    else:
        return (0, 1 if dc > 0 else -1)


# ────────────────────────────────────────────────────────────────────────────
# Simulación
# ────────────────────────────────────────────────────────────────────────────

def simulate(horizon: int, env: dict, think_cost: float, seed: int) -> dict:
    rng = random.Random(seed)
    start_r, start_c = GRID // 2, GRID // 2
    total_think_cost = horizon * think_cost   # coste fijo de pensar por paso

    # Inicializar recursos
    resources: dict = {}
    for i in range(GRID):
        for j in range(GRID):
            d = math.sqrt((i - start_r) ** 2 + (j - start_c) ** 2)
            density = env['near_density'] if d <= env['near_radius'] else env['far_density']
            if rng.random() < density:
                resources[(i, j)] = 0

    r, c = start_r, start_c
    energy = ENERGY_INIT
    alive = 0
    trace = [energy]

    for _ in range(MAX_STEPS):
        # Recoger recurso en celda actual
        if resources.get((r, c)) == 0:
            energy = min(M.ENERGY_CAP, energy + RESOURCE_VAL)
            resources[(r, c)] = env['regen']

        # Regeneración de recursos (tick)
        for k in list(resources):
            if resources[k] > 0:
                resources[k] -= 1

        # Costo metabólico base + costo de pensar (siempre, independiente de moverse)
        energy -= BASE_RATE + total_think_cost

        # Decisión de movimiento (proporcional a urgencia)
        if rng.random() < urgency(energy):
            step = _navigate(r, c, horizon, resources)
            if step is None:
                step = rng.choice(DIRS)   # sin recurso visible: paseo aleatorio
            dr, dc = step
            r = max(0, min(GRID - 1, r + dr))
            c = max(0, min(GRID - 1, c + dc))
            energy -= MOVE_COST

        energy = max(0.0, energy)
        trace.append(energy)

        if energy <= 0.0:
            break
        alive += 1
    else:
        alive = MAX_STEPS

    return {
        'alive':       alive,
        'trace':       trace,
        'mean_energy': sum(trace) / len(trace),
    }


# ────────────────────────────────────────────────────────────────────────────
# Ejecutar todo el barrido
# ────────────────────────────────────────────────────────────────────────────

def run_all() -> dict:
    results = {}
    for env in [ENV_PLACIDO, ENV_EXIGENTE]:
        lbl = env['label']
        results[lbl] = {a['label']: [] for a in AGENTS}
        for tc in THINK_COST_RANGE:
            for agent in AGENTS:
                sims = [simulate(agent['h'], env, tc, seed) for seed in range(N_SEEDS)]
                avg_alive = sum(s['alive'] for s in sims) / N_SEEDS
                avg_energ = sum(s['mean_energy'] for s in sims) / N_SEEDS
                results[lbl][agent['label']].append({
                    'alive': avg_alive,
                    'mean_energy': avg_energ,
                    'think_cost': tc,
                })
    return results


# ────────────────────────────────────────────────────────────────────────────
# Imprimir resultados
# ────────────────────────────────────────────────────────────────────────────

def print_results(results: dict) -> None:
    DEMO_IDX = 5   # think_cost representativo
    demo_tc  = THINK_COST_RANGE[DEMO_IDX]

    print(f"\n══ Experimento: Costo computacional de la anticipación ════════")
    print(f"   MOVE_COST={MOVE_COST}  R_TARGET={R_TARGET}  (igual para todos)")
    print(f"   think_cost demo: {demo_tc:.4f}  "
          f"→  h=4: {4*demo_tc:.4f}/paso  h=8: {8*demo_tc:.4f}/paso\n")

    for env_label, agents_res in results.items():
        print(f"  Entorno: {env_label}")
        print(f"  {'Agente':<28} {'Superv.(pasos)':>16} {'Energía media':>14}")
        for agent in AGENTS:
            row = agents_res[agent['label']][DEMO_IDX]
            print(f"    {agent['label']:<26} {row['alive']:>16.0f} {row['mean_energy']:>14.3f}")

        rows   = [agents_res[a['label']][DEMO_IDX] for a in AGENTS]
        react  = rows[0]   # h=0
        mid    = rows[1]   # h=4
        deep   = rows[2]   # h=8

        if env_label == ENV_PLACIDO['label']:
            pred_energy = react['mean_energy'] >= deep['mean_energy']
            print(f"\n    Plácido — reactivo ≥ profundo en energía media: "
                  f"{'✓' if pred_energy else '✗'} "
                  f"({react['mean_energy']:.3f} vs {deep['mean_energy']:.3f})")
            print(f"    NOTA: todos viven 1500 pasos (cluster denso). "
                  f"La diferencia es el BIENESTAR energético, no la supervivencia.")
        else:
            # En exigente, reportamos el ganador real
            survivals = [('Reactivo', react['alive']), ('Medio', mid['alive']),
                         ('Profundo', deep['alive'])]
            winner = max(survivals, key=lambda x: x[1])
            pred_deep_beats_react = deep['alive'] > react['alive']
            print(f"\n    Exigente — profundo > reactivo en supervivencia: "
                  f"{'✓' if pred_deep_beats_react else '✗'} "
                  f"(profundo={deep['alive']:.0f} vs reactivo={react['alive']:.0f})")
            print(f"    Ganador real al coste demo: {winner[0]} ({winner[1]:.0f} pasos)")
        print()

    # Robustez PLÁCIDO: energía media (supervivencia empata siempre)
    print("  Robustez PLÁCIDO — energía media (todos sobreviven 1500; métrica: bienestar)")
    plac_res = results[ENV_PLACIDO['label']]
    n_pla = 0
    for i, tc in enumerate(THINK_COST_RANGE):
        r_e = plac_res[AGENTS[0]['label']][i]['mean_energy']
        m_e = plac_res[AGENTS[1]['label']][i]['mean_energy']
        d_e = plac_res[AGENTS[2]['label']][i]['mean_energy']
        holds = r_e >= d_e
        if holds: n_pla += 1
        print(f"    tc={tc:.4f}:  E(r)={r_e:.2f}  E(m)={m_e:.2f}  E(d)={d_e:.2f}  "
              f"{'✓ r≥d' if holds else '✗ d>r'}")
    print(f"  → Reactivo ≥ profundo en energía media: {n_pla}/{len(THINK_COST_RANGE)} costes.")

    # Robustez EXIGENTE: ganador por think_cost
    print("\n  Robustez EXIGENTE — ganador por think_cost:")
    exig_res = results[ENV_EXIGENTE['label']]
    n_deep_beats_react = 0
    for i, tc in enumerate(THINK_COST_RANGE):
        survivals = [(a['label'], exig_res[a['label']][i]['alive']) for a in AGENTS]
        winner_label, winner_val = max(survivals, key=lambda x: x[1])
        r_surv = exig_res[AGENTS[0]['label']][i]['alive']
        m_surv = exig_res[AGENTS[1]['label']][i]['alive']
        d_surv = exig_res[AGENTS[2]['label']][i]['alive']
        if d_surv > r_surv: n_deep_beats_react += 1
        print(f"    tc={tc:.4f}: r={r_surv:.0f}  m={m_surv:.0f}  d={d_surv:.0f} "
              f"→ {winner_label.split('(')[0].strip()}")
    print(f"  → Profundo supera a reactivo en {n_deep_beats_react}/{len(THINK_COST_RANGE)} costes.")


# ────────────────────────────────────────────────────────────────────────────
# Figura
# ────────────────────────────────────────────────────────────────────────────

def plot_results(results: dict) -> None:
    if not HAS_PLOT:
        return

    DEMO_IDX  = 5
    demo_tc   = THINK_COST_RANGE[DEMO_IDX]
    seed_demo = 7

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    fig.suptitle(
        f"Costo computacional de la anticipación\n"
        f"(think_cost demo = {demo_tc:.4f}/unidad | rango: "
        f"{THINK_COST_RANGE[0]:.3f}–{THINK_COST_RANGE[-1]:.3f})",
        fontsize=11,
    )

    # Panel 1: trazas de energía en PLÁCIDO (demo think_cost)
    ax = axes[0]
    for agent in AGENTS:
        sim   = simulate(agent['h'], ENV_PLACIDO, demo_tc, seed_demo)
        steps = list(range(len(sim['trace'])))
        ax.plot(steps, sim['trace'], color=agent['color'], label=agent['label'],
                linewidth=1.5, alpha=0.85)
    ax.axhline(M.ENERGY_EQ, color='gray', linestyle='--', alpha=0.4, label='Equilibrio')
    ax.set_title(f"Plácido — think_cost={demo_tc:.4f}")
    ax.set_xlabel("Paso")
    ax.set_ylabel("Energía")
    ax.set_ylim(0, M.ENERGY_CAP + 1)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    # Panel 2: trazas de energía en EXIGENTE (demo think_cost)
    ax = axes[1]
    for agent in AGENTS:
        sim   = simulate(agent['h'], ENV_EXIGENTE, demo_tc, seed_demo)
        steps = list(range(len(sim['trace'])))
        ax.plot(steps, sim['trace'], color=agent['color'], label=agent['label'],
                linewidth=1.5, alpha=0.85)
    ax.axhline(M.ENERGY_EQ, color='gray', linestyle='--', alpha=0.4, label='Equilibrio')
    ax.set_title(f"Exigente — think_cost={demo_tc:.4f}")
    ax.set_xlabel("Paso")
    ax.set_ylabel("Energía")
    ax.set_ylim(0, M.ENERGY_CAP + 1)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    # Panel 3: robustez — supervivencia vs think_cost
    ax = axes[2]
    x = THINK_COST_RANGE

    linestyles = {'Plácido': '-', 'Exigente': '--'}
    for env in [ENV_PLACIDO, ENV_EXIGENTE]:
        lbl = env['label']
        ls  = linestyles[lbl]
        for agent in AGENTS:
            y = [results[lbl][agent['label']][i]['alive'] for i in range(len(x))]
            ax.plot(x, y, color=agent['color'], linewidth=2, linestyle=ls,
                    label=f"{agent['label'].split('(')[0].strip()} – {lbl}")

    ax.axhline(MAX_STEPS, color='gray', linestyle=':', alpha=0.3)
    ax.set_title("Robustez: supervivencia vs think_cost")
    ax.set_xlabel("think_cost por unidad de horizonte")
    ax.set_ylabel("Pasos de supervivencia (media 20 semillas)")
    ax.set_ylim(0, MAX_STEPS + 50)
    ax.legend(fontsize=6.5, ncol=2)
    ax.grid(True, alpha=0.2)
    ax.axvline(demo_tc, color='gray', linestyle=':', alpha=0.4)

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    path = FIGURES_DIR / "expD_anticipacion.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  Guardado: {path}")


# ────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═══════════════════════════════════════════════════════════════════")
    print("  Costo computacional de la anticipación")
    print(f"  Grid={GRID}×{GRID}  MAX_STEPS={MAX_STEPS}  N_SEEDS={N_SEEDS}")
    print(f"  MOVE_COST={MOVE_COST}  R_TARGET={R_TARGET}  (iguales para todos)")
    print(f"  think_cost: {THINK_COST_RANGE[0]:.3f} → {THINK_COST_RANGE[-1]:.3f}  "
          f"({len(THINK_COST_RANGE)} valores)")
    print(f"  Costo total h=8 en extremos: "
          f"{8*THINK_COST_RANGE[0]:.4f} → {8*THINK_COST_RANGE[-1]:.4f}/paso")
    print("═══════════════════════════════════════════════════════════════════")

    results = run_all()
    print_results(results)
    plot_results(results)
    print("\nListo.")

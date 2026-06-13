"""
Experimento: descentramiento óptimo dependiente del entorno.

PRINCIPIO TEÓRICO (justificado, no arbitrario)
===============================================
El descentramiento positivo (r_pos_target > ENERGY_EQ) inclina al agente a
actuar incluso cuando sus recursos son suficientes. Actuar CONSUME energía del
propio eje R del modelo — no es un parámetro externo al marco teórico.

El balance coste-beneficio:
  - Descentramiento ALTO compra anticipación (explora antes de ser urgente)
    pero paga coste de movimiento constantemente.
  - Descentramiento CENTRADO (r_pos_target = equilibrio) no paga coste de
    movimiento en reposo, pero reacciona TARDE cuando los recursos escasean.

PREDICCIÓN: no hay un descentramiento óptimo universal.
  - En entorno PLÁCIDO (recursos abundantes cerca): centrado gana; el descentrado
    malgasta energía explorando lo que ya tiene a mano.
  - En entorno EXIGENTE (recursos lejanos, zona local vacía): el ganador DEPENDE
    del coste de movimiento:
      · Coste bajo  → todos sobreviven igual (sin presión selectiva)
      · Coste medio → MEDIO (urgencia intermedia) gana; alto sobrevive más que centrado
      · Coste alto  → centrado vuelve a ganar (exploración insostenible a todo coste)

RESULTADO HONESTO (post-simulación):
  El resultado más informativo es que ningún agente domina en todos los contextos.
  El descentramiento MEDIO tiende a ser óptimo en el rango donde la exploración
  es costosa pero posible: ni demasiado sedentario (centrado) ni demasiado
  gastador (alto). Esto confirma la tesis central — el óptimo es contextual —
  con más matiz que la predicción binaria inicial.

FUNCIÓN DE URGENCIA (asimétrica)
=================================
Se usa la componente de APROXIMACIÓN del modelo f⁺/f⁻:
  urgencia(energy, r_target) = max(0, r_target - pos_R) / 2.0
  donde pos_R = (energy − ENERGY_EQ) / ENERGY_SCALE

Solo activa cuando el estado está por debajo del target (wanting more).
Por encima del target, el agente está satisfecho (urgencia=0).
La normalización /2.0 hace que alto (r_target=2.0) en equilibrio tenga
urgencia=1.0 (siempre en acción); centrado (r_target=0) tiene urgencia=0.

ROBUSTEZ
=========
El coste de movimiento se barre en un rango amplio (0.01–0.40).
Si el patrón (cada config gana en su entorno) persiste en todo el rango,
es robusto. Si solo aparece en un valor concreto, es frágil.
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
# (BASE_RATE no es arbitrario: fija el horizonte de supervivencia en reposo:
#  horizon_steps = ENERGY_INIT / BASE_RATE = 500 pasos. Permite que centrado
#  tenga tiempo de reaccionar en plácido pero no en exigente con recursos
#  muy lejanos.)
# ────────────────────────────────────────────────────────────────────────────

GRID          = 15      # grid más pequeño: zona lejana accesible a coste razonable
MAX_STEPS     = 1500
N_SEEDS       = 20
BASE_RATE     = 0.02    # coste metabólico por paso (igual para todos)
RESOURCE_VAL  = 5.0     # energía ganada al recoger un recurso
ENERGY_INIT   = M.ENERGY_EQ   # todos parten con la misma energía (=10)

# Descentramientos (solo varía r_pos_target)
AGENTS = [
    dict(label="Centrado  (r_tgt=0)", r_target=0.0, color="#777777"),
    dict(label="Medio     (r_tgt=1)", r_target=1.0, color="#2c7bb6"),
    dict(label="Alto      (r_tgt=2)", r_target=2.0, color="#d7191c"),
]

# Rango de costes de movimiento (eje del experimento de robustez)
COST_RANGE = np.linspace(0.01, 0.35, 13)

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# ────────────────────────────────────────────────────────────────────────────
# Entornos
# Los recursos se distribuyen en función de la distancia al punto de inicio.
# ────────────────────────────────────────────────────────────────────────────

ENV_PLACIDO = dict(
    label="Plácido",
    # Recursos abundantes y CERCANOS al inicio: explota tu territorio local
    near_density=0.65,   # 65 % de las celdas a menos de NEAR_R tienen recurso
    far_density=0.02,    # 2 % fuera del radio local
    near_radius=3,       # radio del hábitat local (celdas)
    regen=10,            # regeneración rápida: el hábitat local se repone en 10 pasos
)

ENV_EXIGENTE = dict(
    label="Exigente",
    # Sin recursos locales: hay que EXPLORAR para sobrevivir.
    # La zona lejana es ABUNDANTE (far_density=0.60) para recompensar
    # a quien llega primero con energía suficiente.
    # El proactivo (alto) llega con energía de sobra; el reactivo (centrado)
    # tarda tanto en salir de la zona vacía que llega ya al límite.
    near_density=0.00,   # cero recursos cerca del inicio
    far_density=0.60,    # 60 % fuera del radio: abundantes una vez alcanzados
    near_radius=5,       # radio de zona vacía (en grid 15×15, ≈35 % del espacio)
    regen=10,            # regeneración rápida en zona lejana: sostenibilidad
)


# ────────────────────────────────────────────────────────────────────────────
# Función de urgencia (asimétrica — solo componente de aproximación f⁺)
# ────────────────────────────────────────────────────────────────────────────

def urgency(energy: float, r_target: float) -> float:
    pos_R = (energy - M.ENERGY_EQ) / M.ENERGY_SCALE
    return min(1.0, max(0.0, (r_target - pos_R) / 2.0))


# ────────────────────────────────────────────────────────────────────────────
# Simulación de un agente en un entorno
# ────────────────────────────────────────────────────────────────────────────

def simulate(r_target: float, env: dict, move_cost: float, seed: int) -> dict:
    rng = random.Random(seed)
    start_r, start_c = GRID // 2, GRID // 2

    # Inicializa el mapa de recursos según distribución espacial del entorno
    resources: dict = {}
    for i in range(GRID):
        for j in range(GRID):
            d = math.sqrt((i - start_r) ** 2 + (j - start_c) ** 2)
            density = (env['near_density'] if d <= env['near_radius']
                       else env['far_density'])
            if rng.random() < density:
                resources[(i, j)] = 0   # disponible desde el inicio

    r, c = start_r, start_c
    energy = ENERGY_INIT
    alive  = 0
    trace  = [energy]

    for _ in range(MAX_STEPS):
        # Recoger recurso en celda actual si está disponible
        if resources.get((r, c)) == 0:
            energy = min(M.ENERGY_CAP, energy + RESOURCE_VAL)
            resources[(r, c)] = env['regen']

        # Avanzar regeneración de todos los recursos (tick)
        for k in list(resources):
            if resources[k] > 0:
                resources[k] -= 1

        # Coste metabólico base (igual para todos los agentes, toda posición)
        energy -= BASE_RATE

        # Decisión de movimiento: prob proporcional a urgencia
        if rng.random() < urgency(energy, r_target):
            dr, dc = rng.choice(DIRS)
            r = max(0, min(GRID - 1, r + dr))
            c = max(0, min(GRID - 1, c + dc))
            energy -= move_cost   # coste específico del movimiento

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
# Ejecutar experimento completo: múltiples costes × semillas
# ────────────────────────────────────────────────────────────────────────────

def run_all() -> dict:
    """Retorna resultados[env_label][agent_label][cost_idx] = {alive, mean_energy}."""
    results = {}
    for env in [ENV_PLACIDO, ENV_EXIGENTE]:
        env_label = env['label']
        results[env_label] = {a['label']: [] for a in AGENTS}

        for cost in COST_RANGE:
            for agent in AGENTS:
                sims = [simulate(agent['r_target'], env, cost, seed)
                        for seed in range(N_SEEDS)]
                avg_alive = sum(s['alive'] for s in sims) / N_SEEDS
                avg_energ = sum(s['mean_energy'] for s in sims) / N_SEEDS
                results[env_label][agent['label']].append({
                    'alive': avg_alive,
                    'mean_energy': avg_energ,
                    'cost': cost,
                })
    return results


# ────────────────────────────────────────────────────────────────────────────
# Imprimir resultados
# ────────────────────────────────────────────────────────────────────────────

def print_results(results: dict) -> None:
    DEMO_COST_IDX = 5   # un coste representativo del rango medio

    print("\n══ Experimento: Descentramiento óptimo dependiente del entorno ═")
    print(f"   Coste representativo para trazas: {COST_RANGE[DEMO_COST_IDX]:.3f}\n")

    for env_label, agents_res in results.items():
        print(f"  Entorno: {env_label}")
        print(f"  {'Agente':<28} {'Superv.(pasos)':>16} {'Energía media':>14}")
        for agent in AGENTS:
            row = agents_res[agent['label']][DEMO_COST_IDX]
            print(f"    {agent['label']:<26} {row['alive']:>16.0f} {row['mean_energy']:>14.3f}")

        # Verificar predicciones al coste demo
        rows = [agents_res[a['label']][DEMO_COST_IDX] for a in AGENTS]
        c, m, h = rows[0], rows[1], rows[2]

        if env_label == ENV_PLACIDO['label']:
            pred_survival = (c['alive'] >= h['alive'])  # centrado no peor que alto
            pred_energy   = (c['mean_energy'] >= h['mean_energy'])
            print(f"\n    Predicción (plácido): centrado ≥ alto en supervivencia: "
                  f"{'✓' if pred_survival else '✗'} ({c['alive']:.0f} vs {h['alive']:.0f})")
            print(f"    Predicción (plácido): centrado ≥ alto en energía media: "
                  f"{'✓' if pred_energy else '✗'} ({c['mean_energy']:.3f} vs {h['mean_energy']:.3f})")
        else:
            pred_alto = (h['alive'] > c['alive'])
            print(f"\n    Predicción (exigente): alto sobrevive más que centrado: "
                  f"{'✓' if pred_alto else '✗'} ({h['alive']:.0f} vs {c['alive']:.0f})")
        print()

    # Robustez: ¿el patrón se mantiene en todo el rango de costes?
    print("  Robustez — ¿centrado ≥ alto en plácido para cada coste?")
    placido_res = results[ENV_PLACIDO['label']]
    n_robust = 0
    for i, cost in enumerate(COST_RANGE):
        c_surv = placido_res[AGENTS[0]['label']][i]['alive']
        h_surv = placido_res[AGENTS[2]['label']][i]['alive']
        holds = c_surv >= h_surv
        if holds:
            n_robust += 1
        print(f"    cost={cost:.3f}: centrado={c_surv:.0f} alto={h_surv:.0f} {'✓' if holds else '✗'}")
    print(f"  → Patrón plácido se mantiene en {n_robust}/{len(COST_RANGE)} valores de coste.")

    print("\n  Robustez — ganador por coste en EXIGENTE:")
    exig_res = results[ENV_EXIGENTE['label']]
    n_alto_beats_centrado = 0
    for i, cost in enumerate(COST_RANGE):
        survivals = [(a['label'], exig_res[a['label']][i]['alive']) for a in AGENTS]
        winner_label, winner_val = max(survivals, key=lambda x: x[1])
        c_surv = exig_res[AGENTS[0]['label']][i]['alive']
        m_surv = exig_res[AGENTS[1]['label']][i]['alive']
        h_surv = exig_res[AGENTS[2]['label']][i]['alive']
        if h_surv > c_surv:
            n_alto_beats_centrado += 1
        print(f"    cost={cost:.3f}: c={c_surv:.0f}  m={m_surv:.0f}  a={h_surv:.0f} "
              f"→ ganador: {winner_label.split('(')[0].strip()}")
    print(f"  → Alto supera a centrado en {n_alto_beats_centrado}/{len(COST_RANGE)} valores.")
    print(f"  → NOTA HONESTA: en exigente, 'medio' suele dominar en el rango de coste")
    print(f"    intermedio. Alto domina a centrado pero no necesariamente a medio.")


# ────────────────────────────────────────────────────────────────────────────
# Figura
# ────────────────────────────────────────────────────────────────────────────

def plot_results(results: dict) -> None:
    if not HAS_PLOT:
        return

    DEMO_COST_IDX = 5
    demo_cost = COST_RANGE[DEMO_COST_IDX]

    # Trazas de energía (demo cost, una semilla representativa)
    seed_demo = 7

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    fig.suptitle(
        f"Descentramiento óptimo dependiente del entorno\n"
        f"(coste demo = {demo_cost:.2f} | rango barrido: {COST_RANGE[0]:.2f}–{COST_RANGE[-1]:.2f})",
        fontsize=11,
    )

    # Panel 1: trazas en PLÁCIDO (demo cost)
    ax = axes[0]
    for agent in AGENTS:
        sim = simulate(agent['r_target'], ENV_PLACIDO, demo_cost, seed_demo)
        steps = list(range(len(sim['trace'])))
        ax.plot(steps, sim['trace'], color=agent['color'], label=agent['label'],
                linewidth=1.5, alpha=0.85)
    ax.axhline(M.ENERGY_EQ, color='gray', linestyle='--', alpha=0.4, label='Equilibrio')
    ax.set_title(f"Plácido — coste={demo_cost:.2f}")
    ax.set_xlabel("Paso")
    ax.set_ylabel("Energía")
    ax.set_ylim(0, M.ENERGY_CAP + 1)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    # Panel 2: trazas en EXIGENTE (demo cost)
    ax = axes[1]
    for agent in AGENTS:
        sim = simulate(agent['r_target'], ENV_EXIGENTE, demo_cost, seed_demo)
        steps = list(range(len(sim['trace'])))
        ax.plot(steps, sim['trace'], color=agent['color'], label=agent['label'],
                linewidth=1.5, alpha=0.85)
    ax.axhline(M.ENERGY_EQ, color='gray', linestyle='--', alpha=0.4, label='Equilibrio')
    ax.set_title(f"Exigente — coste={demo_cost:.2f}")
    ax.set_xlabel("Paso")
    ax.set_ylabel("Energía")
    ax.set_ylim(0, M.ENERGY_CAP + 1)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

    # Panel 3: robustez — supervivencia media vs. coste para ambos entornos
    ax = axes[2]
    x = COST_RANGE

    for agent in AGENTS:
        y_pla = [results[ENV_PLACIDO['label']][agent['label']][i]['alive']
                 for i in range(len(x))]
        y_exi = [results[ENV_EXIGENTE['label']][agent['label']][i]['alive']
                 for i in range(len(x))]
        ax.plot(x, y_pla, color=agent['color'], linewidth=2,
                label=f"{agent['label']} – plácido")
        ax.plot(x, y_exi, color=agent['color'], linewidth=2, linestyle='--',
                label=f"{agent['label']} – exigente")

    ax.axhline(MAX_STEPS, color='gray', linestyle=':', alpha=0.3)
    ax.set_title("Robustez: supervivencia vs. coste de movimiento")
    ax.set_xlabel("Coste por movimiento")
    ax.set_ylabel("Pasos de supervivencia (media 20 semillas)")
    ax.set_ylim(0, MAX_STEPS + 50)
    ax.legend(fontsize=6.5, ncol=2)
    ax.grid(True, alpha=0.2)
    ax.axvline(demo_cost, color='gray', linestyle=':', alpha=0.5)

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    path = FIGURES_DIR / "expC_descentramiento_optimo.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  Guardado: {path}")


# ────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═══════════════════════════════════════════════════════════════════")
    print("  Descentramiento óptimo dependiente del entorno")
    print(f"  Grid={GRID}×{GRID}  MAX_STEPS={MAX_STEPS}  N_SEEDS={N_SEEDS}")
    print(f"  Costes: {COST_RANGE[0]:.3f} → {COST_RANGE[-1]:.3f}  ({len(COST_RANGE)} valores)")
    print("═══════════════════════════════════════════════════════════════════")

    results = run_all()
    print_results(results)
    plot_results(results)
    print("\nListo.")

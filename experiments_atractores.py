"""
Experimento: mapa de atractores del modelo G-EMV.

Genera N_INITIAL condiciones iniciales repartidas por todo el espacio de
estados (pos_a ∈ [-4.0, +4.0], ten_a ∈ [|pos_a|, 7.0] para cada eje),
deja evolucionar la dinámica sin estímulos externos durante N_STEPS pasos,
registra los estados finales y analiza si se agrupan (atractores discretos)
o se dispersan uniformemente.

IMPLEMENTACIÓN: completamente vectorizado con numpy; sin sklearn.
K-means manual para el análisis de agrupamiento.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

import model as M
from model import ModelConfig, DEFAULT_CONFIG

# ─── Parámetros del experimento ───────────────────────────────────────────────
N_INITIAL    = 3000     # número de condiciones iniciales
N_STEPS      = 400      # pasos de descenso de gradiente por trayectoria
ETA          = 0.05     # learning rate (igual que todos los experimentos)
SEED         = 42       # reproducibilidad

# Rango del muestreo en espacio (pos, ten)
POS_RANGE    = 4.0      # pos_a ∈ [-POS_RANGE, +POS_RANGE]
TEN_MAX      = 7.0      # ten_a ≤ TEN_MAX (< VOL_MAX=8 para estados físicamente válidos)

# K-means
K_VALUES     = [1, 2, 4, 6, 8, 12]  # valores de k a evaluar
KMEANS_ITER  = 200      # iteraciones Lloyd
KMEANS_RUNS  = 10       # reinicializaciones aleatorias para estabilidad

# Umbral para considerar un cluster "compacto" (σ < COMPACT_THR en cada dim)
COMPACT_THR  = 0.05

OUTFILE      = Path(__file__).parent / "attractor_data.json"
# ─────────────────────────────────────────────────────────────────────────────


# ─── Dinámica vectorizada ─────────────────────────────────────────────────────

def run_all(pF, nF, pR, nR, pS, nS, cfg: ModelConfig, n_steps: int):
    """
    Evoluciona N trayectorias en paralelo (vectorización numpy).
    Modifica las arrays in-place y devuelve (pos_F, pos_R, pos_S) finales.
    """
    TBM = M.TEN_BASAL_MIN     # 0.10
    VM  = M.VOL_MAX            # 8.0
    surplus_allowed = VM - 3.0 * TBM   # 7.70

    for _ in range(n_steps):
        pos_F = pF - nF;  pos_R = pR - nR;  pos_S = pS - nS
        ten_F = pF + nF;  ten_R = pR + nR;  ten_S = pS + nS

        dpos_F = pos_F - cfg.f_pos_target
        dpos_R = pos_R - cfg.r_pos_target
        dpos_S = pos_S - cfg.s_pos_target
        dten_F = ten_F - cfg.f_ten_target
        dten_R = ten_R - cfg.r_ten_target
        dten_S = ten_S - cfg.s_ten_target

        sqF = dpos_F**2;  sqR = dpos_R**2;  sqS = dpos_S**2

        C_F = cfg.sens_F * (sqR + sqS)
        C_R = cfg.sens_R * (sqF + sqS)
        C_S = cfg.sens_S * (sqF + sqR)

        W_F = cfg.sens_R * ten_R + cfg.sens_S * ten_S
        W_R = cfg.sens_F * ten_F + cfg.sens_S * ten_S
        W_S = cfg.sens_F * ten_F + cfg.sens_R * ten_R

        G_pF =  2*(cfg.w_f_pos + W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
        G_nF = -2*(cfg.w_f_pos + W_F)*dpos_F + 2*cfg.w_f_ten*dten_F + C_F
        G_pR =  2*(cfg.w_r_pos + W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
        G_nR = -2*(cfg.w_r_pos + W_R)*dpos_R + 2*cfg.w_r_ten*dten_R + C_R
        G_pS =  2*(cfg.w_s_pos + W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S
        G_nS = -2*(cfg.w_s_pos + W_S)*dpos_S + 2*cfg.w_s_ten*dten_S + C_S

        pF = np.maximum(0.0, pF - ETA * G_pF)
        nF = np.maximum(0.0, nF - ETA * G_nF)
        pR = np.maximum(0.0, pR - ETA * G_pR)
        nR = np.maximum(0.0, nR - ETA * G_nR)
        pS = np.maximum(0.0, pS - ETA * G_pS)
        nS = np.maximum(0.0, nS - ETA * G_nS)

        # ── Suelo TEN_BASAL_MIN (eje por eje) ─────────────────────────────
        for fp, fn in [(pF, nF), (pR, nR), (pS, nS)]:
            ten = fp + fn
            add = np.maximum(0.0, TBM - ten) * 0.5
            fp += add;  fn += add

        # ── Techo VOL_MAX (escala solo el excedente) ───────────────────────
        ten_F = pF + nF;  ten_R = pR + nR;  ten_S = pS + nS
        total = ten_F + ten_R + ten_S
        over  = total > VM

        if over.any():
            exc_F = np.maximum(0.0, ten_F - TBM)
            exc_R = np.maximum(0.0, ten_R - TBM)
            exc_S = np.maximum(0.0, ten_S - TBM)
            exc_t = exc_F + exc_R + exc_S
            safe  = np.where(exc_t > 0, exc_t, 1.0)
            sc    = np.where(over & (exc_t > 0), surplus_allowed / safe, 1.0)

            rF = np.where(over & (ten_F > 0), (TBM + exc_F*sc) / ten_F, 1.0)
            rR = np.where(over & (ten_R > 0), (TBM + exc_R*sc) / ten_R, 1.0)
            rS = np.where(over & (ten_S > 0), (TBM + exc_S*sc) / ten_S, 1.0)

            pF *= rF;  nF *= rF
            pR *= rR;  nR *= rR
            pS *= rS;  nS *= rS

    return pF - nF, pR - nR, pS - nS


# ─── Muestreo ─────────────────────────────────────────────────────────────────

def sample_initial(n: int, rng: np.random.Generator):
    """
    Muestrea n estados iniciales en (pos_a, ten_a) para cada eje y convierte
    a (f⁺, f⁻) con ten_a ≥ |pos_a| (garantiza f⁺, f⁻ ≥ 0).
    """
    forces = {}
    for axis in ('F', 'R', 'S'):
        pos = rng.uniform(-POS_RANGE, POS_RANGE, size=n)
        # ten_a uniforme en [|pos_a| + ε, TEN_MAX]
        min_ten = np.abs(pos) + 1e-4
        u       = rng.uniform(0.0, 1.0, size=n)
        ten     = min_ten + u * (TEN_MAX - min_ten)
        ten     = np.clip(ten, min_ten, TEN_MAX)
        forces[f'p{axis}'] = (ten + pos) / 2
        forces[f'n{axis}'] = (ten - pos) / 2

    return (forces['pF'], forces['nF'],
            forces['pR'], forces['nR'],
            forces['pS'], forces['nS'])


# ─── K-means manual ───────────────────────────────────────────────────────────

def kmeans(pts: np.ndarray, k: int, n_iter: int, rng: np.random.Generator):
    """Lloyd's k-means. Devuelve (labels, centers, wcss)."""
    n = len(pts)
    best_wcss, best_labels, best_centers = np.inf, None, None

    for _ in range(KMEANS_RUNS):
        # Inicialización k-means++
        idx = [rng.integers(0, n)]
        for _ in range(k - 1):
            dists = np.min(
                [np.sum((pts - pts[i])**2, axis=1) for i in idx],
                axis=0
            )
            probs = dists / dists.sum()
            idx.append(rng.choice(n, p=probs))
        centers = pts[idx].copy()

        labels = np.zeros(n, dtype=int)
        for _ in range(n_iter):
            dists  = np.array([np.sum((pts - c)**2, axis=1) for c in centers])
            new_lb = np.argmin(dists, axis=0)
            if np.all(new_lb == labels):
                break
            labels = new_lb
            for j in range(k):
                mask = labels == j
                if mask.any():
                    centers[j] = pts[mask].mean(axis=0)

        wcss = sum(
            np.sum((pts[labels == j] - centers[j])**2)
            for j in range(k) if (labels == j).any()
        )
        if wcss < best_wcss:
            best_wcss, best_labels, best_centers = wcss, labels.copy(), centers.copy()

    return best_labels, best_centers, best_wcss


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(SEED)
    cfg = DEFAULT_CONFIG

    print("══ EXPERIMENTO: MAPA DE ATRACTORES G-EMV ══════════════════════════")
    print(f"  N condiciones iniciales : {N_INITIAL}")
    print(f"  N pasos por trayectoria : {N_STEPS}")
    print(f"  η                       : {ETA}")
    print(f"  Muestreo                : pos_a ∈ [{-POS_RANGE:.1f}, +{POS_RANGE:.1f}], "
          f"ten_a ∈ [|pos_a|, {TEN_MAX:.1f}]")
    print()
    print("  Equilibrio teórico (sin acoplamiento, nX=0):")
    print("    pos_F* ≈ 0.800   pos_R* ≈ 1.514   pos_S* ≈ 0.629")
    print()

    # ── 1. Condiciones iniciales ──────────────────────────────────────────────
    print("  [1/4] Generando condiciones iniciales...", end=" ", flush=True)
    pF0, nF0, pR0, nR0, pS0, nS0 = sample_initial(N_INITIAL, rng)
    print(f"OK")
    print(f"    Rango inicial pos_F: [{(pF0-nF0).min():.2f}, {(pF0-nF0).max():.2f}]")
    print(f"    Rango inicial pos_R: [{(pR0-nR0).min():.2f}, {(pR0-nR0).max():.2f}]")
    print(f"    Rango inicial pos_S: [{(pS0-nS0).min():.2f}, {(pS0-nS0).max():.2f}]")
    print()

    # ── 2. Evolución ──────────────────────────────────────────────────────────
    print(f"  [2/4] Evolucionando {N_INITIAL} trayectorias × {N_STEPS} pasos (vectorizado)...",
          end=" ", flush=True)
    pF, nF, pR, nR, pS, nS = (pF0.copy(), nF0.copy(), pR0.copy(),
                                nR0.copy(), pS0.copy(), nS0.copy())
    fpos_F, fpos_R, fpos_S = run_all(pF, nF, pR, nR, pS, nS, cfg, N_STEPS)
    print("OK")

    pts = np.stack([fpos_F, fpos_R, fpos_S], axis=1)   # shape (N, 3)

    # ── 3. Estadísticas descriptivas ──────────────────────────────────────────
    print()
    print("  [3/4] Estadísticas de estados finales:")
    for i, ax in enumerate(('F (físico)', 'R (recursos)', 'S (social)')):
        col = pts[:, i]
        print(f"    pos_{ax[0]}: "
              f"min={col.min():.4f}  max={col.max():.4f}  "
              f"mean={col.mean():.4f}  std={col.std():.4f}  "
              f"median={np.median(col):.4f}")

    max_std = max(pts[:, i].std() for i in range(3))
    print()
    if max_std < COMPACT_THR:
        print(f"  → Dispersión máxima σ_max = {max_std:.5f} < {COMPACT_THR}")
        print("  → DIAGNÓSTICO PREVIO: los estados finales están EXTREMADAMENTE compactos.")
    else:
        print(f"  → Dispersión máxima σ_max = {max_std:.4f}")

    # ── 4. K-means con normalización interna ──────────────────────────────────
    print()
    print(f"  [4/4] K-means para k ∈ {K_VALUES} (Lloyd, {KMEANS_RUNS} reinicios)...")

    # Centrar y escalar para k-means (cada dim divide por su std)
    means = pts.mean(axis=0)
    stds  = pts.std(axis=0)
    stds  = np.where(stds > 1e-10, stds, 1.0)   # evita div/0 si todo coincide
    pts_sc = (pts - means) / stds

    wcss_list = []
    cluster_results = {}
    all_identical = max_std < 1e-9
    for k in K_VALUES:
        if all_identical:
            # Todos los puntos son idénticos: k-means degenerado, WCSS=0 trivialmente
            labels_k  = np.zeros(N_INITIAL, dtype=int)
            centers_k = pts[:1].copy()
            wcss_k    = 0.0
        else:
            labels_k, centers_k, wcss_k = kmeans(pts_sc, k, KMEANS_ITER, rng)
            centers_k = centers_k * stds + means
        wcss_list.append(wcss_k)
        cluster_results[k] = (labels_k, centers_k)
        print(f"    k={k:>2}:  WCSS = {wcss_k:>12.4f}")

    # Ratio de mejora al pasar de k a k+1 (caída brusca = elbow)
    print()
    if all_identical:
        print("  WCSS = 0 para todo k (todos los puntos son idénticos — elbow no aplica).")
    else:
        print("  Ratio de mejora WCSS (k+1)/k — elbow si cae abruptamente:")
        for i in range(1, len(K_VALUES)):
            if wcss_list[i-1] > 0:
                ratio = wcss_list[i] / wcss_list[i-1]
                print(f"    k={K_VALUES[i-1]}→{K_VALUES[i]}: ratio={ratio:.4f}  "
                      f"{'← posible elbow' if ratio < 0.5 else ''}")
            else:
                print(f"    k={K_VALUES[i-1]}→{K_VALUES[i]}: WCSS ya = 0")

    # ── 5. Informe de clusters para el k "natural" ────────────────────────────
    # Usar k=2 y k=4 como prueba de estructura adicional
    print()
    print("  ══ DETALLE DE CLUSTERS ═══════════════════════════════════════════")

    for k_show in [1, 2, 4]:
        if k_show not in cluster_results:
            continue
        labels_k, centers_k = cluster_results[k_show]
        print(f"\n  — k = {k_show} —")
        print(f"  {'ID':>3}  {'N':>6}  {'%':>5}  "
              f"{'ctr_pos_F':>10}  {'ctr_pos_R':>10}  {'ctr_pos_S':>10}  "
              f"{'σ_F':>7}  {'σ_R':>7}  {'σ_S':>7}")
        print("  " + "─"*76)
        for j in range(k_show):
            mask = labels_k == j
            sz   = mask.sum()
            if sz == 0:
                continue
            ctr = pts[mask].mean(axis=0)
            std = pts[mask].std(axis=0)
            print(f"  {j:>3}  {sz:>6}  {sz/N_INITIAL*100:>4.1f}%"
                  f"  {ctr[0]:>10.4f}  {ctr[1]:>10.4f}  {ctr[2]:>10.4f}"
                  f"  {std[0]:>7.5f}  {std[1]:>7.5f}  {std[2]:>7.5f}")

    # ── 6. Diagnóstico final ──────────────────────────────────────────────────
    print()
    print("  ══ DIAGNÓSTICO FINAL ════════════════════════════════════════════")

    # Punto de atracción global (definido siempre)
    global_center = pts.mean(axis=0)
    wcss_1 = wcss_list[0]
    wcss_2 = wcss_list[1]
    ratio_12 = (wcss_2 / wcss_1) if wcss_1 > 0 else 1.0

    if max_std < COMPACT_THR:
        print(f"\n  RESULTADO: ATRACTOR ÚNICO MUY COMPACTO.")
        print(f"  Todos los {N_INITIAL} estados finales convergen al mismo punto:")
        print(f"    pos_F* = {global_center[0]:.5f}")
        print(f"    pos_R* = {global_center[1]:.5f}")
        print(f"    pos_S* = {global_center[2]:.5f}")
        print(f"  Dispersión máx σ = {max_std:.2e}  (umbral = {COMPACT_THR})")
        print(f"  Esto confirma que G-EMV tiene UN único atractor global para")
        print(f"  la configuración por defecto: un equilibrio homeostático estable.")
        print(f"  La predicción de atractores discretos se cumple: hay exactamente 1.")
    elif ratio_12 > 0.9:
        print(f"\n  RESULTADO: DISTRIBUCIÓN ESENCIALMENTE UNIFORME O UN SOLO CLUSTER.")
        print(f"  La mejora de k=1 a k=2 es mínima (ratio WCSS={ratio_12:.3f}).")
        print(f"  Los estados finales se dispersan sin agrupamiento claro.")
        print(f"  Esto sería un resultado NEGATIVO: sin atractores discretos detectables.")
    else:
        print(f"\n  RESULTADO: MÚLTIPLES ATRACTORES DETECTADOS.")
        print(f"  La caída de WCSS k=1→k=2 es sustancial (ratio={ratio_12:.3f}).")
        print(f"  Centros de los atractores para k=2:")
        for j in range(2):
            c = centers_2[j]
            sz = (labels_2 == j).sum()
            print(f"    Atractor {j}: pos_F={c[0]:.4f}, pos_R={c[1]:.4f}, "
                  f"pos_S={c[2]:.4f}  (N={sz})")
        print(f"  Investigar si corresponden a orientaciones teóricas distintas.")

    # Compara con teórico
    print()
    print("  Comparación con equilibrio teórico (sin acoplamiento):")
    print(f"    Teórico: pos_F=0.8000, pos_R=1.5143, pos_S=0.6289")
    print(f"    Empírico: pos_F={global_center[0]:.4f}, pos_R={global_center[1]:.4f}, "
          f"pos_S={global_center[2]:.4f}")
    print(f"    Diferencia (efecto acoplamiento): "
          f"ΔF={global_center[0]-0.8000:+.4f}, "
          f"ΔR={global_center[1]-1.5143:+.4f}, "
          f"ΔS={global_center[2]-0.6289:+.4f}")

    # ── 7. Guarda datos para figura 3D ────────────────────────────────────────
    # Punto de atracción global (siempre bien definido)
    attractor = {"pos_F": float(fpos_F.mean()),
                 "pos_R": float(fpos_R.mean()),
                 "pos_S": float(fpos_S.mean())}

    output = {
        "experiment": "attractor_map_gemv",
        "n_initial": N_INITIAL,
        "n_steps": N_STEPS,
        "eta": ETA,
        "pos_range": POS_RANGE,
        "ten_max": TEN_MAX,
        "seed": SEED,
        "final_stats": {
            "pos_F": {"mean": float(fpos_F.mean()), "std": float(fpos_F.std()),
                      "min": float(fpos_F.min()), "max": float(fpos_F.max())},
            "pos_R": {"mean": float(fpos_R.mean()), "std": float(fpos_R.std()),
                      "min": float(fpos_R.min()), "max": float(fpos_R.max())},
            "pos_S": {"mean": float(fpos_S.mean()), "std": float(fpos_S.std()),
                      "min": float(fpos_S.min()), "max": float(fpos_S.max())},
        },
        "wcss_by_k": {str(K_VALUES[i]): float(wcss_list[i]) for i in range(len(K_VALUES))},
        "theoretical_equilibrium": {"pos_F": 0.8000, "pos_R": 1.5143, "pos_S": 0.6289},
        "attractor": attractor,
        "points": [
            {
                "pos_F": float(fpos_F[i]),
                "pos_R": float(fpos_R[i]),
                "pos_S": float(fpos_S[i]),
            }
            for i in range(N_INITIAL)
        ]
    }

    with open(OUTFILE, "w") as f:
        json.dump(output, f, separators=(',', ':'))
    print()
    print(f"  Datos guardados → {OUTFILE.name}")
    print(f"  ({N_INITIAL} puntos, campos: pos_F, pos_R, pos_S)")


if __name__ == "__main__":
    main()

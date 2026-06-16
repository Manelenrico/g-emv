"""
Experimento: firmas de activación ante problemas variados (G-EMV).

Genera 3000 perturbaciones (10% puras de referencia, 45% mezclas 2 ejes,
45% mezclas 3 ejes) con magnitudes aleatorias continuas. Para cada perturbación
captura la firma de activación = desviación media en (pos_F, pos_R, pos_S) durante
los primeros T_WINDOW pasos de recuperación. Normaliza a vector unitario y analiza
si las firmas se agrupan (repertorio limitado de orientaciones) o se distribuyen
uniformemente en la esfera 3D.

La pregunta: ¿el modelo "redondea" mezclas hacia unas pocas orientaciones básicas,
o genera respuestas proporcionalmente distribuidas entre los ejes?
"""

import json
from pathlib import Path
import numpy as np
import model as M
from model import DEFAULT_CONFIG

# ─── Parámetros ────────────────────────────────────────────────────────────────
N_TOTAL  = 3000
N_PURE   = 300       # 10% : 50 por cada uno de los 6 tipos puros {±F, ±R, ±S}
N_MIX2   = 1350      # 45% : mezclas de 2 ejes (cada uno ± aleatoriamente)
N_MIX3   = 1350      # 45% : mezclas de 3 ejes

T_WARM   = 500       # pasos para llegar al equilibrio antes de perturbar
T_WINDOW = 80        # ventana de captura: pasos post-perturbación

ETA      = 0.05
DELTA_MIN = 0.5      # magnitud mínima de cada componente de estímulo
DELTA_MAX = 3.5      # magnitud máxima

SEED     = 42

K_VALUES  = [1, 2, 4, 6, 8, 12]
KM_RUNS   = 20
KM_ITER   = 400

POLE_ANGLE_DEG = 30  # umbral en grados: "cerca de un polo puro"

OUTFILE = Path(__file__).parent / "attractor_signatures.json"
# ───────────────────────────────────────────────────────────────────────────────


# ─── Paso vectorizado ──────────────────────────────────────────────────────────

def step(pF, nF, pR, nR, pS, nS, cfg):
    """Un paso vectorizado de descenso de gradiente + constraints (arrays numpy)."""
    TBM = M.TEN_BASAL_MIN
    VM  = M.VOL_MAX

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

    # ── Suelo TEN_BASAL_MIN (eje por eje) ────────────────────────────────────
    add_F = np.maximum(0.0, TBM - (pF + nF)) * 0.5
    pF = pF + add_F;  nF = nF + add_F
    add_R = np.maximum(0.0, TBM - (pR + nR)) * 0.5
    pR = pR + add_R;  nR = nR + add_R
    add_S = np.maximum(0.0, TBM - (pS + nS)) * 0.5
    pS = pS + add_S;  nS = nS + add_S

    # ── Techo VOL_MAX (escala solo el excedente) ──────────────────────────────
    ten_F = pF + nF;  ten_R = pR + nR;  ten_S = pS + nS
    total = ten_F + ten_R + ten_S
    over  = total > VM
    if np.any(over):
        sur = VM - 3.0 * TBM
        exc_F = np.maximum(0.0, ten_F - TBM)
        exc_R = np.maximum(0.0, ten_R - TBM)
        exc_S = np.maximum(0.0, ten_S - TBM)
        exc_t = exc_F + exc_R + exc_S
        safe  = np.where(exc_t > 0, exc_t, 1.0)
        sc    = np.where(over & (exc_t > 0), sur / safe, 1.0)
        rF = np.where(over & (ten_F > 0), (TBM + exc_F*sc) / ten_F, 1.0)
        rR = np.where(over & (ten_R > 0), (TBM + exc_R*sc) / ten_R, 1.0)
        rS = np.where(over & (ten_S > 0), (TBM + exc_S*sc) / ten_S, 1.0)
        pF = pF * rF;  nF = nF * rF
        pR = pR * rR;  nR = nR * rR
        pS = pS * rS;  nS = nS * rS

    return pF, nF, pR, nR, pS, nS


# ─── Equilibrio ───────────────────────────────────────────────────────────────

def find_equilibrium(cfg):
    """Calcula el equilibrio numéricamente (un solo agente, T_WARM pasos)."""
    pF = np.array([0.87]); nF = np.array([0.05])
    pR = np.array([1.65]); nR = np.array([0.05])
    pS = np.array([0.73]); nS = np.array([0.05])
    for _ in range(T_WARM):
        pF, nF, pR, nR, pS, nS = step(pF, nF, pR, nR, pS, nS, cfg)
    return (float(pF[0]), float(nF[0]),
            float(pR[0]), float(nR[0]),
            float(pS[0]), float(nS[0]))


# ─── Generación de perturbaciones ─────────────────────────────────────────────
# Representación: v = (v_F, v_R, v_S) donde v_a > 0 → pA += v_a
#                                                v_a < 0 → nA += |v_a|
# Aplicación: pA += max(0, v_a); nA += max(0, -v_a)

def generate_perturbations(rng):
    """
    Genera N_TOTAL perturbaciones como vectores signed (v_F, v_R, v_S).
    Returns: array (N_TOTAL, 3) y array de tipos (N_TOTAL,) con strings.
    """
    vecs  = np.zeros((N_TOTAL, 3))
    ptypes = np.empty(N_TOTAL, dtype=object)

    # ── Puras: 50 × 6 tipos {+F, -F, +R, -R, +S, -S} ────────────────────────
    n_per = N_PURE // 6
    idx   = 0
    labels_pure = ['+F', '-F', '+R', '-R', '+S', '-S']
    for k, (ax, sign) in enumerate([(0,+1),(0,-1),(1,+1),(1,-1),(2,+1),(2,-1)]):
        deltas = rng.uniform(DELTA_MIN, DELTA_MAX, n_per)
        for d in deltas:
            vecs[idx, ax]  = sign * d
            ptypes[idx]    = labels_pure[k]
            idx += 1

    # ── Mezclas 2-ejes ────────────────────────────────────────────────────────
    axes_pairs = [(0,1), (0,2), (1,2)]
    for _ in range(N_MIX2):
        pair   = axes_pairs[rng.integers(0, 3)]
        signs  = rng.choice([-1, 1], size=2)
        deltas = rng.uniform(DELTA_MIN, DELTA_MAX, 2)
        vecs[idx, pair[0]] = signs[0] * deltas[0]
        vecs[idx, pair[1]] = signs[1] * deltas[1]
        ptypes[idx] = 'mix2'
        idx += 1

    # ── Mezclas 3-ejes ────────────────────────────────────────────────────────
    for _ in range(N_MIX3):
        signs  = rng.choice([-1, 1], size=3)
        deltas = rng.uniform(DELTA_MIN, DELTA_MAX, 3)
        vecs[idx] = signs * deltas
        ptypes[idx] = 'mix3'
        idx += 1

    # Mezcla aleatoria para evitar efectos de orden
    perm = rng.permutation(N_TOTAL)
    return vecs[perm], ptypes[perm]


# ─── Cálculo de firmas ────────────────────────────────────────────────────────

def compute_signatures(eq, vecs, cfg):
    """
    Aplica cada perturbación v sobre el equilibrio y registra la firma de
    activación = desviación media en (pos_F, pos_R, pos_S) durante T_WINDOW pasos.

    eq : (pF_eq, nF_eq, pR_eq, nR_eq, pS_eq, nS_eq)
    vecs : (N, 3) signed perturbation vectors
    Returns: (N, 3) array de firmas brutas (sin normalizar)
    """
    N = len(vecs)
    pF_eq, nF_eq, pR_eq, nR_eq, pS_eq, nS_eq = eq
    eq_pos_F = pF_eq - nF_eq
    eq_pos_R = pR_eq - nR_eq
    eq_pos_S = pS_eq - nS_eq

    # Aplica perturbaciones al equilibrio
    pF = np.full(N, pF_eq) + np.maximum(0.0,  vecs[:, 0])
    nF = np.full(N, nF_eq) + np.maximum(0.0, -vecs[:, 0])
    pR = np.full(N, pR_eq) + np.maximum(0.0,  vecs[:, 1])
    nR = np.full(N, nR_eq) + np.maximum(0.0, -vecs[:, 1])
    pS = np.full(N, pS_eq) + np.maximum(0.0,  vecs[:, 2])
    nS = np.full(N, nS_eq) + np.maximum(0.0, -vecs[:, 2])

    # Aplica post_init (constraints) al estado perturbado
    add_F = np.maximum(0.0, M.TEN_BASAL_MIN - (pF + nF)) * 0.5
    pF += add_F;  nF += add_F
    add_R = np.maximum(0.0, M.TEN_BASAL_MIN - (pR + nR)) * 0.5
    pR += add_R;  nR += add_R
    add_S = np.maximum(0.0, M.TEN_BASAL_MIN - (pS + nS)) * 0.5
    pS += add_S;  nS += add_S

    # Acumula desviaciones durante T_WINDOW pasos
    acc_F = np.zeros(N)
    acc_R = np.zeros(N)
    acc_S = np.zeros(N)

    for _ in range(T_WINDOW):
        pF, nF, pR, nR, pS, nS = step(pF, nF, pR, nR, pS, nS, cfg)
        acc_F += (pF - nF) - eq_pos_F
        acc_R += (pR - nR) - eq_pos_R
        acc_S += (pS - nS) - eq_pos_S

    sigs = np.stack([acc_F, acc_R, acc_S], axis=1) / T_WINDOW
    return sigs


# ─── K-means (Lloyd, k-means++) ───────────────────────────────────────────────

def kmeans(pts, k, rng):
    n = len(pts)
    best_wcss, best_labels, best_centers = np.inf, None, None

    for _ in range(KM_RUNS):
        # Inicialización k-means++
        idx_c = [int(rng.integers(0, n))]
        for _ in range(k - 1):
            dists = np.min(
                [np.sum((pts - pts[i])**2, axis=1) for i in idx_c], axis=0)
            total = dists.sum()
            if total == 0:
                idx_c.append(int(rng.integers(0, n)))
            else:
                idx_c.append(int(rng.choice(n, p=dists/total)))
        centers = pts[idx_c].copy().astype(float)

        labels = np.zeros(n, dtype=int)
        for _ in range(KM_ITER):
            dists2  = np.array([np.sum((pts - c)**2, axis=1) for c in centers])
            new_lb  = np.argmin(dists2, axis=0)
            if np.all(new_lb == labels):
                break
            labels  = new_lb
            for j in range(k):
                m = labels == j
                if m.any():
                    centers[j] = pts[m].mean(axis=0)

        wcss = sum(np.sum((pts[labels == j] - centers[j])**2)
                   for j in range(k) if (labels == j).any())
        if wcss < best_wcss:
            best_wcss, best_labels, best_centers = wcss, labels.copy(), centers.copy()

    return best_labels, best_centers, best_wcss


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(SEED)
    cfg = DEFAULT_CONFIG

    print("══ EXPERIMENTO: FIRMAS DE ACTIVACIÓN G-EMV ════════════════════════")
    print(f"  N total        : {N_TOTAL}  (puras={N_PURE} 10%, "
          f"mix2={N_MIX2} 45%, mix3={N_MIX3} 45%)")
    print(f"  T_WINDOW       : {T_WINDOW} pasos post-perturbación")
    print(f"  Δ magnitud     : [{DELTA_MIN:.1f}, {DELTA_MAX:.1f}] (uniforme por componente)")
    print()

    # ── 1. Equilibrio ─────────────────────────────────────────────────────────
    print("  [1/5] Calculando equilibrio...", end=" ", flush=True)
    eq = find_equilibrium(cfg)
    pF_eq, nF_eq, pR_eq, nR_eq, pS_eq, nS_eq = eq
    eq_pos = np.array([pF_eq - nF_eq, pR_eq - nR_eq, pS_eq - nS_eq])
    print(f"OK → pos_F={eq_pos[0]:.4f}, pos_R={eq_pos[1]:.4f}, pos_S={eq_pos[2]:.4f}")
    print()

    # ── 2. Perturbaciones ─────────────────────────────────────────────────────
    print("  [2/5] Generando perturbaciones...", end=" ", flush=True)
    vecs, ptypes = generate_perturbations(rng)
    print(f"OK  (mezclas: {(ptypes=='mix2').sum() + (ptypes=='mix3').sum()} / {N_TOTAL})")
    print()

    # ── 3. Firmas ─────────────────────────────────────────────────────────────
    print(f"  [3/5] Calculando {N_TOTAL} firmas × {T_WINDOW} pasos (vectorizado)...",
          end=" ", flush=True)
    sigs_raw = compute_signatures(eq, vecs, cfg)
    print("OK")

    # Normaliza a vector unitario
    norms = np.linalg.norm(sigs_raw, axis=1, keepdims=True)
    valid = (norms.ravel() > 1e-10)
    sigs  = sigs_raw[valid].copy()
    sigs /= np.linalg.norm(sigs, axis=1, keepdims=True)
    ptypes_v = ptypes[valid]
    N_valid   = len(sigs)
    print(f"    → {N_valid}/{N_TOTAL} firmas válidas (norma > 0) normalizadas a vector unitario")
    print()

    # ── 4. Estadísticas descriptivas ──────────────────────────────────────────
    print("  [4/5] Estadísticas de las firmas normalizadas:")
    for i, ax in enumerate(['F (físico)', 'R (recursos)', 'S (social)']):
        col = sigs[:, i]
        print(f"    sig_{ax[0]}: "
              f"mean={col.mean():+.4f}  std={col.std():.4f}  "
              f"min={col.min():+.4f}  max={col.max():+.4f}")

    # Análisis de dominancia: ¿qué eje domina cada firma?
    dom = np.argmax(np.abs(sigs), axis=1)
    dom_counts = {ax: int((dom == i).sum()) for i, ax in enumerate(['F','R','S'])}
    print()
    print("  Eje dominante (|sig_a| máxima):")
    for ax, cnt in dom_counts.items():
        frac = cnt / N_valid * 100
        bar  = "█" * int(frac/2)
        print(f"    {ax}: {cnt:>5} ({frac:>5.1f}%)  {bar}")

    # Null: si las firmas fueran uniformes en la esfera,
    # se esperaría 1/3 ≈ 33.3% por eje.
    print(f"  (Esperado bajo distribución uniforme: 33.3% por eje)")

    # Análisis de "polo puro": fracción de firmas dentro de POLE_ANGLE_DEG
    pole_thresh = np.cos(np.radians(POLE_ANGLE_DEG))  # cos(30°) = 0.866
    # Polos en orden: +F, +R, +S, -F, -R, -S
    poles      = np.vstack([np.eye(3), -np.eye(3)])
    pole_names_ordered = ['+F', '+R', '+S', '-F', '-R', '-S']
    near_pole = np.zeros(N_valid, dtype=bool)
    for p in poles:
        dot = sigs @ p   # coseno del ángulo con el polo (con signo)
        near_pole |= (dot >= pole_thresh)
    frac_pole = near_pole.mean()

    # Fracción nula esperada en esfera uniforme:
    # Área de 6 casquetes esféricos no solapados de semiángulo θ = 6 × (1-cosθ)/2
    frac_null = 6.0 * (1.0 - pole_thresh) / 2.0

    print()
    print(f"  Fracción de firmas dentro de {POLE_ANGLE_DEG}° de un polo puro: "
          f"{frac_pole*100:.1f}%")
    print(f"  (Nulo esférico: {frac_null*100:.1f}%  |  Clustering perfecto: ≈100%)")

    # Análisis separado: puras vs mezclas
    mask_pure = np.array([('mix' not in pt) for pt in ptypes_v])
    mask_mix  = ~mask_pure
    if mask_mix.any():
        frac_pole_mix  = near_pole[mask_mix].mean()
        frac_pole_pure = near_pole[mask_pure].mean() if mask_pure.any() else float('nan')
        print(f"    — Solo puras:   {frac_pole_pure*100:.1f}%  (esperado ≈100% si responde por ejes puros)")
        print(f"    — Solo mezclas: {frac_pole_mix*100:.1f}%  (clave vs nulo={frac_null*100:.1f}%: si alto → redondea)")
    print()

    # ── 5. K-means ────────────────────────────────────────────────────────────
    print(f"  [5/5] K-means sobre firmas normalizadas (k ∈ {K_VALUES})...")
    wcss_list = []
    cluster_results = {}
    for k in K_VALUES:
        lbl, ctr, wcss = kmeans(sigs, k, rng)
        wcss_list.append(wcss)
        cluster_results[k] = (lbl, ctr)
        print(f"    k={k:>2}:  WCSS = {wcss:>10.2f}  "
              f"(WCSS/N = {wcss/N_valid:.4f}  per-point)")

    print()
    print("  Ratio WCSS(k+1)/WCSS(k) — caída brusca indica elbow natural:")
    for i in range(1, len(K_VALUES)):
        if wcss_list[i-1] > 0:
            r = wcss_list[i] / wcss_list[i-1]
            flag = "  ← ELBOW" if r < 0.60 else ""
            print(f"    k={K_VALUES[i-1]}→{K_VALUES[i]}: {r:.4f}{flag}")

    # ── Detalle de clusters para k=2, 4, 6 ───────────────────────────────────
    print()
    print("  ══ DETALLE DE CLUSTERS ═══════════════════════════════════════════")
    for k_show in [2, 4, 6]:
        if k_show not in cluster_results:
            continue
        lbl_k, ctr_k = cluster_results[k_show]
        print(f"\n  — k = {k_show} —")
        print(f"  {'ID':>2}  {'N':>6}  {'%':>5}  "
              f"{'ctr_F':>8}  {'ctr_R':>8}  {'ctr_S':>8}  "
              f"{'σ_F':>6}  {'σ_R':>6}  {'σ_S':>6}  "
              f"{'pole?':>6}  angulo_ctr")
        print("  " + "─"*85)
        for j in range(k_show):
            mask = lbl_k == j
            if not mask.any():
                continue
            sz  = mask.sum()
            ctr = ctr_k[j]
            ctr_norm = ctr / (np.linalg.norm(ctr) + 1e-15)
            std = sigs[mask].std(axis=0)
            # Polo más cercano (con signo)
            dots_signed   = poles @ ctr_norm      # coseno con signo hacia cada polo
            best_pole_idx = np.argmax(dots_signed)
            angle_to_pole = np.degrees(np.arccos(min(1.0, dots_signed[best_pole_idx])))
            pole_near     = 'SÍ' if angle_to_pole < POLE_ANGLE_DEG else 'NO'
            # Fracción de mezclas en este cluster
            mix_in_cluster = mask_mix[mask].mean() * 100
            print(f"  {j:>2}  {sz:>6}  {sz/N_valid*100:>4.1f}%"
                  f"  {ctr_norm[0]:>8.3f}  {ctr_norm[1]:>8.3f}  {ctr_norm[2]:>8.3f}"
                  f"  {std[0]:>6.3f}  {std[1]:>6.3f}  {std[2]:>6.3f}"
                  f"  {pole_near:>6}  {angle_to_pole:.1f}° de {pole_names_ordered[best_pole_idx]}"
                  f"  (mezclas: {mix_in_cluster:.0f}%)")

    # ── Diagnóstico final ─────────────────────────────────────────────────────
    print()
    print("  ══ DIAGNÓSTICO FINAL ════════════════════════════════════════════")

    wcss_1 = wcss_list[0]
    wcss_6 = wcss_list[K_VALUES.index(6)] if 6 in K_VALUES else None
    ratio_1_to_6 = wcss_6 / wcss_1 if wcss_6 else None

    print()
    print(f"  Fracción de mezclas dentro de {POLE_ANGLE_DEG}° de un polo puro: "
          f"{frac_pole_mix*100:.1f}%  (nulo esférico: {frac_null*100:.1f}%  enrichment: "
          f"×{frac_pole_mix/frac_null:.2f})")
    print()

    if frac_pole_mix > 0.70:
        print("  RESULTADO: AGRUPAMIENTO FUERTE.")
        print(f"  El {frac_pole_mix*100:.0f}% de las mezclas termina orientado hacia un polo puro.")
        print("  El modelo SÍ 'redondea' respuestas mixtas hacia unas pocas orientaciones.")
    elif frac_pole_mix > 0.40:
        print("  RESULTADO: AGRUPAMIENTO MODERADO.")
        print(f"  El {frac_pole_mix*100:.0f}% de las mezclas está dentro de {POLE_ANGLE_DEG}° de un polo.")
        print("  Las mezclas se inclinan hacia orientaciones puras pero con transiciones amplias.")
    else:
        print("  RESULTADO: DISTRIBUCIÓN APROXIMADAMENTE UNIFORME.")
        print(f"  Solo el {frac_pole_mix*100:.0f}% de las mezclas está cerca de un polo puro.")
        print("  El modelo NO redondea las respuestas: la orientación de salida es proporcional")
        print("  a la mezcla de entrada. No emerge un repertorio limitado de orientaciones.")

    # Calidad del elbow
    ratios = [wcss_list[i]/wcss_list[i-1] for i in range(1, len(K_VALUES))
              if wcss_list[i-1] > 0]
    best_elbow = min(ratios) if ratios else 1.0
    print()
    print(f"  Mejor ratio WCSS (elbow): {best_elbow:.4f}  "
          f"({'estructura clara ≤0.60' if best_elbow <= 0.60 else 'sin estructura clara >0.60'})")

    if dom_counts['F']/N_valid > 0.50 or dom_counts['R']/N_valid > 0.50 or dom_counts['S']/N_valid > 0.50:
        dom_ax = max(dom_counts, key=dom_counts.get)
        print(f"  → El eje {dom_ax} domina {dom_counts[dom_ax]/N_valid*100:.0f}% de las respuestas "
              f"(posible asimetría de calibración).")

    # ── Guarda datos ──────────────────────────────────────────────────────────
    output = {
        "experiment": "activation_signatures_gemv",
        "n_total": N_TOTAL, "n_valid": N_valid,
        "t_window": T_WINDOW, "delta_range": [DELTA_MIN, DELTA_MAX],
        "equilibrium": {"pos_F": float(eq_pos[0]), "pos_R": float(eq_pos[1]),
                        "pos_S": float(eq_pos[2])},
        "dominance": dom_counts,
        "pole_fraction": {
            "all":   float(frac_pole),
            "pure":  float(frac_pole_pure) if mask_pure.any() else None,
            "mixed": float(frac_pole_mix),
        },
        "wcss_by_k": {str(K_VALUES[i]): float(wcss_list[i]) for i in range(len(K_VALUES))},
        "clusters_k6": [
            {
                "id": int(j),
                "size": int((cluster_results[6][0] == j).sum()),
                "center_normalized": cluster_results[6][1][j].tolist(),
            }
            for j in range(6)
            if (cluster_results[6][0] == j).any()
        ] if 6 in cluster_results else [],
        "signatures": [
            {"sig_F": float(sigs[i, 0]),
             "sig_R": float(sigs[i, 1]),
             "sig_S": float(sigs[i, 2]),
             "type":  str(ptypes_v[i])}
            for i in range(N_valid)
        ]
    }

    with open(OUTFILE, "w") as f:
        json.dump(output, f, separators=(',', ':'))
    print()
    print(f"  Datos guardados → {OUTFILE.name}  ({N_valid} puntos: sig_F, sig_R, sig_S, type)")


if __name__ == "__main__":
    main()

"""
Experimento: la tensión importa por sí misma — fuerzas independientes.

PREGUNTA
========
Dos agentes con posición idéntica (pos_a=0 en los tres ejes) pero con
tensión física distinta demuestran que la tensión es un grado de libertad
independiente que el modelo puede distinguir y que produce conducta diferente?

AGENTES
=======
  CALMA: pF=nF=1.0  →  pos_F=0, ten_F=2.0
  TENSO: pF=nF=3.8  →  pos_F=0, ten_F=7.6
  R, S idénticos en ambos: al mínimo basal (ten_R=ten_S=TEN_BASAL_MIN=0.10)

PREDICCIONES (a confirmar O refutar)
=====================================
  1. TENSO paga más coste en reposo (aunque d_pos sea idéntico).
  2. TENSO es más sensible a estímulos: pendiente de distancia mayor.
  3. TENSO contamina más los ejes R y S en reposo (coupling mayor por nF alto).

MÉTODO
======
  Fase 1: comparación estática en reposo — descomposición d_pos / d_ten / coupling.
  Fase 2: barrido de estímulo (N pasos de δ fuerza/paso), dos versiones:
    (a) Geométrico puro — sin State.__post_init__. Muestra la geometría limpia.
    (b) Constructor      — a través de State, con VOL_MAX y TEN_BASAL_MIN activos.
  La diferencia entre (a) y (b) es el efecto del techo de volumen.
"""

from __future__ import annotations
import math
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

import model as M
from model import State, DEFAULT_CONFIG

FIGURES_DIR = Path(__file__).parent / "figures"

# ────────────────────────────────────────────────────────────────────────────
# Estados iniciales
# ────────────────────────────────────────────────────────────────────────────

BASAL = M.TEN_BASAL_MIN / 2   # 0.05 — cada fuerza al mínimo basal del eje

INIT = {
    "CALMA": dict(pF=1.0, nF=1.0, pR=BASAL, nR=BASAL, pS=BASAL, nS=BASAL),
    "TENSO": dict(pF=3.8, nF=3.8, pR=BASAL, nR=BASAL, pS=BASAL, nS=BASAL),
}

CFG = DEFAULT_CONFIG

# ────────────────────────────────────────────────────────────────────────────
# Helper: descomposición de la distancia
# ────────────────────────────────────────────────────────────────────────────

def _decompose(pF, nF, pR, nR, pS, nS, cfg=CFG) -> dict:
    """Calcula d² descompuesto en d_pos, d_ten, coupling, más d_total."""
    pos_F = pF - nF;  ten_F = pF + nF
    pos_R = pR - nR;  ten_R = pR + nR
    pos_S = pS - nS;  ten_S = pS + nS
    d_pos = (
        cfg.w_f_pos * (pos_F - cfg.f_pos_target) ** 2 +
        cfg.w_r_pos * (pos_R - cfg.r_pos_target) ** 2 +
        cfg.w_s_pos * (pos_S - cfg.s_pos_target) ** 2
    )
    d_ten = (
        cfg.w_f_ten * (ten_F - cfg.f_ten_target) ** 2 +
        cfg.w_r_ten * (ten_R - cfg.r_ten_target) ** 2 +
        cfg.w_s_ten * (ten_S - cfg.s_ten_target) ** 2
    )
    dF_sq = (pos_F - cfg.f_pos_target) ** 2
    dR_sq = (pos_R - cfg.r_pos_target) ** 2
    dS_sq = (pos_S - cfg.s_pos_target) ** 2
    cpl = (
        cfg.sens_F * ten_F * (dR_sq + dS_sq) +
        cfg.sens_R * ten_R * (dF_sq + dS_sq) +
        cfg.sens_S * ten_S * (dF_sq + dR_sq)
    )
    d_sq = d_pos + d_ten + cpl
    return {
        "d_pos": d_pos, "d_ten": d_ten, "coupling": cpl,
        "d_sq": d_sq,
        "d_total": math.sqrt(max(0.0, d_sq)),
        "pos_F": pos_F, "ten_F": ten_F,
        "pF": pF, "nF": nF,
    }


# ────────────────────────────────────────────────────────────────────────────
# Fase 1 — Coste en reposo
# ────────────────────────────────────────────────────────────────────────────

def run_fase1() -> tuple[dict, dict]:
    print("\n═══ Fase 1: Coste en reposo ════════════════════════════════════════")
    print(f"  CALMA: pF=nF=1.0  →  ten_F=2.0, pos_F=0")
    print(f"  TENSO: pF=nF=3.8  →  ten_F=7.6, pos_F=0")
    print(f"  R, S: mínimo basal (ten_R=ten_S={M.TEN_BASAL_MIN:.2f}) en ambos\n")

    dc = _decompose(**INIT["CALMA"])
    dt = _decompose(**INIT["TENSO"])

    print(f"  {'':8}  {'d_pos':>9}  {'d_ten':>9}  {'coupling':>9}  {'d_total':>9}")
    for label, d in [("CALMA", dc), ("TENSO", dt)]:
        print(f"  {label:8}  {d['d_pos']:>9.4f}  {d['d_ten']:>9.4f}  "
              f"{d['coupling']:>9.4f}  {d['d_total']:>9.4f}")

    dpos_ok = abs(dc["d_pos"] - dt["d_pos"]) < 1e-9
    print(f"\n  Control — d_pos idéntico : {'✓' if dpos_ok else '✗ ERROR'}")
    print(f"  d_ten    TENSO/CALMA   : {dt['d_ten']   / max(dc['d_ten'],  1e-12):.2f}×")
    print(f"  coupling TENSO/CALMA   : {dt['coupling'] / max(dc['coupling'],1e-12):.2f}×")
    print(f"  d_total  TENSO/CALMA   : {dt['d_total'] / max(dc['d_total'], 1e-12):.2f}×")

    return dc, dt


# ────────────────────────────────────────────────────────────────────────────
# Fase 2 — Barrido de estímulo
# ────────────────────────────────────────────────────────────────────────────

N_STEPS = 25
DELTA   = 0.20   # fuerza añadida por paso de estímulo


def _sweep_geo(init: dict, stim: str) -> list[dict]:
    """Barrido geométrico puro: aplica el estímulo a las fuerzas brutas,
    sin pasar por State.__post_init__ (sin TEN_BASAL_MIN, sin VOL_MAX)."""
    rows = []
    pF0, nF0 = init["pF"], init["nF"]
    pR, nR, pS, nS = init["pR"], init["nR"], init["pS"], init["nS"]
    for k in range(N_STEPS + 1):
        pF_k = pF0 + k * DELTA if stim == "oportunidad" else pF0
        nF_k = nF0 + k * DELTA if stim == "amenaza"     else nF0
        d = _decompose(pF_k, nF_k, pR, nR, pS, nS)
        d["step"] = k
        d["vol_clipped"] = False
        rows.append(d)
    return rows


def _sweep_ctr(init: dict, stim: str) -> list[dict]:
    """Barrido a través del constructor State (TEN_BASAL_MIN y VOL_MAX activos).
    vol_clipped=True cuando __post_init__ modificó los valores pedidos."""
    rows = []
    pF0, nF0 = init["pF"], init["nF"]
    pR, nR, pS, nS = init["pR"], init["nR"], init["pS"], init["nS"]
    for k in range(N_STEPS + 1):
        pF_k = pF0 + k * DELTA if stim == "oportunidad" else pF0
        nF_k = nF0 + k * DELTA if stim == "amenaza"     else nF0
        st = State(pF=pF_k, nF=nF_k, pR=pR, nR=nR, pS=pS, nS=nS)
        d = _decompose(st.pF, st.nF, st.pR, st.nR, st.pS, st.nS)
        d["step"]        = k
        d["vol_clipped"] = abs(st.pF - pF_k) > 1e-9   # __post_init__ modificó pF
        d["total_int"]   = (pF_k + nF_k) + (pR + nR) + (pS + nS)
        d["total_real"]  = st.ten_F + st.ten_R + st.ten_S
        rows.append(d)
    return rows


def _slopes(rows: list[dict]) -> list[float]:
    return [(rows[k+1]["d_total"] - rows[k]["d_total"]) / DELTA
            for k in range(len(rows) - 1)]


def _print_sweep_summary(label: str, geo: list[dict], ctr: list[dict]) -> None:
    sg = _slopes(geo)
    sc = _slopes(ctr)
    n_clip = sum(1 for r in ctr if r["vol_clipped"])
    d0g, dNg = geo[0]["d_total"], geo[-1]["d_total"]
    d0c, dNc = ctr[0]["d_total"], ctr[-1]["d_total"]
    print(f"  {label}")
    print(f"    geo : d0={d0g:.4f}  dN={dNg:.4f}  Δd={dNg-d0g:+.4f}  "
          f"pendiente_0={sg[0]:+.4f}  pendiente_N={sg[-1]:+.4f}")
    print(f"    ctr : d0={d0c:.4f}  dN={dNc:.4f}  Δd={dNc-d0c:+.4f}  "
          f"pendiente_0={sc[0]:+.4f}  pendiente_N={sc[-1]:+.4f}  "
          f"pasos-techo={n_clip}/{N_STEPS}")


def _print_step_table(geo_c, geo_t, ctr_c, ctr_t) -> None:
    step5 = range(0, N_STEPS + 1, 5)
    print(f"\n  {'paso':>5}  {'Δf':>5}  "
          f"{'CALMA-geo':>11} {'TENSO-geo':>11}  "
          f"{'CALMA-ctr':>11} {'TENSO-ctr':>11}  {'⚡':>4}")
    for k in step5:
        df = k * DELTA
        clip = "T" if ctr_t[k]["vol_clipped"] else "-"
        print(f"  {k:>5}  +{df:>4.2f}  "
              f"{geo_c[k]['d_total']:>11.4f} {geo_t[k]['d_total']:>11.4f}  "
              f"{ctr_c[k]['d_total']:>11.4f} {ctr_t[k]['d_total']:>11.4f}  "
              f"{clip:>4}")


def run_fase2() -> dict:
    print(f"\n═══ Fase 2: Barrido de estímulo ════════════════════════════════════")
    print(f"  N={N_STEPS} pasos, δ={DELTA}/paso  "
          f"(rango total: 0 → {N_STEPS*DELTA:.1f} unidades de fuerza)")
    print(f"  (geo) = barrido geométrico puro, sin __post_init__")
    print(f"  (ctr) = a través del constructor, VOL_MAX={M.VOL_MAX:.1f} activo")

    all_rows: dict = {}

    for stim, stim_name in [("oportunidad", "OPORTUNIDAD (pF ↑)"),
                             ("amenaza",     "AMENAZA (nF ↑)")]:

        print(f"\n  ── {stim_name} ───────────────────────────────────────────")

        geo_c = _sweep_geo(INIT["CALMA"], stim)
        geo_t = _sweep_geo(INIT["TENSO"], stim)
        ctr_c = _sweep_ctr(INIT["CALMA"], stim)
        ctr_t = _sweep_ctr(INIT["TENSO"], stim)
        all_rows[(stim, "geo_c")] = geo_c
        all_rows[(stim, "geo_t")] = geo_t
        all_rows[(stim, "ctr_c")] = ctr_c
        all_rows[(stim, "ctr_t")] = ctr_t

        _print_sweep_summary("CALMA", geo_c, ctr_c)
        _print_sweep_summary("TENSO", geo_t, ctr_t)

        if stim == "amenaza":
            print(f"\n  Contagio cruzado (mutuo) durante AMENAZA (geométrico):")
            for lbl, rows in [("CALMA", geo_c), ("TENSO", geo_t)]:
                c0 = rows[0]["coupling"]
                cN = rows[-1]["coupling"]
                print(f"    {lbl}: reposo={c0:.4f}  →  "
                      f"final (nF+{N_STEPS*DELTA:.1f})={cN:.4f}  Δcoupling={cN-c0:+.4f}")

        _print_step_table(geo_c, geo_t, ctr_c, ctr_t)

    return all_rows


# ────────────────────────────────────────────────────────────────────────────
# Figuras
# ────────────────────────────────────────────────────────────────────────────

def plot_results(all_rows: dict) -> None:
    if not HAS_PLOT:
        return

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(
        "La tensión importa: CALMA (ten_F=2.0) vs TENSO (ten_F=7.6)\n"
        f"Posición idéntica (pos=0 en todos los ejes). R,S al basal. "
        f"δ={DELTA}/paso, {N_STEPS} pasos.",
        fontsize=11,
    )
    colors = {"CALMA": "#2c7bb6", "TENSO": "#d7191c"}

    for row_i, (stim, stim_name) in enumerate([
        ("oportunidad", "Oportunidad (pF ↑)"),
        ("amenaza",     "Amenaza (nF ↑)"),
    ]):
        geo_c = all_rows[(stim, "geo_c")]
        geo_t = all_rows[(stim, "geo_t")]
        ctr_c = all_rows[(stim, "ctr_c")]
        ctr_t = all_rows[(stim, "ctr_t")]
        x = [r["step"] * DELTA for r in geo_c]

        # Panel izquierdo: geométrico puro
        ax = axes[row_i][0]
        ax.plot(x, [r["d_total"] for r in geo_c],
                color=colors["CALMA"], lw=2.0, label="CALMA")
        ax.plot(x, [r["d_total"] for r in geo_t],
                color=colors["TENSO"], lw=2.0, label="TENSO")
        ax.axhline(geo_c[0]["d_total"], color=colors["CALMA"],
                   lw=0.8, ls="--", alpha=0.45, label="d₀ CALMA")
        ax.axhline(geo_t[0]["d_total"], color=colors["TENSO"],
                   lw=0.8, ls="--", alpha=0.45, label="d₀ TENSO")
        ax.set_title(f"{stim_name}  —  Geométrico puro (sin techo)")
        ax.set_xlabel("Fuerza añadida (k·δ)")
        ax.set_ylabel("Distancia homeostática")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.25)

        # Panel derecho: constructor (con techo)
        ax = axes[row_i][1]
        ax.plot(x, [r["d_total"] for r in ctr_c],
                color=colors["CALMA"], lw=2.0, label="CALMA (ctr)")
        ax.plot(x, [r["d_total"] for r in ctr_t],
                color=colors["TENSO"], lw=2.0, label="TENSO (ctr)")
        # Puntos donde VOL_MAX actúa sobre TENSO
        clip_x = [r["step"] * DELTA for r in ctr_t if r["vol_clipped"]]
        clip_y = [r["d_total"]       for r in ctr_t if r["vol_clipped"]]
        if clip_x:
            ax.scatter(clip_x, clip_y, color=colors["TENSO"],
                       marker="x", s=40, zorder=6, label="VOL_MAX activo")
            ax.axvline(clip_x[0], color="gray", lw=0.8, ls=":",
                       alpha=0.55, label=f"techo desde δ={clip_x[0]:.2f}")
        ax.axhline(ctr_c[0]["d_total"], color=colors["CALMA"],
                   lw=0.8, ls="--", alpha=0.45)
        ax.axhline(ctr_t[0]["d_total"], color=colors["TENSO"],
                   lw=0.8, ls="--", alpha=0.45)
        ax.set_title(f"{stim_name}  —  Constructor (VOL_MAX={M.VOL_MAX:.0f})")
        ax.set_xlabel("Fuerza pedida (k·δ) — real puede ser menor por techo")
        ax.set_ylabel("Distancia homeostática")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.25)

    fig.tight_layout()
    FIGURES_DIR.mkdir(exist_ok=True)
    path = FIGURES_DIR / "exp_tension.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  Figura guardada: {path}")


# ────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═══════════════════════════════════════════════════════════════════")
    print("  Experimento: la tensión importa — fuerzas independientes")
    print(f"  VOL_MAX={M.VOL_MAX:.1f}  TEN_BASAL_MIN={M.TEN_BASAL_MIN:.2f}")
    print("═══════════════════════════════════════════════════════════════════")

    run_fase1()
    all_rows = run_fase2()
    plot_results(all_rows)
    print("\nListo.")

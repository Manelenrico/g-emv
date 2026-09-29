"""[P5-6C · cierre] Las figuras F4 y F5 de la serie viva.

  python3 cantera/paper5/fig_P56C.py 1 2 3 4 5 amp1 ...

F4 · «aceptadas y curva real por brazo»: el embudo por brazo (propuestas ->
     evaluadas -> aceptadas) y, para cada forma aceptada y cada punto de
     control, la `d` PROYECTADA contra la `d` REAL, con la banda de 0,05 que
     define la medida principal.
F5 · «la confianza a lo largo de una vida»: C a lo largo de los tics, un trazo
     por asiento, leida de `forma_evaluada.C` (que el diario escribe en CADA
     evaluacion) y con los puntos de control encima.

Los diarios se leen DE UNO EN UNO y se tira todo menos lo que la figura usa:
los ciento veinte de la serie no caben juntos en memoria.
"""
import glob, json, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FIG = os.path.join(AQUI, "figF")
COL = {"A": "#0B3E49", "F": "#C4450B", "T": "#C9A227"}
NOM = {"A": "A · cuerpo solo", "F": "F · consejero", "T": "T · azar"}
BANDA = 0.05


def recoge(tandas):
    """{brazo: {...}} con lo minimo: embudo, puntos de control, trazos de C."""
    out = {b: {"prop": 0, "eval": 0, "acep": 0,
               "puntos": [], "C": []} for b in ("A", "F", "T")}
    for tanda in tandas:
        pat = os.path.join(RAIZ, "paintball", "runs", f"P56C_t{tanda}_*")
        for d in sorted(glob.glob(pat)):
            brazo = os.path.basename(d).split("_", 3)[2]
            for f in sorted(glob.glob(os.path.join(d, "*.art.log"))):
                o = out[brazo]
                traza = []
                for linea in open(f, encoding="utf-8"):
                    if '"forma_' not in linea:
                        continue
                    try:
                        r = json.loads(linea)
                    except Exception:
                        continue
                    k = r.get("k")
                    if k == "forma_propuesta":
                        o["prop"] += 1
                    elif k == "forma_evaluada":
                        o["eval"] += 1
                        if r.get("C") is not None:
                            traza.append((r["tick"], r["C"]))
                    elif k == "forma_aceptada":
                        o["acep"] += 1
                if traza:
                    o["C"].append(traza)
                # los puntos de control viven en `confianza`, no en `forma_*`
                for linea in open(f, encoding="utf-8"):
                    if '"k":"confianza"' not in linea:
                        continue
                    try:
                        r = json.loads(linea)
                    except Exception:
                        continue
                    if r.get("d_real") is None or r.get("d_proyectada") is None:
                        continue
                    o["puntos"].append((r["d_proyectada"], r["d_real"]))
    return out


def f4(D, tandas):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6))
    # (a) el embudo
    etapas = ["propuestas", "evaluadas", "aceptadas"]
    x = range(len(etapas))
    dy = {"A": (0, -14), "F": (0, -14), "T": (0, 9)}   # sin solapes
    for b in ("A", "F", "T"):
        v = [D[b]["prop"], D[b]["eval"], D[b]["acep"]]
        ax1.plot(x, v, "o-", color=COL[b], lw=2, ms=7, label=NOM[b])
        for i, n in enumerate(v):
            ax1.annotate(f"{n:,}".replace(",", "."), (i, max(n, 0.6)),
                         textcoords="offset points", xytext=dy[b],
                         ha="center", fontsize=8, color=COL[b],
                         fontweight="bold")
    ax1.set_yscale("symlog", linthresh=1)
    ax1.set_xticks(list(x)); ax1.set_xticklabels(etapas)
    ax1.set_ylabel("formas (escala log)")
    ax1.set_title("(a) el embudo, por brazo", fontsize=11, loc="left")
    ax1.legend(fontsize=8, frameon=False)
    ax1.grid(alpha=.25, ls=":")
    # (b) proyectada contra real
    todo = [v for b in ("F", "T") for v in D[b]["puntos"]]
    if todo:
        lo = min(min(p for p, _ in todo), min(r for _, r in todo))
        hi = max(max(p for p, _ in todo), max(r for _, r in todo))
        m = (hi - lo) * 0.05 or 0.1
        lo, hi = lo - m, hi + m
        ax2.plot([lo, hi], [lo, hi], color="#888", lw=1, zorder=1)
        ax2.fill_between([lo, hi], [lo, hi], [lo + BANDA, hi + BANDA],
                         color="#888", alpha=.18, zorder=0,
                         label=f"banda de {BANDA} (la medida)")
        for b in ("F", "T"):
            P = D[b]["puntos"]
            if not P:
                continue
            cum = sum(1 for p, r in P if r <= p + BANDA)
            ax2.scatter([p for p, _ in P], [r for _, r in P], s=34,
                        color=COL[b], alpha=.75, edgecolor="white", lw=.6,
                        zorder=3,
                        label=f"{b}: {cum}/{len(P)} = {cum / len(P) * 100:.1f} %")
        ax2.set_xlim(lo, hi); ax2.set_ylim(lo, hi)
        ax2.set_xlabel("d proyectada por la forma")
        ax2.set_ylabel("d real en ese punto de control")
        ax2.set_title("(b) lo prometido contra lo que pasó", fontsize=11,
                      loc="left")
        ax2.legend(fontsize=8, frameon=False, loc="upper left")
        ax2.grid(alpha=.25, ls=":")
    ax2.annotate("la banda de 0,05 es fina a esta escala: «cumple» ≈ «en la\n"
                 "línea o por debajo» · por debajo = mejor de lo prometido",
                 (0.98, 0.03), xycoords="axes fraction", ha="right",
                 fontsize=7.5, color="#555", style="italic")
    fig.suptitle("F4 · las aceptadas y su curva real, por brazo "
                 f"({', '.join(str(t) for t in tandas)})", fontsize=12)
    fig.tight_layout()
    p = os.path.join(FIG, "F4_aceptadas_curva.png")
    fig.savefig(p, dpi=160); plt.close(fig)
    return p


def f5(D, tandas):
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.2), sharey=True)
    for ax, b in zip(axs, ("F", "T")):
        trazas = sorted(D[b]["C"], key=len, reverse=True)
        for tr in trazas:
            ax.plot([t for t, _ in tr], [c for _, c in tr],
                    color=COL[b], lw=.8, alpha=.35)
        if trazas:
            ax.plot([t for t, _ in trazas[0]], [c for _, c in trazas[0]],
                    color=COL[b], lw=2.2, alpha=1,
                    label=f"el asiento con más evaluaciones ({len(trazas[0])})")
        ax.axhline(0.30, color="#444", lw=1, ls="--")
        ax.annotate("C₀ = 0,30", (0.01, 0.305), xycoords=("axes fraction",
                    "data"), fontsize=8, color="#444")
        ax.set_title(f"{NOM[b]} · {len(trazas)} asientos", fontsize=11,
                     loc="left")
        ax.set_xlabel("tic")
        ax.grid(alpha=.25, ls=":")
        if trazas:
            ax.legend(fontsize=8, frameon=False, loc="lower right")
    axs[0].set_ylabel("confianza C")
    fig.suptitle("F5 · la confianza a lo largo de una vida "
                 f"({', '.join(str(t) for t in tandas)})", fontsize=12)
    fig.tight_layout()
    p = os.path.join(FIG, "F5_confianza_vida.png")
    fig.savefig(p, dpi=160); plt.close(fig)
    return p


def main():
    tandas = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    os.makedirs(FIG, exist_ok=True)
    D = recoge(tandas)
    for b in ("A", "F", "T"):
        o = D[b]
        print(f"  {b}: propuestas {o['prop']:5d} · evaluadas {o['eval']:5d} "
              f"· aceptadas {o['acep']:3d} · puntos de control "
              f"{len(o['puntos']):3d} · trazos de C {len(o['C'])}")
    print("  " + f4(D, tandas))
    print("  " + f5(D, tandas))


if __name__ == "__main__":
    main()

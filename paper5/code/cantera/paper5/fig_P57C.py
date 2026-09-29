"""[P5-7C] Las dos figuras del cierre.

  F1 · la arena vista por brazo, asiento a asiento.
  F2 · una vida de Q: ignorancia global, amenaza graduada y los tics en que la
       curiosidad decidio — todo leido del diario, no reconstruido.
"""
import collections, glob, json, os, statistics as st, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4")); sys.path.insert(0, AQUI)
import serie_util as U
FIG = os.path.join(AQUI, "figI")
COL = {"A": "#0B3E49", "Q": "#C4450B"}


def f1(tandas):
    D = json.load(open(os.path.join(
        AQUI, f"P57C_t{'_'.join(tandas)}_medidas.json")))
    A = sorted(o["vista_final"] for o in D if o["brazo"] == "A")
    Q = sorted(o["vista_final"] for o in D if o["brazo"] == "Q")
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    for n, v in (("A", A), ("Q", Q)):
        ax.plot(range(1, len(v) + 1), v, "o-", color=COL[n], lw=1.6, ms=4.5,
                label=f"{n} · mediana {st.median(v):.4f}  (n={len(v)})")
        ax.axhline(st.median(v), color=COL[n], lw=.9, ls=":")
    ax.set_xlabel("asiento, ordenado por lo que vio")
    ax.set_ylabel("fraccion de la arena vista al acabar")
    ax.grid(alpha=.25, ls=":")
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    ax.set_title("F1 · la arena vista, por brazo — las cuarenta partidas",
                 fontsize=12, loc="left")
    ax.annotate(f"Q/A = {st.median(Q) / st.median(A):.3f}x  (Q1 pedia > 1,30x)",
                (0.98, 0.04), xycoords="axes fraction", ha="right",
                fontsize=9, style="italic", color="#444")
    fig.tight_layout()
    p = os.path.join(FIG, "F1_arena_vista.png")
    fig.savefig(p, dpi=160); plt.close(fig)
    return p


def f2(tandas):
    # la vida de Q con mas decisiones de curiosidad
    cand = []
    for t in tandas:
        for d in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                               f"P57C_t{t}_Q_*"))):
            for f in sorted(glob.glob(os.path.join(d, "*.art.log"))):
                n = 0
                with open(f, encoding="utf-8") as fh:
                    for ln in fh:
                        if '"decidio": true' in ln or '"decidio":true' in ln:
                            n += 1
                cand.append((n, f))
    # la vida con la MEDIANA de decisiones: la del maximo es ilegible (miles
    # de lineas tapan la figura) y ademas no es representativa.
    cand.sort()
    mejor_n, mejor = cand[len(cand) // 2]
    cur = [r for r in U.lee(mejor) if r.get("k") == "curiosidad_tic"]
    T = [r["tick"] for r in cur]
    IG = [r["ign_global"] for r in cur]
    AM = [r["amenaza"] for r in cur]
    DEC = [r["tick"] for r in cur if r.get("decidio")]
    V = 100
    SU = [st.median(AM[max(0, i - V):i + 1]) for i in range(len(AM))]
    fig, ax = plt.subplots(figsize=(12.5, 4.6))
    # las decisiones son MILES: dibujarlas como lineas tapa la figura entera.
    # Se dibuja su DENSIDAD (fraccion de tics con decision en ventanas de 100)
    # como una banda en la base, que si se lee.
    dset = set(DEC)
    paso = 100
    xs, ys = [], []
    for i in range(min(T), max(T) + 1, paso):
        ven = [t for t in T if i <= t < i + paso]
        if ven:
            xs.append(i + paso / 2)
            ys.append(sum(1 for t in ven if t in dset) / len(ven))
    ax.fill_between(xs, 0, [y * 0.28 for y in ys], color="#C9A227",
                    alpha=.55, zorder=1, step="mid")
    ax.plot(T, IG, color="#0B3E49", lw=2.0, label="ignorancia global", zorder=4)
    ax.plot(T, AM, color="#C4450B", lw=.5, alpha=.22, zorder=2)
    ax.plot(T, SU, color="#C4450B", lw=1.8, zorder=3,
            label="amenaza graduada (mediana movil 100; cruda en tenue)")
    ax.fill_between([], [], color="#C9A227", alpha=.55,
                    label=f"densidad de decisiones de la curiosidad "
                          f"({len(DEC)} de {len(T)} tics; la banda llena = "
                          f"el 28 % del eje)")
    ax.axhspan(0, 0.2, color="#2e7d32", alpha=.06)
    ax.axhspan(0.6, 1, color="#b71c1c", alpha=.06)
    ax.annotate("seguro", (0.995, 0.06), xycoords="axes fraction", ha="right",
                fontsize=8.5, color="#2e7d32", weight="bold")
    ax.annotate("inseguro", (0.995, 0.93), xycoords="axes fraction",
                ha="right", fontsize=8.5, color="#b71c1c", weight="bold")
    ax.set_xlabel("tic"); ax.set_ylabel("fraccion / amenaza [0-1]")
    ax.set_ylim(0, 1); ax.set_xlim(min(T), max(T))
    ax.grid(alpha=.2, ls=":")
    ax.legend(fontsize=8.5, frameon=False, loc="lower left", ncol=3)
    nom = os.path.basename(os.path.dirname(mejor))
    ax.set_title(f"F2 · una vida de Q — {nom} (todo LEIDO del diario)",
                 fontsize=12, loc="left")
    fig.tight_layout()
    p = os.path.join(FIG, "F2_una_vida_Q.png")
    fig.savefig(p, dpi=160); plt.close(fig)
    print(f"  vida elegida {nom} · {len(cur):,} tics · {len(DEC)} decisiones")
    return p


if __name__ == "__main__":
    tandas = sys.argv[1:] or ["1", "2", "3", "4"]
    os.makedirs(FIG, exist_ok=True)
    print("  " + f1(tandas))
    print("  " + f2(tandas))

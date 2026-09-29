"""[P5-3A · A6] W y vida reales, con la foto congelada y la proyeccion con
intencion superpuestas en diez tics de decision, elegidos con semilla fija."""
import glob, json, os, random, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                    # noqa: E402
import banco_llaves as B                                  # noqa: E402
import proyeccion as P                                    # noqa: E402

SEM, K, N = 20260920, 100, 10
ACENTO, TINTA, GRIS, REJILLA = "#C4450B", "#111111", "#6E6E6E", "#DDDDDD"
AZUL = "#0B3E49"


def una(f, titulo, salida):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
    vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
    serie = [(r["tick"], P.W_de(P.estado_de(r), mundo), r.get("hp"))
             for r in vivos]
    decs = []
    for r in vivos:
        R = r.get("RADIOGRAFIA") or {}
        el = R.get("elegido") or ""
        d = (R.get("candidatos") or {}).get(el)
        if el.startswith("ir_") and isinstance(d, dict) and d.get("pos_prevista") \
                and (r["tick"] + K) in tk:
            decs.append((r, tuple(d["pos_prevista"])))
    if not decs:
        return None
    rnd = random.Random(SEM)
    sel = sorted(rnd.sample(decs, min(N, len(decs))), key=lambda x: x[0]["tick"])
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["DejaVu Sans"], "font.size": 7.5,
                         "axes.edgecolor": GRIS, "text.color": TINTA,
                         "axes.labelcolor": TINTA, "xtick.color": GRIS,
                         "ytick.color": GRIS, "figure.facecolor": "white",
                         "axes.facecolor": "white", "savefig.facecolor": "white"})
    fig, ax = plt.subplots(2, 1, figsize=(6.69, 4.2), dpi=300, sharex=True,
                           gridspec_kw={"hspace": 0.34, "left": 0.09,
                                        "right": 0.985, "top": 0.80,
                                        "bottom": 0.105})
    ax[0].plot([x[0] for x in serie], [x[1] for x in serie], color=TINTA,
               lw=0.8, label="lo que llevó de verdad")
    ax[1].plot([x[0] for x in serie], [x[2] for x in serie], color=TINTA,
               lw=0.8, label="la vida que tuvo de verdad")
    for j, (r, dest) in enumerate(sel):
        t = r["tick"]
        e0 = P.estado_de(r)
        W0 = P.W_de(e0, mundo)
        suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
                 if it.get("pos")}
        fo = P.congelada(e0, mundo, K)
        pi = P.proyectar(e0, {"destino": dest, "coger": dest in suelo}, K,
                         mundo, suelo)
        for a, cf, cp in ((0, fo["W"], pi["W"]), (1, fo["hp"], pi["hp"])):
            ax[a].plot([t, t + K], [[W0, e0["hp"]][a], cf], color=GRIS,
                       lw=0.9, ls=(0, (3, 2)), zorder=3,
                       label="la foto de hoy (congela)" if j == 0 else None)
            ax[a].plot([t, t + K], [[W0, e0["hp"]][a], cp], color=ACENTO,
                       lw=1.0, zorder=4,
                       label="la proyección con intención" if j == 0 else None)
            ax[a].plot([t + K], [cf], "o", ms=2.6, color=GRIS, zorder=5)
            ax[a].plot([t + K], [cp], "o", ms=2.6, color=ACENTO, zorder=6)
    ax[0].set_ylabel("W (lo que lleva)")
    ax[1].set_ylabel("vida")
    ax[1].set_xlabel("instantes de partida (24 por segundo)")
    for a in ax:
        a.grid(axis="y", color=REJILLA, lw=0.4)
        a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
        a.legend(frameon=False, fontsize=6.8, ncol=3, loc="lower left",
                 bbox_to_anchor=(0.0, 1.005), borderaxespad=0.0)
    fig.suptitle(titulo, fontsize=10, x=0.012, ha="left", y=0.975)
    fig.text(0.012, 0.925,
             f"diez decisiones de andar, elegidas al azar con semilla {SEM} · "
             f"cada raya va del instante de decidir a {K} instantes después",
             fontsize=7, color=GRIS, ha="left")
    fig.savefig(salida)
    plt.close(fig)
    return salida


def main():
    os.makedirs(os.path.join(AQUI, "figE"), exist_ok=True)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
    mejor = max(idx, key=lambda i: os.path.getsize(fs[i]))
    p = una(fs[mejor], "Una vida de S-2 · la foto contra la proyección",
            os.path.join(AQUI, "figE", "A6_S2.png"))
    print("escrito:", p)
    q = una(sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P5_C2",
                                          "*policy_agent_10.art.log")))[0],
            "Una vida del mundo lento · la foto contra la proyección",
            os.path.join(AQUI, "figE", "A6_lento.png"))
    print("escrito:", q)


if __name__ == "__main__":
    main()

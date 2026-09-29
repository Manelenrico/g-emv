"""[P5-4A · A6] La confianza a lo largo de una vida, en dos diarios."""
import glob, json, os, random, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4")); sys.path.insert(0, AQUI)
import serie_util as U
import banco_llaves as B, confianza as CF
COL = {"oraculo": "#0B3E49", "nadie": "#C9A227", "mentiroso": "#C4450B"}
NOM = {"oraculo": "oráculo", "nadie": "nadie se mueve", "mentiroso": "mentiroso"}
SOL = ("#", "F", "R")


def traza(f, cons, rnd):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    filas_m = list(sm["filas"])
    slot, herm = pc.get("slot"), pc.get("teammate_slot")
    otro = f.replace(f"policy_agent_{slot}", f"policy_agent_{herm}")
    dia_h = ({rr["tick"]: rr for rr in U.lee(otro)
              if rr.get("k") == "tick" and rr.get("phase") == "live"}
             if os.path.exists(otro) else None)
    dia_yo = {r["tick"]: r for r in recs
              if r.get("k") == "tick" and r.get("phase") == "live"}
    tics = sorted(t for t in dia_yo if t >= 300 and t % 50 == 0)
    C, xs, ys = CF.C0, [], []
    for t in tics:
        riv = {a.get("slot"): tuple(a.get("pos") or ())
               for a in (dia_yo[t].get("ve_agentes") or [])
               if a.get("pos") and a.get("slot") != herm}
        for k in (0, 25, 50, 75, 100):
            u = t + k
            if u not in dia_yo:
                break
            dicho = CF.dice(cons, riv, u, dia_yo, dia_h, herm, filas_m, rnd)
            C, _o, _m = CF.actualiza_C(C, dicho, dia_yo, dia_h, u, herm)
        xs.append(t); ys.append(C)
    return xs, ys, os.path.basename(f)[5:13]


def main():
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
    largos = sorted(idx, key=lambda i: -os.path.getsize(fs[i]))[:2]
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["DejaVu Sans"], "font.size": 7.5,
                         "axes.edgecolor": "#6E6E6E", "figure.facecolor": "white",
                         "axes.facecolor": "white", "savefig.facecolor": "white"})
    fig, ax = plt.subplots(1, 2, figsize=(6.69, 2.6), dpi=300, sharey=True,
                           gridspec_kw={"wspace": 0.12, "left": 0.085,
                                        "right": 0.99, "top": 0.74,
                                        "bottom": 0.17})
    for j, i in enumerate(largos):
        for cons in ("oraculo", "nadie", "mentiroso"):
            xs, ys, nom = traza(fs[i], cons, random.Random(20260920))
            ax[j].plot(xs, ys, lw=1.2, color=COL[cons],
                       label=NOM[cons] if j == 0 else None)
        ax[j].set_title(f"diario {nom}", fontsize=8)
        ax[j].set_xlabel("instantes de partida")
        ax[j].set_ylim(-0.03, 1.03)
        ax[j].grid(axis="y", color="#DDDDDD", lw=0.4); ax[j].set_axisbelow(True)
        for s in ("top", "right"):
            ax[j].spines[s].set_visible(False)
    ax[0].set_ylabel("confianza C")
    ax[0].legend(frameon=False, fontsize=7, ncol=3, loc="lower left",
                 bbox_to_anchor=(0.0, 1.12))
    fig.suptitle("La confianza que se gana", fontsize=10, x=0.012, ha="left",
                 y=0.975)
    fig.text(0.012, 0.90, "C empieza en 0,5 · +0,05 por acierto (3 casillas o "
             "menos) · −0,10 por fallo · solo cuentan los rivales comprobados",
             fontsize=6.8, color="#6E6E6E", ha="left")
    os.makedirs(os.path.join(AQUI, "figC"), exist_ok=True)
    p = os.path.join(AQUI, "figC", "A6_confianza.png")
    fig.savefig(p); plt.close(fig)
    print("escrito:", p)


if __name__ == "__main__":
    main()

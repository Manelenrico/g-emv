"""[P5-7A · A7] Una vida del mundo lento, en una sola linea de tiempo.

La ignorancia global, la amenaza graduada y los tics en que la curiosidad
habria cambiado la decision, sobre el mismo eje.

  python3 cantera/paper5/fig_P57A.py            (P5_C2/10, la vida mas larga)
  python3 cantera/paper5/fig_P57A.py P5_B1 10
"""
from __future__ import annotations
import copy, glob, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)

import serie_util as U                                    # noqa: E402
from serie_util import D, DOV                             # noqa: E402
from alma import appraisal_zs_v42_exp as V42              # noqa: E402
import banco_llaves as B                                  # noqa: E402
import curiosidad as C                                    # noqa: E402

FIG = os.path.join(AQUI, "figG")
K = 0.2
COL_IGN = "#0B3E49"
COL_AM = "#C4450B"
COL_CAMBIO = "#C9A227"
COL_FRONT = "#6A3D9A"


def main():
    carpeta = sys.argv[1] if len(sys.argv) > 1 else "P5_C2"
    slot = sys.argv[2] if len(sys.argv) > 2 else "10"
    os.makedirs(FIG, exist_ok=True)
    f = [x for x in sorted(glob.glob(os.path.join(
        RAIZ, "paintball", "runs", carpeta, "*.art.log")))
        if f"policy_agent_{slot}" in x][0]
    U.pon(False)
    C.instala()
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    arr = next((r for r in recs if r.get("k") == "arranque"), None)
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    INT = ((arr or {}).get("constitucion") or {}).get("intelligence", 8)
    herm = pc.get("teammate_slot")
    ojo = C.Ojo(mundo, INT)
    C.CUR.ojo = ojo
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    dano_hist = []
    T, IG, AM, CAMB, CAMF = [], [], [], [], []
    for r in [x for x in recs if x.get("k") == "tick"]:
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t)
        blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        dano_hist.append((t, sum(float(x.get("amount") or 0)
                                 if isinstance(x, dict) else float(x or 0)
                                 for x in (r.get("damage_taken") or []))))
        if r.get("phase") != "live":
            continue
        pos = tuple(r.get("pos") or ())
        if not pos:
            continue
        ojo.mira(pos, t)
        d100 = sum(v for (tt, v) in dano_hist if t - tt < C.VENTANA_DANO)
        am, _ = C.amenaza(r, mundo, herm, d100, t)
        T.append(t); IG.append(ojo.ignorancia_global()); AM.append(am)
        if t < B.DESDE or (t - B.DESDE) % B.CADA:
            continue
        pre = copy.deepcopy(mem)
        _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
        if ((r.get("intencion") or {}).get("do") == "attack"
                or _el.startswith("atacar")):
            mem.ultimo_ataque = t
        ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo, "tick": t,
               "r": r}
        C.CUR.on = False
        base = B.decide_v42(ctx)
        C.CUR.dist_frontera = C.dist_a_frontera(ojo, mundo)
        C.CUR.ign_global = ojo.ignorancia_global()
        C.CUR.on, C.CUR.k, C.CUR.balanza = True, K, True
        C.CUR.amenaza_ahora = am
        C.CUR.modo = "local"
        if B.decide_v42(ctx)["elegido"] != base["elegido"]:
            CAMB.append(t)
        C.CUR.modo = "frontera"
        if B.decide_v42(ctx)["elegido"] != base["elegido"]:
            CAMF.append(t)
        C.CUR.on = False

    fig, ax = plt.subplots(figsize=(12.5, 4.6))
    ax.plot(T, IG, color=COL_IGN, lw=1.8, label="ignorancia global")
    # la amenaza cruda entra y sale de golpe (un armado aparece y desaparece
    # de la vista): se dibuja tenue, y encima su mediana movil de 100 tics,
    # que es la que se puede leer.
    ax.plot(T, AM, color=COL_AM, lw=.6, alpha=.28)
    import statistics as _st
    V = 100
    SU = [_st.median(AM[max(0, i - V):i + 1]) for i in range(len(AM))]
    ax.plot(T, SU, color=COL_AM, lw=1.8,
            label="amenaza graduada (mediana movil 100 tics; cruda en tenue)")
    ax.axhspan(0, C.SEGURO, color="#2e7d32", alpha=.07)
    ax.axhspan(C.INSEGURO, 1, color="#b71c1c", alpha=.07)
    ax.axhline(C.SEGURO, color="#2e7d32", lw=.8, ls=":")
    ax.axhline(C.INSEGURO, color="#b71c1c", lw=.8, ls=":")
    ax.annotate("seguro", (0.995, 0.06), xycoords="axes fraction", ha="right",
                fontsize=8.5, color="#2e7d32", weight="bold")
    ax.annotate("inseguro", (0.995, 0.93), xycoords="axes fraction",
                ha="right", fontsize=8.5, color="#b71c1c", weight="bold")
    for t in CAMF:
        ax.axvline(t, color=COL_FRONT, lw=1.2, alpha=.55, zorder=2)
    for t in CAMB:
        ax.axvline(t, color=COL_CAMBIO, lw=1.8, alpha=.95, zorder=4)
    if CAMF:
        ax.plot([], [], color=COL_FRONT, lw=1.6,
                label=f"cambia la FRONTERA ({len(CAMF)})")
    if CAMB:
        ax.plot([], [], color=COL_CAMBIO, lw=1.8,
                label=f"cambia el LOCAL ({len(CAMB)})")
    ax.set_xlabel("tic"); ax.set_ylabel("fraccion / amenaza [0-1]")
    ax.set_ylim(0, 1); ax.set_xlim(min(T), max(T))
    ax.grid(alpha=.22, ls=":")
    ax.legend(fontsize=8.5, frameon=False, loc="lower left", ncol=3,
              framealpha=.9)
    ax.set_title(f"A7 · una vida del mundo lento — {carpeta}/{slot} "
                 f"(k = {K}, con balanza) — las dos variantes",
                 fontsize=12, loc="left")
    fig.tight_layout()
    p = os.path.join(FIG, f"A7_{carpeta}_a{slot}.png")
    fig.savefig(p, dpi=160); plt.close(fig)
    print(f"  tics vivos {len(T):,} · cambios local {len(CAMB)} · "
          f"frontera {len(CAMF)} · {p}")


if __name__ == "__main__":
    main()

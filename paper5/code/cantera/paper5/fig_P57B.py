"""[P5-7B · B4] Una vida del lento: los asientos a la vista, su conocimiento y
su signo a lo largo del tiempo, y los tics en que cada fila cambio la decision.
"""
import copy, glob, os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4")); sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B, curiosidad as C, otros as O

FIG = os.path.join(AQUI, "figH")
K_O, K_S = 0.1, 0.1
COL = {-1: "#C4450B", 0: "#8a8a8a", 1: "#2e7d32"}
NOM = {-1: "negativo (nos pego o disparo)", 0: "neutro (sin evidencia)",
       1: "positivo (pudo y no quiso)"}


def main():
    carp = sys.argv[1] if len(sys.argv) > 1 else "P5_C2"
    slot = sys.argv[2] if len(sys.argv) > 2 else "10"
    os.makedirs(FIG, exist_ok=True)
    f = [x for x in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                                  carp, "*.art.log")))
         if f"policy_agent_{slot}" in x][0]
    U.pon(False); O.instala()
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    herm = pc.get("teammate_slot")
    mem_o = O.MemoriaOtros(mundo, herm); O.SOC.mem = mem_o
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    dh = []
    serie = {}          # slot -> [(tick, conocimiento, signo)]
    CAMB_O, CAMB_S = [], []
    for r in recs:
        if r.get("k") != "tick":
            continue
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        dh.append((t, sum(float(x.get("amount") or 0) if isinstance(x, dict)
                          else 0.0 for x in (r.get("damage_taken") or []))))
        if r.get("phase") != "live":
            continue
        mem_o.observa(r, t)
        for sl, ob in mem_o.por_slot.items():
            serie.setdefault(sl, []).append((t, ob.conocimiento(), ob.signo(100)))
        pre = copy.deepcopy(mem)
        if t < B.DESDE or (t - B.DESDE) % B.CADA:
            continue
        d100 = sum(v for (tt, v) in dh if t - tt < C.VENTANA_DANO)
        am, _ = C.amenaza(r, mundo, herm, d100, t)
        ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo, "tick": t, "r": r}
        O.SOC.on = False
        base = B.decide_v42(ctx)
        O.SOC.amenaza_ahora = am
        O.SOC.desconocido = mem_o.desconocido_mas_cerca(r)
        O.SOC.positivos = mem_o.positivos_a_la_vista(r)
        for ko, ks, caja in ((K_O, 0.0, CAMB_O), (0.0, K_S, CAMB_S)):
            O.SOC.on, O.SOC.k_o, O.SOC.k_s = True, ko, ks
            O.SOC.reinicia_cuentas()
            if B.decide_v42(ctx)["elegido"] != base["elegido"]:
                caja.append(t)
        O.SOC.on = False

    fig, ax = plt.subplots(figsize=(12.5, 5.0))
    vistos = sorted(serie, key=lambda s: -len(serie[s]))[:8]
    for sl in vistos:
        v = serie[sl]
        ax.plot([x[0] for x in v], [x[1] for x in v], lw=1.1, alpha=.85,
                color=COL[v[-1][2]])
        ax.annotate(f"{sl}", (v[-1][0], v[-1][1]), fontsize=7.5,
                    color=COL[v[-1][2]], xytext=(3, 0),
                    textcoords="offset points")
    for s_, n_ in NOM.items():
        ax.plot([], [], color=COL[s_], lw=2, label=n_)
    for t in CAMB_S:
        ax.axvline(t, color="#6A3D9A", lw=1.4, alpha=.6, zorder=2)
    for t in CAMB_O:
        ax.axvline(t, color="#C9A227", lw=1.8, alpha=.95, zorder=3)
    if CAMB_O:
        ax.plot([], [], color="#C9A227", lw=1.8,
                label=f"cambia R-CURIOSIDAD-OTROS ({len(CAMB_O)})")
    if CAMB_S:
        ax.plot([], [], color="#6A3D9A", lw=1.4,
                label=f"cambia S-VINCULO-EXTRANO ({len(CAMB_S)})")
    ax.set_xlabel("tic"); ax.set_ylabel("conocimiento del asiento [0-1]")
    ax.set_ylim(0, 1.05); ax.grid(alpha=.22, ls=":")
    ax.legend(fontsize=8, frameon=False, loc="lower right", ncol=2)
    ax.set_title(f"B4 · los otros en una vida del lento — {carp}/{slot} "
                 f"(k_o={K_O}, k_s={K_S}); color = signo al final",
                 fontsize=12, loc="left")
    fig.tight_layout()
    p = os.path.join(FIG, f"B4_{carp}_a{slot}.png")
    fig.savefig(p, dpi=160); plt.close(fig)
    print(f"  asientos vistos {len(serie)} · cambios otros {len(CAMB_O)} · "
          f"vinculo {len(CAMB_S)} · {p}")


if __name__ == "__main__":
    main()

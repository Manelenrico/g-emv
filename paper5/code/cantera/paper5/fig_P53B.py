"""[P5-3B · B6] Tres escenas: una aceptada, una rechazada por vida minima y una
rechazada por area, con la curva de la forma y la de seguir solo."""
import collections, glob, json, os, random, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                      # noqa: E402
from serie_util import D, DOV                               # noqa: E402
from alma import appraisal_zs_v42_exp as V42                # noqa: E402
import banco_llaves as B                                    # noqa: E402
import banco_forma3 as BF                                    # noqa: E402
import proyeccion as P                                      # noqa: E402
import forma as F                                           # noqa: E402

ACENTO, TINTA, GRIS, REJILLA = "#C4450B", "#111111", "#6E6E6E", "#DDDDDD"
HOR = BF.HOR


def busca(n_por_tipo=1):
    """Recorre diarios hasta tener un caso de cada veredicto."""
    D.A = V42
    U.pon(False)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(BF.SEMILLA).sample(range(len(fs)), 40))
    want = {"ok": [], "vida": [], "area": []}
    import copy
    for i in idx:
        if all(len(v) >= n_por_tipo for v in want.values()):
            break
        f = fs[i]
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            continue
        BF.B.pon_v42(B.interruptores(recs))
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
        vivos = [r for r in recs if r.get("k") == "tick"
                 and r.get("phase") == "live"]
        vivo = {r["tick"] for r in vivos}
        pos_t = {r["tick"]: tuple(r.get("pos") or ()) for r in vivos}
        d_t = {}
        for r in vivos:
            R = r.get("RADIOGRAFIA") or {}
            c = (R.get("candidatos") or {}).get(R.get("elegido"))
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
        for r in [x for x in recs if x.get("k") == "tick"]:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t)
            blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            pre = copy.deepcopy(mem)
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if (r.get("intencion") or {}).get("do") == "attack" or _el.startswith("atacar"):
                mem.ultimo_ataque = t
            if not (t >= BF.DESDE and t % BF.CADA == 0):
                continue
            t2 = t + HOR
            if not (t2 in vivo and d_t.get(t2) is not None
                    and d_t.get(t) is not None and d_t[t2] < d_t[t]):
                continue
            bd = B.decide_v42({"o": o, "mundo": mundo, "mem": pre, "blo": blo,
                               "tick": t, "r": r})
            el = bd.get("elegido") or ""
            dest_cuerpo = None
            for n, rec in D.candidatos(o, mundo, copy.deepcopy(pre), t,
                                       copy.deepcopy(blo)):
                if n == el and isinstance(rec, dict) and rec.get("destino"):
                    dest_cuerpo = tuple(rec["destino"])
                    break
            tramos = BF.tramos_reales(tk, t, HOR)
            if tramos and tramos[0].get("destino") and dest_cuerpo \
                    and tuple(tramos[0]["destino"]) == tuple(dest_cuerpo):
                continue
            e0 = P.estado_de(r)
            suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
                     if it.get("pos")}
            pcs = F.puntos_de_control(e0, tramos)
            tics = [x[0] for x in pcs]
            cf = F.curva(e0, o, tramos, mundo, pre, suelo)
            base_c = list(D.candidatos(o, mundo, copy.deepcopy(pre), t,
                                       copy.deepcopy(blo)))
            cs, quien, _sv = F.mejor_propia(e0, o, base_c, tics, mundo, pre,
                                            suelo, t)
            if cs is None:
                continue
            ver, ar, dt = F.juzga_forma(cf, cs, t)
            if len(want[ver]) < n_por_tipo:
                want[ver].append({"diario": os.path.basename(f), "tic": t,
                                  "cf": cf, "cs": cs, "area": ar,
                                  "tramos": tramos, "ver": ver})
        del recs
    return want


def dibuja(want, salida):
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["DejaVu Sans"], "font.size": 7.5,
                         "axes.edgecolor": GRIS, "text.color": TINTA,
                         "axes.labelcolor": TINTA, "xtick.color": GRIS,
                         "ytick.color": GRIS, "figure.facecolor": "white",
                         "axes.facecolor": "white", "savefig.facecolor": "white"})
    titulos = {"ok": "aceptada", "vida": "rechazada por vida mínima",
               "area": "rechazada por área"}
    fig, ax = plt.subplots(1, 3, figsize=(6.69, 2.7), dpi=300,
                           gridspec_kw={"wspace": 0.30, "left": 0.075,
                                        "right": 0.99, "top": 0.72,
                                        "bottom": 0.16})
    for j, key in enumerate(("ok", "vida", "area")):
        a = ax[j]
        if not want[key]:
            a.set_axis_off()
            continue
        c = want[key][0]
        tf = [p["tic"] for p in c["cf"]]
        a.plot(tf, [p["d"] for p in c["cf"]], "-o", ms=3.4, lw=1.1,
               color=ACENTO, label="la forma")
        a.plot([p["tic"] for p in c["cs"]], [p["d"] for p in c["cs"]],
               "--s", ms=3.0, lw=1.0, color=GRIS, label="la mejor propia")
        for p in c["cf"]:
            if p["vida"] is not None and p["vida"] < F.VIDA_MIN:
                a.plot([p["tic"]], [p["d"]], "x", ms=7, color=TINTA, zorder=5)
        a.set_title(f"{titulos[key]}\ntic {c['tic']} · área {c['area']:+.3f}"
                    f" · propia: {c.get('quien')}",
                    fontsize=7.8, color=TINTA)
        a.set_xlabel("instante")
        if j == 0:
            a.set_ylabel("d (más bajo, mejor)")
            a.legend(frameon=False, fontsize=6.8, loc="best")
        a.grid(axis="y", color=REJILLA, lw=0.4)
        a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    fig.suptitle("Tres formas contra la mejor curva del puñado propio",
                 fontsize=10, x=0.012, ha="left", y=0.965)
    fig.text(0.012, 0.865, "cada punto es un punto de control, en el tic de "
             "llegada de su tramo · la aspa marca vida por debajo de 15",
             fontsize=7, color=GRIS, ha="left")
    fig.savefig(salida)
    plt.close(fig)
    return salida


if __name__ == "__main__":
    w = busca()
    os.makedirs(os.path.join(AQUI, "figB"), exist_ok=True)
    for k, v in w.items():
        print(k, len(v), (v[0]["diario"][:20], v[0]["tic"]) if v else "")
    print("escrito:", dibuja(w, os.path.join(AQUI, "figB", "C4_formas.png")))

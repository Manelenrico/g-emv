"""[P8] Prompt 150 (copia del programa del v5, prompt 134, con las clases, la carpeta y las semillas del v6; la protagonista RG69r+voz, «RG69rvoz» en las carpetas, en el sitio de RG68r) (texto del v5:) [P8] Prompt 134 (copia del programa del v4, prompt 117, con las clases, la carpeta y las semillas del v5): las medidas sin predicción del experimento v4 (copia de medidas_v3.py con las clases, las semillas y la carpeta del v4) (valle_experimento_v6), como las fija predicciones_selladas_v6.md (sección «Cómo se mide cada
predicción y cada medida»). Solo lee.
  M1 felicidad funcional (las cinco clases de criatura); M2 momentos hygge, M3 los sitios en el cuaderno, M4 los tres mapas (figuras), M5 el huerto y M6 el
  perdón (RG69r+voz; M5 también las demás clases y los jugadores de base).
   python3 medidas_v6.py -> medidas_v6.md, medidas_v6.json y salida/figuras_v6/mapas_<mundo>.png"""
import gzip, json, os, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import cuerpo_valle as CV
EXP = "/Volumes/Mem G-EMV/valle_experimento_v6"; SEM = range(30161, 30201); MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian")
CRI = ("RG69rvoz", "RG69r", "RG68r", "RG068r"); BASE = ("tonto", "recolector"); FIG = os.path.join(AQUI, "salida", "figuras_v6")
MC = CV.MUNDO_CFG; DIA = MC["dia"]["turnos"]; FLACA = MC["criaturas"]["umbral_flaca"]
FASES = []
for nom, n in MC["dia"]["fases"]: FASES += [nom] * int(n)
fase = lambda t: FASES[t % DIA] if len(FASES) == DIA else None
her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
def ruta(v, mu, s): return os.path.join(EXP, f"{v}_{mu}_s{s}_d40" if v in BASE else f"{v}_{mu}+sabores_s{s}_d40")

def m1(arg):
    v, mu, s = arg; d = ruta(v, mu, s); A = defaultdict(lambda: [0, 0, 0.0, 0.0, 0.0])          # turnos despierta, turnos feliz, suma de los tres balances
    for l in gzip.open(os.path.join(d, "balance.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l)
        for a, r in x["c"].items():
            if r[6]: continue
            z = A[a]; z[0] += 1; z[1] += r[0] > 0 and r[1] > 0 and r[2] > 0; z[2] += r[0]; z[3] += r[1]; z[4] += r[2]
    por = {a: {"feliz": z[1] / z[0], "b": [z[2] / z[0], z[3] / z[0], z[4] / z[0]]} for a, z in A.items() if z[0]}
    fr = [p["feliz"] for p in por.values()]
    return {"v": v, "mu": mu, "s": s, "aldea": sum(fr) / len(fr) if fr else None, "peor": min(fr) if fr else None, "por": por}

def rg(arg):
    """M2, M3, M4, M5 (quién) y M6 en una partida de RG69r+voz"""
    v, mu, s = arg; d = ruta(v, mu, s); fin = json.load(open(os.path.join(d, "fin.json")))
    ham = {}; pos = {}; miedo = Counter(); peleas = Counter(); trab = Counter(); robos = []
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["turno"]
        for a, g in x["agentes"].items():
            ham[(t, a)] = g["cuerpo"]["hambre"]; pos[(t, a)] = tuple(g["pos"])
            if g.get("accion") == "trabajar" and g.get("resultado") == "ok": trab[a] += 1
        for e in x["eventos"]:
            for k in ("bestia_pega", "bestia_roba"):
                y = e.get(k)
                if y and (t, y) in pos: miedo[pos[(t, y)]] += 1
            if "empujon" in e:
                b = e.get("a")
                if b and (t, b) in pos: peleas[pos[(t, b)]] += 1
                if e.get("gana") and e.get("soltado"):
                    w_ = e["gana"]; p_ = e["a"] if w_ == e["empujon"] else e["empujon"]
                    if w_[0] != p_[0]: robos.append((t, p_, w_))
    bien = defaultdict(lambda: [0.0, 0]); hyg = Counter(); noches = set()
    for l in gzip.open(os.path.join(d, "balance.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["t"]; fa = fase(t); c = x["c"]
        for a, r in c.items():
            if not r[6]: z = bien[(r[3], r[4])]; z[0] += r[0] + r[1] + r[2]; z[1] += 1
            if fa in ("anochecer", "noche"):
                n_ = (a, (t - (DIA if fa == "noche" and t % DIA < DIA // 2 else 0)) // DIA); noches.add(n_)
                h = her(a)
                if r[5] == "C" and h in c and c[h][5] == "C" and ham.get((t, a), 0) <= FLACA and not r[7] and r[0] > 0 and r[1] > 0 and r[2] > 0: hyg[n_] += 1
    # M3: los recuerdos de sitios, pesados por la intensidad
    M3 = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    cs = json.load(open(os.path.join(d, "cuaderno_sitios.json")))
    for a, O in cs.items():
        for o, S in O.items():
            for sit, R in S.items():
                for r in R:
                    if r.get("origen") != "vivido": continue
                    w_ = float(r.get("intensidad") or 0.0); z = M3[f"{o[6:]}|{sit}"]; z[0] += w_
                    z[1] += w_ * float((r.get("efecto") or {}).get("cuerpo") or 0.0); z[2] += w_ * float((r.get("efecto") or {}).get("recursos") or 0.0); z[3] += w_ * float((r.get("importancia") or {}).get("cuerpo") or 0.0)
    # M6: el perdón (radar_dia: al empezar cada día, lo que vale cada otra)
    RD = json.load(open(os.path.join(d, "radar_dia.json"))); val = {a: {int(e[0]): e[1] for e in L_} for a, L_ in RD.items()}
    muere = {m["criatura"]: m["dia"] for m in fin["muertes"]}; M6 = []
    for t, p_, w_ in robos:
        dd = t // DIA; V = val.get(p_, {})
        if dd not in V or w_ not in V[dd]: continue
        v0 = sum(V[dd][w_][k] for k in ("cuerpo", "recursos", "vinculo")); fin_d = min(muere.get(p_, 40), muere.get(w_, 40), 40); vuelve = None
        for d2 in range(dd + 1, fin_d + 1):
            if d2 in V and w_ in V[d2] and sum(V[d2][w_][k] for k in ("cuerpo", "recursos", "vinculo")) >= v0: vuelve = d2 - dd; break
        M6.append(vuelve)
    return {"v": v, "mu": mu, "s": s, "bien": {f"{k[0]},{k[1]}": z for k, z in bien.items()}, "miedo": {f"{k[0]},{k[1]}": n for k, n in miedo.items()},
            "peleas": {f"{k[0]},{k[1]}": n for k, n in peleas.items()}, "hyg": sum(hyg.values()), "hyg_noches_con": len(hyg), "noches": len(noches),
            "M3": {k: z for k, z in M3.items()}, "trab": dict(trab), "M6": M6}

def trabaja(arg):
    v, mu, s = arg; n = 0
    for l in gzip.open(os.path.join(ruta(v, mu, s), "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); n += sum(1 for g in x["agentes"].values() if g.get("accion") == "trabajar" and g.get("resultado") == "ok")
    return {"v": v, "mu": mu, "n": n}

def mapas(R):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; import numpy as np; import lanzador as L
    e = L.MU.Valle(); _, inf = e.reset(seed=SEM[0]); mp = inf[e.agents[0]]["mapa"]; W, H = mp["ancho"] + 2, mp["alto"] + 2; os.makedirs(FIG, exist_ok=True); out = []
    for mu in MUNDOS:
        X = [r for r in R if r["mu"] == mu]; B = np.full((H, W), np.nan); M = np.zeros((H, W)); P = np.zeros((H, W)); acc = defaultdict(lambda: [0.0, 0])
        for r in X:
            for k, (s_, n) in r["bien"].items(): z = acc[k]; z[0] += s_; z[1] += n
            for k, n in r["miedo"].items(): x_, y_ = map(int, k.split(",")); M[y_, x_] += n
            for k, n in r["peleas"].items(): x_, y_ = map(int, k.split(",")); P[y_, x_] += n
        for k, (s_, n) in acc.items():
            x_, y_ = map(int, k.split(","))
            if n >= 20: B[y_, x_] = s_ / n
        fig, ax = plt.subplots(1, 3, figsize=(15, 5.2))
        for a_, Z, t_, cm in ((ax[0], B, "bienestar: balance medio (cuerpo + recursos + vínculo), despierta", "RdYlGn"), (ax[1], M, "miedo: golpes y robos de la bestia", "Reds"), (ax[2], P, "peleas: empujones (y robos) entre criaturas", "Purples")):
            im = a_.imshow(Z, cmap=cm, origin="upper"); a_.set_title(t_, fontsize=9); a_.set_xticks([]); a_.set_yticks([]); fig.colorbar(im, ax=a_, fraction=0.046)
        fig.suptitle(f"El valle, {mu} — RG69r+voz, 40 partidas (semillas 30161-30200)", fontsize=11); f_ = os.path.join(FIG, f"mapas_{mu}.png"); fig.savefig(f_, dpi=110, bbox_inches="tight"); plt.close(fig); out.append(f_)
    return out


if __name__ == "__main__":
    hecho = lambda v, mu, s: os.path.exists(os.path.join(ruta(v, mu, s), "fin.json"))
    T1 = [(v, mu, s) for v in CRI for mu in MUNDOS for s in SEM if hecho(v, mu, s)]; T2 = [x for x in T1 if x[0] == "RG69rvoz"]; T3 = [(v, mu, s) for v in CRI + BASE for mu in MUNDOS for s in SEM if hecho(v, mu, s)]
    with Pool(9) as p: R1 = p.map(m1, T1); R2 = p.map(rg, T2); R3 = p.map(trabaja, T3)
    w = []; pc = lambda a, b: f"{100 * a / b:.0f} %" if b else "—"; med = lambda X: sorted(X)[len(X) // 2] if X else float("nan"); m = lambda X: sum(X) / len(X) if X else float("nan")
    w.append(f"Partidas leídas: criaturas {len(T1)} (RG69r+voz {len(T2)}); con los jugadores de base, {len(T3)}.\n")
    w.append("## M1. Felicidad funcional (turnos despierta con los tres balances > 0)\n\n| mundo | clase | la aldea (media de las ocho): media · mediana de las partidas | la peor parada: media · mediana | balances medios: cuerpo · recursos · vínculo |\n|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in CRI:
            X = [r for r in R1 if r["v"] == v and r["mu"] == mu and r["aldea"] is not None]; bb = [p["b"] for r in X for p in r["por"].values()]
            if X: w.append(f"| {mu} | {v} | {100 * m([r['aldea'] for r in X]):.0f} % · {100 * med([r['aldea'] for r in X]):.0f} % | {100 * m([r['peor'] for r in X]):.0f} % · {100 * med([r['peor'] for r in X]):.0f} % | " + " · ".join(f"{m([b[i] for b in bb]):+.2f}" for i in range(3)) + " |")
    w.append("\n## M2. Momentos hygge (RG69r+voz): al anochecer o de noche, en su casa con la hermana dentro, sin estar flaca, sin la bestia a la vista y con los tres balances > 0\n\n| mundo | turnos hygge por criatura y noche | noches (de cada criatura) con al menos uno |\n|---|---|---|")
    for mu in MUNDOS:
        X = [r for r in R2 if r["mu"] == mu]
        if X: w.append(f"| {mu} | {sum(r['hyg'] for r in X) / max(1, sum(r['noches'] for r in X)):.1f} | {pc(sum(r['hyg_noches_con'] for r in X), sum(r['noches'] for r in X))} |")
    w.append("\n## M3. Lo que siente en cada sitio según sus recuerdos (RG69r+voz; recuerdos vividos, pesados por la intensidad): efecto en cuerpo · efecto en recursos · importancia (cuerpo)\n")
    sitios = sorted({k for r in R2 for k in r["M3"]})
    w.append("| sitio | " + " | ".join(MUNDOS) + " |\n|" + "---|" * (len(MUNDOS) + 1))
    for k in sitios:
        cel = []
        for mu in MUNDOS:
            z = [0.0, 0.0, 0.0, 0.0]
            for r in R2:
                if r["mu"] == mu and k in r["M3"]: z = [a + b for a, b in zip(z, r["M3"][k])]
            cel.append(f"{z[1] / z[0]:+.2f} · {z[2] / z[0]:+.2f} · {z[3] / z[0]:+.3f}" if z[0] else "—")
        w.append(f"| {k.replace('|', ', ')} | " + " | ".join(cel) + " |")
    w.append("\n## M4. Los tres mapas del valle (figuras)\n")
    for f_ in mapas(R2): w.append(f"![{os.path.basename(f_)}]({os.path.relpath(f_, AQUI)})")
    w.append("\n## M5. El huerto: veces que se trabaja una planta, por partida\n\n| mundo | " + " | ".join(CRI + BASE) + " |\n|" + "---|" * (len(CRI + BASE) + 1))
    for mu in MUNDOS: w.append(f"| {mu} | " + " | ".join(f"{m([r['n'] for r in R3 if r['v'] == v and r['mu'] == mu]):.0f}" for v in CRI + BASE) + " |")
    w.append("\n**Quién trabaja, en RG69r+voz** (de lo trabajado en cada partida): la criatura que más · las dos de la casa que más\n\n| mundo | la que más | la casa que más |\n|---|---|---|")
    for mu in MUNDOS:
        X = [r for r in R2 if r["mu"] == mu and r["trab"]]
        top = [max(r["trab"].values()) / sum(r["trab"].values()) for r in X]; casa = [max(sum(n for a, n in r["trab"].items() if a[0] == c) for c in "ABCD") / sum(r["trab"].values()) for r in X]
        if X: w.append(f"| {mu} | {100 * m(top):.0f} % | {100 * m(casa):.0f} % |")
    w.append("\n## M6. El perdón (RG69r+voz): días hasta que la ladrona vuelve a valer en el radar de la robada lo que valía el día del robo\n\n| mundo | robos de vecinas | días: mediana (de los que vuelven) | sin volver |\n|---|---|---|---|")
    for mu in MUNDOS:
        Z = [z for r in R2 if r["mu"] == mu for z in r["M6"]]; V_ = [z for z in Z if z is not None]
        if Z: w.append(f"| {mu} | {len(Z)} | {med(V_)} | {pc(len(Z) - len(V_), len(Z))} |")
    json.dump({"M1": R1, "M2_M6": [{k: r[k] for k in ("v", "mu", "s", "hyg", "hyg_noches_con", "noches", "M3", "trab", "M6")} for r in R2], "M5": R3}, open(os.path.join(AQUI, "salida", "medidas_v6.json"), "w"), ensure_ascii=False)
    open(os.path.join(AQUI, "medidas_v6.md"), "w").write("\n".join(w) + "\n"); print("\n".join(w))

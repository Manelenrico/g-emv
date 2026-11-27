"""[P8] Prompt 90: RG45r (la pieza I con la hermana, el duelo desde el radar) frente a RG44r, en normal, sequía y «bestias que crían» con los sabores (semillas
1001-1021, 40 días), del registro del mundo y de lo que apunta cada criatura (imagina.json, radar_dia.json):
  1. junto a la hermana herida cuando hay peligro (una bestia a dos casillas o menos de ella o de la herida, o a la vista de ella) y sin peligro;
  2. a casa juntas al anochecer: de los días con las dos hermanas vivas, en cuántos están las dos en casa al empezar la noche, y en cuántos entran (la primera vez
     en casa desde el anochecer) con cinco turnos o menos de diferencia;
  3. si una sigue a la otra: con las dos fuera de casa y a cuatro casillas o menos, de los turnos en que la otra se movió en el turno anterior, en cuántos da ella
     el mismo paso;
  4. si se juntan para echar a la bestia (de analiza_v44: echadas y quién va junta);
  5. vivas (pareadas por semilla);
  6. la reconstrucción tras la muerte de la hermana: la parte de cada día pegada a una vecina viva (cinco días antes y diez después), cuándo pasa de lo de antes,
     y el valor aprendido (radar: cuerpo + recursos + vínculo) de la vecina que más vale para ella, el día de la muerte y 5 y 10 días después, frente a las
     que no la perdieron (los mismos días);
  y de RG45r: las costumbres aprendidas frente a lo que hace de verdad la hermana (todos sus pasos, con la misma clasificación, clase_paso de cuerpo_valle), lo
  que predice frente a dónde está de verdad al acabar la mirada (y frente a quedarse donde la vio o seguir su último paso), y el duelo de cada muerte.
   python3 analiza_v45.py -> markdown por pantalla"""
import gzip, json, os, random, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
for p_ in (RAIZ, os.path.join(RAIZ, "valle")):
    if p_ not in sys.path: sys.path.insert(0, p_)
import lanzador as L0                                                     # el mundo del valle (valle/mundo.py), como lo importa el lanzador
import cuerpo_valle as CV, analiza_v44 as A44
from jugadores import Mapa
Valle = L0.MU.Valle
T44 = "/Volumes/Mem G-EMV/valle_taller_v44"; T45R = "/Volumes/Mem G-EMV/valle_taller_v45_rg44"; SEM = range(1001, 1022); NB = 10000
CFG = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); CR = CFG["criaturas"]; VF = CR["vista_por_fase"]; H = CV.T["mirada"]
DIA = CFG["dia"]["turnos"]; INI_NOCHE = sum(n for f, n in CFG["dia"]["fases"] if f != "noche"); INI_ANOCHECER = INI_NOCHE - dict(CFG["dia"]["fases"])["anochecer"]
MUNDOS = ("normal+sabores", "sequia+sabores", "bestias_crian+sabores")
cheb = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])); her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
_MAPA = {}

def mapa(s):
    if s not in _MAPA:
        e = Valle(); _, inf = e.reset(seed=s); mp = inf[e.agents[0]]["mapa"]; _MAPA[s] = (Mapa(mp), {k: {tuple(c) for c in v["celdas"]} for k, v in mp["casas"].items()})
    return _MAPA[s]

def carpeta(v, mu, s):
    d = os.path.join(T45R, f"{v}_{mu}_s{s}_d40")
    return d if (v == "RG44r" and os.path.exists(os.path.join(d, "fin.json"))) else os.path.join(T44, f"{v}_{mu}_s{s}_d40")

def una(arg):
    v, mu, s = arg; d = carpeta(v, mu, s); M, CASAS = mapa(s); TODAS = set().union(*CASAS.values())
    fin = json.load(open(os.path.join(d, "fin.json"))); L = [json.loads(l) for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8")]
    C = Counter(); verdad = defaultdict(Counter); sigue = Counter(); entra = {}; cerca_dia = defaultdict(lambda: defaultdict(lambda: [0, 0])); muere_her = {}
    pos = lambda Lx, a: tuple(Lx["agentes"][a]["pos"]); viva = lambda Lx, a: a in Lx["agentes"] and not Lx["agentes"][a]["cuerpo"]["muerta"]
    for i, x in enumerate(L):
        t = x["turno"]; dia, r = divmod(t, DIA); bs = [tuple(b["pos"]) for b in (x.get("bestias") or [x["bestia"]]) if b.get("pos") is not None]
        for a, g in x["agentes"].items():
            if g["cuerpo"]["muerta"]: continue
            p = tuple(g["pos"]); h = her(a); hv = viva(x, h)
            if not hv and a not in muere_her and h in x["agentes"]: muere_her[a] = t
            if hv:
                hp = pos(x, h)
                if x["agentes"][h]["cuerpo"]["vida"] < CR["umbral_herida"]:            # 1. junto a la herida
                    pel = any(cheb(b, hp) <= 2 or cheb(b, p) <= 2 or cheb(b, p) <= VF[x["fase"]] for b in bs)
                    k = "peligro" if pel else "sin"; C["her_" + k] += 1; C["her_" + k + "_junto"] += cheb(p, hp) <= 1
                if i > 0 and viva(L[i - 1], h) and viva(L[i - 1], a):                   # las costumbres de verdad: cada paso de la hermana (vista o no)
                    q0 = pos(L[i - 1], h); bq = min(bs, key=lambda b: cheb(b, q0)) if bs else None
                    kk = CV.clase_paso(M, CASAS[a[0]], q0, hp, p, bq)
                    if kk is not None:
                        hx = L[i - 1]["agentes"][h]["cuerpo"]; sit = CV.situacion_de(hx["hambre"] > CR["umbral_flaca"], hx["vida"] < CR["umbral_herida"], bq is not None and cheb(bq, q0) <= VF[L[i - 1]["fase"]], L[i - 1]["fase"], False)
                        verdad[sit.rsplit("|", 1)[0]][kk] += 1
                    if i > 1 and viva(L[i - 2], h) and p not in TODAS and hp not in TODAS and cheb(p, hp) <= 4:      # 3. sigue a la otra
                        paso_h = (q0[0] - pos(L[i - 2], h)[0], q0[1] - pos(L[i - 2], h)[1]); pa0 = pos(L[i - 1], a); paso_a = (p[0] - pa0[0], p[1] - pa0[1])
                        if paso_h != (0, 0): sigue["n"] += 1; sigue["igual"] += paso_a == paso_h
            if r >= INI_ANOCHECER and p in CASAS[a[0]] and (a, dia) not in entra: entra[(a, dia)] = r
            cerca_dia[a][dia][0] += any(y[0] != a[0] and not gy["cuerpo"]["muerta"] and cheb(p, tuple(gy["pos"])) <= 1 for y, gy in x["agentes"].items())
            cerca_dia[a][dia][1] += 1                                                   # 6. pegada a una vecina viva, por día
        if r == INI_NOCHE:                                                              # 2. las dos en casa al empezar la noche
            for c in sorted({a[0] for a in x["agentes"]}):
                a1, a2 = c + "1", c + "2"
                if viva(x, a1) and viva(x, a2):
                    C["casa_dias"] += 1; C["casa_juntas"] += pos(x, a1) in CASAS[c] and pos(x, a2) in CASAS[c]
                    e1, e2 = entra.get((a1, dia)), entra.get((a2, dia))
                    if e1 is not None and e2 is not None: C["entran"] += 1; C["entran_juntas"] += abs(e1 - e2) <= 5
    out = {"v": v, "mu": mu, "s": s, "vivas": 8 - len(fin["muertes"]), "hambre": sum(1 for m in fin["muertes"] if m["causa"] == "hambre"), "C": dict(C), "sigue": dict(sigue),
           "verdad": {k: dict(c) for k, c in verdad.items()}, "b44": A44.una((v, mu, s, os.path.dirname(d)))}
    # 6. la reconstrucción
    rd = json.load(open(os.path.join(d, "radar_dia.json"))) if os.path.exists(os.path.join(d, "radar_dia.json")) else {}
    rec = []
    for a, td in muere_her.items():
        if not viva(L[-1], a) and fin_dia(fin, a) is not None and fin_dia(fin, a) - td // DIA < 5: continue
        d0 = td // DIA; antes = [cerca_dia[a][k][0] / max(1, cerca_dia[a][k][1]) for k in range(max(0, d0 - 5), d0)]; despues = {k - d0: cerca_dia[a][k][0] / max(1, cerca_dia[a][k][1]) for k in range(d0 + 1, d0 + 11) if k in cerca_dia[a]}
        m0 = sum(antes) / len(antes) if antes else 0.0; tarda = next((k for k in sorted(despues) if despues[k] > m0), None)
        val = vecina_val(rd.get(a), a)
        rec.append({"a": a, "dia": d0, "antes": round(m0, 4), "despues": {k: round(v_, 4) for k, v_ in despues.items()}, "tarda": tarda,
                    "valor": {k: val.get(d0 + k) for k in (0, 5, 10)}})
    out["rec"] = rec
    # control: las que no perdieron a su hermana, el valor de su mejor vecina en los mismos días (los de las muertes de esa partida)
    out["control"] = [{k: vecina_val(rd.get(a), a).get(r_["dia"] + k) for k in (0, 5, 10)} for r_ in rec for a in rd if a not in muere_her]
    if os.path.exists(os.path.join(d, "imagina.json")):
        I = json.load(open(os.path.join(d, "imagina.json"))); pr = Counter(); apr = defaultdict(Counter); du = []
        for a, z in I.items():
            for sit, c in z["costumbre"].items(): apr[sit.rsplit("|", 1)[0]].update(c)
            for (t, q, pred, iner, modo, best, p) in z["pred"]:
                j = t + H
                if j < len(L) and viva(L[j], her(a)):
                    real = pos(L[j], her(a))
                    for k_, x_ in (("pred", pred), ("quieta", q), ("inercia", iner)): pr[k_ + "_err"] += cheb(tuple(x_), real); pr[k_ + "_cerca"] += cheb(tuple(x_), real) <= 2
                    pr["n"] += 1; pr["modo_" + modo] += 1
            du += [dict(x_, de=a) for x_ in z["duelos"]]
        out.update(pred=dict(pr), aprendido={k: dict(c) for k, c in apr.items()}, duelos=du)
    return out

def fin_dia(fin, a): return next((m["dia"] for m in fin["muertes"] if m["criatura"] == a), None)

def vecina_val(R, a):
    """por día, el valor aprendido (cuerpo + recursos + vínculo del radar) de la vecina que más vale para ella"""
    if not R: return {}
    return {d_: round(max([sum(v_.values()) for x, v_ in rr.items() if x[0] != a[0]] or [0.0]), 4) for d_, rr, _ in R}

def boot(d):
    x = [d[s] for s in sorted(d)]; n = len(x); r = random.Random(8)
    m = sorted(sum(x[r.randrange(n)] for _ in range(n)) / n for _ in range(NB)); return f"{sum(x) / n:+.2f} [{m[int(0.025 * NB)]:+.2f}, {m[int(0.975 * NB) - 1]:+.2f}]"

def pc(C, a, b): return f"{100 * C[a] / C[b]:.0f} %" if C[b] else "—"


if __name__ == "__main__":
    with Pool(8) as p: R = p.map(una, [(v, mu, s) for v in ("RG44r", "RG45r") for mu in MUNDOS for s in SEM])
    by = {(r["v"], r["mu"], r["s"]): r for r in R}
    print("## RG45r frente a RG44r (40 días, semillas 1001-1021)\n\n| mundo | clase | vivas | muertes de hambre | junto a la herida: con peligro · sin | las dos en casa al empezar la noche | entran con ≤ 5 turnos | sigue el paso de la otra | echadas (con la hermana · con vecinas) |\n|---|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("RG44r", "RG45r"):
            L = [by[(v, mu, s)] for s in SEM]; C = Counter(); sg = Counter(); G = Counter(); B = Counter()
            for r in L: C.update(r["C"]); sg.update(r["sigue"]); G.update(r["b44"]["grupos"]); B.update(r["b44"]["C"])
            print(f"| {mu} | {v} | {sum(r['vivas'] for r in L) / 21:.2f} | {sum(r['hambre'] for r in L)} | {pc(C, 'her_peligro_junto', 'her_peligro')} ({C['her_peligro']}) · {pc(C, 'her_sin_junto', 'her_sin')} | "
                  f"{pc(C, 'casa_juntas', 'casa_dias')} | {pc(C, 'entran_juntas', 'entran')} | {pc(sg, 'igual', 'n')} | {B['bestia_echada']} ({G['empujar|con la hermana']} · {G['empujar|con vecinas'] + G['empujar|con la hermana y vecinas']}) |")
        print(f"| {mu} | RG45r − RG44r, vivas | {boot({s: by[('RG45r', mu, s)]['vivas'] - by[('RG44r', mu, s)]['vivas'] for s in SEM})} | | | | | | |")
    print("\n## La reconstrucción tras la muerte de la hermana\n\n| mundo | clase | muertes de hermana (con la otra viva 5 días o más) | pegada a una vecina: antes · días 1-5 · días 6-10 | pasa de lo de antes (de las que lo hacen) · día mediano | valor de su mejor vecina: el día · +5 · +10 | lo mismo, las que no la perdieron |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("RG44r", "RG45r"):
            rec = [x for s in SEM for x in by[(v, mu, s)]["rec"]]; ctl = [x for s in SEM for x in by[(v, mu, s)]["control"]]
            if not rec: print(f"| {mu} | {v} | 0 | | | | |"); continue
            m = lambda L_: (sum(L_) / len(L_)) if L_ else float("nan")
            d15 = m([m([x["despues"][k] for k in x["despues"] if k <= 5] or [0]) for x in rec]); d610 = m([m([x["despues"][k] for k in x["despues"] if k > 5] or [0]) for x in rec])
            ta = sorted(x["tarda"] for x in rec if x["tarda"] is not None)
            val = lambda k: m([x["valor"][k] for x in rec if x["valor"].get(k) is not None]); cval = lambda k: m([x[k] for x in ctl if x.get(k) is not None])
            print(f"| {mu} | {v} | {len(rec)} | {100 * m([x['antes'] for x in rec]):.0f} % · {100 * d15:.0f} % · {100 * d610:.0f} % | {len(ta)} de {len(rec)} · {ta[len(ta) // 2] if ta else '—'} | "
                  f"{val(0):.3f} · {val(5):.3f} · {val(10):.3f} | {cval(0):.3f} · {cval(5):.3f} · {cval(10):.3f} |")
    print("\n## RG45r: lo que predice de la hermana al acabar la mirada (44 turnos), frente a dónde está de verdad\n\n| mundo | predicciones | por costumbre · por su último paso | error medio (casillas): lo que imagina · quedarse donde la vio · seguir su último paso | a 2 o menos: lo mismo |\n|---|---|---|---|---|")
    for mu in MUNDOS:
        P = Counter()
        for s in SEM: P.update(by[("RG45r", mu, s)].get("pred") or {})
        n = P["n"]
        print(f"| {mu} | {n} | {100 * P['modo_costumbre'] / n:.0f} % · {100 * P['modo_inercia'] / n:.0f} % | {P['pred_err'] / n:.1f} · {P['quieta_err'] / n:.1f} · {P['inercia_err'] / n:.1f} | "
              f"{100 * P['pred_cerca'] / n:.0f} % · {100 * P['quieta_cerca'] / n:.0f} % · {100 * P['inercia_cerca'] / n:.0f} % |")
    print("\n## RG45r: sus costumbres aprendidas frente a lo que hace de verdad la hermana (todos sus pasos; sin «la han llamado», que el registro no guarda)\n")
    for mu in MUNDOS:
        A_ = defaultdict(Counter); V_ = defaultdict(Counter)
        for s in SEM:
            for k, c in (by[("RG45r", mu, s)].get("aprendido") or {}).items(): A_[k].update(c)
            for k, c in by[("RG45r", mu, s)]["verdad"].items(): V_[k].update(c)
        print(f"\n**{mu}** (las situaciones con más pasos; en cada una, la parte de cada destino: aprendido / de verdad; y la distancia de variación total)\n\n| situación (flaca, herida, bestia · hora) | pasos vistos · de verdad | " + " | ".join(CV.COSTUMBRES) + " | distancia |\n|---|---|" + "---|" * len(CV.COSTUMBRES) + "---|")
        tvs = []
        for k in sorted(V_, key=lambda k: -sum(V_[k].values()))[:8]:
            na, nv = sum(A_[k].values()), sum(V_[k].values())
            if not na: continue
            tv = 0.5 * sum(abs(A_[k][c] / na - V_[k][c] / nv) for c in CV.COSTUMBRES); tvs.append((tv, nv))
            print(f"| {k} | {na} · {nv} | " + " | ".join(f"{100 * A_[k][c] / na:.0f} / {100 * V_[k][c] / nv:.0f}" for c in CV.COSTUMBRES) + f" | {tv:.2f} |")
        print(f"\nDistancia media (pesada por los pasos de verdad): {sum(a * b for a, b in tvs) / max(1, sum(b for _, b in tvs)):.2f}")
    print("\n## RG45r: el duelo de cada muerte (del radar: cuerpo · recursos · vínculo; y lo que daba el reparto de antes, 0,15 · 0,25 · 0,6 del vínculo)\n\n| mundo | por quién | muertes vistas | del radar (media) | suma | antes (media) | suma antes |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        D = [x for s in SEM for x in (by[("RG45r", mu, s)].get("duelos") or [])]
        for h_, nom in ((True, "la hermana"), (False, "una vecina")):
            X = [x for x in D if x["hermana"] == h_]
            if not X: continue
            m3 = {k: sum(x["w3"][k] for x in X) / len(X) for k in ("cuerpo", "recursos", "vinculo")}; a3 = {k: sum(x["antes"][k] for x in X) / len(X) for k in ("cuerpo", "recursos", "vinculo")}
            print(f"| {mu} | {nom} | {len(X)} | {m3['cuerpo']:.3f} · {m3['recursos']:.3f} · {m3['vinculo']:.3f} | {sum(m3.values()):.3f} | {a3['cuerpo']:.3f} · {a3['recursos']:.3f} · {a3['vinculo']:.3f} | {sum(a3.values()):.3f} |")

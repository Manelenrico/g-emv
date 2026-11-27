"""[P8] Prompt 92 (diagnóstico, solo mirar), de las partidas de cierre (valle_taller_v46: RG46r y RG046r con los sabores; el tonto, del experimento; 40 días,
semillas 1001-1021), en los cinco mundos:
  1. dormir fuera de casa: de los turnos de noche dormida, dónde (su casa, otra casa, fuera y en qué terreno), junto a quién (la hermana, una vecina, sola), a qué
     distancia andando de su casa y con cuánto cansancio se duerme (el turno en que empieza a dormir esa noche); y lo que cuesta: golpes de la bestia y robos a
     las dormidas fuera, y muertes de noche fuera; y lo que cree al acabar de dormir fuera (fin.json: cree «dormir|fuera»);
  2. los empujones entre criaturas: quién empuja a quién (hermana, vecina), con cuánta hambre la que empuja, qué lleva la empujada, quién gana y qué suelta, y
     qué le pasa a la empujada (su hambre 100 turnos después; si muere en dos días, y de qué).
   python3 diag_v47.py -> markdown por pantalla"""
import gzip, json, os, sys
from collections import Counter
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import lanzador as L0
from jugadores import Mapa
EXP = "/Volumes/Mem G-EMV/valle_experimento"; T44 = "/Volumes/Mem G-EMV/valle_taller_v44"; T46 = "/Volumes/Mem G-EMV/valle_taller_v46"; SEM = range(1001, 1022)
CFG = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); DIA = CFG["dia"]["turnos"]; CR = CFG["criaturas"]
MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian"); JUG = ("tonto", "RG46r", "RG046r")
cheb = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])); her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
_M = {}

def mapa(s):
    if s not in _M:
        e = L0.MU.Valle(); _, inf = e.reset(seed=s); mp = inf[e.agents[0]]["mapa"]; M = Mapa(mp); ley = {v: k for k, v in mp["leyenda"].items()} if isinstance(mp.get("leyenda"), dict) else {}
        casas = {k: {tuple(c) for c in v["celdas"]} for k, v in mp["casas"].items()}
        _M[s] = (M, casas, {k: M.distancias(sorted(v)) for k, v in casas.items()}, mp["leyenda"])
    return _M[s]

def ruta(v, mu, s):
    if v == "tonto": return os.path.join(T44 if mu == "bestias_crian" else EXP, f"{v}_{mu}_s{s}_d40")
    return os.path.join(T46, f"{v}_{mu}+sabores_s{s}_d40")

def una(arg):
    v, mu, s = arg; d = ruta(v, mu, s); M, CASAS, DC, ley = mapa(s); TODAS = {c: k for k, v_ in CASAS.items() for c in v_}
    fin = json.load(open(os.path.join(d, "fin.json"))); C = Counter(); E = Counter(); prev = None; L = [json.loads(l) for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8")]
    dist = Counter(); cans = []; empuj = []
    for i, x in enumerate(L):
        noche = x["fase"] == "noche"
        for a, g in x["agentes"].items():
            if g["cuerpo"]["muerta"]: continue
            p = tuple(g["pos"]); dorm = bool(g["cuerpo"].get("dormida"))
            if noche and dorm:
                k = "su casa" if TODAS.get(p) == a[0] else ("otra casa" if p in TODAS else "fuera")
                C["dorm"] += 1; C["dorm|" + k] += 1
                if k == "fuera":
                    C["fuera|" + str(M.T[p[1]][p[0]])] += 1
                    jun = [y for y, gy in x["agentes"].items() if y != a and not gy["cuerpo"]["muerta"] and cheb(p, tuple(gy["pos"])) <= 1]
                    C["fuera_junto|" + ("hermana" if her(a) in jun else ("vecina" if jun else "sola"))] += 1
                    dc = DC[a[0]].get(p); dist[min(30, dc // 5 * 5) if dc is not None else "?"] += 1
                pd = prev["agentes"].get(a) if prev else None
                if pd and not pd["cuerpo"].get("dormida"): cans.append((k, g["cuerpo"]["cansancio"], g["cuerpo"]["hambre"]))
            if g.get("accion") == "empujar" and g.get("objetivo") and not str(g["objetivo"]).startswith("bestia") and not str(g.get("resultado", "")).startswith("no:") and prev:
                b = g["objetivo"]; pb = prev["agentes"].get(b) or {}; pa = prev["agentes"].get(a) or {}
                ev = next((e for e in x["eventos"] if e.get("empujon") == a and e.get("a") == b), {})
                j = min(len(L) - 1, i + 100); hb = L[j]["agentes"].get(b, {}).get("cuerpo", {})
                mb = next((m for m in fin["muertes"] if m["criatura"] == b), None)
                empuj.append({"hermana": b == her(a), "hambre": (pa.get("cuerpo") or {}).get("hambre"), "lleva_b": (pb.get("bolsa") or []).count("comida"), "lleva_a": (pa.get("bolsa") or []).count("comida"),
                              "gana": "ella" if ev.get("gana") == a else ("la otra" if ev.get("gana") == b else "nadie"), "soltado": len(ev.get("soltado") or []),
                              "hb_luego": hb.get("hambre"), "hb_antes": (pb.get("cuerpo") or {}).get("hambre"), "b_muere_2d": bool(mb and 0 <= mb["turno"] - x["turno"] <= 2 * DIA), "b_causa": mb["causa"] if mb else None})
        for e in x["eventos"]:
            if "bestia_pega" in e or "bestia_roba" in e:
                y = e.get("bestia_pega") or e.get("bestia_roba"); gy = x["agentes"].get(y) or {}; py = tuple(gy.get("pos") or (0, 0))
                ya_dorm = bool(prev and (prev["agentes"].get(y) or {}).get("cuerpo", {}).get("dormida"))
                if ya_dorm and py not in TODAS: E["pega" if "bestia_pega" in e else "roba"] += 1
            if "muere" in e and noche:
                y = e["muere"]; gy = x["agentes"].get(y) or {}
                if tuple(gy.get("pos") or (0, 0)) not in TODAS: E["muere_noche_fuera|" + str(e.get("causa"))] += 1
        prev = x
    cree = [c_.get("cree", {}).get("dormir|fuera") for c_ in (fin.get("criaturas") or {}).values() if isinstance(c_, dict) and isinstance(c_.get("cree"), dict)]
    return {"v": v, "mu": mu, "s": s, "C": dict(C), "E": dict(E), "dist": dict(dist), "cans": cans, "emp": empuj, "cree": [c_ for c_ in cree if c_ is not None], "ley": ley}


if __name__ == "__main__":
    with Pool(8) as p: R = p.map(una, [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM])
    by = {}
    for r in R: by.setdefault((r["v"], r["mu"]), []).append(r)
    ley = R[0]["ley"]; nom = {v: k for k, v in ley.items()} if isinstance(ley, dict) else {}
    pc = lambda a, b: f"{100 * a / b:.0f} %" if b else "—"
    print("## 1. Dormir de noche: dónde, junto a quién, a qué distancia, con cuánto cansancio, y lo que cuesta (21 partidas por jugador y mundo)\n")
    print(f"(terrenos: {nom})\n\n| mundo | jugador | de lo dormido: su casa · otra casa · fuera | fuera, en qué terreno | fuera: junto a la hermana · a una vecina · sola | fuera: a ≤4 pasos de casa · 5-9 · 10-19 · ≥20 | cansancio al dormirse: en casa · fuera | dormidas fuera: golpes · robos de la bestia (por partida) | muertes de noche fuera |\n|---|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            Lr = by[(v, mu)]; C = sum((Counter(r["C"]) for r in Lr), Counter()); E = sum((Counter(r["E"]) for r in Lr), Counter()); D = sum((Counter(r["dist"]) for r in Lr), Counter())
            ca = [c for r in Lr for c in r["cans"]]; m = lambda X: sum(X) / len(X) if X else float("nan")
            ter = ", ".join(f"{nom.get(t, t)} {pc(n, C['dorm|fuera'])}" for t, n in sorted(((k.split("|")[1], n) for k, n in C.items() if k.startswith("fuera|") and not k.startswith("fuera_junto")), key=lambda z: -z[1])[:4])
            dd = lambda a, b: sum(n for k, n in D.items() if k != "?" and a <= k < b)
            df = sum(n for k, n in D.items() if k != "?") or 1
            mue = sum(n for k, n in E.items() if k.startswith("muere_noche_fuera"))
            print(f"| {mu} | {v} | {pc(C['dorm|su casa'], C['dorm'])} · {pc(C['dorm|otra casa'], C['dorm'])} · {pc(C['dorm|fuera'], C['dorm'])} | {ter or '—'} | "
                  f"{pc(C['fuera_junto|hermana'], C['dorm|fuera'])} · {pc(C['fuera_junto|vecina'], C['dorm|fuera'])} · {pc(C['fuera_junto|sola'], C['dorm|fuera'])} | "
                  f"{pc(dd(0, 5), df)} · {pc(dd(5, 10), df)} · {pc(dd(10, 20), df)} · {pc(dd(20, 99), df)} | {m([c for k, c, h in ca if k == 'su casa']):.0f} · {m([c for k, c, h in ca if k == 'fuera']):.0f} | "
                  f"{E['pega'] / 21:.2f} · {E['roba'] / 21:.2f} | {mue} {dict((k.split('|')[1], n) for k, n in E.items() if k.startswith('muere_noche_fuera'))} |")
    print("\nLo que creen al acabar de dormir fuera (cuerpo, fin.json), RG46r y RG046r: " + "; ".join(f"{v} {mu}: {sum(c for r in by[(v, mu)] for c in r['cree']) / max(1, sum(len(r['cree']) for r in by[(v, mu)])):.2f}" for v in ("RG46r", "RG046r") for mu in MUNDOS))
    print("\n## 2. Los empujones entre criaturas (RG46r y RG046r; el tonto no empuja)\n\n| mundo | jugador | por partida | a la hermana | hambre de la que empuja (mediana) | la empujada lleva comida | gana la que empuja · la otra · nadie | suelta algo | la empujada: hambre antes → 100 turnos después (media) | la empujada muere en 2 días (de hambre) |\n|---|---|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("RG46r", "RG046r"):
            X = [e for r in by[(v, mu)] for e in r["emp"]]; n = len(X)
            if not n: continue
            hs = sorted(e["hambre"] for e in X if e["hambre"] is not None); g = Counter(e["gana"] for e in X)
            ha = [e["hb_antes"] for e in X if e["hb_antes"] is not None and e["hb_luego"] is not None]; hl = [e["hb_luego"] for e in X if e["hb_antes"] is not None and e["hb_luego"] is not None]
            print(f"| {mu} | {v} | {n / 21:.0f} | {pc(sum(e['hermana'] for e in X), n)} | {hs[len(hs) // 2]:.0f} | {pc(sum(1 for e in X if e['lleva_b'] > 0), n)} | {pc(g['ella'], n)} · {pc(g['la otra'], n)} · {pc(g['nadie'], n)} | "
                  f"{pc(sum(1 for e in X if e['soltado'] > 0), n)} | {sum(ha) / len(ha):.0f} → {sum(hl) / len(hl):.0f} | {sum(e['b_muere_2d'] for e in X)} ({sum(1 for e in X if e['b_muere_2d'] and e['b_causa'] == 'hambre')}) |")

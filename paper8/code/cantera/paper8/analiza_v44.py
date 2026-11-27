"""[P8] Prompt 89, del registro del mundo (40 días):
  - punto 3: el tonto y el recolector en «bestias_crian» (semillas 1001-1040), frente al normal y a la bestia de día de siempre (las del experimento): vivas y de
    qué mueren;
  - punto 4: RG44r frente a RG43r, en «normal+sabores» y «bestias_crian+sabores» (semillas 1001-1021): cuántas veces empujan o pegan a una bestia (y con qué
    resultado), cuántas veces la echan y la matan, quién se une (en cada turno con empujones o golpes a una bestia: sola, con la hermana, con vecinas), golpes
    y robos de las bestias, vivas y muertes de hambre (pareadas por semilla).
   python3 analiza_v44.py -> markdown por pantalla"""
import gzip, json, os, random
from collections import Counter
from multiprocessing import Pool
EXP = "/Volumes/Mem G-EMV/valle_experimento"; T44 = "/Volumes/Mem G-EMV/valle_taller_v44"; NB = 10000
her = lambda a: a[0] + ("2" if a[1] == "1" else "1")

def quien(grupo):
    """quién va junta en un turno: sola, con la hermana, con vecinas (de otras casas), o con las dos"""
    if len(grupo) == 1: return "sola"
    casas = {a[0] for a in grupo}; hermanas = any(her(a) in grupo for a in grupo)
    if len(casas) == 1: return "con la hermana"
    return "con la hermana y vecinas" if hermanas else "con vecinas"

def una(arg):
    v, mu, s, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d40"); fin = json.load(open(os.path.join(d, "fin.json")))
    C = Counter(); grupos = Counter()
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        L = json.loads(l); por = {}
        for a, g in L["agentes"].items():
            ob = str(g.get("objetivo") or "")
            if g.get("accion") in ("empujar", "golpear") and ob.startswith("bestia"):
                C[g["accion"]] += 1; r = str(g.get("resultado", ""))
                C[g["accion"] + "|" + ("no pegada" if r.startswith("no:") else r.split(" (")[0])] += 1
                if not r.startswith("no:"): por.setdefault((ob, g["accion"]), set()).add(a)
        for (ob, ac), gr in por.items(): grupos[ac + "|" + quien(gr)] += 1; grupos[ac + "|n=" + str(len(gr))] += 1
        for e in L["eventos"]:
            for k in ("bestia_echada", "bestia_muere", "bestia_pega", "bestia_roba", "bestia_suelta", "bestia_nace"):
                if k in e: C[k] += 1
    return {"v": v, "mu": mu, "s": s, "vivas": 8 - len(fin["muertes"]), "causas": Counter(m["causa"] if m["causa"] in ("hambre", "bestia", "terreno") else "otras" for m in fin["muertes"]),
            "C": dict(C), "grupos": dict(grupos)}

def boot(d):
    x = [d[s] for s in sorted(d)]; n = len(x); r = random.Random(8)
    m = sorted(sum(x[r.randrange(n)] for _ in range(n)) / n for _ in range(NB)); return f"{sum(x) / n:+.2f} [{m[int(0.025 * NB)]:+.2f}, {m[int(0.975 * NB) - 1]:+.2f}]"


if __name__ == "__main__":
    S3 = range(1001, 1041); S4 = range(1001, 1022)
    T = [(v, mu, s, EXP) for v in ("tonto", "recolector") for mu in ("normal", "bestia_dia") for s in S3] + [(v, "bestias_crian", s, T44) for v in ("tonto", "recolector") for s in S3]
    T += [(v, mu, s, T44) for v in ("RG43r", "RG44r") for mu in ("normal+sabores", "bestias_crian+sabores") for s in S4]
    with Pool(8) as p: R = p.map(una, T)
    by = {(r["v"], r["mu"], r["s"]): r for r in R}
    print("## Punto 3: el tonto y el recolector en «bestias que crían» (40 días, semillas 1001-1040)\n\n| jugador | mundo | vivas al día 40 (de 8) | % | muertes: hambre · bestia · terreno · otras | golpes · robos de las bestias por partida |\n|---|---|---|---|---|---|")
    for v in ("tonto", "recolector"):
        for mu in ("normal", "bestia_dia", "bestias_crian"):
            L = [by[(v, mu, s)] for s in S3]; c = Counter()
            for r in L: c.update(r["causas"])
            vi = sum(r["vivas"] for r in L) / len(L)
            print(f"| {v} | {mu} | {vi:.2f} | {100 * vi / 8:.0f} % | {c['hambre']} · {c['bestia']} · {c['terreno']} · {c['otras']} | "
                  f"{sum(r['C'].get('bestia_pega', 0) for r in L) / len(L):.1f} · {sum(r['C'].get('bestia_roba', 0) for r in L) / len(L):.1f} |")
    print("\n## Punto 4: RG44r frente a RG43r (40 días, semillas 1001-1021)\n\n| mundo | clase | vivas al día 40 | muertes de hambre · bestia | empujones a una bestia (ganados) · golpes a una bestia | echadas | muertas | golpes · robos de las bestias | bestias nacidas |\n|---|---|---|---|---|---|---|---|---|")
    for mu in ("normal+sabores", "bestias_crian+sabores"):
        for v in ("RG43r", "RG44r"):
            L = [by[(v, mu, s)] for s in S4]; C = Counter(); c = Counter()
            for r in L: C.update(r["C"]); c.update(r["causas"])
            n = len(L)
            print(f"| {mu} | {v} | {sum(r['vivas'] for r in L) / n:.2f} | {c['hambre']} · {c['bestia']} | {C['empujar'] / n:.2f} ({C['empujar|gana'] / n:.2f}) · {C['golpear'] / n:.2f} | "
                  f"{C['bestia_echada'] / n:.2f} | {C['bestia_muere'] / n:.2f} | {C['bestia_pega'] / n:.1f} · {C['bestia_roba'] / n:.1f} | {C['bestia_nace'] / n:.1f} |")
        print(f"| {mu} | RG44r − RG43r, vivas | {boot({s: by[('RG44r', mu, s)]['vivas'] - by[('RG43r', mu, s)]['vivas'] for s in S4})} | | | | | | |")
    print("\nTotales en las 21 partidas de cada una (empujones y golpes a una bestia, por resultado; y en cada turno con empujones o golpes a una misma bestia, quién va junta):\n")
    for mu in ("normal+sabores", "bestias_crian+sabores"):
        for v in ("RG43r", "RG44r"):
            C = Counter(); G = Counter()
            for s in S4: C.update(by[(v, mu, s)]["C"]); G.update(by[(v, mu, s)]["grupos"])
            res = {k: n for k, n in C.items() if "|" in k}
            print(f"- {mu}, {v}: resultados {dict(sorted(res.items()))}; turnos por grupo {dict(sorted(G.items()))}; echadas {C['bestia_echada']}, muertas {C['bestia_muere']}, sueltan lo robado {C['bestia_suelta']}")

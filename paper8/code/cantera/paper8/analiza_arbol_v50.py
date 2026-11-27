"""[P8] Prompt 96, punto B.6: el árbol de fruta dulce en las partidas de prueba (valle_prueba_v51: RG50r con los sabores, el tonto y el recolector; normal y sequía con
el árbol, semillas 9001-9003, 40 días), del registro del mundo y de arbol.json:
  - quién lo descubre y cuándo (la primera vez que tiene un árbol activo a la vista de la fase);
  - cada recogida (coger con éxito junto a un árbol activo): cuándo salió de cerca de casa (la última vez a 5 casillas o menos de una celda de su casa) y cuándo
    volvió, y si volvió antes de la noche; si iba sola o con otras (a 3 casillas o menos);
  - la fruta dulce (con los sabores, origen «dulce»): dónde se la comen (a 8 casillas o menos del árbol, de su casa, o en otro sitio), a quién la dan;
  - lo que le quita la bestia en el árbol (arbol.json, roba_dulce);
  - las noches con un árbol activo frente a las demás: turnos de bestia cerca de la aldea (a 8 casillas o menos de alguna casa) y golpes y robos allí, por noche.
   python3 analiza_arbol_v50.py -> markdown por pantalla y salida/arbol_viajes_v50.json (los viajes, para el GIF)"""
import gzip, json, os
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
CFG = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); VF = CFG["criaturas"]["vista_por_fase"]; DIA = CFG["dia"]["turnos"]
CASA = defaultdict(set)
for c in CFG["mapa"]["casas"]:
    for dx in range(3):
        for dy in range(3): CASA[c["id"]].add((c["x0"] + dx, c["y0"] + dy))
TODAS = set().union(*CASA.values()); P51 = "/Volumes/Mem G-EMV/valle_prueba_v51"
cheb = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])); her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
dcasa = lambda a, p: min(cheb(p, q) for q in CASA[a[0]])
JUEGOS = [("RG50r", mu + "+sabores+arbol") for mu in ("normal", "sequia")] + [(v, mu + "+arbol") for v in ("tonto", "recolector") for mu in ("normal", "sequia")]

def una(arg):
    v, mu, s = arg; d = os.path.join(P51, f"{v}_{mu}_s{s}_d40"); L = [json.loads(l) for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt")]
    AR = json.load(open(os.path.join(d, "arbol.json"))) if os.path.exists(os.path.join(d, "arbol.json")) else {}
    fin = json.load(open(os.path.join(d, "fin.json"))); C = Counter(); desc = {}; recog = []; noches = defaultdict(Counter)
    for i, x in enumerate(L):
        act = [(a_[0], a_[1]) for a_ in (x.get("arboles") or []) if a_[2] is not None]; t = x["turno"]
        if x["fase"] == "noche":
            k = "con" if act else "sin"; noches[(x["turno"] // DIA, k)]["turnos"] += 1
            for b in (x.get("bestias") or [x["bestia"]]):
                if b.get("pos") and min(cheb(tuple(b["pos"]), q) for q in TODAS) <= 8: noches[(x["turno"] // DIA, k)]["bestia_aldea"] += 1
            for e in x["eventos"]:
                y = e.get("bestia_pega") or e.get("bestia_roba")
                if y and y in x["agentes"] and min(cheb(tuple(x["agentes"][y]["pos"]), q) for q in TODAS) <= 8: noches[(x["turno"] // DIA, k)]["ataques_aldea"] += 1
        for a, g in x["agentes"].items():
            if g["cuerpo"]["muerta"]: continue
            p = tuple(g["pos"])
            for q in act:
                if a not in desc and cheb(p, q) <= VF[x["fase"]]: desc[a] = t
            if g.get("accion") == "coger" and g.get("resultado") == "ok" and g.get("de") == "matorral" and any(cheb(p, q) <= 1 for q in act) and i > 0:
                q = next(q for q in act if cheb(p, q) <= 1); j0 = next((j for j in range(i, -1, -1) if a in L[j]["agentes"] and dcasa(a, tuple(L[j]["agentes"][a]["pos"])) <= 5), None)
                j1 = next((j for j in range(i, len(L)) if a in L[j]["agentes"] and not L[j]["agentes"][a]["cuerpo"]["muerta"] and dcasa(a, tuple(L[j]["agentes"][a]["pos"])) <= 5), None)
                otras = [y for y, gy in x["agentes"].items() if y != a and not gy["cuerpo"]["muerta"] and cheb(p, tuple(gy["pos"])) <= 3]
                recog.append({"a": a, "t": t, "arbol": list(q), "sale": L[j0]["turno"] if j0 is not None else None, "vuelve": L[j1]["turno"] if j1 is not None else None,
                              "fase_vuelve": L[j1]["fase"] if j1 is not None else None, "con": otras, "muere_antes_de_volver": j1 is None})
            o = g.get("origen")
            if g.get("accion") == "comer" and g.get("resultado") == "ok" and o == "dulce":
                at = [q for q in [(z[0], z[1]) for z in (x.get("arboles") or [])]]
                C["come_dulce|" + ("en el árbol" if any(cheb(p, q) <= 8 for q in at) else ("en casa o cerca" if dcasa(a, p) <= 8 else "en otro sitio"))] += 1
            if g.get("accion") == "dar" and g.get("resultado") == "ok" and o == "dulce":
                ob = g.get("objetivo"); fl = (L[i - 1]["agentes"].get(ob) or {}).get("cuerpo", {}).get("hambre", 0) > CFG["criaturas"]["umbral_flaca"] if i else False
                C["da_dulce|" + ("hermana" if ob == her(a) else "vecina")] += 1; C["da_dulce_flaca"] += fl
    return {"v": v, "mu": mu, "s": s, "vivas": 8 - len(fin["muertes"]), "AR": AR, "desc": desc, "recog": recog, "C": dict(C), "noches": {f"{k[0]}|{k[1]}": dict(c) for k, c in noches.items()}}


if __name__ == "__main__":
    with Pool(8) as p: R = p.map(una, [(v, mu, s) for v, mu in JUEGOS for s in (9001, 9002, 9003)])
    json.dump([{k: r[k] for k in ("v", "mu", "s", "recog")} for r in R], open(os.path.join(AQUI, "salida", "arbol_viajes_v50.json"), "w"), ensure_ascii=False)
    print("| jugador | mundo | vivas (de 8, media) | apariciones · frutas puestas · perdidas sin coger | lo descubren (criaturas; primer día mediano) | recogidas (criaturas distintas) | vuelven antes de la noche · de noche · no vuelven | solas · con otras | la bestia va al árbol (noches) · le quita la dulce en el árbol | se comen la dulce: en el árbol · en casa o cerca · en otro sitio | dan la dulce: a la hermana · a una vecina (a quien estaba flaca) |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for v, mu in JUEGOS:
        X = [r for r in R if r["v"] == v and r["mu"] == mu]; AR = Counter(); C = Counter()
        for r in X:
            for k in ("aparece", "frutos_puestos", "frutos_se_pierden", "roba_dulce", "bestia_va"): AR[k] += r["AR"].get(k, 0)
            C.update(r["C"])
        ds = sorted(t // DIA for r in X for t in r["desc"].values()); rc = [z for r in X for z in r["recog"]]
        quien = {(r["s"], z["a"]) for r in X for z in r["recog"]}
        antes = sum(1 for z in rc if z["fase_vuelve"] in ("mañana", "tarde")); noche = sum(1 for z in rc if z["fase_vuelve"] in ("anochecer", "noche")); nov = sum(1 for z in rc if z["muere_antes_de_volver"])
        print(f"| {v} | {mu.split('+')[0]} | {sum(r['vivas'] for r in X) / len(X):.2f} | {AR['aparece']} · {AR['frutos_puestos']} · {AR['frutos_se_pierden']} | {len(ds)} ({ds[len(ds) // 2] if ds else '—'}) | {len(rc)} ({len(quien)}) | "
              f"{antes} · {noche} · {nov} | {sum(1 for z in rc if not z['con'])} · {sum(1 for z in rc if z['con'])} | {AR['bestia_va']} · {AR['roba_dulce']} | "
              f"{C['come_dulce|en el árbol']} · {C['come_dulce|en casa o cerca']} · {C['come_dulce|en otro sitio']} | {C['da_dulce|hermana']} · {C['da_dulce|vecina']} ({C['da_dulce_flaca']}) |")
    print("\n## Las noches con un árbol activo frente a las demás (por noche: turnos de bestia a 8 casillas o menos de una casa · golpes y robos allí)\n\n| jugador | mundo | noches con árbol: bestia cerca de la aldea · ataques | noches sin árbol: lo mismo |\n|---|---|---|---|")
    for v, mu in JUEGOS:
        X = [r for r in R if r["v"] == v and r["mu"] == mu]; A = defaultdict(Counter)
        for r in X:
            for k, c in r["noches"].items(): A[k.split("|")[1]]["noches"] += 1; A[k.split("|")[1]].update(c)
        f = lambda k: f"{A[k]['bestia_aldea'] / max(1, A[k]['noches']):.1f} · {A[k]['ataques_aldea'] / max(1, A[k]['noches']):.2f} ({A[k]['noches']} noches)"
        print(f"| {v} | {mu.split('+')[0]} | {f('con')} | {f('sin')} |")

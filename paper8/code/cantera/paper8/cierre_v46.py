"""[P8] Prompt 91, punto 3: la tabla de cierre con los criterios de Manel, del registro del mundo (40 días, semillas 1001-1021), para RG46r y RG046r (con los sabores)
y el tonto y el recolector (los mismos mundos, sin sabores: no comen distinto), en abundancia, normal, sequía, sequía dura y «bestias que crían»:
  - vivas al día 40 (de 8) y de qué mueren;
  - pelearse sí, matarse no: empujones y golpes entre criaturas, y muertes por golpe de otra;
  - dormir de noche y dónde: de los turnos de noche vivas, cuántos duerme, y dónde está (su casa, otra casa, fuera);
  - dar a quien lo necesita y guardar: comidas y medicinas dadas (a quien estaba flaca o herida el turno antes; a la hermana o a una vecina; de qué origen la
    comida) y lo dejado en la despensa o el almacén;
  - las conductas: con la bestia a la vista y fuera de casa, con otra pegada; echadas y muertas de la bestia, y quién va junta; tras perder a la hermana, la
    parte del día pegada a una vecina (5 días antes, 5 después).
   python3 cierre_v46.py -> markdown por pantalla"""
import gzip, json, os, sys
from collections import Counter
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import analiza_v44 as A44
EXP = "/Volumes/Mem G-EMV/valle_experimento"; T44 = "/Volumes/Mem G-EMV/valle_taller_v44"; T46 = "/Volumes/Mem G-EMV/valle_taller_v46"; SEM = range(1001, 1022)
CFG = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); CR = CFG["criaturas"]; VF = CR["vista_por_fase"]; DIA = CFG["dia"]["turnos"]
CASA = {}
for c in CFG["mapa"]["casas"]:
    for dx in range(3):
        for dy in range(3): CASA[(c["x0"] + dx, c["y0"] + dy)] = c["id"]
cheb = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])); her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian"); JUG = ("tonto", "recolector", "RG46r", "RG046r")

def ruta(v, mu, s):
    if v in ("tonto", "recolector"): return os.path.join(T44 if mu == "bestias_crian" else EXP, f"{v}_{mu}_s{s}_d40")
    return os.path.join(T46, f"{v}_{mu}+sabores_s{s}_d40")

def una(arg):
    v, mu, s = arg; d = ruta(v, mu, s); fin = json.load(open(os.path.join(d, "fin.json"))); C = Counter(); dar = Counter(); prev = None
    viva = lambda L, a: a in L["agentes"] and not L["agentes"][a]["cuerpo"]["muerta"]; muere_her = {}; cerca = {}
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        L = json.loads(l); t = L["turno"]; dia = t // DIA; bs = [tuple(b["pos"]) for b in (L.get("bestias") or [L["bestia"]]) if b.get("pos") is not None]
        for a, g in L["agentes"].items():
            if g["cuerpo"]["muerta"]: continue
            p = tuple(g["pos"]); ac = g.get("accion"); ob = g.get("objetivo"); res = str(g.get("resultado", ""))
            if ac in ("empujar", "golpear") and ob and not str(ob).startswith("bestia") and not res.startswith("no:"): C[ac] += 1
            if L["fase"] == "noche":
                C["noche"] += 1; C["noche_duerme"] += bool(g["cuerpo"].get("dormida"))
                k = "su casa" if CASA.get(p) == a[0] else ("otra casa" if p in CASA else "fuera"); C["noche_" + k] += 1
            if ac == "dejar" and res == "ok" and g.get("en") in ("despensa", "almacen"): C["deja_" + g["en"]] += 1
            if ac == "dejar" and res == "ok": C["deja_ok"] += 1
            if ac == "dar" and res == "ok" and prev is not None and ob in prev["agentes"]:
                cb = prev["agentes"][ob]["cuerpo"]; tp = g.get("tipo")
                nec = (tp == "comida" and cb["hambre"] > CR["umbral_flaca"]) or (tp != "comida" and cb["vida"] < CR["umbral_herida"])
                dar[f"{tp}|{'hermana' if ob == her(a) else 'vecina'}|{'necesita' if nec else 'no'}|{g.get('origen') or '-'}"] += 1
            if p not in CASA and bs:
                if any(cheb(p, b) <= VF[L["fase"]] for b in bs):
                    C["bestia_vista"] += 1; C["bestia_vista_junta"] += any(y != a and not gy["cuerpo"]["muerta"] and cheb(p, tuple(gy["pos"])) <= 1 for y, gy in L["agentes"].items())
            h = her(a)
            if h in L["agentes"] and not viva(L, h) and a not in muere_her: muere_her[a] = dia
            x = cerca.setdefault(a, {}).setdefault(dia, [0, 0]); x[1] += 1
            x[0] += any(y[0] != a[0] and not gy["cuerpo"]["muerta"] and cheb(p, tuple(gy["pos"])) <= 1 for y, gy in L["agentes"].items())
        prev = L
    causas = Counter("golpe" if str(m["causa"]).startswith("golpe") else m["causa"] for m in fin["muertes"])
    rec = []
    for a, d0 in muere_her.items():
        antes = [cerca[a][k][0] / cerca[a][k][1] for k in range(max(0, d0 - 5), d0) if k in cerca[a]]; desp = [cerca[a][k][0] / cerca[a][k][1] for k in range(d0 + 1, d0 + 6) if k in cerca[a]]
        if antes and len(desp) >= 3: rec.append((sum(antes) / len(antes), sum(desp) / len(desp)))
    b = A44.una((v, mu + ("+sabores" if v.startswith("RG") else ""), s, os.path.dirname(d)))
    return {"v": v, "mu": mu, "s": s, "vivas": 8 - len(fin["muertes"]), "causas": dict(causas), "C": dict(C), "dar": dict(dar), "rec": rec, "b": b}


if __name__ == "__main__":
    with Pool(8) as p: R = p.map(una, [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM])
    by = {}
    for r in R: by.setdefault((r["v"], r["mu"]), []).append(r)
    pc = lambda a, b: f"{100 * a / b:.0f} %" if b else "—"
    print("## Vivas y de qué mueren (21 partidas por jugador y mundo)\n\n| mundo | tonto | recolector | RG46r | RG046r | muertes RG46r: hambre · bestia · golpe · terreno | RG046r |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        f = lambda v: sum(r["vivas"] for r in by[(v, mu)]) / 21
        cs = lambda v: (lambda c: f"{c['hambre']} · {c['bestia']} · {c['golpe']} · {c['terreno']}")(sum((Counter(r["causas"]) for r in by[(v, mu)]), Counter()))
        print(f"| {mu} | {f('tonto'):.2f} | {f('recolector'):.2f} | {f('RG46r'):.2f} | {f('RG046r'):.2f} | {cs('RG46r')} | {cs('RG046r')} |")
    print("\n## Pelearse, dormir, dar y guardar (por partida, o en % de los turnos)\n\n| mundo | jugador | empujones · golpes a otras | muertes por golpe | de noche: duerme · en su casa · otra casa · fuera | comidas dadas (a quien lo necesitaba) · medicinas dadas (ídem) | dejadas: despensa · almacén |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            L = by[(v, mu)]; C = sum((Counter(r["C"]) for r in L), Counter()); D = sum((Counter(r["dar"]) for r in L), Counter()); c = sum((Counter(r["causas"]) for r in L), Counter())
            com = sum(n for k, n in D.items() if k.startswith("comida|")); comn = sum(n for k, n in D.items() if k.startswith("comida|") and "|necesita|" in k)
            med = sum(n for k, n in D.items() if not k.startswith("comida|")); medn = sum(n for k, n in D.items() if not k.startswith("comida|") and "|necesita|" in k)
            print(f"| {mu} | {v} | {C['empujar'] / 21:.1f} · {C['golpear'] / 21:.1f} | {c['golpe']} | {pc(C['noche_duerme'], C['noche'])} · {pc(C['noche_su casa'], C['noche'])} · {pc(C['noche_otra casa'], C['noche'])} · {pc(C['noche_fuera'], C['noche'])} | "
                  f"{com / 21:.1f} ({pc(comn, com)}) · {med / 21:.2f} ({pc(medn, med)}) | {C['deja_despensa'] / 21:.1f} · {C['deja_almacen'] / 21:.1f} |")
    print("\n## Las conductas (RG46r y RG046r; el tonto y el recolector no dan, no empujan ni pegan)\n\n| mundo | jugador | con la bestia a la vista (fuera), con otra pegada | echadas · muertas (en 21 partidas) | echan: con la hermana · con vecinas | comida dada: a la hermana · a una vecina · del huerto (llevando de las dos, …) | tras perder a la hermana, pegada a una vecina: antes · 5 días después (casos) |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            L = by[(v, mu)]; C = sum((Counter(r["C"]) for r in L), Counter()); D = sum((Counter(r["dar"]) for r in L), Counter())
            B = sum((Counter(r["b"]["C"]) for r in L), Counter()); G = sum((Counter(r["b"]["grupos"]) for r in L), Counter()); rec = [x for r in L for x in r["rec"]]
            ch = sum(n for k, n in D.items() if k.startswith("comida|hermana")); cv = sum(n for k, n in D.items() if k.startswith("comida|vecina")); hu = sum(n for k, n in D.items() if k.startswith("comida|") and k.endswith("|huerto"))
            m = lambda X: sum(X) / len(X) if X else float("nan")
            print(f"| {mu} | {v} | {pc(C['bestia_vista_junta'], C['bestia_vista'])} | {B['bestia_echada']} · {B['bestia_muere']} | {G['empujar|con la hermana']} · {G['empujar|con vecinas'] + G['empujar|con la hermana y vecinas']} | "
                  f"{ch} · {cv} · {pc(hu, ch + cv)} | {100 * m([a for a, _ in rec]):.0f} % · {100 * m([b for _, b in rec]):.0f} % ({len(rec)}) |")

"""[P8] Prompt 107: la tabla de cierre v5. Jugadores: RG55r y RG055r (valle_cierre_v5), RG50r, el tonto y el recolector (valle_taller_v52, comprobados idénticos con el
código de ahora: puerta_cierre_v5.json); el árbol encendido en los cinco mundos; semillas 1001-1021; 40 días. Para que los análisis del cierre (cierre_v46, diag_v47,
diag_robos_v47, verdad_noche_v49, analiza_arbol_v50) sirvan sin tocarlos, una carpeta de vista, valle_cierre_v5_vista, con enlaces simbólicos a las partidas (no
copia ni cambia nada). Los cálculos de siempre son los de cierre_v52 (importados con la carpeta cambiada); lo nuevo:
  - dormir (la primera vez de cada noche, cada criatura): dentro de su casa · en una puerta · en otra casa · fuera;
  - dar (registro del mundo, con éxito): por partida, a la hermana · a una vecina · a una que le robó antes (hermana · vecina); qué comida (el origen: huerto, bosque,
    dulce, sin origen) y medicina;
  - dar la última comida: cuántas veces, con cuánta hambre propia y de la que recibe;
  - los regalos a la hermana solo por el gesto (RG55r, registro de la foto: los regalos hechos, sin las decisiones de dormir de un tirón; ni alivio ni gusto);
  - las diferencias de vivas por semillas emparejadas (media [IC 95 %], bootstrap): RG55r − tonto, RG55r − RG055r, RG55r − RG50r.
   python3 tabla_cierre_v5.py -> cierre_v5/tabla_cierre_v5.md"""
import gzip, json, os, random, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path.insert(0, P8); sys.path.insert(0, os.path.join(P8, "medida_v3"))
import cierre_v46 as C46, diag_v47 as D47, diag_robos_v47 as R47, verdad_noche_v49 as VN, analiza_arbol_v50 as AA
T7 = "/Volumes/Mem G-EMV"; V5 = os.path.join(T7, "valle_cierre_v5"); T52 = os.path.join(T7, "valle_taller_v52"); VISTA = os.path.join(T7, "valle_cierre_v5_vista")
NUEVAS = ("RG55r", "RG055r", "RG50r"); JUG = ("tonto", "recolector") + NUEVAS; MUNDOS = C46.MUNDOS; SEM = range(1001, 1022); NB = 10000
def nombre(v, mu, s): return f"{v}_{mu}+sabores_s{s}_d40" if v.startswith("RG") else f"{v}_{mu}_s{s}_d40"
def ruta(v, mu, s): return os.path.join(VISTA, nombre(v, mu, s))
C46.ruta = ruta; D47.ruta = ruta; R47.T46 = VISTA; VN.CARP = {v: VISTA for v in NUEVAS}; AA.P51 = VISTA; C46.SEM = SEM
her = lambda a: a[0] + ("2" if a[1] == "1" else "1")

def vista():
    os.makedirs(VISTA, exist_ok=True)
    for v in JUG:
        for mu in MUNDOS:
            for s in SEM:
                n = nombre(v, mu, s); src = os.path.join(V5 if v in ("RG55r", "RG055r") else T52, n); dst = os.path.join(VISTA, n)
                if not os.path.lexists(dst): os.symlink(src, dst)

def arbol(arg):
    v, mu, s = arg; return AA.una((v, mu + "+sabores" if v.startswith("RG") else mu, s))

def guarda_dulce(arg):
    v, mu, s = arg; prev = None; n = 0
    for l in gzip.open(os.path.join(ruta(v, mu, s), "mundo.jsonl.gz"), "rt"):
        x = json.loads(l)
        for a, g in x["agentes"].items():
            if prev and g.get("accion") == "dejar" and g.get("resultado") == "ok" and g.get("en") == "despensa" and a in prev["agentes"]:
                if (prev["agentes"][a].get("bolsa_origen") or []).count("dulce") > (g.get("bolsa_origen") or []).count("dulce"): n += 1
        prev = x
    return {"v": v, "mu": mu, "s": s, "dulce_despensa": n}

def nuevo(arg):
    """dormir (dentro · puerta · otra casa · fuera), dar (a quién, a las que robaron, qué), la última comida, y (RG55r) los regalos solo por el gesto"""
    v, mu, s = arg; d = ruta(v, mu, s)
    import lanzador as L
    e = L.MU.Valle(); _, inf = e.reset(seed=s); mp = inf[e.agents[0]]["mapa"]
    casa = {k: {tuple(c) for c in w["celdas"]} for k, w in mp["casas"].items()}; puertas = {tuple(w["puerta"]) for w in mp["casas"].values()}
    C = Counter(); prev = {}; ladron = defaultdict(set); ult = []; tiron = set(); hizo = {}
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l)
        for a, g in x["agentes"].items():
            if g["cuerpo"].get("de_un_tiron"): tiron.add((x["turno"], a))
            hizo[(x["turno"], a)] = g.get("accion"); dor = bool(g["cuerpo"].get("dormida")); p = tuple(g["pos"])
            if dor and a in prev and not prev[a][3]:
                C["duerme"] += 1; C["duerme|" + ("puerta" if p in puertas else ("dentro" if p in casa[a[0]] else ("otra casa" if any(p in c for c in casa.values()) else "fuera")))] += 1
            if g.get("accion") == "dar" and g.get("resultado") == "ok" and g.get("objetivo") and a in prev:
                b = g["objetivo"]; h = b == her(a); C["da|" + ("hermana" if h else "vecina")] += 1; C["da|ladrona_" + ("hermana" if h else "vecina")] += b in ladron[a]
                tp = g.get("tipo") or "comida"
                if tp == "comida":
                    antes = Counter(prev[a][2]); antes.subtract(Counter(g.get("bolsa_origen") or [])); org = next((str(o) for o, n in antes.items() if n > 0), "?")
                    C["da_comida|" + org] += 1
                    if prev[a][0].count("comida") == 1 and b in prev: ult.append({"h": prev[a][1], "ho": prev[b][1], "hermana": h})
                else: C["da|" + tp] += 1; C["med_partida"] += 1
        for ev in x["eventos"]:
            if "empujon" in ev and ev.get("gana") and ev.get("soltado"):
                pierde = ev["a"] if ev["gana"] == ev["empujon"] else ev["empujon"]; ladron[pierde].add(ev["gana"])
        for a, g in x["agentes"].items(): prev[a] = (list(g.get("bolsa") or []), g["cuerpo"]["hambre"], list(g.get("bolsa_origen") or []), bool(g["cuerpo"].get("dormida")))
    G = Counter()
    if v == "RG55r" and os.path.exists(os.path.join(d, "fotos.jsonl.gz")):
        for l in gzip.open(os.path.join(d, "fotos.jsonl.gz"), "rt", encoding="utf-8"):
            x = json.loads(l)
            if x["e"] < 0 or (x["t"] - 1, x["a"]) in tiron or hizo.get((x["t"], x["a"])) != "dar": continue
            o = x["o"][x["e"]]
            if o[1].get("accion") != "dar": continue
            F = dict(x["o"][0][3]); F.update(o[3]) if x["e"] else None; k = "hermana" if o[1].get("a") == her(x["a"]) else "vecina"
            ali = (F.get("G-R-HERMANO-FALTA", 0) or 0) + (F.get("G-ALIVIO", 0) or 0) > 0; gus = (F.get("G-SABOR-OTRA", 0) or 0) > 0
            tp = "comida" if (o[1].get("tipo") or "comida") == "comida" else "medicina"; k = k + "|" + tp      # (por separado: comida y medicina)
            G["n|" + k] += 1; G["alivio|" + k] += ali; G["gusto|" + k] += gus; G["solo_gesto|" + k] += (not ali and not gus)
    return {"v": v, "mu": mu, "s": s, "C": dict(C), "ult": ult, "G": dict(G)}

def boot(d):
    x = [d[s] for s in sorted(d)]; n = len(x); r = random.Random(8)
    m = sorted(sum(x[r.randrange(n)] for _ in range(n)) / n for _ in range(NB)); return f"{sum(x) / n:+.2f} [{m[int(0.025 * NB)]:+.2f}, {m[int(0.975 * NB) - 1]:+.2f}]"


if __name__ == "__main__":
    vista()
    T_ = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]; TN = [(v, mu, s) for v in NUEVAS for mu in MUNDOS for s in SEM]
    with Pool(8) as p:
        RC = p.map(C46.una, T_); RD = p.map(D47.una, [(v, mu, s) for v in ("tonto",) + NUEVAS for mu in MUNDOS for s in SEM]); RR = p.map(R47.una, TN)
        RV = p.map(VN.una, TN); RA = p.map(arbol, T_); RG = p.map(guarda_dulce, TN); RN = p.map(nuevo, T_)
    W = []; out = W.append
    by = defaultdict(list)
    for r in RC: by[(r["v"], r["mu"])].append(r)
    viv = {(r["v"], r["mu"], r["s"]): r["vivas"] for r in RC}
    pc = lambda a, b: f"{100 * a / b:.0f} %" if b else "—"; m = lambda X: sum(X) / len(X) if X else float("nan"); N_ = len(SEM)
    out("## Vivas al día 40 (de 8) y de qué mueren\n\n| mundo | tonto | recolector | RG55r | RG055r | RG50r | muertes RG55r: hambre · bestia · golpe · terreno | RG055r | RG50r |\n|---|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        f = lambda v: sum(r["vivas"] for r in by[(v, mu)]) / N_
        cs = lambda v: (lambda c: f"{c['hambre']} · {c['bestia']} · {c['golpe']} · {c['terreno']}")(sum((Counter(r["causas"]) for r in by[(v, mu)]), Counter()))
        out(f"| {mu} | {f('tonto'):.2f} | {f('recolector'):.2f} | {f('RG55r'):.2f} | {f('RG055r'):.2f} | {f('RG50r'):.2f} | {cs('RG55r')} | {cs('RG055r')} | {cs('RG50r')} |")
    out("\n## Diferencia de vivas por semillas emparejadas (media [IC 95 %], bootstrap de semillas)\n\n| mundo | RG55r − tonto | RG55r − RG055r | RG55r − RG50r |\n|---|---|---|---|")
    for mu in MUNDOS:
        dd = lambda a, b: boot({s: viv[(a, mu, s)] - viv[(b, mu, s)] for s in SEM})
        out(f"| {mu} | {dd('RG55r', 'tonto')} | {dd('RG55r', 'RG055r')} | {dd('RG55r', 'RG50r')} |")
    out("\n## Pelearse, dormir, dar y guardar (los cálculos de siempre, cierre_v46)\n\n| mundo | jugador | empujones · golpes a otras (por partida) | muertes por golpe | de noche: duerme · en su casa · otra casa · fuera | comidas dadas (a quien lo necesitaba) · medicinas (ídem) | a la hermana · a una vecina (total) | dejadas: despensa · almacén |\n|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            L_ = by[(v, mu)]; C = sum((Counter(r["C"]) for r in L_), Counter()); D = sum((Counter(r["dar"]) for r in L_), Counter()); c = sum((Counter(r["causas"]) for r in L_), Counter())
            com = sum(n for k, n in D.items() if k.startswith("comida|")); comn = sum(n for k, n in D.items() if k.startswith("comida|") and "|necesita|" in k)
            med = sum(n for k, n in D.items() if not k.startswith("comida|")); medn = sum(n for k, n in D.items() if not k.startswith("comida|") and "|necesita|" in k)
            ch = sum(n for k, n in D.items() if k.startswith("comida|hermana")); cv = sum(n for k, n in D.items() if k.startswith("comida|vecina"))
            out(f"| {mu} | {v} | {C['empujar'] / N_:.1f} · {C['golpear'] / N_:.1f} | {c['golpe']} | {pc(C['noche_duerme'], C['noche'])} · {pc(C['noche_su casa'], C['noche'])} · {pc(C['noche_otra casa'], C['noche'])} · {pc(C['noche_fuera'], C['noche'])} | "
                f"{com / N_:.1f} ({pc(comn, com)}) · {med / N_:.2f} ({pc(medn, med)}) | {ch} · {cv} | {C['deja_despensa'] / N_:.1f} · {C['deja_almacen'] / N_:.1f} |")
    byn = defaultdict(list)
    for r in RN: byn[(r["v"], r["mu"])].append(r)
    out("\n## Dormir: la primera vez de cada noche (cada criatura)\n\n| mundo | jugador | noches | dentro de su casa | en una puerta | en otra casa | fuera |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            C = sum((Counter(r["C"]) for r in byn[(v, mu)]), Counter()); n = C["duerme"]
            out(f"| {mu} | {v} | {n} | {pc(C['duerme|dentro'], n)} | {pc(C['duerme|puerta'], n)} | {pc(C['duerme|otra casa'], n)} | {pc(C['duerme|fuera'], n)} |")
    out("\n## Dar (registro del mundo; por partida): a quién, a las que robaron y qué\n\n| mundo | jugador | a la hermana · a una vecina (comida y medicina) | a una que le robó antes: hermana · vecina | comida dada: huerto · bosque · dulce · sin origen | medicina: media (mediana; máximo) | regalos a la hermana solo por el gesto (RG55r): comida · medicina |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            X = byn[(v, mu)]; C = sum((Counter(r["C"]) for r in X), Counter()); G = sum((Counter(r["G"]) for r in X), Counter())
            ge = (lambda c, md: f"{pc(G['solo_gesto|hermana|comida'], c)} (de {c}) · {pc(G['solo_gesto|hermana|medicina'], md)} (de {md})")(G['n|hermana|comida'], G['n|hermana|medicina']) if v == "RG55r" else "—"
            mp = sorted(r["C"].get("med_partida", 0) for r in X)
            out(f"| {mu} | {v} | {C['da|hermana'] / N_:.1f} · {C['da|vecina'] / N_:.1f} | {C['da|ladrona_hermana'] / N_:.1f} · {C['da|ladrona_vecina'] / N_:.1f} | "
                f"{C['da_comida|huerto'] / N_:.1f} · {C['da_comida|bosque'] / N_:.1f} · {C['da_comida|dulce'] / N_:.2f} · {C['da_comida|None'] / N_:.1f} | {sum(mp) / N_:.2f} ({mp[len(mp) // 2]}; {mp[-1]}) | {ge} |")
    banda = lambda h: "≤60" if h <= 60 else ("60-80" if h <= 80 else ">80")
    out("\n## Dar la última comida (21 partidas por jugador y mundo; sumas)\n\n| mundo | jugador | veces (a la hermana) | hambre propia: ≤60 · 60-80 · >80 | hambre de la otra: ≤60 · 60-80 · >80 | con hambre propia > 60: la otra ≤60 · 60-80 · >80 | hambre propia media · de la otra |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            U = [u for r in byn[(v, mu)] for u in r["ult"]]; B1 = Counter(banda(u["h"]) for u in U); B2 = Counter(banda(u["ho"]) for u in U); B3 = Counter(banda(u["ho"]) for u in U if u["h"] > 60)
            out(f"| {mu} | {v} | {len(U)} ({sum(u['hermana'] for u in U)}) | {B1['≤60']} · {B1['60-80']} · {B1['>80']} | {B2['≤60']} · {B2['60-80']} · {B2['>80']} | {B3['≤60']} · {B3['60-80']} · {B3['>80']} | {m([u['h'] for u in U]):.0f} · {m([u['ho'] for u in U]):.0f} |")
    out("\n## Las conductas (cierre_v46)\n\n| mundo | jugador | con la bestia a la vista (fuera), con otra pegada | echadas · muertas | echan: con la hermana · con vecinas | tras perder a la hermana, pegada a una vecina: antes · 5 días después (casos) |\n|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            L_ = by[(v, mu)]; C = sum((Counter(r["C"]) for r in L_), Counter()); B = sum((Counter(r["b"]["C"]) for r in L_), Counter()); G = sum((Counter(r["b"]["grupos"]) for r in L_), Counter()); rec = [x for r in L_ for x in r["rec"]]
            out(f"| {mu} | {v} | {pc(C['bestia_vista_junta'], C['bestia_vista'])} | {B['bestia_echada']} · {B['bestia_muere']} | {G['empujar|con la hermana']} · {G['empujar|con vecinas'] + G['empujar|con la hermana y vecinas']} | {100 * m([a for a, _ in rec]):.0f} % · {100 * m([b for _, b in rec]):.0f} % ({len(rec)}) |")
    byd = defaultdict(list)
    for r in RD: byd[(r["v"], r["mu"])].append(r)
    byv = defaultdict(list)
    for r in RV: byv[(r["v"], r["mu"])].append(r)
    out("\n## Dormir fuera, lo que cuesta, y lo que creen al acabar (diag_v47, verdad_noche_v49)\n\n| mundo | jugador | de lo dormido: su casa · otra casa · fuera | fuera: junto a la hermana · a una vecina · sola | dormidas fuera: golpes · robos de la bestia (por partida) | muertes de noche fuera | lo que creen al acabar de dormir fuera | lo que quita de verdad por noche fuera |\n|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("tonto",) + NUEVAS:
            L_ = byd[(v, mu)]; C = sum((Counter(r["C"]) for r in L_), Counter()); E = sum((Counter(r["E"]) for r in L_), Counter()); cr = [c for r in L_ for c in r["cree"]]
            mue = sum(n for k, n in E.items() if k.startswith("muere_noche_fuera"))
            vn = sum((Counter(r["C"]) for r in byv.get((v, mu), [])), Counter()); real = f"{vn['fuera_vida'] / vn['fuera_noches']:.2f} ({vn['fuera_noches']} noches)" if vn.get("fuera_noches") else "—"
            out(f"| {mu} | {v} | {pc(C['dorm|su casa'], C['dorm'])} · {pc(C['dorm|otra casa'], C['dorm'])} · {pc(C['dorm|fuera'], C['dorm'])} | {pc(C['fuera_junto|hermana'], C['dorm|fuera'])} · {pc(C['fuera_junto|vecina'], C['dorm|fuera'])} · {pc(C['fuera_junto|sola'], C['dorm|fuera'])} | "
                f"{E['pega'] / N_:.2f} · {E['roba'] / N_:.2f} | {mue} | {m(cr):.3f} | {real} |")
    out("\n## Los empujones (diag_v47)\n\n| mundo | jugador | por partida | a la hermana | la empujada lleva comida | gana la que empuja |\n|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in NUEVAS:
            X = [e for r in byd[(v, mu)] for e in r["emp"]]; n = len(X)
            out(f"| {mu} | {v} | {n / N_:.0f} | {pc(sum(e['hermana'] for e in X), n)} | {pc(sum(1 for e in X if e['lleva_b'] > 0), n)} | {pc(sum(1 for e in X if e['gana'] == 'ella'), n)} |")
    byr = defaultdict(list)
    for r in RR: byr[(r["v"], r["mu"])].append(r)
    DIMS = R47.DIMS
    out("\n## El valor de quien roba, del día del robo al siguiente (diag_robos_v47; cambio medio del radar; control: el de las demás)\n\n| mundo | clase | robos | la robada: cuerpo · recursos · vínculo | control | las que lo ven | control |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in NUEVAS:
            L_ = byr[(v, mu)]; agg = {k: defaultdict(list) for k in ("robada", "robada_control", "ven", "ven_control")}
            for r in L_:
                for k, dd in r["cambio"].items():
                    for dim, xs in dd.items(): agg[k][dim] += xs
            fm = lambda k: " · ".join(f"{m(agg[k][dim]):+.4f}" for dim in DIMS)
            out(f"| {mu} | {v} | {sum(r['robos'] for r in L_)} | {fm('robada')} | {fm('robada_control')} | {fm('ven')} | {fm('ven_control')} |")
    bya = defaultdict(list)
    for r in RA: bya[(r["v"], r["mu"].split("+")[0])].append(r)
    gd = defaultdict(int)
    for r in RG: gd[(r["v"], r["mu"])] += r["dulce_despensa"]
    out("\n## El árbol de fruta dulce (21 partidas por jugador y mundo)\n\n| mundo | jugador | apariciones · frutas puestas | lo descubren (criaturas; día mediano) | viajes con recogida (criaturas distintas) | solas · acompañadas | frutas cogidas · perdidas sin coger | vuelven antes de la noche · de noche · no vuelven | la bestia pasa por el árbol · le quita la dulce | se comen la dulce: en el árbol · en casa o cerca · en otro sitio | la dan (a la hermana · a una vecina) | la guardan en la despensa |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            X = bya[(v, mu)]; AR = Counter(); C = Counter()
            for r in X:
                for k in ("aparece", "frutos_puestos", "frutos_se_pierden", "roba_dulce", "bestia_va"): AR[k] += r["AR"].get(k, 0)
                C.update(r["C"])
            ds = sorted(t // C46.DIA for r in X for t in r["desc"].values()); rc = [z for r in X for z in r["recog"]]; q = {(r["s"], z["a"]) for r in X for z in r["recog"]}
            out(f"| {mu} | {v} | {AR['aparece']} · {AR['frutos_puestos']} | {len(ds)} ({ds[len(ds) // 2] if ds else '—'}) | {len(rc)} ({len(q)}) | {sum(1 for z in rc if not z['con'])} · {sum(1 for z in rc if z['con'])} | "
                f"{AR['frutos_puestos'] - AR['frutos_se_pierden']} · {AR['frutos_se_pierden']} | {sum(1 for z in rc if z['fase_vuelve'] in ('mañana', 'tarde'))} · {sum(1 for z in rc if z['fase_vuelve'] in ('anochecer', 'noche'))} · {sum(1 for z in rc if z['muere_antes_de_volver'])} | "
                f"{AR['bestia_va']} · {AR['roba_dulce']} | {C['come_dulce|en el árbol']} · {C['come_dulce|en casa o cerca']} · {C['come_dulce|en otro sitio']} | {C['da_dulce|hermana']} · {C['da_dulce|vecina']} | {gd.get((v, mu), '—') if v.startswith('RG') else '—'} |")
    open(os.path.join(AQUI, "tabla_cierre_v5.md"), "w").write("\n".join(W) + "\n"); print("\n".join(W))

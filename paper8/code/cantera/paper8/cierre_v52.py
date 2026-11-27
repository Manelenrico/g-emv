"""[P8] Prompt 97: la tabla de cierre definitiva (valle_taller_v52: el árbol de fruta dulce encendido en los cinco mundos; RG50r y RG050r con los sabores, el tonto
y el recolector; 21 semillas, 40 días). Solo lee: los cálculos son los de cierre_v46 (vivas, peleas, noche, dar, guardar, conductas), diag_v47 (dormir fuera y lo
que cuesta, empujones, la creencia al final), diag_robos_v47 (el valor de quien roba y las que más roban), verdad_noche_v49 (lo que quita de verdad una noche
fuera) y analiza_arbol_v50 (el árbol), importados con la carpeta cambiada; y, por mundo, la diferencia de vivas RG50r − RG050r y RG50r − el tonto, con su
intervalo del 95 % por semillas emparejadas (bootstrap). Y la fruta dulce guardada en la despensa (con los sabores: dejar en la despensa una comida de origen dulce).
   python3 cierre_v52.py -> markdown por pantalla"""
import gzip, json, os, random, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import cierre_v46 as C46, diag_v47 as D47, diag_robos_v47 as R47, verdad_noche_v49 as VN, analiza_arbol_v50 as AA
T52 = "/Volumes/Mem G-EMV/valle_taller_v52"
def ruta(v, mu, s): return os.path.join(T52, f"{v}_{mu}+sabores_s{s}_d40" if v.startswith("RG") else f"{v}_{mu}_s{s}_d40")
C46.ruta = ruta; D47.ruta = ruta; R47.T46 = T52; VN.CARP = {"RG50r": T52, "RG050r": T52}; AA.P51 = T52
NUEVAS = ("RG50r", "RG050r"); JUG = ("tonto", "recolector") + NUEVAS; MUNDOS = C46.MUNDOS; SEM = C46.SEM; NB = 10000

def guarda_dulce(arg):
    v, mu, s = arg; prev = None; n = 0
    for l in gzip.open(os.path.join(ruta(v, mu, s), "mundo.jsonl.gz"), "rt"):
        x = json.loads(l)
        for a, g in x["agentes"].items():
            if prev and g.get("accion") == "dejar" and g.get("resultado") == "ok" and g.get("en") == "despensa" and a in prev["agentes"]:
                if (prev["agentes"][a].get("bolsa_origen") or []).count("dulce") > (g.get("bolsa_origen") or []).count("dulce"): n += 1
        prev = x
    return {"v": v, "mu": mu, "s": s, "dulce_despensa": n}

def arbol(arg):
    v, mu, s = arg; return AA.una((v, mu + "+sabores" if v.startswith("RG") else mu, s))

def boot(d):
    x = [d[s] for s in sorted(d)]; n = len(x); r = random.Random(8)
    m = sorted(sum(x[r.randrange(n)] for _ in range(n)) / n for _ in range(NB)); return f"{sum(x) / n:+.2f} [{m[int(0.025 * NB)]:+.2f}, {m[int(0.975 * NB) - 1]:+.2f}]"


if __name__ == "__main__":
    T_ = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]; TN = [(v, mu, s) for v in NUEVAS for mu in MUNDOS for s in SEM]
    with Pool(8) as p:
        RC = p.map(C46.una, T_); RD = p.map(D47.una, [(v, mu, s) for v in ("tonto",) + NUEVAS for mu in MUNDOS for s in SEM]); RR = p.map(R47.una, TN)
        RV = p.map(VN.una, TN); RA = p.map(arbol, T_); RG = p.map(guarda_dulce, TN)
    by = defaultdict(list)
    for r in RC: by[(r["v"], r["mu"])].append(r)
    viv = {(r["v"], r["mu"], r["s"]): r["vivas"] for r in RC}
    pc = lambda a, b: f"{100 * a / b:.0f} %" if b else "—"; m = lambda X: sum(X) / len(X) if X else float("nan")
    print("## Vivas al día 40 (de 8) y de qué mueren\n\n| mundo | tonto | recolector | RG50r | RG050r | muertes RG50r: hambre · bestia · golpe · terreno | RG050r |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        f = lambda v: sum(r["vivas"] for r in by[(v, mu)]) / 21
        cs = lambda v: (lambda c: f"{c['hambre']} · {c['bestia']} · {c['golpe']} · {c['terreno']}")(sum((Counter(r["causas"]) for r in by[(v, mu)]), Counter()))
        print(f"| {mu} | {f('tonto'):.2f} | {f('recolector'):.2f} | {f('RG50r'):.2f} | {f('RG050r'):.2f} | {cs('RG50r')} | {cs('RG050r')} |")
    print("\n## Diferencia de vivas por semillas emparejadas (media [IC 95 %])\n\n| mundo | RG50r − RG050r | RG50r − tonto | RG050r − tonto | RG50r − recolector |\n|---|---|---|---|---|")
    for mu in MUNDOS:
        dd = lambda a, b: boot({s: viv[(a, mu, s)] - viv[(b, mu, s)] for s in SEM})
        print(f"| {mu} | {dd('RG50r', 'RG050r')} | {dd('RG50r', 'tonto')} | {dd('RG050r', 'tonto')} | {dd('RG50r', 'recolector')} |")
    print("\n## Pelearse, dormir, dar y guardar\n\n| mundo | jugador | empujones · golpes a otras (por partida) | muertes por golpe | de noche: duerme · en su casa · otra casa · fuera | comidas dadas (a quien lo necesitaba) · medicinas (ídem) | a la hermana · a una vecina | dejadas: despensa · almacén |\n|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            L_ = by[(v, mu)]; C = sum((Counter(r["C"]) for r in L_), Counter()); D = sum((Counter(r["dar"]) for r in L_), Counter()); c = sum((Counter(r["causas"]) for r in L_), Counter())
            com = sum(n for k, n in D.items() if k.startswith("comida|")); comn = sum(n for k, n in D.items() if k.startswith("comida|") and "|necesita|" in k)
            med = sum(n for k, n in D.items() if not k.startswith("comida|")); medn = sum(n for k, n in D.items() if not k.startswith("comida|") and "|necesita|" in k)
            ch = sum(n for k, n in D.items() if k.startswith("comida|hermana")); cv = sum(n for k, n in D.items() if k.startswith("comida|vecina"))
            print(f"| {mu} | {v} | {C['empujar'] / 21:.1f} · {C['golpear'] / 21:.1f} | {c['golpe']} | {pc(C['noche_duerme'], C['noche'])} · {pc(C['noche_su casa'], C['noche'])} · {pc(C['noche_otra casa'], C['noche'])} · {pc(C['noche_fuera'], C['noche'])} | "
                  f"{com / 21:.1f} ({pc(comn, com)}) · {med / 21:.2f} ({pc(medn, med)}) | {ch} · {cv} | {C['deja_despensa'] / 21:.1f} · {C['deja_almacen'] / 21:.1f} |")
    print("\n## Las conductas\n\n| mundo | jugador | con la bestia a la vista (fuera), con otra pegada | echadas · muertas | echan: con la hermana · con vecinas | tras perder a la hermana, pegada a una vecina: antes · 5 días después (casos) |\n|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            L_ = by[(v, mu)]; C = sum((Counter(r["C"]) for r in L_), Counter()); B = sum((Counter(r["b"]["C"]) for r in L_), Counter()); G = sum((Counter(r["b"]["grupos"]) for r in L_), Counter()); rec = [x for r in L_ for x in r["rec"]]
            print(f"| {mu} | {v} | {pc(C['bestia_vista_junta'], C['bestia_vista'])} | {B['bestia_echada']} · {B['bestia_muere']} | {G['empujar|con la hermana']} · {G['empujar|con vecinas'] + G['empujar|con la hermana y vecinas']} | "
                  f"{100 * m([a for a, _ in rec]):.0f} % · {100 * m([b for _, b in rec]):.0f} % ({len(rec)}) |")
    byd = defaultdict(list)
    for r in RD: byd[(r["v"], r["mu"])].append(r)
    byv = defaultdict(list)
    for r in RV: byv[(r["v"], r["mu"])].append(r)
    print("\n## Dormir fuera, lo que cuesta, y lo que creen al acabar\n\n| mundo | jugador | de lo dormido: su casa · otra casa · fuera | fuera: junto a la hermana · a una vecina · sola | dormidas fuera: golpes · robos de la bestia (por partida) | muertes de noche fuera | lo que creen al acabar de dormir fuera (media) | lo que quita de verdad la bestia por noche fuera |\n|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("tonto",) + NUEVAS:
            L_ = byd[(v, mu)]; C = sum((Counter(r["C"]) for r in L_), Counter()); E = sum((Counter(r["E"]) for r in L_), Counter()); cr = [c for r in L_ for c in r["cree"]]
            mue = sum(n for k, n in E.items() if k.startswith("muere_noche_fuera"))
            vn = sum((Counter(r["C"]) for r in byv.get((v, mu), [])), Counter()); real = f"{vn['fuera_vida'] / vn['fuera_noches']:.2f} ({vn['fuera_noches']} noches)" if vn.get("fuera_noches") else "—"
            print(f"| {mu} | {v} | {pc(C['dorm|su casa'], C['dorm'])} · {pc(C['dorm|otra casa'], C['dorm'])} · {pc(C['dorm|fuera'], C['dorm'])} | {pc(C['fuera_junto|hermana'], C['dorm|fuera'])} · {pc(C['fuera_junto|vecina'], C['dorm|fuera'])} · {pc(C['fuera_junto|sola'], C['dorm|fuera'])} | "
                  f"{E['pega'] / 21:.2f} · {E['roba'] / 21:.2f} | {mue} | {m(cr):.3f} | {real} |")
    print("\n## Los empujones\n\n| mundo | jugador | por partida | a la hermana | la empujada lleva comida | gana la que empuja |\n|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in NUEVAS:
            X = [e for r in byd[(v, mu)] for e in r["emp"]]; n = len(X)
            print(f"| {mu} | {v} | {n / 21:.0f} | {pc(sum(e['hermana'] for e in X), n)} | {pc(sum(1 for e in X if e['lleva_b'] > 0), n)} | {pc(sum(1 for e in X if e['gana'] == 'ella'), n)} |")
    byr = defaultdict(list)
    for r in RR: byr[(r["v"], r["mu"])].append(r)
    DIMS = R47.DIMS
    print("\n## El valor de quien roba, del día del robo al siguiente (cambio medio del radar; control: el de las demás)\n\n| mundo | clase | robos | la robada: cuerpo · recursos · vínculo | control | las que lo ven: cuerpo · recursos · vínculo | control |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in NUEVAS:
            L_ = byr[(v, mu)]; agg = {k: defaultdict(list) for k in ("robada", "robada_control", "ven", "ven_control")}
            for r in L_:
                for k, dd in r["cambio"].items():
                    for dim, xs in dd.items(): agg[k][dim] += xs
            fm = lambda k: " · ".join(f"{m(agg[k][dim]):+.4f}" for dim in DIMS)
            print(f"| {mu} | {v} | {sum(r['robos'] for r in L_)} | {fm('robada')} | {fm('robada_control')} | {fm('ven')} | {fm('ven_control')} |")
    print("\n## Las que más roban (las dos de cada partida con más robos) frente a las que menos\n\n| mundo | clase | robos por partida: las que más · las que menos | regalos que reciben (por partida) | turnos con otra pegada | sus empujones a una bestia, acompañada |\n|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in NUEVAS:
            A = Counter(); B = Counter()
            for r in byr[(v, mu)]:
                orden = sorted(r["por"], key=lambda a: (r["por"][a].get("roba", 0), a))
                for a in orden[-2:]: A.update(r["por"][a])
                for a in orden[:2]: B.update(r["por"][a])
            n = 2 * len(byr[(v, mu)])
            print(f"| {mu} | {v} | {A['roba'] / n:.1f} · {B['roba'] / n:.1f} | {A['recibe'] / n:.1f} · {B['recibe'] / n:.1f} | {pc(A['pegada'], A['turnos'])} · {pc(B['pegada'], B['turnos'])} | "
                  f"{pc(A['contra_bestia_acompanada'], A['contra_bestia'])} ({A['contra_bestia']}) · {pc(B['contra_bestia_acompanada'], B['contra_bestia'])} ({B['contra_bestia']}) |")
    bya = defaultdict(list)
    for r in RA: bya[(r["v"], r["mu"].split("+")[0])].append(r)
    gd = defaultdict(int)
    for r in RG: gd[(r["v"], r["mu"])] += r["dulce_despensa"]
    print("\n## El árbol de fruta dulce (21 partidas por jugador y mundo)\n\n| mundo | jugador | apariciones · frutas puestas | lo descubren (criaturas; día mediano) | viajes con recogida (criaturas distintas) | solas · acompañadas | frutas cogidas · perdidas sin coger | vuelven antes de la noche · de noche · no vuelven | la bestia pasa por el árbol · le quita la dulce | se comen la dulce: en el árbol · en casa o cerca · en otro sitio | la dan (a la hermana · a una vecina) | la guardan en la despensa |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            X = bya[(v, mu)]; AR = Counter(); C = Counter()
            for r in X:
                for k in ("aparece", "frutos_puestos", "frutos_se_pierden", "roba_dulce", "bestia_va"): AR[k] += r["AR"].get(k, 0)
                C.update(r["C"])
            ds = sorted(t // C46.DIA for r in X for t in r["desc"].values()); rc = [z for r in X for z in r["recog"]]; q = {(r["s"], z["a"]) for r in X for z in r["recog"]}
            print(f"| {mu} | {v} | {AR['aparece']} · {AR['frutos_puestos']} | {len(ds)} ({ds[len(ds) // 2] if ds else '—'}) | {len(rc)} ({len(q)}) | {sum(1 for z in rc if not z['con'])} · {sum(1 for z in rc if z['con'])} | "
                  f"{AR['frutos_puestos'] - AR['frutos_se_pierden']} · {AR['frutos_se_pierden']} | {sum(1 for z in rc if z['fase_vuelve'] in ('mañana', 'tarde'))} · {sum(1 for z in rc if z['fase_vuelve'] in ('anochecer', 'noche'))} · {sum(1 for z in rc if z['muere_antes_de_volver'])} | "
                  f"{AR['bestia_va']} · {AR['roba_dulce']} | {C['come_dulce|en el árbol']} · {C['come_dulce|en casa o cerca']} · {C['come_dulce|en otro sitio']} | {C['da_dulce|hermana']} · {C['da_dulce|vecina']} | {gd.get((v, mu), '—') if v.startswith('RG') else '—'} |")

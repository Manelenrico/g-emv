"""[P8] Prompt 134: la evaluación del experimento de la base del ocho, v5 (valle_experimento_v5: RG68r, RG068r, S68, S068, P68, RG61r como referencia, el tonto
y el recolector; los cinco mundos con el árbol; semillas 30121-30160; 40 días), con las medidas selladas en predicciones_selladas_v5.md (sección «Cómo se mide
cada predicción y cada medida»). Es evalua_experimento_v4.py (prompt 117) con las clases, la carpeta y las semillas cambiadas, RG61r como jugador más, y los
cambios del v5: P16 (RG68r empuja más que RG068r) y P17 (las partidas con alguna racha > 10, 4 o menos de 200) cambian; P18 a P23 nuevas, de RG68r frente a
RG61r emparejadas (despertares por voz, felicidad de la aldea, vivas, empujones, dormir dentro, el hambre corregida). Solo lee. Los cálculos por partida son los
de cierre_v46 (vivas, causas, bestia a la vista, dar, conductas), diag_v47 (dormir: dónde), analiza_v45 (la reconstrucción tras perder a la hermana, con la
criatura viva 5 días o más), analiza_arbol_v50 (el árbol) y la medida de C5 de evalua_confirmacion (P11, con ambivalencia.py), importados con la carpeta
cambiada; la felicidad funcional, como compara_voz.m1c; el hambre corregida, como arreglos_v12/hambre_corr (escritas aquí para no importar sus rutas).
   python3 evalua_experimento_v5.py -> markdown por pantalla y salida/evalua_experimento_v5.json"""
import gzip, json, os, random, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import cierre_v46 as C46, diag_v47 as D47, analiza_v45 as A45, analiza_arbol_v50 as AA
from ambivalencia import ambivalencia
EXP = "/Volumes/Mem G-EMV/valle_experimento_v5"; SEM = range(30121, 30161); NS = len(SEM); NB = 10000; N_MUESTRA = 2000
MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian"); CRI = ("RG68r", "RG068r", "S68", "S068", "P68", "RG61r"); BASE = ("tonto", "recolector"); JUG = BASE + CRI
def ruta(v, mu, s): return os.path.join(EXP, f"{v}_{mu}+sabores_s{s}_d40" if v not in BASE else f"{v}_{mu}_s{s}_d40")
sys.path.insert(0, os.path.join(AQUI, "cierre_v5")); import tabla_cierre_v5 as TC            # (P9: dormir dentro y en una puerta; se importa antes de fijar las rutas)
C46.ruta = ruta; D47.ruta = ruta; AA.P51 = EXP; TC.ruta = ruta
import analiza_v44 as A44
_a44 = A44.una
def _a44_una(arg):
    """cierre_v46 solo pone «+sabores» a las clases que empiezan por RG: S68, S068 y P68 también juegan con los sabores"""
    v, mu, s, c = arg
    if v not in BASE and not mu.endswith("+sabores"): mu = mu + "+sabores"
    return _a44((v, mu, s, c))
A44.una = _a44_una
A45.carpeta = lambda v, mu, s: ruta(v, mu.replace("+sabores", ""), s)
FLACA = C46.CR["umbral_flaca"]

def hecho(v, mu, s): return os.path.exists(os.path.join(ruta(v, mu, s), "fin.json"))
sys.path.insert(0, os.path.join(AQUI, "medida_v4")); import dormir_v4 as DV4

def dormir9(arg):
    """(prompt 117) P9: la primera vez que se duerme cada noche, con la cuenta arreglada (medida_v4/dormir_v4)"""
    v, mu, s = arg; return dict(DV4.una(ruta(v, mu, s), s), v=v, mu=mu, s=s)

def v5(arg):
    """(prompt 134) para P18 a P23, por partida: los despertares (todos y por voz: motivo «llamada …» o «voz …») y las noches-criatura (las vivas al empezar
    cada día); la felicidad funcional (como compara_voz.m1c: por criatura, la parte de sus turnos despierta con los tres balances de las seis > 0; la aldea, la
    media; la peor parada, la menor); y el hambre por criatura y día, para la medida corregida (como arreglos_v12/hambre_corr.por_dia)"""
    v, mu, s = arg; d = ruta(v, mu, s); DIA = C46.DIA; dormida = {}; P = defaultdict(lambda: [0.0, 0, False]); desp = Counter(); noches = 0
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["turno"]; dormida[t] = {a: bool(g["cuerpo"].get("dormida")) for a, g in x["agentes"].items() if not g["cuerpo"]["muerta"]}
        for e in x.get("eventos") or []:
            if "despierta" in e: desp["todos"] += 1; desp["voz"] += str(e.get("por")).startswith(("llamada", "voz"))
        for a, g in x["agentes"].items():
            if g["cuerpo"]["muerta"]: continue
            if t % DIA == 0: noches += 1
            h = g["cuerpo"]["hambre"]; z = P[f"{a}|{t // DIA}"]; z[0] += h; z[1] += 1; z[2] = z[2] or h > FLACA
    A = defaultdict(lambda: [0, 0])
    for l in gzip.open(os.path.join(d, "criaturas.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); dm = dormida.get(x["turno"], {})
        for a, c in (x.get("criaturas") or {}).items():
            s_ = c.get("seis")
            if not s_ or a not in dm or dm[a]: continue
            A[a][0] += 1; A[a][1] += (s_["placer"] - s_["displacer"]) > 0 and (s_["alegria"] - s_["enfado"]) > 0 and (s_["amor"] - s_["tristeza"]) > 0
    fr = [z[1] / z[0] for z in A.values() if z[0]]
    return {"v": v, "mu": mu, "s": s, "desp": dict(desp), "noches": noches, "feliz_aldea": sum(fr) / len(fr) if fr else None, "feliz_peor": min(fr) if fr else None, "P": dict(P)}

def corregida(pc, pr):
    """(prompt 134) el hambre corregida de una pareja (arreglos_v12/hambre_corr.corregida): solo los pares criatura-día vivos en las dos. Devuelve (hambre de la
    condición, de la referencia, días > 60 de la condición, de la referencia), o None"""
    k = set(pc) & set(pr)
    if not k: return None
    f = lambda P: (sum(P[q][0] for q in k) / max(1, sum(P[q][1] for q in k)), sum(1 for q in k if P[q][2]) / len(k))
    (hc, dc), (hr, dr) = f(pc), f(pr); return hc, hr, dc, dr

def p13_15(arg):
    """(prompt 113) en una partida: P13, si hay algún «dar comida» con éxito con una sola comida en la bolsa y el hambre > 60 en el turno anterior; P14, por par
    (criatura, vecina), los regalos de comida y los días que viven las dos, desde el primer robo de la vecina (pares ladrones) o en toda la partida (los demás);
    P15, por par y tipo, la racha más larga de regalos que van y vuelven con 40 turnos o menos entre uno y otro (comprueba_v58.bucles) y con menos de 40"""
    v, mu, s = arg; d = ruta(v, mu, s); fin = json.load(open(os.path.join(d, "fin.json"))); DIA = C46.DIA
    muere = {m["criatura"]: m["turno"] for m in fin["muertes"]}; prev = {}; ultima = 0; robo = {}; dones = defaultdict(list); E = defaultdict(list); T = 0
    her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["turno"]; T = t
        for a, g in x["agentes"].items():
            if g.get("accion") == "dar" and g.get("resultado") == "ok" and g.get("objetivo"):
                tp = g.get("tipo") or "comida"; b = g["objetivo"]; E[(tuple(sorted((a, b))), tp)].append((t, a))
                if tp == "comida":
                    if a in prev and prev[a][0].count("comida") == 1 and prev[a][1] > FLACA: ultima += 1
                    if b[0] != a[0]: dones[(a, b)].append(t)
        for ev in x["eventos"]:
            if "empujon" in ev and ev.get("gana") and ev.get("soltado"):
                w = ev["gana"]; p = ev["a"] if w == ev["empujon"] else ev["empujon"]
                if w[0] != p[0] and (p, w) not in robo: robo[(p, w)] = t
        for a, g in x["agentes"].items(): prev[a] = (list(g.get("bolsa") or []), g["cuerpo"]["hambre"])
    fin_de = lambda a, b: min(muere.get(a, T), muere.get(b, T), T)
    P14 = []
    for a in "A1 A2 B1 B2 C1 C2 D1 D2".split():
        for b in "A1 A2 B1 B2 C1 C2 D1 D2".split():
            if a == b or b[0] == a[0]: continue
            t0 = robo.get((a, b)); t1 = fin_de(a, b)
            if t0 is not None: dias = (t1 - t0) / DIA; n = sum(1 for t in dones[(a, b)] if t >= t0); P14.append(("ladrona", n / dias) if dias > 0 else None)
            else: dias = t1 / DIA; P14.append(("nunca", len(dones[(a, b)]) / dias) if dias > 0 else None)
    racha = {}
    for (par, tp), L_ in E.items():
        for lim, k in ((40, "le40"), (39, "lt40")):
            r = best = 1
            for (t0, a0), (t1, a1) in zip(L_, L_[1:]):
                r = r + 1 if (t1 - t0 <= lim and a1 != a0) else 1; best = max(best, r)
            racha[(tp, k)] = max(racha.get((tp, k), 0), best)
    return {"v": v, "mu": mu, "s": s, "ultima": ultima, "P14": [z for z in P14 if z], "robos_vecina": len(robo), "racha": {f"{a}|{b}": n for (a, b), n in racha.items()}}
def arbol(arg):
    v, mu, s = arg; return AA.una((v, mu + "+sabores" if v not in BASE else mu, s))
def rec45(arg):
    v, mu, s = arg; r = A45.una((v, mu + "+sabores", s)); return {"v": v, "mu": mu, "s": s, "rec": r["rec"]}

def boot(x):
    n = len(x)
    if not n: return {"media": float("nan"), "lo": float("nan"), "hi": float("nan"), "n": 0}      # (sin partidas todavía: para probar con el experimento a medias)
    r = random.Random(8); m = sorted(sum(x[r.randrange(n)] for _ in range(n)) / n for _ in range(NB))
    return {"media": sum(x) / n, "lo": m[int(0.025 * NB)], "hi": m[int(0.975 * NB) - 1], "n": n}
fb = lambda b: f"{b['media']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]"

def p11(quita_ir=False, quita_dar=False):
    """la medida de C5 (evalua_confirmacion), en los estados de RG68r: Q4 − Q1 de la coincidencia con las sumas, cuartos de ambivalencia dentro de cada
    mundo; IC por bootstrap de partidas. (prompt 113) Con todas las decisiones (las de ir, columna 15 del lanzador arreglado); con `quita_ir`, sin ellas.
    (prompt 117) Con `quita_dar`: la misma muestra y los mismos cuartos, sin las decisiones en que RG68r elige dar o las sumas eligen dar"""
    G = defaultdict(list); LIN = {}
    for mu in MUNDOS:
        cuenta = {}
        for s in SEM:
            f = os.path.join(ruta("RG68r", mu, s), "decisiones.jsonl.gz")
            if os.path.exists(f): LIN[(mu, s)] = [l for l in gzip.open(f, "rt", encoding="utf-8") if not (quita_ir and json.loads(l)[14])]; cuenta[s] = len(LIN[(mu, s)])
        tot = sum(cuenta.values())
        if not tot: continue
        r = random.Random(f"8|RG68r|{mu}"); elegidos = sorted(r.sample(range(tot), min(N_MUESTRA, tot))); E = []; base = 0; j = 0
        for s in sorted(cuenta):
            quiero = set()
            while j < len(elegidos) and elegidos[j] < base + cuenta[s]: quiero.add(elegidos[j] - base); j += 1
            if quiero:
                filas = [json.loads(l) for i, l in enumerate(LIN[(mu, s)]) if i in quiero]
                nec = {(x[0], x[1]) for x in filas}; amb = {}
                for l in gzip.open(os.path.join(ruta("RG68r", mu, s), "criaturas.jsonl.gz"), "rt", encoding="utf-8"):
                    x = json.loads(l)
                    for a, c in x["criaturas"].items():
                        if (x["turno"], a) in nec and c.get("seis"): amb[(x["turno"], a)] = ambivalencia(c["seis"])[0]
                for x in filas:
                    if (x[0], x[1]) in amb: E.append({"s": s, "amb": amb[(x[0], x[1])], "igual": x[7], "dar": x[2] == "dar" or x[4] == "dar"})
            base += cuenta[s]
        if not E: continue
        orden = sorted(e["amb"] for e in E); q1, q3 = orden[len(orden) // 4], orden[(3 * len(orden)) // 4]
        for e in E:
            e["q"] = 1 if e["amb"] <= q1 else (4 if e["amb"] >= q3 else 0)
            if quita_dar and e["dar"]: continue                                 # (prompt 117) los cuartos ya están puestos con toda la muestra
            G[(mu, e["s"])].append(e)
    def dif(L_):
        a = [e["igual"] for e in L_ if e["q"] == 4]; b = [e["igual"] for e in L_ if e["q"] == 1]
        return (sum(a) / len(a) - sum(b) / len(b)) if a and b else None
    ks = sorted(G); r = random.Random(8); v = []
    if not ks: return {"media": None, "lo": float("nan"), "hi": float("nan"), "n_partidas": 0, "n_decisiones": 0, "coinc_Q4": float("nan"), "coinc_Q1": float("nan")}
    for _ in range(NB):
        x = dif([e for _ in ks for e in G[ks[r.randrange(len(ks))]]])
        if x is not None: v.append(x)
    v.sort(); todos = [e for k in ks for e in G[k]]
    q4 = [e["igual"] for e in todos if e["q"] == 4]; q1_ = [e["igual"] for e in todos if e["q"] == 1]
    return {"media": dif(todos), "lo": v[int(0.025 * len(v))], "hi": v[int(0.975 * len(v)) - 1], "n_partidas": len(ks), "n_decisiones": len(todos),
            "coinc_Q4": sum(q4) / max(1, len(q4)), "coinc_Q1": sum(q1_) / max(1, len(q1_))}


if __name__ == "__main__":
    T_ = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM if hecho(v, mu, s)]
    with Pool(8) as p:
        RC = p.map(C46.una, T_); RD = p.map(D47.una, [x for x in T_ if x[0] in ("tonto", "RG68r", "RG068r")])
        RA = p.map(arbol, [x for x in T_ if x[0] in ("RG68r", "recolector", "RG068r", "tonto")]); RR = p.map(rec45, [x for x in T_ if x[0] == "RG68r"])
        RN = p.map(dormir9, [x for x in T_ if x[0] in ("RG68r", "RG61r")]); RP = p.map(p13_15, [x for x in T_ if x[0] in CRI])
        RV = p.map(v5, [x for x in T_ if x[0] in ("RG68r", "RG61r")])                      # (prompt 134) P18 a P23
    P11 = p11(); P11s = p11(quita_ir=True); P11d = p11(quita_dar=True)
    by = defaultdict(list); viv = {}
    for r in RC: by[(r["v"], r["mu"])].append(r); viv[(r["v"], r["mu"], r["s"])] = r["vivas"]
    byd = defaultdict(list)
    for r in RD: byd[(r["v"], r["mu"])].append(r)
    bya = defaultdict(list)
    for r in RA: bya[(r["v"], r["mu"].split("+")[0])].append(r)
    pc = lambda a, b: f"{100 * a / b:.0f} %" if b else "—"; out = []; w = out.append; RES = {}
    par = lambda a, b, mu: boot([viv[(a, mu, s)] - viv[(b, mu, s)] for s in SEM if (a, mu, s) in viv and (b, mu, s) in viv])
    w(f"Partidas leídas: {len(T_)} de 1.600.\n")
    # ── las predicciones ──
    w("## Las predicciones\n")
    d1 = {mu: par("RG68r", "tonto", mu) for mu in ("sequia", "sequia_dura", "bestias_crian")}; ok = all(b["media"] >= 1 and b["lo"] > 0 for b in d1.values())
    w(f"**P1** ({'CUMPLE' if ok else 'FALLA'}). Vivas RG68r − tonto: " + "; ".join(f"{mu} {fb(b)}" for mu, b in d1.items())); RES["P1"] = ok
    m2 = {mu: sum(r["vivas"] for r in by[("RG68r", mu)]) / max(1, len(by[("RG68r", mu)])) for mu in ("abundancia", "normal")}; ok = all(x >= 7.5 for x in m2.values())
    w(f"\n**P2** ({'CUMPLE' if ok else 'FALLA'}). Vivas de RG68r: " + "; ".join(f"{mu} {x:.2f}" for mu, x in m2.items()) + f". (Declarado: en el normal, RG68r − tonto = {fb(par('RG68r', 'tonto', 'normal'))}.)"); RES["P2"] = ok
    g3 = sum(sum(1 for c, n in r["causas"].items() if c == "golpe" for _ in range(n)) for r in RC); ok = g3 == 0
    w(f"\n**P3** ({'CUMPLE' if ok else 'FALLA'}). Muertes por golpe en las {len(RC)} partidas: {g3}."); RES["P3"] = ok
    fr = {}
    for v in ("RG68r", "tonto"):
        C = sum((Counter(r["C"]) for mu in MUNDOS for r in by[(v, mu)]), Counter()); fr[v] = C["bestia_vista_junta"] / max(1, C["bestia_vista"])
    porm = {mu: tuple((lambda C: C["bestia_vista_junta"] / max(1, C["bestia_vista"]))(sum((Counter(r["C"]) for r in by[(v, mu)]), Counter())) for v in ("RG68r", "tonto")) for mu in MUNDOS}
    ok = fr["RG68r"] >= 3 * fr["tonto"]
    w(f"\n**P4** ({'CUMPLE' if ok else 'FALLA'}). Con la bestia a la vista, con otra pegada (los cinco mundos): RG68r {100 * fr['RG68r']:.1f} %, tonto {100 * fr['tonto']:.1f} % (×{fr['RG68r'] / max(1e-9, fr['tonto']):.1f}). Por mundo: " + "; ".join(f"{mu} {100 * a:.0f} % · {100 * b:.0f} %" for mu, (a, b) in porm.items())); RES["P4"] = ok
    L5 = by[("RG68r", "bestias_crian")]; e5 = sum(r["b"]["C"].get("bestia_echada", 0) for r in L5) / max(1, len(L5)); ok = e5 >= 1
    w(f"\n**P5** ({'CUMPLE' if ok else 'FALLA'}). Echadas por partida de RG68r en bestias que crían: {e5:.2f}."); RES["P5"] = ok
    p6 = {}
    for mu in MUNDOS:
        D = sum((Counter(r["dar"]) for r in by[("RG68r", mu)]), Counter()); h = sum(n for k, n in D.items() if k.startswith("comida|hermana")); vc = sum(n for k, n in D.items() if k.startswith("comida|vecina"))
        p6[mu] = (h, vc / 6)
    ok = all(h > v6 for h, v6 in p6.values())
    w(f"\n**P6** ({'CUMPLE' if ok else 'FALLA'}). Comida dada a la hermana · a cada vecina (las de las vecinas / 6): " + "; ".join(f"{mu} {h} · {v6:.1f}" for mu, (h, v6) in p6.items())); RES["P6"] = ok
    p7 = {}
    for mu in MUNDOS:
        D = sum((Counter(r["dar"]) for r in by[("RG68r", mu)]), Counter()); tot = sum(n for k, n in D.items() if k.startswith("comida|")); nec = sum(n for k, n in D.items() if k.startswith("comida|") and "|necesita|" in k)
        p7[mu] = nec / max(1, tot)
    ok = p7["sequia"] > p7["abundancia"] and p7["sequia_dura"] > p7["abundancia"]
    w(f"\n**P7** ({'CUMPLE' if ok else 'FALLA'}). Parte de lo dado a quien estaba flaca: " + "; ".join(f"{mu} {100 * x:.0f} %" for mu, x in p7.items())); RES["P7"] = ok
    d8 = []
    for r in RR:
        for x in r["rec"]:
            dd = [x["despues"][k] for k in x["despues"] if int(k) <= 5]
            if dd: d8.append(sum(dd) / len(dd) - x["antes"])
    b8 = boot(d8) if len(d8) > 1 else None; ok = bool(b8 and b8["media"] > 0 and b8["lo"] > 0)
    w(f"\n**P8** ({'CUMPLE' if ok else 'FALLA'}). Pegada a una vecina, 5 días después − 5 antes de perder a la hermana (por criatura): {fb(b8) if b8 else '—'} (n={len(d8)} criaturas)."); RES["P8"] = ok
    p9 = {}; pu9 = Counter()
    for mu in MUNDOS:
        C = sum((Counter({k: x for k, x in r.items() if isinstance(x, int)}) for r in RN if r["mu"] == mu and r["v"] == "RG68r"), Counter()); p9[mu] = C["dentro"] / max(1, C["noches"])
        for k in ("puerta", "puerta_agotada", "puerta_sin_agotar"): pu9[k] += C[k]
    ok = all(x >= 0.55 for x in p9.values()) and pu9["puerta_sin_agotar"] == 0
    malas = [(r["mu"], r["s"], z["a"], z["t"]) for r in RN if r["v"] == "RG68r" for z in r["puertas_sin_agotar"]][:5]
    w(f"\n**P9** ({'CUMPLE' if ok else 'FALLA'}). La primera vez que se duerme cada noche, dentro de su casa: " + "; ".join(f"{mu} {100 * x:.0f} %" for mu, x in p9.items()) +
      f". En una puerta, en las 200 partidas: {pu9['puerta']} ({pu9['puerta_agotada']} agotada, **{pu9['puerta_sin_agotar']} sin estar agotada**{'; las primeras: ' + str(malas) if malas else ''})."); RES["P9"] = ok
    b10 = {mu: par("RG068r", "RG68r", mu) for mu in ("sequia", "sequia_dura")}; ok = all(b["hi"] >= 0 for b in b10.values())
    w(f"\n**P10** ({'CUMPLE' if ok else 'FALLA'}). Vivas RG068r − RG68r: " + "; ".join(f"{mu} {fb(b)}" for mu, b in b10.items()) + "."); RES["P10"] = ok
    nn = lambda d: d["media"] if d["media"] is not None else float("nan")
    ok = P11["media"] is not None and P11["media"] > 0 and P11["lo"] > 0 and P11d["media"] is not None and P11d["media"] < 0
    w(f"\n**P11** ({'CUMPLE' if ok else 'FALLA'}). Coincidencia de RG68r con las sumas, Q4 − Q1: {nn(P11):+.3f} [{P11['lo']:+.3f}, {P11['hi']:+.3f}] (Q4 {100 * P11['coinc_Q4']:.1f} %, Q1 {100 * P11['coinc_Q1']:.1f} %; {P11['n_decisiones']} decisiones de {P11['n_partidas']} partidas). "
      f"Sin las decisiones en que alguna de las dos da: {nn(P11d):+.3f} [{P11d['lo']:+.3f}, {P11d['hi']:+.3f}] (Q4 {100 * P11d['coinc_Q4']:.1f} %, Q1 {100 * P11d['coinc_Q1']:.1f} %; {P11d['n_decisiones']} decisiones). "
      f"Sin las decisiones de ir: {nn(P11s):+.3f} [{P11s['lo']:+.3f}, {P11s['hi']:+.3f}]."); RES["P11"] = ok
    def fruta(v):
        AR = Counter(); rc = []
        for mu in MUNDOS:
            for r in bya[(v, mu)]:
                for k in ("frutos_puestos", "frutos_se_pierden"): AR[k] += r["AR"].get(k, 0)
                rc += r["recog"]
        return (AR["frutos_puestos"] - AR["frutos_se_pierden"]) / max(1, AR["frutos_puestos"]), rc
    fR, rcR = fruta("RG68r"); fC, _ = fruta("recolector"); vu = [z for z in rcR if z["fase_vuelve"] is not None]; tarde = sum(1 for z in vu if z["fase_vuelve"] in ("anochecer", "noche")) / max(1, len(vu))
    ok = fR < 0.15 and fR < fC
    w(f"\n**P12** ({'CUMPLE' if ok else 'FALLA'}). Fruta del árbol cogida: RG68r {100 * fR:.1f} %, recolector {100 * fC:.1f} %."); RES["P12"] = ok
    M7 = {"tarde": tarde, "n": len(vu)}
    R58 = [r for r in RP if r["v"] == "RG68r"]; n13 = sum(1 for r in R58 if r["ultima"] > 0); ok = n13 <= 0.02 * len(R58)
    w(f"\n**P13** ({'CUMPLE' if ok else 'FALLA'}). Partidas de RG68r con algún «dar la última comida» con hambre > {FLACA}: {n13} de {len(R58)} (veces: {sum(r['ultima'] for r in R58)})."); RES["P13"] = ok
    p14 = {}
    for mu in MUNDOS:
        X = [z for r in R58 if r["mu"] == mu for z in r["P14"]]; L1 = [z[1] for z in X if z[0] == "ladrona"]; L0 = [z[1] for z in X if z[0] == "nunca"]
        if L1: p14[mu] = (sum(L1) / len(L1), sum(L0) / max(1, len(L0)), len(L1), len(L0))
    M8 = {mu: {"robaron": a, "nunca": b, "pares": (n1, n0)} for mu, (a, b, n1, n0) in p14.items()}       # (prompt 117) P14 pasa a medida sin predicción (M8)
    em = {(v, mu): sum(r["C"].get("empujar", 0) for r in by[(v, mu)]) / max(1, len(by[(v, mu)])) for v in ("RG68r", "RG068r", "RG61r") for mu in MUNDOS}
    ok = all(em[("RG68r", mu)] > em[("RG068r", mu)] for mu in MUNDOS)                     # (prompt 134) P16: más que RG068r
    w(f"\n**P16** ({'CUMPLE' if ok else 'FALLA'}). Empujones a otras por partida, RG68r · RG068r: " + "; ".join(f"{mu} {em[('RG68r', mu)]:.0f} · {em[('RG068r', mu)]:.0f} (×{em[('RG68r', mu)] / max(1e-9, em[('RG068r', mu)]):.1f})" for mu in MUNDOS) + "."); RES["P16"] = ok
    mx = {v: {k: max((r["racha"].get(k, 0) for r in RP if r["v"] == v), default=0) for k in ("comida|le40", "medicina|le40", "comida|lt40", "medicina|lt40")} for v in CRI}
    peor = max(((r["racha"].get(k, 0), r["mu"], r["s"], k) for r in R58 for k in ("comida|lt40", "medicina|lt40")), default=(0, "", 0, ""))
    n17 = sum(1 for r in R58 if r["racha"].get("comida|lt40", 0) > 10 or r["racha"].get("medicina|lt40", 0) > 10); ok = n17 <= 4      # (prompt 134) P17: 4 o menos de 200
    w(f"\n**P17** ({'CUMPLE' if ok else 'FALLA'}). Partidas de RG68r con alguna racha de ida y vuelta de más de 10 (menos de 40 turnos entre uno y otro): **{n17} de {len(R58)}**. La racha de ida y vuelta más larga en las 200 partidas de RG68r:comida {mx['RG68r']['comida|lt40']}, medicina {mx['RG68r']['medicina|lt40']} (la peor: {peor[0]}, {peor[1]} {peor[2]}, {peor[3]}); con «40 o menos»: {mx['RG68r']['comida|le40']} · {mx['RG68r']['medicina|le40']}. Las otras clases (comida · medicina): " + "; ".join(f"{v} {mx[v]['comida|lt40']} · {mx[v]['medicina|lt40']}" for v in CRI if v != "RG68r") + "."); RES["P17"] = ok
    # ── (prompt 134) P18 a P23: RG68r frente a RG61r, en las mismas semillas, emparejadas ──
    rv = {(r["v"], r["mu"], r["s"]): r for r in RV}
    pv = lambda k, mu: boot([rv[("RG68r", mu, s)][k] - rv[("RG61r", mu, s)][k] for s in SEM if ("RG68r", mu, s) in rv and ("RG61r", mu, s) in rv
                             and rv[("RG68r", mu, s)][k] is not None and rv[("RG61r", mu, s)][k] is not None])
    dv = {(v, mu): (lambda L_: sum(r["desp"].get("voz", 0) for r in L_) / max(1, sum(r["noches"] for r in L_)))([r for r in RV if r["v"] == v and r["mu"] == mu]) for v in ("RG68r", "RG61r") for mu in MUNDOS}
    ok = all(dv[("RG68r", mu)] < 1 for mu in MUNDOS)
    w(f"\n**P18** ({'CUMPLE' if ok else 'FALLA'}). Despertares por voz por criatura y noche, RG68r · RG61r: " + "; ".join(f"{mu} {dv[('RG68r', mu)]:.2f} · {dv[('RG61r', mu)]:.2f}" for mu in MUNDOS) + "."); RES["P18"] = ok
    b19 = {mu: pv("feliz_aldea", mu) for mu in MUNDOS}; n19 = sum(1 for b in b19.values() if b["lo"] > 0); ok = n19 >= 4
    w(f"\n**P19** ({'CUMPLE' if ok else 'FALLA'}). Felicidad de la aldea, RG68r − RG61r: " + "; ".join(f"{mu} {b['media']:+.3f} [{b['lo']:+.3f}, {b['hi']:+.3f}]" for mu, b in b19.items()) + f" (con el intervalo sobre cero en {n19} de 5)."); RES["P19"] = ok
    b20 = {mu: par("RG68r", "RG61r", mu) for mu in MUNDOS}; ok = all(b["hi"] >= 0 for b in b20.values())
    w(f"\n**P20** ({'CUMPLE' if ok else 'FALLA'}). Vivas RG68r − RG61r: " + "; ".join(f"{mu} {fb(b)}" for mu, b in b20.items()) + "."); RES["P20"] = ok
    ok = all(em[("RG68r", mu)] < em[("RG61r", mu)] for mu in MUNDOS)
    e21 = {mu: boot([r1["C"].get("empujar", 0) - r0["C"].get("empujar", 0) for r1 in by[("RG68r", mu)] for r0 in by[("RG61r", mu)] if r1["s"] == r0["s"]]) for mu in MUNDOS}
    w(f"\n**P21** ({'CUMPLE' if ok else 'FALLA'}). Empujones a otras por partida, RG68r · RG61r: " + "; ".join(f"{mu} {em[('RG68r', mu)]:.0f} · {em[('RG61r', mu)]:.0f} (emparejadas {e21[mu]['media']:+.0f} [{e21[mu]['lo']:+.0f}, {e21[mu]['hi']:+.0f}])" for mu in MUNDOS) + "."); RES["P21"] = ok
    d22 = {}
    for v in ("RG68r", "RG61r"):
        for mu in MUNDOS:
            C = sum((Counter({k: x for k, x in r.items() if isinstance(x, int)}) for r in RN if r["mu"] == mu and r["v"] == v), Counter()); d22[(v, mu)] = C["dentro"] / max(1, C["noches"])
    ok = all(d22[("RG68r", mu)] > d22[("RG61r", mu)] for mu in MUNDOS)
    w(f"\n**P22** ({'CUMPLE' if ok else 'FALLA'}). Noches que se duerme dentro de su casa (la cuenta de P9), RG68r · RG61r: " + "; ".join(f"{mu} {100 * d22[('RG68r', mu)]:.0f} % · {100 * d22[('RG61r', mu)]:.0f} %" for mu in MUNDOS) + "."); RES["P22"] = ok
    b23 = {}
    for mu in MUNDOS:
        cc = [corregida(rv[("RG68r", mu, s)]["P"], rv[("RG61r", mu, s)]["P"]) for s in SEM if ("RG68r", mu, s) in rv and ("RG61r", mu, s) in rv]; cc = [z for z in cc if z]
        b23[mu] = boot([z[0] - z[1] for z in cc]); b23[mu]["d60"] = boot([z[2] - z[3] for z in cc])
    ok = all(b["media"] < 2 for b in b23.values())
    w(f"\n**P23** ({'CUMPLE' if ok else 'FALLA'}). Hambre media corregida, RG68r − RG61r: " + "; ".join(f"{mu} {fb(b)}" for mu, b in b23.items()) + ". (Días con hambre > 60, corregida: " + "; ".join(f"{mu} {b['d60']['media']:+.3f} [{b['d60']['lo']:+.3f}, {b['d60']['hi']:+.3f}]" for mu, b in b23.items()) + ".)"); RES["P23"] = ok
    w(f"\n**Se cumplen {sum(RES.values())} de {len(RES)}:** " + ", ".join(k for k, x in RES.items() if x) + (f". Fallan: " + ", ".join(k for k, x in RES.items() if not x) if not all(RES.values()) else "") + ".\n")
    w("## Las medidas que salen de las predicciones del v3 (sin predicción)\n")
    w(f"**M7** (la hora de las vueltas del árbol). Vueltas de RG68r al anochecer o de noche: {100 * M7['tarde']:.0f} % de {M7['n']}.")
    w(f"\n**M8** (era P14; no sabemos qué saldrá). Comida por día que recibe una vecina: las que le han robado (desde el primer robo) · las que nunca, en los mundos con robos: " + "; ".join(f"{mu} {a:.3f} · {b:.3f} ({n1} · {n0} pares)" for mu, (a, b, n1, n0) in p14.items()) + ".\n")
    # ── la tabla ──
    w("## Vivas al día 40 (de 8; media de las semillas)\n\n| mundo | " + " | ".join(JUG) + " |\n|" + "---|" * (len(JUG) + 1))
    for mu in MUNDOS: w(f"| {mu} | " + " | ".join(f"{sum(r['vivas'] for r in by[(v, mu)]) / max(1, len(by[(v, mu)])):.2f}" for v in JUG) + " |")
    w("\n## Diferencias de vivas por semillas emparejadas (media [IC 95 %])\n\n| mundo | RG68r − RG068r | RG68r − tonto | RG068r − tonto | RG68r − recolector | RG68r − S68 | RG68r − P68 | RG68r − RG61r |\n|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS: w(f"| {mu} | {fb(par('RG68r', 'RG068r', mu))} | {fb(par('RG68r', 'tonto', mu))} | {fb(par('RG068r', 'tonto', mu))} | {fb(par('RG68r', 'recolector', mu))} | {fb(par('RG68r', 'S68', mu))} | {fb(par("RG68r", "P68", mu))} | {fb(par("RG68r", "RG61r", mu))} |")
    w("\n## Muertes (hambre · bestia · golpe · terreno), sumadas\n\n| mundo | " + " | ".join(JUG) + " |\n|" + "---|" * (len(JUG) + 1))
    for mu in MUNDOS: w(f"| {mu} | " + " | ".join((lambda c: f"{c['hambre']} · {c['bestia']} · {c['golpe']} · {c['terreno']}")(sum((Counter(r["causas"]) for r in by[(v, mu)]), Counter())) for v in JUG) + " |")
    w("\n## Pelearse, dormir, dar y guardar (por partida, o en %)\n\n| mundo | jugador | empujones a otras | de noche: duerme · en su casa | comidas dadas (a quien lo necesitaba) · medicinas | a la hermana · a una vecina | dejadas: despensa · almacén |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in JUG:
            L_ = by[(v, mu)]; n = max(1, len(L_)); C = sum((Counter(r["C"]) for r in L_), Counter()); D = sum((Counter(r["dar"]) for r in L_), Counter())
            com = sum(x for k, x in D.items() if k.startswith("comida|")); comn = sum(x for k, x in D.items() if k.startswith("comida|") and "|necesita|" in k); med = sum(x for k, x in D.items() if not k.startswith("comida|"))
            ch = sum(x for k, x in D.items() if k.startswith("comida|hermana")); cv = sum(x for k, x in D.items() if k.startswith("comida|vecina"))
            w(f"| {mu} | {v} | {C['empujar'] / n:.0f} | {pc(C['noche_duerme'], C['noche'])} · {pc(C['noche_su casa'], C['noche'])} | {com / n:.1f} ({pc(comn, com)}) · {med / n:.2f} | {ch} · {cv} | {C['deja_despensa'] / n:.0f} · {C['deja_almacen'] / n:.0f} |")
    w("\n## Las conductas (RG y el tonto)\n\n| mundo | jugador | con la bestia a la vista, con otra pegada | echadas (por partida) | echan: con la hermana · con vecinas |\n|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("tonto",) + CRI:
            L_ = by[(v, mu)]; n = max(1, len(L_)); C = sum((Counter(r["C"]) for r in L_), Counter()); B = sum((Counter(r["b"]["C"]) for r in L_), Counter()); G = sum((Counter(r["b"]["grupos"]) for r in L_), Counter())
            w(f"| {mu} | {v} | {pc(C['bestia_vista_junta'], C['bestia_vista'])} | {B['bestia_echada'] / n:.2f} | {G['empujar|con la hermana']} · {G['empujar|con vecinas'] + G['empujar|con la hermana y vecinas']} |")
    w("\n## Dormir fuera y lo que creen al acabar\n\n| mundo | jugador | de lo dormido: su casa · otra casa · fuera | dormidas fuera: golpes · robos de la bestia (por partida) | lo que creen al acabar de dormir fuera |\n|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("tonto", "RG68r", "RG068r"):
            L_ = byd[(v, mu)]; n = max(1, len(L_)); C = sum((Counter(r["C"]) for r in L_), Counter()); E = sum((Counter(r["E"]) for r in L_), Counter()); cr = [c for r in L_ for c in r["cree"]]
            w(f"| {mu} | {v} | {pc(C['dorm|su casa'], C['dorm'])} · {pc(C['dorm|otra casa'], C['dorm'])} · {pc(C['dorm|fuera'], C['dorm'])} | {E['pega'] / n:.2f} · {E['roba'] / n:.2f} | {(sum(cr) / len(cr)) if cr else float('nan'):.3f} |")
    w("\n## El árbol de fruta dulce\n\n| mundo | jugador | lo descubren (criaturas) | viajes con recogida (criaturas distintas) | solas · acompañadas | frutas cogidas · puestas | vuelven antes de la noche · de noche · no vuelven | la bestia le quita la dulce |\n|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("tonto", "recolector", "RG68r", "RG068r"):
            X = bya[(v, mu)]; AR = Counter()
            for r in X:
                for k in ("frutos_puestos", "frutos_se_pierden", "roba_dulce"): AR[k] += r["AR"].get(k, 0)
            rc = [z for r in X for z in r["recog"]]; q = {(r["s"], z["a"]) for r in X for z in r["recog"]}
            w(f"| {mu} | {v} | {sum(len(r['desc']) for r in X)} | {len(rc)} ({len(q)}) | {sum(1 for z in rc if not z['con'])} · {sum(1 for z in rc if z['con'])} | {AR['frutos_puestos'] - AR['frutos_se_pierden']} · {AR['frutos_puestos']} | "
              f"{sum(1 for z in rc if z['fase_vuelve'] in ('mañana', 'tarde'))} · {sum(1 for z in rc if z['fase_vuelve'] in ('anochecer', 'noche'))} · {sum(1 for z in rc if z['muere_antes_de_volver'])} | {AR['roba_dulce']} |")
    print("\n".join(out)); json.dump({"predicciones": RES, "P11": P11, "P11_sin_ir": P11s, "P11_sin_dar": P11d, "P9": {"dentro": p9, "puertas": dict(pu9)}, "P16": {f"{v}|{mu}": x for (v, mu), x in em.items()}, "M7": M7, "M8": M8, "P17_partidas": n17, "P18": {f"{v}|{mu}": x for (v, mu), x in dv.items()}, "P19": b19, "P20": b20, "P21": e21, "P22": {f"{v}|{mu}": x for (v, mu), x in d22.items()}, "P23": b23, "partidas": len(T_)}, open(os.path.join(AQUI, "salida", "evalua_experimento_v5.json"), "w"), ensure_ascii=False, indent=1)

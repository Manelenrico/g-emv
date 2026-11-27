"""[P8] Prompt 143, puntos 6 y 7: el taller de la voz de ir a casa frente a las partidas selladas. Solo lee: no juega nada.
PARTIDAS: VC1 (/Volumes/Mem G-EMV/valle_vc1_taller); RG68r y su gemela RG068r selladas (valle_experimento_v5); en sequía dura, RG68r sin frío (prompt 141,
valle_sin_frio_v1). Sequía dura y sequía, semillas 30121 a 30140; normal y bestias que crían, 30121 a 30130 (los cuatro mundos están en el v5 con esos
nombres, todos «+sabores»). Las diferencias, emparejadas por semilla (la media de las diferencias de cada partida), con intervalo del 95 % (bootstrap de
10.000, semilla 8).
LAS MEDIDAS, por partida (las reglas, fijadas aquí antes de mirar el taller):
  - LAS NOCHES: las de dormir_fuera_v5/noches_v5.py (importado: una noche es «fuera» si en la fase noche está dormida fuera de su casa más de la mitad de los
    turnos; «dentro» si dormida dentro más de la mitad; si no, «despierta»), de cada criatura viva al empezar la noche. NOCHES FUERA: la parte de las noches
    que son «fuera» (de todas: dentro, fuera y despierta), en los días 0 a 9 y en toda la partida;
  - A QUÉ TURNO ENTRA EN CASA: el turno del día en que entra en su casa por primera vez desde el 160 (noches_v5: «entra»), media de las noches en que entra;
    y la parte de las noches en que no entra (antes de acabar el día);
  - VIVAS EL DÍA 40: las criaturas sin muerte en fin.json; MUERTES, por causa; MUERTES HASTA EL DÍA 14 (con el día de la muerte ≤ 14);
  - HAMBRE AL EMPEZAR EL DÍA 10: la media de las vivas en el turno 4.000;
  - TURNOS AL FRÍO: por criatura y día viva, los turnos en una fase fría (la temperatura de fuera bajo la zona cómoda, config_valle.json) fuera de cualquier
    casa (sitio de balance.jsonl.gz que no es «C», «O» ni «P»; la puerta tiene la temperatura de dentro, mundo.py:681-686);
  - COMIDAS: comidas comidas con éxito, por criatura y día viva;
  - FELICIDAD DE LA ALDEA Y DE LA PEOR PARADA: las de evalua_experimento_v5.v5 (importado: por criatura, la parte de sus turnos despierta con los tres balances
    de las seis > 0; la aldea, la media; la peor parada, la menor);
  - EMPUJONES: los que el mundo hizo a otra criatura (no a la bestia; no los «no: …»), por partida;
  - DESPERTARES: los del mundo (eventos «despierta»), por partida;
  - PEGADA A LA HERMANA: por criatura y día viva, los turnos con la hermana viva a una casilla o menos (Chebyshev).
LA REGLA (punto 6 del prompt): pasa si (1) en sequía y sequía dura juntas, días 0 a 9, la parte de noches fuera de VC1 (las noches fuera sumadas entre todas
las noches sumadas, de las 40 partidas) es como mucho dos tercios de la de RG68r sellada; y (2) en cada mundo, con las medias de las partidas, vivas el día 40
de VC1 − RG68r ≥ −0,2, felicidad de la aldea de VC1 − RG68r ≥ −0,03 y empujones de VC1 ≤ 1,25 × los de RG68r.
LA VOZ (voz_a_casa_v1/voces_v1.py): cuántas veces suena por partida y por criatura y día viva, a qué turnos del día, cuántas se devuelven, cuántas acaban con
las dos en casa, y en cuántas decisiones oyendo cambió lo elegido.
   python3 voz_a_casa_v1/analiza_vc1.py -> voz_a_casa_v1/analiza_vc1.md y .json"""
import gzip, json, os, random, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path[:0] = [P8, AQUI, os.path.join(P8, "dormir_fuera_v5")]
import diario_v1 as V1
import noches_v5 as N5
import voces_v1 as VV
T7 = "/Volumes/Mem G-EMV"; DIA = V1.DIA; NB = 10000; TC = V1.CFG["temperatura"]
FRIAS = {f for f, g in TC["fuera"].items() if g < TC["confort"][0]}
CARP = {"VC1": (os.path.join(T7, "valle_vc1_taller"), "VC1"), "RG68r": (os.path.join(T7, "valle_experimento_v5"), "RG68r"),
        "gemela": (os.path.join(T7, "valle_experimento_v5"), "RG068r"), "sin frío": (os.path.join(T7, "valle_sin_frio_v1"), "RG68r")}
MUNDOS = {"sequia_dura": range(30121, 30141), "sequia": range(30121, 30141), "normal": range(30121, 30131), "bestias_crian": range(30121, 30131)}
NOMBRE = {"sequia_dura": "sequía dura", "sequia": "sequía", "normal": "normal", "bestias_crian": "bestias que crían"}
JUG = lambda mu: ("VC1", "RG68r", "gemela") + (("sin frío",) if mu == "sequia_dura" else ())
her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
cheb = lambda p, q: max(abs(p[0] - q[0]), abs(p[1] - q[1]))
OUT = os.path.join(AQUI, "partidas"); os.makedirs(OUT, exist_ok=True); os.makedirs(os.path.join(AQUI, "noches"), exist_ok=True)

def ruta(j, mu, s): c, v = CARP[j]; return os.path.join(c, f"{v}_{mu}+sabores_s{s}_d40")

def una(x):
    j, mu, s = x; f = os.path.join(OUT, f"{j.replace(' ', '_')}_{mu}_{s}.json")
    if os.path.exists(f): return f
    c, v = CARP[j]; d = ruta(j, mu, s)
    if not os.path.exists(os.path.join(d, "fin.json")): raise SystemExit(f"partida sin acabar: {d}")     # (antes de escribir nada)
    import evalua_experimento_v5 as EV
    EV.ruta = lambda v_, mu_, s_: d
    fel = EV.v5((v, mu, s))
    nf = N5.una((v, mu, s, c, 40, os.path.join(AQUI, "noches", f"{j.replace(' ', '_')}_{mu}_{s}.json"))); N = json.load(open(nf))["noches"]
    SIT = {}
    for l in gzip.open(os.path.join(d, "balance.jsonl.gz"), "rt", encoding="utf-8"):
        b = json.loads(l); SIT[b["t"]] = {a: q[5] for a, q in b["c"].items()}
    cd = set(); com = frio = peg = emp = desp = 0; h10 = None; agentes = None
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        m = json.loads(l); t = m["turno"]; A = {a: g for a, g in m["agentes"].items() if isinstance(g, dict) and "cuerpo" in g and a != "bestia"}
        if agentes is None: agentes = sorted(A)
        desp += sum(1 for e in m.get("eventos") or [] if "despierta" in e)
        if t == 10 * DIA: hv = [g["cuerpo"]["hambre"] for g in A.values() if not g["cuerpo"]["muerta"]]; h10 = sum(hv) / len(hv) if hv else None
        for a, g in A.items():
            if g["cuerpo"]["muerta"]: continue
            cd.add((a, t // DIA)); k = g.get("accion")
            com += k == "comer" and g.get("resultado") == "ok" and g.get("tipo") == "comida"
            emp += k == "empujar" and bool(g.get("objetivo")) and not str(g["objetivo"]).startswith("bestia") and not str(g.get("resultado") or "").startswith("no:")
            frio += m.get("fase") in FRIAS and (SIT.get(t) or {}).get(a) not in ("C", "O", "P", None)
            h = A.get(her(a)); peg += h is not None and not h["cuerpo"]["muerta"] and cheb(g["pos"], h["pos"]) <= 1
    fin = json.load(open(os.path.join(d, "fin.json"))); mu_ = [x for x in fin["muertes"] if x["dia"] < 40]
    n = max(1, len(cd)); noc = lambda dmax: [z for z in N if z["dia"] < dmax]
    r = {"j": j, "mu": mu, "s": s, "n_cd": len(cd), "vivas40": len(agentes) - len(mu_), "muertes": len(mu_), "causas": dict(Counter(x["causa"] for x in mu_)),
         "muertes14": sum(1 for x in mu_ if x["dia"] <= 14), "h10": h10, "frio": frio / n, "comidas": com / n, "pegada": peg / n, "empujones": emp, "despertares": desp,
         "feliz_aldea": fel["feliz_aldea"], "feliz_peor": fel["feliz_peor"],
         "noches10": [sum(z["tipo"] == "fuera" for z in noc(10)), len(noc(10))], "noches40": [sum(z["tipo"] == "fuera" for z in N), len(N)],
         "entra": [sum(z["entra"] for z in N if z["entra"] is not None), sum(z["entra"] is not None for z in N), len(N)]}
    json.dump(r, open(f, "w")); return f

def boot(x):
    x = [v for v in x if v is not None]
    if not x: return None
    r = random.Random(8); n = len(x); m = sorted(sum(x[r.randrange(n)] for _ in range(n)) / n for _ in range(NB)); return sum(x) / n, m[int(0.025 * NB)], m[int(0.975 * NB) - 1]
def f_(b, k=2, pc=False):
    if b is None: return "—"
    if pc: return f"{100 * b[0]:+.{k}f} [{100 * b[1]:+.{k}f}, {100 * b[2]:+.{k}f}] pp"
    return f"{b[0]:+.{k}f} [{b[1]:+.{k}f}, {b[2]:+.{k}f}]".replace(".", ",")
def media(L): L = [v for v in L if v is not None]; return sum(L) / len(L) if L else None

MED = [("noches fuera, días 0 a 9 (parte)", lambda r: r["noches10"][0] / r["noches10"][1] if r["noches10"][1] else None, True),
       ("noches fuera, toda la partida (parte)", lambda r: r["noches40"][0] / r["noches40"][1] if r["noches40"][1] else None, True),
       ("a qué turno del día entra en casa (desde el 160)", lambda r: r["entra"][0] / r["entra"][1] if r["entra"][1] else None, False),
       ("noches sin entrar en casa desde el 160 (parte)", lambda r: 1 - r["entra"][1] / r["entra"][2] if r["entra"][2] else None, True),
       ("vivas el día 40", lambda r: r["vivas40"], False), ("muertes", lambda r: r["muertes"], False), ("  de hambre", lambda r: r["causas"].get("hambre", 0), False),
       ("  por la bestia", lambda r: r["causas"].get("bestia", 0), False), ("  de otra cosa", lambda r: r["muertes"] - r["causas"].get("hambre", 0) - r["causas"].get("bestia", 0), False),
       ("muertes hasta el día 14", lambda r: r["muertes14"], False), ("hambre al empezar el día 10 (las vivas)", lambda r: r["h10"], False),
       ("turnos al frío fuera de casa (por criatura y día)", lambda r: r["frio"], False), ("comidas (por criatura y día)", lambda r: r["comidas"], False),
       ("felicidad de la aldea", lambda r: r["feliz_aldea"], False), ("felicidad de la peor parada", lambda r: r["feliz_peor"], False),
       ("empujones (por partida)", lambda r: r["empujones"], False), ("despertares (por partida)", lambda r: r["despertares"], False),
       ("turnos pegada a la hermana (por criatura y día)", lambda r: r["pegada"], False)]


if __name__ == "__main__" and len(sys.argv) == 5 and sys.argv[1] == "una":          # (para probar una partida: una <jugador> <mundo> <semilla>)
    print(open(una((sys.argv[2].replace("_", " ") if sys.argv[2] == "sin_frío" else sys.argv[2], sys.argv[3], int(sys.argv[4])))).read()); sys.exit()
if __name__ == "__main__":
    T_ = [(j, mu, s) for mu, S in MUNDOS.items() for j in JUG(mu) for s in S]
    if sys.argv[1:] == ["selladas"]:                                            # (solo las medidas de las selladas, mientras se juega el taller)
        with Pool(3) as p: p.map(una, [x for x in T_ if x[0] != "VC1"])
        sys.exit()
    with Pool(6) as p: F = p.map(una, T_)
    R = {(r["j"], r["mu"], r["s"]): r for r in (json.load(open(f)) for f in F)}; J = {"medidas": {}}
    w = ["# El taller de la voz de ir a casa: VC1 frente a las selladas\n"]
    # ── la regla ──
    S2 = [(mu, s) for mu in ("sequia", "sequia_dura") for s in MUNDOS[mu]]
    fv = sum(R[("VC1",) + k]["noches10"][0] for k in S2) / sum(R[("VC1",) + k]["noches10"][1] for k in S2)
    fr = sum(R[("RG68r",) + k]["noches10"][0] for k in S2) / sum(R[("RG68r",) + k]["noches10"][1] for k in S2)
    rr = random.Random(8); bs = []
    for _ in range(NB):
        q = [S2[rr.randrange(len(S2))] for _ in S2]
        a_ = sum(R[("VC1",) + k]["noches10"][0] for k in q) / sum(R[("VC1",) + k]["noches10"][1] for k in q); b_ = sum(R[("RG68r",) + k]["noches10"][0] for k in q) / sum(R[("RG68r",) + k]["noches10"][1] for k in q)
        bs.append(1 - a_ / b_)
    bs.sort(); baja = 1 - fv / fr; ok1 = fv <= fr * 2 / 3
    w.append("## La regla\n")
    w.append(f"**Primera parte** (sequía y sequía dura juntas, días 0 a 9): noches fuera de VC1 {100 * fv:.1f} %, de RG68r sellada {100 * fr:.1f} %; baja un {100 * baja:.1f} % "
             f"[{100 * bs[int(0.025 * NB)]:.1f}, {100 * bs[int(0.975 * NB) - 1]:.1f}] (hace falta al menos un 33,3 %): {'se cumple' if ok1 else 'no se cumple'}.\n")
    w.append("**Segunda parte** (en cada mundo, medias de las partidas, VC1 − RG68r sellada):\n\n| mundo | vivas el día 40 (≥ −0,2) | felicidad de la aldea (≥ −0,03) | empujones: VC1 / RG68r (≤ 1,25) | se cumple |\n|---|---|---|---|---|")
    ok2 = True; J["regla"] = {"noches_vc1": fv, "noches_rg68r": fr, "baja": baja, "baja_ic": [bs[int(0.025 * NB)], bs[int(0.975 * NB) - 1]], "primera": ok1, "mundos": {}}
    for mu, S in MUNDOS.items():
        mv = lambda j, k: media([R[(j, mu, s)][k] for s in S])
        dv = mv("VC1", "vivas40") - mv("RG68r", "vivas40"); df = mv("VC1", "feliz_aldea") - mv("RG68r", "feliz_aldea"); qe = mv("VC1", "empujones") / max(1e-9, mv("RG68r", "empujones"))
        o = dv >= -0.2 - 1e-9 and df >= -0.03 - 1e-9 and qe <= 1.25 + 1e-9;           # («como mucho»: el límite justo cuenta; 1e-9 por el redondeo de la resta)
        ok2 = ok2 and o; J["regla"]["mundos"][mu] = {"vivas": dv, "feliz": df, "empujones": qe, "ok": o}
        w.append(f"| {NOMBRE[mu]} | {dv:+.2f} | {df:+.3f} | {qe:.2f} ({mv('VC1', 'empujones'):.1f} / {mv('RG68r', 'empujones'):.1f}) | {'sí' if o else 'no'} |".replace(".", ","))
    J["regla"]["segunda"] = ok2; J["regla"]["pasa"] = ok1 and ok2
    w.append(f"\n**La regla {'PASA' if ok1 and ok2 else 'NO PASA'}.**\n")
    # ── por mundo ──
    for mu, S in MUNDOS.items():
        js = JUG(mu); w.append(f"## {NOMBRE[mu]} ({len(S)} semillas)\n")
        w.append("| medida | " + " | ".join(js) + " | VC1 − RG68r [95 %] | VC1 − gemela [95 %] |" + (" VC1 − sin frío [95 %] |" if "sin frío" in js else "") + "\n|---|" + "---|" * (len(js) + 2 + ("sin frío" in js)))
        for nom, fn, pc in MED:
            vals = [media([fn(R[(j, mu, s)]) for s in S]) for j in js]
            difs = [boot([None if fn(R[("VC1", mu, s)]) is None or fn(R[(o, mu, s)]) is None else fn(R[("VC1", mu, s)]) - fn(R[(o, mu, s)]) for s in S]) for o in js[1:]]
            fv_ = (lambda x: "—" if x is None else (f"{100 * x:.1f} %" if pc else f"{x:.2f}").replace(".", ","))
            w.append(f"| {nom} | " + " | ".join(fv_(x) for x in vals) + " | " + " | ".join(f_(b, 1, True).replace(".", ",") if pc else f_(b) for b in difs) + " |")
            J["medidas"][f"{mu}|{nom}"] = {"valores": dict(zip(js, vals)), "difs": dict(zip(js[1:], difs))}
        w.append("")
    # ── la voz ──
    w.append("## La voz\n")
    w.append("| mundo | voces por partida | por criatura y día viva | «ir a casa» ya era lo elegido | devueltas | las dos en casa | devuelta y las dos en casa | decisiones oyendo | en las que cambió lo elegido |\n|---|---|---|---|---|---|---|---|---|")
    TURNOS = Counter(); CAMB = Counter(); J["voz"] = {}
    for mu, S in MUNDOS.items():
        V = []; O = []; ncd = 0
        for s in S:
            vs, oye, _ = VV.voces(ruta("VC1", mu, s)); V += vs; O += oye; ncd += R[("VC1", mu, s)]["n_cd"]
        n = len(V); pc = lambda k: f"{100 * k / n:.0f} %" if n else "—"
        for v in V: TURNOS[(mu, 20 * (v["k"] // 20))] += 1
        for o in O:
            if o["cambio"]: CAMB[(o["sin_oir"], o["elige"])] += 1
        nc = sum(o["cambio"] for o in O)
        w.append(f"| {NOMBRE[mu]} | {n / len(S):.1f} | {n / max(1, ncd):.2f} | {pc(sum(v['ya_era'] for v in V))} | {sum(v['devuelta'] for v in V)} ({pc(sum(v['devuelta'] for v in V))}) | "
                 f"{sum(v['dos_en_casa'] for v in V)} ({pc(sum(v['dos_en_casa'] for v in V))}) | {sum(v['devuelta'] and v['dos_en_casa'] for v in V)} | {len(O)} | {nc} ({100 * nc / max(1, len(O)):.1f} %) |".replace(".", ","))
        J["voz"][mu] = {"voces": n, "partidas": len(S), "n_cd": ncd, "ya_era": sum(v["ya_era"] for v in V), "devueltas": sum(v["devuelta"] for v in V), "dos_en_casa": sum(v["dos_en_casa"] for v in V),
                        "oyendo": len(O), "cambios": nc}
    w.append("\n**A qué turno del día suena** (voces, por tramos de 20 turnos):\n\n| mundo | " + " | ".join(f"{k}-{k + 19}" for k in range(180, 400, 20)) + " |\n|---|" + "---|" * 11)
    for mu in MUNDOS: w.append(f"| {NOMBRE[mu]} | " + " | ".join(str(TURNOS[(mu, k)]) for k in range(180, 400, 20)) + " |")
    w.append("\n**Cuando lo oído cambió lo elegido** (los cuatro mundos; sin haberla oído → oyéndola; los diez más frecuentes):\n\n| sin oírla | oyéndola | decisiones |\n|---|---|---|")
    for (a, b), n in CAMB.most_common(10): w.append(f"| {a} | {b} | {n} |")
    open(os.path.join(AQUI, "analiza_vc1.md"), "w").write("\n".join(w) + "\n"); json.dump(J, open(os.path.join(AQUI, "analiza_vc1.json"), "w"), ensure_ascii=False, default=str); print("\n".join(w))

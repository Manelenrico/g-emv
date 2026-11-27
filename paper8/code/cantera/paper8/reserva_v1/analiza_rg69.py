"""[P8] Prompt 146, puntos 2 a 4: el taller de la reserva (RG69r, /Volumes/Mem G-EMV/valle_rg69_taller) frente a la RG68r sellada y la gemela RG068r del v5,
emparejadas por semilla (sin volver a jugarlas). Solo lee: no juega nada.
LAS MEDIDAS (importadas, no copiadas):
  - las del prompt 143 (voz_a_casa_v1/analiza_vc1.una: vivas el día 40, muertes y sus causas, hambre al empezar el día 10, felicidad de la aldea y de la peor
    parada, empujones, noches fuera, comidas…). Las de las selladas ya estaban medidas en voz_a_casa_v1/partidas/ y se leen de ahí; las de RG69r van a
    reserva_v1/partidas/ y reserva_v1/noches/;
  - las del prompt 144 (hambre_ganancias_v1/extrae_hg_v1.una, días 0 a 9: turnos despierta con hambre > 30 y comida en la bolsa, hambre al comer, comidas
    con 60 o más, destino de lo que coge). Las de las selladas en sequía y sequía dura ya estaban en hambre_ganancias_v1/datos/; las demás van a
    reserva_v1/datos/;
  - nueva: SIN NADA AL LLEGAR A LA ESCASEZ: en el primer turno del día 10 y del día 30 (las escaseces de las sequías, prompt 138), cuántas criaturas vivas no
    llevan comida en la bolsa y no hay comida en la despensa de su casa (mundo.jsonl.gz y criaturas.jsonl.gz), por partida.
LA REGLA (fijada en el prompt antes de jugar). Pasa si se cumplen las dos:
  a) MECANISMO: sequía y sequía dura juntas, días 0 a 9, los turnos al día despierta con hambre > 30 y comida en la bolsa (por criatura y día viva; la media
     de las 40 partidas, como el 144) de RG69r son como mucho la mitad de los de RG68r sellada;
  b) NO HACE DAÑO, en cada mundo, con las medias de las partidas: vivas el día 40 de RG69r − RG68r ≥ −0,2; felicidad de la aldea ≥ −0,03; empujones de
     RG69r ≤ 1,25 × los de RG68r (el límite justo cuenta: 1e-9 por el redondeo de la resta, como en el 143).
Los intervalos: bootstrap de las semillas emparejadas (10.000, semilla 8).
   python3 reserva_v1/analiza_rg69.py -> reserva_v1/analiza_rg69.md y .json"""
import gzip, json, os, random, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI)
sys.path[:0] = [P8, os.path.join(P8, "voz_a_casa_v1"), os.path.join(P8, "hambre_ganancias_v1"), os.path.join(P8, "gemela_v5"), os.path.join(P8, "dormir_fuera_v5")]
import analiza_vc1 as AN
import extrae_hg_v1 as X
T7 = AN.T7; DIA = AN.DIA; NB = AN.NB; TALLER = os.path.join(T7, "valle_rg69_taller"); EXP = os.path.join(T7, "valle_experimento_v5")
AN.CARP["RG69r"] = (TALLER, "RG69r"); MUNDOS = AN.MUNDOS; NOMBRE = AN.NOMBRE
VAR = {"RG69r": "RG69r", "RG68r": "RG68r", "gemela": "RG068r"}
for d_ in ("partidas", "noches", "datos"): os.makedirs(os.path.join(AQUI, d_), exist_ok=True)

def med143(x):
    j, mu, s = x
    if j != "RG69r": return os.path.join(P8, "voz_a_casa_v1", "partidas", f"{j}_{mu}_{s}.json") if os.path.exists(os.path.join(P8, "voz_a_casa_v1", "partidas", f"{j}_{mu}_{s}.json")) else AN.una(x)
    AN.OUT = os.path.join(AQUI, "partidas"); AN.AQUI = AQUI; return AN.una(x)

def med144(x):
    j, mu, s = x; v = VAR[j]; viejo = os.path.join(P8, "hambre_ganancias_v1", "datos", f"{v}_{mu}_{s}.json")
    if os.path.exists(viejo): return viejo
    X.EXP = TALLER if j == "RG69r" else EXP; X.AQUI = AQUI
    if not os.path.exists(os.path.join(X.EXP, f"{v}_{mu}+sabores_s{s}_d40", "fin.json")): raise SystemExit(f"partida sin acabar: {v} {mu} {s}")
    return X.una((v, mu, s))

def vacias(x):
    """en el primer turno del día 10 y del día 30: las vivas sin comida en la bolsa ni en la despensa de su casa, y las vivas"""
    j, mu, s = x; f = os.path.join(AQUI, "partidas", f"vacias_{j}_{mu}_{s}.json")
    if os.path.exists(f): return f
    d = os.path.join(TALLER if j == "RG69r" else EXP, f"{VAR[j]}_{mu}+sabores_s{s}_d40"); out = {}
    for lm, lc in zip(gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"), gzip.open(os.path.join(d, "criaturas.jsonl.gz"), "rt", encoding="utf-8")):
        m = json.loads(lm); t = m["turno"]
        if t > 30 * DIA: break
        if t in (10 * DIA, 30 * DIA):
            c = json.loads(lc); V = [(a, g) for a, g in m["agentes"].items() if a != "bestia" and isinstance(g, dict) and "cuerpo" in g and not g["cuerpo"]["muerta"]]
            out[str(t // DIA)] = [sum(1 for a, g in V if "comida" not in (g.get("bolsa") or []) and (c.get("despensas") or {}).get(a[0], {}).get("comida", 0) == 0), len(V)]
    json.dump(out, open(f, "w")); return f

def todo(x): return x, med143(x), (med144(x)), vacias(x)


if __name__ == "__main__":
    T_ = [(j, mu, s) for mu, S in MUNDOS.items() for j in ("RG69r", "RG68r", "gemela") for s in S]
    with Pool(6) as p: F = p.map(todo, T_)
    A = {x: json.load(open(a)) for x, a, _, _ in F}; H = {x: json.load(open(b)) for x, _, b, _ in F}; Vc = {x: json.load(open(c)) for x, _, _, c in F}
    cd = lambda r: max(1, sum(1 for z in r["dias"] if z["turnos"]))
    def mean_(L): L = [v for v in L if v is not None]; return sum(L) / len(L) if L else None
    M = [(e, k, f) for e, f, k in AN.MED] + [
        ("turnos despierta con hambre > 30 y comida en la bolsa (por criatura y día, días 0 a 9)", "h", lambda r: sum(z["h30_bolsa"] for z in r["dias"]) / cd(r)),
        ("ídem, con hambre > 60", "h", lambda r: sum(z["h60_bolsa"] for z in r["dias"]) / cd(r)),
        ("turnos despierta con hambre > 30 sin comida en ninguna parte (días 0 a 9)", "h", lambda r: sum(z["h30_nada"] for z in r["dias"]) / cd(r)),
        ("hambre al comer (media, días 0 a 9)", "h", lambda r: mean_([c["h"] for c in r["comidas"]])),
        ("comidas con 60 o más de hambre (parte, días 0 a 9)", "hp", lambda r: (sum(1 for c in r["comidas"] if c["h"] is not None and c["h"] >= 60) / len(r["comidas"])) if r["comidas"] else None),
        ("comida que le quitan a empujones (parte de lo nuevo que coge, días 0 a 9)", "hp", lambda r: (lambda L: sum(c["destino"] == "quitada" for c in L) / len(L) if L else None)([c for c in r["cogidas"] if c["de"] in X.FUERA_DESP])),
        ("comidas por criatura y día (días 0 a 9)", "h", lambda r: sum(z["comidas"] for z in r["dias"]) / cd(r)),
        ("vivas sin comida en la bolsa ni en la despensa, día 10 (por partida)", "v", lambda r: r.get("10", [None])[0]),
        ("vivas sin comida en la bolsa ni en la despensa, día 30 (por partida)", "v", lambda r: r.get("30", [None])[0])]
    def val(m, x):
        e, k, f = m
        if k is True or k is False: return f(A[x])
        return f(Vc[x] if k == "v" else H[x])
    def pc(m): return m[1] is True or m[1] == "hp"
    w = ["# El taller de la reserva: RG69r frente a la RG68r sellada (y la gemela)\n"]; J = {"medidas": {}}
    # ── la regla ──
    S2 = [(mu, s) for mu in ("sequia", "sequia_dura") for s in MUNDOS[mu]]; fa = M[-9][2]
    a69 = [fa(H[("RG69r",) + k]) for k in S2]; a68 = [fa(H[("RG68r",) + k]) for k in S2]; m69, m68 = sum(a69) / len(a69), sum(a68) / len(a68)
    rr = random.Random(8); bs = []
    for _ in range(NB):
        i = [rr.randrange(len(S2)) for _ in S2]; bs.append(sum(a69[k] for k in i) / max(1e-9, sum(a68[k] for k in i)))
    bs.sort(); ok1 = m69 <= 0.5 * m68 + 1e-9
    J["regla"] = {"a": {"RG69r": m69, "RG68r": m68, "cociente": m69 / m68, "ic": [bs[int(0.025 * NB)], bs[int(0.975 * NB) - 1]], "ok": ok1}, "b": {}}
    w += ["## La regla\n", f"**a) Mecanismo** (sequía y sequía dura juntas, días 0 a 9): turnos al día despierta con hambre > 30 y comida en la bolsa, RG69r {m69:.2f} frente a RG68r sellada {m68:.2f}; "
          f"el cociente es {m69 / m68:.3f} [{bs[int(0.025 * NB)]:.3f}, {bs[int(0.975 * NB) - 1]:.3f}] (hace falta 0,5 o menos): ".replace(".", ",") + f"{'se cumple' if ok1 else 'no se cumple'}.\n",
          "**b) No hace daño** (en cada mundo, medias de las partidas, RG69r − RG68r sellada):\n", "| mundo | vivas el día 40 (≥ −0,2) | felicidad de la aldea (≥ −0,03) | empujones RG69r / RG68r (≤ 1,25) | se cumple |", "|---|---|---|---|---|"]
    ok2 = True
    for mu, S in MUNDOS.items():
        mv = lambda j, k: AN.media([A[(j, mu, s)][k] for s in S])
        dv = mv("RG69r", "vivas40") - mv("RG68r", "vivas40"); df = mv("RG69r", "feliz_aldea") - mv("RG68r", "feliz_aldea"); qe = mv("RG69r", "empujones") / max(1e-9, mv("RG68r", "empujones"))
        o = dv >= -0.2 - 1e-9 and df >= -0.03 - 1e-9 and qe <= 1.25 + 1e-9; ok2 = ok2 and o; J["regla"]["b"][mu] = {"vivas": dv, "feliz": df, "empujones": qe, "ok": o}
        w.append(f"| {NOMBRE[mu]} | {dv:+.2f} | {df:+.3f} | {qe:.2f} ({mv('RG69r', 'empujones'):.1f} / {mv('RG68r', 'empujones'):.1f}) | {'sí' if o else 'no'} |".replace(".", ","))
    J["regla"]["pasa"] = ok1 and ok2; w.append(f"\n**La regla {'PASA' if ok1 and ok2 else 'NO PASA'}.**\n")
    # ── por mundo ──
    for mu, S in MUNDOS.items():
        w += [f"## {NOMBRE[mu]} ({len(S)} semillas)\n", "| medida | RG69r | RG68r | gemela | RG69r − RG68r [95 %] | RG69r − gemela [95 %] |", "|---|---|---|---|---|---|"]
        for m in M:
            vs = {j: [val(m, (j, mu, s)) for s in S] for j in ("RG69r", "RG68r", "gemela")}
            d1 = AN.boot([a - b for a, b in zip(vs["RG69r"], vs["RG68r"]) if a is not None and b is not None])
            d2 = AN.boot([a - b for a, b in zip(vs["RG69r"], vs["gemela"]) if a is not None and b is not None])
            mm = {j: AN.media(v) for j, v in vs.items()}; J["medidas"][f"{mu}|{m[0]}"] = {"valores": mm, "difs": {"RG68r": d1, "gemela": d2}}
            fm = (lambda x: "—" if x is None else f"{100 * x:.1f} %") if pc(m) else (lambda x: "—" if x is None else f"{x:.2f}")
            w.append(f"| {m[0]} | {fm(mm['RG69r'])} | {fm(mm['RG68r'])} | {fm(mm['gemela'])} | {AN.f_(d1, 1, True) if pc(m) else AN.f_(d1)} | {AN.f_(d2, 1, True) if pc(m) else AN.f_(d2)} |".replace(".", ","))
        w.append("")
    RV = {}
    for mu, S in MUNDOS.items():
        for s in S:
            p_ = os.path.join(TALLER, f"RG69r_{mu}+sabores_s{s}_d40", "reserva_v69.json")
            if os.path.exists(p_): RV[(mu, s)] = sum(x["con_reserva"] for x in json.load(open(p_)).values())
    w.append(f"**Las fotos de comer que usaron la reserva** (RG69r, por partida de 40 días): media {sum(RV.values()) / max(1, len(RV)):.0f}.")
    open(os.path.join(AQUI, "analiza_rg69.md"), "w").write("\n".join(w) + "\n"); json.dump(J, open(os.path.join(AQUI, "analiza_rg69.json"), "w"), ensure_ascii=False, default=list)
    print("\n".join(w))

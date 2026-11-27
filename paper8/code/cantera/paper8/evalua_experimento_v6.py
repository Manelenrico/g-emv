"""[P8] Prompt 149 (preparado; el experimento NO se ha lanzado): la evaluación del experimento v6, el de la reserva y la voz (valle_experimento_v6: el tonto, el
recolector, RG68r, RG068r, RG69r y la protagonista RG69r+voz, «RG69rvoz» en las carpetas; los cinco mundos con el árbol; semillas 30161-30200; 40 días), con
las medidas de predicciones_v6_borrador.md (sección «Cómo se mide»). Es evalua_experimento_v5.py (prompt 134) con los jugadores nuevos y las medidas nuevas.
Solo lee.
LO QUE SE QUEDA DEL V5 (sus piezas, importadas con la carpeta cambiada, sin cambiar ninguna medida ni ningún umbral): cierre_v46 (vivas, causas, bestia a la
vista, dar, conductas, empujones), diag_v47 (dormir: dónde), analiza_v45 (la reconstrucción tras perder a la hermana), analiza_arbol_v50 (el árbol),
medida_v4/dormir_v4 (P9) y, de evalua_experimento_v5, p13_15 (P13, M8 y las rachas de P17), v5 (los despertares de P18, la felicidad de la aldea) y p11 (M9,
la antigua P11, con su muestreo y su semilla «8|RG68r|<mundo>» palabra por palabra, leída en las decisiones de la protagonista). P1 a P9, P12, P13, P16 y P17 se
miden en la protagonista en el sitio de RG68r y se dicen también para RG69r y RG68r, sin contar como predicción.
LO NUEVO (las medidas de los talleres, importadas): voz_a_casa_v1/analiza_vc1.una (prompt 143: las noches fuera de los días 0 a 9 de dormir_fuera_v5/noches_v5,
el hambre al empezar el día 10, los turnos al frío); hambre_ganancias_v1/extrae_hg_v1.una (prompt 144: días 0 a 9, los turnos despierta con hambre > 30 y
comida en la bolsa, la comida que le quitan a empujones); las vivas sin comida en la bolsa ni en la despensa (prompt 146, reserva_v1/analiza_rg69.vacias, aquí
con el hambre al empezar el día 30 en la misma pasada); y voz_a_casa_v1/voces_v1.voces (prompt 143: la voz).
DOS MODOS:
   python3 evalua_experimento_v6.py              -> el experimento (valle_experimento_v6) -> salida/evalua_experimento_v6.md y .json
   python3 evalua_experimento_v6.py talleres     -> (prompt 149, punto 2) las partidas de los talleres frente a lo sellado del v5 en las mismas semillas: RG69r en
        valle_rg69_taller (146 y la abundancia del 149), RG69r+voz en valle_vr1_taller (147 y la abundancia del 149), los demás en valle_experimento_v5; sequía
        y sequía dura 30121-30140, abundancia, normal y bestias que crían 30121-30130 -> salida/evalua_talleres_v6.md y .json
   En el modo talleres hay menos de 200 partidas por jugador: P13 y P17 («4 o menos de 200») se cuentan en proporción (≤ 2 de cada 100), solo para el informe de
   los talleres. En el experimento son «4 o menos de las 200», como en el v5 (prompt 150).
M14 (prompt 150): las muertes por causa (hambre, bestia, frío, otras), por mundo y por época, en las cuatro clases de criatura (ver su tabla).
LO CERCA DEL UMBRAL (punto 2 del prompt 149, solo se informa): el margen es (valor − umbral) / |umbral|, del lado en que se cumple (negativo si no se cumple);
con varios mundos, el peor. Cuando el umbral es cero (un límite del intervalo sobre o bajo cero, cero muertes), el margen es el límite partido por la media
(cuánto del efecto queda por encima de cero); en P3 (contar muertes) no hay margen. «Cerca»: margen de menos del 20 %."""
import gzip, json, math, os, random, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
for p_ in ("voz_a_casa_v1", "hambre_ganancias_v1", "dormir_fuera_v5", "medida_v4", "reserva_v1"): sys.path.insert(0, os.path.join(AQUI, p_))
import evalua_experimento_v5 as EV                                              # (primero: al importarse fija las rutas del v5 en sus piezas; aquí se cambian después)
C46, D47, A45, AA, A44, DV4 = EV.C46, EV.D47, EV.A45, EV.AA, EV.A44, EV.DV4
import analiza_vc1 as AN
import extrae_hg_v1 as X
import voces_v1 as VV
MODO = "talleres" if len(sys.argv) > 1 and sys.argv[1] == "talleres" else "experimento"
T7 = "/Volumes/Mem G-EMV"; DIA = C46.DIA; NB = EV.NB; FLACA = EV.FLACA
MUNDOS = EV.MUNDOS; PROTA = "RG69rvoz"; CRI = ("RG68r", "RG068r", "RG69r", "RG69rvoz"); BASE = ("tonto", "recolector"); JUG = BASE + CRI
NOM = {"RG69rvoz": "RG69r+voz"}; nom = lambda v: NOM.get(v, v); QUIEN = (PROTA, "RG69r", "RG68r")
if MODO == "experimento":
    EXP = os.path.join(T7, "valle_experimento_v6"); SEMM = {mu: range(30161, 30201) for mu in MUNDOS}; CARPETA = {v: EXP for v in JUG}
    SAL = "evalua_experimento_v6"; PROP = 1.0
else:
    V5 = os.path.join(T7, "valle_experimento_v5"); CARPETA = {v: V5 for v in JUG}; CARPETA["RG69r"] = os.path.join(T7, "valle_rg69_taller"); CARPETA[PROTA] = os.path.join(T7, "valle_vr1_taller")
    SEMM = {mu: range(30121, 30141 if mu in ("sequia", "sequia_dura") else 30131) for mu in MUNDOS}; SAL = "evalua_talleres_v6"; PROP = None
CACHE = os.path.join(AQUI, "evalua_v6", MODO)
for d_ in ("partidas", "noches", "datos"): os.makedirs(os.path.join(CACHE, d_), exist_ok=True)
def ruta(v, mu, s): return os.path.join(CARPETA[v], f"{v}_{mu}+sabores_s{s}_d40" if v not in BASE else f"{v}_{mu}_s{s}_d40")
EV.ruta = ruta; C46.ruta = ruta; D47.ruta = ruta; EV.TC.ruta = ruta; EV.SEM = range(min(min(S) for S in SEMM.values()), max(max(S) for S in SEMM.values()) + 1)
A45.carpeta = lambda v, mu, s: ruta(v, mu.replace("+sabores", ""), s)
AN.OUT = os.path.join(CACHE, "partidas"); AN.AQUI = CACHE; AN.CARP.update({v: (CARPETA[v], v) for v in CRI}); X.AQUI = CACHE

def hecho(v, mu, s): return os.path.exists(os.path.join(ruta(v, mu, s), "fin.json"))
def c46(x): return C46.una(x)
def d47(x): return D47.una(x)
def arbol(x):
    v, mu, s = x; AA.P51 = CARPETA[v]; return AA.una((v, mu + "+sabores" if v not in BASE else mu, s))
def rec45(x):
    v, mu, s = x; r = A45.una((v, mu + "+sabores", s)); return {"v": v, "mu": mu, "s": s, "rec": r["rec"]}
def dormir9(x):
    v, mu, s = x; return dict(DV4.una(ruta(v, mu, s), s), v=v, mu=mu, s=s)
def p13(x): EV.ruta = ruta; return EV.p13_15(x)
def v5m(x): EV.ruta = ruta; return {k: y for k, y in EV.v5(x).items() if k != "P"}

def escasez(x):
    """(M11, P27) al empezar el día 10 y el día 30: las vivas, las vivas sin comida en la bolsa ni en la despensa de su casa (como reserva_v1/analiza_rg69.vacias)
    y el hambre media de las vivas; de fin.json, las muertes de hambre en los días 10 a 14 y 30 a 34"""
    v, mu, s = x; d = ruta(v, mu, s); out = {}
    for lm, lc in zip(gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"), gzip.open(os.path.join(d, "criaturas.jsonl.gz"), "rt", encoding="utf-8")):
        m = json.loads(lm); t = m["turno"]
        if t > 30 * DIA: break
        if t in (10 * DIA, 30 * DIA):
            c = json.loads(lc); V = [(a, g) for a, g in m["agentes"].items() if a != "bestia" and isinstance(g, dict) and "cuerpo" in g and not g["cuerpo"]["muerta"]]
            out[str(t // DIA)] = {"vacias": sum(1 for a, g in V if "comida" not in (g.get("bolsa") or []) and (c.get("despensas") or {}).get(a[0], {}).get("comida", 0) == 0),
                                  "vivas": len(V), "hambre": sum(g["cuerpo"]["hambre"] for _, g in V) / len(V) if V else None}
    fin = json.load(open(os.path.join(d, "fin.json")))
    for d0 in (10, 30): out[f"muertes_hambre_{d0}"] = sum(1 for z in fin["muertes"] if z["causa"] == "hambre" and d0 <= z["dia"] <= d0 + 4)
    return out
def nuevas(x):
    """las medidas de los talleres de una partida de criatura: las del 143 (analiza_vc1.una), las del 144 (extrae_hg_v1.una), escasez y la voz"""
    v, mu, s = x; a = json.load(open(AN.una(x))); X.EXP = CARPETA[v]; h = json.load(open(X.una(x)))
    cd = max(1, sum(1 for z in h["dias"] if z["turnos"])); cog = [c for c in h["cogidas"] if c["de"] in X.FUERA_DESP]
    r = {"v": v, "mu": mu, "s": s, "noches10": a["noches10"], "h10": a["h10"], "frio": a["frio"], "vivas40": a["vivas40"], "empujones_143": a["empujones"],
         "h30_bolsa": sum(z["h30_bolsa"] for z in h["dias"]) / cd, "cogidas": len(cog), "quitadas": sum(c["destino"] == "quitada" for c in cog), "escasez": escasez(x)}
    if v == PROTA:
        vs, oye, _ = VV.voces(ruta(v, mu, s))
        r["voz"] = {"voces": len(vs), "devueltas": sum(z["devuelta"] for z in vs), "dos_en_casa": sum(z["dos_en_casa"] for z in vs), "ya_era": sum(z["ya_era"] for z in vs),
                    "decisiones_oyendo": len(oye), "cambio": sum(o["cambio"] for o in oye), "n_cd": a["n_cd"]}
    return r

boot = EV.boot
fb = lambda b: f"{b['media']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]"
def zm(bound, media):
    """el margen cuando el umbral es cero: el límite partido por la media"""
    return bound / abs(media) if media else (0.0 if bound == 0 else math.copysign(math.inf, bound))
rel = lambda valor, umbral: (valor - umbral) / abs(umbral)


if __name__ == "__main__":
    T_ = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEMM[mu] if hecho(v, mu, s)]
    if MODO == "talleres": T_ = [x for x in T_ if x[0] in (PROTA, "RG69r") or hecho("RG69r", x[1], x[2])]   # (las semillas que tienen los talleres)
    TC_ = [x for x in T_ if x[0] in CRI]
    with Pool(8) as p:
        RC = p.map(c46, T_); RD = p.map(d47, [x for x in T_ if x[0] in ("tonto",) + CRI]); RA = p.map(arbol, [x for x in T_ if x[0] in ("recolector", "tonto") + CRI])
        RR = p.map(rec45, [x for x in T_ if x[0] in QUIEN]); RN = p.map(dormir9, [x for x in T_ if x[0] in QUIEN]); RP = p.map(p13, TC_)
        RV = p.map(v5m, TC_); RW = p.map(nuevas, TC_)
    EV.ruta = lambda v, mu, s: ruta(PROTA, mu, s)                              # (M9: la medida de P11 del v5, en las decisiones de la protagonista)
    M9 = EV.p11(); M9s = EV.p11(quita_ir=True); M9d = EV.p11(quita_dar=True)
    by = defaultdict(list); viv = {}
    for r in RC: by[(r["v"], r["mu"])].append(r); viv[(r["v"], r["mu"], r["s"])] = r["vivas"]
    bya = defaultdict(list)
    for r in RA: bya[(r["v"], r["mu"].split("+")[0])].append(r)
    rv = {(r["v"], r["mu"], r["s"]): r for r in RV}; rw = {(r["v"], r["mu"], r["s"]): r for r in RW}
    par = lambda a, b, mu: boot([viv[(a, mu, s)] - viv[(b, mu, s)] for s in SEMM[mu] if (a, mu, s) in viv and (b, mu, s) in viv])
    npart = Counter(r["v"] for r in RC); out = []; w = out.append; RES = {}
    def apunta(k, quien, ok, texto, margen=None, cuenta=True):
        cerca = margen is not None and abs(margen) < 0.2
        RES[f"{k}|{quien}"] = {"pred": k, "quien": nom(quien), "cumple": bool(ok), "margen": margen, "cerca": cerca, "cuenta": cuenta, "texto": texto}
        w(f"**{k}{' · ' + nom(quien) if quien else ''}** ({'CUMPLE' if ok else 'FALLA'}{'; CERCA DEL UMBRAL' if cerca else ''}"
          f"{'' if margen is None else f'; margen {100 * margen:+.0f} %'}{'' if cuenta else '; no cuenta como predicción'}). {texto}\n")
    w(f"# Evaluación del v6 ({'el experimento' if MODO == 'experimento' else 'los talleres frente a lo sellado del v5, en las mismas semillas'})\n")
    w("Partidas leídas: " + ", ".join(f"{nom(v)} {npart[v]}" for v in JUG) + ".\n"); w("## Las predicciones que se quedan (en la protagonista; también en RG69r y RG68r, sin contar)\n")
    for X_ in QUIEN:
        cu = X_ == PROTA
        d1 = {mu: par(X_, "tonto", mu) for mu in ("sequia", "sequia_dura", "bestias_crian")}; ok = all(b["media"] >= 1 and b["lo"] > 0 for b in d1.values())
        apunta("P1", X_, ok, f"Vivas {nom(X_)} − tonto: " + "; ".join(f"{mu} {fb(b)}" for mu, b in d1.items()) + ".", min(min(rel(b["media"], 1), zm(b["lo"], b["media"])) for b in d1.values()), cu)
        m2 = {mu: sum(r["vivas"] for r in by[(X_, mu)]) / max(1, len(by[(X_, mu)])) for mu in ("abundancia", "normal")}; ok = all(x >= 7.5 for x in m2.values())
        apunta("P2", X_, ok, f"Vivas: " + "; ".join(f"{mu} {x:.2f}" for mu, x in m2.items()) + f". (Declarado: en el normal, {nom(X_)} − tonto = {fb(par(X_, 'tonto', 'normal'))}.)", min(rel(x, 7.5) for x in m2.values()), cu)
        g3 = sum(r["causas"].get("golpe", 0) for r in RC if r["v"] == X_); g3t = sum(r["causas"].get("golpe", 0) for r in RC)
        apunta("P3", X_, g3t == 0, f"Muertes por golpe: en las partidas de {nom(X_)}, {g3}; en todas las leídas ({len(RC)}), {g3t}.", None, cu)
        fr = {}
        for v in (X_, "tonto"):
            C = sum((Counter(r["C"]) for mu in MUNDOS for r in by[(v, mu)]), Counter()); fr[v] = C["bestia_vista_junta"] / max(1, C["bestia_vista"])
        q = fr[X_] / max(1e-9, fr["tonto"])
        apunta("P4", X_, fr[X_] >= 3 * fr["tonto"], f"Con la bestia a la vista, con otra pegada (los cinco mundos): {nom(X_)} {100 * fr[X_]:.1f} %, tonto {100 * fr['tonto']:.1f} % (×{q:.1f}).", rel(q, 3), cu)
        L_ = by[(X_, "bestias_crian")]; e5 = sum(r["b"]["C"].get("bestia_echada", 0) for r in L_) / max(1, len(L_))
        apunta("P5", X_, e5 >= 1, f"Echadas por partida en bestias que crían: {e5:.2f}.", rel(e5, 1), cu)
        p6 = {}
        for mu in MUNDOS:
            D = sum((Counter(r["dar"]) for r in by[(X_, mu)]), Counter()); p6[mu] = (sum(n for k, n in D.items() if k.startswith("comida|hermana")), sum(n for k, n in D.items() if k.startswith("comida|vecina")) / 6)
        apunta("P6", X_, all(h > v6 for h, v6 in p6.values()), "Comida dada a la hermana · a cada vecina: " + "; ".join(f"{mu} {h} · {v6:.1f}" for mu, (h, v6) in p6.items()) + ".",
               min(rel(h, v6) if v6 else (math.inf if h > 0 else 0.0) for h, v6 in p6.values()), cu)
        p7 = {}
        for mu in MUNDOS:
            D = sum((Counter(r["dar"]) for r in by[(X_, mu)]), Counter()); tot = sum(n for k, n in D.items() if k.startswith("comida|"))
            p7[mu] = sum(n for k, n in D.items() if k.startswith("comida|") and "|necesita|" in k) / max(1, tot)
        apunta("P7", X_, p7["sequia"] > p7["abundancia"] and p7["sequia_dura"] > p7["abundancia"], "Parte de lo dado a quien estaba flaca: " + "; ".join(f"{mu} {100 * x:.0f} %" for mu, x in p7.items()) + ".",
               min(rel(p7[m], p7["abundancia"]) if p7["abundancia"] else math.inf for m in ("sequia", "sequia_dura")), cu)
        d8 = []
        for r in RR:
            if r["v"] != X_: continue
            for z in r["rec"]:
                dd = [z["despues"][k] for k in z["despues"] if int(k) <= 5]
                if dd: d8.append(sum(dd) / len(dd) - z["antes"])
        b8 = boot(d8) if len(d8) > 1 else None; ok = bool(b8 and b8["media"] > 0 and b8["lo"] > 0)
        apunta("P8", X_, ok, f"Pegada a una vecina, 5 días después − 5 antes de perder a la hermana: {fb(b8) if b8 else '—'} (n={len(d8)} criaturas).", zm(b8["lo"], b8["media"]) if b8 else None, cu)
        p9 = {}; pu9 = Counter()
        for mu in MUNDOS:
            C = sum((Counter({k: x for k, x in r.items() if isinstance(x, int)}) for r in RN if r["mu"] == mu and r["v"] == X_), Counter()); p9[mu] = C["dentro"] / max(1, C["noches"])
            for k in ("puerta", "puerta_agotada", "puerta_sin_agotar"): pu9[k] += C[k]
        apunta("P9", X_, all(x >= 0.55 for x in p9.values()) and pu9["puerta_sin_agotar"] == 0, "La primera vez que se duerme cada noche, dentro de su casa: " + "; ".join(f"{mu} {100 * x:.0f} %" for mu, x in p9.items())
               + f". En una puerta: {pu9['puerta']} ({pu9['puerta_agotada']} agotada, **{pu9['puerta_sin_agotar']} sin estar agotada**).", min(rel(x, 0.55) for x in p9.values()), cu)
        def fruta(v):
            A_ = Counter()
            for mu in MUNDOS:
                for r in bya[(v, mu)]:
                    for k in ("frutos_puestos", "frutos_se_pierden"): A_[k] += r["AR"].get(k, 0)
            return (A_["frutos_puestos"] - A_["frutos_se_pierden"]) / max(1, A_["frutos_puestos"])
        fX, fC = fruta(X_), fruta("recolector")
        apunta("P12", X_, fX < 0.15 and fX < fC, f"Fruta del árbol cogida: {nom(X_)} {100 * fX:.1f} %, recolector {100 * fC:.1f} %.", min(-rel(fX, 0.15), -rel(fX, fC) if fC else math.inf), cu)
        RX = [r for r in RP if r["v"] == X_]; n13 = sum(1 for r in RX if r["ultima"] > 0); lim = 4 if MODO == "experimento" else 0.02 * len(RX)
        apunta("P13", X_, n13 <= lim, f"Partidas con algún «dar la última comida» con hambre > {FLACA}: {n13} de {len(RX)} (el límite, 2 de cada 100: {lim:.1f}).", (lim - n13) / lim if lim else None, cu)
        em = {(v, mu): sum(r["C"].get("empujar", 0) for r in by[(v, mu)]) / max(1, len(by[(v, mu)])) for v in (X_, "RG068r") for mu in MUNDOS}
        apunta("P16", X_, all(em[(X_, mu)] > em[("RG068r", mu)] for mu in MUNDOS), f"Empujones a otras por partida, {nom(X_)} · RG068r: " + "; ".join(f"{mu} {em[(X_, mu)]:.0f} · {em[('RG068r', mu)]:.0f} (×{em[(X_, mu)] / max(1e-9, em[('RG068r', mu)]):.1f})" for mu in MUNDOS) + ".",
               min(rel(em[(X_, mu)], em[("RG068r", mu)]) for mu in MUNDOS), cu)
        n17 = sum(1 for r in RX if r["racha"].get("comida|lt40", 0) > 10 or r["racha"].get("medicina|lt40", 0) > 10); lim = 4 if MODO == "experimento" else 4 * len(RX) / 200
        mx = max((max(r["racha"].get("comida|lt40", 0), r["racha"].get("medicina|lt40", 0)) for r in RX), default=0)
        apunta("P17", X_, n17 <= lim, f"Partidas con alguna racha de ida y vuelta de más de 10: {n17} de {len(RX)} (el límite, 4 de cada 200: {lim:.1f}); la racha más larga: {mx}.", (lim - n17) / lim if lim else None, cu)
        dv = {mu: (lambda L_: sum(r["desp"].get("voz", 0) for r in L_) / max(1, sum(r["noches"] for r in L_)))([r for r in RV if r["v"] == X_ and r["mu"] == mu]) for mu in MUNDOS}
        apunta("P18", X_, all(x < 1 for x in dv.values()), "Despertares por voz por criatura y noche: " + "; ".join(f"{mu} {x:.2f}" for mu, x in dv.items()) + ".", min(-rel(x, 1) for x in dv.values()), cu)
    b10 = {mu: par("RG068r", "RG68r", mu) for mu in ("sequia", "sequia_dura")}
    apunta("P10", "", all(b["hi"] >= 0 for b in b10.values()), "Vivas RG068r − RG68r: " + "; ".join(f"{mu} {fb(b)}" for mu, b in b10.items()) + ".", min(zm(b["hi"], b["media"]) for b in b10.values()))
    # ── las nuevas ──
    w("## Las predicciones nuevas\n")
    S2 = [(mu, s) for mu in ("sequia", "sequia_dura") for s in SEMM[mu]]
    def media_h30(v): L_ = [rw[(v,) + k]["h30_bolsa"] for k in S2 if (v,) + k in rw]; return sum(L_) / len(L_) if L_ else float("nan")
    h69, h68, hp = media_h30("RG69r"), media_h30("RG68r"), media_h30(PROTA)
    apunta("P24", "RG69r", h69 <= 0.5 * h68, f"Sequía y sequía dura, días 0 a 9, turnos al día despierta con hambre > 30 y comida en la bolsa: RG69r {h69:.2f}, RG68r {h68:.2f} (cociente {h69 / h68:.3f}; hace falta 0,5 o menos).", -rel(h69 / h68, 0.5))
    b25 = par("RG69r", "RG68r", "sequia_dura")
    apunta("P25", "RG69r", b25["lo"] > 0, f"Sequía dura, vivas RG69r − RG68r: {fb(b25)}.", zm(b25["lo"], b25["media"]))
    def no_dana(a, b, k):
        partes = {}; ok = True; mg = math.inf
        for mu in MUNDOS:
            bv = par(a, b, mu); fa = [rv[(a, mu, s)]["feliz_aldea"] - rv[(b, mu, s)]["feliz_aldea"] for s in SEMM[mu] if (a, mu, s) in rv and (b, mu, s) in rv and rv[(a, mu, s)]["feliz_aldea"] is not None and rv[(b, mu, s)]["feliz_aldea"] is not None]
            df = sum(fa) / len(fa) if fa else float("nan"); ea = [r["C"].get("empujar", 0) for r in by[(a, mu)]]; eb = [r["C"].get("empujar", 0) for r in by[(b, mu)]]
            qe = (sum(ea) / max(1, len(ea))) / max(1e-9, sum(eb) / max(1, len(eb))); o = bv["hi"] >= 0 and df >= -0.03 and qe <= 1.25; ok = ok and o
            mg = min(mg, zm(bv["hi"], bv["media"]), rel(df, -0.03), -rel(qe, 1.25)); partes[mu] = (bv, df, qe, o)
        apunta(k, a, ok, f"{nom(a)} frente a {nom(b)}, por mundo (vivas; felicidad de la aldea, media; empujones, cociente): " + "; ".join(f"{mu} {fb(bv)}; {df:+.3f}; ×{qe:.2f}{'' if o else ' (NO)'}" for mu, (bv, df, qe, o) in partes.items()) + ".", mg)
    no_dana("RG69r", "RG68r", "P26")
    vac = lambda v: [rw[(v, "sequia_dura", s)]["escasez"].get("10", {}).get("vacias") for s in SEMM["sequia_dura"] if (v, "sequia_dura", s) in rw]
    v69, v68 = vac("RG69r"), vac("RG68r"); m69, m68 = sum(v69) / max(1, len(v69)), sum(v68) / max(1, len(v68))
    apunta("P27", "RG69r", m69 > m68, f"Sequía dura, vivas al empezar el día 10 con la bolsa y la despensa vacías, por partida: RG69r {m69:.2f}, RG68r {m68:.2f}.", rel(m69, m68) if m68 else None)
    nf = lambda v: [rw[(v,) + k]["noches10"] for k in S2 if (v,) + k in rw]
    pn = lambda v: sum(a for a, _ in nf(v)) / max(1, sum(b for _, b in nf(v))); qn = pn(PROTA) / max(1e-9, pn("RG69r"))
    apunta("P28", PROTA, qn <= 2 / 3, f"Sequía y sequía dura, días 0 a 9, noches dormidas fuera: {nom(PROTA)} {100 * pn(PROTA):.1f} %, RG69r {100 * pn('RG69r'):.1f} % (cociente {qn:.3f}; hace falta 0,667 o menos).", -rel(qn, 2 / 3))
    apunta("P29", PROTA, hp <= 0.5 * h68, f"La medida de P24 en {nom(PROTA)}: {hp:.2f}, RG68r {h68:.2f} (cociente {hp / h68:.3f}; hace falta 0,5 o menos).", -rel(hp / h68, 0.5))
    no_dana(PROTA, "RG69r", "P30")
    b31 = par(PROTA, "RG68r", "sequia_dura")
    apunta("P31", PROTA, b31["lo"] > 0, f"Sequía dura, vivas {nom(PROTA)} − RG68r: {fb(b31)}.", zm(b31["lo"], b31["media"]))
    pr = [z for z in RES.values() if z["cuenta"]]
    w(f"**Cuentan como predicción {len(pr)}; se cumplen {sum(z['cumple'] for z in pr)}.** Fallan: {', '.join(z['pred'] for z in pr if not z['cumple']) or 'ninguna'}. Cerca del umbral (menos del 20 %): {', '.join(z['pred'] + ' ' + z['quien'] for z in pr if z['cerca']) or 'ninguna'}.\n")
    # ── las medidas sin predicción ──
    w("## Medidas sin predicción\n")
    nn = lambda d: d["media"] if d["media"] is not None else float("nan")
    w(f"**M9** (era P11). Coincidencia de {nom(PROTA)} con las sumas, Q4 − Q1: {nn(M9):+.3f} [{M9['lo']:+.3f}, {M9['hi']:+.3f}] ({M9['n_decisiones']} decisiones de {M9['n_partidas']} partidas). "
      f"Sin las decisiones de dar: {nn(M9d):+.3f} [{M9d['lo']:+.3f}, {M9d['hi']:+.3f}]. Sin las de ir: {nn(M9s):+.3f} [{M9s['lo']:+.3f}, {M9s['hi']:+.3f}].\n")
    w(f"**M10.** Vivas {nom(PROTA)} − RG068r: " + "; ".join(f"{mu} {fb(par(PROTA, 'RG068r', mu))}" for mu in MUNDOS) + ".\n")
    M11 = {}
    w("**M11** (por partida; medias de las partidas):\n\n| mundo | jugador | hambre al empezar el día 10 | y el 30 | muertes de hambre, días 10 a 14 | y 30 a 34 | vivas sin reserva al empezar el día 10 | y el 30 |\n|---|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in CRI:
            Z = [rw[(v, mu, s)]["escasez"] for s in SEMM[mu] if (v, mu, s) in rw]; mm = lambda f: (lambda L_: sum(L_) / len(L_) if L_ else float("nan"))([q for q in map(f, Z) if q is not None])
            M11[f"{v}|{mu}"] = r_ = {"h10": mm(lambda z: z.get("10", {}).get("hambre")), "h30": mm(lambda z: z.get("30", {}).get("hambre")), "mh10": mm(lambda z: z["muertes_hambre_10"]),
                                     "mh30": mm(lambda z: z["muertes_hambre_30"]), "v10": mm(lambda z: z.get("10", {}).get("vacias")), "v30": mm(lambda z: z.get("30", {}).get("vacias"))}
            w(f"| {mu} | {nom(v)} | {r_['h10']:.1f} | {r_['h30']:.1f} | {r_['mh10']:.2f} | {r_['mh30']:.2f} | {r_['v10']:.2f} | {r_['v30']:.2f} |")
    M12 = {}
    w(f"\n**M12** (la voz de {nom(PROTA)}, por partida):\n\n| mundo | voces | por criatura y día | se devuelven | las dos en casa | «ir a casa» ya era lo elegido | decisiones oyendo en que cambió lo elegido |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        Z = [rw[(PROTA, mu, s)]["voz"] for s in SEMM[mu] if (PROTA, mu, s) in rw]
        if not Z: continue
        t = lambda k: sum(z[k] for z in Z); nv = max(1, t("voces")); M12[mu] = {k: t(k) / len(Z) for k in Z[0]}
        w(f"| {mu} | {t('voces') / len(Z):.1f} | {t('voces') / max(1, t('n_cd')):.2f} | {100 * t('devueltas') / nv:.0f} % | {100 * t('dos_en_casa') / nv:.0f} % | {100 * t('ya_era') / nv:.0f} % | {100 * t('cambio') / max(1, t('decisiones_oyendo')):.0f} % |")
    M13 = {}
    w("\n**M13** (la comida que le quitan a empujones, parte de lo que coge, días 0 a 9; los turnos al frío fuera de casa, por criatura y día):\n\n| mundo | " + " | ".join(nom(v) for v in CRI) + " |\n|" + "---|" * (len(CRI) + 1))
    for mu in MUNDOS:
        cel = []
        for v in CRI:
            Z = [rw[(v, mu, s)] for s in SEMM[mu] if (v, mu, s) in rw]; q_ = sum(z["quitadas"] for z in Z) / max(1, sum(z["cogidas"] for z in Z)); fr_ = sum(z["frio"] for z in Z) / max(1, len(Z))
            M13[f"{v}|{mu}"] = {"quitada": q_, "frio": fr_}; cel.append(f"{100 * q_:.1f} % · {fr_:.1f}")
        w(f"| {mu} | " + " | ".join(cel) + " |")
    # (M14, prompt 150) las muertes por causa y por época. La época es la del calendario de las épocas del mundo (config_valle.json, matorrales.epocas:
    # sus días por época y sus nombres, leídos de la config) en el día de la muerte (fin.json), también en los mundos que no tienen las épocas encendidas.
    # «frío» es la causa «frio» o «frío» del registro; «otras», cualquier otra que no sea hambre ni bestia (golpe, terreno…)
    EPC = json.load(open(os.path.join(os.path.dirname(os.path.dirname(AQUI)), "valle", "config_valle.json"), encoding="utf-8"))["matorrales"]["epocas"]
    epoca = lambda dia: EPC["nombres"][(dia // EPC["duracion_dias"]) % len(EPC["factores"])]; EPS = list(dict.fromkeys(EPC["nombres"]))
    caus = lambda c: "hambre" if c == "hambre" else "bestia" if c == "bestia" else "frio" if c in ("frio", "frío") else "otras"; CAUS = ("hambre", "bestia", "frio", "otras")
    M14 = {}
    w("\n**M14** (muertes por causa y por época, sumadas en las partidas de cada mundo; hambre · bestia · frío · otras):\n\n| mundo | jugador | partidas | "
      + " | ".join(f"época {e}" for e in EPS) + " | todas |\n|" + "---|" * (len(EPS) + 4))
    for mu in MUNDOS:
        for v in CRI:
            Z = Counter(); n_ = 0
            for s in SEMM[mu]:
                if (v, mu, s) not in viv: continue
                n_ += 1
                for z in json.load(open(os.path.join(ruta(v, mu, s), "fin.json")))["muertes"]: Z[(caus(z["causa"]), epoca(z["dia"]))] += 1
            M14[f"{v}|{mu}"] = {"partidas": n_, **{f"{k}|{e}": Z[(k, e)] for k in CAUS for e in EPS}}
            w(f"| {mu} | {nom(v)} | {n_} | " + " | ".join(" · ".join(str(Z[(k, e)]) for k in CAUS) for e in EPS) + " | " + " · ".join(str(sum(Z[(k, e)] for e in EPS)) for k in CAUS) + " |")
    R58 = [r for r in RP if r["v"] == PROTA]; p14 = {}
    for mu in MUNDOS:
        X2 = [z for r in R58 if r["mu"] == mu for z in r["P14"]]; L1 = [z[1] for z in X2 if z[0] == "ladrona"]; L0 = [z[1] for z in X2 if z[0] == "nunca"]
        if L1: p14[mu] = (sum(L1) / len(L1), sum(L0) / max(1, len(L0)), len(L1), len(L0))
    w(f"\n**M8** (no sabemos qué saldrá). Comida por día que recibe una vecina de {nom(PROTA)}: las que le han robado · las que nunca: " + "; ".join(f"{mu} {a:.3f} · {b:.3f} ({n1} · {n0} pares)" for mu, (a, b, n1, n0) in p14.items()) + ".")
    vu = [z for mu in MUNDOS for r in bya[(PROTA, mu)] for z in r["recog"] if z["fase_vuelve"] is not None]
    w(f"\n**M7.** Vueltas del árbol de {nom(PROTA)} al anochecer o de noche: {100 * sum(1 for z in vu if z['fase_vuelve'] in ('anochecer', 'noche')) / max(1, len(vu)):.0f} % de {len(vu)}.\n")
    w("**M1 a M6, A1, A2 y A4** se calculan con los programas del v5 (medidas_v5, anadidas_v5, duelo_soledad_v5), que no están en este evaluador (como en el v5).\n")
    w("## Vivas al día 40 (de 8; media de las semillas)\n\n| mundo | " + " | ".join(nom(v) for v in JUG) + " |\n|" + "---|" * (len(JUG) + 1))
    for mu in MUNDOS: w(f"| {mu} | " + " | ".join(f"{sum(r['vivas'] for r in by[(v, mu)]) / max(1, len(by[(v, mu)])):.2f}" for v in JUG) + " |")
    w("\n## Muertes (hambre · bestia · golpe · terreno), sumadas\n\n| mundo | " + " | ".join(nom(v) for v in JUG) + " |\n|" + "---|" * (len(JUG) + 1))
    for mu in MUNDOS: w(f"| {mu} | " + " | ".join((lambda c: f"{c['hambre']} · {c['bestia']} · {c['golpe']} · {c['terreno']}")(sum((Counter(r["causas"]) for r in by[(v, mu)]), Counter())) for v in JUG) + " |")
    txt = "\n".join(out); open(os.path.join(AQUI, "salida", SAL + ".md"), "w").write(txt + "\n"); print(txt)
    json.dump({"modo": MODO, "predicciones": RES, "M9": M9, "M9_sin_ir": M9s, "M9_sin_dar": M9d, "M11": M11, "M12": M12, "M13": M13, "M14": M14, "partidas": dict(npart)},
              open(os.path.join(AQUI, "salida", SAL + ".json"), "w"), ensure_ascii=False, indent=1, default=str)

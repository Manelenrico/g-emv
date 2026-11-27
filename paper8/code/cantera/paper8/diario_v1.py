"""[P8] Prompt 135: el diario de un día de una criatura, en español llano y en el idioma del cuerpo, escrito a partir de los registros de una partida (solo lee):
mundo.jsonl.gz (lo que hace, dónde está, su cuerpo, su bolsa, los sucesos), criaturas.jsonl.gz (las llamadas que lanza, las despensas), balance.jsonl.gz (el sitio
y los tres balances: cuerpo, recursos, vínculo), diario.jsonl.gz (para qué va, adónde, lo que oye, a quién ve, las filas que más pesan; diarios_v1/lanza_diario_v1)
y arbol.json (dónde están los árboles dulces).
El día va por tramos: la mañana y la tarde, cada una en dos mitades, el anochecer y la noche. En cada tramo: dónde estuvo, con quién, qué hizo, qué le pasó y
cómo estaba en cuerpo, recursos y vínculo. Sin los números de las fuerzas: con palabras.
LAS PALABRAS (declaradas; no son números del cuerpo, son las bandas del diario):
  - el hambre: poca (< 30), algo (30 a 60), mucha (> 60: el umbral de flaca del mundo); harta si está por debajo de 0;
  - el cansancio: descansada (< 40), cansada (40 a 70), muy cansada (> 70: el umbral del compromiso);
  - la vida: entera (100), algo herida (70 a 100), herida (< 70: el umbral de herida del mundo);
  - «casi siempre», «la mitad», «a ratos», «un momento», según la parte del tramo (> 3/4, > 1/3, > 1/10, alguna vez);
  - los balances de cada dimensión: «bien» si la ganancia pasa a la pérdida, «mal» si no, con la parte del tramo despierta.
Al final, tres líneas de cuentas: los turnos del día, ir al árbol dulce y volver desde su casa (el más cercano de los dos, por el camino más corto desde la puerta,
como arbol_caminos.py), y la comida guardada en la despensa de su casa y en el almacén al acabar el día.
   python3 diario_v1.py <carpeta de la partida> <criatura> <día> [salida.md]"""
import gzip, json, os, sys
from collections import Counter, defaultdict
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, RAIZ)
from valle import mundo as MU
from valle.jugadores import Mapa, DIRS
_E = MU.Valle(); _o, _inf = _E.reset(seed=1); MAPA = Mapa(_inf[_E.agents[0]]["mapa"]); CFG = _E.cfg; DIA = int(CFG["dia"]["turnos"])
FLACA = float(CFG["criaturas"]["umbral_flaca"]); HERIDA = float(CFG["criaturas"]["umbral_herida"]); VIDA = float(CFG["criaturas"]["vida_max"])
TRAMOS = []
_t0 = 0
for _f, _n in CFG["dia"]["fases"]:
    if _f in ("mañana", "tarde"): TRAMOS += [(f"primera mitad de la {_f}", _t0, _t0 + _n // 2), (f"segunda mitad de la {_f}", _t0 + _n // 2, _t0 + _n)]
    else: TRAMOS.append((f"el {_f}" if _f == "anochecer" else f"la {_f}", _t0, _t0 + _n))
    _t0 += _n
her = lambda a: a[0] + ("2" if a[1] == "1" else "1"); cheb = lambda p, q: max(abs(p[0] - q[0]), abs(p[1] - q[1]))
SITIO = {"C": "en su casa", "O": "en otra casa", "P": "en la puerta de su casa", "bosque": "en el bosque", "huerto": "en el huerto", "aldea": "por la aldea",
         "camino": "por el camino", "salvaje": "en lo salvaje", "almacen": "junto al almacén"}
VA = {"ir_casa": "a casa", "ir_pareja": "con su hermana", "ir_objeto": "a coger algo que vio", "trabajar_planta": "a trabajar el huerto", "ir_matorral": "a un matorral que recordaba",
      "ir_botin": "al almacén a por comida", "ir_frontera": "a ver lo que no conocía", "ir_bosque": "al bosque", "ir_vecina": "con una vecina que lo necesitaba",
      "ir_llamada": "adonde llamaron «aquí hay comida»", "ir_bestia": "a por la bestia", "ir_ronda": "de ronda por los matorrales"}
PIERDE = {"F-HAMBRE": "el hambre", "F-CANSANCIO": "el cansancio", "F-FRIO": "el frío", "F-DANO": "el dolor de una herida", "F-4-ALCANCE": "el miedo a la bestia",
          "S-8-EXPOSICION": "sentirse expuesta", "R-CARENCIA": "tener poca comida guardada", "R-ACOPIO": "las ganas de juntar más comida", "S-DANO-PAREJA": "lo mal que veía a su hermana",
          "R-HERMANO-FALTA": "lo que le faltaba a su hermana", "S-SOLEDAD": "la soledad", "S-COMPANIA": "echar de menos a su hermana", "R-CURIOSIDAD-FRONTERA": "la curiosidad por lo que no conocía",
          "F-HERMANO-AMENAZA": "el miedo por su hermana", "S-DUELO-CUERPO": "el duelo", "S-DUELO-RECURSOS": "el duelo", "S-DUELO-VINCULO": "el duelo", "S-MUERTE-PAREJA": "la muerte de su hermana",
          "S-QUITAR": "lo que quitaba a otra", "S-DANAR": "el daño que hacía a otra", "P-RADAR-CUERPO": "lo que podía perder de las suyas"}
GANA = {"G-F-HAMBRE": "quitarse el hambre", "G-R-CARENCIA": "tener comida guardada", "S-DAR": "lo que alivia dar", "G-GESTO": "el gesto de dar", "G-ALIVIO": "el alivio de otra",
        "G-SABOR-OTRA": "el gusto de otra", "P-COMER": "el gusto de comer", "R-CONSEGUIR": "conseguir comida", "S-JUNTAS": "estar juntas"}
LLAMA = {"aqui_estoy": "«aquí estoy»", "aqui_hay_comida": "«aquí hay comida»", "la_bestia": "«¡la bestia!»", "ven_lo_necesito": "«ven, lo necesito»"}
SONIDO = {"alegria": "alegría", "enfado": "enfado", "placer": "placer", "dolor": "dolor", "amor": "cariño", "tristeza": "tristeza"}
ORIGEN = {"huerto": "del huerto", "bosque": "del bosque", "dulce": "fruta dulce", "bestia": "que soltó la bestia", None: "sin saber de dónde"}

def rato(p):
    return "casi siempre" if p > 0.75 else ("la mitad del tiempo" if p > 1 / 3 else ("a ratos" if p > 0.1 else ("un momento" if p > 0 else "nunca")))
def hambre(h): return "harta" if h < 0 else ("con poca hambre" if h < 30 else ("con algo de hambre" if h <= FLACA else "con mucha hambre"))
def cansancio(c): return "descansada" if c < 40 else ("cansada" if c <= 70 else "muy cansada")
def vida(v): return "con la vida entera" if v >= VIDA else ("algo herida" if v >= HERIDA else "herida")
def quien(a, b): return "su hermana" if b == her(a) else f"la vecina {b}"
def lista(xs):
    xs = [x for x in xs if x]
    return "" if not xs else (xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1])

def lee(d, dia):
    t0, t1 = dia * DIA, (dia + 1) * DIA; R = {}
    for nom in ("mundo", "criaturas", "balance", "diario"):
        f = os.path.join(d, f"{nom}.jsonl.gz"); R[nom] = {}
        if not os.path.exists(f): continue
        for l in gzip.open(f, "rt", encoding="utf-8"):
            x = json.loads(l); t = x.get("turno", x.get("t"))
            if t0 - 1 <= t < t1: R[nom][t] = x
    R["arbol"] = json.load(open(os.path.join(d, "arbol.json"))) if os.path.exists(os.path.join(d, "arbol.json")) else {}
    return R

def tramo(a, R, nom, ta, tb):
    M, C, B, Dz = R["mundo"], R["criaturas"], R["balance"], R["diario"]; ts = [t for t in range(ta, tb) if t in M and a in M[t]["agentes"] and not M[t]["agentes"][a]["cuerpo"]["muerta"]]
    if not ts: return None
    g0, g1 = M[ts[0]]["agentes"][a], M[ts[-1]]["agentes"][a]; n = len(ts); w = [f"**{nom[0].upper() + nom[1:]}.**"]
    # dónde: los sitios en orden, sin los ratos de menos de 3 turnos
    seq = []
    for t in ts:
        s_ = (B.get(t) or {}).get("c", {}).get(a); s_ = SITIO.get(s_[5], s_[5]) if s_ else None
        if s_ is None: continue
        if seq and seq[-1][0] == s_: seq[-1][1] += 1
        else: seq.append([s_, 1])
    seq = [z for z in seq if z[1] >= 3]; com = []
    for z in seq:
        if not com or com[-1] != z[0]: com.append(z[0])
    arboles = [tuple(x[:2]) for x in (M[ts[0]].get("arboles") or []) if x[2] is not None] if M[ts[0]].get("arboles") else []
    cerca_arbol = sum(1 for t in ts if any(cheb(tuple(M[t]["agentes"][a]["pos"]), q) <= 2 for q in arboles))
    if com: w.append(f"Estuvo {com[0]}" + (", luego " + lista(com[1:5]) if len(com) > 1 else "") + (" (y más sitios)" if len(com) > 5 else "") + "." + (f" Estuvo junto a un árbol dulce {rato(cerca_arbol / n)}." if cerca_arbol else ""))
    # con quién: pegada (a una casilla o menos), y a la vista
    peg = Counter(); vis = Counter(); hh = her(a)
    for t in ts:
        p = tuple(M[t]["agentes"][a]["pos"])
        for b, gb in M[t]["agentes"].items():
            if b != a and not gb["cuerpo"]["muerta"] and cheb(p, tuple(gb["pos"])) <= 1: peg[b] += 1
        for b in ((Dz.get(t) or {}).get("c", {}).get(a) or {}).get("ve") or []: vis[b] += 1
    vivah = hh in M[ts[-1]]["agentes"] and not M[ts[-1]]["agentes"][hh]["cuerpo"]["muerta"]
    con = [(f"pegada a su hermana {rato(peg[hh] / n)}" if peg[hh] else "nunca pegada a su hermana") if vivah else "sin su hermana, que ya no vive"]
    vec = sorted(((b, x) for b, x in peg.items() if b != hh), key=lambda z: -z[1])
    if vec: con.append("con vecinas al lado " + rato(max(x for _, x in vec) / n) + f" ({lista([quien(a, b) for b, _ in vec[:3]])})")
    else: con.append("sin ninguna vecina al lado")
    if vivah and vis[hh]: con.append(f"veía a su hermana {rato(vis[hh] / n)}")
    w.append(("Estuvo " + lista(con) + ".").replace("Estuvo nunca pegada", "No estuvo pegada"))
    # qué hizo, y para qué iba
    A = Counter(); va = Counter(); hizo = []; llamo = Counter()
    for t in ts:
        g = M[t]["agentes"][a]; k = g.get("accion"); ok = g.get("resultado") == "ok"
        z = (Dz.get(t) or {}).get("c", {}).get(a) or {}; q = (z.get("acc") or {}).get("_ir") or (z.get("dest") or {}).get("que")
        if q and k in ("mover", "quedarse"): va[q] += 1
        if k == "comer" and ok: A[f"comió {ORIGEN.get(g.get('origen'), 'algo')}"] += 1
        elif k == "coger" and ok: A["cogió " + {"comida": "comida", "medicina": "medicina"}.get(g.get("tipo"), "algo") + {"almacen": " del almacén", "despensa": " de la despensa", "suelo": " del suelo", "planta": " de una planta", "matorral": " de un matorral", "arbol": " del árbol dulce"}.get(g.get("de"), "")] += 1
        elif k == "dejar" and ok: A["dejó " + (g.get("tipo") or "algo") + {"despensa": " en la despensa de su casa", "almacen": " en el almacén", "suelo": " en el suelo"}.get(g.get("en"), "")] += 1
        elif k == "dar" and ok and g.get("objetivo"): A[f"dio {g.get('tipo') or 'comida'} a {quien(a, g['objetivo'])}"] += 1
        elif k == "trabajar" and ok: A["trabajó el huerto"] += 1
        elif k == "dormir": A["durmió"] += 1
        elif k == "empujar" and g.get("objetivo"):
            gana = str(g.get("resultado") or "").startswith("gana " + a); sol = g.get("soltado") or []
            pb_ = ((M.get(t - 1) or {}).get("agentes", {}).get(a) or {}).get("bolsa") or []; sube = max(0, (g.get("bolsa") or []).count("comida") - pb_.count("comida"))
            hizo.append(f"empujó a {quien(a, g['objetivo'])}" + ((" y ganó" + (f": le quitó {sube} {'comida' if sube == 1 else 'comidas'}" if sube else "") + (f" y {len(sol) - sube} cayeron al suelo" if len(sol) > sube else "")) if gana else " y perdió"))
        ll = ((C.get(t) or {}).get("criaturas", {}).get(a) or {}).get("llama")
        if ll and k != "dormir": llamo[LLAMA.get(ll.get("llamada"), ll.get("llamada"))] += 1
        for b, gb in M[t]["agentes"].items():                                   # lo que le dan
            if b != a and gb.get("accion") == "dar" and gb.get("resultado") == "ok" and gb.get("objetivo") == a: A[f"recibió {gb.get('tipo') or 'comida'} de {quien(a, b)}"] += 1
        # la comida que baja de la bolsa sin comerla, darla, dejarla ni que se la quiten: se le pudrió (el mundo la pudre al acabar el día, mundo.py:1039-1053, sin suceso)
        pb = ((M.get(t - 1) or {}).get("agentes", {}).get(a) or {}).get("bolsa")
        if pb is not None:
            baja = pb.count("comida") - (g.get("bolsa") or []).count("comida")
            quitan = any((e.get("bestia_roba") == a) or ("empujon" in e and a in (e["empujon"], e.get("a")) and e.get("gana") != a and e.get("soltado")) for e in M[t].get("eventos") or [])
            if baja > 0 and not (ok and k in ("comer", "dar", "dejar")) and not quitan: A["se le pudrió comida en la bolsa"] += baja
    txt = [f"{k}" + (f" ({x} veces)" if x > 1 and k != "durmió" else "") for k, x in A.most_common() if k != "durmió"]
    if A["durmió"]: txt.insert(0, "durmió " + rato(A["durmió"] / n))
    w.append(("Hizo esto: " + lista(txt + hizo[:4]) + ("; y empujó más veces" if len(hizo) > 4 else "") + ".") if (txt or hizo) else "No hizo nada más que estar.")
    if va: w.append("Cuando andaba, iba sobre todo " + lista([VA.get(q, q) for q, _ in va.most_common(3)]) + ".")
    if llamo: w.append("Llamó " + lista([f"{k}" + (f" {x} veces" if x > 1 else "") for k, x in llamo.most_common(3)]) + ".")
    # qué le pasó
    pas = []; oye = Counter(); bestia_vista = 0
    for t in ts:
        for e in M[t].get("eventos") or []:
            if e.get("bestia_pega") == a: pas.append("la bestia le pegó")
            if e.get("bestia_roba") == a: pas.append("la bestia le robó " + lista(e.get("que") or ["algo"]))
            if e.get("despierta") == a: pas.append("la despertaron (" + {"empujon": "un empujón", "golpe": "un golpe", "bestia al lado": "la bestia al lado"}.get(e.get("por"), str(e.get("por")).replace("llamada ", "una llamada: ").replace("voz ", "una voz: ")) + ")")
            if "empujon" in e and e.get("a") == a: pas.append(f"la empujó {quien(a, e['empujon'])}" + (" y le quitó comida" if e.get("gana") == e["empujon"] and e.get("soltado") else (" pero no pudo con ella" if e.get("gana") == a else "")))
            if "muere" in e: pas.append(("murió su hermana" if e["muere"] == her(a) else f"murió {quien(a, e['muere'])}") + f" ({e.get('causa')})")
            if "bestia_echada" in e and cheb(tuple(M[t]["agentes"][a]["pos"]), tuple(e.get("desde") or (0, 0))) <= 2: pas.append("echaron a la bestia a su lado")
        z = (Dz.get(t) or {}).get("c", {}).get(a) or {}
        bestia_vista += bool(z.get("bestia"))
        for o in z.get("oye") or []:
            q = o[1] or ""; s_ = "su hermana" if o[0] == her(a) else "una vecina"
            oye[(f"a {s_} llamar " + LLAMA.get(q, q)) if not q.startswith("sonido:") else f"a {s_} sonar a {SONIDO.get(q[7:], q[7:])}"] += 1
    pc = Counter(pas)
    if pc: w.append("Le pasó: " + lista([k + (f" ({x} veces)" if x > 1 else "") for k, x in pc.most_common(6)]) + ".")
    if bestia_vista: w.append(f"Vio la bestia {rato(bestia_vista / n)}.")
    if oye: w.append("Oyó " + lista([k + (f" ({x} veces)" if x > 2 else "") for k, x in oye.most_common(4)]) + ".")
    # cómo estaba: cuerpo, recursos, vínculo
    c0, c1 = g0["cuerpo"], g1["cuerpo"]
    cu = f"Empezó {hambre(c0['hambre'])}, {cansancio(c0['cansancio'])} y {vida(c0['vida'])}"
    cu += (f"; acabó {hambre(c1['hambre'])}, {cansancio(c1['cansancio'])} y {vida(c1['vida'])}." if (hambre(c0['hambre']), cansancio(c0['cansancio']), vida(c0['vida'])) != (hambre(c1['hambre']), cansancio(c1['cansancio']), vida(c1['vida'])) else ", y así siguió.")
    w.append(cu)
    gp = ((M.get(ts[0] - 1) or {}).get("agentes", {}).get(a)) or g0; b0, b1 = (gp.get("bolsa") or []), (g1.get("bolsa") or [])      # (la bolsa al empezar el tramo: la del turno de antes)
    w.append(f"Llevaba {b0.count('comida')} {'comida' if b0.count('comida') == 1 else 'comidas'}" + (" y una medicina" if "medicina" in b0 else "") + f"; al acabar el tramo, {b1.count('comida')}" + (" y una medicina" if "medicina" in b1 else "") + ".")
    bal = [B[t]["c"][a] for t in ts if t in B and a in B[t]["c"] and not B[t]["c"][a][6]]
    if bal:
        dims = [("en el cuerpo", 0), ("en lo que tiene", 1), ("con las suyas", 2)]
        w.append("Despierta, se sintió " + lista([f"bien {d} {rato(sum(1 for z in bal if z[i] > 0) / len(bal))}" for d, i in dims]) + ".")
    P = Counter(); G = Counter()
    for t in ts:
        z = (Dz.get(t) or {}).get("c", {}).get(a) or {}
        if z.get("pierde"): P[PIERDE.get(z["pierde"][0][0], z["pierde"][0][0])] += 1
        for k, _ in (z.get("pierde") or [])[1:3]: P[PIERDE.get(k, k)] += 0.25
        if z.get("gana"): G[GANA.get(z["gana"][0][0], z["gana"][0][0])] += 1
    if P: w.append("Lo que más le pesaba: " + lista([k for k, _ in P.most_common(3)]) + ".")
    if G: w.append("Lo que más le tiraba: " + lista([k for k, _ in G.most_common(2)]) + ".")
    return "\n".join(w)

def diario(d, a, dia):
    R = lee(d, dia); M = R["mundo"]
    w = [f"# El día {dia} de {a} (casa {a[0]}; su hermana es {her(a)}; a las vecinas se las llama por su casa: B1 y B2 son de la casa B)\n"]
    for nom, ta, tb in TRAMOS:
        x = tramo(a, R, nom, dia * DIA + ta, dia * DIA + tb)
        if x: w.append(x + "\n")
    # las cuentas
    fases = ", ".join(f"{f} {n}" for f, n in CFG["dia"]["fases"])
    sit = [tuple(z[0]) for z in (R["arbol"].get("sitios") or [])]; Dd = MAPA.distancias([MAPA.puerta[a[0]]]); ida = None
    for c in sit:
        dd = [Dd[p] for p in ((c[0] + dx, c[1] + dy) for dx, dy in DIRS.values()) if p in Dd]
        if dd and (ida is None or min(dd) < ida): ida = min(dd)
    tl = max((t for t in R["criaturas"] if t < (dia + 1) * DIA), default=None); de = ((R["criaturas"].get(tl) or {}).get("despensas") or {}).get(a[0], {}) if tl is not None else {}
    al = ((R["criaturas"].get(tl) or {}).get("almacen") or {}) if tl is not None else {}
    w.append("**Cuentas.**")
    w.append(f"- El día tiene {DIA} turnos ({fases}).")
    w.append(f"- Ir al árbol dulce y volver desde su casa: {2 * ida} turnos (el más cercano de los dos; desde la puerta)." if ida is not None else "- Ir al árbol dulce y volver desde su casa: no se sabe (no hay árboles en esta partida).")
    w.append(f"- Comida guardada al acabar el día: {de.get('comida', 0)} en la despensa de su casa y {al.get('comida', 0)} en el almacén (de todas).")
    return "\n".join(w) + "\n"


if __name__ == "__main__":
    d, a, dia = sys.argv[1], sys.argv[2], int(sys.argv[3]); txt = diario(d, a, dia)
    if len(sys.argv) > 4: open(sys.argv[4], "w").write(txt)
    print(txt)

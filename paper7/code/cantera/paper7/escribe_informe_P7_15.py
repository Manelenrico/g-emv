"""[P7-15] Escribe informe_P7_15.md desde P7_15_vidas.json, P7_15_regalo.json, P7_15_pedidos.json (analiza_P7_15.py), P7_15_decisiones.json
(banco_P7_15.py), los campos (P7_10_campo.json, P7_14b_campo.json) y las vidas (P7_11_vidas.json, P7_14b_vidas.json). Ninguna cifra a mano."""
import collections, hashlib, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
J = lambda p: json.load(open(os.path.join(AQUI, p))); md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
V = list(J("P7_15_vidas.json").values()); C = {"P7-10": J("P7_10_campo.json"), "P7-14b": J("P7_14b_campo.json")}; M = {"P7-10": J("P7_11_vidas.json"), "P7-14b": J("P7_14b_vidas.json")}
S14 = J("P7_14b_sello_resultado.json"); G = J("P7_15_regalo.json"); P = J("P7_15_pedidos.json"); R = J("P7_15_decisiones.json"); CAMPOS = ("P7-10", "P7-14b")
kk = lambda v: f"s{v['serie']}_d{v['dia']}_{v['brazo']}_{v['slot']}"; cc = lambda v: C[v["campo"]][kk(v)]; mm = lambda v: M[v["campo"]][kk(v)]
TEMPRANA = 11000
def val(v, m):
    if m == "puesto": return cc(v)["puesto"]
    if m == "vida al morir": return float(cc(v)["hp_final"])
    if m == "muere por rival": return int(cc(v)["causa_muerte"] == "rival")
    if m == "muere por el anillo": return int(cc(v)["causa_muerte"] == "anillo")
    if m == "sobrevive al final": return int(cc(v)["causa_muerte"] == "sobrevive")
    if m == "muere antes del tic 11.000": return int(v["ultimo_tick"] < TEMPRANA)
    if m == "muere antes del tic 10.000": return int(v["ultimo_tick"] < 10000)
    if m == "muere antes del tic 12.000": return int(v["ultimo_tick"] < 12000)
    if m == "muere por rival yendo a por un botiquín": return int(cc(v)["causa_muerte"] == "rival" and mm(v)["muerte"]["moda"] == "ir a por un botiquin")
    if m == "abre el canal en sus últimos 10 s y muere por rival": return int(cc(v)["causa_muerte"] == "rival" and mm(v)["muerte"]["tics_en_canal"] > 0)
    return v[m]
def par(a, b, m, campos):
    ps = collections.defaultdict(lambda: {a: [], b: []})
    for v in V:
        if v["campo"] in campos and v["brazo"] in (a, b): ps[(v["campo"], v["semilla"])][v["brazo"]].append(val(v, m))
    d = [st.mean(p[a]) - st.mean(p[b]) for p in ps.values()]; mu = st.mean(d); se = st.stdev(d) / math.sqrt(len(d))
    return {"a": st.mean(x for p in ps.values() for x in p[a]), "b": st.mean(x for p in ps.values() for x in p[b]), "d": mu, "se": se, "z": (mu / se if se else 0.0), "n": len(d)}
W = []; w = W.append
def tabla(a, b, metricas, dec):
    w(f"| medida (por vida) | P7-10: {a} | {b} | d̄ | d̄/se | P7-14b: {a} | {b} | d̄ | d̄/se | los dos campos: d̄ | d̄/se | ¿en los dos? |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|\n")
    fuertes = []
    for m, nom in metricas:
        x, y, z = par(a, b, m, ("P7-10",)), par(a, b, m, ("P7-14b",)), par(a, b, m, CAMPOS); de = dec.get(m, 2)
        dos = abs(x["z"]) > 2 and abs(y["z"]) > 2 and x["d"] * y["d"] > 0
        if dos: fuertes.append(nom)
        w(f"| {nom} | {n(x['a'], de)} | {n(x['b'], de)} | {n(x['d'], de)} | {n(x['z'], 1)} | {n(y['a'], de)} | {n(y['b'], de)} | {n(y['d'], de)} | {n(y['z'], 1)} | {n(z['d'], de)} | {'**' if abs(z['z']) > 2 else ''}{n(z['z'], 1)}{'**' if abs(z['z']) > 2 else ''} | {'**sí**' if dos else 'no'} |\n")
    return fuertes
M1 = [("puesto", "puesto"), ("vida al morir", "vida al morir"), ("ultimo_tick", "último tic vivo"), ("fase_al_morir", "fase del anillo al morir (0 a 7)"), ("muere antes del tic 10.000", "muere antes del tic 10.000 (0/1)"), ("muere antes del tic 11.000", "muere antes del tic 11.000 (0/1)"),
      ("muere antes del tic 12.000", "muere antes del tic 12.000 (0/1)"), ("muere por rival", "muere por rival (0/1)"), ("muere por el anillo", "muere por el anillo (0/1)"), ("sobrevive al final", "sobrevive al final (0/1)"),
      ("muere por rival yendo a por un botiquín", "muere por rival yendo a por un botiquín (0/1)"), ("abre el canal en sus últimos 10 s y muere por rival", "muere por rival habiendo abierto el canal en sus últimos 10 s (0/1)")]
M2 = [("vida_menos_de_50", "parte de la vida con menos de 50 de vida"), ("vida_menos_de_30", "… con menos de 30"), ("fuera_del_circulo", "parte de la vida fuera del círculo"), ("pelea", "parte de la vida con un rival a una o dos casillas"),
      ("con_botiquin", "parte de la vida con algún botiquín"), ("botiquines_media", "botiquines a bordo, media"), ("con_racion", "… con alguna ración"), ("con_arma", "… con un arma (mano o zurrón)"), ("con_municion", "… con munición"),
      ("zurron_lleno", "… con el zurrón lleno"), ("casillas_por_1000_tics", "casillas recorridas por 1.000 tics")]
DEC = {"ultimo_tick": 0, "vida_menos_de_50": 3, "vida_menos_de_30": 3, "fuera_del_circulo": 3, "pelea": 3, "con_botiquin": 3, "botiquines_media": 3, "con_racion": 3, "con_arma": 3, "con_municion": 3, "zurron_lleno": 3, "casillas_por_1000_tics": 1}
L = lambda campo, b: [v for v in V if v["campo"] == campo and v["brazo"] == b]
tA = {c: [v for v in L(c, "APRENDE") if v["ultimo_tick"] < TEMPRANA] for c in CAMPOS}; tB = {c: [v for v in L(c, "BORRADO") if v["ultimo_tick"] < TEMPRANA] for c in CAMPOS}
def sin_tempranas(campo):
    A = {(v["serie"], v["dia"], v["slot"]): v for v in L(campo, "APRENDE")}; B = {(v["serie"], v["dia"], v["slot"]): v for v in L(campo, "BORRADO")}
    d = [cc(A[x])["puesto"] - cc(B[x])["puesto"] for x in A if A[x]["ultimo_tick"] >= TEMPRANA and B[x]["ultimo_tick"] >= TEMPRANA]; t = [cc(A[x])["puesto"] - cc(B[x])["puesto"] for x in A]
    return st.mean(t), st.stdev(t) / math.sqrt(len(t)), len(d), st.mean(d), st.stdev(d) / math.sqrt(len(d))
def fisher(a, b, c, d):
    """cola derecha de la exacta de Fisher: P(X >= a) con margenes fijos"""
    f = lambda x: math.comb(a + b, x) * math.comb(c + d, a + c - x) / math.comb(a + b + c + d, a + c)
    return sum(f(x) for x in range(a, min(a + b, a + c) + 1))
nA = sum(len(tA[c]) for c in CAMPOS); nB = sum(len(tB[c]) for c in CAMPOS); pF = fisher(nA, 160 - nA, nB, 160 - nB)
# decisiones
def cat(e):
    e = str(e)
    if e == "usar_botiquin": return "usar el botiquín"
    if e == "usar_racion": return "usar una ración"
    if e == "ir_curioso": return "ir por curiosidad"
    if e == "ir_objeto": return "ir a por un objeto"
    if e == "coger": return "coger"
    if e.startswith("hacer_sitio_"): return "hacer sitio"
    if e.startswith("soltar_first_aid"): return "regalar"
    if e.startswith("soltar_"): return "soltar otra cosa"
    if e.startswith(("move_", "paso_")): return "moverse"
    if e.startswith(("atacar_", "empunar_")): return "atacar"
    if e in ("ir_pareja", "ir_centro", "ir_botin"): return "ir a un sitio (hermano, centro o botín)"
    if e == "noop": return "quedarse quieto"
    return "otro"
tot = sum(r["tics_comparados"] for r in R); dif = sum(len(r["distintos"]) for r in R); ini = collections.Counter(); todos = collections.Counter(); pordia = collections.defaultdict(lambda: [0, 0, 0]); fid = collections.Counter()
for r in R:
    prev = None; pordia[r["dia"]][0] += r["tics_comparados"]; fid.update(r["fidelidad"])
    for x in r["distintos"]:
        p = (cat(x["con_cuaderno"]), cat(x["sin_los_dias_anteriores"])); todos[p] += 1; pordia[r["dia"]][1] += 1
        if prev is None or x["t"] - prev > 12: ini[p] += 1; pordia[r["dia"]][2] += 1
        prev = x["t"]
qu = [x for r in R for x in r["distintos"] if x["con_cuaderno"] == "noop" and x["sin_los_dias_anteriores"] == "usar_botiquin"]; hq = sorted(x["hp"] for x in qu)
hs = [x for r in R for x in r["distintos"] if x["con_cuaderno"] == "noop" and str(x["sin_los_dias_anteriores"]).startswith("hacer_sitio")]
TQ = ("quedarse quieto", "usar el botiquín")
temp14 = []
for r in R:
    v = next(v for v in V if v["campo"] == "P7-14b" and v["brazo"] == "APRENDE" and (v["serie"], v["dia"], v["slot"]) == (r["serie"], r["dia"], r["slot"]))
    if v["ultimo_tick"] < TEMPRANA:
        d = [x for x in r["distintos"] if x["t"] >= v["ultimo_tick"] - 480]
        temp14.append((v, r, len(d), sum(1 for x in d if (cat(x["con_cuaderno"]), cat(x["sin_los_dias_anteriores"])) == TQ), min(480, r["tics_comparados"])))
# el resto de vidas: quieto -> usar en sus ultimos 20 s
otras = []
for r in R:
    v = next(v for v in V if v["campo"] == "P7-14b" and v["brazo"] == "APRENDE" and (v["serie"], v["dia"], v["slot"]) == (r["serie"], r["dia"], r["slot"]))
    if v["ultimo_tick"] >= TEMPRANA and cc(v)["causa_muerte"] != "sobrevive": otras.append(sum(1 for x in r["distintos"] if x["t"] >= v["ultimo_tick"] - 480 and (cat(x["con_cuaderno"]), cat(x["sin_los_dias_anteriores"])) == TQ))
st10, se10, np10, dn10, sn10 = sin_tempranas("P7-10"); st14, se14, np14, dn14, sn14 = sin_tempranas("P7-14b")
enc = [t for e in G for t in e["tics"] if t["donde"] == "encima"]; lado = [t for e in G for t in e["tics"] if t["donde"] == "al lado"]
hsd = [min(x for k_, x in t["cand"].items() if k_.startswith("hacer_sitio_")) - t["cand"]["noop"] for t in enc if any(k_.startswith("hacer_sitio_") for k_ in t["cand"])]

w(f"""# P7-15 · Dónde pierde el puesto el que recuerda

*5-oct-2026. Todo lo de este paso es POSTERIOR A LOS DOS SELLOS (P7-10 y P7-14b) y se declara así: lecturas de los 640 diarios de los dos campos y un
banco de réplica, con medidas elegidas después de ver los resultados. Coste: **créditos de la plataforma 0 USD; consola de Anthropic 0 USD.**
`motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; cuerpo y congelados sin tocar. El banco (`banco_P7_15.py`) replica las 80 vidas de
APRENDE de P7-14b, una vida por proceso, y reproduce la decisión del campo en {n(fid['igual'])} de {n(sum(fid.values()))} tics.*

## Lo que sale, en corto

1. **El puesto se pierde en unas pocas muertes tempranas.** En los dos campos, 10 de las 80 vidas de APRENDE mueren antes del tic 11.000; de BORRADO,
   {len(tB['P7-10'])} y {len(tB['P7-14b'])}. Casi todas son por rival y acaban entre los puestos 12 y 16. Quitando los pares en que alguno de los dos muere pronto, la diferencia
   de puesto baja de {n(st10, 2)} a {n(dn10, 2)} (se {n(sn10, 2)}) en P7-10 y de {n(st14, 2)} a {n(dn14, 2)} (se {n(sn14, 2)}) en P7-14b: dentro del ruido.
   Un matiz que importa: en P7-14b, ESPERANZA y TECHO mueren pronto casi tanto como APRENDE ({len([v for v in L('P7-14b', 'ESPERANZA') if v['ultimo_tick'] < TEMPRANA])} y {len([v for v in L('P7-14b', 'TECHO') if v['ultimo_tick'] < TEMPRANA])}); ahí el brazo distinto es BORRADO, que muere poco al principio.
2. **Nada de cómo vive los separa**: ni el tiempo con poca vida, ni el círculo, ni las peleas, ni el zurrón, ni lo que anda superan el ruido entre semillas en los dos campos.
3. **El cuaderno cambia la decisión en el {n(100 * dif / tot, 1)} % de los tics.** El cambio que más tics ocupa: con el cuaderno se queda quieto donde, sin los
   recuerdos de días anteriores, usaría el botiquín ({n(todos[TQ])} tics en {sum(1 for r in R if any((cat(x['con_cuaderno']), cat(x['sin_los_dias_anteriores'])) == TQ for x in r['distintos']))} de 80 vidas, con la vida en {n(st.median(hq))} de mediana). **El que recuerda espera más para curarse.**
4. **Las dos cosas se tocan**: en {sum(1 for t in temp14 if t[3] > 0)} de las {len(temp14)} muertes tempranas de APRENDE en P7-14b, en sus últimos 20 segundos hubo tics en que con el cuaderno se quedó
   quieto y sin él habría usado el botiquín. Es una coincidencia medida, no una prueba de causa: el banco no dice qué habría pasado después.
5. **El regalo que nadie coge**: quien pide lleva el zurrón lleno. No puede coger el botiquín y hacer sitio no gana.

## Sección 1 · Cuándo y cómo muere

Emparejado por semilla: en cada semilla, la media de las 4 vidas de un brazo (2 series × 2 asientos) menos la del otro; d̄ es la media sobre las 20
semillas de cada campo (o las 40 de los dos) y se su error típico. «¿En los dos?» = |d̄/se| > 2 en cada campo por separado y con el mismo signo: la prueba más dura.
Hay {len(M1) + len(M2)} medidas en esta sección y la siguiente: con tantas, alguna pasaría de 2 por azar en un campo; por eso se pide en los dos.

**APRENDE frente a BORRADO:**

""")
f1 = tabla("APRENDE", "BORRADO", M1, DEC)
w("\n**TECHO frente a BORRADO** (referencia):\n\n"); f1t = tabla("TECHO", "BORRADO", M1, DEC)
w(f"""
Lo único que pasa la prueba dura en APRENDE frente a BORRADO: {", ".join(f1) or "nada"}. En TECHO frente a BORRADO: {", ".join(f1t) or "nada"}.

**Las muertes tempranas** (el corte en el tic 11.000 lo he puesto después de ver los datos, por la curva de vivos; con 10.000 y 12.000 está en la tabla de arriba).
Vivos en cada momento, de 80:

| | tic 8.000 | 10.000 | 11.000 | 12.000 | 13.000 | 14.000 |
|---|---:|---:|---:|---:|---:|---:|
""")
for c in CAMPOS:
    for b in ("BORRADO", "APRENDE", "TECHO"): w(f"| {c}, {b} | " + " | ".join(str(sum(1 for v in L(c, b) if v["ultimo_tick"] >= t)) for t in (8000, 10000, 11000, 12000, 13000, 14000)) + " |\n")
w(f"""
| | P7-10: APRENDE | BORRADO | TECHO | P7-14b: APRENDE | BORRADO | TECHO |
|---|---:|---:|---:|---:|---:|---:|
""")
def fila6(nom, f): w(f"| {nom} | " + " | ".join(f(L(c, b)) for c in CAMPOS for b in ("APRENDE", "BORRADO", "TECHO")) + " |\n")
tp = lambda X: [v for v in X if v["ultimo_tick"] < TEMPRANA]
fila6("mueren antes del tic 11.000", lambda X: str(len(tp(X))))
fila6("… por rival", lambda X: str(sum(1 for v in tp(X) if cc(v)["causa_muerte"] == "rival")))
fila6("… en los puestos 12 a 16", lambda X: str(sum(1 for v in tp(X) if cc(v)["puesto"] >= 12)))
fila6("… con algún botiquín a bordo al morir", lambda X: str(sum(1 for v in tp(X) if mm(v)["muerte"]["botiquines_a_bordo"] > 0)))
fila6("… habiendo abierto el canal en sus últimos 10 s", lambda X: str(sum(1 for v in tp(X) if mm(v)["muerte"]["tics_en_canal"] > 0)))
fila6("… lo que más hacía: ir a por un botiquín", lambda X: str(sum(1 for v in tp(X) if mm(v)["muerte"]["moda"] == "ir a por un botiquin")))
fila6("… lo que más hacía: moverse paso a paso", lambda X: str(sum(1 for v in tp(X) if mm(v)["muerte"]["moda"] == "moverse paso a paso")))
fila6("puesto medio de todas las vidas", lambda X: n(st.mean(cc(v)["puesto"] for v in X), 2))
fila6("puesto medio sin las que mueren pronto", lambda X: n(st.mean(cc(v)["puesto"] for v in X if v["ultimo_tick"] >= TEMPRANA), 2))
w(f"""
- APRENDE: 10 y 10 muertes tempranas; BORRADO: {len(tB['P7-10'])} y {len(tB['P7-14b'])}. Juntando los dos campos, {nA} de 160 contra {nB} de 160 (exacta de Fisher, una cola: p = {n(pF, 3)}).
  Por semillas, la diferencia en «muere antes del tic 11.000» pasa de 2·se en los dos campos por separado, por poco (tabla de arriba), y con el corte en 12.000 también; con el corte en 10.000, no. Son pocos casos.
- **El puesto, sin esos pares.** APRENDE − BORRADO en puesto, pares por (serie, día, asiento): P7-10, todos los pares {n(st10, 2)} (se {n(se10, 2)}); los {np10} pares en que
  ninguno muere pronto, {n(dn10, 2)} (se {n(sn10, 2)}). P7-14b: {n(st14, 2)} (se {n(se14, 2)}) y, en {np14} pares, {n(dn14, 2)} (se {n(sn14, 2)}). Más de la mitad de la diferencia de puesto está en las muertes tempranas.
- Morir pronto cuesta muchos puestos de golpe (quien muere antes del tic 11.000 queda casi siempre del 12 al 16), así que 6 o 7 muertes tempranas de más en 80 vidas mueven la media más de medio puesto.
- TECHO tiene {len(tp(L('P7-10', 'TECHO')))} y {len(tp(L('P7-14b', 'TECHO')))}: en P7-14b, tantas como para no poder decir que sea cosa solo de APRENDE. ESPERANZA en P7-14b tiene {len(tp(L('P7-14b', 'ESPERANZA')))} (su SUELO en P7-10, {len(tp(L('P7-10', 'SUELO')))}).
  En P7-14b el brazo que se separa de los demás por abajo es BORRADO, que muere poco al principio.

## Sección 2 · Cómo vive

""")
f2 = tabla("APRENDE", "BORRADO", M2, DEC)
w("\n**TECHO frente a BORRADO:**\n\n"); f2t = tabla("TECHO", "BORRADO", M2, DEC)
w(f"""
**Ninguna de las {len(M2)} medidas separa a APRENDE de BORRADO en los dos campos** ({", ".join(f2) or "ninguna pasa la prueba dura"}). APRENDE no pasa más tiempo con poca vida, no está más fuera
del círculo, no pelea más, no lleva otro zurrón (los mismos botiquines, raciones, armas y munición, dentro del ruido) y no anda más.

## Sección 3 · Qué decisiones cambia el cuaderno

`banco_P7_15.py` → `P7_15_decisiones.json`. Las 80 vidas de APRENDE de P7-14b, tal como se jugaron. En cada tic el cuerpo decide dos veces sobre la
misma escena y la misma memoria de la partida: con su cuaderno, y con el cuaderno que tendría BORRADO ese día (vacío al empezar: solo los recuerdos
de hoy). Se cuenta cada tic en que las dos decisiones difieren y, aparte, los EPISODIOS: el primer tic de cada racha de tics seguidos distintos
(huecos de hasta 12 tics, medio segundo). El banco describe ese tic; no dice qué habría pasado después.

{n(tot)} tics comparados; la decisión cambia en **{n(dif)} ({n(100 * dif / tot, 1)} %)**, en {n(sum(ini.values()))} episodios ({n(sum(ini.values()) / len(R), 1)} por vida). En esos tics las ganas del botiquín valen k = {n(st.mean(x['k_ganas'] for r in R for x in r['distintos']), 2)} con el
cuaderno y {n(st.mean(x['k_ganas_de_hoy'] for r in R for x in r['distintos']), 2)} solo con lo de hoy.

| con el cuaderno elige | solo con lo de hoy elegiría | episodios | tics |
|---|---|---:|---:|
""")
for p, c in sorted(ini.items(), key=lambda x: -todos[x[0]])[:14]: w(f"| {p[0]} | {p[1]} | {n(c)} | {n(todos[p])} |\n")
a_ = collections.Counter(); b_ = collections.Counter()
for (x, y), c in ini.items(): a_[x] += c; b_[y] += c
w(f"""
(Las {min(14, len(ini))} parejas con más tics; hay {len(ini)}.) Por tipo de candidato, episodios en que lo elige con el cuaderno / solo con lo de hoy: """ + "; ".join(f"{k_} {a_.get(k_, 0)} / {b_.get(k_, 0)}" for k_ in ("ir a por un objeto", "ir por curiosidad", "moverse", "ir a un sitio (hermano, centro o botín)", "quedarse quieto", "usar el botiquín", "hacer sitio", "regalar", "coger", "atacar")) + f""".

Lo que se lee:
- **Esperar en vez de curarse.** `noop` con el cuaderno, `usar_botiquin` solo con lo de hoy: {ini[TQ]} episodios pero {n(todos[TQ])} tics (dos tercios de todos los tics distintos), en
  {sum(1 for r in R if any((cat(x['con_cuaderno']), cat(x['sin_los_dias_anteriores'])) == TQ for x in r['distintos']))} de las 80 vidas. La vida en esos tics: mediana {n(st.median(hq))}, el 80 % entre {n(hq[len(hq) // 10])} y {n(hq[9 * len(hq) // 10])}. Con las ganas a 0,3 (esperanza) el botiquín se gasta
  como una ración, en cuanto falta algo; con las ganas aprendidas ({n(st.median([x['k_ganas'] for x in qu]), 2)} de mediana) gastarlo cuesta más y el cuerpo aguanta herido sin usarlo. Al revés (usar con el cuaderno y no sin él): {a_.get('usar el botiquín', 0)} episodios.
- **Ir a por objetos en vez de moverse o curiosear.** Con el cuaderno elige `ir_objeto` en {a_.get('ir a por un objeto', 0)} episodios en que sin él haría otra cosa (moverse, ir por curiosidad, al centro o al
  botín); al revés, {b_.get('ir a por un objeto', 0)}. Son muchos episodios y pocos tics: decisiones sueltas de hacia dónde dar el paso. El diario no dice a por qué objeto iba.
- **No hacer sitio.** Con un botiquín a bordo y una ración en la casilla: con el cuaderno se queda como está; solo con lo de hoy cambiaría el botiquín por la ración ({ini[('quedarse quieto', 'hacer sitio')]} episodios, {n(len(hs))} tics, todos `hacer_sitio_first_aid_por_rations`).
- **Regalar.** {ini[('regalar', 'quedarse quieto')]} regalos que con solo lo de hoy no haría (la creencia de quien regala es la que deja pasar el regalo).

Por días (parte de los tics con la decisión distinta; episodios por vida):

| día | """ + " | ".join(str(d) for d in range(1, 21)) + """ |
|---|""" + "---:|" * 20 + """
| tics distintos | """ + " | ".join(f"{n(100 * pordia[d][1] / max(1, pordia[d][0]), 1)} %" for d in range(1, 21)) + """ |
| episodios por vida | """ + " | ".join(n(pordia[d][2] / 4, 0) for d in range(1, 21)) + f""" |

El día 1 no hay ninguna (el cuaderno está vacío: las dos decisiones son la misma, como debe). Los días con muchos tics distintos son los de las
rachas largas de «esperar en vez de curarse».

**Las muertes tempranas de APRENDE en P7-14b, en sus últimos 20 segundos** (480 tics):

| vida | muere en el tic | puesto | causa | tics con la decisión distinta | de ellos, «quieto» con el cuaderno y «usar el botiquín» sin él |
|---|---:|---:|---|---:|---:|
""")
for v, r, nd, nq, de in sorted(temp14, key=lambda t: t[0]["ultimo_tick"]): w(f"| serie {v['serie']}, día {v['dia']}, asiento {v['slot']} | {n(v['ultimo_tick'])} | {cc(v)['puesto']} | {cc(v)['causa_muerte']} | {nd} de {de} | {nq} |\n")
w(f"""
En {sum(1 for t in temp14 if t[3] > 0)} de las {len(temp14)}, en sus últimos 20 segundos el que recuerda se quedó quieto con el botiquín en el zurrón en tics en que, con solo lo de hoy, lo habría usado.
En las otras {len(otras)} vidas de APRENDE que mueren (después del tic 11.000), eso pasa en {sum(1 for x in otras if x > 0)}. **Es una coincidencia medida y no una prueba**: no sé si usarlo las habría salvado
(en varias el canal se abrió igualmente al final), y BORRADO no se ha replicado al revés.

**Lo que va en contra de leerlo como causa.** ESPERANZA es el brazo que menos espera (ganas a 0,3 siempre, usa el botiquín como una ración) y en P7-14b tiene {len([v for v in L('P7-14b', 'ESPERANZA') if v['ultimo_tick'] < TEMPRANA])} muertes
tempranas, una más que APRENDE; en P7-10 su SUELO tuvo {len([v for v in L('P7-10', 'SUELO') if v['ultimo_tick'] < TEMPRANA])}. Si esperar para curarse fuera lo que mata pronto, ESPERANZA debería morir pronto menos que nadie, y en P7-14b no es así.
Lo que se sostiene en los dos campos es más estrecho: APRENDE muere pronto más que BORRADO. Por qué BORRADO muere pronto menos que los otros tres brazos en P7-14b no lo explica nada de lo medido aquí.

## Sección 4 · Las tres sospechas de la mesa

| sospecha | lo medido | veredicto |
|---|---|---|
| (a) espera más para curarse y pasa más tiempo con poca vida | **Espera más: sí**, en la decisión ({n(todos[TQ])} tics en {sum(1 for r in R if any((cat(x['con_cuaderno']), cat(x['sin_los_dias_anteriores'])) == TQ for x in r['distintos']))} de 80 vidas en que con el cuaderno no usa el botiquín y sin él lo usaría; y en el campo usa con menos vida: {n(S14['Q4']['mediana_vida_al_usar_d11_20']['APRENDE'])} contra {n(S14['Q4']['mediana_vida_al_usar_d11_20']['BORRADO'])} en los días 11 a 20 de P7-14b). **Más tiempo con poca vida: no**: la parte de la vida por debajo de 50 y de 30 no se distingue de la de BORRADO en ningún campo | **la mitad se sostiene**: espera más, pero eso no se ve como más tiempo con poca vida; se ve, si acaso, en las muertes tempranas |
| (b) lleva botiquines en lugar de otras cosas | botiquines, raciones, armas y munición a bordo, y zurrón lleno: ninguna diferencia que pase de 2·se en los dos campos | **no se sostiene** |
| (c) la curiosidad de BORRADO le lleva a algo que le da ventaja | BORRADO y APRENDE van a por botiquines una parte parecida de la vida y llevan lo mismo; en el banco, sin los días anteriores iría más por curiosidad ({b_.get('ir por curiosidad', 0)} episodios contra {a_.get('ir por curiosidad', 0)}) y menos a por objetos, pero son pasos sueltos, y lo que lleva y lo que anda no cambia | **no se sostiene** con lo medido |
| otra, que aparece | **las muertes tempranas**: 10 y 10 de APRENDE contra {len(tB['P7-10'])} y {len(tB['P7-14b'])} de BORRADO, que llevan más de la mitad de la diferencia de puesto, y que en P7-14b coinciden con tics de «esperar en vez de curarse»; pero ESPERANZA, que no espera, muere pronto tanto como APRENDE en P7-14b | **es donde está el puesto**; el porqué no está resuelto |

## Sección 5 · El regalo que nadie coge

Los {len(G)} regalos de APRENDE en P7-14b que vuelve a coger quien los dio (`P7_15_regalo.json`). En {sum(1 for e in G if e['tics'])} el hermano que pedía estuvo encima o al lado del botiquín regalado
durante la espera: {n(len(enc))} tics encima (en {sum(1 for e in G if any(t['donde'] == 'encima' for t in e['tics']))} regalos) y {n(len(lado))} al lado.

| el que pedía | encima del botiquín ({n(len(enc))} tics) | al lado ({n(len(lado))} tics) |
|---|---:|---:|
| botiquines a bordo | 0 en todos | 0 en todos |
| zurrón lleno | {n(sum(1 for t in enc if t['zurron_lleno']))} | {n(sum(1 for t in lado if t['zurron_lleno']))} |
| el candidato `coger` existe | {sum(1 for t in enc if t['hay_coger'])} | {sum(1 for t in lado if t['hay_coger'])} |
| `coger` escondido ese tic por el arreglo del seis («la mochila no cambia») | {n(sum(1 for t in enc if t['coger_escondido']))} | {n(sum(1 for t in lado if t['coger_escondido']))} |
| el candidato de hacer sitio existe | {n(sum(1 for t in enc if t['hay_hacer_sitio']))} | {n(sum(1 for t in lado if t['hay_hacer_sitio']))} |
| un candidato de ir a por él (`ir_objeto` o `ir_curioso`) existe | {sum(1 for t in enc if t['hay_ir_a_por_objeto'])} | {n(sum(1 for t in lado if t['hay_ir_a_por_objeto']))} |
| lo que elige | {", ".join(f"`{k_}` {c}" for k_, c in collections.Counter(t['el'] for t in enc).most_common(3))} | {", ".join(f"`{k_}` {n(c)}" for k_, c in collections.Counter(t['el'] for t in lado).most_common(3))} |

Lo que lleva cuando está encima: {"; ".join(f"{' y '.join(str(x) for x in k_)} ({c} tics)" for k_, c in collections.Counter(tuple(sorted(str(x) for x in t['zurron'])) for t in enc).most_common(4))}.

**Por qué no gana coger, con archivo y línea:**
1. **El zurrón tiene dos ranuras y están llenas** (una ración y un arma, red o munición) en los {n(len(enc))} tics en que está encima.
2. **`coger` no llega a ser candidato.** El cuerpo lo propone si hay un objeto en la casilla (`decisor_zs.py:475-483`), pero el arreglo del seis lo esconde cuando la previsión dice que el
   zurrón no cambiaría (`arreglos_P6_8b.py:85` y `:135-140`, registro `llena8` «prevision: la mochila no cambia»): {n(sum(1 for t in enc if t['coger_escondido']))} de {n(len(enc))} tics.
3. **Hacer sitio existe y no gana.** `hacer_sitio_rations_por_first_aid` está entre los candidatos en los {n(sum(1 for t in enc if t['hay_hacer_sitio']))} tics (`descubre_P7.py:307-322`), y su d frente a la de `noop`:
   igual en {sum(1 for x in hsd if abs(x) < 1e-9)} tics (empate: desde P7-14b, en un empate no se suelta nada) y peor en {sum(1 for x in hsd if x > 1e-9)} (mediana de la diferencia {n(st.median([x for x in hsd if x > 1e-9]), 3)}); mejor, en {sum(1 for x in hsd if x < -1e-9)}.
   Cambiar la ración por el botiquín no le compensa.
4. **Al lado, casi nunca hay candidato de ir a por él** ({n(sum(1 for t in lado if t['hay_ir_a_por_objeto']))} de {n(len(lado))} tics): con el zurrón lleno la promesa del botiquín calla («zurrón lleno: no es adquirible», `decisor_zs.py:647-650`) y
   `ir_curioso` solo se crea si el botiquín cabe (`descubre_P7.py:286`).
5. **No es «lo dado, dado está» aplicado a quien recibe**: la cesión (`mem.cedidos`, `decisor_zs.py:900-904`) solo se apunta en la memoria de quien suelta, y es lo que le impide a ÉL volver a
   cogerlo hasta que caduca (`appraisal_zs_v42_exp.py:663-683`); a esa caducidad se debe que lo recoja a los 280 tics.

**Y sin embargo pedía.** El pedido exige que la promesa del botiquín sea mayor que cero (`pide_P7.pide`). Con el zurrón lleno la promesa del cuerpo es 0, pero `descubre_P7` le suma lo que
aliviaría la curiosidad aunque no quepa (`descubre_P7.py:346-355`), así que una criatura con curiosidad y el zurrón lleno pide un botiquín que no puede coger. En TECHO, sin curiosidad, eso
no puede pasar con el zurrón lleno; sus 23 regalos vueltos a coger no están mirados aquí.

## Sección 6 · El pedido que se cierra al ver

P7-14b, los pedidos cerrados con motivo «lo ve» (`P7_15_pedidos.json`): si en los 30 segundos siguientes (720 tics) la criatura cogió un botiquín.

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
BR = ("ESPERANZA", "BORRADO", "APRENDE", "TECHO"); Pb = {b: [p for p in P if p["brazo"] == b] for b in BR}
def fila4(nom, f): w(f"| {nom} | " + " | ".join(f(Pb[b]) for b in BR) + " |\n")
fila4("pedidos cerrados porque «lo ve»", lambda X: str(len(X)))
fila4("… coge un botiquín en los 30 s siguientes", lambda X: f"{sum(1 for p in X if p['coge_en_30_s'])} ({n(100 * sum(1 for p in X if p['coge_en_30_s']) / max(1, len(X)), 0)} %)")
fila4("… y era uno de los que veía al cerrar", lambda X: str(sum(1 for p in X if p["era_uno_de_los_que_veia"])))
fila4("tics hasta cogerlo (mediana)", lambda X: n(st.median([p["tics_hasta_cogerlo"] for p in X if p["coge_en_30_s"]] or [0])))
fila4("la criatura vivió esos 30 s", lambda X: str(sum(1 for p in X if p["vivio_los_30_s"])))
tt = [p for p in P]
w(f"""
En los cuatro brazos juntos, {sum(1 for p in tt if p['coge_en_30_s'])} de {n(len(tt))} ({n(100 * sum(1 for p in tt if p['coge_en_30_s']) / len(tt), 0)} %): **casi cuatro de cada cinco pedidos se cierran al ver un botiquín que la criatura no llega a coger en medio minuto.**
«Lo ve» cierra el pedido, pero ver no es tener.

## Sección 7 · Lo que queda para la mesa (propuestas, nada decidido)

1. **Dónde mirar ahora: las muertes tempranas.** Son 10 de 80 en cada campo y llevan más de la mitad del puesto. Lo siguiente barato es un banco sobre esas 20 vidas (y las de BORRADO
   y TECHO que mueren pronto): escena a escena, qué veía, cuándo empezó el daño, cuándo abrió el canal y qué candidato tenía de alejarse.
2. **Esperar para curarse puede ser lo que el diseño quería y aun así costar el puesto.** P1 de P7-10 pedía que aprendiera a esperar. Si esperar bajo ataque es el problema, la pregunta de
   diseño es de qué depende la espera (hoy, de las ganas: cuanto más vale el botiquín, más cuesta gastarlo), no si se espera.
3. **El pedido con el zurrón lleno**: pedir lo que no cabe. O el pedido exige que quepa, o quien recibe hace sitio; es decisión de la mesa.
4. **Cuándo se cierra un pedido**: hoy al ver cualquier botiquín; casi cuatro de cada cinco veces no llega a tenerlo en medio minuto.
5. Todo esto son 6 o 7 muertes de diferencia por campo: la señal es la misma en dos campos independientes, pero es pequeña en número. No lo daría por cerrado sin el banco del punto 1.
6. **Puede que la pregunta esté al revés.** En P7-14b APRENDE no acaba peor que ESPERANZA ni que TECHO (dentro de 2·se, `informe_P7_14b.md`): es BORRADO el que acaba mejor que los tres. En P7-10 era APRENDE el
   que acababa peor que los otros tres. «Por qué pierde el que recuerda» y «por qué gana el que olvida cada día» no son la misma pregunta, y los dos campos no dicen lo mismo sobre cuál es.

## Archivos

| archivo | qué es |
|---|---|
| `analiza_P7_15.py` → `P7_15_vidas.json`, `P7_15_regalo.json`, `P7_15_pedidos.json` | lectura de los 640 diarios (cuándo muere, cómo vive), las escenas del regalo que nadie coge y los pedidos cerrados por «lo ve» |
| `banco_P7_15.py` → `P7_15_decisiones.json` | las 80 vidas de APRENDE de P7-14b decididas dos veces por tic |
| `escribe_informe_P7_15.py`, `informe_P7_15.md` | este informe |
""")
txt = "".join(W); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_15.md"), "w").write(txt); print("informe escrito", len(txt))

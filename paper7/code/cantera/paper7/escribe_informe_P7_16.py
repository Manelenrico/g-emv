"""[P7-16] Escribe informe_P7_16.md desde P7_16_vidas.json (analiza_P7_16.py), P7_16_pedir.json (banco_P7_16.py), P7_16_F1.json y P7_14b_vidas.json."""
import collections, hashlib, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
J = lambda p: json.load(open(os.path.join(AQUI, p))); md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
V = list(J("P7_16_vidas.json").values()); PE = J("P7_16_pedir.json"); F1 = J("P7_16_F1.json"); V14 = J("P7_14b_vidas.json")
BZ = lambda b: "ESPERANZA" if b == "SUELO" else b; BR = ("ESPERANZA", "BORRADO", "APRENDE", "TECHO"); CAMPOS = ("P7-10", "P7-14b")
TIPOS = ("emboscada", "pelea larga", "curandose bajo golpes", "esperando con botiquin", "anillo", "otra")
TN = {"emboscada": "emboscada", "pelea larga": "pelea larga", "curandose bajo golpes": "curándose bajo golpes", "esperando con botiquin": "esperando con botiquín", "anillo": "anillo", "otra": "otra"}
L = lambda c, b: [v for v in V if v["campo"] == c and BZ(v["brazo"]) == b]
def tem(c, b, corte): return [v for v in L(c, b) if "escena" in v and v["ultimo_tick"] < corte]
med = lambda xs: (st.median(xs) if xs else None)
W = []; w = W.append
def fila8(nom, f): w(f"| {nom} | " + " | ".join(f(c, b) for c in CAMPOS for b in BR) + " |\n")
E12 = [v for v in V if "escena" in v]; E11 = [v for v in E12 if v["ultimo_tick"] < 11000]
def suma(X, k): return sum(v["escena"]["episodio"][k] for v in X if v["escena"]["episodio"])
def cuenta(X, f): return sum(1 for v in X if v["escena"]["episodio"] and f(v["escena"]["episodio"]))
def par(a, b, m, campo, src="primeros"):
    ps = collections.defaultdict(lambda: {a: [], b: []})
    for v in V:
        x = v[src][m] if src else v[m]
        if v["campo"] == campo and BZ(v["brazo"]) in (a, b) and x is not None: ps[v["semilla"]][BZ(v["brazo"])].append(x)
    d = [st.mean(p[a]) - st.mean(p[b]) for p in ps.values() if p[a] and p[b]]; mu = st.mean(d); se = st.stdev(d) / math.sqrt(len(d))
    return {"a": st.mean(x for p in ps.values() for x in p[a]), "b": st.mean(x for p in ps.values() for x in p[b]), "d": mu, "z": (mu / se if se else 0.0)}
w(f"""# P7-16 · Las muertes tempranas, escena a escena, y pedir corregido

*5-oct-2026. Último análisis de este asunto: se informa de lo que se sostiene y no se prueban hipótesis nuevas. Todo es POSTERIOR A LOS SELLOS de
P7-10 y P7-14b. Coste: **créditos de la plataforma 0 USD; consola de Anthropic 0 USD.** `motor/model.py` = `{md5('motor/model.py')}` al empezar y al
acabar; cuerpo y congelados sin tocar. Parte A: lectura de los 640 diarios (`analiza_P7_16.py` → `P7_16_vidas.json`). Parte B: código nuevo detrás de un
interruptor apagado por defecto y un banco de réplica, una vida por proceso (`banco_P7_16.py` → `P7_16_pedir.json`); no se ha jugado nada.*

{{CORTO}}

# PARTE A · LAS ESCENAS

## Sección 1 · Las muertes tempranas, una por una

Todas las vidas que mueren antes del tic 12.000 en los cuatro brazos y los dos campos: **{len(E12)}** ({len(E11)} antes del tic 11.000). El brazo ESPERANZA de P7-14b es el SUELO de P7-10.

| | P7-10: ESPERANZA | BORRADO | APRENDE | TECHO | P7-14b: ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
""")
fila8("mueren antes del tic 11.000", lambda c, b: str(len(tem(c, b, 11000))))
fila8("mueren antes del tic 12.000", lambda c, b: str(len(tem(c, b, 12000))))
w("""
Lo que sigue es de las muertes antes del tic 12.000 (el corte ancho), con los dos campos juntos por brazo; el EPISODIO FINAL DE DAÑO son los golpes
seguidos sin un hueco de más de 10 segundos hasta la muerte.

| en el episodio final | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
""")
def fila4(nom, f): w(f"| {nom} | " + " | ".join(f([v for v in E12 if BZ(v['brazo']) == b]) for b in BR) + " |\n")
ep = lambda X: [v["escena"]["episodio"] for v in X if v["escena"]["episodio"]]; ve = lambda X: [v["escena"]["ventana_30_s"] for v in X]
fila4("muertes", lambda X: str(len(X)))
fila4("rivales distintos vistos en los 30 s anteriores (mediana)", lambda X: n(med([x["rivales_distintos"] for x in ve(X)])))
fila4("distancia mínima a un rival en esos 30 s (mediana, casillas)", lambda X: n(med([x["dist_minima_a_un_rival"] for x in ve(X) if x["dist_minima_a_un_rival"] is not None])))
fila4("tics con un rival a 2 casillas o menos, de 720 (mediana)", lambda X: n(med([x["tics_con_rival_a_2_o_menos"] for x in ve(X)])))
fila4("el daño empieza… tics antes de morir (mediana)", lambda X: n(med([e["dura_tics"] for e in ep(X)])))
fila4("… desde la vida (mediana)", lambda X: n(med([e["desde_la_vida"] for e in ep(X)])))
fila4("… desde 80 de vida o más", lambda X: str(sum(1 for e in ep(X) if e["desde_la_vida"] >= 80)))
fila4("daño de rivales en el episodio (mediana)", lambda X: n(med([e["dano_de_rivales"] for e in ep(X)]), 1))
fila4("llevaba botiquín en el episodio", lambda X: str(sum(1 for e in ep(X) if e["llevo_botiquin_en_el_episodio"])))
fila4("abrió el canal en el episodio", lambda X: str(sum(1 for e in ep(X) if e["aperturas_del_canal"])))
fila4("veces que abrió el canal / gastó el botiquín / se le cortó", lambda X: f"{sum(e['aperturas_del_canal'] for e in ep(X))} / {sum(e['canales_gastados'] for e in ep(X))} / {sum(e['canales_cortados'] for e in ep(X))}")
fila4("murió con el canal abierto", lambda X: str(sum(1 for e in ep(X) if e["canal_abierto_al_morir"])))
fila4("eligió esperar con el candidato de usar delante, 1 s o más", lambda X: str(sum(1 for e in ep(X) if e["tics_esperando"] >= 24)))
fila4("tics esperando en el episodio (mediana)", lambda X: n(med([e["tics_esperando"] for e in ep(X)])))
fila4("tics con un rival a 5 o menos (mediana)", lambda X: n(med([e["tics_con_rival_a_5_o_menos"] for e in ep(X)])))
fila4("… de ellos, con un candidato de alejarse", lambda X: f"{n(100 * sum(e['tics_con_candidato_de_alejarse'] for e in ep(X)) / max(1, sum(e['tics_con_rival_a_5_o_menos'] for e in ep(X))))} %")
fila4("… cuando lo hay, lo elige", lambda X: f"{n(100 * sum(e['tics_en_que_eligio_alejarse'] for e in ep(X)) / max(1, sum(e['tics_con_candidato_de_alejarse'] for e in ep(X))))} %")
fila4("cuánto peor es la d de alejarse que la del elegido (mediana de las medianas)", lambda X: n(med([e["d_de_alejarse_menos_la_del_elegido_mediana"] for e in ep(X) if e["d_de_alejarse_menos_la_del_elegido_mediana"] is not None]), 3))
ap14 = [v for v in E12 if v["campo"] == "P7-14b" and v["brazo"] == "APRENDE"]
w(f"""
Lo que se lee, sin más:
- **Casi todas empiezan con la vida entera** (mediana 100 en los cuatro brazos) y duran poco: de la primera herida a la muerte pasan entre {n(min(med([e['dura_tics'] for e in ep([v for v in E12 if BZ(v['brazo']) == b])]) for b in BR))} y {n(max(med([e['dura_tics'] for e in ep([v for v in E12 if BZ(v['brazo']) == b])]) for b in BR))} tics de mediana (de 10 a 18 segundos).
- **El canal casi nunca llega a curar.** Entre los cuatro brazos se abrió {suma(E12, 'aperturas_del_canal')} veces en esos episodios, se gastó el botiquín {suma(E12, 'canales_gastados')} y se cortó {suma(E12, 'canales_cortados')}. Un golpe corta el canal; quien lo abre bajo golpes lo pierde.
- **Alejarse existe poco y gana menos**: con un rival a 5 casillas o menos, hay un candidato de paso que se aleja en entre el 15 y el 36 % de los tics, y cuando lo hay se elige uno de cada cinco o tres veces.
  El resto de los tics el cuerpo no tiene paso que dar (el enfriamiento del movimiento: solo `noop`) o prefiere otra cosa.
- **Esperar con el botiquín delante** (1 segundo o más en el episodio): APRENDE {cuenta([v for v in E12 if v['brazo'] == 'APRENDE'], lambda e: e['tics_esperando'] >= 24)} de {len([v for v in E12 if v['brazo'] == 'APRENDE'])}, TECHO {cuenta([v for v in E12 if v['brazo'] == 'TECHO'], lambda e: e['tics_esperando'] >= 24)} de {len([v for v in E12 if v['brazo'] == 'TECHO'])}, BORRADO {cuenta([v for v in E12 if v['brazo'] == 'BORRADO'], lambda e: e['tics_esperando'] >= 24)} de {len([v for v in E12 if v['brazo'] == 'BORRADO'])}, ESPERANZA {cuenta([v for v in E12 if BZ(v['brazo']) == 'ESPERANZA'], lambda e: e['tics_esperando'] >= 24)} de {len([v for v in E12 if BZ(v['brazo']) == 'ESPERANZA'])}.
  En APRENDE de P7-14b, el banco de P7-15 (decidir con y sin los días anteriores) da tics de «quieto en vez de usar» en los últimos 30 segundos en {sum(1 for v in ap14 if (v['escena'].get('banco_P7_15_quieto_en_vez_de_usar_en_30_s') or 0) > 0)} de las {len(ap14)}.

## Sección 2 · Los tipos

Declarados en la cabecera de `analiza_P7_16.py` antes de contar, y aplicados en este orden (el primero que cumpla): **anillo** (en el episodio final el anillo
hace más daño que los rivales); **curándose bajo golpes** (abrió el canal en el episodio y recibió daño de un rival con él abierto, o murió con él abierto);
**esperando con botiquín** (llevaba botiquín, tuvo el candidato de usarlo y eligió otra cosa 1 segundo o más, sin llegar a abrir el canal); **emboscada**
(nada de lo anterior y de la primera herida a la muerte pasan 10 segundos o menos); **pelea larga** (más de 10 segundos). Los umbrales de 10 y de 1 segundo son míos.

Antes del tic 12.000:

| tipo | P7-10: ESPERANZA | BORRADO | APRENDE | TECHO | P7-14b: ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
""")
for t in TIPOS:
    if any(v["escena"]["tipo"] == t for v in E12): fila8(TN[t], lambda c, b, t=t: str(sum(1 for v in tem(c, b, 12000) if v["escena"]["tipo"] == t)))
fila8("**total**", lambda c, b: f"**{len(tem(c, b, 12000))}**")
w("""
Antes del tic 11.000:

| tipo | P7-10: ESPERANZA | BORRADO | APRENDE | TECHO | P7-14b: ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
""")
for t in TIPOS:
    if any(v["escena"]["tipo"] == t for v in E11): fila8(TN[t], lambda c, b, t=t: str(sum(1 for v in tem(c, b, 11000) if v["escena"]["tipo"] == t)))
fila8("**total**", lambda c, b: f"**{len(tem(c, b, 11000))}**")
tA = {t: sum(1 for v in E12 if v["brazo"] == "APRENDE" and v["escena"]["tipo"] == t) for t in TIPOS}; tB = {t: sum(1 for v in E12 if v["brazo"] == "BORRADO" and v["escena"]["tipo"] == t) for t in TIPOS}
w(f"""
**No hay un tipo de muerte que sea el de APRENDE.** Con el corte en 12.000 y los dos campos juntos, APRENDE tiene {tA['emboscada']} emboscadas, {tA['pelea larga']} peleas largas, {tA['anillo']} por el anillo,
{tA['curandose bajo golpes']} curándose bajo golpes y {tA['esperando con botiquin']} esperando con botiquín; BORRADO, {tB['emboscada']}, {tB['pelea larga']}, {tB['anillo']}, {tB['curandose bajo golpes']} y {tB['esperando con botiquin']}. APRENDE tiene más de casi todo, y el reparto cambia de un campo a otro
(en P7-10 mandan las peleas largas, en P7-14b las emboscadas). «Esperando con botiquín» como tipo casi no existe ({sum(1 for v in E12 if v['escena']['tipo'] == 'esperando con botiquin')} de {len(E12)}): quien espera con el botiquín acaba abriendo el canal y cae en «curándose bajo golpes», o muere de otra cosa.

## Sección 3 · TECHO

| | P7-10 | P7-14b |
|---|---:|---:|
| muertes de TECHO antes del tic 11.000 / 12.000 | {len(tem('P7-10', 'TECHO', 11000))} / {len(tem('P7-10', 'TECHO', 12000))} | {len(tem('P7-14b', 'TECHO', 11000))} / {len(tem('P7-14b', 'TECHO', 12000))} |
| … en las que esperó 1 s o más con el candidato de usar delante | {cuenta(tem('P7-10', 'TECHO', 12000), lambda e: e['tics_esperando'] >= 24)} | {cuenta(tem('P7-14b', 'TECHO', 12000), lambda e: e['tics_esperando'] >= 24)} |
| lo mismo en APRENDE: muertes / con espera | {len(tem('P7-10', 'APRENDE', 12000))} / {cuenta(tem('P7-10', 'APRENDE', 12000), lambda e: e['tics_esperando'] >= 24)} | {len(tem('P7-14b', 'APRENDE', 12000))} / {cuenta(tem('P7-14b', 'APRENDE', 12000), lambda e: e['tics_esperando'] >= 24)} |

Parte de la vida esperando (toda la vida; un tic con `usar_botiquin` entre los candidatos y otra cosa elegida):

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| P7-10 | """ + " | ".join(f"{n(100 * st.mean(v['esperando_toda_la_vida'] for v in L('P7-10', b)), 1)} %" for b in BR) + """ |
| P7-14b | """ + " | ".join(f"{n(100 * st.mean(v['esperando_toda_la_vida'] for v in L('P7-14b', b)), 1)} %" for b in BR) + f""" |

**¿Por qué esperar no le cuesta a TECHO lo que parece costarle a APRENDE? Lo medido no dice que a APRENDE le cueste.** TECHO espera tanto como APRENDE o más
({n(100 * st.mean(v['esperando_toda_la_vida'] for v in L('P7-10', 'TECHO')), 1)} y {n(100 * st.mean(v['esperando_toda_la_vida'] for v in L('P7-14b', 'TECHO')), 1)} % de la vida, frente a {n(100 * st.mean(v['esperando_toda_la_vida'] for v in L('P7-10', 'APRENDE')), 1)} y {n(100 * st.mean(v['esperando_toda_la_vida'] for v in L('P7-14b', 'APRENDE')), 1)} %), y muere pronto menos que APRENDE en P7-10 ({len(tem('P7-10', 'TECHO', 11000))} contra {len(tem('P7-10', 'APRENDE', 11000))}) y casi lo mismo en P7-14b ({len(tem('P7-14b', 'TECHO', 11000))} contra {len(tem('P7-14b', 'APRENDE', 11000))}).
En sus muertes tempranas la espera aparece en {cuenta([v for v in E12 if v['brazo'] == 'TECHO'], lambda e: e['tics_esperando'] >= 24)} de {len([v for v in E12 if v['brazo'] == 'TECHO'])}; en las de APRENDE, en {cuenta([v for v in E12 if v['brazo'] == 'APRENDE'], lambda e: e['tics_esperando'] >= 24)} de {len([v for v in E12 if v['brazo'] == 'APRENDE'])}. Esperar acompaña a las muertes tempranas de APRENDE más que a las de TECHO, pero
el brazo que más espera no es el que más muere pronto. Con esto no se puede decir que esperar sea lo que mata: se queda en algo que APRENDE hace
mientras muere, no en la razón.

## Sección 4 · BORRADO

Los primeros 11.000 tics de cada vida, BORRADO menos cada uno de los otros tres brazos, emparejado por semilla (20 semillas por campo; d̄/se en cada campo).
En negrita, lo que pasa de 2 en los dos campos con el mismo signo.

| medida (primeros 11.000 tics) | BORRADO (P7-10 / P7-14b) | − APRENDE: d̄/se | − TECHO: d̄/se | − ESPERANZA: d̄/se |
|---|---|---|---|---|
""")
MB = [("vida_menos_de_50", "parte del tiempo con menos de 50 de vida", 3, 100), ("rival_a_1_o_2", "… con un rival a 1 o 2 casillas", 3, 100), ("rivales_a_la_vista_media", "rivales a la vista (media)", 2, 1), ("dist_al_centro", "distancia al centro del círculo", 2, 1),
      ("dist_al_hermano", "distancia al hermano", 2, 1), ("con_botiquin", "… con botiquín", 3, 100), ("con_racion", "… con ración", 3, 100), ("con_arma", "… con arma", 3, 100), ("zurron_lleno", "… con el zurrón lleno", 3, 100),
      ("casillas_por_1000_tics", "casillas por 1.000 tics", 1, 1), ("esperando", "… esperando con el candidato de usar delante", 3, 100), ("en_canal", "… con el canal abierto", 3, 100), ("dano_rival_por_1000_tics", "daño de rivales por 1.000 tics", 2, 1),
      ("golpes_de_rival", "golpes de rival recibidos", 2, 1), ("ir_curioso", "… con `ir_curioso` elegido", 3, 100), ("ir_objeto", "… con `ir_objeto` elegido", 3, 100), ("noop", "… con `noop` elegido", 3, 100)]
fuertes = collections.defaultdict(list)
for m, nom, de, f in MB:
    cel = []
    for otro in ("APRENDE", "TECHO", "ESPERANZA"):
        x, y = par("BORRADO", otro, m, "P7-10"), par("BORRADO", otro, m, "P7-14b"); dos = abs(x["z"]) > 2 and abs(y["z"]) > 2 and x["d"] * y["d"] > 0
        if dos: fuertes[otro].append(nom)
        cel.append(f"{'**' if dos else ''}{n(x['z'], 1)} / {n(y['z'], 1)}{'**' if dos else ''}")
    b10, b14 = par("BORRADO", "APRENDE", m, "P7-10")["a"], par("BORRADO", "APRENDE", m, "P7-14b")["a"]
    w(f"| {nom} | {n(f * b10, 1 if f == 100 else de)}{' %' if f == 100 else ''} / {n(f * b14, 1 if f == 100 else de)}{' %' if f == 100 else ''} | " + " | ".join(cel) + " |\n")
w(f"""
- **Frente a APRENDE, nada pasa la prueba de los dos campos** ({", ".join(fuertes['APRENDE']) or "ninguna medida"}). Lo más cerca: BORRADO espera menos con el botiquín delante (d̄/se {n(par('BORRADO', 'APRENDE', 'esperando', 'P7-10')['z'], 1)} y {n(par('BORRADO', 'APRENDE', 'esperando', 'P7-14b')['z'], 1)}).
- **Frente a TECHO y a ESPERANZA**, lo que pasa en los dos campos es lo que el diseño pone: {", ".join(fuertes['TECHO']) or "nada"} (BORRADO tiene curiosidad y ellos no; por eso está menos tiempo sin hacer nada).
- Juntando las dos cosas: BORRADO es el único brazo que **se mueve por curiosidad y a la vez no espera para curarse** (cada día empieza sin saber, con el
  botiquín valorado como una ración). APRENDE tiene la curiosidad pero espera; ESPERANZA no espera pero no tiene curiosidad; TECHO ni lo uno ni lo otro.
  Que esa combinación sea la que le da ventaja es una lectura de la tabla, no algo medido: ninguna de las medidas de cómo vive en esos 11.000 tics
  (poca vida, rivales cerca, daño recibido, lo que lleva, dónde está) lo separa de los otros tres en los dos campos.

## Sección 5 · Conclusión en tres líneas

- **Se sostiene en los dos campos a la vez:** APRENDE acaba alrededor de un puesto peor que BORRADO y muere más antes del tic 11.000 y del 12.000; BORRADO es el único brazo con curiosidad que no espera para curarse.
- **No se sostiene:** que haya un tipo de muerte propio de APRENDE; que esperar para curarse sea lo que mata (TECHO espera lo mismo; ESPERANZA no espera y muere pronto igual en P7-14b); que APRENDE viva distinto (vida, peleas, zurrón, sitio) antes de morir.
- **Queda abierto:** por qué BORRADO muere pronto menos que los otros tres en P7-14b, y si la diferencia de 6 o 7 muertes tempranas por campo es algo del cuaderno o del azar de las partidas; con estos dos campos no se puede decidir.

# PARTE B · PEDIR CORREGIDO

{{PARTE_B}}

## Archivos

| archivo | qué es |
|---|---|
| `analiza_P7_16.py` → `P7_16_vidas.json` | las escenas de las 95 muertes tempranas, los tipos, la espera y los primeros 11.000 tics de las 640 vidas |
| `pide_P7.py` (`pide2`, `cabe`, `haria_sitio`), `descubre_P7.py` (`PIDE2`, `_promesa`) | pedir corregido, detrás de `GEMV_P7_PIDE2` (apagado por defecto) |
| `banco_P7_16.py` → `P7_16_pedir.json`; `P7_16_F1.json` | el banco de pedir corregido sobre P7-14b y F1 |
| `escribe_informe_P7_16.py`, `informe_P7_16.md` | este informe |
""")
# ───────── parte B ─────────
PV = PE["por_vida"]; G = PE["regalos"]; B = []; b = B.append
def sb(k, brazo=None): return sum(x[k] for x in PV.values() if brazo is None or x["brazo"] == brazo)
def cier(k, brazo=None):
    c = collections.Counter()
    for x in PV.values():
        if brazo is None or x["brazo"] == brazo: c.update(x[k])
    return c
b(f"""## Sección 6 · Lo construido

En `pide_P7.py` y `descubre_P7.py`, detrás del interruptor `GEMV_P7_PIDE2` (0 por defecto: los campos jugados se replican como se jugaron; con 0 nada cambia).

| regla (diseño de Manel) | cómo está hecha | dónde |
|---|---|---|
| (a) el pedido se cierra al tener, o cuando ya no le falta vida; no al verlo | una vez abierto sigue abierto hasta que el botiquín está en el zurrón o la vida llega a su máximo (`mem.hp_max`); ver un botiquín ya no lo cierra. Para abrirlo sigue haciendo falta no ver ninguno | `pide_P7.pide2` |
| (b) solo se pide lo que se podría coger | con un hueco para él (`decisor_zs._pack_con`, la prueba de «cabe» del cuerpo) y la promesa mayor que cero; o, con el zurrón lleno, si hacer sitio ganaría: se le pregunta a `decide`, sobre una copia de la escena con un botiquín en su casilla y una copia de la memoria, si elegiría `hacer_sitio_<algo>_por_<botiquín>`. Si no, no pide, y un pedido abierto se cierra | `pide_P7.cabe`, `pide_P7.haria_sitio` |
| (c) las ganas no suman alivio de curiosidad cuando no se podría llevar | `_promesa` devuelve solo la promesa del cuerpo (que con el zurrón lleno es 0) cuando el botiquín no cabe | `descubre_P7.py`, `_promesa` |

**Una consecuencia de (a) que la mesa debe ver:** si el pedido se cierra «cuando ya no le falta vida», una criatura con la vida entera no puede tener un pedido abierto
(se cerraría en el parte siguiente). Lo he hecho así, literal: **con el pedido corregido solo se pide estando herido.** En P7-14b, {n(sb('campo_pedia_sin_faltarle_vida'))} de los {n(sb('campo_con_pedido'))} partes con pedido
se emitieron con la vida entera.

**F1 sigue pasando** (`P7_16_F1.json`): apagado {n(F1['apagado']['fidelidad']['igual'])} tics iguales y {F1['apagado']['fidelidad']['difiere']} distintos; TECHO {n(F1['TECHO']['fidelidad']['igual'])} y {F1['TECHO']['fidelidad']['difiere']} (los dos de siempre).

## Sección 7 · El banco sobre P7-14b

`banco_P7_16.py`: las 320 vidas de P7-14b replicadas con el pedido corregido. La réplica sigue el diario: dice qué parte habría emitido cada criatura en la vida que vivió,
no cómo habría sido la partida. Fidelidad de la elección tic a tic: pase 1, {n(PE['fidelidad_pase1'].get('igual', 0))} iguales y {n(PE['fidelidad_pase1'].get('difiere', 0))} distintos (los distintos vienen de (c): sin el alivio de curiosidad de lo que no cabe, algunos pasos cambian).

| | ESPERANZA | BORRADO | APRENDE | TECHO | los cuatro |
|---|---:|---:|---:|---:|---:|
""")
def filb(nom, f): b(f"| {nom} | " + " | ".join(f(x) for x in BR) + f" | {f(None)} |\n")
filb("partes comparados", lambda x: n(sb("partes", x)))
filb("partes con pedido en el campo", lambda x: n(sb("campo_con_pedido", x)))
filb("partes con pedido, corregido", lambda x: n(sb("nuevo_con_pedido", x)))
filb("pedía en el campo y corregido no", lambda x: n(sb("pedia_y_ya_no", x)))
filb("… porque no tenía hueco", lambda x: n(sb("campo_pedia_sin_hueco", x)))
filb("… porque no le faltaba vida", lambda x: n(sb("campo_pedia_sin_faltarle_vida", x)))
filb("no pedía en el campo y corregido sí", lambda x: n(sb("no_pedia_y_ahora_si", x)))
filb("partes con pedido porque hacer sitio ganaría", lambda x: n(sb("nuevo_por_hacer_sitio", x)))
filb("pedidos abiertos en el campo", lambda x: n(sb("campo_abiertos", x)))
filb("pedidos abiertos, corregido", lambda x: n(sb("nuevo_abiertos", x)))
mot_c = cier("campo_cierres"); mot_n = cier("nuevo_cierres")
filb("cierres en el campo: «lo ve» / «lo lleva» / otros", lambda x: (lambda c: f"{c.get('lo ve', 0)} / {c.get('lo lleva', 0)} / {sum(v for k_, v in c.items() if k_ not in ('lo ve', 'lo lleva'))}")(cier("campo_cierres", x)))
filb("cierres corregido: «lo lleva» / «ya no le falta vida» / «no podría cogerlo» / «ya no le alivia»", lambda x: (lambda c: f"{c.get('lo lleva', 0)} / {c.get('ya no le falta vida', 0)} / {c.get('no podria cogerlo', 0)} / {c.get('ya no le alivia (promesa 0)', 0)}")(cier("nuevo_cierres", x)))
GA = [g for g in G if g["brazo"] == "APRENDE"]; G48 = [g for g in GA if g["destino_en_el_campo"] == "lo recoge el mismo"]
b(f"""
**Los regalos** (pase 2: quien regaló oye los partes corregidos del hermano; {n(PE['partes_cambiados_pase2'])} partes cambian; fidelidad {n(PE['fidelidad_pase2'].get('igual', 0))} iguales, {n(PE['fidelidad_pase2'].get('difiere', 0))} distintos):

| | regalos en el campo | el hermano pediría (corregido) | la réplica sigue regalando | no se habrían hecho |
|---|---:|---:|---:|---:|
| **los 48 de APRENDE que volvían a quien los dio** | {len(G48)} | {sum(1 for g in G48 if g['hermano_pide_corregido'])} | {sum(1 for g in G48 if g['sigue_regalando'])} | **{sum(1 for g in G48 if not g['sigue_regalando'])}** |
| los 7 de APRENDE que cogió el hermano | {sum(1 for g in GA if g['destino_en_el_campo'] == 'lo recoge el hermano')} | {sum(1 for g in GA if g['destino_en_el_campo'] == 'lo recoge el hermano' and g['hermano_pide_corregido'])} | {sum(1 for g in GA if g['destino_en_el_campo'] == 'lo recoge el hermano' and g['sigue_regalando'])} | {sum(1 for g in GA if g['destino_en_el_campo'] == 'lo recoge el hermano' and not g['sigue_regalando'])} |
| todos los de APRENDE | {len(GA)} | {sum(1 for g in GA if g['hermano_pide_corregido'])} | {sum(1 for g in GA if g['sigue_regalando'])} | {sum(1 for g in GA if not g['sigue_regalando'])} |
| todos los de TECHO | {sum(1 for g in G if g['brazo'] == 'TECHO')} | {sum(1 for g in G if g['brazo'] == 'TECHO' and g['hermano_pide_corregido'])} | {sum(1 for g in G if g['brazo'] == 'TECHO' and g['sigue_regalando'])} | {sum(1 for g in G if g['brazo'] == 'TECHO' and not g['sigue_regalando'])} |
| todos (los cuatro brazos) | {len(G)} | {sum(1 for g in G if g['hermano_pide_corregido'])} | {sum(1 for g in G if g['sigue_regalando'])} | {sum(1 for g in G if not g['sigue_regalando'])} |

{{LECTURA_B}}
""")
def txt_de(nombre):
    p = os.path.join(AQUI, "_P7_16_tmp", nombre); return open(p).read().strip() if os.path.exists(p) else "(pendiente)"
txt = "".join(W).replace("{PARTE_B}", "".join(B)).replace("{LECTURA_B}", txt_de("lectura_b.md")).replace("{CORTO}", txt_de("corto.md")); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_16.md"), "w").write(txt); print("informe escrito", len(txt))

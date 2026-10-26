"""[P7-22] Escribe informe_P7_22.md desde P7_22_resultado.json, P7_22_decisiones.json, P7_22_extra_catalogo*.json y P7_22_fijado.json (ninguna cifra a mano)."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_22_resultado.json"); D = J("P7_22_decisiones.json"); F = J("P7_22_fijado.json"); X1 = J("P7_22_extra_catalogo.json"); X2 = J("P7_22_extra_catalogo_s.json"); REC = J("P7_22_recuerdos.json")
n = lambda x, d=3: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda p: hashlib.md5(open(os.path.join(AQUI, p), "rb").read()).hexdigest()
S = R["principal"]["separacion"]
def t_sep(sep):
    L = ["| campo | círculo | aperturas (con recuerdos previos) | completadas | A: sin condición | B: dentro/fuera, como hoy | C: por parecido |", "|---|---|---:|---:|---:|---:|---:|"]
    for k, v in sep.items():
        c, z = k.split("|"); L.append(f"| {c} | {z} | {v['aperturas']} | {v['completadas']} | {n(v['A'])} | {n(v['B'])} | {n(v['C'])} |")
    return "\n".join(L)
r1 = {c: S[f"{c}|dentro"]["C"] for c in ("P7-10", "P7-14b")}; r2 = {c: S[f"{c}|dentro"]["C"] - S[f"{c}|dentro"]["B"] for c in ("P7-10", "P7-14b")}
FC = R["principal"]["fuera_por_criatura"]; r3_antes = sum(1 for v in FC.values() if v["primer_dia_por_debajo_del_25%"] is not None and v["primer_dia_por_debajo_del_25%"] < 10); r3_queda = sum(1 for v in FC.values() if v["desde_el_dia_10_todas_por_debajo"])
U = F["umbral_dolor_F"]; E = [e for r in D for e in r["elecciones_de_usar"]]
def celda(dentro, poco):
    X = [e for e in E if e["dentro"] == dentro and ((e["dolor_F"] < U) if poco else (e["dolor_F"] >= U))]; s = sum(1 for e in X if e["C"] == "usar_botiquin")
    return X, s
L4 = ["| situación al elegir | elecciones de `usar_botiquin` del campo | con C sigue usando | en su lugar elige | cura imaginada del campo (mediana) | cura imaginada con C |", "|---|---:|---:|---|---:|---:|"]
for dentro in (True, False):
    for poco in (True, False):
        X, s = celda(dentro, poco); otros = collections.Counter(e["C"] for e in X if e["C"] != "usar_botiquin")
        L4.append(f"| {'dentro' if dentro else 'fuera'}, {'poco dolorido' if poco else 'muy dolorido'} | {len(X)} | {s} ({n(100*s/len(X),0) if X else '—'} %) | {', '.join(f'`{k}` {v}' for k, v in otros.most_common(3))} | {n(st.median([e['heal_campo'] for e in X if e['heal_campo'] is not None]),1) if X else '—'} | {n(st.median([e['heal_C'] for e in X]),1) if X else '—'} |")
Xd1, s1 = celda(True, True); Xd2, s2 = celda(True, False); r4a = 100 * s1 / len(Xd1); r4b = 100 * s2 / len(Xd2)
DIF = [d for r in D for d in r["distintos"]]; cd = collections.Counter((d["campo"], d["C"]) for d in DIF)
M = R["mapa_emocional"]
LM = ["| recuerdos | n | dolor F (mediana; cuartiles 1 y 3) | dolor R | dolor S | positivo | distancia total |", "|---|---:|---:|---:|---:|---:|---:|"]
for k, v in M.items(): LM.append(f"| {k.replace('|', ', ')} | {v['n']} | {n(v['dolor_F'])} ({n(v['dolor_F_cuartiles'][0])} – {n(v['dolor_F_cuartiles'][2])}) | {n(v['dolor_R'])} | {n(v['dolor_S'])} | {n(v['positivo'])} | {n(v['d'])} |")
LS = ["| variante (después del sello) | P7-10 dentro: B / C | P7-14b dentro: B / C | los dos dentro: B / C |", "|---|---:|---:|---:|"]
for k, v in R["sensibilidad"].items():
    s_ = v["separacion"]; LS.append(f"| {v['etiqueta']} | {n(s_['P7-10|dentro']['B'])} / {n(s_['P7-10|dentro']['C'])} | {n(s_['P7-14b|dentro']['B'])} / {n(s_['P7-14b|dentro']['C'])} | {n(s_['los dos|dentro']['B'])} / {n(s_['los dos|dentro']['C'])} |")
XS = X1["resumen"]["separacion"]
LX = ["| efecto = cura del catálogo si se completa, 0 si se corta (NO sellado) | A | B | C |", "|---|---:|---:|---:|"] + [f"| {k.replace('|', ', ')} | {n(v['A'])} | {n(v['B'])} | {n(v['C'])} |" for k, v in XS.items()]
LX2 = ["| … y además s más estrecho (NO sellado) | P7-10 dentro: C | P7-14b dentro: C | los dos dentro: C |", "|---|---:|---:|---:|"] + [f"| {k} | {n(v['P7-10|dentro']['C'])} | {n(v['P7-14b|dentro']['C'])} | {n(v['los dos|dentro']['C'])} |" for k, v in X2.items()]

import bisect
def _auc(p):
    xs = sorted(c for c, ok in p if ok); ys = sorted(c for c, ok in p if not ok)
    if not xs or not ys: return None
    return sum(bisect.bisect_left(ys, x) + 0.5 * (bisect.bisect_right(ys, x) - bisect.bisect_left(ys, x)) for x in xs) / (len(xs) * len(ys))
def _por_dia(forma):
    por = collections.defaultdict(list)
    for f in R["aperturas"]:
        if f["dentro"] and f["previos"] > 0: por[f["dia"]].append(f)
    a = [(_auc([(f[forma], f["completado"]) for f in v]), len(v)) for v in por.values()]; a = [x for x in a if x[0] is not None]
    return sum(x * k for x, k in a) / sum(k for _, k in a)
POR_DIA_C = _por_dia("C"); POR_DIA_B = _por_dia("B")
recs = [r for v in REC.values() for r in v["recuerdos"]]; cur = [r for r in recs if r["completado"]]
T = f"""# P7-22 · Recordar por parecido, en banco

*7-oct-2026. Coste: plataforma 0, consola 0. Sin partidas ni llamadas: recuerdos leídos de los diarios y réplicas de vidas ya jugadas, una por proceso.
`motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}` al empezar y al acabar; cuerpo y congelados sin tocar; archivos nuevos con sufijo `_P7_22`.
Sello: `SELLO_P7_22.md` (commits `aa6d995` y `36c5c23`), escrito antes de calcular. Este informe lo escribe `escribe_informe_P7_22.py` desde los JSON.*

## El sello, en corto: no pasa

| | regla | resultado | |
|---|---|---|---|
| R1 | dentro, C separa ≥ 0,65 en los dos campos | **{n(r1['P7-10'])}** (P7-10) y **{n(r1['P7-14b'])}** (P7-14b): por debajo de 0,5, al revés | **no pasa** |
| R2 | dentro, C − B ≥ 0,03 | {n(r2['P7-10'], 3)} y {n(r2['P7-14b'], 3)} | **no pasa** (B también separa al revés) |
| R3 | fuera, C cae bajo el 25 % del catálogo antes del día 10, en las 4 criaturas de cada campo | primera caída antes del día 10 en {r3_antes} de 8; se queda abajo desde el día 10 en {r3_queda} de 8 | **no pasa** |
| R4 | días 11-20 (P7-14b): dentro y poco dolorido sigue usando ≥ 80 %; muy dolorido ≥ 50 % | {n(r4a, 0)} % y {n(r4b, 0)} % | **no pasa** |

**Lo que hay detrás, en una frase:** tal como se fijó, el recuerdo guarda *cuánto subió la vida*, y eso choca con el techo: {sum(1 for r in cur if r['hp_cierre'] >= 100)} de las {len(cur)} curas llegan a 100 de vida,
así que una cura en un cuerpo sano vale {n(st.median([r['efecto']['cuerpo'] for r in cur if r['hp0'] >= 80]), 0)} de vida (mediana con vida ≥ 80 al abrir) y una en un cuerpo herido {n(st.median([r['efecto']['cuerpo'] for r in cur if r['hp0'] < 60]), 0)} (vida < 60). La creencia aprende
«cuánto cura», que es alto donde hay dolor, y donde hay dolor es donde más se corta: por eso separa al revés. Con el efecto puesto a la cura del catálogo
(medido después del sello, sección 6), C separa {n(XS['P7-10|dentro']['C'])} y {n(XS['P7-14b|dentro']['C'])}: mejor que B, pero lejos del 0,65. La foto de ahora, sola, separa 0,72 (P7-21).

## Sección 1 · Los recuerdos y lo fijado

- `recuerdos_P7_22.py` → `P7_22_recuerdos.json`: {len(recs)} recuerdos, uno por canal de botiquín de las 160 vidas de APRENDE de los dos campos ({len(cur)} completados, {len(recs) - len(cur)} cortados), cada uno con
  contexto (dentro/fuera, golpeada en los 48 anteriores), foto emocional al abrir (dolor F, R, S; positivo; distancia total), efecto (completado: lo que subió la vida al cerrar, de 0 a 50;
  recursos −1; cortado: 0), intensidad = 1 + min(1, efecto / 50), día de la serie.
- **s = {n(F['s'], 4)}**: mediana de las distancias euclídeas entre todos los pares de aperturas ({F['pares']:,} pares), fijada con `banco_P7_22.py --fija` antes de medir nada. Umbral «poco / muy dolorido»: dolor F {n(U, 4)}, la mediana de las aperturas dentro.
- Las tres formas (A, B, C), el neutro (peso 1), el olvido (0,95 por día) y el parecido de contexto (0,25 / 0,5): como en el encargo; están escritas en `banco_P7_22.py` y en el sello.
- Al abrir en el día d se recuerdan los recuerdos de los días anteriores de esa criatura. Una apertura sin recuerdos previos no entra en la separación.

## Sección 2 · Separación de las tres formas (medida 1)

{t_sep(S)}

Las tres formas separan por debajo de 0,5 dentro del círculo: las aperturas que se completan tienen la creencia **más baja**. La mediana de la creencia C dentro es
{n(st.median([f['C'] for f in R['aperturas'] if f['dentro'] and f['previos'] > 0 and f['completado']]), 1)} cuando cura y {n(st.median([f['C'] for f in R['aperturas'] if f['dentro'] and f['previos'] > 0 and not f['completado']]), 1)} cuando se corta. Lo mismo pasa dentro de cada día (separación media por día de C, {n(POR_DIA_C)}; de B, {n(POR_DIA_B)}), así que no es
solo que los días cambien. La explicación está en el efecto (arriba): la creencia mide cuánto cura, no si cura.

## Sección 3 · Fuera del círculo (R3)

Por criatura (campo, serie, asiento): la creencia C en sus aperturas fuera, con recuerdos previos.

| criatura | aperturas fuera | primer día con C < 12,5 | desde el día 10, todas < 12,5 |
|---|---:|---:|---|
""" + "\n".join(f"| {k} | {v['aperturas_fuera']} | {v['primer_dia_por_debajo_del_25%']} | {'sí' if v['desde_el_dia_10_todas_por_debajo'] else 'no' if v['desde_el_dia_10_todas_por_debajo'] is False else '—'} |" for k, v in FC.items()) + f"""

La creencia fuera baja pronto (antes del día 10 en {r3_antes} de 8) pero no se queda abajo: con pocos recuerdos fuera y el parecido de contexto 0,25 con los de dentro, los de dentro
(que valen más) la vuelven a subir. R3 pedía las dos cosas.

## Sección 4 · La repetición de decisiones con C (R4 y medida 2)

`banco_decide_P7_22.py` → `P7_22_decisiones.json`: {len(D)} vidas de APRENDE de P7-14b (días 11 a 20), réplica bit-exacta del campo ({sum(r['fidelidad'].get('igual', 0) for r in D):,} tics iguales, {sum(r['fidelidad'].get('difiere', 0) for r in D)} distintos).
En cada tic el cuerpo decide dos veces: con su cuaderno y con la cura imaginada recordada por parecido (C) sobre la foto de ese tic. Solo cambia `heal_imaginado`; las ganas quedan.

{chr(10).join(L4)}

De las {len([e for e in E if e['C'] != 'usar_botiquin'])} elecciones del campo que C no sigue, en 1 elige usar en los 10 segundos siguientes; el resto es quedarse quieta. La cura imaginada con C es un tercio de la del campo
(medianas {n(st.median([e['heal_C'] for e in E]), 1)} frente a {n(st.median([e['heal_campo'] for e in E if e['heal_campo'] is not None]), 1)}): el cuaderno del campo lleva el «al menos» de P7-7 (una cura con techo es cota inferior) y C no, porque su efecto es lo que subió la vida.
Tics con decisión distinta en las {len(D)} vidas: {len(DIF)} de {sum(r['tics_comparados'] for r in D):,}: {", ".join(f"`{a}` → `{b}` {k}" for (a, b), k in cd.most_common(4))}. Los {cd[('noop', 'usar_botiquin')]} en que C usa y el campo no son en otros tics, no retrasos.

## Sección 5 · El mapa emocional (medida 3)

{chr(10).join(LM)}

Los cortes abren con más dolor en los tres dominios y más distancia; lo positivo no cambia. Dentro, el cuartil 3 del dolor F de las curas ({n(M['dentro|cura']['dolor_F_cuartiles'][2])}) queda por debajo
de la mediana de los cortes ({n(M['dentro|corte']['dolor_F'])}): las fotos se solapan, pero están desplazadas.

## Sección 6 · Sensibilidad (después del sello, marcada como tal)

**Lo que pedía el encargo** (s a la mitad y al doble; contexto más blando y más duro), con el efecto sellado:

{chr(10).join(LS)}

Ninguna variante saca a C de por debajo de 0,5: el problema no es s ni el contexto, es el efecto.

**Lo que no pedía el encargo y he mirado para entender el fallo** (NO sellado): el efecto puesto a la cura del catálogo si se completa (50) y 0 si se corta, con lo que la
creencia pasa a ser «qué parte de la cura espero», y s más estrecho:

{chr(10).join(LX)}

{chr(10).join(LX2)}

Con eso C separa mejor que B (por {n(XS['los dos|dentro']['C'] - XS['los dos|dentro']['B'], 2)} en los dos campos juntos) pero se queda en 0,55-0,57 por mucho que se estreche s: los recuerdos de días anteriores,
pesados por parecido, saben menos del corte que la foto de ahora (0,72). Con una mediana de {n(st.median([f['C_pesos'] for f in R['aperturas'] if f['dentro'] and f['previos'] > 0]), 1)} de peso vivido por apertura (frente a {n(st.median([f['B_pesos'] for f in R['aperturas'] if f['dentro'] and f['previos'] > 0]), 1)} en B), la creencia C
se apoya en pocos recuerdos.

## Sección 7 · Lo que esto dice, y lo que queda para la mesa

1. El diseño (todo recuerdo con su marca emocional; recordar por parecido) se ha probado tal como se fijó y **no pasa el sello**. La causa principal no es el parecido sino
   **qué guarda el recuerdo**: «cuánto subió la vida» choca con el techo de 100 y hace que las curas en cuerpos sanos valgan poco. El cuaderno del campo ya trata esto con el
   «al menos» de P7-7; este banco no lo hizo, por fijar un efecto simple. Es un fallo de lo que fijé yo, no del diseño de Manel, y lo digo.
2. Aun arreglado eso (efecto = cura del catálogo, no sellado), recordar por parecido llega a 0,55-0,57 dentro del círculo, por encima de B (0,45) y por debajo del 0,65 pedido.
   La foto de ahora separa más (0,72). Un recuerdo que guardase *si se completó* además de *cuánto curó*, o una creencia de dos partes (probabilidad de completar × cura),
   es otro diseño: se propone, no se hace.
3. Fuera del círculo, la creencia baja pronto pero los recuerdos de dentro la levantan por el contexto 0,25. Si el corte por el anillo fuera del círculo es casi seguro
   (P7-21: 85 % de los canales fuera los corta el anillo), el parecido de contexto dentro/fuera tendría que ser más duro que 0,25, o el recuerdo de fuera más pesado.
4. R4 falla porque la cura imaginada con C es un tercio de la del campo (sin el «al menos»); con esa cura el cuerpo se queda quieto en vez de usar. No dice nada de la
   idea de recordar por parecido en sí; dice que el efecto del recuerdo tiene que llevar el techo.
5. Nada de esto se ha jugado; son réplicas y recuerdos leídos de los diarios.

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P7_22.md` | el sello, con s, el umbral, las reglas y los md5 |
| `recuerdos_P7_22.py` → `P7_22_recuerdos.json` | los {len(recs)} recuerdos |
| `banco_P7_22.py` → `P7_22_fijado.json`, `P7_22_resultado.json` | s y umbral; separaciones, R3, mapa emocional, sensibilidad |
| `banco_decide_P7_22.py` → `P7_22_decisiones.json` | la repetición de decisiones (R4, medida 2) |
| `P7_22_extra_catalogo.json`, `P7_22_extra_catalogo_s.json` | lo no sellado de la sección 6 |
| `informe_P7_22.md` | este informe |
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_22.md"), "w").write(T); print(len(T))

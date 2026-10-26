"""[P7-13] Escribe informe_P7_13.md desde P7_13_F1.json, P7_13_F2.json, P7_13_ganas.json, P7_13_humo.json, P7_13_estado.json y P7_11_vidas.json."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
J = lambda p: json.load(open(os.path.join(AQUI, p))); md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
F1 = J("P7_13_F1.json"); F2 = J("P7_13_F2.json"); GA = J("P7_13_ganas.json"); H = J("P7_13_humo.json"); E = J("P7_13_estado.json"); V = J("P7_11_vidas.json")
K = H.pop("_constantes"); pet = E["peticiones"]; coste = sum(float(p.get("coste_usd") or 0) for p in pet)
G = F2["regalos"]; R2 = F2["resumen"]; PV = F2["pedidos_por_vida"]
em = sum(p["emisiones"] for p in PV.values()); pidiendo = sum(p["pidiendo"] for p in PV.values()); abre = sum(p["abre"] for p in PV.values()); cier = collections.Counter()
for p in PV.values(): cier.update(p["cierra"])
ap3 = [v for v in V.values() if v["brazo"] == "APRENDE" and v["dia"] <= 3]
hv = sorted(H.values(), key=lambda o: (o["dia"], o["slot"]))
oc = lambda k: sum(o["ocasiones"][k] for o in hv)
dm = [o["ocasiones"]["d_regalar_menos_la_mejor_otra"] for o in hv if o["ocasiones"]["d_regalar_menos_la_mejor_otra"]["n"]]
W = []; w = W.append
w(f"""# P7-13 · Pedir y dejar de pedir

*4-oct-2026. Diseño de Manel (4-oct). Coste: **créditos de la plataforma {n(coste, 4)} USD** (el humo: 3 partidas); **consola de Anthropic 0 USD**.
Acumulado del siete en la plataforma: {n(15.7463 + coste, 4)} USD. Saldos: no consultados. `motor/model.py` = `{md5('motor/model.py')}` al empezar y al
acabar; el cuerpo y los congelados no se tocan: todo en archivos `_P7`, enganchado desde fuera. Una vida por proceso en los bancos; la memoria
viaja solo en el cuaderno. Los números de método son los de la mesa: ninguno se ha cambiado.*

## Lo que sale, en corto

1. **El pedido funciona como pieza**: viaja en el parte (cabe: el parte más largo visto mide {max(max(p['largo_max'] or 0 for p in PV.values()), max(o['largo_max'] for o in hv))} caracteres de 120), se abre y se cierra solo, y F1 pasa.
2. **En banco (F2), de los 171 regalos de APRENDE en P7-10 quedarían {R2['la_replica_sigue_regalando']}**: el hermano pedía en {R2['el_hermano_pedia']}. El círculo se corta.
3. **En el humo (F3), cero regalos en las 6 vidas**, con {n(oc('hermano_pide_y_llevo_1_o_mas'))} tics en que el hermano pedía y el otro llevaba un botiquín: llevaba uno solo (nunca dos) y
   regalar el único perdió siempre (en ningún tic estuvo por delante). Un pedido estuvo abierto un tercio de la vida sin que nadie lo atendiera.
   No es un fallo de la pieza: es lo que el cuerpo ya hacía con su último botiquín. Pero el humo no ha visto ni un regalo con pedido.
4. **Tres días no bastan para ver el círculo**: en P7-10, los días 1 a 3 de APRENDE dieron {sum(v['regala_n'] for v in ap3)} regalos en {len(ap3)} vidas; los 171 llegan después.
5. **Un hallazgo fuera del encargo, importante: todo el campo del siete se ha jugado con los ojos compartidos apagados** (sección 7).

## Sección 1 · La pieza (J): cómo quedó

Archivo nuevo `pide_P7.py`; política `policy_pareja_P7_13.py` (la del siete más `pide_P7.aplica`, después de `descubre_P7.aplica`); imagen
`Dockerfile.pareja_P7_13`. Interruptor `GEMV_P7_PIDE`, 0 por defecto (apagado en F1), 1 en la imagen del humo.

| punto del diseño | cómo está hecho | dónde |
|---|---|---|
| 1 · pedir es un estado que viaja en el parte | el parte E1 gana al final un campo ` q<letra>` mientras la criatura pide (la letra de la clase se lee del catálogo del mundo, no se cablea); cuando deja de pedir, el parte siguiente va sin el campo. Ningún mensaje nuevo: es el parte de cada {K['CADA']} tics. Se envuelven `parte.emite` y `parte.parsea` | `pide_P7.py` (`_emite`, `_parsea`); los llaman `policy_cortex.py:966` y `appraisal_zs_v42_exp.py:578` |
| cabe en 120 | el parte más largo: {max(p['largo_max'] or 0 for p in PV.values())} caracteres en los {n(em)} partes del banco, {max(o['largo_max'] for o in hv)} en los {n(sum(o['partes'] for o in hv))} del humo; el campo añade 3. Si no cupiera, el parte sale sin el campo y se apunta | `pide_P7.py`, `parte.ascii_limpio` |
| 2 · cuándo pide | no lleva botiquín, no ve ninguno en el suelo, y la promesa del botiquín es mayor que cero. La promesa es `decisor_zs._promesa` (decisor_zs.py:620-683; botiquín, :643-656): lo que baja R-ACOPIO al imaginarlo en el zurrón, con el k de las ganas de la criatura (`descubre_P7.py:332`, creencia y esperanza) más lo que le alivia la curiosidad (`descubre_P7.py:346-355`). Es el mismo número que hoy enciende las ganas de ir a por él (`_mejor_objeto`, decisor_zs.py:698-699). Ningún umbral nuevo | `pide_P7.pide` |
| 3 · el regalo mira el pedido | con un botiquín en el suelo de la foto, las filas que regalan (S-DANO-PAREJA, S-HERIDO, R-HERMANO-FALTA, S-PROVISION: `descubre_P7.FILAS_REGALO`) solo cuentan lo que ese botiquín les alivia si el último parte fresco del hermano (caducidad {K['CADUCIDAD']} tics, la del cinco) lleva el pedido; sin pedido valen lo que valdrían sin el botiquín en el suelo. Se evalúa en cada decisión: si el pedido desaparece, el regalo pierde su razón | `pide_P7.py` (`_filas`, `hermano_pide`) |
| 4 · igual en los cuatro brazos | la pieza no mira el brazo; en TECHO actúa igual (la pieza G no, por eso J va aparte) | `pide_P7.aplica` |
| 7 · solo el botiquín | el pedido solo existe para `mundo.id_botiquin`; las flechas, después | `pide_P7.py` |

**Dos decisiones mías dentro del diseño, declaradas:** «no lo ve a su alcance» lo he leído como «no hay ningún botiquín en lo que ve»
(`obs.visible.items`), sin distancia; y la promesa incluye la parte de la curiosidad, porque es lo que hoy enciende el ir a por él.

## Sección 2 · ¿Las ganas de APRENDE son las de TECHO con la misma creencia? (punto 5; nada cambiado)

`ganas_P7_13.py` → `P7_13_ganas.json`: se llama a `descubre_P7.k_ganas` con un cuaderno de pega cuya creencia es la cura del catálogo ({n(GA['TECHO']['cura_catalogo'])}) y se barre la ignorancia.

| | ignorancia | k de las ganas | R-ACOPIO sin botiquín (`ACOPIO_M`) | R-ACOPIO «con una no basta» | `W_TARGET` | peso del botiquín en W | cura imaginada al usar |
|---|---:|---:|---:|---:|---:|---:|---:|
""")
for nom in ("TECHO", "APRENDE"):
    for f in GA[nom]["filas"]: w(f"| {nom} | {n(f['ignorancia'], 2)} | {n(f['k_ganas'], 3)} | {n(f['ACOPIO_M'], 4)} | {n(f['ACOPIO_POR_DOS'], 4)} | {n(f['W_TARGET'], 3)} | {n(f['peso_del_botiquin_en_W'], 3)} | {n(f['cura_imaginada_al_usar'], 1)} |\n")
f05 = next(f for f in GA["APRENDE"]["filas"] if f["ignorancia"] == 0.05)
w(f"""
**Solo son iguales con ignorancia 0.** `W_TARGET` es {n(GA['TECHO']['W_TARGET0'], 1)} en TECHO (`appraisal_zs_v42_exp.py:126`) y 2 + k en APRENDE (`descubre_P7.py:332`); el
peso de R-ACOPIO es {n(GA['TECHO']['ACOPIO_M0'], 2)} en TECHO (`appraisal:111`) y {n(GA['TECHO']['ACOPIO_M0'], 2)} × k en APRENDE (`descubre_P7.py:332`), con
k = `mezcla` / cura = ((1 − ignorancia) × creencia + ignorancia × esperanza) / cura (`descubre_P7.py:107-118`). Con creencia = cura, k = 1 − ignorancia × (1 − {n(GA['TECHO']['esperanza'])} / {n(GA['TECHO']['cura_catalogo'])}):
con la ignorancia del día 20 de P7-10 (0,05), k = {n(f05['k_ganas'], 3)}, `W_TARGET` {n(f05['W_TARGET'], 3)} y R-ACOPIO {n(f05['ACOPIO_M'], 4)}. La esperanza tira hacia abajo: lo poco que aún ignora lo imagina como una ración.
Dos cosas más separan a los dos brazos aunque k fuera 1: APRENDE tiene además la fila R-CURIOSIDAD, su promesa y el candidato `ir_curioso`
(`descubre_P7.py:277`, `:286-306`, `:337-338`, `:346-355`), que TECHO no tiene; y la creencia nunca llega a la cura, porque el recuerdo neutro del
cuaderno (peso 1, efecto 0, `cuaderno_P7.py`) la deja en cura × (1 − ignorancia) como mucho: el descuento por ignorancia entra dos veces.

**Arreglo que propongo, sin aplicar** (decide la mesa): que la mezcla use la creencia SIN el neutro (la media de lo vivido) y deje al neutro solo en
la ignorancia. Así, con todo lo vivido igual a la cura, el efecto imaginado sería (1 − ign) × cura + ign × esperanza: un solo descuento, que
tiende a la cura y a las ganas de TECHO cuando la ignorancia tiende a 0. La curiosidad es otra pregunta (si un cuerpo que ya sabe debe seguir yendo).

## Sección 3 · El brazo SUELO se llama ESPERANZA (punto 6)

`descubre_P7.entorno()` devuelve ahora `ESPERANZA` para el brazo sin cuaderno ni curiosidad (`descubre_P7.py:65` y cabecera); la imagen nueva
(`Dockerfile.pareja_P7_13`) usa ese nombre; `banco_P7_5.BRAZOS` tiene `ESPERANZA` y conserva `SUELO` como nombre viejo, porque las carpetas de
los diarios de P7-10 (`P710_…_SUELO_…`) y sus informes ya escritos no se renombran. No se ha jugado ningún suelo nuevo. `descubre_P7.py` cambia
solo en esa etiqueta y su comentario (md5 de hoy `{md5('cantera/paper7/descubre_P7.py')}`).

## Sección 4 · F1: apagado y TECHO reproducen A4

`banco_P7_13.py --f1` → `P7_13_F1.json`: los 80 diarios de A4, un subproceso por vida, con la política de P7-13 y el pedido apagado.

| brazo | tics iguales | distintos | pedir |
|---|---:|---:|---|
""")
for b in ("apagado", "TECHO"): w(f"| {b} | {n(F1[b]['fidelidad'].get('igual'))} | {n(F1[b]['fidelidad'].get('difiere', 0))} ({'; '.join(d['vida'][-14:] + ' t ' + str(d['t']) for d in F1[b]['desacuerdos'])}) | {F1[b]['hecho_J']} |\n")
gp = collections.Counter((g["hermano_pide"], g["sigue_regalando"]) for g in G)
w(f"""
Los mismos dos tics de siempre. **F1 pasa.**

## Sección 5 · F2: los 171 regalos de APRENDE en P7-10, con pedido

`banco_P7_13.py --f2` → `P7_13_F2.json`. Dos pases de réplica sobre las {len(PV) // 2} partidas con algún regalo ({len(PV)} vidas). Pase 1: cada vida con el
pedido encendido, para saber qué parte habría emitido cada criatura. Pase 2: la vida de quien regaló, oyendo los partes del hermano con su
pedido ({n(R2['partes_del_hermano_con_pedido_oidos'])} partes cambiados); en cada tic en que el campo regaló, si el último parte fresco del hermano pedía y qué elige la réplica.

| | |
|---|---:|
| regalos del campo | {R2['regalos']} |
| el hermano pedía en ese tic | **{R2['el_hermano_pedia']}** |
| la réplica sigue regalando | **{R2['la_replica_sigue_regalando']}** |
| … con pedido | {gp[(True, True)]} |
| … sin pedido | {gp[(False, True)]} |
| regalos nuevos en otros tics | {R2['regalos_nuevos_en_otros_tics']} |
| lo que elige la réplica donde el campo regaló | {", ".join(f"`{k}` {c}" for k, c in collections.Counter(g['elegido_replica'] for g in G).most_common(4))} |

**De 171 seguirían ocurriendo {R2['la_replica_sigue_regalando']}.** En {gp[(False, False)]} el hermano no pedía y la réplica no regala. Los {gp[(False, True)]} que se regalan sin pedido son empates: sin
nada que ganar, la d de regalar es la de `noop`, y el desempate de la casa no deja ganar a `noop` (lo visto en P7-11 con SUELO); esos {gp[(False, True)]} seguirían hasta que la mesa decida sobre ese desempate.
Por qué el hermano casi nunca pedía, en los {n(em)} partes del pase 1: llevaba botiquín en {n(100 * (1 - (pidiendo + sum(1 for _ in [])) / em) if False else None)}""".replace("llevaba botiquín en –", "pedía en") + f""" {n(pidiendo)} ({n(100 * pidiendo / em, 1)} %); abrió {abre} pedidos y se cerraron {sum(cier.values())}: {", ".join(f"«{k}» {c}" for k, c in cier.most_common())}.
En {sum(1 for g in G if not g['hermano_pide'] and g['parte_b'] == 0)} de los regalos sin pedido el parte del hermano decía b0: no llevaba botiquín, pero veía uno o no le aliviaba tenerlo.

Dos avisos de banco. La réplica sigue el diario: después de la primera decisión distinta, lo que ve la criatura es lo que pasó en el campo, no
lo que habría pasado (fidelidad del pase 2: {n(F2['fidelidad_pase2']['igual'])} tics iguales, {n(F2['fidelidad_pase2']['difiere'])} distintos). Y los distintos no son solo regalos: sin pedido,
un botiquín en el suelo junto al hermano deja de aliviar, y la réplica lo coge donde el campo lo dejaba estar (`noop` → `coger` es el desacuerdo más frecuente).

## Sección 6 · F3: el humo de 3 días (APRENDE, pedir encendido)

Semillas nuevas, declaradas antes de jugar en el commit `17ac0f2` (`semillas_P7_13.json`: k = 109, 110, 111 de la sucesión 20260916 + k × 104729;
P7-10 usó k = 89 a 108): {", ".join(str(p['semilla']) for p in pet)}. Una serie, tres días encadenados (el cuaderno viaja horneado en la imagen del día siguiente),
roster lento v2, mundo 0.1.19, como P7-10. Imágenes {", ".join(E['imagenes'][k]['etiqueta'].split(':')[1] for k in sorted(E['imagenes']))}. Diarios en `paintball/runs/P713_*` (fuera de git). Lectura: `analiza_P7_13.py` → `P7_13_humo.json`.
Los seis diarios dicen brazo APRENDE y pedir encendido; 0 errores de las piezas del siete.

| día | asiento | partes | con pedido | pedidos abiertos | cerrados (por qué) | regalos (con pedido / sin) | recogidos por el hermano | vueltos a coger por él mismo | botiquines cogidos | usos | tics yendo a por botiquines (de la vida) | puesto |
|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---|---:|
""")
for o in hv:
    cc = collections.Counter(c["motivo"] for c in o["cierres"]); g = o["regalos"]
    w(f"| {o['dia']} | {o['slot']} | {o['partes']} | {o['partes_con_pedido']} | {o['pedidos_abiertos']} | {o['pedidos_cerrados']} ({', '.join(f'«{k}» {c}' for k, c in cc.items()) or '–'}){' · 1 abierto al final' if o['abierto_al_final'] else ''} | {o['regalos_n']} ({o['regalos_con_pedido']} / {o['regalos_n'] - o['regalos_con_pedido']}) | {sum(1 for x in g if x['destino'] == 'lo recoge el hermano')} | {sum(1 for x in g if x['destino'] == 'lo recoge el mismo')} | {o['coge_botiquines']} | {o['usos']} | {n(o['tics_yendo_a_por_botiquin'])} ({n(100 * o['tics_yendo_a_por_botiquin'] / o['tics'], 1)} %) | {o['puesto']} |\n")
tot_ab = sum(o["pedidos_abiertos"] for o in hv); tot_ce = sum(o["pedidos_cerrados"] for o in hv); mot = collections.Counter(c["motivo"] for o in hv for c in o["cierres"]); dados = sum(1 for o in hv for c in o["cierres"] if c["lo_habia_soltado_el_hermano"])
w(f"""
**Pedidos.** {tot_ab} abiertos, {tot_ce} cerrados, {sum(1 for o in hv if o['abierto_al_final'])} abiertos al acabar la vida. Todos los cierres son «{mot.most_common(1)[0][0]}» ({mot.most_common(1)[0][1]} de {tot_ce}): la criatura dejó de pedir porque
vio un botiquín en el suelo. Ninguno se cerró porque el hermano se lo diera ({dados} botiquines cogidos tras un cierre eran del hermano). El campo ` q` va en
{sum(o['voz_con_campo'] for o in hv)} de los {n(sum(o['partes_voz'] for o in hv))} partes emitidos; el más largo mide {max(o['largo_max'] for o in hv)} caracteres.

**Regalos: {sum(o['regalos_n'] for o in hv)} en las 6 vidas.** No por falta de ocasión:

| día | asiento | tics con el hermano pidiendo | … y yo con 1 botiquín o más | … y yo con 2 o más | … y el candidato de regalar existe | regalar elegido | d de regalar menos la del mejor otro candidato: mínima (mediana) |
|---:|---:|---:|---:|---:|---:|---:|---|
""")
for o in hv:
    c = o["ocasiones"]; d = c["d_regalar_menos_la_mejor_otra"]
    w(f"| {o['dia']} | {o['slot']} | {n(c['hermano_pide'])} | {n(c['hermano_pide_y_llevo_1_o_mas'])} | {c['hermano_pide_y_llevo_2_o_mas']} | {n(c['hermano_pide_y_candidato_de_regalar'])} | {c['elegido_regalar']} | {(n(d['min'], 3) + ' (' + n(d['mediana'], 3) + ')') if d['n'] else '–'} |\n")
w(f"""
En {n(oc('hermano_pide_y_candidato_de_regalar'))} tics el hermano pedía, quien podía dar llevaba botiquín y el candidato de regalar estaba sobre la mesa; regalar no ganó en ninguno
(la d de regalar quedó siempre por encima de la del mejor otro candidato: la más cerca, {n(min(x['min'] for x in dm), 3)}). En todos llevaba **un solo botiquín**
(con dos o más: {oc('hermano_pide_y_llevo_2_o_mas')} tics). El cuerpo congelado le cobra un coste propio a la foto que da su última venda («dar de lo que te falta», `appraisal_zs_v42_exp.py:968-984`);
en el humo ese coste ganó siempre. El pedido no cambia eso ni tenía que cambiarlo. El asiento 10 llevó un botiquín casi toda la vida
los tres días y el asiento 11 pidió entre {min(o['partes_con_pedido'] for o in hv if o['slot'] == 11)} y {max(o['partes_con_pedido'] for o in hv if o['slot'] == 11)} partes por día (un tercio de sus partes) sin recibir nada.

**Lo que el humo dice y lo que no.**
- Dice: la pieza corre en el campo sin errores, el pedido se abre, viaja y se cierra, y no hay ningún regalo sin pedido ({sum(o['regalos_n'] - o['regalos_con_pedido'] for o in hv)}).
- No dice si el círculo se corta: no ha habido ni un regalo, tampoco con pedido. En P7-10, los días 1 a 3 de APRENDE ({len(ap3)} vidas) dieron {sum(v['regala_n'] for v in ap3)} regalos en {sum(1 for v in ap3 if v['regala_n'])} vidas
  y {n(100 * st.mean(v['contadores'].get('tics ir a por un botiquin', 0) / v['contadores']['tics'] for v in ap3), 1)} % de la vida yendo a por botiquines; el humo, {sum(o['regalos_n'] for o in hv)} regalos y {n(100 * st.mean(o['tics_yendo_a_por_botiquin'] / o['tics'] for o in hv), 1)} %. Con 6 vidas y esa tasa de base, cero regalos no distingue nada.
  Los 171 regalos de P7-10 llegan casi todos después del día 3; un humo de tres días no llega ahí.
- Deja una pregunta para la mesa: un pedido puede pasarse un tercio de la vida abierto con el hermano al lado y con un botiquín. Si eso es lo
  querido (nadie da su último botiquín) o si pedir debería pesar más que tener de sobra, no lo decide el taller.
- Puestos de las 6 vidas: {", ".join(str(o['puesto']) for o in hv)}. Son 3 partidas: no se lee nada de ahí.

**Paradas.** Hacia las 17:45 hubo un corte de luz: la cadena murió esperando el día 3 (error de DNS), con el día 3 ya pedido a las 17:43. No se ha
vuelto a jugar nada: al volver la red se recogió esa misma partida (`lanza_P7_13.py --recoge`). Disco: 14,4 GB libres al empezar, 14,1 al acabar.

## Sección 7 · Fuera del encargo: el campo del siete se juega con los ojos apagados

Al montar el banco vi que la réplica emitía el parte E2 (el de los ojos compartidos del seis) y el campo del siete el E1. Mirado en los diarios
(`arranque`, `ojos_resumen` y el primer parte de cada uno):

| diarios | `GEMV_OJOS` | parte | tics con lo del hermano inyectado |
|---|---|---|---|
| A4 del seis (P6-11, P6-24): el cuerpo que F1 reproduce | 1 | E2, cada 25 tics | miles por vida (6.871 y 7.930 en los dos mirados) |
| campo del siete (P7-5, P7-9, P7-10; y el humo de hoy) | **0** | E1, cada 48 tics | 0 |

`Dockerfile.pareja11` trae `GEMV_OJOS=0` por defecto (`:145`) y las imágenes del siete lo heredaron; los diarios de A4 del seis lo llevan encendido.
**Todas las partidas del siete se han jugado sin ojos compartidos: no es el A4 del seis, es A4 con los ojos apagados.** Ningún informe del siete lo
declara. F1 no lo ve porque replica diarios de A4 con su propio ajuste. Los bancos de P7-11 corrieron con los ojos encendidos sobre diarios jugados
sin ellos; reprodujeron el campo casi entero porque sin partes E2 que oír esa pieza no hace nada. He jugado el humo como P7-10 (ojos apagados) para
que sea comparable. Si se encienden, el pedido hay que llevarlo también al parte E2 (`parte2.py`), que se llena hasta los 120 caracteres: el campo
tendría que ir en la cabeza, antes de los rivales y los recursos. No lo he hecho. **Qué cuerpo es el del siete lo decide Manel.**

## Sección 8 · F4: créditos

| día | semilla | créditos |
|---:|---|---:|
""" + "".join(f"| {p['dia']} | {p['semilla']} | {n(p['coste_usd'], 4)} USD |\n" for p in pet) + f"""
Créditos de la plataforma: **{n(coste, 4)} USD** en {len(pet)} partidas (el día 2 costó menos de la mitad que los otros dos; no sé por qué: las dos criaturas vivieron la partida entera).
{len(E['imagenes'])} imágenes subidas más una de prueba (v50), sin créditos. Consola de Anthropic: **0 USD**. Acumulado del siete en la plataforma: {n(15.7463 + coste, 4)} USD. Saldos: no consultados.

## Sección 9 · Lo que queda para la mesa

1. Qué cuerpo juega el siete: con ojos o sin ellos (sección 7). Afecta a todo lo jugado y a dónde va el pedido.
2. El pedido corta el círculo en banco (171 → {R2['la_replica_sigue_regalando']}), pero el humo no lo ha puesto a prueba: haría falta un campo más largo, o empezar con cuadernos ya avanzados.
3. El último botiquín no se regala aunque el hermano pida ({n(oc('hermano_pide_y_candidato_de_regalar'))} tics de ocasión, 0 regalos).
4. Los {gp[(False, True)]} regalos en empate con `noop` siguen ahí (el desempate no deja ganar a `noop`).
5. Las ganas de APRENDE no llegan a las de TECHO por el doble descuento de la ignorancia (sección 2; arreglo propuesto, sin aplicar).
6. «A su alcance» lo he leído como «a la vista»: si la mesa quiere una distancia, es un número suyo.

## Archivos

| archivo | qué es |
|---|---|
| `pide_P7.py`, `policy_pareja_P7_13.py`, `Dockerfile.pareja_P7_13` | la pieza J, la política y la imagen |
| `descubre_P7.py`, `banco_P7_5.py` | el brazo SUELO pasa a ESPERANZA (solo la etiqueta) |
| `banco_P7_13.py` → `P7_13_F1.json`, `P7_13_F2.json` | F1 y F2 |
| `ganas_P7_13.py` → `P7_13_ganas.json` | la comprobación del punto 5 |
| `lanza_P7_13.py`, `semillas_P7_13.json`, `P7_13_estado.json`, `P7_13_res/`, `cuadernos_P7_13/` | el humo |
| `analiza_P7_13.py` → `P7_13_humo.json` | la lectura del humo |
| `escribe_informe_P7_13.py`, `informe_P7_13.md` | este informe |
""")
txt = "".join(W); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_13.md"), "w").write(txt); print("informe escrito", len(txt))

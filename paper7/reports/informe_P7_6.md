# P7-6 · La curiosidad hecha de ignorancia, y poder hacer sitio

*3-oct-2026. Coste: **créditos de la plataforma** 0,1930 USD en 3 partidas (por día: 1: 0,0569, 2: 0,0279, 3: 0,1082); **consola de Anthropic 0 USD**.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; congelados y cuerpo sin tocar: todo en archivos `_P7`. Una vida por
proceso; la memoria viaja solo en el cuaderno. Los números de método son los de la mesa; cuando uno no funciona se informa, no se cambia.*

## Sección 1 · Los dos cambios, en el código

**Cambio 1, la curiosidad como carencia de conocimiento** (`cuaderno_P7.py`, `descubre_P7.py`). Ignorancia de una clase = peso del neutro /
(peso del neutro + suma de los pesos de los recuerdos vividos de esa clase en todas sus situaciones, vistos desde el día actual):
`Cuaderno.ignorancia`; nunca probado 1, recién probado baja, con días sin vivirlo sube despacio porque los vividos se apagan con 0,95 y el
neutro no. Desaparecen la cuenta de usos, la forma de la novedad de P7-5 y la pendiente topada tras aquel humo. La fila **R-CURIOSIDAD**
es una carencia como las demás: negativa, reparto como R-ACOPIO (0,1, 0,8, 0,1), M = 0,18 × calma × ignorancia × alivio, con calma = 1 − máx
(alcance, agresor, hermano amenaza, hermano golpe, anticipación del fuego) y alivio = 1 sin la cosa (estar al lado no alivia nada), 0,5 con
la cosa en el zurrón, 0 en la foto que la usa. Entra en el envoltorio de `A.filas` y en `A.REPARTO` desde fuera; la promesa de ir a por la
cosa (`D._promesa`) suma M × 0,5, lo que alivia tenerla.

**Cambio 2, hacer sitio** (`descubre_P7.py`, pieza E). Candidato compuesto `hacer_sitio_<suelta>_por_<coge>`, creado en el envoltorio de
`D.candidatos` cuando hay un objeto en mi casilla que `coger` no puede tomar (zurrón lleno y sin pila donde apilarlo) y llevo un consumible de
otra clase. Es un `soltar` del decisor (ranura fuera, el objeto al suelo, acción `drop`) cuya receta lleva en `item` el marcador
`suelta|coge`; el envoltorio de `D._obs_prevista` lo reconoce y pone además en la foto el objeto cogido en el zurrón: lo que se pierde
contra lo que se gana, en la misma imaginación. Al elegirlo se borra la cesión que `decide` apunta en `mem.cedidos` (decisor_zs.py:902-903),
para que `coger` pueda tomar el objeto al tic siguiente. Interruptor `GEMV_P7_SITIO`, igual en los cuatro brazos, apagado en F1.

**Un ajuste de la pieza C, encontrado en F2 y declarado.** Las ganas del botiquín son toda la fila R-ACOPIO, también su rama "con una sola
no basta" (`ACOPIO_POR_DOS`, appraisal:221, :951-953), que P7-5 no escalaba por la creencia. Sin escalarla, al coger el primer botiquín
aparecía un acopio de 0,10 que pesaba más que el alivio de la curiosidad (0,09) y `coger` perdía con el zurrón libre (F2, primera corrida:
145 de 773 veces encima con sitio). Escalada por k, como el resto de las ganas, `coger` gana 619 de 773. No se tocó ningún número de la mesa.

## Sección 2 · F1: con todo apagado y con TECHO, la variante reproduce A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
| apagado (hacer sitio apagado) | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |
| TECHO (hacer sitio apagado) | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |

Los mismos dos tics de P6-30 y P7-5. **F1 pasa.** Fuente: `banco_P7_5.py --f1` (`P7_6_F1.json`).

## Sección 3 · F2: las escenas del humo de P7-5 en que el cuerpo se quedó al lado de un botiquín

Réplica de los seis diarios del humo de P7-5 con los dos cambios (brazo APRENDE, cuaderno vacío, un subproceso por vida, `banco_P7_6.py`),
registrando en cada tic a una casilla o menos de un botiquín la elección de la réplica y las d de sus candidatos. El mundo es el del diario:
lo elegido no cambia la partida, pero se ve qué haría. 25.420 escenas:

| situación | coger | hacer sitio (y qué suelta) | ir al objeto | otra |
|---|---:|---:|---:|---:|
| encima del botiquín, con ranura libre | 619 | 0 | 13 | 141 |
| encima, zurrón lleno | 0 | 21 (suelta rations 21) | 0 | 1.235 |
| al lado (una casilla), con ranura libre | 7 | 0 | 41 | 1.158 |
| al lado, zurrón lleno | 0 | 0 | 234 | 21.951 |

Lectura. Encima con ranura libre, `coger` gana 619 de 773. Encima con el zurrón lleno, el candidato de hacer sitio
existió en 23 tics (solo cuando lleva un consumible de otra clase: en el resto el zurrón va de armas y munición, que por diseño no se sueltan) y ganó
en 21, soltando raciones. Al lado del botiquín la curiosidad no mueve por sí sola (estar al lado no alivia nada): `ir al objeto` gana en
275 tics y el resto son `noop` o pasos de otras filas. Fuente: `P7_6_F2.json`.

## Sección 4 · F3: el humo de tres días (brazo APRENDE, las dos criaturas)

Semillas nuevas, nunca usadas: día 1: 26858843, día 2: 26963572, día 3: 27068301 (las tres siguientes de la sucesión de semillas_S2 tras las de P7-5).
Imágenes: día 1: gemv-p7-aprende:v4 (5f2e12a3…), día 2: gemv-p7-aprende:v5 (db830c98…), día 3: gemv-p7-aprende:v6 (fcc6998d…); el cuaderno de cada día viaja horneado al siguiente (el registro de fin ya va antes de la subida).

**Día 1** (semilla 26858843, completed, coste 0,0569 USD de plataforma).

| criatura | vivo · puesto | se acerca (tics con curiosidad > 0 y elección hacia un objeto) | hace sitio (tic, qué suelta) | coge (con sitio libre / tras hacer sitio) | usa (tic, situación, imaginó) | cuaderno leído | cuaderno al acabar: recuerdos, ignorancia, creencias |
|---|---|---:|---|---|---|---|---|
| 10 | 8.246 · 15 | 520 | ninguno | 0 / 0 | ninguno | no (día 0) | 0, –, – |
| 11 | 14.233 · 3 | 379 | ninguno | 0 / 0 | ninguno | no (día 0) | 0, –, – |

**Día 2** (semilla 26963572, completed, coste 0,0279 USD de plataforma).

| criatura | vivo · puesto | se acerca (tics con curiosidad > 0 y elección hacia un objeto) | hace sitio (tic, qué suelta) | coge (con sitio libre / tras hacer sitio) | usa (tic, situación, imaginó) | cuaderno leído | cuaderno al acabar: recuerdos, ignorancia, creencias |
|---|---|---:|---|---|---|---|---|
| 10 | 14.929 · 1 | 575 | ninguno | 0 / 0 | ninguno | sí (día 1) | 0, –, – |
| 11 | 14.929 · 2 | 622 | ninguno | 0 / 0 | ninguno | sí (día 1) | 0, –, – |

**Día 3** (semilla 27068301, completed, coste 0,1082 USD de plataforma).

| criatura | vivo · puesto | se acerca (tics con curiosidad > 0 y elección hacia un objeto) | hace sitio (tic, qué suelta) | coge (con sitio libre / tras hacer sitio) | usa (tic, situación, imaginó) | cuaderno leído | cuaderno al acabar: recuerdos, ignorancia, creencias |
|---|---|---:|---|---|---|---|---|
| 10 | 13.058 · 4 | 435 | ninguno | 0 / 0 | ninguno | sí (día 2) | 0, –, – |
| 11 | 13.151 · 3 | 530 | ninguno | 5 / 0 | 10665 dentro 0,0 | sí (día 2) | 1, 0,475, dentro: cuerpo 0,5, recursos -0,52, vínculo 0,00 |

**Lectura del humo.** Tics encima de un botiquín, por día y asiento (con ranura libre / zurrón lleno con un consumible que soltar / candidato de hacer sitio presente / elegido hacer sitio / elegido coger; zurrón más frecuente): día 1 asiento 10: 0 (0 / 0 / 0 / 0 / 0; –); día 1 asiento 11: 97 (0 / 97 / 0 / 0 / 1; ['rations', 'darts']); día 2 asiento 10: 392 (0 / 0 / 0 / 0 / 0; ['darts', 'blowgun']); día 2 asiento 11: 129 (0 / 129 / 0 / 0 / 0; ['rations', 'bow']); día 3 asiento 10: 22 (0 / 22 / 22 / 0 / 0; ['knives', 'rations', 'bow', 'arrows']); día 3 asiento 11: 121 (121 / 0 / 0 / 0 / 5; [None, None]). Cogidas en los tres días: 5. Usos: día 3 asiento 11, tic 10.665, dentro, vida 99, imaginó 0,0, ignorancia antes 1,000. Huellas: cuerpo +1.0 (la vida ya estaba casi llena), recursos -1, vínculo +0.0, intensidad 1.162; tras ese uso la ignorancia del botiquín pasa de 1 a 0,475 (peso vivido 1,104 contra el neutro 1). **Un fallo de fontanería encontrado en el día 1 y corregido para el día 3, declarado.** El candidato de hacer sitio se creaba solo para el primer objeto de la casilla (`aqui[0]`, el mismo que mira `coger`, decisor_zs.py:478-482); en la cámara los botiquines comparten casilla con pilas de munición que sí caben, así que el día 1 el asiento 11 pasó 97 tics encima de un botiquín con raciones en el zurrón y el candidato no existió; igual el día 2 (asiento 11, 129 tics con raciones y arco). Desde el día 3 el candidato se crea para cada objeto de la casilla que no cabe. En banco, sobre el diario del día 1 (asiento 11, tics 12.500-12.640), con la corrección el candidato aparece en 11 tics y gana en 8. Los días 1 y 2 jugaron sin él. El día 3, con la corrección: el asiento 11 cogió botiquines con el zurrón libre (5 cogidas, encima con ranura libre `coger` ganó 5 de 121 tics) y usó uno; el asiento 10 estuvo 22 tics encima de uno con el zurrón lleno llevando raciones, el candidato de hacer sitio existió los 22 y perdió los 22: soltar la ración cuesta más (su valor en W, carencia) de lo que alivia conocer el botiquín (0,09), tal como lo pesa la mesa; se informa, no se cambia. La curiosidad sí acerca (cientos de elecciones hacia un objeto con la fila encendida) y las criaturas pasan miles de tics a una casilla de un botiquín, casi siempre con el zurrón lleno de armas y munición, que por diseño no se sueltan: ahí no hay sitio que hacer.

GIF de los datos del primer uso (`gif_P7_5.py`, local, fuera de git): `P7_6_dia3_acercamiento_10.gif`, `P7_6_dia3_uso_11.gif`.

## Sección 5 · F4: créditos del humo

Créditos de la plataforma: 0,1930 USD en 3 partidas enteras (por día 0,0569, 0,0279, 0,1082; media 0,0643). Seis subidas de imagen (v1-v6 de `gemv-p7-aprende`, tres de P7-5 y tres de P7-6), sin créditos. Consola de Anthropic: 0.

## Sección 6 · Lo que queda para la mesa

1. El zurrón: la curiosidad y hacer sitio solo pueden actuar cuando lleva un consumible que soltar; con armas y munición en las dos ranuras (lo
   más frecuente en la cámara) no hay sitio que hacer. Si se quiere que la curiosidad pueda probar lo nuevo, hace falta decidir si se
   suelta también munición o un arma sobrante (decisión de diseño).
2. "Estar al lado no alivia nada" deja el último paso en manos de la promesa de `ir_objeto` (M × 0,5); en F2 gana pocas veces frente a
   `noop` al lado del botiquín. Es lo que fija el diseño; se informa.
3. Qué objeto toma `pickup` cuando hay varios en la casilla lo decide el mundo (pregunta para Ari): hacer sitio suelta uno y pide coger,
   pero no elige cuál se recoge.
4. El escalado de `ACOPIO_POR_DOS` por la creencia (sección 1) es una lectura de la pieza C ("las ganas... salen de la creencia"), no un
   número nuevo; queda a la mesa confirmarla.

## Archivos

| archivo | qué es |
|---|---|
| `cuaderno_P7.py`, `descubre_P7.py` | la ignorancia y la curiosidad; hacer sitio; el escalado de `ACOPIO_POR_DOS` |
| `banco_P7_5.py --f1`, `P7_6_F1.json`; `banco_P7_6.py`, `P7_6_F2.json` | F1 y F2 |
| `lanza_P7_6.py`, `Dockerfile.pareja_P7_6`, `P7_6_brazos.json`, `P7_6_dia*_{peticion,resultado,cuaderno_*}.json`, `cuadernos_humo_P7_6/` | el humo |
| `humo_P7_6.py`, `P7_6_humo.json`, `P7_6_diarios_manifiesto.md` | la lectura del humo y el manifiesto de los diarios (fuera de git) |
| `escribe_informe_P7_6.py`, `informe_P7_6.md` | este informe |

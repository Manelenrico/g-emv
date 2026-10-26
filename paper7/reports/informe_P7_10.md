# P7-10 · El primer campo del siete, con la esperanza

*3/4-oct-2026. Coste: **créditos de la plataforma** 14,3122 USD en 160 partidas (SUELO 40: 3,4211, BORRADO 40: 3,6385, APRENDE 40: 3,6620, TECHO 40: 3,5907); **consola de Anthropic 0 USD**.
Total de créditos de P7-10: 14,3122 USD. Acumulado del siete en la plataforma: 15,7463 USD (P7-5 a P7-9: 1,4341).
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; los 202 congelados del cinco y los 32 del seis con su md5; el cuerpo no se toca: todo en
archivos `_P7`. Una vida por proceso; la memoria viaja solo en el cuaderno. Sello antes de jugar: `SELLO_P7_10.md`, commit `2f302a0a96d7`.
Peticiones: {'completed': 160}.*

## Sección 1 · El arreglo: en un empate, hacer sitio no gana

Pieza I de `descubre_P7.py` (`desempate_sin_sitio`, envoltorio de `D.select_tiebreak`, el desempate de la casa que `decide` llama en
decisor_zs.py:895). Si el mínimo de la d terminal lo comparten (empate exacto, ±1e-9) un candidato de hacer sitio y otro que no lo es, o si
el paisaje es degenerado (spread ≤ 1e-3), los de hacer sitio salen del desempate: se queda lo que se tiene. Si hacer sitio gana solo, gana.
Lo medido antes del arreglo (día 2 del freno de P7-9, asiento 10): la vuelta de cada oscilación ración ↔ botiquín era un empate exacto con
`noop` (diferencia 0,0), que `noop` no puede ganar; la ida ganaba de verdad (0,16).

**Banco** (`banco_P7_10.py` → `P7_10_sitio.json`; réplica de los días 1 y 2 de P7-9, asiento 10, con el cuaderno que leyó ese día):

| día | hacer sitio en el campo (oscilaciones) | sin el arreglo: hacer sitio (oscilaciones) | con el arreglo: hacer sitio (oscilaciones) | en los tics donde el campo hizo sitio, con el arreglo |
|---|---|---|---|---|
| 1 | 9 (4) | 9 (4) | 4 (0) | noop 5, hacer sitio 4 |
| 2 | 9 (7) | 9 (7) | 5 (0) | hacer sitio 5, noop 4 |

Las oscilaciones desaparecen (4 → 0, 7 → 0); los hacer-sitio que ganaban por su valor siguen ganando.

## Sección 2 · F1: apagado y TECHO reproducen A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
| apagado | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |
| TECHO | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |

Los mismos dos tics de siempre. **F1 pasa** (`P7_10_F1.json`).

## Sección 3 · El sello y el campo

`SELLO_P7_10.md` (sustituye al de P7-8): md5 de los archivos, las 20 semillas nuevas (k = 89..108, serie 2 en orden inverso) y las seis predicciones
con su medida, en el commit `2f302a0a96d7`, antes de pedir ninguna partida. Imágenes: BORRADO: gemv-p7-campo:v8, SUELO: gemv-p7-campo:v7, TECHO: gemv-p7-campo:v9; APRENDE,
una por serie y día (v10 en adelante), con los cuadernos del día anterior. Lanzador `lanza_P7_10.py` (las dos cadenas de APRENDE y los brazos fijos
en tandas, a la vez, con un cerrojo sobre el estado); lector `campo_P7_10.py` → `P7_10_campo.json`.

## Sección 4 · El freno (APRENDE, serie 1, días 1 a 3)

APRENDE, serie 1, días 1 a 3 (3-oct, 21:44 a 22:24), antes de pedir nada más. Las tres condiciones de la mesa pasaron: (a) el cuaderno viaja y se
lee los días 2 y 3; (b) cero regalos de botiquines con creencia "no sé" (día 3: 2 regalos, con creencia 26,4); (c) el asiento 10 pasa de "no sé" a
creencia 29,3 e ignorancia 0,223. Al leerlo se vio un fallo de fontanería (con el canal abierto, el cuerpo regaló la pila de botiquines y la ventana
apuntó dos "cura 0, firme"); el arreglo y el cuaderno rehecho del día 3 del asiento 11 están en el apéndice de `SELLO_P7_10.md` (commit `4fb3c63`),
escrito antes de las 157 partidas restantes. Las predicciones no cambiaron.

## Sección 5 · El campo: lo que se mide

**Lo jugado.** 160 partidas de 160, todas `completed`; 320 vidas leídas de 320 (`P7_10_campo.json`). El cuaderno de APRENDE se leyó al arrancar
en todas las vidas de los días 2 a 20 (0 fallos). Oscilaciones de hacer sitio: 0 en los cuatro brazos (el arreglo de la sección 1 aguanta en el campo).

**La noche (paradas, con su hora).**

| cuándo | qué | espacio libre |
|---|---|---:|
| 3-oct, 22:48 | parada por disco lleno (29 partidas pedidas, recogidas después; commit `6b98cc8`) | 0 GB |
| 4-oct, 00:27 | reanudación: Docker limpio (Manel borró `Docker.raw`, 21 GB); cadenas de APRENDE (serie 1 desde el día 5, serie 2 desde el día 2) y tandas de fijos | 26,91 GB |
| 4-oct, 02:19 | última tanda de fijos acabada | – |
| 4-oct, 04:30 | cadena de APRENDE de la serie 1 acabada (día 20) | – |
| 4-oct, 05:03 | corte de luz: sin red; la cadena de la serie 2 cae con error de DNS, con el día 20 ya pedido (04:59) | 14,80 GB |
| 4-oct, 05:13 | vuelve la red; día 20 de la serie 2 recogido; 160 de 160 | 14,87 GB |

Ninguna parada por disco en la reanudación (guarda en 5 GB; mínimo visto 14,80 GB). Tras cada horneado: `docker builder prune -af`,
`docker image prune -f` y fuera las imágenes de APRENDE de días anteriores de esa serie; la del día en juego no se tocó. Ningún .zip borrado.
Un resto del disco lleno del día 3: el diario del asiento 10 de SUELO, serie 1, día 1 había quedado vacío (0 bytes) y el del asiento 11 no se
había bajado; el primero se rehízo desde su .zip y el segundo se bajó de nuevo. Los 320 diarios coinciden en tamaño con su .zip.
El lanzador cambió dos veces después del sello (guarda de disco y limpieza de Docker; nada de lo que se juega): su md5 ya no es el del sello.

**Por brazo** (80 vidas cada uno; un uso = botiquín gastado):

| brazo | botiquines cogidos | regalados | usos | canales interrumpidos | mediana de la vida al usar | usos con vida < 50 | usos con vida ≥ 80 | hacer sitio | muere por anillo / rival / sobrevive | partidas ganadas (vidas en el puesto 1) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| SUELO | 123 | 24 | 70 | 78 | 85 | 5 | 50 | 12 | 41 / 14 / 25 | 13 |
| BORRADO | 143 | 21 | 94 | 105 | 86 | 12 | 61 | 22 | 32 / 22 / 26 | 8 |
| APRENDE | 297 | 171 | 89 | 169 | 69 | 20 | 25 | 18 | 36 / 28 / 16 | 7 |
| TECHO | 168 | 69 | 61 | 121 | 63 | 16 | 16 | 12 | 42 / 13 / 25 | 14 |

**Mediana de la vida al usar, por tramos de días** (entre paréntesis, usos):

| brazo | días 1-5 | días 6-10 | días 11-15 | días 16-20 |
|---|---:|---:|---:|---:|
| SUELO | 85 (21) | 83,5 (18) | 86 (20) | 83 (11) |
| BORRADO | 78 (23) | 89 (27) | 88,5 (24) | 86 (20) |
| APRENDE | 68 (27) | 71 (21) | 73 (24) | 67 (17) |
| TECHO | 63 (11) | 76 (7) | 60 (17) | 63 (26) |

**El cuaderno de APRENDE** (creencia del botiquín, cuerpo, dentro del círculo; "–" = "no sé"):

| criatura | creencia al fin de los días 1 / 5 / 10 / 15 / 20 | ignorancia 1 / 5 / 10 / 15 / 20 | recuerdos al final (firmes) |
|---|---|---|---:|
| serie 1, asiento 10 | – / 34,3 / 40,9 / 41,2 / 41,8 | – / 0,094 / 0,069 / 0,057 / 0,046 | 25 (8) |
| serie 1, asiento 11 | 31,0 / 33,2 / 32,0 / 36,3 / 34,0 | 0,162 / 0,112 / 0,088 / 0,074 / 0,061 | 20 (3) |
| serie 2, asiento 10 | – / 35,8 / 41,0 / 41,8 / 42,4 | – / 0,109 / 0,064 / 0,050 / 0,055 | 22 (6) |
| serie 2, asiento 11 | 4,1 / 12,9 / 28,9 / 36,5 / 38,3 | 0,326 / 0,163 / 0,095 / 0,054 / 0,055 | 22 (3) |

Figuras: `P7_10_fig_vida_al_usar.png`, `P7_10_fig_creencia.png`, `P7_10_fig_ignorancia.png`, `P7_10_fig_usos.png`.

## Sección 6 · El sello, cifra a cifra

Evaluado una sola vez, al final, con `sello_P7_10.py` sobre las 320 vidas (`P7_10_sello_resultado.json`). **Dos de seis: pasan P2 y P3; fallan P1, P4, P5 y P6.**

| predicción | medida | resultado |
|---|---|---|
| **P1. Aprende a esperar** (mediana de la vida al usar, días 16-20 < días 1-5, en ≥ 3 de 4 criaturas) | serie 1 asiento 10: 63 → 66 (8 y 7 usos); serie 1 asiento 11: 66 → 73 (7 y 5); serie 2 asiento 10: 86 → 58,5 (7 y 2); serie 2 asiento 11: 89 → 61 (5 y 3) | 2 de 4: **falla** |
| **P2. Lo hace por lo que recuerda** (días 11-20, APRENDE < BORRADO) | APRENDE 69 (41 usos), BORRADO 87,5 (44 usos) | **pasa** |
| **P3. La creencia sube** (día 20 > día 5, en ≥ 3 de 4) | 34,3 → 41,8; 33,2 → 34,0; 35,8 → 42,4; 12,9 → 38,3 | 4 de 4: **pasa** |
| **P4. Pero se queda corta** (creencia final < 40, en ≥ 3 de 4) | 41,8; 34,0; 42,4; 38,3 | 2 de 4: **falla** (dos criaturas pasan de 40) |
| **P5.** SUELO ≤ 0,1 usos por vida; y TECHO usa con menos vida que APRENDE en los días 1-5 | SUELO: 0,875 usos por vida (70 en 80 vidas); TECHO 63, APRENDE 68 | la mitad de SUELO **falla**, la de TECHO pasa: **falla** |
| **P6.** Vida al morir y puesto iguales entre brazos (|d̄| ≤ 2·se, 80 pares, las dos medidas, los seis pares) | fuera de 2·se: BORRADO − APRENDE (vida al morir +5,06, se 2,33; puesto −1,25, se 0,61) y APRENDE − TECHO (vida −4,56, se 2,05; puesto +1,55, se 0,57); los otros cuatro pares, dentro | **falla** |

Medias de P6: vida al morir SUELO 10,6, BORRADO 11,5, APRENDE 6,4, TECHO 11,0; puesto SUELO 4,70, BORRADO 4,66, APRENDE 5,91, TECHO 4,36.
APRENDE acaba peor que BORRADO y que TECHO en las dos medidas; frente a SUELO la diferencia va en el mismo sentido y queda dentro de 2·se
(vida +4,15, se 2,31; puesto −1,21, se 0,62).

## Sección 7 · Créditos

Créditos de la plataforma: 14,3122 USD en 160 partidas enteras (SUELO: 40 partidas, 3,4211 USD, BORRADO: 40 partidas, 3,6385 USD, APRENDE: 40 partidas, 3,6620 USD, TECHO: 40 partidas, 3,5907 USD; media por partida 0,0895). Subidas de imagen: 43, sin créditos. Consola de Anthropic: 0 USD. Acumulado del siete en la plataforma: 15,7463 USD.

## Sección 8 · Lo que queda para la mesa

Lo que el campo deja sobre la mesa, sin decidir nada (las decisiones son de Manel):

1. **P2 pasa, pero no por la razón de P1.** APRENDE usa con menos vida que BORRADO (69 frente a 87,5), pero ya lo hace en los días 1-5 (68 frente a 78) y
   su mediana no baja con los días (68, 71, 73, 67). En la serie 1 no baja en ninguna de las dos criaturas; en la serie 2 baja en las dos, con 2 y 3 usos
   en el tramo final. La diferencia con BORRADO aparece pronto y no crece: "aprende a esperar a lo largo de 20 días" no se ve.
2. **APRENDE acaba peor** (vida al morir y puesto, fuera de 2·se frente a BORRADO y TECHO; 7 vidas ganadoras frente a 8, 13 y 14). Es el brazo que
   más botiquines coge (297) y más regala (171), y el que más muere a manos de un rival (28 de 80). Si coger y regalar le cuesta posición es una
   pregunta que este campo no contesta: no se midió.
3. **SUELO usa botiquines** (0,875 por vida, con la vida alta: mediana 85). La mesa esperaba casi cero. O el brazo no es lo que la mesa creía, o el
   cuerpo congelado ya los usa sin el siete: hay que mirarlo antes de leer nada contra SUELO.
4. **La creencia pasa de 40 en dos criaturas** (41,8 y 42,4): "se queda corta" falla por poco; las cuatro están entre 34 y 42,4 y casi planas desde el día 10.
5. Fontanería: el lanzador no reintenta si se cae la red (la cadena de la serie 2 murió con el corte de luz de las 05:03; el día 20 ya estaba pedido y no se perdió nada).

## Archivos

| archivo | qué es |
|---|---|
| `descubre_P7.py` (pieza I) | en un empate, hacer sitio no gana |
| `banco_P7_10.py`, `P7_10_sitio.json`; `banco_P7_5.py --f1`, `P7_10_F1.json` | el banco del arreglo y F1 |
| `SELLO_P7_10.md`, `semillas_P7_10.json`, `Dockerfile.pareja_P7_8`, `lanza_P7_10.py`, `P7_10_estado.json`, `P7_10_res/`, `cuadernos_P7_10/` | el campo: sello, semillas, imagen, lanzador, estado, resultados y cuadernos |
| `campo_P7_10.py`, `P7_10_campo.json`, `sello_P7_10.py`, `P7_10_sello_resultado.json`, `figuras_P7_10.py`, `P7_10_fig_*.png`, `P7_10_diarios_manifiesto.md` | lector, evaluador del sello, figuras, manifiesto |
| `escribe_informe_P7_10.py`, `informe_P7_10.md` | este informe |

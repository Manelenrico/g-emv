# P7-8 · El primer campo del siete: el arreglo del regalo, el sello y el freno

*3-oct-2026. Coste: **créditos de la plataforma** 0,3246 USD en 3 partidas (el freno: APRENDE, serie 1, días 1 a 3; por día 0,1092, 0,1066, 0,1088); **consola de Anthropic 0 USD**.
Total de créditos de P7-8: 0,3246 USD. El resto del campo (157 partidas) NO se jugó: el freno paró (sección 5).
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; los 202 congelados del cinco y los 32 del seis con su md5; el cuerpo no se toca: todo en
archivos `_P7`. Una vida por proceso; la memoria viaja solo en el cuaderno. Sello antes de jugar: `SELLO_P7_8.md`, commit `c78ff4db0ffa`.*

## Sección 1 · El arreglo: el regalo mira lo aprendido

**Lo que pagaba el regalo.** En el banco (réplica del día 1 del humo de P7-7, asiento 11, tic 2.200, `_P7_8_tmp/dbg_regalo.py`) la foto de
`soltar_first_aid` con el botiquín desconocido ganaba a `noop` por dos filas: **S-PROVISION** (la hermana sin venda por su parte, appraisal:1312-1362),
que bajaba de 0,30 a 0,045 con el botiquín en el suelo junto a ella, y **R-CURIOSIDAD**, que bajaba de 0,09 a 0 porque mi alivio tomaba la foto de
soltar por la de usar (valía 0 cuando la foto llevaba menos botiquines que los reales, y esa es también la foto de soltarlo). La medicina junto
a la cama (S-DANO-PAREJA) no intervenía en esa escena (la hermana no estaba herida).

**El arreglo, desde fuera** (`descubre_P7.py`, pieza G `regalo_aprendido`, en el envoltorio de `A.filas`). Para el botiquín, lo que vale para el
hermano un botiquín en el suelo se valora con la creencia de quien regala, como las ganas: k = creencia máxima del cuerpo / cura del catálogo
("no sé" = 0). Se hace con el propio cuerpo: cuando hay un botiquín a la vista en el suelo y el hermano a la vista, se vuelven a calcular las
filas con los botiquines del suelo quitados de la vista (F_sin, con las mismas constantes escaladas) y toda fila que cambie por ello queda
F_sin + (F − F_sin) × k. Así entran S-PROVISION, S-DANO-PAREJA, S-HERIDO y R-HERMANO-FALTA, que son las que leen ese hecho. Las raciones, como
hoy (siguen en la vista). Con TECHO (k = 1) no se toca nada. Y el alivio de la curiosidad vale 0 solo en la foto que usa el botiquín
(`_cura_en_curso`, la marca que el decisor pone solo ahí, decisor_zs.py:830,877-878). Ese segundo punto es un fallo de P7-6/P7-7 que se declara:
soltar el botiquín parecía aliviar la curiosidad como usarlo, y explica parte del regalo y de la oscilación de hacer sitio ración ↔ botiquín del
día 3 de P7-7.

**Banco del regalo** (`banco_P7_8.py` → `P7_8_regalo.json`; réplica en abierto del día 1 del humo de P7-7, brazo APRENDE, cuaderno vacío, un
subproceso por vida):

| vida | regalos en el campo (P7-7) | regalos de la réplica | de ellos con "no sé" | en los tics donde el campo regaló, la réplica elige | d en uno de esos tics |
|---|---:|---:|---:|---|---|
| 27173030/10 | 30 | 0 | 0 | noop 30 | tic 627, k 0,00: `noop` 3,291, `soltar_first_aid` 3,377 |
| 27173030/11 | 8 | 0 | 0 | noop 8 | tic 2.200, k 0,00: `noop` 3,177, `soltar_first_aid` 3,262 |

El asiento 10 deja de regalar botiquines desconocidos (30 → 0) y el 11 también (8 → 0). (Las cogidas de la réplica, 3.825 y 540, son un
artefacto de la réplica en abierto: el diario no cambia cuando la réplica coge, y vuelve a coger el tic siguiente.)

## Sección 2 · F1: apagado y TECHO reproducen A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
| apagado | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |
| TECHO | 1.007.274 | 2 | A4_21622393/10 t 1832; A4_21622393/10 t 2041 |

Los mismos dos tics de siempre. **F1 pasa** con la pieza G y el alivio corregido (`P7_8_F1.json`).

## Sección 3 · El campo y el sello

Cuatro brazos (SUELO, BORRADO, APRENDE, TECHO) × 20 días × 2 series = 160 partidas, emparejadas por semilla; 20 semillas nuevas declaradas
(`semillas_P7_8.json`, sucesión 20260916 + k·104729, k = 69..88, comprobadas sin uso), la serie 2 en orden inverso. Una imagen por brazo
(`Dockerfile.pareja_P7_8`, ARG BRAZO y CUAD; `lanza_P7_8.py` construye, pide, recoge, baja y extrae los cuadernos; el estado en
`P7_8_estado.json`); para APRENDE una imagen por serie y día con los cuadernos del día anterior. Las cinco predicciones, con su medida, en
`SELLO_P7_8.md` (md5 de los archivos y commit `c78ff4db0ffa`, antes de pedir ninguna partida). El evaluador del sello
(`sello_P7_8.py`) y las figuras (`figuras_P7_8.py`) están escritos y no se han ejecutado sobre un campo completo.

## Sección 4 · El freno: APRENDE, serie 1, días 1 a 3

Imágenes: día 1: gemv-p7-campo:v1 (0d199b8e…), día 2: gemv-p7-campo:v2 (756d0be9…), día 3: gemv-p7-campo:v3 (0d209dea…). Lector: `campo_P7_8.py` → `P7_8_campo.json` (las mismas reglas para
los cuatro brazos: un uso es una ventana del canal `channeling first_aid` del diario crudo; gastado si baja el n a bordo).

| día (semilla) | criatura | vivo · puesto · causa | coge (cómo) | regala | usos gastados (tic, situación, vida, curada) | interrumpidos | cuaderno leído | cuaderno al acabar: recuerdos (firmes / al menos), creencia cuerpo dentro, ignorancia |
|---|---|---|---|---:|---|---:|---|---|
| 1 (27487217) | 10 | 12.480 · 8 · anillo (vida 0) | 2 (por ganas 1, de paso 1) | 0 | ninguno | 0 | no (día 1) | 0 (0 / 0), no sé, – |
| 1 (27487217) | 11 | 11.898 · 12 · rival (vida 6) | 1 (por ganas 1) | 0 | ninguno | 7 | no (día 1) | 0 (0 / 0), no sé, – |
| 2 (27591946) | 10 | 12.559 · 4 · anillo (vida 13) | 1 (por ganas 1) | 0 | 1909 dentro 84 +16 | 1 | sí (día 2) | 1 (0 / 1), 8,46, 0,471 |
| 2 (27591946) | 11 | 13.728 · 3 · anillo (vida 14) | 1 (por curiosidad 1) | 0 | 1760 dentro 92 +8 | 0 | sí (día 2) | 1 (0 / 1), 4,28, 0,465 |
| 3 (27696675) | 10 | 14.176 · 5 · rival (vida 4) | 5 (por ganas 3, por curiosidad 2) | 4 | 9494 dentro 89 +11 | 0 | sí (día 3) | 2 (0 / 2), 9,43, 0,278 |
| 3 (27696675) | 11 | 11.675 · 7 · rival (vida 2) | 2 (por ganas 1, de paso 1) | 0 | ninguno | 0 | sí (día 3) | 1 (0 / 1), 4,18, 0,477 |

**(a) El cuaderno viaja y se lee**: sí los días 2 y 3, las dos criaturas (`P7_cuaderno` arranque: leído, día 2 y 3; el de fin de cada día es el
que viajó horneado al siguiente). **Pasa.**

**(b) Cero regalos de botiquines con creencia "no sé"**: días 1 y 2, 0 regalos; día 3, el asiento 10 regaló 4 (tics 9.625, 9.921, 10.212, 11.748) con creencia
leída 8,46 (k = 0,17: el regalo ya vale algo, y vuelve a ganar en 4 de sus 5 cogidas, con la vida a 100). Ninguno con "no sé". **Pasa** tal como
está escrito; la cogida que se regala vuelve en cuanto hay creencia (sección 6).

**(c) Al menos un recuerdo firme del botiquín**: **no.** Tres usos gastados en tres días (vida 84, 92 y 89, todos dentro),
los tres llenaron la vida hasta 100 y quedaron como "al menos" (+16, +8, +11); ningún uso con la vida por debajo de 50. El día 1 el asiento 11 abrió
el canal 7 veces y las 7 se le cerraron con un golpe de un rival (P1, cada unos 50 tics; murió con la vida a 6 con el botiquín en el zurrón).
**Falla, y el campo para aquí**, como pidió la mesa: 3 partidas jugadas de 160, 0,3246 USD.

**Corrección a P7-7, vista aquí.** En P7-7 escribí que las ventanas interrumpidas las rompía el cuerpo "moviéndose mientras cura". No es así: en
las tres ventanas del día 1 de P7-7 (asiento 10) el canal siguió abierto tras el primer `move` y se cerró en el tic de un daño (un golpe de P14 de
10,8; el anillo, 3,28; el anillo, 3,28), y en las 7 del día 1 de aquí, en el tic de un golpe de P1. **El canal lo rompe el daño recibido, no el
movimiento.** La regla de P7-7 (ventana sin gasto = interrumpida, no se apunta) sigue siendo correcta; cambia la causa y lo que queda para la mesa:
curar bajo fuego no cura.

## Sección 5 · Lo que no se hizo

Las 157 partidas restantes, las curvas por día, el evaluador del sello y los GIF del primer uso firme y del día 15 o más: no hay datos.
Los tres diarios del freno quedan en `paintball/runs/P78_s1_d{1,2,3}_APRENDE_<semilla>/` (fuera de git; manifiesto `P7_8_diarios_manifiesto.md`).

## Sección 6 · Lo que queda para la mesa

1. **El freno (c) y la vida casi llena.** La creencia solo se hace firme cuando el cuerpo usa el botiquín con la vida baja; pero el candidato
   `usar_botiquin` existe en cuanto falta un punto (decisor_zs.py:485) y la curiosidad lo empuja (alivio 0 en la foto de usar): en tres días,
   tres usos entre 84 y 92 de vida. Opciones para decidir: (i) que el "al menos" cuente como aprendizaje para el freno (la ignorancia del
   asiento 10 bajó a 0,278 y su creencia es 9,4, el cuerpo ya quiere el botiquín); (ii) que la curiosidad no empuje a usar (alivio 0,5 también en
   la foto de usar, como tenerlo), para que el uso lo pidan el daño y la creencia; (iii) jugar más días del freno. Número y regla: la mesa.
2. **Curar bajo fuego.** El daño recibido rompe el canal (7 de 7 el día 1, asiento 11). El cuerpo congelado no lo sabe: abre el canal con el
   agresor encima y pierde el botiquín de valor cero cada vez (el botiquín no se gasta, pero el tiempo sí). ¿Imaginar que el uso falla si hay
   un rival en alcance (la fila F-4-ALCANCE ya lo mira)?
3. **La cogida que se regala vuelve con creencia** (día 3, 4 de 5): con k = 0,17 el regalo vale 0,17 de lo que valía, y sigue ganando con la vida
   a 100 porque entonces el botiquín no me sirve para nada que la foto vea. Es coherente con la regla; se informa.
4. Pendiente de P7-7: si el mundo salta un primer objeto que no cabe (Ari).

## Archivos

| archivo | qué es |
|---|---|
| `descubre_P7.py` (pieza G, `alivio_de`) | el regalo mira lo aprendido; el alivio solo en la foto de usar |
| `banco_P7_8.py`, `P7_8_regalo.json`; `banco_P7_5.py --f1`, `P7_8_F1.json` | el banco del regalo y F1 |
| `SELLO_P7_8.md`, `semillas_P7_8.json`, `Dockerfile.pareja_P7_8`, `lanza_P7_8.py`, `P7_8_estado.json`, `P7_8_res/`, `cuadernos_P7_8/` | el campo: sello, semillas, imagen, lanzador, estado, resultados y cuadernos del freno |
| `campo_P7_8.py`, `P7_8_campo.json`, `sello_P7_8.py`, `figuras_P7_8.py`, `P7_8_diarios_manifiesto.md` | el lector, el evaluador del sello (sin ejecutar sobre el campo), las figuras (sin datos), el manifiesto |
| `escribe_informe_P7_8.py`, `informe_P7_8.md` | este informe |

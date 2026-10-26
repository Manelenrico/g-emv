# P7-14 · El segundo campo, con pedir: PARADO EN EL FRENO

*4-oct-2026. **El freno falla en la condición (b) y el campo está parado**, como manda el sello: se han jugado 3 de las 160 partidas (APRENDE, serie 1,
días 1 a 3) y no se ha pedido ninguna más. Coste: **créditos de la plataforma 0,2542 USD** (0,0960, 0,0492, 0,1090); **consola de Anthropic 0 USD**.
Acumulado del siete en la plataforma: 16,2689 USD. Saldos: no consultados. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y
congelados sin tocar. Sello antes de jugar: `SELLO_P7_14.md`, commit `045b28f189c7`. Del freno solo se han mirado sus tres condiciones; el sello no se ha evaluado.*

## Sección 1 · Paso 0: sitio

`sitio_P7_14.py` → `P7_14_sitio.json`. Borrados **883 diarios extraídos del paper cinco** (11,63 GiB), todos con su .zip presente y comprobados en el momento: md5 del
.zip igual al de `sumas_P7_12.csv`, md5 de lo que hay dentro del .zip igual al del diario según ese csv, y el diario del disco con ese mismo md5.
Diarios que no cumplían la condición: **0**. Ningún .zip ni manifiesto borrado (siguen los 883 .zip del cinco y `cantera/paper5/DIARIOS_MANIFIESTO.md`).
Espacio libre: **14,07 GB antes, 26,55 GB después**. Los .zip del cinco siguen teniendo una sola copia, en este Mac.

## Sección 2 · Paso 1: el arreglo (la ignorancia descuenta una sola vez)

`cuaderno_P7.creencia(..., con_neutro=False)` da la media de lo vivido, sin el recuerdo neutro; `descubre_P7.k_ganas` y `heal_imaginado` usan esa
(`creencia_vivida_max_cuerpo`, `creencia_vivida_cuerpo`). El neutro se queda en la ignorancia y en la creencia que se informa y que mira el regalo.
Comprobado con el cuaderno de verdad (`ganas_P7_14.py` → `P7_14_ganas.json`), recuerdos firmes con efecto igual a la cura:

| recuerdos | ignorancia | creencia con neutro | creencia vivida | k de las ganas | `W_TARGET` | R-ACOPIO | con ignorancia 0: k, `W_TARGET`, R-ACOPIO | ¿igual a TECHO? |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 0,500 | 25,0 | 50,0 | 0,650 | 2,650 | 0,1170 | 1,0, 3,0, 0,18 | sí, exactamente |
| 3 | 0,250 | 37,5 | 50,0 | 0,825 | 2,825 | 0,1485 | 1,0, 3,0, 0,18 | sí, exactamente |
| 10 | 0,091 | 45,5 | 50,0 | 0,936 | 2,936 | 0,1685 | 1,0, 3,0, 0,18 | sí, exactamente |
| 30 | 0,032 | 48,4 | 50,0 | 0,977 | 2,977 | 0,1759 | 1,0, 3,0, 0,18 | sí, exactamente |

TECHO: k 1, `W_TARGET` 3,0, R-ACOPIO 0,18. Sin ningún recuerdo, k sigue en 0,3 (la esperanza). **F1 sigue pasando** (`P7_14_F1.json`):
apagado 1.007.274 tics iguales y 2 distintos; TECHO 1.007.274 y 2 (los dos de siempre).

## Sección 3 · El sello y lo preparado

`SELLO_P7_14.md` (commit `045b28f189c7`, subido antes de pedir nada): los cuatro brazos con pedir y ojos apagados, 20 días, dos series, semillas nuevas
k = 112 a 131, md5 de los archivos, las cinco preguntas con su medida y el freno. Imágenes horneadas con ese código: ESPERANZA v54, BORRADO v55, TECHO v56, APRENDE_s1_d1 v57, APRENDE_s1_d2 v58, APRENDE_s1_d3 v59.
Lanzador `lanza_P7_14.py`: guarda de disco en 5 GB, limpieza de Docker tras cada horneado, y espera de red (si cae la red espera y reintenta; al
pedir una partida solo reintenta si la conexión no llegó a abrirse). Esperas de red en el freno: 0; paradas: 0.

## Sección 4 · El freno (APRENDE, serie 1, días 1 a 3; de 20:52 a 21:33)

`freno_P7_14.py` → `P7_14_freno.json`.

| condición | medida | resultado |
|---|---|---|
| (a) el cuaderno viaja y se lee | día 1 sin leer (vacío), días 2 y 3 leídos, en los dos asientos | **pasa** |
| (b) hay pedidos, y ningún regalo sin pedido | 15 pedidos abiertos; 2 regalos, **1 sin pedido**; pedir encendido en las 6 vidas, 0 errores | **FALLA** |
| (c) la creencia sube y la ignorancia baja en al menos una criatura | asiento 11: creencia 0,0 → 14,5, ignorancia 0,394 → 0,124; asiento 10: 14,0 → 12,9, 0,290 → 0,228 | **pasa** (el 11) |

**Los dos regalos del freno** (mirados uno a uno porque son la condición que falla):

| día, asiento, tic | ¿pedía el hermano? | d de regalar y de `noop` | adónde fue |
|---|---|---|---|
| día 3, asiento 10, tic 11.881 | sí: sus tres partes anteriores llevaban el pedido (el último, 24 tics antes) | 4,53492 contra 4,55076: regalar gana por 0,016 | lo recoge el hermano, que deja de pedir en el parte siguiente («lo ve») |
| día 1, asiento 10, tic 4.979 | **no**: su último parte (34 tics antes) iba sin pedido, porque veía un botiquín | **3,82825 contra 3,82825: empate exacto** (spread 0,0) | desaparece, con un rival visto encima |

El regalo con pedido es la pieza funcionando: pide, se lo dan, lo coge, deja de pedir. **El regalo sin pedido no es que la pieza deje pasar
beneficio: es un empate.** Sin pedido, regalar no alivia nada y su d es exactamente la de `noop`; y el desempate de la casa no deja ganar a `noop`
(`decisor_zs.py:895-897`, `exclude_noop=True`), así que entre «no hacer nada» y «regalar» gana regalar. Es el mismo caso que ya se vio en P7-11
(los 24 regalos de SUELO) y en el banco de P7-13 (5 de los 21 regalos que quedaban). El sello pide «ningún regalo sin pedido»: con la letra del
sello, (b) falla, y el campo para.

## Sección 5 · Lo que queda para la mesa (propuesta, sin aplicar)

1. **El arreglo que propongo es el de la pieza I, para el regalo**: en un empate, regalar no gana. La pieza I ya hace eso con hacer sitio
   (`descubre_P7.desempate_sin_sitio`: si el mínimo de d lo comparten un candidato de hacer sitio y otro que no lo es, hacer sitio sale del
   desempate). Extenderla a `soltar_<botiquín>` deja el regalo solo cuando gana de verdad. No pone ningún número nuevo. No lo he aplicado: cambia
   el código sellado, y eso es un sello nuevo.
2. **O cambiar la condición (b)** a «ningún regalo sin pedido que gane de verdad» y dejar los empates como están. También es decisión de la mesa.
3. Con cualquiera de las dos: las tres partidas del freno ya jugadas llevan el código de hoy. Si se toca el código, el campo empieza de cero con
   semillas nuevas (quedan por delante k = 132 en adelante) o se declara que los días 1 a 3 de la serie 1 se repiten; si solo se cambia la
   condición, se puede seguir desde el día 4 con estas mismas semillas.
4. Las imágenes fijas (ESPERANZA v54, BORRADO v55, TECHO v56) y los cuadernos de los días 1 a 3 quedan guardados; no se ha pedido nada más.

## Archivos

| archivo | qué es |
|---|---|
| `sitio_P7_14.py`, `P7_14_sitio.json` | paso 0 |
| `cuaderno_P7.py`, `descubre_P7.py`, `ganas_P7_14.py`, `P7_14_ganas.json`, `P7_14_F1.json` | paso 1 y F1 |
| `SELLO_P7_14.md`, `semillas_P7_14.json`, `lanza_P7_14.py`, `campo_P7_14.py`, `analiza_P7_14.py`, `sello_P7_14.py` | el sello, las semillas, el lanzador, los lectores y el evaluador |
| `freno_P7_14.py`, `P7_14_freno.json`, `P7_14_estado.json`, `P7_14_res/`, `cuadernos_P7_14/` | el freno y lo jugado |
| `informe_P7_14.md` | este informe |

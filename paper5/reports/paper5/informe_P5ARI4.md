# P5-ARI4 · Dos comprobaciones para las notas de Ari (patrocinador y curiosidad en tramos limpios), y las dos bolsas del gasto

*28-sep-2026. Coste cero: solo diarios que ya existían (`paintball/runs/P56C_t1_*`, 24 diarios de 12 partidas) y
los JSON de P5-LAG; ninguna partida, ninguna llamada. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al
principio y al final; los 202 congelados del cinco y los 32 del seis: 0 alterados al principio y al final. Ningún
número se escribió antes de calcularlo. Sin propuestas de diseño.*

## 1 · El patrocinador (apéndice A.1): un tic de diferencia, y es del diario

**La configuración** (`cantera/paper5/roster_lento_v1.json`, bloque `sponsor.scripted_gifts`): equipo A, tic
2.016, raciones al asiento 0; equipo A, tic 4.608, botiquín al asiento 1; equipo B, 2.040 / 4.632; y así, un
equipo cada 24 tics. El equipo F (la pareja, asientos 10 y 11) es el sexto: **2.136 (raciones, asiento 10) y
4.728 (botiquín, asiento 11)**.

**Los diarios** (24 diarios de P5-6C, brazos A y F, 12 partidas). El anuncio llega como un evento
`gift_incoming` dentro del registro de un tic, y el registro del tic *t* lleva los eventos que el mundo produjo
en *t − 1*:

| | tic de la configuración | tic del diario en que aparece el anuncio | `lands_tick` que trae el propio evento | tic del diario en que aparece `gift_landed` | diarios en que se ve |
|---|---|---|---|---|---|
| raciones al asiento 10 (equipo F) | **2.136** | **2.137** | **2.256** (= 2.136 + 120) | **2.257** | 19 de 24 (los vivos entonces) |
| botiquín al asiento 11 (equipo F) | **4.728** | **4.729** | **4.848** (= 4.728 + 120) | **4.849** | 17 de 24 |
| primera ración de la partida (equipo A, asiento 0) | 2.016 | 2.017 | 2.136 | 2.137 | |
| último botiquín (equipo H, asiento 15) | 4.776 | 4.777 | 4.896 | 4.897 | |

Todos los diarios coinciden tic por tic. **Lo que Manel dice de la pareja se confirma**: raciones anunciadas
al asiento 10 en el tic 2.136 y botiquín al asiento 11 en el 4.728, cada uno llegando 120 tics después (2.256 y
4.848). El propio evento lo dice: su campo `lands_tick` es exactamente el tic de la configuración más 120.

**De dónde salieron nuestras cifras.** `informe_P5ARI3.md` (§(d)) leyó los anuncios en el diario
`P58M_t0_K_20260916` y copió el tic del *registro* en que aparecían («tic 2017: gift_incoming slot 0 …
tics 2017 a 2185 … 4609 a 4777»), y el apéndice A.1 los heredó. Son los tics de observación del diario: el
mundo anuncia en 2.016-2.184 y 4.608-4.776, y el cuerpo lo lee en la observación siguiente. **Un tic de
diferencia, y es de cómo registra el diario, no del mundo.** El apéndice puede decirlo en cualquiera de los dos
marcos, pero debe decir cuál: «anunciados por el mundo en los tics 2.016 a 2.184 y 4.608 a 4.776 (el diario los
lee un tic después), y cada regalo aterriza 120 tics después de su anuncio».

## 2 · Curiosidad en tramos limpios: «casi seis veces más mundo por instante mientras viaja» (5,81)

La cifra del cinco (P5-8M, apéndice fila 8): con la curiosidad como forma (brazo K), casillas nuevas por cien
tics **dentro de un viaje** contra **fuera de él**, 46,95 contra 8,08, **5,81 veces**. En P5-LAG se midió
igual (`mide_P5_LAG.py`, `P5_LAG_resumen.json` → «P5-8M K1») y la fila quedó en la tabla 2d del informe,
pero no en su resumen; aquí se vuelve a calcular desde `P5_LAG_medidas.json` (las 39 vidas de K), con un
intervalo por vidas que entonces no se dio:

| brazo K, casillas nuevas por cien tics | todos los tics | **solo tics limpios** |
|---|---|---|
| dentro de un viaje (tics · nuevas) | 46,95 (7.135 · 3.350) | **49,70** (6.231 · 3.097) |
| fuera de un viaje | 8,08 (316.590 · 25.569) | **8,90** (276.906 · 24.654) |
| **dentro / fuera** | **5,81** | **5,58** |
| IC95 por vidas (bootstrap, 10.000 remuestreos, semilla 0) | [4,58, 7,20] | [4,20, 7,15] |

**Se sostiene.** En tramos limpios (sin ningún paso perdido a menos de 24 tics) el cuerpo descubre 5,6 veces
más mundo por instante cuando viaja que cuando no viaja; la frase «casi seis veces» sigue valiendo, con el
intervalo entre 4,2 y 7,2. Las dos tasas suben al limpiar (el viaje de 47 a 50, el resto de 8,1 a 8,9),
porque los tics que se quitan son los de los encargos, donde el cuerpo se queda quieto sin quererlo y no
descubre nada; la razón baja un poco porque sube más el denominador.

## 3 · Las dos bolsas del gasto (regla permanente, escrita en `CLAUDE.md`)

| paso | créditos de la plataforma (partidas + sidecar) | dólares de la consola de Anthropic (clave del `.env`) |
|---|---|---|
| **P6-25** (banco del razonador) | 0 (ninguna partida) | **6,60 USD**: 692 llamadas con el SDK de Anthropic y la clave de `cantera/paper5/.env` (Haiku 4.5 y Sonnet 4.5), gasto contado con el `usage` de cada respuesta (`P6_25_crudas_*.jsonl`, `P6_25_gasto.json`) |
| **P6-26** (humo de campo de A8) | **0,159**: 0,112 de las 2 partidas + **0,047** de 8 llamadas por el sidecar (cabecera `X-Coworld-Spend-Usd`) | el humo nativo con la clave: 1 tanda de 1-2 llamadas bajo un tope propio de 0,05 USD, no guardado aparte |
| **P6-27** (humo + serie de A8) | **4,59**: 3,430 de 42 partidas + 1,159 de 266 llamadas por el sidecar | los humos nativos con la clave: 3 tandas de 1-2 llamadas, tope propio 0,05 cada una, no guardadas aparte |

Así que **los 6,60 de P6-25 salieron de la consola de Anthropic**, y **los 0,047 de P6-26 y los 4,59 de P6-27
salieron de los créditos de la plataforma** (el sidecar de Bedrock mide el gasto de lenguaje de los pods y lo
carga a la cuenta de la plataforma; esa cifra es una estimación a precio de lista, no una factura).

**Sobre el panel de la consola que marca 0 tokens en los últimos siete días.** Las 692 llamadas de P6-25 se
hicieron hoy, 28-sep, con la clave de `cantera/paper5/.env` (un archivo de una línea, fechado el 20-sep, sin
comentario que diga a qué espacio de trabajo pertenece), y las respuestas traen `usage` real (tokens de entrada,
salida, escritura y lectura de caché) y los identificadores de modelo `claude-haiku-4-5-20251001` y
`claude-sonnet-4-5-20250929`: las llamadas se sirvieron y se contaron. Si el panel marca 0, esa clave no
pertenece al espacio de trabajo (o a la organización) que el panel está mostrando, o el panel filtra por otra
clave; no puedo comprobarlo desde aquí sin exponer la clave, que no se imprime. Lo que sí puedo dar: el gasto
por `usage` es 6,5959 USD a precio de lista, y desde hoy los informes llevarán las dos bolsas separadas.

**Saldos.** El de la consola de Anthropic no es visible desde aquí (es del panel). El de los créditos de la
plataforma tampoco: la API no expone ninguna ruta de saldo (`/v2/credits`, `/v2/balance`, `/v2/me` devuelven
404) y la CLI no tiene comando de cuenta; la única cifra que la plataforma devuelve es `cost_usd` por partida y
la cabecera de gasto por pod. Los saldos quedan declarados como «a leer en los paneles»; en cuanto Manel los
dé, se anotan.

## 4 · Archivos

Sin archivos nuevos de código: las cifras del punto 1 salen de leer los eventos `gift_incoming` /
`gift_landed` de los 24 diarios de P5-6C (`paintball/runs/P56C_t1_*`, fuera de git, en el manifiesto del
cinco); las del punto 2, de `cantera/paper5/P5_LAG_medidas.json` con la misma cuenta de `mide_P5_LAG.py`; las
del punto 3, de `P6_25_gasto.json`, `P6_25_crudas_*.jsonl`, `P6_26_humo.json`, `P6_27_humo.json`,
`P6_27_serie.json` y los JSON de las partidas `P626_t1_*`, `P627_t*`.

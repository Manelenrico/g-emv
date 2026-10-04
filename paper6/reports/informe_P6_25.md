# P6-25 · El razonador de lenguaje frente al consejero de reglas, en banco

*28-sep-2026. Gasto **6,5957 USD** de 10 (692 llamadas: humo 2, primera 400, bucle 130, pareja
160; medido con el `usage` de la API, llamada a llamada). Nada jugado en la plataforma.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; los 202
congelados del cinco y los 32 del seis: 0 alterados al principio y al final. La clave, solo
desde `cantera/paper5/.env`, ni impresa ni escrita. Lo nuevo, en archivos aparte y declarado:
`P6_25_censo.json` (las 498 propuestas del oráculo con su veredicto de campo),
`escenas_P6_25.py` → `P6_25_escenas.json`, `instruccion_P6_25.md`, `razonador_P6_25.py` →
`P6_25_crudas_*.jsonl`, `P6_25_planes_*.json`, `P6_25_gasto.json`; `juez_P6_25.py` →
`P6_25_juicios_*.json`; `mide_P6_25.py` → `P6_25_medidas.json`; `sello_P6_25.py` →
`SELLO_P6_25.md` (md5 `df59c7bd7ff42facff25cb5b3b402010`, cerrado antes de la primera llamada)
y `P6_25_sello.json`. Ningún número se escribió antes de calcularlo. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**En las 200 escenas del anillo, la puerta6 acepta el plan del razonador tan a menudo como el
del oráculo de reglas: oráculo 51 %, Haiku 51 % de sus planes (49 % de las escenas), Sonnet
55 % (50 %), con la misma ganancia imaginada (medianas 0,31 / 0,25 / 0,29) y el destino dentro
del círculo futuro en el 98 % (Haiku) y el 85 % (Sonnet) de los planes.** Lo que separa a los
dos consejeros no es la puerta sino el reloj: el razonador tarda 3,7 s (Haiku) y 8,1 s (Sonnet)
y, juzgado con el estado del instante en que llega la respuesta, **solo sigue pasando el 52 % y
el 41 % de lo que había pasado**; el oráculo responde en un tic. El bucle de Manel recupera
poco: a los rechazados, la segunda propuesta pasa el 8 % (Haiku) y el 14 % (Sonnet), la tercera
el 0 % y el 4 %. En la pareja, los dos hermanos eligen la misma zona (Chebyshev ≤ 3) en el 83 %
y el 100 % de los pares, pero las dos puertas aceptan a la vez solo en el 20 % y el 18 %; el
mensaje cabe en 120 caracteres siempre, y junto al parte E2 (110 de mediana) casi nunca. Sello:
**7 aciertos, 1 no alcanzada, 2 fallos** (el razonador no pasa menos que el oráculo; el bucle no
sube la tasa).

## 1 · CÓMO SE HIZO (puntos 1 y 2, el método)

**Las escenas.** El censo (`P6_25_censo.json`): 498 propuestas del oráculo en las fases 5-7 de
las 80 vidas de A7h (P6-23 y P6-24), 379 con el hermano vivo; la puerta6 les dio en el campo
205 `ok`, 234 `area`, 33 `vida` (26 sin veredicto). Muestra: 200 al azar (semilla 20260928),
40 de ellas de pareja (el hermano tiene diario en ese tic). Cada vida se repite **en seco por la
vía real** (molde de los bancos P6-15/P6-18): el alma espejo de A7h
(`AlmaPareja23(con_proceso=False)`, la misma del proceso juez) recibe los mensajes del diario
por un cable falso y decide tic a tic; reproduce la elección real en 892.484 de 900.575 tics
(99,1 %). En los tics de escena se construye **el texto** por la vía del consejero del cinco
(`_escena_relator` + `relator_t5.relato`, byte a byte, más los seis números del cuerpo de
P5-5B) y se añaden **las palabras del seis** (`instruccion_P6_25.md` en la instrucción; en la
escena, cinco bloques): el calendario del anillo y el círculo de ahora y el siguiente con la
regla del juego de P6-21, su casilla y su vida, el hermano según el parte E2 (y su último
mensaje tal cual), los rivales vistos y contados, y los últimos 100 tics (vida, quemaduras,
golpes, pasos). Mediana 3.119 caracteres (máximo 4.183). Y se guarda **la instantánea** que
el hilo principal mandaría al proceso juez (`encarga_juicio`, pickle): en t, en t+D para D de
2 a 14 s (para el retraso) y en t para el hermano; 240 escenas, 380 MB en el borrador, fuera
de git (se regeneran con el guion).

**El razonador**, por la vía del cinco (`consejero_forma`: clave, cliente, manual M2 cacheado,
instrucción de P5-5B + tabla enseñada + la página nueva), dos modelos: Haiku 4.5 (barato) y
Sonnet 4.5 (medio). Corre fuera de cualquier hilo principal (es banco; en el campo iría por el
proceso de P6-23). **El juez**: la puerta6 real de A7h en procesos aparte, cargando la
instantánea y llamando a `_juzga` tal cual; captura además las filas que más pesaron en contra
(ganchos de P6-15) y mide si el destino queda dentro del círculo al que va la fase. Sobre los
planes del oráculo reproduce el veredicto de campo en 159 de 190 (83,7 %; las diferencias son
tics de más o de menos en la instantánea: en el campo el juicio llega 20 tics después).

## 2 · EL PLAN DEL RAZONADOR FRENTE AL DEL ORÁCULO (mismas 200 escenas)

| | oráculo | Haiku 4.5 | Sonnet 4.5 |
|---|---|---|---|
| respuestas con plan · callan · intraducibles · no parsean | 200 | 191 · 6 · **3 (1,5 %)** · 0 | 183 · 2 · **15 (7,5 %)** · 0 |
| tramos por plan (media) | 2-4 | 2,6 | 3,7 |
| **acepta puerta6** (sobre planes) | **102 / 200 = 51,0 %** [44-58] | **98 / 191 = 51,3 %** [44-58] | **100 / 183 = 54,6 %** [47-62] |
| acepta (sobre escenas) | 51,0 % | 49,0 % | 50,0 % |
| veredictos: ok · area · vida | 102 · 84 · 14 | 98 · 80 · 13 | 100 · 68 · 15 |
| ganancia imaginada (ventaja), mediana de los aceptados · de todos | 0,309 · 0,096 | 0,255 · 0,076 | 0,295 · 0,125 |
| destino dentro del círculo futuro (P6-21) · a salvo al llegar | 100 % · 100 % | **97,9 %** · 96,3 % | **85,2 %** · 84,2 % |
| tiempo de respuesta, mediana · p90 | 1 tic | **3,66 s** · 5,31 s | **8,13 s** · 11,74 s |
| coste por llamada (usage) | 0 | **0,0041 USD** | **0,0148 USD** |
| emparejado con el oráculo: los dos ok · solo oráculo · solo razonador · ninguno | | 86 · 16 · 12 · 86 (McNemar p 0,57) | 88 · 14 · 12 · 86 (p 0,85) |
| la fila que más pesó en contra (planes rechazados) | | S-8-EXPOSICION 24, F-REENCUENTRO 19, F-4-ALCANCE 16 | S-8-EXPOSICION 17, F-4-ALCANCE 16, F-REENCUENTRO 11 |
| renglones que nombra (`por`) | | F-ANTICIPACION 255, F-DANO 192, S-SOLEDAD 24 | F-ANTICIPACION 498, F-DANO 107, S-SOLEDAD 28 |

Un plan aceptado de Sonnet (escena `20260916_10_12332`, ventaja 0,079): ir a (21,22), ir a
(22,23), esperar 50, esperar 50; «dentro de la zona segura en (22,23), esperando el cierre».
Uno rechazado (`_13000`, ventaja −0,024, por área): ir a (22,24) y tres esperas; en contra,
S-8-EXPOSICION (+0,028) y F-4-ALCANCE (+0,012): la casilla elegida queda a la vista de más
rivales que la que el cuerpo imaginado elige solo.

**Lo que dicen las medidas.** (1) Con el texto del seis, el razonador propone lo mismo que el
oráculo, «ir y quedarse», y la puerta lo trata igual: acepta la mitad, rechaza por área la otra
mitad, y en 172-174 de 200 escenas (86-87 %) los dos consejeros reciben el mismo veredicto. (2) La
puerta no ve diferencia de calidad entre reglas y lenguaje: ventaja de los aceptados 0,31 contra
0,25-0,29. (3) Sonnet se sale del círculo futuro en el 15 % de los planes (Haiku, 2 %): elige
casillas fuera del radio o intraducibles (15 de 200: «casilla fuera del mapa o sólida»), y por
eso, contando escenas, no gana a Haiku. (4) El precio: Haiku 0,004 USD y 3,7 s; Sonnet 0,015 USD
y 8,1 s; el oráculo, 6 ms en el proceso.

## 3 · EL RETRASO (punto 3)

Cada plan de la primera vuelta se juzga también con la instantánea de t+D, D = el primer punto
de la rejilla (2, 4, 6 … 14 s) que no queda antes de su tiempo de respuesta.

| | Haiku (D: 4 s en 110, 6 s en 46, 8 s en 6) | Sonnet (D: 8 s en 55, 10 s en 38, 12 s en 29, 14 s en 7) |
|---|---|---|
| planes juzgables en t+D · sin instantánea (muerto o partida acabada) | 162 · 31 | 130 · **61** |
| aceptados en t, de esos | 83 (51,2 %) | 78 (60,0 %) |
| **de los aceptados en t, siguen pasando en t+D** | **43 / 83 = 51,8 %** [41-62] | **32 / 78 = 41,0 %** [31-52] |
| rechazados en t que pasan en t+D | 24 / 79 = 30,4 % | 15 / 52 = 28,8 % |
| pasan en t+D, sobre todos | 41,4 % | 36,2 % |
| ventaja en t+D de los aceptados en t (mediana) | 0,097 | 0,030 |

Con 4-6 s de retraso, la mitad de lo aceptado deja de valer; con 8-14 s, seis de cada diez, y
además 61 de las 200 escenas de Sonnet ya no existen cuando llega la respuesta (el cuerpo murió
o la partida acabó). Que un 30 % de los rechazados pase en t+D dice lo mismo desde el otro
lado: el veredicto de la puerta cambia con el instante tanto como con el plan.

## 4 · EL BUCLE DE MANEL (punto 4)

En las 80 primeras escenas de la muestra: cuando la puerta rechaza, el razonador recibe el
motivo en palabras (el veredicto y las filas que más pesaron en contra, con sus pesos) y su
plan anterior, y se le pide otro plan; hasta dos veces más.

| | Haiku | Sonnet |
|---|---|---|
| primera propuesta (80 escenas) | 37 / 75 = 49,3 % | 41 / 75 = 54,7 % |
| segunda, a los rechazados de la primera | **3 / 37 = 8,1 %** [3-21] | **4 / 28 = 14,3 %** [6-32] |
| tercera, a los rechazados de la segunda | **0 / 34 = 0,0 %** [0-10] | **1 / 24 = 4,2 %** [1-20] |
| escenas con algún plan aceptado: tras 1 · 2 · 3 vueltas | 46,2 → 50,0 → 50,0 % | 51,2 → 56,2 → 57,5 % |
| la segunda cambia de destino | 75,7 % | 92,9 % |
| ventaja mediana, primera → segunda (mismas escenas) | −0,030 → −0,038 | −0,012 → −0,014 |

**No pasan más la segunda ni la tercera.** El motivo en palabras hace cambiar el destino (en
tres de cada cuatro segundas propuestas) pero no la ventaja: las escenas rechazadas son las que
el cuerpo imaginado ya resuelve mejor por sí mismo (o las que no tienen salida), y otra casilla
del mismo círculo no cambia eso. El bucle añade 4-6 puntos de escenas con algún plan aceptado,
a 2-3 llamadas más por escena.

## 5 · LA PAREJA (punto 5)

40 pares (las escenas de pareja: los dos hermanos vivos, cada uno con su vista, el último
mensaje del otro y la misma petición de plan conjunto, zona y mensaje).

| | Haiku | Sonnet |
|---|---|---|
| dan zona los dos · **coinciden** (Chebyshev ≤ 3) · distancia mediana | 40 · **33 / 40 = 82,5 %** · 1 | 40 · **40 / 40 = 100 %** · 1 |
| las dos zonas dentro del círculo futuro | 97,5 % | 95,0 % |
| **lo aceptan las dos puertas** · alguna · por hermano | **8 / 40 = 20,0 %** · 70,0 % · 45,6 % | **7 / 40 = 17,5 %** · 67,5 % · 47,9 % |
| mensaje: largo mediano · máximo · cabe en 120 · ASCII | 83 · 119 · **100 %** · 96,2 % | 77 · 112 · **100 %** · 100 % |
| cabe junto al E2 de ese instante en los 120 del canal | 3 / 80 = 3,8 % | 7 / 80 = 8,8 % |

Los dos razonadores se ponen de acuerdo en la zona sin hablarse (los dos leen el mismo centro
y el mismo radio) y la eligen dentro del círculo futuro; pero las puertas son dos, cada una
sobre su cuerpo, y aceptar las dos a la vez pasa en uno de cada cinco pares, como el producto
de dos tasas del 45 %. El mensaje («Voy a 22,24 radio5. Tu ve ahi. Quedarse dentro hasta fin
de fase…») cabe en 120 caracteres solo, no junto al parte E2, que ya ocupa 110 de mediana:
necesitaría su propio mensaje del canal.

## 6 · EL SELLO, CONTRASTADO (`SELLO_P6_25.md`, md5 `df59c7bd7ff42facff25cb5b3b402010`)

| punto | predicción | medido | veredicto |
|---|---|---|---|
| 2a aceptación | oráculo ≈ 43 % del campo (±10); razonador por debajo de 10,5 / 18,1 % y de la mitad del oráculo | oráculo 51,0 % (campo 43,4 %: dentro de los 10 puntos); Haiku 51,3 %, Sonnet 54,6 % | **falla**: el razonador pasa como el oráculo |
| 2b ventaja de los aceptados | razonador por debajo del oráculo (0,253 en el campo) | 0,255 / 0,295 contra 0,309 en el banco | acierta (por poco) |
| 2c dentro del círculo futuro | oráculo 100 %; razonador ≥ 70 % | 100 %; 97,9 / 85,2 % | acierta |
| 2d intraducibles | ≈ 0,9 / 8,1 %; < 15 % | 1,5 / 7,5 % | acierta |
| 2e tiempo y coste | 0,7-1,5× lo del cinco (4,4 s y 0,0043; 10,6 s y 0,0150) | 3,66 s y 0,0041 (0,84× / 0,96×); 8,13 s y 0,0148 (0,77× / 0,98×) | acierta |
| 3 retraso | ≥ un tercio de los aceptados deja de pasar; Sonnet pierde más | 48 % y 59 % dejan de pasar; Sonnet más | acierta |
| 4 bucle | 2ª y 3ª pasan más que la 1ª, entre 0 y 15 puntos más | 8,1 y 0,0 % (Haiku), 14,3 y 4,2 % (Sonnet) contra 49-55 % | **falla** |
| 5a coinciden en la zona | ≥ la mitad de los pares | 82,5 / 100 % | acierta |
| 5b aceptan las dos puertas | < 20 % | 20,0 % (Haiku), 17,5 % (Sonnet) | no alcanzada en Haiku (al borde), acierta en Sonnet |
| 5c mensaje ≤ 120 | ≥ 80 % | 100 % (junto al E2: 4-9 %) | acierta |
| gasto | ≤ 10 USD | 6,60 | acierta |

**7 aciertos, 1 no alcanzada, 2 fallos.** Los dos fallos son el hallazgo: (i) con la escena del
seis delante, el razonador de lenguaje propone lo que la puerta acepta tan a menudo como el
oráculo de reglas, cuando en el cinco pasaba una de cada seis; lo que le falta no es juicio
sino tiempo; (ii) decirle por qué se le rechazó no le sirve para pasar.

## 7 · DECLARACIONES

- El md5 de `razonador_P6_25.py` en el sello (`6563f926…`) no es el final (`bf0ed172…`): tras el
  humo se corrigió un error de parseo propio (`saca_json` devolvía una tupla), se añadió el
  recuento del gasto desde las crudas (dos modos corrieron a la vez y el archivo del gasto lo
  escribía el último), se pasó la mitad emocional de los tramos al plan guardado, y se fijaron
  los tamaños del bucle (80 escenas) y de la pareja (40 pares) con el precio medido en la
  primera vuelta. Nada de eso cambia la pregunta al modelo ni el juicio. Los otros archivos
  sellados (escenas, juez, instrucción, `P6_25_escenas.json`) no cambiaron.
- El humo costó 0,073 USD por la escritura de la caché del manual (10.789 tokens); en tanda, la
  caché se lee y el coste es el de arriba.
- En la escena del humo el relato del cinco decía «No sabes dónde está tu hermano» mientras el
  bloque del seis lo veía en (24,24): el relato del cinco se construye desde el registro del
  tic anterior (`ultimo_rec`) y el bloque del seis desde la observación del tic; se deja tal
  cual, byte a byte, y se declara.
- Las instantáneas (380 MB) están en el borrador de la sesión, fuera de git; se regeneran con
  `escenas_P6_25.py` desde los diarios del manifiesto.
- `mide_P6_25.py` tenía el tamaño del bucle cableado a 50; se lee ahora del razonador (80).
- Las respuestas crudas (`P6_25_crudas_*.jsonl`, 1,3 MB) quedan fuera de git como las del cinco
  (`*.jsonl` en `.gitignore`); su md5 está en `DIARIOS_P6_MANIFIESTO.md`.

## 8 · ARCHIVOS

| archivo | qué es |
|---|---|
| `P6_25_censo.json` | las 498 propuestas del oráculo en las fases 5-7 con su veredicto de campo |
| `escenas_P6_25.py` → `P6_25_escenas.json` | la réplica en seco, el texto de cada escena y las rutas de las instantáneas |
| `instruccion_P6_25.md` | las palabras del seis añadidas a la instrucción del cinco |
| `razonador_P6_25.py` → `P6_25_crudas_{humo,primera,bucle2,bucle3,pareja}.jsonl`, `P6_25_planes_*.json`, `P6_25_gasto.json` | las llamadas, las respuestas crudas, los planes traducidos y el gasto |
| `juez_P6_25.py` → `P6_25_juicios_{oraculo,primera,retraso_primera,bucle2,bucle3,pareja}.json` | la puerta6 en proceso aparte sobre las instantáneas |
| `mide_P6_25.py` → `P6_25_medidas.json` | todas las cifras de este informe |
| `sello_P6_25.py` → `SELLO_P6_25.md`, `P6_25_sello.json` | el sello |

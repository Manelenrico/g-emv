# El experimento de la base del ocho, segunda versión (v3): informe

*Prompt 113, del 10 al 11 de noviembre de 2026. Sobre el congelado `valle-congelado-v3` (RG58r). Las predicciones se sellaron antes de jugar ninguna partida (`predicciones_selladas_v3.md`).*

> **Fe de erratas (11-nov-2026, prompt 114; detalle en `informe_diagnostico_v4.md`):**
> 1. **P11:** en la nota de abajo escribí «Igual que en el v2». Es falso: en el v2 P11 se cumplió, con −0,128 [−0,150, −0,106] con la medida completa. El cambio de signo del v3 viene de las decisiones en que las sumas eligen dar; sin ellas sale −0,117.
> 2. **Dormir (P9 y la tabla «la primera vez de cada noche»):** el programa contaba cada vez que una criatura se dormía, a cualquier hora, no la primera de cada noche. Con la cuenta arreglada, RG58r duerme dentro de su casa el 76 %, 75 %, 73 %, 65 % y 70 % de las noches (abundancia, normal, sequía, sequía dura y bestias que crían), y en una puerta 129 noches (no 172). P9 sigue fallando, por la puerta. Las cifras de abajo se dejan como salieron.

## En pocas palabras

- **Se han jugado las 1.400 partidas:** 7 jugadores × 5 mundos × 40 semillas (30041–30080) × 40 días. No ha fallado ninguna.
- **Se cumplen 10 de las 15 predicciones:** P1, P2, P3, P4, P5, P6, P7, P8, P10 y P13.
- **Fallan 5:**
  - **P9:** se duerme en una puerta 172 veces.
  - **P11:** la diferencia sale al revés de lo predicho.
  - **P12:** solo el 48 % de las vueltas del árbol son de noche.
  - **P14:** las vecinas que le robaron no reciben menos.
  - **P15:** hay una racha de 15 regalos de ida y vuelta.
- **RG58r vive mucho más que el tonto donde hay escasez o bestias:**

  | mundo | criaturas vivas de más (de 8) | intervalo |
  |---|---|---|
  | sequía | +2,7 | [+2,3, +3,1] |
  | sequía dura | +1,7 | [+1,4, +2,1] |
  | bestias que crían | +2,9 | [+2,4, +3,5] |

  RG058r, la gemela que solo mira lo que pierde, vive algo más que RG58r en las sequías, como se había declarado (P10).
- **Al perder a la hermana, la tristeza (el duelo) baja a la mitad en unos 6 días, pero la soledad se queda.** Sobre todo en casa: allí la soledad sube casi a su techo, 0,5, y en tres de cada cuatro casos no baja ni a la mitad. Es una medida añadida después de sellar, sin predicción.

## Cómo se ha jugado

- **Push del sellado:** el commit de las predicciones (`61276d6b`) y la etiqueta `valle-congelado-v3` subieron a GitHub (gemv-coworld, rama `paintball`) el 9-nov-2026 a las 23:04:40 UTC, antes de jugar. No ha habido más push.
- **La comprobación jugada** (`salida/puerta_experimento_v3.json`): RG58r y el tonto salen idénticos a sus partidas de referencia del congelado: muertes, criaturas y mundo, línea a línea.
- **Apuntar no cambia nada** (`salida/prueba_experimento_v3.json`): dos partidas jugadas con el registro nuevo y sin él salen idénticas.
- **El experimento:** `lanza_experimento_v3.py experimento 10`, en la carpeta oficial `valle_experimento_v3`.
  - Empezó el 10-nov hacia las 00:04 y acabó el 11-nov a las 05:17: unas 29 horas.
  - Tardó más de lo que estimé al empezar. Cada partida de criatura costaba unos 18 minutos con 10 procesos.
  - 1.400 de 1.400 partidas, ninguna saltada, ningún error en el registro.
- **Lo que se ha vuelto a jugar después**, para la medida del duelo y la soledad (ver abajo):
  - las 105 partidas de RG58r donde muere una hermana;
  - salen las 105 idénticas a las del experimento (`salida/duelo_soledad_v3_puerta.json`).

## Las predicciones, una a una

Los intervalos son del 95 %, por bootstrap de 10.000 remuestreos con semilla 8. Todo sale de `evalua_experimento_v3.py` (`salida/evalua_experimento_v3.md` y `.json`).

| | qué se predijo (resumido) | se cumple si | lo que ha salido | |
|---|---|---|---|---|
| P1 | en sequía, sequía dura y bestias que crían, RG58r vive al menos una criatura más que el tonto | media ≥ 1 e intervalo > 0 en los tres | sequía +2,67 [+2,30, +3,05]; sequía dura +1,73 [+1,40, +2,05]; bestias que crían +2,92 [+2,35, +3,52] | **SE CUMPLE** |
| P2 | en abundancia y normal, RG58r vive de media al menos 7,5 de 8 | las dos ≥ 7,5 | abundancia 7,88; normal 7,85. Declarado: en el normal, RG58r − tonto = −0,12 [−0,25, +0,00] | **SE CUMPLE** |
| P3 | ninguna muerte por golpe entre criaturas | 0 en las 1.400 | 0 | **SE CUMPLE** |
| P4 | con la bestia a la vista, otra pegada al menos el triple de veces que en el tonto | ≥ 3 veces, sumando los cinco mundos | RG58r 35,0 %, tonto 7,6 % (4,6 veces). Por mundo: abundancia 43 · 3; normal 41 · 4; sequía 34 · 2; sequía dura 38 · 2; bestias que crían 33 · 11 | **SE CUMPLE** |
| P5 | en bestias que crían, RG58r echa la bestia al menos una vez por partida | media ≥ 1 | 6,38 por partida | **SE CUMPLE** |
| P6 | da más comida a la hermana que a cada vecina, en todos los mundos | en los cinco | hermana · cada vecina: abundancia 394 · 39,5; normal 524 · 73,2; sequía 678 · 80,3; sequía dura 462 · 73,5; bestias que crían 845 · 94,0 | **SE CUMPLE** |
| P7 | lo que da a quien está flaca es más en las sequías que en abundancia | sequía y sequía dura > abundancia | abundancia 23 %; normal 64 %; sequía 68 %; sequía dura 78 %; bestias que crían 79 % | **SE CUMPLE** |
| P8 | tras la muerte de la hermana pasa más tiempo con vecinas | media > 0 e intervalo > 0 | +0,12 [+0,09, +0,15] de la parte del día pegada a una vecina (165 criaturas) | **SE CUMPLE** |
| P9 | duerme dentro de su casa al menos el 45 % de las noches, y nunca en una puerta | ≥ 45 % en los cinco y 0 en una puerta | dentro: abundancia 65 %; normal 61 %; sequía 58 %; sequía dura 49 %; bestias que crían 57 % (esto sí). **En una puerta: 172 veces** en las 200 partidas | **FALLA** |
| P10 | en las sequías, RG058r vive igual o más que RG58r | límite superior del intervalo ≥ 0 en las dos | RG058r − RG58r: sequía +0,40 [+0,12, +0,68]; sequía dura +0,47 [+0,03, +0,90] | **SE CUMPLE** |
| P11 | en los momentos ambivalentes, RG58r y S58 eligen distinto más a menudo | Q4 − Q1 < 0 con el intervalo < 0 | **+0,132 [+0,103, +0,161]**: en los momentos más ambivalentes coinciden **más**, no menos (Q4 71,2 %, Q1 58,0 %). Sin las decisiones de ir: +0,163 [+0,135, +0,192] | **FALLA** |
| P12 | coge menos del 15 % de la fruta del árbol, menos que el recolector, y más de la mitad de sus vueltas son de noche | las tres cosas | coge el 4,0 % (el recolector el 22,5 %): esto sí. **Vueltas al anochecer o de noche: 48 %** de 757 | **FALLA** |
| P13 | no da su última comida con más de 60 de hambre en más de 2 de cada 100 partidas | ≤ 4 de 200 | 0 de 200 | **SE CUMPLE** |
| P14 | las vecinas que le han robado reciben menos comida que las que nunca le robaron | en todos los mundos con robos | comida por día, las que robaron · las que nunca: abundancia 0,003 · 0,002; normal 0,005 · 0,004; sequía 0,007 · 0,004; sequía dura 0,010 · 0,011; bestias que crían 0,008 · 0,010. **En tres mundos reciben más las que robaron** | **FALLA** |
| P15 | ninguna racha de más de 10 regalos de ida y vuelta del mismo tipo | ninguna > 10 en las 200 | **comida 15** (bestias que crían, semilla 30046), medicina 1. Con «menos de 40 turnos» o «40 o menos», lo mismo: 15 · 1 | **FALLA** |

**Notas a las que fallan:**
- **P9:** la parte dentro de casa se cumple en los cinco mundos; falla solo por la puerta.
- **P11:** el resultado es claro y en la dirección contraria. Igual que en el v2.
- **P14:**
  - Casi todos los pares (criatura, vecina) han sufrido algún robo: entre 1.396 y 1.741 pares ladrones por mundo, frente a 179–524 que nunca robaron.
  - Las tasas son muy pequeñas: menos de una comida cada 100 días por par.
- **P15:** en las otras clases, la racha más larga (comida · medicina) es:

  | clase | comida | medicina |
  |---|---|---|
  | RG058r | 1 | 3 |
  | S58 | 11 | 1 |
  | S058 | 3 | 2 |
  | P58 | 4 | 2 |

  S58 da muchísima comida (más de 1.000 comidas por partida en abundancia, normal y sequía; ver la tabla). Pero su racha de ida y vuelta más larga es de 11, porque reparte entre muchas.

## La tabla, como la del cierre v5

Está entera en `tabla_experimento_v3.md` (de `tabla_experimento_v3.py`) y copiada al final de este informe, en el anexo A.

## Las medidas sin predicción (M1–M6)

Están enteras en `medidas_v3.md` (de `medidas_v3.py`) y copiadas en el anexo B, con los mapas. Lo principal:

- **M1, felicidad funcional** (turnos despierta con los tres balances en positivo):
  - **RG58r, la media de la aldea:** abundancia 76 %; normal 62 %; sequía 56 %; sequía dura 36 %; bestias que crían 41 %.
  - **La peor parada** de cada aldea: de 56 % a 14 %.
  - **S58 y P58** quedan por debajo de RG58r en todos los mundos.
  - **Aviso: RG058r y S058 dan 0 % por construcción, no por estar peor.** No tienen las filas de ganancia (`rg_ganancias=False`): su placer, su alegría y su amor son nulos y sus tres balances no pueden ser positivos. Para ellas la medida no dice nada.
- **M2, momentos hygge** (RG58r): las noches con al menos uno, de cada criatura:

  | mundo | noches con al menos uno |
  |---|---|
  | abundancia | 71 % |
  | normal | 59 % |
  | sequía | 51 % |
  | sequía dura | 24 % |
  | bestias que crían | 41 % |

- **M3, lo que siente en cada sitio según sus recuerdos:**
  - De día, todos los sitios dejan recuerdos buenos en recursos.
  - De noche, mucho menos.
  - Los recuerdos peores para el cuerpo son, sobre todo, los de lo salvaje de noche, y en los mundos duros también los del camino de noche.
- **M4, los tres mapas por mundo:** bienestar, miedo y peleas. Están en `salida/figuras_v3/mapas_<mundo>.png` y en el anexo B.
  - **Bienestar:** alto en el centro del valle, alrededor de las casas.
  - **Peleas:** se juntan en unas pocas casillas del centro.
- **M5, el huerto:** se trabaja entre unas 4.500 y 6.400 veces por partida en las clases de criatura (S58 es la que menos); el tonto, entre 3.300 y 5.500.
  - En RG58r, la criatura que más trabaja hace el 17 % del total.
  - En la sequía dura, el 28 %.
- **M6, el perdón:**
  - Hay muchísimos robos de vecinas: de 3.529 a 8.253 por mundo, en 40 partidas.
  - De los que vuelven a valer lo de antes en el radar de la robada, la mediana es 1 día.
  - Entre el 45 % y el 49 % no vuelven antes del final o de una muerte.

## Medidas añadidas después de sellar, sin predicción

Las pidió Manel con el experimento ya en marcha. No tienen predicción: se dicen, no se cumplen ni fallan. Están en `anadidas_v3.py` → `anadidas_v3.md` (A1–A3) y en `duelo_soledad_v3.py` → `duelo_soledad_v3.md` (A4). Las tablas enteras están en el anexo C.

### A1. Dónde se dan regalos, junto al bienestar

Por mundo, sumando las 40 partidas de RG58r: comida y medicina dadas con éxito, en la casilla de quien da. Las figuras están en `salida/figuras_v3/regalos_<mundo>.png`.

- Los regalos se juntan en muy pocas casillas del centro del valle, las mismas donde se juntan las peleas (M4).
- En el resto del valle apenas se dan.

### A2. La que pierde a su hermana frente a las que la conservan

Son las criaturas de RG58r cuya hermana muere el día 5 o después, y que viven al menos 5 días más: 167 casos en las 200 partidas. Se comparan con las de la misma partida que conservan a su hermana esos mismos días, 610 casos de control. Cifras de los cinco mundos juntos:

| | pierde a la hermana: antes → después | la conserva: antes → después |
|---|---|---|
| felicidad funcional | 27 % → 1 % | 41 % → 45 % |
| felicidad en casa | 36 % → 0 % | 48 % → 47 % |
| duerme en su casa | 78 % → 73 % | 79 % → 76 % |
| pegada a una vecina, de día | 16 % → 28 % | 17 % → 15 % |
| pegada a una vecina, de noche | 10 % → 22 % | 11 % → 12 % |

- **Días hasta recuperar la felicidad de antes:** mediana de 11 días entre las que la recuperan. **134 de las 167 no la recuperan** antes del día 40 o de su propia muerte.
- **Busca la compañía de una vecina:** sí, de día y también de noche. De noche el tiempo pegada a una vecina pasa del 10 % al 22 %.
- **Sigue durmiendo en casa:** casi igual que antes (del 78 % al 73 %), como las de control.
- Los casos son 167 aquí, 165 en P8 y 164 en A4, por pequeñas diferencias de criterio:
  - P8 usa el criterio de `analiza_v45`;
  - aquí se exige que la muerte sea del día 5 o después;
  - en A4 se quedan fuera tres casos sin turnos despierta en la ventana.

### A3. Cuántas opciones compara la foto de RG50r en cada decisión

Sale del registro de la foto del prompt 101 (`valle_fotos_v3`).

- **Las partidas:** Manel habla de 27 partidas, que son las de RG50r, RG050r y S50. Las de RG50r son 9 (abundancia, sequía y sequía dura, semillas 30001–30003), con 612.178 decisiones.
- **Opciones por decisión:** media 17,1, mediana 18, máximo 36. Es casi igual en los tres mundos.
- **De qué tipo** (cuántas de cada tipo hay de media en cada decisión):

  | tipo de opción | por decisión |
  |---|---|
  | ir a un matorral | 4,0 |
  | moverse un paso | 3,0 |
  | dejar | 1,2 |
  | quedarse | 1,0 |
  | empujar | 0,9 |
  | golpear | 0,9 |
  | dar | 0,8 |
  | ir a la frontera | 0,8 |
  | ir al bosque | 0,7 |
  | ir a un objeto | 0,6 |
  | ir al botín | 0,6 |
  | ir a casa | 0,6 |
  | dormir | 0,5 |
  | comer | 0,4 |
  | ir con la hermana | 0,4 |
  | ir con una vecina | 0,3 |
  | trabajar una planta | 0,2 |
  | coger | 0,1 |
  | trabajar | 0,1 |
  | ir a una llamada | 0,1 |

- **Cada cuántos turnos decide** una criatura: mediana 1 turno, media 1,6. El 91 % de las veces vuelve a decidir en el turno siguiente.
- **Lo que el registro no apunta:**
  - los turnos en que sigue un destino ya elegido;
  - las noches en que el mundo la duerme de un tirón.

  Por eso, en tiempo de reloj, la criatura decide algo menos a menudo de lo que dicen estas cifras.

### A4. El duelo y la soledad, por separado

Medida pedida después de A2. Las dos señales salen de la foto de ahora que calcula cada criatura en cada turno:
- **el duelo** (la tristeza por la pérdida): las filas S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO;
- **la soledad** (estar sin compañía): la fila S-SOLEDAD, en todos los turnos despierta y aparte solo los de su casa.

Aparte se da S-COMPANIA, que mide lo lejos que está la hermana viva. Al morir ella, el cuerpo deja de calcularla.

**De dónde salen los números:**
- El experimento no apunta estas filas. Por eso se volvieron a jugar las 105 partidas de RG58r con una hermana muerta y se apuntaron.
- Las 105 salieron idénticas a las del experimento.

**Cómo se mide:**
- Medias por turno despierta: los 5 días antes de la muerte, el día siguiente y el peor de los 5 días después.
- Desde ese peor día, cuántos días tarda cada señal:
  - **«a la mitad»:** en bajar a la mitad de la subida o menos;
  - **«vuelve»:** en bajar a una décima o menos.
- La medida «a la mitad» la añadí al probar con una sola partida, antes de ver los datos de todas. Hacía falta porque el duelo baja hacia un suelo, el 30 % de lo que era (DUELO_SUELO = 0,3), y no hacia cero; así, con «vuelve» solo, el duelo casi nunca vuelve.

Cifras de los cinco mundos juntos:

| señal | grupo | antes | peor de los 5 días después | baja a la mitad: mediana de días (cuántas llegan) | vuelve a como estaba |
|---|---|---|---|---|---|
| duelo | pierde a la hermana (164) | 0,04 | 1,48 (el día siguiente) | **6 días** (111 de las 139 a las que sube) | 1 de 139 |
| soledad | pierde a la hermana (164) | 0,03 | 0,46 (hacia el día 3) | 12 días (**solo 40 de 164**) | **ninguna** |
| soledad en casa | pierde a la hermana (163) | 0,02 | 0,50, el techo (desde el día siguiente) | 9 días (**solo 43 de 163**) | **ninguna** |
| duelo | la conserva (600) | 0,02 | 0,25 | 5 días (279 de 341) | 13 de 341 |
| soledad | la conserva (600) | 0,02 | 0,05 | 4 días (315 de 327) | 4 días (315 de 327) |

**Lo que se ve:**
- **La tristeza baja en unos días.** El duelo salta el día después de la muerte y en la mitad de los casos baja a la mitad en unos 6 días. Después se queda en su suelo.
- **La soledad se queda.** Sube durante dos o tres días hasta casi su techo (0,5) y, en tres de cada cuatro casos, no baja ni a la mitad.
  - En casa es más clara: desde el día siguiente está casi en el techo (0,48 de media). Allí, sin la hermana, no suele haber nadie a la vista que acompañe.
  - Ninguna criatura vuelve a la soledad de antes.
- **Pasa en los cinco mundos** (tabla entera en el anexo C). La sequía dura es donde más se mueve la soledad: allí baja a la mitad en 33 de 76 casos, frente a 1–3 casos en los otros mundos.
- **Las de control también tienen algo de duelo** (0,25 en su peor día), porque el cuerpo hace sentir duelo, más corto, por una vecina que muere. Su soledad apenas se mueve.
- **La falta de la hermana viva (S-COMPANIA)** cae a casi cero al morir ella, porque el cuerpo deja de calcularla. Desde entonces es la soledad la que lleva la ausencia.

## Fallos míos y arreglos (ninguno en el experimento)

- **Tres veces lancé un `python3 -` con la entrada vacía**, que Manel tiene prohibido: una al preparar el experimento, otra el 10-nov al preparar A4, y otra el 11-nov al repasar este informe. Ninguna ejecutó nada, pero no debió pasar ni una vez.
- **`tabla_experimento_v3.py` falló la primera vez.** Solo ponía «+sabores» al nombre de las partidas de las clases que empiezan por RG, y S58, S058 y P58 también juegan con los sabores. Lo arreglé como ya estaba en `evalua_experimento_v3.py`. Es un fallo del análisis, no del experimento.
- **`duelo_soledad_v3.py` leía mal el nombre de las partidas** de los mundos que empiezan por «s». Lo arreglé antes de dar ninguna cifra.
- **En A2, una casilla salía «nan»** cuando ninguna criatura se recuperaba. Ahora dice «— (no vuelven 6 de 6)».
- **No se ha cambiado nada del experimento** mientras se jugaba.

## Gasto

| bolsa | gasto en el prompt | saldo |
|---|---|---|
| créditos de la plataforma | 0 (todo se jugó en el Mac) | no lo he leído |
| dólares de la consola de Anthropic | 0 | no lo he leído |

## Ficheros

- **Programas** (en `cantera/paper8/`):
  - `lanza_experimento_v3.py`, sellado;
  - `evalua_experimento_v3.py`, `tabla_experimento_v3.py`, `medidas_v3.py`, `anadidas_v3.py` y `duelo_soledad_v3.py`;
  - las pruebas `prueba_medidas_v3.py`, `prueba_anadidas_v3.py` y `prueba_duelo_soledad_v3.py`.
- **Resultados:**
  - `salida/evalua_experimento_v3.md` y `.json`, `tabla_experimento_v3.md`, `medidas_v3.md`, `salida/medidas_v3.json`, `anadidas_v3.md`, `duelo_soledad_v3.md` y `salida/duelo_soledad_v3.json`;
  - las figuras en `salida/figuras_v3/`;
  - las comprobaciones `salida/puerta_experimento_v3.json`, `salida/prueba_experimento_v3.json` y `salida/duelo_soledad_v3_puerta.json`.
- **Las partidas** (en el disco «Mem G-EMV»):
  - `valle_experimento_v3`, las 1.400;
  - `valle_experimento_v3_duelo`, las 105 vueltas a jugar, con `filas.jsonl.gz`.

## Anexo A. La tabla, como la del cierre v5 (`tabla_experimento_v3.md`)

*En los anexos, los decimales van con punto, tal como salen de los programas; «—» quiere decir que no hay nada que medir.*

### Vivas al día 40 (de 8) y de qué mueren

| mundo | tonto | recolector | RG58r | RG058r | S58 | S058 | P58 | muertes RG58r: hambre · bestia · golpe · terreno | RG058r |
|---|---|---|---|---|---|---|---|---|---|
| abundancia | 8.00 | 8.00 | 7.88 | 8.00 | 7.83 | 8.00 | 7.88 | 0 · 4 · 0 · 1 | 0 · 0 · 0 · 0 |
| normal | 7.97 | 7.83 | 7.85 | 7.97 | 7.60 | 8.00 | 7.85 | 2 · 4 · 0 · 0 | 0 · 1 · 0 · 0 |
| sequia | 4.65 | 7.95 | 7.33 | 7.72 | 6.22 | 7.83 | 7.00 | 18 · 8 · 0 · 1 | 7 · 4 · 0 · 0 |
| sequia_dura | 2.00 | 3.50 | 3.73 | 4.20 | 2.92 | 3.48 | 3.88 | 151 · 17 · 0 · 3 | 144 · 8 · 0 · 0 |
| bestias_crian | 3.23 | 5.55 | 6.15 | 6.55 | 4.47 | 6.58 | 6.15 | 20 · 52 · 0 · 2 | 10 · 45 · 0 · 3 |

### Diferencia de vivas por semillas emparejadas (media [IC 95 %], bootstrap de semillas)

| mundo | RG58r − tonto | RG58r − RG058r | RG58r − S58 | RG58r − P58 |
|---|---|---|---|---|
| abundancia | -0.12 [-0.23, -0.03] | -0.12 [-0.23, -0.03] | +0.05 [-0.12, +0.23] | +0.00 [-0.15, +0.15] |
| normal | -0.12 [-0.25, +0.00] | -0.12 [-0.25, +0.00] | +0.25 [-0.07, +0.65] | +0.00 [-0.17, +0.20] |
| sequia | +2.67 [+2.30, +3.05] | -0.40 [-0.68, -0.12] | +1.10 [+0.70, +1.48] | +0.33 [+0.00, +0.65] |
| sequia_dura | +1.73 [+1.40, +2.05] | -0.47 [-0.90, -0.03] | +0.80 [+0.45, +1.15] | -0.15 [-0.50, +0.23] |
| bestias_crian | +2.92 [+2.35, +3.52] | -0.40 [-0.82, +0.05] | +1.68 [+1.20, +2.12] | +0.00 [-0.42, +0.42] |

### Pelearse, dormir, dar y guardar (los cálculos de siempre, cierre_v46)

| mundo | jugador | empujones · golpes a otras (por partida) | muertes por golpe | de noche: duerme · en su casa · otra casa · fuera | comidas dadas (a quien lo necesitaba) · medicinas (ídem) | a la hermana · a una vecina (total) | dejadas: despensa · almacén |
|---|---|---|---|---|---|---|---|
| abundancia | tonto | 0.0 · 0.0 | 0 | 100 % · 100 % · 0 % · 0 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 514.9 |
| abundancia | recolector | 0.0 · 0.0 | 0 | 99 % · 99 % · 0 % · 1 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 512.3 |
| abundancia | RG58r | 241.3 · 0.3 | 0 | 89 % · 79 % · 4 % · 17 % | 15.8 (23 %) · 0.75 (57 %) | 394 · 237 | 229.4 · 0.2 |
| abundancia | RG058r | 58.8 · 0.0 | 0 | 84 % · 87 % · 1 % · 11 % | 5.7 (63 %) · 0.42 (35 %) | 157 · 71 | 197.4 · 0.1 |
| abundancia | S58 | 582.3 · 0.0 | 0 | 83 % · 35 % · 4 % · 61 % | 1683.8 (2 %) · 0.53 (67 %) | 45452 · 21902 | 101.2 · 0.0 |
| abundancia | S058 | 53.5 · 0.0 | 0 | 82 % · 87 % · 2 % · 11 % | 3.0 (49 %) · 0.50 (10 %) | 84 · 37 | 166.1 · 0.0 |
| abundancia | P58 | 397.4 · 5.7 | 0 | 84 % · 69 % · 6 % · 25 % | 116.2 (8 %) · 0.57 (39 %) | 3038 · 1608 | 226.3 · 0.1 |
| normal | tonto | 0.0 · 0.0 | 0 | 100 % · 100 % · 0 % · 0 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 480.9 |
| normal | recolector | 0.0 · 0.0 | 0 | 99 % · 99 % · 0 % · 1 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 294.8 |
| normal | RG58r | 265.4 · 0.3 | 0 | 89 % · 78 % · 4 % · 18 % | 24.1 (64 %) · 1.50 (43 %) | 524 · 439 | 184.7 · 0.0 |
| normal | RG058r | 72.2 · 0.0 | 0 | 85 % · 87 % · 1 % · 12 % | 10.0 (90 %) · 1.40 (36 %) | 260 · 140 | 178.9 · 0.0 |
| normal | S58 | 531.9 · 0.0 | 0 | 82 % · 44 % · 5 % · 50 % | 1019.9 (8 %) · 0.78 (55 %) | 28969 · 11825 | 83.8 · 0.2 |
| normal | S058 | 67.0 · 0.0 | 0 | 84 % · 88 % · 1 % · 11 % | 7.0 (91 %) · 1.35 (24 %) | 195 · 84 | 199.6 · 0.0 |
| normal | P58 | 413.0 · 4.2 | 0 | 84 % · 70 % · 5 % · 25 % | 90.5 (30 %) · 1.35 (33 %) | 2098 · 1524 | 160.6 · 0.1 |
| sequia | tonto | 0.0 · 0.0 | 0 | 100 % · 100 % · 0 % · 0 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 337.5 |
| sequia | recolector | 0.0 · 0.0 | 0 | 99 % · 99 % · 0 % · 1 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 327.4 |
| sequia | RG58r | 237.5 · 0.2 | 0 | 88 % · 75 % · 5 % · 20 % | 29.0 (68 %) · 1.95 (71 %) | 678 · 482 | 174.0 · 0.1 |
| sequia | RG058r | 64.8 · 0.0 | 0 | 87 % · 87 % · 1 % · 12 % | 15.3 (93 %) · 1.77 (68 %) | 409 · 202 | 185.4 · 0.1 |
| sequia | S58 | 478.6 · 0.0 | 0 | 83 % · 34 % · 4 % · 62 % | 1023.5 (8 %) · 0.88 (80 %) | 24749 · 16191 | 54.1 · 0.0 |
| sequia | S058 | 62.6 · 0.0 | 0 | 84 % · 87 % · 1 % · 11 % | 15.1 (92 %) · 1.23 (49 %) | 416 · 188 | 142.7 · 0.0 |
| sequia | P58 | 352.1 · 4.0 | 0 | 84 % · 69 % · 5 % · 26 % | 93.2 (30 %) · 1.68 (46 %) | 2126 · 1601 | 138.2 · 0.1 |
| sequia_dura | tonto | 0.0 · 0.0 | 0 | 100 % · 100 % · 0 % · 0 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 166.9 |
| sequia_dura | recolector | 0.0 · 0.0 | 0 | 100 % · 99 % · 0 % · 1 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 212.1 |
| sequia_dura | RG58r | 133.1 · 0.2 | 0 | 87 % · 65 % · 6 % · 29 % | 22.6 (78 %) · 1.80 (88 %) | 462 · 441 | 50.2 · 0.1 |
| sequia_dura | RG058r | 41.4 · 0.0 | 0 | 83 % · 81 % · 5 % · 14 % | 15.2 (98 %) · 2.58 (92 %) | 397 · 209 | 57.2 · 0.0 |
| sequia_dura | S58 | 193.6 · 0.0 | 0 | 85 % · 33 % · 3 % · 64 % | 419.6 (11 %) · 0.53 (95 %) | 9017 · 7765 | 13.8 · 0.0 |
| sequia_dura | S058 | 35.0 · 0.0 | 0 | 81 % · 74 % · 8 % · 18 % | 14.8 (94 %) · 2.05 (82 %) | 329 · 264 | 61.7 · 0.0 |
| sequia_dura | P58 | 180.8 · 2.5 | 0 | 84 % · 66 % · 6 % · 28 % | 62.2 (39 %) · 1.38 (80 %) | 1319 · 1171 | 45.4 · 0.0 |
| bestias_crian | tonto | 0.0 · 0.0 | 0 | 100 % · 100 % · 0 % · 0 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 279.5 |
| bestias_crian | recolector | 0.0 · 0.0 | 0 | 99 % · 99 % · 0 % · 1 % | 0.0 (—) · 0.00 (—) | 0 · 0 | 0.0 · 248.6 |
| bestias_crian | RG58r | 218.6 · 0.2 | 0 | 88 % · 74 % · 5 % · 22 % | 35.2 (79 %) · 2.27 (89 %) | 845 · 564 | 219.3 · 0.1 |
| bestias_crian | RG058r | 60.7 · 0.0 | 0 | 87 % · 87 % · 1 % · 12 % | 18.7 (96 %) · 3.35 (96 %) | 501 · 247 | 163.9 · 0.0 |
| bestias_crian | S58 | 391.4 · 0.0 | 0 | 82 % · 38 % · 5 % · 57 % | 710.0 (11 %) · 1.23 (90 %) | 17448 · 10954 | 57.5 · 0.0 |
| bestias_crian | S058 | 59.0 · 0.0 | 0 | 87 % · 86 % · 2 % · 12 % | 21.4 (95 %) · 2.50 (90 %) | 620 · 238 | 182.2 · 0.0 |
| bestias_crian | P58 | 304.1 · 3.3 | 0 | 85 % · 68 % · 5 % · 27 % | 90.7 (47 %) · 2.52 (89 %) | 2016 · 1612 | 161.0 · 0.0 |

### Dormir: la primera vez de cada noche (cada criatura)

| mundo | jugador | noches | dentro de su casa | en una puerta | en otra casa | fuera |
|---|---|---|---|---|---|---|
| abundancia | tonto | 12800 | 100 % | 0 % | 0 % | 0 % |
| abundancia | recolector | 12810 | 99 % | 0 % | 0 % | 1 % |
| abundancia | RG58r | 29695 | 65 % | 0 % | 2 % | 33 % |
| abundancia | RG058r | 40346 | 84 % | 0 % | 1 % | 16 % |
| abundancia | S58 | 41355 | 25 % | 0 % | 2 % | 73 % |
| abundancia | S058 | 43256 | 86 % | 0 % | 1 % | 13 % |
| abundancia | P58 | 44655 | 46 % | 0 % | 3 % | 51 % |
| normal | tonto | 12787 | 100 % | 0 % | 0 % | 0 % |
| normal | recolector | 12681 | 99 % | 0 % | 0 % | 1 % |
| normal | RG58r | 29599 | 61 % | 0 % | 2 % | 37 % |
| normal | RG058r | 42163 | 80 % | 0 % | 1 % | 19 % |
| normal | S58 | 40065 | 30 % | 0 % | 2 % | 68 % |
| normal | S058 | 44702 | 85 % | 0 % | 1 % | 15 % |
| normal | P58 | 43736 | 47 % | 0 % | 3 % | 51 % |
| sequia | tonto | 9659 | 100 % | 0 % | 0 % | 0 % |
| sequia | recolector | 12754 | 99 % | 0 % | 0 % | 1 % |
| sequia | RG58r | 28571 | 58 % | 0 % | 2 % | 40 % |
| sequia | RG058r | 37728 | 81 % | 0 % | 1 % | 18 % |
| sequia | S58 | 35327 | 22 % | 0 % | 2 % | 76 % |
| sequia | S058 | 40240 | 83 % | 0 % | 1 % | 16 % |
| sequia | P58 | 38864 | 46 % | 0 % | 3 % | 51 % |
| sequia_dura | tonto | 6053 | 100 % | 0 % | 0 % | 0 % |
| sequia_dura | recolector | 9042 | 99 % | 0 % | 0 % | 1 % |
| sequia_dura | RG58r | 17389 | 49 % | 0 % | 2 % | 49 % |
| sequia_dura | RG058r | 22409 | 70 % | 0 % | 1 % | 29 % |
| sequia_dura | S58 | 17649 | 23 % | 0 % | 1 % | 76 % |
| sequia_dura | S058 | 21145 | 65 % | 0 % | 2 % | 34 % |
| sequia_dura | P58 | 22624 | 45 % | 0 % | 2 % | 53 % |
| bestias_crian | tonto | 9253 | 100 % | 0 % | 0 % | 0 % |
| bestias_crian | recolector | 12209 | 99 % | 0 % | 0 % | 1 % |
| bestias_crian | RG58r | 27971 | 57 % | 0 % | 3 % | 40 % |
| bestias_crian | RG058r | 36882 | 77 % | 0 % | 1 % | 22 % |
| bestias_crian | S58 | 33123 | 25 % | 0 % | 2 % | 73 % |
| bestias_crian | S058 | 33314 | 79 % | 0 % | 1 % | 20 % |
| bestias_crian | P58 | 36110 | 47 % | 0 % | 2 % | 50 % |

### Dar (registro del mundo; por partida): a quién, a las que robaron y qué

| mundo | jugador | a la hermana · a una vecina (comida y medicina) | a una que le robó antes: hermana · vecina | comida dada: huerto · bosque · dulce · sin origen | medicina: media (mediana; máximo) |
|---|---|---|---|---|---|
| abundancia | tonto | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| abundancia | recolector | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| abundancia | RG58r | 10.0 · 6.5 | 3.1 · 4.3 | 11.1 · 3.8 · 0.10 · 0.7 | 0.75 (0; 3) |
| abundancia | RG058r | 4.1 · 2.0 | 2.2 · 0.5 | 4.2 · 1.1 · 0.00 · 0.4 | 0.42 (0; 2) |
| abundancia | S58 | 1136.4 · 548.0 | 335.9 · 394.7 | 1414.3 · 36.2 · 4.50 · 102.2 | 0.53 (0; 3) |
| abundancia | S058 | 2.3 · 1.2 | 1.3 · 0.3 | 2.4 · 0.3 · 0.03 · 0.3 | 0.50 (0; 3) |
| abundancia | P58 | 76.0 · 40.7 | 23.1 · 23.4 | 83.0 · 17.1 · 0.03 · 13.1 | 0.57 (0; 3) |
| normal | tonto | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| normal | recolector | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| normal | RG58r | 13.3 · 12.2 | 4.7 · 8.3 | 16.6 · 6.2 · 0.12 · 1.0 | 1.50 (1; 4) |
| normal | RG058r | 7.3 · 4.1 | 4.4 · 0.6 | 7.3 · 2.5 · 0.00 · 0.2 | 1.40 (1; 5) |
| normal | S58 | 724.4 · 296.2 | 249.4 · 145.5 | 791.1 · 36.2 · 0.00 · 120.6 | 0.78 (1; 2) |
| normal | S058 | 5.5 · 2.9 | 2.9 · 0.7 | 5.1 · 1.8 · 0.03 · 0.1 | 1.35 (1; 6) |
| normal | P58 | 52.7 · 39.2 | 13.6 · 23.0 | 55.4 · 19.1 · 0.35 · 13.8 | 1.35 (1; 5) |
| sequia | tonto | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| sequia | recolector | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| sequia | RG58r | 17.6 · 13.3 | 6.5 · 10.1 | 20.6 · 7.5 · 0.12 · 0.7 | 1.95 (2; 7) |
| sequia | RG058r | 10.9 · 6.2 | 5.9 · 1.4 | 11.6 · 3.2 · 0.07 · 0.4 | 1.77 (1; 9) |
| sequia | S58 | 618.9 · 405.5 | 196.3 · 250.6 | 810.4 · 37.7 · 0.97 · 102.2 | 0.88 (0; 4) |
| sequia | S058 | 11.0 · 5.3 | 7.2 · 1.0 | 11.4 · 3.3 · 0.03 · 0.4 | 1.23 (1; 6) |
| sequia | P58 | 53.4 · 41.4 | 15.2 · 25.1 | 59.1 · 18.3 · 0.23 · 13.1 | 1.68 (2; 5) |
| sequia_dura | tonto | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| sequia_dura | recolector | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| sequia_dura | RG58r | 12.3 · 12.1 | 3.9 · 7.4 | 14.9 · 6.2 · 0.12 · 1.1 | 1.80 (2; 5) |
| sequia_dura | RG058r | 11.4 · 6.3 | 6.6 · 1.4 | 11.8 · 2.8 · 0.17 · 0.5 | 2.58 (2; 8) |
| sequia_dura | S58 | 225.7 · 194.4 | 55.8 · 69.7 | 259.4 · 18.2 · 1.23 · 112.0 | 0.53 (0; 4) |
| sequia_dura | S058 | 9.3 · 7.5 | 5.1 · 1.9 | 11.9 · 2.6 · 0.00 · 0.3 | 2.05 (2; 10) |
| sequia_dura | P58 | 33.5 · 30.1 | 7.5 · 15.7 | 34.6 · 11.6 · 0.30 · 14.0 | 1.38 (1; 6) |
| bestias_crian | tonto | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| bestias_crian | recolector | 0.0 · 0.0 | 0.0 · 0.0 | 0.0 · 0.0 · 0.00 · 0.0 | 0.00 (0; 0) |
| bestias_crian | RG58r | 22.1 · 15.4 | 6.7 · 9.9 | 22.4 · 11.4 · 0.03 · 0.9 | 2.27 (2; 9) |
| bestias_crian | RG058r | 14.3 · 7.7 | 8.9 · 2.0 | 13.4 · 4.8 · 0.07 · 0.4 | 3.35 (3; 10) |
| bestias_crian | S58 | 436.7 · 274.6 | 131.4 · 133.8 | 494.9 · 33.0 · 1.70 · 132.1 | 1.23 (1; 5) |
| bestias_crian | S058 | 16.6 · 7.4 | 10.2 · 1.4 | 15.8 · 5.2 · 0.05 · 0.4 | 2.50 (3; 7) |
| bestias_crian | P58 | 51.3 · 41.9 | 13.4 · 25.0 | 49.0 · 23.1 · 0.30 · 16.5 | 2.52 (3; 7) |

### Dar la última comida (21 partidas por jugador y mundo; sumas)

| mundo | jugador | veces (a la hermana) | hambre propia: ≤60 · 60-80 · >80 | hambre de la otra: ≤60 · 60-80 · >80 | con hambre propia > 60: la otra ≤60 · 60-80 · >80 | hambre propia media · de la otra |
|---|---|---|---|---|---|---|
| abundancia | tonto | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| abundancia | recolector | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| abundancia | RG58r | 13 (7) | 13 · 0 · 0 | 6 · 7 · 0 | 0 · 0 · 0 | -0 · 31 |
| abundancia | RG058r | 16 (16) | 16 · 0 · 0 | 0 · 16 · 0 | 0 · 0 · 0 | 7 · 63 |
| abundancia | S58 | 1349 (667) | 1333 · 16 · 0 | 834 · 492 · 23 | 0 · 12 · 4 | 3 · 26 |
| abundancia | S058 | 13 (12) | 13 · 0 · 0 | 2 · 10 · 1 | 0 · 0 · 0 | -0 · 56 |
| abundancia | P58 | 81 (50) | 81 · 0 · 0 | 71 · 10 · 0 | 0 · 0 · 0 | -9 · 12 |
| normal | tonto | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| normal | recolector | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| normal | RG58r | 44 (32) | 44 · 0 · 0 | 11 · 30 · 3 | 0 · 0 · 0 | 6 · 46 |
| normal | RG058r | 55 (45) | 55 · 0 · 0 | 3 · 48 · 4 | 0 · 0 · 0 | 3 · 63 |
| normal | S58 | 1804 (907) | 1754 · 50 · 0 | 647 · 1047 · 110 | 1 · 36 · 13 | 13 · 43 |
| normal | S058 | 56 (50) | 56 · 0 · 0 | 1 · 49 · 6 | 0 · 0 · 0 | 9 · 65 |
| normal | P58 | 105 (71) | 104 · 1 · 0 | 59 · 44 · 2 | 0 · 1 · 0 | 4 · 30 |
| sequia | tonto | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| sequia | recolector | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| sequia | RG58r | 49 (45) | 49 · 0 · 0 | 5 · 42 · 2 | 0 · 0 · 0 | 15 · 58 |
| sequia | RG058r | 144 (124) | 144 · 0 · 0 | 0 · 126 · 18 | 0 · 0 · 0 | 10 · 69 |
| sequia | S58 | 2008 (958) | 1950 · 58 · 0 | 660 · 1233 · 115 | 0 · 41 · 17 | 14 · 45 |
| sequia | S058 | 203 (173) | 203 · 0 · 0 | 2 · 181 · 20 | 0 · 0 · 0 | 9 · 66 |
| sequia | P58 | 122 (89) | 121 · 1 · 0 | 49 · 65 · 8 | 0 · 1 · 0 | 10 · 43 |
| sequia_dura | tonto | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| sequia_dura | recolector | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| sequia_dura | RG58r | 91 (80) | 91 · 0 · 0 | 8 · 75 · 8 | 0 · 0 · 0 | 22 · 60 |
| sequia_dura | RG058r | 282 (231) | 282 · 0 · 0 | 0 · 237 · 45 | 0 · 0 · 0 | 12 · 70 |
| sequia_dura | S58 | 1412 (663) | 1324 · 88 · 0 | 469 · 816 · 127 | 0 · 63 · 25 | 18 · 46 |
| sequia_dura | S058 | 239 (172) | 239 · 0 · 0 | 5 · 206 · 28 | 0 · 0 · 0 | 8 · 67 |
| sequia_dura | P58 | 146 (117) | 145 · 1 · 0 | 45 · 90 · 11 | 0 · 1 · 0 | 16 · 46 |
| bestias_crian | tonto | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| bestias_crian | recolector | 0 (0) | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 | — · — |
| bestias_crian | RG58r | 99 (88) | 99 · 0 · 0 | 6 · 88 · 5 | 0 · 0 · 0 | 20 · 62 |
| bestias_crian | RG058r | 237 (206) | 237 · 0 · 0 | 4 · 216 · 17 | 0 · 0 · 0 | 10 · 65 |
| bestias_crian | S58 | 2123 (1083) | 2039 · 84 · 0 | 768 · 1232 · 123 | 0 · 68 · 16 | 15 · 43 |
| bestias_crian | S058 | 327 (283) | 327 · 0 · 0 | 7 · 284 · 36 | 0 · 0 · 0 | 9 · 66 |
| bestias_crian | P58 | 140 (106) | 140 · 0 · 0 | 37 · 99 · 4 | 0 · 0 · 0 | 12 · 47 |

### Las conductas (cierre_v46)

| mundo | jugador | con la bestia a la vista (fuera), con otra pegada | echadas · muertas | echan: con la hermana · con vecinas | tras perder a la hermana, pegada a una vecina: antes · 5 días después (casos) |
|---|---|---|---|---|---|
| abundancia | tonto | 3 % | 0 · 0 | 0 · 0 | — · — (0) |
| abundancia | recolector | 26 % | 0 · 0 | 0 · 0 | — · — (0) |
| abundancia | RG58r | 43 % | 4 · 0 | 3 · 1 | 26 % · 47 % (4) |
| abundancia | RG058r | 39 % | 1 · 0 | 1 · 0 | — · — (0) |
| abundancia | S58 | 75 % | 20 · 0 | 13 · 7 | 49 % · 72 % (4) |
| abundancia | S058 | 64 % | 7 · 0 | 7 · 0 | — · — (0) |
| abundancia | P58 | 30 % | 2 · 0 | 0 · 2 | 39 % · 49 % (4) |
| normal | tonto | 4 % | 0 · 0 | 0 · 0 | 3 % · 1 % (1) |
| normal | recolector | 26 % | 0 · 0 | 0 · 0 | 4 % · 4 % (3) |
| normal | RG58r | 41 % | 10 · 0 | 10 · 0 | 12 % · 28 % (6) |
| normal | RG058r | 26 % | 2 · 0 | 1 · 1 | 9 % · 13 % (1) |
| normal | S58 | 69 % | 13 · 0 | 8 · 5 | 45 % · 54 % (8) |
| normal | S058 | 49 % | 5 · 0 | 5 · 0 | — · — (0) |
| normal | P58 | 32 % | 11 · 0 | 10 · 1 | 23 % · 31 % (5) |
| sequia | tonto | 2 % | 0 · 0 | 0 · 0 | 3 % · 1 % (102) |
| sequia | recolector | 27 % | 0 · 0 | 0 · 0 | 4 % · 3 % (2) |
| sequia | RG58r | 34 % | 4 · 0 | 4 · 0 | 16 % · 27 % (25) |
| sequia | RG058r | 27 % | 0 · 0 | 0 · 0 | 5 % · 12 % (5) |
| sequia | S58 | 64 % | 12 · 0 | 9 · 3 | 40 % · 57 % (41) |
| sequia | S058 | 53 % | 10 · 0 | 10 · 0 | 9 % · 18 % (6) |
| sequia | P58 | 32 % | 5 · 0 | 3 · 2 | 18 % · 23 % (36) |
| sequia_dura | tonto | 2 % | 0 · 0 | 0 · 0 | 3 % · 1 % (101) |
| sequia_dura | recolector | 20 % | 0 · 0 | 0 · 0 | 6 % · 3 % (95) |
| sequia_dura | RG58r | 38 % | 5 · 0 | 2 · 3 | 13 % · 26 % (86) |
| sequia_dura | RG058r | 30 % | 5 · 0 | 5 · 0 | 7 % · 33 % (89) |
| sequia_dura | S58 | 60 % | 7 · 0 | 6 · 1 | 34 % · 42 % (84) |
| sequia_dura | S058 | 40 % | 2 · 0 | 2 · 0 | 7 % · 34 % (111) |
| sequia_dura | P58 | 38 % | 6 · 0 | 6 · 0 | 15 % · 26 % (83) |
| bestias_crian | tonto | 11 % | 0 · 0 | 0 · 0 | 3 % · 2 % (118) |
| bestias_crian | recolector | 26 % | 0 · 0 | 0 · 0 | 8 % · 6 % (51) |
| bestias_crian | RG58r | 33 % | 255 · 0 | 182 · 73 | 13 % · 21 % (56) |
| bestias_crian | RG058r | 23 % | 87 · 0 | 58 · 29 | 6 % · 21 % (44) |
| bestias_crian | S58 | 48 % | 148 · 0 | 100 · 48 | 36 % · 51 % (72) |
| bestias_crian | S058 | 32 % | 140 · 0 | 111 · 29 | 7 % · 20 % (38) |
| bestias_crian | P58 | 33 % | 225 · 0 | 143 · 82 | 18 % · 24 % (52) |

### Dormir fuera, lo que cuesta, y lo que creen al acabar (diag_v47, verdad_noche_v49)

| mundo | jugador | de lo dormido: su casa · otra casa · fuera | fuera: junto a la hermana · a una vecina · sola | dormidas fuera: golpes · robos de la bestia (por partida) | muertes de noche fuera | lo que creen al acabar de dormir fuera | lo que quita de verdad por noche fuera |
|---|---|---|---|---|---|---|---|
| abundancia | tonto | 100 % · 0 % · 0 % | 11 % · 5 % · 84 % | 0.00 · 0.00 | 0 | — | — |
| abundancia | RG58r | 86 % · 2 % · 12 % | 34 % · 9 % · 57 % | 1.82 · 1.62 | 2 | -0.943 | 1.08 (1365 noches) |
| abundancia | RG058r | 96 % · 1 % · 4 % | 51 % · 4 % · 44 % | 0.30 · 0.28 | 0 | -0.764 | 1.68 (143 noches) |
| abundancia | S58 | 39 % · 2 % · 59 % | 69 % · 14 % · 17 % | 3.62 · 3.05 | 5 | -0.697 | 0.61 (6300 noches) |
| abundancia | S058 | 96 % · 1 % · 4 % | 56 % · 4 % · 39 % | 0.20 · 0.23 | 0 | -0.740 | 0.32 (124 noches) |
| abundancia | P58 | 78 % · 3 % · 19 % | 39 % · 13 % · 48 % | 1.88 · 1.60 | 3 | -0.795 | 0.68 (1876 noches) |
| normal | tonto | 100 % · 0 % · 0 % | 17 % · 17 % · 67 % | 0.05 · 0.05 | 0 | — | — |
| normal | RG58r | 84 % · 2 % · 14 % | 35 % · 8 % · 58 % | 1.55 · 1.32 | 5 | -0.981 | 1.15 (1565 noches) |
| normal | RG058r | 95 % · 1 % · 5 % | 38 % · 5 % · 57 % | 0.53 · 0.25 | 0 | -0.916 | 0.77 (260 noches) |
| normal | S58 | 51 % · 3 % · 47 % | 60 % · 16 % · 24 % | 3.23 · 2.30 | 5 | -0.923 | 0.73 (4752 noches) |
| normal | S058 | 95 % · 1 % · 4 % | 46 % · 4 % · 50 % | 0.28 · 0.25 | 0 | -0.861 | 0.51 (234 noches) |
| normal | P58 | 79 % · 3 % · 18 % | 34 % · 10 % · 56 % | 2.08 · 1.48 | 3 | -1.212 | 0.91 (1812 noches) |
| sequia | tonto | 100 % · 0 % · 0 % | 0 % · 14 % · 86 % | 0.00 · 0.00 | 0 | — | — |
| sequia | RG58r | 82 % · 2 % · 16 % | 37 % · 9 % · 54 % | 1.57 · 1.30 | 12 | -1.399 | 0.95 (1689 noches) |
| sequia | RG058r | 95 % · 1 % · 5 % | 35 % · 5 % · 60 % | 0.60 · 0.40 | 8 | -1.156 | 1.18 (306 noches) |
| sequia | S58 | 38 % · 2 % · 60 % | 66 % · 17 % · 17 % | 3.90 · 2.58 | 28 | -1.228 | 0.71 (5685 noches) |
| sequia | S058 | 95 % · 1 % · 4 % | 41 % · 4 % · 55 % | 0.55 · 0.30 | 3 | -1.294 | 1.60 (275 noches) |
| sequia | P58 | 77 % · 3 % · 20 % | 35 % · 12 % · 53 % | 2.02 · 1.35 | 19 | -1.501 | 0.97 (1849 noches) |
| sequia_dura | tonto | 100 % · 0 % · 0 % | 0 % · 0 % · 100 % | 0.00 · 0.00 | 0 | — | — |
| sequia_dura | RG58r | 72 % · 2 % · 26 % | 37 % · 18 % · 44 % | 1.55 · 1.30 | 49 | -2.365 | 0.80 (1848 noches) |
| sequia_dura | RG058r | 91 % · 1 % · 8 % | 22 % · 15 % · 63 % | 0.75 · 0.42 | 36 | -2.879 | 1.06 (492 noches) |
| sequia_dura | S58 | 36 % · 1 % · 62 % | 58 % · 26 % · 15 % | 2.83 · 1.48 | 63 | -2.330 | 0.87 (3938 noches) |
| sequia_dura | S058 | 86 % · 2 % · 12 % | 22 % · 29 % · 49 % | 0.70 · 0.30 | 52 | -3.026 | 1.10 (656 noches) |
| sequia_dura | P58 | 75 % · 3 % · 22 % | 35 % · 15 % · 50 % | 1.30 · 0.95 | 45 | -2.150 | 0.55 (1541 noches) |
| bestias_crian | tonto | 100 % · 0 % · 0 % | 13 % · 0 % · 87 % | 0.00 · 0.00 | 0 | — | — |
| bestias_crian | RG58r | 80 % · 3 % · 17 % | 39 % · 7 % · 54 % | 2.90 · 2.33 | 12 | -1.605 | 1.12 (1788 noches) |
| bestias_crian | RG058r | 94 % · 1 % · 5 % | 28 % · 5 % · 67 % | 0.68 · 0.33 | 5 | -1.239 | 1.50 (374 noches) |
| bestias_crian | S58 | 43 % · 2 % · 55 % | 65 % · 17 % · 18 % | 4.78 · 3.12 | 24 | -1.558 | 1.01 (4769 noches) |
| bestias_crian | S058 | 94 % · 1 % · 5 % | 35 % · 5 % · 60 % | 0.60 · 0.40 | 6 | -1.021 | 1.26 (348 noches) |
| bestias_crian | P58 | 77 % · 3 % · 21 % | 43 % · 8 % · 49 % | 3.12 · 2.20 | 13 | -1.548 | 1.16 (1995 noches) |

### Los empujones (diag_v47)

| mundo | jugador | por partida | a la hermana | la empujada lleva comida | gana la que empuja |
|---|---|---|---|---|---|
| abundancia | RG58r | 241 | 4 % | 97 % | 90 % |
| abundancia | RG058r | 59 | 33 % | 91 % | 77 % |
| abundancia | S58 | 582 | 2 % | 98 % | 91 % |
| abundancia | S058 | 53 | 43 % | 85 % | 76 % |
| abundancia | P58 | 397 | 2 % | 98 % | 89 % |
| normal | RG58r | 265 | 4 % | 97 % | 88 % |
| normal | RG058r | 72 | 30 % | 91 % | 79 % |
| normal | S58 | 532 | 2 % | 97 % | 89 % |
| normal | S058 | 67 | 34 % | 90 % | 79 % |
| normal | P58 | 413 | 2 % | 98 % | 88 % |
| sequia | RG58r | 238 | 4 % | 97 % | 87 % |
| sequia | RG058r | 65 | 27 % | 91 % | 80 % |
| sequia | S58 | 479 | 2 % | 98 % | 90 % |
| sequia | S058 | 63 | 35 % | 87 % | 77 % |
| sequia | P58 | 352 | 2 % | 97 % | 86 % |
| sequia_dura | RG58r | 133 | 5 % | 95 % | 85 % |
| sequia_dura | RG058r | 41 | 36 % | 79 % | 69 % |
| sequia_dura | S58 | 194 | 5 % | 94 % | 88 % |
| sequia_dura | S058 | 35 | 38 % | 79 % | 68 % |
| sequia_dura | P58 | 181 | 4 % | 96 % | 87 % |
| bestias_crian | RG58r | 219 | 4 % | 97 % | 87 % |
| bestias_crian | RG058r | 61 | 34 % | 85 % | 77 % |
| bestias_crian | S58 | 391 | 3 % | 97 % | 89 % |
| bestias_crian | S058 | 59 | 37 % | 82 % | 74 % |
| bestias_crian | P58 | 304 | 3 % | 97 % | 89 % |

### El valor de quien roba, del día del robo al siguiente (diag_robos_v47; cambio medio del radar; control: el de las demás)

| mundo | clase | robos | la robada: cuerpo · recursos · vínculo | control | las que lo ven | control |
|---|---|---|---|---|---|---|
| abundancia | RG58r | 7832 | +0.0000 · -0.0623 · +0.0108 | +0.0000 · +0.0006 · -0.0034 | +0.0000 · -0.0372 · +0.0195 | +0.0000 · -0.0053 · +0.0056 |
| abundancia | RG058r | 1632 | +0.0000 · -0.1855 · +0.0272 | +0.0000 · +0.0026 · +0.0011 | +0.0000 · -0.0744 · +0.0228 | +0.0000 · -0.0024 · +0.0090 |
| abundancia | S58 | 17954 | +0.0000 · -0.0025 · +0.0170 | +0.0000 · +0.0142 · +0.0001 | +0.0001 · -0.0265 · +0.0175 | +0.0000 · +0.0028 · +0.0065 |
| abundancia | S058 | 1399 | +0.0001 · -0.1704 · +0.0345 | +0.0000 · -0.0007 · +0.0016 | +0.0000 · -0.0797 · +0.0305 | +0.0000 · -0.0037 · +0.0110 |
| abundancia | P58 | 12857 | +0.0001 · -0.0456 · +0.0085 | +0.0000 · +0.0010 · -0.0042 | +0.0001 · -0.0370 · +0.0130 | +0.0000 · -0.0088 · +0.0010 |
| normal | RG58r | 8319 | +0.0000 · -0.0597 · +0.0103 | -0.0000 · +0.0000 · -0.0037 | +0.0000 · -0.0353 · +0.0176 | +0.0000 · -0.0064 · +0.0035 |
| normal | RG058r | 2024 | -0.0000 · -0.1674 · +0.0206 | -0.0000 · +0.0012 · +0.0005 | +0.0000 · -0.0578 · +0.0196 | +0.0000 · -0.0024 · +0.0044 |
| normal | S58 | 15504 | +0.0000 · +0.0088 · +0.0159 | -0.0000 · +0.0148 · -0.0014 | -0.0000 · -0.0352 · +0.0178 | -0.0000 · -0.0008 · +0.0055 |
| normal | S058 | 1844 | +0.0000 · -0.1646 · +0.0278 | +0.0000 · -0.0007 · +0.0010 | +0.0000 · -0.0668 · +0.0216 | +0.0000 · -0.0027 · +0.0057 |
| normal | P58 | 12872 | +0.0001 · -0.0412 · +0.0085 | +0.0000 · +0.0022 · -0.0044 | +0.0001 · -0.0276 · +0.0137 | +0.0000 · -0.0037 · +0.0010 |
| sequia | RG58r | 7348 | +0.0000 · -0.0574 · +0.0088 | +0.0000 · +0.0014 · -0.0049 | +0.0000 · -0.0354 · +0.0193 | +0.0000 · -0.0047 · +0.0045 |
| sequia | RG058r | 1819 | -0.0000 · -0.1716 · +0.0237 | -0.0001 · +0.0012 · +0.0005 | +0.0000 · -0.0599 · +0.0200 | +0.0000 · -0.0007 · +0.0072 |
| sequia | S58 | 13722 | +0.0000 · +0.0105 · +0.0187 | +0.0000 · +0.0194 · +0.0002 | +0.0001 · -0.0281 · +0.0200 | +0.0000 · +0.0032 · +0.0076 |
| sequia | S058 | 1602 | +0.0001 · -0.1629 · +0.0294 | +0.0000 · -0.0017 · +0.0008 | +0.0000 · -0.0687 · +0.0248 | +0.0000 · -0.0027 · +0.0078 |
| sequia | P58 | 10675 | +0.0001 · -0.0399 · +0.0063 | +0.0000 · +0.0011 · -0.0060 | +0.0001 · -0.0374 · +0.0135 | +0.0000 · -0.0093 · -0.0006 |
| sequia_dura | RG58r | 3860 | -0.0000 · -0.0671 · +0.0058 | -0.0000 · +0.0001 · -0.0125 | +0.0000 · -0.0471 · +0.0264 | -0.0000 · -0.0086 · +0.0023 |
| sequia_dura | RG058r | 881 | +0.0001 · -0.2124 · +0.0467 | +0.0000 · -0.0003 · +0.0005 | +0.0000 · -0.0953 · +0.0333 | +0.0000 · -0.0057 · +0.0118 |
| sequia_dura | S58 | 5252 | +0.0000 · +0.0165 · +0.0186 | +0.0000 · +0.0297 · +0.0035 | -0.0001 · -0.0578 · +0.0329 | -0.0001 · -0.0021 · +0.0163 |
| sequia_dura | S058 | 726 | -0.0001 · -0.2079 · +0.0612 | +0.0000 · +0.0008 · +0.0022 | +0.0001 · -0.0949 · +0.0434 | +0.0000 · -0.0041 · +0.0139 |
| sequia_dura | P58 | 5420 | +0.0003 · -0.0491 · +0.0085 | +0.0001 · +0.0026 · -0.0110 | +0.0002 · -0.0448 · +0.0225 | +0.0001 · -0.0092 · -0.0004 |
| bestias_crian | RG58r | 6607 | +0.0001 · -0.0602 · +0.0086 | +0.0000 · +0.0025 · -0.0049 | +0.0001 · -0.0321 · +0.0205 | +0.0001 · -0.0018 · +0.0049 |
| bestias_crian | RG058r | 1525 | -0.0002 · -0.1846 · +0.0289 | -0.0000 · +0.0010 · +0.0009 | +0.0001 · -0.0648 · +0.0272 | +0.0000 · -0.0008 · +0.0074 |
| bestias_crian | S58 | 11088 | +0.0001 · +0.0032 · +0.0179 | +0.0000 · +0.0134 · +0.0001 | +0.0001 · -0.0298 · +0.0232 | +0.0001 · -0.0028 · +0.0088 |
| bestias_crian | S058 | 1382 | -0.0001 · -0.1641 · +0.0301 | +0.0000 · +0.0029 · +0.0006 | +0.0001 · -0.0619 · +0.0295 | +0.0001 · -0.0021 · +0.0097 |
| bestias_crian | P58 | 9372 | +0.0002 · -0.0372 · +0.0048 | +0.0001 · +0.0034 · -0.0075 | +0.0002 · -0.0289 · +0.0147 | +0.0001 · -0.0015 · -0.0020 |

### El árbol de fruta dulce (21 partidas por jugador y mundo)

| mundo | jugador | apariciones · frutas puestas | lo descubren (criaturas; día mediano) | viajes con recogida (criaturas distintas) | solas · acompañadas | frutas cogidas · perdidas sin coger | vuelven antes de la noche · de noche · no vuelven | la bestia pasa por el árbol · le quita la dulce | se comen la dulce: en el árbol · en casa o cerca · en otro sitio | la dan (a la hermana · a una vecina) | la guardan en la despensa |
|---|---|---|---|---|---|---|---|---|---|---|---|
| abundancia | tonto | 201 · 4020 | 6 (28) | 0 (0) | 0 · 0 | 0 · 4020 | 0 · 0 · 0 | 621 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| abundancia | recolector | 201 · 4020 | 105 (14) | 909 (92) | 640 · 269 | 902 · 3118 | 696 · 213 · 0 | 621 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| abundancia | RG58r | 201 · 4020 | 9 (16) | 42 (6) | 9 · 33 | 42 · 3978 | 20 · 0 · 22 | 620 · 2 | 15 · 4 · 5 | 0 · 4 | 0 |
| abundancia | RG058r | 201 · 4020 | 7 (17) | 8 (2) | 8 · 0 | 8 · 4012 | 0 · 8 · 0 | 620 · 0 | 1 · 5 · 0 | 0 · 0 | 0 |
| abundancia | S58 | 201 · 4020 | 22 (25) | 121 (15) | 15 · 106 | 117 · 3903 | 25 · 96 · 0 | 613 · 6 | 52 · 17 · 17 | 136 · 52 | — |
| abundancia | S058 | 201 · 4020 | 12 (14) | 25 (4) | 8 · 17 | 25 · 3995 | 0 · 25 · 0 | 619 · 1 | 3 · 7 · 2 | 1 · 0 | — |
| abundancia | P58 | 201 · 4020 | 14 (21) | 37 (7) | 22 · 15 | 37 · 3983 | 9 · 14 · 14 | 621 · 1 | 8 · 9 · 6 | 1 · 0 | — |
| normal | tonto | 201 · 4020 | 6 (19) | 0 (0) | 0 · 0 | 0 · 4020 | 0 · 0 · 0 | 621 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| normal | recolector | 201 · 4020 | 115 (13) | 965 (106) | 656 · 309 | 957 · 3063 | 755 · 210 · 0 | 621 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| normal | RG58r | 201 · 4020 | 29 (22) | 187 (23) | 78 · 109 | 187 · 3833 | 124 · 63 · 0 | 618 · 2 | 54 · 42 · 14 | 5 · 0 | 0 |
| normal | RG058r | 201 · 4020 | 27 (23) | 79 (15) | 70 · 9 | 79 · 3941 | 41 · 38 · 0 | 620 · 1 | 12 · 38 · 11 | 0 · 0 | 0 |
| normal | S58 | 201 · 4020 | 7 (10) | 1 (1) | 1 · 0 | 1 · 4019 | 1 · 0 · 0 | 614 · 0 | 0 · 0 · 1 | 0 · 0 | — |
| normal | S058 | 201 · 4020 | 30 (25) | 104 (17) | 53 · 51 | 104 · 3916 | 65 · 39 · 0 | 620 · 4 | 27 · 31 · 16 | 1 · 0 | — |
| normal | P58 | 201 · 4020 | 29 (19) | 211 (23) | 80 · 131 | 211 · 3809 | 63 · 148 · 0 | 616 · 6 | 86 · 46 · 20 | 9 · 5 | — |
| sequia | tonto | 201 · 4020 | 4 (37) | 0 (0) | 0 · 0 | 0 · 4020 | 0 · 0 · 0 | 621 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| sequia | recolector | 201 · 4020 | 106 (14) | 899 (97) | 620 · 279 | 887 · 3133 | 700 · 199 · 0 | 621 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| sequia | RG58r | 201 · 4020 | 31 (18) | 179 (24) | 81 · 98 | 179 · 3841 | 78 · 101 · 0 | 618 · 4 | 53 · 40 · 26 | 3 · 2 | 13 |
| sequia | RG058r | 201 · 4020 | 36 (20) | 143 (24) | 80 · 63 | 143 · 3877 | 78 · 61 · 4 | 621 · 3 | 36 · 57 · 18 | 3 · 0 | 24 |
| sequia | S58 | 201 · 4020 | 19 (16) | 98 (15) | 22 · 76 | 98 · 3922 | 22 · 60 · 16 | 616 · 4 | 49 · 8 · 13 | 46 · 4 | — |
| sequia | S058 | 201 · 4020 | 27 (15) | 103 (18) | 44 · 59 | 104 · 3916 | 43 · 60 · 0 | 620 · 2 | 38 · 37 · 11 | 1 · 0 | — |
| sequia | P58 | 201 · 4020 | 31 (17) | 155 (23) | 100 · 55 | 155 · 3865 | 64 · 82 · 9 | 620 · 4 | 50 · 36 · 31 | 7 · 2 | — |
| sequia_dura | tonto | 192 · 3840 | 1 (9) | 0 (0) | 0 · 0 | 20 · 3820 | 0 · 0 · 0 | 594 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| sequia_dura | recolector | 201 · 4020 | 95 (12) | 852 (77) | 662 · 190 | 849 · 3171 | 677 · 175 · 0 | 621 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| sequia_dura | RG58r | 201 · 4020 | 18 (14) | 140 (18) | 76 · 64 | 140 · 3880 | 57 · 67 · 16 | 617 · 2 | 63 · 33 · 19 | 2 · 3 | 5 |
| sequia_dura | RG058r | 201 · 4020 | 24 (11) | 197 (20) | 123 · 74 | 197 · 3823 | 108 · 84 · 5 | 618 · 5 | 61 · 64 · 24 | 3 · 4 | 43 |
| sequia_dura | S58 | 201 · 4020 | 7 (21) | 54 (6) | 1 · 53 | 54 · 3966 | 0 · 43 · 11 | 619 · 5 | 34 · 9 · 0 | 59 · 0 | — |
| sequia_dura | S058 | 201 · 4020 | 20 (6) | 119 (16) | 55 · 64 | 119 · 3901 | 36 · 83 · 0 | 620 · 1 | 42 · 29 · 20 | 0 · 0 | — |
| sequia_dura | P58 | 201 · 4020 | 16 (12) | 124 (13) | 72 · 52 | 124 · 3896 | 22 · 90 · 12 | 620 · 7 | 42 · 46 · 20 | 8 · 4 | — |
| bestias_crian | tonto | 201 · 4020 | 9 (13) | 0 (0) | 0 · 0 | 20 · 4000 | 0 · 0 · 0 | 666 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| bestias_crian | recolector | 201 · 4020 | 108 (13) | 942 (98) | 684 · 258 | 930 · 3090 | 697 · 245 · 0 | 666 · 0 | 0 · 0 · 0 | 0 · 0 | — |
| bestias_crian | RG58r | 201 · 4020 | 48 (23) | 258 (36) | 103 · 155 | 258 · 3762 | 112 · 135 · 11 | 634 · 19 | 89 · 51 · 24 | 1 · 0 | 20 |
| bestias_crian | RG058r | 201 · 4020 | 41 (23) | 244 (33) | 159 · 85 | 245 · 3775 | 62 · 182 · 0 | 662 · 7 | 57 · 86 · 8 | 2 · 1 | 30 |
| bestias_crian | S58 | 201 · 4020 | 19 (21) | 119 (16) | 27 · 92 | 116 · 3904 | 19 · 88 · 12 | 636 · 5 | 47 · 15 · 20 | 89 · 6 | — |
| bestias_crian | S058 | 201 · 4020 | 41 (24) | 241 (32) | 153 · 88 | 241 · 3779 | 66 · 175 · 0 | 657 · 8 | 55 · 62 · 16 | 2 · 0 | — |
| bestias_crian | P58 | 201 · 4020 | 28 (26) | 261 (23) | 140 · 121 | 260 · 3760 | 82 · 165 · 14 | 628 · 13 | 86 · 64 · 35 | 10 · 2 | — |

## Anexo B. Las medidas sin predicción, M1–M6 (`medidas_v3.md`)

Partidas leídas: criaturas 1000 (RG58r 200); con los jugadores de base, 1400.

### M1. Felicidad funcional (turnos despierta con los tres balances > 0)

| mundo | clase | la aldea (media de las ocho): media · mediana de las partidas | la peor parada: media · mediana | balances medios: cuerpo · recursos · vínculo |
|---|---|---|---|---|
| abundancia | RG58r | 76 % · 76 % | 56 % · 56 % | +0.36 · +0.97 · +0.42 |
| abundancia | RG058r | 0 % · 0 % | 0 % · 0 % | -0.36 · -0.41 · -0.22 |
| abundancia | S58 | 65 % · 66 % | 50 % · 53 % | +0.29 · +0.66 · +0.57 |
| abundancia | S058 | 0 % · 0 % | 0 % · 0 % | -0.32 · -0.42 · -0.20 |
| abundancia | P58 | 63 % · 64 % | 48 % · 50 % | +0.21 · +0.87 · +0.38 |
| normal | RG58r | 62 % · 62 % | 39 % · 40 % | +0.23 · +0.65 · +0.32 |
| normal | RG058r | 0 % · 0 % | 0 % · 0 % | -0.46 · -0.53 · -0.26 |
| normal | S58 | 47 % · 46 % | 31 % · 31 % | +0.10 · +0.18 · +0.43 |
| normal | S058 | 0 % · 0 % | 0 % · 0 % | -0.40 · -0.55 · -0.24 |
| normal | P58 | 50 % · 50 % | 32 % · 35 % | +0.08 · +0.49 · +0.29 |
| sequia | RG58r | 56 % · 57 % | 30 % · 32 % | +0.12 · +0.51 · +0.27 |
| sequia | RG058r | 0 % · 0 % | 0 % · 0 % | -0.49 · -0.57 · -0.28 |
| sequia | S58 | 43 % · 43 % | 23 % · 22 % | -0.04 · +0.12 · +0.35 |
| sequia | S058 | 0 % · 0 % | 0 % · 0 % | -0.45 · -0.59 · -0.26 |
| sequia | P58 | 45 % · 46 % | 23 % · 21 % | -0.03 · +0.40 · +0.23 |
| sequia_dura | RG58r | 36 % · 36 % | 14 % · 12 % | -0.31 · +0.09 · +0.05 |
| sequia_dura | RG058r | 0 % · 0 % | 0 % · 0 % | -0.93 · -0.82 · -0.46 |
| sequia_dura | S58 | 30 % · 31 % | 12 % · 10 % | -0.40 · -0.17 · +0.12 |
| sequia_dura | S058 | 0 % · 0 % | 0 % · 0 % | -0.97 · -0.85 · -0.48 |
| sequia_dura | P58 | 32 % · 31 % | 12 % · 11 % | -0.38 · +0.05 · +0.05 |
| bestias_crian | RG58r | 41 % · 42 % | 21 % · 19 % | -0.12 · +0.26 · +0.17 |
| bestias_crian | RG058r | 0 % · 0 % | 0 % · 0 % | -0.74 · -0.74 · -0.37 |
| bestias_crian | S58 | 30 % · 29 % | 14 % · 14 % | -0.30 · -0.11 · +0.23 |
| bestias_crian | S058 | 0 % · 0 % | 0 % · 0 % | -0.71 · -0.75 · -0.35 |
| bestias_crian | P58 | 33 % · 32 % | 15 % · 14 % | -0.24 · +0.14 · +0.15 |

### M2. Momentos hygge (RG58r): al anochecer o de noche, en su casa con la hermana dentro, sin estar flaca, sin la bestia a la vista y con los tres balances > 0

| mundo | turnos hygge por criatura y noche | noches (de cada criatura) con al menos uno |
|---|---|---|
| abundancia | 84.6 | 71 % |
| normal | 68.3 | 59 % |
| sequia | 57.5 | 51 % |
| sequia_dura | 23.7 | 24 % |
| bestias_crian | 42.3 | 41 % |

### M3. Lo que siente en cada sitio según sus recuerdos (RG58r; recuerdos vividos, pesados por la intensidad): efecto en cuerpo · efecto en recursos · importancia (cuerpo)

| sitio | abundancia | normal | sequia | sequia_dura | bestias_crian |
|---|---|---|---|---|---|
| aldea, dia | -0.00 · +0.73 · -0.000 | -0.00 · +0.52 · -0.000 | -0.00 · +0.52 · -0.000 | -0.00 · +0.35 · +0.001 | -0.01 · +0.37 · +0.001 |
| aldea, noche | -0.01 · +0.40 · +0.003 | -0.01 · +0.24 · +0.001 | -0.01 · +0.29 · +0.002 | -0.01 · +0.12 · +0.007 | -0.02 · +0.14 · +0.002 |
| bosque, dia | -0.00 · +0.67 · -0.000 | -0.00 · +0.51 · -0.000 | -0.00 · +0.46 · -0.000 | -0.00 · +0.35 · +0.002 | -0.01 · +0.38 · +0.001 |
| bosque, noche | -0.01 · +0.13 · +0.002 | -0.01 · +0.11 · +0.003 | -0.01 · +0.06 · +0.004 | -0.01 · +0.06 · +0.016 | -0.03 · +0.06 · +0.003 |
| camino, dia | +0.00 · +0.68 · -0.000 | -0.00 · +0.52 · +0.000 | -0.00 · +0.44 · +0.002 | -0.00 · +0.35 · +0.014 | -0.03 · +0.43 · +0.007 |
| camino, noche | -0.02 · +0.08 · +0.028 | -0.02 · +0.12 · +0.007 | -0.03 · +0.06 · +0.029 | -0.07 · +0.17 · +0.098 | -0.08 · +0.10 · +0.024 |
| casa, dia | -0.00 · +0.67 · +0.000 | -0.00 · +0.44 · -0.000 | -0.00 · +0.47 · +0.001 | -0.00 · +0.27 · +0.005 | -0.00 · +0.30 · +0.003 |
| casa, noche | -0.00 · +0.11 · -0.001 | -0.00 · +0.06 · -0.001 | -0.00 · +0.08 · -0.002 | -0.00 · +0.04 · -0.002 | -0.00 · +0.03 · -0.006 |
| huerto, dia | -0.00 · +0.74 · +0.000 | -0.00 · +0.58 · -0.000 | -0.00 · +0.54 · +0.001 | -0.00 · +0.37 · +0.004 | -0.01 · +0.50 · +0.003 |
| huerto, noche | -0.02 · +0.12 · +0.002 | -0.03 · +0.14 · +0.003 | -0.04 · +0.06 · +0.012 | -0.04 · +0.02 · +0.019 | -0.03 · +0.07 · +0.012 |
| salvaje, dia | -0.06 · +0.63 · +0.007 | -0.06 · +0.52 · +0.009 | -0.07 · +0.49 · +0.010 | -0.07 · +0.53 · +0.024 | -0.09 · +0.43 · +0.014 |
| salvaje, noche | -0.17 · +0.15 · +0.032 | -0.12 · +0.03 · +0.016 | -0.15 · +0.03 · +0.024 | -0.08 · +0.03 · +0.039 | -0.07 · +0.01 · +0.006 |

### M4. Los tres mapas del valle (figuras)

![mapas_abundancia.png](salida/figuras_v3/mapas_abundancia.png)
![mapas_normal.png](salida/figuras_v3/mapas_normal.png)
![mapas_sequia.png](salida/figuras_v3/mapas_sequia.png)
![mapas_sequia_dura.png](salida/figuras_v3/mapas_sequia_dura.png)
![mapas_bestias_crian.png](salida/figuras_v3/mapas_bestias_crian.png)

### M5. El huerto: veces que se trabaja una planta, por partida

| mundo | RG58r | RG058r | S58 | S058 | P58 | tonto | recolector |
|---|---|---|---|---|---|---|---|
| abundancia | 6344 | 6432 | 5638 | 6429 | 6298 | 3512 | 0 |
| normal | 6372 | 6447 | 5819 | 6446 | 6380 | 5527 | 0 |
| sequia | 6336 | 6443 | 5548 | 6438 | 6259 | 3953 | 0 |
| sequia_dura | 5287 | 5568 | 4466 | 5014 | 5424 | 3293 | 0 |
| bestias_crian | 6290 | 6397 | 5403 | 6355 | 6257 | 4750 | 0 |

**Quién trabaja, en RG58r** (de lo trabajado en cada partida): la criatura que más · las dos de la casa que más

| mundo | la que más | la casa que más |
|---|---|---|
| abundancia | 17 % | 30 % |
| normal | 17 % | 29 % |
| sequia | 17 % | 30 % |
| sequia_dura | 28 % | 40 % |
| bestias_crian | 19 % | 31 % |

### M6. El perdón (RG58r): días hasta que la ladrona vuelve a valer en el radar de la robada lo que valía el día del robo

| mundo | robos de vecinas | días: mediana (de los que vuelven) | sin volver |
|---|---|---|---|
| abundancia | 7673 | 1 | 45 % |
| normal | 8253 | 1 | 46 % |
| sequia | 7174 | 1 | 46 % |
| sequia_dura | 3529 | 1 | 49 % |
| bestias_crian | 6447 | 1 | 45 % |

## Anexo C. Las medidas añadidas después de sellar (`anadidas_v3.md` y `duelo_soledad_v3.md`)

*Medidas añadidas después de sellar, sin predicción.*

### A1. Dónde se dan regalos, junto al bienestar (RG58r)

![regalos_abundancia.png](salida/figuras_v3/regalos_abundancia.png)
![regalos_normal.png](salida/figuras_v3/regalos_normal.png)
![regalos_sequia.png](salida/figuras_v3/regalos_sequia.png)
![regalos_sequia_dura.png](salida/figuras_v3/regalos_sequia_dura.png)
![regalos_bestias_crian.png](salida/figuras_v3/regalos_bestias_crian.png)

### A2. La que pierde a su hermana frente a las que la conservan (RG58r; 5 días antes y 5 después)

| mundo | grupo | casos | felicidad funcional: antes · después | felicidad en casa: antes · después | duerme en casa: antes · después | pegada a una vecina, de día: antes · después | de noche: antes · después | días hasta recuperarse: mediana de las que vuelven (no vuelven: de cuántas) |
|---|---|---|---|---|---|---|---|---|
| abundancia | pierde a la hermana | 5 | 64 % · 7 % | 61 % · 0 % | 64 % · 76 % | 30 % · 48 % | 12 % · 32 % | 14 (no vuelven 3 de 5) |
| abundancia | la conserva (control) | 30 | 78 % · 84 % | 80 % · 88 % | 84 % · 86 % | 26 % · 21 % | 11 % · 12 % | — |
| normal | pierde a la hermana | 6 | 46 % · 0 % | 57 % · 0 % | 70 % · 70 % | 17 % · 28 % | 5 % · 27 % | — (no vuelven 6 de 6) |
| normal | la conserva (control) | 36 | 70 % · 74 % | 81 % · 74 % | 84 % · 79 % | 15 % · 16 % | 10 % · 13 % | — |
| sequia | pierde a la hermana | 26 | 34 % · 2 % | 48 % · 0 % | 73 % · 64 % | 18 % · 27 % | 11 % · 27 % | 10 (no vuelven 21 de 26) |
| sequia | la conserva (control) | 146 | 45 % · 58 % | 52 % · 59 % | 78 % · 74 % | 18 % · 16 % | 11 % · 13 % | — |
| sequia_dura | pierde a la hermana | 76 | 20 % · 0 % | 28 % · 0 % | 83 % · 75 % | 15 % · 31 % | 9 % · 20 % | 12 (no vuelven 51 de 76) |
| sequia_dura | la conserva (control) | 150 | 27 % · 23 % | 29 % · 17 % | 76 % · 72 % | 18 % · 16 % | 13 % · 13 % | — |
| bestias_crian | pierde a la hermana | 54 | 28 % · 0 % | 37 % · 0 % | 77 % · 75 % | 14 % · 22 % | 11 % · 21 % | 9 (no vuelven 53 de 54) |
| bestias_crian | la conserva (control) | 248 | 39 % · 43 % | 48 % · 50 % | 81 % · 78 % | 14 % · 12 % | 10 % · 11 % | — |
| todos | pierde a la hermana | 167 | 27 % · 1 % | 36 % · 0 % | 78 % · 73 % | 16 % · 28 % | 10 % · 22 % | 11 (no vuelven 134 de 167) |
| todos | la conserva (control) | 610 | 41 % · 45 % | 48 % · 47 % | 79 % · 76 % | 17 % · 15 % | 11 % · 12 % | — |

### A3. Cuántas opciones compara la foto de RG50r en cada decisión (registro de la foto del prompt 101, 9 partidas)

- **Opciones por decisión:** media 17.1, mediana 18, máximo 36 (612178 decisiones).
- **Cada cuántos turnos decide una criatura** (entre dos decisiones suyas que salen de la foto): media 1.6, mediana 1; decide en el turno siguiente el 91 % de las veces.
- **De qué tipo son las opciones** (por decisión, de media): ir_matorral 4.03, mover 3.00, dejar 1.24, quedarse 1.00, empujar 0.93, golpear 0.93, dar 0.80, ir_frontera 0.76, ir_bosque 0.65, ir_objeto 0.59, ir_botin 0.59, ir_casa 0.56, dormir 0.46, comer 0.41, ir_pareja 0.37, ir_vecina 0.33, trabajar_planta 0.23, coger 0.11, trabajar 0.09, ir_llamada 0.06.

| mundo | decisiones | opciones: media · mediana · máximo | turnos entre decisiones: media · mediana |
|---|---|---|---|
| abundancia | 248243 | 17.1 · 18 · 36 | 1.5 · 1 |
| sequia | 224399 | 17.0 · 18 · 36 | 1.6 · 1 |
| sequia_dura | 139536 | 17.4 · 18 · 36 | 1.6 · 1 |

### A4. El duelo y la soledad, por mundo

*Medida añadida después de sellar, sin predicción.*

Partidas vueltas a jugar: 105, idénticas a las del experimento: 105 (solo cuentan esas).

Duelo = S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO; soledad = S-SOLEDAD (todos sus turnos despierta; «en casa», los de su casa); compañía = S-COMPANIA (lo lejos que está la hermana viva; al morir ella deja de calcularse). Medias por turno despierta. «Vuelve»: el primer día cuya media queda a una décima o menos de la subida.

Desde su peor día de los 5 después: «a la mitad», el primer día cuya media queda a la mitad de la subida o menos; «vuelve», a una décima o menos (el duelo baja hacia un suelo, DUELO_SUELO, no hacia cero). Días contados desde la muerte.

| mundo | grupo | señal | casos | antes | día después | peor de los 5 días | subida (pico − antes) | sube en | peor día: mediana | a la mitad: mediana de días (llegan / suben) | vuelve: mediana de días (vuelven / suben) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| abundancia | pierde a la hermana | duelo | 5 | 0.000 | 1.425 | 1.504 | 1.504 | 5 | 1 | 5 (3 / 5) | — (0 / 5) |
| abundancia | pierde a la hermana | soledad | 5 | 0.054 | 0.383 | 0.461 | 0.407 | 5 | 3 | 7 (2 / 5) | — (0 / 5) |
| abundancia | pierde a la hermana | soledad en casa | 5 | 0.049 | 0.500 | 0.500 | 0.451 | 5 | 1 | 6 (3 / 5) | — (0 / 5) |
| abundancia | pierde a la hermana | falta de la hermana viva (compañía) | 5 | 0.025 | 0.001 | 0.001 | -0.023 | 0 | — | — (0 / 0) | — (0 / 0) |
| abundancia | la conserva | duelo | 30 | 0.000 | 0.096 | 0.096 | 0.096 | 7 | 1 | 3 (5 / 7) | — (0 / 7) |
| abundancia | la conserva | soledad | 30 | 0.009 | 0.004 | 0.043 | 0.034 | 18 | 2 | 3 (16 / 18) | 3 (16 / 18) |
| abundancia | la conserva | soledad en casa | 30 | 0.002 | 0.003 | 0.013 | 0.011 | 16 | 3 | 4 (15 / 16) | 4 (15 / 16) |
| abundancia | la conserva | falta de la hermana viva (compañía) | 30 | 0.013 | 0.008 | 0.023 | 0.010 | 19 | 3 | 4 (17 / 19) | 4 (17 / 19) |
| normal | pierde a la hermana | duelo | 6 | 0.000 | 1.491 | 1.491 | 1.491 | 5 | 1 | 5 (5 / 5) | — (0 / 5) |
| normal | pierde a la hermana | soledad | 6 | 0.028 | 0.427 | 0.448 | 0.420 | 6 | 3 | 14 (1 / 6) | — (0 / 6) |
| normal | pierde a la hermana | soledad en casa | 6 | 0.004 | 0.472 | 0.487 | 0.482 | 6 | 2 | 11 (1 / 6) | — (0 / 6) |
| normal | pierde a la hermana | falta de la hermana viva (compañía) | 6 | 0.019 | 0.004 | 0.015 | -0.004 | 1 | 5 | 6 (1 / 1) | 6 (1 / 1) |
| normal | la conserva | duelo | 36 | 0.000 | 0.119 | 0.119 | 0.119 | 10 | 1 | 3 (10 / 10) | — (0 / 10) |
| normal | la conserva | soledad | 36 | 0.024 | 0.005 | 0.019 | -0.005 | 22 | 4 | 5 (22 / 22) | 5 (22 / 22) |
| normal | la conserva | soledad en casa | 36 | 0.016 | 0.002 | 0.023 | 0.007 | 17 | 4 | 5 (17 / 17) | 5 (17 / 17) |
| normal | la conserva | falta de la hermana viva (compañía) | 36 | 0.016 | 0.010 | 0.025 | 0.009 | 23 | 4 | 5 (23 / 23) | 6 (23 / 23) |
| sequia | pierde a la hermana | duelo | 25 | 0.014 | 0.939 | 1.021 | 1.006 | 17 | 1 | 5 (17 / 17) | — (0 / 17) |
| sequia | pierde a la hermana | soledad | 25 | 0.049 | 0.422 | 0.458 | 0.410 | 25 | 3 | 7 (3 / 25) | — (0 / 25) |
| sequia | pierde a la hermana | soledad en casa | 24 | 0.017 | 0.482 | 0.500 | 0.483 | 24 | 1 | 10 (4 / 24) | — (0 / 24) |
| sequia | pierde a la hermana | falta de la hermana viva (compañía) | 25 | 0.038 | 0.038 | 0.052 | 0.014 | 12 | 3 | 4 (12 / 12) | 4 (11 / 12) |
| sequia | la conserva | duelo | 140 | 0.016 | 0.177 | 0.196 | 0.181 | 72 | 1 | 4 (67 / 72) | 7 (4 / 72) |
| sequia | la conserva | soledad | 140 | 0.025 | 0.017 | 0.048 | 0.023 | 70 | 3 | 4 (68 / 70) | 4 (68 / 70) |
| sequia | la conserva | soledad en casa | 138 | 0.009 | 0.007 | 0.029 | 0.020 | 58 | 3 | 4 (57 / 58) | 4 (56 / 58) |
| sequia | la conserva | falta de la hermana viva (compañía) | 140 | 0.025 | 0.018 | 0.034 | 0.009 | 83 | 2 | 4 (83 / 83) | 4 (83 / 83) |
| sequia_dura | pierde a la hermana | duelo | 76 | 0.066 | 1.685 | 1.795 | 1.728 | 70 | 1 | 6 (53 / 70) | 5 (1 / 70) |
| sequia_dura | pierde a la hermana | soledad | 76 | 0.032 | 0.413 | 0.463 | 0.431 | 76 | 3 | 12 (33 / 76) | — (0 / 76) |
| sequia_dura | pierde a la hermana | soledad en casa | 76 | 0.014 | 0.478 | 0.500 | 0.486 | 76 | 1 | 9 (31 / 76) | — (0 / 76) |
| sequia_dura | pierde a la hermana | falta de la hermana viva (compañía) | 76 | 0.031 | 0.016 | 0.025 | -0.007 | 19 | 2 | 4 (19 / 19) | 5 (18 / 19) |
| sequia_dura | la conserva | duelo | 150 | 0.052 | 0.360 | 0.444 | 0.392 | 116 | 1 | 5 (95 / 116) | 8 (8 / 116) |
| sequia_dura | la conserva | soledad | 150 | 0.033 | 0.030 | 0.060 | 0.027 | 87 | 3 | 4 (87 / 87) | 4 (87 / 87) |
| sequia_dura | la conserva | soledad en casa | 150 | 0.010 | 0.015 | 0.035 | 0.025 | 77 | 3 | 4 (76 / 77) | 4 (76 / 77) |
| sequia_dura | la conserva | falta de la hermana viva (compañía) | 150 | 0.029 | 0.017 | 0.041 | 0.012 | 79 | 3 | 4 (77 / 79) | 4 (75 / 79) |
| bestias_crian | pierde a la hermana | duelo | 52 | 0.029 | 1.219 | 1.250 | 1.222 | 42 | 1 | 6 (33 / 42) | — (0 / 42) |
| bestias_crian | pierde a la hermana | soledad | 52 | 0.029 | 0.435 | 0.465 | 0.437 | 52 | 3 | 8 (1 / 52) | — (0 / 52) |
| bestias_crian | pierde a la hermana | soledad en casa | 52 | 0.014 | 0.467 | 0.498 | 0.484 | 52 | 1 | 12 (4 / 52) | — (0 / 52) |
| bestias_crian | pierde a la hermana | falta de la hermana viva (compañía) | 52 | 0.027 | 0.009 | 0.018 | -0.008 | 12 | 3 | 4 (10 / 12) | 4 (9 / 12) |
| bestias_crian | la conserva | duelo | 244 | 0.013 | 0.167 | 0.196 | 0.183 | 136 | 1 | 5 (102 / 136) | 5 (1 / 136) |
| bestias_crian | la conserva | soledad | 244 | 0.021 | 0.013 | 0.039 | 0.019 | 130 | 3 | 4 (122 / 130) | 4 (122 / 130) |
| bestias_crian | la conserva | soledad en casa | 243 | 0.010 | 0.006 | 0.025 | 0.015 | 113 | 3 | 4 (110 / 113) | 4 (110 / 113) |
| bestias_crian | la conserva | falta de la hermana viva (compañía) | 244 | 0.024 | 0.014 | 0.034 | 0.010 | 138 | 3 | 4 (132 / 138) | 4 (130 / 138) |
| todos | pierde a la hermana | duelo | 164 | 0.042 | 1.409 | 1.484 | 1.442 | 139 | 1 | 6 (111 / 139) | 5 (1 / 139) |
| todos | pierde a la hermana | soledad | 164 | 0.034 | 0.421 | 0.462 | 0.428 | 164 | 3 | 12 (40 / 164) | — (0 / 164) |
| todos | pierde a la hermana | soledad en casa | 163 | 0.015 | 0.475 | 0.499 | 0.484 | 163 | 1 | 9 (43 / 163) | — (0 / 163) |
| todos | pierde a la hermana | falta de la hermana viva (compañía) | 164 | 0.030 | 0.016 | 0.026 | -0.004 | 44 | 3 | 4 (42 / 44) | 4 (39 / 44) |
| todos | la conserva | duelo | 600 | 0.022 | 0.211 | 0.249 | 0.226 | 341 | 1 | 5 (279 / 341) | 7 (13 / 341) |
| todos | la conserva | soledad | 600 | 0.024 | 0.017 | 0.045 | 0.021 | 327 | 3 | 4 (315 / 327) | 4 (315 / 327) |
| todos | la conserva | soledad en casa | 597 | 0.010 | 0.008 | 0.028 | 0.018 | 281 | 3 | 4 (275 / 281) | 4 (274 / 281) |
| todos | la conserva | falta de la hermana viva (compañía) | 600 | 0.024 | 0.015 | 0.035 | 0.010 | 342 | 3 | 4 (332 / 342) | 4 (328 / 342) |

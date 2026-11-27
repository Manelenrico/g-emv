# El experimento de la base del ocho, v5: informe

*Prompt 134, del 15 al 16 de noviembre de 2026. Sobre el congelado `valle-congelado-v5` (RG68r: RG61r con «ven, lo necesito» apagado y la dormida sin voz). Las predicciones se sellaron y se subieron antes de jugar ninguna partida (`predicciones_selladas_v5.md`).*

## En pocas palabras

- **Se han jugado las 1.600 partidas,** sin ninguna fallida: 8 jugadores × 5 mundos × 40 semillas (30121–30160) × 40 días.
- **Se cumplen las 21 predicciones.**
- **RG68r frente a RG61r, en las mismas semillas:**
  - **más feliz en los cinco mundos:** la aldea +0,086 [+0,076, +0,097] y la peor parada +0,104 [+0,080, +0,129];
  - **empuja la mitad:** −105 empujones por partida;
  - **duerme más en casa:** +6,3 puntos de noches dentro, y 3,8 noches menos fuera por criatura;
  - **despierta 0,23 veces por noche**, frente a 31,9;
  - **vive igual:** −0,01 [−0,15, +0,13]. En la sequía dura vive algo menos, pero dentro del ruido (−0,40 [−0,85, +0,05]).
- **El hambre media sube +0,73 con la medida corregida** [+0,39, +1,09], pero los días con hambre de más de 60 **bajan** (−0,019 [−0,029, −0,010]). Es el fallo conocido 17 del congelado.
- **El bucle de regalos entre hermanas hartas sigue:** en 1 de las 200 partidas de RG68r hay una racha de 24. Es menos de 4, así que P17 se cumple.

## Cómo se ha jugado

- **El sellado:** el commit del congelado y las predicciones (`65ee6048`) y la etiqueta `valle-congelado-v5` subieron a GitHub (gemv-coworld, rama `paintball`) el **15-nov-2026 a las 09:52:07** (08:52:07 UTC), antes de jugar.
  - Comprobado con `git ls-remote`.
  - **Antes del push,** `revisa_subida.py` encontró una ruta personal en `informe_disco_v4.md` (prompt 122). Por la regla, paré y te pregunté. Decidiste corregir y subir: la cambié por `[ruta local]` en un commit aparte (`4120bc9f`). Después, `revisa_subida.py` y `copia_taller.py --solo-buscar` salieron limpios. La versión vieja queda en la historia del repositorio privado, como dice la decisión PUSH-1.
  - **La caché `por_partida.json` salió del repositorio** antes del push: la quité del commit que la llevaba, que era el último y no estaba subido (`--amend`, ahora `f33845c5`). Sigue en el disco y está en `.gitignore`.
- **La comprobación jugada** (`salida/puerta_experimento_v5.json`), idéntica en muertes, criaturas, mundo y criaturas línea a línea:
  - RG68r (bestias que crían, 1004), frente a su partida de M del taller del prompt 131 (es el mismo jugador);
  - el tonto (normal, 30001), frente a la del v2.
- **Apuntar no cambia nada** (`salida/prueba_experimento_v5.json`): RG68r y RG068r, 10 días, con los registros y sin ellos, salen idénticas.
- **El experimento:** `lanza_experimento_v5.py experimento 10`, en `valle_experimento_v5`.
  - Empezó el 15-nov a las 09:53 y acabó el 16-nov a las 20:29: unas 34,5 horas.
  - Te dije «hacia las 21:00 del 16», luego «00:30 del 17» y luego «23:00»; acabó antes que las tres.
  - 1.600 de 1.600 partidas, ningún error en el registro.

## Las predicciones, una a una

Los intervalos son del 95 %, por bootstrap de 10.000 remuestreos con semilla 8. Todo sale de `evalua_experimento_v5.py` (`salida/evalua_experimento_v5.md` y `.json`), escrito y sellado antes de jugar.

| | qué se predijo (resumido) | se cumple si | lo que ha salido | |
|---|---|---|---|---|
| P1 | en sequía, sequía dura y bestias que crían, RG68r vive al menos una criatura más que el tonto | media ≥ 1 e intervalo > 0 en los tres | sequía +2,70 [+2,33, +3,12]; sequía dura +1,52 [+1,18, +1,85]; bestias que crían +2,90 [+2,45, +3,35] | **SE CUMPLE** |
| P2 | en abundancia y normal, vive de media al menos 7,5 de 8 | las dos ≥ 7,5 | abundancia 7,95; normal 7,83. Declarado: en el normal, RG68r − tonto = −0,07 [−0,25, +0,10] | **SE CUMPLE** |
| P3 | ninguna muerte por golpe entre criaturas | 0 en las 1.600 | 0 | **SE CUMPLE** |
| P4 | con la bestia a la vista, otra pegada al menos el triple que en el tonto | ≥ 3 veces en la suma | RG68r 30,8 %, tonto 8,9 % (3,5 veces) | **SE CUMPLE** |
| P5 | en bestias que crían, echa la bestia al menos una vez por partida | media ≥ 1 | 5,75 por partida | **SE CUMPLE** |
| P6 | da más comida a la hermana que a cada vecina, en todos los mundos | en los cinco | hermana · cada vecina: abundancia 302 · 13,5; normal 427 · 48,8; sequía 664 · 59,3; sequía dura 510 · 49,7; bestias que crían 834 · 82,5 | **SE CUMPLE** |
| P7 | lo que da a quien está flaca es más en las sequías que en abundancia | sequía y sequía dura > abundancia | abundancia 28 %; normal 74 %; sequía 79 %; sequía dura 81 %; bestias que crían 84 % | **SE CUMPLE** |
| P8 | tras la muerte de la hermana pasa más tiempo con vecinas | media > 0 e intervalo > 0 | +0,11 [+0,08, +0,14] (162 criaturas) | **SE CUMPLE** |
| P9 | duerme dentro al menos el 55 % de las noches; nunca en una puerta sin estar agotada | ≥ 55 % en los cinco; 0 | dentro: 82 %, 81 %, 80 %, 72 %, 77 %. En una puerta, 41 noches, **las 41 agotada** | **SE CUMPLE** |
| P10 | en las sequías, RG068r vive igual o más que RG68r | límite superior ≥ 0 en las dos | sequía +0,25 [+0,03, +0,47]; sequía dura +0,97 [+0,57, +1,38] | **SE CUMPLE** |
| P11 | en los momentos más ambivalentes, RG68r y S68 coinciden más; sin las decisiones de dar, al revés | Q4 − Q1 > 0 con el intervalo > 0, y sin dar < 0 | **+0,042 [+0,011, +0,074]** (Q4 65,0 %, Q1 60,8 %). Sin las de dar: **−0,175 [−0,204, −0,146]**. Sin las de ir: +0,072 | **SE CUMPLE** |
| P12 | coge menos del 15 % de la fruta del árbol y menos que el recolector | las dos | RG68r 3,0 %, recolector 28,8 % | **SE CUMPLE** |
| P13 | no da su última comida con más de 60 de hambre en más de 2 de cada 100 partidas | ≤ 4 de 200 | 1 de 200 | **SE CUMPLE** |
| P16 | RG68r empuja más que RG068r en los cinco mundos | media mayor en los cinco | abundancia 98 · 48; normal 146 · 62; sequía 139 · 61; sequía dura 85 · 42; bestias que crían 165 · 61 | **SE CUMPLE** |
| P17 | rachas de ida y vuelta de más de 10 en 4 o menos de las 200 partidas de RG68r | ≤ 4 | **1 de 200** (comida, 24, abundancia 30149) | **SE CUMPLE** |
| P18 | despertares por voz por debajo de 1 por criatura y noche en los cinco mundos | < 1 en los cinco | RG68r · RG61r: 0,08 · 34,0; 0,09 · 37,2; 0,08 · 35,0; 0,07 · 23,1; 0,14 · 30,2 | **SE CUMPLE** |
| P19 | felicidad de la aldea mayor, con el intervalo sobre cero, en al menos cuatro mundos | ≥ 4 | **en los cinco:** abundancia +0,114; normal +0,124; sequía +0,089; sequía dura +0,036 [+0,011, +0,060]; bestias que crían +0,070 | **SE CUMPLE** |
| P20 | las vivas no son menos con el intervalo bajo cero en ningún mundo | en ninguno | abundancia +0,03; normal −0,07; sequía +0,07; **sequía dura −0,40 [−0,85, +0,05]**; bestias que crían +0,33 [−0,05, +0,72] | **SE CUMPLE** |
| P21 | empuja menos en los cinco mundos | menor en los cinco | RG68r · RG61r: 98 · 248; 146 · 279; 139 · 248; 85 · 138; 165 · 248 (todas las emparejadas fuera del ruido) | **SE CUMPLE** |
| P22 | duerme dentro de casa más noches en los cinco mundos | mayor en los cinco | RG68r · RG61r: 82 · 76; 81 · 75; 80 · 73; 72 · 65; 77 · 71 % | **SE CUMPLE** |
| P23 | el hambre media corregida sube menos de 2 puntos en los cinco mundos | media < 2 en los cinco | abundancia +0,76; normal +0,37; sequía +0,76; **sequía dura +1,05 [+0,05, +2,06]**; bestias que crían +0,73 | **SE CUMPLE** |

**Dos que pasan por poco:**
- **P20, en la sequía dura:** RG68r vive 0,40 menos y el intervalo llega a +0,05. Por muy poco no queda bajo cero.
- **P23, en la sequía dura:** la media es +1,05, por debajo del 2, pero el intervalo llega hasta +2,06.

**P17, qué pasa** (`mira_racha_v5.py`, `salida/mira_racha_v5.md`):
- La racha de 24 es el bucle de siempre: las hermanas C1 y C2, el día 9 por la mañana, hartas (hambre por debajo de 0) y con 3 o 4 comidas cada una, se dan comida la una a la otra en el mismo turno, 13 turnos seguidos.
- En las otras clases, la más larga es:

  | RG068r | S68 | S068 | P68 | RG61r |
  |---|---|---|---|---|
  | 3 | 13 | 37 | 6 | 3 |

  La de 37 de S068 es igual: dos hermanas sin hambre, de tarde.

## La tabla, como la del cierre v5

Está entera en `tabla_experimento_v5.md` (de `tabla_experimento_v5.py`). Las vivas al día 40, de 8:

| mundo | tonto | recolector | RG68r | RG068r | S68 | S068 | P68 | RG61r |
|---|---|---|---|---|---|---|---|---|
| abundancia | 7,88 | 8,00 | 7,95 | 8,00 | 7,95 | 8,00 | 7,92 | 7,92 |
| normal | 7,90 | 7,95 | 7,83 | 7,92 | 7,70 | 7,95 | 7,80 | 7,90 |
| sequía | 4,72 | 7,92 | 7,42 | 7,67 | 6,65 | 7,75 | 7,20 | 7,35 |
| sequía dura | 1,95 | 3,27 | 3,48 | 4,45 | 3,12 | 4,17 | 3,88 | 3,88 |
| bestias que crían | 3,42 | 5,53 | 6,33 | 6,38 | 5,50 | 6,35 | 6,12 | 6,00 |

- **En la sequía, el recolector vive más que RG68r** (7,92 frente a 7,42).
- **RG068r, que decide solo por lo que pierde, vive más que RG68r en las dos sequías** (P10).
- En la sequía dura, RG68r muere casi siempre de hambre: 164 de sus 181 muertes.

## Las medidas sin predicción

Están enteras en:
- `medidas_v5.md`: M1 a M6, con los mapas en `salida/figuras_v5/`;
- `anadidas_v5.md`: A1 y A2;
- `duelo_soledad_v5.md`: A4;
- `salida/evalua_experimento_v5.md`: M7 y M8;
- `tabla_experimento_v5.md`: la tabla como la del cierre v5.

Lo principal:

- **M1, felicidad funcional** (media de la aldea · la peor parada):

  | mundo | RG68r | RG61r |
  |---|---|---|
  | abundancia | 88 % · 77 % | 77 % · 59 % |
  | normal | 75 % · 54 % | 63 % · 40 % |
  | sequía | 66 % · 41 % | 57 % · 31 % |
  | sequía dura | 43 % · 18 % | 39 % · 16 % |
  | bestias que crían | 47 % · 27 % | 40 % · 20 % |

  RG068r y S068 dan 0 % por construcción, porque no tienen filas de ganancia.
- **M2, momentos hygge** (RG68r): las noches con al menos uno van del 64 % en abundancia al 22 % en la sequía dura. En el v4, con RG61r, del 73 % al 27 %.
- **M6, el perdón:** de 2.100 a 4.800 robos de vecinas por mundo, menos que en el v4. De los que vuelven, la mediana es 1 día; del 44 % al 54 % no vuelven.
- **M7:** el 60 % de las 569 vueltas del árbol de RG68r son al anochecer o de noche.
- **M8,** lo que reciben las vecinas que le robaron frente a las que no: tampoco se ve que reciban menos (comida por día, entre 0,001 y 0,009).
- **A2, la que pierde a su hermana** (159 casos, frente a 518 de control):

  | | pierde a la hermana: antes → después | la conserva: antes → después |
  |---|---|---|
  | felicidad funcional | 36 % → 0 % | 47 % → 46 % |
  | felicidad en casa | 40 % → 0 % | 53 % → 48 % |
  | duerme en casa | 77 % → 79 % | 77 % → 73 % |
  | pegada a una vecina, de día | 9 % → 22 % | 9 % → 9 % |
  | pegada a una vecina, de noche | 7 % → 14 % | 6 % → 6 % |

  139 de 159 no recuperan la felicidad de antes. Entre las que la recuperan, la mediana es 12 días.
- **A4, el duelo y la soledad**, de las filas apuntadas (159 casos):
  - **el duelo** salta al día siguiente (de 0,05 a 1,61; el peor día, 1,68) y baja a la mitad en una mediana de **6 días** (121 de los 148 en que sube);
  - **la soledad** sube a 0,44–0,48 y solo baja a la mitad en **30 de 159** casos (mediana de 15 días). **La soledad en casa** está casi en el techo (0,48–0,50) y baja a la mitad en 24 de 158;
  - igual que en el v3 y el v4: la tristeza baja en unos días y la soledad se queda.

## RG68r al lado de RG61r, emparejadas

*Las mismas semillas (30121–30160): 40 parejas por mundo. RG68r − RG61r, intervalo del 95 %; «\*» quiere decir que sale del ruido (`compara_v5_rg61r.md`, con todas las medidas de los talleres).*

| mundo | vivas | felicidad: aldea · peor parada | empujones | noches dentro | comidas dadas | hambre corregida |
|---|---|---|---|---|---|---|
| abundancia | +0,03 | +0,114\* · +0,174\* | −149\* | +0,055\* | −9,7\* | +0,76\* |
| normal | −0,07 | +0,124\* · +0,147\* | −132\* | +0,061\* | −8,2\* | +0,37 |
| sequía | +0,07 | +0,089\* · +0,104\* | −109\* | +0,065\* | −5,8\* | +0,76\* |
| sequía dura | −0,40 [−0,85, +0,05] | +0,036\* · +0,019 | −53\* | +0,074\* | −3,3\* | +1,05\* |
| bestias que crían | +0,33 [−0,05, +0,72] | +0,070\* · +0,078\* | −83\* | +0,059\* | −7,1\* | +0,73 |
| **los cinco** | **−0,01** | **+0,086\* · +0,104\*** | **−105\*** | **+0,063\*** | **−6,8\*** | **+0,73\*** |

En los cinco mundos juntos, además:
- **despertares:** 0,23 frente a 31,9 por noche;
- **golpes:** −0,22\*;
- **días con hambre de más de 60 (corregida):** −0,019\*;
- **a quién se da:** se da menos (−6,8 comidas), sobre todo a quien no lo necesita. La parte que va a quien tiene hambre de más de 60 sube del 65 % al 71 %\*;
- **lo que se quitan** después de dárselo baja del 17 % al 12 %\*;
- **muertes:** por hambre +0,03 y por la bestia −0,03, las dos dentro del ruido;
- **noches durmiendo fuera:** 7,6 frente a 11,4 por criatura\*;
- **el eco del vínculo entre hermanas** sube: +0,049\*.

Es lo mismo que salió en el taller del prompt 131 con las semillas 1001–1020, salvo dos cosas: aquí las vivas no suben (allí, +0,25), y las muertes por hambre no bajan.

## Fallos míos y arreglos (ninguno en el experimento)

- **Volví a lanzar dos `python3 -` vacíos** por la entrada estándar mientras preparaba el sellado: uno al editar el lanzador y otro al final de un comando de prueba. No hicieron nada. Es una falta repetida.
- **Un comando con un error de sintaxis mío** (al escribir `comprueba_clases_v5.py`) no llegó a ejecutarse; lo rehíce con el fichero escrito aparte.
- **Las horas de fin** que te di fueron cambiando (21:00 del 16, luego 00:30 del 17, luego 23:00). Acabó a las 20:29 del 16.
- **Los programas de las medidas sin predicción** los adapté y los probé mientras jugaba, no al final (en el v4 fue al revés).

## Gasto

| bolsa | gasto en el prompt | saldo |
|---|---|---|
| créditos de la plataforma | 0 (todo se jugó en el Mac) | no lo he leído |
| dólares de la consola de Anthropic | 0 | no lo he leído |

## Ficheros

- **El sellado:**
  - `CONGELADO_P8_v5.md` y `predicciones_selladas_v5.md`;
  - `congelado_v5/`: las huellas md5, las semillas y las clases;
  - `lanza_experimento_v5.py` y `evalua_experimento_v5.py`;
  - las pruebas: `salida/puerta_experimento_v5.json`, `salida/prueba_experimento_v5.json`, `salida/prueba_evalua_v5.py` y `medida_v5/mira_prueba_v5.py`.
- **El análisis:**
  - `medidas_v5.py`, `anadidas_v5.py`, `duelo_soledad_v5.py` y `tabla_experimento_v5.py`;
  - `compara_v5_rg61r.py` y `mira_racha_v5.py`;
  - la prueba `salida/prueba_compara_v5.py`.
- **Las salidas:**
  - `salida/evalua_experimento_v5.md` y `.json`;
  - `medidas_v5.md`, `anadidas_v5.md`, `duelo_soledad_v5.md` y `tabla_experimento_v5.md`;
  - `compara_v5_rg61r.md` y `salida/mira_racha_v5.md`;
  - las figuras, en `salida/figuras_v5/`.
- **Las partidas:** `valle_experimento_v5`, en el disco «Mem G-EMV».

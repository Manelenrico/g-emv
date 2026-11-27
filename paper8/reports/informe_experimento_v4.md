# El experimento de la base del ocho, tercera versión (v4): informe

*Prompt 117, del 11 al 12 de noviembre de 2026. Sobre el congelado `valle-congelado-v4` (RG61r: que robar deje huella en el vínculo). Las predicciones se sellaron y se subieron antes de jugar ninguna partida (`predicciones_selladas_v4.md`).*

## En pocas palabras

- **Se han jugado las 1.400 partidas,** sin ninguna fallida: 7 jugadores × 5 mundos × 40 semillas (30081–30120) × 40 días.
- **Se cumplen 14 de las 15 predicciones.** Falla solo **P17**: en 2 de las 200 partidas de RG61r hay una racha de regalos de comida de ida y vuelta de más de 10 (89 y 29).
  - Las dos son **intercambios a la vez entre hermanas, sin hambre:** se dan comida la una a la otra en el mismo turno, turno tras turno.
- **P11 sale como se predijo desde el diagnóstico del v3:**
  - en los momentos más ambivalentes, RG61r y las sumas coinciden más (+0,143 [+0,116, +0,170]);
  - sin las decisiones de dar, la diferencia es negativa (−0,115 [−0,139, −0,089]).
- **P9 se cumple con la cuenta arreglada:** RG61r duerme dentro de su casa del 69 % al 77 % de las noches. Las 141 veces que se duerme en una puerta, estaba agotada.
- **RG61r vive bastante más que el tonto donde hay escasez o bestias:**

  | mundo | criaturas vivas de más (de 8) | intervalo |
  |---|---|---|
  | sequía | +2,3 | [+2,0, +2,7] |
  | sequía dura | +2,1 | [+1,7, +2,4] |
  | bestias que crían | +2,4 | [+1,8, +3,0] |

- **Empuja unas tres veces más que RG061r** (P16): de 2,8 a 3,4 veces según el mundo.
- **Al lado de RG58r del v3** (semillas distintas): vive igual o algo más, empuja igual (más en bestias que crían), da algo más y está igual de feliz.

## Cómo se ha jugado

- **El sellado:** el commit del congelado y las predicciones (`27b23137`) y la etiqueta `valle-congelado-v4` subieron a GitHub (gemv-coworld, rama `paintball`) el **11-nov-2026 a las 12:56:36** (11:56:36 UTC), antes de jugar.
  - Comprobado con `git ls-remote`.
  - Antes, `revisa_subida.py` y `copia_taller.py --solo-buscar` salieron limpios.
  - Con ese push subieron también los commits locales anteriores, que son sus antecesores.
- **La comprobación jugada** (`salida/puerta_experimento_v4.json`), idéntica en muertes, criaturas, mundo y criaturas línea a línea:
  - RG61r (bestias que crían, 1004), frente a su partida del taller;
  - el tonto (normal, 30001), frente a la del v2.
- **Apuntar no cambia nada** (`salida/prueba_experimento_v4.json`): RG61r y RG061r, 10 días, con los registros nuevos y sin ellos, salen idénticos.
- **Los registros nuevos:** las filas de duelo, soledad y compañía se apuntaron en cada partida de criatura (`filas.jsonl.gz`). Así la A4 sale sin volver a jugar nada.
- **El experimento:** `lanza_experimento_v4.py experimento 10`, en `valle_experimento_v4`.
  - Empezó el 11-nov a las 12:57 y acabó el 12-nov a las 18:31: unas 29,5 horas, como el v3.
  - 1.400 de 1.400 partidas, ningún error en el registro.

## Las predicciones, una a una

Los intervalos son del 95 %, por bootstrap de 10.000 remuestreos con semilla 8. Todo sale de `evalua_experimento_v4.py` (`salida/evalua_experimento_v4.md` y `.json`).

| | qué se predijo (resumido) | se cumple si | lo que ha salido | |
|---|---|---|---|---|
| P1 | en sequía, sequía dura y bestias que crían, RG61r vive al menos una criatura más que el tonto | media ≥ 1 e intervalo > 0 en los tres | sequía +2,33 [+2,00, +2,65]; sequía dura +2,05 [+1,73, +2,38]; bestias que crían +2,38 [+1,75, +3,00] | **SE CUMPLE** |
| P2 | en abundancia y normal, RG61r vive de media al menos 7,5 de 8 | las dos ≥ 7,5 | abundancia 7,95; normal 7,95. Declarado: en el normal, RG61r − tonto = −0,05 [−0,12, +0,00] | **SE CUMPLE** |
| P3 | ninguna muerte por golpe entre criaturas | 0 en las 1.400 | 0 | **SE CUMPLE** |
| P4 | con la bestia a la vista, otra pegada al menos el triple que en el tonto | ≥ 3 veces, sumando los cinco mundos | RG61r 34,4 %, tonto 8,6 % (4,0 veces). Por mundo: abundancia 44 · 3; normal 34 · 5; sequía 39 · 3; sequía dura 39 · 4; bestias que crían 32 · 12 | **SE CUMPLE** |
| P5 | en bestias que crían, RG61r echa la bestia al menos una vez por partida | media ≥ 1 | 5,47 por partida | **SE CUMPLE** |
| P6 | da más comida a la hermana que a cada vecina, en todos los mundos | en los cinco | hermana · cada vecina: abundancia 493 · 54,3; normal 619 · 90,2; sequía 897 · 80,2; sequía dura 560 · 84,0; bestias que crían 875 · 128,7 | **SE CUMPLE** |
| P7 | lo que da a quien está flaca es más en las sequías que en abundancia | sequía y sequía dura > abundancia | abundancia 26 %; normal 68 %; sequía 60 %; sequía dura 78 %; bestias que crían 80 % | **SE CUMPLE** |
| P8 | tras la muerte de la hermana pasa más tiempo con vecinas | media > 0 e intervalo > 0 | +0,12 [+0,09, +0,15] de la parte del día pegada a una vecina (157 criaturas) | **SE CUMPLE** |
| P9 | duerme dentro de su casa al menos el 55 % de las noches en los cinco mundos, y ninguna noche en una puerta sin estar agotada | ≥ 55 % en los cinco; 0 en una puerta sin estar agotada | dentro: abundancia 77 %; normal 74 %; sequía 74 %; sequía dura 69 %; bestias que crían 72 %. En una puerta, 141 noches, **las 141 agotada** | **SE CUMPLE** |
| P10 | en las sequías, RG061r vive igual o más que RG61r | límite superior ≥ 0 en las dos | RG061r − RG61r: sequía +0,30 [+0,00, +0,60]; sequía dura +0,07 [−0,35, +0,47] | **SE CUMPLE** |
| P11 | en los momentos más ambivalentes, RG61r y S61 coinciden más; sin las decisiones de dar, al revés | Q4 − Q1 > 0 con el intervalo > 0, y sin dar < 0 | **+0,143 [+0,116, +0,170]** (Q4 71,6 %, Q1 57,3 %). Sin las decisiones en que alguna de las dos da: **−0,115 [−0,139, −0,089]** (Q4 74,4 %, Q1 85,9 %; 8.335 decisiones). Sin las de ir: +0,161 [+0,131, +0,190] | **SE CUMPLE** |
| P12 | coge menos del 15 % de la fruta del árbol y menos que el recolector | las dos | RG61r 3,8 %, recolector 28,2 % | **SE CUMPLE** |
| P13 | no da su última comida con más de 60 de hambre en más de 2 de cada 100 partidas | ≤ 4 de 200 | 1 de 200 (una vez) | **SE CUMPLE** |
| P16 | RG61r empuja al menos el doble que RG061r en los cinco mundos | ≥ 2 veces en los cinco | RG61r · RG061r por partida: abundancia 248 · 72 (×3,4); normal 278 · 93 (×3,0); sequía 240 · 84 (×2,9); sequía dura 135 · 48 (×2,8); bestias que crían 250 · 78 (×3,2) | **SE CUMPLE** |
| P17 | la racha más larga de regalos de ida y vuelta de RG61r es de 10 o menos | ninguna > 10 en las 200 | **comida 89** (sequía, semilla 30109), medicina 2 | **FALLA** |

**P17, qué pasa** (`mira_racha_v4.py`, `cuenta_rachas_v4.py`):
- **Las rachas de más de 10** salen en 2 de las 200 partidas de RG61r, las dos en sequía: 30109 con 89 y 30091 con 29. En las otras clases:

  | clase | partidas con rachas de más de 10 |
  |---|---|
  | RG061r | 2 de 200: abundancia 30085 con 37, sequía 30085 con 23 |
  | S61, S061 y P61 | ninguna (la más larga es de 10) |

- **La de 89:** las hermanas D1 y D2, el día 20, de noche, despiertas, sin hambre (de 0 a 7) y con 4 comidas cada una. Se dan comida **la una a la otra en el mismo turno**, turno tras turno, durante 45 turnos.
- **La de 37 de RG061r** es igual: dos hermanas sin hambre, de tarde, cada turno.
- Es un intercambio a la vez. La regla `devolver_v58` lo cuenta como devolución y le quita el gesto, el alivio y el gusto, pero aun así se repite.
- **Lo que no sé:** qué fila hace que dar siga ganando. No lo he mirado más, porque el experimento no apunta la foto y no se arregla nada aquí.
- En el taller del prompt 116, con las semillas 1001–1010, no salió (la racha más larga fue de 3).

## La tabla, como la del cierre v5

Está entera en `tabla_experimento_v4.md` (de `tabla_experimento_v4.py`), con la sección de dormir contada con la cuenta arreglada.

## Las medidas sin predicción

Están enteras en `medidas_v4.md` (M1–M6, con los mapas en `salida/figuras_v4/`), `anadidas_v4.md` (A1, A2), `duelo_soledad_v4.md` (A4) y `salida/evalua_experimento_v4.md` (M7, M8). Lo principal:

- **M1, felicidad funcional** (RG61r, media de la aldea):

  | mundo | media de la aldea | la peor parada |
  |---|---|---|
  | abundancia | 76 % | 60 % |
  | normal | 61 % | 39 % |
  | sequía | 56 % | 32 % |
  | sequía dura | 37 % | 14 % |
  | bestias que crían | 41 % | 22 % |

  RG061r y S061 dan 0 % por construcción, porque no tienen filas de ganancia.
- **M2, momentos hygge** (RG61r): las noches con al menos uno, de cada criatura, van del 73 % en abundancia al 27 % en la sequía dura.
- **M4:** los tres mapas por mundo están en `salida/figuras_v4/mapas_<mundo>.png`.
- **M6, el perdón:** de 3.600 a 8.800 robos de vecinas por mundo. De los que vuelven, la mediana es 1 día; del 46 % al 50 % no vuelven antes del final o de una muerte.
- **M7, la hora de las vueltas del árbol:** el 64 % de las 717 vueltas de RG61r son al anochecer o de noche. En el v3, con RG58r, el 48 %.
- **M8, lo que reciben las vecinas que le robaron frente a las que no** (comida por día; no sabíamos qué saldría):

  | mundo | las que robaron | las que no |
  |---|---|---|
  | abundancia | 0,004 | 0,001 |
  | normal | 0,006 | 0,007 |
  | sequía | 0,007 | 0,007 |
  | sequía dura | 0,012 | 0,011 |
  | bestias que crían | 0,011 | 0,013 |

  No se ve que reciban menos. Los pares que nunca robaron son pocos (119 a 509 por mundo, frente a unos 1.400–1.800).
- **A1:** el mapa de regalos de cada mundo está junto al del bienestar, en `salida/figuras_v4/regalos_<mundo>.png`.
- **A2, la que pierde a su hermana** (158 casos, frente a 524 de control):

  | | pierde a la hermana: antes → después | la conserva: antes → después |
  |---|---|---|
  | felicidad funcional | 28 % → 0 % | 38 % → 40 % |
  | felicidad en casa | 37 % → 0 % | 45 % → 44 % |
  | duerme en casa | 75 % → 75 % | 73 % → 72 % |
  | pegada a una vecina, de día | 13 % → 27 % | 15 % → 13 % |
  | pegada a una vecina, de noche | 9 % → 17 % | 11 % → 9 % |

  Días hasta recuperar la felicidad de antes: mediana de 12 entre las que la recuperan; **126 de 158 no la recuperan**.
- **A4, el duelo y la soledad**, de las filas apuntadas (157 casos):
  - **El duelo** salta al día siguiente de la muerte (de 0,04 a 1,40; el peor día, 1,50) y baja a la mitad en una mediana de **6 días** (111 de los 134 en que sube).
  - **La soledad** sube a 0,43–0,47 y solo baja a la mitad en **40 de 157** casos. **La soledad en casa** está casi en el techo (0,48) desde el día siguiente y baja a la mitad en 35 de 157.
  - Ninguna vuelve a como estaba.
  - Es lo mismo que en el v3: la tristeza baja en unos días y la soledad se queda.

## RG61r (v4) al lado de RG58r (v3)

*Aviso: **son semillas distintas** (v3: 30041–30080; v4: 30081–30120). No hay emparejamiento. La diferencia de vivas es entre medias de 40 partidas, con su intervalo por bootstrap de partidas (`compara_v3_v4.py`).*

| mundo | vivas al día 40: RG58r · RG61r · diferencia [IC 95 %] | empujones por partida: RG58r · RG61r | comidas dadas por partida (hermana · vecinas): RG58r → RG61r | felicidad funcional (aldea): RG58r · RG61r |
|---|---|---|---|---|
| abundancia | 7,88 · 7,95 · +0,08 [−0,05, +0,20] | 241 · 248 | 9,8 · 5,9 → 12,3 · 8,2 | 76 % · 76 % |
| normal | 7,85 · 7,95 · +0,10 [−0,03, +0,22] | 265 · 278 | 13,1 · 11,0 → 15,5 · 13,5 | 62 % · 61 % |
| sequía | 7,33 · 7,30 · −0,03 [−0,33, +0,28] | 238 · 240 | 16,9 · 12,1 → 22,4 · 12,0 | 56 % · 56 % |
| sequía dura | 3,73 · 4,03 · +0,30 [−0,08, +0,68] | 133 · 135 | 11,6 · 11,0 → 14,0 · 12,6 | 36 % · 37 % |
| bestias que crían | 6,15 · 6,28 · +0,12 [−0,35, +0,60] | 219 · 250 | 21,1 · 14,1 → 21,9 · 19,3 | 41 % · 41 % |

- **Vivas:** ninguna diferencia sale del ruido.
- **Empujones:** casi iguales; en bestias que crían, más.
- **Comidas dadas:** algo más, sobre todo a la hermana en sequía (16,9 → 22,4) y a las vecinas en bestias que crían (14,1 → 19,3).
- **Felicidad funcional:** igual.

## Fallos míos y arreglos (ninguno en el experimento)

- **Los programas de análisis del v4 los adapté tarde.** El 12-nov a las 12:46 te dije que me ponía con ellos y no lo hice hasta que preguntaste a las 16:17. Estuvieron listos y probados antes de que acabara el experimento.
- **La A2 del v3 tenía un fallo:** su «sigue durmiendo en casa» contaba la última vez que la criatura se dormía cada día, a cualquier hora, como la tabla de dormir. En el v4 se cuenta la primera vez de cada noche, dentro y sin la puerta, como está sellado.
- **En este prompt no he lanzado ningún `python3 -` con la entrada vacía ni ningún análisis por la entrada estándar.**

## Gasto

| bolsa | gasto en el prompt | saldo |
|---|---|---|
| créditos de la plataforma | 0 (todo se jugó en el Mac) | no lo he leído |
| dólares de la consola de Anthropic | 0 | no lo he leído |

## Ficheros

- **El sellado:**
  - `CONGELADO_P8_v4.md` y `predicciones_selladas_v4.md`;
  - `congelado_v4/` (las huellas md5, las semillas);
  - `lanza_experimento_v4.py`, `medida_v4/dormir_v4.py` y `evalua_experimento_v4.py`.
- **El análisis:**
  - `medidas_v4.py`, `anadidas_v4.py`, `duelo_soledad_v4.py`, `tabla_experimento_v4.py` y `compara_v3_v4.py`;
  - `mira_racha_v4.py` y `cuenta_rachas_v4.py`;
  - la prueba `prueba_analisis_v4.py`.
- **Las salidas:** `salida/evalua_experimento_v4.md` y `.json`, `tabla_experimento_v4.md`, `medidas_v4.md`, `anadidas_v4.md`, `duelo_soledad_v4.md`, `compara_v3_v4.md`, y las figuras en `salida/figuras_v4/`.
- **Las partidas:** `valle_experimento_v4`, en el disco «Mem G-EMV».

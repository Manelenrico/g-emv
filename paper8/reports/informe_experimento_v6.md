# El experimento de la base del ocho, v6: informe

*Prompt 150, del 18 al 19 de noviembre de 2026. Sobre el congelado `valle-congelado-v6`. La protagonista es RG69r+voz, «RG69rvoz» en las carpetas: RG68r con la reserva del 146 (RG69r) y la voz de ir a casa del 143, en clases hijas, sin tocar ninguna. Las predicciones se sellaron y se subieron antes de jugar ninguna partida (`predicciones_selladas_v6.md`). Lo que no se cumple se cuenta igual.*

## En pocas palabras

- **Se han jugado las 1.200 partidas,** sin ninguna fallida: 6 jugadores × 5 mundos × 40 semillas (30161–30200) × 40 días.
- **Se cumplen 21 de las 23 predicciones. Fallan P25 y P31,** las dos de «vive más que RG68r en la sequía dura con el intervalo sobre cero». Era uno de los riesgos declarados antes de jugar:
  - RG69r − RG68r: −0,05 [−0,40, +0,28];
  - RG69r+voz − RG68r: +0,20 [−0,23, +0,62].
- **La protagonista vive más o igual que las otras clases de criatura en los cinco mundos** (tabla de abajo), pero ninguna diferencia con RG68r sale del ruido.
- **Lo que la reserva y la voz tenían que cambiar, cambia:**
  - Días 0 a 9 de las sequías, turnos con hambre de más de 30 y comida en la bolsa: 2,98 al día, frente a 31,97 de RG68r (P29).
  - Noches dormidas fuera en esos días: 7,0 %, frente al 24,2 % de RG69r (P28).
  - Duerme dentro de casa del 86 % al 97 % de las noches; RG68r, del 75 % al 83 %.
  - Es la más feliz de las cuatro clases de criatura en los cinco mundos (M1).
- **P26 se cumple justo en el límite en la abundancia,** otro riesgo declarado. RG69r − RG68r da −0,07 [−0,17, +0,00]: RG68r no pierde ninguna criatura y RG69r pierde 3 por la bestia. El límite de arriba es cero y la regla pide «≥ 0», así que pasa.
- **El bucle de regalos entre hermanas hartas:** en 1 de las 200 partidas de la protagonista hay una racha de más de 10, de 15. P17 se cumple.

## Cómo se ha jugado

- **El sellado:** el commit `759acc39` y la etiqueta `valle-congelado-v6` subieron a GitHub (gemv-coworld, rama `paintball`). GitHub da la hora del push: **18-nov-2026 a las 00:03:14** (23:03:14 UTC del 17), antes de jugar ninguna partida.
  - Comprobado con `git ls-remote`.
  - Antes, `revisa_subida.py` y `copia_taller.py --solo-buscar` salieron limpios.
  - Con el push subieron también los 15 commits locales anteriores (prompts 135 a 149).
- **Las huellas** se comprobaron antes de pasar el evaluador y no han cambiado desde el sellado:
  - el congelado `3c332f41…`;
  - las predicciones `95036770…`;
  - el lanzador `b2e1b707…`, el de las 8 puertas del 149;
  - el evaluador `763dec48…`.
- **El experimento:** `lanza_experimento_v6.py experimento 10`, en `valle_experimento_v6`, una carpeta que no existía antes.
  - Empezó el 18-nov a las 00:03:26 y acabó el 18-nov a las 22:28: unas 22,5 horas.
  - Te dije «hacia las 03:00 del 19», luego «00:30» y luego «01:00»; acabó antes que las tres.
  - 1.200 de 1.200 partidas, todas con su `fin.json`, y el registro de errores vacío.
  - Las partidas de la protagonista escriben sus decisiones, `reserva_v69.json` y `voz_vc1.json`. Lo comprobé en las primeras dos, a las 04:13.
- **El evaluador sellado** (`evalua_experimento_v6.py`) tardó 34 minutos. Sale en `salida/evalua_experimento_v6.md` y `.json`.

## Vivas al día 40

De 8 criaturas; media de las 40 semillas.

| mundo | tonto | recolector | RG68r | RG068r | RG69r | RG69r+voz |
|---|---|---|---|---|---|---|
| abundancia | 8,00 | 7,97 | 8,00 | 7,97 | 7,92 | **8,00** |
| normal | 8,00 | 7,97 | 7,92 | 7,78 | 7,92 | **8,00** |
| sequía | 5,12 | 7,97 | 7,45 | 7,67 | 7,72 | **7,80** |
| sequía dura | 1,55 | 3,42 | 4,03 | 4,12 | 3,98 | **4,22** |
| bestias que crían | 3,50 | 5,55 | 6,28 | 6,50 | 6,50 | **6,65** |

- **La protagonista no pierde ninguna criatura en la abundancia ni en el normal.**
- **En la sequía, el recolector sigue viviendo más que todas las criaturas** (7,97).
- **En la sequía dura casi todas mueren de hambre en la época de escasez.** En la protagonista son 122 de sus 151 muertes (M14).
- **RG68r, la misma clase sellada del v5, vive más aquí en la sequía dura:** 4,03 frente a 3,48 en las semillas 30121–30160. Son semillas distintas.

**Muertes** (hambre · bestia · golpe · terreno), sumadas en las 40 partidas:

| mundo | tonto | recolector | RG68r | RG068r | RG69r | RG69r+voz |
|---|---|---|---|---|---|---|
| abundancia | 0 · 0 · 0 · 0 | 0 · 0 · 0 · 1 | 0 · 0 · 0 · 0 | 1 · 0 · 0 · 0 | 0 · 3 · 0 · 0 | 0 · 0 · 0 · 0 |
| normal | 0 · 0 · 0 · 0 | 0 · 0 · 0 · 1 | 0 · 3 · 0 · 0 | 6 · 3 · 0 · 0 | 1 · 2 · 0 · 0 | 0 · 0 · 0 · 0 |
| sequía | 115 · 0 · 0 · 0 | 0 · 1 · 0 · 0 | 16 · 6 · 0 · 0 | 8 · 2 · 0 · 3 | 7 · 4 · 0 · 0 | 3 · 5 · 0 · 0 |
| sequía dura | 258 · 0 · 0 · 0 | 176 · 2 · 0 · 5 | 144 · 10 · 0 · 5 | 138 · 12 · 0 · 5 | 143 · 13 · 0 · 5 | 139 · 9 · 0 · 3 |
| bestias que crían | 167 · 13 · 0 · 0 | 73 · 22 · 0 · 3 | 26 · 43 · 0 · 0 | 18 · 40 · 0 · 2 | 5 · 55 · 0 · 0 | 10 · 42 · 0 · 2 |

## Las predicciones, una a una

Los intervalos son del 95 %, por bootstrap de 10.000 remuestreos con semilla 8. «Margen» es lo que da el evaluador sellado: cuánto le sobra al valor respecto al umbral; «cerca» quiere decir menos del 20 %.

**Las que se quedan del v5, en la protagonista:**

| | qué se predijo (resumido) | se cumple si | lo que ha salido | |
|---|---|---|---|---|
| P1 | en la sequía, la sequía dura y bestias que crían, vive al menos una criatura más que el tonto | media ≥ 1 y límite de abajo > 0 en los tres | sequía +2,67 [+2,40, +2,98]; sequía dura +2,67 [+2,27, +3,08]; bestias que crían +3,15 [+2,58, +3,73] | **SE CUMPLE** |
| P2 | en la abundancia y el normal vive de media al menos 7,5 de 8 | las dos ≥ 7,5 | 8,00 y 8,00 (cerca del umbral, el 7 %, porque 8 es el techo). Declarado: en el normal, RG69r+voz − tonto = +0,00 [+0,00, +0,00] | **SE CUMPLE** |
| P3 | ninguna muerte por golpe entre criaturas | 0 en las 1.200 | 0 | **SE CUMPLE** |
| P4 | con la bestia a la vista, otra pegada al menos el triple que en el tonto | ≥ 3 veces en la suma | 30,8 % frente a 8,3 % (3,7 veces). Era el riesgo «va justa» | **SE CUMPLE** |
| P5 | en bestias que crían, echa la bestia al menos una vez por partida | media ≥ 1 | 7,30 por partida | **SE CUMPLE** |
| P6 | da más comida a la hermana que a cada vecina, en todos los mundos | en los cinco | hermana · cada vecina: abundancia 323 · 4,2; normal 285 · 7,2; sequía 590 · 23,8; sequía dura 404 · 30,5; bestias que crían 657 · 25,2 | **SE CUMPLE** |
| P7 | lo que da a quien está flaca es más en las sequías que en la abundancia | sequía y sequía dura > abundancia | abundancia 6 %; normal 28 %; sequía 42 %; sequía dura 51 %; bestias que crían 50 % | **SE CUMPLE** |
| P8 | tras la muerte de la hermana pasa más tiempo con vecinas | media > 0 y límite de abajo > 0 | +0,15 [+0,12, +0,18] (137 criaturas) | **SE CUMPLE** |
| P9 | duerme dentro al menos el 55 % de las noches; nunca en una puerta sin estar agotada | ≥ 55 % en los cinco; 0 | dentro: 97 %, 95 %, 93 %, 86 %, 91 %. En una puerta, 55 noches, **las 55 agotada** | **SE CUMPLE** |
| P10 | en las sequías, RG068r vive igual o más que RG68r | límite de arriba ≥ 0 en las dos | sequía +0,23 [−0,05, +0,50]; sequía dura +0,10 [−0,28, +0,50] | **SE CUMPLE** |
| P12 | coge menos del 15 % de la fruta del árbol, y menos que el recolector | las dos | 2,6 % frente al 27,0 % del recolector | **SE CUMPLE** |
| P13 | dar la última comida con más de 60 de hambre | ≤ 4 de las 200 | 0 de 200 | **SE CUMPLE** |
| P16 | empuja más que RG068r en los cinco mundos | media mayor en los cinco | abundancia 67 · 45; normal 120 · 62; sequía 108 · 60; sequía dura 73 · 40; bestias que crían 131 · 61 | **SE CUMPLE** |
| P17 | rachas de ida y vuelta de más de 10 en 4 o menos de sus 200 partidas | ≤ 4 | 1 de 200 (la más larga, 15) | **SE CUMPLE** |
| P18 | despertares por voz por debajo de 1 por criatura y noche | < 1 en los cinco | 0,02; 0,04; 0,06; 0,07; 0,12 | **SE CUMPLE** |

**Las nuevas:**

| | qué se predijo (resumido) | se cumple si | lo que ha salido | |
|---|---|---|---|---|
| P24 | sequías, días 0 a 9: RG69r pasa menos turnos con hambre de más de 30 y comida en la bolsa | RG69r ≤ 0,5 × RG68r | 3,75 frente a 31,97 (0,117) | **SE CUMPLE** |
| P25 | sequía dura: RG69r vive más que RG68r | límite de abajo > 0 | **−0,05 [−0,40, +0,28]** | **FALLA** |
| P26 | RG69r frente a RG68r, en cada mundo: vivas, felicidad de la aldea, empujones | límite de arriba de las vivas ≥ 0, felicidad ≥ −0,03 y empujones ≤ 1,25 veces, en los cinco | vivas: abundancia **−0,07 [−0,17, +0,00]**; normal +0,00 [−0,12, +0,12]; sequía +0,28 [+0,05, +0,50]; sequía dura −0,05 [−0,40, +0,28]; bestias que crían +0,23 [−0,23, +0,68]. Felicidad: −0,004; +0,024; +0,009; +0,008; +0,034. Empujones: ×1,01; ×0,86; ×0,92; ×0,92; ×0,85 | **SE CUMPLE** (en el límite) |
| P27 | sequía dura: más criaturas vivas al empezar el día 10 con la bolsa y la despensa vacías | RG69r > RG68r | 5,08 frente a 4,12 por partida | **SE CUMPLE** |
| P28 | sequías, días 0 a 9: la voz baja las noches dormidas fuera | RG69r+voz ≤ 2/3 × RG69r | 7,0 % frente a 24,2 % (0,290) | **SE CUMPLE** |
| P29 | la medida de P24, en la protagonista | ≤ 0,5 × RG68r | 2,98 frente a 31,97 (0,093) | **SE CUMPLE** |
| P30 | las tres partes de P26, RG69r+voz frente a RG69r | en los cinco mundos | vivas: +0,07 [+0,00, +0,17]; +0,07 [+0,00, +0,15]; +0,07 [−0,10, +0,25]; +0,25 [−0,12, +0,62]; +0,15 [−0,28, +0,60]. Felicidad: +0,031; +0,028; +0,036; +0,031; +0,014. Empujones: ×0,80; ×0,94; ×0,86; ×0,84; ×0,94 | **SE CUMPLE** |
| P31 | sequía dura: la protagonista vive más que RG68r | límite de abajo > 0 | **+0,20 [−0,23, +0,62]** | **FALLA** |

**Cuentan 23; se cumplen 21; fallan P25 y P31.** Las dos fallan por el ruido, no por el signo: la reserva sola no cambia nada y la protagonista vive 0,20 más, pero el intervalo toca el cero. En los talleres (30121–30140) salían por encima de cero, pero eran semillas ya vistas y no contaban.

**Cómo salieron los riesgos declarados antes de jugar:**
- **P26 en la abundancia:** se cumple justo en el límite. RG68r no pierde ninguna criatura en sus 40 partidas y RG69r pierde 3, las tres por la bestia. Así, todas las diferencias por semilla son cero o negativas, y el límite de arriba del intervalo es cero justo. La felicidad (−0,004) queda lejos del −0,03.
- **P4:** 3,7 veces; en los talleres, 3,5.
- **El hueco con la gemela (P25 y P31):** fallan, como se avisó. RG068r vive más o igual que RG68r (P10), y la protagonista vive igual o más que RG068r en los cinco mundos (M10), pero dentro del ruido en las sequías.
- **Las bestias que crían, con la voz:** frente a RG69r +0,15 [−0,28, +0,60]; frente a RG68r, unas +0,37 en las medias (6,65 frente a 6,28). No se predijo dirección.
- **Las nuevas (P24 a P31)** se han jugado ahora en semillas que no se habían visto. Las que cuentan son estas.

**Lo mismo en RG69r y RG68r** (no cuenta como predicción): P1 a P18 se cumplen también en las dos. RG68r tiene 3 de 200 partidas con «la última comida con más de 60 de hambre» (P13) y una racha de 30 (P17).

## Las medidas sin predicción

Están enteras en:
- `salida/evalua_experimento_v6.md`: M7 a M14;
- `medidas_v6.md`: M1 a M6, con los mapas en `salida/figuras_v6/`;
- `anadidas_v6.md`: A1 y A2;
- `duelo_soledad_v6.md`: A4.

Lo principal:

- **M1, felicidad funcional** (la aldea · la peor parada). La protagonista es la más alta en los cinco mundos:

  | mundo | RG69r+voz | RG69r | RG68r |
  |---|---|---|---|
  | abundancia | 92 % · 85 % | 89 % · 80 % | 89 % · 82 % |
  | normal | 79 % · 65 % | 77 % · 60 % | 74 % · 57 % |
  | sequía | 72 % · 56 % | 68 % · 53 % | 67 % · 43 % |
  | sequía dura | 45 % · 17 % | 42 % · 16 % | 41 % · 16 % |
  | bestias que crían | 53 % · 33 % | 52 % · 31 % | 49 % · 26 % |

  RG068r da 0 % por construcción.
- **M2, momentos hygge:** las noches con al menos uno van del 92 % en la abundancia al 40 % en la sequía dura. En el v5, con RG68r, del 64 % al 22 %.
- **M5, el huerto:** se trabaja igual en las cuatro clases (unas 6.400 veces por partida; en la sequía dura, unas 5.600 a 5.800).
- **M6, el perdón:** de 1.700 a 3.600 robos de vecinas por mundo. De los que vuelven, la mediana es 1 día; del 48 % al 57 % no vuelven.
- **M7:** el 24 % de las 488 vueltas del árbol son al anochecer o de noche (RG68r en el v5: 60 %).
- **M8,** lo que reciben las vecinas que le robaron frente a las que no: igual (entre 0,000 y 0,004 comidas por día).
- **M9** (era P11): Q4 − Q1 = +0,198 [+0,172, +0,224]. Sin las decisiones de dar, −0,026 [−0,049, −0,003]; sin las de ir, +0,286.
- **M10, la protagonista frente a RG068r:**
  - abundancia +0,03 [+0,00, +0,07];
  - normal +0,23 [+0,10, +0,38];
  - sequía +0,12 [−0,07, +0,33];
  - sequía dura +0,10 [−0,33, +0,50];
  - bestias que crían +0,15 [−0,33, +0,65].
- **M11, el hambre al empezar el día 10, en la sequía dura:**

  | RG68r | RG068r | RG69r | RG69r+voz |
  |---|---|---|---|
  | 54,3 | 27,9 | 31,4 | 24,6 |

  El día 30 es 28,5 · 12,8 · 6,7 · 4,1. Pero las muertes de hambre de los días 10 a 14 apenas cambian (3,15 · 2,70 · 2,88 · 3,02 por partida): llega con menos hambre, pero sin reserva (5,17 criaturas sin comida, frente a 4,12).
- **M12, la voz:**
  - de 0,83 a 1,20 voces por criatura y día;
  - se devuelven del 30 % al 43 %;
  - «ir a casa» ya era lo elegido del 42 % al 51 % de las veces;
  - cambia lo elegido en el 6 % al 14 % de las decisiones oyendo, más en la sequía dura.
- **M13:**
  - le quitan a empujones menos comida que a RG68r y RG69r: por ejemplo, el 20,1 % en la sequía dura, frente al 27,1 % de RG68r;
  - pasa menos turnos al frío fuera de casa: 28,3 por día frente a 49,1 de RG68r en la sequía dura, y 6,2 frente a 34,1 en la abundancia.
- **M14, muertes por causa y por época:** el frío sale a cero, como se declaró. En la sequía dura, la mayoría de las muertes de hambre son en la época de escasez (RG69r+voz, 122 de 139). En bestias que crían, la protagonista muere más por la bestia que de hambre (42 · 10), igual que RG68r (43 · 26).
- **A2, la que pierde a su hermana** (136 casos, frente a 378 de control):

  | | pierde a la hermana: antes → después | la conserva: antes → después |
  |---|---|---|
  | felicidad funcional | 29 % → 1 % | 44 % → 44 % |
  | felicidad en casa | 37 % → 1 % | 52 % → 48 % |
  | duerme en casa | 86 % → 72 % | 91 % → 94 % |
  | pegada a una vecina, de día | 10 % → 27 % | 9 % → 9 % |
  | pegada a una vecina, de noche | 7 % → 20 % | 5 % → 7 % |

  109 de 136 no recuperan la felicidad de antes; entre las que la recuperan, la mediana es 15 días.
- **A4, el duelo y la soledad,** de las filas apuntadas (135 casos):
  - el duelo salta al día siguiente (de 0,05 a 1,64) y baja a la mitad en una mediana de 5 días (109 de los 130 en que sube);
  - la soledad sube a 0,43–0,48 y solo baja a la mitad en 34 de 135 casos (mediana de 16 días);
  - igual que en el v3, el v4 y el v5: la tristeza baja en unos días y la soledad se queda.

## Fallos míos y arreglos (ninguno en el experimento)

- **Python suelto, declarado:**
  - mientras preparaba el sellado, dos `python3 -` con un texto pegado: uno para añadir M14 y el «4 de las 200» al evaluador, antes de sellarlo, y otro para añadir dos grupos a `congelado_v6/md5_v6.py`;
  - un `python3 -m py_compile` para comprobar que compilaban los tres programas adaptados;
  - al final, dos `python3 -c` para leer el `.json` del evaluador (P26). Solo leían; no daban nada que no estuviera en el `.md`.
- **`duelo_soledad_v6.py` se paró la primera vez.** Al adaptarlo del v5, la sustitución de nombres puso la etiqueta «RG69r+voz» donde va el nombre de la carpeta, «RG69rvoz», en dos líneas: la 50, del modo «jugar», que no se usa, y la 72. No escribió nada. Arreglé las dos líneas y lo volví a pasar bien.
- **En M1 y M5 (`medidas_v6.md`), las tablas ponen «RG69rvoz»** donde deberían poner «RG69r+voz». Es solo la etiqueta; no lo he cambiado.
- **Dos esperas mías repetidas** vigilando el evaluador; las paré.
- **Las horas de fin que te di fueron cambiando** (03:00, 00:30 y 01:00 del 19). Acabó a las 22:28 del 18.
- **Los programas de las medidas sin predicción** los adapté mientras jugaba, pero no los probé hasta el final, para no ver ningún número antes de tiempo. Por eso el fallo de `duelo_soledad_v6.py` salió al final.

## Gasto

| bolsa | gasto en el prompt | saldo |
|---|---|---|
| créditos de la plataforma | 0 (todo se jugó en el Mac) | no lo he leído |
| dólares de la consola de Anthropic | 0 | no lo he leído |

## Ficheros

- **El sellado** (commit `759acc39`, etiqueta `valle-congelado-v6`):
  - `CONGELADO_P8_v6.md` y `predicciones_selladas_v6.md`;
  - `congelado_v6/`;
  - `lanza_experimento_v6.py` y `evalua_experimento_v6.py`.
- **El análisis:** `medidas_v6.py`, `anadidas_v6.py` y `duelo_soledad_v6.py`, copias de los del v5 con la protagonista, la carpeta y las semillas del v6.
- **Las salidas:**
  - `salida/evalua_experimento_v6.md` y `.json`;
  - `medidas_v6.md`, `anadidas_v6.md`, `duelo_soledad_v6.md` y `salida/duelo_soledad_v6.json`;
  - las figuras, en `salida/figuras_v6/`.
- **Fuera del commit:**
  - las partidas, en `valle_experimento_v6`, en el disco «Mem G-EMV»;
  - las cachés de cada partida: `evalua_v6/` (284 MB) y los `noches_*.json` de `dormir_fuera_v5/`;
  - `salida/medidas_v6.json`, como en el v5;
  - los registros, en `salida/logs_v6/`.

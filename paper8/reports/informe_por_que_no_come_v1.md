# Valle · prompt 145 · Por qué RG68r no se come lo que lleva en la bolsa

**Qué es esto:**
- **Solo diagnóstico.** Se volvieron a jugar 10 partidas selladas solo para leer lo que la criatura ya calculaba; ninguna decisión cambia.
- **No cambia el congelado ni las predicciones selladas.** No se ha tocado `model.py` ni la clase RG68r. No se ha llamado a ningún modelo de lenguaje. **Gasto: cero.**

**Los programas:**
- `lanza_pnc_v1.py`: vuelve a jugar con el registro;
- `por_que_no_come_v1/regla_comer_v1.py`: el punto 1;
- `por_que_no_come_v1/analiza_pnc_v1.py`: las tablas y las historias, que van a `analiza_pnc_v1.md` y `.json`.

Las reglas de cada uno están en su cabecera.

## Resumen

**1. Todo lo que contó el 144 se podía comer en el acto.**
- **Lo que hay en la bolsa:** comida o medicina. No hay semillas ni nada que haya que llevar a casa para comerlo.
- **La única regla del mundo para comer es «harta»:** con el hambre por debajo de 15 no se puede (`valle/mundo.py:486-489` y `:591`). No pide estar quieta, ni en casa, ni de día.
- **La cuenta rehecha** (80 partidas selladas, días 0 a 9), turnos despierta con hambre > 30 por criatura y día:

  | turnos despierta con hambre > 30, por criatura y día | RG68r | gemela |
  |---|---|---|
  | lleva comida que se puede comer ya | 30,3 | 4,9 |
  | solo lleva medicina | 1,7 | 2,5 |
  | no lleva nada, pero hay comida en la despensa | 0,9 | 0,9 |
  | no hay comida en ninguna parte | 15,1 | 7,9 |

- **Ningún «comer» rechazado por otra razón:** el mundo solo rechazó «comer» por llevar la bolsa vacía (RG68r 23 veces y la gemela 10).
- **Así que las cosas que no se pueden comer no lo explican,** y se siguió adelante.

**2. Volver a jugar da exactamente lo mismo.** Las 10 partidas (RG68r, sequía y sequía dura, semillas 30121 a 30125, días 0 a 9) son idénticas a las selladas, línea a línea, en el registro del mundo y en el de las criaturas. Por eso son iguales las comidas, los empujones, las muertes y las posiciones de cada turno (`salida/puerta_pnc_v1.json`).

**3. «Comer» siempre está, pero queda lejos.** Hay 50.965 turnos de una criatura viva con hambre > 30 y comida en la bolsa. De ellos:
- **No decide en el 32 % de los turnos despierta** (12.475): sigue andando hacia un destino ya elegido. En ese momento no se pone a comparar.
- **En las 26.826 decisiones despierta, «comer» está entre los candidatos el 100 % de las veces.** Ni el mundo ni el menú lo quitan nunca.
- **Lo elige** en el 38,6 % de esas decisiones: el 53,6 % en sequía y el 27,6 % en sequía dura.
- **Cuando no lo elige** (16.476 decisiones):
  - casi siempre queda lejos: mediana +0,357 de malestar, y solo un 2,1 % a menos de 0,01;
  - en el 64 % de esas decisiones queda la sexta o peor;
  - en su lugar elige quedarse (51 %), trabajar el huerto (26 %), ir a casa (5 %), ir a la hermana (4,5 %) o ir a por un objeto (4 %).

**4. La hipótesis de la mesa se cumple.** Para RG68r, tener comida es una ganancia de recursos, y comer se la gasta.
- **La fila que más hunde a «comer» es V-RECURSOS.** Es la ganancia de recursos por la comida que tiene, contando la bolsa, la despensa y su parte del almacén (`cuerpo_valle.py:2261-2276`).
  - Quitándola sola, gana «comer» en el **59 %** de las decisiones en que no come.
  - De media vale 0,29 en «comer» y 0,79 en lo elegido (−0,50).
- **Las otras dos que más pesan:**
  - V-CUERPO, una ganancia: quitándola sola, gana «comer» en el 33 %;
  - R-CARENCIA, una pérdida de recursos: lo es en el 32 %. «Comer» la sube +0,23.
- **Por dimensiones, «comer» menos lo elegido** (neto = ganancia − pérdida): cuerpo **+0,56**, recursos **−0,69**, vínculo −0,02.
  - En el 100 % de esas decisiones (16.475 de 16.476), el neto de recursos de «comer» queda por debajo del de lo elegido.
  - Lo que gana en cuerpo no compensa lo que pierde en recursos.
- **Es la última comida que lleva lo que no se come.** Cuando no come, el 70 % de las veces lleva **una sola comida** en la bolsa (media 1,45). Cuando sí come, lleva 4,45 de media.
  - Con poca comida, la fila de recursos cae deprisa con cada comida que gasta (es W / (W + k)), así que comerse la última es lo que más le cuesta.

**5. Que se la quiten a empujones.** De las 16.476 decisiones en que no come, en 917 (5,6 %) pierde comida a empujones en los 44 turnos siguientes. Son 88 empujones distintos. Las decisiones en que sí come acaban así en un 3,4 % (347 de 10.350).
- **Sequía dura:** 6,6 % frente a 3,1 %.
- **Sequía:** 3,4 % frente a 3,6 %.

## Las tres frases

1. **No come por la mesa.** Para RG68r, la comida que lleva vale como ganancia de recursos, sobre todo cuando es la última. Comérsela se la quita, y eso pesa más que lo que gana en cuerpo: el neto de recursos de «comer» queda por debajo del de lo elegido en todas las decisiones en que no come. Quitar solo esa fila haría ganar a «comer» en el 59 % de ellas.
2. **No le falta la opción.** «Comer» está entre los candidatos en el 100 % de sus decisiones, y el mundo deja comer siempre con hambre de más de 15. Lo que pasa es que queda lejos de lo elegido (mediana +0,36), y casi un tercio de esos turnos ni siquiera decide, porque va andando a un destino.
3. **Guardar la última comida le sale caro poco a poco.** En 5,6 de cada 100 decisiones en que no come, se la quitan a empujones en los 44 turnos siguientes, frente a 3,4 cuando come. La diferencia está casi toda en sequía dura.

## Lo que esto no dice

- **Por qué la gemela sí come:** de ella no hay registro de candidatos. Este análisis no dice si lleva la misma fila de recursos ni con qué peso.
- **Qué cambiaría al tocar la fila:** quitarla aquí es una lectura de las filas, no una prueba. Cambiar una fila cambiaría todo lo que viene después.

## Lo simple que elegí (no estaba dicho)

- **Qué es una decisión «despierta»:** lo que hace ese turno no es dormir, como el 144. Las decisiones de dormir se cuentan aparte (11.664).
- **«La fila que lo hunde»:** la que, quitada sola de todos los candidatos, hace ganar a «comer», calculado con el mismo malestar de la criatura. Una decisión puede tener varias, o ninguna (el 27 %).
- **Las filas de recursos:** las que la criatura reparte sobre todo a recursos (su tabla de reparto, guardada en cada partida en `no_come_cfg.json`).
- **«Le quitan a empujones»:** pierde un empujón y suelta comida en los turnos t+1 a t+44.
- **Las tres historias:** sacadas con random.Random(8).sample entre las decisiones despierta en que «comer» estaba y no lo eligió.

## Tropiezos

- **Python suelto, contra la regla:** se me escaparon dos `-c` que no hacían nada (`python3 -c 1` y `python3 -I -c "pass"`), mientras miraba el código del mundo.
- **Una segunda pasada que no hacía falta:**
  - **Qué parecía estar mal:** en la primera pasada, el análisis daba las filas V-…, G-… y P-SABOR sin reparto y como «pérdida». La criatura las da de alta mientras juega, así que el programa de análisis no las conocía.
  - **Qué hice:** pensé que también estaban mal las seis sumas guardadas, cambié el lanzador para guardar la tabla de reparto de la criatura y volví a jugar las 10 partidas en `valle_pnc_v2`.
  - **Lo que resultó:** las sumas estaban bien. La criatura no lleva reparto propio, y las filas que da de alta ya estaban en la misma tabla del mismo proceso.
  - **Lo que queda:** la primera pasada sigue en `/Volumes/Mem G-EMV/valle_pnc_v1`, sin borrar. Si quieres quitarla, es cosa tuya.
- **Un comentario mal puesto:** al cambiar la carpeta con sed, dejé `EXP` dentro de un comentario y la comprobación final falló. Lo arreglé y la repetí: pasa.

## Gasto

- **Créditos de la plataforma:** 0.
- **Dólares de la consola de Anthropic:** 0.

---


## las 10 partidas

**Los turnos con hambre > 30 y comida en la bolsa** (cada criatura viva):

| | turnos | parte |
|---|---|---|
| todos | 50965 | |
| despierta (no duerme ese turno) | 39301 | 77,1 % |
| despierta y decide (hay fotos) | 26826 | 68,3 % de los despierta |
| despierta y no decide: sigue destino | 12475 | 31,7 % de los despierta |
| decide dormir | 11664 | |

Lo que hace cuando no decide (sigue lo ya elegido): mover 12475.

**En las decisiones despierta:**

| | decisiones | parte |
|---|---|---|
| «comer» está entre los candidatos | 26826 | 100,0 % |
| «comer» no está | 0 | 0,0 % |
| está y la elige | 10350 | 38,6 % de las que está |
| está y elige otra cosa | 16476 | 61,4 % de las que está |

**Cuando está y no la elige:**

| puesto de «comer» | 2 | 3 | 4 | 5 | 6 o más |
|---|---|---|---|---|---|
| decisiones | 1521 | 1284 | 1301 | 1764 | 10606 |

A cuánto queda de lo elegido (malestar de «comer» − el de lo elegido): mediana +0,3566, cuartiles +0,1292 y +0,5885; a menos de 0,01: 2,1 %.

Lo que elige en su lugar: quedarse 51,1 %, trabajar_planta 25,8 %, ir_casa 4,8 %, ir_pareja 4,5 %, ir_objeto 4,1 %, coger 3,2 %, mover 2,6 %, ir_botin 2,1 %.

Cuánta comida lleva entonces en la bolsa: 1: 69,7 %, 2: 23,0 %, 3: 3,3 %, 4 o más: 4,0 % (media 1,45; cuando sí come, media 4,45).

**Las filas que lo hunden** (quitada una sola, de todos los candidatos, gana «comer»): hay alguna en 12033 de 16476 (73,0 %).

| fila | reparto (cuerpo, recursos, vínculo) | ganancia o pérdida | decisiones en que, quitada, gana «comer» | parte |
|---|---|---|---|---|
| V-RECURSOS | (0.0, 1.0, 0.0) | ganancia | 9712 | 58,9 % |
| V-CUERPO | (1.0, 0.0, 0.0) | ganancia | 5438 | 33,0 % |
| R-CARENCIA | (0.15, 0.7, 0.15) | pérdida | 5261 | 31,9 % |
| G-F-HAMBRE | (0.8, 0.1, 0.1) | ganancia | 333 | 2,0 % |
| G-R-CARENCIA | (0.15, 0.7, 0.15) | ganancia | 325 | 2,0 % |
| F-FRIO | (0.8, 0.1, 0.1) | pérdida | 164 | 1,0 % |
| G-F-CANSANCIO | (0.8, 0.1, 0.1) | ganancia | 104 | 0,6 % |
| P-SABOR | (0.8, 0.1, 0.1) | ganancia | 95 | 0,6 % |
| V-VINCULO | (0.0, 0.0, 1.0) | ganancia | 82 | 0,5 % |
| F-CANSANCIO | (0.8, 0.1, 0.1) | pérdida | 54 | 0,3 % |
| R-HERMANO-FALTA | (0.1, 0.8, 0.1) | pérdida | 42 | 0,3 % |
| S-COMPANIA | (0.1, 0.1, 0.8) | pérdida | 18 | 0,1 % |

**Las seis sumas, de media** (puntos 3 y 4; «comer» y lo elegido en la misma decisión):

| suma | «comer» | lo elegido | «comer» − lo elegido |
|---|---|---|---|
| ganancia de cuerpo | +0,987 | +0,699 | +0,288 |
| pérdida de cuerpo | +0,599 | +0,872 | -0,273 |
| ganancia de recursos | +0,487 | +1,048 | -0,561 |
| pérdida de recursos | +0,921 | +0,791 | +0,130 |
| ganancia de vínculo | +0,591 | +0,615 | -0,024 |
| pérdida de vínculo | +0,363 | +0,365 | -0,002 |
| **neto (ganancia − pérdida), «comer» − elegido** | cuerpo +0,561 | recursos -0,691 | vínculo -0,022 |

En 16475 de 16476 (100,0 %) el neto de recursos de «comer» queda por debajo del de lo elegido.

**Fila a fila, «comer» − lo elegido** (media sobre las decisiones en que no la elige; las 14 que más se mueven):

| fila | reparto (cuerpo, recursos, vínculo) | ganancia o pérdida | «comer» − elegido | decisiones con esa fila |
|---|---|---|---|---|
| V-RECURSOS | (0.0, 1.0, 0.0) | ganancia | -0,498 | 16425 |
| F-HAMBRE | (0.8, 0.1, 0.1) | pérdida | -0,410 | 16476 |
| R-CARENCIA | (0.15, 0.7, 0.15) | pérdida | +0,229 | 16476 |
| G-F-HAMBRE | (0.8, 0.1, 0.1) | ganancia | +0,160 | 16476 |
| P-SABOR | (0.8, 0.1, 0.1) | ganancia | +0,115 | 10233 |
| G-R-CARENCIA | (0.15, 0.7, 0.15) | ganancia | -0,111 | 16454 |
| V-CUERPO | (1.0, 0.0, 0.0) | ganancia | +0,099 | 16476 |
| V-VINCULO | (0.0, 0.0, 1.0) | ganancia | -0,019 | 14426 |
| F-FRIO | (0.8, 0.1, 0.1) | pérdida | +0,018 | 1891 |
| G-F-FRIO | (0.8, 0.1, 0.1) | ganancia | -0,015 | 1189 |
| V-RADAR-RECURSOS | (0.0, 1.0, 0.0) | ganancia | -0,008 | 12087 |
| R-HERMANO-FALTA | (0.1, 0.8, 0.1) | pérdida | +0,008 | 2420 |
| G-ALIVIO | (0.1, 0.1, 0.8) | ganancia | -0,008 | 155 |
| F-CANSANCIO | (0.8, 0.1, 0.1) | pérdida | +0,006 | 14208 |

**La hipótesis de la mesa** (punto 4): las filas que van a recursos, «comer» frente a lo elegido.

| fila de recursos | ganancia o pérdida | «comer» (media) | lo elegido (media) | «comer» − elegido |
|---|---|---|---|---|
| V-RECURSOS | ganancia | +0,294 | +0,792 | -0,498 |
| R-CARENCIA | pérdida | +0,932 | +0,702 | +0,229 |
| G-R-CARENCIA | ganancia | +0,020 | +0,131 | -0,111 |
| V-RADAR-RECURSOS | ganancia | +0,142 | +0,150 | -0,008 |
| R-HERMANO-FALTA | pérdida | +0,050 | +0,042 | +0,008 |
| G-R-ACOPIO | ganancia | +0,000 | +0,001 | -0,001 |
| R-ACOPIO | pérdida | +0,161 | +0,160 | +0,001 |
| G-R-CURIOSIDAD-FRONTERA | ganancia | +0,000 | +0,000 | -0,000 |
| R-CURIOSIDAD-FRONTERA | pérdida | +0,003 | +0,003 | +0,000 |
| P-RADAR-RECURSOS | pérdida | +0,001 | +0,001 | -0,000 |

**Le quitan a empujones en los 44 turnos siguientes** (punto 5): 917 de 16476 decisiones en que no come (5,6 %); son 88 empujones distintos. Para comparar, en las decisiones en que sí come: 347 de 10350 (3,4 %).

## sequía

**Los turnos con hambre > 30 y comida en la bolsa** (cada criatura viva):

| | turnos | parte |
|---|---|---|
| todos | 19398 | |
| despierta (no duerme ese turno) | 15722 | 81,0 % |
| despierta y decide (hay fotos) | 11323 | 72,0 % de los despierta |
| despierta y no decide: sigue destino | 4399 | 28,0 % de los despierta |
| decide dormir | 3676 | |

Lo que hace cuando no decide (sigue lo ya elegido): mover 4399.

**En las decisiones despierta:**

| | decisiones | parte |
|---|---|---|
| «comer» está entre los candidatos | 11323 | 100,0 % |
| «comer» no está | 0 | 0,0 % |
| está y la elige | 6073 | 53,6 % de las que está |
| está y elige otra cosa | 5250 | 46,4 % de las que está |

**Cuando está y no la elige:**

| puesto de «comer» | 2 | 3 | 4 | 5 | 6 o más |
|---|---|---|---|---|---|
| decisiones | 487 | 454 | 445 | 555 | 3309 |

A cuánto queda de lo elegido (malestar de «comer» − el de lo elegido): mediana +0,3376, cuartiles +0,1162 y +0,6061; a menos de 0,01: 1,9 %.

Lo que elige en su lugar: quedarse 44,0 %, trabajar_planta 27,2 %, ir_casa 5,7 %, ir_objeto 5,7 %, ir_pareja 4,8 %, coger 3,8 %, mover 3,2 %, ir_botin 3,1 %.

Cuánta comida lleva entonces en la bolsa: 1: 60,1 %, 2: 26,6 %, 3: 5,4 %, 4 o más: 7,8 % (media 1,67; cuando sí come, media 4,74).

**Las filas que lo hunden** (quitada una sola, de todos los candidatos, gana «comer»): hay alguna en 3701 de 5250 (70,5 %).

| fila | reparto (cuerpo, recursos, vínculo) | ganancia o pérdida | decisiones en que, quitada, gana «comer» | parte |
|---|---|---|---|---|
| V-RECURSOS | (0.0, 1.0, 0.0) | ganancia | 2719 | 51,8 % |
| V-CUERPO | (1.0, 0.0, 0.0) | ganancia | 1980 | 37,7 % |
| R-CARENCIA | (0.15, 0.7, 0.15) | pérdida | 1875 | 35,7 % |
| G-R-CARENCIA | (0.15, 0.7, 0.15) | ganancia | 115 | 2,2 % |
| G-F-HAMBRE | (0.8, 0.1, 0.1) | ganancia | 91 | 1,7 % |
| F-FRIO | (0.8, 0.1, 0.1) | pérdida | 90 | 1,7 % |
| V-VINCULO | (0.0, 0.0, 1.0) | ganancia | 46 | 0,9 % |
| P-SABOR | (0.8, 0.1, 0.1) | ganancia | 35 | 0,7 % |
| F-CANSANCIO | (0.8, 0.1, 0.1) | pérdida | 23 | 0,4 % |
| G-F-CANSANCIO | (0.8, 0.1, 0.1) | ganancia | 18 | 0,3 % |
| G-F-FRIO | (0.8, 0.1, 0.1) | ganancia | 6 | 0,1 % |
| R-HERMANO-FALTA | (0.1, 0.8, 0.1) | pérdida | 4 | 0,1 % |

**Las seis sumas, de media** (puntos 3 y 4; «comer» y lo elegido en la misma decisión):

| suma | «comer» | lo elegido | «comer» − lo elegido |
|---|---|---|---|
| ganancia de cuerpo | +0,984 | +0,700 | +0,284 |
| pérdida de cuerpo | +0,549 | +0,798 | -0,249 |
| ganancia de recursos | +0,579 | +1,122 | -0,543 |
| pérdida de recursos | +0,876 | +0,741 | +0,135 |
| ganancia de vínculo | +0,574 | +0,597 | -0,023 |
| pérdida de vínculo | +0,356 | +0,358 | -0,002 |
| **neto (ganancia − pérdida), «comer» − elegido** | cuerpo +0,533 | recursos -0,678 | vínculo -0,021 |

En 5249 de 5250 (100,0 %) el neto de recursos de «comer» queda por debajo del de lo elegido.

**Fila a fila, «comer» − lo elegido** (media sobre las decisiones en que no la elige; las 14 que más se mueven):

| fila | reparto (cuerpo, recursos, vínculo) | ganancia o pérdida | «comer» − elegido | decisiones con esa fila |
|---|---|---|---|---|
| V-RECURSOS | (0.0, 1.0, 0.0) | ganancia | -0,469 | 5242 |
| F-HAMBRE | (0.8, 0.1, 0.1) | pérdida | -0,394 | 5250 |
| R-CARENCIA | (0.15, 0.7, 0.15) | pérdida | +0,239 | 5250 |
| G-F-HAMBRE | (0.8, 0.1, 0.1) | ganancia | +0,176 | 5250 |
| G-R-CARENCIA | (0.15, 0.7, 0.15) | ganancia | -0,122 | 5250 |
| P-SABOR | (0.8, 0.1, 0.1) | ganancia | +0,106 | 3072 |
| V-CUERPO | (1.0, 0.0, 0.0) | ganancia | +0,095 | 5250 |
| V-VINCULO | (0.0, 0.0, 1.0) | ganancia | -0,024 | 4576 |
| F-FRIO | (0.8, 0.1, 0.1) | pérdida | +0,024 | 480 |
| G-F-FRIO | (0.8, 0.1, 0.1) | ganancia | -0,022 | 511 |
| F-CANSANCIO | (0.8, 0.1, 0.1) | pérdida | +0,014 | 4577 |
| V-RADAR-RECURSOS | (0.0, 1.0, 0.0) | ganancia | -0,011 | 3684 |
| G-S-COMPANIA | (0.1, 0.1, 0.8) | ganancia | -0,008 | 358 |
| V-RADAR-VINCULO | (0.0, 0.0, 1.0) | ganancia | +0,003 | 1970 |

**La hipótesis de la mesa** (punto 4): las filas que van a recursos, «comer» frente a lo elegido.

| fila de recursos | ganancia o pérdida | «comer» (media) | lo elegido (media) | «comer» − elegido |
|---|---|---|---|---|
| V-RECURSOS | ganancia | +0,389 | +0,858 | -0,469 |
| R-CARENCIA | pérdida | +0,902 | +0,663 | +0,239 |
| G-R-CARENCIA | ganancia | +0,017 | +0,139 | -0,122 |
| V-RADAR-RECURSOS | ganancia | +0,143 | +0,155 | -0,011 |
| R-HERMANO-FALTA | pérdida | +0,016 | +0,013 | +0,003 |
| R-ACOPIO | pérdida | +0,170 | +0,169 | +0,001 |
| G-R-ACOPIO | ganancia | +0,000 | +0,001 | -0,001 |
| G-R-CURIOSIDAD-FRONTERA | ganancia | +0,000 | +0,001 | -0,001 |
| R-CURIOSIDAD-FRONTERA | pérdida | +0,007 | +0,005 | +0,001 |
| P-RADAR-RECURSOS | pérdida | +0,000 | +0,000 | +0,000 |

**Le quitan a empujones en los 44 turnos siguientes** (punto 5): 177 de 5250 decisiones en que no come (3,4 %); son 19 empujones distintos. Para comparar, en las decisiones en que sí come: 216 de 6073 (3,6 %).

## sequía dura

**Los turnos con hambre > 30 y comida en la bolsa** (cada criatura viva):

| | turnos | parte |
|---|---|---|
| todos | 31567 | |
| despierta (no duerme ese turno) | 23579 | 74,7 % |
| despierta y decide (hay fotos) | 15503 | 65,7 % de los despierta |
| despierta y no decide: sigue destino | 8076 | 34,3 % de los despierta |
| decide dormir | 7988 | |

Lo que hace cuando no decide (sigue lo ya elegido): mover 8076.

**En las decisiones despierta:**

| | decisiones | parte |
|---|---|---|
| «comer» está entre los candidatos | 15503 | 100,0 % |
| «comer» no está | 0 | 0,0 % |
| está y la elige | 4277 | 27,6 % de las que está |
| está y elige otra cosa | 11226 | 72,4 % de las que está |

**Cuando está y no la elige:**

| puesto de «comer» | 2 | 3 | 4 | 5 | 6 o más |
|---|---|---|---|---|---|
| decisiones | 1034 | 830 | 856 | 1209 | 7297 |

A cuánto queda de lo elegido (malestar de «comer» − el de lo elegido): mediana +0,3615, cuartiles +0,1415 y +0,5815; a menos de 0,01: 2,2 %.

Lo que elige en su lugar: quedarse 54,5 %, trabajar_planta 25,1 %, ir_pareja 4,4 %, ir_casa 4,3 %, ir_objeto 3,3 %, coger 2,9 %, mover 2,3 %, ir_botin 1,7 %.

Cuánta comida lleva entonces en la bolsa: 1: 74,1 %, 2: 21,3 %, 3: 2,3 %, 4 o más: 2,3 % (media 1,35; cuando sí come, media 4,04).

**Las filas que lo hunden** (quitada una sola, de todos los candidatos, gana «comer»): hay alguna en 8332 de 11226 (74,2 %).

| fila | reparto (cuerpo, recursos, vínculo) | ganancia o pérdida | decisiones en que, quitada, gana «comer» | parte |
|---|---|---|---|---|
| V-RECURSOS | (0.0, 1.0, 0.0) | ganancia | 6993 | 62,3 % |
| V-CUERPO | (1.0, 0.0, 0.0) | ganancia | 3458 | 30,8 % |
| R-CARENCIA | (0.15, 0.7, 0.15) | pérdida | 3386 | 30,2 % |
| G-F-HAMBRE | (0.8, 0.1, 0.1) | ganancia | 242 | 2,2 % |
| G-R-CARENCIA | (0.15, 0.7, 0.15) | ganancia | 210 | 1,9 % |
| G-F-CANSANCIO | (0.8, 0.1, 0.1) | ganancia | 86 | 0,8 % |
| F-FRIO | (0.8, 0.1, 0.1) | pérdida | 74 | 0,7 % |
| P-SABOR | (0.8, 0.1, 0.1) | ganancia | 60 | 0,5 % |
| R-HERMANO-FALTA | (0.1, 0.8, 0.1) | pérdida | 38 | 0,3 % |
| V-VINCULO | (0.0, 0.0, 1.0) | ganancia | 36 | 0,3 % |
| F-CANSANCIO | (0.8, 0.1, 0.1) | pérdida | 31 | 0,3 % |
| S-COMPANIA | (0.1, 0.1, 0.8) | pérdida | 14 | 0,1 % |

**Las seis sumas, de media** (puntos 3 y 4; «comer» y lo elegido en la misma decisión):

| suma | «comer» | lo elegido | «comer» − lo elegido |
|---|---|---|---|
| ganancia de cuerpo | +0,988 | +0,698 | +0,290 |
| pérdida de cuerpo | +0,622 | +0,906 | -0,284 |
| ganancia de recursos | +0,444 | +1,014 | -0,570 |
| pérdida de recursos | +0,942 | +0,815 | +0,127 |
| ganancia de vínculo | +0,599 | +0,623 | -0,024 |
| pérdida de vínculo | +0,367 | +0,369 | -0,002 |
| **neto (ganancia − pérdida), «comer» − elegido** | cuerpo +0,574 | recursos -0,697 | vínculo -0,023 |

En 11226 de 11226 (100,0 %) el neto de recursos de «comer» queda por debajo del de lo elegido.

**Fila a fila, «comer» − lo elegido** (media sobre las decisiones en que no la elige; las 14 que más se mueven):

| fila | reparto (cuerpo, recursos, vínculo) | ganancia o pérdida | «comer» − elegido | decisiones con esa fila |
|---|---|---|---|---|
| V-RECURSOS | (0.0, 1.0, 0.0) | ganancia | -0,512 | 11183 |
| F-HAMBRE | (0.8, 0.1, 0.1) | pérdida | -0,417 | 11226 |
| R-CARENCIA | (0.15, 0.7, 0.15) | pérdida | +0,225 | 11226 |
| G-F-HAMBRE | (0.8, 0.1, 0.1) | ganancia | +0,152 | 11226 |
| P-SABOR | (0.8, 0.1, 0.1) | ganancia | +0,118 | 7161 |
| G-R-CARENCIA | (0.15, 0.7, 0.15) | ganancia | -0,106 | 11204 |
| V-CUERPO | (1.0, 0.0, 0.0) | ganancia | +0,101 | 11226 |
| V-VINCULO | (0.0, 0.0, 1.0) | ganancia | -0,016 | 9850 |
| F-FRIO | (0.8, 0.1, 0.1) | pérdida | +0,015 | 1411 |
| G-F-FRIO | (0.8, 0.1, 0.1) | ganancia | -0,012 | 678 |
| R-HERMANO-FALTA | (0.1, 0.8, 0.1) | pérdida | +0,010 | 2207 |
| G-ALIVIO | (0.1, 0.1, 0.8) | ganancia | -0,010 | 139 |
| V-RADAR-RECURSOS | (0.0, 1.0, 0.0) | ganancia | -0,006 | 8403 |
| G-S-COMPANIA | (0.1, 0.1, 0.8) | ganancia | -0,005 | 498 |

**La hipótesis de la mesa** (punto 4): las filas que van a recursos, «comer» frente a lo elegido.

| fila de recursos | ganancia o pérdida | «comer» (media) | lo elegido (media) | «comer» − elegido |
|---|---|---|---|---|
| V-RECURSOS | ganancia | +0,249 | +0,761 | -0,512 |
| R-CARENCIA | pérdida | +0,946 | +0,721 | +0,225 |
| G-R-CARENCIA | ganancia | +0,022 | +0,128 | -0,106 |
| R-HERMANO-FALTA | pérdida | +0,065 | +0,055 | +0,010 |
| V-RADAR-RECURSOS | ganancia | +0,142 | +0,148 | -0,006 |
| G-R-ACOPIO | ganancia | +0,000 | +0,001 | -0,001 |
| R-ACOPIO | pérdida | +0,157 | +0,156 | +0,000 |
| G-R-CURIOSIDAD-FRONTERA | ganancia | +0,000 | +0,000 | -0,000 |
| R-CURIOSIDAD-FRONTERA | pérdida | +0,002 | +0,002 | +0,000 |
| P-RADAR-RECURSOS | pérdida | +0,001 | +0,001 | -0,000 |

**Le quitan a empujones en los 44 turnos siguientes** (punto 5): 740 de 11226 decisiones en que no come (6,6 %); son 69 empujones distintos. Para comparar, en las decisiones en que sí come: 131 de 4277 (3,1 %).

## Tres historias (sacadas a suertes)

### sequía dura 30121, C2, día 9, turno 130

- **Cómo está:** hambre 34,8, 2 comidas en la bolsa, fuera de casa (casilla [31, 26]).
- **Lo que elige:** quedarse {"accion": "quedarse"}; «comer» queda la 7.ª de 18, a +0.1123 de malestar.
- **Los cinco primeros** (malestar; ganancia y pérdida de cuerpo, recursos y vínculo): quedarse 2.5889 [0.72588, 0.55573, 0.9427, 0.64433, 0.69294, 0.32128]; ir_pareja 2.6099 [0.70499, 0.57312, 0.94043, 0.64663, 0.69107, 0.32348]; ir_bosque 2.6177 [0.69997, 0.58008, 0.93994, 0.64754, 0.69074, 0.32436]; ir_frontera 2.6177 [0.69997, 0.58008, 0.93994, 0.64754, 0.69074, 0.32436]; ir_casa 2.6213 [0.70499, 0.57541, 0.94043, 0.64891, 0.69107, 0.34176].
- **«comer» frente a lo elegido, por dimensión:** [1.0876, 0.29764, 0.7018, 0.67691, 0.72653, 0.30151] frente a [0.72588, 0.55573, 0.9427, 0.64433, 0.69294, 0.32128].
- **Lo que la hunde** (quitada, gana «comer»): V-CUERPO, V-RECURSOS.
- **Después:** vuelve a comer a los 47 turnos; no pierde comida a empujones en los 44 turnos.

### sequía dura 30124, A1, día 5, turno 27

- **Cómo está:** hambre 52,3, 2 comidas en la bolsa, fuera de casa (casilla [19, 19]).
- **Lo que elige:** coger {"accion": "coger", "de": "planta", "tipo": "comida"}; «comer» queda la 6.ª de 22, a +0.2996 de malestar.
- **Los cinco primeros** (malestar; ganancia y pérdida de cuerpo, recursos y vínculo): coger 2.5812 [0.62477, 0.75563, 1.24568, 0.66234, 0.74375, 0.27572]; ir_botin 2.5875 [0.62302, 0.76071, 1.2454, 0.66307, 0.74373, 0.27637]; ir_objeto 2.5875 [0.62302, 0.76071, 1.2454, 0.66307, 0.74373, 0.27637]; trabajar_planta 2.5923 [0.61545, 0.8279, 1.14949, 0.56537, 0.76709, 0.26433]; quedarse 2.8729 [0.60921, 0.77207, 0.9701, 0.74447, 0.72778, 0.2932].
- **«comer» frente a lo elegido, por dimensión:** [1.04012, 0.48864, 0.73715, 0.77846, 0.76889, 0.27114] frente a [0.62477, 0.75563, 1.24568, 0.66234, 0.74375, 0.27572].
- **Lo que la hunde** (quitada, gana «comer»): ninguna fila sola.
- **Después:** vuelve a comer a los 13 turnos; no pierde comida a empujones en los 44 turnos.

### sequía dura 30124, D1, día 5, turno 157

- **Cómo está:** hambre 37,1, 2 comidas en la bolsa, fuera de casa (casilla [21, 10]).
- **Lo que elige:** quedarse {"accion": "quedarse"}; «comer» queda la 2.ª de 19, a +0.0059 de malestar.
- **Los cinco primeros** (malestar; ganancia y pérdida de cuerpo, recursos y vínculo): quedarse 2.8679 [0.64416, 0.82367, 1.08148, 0.75669, 0.547, 0.30254]; comer 2.8738 [0.82252, 0.58436, 0.82012, 0.78593, 0.55852, 0.28402]; ir_pareja 2.8825 [0.63238, 0.83359, 1.08019, 0.75799, 0.54595, 0.30379]; ir_frontera 2.9032 [0.62059, 0.84899, 1.07891, 0.75998, 0.5449, 0.30573]; ir_objeto 2.9886 [0.62097, 0.86407, 1.14163, 0.70058, 0.01738, 0.33691].
- **«comer» frente a lo elegido, por dimensión:** [0.82252, 0.58436, 0.82012, 0.78593, 0.55852, 0.28402] frente a [0.64416, 0.82367, 1.08148, 0.75669, 0.547, 0.30254].
- **Lo que la hunde** (quitada, gana «comer»): R-CARENCIA, V-CUERPO, V-RECURSOS.
- **Después:** vuelve a comer a los 4 turnos; no pierde comida a empujones en los 44 turnos.


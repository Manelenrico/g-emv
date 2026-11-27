# Los dos experimentos sellados, juntos (v5 y v6)

*Prompt 151, 19 de noviembre de 2026.*

**Todo lo que hay aquí es análisis hecho después de ver los datos, no predicción.**
- Solo se leen partidas ya jugadas: las del v5 (`valle_experimento_v5`, semillas 30121–30160) y las del v6 (`valle_experimento_v6`, semillas 30161–30200).
- No se ha jugado nada ni se ha llamado a ningún modelo.
- **No cambia ningún congelado ni ninguna predicción:** el v5 y el v6 siguen como se sellaron, y sus informes también.

Cada diferencia va con su intervalo del 95 %, por bootstrap de 10.000 remuestreos con semilla 8. Las diferencias entre clases van emparejadas por semilla. La diferencia entre los dos experimentos se calcula remuestreando las semillas de cada uno por separado.

**De dónde sale cada medida:**
- **Las vivas el día 40:** 8 menos las muertes de `fin.json`, como en los evaluadores.
- **El hambre al empezar el día 10 y las muertes de hambre en cada escasez:** la medida de M11, importada del evaluador sellado del v6 (`escasez`), sin tocarlo.
- **Las épocas:** las de la config de cada partida. Son días de 5 en ciclo (abundancia, normal, escasez, normal), así que los días 10 a 14 y 30 a 34 son escasez.

**Programas:**
- `juntos_v1/juntos_v1.py` para los puntos 1 a 4; salen en `juntos_v1/juntos_v1.md` y `.json`;
- `juntos_v1/m9_v1.py` para el punto 5; sale en `juntos_v1/m9_v1.md` y `.json`.

## 1. La gemela frente a RG68r: las vivas el día 40

RG068r − RG68r, emparejadas por semilla:

| mundo | v5 | v6 | las 80 semillas juntas | v6 − v5 |
|---|---|---|---|---|
| abundancia | +0,05 [+0,00, +0,12] | −0,03 [−0,07, +0,00] | +0,01 [−0,03, +0,06] | −0,08 [−0,17, +0,00] |
| normal | +0,10 [−0,05, +0,25] | −0,15 [−0,33, +0,00] | −0,03 [−0,14, +0,09] | **−0,25 [−0,47, −0,03]** |
| sequía | +0,25 [+0,03, +0,47] | +0,23 [−0,05, +0,50] | **+0,24 [+0,06, +0,41]** | −0,02 [−0,38, +0,33] |
| sequía dura | +0,97 [+0,57, +1,38] | +0,10 [−0,28, +0,50] | **+0,54 [+0,25, +0,84]** | **−0,88 [−1,43, −0,30]** |
| bestias que crían | +0,05 [−0,38, +0,47] | +0,23 [−0,20, +0,65] | +0,14 [−0,15, +0,44] | +0,17 [−0,42, +0,80] |

Las medias de cada clase (RG68r · RG068r), para leer la tabla:

| mundo | v5 | v6 |
|---|---|---|
| abundancia | 7,95 · 8,00 | 8,00 · 7,97 |
| normal | 7,83 · 7,92 | 7,92 · 7,78 |
| sequía | 7,42 · 7,67 | 7,45 · 7,67 |
| sequía dura | **3,48** · 4,45 | **4,03** · 4,12 |
| bestias que crían | 6,33 · 6,38 | 6,28 · 6,50 |

- **En la sequía, los dos experimentos cuadran:** la gemela vive un cuarto de criatura más en los dos.
- **En la sequía dura no cuadran:** la ventaja de la gemela pasa de casi una criatura a una décima. La diferencia entre los dos experimentos sale del ruido.
  - Es sobre todo porque RG68r vive más en las semillas del v6: 4,03 frente a 3,48. La gemela vive algo menos: 4,12 frente a 4,45.
- **En el normal, la diferencia entre experimentos también sale del ruido,** pero por poco: el intervalo llega a −0,03. Se debe a 0,15 criaturas.

## 2. El hambre al empezar el día 10 y las muertes de hambre en cada escasez

RG068r − RG68r, emparejadas por semilla:

| medida | mundo | v5 | v6 | las 80 juntas | v6 − v5 |
|---|---|---|---|---|---|
| hambre al empezar el día 10 (media de las vivas) | sequía | −15,69 [−18,51, −12,92] | −13,30 [−16,52, −9,97] | −14,49 [−16,68, −12,31] | +2,38 [−1,96, +6,79] |
| | sequía dura | −24,57 [−28,81, −20,33] | −26,42 [−31,10, −21,69] | −25,49 [−28,68, −22,36] | −1,85 [−8,11, +4,32] |
| muertes de hambre, días 10 a 14 (por partida) | sequía | −0,07 [−0,23, +0,07] | −0,12 [−0,33, +0,05] | −0,10 [−0,23, +0,01] | −0,05 [−0,28, +0,17] |
| | sequía dura | −1,27 [−1,77, −0,78] | −0,45 [−0,95, +0,05] | **−0,86 [−1,23, −0,49]** | **+0,82 [+0,12, +1,55]** |
| muertes de hambre, días 30 a 34 (por partida) | sequía | +0,03 [−0,07, +0,12] | −0,03 [−0,12, +0,05] | +0,00 [−0,07, +0,07] | −0,05 [−0,20, +0,10] |
| | sequía dura | +0,05 [−0,10, +0,20] | +0,12 [−0,03, +0,30] | +0,09 [−0,03, +0,21] | +0,07 [−0,15, +0,33] |

Las medias (RG68r · RG068r):

| medida | mundo | v5 | v6 |
|---|---|---|---|
| hambre al empezar el día 10 | sequía | 19,51 · 3,82 | 19,04 · 5,74 |
| | sequía dura | 48,71 · 24,14 | 54,34 · 27,92 |
| muertes de hambre, días 10 a 14 | sequía | 0,15 · 0,07 | 0,23 · 0,10 |
| | sequía dura | 3,67 · 2,40 | 3,15 · 2,70 |
| muertes de hambre, días 30 a 34 | sequía | 0,05 · 0,07 | 0,05 · 0,03 |
| | sequía dura | 0,05 · 0,10 | 0,05 · 0,17 |

- **La gemela llega al día 10 con mucha menos hambre en los dos experimentos,** y por lo mismo: unos 15 puntos menos en la sequía y unos 25 en la sequía dura. Esta diferencia no cambia de un experimento al otro.
- **Lo que cambia es cuántas mueren en la primera escasez de la sequía dura.** En el v5, la gemela perdía 1,27 criaturas menos por partida; en el v6, solo 0,45 menos.
  - RG68r muere menos en el v6 (3,15 frente a 3,67) y la gemela algo más (2,70 frente a 2,40).
  - Con la misma ventaja de hambre, la ventaja en muertes casi desaparece. Es el mismo hueco que en las vivas del punto 1.
- **En la segunda escasez (días 30 a 34) casi no muere nadie de hambre,** en ninguna de las dos clases ni en ningún experimento.

## 3. Solo el v6: la reserva y la voz

Emparejadas por semilla.

**Las vivas el día 40:**

| mundo | RG69r+voz − RG68r | RG69r − RG68r | RG69r+voz − RG69r |
|---|---|---|---|
| abundancia | +0,00 [+0,00, +0,00] | −0,07 [−0,17, +0,00] | +0,07 [+0,00, +0,17] |
| normal | +0,07 [+0,00, +0,15] | +0,00 [−0,12, +0,12] | +0,07 [+0,00, +0,15] |
| sequía | **+0,35 [+0,10, +0,60]** | **+0,28 [+0,05, +0,50]** | +0,07 [−0,10, +0,25] |
| sequía dura | +0,20 [−0,23, +0,62] | −0,05 [−0,40, +0,28] | +0,25 [−0,12, +0,62] |
| bestias que crían | +0,38 [−0,07, +0,82] | +0,23 [−0,23, +0,68] | +0,15 [−0,28, +0,60] |

**Las muertes de hambre en la partida:**

| mundo | RG69r+voz − RG68r | RG69r − RG68r | RG69r+voz − RG69r |
|---|---|---|---|
| abundancia | +0,00 [+0,00, +0,00] | +0,00 [+0,00, +0,00] | +0,00 [+0,00, +0,00] |
| normal | +0,00 [+0,00, +0,00] | +0,03 [+0,00, +0,07] | −0,03 [−0,07, +0,00] |
| sequía | **−0,33 [−0,55, −0,12]** | **−0,23 [−0,45, −0,03]** | −0,10 [−0,25, +0,03] |
| sequía dura | −0,12 [−0,57, +0,30] | −0,03 [−0,40, +0,35] | −0,10 [−0,47, +0,28] |
| bestias que crían | **−0,40 [−0,60, −0,20]** | **−0,53 [−0,75, −0,30]** | +0,12 [−0,03, +0,28] |

**Las muertes de hambre por época,** sumadas en las 40 partidas (entre paréntesis, por partida):

| mundo | clase | época de abundancia | época normal | época de escasez | todas |
|---|---|---|---|---|---|
| sequía | RG68r | 0 (0,00) | 5 (0,12) | 11 (0,28) | 16 (0,40) |
| | RG068r | 0 (0,00) | 3 (0,07) | 5 (0,12) | 8 (0,20) |
| | RG69r | 0 (0,00) | 2 (0,05) | 5 (0,12) | 7 (0,17) |
| | RG69r+voz | 0 (0,00) | 1 (0,03) | 2 (0,05) | 3 (0,07) |
| sequía dura | RG68r | 0 (0,00) | 16 (0,40) | 128 (3,20) | 144 (3,60) |
| | RG068r | 1 (0,03) | 22 (0,55) | 115 (2,88) | 138 (3,45) |
| | RG69r | 0 (0,00) | 25 (0,62) | 118 (2,95) | 143 (3,58) |
| | RG69r+voz | 0 (0,00) | 17 (0,42) | 122 (3,05) | 139 (3,48) |

**Las muertes de hambre en la época de escasez,** por partida, emparejadas:

| mundo | RG69r+voz − RG68r | RG69r − RG68r | RG69r+voz − RG69r |
|---|---|---|---|
| sequía | **−0,23 [−0,40, −0,05]** | −0,15 [−0,35, +0,03] | −0,07 [−0,17, +0,03] |
| sequía dura | −0,15 [−0,70, +0,40] | −0,25 [−0,68, +0,17] | +0,10 [−0,40, +0,60] |

- **En la sequía la reserva salva:** con RG69r mueren de hambre 0,23 criaturas menos por partida y viven 0,28 más. Con la voz encima, 0,33 menos y 0,35 más.
- **En bestias que crían, la reserva quita muertes de hambre, pero no salva vidas:**
  - RG69r tiene 0,53 muertes de hambre menos por partida, pero la bestia mata más (55 frente a 43 en las 40 partidas; tabla de muertes del informe del v6);
  - las vivas suben +0,23 [−0,23, +0,68], dentro del ruido.
- **En la sequía dura no salva:** las vivas (−0,05), las muertes de hambre (−0,03) y las de la escasez (−0,25) quedan dentro del ruido.
  - En las cuatro clases, unas 3 de cada 3,5 muertes de hambre por partida son en la época de escasez.
- **En la abundancia y el normal no hay nada que salvar:** casi no muere nadie de hambre.

## 4. ¿El hambre del día 10 anuncia la muerte?

*v6, sequía dura, las cuatro clases de criatura.* Al empezar el día 10 (el primer turno del día) estaban vivas 1.265 criaturas en las 160 partidas. Murieron de hambre en los días 10 a 14 **470**, el 37 %.

**Por su hambre ese turno,** en cuatro tramos (los cuartos de las 1.265 juntas):

| clase | hambre menos de 5,1 | de 5,1 a 33,6 | de 33,6 a 63,1 | 63,1 o más |
|---|---|---|---|---|
| RG68r | 27 % (3 de 11) | 29 % (16 de 56) | 34 % (39 de 114) | 52 % (68 de 132) |
| RG068r | 30 % (30 de 101) | 32 % (29 de 92) | 37 % (23 de 62) | 41 % (26 de 64) |
| RG69r | 25 % (23 de 92) | 35 % (29 de 82) | 39 % (26 de 67) | 49 % (37 de 75) |
| RG69r+voz | 36 % (40 de 112) | 40 % (34 de 86) | 44 % (32 de 73) | 33 % (15 de 46) |
| **las cuatro** | **30 %** (96 de 316) | **34 %** (108 de 316) | **38 %** (120 de 316) | **46 %** (146 de 317) |

**Por la comida que tiene ese turno:**

| clase | lleva comida en la bolsa | solo hay en la despensa | ni en la bolsa ni en la despensa |
|---|---|---|---|
| RG68r | 33 % (49 de 148) | — (ninguna) | 47 % (77 de 165) |
| RG068r | 27 % (30 de 110) | 38 % (3 de 8) | 37 % (75 de 201) |
| RG69r | 33 % (36 de 109) | 0 % (0 de 4) | 39 % (79 de 203) |
| RG69r+voz | 32 % (33 de 104) | 50 % (3 de 6) | 41 % (85 de 207) |
| **las cuatro** | **31 %** (148 de 471) | 33 % (6 de 18) | **41 %** (316 de 776) |

**Las dos cosas juntas** (las cuatro clases):

| hambre el día 10 | con comida (bolsa o despensa) | sin comida |
|---|---|---|
| menos de 5,1 | 29 % (59 de 206) | 34 % (37 de 110) |
| de 5,1 a 33,6 | 33 % (55 de 168) | 36 % (53 de 148) |
| de 33,6 a 63,1 | 32 % (25 de 79) | 40 % (95 de 237) |
| 63,1 o más | 42 % (15 de 36) | 47 % (131 de 281) |

**Cuál separa mejor a las que mueren.** Lo mido con el área bajo la curva: la probabilidad de que una criatura que muere esté peor que una que vive, con los empates a la mitad. 0,5 quiere decir que no separa nada y 1, que separa del todo. El intervalo es por bootstrap de las 160 partidas:

| señal | área | intervalo |
|---|---|---|
| el hambre del día 10 | 0,575 | [0,545, 0,605] |
| no tener comida (ni en la bolsa ni en la despensa) | 0,547 | [0,521, 0,572] |
| no llevar comida en la bolsa | 0,546 | [0,520, 0,570] |
| el hambre menos «no tener comida» | +0,029 | [−0,002, +0,058] |

- **El hambre separa algo mejor que la comida,** pero la diferencia toca el cero.
- **Las dos separan poco.** De las que empiezan el día 10 con menos de 5 de hambre muere de hambre el 30 %; de las que empiezan con más de 63, el 46 %.
- **Lo que pasa en los cinco días de escasez pesa más que cómo se llega a ellos.**

## 5. M9, explicada en llano

**Qué mide.**
- En cada decisión, el registro guarda lo que elige la criatura y lo que elegirían «las sumas» en el mismo estado exacto. Las sumas son el valorador de S68: suman ganancias y pérdidas de cada opción.
- También guarda si las dos eligen lo mismo.
- **La ambivalencia de un momento** mide cuánto hay a la vez de bueno y de malo en el estado de la criatura. Por cada una de las tres dimensiones (cuerpo, recursos, vínculo) se toma la menor de su ganancia y su pérdida, y de las tres, la mayor.
- Se toman 2.000 decisiones por mundo y se parten en cuartos por su ambivalencia. **Q4 − Q1** es cuánto más coinciden la criatura y las sumas en el cuarto más ambivalente que en el menos.

**El programa la rehace igual que el evaluador:** la misma muestra, los mismos cuartos y el mismo bootstrap. Con todas las decisiones y sin las de dar, da exactamente lo que guardaron los evaluadores: el v5 +0,042 [+0,011, +0,074], el v6 +0,198 [+0,172, +0,224].

**Q4 − Q1 en cada experimento:**

| decisiones | v5 (RG68r) | v6 (RG69r+voz) | v6 − v5 |
|---|---|---|---|
| todas | +0,042 [+0,011, +0,074] | +0,198 [+0,172, +0,224] | **+0,156 [+0,115, +0,197]** |
| sin las de dar | −0,175 [−0,204, −0,146] | −0,026 [−0,049, −0,003] | **+0,149 [+0,113, +0,185]** |
| sin las de comer | +0,200 [+0,171, +0,229] | +0,228 [+0,200, +0,256] | +0,027 [−0,012, +0,069] |
| sin las de dar ni las de comer | −0,044 [−0,067, −0,021] | −0,024 [−0,048, −0,000] | +0,019 [−0,013, +0,052] |
| sin las de ir (en la misma muestra) | +0,032 [−0,001, +0,065] | +0,240 [+0,214, +0,267] | **+0,208 [+0,167, +0,251]** |

*«Sin las de ir», aquí, quita las de ir de la misma muestra. La cifra de los evaluadores las quita antes de muestrear (v5 +0,072), así que no son la misma medida.*

**Qué hay en cada cuarto.**
- Una decisión es «de dar» si alguna de las dos elige dar. Es «de comer» si alguna elige comer. «De ir» es una decisión de ir a un sitio, y «el resto», todas las demás.
- «Pone» es lo que aporta cada tipo a Q4 − Q1.

| tipo | v5: parte de Q1 · de Q4 | v5: coinciden en Q1 · Q4 | v5: pone | v6: parte de Q1 · de Q4 | v6: coinciden en Q1 · Q4 | v6: pone |
|---|---|---|---|---|---|---|
| dar | 29 % · 4 % | 0 % · 0 % | −0,000 | 30 % · 5 % | 0 % · 2 % | +0,000 |
| comer | 11 % · 24 % | 58 % · **14 %** | −0,030 | 11 % · 22 % | 76 % · **77 %** | +0,083 |
| ir | 8 % · 23 % | 78 % · 73 % | +0,107 | 7 % · 19 % | 77 % · 68 % | +0,069 |
| el resto | 53 % · 49 % | 92 % · 92 % | −0,035 | 51 % · 54 % | 92 % · 94 % | +0,045 |
| todas | | 61 % · 65 % | +0,042 | | 61 % · 81 % | +0,198 |

**En las decisiones de comer,** quién elige comer:

| cuarto | v5 | v6 |
|---|---|---|
| Q1 | 273 decisiones: las dos comen 84 %; solo las sumas 15 % | 285: las dos comen 97 %; solo las sumas 3 % |
| Q4 | 601: las dos comen 16 %; **solo las sumas 83 %** | 550: **las dos comen 85 %**; solo las sumas 13 % |

**Qué ha cambiado del v5 al v6:**
- **En el cuarto menos ambivalente (Q1) no cambia nada:** coinciden el 61 % de las veces en los dos.
- **Todo el cambio está en el cuarto más ambivalente (Q4),** que pasa del 65 % al 81 %. Ahí, una de cada cuatro o cinco decisiones es de comer.
  - En el v5, en esas decisiones las sumas elegían comer y RG68r no, el 83 % de las veces. Es lo que el prompt 145 vio: no se comía lo que llevaba en la bolsa.
  - En el v6, la protagonista lleva la reserva del 146 y come con las sumas el 85 % de las veces.
- **Quitando las decisiones de comer, los dos experimentos dan lo mismo,** dentro del ruido: +0,200 y +0,228, una diferencia de +0,027 [−0,012, +0,069].
- **Quitando las de dar, la subida sigue** (+0,149). Las de dar no explican el cambio: nunca coinciden, ni en el v5 ni en el v6, y pesan igual en los dos (el 29 % y el 30 % de Q1). Por eso, al quitarlas, Q4 − Q1 se vuelve negativa en los dos.
- **Las de ir ponen algo menos en el v6** (+0,069 frente a +0,107). Por eso, sin ellas, la subida es aún mayor.
- La columna «pone» reparte la diferencia entre tipos, pero también depende de cuántas decisiones de cada tipo caen en cada cuarto. Por eso «el resto» también cambia (de −0,035 a +0,045). La prueba limpia es la de quitar un tipo entero, y esa dice que el cambio viene de comer.

No saco ninguna conclusión sobre el motor: esto solo dice qué decisiones han cambiado.

## 6. Las cuatro frases

1. **La gemela vive de más, con las 80 semillas:** +0,24 [+0,06, +0,41] criaturas en la sequía y +0,54 [+0,25, +0,84] en la sequía dura.
2. **En la sequía los dos experimentos cuadran (+0,25 y +0,23); en la sequía dura no** (+0,97 y +0,10; v6 − v5 = −0,88 [−1,43, −0,30]). El desajuste no está en el hambre con que se llega al día 10, que es la misma ventaja de unos 25 puntos en los dos (v6 − v5 = −1,85 [−8,11, +4,32]). Está en cuántas mueren en la primera escasez (v6 − v5 = +0,82 [+0,12, +1,55] muertes por partida).
3. **La reserva salva en la sequía** (RG69r − RG68r: +0,28 [+0,05, +0,50] vivas y −0,23 [−0,45, −0,03] muertes de hambre). En bestias que crían quita muertes de hambre (−0,53 [−0,75, −0,30]) pero no vidas, porque la bestia mata más (+0,23 [−0,23, +0,68] vivas). **En la sequía dura no salva** (−0,05 [−0,40, +0,28] vivas; −0,25 [−0,68, +0,17] muertes de hambre en la escasez).
4. **En la escasez de la sequía dura, ni el hambre del día 10 ni la comida que se tiene anuncian bien la muerte.** El hambre separa algo mejor (área 0,575 [0,545, 0,605], frente a 0,547 [0,521, 0,572] para no tener comida), pero la diferencia toca el cero (+0,029 [−0,002, +0,058]). Incluso de las que empiezan casi sin hambre muere el 30 %.

## Fallos míos y arreglos

- **Python suelto, declarado.** Hubo ocho `python3 -c`, todos de solo leer:
  - tres para ver la forma de `fin.json` y la config de las épocas en una partida del v5 y otra del v6;
  - uno para encontrar el fichero de `cierre_v46` y ver cómo cuenta las vivas;
  - cuatro para leer los resultados guardados de M9 y P11 en los `.json` de los evaluadores.
  Además, este `python3 -` con un texto pegado, para corregir este párrafo.
  El análisis está entero en los dos programas.
- **M9 no se importa: se rehace.** La función del evaluador del v5 (`p11`) no deja separar las decisiones por tipo, así que el programa repite sus pasos. Por eso, antes de separar nada, comprueba que da los mismos números que los dos evaluadores, en la media y en el intervalo. Da los mismos.
- **Los tramos del punto 4 son los cuartos de todas las criaturas juntas.** No se pedía cómo hacerlos y es lo más sencillo.

## Gasto

| bolsa | gasto en el prompt | saldo |
|---|---|---|
| créditos de la plataforma | 0 (no se ha jugado nada) | no lo he leído |
| dólares de la consola de Anthropic | 0 | no lo he leído |

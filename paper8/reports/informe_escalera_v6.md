# La escalera con la reserva: el informe

*19-nov-2026, prompt 152. Las predicciones se sellaron antes de jugar (`predicciones_selladas_v6_escalera.md`, etiqueta `valle-escalera-v6`, commit 24cdb2db). Después de sellar no se ha cambiado ningún umbral ni ningún texto de predicción. Lo que no se cumple se cuenta igual.*

## En pocas palabras

- **E1 se cumple.** Con los cinco mundos juntos, RG69r+voz vive más que S69+voz: **+0,19 [+0,07, +0,32]** vivas el día 40, en 200 parejas.
- **E2 falla.** En la sequía la diferencia es **+0,12 [−0,07, +0,33]**, en 40 parejas. El límite de abajo no pasa de cero.
- **Cuentan 2; se cumple 1.**
- **La ventaja se ha encogido, como se declaró.** Con la base vieja del v5 era +0,41 [+0,27, +0,57]. Ahora es +0,19, menos de la mitad.
- **Frente a P69+voz**, sin predicción: +0,10 [−0,03, +0,23] con los cinco mundos juntos. En ningún mundo por separado es claramente distinta de cero.
- **Donde la protagonista sí se separa con claridad de las otras dos:**
  - empuja mucho menos: de 16 a 60 empujones menos por partida;
  - duerme menos noches fuera;
  - la aldea es más feliz.
  - Esto pasa en los cinco mundos y frente a las dos.

## Lo que se ha hecho

1. **Las puertas y la prueba**, antes de sellar: 3 de 3 idénticas línea a línea, y en 10 días la reserva actúa y la voz suena en los dos jugadores nuevos. Se cuenta en el fichero de predicciones, apartado «Antes de sellar».
2. **El sellado:**
   - commit 24cdb2db y etiqueta `valle-escalera-v6`;
   - `revisa_subida` y `copia_taller` sin hallazgos;
   - push a gemv-coworld (`paintball`) a las 00:35:44 del 19-nov (hora de GitHub: 2026-11-18T23:35:44Z);
   - `git ls-remote` daba la rama y la etiqueta en 24cdb2db.
3. **El experimento:** `lanza_escalera_v6.py experimento 10`, de las 00:35 a las 11:45 del 19-nov.
   - **400 partidas**: S69+voz y P69+voz × 5 mundos × semillas 30161-30200 × 40 días, en la carpeta nueva `valle_escalera_v6`.
   - Ninguna saltada, ninguna fallida, el fichero de errores vacío y las 400 con su `fin.json`.
   - RG69r+voz no se ha vuelto a jugar: sus 200 partidas se leen del v6 sellado.
4. **Las huellas, al acabar:** las mismas que se sellaron (tabla al final).
5. **El evaluador sellado:** `python3 evalua_escalera_v6.py`, 6 minutos y medio, 600 partidas leídas (200 de cada jugador). La salida es `salida/evalua_escalera_v6.md` y `.json`.

## Las predicciones

| | qué | resultado | |
|---|---|---|---|
| **E1** | RG69r+voz − S69+voz, vivas el día 40, los cinco mundos juntos (200 parejas) | **+0,19 [+0,07, +0,32]** | **se cumple** |
| **E2** | lo mismo, solo en la sequía (40 parejas) | **+0,12 [−0,07, +0,33]** | **falla** |

**Por qué falla E2.** En la sequía la protagonista muere mucho menos de hambre que S69+voz: 3 muertes contra 11 en las 40 partidas, una diferencia de −0,20 [−0,35, −0,05] por partida. Pero muere más por la bestia: 5 contra 2. Así, la diferencia de vivas se queda en +0,12 (+5 vivas en 40 partidas) y no alcanza. Es una lectura de los números, no una medida nueva.

## Las vivas el día 40 de los tres jugadores

De 8; media de las 40 semillas.

| mundo | RG69r+voz | S69+voz | P69+voz |
|---|---|---|---|
| abundancia | 8,00 | 8,00 | 7,95 |
| normal | 8,00 | 7,95 | 8,00 |
| sequía | 7,80 | 7,67 | 7,60 |
| sequía dura | 4,22 | 3,73 | 4,05 |
| bestias que crían | 6,65 | 6,38 | 6,55 |
| **los cinco** | **6,93** | **6,75** | **6,83** |

Con los cinco mundos juntos, la escalera va en el orden esperado: RG69r+voz por encima de P69+voz, y P69+voz por encima de S69+voz. Mundo a mundo no siempre: en la abundancia y en la sequía, P69+voz queda por debajo de S69+voz.

## Las medidas sin predicción (punto 5)

Por mundo y emparejadas por semilla, con el intervalo del 95 %. Las celdas `+0,00 [+0,00, +0,00]` son mundos donde los dos jugadores dan lo mismo en todas las semillas.

### Vivas el día 40

| mundo | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|
| abundancia | +0,00 [+0,00, +0,00] | +0,05 [+0,00, +0,15] |
| normal | +0,05 [+0,00, +0,12] | +0,00 [+0,00, +0,00] |
| sequía | +0,12 [−0,07, +0,33] | +0,20 [−0,03, +0,42] |
| sequía dura | **+0,50 [+0,15, +0,85]** | +0,17 [−0,23, +0,57] |
| bestias que crían | +0,28 [−0,17, +0,75] | +0,10 [−0,35, +0,53] |

Frente a S69+voz, la ventaja clara está en la sequía dura. Frente a P69+voz no hay ningún mundo con el límite de abajo por encima de cero.

### Muertes de hambre por partida

| mundo | medias RG69r+voz · S69+voz · P69+voz | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 0,00 · 0,00 · 0,00 | +0,00 | +0,00 |
| normal | 0,00 · 0,00 · 0,00 | +0,00 | +0,00 |
| sequía | 0,07 · 0,28 · 0,28 | **−0,20 [−0,35, −0,05]** | **−0,20 [−0,40, −0,03]** |
| sequía dura | 3,48 · 4,22 · 3,67 | **−0,75 [−1,10, −0,38]** | −0,20 [−0,62, +0,23] |
| bestias que crían | 0,25 · 0,42 · 0,57 | −0,17 [−0,47, +0,07] | **−0,33 [−0,57, −0,07]** |

### Turnos al día despierta con hambre de más de 30 y comida en la bolsa, días 0 a 9

| mundo | medias RG69r+voz · S69+voz · P69+voz | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 1,90 · 1,78 · 2,19 | +0,12 [−0,33, +0,57] | −0,29 [−0,69, +0,15] |
| normal | 3,56 · 2,77 · 3,46 | **+0,78 [+0,17, +1,42]** | +0,10 [−0,59, +0,78] |
| sequía | 2,04 · 2,17 · 2,59 | −0,14 [−0,68, +0,38] | **−0,56 [−1,07, −0,05]** |
| sequía dura | 3,92 · 4,01 · 5,02 | −0,09 [−0,69, +0,50] | **−1,10 [−1,79, −0,38]** |
| bestias que crían | 4,32 · 3,87 · 4,88 | +0,45 [−0,17, +1,08] | −0,56 [−1,15, +0,02] |

Con la reserva puesta, S69+voz deja la comida en la bolsa con hambre tanto como la protagonista; en el mundo normal, incluso menos. P69+voz la deja más, sobre todo en las dos sequías.

### Noches dormidas fuera, días 0 a 9 (parte de las noches, por partida)

| mundo | medias RG69r+voz · S69+voz · P69+voz | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 0,047 · 0,103 · 0,072 | **−0,056 [−0,079, −0,036]** | **−0,025 [−0,040, −0,010]** |
| normal | 0,065 · 0,097 · 0,095 | **−0,032 [−0,051, −0,014]** | **−0,030 [−0,045, −0,015]** |
| sequía | 0,060 · 0,110 · 0,088 | **−0,051 [−0,076, −0,028]** | **−0,028 [−0,044, −0,013]** |
| sequía dura | 0,081 · 0,108 · 0,112 | **−0,027 [−0,051, −0,005]** | **−0,031 [−0,047, −0,015]** |
| bestias que crían | 0,077 · 0,113 · 0,120 | **−0,036 [−0,057, −0,018]** | **−0,044 [−0,061, −0,027]** |

Las tres llevan la misma voz de ir a casa, pero la protagonista duerme fuera menos que las otras dos en los cinco mundos.

### Empujones a otra criatura por partida

| mundo | medias RG69r+voz · S69+voz · P69+voz | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 67,1 · 127,4 · 120,8 | **−60,30 [−74,45, −46,27]** | **−53,70 [−63,73, −43,60]** |
| normal | 120,1 · 136,6 · 142,7 | **−16,50 [−29,82, −3,38]** | **−22,60 [−32,73, −12,18]** |
| sequía | 107,5 · 142,1 · 135,9 | **−34,55 [−52,05, −17,95]** | **−28,38 [−38,40, −19,25]** |
| sequía dura | 72,6 · 98,6 · 92,8 | **−25,98 [−40,02, −11,18]** | **−20,15 [−35,50, −5,20]** |
| bestias que crían | 131,2 · 164,7 · 157,1 | **−33,42 [−46,98, −19,90]** | **−25,82 [−36,92, −14,60]** |

### Felicidad de la aldea

| mundo | medias RG69r+voz · S69+voz · P69+voz | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | 0,921 · 0,895 · 0,885 | **+0,025 [+0,017, +0,034]** | **+0,036 [+0,026, +0,046]** |
| normal | 0,793 · 0,786 · 0,766 | +0,007 [−0,007, +0,022] | **+0,027 [+0,014, +0,041]** |
| sequía | 0,717 · 0,679 · 0,675 | **+0,038 [+0,020, +0,055]** | **+0,042 [+0,026, +0,060]** |
| sequía dura | 0,451 · 0,412 · 0,413 | **+0,039 [+0,009, +0,068]** | **+0,038 [+0,007, +0,068]** |
| bestias que crían | 0,533 · 0,491 · 0,481 | **+0,043 [+0,023, +0,063]** | **+0,053 [+0,027, +0,079]** |

### Muertes por causa

Bestia · hambre · terreno, sumadas en las 40 partidas de cada mundo.

| mundo | RG69r+voz | S69+voz | P69+voz |
|---|---|---|---|
| abundancia | 0 · 0 · 0 | 0 · 0 · 0 | 2 · 0 · 0 |
| normal | 0 · 0 · 0 | 2 · 0 · 0 | 0 · 0 · 0 |
| sequía | 5 · 3 · 0 | 2 · 11 · 0 | 5 · 11 · 0 |
| sequía dura | 9 · 139 · 3 | 2 · 169 · 0 | 9 · 147 · 2 |
| bestias que crían | 42 · 10 · 2 | 48 · 17 · 0 | 35 · 23 · 0 |
| **los cinco** | **56 · 152 · 5** | **54 · 197 · 0** | **51 · 181 · 2** |

La diferencia entre los tres está casi toda en el hambre: 152, 181 y 197 muertes. Por la bestia mueren más o menos igual.

## Cómo ha salido lo declarado (punto 4)

| lo declarado | cómo ha salido |
|---|---|
| RG69r+voz frente a P69+voz no se predice; se mide igual | +0,10 [−0,03, +0,23] con los cinco mundos juntos y +0,20 [−0,03, +0,42] en la sequía. Ninguno pasa de cero por abajo. La protagonista queda por encima en vivas, pero sin separarse con claridad. |
| El lado de RG69r+voz ya se había visto en el v6 | Se ha leído tal cual del v6 sellado. Sus vivas son las del informe del v6 (8,00 / 8,00 / 7,80 / 4,22 / 6,65). |
| La ventaja puede encogerse respecto al +0,41 [+0,27, +0,57] del v5 | **Se ha encogido**, a +0,19 [+0,07, +0,32]. Los dos intervalos casi no se solapan: el de ahora acaba en +0,32 y el del v5 empieza en +0,27. No se ha hecho una prueba de la diferencia entre los dos experimentos. |
| Las gemelas sin ganancias no se vuelven a jugar | No se han jugado. |

## Tropiezos y cosas que declarar

- **Antes de sellar, un arreglo en el evaluador.** En la primera prueba del evaluador faltaba una carpeta de la caché (`noches`). Se arregló antes de sellar y está declarado en el fichero de predicciones. Después de sellar no se ha tocado.
- **Tres veces Python suelto**, todas antes de sellar y solo para leer o rellenar, sin cambiar ninguna medida:
  - un `python3 -c` para ver los interruptores de RG68r, S68 y P68;
  - un `python3 -c` para leer el JSON de las puertas;
  - un `python3 -` para rellenar el apartado «Antes de sellar» del fichero de predicciones.
- **El push del sellado subió también dos commits anteriores:**
  - 84bafe1c, el informe del v6, que era local;
  - e4598d9c, el análisis del v5 y el v6 juntos.
- **Ninguna partida fallida ni repetida.**

## Las huellas al acabar

Las mismas que se sellaron.

| fichero | md5 |
|---|---|
| `predicciones_selladas_v6_escalera.md` | `09264179d2523332bcfa805051a648c4` |
| `lanza_escalera_v6.py` | `a144ce48e3ec82b0cb9ac330f0381e73` |
| `evalua_escalera_v6.py` | `c36e5c219712418ed0c29c12341d7131` |
| `lanza_experimento_v6.py` | `b2e1b7077c3fe81cc5b874ec64757e87` |
| `evalua_experimento_v6.py` | `763dec488835e0783231b6acf2d7d193` |
| `cuerpo_vr1.py` | `82a02353b66626a783ec03d8795be243` |
| `cuerpo_rg69.py` | `393a909fcb095e8a09a230f8170f5fa0` |
| `cuerpo_vc1.py` | `80f68dbc62c538e8a83af53d4a4bb2ec` |
| `lanza_vc1.py` | `5e232b2e0cdcfd479ffbc3a06fa94ac8` |
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` |

## Los datos

- **Las partidas** están en el disco «Mem G-EMV», carpeta `valle_escalera_v6`.
- **La caché del evaluador** está en `evalua_escalera_v6/experimento/`.
- **Los registros del lanzador** están en `salida/logs_escalera/`.
- Ninguno de los tres entra en el commit.

## El gasto

- **Créditos de la plataforma:** 0. No se ha jugado ninguna partida en la plataforma.
- **Dólares de la consola de Anthropic:** 0. No se ha usado la clave.
- **Los saldos** no se han leído en este prompt.

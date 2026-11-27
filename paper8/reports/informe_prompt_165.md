# Prompt 165: qué más cambia en lo que hace la que pierde a su hermana

**Qué es:**
- Solo cuentas sobre las partidas selladas del v6 (semillas 30161 a 30200, los cinco mundos, la protagonista RG69r+voz); no se juega nada.
- Programa: `tras_hermana_165.py`. Salida: `salida/tras_hermana_165.md` y `.json`.
- Las medidas se fijaron antes de mirar, en el commit 8eb9c38f (la sección que va a continuación de la tabla).
- **Ninguna medida es una predicción:** todo es análisis hecho después.

**Casos y controles:** 136 casos y 378 controles, los mismos de A2, de 73 partidas.

**Cómo leer la tabla:**
- El cambio está emparejado por criatura y medido por día. Va con su intervalo del 95 % (`boot` del v6, 10 000 remuestreos, semilla 8).
- «¿Fuera del cero?» dice si el intervalo del cambio en los casos deja fuera el cero.
- La última columna dice lo mismo para «el cambio del caso menos la media del cambio de sus controles». Los controles son los de su partida, medidos desde el mismo día.

## Tabla resumen

| medida (por día) | casos: antes | después − antes [95 %] | ¿fuera del cero? | días 6-15 − antes [95 %] | ¿fuera del cero? | caso − sus controles fuera del cero: después · días 6-15 |
|---|---|---|---|---|---|---|
| comidas que come | 2,99 | +0,38 [+0,33, +0,44] | sí | +0,22 [+0,17, +0,26] | sí | sí · sí |
| hambre media | 22,35 | -3,99 [-6,83, -1,07] | sí | -14,22 [-17,02, -11,51] | sí | no · no |
| comida que coge (total) | 3,76 | +1,47 [+1,06, +1,86] | sí | +1,37 [+0,94, +1,77] | sí | sí · no |
| · de la planta del huerto | 2,12 | +1,48 [+1,25, +1,71] | sí | +1,78 [+1,53, +2,02] | sí | sí · sí |
| · de un matorral | 0,91 | +0,44 [+0,32, +0,56] | sí | +0,07 [-0,05, +0,20] | no | sí · sí |
| · del suelo | 0,13 | +0,08 [+0,02, +0,15] | sí | +0,13 [+0,06, +0,21] | sí | sí · sí |
| · del almacén | 0,01 | -0,01 [-0,03, +0,00] | no | -0,01 [-0,03, +0,00] | no | no · no |
| · de la despensa de su casa | 0,60 | -0,51 [-0,86, -0,22] | sí | -0,60 [-0,97, -0,29] | sí | sí · sí |
| · de la despensa de otra casa | 0,00 | +0,00 [+0,00, +0,00] | no | +0,00 [+0,00, +0,00] | no | no · no |
| comida que da (total) | 0,07 | -0,02 [-0,05, +0,01] | no | -0,04 [-0,06, -0,01] | sí | sí · no |
| · a la hermana | 0,06 | -0,06 [-0,08, -0,04] | sí | -0,06 [-0,08, -0,04] | sí | sí · sí |
| · a las vecinas | 0,01 | +0,04 [+0,01, +0,07] | sí | +0,02 [+0,01, +0,05] | sí | sí · sí |
| turnos de trabajo en el huerto | 21,02 | +14,07 [+10,91, +17,41] | sí | +16,12 [+13,29, +18,98] | sí | sí · sí |
| turnos quieta de día | 95,23 | -25,72 [-33,96, -17,26] | sí | -12,19 [-23,28, -1,57] | sí | sí · sí |
| distancia media a su casa de día (casillas) | 6,34 | +2,00 [+1,47, +2,53] | sí | +1,35 [+0,80, +1,91] | sí | sí · sí |
| noches dentro de su casa (parte) | 0,856 | -0,201 [-0,258, -0,143] | sí | -0,114 [-0,170, -0,058] | sí | sí · sí |
| noches en casa ajena (parte) | 0,006 | +0,040 [+0,024, +0,058] | sí | +0,011 [+0,000, +0,021] | sí | sí · sí |
| noches fuera de las casas (parte) | 0,112 | +0,054 [+0,006, +0,100] | sí | +0,066 [+0,015, +0,117] | sí | sí · sí |
| noches despierta (parte) | 0,026 | +0,106 [+0,076, +0,138] | sí | +0,037 [+0,017, +0,058] | sí | sí · sí |
| con cuántas duerme en la misma casa | 0,782 | -0,716 [-0,759, -0,671] | sí | -0,736 [-0,780, -0,692] | sí | sí · sí |
| empujones que da | 0,36 | -0,18 [-0,28, -0,07] | sí | -0,21 [-0,34, -0,05] | sí | sí · no |
| empujones que recibe | 0,38 | +0,29 [+0,16, +0,42] | sí | +0,09 [-0,04, +0,23] | no | sí · sí |
| llamadas que hace | 39,31 | +29,50 [+17,97, +41,86] | sí | +15,75 [+6,64, +25,15] | sí | sí · sí |
| veces que entra en la zona salvaje | 0,41 | +0,22 [+0,09, +0,36] | sí | +0,16 [-0,01, +0,35] | no | sí · sí |

**Con el intervalo fuera del cero, en los casos:**
- **Los cinco días después:** 21 de 24 medidas. No cambian:
  - coger del almacén;
  - coger de la despensa de otra casa (antes ya eran 0,01 y 0,00 por día);
  - la comida que da, en total.
- **Los días 6 a 15:** 19 de 24 medidas. No cambian:
  - coger de un matorral;
  - coger del almacén;
  - coger de la despensa de otra casa;
  - los empujones que recibe;
  - las entradas en la zona salvaje.

**La hambre media:** baja en los casos, pero frente a sus controles el intervalo toca el cero en las dos ventanas. Antes de la muerte, los casos tenían más hambre que los controles: 22,4 frente a 14,2.

**Lo que miden por fuerza.** Dos medidas cuentan a la hermana por definición, así que tras su muerte la pierden sin más:
- «con cuántas duerme en la misma casa»;
- «comida que da a la hermana».

**Muertes antes del día 40,** contando desde el día de la muerte de la hermana:

| grupo | mueren | de hambre | por la bestia | por el terreno |
|---|---|---|---|---|
| casos | 6 de 136 (4,4 %) | 1 | 4 | 1 |
| controles | 11 de 378 (2,9 %) | 2 | 8 | 1 |

En los controles se cuentan entradas, no criaturas; ver «Lo que tuve que decidir».

## Lo fijado antes de mirar los resultados

Esta sección se escribió y se guardó en un commit local antes de correr las cuentas. Ninguna de estas medidas es una predicción: todo es análisis hecho después, sobre partidas ya selladas.

**Partidas.** Las selladas del v6, `valle_experimento_v6`, semillas 30161 a 30200, los cinco mundos, con la protagonista RG69r+voz («RG69rvoz»). No se juega ni se rejuega nada.

**Casos y controles: los de A2/A4,** tal como los cuenta `seccion5_164.py`. Deberían salir 136 y 378; si no salen, lo digo.
- **Caso:** una criatura cuya hermana muere el día 5 o después, y que vive al menos 5 días más (`duelo_soledad_v6.casos_de`). El día de la muerte de la hermana es *d*.
- **Control:** cada criatura de otra casa de la misma partida que conserva a su hermana, y que sigue viva con ella hasta el día *d* + 5. Se mide desde el mismo día *d* que su caso.

**Ventanas,** en días de 400 turnos:
- **antes:** de *d* − 5 a *d* − 1;
- **después:** de *d* + 1 a *d* + 5;
- **días 6 a 15:** de *d* + 6 a *d* + 15.

El día *d* no entra en ninguna. Un día cuenta solo si la criatura está viva el día entero, y solo hasta el día 39 (la partida dura 40). Cada ventana es la media de sus días que cuentan; si no queda ninguno, esa criatura no entra en esa comparación.

**Comparaciones:**
- **Cambio, emparejado por criatura:** después − antes, y días 6 a 15 − antes. Se da la media de las criaturas con su intervalo del 95 %: `boot` del v6, 10 000 remuestreos, semilla 8. Esto se hace en los casos y, aparte, en los controles.
- **Caso − sus controles:** el cambio del caso menos la media del cambio de sus controles (los de su misma partida y su mismo *d*), con el mismo intervalo.
- **«Cambia»** quiere decir que el intervalo del cambio en los casos no toca el cero. Digo también, para cada medida, si lo toca el de «caso − sus controles».

**Las medidas, por día. Se dan todas, cambien o no:**

1. Comidas que come: «comer» con éxito, de comida.
2. Hambre media: la media de su hambre en los turnos vivos del día.
3. Comida que coge: «coger» con éxito, de comida, en total.
4. a 9. **De dónde la coge** (el campo «de» del registro):
   4. planta del huerto;
   5. matorral;
   6. suelo;
   7. almacén;
   8. despensa de su casa;
   9. despensa de otra casa.

   (Para las despensas se mira en qué casa está la criatura.)
10. Comida que da: «dar» con éxito, de comida, en total.
11. y 12. **A quién la da:**
    11. a la hermana;
    12. a las vecinas.

    Tras la muerte, a la hermana es cero por fuerza; se da igual.
13. Turnos de trabajo en el huerto: «trabajar» con éxito.
14. Turnos quieta de día: «quedarse», en la mañana y la tarde (turnos 0 a 239 del día).
15. Distancia media a su casa de día: la distancia de Chebyshev a la casilla más cercana de su casa (0 dentro), en sus turnos vivos de la mañana y la tarde.
16. a 19. **Dónde pasa la noche.** Es la medida del prompt 162 (`casas_noches_162.noches`, importada): cada noche es del sitio donde duerme más de la mitad de sus turnos de la fase «noche». Las cuatro dan la parte de las noches:
    16. dentro de su casa (con su puerta);
    17. en casa ajena (con su puerta);
    18. fuera de las casas;
    19. despierta: ningún sitio pasa de la mitad.

    Esta última no la pide el prompt; la añado para que las cuatro sumen uno.
20. Con cuántas duerme en la misma casa: las otras criaturas cuya noche es de la misma casa que la suya. Es 0 si duerme fuera o despierta.
21. Empujones que da: «empujar» con resultado (sin «no:») a otra criatura, no a la bestia.
22. Empujones que recibe: los mismos, con ella de objetivo.
23. Llamadas que hace: los turnos con «llama» en `criaturas.jsonl.gz`, que son las llamadas de voz del mundo. Los mensajes de la pieza de voz a la hermana, en `voz_vc1.json`, quedan fuera.
24. Veces que entra en la zona salvaje: pasa de una casilla que no es salvaje a una que sí. Las casillas salvajes salen del mapa del mundo, `valle/mundo.py`, en `celdas_salvaje`.

**Muertes,** contando desde *d*:
- en los casos y en los controles, cuántas mueren antes de que acabe la partida (antes del día 40) y de qué (la «causa» de `fin.json`);
- cuántos días después de *d*: mediana y media.

Con 24 medidas y dos ventanas hay 48 intervalos en los casos. Lo digo para que se lea con eso en mente; no corrijo nada por ello.

## Lo que tuve que decidir

Lo que el prompt no fija, y que resolví por lo más simple:

**Ya en la sección fijada:**
- «de día» = la mañana y la tarde;
- la distancia, de Chebyshev a la casilla más cercana de su casa;
- las noches en la puerta cuentan con su casa;
- las llamadas son el campo «llama».

**Lo que se vio al correr:**
- **Días que faltan:**
  - un caso (bestias_crian, 30171, C1) pierde a la hermana el día 39 y no tiene días después;
  - 11 casos no tienen ningún día entre el 6 y el 15, y 16 tienen menos de 10 (la partida acaba en el día 39);
  - por eso las n de la tabla completa son 135 y 125.
- **Casos sin controles:** 26 casos no tienen ninguno, porque en su partida todas las otras casas pierden a alguna antes de *d* + 5. «Caso − sus controles» se hace con 109 casos (99 en los días 6 a 15).
- **Controles repetidos:** una misma criatura puede ser control de más de un caso de su partida. Las 378 entradas son 274 criaturas distintas. La tabla de muertes cuenta entradas, como el A2.
- **El intervalo:** remuestrea criaturas, no partidas, como pide «emparejado por criatura». Los casos de una misma partida no son independientes entre sí.
- **Coger de una despensa sin estar en una casa:** no pasa ninguna vez. La regla de mirar en qué casa está no deja casos sueltos.

**Un error mío, ya corregido.** En la primera pasada entera, las partidas sin casos no devolvían la cuenta de «despensa sin casa» y el programa paró al juntar los resultados. Lo arreglé y lo relancé. No se había escrito ninguna salida.

## Lo que no se pudo

Nada de lo pedido se quedó sin hacer.

### Tabla completa: los cinco días después, frente a los cinco días de antes

| medida (por día) | casos: antes → ahora | casos: cambio [95 %] (n) | controles: antes → ahora | controles: cambio [95 %] (n) | caso − sus controles [95 %] (n) | ¿fuera del cero? caso · caso − controles |
|---|---|---|---|---|---|---|
| comidas que come | 2,99 → 3,37 | +0,38 [+0,33, +0,44] (135) | 3,05 → 3,09 | +0,04 [+0,01, +0,07] (372) | +0,29 [+0,22, +0,36] (109) | sí · sí |
| hambre media | 22,35 → 18,42 | -3,99 [-6,83, -1,07] (135) | 14,22 → 13,75 | -0,50 [-1,81, +0,83] (372) | -2,39 [-5,56, +0,75] (109) | sí · no |
| comida que coge (total) | 3,76 → 5,22 | +1,47 [+1,06, +1,86] (135) | 4,30 → 4,44 | +0,13 [-0,25, +0,51] (372) | +1,55 [+1,00, +2,10] (109) | sí · sí |
| · de la planta del huerto | 2,12 → 3,58 | +1,48 [+1,25, +1,71] (135) | 2,34 → 2,42 | +0,08 [-0,04, +0,19] (372) | +1,43 [+1,14, +1,73] (109) | sí · sí |
| · de un matorral | 0,91 → 1,34 | +0,44 [+0,32, +0,56] (135) | 0,85 → 0,74 | -0,11 [-0,18, -0,05] (372) | +0,62 [+0,47, +0,78] (109) | sí · sí |
| · del suelo | 0,13 → 0,21 | +0,08 [+0,02, +0,15] (135) | 0,16 → 0,14 | -0,03 [-0,07, +0,03] (372) | +0,13 [+0,04, +0,22] (109) | sí · sí |
| · del almacén | 0,01 → 0,00 | -0,01 [-0,03, +0,00] (135) | 0,02 → 0,00 | -0,02 [-0,04, -0,01] (372) | +0,00 [+0,00, +0,00] (109) | no · no |
| · de la despensa de su casa | 0,60 → 0,10 | -0,51 [-0,86, -0,22] (135) | 0,92 → 1,15 | +0,21 [-0,14, +0,57] (372) | -0,63 [-1,13, -0,16] (109) | sí · sí |
| · de la despensa de otra casa | 0,00 → 0,00 | +0,00 [+0,00, +0,00] (135) | 0,00 → 0,00 | +0,00 [+0,00, +0,00] (372) | +0,00 [+0,00, +0,00] (109) | no · no |
| comida que da (total) | 0,07 → 0,04 | -0,02 [-0,05, +0,01] (135) | 0,07 → 0,08 | +0,02 [-0,00, +0,03] (372) | -0,05 [-0,09, -0,01] (109) | no · sí |
| · a la hermana | 0,06 → 0,00 | -0,06 [-0,08, -0,04] (135) | 0,05 → 0,07 | +0,02 [+0,01, +0,04] (372) | -0,09 [-0,12, -0,06] (109) | sí · sí |
| · a las vecinas | 0,01 → 0,04 | +0,04 [+0,01, +0,07] (135) | 0,02 → 0,01 | -0,01 [-0,02, +0,00] (372) | +0,04 [+0,01, +0,07] (109) | sí · sí |
| turnos de trabajo en el huerto | 21,02 → 35,22 | +14,07 [+10,91, +17,41] (135) | 20,66 → 23,09 | +2,41 [+1,09, +3,76] (372) | +10,01 [+6,21, +13,96] (109) | sí · sí |
| turnos quieta de día | 95,23 → 69,48 | -25,72 [-33,96, -17,26] (135) | 108,81 → 120,03 | +11,11 [+6,71, +15,36] (372) | -42,83 [-53,47, -32,21] (109) | sí · sí |
| distancia media a su casa de día (casillas) | 6,34 → 8,35 | +2,00 [+1,47, +2,53] (135) | 5,68 → 5,28 | -0,38 [-0,59, -0,16] (372) | +2,40 [+1,77, +3,00] (109) | sí · sí |
| noches dentro de su casa (parte) | 0,856 → 0,654 | -0,201 [-0,258, -0,143] (135) | 0,906 → 0,918 | +0,012 [-0,011, +0,034] (372) | -0,213 [-0,286, -0,140] (109) | sí · sí |
| noches en casa ajena (parte) | 0,006 → 0,046 | +0,040 [+0,024, +0,058] (135) | 0,008 → 0,004 | -0,004 [-0,010, +0,001] (372) | +0,042 [+0,024, +0,062] (109) | sí · sí |
| noches fuera de las casas (parte) | 0,112 → 0,167 | +0,054 [+0,006, +0,100] (135) | 0,062 → 0,045 | -0,017 [-0,034, -0,001] (372) | +0,077 [+0,016, +0,135] (109) | sí · sí |
| noches despierta (parte) | 0,026 → 0,133 | +0,106 [+0,076, +0,138] (135) | 0,023 → 0,032 | +0,009 [-0,003, +0,022] (372) | +0,094 [+0,060, +0,130] (109) | sí · sí |
| con cuántas duerme en la misma casa | 0,782 → 0,067 | -0,716 [-0,759, -0,671] (135) | 0,875 → 0,879 | +0,004 [-0,026, +0,034] (372) | -0,726 [-0,794, -0,657] (109) | sí · sí |
| empujones que da | 0,36 → 0,19 | -0,18 [-0,28, -0,07] (135) | 0,41 → 0,53 | +0,12 [+0,05, +0,18] (372) | -0,35 [-0,49, -0,21] (109) | sí · sí |
| empujones que recibe | 0,38 → 0,66 | +0,29 [+0,16, +0,42] (135) | 0,31 → 0,25 | -0,07 [-0,13, -0,01] (372) | +0,46 [+0,31, +0,61] (109) | sí · sí |
| llamadas que hace | 39,31 → 68,09 | +29,50 [+17,97, +41,86] (135) | 37,28 → 27,32 | -9,59 [-13,12, -6,10] (372) | +43,35 [+28,86, +58,89] (109) | sí · sí |
| veces que entra en la zona salvaje | 0,41 → 0,64 | +0,22 [+0,09, +0,36] (135) | 0,31 → 0,23 | -0,07 [-0,12, -0,02] (372) | +0,34 [+0,18, +0,50] (109) | sí · sí |

### Tabla completa: los días 6 a 15 después, frente a los cinco días de antes

| medida (por día) | casos: antes → ahora | casos: cambio [95 %] (n) | controles: antes → ahora | controles: cambio [95 %] (n) | caso − sus controles [95 %] (n) | ¿fuera del cero? caso · caso − controles |
|---|---|---|---|---|---|---|
| comidas que come | 2,99 → 3,20 | +0,22 [+0,17, +0,26] (125) | 3,05 → 3,05 | +0,00 [-0,02, +0,03] (323) | +0,21 [+0,15, +0,27] (99) | sí · sí |
| hambre media | 22,35 → 8,19 | -14,22 [-17,02, -11,51] (125) | 14,22 → 7,14 | -7,16 [-8,53, -5,81] (323) | -2,52 [-5,50, +0,28] (99) | sí · no |
| comida que coge (total) | 3,76 → 5,15 | +1,37 [+0,94, +1,77] (125) | 4,30 → 4,78 | +0,51 [+0,08, +0,96] (323) | +0,63 [-0,14, +1,34] (99) | sí · no |
| · de la planta del huerto | 2,12 → 3,89 | +1,78 [+1,53, +2,02] (125) | 2,34 → 2,85 | +0,51 [+0,38, +0,64] (323) | +0,97 [+0,67, +1,27] (99) | sí · sí |
| · de un matorral | 0,91 → 0,95 | +0,07 [-0,05, +0,20] (125) | 0,85 → 0,67 | -0,16 [-0,23, -0,09] (323) | +0,35 [+0,19, +0,50] (99) | no · sí |
| · del suelo | 0,13 → 0,26 | +0,13 [+0,06, +0,21] (125) | 0,16 → 0,14 | -0,03 [-0,08, +0,01] (323) | +0,19 [+0,10, +0,28] (99) | sí · sí |
| · del almacén | 0,01 → 0,00 | -0,01 [-0,03, +0,00] (125) | 0,02 → 0,00 | -0,02 [-0,04, -0,01] (323) | +0,00 [+0,00, +0,00] (99) | no · no |
| · de la despensa de su casa | 0,60 → 0,05 | -0,60 [-0,97, -0,29] (125) | 0,92 → 1,12 | +0,22 [-0,19, +0,63] (323) | -0,88 [-1,57, -0,26] (99) | sí · sí |
| · de la despensa de otra casa | 0,00 → 0,00 | +0,00 [+0,00, +0,00] (125) | 0,00 → 0,00 | +0,00 [+0,00, +0,00] (323) | +0,00 [+0,00, +0,00] (99) | no · no |
| comida que da (total) | 0,07 → 0,03 | -0,04 [-0,06, -0,01] (125) | 0,07 → 0,03 | -0,04 [-0,06, -0,02] (323) | +0,01 [-0,03, +0,05] (99) | sí · no |
| · a la hermana | 0,06 → 0,00 | -0,06 [-0,08, -0,04] (125) | 0,05 → 0,02 | -0,02 [-0,04, -0,01] (323) | -0,03 [-0,06, -0,00] (99) | sí · sí |
| · a las vecinas | 0,01 → 0,03 | +0,02 [+0,01, +0,05] (125) | 0,02 → 0,01 | -0,02 [-0,03, -0,01] (323) | +0,04 [+0,02, +0,06] (99) | sí · sí |
| turnos de trabajo en el huerto | 21,02 → 37,48 | +16,12 [+13,29, +18,98] (125) | 20,66 → 23,31 | +2,61 [+1,38, +3,90] (323) | +12,80 [+9,17, +16,42] (99) | sí · sí |
| turnos quieta de día | 95,23 → 83,57 | -12,19 [-23,28, -1,57] (125) | 108,81 → 132,08 | +22,02 [+17,61, +26,53] (323) | -48,26 [-60,20, -36,05] (99) | sí · sí |
| distancia media a su casa de día (casillas) | 6,34 → 7,69 | +1,35 [+0,80, +1,91] (125) | 5,68 → 4,61 | -1,06 [-1,31, -0,82] (323) | +2,66 [+2,04, +3,29] (99) | sí · sí |
| noches dentro de su casa (parte) | 0,856 → 0,735 | -0,114 [-0,170, -0,058] (125) | 0,906 → 0,936 | +0,027 [+0,006, +0,047] (323) | -0,119 [-0,182, -0,056] (99) | sí · sí |
| noches en casa ajena (parte) | 0,006 → 0,017 | +0,011 [+0,000, +0,021] (125) | 0,008 → 0,003 | -0,006 [-0,011, -0,001] (323) | +0,020 [+0,007, +0,036] (99) | sí · sí |
| noches fuera de las casas (parte) | 0,112 → 0,183 | +0,066 [+0,015, +0,117] (125) | 0,062 → 0,031 | -0,033 [-0,048, -0,017] (323) | +0,071 [+0,013, +0,128] (99) | sí · sí |
| noches despierta (parte) | 0,026 → 0,064 | +0,037 [+0,017, +0,058] (125) | 0,023 → 0,031 | +0,012 [-0,000, +0,024] (323) | +0,029 [+0,004, +0,054] (99) | sí · sí |
| con cuántas duerme en la misma casa | 0,782 → 0,041 | -0,736 [-0,780, -0,692] (125) | 0,875 → 0,891 | +0,012 [-0,019, +0,042] (323) | -0,756 [-0,822, -0,687] (99) | sí · sí |
| empujones que da | 0,36 → 0,16 | -0,21 [-0,34, -0,05] (125) | 0,41 → 0,40 | -0,00 [-0,07, +0,07] (323) | -0,20 [-0,38, +0,01] (99) | sí · no |
| empujones que recibe | 0,38 → 0,46 | +0,09 [-0,04, +0,23] (125) | 0,31 → 0,19 | -0,13 [-0,18, -0,08] (323) | +0,29 [+0,14, +0,47] (99) | no · sí |
| llamadas que hace | 39,31 → 54,25 | +15,75 [+6,64, +25,15] (125) | 37,28 → 24,99 | -10,81 [-15,51, -6,11] (323) | +33,36 [+20,90, +46,18] (99) | sí · sí |
| veces que entra en la zona salvaje | 0,41 → 0,58 | +0,16 [-0,01, +0,35] (125) | 0,31 → 0,18 | -0,11 [-0,18, -0,05] (323) | +0,38 [+0,16, +0,62] (99) | no · sí |

### Muertes antes del día 40, contando desde el día de la muerte de la hermana

| grupo | criaturas | mueren antes del día 40 | de hambre | por la bestia | por el terreno | otra causa | días después de d: mediana · media |
|---|---|---|---|---|---|---|---|
| pierde a la hermana | 136 | 6 (4,4 %) | 1 | 4 | 1 | 0 | 16,8 · 14,3 |
| la conserva (control) | 378 | 11 (2,9 %) | 2 | 8 | 1 | 0 | 18,1 · 15,3 |

## Tiempo, gasto y procesos

**Tiempo:** cada pasada por las 200 partidas tarda alrededor de 1 minuto, con 6 procesos. El pico de memoria fue de unos 100 MB por proceso.

**Gasto:**
- créditos de la plataforma: 0 (no se juega nada);
- dólares de la consola de Anthropic: 0 (ninguna llamada).

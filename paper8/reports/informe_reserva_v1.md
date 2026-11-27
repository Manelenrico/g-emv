# Valle · prompt 146 · El taller de la reserva (RG69r)

**La regla PASA.**
- **a) Mecanismo:** en sequía y sequía dura juntas, días 0 a 9, los turnos al día despierta con hambre > 30 y comida en la bolsa bajan de **30,3** (RG68r sellada) a **3,3**. Es un cociente de 0,110 [0,097, 0,124], y hacía falta 0,5 o menos.
- **b) No hace daño en ningún mundo.** En los cuatro:
  - las vivas el día 40 suben o quedan igual;
  - la felicidad de la aldea no baja más de 0,003;
  - los empujones no suben.

**Qué es esto:**
- **Un taller:** un solo intento, nada sellado. No cambia el congelado ni las predicciones selladas.
- **Lo que no se ha tocado:** `model.py` ni la clase RG68r.
- **Sin modelo de lenguaje. Gasto: cero.**

**Los programas:**
- `cuerpo_rg69.py`: la clase hija con el cambio;
- `lanza_rg69.py`: la puerta y el taller;
- `reserva_v1/analiza_rg69.py`: la regla y las tablas, que van a `analiza_rg69.md` y `.json`;
- `reserva_v1/historias_rg69.py`: las tres historias;
- `reserva_v1/gif_rg69.py`: el GIF.

Las reglas de cada uno están en su cabecera, fijadas antes de mirar los resultados.

## 1. El cambio y la puerta

**Dónde está el cambio:** en la capa de la criatura, en la clase hija `cuerpo_rg69.RG69` (de `cuerpo_valle.Criatura`). `model.py` no hace falta.

**La decisión de Manel:** con hambre para poder comer (≥ 15, `harta_por_debajo`, leída de `valle/config_valle.json`), comerse lo que lleva no es perder recursos.

**Qué hace:** en la foto de «comerse ahora una comida», y solo ahí, las cuentas de recursos leen la bolsa como si esa comida siguiera dentro.
- **Lo que no cambia:** las fotos de las demás acciones, el hambre que quita, el gusto y las otras filas. Ningún número nuevo.

**Una elección mía, que hay que decir:** el prompt nombraba V-RECURSOS. Pero en la foto de comer hay dos filas que cuentan la comida guardada:
- **V-RECURSOS:** la ganancia por la comida que tiene (`vivir_bien`).
- **R-CARENCIA:** la pérdida por la que le falta (`falta_comida`). En el 145 era una de las filas que más hundían «comer».

He neutralizado las dos, porque «no cuenta como pérdida de recursos» abarca las dos cuentas. Si Manel quiere solo V-RECURSOS, es un taller aparte.

**La puerta pasa** (`salida/puerta_rg69.json`, días 0 a 9):

| partida | mundo, línea a línea | criaturas, línea a línea | fotos que usaron la reserva |
|---|---|---|---|
| RG69r con el cambio apagado, sequía dura 30121 | idéntico a RG68r sellada | idéntico | 0 |
| RG69r con el cambio apagado, sequía 30121 | idéntico | idéntico | 0 |
| RG69r con el cambio encendido, sequía dura 30121 | distinto (el cambio actúa) | distinto | 7.683 |

**El taller:** 60 partidas de 40 días, todas acabadas. Fueron 20 semillas (30121 a 30140) de sequía dura y 20 de sequía, y 10 (30121 a 30130) de normal y 10 de bestias que crían.
- **Con qué se compara:** con la RG68r sellada y la gemela RG068r del v5, emparejadas por semilla y sin volver a jugarlas.
- **Cuánto se usa la reserva:** de media, 30.124 fotos de comer por partida.

## 2. La regla

| mundo | vivas el día 40, RG69r − RG68r (≥ −0,2) | felicidad de la aldea (≥ −0,03) | empujones RG69r / RG68r (≤ 1,25) | se cumple |
|---|---|---|---|---|
| sequía dura | **+0,90** [+0,45, +1,35] | −0,003 | 0,99 (86,8 / 88,0) | sí |
| sequía | +0,30 [+0,00, +0,60] | +0,017 | 0,88 (126,9 / 143,7) | sí |
| normal | +0,00 | −0,003 | 0,99 (131,1 / 131,8) | sí |
| bestias que crían | +0,30 [−0,40, +1,00] | +0,051 | 0,99 (151,0 / 153,1) | sí |

## 3. Las vidas, también frente a la gemela (no era condición)

| mundo | vivas el día 40: RG69r | RG68r | gemela | RG69r − RG68r [95 %] | RG69r − gemela [95 %] |
|---|---|---|---|---|---|
| sequía dura | 4,30 | 3,40 | 4,70 | +0,90 [+0,45, +1,35] | −0,40 [−0,90, +0,15] |
| sequía | 7,70 | 7,40 | 7,85 | +0,30 [+0,00, +0,60] | −0,15 [−0,45, +0,15] |
| normal | 7,90 | 7,90 | 8,00 | +0,00 [−0,30, +0,30] | −0,10 [−0,30, +0,00] |
| bestias que crían | 6,80 | 6,50 | 6,70 | +0,30 [−0,40, +1,00] | +0,10 [−0,80, +1,00] |

**De dónde salen las vidas en sequía dura:** de hambre (muertes de hambre 3,30 frente a 4,20). Ya mueren menos hasta el día 14 (3,30 frente a 4,25).

**Frente a la gemela:** la distancia de sequía dura baja de −1,30 (la que había en el v5) a −0,40, y el intervalo ya toca el cero. No llega a igualarla.

## 4. Lo demás que pedía contar

Días 0 a 9 en las medidas que vienen del 144 (marcadas «0-9»). El resto es la partida entera o el día que se dice.

| medida | sequía dura: RG69r | RG68r | gemela | sequía: RG69r | RG68r | gemela |
|---|---|---|---|---|---|---|
| turnos despierta con hambre > 30 y comida en la bolsa, por criatura y día (0-9) | **4,2** | 42,3 | 6,2 | **2,5** | 18,3 | 3,5 |
| ídem, con hambre > 60 (0-9) | 0,5 | 8,3 | 0,9 | 0,1 | 2,4 | 0,3 |
| turnos despierta con hambre > 30 sin comida en ninguna parte (0-9) | 19,4 | 28,3 | 17,1 | 2,1 | 5,2 | 3,4 |
| hambre al comer, media (0-9) | **25,5** | 36,0 | 26,3 | **21,2** | 25,7 | 22,4 |
| comidas con 60 o más de hambre (0-9) | **5,2 %** | 19,3 % | 5,5 % | **0,5 %** | 4,9 % | 1,3 % |
| comidas por criatura y día (0-9) | 3,03 | 2,96 | 2,97 | 3,04 | 2,99 | 2,98 |
| comida que le quitan a empujones, parte de lo que coge (0-9) | 26,2 % | 28,5 % | 17,7 % | 23,1 % | 24,9 % | 15,4 % |
| hambre al empezar el día 10 (las vivas) | **31,1** | 48,7 | 24,8 | **3,6** | 21,1 | 3,4 |
| vivas sin comida en la bolsa ni en la despensa, día 10 (por partida) | 5,15 de 7,9 | 3,55 de 7,7 | 4,55 de 7,95 | 1,35 | 0,95 | 1,40 |
| ídem, día 30 | 1,05 de 4,3 | 0,35 de 3,55 | 2,05 de 4,75 | 1,35 | 0,60 | 1,95 |
| noches fuera, días 0 a 9 | 25,5 % | 23,4 % | 5,6 % | 24,4 % | 22,7 % | 5,6 % |

**Normal y bestias que crían van igual:**
- los turnos con hambre y comida encima bajan de 31,1 a 4,5 y de 48,1 a 4,9;
- el hambre al empezar el día 10 baja en 14 y en 19.

Las tablas completas, con los intervalos de los cuatro mundos, están en `reserva_v1/analiza_rg69.md`.

**Lo que no arregla:**
- **Lo que le quitan a empujones apenas baja,** 2 puntos, y sigue unos 8 puntos por encima de la gemela.
- **Las noches fuera no cambian,** alrededor del 23-25 % frente al 5 % de la gemela. La reserva no las toca: eso era la voz de ir a casa (143).
- **Llega más veces con la bolsa y la despensa vacías al día 10 y al 30:**
  - en sequía dura, 5,15 frente a 3,55 el día 10 (+1,60 [+0,65, +2,50]);
  - el día 30, 1,05 frente a 0,35.

  Se come la reserva en vez de cargarla, pero llega al día 10 con mucha menos hambre (31 frente a 49). En el día 30 está más cerca de la gemela (2,05) que de la sellada. La felicidad de la peor parada en sequía dura baja un poco: −0,03 [−0,06, −0,00].

## Tres frases

1. **Con el cambio, se come lo que lleva:** los turnos con hambre y comida encima bajan de 30,3 a 3,3 en las sequías, por debajo incluso de la gemela (4,9).
2. **Pasa la regla sin hacer daño:**
   - **sequía dura:** +0,90 vivas el día 40 frente a la sellada y 17,7 menos de hambre al empezar el día 10;
   - **los otros tres mundos:** no pierden nada.
3. **No llega a la gemela** (−0,40 vivas en sequía dura, intervalo que toca el cero): sigue durmiendo fuera, perdiendo más comida a empujones y llegando más veces sin reserva a la escasez.

## Tres historias (a suertes, `reserva_v1/historias_rg69.md`)

**Cómo se escogen:** de 1.587 criatura-días de sequía dura (días 0 a 9) vivos en las dos partidas, tres a suertes con `random.Random(8)`, fijado antes de mirar.

**Sequía dura 30126, D1, día 4:**
- **RG68r sellada:** come 2 veces, con hambre 19 y 43. Pasa 35 turnos despierta con hambre y comida en la bolsa. Coge 5 y le quitan 2 a empujones.
- **RG69r:** come 3 veces, con hambre 27, 15 y 15. Pasa 0 turnos con hambre y comida encima. Coge 5 y no le quitan ninguna.

**Sequía dura 30130, B2, día 8:**
- **RG68r sellada:** come 3 veces, con hambre 47, 40 y 15. Pasa 59 turnos con hambre y comida encima. Coge 4 y no le quitan ninguna.
- **RG69r:** come 3 veces, con hambre 31, 42 y 41. Pasa 11 turnos con hambre y comida encima. **Pasa 51 turnos con hambre sin comida en ninguna parte,** porque se ha comido la reserva antes. Coge 4 y le quitan 1.

  Es la cara mala de la tabla: llegar sin reserva.

**Sequía dura 30130, C1, día 8:**
- **RG68r sellada:** come 3 veces, con hambre 52, 21 y 15. Pasa 87 turnos con hambre y comida encima, y coge 6.
- **RG69r:** come 3 veces, con hambre 30, 15 y 15. Pasa 0 turnos con hambre y comida encima. No coge nada nuevo en todo el día: le basta con lo que ya llevaba.

## El GIF (`reserva_v1/gif_rg69.gif`, fuera del commit como todos los GIF)

**Qué muestra:** sequía dura 30128, B1 (en rojo) y su hermana B2 (en azul), días 8 a 12. A la izquierda la RG68r sellada y a la derecha RG69r.
- **El fotograma:** uno cada 4 turnos, 500 en total.
- **Cómo se escogió:** a suertes (`random.Random(8)`) entre las 158 criatura-semilla vivas al empezar el día 8 en las dos partidas.
- **Cómo se hace:** de los datos crudos, con matplotlib.
- **El primer fotograma:** las dos llevan 4 comidas. La sellada come con hambre 5 y RG69r se queda quieta con hambre 12.

## Lo más sencillo que escogí

- **R-CARENCIA también neutralizada.** Está explicado en el punto 1.
- **«Hambre para poder comer»:** es el hambre de ahora de la criatura (la que ve al decidir), no la de la foto.
- **La regla a):** la media de las 40 partidas de sequía y sequía dura juntas, por criatura y día viva, como en el 144. El intervalo es un bootstrap del cociente por semillas.
- **«Bolsa y despensa vacías»:** las vivas sin ninguna comida en la bolsa y con la despensa de su casa a cero de comida, en el primer turno del día 10 y del 30.
- **Las medidas de las selladas:** se leen de lo ya medido en el 143 y el 144. Las de normal y bestias que crían del 144 se midieron ahora sobre las selladas del v5, sin volver a jugarlas.

## Tropiezos

Ninguno ha cambiado un número:
- `historias_rg69.py` pedía un dato que el extractor del 144 no guarda (lo que lleva de media). Quité esa frase.
- `analiza_rg69.py` tenía las medidas del 143 en otro orden y falló al empezar. Se arregló y se volvió a pasar.
- `gif_rg69.py` falló porque las muertas pueden faltar del registro del mundo. Ahora cuentan como muertas.
- **Python suelto:** ninguno. Para ver el primer fotograma del GIF usé `sips`, la herramienta de imágenes de macOS.

## Gasto

- **Créditos de la plataforma:** 0, porque no se jugó en la plataforma. No he leído el saldo.
- **Dólares de la consola de Anthropic:** 0, porque no se llamó a ningún modelo.

**Procesos vivos al acabar:** ninguno.

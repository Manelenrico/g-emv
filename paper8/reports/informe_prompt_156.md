# Prompt 156: la felicidad día a día, la figura D, cuándo, y el GIF v3

*19-nov-2026. Solo se ha leído: ninguna partida jugada, nada sellado tocado y la clave sin usar. Todo es análisis hecho después de ver los datos, no predicción. No se proponen causas.*

## Parte 1: la felicidad y los empujones día a día

Hecho con un programa nuevo, `felicidad_dia_a_dia.py`. La salida está en `salida/felicidad_dia_a_dia.md` y `.json`. Las cuentas de cada partida van a `felicidad_dia_a_dia/partidas.json`, que queda fuera del commit.

- **La felicidad del día**, por partida y día:
  - por criatura viva, la parte de sus turnos despierta de ese día con los tres balances de las seis a la vez por encima de cero (la condición de `evalua_experimento_v5.v5`, en un solo día);
  - la aldea, la media de las vivas que tienen algún turno despierta ese día;
  - se enseña de 0 a 100.
- **Los empujones del día**, contados como en `cierre_v46`.
- **Las 600 partidas:** tres jugadores, cinco mundos y 40 semillas.
- **Para cada día del 1 al 40**, la media de las 40 semillas con su intervalo del 95 % (el bootstrap de siempre: 10.000 remuestreos, semilla 8).
- **Los días se enseñan del 1 al 40**: el dato 0 es el día 1.

**Los días de escasez de cada mundo** salen de la regla del propio mundo:
- La regla (`valle/mundo.py`, `Valle.epoca`): la época del día es `nombres[(día // duracion_dias) % número de factores]`, solo si las épocas están activas.
- En la sequía dura, las épocas son las de `estres.sequia_dura` con cada factor multiplicado por su «multiplica» (líneas 254-257).
- Los números salen de lo que se jugó, en el `fin.json` de cada mundo.
- **Un día es de escasez** si su época se llama «escasez» y su factor está por debajo de 1.
  - **Lo puse yo:** en la abundancia, la época que se llama «escasez» tiene factor 1,3, no baja nada y no la marco.
  - En la sequía dura, con el «multiplica», todos los factores quedan por debajo de 1. Por eso no basta con «factor < 1», que marcaría los 40 días.
- **Lo que queda:**
  - sequía: días 11-15 y 31-35;
  - sequía dura: días 11-15 y 31-35;
  - abundancia, normal y bestias que crían: ninguno.

## Parte 2: la figura D

Dibujada con el mismo programa, en PNG (200 puntos por pulgada) y PDF:
- **`figuras/escalera_D_felicidad_dia_a_dia`:**
  - cinco paneles pequeños, uno por mundo;
  - el día en el eje de abajo (1 a 40) y la felicidad de 0 a 100;
  - tres líneas con su banda del 95 %;
  - los colores y rótulos de las figuras A, B y C («decide con el motor», «decide sumando», «decide con la posición»);
  - los días de escasez, con una banda naranja suave;
  - la leyenda en el sexto hueco.
- **`figuras/escalera_D_sequia`:** la misma, solo con la sequía y en grande, con letra de 15 puntos.

Las he mirado y se leen bien.

## Parte 3: cuándo

Diferencias emparejadas por semilla, con intervalo del 95 %. Felicidad de la aldea del día, de 0 a 100; por partida, la media de los días del tramo.

### Sequía: felicidad

| tramo | días | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|---|
| antes de la primera | 1-10 | 89,1 · 85,8 · 84,4 | +3,3 [+1,3, +5,4] | +4,7 [+2,7, +6,8] |
| durante la primera | 11-15 | 53,6 · 49,0 · 45,7 | +4,6 [+1,2, +7,9] | +7,9 [+3,9, +11,9] |
| entre las dos | 16-30 | 75,9 · 72,5 · 72,3 | +3,4 [+0,6, +6,0] | +3,5 [+0,8, +6,3] |
| durante la segunda | 31-35 | 57,6 · 52,2 · 54,2 | +5,4 [+1,5, +9,3] | +3,4 [−0,0, +6,9] |
| después de la segunda | 36-40 | 59,9 · 56,3 · 58,2 | +3,6 [−1,1, +8,4] | +1,7 [−2,1, +5,5] |

### Sequía: empujones por día

| tramo | días | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|---|
| antes de la primera | 1-10 | 2,8 · 6,6 · 4,7 | −3,8 [−4,9, −2,7] | −1,9 [−2,6, −1,2] |
| durante la primera | 11-15 | 3,5 · 2,8 · 4,0 | +0,7 [+0,0, +1,3] | −0,6 [−1,4, +0,2] |
| entre las dos | 16-30 | 2,3 · 2,6 · 2,6 | −0,3 [−1,0, +0,3] | −0,3 [−0,9, +0,1] |
| durante la segunda | 31-35 | 2,8 · 2,2 · 2,7 | +0,6 [−0,0, +1,2] | +0,1 [−0,4, +0,6] |
| después de la segunda | 36-40 | 2,8 · 2,4 · 3,2 | +0,4 [−0,4, +1,2] | −0,3 [−1,1, +0,4] |

### Sequía dura: felicidad

| tramo | días | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|---|
| antes de la primera | 1-10 | 71,4 · 66,7 · 64,7 | +4,7 [+2,0, +7,4] | +6,7 [+4,2, +9,2] |
| durante la primera | 11-15 | 10,2 · 5,5 · 7,4 | +4,7 [+2,5, +7,0] | +2,8 [+0,7, +4,9] |
| entre las dos | 16-30 | 30,6 · 25,6 · 29,7 | +5,1 [−3,4, +13,3] | +0,9 [−7,3, +9,4] |
| durante la segunda | 31-35 | 26,2 · 17,9 · 21,9 | +8,3 [+0,6, +16,1] | +4,3 [−3,5, +12,0] |
| después de la segunda | 36-40 | 29,7 · 19,7 · 26,0 | +10,0 [+1,5, +18,0] | +3,7 [−4,3, +11,7] |

### Sequía dura: empujones por día

| tramo | días | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|---|
| antes de la primera | 1-10 | 3,7 · 6,4 · 5,2 | −2,7 [−3,5, −1,9] | −1,6 [−2,1, −1,1] |
| durante la primera | 11-15 | 1,7 · 1,4 · 1,5 | +0,3 [−0,2, +0,8] | +0,2 [−0,4, +0,7] |
| entre las dos | 16-30 | 1,2 · 1,4 · 1,5 | −0,2 [−0,8, +0,5] | −0,3 [−1,0, +0,3] |
| durante la segunda | 31-35 | 1,1 · 0,8 · 1,0 | +0,3 [−0,2, +0,8] | +0,1 [−0,5, +0,6] |
| después de la segunda | 36-40 | 0,8 · 0,7 · 1,0 | +0,1 [−0,5, +0,6] | −0,2 [−0,8, +0,4] |

**Lo que se ve:**
- **En la felicidad**, decide con el motor va por delante en todos los tramos de las dos sequías. Fuera de la primera mitad, varios intervalos tocan el cero.
- **En los empujones**, la diferencia está casi toda en los días 1 a 10. Después de la primera escasez, los tres empujan más o menos igual.

**Los últimos días.** En el conjunto de las semillas, RG69r+voz no queda por detrás:
- en los días 36 a 40 de la sequía va por delante, +3,6 [−1,1, +8,4] frente a S69+voz y +1,7 [−2,1, +5,5] frente a P69+voz, con los dos intervalos tocando el cero;
- el día 40 no hay diferencia clara: −2,2 [−7,1, +2,9] frente a S69+voz y +1,4 [−3,3, +5,9] frente a P69+voz.

Queda por detrás solo en la semilla 30182, y solo el día 40: 78 frente a 90 y 90. En los días 36 a 40 de esa misma semilla va por delante: 66,6 frente a 46,7 y 51,1.

## Parte 4: el GIF v3

- **El programa:** `gif_partida_entera_v3.py`, una copia de `gif_partida_entera_v2.py` con solo tres cambios.
- **El fichero:** `figuras/tres_aldeas_sequia_30182_v3.gif`. Los anteriores siguen en su sitio.
- **Los tres cambios:**
  1. **Una segunda barra de la aldea** al lado de la oscura, con la felicidad de toda la partida hasta ese momento: la medida de siempre desde el turno 0, como el GIF del 154. Es gris clara, con trama y borde oscuro. Las dos barras se rotulan «hoy» y «toda la partida».
  2. **Una línea de leyenda abajo del todo:** «punto hueco, dormida · X, la bestia · fondo naranja, escasez».
  3. **El último fotograma se queda quieto 4 segundos.**
- **Duración y tamaño:**
  - **52 segundos** y **6,8 MB**, con el último fotograma quieto 4,1 segundos;
  - lo he medido leyendo el GIF;
  - el GIF guarda la duración de cada fotograma en centésimas, así que los 125 ms se quedan en 120: por eso dura 52 segundos y no 54;
  - Pillow junta en uno los fotogramas iguales del final.
- **Al acabar**, la barra «toda la partida» da 70, 64 y 61, lo mismo que el GIF del 154, y la barra «hoy» da 78, 90 y 90.
- **Los cuatro fotogramas sueltos** (PNG), los días 5, 12 y 16 a media mañana, como en el v2:
  - `figuras/tres_aldeas_sequia_30182_v3_dia05.png`;
  - `figuras/tres_aldeas_sequia_30182_v3_dia12.png`;
  - `figuras/tres_aldeas_sequia_30182_v3_dia16.png`;
  - `figuras/tres_aldeas_sequia_30182_v3_dia40.png`.

## Lo que no se ha podido o hay que saber

- **La línea de leyenda de arriba** sigue diciendo «y, oscura, la media de la aldea», como en el v2. El prompt pedía que lo demás quedase igual. La barra nueva se explica con sus rótulos «hoy» y «toda la partida».
- **La tabla de los tramos** solo tiene sentido en las dos sequías, que son los mundos con escasez. En los otros tres no hay tramos.

## Tropiezos

- **El panel de la sequía** de la figura D salía sin los números de los días: está en la fila de arriba y no tiene panel debajo. Lo arreglé y volví a dibujar con la caché.
- **La primera línea de los días de escasez** del informe se paraba en los mundos sin escasez. La cambié por una función más sencilla antes de correr el programa.
- **Python suelto: lo declaro.** Usé una vez `python3 -I -c` para leer la duración de los fotogramas del GIF, que solo lee el fichero.
- **Los cambios al programa del GIF** los hice con `sed`, sobre la copia nueva.

## Lo que entra en el commit

**Entra:**
- este informe;
- `felicidad_dia_a_dia.py` y su salida (`salida/felicidad_dia_a_dia.md` y `.json`);
- las figuras D en PNG y PDF;
- `gif_partida_entera_v3.py` y sus cuatro fotogramas en PNG;
- la línea de STATUS.

**Queda fuera:**
- el GIF;
- la caché de las cuentas por partida;
- los datos de las partidas.

Commit local, sin push.

## El gasto

- **Créditos de la plataforma:** 0.
- **Dólares de la consola de Anthropic:** 0.
- **Los saldos** no se han leído.

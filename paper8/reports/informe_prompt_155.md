# Prompt 155: la felicidad solo de las vivas, y el GIF rehecho

*19-nov-2026. Solo se ha leído: ninguna partida jugada, nada sellado tocado y la clave sin usar. Todo es análisis hecho después de ver los datos, no predicción.*

## Parte 1: la felicidad de la aldea contando solo a las que llegan vivas

Hecho con `felicidad_solo_vivas.py`; la salida está en `salida/felicidad_solo_vivas.md` y `.json`.

- **Cómo se cuenta.** Cada criatura, igual que siempre: la parte de sus turnos vivos y despierta con los tres balances de las seis por encima de cero. Solo cambia quién entra en la media de la aldea: las que siguen vivas en el último turno de la partida.
- **La comprobación.** La medida de siempre, rehecha en el mismo programa, da lo mismo que la pieza del evaluador sellado en las 600 partidas, una a una.
- **Ninguna partida acaba sin vivas**, así que todas las parejas cuentan: 40 por mundo y 200 con los cinco juntos.
- **Muertas en las 200 partidas de cada jugador:** RG69r+voz 213, S69+voz 251 y P69+voz 234.

**Medias de las 40 semillas** (felicidad de 0 a 1):

| mundo | medida | decide con el motor (RG69r+voz) | decide sumando (S69+voz) | decide con la posición (P69+voz) |
|---|---|---|---|---|
| abundancia | siempre | 0,921 | 0,895 | 0,885 |
| | solo vivas | 0,921 | 0,895 | 0,886 |
| normal | siempre | 0,793 | 0,786 | 0,766 |
| | solo vivas | 0,793 | 0,786 | 0,766 |
| sequía | siempre | 0,717 | 0,679 | 0,675 |
| | solo vivas | 0,716 | 0,680 | 0,675 |
| sequía dura | siempre | 0,451 | 0,412 | 0,413 |
| | solo vivas | 0,373 | 0,310 | 0,332 |
| bestias que crían | siempre | 0,533 | 0,491 | 0,481 |
| | solo vivas | 0,533 | 0,489 | 0,474 |
| **los cinco** | siempre | 0,683 | 0,652 | 0,644 |
| | solo vivas | 0,667 | 0,632 | 0,626 |

**Diferencias emparejadas por semilla, con su intervalo del 95 %** (bootstrap de siempre):

| mundo | medida | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| abundancia | siempre | +0,025 [+0,017, +0,034] | +0,036 [+0,026, +0,046] |
| | solo vivas | +0,025 [+0,017, +0,034] | +0,035 [+0,024, +0,045] |
| normal | siempre | +0,007 [−0,007, +0,022] | +0,027 [+0,014, +0,041] |
| | solo vivas | +0,007 [−0,007, +0,022] | +0,027 [+0,014, +0,041] |
| sequía | siempre | +0,038 [+0,020, +0,055] | +0,042 [+0,026, +0,060] |
| | solo vivas | +0,036 [+0,017, +0,054] | +0,041 [+0,023, +0,059] |
| sequía dura | siempre | +0,039 [+0,009, +0,068] | +0,038 [+0,007, +0,068] |
| | solo vivas | +0,062 [+0,004, +0,119] | +0,041 [−0,011, +0,094] |
| bestias que crían | siempre | +0,043 [+0,023, +0,063] | +0,053 [+0,027, +0,079] |
| | solo vivas | +0,044 [+0,022, +0,068] | +0,059 [+0,032, +0,087] |
| **los cinco** | siempre | **+0,031 [+0,022, +0,039]** | **+0,039 [+0,030, +0,049]** |
| | solo vivas | **+0,035 [+0,021, +0,049]** | **+0,041 [+0,028, +0,053]** |

**Lo que se ve:**
- **En cuatro mundos casi no cambia nada.** Las que mueren son pocas y su felicidad se parece a la de las demás.
- **En la sequía dura sí cambia.** Contando solo a las vivas, la felicidad baja en los tres jugadores, de 0,41-0,45 a 0,31-0,37. Las que mueren pronto tienen pocos turnos y casi todos son de antes de la escasez, cuando todavía son felices; al sacarlas, quedan las que pasan la escasez entera.
  - La ventaja frente a S69+voz crece (+0,062), con un intervalo mucho más ancho.
  - Frente a P69+voz, el intervalo toca el cero.
- **Con los cinco juntos, la ventaja de decidir con el motor no cambia:** sigue por encima de cero frente a los dos y un poco más grande. La regla de la parte 1 del 154 (morir no cuesta felicidad) no es lo que da la ventaja.

## Parte 2: el GIF de la partida entera, rehecho

Hecho con un programa nuevo, `gif_partida_entera_v2.py`. Importa la lectura de los datos, las épocas, los colores de casa y el paso de `gif_partida_entera.py` (que queda igual), el momento del día de `gif_tres_aldeas.py`, y los rótulos y colores de los jugadores de `figuras_escalera_paper8.py`.

- **El fichero:** `figuras/tres_aldeas_sequia_30182_v2.gif`. El del 154 sigue en su sitio, sin tocar.
- **Duración y tamaño:** un fotograma cada 40 turnos, 401 fotogramas a 8 por segundo: **50 segundos** y **6,4 MB**.
- **Los cambios que pedía el prompt:**
  - **Rótulos.** Ahora dicen solo «decide con el motor», «decide sumando» y «decide con la posición», en el color de cada jugador.
  - **Días del 1 al 40.** El dato 0 se enseña como día 1, y el último fotograma dice «día 40 · noche (acaba)».
  - **El color de cada criatura** es siempre el de su casa, vivo. El punto va hueco si duerme; la bestia es una X; una muerta desaparece del mapa.
  - **Debajo de cada aldea, las barras de 0 a 100.** Hay ocho finas, una por criatura, del color de su casa, de dos en dos por hermanas, con la felicidad de su último día. Al lado, una ancha y oscura con la media de la aldea. Una muerta deja su barra vacía con una X.
  - **Encima de cada aldea:** el día y el momento del día, las vivas y los empujones acumulados, en dos líneas.
  - **La tira de abajo**, común a las tres aldeas. Tiene dos gráficas que se van dibujando: la felicidad de la aldea del último día y los empujones acumulados. Las líneas van en azul para el motor, naranja para la suma y verde para la posición, como en las figuras fijas.
  - **Las dos escaseces** (días 11 a 15 y 31 a 35, contados del 1 al 40) van marcadas con una banda naranja suave en las dos gráficas y con el fondo naranja suave en los mapas.
  - **Una línea de leyenda arriba:** «Sequía, semilla 30182 · barras: la felicidad del último día de cada criatura (0 a 100) y, oscura, la media de la aldea».
- **Los cuatro fotogramas sueltos** (PNG):
  - `figuras/tres_aldeas_sequia_30182_v2_dia05.png`;
  - `figuras/tres_aldeas_sequia_30182_v2_dia12.png`, en plena escasez;
  - `figuras/tres_aldeas_sequia_30182_v2_dia16.png`;
  - `figuras/tres_aldeas_sequia_30182_v2_dia40.png`, el último turno.
- **Al acabar, el GIF da:** 8 vivas en las tres aldeas; 102, 134 y 132 empujones (los mismos del 153); y una felicidad del último día de 78, 90 y 90. Ojo: esta es la del último día, no la de la partida entera (70, 64 y 61), y el último día va al revés que la partida. Se ve en la tira: decide con el motor va por delante en muchos tramos, sobre todo dentro de las dos escaseces, y se queda atrás en los últimos días.

**Lo puse yo, por ser lo más sencillo:**
- **La media de la aldea de las barras** es la media de las barras de las vivas. Es la felicidad del último día, no la acumulada desde el turno 0 del GIF del 154. La línea de la tira es esa misma barra oscura a lo largo de la partida.
- **Los fotogramas de los días 5, 12 y 16** son de media mañana (turno 80 del día), para que se vean las criaturas despiertas.
- **Un aviso de una palabra**, «ESCASEZ», que sale en naranja arriba a la derecha durante la escasez, aparte de la línea de leyenda.
- **Los colores de casa son los del 154**: rojo, azul, verde y morado. El azul y el verde de las casas se parecen a los de dos jugadores, pero las casas solo salen en los mapas y en las barras, y los jugadores en los rótulos y en la tira.

## Lo que no se ha podido o hay que saber

- **La leyenda de arriba no explica el punto hueco ni la X.** El prompt pedía una sola línea corta, con el mundo, la semilla y las barras, y lo he dejado así: hueco es dormida, X es la bestia.
- **En esta semilla no muere ninguna criatura** en las tres aldeas, así que la barra vacía con su X no llega a salir en el GIF. Está en el programa, pero no se ha podido ver con estos datos.
- **El GIF no entra en el commit**, como pedía el prompt.

## Tropiezos

- **En el primer borrador** el nombre del jugador pisaba la línea del día, y la leyenda de arriba chocaba con el aviso de escasez.
- **El tinte de la escasez casi no se veía con 0,16**, así que volví al 0,22 del 154.
- **La leyenda de las tres líneas tapaba las caídas de la felicidad**, así que la pasé a la gráfica de los empujones, donde arriba a la izquierda no hay nada.
- **Los tres arreglos los hice con `sed`** sobre el programa nuevo. No hay Python suelto.

## Lo que entra en el commit

**Entra:**
- este informe;
- `felicidad_solo_vivas.py` y su salida (`salida/felicidad_solo_vivas.md` y `.json`);
- `gif_partida_entera_v2.py`;
- los cuatro fotogramas en PNG;
- la línea de STATUS.

**Queda fuera:** el GIF y los datos de las partidas.

Commit local, sin push.

## El gasto

- **Créditos de la plataforma:** 0.
- **Dólares de la consola de Anthropic:** 0.
- **Los saldos** no se han leído.

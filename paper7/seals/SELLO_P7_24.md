# SELLO P7-24 · El campo de la primera etapa: nacer sin saber qué curan el botiquín ni la ración

*7-oct-2026. Escrito ANTES de pedir ninguna partida. Coste previsto: hasta 120 partidas en la plataforma; consola 0.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Cuerpo y congelados sin tocar. Archivos `_P7`; una vida por proceso; la memoria viaja solo en el cuaderno.*

## El diseño

- Tres brazos, como interruptores de la misma imagen (`Dockerfile.pareja_P7_24` = la del humo de P7-23 con el paso 0): **TECHO** (nace sabiendo, con pedir), **APRENDE** (nace sin
  saber, cuaderno que viaja de un día al siguiente), **BORRADO** (nace sin saber, cuaderno vaciado cada noche). Pedir corregido (P7-17) y lo dado entregado (P7-19) en los tres;
  ojos compartidos apagados. 20 días, dos series; la misma semilla para los tres brazos cada día.
- **Semillas nuevas**, declaradas antes de jugar (`semillas_P7_24.json`): la sucesión de siempre, 20260916 + k·104729, k = 155 a 174 (las siguientes a las del humo de P7-23,
  152-154); la serie 2 juega las mismas 20 en orden inverso. Serie 1: 36493911, 36598640, …, 38483762.
- Paso 0 hecho y declarado (commit `e52e306`): la curiosidad no va a destinos sin camino y, en empate entre las dos clases, va al objeto más cercano por camino.
- Las dos decisiones del vigilante de P7-23 (curiosidad hacia la clase que más llama; W_TARGET = 1 + k_botiquín + k_ración) quedan aprobadas por Manel (7-oct).

## Definiciones, fijadas antes de medir

- **Primer contacto** con un objeto: el primer tic en que una unidad de esa clase entra en el zurrón. **Recuerdo firme**: un uso completado sin la marca «al menos».
- **Creencia** de un objeto: la del cuaderno con el recuerdo neutro (`cuaderno_P7.creencia`), por situación (dentro/fuera); la de la ración, la mayor de sus situaciones;
  la del botiquín, la de dentro del círculo. **Ignorancia**: la del cuaderno (`ignorancia`, P7-6), al cerrar el día.
- **Instantes de vida desde el primer contacto** (E2): los tics vividos desde el tic del primer contacto hasta el tic del primer recuerdo firme, sumando los de los días
  intermedios enteros si hay más de un día entre los dos.
- **Puesto**: `final.placement` de cada vida (1 el mejor, 16 el peor). **Diferencia de puesto** APRENDE − TECHO (y BORRADO − TECHO): media de las diferencias emparejadas
  por serie, día y asiento; su error estándar, el de esas diferencias emparejadas (desviación típica / raíz de n). Días 1 a 5: n = 2 series × 5 días × 2 asientos = 20 parejas;
  días 16 a 20: 20 parejas.
- **Vida al usar el botiquín** (E6): la vida en el tic de apertura del canal (registro `P7_nace_uso`), mediana sobre todas las aperturas de los días 11 a 20 del brazo.
- **Tiempo en `ir_curioso`**: tics con `RADIOGRAFIA.elegido` = `ir_curioso`.

## Las reglas

| | regla | pasa si |
|---|---|---|
| E1 | descubre | APRENDE: al acabar el día 5, las 4 criaturas tienen ≥ 1 recuerdo firme del botiquín y ≥ 1 de la ración; al acabar el día 10, ignorancia < 0,3 en los dos objetos en ≥ 3 de las 4 |
| E2 | aprende a aprender | en ≥ 3 de las 4 criaturas de APRENDE, el segundo objeto que llega a su primer recuerdo firme tarda menos instantes de vida desde su primer contacto que el primero |
| E3 | qué aprende antes | en ≥ 3 de las 4, el día en que la creencia de la ración llega a 12 (80 % de 15) es anterior al día en que la del botiquín dentro llega a 40 (80 % de 50); no llegar cuenta como después |
| E4 | qué pierde y qué recupera | días 1-5: APRENDE − TECHO > 2 errores estándar (peor puesto); días 16-20: esa diferencia ≤ la mitad de la de los días 1-5 |
| E5 | sin memoria no recupera | BORRADO − TECHO en los días 16-20 ≥ la mitad de la de los días 1-5 |
| E6 | lo aprendido cambia la conducta | días 11-20: mediana de la vida al abrir el botiquín, APRENDE < BORRADO |

Sin predicción, solo medida: APRENDE frente a BORRADO en puesto.

## El freno (antes del resto): APRENDE, serie 1, días 1 a 3

Se sigue si (a) el cuaderno viaja y se lee (registro `P7_cuaderno` de arranque con `leido` verdadero los días 2 y 3 y recuerdos del día anterior dentro); (b) ninguna de las 6
criaturas pasa más de la mitad de su vida en `ir_curioso` sin tocar ningún objeto; (c) en al menos una criatura sube la creencia de alguno de los dos objetos (de «no sé» a un
valor, o de un valor a otro mayor, entre el cierre de un día y el siguiente). Si algo falla, se para y se dice. Del freno no se mira nada más; el sello se evalúa una vez, al final.

## Guardas

Disco: limpieza de Docker tras cada horneado; si baja de 5 GB, parada limpia y aviso. Red: esperar y reintentar, o parada limpia con la hora. Nada de resultados parciales.

## md5 de lo sellado

- `nace_P7_23.py`: `6e187039d3189f2af64840f050d2eaac`
- `recuerdo_P7_23.py`: `519e69e67026c880d49af76bc14eed30`
- `policy_pareja_P7_23.py`: `fad2c97ed13783cbe7b8d176a9f96735`
- `descubre_P7.py`: `1dac5ed0f51b06fcb6b6a5aa31c3e1c5`
- `pide_P7.py`: `4766e5a3b0afdc20b787d0b79da9fe31`
- `cuaderno_P7.py`: `f4c6a9dae0af4831cfa930da18b74376`
- `Dockerfile.pareja_P7_24`: `be589f05420a5a25072391f01f5c08e5`
- `lanza_P7_24.py`: `dd43c880d4c231e1c4de28e30dd17981`
- `semillas_P7_24.json`: `5949267f29e4f0ca8a1bd35b561aeb57`

Commit del sello: `6afb94261951` (gemv-coworld, paintball).

## Añadido posterior al freno (P7-27, 8-oct-2026; decisión de la mesa, declarado como cambio posterior a ver el freno)

La condición (b) estaba mal planteada: contaba como curiosidad los instantes en que el cuerpo no puede moverse (P7-25). Se sustituye por **(b')**: en al menos 4 de las 6 vidas
de los días 1 a 3 de APRENDE, serie 1, la criatura toca algún objeto desconocido (una unidad de botiquín o de ración entra en el zurrón). Sobre lo ya jugado: tocan 4 de 6
(día 1 asiento 11, día 2 asiento 10, día 3 asientos 10 y 11; no tocan día 1 asiento 10 y día 2 asiento 11). **(b') pasa.** (a) y (c) ya pasaban. El campo sigue desde el día 4
tal como está sellado: mismas semillas, brazos, guardas y medidas; E1 a E6 no cambian; nada del cuerpo ni de la curiosidad cambia (escala ×1, la calma como está, la cautela de
P7-26 apagada).

## Añadido posterior (P7-27, 8-oct-2026; decisión de la mesa, motivado por un fallo de la plataforma)

En 6 partidas completadas la plataforma no tenía el artefacto (el diario) de uno o de los dos asientos: la conexión del juego con la política se cortó a media partida y la
política murió sin subirlo (traza `websockets.exceptions.ConnectionClosedError` en el registro de salida); en 4 de ellas la plataforma tampoco guardó el registro de salida del asiento («the pod was deleted before log collection»), así que de ese asiento no queda nada. Lo decidido:
1. Los diarios perdidos se rescatan del registro de salida (stdout) de cada asiento, que la plataforma sí guarda, y quedan marcados como parciales con el tic del corte
   (`PARCIAL_agent_<asiento>.json` junto al diario; `parcial` en `P7_24_estado.json`). En APRENDE se toma el cuaderno de fin que la política escribió en el corte.
2. Las dos cadenas siguen con esos cuadernos (serie 1 desde el día 13, serie 2 desde el 19), sin repetir ninguna partida.
3. Medidas: en las partidas con un corte, el aprendizaje (creencias, ignorancia, recuerdos, primeros contactos y usos) cuenta hasta el corte; la partida entera, los dos
   asientos, sale de las comparaciones de puesto, vida al morir y causa de muerte (E4, E5 y la medida sin predicción); en las comparaciones emparejadas se quita el par de ese
   día y esa semilla en los brazos que se comparan. Se informa de cuántas vidas y partidas quedan fuera, y E4 y E5 se repiten también sin excluir nada, como comprobación.
4. Si vuelve a faltar un artefacto, se rescata del registro de salida, se marca y se sigue (`lanza_P7_24.rescata_del_registro`); si faltara también el cuaderno, parada y aviso.

| partida | asiento sin artefacto | tic del corte | líneas rescatadas | cuaderno de fin |
|---|---|---|---:|---|
| serie 1, día 3, BORRADO (semilla 36703369) | asiento 10 | ninguno: la plataforma tampoco guardó el registro de salida («the pod was deleted before log collection»); no se sabe cuánto jugó ese asiento | 0 | no |
| serie 2, día 7, TECHO (semilla 37855388) | asiento 10 | ninguno: la plataforma tampoco guardó el registro de salida («the pod was deleted before log collection»); no se sabe cuánto jugó ese asiento | 0 | no |
| serie 1, día 10, BORRADO (semilla 37436472) | asiento 10 | ninguno: la plataforma tampoco guardó el registro de salida («the pod was deleted before log collection»); no se sabe cuánto jugó ese asiento | 0 | no |
| serie 1, día 18, TECHO (semilla 38274304) | asiento 10 | ninguno: la plataforma tampoco guardó el registro de salida («the pod was deleted before log collection»); no se sabe cuánto jugó ese asiento | 0 | no |
| serie 1, día 12, APRENDE (semilla 37645930) | asiento 11 | 7625 | 3646 | sí |
| serie 2, día 18, APRENDE (semilla 36703369) | asiento 10 | 8416 | 294 | sí |
| serie 2, día 18, APRENDE (semilla 36703369) | asiento 11 | 10827 | 5434 | sí |

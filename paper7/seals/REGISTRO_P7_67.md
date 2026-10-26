# REGISTRO P7-67 · El control de la amenaza: la prueba de P7-66 con menos rivales

## (17-oct.-2026) Decisiones de la mesa y banco de plataforma, escritos ANTES de lanzar nada

### Decisiones de la mesa
1. **Cómo se quitan rivales**: los asientos sobrantes los ocupa una política nuestra **pasiva** (`pasiva_P7_67.py`: se conecta, no reparte puntos —el juego pone los de
   por defecto— y a cada observación responde «nada»: no se mueve, no coge, no ataca). El juego no se toca; la versión compilada del juego es el plan B.
2. **Para la calma y la interrupción solo cuentan los rivales ACTIVOS.** La pieza (`invita_P7_67`) los distingue por asiento (los asientos activos van en la imagen,
   `GEMV_P7_67_ACTIVOS`). Las pasivas las ignora la regla, pero se miden (punto e).
3. **Los rivales activos son rivales de liga del roster de P7-65** (`roster_lento_v2_PROPUESTA.json`, 14 sillas), elegidos con una semilla fija:
   `random.Random(6767)`: primero `choice` sobre las 14 sillas (cada política tantas veces como sillas tenía), después `choice` sobre los asientos 0-9 y 12-15.
   Resultado: **aaron-zs-fable v2** (`9457da2a-832d-45e5-b918-9209e86f9948`) en el **asiento 4** (sale del pedestal (24, 40), al sur).
4. **Se juega en la plataforma.**
5. **El resto del mundo, como en P7-66**: las mismas piezas (`invita_P7_66b` sin cambios en su lógica: misma invitación y mismo destino para las dos hermanas, los primeros
   300 tics de la fase viva, destino a 8-15 casillas de las dos, interrupción a ≤ 3, una sola llegada por criatura, destino y día; calma para aceptar = ningún rival
   ACTIVO a ≤ 5 y ningún golpe en 48 tics), hermanas COMPARTE con fusión, miedo 0,5 / 1,5, y la configuración de partida del roster lento (`roster_lento_v1.json`).

### Banco (paso 2)
- **Roster**: las dos hermanas en los asientos 10 y 11; el rival activo en el asiento 4; 13 pasivas en los asientos 0-3, 5-9 y 12-15.
- **Brazos**: MIENTE (la invitación apunta a una casilla del borde donde nunca se vio un botiquín en P7-65, `P7_66b_casillas.json`; `falsa=True`) y HONESTA (a una de
  las 5 casillas del centro con más botiquines; `falsa=False`). El destino de cada día se elige como en el segundo banco de P7-66 (`random.Random(1000·día + 10)` entre las
  casillas a 8-15 de las dos salidas (13, 13) y (18, 9) que no son su pedestal).
- **La invitación la escribe el guión** (no se llama a la razón: 0 $ de consola).
- **4 días por brazo** = 8 partidas. Cada brazo es una cadena: el cuaderno de fin de cada hermana es el que lee al día siguiente (la confianza viaja).
  Semillas del día 1 al 4: las de la serie 1 de P7-65 (`semillas_P7_41.json`: 43406025, 43510754, 43615483, 43720212), las mismas en los dos brazos.
- **Reintento**: si la plataforma borra el contenedor de una partida, un solo reintento con la misma imagen y la misma semilla (como en P7-65).

### Medidas (informe)
- a) fracción de las aceptadas en calma que llegan, por brazo y hermana (y por pareja);
- b) intentos interrumpidos (por un rival activo a ≤ 3);
- c) evaluaciones de la mentira por serie (llegadas en MIENTE; «serie» = los 4 días de un brazo, como en P7-66);
- d) fracción del día en calma (regla de la pieza: sin rival ACTIVO a ≤ 5, sin golpe en 48 tics) y largo de los tramos de calma, frente a P7-65 (allí con todos los
  rivales activos, con la misma cuenta);
- e) cómo trata el cuerpo a las pasivas: tiempo a ≤ 2 casillas de una pasiva, alejarse (paso que aumenta la distancia a la pasiva más cercana estando a ≤ 3), ataques
  a pasivas (elige `atacar_*` con una pasiva en esa dirección y al alcance), muertes de pasivas (`final.reason == "eliminated"` del asiento) y coger lo que sueltan
  (elige `coger` en una casilla a ≤ 1 de donde murió una pasiva, después de su muerte);
- f) 2 GIF de los datos crudos (matplotlib), uno por brazo.

### Listones
- **Listón de P7-66, sin cambios**: en MIENTE, al menos la mitad de las aceptadas llegan **y** al menos 30 evaluaciones de la mentira por serie.
- **Listón nuevo (la ruta de las pasivas)**: si las criaturas pasan **más de una cuarta parte del día** atacando o persiguiendo a pasivas, la ruta de las pasivas no vale
  → plan B (el juego compilado). Definición operativa, fijada antes de ver datos: fracción de los tics de la fase viva en que la criatura (i) elige `atacar_*` contra una
  pasiva, o (ii) está a ≤ 3 casillas de una pasiva visible y su paso la acerca a ella (Chebyshev). Se da por criatura y su media; falla si la media pasa del 25 %.
  (ii) cuenta de más a propósito: también entra quien solo pasa al lado.

### Para la mesa (no decidido; el listón no se cambia aquí)
- La cuenta de «evaluaciones por serie» de P7-66 (`banco_P7_66b.py`) es: llegadas por vida-día × 2 hermanas × 13 días (los días 8-20 de una serie de 20, los que llevan la
  mentira). Con **una invitación al día** y **una sola llegada por criatura, destino y día**, el máximo es 1 × 2 × 13 = **26 < 30**: la segunda mitad del listón no se puede
  alcanzar por construcción, ni aunque llegue el 100 %. Ya era así en el segundo banco de P7-66 (que dio 0 y no llegó a importar). El informe dará la cifra con la misma
  cuenta y dirá que el tope es 26; qué hacer (varios destinos al día, contar más días, o bajar a 26) es de la mesa.

motor/model.py md5 `1e511978c251130e95169ebf8443efa1`, comprobado al escribir este registro.

## (17-oct.-2026) Corrección de Manel al banco, antes de lanzar

1. **El destino de la mentira tiene que estar a más de 6 casillas (Chebyshev, la misma distancia que el resto de la pieza) de cualquier pedestal ocupado por una pasiva**
   (asientos 0-3, 5-9 y 12-15), además de las condiciones de P7-66 (borde a ≥ 15 del centro, transitable, sin botiquines vistos en P7-65, a 8-15 de las dos salidas,
   que no sea su pedestal). Casillas que lo cumplen: **76** de las 154 que cumplían P7-66 (`P7_67_destinos.json`). El destino del día se elige igual que antes
   (`random.Random(1000·día + 10).choice` sobre esa lista ordenada): día 1 (5, 10), día 2 (4, 7), día 3 (24, 1), día 4 (4, 6); la pasiva más cercana queda a 8, 11, 7 y 12.
   La honesta no cambia (las 3 casillas del centro que cumplen la distancia a las salidas ya están a ≥ 10 de cualquier pedestal): días 1-4 (27, 23), (21, 24), (27, 23), (27, 23).
2. **Duración de los ratos de calma con un solo rival activo** (ya en el punto d), y si dan tiempo de sobra para llegar a un destino a 8-15 casillas. Criterio fijado
   antes de ver datos: andar 15 casillas lleva ~165 tics (un paso cada ~11 tics, medido en P7-65); se da la mediana y los cuartiles del largo de los tramos de calma,
   la fracción de tramos ≥ 165 tics, y lo mismo solo para los tramos que empiezan en los primeros 300 tics de la fase viva (los únicos en que la invitación empuja).
   «Tiempo de sobra» = la mediana de esos tramos es de al menos 2 × 165 = 330 tics; «justo» = entre 165 y 330; «no da» = por debajo de 165. Se compara con P7-65.

## (17-oct.-2026) Humo local de la pasiva (0 créditos), antes de lanzar

Partida local (variante competition del Mac): hermanas P7-67 en 10 y 11 y la pasiva en los otros 14 (también en el 4: en local no hay imagen del rival de liga).
- Las pasivas se conectan y no hacen nada: daño hecho 0 y bajas 0 en los 16 asientos. Las hermanas arrancan con `invita_P7_67` (activos [4]) y aceptan la invitación en el tic 241.
- Las 14 pasivas acaban `eliminated` entre los tics 3.768 y 3.816 sin que nadie les haga daño. Lo más probable: la zona alcanza su pedestal (en local el radio baja de 15 a 11 entre
  los tics 3.264 y 3.888, y los pedestales están a ~16 del centro); no está comprobado. Con la zona del roster lento de la plataforma eso pasaría hacia el tic ~10.000. Las que reciben el regalo del
  patrocinador viven 48 tics más. **Consecuencia para el banco**: la pasiva no vive todo el día; el tramo que se mide (los primeros 300 tics de la fase viva) no cambia, pero el
  punto e) solo tiene sentido mientras viven y el informe lo dará con esa ventana. Si al final solo quedan las hermanas, la partida acaba antes.
- Arreglo: la pasiva salía con error al acabar (el juego cierra sin trama de cierre); ahora lo apunta y sale limpia. En local hay que pasar una sola orden `--run` para todas las
  imágenes (elige la pasiva o la pareja por el archivo que lleva); en la plataforma cada imagen usa su CMD, como en P7-65.

## (17-oct.-2026, 10:40) Resultado del banco de plataforma (8 partidas, 0 reintentos)

- Listón de P7-66: MIENTE 0 de 8 aceptadas llegan, 0 evaluaciones por serie → no se alcanza. Listón nuevo de las pasivas: 0,01 % del día → la ruta de las pasivas vale (no hay plan B).
- Ratos de calma con un rival: los del tramo de salida, mediana 11.039 tics → «de sobra» (P7-65: 11, «no da»).
- **Hallazgo**: `invita_P7_66b` (usada sin cambios, decisión 5) mira la distancia 8-15 a ella y a su hermana **en cada tic**, no solo al aceptar: a 7 casillas el candidato `ir_sitio`
  desaparece y vuelve a 8 (columpio). Mientras empuja, llegar es imposible. Esto pone en duda la lectura del cierre de P7-66 (no se reescribe aquí; queda anotado). Propuestas a la mesa
  en `informe_P7_67.md`; no se lanza nada más sin su decisión.

## (17-oct.-2026, 10:31) Decisiones de la mesa sobre el banco, escritas ANTES de construir

1. **Pieza nueva `invita_P7_67b`** (`invita_P7_66b` e `invita_P7_67` no se tocan): la distancia de 8-15 casillas al destino (de ella y de su hermana) se comprueba **solo al aceptar**.
   Desde ahí, `ir_sitio` sigue ofrecido hasta el juicio: llegada, interrupción (un rival ACTIVO a ≤ 3) o fin de la ventana (480 tics). Todo lo demás, como en `invita_P7_66b`.
   Lectura que hago, declarada: con la invitación ya aceptada y abierta tampoco se miran el tramo de 300 tics ni la calma para seguir ofreciéndola («sigue ofrecido hasta el juicio»);
   antes de aceptar, todo igual que en `invita_P7_66b` (calma, tramo de 300 tics, 8-15 de las dos, una llegada por destino y día). Las interrupciones siguen contando solo con rivales activos.
2. **Juicio de la llegada, en los dos brazos**: llegar sigue siendo estar a ≤ 1 del destino; **acierto si hay un botiquín visible a ≤ 3 casillas del destino al llegar**, fallo si no.
   Los destinos de la mentira siguen siendo los de `P7_67_destinos.json` (nunca se vio un botiquín en P7-65 y a > 6 de cualquier estatua); la honesta, las mismas casillas del centro.
3. **Listón de viabilidad, corregido antes de ver el nuevo banco**: en MIENTE llega **al menos la mitad de las aceptadas**. El listón de 30 evaluaciones por serie **se sustituye**: con una
   invitación al día y una sola llegada por criatura, destino y día, el tope es 1 × 2 hermanas × 13 días = 26 < 30, así que el diseño lo hacía imposible aunque llegase el 100 %. En su lugar,
   **el campo tendrá las series necesarias para sumar al menos 120 evaluaciones de la mentira** (cuántas series, se calcula con la tasa de llegada de este banco).
4. **Banco**: el mismo de antes con la pieza nueva: 1 rival activo (aaron-zs-fable v2, asiento 4), 13 estatuas (pasivas), hermanas en 10 y 11, MIENTE y HONESTA, 4 días por brazo
   (8 partidas), mismas semillas y destinos, cadena de cuadernos nueva desde el día 1. Mismas medidas a)-f).
5. **Aparte, sin jugar**: revisar los 11 intentos del segundo banco de P7-66 y contar en cuántos influyó la regla de distancia mirada en cada tic; corregir la conclusión de P7-66 en
   WHERE_IS_SEVEN.md según lo que salga, diciendo que la lectura anterior estaba contaminada por ese fallo.

## (17-oct.-2026, 11:10) Pieza `invita_P7_67b` construida (18 pruebas pasan) y humo local, antes de lanzar el banco

- Humo local (0 créditos; solo hermanas y pasivas, sin rival): las dos aceptan en el tic 241 y no llegan (MIENTE, destino (5, 10)). La pieza hace lo decidido: `ir_sitio` está entre
  los candidatos en 479 de los 480 tics de la ventana, también a menos de 8 casillas. Lo que frena ahora es el cuerpo: el paso que se ejecuta es el del tic en que el movimiento está
  listo, y en esos tics la prudente gira en un triángulo de tres casillas: en una elige `ir_sitio` (noroeste, hacia el destino) y en las otras dos `ir_objeto` (este y sur, hacia objetos
  que ve). Corrección de una cifra del primer banco: los «tics eligiendo `ir_sitio`» del informe cuentan sobre todo tics de espera, en los que no se mueve; lo que mueve es el tic listo.
  El banco de plataforma mide ahora también la elección en los tics listos.

## (17-oct.-2026, 10:39) Corrección de hora

La entrada anterior («11:10, pieza `invita_P7_67b` construida y humo local») se escribió hacia las 10:35, no a las 11:10; la hora se puso mal. El banco nuevo se lanzó a las 10:37.

## (17-oct.-2026, 11:55) Resultado del banco con `invita_P7_67b` (8 partidas, 0 reintentos)

- Listón de viabilidad (corregido a las 10:31): en MIENTE llegan 4 de 8 aceptadas = 50 % → **pasa, justo en el borde** (Wilson 95 %: 21,5-78,5 %). HONESTA: 8 de 8 (7 aciertos a ≤ 3).
- Llegadas de la mentira por días: días 1 y 4, las dos hermanas; días 2 y 3, ninguna (gana `ir_objeto` o se reparte la elección; `ir_sitio` ofrecido toda la ventana).
- Para 120 evaluaciones de la mentira, con esta tasa (13 por serie con la cuenta de P7-66) hacen falta 10 series; con el borde bajo del intervalo, 22. Cuenta para la mesa, no decisión.
- Estatuas: 1,61 % del día de media (máximo 23,5 % en una criatura que vivió 1.442 tics), 0 ataques: la ruta vale.
- Revisión de P7-66b (sin jugar): la regla de distancia mirada en cada tic influyó en 6 de 11 intentos; WHERE_IS_SEVEN.md corregido. Informe `informe_P7_67_segundo_banco.md`.

## (17-oct.-2026, 14:25) Humo del campo (punto 5): pasa

9 partidas (día 1 de la serie 1 de cada brazo y nivel), 2 cadenas en paralelo, 0 reintentos, de 13:01 a 14:18. `verifica_humo_P7_67F.py` → `P7_67F_humo.json`: los 18 asientos pasan.
- Guarda de latencia: pasa en todos (p95 de 6,4 a 14,1 ms); ninguna partida marcada.
- Diario y cuaderno de fin en todos los asientos.
- Activos por nivel, los del diseño.
- Juicio: aciertos recalculados a ≤ 3 iguales a los apuntados.
- CONGELADA: arranca con la pieza y cierra en 0,5. Ese día no hubo llegada, así que en el campo no se vio todavía a la pieza devolver la confianza a 0,5; eso solo está probado en las pruebas.
- `analiza_P7_67.py` corre sobre esos datos. Con un día y una serie, P1 y P2 salen NO CALCULABLE; las cifras de P3 no son un resultado y no se leen.

Las 9 partidas cuentan como campo. El campo (7 cadenas) espera el visto bueno de Manel.

## (17-oct-2026, 15:34) Visto bueno de Manel al campo, con ajustes (enmienda 1 del sello), antes de lanzar

Se confirman las interpretaciones 1, 2, 3 y 5. Cambios:
- P3 pasa a llevar el brazo como indicadora.
- Nueva predicción P3b: llegadas medias por día en los días 1-5, con 0 los días sin oportunidad.
- Nuevo descriptivo: fracción de días con oportunidad por nivel.
- Disco aprobado: borrar solo el `.art.log` tras copiar al T7 y releer por md5; queda el `.zip`.
- Vigilancia de CONGELADA en su primera llegada; si la confianza no vuelve a 0,5, para el campo entero.
- Campo con 7 cadenas en paralelo; si algo falla, para y queda escrito; al cerrar, solo el estado y las incidencias.

Guion de análisis nuevo: md5 `7bef2e46106bb860c366b0bdb1dba037`. Detalle en `SELLO_P7_67.md`, enmienda 1.

## (17-oct-2026, 21:50) Campo PARADO por la guarda de latencia (regla dura); nada arreglado

- El campo empezó a las 15:35 con 7 cadenas. A las 21:42 la orquesta paró sola: en `n1_s1_d19_CONGELADA`, asiento 11, hubo un 21,1 % de pasos «bloqueados sin cuerpo» (387 de 1.838 pasos listos), por encima del 5 %. 353 de ellos son el mismo paso, de (29, 21) hacia el oeste, a (28, 21). La guarda no lo reconoce como una rareza del mundo conocida. Latencia de esa vida: mediana 5,5 ms, p95 16,8 ms, 0,01 % sobre el tic. Es la única vida marcada del campo.
- Estado al parar: 120 partidas pedidas; 116 completadas (las 9 del humo incluidas) y 4 en vuelo en la plataforma, sin recoger (n1 s1 d19 HONESTA y MIENTE, n1 s2 d10 HONESTA, n2 s2 d1 MIENTE). 0 reintentos, 0 días perdidos, 0 paradas por red, plataforma o disco. 13 cadenas tocadas.
- Vigilancia de CONGELADA (15:56, n1 s1 d2, asiento 10): la confianza vuelve a 0,5 en las tres dimensiones. Pasa.
- Disco: 20 GB libres; el archivo al T7 aún no se ha disparado (umbral 15 GB). `motor/model.py` intacto.
- No se ha mirado ningún resultado del sello. Siguiendo la enmienda 1 (punto 6), no se arregla nada: espera a Manel.

## (17-oct-2026, 22:25) Diagnóstico de la parada (sin mirar resultados del sello; el campo sigue parado)

1. **Las 4 partidas en vuelo, recogidas y guardadas** (22:00-22:01), sin analizarlas: 8 vidas con cuaderno de fin, ninguna marcada. Estado: 120 partidas completadas.
2. **La casilla (28, 21) en esa semilla es un muro de fortaleza (`F`)** del mapa fijo (`static_map`). El mapa del cuerpo la tiene por sólida: `mundo.solido` cuenta `#`, `F` y `R`, y el campo
   geodésico la excluye. El paso que se emitió fue en línea recta contra el muro. En `decisor_zs._a_json` eso solo ocurre cuando el campo geodésico hacia el destino sale vacío, es decir,
   cuando el destino es una casilla sólida. **Hipótesis sin comprobar:** el diario no guarda el destino de `ir_pareja`; la posición recordada de la hermana podría haber caído sobre el muro.
3. **Lo que hacía el cuerpo en los 353 choques: `ir_pareja`, ir hacia su hermana**, en todos (tics 11.912-12.264). La hermana estaba quieta dentro de la fortaleza, en (27, 21) según su
   propio diario, y la criatura fuera, en (29, 21), con el muro (28, 21) entre las dos; la criatura no la veía. Con `ir_sitio`, nada: ningún intento abierto ni ofrecido en esos tics; ese día
   no hubo ni una aceptación. GIF de los datos crudos: `P7_67F_bloqueo.gif` (`gif_bloqueo_P7_67F.py`, tics 11.880-12.300).
4. **Las 120 partidas completadas (240 vidas), todo junto** (`diagnostico_bloqueos_P7_67F.py` → `P7_67F_bloqueos.json`): 2.270 pasos bloqueados sin cuerpo de 667.110 pasos listos.
   - Vidas por encima del 1 %: **15**; del 2 %: **13**; del 5 %: **1** (la de la parada).
   - Bloqueados con `ir_sitio` elegido: 4 (0,18 % de todos); con un intento de `ir_sitio` abierto: 23 (1,0 %). Ninguna vida tiene más de 3 bloqueos con `ir_sitio` activo.
   - Las otras 14 vidas por encima del 1 % (entre el 1,1 % y el 4,5 %) chocan todas contra la casilla (27, 21), suelo dentro de la misma fortaleza. Son pasos sueltos (`move_N` o
     `move_E`), sin `ir_sitio` (0 bloqueos con él) y sin la hermana ni ningún agente visible en esa casilla. Qué la ocupa no lo he averiguado.

**Lectura con el criterio de Manel:** los choques **no están ligados a `ir_sitio`**, y **no hay más vidas con bloqueos altos mientras `ir_sitio` estaba activo**. Sobre el 5 %, el caso es
**aislado** (1 de 240). Pero el mismo sitio, la fortaleza junto a (27-28, 21), produce bloqueos del 1-4,5 % en otras 14 vidas, por debajo del umbral. Como el criterio pide «caso aislado»
y el mismo sitio se repite por debajo del umbral, no reanudo y lo dejo a Manel.

## (17-oct-2026, 22:07) Decisión de la mesa sobre la parada, escrita antes de reanudar

1. La partida `n1_s1_d19_CONGELADA` se trata como **marcada**: sale entera en la robustez.
2. **Rareza conocida del mundo, como en P7-30.** Los pasos bloqueados sin cuerpo en las casillas (27, 21) y (28, 21) de esa fortaleza no paran el campo. Si una vida pasa del 5 % de pasos
   bloqueados y la mayoría (más de la mitad de sus bloqueados sin cuerpo) son contra esas dos casillas, la vida queda marcada, su partida sale en la robustez y el campo sigue.
   **Motivo:** los choques son `ir_pareja` contra el muro de la fortaleza con la hermana dentro; no están ligados a `ir_sitio` (4 de 2.270 bloqueos con `ir_sitio` elegido).
3. **Todo lo demás de la guarda sigue igual:** la latencia sigue siendo dura (más del 10 % de decisiones sobre el tic para el campo), y los bloqueos por encima del 5 % en cualquier
   otra casilla siguen parando el campo.
4. Se reanuda el campo con 7 cadenas en paralelo. Al cerrar no se miran los resultados del sello: solo el estado, las incidencias y la lista de vidas marcadas con el motivo de cada una.
   Puesto en `lanza_P7_67F.py` (md5 nuevo `baa57503b8d702c6ef41e3351dbdf196`) con la función `rareza_fortaleza`. Probada así:
   - la vida de la parada (`n1_s1_d19_CONGELADA`, asiento 11) es rareza;
   - un diario sintético contra (28, 21) es rareza; contra (30, 21) no lo es;
   - si la latencia salta la regla dura, no hay rareza que valga.

   La vida de la parada queda en el estado, en `rarezas_fortaleza`. Las demás reglas de la guarda no cambian.

## (18-oct-2026, 03:25) Segunda parada del campo por la guarda (regla dura); nada arreglado

- El campo se reanudó el 17-oct a las 22:09. Paró el 18-oct a las 03:17: `n1_s3_d7_CONGELADA`, asiento 10, con un 5,9 % de pasos bloqueados sin cuerpo (> 5 %). Latencia de esa vida:
  p95 10,8 ms. Sus bloqueos van contra (27, 22) (74) y (27, 21) (16), dentro de la misma fortaleza. La casilla (27, 22) no está en la rareza que fijó la mesa (solo (27, 21) y (28, 21)),
  así que la regla para el campo.
- Lectura solo de su diario, sin resultados del sello: el cuerpo había elegido `ir_curioso` (75) y `move_N` (15); 0 bloqueos con un intento de `ir_sitio` abierto; la hermana no estaba
  en esas casillas. Tics 2.297-11.360.
- Estado: 214 partidas pedidas: 210 completadas y 4 en vuelo sin recoger (n2 s3 d4 MIENTE, n1 s3 d6 MIENTE, n3 s3 d1 MIENTE, n14 s3 d1 HONESTA). 0 reintentos, 0 días perdidos,
  0 paradas por red, plataforma o disco. 19 cadenas completas.
- Disco: el archivo al T7 se disparó una vez (18-oct, 02:25): 3.464 archivos copiados y releídos iguales, 14,3 GB; 366 `.art.log` borrados (13,7 GB). 25 GB libres. `motor/model.py` intacto.
- Vidas marcadas hasta ahora: 2 (la de la primera parada, n1 s1 d19 CONGELADA asiento 11, ya tratada como rareza de la fortaleza, y esta).


## (18-oct-2026, 08:05) Decisión de la mesa sobre la segunda parada, escrita antes de reanudar

1. La partida `n1_s3_d7_CONGELADA` se trata como **marcada**: sale entera en la robustez.
2. **La excepción de la fortaleza pasa a ser por zona, no por casillas.** La zona son todas las casillas del muro de fortaleza (`F`) del mapa fijo, más todas las casillas de suelo dentro de
   ella o a 1 casilla o menos (Chebyshev) de sus muros. Si una vida pasa del 5 % de pasos bloqueados sin cuerpo y la mayoría (más de la mitad) son contra casillas de la zona, la vida queda
   marcada, su partida sale en la robustez y el campo sigue.
   **Zona exacta** (`P7_67F_zona_fortaleza.json`, calculada del `static_map` de las 210 partidas completadas): es el cuadrado **x 19-29, y 19-29**, con **121 casillas**. En el mapa hay
   una sola fortaleza y sus 24 casillas `F` son las mismas en todas esas semillas. Ninguna de las 97 casillas de suelo de la zona es roca ni pared en ninguna de ellas.
   - Muro `F` (24): (20, 20), (20, 21), (20, 22), (20, 25), (20, 26), (20, 27), (20, 28), (21, 20), (21, 28), (22, 20), (22, 28), (25, 20), (25, 28), (26, 20), (26, 28), (27, 20), (27, 28), (28, 20), (28, 21), (28, 22), (28, 25), (28, 26), (28, 27), (28, 28).
   - Suelo (97): (19, 19), (19, 20), (19, 21), (19, 22), (19, 23), (19, 24), (19, 25), (19, 26), (19, 27), (19, 28), (19, 29), (20, 19), (20, 23), (20, 24), (20, 29), (21, 19), (21, 21), (21, 22), (21, 23), (21, 24), (21, 25), (21, 26), (21, 27), (21, 29), (22, 19), (22, 21), (22, 22), (22, 23), (22, 24), (22, 25), (22, 26), (22, 27), (22, 29), (23, 19), (23, 20), (23, 21), (23, 22), (23, 23), (23, 24), (23, 25), (23, 26), (23, 27), (23, 28), (23, 29), (24, 19), (24, 20), (24, 21), (24, 22), (24, 23), (24, 24), (24, 25), (24, 26), (24, 27), (24, 28), (24, 29), (25, 19), (25, 21), (25, 22), (25, 23), (25, 24), (25, 25), (25, 26), (25, 27), (25, 29), (26, 19), (26, 21), (26, 22), (26, 23), (26, 24), (26, 25), (26, 26), (26, 27), (26, 29), (27, 19), (27, 21), (27, 22), (27, 23), (27, 24), (27, 25), (27, 26), (27, 27), (27, 29), (28, 19), (28, 23), (28, 24), (28, 29), (29, 19), (29, 20), (29, 21), (29, 22), (29, 23), (29, 24), (29, 25), (29, 26), (29, 27), (29, 28), (29, 29).
3. **El resto de la guarda no cambia:** latencia dura, y los bloqueos por encima del 5 % fuera de la zona siguen parando el campo.
4. Primero se recogen las 4 partidas en vuelo; después se reanuda con 7 cadenas en paralelo.
5. Al cerrar no se miran los resultados del sello: solo el estado, las incidencias y la lista de vidas marcadas con su motivo.
   Puesto en `lanza_P7_67F.py` (md5 nuevo `75af5dbc899649b6ddb4215d1b954206`): la rareza lee la zona de `P7_67F_zona_fortaleza.json`. Probada así:
   - la vida de la segunda parada (`n1_s3_d7_CONGELADA`, asiento 10) es rareza de la zona;
   - un diario sintético contra (29, 29), dentro de la zona, es rareza; contra (30, 30), fuera, no;
   - dentro de la zona pero con la regla dura de latencia saltada, no hay rareza que valga.

   La vida queda en el estado, en `rarezas_fortaleza`.

## (18-oct-2026, 13:35) Tercera parada del campo: la plataforma perdió el diario de una hermana; nada arreglado

- El campo se reanudó a las 08:08. Paró a las 13:25 por fallo de recogida, no por la guarda. En `n1_s4_d9_HONESTA` la plataforma da la partida por completada (sin error; con
  puntuaciones), pero no tiene el artefacto del asiento 10. Su registro de salida dice: «No logs collected for pod job-50767fa4-game-player-10 container player: the pod was deleted
  before log collection». El rescate dio 0 líneas, sin cuaderno de fin, así que la cadena `n1_HONESTA_s4` no puede hornear el día 10. El lanzador para por diseño
  («sin cuaderno de fin»). Es el mismo tipo de incidente que en P7-65 (pods borrados por la plataforma), donde se resolvió con un único reintento con la misma imagen y semilla.
  El diario del asiento 11 de esa partida no se llegó a bajar.
- Estado: 310 partidas pedidas: 305 completadas, esta incluida, y 5 en vuelo sin recoger (n1 s4 d9 MIENTE, n2 s4 d2 MIENTE, n1 s4 d11 CONGELADA, n3 s4 d2 HONESTA, n14 s4 d1 HONESTA).
  0 reintentos, 0 días perdidos. 15 GB libres: el archivo al T7 no se ha vuelto a disparar porque el campo paró justo en el umbral. `motor/model.py` intacto.
- Vidas marcadas: n1 s1 d19 CONGELADA asiento 11 y n1 s3 d7 CONGELADA asiento 10 (las dos, rareza de la zona de la fortaleza), y n1 s4 d9 HONESTA asiento 10 (sin diario: no se
  pudo medir).

## (18-oct-2026, 13:43) Decisión de la mesa sobre la tercera parada, escrita antes de reanudar

1. **Reintento de `n1_s4_d9_HONESTA`, una sola vez**, con la misma imagen y la misma semilla. La primera partida se aparta: no cuenta como marcada y consta como apartada por fallo de la
   plataforma. La cadena sigue con el resultado del reintento.
2. **Regla fija para el resto del campo:** si la plataforma da una partida por completada pero falta algún diario porque borró el contenedor antes de recogerlo, el lanzador la reintenta
   automáticamente UNA vez, con la misma imagen y semilla, sin parar el campo, y lo apunta en este registro. Si el reintento también falla, el campo para y se avisa a Manel.
3. **Al reanudar:** primero se recogen las 5 partidas en vuelo, después salta el archivo al T7 y el campo sigue con 7 cadenas en paralelo.
4. **Al cerrar, como siempre:** estado, incidencias, vidas marcadas y partidas apartadas, sin mirar resultados del sello.
   Puesto en `lanza_P7_67F.py` (md5 nuevo `b632b91869a4af0ee18959589e843b00`) con `aparta_y_reintenta`. La partida pasa a `apartadas_plataforma`, sus archivos se renombran
   `_apartada1` y la cadena vuelve a los cuadernos del día anterior (en el día 1, a ninguno). Se pide el reintento y queda una línea en este registro. Si la misma partida vuelve a
   perder un diario, el campo para (salida 12). Pruebas: `prueba_aparta_P7_67F.py`, 7 pasan.

- (2026-10-18T13:47:25) Partida `n1_s4_d9_HONESTA` APARTADA por fallo de la plataforma (n1_s4_d9_HONESTA asiento 10: la plataforma borro el contenedor antes de recoger el diario (decision de la mesa, 18-oct 13:43)); se reintenta una vez con la misma imagen y semilla (regla de la mesa del 18-oct, 13:43).

- (2026-10-19T14:18:15) Partida `n1_s10_d7_MIENTE` APARTADA por fallo de la plataforma (n1_s10_d7_MIENTE asiento 10: la plataforma borro el contenedor antes de recoger el diario); se reintenta una vez con la misma imagen y semilla (regla de la mesa del 18-oct, 13:43).

- (2026-10-19T19:28:22) Partida `n1_s10_d20_MIENTE` APARTADA por fallo de la plataforma (n1_s10_d20_MIENTE asiento 11: la plataforma borro el contenedor antes de recoger el diario); se reintenta una vez con la misma imagen y semilla (regla de la mesa del 18-oct, 13:43).

- (2026-10-19T20:15:47) Partida `n1_s11_d18_HONESTA` APARTADA por fallo de la plataforma (n1_s11_d18_HONESTA asiento 10: la plataforma borro el contenedor antes de recoger el diario); se reintenta una vez con la misma imagen y semilla (regla de la mesa del 18-oct, 13:43).

- (2026-10-20T05:28:37) Partida `n1_s15_d2_MIENTE` APARTADA por fallo de la plataforma (n1_s15_d2_MIENTE asiento 11: la plataforma borro el contenedor antes de recoger el diario); se reintenta una vez con la misma imagen y semilla (regla de la mesa del 18-oct, 13:43).

## (20-oct-2026, 07:50) Caída de Docker Desktop durante el campo; revisión antes de seguir

- **Qué pasó.** Docker Desktop cayó («session healthcheck failed fatally: Unavailable: connection error: only one connection allowed»). Manel lo cerró con Quit y lo volvió a abrir, sin
  reset. En el registro del lanzador: un fallo aislado de horneado hacia las 07:13 (un intento; el campo siguió) y la caída de verdad tras pedir `n1_s14_d14_MIENTE` (07:19). Desde
  entonces el lanzador se quedó reintentando el horneado de `n1_s15_d6_MIENTE` (16 intentos, uno por minuto) sin recoger nada. Ninguna partida se perdió ni se apartó por la caída.
- **Docker, ahora.** Responde (`docker info`: 29.7.2, 0 contenedores, 197 imágenes). Con Docker de vuelta, el horneado de `n1_s15_d6_MIENTE` terminó y su subida acabó. El lanzador se
  congeló (SIGSTOP) a las 07:41, mientras subía, para revisar antes de seguir.
- **Disco.** 29 GB libres. Antes de la caída, unos 12,4-12,8 GB durante horas: el archivo al T7 copiaba y borraba bien (6-8 `.art.log` por pasada), pero el disco de Docker (`Docker.raw`)
  había crecido. Al reiniciarlo se liberaron unos 16 GB; ahora ocupa 7,7 GB. Pudo influir en la caída; no está demostrado.
- **Cadenas.** Las 82 empezadas están en un punto limpio: el último día terminado tiene los dos diarios, los dos cuadernos de fin y la latencia medida, y el cuaderno que leerá el día
  siguiente es idéntico al de fin (md5). Dos aún no han empezado (n1 s16 MIENTE y HONESTA). La única cadena que quedó a medias en el horneado, `n1_MIENTE_s15` (día 6), se horneó con los
  cuadernos del día 5, iguales a los de fin; su imagen está subida y se pedirá al seguir.
- **Partidas pedidas durante la caída.** 5 (n1 s14 d19 CONGELADA, n1 s15 d11 CONGELADA, n1 s15 d7 HONESTA, n1 s14 d17 HONESTA, n1 s14 d14 MIENTE). Las 5 terminaron en la plataforma sin
  error (07:15-07:32); faltaba bajarlas, y se bajan al seguir.
- **Totales.** 1.025 partidas completadas de 1.140 (5 más terminadas en la plataforma, sin bajar); 5 partidas apartadas por la plataforma, todas repetidas con éxito; 9 vidas marcadas.
  La nueva, desde el último parte: `n1_s14_d16_HONESTA`, asiento 11, rareza de la zona de la fortaleza (5,8 %).
- **Decisión** (regla de Manel): todas las cadenas en punto limpio → se reanuda el campo tal como estaba sellado, sin cambiar nada: el mismo proceso, descongelado (SIGCONT).
  `motor/model.py` intacto; ninguna pieza sellada tocada.
- **Corrección de la entrada anterior (07:55):** los totales que puse estaban mal contados. En el estado, al congelar, había **1.031 partidas completadas** (no 1.025), y las 5 terminadas
  en la plataforma, aún sin bajar, van aparte. Hay **11 vidas marcadas** (no 9):
  - 9 por la rareza de la zona de la fortaleza: n1 s1 d19 CONGELADA a11, n1 s3 d7 CONGELADA a10, n1 s6 d3 MIENTE a11, n1 s6 d12 HONESTA a11, n1 s8 d3 HONESTA a10,
    n1 s7 d14 HONESTA a11, n1 s13 d6 HONESTA a11 (8,6 %), n1 s15 d1 HONESTA a11 (14,5 %) y n1 s14 d16 HONESTA a11 (5,8 %);
  - 2 por latencia leve: n1 s5 d11 CONGELADA a10 (1,89 % sobre el tic) y n14 s6 d4 MIENTE a11 (1,12 %).
  
  El resto de la entrada no cambia. El lanzador se descongeló a las 07:42 y siguió: subió la imagen y pidió `n1_s15_d6_MIENTE`.

- (2026-10-20T12:00:45) Partida `n1_s16_d9_HONESTA` APARTADA por fallo de la plataforma (n1_s16_d9_HONESTA asiento 11: la plataforma borro el contenedor antes de recoger el diario); se reintenta una vez con la misma imagen y semilla (regla de la mesa del 18-oct, 13:43).

## (20-oct-2026, 15:35) Campo P7-67 TERMINADO: estado e incidencias (sin mirar resultados del sello)

- **Estado.** 1.140 de 1.140 partidas completadas, 84 de 84 cadenas. Nivel 1: MIENTE, CONGELADA y HONESTA, 320 cada una. Niveles 2, 3 y 14: MIENTE y HONESTA, 30 cada una. Cierre a las 15:28.
  Todas las vidas tienen cuaderno de fin. 0 días perdidos.
- **Paradas (3, todas resueltas por la mesa):**
  - 17-oct 21:42, guarda (n1 s1 d19 CONGELADA a11, 21,1 %); resuelta con la rareza de la fortaleza (enmienda 2);
  - 18-oct 03:17, guarda (n1 s3 d7 CONGELADA a10, 5,9 %); resuelta con la zona de la fortaleza (enmienda 3);
  - 18-oct 13:25, diario perdido por la plataforma (n1 s4 d9 HONESTA a10); resuelta con apartar y reintentar (enmienda 4).
- **Caída de Docker Desktop** (20-oct, desde las 07:19): revisada y reanudada sin cambios (entrada de las 07:50).
- **Partidas apartadas por fallo de la plataforma (6, repetidas con la misma imagen y semilla, todas bien):** n1 s4 d9 HONESTA, n1 s10 d7 MIENTE, n1 s10 d20 MIENTE, n1 s11 d18 HONESTA,
  n1 s15 d2 MIENTE, n1 s16 d9 HONESTA.
- **Vidas marcadas (13; su partida sale entera en la robustez):**
  - 11 por la rareza de la zona de la fortaleza (bloqueados sin cuerpo > 5 %, la mayoría en la zona): n1 s1 d19 CONGELADA a11 (21,1 %), n1 s3 d7 CONGELADA a10 (5,9 %), n1 s6 d3 MIENTE a11
    (5,4 %), n1 s6 d12 HONESTA a11 (12,2 %), n1 s8 d3 HONESTA a10 (5,3 %), n1 s7 d14 HONESTA a11 (8,3 %), n1 s13 d6 HONESTA a11 (8,6 %), n1 s15 d1 HONESTA a11 (14,5 %), n1 s14 d16 HONESTA a11
    (5,8 %), n1 s16 d1 HONESTA a11 (6,3 %) y n1 s16 d10 MIENTE a11 (13,3 %);
  - 2 por latencia leve (> 1 % de decisiones sobre el tic, por debajo de la regla dura del 10 %): n1 s5 d11 CONGELADA a10 (1,89 %) y n14 s6 d4 MIENTE a11 (1,12 %).
- **Vigilancia de CONGELADA:** pasó (la confianza vuelve a 0,5 tras la primera llegada).
- **Disco:** 70 pasadas del archivo al T7; 2.054 `.art.log` borrados tras copiar y releer por md5, 0 distintos. 20 GB libres al cerrar. La vigilancia de 10 GB no saltó.
- **Gasto:** plataforma, 1.146 créditos de experiencia (1.140 partidas + 6 reintentos); consola, 0 $. `motor/model.py` intacto.
- No se ha corrido el guion de análisis sellado. Espera a Manel.

## (20-oct-2026, 17:40) Apertura del sello

- Comprobaciones previas, todas en orden: `model.py` intacto; `analiza_P7_67.py` con el md5 de la enmienda 1 (`7bef2e46…`), igual antes y después de correr; `SELLO_P7_67.md` sin cambios desde la
  enmienda 4; partidas por brazo y nivel según el diseño (1.140); las 2.280 vidas con diario y cuaderno de fin; 13 partidas marcadas.
- Guion sellado corrido tal cual (3 min). **P1 PASA** y **P2 PASA**; **P3 NO PASA** y **P3b NO PASA**. Ningún veredicto cambia en las dos cuentas de robustez. Detalle, descriptivo, cotas y GIF en
  `informe_P7_67_campo.md` (escrito por `escribe_informe_P7_67_campo.py`; `informe_P7_67.md` ya era el del primer banco y no se sobrescribe).
- Saldo de créditos: la API no lo da; no consta.

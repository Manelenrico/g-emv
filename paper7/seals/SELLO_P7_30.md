# SELLO P7-30 · El segundo campo de la primera etapa: nacer sin saber, con la pieza rápida y la curiosidad del cuánto

*8-oct-2026. Escrito ANTES de pedir ninguna partida del campo (el humo de freno, días 1-3 de P7-29/29b, es anterior y no cuenta en el campo). Coste previsto: hasta 120 partidas
en la plataforma; consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Cuerpo y congelados sin tocar. Archivos `_P7`; una vida por proceso; la memoria viaja
solo en el cuaderno.*

## El diseño

- Tres brazos, como interruptores de la misma imagen (`Dockerfile.pareja_P7_30` = la del humo de P7-29b): **TECHO** (nace sabiendo, con pedir), **APRENDE** (nace sin saber,
  cuaderno que viaja de un día al siguiente), **BORRADO** (nace sin saber, cuaderno vaciado cada noche). Las piezas de P7-29b en los tres: caché por tic del recuerdo (arreglo 0),
  la curiosidad solo mueve por curiosidad (arreglo 1), el corte no entra en la media del efecto y se guarda como recuerdo del acto (arreglo 3), y la curiosidad del cuánto
  (`nace_P7_29.py`); sin red de muros (quitada por la mesa, P7-29b). Pedir corregido (P7-17) y lo dado entregado (P7-19) en los tres; ojos compartidos apagados. 20 días,
  dos series; la misma semilla para los tres brazos cada día.
- **Semillas nuevas**, declaradas antes de jugar (`semillas_P7_30.json`): la sucesión de siempre, 20260916 + k·104729, k = 178 a 197 (las siguientes a las del humo de P7-29,
  175-177); la serie 2 juega las mismas 20 en orden inverso. Serie 1: 38902678, 39007407, …, 40892529.
- El freno (paso 1 de la mesa) se evalúa sobre el humo de P7-29/29b antes de pedir ninguna partida del campo (`freno_P7_30.py` -> `P7_30_freno.json`): (a) el cuaderno viaja y
  se lee; (b) en al menos 4 de las 6 vidas la criatura toca algún objeto desconocido; (c) en al menos una criatura sube la creencia de alguno de los dos objetos; (d) la guarda
  de latencia pasa en las 6 vidas. Resultado en el informe.

## Definiciones, fijadas antes de medir (las de SELLO_P7_24.md, con las mismas palabras)

- **Primer contacto** con un objeto: el primer tic en que una unidad de esa clase entra en el zurrón. **Recuerdo firme**: un uso completado sin la marca «al menos».
- **Creencia** de un objeto: la del cuaderno con el recuerdo neutro (`cuaderno_P7.creencia`; en este campo, `CuadernoP29.creencia`: la misma media, sin los cortes, por el
  arreglo 3), por situación (dentro/fuera); la de la ración, la mayor de sus situaciones; la del botiquín, la de dentro del círculo. **Ignorancia**: la del cuaderno
  (`ignorancia`, P7-6), al cerrar el día. **Ignorancia del cuánto**: `ignorancia_cuanto` del cuaderno (peso del neutro / (neutro + pesos de los recuerdos firmes)), al cerrar el día.
- **Instantes de vida desde el primer contacto** (E2): los tics vividos desde el tic del primer contacto hasta el tic del primer recuerdo firme, sumando los de los días
  intermedios enteros si hay más de un día entre los dos.
- **Puesto**: `final.placement` de cada vida (1 el mejor, 16 el peor). **Diferencia de puesto** APRENDE − TECHO (y BORRADO − TECHO, y APRENDE − BORRADO): media de las
  diferencias emparejadas por serie, día y asiento; su error estándar, el de esas diferencias emparejadas (desviación típica / raíz de n). Días 1 a 5: n = 2 series × 5 días ×
  2 asientos = 20 parejas; días 16 a 20: 20 parejas.
- **Vida al usar el botiquín** (E6): la vida en el tic de apertura del canal (registro `P7_nace_uso`), mediana sobre todas las aperturas de los días 11 a 20 del brazo.
- **Tiempo en `ir_curioso`**: tics con `RADIOGRAFIA.elegido` = `ir_curioso` (y, aparte, solo los tics con el paso listo, P7-25).
- **Cortes**: usos no completados (huella con `corte`); se cuentan aparte y no entran en ninguna creencia.
- **Vida al usar el botiquín cuando le pesa la curiosidad del cuánto**: aperturas de canal del botiquín en las que la fila `R-CURIOSIDAD-CUANTO` de la foto de usar está
  aliviada (lo que le falta de vida, hp_max − hp, es mayor que lo más alto que sabe que da el botiquín, `sabido_max` del cuaderno en ese momento); se da la vida en esas
  aperturas frente a las demás.
- **Latencia**: por brazo y vida, mediana, p95 y máximo de `RADIOGRAFIA.ms` (el tiempo de cada decisión), la fracción de decisiones por encima del tic (41,7 ms) y la fracción
  de pasos listos bloqueados sin un cuerpo delante (`guarda_latencia_P7_29.py`).

## Las reglas

| | regla | pasa si |
|---|---|---|
| E1 | descubre | APRENDE: al acabar el día 5, las 4 criaturas tienen ≥ 1 recuerdo firme del botiquín y ≥ 1 de la ración; al acabar el día 10, ignorancia < 0,3 en los dos objetos en ≥ 3 de las 4 |
| E2 | aprende a aprender | en ≥ 3 de las 4 criaturas de APRENDE, el segundo objeto que llega a su primer recuerdo firme tarda menos instantes de vida desde su primer contacto que el primero |
| E3 | qué aprende antes | en ≥ 3 de las 4, el día en que la creencia de la ración llega a 12 (80 % de 15) es anterior al día en que la del botiquín dentro llega a 40 (80 % de 50); no llegar cuenta como después |
| E4 | qué pierde y qué recupera | días 1-5: APRENDE − TECHO > 2 errores estándar (peor puesto); días 16-20: esa diferencia ≤ la mitad de la de los días 1-5 |
| E5 | sin memoria no recupera | BORRADO − TECHO en los días 16-20 ≥ la mitad de la de los días 1-5 |
| E6 | lo aprendido cambia la conducta | días 11-20: mediana de la vida al abrir el botiquín, APRENDE < BORRADO |
| E7 | el cuánto | en APRENDE, la creencia del botiquín dentro del círculo (sin cortes) llega a 35 o más el día 20 en al menos 3 de las 4 criaturas |
| E8 | no se hunde | en los días 16 a 20, la diferencia de puesto APRENDE − BORRADO no es mayor que en los días 1 a 5 por más de 2 errores estándar (el error estándar de la diferencia de las dos medias: raíz de la suma de los dos errores estándar al cuadrado) |

Sin predicción, solo medida: APRENDE frente a BORRADO en puesto (todos los días); lo de P7-24 y, además, firmes, «al menos» y cortes (aparte) por objeto; la ignorancia del
cuánto día a día; con cuánta vida usa el botiquín cuando le pesa la curiosidad del cuánto; la latencia por brazo y vida.

## Guardas

Disco: limpieza de Docker tras cada horneado; si baja de 5 GB, parada limpia y aviso. Red: esperar y reintentar, o parada limpia con la hora. Cortes de la plataforma
(artefacto ausente): como en P7-27 (se rescata el diario del registro de salida, se marca como parcial con el tic del corte, la cadena sigue con el cuaderno del corte;
en las medidas, el aprendizaje cuenta hasta el corte y la partida entera sale de puesto, vida al morir y causa; en las emparejadas se quita el par; E4, E5 y E8 se repiten
también sin excluir nada; si faltara también el cuaderno, parada y aviso). Latencia (mesa, P7-30): si en alguna vida más del 1 % de las decisiones pasan de 41,7 ms, o más
del 5 % de los pasos listos salen bloqueados sin un cuerpo delante, la cadena para y avisa; mediana, p95 y máximo se informan sin parar por ellos. Nada de resultados
parciales: el sello se evalúa una vez, al final.

## md5 de lo sellado

- `nace_P7_29.py`: `93fbba4cd052c583f9fcb30c24e8504b`
- `nace_P7_23.py`: `0083986bd7d2e51ee0295d6860e9e06a`
- `recuerdo_P7_23.py`: `519e69e67026c880d49af76bc14eed30`
- `policy_pareja_P7_29.py`: `08db5b71d7e5c5a3dce3f47fcf4b4643`
- `descubre_P7.py`: `1dac5ed0f51b06fcb6b6a5aa31c3e1c5`
- `pide_P7.py`: `4766e5a3b0afdc20b787d0b79da9fe31`
- `cuaderno_P7.py`: `f4c6a9dae0af4831cfa930da18b74376`
- `guarda_latencia_P7_29.py`: `21696e98acbc8d8e096c63d75694daf1`
- `Dockerfile.pareja_P7_30`: `7abfd1629235767d8c57018692976ce0`
- `lanza_P7_30.py`: `7d4afba15af5e6bb6b12099e8424e943`
- `semillas_P7_30.json`: `f1366f62683b3dbd11d17a33c18a3c7b`

Commit del sello: `f10da2238951` (gemv-coworld, paintball); este añadido va en el commit inmediatamente posterior, también anterior a la primera partida del campo.

## Añadido posterior (8-oct-2026, decisión de la mesa tras la parada por la guarda de latencia; declarado como cambio posterior)

La guarda de latencia (regla de la mesa de P7-30) NO PASA en 7 vidas de BORRADO, ninguna de TECHO ni de APRENDE. Motivos: latencia por carga de la plataforma (los 80 fijos jugaron a la vez; el cuaderno de BORRADO está vacío, así que no es el recuerdo) en 5 o 6, y un obstáculo invisible para el cuerpo (probablemente un rival camuflado) en 1 o 2. La lista:

| partida | asiento | ms mediana · p95 · máx | decisiones sobre el tic | pasos listos bloqueados sin cuerpo | motivo de la guarda |
|---|---:|---|---:|---:|---|
| serie 1 día 1 BORRADO | 11 | 5.76 · 44.68 · 117.55 | 7.36 % | 0.4 % | decisiones por encima del tic 7.36 % > 1 % |
| serie 1 día 7 BORRADO | 10 | 5.54 · 16.95 · 78.5 | 0.09 % | 40.5 % | bloqueados sin cuerpo 40.5 % > 5 % |
| serie 1 día 12 BORRADO | 10 | 10.25 · 29.46 · 71.0 | 3.68 % | 1.5 % | decisiones por encima del tic 3.68 % > 1 % |
| serie 2 día 6 BORRADO | 11 | 13.82 · 33.23 · 101.62 | 3.58 % | 0.2 % | decisiones por encima del tic 3.58 % > 1 % |
| serie 2 día 7 BORRADO | 11 | 10.76 · 44.21 · 110.23 | 6.49 % | 0.0 % | decisiones por encima del tic 6.49 % > 1 % |
| serie 2 día 11 BORRADO | 11 | 5.85 · 41.56 · 121.62 | 4.96 % | 0.4 % | decisiones por encima del tic 4.96 % > 1 % |
| serie 2 día 17 BORRADO | 10 | 9.42 · 29.94 · 93.67 | 1.08 % | 0.2 % | decisiones por encima del tic 1.08 % > 1 % |

Lo decidido: (1) el campo sigue; las cadenas de APRENDE se reanudan una serie detrás de otra (no las dos a la vez). (2) El sello se evalúa DOS veces: con todas las vidas, y
quitando esas 7 partidas enteras (los dos asientos) de las comparaciones de puesto, vida al morir y causa, y sus pares emparejados (además de las partidas con corte de la
plataforma, si las hay). Si alguna predicción cambia de resultado entre las dos cuentas, se dice. (3) La guarda sigue igual para lo que queda: si salta en una vida de APRENDE,
parada y aviso; si salta en otra de BORRADO o TECHO (ya jugados), se marca y se sigue. (4) La casilla del obstáculo invisible de serie 1 día 7 asiento 10 se describe en el informe.
Nada del sello se ha mirado antes de este añadido ni se mira hasta el final.

## Añadido posterior (8-oct-2026, decisión de la mesa tras la segunda parada; declarado como cambio posterior, solo de rendimiento)

La guarda de latencia salta en serie 1 día 2 APRENDE asiento 11 (5.17 % de decisiones por encima del tic; mediana 9.74 ms, p95 42.48, máximo
110.45; 2 recuerdos en el cuaderno; jugada con los fijos ya acabados). Causa (réplica en banco, que reproduce el crecimiento): la decisión crece con los objetos
recordados del mapa: el cuerpo pide `_promesa` por cada objeto recordado (`_mejor_objeto`, decisor_zs.py:684-706) y para el botiquín y el camuflaje cada petición vale dos
`filas` enteras (decisor_zs.py:656-658, 674-677), que con las piezas del siete pesan el doble cuando la hermana y consumibles están a la vista (`regalo_nace`); 11 → 42
`filas` por tic. Lo decidido:
1. Se aplica una MEMORIA POR TIC de `D._promesa` por (observación, memoria, objeto) en `nace_P7_29.py` (misma idea que la caché del recuerdo, arreglo 0): mismos
   argumentos, mismo resultado. Prueba de que las decisiones son idénticas bit a bit: la vida serie 1 día 2 asiento 11 replicada con y sin la memoria, 10.416 tics
   iguales de 10.416; y las 16 vidas replicables de los días 16-20 de P7-24 con la memoria, 126.417 tics iguales y 3 distintos (los mismos 3 de siempre, sin la memoria
   también). md5 nuevo de `nace_P7_29.py`: `9f43cd057c0eb6f6e3119b0989bbf233` (el sellado era `93fbba4cd052c583f9fcb30c24e8504b`). Las imágenes de APRENDE desde el día 3 de
   la serie 1 y toda la serie 2 llevan la memoria; los 80 fijos y los días 1-2 de la serie 1 se jugaron sin ella.
2. La vida serie 1 día 2 APRENDE asiento 11 se queda en el campo y se marca como las 7 de BORRADO: su cuaderno viaja y su aprendizaje cuenta; la partida entera entra en
   la doble evaluación del sello (con y sin las partidas marcadas). Partidas marcadas: las 7 de BORRADO del añadido anterior y esta (8 en total).
3. La serie 1 se reanuda desde el día 3 y después la serie 2, una detrás de otra. La guarda no cambia; si vuelve a saltar en una vida de APRENDE, parada y aviso.
4. El obstáculo invisible de serie 1 día 7 BORRADO asiento 10 (casilla (14,25), suelo en el mapa, nadie a la vista para ningún asiento, 711 pasos listos bloqueados y
   después la casilla se cruza; el camuflaje no oculta a 1 casilla) queda anotado como rareza del mundo, sin más análisis; pregunta pendiente para Ari.
Nada del sello se ha mirado.

## Añadido posterior (8-oct-2026, decisión de la mesa tras la tercera parada; declarado como cambio posterior)

La guarda salta en dos vidas más de APRENDE: serie 1 día 5 asiento 10 (2,19 % de decisiones sobre el tic) y serie 2 día 9 asiento 10 (4,26 %; el último cuarto a 27,8 ms con
12 candidatos de media, una pelea). La serie 2 arrancó pese a la parada de la serie 1 por un fallo del encadenado (el `&&` miraba la salida del filtro de texto, no la del
lanzador); corregido. Lo decidido:
1. Memoria por tic de la doble evaluación de `regalo_nace`: PROBADA y NO APLICADA. Da decisiones idénticas (s1 d5 asiento 10: 12.120 de 12.120; s2 d9 asiento 10: 14.568 de
   14.568, comparadas con y sin memoria), pero no ahorra tiempo: la firma de la escena cuesta lo que ahorra (último cuarto 4,34 → 4,30 ms en esta máquina). `nace_P7_29.py`
   se queda con el md5 del añadido anterior (`9f43cd057c0eb6f6e3119b0989bbf233`).
2. Desde ahora la guarda de latencia MARCA y no para, también en APRENDE: cada vida que la pase (> 1 % de decisiones sobre el tic o > 5 % de pasos listos bloqueados sin cuerpo)
   se marca y su partida entera entra en la segunda cuenta del sello. Solo para si una vida de cualquier brazo supera el 10 % de decisiones sobre el tic o el 5 % de pasos
   bloqueados sin cuerpo (`guarda_latencia_P7_29.py`, `para`). Marcadas hasta aquí: 7 de BORRADO, 3 de APRENDE (s1 d2 asiento 11, s1 d5 asiento 10, s2 d9 asiento 10).
3. La serie 1 se reanuda desde el día 6 y la serie 2 desde el día 10, una detrás de otra; una parada de verdad para las dos.
4. El informe final da, además de las dos cuentas del sello: por vida, la fracción de decisiones sobre el tic frente a su puesto y su muerte (si las vidas lentas acaban
   peor); y declara que APRENDE y BORRADO cargan con el coste de las piezas del siete (2-4 veces el de TECHO por candidato) y TECHO no, así que E4 está inclinada en contra
   de APRENDE.
5. La diferencia de la réplica en s2 d9 asiento 10 (388 tics) queda apuntada; no se persigue ahora.
Nada del sello se ha mirado.

## Añadido posterior (9-oct-2026, decisión de la mesa tras la cuarta parada; declarado como cambio posterior)

Serie 1 día 7 APRENDE asiento 10: el 41,0 % de los pasos listos salen bloqueados sin un cuerpo delante, en la MISMA casilla que BORRADO asiento 10 el mismo día (semilla
k = 184, 39531052): desde (15,25) hacia el oeste, (14,25), suelo en el mapa, nadie a la vista, hacia los tics 4.400-5.100; después la casilla se cruza. Lo decidido:
1. La casilla (14,25) de la semilla k = 184, en esa ventana (asiento 10), queda anotada como RAREZA DEL MUNDO, con las dos partidas (s1 d7 BORRADO y s1 d7 APRENDE). Las dos
   siguen marcadas y entran en la segunda cuenta del sello.
2. Para esa semilla, esa casilla y esa ventana la regla de parar por más del 5 % de pasos bloqueados sin cuerpo no se aplica: se marca y se sigue
   (`guarda_latencia_P7_29.RAREZAS`, `es_rareza`). En cualquier otro sitio la regla sigue igual.
3. La serie 1 se reanuda desde el día 8 y después la serie 2 desde el día 10, una detrás de otra.
4. Pregunta para Ari: qué ocupa la casilla (14,25) en la semilla k = 184 hacia los tics 4.400 a 5.100, que bloquea el paso desde el este sin que el agente lo vea.
Nada del sello se ha mirado.

# Paper ocho · Confirmación v1 (prompt 72)

Aquí van números, sin interpretar. La evaluación completa está en `salida/evaluacion_confirmacion_v1.md` y `.json`.

## Qué se ha hecho

**1. P32, la criatura de posición** (`cuerpo_valle.compone_posicion` y el interruptor `posicion_v30`). Es RG32r en todo menos en cómo vale cada foto:
- Usa las mismas filas, el mismo reparto y la misma saturación de las ganancias (`satura_v8`, que RG32r tiene encendida).
- La foto vale la distancia del motor con solo su término de posición: √Σ w_pos·(ganancia − pérdida − meta)².
  - Los pesos y las metas se importan de `DEFAULT_CONFIG`.
  - No hay tensión, ni techo, ni mínimo basal (el mínimo no mueve la posición), ni acoplamiento.
- La voz, la interrupción y el contagio salen de las seis sumas crudas, como en S32.
- No hizo falta parar: todo tenía un equivalente limpio.

**Pruebas de P32** (`prueba_p32.py`, resultado en `salida/prueba_p32.json`):
- **(a)** En 2.000 estados al azar, la `d` de P32 es idéntica a `opponent_distance` del motor con los pesos de tensión y las sensibilidades a 0. En 2.000 conjuntos de filas al azar, con la saturación, es idéntica a su cálculo directo.
- **(b)** Su voz es la misma que la de S32 para las mismas filas.
- **(c)** Dos partidas cortas (3 días, semillas 2101 y 2102, bestia de día) juegan y deciden con el valorador de posición. No se contaron vivas.
- **(d) La puerta:** con el interruptor apagado, RG32r y S32 salen idénticas a las del experimento (bestia de día, semilla 1001, 40 días). Se comparó el registro del mundo entero línea a línea (16.000 líneas) y las muertes.

**2. Medida de ambivalencia** (`ambivalencia.py`):
- Usa el `State` del motor solo como instrumento, sobre las seis sumas de ahora del registro de criaturas.
- La ambivalencia de cada dimensión es min(ganancia, pérdida); la del estado es la mayor de las tres.

Probada sobre estados viejos del experimento (semillas 1001–1004), sin mirar coincidencias:

| clases | media | cuartos | máximo | estados con cero |
|---|---|---|---|---|
| RG32r y S32 | 0,68 | 0,57–0,79 | 2,1 | ninguno |
| RG032r y S032 | 0,0001 | — | — | 99 % |

**3. Congelado** con la etiqueta `valle-confirmacion-v1`:
- Commit `79afe666`, objeto de la etiqueta `cdac652f`.
- Las huellas están en `CONGELADO_P8.md`, en una sección nueva. Todo lo de v1 sigue igual salvo `cuerpo_valle.py` y `banco_v7.py`.
- Las predicciones están tal cual en `predicciones_confirmacion.md`.
- Subido al repositorio privado gemv-coworld (`paintball`) después de pasar `revisa_subida.py` (0 correos, 0 claves y 0 rutas en 1.945 líneas) y `copia_taller.py --solo-buscar` (limpio).
- GitHub registró el push el 2026-11-03 a las 06:19:37 UTC.
- `git ls-remote`: `paintball` = `79afe666`, etiqueta = `cdac652f`.
- El push también subió los dos commits locales anteriores, que están por debajo del congelado: los resultados v1 (`8608d490`) y la exploración v1 (`87c051b2`).

**4. Partidas:**
- 320 partidas de 40 días, semillas 2001–2040:
  - bestia de día: RG32r, S32, P32, RG032r y S032;
  - sequía dura: RG32r, S32 y P32.
- Las jugó `lanza_confirmacion.py`, que usa `lanzador.una`, el mismo del experimento. En cada decisión pregunta en el mismo estado exacto a los tres valoradores (motor, sumas y posición), con el mismo desempate y la misma regla del empate exacto.
- De 07:20 a 12:48 del 3 de noviembre (5 h 28 min), sin fallos. Ocupan 1,7 GB en el T7 (`valle_confirmacion/`).
- **Comprobación interna:** cada clase coincide al 100 % con su propio valorador, en las ocho combinaciones de clase y mundo.

**Incidente:** mi primera prueba corta del lanzador la lancé con `python -c`. Los procesos hijos no heredaron la carpeta ni los días de prueba, y se pusieron a jugar partidas de 40 días con las semillas de prueba 2101–2103 en la carpeta oficial. Las paré y moví la carpeta entera, sin borrar nada, a `valle_prueba_p32/carpeta_oficial_por_error_2101-2103`. Eso fue antes de congelar y de lanzar el experimento de confirmación, que empezó en una carpeta vacía.

## Cuánto deciden igual

Son 2.000 decisiones al azar por clase y mundo. Cada celda es el % de veces que el valorador elegiría la misma opción que la criatura.

| clase | mundo | con el motor | con las sumas | con la posición |
|---|---|---|---|---|
| RG32r | bestia de día | 100 | 85.2 | 92.0 |
| S32 | bestia de día | 79.1 | 100 | 78.5 |
| P32 | bestia de día | 94.7 | 87.1 | 100 |
| RG032r | bestia de día | 100 | 96.8 | 96.0 |
| S032 | bestia de día | 94.5 | 100 | 90.3 |
| RG32r | sequía dura | 100 | 87.2 | 90.6 |
| S32 | sequía dura | 81.7 | 100 | 82.8 |
| P32 | sequía dura | 93.5 | 86.8 | 100 |

Las tablas por situación (hambre, bestia, hermana y noche) están en la evaluación completa.

**Por cuartos de ambivalencia** (% igual; los cuartos son de los estados de cada clase y mundo):

| clase (valorador) | mundo | Q1 (la menos) | Q2 | Q3 | Q4 (la más) |
|---|---|---|---|---|---|
| RG32r (sumas) | bestia de día | 93.2 | 85.2 | 82.6 | 79.6 |
| RG32r (posición) | bestia de día | 94.6 | 91.2 | 92.2 | 90.0 |
| S32 (motor) | bestia de día | 86.6 | 79.8 | 72.8 | 77.4 |
| P32 (motor) | bestia de día | 96.0 | 94.8 | 94.8 | 93.2 |
| RG32r (sumas) | sequía dura | 93.0 | 89.6 | 86.4 | 80.0 |
| RG32r (posición) | sequía dura | 95.6 | 91.4 | 89.8 | 85.8 |
| S32 (motor) | sequía dura | 85.6 | 79.8 | 79.6 | 81.6 |
| P32 (motor) | sequía dura | 94.0 | 94.0 | 93.2 | 92.6 |

En RG032r y S032 la ambivalencia vale 0 en casi todos los estados, así que no hay cuartos.

## Las predicciones

- **Intervalos:** del 95 %, por bootstrap pareado por semilla, con 10.000 remuestreos.
- **C5 y C6:** bootstrap de estados agrupados por partida. Se evalúan en cada mundo y en los dos juntos.
- **Regla:** «más» o «menos» se cumple si la diferencia va en esa dirección y el intervalo no incluye el cero.

| | predicción | medida | diferencia [IC 95 %] | resultado |
|---|---|---|---|---|
| C1 | en bestia de día, RG32r vive más que S32 | vivas al final, RG32r − S32 | +0.30 [−0.05, +0.65] | **no se cumple** |
| C2 | RG32r, menos turnos con el hambre al máximo que S32 (bestia de día) | por 1.000 turnos vivos, RG32r − S32 | −1.72 [−2.32, −1.14] | **se cumple** |
| C3 | motor y sumas coinciden menos con ganancias que sin ellas | coincidencia RG32r–S32 − RG032r–S032 (bestia de día) | −0.116 [−0.135, −0.097] | **se cumple** |
| C4 | en bestia de día, RG32r vive más que P32 | vivas al final, RG32r − P32 | +0.05 [−0.28, +0.38] | **no se cumple** |
| C5 | RG32r–S32 coinciden menos en Q4 que en Q1 | Q4 − Q1, bestia de día | −0.136 [−0.174, −0.097] | **se cumple** |
| | | Q4 − Q1, sequía dura | −0.130 [−0.168, −0.090] | **se cumple** |
| | | Q4 − Q1, los dos mundos | −0.133 [−0.160, −0.106] | **se cumple** |
| C6 | lo mismo para RG32r–P32 | Q4 − Q1, bestia de día | −0.046 [−0.076, −0.015] | **se cumple** |
| | | Q4 − Q1, sequía dura | −0.098 [−0.133, −0.063] | **se cumple** |
| | | Q4 − Q1, los dos mundos | −0.072 [−0.095, −0.048] | **se cumple** |

El texto sellado de C4 añade: «Si no se cumple, la ventaja viene de la distancia a la meta».

**Sequía dura** (sin predicción; se informa). Vivas al final:

| clase o diferencia | vivas |
|---|---|
| RG32r | 3.70 |
| S32 | 3.08 |
| P32 | 3.50 |
| RG32r − S32 | +0.62 [+0.15, +1.07] |
| RG32r − P32 | +0.20 [−0.17, +0.57] |
| S32 − P32 | −0.42 [−0.78, −0.07] |

**Todas las clases:**

| clase | mundo | vivas | hambre al máximo por 1.000 | muertes de hambre / bestia / otras (40 partidas) |
|---|---|---|---|---|
| RG32r | bestia de día | 7.30 | 1.20 | 8 / 19 / 1 |
| S32 | bestia de día | 7.00 | 2.92 | 21 / 18 / 1 |
| P32 | bestia de día | 7.25 | 1.72 | 8 / 21 / 1 |
| RG032r | bestia de día | 7.50 | 0.87 | 8 / 12 / 0 |
| S032 | bestia de día | 7.42 | 0.85 | 7 / 15 / 1 |
| RG32r | sequía dura | 3.70 | 14.71 | 158 / 12 / 2 |
| S32 | sequía dura | 3.08 | 18.07 | 174 / 21 / 2 |
| P32 | sequía dura | 3.50 | 15.74 | 169 / 8 / 3 |

## Exploración (añadido de Manel; no es predicción): dimensiones en conflicto a la vez

Una dimensión está en conflicto en un estado si su ambivalencia queda por encima de la mediana de esa dimensión en la muestra de la clase y el mundo. Cada celda es el % igual, con el número de estados entre paréntesis.

| clase (valorador) | mundo | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| RG32r (sumas) | bestia de día | 91.1 (473) | 85.3 (476) | 82.0 (633) | 83.0 (418) |
| RG32r (posición) | bestia de día | 94.5 (473) | 92.0 (476) | 91.9 (633) | 89.2 (418) |
| RG32r (sumas) | sequía dura | 92.5 (468) | 88.5 (460) | 85.8 (681) | 82.1 (391) |
| RG32r (posición) | sequía dura | 95.1 (468) | 90.7 (460) | 89.1 (681) | 88.0 (391) |
| S32 (motor) | bestia de día | 91.0 (413) | 78.6 (566) | 73.8 (633) | 76.0 (388) |
| S32 (motor) | sequía dura | 91.3 (427) | 80.9 (477) | 77.9 (768) | 79.0 (328) |
| P32 (motor) | bestia de día | 96.4 (445) | 95.0 (519) | 95.4 (631) | 91.4 (405) |
| P32 (motor) | sequía dura | 94.0 (463) | 92.7 (478) | 94.0 (655) | 92.8 (403) |

En RG032r y S032 casi no hay conflictos: 47 y 33 estados con 1 o más, de 2.000.

**Con 2 o 3 dimensiones en conflicto, cuál prioriza la opción elegida.** Es la dimensión en conflicto cuya posición, en la foto de esa opción, queda más por encima de la media de las opciones de ese turno. En cada fila, «criatura» es lo que eligió y las otras columnas son lo que elegiría cada valorador en esos mismos estados. Cada celda da F / R / S en %.

| clase | mundo | n | criatura | motor | sumas | posición |
|---|---|---|---|---|---|---|
| RG32r | bestia de día | 1051 | 33.1 / 18.7 / 48.1 | 33.1 / 18.7 / 48.1 | 35.3 / 16.3 / 48.4 | 32.4 / 21.7 / 45.9 |
| S32 | bestia de día | 1021 | 27.5 / 16.5 / 56.0 | 33.7 / 26.1 / 40.3 | 27.5 / 16.5 / 56.0 | 32.8 / 27.7 / 39.5 |
| P32 | bestia de día | 1036 | 31.4 / 20.0 / 48.6 | 32.5 / 19.6 / 47.9 | 34.7 / 16.5 / 48.7 | 31.4 / 20.0 / 48.6 |
| RG32r | sequía dura | 1072 | 29.4 / 16.4 / 54.2 | 29.4 / 16.4 / 54.2 | 33.0 / 15.9 / 51.1 | 29.5 / 20.6 / 49.9 |
| S32 | sequía dura | 1096 | 27.6 / 14.1 / 58.3 | 33.7 / 21.8 / 44.5 | 27.6 / 14.1 / 58.3 | 31.8 / 24.5 / 43.7 |
| P32 | sequía dura | 1058 | 29.4 / 17.2 / 53.4 | 31.5 / 16.4 / 52.1 | 33.1 / 15.2 / 51.7 | 29.4 / 17.2 / 53.4 |

## Gasto, comprobaciones y tiempo

- **Gasto:**
  - créditos de la plataforma: 0 (no hubo partidas en la plataforma);
  - dólares de la consola de Anthropic: 0 (sin llamadas).
- **Comprobaciones:**
  - `motor/model.py` md5 `1e511978c251130e95169ebf8443efa1` (sin cambios);
  - el sello de la confirmación sigue intacto al evaluar (todas las huellas de la sección nueva coinciden).
- **Tiempo:**
  - estimado: unas 9 h;
  - partidas: 5 h 28 min;
  - evaluación: 3 min.
- **Commit:** local, sin push.

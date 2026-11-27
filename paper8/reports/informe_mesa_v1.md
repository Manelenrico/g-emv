# Paper ocho · Los dilemas en la mesa v1 (prompt 74)

No se ha jugado ninguna partida. Aquí van números, sin interpretar. Las tablas completas están en:
- `salida/evaluacion_mesa_v1.md` (las respuestas, en `salida/mesa/mesa.jsonl`);
- `salida/explora_d73.md` (la exploración de D).

## 1. Los estados (`mesa_dilemas.py`)

**El montaje.** Se usa el mundo de siempre (`Valle.reset` con la semilla). La protagonista es A1, su hermana A2 y la vecina B1. Hay 20 variantes por estado: semillas 4001–4020, y con cada semilla una fila del bosque del norte y un sentido (este u oeste) al azar.

**La memoria la pone la propia criatura, viendo.**
- Lo lejano lo ve de cerca hace poco: anda con pasos dictados que el mundo da como siempre. Cada turno mira con su `actua`, y lo que ella elige no se hace.
- La hermana y la vecina están quietas y llaman «ven, lo necesito» fuerte (alcance 10) cada turno. Son acciones dictadas, que el mundo lleva como siempre.

| estado | grados | montaje |
|---|---|---|
| A | N de 1 a 10 | hambre 70; 1 comida a 2; montón de N a 12 en sentido contrario, visto a 4 (anda 8 pasos) |
| B | vida de la hermana de 90 a 10 | hambre 70; comida a 4; la hermana a 8 en sentido contrario, vista a 4 (anda 4 pasos), llamando |
| C | hambre de 30 a 100 | comida a 3 y la bestia a 4, a la vista |
| D | vida de la vecina de 90 a 10 | la hermana (vida 30) a 8 a un lado y la vecina a 8 al otro, las dos llamando; las ve a las dos (anda 8 pasos y vuelve 4) |

- **El hambre:** en A, B y C se pone a su valor justo antes de preguntar.
- **Comprobación previa:** antes de congelar se comprobó el montaje solo con el mundo, sin ninguna criatura. En los 160 casos probados la protagonista acaba en su sitio, lo lejano está a la vista al empezar (en D, la vecina se ve durante el paseo) y las llamadas llegan.

**La pregunta.**
- En el sitio del dilema, la criatura hace su `actua` una vez más. Antes se le vacían la cola de llamadas y el destino comprometido, y se desarman las ganas de llamar, para que mire todas sus fotos; eso no toca cómo valora.
- Cada opción se valora con su `foto`, sus `filas` y su valorador. También se valora con los otros dos.
- Las opciones:
  - A: el montón frente a la comida cerca;
  - B: la hermana frente a la comida;
  - C: la comida frente a la mejor de sus demás candidatas;
  - D: la vecina frente a la hermana.
- **Margen** = d(la otra) − d(dolor). Si es positivo, prefiere el dolor (en D, la vecina).
- **Punto de cambio:** el primer grado con margen positivo.

**Lo que no tiene un equivalente limpio (A).**
- La foto de «ir a por comida» imagina que coge una sola, y la memoria de la criatura guarda un valor por casilla, no cuántas comidas hay. N no entra en ninguna foto.
- Entre las comidas recordadas, solo la que más promete por distancia pasa a ser candidata. En los 1.000 estados de A el montón no está entre sus candidatas, y todas eligen la comida cercana.

## 2. Congelado, antes de preguntar a ninguna criatura

- **Etiqueta:** `valle-mesa-v1`. Commit `caf63cda`; objeto de la etiqueta `8b90a22e`.
- **Huellas:** en una sección nueva de `CONGELADO_P8.md`. Lo congelado antes sigue igual.
- **Predicciones:** tal cual, en `predicciones_mesa.md`.
- **Subida:** al repositorio privado gemv-coworld (`paintball`), después de pasar `revisa_subida.py` (0 correos, 0 claves y 0 rutas en 3.484 líneas) y `copia_taller.py --solo-buscar` (limpio).
  - GitHub registró el push el 2026-11-03 a las 14:27:46 UTC.
  - `git ls-remote`: `paintball` = `caf63cda`, etiqueta = `8b90a22e`.
- **Preguntas:** 3.600 (4 estados, sus grados, 20 variantes y 5 clases), en 17 s.

## 3. Las predicciones

Intervalos del 95 % por bootstrap sobre las 20 variantes.

| | predicción | medida | resultado |
|---|---|---|---|
| M1 | en A y B, el punto de cambio de RG32r está más arriba que el de S32 | A: +0.00 [0, 0]; B: +0.00 [0, 0] | **no se cumple** |
| M2 | la diferencia de puntos de cambio RG032r–S032 es menor que RG32r–S32 | media de los cuatro estados, normalizada: +0.000 [0, 0] | **no se cumple** |
| M3 | en C, RG32r se separa más de P32 cuanto más alta es el hambre | pendiente de \|margen RG32r − margen P32\| por punto de hambre: −0.00615 [−0.00628, −0.00603] | **no se cumple** |

En C, el punto de cambio medio es el grado 1 en RG32r y en P32.

## 4. Exploración (no es predicción)

**Puntos de cambio** (las cinco clases igual en las 20 variantes):

| estado | punto de cambio |
|---|---|
| A | grado 1: prefieren el montón con cualquier N |
| B | nunca: prefieren la comida con cualquier vida de la hermana |
| C | grado 1: prefieren la comida con cualquier hambre |
| D | nunca: prefieren la hermana con cualquier vida de la vecina |

**Margen medio** (con su valorador):

| estado | RG32r | S32 | P32 | RG032r | S032 |
|---|---|---|---|---|---|
| A (igual para N de 1 a 10) | +0.044 | +0.119 | +0.069 | +0.035 | +0.037 |
| B, hermana con vida 90–70 | −1.738 | −2.663 | −1.955 | −0.728 | −0.793 |
| B, hermana con vida 60–10 | −1.860 | −2.798 | −2.038 | −0.808 | −0.860 |
| C, hambre 30 | +1.557 | +3.582 | +1.973 | +0.712 | +0.824 |
| C, hambre 70 | +1.559 | +2.516 | +1.747 | +0.502 | +0.545 |
| C, hambre 100 | +2.159 | +3.738 | +2.175 | +1.313 | +1.313 |
| D (igual para vida de 90 a 10) | −0.103 | −0.466 | −0.108 | −0.038 | −0.069 |

En B, el margen solo cambia entre 70 y 60, que es donde la vida de la hermana pasa de «sana» a «herida» en lo que se ve de ella (`umbral_herida` 70). Los niveles por debajo dan el mismo margen.

**En C, con qué se compara la comida** (la mejor de sus demás candidatas):
- RG32r y P32: ir al bosque el 79 %, ir a casa el 21 %;
- S32, RG032r y S032: ir al bosque el 71 %, ir a casa el 29 %.

**Lo que elegirían entre todas sus candidatas:**
- A, B y C: ir a la comida cercana, el 100 %.
- D, con ganancias: ir a un matorral el 45 %, al bosque el 45 % y a una comida el 10 %.
- D, sin ganancias: al bosque el 60–65 % y a un matorral el 35–40 %.
- La opción de dolor es candidata en el 100 % de B, C y D, y en el 0 % de A.

**Márgenes de los tres valoradores sobre las mismas filas** (estados de RG32r):

| estado | motor | sumas | posición |
|---|---|---|---|
| A | +0.044 | +0.119 | +0.069 |
| B | −1.819 | −2.753 | −2.010 |
| C | +1.708 | +3.126 | +1.943 |
| D | −0.103 | −0.466 | −0.108 |

## 5. Exploración: la escena D del prompt 73 (`explora_d73.py`)

Es la medida del prompt 73: la primera a la que llega a una casilla o menos en los 44 turnos.

| clase | llega a la hermana | llega a la vecina | ninguna | al llegar a la hermana: casillas que se movió ella / la hermana | a la vecina: ella / la vecina |
|---|---|---|---|---|---|
| RG32r | 11 | 10 | 19 | 10.6 / 10.7 | 7.2 / 7.0 |
| S32 | 15 | 12 | 13 | 10.3 / 10.1 | 7.8 / 7.6 |
| P32 | 11 | 7 | 22 | 10.3 / 10.3 | 6.3 / 6.1 |
| RG032r | 13 | 4 | 23 | 9.4 / 9.5 | 12.5 / 11.5 |
| S032 | 29 | 4 | 7 | 10.4 / 9.9 | 6.8 / 7.5 |

**La primera decisión (turno 0):**
- RG32r, S32 y P32 eligen ir a la hermana en las 40 semillas, y en ese estado los tres valoradores también.
- RG032r elige ir al bosque en 39 (ir a casa en 1).
- S032 elige ir a la hermana en 39 (ir a casa en 1).
- En esos 39 estados de las dos clases sin ganancias: motor y posición eligen ir al bosque, y las sumas ir a la hermana.

**Sus decisiones en los 44 turnos** (media por partida; el resto de turnos sigue su destino comprometido):

| clase | ir a la hermana | ir a la vecina | ir a un matorral | ir al bosque | primera que va a una de las dos |
|---|---|---|---|---|---|
| RG32r | 1.2 | 0.0 | 1.6 | 3.8 | la hermana, en el turno 0, en las 40 |
| S32 | 1.3 | 0.1 | 1.8 | 3.4 | la hermana, en el turno 0, en las 40 |
| P32 | 1.2 | 0.0 | 1.5 | 3.7 | la hermana, en el turno 0, en las 40 |
| RG032r | 0.0 | 0.0 | 1.6 | 4.1 | la hermana en 1 (turno 39); nunca en 39 |
| S032 | 1.0 | 0.0 | 1.4 | 3.7 | la hermana, en el turno 0, en 39; nunca en 1 |

**La hermana y la vecina** (media por partida, de 44 turnos):
- se mueven 41–43 turnos;
- la hermana llama 22–27 turnos y la vecina 28–29.

## Gasto, comprobaciones y tiempo

- **Gasto:**
  - créditos de la plataforma: 0;
  - dólares de la consola de Anthropic: 0.
- **Comprobaciones:**
  - `motor/model.py` md5 `1e511978c251130e95169ebf8443efa1` (sin cambios);
  - el valle y las criaturas congeladas no cambian.
- **Tiempo:**
  - estimado: unas 6 h;
  - real: 1 h (14:30–15:30).
- **Commit:** local, sin push.

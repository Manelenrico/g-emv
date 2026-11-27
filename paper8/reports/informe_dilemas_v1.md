# Paper ocho · Dilemas v1 (prompt 73)

Aquí van números, sin interpretar. Las tablas completas están en `salida/evaluacion_dilemas_v1.md` y `.json`.

## 1. Las escenas (`escenas_dilemas.py`)

Una escena solo fija la situación de partida, que se pone justo después de `Valle.reset`. Las reglas del mundo y las criaturas no cambian, y todo lo que la escena no dice queda como siempre.

Los personajes:
- la protagonista es A1;
- su hermana es A2;
- la vecina es B1.

**Tres cosas no se podían montar tal cual con las reglas del mundo.** Uso la versión más parecida:

1. **La vista.** De día se ve a 5 casillas y al anochecer a 3. La criatura empieza sin recuerdos, y dárselos sería tocar la criatura. Lo que el prompt pone a 6, 8 o 12 casillas no lo vería, así que va al borde de la vista: a 5 de día y a 3 al anochecer.
2. **«Pidiendo ayuda».** La llamada la hace la otra criatura si ella lo elige, porque es de la misma clase. La escena la deja herida, pero no llama por ella. Se mide cuántos turnos llama.
3. **«Durmiendo fuera» (F).** De día, dormir lo elige cada criatura turno a turno. De noche, en cambio, el mundo la mantiene dormida de un tirón hasta la mañana o hasta un peligro. Por eso F empieza al anochecer (turno 240), con la hermana dormida de un tirón fuera de casa.

**La bestia en C y F.** Se pone ya bajada (en C, en el modo de la bestia de día; en F, en el de la noche), con su ruta al huerto. Como en el primer turno ninguna planta tiene fruto, la bestia se da la vuelta hacia su entrada, a un paso por turno: lo que hace siempre.

**E y F, que empiezan al anochecer.** Al adelantar el reloj, lo que tocaba dar fruto antes (huerto y matorrales) da fruto en el primer turno.

| escena | escalones | la protagonista | lo demás |
|---|---|---|---|
| A, esforzarse por recursos | montón de 1, 3 o 6 | (12,10), hambre 70 | 1 comida a 2 casillas al este; el montón a 5 al oeste (el prompt decía unas 12) |
| B, pasar hambre por la hermana | herida (vida 55), muy herida (30), moribunda (12) | (12,10), hambre 70 | 1 comida a 4 al este; la hermana herida a 5 al oeste (el prompt decía 6) |
| C, comida y bestia | hambre 50, 75 o 95 | (10,10) | 1 comida a 3 al este; la bestia a 4, junto a la comida |
| D, hermana o vecina | las dos muy heridas (vida 30) | (12,10) | la hermana a 5 al oeste y la vecina a 5 al este (el prompt decía 6) |
| E, frío o comida | 1, 3 o 6 comidas | (10,38), al anochecer (12°), a unas 16 casillas de casa | las comidas a 3 al sur, lejos de casa (el prompt decía 8) |
| F, tres dimensiones | — | (21,25), al anochecer, a 3 de la puerta de casa | la bestia a 2 (y a 2 de la puerta); 1 comida a 3 al oeste; la hermana dormida a 3 al sureste (el prompt decía 4 y 6) |

**Valores que he elegido yo,** porque el prompt no los fija:
- las vidas de cada nivel, dentro de las bandas de `vida_niveles`;
- en D, «muy herida» para las dos;
- en E y F, el resto del cuerpo como en la partida normal (hambre 0).

## 2. La comprobación con el tonto (`gif_escenas_dilemas.py`)

Hay un GIF de los primeros 44 turnos de cada escena y escalón (14), semilla 3001, en `salida/dilemas_gif/`. La foto de partida en números está en `montaje.json`.

**Están bien montadas.** Las posiciones, el hambre, la vida de las heridas, la comida en el suelo, la temperatura (16° de día, 12° al anochecer), la hermana dormida de un tirón (F) y la bestia bajada (C y F) salen como se dice arriba. Ninguna casilla de la escena coincide con un matorral en la semilla 3001.

**F tuvo que rehacerse antes de congelar.** En su primera versión la protagonista empezaba pegada a la puerta de casa, y todas las clases (y el tonto) entraban en el primer turno. La moví a 3 casillas de la puerta, con todo a la vista.

## 3. Congelado

- **Etiqueta:** `valle-dilemas-v1`. Commit `aa7fd4b1`; objeto de la etiqueta `59fcb4e5`.
- **Huellas:** en una sección nueva de `CONGELADO_P8.md`. Lo congelado antes sigue igual, comprobado archivo a archivo.
- **Predicciones:** tal cual, en `predicciones_dilemas.md`.
- **Subida:** al repositorio privado gemv-coworld (`paintball`), después de pasar `revisa_subida.py` (0 correos, 0 claves y 0 rutas en 2.744 líneas) y `copia_taller.py --solo-buscar` (limpio).
  - GitHub registró el push el 2026-11-03 a las 12:24:12 UTC.
  - `git ls-remote`: `paintball` = `aa7fd4b1`, etiqueta = `59fcb4e5`.

## 4. Las partidas

- **Qué se jugó:** 14 escena-escalones × 5 clases (RG32r, S32, P32, RG032r, S032) × semillas 3001–3040 = 2.800 partidas, hasta el final del día de la escena.
- **Cómo:** `lanza_dilemas.py`, con los registros del experimento y los tres valoradores preguntados en cada decisión.
- **Cuándo:** de 13:24 a 14:25 del 3 de noviembre (1 h 01 min), sin fallos.
- **Tamaño:** 3,4 GB en el T7 (`valle_dilemas/`).

**Medidas** (las fijé antes de jugar, en `evalua_dilemas.py`):
- **Qué elige:** la primera diana de la escena a la que llega en los primeros 44 turnos. Llegar es ponerse a una casilla o menos de la casilla o de la otra criatura; «casa» es estar dentro de su casa. Si no llega a ninguna, «ninguna».
- **Acepta el dolor:**
  - A: el montón;
  - B: la hermana;
  - C: la comida, con la bestia;
  - E: la comida, con frío.
- **Punto de cambio:** el primer escalón en que acepta el dolor (1 a 3), o 4 si no acepta en ninguno.

## 5. Las predicciones

| | predicción | medida | diferencia [IC 95 %], pareada por semilla | resultado |
|---|---|---|---|---|
| D1 | en F, RG32r y S32 eligen distinto más a menudo que en C y D | distinto en F − media en C y D | −0.069 [−0.106, −0.037] | **no se cumple** |
| D2 | en A, B y E, RG32r necesita un escalón más alto que S32 | A: punto de cambio / aceptación | +0.00 [0, 0] / +0.000 [0, 0] | no |
| | | B: punto de cambio / aceptación | +0.00 [0, 0] / +0.000 [0, 0] | no |
| | | E: punto de cambio / aceptación | −0.15 [−0.38, 0.00] / +0.050 [0.000, +0.125] | no |
| | | en las tres | | **no se cumple** |
| D3 | en todas las escenas, RG032r y S032 eligen igual más a menudo que RG32r y S32 | A / B / C / F | +0.000 [0, 0] en las cuatro | no |
| | | D | −0.375 [−0.575, −0.175] | no |
| | | E | +0.050 [0.000, +0.125] | no |
| | | en las seis | | **no se cumple** |

Fracción de semillas en que RG32r y S32 eligen distinto: F 0,000; C 0,000; D 0,275.

## 6. Exploración (no es predicción)

**Qué elige** (% de las 40 semillas):
- **A, B y C.** Las cinco clases llegan el 100 % a la diana más cercana: la comida a 2 (A), la comida a 4 (B) y la comida a 3 (C). Llegan en el turno 0 a 2, igual en todos los escalones. Nadie llega primero al montón ni a la hermana.
- **D.** Por clase:

  | clase | hermana | vecina | ninguna |
  |---|---|---|---|
  | RG32r | 28 | 25 | 48 |
  | S32 | 38 | 30 | 32 |
  | P32 | 28 | 18 | 55 |
  | RG032r | 32 | 10 | 58 |
  | S032 | 72 | 10 | 18 |

- **E.** RG32r y P32 eligen la comida el 100 % en los tres escalones; S32, el 95 % (5 % ninguna). RG032r y S032 eligen la comida el 20 % (80 % ninguna). Ninguna clase llega a casa en los 44 turnos.
- **F.** RG32r, S32 y P32: casa 75 %, hermana 25 %. RG032r y S032: casa 75 %, comida 25 %.

**Punto de cambio** (media; 4 = no acepta en ningún escalón):

| clase | A | B | C | E |
|---|---|---|---|---|
| RG32r | 4 | 4 | 1 | 1 |
| S32 | 4 | 4 | 1 | 1,15 |
| P32 | 4 | 4 | 1 | 1 |
| RG032r | 4 | 4 | 1 | 3,4 |
| S032 | 4 | 4 | 1 | 3,4 |

**Lo que hacen en los 44 turnos y cómo están a los 44 turnos y al final del día:** están las tablas completas en la evaluación (mover, quedarse, coger, comer, dejar, dar, dormir; llamadas de ella, de la hermana y de la vecina; viva, hambre, vida, hermana viva, despensa y bolsa). Algunos números:
- **B, la hermana.** Llama 23–32 de los 44 turnos.
- **B, moribunda.** Al final del día la hermana sigue viva el 98 % con RG32r y el 92 % con S32.
- **F, vida a los 44 turnos.** P32 tiene 69,6 y las otras cuatro clases 80,7–80,9.
- **E, hambre al final del día.** RG32r, S32 y P32 tienen 44–46; RG032r y S032, 2–3.

**Sus decisiones de los 44 turnos frente a cada valorador en el mismo estado** (% igual):

| escena | RG32r con las sumas | RG32r con la posición | RG032r con las sumas |
|---|---|---|---|
| A | 79.3 | 95.8 | 95.3 |
| B | 63.0 | 87.0 | 95.1 |
| C | 74.2 | 86.8 | 89.6 |
| D | 88.8 | 96.4 | 82.3 |
| E | 93.2 | 100.0 | 98.3 |
| F | 89.4 | 87.9 | 96.0 |

## Gasto, comprobaciones y tiempo

- **Gasto:**
  - créditos de la plataforma: 0;
  - dólares de la consola de Anthropic: 0.
- **Comprobaciones:**
  - `motor/model.py` md5 `1e511978c251130e95169ebf8443efa1` (sin cambios);
  - el valle y las criaturas congeladas no cambian; las escenas solo ponen la situación de partida.
- **Tiempo:**
  - estimado: unas 6 h;
  - real: unas 1 h 35 min (las partidas, 1 h 01 min).
- **Commit:** local, sin push.

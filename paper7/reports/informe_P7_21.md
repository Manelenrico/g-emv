# P7-21 · Dónde mueren las que recuerdan, y el botiquín bajo golpes

*7-oct-2026. Coste: plataforma 0, consola 0. Solo lectura de los 640 diarios de los dos campos (P7-10 y P7-14b; 80 vidas por brazo y campo), posterior a los sellos;
no se ha jugado ni replicado nada. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar.
`analiza_P7_21.py` → `P7_21_vidas.json`; este informe lo escribe `escribe_informe_P7_21.py` desde ese archivo. En P7-10 el brazo ESPERANZA se llamaba SUELO.*

## Lo que sale, en corto

- **La pista de Ari no separa a las que recuerdan.** Todas mueren en el mismo sitio: en la cámara central o pegadas a ella, a unas 9 casillas de la caja más
  cercana. En las muertes antes del tic 12.000, APRENDE muere dentro de la cámara en 13 de 35 y BORRADO en 7 de 16; en el primer golpe de la pelea
  final, a 0 casillas de la cámara en la mediana las dos; en los 30 segundos anteriores, el 100 % del tiempo cerca de cajas o cámara, las dos. El motivo
  es el mundo: el anillo empieza a cerrarse en el tic 7.296 y empuja a todas hacia el centro, y «temprano» (antes del 11.000) ya es con el anillo cerrándose.
- **Lo que la llevó allí** (los 30 s antes del primer golpe) es sobre todo estar quieta (`noop`, 69 % de los tics en APRENDE); la curiosidad pesa algo más en la que recuerda
  (21 % frente a 14 % en BORRADO); ir a por el botiquín, 0 % en las dos.
- **El botiquín bajo golpes (APRENDE y BORRADO, los dos campos, 939 canales):** «me han golpeado en los 48 instantes anteriores» separa mejor que «dentro o fuera»:
  completan 82 de 97 (85 %) de los canales abiertos sin daño antes frente a 325 de 842 (39 %) con daño antes; dentro del círculo, 354 de 605 (59 %); fuera, 53 de 334 (16 %).
  Fuera del círculo casi todo lo corta el anillo (pega cada 24 instantes y el canal dura 48); dentro, lo corta el rival. Las dos cosas juntas: dentro y sin daño antes, el canal cura casi siempre.
- **El estado emocional al abrir** (añadido de Manel, sección 5): dentro del círculo, el dolor del cuerpo separa los canales que curan de los que corta el daño
  mejor que «golpeada en los 48 anteriores» (separación 0,69 frente a 0,59); fuera del círculo no separa nada. El diario no distingue alivio de atracción.
- **Sí, el cuerpo se mueve con el canal abierto sin que se corte:** de los 407 canales completados, 397 cambiaron de casilla mientras estaba abierto. Lo que dijo P7-1 (57 de 59) se confirma a lo grande.

## Sección 1 · Definiciones, puestas antes de contar

- **Cajas:** los 16 pedestales del mapa (`static_map.pedestals` del diario; están en un anillo a unas 16 casillas del centro). **Objeto a la vista:** cada entrada de `ve_items` del tic.
- **Cámara:** la fortaleza central (`mundo_leido`: 49 celdas en torno al centro (24, 24), un cuadrado de 7×7). Distancia a la cámara = distancia Chebyshev al centro menos 3; 0 dentro.
- **Cerca de cajas o cámara:** a 3 casillas o menos de un pedestal o a 3 o menos de la cámara.
- **Muerte temprana:** antes del tic 11.000 y, aparte, del 12.000. **Primer golpe de la pelea final:** el de P7-20.
- **Qué la llevó allí:** lo elegido (`RADIOGRAFIA.elegido`) en los 720 tics anteriores al primer golpe, en partes. `ir_objeto` se separa en «a por el botiquín» y «a por otro objeto» por el objeto a la vista más cercano al que el paso elegido acerca: es una aproximación, porque el diario no guarda a qué objeto va el candidato.
- **Canal:** tics seguidos con `channeling` del botiquín en `effects`. **Se completa** si al cerrarse lleva un botiquín menos. Si no, **lo corta** el daño de rival o del anillo si lo hubo en el tic del cierre o en el anterior; si no, «sin daño registrado». **Dentro del círculo:** distancia euclídea al centro de la zona ≤ su radio al abrir. **Golpeada antes:** algún daño en los 48 tics anteriores a la apertura (y, aparte, en los 24). **Se movió:** cambió de casilla con el canal abierto.

## Sección 2 · Dónde mueren (la pista de Ari)

Distancias en casillas, medianas. «Cerca» = a 3 o menos de cajas o cámara.

**Muertes antes del tic 11.000**

| campo | brazo | muertes | en la muerte: a la caja más cercana | a la cámara | al objeto a la vista más cercano (n) | dentro de la cámara | cerca de cajas o cámara | en el primer golpe (n): a la caja | a la cámara | cerca | tics cerca en los 30 s antes de morir | antes del golpe |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 4 | 9,5 | 0,0 | 2,5 (4) | 3 de 4 | 4 de 4 | (4) 10,0 | 0,5 | 4 de 4 | 100 % | 100 % |
| P7-10 | BORRADO | 3 | 9,0 | 0,0 | 3,0 (3) | 2 de 3 | 3 de 3 | (3) 9,0 | 2,0 | 3 de 3 | 92 % | 89 % |
| P7-10 | APRENDE | 10 | 10,0 | 0,0 | 1,5 (10) | 6 de 10 | 10 de 10 | (10) 10,0 | 0,0 | 10 de 10 | 100 % | 100 % |
| P7-10 | TECHO | 5 | 7,0 | 2,0 | 2,0 (5) | 1 de 5 | 4 de 5 | (4) 9,0 | 1,0 | 3 de 4 | 94 % | 99 % |
| P7-14b | ESPERANZA | 11 | 8,0 | 4,0 | 1,0 (11) | 3 de 11 | 6 de 11 | (7) 10,0 | 1,0 | 6 de 7 | 68 % | 80 % |
| P7-14b | BORRADO | 4 | 9,0 | 0,0 | 2,0 (4) | 4 de 4 | 4 de 4 | (4) 9,5 | 0,0 | 4 de 4 | 89 % | 86 % |
| P7-14b | APRENDE | 10 | 9,0 | 1,5 | 2,5 (8) | 3 de 10 | 10 de 10 | (8) 10,0 | 1,5 | 7 de 8 | 83 % | 50 % |
| P7-14b | TECHO | 8 | 10,0 | 0,5 | 2,0 (8) | 4 de 8 | 8 de 8 | (8) 10,0 | 0,0 | 8 de 8 | 100 % | 100 % |
| los dos | ESPERANZA | 15 | 9,0 | 1,0 | 1,0 (15) | 6 de 15 | 10 de 15 | (11) 10,0 | 1,0 | 10 de 11 | 71 % | 100 % |
| los dos | BORRADO | 7 | 9,0 | 0,0 | 2,0 (7) | 6 de 7 | 7 de 7 | (7) 9,0 | 0,0 | 7 de 7 | 92 % | 89 % |
| los dos | APRENDE | 20 | 9,5 | 1,0 | 2,0 (18) | 9 de 20 | 20 de 20 | (18) 10,0 | 1,0 | 17 de 18 | 100 % | 100 % |
| los dos | TECHO | 13 | 10,0 | 1,0 | 2,0 (13) | 5 de 13 | 12 de 13 | (12) 10,0 | 0,0 | 11 de 12 | 100 % | 100 % |

**Muertes antes del tic 12.000**

| campo | brazo | muertes | en la muerte: a la caja más cercana | a la cámara | al objeto a la vista más cercano (n) | dentro de la cámara | cerca de cajas o cámara | en el primer golpe (n): a la caja | a la cámara | cerca | tics cerca en los 30 s antes de morir | antes del golpe |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 10 | 9,0 | 1,5 | 2,5 (10) | 4 de 10 | 6 de 10 | (6) 11,0 | 0,5 | 6 de 6 | 88 % | 100 % |
| P7-10 | BORRADO | 9 | 9,0 | 1,0 | 2,0 (9) | 3 de 9 | 6 de 9 | (6) 9,5 | 1,5 | 6 de 6 | 92 % | 97 % |
| P7-10 | APRENDE | 19 | 10,0 | 1,0 | 2,0 (19) | 9 de 19 | 14 de 19 | (16) 10,0 | 0,0 | 16 de 16 | 98 % | 100 % |
| P7-10 | TECHO | 6 | 6,0 | 4,0 | 1,5 (6) | 1 de 6 | 5 de 6 | (4) 9,0 | 1,0 | 3 de 4 | 86 % | 99 % |
| P7-14b | ESPERANZA | 18 | 8,0 | 4,0 | 1,0 (18) | 5 de 18 | 8 de 18 | (10) 10,0 | 1,5 | 7 de 10 | 58 % | 74 % |
| P7-14b | BORRADO | 7 | 9,0 | 0,0 | 2,0 (7) | 4 de 7 | 6 de 7 | (6) 10,0 | 0,0 | 6 de 6 | 78 % | 100 % |
| P7-14b | APRENDE | 16 | 9,0 | 2,5 | 2,0 (13) | 4 de 16 | 12 de 16 | (11) 10,0 | 2,0 | 10 de 11 | 77 % | 56 % |
| P7-14b | TECHO | 10 | 9,5 | 1,0 | 2,0 (10) | 4 de 10 | 9 de 10 | (10) 10,0 | 0,0 | 10 de 10 | 99 % | 100 % |
| los dos | ESPERANZA | 28 | 8,0 | 4,0 | 2,0 (28) | 9 de 28 | 14 de 28 | (16) 10,0 | 1,0 | 13 de 16 | 66 % | 100 % |
| los dos | BORRADO | 16 | 9,0 | 1,0 | 2,0 (16) | 7 de 16 | 12 de 16 | (12) 10,0 | 1,0 | 12 de 12 | 78 % | 100 % |
| los dos | APRENDE | 35 | 9,0 | 1,0 | 2,0 (32) | 13 de 35 | 26 de 35 | (27) 10,0 | 0,0 | 26 de 27 | 94 % | 100 % |
| los dos | TECHO | 16 | 9,0 | 2,0 | 2,0 (16) | 5 de 16 | 14 de 16 | (14) 10,0 | 0,0 | 13 de 14 | 96 % | 100 % |

**Todas las muertes**

| campo | brazo | muertes | en la muerte: a la caja más cercana | a la cámara | al objeto a la vista más cercano (n) | dentro de la cámara | cerca de cajas o cámara | en el primer golpe (n): a la caja | a la cámara | cerca | tics cerca en los 30 s antes de morir | antes del golpe |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 55 | 9,0 | 2,0 | 2,0 (55) | 15 de 55 | 39 de 55 | (26) 11,0 | 0,0 | 26 de 26 | 100 % | 100 % |
| P7-10 | BORRADO | 54 | 10,0 | 1,0 | 2,0 (52) | 24 de 54 | 40 de 54 | (32) 11,0 | 0,0 | 32 de 32 | 100 % | 100 % |
| P7-10 | APRENDE | 64 | 10,0 | 0,0 | 2,0 (64) | 34 de 64 | 51 de 64 | (43) 11,0 | 0,0 | 43 de 43 | 100 % | 100 % |
| P7-10 | TECHO | 55 | 9,0 | 2,0 | 1,0 (54) | 18 de 55 | 42 de 55 | (25) 11,0 | 0,0 | 24 de 25 | 100 % | 100 % |
| P7-14b | ESPERANZA | 57 | 10,0 | 1,0 | 2,0 (56) | 23 de 57 | 41 de 57 | (30) 10,0 | 0,0 | 27 de 30 | 100 % | 100 % |
| P7-14b | BORRADO | 49 | 9,0 | 2,0 | 2,0 (49) | 16 de 49 | 37 de 49 | (22) 10,5 | 0,0 | 22 de 22 | 100 % | 100 % |
| P7-14b | APRENDE | 58 | 9,0 | 2,0 | 2,0 (54) | 20 de 58 | 43 de 58 | (30) 10,5 | 0,0 | 29 de 30 | 100 % | 100 % |
| P7-14b | TECHO | 56 | 10,0 | 1,5 | 2,0 (56) | 21 de 56 | 47 de 56 | (30) 10,5 | 0,0 | 30 de 30 | 100 % | 100 % |
| los dos | ESPERANZA | 112 | 9,0 | 2,0 | 2,0 (111) | 38 de 112 | 80 de 112 | (56) 11,0 | 0,0 | 53 de 56 | 100 % | 100 % |
| los dos | BORRADO | 103 | 9,0 | 2,0 | 2,0 (101) | 40 de 103 | 77 de 103 | (54) 11,0 | 0,0 | 54 de 54 | 100 % | 100 % |
| los dos | APRENDE | 122 | 10,0 | 1,0 | 2,0 (118) | 54 de 122 | 94 de 122 | (73) 11,0 | 0,0 | 72 de 73 | 100 % | 100 % |
| los dos | TECHO | 111 | 9,0 | 2,0 | 2,0 (110) | 39 de 111 | 89 de 111 | (55) 11,0 | 0,0 | 54 de 55 | 100 % | 100 % |

Lectura: en todos los brazos y los dos campos la muerte es en la cámara o a su lado (mediana 0 a 2 casillas), lejos de las cajas (9 a 11). No hay un sitio distinto
para APRENDE. El objeto a la vista más cercano está a 2 casillas en todos: el centro guarda objetos y es donde el anillo junta a todas.

**APRENDE frente a BORRADO, emparejadas por semilla** (misma serie, día y asiento; la semilla fija el mapa, no lo que hacen los rivales):

Antes del tic 11.000:

| campo | las dos viven | APRENDE muere, BORRADO vive | APRENDE vive, BORRADO muere | las dos mueren (distancia a la cámara de A y de B) |
|---|---:|---:|---:|---|
| P7-10 | 67 | 10 | 3 | 0  |
| P7-14b | 70 | 6 | 0 | 4 (1, 0) (0, 0) (1, 0) (3, 0) |
| los dos | 137 | 16 | 3 | 4 (1, 0) (0, 0) (1, 0) (3, 0) |

Antes del tic 12.000:

| campo | las dos viven | APRENDE muere, BORRADO vive | APRENDE vive, BORRADO muere | las dos mueren (distancia a la cámara de A y de B) |
|---|---:|---:|---:|---|
| P7-10 | 54 | 17 | 7 | 2 (8, 7) (0, 1) |
| P7-14b | 62 | 11 | 2 | 5 (1, 0) (0, 0) (1, 0) (7, 14) (3, 0) |
| los dos | 116 | 28 | 9 | 7 (8, 7) (0, 1) (1, 0) (0, 0) (1, 0) (7, 14) (3, 0) |

Las pocas parejas en que mueren las dos lo hacen a la misma distancia de la cámara, salvo una (7 y 14, en P7-14b). Lo que separa a los brazos es cuántas mueren, no dónde.

**Qué la llevó allí** (parte de los 720 tics antes del primer golpe de la pelea final, media por muerte; antes del tic 12.000, los dos campos):

| brazo (los dos campos) | muertes con pelea final | `noop` | `ir_curioso` | `ir_objeto` (otro objeto) | `ir_objeto` (botiquín) | `ir_centro` | `ir_pareja` | `ir_botin` | paso | atacar | último `ir_*` antes del golpe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ESPERANZA | 16 | 89 % | 0 % | 2 % | 1 % | 1 % | 1 % | 1 % | 5 % | 0 % | ir_objeto (otro) 8, ir_centro 3, ninguno 2, ir_pareja 2, ir_objeto (botiquin) 1 |
| BORRADO | 12 | 77 % | 14 % | 3 % | 0 % | 0 % | 0 % | 1 % | 4 % | 0 % | ir_objeto (otro) 7, ir_curioso 2, ir_pareja 2, ninguno 1 |
| APRENDE | 27 | 69 % | 21 % | 3 % | 0 % | 1 % | 1 % | 1 % | 4 % | 0 % | ir_objeto (otro) 9, ir_pareja 6, ir_centro 5, ir_curioso 5, ninguno 1, ir_botin 1 |
| TECHO | 14 | 87 % | 0 % | 2 % | 0 % | 0 % | 1 % | 0 % | 9 % | 0 % | ir_objeto (otro) 7, ir_centro 3, ir_objeto (botiquin) 2, ninguno 1, ir_botin 1 |

Antes del 11.000:

| brazo (los dos campos) | muertes con pelea final | `noop` | `ir_curioso` | `ir_objeto` (otro objeto) | `ir_objeto` (botiquín) | `ir_centro` | `ir_pareja` | `ir_botin` | paso | atacar | último `ir_*` antes del golpe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ESPERANZA | 11 | 90 % | 0 % | 2 % | 0 % | 1 % | 1 % | 1 % | 5 % | 0 % | ir_objeto (otro) 5, ninguno 2, ir_pareja 2, ir_centro 2 |
| BORRADO | 7 | 67 % | 24 % | 3 % | 0 % | 1 % | 1 % | 2 % | 2 % | 0 % | ir_objeto (otro) 3, ir_curioso 2, ir_pareja 2 |
| APRENDE | 18 | 69 % | 23 % | 3 % | 0 % | 1 % | 1 % | 1 % | 3 % | 0 % | ir_objeto (otro) 7, ir_curioso 4, ir_pareja 3, ir_centro 2, ninguno 1, ir_botin 1 |
| TECHO | 12 | 86 % | 0 % | 2 % | 0 % | 0 % | 1 % | 0 % | 10 % | 0 % | ir_objeto (otro) 7, ir_centro 2, ir_objeto (botiquin) 1, ninguno 1, ir_botin 1 |

## Sección 3 · El botiquín bajo golpes

APRENDE y BORRADO, los dos campos juntos (939 canales: APRENDE 467, BORRADO 472).

**Ventana de 48 instantes antes de abrir**

| situación | canales | se completan | los corta el daño de un rival | el daño del anillo | muere con el canal abierto | se cortan sin daño registrado |
|---|---:|---:|---:|---:|---:|---:|
| dentro del círculo, golpeada antes | 512 | 274 (54 %) | 155 | 53 | 8 | 22 |
| dentro del círculo, sin daño antes | 93 | 80 (86 %) | 5 | 4 | 1 | 3 |
| fuera del círculo, golpeada antes | 330 | 51 (15 %) | 5 | 252 | 20 | 2 |
| fuera del círculo, sin daño antes | 4 | 2 (50 %) | 0 | 2 | 0 | 0 |

**Ventana de 24 instantes**

| situación | canales | se completan | los corta el daño de un rival | el daño del anillo | muere con el canal abierto | se cortan sin daño registrado |
|---|---:|---:|---:|---:|---:|---:|
| dentro del círculo, golpeada antes | 406 | 196 (48 %) | 141 | 39 | 8 | 22 |
| dentro del círculo, sin daño antes | 199 | 158 (79 %) | 19 | 18 | 1 | 3 |
| fuera del círculo, golpeada antes | 317 | 46 (15 %) | 5 | 245 | 20 | 1 |
| fuera del círculo, sin daño antes | 17 | 7 (41 %) | 0 | 9 | 0 | 1 |

**Cada factor por separado:** dentro del círculo completan 354 de 605 (59 %), fuera 53 de 334 (16 %); sin daño en los 48 anteriores 82 de 97 (85 %), con daño 325 de 842 (39 %);
con la ventana de 24: sin daño 165 de 216 (76 %), con daño 242 de 723 (33 %). **«Me están golpeando» separa más que «dentro o fuera»** (46 puntos
contra 43 de diferencia entre sus dos valores con la ventana de 48), pero los dos factores van juntos: fuera del círculo casi siempre hay daño antes (el anillo), y ahí
el anillo corta casi todo porque pega cada 24 instantes y el canal dura 48. La celda buena es «dentro y sin daño antes».

**Por brazo y campo** (ventana de 48):

*APRENDE, P7-10*

| situación | canales | se completan | los corta el daño de un rival | el daño del anillo | muere con el canal abierto | se cortan sin daño registrado |
|---|---:|---:|---:|---:|---:|---:|
| dentro del círculo, golpeada antes | 146 | 62 (42 %) | 61 | 19 | 3 | 1 |
| dentro del círculo, sin daño antes | 30 | 26 (87 %) | 3 | 1 | 0 | 0 |
| fuera del círculo, golpeada antes | 88 | 10 (11 %) | 0 | 74 | 3 | 1 |
| fuera del círculo, sin daño antes | 0 | 0 (— %) | 0 | 0 | 0 | 0 |

*APRENDE, P7-14b*

| situación | canales | se completan | los corta el daño de un rival | el daño del anillo | muere con el canal abierto | se cortan sin daño registrado |
|---|---:|---:|---:|---:|---:|---:|
| dentro del círculo, golpeada antes | 115 | 61 (53 %) | 29 | 10 | 2 | 13 |
| dentro del círculo, sin daño antes | 17 | 14 (82 %) | 0 | 2 | 1 | 0 |
| fuera del círculo, golpeada antes | 70 | 10 (14 %) | 2 | 49 | 9 | 0 |
| fuera del círculo, sin daño antes | 1 | 1 (100 %) | 0 | 0 | 0 | 0 |

*BORRADO, P7-10*

| situación | canales | se completan | los corta el daño de un rival | el daño del anillo | muere con el canal abierto | se cortan sin daño registrado |
|---|---:|---:|---:|---:|---:|---:|
| dentro del círculo, golpeada antes | 113 | 66 (58 %) | 33 | 10 | 0 | 4 |
| dentro del círculo, sin daño antes | 26 | 23 (88 %) | 2 | 0 | 0 | 1 |
| fuera del círculo, golpeada antes | 61 | 10 (16 %) | 0 | 49 | 2 | 0 |
| fuera del círculo, sin daño antes | 1 | 1 (100 %) | 0 | 0 | 0 | 0 |

*BORRADO, P7-14b*

| situación | canales | se completan | los corta el daño de un rival | el daño del anillo | muere con el canal abierto | se cortan sin daño registrado |
|---|---:|---:|---:|---:|---:|---:|
| dentro del círculo, golpeada antes | 138 | 85 (62 %) | 32 | 14 | 3 | 4 |
| dentro del círculo, sin daño antes | 20 | 17 (85 %) | 0 | 1 | 0 | 2 |
| fuera del círculo, golpeada antes | 111 | 21 (19 %) | 3 | 80 | 6 | 1 |
| fuera del círculo, sin daño antes | 2 | 0 (0 %) | 0 | 2 | 0 | 0 |

**Los cortes.** Duración de los canales cortados (tics), los más frecuentes: 23 (84), 22 (52), 19 (37), 21 (32), 20 (32), 17 (28); los completados duran 48 (405 de 407; 2 con otra duración: se completan por llevar un botiquín menos, y un botiquín dado durante el canal cuenta igual).
Los 27 cortes «sin daño registrado» son cortes que el diario no explica (26 de ellos con movimiento, pero el movimiento no corta: sección 4).

## Sección 4 · Moverse con el canal abierto (para contestar a Ari)

De los 407 canales completados de APRENDE y BORRADO, **397 cambiaron de casilla** con el canal abierto y se completaron igual: moverse no corta el canal. Lo que lo corta es el daño:
de los 532 cortes, 476 tienen daño de rival o del anillo en el tic del cierre o el anterior, 29 son muertes con el canal abierto y 27 no tienen daño registrado.
Confirma lo que Ari dice del mundo (el canal dura 48 instantes y cualquier daño lo corta) y lo de P7-1 (57 de 59 completados se movieron).

## Sección 5 · El estado emocional del cuerpo al abrir el canal (añadido de Manel, 7-oct)

**Lo que el diario guarda por instante, y lo que no.** En cada tic, `RADIOGRAFIA.ahora.filas` trae cada fila activa de la tabla con su magnitud, su signo (`-`
dolor, `+` lo positivo) y su reparto en los tres dominios (F cuerpo, R recursos, S vínculo), y `d_ahora` trae la distancia total. **No distingue, dentro de
lo positivo, el alivio de la atracción:** solo hay un signo. Así que el mapa es: dolor por dominio (suma de las filas con `-`), positivo por dominio (suma
de las filas con `+`) y la distancia total, en el tic de apertura. `emocion_P7_21.py` → `P7_21_emocion.json` (939 canales de 939, todos con estado).

Se comparan los canales que se completan con los que corta el daño (de rival o del anillo; fuera quedan las muertes con el canal abierto y los cortes sin daño).
«Separación» es la probabilidad de que un canal cortado tenga la medida más alta que uno que cura (0,5 = no separa; 1 = separa del todo; por debajo de 0,5, al revés).

| medida al abrir | dentro: mediana si cura | dentro: mediana si lo corta el daño | dentro: separación | fuera: mediana si cura | fuera: mediana si lo corta | fuera: separación |
|---|---:|---:|---:|---:|---:|---:|
| canales | 354 curan | 217 cortados | | 53 curan | 259 cortados | |
| dolor del cuerpo (F) | 0,850 | 1,037 | 0,69 | 0,902 | 0,974 | 0,55 |
| dolor en recursos (R) | 0,472 | 0,532 | 0,60 | 0,509 | 0,564 | 0,56 |
| dolor en vínculo (S) | 0,429 | 0,502 | 0,63 | 0,409 | 0,458 | 0,49 |
| dolor total | 1,797 | 2,149 | 0,67 | 1,918 | 2,046 | 0,55 |
| positivo total | 0,240 | 0,240 | 0,52 | 0,161 | 0,129 | 0,40 |
| distancia total | 3,567 | 3,888 | 0,68 | 3,754 | 3,865 | 0,56 |
| vida al abrir | 81,000 | 70,000 | 0,36 | 73,000 | 64,000 | 0,40 |
| golpeada en los 48 anteriores | 1,000 | 1,000 | 0,59 | 1,000 | 1,000 | 0,52 |
| golpeada en los 24 anteriores | 1,000 | 1,000 | 0,64 | 1,000 | 1,000 | 0,55 |

**Lectura.** Dentro del círculo, **el dolor del cuerpo (F) al abrir separa los canales que curan de los que no mejor que «me han golpeado en los 48 anteriores»**
(0,69 frente a 0,59), y algo mejor que la ventana de 24 (0,64); el dolor total y la distancia total separan casi igual que el dolor del cuerpo; el dolor en
recursos y en vínculo, menos; lo positivo, nada. La vida al abrir va en el mismo sentido (los cortados abren con menos vida: 0,36, es decir, 0,64 a favor de la vida alta). Fuera del círculo no separa
nada, ni el estado ni los golpes: ahí corta el anillo. Entre las filas, las que están más veces encendidas al abrir en los cortados que en los que curan son
S-7-AGRESOR (70 % frente a 56 %) y S-DANO-PAREJA (44 % frente a 34 %): el rival al lado y el hermano herido.

Solo se describe; no se cambia nada del cuaderno. Si el cuerpo guardara el estado al abrir, lo que más valdría para prever el corte es el dolor del cuerpo, que ya
lleva dentro el daño reciente y la vida que queda; «golpeada hace poco» añade poco encima.

## Lo que esto dice y lo que no

- Dónde mueren no distingue a la que recuerda: el anillo las lleva a todas al centro. Si la curiosidad, la esperanza o las ganas la llevan antes a sitios peores, no se ve en el lugar de la muerte ni en el del primer golpe; se ve, como mucho, en que elige `ir_curioso` algo más en los 30 s previos.
- La condición de corte del canal es «daño en 48 instantes», y los diarios la cumplen; hoy el cuaderno no apunta los cortes sin gasto (decisión de la mesa). Si el cuerpo supiera que «golpeada en los últimos 48» casi siempre acaba en corte, sería un cambio de arquitectura: se propone, no se hace.
- Todo es posterior a los sellos; sin pruebas estadísticas.

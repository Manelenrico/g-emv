# P7-50 · El campo del capítulo 4 en dos mundos: plataforma (3 series) y local

*12/13-oct-2026. Sello `SELLO_P7_49.md` con el addendum P7-50 (commit `7f0d262`, antes de lanzar). `motor/model.py` = `1e511978c251130e95169ebf8443efa1`, intacto. Bolsa 1: 126 partidas pedidas = 126 créditos (120 válidas, 3 de ellas el humo, que pasó y cuenta: p95 9,9-12,5 ms; 6 apartadas); saldo **≈ 102 + recargas (estimación)** (no legible por la API; 228 el 12-oct 06:47 + recargas − 126). Bolsa 2: 0 $. Scripts: `lanza_P7_50.py`, `orquesta_P7_50.py`,
`equidad_P7_50.py` → `P7_50_equidad.json`, `analiza_P7_50.py` → `P7_50_sello.json`, `potencia_P7_49.py`, `escribe_informe_P7_50.py` (este informe; ninguna cifra a mano).*

## Mundo 1 · Plataforma (liga real, 3 series × 20 días × COMPARTE / SOLAS)

Pareja valiente (asiento 10, MIEDO 0,5) / prudente (11, MIEDO 1,5), ojos compartidos en los dos brazos; la única diferencia es compartir (mirando + canal + noche). Equidad, paradas
y tope como en P7-43e: 0 paradas duras, 9 vidas marcadas de 240, diferencia máxima del % sobre el tic entre brazos 0,03 puntos (no dudosa).

| brazo | vidas | % sobre el tic | % bloqueados sin cuerpo | ms mediana | p95 máx | marcadas |
|---|---:|---:|---:|---:|---:|---:|
| COMPARTE | 120 | 0,21 | 0,29 | 4,08 | 44,6 | 6 |
| SOLAS | 120 | 0,18 | 0,21 | 4,04 | 44,6 | 3 |

**Ruido** (de P7-45, usado en el sello): S1 sd 132 sobre media 363; S2 sd 1,20 sobre 2,84; S3 sd 0,018 sobre 0,228. Con 3 series solo S3 tiene potencia
(efecto mínimo 20 %); S1 y S2 solo saldrían con efectos del 89 % y 104 % (declarado en el addendum).

| | medida | COMPARTE (por serie) | SOLAS (por serie) | COMPARTE − SOLAS ± ee | dirección prevista | ≥ 3 ee | veredicto | sin marcadas |
|---|---|---|---|---|---|---|---|---|
| S1 | área bajo la curva del botiquín de la hermana que menos prueba (d1-20) | 632,7, 637,7, 795,6 · media 688,68 | 213,4, 642,6, 419,1 · media 425,05 | 263,63 ± 134,98 | sí | no | **NO PASA** | 226,61 ± 101,18 (no) |
| S2 | parecido entre hermanas (d11-20, 4 objetos) | 0,1, 0,1, 0,1 · media 0,10 | 7,1, 1,2, 4,0 · media 4,11 | -4,01 ± 1,71 | sí | no | **NO PASA** | -3,92 ± 1,75 (no) |
| S3 | fracción de pruebas a red + camuflaje | 0,2, 0,3, 0,2 · media 0,22 | 0,2, 0,2, 0,2 · media 0,23 | -0,01 ± 0,03 | sí | no | **NO PASA** | -0,01 ± 0,02 (no) |

La hermana que menos prueba por sí misma (decidida en SOLAS): serie 1: asiento 11 (prudente; pruebas en SOLAS 10: 83, 11: 54); serie 2: asiento 11 (prudente; pruebas en SOLAS 10: 75, 11: 66); serie 3: asiento 10 (valiente; pruebas en SOLAS 10: 69, 11: 93).

| serie · brazo | días válidos | pruebas valiente · prudente | recibidos: canal · noche · vistos (contagio) | puesto valiente · prudente | creencia botiquín d20 (10 · 11) | marcadas |
|---|---:|---|---|---|---|---:|
| s1 COMPARTE | 20 | 72 · 95 | 106 · 7 · 17 (2) | 5,25 · 4,45 | 40,9 · 40,9 | 2 |
| s1 SOLAS | 20 | 83 · 54 | 0 · 0 · 0 (0) | 4,10 · 3,80 | 43,5 · 12,1 | 0 |
| s2 COMPARTE | 20 | 66 · 74 | 89 · 9 · 15 (2) | 6,70 · 4,65 | 39,2 · 39,2 | 0 |
| s2 SOLAS | 20 | 75 · 66 | 0 · 0 · 0 (0) | 5,20 · 5,05 | 34,7 · 41,5 | 3 |
| s3 COMPARTE | 20 | 80 · 117 | 106 · 13 · 15 (3) | 3,80 · 4,30 | 45,8 · 45,8 | 4 |
| s3 SOLAS | 20 | 69 · 93 | 0 · 0 · 0 (0) | 3,95 · 4,95 | 43,1 · 39,4 | 0 |

**Rachas ≥ 72 tics que la regla v3b no quitó** (Manel, 12-oct), por brazo y hermana, en las 240 vidas válidas:

| brazo · hermana | vidas | rachas ≥ 72 tics no quitadas | de ellas, marcadas por v3b en la racha | empujes en rachas largas (tras la marca) | rachas cortas (< 72) | % bloqueados sin cuerpo (media) |
|---|---:|---:|---:|---|---:|---:|
| COMPARTE · valiente | 60 | 0 | 0 | 0 (0) | 50 | 0,03 |
| COMPARTE · prudente | 60 | 0 | 0 | 0 (0) | 10 | 0,01 |
| SOLAS · valiente | 60 | 0 | 0 | 0 (0) | 20 | 0,02 |
| SOLAS · prudente | 60 | 0 | 0 | 0 (0) | 32 | 0,01 |

En los intentos apartados: apartadas s3 d1 SOLAS a11: 1 racha(s) de 311 empujes ({'ir_pareja': 311}; marcada sí).

**Incidencias del día** (regla del addendum 2: un reintento, luego día perdido): 4 reintentos (s3 d1 SOLAS: guarda dura, bloqueos sin cuerpo; s2 d10 COMPARTE: pod del asiento 10 borrado por la plataforma; s1 d15 SOLAS: guarda dura, latencia; s2 d14 COMPARTE: guarda dura, latencia), 2 partidas apartadas (pedidas por otra orquesta con los cuadernos de un intento parado), 0 días perdidos. Partidas pedidas en total: 126 (120 válidas).

**Veredicto de la plataforma**: ninguna de S1-S3 pasa; S1 va en dirección prevista (264 ± 135), S2 prevista (-4,01 ± 1,71), S3 prevista (-0,005 ± 0,029).

### Comprobación de imágenes (Manel, 12-oct): con qué versión se jugó cada partida

| serie | brazo | día → versión de la imagen (gemv-p7-campo:vN) | pvid coincide con su imagen | cuadernos horneados (d > 1) |
|---|---|---|---|---|
| 1 | COMPARTE | d1:v472 d2:v474 d3:v475 d4:v481 d5:v490 d6:v496 d7:v502 d8:v508 d9:v514 d10:v520 d11:v526 d12:v532 d13:v538 d14:v544 d15:v550 d16:v556 d17:v562 d18:v570 d19:v576 d20:v582 | 20 de 20 | 19 de 19 |
| 1 | SOLAS | d1:v473 d2:v478 d3:v484 d4:v492 d5:v498 d6:v504 d7:v510 d8:v516 d9:v522 d10:v528 d11:v534 d12:v540 d13:v546 d14:v552 d15:v566 d16:v573 d17:v579 d18:v585 d19:v590 d20:v595 | 20 de 20 | 19 de 19 |
| 2 | COMPARTE | d1:v477 d2:v483 d3:v491 d4:v497 d5:v503 d6:v509 d7:v515 d8:v521 d9:v527 d10:v539 d11:v545 d12:v551 d13:v557 d14:v571 d15:v577 d16:v583 d17:v588 d18:v593 d19:v597 d20:v599 | 20 de 20 | 19 de 19 |
| 2 | SOLAS | d1:v480 d2:v493 d3:v499 d4:v505 d5:v511 d6:v517 d7:v523 d8:v529 d9:v535 d10:v541 d11:v547 d12:v553 d13:v559 d14:v565 d15:v572 d16:v578 d17:v584 d18:v589 d19:v594 d20:v598 | 20 de 20 | 19 de 19 |
| 3 | COMPARTE | d1:v476 d2:v482 d3:v489 d4:v495 d5:v501 d6:v507 d7:v513 d8:v519 d9:v525 d10:v531 d11:v537 d12:v543 d13:v549 d14:v555 d15:v561 d16:v567 d17:v574 d18:v580 d19:v586 d20:v591 | 20 de 20 | 19 de 19 |
| 3 | SOLAS | d1:v488 d2:v494 d3:v500 d4:v506 d5:v512 d6:v518 d7:v524 d8:v530 d9:v536 d10:v542 d11:v548 d12:v554 d13:v560 d14:v569 d15:v575 d16:v581 d17:v587 d18:v592 d19:v596 d20:v600 | 20 de 20 | 19 de 19 |

Piezas en los diarios (`P7_49_arranque_campo`): 2 listas distintas, que solo difieren en la etiqueta del brazo (`hermanas_P7_48:comparte` / `:solas`): efecto_P7_39, contrafactual_P7_38:B1, filo_P7_40, escala_P7_48, hermanas_P7_48:comparte, miedo_P7_49, rapido_P7_43 · efecto_P7_39, contrafactual_P7_38:B1, filo_P7_40, escala_P7_48, hermanas_P7_48:solas, miedo_P7_49, rapido_P7_43.
Mando de miedo en todos los diarios: MIEDO_V 0.5 / MIEDO_P 1.5 con 9 filas, 1 variante(s). Avisos (pvid pedido ≠ imagen, modo ≠ brazo, MIEDO ≠ 0,5/1,5, cuadernos sin hornear): ninguno.
Archivos que copia la imagen cambiados desde la primera subida del campo (2026-10-12T12:45:47): ninguno. La carrera de versiones del 12-oct (tres orquestas subiendo a la vez) solo pudo
fallar la aserción del lanzador (y falló una vez, sin pedir partida): ninguna partida se pidió con un pvid distinto del de su propia imagen.

## Mundo 2 · Local (coworld play en el Mac, 0 créditos)

Antes de jugar, el ruido local con las vidas de P7-48 (cadenas de 3 días, 8 parejas por brazo; 16 criaturas nuestras, todas mueren antes del final):

| brazo (P7-48, 3 días, 8 parejas) | S1 proxy (suma de 3 días de la creencia del botiquín de la que menos cree) media · sd | S2 proxy (d2-3) media · sd | S3 media · sd |
|---|---|---|---|
| comparte | 24,8 · 47,3 | 0,19 · 0,40 | 0,116 · 0,140 |
| solas | 0,0 · 0,0 | 5,16 · 4,32 | 0,066 · 0,059 |

Coeficiente de variación (las dos cadenas juntas): S1 2,81, S2 1,46, S3 1,18. Series locales necesarias para un 50 % a 3 ee, con 8 parejas por serie y brazo (n ≥ 18 × CV² / 0,25 / 8):
S1 71, S2 20, S3 13. Cada serie local = 40 partidas × (≈ 377 s de juego + ≈ 150 s de horneado) ≈ 5,9 h y ≈ 12 GB de diarios antes de comprimir: en 24 h caben 4 series.
**No jugada: sin potencia en 24 h ni disco** (decisión de Manel, 12-oct): las series con potencia (S1 71, S2 20) no caben frente a las 4 que entran en 24 h, y pedirían ≈ 240 GB de diarios antes de comprimir. En el mundo local, en 3 días casi ninguna pareja llega a creer en el botiquín (S1 en SOLAS: 0 en las 8 parejas):
las vidas son cortas y las pruebas escasas; el escalado a 20 días es una extrapolación declarada. Lo que cabe en 24 h (4 series, ≈ 40 h de CPU del Mac) no distinguiría ni un 100 %.

## Lectura

1. **Dirección y tamaño.** S1 y S2 van en la dirección prevista y lejos de los 3 errores típicos: la hermana que menos prueba cree 689 frente a 425 de área (+62 %, 2,0 ee); las
   hermanas que comparten acaban creyendo casi lo mismo (0,10 de diferencia media en d11-20 frente a 4,11; 2,3 ee): el canal y la noche pasan cada recuerdo vivido, así que los dos
   cuadernos convergen (creencia del botiquín al d20 idéntica en las tres parejas de COMPARTE). S3, la única con potencia, es nula: compartir no reduce las pruebas a red y
   camuflaje (22 % frente a 22 %): lo que la hermana cuenta del camuflaje («no hizo nada», importancia pequeña) pesa poco contra la ignorancia, como en P7-47.
2. **Vigilancia.** En COMPARTE la prudente prueba más que la valiente en las tres series (95 frente a 72, 74 frente a 66, 117 frente a 80); en SOLAS no hay orden fijo. Contagio de errores:
   7 de 377 recuerdos recibidos. Rachas ≥ 72 tics no quitadas por v3b: 0 en las 240 vidas válidas (la única fue la del intento apartado); las rachas cortas
   salen más en las valientes de COMPARTE (50) que en las prudentes (10): la sospecha de que el miedo a separarse escalado atasca a las prudentes no se ve.
3. **Lo que diría más series.** Con el ruido observado en este campo (S1 sd entre series 207), S1 a 3 ee pediría unas 12 series por brazo para este tamaño de efecto;
   S2, 10. Para la mesa.

## Línea final

Los dos mundos no se pueden comparar: el local no se jugó por falta de potencia. En la plataforma no pasa ninguna predicción.

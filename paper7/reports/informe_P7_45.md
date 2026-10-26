# P7-45 · El campo del capítulo 3 entero: tres series, el sello evaluado

*12-oct-2026. Bolsa 1 (créditos de experiencia, 1 por partida): el campo 360 (serie 1: 120, serie 2: 120, serie 3: 120) + humo 3 + fuera de resultados 112
(piloto 1 95, piloto 2 13, humo que murió al arrancar 3, intento parado de APRENDE_p d20 1) = 475 créditos del campo. Acumulado del siete: 710 + 475 = **1185**.
Disponibles: **228** (saldo real de la página de la plataforma, 12-oct 06:47, dato de Manel; la estimación de ≈ 163 que llevaba este informe se corrige). Bolsa 2 (consola de Anthropic): 0 $.
Disco: la serie 1 ocupa 9,54 GB, la 2 9,17 GB, la 3 9,04 GB (diarios y zips); libre 10,0 GB tras archivar en el T7 P7-30, P7-34 y los pilotos (478 diarios borrados tras
copia leída de vuelta; `P7_43_borrado.json`). `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Sello `SELLO_P7_42.md` (commit `a481226`) con sus addenda 1-12, sin reescribir.
Piezas: `rapido_P7_43.py` = `0ec5f59cba0ff99e16e917ef86c3421b`, `filo_P7_40.py` = `1fefeef2071af1f2adaf9ab116d0254f`, `azar_P7_41.py` = `b4ef6a1a93e2c1c5b143043b3928e6e2`, `campo_P7_41.py` = `2146861db7a18d24990a016632fc74ab`.
Scripts: `orquesta_P7_43.py`, `equidad_P7_43.py` → `P7_43_equidad*.json`, `analiza_P7_42.py` → `P7_42_datos.json`, `sello_P7_42.py` → `P7_42_sello.json`, `latencia_P7_43.py` + `latencia_P7_45.py` → `P7_45_latencia.json/.png`,
`escribe_informe_P7_45.py` (este informe; ninguna cifra a mano).*

## Sección 1 · El campo tal como se jugó

Tres series × 20 días × 6 variantes = 360 partidas (720 vidas), imágenes v3b (cachés con decisiones idénticas y regla del cuerpo de los 72 tics), tope de 12 partidas a la vez con subida
a 20 solo si el día 1 de los seis brazos cumple (p95 < 20 ms y < 1 % sobre el tic), semillas k 221-240 (serie 1 en orden, 2 inversa, 3 rotada). Serie 1 el 11-oct de 10:46 a 16:15 (con
el reintento de APRENDE_p d20, addendum 12); serie 2 el 11-oct de 17:01 a 22:17; serie 3 del 11 al 12-oct, de 22:31 a 04:07 (el día 1 no cumplió: un p95 de 28,4 ms;
siguió en 12 toda la serie). Ninguna petición rechazada por la plataforma. Regla de comparación (addendum 12): solo días válidos en todos los brazos → los 20 días de las tres series son válidos en los 6 brazos.

| serie | partidas | tope | diferencia máx. del % sobre el tic entre brazos (puntos) | extremos | paradas duras | vidas marcadas |
|---|---:|---|---:|---|---:|---:|
| 1 | 120 | 12 → 20 a las 11:57:53 | 0,34 | BORRADO_p / TECHO | 0 | 8 |
| 2 | 120 | 12 → 20 a las 18:20:11 | 0,09 | APRENDE_p / APRENDE_v | 0 | 2 |
| 3 | 120 | 12 → 12 a las 00:10:40 | 0,63 | APRENDE_p / TECHO | 0 | 6 |
| las tres | 360 | | 0,33 | APRENDE_p / TECHO | 0 | 16 |

| brazo | vidas | % decisiones sobre el tic (media) | % pasos listos bloqueados sin cuerpo (media) | ms por decisión (mediana) | p95 máximo (ms) | marcadas |
|---|---:|---:|---:|---:|---:|---:|
| TECHO | 120 | 0,02 | 0,36 | 1,17 | 20,5 | 0 |
| BORRADO valiente | 120 | 0,06 | 0,24 | 3,22 | 36,0 | 1 |
| BORRADO prudente | 120 | 0,19 | 0,13 | 2,92 | 42,5 | 6 |
| APRENDE valiente | 120 | 0,05 | 0,25 | 3,41 | 32,3 | 2 |
| APRENDE prudente | 120 | 0,35 | 0,26 | 3,52 | 50,7 | 7 |
| SIN EMOCIÓN | 120 | 0,04 | 0,41 | 2,04 | 29,2 | 0 |

Paradas duras: 0 en las 360 partidas (la única del campo fue el primer intento de APRENDE_p s1 d20, fuera de resultados, addendum 12). Vidas marcadas por la guarda (segunda
cuenta del sello): 16 de 720: s1 d17 BORRADO_v a10; s1 d4 BORRADO_p a10; s1 d5 BORRADO_p a10; s1 d10 BORRADO_p a11; s1 d11 BORRADO_p a11; s2 d18 BORRADO_p a11; s3 d11 BORRADO_p a10; s1 d8 APRENDE_v a10; s3 d2 APRENDE_v a10; s1 d4 APRENDE_p a11; s1 d19 APRENDE_p a10; s2 d18 APRENDE_p a10; s3 d11 APRENDE_p a10; s3 d15 APRENDE_p a10; s3 d17 APRENDE_p a11; s3 d18 APRENDE_p a11. Equidad: la diferencia máxima del % sobre el tic entre brazos es 0,33 puntos en el total
y 0,34, 0,09, 0,63 por serie: ninguna dudosa (umbral 2).

## Sección 2 · El sello evaluado (6 criaturas por cadena; BORRADO fuera de la comparación de rapidez)

Decisión de la mesa (Manel, 11-oct): BORRADO no entra en la comparación de rapidez porque su cuaderno se vacía cada noche y lo que aprende un día lo pierde; la rapidez se compara entre
APRENDE y SIN EMOCIÓN (como ya decía el sello: R1 solo enfrenta APRENDE_p y APRENDE_v a SIN) y BORRADO queda como referencia de lo que se aprende dentro de un día (sección 3).

**Cuenta con todas las vidas.** R1 (APRENDE llega antes que SIN con el botiquín; días): APRENDE_p − SIN -3,3 ± 4,2, cumple; APRENDE_v − SIN 0,3 ± 3,2, NO cumple → **R1 NO PASA**. C1 (usos del botiquín con hp < 50, proporción): APRENDE_p − SIN -0,026 ± 0,065, NO cumple; APRENDE_v − SIN -0,037 ± 0,064, NO cumple → **C1 NO PASA**.

**Cuenta sin las 16 partidas marcadas.** R1 (APRENDE llega antes que SIN con el botiquín; días): APRENDE_p − SIN -3,3 ± 4,2, cumple; APRENDE_v − SIN 0,3 ± 3,2, NO cumple → **R1 NO PASA**. C1 (usos del botiquín con hp < 50, proporción): APRENDE_p − SIN -0,000 ± 0,067, NO cumple; APRENDE_v − SIN -0,029 ± 0,064, NO cumple → **C1 NO PASA**.

S1 (sabiduría, sin predicción): segundos en red o camuflaje en los días 11-20 por vida: TECHO 273,5 s (vida perdida 65,8), BORRADO valiente 340,9 s (vida perdida 68,2), BORRADO prudente 312,9 s (vida perdida 62,0), APRENDE valiente 259,5 s (vida perdida 58,4), APRENDE prudente 364,3 s (vida perdida 80,3), SIN EMOCIÓN 204,1 s (vida perdida 53,7).
Carácter (puesto valiente − prudente, menor = mejor): APRENDE 0,87 ± 0,49, BORRADO 0,03 ± 0,50.

| variante | vidas | puesto ± ee | rapidez botiquín, por criatura (días; 21 = no llega) · media ± ee | rapidez ración · media | cuándo botiquín (hp < 50 / usos) · ración (hp < 100 / usos) | sabiduría d11-20: s en red · s en camuflaje · vida perdida (las dos) | pruebas (b · r · red · cam) · forzadas | mueren |
|---|---:|---|---|---|---|---|---|---:|
| TECHO | 120 | 4,82 ± 0,32 | (referencia, sección 3) | (referencia) | 0 / 0 (0 %) · 0 / 0 | 212,3 · 156,3 · 65,8 | 0 (0 · 0 · 0 · 0) · 0 | 92 |
| BORRADO valiente | 120 | 4,28 ± 0,34 | (referencia, sección 3) | (referencia) | 38 / 202 (19 %) · 115 / 115 | 222,8 · 245,2 · 68,2 | 408 (195 · 111 · 51 · 51) · 0 | 63 |
| BORRADO prudente | 120 | 4,24 ± 0,37 | (referencia, sección 3) | (referencia) | 33 / 188 (18 %) · 144 / 144 | 207,7 · 251,0 · 62,0 | 422 (180 · 141 · 50 · 51) · 0 | 61 |
| APRENDE valiente | 120 | 5,08 ± 0,39 | 13, 10, 21, 21, 21, 18 · 17,3 ± 1,9 | 2, 3, 1, 2, 4, 4 · 2,7 | 48 / 202 (24 %) · 124 / 124 | 195,6 · 167,2 · 58,4 | 411 (193 · 122 · 45 · 51) · 0 | 78 |
| APRENDE prudente | 120 | 4,22 ± 0,29 | 21, 21, 21, 4, 6, 9 · 13,7 ± 3,3 | 2, 11, 7, 2, 3, 9 · 5,7 | 44 / 177 (25 %) · 183 / 184 | 214,8 · 221,2 · 80,3 | 449 (170 · 180 · 49 · 50) · 0 | 75 |
| SIN EMOCIÓN | 120 | 5,42 ± 0,39 | 21, 7, 21, 21, 11, 21 · 17,0 ± 2,6 | 11, 2, 17, 2, 21, 12 · 10,8 | 17 / 62 (27 %) · 99 / 99 | 111,9 · 118,0 · 53,7 | 202 (58 · 93 · 31 · 20) · 349 | 82 |

| cadena | criatura (serie · asiento) | creencia del botiquín al cerrar el d20 (máximo del recorrido) | creencia de la ración al d20 |
|---|---|---|---|
| APRENDE valiente | s1 · a10 | 26,2 (31,4) | 12,9 |
| APRENDE valiente | s1 · a11 | 31,6 (36,5) | 10,8 |
| APRENDE valiente | s2 · a10 | 24,1 (24,3) | 12,5 |
| APRENDE valiente | s2 · a11 | 17,8 (21,2) | 8,0 |
| APRENDE valiente | s3 · a10 | 12,6 (16,3) | 13,4 |
| APRENDE valiente | s3 · a11 | 31,5 (32,2) | 10,5 |
| APRENDE prudente | s1 · a10 | 22,4 (23,0) | 11,2 |
| APRENDE prudente | s1 · a11 | 18,7 (19,0) | 11,4 |
| APRENDE prudente | s2 · a10 | 10,9 (11,1) | 13,5 |
| APRENDE prudente | s2 · a11 | 25,1 (35,1) | 10,9 |
| APRENDE prudente | s3 · a10 | 36,9 (39,8) | 12,0 |
| APRENDE prudente | s3 · a11 | 36,7 (37,0) | 12,8 |
| SIN EMOCIÓN | s1 · a10 | 18,9 (18,9) | 13,3 |
| SIN EMOCIÓN | s1 · a11 | 38,7 (39,0) | 12,0 |
| SIN EMOCIÓN | s2 · a10 | — (0,0) | 7,1 |
| SIN EMOCIÓN | s2 · a11 | — (0,0) | 13,0 |
| SIN EMOCIÓN | s3 · a10 | 25,8 (36,8) | 5,4 |
| SIN EMOCIÓN | s3 · a11 | — (0,0) | 12,5 |

| variante | pruebas por vida y día, d1 → d20 |
|---|---|
| TECHO | 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 |
| BORRADO valiente | 2,5 3,0 3,3 2,7 4,5 3,3 3,0 3,0 3,0 3,8 3,2 3,8 2,7 2,8 3,0 6,5 3,8 2,8 4,5 2,7 |
| BORRADO prudente | 3,5 4,5 3,8 2,7 3,0 2,8 1,5 4,2 5,3 2,8 3,0 4,8 3,3 2,7 3,2 4,5 2,2 5,2 3,7 3,7 |
| APRENDE valiente | 3,2 2,8 4,0 2,5 4,8 2,8 3,3 2,7 4,3 3,5 3,2 2,8 5,3 4,7 2,8 3,7 2,0 4,7 1,7 3,7 |
| APRENDE prudente | 1,7 3,7 3,7 2,8 5,8 4,2 2,7 2,8 3,5 3,7 2,7 4,8 3,7 2,7 2,3 4,3 2,8 5,8 8,8 2,3 |
| SIN EMOCIÓN | 0,3 0,8 0,8 0,3 1,3 1,7 1,2 2,5 0,8 1,3 2,2 1,3 1,8 2,0 2,5 2,3 1,2 4,0 2,2 3,0 |

## Sección 3 · BORRADO (y TECHO) como referencia de lo que se aprende dentro de un día

Vidas cuya creencia al cerrar el día llega al 50 % del efecto real (botiquín 25 de 50; ración 7,5 de 15), con el cuaderno vacío al arrancar:
- BORRADO valiente: botiquín 10 de 120 vidas (s1 d2 a10, s1 d12 a11, s1 d17 a10, s1 d19 a10, s2 d5 a11, s2 d11 a10, s2 d14 a11, s2 d16 a10, s3 d7 a11, s3 d9 a10); ración 29 de 120.
- BORRADO prudente: botiquín 10 de 120 vidas (s2 d2 a10, s2 d4 a10, s2 d7 a10, s2 d8 a11, s2 d9 a11, s2 d10 a11, s2 d13 a11, s3 d3 a11, s3 d9 a10, s3 d11 a10); ración 28 de 120.
- TECHO: botiquín 0 de 120 vidas (ninguna); ración 0 de 120.
Lo que significa el «50 % el día 2» de un BORRADO: esa criatura usó el botiquín dentro de ese día lo bastante para que su creencia de cierre llegara a 25, y lo perdió al dormir; es un día
afortunado, no acumulación.

## Sección 4 · La curva de latencia de APRENDE prudente frente al cuaderno (tres series)

| cadena | n días | Spearman mediana ~ cuaderno (s1 · s2 · s3 · juntas) | Spearman % sobre el tic ~ cuaderno (juntas) | ms más por cada 100 apuntes (recta) | mediana media (ms) | % sobre el tic medio | días con ≥ 1 % |
|---|---:|---|---:|---:|---:|---:|---:|
| APRENDE prudente | 57 | 0,36 · 0,57 · 0,60 · **0,56** | 0,45 | 0,271 | 4,43 | 0,365 | 7 |
| APRENDE valiente | 57 | 0,13 · 0,14 · 0,36 · **0,17** | 0,07 | 0,053 | 3,81 | 0,047 | 0 |
| SIN EMOCIÓN | 57 | -0,10 · 0,27 · 0,23 · **0,04** | 0,12 | 0,047 | 2,33 | 0,037 | 0 |

El cuaderno de APRENDE prudente con el que arranca el d20 tiene 1.210, 1.466, 1.418 recuerdos + apuntes en las series 1, 2 y 3. Figura: `P7_45_latencia.png` (mediana de ms por día frente al
tamaño del cuaderno, tres series, tres cadenas; de `P7_43_latencia_s1-3.json`).

## Sección 5 · Apéndice: fuera de resultados

Piloto 1 (95 partidas, 63 a la vez, guarda dura), piloto 2 (13, regla v1), humo que murió al arrancar (3), humo bueno (3, APRENDE valiente desde el cuaderno del d13) y el primer
intento de APRENDE_p s1 d20 (1). Diarios: `P741p_*`, `P741q_*`, `P741x_*`, `P741r_*` (zips en el Mac y en el T7). Pendiente de P7-44: repetir la medida del camuflaje por brazo
(SIN EMOCIÓN y TECHO por separado) con los 720 diarios del campo.

## Lectura

1. **El sello no pasa.** R1: APRENDE prudente llega 3,3 días antes que SIN EMOCIÓN con el botiquín, pero el error típico es 4,2 días (menos de una vez el ruido); APRENDE valiente
   no llega antes (0,3 ± 3,2). C1: la proporción de usos del botiquín con hp < 50 es 25 % en APRENDE prudente, 24 % en APRENDE valiente y
   27 % en SIN: ninguna diferencia llega a un error típico. Ninguna medida del campo llega a 3 veces el ruido. Con 6 criaturas por cadena, APRENDE y SIN EMOCIÓN son
   indistinguibles en rapidez y en cuándo. La segunda cuenta (sin las 16 partidas marcadas) dice lo mismo.
2. **La rapidez es, sobre todo, ruido entre criaturas**: en APRENDE prudente, 3 criaturas no llegan a 25 en 20 días y las otras llegan los días 4, 6, 9; al cerrar el d20, 3 de 6 están en 25 o más
   (APRENDE valiente: 3 de 6). En SIN, 3 de las 6 criaturas acaban con creencia 0 del botiquín: en 20 días no llegaron a usarlo ni una vez (la moneda fuerza ir y coger, y el usar;
   pero el veto de lo desconocido hace que fuera de la moneda no lo use).
3. **SIN EMOCIÓN probó la mitad que APRENDE**: 1,7 pruebas por vida (349 forzadas en 120 vidas) frente a 3,4 y 3,7 de APRENDE y 3,4-3,5 de BORRADO. La calibración de ε en lazo
   abierto (±20 % de las pruebas de APRENDE, sello) no se ha cumplido en lazo cerrado: hay que decirlo al leer R1 y C1 (SIN empata probando la mitad). Causa probable: en la réplica
   los «momentos con objeto al alcance» eran casi todos los tics; en la partida real la criatura forzada a ir y coger no siempre llega (ventana de 240 tics) y las forzadas que no
   acaban en cogida no dejan huella de prueba. Se propone, no se ejecuta: contar las forzadas que acaban (cogida o usada) frente a las que caducan, con `P7_41_azar` (`fines`).
4. **Carácter**: APRENDE valiente queda 0,87 ± 0,49 puestos peor que el prudente (menos de dos errores típicos); en BORRADO no hay diferencia (0,03 ± 0,50).
   Mueren 78 de 120 vidas de APRENDE valiente, 75 del prudente, 82 de SIN y 92 de TECHO.
5. **Sabiduría (S1)**: SIN EMOCIÓN es la que menos tiempo pasa con la red y el camuflaje en los días 11-20 (204 s por vida) y APRENDE prudente la que más (364 s); TECHO, que no
   prueba nada, 274 s. La vida perdida en esos tics va de 54 a 80. Sin predicción sellada, se informa.
6. **Latencia**: APRENDE prudente es la única cadena cuya mediana sube con el cuaderno (Spearman 0,56 con 57 días; 0,27 ms más por cada 100 apuntes: de 86 a 1.365
   recuerdos + apuntes (medias del d2 y del d20) son ≈ 3,5 ms sobre una mediana media de 4,4); 7 de sus 57 días tienen ≥ 1 % de decisiones sobre el tic. Pero 13 de las 16 vidas marcadas son prudentes, y
   BORRADO prudente, con cuaderno vacío, tiene 6: la lentitud del prudente no es solo el cuaderno. La equidad se mantiene (≤ 0,63 puntos entre brazos).

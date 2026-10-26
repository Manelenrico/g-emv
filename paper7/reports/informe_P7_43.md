# P7-43 · La serie 1 del campo del capítulo 3: arreglos tras la parada de la guarda, pilotos y lo jugado

*11-oct-2026. Plataforma hoy: 139 créditos (3 de un humo que murió al arrancar, 3 del humo bueno, 13 del piloto 2, 120 de la serie 1); anoche, piloto 1: 95. Acumulado del siete:
710 + 95 + 139 = 944 créditos. Disponibles: los que diga la página de la plataforma (Manel). Consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Sello `SELLO_P7_42.md` con
sus addenda 1-11 (fechados, sin reescribir). Piezas de campo: `rapido_P7_43.py` = `0ec5f59cba0ff99e16e917ef86c3421b` (cachés y regla v3b), `filo_P7_40.py` = `1fefeef2071af1f2adaf9ab116d0254f`, `azar_P7_41.py` = `b4ef6a1a93e2c1c5b143043b3928e6e2`,
`campo_P7_41.py` = `2146861db7a18d24990a016632fc74ab`. Scripts: `orquesta_P7_43.py` (tope 12 → 20), `corre_P7_43.sh`, `equidad_P7_43.py` → `P7_43_equidad_s1.json`, `analiza_P7_42.py` → `P7_42_datos.json`,
`sello_P7_42.py` → `P7_42_sello.json`, `escribe_informe_P7_43.py` (este informe; ninguna cifra a mano).*

## Sección 1 · Qué pasó y qué se arregló (mesa P7-43 a 43e)

- **Piloto 1** (noche del 10 al 11, 95 partidas, 63 a la vez): la guarda dura paró las tres cadenas; 6 vidas con 10-30 % de decisiones sobre el tic o 5-86 % de pasos bloqueados sin
  cuerpo. Causas: latencia (factor plataforma/local de 1,8× a 10,7× en la misma noche: contención por nuestro propio paralelismo) y empujes contra casillas «libres»: vainas
  (`pod_*`, fijas) y **rivales camuflados** (`camo_glass`, invisibles para nosotros; P7-44).
- **Cachés con decisiones idénticas** (`rapido_P7_43`: la segunda tasación del regalo por tic y clave de foto; `filo_P7_40`: ignorancia y curiosidad por tic): 69431 decisiones en
  6 vidas del piloto, 0 distintas.
- **Regla del cuerpo de los 72 tics**, v3b: racha de empujes bloqueados hacia la misma casilla, sin moverse, por tiempo de reloj (el enfriamiento no la rompe); marca de 30 s
  renovable; se olvida al morir; los `ir_*` con destino en casilla no transitable (marcada o del agua) salen de la lista. Piloto 2 (13 partidas, regla v1) y el humo que murió al
  arrancar (3: el Dockerfile no copiaba la pieza; ahora la composición entera se comprueba al hornear) quedan fuera de resultados.
- **Humo bueno** (3 × APRENDE valiente desde el cuaderno del d13): medianas 1,9-4,2 ms, p95 7,1-13,8, 0 % sobre el tic; corte revisado por la mesa a p95 < 20 ms.
- **Serie 1** con v3b, tope de 12 partidas a la vez (cadenas primero), subido a 20 al cumplir el día 1 (11:57:53).

## Sección 2 · Equidad de la lentitud, paradas y créditos (serie 1)

| brazo | vidas | % decisiones sobre el tic (media) | % pasos listos bloqueados sin cuerpo (media) | ms por decisión (mediana) | p95 máximo (ms) | marcadas | paradas |
|---|---:|---:|---:|---:|---:|---:|---:|
| TECHO | 40 | 0,00 | 0,19 | 1,24 | 11,4 | 0 | 0 |
| BORRADO valiente | 40 | 0,08 | 0,21 | 3,30 | 36,0 | 1 | 0 |
| BORRADO prudente | 40 | 0,34 | 0,16 | 2,74 | 42,1 | 4 | 0 |
| APRENDE valiente | 40 | 0,05 | 0,24 | 3,47 | 30,2 | 1 | 0 |
| APRENDE prudente | 40 | 0,26 | 0,26 | 3,17 | 44,0 | 2 | 0 |
| SIN EMOCIÓN | 40 | 0,03 | 0,44 | 2,08 | 24,9 | 0 | 0 |

Diferencia máxima entre brazos del % sobre el tic: **0,34 puntos** (BORRADO_p frente a TECHO): no dudoso (≤ 2).
Paradas de la guarda dura (antes del reintento): 0 (ninguna). Vidas marcadas: 8 de 240.
Partidas de la serie 1: 120 de 120. Cierre (addendum 12): SIN d20 pedido después; APRENDE_p d20 jugado de nuevo UNA vez con el mismo cuaderno (d19) y tope 2: pasó la guarda
(medianas 3,7 y 3,4 ms frente a 11,1 y 10,9 del intento parado, mismo cuaderno: la lentitud era la escena —centro, 18 candidatos, hermana a la vista— y la hora, no el cuaderno;
el intento parado queda aparte, fuera de resultados). Curva de latencia por día y brazo: `P7_43_latencia_s1.json` (`latencia_P7_43.py`): las medianas de las cadenas van de 2 a 5 ms
del d2 al d18 mientras el cuaderno pasa de 3 a 50 recuerdos y de 80 a 1.100 apuntes (Spearman mediana-cuaderno: APRENDE_v 0,13, APRENDE_p 0,36, SIN −0,03); BORRADO, con
cuaderno vacío, tiene las mismas medianas y los mismos picos.

| brazo | % sobre el tic por día, d1 → d20 |
|---|---|
| TECHO | 0,0 0,1 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 |
| BORRADO valiente | 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 1,4 0,0 0,0 0,0 |
| BORRADO prudente | 0,0 0,0 0,0 1,5 1,4 0,1 0,0 0,0 0,0 2,7 0,7 0,0 0,0 0,0 0,0 0,0 0,3 0,0 0,1 0,0 |
| APRENDE valiente | 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,6 0,1 0,0 0,0 0,3 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 |
| APRENDE prudente | 0,0 0,0 0,0 3,2 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,2 0,0 0,3 1,4 0,0 |
| SIN EMOCIÓN | 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,3 0,2 0,0 |

## Sección 3 · Las medidas de la serie 1 (parcial: 2 criaturas por variante; el sello se evalúa con las tres series)

| variante | vidas | puesto ± ee | rapidez botiquín (días; 21 = no llega) · media | rapidez ración | cuándo botiquín (hp < 50 / usos) · ración (hp < 100 / usos) | sabiduría d11-20: s en red · s en camuflaje · vida perdida (las dos) | pruebas (b · r · red · cam) · forzadas |
|---|---:|---|---|---|---|---|---|
| TECHO | 40 | 4,88 ± 0,57 | 21, 21 · 21,0 | 21, 21 · 21,0 | 0 / 0 (0 %) · 0 / 0 | 288,1 · 176,5 · 85,0 | 0 (0 · 0 · 0 · 0) · 0 |
| BORRADO valiente | 40 | 4,10 ± 0,64 | 2, 12 · 7,0 | 1, 7 · 4,0 | 12 / 65 (18 %) · 44 / 44 | 238,0 · 236,6 · 59,8 | 139 (64 · 44 · 15 · 16) · 0 |
| BORRADO prudente | 40 | 4,90 ± 0,74 | 21, 21 · 21,0 | 5, 9 · 7,0 | 7 / 56 (12 %) · 55 / 55 | 203,1 · 224,1 · 60,6 | 141 (54 · 53 · 16 · 18) · 0 |
| APRENDE valiente | 40 | 4,42 ± 0,57 | 13, 10 · 11,5 | 2, 3 · 2,5 | 16 / 64 (25 %) · 40 / 40 | 234,8 · 170,8 · 52,9 | 137 (63 · 40 · 17 · 17) · 0 |
| APRENDE prudente | 40 | 4,88 ± 0,52 | 21, 21 · 21,0 | 2, 11 · 6,5 | 7 / 42 (17 %) · 59 / 59 | 198,8 · 226,6 · 65,7 | 132 (42 · 57 · 15 · 18) · 0 |
| SIN EMOCIÓN | 40 | 4,80 ± 0,60 | 21, 7 · 14,0 | 11, 2 · 6,5 | 9 / 38 (24 %) · 57 / 57 | 142,6 · 153,0 · 72,7 | 110 (37 · 53 · 12 · 8) · 118 |

R1 (APRENDE antes que SIN con el botiquín): APRENDE_p − SIN 7,0 ± 7,0 días, APRENDE_v − SIN -2,5 ± 7,2. C1 (usos del botiquín con hp < 50): APRENDE_p − SIN
-0,070 ± 0,090, APRENDE_v − SIN 0,013 ± 0,088. Con 2 criaturas por variante nada llega a 3 errores típicos; se evalúa al cerrar las tres series.

| variante | pruebas por vida y día, d1 → d20 |
|---|---|
| TECHO | 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 0,0 |
| BORRADO valiente | 3,0 1,5 3,0 2,5 2,0 4,0 1,0 3,0 2,5 6,0 3,0 5,0 0,0 2,5 2,0 5,5 8,0 3,5 8,5 3,0 |
| BORRADO prudente | 3,5 3,5 2,5 3,5 3,5 4,0 1,5 3,5 6,0 4,0 2,0 5,5 1,5 1,5 3,0 2,0 2,5 9,0 3,5 4,5 |
| APRENDE valiente | 3,0 2,5 4,5 2,5 4,0 0,5 3,0 3,0 4,0 4,5 5,0 2,5 3,5 4,5 2,0 6,0 2,5 6,5 1,5 3,0 |
| APRENDE prudente | 2,5 3,5 5,0 1,0 4,5 3,5 1,0 2,5 3,0 3,5 2,0 1,5 1,0 2,0 1,5 8,0 2,5 7,0 8,5 2,0 |
| SIN EMOCIÓN | 0,5 1,5 1,0 0,5 1,5 2,0 2,5 5,5 2,5 1,5 5,5 0,5 1,0 3,0 4,5 4,0 2,0 7,0 3,5 5,0 |

## Lectura (provisional)

Con la serie 1 sola: (i) la lentitud es pareja entre brazos (≤ 0,34 puntos) y los bloqueos sin cuerpo bajan a 0,2-0,5 % (piloto 1: 5-86 %): la regla v3b y el tope de
paralelismo hacen lo que se les pidió; la única parada es de latencia, en la última partida de APRENDE prudente (cuaderno del d19 con 1.168 apuntes; 37-44 ms de mediana en los
últimos 1.500 tics del final de partida). (ii) La creencia del botiquín sube despacio: APRENDE prudente no llega a 25 en 20 días en ninguna de sus 2 criaturas (a10: 23 el d20 con
15 recuerdos; a11: 19 con 26), APRENDE valiente llega los días 13 y 10, SIN EMOCIÓN una criatura el día 7 (usos forzados a cualquier vida: efectos grandes) y la otra no llega:
con el filtro B1 las intensidades quedan cerca de 1 y el neutro pesa más, y con la cautela se prueba menos. (iii) La sabiduría va por separado para red y camuflaje (tabla).
Todo esto se mide de verdad con 6 criaturas por variante: series 2 y 3.

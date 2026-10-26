# P7-56 · Sello y plan del primer campo del capítulo 5: la razón honesta (NADA lanzado)

*13-oct-2026. Sello `SELLO_P7_56.md` (commit `8ca48f2`, antes de calcular), con la tabla del mundo para juzgar las promesas fijada ANTES. Plataforma 0 créditos hoy; consola 0 $ hoy.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Potencia: `potencia_P7_56.py` → `P7_56_potencia.json` sobre los diarios de P7-50; coste de consola de `P7_54_razon.json`; `escribe_informe_P7_56.py` (este informe; ninguna cifra a mano).*

## Sección 1 · El sello (resumen; el texto que manda es `SELLO_P7_56.md`)

CON RAZÓN / SIN RAZÓN sobre COMPARTE de P7-50 (pareja 0,5/1,5, OJOS=1, hermanas) con la **fusión por evento** (`hermanas_P7_48` con `GEMV_P7_48_FUSION=1`, construida y comprobada en
réplica: el visto y el contado del mismo uso quedan en un solo recuerdo, marcado `confirmado_visto`). Noche como en el capítulo 4. En CON RAZÓN cada hermana tiene su razón
(`claude-sonnet-5-5`), diario limpio y menú (P7-54), invitaciones no compartidas, confianza 0,5 → 0,7 c + 0,3 acierto. R1 (menos usos del botiquín cortados por un golpe en CON
RAZÓN), R2 (al d20, confianza en cuerpo mayor en las invitaciones verdad que en las falsas, verdad por la tabla del mundo), a 3 veces el ruido; vigilancia sin predicción. Humo de 3; guarda,
equidad, tope y reintento como en P7-43e / P7-50.

## Sección 2 · Potencia de R1 con P7-50

| brazo de P7-50 | serie | usos del botiquín | cortados por un golpe | fracción |
|---|---:|---:|---:|---:|
| COMPARTE | 1 | 78 | 52 | 0,667 |
| COMPARTE | 2 | 68 | 41 | 0,603 |
| COMPARTE | 3 | 110 | 77 | 0,700 |
| SOLAS | 1 | 63 | 32 | 0,508 |
| SOLAS | 2 | 57 | 26 | 0,456 |
| SOLAS | 3 | 59 | 25 | 0,424 |

COMPARTE (la base de los dos brazos): 256 usos del botiquín en 3 series (85 por serie, las dos hermanas), 170 cortados por un golpe: fracción media 0,657, ruido entre series sd 0,049,
error binomial por serie 0,051. **En 3 series por brazo se vería una reducción del 18-19 % a 3 ee: un 30 % pide 2-2 series, un 50 % 1-1: R1 tiene potencia.** Lo esperado por brazo en 3 series: ≈ 256 usos y ≈ 170 cortes en SIN RAZÓN;
en CON RAZÓN, un 30 % menos serían ≈ 119 cortes. (SOLAS, como segunda referencia: fracción 0,463, sd 0,042: las que comparten usan más el botiquín bajo golpes.)
R2 no tiene ruido previo (no ha habido razón en ningún campo): se informa con el error típico que salga; se declara que el vínculo no informa (B saturado).

## Sección 3 · Coste

- **Créditos (bolsa 1)**: 2 brazos × 20 días × 3 series = 120 + 3 del humo (que cuentan si pasan) = **123**, más los reintentos que haya (P7-50: 4 + 2 apartadas en 126). Saldo de partida ≈ 102
  (228 − 126 de P7-50, 12-oct; no legible por la API) + 71 al día: el campo cabe en 1 día(s) de recarga (≈ 173); con margen para 6 reintentos, en 1 día(s).
- **Dólares de consola (bolsa 2)**: una llamada por hermana y día en CON RAZÓN = 2 × 20 × 3 = 120 llamadas; medido en P7-54: 13.111 + 1.990 tokens por llamada = 0,0692 $ supuestos (3/15 $ por millón)
  → **≈ 8,30 $**; con reintentos y la llamada de prueba, ≈ 8,73 $. Si la noche del humo falla, se repite la llamada (misma noche, mismo diario).
- Antes de lanzar: una llamada de prueba con la clave nueva de Manel en `cantera/paper5/.env` (una línea, modelo `claude-sonnet-5-5`; se anota su coste).

## Sección 4 · Lo que falta para lanzar (construido / por construir)

- Construido: `hermanas_P7_48` con fusión (gated), `invita_P7_54`, `campo_P7_54` (hermanas comparte + miedo + invitación), `Dockerfile.pareja_P7_54` (ARG HERMANAS; las invitaciones viajan en CUAD),
  `diario_razon_P7_54` (diario limpio desde un diario `.art.log`), `razon_P7_54` (prompt v2, parser), `local54_P7_54` (la cadena local con la razón entre días).
- Por construir al lanzar: `lanza_P7_56.py` / `orquesta_P7_56.py` = los de P7-50 con dos variantes (CON_RAZON, SIN_RAZON), `Dockerfile.pareja_P7_54`, `GEMV_P7_48_FUSION=1` en los dos,
  y en CON_RAZON, tras recoger el día d: diario limpio de las dos hermanas → razón → `invitaciones_P7_10/11.json` en `cuadernos_P7_56/CON_RAZON_serie<S>/` antes de hornear el d+1
  (si la razón falla, se reintenta una vez; si vuelve a fallar, el día sale sin invitaciones y se anota). Equidad y análisis: `equidad_P7_50` y `analiza_P7_50` con los nombres nuevos más
  R1/R2 y la vigilancia del sello.


# El campo (13-oct-2026): 3 series jugadas

*120 partidas válidas de 124 pedidas (3 de humo, que pasó por decisión de Manel; 4 reintentos únicos; 0 apartadas; 0 días perdidos). Bolsa 1: 124 partidas pedidas (hay
partidas que cuentan 0 créditos en la página); saldo real 107 a las 15:27 del 13-oct antes de la serie 3; ahora no legible (la página la ve Manel). Bolsa 2 (consola): 114 llamadas de razón = 1.162.541 + 230.640 tokens =
**6,95 $** supuestos; por serie: serie 1 2,30 $, serie 2 2,33 $, serie 3 2,33 $; más 0,0001 $ de la llamada de prueba. Noches sin razón: 1 (s2 d18 a11: 0 invitaciones validas).
Scripts: `analiza_P7_56.py` → `P7_56_sello.json`, `equidad_P7_56.py`, `incidencias_P7_56.py`, `amenaza_P7_56.py`, `escribe_informe_P7_56_campo.py` (esta parte; ninguna cifra a mano). `motor/model.py` intacto.*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| R1 | fracción de usos del botiquín cortados por un golpe: CON < SIN, ≥ 3 ee | CON 0,587 · SIN 0,685; -0,098 ± 0,059 (1,7 ee) | NO (dirección prevista) |
| R2 | al día 20, confianza en el cuerpo mayor tras invitaciones verdad que tras falsas (tabla del mundo) | verdad 0,657 (1154) · falsas 0,132 (54); 0,525 ± 0,032 (16,4 ee) | sí |

Segunda cuenta sin partidas marcadas: R1 -0,029 ± 0,075 (no pasa); R2 0,571 ± 0,023 (pasa). Días válidos: los 20 de las 3 series en los dos brazos.

| serie | CON_RAZON: usos del botiquín · cortados · fracción | SIN_RAZON: usos · cortados · fracción |
|---:|---|---|
| 1 | 59 · 38 · 0,644 | 100 · 65 · 0,650 |
| 2 | 52 · 25 · 0,481 | 90 · 66 · 0,733 |
| 3 | 74 · 47 · 0,635 | 88 · 59 · 0,670 |

Lo esperado en el plan: una reducción visible del 18-19 % con 3 series. La observada es del 14 %: en la dirección prevista, por debajo de lo que 3 series pueden ver. Y la razón cambió el uso:
CON_RAZON usó el botiquín 185 veces y SIN_RAZON 278.

## Vigilancia (sin predicción)

| serie · brazo | usos del botiquín | pruebas (a red+cam) | puesto valiente · prudente | vida perdida valiente · prudente | muertes v · p | camuflaje + quieta: ventanas · golpes/min | marcadas |
|---|---:|---|---|---|---|---|---:|
| s1 CON_RAZON | 59 | 124 (30) | 5,80 · 6,00 | 102 · 110 | 10 · 10 | 4 · 7,47 | 0 |
| s1 SIN_RAZON | 100 | 178 (33) | 7,20 · 5,15 | 116 · 136 | 9 · 11 | 5 · 0,00 | 3 |
| s2 CON_RAZON | 52 | 131 (30) | 6,05 · 5,90 | 111 · 116 | 7 · 11 | 6 · 1,00 | 4 |
| s2 SIN_RAZON | 90 | 169 (30) | 5,55 · 6,45 | 113 · 120 | 7 · 14 | 6 · 0,00 | 5 |
| s3 CON_RAZON | 74 | 153 (31) | 5,80 · 3,85 | 115 · 121 | 10 · 9 | 4 · 0,00 | 4 |
| s3 SIN_RAZON | 88 | 162 (33) | 4,15 · 4,95 | 114 · 117 | 5 · 9 | 10 · 0,00 | 3 |

La confianza en la dimensión vínculo no informa (B saturado en 1, P7-53).

| serie | aceptadas · evaluadas · pendientes al cierre | aceptadas por acción | confianza al d20: valiente (c · r · v) | prudente (c · r · v) |
|---:|---|---|---|---|
| 1 | 529 · 514 · 15 | QUEDARSE_QUIETA 233, COGER_BOTIQUIN 131, ACERCARSE_HERMANA 120, COGER_RACION 29, USAR_BOTIQUIN 5, COGER_RED 5, COGER_CAMUFLAJE 4, DAR_BOTIQUIN_HERMANA 1, USAR_RACION 1 | 0,96 · 1,00 · 0,92 | 0,92 · 0,14 · 0,92 |
| 2 | 420 · 413 · 7 | COGER_BOTIQUIN 158, ACERCARSE_HERMANA 91, QUEDARSE_QUIETA 81, COGER_RACION 62, COGER_CAMUFLAJE 20, USAR_BOTIQUIN 5, USAR_RACION 2, COGER_RED 1 | 0,93 · 0,31 · 0,69 | 0,58 · 0,91 · 0,01 |
| 3 | 285 · 281 · 4 | COGER_BOTIQUIN 134, ACERCARSE_HERMANA 57, COGER_RACION 48, QUEDARSE_QUIETA 37, USAR_BOTIQUIN 4, USAR_RACION 3, COGER_CAMUFLAJE 2 | 0,94 · 0,95 · 0,11 | 0,60 · 0,81 · 0,21 |

De las invitaciones aceptadas, cuántas llegan a evaluarse (no cortadas por la muerte ni por el fin de la partida), por día y hermana (las tres series):

| día | valiente: aceptadas → evaluadas | prudente: aceptadas → evaluadas |
|---:|---|---|
| 1 | 0 → 0 | 0 → 0 |
| 2 | 8 → 6 | 7 → 4 |
| 3 | 69 → 66 | 20 → 20 |
| 4 | 13 → 11 | 34 → 34 |
| 5 | 48 → 47 | 9 → 9 |
| 6 | 64 → 63 | 38 → 37 |
| 7 | 13 → 13 | 37 → 37 |
| 8 | 36 → 35 | 16 → 16 |
| 9 | 72 → 71 | 26 → 26 |
| 10 | 36 → 36 | 61 → 60 |
| 11 | 40 → 40 | 60 → 59 |
| 12 | 2 → 1 | 2 → 2 |
| 13 | 11 → 10 | 38 → 38 |
| 14 | 55 → 55 | 15 → 14 |
| 15 | 82 → 81 | 26 → 26 |
| 16 | 15 → 15 | 25 → 25 |
| 17 | 12 → 11 | 3 → 3 |
| 18 | 86 → 86 | 48 → 47 |
| 19 | 6 → 6 | 4 → 3 |
| 20 | 63 → 62 | 34 → 33 |

## Incidencias, equidad y latencia

| tipo | serie · día · brazo | hora | motivo |
|---|---|---|---|
| reintento | s2 d6 CON_RAZON | 08:09 | guarda dura: 16,84 % de decisiones sobre el tic en el asiento 10 (latencia); reintento con |
| reintento | s1 d14 SIN_RAZON | 10:18 | guarda dura: 10,89 % de decisiones sobre el tic en el asiento 10 (latencia de la plataform |
| reintento | s2 d14 CON_RAZON | 10:43 | la plataforma borro el pod del asiento 11 antes de recoger el registro (sin artefacto ni c |
| reintento | s2 d16 CON_RAZON | 11:45 | guarda dura: 12,47 % de decisiones sobre el tic en el asiento 11 (latencia de la plataform |

Equidad: 0,15 puntos entre brazos (no dudosa); marcadas 8 (CON) y 11 (SIN) de 120 cada uno; medianas 4,33 y 4,95 ms. El reparto de reintentos (3 en CON, 1 en
SIN) es azar de la plataforma: el brazo con razón va más ligero (menos marcadas, menos % sobre el tic), las invitaciones horneadas pesan 3413-4214 bytes frente a 676458-971084 de los
cuadernos, el horneado tarda lo mismo (153 s frente a 169) y las vidas lentas se reparten en las dos cadenas sin agruparse por hora.

% de decisiones sobre el tic por brazo y día (media de los dos asientos, tres series):

| brazo | d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 | d10 | d11 | d12 | d13 | d14 | d15 | d16 | d17 | d18 | d19 | d20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CON_RAZON | 0,00 | 1,53 | 0,00 | 0,00 | 0,00 | 0,00 | 0,13 | 0,02 | 0,40 | 0,01 | 0,00 | 0,00 | 0,80 | 0,82 | 0,20 | 0,02 | 1,78 | 0,01 | 0,77 | 0,00 |
| SIN_RAZON | 0,07 | 0,00 | 0,09 | 0,92 | 0,04 | 0,01 | 1,55 | 1,19 | 0,00 | 0,98 | 0,14 | 1,19 | 0,01 | 0,11 | 0,99 | 0,00 | 0,00 | 1,12 | 0,92 | 0,29 |

## Para el sello de P7-57: el botiquín en situación de amenaza (tal como está definida ahora)

Amenaza = rival a ≤ 4 casillas o fuego al abrir la prueba, o golpe recibido en los 48 tics anteriores (sin «vida < 30»). La falsa de P7-57 se juzga por lo vivido, siempre: esta fracción es la
probabilidad de que la mentira se desmienta al usarla, y la cura de los no cortados, lo que la «confirma» (refuerzo intermitente).

| brazo | en amenaza: usos · cortados · fracción cortada | cura media (todos · no cortados) | sin amenaza: usos · fracción cortada · cura media |
|---|---|---|---|
| CON_RAZON | 180 · 110 · 0,611 | 7,2 · 18,4 | 5 · 0,000 · 25,2 |
| SIN_RAZON | 269 · 190 · 0,706 | 6,5 · 22,0 | 9 · 0,000 · 26,7 |
| los dos | 449 · 300 · 0,668 | 6,8 · 20,3 | 14 · 0,000 · 26,1 |

En los dos brazos, 449 de 463 usos del botiquín fueron en amenaza; se cortaron el 67 %; los no cortados curaron 20,3 de media (127 de ellos tocaron el techo de vida, así
que su efecto es «al menos»). Con la regla de acierto (|vivido| ≥ la mitad de lo prometido), la falsa (+50) se confirmaría solo cuando la cura no se corta y alcanza 25.

## Lectura

1. **R1 no pasa**: con razón, la fracción de curas del botiquín cortadas por un golpe baja de 0,685 a 0,587 (1,7 errores típicos; hacía falta 3). En la segunda cuenta, sin las partidas
   marcadas por la guarda, la diferencia casi desaparece (-0,029 ± 0,075): el efecto es frágil. Lo que sí cambia con la razón es CUÁNTO se usa el botiquín (un tercio menos): las
   invitaciones aceptadas son sobre todo coger botiquines y raciones, quedarse quieta y acercarse a la hermana, no usar el botiquín.
2. **R2 pasa con mucho margen**: tras las invitaciones verdad la confianza en el cuerpo queda en 0,66 y tras las falsas en 0,13. Matiz: la mayoría de las evaluaciones son de coger (que la
   tabla da por verdad cuando promete 0 y casi siempre acierta) y las falsas son pocas (54); el mecanismo de confianza distingue la razón que acierta de la que no, que es lo que
   el campo de la mentira (P7-57) necesita.
3. Para P7-57: en amenaza, dos de cada tres curas del botiquín se cortan; la mentira «úsalo aunque te golpeen» se desmentirá la mayoría de las veces y se confirmará en el tercio restante.

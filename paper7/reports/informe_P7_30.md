# P7-30 · El segundo campo de la primera etapa: nacer sin saber, con la pieza rápida y la curiosidad del cuánto

*2026-10-09 (sellado el 8-oct-2026 en `f10da22`, antes de la primera partida). Coste: plataforma 10,4909 USD (las 120 partidas del campo) más 0,2624 del humo de freno (P7-29/29b, 3 partidas); consola 0.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. Sello: `SELLO_P7_30.md`. Diarios en `paintball/runs/P730_*` (fuera de git);
`analiza_P7_30.py` → `P7_30_vidas.json`; `sello_P7_30.py` → `P7_30_resumen.json`; figuras `figuras_P7_30.py`; este informe lo escribe `escribe_informe_P7_30.py`. El sello se ha evaluado una sola vez, al final.*

## El freno (paso 1 de la mesa, sobre el humo de P7-29/29b)

`freno_P7_30.py` → `P7_30_freno.json`: (a) el cuaderno viaja y se lee los días 2 y 3: sí; (b) tocan algún objeto desconocido 5 de 6 (d1 a10, d1 a11, d2 a10, d3 a10, d3 a11); (c) sube la creencia: d2 a10 racion: None -> 8.5808; d3 a10 racion: 8.5808 -> 11.4004; d3 a11 botiquin: None -> 28.7075; d3 a11 racion: None -> 4.5824; (d) la guarda de latencia (regla de la mesa de P7-30) pasa en 6 de 6. **PASA.** Guarda de latencia del humo: d1·10 5,3 / 20,5 / 84,1 ms, 0,32 % sobre el tic; d1·11 7,0 / 12,4 / 34,2 ms, 0,00 % sobre el tic; d2·10 1,2 / 5,4 / 27,1 ms, 0,00 % sobre el tic; d2·11 1,8 / 6,6 / 38,7 ms, 0,00 % sobre el tic; d3·10 2,8 / 14,4 / 46,2 ms, 0,01 % sobre el tic; d3·11 2,0 / 7,9 / 24,0 ms, 0,00 % sobre el tic.

## El sello

| | regla | resultado | |
|---|---|---|---|
| E1 | descubre: firmes de los dos al día 5 en las 4; ignorancia < 0,3 al día 10 en ≥ 3 | firmes de los dos al día 5: **1 de 4**; ignorancia < 0,3 al día 10: 4 de 4 | **no pasa** |
| E2 | aprende a aprender: el segundo objeto tarda menos en ≥ 3 | 1 de 4 | **no pasa** |
| E3 | qué aprende antes: la ración llega al 80 % antes que el botiquín en ≥ 3 | 2 de 4 | **no pasa** |
| E4 | pierde y recupera: APRENDE − TECHO > 2 ee en 1-5; ≤ la mitad en 16-20 | 1-5: 0,60 ± 1,34 (n 20); 16-20: -0,80 ± 0,80 (n 20) | **no pasa** |
| E5 | sin memoria no recupera: BORRADO − TECHO en 16-20 ≥ la mitad de 1-5 | 1-5: -0,25 ± 1,25 (n 20); 16-20: 0,10 ± 0,90 (n 20) | **pasa** |
| E6 | lo aprendido cambia la conducta: vida al abrir el botiquín (11-20), APRENDE < BORRADO | medianas 74 (94 aperturas) frente a 88 (64) | **pasa** |
| E7 | el cuánto: creencia del botiquín dentro ≥ 35 el día 20 en ≥ 3 de 4 | 2 de 4 | **no pasa** |
| E8 | no se hunde: APRENDE − BORRADO en 16-20 no mayor que en 1-5 por más de 2 ee | 1-5: 0,85 ± 1,49 (n 20); 16-20: -0,90 ± 0,95 (n 20); crece -1,75 con ee de la diferencia 1,77 | **pasa** |

**Primera cuenta (todas las vidas; solo salen las partidas con corte de la plataforma, como manda el sello): pasan E5, E6, E8; no pasan E1, E2, E3, E4, E7.**

**Segunda cuenta (quitando además las 14 partidas marcadas por la guarda de latencia, enteras, y sus pares):** E4 1-5 0,00 ± 1,33 (n 16), 16-20 -1,38 ± 0,94 (n 16) → no pasa; E5 1-5 -0,39 ± 1,39 (n 18), 16-20 -0,33 ± 0,95 (n 18) → no pasa; E6 medianas 73 (88) frente a 85 (56) → pasa; E8 1-5 -1,36 ± 1,64 (n 14), 16-20 -1,07 ± 1,27 (n 14), crece 0,29 con ee 2,08 → pasa; E1, E2, E3 y E7 no dependen del puesto. **Cambian de resultado entre las dos cuentas: E5.** Sin excluir nada (ni cortes): E4 no pasa, E5 pasa, E8 pasa. Partidas marcadas: serie 1 día 1 BORRADO, serie 1 día 2 APRENDE, serie 1 día 5 APRENDE, serie 1 día 7 APRENDE, serie 1 día 7 BORRADO, serie 1 día 12 BORRADO, serie 1 día 20 APRENDE, serie 2 día 6 BORRADO, serie 2 día 7 BORRADO, serie 2 día 9 APRENDE, serie 2 día 11 BORRADO, serie 2 día 14 APRENDE, serie 2 día 17 BORRADO, serie 2 día 20 APRENDE.

**Lectura del sello.** Lo que P7-24 no tenía y este campo sí: **la que recuerda ya no se hunde** (E8): APRENDE − BORRADO pasa de 0,85 puestos en los días 1-5 a -0,90 en los días 16-20 (en P7-24, de +0,9 a +4,0), y APRENDE − TECHO de 0,60 a -0,80: al final del campo la que recuerda queda por delante de las otras dos, y E4 no pasa solo porque en los días 1-5 no estaba peor que el techo por más de 2 errores estándar (su primera mitad: no hay nada que recuperar). E5 pasa en la primera cuenta y no en la segunda porque BORRADO − TECHO es cero en los dos bloques (-0,25 y 0,10): la regla "≥ la mitad" no distingue nada cuando la diferencia de partida es nula o negativa; es la única predicción que cambia entre las dos cuentas y cambia por eso. E6 pasa (vida al abrir el botiquín 74 frente a 88). E7 no pasa por una criatura: 2 de 4 llegan a 35 (35,8, 28,8, 39,6, 29,8; en P7-24 el techo del campo era 29,9). E1, E2 y E3 siguen sin pasar como en P7-24: la ignorancia baja en las cuatro (4 de 4 al día 10) pero los recuerdos firmes del botiquín son pocos (0, 0, 1, 0 al día 5): el cuerpo sigue usando casi siempre entero y aprendiendo "al menos".

## Sección 1 · El campo tal como se jugó

- 3 brazos × 20 días × 2 series = 120 partidas pedidas, la misma semilla para los tres brazos cada día (`semillas_P7_30.json`: k = 178-197; serie 2 en orden inverso). 240 vidas con diario.
- Partidas con corte de la plataforma: **0**.
- Guarda de latencia (mesa, P7-30): vidas que no pasan: 15 de 240 (APRENDE 8, BORRADO 7, TECHO 0). Tiempo de decisión por brazo (mediana de medianas · p95 máximo · máximo): APRENDE 3,92 · 42,5 · 123,5 ms, BORRADO 5,01 · 44,7 · 121,6 ms, TECHO 1,84 · 15,9 · 88,2 ms; decisiones por encima del tic (media de vidas): APRENDE 0,31 %, BORRADO 0,38 %, TECHO 0,00 %; pasos listos bloqueados sin cuerpo (media): APRENDE 1,26 %, BORRADO 0,69 %, TECHO 0,36 %.

| brazo | días | ms por decisión: mediana (mediana de vidas) · p95 (máx entre vidas) | decisiones por encima del tic (máx entre vidas) | pasos listos bloqueados sin cuerpo (máx) | vidas que no pasan la guarda |
|---|---|---|---:|---:|---:|
| TECHO | 1-5 | 1,58 · 15,9 | 0,13 % | 0,47 % | 0 |
| TECHO | 6-10 | 1,17 · 14,4 | 0,06 % | 3,11 % | 0 |
| TECHO | 11-15 | 1,41 · 15,4 | 0,09 % | 2,68 % | 0 |
| TECHO | 16-20 | 1,19 · 14,6 | 0,00 % | 0,28 % | 0 |
| BORRADO | 1-5 | 5,06 · 44,7 | 7,36 % | 0,85 % | 1 |
| BORRADO | 6-10 | 4,95 · 44,2 | 6,49 % | 40,49 % | 3 |
| BORRADO | 11-15 | 5,83 · 41,6 | 4,96 % | 1,52 % | 2 |
| BORRADO | 16-20 | 3,88 · 31,6 | 1,08 % | 2,64 % | 1 |
| APRENDE | 1-5 | 3,92 · 42,5 | 5,17 % | 0,88 % | 2 |
| APRENDE | 6-10 | 2,26 · 40,5 | 4,26 % | 40,99 % | 2 |
| APRENDE | 11-15 | 2,67 · 25,8 | 0,36 % | 40,76 % | 1 |
| APRENDE | 16-20 | 2,96 · 38,2 | 3,21 % | 2,60 % | 3 |

## Sección 2 · Las medidas, por brazo y bloque de días

| brazo | días | vidas (en puesto) | puesto medio | mueren · vida al morir (mediana) | botiquín: canales (firmes, «al menos», cortes) · vida al abrir | ración: canales (firmes, «al menos», cortes) · vida al abrir | pedidos · regalos | `ir_curioso` con paso listo (mediana %) | contacto botiquín · ración (vidas) | ign. del cuánto botiquín (media) |
|---|---|---|---:|---|---|---|---|---:|---|---:|
| TECHO | 1-5 | 20 (20) | 4,95 | 14 · 6 | 56 canales del diario · 63 | 0 (0, 0, 0) · — | 30 · 14 | 0,0 | 19 · 16 | — |
| TECHO | 6-10 | 20 (20) | 8,05 | 19 · 4 | 56 canales del diario · 49 | 0 (0, 0, 0) · — | 28 · 22 | 0,0 | 16 · 9 | — |
| TECHO | 11-15 | 20 (20) | 5,85 | 20 · 8 | 71 canales del diario · 49 | 0 (0, 0, 0) · — | 32 · 23 | 0,0 | 17 · 11 | — |
| TECHO | 16-20 | 20 (20) | 5,75 | 16 · 3 | 72 canales del diario · 54 | 0 (0, 0, 0) · — | 28 · 19 | 0,0 | 19 · 16 | — |
| BORRADO | 1-5 | 20 (20) | 4,70 | 12 · 1 | 46 (3, 18, 25) · 86 | 31 (16, 10, 5) · 86 | 12 · 5 | 0,5 | 18 · 13 | 0,916 |
| BORRADO | 6-10 | 20 (20) | 6,70 | 15 · 2 | 34 (0, 16, 18) · 86 | 22 (15, 7, 0) · 83 | 6 · 1 | 0,4 | 16 · 9 | 1,000 |
| BORRADO | 11-15 | 20 (20) | 7,00 | 18 · 3 | 31 (2, 16, 13) · 89 | 15 (5, 8, 0) · 89 | 11 · 7 | 0,3 | 16 · 13 | 0,942 |
| BORRADO | 16-20 | 20 (20) | 5,85 | 15 · 2 | 32 (1, 18, 12) · 85 | 22 (10, 12, 0) · 92 | 12 · 6 | 0,3 | 18 · 15 | 0,970 |
| APRENDE | 1-5 | 20 (20) | 5,55 | 14 · 2 | 38 (1, 14, 23) · 80 | 26 (9, 17, 0) · 93 | 26 · 16 | 0,1 | 16 · 15 | 0,944 |
| APRENDE | 6-10 | 20 (20) | 6,25 | 14 · 2 | 23 (2, 11, 10) · 80 | 28 (6, 21, 1) · 93 | 23 · 30 | 0,3 | 14 · 13 | 0,845 |
| APRENDE | 11-15 | 20 (20) | 7,55 | 19 · 2 | 44 (2, 8, 34) · 67 | 17 (4, 12, 0) · 93 | 23 · 16 | 0,3 | 13 · 13 | 0,691 |
| APRENDE | 16-20 | 20 (20) | 4,95 | 12 · 4 | 46 (5, 16, 19) · 84 | 39 (6, 19, 0) · 86 | 32 · 47 | 0,2 | 16 · 16 | 0,337 |

TECHO sabe y no escribe recuerdos: sus usos del botiquín salen de los canales del diario (definiciones de P7-21), como en P7-24.

## Sección 3 · E1, E2, E3 y E7 de cerca (las 4 criaturas de APRENDE)

**E1.**

| criatura | recuerdos firmes al acabar el día 5: botiquín / ración | ignorancia al acabar el día 10: botiquín / ración |
|---|---|---|
| s1_10 | 0 / 5 | 0,144 / 0,046 |
| s1_11 | 0 / 2 | 0,073 / 0,260 |
| s2_10 | 1 / 1 | 0,040 / 0,059 |
| s2_11 | 0 / 1 | 0,067 / 0,102 |

**E2.**

| criatura | primer contacto (tics de vida acumulados): botiquín / ración | primer recuerdo firme: botiquín / ración | tarda desde el contacto: botiquín / ración | orden | el segundo tarda menos |
|---|---|---|---|---|---|
| s1_10 | 626 / 11.742 | 189.209 / 53.051 | 188.583 / 41.309 | racion → botiquin | no |
| s1_11 | 23.450 / 10.417 | 150.348 / 12.714 | 126.898 / 2.297 | racion → botiquin | no |
| s2_10 | 626 / 10.521 | 52.720 / 56.044 | 52.094 / 45.523 | botiquin → racion | sí |
| s2_11 | 637 / 8.903 | 192.762 / 62.338 | 192.125 / 53.435 | racion → botiquin | no |

**E3.**

| criatura | día en que la ración llega a 12 | día en que el botiquín (dentro) llega a 40 | la ración antes |
|---|---:|---:|---|
| s1_10 | 4 | nunca | sí |
| s1_11 | 20 | nunca | sí |
| s2_10 | nunca | 15 | no |
| s2_11 | nunca | nunca | no |

**E7.**

| criatura | creencia del botiquín dentro (sin cortes) al acabar el día 20 | ≥ 35 |
|---|---:|---|
| s1_10 | 35,8 | sí |
| s1_11 | 28,8 | no |
| s2_10 | 39,6 | sí |
| s2_11 | 29,8 | no |

**Por criatura y día** (creencia e ignorancia al cerrar el día; firmes, «al menos» y cortes aparte):

| criatura | día | botiquín: creencia dentro · ignorancia · ign. cuánto · sabe | firmes · al menos · cortes (botiquín) | ración: creencia · ign. cuánto | firmes · al menos · cortes (ración) | puesto |
|---|---:|---|---|---|---|---:|
| s1·10 | 1 | 13,0 · 0,457 · 1,000 · 24,0 | 0 · 1 · 0 | 7,7 · 1,000 | 0 · 1 · 0 | 3 |
| s1·10 | 3 | 19,5 · 0,122 · 1,000 · 30,0 | 0 · 3 · 4 | 8,7 · 1,000 | 0 · 3 · 0 | 2 |
| s1·10 | 5 | 19,0 · 0,133 · 1,000 · 30,0 | 0 · 3 · 4 | 12,4 · 0,153 | 5 · 8 · 0 | 6 |
| s1·10 | 8 | 18,3 · 0,131 · 1,000 · 30,0 | 0 · 4 · 4 | 12,5 · 0,174 | 5 · 16 · 0 | 6 |
| s1·10 | 10 | 17,7 · 0,144 · 1,000 · 30,0 | 0 · 4 · 4 | 12,3 · 0,189 | 5 · 18 · 0 | 12 |
| s1·10 | 13 | 23,2 · 0,058 · 1,000 · 33,0 | 0 · 6 · 13 | 12,1 · 0,147 | 7 · 20 · 0 | 6 |
| s1·10 | 15 | 22,7 · 0,040 · 1,000 · 33,0 | 0 · 6 · 21 | 11,9 · 0,160 | 7 · 21 · 0 | 7 |
| s1·10 | 18 | 30,9 · 0,035 · 0,277 · 50,0 | 2 · 7 · 24 | 11,6 · 0,182 | 7 · 21 · 0 | 2 |
| s1·10 | 20 | 35,8 · 0,032 · 0,222 · 50,0 | 3 · 9 · 26 | 11,3 · 0,198 | 7 · 24 · 0 | 6 |
| s1·11 | 1 | — · 1,000 · 1,000 · — | 0 · 0 · 0 | 7,6 · 0,498 | 1 · 1 · 0 | 7 |
| s1·11 | 3 | 3,0 · 0,197 · 1,000 · 27,0 | 0 · 2 · 2 | 3,1 · 0,333 | 2 · 1 · 0 | 1 |
| s1·11 | 5 | 7,1 · 0,062 · 1,000 · 27,0 | 0 · 4 · 11 | 3,0 · 0,356 | 2 · 1 · 0 | 5 |
| s1·11 | 8 | 6,8 · 0,066 · 1,000 · 27,0 | 0 · 5 · 11 | 4,8 · 0,393 | 2 · 2 · 0 | 14 |
| s1·11 | 10 | 6,6 · 0,073 · 1,000 · 27,0 | 0 · 5 · 11 | 4,7 · 0,417 | 2 · 2 · 0 | 8 |
| s1·11 | 13 | 32,1 · 0,039 · 0,430 · 50,0 | 1 · 8 · 19 | 7,7 · 0,290 | 3 · 3 · 0 | 13 |
| s1·11 | 15 | 31,2 · 0,031 · 0,455 · 50,0 | 1 · 9 · 26 | 7,5 · 0,311 | 3 · 4 · 0 | 6 |
| s1·11 | 18 | 29,8 · 0,035 · 0,494 · 50,0 | 1 · 10 · 26 | 11,0 · 0,160 | 6 · 5 · 0 | 7 |
| s1·11 | 20 | 28,8 · 0,037 · 0,519 · 50,0 | 1 · 11 · 26 | 12,0 · 0,128 | 8 · 12 · 0 | 5 |
| s2·10 | 1 | 6,2 · 0,437 · 1,000 · 11,0 | 0 · 1 · 0 | 3,6 · 1,000 | 0 · 1 · 0 | 4 |
| s2·10 | 3 | 12,6 · 0,136 · 1,000 · 27,0 | 0 · 4 · 2 | 6,9 · 1,000 | 0 · 3 · 0 | 2 |
| s2·10 | 5 | 27,6 · 0,088 · 0,448 · 50,0 | 1 · 5 · 4 | 8,6 · 0,425 | 1 · 3 · 0 | 11 |
| s2·10 | 8 | 26,1 · 0,083 · 0,486 · 50,0 | 1 · 7 · 4 | 9,0 · 0,463 | 1 · 5 · 0 | 9 |
| s2·10 | 10 | 39,7 · 0,040 · 0,205 · 50,0 | 3 · 8 · 13 | 7,4 · 0,132 | 6 · 9 · 1 | 6 |
| s2·10 | 13 | 38,4 · 0,046 · 0,232 · 50,0 | 3 · 8 · 13 | 8,0 · 0,129 | 7 · 11 · 1 | 2 |
| s2·10 | 15 | 41,5 · 0,039 · 0,170 · 50,0 | 4 · 9 · 15 | 7,9 · 0,141 | 7 · 13 · 1 | 5 |
| s2·10 | 18 | 40,4 · 0,043 · 0,193 · 50,0 | 4 · 10 · 15 | 7,8 · 0,161 | 7 · 15 · 1 | 5 |
| s2·10 | 20 | 39,6 · 0,032 · 0,209 · 50,0 | 4 · 16 · 18 | 7,6 · 0,175 | 7 · 20 · 1 | 3 |
| s2·11 | 1 | — · 0,158 · 1,000 · 7,0 | 0 · 1 · 3 | 3,5 · 1,000 | 0 · 1 · 0 | 3 |
| s2·11 | 3 | — · 0,172 · 1,000 · 7,0 | 0 · 1 · 3 | 6,8 · 1,000 | 0 · 4 · 0 | 10 |
| s2·11 | 5 | 8,2 · 0,133 · 1,000 · 15,0 | 0 · 2 · 4 | 9,3 · 0,476 | 1 · 5 · 0 | 5 |
| s2·11 | 8 | 15,0 · 0,102 · 1,000 · 33,0 | 0 · 5 · 4 | 9,2 · 0,340 | 2 · 9 · 0 | 16 |
| s2·11 | 10 | 16,1 · 0,067 · 1,000 · 33,0 | 0 · 8 · 5 | 8,9 · 0,364 | 2 · 9 · 0 | 5 |
| s2·11 | 13 | 19,3 · 0,068 · 1,000 · 33,0 | 0 · 9 · 5 | 8,3 · 0,400 | 2 · 9 · 0 | 9 |
| s2·11 | 15 | 19,1 · 0,074 · 1,000 · 33,0 | 0 · 9 · 5 | 8,7 · 0,425 | 2 · 12 · 0 | 7 |
| s2·11 | 18 | 30,8 · 0,045 · 0,423 · 50,0 | 1 · 12 · 11 | 8,5 · 0,463 | 2 · 13 · 0 | 6 |
| s2·11 | 20 | 29,8 · 0,036 · 0,308 · 50,0 | 2 · 13 · 16 | 10,7 · 0,320 | 3 · 13 · 0 | 2 |

Cortes del botiquín y de la ración en APRENDE (87 recuerdos del acto), por causa: daño · noop: 56, daño · ir_curioso: 20, daño · ir_botin: 3, daño · move_SW: 2, daño · move_SE: 1, daño · atacar_S: 1, daño · ir_objeto: 1, daño · move_W: 1.

## Sección 4 · El puesto (E4, E5, E8)

| comparación | días 1-5 (media ± error estándar) | días 16-20 |
|---|---|---|
| APRENDE - TECHO · excluyendo las partidas con corte | 0,60 ± 1,34 (n 20) | -0,80 ± 0,80 (n 20) |
| APRENDE - TECHO · sin excluir nada | 0,60 ± 1,34 (n 20) | -0,80 ± 0,80 (n 20) |
| APRENDE - TECHO · excluyendo cortes y marcadas | 0,00 ± 1,33 (n 16) | -1,38 ± 0,94 (n 16) |
| BORRADO - TECHO · excluyendo las partidas con corte | -0,25 ± 1,25 (n 20) | 0,10 ± 0,90 (n 20) |
| BORRADO - TECHO · sin excluir nada | -0,25 ± 1,25 (n 20) | 0,10 ± 0,90 (n 20) |
| BORRADO - TECHO · excluyendo cortes y marcadas | -0,39 ± 1,39 (n 18) | -0,33 ± 0,95 (n 18) |
| APRENDE − BORRADO (E8; partidas con corte excluidas) | 0,85 ± 1,49 (n 20) | -0,90 ± 0,95 (n 20) |
| APRENDE − BORRADO (sin excluir) | 0,85 ± 1,49 (n 20) | -0,90 ± 0,95 (n 20) |

Figuras: `P7_30_fig_puesto.png` (el puesto por día) y `P7_30_fig_creencias.png` (creencia e ignorancia por día de cada criatura, APRENDE y BORRADO).

## Sección 5 · Lo aprendido y la conducta (E6, y el cuánto al usar)

Vida al abrir el botiquín en los días 11-20: APRENDE mediana 74 en 94 aperturas; BORRADO 88 en 64. Con cuánta vida usa APRENDE el botiquín cuando le pesa la curiosidad del cuánto (lo que le falta es mayor que lo más alto que sabe que da): 57 aperturas, vida mediana 40; cuando lo conoce y no le pesa: 95, mediana 84; sin conocerlo aún: 4, mediana 91.

## Sección 5b · Las vidas lentas y el puesto (mesa, P7-30); el sesgo de E4

| brazo | vidas | correlación de rangos: decisiones sobre el tic ~ puesto | ~ muere | marcadas por la guarda: n · puesto medio · mueren · tic de muerte (mediana) | no marcadas: n · puesto medio · mueren · tic de muerte |
|---|---:|---:|---:|---|---|
| APRENDE | 80 | 0,06 | 0,06 | 8 · 5,88 · 6 · 12.528 | 72 · 6,10 · 53 · 12.816 |
| BORRADO | 80 | -0,16 | 0,01 | 7 · 6,14 · 6 · 12.948 | 73 · 6,05 · 54 · 12.588 |
| TECHO | 80 | -0,05 | 0,03 | 0 · — · 0 · — | 80 · 6,15 · 69 · 12.888 |

Las doce vidas más lentas de APRENDE (decisiones sobre el tic · ms mediana · puesto · muerte): s1 d2 a11: 5,17 % · 9,7 · 15 · tic 10.896; s2 d9 a10: 4,26 % · 9,9 · 1 · vive; s2 d20 a11: 3,21 % · 20,0 · 2 · vive; s2 d20 a10: 2,83 % · 23,9 · 3 · tic 14.037; s1 d20 a11: 2,61 % · 8,0 · 5 · tic 13.488; s1 d5 a10: 2,19 % · 5,2 · 6 · tic 12.600; s2 d5 a10: 0,84 % · 6,9 · 11 · tic 11.712; s1 d8 a10: 0,73 % · 4,7 · 6 · tic 13.008; s2 d2 a11: 0,53 % · 2,8 · 5 · tic 13.184; s1 d18 a10: 0,39 % · 6,3 · 2 · vive; s2 d11 a11: 0,36 % · 4,2 · 10 · tic 11.928; s2 d13 a10: 0,35 % · 5,7 · 2 · vive.

**Declaración (mesa, P7-30):** APRENDE y BORRADO cargan con el coste de las piezas del siete en cada candidato (decisión a 3,9 y 5,0 ms de mediana frente a 1,8 de TECHO; decisiones por encima del tic 0,31 % y 0,38 % frente a 0,00 %) y TECHO no; cuando una decisión llega tarde el mundo la aplica tarde y el cuerpo pierde pasos. Por eso **E4 (APRENDE − TECHO) está inclinada en contra de APRENDE**, y E5 (BORRADO − TECHO) en contra de BORRADO; E8 (APRENDE − BORRADO) compara dos brazos con la misma carga.

## Sección 5c · Lo que esto dice, y lo que queda para la mesa

1. **El arreglo de P7-29 hace lo que decía.** `ir_curioso` con el paso listo: mediana del 0,2 % en los días 16-20 (P7-24: 39 %); la decisión de APRENDE a 3,9 ms de mediana con el 0,31 % de decisiones sobre el tic (P7-24, días 16-20: 31 ms y 32 %); y el puesto de la que recuerda ya no cae con los días (E8). Las vidas lentas no acaban peor (correlación de rangos entre decisiones sobre el tic y puesto: 0,06 en APRENDE).
2. **Lo que aprende sigue siendo flojo y "al menos".** Creencia del botiquín dentro al día 20: 35,8, 28,8, 39,6, 29,8 de 50 (sin cortes, arreglo 3; en P7-24, 9,5-17,6 con cortes); firmes del botiquín en 20 días: 3, 1, 4, 2 por criatura, frente a 9, 11, 16, 13 "al menos" y 26, 26, 18, 16 cortes (guardados aparte como actos, 87 en total, todos por daño: daño · noop: 56, daño · ir_curioso: 20, daño · ir_botin: 3).
3. **El cuánto hace lo que se diseñó:** cuando le pesa (lo que le falta es mayor que lo más alto que sabe que da el botiquín), lo abre con una vida mediana de 40 (57 aperturas); cuando no, con 84 (95). La ignorancia del cuánto del botiquín al día 20: 0,222, 0,519, 0,209, 0,308; la de la ración, 0,198, 0,128, 0,175, 0,320.
4. **Lo que queda para la mesa:** E5 está mal planteada cuando BORRADO no empieza peor que TECHO; E4 está inclinada en contra de APRENDE por la carga de las piezas (sección 5b); las inundaciones del mundo (P7-31) explican las 2 partidas marcadas por pasos bloqueados sin cuerpo y el cuerpo congelado no las lee; el recuerdo firme sigue siendo la pieza que falta para que la creencia del botiquín llegue a su cura.

## Sección 6 · Créditos

Plataforma: 10,4909 USD en 120 partidas del campo (0,0874 por partida) + 0,2624 USD del humo de freno (3 partidas). Acumulado del siete en la plataforma: 42,0106 (hasta P7-29b, con el día 1 del humo) + 0,1535 (días 2 y 3 del humo) + 10,4909 = **52,6550 USD**. Consola de Anthropic: 0. Saldos no consultados.

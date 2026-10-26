# P7-29b · El humo con la pieza rápida, y la latencia de los campos anteriores

*8-oct-2026. Coste: plataforma 0,1089 USD (el humo, F5); consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. Decisiones de la mesa aplicadas: (1) la red de los muros se quita del todo (`nace_P7_29.py`, `banco_P7_29.py`, `Dockerfile.pareja_P7_29`; queda en el commit f9a2e75); quedan la caché, la curiosidad que solo mueve por curiosidad, el corte aparte y la curiosidad del cuánto; (2) guarda de latencia nueva (`guarda_latencia_P7_29.py`, enganchada en `lanza_P7_29.py` al bajar cada diario: p95 > 20 ms o más del 5 % de pasos listos bloqueados sin cuerpo delante = la cadena para y avisa). Este informe lo escribe `escribe_informe_P7_29b.py` desde `P7_29_humo.json`, `P7_29_estado.json` y `P7_29b_latencia.json`. Ninguna cifra a mano.*

## En corto

1. **Humo F4 (APRENDE, semillas k 175-177): PARADO por la guarda de latencia tras el día 1** (1 partida jugada: d1 completed). La guarda es la regla 2 de la mesa: p95 > 20 ms = la cadena para y avisa; aquí el p95 del asiento 10 fue 20,53 ms (por 0,53 ms), con mediana 5,3 ms y el 0,3 % de los tics por encima del tic; los tics más lentos son los de 20-21 candidatos (todos los pasos y ataques posibles), no los del recuerdo (el cuaderno acaba el día con 2 recuerdos). Con esta guarda, en P7-14b habrían parado 12 vidas de 320 (punto 4). Los días 2 y 3 no se han jugado: decisión de la mesa. Guarda de latencia: NO PASA en d1 asiento 10: p95 20.53 ms > 20.0; ms de decisión: d1·10 5,3 / 20,5 / 84,1, d1·11 7,0 / 12,4 / 34,2 (mediana / p95 / máximo).
2. **Lo que hizo la que nace rápida (día 1):** d1·10: botiquín 2 canales (0 firmes, 2 al menos, 0 cortes), ración 0 (0 firmes), creencia botiquín 4,3, ign. cuánto 1,00, ir_curioso 0 %, puesto 1; d1·11: botiquín 2 canales (0 firmes, 1 al menos, 1 cortes), ración 0 (0 firmes), creencia botiquín —, ign. cuánto 1,00, ir_curioso 1 %, puesto 3.
3. **Punto 4 (P7-10 y P7-14b, solo describir):** APRENDE decidía más despacio que los demás (mediana 3,1 ms en P7-10 y 3,8 en P7-14b, frente a TECHO 1,2 y 2,1, BORRADO 2,0 y 2,8), pero muy por debajo del tic: 0,00 % y 0,02 % de tics por encima de 41,7 ms, y 0,37 % / 0,28 % de pasos listos bloqueados sin cuerpo (los demás brazos, parecido). Las muertes tempranas de APRENDE (1 en P7-10, 4 en P7-14b) pasan todas la guarda (p95 4,5 y 10,7 ms; bloqueados sin cuerpo 2,0 % y 1,0 %): **la latencia no explica las muertes tempranas que separaban a APRENDE de BORRADO en esos campos.** Lo que creció hasta romper fue el recuerdo por parecido de P7-23 (P7-24), que esos campos no tenían.

## F4 · El humo de 3 días (APRENDE, semillas nuevas)

Semillas: `semillas_P7_29.json` (k 175-177: 38588491, 38693220, 38797949); imagen `Dockerfile.pareja_P7_29` (GEMV_P7_29=1: caché, curiosidad por curiosidad, corte aparte, cuánto; sin red de muros); lanzador `lanza_P7_29.py --cadena-aprende 1 1 3` (cada día se hornea con los cuadernos del día anterior); diarios en `paintball/runs/P729_s1_d<D>_APRENDE_<semilla>/`; lectura `analiza_P7_29.py` -> `P7_29_humo.json`. Partidas: d1 completed (0,1089 USD).

**La guarda de latencia** (medida al bajar cada diario; `P7_29_estado.json`, `peticiones[].latencia`):

| día · asiento | decisiones | ms mediana · p95 · máximo | tics por encima del tic (41,7 ms) | pasos listos | bloqueados · sin cuerpo delante | guarda |
|---|---:|---|---:|---:|---|---|
| d1 · 10 | 14.188 | 5,30 · 20,53 · 84,14 | 0,32 % | 2.178 | 57 · 6 (0,28 %) | NO PASA: p95 20.53 ms > 20.0 |
| d1 · 11 | 12.648 | 6,96 · 12,37 · 34,25 | 0,00 % | 10.051 | 58 · 5 (0,05 %) | pasa |

**Por día y criatura:**

| día · asiento | tics | puesto | contacto botiquín · ración (tic) | botiquín: canales · firmes · al menos · cortes (vida al abrir) | ración: canales · firmes · al menos · cortes | creencia botiquín dentro · fuera | ignorancia clase · cuánto · lo más alto que sabe | ración: creencia dentro · ign. cuánto | `ir_curioso` con paso listo |
|---|---:|---:|---|---|---|---|---|---|---|
| d1 · 10 | 14.188 | 1 | 626 · 12.734 | 2 · 0 · 2 · 0 (92, 93) | 0 · 0 · 0 · 0 | 4,3 · 3,6 | 0,311 · 1,000 · 8,0 | — · — | 7 (0 %) |
| d1 · 11 | 12.648 | 3 | 1.324 · — | 2 · 0 · 1 · 1 (93, 86) | 0 · 0 · 0 · 0 | — · 7,3 | 0,326 · 1,000 · 14,0 | — · — | 93 (1 %) |

Cortes del día con su causa (recuerdos `acto` del cuaderno, arreglo 3): d1·11 botiquin: daño 6.56 de ['anillo'], última elección `ir_pareja`, 46 tics.

La fila del cuánto en la partida (`P7_cuanto`, una muestra cada 3.000 tics): d1·10 t481: M 0,0000 (curiosidad de clase 0,0950), botiquín ign. 1,000 / cuánto 1,000 / sabe —; d1·10 t3.481: M 0,0000 (curiosidad de clase 0,0704), botiquín ign. 1,000 / cuánto 1,000 / sabe —; d1·10 t6.481: M 0,0000 (curiosidad de clase 0,0707), botiquín ign. 1,000 / cuánto 1,000 / sabe —; d1·10 t9.481: M 0,0000 (curiosidad de clase 0,0700), botiquín ign. 1,000 / cuánto 1,000 / sabe —; d1·11 t481: M 0,0000 (curiosidad de clase 0,0946), botiquín ign. 1,000 / cuánto 1,000 / sabe —; d1·11 t3.481: M 0,0000 (curiosidad de clase 0,0694), botiquín ign. 1,000 / cuánto 1,000 / sabe —; d1·11 t6.481: M 0,0000 (curiosidad de clase 0,0700), botiquín ign. 1,000 / cuánto 1,000 / sabe —; d1·11 t9.481: M 0,0000 (curiosidad de clase 0,0730), botiquín ign. 1,000 / cuánto 1,000 / sabe —.

(GIF: en el día 1 no hay ningún uso firme del botiquín (dos "al menos" por asiento y un corte): no hay GIF que hacer.)

## F5 · Créditos del humo

Plataforma: 0,1089 USD en 1 partidas; acumulado de la séptima: 42,0106 USD. Consola de Anthropic: 0. Saldos no consultados.

## Punto 4 · La latencia de P7-10 y P7-14b (solo describir)

`latencia_P7_29b.py` -> `P7_29b_latencia.json`: los 640 diarios de los dos campos (4 brazos × 20 días × 2 series × 2 asientos cada uno) con la misma guarda (`RADIOGRAFIA.ms` del diario: el tiempo de `decide` de cada tic, `policy_cortex.py:511-618`; pasos listos bloqueados sin agente a la vista en la casilla del paso). El diario sí lo permite medir: el tiempo se apuntó en todos los campos; nadie lo había mirado.

| campo · brazo · bloque | vidas | ms mediana (media de vidas) | ms p95 (media · máx) | ms máx | tics por encima del tic | bloqueados sin cuerpo (media) | vidas con p95 > 20 ms · con sin-cuerpo > 5 % | muertas · antes del tic 4.000 · por rival | tic de muerte (mediana) | puesto medio |
|---|---:|---:|---|---:|---:|---:|---|---|---:|---:|
| P7-10 · APRENDE · dias 1-5 | 20 | 1,81 | 6,5 · 8,8 | 35,1 | 0,00 % | 0,48 % | 0 · 0 | 14 · 1 · 7 | 13.068 | 6,10 |
| P7-10 · APRENDE · dias 16-20 | 20 | 2,79 | 8,9 · 14,1 | 54,8 | 0,00 % | 0,23 % | 0 · 0 | 16 · 0 · 8 | 13.222 | 6,05 |
| P7-10 · APRENDE · todos | 80 | 3,06 | 8,8 · 25,3 | 77,9 | 0,00 % | 0,37 % | 2 · 0 | 64 · 1 · 28 | 12.864 | 5,91 |
| P7-10 · BORRADO · dias 1-5 | 20 | 1,76 | 7,2 · 10,7 | 53,3 | 0,00 % | 0,42 % | 0 · 0 | 12 · 0 · 4 | 13.404 | 4,30 |
| P7-10 · BORRADO · dias 16-20 | 20 | 2,11 | 7,0 · 13,5 | 46,7 | 0,00 % | 0,49 % | 0 · 0 | 15 · 1 · 4 | 14.448 | 4,80 |
| P7-10 · BORRADO · todos | 80 | 2,05 | 7,1 · 13,9 | 72,5 | 0,00 % | 0,36 % | 0 · 0 | 54 · 2 · 19 | 13.956 | 4,66 |
| P7-10 · SUELO · dias 1-5 | 20 | 1,45 | 5,8 · 8,8 | 29,0 | 0,00 % | 0,47 % | 0 · 0 | 13 · 0 · 3 | 13.920 | 3,75 |
| P7-10 · SUELO · dias 16-20 | 20 | 1,93 | 6,7 · 10,4 | 74,4 | 0,00 % | 0,28 % | 0 · 0 | 13 · 0 · 4 | 11.996 | 5,80 |
| P7-10 · SUELO · todos | 80 | 1,98 | 6,5 · 20,2 | 74,4 | 0,00 % | 0,33 % | 1 · 1 | 55 · 0 · 14 | 12.912 | 4,70 |
| P7-10 · TECHO · dias 1-5 | 20 | 1,00 | 3,8 · 6,9 | 32,2 | 0,00 % | 0,22 % | 0 · 0 | 16 · 0 · 4 | 12.912 | 4,75 |
| P7-10 · TECHO · dias 16-20 | 20 | 1,29 | 4,0 · 5,0 | 39,3 | 0,00 % | 0,17 % | 0 · 0 | 11 · 0 · 1 | 14.040 | 3,45 |
| P7-10 · TECHO · todos | 80 | 1,23 | 3,8 · 6,9 | 51,4 | 0,00 % | 0,15 % | 0 · 0 | 55 · 1 · 14 | 13.008 | 4,36 |
| P7-14b · APRENDE · dias 1-5 | 20 | 3,04 | 12,0 · 22,7 | 126,9 | 0,04 % | 0,44 % | 2 · 0 | 13 · 0 · 7 | 12.696 | 5,70 |
| P7-14b · APRENDE · dias 16-20 | 20 | 3,83 | 12,5 · 23,6 | 84,8 | 0,01 % | 0,11 % | 1 · 0 | 16 · 0 · 3 | 12.210 | 6,85 |
| P7-14b · APRENDE · todos | 80 | 3,75 | 12,9 · 30,1 | 126,9 | 0,02 % | 0,28 % | 7 · 0 | 58 · 4 · 19 | 12.780 | 5,59 |
| P7-14b · BORRADO · dias 1-5 | 20 | 2,48 | 9,7 · 18,7 | 68,8 | 0,01 % | 0,20 % | 0 · 0 | 13 · 0 · 2 | 12.864 | 4,10 |
| P7-14b · BORRADO · dias 16-20 | 20 | 2,59 | 9,7 · 13,9 | 51,0 | 0,00 % | 0,31 % | 0 · 0 | 11 · 0 · 3 | 14.341 | 4,35 |
| P7-14b · BORRADO · todos | 80 | 2,84 | 10,1 · 26,7 | 93,1 | 0,02 % | 0,31 % | 3 · 0 | 49 · 2 · 11 | 12.936 | 4,36 |
| P7-14b · ESPERANZA · dias 1-5 | 20 | 3,07 | 10,1 · 23,5 | 64,4 | 0,01 % | 0,24 % | 1 · 0 | 14 · 0 · 4 | 13.164 | 5,20 |
| P7-14b · ESPERANZA · dias 16-20 | 20 | 3,18 | 8,6 · 14,2 | 82,6 | 0,00 % | 0,11 % | 0 · 0 | 16 · 0 · 7 | 12.732 | 6,70 |
| P7-14b · ESPERANZA · todos | 80 | 3,11 | 9,7 · 29,3 | 82,6 | 0,01 % | 0,18 % | 2 · 0 | 57 · 2 · 19 | 13.008 | 5,34 |
| P7-14b · TECHO · dias 1-5 | 20 | 1,68 | 4,9 · 7,7 | 33,3 | 0,00 % | 0,34 % | 0 · 0 | 12 · 0 · 3 | 12.816 | 4,05 |
| P7-14b · TECHO · dias 16-20 | 20 | 1,93 | 5,6 · 10,5 | 22,4 | 0,00 % | 0,17 % | 0 · 0 | 14 · 0 · 9 | 13.848 | 4,90 |
| P7-14b · TECHO · todos | 80 | 2,11 | 5,8 · 11,3 | 47,4 | 0,00 % | 0,22 % | 0 · 0 | 56 · 3 · 22 | 12.924 | 4,89 |

| campo · brazo | muertes tempranas (< 4.000) | de ellas, no pasan la guarda | p95 medio (ms) · bloqueados sin cuerpo (media) | el resto de vidas: no pasan la guarda · bloqueados sin cuerpo (media) |
|---|---:|---:|---|---|
| P7-10 · APRENDE | 1 | 0 | 4,5 · 2,04 % | 2 de 79 · 0,34 % |
| P7-10 · BORRADO | 2 | 0 | 5,8 · 0,00 % | 0 de 78 · 0,36 % |
| P7-10 · SUELO | 0 | 0 | — · — % | 2 de 80 · 0,33 % |
| P7-10 · TECHO | 1 | 0 | 2,6 · 0,00 % | 0 de 79 · 0,15 % |
| P7-14b · APRENDE | 4 | 0 | 10,7 · 0,97 % | 7 de 76 · 0,25 % |
| P7-14b · BORRADO | 2 | 0 | 6,3 · 0,00 % | 3 de 78 · 0,31 % |
| P7-14b · ESPERANZA | 2 | 0 | 5,7 · 1,25 % | 2 de 78 · 0,16 % |
| P7-14b · TECHO | 3 | 0 | 5,5 · 0,33 % | 0 de 77 · 0,21 % |

Vidas que no pasarían la guarda nueva (16 de 640):

| vida que no pasa la guarda | ms mediana · p95 · máx | bloqueados sin cuerpo | muerte |
|---|---|---:|---|
| P7-14b s1 d15 APRENDE asiento 11 | 4,4 · 30,1 · 56,6 | 0,00 % | sobrevive, puesto 2 |
| P7-14b s1 d6 ESPERANZA asiento 11 | 6,2 · 29,3 · 65,2 | 0,12 % | sobrevive, puesto 1 |
| P7-14b s2 d7 APRENDE asiento 10 | 5,5 · 27,9 · 73,0 | 0,10 % | tic 11.856, anillo, puesto 9 |
| P7-14b s1 d8 BORRADO asiento 11 | 3,8 · 26,7 · 76,0 | 0,27 % | tic 14.688, anillo, puesto 4 |
| P7-14b s1 d9 APRENDE asiento 11 | 4,3 · 25,7 · 68,1 | 0,04 % | sobrevive, puesto 1 |
| P7-10 s1 d15 APRENDE asiento 11 | 11,7 · 25,3 · 65,5 | 0,82 % | tic 12.528, rival, puesto 3 |
| P7-14b s1 d19 APRENDE asiento 10 | 15,7 · 23,6 · 84,8 | 0,04 % | tic 13.944, anillo, puesto 3 |
| P7-14b s1 d5 ESPERANZA asiento 10 | 4,1 · 23,5 · 64,4 | 1,02 % | tic 12.024, anillo, puesto 8 |
| P7-14b s2 d15 BORRADO asiento 10 | 4,5 · 22,8 · 93,1 | 0,35 % | tic 13.872, anillo, puesto 4 |
| P7-14b s2 d1 APRENDE asiento 11 | 8,2 · 22,7 · 126,9 | 0,44 % | sobrevive, puesto 2 |
| P7-10 s1 d12 APRENDE asiento 10 | 7,8 · 22,1 · 77,9 | 0,85 % | tic 12.347, rival, puesto 8 |
| P7-14b s1 d11 BORRADO asiento 10 | 10,4 · 21,8 · 64,3 | 0,05 % | tic 14.617, rival, puesto 4 |
| P7-14b s1 d1 APRENDE asiento 11 | 6,6 · 21,6 · 111,8 | 0,78 % | tic 14.640, anillo, puesto 5 |
| P7-10 s1 d15 SUELO asiento 10 | 7,7 · 20,2 · 41,0 | 0,12 % | tic 14.617, rival, puesto 6 |
| P7-14b s1 d14 APRENDE asiento 11 | 7,6 · 20,1 · 50,2 | 0,61 % | tic 12.096, anillo, puesto 7 |
| P7-10 s1 d13 SUELO asiento 10 | 0,7 · 3,9 · 16,6 | 7,56 % | tic 12.816, anillo, puesto 4 |

Lectura. En los dos campos APRENDE era el brazo más lento (lee el cuaderno y calcula la creencia; en P7-14b además pide), BORRADO el segundo y TECHO el más rápido, pero todos a 2-4 ms de mediana y 4-13 ms de p95: una décima parte del tic. Las vidas que no pasan la guarda nueva son por el p95 (hasta 30 ms), no por pasos bloqueados sin cuerpo (1 vida de 640 pasa del 5 %; la media es 0,2-0,4 %, frente al 32 % de APRENDE en los días 16-20 de P7-24). Las muertes tempranas de APRENDE son 1 y 4, todas con la guarda limpia, y la fracción de bloqueados sin cuerpo en ellas no es mayor que en el resto. Por tanto, lo que separaba a APRENDE de BORRADO en P7-10 y P7-14b no puede atribuirse a la latencia; sigue siendo lo que dijeron esos informes. La latencia que rompe aparece con el recuerdo por parecido (P7-22/23) sobre cuadernos de 20-30 recuerdos (P7-24, días 11-20).

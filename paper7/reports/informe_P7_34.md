# P7-34 · El campo de lo inútil

*10-oct-2026. Plataforma: 11,7878 USD en 120 partidas (créditos de la plataforma, por el sidecar de Bedrock); consola de Anthropic: 0. Acumulado del siete:
52,9290 + 11,7878 = 64,7168 USD de plataforma (saldos no consultados). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final; cuerpo y congelados sin tocar.
Sello: `SELLO_P7_34.md` (commit `65e7354`, antes de pedir ninguna partida). Piezas: las de P7-33 (`nace_P7_33.py` = `a56fd98d6148b161a1c07cec9b6ebbfb`, `policy_pareja_P7_33.py`) con el arreglo del paso 0 en
`nace_P7_29.py` (= `f8b85c6f61257b09ae3c1d961382f7e6`). Scripts: `lanza_P7_34.py`, `corre_P7_34.sh`, `freno_P7_34.py`, `analiza_P7_34.py` → `P7_34_datos.json`, `sello_P7_34.py` → `P7_34_sello.json`,
`figuras_P7_34.py`, `gif_P7_34.py`, `escribe_informe_P7_34.py` (este informe; ninguna cifra a mano). Diarios en `paintball/runs/P734_*` (fuera de git).*

## Paso 0 · El arreglo del descuadre de fotos

El descuadre «N fotos para N+1 candidatos» (marcado como `P7_error` por `nace_P7_29`) no venía de la pieza de las cuatro cosas: la pieza congelada del seis `arreglos_P6_8b._cands`
(`cantera/paper6/arreglos_P6_8b.py:134-140`), que `policy_pareja11.run` aplica DESPUÉS de las del siete (`policy_pareja11.py:53`), esconde `coger` cuando la mochila está llena
(registro `llena8`) por FUERA del envoltorio del siete; los nombres de los candidatos se tomaban antes y las fotos por índice (`_P29_curioso`, `_P29_usa`) se corrían un sitio en
esos tics. Ya ocurría en P7-30 (d10 de APRENDE: 3 marcas por vida, el tope de 3 que escribe el diario). Arreglo en `nace_P7_29.decidir`: se envuelve lo que haya en `D.candidatos`
en el momento de decidir y los nombres se toman de la lista final (el patrón de `policy_cortex.decidir`). Comprobado antes de jugar: la réplica de la vida d1 a10 del humo de P7-33
da 0 descuadres y 11.130 / 11.130 decisiones iguales al diario; F1 de P7-33 repetida con el arreglo, idéntica (todo apagado = A4: 1.007.274 igual · 2 difiere; TECHO con oído y
ley: 1.007.078 igual · 198 difiere en 6 vidas); F2 de P7-33 repetida, idéntica en todas las medidas (cuaderno vacío: k = 0 y cura imaginada 0; tres redes sin efecto: creencia 0,0,
ignorancia 0,21-0,27, `ir_curioso` a la red 0/0/0/115). En el campo: 0 errores de fotos en 238 vidas.

## El diseño y el freno

Las piezas de P7-33 tal como quedaron; tres brazos (TECHO, APRENDE, BORRADO) de la misma imagen (`Dockerfile.pareja_P7_34`); pedir corregido y lo dado entregado; ojos compartidos
apagados; 20 días; la misma semilla para los tres brazos cada día; dos series una detrás de otra (la 2 en orden inverso). Semillas k = 201-220 (`semillas_P7_34.json`,
declaradas antes de jugar): serie 1 41311445, 41416174, …, 43301296. Guardas de P7-30 (latencia marca y sigue; para solo al 10 % sobre el tic o al 5 % bloqueados sin
cuerpo; disco; red; cortes).

Freno (días 1-3 de APRENDE, serie 1; `P7_34_freno.json`): (a) el cuaderno viaja y se lee: sí; (b) tocan alguna de las cuatro cosas: 6 de 6 vidas (d1 a10, d1 a11, d2 a10, d2 a11, d3 a10, d3 a11): sí;
(c) sube la creencia de alguna cosa útil: d3 a11 racion: 12.1087 -> 12.4847: sí; (d) errores de fotos: d1 a10 0, d1 a11 0, d2 a10 0, d2 a11 0, d3 a10 0, d3 a11 0: sí. **FRENO: PASA.**

| vida | puesto | cuaderno leído | recuerdos arranque → cierre | orden de contacto | creencia útil al cerrar (botiquín / ración) | errores de fotos | guarda (mediana ms · sobre el tic · sin cuerpo) |
|---|---:|---|---|---|---|---:|---|
| d1 a10 | 2 | no | 0 → 10 | red, botiquin, camuflaje, racion | 11,4 / 6,0 | 0 | 2,8 · 0,00 % · 0,06 % |
| d1 a11 | 1 | no | 0 → 9 | racion, botiquin | 11,4 / 12,2 | 0 | 3,8 · 0,01 % · 0,00 % |
| d2 a10 | 1 | sí | 10 → 14 | racion, camuflaje | 11,2 / 5,6 | 0 | 8,7 · 4,61 % · 0,04 % |
| d2 a11 | 2 | sí | 9 → 15 | racion, red, botiquin | 11,1 / 12,1 | 0 | 3,4 · 0,00 % · 0,15 % |
| d3 a10 | 2 | sí | 14 → 16 | botiquin | 11,1 / 5,5 | 0 | 4,5 · 0,01 % · 0,17 % |
| d3 a11 | 4 | sí | 15 → 20 | camuflaje, botiquin, red, racion | 10,9 / 12,5 | 0 | 1,6 · 0,00 % · 0,14 % |

## El campo

238 vidas leídas de 120 partidas; partidas con corte: 2 (s2 d6 TECHO, s2 d8 TECHO); partidas marcadas por la guarda de latencia: 21 (s1 d2 APRENDE, s1 d2 BORRADO, s1 d3 BORRADO, s1 d5 BORRADO, s1 d7 BORRADO, s1 d10 APRENDE, s1 d10 BORRADO, s1 d13 APRENDE, s1 d18 APRENDE, s1 d20 BORRADO, s2 d2 APRENDE, s2 d2 BORRADO, s2 d3 APRENDE, s2 d7 BORRADO, s2 d11 BORRADO, s2 d12 BORRADO, s2 d15 BORRADO, s2 d16 APRENDE, s2 d16 BORRADO, s2 d18 BORRADO, s2 d20 BORRADO);
vidas marcadas: 24 (s1 d10 APRENDE a10 (1,35 % · 0,28 %); s1 d10 BORRADO a11 (1,32 % · 0,19 %); s1 d13 APRENDE a11 (1,12 % · 0,49 %); s1 d18 APRENDE a10 (1,42 % · 0,08 %); s1 d20 BORRADO a10 (4,24 % · 0,00 %); s1 d2 APRENDE a10 (4,61 % · 0,04 %); s1 d2 BORRADO a10 (1,67 % · 0,14 %); s1 d2 BORRADO a11 (3,20 % · 0,05 %); s1 d3 BORRADO a10 (1,71 % · 0,00 %); s1 d5 BORRADO a10 (6,74 % · 0,06 %); s1 d5 BORRADO a11 (1,95 % · 0,00 %); s1 d7 BORRADO a11 (4,78 % · 0,19 %); s2 d11 BORRADO a11 (2,35 % · 0,95 %); s2 d12 BORRADO a10 (5,54 % · 3,27 %); s2 d15 BORRADO a10 (2,32 % · 0,06 %); s2 d16 APRENDE a10 (3,35 % · 1,18 %); s2 d16 BORRADO a11 (7,12 % · 0,00 %); s2 d18 BORRADO a10 (4,86 % · 0,00 %); s2 d18 BORRADO a11 (3,56 % · 0,00 %); s2 d20 BORRADO a11 (4,09 % · 0,07 %); s2 d2 APRENDE a10 (2,24 % · 0,07 %); s2 d2 BORRADO a10 (3,96 % · 1,82 %); s2 d3 APRENDE a10 (7,43 % · 4,29 %); s2 d7 BORRADO a11 (15,98 % · 0,24 %)).

### Las cuatro cosas por brazo y bloque de días

(«Pruebas» del botiquín y la ración: huellas de uso; de la red y el camuflaje: ventanas de 10 s. «Usos»: aperturas del canal `P7_nace_uso` (TECHO nace sabiendo y no lo tiene: sus bajadas de unidades van juntas en la última cifra). «Sueltas»: bajadas que no son usos.)

| brazo | días | vidas | botiquin: vidas con contacto · cogidas/vida · pruebas (en calma) · usos · sueltas | racion: vidas con contacto · cogidas/vida · pruebas (en calma) · usos · sueltas | red: vidas con contacto · cogidas/vida · pruebas (en calma) · usos · sueltas | camuflaje: vidas con contacto · cogidas/vida · pruebas (en calma) · usos · sueltas |
|---|---|---:|---|---|---|---|
| TECHO | 1-5 | 20 | 17 · 2,10 · 0 (0) · — · 35 | 12 · 2,15 · 0 (0) · — · 36 | 4 · 0,20 · 0 (0) · — · 0 | 7 · 0,35 · 0 (0) · — · 1 |
| TECHO | 6-10 | 18 | 17 · 1,72 · 0 (0) · — · 23 | 9 · 2,72 · 0 (0) · — · 41 | 6 · 0,39 · 0 (0) · — · 0 | 5 · 0,28 · 0 (0) · — · 0 |
| TECHO | 11-15 | 20 | 18 · 2,00 · 0 (0) · — · 34 | 13 · 1,85 · 0 (0) · — · 31 | 7 · 0,35 · 0 (0) · — · 0 | 6 · 0,30 · 0 (0) · — · 0 |
| TECHO | 16-20 | 20 | 20 · 2,85 · 0 (0) · — · 50 | 11 · 2,10 · 0 (0) · — · 36 | 3 · 0,15 · 0 (0) · — · 0 | 4 · 0,35 · 0 (0) · — · 3 |
| BORRADO | 1-5 | 20 | 12 · 0,90 · 31 (13) · 31 · 1 | 6 · 1,00 · 14 (4) · 14 · 3 | 6 · 0,30 · 6 (4) · 0 · 0 | 6 · 0,30 · 5 (3) · 0 · 0 |
| BORRADO | 6-10 | 20 | 15 · 1,00 · 23 (2) · 23 · 3 | 9 · 1,10 · 13 (4) · 14 · 4 | 8 · 0,40 · 7 (6) · 0 · 0 | 7 · 0,35 · 7 (6) · 0 · 0 |
| BORRADO | 11-15 | 20 | 16 · 1,10 · 29 (2) · 30 · 1 | 9 · 1,05 · 8 (0) · 8 · 2 | 9 · 0,45 · 9 (8) · 0 · 0 | 8 · 0,50 · 9 (9) · 0 · 3 |
| BORRADO | 16-20 | 20 | 13 · 0,90 · 25 (6) · 25 · 1 | 9 · 1,45 · 18 (1) · 18 · 4 | 7 · 0,35 · 7 (5) · 0 · 0 | 8 · 0,40 · 5 (3) · 0 · 0 |
| APRENDE | 1-5 | 20 | 16 · 1,30 · 31 (11) · 32 · 3 | 15 · 3,35 · 43 (3) · 44 · 13 | 8 · 0,45 · 7 (6) · 0 · 0 | 7 · 0,40 · 6 (3) · 0 · 1 |
| APRENDE | 6-10 | 20 | 14 · 1,35 · 33 (7) · 34 · 5 | 13 · 2,20 · 28 (1) · 28 · 9 | 8 · 0,45 · 8 (7) · 0 · 0 | 8 · 0,40 · 8 (6) · 0 · 0 |
| APRENDE | 11-15 | 20 | 16 · 1,75 · 44 (11) · 45 · 7 | 12 · 2,15 · 22 (1) · 22 · 16 | 8 · 0,45 · 8 (7) · 0 · 0 | 8 · 0,40 · 8 (7) · 0 · 0 |
| APRENDE | 16-20 | 20 | 14 · 1,65 · 32 (9) · 35 · 15 | 15 · 5,55 · 30 (3) · 31 · 68 | 7 · 0,45 · 8 (6) · 0 · 1 | 9 · 0,55 · 10 (8) · 0 · 2 |

### Lo que lleva cada criatura de APRENDE en el cuaderno (al cerrar los días 5, 10, 15 y 20)

| criatura | día | botiquin: recuerdos (firmes · «al menos» · cortes · «no hizo nada») · creencia · ignorancia · ganas | racion: recuerdos (firmes · «al menos» · cortes · «no hizo nada») · creencia · ignorancia · ganas | red: recuerdos (firmes · «al menos» · cortes · «no hizo nada») · creencia · ignorancia · ganas | camuflaje: recuerdos (firmes · «al menos» · cortes · «no hizo nada») · creencia · ignorancia · ganas |
|---|---|---|---|---|---|
| s1 a10 | 5 | 10 (0 · 6 · 4 · —) · 12,6 · 0,09 · 0,141 | 8 (0 · 8 · 0 · —) · 5,8 · 0,12 · 1,258 | 2 (2 · 0 · 0 · 2) · 0,0 · 0,36 · 0,000 | 2 (2 · 0 · 0 · 2) · 0,0 · 0,35 · 0,000 |
| s1 a10 | 10 | 21 (0 · 9 · 12 · —) · 10,9 · 0,05 · 0,219 | 19 (3 · 16 · 0 · —) · 5,7 · 0,06 · 0,613 | 4 (4 · 0 · 0 · 4) · 0,0 · 0,23 · 0,000 | 4 (4 · 0 · 0 · 4) · 0,0 · 0,21 · 0,000 |
| s1 a10 | 15 | 39 (2 · 14 · 23 · —) · 35,0 · 0,03 · 0,257 | 23 (6 · 17 · 0 · —) · 8,3 · 0,06 · 0,511 | 7 (7 · 0 · 0 · 7) · 0,0 · 0,15 · 0,000 | 6 (6 · 0 · 0 · 6) · 0,0 · 0,17 · 0,000 |
| s1 a10 | 20 | 55 (4 · 17 · 34 · —) · 37,8 · 0,02 · 0,590 | 36 (14 · 22 · 0 · —) · 11,2 · 0,04 · 1,171 | 9 (9 · 0 · 0 · 9) · 0,0 · 0,14 · 0,000 | 10 (10 · 0 · 0 · 10) · 0,0 · 0,11 · 0,000 |
| s1 a11 | 5 | 5 (0 · 4 · 1 · —) · 15,6 · 0,17 · 0,230 | 13 (6 · 7 · 0 · —) · 8,7 · 0,08 · 1,099 | 3 (3 · 0 · 0 · 3) · 0,0 · 0,23 · 0,000 | 1 (1 · 0 · 0 · 1) · 0,0 · 0,51 · 0,000 |
| s1 a11 | 10 | 13 (1 · 5 · 7 · —) · 31,0 · 0,07 · 0,470 | 21 (12 · 9 · 0 · —) · 13,0 · 0,05 · 1,089 | 3 (3 · 0 · 0 · 3) · 0,0 · 0,28 · 0,000 | 3 (3 · 0 · 0 · 3) · 0,0 · 0,27 · 0,000 |
| s1 a11 | 15 | 21 (2 · 9 · 10 · —) · 35,9 · 0,05 · 0,598 | 28 (14 · 14 · 0 · —) · 13,2 · 0,05 · 1,137 | 5 (5 · 0 · 0 · 5) · 0,0 · 0,21 · 0,000 | 5 (5 · 0 · 0 · 5) · 0,0 · 0,21 · 0,000 |
| s1 a11 | 20 | 33 (2 · 14 · 17 · —) · 33,2 · 0,03 · 0,346 | 30 (14 · 16 · 0 · —) · 12,9 · 0,05 · 1,352 | 7 (7 · 0 · 0 · 6) · 3,3 · 0,16 · 0,001 | 6 (6 · 0 · 0 · 6) · 0,0 · 0,21 · 0,057 |
| s2 a10 | 5 | 10 (2 · 4 · 4 · —) · 36,4 · 0,08 · 0,314 | 16 (14 · 2 · 0 · —) · 13,7 · 0,06 · 0,998 | 0 (0 · 0 · 0 · 0) · — · 1,00 · 0,000 | 2 (2 · 0 · 0 · 2) · 0,0 · 0,28 · 0,000 |
| s2 a10 | 10 | 13 (2 · 5 · 6 · —) · 33,7 · 0,08 · 0,407 | 20 (16 · 4 · 0 · —) · 13,6 · 0,06 · 1,129 | 4 (4 · 0 · 0 · 4) · 0,0 · 0,20 · 0,000 | 4 (4 · 0 · 0 · 4) · 0,0 · 0,20 · 0,000 |
| s2 a10 | 15 | 14 (3 · 5 · 6 · —) · 36,2 · 0,09 · 0,777 | 22 (16 · 6 · 0 · —) · 13,2 · 0,07 · 1,603 | 6 (6 · 0 · 0 · 6) · 0,0 · 0,17 · 0,024 | 7 (7 · 0 · 0 · 6) · 6,4 · 0,14 · 0,060 |
| s2 a10 | 20 | 16 (3 · 7 · 6 · —) · 33,5 · 0,09 · 0,488 | 28 (16 · 12 · 0 · —) · 12,8 · 0,06 · 1,468 | 9 (9 · 0 · 0 · 9) · 0,0 · 0,12 · 0,037 | 9 (9 · 0 · 0 · 8) · 4,5 · 0,12 · 0,021 |
| s2 a11 | 5 | 5 (0 · 2 · 3 · —) · 11,5 · 0,17 · 0,234 | 6 (3 · 2 · 1 · —) · 5,6 · 0,12 · 0,870 | 2 (2 · 0 · 0 · 2) · 0,0 · 0,35 · 0,000 | 1 (1 · 0 · 0 · 1) · 0,0 · 0,52 · 0,000 |
| s2 a11 | 10 | 16 (0 · 12 · 4 · —) · 22,7 · 0,06 · 0,433 | 11 (3 · 7 · 1 · —) · 6,8 · 0,08 · 1,343 | 4 (4 · 0 · 0 · 4) · 0,0 · 0,22 · 0,000 | 3 (3 · 0 · 0 · 3) · 0,0 · 0,29 · 0,000 |
| s2 a11 | 15 | 33 (0 · 18 · 15 · —) · 24,7 · 0,03 · 0,568 | 19 (10 · 8 · 1 · —) · 12,8 · 0,06 · 1,301 | 5 (5 · 0 · 0 · 4) · 4,6 · 0,21 · 0,027 | 4 (4 · 0 · 0 · 4) · 0,0 · 0,27 · 0,102 |
| s2 a11 | 20 | 35 (0 · 20 · 15 · —) · 23,5 · 0,04 · 0,480 | 28 (15 · 12 · 1 · —) · 13,7 · 0,04 · 1,385 | 6 (6 · 0 · 0 · 5) · 3,4 · 0,20 · 0,007 | 7 (7 · 0 · 0 · 7) · 0,0 · 0,17 · 0,080 |

### Puesto, muerte, latencia y agua

| brazo | días | vidas (en puesto) | puesto medio | mueren · tic de la muerte (mediana) | ms por decisión: mediana · p95 (máx entre vidas) | sobre el tic (máx) | bloqueados sin cuerpo (máx) | vidas marcadas | avisos oídos · casillas cerradas (máx) · tics con `blocked` por vida (cualquier causa) |
|---|---|---|---:|---|---|---:|---:|---:|---|
| TECHO | 1-5 | 20 (20) | 5,75 | 18 · 12.936 | 1,04 · 13,6 | 0,06 % | 0,21 % | 0 | 20 · 25 · 679,2 |
| TECHO | 6-10 | 18 (16) | 5,88 | 10 · 11.657 | 1,64 · 12,8 | 0,01 % | 1,89 % | 0 | 16 · 25 · 1.432,7 |
| TECHO | 11-15 | 20 (20) | 5,25 | 14 · 12.841 | 1,46 · 11,6 | 0,03 % | 0,23 % | 0 | 20 · 25 · 1.254,8 |
| TECHO | 16-20 | 20 (20) | 5,45 | 18 · 13.866 | 1,17 · 18,4 | 0,16 % | 1,78 % | 0 | 20 · 25 · 221,5 |
| BORRADO | 1-5 | 20 (20) | 7,60 | 15 · 11.496 | 3,66 · 45,5 | 6,74 % | 2,64 % | 6 | 18 · 25 · 65,7 |
| BORRADO | 6-10 | 20 (20) | 5,90 | 16 · 12.700 | 3,91 · 55,0 | 15,98 % | 0,43 % | 3 | 19 · 25 · 311,9 |
| BORRADO | 11-15 | 20 (20) | 7,60 | 16 · 11.914 | 3,56 · 43,3 | 5,54 % | 3,27 % | 3 | 18 · 25 · 126,5 |
| BORRADO | 16-20 | 20 (20) | 7,15 | 14 · 11.594 | 3,90 · 44,8 | 7,12 % | 1,31 % | 5 | 20 · 25 · 43,4 |
| APRENDE | 1-5 | 20 (20) | 4,80 | 11 · 12.744 | 3,65 · 47,0 | 7,43 % | 4,29 % | 3 | 20 · 25 · 396,5 |
| APRENDE | 6-10 | 20 (20) | 4,90 | 12 · 12.672 | 3,76 · 27,6 | 1,35 % | 0,36 % | 1 | 19 · 25 · 450,2 |
| APRENDE | 11-15 | 20 (20) | 5,40 | 15 · 13.800 | 3,29 · 27,3 | 1,12 % | 0,70 % | 1 | 18 · 25 · 137,9 |
| APRENDE | 16-20 | 20 (20) | 5,45 | 13 · 12.243 | 3,33 · 32,1 | 3,35 % | 1,18 % | 2 | 20 · 25 · 208,9 |

## El sello, evaluado una vez

### Primera cuenta: con todas las vidas (las partidas con corte, fuera de los puestos)

| | regla | resultado | pasa |
|---|---|---|---|
| I1 | prueba lo inútil (día 5: ≥ 1 prueba de red y ≥ 1 de camuflaje en las 4) | s1 a10: red 2, camuflaje 2; s1 a11: red 3, camuflaje 1; s2 a10: red 0, camuflaje 2; s2 a11: red 2, camuflaje 1 | NO |
| I2 | deja de quererlo (días 11-20: inútil/vida de APRENDE ≤ ¼ de TECHO y ≤ ¼ de su útil) | APRENDE inútil 0,925 por vida (n = 40); TECHO inútil 0,575 (n = 40); APRENDE útil 5,550 | NO |
| I3 | lo recuerda débil (día 20: intensidad media inútil < ½ útil) | útil 1,1963 · inútil 1,1636; por criatura: s1 a10: útil 1,177 (57), inútil 1,144 (19); s1 a11: útil 1,198 (46), inútil 1,150 (13); s2 a10: útil 1,186 (38), inútil 1,230 (18); s2 a11: útil 1,226 (47), inútil 1,113 (13) | NO |
| I4 | lo olvidado vuelve a parecer nuevo (≥ 2 criaturas con una prueba tras ≥ 5 días sin tocar la cosa) | 2 criaturas: s1 a10: ninguna; s1 a11: red día 11; s2 a10: ninguna; s2 a11: red día 18 | sí |
| I5 | lo útil sigue (botiquín dentro ≥ 30 el día 20 en ≥ 3 de 4; y no se hunde frente a BORRADO) | creencia día 20: s1 a10 37,8, s1 a11 33,2, s2 a10 33,5, s2 a11 23,5 → 3 llegan a 30; APRENDE − BORRADO días 1-5 -2,80 ± 1,22 (n = 20), días 16-20 -1,70 ± 1,41 (n = 20); ee de la diferencia 1,87; se hunde: False | sí |
| I6 | lo curioso en calma (≥ 80 % de las pruebas de red y camuflaje de APRENDE en calma) | 50 de 64 aperturas en calma (78,1 %) | NO |

### Segunda cuenta: sin las partidas marcadas por la guarda

| | regla | resultado | pasa |
|---|---|---|---|
| I1 | prueba lo inútil (día 5: ≥ 1 prueba de red y ≥ 1 de camuflaje en las 4) | s1 a10: red 2, camuflaje 1; s1 a11: red 2, camuflaje 1; s2 a10: red 0, camuflaje 2; s2 a11: red 2, camuflaje 1 | NO |
| I2 | deja de quererlo (días 11-20: inútil/vida de APRENDE ≤ ¼ de TECHO y ≤ ¼ de su útil) | APRENDE inútil 0,941 por vida (n = 34); TECHO inútil 0,575 (n = 40); APRENDE útil 6,147 | NO |
| I3 | lo recuerda débil (día 20: intensidad media inútil < ½ útil) | útil 1,1963 · inútil 1,1636; por criatura: s1 a10: útil 1,177 (57), inútil 1,144 (19); s1 a11: útil 1,198 (46), inútil 1,150 (13); s2 a10: útil 1,186 (38), inútil 1,230 (18); s2 a11: útil 1,226 (47), inútil 1,113 (13) | NO |
| I4 | lo olvidado vuelve a parecer nuevo (≥ 2 criaturas con una prueba tras ≥ 5 días sin tocar la cosa) | 0 criaturas: s1 a10: ninguna; s1 a11: ninguna; s2 a10: ninguna; s2 a11: ninguna | NO |
| I5 | lo útil sigue (botiquín dentro ≥ 30 el día 20 en ≥ 3 de 4; y no se hunde frente a BORRADO) | creencia día 20: s1 a10 37,8, s1 a11 33,2, s2 a10 33,5, s2 a11 23,5 → 3 llegan a 30; APRENDE − BORRADO días 1-5 -1,60 ± 1,97 (n = 10), días 16-20 -1,90 ± 2,27 (n = 10); ee de la diferencia 3,01; se hunde: False | sí |
| I6 | lo curioso en calma (≥ 80 % de las pruebas de red y camuflaje de APRENDE en calma) | 43 de 56 aperturas en calma (76,8 %) | NO |

Cambian entre las dos cuentas: I4. Sin predicción, solo medida: APRENDE − BORRADO en puesto, los 20 días: -1,93 ± 0,62 (n = 80).


## Lectura

(i) **Lo inútil se prueba, y en calma, pero no en las cuatro antes del día 5 (I1 no pasa)**: tres criaturas prueban la red y el camuflaje en los días 1-5; la cuarta (s2 a10) no prueba la red porque no la toca (s2 a10: 0 redes cogidas en los días 1-5); el camuflaje lo prueban las cuatro. En los 20 días, las 4 criaturas acumulan 63 recuerdos de red y camuflaje, 60 de ellos «no hizo nada». (ii) **Lo curioso en calma, casi (I6: 78,1 %, el umbral era 80)**: de 64 aperturas de red y camuflaje, 50 en calma; las 14 restantes, 14 con un rival a 4 casillas o menos, 0 con fuego, 1 con la vida por debajo de 30. El botiquín y la ración, al revés: de sus 271 aperturas en APRENDE, 46 en calma. (iii) **No deja de quererlo (I2 no pasa)**: en los días 11-20 APRENDE coge 0,93 redes + camuflajes por vida, MÁS que TECHO (0,57), y no la cuarta parte de lo útil (5,55); las ganas (k) de red y camuflaje están en 0,000 casi siempre (tabla del cuaderno), así que lo que las coge no es la curiosidad de clase: `ir_curioso` con el paso listo es el 1,5 % (mediana) en APRENDE; la lectura más sencilla (mía, no comprobada en este informe) es que las coge el cuerpo al pasar por encima (`coger`, que no sabe de clases) y, de vez en cuando, la curiosidad que vuelve cuando el olvido sube la ignorancia (I4); separarlo pide mirar qué candidato se elige en cada cogida. (iv) **Lo recuerda igual de fuerte, no más débil (I3 no pasa)**: intensidad media 1,164 en los recuerdos de red y camuflaje frente a 1,196 en los de botiquín y ración: la intensidad del cuaderno (`cuaderno_P7`) sale del cambio del malestar durante la prueba, no del efecto, y en 10 s de calma el malestar cambia lo mismo con una red puesta que con un botiquín usado. Un recuerdo de «no hizo nada» pesa en el cuaderno lo mismo que uno de curar 28 puntos; lo que los distingue es la creencia (0,0 en red y camuflaje en 5 de 8 cuadernos del día 20; s1 a11 red 3,3 con 1 recuerdo con efecto en el cuerpo, s2 a10 camuflaje 4,5 con 1 recuerdo con efecto en el cuerpo, s2 a11 red 3,4 con 1 recuerdo con efecto en el cuerpo: ventanas en las que la vida subió por otra causa). (v) **Lo olvidado vuelve a parecer nuevo (I4 pasa en la primera cuenta)**: s1 a11 prueba una red el día 11 tras cinco días sin tocarla, y s2 a11 el día 18; en la segunda cuenta I4 cae no porque aparezca un contacto, sino porque las partidas marcadas (s1 d10 y s2 d16 de APRENDE, marcadas por el OTRO asiento) salen de la ventana de cinco días y la regla, tal como está escrita, exige los cinco días presentes. (vi) **Lo útil sigue (I5 pasa)**: creencia del botiquín dentro el día 20 s1 a10 37,8, s1 a11 33,2, s2 a10 33,5, s2 a11 23,5 (3 de 4 llegan a 30); APRENDE − BORRADO en puesto -2,80 ± 1,22 en los días 1-5 y -1,70 ± 1,41 en los 16-20 (negativo = mejor puesto que BORRADO): la que recuerda no se hunde y queda por delante de la que borra los 20 días (-1,93 ± 0,62, n = 80). (vii) **Latencia**: vidas marcadas por brazo TECHO 0, BORRADO 17, APRENDE 7 (medianas de ms por decisión 1,21, 3,75, 3,56); la peor, s2 d7 BORRADO a11 con el 15,98 % sobre el tic, disparó la parada dura del lanzador (> 10 %) cuando la serie 2 ya estaba entera jugada y bajada: nada quedó sin jugar. La pieza de las cuatro cosas pesa más en BORRADO (cuaderno vacío cada día: más clases ignoradas, más `ir_curioso`, más fotos) que en APRENDE. (viii) **Oído y ley**: las 228 avisos de inundación oídos en 238 vidas, 25 casillas cerradas en cada una; ninguna vida con más del 5 % de pasos listos bloqueados sin cuerpo (máximo 4,29 %): el agua ya no bloquea a nadie. (ix) Dos cortes de la plataforma sin artefacto (s2 d6 y s2 d8 de TECHO, asiento 11, 0 líneas rescatadas): sus partidas salen de los puestos; 0 errores de fotos en las 238 vidas.
## Figuras y GIFs

- `P7_34_fig_cuatro.png`: creencia, ignorancia y ganas de las cuatro cosas por día (APRENDE, media de las criaturas con valor; BORRADO punteado). `P7_34_fig_cogidas.png`: cogidas de lo útil frente a lo inútil por día y brazo. `P7_34_fig_puesto.png`: el puesto por día en los tres brazos (`figuras_P7_34.py`, de `P7_34_datos.json`).
- `P7_34_gif_prueba_red.gif`: la criatura s1 a10 de APRENDE, día 1, prueba del red abierta en calma en el tic 593 (cierra en el 833); `P7_34_gif_uso_botiquin.gif`: la misma criatura, día 1, uso del botiquín abierto en peligro en el tic 11556 (rival_a_4). GIFs de los datos del diario (matplotlib), fuera de git; `gif_P7_34.py`, `P7_34_gif.json`.

## Gasto

Plataforma: 11,7878 USD en 120 partidas (0,0982 por partida; el humo de P7-33 costó 0,2740 en 3). Acumulado del siete: 64,7168 USD de plataforma. Consola de Anthropic: 0. Saldos no consultados.

# P7-46 · Banco (coste cero): lectura por prueba del campo P7-45 — EXPLORATORIO, SIN SELLO

*12-oct-2026. Banco sobre los 720 diarios de las tres series (P7-45); no se jugó ninguna partida. **Exploratorio: no hay sello, no hay predicción, no se evalúa nada; se cuenta y se
describe.** Motivo (Manel): SIN EMOCIÓN probó la mitad que APRENDE en lazo cerrado y las medidas por vida no comparan qué elige cada uno. BORRADO, solo como referencia.
Bolsa 1: 0 créditos hoy (acumulado del siete 1.185; saldo **228** créditos, página de la plataforma, 12-oct 06:47, dato de Manel). Bolsa 2: 0 $. Disco: 33 GB libres (sección 6).
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Scripts: `banco_P7_46.py` → `P7_46_datos.json` (720 vidas), `analiza_P7_46.py` → `P7_46_resumen.json`, `escribe_informe_P7_46.py`
(este informe; ninguna cifra a mano). Definiciones: «prueba» = huella `P7_huella` (ventana de prueba de una de las cuatro cosas, del congelado P7-33); «creencia» = `creencia_despues.cuerpo`
de esa huella (la creencia del cuerpo tras esa prueba); «calma / peligro» = el `peligro` de la apertura `P7_33_prueba` más cercana (≤ 24 tics) a la huella, tal como lo define el congelado
(calma = sin rival a 4, sin fuego, vida ≥ 30); «forzada» = `P7_41_azar` momento=forzada con su `fin`.*

## Sección 1 · SIN EMOCIÓN: forzadas que acaban y forzadas que caducan

349 forzadas en 120 vidas (2,91 por vida): acaban 101 (29 %), caducan 243 (70 %), sin fin (muerte o final de partida) 5. Las que acaban tardan
38 tics de media (ventana de 240).

| tipo | forzadas | acaban (cogida / usada) | caducan | sin fin (muerte o final) |
|---|---:|---:|---:|---:|
| ir | 247 | 83 | 159 | 5 |
| usar | 102 | 18 | 84 | 0 |

| objeto | forzadas | acaban | caducan |
|---|---:|---:|---:|
| botiquin | 133 | 43 | 90 |
| racion | 111 | 43 | 66 |
| red | 75 | 11 | 62 |
| camuflaje | 30 | 4 | 25 |

**Por qué caducan** (diagnóstico de la ventana, categorías excluyentes en este orden):
- **ir** (159 caducan): llega: el cuerpo no ofrece coger 93 (58 %); llega: zurrón lleno (hacer_sitio, sin coger) 61 (38 %); llega: coger ofrecido y no cogido 5 (3 %).
- **usar** (84 caducan): usar nunca ofrecido por el cuerpo 79 (94 %); usar elegido y no consumido 5 (6 %).
- En las forzadas de **usar** que caducan, el hp está a 100 en el 81 % de los tics (hp al abrir: 96 de media; en las que acaban usadas, 83): el cuerpo congelado no
  ofrece `usar_*` con la vida llena, y la moneda, que cae en cualquier tic con un consumible en el zurrón, lo pide sobre todo entonces.
- En las de **ir** que caducan, el destino estaba a 3,3 casillas al abrir (en las cogidas, 3,6): casi todas LLEGAN. La cogida de una forzada de ir depende del
  `recoger` del paso de llegada (`ir_azar` lleva `recoger`); si no cuaja, en la casilla el único camino es `coger`, y el cuerpo congelado lo construye con el PRIMER objeto de la
  casilla (`decisor_zs.py`, paso 5: `aqui[0]`) y la regla congelada del seis lo esconde si la previsión dice que la mochila no cambia (`arreglos_P6_8b`, registro `llena8`). En
  89 de las 93 ventanas «llega: el cuerpo no ofrece coger» hay registros `llena8` («prevision: la mochila no cambia»; 10616 en total); con el zurrón lleno de verdad el cuerpo ofrece `hacer_sitio_*`, que la forzada
  no reconoce. Es decir: la moneda manda ir, la criatura va, y al llegar la pieza SIN no sabe coger lo que fue a buscar. Se apunta como límite de la pieza `azar_P7_41` (no del
  cuerpo), a corregir si se vuelve a jugar SIN: la forzada debería terminar con el `recoger` de la llegada o pedir `hacer_sitio_*` / el `coger` del objeto forzado. Se propone, no se toca.
- De las 101 forzadas que acaban, 37 dejan una huella de prueba del mismo objeto dentro de la ventana + 240 tics (ir: 19 de 83; usar: 18 de 18): una forzada de ir que
  acaba en cogida no es todavía una prueba (la prueba de la red o el camuflaje empieza al ponérselos; la del botiquín, al usarlo).

## Sección 2 · Aprendizaje por prueba (botiquín y ración)

| variante | criaturas (o vidas) con pruebas de botiquín | pruebas de botiquín por criatura | creencia tras la 1.ª (n) | tras la 3.ª (n) | tras la 5.ª (n) | cambio medio por prueba ± ee (n pruebas) | primera prueba en la que llega a 25 (por criatura) |
|---|---:|---:|---|---|---|---|---|
| BORRADO valiente | 81 | 2,4 | 4,3 (81) | 5,7 (29) | 8,1 (6) | 3,96 ± 0,50 (195) | 10 de 81 vidas (k: 1, 1, 1, 2, 2, 2, 2, 3, 5, 8) |
| BORRADO prudente | 78 | 2,3 | 2,6 (78) | 8,2 (24) | 7,5 (8) | 4,64 ± 0,54 (180) | 10 de 78 vidas (k: 1, 1, 1, 2, 2, 3, 3, 4, 6, 8) |
| APRENDE valiente | 6 | 32,2 | 5,8 (6) | 6,6 (6) | 8,3 (6) | 0,76 ± 0,28 (193) | 23, 12, —, —, —, 30 |
| APRENDE prudente | 6 | 28,3 | 1,3 (6) | 8,5 (6) | 8,7 (6) | 0,67 ± 0,53 (170) | —, —, —, 11, 10, 17 |
| SIN EMOCIÓN | 6 | 9,7 | 5,7 (3) | 9,3 (3) | 9,3 (3) | 1,45 ± 1,03 (58) | —, 1, —, —, 10, — |

| variante | criaturas con pruebas de ración | pruebas por criatura | creencia tras la 1.ª (n) | tras la 3.ª (n) | tras la 5.ª (n) | cambio medio por prueba ± ee (n) |
|---|---:|---:|---|---|---|---|
| BORRADO valiente | 57 | 1,9 | 6,6 (57) | 10,3 (13) | 10,8 (3) | 3,56 ± 0,33 (111) |
| BORRADO prudente | 56 | 2,5 | 4,5 (56) | 8,9 (20) | 11,6 (11) | 2,86 ± 0,23 (141) |
| APRENDE valiente | 6 | 20,3 | 6,7 (6) | 10,2 (6) | 10,3 (6) | 0,56 ± 0,25 (122) |
| APRENDE prudente | 6 | 30,0 | 4,8 (6) | 7,0 (6) | 8,4 (6) | 0,41 ± 0,12 (180) |
| SIN EMOCIÓN | 6 | 15,5 | 7,9 (6) | 10,5 (4) | 9,5 (4) | 0,70 ± 0,23 (93) |

## Sección 3 · Elección: a qué va cada prueba, por tramo de días

| variante | d1-5: pruebas · a red+cam | d6-10 | d11-15 | d16-20 | todas: pruebas · a red+cam · a botiquín+ración (b · r · red · cam) |
|---|---|---|---|---|---|
| TECHO | 0 · — | 0 · — | 0 · — | 0 · — | 0 · — · — (0 · 0 · 0 · 0) |
| BORRADO valiente | 96 · 26 % | 97 · 27 % | 93 · 28 % | 122 · 20 % | 408 · 25 % · 75 % (195 · 111 · 51 · 51) |
| BORRADO prudente | 105 · 24 % | 100 · 24 % | 102 · 24 % | 115 · 24 % | 422 · 24 % · 76 % (180 · 141 · 50 · 51) |
| APRENDE valiente | 104 · 22 % | 100 · 26 % | 113 · 20 % | 94 · 26 % | 411 · 23 % · 77 % (193 · 122 · 45 · 51) |
| APRENDE prudente | 106 · 19 % | 101 · 25 % | 97 · 28 % | 145 · 19 % | 449 · 22 % · 78 % (170 · 180 · 49 · 50) |
| SIN EMOCIÓN | 22 · 36 % | 45 · 20 % | 59 · 30 % | 76 · 21 % | 202 · 25 % · 75 % (58 · 93 · 31 · 20) |

En SIN, las forzadas (lo que pide la moneda) van a: botiquín 133, ración 111, red 75, camuflaje 30; a red + camuflaje por tramo: d1-5 26 % (93), d6-10 33 % (89), d11-15 33 % (91), d16-20 29 % (76).

## Sección 4 · Cuándo se prueba: calma o peligro

| variante | pruebas | con apertura P7-33 a ≤ 1 s | en calma | en peligro | rival a ≤ 4 | fuego | vida < 30 | hp0 < 50 | en calma por objeto (b · r · red · cam) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| TECHO | 0 | 0 | — | — | — | — | — | — | — · — · — · — |
| BORRADO valiente | 408 | 408 | 33 % | 67 % | 64 % | 0 % | 4 % | 10 % | 18 % · 14 % · 82 % · 78 % |
| BORRADO prudente | 422 | 422 | 32 % | 68 % | 66 % | 0 % | 4 % | 11 % | 12 % · 21 % · 86 % · 84 % |
| APRENDE valiente | 411 | 411 | 33 % | 67 % | 65 % | 0 % | 5 % | 12 % | 29 % · 11 % · 87 % · 57 % |
| APRENDE prudente | 449 | 449 | 32 % | 68 % | 66 % | 0 % | 6 % | 14 % | 22 % · 21 % · 82 % · 60 % |
| SIN EMOCIÓN | 202 | 202 | 31 % | 69 % | 67 % | 0 % | 6 % | 10 % | 17 % · 22 % · 64 % · 60 % |

## Sección 5 · R1 contado de nuevo: si SIN hubiera probado el botiquín tanto como APRENDE

Solo cuenta, no simula: (i) f = pruebas de botiquín por vida de APRENDE ÷ las de SIN; (ii) k* = primera prueba en la que la mediana de la creencia del botiquín (sección 2) llega a 25,
con la curva de cada cadena (las tres se dan); (iii) para cada criatura de SIN, su calendario real de pruebas acumuladas por día, multiplicado por f; día* = primer
día en que f × acumulado ≥ k*, 21 si no. Supuestos: lo que se aprende por prueba no cambia y las pruebas extra caen en los mismos días que las reales. La comprobación del método es
la cuenta con f = 1, que debe parecerse a la rapidez real.

Curva de la mediana (k: creencia tras la k-ésima prueba, n criaturas): APRENDE prudente: k1 1,3 (6), k2 6,4 (6), k3 8,5 (6), k4 8,7 (6), k5 8,7 (6), k6 8,4 (6), k7 8,1 (6), k8 7,8 (6); APRENDE valiente: k1 5,8 (6), k2 6,0 (6), k3 6,6 (6), k4 8,5 (6), k5 8,3 (6), k6 11,2 (6), k7 11,2 (6), k8 11,9 (6); SIN EMOCIÓN: k1 5,7 (3), k2 10,0 (3), k3 9,3 (3), k4 9,3 (3), k5 9,3 (3), k6 12,1 (3), k7 11,9 (3), k8 12,8 (3). Cada cadena da un k* distinto; la cuenta se hace con los tres, y la comprobación f = 1 dice cuál es coherente con qué cadena.

| cadena | pruebas de botiquín por vida | rapidez real (días por criatura) · media | k* propia (prueba en la que la mediana llega a 25) |
|---|---:|---|---:|
| APRENDE prudente | 1,42 | 21, 21, 21, 4, 6, 9 · 13,7 | 17 |
| APRENDE valiente | 1,61 | 13, 10, 21, 21, 21, 18 · 17,3 | 30 |
| SIN EMOCIÓN | 0,48 | 21, 7, 21, 21, 11, 21 · 17,0 | 10 |

| curva que da k* | k* | comprobación f = 1: SIN contada / real · la propia contada / real | SIN contada con f de APRENDE_p (días) · media | R1 contada frente a APRENDE_p (real) ± ee | SIN contada con f de APRENDE_v · media | R1 contada frente a APRENDE_v (real) ± ee |
|---|---:|---|---|---|---|---|
| SIN EMOCIÓN | 10 | 17,2 / 17,0 · 17,2 / 17,0 | 15, 8, 21, 21, 6, 21 · 15,3 | -1,7 (-3,3) ± 4,4 | 15, 8, 21, 21, 6, 21 · 15,3 | 2,0 (0,3) ± 3,4 |
| APRENDE prudente | 17 | 20,0 / 17,0 · 12,8 / 13,7 | 15, 8, 21, 21, 6, 21 · 15,3 | -1,7 (-3,3) ± 4,4 | 15, 8, 21, 21, 6, 21 · 15,3 | 2,0 (0,3) ± 3,4 |
| APRENDE valiente | 30 | 21,0 / 17,0 · 17,8 / 17,3 | 20, 11, 21, 21, 12, 21 · 17,7 | -4,0 (-3,3) ± 3,9 | 18, 11, 21, 21, 11, 21 · 17,2 | 0,2 (0,3) ± 2,8 |

## Sección 6 · Disco (archivado en el T7, 12-oct)

Los pilotos de P7-42 ya estaban archivados el 11-oct (zips leídos de vuelta y relectura tras remontar; `P7_43_copia.json`). Hoy, con el T7 conectado: los campos del seis que seguían con
diarios extraídos (P61, P610, P611, P616, P618, P622, P623, P624, P626, P627, P64, P66, P68), P7-33 y el resto de P7-24 — nada de eso lo usa el análisis del siete — a
`/Volumes/Mem G-EMV/gemv_archivo_2026-10-12` (`archiva_P7_46.py`, molde del 11-oct): 988 archivos copiados (0,97 GiB: zips, registros, PARCIAL, manifiestos, estados), leídos de vuelta iguales
988 de 988, relectura tras desmontar y montar sí; borrados del Mac 704 diarios extraídos cuyo zip pasó (no borrados [['paintball/runs/P724_s1_d10_BORRADO_37436472/ereq_02c798b2-3d4b-4b3f-8406-22e4fac4b380-policy_agent_10.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s1_d12_APRENDE_37645930/ereq_be42adf6-6052-4cf2-b283-df9725ae8913-policy_agent_11.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s1_d18_TECHO_38274304/ereq_e84d58b3-2ff1-44d4-baa1-21b9039d4f3f-policy_agent_10.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s1_d20_APRENDE_38483762/ereq_2fabc777-f3a8-4cd0-b6ab-27aa6daf94ae-policy_agent_11.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s1_d3_BORRADO_36703369/ereq_1dd08e8e-72e6-4d98-9a70-97f128ee7f6b-policy_agent_10.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s2_d18_APRENDE_36703369/ereq_7c970a48-2b0c-46f1-aed8-0c278d743a85-policy_agent_10.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s2_d18_APRENDE_36703369/ereq_7c970a48-2b0c-46f1-aed8-0c278d743a85-policy_agent_11.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s2_d20_APRENDE_36493911/ereq_52f5f499-b166-4fef-8449-f8522fd3157e-policy_agent_10.art.log', 'sin .zip (rescatado del registro de salida): no se borra'], ['paintball/runs/P724_s2_d7_TECHO_37855388/ereq_a27cab1e-5ea6-4a67-96e6-4c3dbcdb904c-policy_agent_10.art.log', 'sin .zip (rescatado del registro de salida): no se borra']]: rescatados sin zip); libre 11,5 → 35,5 GB. Los zips
se quedan en el Mac; las tres series (27 GB) no se tocan.

## Lectura (exploratoria; nada de esto evalúa el sello)

1. **La moneda de SIN manda, pero el cuerpo no obedece**: de 349 forzadas, acaban 101 (29 %). Las de usar caducan porque el cuerpo congelado no ofrece `usar_*` con la vida llena
   (79 de 84); las de ir llegan y no cogen (154 de 159): la pieza SIN no sabe terminar lo que empieza. Por eso
   SIN probó la mitad: no por la ε calibrada, sino porque la forzada muere en la llegada o en el usar. Es un límite de `azar_P7_41`, no del aprendiz ni del cuerpo.
2. **Lo que se aprende por prueba** del botiquín es parecido entre cadenas y pequeño: creencia tras la 3.ª prueba 8,5 (APRENDE prudente), 6,6 (valiente), 9,3 (SIN, n = 3); tras la 5.ª
   8,7, 8,3, 9,3. Para llegar a 25 la mediana necesita 17 pruebas en APRENDE prudente, 30 en valiente y 10 en SIN (3 criaturas); el cambio medio por prueba es
   0,67 ± 0,53, 0,76 ± 0,28 y 1,45 ± 1,03. BORRADO, desde cero cada día, sube 4,0-4,6 por prueba (las primeras pruebas son las que más suben).
3. **La elección no distingue a nadie**: a red + camuflaje va el 25 % de las pruebas de SIN y el 22 %-23 % de las de APRENDE (BORRADO 24 %-25 %), y no cambia con los días. La curiosidad con
   esperanza de clase (P7-40) no desvía las pruebas hacia lo útil ni lejos de lo inútil más que la moneda.
4. **Se prueba en peligro**: en calma solo el 32 %-33 % de las pruebas en todos los brazos (SIN 31 %); con rival a 4 casillas o menos el 64 %-67 %. Botiquín y ración se prueban en
   peligro (en calma 22 %-29 % en APRENDE), la red y el camuflaje en calma (82 %-87 %): es el cuerpo quien decide cuándo (usa el botiquín cuando le duele), no el aprendiz.
5. **R1 contado de nuevo**: si SIN hubiera probado el botiquín 2,9-3,3 veces más (lo de APRENDE), con su propia curva (k* = 10) su rapidez media pasaría de 17,0 a 15,3 días y R1 quedaría en
   -1,7 ± 4,4 (prudente) y 2,0 ± 3,4 (valiente): el mismo ruido que el real (-3,3 y 0,3). Con la curva de APRENDE prudente (k* = 17) o valiente (k* = 30) sale
   -1,7 / -4,0 frente a prudente. 3 de las 6 criaturas de SIN no probaron el botiquín ni una vez: multiplicar cero sigue siendo cero, y son ellas las que sostienen el 21.
   La comprobación f = 1 cuadra con la cadena que presta la curva (17,2 / 17,0 en SIN; 12,8 / 13,7 en prudente; 17,8 / 17,3 en valiente) y no cuadra cruzada: lo que se aprende por prueba NO es igual entre cadenas, así que
   el supuesto (i) de la cuenta es el flojo. Conclusión exploratoria: R1 no cambiaría de signo ni saldría del ruido por igualar las pruebas; lo que separa a las criaturas es si
   el cuerpo llega a usar el botiquín alguna vez, y eso lo decide el dolor, no la curiosidad.

# Valle · prompt 144 · De dónde sale el hambre de más de la criatura con ganancias

**Qué es esto:**
- **Solo análisis de partidas ya jugadas:** la RG68r sellada y su gemela RG068r del experimento v5, en sequía dura y sequía, semillas 30121 a 30140, días 0 a 9.
- **No se ha jugado nada nuevo ni se ha llamado a ningún modelo. Gasto: cero.**
- **No cambia el congelado v5 ni las predicciones selladas.**

**Los programas,** en `hambre_ganancias_v1/` (las reglas de cada uno están en su cabecera):
- `extrae_hg_v1.py`: lee cada partida y sigue una a una las cosas de cada bolsa;
- `analiza_hg_v1.py`: las tablas y los intervalos, que van a `analiza_hg_v1.md` y `.json`;
- `mira_v1.py` y `mira_datos_v1.py`: comprobaciones.

**Cómo se cuenta:**
- Cada diferencia es RG68r − gemela, emparejada por semilla.
- El intervalo del 95 % es bootstrap de las semillas, con 10.000 remuestras y semilla 8.
- «Las dos sequías» junta las 40 parejas de semillas.

## Resumen

**1. Pasa hambre llevando comida encima.**
- **Con hambre de más de 30 y comida en la bolsa:** RG68r pasa 30,3 turnos despierta por criatura y día; la gemela, 4,9. La diferencia es **+25,5 [+21,7, +29,3]**.
- **Con hambre de más de 30 y sin comida en ninguna parte:** también pasa más, pero mucho menos: +6,5 [+4,0, +9,2].
- **Con comida solo en la despensa:** casi nunca, ni una ni otra (−0,03 [−0,64, +0,58]).
- **Con hambre de más de 60 y comida en la bolsa:** 5,4 turnos frente a 0,6 (+4,8 [+3,8, +5,8]).
- **En sequía dura sale lo mismo, y más fuerte:** +36,0 [+33,5, +38,5] turnos con hambre >30 y comida en la bolsa.

**2. Come lo mismo, pero más tarde.**
- **Comidas por criatura y día:** casi las mismas, 2,98 frente a 2,97 (+0,01 [−0,01, +0,02]).
- **Hambre al comer:** 30,9 frente a 24,3 (+6,5 [+5,3, +7,8]).
- **Comidas con 60 de hambre o más:** el 12,1 % de sus comidas, frente al 3,4 % de la gemela (+8,7 pp [+6,8, +10,7]). En sequía dura, el 19,3 % frente al 5,5 %.

**3. Coge lo mismo, pero pierde más de lo que coge.**
- **Comida nueva cogida por criatura y día:** la misma (4,86 frente a 4,90; −0,04 [−0,15, +0,08]).
- **Hambre al cogerla:** 11,9 frente a 1,0 (+11,0 [+9,9, +12,0]).
- **Se la quitan en empujones:** el 26,7 % de lo nuevo que coge, frente al 16,5 % (+10,2 pp [+8,2, +12,1]).
- **Se la come ella:** el 50,9 % frente al 55,0 % (−4,1 pp [−5,5, −2,6]).
- **Lo que se come ella, lo come antes:** de cogerlo a comérselo pasan 236 turnos de media frente a 262 (−26 [−39, −13]).

**4. Dónde y cuándo come.**
- **En casa:** come mucho menos (0,59 comidas por criatura y día frente a 0,94; −0,35 [−0,40, −0,31]). Come más en el huerto, el bosque y la aldea.
- **Por mañana y tarde:** come menos por la mañana (−0,10 [−0,13, −0,07]) y más por la tarde y al anochecer.
- **De dónde sale:**
  - **de la bolsa, comida que lleva un rato encima:** las tres cuartas partes de las comidas en las dos (75 % frente a 72 %);
  - **de la despensa:** apenas, en las dos (3,7 % frente a 4,8 %).
- **Dónde empieza el día:** RG68r está fuera de casa en el primer turno del día la mitad de los días (50,5 %); la gemela, el 28,9 % (+21,5 pp).
- **Los días que empieza en casa:** come menos por la mañana que la gemela (1,53 frente a 1,75; −0,21 [−0,25, −0,18]).

**5. Busca menos tiempo y empieza a buscar con más hambre.**
- **Turnos dedicados a ir a por comida y cogerla:** 30,8 frente a 35,7 por criatura y día (−4,9 [−7,2, −2,6]).
- **Comida ganada:** la misma, así que gana más por turno (0,166 frente a 0,144 por turno; +0,022 [+0,011, +0,034]).
- **Hambre al empezar un viaje:** 10,4 frente a −1,7 (+12,2 [+10,9, +13,5]). El hambre puede bajar de cero en este mundo: lo que sobra al comer no se pierde.
- **Hambre al empezar el primer viaje del día:** 21,1 frente a 6,2 (+14,9 [+13,4, +16,5]).
- **Lo que dice el registro de decisiones de RG68r:** la primera decisión del día de ir a por comida la toma con un hambre media de 21,0 (27,1 en sequía dura, 14,8 en sequía). Cae, de media, en el turno 28 del día.

## Las tres frases

1. **RG68r pasa hambre con la comida a mano.** Casi todo su hambre de más se da con comida en la bolsa: unos 25 turnos de más al día con hambre de más de 30, frente a unos 6 sin comida en ninguna parte. Come las mismas veces que la gemela, pero con 6,5 puntos más de hambre.
2. **Frente a la gemela:**
   - **Comer:** come lo mismo, más tarde y más lejos de casa.
   - **Buscar:** coge lo mismo, dedicándole unos 5 turnos menos al día. Sale a buscar con unos 12 puntos más de hambre, cuando la gemela sale casi sin hambre. Pierde en empujones una parte mayor de lo que coge (27 % frente a 17 %).
3. **Lo que estos registros no pueden decir es por qué no come lo que lleva.**
   - El registro de decisiones guarda solo lo elegido y lo que se elegiría sumando de otras tres maneras, sin el malestar de cada candidato. No se sabe si «comer» estaba entre los candidatos ni a cuánto quedó.
   - De la gemela no hay registro de decisiones, así que sus viajes salen solo del registro del mundo.
   - Tampoco se puede decir si la comida perdida en empujones es causa o efecto de llevar más comida encima más rato.

## Lo simple que elegí (no estaba dicho)

- **El hambre al hacer algo:** la del turno de antes, la que tenía al decidirlo.
- **«Recién cogida»:** la que cogió de una planta, un matorral o el suelo hace 10 turnos o menos.
- **Un viaje:** los «mover» seguidos justo antes de coger comida, que no sea de la despensa, más los «coger» que vengan después. Trabajar el huerto va aparte.
- **Las opciones de «ir a por comida» del registro de decisiones:** ir_matorral, ir_objeto, ir_botin y coger. Ir_objeto también puede ser ir a por medicina.
- **Qué se pudre:** el mundo no lo apunta. Al cuadrar la bolsa, lo que sobra se cuenta como podrido, salvo el turno en que la bestia le robó.
  - **El cuadre de las 80 partidas:** nunca falta en la bolsa algo comido o dado; solo 23 cosas entraron sin saber de dónde.
- **Dónde empieza el día:** el sitio en el primer turno del día, dentro de casa sin contar la puerta.

## Tropiezos

- **Otro `python3 -c` suelto:** sin querer, uno que no hacía nada (`python3 -c 1`) mientras buscaba en el código del mundo. Va contra la regla.
- **Un nombre que confundía:** el primer nombre de la fila «días que amaneció fuera» no decía qué se mide. Lo cambié por «días que empieza fuera de casa».

## Gasto

- **Créditos de la plataforma:** 0.
- **Dólares de la consola de Anthropic:** 0.

---

Cada diferencia es RG68r − gemela, emparejada por semilla, con su intervalo del 95 %.

## las dos sequías (40 semillas)

| medida | RG68r | gemela | RG68r − gemela [95 %] |
|---|---|---|---|
| **2. Turnos despierta con hambre > 30, por criatura y día** | | | |
| con hambre > 30: lleva comida en la bolsa | 30,31 | 4,86 | +25,46 [+21,67, +29,28] |
| con hambre > 30: sin comida en la bolsa, con comida en la despensa | 0,95 | 0,98 | -0,03 [-0,64, +0,58] |
| con hambre > 30: sin comida en ninguna | 16,75 | 10,27 | +6,48 [+3,99, +9,21] |
| con hambre > 60: lleva comida en la bolsa | 5,38 | 0,61 | +4,76 [+3,79, +5,76] |
| con hambre > 60: sin comida en la bolsa, con comida en la despensa | 0,14 | 0,14 | -0,00 [-0,16, +0,18] |
| con hambre > 60: sin comida en ninguna | 5,03 | 2,09 | +2,93 [+1,58, +4,46] |
| turnos despierta (por criatura y día) | 256,48 | 249,68 | +6,80 [+5,48, +8,07] |
| hambre al comer (media) | 30,85 | 24,32 | +6,53 [+5,31, +7,79] |
| comidas con hambre < 20 (parte) | 0,500 | 0,616 | -0,115 [-0,138, -0,093] |
| comidas con hambre 20-30 (parte) | 0,113 | 0,112 | +0,000 [-0,010, +0,011] |
| comidas con hambre 30-45 (parte) | 0,163 | 0,193 | -0,030 [-0,042, -0,018] |
| comidas con hambre 45-60 (parte) | 0,103 | 0,045 | +0,058 [+0,050, +0,068] |
| comidas con hambre ≥ 60 (parte) | 0,121 | 0,034 | +0,087 [+0,068, +0,107] |
| **3. Lo que coge** | | | |
| cogidas nuevas (huerto, matorral, suelo, almacén), por criatura y día | 4,86 | 4,90 | -0,04 [-0,15, +0,08] |
| cogidas de la despensa, por criatura y día | 0,67 | 0,65 | +0,02 [-0,15, +0,19] |
| hambre al coger una nueva (media) | 11,90 | 0,95 | +10,96 [+9,93, +12,04] |
| turnos de cogerla a comérsela, las nuevas que se come ella (media) | 236,45 | 262,37 | -25,92 [-38,85, -13,23] |
| ídem, mediana | 178,32 | 220,65 | -42,33 [-62,38, -22,74] |
| ídem, las de la despensa (media) | 125,58 | 151,27 | -28,12 [-53,60, -2,48] |
| destino de las nuevas: se la come ella (parte) | 0,509 | 0,550 | -0,041 [-0,055, -0,026] |
| destino de las nuevas: la da (parte) | 0,016 | 0,009 | +0,007 [+0,004, +0,010] |
| destino de las nuevas: se la quitan (parte) | 0,267 | 0,165 | +0,102 [+0,082, +0,121] |
| destino de las nuevas: la guarda en la despensa (parte) | 0,040 | 0,062 | -0,022 [-0,035, -0,011] |
| destino de las nuevas: la deja en el almacén o el suelo (parte) | 0,009 | 0,008 | +0,001 [-0,006, +0,006] |
| destino de las nuevas: se pudre (parte) | 0,130 | 0,167 | -0,037 [-0,049, -0,027] |
| destino de las nuevas: sigue en la bolsa o muere con ella (parte) | 0,029 | 0,037 | -0,009 [-0,013, -0,004] |
| destino de las de la despensa: se la come ella (parte) | 0,185 | 0,246 | -0,058 [-0,109, -0,005] |
| destino de las de la despensa: se la quitan (parte) | 0,040 | 0,037 | +0,003 [-0,020, +0,025] |
| destino de las de la despensa: vuelve a la despensa (parte) | 0,653 | 0,591 | +0,055 [-0,015, +0,121] |
| destino de las de la despensa: se pudre (parte) | 0,107 | 0,103 | +0,007 [-0,021, +0,037] |
| **4. Comidas por criatura y día** | | | |
| todas | 2,98 | 2,97 | +0,01 [-0,01, +0,02] |
| en la fase mañana | 1,61 | 1,71 | -0,10 [-0,13, -0,07] |
| en la fase tarde | 1,18 | 1,13 | +0,06 [+0,03, +0,09] |
| en la fase anochecer | 0,15 | 0,11 | +0,04 [+0,02, +0,06] |
| en la fase noche | 0,04 | 0,03 | +0,01 [-0,00, +0,02] |
| en casa (dentro o en su puerta) | 0,59 | 0,94 | -0,35 [-0,40, -0,31] |
| en la aldea | 0,34 | 0,25 | +0,09 [+0,06, +0,12] |
| en el huerto | 1,00 | 0,84 | +0,16 [+0,12, +0,20] |
| en el bosque | 0,95 | 0,85 | +0,10 [+0,05, +0,15] |
| en otro sitio | 0,10 | 0,09 | +0,01 [-0,01, +0,03] |
| de dónde sale: de la bolsa (lleva un rato) (parte de las comidas) | 0,753 | 0,721 | +0,032 [+0,015, +0,048] |
| de dónde sale: de la despensa (parte de las comidas) | 0,037 | 0,048 | -0,012 [-0,022, -0,001] |
| de dónde sale: del almacén (parte de las comidas) | 0,118 | 0,121 | -0,003 [-0,010, +0,005] |
| de dónde sale: recién cogida (parte de las comidas) | 0,093 | 0,110 | -0,018 [-0,031, -0,004] |
| comidas de la mañana, días que empieza dentro de casa (primer turno del día) | 1,53 | 1,75 | -0,21 [-0,25, -0,18] |
| comidas de la mañana, días que empieza fuera de casa | 1,68 | 1,61 | +0,07 [+0,02, +0,12] |
| días que empieza fuera de casa (parte) | 0,505 | 0,289 | +0,215 [+0,187, +0,244] |
| **5. Ir a por comida (lo que deja el registro del mundo)** | | | |
| turnos dedicados (ir y coger), por criatura y día | 30,77 | 35,72 | -4,94 [-7,24, -2,62] |
| comida ganada en esos viajes, por criatura y día | 4,86 | 4,90 | -0,04 [-0,15, +0,08] |
| comida ganada por turno dedicado | 0,166 | 0,144 | +0,022 [+0,011, +0,034] |
| viajes por criatura y día | 2,73 | 2,59 | +0,14 [+0,08, +0,20] |
| hambre al empezar un viaje (media) | 10,44 | -1,72 | +12,16 [+10,87, +13,53] |
| hambre al empezar el primer viaje de cada día (media) | 21,14 | 6,23 | +14,91 [+13,39, +16,53] |
| turnos trabajando el huerto, por criatura y día | 19,60 | 20,02 | -0,43 [-0,64, -0,22] |

**Solo RG68r, de su registro de decisiones** (la gemela no lo tiene):

| medida | RG68r |
|---|---|
| turnos con la última decisión «ir a por comida», por criatura y día | 54,64 |
| hambre en la primera decisión de ir a por comida de cada día (media) | 20,97 |
| ídem, con hambre < 15 (parte) | 0,525 |
| ídem, con hambre ≥ 30 (parte) | 0,342 |
| turno del día de esa primera decisión (media) | 27,71 |

## sequía dura (20 semillas)

| medida | RG68r | gemela | RG68r − gemela [95 %] |
|---|---|---|---|
| **2. Turnos despierta con hambre > 30, por criatura y día** | | | |
| con hambre > 30: lleva comida en la bolsa | 42,29 | 6,24 | +36,04 [+33,51, +38,45] |
| con hambre > 30: sin comida en la bolsa, con comida en la despensa | 1,27 | 1,09 | +0,18 [-0,82, +1,18] |
| con hambre > 30: sin comida en ninguna | 28,28 | 17,11 | +11,17 [+7,13, +15,35] |
| con hambre > 60: lleva comida en la bolsa | 8,33 | 0,93 | +7,40 [+6,58, +8,22] |
| con hambre > 60: sin comida en la bolsa, con comida en la despensa | 0,25 | 0,12 | +0,13 [-0,14, +0,45] |
| con hambre > 60: sin comida en ninguna | 9,41 | 3,76 | +5,65 [+3,42, +8,08] |
| turnos despierta (por criatura y día) | 257,29 | 250,03 | +7,26 [+5,98, +8,83] |
| hambre al comer (media) | 36,04 | 26,28 | +9,76 [+8,49, +11,06] |
| comidas con hambre < 20 (parte) | 0,405 | 0,569 | -0,164 [-0,189, -0,138] |
| comidas con hambre 20-30 (parte) | 0,111 | 0,116 | -0,005 [-0,019, +0,009] |
| comidas con hambre 30-45 (parte) | 0,159 | 0,203 | -0,044 [-0,057, -0,031] |
| comidas con hambre 45-60 (parte) | 0,132 | 0,057 | +0,075 [+0,063, +0,088] |
| comidas con hambre ≥ 60 (parte) | 0,193 | 0,055 | +0,138 [+0,119, +0,158] |
| **3. Lo que coge** | | | |
| cogidas nuevas (huerto, matorral, suelo, almacén), por criatura y día | 4,31 | 4,36 | -0,06 [-0,14, +0,04] |
| cogidas de la despensa, por criatura y día | 0,56 | 0,69 | -0,14 [-0,36, +0,07] |
| hambre al coger una nueva (media) | 16,89 | 3,69 | +13,20 [+11,96, +14,52] |
| turnos de cogerla a comérsela, las nuevas que se come ella (media) | 198,94 | 221,07 | -22,13 [-33,92, -10,61] |
| ídem, mediana | 130,07 | 153,95 | -23,88 [-38,92, -7,83] |
| ídem, las de la despensa (media) | 98,79 | 143,12 | -44,33 [-80,75, -8,72] |
| destino de las nuevas: se la come ella (parte) | 0,544 | 0,599 | -0,055 [-0,069, -0,040] |
| destino de las nuevas: la da (parte) | 0,022 | 0,014 | +0,009 [+0,004, +0,013] |
| destino de las nuevas: se la quitan (parte) | 0,285 | 0,177 | +0,108 [+0,086, +0,130] |
| destino de las nuevas: la guarda en la despensa (parte) | 0,034 | 0,060 | -0,026 [-0,045, -0,009] |
| destino de las nuevas: la deja en el almacén o el suelo (parte) | 0,003 | 0,007 | -0,004 [-0,014, +0,003] |
| destino de las nuevas: se pudre (parte) | 0,095 | 0,123 | -0,028 [-0,040, -0,015] |
| destino de las nuevas: sigue en la bolsa o muere con ella (parte) | 0,016 | 0,020 | -0,005 [-0,009, -0,001] |
| destino de las de la despensa: se la come ella (parte) | 0,201 | 0,243 | -0,042 [-0,110, +0,025] |
| destino de las de la despensa: se la quitan (parte) | 0,047 | 0,034 | +0,013 [-0,009, +0,035] |
| destino de las de la despensa: vuelve a la despensa (parte) | 0,632 | 0,599 | +0,033 [-0,044, +0,114] |
| destino de las de la despensa: se pudre (parte) | 0,101 | 0,101 | -0,000 [-0,035, +0,036] |
| **4. Comidas por criatura y día** | | | |
| todas | 2,96 | 2,97 | -0,00 [-0,02, +0,01] |
| en la fase mañana | 1,58 | 1,69 | -0,12 [-0,16, -0,07] |
| en la fase tarde | 1,19 | 1,12 | +0,07 [+0,04, +0,11] |
| en la fase anochecer | 0,15 | 0,12 | +0,03 [+0,01, +0,05] |
| en la fase noche | 0,04 | 0,03 | +0,01 [-0,00, +0,03] |
| en casa (dentro o en su puerta) | 0,53 | 0,91 | -0,37 [-0,44, -0,31] |
| en la aldea | 0,34 | 0,25 | +0,09 [+0,04, +0,13] |
| en el huerto | 0,98 | 0,80 | +0,18 [+0,15, +0,22] |
| en el bosque | 1,00 | 0,91 | +0,10 [+0,03, +0,16] |
| en otro sitio | 0,10 | 0,10 | +0,00 [-0,02, +0,03] |
| de dónde sale: de la bolsa (lleva un rato) (parte de las comidas) | 0,730 | 0,681 | +0,049 [+0,028, +0,070] |
| de dónde sale: de la despensa (parte de las comidas) | 0,036 | 0,051 | -0,015 [-0,028, -0,003] |
| de dónde sale: del almacén (parte de las comidas) | 0,118 | 0,118 | -0,001 [-0,012, +0,010] |
| de dónde sale: recién cogida (parte de las comidas) | 0,117 | 0,149 | -0,032 [-0,052, -0,013] |
| comidas de la mañana, días que empieza dentro de casa (primer turno del día) | 1,49 | 1,72 | -0,23 [-0,29, -0,18] |
| comidas de la mañana, días que empieza fuera de casa | 1,66 | 1,64 | +0,02 [-0,04, +0,08] |
| días que empieza fuera de casa (parte) | 0,517 | 0,324 | +0,193 [+0,158, +0,228] |
| **5. Ir a por comida (lo que deja el registro del mundo)** | | | |
| turnos dedicados (ir y coger), por criatura y día | 34,68 | 39,88 | -5,19 [-8,32, -2,06] |
| comida ganada en esos viajes, por criatura y día | 4,31 | 4,36 | -0,06 [-0,14, +0,04] |
| comida ganada por turno dedicado | 0,126 | 0,113 | +0,013 [+0,002, +0,024] |
| viajes por criatura y día | 2,56 | 2,41 | +0,15 [+0,09, +0,21] |
| hambre al empezar un viaje (media) | 16,87 | 1,95 | +14,92 [+13,24, +16,65] |
| hambre al empezar el primer viaje de cada día (media) | 27,64 | 10,52 | +17,12 [+14,94, +19,33] |
| turnos trabajando el huerto, por criatura y día | 19,78 | 20,11 | -0,32 [-0,62, -0,03] |

**Solo RG68r, de su registro de decisiones** (la gemela no lo tiene):

| medida | RG68r |
|---|---|
| turnos con la última decisión «ir a por comida», por criatura y día | 59,59 |
| hambre en la primera decisión de ir a por comida de cada día (media) | 27,13 |
| ídem, con hambre < 15 (parte) | 0,428 |
| ídem, con hambre ≥ 30 (parte) | 0,450 |
| turno del día de esa primera decisión (media) | 27,58 |

## sequía (20 semillas)

| medida | RG68r | gemela | RG68r − gemela [95 %] |
|---|---|---|---|
| **2. Turnos despierta con hambre > 30, por criatura y día** | | | |
| con hambre > 30: lleva comida en la bolsa | 18,34 | 3,47 | +14,87 [+12,22, +17,88] |
| con hambre > 30: sin comida en la bolsa, con comida en la despensa | 0,64 | 0,87 | -0,24 [-0,94, +0,42] |
| con hambre > 30: sin comida en ninguna | 5,23 | 3,43 | +1,79 [+0,22, +3,21] |
| con hambre > 60: lleva comida en la bolsa | 2,42 | 0,29 | +2,13 [+1,51, +2,89] |
| con hambre > 60: sin comida en la bolsa, con comida en la despensa | 0,03 | 0,17 | -0,14 [-0,30, -0,01] |
| con hambre > 60: sin comida en ninguna | 0,64 | 0,43 | +0,22 [-0,30, +0,65] |
| turnos despierta (por criatura y día) | 255,67 | 249,32 | +6,34 [+4,07, +8,41] |
| hambre al comer (media) | 25,66 | 22,36 | +3,30 [+2,51, +4,22] |
| comidas con hambre < 20 (parte) | 0,596 | 0,663 | -0,067 [-0,091, -0,045] |
| comidas con hambre 20-30 (parte) | 0,115 | 0,109 | +0,006 [-0,010, +0,023] |
| comidas con hambre 30-45 (parte) | 0,166 | 0,183 | -0,017 [-0,034, +0,001] |
| comidas con hambre 45-60 (parte) | 0,075 | 0,033 | +0,042 [+0,034, +0,049] |
| comidas con hambre ≥ 60 (parte) | 0,049 | 0,013 | +0,036 [+0,025, +0,048] |
| **3. Lo que coge** | | | |
| cogidas nuevas (huerto, matorral, suelo, almacén), por criatura y día | 5,42 | 5,43 | -0,02 [-0,22, +0,19] |
| cogidas de la despensa, por criatura y día | 0,78 | 0,61 | +0,18 [-0,06, +0,42] |
| hambre al coger una nueva (media) | 6,92 | -1,79 | +8,71 [+7,79, +9,70] |
| turnos de cogerla a comérsela, las nuevas que se come ella (media) | 273,96 | 303,67 | -29,71 [-52,05, -6,84] |
| ídem, mediana | 226,57 | 287,35 | -60,77 [-93,97, -25,68] |
| ídem, las de la despensa (media) | 152,37 | 160,33 | -10,10 [-43,28, +25,70] |
| destino de las nuevas: se la come ella (parte) | 0,475 | 0,502 | -0,027 [-0,052, -0,003] |
| destino de las nuevas: la da (parte) | 0,010 | 0,005 | +0,005 [+0,002, +0,008] |
| destino de las nuevas: se la quitan (parte) | 0,249 | 0,154 | +0,095 [+0,062, +0,130] |
| destino de las nuevas: la guarda en la despensa (parte) | 0,045 | 0,064 | -0,019 [-0,033, -0,003] |
| destino de las nuevas: la deja en el almacén o el suelo (parte) | 0,015 | 0,010 | +0,005 [-0,002, +0,012] |
| destino de las nuevas: se pudre (parte) | 0,164 | 0,211 | -0,047 [-0,063, -0,031] |
| destino de las nuevas: sigue en la bolsa o muere con ella (parte) | 0,041 | 0,054 | -0,013 [-0,020, -0,005] |
| destino de las de la despensa: se la come ella (parte) | 0,168 | 0,249 | -0,075 [-0,155, +0,003] |
| destino de las de la despensa: se la quitan (parte) | 0,033 | 0,041 | -0,008 [-0,047, +0,031] |
| destino de las de la despensa: vuelve a la despensa (parte) | 0,674 | 0,582 | +0,080 [-0,035, +0,187] |
| destino de las de la despensa: se pudre (parte) | 0,113 | 0,104 | +0,014 [-0,027, +0,060] |
| **4. Comidas por criatura y día** | | | |
| todas | 2,99 | 2,98 | +0,02 [-0,01, +0,04] |
| en la fase mañana | 1,64 | 1,73 | -0,09 [-0,13, -0,04] |
| en la fase tarde | 1,17 | 1,13 | +0,04 [+0,00, +0,09] |
| en la fase anochecer | 0,15 | 0,09 | +0,06 [+0,03, +0,08] |
| en la fase noche | 0,03 | 0,02 | +0,01 [-0,01, +0,02] |
| en casa (dentro o en su puerta) | 0,64 | 0,97 | -0,33 [-0,39, -0,28] |
| en la aldea | 0,34 | 0,25 | +0,09 [+0,06, +0,12] |
| en el huerto | 1,02 | 0,87 | +0,14 [+0,07, +0,21] |
| en el bosque | 0,90 | 0,80 | +0,10 [+0,02, +0,18] |
| en otro sitio | 0,09 | 0,07 | +0,02 [-0,02, +0,05] |
| de dónde sale: de la bolsa (lleva un rato) (parte de las comidas) | 0,776 | 0,760 | +0,015 [-0,007, +0,036] |
| de dónde sale: de la despensa (parte de las comidas) | 0,038 | 0,046 | -0,008 [-0,024, +0,009] |
| de dónde sale: del almacén (parte de las comidas) | 0,118 | 0,123 | -0,005 [-0,015, +0,006] |
| de dónde sale: recién cogida (parte de las comidas) | 0,068 | 0,071 | -0,003 [-0,016, +0,012] |
| comidas de la mañana, días que empieza dentro de casa (primer turno del día) | 1,58 | 1,78 | -0,20 [-0,24, -0,15] |
| comidas de la mañana, días que empieza fuera de casa | 1,70 | 1,58 | +0,12 [+0,05, +0,19] |
| días que empieza fuera de casa (parte) | 0,493 | 0,255 | +0,238 [+0,194, +0,280] |
| **5. Ir a por comida (lo que deja el registro del mundo)** | | | |
| turnos dedicados (ir y coger), por criatura y día | 26,87 | 31,56 | -4,69 [-8,08, -1,44] |
| comida ganada en esos viajes, por criatura y día | 5,42 | 5,43 | -0,02 [-0,22, +0,19] |
| comida ganada por turno dedicado | 0,206 | 0,175 | +0,031 [+0,011, +0,050] |
| viajes por criatura y día | 2,91 | 2,77 | +0,14 [+0,03, +0,24] |
| hambre al empezar un viaje (media) | 4,01 | -5,40 | +9,41 [+8,29, +10,58] |
| hambre al empezar el primer viaje de cada día (media) | 14,64 | 1,94 | +12,70 [+11,07, +14,55] |
| turnos trabajando el huerto, por criatura y día | 19,41 | 19,94 | -0,53 [-0,81, -0,23] |

**Solo RG68r, de su registro de decisiones** (la gemela no lo tiene):

| medida | RG68r |
|---|---|
| turnos con la última decisión «ir a por comida», por criatura y día | 49,69 |
| hambre en la primera decisión de ir a por comida de cada día (media) | 14,82 |
| ídem, con hambre < 15 (parte) | 0,623 |
| ídem, con hambre ≥ 30 (parte) | 0,233 |
| turno del día de esa primera decisión (media) | 27,84 |

**Cuadre de la bolsa** (las 80 partidas): lo que sobraba al cuadrar (podrido) 6365; lo que se llevó la bestia 224; lo que faltaba (entró sin saber de dónde) 23; lo comido o dado que no encontré en la bolsa 0.

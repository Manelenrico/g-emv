# Predicciones selladas v6: el experimento de la reserva y la voz

*17-nov-2026, antes de jugar ninguna partida del experimento. Sobre el congelado `valle-congelado-v6` (`CONGELADO_P8_v6.md`, la protagonista RG69r+voz). Lo que no se cumpla se cuenta igual.*

*Es `predicciones_v6_borrador.md` (prompt 149) con el formato de `predicciones_selladas_v5.md`, sin cambiar ningún umbral ni ninguna medida. La protagonista, RG69r+voz, la eligió Manel (prompt 150). Solo hay los añadidos que pidió Manel en el prompt 150:*
- *la sección «Riesgos que se declaran antes de jugar»;*
- *una medida más, M14 (las muertes por causa, por mundo y por época);*
- *P13 y P17 son «4 o menos de las 200», como en el v5: la cuenta en proporción fue solo para el informe de los talleres;*
- *en «Antes de sellar», las 8 puertas del prompt 149, que apuntar no cambia nada, las semillas y las huellas md5.*

*Las medidas sin predicción M1 a M8, A1, A2 y A4 se copian del v5, con RG69r+voz en el sitio de RG68r.*

## El diseño

- **Jugadores:**
  - el tonto y el recolector;
  - RG68r y RG068r, las del v5;
  - RG69r (la reserva, prompt 146: `cuerpo_rg69.RG69`);
  - la protagonista, RG69r+voz (la reserva y la voz de ir a casa, prompt 147: `cuerpo_vr1.RG69V`). En las carpetas se llama `RG69rvoz`.
- **Mundos:** los cinco (abundancia, normal, sequía, sequía dura y bestias que crían), con el árbol de fruta dulce encendido.
- **Semillas:** 30161–30200, nunca usadas (`preparar_v6/semillas_v6.md`).
- **Partidas:** de 40 días; 6 × 5 × 40 = 1.200.
- **Diferencias:** por semillas emparejadas, con intervalo del 95 %.
- **El lanzador:** `lanza_experimento_v6.py`, reanudable y con el Mac despierto. Juega en la carpeta oficial `valle_experimento_v6`, sin pruebas mezcladas.
- **El evaluador:** `evalua_experimento_v6.py`.
- **Lo que se apunta** (los registros del v5 y lo de los talleres):
  - **en las cuatro clases de criatura,** por criatura y turno: `balance.jsonl.gz` y `filas.jsonl.gz`. Al acabar: `cuaderno_sitios.json` y `cuenta_v61.json`;
  - **en la protagonista,** el registro de decisiones con las de ir (`decisiones.jsonl.gz`);
  - **en RG69r y RG69r+voz,** `reserva_v69.json`;
  - **en RG69r+voz,** `voz_vc1.json`.

## Las predicciones (el texto de la mesa)

**Se quedan, palabra por palabra, con RG69r+voz en el sitio de RG68r.** Se dicen también para RG69r y RG68r, sin contar como predicción.

P1. En sequía, sequía dura y bestias que crían, RG69r+voz vive al menos una criatura más que el tonto, con el intervalo por encima de cero.
P2. En abundancia y normal, RG69r+voz vive de media al menos 7,5 de 8. Declarado: en el normal, el tonto puede vivir algo más.
P3. Ninguna muerte por golpe entre criaturas en ningún mundo.
P4. Con la bestia a la vista, la fracción de veces con otra pegada es al menos el triple en RG69r+voz que en el tonto.
P5. En bestias que crían, RG69r+voz echa la bestia al menos una vez por partida de media.
P6. RG69r+voz da más comida a la hermana que a cada vecina, por cabeza, en todos los mundos.
P7. La parte de lo que RG69r+voz da a quien está flaca es mayor en sequía y en sequía dura que en abundancia.
P8. En los cinco días siguientes a la muerte de la hermana, RG69r+voz pasa más tiempo con vecinas que en los cinco anteriores, emparejado por criatura.
P9. RG69r+voz duerme dentro de su casa al menos el 55 % de las noches en los cinco mundos, y ninguna noche en una puerta sin estar agotada.
P10. En la sequía y en la sequía dura, RG068r vive igual o más que RG68r.
P12. Sin razón, RG69r+voz coge menos del 15 % de la fruta del árbol y menos que el recolector.
P13. Sin ninguna regla que lo impida, RG69r+voz no da su última comida con más de 60 de hambre propia en más de 2 de cada 100 partidas.
P16. RG69r+voz empuja más que RG068r en los cinco mundos.
P17. Hay rachas de regalos de ida y vuelta de más de 10 en 4 o menos de las 200 partidas de RG69r+voz.
P18. Los despertares por voz quedan por debajo de 1 por criatura y noche en los cinco mundos (RG69r+voz).

**Salen:**
- **P11** pasa a medida sin predicción (M9). Se declara: es la pregunta de la escalera, sellada en el v5, y no sabemos qué saldrá con la reserva.
- **P19 a P23** desaparecen, porque RG61r no juega.

**Nuevas:**

P24. En la sequía y la sequía dura juntas, días 0 a 9, los turnos al día despierta con hambre de más de 30 y comida en la bolsa: RG69r, como mucho la mitad que RG68r.
P25. En la sequía dura, RG69r vive más que RG68r, con el límite inferior del intervalo sobre cero.
P26. La reserva no hace daño (RG69r frente a RG68r, cinco mundos): en ningún mundo el límite superior del intervalo de las vivas queda bajo cero; en ningún mundo la felicidad de la aldea baja más de 0,03 de media; en ningún mundo los empujones por partida pasan de 1,25 veces.
P27. Coste declarado: en la sequía dura, las vivas que llegan al empezar el día 10 con la bolsa y la despensa vacías son más, de media por partida, en RG69r que en RG68r.
P28. En la sequía y la sequía dura juntas, días 0 a 9, las noches dormidas fuera (la medida del taller 147): RG69r+voz, como mucho dos tercios de las de RG69r.
P29. La voz no rompe la reserva: la medida de P24 en RG69r+voz, como mucho la mitad que RG68r.
P30. La voz no hace daño: las tres partes de P26, RG69r+voz frente a RG69r.
P31. En la sequía dura, RG69r+voz vive más que RG68r, con el límite inferior del intervalo sobre cero.

*Cuentan como predicción 23: P1 a P9, P12, P13 y P16 a P18 en la protagonista (14), P10, y P24 a P31 (8). P14 sigue como medida sin predicción (M8); P15 sigue quitada.*

## Riesgos que se declaran antes de jugar

- **P26 en la abundancia.** En el taller (10 semillas ya vistas, 30121–30130), RG69r frente a RG68r dio −0,30 vivas [−0,60, +0,00], por 3 muertes por la bestia, y la felicidad de la aldea, −0,025. La predicción se escribió antes de ver la abundancia y no se cambia. Puede fallar ahí.
- **P4 va justa:** 3,5 veces frente a 3 en los talleres.
- **El hueco con la gemela ya cambió entre experimentos** (v4: +0,07 en la sequía dura). P25 y P31 pueden fallar en semillas nuevas.
- **Las bestias que crían, con la voz,** dieron −0,20 y +0,70 en dos talleres de 10 semillas: no se predice dirección.
- **Las predicciones nuevas (P24 a P31)** salen de talleres jugados en semillas ya vistas (30121 a 30140). Que se cumplan allí no cuenta.

## Las medidas sin predicción

**Las del v5, en la protagonista** (el texto de `predicciones_selladas_v5.md`, con RG69r+voz en el sitio de RG68r):

M1. Felicidad funcional: en cada turno despierta, el balance de cada dimensión es la fuerza de ganancia menos la de pérdida; la criatura está en felicidad funcional cuando las tres están en positivo a la vez. Por criatura, la parte del tiempo así y la media de los tres balances; de la aldea, la media y la peor parada.
M2. Momentos hygge: al atardecer o de noche, en su casa, con la hermana dentro, sin estar flaca, sin la bestia a la vista y con las tres dimensiones en positivo. Cuántos por criatura y por noche.
M3. Lo que siente en cada sitio según sus recuerdos: la marca emocional media de los recuerdos del cuaderno por tipo de sitio.
M4. Los tres mapas del valle por mundo: por casilla, el balance medio (bienestar), la pérdida por la bestia (miedo), y los empujones y robos (peleas).
M5. El huerto: cuántas veces se trabaja y por quién.
M6. El perdón: después de un robo, cuántos días tarda en volver lo que vale la ladrona en el radar de la robada a lo que valía antes.
M7. La hora de las vueltas del árbol: la parte de las vueltas de RG69r+voz después de anochecer.
M8. Las vecinas que le han robado a RG69r+voz reciben de ella menos comida, por cabeza, que las vecinas que nunca le han robado, en los mundos donde hay robos. **Se declara que no sabemos qué saldrá.**
A1. El mapa de dónde se dan regalos, por mundo, junto al mapa del bienestar.
A2. La criatura que ha perdido a su hermana frente a las que la conservan: su felicidad funcional antes y después de la muerte, su felicidad en casa, si sigue durmiendo en casa, cuántos días tarda en recuperarse, y si busca la compañía de una vecina, también de noche.
A4. En la que pierde a su hermana, las dos señales por separado: la del duelo (la tristeza por la pérdida) y la de la soledad (estar sin ella, sobre todo en casa). Para cada una, cómo está antes de la muerte, cuánto sube después y cuántos días tarda en volver a como estaba.

**Las del v6** (el texto de la mesa):

M9. Era P11, con sus dos cifras.
M10. RG69r+voz frente a RG068r, vivas en los cinco mundos. Se declara que no sabemos si la alcanza en la sequía dura.
M11. En las cuatro clases de criatura: el hambre al empezar los días 10 y 30; las muertes de hambre en cada escasez (días 10 a 14 y 30 a 34); las vivas que llegan a cada escasez sin reserva.
M12. La voz. Cuántas veces suena, se devuelve, acaban las dos en casa, y cuántas veces «ir a casa» ya era lo elegido.
M13. La comida que le quitan a empujones (parte de lo que coge) y los turnos al frío.
M14. Las muertes por causa (hambre, bestia, frío, otras), por mundo y por época, en las cuatro clases de criatura.

## Cómo se mide cada predicción y cada medida

*Añadido por mí antes de jugar, para que no haya que elegir después.*

**Las que se quedan** se miden con las medidas del v5, sin cambiar nada:
- son las piezas de `evalua_experimento_v5.py`, importadas por `evalua_experimento_v6.py`;
- se miden en las 200 partidas de RG69r+voz (40 por mundo), donde el v5 decía RG68r.

**Las nuevas** se miden con las medidas de los talleres, importadas:
- `voz_a_casa_v1/analiza_vc1.una` (143);
- `hambre_ganancias_v1/extrae_hg_v1.una` (144);
- la cuenta de bolsa y despensa vacías de `reserva_v1/analiza_rg69.py` (146);
- `voz_a_casa_v1/voces_v1.voces` (143).

**Lo común, como en el v5:**
- **Las vivas** son las del día 40, de 8.
- **Los intervalos** del 95 % salen de un bootstrap de 10.000 remuestreos, con semilla 8: de las semillas emparejadas, o de lo que se diga en cada una.
- **Lo de dar** es solo comida, dada con éxito (registro del mundo), salvo en P17, que cuenta comida y medicina por separado.
- **«Flaca»** es el hambre por encima del umbral de flaca del mundo (60) en el turno anterior.
- **«Vecina»** es cualquier criatura de otra casa.
- **«RG69r+voz»** es la clase. Cuando una predicción no dice otra cosa, se mide en sus 200 partidas (40 por mundo).

| | cómo se mide | se cumple si |
|---|---|---|
| P1 | vivas de RG69r+voz − vivas del tonto, emparejadas por semilla, en cada uno de los tres mundos | en los tres, la media es ≥ 1 y el límite inferior del intervalo es > 0 |
| P2 | la media de vivas de RG69r+voz en abundancia y en normal | las dos son ≥ 7,5 |
| P3 | las muertes con causa «golpe de …», en las 1.200 partidas | no hay ninguna |
| P4 | de los turnos fuera de casa con alguna bestia a la vista de la fase, la parte con otra criatura a una casilla o menos (`cierre_v46`); RG69r+voz frente al tonto, sumando los cinco mundos | la de RG69r+voz es ≥ 3 veces la del tonto en la suma de los cinco |
| P5 | las veces que se echa una bestia (evento `bestia_echada`), por partida de RG69r+voz, en bestias que crían | la media es ≥ 1 |
| P6 | lo dado a la hermana frente a lo dado a las seis vecinas dividido entre seis, sumando las 40 partidas de cada mundo | en los cinco mundos, lo de la hermana es mayor |
| P7 | la parte de lo dado por RG69r+voz a quien estaba flaca, por mundo | la de la sequía y la de la sequía dura son las dos mayores que la de la abundancia |
| P8 | por cada criatura de RG69r+voz que pierde a su hermana y sigue viva 5 días o más: la parte del día pegada a una vecina viva, la media de los 5 días después menos la de los 5 antes (`analiza_v45`); todas las criaturas de los cinco mundos, con intervalo por bootstrap de criaturas | la media es > 0 y el límite inferior del intervalo es > 0 |
| P9 | la primera vez que se duerme cada criatura cada noche (`medida_v4/dormir_v4.py`): la parte dentro de su casa (sin la puerta), por mundo, y las veces en una puerta sin estar agotada | ≥ 55 % dentro en los cinco mundos, y 0 en una puerta sin estar agotada en las 200 partidas |
| P10 | vivas de RG068r − vivas de RG68r, emparejadas por semilla, en la sequía y en la sequía dura | en los dos, el límite superior del intervalo es ≥ 0 |
| P12 | de las frutas puestas, la parte cogida (puestas menos perdidas), en las partidas de RG69r+voz y en las del recolector, sumando los cinco mundos (`analiza_arbol_v50`) | RG69r+voz coge < 15 % y menos que el recolector |
| P13 | las partidas de RG69r+voz con al menos un «dar comida» con éxito en el que quien da llevaba una sola comida y tenía el hambre > 60 en el turno anterior | como mucho 2 de cada 100: ≤ 4 de las 200 |
| P16 | los empujones a otra criatura por partida (`cierre_v46`: «empujar» a otra criatura, no a la bestia, sin resultado «no:»), RG69r+voz y RG068r, en cada mundo | en los cinco mundos, la media por partida de RG69r+voz es mayor que la de RG068r |
| P17 | en cada partida, por par de criaturas y tipo (comida, medicina), la racha más larga de regalos que van y vuelven (A→B, B→A, …) con menos de 40 turnos entre uno y otro (`comprueba_v58.bucles`), en las 200 partidas de RG69r+voz | las partidas con alguna racha > 10 (de comida o de medicina) son 4 o menos de las 200 |
| P18 | los despertares por voz (eventos «despierta» con motivo «llamada …» o «voz …») de RG69r+voz, sumados en las 40 partidas de cada mundo, entre sus noches-criatura (las criaturas vivas al empezar cada día) | en los cinco mundos, < 1 por criatura y noche |
| P24 | **la medida del 144** (`extrae_hg_v1`, días 0 a 9), por partida: los turnos despierta (no dormida) con hambre > 30 y alguna comida en la bolsa, entre los pares criatura-día vivos. La media de las 80 partidas de sequía y sequía dura de cada jugador. RG69r frente a RG68r | la de RG69r ≤ 0,5 × la de RG68r |
| P25 | vivas de RG69r − vivas de RG68r, emparejadas por semilla, en la sequía dura | el límite inferior del intervalo es > 0 |
| P26 | en cada mundo, RG69r frente a RG68r: las vivas emparejadas (como P25); la felicidad funcional de la aldea (M1 del v5: por criatura, la parte de sus turnos despierta con los tres balances > 0; la aldea, la media; `evalua_experimento_v5.v5`), media de las diferencias emparejadas; los empujones por partida (como P16), la media de RG69r entre la de RG68r | en los cinco mundos: el límite superior de las vivas ≥ 0, la felicidad ≥ −0,03 y los empujones ≤ 1,25 veces |
| P27 | en el primer turno del día 10, las criaturas vivas que no llevan ninguna comida en la bolsa y cuya casa no tiene comida en la despensa (`mundo.jsonl.gz` y `criaturas.jsonl.gz`, como el 146), por partida; la media de las 40 partidas de sequía dura | la de RG69r es mayor que la de RG68r |
| P28 | **la medida del 143 y el 147** (`dormir_fuera_v5/noches_v5`, por `analiza_vc1`): de cada criatura viva al empezar la noche, la noche es «fuera» si en la fase noche está dormida fuera de su casa más de la mitad de los turnos. La parte de noches «fuera», sumando todas las noches de los días 0 a 9 de las 80 partidas de sequía y sequía dura de cada jugador | la de RG69r+voz ≤ 2/3 × la de RG69r |
| P29 | la medida de P24, RG69r+voz frente a RG68r | la de RG69r+voz ≤ 0,5 × la de RG68r |
| P30 | las tres partes de P26, RG69r+voz frente a RG69r | las tres, en los cinco mundos |
| P31 | vivas de RG69r+voz − vivas de RG68r, emparejadas por semilla, en la sequía dura | el límite inferior del intervalo es > 0 |

**M9 (era P11), con detalle** (la medida del v5, palabra por palabra):
- **De dónde salen las decisiones:** en cada decisión de RG69r+voz, `decisiones.jsonl.gz` guarda la opción elegida y la que elegiría cada valorador (el motor, las sumas y la posición) en el mismo estado exacto, **también las de ir** (`medida_v3/lanza_medida_v3.py`).
- **La medida es la del v2, el v3 y el v5, sin cambiar:**
  - cómo se desempata: con las reglas de empate de ahora;
  - la muestra: 2.000 decisiones por mundo, con la semilla del muestreo «8|RG68r|<mundo>»;
  - la ambivalencia: la mayor de las tres dimensiones, y la de cada una es la menor de su ganancia y su pérdida (`ambivalencia.py`);
  - los cuartos van dentro de cada mundo;
  - se compara Q4 − Q1 de `igual_sumas`, sumando los cinco mundos;
  - el intervalo, por bootstrap de partidas.
- **La segunda cifra usa la misma muestra y los mismos cuartos,** quitando las decisiones en que la elegida o la de las sumas es «dar».
- **Se dice también la cifra sin las decisiones de ir.**

**Las medidas sin predicción** (se dicen; no se cumplen ni fallan). Salen de `balance.jsonl.gz`, `filas.jsonl.gz`, `mundo.jsonl.gz`, `criaturas.jsonl.gz`, `fin.json`, `cuaderno_sitios.json`, `radar_dia.json` y `voz_vc1.json`, en las partidas de RG69r+voz, con las demás clases de criatura para comparar donde tenga sentido:

| | cómo se mide |
|---|---|
| M1 | **los balances:** en cada turno despierta (`dormida` = 0), cuerpo = placer − displacer, recursos = alegría − enfado, vínculo = amor − tristeza (las seis sumas del registro de criaturas). **Felicidad funcional:** los tres > 0. **Por criatura:** la parte de sus turnos despierta así, y la media de cada balance. **De la aldea, por partida:** la media de las ocho criaturas y la peor parada (la criatura con la parte menor). Se dice por mundo, con la media y la mediana de las partidas. (RG068r no tiene filas de ganancia: su 0 % es por construcción) |
| M2 | **un momento hygge** es un turno al anochecer o de noche en que la criatura: está en su casa (sitio C), su hermana viva está también en esa casa, no está flaca, no ve la bestia y tiene los tres balances > 0 (despierta o dormida). **Se cuenta,** por criatura y por noche, el número de esos turnos y la parte de las noches con al menos uno. Por mundo |
| M3 | **la marca emocional de un recuerdo de sitio** («sitio:<terreno>», por situación día o noche) es su efecto en cuerpo y en recursos y su importancia, pesados por la intensidad. **La media,** por tipo de sitio y situación, de todos los recuerdos vividos de todas las criaturas al acabar la partida (`cuaderno_sitios.json`). Por mundo |
| M4 | **tres mapas por mundo** (figuras, casilla a casilla, sumando las 40 partidas de RG69r+voz): **bienestar,** la media de (cuerpo + recursos + vínculo) de las criaturas despiertas en esa casilla; **miedo,** los golpes de la bestia (`bestia_pega`) y los robos de la bestia (`bestia_roba`) en la casilla de la criatura; **peleas,** los empujones entre criaturas (`empujon`) y los robos (con `soltado`) en la casilla de quien recibe el empujón |
| M5 | **el huerto:** cuántas veces se trabaja una planta («trabajar» con éxito) por partida, por clase y mundo; y, en RG69r+voz, quién: la parte de cada criatura (la que más, las dos de cada casa) |
| M6 | **el perdón:** por cada robo de una vecina a una criatura de RG69r+voz (como en M8), lo que vale la ladrona en el radar de la robada (cuerpo + recursos + vínculo, de `radar_dia.json`) el día del robo; y los días hasta que vuelve a ese valor o más. Si no vuelve antes del final o de que muera una de las dos, queda «sin volver». Se dice la mediana de los días y la parte sin volver, por mundo |
| M7 | de las recogidas de RG69r+voz con vuelta, la parte que vuelve (a 5 casillas o menos de su casa) al anochecer o de noche (`analiza_arbol_v50`) |
| M8 | por cada par (criatura de RG69r+voz, vecina): «le ha robado» si la vecina ganó un empujón contra ella y se llevó algo (evento `empujon` con `soltado`). Para cada par ladrón, la comida que recibe la vecina por día que viven las dos **desde el primer robo**; para cada par que nunca le robó, por día que viven las dos en toda la partida. Media de esas tasas por par, en cada mundo con al menos un robo de una vecina |
| A1 | por mundo, sumando las 40 partidas de RG69r+voz: la comida y la medicina dadas con éxito, en la casilla de quien da (figura), junto al mapa del bienestar de M4 |
| A2 | las criaturas de RG69r+voz cuya hermana muere el día 5 o después y viven al menos 5 días más, frente a las de la misma partida que conservan a su hermana esos días. En los 5 días antes y los 5 después: la felicidad funcional, la felicidad en casa, la parte de las noches que se duerme en casa, la parte del tiempo pegada a una vecina de día y de noche. Y los días hasta recuperar la felicidad de antes |
| A4 | en esos mismos casos, de `filas.jsonl.gz`: **el duelo** (S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO), **la soledad** (S-SOLEDAD; en todos sus turnos despierta y en los de su casa) y **la falta de la hermana viva** (S-COMPANIA). Medias por turno despierta: antes (5 días), el día después y el peor de los 5 después. Y, desde ese peor día, los días hasta bajar a la mitad de la subida y a una décima |
| M9 | la medida de P11 del v5, palabra por palabra (ver arriba), en las decisiones de RG69r+voz; también sin las de ir |
| M10 | vivas de RG69r+voz − vivas de RG068r, emparejadas por semilla, en cada mundo, con su intervalo |
| M11 | por partida, en las cuatro clases de criatura: el hambre media de las vivas en el primer turno del día 10 y del día 30; las muertes de hambre (fin.json) con el día de 10 a 14 y de 30 a 34; las vivas sin comida en la bolsa ni en la despensa en el primer turno del día 10 y del 30 (como P27). Medias por mundo |
| M12 | de `voz_vc1.json` y `voz_a_casa_v1/voces_v1.voces` (las reglas del 143): por partida de RG69r+voz, las voces; por criatura y día viva; la parte que se devuelve (la que la oye da la suya mientras dura); la parte en que las dos están dentro de su casa a la vez en algún turno de los 44; la parte en que «ir a casa» ya era lo elegido por la que la da; y las decisiones oyendo en que cambió lo elegido |
| M13 | la comida que le quitan a empujones: de lo que coge de fuera de la despensa en los días 0 a 9, la parte que acaba en manos de otra por un empujón (`extrae_hg_v1`, 144); los turnos al frío: por criatura y día viva, los turnos en una fase fría fuera de cualquier casa (`analiza_vc1`, 143). En las cuatro clases de criatura |
| M14 | de `fin.json`, cada muerte con su causa y su día, en las cuatro clases de criatura, sumadas en las 40 partidas de cada mundo. **Las causas:** hambre, bestia, frío (la causa «frío» del registro) y otras (cualquier otra: golpe, terreno…). **Se declara:** en el mundo de ahora el frío no mata por sí mismo, sube el hambre (prompt 55, `valle/mundo.py`); se espera la columna del frío a cero, y lo que mata el frío sale como hambre. **La época** es la del calendario de las épocas del mundo (`valle/config_valle.json`, `matorrales.epocas`: épocas de 5 días en ciclo, abundancia, normal, escasez, normal; leídas de la config, no copiadas) en el día de la muerte; también en los mundos que no tienen las épocas encendidas (normal y bestias que crían), donde es solo el día del calendario |

**Lo que miden los programas aparte:** M1 a M6, A1, A2 y A4 salen de los programas del v5 adaptados a la protagonista, que se escriben mientras se juega, con las medidas tal como están descritas arriba. Todo lo demás sale de `evalua_experimento_v6.py`.

## Antes de sellar

- **Las 8 puertas** (prompt 149, `lanza_experimento_v6.py puerta` → `salida/puerta_experimento_v6.json`). Con el código congelado y sin los registros, partidas enteras de 40 días en sequía dura 30121, **idénticas** en muertes, criaturas al acabar, mundo y criaturas línea a línea:

| partida | frente a | idéntica |
|---|---|---|
| el tonto | la del v5 (`valle_experimento_v5`) | sí |
| el recolector | la del v5 | sí |
| RG68r | la del v5 | sí |
| RG068r | la del v5 | sí |
| RG69r con la reserva apagada | RG68r del v5 | sí |
| RG69r+voz con la voz apagada | RG69r del taller del 146 (`valle_rg69_taller`) | sí |
| RG69r, encendida | RG69r del taller del 146 | sí |
| RG69r+voz, encendida | RG69r+voz del taller del 147 (`valle_vr1_taller`) | sí |

- **Apuntar no cambia nada** (`lanza_experimento_v6.py prueba` → `salida/prueba_experimento_v6.json`). RG69r+voz (normal, 9101) y RG69r (bestias que crían, 9102), 10 días, salen idénticas con los registros y sin ellos:
  - RG69r+voz escribe las decisiones, el balance, las filas, el cuaderno, las cuentas, `reserva_v69.json` y `voz_vc1.json`;
  - RG69r escribe todo menos las decisiones y la voz, como debe.
- **Las semillas** 30161–30200 no las lleva ninguna partida del disco (`preparar_v6/semillas_v6.md`). En el repositorio solo salen la 30161, en el lanzador y el evaluador del v6, y un falso positivo de la 30175 (parte de un número largo de una partida de paintball). La carpeta oficial `valle_experimento_v6` no existe antes de lanzar.
- **El evaluador, pasado por los talleres** (prompt 149: `evalua_experimento_v6.py talleres`, 420 partidas, `salida/evalua_talleres_v6.md`): mide todo. Tras añadir M14 y el «4 de las 200» del experimento, lo he vuelto a pasar por los talleres y da las mismas predicciones (`salida/evalua_talleres_v6.md`: 23 de 23 se cumplirían, como en el 149; lo único nuevo es la tabla de M14, y sus totales cuadran con la de las muertes).
- **Las huellas:**
  - el congelado es la etiqueta `valle-congelado-v6` (`CONGELADO_P8_v6.md`, md5 `3c332f41cc9510b5ce59b1cf2d31f92d`);
  - el lanzador del experimento es `lanza_experimento_v6.py`, md5 `b2e1b7077c3fe81cc5b874ec64757e87`;
  - el evaluador es `evalua_experimento_v6.py`, md5 `763dec488835e0783231b6acf2d7d193`.
- **El evaluador** (`evalua_experimento_v6.py`) está escrito antes de jugar. Los programas de M1 a M6, A1, A2 y A4 se adaptan del v5 mientras se juega, con las medidas tal como están descritas arriba.

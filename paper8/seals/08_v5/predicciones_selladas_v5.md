# Predicciones selladas v5: el experimento de la base del ocho, v5

*15-nov-2026, antes de jugar ninguna partida del experimento. Sobre el congelado `valle-congelado-v5` (`CONGELADO_P8_v5.md`, RG68r). Lo que no se cumpla se cuenta igual.*

*Es `predicciones_selladas_v4.md` con los nombres de las clases cambiados (RG61r → RG68r, RG061r → RG068r, S61 → S68, S061 → S068, P61 → P68) y solo los cambios que pidió Manel en el prompt 134: P16 y P17 cambian; P18 a P23 son nuevas, todas de RG68r frente a RG61r (que juega como referencia) en las mismas semillas, emparejadas. Las demás, palabra por palabra.*
- *He quitado las marcas «(cambia)» y «(nueva)» del v4, porque eran respecto al v3.*
- *El diseño (jugadores, semillas, partidas, lanzador, carpeta) y «Antes de sellar» dicen lo del v5.*
- *En «Cómo se mide» van las filas de P16 a P23, la medida del hambre corregida y la de los despertares por noche (los programas de medida del v4, con esas dos).*

## El diseño

- **Jugadores:** RG68r, RG068r, S68, S068, P68, RG61r (la base del v4, como referencia), el tonto y el recolector.
- **Mundos:** los cinco (abundancia, normal, sequía, sequía dura y bestias que crían), con el árbol de fruta dulce encendido.
- **Semillas:** 30121–30160, nunca usadas (`congelado_v5/semillas_v5.md`).
- **Partidas:** de 40 días; 8 × 5 × 40 = 1.600.
- **Diferencias:** por semillas emparejadas, con intervalo del 95 %.
- **El lanzador:** `lanza_experimento_v5.py`, reanudable y con el Mac despierto. Juega en la carpeta oficial `valle_experimento_v5`, sin pruebas mezcladas.
- **Lo que se apunta:**
  - **en RG68r,** el registro de decisiones con las de ir (`decisiones.jsonl.gz`, el lanzador arreglado del prompt 101);
  - **en las seis clases de criatura,** por criatura y turno:
    - el balance de cada dimensión, la casilla, el sitio, si está dormida y si ve la bestia (`balance.jsonl.gz`);
    - las filas de duelo, soledad y compañía de la foto de ahora (`filas.jsonl.gz`: S-DUELO-CUERPO, S-DUELO-RECURSOS, S-DUELO-VINCULO, S-SOLEDAD, S-COMPANIA), para no tener que volver a jugar;
  - **y al acabar cada partida,** los recuerdos de sitios del cuaderno (`cuaderno_sitios.json`) y las cuentas de la v61 (`cuenta_v61.json`: los apuntes de regalo que ya no se hacen y los robos que bajan el trato).

## Las predicciones (el texto de Manel)

P1. En sequía, sequía dura y bestias que crían, RG68r vive al menos una criatura más que el tonto, con el intervalo por encima de cero.
P2. En abundancia y normal, RG68r vive de media al menos 7,5 de 8. Declarado: en el normal, el tonto puede vivir algo más.
P3. Ninguna muerte por golpe entre criaturas en ningún mundo.
P4. Con la bestia a la vista, la fracción de veces con otra pegada es al menos el triple en RG68r que en el tonto.
P5. En bestias que crían, RG68r echa la bestia al menos una vez por partida de media.
P6. RG68r da más comida a la hermana que a cada vecina, por cabeza, en todos los mundos.
P7. La parte de lo que RG68r da a quien está flaca es mayor en sequía y en sequía dura que en abundancia.
P8. En los cinco días siguientes a la muerte de la hermana, RG68r pasa más tiempo con vecinas que en los cinco anteriores, emparejado por criatura.
P9. RG68r duerme dentro de su casa al menos el 55 % de las noches en los cinco mundos, y ninguna noche en una puerta sin estar agotada.
P10. En la sequía y en la sequía dura, RG068r vive igual o más que RG68r.
P11. En los momentos más ambivalentes RG68r y S68 coinciden más (Q4 menos Q1 mayor que cero, con el intervalo sobre cero), y quitando las decisiones en que alguna de las dos da, la diferencia es menor que cero. **Se declara que esta predicción sale del diagnóstico del v3** (`informe_diagnostico_v4.md`, punto 1).
P12. Sin razón, RG68r coge menos del 15 % de la fruta del árbol y menos que el recolector. (La hora de las vueltas pasa a medida sin predicción, M7.)
P13. Sin ninguna regla que lo impida, RG68r no da su última comida con más de 60 de hambre propia en más de 2 de cada 100 partidas.
P16. **(cambia)** RG68r empuja más que RG068r en los cinco mundos.
P17. **(cambia)** Hay rachas de regalos de ida y vuelta de más de 10 en 4 o menos de las 200 partidas de RG68r.
P18. **(nueva)** Los despertares por voz quedan por debajo de 1 por criatura y noche en los cinco mundos.
P19. **(nueva)** La felicidad de la aldea es mayor con el intervalo sobre cero en al menos cuatro mundos.
P20. **(nueva)** Las vivas no son menos con el intervalo bajo cero en ningún mundo.
P21. **(nueva)** Empuja menos en los cinco mundos.
P22. **(nueva)** Duerme dentro de casa más noches en los cinco mundos.
P23. **(nueva)** El hambre media corregida sube menos de 2 puntos en los cinco mundos.

*P18 a P23 son todas de RG68r frente a RG61r en las mismas semillas, emparejadas. P14 sigue como medida sin predicción (M8); P15 sigue quitada.*


## Las medidas sin predicción

**Las del v3** (el texto de Manel, sin cambiar nada):

M1. Felicidad funcional: en cada turno despierta, el balance de cada dimensión es la fuerza de ganancia menos la de pérdida; la criatura está en felicidad funcional cuando las tres están en positivo a la vez. Por criatura, la parte del tiempo así y la media de los tres balances; de la aldea, la media y la peor parada.
M2. Momentos hygge: al atardecer o de noche, en su casa, con la hermana dentro, sin estar flaca, sin la bestia a la vista y con las tres dimensiones en positivo. Cuántos por criatura y por noche.
M3. Lo que siente en cada sitio según sus recuerdos: la marca emocional media de los recuerdos del cuaderno por tipo de sitio.
M4. Los tres mapas del valle por mundo: por casilla, el balance medio (bienestar), la pérdida por la bestia (miedo), y los empujones y robos (peleas).
M5. El huerto: cuántas veces se trabaja y por quién.
M6. El perdón: después de un robo, cuántos días tarda en volver lo que vale la ladrona en el radar de la robada a lo que valía antes.

**Las que salen de las predicciones del v3:**

M7. (era la segunda parte de P12) La hora de las vueltas del árbol: la parte de las vueltas de RG68r después de anochecer.
M8. (era P14) Las vecinas que le han robado a RG68r reciben de ella menos comida, por cabeza, que las vecinas que nunca le han robado, en los mundos donde hay robos. **Se declara que no sabemos qué saldrá.**

**Las añadidas al v3 después de sellar, que aquí entran desde el principio:**

A1. El mapa de dónde se dan regalos, por mundo, junto al mapa del bienestar.
A2. La criatura que ha perdido a su hermana frente a las que la conservan: su felicidad funcional antes y después de la muerte, su felicidad en casa, si sigue durmiendo en casa, cuántos días tarda en recuperarse, y si busca la compañía de una vecina, también de noche.
A4. En la que pierde a su hermana, las dos señales por separado: la del duelo (la tristeza por la pérdida) y la de la soledad (estar sin ella, sobre todo en casa). Para cada una, cómo está antes de la muerte, cuánto sube después y cuántos días tarda en volver a como estaba.

## Cómo se mide cada predicción y cada medida

*Añadido por mí antes de jugar, para que no haya que elegir después. Las medidas son las del v3 (`evalua_experimento_v3.py`, `medidas_v3.py`, `anadidas_v3.py`, `duelo_soledad_v3.py`), con estos cambios:*
- *dormir, con la cuenta arreglada (`medida_v4/dormir_v4.py`);*
- *P11, con la cifra sin las decisiones de dar;*
- *A4, con las filas apuntadas en la partida (`filas.jsonl.gz`) en vez de volver a jugar.*
- *(v5) el hambre, con la medida corregida (prompt 132, `arreglos_v12/hambre_corr.py`): en cada pareja de partidas (RG68r y RG61r en el mismo mundo y semilla), solo los pares criatura-día en que esa criatura está viva en las dos (algún turno de ese día); el hambre media es la de los turnos vivos de esos pares; los días con hambre > 60, la parte de esos pares con hambre > 60 en algún turno;*
- *(v5) los despertares por noche: los eventos «despierta» del registro del mundo, todos y por voz (motivo «llamada …» o «voz …»), divididos entre las noches-criatura (las criaturas vivas al empezar cada día), por partida.*

**Lo común:**
- **Las vivas** son las del día 40, de 8.
- **Los intervalos** del 95 % salen de un bootstrap de 10.000 remuestreos, con semilla 8: de las semillas emparejadas, o de lo que se diga en cada una.
- **Lo de dar** es solo comida, dada con éxito (registro del mundo), salvo en P17, que cuenta comida y medicina por separado.
- **«Flaca»** es el hambre por encima del umbral de flaca del mundo (60) en el turno anterior.
- **«Vecina»** es cualquier criatura de otra casa.
- **«RG68r»** es la clase. Cuando una predicción no dice otra cosa, se mide en sus 200 partidas (40 por mundo).

| | cómo se mide | se cumple si |
|---|---|---|
| P1 | vivas de RG68r − vivas del tonto, emparejadas por semilla, en cada uno de los tres mundos | en los tres, la media es ≥ 1 y el límite inferior del intervalo es > 0 |
| P2 | la media de vivas de RG68r en abundancia y en normal | las dos son ≥ 7,5 |
| P3 | las muertes con causa «golpe de …», en las 1.600 partidas | no hay ninguna |
| P4 | de los turnos fuera de casa con alguna bestia a la vista de la fase, la parte con otra criatura a una casilla o menos (`cierre_v46`); RG68r frente al tonto, sumando los cinco mundos (también se dice por mundo) | la de RG68r es ≥ 3 veces la del tonto en la suma de los cinco |
| P5 | las veces que se echa una bestia (evento `bestia_echada`), por partida de RG68r, en bestias que crían | la media es ≥ 1 |
| P6 | lo dado a la hermana frente a lo dado a las seis vecinas dividido entre seis, sumando las 40 partidas de cada mundo | en los cinco mundos, lo de la hermana es mayor |
| P7 | la parte de lo dado por RG68r a quien estaba flaca, por mundo | la de la sequía y la de la sequía dura son las dos mayores que la de la abundancia |
| P8 | por cada criatura de RG68r que pierde a su hermana y sigue viva 5 días o más: la parte del día pegada a una vecina viva, la media de los 5 días después menos la de los 5 antes (`analiza_v45`, como en el v2); todas las criaturas de los cinco mundos, con intervalo por bootstrap de criaturas | la media es > 0 y el límite inferior del intervalo es > 0 |
| P9 | **la primera vez que se duerme cada criatura cada noche** (`medida_v4/dormir_v4.py`): por criatura viva y por día, el primer turno del anochecer o de la noche en que está dormida (si ya dormía, el primero del anochecer). Se mide la parte dentro de su casa (sin la puerta), por mundo, y las veces en una puerta sin estar agotada (`agotada` del registro del mundo, ese turno o el anterior) | ≥ 55 % dentro en los cinco mundos, y 0 en una puerta sin estar agotada en las 200 partidas |
| P10 | vivas de RG068r − vivas de RG68r, emparejadas por semilla, en la sequía y en la sequía dura | en los dos, el límite superior del intervalo es ≥ 0 (RG068r no vive claramente menos) |
| P11 | la medida de C5 de `evalua_confirmacion.py`, en los estados de RG68r, con todas las decisiones, también las de ir (ver abajo); y la misma medida, en la misma muestra, quitando las decisiones en que RG68r elige dar o las sumas (el valorador de S68) eligen dar | Q4 − Q1 > 0 con el límite inferior del intervalo > 0; y, sin las de dar, Q4 − Q1 < 0 (se da su intervalo) |
| P12 | de las frutas puestas, la parte cogida (puestas menos perdidas), en las partidas de RG68r y en las del recolector, sumando los cinco mundos (`analiza_arbol_v50`) | RG68r coge < 15 % y menos que el recolector |
| P13 | las partidas de RG68r con al menos un «dar comida» con éxito en el que quien da llevaba una sola comida y tenía el hambre > 60 en el turno anterior | como mucho 2 de cada 100: ≤ 4 de las 200 |
| P16 | los empujones a otra criatura por partida (`cierre_v46`: «empujar» a otra criatura, no a la bestia, sin resultado «no:»), RG68r y RG068r, en cada mundo | en los cinco mundos, la media por partida de RG68r es mayor que la de RG068r |
| P17 | en cada partida, por par de criaturas y tipo (comida, medicina), la racha más larga de regalos que van y vuelven (A→B, B→A, …) con menos de 40 turnos entre uno y otro (`comprueba_v58.bucles`), en las 200 partidas de RG68r (también se dice para las otras clases de criatura) | las partidas de RG68r con alguna racha > 10 (de comida o de medicina) son 4 o menos de las 200 |
| P18 | los despertares por voz (motivo «llamada …» o «voz …») de RG68r, sumados en las 40 partidas de cada mundo, entre sus noches-criatura (se da también RG61r y la diferencia emparejada) | en los cinco mundos, < 1 por criatura y noche |
| P19 | la felicidad funcional de la aldea (M1: la media de las ocho criaturas, por partida), RG68r − RG61r, emparejadas por semilla, en cada mundo | en al menos cuatro mundos, el límite inferior del intervalo es > 0 |
| P20 | vivas de RG68r − vivas de RG61r, emparejadas por semilla, en cada mundo | en ningún mundo el límite superior del intervalo es < 0 |
| P21 | los empujones a otra criatura por partida (como en P16), RG68r y RG61r, en cada mundo (se da también la diferencia emparejada) | en los cinco mundos, la media por partida de RG68r es menor que la de RG61r |
| P22 | la parte de las noches en que se duerme dentro de su casa (la cuenta de P9, `medida_v4/dormir_v4.py`), RG68r y RG61r, en cada mundo | en los cinco mundos, la de RG68r es mayor que la de RG61r |
| P23 | el hambre media con la medida corregida, RG68r − RG61r, emparejadas por semilla, en cada mundo (con su intervalo) | en los cinco mundos, la media de la diferencia es < 2 |

**P11, con detalle:**
- **De dónde salen las decisiones:** en cada decisión de RG68r, `decisiones.jsonl.gz` guarda la opción elegida y la que elegiría cada valorador (el motor, las sumas y la posición) en el mismo estado exacto, **también las de ir**. Es el lanzador arreglado del prompt 101 (`medida_v3/lanza_medida_v3.py`).
- **La medida es la del v2 y el v3, sin cambiar:**
  - cómo se desempata: con las reglas de empate de ahora;
  - la muestra: 2.000 decisiones por mundo, con la semilla del muestreo «8|RG68r|<mundo>»;
  - la ambivalencia: la mayor de las tres dimensiones, y la de cada una es la menor de su ganancia y su pérdida (`ambivalencia.py`);
  - los cuartos van dentro de cada mundo;
  - se compara Q4 − Q1 de `igual_sumas`, sumando los cinco mundos;
  - el intervalo, por bootstrap de partidas.
- **La segunda parte usa la misma muestra y los mismos cuartos,** quitando las decisiones en que la elegida o la de las sumas es «dar» (como en `diagnostico_v4/p11_diag.py`).
- **Se dirá también la cifra sin las decisiones de ir.**

**Las medidas sin predicción** (se dicen; no se cumplen ni fallan). Salen de `balance.jsonl.gz`, `filas.jsonl.gz`, `mundo.jsonl.gz`, `cuaderno_sitios.json` y `radar_dia.json`, en las partidas de RG68r, con las demás clases de criatura para comparar donde tenga sentido:

| | cómo se mide |
|---|---|
| M1 | **los balances:** en cada turno despierta (`dormida` = 0), cuerpo = placer − displacer, recursos = alegría − enfado, vínculo = amor − tristeza (las seis sumas del registro de criaturas). **Felicidad funcional:** los tres > 0. **Por criatura:** la parte de sus turnos despierta así, y la media de cada balance. **De la aldea, por partida:** la media de las ocho criaturas y la peor parada (la criatura con la parte menor). Se dice por mundo, con la media y la mediana de las partidas. (RG068r y S068 no tienen filas de ganancia: su 0 % es por construcción) |
| M2 | **un momento hygge** es un turno al anochecer o de noche en que la criatura: está en su casa (sitio C), su hermana viva está también en esa casa, no está flaca, no ve la bestia y tiene los tres balances > 0 (despierta o dormida). **Se cuenta,** por criatura y por noche, el número de esos turnos y la parte de las noches con al menos uno. Por mundo |
| M3 | **la marca emocional de un recuerdo de sitio** («sitio:<terreno>», por situación día o noche) es su efecto en cuerpo y en recursos y su importancia, pesados por la intensidad. **La media,** por tipo de sitio y situación, de todos los recuerdos vividos de todas las criaturas al acabar la partida (`cuaderno_sitios.json`). Por mundo |
| M4 | **tres mapas por mundo** (figuras, casilla a casilla, sumando las 40 partidas de RG68r): **bienestar,** la media de (cuerpo + recursos + vínculo) de las criaturas despiertas en esa casilla; **miedo,** los golpes de la bestia (`bestia_pega`) y los robos de la bestia (`bestia_roba`) en la casilla de la criatura; **peleas,** los empujones entre criaturas (`empujon`) y los robos (con `soltado`) en la casilla de quien recibe el empujón |
| M5 | **el huerto:** cuántas veces se trabaja una planta («trabajar» con éxito) por partida, por clase y mundo; y, en RG68r, quién: la parte de cada criatura (la que más, las dos de cada casa) |
| M6 | **el perdón:** por cada robo de una vecina a una criatura de RG68r (como en M8), lo que vale la ladrona en el radar de la robada (cuerpo + recursos + vínculo, de `radar_dia.json`) el día del robo; y los días hasta que vuelve a ese valor o más. Si no vuelve antes del final o de que muera una de las dos, queda «sin volver». Se dice la mediana de los días y la parte sin volver, por mundo |
| M7 | de las recogidas de RG68r con vuelta, la parte que vuelve (a 5 casillas o menos de su casa) al anochecer o de noche (`analiza_arbol_v50`) |
| M8 | por cada par (criatura de RG68r, vecina): «le ha robado» si la vecina ganó un empujón contra ella y se llevó algo (evento `empujon` con `soltado`). Para cada par ladrón, la comida que recibe la vecina por día que viven las dos **desde el primer robo**; para cada par que nunca le robó, por día que viven las dos en toda la partida. Media de esas tasas por par, en cada mundo con al menos un robo de una vecina |
| A1 | por mundo, sumando las 40 partidas de RG68r: la comida y la medicina dadas con éxito, en la casilla de quien da (figura), junto al mapa del bienestar de M4 (`anadidas_v3.py`) |
| A2 | las criaturas de RG68r cuya hermana muere el día 5 o después y viven al menos 5 días más, frente a las de la misma partida que conservan a su hermana esos días. En los 5 días antes y los 5 después: la felicidad funcional, la felicidad en casa, la parte de las noches que se duerme en casa, la parte del tiempo pegada a una vecina de día y de noche. Y los días hasta recuperar la felicidad de antes (`anadidas_v3.py`) |
| A4 | en esos mismos casos, de `filas.jsonl.gz`: **el duelo** (S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO), **la soledad** (S-SOLEDAD; en todos sus turnos despierta y en los de su casa) y **la falta de la hermana viva** (S-COMPANIA). Medias por turno despierta: antes (5 días), el día después y el peor de los 5 después. Y, desde ese peor día, los días hasta bajar a la mitad de la subida y a una décima (`duelo_soledad_v3.py`) |

## Antes de sellar

- **La comprobación jugada** (`lanza_experimento_v5.py puerta` → `salida/puerta_experimento_v5.json`), con el código congelado y sin los registros nuevos, sale **idéntica** en muertes, criaturas, mundo y criaturas línea a línea:
  - RG68r (bestias que crían, 1004), frente a su partida de M (`valle_arreglos_v11/RG67r_M_bestias_crian+sabores_s1004_d40`), la del taller del prompt 131: es el mismo jugador con otro nombre;
  - el tonto (normal, 30001), frente a `valle_experimento_v2`.
- **Apuntar no cambia nada** (`lanza_experimento_v5.py prueba` → `salida/prueba_experimento_v5.json`):
  - RG68r (normal, 9101) y RG068r (bestias que crían, 9102), 10 días, con los registros y sin ellos, salen idénticas;
  - con ellos, RG68r apunta 23.089 decisiones, 3.422 de ellas de ir, más el balance, las filas de duelo, soledad y compañía, los recuerdos de sitios y las cuentas de la v61 (`medida_v5/mira_prueba_v5.py`).
- **Las medidas nuevas del evaluador** (los despertares, la felicidad y el hambre corregida) dan lo mismo que las del taller del prompt 132 en tres partidas que ya existían (`salida/prueba_evalua_v5.py`: M en normal 1001, felicidad de la aldea 0,768 y 28 despertares en 320 noches-criatura, como en `arreglos_v12/compara_v12`).
- **Las semillas** 30121–30160 no las lleva ninguna partida del disco (`congelado_v5/semillas_v5.md`).
- **Las huellas:**
  - el congelado es la etiqueta `valle-congelado-v5` (`CONGELADO_P8_v5.md`, md5 `27540ecfd66ee14ab96dd192942fa413`);
  - el lanzador del experimento es `lanza_experimento_v5.py`, md5 `b61ba0b3924b63d1227db699bea91c94`;
  - el evaluador es `evalua_experimento_v5.py`, md5 `ef52cfbc5fa4773110604bbd5de93364`.
- **El evaluador** (`evalua_experimento_v5.py`) está escrito antes de jugar. Los programas de las medidas sin predicción se adaptan del v4 mientras se juega, con las medidas tal como están descritas arriba.

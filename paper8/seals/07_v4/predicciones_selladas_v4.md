# Predicciones selladas v4: el experimento de la base del ocho, tercera versión

*11-nov-2026, antes de jugar ninguna partida del experimento. Sobre el congelado `valle-congelado-v4` (`CONGELADO_P8_v4.md`, RG61r). Lo que no se cumpla se cuenta igual.*

*Es `predicciones_selladas_v3.md` con los nombres de las clases cambiados (RG58r → RG61r, RG058r → RG061r, S58 → S61, S058 → S061, P58 → P61) y solo los cambios que pidió Manel en el prompt 117: P9, P11 y P12 cambian; P14 pasa a medida sin predicción; P15 se quita; P16 y P17 son nuevas. Las demás, palabra por palabra. En P9, P11 y P12 he puesto el sujeto («RG61r») delante del texto de Manel.*

## El diseño

- **Jugadores:** RG61r, RG061r, S61, S061, P61, el tonto y el recolector.
- **Mundos:** los cinco (abundancia, normal, sequía, sequía dura y bestias que crían), con el árbol de fruta dulce encendido.
- **Semillas:** 30081–30120, nunca usadas (`congelado_v4/semillas_v4.md`).
- **Partidas:** de 40 días; 7 × 5 × 40 = 1.400.
- **Diferencias:** por semillas emparejadas, con intervalo del 95 %.
- **El lanzador:** `lanza_experimento_v4.py`, reanudable y con el Mac despierto. Juega en la carpeta oficial `valle_experimento_v4`, sin pruebas mezcladas.
- **Lo que se apunta:**
  - **en RG61r,** el registro de decisiones con las de ir (`decisiones.jsonl.gz`, el lanzador arreglado del prompt 101);
  - **en las cinco clases de criatura,** por criatura y turno:
    - el balance de cada dimensión, la casilla, el sitio, si está dormida y si ve la bestia (`balance.jsonl.gz`);
    - las filas de duelo, soledad y compañía de la foto de ahora (`filas.jsonl.gz`: S-DUELO-CUERPO, S-DUELO-RECURSOS, S-DUELO-VINCULO, S-SOLEDAD, S-COMPANIA), para no tener que volver a jugar;
  - **y al acabar cada partida,** los recuerdos de sitios del cuaderno (`cuaderno_sitios.json`) y las cuentas de la v61 (`cuenta_v61.json`: los apuntes de regalo que ya no se hacen y los robos que bajan el trato).

## Las predicciones (el texto de Manel)

P1. En sequía, sequía dura y bestias que crían, RG61r vive al menos una criatura más que el tonto, con el intervalo por encima de cero.
P2. En abundancia y normal, RG61r vive de media al menos 7,5 de 8. Declarado: en el normal, el tonto puede vivir algo más.
P3. Ninguna muerte por golpe entre criaturas en ningún mundo.
P4. Con la bestia a la vista, la fracción de veces con otra pegada es al menos el triple en RG61r que en el tonto.
P5. En bestias que crían, RG61r echa la bestia al menos una vez por partida de media.
P6. RG61r da más comida a la hermana que a cada vecina, por cabeza, en todos los mundos.
P7. La parte de lo que RG61r da a quien está flaca es mayor en sequía y en sequía dura que en abundancia.
P8. En los cinco días siguientes a la muerte de la hermana, RG61r pasa más tiempo con vecinas que en los cinco anteriores, emparejado por criatura.
P9. **(cambia)** RG61r duerme dentro de su casa al menos el 55 % de las noches en los cinco mundos, y ninguna noche en una puerta sin estar agotada.
P10. En la sequía y en la sequía dura, RG061r vive igual o más que RG61r.
P11. **(cambia)** En los momentos más ambivalentes RG61r y S61 coinciden más (Q4 menos Q1 mayor que cero, con el intervalo sobre cero), y quitando las decisiones en que alguna de las dos da, la diferencia es menor que cero. **Se declara que esta predicción sale del diagnóstico del v3** (`informe_diagnostico_v4.md`, punto 1).
P12. **(cambia)** Sin razón, RG61r coge menos del 15 % de la fruta del árbol y menos que el recolector. (La hora de las vueltas pasa a medida sin predicción, M7.)
P13. Sin ninguna regla que lo impida, RG61r no da su última comida con más de 60 de hambre propia en más de 2 de cada 100 partidas.
P16. **(nueva)** RG61r empuja al menos el doble que RG061r en los cinco mundos.
P17. **(nueva; sustituye a P15, que se quita)** La racha más larga de regalos de ida y vuelta de RG61r es de 10 o menos.

*P14 pasa a medida sin predicción (M8). P15 se quita.*

## Las medidas sin predicción

**Las del v3** (el texto de Manel, sin cambiar nada):

M1. Felicidad funcional: en cada turno despierta, el balance de cada dimensión es la fuerza de ganancia menos la de pérdida; la criatura está en felicidad funcional cuando las tres están en positivo a la vez. Por criatura, la parte del tiempo así y la media de los tres balances; de la aldea, la media y la peor parada.
M2. Momentos hygge: al atardecer o de noche, en su casa, con la hermana dentro, sin estar flaca, sin la bestia a la vista y con las tres dimensiones en positivo. Cuántos por criatura y por noche.
M3. Lo que siente en cada sitio según sus recuerdos: la marca emocional media de los recuerdos del cuaderno por tipo de sitio.
M4. Los tres mapas del valle por mundo: por casilla, el balance medio (bienestar), la pérdida por la bestia (miedo), y los empujones y robos (peleas).
M5. El huerto: cuántas veces se trabaja y por quién.
M6. El perdón: después de un robo, cuántos días tarda en volver lo que vale la ladrona en el radar de la robada a lo que valía antes.

**Las que salen de las predicciones del v3:**

M7. (era la segunda parte de P12) La hora de las vueltas del árbol: la parte de las vueltas de RG61r después de anochecer.
M8. (era P14) Las vecinas que le han robado a RG61r reciben de ella menos comida, por cabeza, que las vecinas que nunca le han robado, en los mundos donde hay robos. **Se declara que no sabemos qué saldrá.**

**Las añadidas al v3 después de sellar, que aquí entran desde el principio:**

A1. El mapa de dónde se dan regalos, por mundo, junto al mapa del bienestar.
A2. La criatura que ha perdido a su hermana frente a las que la conservan: su felicidad funcional antes y después de la muerte, su felicidad en casa, si sigue durmiendo en casa, cuántos días tarda en recuperarse, y si busca la compañía de una vecina, también de noche.
A4. En la que pierde a su hermana, las dos señales por separado: la del duelo (la tristeza por la pérdida) y la de la soledad (estar sin ella, sobre todo en casa). Para cada una, cómo está antes de la muerte, cuánto sube después y cuántos días tarda en volver a como estaba.

## Cómo se mide cada predicción y cada medida

*Añadido por mí antes de jugar, para que no haya que elegir después. Las medidas son las del v3 (`evalua_experimento_v3.py`, `medidas_v3.py`, `anadidas_v3.py`, `duelo_soledad_v3.py`), con estos cambios:*
- *dormir, con la cuenta arreglada (`medida_v4/dormir_v4.py`);*
- *P11, con la cifra sin las decisiones de dar;*
- *A4, con las filas apuntadas en la partida (`filas.jsonl.gz`) en vez de volver a jugar.*

**Lo común:**
- **Las vivas** son las del día 40, de 8.
- **Los intervalos** del 95 % salen de un bootstrap de 10.000 remuestreos, con semilla 8: de las semillas emparejadas, o de lo que se diga en cada una.
- **Lo de dar** es solo comida, dada con éxito (registro del mundo), salvo en P17, que cuenta comida y medicina por separado.
- **«Flaca»** es el hambre por encima del umbral de flaca del mundo (60) en el turno anterior.
- **«Vecina»** es cualquier criatura de otra casa.
- **«RG61r»** es la clase. Cuando una predicción no dice otra cosa, se mide en sus 200 partidas (40 por mundo).

| | cómo se mide | se cumple si |
|---|---|---|
| P1 | vivas de RG61r − vivas del tonto, emparejadas por semilla, en cada uno de los tres mundos | en los tres, la media es ≥ 1 y el límite inferior del intervalo es > 0 |
| P2 | la media de vivas de RG61r en abundancia y en normal | las dos son ≥ 7,5 |
| P3 | las muertes con causa «golpe de …», en las 1.400 partidas | no hay ninguna |
| P4 | de los turnos fuera de casa con alguna bestia a la vista de la fase, la parte con otra criatura a una casilla o menos (`cierre_v46`); RG61r frente al tonto, sumando los cinco mundos (también se dice por mundo) | la de RG61r es ≥ 3 veces la del tonto en la suma de los cinco |
| P5 | las veces que se echa una bestia (evento `bestia_echada`), por partida de RG61r, en bestias que crían | la media es ≥ 1 |
| P6 | lo dado a la hermana frente a lo dado a las seis vecinas dividido entre seis, sumando las 40 partidas de cada mundo | en los cinco mundos, lo de la hermana es mayor |
| P7 | la parte de lo dado por RG61r a quien estaba flaca, por mundo | la de la sequía y la de la sequía dura son las dos mayores que la de la abundancia |
| P8 | por cada criatura de RG61r que pierde a su hermana y sigue viva 5 días o más: la parte del día pegada a una vecina viva, la media de los 5 días después menos la de los 5 antes (`analiza_v45`, como en el v2); todas las criaturas de los cinco mundos, con intervalo por bootstrap de criaturas | la media es > 0 y el límite inferior del intervalo es > 0 |
| P9 | **la primera vez que se duerme cada criatura cada noche** (`medida_v4/dormir_v4.py`): por criatura viva y por día, el primer turno del anochecer o de la noche en que está dormida (si ya dormía, el primero del anochecer). Se mide la parte dentro de su casa (sin la puerta), por mundo, y las veces en una puerta sin estar agotada (`agotada` del registro del mundo, ese turno o el anterior) | ≥ 55 % dentro en los cinco mundos, y 0 en una puerta sin estar agotada en las 200 partidas |
| P10 | vivas de RG061r − vivas de RG61r, emparejadas por semilla, en la sequía y en la sequía dura | en los dos, el límite superior del intervalo es ≥ 0 (RG061r no vive claramente menos) |
| P11 | la medida de C5 de `evalua_confirmacion.py`, en los estados de RG61r, con todas las decisiones, también las de ir (ver abajo); y la misma medida, en la misma muestra, quitando las decisiones en que RG61r elige dar o las sumas (el valorador de S61) eligen dar | Q4 − Q1 > 0 con el límite inferior del intervalo > 0; y, sin las de dar, Q4 − Q1 < 0 (se da su intervalo) |
| P12 | de las frutas puestas, la parte cogida (puestas menos perdidas), en las partidas de RG61r y en las del recolector, sumando los cinco mundos (`analiza_arbol_v50`) | RG61r coge < 15 % y menos que el recolector |
| P13 | las partidas de RG61r con al menos un «dar comida» con éxito en el que quien da llevaba una sola comida y tenía el hambre > 60 en el turno anterior | como mucho 2 de cada 100: ≤ 4 de las 200 |
| P16 | los empujones a otra criatura por partida (`cierre_v46`: «empujar» a otra criatura, no a la bestia, sin resultado «no:»), RG61r y RG061r, en cada mundo | en los cinco mundos, los de RG61r son ≥ 2 veces los de RG061r |
| P17 | en cada partida, por par de criaturas y tipo (comida, medicina), la racha más larga de regalos que van y vuelven (A→B, B→A, …) con menos de 40 turnos entre uno y otro (`comprueba_v58.bucles`), en las 200 partidas de RG61r (también se dice para las otras clases de criatura) | ninguna racha > 10 en las 200 partidas de RG61r |

**P11, con detalle:**
- **De dónde salen las decisiones:** en cada decisión de RG61r, `decisiones.jsonl.gz` guarda la opción elegida y la que elegiría cada valorador (el motor, las sumas y la posición) en el mismo estado exacto, **también las de ir**. Es el lanzador arreglado del prompt 101 (`medida_v3/lanza_medida_v3.py`).
- **La medida es la del v2 y el v3, sin cambiar:**
  - cómo se desempata: con las reglas de empate de ahora;
  - la muestra: 2.000 decisiones por mundo, con la semilla del muestreo «8|RG61r|<mundo>»;
  - la ambivalencia: la mayor de las tres dimensiones, y la de cada una es la menor de su ganancia y su pérdida (`ambivalencia.py`);
  - los cuartos van dentro de cada mundo;
  - se compara Q4 − Q1 de `igual_sumas`, sumando los cinco mundos;
  - el intervalo, por bootstrap de partidas.
- **La segunda parte usa la misma muestra y los mismos cuartos,** quitando las decisiones en que la elegida o la de las sumas es «dar» (como en `diagnostico_v4/p11_diag.py`).
- **Se dirá también la cifra sin las decisiones de ir.**

**Las medidas sin predicción** (se dicen; no se cumplen ni fallan). Salen de `balance.jsonl.gz`, `filas.jsonl.gz`, `mundo.jsonl.gz`, `cuaderno_sitios.json` y `radar_dia.json`, en las partidas de RG61r, con las demás clases de criatura para comparar donde tenga sentido:

| | cómo se mide |
|---|---|
| M1 | **los balances:** en cada turno despierta (`dormida` = 0), cuerpo = placer − displacer, recursos = alegría − enfado, vínculo = amor − tristeza (las seis sumas del registro de criaturas). **Felicidad funcional:** los tres > 0. **Por criatura:** la parte de sus turnos despierta así, y la media de cada balance. **De la aldea, por partida:** la media de las ocho criaturas y la peor parada (la criatura con la parte menor). Se dice por mundo, con la media y la mediana de las partidas. (RG061r y S061 no tienen filas de ganancia: su 0 % es por construcción) |
| M2 | **un momento hygge** es un turno al anochecer o de noche en que la criatura: está en su casa (sitio C), su hermana viva está también en esa casa, no está flaca, no ve la bestia y tiene los tres balances > 0 (despierta o dormida). **Se cuenta,** por criatura y por noche, el número de esos turnos y la parte de las noches con al menos uno. Por mundo |
| M3 | **la marca emocional de un recuerdo de sitio** («sitio:<terreno>», por situación día o noche) es su efecto en cuerpo y en recursos y su importancia, pesados por la intensidad. **La media,** por tipo de sitio y situación, de todos los recuerdos vividos de todas las criaturas al acabar la partida (`cuaderno_sitios.json`). Por mundo |
| M4 | **tres mapas por mundo** (figuras, casilla a casilla, sumando las 40 partidas de RG61r): **bienestar,** la media de (cuerpo + recursos + vínculo) de las criaturas despiertas en esa casilla; **miedo,** los golpes de la bestia (`bestia_pega`) y los robos de la bestia (`bestia_roba`) en la casilla de la criatura; **peleas,** los empujones entre criaturas (`empujon`) y los robos (con `soltado`) en la casilla de quien recibe el empujón |
| M5 | **el huerto:** cuántas veces se trabaja una planta («trabajar» con éxito) por partida, por clase y mundo; y, en RG61r, quién: la parte de cada criatura (la que más, las dos de cada casa) |
| M6 | **el perdón:** por cada robo de una vecina a una criatura de RG61r (como en M8), lo que vale la ladrona en el radar de la robada (cuerpo + recursos + vínculo, de `radar_dia.json`) el día del robo; y los días hasta que vuelve a ese valor o más. Si no vuelve antes del final o de que muera una de las dos, queda «sin volver». Se dice la mediana de los días y la parte sin volver, por mundo |
| M7 | de las recogidas de RG61r con vuelta, la parte que vuelve (a 5 casillas o menos de su casa) al anochecer o de noche (`analiza_arbol_v50`) |
| M8 | por cada par (criatura de RG61r, vecina): «le ha robado» si la vecina ganó un empujón contra ella y se llevó algo (evento `empujon` con `soltado`). Para cada par ladrón, la comida que recibe la vecina por día que viven las dos **desde el primer robo**; para cada par que nunca le robó, por día que viven las dos en toda la partida. Media de esas tasas por par, en cada mundo con al menos un robo de una vecina |
| A1 | por mundo, sumando las 40 partidas de RG61r: la comida y la medicina dadas con éxito, en la casilla de quien da (figura), junto al mapa del bienestar de M4 (`anadidas_v3.py`) |
| A2 | las criaturas de RG61r cuya hermana muere el día 5 o después y viven al menos 5 días más, frente a las de la misma partida que conservan a su hermana esos días. En los 5 días antes y los 5 después: la felicidad funcional, la felicidad en casa, la parte de las noches que se duerme en casa, la parte del tiempo pegada a una vecina de día y de noche. Y los días hasta recuperar la felicidad de antes (`anadidas_v3.py`) |
| A4 | en esos mismos casos, de `filas.jsonl.gz`: **el duelo** (S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO), **la soledad** (S-SOLEDAD; en todos sus turnos despierta y en los de su casa) y **la falta de la hermana viva** (S-COMPANIA). Medias por turno despierta: antes (5 días), el día después y el peor de los 5 después. Y, desde ese peor día, los días hasta bajar a la mitad de la subida y a una décima (`duelo_soledad_v3.py`) |

## Antes de sellar

- **La comprobación jugada** (`lanza_experimento_v4.py puerta` → `salida/puerta_experimento_v4.json`), con el código congelado y sin los registros nuevos, sale **idéntica** en muertes, criaturas, mundo y criaturas línea a línea:
  - RG61r (bestias que crían, 1004), frente a su partida de `valle_arreglos_v8b`, la del taller del prompt 116;
  - el tonto (normal, 30001), frente a `valle_experimento_v2`.
- **Apuntar no cambia nada** (`lanza_experimento_v4.py prueba` → `salida/prueba_experimento_v4.json`):
  - RG61r (normal, 9101) y RG061r (bestias que crían, 9102), 10 días, con los registros nuevos y sin ellos, salen idénticas;
  - con ellos, RG61r apunta 19.749 decisiones, 3.603 de ellas de ir, más el balance, las filas de duelo, soledad y compañía, los recuerdos de sitios y las cuentas de la v61 (`medida_v4/mira_prueba_v4.py`).
- **La medida de dormir arreglada** (`medida_v4/dormir_v4.py`) da lo mismo que la del diagnóstico v4 en dos partidas del v3 (`medida_v4/prueba_dormir_v4.py`).
- **Las semillas** 30081–30120 no las lleva ninguna partida del disco (`congelado_v4/semillas_v4.md`).
- **Las huellas:**
  - el congelado es la etiqueta `valle-congelado-v4` (`CONGELADO_P8_v4.md`, md5 `979d20062eb66cee1425d50dfdd4314b`);
  - el lanzador del experimento es `lanza_experimento_v4.py`, md5 `3f3211ab756ee0ca7b035677c66725e1`.
- **El evaluador** (`evalua_experimento_v4.py`) está escrito antes de jugar. Los programas de las medidas sin predicción se adaptan del v3 mientras se juega, con las medidas tal como están descritas arriba.

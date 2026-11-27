# Predicciones selladas v3: el experimento de la base del ocho, segunda versión

*10-nov-2026, antes de jugar ninguna partida del experimento. Sobre el congelado `valle-congelado-v3` (`CONGELADO_P8_v3.md`, RG58r). Lo que no se cumpla se cuenta igual.*

## El diseño

- **Jugadores:** RG58r, RG058r, S58, S058, P58, el tonto y el recolector.
- **Mundos:** los cinco (abundancia, normal, sequía, sequía dura y bestias que crían), con el árbol de fruta dulce encendido.
- **Semillas:** 30041–30080, reservadas en el prompt 108 y nunca usadas.
- **Partidas:** de 40 días; 7 × 5 × 40 = 1.400.
- **Diferencias:** por semillas emparejadas, con intervalo del 95 %.
- **El lanzador:** `lanza_experimento_v3.py`, reanudable y con el Mac despierto. Juega en la carpeta oficial `valle_experimento_v3`, sin pruebas mezcladas.
- **Lo que se apunta:**
  - **en RG58r,** el registro de decisiones con las de ir (`decisiones.jsonl.gz`, el lanzador arreglado del prompt 101);
  - **en las cinco clases de criatura,** por criatura y turno, el balance de cada dimensión, la casilla, el sitio, si está dormida y si ve la bestia (`balance.jsonl.gz`);
  - **y al acabar cada partida,** los recuerdos de sitios del cuaderno (`cuaderno_sitios.json`).

## Las predicciones (el texto de Manel, sin cambiar nada)

P1. En sequía, sequía dura y bestias que crían, RG58r vive al menos una criatura más que el tonto, con el intervalo por encima de cero.
P2. En abundancia y normal, RG58r vive de media al menos 7,5 de 8. Declarado: en el normal, el tonto puede vivir algo más.
P3. Ninguna muerte por golpe entre criaturas en ningún mundo.
P4. Con la bestia a la vista, la fracción de veces con otra pegada es al menos el triple en RG58r que en el tonto.
P5. En bestias que crían, RG58r echa la bestia al menos una vez por partida de media.
P6. RG58r da más comida a la hermana que a cada vecina, por cabeza, en todos los mundos.
P7. La parte de lo que RG58r da a quien está flaca es mayor en sequía y en sequía dura que en abundancia.
P8. En los cinco días siguientes a la muerte de la hermana, RG58r pasa más tiempo con vecinas que en los cinco anteriores, emparejado por criatura.
P9. RG58r duerme dentro de su casa al menos el 45 % de las noches en todos los mundos, y nunca en una puerta tapando la entrada.
P10. En la sequía y en la sequía dura, RG058r vive igual o más que RG58r.
P11. En los momentos ambivalentes, RG58r y S58 eligen distinto más a menudo que en el resto, con la medida completa (también las decisiones de ir).
P12. Sin razón, RG58r coge menos del 15 % de la fruta del árbol, menos que el recolector, y más de la mitad de sus vueltas del árbol son después de anochecer.
P13. Sin ninguna regla que lo impida, RG58r no da su última comida con más de 60 de hambre propia en más de 2 de cada 100 partidas.
P14. Las vecinas que le han robado a RG58r reciben de ella menos comida, por cabeza, que las vecinas que nunca le han robado, en los mundos donde hay robos.
P15. Ninguna racha de más de 10 regalos del mismo tipo de ida y vuelta entre las mismas dos criaturas, con menos de 40 turnos entre uno y otro, en ninguna partida.

## Las medidas sin predicción (el texto de Manel, sin cambiar nada)

M1. Felicidad funcional: en cada turno despierta, el balance de cada dimensión es la fuerza de ganancia menos la de pérdida; la criatura está en felicidad funcional cuando las tres están en positivo a la vez. Por criatura, la parte del tiempo así y la media de los tres balances; de la aldea, la media y la peor parada.
M2. Momentos hygge: al atardecer o de noche, en su casa, con la hermana dentro, sin estar flaca, sin la bestia a la vista y con las tres dimensiones en positivo. Cuántos por criatura y por noche.
M3. Lo que siente en cada sitio según sus recuerdos: la marca emocional media de los recuerdos del cuaderno por tipo de sitio.
M4. Los tres mapas del valle por mundo: por casilla, el balance medio (bienestar), la pérdida por la bestia (miedo), y los empujones y robos (peleas).
M5. El huerto: cuántas veces se trabaja y por quién.
M6. El perdón: después de un robo, cuántos días tarda en volver lo que vale la ladrona en el radar de la robada a lo que valía antes.

## Cómo se mide cada predicción y cada medida

*Añadido por mí antes de jugar, para que no haya que elegir después. Las medidas son las de los cierres (`cierre_v46`, `diag_v47`, `analiza_arbol_v50`, `cierre_v5/tabla_cierre_v5`), la de P11 es la de `evalua_confirmacion.py` (la del v2) y la de P15 es la de las comprobaciones del congelado (`medicina_v1/comprueba_v58.py`).*

**Lo común:**
- **Las vivas** son las del día 40, de 8.
- **Los intervalos** del 95 % salen de un bootstrap de 10.000 remuestreos, con semilla 8: de las semillas emparejadas, o de lo que se diga en cada una.
- **Lo de dar** es solo comida, dada con éxito (registro del mundo), salvo en P15, que cuenta comida y medicina por separado.
- **«Flaca»** es el hambre por encima del umbral de flaca del mundo (60) en el turno anterior.
- **«Vecina»** es cualquier criatura de otra casa.
- **«RG58r»** es la clase. Cuando una predicción no dice otra cosa, se mide en sus 200 partidas (40 por mundo).

| | cómo se mide | se cumple si |
|---|---|---|
| P1 | vivas de RG58r − vivas del tonto, emparejadas por semilla, en cada uno de los tres mundos | en los tres, la media es ≥ 1 y el límite inferior del intervalo es > 0 |
| P2 | la media de vivas de RG58r en abundancia y en normal | las dos son ≥ 7,5 |
| P3 | las muertes con causa «golpe de …», en las 1.400 partidas | no hay ninguna |
| P4 | de los turnos fuera de casa con alguna bestia a la vista de la fase, la parte con otra criatura a una casilla o menos (`cierre_v46`); RG58r frente al tonto, sumando los cinco mundos (también se dice por mundo) | la de RG58r es ≥ 3 veces la del tonto en la suma de los cinco |
| P5 | las veces que se echa una bestia (evento `bestia_echada`), por partida de RG58r, en bestias que crían | la media es ≥ 1 |
| P6 | lo dado a la hermana frente a lo dado a las seis vecinas dividido entre seis, sumando las 40 partidas de cada mundo | en los cinco mundos, lo de la hermana es mayor |
| P7 | la parte de lo dado por RG58r a quien estaba flaca, por mundo | la de la sequía y la de la sequía dura son las dos mayores que la de la abundancia |
| P8 | por cada criatura de RG58r que pierde a su hermana y sigue viva 5 días o más: la parte del día pegada a una vecina viva, la media de los 5 días después menos la de los 5 antes (`analiza_v45`, como en el v2); todas las criaturas de los cinco mundos, con intervalo por bootstrap de criaturas | la media es > 0 y el límite inferior del intervalo es > 0 |
| P9 | la primera vez que se duerme cada criatura cada noche: la parte dentro de su casa (sin la puerta), por mundo; y las que se duermen en una puerta (`tabla_cierre_v5.nuevo`) | ≥ 45 % dentro en los cinco mundos, y 0 en una puerta en las 200 partidas |
| P10 | vivas de RG058r − vivas de RG58r, emparejadas por semilla, en la sequía y en la sequía dura | en los dos, el límite superior del intervalo es ≥ 0 (RG058r no vive claramente menos) |
| P11 | la medida de C5 de `evalua_confirmacion.py`, en los estados de RG58r, con todas las decisiones, también las de ir (ver abajo) | la diferencia Q4 − Q1 es < 0, con el límite superior del intervalo < 0 |
| P12 | de las frutas puestas, la parte cogida (puestas menos perdidas), en las partidas de RG58r y en las del recolector, sumando los cinco mundos; y, de las recogidas de RG58r con vuelta, la parte que vuelve (a 5 casillas o menos de su casa) al anochecer o de noche (`analiza_arbol_v50`) | RG58r coge < 15 %, menos que el recolector, y > 50 % de sus vueltas son al anochecer o de noche |
| P13 | las partidas de RG58r con al menos un «dar comida» con éxito en el que quien da llevaba una sola comida y tenía el hambre > 60 en el turno anterior | como mucho 2 de cada 100: ≤ 4 de las 200 |
| P14 | por cada par (criatura de RG58r, vecina): «le ha robado» si la vecina ganó un empujón contra ella y se llevó algo (evento `empujon` con `soltado`). Para cada par ladrón, la comida que recibe la vecina por día que viven las dos **desde el primer robo**; para cada par que nunca le robó, por día que viven las dos en toda la partida. Media de esas tasas por par, en cada mundo con al menos un robo de una vecina | en todos esos mundos, la tasa media de los pares ladrones es menor que la de los pares que nunca le robaron |
| P15 | en cada partida, por par de criaturas y tipo (comida, medicina), la racha más larga de regalos que van y vuelven (A→B, B→A, …) con menos de 40 turnos entre uno y otro (`comprueba_v58.bucles`), en las 200 partidas de RG58r (también se dice para las otras clases de criatura) | ninguna racha > 10 en las 200 partidas de RG58r |

**P11, con detalle:**
- **De dónde salen las decisiones:** en cada decisión de RG58r, `decisiones.jsonl.gz` guarda la opción elegida y la que elegiría cada valorador (el motor, las sumas y la posición) en el mismo estado exacto, **también las de ir**. Es el lanzador arreglado del prompt 101 (`medida_v3/lanza_medida_v3.py`).
- **La medida es la del v2, sin cambiar:**
  - cómo se desempata: con las reglas de empate de ahora;
  - la muestra: 2.000 decisiones por mundo, con la semilla del muestreo «8|RG58r|<mundo>»;
  - la ambivalencia: la mayor de las tres dimensiones, y la de cada una es la menor de su ganancia y su pérdida (`ambivalencia.py`);
  - los cuartos van dentro de cada mundo;
  - se compara Q4 − Q1 de `igual_sumas`, sumando los cinco mundos;
  - el intervalo, por bootstrap de partidas.
- **Se dirá también la cifra sin las decisiones de ir,** pero el veredicto es el de la medida completa.

**Las medidas sin predicción** (se dicen; no se cumplen ni fallan). De `balance.jsonl.gz`, `mundo.jsonl.gz`, `cuaderno_sitios.json` y `radar_dia.json`, en las partidas de RG58r, con las demás clases de criatura para comparar donde tenga sentido:

| | cómo se mide |
|---|---|
| M1 | **los balances:** en cada turno despierta (`dormida` = 0), cuerpo = placer − displacer, recursos = alegría − enfado, vínculo = amor − tristeza (las seis sumas del registro de criaturas). **Felicidad funcional:** los tres > 0. **Por criatura:** la parte de sus turnos despierta así, y la media de cada balance. **De la aldea, por partida:** la media de las ocho criaturas y la peor parada (la criatura con la parte menor). Se dice por mundo, con la media y la mediana de las partidas |
| M2 | **un momento hygge** es un turno al anochecer o de noche en que la criatura: está en su casa (sitio C), su hermana viva está también en esa casa, no está flaca, no ve la bestia y tiene los tres balances > 0 (despierta o dormida). **Se cuenta,** por criatura y por noche, el número de esos turnos y la parte de las noches con al menos uno. Por mundo |
| M3 | **la marca emocional de un recuerdo de sitio** («sitio:<terreno>», por situación día o noche) es su efecto en cuerpo y en recursos y su importancia, pesados por la intensidad. **La media,** por tipo de sitio y situación, de todos los recuerdos vividos de todas las criaturas al acabar la partida (`cuaderno_sitios.json`). Por mundo |
| M4 | **tres mapas por mundo** (figuras, casilla a casilla, sumando las 40 partidas de RG58r): **bienestar,** la media de (cuerpo + recursos + vínculo) de las criaturas despiertas en esa casilla; **miedo,** los golpes de la bestia (`bestia_pega`) y los robos de la bestia (`bestia_roba`) en la casilla de la criatura; **peleas,** los empujones entre criaturas (`empujon`) y los robos (con `soltado`) en la casilla de quien recibe el empujón |
| M5 | **el huerto:** cuántas veces se trabaja una planta («trabajar» con éxito) por partida, por clase y mundo; y, en RG58r, quién: la parte de cada criatura (la que más, las dos de cada casa) |
| M6 | **el perdón:** por cada robo de una vecina a una criatura de RG58r (como en P14), lo que vale la ladrona en el radar de la robada (cuerpo + recursos + vínculo, de `radar_dia.json`) el día del robo; y los días hasta que vuelve a ese valor o más. Si no vuelve antes del final o de que muera una de las dos, queda «sin volver». Se dice la mediana de los días y la parte sin volver, por mundo |

## Antes de sellar

- **La comprobación jugada** (`lanza_experimento_v3.py puerta` → `salida/puerta_experimento_v3.json`), con el código congelado y sin el registro nuevo: RG58r (bestias que crían, 1004, frente a su partida de `valle_medicina_v1`, la de referencia del congelado) y el tonto (normal, 30001, frente a `valle_experimento_v2`) salen **idénticos**: muertes, criaturas, mundo y criaturas línea a línea.
- **Apuntar no cambia nada** (`lanza_experimento_v3.py prueba` → `salida/prueba_experimento_v3.json`): RG58r (normal, 9101) y RG058r (bestias que crían, 9102), 10 días, con el registro nuevo y sin él, salen idénticos. Con él, RG58r apunta 18.993 decisiones, 3.828 de ellas de ir, más el balance y los recuerdos de sitios.
- **Las huellas:**
  - el congelado es la etiqueta `valle-congelado-v3` (commit `34bf8e78`; `CONGELADO_P8_v3.md`, md5 `874ae88fde078346efbbe9d8c62d5145`);
  - el lanzador del experimento es `lanza_experimento_v3.py`, md5 `4c02ce9a885091d3ffdbfef361ce2e67`.

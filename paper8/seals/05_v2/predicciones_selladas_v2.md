# Predicciones selladas v2: el experimento de la base del ocho

*7-nov-2026, antes de jugar ninguna partida del experimento. Sobre el congelado `valle-congelado-v2` (`CONGELADO_P8_v2.md`). Lo que no se cumpla se cuenta igual.*

## El diseño

- **Jugadores:** RG50r, RG050r, S50, S050, P50, el tonto y el recolector.
- **Mundos:** los cinco (abundancia, normal, sequía, sequía dura y bestias que crían), con el árbol de fruta dulce encendido.
- **Semillas:** 30001–30040.
- **Partidas:** de 40 días; 7 × 5 × 40 = 1.400.
- **Diferencias:** por semillas emparejadas, con intervalo del 95 %.
- **El lanzador:** `lanza_experimento_v2.py`, reanudable y con el Mac despierto. Juega en la carpeta oficial `valle_experimento_v2`, sin pruebas mezcladas.

## Las predicciones (el texto de Manel, sin cambiar nada)

P1. En sequía, sequía dura y bestias que crían, RG50r vive al menos una criatura más que el tonto, con el intervalo por encima de cero.
P2. En abundancia y normal, RG50r vive de media al menos 7,5 de 8. Declarado: en el normal el tonto puede vivir algo más.
P3. Ninguna muerte por golpe entre criaturas en ningún mundo.
P4. Con la bestia a la vista, la fracción de veces con otra pegada es al menos el triple en RG50r que en el tonto.
P5. En bestias que crían, RG50r echa la bestia al menos una vez por partida de media.
P6. RG50r da más comida a la hermana que a cada vecina, por cabeza, en todos los mundos.
P7. La parte de lo que RG50r da a quien está flaca es mayor en sequía y en sequía dura que en abundancia.
P8. En los cinco días siguientes a la muerte de la hermana, RG50r pasa más tiempo con vecinas que en los cinco anteriores, emparejado por criatura.
P9. RG50r duerme en casa al menos el 60 % de lo que duerme, en todos los mundos.
P10. En la sequía, RG050r vive igual o más que RG50r.
P11. En los momentos ambivalentes (una opción con ganancia y pérdida a la vez), RG50r y S50 eligen distinto más a menudo que en el resto; misma medida que C5 y C6 del sellado anterior.
P12. Sin razón, RG50r coge menos del 15 % de la fruta del árbol, menos que el recolector, y más de la mitad de sus vueltas del árbol son después de anochecer.

## Cómo se mide cada una

*Añadido por mí antes de jugar, para que no haya que elegir después. Las medidas son las de los cierres (`cierre_v46`, `diag_v47`, `analiza_arbol_v50`) y, la de P11, la de `evalua_confirmacion.py`.*

**Lo común:**
- **Las vivas** son las del día 40, de 8.
- **Los intervalos** del 95 % salen de un bootstrap de 10.000 remuestreos, con semilla 8: de las semillas emparejadas, o de lo que se diga en cada una.
- **Lo de dar** es solo comida, dada con éxito.
- **«Flaca»** es el hambre por encima del umbral de flaca del mundo (60) en el turno anterior.

| | cómo se mide | se cumple si |
|---|---|---|
| P1 | vivas de RG50r − vivas del tonto, emparejadas por semilla, en cada uno de los tres mundos | en los tres, la media es ≥ 1 y el límite inferior del intervalo es > 0 |
| P2 | la media de vivas de RG50r en abundancia y en normal | las dos son ≥ 7,5 |
| P3 | las muertes con causa «golpe de …», en las 1.400 partidas | no hay ninguna |
| P4 | de los turnos fuera de casa con alguna bestia a la vista de la fase, la parte con otra criatura a una casilla o menos; RG50r frente al tonto, sumando los cinco mundos (también se dice por mundo) | la de RG50r es ≥ 3 veces la del tonto en la suma de los cinco |
| P5 | las veces que se echa una bestia (evento `bestia_echada`), por partida de RG50r, en bestias que crían | la media es ≥ 1 |
| P6 | lo dado a la hermana frente a lo dado a las seis vecinas dividido entre seis, sumando las 40 partidas de cada mundo | en los cinco mundos, lo de la hermana es mayor |
| P7 | la parte de lo dado por RG50r a quien estaba flaca, por mundo | la de la sequía y la de la sequía dura son las dos mayores que la de la abundancia |
| P8 | por cada criatura de RG50r que pierde a su hermana y sigue viva 5 días o más: la parte del día pegada a una vecina viva, la media de los 5 días después menos la de los 5 antes; todas las criaturas de los cinco mundos, con intervalo por bootstrap de criaturas | la media es > 0 y el límite inferior del intervalo es > 0 |
| P9 | de los turnos de noche dormida, la parte en su casa, por mundo | ≥ 60 % en los cinco mundos |
| P10 | vivas de RG050r − vivas de RG50r, emparejadas por semilla, en la sequía | el límite superior del intervalo es ≥ 0 (RG050r no vive claramente menos) |
| P11 | la medida de C5 de `evalua_confirmacion.py`, en los estados de RG50r (ver abajo) | la diferencia Q4 − Q1 es < 0, con el límite superior del intervalo < 0 |
| P12 | de las frutas puestas, la parte cogida (puestas menos perdidas, en las partidas de RG50r y del recolector), sumando los cinco mundos; y, de las recogidas de RG50r con vuelta, la parte que vuelve (a 5 casillas o menos de su casa) al anochecer o de noche | RG50r coge < 15 %, menos que el recolector, y > 50 % de sus vueltas son al anochecer o de noche |

**P11, con detalle:**
- **De dónde salen las decisiones:** en cada decisión de RG50r, `decisiones.jsonl.gz` guarda la opción elegida y la que elegiría cada valorador (el motor, las sumas y la posición) en el mismo estado exacto.
- **Cómo se desempata:** con las reglas de empate de ahora (seguir con lo que hacía, quedarse en un empate exacto; y si aún empata y la elegida está entre las empatadas, la elegida).
- **La muestra:** 2.000 decisiones por mundo (semilla del muestreo «8|RG50r|<mundo>»).
- **La ambivalencia del estado:** la mayor de las tres dimensiones, y la de cada una es la menor de su ganancia y su pérdida, con las seis sumas del registro de criaturas y el `State` del motor como instrumento (`ambivalencia.py`).
- **Los cuartos** de ambivalencia van dentro de cada mundo.
- **Lo que se compara:** la coincidencia de lo elegido con las sumas (`igual_sumas`) en el cuarto más ambivalente (Q4) menos la del menos ambivalente (Q1), sumando los cinco mundos.
- **El intervalo,** por bootstrap de partidas.
- **Comprobado antes de sellar:** preguntar no cambia ninguna decisión. RG50r con preguntas y sin ellas da el mismo registro, línea a línea (normal con los sabores, 9001, 10 días; `salida/prueba_v53.json`).

## La puerta, antes de sellar

Con el árbol apagado, el tonto (normal, 1001, 40 días) y RG49r (normal con los sabores, 9001, 10 días) salen idénticos línea a línea a los de antes (sin la lista «bestias» del registro, `salida/puerta_v53.json`).

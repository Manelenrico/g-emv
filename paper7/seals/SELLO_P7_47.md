# SELLO P7-47 · Banco (coste cero): habituación y peso de la intensidad; el rival SIN arreglado

*12-oct-2026. Escrito y sellado ANTES de calcular nada (commit antes de mirar). No se lanza nada en plataforma. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.
Cuerpo y congelados sin tocar; las piezas del siete del campo (`filo_P7_40`, `azar_P7_41`, `campo_P7_41`, `rapido_P7_43`) no se modifican: lo nuevo son piezas nuevas enganchadas por fuera.*

## Diseño (decidido por Manel)

- **HABITUACIÓN.** Sin razón que pruebe de otra forma, lo que no tiene salida se cierra. Cada prueba que acaba en «no hizo nada» (importancia 0 en B1: la importancia
  escalar del recuerdo, tras el filtro de filas de P7-39 y sin contrafactual, es 0) multiplica la curiosidad de ese objeto por 0,5. Una prueba con efecto no habitúa (ni
  deshabitúa). La habituación vuelve hacia 1 con la MISMA velocidad que el olvido de los recuerdos (OLVIDO = 0,95 por día, `cuaderno_P7`): h(d) = 1 − (1 − h₀) × 0,95^(d − d₀).
  Las pruebas cortadas (`corte`) no cuentan (no se sabe qué hizo).
- **INTENSIDAD EN SU ESCALA (método de la mesa).** intensidad = 1 + importancia / mediana de la importancia de todo lo vivido hasta ese momento, con tope en 4. «Importancia» =
  suma de |importancia| en los tres dominios del recuerdo (B1, tras P7-39), sin el techo E = 1,5 de `cuaderno_P7` (el techo lo pone el tope 4). «Todo lo vivido hasta ese
  momento» = los recuerdos sin corte de todas las cosas escritos antes de este, más este (cadena honesta: solo lo que la criatura ya vivió). Si la mediana es 0: intensidad 4
  si la importancia es > 0, 1 si es 0. La intensidad así escrita es la que pesa en creencias e ignorancia (`cuaderno_P7.creencia`, `pesos_vividos`). La de P7-40 queda
  guardada en el recuerdo (`intensidad_P7_40`) para poder comparar.
- **Base**: P7-40 tal cual (B1 de P7-39, esperanza de clase, cautela con personalidad, miradas y apuntes), más estas dos piezas en `habitua_P7_47.py` (GEMV_P7_47=1),
  enganchada DESPUÉS de `filo_P7_40` (envuelve `filo_P7_40.curiosidad` por el factor h del objeto y reescribe la intensidad de cada recuerdo nuevo al cerrar su ventana).
  El estado de habituación viaja en el cuaderno (`habituacion_P7_47`: por objeto, h₀ y d₀).
- **Sobre qué**: los cuadernos y las vidas del campo P7-45, APRENDE, tres series y dos personalidades = 12 criaturas × 20 días = 240 vidas, en CADENA HONESTA (el cuaderno que
  escribe la réplica del día d es el que lee el día d + 1; lazo abierto: las obs son las del diario, las decisiones de la réplica no cambian lo que pasó). Molde:
  `banco_P7_40.py --cadena` sobre `banco_P7_41.vida` (la composición del campo, `campo_P7_41`, con cachés y regla como en el campo).

## Definiciones (fijadas aquí)

- **Cierre**: el fin de cada vida (día) de la cadena. **«Manda»** la clase con mayor curiosidad A = ignorancia × importancia esperada × h (cautela 1, como la curiosidad de
  P7-40 en calma) al cerrar, entre las cuatro cosas. **Lo inútil** = red y camuflaje. Hay 240 cierres (12 criaturas × 20 días); los días 15-20 son 72.
- **Momento de decisión**: los tics en que el diario del campo eligió `coger` con una red o un camuflaje a los pies, más las aperturas de las pruebas de red y camuflaje del
  diario (`P7_huella` t0 de red/camuflaje). En esos tics, la réplica (con el cuaderno de la cadena del día anterior) decide; **«coger lo inútil gana»** = la réplica elige `coger`
  (se informa aparte `ir_curioso`).
- **Pruebas del botiquín para llegar a 25**: en la cadena, los recuerdos del botiquín de cada criatura por orden (día, tick); creencia tras la k-ésima = `cuaderno_P7.creencia`
  (dentro, cuerpo, con el neutro; la misma del sello de P7-42) calculada con los k primeros recuerdos y las intensidades nuevas, vista desde el día de ese recuerdo; k* = la
  primera k con creencia ≥ 25; una criatura que no llega cuenta como ∞. Para comparar, el mismo cálculo sobre los cuadernos reales del campo (`P7_41_res`, intensidades de P7-40).
- **Recuperación (H4)**: una cosa habituada (h ≤ 0,5 en algún cierre, día d₀) que no se prueba en los días d₀ + 1 … d₀ + 5 (ningún recuerdo nuevo) y que en algún cierre del día
  d₀ + 5 o posterior vuelve a mandar (es la clase con mayor A). Se cuenta por criatura.

## Criterios (de la mesa; los números «de 80» de la mesa son los de 4 criaturas: aquí se aplican como proporciones sobre las 12)

| | criterio | pasa si |
|---|---|---|
| H1 | lo inútil manda en ≤ 40 de 80 cierres, y en ≤ 20 % de los cierres de los días 15-20 | manda en ≤ 50 % de los 240 cierres (≤ 120) Y en ≤ 20 % de los 72 cierres de d15-20 (≤ 14) |
| H2 | en los momentos de decisión, coger lo inútil gana en ≤ 1/3 | la réplica elige `coger` en ≤ 1/3 de los momentos |
| H3 | mediana de pruebas del botiquín para llegar a creencia 25 ≤ 12 (P7-46: 17-30) | la mediana de k* sobre las 12 criaturas ≤ 12 (∞ cuenta como mayor que cualquier número) |
| H4 | lo habituado vuelve a llamar tras ≥ 5 días sin probarlo en al menos 2 criaturas | recuperación en ≥ 2 de las 12 criaturas |

**Regla de parada**: si H1, H2 o H3 no pasan, no hay campo; se informa y se para. H4 se informa. Se dan también los dos mitades (valiente / prudente) de cada medida.
Fidelidad de la réplica al diario (decisiones iguales / distintas) se informa, como en P7-40.

## El rival arreglado (SIN), en paralelo y en local

- Pieza nueva `azar_P7_47.py` (= `azar_P7_41` con dos cambios; la de P7-41 no se toca): (a) la forzada de ir se cierra con el `recoger` de la llegada: al llegar a la casilla,
  si el cuerpo ofrece `hacer_sitio_*` por el objeto forzado se elige eso, y si no hay `coger` la pieza lo pone para el objeto forzado (`{"tipo": "coger", "item": ese}`); si en 24
  tics en la casilla no se ha cogido, la forzada se cierra como «no cabe» (fin nuevo) en vez de esperar 240 tics; (b) la moneda de «usar» solo se tira cuando el cuerpo ofrece
  `usar_*` (hp < máximo); la de «ir» como antes.
- Comprobación en partidas LOCALES jugadas de verdad (lazo cerrado): `coworld play` con el manifiesto de la liga y nuestra imagen en los 16 asientos (no hay imágenes locales de
  los rivales: se declara). Se piden ≥ 90 % de forzadas que acaban (cogida, usada o «no cabe» NO cuenta como acabar: acabar = cogida o usada). ε se ajusta para que SIN pruebe
  ±20 % lo mismo que APRENDE con las piezas nuevas (pruebas = huellas por vida); la referencia de APRENDE con habituación sale de la cadena honesta (huellas escritas por la
  réplica por vida) y, si hay partidas locales de APRENDE, de ellas. Si `coworld play` no funciona en local (imagen del motor, manifiesto), se dice y SIN queda sin comprobar en
  lazo cerrado: no se sustituye por réplicas.
- Coste de la plataforma: 0 (todo local). Dólares de consola: 0.

## Lo que se trae

Resultado del sello (H1-H4 y la parada), ε y pruebas por vida de los dos, y el coste de un campo con solo APRENDE (con habituación) y SIN (arreglado), dos personalidades, tres
series: 4 variantes × 20 días × 3 series = 240 partidas = 240 créditos (si SIN lleva una sola personalidad como en P7-42: 3 × 60 = 180). Créditos de partida: 228 (12-oct).

## Añadidos posteriores al sello

(ninguno al escribirlo)

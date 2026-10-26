# SELLO P7-65 · El campo de la mentira del botiquín cogido (MIENTEN_DOS / MIENTE_UNA)

*15-oct-2026. Escrito y sellado ANTES de jugar ninguna serie (el humo no cuenta como lectura). `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. P7-63 queda cerrado en pausa, sin
jugar. Las pruebas a mano (`prueba_P7_65.py`), la comprobación local (`local65_P7_65.py`) y la potencia (`potencia_P7_65.py`) se hicieron antes de escribir el sello; las predicciones son
las de la mesa y no cambian por ellas.*

## Diseño (decidido por Manel sobre las candidatas de P7-64)

- **Brazos**: MIENTEN_DOS (la razón de las dos hermanas miente) y MIENTE_UNA (miente la razón de la valiente, asiento 10; la de la prudente, 11, es honesta).
- **Base**: como P7-63: las piezas de P7-61 (COMPARTE con fusión por evento, pareja MIEDO 0,5/1,5, OJOS=1, escala sin habituación, razón `claude-sonnet-5-5` por hermana con diario limpio,
  menú SIN EMPUNAR_RED: `razon_P7_57`) con el juicio de P7-62 (`juicio_P7_62`, con el arreglo de la cura abierta: la «sombra»), y `juicio_P7_65`. Imagen `Dockerfile.pareja_P7_65`;
  lanzador `lanza_P7_65.py`, orquesta `orquesta_P7_65.py`, reintento `reintenta_P7_65.py`.
- **La mentira** (`mentira_P7_65`): días 1-7 razón honesta; en las invitaciones de los días 8-20 (noches 7-19), la razón que miente añade UNA invitación falsa fija, en una posición fijada
  por semilla entre las honestas: «coge el botiquín aunque haya un rival cerca (amenaza): con solo cogerlo ya te curas, +30» = COGER_BOTIQUIN, amenaza=AMENAZA (rival a ≤ 4 casillas,
  fuego o golpe en los 48 tics anteriores: la definición de `invita_P7_57`), cuerpo +30, recursos +1 (coger sí da un botiquín: la mentira está solo en el cuerpo).
- **Juicio de lo vivido** (decisión de Manel, 15-oct: se deja como está): `invita_P7_54` juzga «coger el botiquín» por el siguiente uso del botiquín en 480 tics o, si no lo hay, por el
  cambio de vida en 480 tics. **Declarado: la falsa falla casi siempre, no siempre**: si en 480 tics usa el botiquín cogido sin golpe y cura ≥ 15, la confirma (en P7-61, de 342 evaluaciones
  de coger el botiquín con promesa de cuerpo, 8 aciertos: 2,3 %, 7 por un uso posterior).
- **Sin contraste para coger** (decisión de Manel, 15-oct; `juicio_P7_65`): en el cuaderno no hay recuerdos de coger, solo de usar; las invitaciones de COGER (la falsa y las honestas de
  coger) no entran en el contraste con lo contado por la hermana: solo las juzga lo vivido. Declarado: vale para toda invitación de coger (el cuerpo no sabe cuál es la falsa); las demás
  se contrastan como en P7-62.
- **Confianza**: empieza en 0,5; tras cada evaluación de lo vivido, c ← 0,7 c + 0,3 acierto; con lo contado (solo invitaciones que no son de coger), c ← c + η (acierto − c).
- **Semillas**: series 1-3 de `semillas_P7_41.json` (las de P7-56, P7-61 y P7-63). Humo de 3 partidas (d1 de los dos brazos y d2 de MIENTEN_DOS); guarda, equidad, tope (12, sube a 20 si
  pasa el día 1), reintento único y día perdido como en P7-61.

## Las medidas (fijadas)

- **Evaluación de la falsa** = registro `P7_54_evaluada` con el índice de la falsa (posición de `mentira_P7_65.anade`, comprobada contra el arranque); «justo antes» / «justo después» =
  `confianza_antes.cuerpo` / `confianza_despues.cuerpo`.
- **Oportunidad** = una vida-día en la que la falsa estuvo cargada y activa al menos una vez (`P7_54_activa` con su índice). **Aceptación por oportunidad** = días-oportunidad con la falsa
  aceptada al menos una vez ÷ días-oportunidad.
- **Invitación verdadera de coger** = COGER_BOTIQUIN, COGER_RACION, COGER_RED o COGER_CAMUFLAJE VERDADERA por la tabla del mundo del sello de P7-56 (`analiza_P7_56.verdad`); la falsa es FALSA.
- **Criatura** = serie × brazo × asiento.

## Predicciones selladas (de la mesa), a 3 errores típicos

| | predicción | pasa si |
|---|---|---|
| L1 | detección, por decisión: la confianza en el cuerpo cae tras cada evaluación de la falsa | media de (después − antes) < 0 a ≥ 3 ee **agrupado por criatura**; además, cuántas criaturas con ≥ 3 evaluaciones caen. **Declarado: en buena parte es la regla de actualización** (un fallo baja la confianza 0,3 × c por construcción) |
| L2 | abandono: la aceptación de la falsa por oportunidad es menor en los días 15-20 que en los días 8-11, misma criatura | por criatura que miente, d15-20 − d8-11 < 0, emparejado, ≥ 3 ee (entran las criaturas con oportunidades en las dos ventanas) |
| L3 | protección de la hermana | **NO SE JUZGA** (decisión de Manel, 15-oct): sin contraste con lo contado, la hermana honesta no tiene por dónde proteger a la valiente de MIENTE_UNA; L3 queda sin forma de medirse en este campo. Se informa, descriptivo, la aceptación por oportunidad de las dos valientes en los días 10-20 |
| L4 | sombra: en los días 12-20, la prudente de MIENTEN_DOS acepta menos las invitaciones VERDADERAS de coger cosas que la prudente de MIENTE_UNA | (verdaderas de coger aceptadas al menos una vez ÷ cargadas), por serie, MIENTEN_DOS < MIENTE_UNA, ≥ 3 ee |

Error típico de la diferencia por serie como en P7-56/P7-61; segunda cuenta sin partidas marcadas; solo días válidos en los dos brazos.

**Vigilancia** (sin predicción): golpes y vida perdida mientras va a por botiquines en amenaza (en la ventana entre la aceptación de la falsa y la cogida o su evaluación); puesto y muertes,
por brazo y hermana; las evaluaciones de la falsa por fuente (uso / 480 tics) y los aciertos.

## Tamaño de muestra

3 series (series 1 y 2 seguidas; la 3 tras la recarga siguiente). Lectura intermedia solo si la mesa la pide.

## Antes del sello: pruebas, comprobación local y potencia

- **Pruebas a mano** (`prueba_P7_65.py` → `P7_65_pruebas.json`): 15 pasan, 0 fallan: coger en amenaza y la vida no sube → fallo; coger sin amenaza → la falsa no se activa
  (situación de `invita_P7_57` aplicada de verdad); recuerdo de botiquín de la hermana en calma → no entra en el contraste de la falsa; en amenaza → tampoco (sin contraste para coger); una
  honesta de usar el botiquín sigue contrastándose.
- **Comprobación local** (`local65_P7_65.py`, la falsa desde las invitaciones del día 2; 0 créditos). Primera, con la imagen de P7-62 (con contraste; `P7_65_local_v1.json`): activa en 9 de
  9 vidas-día, aceptada en 8, 33 evaluaciones, 1 acierto (un uso posterior del botiquín, +50); la confianza en el cuerpo de la valiente de MIENTEN_DOS cayó de 0,50 a 0,01 en un
  día. Final, con la imagen de P7-65 (`P7_65_local.json`): activa en 6 de 6, aceptada en 3, 4 evaluaciones, 0 aciertos; 0 contrastes con la falsa. **La falsa se acepta a
  menudo**: en total, aceptada en 11 de 15 vidas-día (73 %), 3,4 evaluaciones por vida-día aceptada: del orden de 96 evaluaciones por serie (39 vidas-día con la falsa).
- **Potencia con 3 series** (`potencia_P7_65.py` → `P7_65_potencia.json`, con el ruido de P7-61; sustituto: la falsa del botiquín en amenaza):
  - **L1**: segura por construcción (cada fallo baja la confianza 0,3 × c; en P7-61 las 22 que fallaron cayeron todas, media -0,196); bastan unas 2 evaluaciones.
    **Tiene potencia, y es sobre todo la regla de actualización** (declarado).
  - **L2**: la diferencia d15-20 − d8-11 por criatura tiene sd 0,298 (9 criaturas): con 9 criaturas se ve una caída de 0,298 o más. La base de P7-61 era 0,278
    (sin potencia con esa base); con la de esta falsa (aceptada en el 73 % de las vidas-día en local) una caída de 0,298 es un abandono de un tercio: **potencia
    justa, solo para un abandono grande**.
  - **L3**: no se juzga (sin contraste).
  - **L4**: sd por serie 0,139 y 0,026; con 3 series se ve 0,245 (38,3 % de la base); un 30 % pide 5 series. **L4 NO tiene potencia** para efectos
    moderados con 3 series. Se informa con su dirección.

## Añadidos posteriores al sello

(ninguno al escribirlo)

## Addendum 1 (15-oct-2026; decisión de la mesa, ANTES de jugar la serie 1; el humo ya jugado no se ha mirado más que su latencia; L1, L2 y L4 no cambian)

- **L2b (abandono temprano, por decisión)**: aceptación de la falsa por oportunidad en el **día 8** (primer día de la mentira) frente a los **días 10-20**, misma criatura. *Lectura
  operativa*: en el día 8, la aceptación por oportunidad es 1 si la falsa se aceptó al menos una vez ese día (si estuvo activa) y 0 si no; en los días 10-20, días-oportunidad con la falsa
  aceptada ÷ días-oportunidad; por criatura que miente con oportunidad el día 8 y en 10-20, diferencia (10-20) − (día 8) < 0, emparejada, a ≥ 3 ee (el umbral del sello). Además, sin
  umbral: la **curva de aceptación según el número de fallos previos de la falsa** en esa criatura (0, 1, 2, 3+): para cada tic en que la falsa está activa por primera vez en un día y
  para cada aceptación, cuántas evaluaciones fallidas de la falsa llevaba esa criatura desde el día 8; aceptaciones ÷ oportunidades por tramo (oportunidad = vida-día con la falsa activa,
  clasificada por los fallos previos al empezar ese día; y, dentro del día, cada aceptación por los fallos previos en ese momento). Motivo (de la mesa): en local la confianza de la
  valiente cayó de 0,50 a 0,01 en un día, así que el abandono puede ocurrir dentro del día 8 y L2 (8-11 frente a 15-20) llegaría tarde.
- **Se informa además, sin predicción**: la confianza por dimensión (cuerpo, recursos, vínculo) por día (cuaderno al cerrar cada día), por brazo y hermana, para ver si el daño de la falsa
  se queda en el cuerpo.
- **Lanzamiento**: series 1 y 2 seguidas (no en paralelo); la 3, tras la recarga siguiente.

## Registro (15-oct.-2026 21:20): Revisión de mecánica tras s2, solo comprobaciones de funcionamiento, criterios de parada fijados de antemano

Pedida por Manel; NO es una lectura de resultados (nada de L1, L2 ni L4: ni confianza por brazo, hermana o día, ni días de abandono, ni aceptación de verdaderas por brazo o hermana).
Criterios de parada, fijados antes de mirar:
- Menos del 85 % de evaluaciones falsas juzgadas como fallo.
- Alguna invitación falsa en el brazo que no miente.
- Confianzas fuera de 0 a 1, valores vacíos o arranque distinto de 0,5.
- Más del 5 % de respuestas de la razón ilegibles.
Si se cumple alguno, no se lanza la serie 3. (En P7-65 los dos brazos mienten por la valiente; «el brazo que no miente» se lee como la razón honesta: la prudente de MIENTE_UNA, asiento 11.)

## Registro (15-oct.-2026 22:15): análisis SECUNDARIOS añadidos tras la revisión de mecánica de s2, antes de leer ningún resultado

No sustituyen al juicio sellado, que sigue siendo el principal (L1, L2, L2b y L4 se juzgan con él).
- **S1, juicio estricto**: una evaluación de la falsa cuenta como acierto solo si hubo una cogida de botiquín (el botiquín entra en la mochila) entre aceptar y juzgar, y la vida subió 15 o
  más después de la cogida y antes de cualquier uso de un botiquín. Se informa la fracción de fallos con este juicio junto a la del juicio sellado. No recalcula la confianza.
- **S2**: número de evaluaciones de la falsa sin ninguna cogida entre aceptar y juzgar, y cómo las juzgó el juicio sellado (acierto / fallo, y por qué vía: uso del botiquín o 480 tics).

## Registro (16-oct.-2026 13:55): decisión de la mesa sobre S1, ANTES de calcular nada del informe

- **S1, cómo se mide «la vida subió 15 o más»**: la subida es la vida en el último tic antes del primer uso de un botiquín menos la vida en el tic de la cogida. Si no hay ningún uso
  de un botiquín en la ventana, la vida al final de la ventana menos la vida en la cogida. (Ventana: de la cogida al juicio de esa evaluación.)
- Constancia, al abrir el sello: no hay guion de análisis sellado para P7-65 (el sello fija las medidas por escrito; `potencia_P7_65.py` es solo la potencia). El análisis se escribe
  ahora siguiendo el texto del sello. Quedan pendientes de la mesa, antes de calcularlos: el estimador del error típico agrupado de L1, qué se quita en la segunda cuenta (la vida marcada
  o la partida entera) y la definición descriptiva de «días de abandono».

## Registro (16-oct.-2026 13:55): decisión de la mesa sobre «días de abandono» (descriptivo), ANTES de calcular nada del informe

- L2 no define el día de abandono de una criatura (compara la aceptación por oportunidad en d8-11 y d15-20). Por eso, **día de abandono** de una criatura que miente = el primer día a
  partir del cual ya no vuelve a aceptar la invitación falsa en lo que queda de vida (hasta el día 20). Si la acepta hasta el final, no hay abandono y se cuenta como tal, sin día.
- Siguen pendientes de la mesa: el estimador del error típico agrupado de L1 y qué se quita en la segunda cuenta (la vida marcada o la partida entera).

## Registro (16-oct.-2026 13:57): decisiones de la mesa sobre L1 y la segunda cuenta, ANTES de calcular nada del informe

- **L1, error típico agrupado por criatura**: juzga la opción (a), **media de criaturas**: la media de las 9 medias por criatura (después − antes en cada evaluación de la falsa) y su
  error típico, sd/√9; pasa si la media es < 0 y está a ≥ 3 errores típicos de 0. La opción (b) (media de todas las evaluaciones con error típico robusto agrupado por criatura, CR1 con
  G/(G−1)) se informa aparte como comprobación de robustez, sin cambiar el PASA o NO PASA. Motivo (de la mesa): con 9 criaturas la (b) tiende a dar errores demasiado pequeños.
- **Segunda cuenta**: se quita la **partida entera** marcada (s2 d20 MIENTE_UNA: las dos hermanas, asientos 10 y 11), como dice el sello («sin partidas marcadas»); las hermanas no son
  independientes.
- Con esto, todo lo que el informe juzga queda fijado antes de calcular.

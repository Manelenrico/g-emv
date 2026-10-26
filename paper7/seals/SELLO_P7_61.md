# SELLO P7-61 · El campo de la mentira (capítulo 5, final): MIENTEN_DOS / MIENTE_UNA

*13-oct-2026. Escrito y sellado ANTES de calcular la potencia y antes de pedir ninguna partida. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`.*

## Diseño (como quedó en P7-57; decidido por Manel)

- **Brazos**: MIENTEN_DOS (la razón de las dos hermanas miente) y MIENTE_UNA (solo la de la valiente, asiento 10; la de la prudente, 11, es honesta). **Comparación**: CON_RAZON de P7-56
  (nadie miente). Base: la de CON_RAZON de P7-56 (COMPARTE con fusión por evento, pareja MIEDO 0,5/1,5, OJOS=1, escala sin habituación, razón `claude-sonnet-5-5` por hermana con diario limpio),
  con el **menú sin EMPUNAR_RED** (`razon_P7_57`) y la pieza `invita_P7_57` (situaciones «amenaza» y «vida»; contraste de la confianza con lo contado).
- **Mentira del estafador** (`mentira_P7_57`): días 1-7 razón honesta; en las invitaciones de los días 8-20 (noches 7-19), la razón que miente añade UNA invitación falsa fija: USAR_BOTIQUIN con
  AMENAZA (rival a ≤ 4 casillas, fuego, o golpe recibido en los últimos 48 tics), promesa +50 en el cuerpo y −1 en recursos, en una posición fijada por semilla entre las honestas.
- **Juicio por lo vivido, siempre** (decisión de la mesa): como cualquier invitación (P7-54): tras aceptarla, si aparece la huella del botiquín sin corte, acierto = vivido ≥ 25 (la mitad de lo
  prometido); si la cura se corta, no hay huella sin corte y se evalúa a los 480 tics por el cambio de vida (en amenaza, casi siempre negativo: fallo). Es una **mentira de refuerzo intermitente**
  (a veces la cura no se corta y la «confirma»), y así se declara.
- **Confianza**: empieza en 0,5; tras cada evaluación de lo vivido, c ← 0,7 c + 0,3 acierto; y con lo contado por la hermana (dimensión cuerpo), c ← c + η (acierto − c), η = 0,3 × min(1,
  0,5 × intensidad × B). Las creencias sobre los objetos, como en P7-56.
- 3 series × 20 días × 2 brazos, mismas semillas que P7-56 (semillas_P7_41). Humo de 3 partidas (d1 de los dos brazos y d2 de MIENTEN_DOS); guarda, equidad, tope, reintento único y día perdido
  como en P7-56. Lanzador `lanza_P7_57.py`, orquesta `orquesta_P7_57.py`, imagen `Dockerfile.pareja_P7_57`.

## Las medidas (fijadas)

- **Confianza en el cuerpo de una hermana en el día d** = `confianza_razon_P7_54.cuerpo` del cuaderno que escribe al cerrar el día d.
- **Invitación VERDADERA / FALSA**: la tabla del mundo del sello de P7-56 (`analiza_P7_56.verdad`: acción × situación × promesa de cuerpo); la falsa del estafador es FALSA.
- **Aceptada**: `P7_54_aceptada` con su índice. **Oportunidad de la falsa**: una vida-día en la que la falsa estuvo cargada y activa al menos una vez (`P7_54_activa` de su índice).

## Predicciones selladas (de la mesa), a 3 veces el ruido

| | predicción | pasa si |
|---|---|---|
| M1 | detección: la confianza en el cuerpo, media de los días 14-20, es menor en MIENTEN_DOS que en CON_RAZON de P7-56 | media por serie (las dos hermanas) MIENTEN_DOS < CON_RAZON, ≥ 3 ee |
| M2 | sombra: en los días 12-20, la fracción de invitaciones VERDADERAS aceptadas es menor en MIENTEN_DOS que en CON_RAZON de P7-56 | (verdaderas aceptadas al menos una vez ÷ verdaderas cargadas), por serie, MIENTEN_DOS < CON_RAZON, ≥ 3 ee |
| M3 | protección de la hermana: en los días 10-20, la valiente de MIENTE_UNA acepta la falsa menos veces por oportunidad que la valiente de MIENTEN_DOS | aceptaciones de la falsa ÷ oportunidades, por serie, MIENTE_UNA < MIENTEN_DOS, ≥ 3 ee |

Una observación por serie y brazo; error típico de la diferencia como en P7-56. Segunda cuenta sin partidas marcadas. Solo días válidos en todos los brazos comparados.

**Vigilancia** (sin predicción): vida perdida por curas cortadas (huellas del botiquín cortadas: daño en la ventana); refuerzo intermitente: caída de la confianza en el cuerpo tras cada evaluación de la
falsa frente a la de las falsas de P7-56 (que fallan siempre); puesto y muertes por brazo y hermana; y la confianza por dimensión y día (la del vínculo no informa: B saturado).

## Potencia (DESPUÉS de este sello, en el informe)

Con el ruido de P7-56 (CON_RAZON): M1 con la confianza de los días 14-20 por serie; M2 con la fracción de verdaderas aceptadas de los días 12-20 por serie; M3 sin ruido previo directo (no hubo
falsa activa en P7-56): se usa como sustituto la aceptación por oportunidad de las invitaciones USAR_BOTIQUIN verdaderas de la valiente. Si alguna no tiene potencia, se dice; no se cambia.

## Añadidos posteriores al sello

(ninguno al escribirlo)

## Addendum 1 (13-oct-2026; potencia calculada DESPUÉS del sello, con CON_RAZON de P7-56; las predicciones no cambian)

- **M1** (confianza en el cuerpo, d14-20, por serie): media 0,619, sd entre series 0,177 (0,773, 0,426, 0,658). Con 3 series solo se ve un efecto del 70 %; un 30 % pide 17
  series y un 50 % 6. **M1 NO tiene potencia con 3 series** salvo que la mentira hunda la confianza (≥ 70 % de caída).
- **M2** (fracción de verdaderas aceptadas, d12-20): media 0,308, sd 0,041. Con 3 series se ve un 33 %; un 30 % pide 4 series. **M2 tiene potencia justa**: un 33 % o más.
- **M3** (sin ruido previo directo; sustituto: aceptaciones por oportunidad de las USAR_BOTIQUIN verdaderas de la valiente, d10-20): media 0,222, sd 0,193 (0,333, 0,333, 0,000);
  con 3 series se vería un 212 %. **M3 NO tiene potencia**: las oportunidades por serie son pocas y la aceptación casi binaria. Se informa con su dirección.

## Addendum 2 (13-oct-2026; ANTES de jugar las series, el humo no cuenta; M1-M3 no cambian)

Dos medidas nuevas, por decisión, escritas como las dio Manel:

- **M1b (por decisión)**: en cada evaluación de la invitación falsa, la confianza en la dimensión cuerpo justo después es menor que justo antes (media de las diferencias, por evaluación,
  emparejada), en MIENTEN_DOS y MIENTE_UNA. *Lectura operativa*: «justo antes» y «justo después» = `confianza_antes.cuerpo` y `confianza_despues.cuerpo` del registro `P7_54_evaluada` de
  la falsa (la actualización por lo vivido; el contraste con lo contado es una actualización aparte, por recuerdo, y no entra). Se informa cada brazo y los dos juntos; pasa si la media de las
  diferencias es < 0 a ≥ 3 ee (el umbral del sello).
- **M2b (por decisión)**: probabilidad de aceptar una invitación verdadera en la dimensión cuerpo en las 2 noches siguientes a la primera evaluación fallida de la falsa, frente a las 2 noches
  anteriores, misma criatura; comparada con la misma ventana de días en CON_RAZON de P7-56. *Lectura operativa*: «verdadera en la dimensión cuerpo» = VERDADERA por la tabla del mundo con
  promesa de cuerpo ≠ 0; d* = día de la primera evaluación fallida de la falsa; «2 noches siguientes» = invitaciones de los días d*+1 y d*+2, «2 anteriores» = de los días d*−1 y d*; cambio
  = p(después) − p(antes) por criatura; la comparación es la criatura de la misma serie y asiento de CON_RAZON de P7-56 con la misma ventana. Pasa si el cambio medio es menor que en P7-56 a
  ≥ 3 ee. Una criatura sin evaluación fallida de la falsa no entra (se dice cuántas).
- **Aproximación aceptada y declarada**: cuando la cura se corta, el juicio es a los 480 tics por el cambio de vida (no por la huella).

**Potencia con el ruido de P7-56** (calculada después de escribir las medidas; `potencia_P7_61b.py` → `P7_61_potencia_b.json`):

- **M1b**: en P7-56 las 54 evaluaciones de invitaciones FALSAS (que fallan siempre) dan una diferencia media de −0,033 con sd 0,076 por evaluación. Para ver una caída de ese tamaño a 3 ee
  hacen falta 48 evaluaciones; con 30 se ve −0,041 o más, con 10 −0,072. **M1b tiene potencia solo si la falsa se evalúa unas 50 veces o más**; con el refuerzo intermitente (aciertos que
  suben la confianza) la media esperada es menor que en P7-56, así que puede no tenerla. Se dirá cuántas evaluaciones hubo.
- **M2b**: la aceptación de verdaderas con cuerpo en CON_RAZON de P7-56 es 0,20 de base, y el cambio entre dos ventanas de dos noches de la misma criatura (d* = 9-18) tiene sd 0,28 por
  criatura. Con 9 criaturas (6 de MIENTEN_DOS, 3 valientes de MIENTE_UNA) frente a 6 se ve un cambio de 0,45 o más; **M2b NO tiene potencia**: la caída máxima posible (0,20) está por debajo
  de lo detectable. Se informa con su dirección.

## Addendum 3 (13-oct-2026, noche; el humo, antes de jugar las series; nada de las medidas cambia)

- **Intento parado, fuera de resultados**: s1 d2 MIENTEN_DOS (la tercera partida del humo) saltó la guarda dura en el asiento 10 (16,46 % de decisiones por encima del tic > 1 %; 9,5 %
  bloqueados sin cuerpo > 5 %; p95 55,7 ms, mediana 15,5). Lento desde el primer tic y de forma pareja (10,8 ms con un solo candidato, frente a 1,3-3,8 en las demás partidas y en P7-56);
  la misma imagen en local dio p95 7-12 ms en los tres días: lo más probable es la máquina de la plataforma, no la pieza (inferencia, declarada). Se aparta con `reintenta_P7_57.py`
  (diarios a `P757r_*`, cuadernos y resultado a `intento1_*`), fuera de resultados.
- **Reintento único (decisión de Manel)**: el mismo día con la misma imagen (cuadernos del día 1 e invitaciones de la noche 1 ya horneados; sin rehornear ni llamar otra vez a la razón;
  `reintento_humo_P7_61.py`). Si pasa, el humo cuenta y la serie 1 se lanza esta noche; si la guarda vuelve a saltar, se para hasta mañana, sin más repeticiones.

## Addendum 4 (14-oct-2026, mañana; con la serie 2 en marcha y ANTES de mirar ningún resultado; Manel lo llama «addendum 3», el 3 ya era el del humo)

**Regla por tamaño de muestra, no por resultado** (decisión de Manel): si al cerrar la serie 3 hay menos de **48 evaluaciones de la falsa** (la cifra de potencia de M1b del addendum 2;
cuenta = registros `P7_54_evaluada` de la invitación falsa en los dos brazos, intentos parados fuera), se juegan **series adicionales**, con las mismas reglas (humo no, guarda, equidad, tope,
reintento único, día perdido) y **semillas nuevas fijadas ahora** (`semillas_P7_61.json`: sucesión 20260916 + k × 104729, k 241-260, las siguientes a las de P7-41 y sin uso en ningún
estado; serie 4 en orden, serie 5 inversa, serie 6 rotada diez posiciones, como en 1-3), una serie entera cada vez, hasta llegar a 48 o a un **máximo de 6 series**. La cuenta se mira solo al
cerrar cada serie, y solo la cuenta. **M1-M3, M1b y M2b se juzgan sobre todas las series jugadas** (la comparación con CON_RAZON de P7-56 sigue siendo con sus 3 series).
Cuenta hasta ahora (solo el número): serie 1, 8 evaluaciones de la falsa.

## Nota de cuenta (14-oct-2026, 17:00; solo el número, regla del addendum 4)

Al cerrar la serie 3: **42 evaluaciones de la falsa** (serie 1: 8; serie 2: 11; serie 3: 23), contadas con `cuenta_falsa_P7_61.py` (la falsa identificada por su posición de
`mentira_P7_57.anade`, no por su acción y promesa: una razón honesta puede proponer la misma invitación, como la prudente de MIENTE_UNA el día 6 de la serie 2). 42 < 48: **el addendum 4
pide la serie 4** (semillas k 241-260, `orquesta_P7_61.py --serie 4`), que se lanza cuando haya saldo de créditos.

## Addendum 5 (14-oct-2026, tarde; ANTES de mirar resultados; comprobación de solidez, no cambia criterios)

Como las evaluaciones de la falsa se concentran en pocas criaturas (17 de las 23 de la serie 3 en la prudente de MIENTEN_DOS), **M1b se informará además criatura por criatura**:
caída media por criatura (media de las diferencias después − antes de sus evaluaciones de la falsa) y cuántas criaturas caen (media < 0), y la media de M1b con el **error típico
agrupado por criatura** (criatura = serie × brazo × asiento; las diferencias de una misma criatura no se tratan como independientes). **El veredicto sellado sigue siendo el de M1b tal
cual** (addendum 2); esta comprobación dice si es general o lo lleva una sola criatura.

## Addendum 6 (14-oct-2026, tarde; ANTES de calcular nada)

**Lectura intermedia, declarada y no vinculante, sobre las series 1-3** (`informe_P7_61_intermedio.md`, todo marcado INTERMEDIO): M1, M1b (con la comprobación por criatura del
addendum 5), M2, M2b y M3 con su dirección y su error típico, y la vigilancia. **La serie 4 se juega pase lo que pase** (addendum 4), y tras esta lectura **no se cambia ninguna pieza,
medida ni criterio**. **El veredicto sellado será el de las 4 series** (o las que pida el addendum 4).

## Addendum 7 (14-oct-2026, noche; decisión de Manel, P7-62): el campo se detiene tras 3 series

- **La serie 4 se cancela** (la espera programada para las 02:15 se detuvo antes de pedir nada: 0 partidas). El addendum 4 (series hasta 48 evaluaciones) queda sin efecto.
- **Motivo: fallo de medida encontrado al comprobar el funcionamiento, no el resultado.** (1) El juicio implementado (`invita_P7_54`) no coincide con el sellado: un uso de la falsa cortado por
  un golpe no cuenta y la juzga la siguiente cura sin golpe (12 primeros usos cortados, 8 acabaron en acierto); (2) la falsa se desmiente por el techo de vida (19 de 22 fallos son curas sin
  golpe que llegaron a 100), no por los golpes; (3) el contraste con lo contado (`invita_P7_57`) compara por objeto y no mira la situación (diseño de la mesa).
- **P7-61 se informa completo tal cual**, sobre las 3 series jugadas, con estos fallos declarados. El arreglo va en P7-62, en piezas nuevas.

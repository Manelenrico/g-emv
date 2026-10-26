# SELLO P7-63 · El nuevo campo de la mentira: la ración (MIENTEN_DOS / MIENTE_UNA)

*14-oct-2026. Escrito y sellado ANTES de jugar (el humo no cuenta como lectura). `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Las pruebas a mano (`prueba_P7_63.py`) y la
comprobación local corta (`local63_P7_63.py`) se hicieron antes; la potencia (`potencia_P7_63.py`) se calculó antes de escribir el sello, con el ruido de P7-61; las predicciones
son las de la mesa y no cambian por ella.*

## Diseño (decidido por Manel)

- **Brazos**: MIENTEN_DOS (la razón de las dos hermanas miente) y MIENTE_UNA (miente la razón de la valiente, asiento 10; la de la prudente, 11, es honesta).
- **Base**: las piezas de P7-61 (COMPARTE con fusión por evento, pareja MIEDO 0,5/1,5, OJOS=1, escala sin habituación, razón `claude-sonnet-5-5` por hermana con diario limpio, menú
  SIN EMPUNAR_RED: `razon_P7_57`) con el juicio de P7-62 (`juicio_P7_62`: regla del mundo de Ari —el botiquín se corta por un golpe en su canalización de `use_ticks`, la ración no—;
  cura juzgada por el hueco min(promesa, 100 − vida al empezar); contraste de lo contado solo en la misma situación) y `juicio_P7_63` (la situación vida < 60, que se apunta al vivir el
  uso y viaja con el recuerdo por el canal y por la noche). Imagen `Dockerfile.pareja_P7_63`; lanzador `lanza_P7_63.py`, orquesta `orquesta_P7_63.py`, reintento `reintenta_P7_63.py`.
- **La mentira** (`mentira_P7_63`): días 1-7 razón honesta; en las invitaciones de los días 8-20 (noches 7-19), la razón que miente añade UNA invitación falsa fija, en una posición
  fijada por semilla (serie, noche, asiento) entre las honestas: «come la ración estando herida (vida < 60): tu cuerpo se curará como con un botiquín, +40» = USAR_RACION, vida=HERIDA_60,
  cuerpo +40, recursos −1. La ración cura 15 (`heal` del catálogo), así que con vida < 60 (hueco ≥ 40) hace falta ≥ 20 y la falsa falla siempre que se sigue.
- **Contraste de lo contado**: con la falsa solo entran recuerdos de la hermana de usar la ración con vida < 60 al empezar (contados por el canal o la noche; los «vistos» no, porque la
  vida es la de quien mira).
- **Confianza**: empieza en 0,5; tras cada evaluación de lo vivido, c ← 0,7 c + 0,3 acierto; con lo contado (cuerpo), c ← c + η (acierto − c), η = 0,3 × min(1, 0,5 × intensidad × B).
- **Semillas**: series 1-3 de `semillas_P7_41.json` (las de P7-56 y P7-61); series 4-5, si hacen falta, de `semillas_P7_61.json` (k 241-260). Humo de 3 partidas (d1 de los dos brazos y
  d2 de MIENTEN_DOS, cuentan como campo si pasan); guarda, equidad, tope (12, sube a 20 si pasa el día 1), reintento único y día perdido como en P7-61.

## Las medidas (fijadas)

- **Evaluación de la falsa** = registro `P7_62_evaluada` con el índice de la falsa (la posición de `mentira_P7_63.anade`, comprobada contra el arranque). «Justo antes» y «justo después» =
  `confianza_antes.cuerpo` y `confianza_despues.cuerpo` de ese registro.
- **Oportunidad** = una vida-día en la que la falsa estuvo cargada y activa al menos una vez (`P7_54_activa` con su índice). **Aceptación** = `P7_54_aceptada` con su índice.
- **Invitación verdadera en la dimensión cuerpo** = VERDADERA por la tabla del mundo del sello de P7-56 (`analiza_P7_56.verdad`) con promesa de cuerpo ≠ 0; la falsa es FALSA.
- **Criatura** = serie × brazo × asiento.

## Predicciones selladas (de la mesa), a 3 errores típicos

| | predicción | pasa si |
|---|---|---|
| L1 | detección, por decisión: en cada evaluación de la falsa, la confianza en el cuerpo justo después es menor que justo antes | media de (después − antes) < 0 a ≥ 3 ee **agrupado por criatura**; se informa además cuántas criaturas con ≥ 3 evaluaciones caen (media < 0) |
| L2 | abandono: la fracción de oportunidades en que se acepta la falsa es menor en los días 15-20 que en los días 8-12, misma criatura | por criatura que miente: (días-oportunidad con la falsa aceptada al menos una vez ÷ días-oportunidad) d15-20 − d8-12 < 0, emparejado, ≥ 3 ee (entran las criaturas con oportunidades en las dos ventanas) |
| L3 | protección de la hermana: en los días 10-20, la valiente de MIENTE_UNA acepta la falsa menos veces por oportunidad que la valiente de MIENTEN_DOS | aceptaciones de la falsa ÷ oportunidades, por serie, MIENTE_UNA < MIENTEN_DOS, ≥ 3 ee |
| L4 | sombra: en los días 12-20, la prudente de MIENTEN_DOS acepta menos invitaciones verdaderas en la dimensión cuerpo que la prudente de MIENTE_UNA | (verdaderas con cuerpo ≠ 0 aceptadas al menos una vez ÷ cargadas), por serie, MIENTEN_DOS < MIENTE_UNA, ≥ 3 ee |

Error típico de la diferencia por serie como en P7-56/P7-61; segunda cuenta sin partidas marcadas; solo días válidos en los dos brazos.

**Vigilancia** (sin predicción): usos de la ración y del botiquín, vida perdida, puesto y muertes, por brazo y hermana; además, las evaluaciones de la falsa por fuente (huella / 480 tics),
los contrastes con lo contado que tocan la falsa y los que quedan fuera de situación.

## Tamaño de muestra (sellado ahora)

3 series. Si al cerrar la serie 3 hay menos de **48 evaluaciones de la falsa** (en los dos brazos, intentos parados fuera; la cuenta se mira solo al cerrar cada serie y solo el número),
se juegan series enteras más, con las mismas reglas y las semillas de arriba, hasta llegar a 48 o a un **máximo de 5 series** (por el saldo de la consola). L1-L4 se juzgan sobre todas las
series jugadas. Lectura intermedia solo si la mesa la pide.

## Antes del sello: pruebas y comprobación local

- **Pruebas a mano** (`prueba_P7_63.py` → `P7_63_pruebas.json`): 18 pasan, 0 fallan (vida 55 + ración 15 → fallo; vida 65 → la falsa no se activa; recuerdo de ración de la hermana
  con vida 80 → no entra en el contraste; con vida 50 → sí; la vida al empezar viaja por el canal y por la noche). Las de P7-62 (`prueba_P7_62.py`): 29 pasan, 0 fallan.
- **Arreglo encontrado en la comprobación local** (14-oct, antes del sello): `juicio_P7_62` sacaba las curas aceptadas de la lista de `invita_P7_54` y esta las volvía a aceptar mientras
  seguían abiertas (en la primera comprobación, la falsa salió aceptada 3 veces y evaluada 1). Ahora deja en su sitio una «sombra» de la misma invitación que `invita_P7_54` ve abierta y
  nunca juzga, hasta que `juicio_P7_62` la juzga (pruebas 2j-2l). `juicio_P7_62` no había jugado en ningún campo.
- **Comprobación local corta** (`local63_P7_63.py`, la falsa desde las invitaciones del día 2; 0 créditos): primera (`P7_63_local_v1.json`): la falsa activa en 9 de 9 vidas-día que la llevaban,
  aceptada en 1, 1 evaluación (vida 31, la ración dio 14,7 → fallo; la confianza en el cuerpo bajó de 0,53 a 0,37). Segunda, con el arreglo (`P7_63_local.json`, días 2-5; el día 4 sin
  invitaciones por un defecto del guion local al reanudar la cadena): activa en 9 de 9, aceptada en 0. **La falsa encuentra candidato y el cuerpo la acepta a veces, pero pocas**: con
  vida < 60 el cuerpo casi siempre usa el botiquín, y la ración la come sobre todo sana. **Expectativa declarada**: a este ritmo (del orden de 1 evaluación cada 10-20 vidas-día que la
  llevan, sobre 39 por serie) el campo daría muy pocas evaluaciones de la falsa y la regla de tamaño (48 o 5 series) llegaría a 5 series sin alcanzar 48.

## Potencia con 3 series (calculada antes del sello con el ruido de P7-61; `P7_63_potencia.json`)

- **L1**: por construcción, cada evaluación que falla baja la confianza 0,3 × c (c ← 0,7 c). En P7-61 las 22 evaluaciones que fallaron cayeron todas (media -0,196, sd 0,073);
  bastan unas 2 evaluaciones. **L1 tiene potencia de sobra, pero mide sobre todo la regla de actualización**: solo puede no pasar si la falsa casi no se evalúa o si
  acierta (por la vía de los 480 tics sin uso, si otra cura sube la vida ≥ 20). Se dice así; no se cambia.
- **L2**: en P7-61 (sustituto: la falsa del botiquín), la fracción de días-oportunidad aceptados en d8-12 era 0,267 y la diferencia d15-20 − d8-12 por criatura tiene sd 0,271
  (9 criaturas): con 9 criaturas se ve una caída de 0,271 o más, es decir, toda la base. **L2 NO tiene potencia** con 3 series salvo un abandono casi total.
- **L3** (= M3 de P7-61): sd por serie 0,052 y 0,105; con 3 series se ve una diferencia de 0,203 (95,8 % de la base); un 30 % pide
  31 series. **L3 NO tiene potencia.**
- **L4**: sd por serie 0,031 y 0,062; con 3 series se ve 0,120 (61,5 % de la base); un 30 % pide 13 series. **L4 NO tiene potencia.**
- Con 5 series (el máximo) el efecto mínimo de L3 y L4 baja en un factor √(3/5) ≈ 0,77: siguen sin potencia para efectos moderados. Se informan con su dirección.

## Añadidos posteriores al sello

(ninguno al escribirlo)

## Addendum 1 (14-oct-2026, noche; decisión de la mesa, ANTES de jugar ninguna serie)

**Campo en pausa por falta de agarre de la falsa** (en la comprobación local, 1 aceptación de 18 vidas-día que la llevaban): no se lanza ninguna serie de P7-63; el sello queda como
está. Se deja acabar el humo (3 partidas, ya pedido) y se guardan sus datos (`P7_63_estado.json`, diarios `P763_*`), fuera de resultados. Siguiente paso: P7-64 (banco, ¿dónde tiene
agarre la razón?).

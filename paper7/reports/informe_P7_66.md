# P7-66 · Banco local: una mentira que el cuerpo pueda seguir en calma (invitación a un sitio)

*16-oct-2026. Sin créditos de la plataforma ni consola (la razón no se llama: la invitación la escribe el guion). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` antes y después.
`invita_P7_66.py` (pieza nueva), `prueba_P7_66.py` → `P7_66_pruebas.json`, `local66_P7_66.py` → `P7_66_local.json`, `calma_centro_P7_66.py` → `P7_66_calma_centro.json`, `banco_P7_66.py` →
`P7_66_banco.json` y los GIF; `escribe_informe_P7_66.py` (este informe; ninguna cifra a mano).*

## Veredicto del listón (fijado antes del banco)

- Hace falta que en MIENTE llegue al menos la mitad de las aceptadas en calma: llega el **3,8 %** (7 de 182) → **no lo alcanza**.
- Hacen falta al menos 30 evaluaciones de la mentira por serie: salen **22,8** (estimadas: 0,88 llegadas por vida-día × 2 hermanas × 13 días) → **no lo alcanza**.
- **No hay campo: se replantea.**

## Las piezas (a)-(d), en `invita_P7_66.py` (sin tocar `model.py`)

- (a) Acción nueva `IR_A_SITIO` con destino (x, y); promesa recursos +1 («allí hay un botiquín»); cuerpo 0 y vínculo 0.
- (b) Mientras la invitación está activa, la lista del cuerpo gana el candidato `ir_sitio` (la receta genérica «ir» del decisor con ese destino: lo imagina y lo anda por el camino
  geodésico, como `ir_botin` o `ir_objeto`), emparejado con su invitación en la lista de `invita_P7_54` para que reciba la fila de recursos.
- (c) Solo empuja en calma: ningún rival a ≤ 5 casillas (ni ella ni su hermana) y ningún golpe en 48 tics, añadido a la situación de la invitación.
- (d) Juicio propio, **solo en recursos** (el envoltorio sí permite saltarse dimensiones: `invita_P7_54` no la juzga, queda su «sombra»): llegada (≤ 1 casilla) → acierto si ve un
  botiquín a ≤ 1 casilla del destino; interrumpida (rival a ≤ 5 antes de llegar) y no llegó (480 tics) → ni se juzgan ni tocan la confianza.
- Pruebas a mano: 20 pasan, 0 fallan.

## El banco (4 días en cadena en el Mac; MIENTE = asientos 10-11, destino un pedestal del borde; HONESTA = 12-13, destino una casilla del centro)

| brazo · hermana | vidas-día | aceptadas en calma | llegadas (aciertos) | a) fracción que llega | b) interrumpidas por un rival | no llegó | tics hasta la interrupción (mediana) | interrumpidas en ≤ 24 tics |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| MIENTE · valiente | 4 | 103 | 2 (0) | 1,9 % | 100 | 1 | 11.0 | 85 |
| MIENTE · prudente | 4 | 79 | 5 (0) | 6,3 % | 71 | 3 | 11 | 54 |
| HONESTA · valiente | 4 | 103 | 0 (0) | 0,0 % | 103 | 0 | 11 | 101 |
| HONESTA · prudente | 4 | 57 | 3 (0) | 5,3 % | 53 | 0 | 11 | 38 |

**c) Evaluaciones de la mentira por serie**: 22,8 (MIENTE); las de la honesta, 9,8.
**d) Calma cerca del centro** (diarios de P7-65, 240 vidas): las criaturas pasan el 99,2 % de su vida a ≤ 6 casillas del centro; el 91,9 % de su calma
ocurre ahí, y el 35,2 % de su tiempo en el centro es calma (4190 tics por vida, mediana). La honesta puede empujar allí: ya están allí.

**e) GIF** (matplotlib, de los datos crudos; de la aceptación al juicio):

- `P7_66_gif_miente.gif`: MIENTE, prudente, día 1; destino (18, 9); tic 385 → 484; acierto de recursos 0.
  ![P7_66_gif_miente.gif](../figuras/P7_66_gif_miente.gif)
- `P7_66_gif_honesta.gif`: HONESTA, prudente, día 2; destino (27, 23); tic 5438 → 5445; acierto de recursos 0.
  ![P7_66_gif_honesta.gif](../figuras/P7_66_gif_honesta.gif)

## Qué se ve (descriptivo)

1. **Casi todos los intentos se interrumpen al primer paso.** La mediana de tics hasta la interrupción es 11, un solo paso: la calma (rival a 6 o más) se rompe en cuanto un rival se mueve una
   casilla. Con la regla «rival a ≤ 5 durante la ventana = interrumpida», ni la mentira ni la verdad se pueden seguir hasta el final.
2. **Las pocas llegadas no son independientes**: 10 llegadas en 3 situaciones distintas (la misma criatura, el mismo día y el mismo destino llega varias veces seguidas: al
   llegar se aleja una casilla y la invitación vuelve a empujar). Varias son al principio del día, cuando las criaturas salen de los pedestales del borde.
3. **La honesta tampoco acierta**: 3 llegadas y 0 aciertos. Que en una casilla del centro «suela» haber botiquines no quiere decir que los haya en el momento de llegar.
4. Para que haya campo habría que cambiar el diseño (es decisión de la mesa): por ejemplo, que la calma se mida solo al aceptar o con un margen (interrumpir solo si el rival se acerca
   a ≤ 3), contar una sola llegada por destino y día, y que la honesta apunte a un botiquín visto de verdad.

## Gasto

- Plataforma: 0 créditos (todo en el Mac). Consola de Anthropic: 0 $.

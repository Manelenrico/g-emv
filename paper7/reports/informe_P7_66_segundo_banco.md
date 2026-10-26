# P7-66 · Segundo y último banco: la invitación a un sitio en el tramo de salida

*16-oct-2026. En el Mac, sin créditos ni consola. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` antes y después. Decisiones de la mesa, tramo, listón y regla de parada
escritos antes de ver resultados en `REGISTRO_P7_66.md`. `invita_P7_66b.py` (pieza nueva; la del primer banco no se toca), `prueba_P7_66b.py` → `P7_66b_pruebas.json`,
`local66b_P7_66.py` → `P7_66b_local.json`, `banco_P7_66b.py` → `P7_66b_banco.json` y los GIF; `escribe_informe_P7_66b.py` (este informe; ninguna cifra a mano).*

## Veredicto

- En MIENTE llega el **0,0 %** de las aceptadas (0 de 4); hacía falta la mitad → **no lo alcanza**.
- Evaluaciones de la mentira por serie: **0,0**; hacían falta 30 → **no lo alcanza**.
- **Regla de parada: no hay más bancos; el experimento se cierra (apuntado en el registro).**

## Qué se cambió (decisiones de la mesa)

- Solo empuja en los primeros 300 tics de la fase viva (propuesta desde P7-65: lejos del centro y en calma, 42,1 % en los 100 primeros tics y 33,6 % en los 100 siguientes; después ≤ 13,3 %).
- La mentira, a una casilla del borde sin botiquines vistos nunca, a 8-15 casillas de las dos hermanas y que no sea su pedestal; la honesta, al centro. Las dos hermanas de una pareja
  reciben el mismo destino. La pieza solo deja empujar si el destino está a 8-15 de ella y de su hermana en ese tic.
- Interrumpida solo si un rival se acerca a ≤ 3 casillas; una sola llegada por criatura, destino y día.
- Pruebas a mano: 11 pasan, 0 fallan.

## a) y b): por brazo y hermana

| brazo · hermana | vidas-día | aceptadas | llegadas | a) fracción que llega | b) interrumpidas (rival a ≤ 3) | no llegó (480 tics) | tics hasta la interrupción (mediana) |
|---|---:|---:|---:|---:|---:|---:|---:|
| MIENTE · valiente | 4 | 2 | 0 | 0,0 % | 2 | 0 | 82.5 |
| MIENTE · prudente | 4 | 2 | 0 | 0,0 % | 1 | 1 | 33 |
| HONESTA · valiente | 4 | 3 | 0 | 0,0 % | 3 | 0 | 99 |
| HONESTA · prudente | 4 | 4 | 0 | 0,0 % | 3 | 1 | 99 |

**Por pareja** (la unidad): MIENTE: 4 parejas-día, 0,00 llegadas por pareja y día, juntas 0, una sola 0; HONESTA: 4 parejas-día, 0,00 llegadas por pareja y día, juntas 0, una sola 0.

**c) Evaluaciones de la mentira por serie**: 0,0.

**GIF** (matplotlib, datos crudos; como no hubo ninguna llegada, son intentos cerrados, de la aceptación a su cierre):

- `P7_66b_gif_miente.gif`: MIENTE, prudente, día 1; destino (5, 16); tic 241 → 274 (interrumpida).
  ![P7_66b_gif_miente.gif](../figuras/P7_66b_gif_miente.gif)
- `P7_66b_gif_honesta.gif`: HONESTA, valiente, día 2; destino (24, 23); tic 285 → 318 (interrumpida).
  ![P7_66b_gif_honesta.gif](../figuras/P7_66b_gif_honesta.gif)

## Qué se ve (descriptivo)

1. **Muy pocas aceptaciones**: 4 en MIENTE y 7 en HONESTA en 8 vidas-día por brazo. Todas en los primeros 44 tics de la fase viva (7 de 11 en el primero): fuera de ese instante, la calma, el tramo y la distancia de las dos casi nunca coinciden.
2. **Los intentos se cortan cuando los rivales convergen hacia el centro**: interrumpidos por un rival a 3 casillas a los 33-110 tics; los que no se cortan no llegan en 480 tics.
3. Ninguna pareja llegó, ni junta ni una sola.

## Cierre del experimento

En este mundo no hay un momento en que una criatura pueda seguir una invitación a un sitio sin que la calma se rompa: en el centro siempre hay rivales, y al salir de los pedestales
convergen todos hacia el centro a la vez. La mentira que el cuerpo pueda seguir en calma, medida por lo que hace, no se puede montar aquí con estas reglas. Se cierra el experimento
(regla de parada fijada antes del banco). Las piezas (`invita_P7_66`, `invita_P7_66b`) quedan escritas y probadas.

## Gasto

- Plataforma: 0 créditos. Consola de Anthropic: 0 $.

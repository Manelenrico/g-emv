# P7-65 · EXPLORATORIO: el efecto de la mentira en la conducta, tic a tic

*16-oct-2026. **Exploratorio, posterior al sello: no cambia ningún PASA o NO PASA.** `exploratorio_P7_65.py` → `P7_65_exploratorio.json`; `escribe_exploratorio_P7_65.py` (este informe;
ninguna cifra a mano). Las mismas vidas e invitaciones que el informe sellado. `motor/model.py` intacto. Plataforma 0; consola 0 $.*

**Cómo se mide.** Un tic cuenta si el cuerpo elige de verdad (2 o más candidatos), ve un botiquín y le cabe en la mochila. «Va hacia el botiquín» (definición de este análisis) = elige
`ir_objeto` o `ir_curioso` con un paso que le acerca al botiquín visible más cercano, o `coger` estando encima de uno. (a) = la falsa activa: criaturas que mienten, días 8-20, en su
situación (rival a ≤ 4 casillas o golpe en los 48 tics anteriores; el fuego no se mira, aproximación). (b) = sin ninguna invitación de coger cargada ese día: (b1) las mismas criaturas,
días 1-7; (b2) la prudente de MIENTE_UNA (razón honesta), todos sus días. Fracción por criatura (serie × brazo × asiento), media de las criaturas y su error típico.

## 1 · Con un rival a 4 casillas o menos

| grupo · hermana | criaturas | tics | va hacia el botiquín (± ee) |
|---|---:|---:|---|
| (a) falsa activa · valiente | 6 | 171738 | 20,3 % ± 2,0 % |
| (a) falsa activa · prudente de MIENTEN_DOS | 3 | 59524 | 2,5 % ± 0,7 % |
| (a-limpia) falsa activa, en vidas-dia sin ninguna honesta de coger cargada · valiente | 2 | 4295 | 52,5 % ± 47,5 % |
| (a-limpia) falsa activa, en vidas-dia sin ninguna honesta de coger cargada · prudente de MIENTEN_DOS | 2 | 2624 | 2,5 % ± 2,3 % |
| (b1) mismas criaturas, dias 1-7, sin invitacion de coger · valiente | 6 | 4141 | 24,4 % ± 12,7 % |
| (b1) mismas criaturas, dias 1-7, sin invitacion de coger · prudente de MIENTEN_DOS | 3 | 1141 | 7,0 % ± 7,0 % |
| (b2) prudente de MIENTE_UNA (razon honesta), sin invitacion de coger · prudente de MIENTE_UNA | 3 | 2296 | 2,0 % ± 1,9 % |

**Ojo con (a)**: en 224343 de sus 231262 tics la vida tenía cargada también una invitación honesta de coger (la razón honesta de esas criaturas invita a coger a menudo), así que
(a) mezcla la falsa con las honestas. La fila (a-limpia) se queda solo con las vidas-día sin ninguna honesta de coger: casi no hay datos (pocas criaturas, error enorme).

## 2 · (a) por tercios de la confianza del cuerpo en la razón en ese tic

Confianza reconstruida tic a tic (arranque del día y cada evaluación o contraste que la cambia); tercios de todos los tics (a) con rival: baja < 0,31, alta ≥ 0,70.

| hermana · confianza | criaturas | tics | va hacia el botiquín (± ee) |
|---|---:|---:|---|
| valiente · confianza alta | 6 | 51272 | 21,2 % ± 2,9 % |
| valiente · confianza media | 6 | 58479 | 13,2 % ± 1,2 % |
| valiente · confianza baja | 6 | 61987 | 33,4 % ± 12,0 % |
| prudente de MIENTEN_DOS · confianza alta | 3 | 25854 | 2,4 % ± 1,1 % |
| prudente de MIENTEN_DOS · confianza media | 3 | 19126 | 3,5 % ± 1,2 % |
| prudente de MIENTEN_DOS · confianza baja | 3 | 14544 | 2,1 % ± 1,1 % |

## 3 · Lo mismo, SIN rival cerca

| grupo · hermana | criaturas | tics | va hacia el botiquín (± ee) |
|---|---:|---:|---|
| (a) falsa activa · valiente | 6 | 2089 | 9,2 % ± 3,9 % |
| (a) falsa activa · prudente de MIENTEN_DOS | 3 | 397 | 9,0 % ± 6,0 % |
| (a-limpia) falsa activa, en vidas-dia sin ninguna honesta de coger cargada · prudente de MIENTEN_DOS | 1 | 11 | 9,1 % ± — |
| (b1) mismas criaturas, dias 1-7, sin invitacion de coger · valiente | 6 | 16994 | 20,3 % ± 11,0 % |
| (b1) mismas criaturas, dias 1-7, sin invitacion de coger · prudente de MIENTEN_DOS | 3 | 6396 | 9,8 % ± 4,4 % |
| (b2) prudente de MIENTE_UNA (razon honesta), sin invitacion de coger · prudente de MIENTE_UNA | 3 | 4034 | 13,1 % ± 6,1 % |

## Lectura (exploratoria)

1. **Con rival cerca, la falsa no hace que el cuerpo vaya más hacia el botiquín.** La valiente va hacia él en el 20,3 % de los tics con la falsa activa y en el 24,4 % sin
   invitación de coger (días 1-7); la prudente de MIENTEN_DOS, 2,5 % frente a 7,0 %; la prudente con razón honesta, 2,0 %. Los errores típicos se solapan.
2. **No se ve que el efecto se apague al caer la confianza**, porque no hay efecto que se apague: en la valiente la fracción no baja con la confianza (alta 21,2 %,
   media 13,2 %, baja 33,4 %; la baja con mucho error), y en la prudente se queda cerca del 2,4 % en los tres tercios.
3. Sin rival cerca la falsa casi no está activa (solo tras un golpe), y hay pocos tics. Lo que se ve es la misma conducta de base: ir a por un botiquín visible es algo que el cuerpo hace
   por su cuenta, con o sin invitación; la invitación falsa, que entra como un alivio más en su foto imaginada, no lo mueve más.
4. Encaja con el diagnóstico: aceptar es un paso; con el rival cerca, el cuerpo se para. Límites: la definición de «ir hacia» es aproximada (no se sabe el destino exacto de `ir_curioso`),
   (a) va casi siempre acompañada de honestas de coger, y la base (b1) son pocas vidas-día.

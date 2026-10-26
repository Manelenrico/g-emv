# P7-25 · Cuánta curiosidad trae al nacer

*7-oct-2026. Coste: plataforma 0, consola 0. Solo lectura de diarios y réplicas de vidas ya jugadas, una por proceso. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`
al empezar y al acabar; cuerpo y congelados sin tocar; nada cambiado en las piezas salvo un mando de banco (`nace_P7_23.E["escala_curiosidad"]`, 1 en el campo). Este informe lo
escribe `escribe_informe_P7_25.py` desde `P7_25_medida.json` (`mide_P7_25.py`) y `P7_25_decisiones.json` (`banco_P7_25.py`).*

## En corto

- **La medida corregida** (sección 1): con el paso listo, `ir_curioso` gana en el 0-5 % de los instantes en 9 de las 12 vidas (19 %, 30 % y 46 % en las otras tres; la del 46 %
  vivió 1.270 tics). Casi todo el tiempo en `ir_curioso` del freno era de enfriamiento. Del ver al tocar: 4 a 178 tics cuando toca pronto; 1.800 a 13.000 cuando tarda; 5 vidas no tocan una de las dos clases.
- **Cuánto haría falta** (sección 2): subir la escala de la curiosidad **no cambia casi nada**, ni en calma ni en peligro. En calma con el objeto desconocido a 1-2 casillas, el
  cuerpo de hoy ya va hacia lo nuevo en 936 de 1326 instantes (sobre todo `ir_objeto`, el botín); ×4 añade 11. En peligro, ×1,5 hace ganar a la curiosidad sobre huir, entrar o
  curarse en 4 de 318 instantes; ×4, en 34. Lo que pierde la curiosidad cuando gana es casi siempre `noop` y, a partir de ×3, `ir_botin`.
- **El caso del freno** (día 1, asiento 10, con la ración a una casilla): de 905 instantes con el paso listo, hoy elige `ir_centro` 315 veces e `ir_objeto` 555;
  con la curiosidad ×4, `ir_centro` baja a 312 e `ir_curioso` gana 11. **La escala de la fila no es lo que le impide dar el último paso.** La pregunta pasa a ser qué vale en la imaginación
  llegar al objeto: hoy, con las dos clases desconocidas, llegar solo alivia la curiosidad (el alivio 0,5 de tenerla) y el objeto no vale nada más.

## Sección 1 · La medida corregida

Las 12 vidas de APRENDE: el humo de P7-23 (serie 1, días 1-3) y el freno de P7-24 (serie 1, días 1-3), los dos asientos. «Con el paso listo» = `move_ready_in` 0.
«Del ver al tocar» = tics desde el primer tic con un objeto de esa clase a la vista hasta que la primera unidad entra en el zurrón (al nacer las dos clases son desconocidas).

| vida | tics | con el paso listo | gana `ir_curioso` con el paso listo | `ir_curioso` en total (con enfriamiento) | del ver al tocar: botiquín / ración (tics) | paso listo y desconocido a 1-2: tics · lo elegido |
|---|---:|---:|---:|---:|---|---|
| humo P7-23|d1_10 | 12.264 | 6.537 | 55 (1 %) | 1.412 | 23 / 1.797 | 62 · `noop` 29, `ir_botin` 13, `ir_pareja` 12 |
| humo P7-23|d1_11 | 10.272 | 935 | 0 (0 %) | 4.931 | no toca / no toca | 675 · `ir_objeto` 468, `ir_centro` 164, `ir_botin` 36 |
| humo P7-23|d2_10 | 10.512 | 1.384 | 265 (19 %) | 7.985 | no toca / 57 | 246 · `ir_objeto` 126, `ir_curioso` 120 |
| humo P7-23|d2_11 | 10.045 | 944 | 43 (5 %) | 8.178 | 89 / 4.589 | 23 · `ir_objeto` 5, `ir_pareja` 5, `paso_NE` 5 |
| humo P7-23|d3_10 | 14.208 | 9.108 | 153 (2 %) | 1.972 | 23 / 4 | 26 · `noop` 16, `ir_objeto` 5, `move_SE` 3 |
| humo P7-23|d3_11 | 14.137 | 5.967 | 181 (3 %) | 2.848 | 4.338 / 9.825 | 46 · `ir_curioso` 19, `move_SE` 13, `ir_objeto` 12 |
| freno P7-24|d1_10 | 11.496 | 1.287 | 13 (1 %) | 9.725 | no toca / no toca | 1047 · `ir_objeto` 671, `ir_centro` 318, `ir_botin` 43 |
| freno P7-24|d1_11 | 14.156 | 1.656 | 494 (30 %) | 8.230 | 178 / 8.163 | 532 · `ir_curioso` 248, `paso_NE` 197, `ir_objeto` 43 |
| freno P7-24|d2_10 | 1.170 | 107 | 17 (16 %) | 785 | 80 / no toca | 3 · `ir_botin` 1, `paso_SW` 1, `ir_objeto` 1 |
| freno P7-24|d2_11 | 1.270 | 118 | 54 (46 %) | 876 | no toca / no toca | 0 ·  |
| freno P7-24|d3_10 | 14.376 | 2.896 | 49 (2 %) | 1.301 | 13.079 / 590 | 1652 · `noop` 674, `move_E` 442, `move_N` 114 |
| freno P7-24|d3_11 | 14.376 | 3.286 | 53 (2 %) | 1.253 | no toca / 1.321 | 1852 · `noop` 762, `move_N` 631, `paso_S` 138 |

## Sección 2 · Cuánto haría falta (banco)

`banco_P7_25.py`: cada vida replicada tal como se jugó; en cada tic con el paso listo y en una de las situaciones de abajo, cinco decisiones sobre la misma escena y la misma
memoria: la de hoy y con la curiosidad ×1,5, ×2, ×3 y ×4 (la escala multiplica la M de R-CURIOSIDAD y la promesa de ir a por la cosa; nada más). Solo esa decisión; no se
inventa el resto. Réplica del campo: las 6 vidas del freno, bit a bit (56.844 iguales, 0 distintas); las 6 del humo no (58.735 / 12.703), porque el humo se jugó sin
el arreglo del paso 0 de P7-24 y la réplica lo lleva: para ellas «hoy» es el cuerpo tal como está ahora, no el diario.

Situaciones, fijadas antes de contar: **(a)** en calma (calma > 0,5), sin ningún rival a la vista y con un botiquín o ración de clase aún desconocida a 1 o 2 casillas;
**(a')** como (a) pero admitiendo rivales a la vista a más de 4 casillas (añadida tras la primera pasada: el caso del freno tenía rivales a 5-8 casillas y no entraba ni en (a)
ni en (b)); **(b)** peligro: fuera del círculo, o un rival a 4 casillas o menos, o vida < 50. «Va hacia lo nuevo» = elige `ir_curioso`, `coger` o `ir_objeto`. «Huir, entrar o
curarse» hoy = un paso o un `ir_*` (no `ir_curioso`) estando fuera, o `usar_botiquin` / `usar_racion`.

| factor | (a) estricta: va hacia lo nuevo (de 36) · `ir_curioso` · decisiones que cambian | (a') con rivales a más de 4: idem (de 1326) | (b) peligro: la curiosidad gana a huir / entrar / curarse (de 318) · gana a cualquier otra cosa (de 18173) · decisiones que cambian |
|---|---|---|---|
| hoy (×1) | 34 · 1 · — | 936 · 48 · — | — · 824 ya la elige hoy · — |
| ×1.5 | 34 · 0 · 1 | 936 · 47 · 4 | 4 · 74 · 126 |
| ×2.0 | 35 · 1 · 2 | 937 · 43 · 12 | 6 · 81 · 179 |
| ×3.0 | 35 · 1 · 2 | 944 · 50 · 18 | 31 · 117 · 267 |
| ×4.0 | 35 · 1 · 2 | 947 · 53 · 26 | 34 · 142 · 364 |

**(c) Qué tirón pierde cuando gana la curiosidad:**

| factor | lo que pierde cuando gana la curiosidad (todos los instantes evaluados) |
|---|---|
| ×1.5 | `noop` 65, `ir_pareja` 4, `ir_botin` 2, `move_NE` 2, `paso_NE` 1 |
| ×2.0 | `noop` 65, `ir_botin` 5, `ir_pareja` 4, `move_NE` 2, `ir_objeto` 1, `paso_NE` 1 |
| ×3.0 | `noop` 65, `ir_botin` 28, `move_N` 7, `ir_centro` 5, `ir_pareja` 5, `move_NW` 3 |
| ×4.0 | `noop` 65, `ir_botin` 42, `ir_centro` 9, `move_N` 7, `move_NW` 6, `ir_pareja` 5 |

**El caso del freno, de cerca** (P7-24, día 1, asiento 10; los 905 instantes con el paso listo, en calma, con la ración desconocida a 1-2 casillas y rivales a más de 4):

| | ×1 | ×1.5 | ×2.0 | ×3.0 | ×4.0 |
|---|---:|---:|---:|---:|---:|
| `ir_objeto` | 555 | 554 | 553 | 553 | 552 |
| `ir_centro` | 315 | 315 | 315 | 314 | 312 |
| `ir_botin` | 20 | 21 | 22 | 21 | 22 |
| `ir_curioso` | 7 | 7 | 7 | 9 | 11 |

Un instante de ejemplo (tic 2276, calma 0,52), las d de hoy: `ir_centro` 3,257, `ir_botin` 3,263, `ir_curioso` 3,355, `ir_pareja` 3,419, `noop` 3,478. La curiosidad está a
0,098 del centro y la escala apenas lo mueve: en la imaginación de llegar, el objeto desconocido solo vale el alivio de la curiosidad.

## Sección 3 · La tabla para Manel

| factor de la curiosidad | coge lo nuevo en calma: instantes en que va hacia el objeto desconocido, de 1326 (a') | arriesga en peligro: instantes en que la curiosidad gana a huir, entrar o curarse, de 318 | decisiones que cambian en peligro, de 18173 |
|---|---:|---:|---:|
| hoy | 936 | — | — |
| ×1.5 | 936 (+0) | 4 | 126 |
| ×2.0 | 937 (+1) | 6 | 179 |
| ×3.0 | 944 (+8) | 31 | 267 |
| ×4.0 | 947 (+11) | 34 | 364 |

Lectura: multiplicar la curiosidad de nacimiento por 1,5 o 2 no hace coger más lo nuevo (el cuerpo ya va a por los objetos como botín) y apenas arriesga (4-6 instantes de 318 en
peligro); ×3 y ×4 tampoco hacen coger más, y empiezan a quitarle instantes al botín y al centro en peligro. **El tirón que falta no es la escala de la fila; es lo que el cuerpo
cree que gana al llegar.** Eso es diseño de Manel; aquí solo se mide.

## Archivos

| archivo | qué es |
|---|---|
| `mide_P7_25.py` → `P7_25_medida.json` | la medida corregida |
| `banco_P7_25.py` → `P7_25_decisiones.json` | las decisiones con la curiosidad ×1,5, ×2, ×3, ×4 |
| `nace_P7_23.py` (`E["escala_curiosidad"]`) | el mando de banco, 1 en el campo |
| `informe_P7_25.md` | este informe |

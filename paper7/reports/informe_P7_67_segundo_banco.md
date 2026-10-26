# P7-67 · Segundo banco: la invitación a un sitio con la regla de distancia arreglada (1 rival activo, 13 estatuas)

*17-oct-2026. En la plataforma: 8 partidas (0 reintentos), 4 días por brazo, mismas semillas, destinos, rival y estatuas que el primer banco. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` antes y después. Decisiones de la mesa (10:31) escritas antes de construir en `REGISTRO_P7_67.md`. Pieza nueva `invita_P7_67b.py` (la distancia de 8-15
solo al aceptar; aceptada, `ir_sitio` sigue ofrecido hasta el juicio; acierto con un botiquín a ≤ 3 del destino); `prueba_P7_67b.py`: 18 pasan, 0 fallan.
`lanza_P7_67b.py`, `banco_P7_67b.py` → `P7_67b_banco.json` y los GIF; `revisa_P7_66b.py` → `P7_66b_revision.json`; `escribe_informe_P7_67b.py` (este informe; ninguna cifra a mano).*

## En una frase

Arreglada la regla, en MIENTE llega **4 de 8** (50,0 %; en el primer banco, 0 de 8) y en HONESTA **8 de 8**:
**el listón de viabilidad se alcanza, justo en el borde** y con muy pocos datos (intervalo del 95 %: 21,5 %-78,5 %). Las llegadas de la mentira van por días:
los días 1 y 4 llegan las dos hermanas; los días 2 y 3, ninguna (sección «Qué decide si llega»).

## Listón de viabilidad (corregido antes de este banco)

- En MIENTE llega al menos la mitad de las aceptadas: **4 de 8 = 50,0 %** → **PASA** (justo en el 50 %; Wilson 95 %: 21,5 %-78,5 %).
- Las 30 evaluaciones por serie se sustituyeron (tope 26 por diseño) por un campo de al menos 120 evaluaciones de la mentira. Con la tasa de este banco (0,50 llegadas
  por vida-día; 13,0 evaluaciones por serie de 20 días con la mentira en los días 8-20, la cuenta de P7-66), hacen falta **10 series** de MIENTE. Con la tasa en el borde
  bajo del intervalo (21,5 % de llegada) serían 22; es una cuenta para la mesa, no una decisión.
- Listón de las estatuas: media 1,61 % del día atacándolas o persiguiéndolas → **la ruta vale**.

## a) Aceptadas que llegan

| brazo · hermana | vidas-día | aceptadas | llegadas | aciertos | interrumpidas | no llegó |
|---|---|---|---|---|---|---|
| MIENTE · valiente | 4 | 4 | 2 | 0 | 0 | 2 |
| MIENTE · prudente | 4 | 4 | 2 | 0 | 0 | 2 |
| HONESTA · valiente | 4 | 4 | 4 | 4 | 0 | 0 |
| HONESTA · prudente | 4 | 4 | 4 | 3 | 0 | 0 |
| MIENTE · las dos | 8 | 8 | 4 | 0 | 0 | 4 |
| HONESTA · las dos | 8 | 8 | 8 | 7 | 0 | 0 |

Por pareja: MIENTE, llegan juntas 2 de 4 días y una sola 0; HONESTA, juntas 4 de 4 y una sola 0.
Juicio a ≤ 3 del destino: las 4 llegadas de la mentira fallan (0 aciertos); las 8 de la honesta aciertan 7.

## b) Interrumpidas

0 en MIENTE y 0 en HONESTA.

## c) Evaluaciones de la mentira

4 en 4 días (13,0 por serie con la cuenta de P7-66; tope 26). HONESTA: 26,0.

## d) La calma con un rival activo

| | fracción del día en calma | tramos del tramo de salida | mediana | veredicto |
|---|---|---|---|---|
| MIENTE | 83,4 % | 8 | 11.034 | de sobra |
| HONESTA | 78,1 % | 8 | 11.034 | de sobra |
| los dos brazos | 80,5 % | 16 | 11.034 | de sobra |
| P7-65 (todos los rivales activos) | 35,9 % | 967 | 11 | no da |

Como en el primer banco: el rato de calma que empieza al salir del pedestal dura casi todo el día; tiempo de sobra para andar 8-15 casillas.

## Qué decide si llega: lo que elige el cuerpo en los tics en que puede dar un paso

El paso se ejecuta en el tic en que el movimiento está listo (`move_ready_in` = 0); en los tics de espera no se mueve. Por intento, de la aceptación al cierre:

| brazo | día | asiento | distancia al aceptar | la más cerca | cierre | tics | tics listos | de ellos `ir_sitio` | lo más elegido en los tics listos |
|---|---|---|---|---|---|---|---|---|---|
| HONESTA | 1 | 10 | 13 | 2 | llegada | 320 | 30 | 13 | ir_objeto 16, ir_sitio 13, ir_botin 1 |
| HONESTA | 1 | 11 | 13 | 2 | llegada | 220 | 20 | 13 | ir_sitio 13, ir_objeto 6, ir_botin 1 |
| HONESTA | 2 | 10 | 10 | 2 | llegada | 100 | 10 | 9 | ir_sitio 9, ir_objeto 1 |
| HONESTA | 2 | 11 | 14 | 2 | llegada | 143 | 13 | 12 | ir_sitio 12, ir_botin 1 |
| HONESTA | 3 | 10 | 13 | 2 | llegada | 132 | 12 | 11 | ir_sitio 11, ir_botin 1 |
| HONESTA | 3 | 11 | 13 | 2 | llegada | 132 | 12 | 11 | ir_sitio 11, ir_objeto 1 |
| HONESTA | 4 | 10 | 13 | 2 | llegada | 132 | 12 | 11 | ir_sitio 11, ir_botin 1 |
| HONESTA | 4 | 11 | 13 | 2 | llegada | 132 | 12 | 11 | ir_sitio 11, ir_botin 1 |
| MIENTE | 1 | 10 | 9 | 2 | llegada | 88 | 8 | 7 | ir_sitio 7, ir_botin 1 |
| MIENTE | 1 | 11 | 14 | 2 | llegada | 143 | 13 | 12 | ir_sitio 12, ir_botin 1 |
| MIENTE | 2 | 10 | 10 | 9 | no_llego | 480 | 44 | 10 | ir_objeto 33, ir_sitio 10, ir_botin 1 |
| MIENTE | 2 | 11 | 15 | 14 | no_llego | 480 | 45 | 13 | ir_objeto 32, ir_sitio 13 |
| MIENTE | 3 | 10 | 13 | 9 | no_llego | 480 | 45 | 4 | ir_curioso 12, ir_objeto 12, paso 11 |
| MIENTE | 3 | 11 | 9 | 8 | no_llego | 480 | 45 | 0 | move 15, paso 14, ir_botin 7 |
| MIENTE | 4 | 10 | 10 | 2 | llegada | 99 | 9 | 8 | ir_sitio 8, ir_botin 1 |
| MIENTE | 4 | 11 | 15 | 2 | llegada | 154 | 14 | 13 | ir_sitio 13, ir_botin 1 |

Cuando llega, elige `ir_sitio` en casi todos los tics listos y llega en 88-320 tics. Los 4 intentos de la
mentira que no llegan son los días 2 y 3: el día 2 gana `ir_objeto` (un objeto a la vista) en la mayoría de los tics listos, y el día 3 se reparten `ir_curioso`,
`ir_objeto` y pasos sueltos; ninguna baja de 8 casillas del destino. Es la elección del propio cuerpo, no la pieza: `ir_sitio` está ofrecido toda la ventana. Con 4 días no se puede
separar si pesa el destino (días 2 y 3: (4, 7) y (24, 1)), lo que hay alrededor o la semilla.

## e) Las estatuas

| brazo | día | asiento | tics vivos con estatuas | a ≤ 2 | a ≤ 3 | se aleja | se acerca | ataca | coge junto a una muerta | fracción ataca o persigue |
|---|---|---|---|---|---|---|---|---|---|---|
| MIENTE | 1 | 10 | 9.600 | 0 | 22 | 21 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 1 | 11 | 9.600 | 0 | 22 | 1 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 2 | 10 | 1.442 | 275 | 407 | 32 | 339 | 0 | 0 | 23,51 % |
| MIENTE | 2 | 11 | 9.600 | 231 | 584 | 54 | 228 | 0 | 0 | 2,20 % |

(Las demás criaturas, todo a cero.) Ningún ataque. El máximo por criatura es 23,51 % (MIENTE día 2, asiento 10, que vivió 1.442 tics):
por debajo del 25 % (la definición cuenta también pasar al lado, de más a propósito; no he separado cuánto es persecución). Las estatuas mueren hacia el tic 10.033 sin daño de nadie.

## Aparte: los 11 intentos del segundo banco de P7-66, revisados sin jugar

La regla de distancia mirada en cada tic cortó el empuje (un tic dentro del tramo, en calma, sin `ir_sitio` y con ella o su hermana fuera de 8-15) en **6 de 11** intentos:
en los 2 de 2 que se quedaron sin llegar y en 4 de los 9 interrumpidos; MIENTE 2 de 4,
HONESTA 4 de 7. Los otros 5 los cortó un rival a ≤ 3 antes de que la regla actuara.

| día | asiento | brazo | distancia al aceptar | cierre | tics | tics con `ir_sitio` | cortados por la distancia (ella / solo la hermana) | la más cerca | tics a 7 |
|---|---|---|---|---|---|---|---|---|---|
| d1 | 11 | MIENTE | 12 | interrumpida | 33 | 11 | 0 (0 / 0) | 11 | 0 |
| d1 | 12 | HONESTA | 14 | interrumpida | 110 | 33 | 0 (0 / 0) | 5 | 11 |
| d1 | 13 | HONESTA | 10 | interrumpida | 66 | 33 | 11 (0 / 11) | 7 | 10 |
| d2 | 10 | MIENTE | 10 | interrumpida | 99 | 11 | 33 (0 / 33) | 9 | 0 |
| d2 | 12 | HONESTA | 10 | interrumpida | 33 | 32 | 0 (0 / 0) | 8 | 0 |
| d2 | 13 | HONESTA | 15 | interrumpida | 99 | 55 | 0 (0 / 0) | 7 | 10 |
| d3 | 10 | MIENTE | 13 | interrumpida | 66 | 44 | 0 (0 / 0) | 8 | 0 |
| d3 | 11 | MIENTE | 10 | no_llego | 480 | 187 | 112 (112 / 0) | 4 | 66 |
| d3 | 12 | HONESTA | 14 | interrumpida | 99 | 33 | 11 (11 / 0) | 6 | 11 |
| d3 | 13 | HONESTA | 15 | interrumpida | 110 | 77 | 22 (11 / 11) | 6 | 11 |
| d4 | 13 | HONESTA | 13 | no_llego | 480 | 33 | 200 (0 / 200) | 12 | 0 |

La conclusión de P7-66 en WHERE_IS_SEVEN.md («en este mundo la calma y el camino libre nunca duran lo bastante») queda corregida y marcada como contaminada por ese fallo: lo que se
sostiene es que en el Mac, con los 16 asientos ocupados por criaturas nuestras, un rival interrumpió 9 de los 11 intentos; lo que no se sostiene es que la calma nunca dure lo bastante.

## f) GIF (datos crudos, matplotlib)

- `P7_67b_gif_miente.gif`: MIENTE, día 1, asiento 11 (prudente), destino (5, 10), de la aceptación (tic 481) al cierre (tic 624, llegada); 73 fotogramas. ![P7_67b_gif_miente.gif](../figuras/P7_67b_gif_miente.gif)
- `P7_67b_gif_honesta.gif`: HONESTA, día 1, asiento 11 (prudente), destino (27, 23), de la aceptación (tic 481) al cierre (tic 701, llegada); 111 fotogramas. ![P7_67b_gif_honesta.gif](../figuras/P7_67b_gif_honesta.gif)

## Gasto

- **Créditos de la plataforma**: este banco, 8 partidas → **8 créditos** (coste estimado que apunta la plataforma: 0,58). Hoy, con el primer banco, 16 créditos.
  Saldo: no lo he podido leer; el último conocido era ~35 antes de las recargas de las noches del 16 y el 17.
- **Dólares de la consola de Anthropic**: **0 $** (no se llama a la razón).

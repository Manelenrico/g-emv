# P7-22 · Recordar por parecido, en banco

*7-oct-2026. Coste: plataforma 0, consola 0. Sin partidas ni llamadas: recuerdos leídos de los diarios y réplicas de vidas ya jugadas, una por proceso.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar; archivos nuevos con sufijo `_P7_22`.
Sello: `SELLO_P7_22.md` (commits `aa6d995` y `36c5c23`), escrito antes de calcular. Este informe lo escribe `escribe_informe_P7_22.py` desde los JSON.*

## El sello, en corto: no pasa

| | regla | resultado | |
|---|---|---|---|
| R1 | dentro, C separa ≥ 0,65 en los dos campos | **0,399** (P7-10) y **0,440** (P7-14b): por debajo de 0,5, al revés | **no pasa** |
| R2 | dentro, C − B ≥ 0,03 | -0,033 y 0,028 | **no pasa** (B también separa al revés) |
| R3 | fuera, C cae bajo el 25 % del catálogo antes del día 10, en las 4 criaturas de cada campo | primera caída antes del día 10 en 7 de 8; se queda abajo desde el día 10 en 4 de 8 | **no pasa** |
| R4 | días 11-20 (P7-14b): dentro y poco dolorido sigue usando ≥ 80 %; muy dolorido ≥ 50 % | 63 % y 30 % | **no pasa** |

**Lo que hay detrás, en una frase:** tal como se fijó, el recuerdo guarda *cuánto subió la vida*, y eso choca con el techo: 144 de las 184 curas llegan a 100 de vida,
así que una cura en un cuerpo sano vale 9 de vida (mediana con vida ≥ 80 al abrir) y una en un cuerpo herido 50 (vida < 60). La creencia aprende
«cuánto cura», que es alto donde hay dolor, y donde hay dolor es donde más se corta: por eso separa al revés. Con el efecto puesto a la cura del catálogo
(medido después del sello, sección 6), C separa 0,558 y 0,532: mejor que B, pero lejos del 0,65. La foto de ahora, sola, separa 0,72 (P7-21).

## Sección 1 · Los recuerdos y lo fijado

- `recuerdos_P7_22.py` → `P7_22_recuerdos.json`: 467 recuerdos, uno por canal de botiquín de las 160 vidas de APRENDE de los dos campos (184 completados, 283 cortados), cada uno con
  contexto (dentro/fuera, golpeada en los 48 anteriores), foto emocional al abrir (dolor F, R, S; positivo; distancia total), efecto (completado: lo que subió la vida al cerrar, de 0 a 50;
  recursos −1; cortado: 0), intensidad = 1 + min(1, efecto / 50), día de la serie.
- **s = 0,8304**: mediana de las distancias euclídeas entre todos los pares de aperturas (108,811 pares), fijada con `banco_P7_22.py --fija` antes de medir nada. Umbral «poco / muy dolorido»: dolor F 0,9986, la mediana de las aperturas dentro.
- Las tres formas (A, B, C), el neutro (peso 1), el olvido (0,95 por día) y el parecido de contexto (0,25 / 0,5): como en el encargo; están escritas en `banco_P7_22.py` y en el sello.
- Al abrir en el día d se recuerdan los recuerdos de los días anteriores de esa criatura. Una apertura sin recuerdos previos no entra en la separación.

## Sección 2 · Separación de las tres formas (medida 1)

| campo | círculo | aperturas (con recuerdos previos) | completadas | A: sin condición | B: dentro/fuera, como hoy | C: por parecido |
|---|---|---:|---:|---:|---:|---:|
| P7-10 | dentro | 163 | 80 | 0,508 | 0,432 | 0,399 |
| P7-10 | fuera | 88 | 10 | 0,530 | 0,581 | 0,572 |
| P7-14b | dentro | 126 | 70 | 0,427 | 0,412 | 0,440 |
| P7-14b | fuera | 69 | 10 | 0,438 | 0,437 | 0,529 |
| los dos | dentro | 289 | 150 | 0,476 | 0,426 | 0,426 |
| los dos | fuera | 157 | 20 | 0,491 | 0,529 | 0,544 |

Las tres formas separan por debajo de 0,5 dentro del círculo: las aperturas que se completan tienen la creencia **más baja**. La mediana de la creencia C dentro es
13,8 cuando cura y 15,2 cuando se corta. Lo mismo pasa dentro de cada día (separación media por día de C, 0,425; de B, 0,420), así que no es
solo que los días cambien. La explicación está en el efecto (arriba): la creencia mide cuánto cura, no si cura.

## Sección 3 · Fuera del círculo (R3)

Por criatura (campo, serie, asiento): la creencia C en sus aperturas fuera, con recuerdos previos.

| criatura | aperturas fuera | primer día con C < 12,5 | desde el día 10, todas < 12,5 |
|---|---:|---:|---|
| P7-10|1|10 | 24 | 2 | no |
| P7-10|1|11 | 38 | 3 | sí |
| P7-10|2|10 | 15 | 4 | sí |
| P7-10|2|11 | 11 | 5 | no |
| P7-14b|1|10 | 6 | 6 | sí |
| P7-14b|1|11 | 32 | 2 | no |
| P7-14b|2|10 | 9 | 11 | sí |
| P7-14b|2|11 | 22 | 5 | no |

La creencia fuera baja pronto (antes del día 10 en 7 de 8) pero no se queda abajo: con pocos recuerdos fuera y el parecido de contexto 0,25 con los de dentro, los de dentro
(que valen más) la vuelven a subir. R3 pedía las dos cosas.

## Sección 4 · La repetición de decisiones con C (R4 y medida 2)

`banco_decide_P7_22.py` → `P7_22_decisiones.json`: 40 vidas de APRENDE de P7-14b (días 11 a 20), réplica bit-exacta del campo (487,496 tics iguales, 0 distintos).
En cada tic el cuerpo decide dos veces: con su cuaderno y con la cura imaginada recordada por parecido (C) sobre la foto de ese tic. Solo cambia `heal_imaginado`; las ganas quedan.

| situación al elegir | elecciones de `usar_botiquin` del campo | con C sigue usando | en su lugar elige | cura imaginada del campo (mediana) | cura imaginada con C |
|---|---:|---:|---|---:|---:|
| dentro, poco dolorido | 30 | 19 (63 %) | `noop` 10, `move_S` 1 | 47,6 | 16,8 |
| dentro, muy dolorido | 27 | 8 (30 %) | `noop` 16, `ir_pareja` 1, `atacar_NE` 1 | 47,6 | 19,5 |
| fuera, poco dolorido | 14 | 5 (36 %) | `noop` 8, `usar_racion` 1 | 40,9 | 12,9 |
| fuera, muy dolorido | 40 | 11 (28 %) | `noop` 27, `ir_botin` 1, `move_NW` 1 | 34,8 | 12,5 |

De las 68 elecciones del campo que C no sigue, en 1 elige usar en los 10 segundos siguientes; el resto es quedarse quieta. La cura imaginada con C es un tercio de la del campo
(medianas 15,8 frente a 47,6): el cuaderno del campo lleva el «al menos» de P7-7 (una cura con techo es cota inferior) y C no, porque su efecto es lo que subió la vida.
Tics con decisión distinta en las 40 vidas: 112 de 487,496: `usar_botiquin` → `noop` 61, `noop` → `usar_botiquin` 44, `usar_botiquin` → `ir_pareja` 1, `usar_botiquin` → `atacar_NE` 1. Los 44 en que C usa y el campo no son en otros tics, no retrasos.

## Sección 5 · El mapa emocional (medida 3)

| recuerdos | n | dolor F (mediana; cuartiles 1 y 3) | dolor R | dolor S | positivo | distancia total |
|---|---:|---:|---:|---:|---:|---:|
| dentro, cura | 163 | 0,884 (0,746 – 1,082) | 0,460 | 0,430 | 0,240 | 3,594 |
| dentro, corte | 145 | 1,099 (0,938 – 1,397) | 0,569 | 0,533 | 0,240 | 3,970 |
| fuera, cura | 21 | 1,007 (0,744 – 1,209) | 0,517 | 0,416 | 0,161 | 3,871 |
| fuera, corte | 138 | 1,109 (0,894 – 1,460) | 0,578 | 0,637 | 0,120 | 4,030 |

Los cortes abren con más dolor en los tres dominios y más distancia; lo positivo no cambia. Dentro, el cuartil 3 del dolor F de las curas (1,082) queda por debajo
de la mediana de los cortes (1,099): las fotos se solapan, pero están desplazadas.

## Sección 6 · Sensibilidad (después del sello, marcada como tal)

**Lo que pedía el encargo** (s a la mitad y al doble; contexto más blando y más duro), con el efecto sellado:

| variante (después del sello) | P7-10 dentro: B / C | P7-14b dentro: B / C | los dos dentro: B / C |
|---|---:|---:|---:|
| s/2 | 0,432 / 0,400 | 0,412 / 0,461 | 0,426 / 0,429 |
| 2s | 0,432 / 0,438 | 0,412 / 0,423 | 0,426 / 0,440 |
| contexto 0,5 / 0,75 | 0,432 / 0,422 | 0,412 / 0,446 | 0,426 / 0,439 |
| contexto 0,1 / 0,25 | 0,432 / 0,392 | 0,412 / 0,435 | 0,426 / 0,415 |

Ninguna variante saca a C de por debajo de 0,5: el problema no es s ni el contexto, es el efecto.

**Lo que no pedía el encargo y he mirado para entender el fallo** (NO sellado): el efecto puesto a la cura del catálogo si se completa (50) y 0 si se corta, con lo que la
creencia pasa a ser «qué parte de la cura espero», y s más estrecho:

| efecto = cura del catálogo si se completa, 0 si se corta (NO sellado) | A | B | C |
|---|---:|---:|---:|
| P7-10, dentro | 0,552 | 0,435 | 0,558 |
| P7-10, fuera | 0,543 | 0,497 | 0,521 |
| P7-14b, dentro | 0,470 | 0,441 | 0,532 |
| P7-14b, fuera | 0,328 | 0,415 | 0,566 |
| los dos, dentro | 0,540 | 0,450 | 0,552 |
| los dos, fuera | 0,446 | 0,476 | 0,536 |

| … y además s más estrecho (NO sellado) | P7-10 dentro: C | P7-14b dentro: C | los dos dentro: C |
|---|---:|---:|---:|
| s/2 | 0,560 | 0,548 | 0,560 |
| s/4 | 0,561 | 0,565 | 0,568 |
| s/8 | 0,557 | 0,575 | 0,572 |
| s/4 y contexto duro | 0,549 | 0,548 | 0,555 |

Con eso C separa mejor que B (por 0,10 en los dos campos juntos) pero se queda en 0,55-0,57 por mucho que se estreche s: los recuerdos de días anteriores,
pesados por parecido, saben menos del corte que la foto de ahora (0,72). Con una mediana de 7,4 de peso vivido por apertura (frente a 18,0 en B), la creencia C
se apoya en pocos recuerdos.

## Sección 7 · Lo que esto dice, y lo que queda para la mesa

1. El diseño (todo recuerdo con su marca emocional; recordar por parecido) se ha probado tal como se fijó y **no pasa el sello**. La causa principal no es el parecido sino
   **qué guarda el recuerdo**: «cuánto subió la vida» choca con el techo de 100 y hace que las curas en cuerpos sanos valgan poco. El cuaderno del campo ya trata esto con el
   «al menos» de P7-7; este banco no lo hizo, por fijar un efecto simple. Es un fallo de lo que fijé yo, no del diseño de Manel, y lo digo.
2. Aun arreglado eso (efecto = cura del catálogo, no sellado), recordar por parecido llega a 0,55-0,57 dentro del círculo, por encima de B (0,45) y por debajo del 0,65 pedido.
   La foto de ahora separa más (0,72). Un recuerdo que guardase *si se completó* además de *cuánto curó*, o una creencia de dos partes (probabilidad de completar × cura),
   es otro diseño: se propone, no se hace.
3. Fuera del círculo, la creencia baja pronto pero los recuerdos de dentro la levantan por el contexto 0,25. Si el corte por el anillo fuera del círculo es casi seguro
   (P7-21: 85 % de los canales fuera los corta el anillo), el parecido de contexto dentro/fuera tendría que ser más duro que 0,25, o el recuerdo de fuera más pesado.
4. R4 falla porque la cura imaginada con C es un tercio de la del campo (sin el «al menos»); con esa cura el cuerpo se queda quieto en vez de usar. No dice nada de la
   idea de recordar por parecido en sí; dice que el efecto del recuerdo tiene que llevar el techo.
5. Nada de esto se ha jugado; son réplicas y recuerdos leídos de los diarios.

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P7_22.md` | el sello, con s, el umbral, las reglas y los md5 |
| `recuerdos_P7_22.py` → `P7_22_recuerdos.json` | los 467 recuerdos |
| `banco_P7_22.py` → `P7_22_fijado.json`, `P7_22_resultado.json` | s y umbral; separaciones, R3, mapa emocional, sensibilidad |
| `banco_decide_P7_22.py` → `P7_22_decisiones.json` | la repetición de decisiones (R4, medida 2) |
| `P7_22_extra_catalogo.json`, `P7_22_extra_catalogo_s.json` | lo no sellado de la sección 6 |
| `informe_P7_22.md` | este informe |

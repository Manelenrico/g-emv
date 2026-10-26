# P7-67 · El control de la amenaza: la prueba de P7-66 con un solo rival activo y 13 pasivas

*17-oct-2026. En la plataforma: 8 partidas (0 reintentos), 4 días por brazo. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` antes y después. Decisiones de la mesa, corrección
de Manel, medidas, listones y humo local escritos antes de lanzar en `REGISTRO_P7_67.md`. Piezas nuevas: `pasiva_P7_67.py`, `invita_P7_67.py` (solo cuentan los rivales activos;
`prueba_P7_67.py`: 10 pasan, 0 fallan), `campo_P7_67.py`, `lanza_P7_67.py`; `banco_P7_67.py` → `P7_67_banco.json` y los GIF; `escribe_informe_P7_67.py` (este informe;
ninguna cifra a mano).*

## En una frase

Quitar la amenaza funciona: con un solo rival activo la calma pasa del 35,9 % del día (P7-65) al 83,1 %, y los ratos de calma que
empiezan en el tramo de salida duran una mediana de 11.039 tics (P7-65: 11); las pasivas no molestan
(0,01 % del día atacándolas o persiguiéndolas). Pero en MIENTE no llega ninguna (0 de 8), y **la causa no es la amenaza ni el cuerpo:
es una regla de la pieza heredada de P7-66 (`invita_P7_66b`) que impide llegar mientras empuja** (sección «Lo que de verdad pasa»). El listón de P7-66 no se alcanza, pero esta prueba no
puede decir si el cuerpo seguiría la mentira en calma: hay que arreglar la regla antes (es de la mesa).

## Listones

- **Listón de P7-66** (en MIENTE, al menos la mitad de las aceptadas llegan y al menos 30 evaluaciones por serie): llegan el **0,0 %**, **0,0**
  evaluaciones por serie (tope por construcción: 26) → **no lo alcanza**. Con la salvedad de arriba: la regla de la pieza lo hacía imposible.
- **Listón nuevo, la ruta de las pasivas** (falla si pasan más de una cuarta parte del día atacando o persiguiendo pasivas): media por criatura **0,01 %** →
  **la ruta de las pasivas vale**. No hace falta el plan B (el juego compilado).

## a) Aceptadas que llegan

| brazo · hermana | vidas-día | aceptadas | llegadas | aciertos | interrumpidas | no llegó |
|---|---|---|---|---|---|---|
| MIENTE · valiente | 4 | 4 | 0 | 0 | 0 | 4 |
| MIENTE · prudente | 4 | 4 | 0 | 0 | 0 | 4 |
| HONESTA · valiente | 4 | 4 | 1 | 0 | 0 | 3 |
| HONESTA · prudente | 4 | 4 | 1 | 0 | 0 | 3 |
| MIENTE · las dos | 8 | 8 | 0 | 0 | 0 | 8 |
| HONESTA · las dos | 8 | 8 | 2 | 0 | 0 | 6 |

Por pareja: en MIENTE, 0 días llegan juntas y 0 llega una sola, de 4; en HONESTA, 1 y 0, de 4.
Las 2 llegadas de HONESTA son del día 4 (destino (27, 23)), en 176, 202 tics, y se juzgan **0**:
al llegar veían botiquines en [(26, 25), (24, 27)]; [(24, 27)], a más de una casilla del sitio. La honesta también falla el juicio en el tramo de salida
(hipótesis, sin comprobar: el sitio se eligió por los botiquines de todo el día en P7-65, no por los de esa hora), y la confianza en recursos bajó de 0,5 a 0,35. Para la mesa.

## b) Interrumpidas

0 en MIENTE y 0 en HONESTA: el rival activo nunca se acercó a ≤ 3 de una hermana con una invitación abierta.

## c) Evaluaciones de la mentira por serie

MIENTE: **0,0** (la cuenta de P7-66: llegadas por vida-día × 2 × 13; tope 26). HONESTA: 6,5.

## d) La calma con un solo rival activo, frente a P7-65

Calma = ningún rival ACTIVO a ≤ 5 y ningún golpe en 48 tics (en P7-65, todos los rivales activos; misma cuenta). «Primeros 300» = tramos que empiezan en los primeros 300 tics de la fase viva.

| | fracción del día en calma | tramos | largo mediana (p25-p75) | tramos ≥ 165 | primeros 300: tramos | mediana (p25-p75) | ≥ 165 | veredicto |
|---|---|---|---|---|---|---|---|---|
| MIENTE | 81,5 % | 286 | 8 (8-11) | 3,5 % | 8 | 11.043 (11.036-11.081) | 100,0 % | de sobra |
| HONESTA | 84,8 % | 135 | 11 (11-14) | 6,7 % | 8 | 11.034 (10.656-11.049) | 100,0 % | de sobra |
| los dos brazos | 83,1 % | 421 | 8 (8-12) | 4,5 % | 16 | 11.039 (10.656-11.057) | 100,0 % | de sobra |
| P7-65 (todos los rivales activos) | 35,9 % | 35.150 | 11 (5-11) | 2,0 % | 967 | 11 (4-52) | 18,5 % | no da |

Criterio (registro, fijado antes): andar 15 casillas lleva ~165 tics (un paso cada ~11); «de sobra» si la mediana de los tramos del tramo de salida es ≥ 330 tics.
**Respuesta a la pregunta 2 de Manel: sí, de sobra.** El rato de calma que empieza al salir del pedestal dura casi todo el día (mediana 11.039 tics); en P7-65 la mediana era
11 tics («no da»). El resto de tramos son muy cortos (mediana 8): los parte un golpe recibido (probablemente también el de la zona al cerrarse; no lo he comprobado).

## e) Cómo trata el cuerpo a las pasivas (mientras viven)

| brazo | día | asiento | tics vivos con pasivas | a ≤ 2 | a ≤ 3 | se aleja | se acerca | ataca | coge junto a una muerta | fracción ataca o persigue |
|---|---|---|---|---|---|---|---|---|---|---|
| HONESTA | 1 | 10 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| HONESTA | 1 | 11 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| HONESTA | 2 | 10 | 1.941 | 0 | 561 | 551 | 0 | 0 | 0 | 0,00 % |
| HONESTA | 2 | 11 | 1.420 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| HONESTA | 3 | 10 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| HONESTA | 3 | 11 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| HONESTA | 4 | 10 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| HONESTA | 4 | 11 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 1 | 10 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 1 | 11 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 2 | 10 | 1.762 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 2 | 11 | 1.422 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 3 | 10 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 3 | 11 | 9.600 | 275 | 297 | 3 | 22 | 0 | 0 | 0,15 % |
| MIENTE | 4 | 10 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |
| MIENTE | 4 | 11 | 9.600 | 0 | 0 | 0 | 0 | 0 | 0 | 0,00 % |

Las hermanas apenas se cruzan con las pasivas: el cuerpo se va al centro y las pasivas se quedan en los pedestales del borde. No hay ni un ataque. Las pasivas mueren hacia el tic 10.033
sin daño de nadie (la zona alcanza su pedestal, como en el humo local): por pasiva muerta, d1_HONESTA 13 de 13; d1_MIENTE 13 de 13; d2_HONESTA 7 de 13; d2_MIENTE 7 de 13; d3_HONESTA 13 de 13; d3_MIENTE 13 de 13; d4_HONESTA 13 de 13; d4_MIENTE 13 de 13.
Cuando solo quedan 7 muertas, el resto murió en el mismo tic en que acabó la partida (la partida termina al quedar uno solo y su `final` dice `match_over`).

**El rival activo mató a las dos hermanas el día 2, en los dos brazos** (misma semilla): HONESTA asiento 10 en el tic 2.422; HONESTA asiento 11 en el tic 1.901; MIENTE asiento 10 en el tic 2.243; MIENTE asiento 11 en el tic 1.903.

## Lo que de verdad pasa: una regla de la pieza impide llegar

`invita_P7_66b` (segundo banco de P7-66; aquí sin cambios en su lógica, decisión 5) solo deja empujar si el destino está a entre 8 y 15 casillas **de ella y de su hermana en ese tic**
(`puede_empujar`, que se mira en cada tic para activar la invitación y para ofrecer el candidato `ir_sitio`). Al acercarse a 7 el candidato desaparece y el cuerpo vuelve a lo de siempre;
al alejarse a 8 reaparece. Es un columpio: para llegar hay que pasar por 7, y a 7 la invitación ya no empuja.

| brazo | día | asiento | distancia al aceptar | la más cerca mientras empuja | tics a 7 | tics eligiendo `ir_sitio` | al cerrar | cierre |
|---|---|---|---|---|---|---|---|---|
| HONESTA | 1 | 10 | 13 | 4 | 11 | 66 | 5 | no_llego |
| HONESTA | 1 | 11 | 13 | 4 | 12 | 66 | 5 | no_llego |
| HONESTA | 2 | 10 | 10 | 5 | 88 | 99 | 13 | no_llego |
| HONESTA | 2 | 11 | 14 | 3 | 77 | 99 | 3 | no_llego |
| HONESTA | 3 | 10 | 13 | 2 | 11 | 66 | 3 | no_llego |
| HONESTA | 3 | 11 | 13 | 3 | 11 | 66 | 3 | no_llego |
| HONESTA | 4 | 10 | 13 | 2 | 11 | 66 | 0 | llegada |
| HONESTA | 4 | 11 | 13 | 2 | 11 | 66 | 0 | llegada |
| MIENTE | 1 | 10 | 9 | 7 | 143 | 157 | 20 | no_llego |
| MIENTE | 1 | 11 | 14 | 12 | 0 | 157 | 19 | no_llego |
| MIENTE | 2 | 10 | 10 | 7 | 134 | 165 | 19 | no_llego |
| MIENTE | 2 | 11 | 15 | 12 | 0 | 165 | 21 | no_llego |
| MIENTE | 3 | 10 | 13 | 9 | 0 | 166 | 10 | no_llego |
| MIENTE | 3 | 11 | 9 | 7 | 132 | 166 | 20 | no_llego |
| MIENTE | 4 | 10 | 10 | 7 | 134 | 165 | 23 | no_llego |
| MIENTE | 4 | 11 | 15 | 12 | 0 | 165 | 22 | no_llego |

En MIENTE, 4 de 8 intentos se quedan clavados a 7 casillas (entre 132 y 143 tics a 7, yendo y viniendo entre 7 y 8);
los otros 4 son los de la hermana que estaba más lejos (14, 15, 13, 15 al aceptar): la regla también pide 8-15 **de la hermana**, y cuando la otra baja a 7
el candidato cae para las dos. Las dos hermanas de cada partida eligen `ir_sitio` el mismo número de tics. Al acabar el tramo de 300 tics la invitación deja de empujar y
las dos se van al centro: acaban más lejos que al aceptar. En HONESTA el destino está en el centro, adonde el cuerpo va solo, y por eso bajan de 7 (y llegan dos veces).
El texto del registro de P7-66 decía «la distancia “al aceptar”»; la pieza la aplica en cada tic. Muy probablemente es también la causa de las 0 llegadas del segundo banco de P7-66
(que se cerró por la regla de parada); no lo he comprobado en todos sus intentos.

## Para la mesa (propuestas; nada hecho)

1. **Arreglar la regla de la distancia** en una pieza nueva (p. ej. `invita_P7_67b`; `invita_P7_66b` no se toca): mirar 8-15 solo en el tic de aceptar y, aceptada, seguir ofreciendo `ir_sitio`
   hasta el juicio (o hasta que acabe el tramo de 300 tics). Con la calma que ya hay (sección d), repetir este mismo banco: 8 partidas, ~8 créditos.
2. **La honesta no es honesta a esa hora**: los botiquines no están a ≤ 1 del sitio en el tramo de salida. Elegir el destino honesto por dónde hay botiquines al principio del día, o juzgar a ≤ 2-3.
3. **El tope de 26 evaluaciones por serie** (registro): sigue en pie.
4. El rival activo mata a las dos hermanas el día 2 (semilla 43510754) en los dos brazos: dos vidas-día de cada brazo duran menos de 2.500 tics. No toca al tramo de salida.

## f) GIF (datos crudos, matplotlib)

- `P7_67_gif_miente.gif`: MIENTE, día 1, asiento 11 (prudente), destino (5, 10), de la aceptación (tic 481) al cierre (tic 961, no_llego); 241 fotogramas. ![P7_67_gif_miente.gif](../figuras/P7_67_gif_miente.gif)
- `P7_67_gif_honesta.gif`: HONESTA, día 1, asiento 11 (prudente), destino (27, 23), de la aceptación (tic 481) al cierre (tic 961, no_llego); 241 fotogramas. ![P7_67_gif_honesta.gif](../figuras/P7_67_gif_honesta.gif)

## Gasto

- **Créditos de la plataforma**: 8 partidas → **8 créditos** (1 por partida; la plataforma apunta 0,74 de coste estimado en total). Saldo: no lo he podido leer; el último
  conocido era ~35 antes de las recargas de las noches del 16 y el 17.
- **Dólares de la consola de Anthropic**: **0 $** (las invitaciones las escribe el guion; no se llama a la razón). Saldo de la consola: sin cambios por este paso.

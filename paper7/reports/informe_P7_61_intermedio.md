# P7-61 · INTERMEDIO · El campo de la mentira: lectura de las series 1-3 (declarada y NO vinculante)

*14-oct-2026. **INTERMEDIO** (addendum 6 del sello): sobre las series 1, 2, 3 (240 vidas); la serie 4 se juega pase lo que pase y **el veredicto sellado será
el de las 4 series** (o las que pida el addendum 4). Tras esta lectura no se cambia ninguna pieza, medida ni criterio. `analiza_P7_61.py` → `P7_61_intermedio.json`;
`escribe_informe_P7_61_intermedio.py` (ninguna cifra a mano). Comparación: CON_RAZON de P7-56 (3 series). `motor/model.py` intacto.*

Comprobación: las invitaciones de cada vida reconstruidas (honestas de la respuesta guardada + la falsa en su posición) cuadran con el arranque en todas (0 que no).

## INTERMEDIO · Las predicciones (una observación por serie; ≥ 3 ee para pasar)

| | qué | A (por serie → media) | B (por serie → media) | A − B ± ee | dirección |
|---|---|---|---|---|---|
| M1 | confianza en el cuerpo, d14-20 | MIENTEN_DOS 0,601 · 0,662 · 0,629 → 0,631 | CON_RAZON P7-56 0,773 · 0,426 · 0,658 → 0,619 | 0,012 ± 0,103 (0,1 ee; sin marcadas 0,1 ee) | la contraria |
| M2 | verdaderas aceptadas / cargadas, d12-20 | MIENTEN_DOS 0,384 · 0,340 · 0,329 → 0,351 | CON_RAZON P7-56 0,268 · 0,350 · 0,305 → 0,308 | 0,043 ± 0,029 (1,5 ee; sin marcadas 1,2 ee) | la contraria |
| M3 | valiente: aceptaciones de la falsa / oportunidades, d10-20 | MIENTE_UNA 0,364 · 0,364 · 0,455 → 0,394 | MIENTEN_DOS 0,273 · 0,273 · 0,091 → 0,212 | 0,182 ± 0,068 (2,7 ee; sin marcadas 2,7 ee) | la contraria |

MIENTE_UNA, de referencia: M1 0,660 · 0,688 · 0,651; M2 0,375 · 0,355 · 0,472. M3: s1: 4/11 frente a 3/11, s2: 4/11 frente a 3/11, s3: 5/11 frente a 1/11 (la falsa estuvo activa todos los días 10-20).

**INTERMEDIO: ninguna pasa.** M1 y M2 van en la dirección contraria o sin diferencia (con la mentira, la confianza en el cuerpo y la aceptación de verdaderas no bajan); M3 va al revés de lo
previsto: la valiente con la hermana honesta acepta la falsa MÁS, no menos.

## INTERMEDIO · M1b (cada evaluación de la falsa: confianza en el cuerpo después − antes) y la comprobación por criatura (addendum 5)

| | evaluaciones | media ± ee (por evaluación) | criaturas que caen | ee agrupado por criatura |
|---|---:|---|---|---|
| MIENTEN_DOS | 31 | -0,011 ± 0,033 (0,3 ee) | 3 de 6 | 0,009 (1,3 ee) |
| MIENTE_UNA | 11 | -0,100 ± 0,058 (1,7 ee) | 3 de 3 | 0,016 (6,1 ee) |
| los dos | 42 | -0,034 ± 0,029 (1,2 ee) | 6 de 9 | 0,019 (1,8 ee) |

Por criatura (n · media): s1 MIENTEN_DOS a10 3 · 0,013; s1 MIENTEN_DOS a11 3 · 0,018; s1 MIENTE_UNA a10 2 · -0,047; s2 MIENTEN_DOS a10 3 · -0,066; s2 MIENTEN_DOS a11 4 · -0,037; s2 MIENTE_UNA a10 4 · -0,126; s3 MIENTEN_DOS a10 1 · 0,001; s3 MIENTEN_DOS a11 17 · -0,005; s3 MIENTE_UNA a10 5 · -0,102.

**INTERMEDIO**: la dirección es la prevista (cae), pero por evaluación no llega (1,2 ee; sin marcadas 1,2). La caída la llevan las valientes de
MIENTE_UNA (las tres caen); la prudente de MIENTEN_DOS de la serie 3, con 17 evaluaciones, casi no se mueve. El ee agrupado es MENOR que el de
evaluación porque la variación está dentro de cada criatura (aciertos y fallos alternan), no entre criaturas: no es un error, pero con 9 criaturas se lee con cuidado.

## INTERMEDIO · M2b (aceptar verdaderas con cuerpo, 2 noches después − 2 antes del primer fallo de la falsa)

Criaturas con fallo de la falsa: 8 de 9 con la falsa evaluada; entran 8. Cambio medio -0,161 frente a -0,049 en la misma ventana de CON_RAZON de P7-56:
-0,112 ± 0,129 (0,9 ee), dirección la prevista. Sin potencia (addendum 2); se informa con su dirección.

## INTERMEDIO · Vigilancia

| brazo · hermana | vidas | puesto medio | muertes | vida perdida media | usos del botiquín · cortados | vida perdida en curas cortadas (por vida) |
|---|---:|---:|---:|---:|---|---:|
| MIENTEN_DOS · valiente | 60 | 4,28 | 16 | 119,8 | 74 · 35 | 5,7 |
| MIENTEN_DOS · prudente | 60 | 4,35 | 26 | 123,8 | 109 · 57 | 7,7 |
| MIENTE_UNA · valiente | 60 | 5,32 | 25 | 114,2 | 77 · 41 | 4,0 |
| MIENTE_UNA · prudente | 60 | 3,97 | 25 | 130,8 | 157 · 102 | 13,7 |
| CON_RAZON · valiente (P7-56) | 60 | 5,88 | 27 | 109,3 | 79 · 42 | 5,0 |
| CON_RAZON · prudente (P7-56) | 60 | 5,25 | 30 | 115,9 | 106 · 68 | 8,7 |

**Refuerzo intermitente**: de 42 evaluaciones de la falsa, 20 la confirman (48 %; suben la confianza 0,143 de media) y 22 la
desmienten (-0,196); caída media neta -0,034 frente a -0,033 de las falsas de P7-56 (que fallaban siempre). Además, 168 contrastes con lo
contado por la hermana tocaron la falsa y 128 la confirmaron (cambio medio por contraste -0,021).

## INTERMEDIO · ¿Algo roto en el funcionamiento? (aparte de los números)

1. **La falsa no se juzga como dice el sello.** El sello (y P7-57) dice: si la cura se corta, se evalúa a los 480 tics por el cambio de vida (casi siempre fallo). El código de
   `invita_P7_54` (que no se toca) juzga con el PRIMER uso del botiquín SIN corte dentro de los 480 tics tras aceptar; un uso cortado no cuenta y espera al siguiente. De 42 evaluaciones,
   12 tuvieron el primer uso cortado por un golpe y aun así 8 acabaron como ACIERTO (lo juzgó una cura posterior sin golpe); por 480 tics: 1.
2. **La falsa se desmiente por el techo de vida, no por los golpes.** De 22 fallos, 19 son curas sin corte que llegaron a 100 (la vida de partida era alta: media 85,8
   en los fallos frente a 49,8 en los aciertos): la cura no podía dar +25. La lección que recibe la confianza es «el botiquín no cura cuando estoy casi sana», no «no cura si me golpean».
3. **Lo contado confirma la falsa fuera de su situación.** El contraste de `invita_P7_57` compara lo contado con la promesa por OBJETO, sin mirar la situación: una cura de la hermana en calma
   «confirma» una promesa hecha para la amenaza. Es el diseño sellado (no un fallo de código), pero añade refuerzo que la mentira no debería recibir.
4. Lo demás funciona: la falsa se inserta en todas las noches previstas (días 8-20 en los asientos que mienten), se activa todos los días, las invitaciones reconstruidas cuadran con el
   arranque, la guarda y los reintentos funcionaron, y las noches sin razón (2) quedaron anotadas.

Con 1 y 2, M1-M3 y M1b miden una mentira que el cuerpo apenas puede desmentir por lo que la hace falsa (los golpes). **No se cambia nada** (addendum 6); se propone para después del campo
que la mesa decida si el juicio de la falsa debe contar el uso cortado y descontar el techo de vida.

## Gasto (hasta el cierre de la serie 3)

- Plataforma: 122 partidas pedidas (humo, 3 series y 2 reintentos; alguna cuenta 0); último saldo leído: 19 créditos (14-oct, 17:03).
- Consola de Anthropic: 14,33 $ en 228 llamadas a la razón (tarifa supuesta 3/15 $ por millón).

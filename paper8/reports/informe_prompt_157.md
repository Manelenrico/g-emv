# Prompt 157: los tramos en los mundos sin escasez y dos preguntas sobre el mundo

*19-nov-2026. Solo se ha leído: ninguna partida jugada, nada sellado tocado y la clave sin usar. Todo es análisis hecho después de ver los datos, no predicción. No se proponen causas de las diferencias entre jugadores.*

Hecho con un programa nuevo, `tramos_y_ritmos_157.py`, que usa la caché del 156 (`felicidad_dia_a_dia/partidas.json`) y sus piezas. La salida está en `salida/tramos_y_ritmos_157.md` y `.json`.
- **Las diferencias** son emparejadas por semilla, con intervalo del 95 %: el bootstrap de siempre, con 10.000 remuestreos y semilla 8.
- **Los días van del 1 al 40.**

## Parte 1: los tramos en los tres mundos sin escasez

Son cuatro tramos de diez días. Por partida se toma la media de los días del tramo; la felicidad de la aldea del día va de 0 a 100. Las medias van en el orden: decide con el motor (RG69r+voz) · decide sumando (S69+voz) · decide con la posición (P69+voz).

### Abundancia: felicidad

| tramo | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| 1-10 | 91,9 · 89,3 · 88,1 | +2,5 [+0,8, +4,5] | +3,7 [+2,3, +5,1] |
| 11-20 | 91,9 · 88,7 · 86,7 | +3,2 [+1,9, +4,5] | +5,2 [+3,6, +6,8] |
| 21-30 | 92,4 · 90,1 · 88,9 | +2,4 [+1,2, +3,6] | +3,6 [+1,7, +5,5] |
| 31-40 | 92,5 · 90,3 · 91,2 | +2,2 [+0,9, +3,6] | +1,3 [−0,2, +2,8] |

### Abundancia: empujones por día

| tramo | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| 1-10 | 2,6 · 6,5 · 4,3 | −3,9 [−5,0, −2,8] | −1,6 [−2,2, −1,1] |
| 11-20 | 1,3 · 2,5 · 3,1 | −1,2 [−1,7, −0,6] | −1,8 [−2,4, −1,2] |
| 21-30 | 1,4 · 1,9 · 2,6 | −0,4 [−0,9, +0,0] | −1,2 [−1,7, −0,7] |
| 31-40 | 1,3 · 1,9 · 2,1 | −0,6 [−1,0, −0,1] | −0,8 [−1,2, −0,4] |

### Normal: felicidad

| tramo | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| 1-10 | 83,0 · 80,4 · 78,2 | +2,6 [+0,4, +4,9] | +4,8 [+2,7, +6,9] |
| 11-20 | 77,4 · 76,2 · 74,2 | +1,2 [−1,7, +4,1] | +3,2 [+0,7, +5,7] |
| 21-30 | 78,9 · 78,4 · 77,3 | +0,5 [−2,0, +3,0] | +1,7 [−0,8, +4,1] |
| 31-40 | 79,4 · 80,3 · 78,1 | −1,0 [−3,3, +1,3] | +1,3 [−1,1, +3,6] |

### Normal: empujones por día

| tramo | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| 1-10 | 3,6 · 6,5 · 5,3 | −2,9 [−3,8, −2,1] | −1,7 [−2,3, −1,1] |
| 11-20 | 3,0 · 2,8 · 3,3 | +0,3 [−0,4, +0,9] | −0,2 [−0,7, +0,3] |
| 21-30 | 2,8 · 2,5 · 3,0 | +0,4 [−0,2, +0,9] | −0,2 [−0,8, +0,5] |
| 31-40 | 2,6 · 1,9 · 2,7 | +0,6 [+0,2, +1,1] | −0,1 [−0,6, +0,3] |

### Bestias que crían: felicidad

| tramo | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| 1-10 | 69,6 · 64,6 · 62,2 | +5,1 [+1,5, +8,7] | +7,4 [+4,1, +10,9] |
| 11-20 | 61,8 · 54,5 · 56,0 | +7,3 [+3,4, +11,1] | +5,7 [+2,7, +8,9] |
| 21-30 | 40,5 · 37,7 · 34,4 | +2,9 [−1,2, +7,1] | +6,1 [+1,8, +10,6] |
| 31-40 | 40,7 · 38,1 · 37,9 | +2,6 [−1,4, +6,6] | +2,8 [−1,6, +7,2] |

### Bestias que crían: empujones por día

| tramo | motor · suma · posición | RG69r+voz − S69+voz | RG69r+voz − P69+voz |
|---|---|---|---|
| 1-10 | 4,1 · 6,5 · 5,9 | −2,5 [−3,4, −1,6] | −1,8 [−2,3, −1,4] |
| 11-20 | 3,4 · 3,9 · 3,6 | −0,5 [−1,1, +0,1] | −0,2 [−0,8, +0,4] |
| 21-30 | 3,4 · 3,2 · 3,4 | +0,2 [−0,4, +0,7] | −0,1 [−0,5, +0,4] |
| 31-40 | 2,3 · 2,8 · 2,8 | −0,5 [−1,2, +0,1] | −0,5 [−1,0, −0,0] |

### Qué parte de la diferencia total de empujones cae en los días 1 a 10

Para cada mundo, tres números en este orden: la diferencia de empujones de la partida entera, la de los días 1 a 10 (media de las 40 semillas, emparejadas) y la parte, que es la segunda entre la primera.

| mundo | RG69r+voz − S69+voz: partida · días 1-10 · parte | RG69r+voz − P69+voz: partida · días 1-10 · parte |
|---|---|---|
| abundancia | −60,3 · −38,6 · 64 % | −53,7 · −16,4 · 30 % |
| normal | −16,5 · −29,0 · 176 % | −22,6 · −17,0 · 75 % |
| sequía | −34,5 · −37,7 · 109 % | −28,4 · −19,0 · 67 % |
| sequía dura | −26,0 · −27,0 · 104 % | −20,1 · −15,8 · 78 % |
| bestias que crían | −33,4 · −24,8 · 74 % | −25,8 · −18,4 · 71 % |

**Una parte de más del 100 %** quiere decir que en los días 11 a 40 RG69r+voz empuja un poco más que el otro, y que eso devuelve parte de lo ahorrado en los diez primeros. En el normal frente a S69+voz, la diferencia de la partida entera (−16,5) es más pequeña que la de los días 1 a 10 sola (−29,0).

**Lo que se ve:**
- **En la felicidad**, RG69r+voz va por delante o igual en casi todos los tramos. Su ventaja es más clara al principio.
  - En el normal se acaba en los días 21 a 40, y frente a S69+voz incluso antes, en los días 11 a 20.
  - En las bestias que crían frente a S69+voz, los intervalos tocan el cero desde el día 21.
- **En los empujones**, la diferencia está sobre todo en los días 1 a 10, como en las sequías. La abundancia es la excepción: allí RG69r+voz sigue empujando menos todo el resto de la partida.

## Parte 2: dos preguntas sobre el mundo

### Primera: el ritmo de dos días

**La regla del valle con ese ritmo es el ciclo del huerto.** Esto se sabe con seguridad, en el código y en los datos:

- **El código:**
  - el ciclo de cada planta del huerto es de 800 turnos (`valle/config_valle.json:688`), y el día tiene 400 (`config_valle.json:537`); el ciclo es de dos días;
  - en el arranque, «fruto_a_punto_en_el_primer_dia» está encendido (`config_valle.json:695`). Con eso, cada planta madura por primera vez en un turno al azar del primer día (`valle/mundo.py:205-206`, `self.rng.randrange(1, self.dia_turnos)`);
  - después, cada planta vuelve a madurar 800 turnos más tarde (`mundo.py:1079` y `1087`, `P["fin"] += H["ciclo_turnos"]`);
  - así, todas las plantas del huerto dan fruto en los mismos días: el 1, 3, 5…, 39 contados del 1 al 40. «desfase_al_azar» (`config_valle.json:692`) solo cuenta sin ese arranque (`mundo.py:208`).
- **Las otras reglas de 800 turnos** no van todas a la vez:
  - los matorrales dan fruto cada 800 turnos (`config_valle.json:801` y `806`), pero cada uno empieza en un turno al azar entre 1 y 800 (`mundo.py:217`);
  - la comida se pudre en 800 turnos en la bolsa y en la planta (`config_valle.json:655` y `658`). Esa cuenta empieza cuando nace cada fruto, así que la de la planta va con el mismo calendario del huerto.
- **Los datos de las 600 partidas** (eventos «da_fruto» de `mundo.jsonl.gz`, de media por partida):

| mundo | frutos del huerto en los días 1, 3, …, 39 | en los días 2, 4, …, 40 | felicidad días 2, 4, …, 40 menos días 3, 5, …, 39: motor · suma · posición |
|---|---|---|---|
| abundancia | 320,0 | 0,0 | +0,2 [−0,5, +1,0] · −0,7 [−1,7, +0,2] · −2,4 [−3,2, −1,5] |
| normal | 320,0 | 0,0 | −3,7 [−4,7, −2,7] · −8,1 [−9,5, −6,7] · −8,6 [−9,5, −7,6] |
| sequía | 320,0 | 0,0 | −5,7 [−6,5, −4,9] · −9,6 [−10,9, −8,3] · −8,4 [−9,5, −7,3] |
| sequía dura | 319,2 | 0,0 | −5,0 [−6,0, −4,0] · −6,4 [−7,6, −5,2] · −6,1 [−7,3, −4,9] |
| bestias que crían | 320,0 | 0,0 | −8,3 [−9,4, −7,1] · −10,9 [−12,3, −9,6] · −10,0 [−11,2, −8,8] |

  - En los cinco mundos, todo el fruto del huerto cae en los días 1, 3, 5…, 39 y nada en los otros.
  - La felicidad de la aldea es más baja los días 2, 4, …, 40 que los días impares, entre 4 y 11 puntos, en el normal, las dos sequías y las bestias que crían. En la abundancia la diferencia es pequeña o nula.
  - El primer día queda fuera de esta cuenta.
  - El ritmo de dos días también está en las dos sequías, aunque allí las escaseces lo tapan en la figura D.

**Lo que no se puede saber con seguridad:**
- El ritmo de la felicidad va exactamente con el del huerto, pero estos datos no dicen qué parte del huerto lo mueve: el fruto, la comida que se pudre en la planta un ciclo después, o el trabajo en el huerto, que sigue el mismo calendario.
- Para saberlo haría falta comparar con partidas sin ese calendario, y no se ha jugado ninguna.
- He buscado en la configuración todas las reglas con números de 800 y 1.600 turnos y con «cada_dias». No he encontrado otra regla que vaya cada dos días con todas las criaturas a la vez. No puedo descartar alguna regla escrita solo en el código que no tenga esos números.

### Segunda: qué pasa hacia el día 21 en las bestias que crían

**Nace la segunda bestia.** Esto se sabe con seguridad, en el código y en los datos:

- **El código:**
  - el mundo de las bestias que crían enciende la cría, una cada 20 días y hasta 2 (`config_valle.json:890`); el lanzador lo pone así para ese mundo (`cantera/paper8/lanzador.py:38-39`);
  - el contador de la cría empieza en 0 (`mundo.py:226`) y suma 1 cada vez que acaba un día (`mundo.py:362`, desde `mundo.py:711`, al cerrar el día);
  - cuando llega a 20 nace otra bestia, si hay menos del máximo (`mundo.py:363-365`, `_g_nueva("nace")`, que escribe el evento «bestia_nace», `mundo.py:305`);
  - eso pasa al acabar el día 20, y desde el día 21 hay dos bestias.
  - **La tercera no nace.** La cuenta llega otra vez a 20 al acabar el día 40, pero ya hay dos.
- **Los datos de las 600 partidas:**

| mundo | partidas con «bestia_nace» | día en que nace (al acabar ese día) | bestias al empezar el día 20 · el 21 · el 40 (media) |
|---|---|---|---|
| abundancia | 0 de 120 | — | 1,00 · 1,00 · 1,00 |
| normal | 0 de 120 | — | 1,00 · 1,00 · 1,00 |
| sequía | 0 de 120 | — | 1,00 · 1,00 · 1,00 |
| sequía dura | 0 de 120 | — | 1,00 · 1,00 · 1,00 |
| bestias que crían | 120 de 120 | día 20 en las 120 | 1,00 · 2,00 · 2,00 |

**Lo que no se puede saber con seguridad.** La bajada de la felicidad cae justo el día en que empieza a haber dos bestias, en las tres aldeas. Pero estos datos no prueban que la bajada venga de la segunda bestia y no de otra cosa que pase a la vez. No he encontrado ninguna otra regla que cambie ese día: la cría es la única del mundo que va por un contador de días.

## Tropiezos

- Ninguno de importancia.
- Primero corregí con `sed` el rótulo de la tabla de la cría, para dejar claro que la bestia nace al acabar el día que se apunta.
- No he usado Python suelto.

## Lo que entra en el commit

**Entra:**
- este informe;
- `tramos_y_ritmos_157.py` y su salida (`salida/tramos_y_ritmos_157.md` y `.json`);
- la línea de STATUS.

**Queda fuera:** la caché del 156 y los datos de las partidas.

Commit local, sin push.

## El gasto

- **Créditos de la plataforma:** 0.
- **Dólares de la consola de Anthropic:** 0.
- **Los saldos** no se han leído.

# P7-20 · La vida en el primer golpe (propuesta de Ari)

*5-oct-2026. Coste: plataforma 0, consola 0. Solo lectura de los 640 diarios de los dos campos (P7-10 y P7-14b, 80 vidas por brazo y campo), posterior a
los sellos; no se ha jugado ni replicado nada. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`; cuerpo sin tocar.
`analiza_P7_20.py` → `P7_20_vidas.json` (640 vidas, 1373 peleas, 238 acaban en muerte); este informe lo escribe `escribe_informe_P7_20.py` desde ese archivo.
En P7-10 el brazo ESPERANZA es el que entonces se llamaba SUELO.*

## Lo que sale, en corto

- **La lectura de Ari no se ve en esta medida.** En las muertes tempranas, el que aprende recibe el primer golpe de la pelea que lo mata con la vida entera
  en la mediana, igual que el que olvida: 100,0 y 100,0 (antes del tic 12.000, los dos campos; 27 y 12 peleas).
- **Sí hay una diferencia, pequeña y de pocos casos:** contando la vida ante el primer golpe de rival de la racha, el que aprende entra por debajo de 100 en 12 de 27 de esas peleas; el que olvida, en 4 de 12.
  Casi toda está en el primer campo (P7-10), donde la mediana del que aprende baja a 92,0; en el segundo campo es 100.
- **En las peleas que no matan, no entra con menos vida que el que olvida** (sección 3): su mediana es 100 en los dos cortes y en los dos campos.
- **Contra el que olvida en la misma semilla** (sección 4): en el tic del primer golpe, el que olvida tenía más vida en unas muertes y menos en otras, casi a partes iguales; la diferencia mediana es 0.

## Sección 1 · Definiciones, puestas antes de contar

- **Golpe de rival**: una entrada de `damage_taken` del diario cuya fuente es un jugador. **Daño del anillo**: fuente `zone`.
- **Racha de daño**: tics con daño (de rival o del anillo) sin un hueco de más de 10 segundos (240 tics). **Pelea**: una racha con al menos un golpe de rival.
- **Primer golpe** (la del encargo, al pie de la letra): el primer daño de rival después de 10 segundos sin daño de ninguna clase; es el primer daño de la
  racha cuando ese daño es de un rival. Una pelea que empieza con daño del anillo no tiene primer golpe con esta definición: se da aparte, como variante,
  la vida ante el primer golpe de rival de la racha.
- **Vida en el primer golpe**: la del tic anterior a ese golpe. La vida máxima vista en las 640 vidas es 100.
- **La pelea acaba en muerte**: la vida muere y es su última racha, con el último daño a 10 segundos o menos del final.
- **Muerte temprana**: muere antes del tic 11.000; y, aparte, antes del 12.000.

## Sección 2 · La vida en el primer golpe de la pelea que acaba en muerte

**Antes del tic 11.000**

| campo | brazo | muertes tempranas | con pelea final contra rival | mueren sin ella (anillo) | con primer golpe (definición) | vida en el primer golpe, mediana | mínimo | variante: ante el primer golpe de rival de la racha, mediana (n) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 4 | 4 | 0 | 4 | 100,0 | 100 | 100,0 (4) |
| P7-10 | BORRADO | 3 | 3 | 0 | 2 | 100,0 | 100 | 100,0 (3) |
| P7-10 | APRENDE | 10 | 10 | 0 | 10 | 92,0 | 50 | 92,0 (10) |
| P7-10 | TECHO | 5 | 4 | 1 | 4 | 85,0 | 32 | 85,0 (4) |
| P7-14b | ESPERANZA | 11 | 7 | 4 | 7 | 100,0 | 58 | 100,0 (7) |
| P7-14b | BORRADO | 4 | 4 | 0 | 4 | 98,5 | 12 | 98,5 (4) |
| P7-14b | APRENDE | 10 | 8 | 2 | 8 | 100,0 | 62 | 100,0 (8) |
| P7-14b | TECHO | 8 | 8 | 0 | 8 | 100,0 | 67 | 100,0 (8) |
| los dos | ESPERANZA | 15 | 11 | 4 | 11 | 100,0 | 58 | 100,0 (11) |
| los dos | BORRADO | 7 | 7 | 0 | 6 | 100,0 | 12 | 100,0 (7) |
| los dos | APRENDE | 20 | 18 | 2 | 18 | 100,0 | 50 | 100,0 (18) |
| los dos | TECHO | 13 | 12 | 1 | 12 | 100,0 | 32 | 100,0 (12) |

**Antes del tic 12.000**

| campo | brazo | muertes tempranas | con pelea final contra rival | mueren sin ella (anillo) | con primer golpe (definición) | vida en el primer golpe, mediana | mínimo | variante: ante el primer golpe de rival de la racha, mediana (n) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 10 | 6 | 4 | 6 | 100,0 | 100 | 100,0 (6) |
| P7-10 | BORRADO | 9 | 6 | 3 | 5 | 100,0 | 94 | 100,0 (6) |
| P7-10 | APRENDE | 19 | 16 | 3 | 15 | 92,0 | 42 | 93,0 (16) |
| P7-10 | TECHO | 6 | 4 | 2 | 4 | 85,0 | 32 | 85,0 (4) |
| P7-14b | ESPERANZA | 18 | 10 | 8 | 9 | 100,0 | 32 | 93,0 (10) |
| P7-14b | BORRADO | 7 | 6 | 1 | 6 | 100,0 | 12 | 100,0 (6) |
| P7-14b | APRENDE | 16 | 11 | 5 | 11 | 100,0 | 62 | 100,0 (11) |
| P7-14b | TECHO | 10 | 10 | 0 | 9 | 100,0 | 67 | 100,0 (10) |
| los dos | ESPERANZA | 28 | 16 | 12 | 15 | 100,0 | 32 | 100,0 (16) |
| los dos | BORRADO | 16 | 12 | 4 | 11 | 100,0 | 12 | 100,0 (12) |
| los dos | APRENDE | 35 | 27 | 8 | 26 | 100,0 | 42 | 100,0 (27) |
| los dos | TECHO | 16 | 14 | 2 | 13 | 100,0 | 32 | 100,0 (14) |

Las muertes «sin pelea final contra rival» son las del anillo solo: su última racha de daño no tiene ningún golpe de rival.

**Reparto** (vida ante el primer golpe de rival de la pelea que mata; los dos campos):

Antes del tic 11.000:

| brazo (los dos campos) | peleas que acaban en muerte | 100 | 75–99 | 50–74 | menos de 50 | por debajo de 100 |
|---|---:|---:|---:|---:|---:|---:|
| ESPERANZA | 11 | 9 | 1 | 1 | 0 | 2 de 11 |
| BORRADO | 7 | 4 | 1 | 0 | 2 | 3 de 7 |
| APRENDE | 18 | 11 | 4 | 3 | 0 | 7 de 18 |
| TECHO | 12 | 9 | 0 | 2 | 1 | 3 de 12 |

Antes del tic 12.000:

| brazo (los dos campos) | peleas que acaban en muerte | 100 | 75–99 | 50–74 | menos de 50 | por debajo de 100 |
|---|---:|---:|---:|---:|---:|---:|
| ESPERANZA | 16 | 11 | 1 | 1 | 3 | 5 de 16 |
| BORRADO | 12 | 8 | 2 | 0 | 2 | 4 de 12 |
| APRENDE | 27 | 15 | 7 | 4 | 1 | 12 de 27 |
| TECHO | 14 | 9 | 1 | 3 | 1 | 5 de 14 |

## Sección 3 · Las peleas que NO acaban en muerte

**En las mismas vidas (las de muerte temprana), como pedía el encargo.** Antes del tic 11.000:

| campo | brazo | peleas que NO acaban en muerte, en las vidas de muerte temprana | con primer golpe (definición) | vida en el primer golpe, mediana | por debajo de 100 |
|---|---|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 3 | 3 | 100,0 | 1 de 3 |
| P7-10 | BORRADO | 1 | 1 | 100,0 | 0 de 1 |
| P7-10 | APRENDE | 12 | 12 | 100,0 | 3 de 12 |
| P7-10 | TECHO | 4 | 4 | 100,0 | 1 de 4 |
| P7-14b | ESPERANZA | 4 | 4 | 100,0 | 1 de 4 |
| P7-14b | BORRADO | 7 | 7 | 90,0 | 4 de 7 |
| P7-14b | APRENDE | 1 | 1 | 100,0 | 0 de 1 |
| P7-14b | TECHO | 7 | 7 | 100,0 | 0 de 7 |
| los dos | ESPERANZA | 7 | 7 | 100,0 | 2 de 7 |
| los dos | BORRADO | 8 | 8 | 95,0 | 4 de 8 |
| los dos | APRENDE | 13 | 13 | 100,0 | 3 de 13 |
| los dos | TECHO | 11 | 11 | 100,0 | 1 de 11 |

Antes del tic 12.000:

| campo | brazo | peleas que NO acaban en muerte, en las vidas de muerte temprana | con primer golpe (definición) | vida en el primer golpe, mediana | por debajo de 100 |
|---|---|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 8 | 8 | 100,0 | 1 de 8 |
| P7-10 | BORRADO | 7 | 7 | 100,0 | 0 de 7 |
| P7-10 | APRENDE | 20 | 20 | 100,0 | 4 de 20 |
| P7-10 | TECHO | 4 | 4 | 100,0 | 1 de 4 |
| P7-14b | ESPERANZA | 12 | 10 | 100,0 | 3 de 10 |
| P7-14b | BORRADO | 9 | 9 | 100,0 | 4 de 9 |
| P7-14b | APRENDE | 5 | 5 | 100,0 | 1 de 5 |
| P7-14b | TECHO | 10 | 10 | 100,0 | 1 de 10 |
| los dos | ESPERANZA | 20 | 18 | 100,0 | 4 de 18 |
| los dos | BORRADO | 16 | 16 | 100,0 | 4 de 16 |
| los dos | APRENDE | 25 | 25 | 100,0 | 5 de 25 |
| los dos | TECHO | 14 | 14 | 100,0 | 2 de 14 |

Son pocas peleas por brazo. Para tener más, **lo mismo en las 80 vidas de cada brazo y campo** (no solo las que mueren pronto), con las peleas que no
acaban en muerte y empiezan antes del tic 12.000; esto es un añadido mío a lo pedido:

| campo | brazo | vidas | peleas que no acaban en muerte y empiezan antes del tic 12.000 | con primer golpe (definición) | mediana | media | por debajo de 100 | por debajo de 75 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| P7-10 | ESPERANZA | 80 | 100 | 100 | 100,0 | 97,3 | 21 (21 %) | 2 |
| P7-10 | BORRADO | 80 | 114 | 111 | 100,0 | 97,1 | 18 (16 %) | 2 |
| P7-10 | APRENDE | 80 | 107 | 106 | 100,0 | 97,5 | 19 (18 %) | 2 |
| P7-10 | TECHO | 80 | 97 | 97 | 100,0 | 96,3 | 24 (25 %) | 3 |
| P7-14b | ESPERANZA | 80 | 84 | 82 | 100,0 | 97,4 | 10 (12 %) | 3 |
| P7-14b | BORRADO | 80 | 103 | 103 | 100,0 | 96,5 | 15 (15 %) | 4 |
| P7-14b | APRENDE | 80 | 98 | 96 | 100,0 | 96,2 | 17 (18 %) | 6 |
| P7-14b | TECHO | 80 | 111 | 111 | 100,0 | 97,2 | 23 (21 %) | 3 |
| los dos | ESPERANZA | 160 | 184 | 182 | 100,0 | 97,3 | 31 (17 %) | 5 |
| los dos | BORRADO | 160 | 217 | 214 | 100,0 | 96,8 | 33 (15 %) | 6 |
| los dos | APRENDE | 160 | 205 | 202 | 100,0 | 96,9 | 36 (18 %) | 8 |
| los dos | TECHO | 160 | 208 | 208 | 100,0 | 96,7 | 47 (23 %) | 6 |

**¿Entra el que aprende en las peleas con menos vida que el que olvida?** En la mediana, no: la suya es 100 en todas las filas, y la del que olvida es 100 o algo menos. En la parte de peleas en que entra por debajo
de 100, la tabla de arriba da la cifra de cada brazo; las diferencias son de pocos puntos y de pocos casos.

## Sección 4 · Contra el que olvida en la misma semilla

Para cada muerte temprana con pelea final: la vida que tenía, en ese mismo tic, el BORRADO de la misma serie, el mismo día y el mismo asiento (misma
semilla), menos la vida del que murió. Solo se describe esa diferencia: **no se rehace la partida**, y la semilla fija el mapa, no lo que hacen los
rivales, así que el BORRADO de ese tic puede estar en otro sitio y en otra situación. La última columna cuenta las muertes en que el que olvida tenía
más vida y la diferencia era, al menos, lo que quitó el último golpe recibido: es lo más cerca que se puede estar de «habría cambiado» sin inventar nada.

Antes del tic 11.000:

| brazo (los dos campos) | muertes tempranas con pelea final | el que olvida ya había muerto en ese tic | el que olvida tenía MÁS vida | igual | MENOS | diferencia mediana | tenía más, y la diferencia era al menos el último golpe recibido |
|---|---:|---:|---:|---:|---:|---:|---:|
| APRENDE | 18 | 1 | 6 | 5 | 6 | 0,0 | 6 |
| TECHO | 12 | 0 | 3 | 7 | 2 | 0,0 | 3 |
| ESPERANZA | 11 | 0 | 2 | 6 | 3 | 0,0 | 2 |

Diferencias, una por muerte, del que aprende (vida del que olvida menos la suya): -61, -21, -20, -20, -8, -6, 0, 0, 0, 0, 0, 8, 14, 16, 27, 38, 50.

Antes del tic 12.000:

| brazo (los dos campos) | muertes tempranas con pelea final | el que olvida ya había muerto en ese tic | el que olvida tenía MÁS vida | igual | MENOS | diferencia mediana | tenía más, y la diferencia era al menos el último golpe recibido |
|---|---:|---:|---:|---:|---:|---:|---:|
| APRENDE | 27 | 1 | 10 | 6 | 10 | 0,0 | 9 |
| TECHO | 14 | 0 | 5 | 7 | 2 | 0,0 | 5 |
| ESPERANZA | 16 | 1 | 5 | 7 | 3 | 0,0 | 5 |

Diferencias del que aprende: -64, -61, -22, -21, -20, -20, -11, -8, -6, -5, 0, 0, 0, 0, 0, 0, 6, 8, 14, 16, 17, 27, 38, 41, 50, 58.

## Sección 5 · La tabla para Ari

Está en `tabla_P7_20_Ari.md`, en inglés, para mandarla tal cual:

**Life (HP) at the first hit — early deaths, both fields (P7-10 and P7-14b), 80 lives per arm per field**

First hit = first damage from a rival after 10 s (240 tics) with no damage of any kind; HP is the one the creature had when it received that hit (max 100).
Fatal fight = the run of damage (gaps of 10 s or less) that ends in the creature's death. n = fights with a first hit under that definition
(fights that open with ring damage, and deaths by the ring alone, have none). Read after the seals; nothing was replayed.

| field | arm | early deaths (<11,000 / <12,000 tics) | HP at first hit of the fatal fight, median (n), <11,000 | same, <12,000 | HP at first hit of non-fatal fights in those lives, median (n), <11,000 | same, <12,000 |
|---|---|---:|---:|---:|---:|---:|
| P7-10 | HOPE (no memory) | 4 / 10 | 100.0 (4) | 100.0 (6) | 100.0 (3) | 100.0 (8) |
| P7-10 | ERASED (forgets) | 3 / 9 | 100.0 (2) | 100.0 (5) | 100.0 (1) | 100.0 (7) |
| P7-10 | LEARNS | 10 / 19 | 92.0 (10) | 92.0 (15) | 100.0 (12) | 100.0 (20) |
| P7-10 | CEILING | 5 / 6 | 85.0 (4) | 85.0 (4) | 100.0 (4) | 100.0 (4) |
| P7-14b | HOPE (no memory) | 11 / 18 | 100.0 (7) | 100.0 (9) | 100.0 (4) | 100.0 (10) |
| P7-14b | ERASED (forgets) | 4 / 7 | 98.5 (4) | 100.0 (6) | 90.0 (7) | 100.0 (9) |
| P7-14b | LEARNS | 10 / 16 | 100.0 (8) | 100.0 (11) | 100.0 (1) | 100.0 (5) |
| P7-14b | CEILING | 8 / 10 | 100.0 (8) | 100.0 (9) | 100.0 (7) | 100.0 (10) |
| both | HOPE (no memory) | 15 / 28 | 100.0 (11) | 100.0 (15) | 100.0 (7) | 100.0 (18) |
| both | ERASED (forgets) | 7 / 16 | 100.0 (6) | 100.0 (11) | 95.0 (8) | 100.0 (16) |
| both | LEARNS | 20 / 35 | 100.0 (18) | 100.0 (26) | 100.0 (13) | 100.0 (25) |
| both | CEILING | 13 / 16 | 100.0 (12) | 100.0 (13) | 100.0 (11) | 100.0 (14) |

## Lo que esto dice y lo que no

- La medida de Ari (la vida al recibir el primer golpe de la pelea que mata) no separa al que aprende del que olvida: los dos entran casi siempre enteros.
- No dice nada de lo que pasa **dentro** de la pelea (cuánto tarda en usar el botiquín una vez herido), que es la otra mitad de su lectura; eso lo miraron
  P7-15 y P7-16 por otro camino. Tampoco es una prueba: son 27 y 12 peleas, sin prueba estadística, y todo es posterior a los sellos.

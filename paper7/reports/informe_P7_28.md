# P7-28 · Por qué se hunde la que recuerda

*8-oct-2026. Coste: plataforma 0, consola 0. Solo lectura de los diarios del campo de P7-24/27 y réplicas de vidas ya jugadas, una por proceso. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo, congelados y piezas de la séptima
sin tocar (ningún arreglo aplicado: lo que se propone queda propuesto). Este informe lo escribe `escribe_informe_P7_28.py` desde `P7_28_resumen.json` (`resume_P7_28.py`, que junta `P7_28_vidas.json` de
`analiza_P7_28.py`, `P7_28_curiosidad.json` de `banco_P7_28.py`, `P7_28_bloqueos*.json` de `bloqueos_P7_28.py` y los `P7_24_vidas.json` / `P7_24_resumen.json` del sello). Exclusiones: las del sello (las 8 partidas con corte de la plataforma salen de
puesto, muerte y pares; el aprendizaje de esos días cuenta hasta el corte). Lectura posterior al sello: no cambia nada de lo sellado y no se añade ningún criterio nuevo que "pase" o "no pase".*

## En corto

1. **La curiosidad no se apaga porque lo que tira no es la curiosidad.** En los días 16-20 la que recuerda elige `ir_curioso` en 7.582 de 26.900 tics con el paso listo (28 %, 15 de 16 vidas
   replicadas) con una ignorancia de 0,044–0,064 (botiquín) y 0,053–0,069 (ración): **la misma que medimos al acabar el día** (en 15 de 15 vidas la menor ignorancia con que decide está a menos de 0,005 de la del cuaderno al acabar; la mayor es la de la mañana, antes de los recuerdos del propio día; la del fin de día suma el olvido de la jornada). El 39 % del sello contaba los 20 diarios; aquí se replican 16, y una de ellas (s1 · 10 · d20, 4.399 tics listos sin un solo `ir_curioso`) pesa mucho en la fracción.
   La fila R-CURIOSIDAD vale M = 0,0053 (mediana) y el alivio que promete llegar es M × 0,5 = 0,0027: nada. Lo que gana es **el candidato** que la curiosidad abre: `ir_curioso` es "ir a por la cosa" con la cosa imaginada en el zurrón al llegar (`descubre_P7.py:299-303`, decisión 2 de P7-7:
   "el mismo candidato de ir a por la cosa que generan las ganas"), valorado por el cuerpo con las ganas aprendidas (k botiquín 0,34, k ración 1,01, medianas), y se crea **siempre** que la clase que más llama no vaya en el zurrón, por pequeña que sea la llamada (`nace_P7_23.py:211`: `v > 0`). Su destino es el sitio recordado más cercano por camino (`nace_P7_23.py:216-226`);
   `ir_objeto` va al objeto de más valor/(1+distancia) (`decisor_zs.py:684-698`), que suele estar más lejos. Así, `ir_curioso` gana a `ir_objeto` por 0,196 de d y a `noop` por 0,395 (medianas). Es un fallo de construcción: la fila se apaga con la ignorancia, el candidato no. Y el diario enseña lo que la réplica no mide: en los días 16-20 el 39 % de los tics con el paso listo de APRENDE acaban en `action_result` = blocked (días 1-5: 8 %; BORRADO 5 %; TECHO 8 %), 6.610 de ellos eligiendo `ir_curioso` hacia un sitio recordado a 8-21 casillas, contra un muro que el cuerpo no tiene en su mapa, con rachas de hasta 2.170 tics en la misma casilla. Propuestas en la sección 1, sin aplicar.
2. **La creencia no se corrige: la bajan los cortes.** Las cuatro criaturas acaban el día 20 creyendo que el botiquín cura s1 · 10: 15,9 · s1 · 11: 9,5 · s2 · 10: 17,6 · s2 · 11: 17,6 (de 50), con ignorancia 0,053 · 0,060 · 0,070 · 0,056. El máximo de todo el campo es 29,9. En las 80 vidas de APRENDE hay 101 canales abiertos y 33 completados: 62 cortes, 26 "al menos", 7 firmes.
   Un corte se apunta como efecto 0 en el cuerpo (`nace_P7_23.py:104`) y entra en la media de la creencia con su peso (`cuaderno_P7.py:94-96`) y en la ignorancia como experiencia vivida: cada corte dice "el botiquín no hizo nada" y la ignorancia baja igual. Las 4 bajadas de 3 o más puntos de un día al siguiente coinciden con cortes; las 6 subidas, con usos firmes o "al menos". En los días 16-20 la que recuerda abre 5 canales en 20 vidas (1 con vida < 50): no se cura porque no llega herida a la pelea que la mata (punto 3).
3. **El puesto se pierde muriendo antes, en pelea, con la vida entera.** Días 16-20, pares sin corte: APRENDE muere 5.173 ± 1.641 tics antes que TECHO (n = 10) y 2.899 ± 1.242 antes que BORRADO (n = 12); en los días 1-5 eran 2.875 ± 1.171 y 799 ± 750.
   De las 14 muertes de APRENDE en los días 16-20, 9 son por rival (TECHO: 2 de 13; BORRADO: 6 de 17), con una vida de 100 (mediana) en el primer golpe de la pelea final: entra sana y pierde. Llevaba botiquín en ese golpe 3 de 9 veces y lo usó 1. TECHO muere por el anillo, tarde, cerca del centro: está quieta (44 % de sus tics con el paso listo en `noop`, a 4,3 casillas del centro de media) y APRENDE anda (37 % en `ir_curioso` y 28 % en `ir_objeto`, a 9,0 casillas). Las que no llevan botiquín no mueren más: en los tres brazos la fracción de tics con botiquín de las muertas y de las vivas es parecida (tabla 3c).
4. **Las dos series van en la misma dirección en APRENDE − TECHO** (crece 4,1 en la serie 1 y 5,3 en la 2), con TECHO mejorando en las dos (6,8 ± 1,6 → 4,6 ± 0,7; 6,8 ± 1,2 → 4,2 ± 0,8) y APRENDE empeorando en las dos. BORRADO − TECHO y APRENDE − BORRADO cambian de signo entre series: con 6-10 pares por celda no se puede decir que crezcan.
5. **Conclusión:** la que recuerda no se hunde por lo que cree del botiquín (lo usa poco y tarde en los tres brazos) sino por lo que hace con el día: un candidato de "ir a por lo recordado" que la curiosidad dejó abierto y que las ganas aprendidas valoran como si fuera deseo, la tiene andando por el mapa (o empujando un muro) 64 % de los tics con el paso listo y la mete en peleas con la vida entera a media partida. El techo no anda (44 % en `noop`); la borrada anda menos (17 %) y más cerca del centro. Lo que habría que cambiar está propuesto en la sección 1; nada se ha tocado.

## Sección 1 · La curiosidad que no se apaga (punto 1)

**Qué se midió.** Réplica de las vidas de APRENDE de los días 16-20 (`banco_P7_28.py`, molde de `banco_P7_25`, una vida por proceso, la pieza de nacer encendida y el cuaderno que leyó ese día). 16 de las 20 vidas se replican con fidelidad exacta salvo 3 tics de 126.420; las otras 4 (s1 d20 asiento 11, s2 d18 los dos, s2 d20 asiento 10) son
los diarios parciales rescatados del registro de salida en P7-27: no traen el `player_config` y la réplica no arranca (`mide_P6_29.config_de`). En cada tic con el paso listo en que el cuerpo elige `ir_curioso` se apunta lo que el cuerpo tiene delante al decidir: la ignorancia de cada clase (`cuaderno.ignorancia`, la del cuaderno vivo), el alivio, la M de R-CURIOSIDAD, el destino (casilla, clase, distancia, dentro o fuera del círculo, si está a la vista o es solo recuerdo), k de las dos clases, zurrón, y las d de los candidatos que compiten; después, del diario, si llega a esa casilla, si coge y si usa en los 240 tics siguientes.

| serie · asiento · día | tics · fidelidad | paso listo | `ir_curioso` gana | ignorancia botiquín al decidir (mín–máx) · al acabar | ignorancia ración al decidir · al acabar | clase del destino | dentro · fuera | llega · coge · usa (240 tics) | d mediana: `ir_curioso` · `ir_objeto` · `noop` |
|---|---|---:|---:|---|---|---|---|---|---|
| s1 · 10 · d16 | 2.967 · exacta | 396 | 118 (30 %) | 0,044–0,047 · 0,046 | 0,063–0,069 · 0,067 | rations 13, first_aid 105 | 118 · 0 | 49 · 19 · 18 | 3,16 · 3,82 · 3,67 |
| s1 · 11 · d16 | 11.136 · exacta | 1.514 | 637 (42 %) | 0,047–0,053 · 0,049 | 0,053–0,056 · 0,056 | rations 339, first_aid 298 | 632 · 5 | 494 · 45 · 0 | 3,32 · 3,43 · 3,58 |
| s1 · 10 · d17 | 11.568 · exacta | 1.593 | 1.379 (87 %) | 0,046–0,046 · 0,048 | 0,053–0,067 · 0,055 | rations 1285, first_aid 94 | 1371 · 8 | 1145 · 71 · 17 | 3,26 · 3,44 · 3,63 |
| s1 · 11 · d17 | 11.592 · exacta | 1.650 | 82 (5 %) | 0,049–0,049 · 0,052 | 0,056–0,056 · 0,059 | rations 72, first_aid 10 | 64 · 18 | 77 · 17 · 0 | 2,77 · 2,74 · 3,07 |
| s1 · 10 · d18 | 7.169 · exacta | 1.158 | 439 (38 %) | 0,046–0,048 · 0,048 | 0,055–0,055 · 0,058 | first_aid 8, rations 431 | 439 · 0 | 8 · 8 · 16 | 2,95 · 3,90 · 3,37 |
| s1 · 11 · d18 | 7.390 · exacta | 1.136 | 731 (64 %) | 0,052–0,052 · 0,054 | 0,059–0,059 · 0,062 | rations 731 | 702 · 29 | 296 · 0 · 0 | 3,22 · 3,44 · 3,58 |
| s1 · 10 · d19 | 961 · exacta | 361 | 9 (2 %) | 0,048–0,048 · 0,050 | 0,058–0,058 · 0,061 | rations 5, first_aid 4 | 9 · 0 | 9 · 9 · 0 | 3,21 · 3,33 · 3,65 |
| s1 · 11 · d19 | 10.920 · exacta | 1.701 | 548 (32 %) | 0,054–0,054 · 0,057 | 0,055–0,062 · 0,058 | rations 21, first_aid 527 | 548 · 0 | 57 · 21 · 0 | 3,67 · 3,42 · 3,77 |
| s1 · 10 · d20 | 11.064 · exacta | 4.399 | 0 (0 %) | — · 0,053 | — · 0,064 | — | 0 · 0 | 0 · 0 · 0 | — · — · — |
| s2 · 10 · d16 | 12.312 · exacta | 1.212 | 1.008 (83 %) | 0,055–0,061 · 0,058 | 0,063–0,063 · 0,066 | rations 993, first_aid 15 | 991 · 17 | 918 · 173 · 4 | 3,00 · 3,19 · 3,42 |
| s2 · 11 · d16 | 12.648 · exacta | 2.328 | 50 (2 %) | 0,046–0,046 · 0,048 | 0,053–0,065 · 0,056 | rations 50 | 42 · 8 | 35 · 14 · 0 | 4,28 · 4,58 · 4,75 |
| s2 · 10 · d17 | 5.236 · exacta | 1.029 | 199 (19 %) | 0,058–0,058 · 0,061 | 0,066–0,066 · 0,069 | rations 12, first_aid 187 | 199 · 0 | 57 · 12 · 0 | 3,15 · 3,08 · 3,42 |
| s2 · 11 · d17 | 7.137 · 3 tics difieren | 5.097 | 2.208 (43 %) | 0,048–0,048 · 0,051 | 0,056–0,056 · 0,059 | rations 2208 | 2208 · 0 | 0 · 0 · 0 | 2,78 · 2,97 · 3,39 |
| s2 · 10 · d19 | 1.720 · exacta | 161 | 15 (9 %) | 0,064–0,064 · 0,067 | 0,062–0,062 · 0,066 | first_aid 4, rations 11 | 15 · 0 | 9 · 4 · 0 | 3,02 · 3,26 · 3,44 |
| s2 · 11 · d19 | 1.920 · exacta | 246 | 141 (57 %) | 0,050–0,050 · 0,053 | 0,058–0,058 · 0,060 | rations 7, first_aid 134 | 141 · 0 | 66 · 7 · 0 | 3,05 · 3,06 · 3,30 |
| s2 · 11 · d20 | 10.680 · exacta | 2.919 | 18 (1 %) | 0,053–0,053 · 0,056 | 0,060–0,060 · 0,064 | rations 17, first_aid 1 | 18 · 0 | 18 · 18 · 0 | 2,46 · 2,73 · 2,90 |

**La ignorancia que usa al decidir es la que medimos al final del día.** En las 15 vidas con algún `ir_curioso`, la menor ignorancia con que decide (la de la tarde, con los recuerdos del propio día ya escritos) está a menos de 0,005 de la del cuaderno al acabar en 15 vidas; la mayor es la de la mañana. La del final es un poco mayor que la última de la tarde por el olvido de la jornada (OLVIDO = 0,95 por día, `cuaderno_P7.py:62`). No hay dos ignorancias: el cuerpo decide con la que medimos.

**Lo que tira.** De los 7.582 tics en que gana `ir_curioso`: destino de clase rations 6195, first_aid 1387; dentro del círculo 7.497; a la vista 2.468 (el resto, recuerdo de `mem.objetos_vistos`); distancia mediana 3 casillas; con botiquín ya en el zurrón 1.475, con ración 1.383 (el candidato se crea para la clase que falta). Agrupando los tics seguidos hacia el mismo destino: 1.924 episodios, de los que llega a la casilla o coge algo en los 240 tics siguientes 1.502 y usa 9. Las d (menor gana): `ir_curioso` 3,097, `ir_objeto` 3,174, `ir_botin` 3,329, `ir_centro` 3,386, `noop` 3,467 (medianas). M de R-CURIOSIDAD mediana 0,0053: su alivio imaginado, M × (1 − 0,5) = 0,0027, no explica una diferencia de 0,395 sobre `noop`. La explica la foto de la llegada con la cosa en el zurrón: ganas R-ACOPIO × k, riqueza W × k, W_TARGET = 1 + k + k (`descubre_P7.py:344`, `nace_P7_23.py:189`), lo mismo que valora `ir_objeto`, pero con un destino más cercano.

**Lo que la réplica no mide y el diario sí: el paso bloqueado.** El diario apunta en cada tic `action_result`; "blocked" es un paso pedido que el mundo no dio. Contados con el paso listo:

| brazo · bloque | vidas | tics con el paso listo | bloqueados | de ellos eligiendo `ir_curioso` · `ir_objeto` · `noop` (bloqueados / elegidos) | vidas con una racha bloqueada de 200 tics o más |
|---|---:|---:|---|---|---:|
| APRENDE días 1-5 | 20 | 41.039 | 3.342 (8 %) | 1.057 / 7.379 · 472 / 4.737 · 8 / 13.158 | 3 |
| APRENDE días 16-20 | 20 | 33.131 | 12.935 (39 %) | 6.610 / 12.096 · 4.709 / 9.227 · 128 / 2.493 | 6 |
| BORRADO días 1-5 | 20 | 24.350 | 1.039 (4 %) | 81 / 1.322 · 16 / 4.344 · 2 / 5.183 | 1 |
| BORRADO días 16-20 | 20 | 43.085 | 2.117 (5 %) | 14 / 2.638 · 6 / 4.511 · 13 / 22.614 | 1 |
| TECHO días 1-5 | 20 | 75.635 | 10.681 (14 %) | 0 / 0 · 1.451 / 8.147 · 22 / 45.469 | 7 |
| TECHO días 16-20 | 20 | 61.681 | 4.681 (8 %) | 0 / 0 · 140 / 5.032 · 2 / 27.367 | 4 |

En APRENDE, días 16-20, 6 vidas tienen una racha de 200 tics o más sin moverse mientras eligen ir a algún sitio:

| vida (APRENDE, días 16-20) | tics listos | bloqueados | racha máxima bloqueada | partida con corte |
|---|---:|---:|---:|---|
| s1 · d19 · 10 | 361 | 271 (75 %) | 271 | no |
| s1 · d20 · 11 | 1.062 | 1.062 (100 %) | 1.062 | sí |
| s2 · d16 · 11 | 2.328 | 773 (33 %) | 713 | no |
| s2 · d17 · 11 | 5.097 | 4.627 (91 %) | 2.170 | no |
| s2 · d18 · 11 | 2.549 | 2.536 (99 %) | 1.301 | sí |
| s2 · d20 · 10 | 2.348 | 2.317 (99 %) | 1.528 | sí |

Ejemplo (s2 · d17 · asiento 11, la réplica y el diario coinciden): en la casilla (46, 15), con el paso listo y la vida a 100, elige `ir_curioso` hacia una ración recordada en (25, 15) (no a la vista, a 21 casillas) y pide `move W` 974 tics seguidos; el mundo responde blocked cada vez. El arreglo del paso 0 de P7-24 exigía un camino según la geodésica del propio cuerpo (`nace_P7_23.py:220-226`), y la geodésica lo da: el muro no está en el mapa del cuerpo, y el cuerpo congelado no lee `action_result`. El candidato apunta siempre al mismo sitio porque el sitio sigue en `mem.objetos_vistos` y es el más cercano por camino (`nace_P7_23.py:226`). Lo mismo le pasa a `ir_objeto` (4.709 bloqueados de 9.227): es una limitación del cuerpo, que la pieza de la séptima multiplica al darle un segundo candidato de ir a por cosas recordadas. 3 de las 6 vidas atascadas están en partidas que la plataforma cortó (P7-27), y por eso no entran en puesto ni en muertes; no se puede saber desde aquí si el atasco tiene que ver con el corte.

**Dónde está el fallo, con archivo y línea.**
- `nace_P7_23.py:206-229` (`_cands`): el candidato `ir_curioso` se crea para la clase con mayor ignorancia × alivio siempre que esa llamada sea `> 0` (línea 211), no vaya en el zurrón y quepa. Con ignorancia 0,05 la llamada es 0,05 > 0: el candidato existe igual que el día 1.
- `descubre_P7.py:299-303 y 318` (decisión 2 de P7-7): el candidato es del tipo `ir` con `recoger`, "el mismo candidato que generan las ganas": la imaginación pone la cosa en el zurrón al llegar y el cuerpo lo valora con las ganas aprendidas. La única parte que depende de la ignorancia es el alivio de la fila (`descubre_P7.py:358-369`, `nace_P7_23.py:242-251`): M × 0,5, cuatro milésimas.
- `cuaderno_P7.py:64-66`: la ignorancia es peso del neutro / (neutro + pesos vividos). Con 20-30 recuerdos vale 0,05 y ya no cambia nada de lo anterior. Esto no es un fallo (mide lo que se diseñó: cuánto se ha vivido), pero conviene saber que no mide cuánto se sabe (sección 2).
- Por diseño, TECHO no tiene este candidato (`NOVEDAD_ON and not SABE`, `descubre_P7.py:298`) y está quieta el 44 % de los tics con el paso listo; BORRADO lo tiene cada día con ignorancia 1 al empezar (ahí sí es curiosidad).

**Propuestas (sin aplicar; decisión de la mesa).** (1) Que el candidato dure lo que dura la fila: crear `ir_curioso` solo mientras la clase sigue sin recuerdo firme en el cuaderno (la definición de "no sabe" que ya usa el sello: E1, "firme de las dos"), y que desde el primer recuerdo firme sean las ganas (`ir_objeto`, `coger`) las que decidan si va a por la cosa, como en el cuerpo de siempre. Ningún número nuevo. Variante más fina, si la mesa prefiere continuidad: que la promesa de `ir_curioso` sea solo el alivio de la fila (llegar sin imaginar la cosa en el zurrón), con lo que se apaga sola con la ignorancia; pero entonces el día 1 tampoco va a por lo nuevo (P7-25 midió que es la foto de la llegada, no la fila, lo que mueve el paso). Lo que cabe esperar de la primera: en los días 16-20 desaparecen los 7.582 tics de `ir_curioso` y el cuerpo cae a `noop` / `ir_objeto` / `ir_centro`; no se puede prever el puesto sin jugar. (2) Para el atasco: que un sitio hacia el que el paso lleva bloqueado un tiempo deje de ser destino (sale de `mem.objetos_vistos` o entra en `cedidos`, que ya excluye sitios: `nace_P7_23.py:219`); el umbral sería un número nuevo y lo fija la mesa; sin él, la que recuerda seguirá pegada a los muros con cualquier arreglo de (1). Lo que no se puede hacer: cambiar el campo sellado.

## Sección 2 · La creencia que se corrige, o no (punto 2)

**Por bloques y brazo** (las 240 vidas, sin excluir: lo que se lleva y se usa no depende del corte; TECHO sin cuaderno, sus usos son los canales del diario, P7-21):

| brazo · bloque | vidas | botiquines llevados (media por tic) · tics con botiquín | raciones llevadas (media) | botiquines cogidos | canales abiertos · completados | vida al abrir (mediana) | aperturas con vida < 50 | huellas: firmes · al menos · cortes |
|---|---:|---|---:|---:|---|---:|---|---|
| APRENDE · días 1-5 | 20 | 0,31 · 31 % | 0,92 | 13 | 27 · 7 | 60 | 9 (4 vidas) | 2 · 5 · 20 |
| APRENDE · días 6-10 | 20 | 0,64 · 61 % | 1,18 | 23 | 40 · 11 | 49 | 20 (9 vidas) | 4 · 7 · 25 |
| APRENDE · días 11-15 | 20 | 0,46 · 41 % | 1,13 | 19 | 29 · 12 | 75 | 9 (6 vidas) | 1 · 11 · 15 |
| APRENDE · días 16-20 | 20 | 0,43 · 36 % | 0,80 | 12 | 5 · 3 | 80 | 1 (1 vidas) | 0 · 3 · 2 |
| BORRADO · días 1-5 | 19 | 0,54 · 42 % | 0,38 | 26 | 40 · 20 | 86 | 8 (4 vidas) | 1 · 17 · 19 |
| BORRADO · días 6-10 | 19 | 0,41 · 35 % | 0,35 | 20 | 26 · 17 | 83 | 5 (2 vidas) | 2 · 15 · 9 |
| BORRADO · días 11-15 | 20 | 0,45 · 37 % | 0,47 | 25 | 28 · 17 | 84 | 9 (5 vidas) | 3 · 14 · 9 |
| BORRADO · días 16-20 | 20 | 0,50 · 43 % | 0,40 | 22 | 59 · 17 | 76 | 13 (4 vidas) | 2 · 15 · 41 |
| TECHO · días 1-5 | 20 | 0,63 · 56 % | 0,62 | 41 | 55 · 18 | 55 | 25 (10 vidas) | — (sin cuaderno) |
| TECHO · días 6-10 | 19 | 0,68 · 52 % | 0,98 | 31 | 54 · 16 | 58 | 22 (9 vidas) | — (sin cuaderno) |
| TECHO · días 11-15 | 20 | 0,53 · 52 % | 1,08 | 22 | 37 · 15 | 60 | 10 (7 vidas) | — (sin cuaderno) |
| TECHO · días 16-20 | 19 | 0,74 · 66 % | 0,54 | 52 | 73 · 19 | 55 | 32 (10 vidas) | — (sin cuaderno) |

Lectura. (i) La que recuerda lleva botiquín menos tiempo que el techo (31 → 36 % de los tics frente a 56 → 66 %) y lo abre mucho menos: 101 canales en 80 vidas frente a 219 del techo y 153 de la borrada; de los suyos completa 33. (ii) En los días 16-20 casi no lo abre: 5 canales, 1 con vida < 50, ningún firme; el techo abre 73 y 32 con vida < 50. (iii) La vida al abrir baja en el techo (mediana 55) y en la que recuerda es 80 en el último bloque: E6 pasó por los días 11-15, no por los 16-20. (iv) Hay días en que la que recuerda se cura herida (vida < 50): 20 vidas de 80, casi todas en los días 1-15 (lista en la tabla por día).

**Por criatura y día** (APRENDE; creencia y la ignorancia del cuaderno al acabar el día; "parcial" = partida con corte, aprendizaje hasta el corte):

| serie · asiento | día | creencia botiquín dentro · fuera | ignorancia | botiquines llevados (media) | cogidos | canales · completados | vida al abrir | aperturas con vida < 50 | firmes · al menos · cortes | puesto |
|---|---:|---|---:|---:|---:|---|---|---:|---|---:|
| s1 · 10 | 1 | — · — | 1,000 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 8 |
| s1 · 10 | 2 | 9,4 · — | 0,176 | 0,26 | 1 | 3 · 1 | 86, 47, 34 | 2 | 1 · 0 · 2 | 16 |
| s1 · 10 | 3 | 9,3 · — | 0,184 | 0,05 | 2 | 1 · 1 | 60 | 0 | 0 · 1 · 0 | 2 |
| s1 · 10 | 4 | 9,2 · — | 0,192 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 15 |
| s1 · 10 | 5 | 9,1 · 0,0 | 0,126 | 0,98 | 1 | 2 · 0 | 36, 26 | 2 | 0 · 0 · 2 | 11 |
| s1 · 10 | 6 | 9,0 · 0,0 | 0,099 | 1,55 | 2 | 3 · 0 | 80, 40, 1 | 2 | 0 · 0 · 2 | 2 |
| s1 · 10 | 7 | 8,9 · 0,0 | 0,068 | 0,61 | 1 | 6 · 0 | 50, 40, 31, 21, 11, 1 | 5 | 0 · 0 · 5 | 10 |
| s1 · 10 | 8 | 16,3 · 0,0 | 0,060 | 0,43 | 2 | 2 · 2 | 75, 67 | 0 | 0 · 2 · 0 | 8 |
| s1 · 10 | 9 | 18,0 · 0,0 | 0,055 | 0,74 | 1 | 2 · 1 | 81, 55 | 0 | 0 · 1 · 1 | 5 |
| s1 · 10 | 10 | 22,3 · 0,0 | 0,050 | 0,01 | 2 | 2 · 2 | 86, 48 | 1 | 1 · 1 · 0 | 5 |
| s1 · 10 | 11 | 22,1 · 0,0 | 0,048 | 0,92 | 1 | 1 · 1 | 78 | 0 | 0 · 1 · 0 | 3 |
| s1 · 10 | 12 | 22,0 · 0,0 | 0,051 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 14 |
| s1 · 10 | 13 | 21,9 · 0,0 | 0,053 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 4 |
| s1 · 10 | 14 | 16,3 · 0,0 | 0,047 | 0,29 | 1 | 3 · 0 | 71, 50, 28 | 1 | 0 · 0 · 3 | 16 |
| s1 · 10 | 15 | 17,2 · 0,0 | 0,046 | 0,51 | 1 | 1 · 1 | 72 | 0 | 0 · 1 · 0 | 7 |
| s1 · 10 | 16 | 17,4 · 0,0 | 0,046 | 0,56 | 1 | 1 · 1 | 80 | 0 | 0 · 1 · 0 | 15 |
| s1 · 10 | 17 | 17,3 · 0,0 | 0,048 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 9 |
| s1 · 10 | 18 | 16,0 · 0,0 | 0,048 | 0,93 | 1 | 1 · 0 | 14 | 1 | 0 · 0 · 1 | 15 |
| s1 · 10 | 19 | 15,9 · 0,0 | 0,050 | 0,81 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 16 |
| s1 · 10 | 20 | 15,9 · 0,0 | 0,053 | 1,99 | 2 | 0 · 0 | — | 0 | 0 · 0 · 0 | 13 |
| s1 · 11 | 1 | 8,7 · — | 0,225 | 0,73 | 1 | 3 · 1 | 89, 78, 67 | 0 | 0 · 1 · 2 | 4 |
| s1 · 11 | 2 | 8,6 · — | 0,234 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 15 |
| s1 · 11 | 3 | 8,5 · — | 0,243 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 1 |
| s1 · 11 | 4 | 4,6 · — | 0,140 | 0,77 | 1 | 3 · 0 | 86, 60, 34 | 1 | 0 · 0 · 3 | 16 |
| s1 · 11 | 5 | 4,6 · — | 0,146 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 12 |
| s1 · 11 | 6 | 2,1 · 0,0 | 0,065 | 1,02 | 2 | 9 · 0 | 85, 98, 94, 83, 72, 61, 50, 45, 5 | 2 | 0 · 0 · 8 | 3 |
| s1 · 11 | 7 | 2,4 · 0,0 | 0,064 | 0,77 | 1 | 1 · 1 | 94 | 0 | 0 · 1 · 0 | 5 |
| s1 · 11 | 8 | 2,5 · 0,0 | 0,063 | 0,68 | 1 | 1 · 1 | 95 | 0 | 0 · 1 · 0 | 5 |
| s1 · 11 | 9 | 2,5 · 0,0 | 0,066 | 0,98 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 16 |
| s1 · 11 | 10 | 6,9 · 0,0 | 0,059 | 0,86 | 2 | 2 · 1 | 25, 18 | 2 | 1 · 0 · 1 | 6 |
| s1 · 11 | 11 | 6,9 · 0,0 | 0,062 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 14 |
| s1 · 11 | 12 (parcial) | 6,9 · 0,0 | 0,065 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | — |
| s1 · 11 | 13 | 8,3 · 0,0 | 0,059 | 0,28 | 3 | 2 · 2 | 92, 76 | 0 | 0 · 2 · 0 | 3 |
| s1 · 11 | 14 | 8,3 · 0,0 | 0,062 | 0,96 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 15 |
| s1 · 11 | 15 | 8,3 · 0,0 | 0,053 | 1,30 | 2 | 3 · 2 | 94, 89, 78 | 0 | 0 · 2 · 1 | 9 |
| s1 · 11 | 16 | 9,6 · 0,0 | 0,049 | 0,27 | 1 | 2 · 1 | 86, 62 | 0 | 0 · 1 · 1 | 10 |
| s1 · 11 | 17 | 9,6 · 0,0 | 0,052 | 1,24 | 2 | 0 · 0 | — | 0 | 0 · 0 · 0 | 8 |
| s1 · 11 | 18 | 9,5 · 0,0 | 0,054 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 14 |
| s1 · 11 | 19 | 9,5 · 0,0 | 0,057 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 11 |
| s1 · 11 | 20 (parcial) | 9,5 · 0,0 | 0,060 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | — |
| s2 · 10 | 1 | 24,1 · 0,0 | 0,081 | 0,88 | 2 | 10 · 2 | 93, 86, 73, 60, 54, 40, 27, 14, 1, 66 | 4 | 1 · 1 · 8 | 1 |
| s2 · 10 | 2 | 23,9 · 0,0 | 0,084 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 13 |
| s2 · 10 | 3 | 23,6 · 0,0 | 0,088 | 0,99 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 3 |
| s2 · 10 | 4 | 23,3 · 0,0 | 0,093 | 0,98 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 14 |
| s2 · 10 | 5 | 22,1 · 0,0 | 0,082 | 0,09 | 1 | 1 · 1 | 80 | 0 | 0 · 1 · 0 | 2 |
| s2 · 10 | 6 | 21,9 · 0,0 | 0,062 | 0,84 | 2 | 3 · 1 | 92, 74, 35 | 1 | 0 · 1 · 2 | 7 |
| s2 · 10 | 7 | 21,7 · 0,0 | 0,065 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 15 |
| s2 · 10 | 8 | 21,5 · 0,0 | 0,068 | 0,59 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 11 |
| s2 · 10 | 9 | 29,9 · 0,0 | 0,065 | 0,01 | 1 | 1 · 1 | 8 | 1 | 1 · 0 · 0 | 14 |
| s2 · 10 | 10 | 29,6 · 0,0 | 0,068 | 0,99 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 13 |
| s2 · 10 | 11 | 29,3 · 0,0 | 0,062 | 0,96 | 2 | 2 · 2 | 95, 80 | 0 | 0 · 2 · 0 | 4 |
| s2 · 10 | 12 | 28,9 · 0,0 | 0,065 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 5 |
| s2 · 10 | 13 | 28,6 · 0,0 | 0,064 | 0,83 | 1 | 1 · 0 | 40 | 1 | 0 · 0 · 1 | 8 |
| s2 · 10 | 14 | 28,2 · 0,0 | 0,067 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 5 |
| s2 · 10 | 15 | 18,3 · 0,0 | 0,061 | 0,08 | 1 | 2 · 0 | 80, 40 | 1 | 0 · 0 · 2 | 11 |
| s2 · 10 | 16 | 18,1 · 0,0 | 0,058 | 1,16 | 2 | 1 · 1 | 92 | 0 | 0 · 1 · 0 | 5 |
| s2 · 10 | 17 | 18,0 · 0,0 | 0,061 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 15 |
| s2 · 10 | 18 (parcial) | 17,9 · 0,0 | 0,064 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | — |
| s2 · 10 | 19 | 17,8 · 0,0 | 0,067 | 0,92 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 16 |
| s2 · 10 | 20 (parcial) | 17,6 · 0,0 | 0,070 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | — |
| s2 · 11 | 1 | — · 2,0 | 0,498 | 0,22 | 1 | 1 · 1 | 96 | 0 | 0 · 1 · 0 | 13 |
| s2 · 11 | 2 | — · 0,7 | 0,181 | 0,28 | 1 | 3 · 0 | 93, 57, 50 | 0 | 0 · 0 · 3 | 14 |
| s2 · 11 | 3 | — · 0,7 | 0,189 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 1 |
| s2 · 11 | 4 | — · 0,7 | 0,197 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 4 |
| s2 · 11 | 5 | — · 0,7 | 0,205 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 7 |
| s2 · 11 | 6 | 21,3 · 0,7 | 0,134 | 0,83 | 1 | 2 · 1 | 25, 1 | 2 | 1 · 0 · 1 | 6 |
| s2 · 11 | 7 | 21,0 · 0,7 | 0,140 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 16 |
| s2 · 11 | 8 | 20,7 · 0,7 | 0,146 | 0,98 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 13 |
| s2 · 11 | 9 | 12,1 · 0,4 | 0,081 | 0,99 | 1 | 6 · 0 | 80, 73, 40, 27, 14, 1 | 4 | 0 · 0 · 5 | 4 |
| s2 · 11 | 10 | 12,0 · 0,3 | 0,085 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 14 |
| s2 · 11 | 11 | 15,5 · 0,3 | 0,081 | 0,26 | 1 | 1 · 1 | 68 | 0 | 0 · 1 · 0 | 3 |
| s2 · 11 | 12 | 15,4 · 0,3 | 0,072 | 0,01 | 1 | 3 · 0 | 29, 16, 3 | 3 | 0 · 0 · 2 | 7 |
| s2 · 11 | 13 | 21,4 · 0,2 | 0,046 | 1,31 | 2 | 7 · 2 | 95, 85, 75, 65, 45, 39, 89 | 2 | 1 · 1 · 5 | 4 |
| s2 · 11 | 14 | 21,0 · 0,2 | 0,046 | 0,54 | 1 | 1 · 1 | 80 | 0 | 0 · 1 · 0 | 3 |
| s2 · 11 | 15 | 18,2 · 0,2 | 0,046 | 0,93 | 1 | 2 · 0 | 75, 16 | 1 | 0 · 0 · 1 | 13 |
| s2 · 11 | 16 | 18,1 · 0,2 | 0,048 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 3 |
| s2 · 11 | 17 | 18,0 · 0,2 | 0,051 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 14 |
| s2 · 11 | 18 (parcial) | 17,8 · 0,2 | 0,050 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | — |
| s2 · 11 | 19 | 17,7 · 0,2 | 0,053 | 0,00 | 0 | 0 · 0 | — | 0 | 0 · 0 · 0 | 15 |
| s2 · 11 | 20 | 17,6 · 0,2 | 0,056 | 0,82 | 1 | 0 · 0 | — | 0 | 0 · 0 · 0 | 12 |

Lectura. La creencia sube a saltos con los usos firmes o "al menos" (6 subidas de 3 o más: s1·10 d7→8 8,9→16,3, s1·10 d9→10 18,0→22,3, s1·11 d9→10 2,5→6,9, s2·10 d8→9 21,5→29,9, s2·11 d10→11 12,0→15,5, s2·11 d12→13 15,4→21,4) y baja a saltos con los cortes (4: s1·10 d13→14 21,9→16,3 (3 cortes), s1·11 d3→4 8,5→4,6 (3 cortes), s2·10 d14→15 28,2→18,3 (2 cortes), s2·11 d8→9 20,7→12,1 (5 cortes)); entre medias cae despacio por el olvido frente al neutro. Un corte se apunta con efecto 0 en el cuerpo (`nace_P7_23.py:104`, decisión declarada en P7-23: "el daño que lo corta va a su causa") y la media de la creencia lo cuenta con su peso (`cuaderno_P7.py:94-96`): un botiquín que no llegó a actuar vale como un botiquín que no cura. Con 62 cortes por 7 firmes, la creencia no puede llegar a 50. **Propuesta, sin aplicar:** que el corte no entre en la media del efecto del cuerpo (que cuente como "no se sabe", es decir, ni en la creencia ni en la ignorancia), como ya se hace con los "al menos" que están por debajo de la creencia firme (`cuaderno_P7.py:97-100`). Es un cambio de la pieza de P7-23, no del cuerpo.

## Sección 3 · Dónde se pierde el puesto (punto 3)

**3a · Las muertes por brazo y bloque** (sin las partidas con corte; causa según P7-21: anillo si en la racha final el anillo hizo más daño que los rivales; primer golpe de la pelea final según P7-20):

| brazo · bloque | vidas (sin corte) | muertas · sobreviven | causa: anillo · rival | tic de muerte (mediana) | peleas finales con golpe de rival | vida en el primer golpe (mediana) | llevaba botiquín en ese golpe · lo usó después | llevaba botiquín al morir | puesto medio |
|---|---:|---|---|---:|---:|---:|---|---:|---:|
| APRENDE · días 1-5 | 20 | 15 · 5 | 9 · 6 | 11.424 | 7 | 95 | 2 · 1 | 4 | 8,60 |
| APRENDE · días 16-20 | 14 | 14 · 0 | 5 · 9 | 7.760 | 9 | 100 | 3 · 1 | 4 | 11,86 |
| BORRADO · días 1-5 | 18 | 16 · 2 | 8 · 8 | 11.592 | 10 | 88 | 2 · 1 | 2 | 8,44 |
| BORRADO · días 16-20 | 20 | 17 · 3 | 11 · 6 | 12.215 | 9 | 82 | 3 · 3 | 4 | 7,35 |
| TECHO · días 1-5 | 20 | 15 · 5 | 8 · 7 | 12.552 | 9 | 79 | 1 · 1 | 2 | 6,80 |
| TECHO · días 16-20 | 18 | 13 · 5 | 11 · 2 | 12.912 | 3 | 46 | 0 · 0 | 5 | 4,39 |

**3b · Emparejadas por semilla, día y asiento** (A − B; puesto: positivo = A peor; tic de muerte: negativo = A muere antes):

| par · bloque | pares | puesto (A − B, media ± ee) | peor · igual · mejor | tic de muerte (A − B, cuando mueren las dos) | causas cruzadas (A/B) |
|---|---:|---|---|---|---|
| APRENDE - TECHO · días 1-5 | 20 | 1,8 ± 1,3 | 11 · 5 · 4 | -2.875,4 ± 1.170,5 (n = 13) | anillo/anillo 5, anillo/rival 3, anillo/vive 1, rival/anillo 2, rival/rival 3, rival/vive 1, vive/anillo 1, vive/rival 1, vive/vive 3 |
| APRENDE - TECHO · días 16-20 | 12 | 6,5 ± 1,5 | 10 · 0 · 2 | -5.172,7 ± 1.640,7 (n = 10) | anillo/anillo 2, anillo/rival 2, anillo/vive 1, rival/anillo 6, rival/vive 1 |
| APRENDE - BORRADO · días 1-5 | 18 | 0,9 ± 1,4 | 8 · 1 · 9 | 799,0 ± 750,3 (n = 13) | anillo/anillo 5, anillo/rival 4, rival/anillo 1, rival/rival 3, rival/vive 2, vive/anillo 2, vive/rival 1 |
| APRENDE - BORRADO · días 16-20 | 14 | 4,0 ± 1,5 | 9 · 1 · 4 | -2.898,7 ± 1.242,1 (n = 12) | anillo/anillo 2, anillo/rival 2, anillo/vive 1, rival/anillo 6, rival/rival 2, rival/vive 1 |
| BORRADO - TECHO · días 1-5 | 18 | 1,1 ± 1,3 | 10 · 2 · 6 | -2.478,4 ± 1.201,2 (n = 14) | anillo/anillo 4, anillo/rival 3, anillo/vive 1, rival/anillo 4, rival/rival 3, rival/vive 1, vive/rival 1, vive/vive 1 |
| BORRADO - TECHO · días 16-20 | 18 | 3,6 ± 1,0 | 14 · 0 · 4 | -2.708,6 ± 1.294,5 (n = 12) | anillo/anillo 7, anillo/rival 1, anillo/vive 2, rival/anillo 3, rival/rival 1, rival/vive 2, vive/anillo 1, vive/vive 1 |

**3c · ¿Mueren más las que no llevan botiquín?** (todas las vidas sin corte; "con" = llevaba botiquín en el primer golpe de la pelea que la mató):

| brazo | muertes en pelea con golpe | llevaban botiquín en el primer golpe · no | vida en el primer golpe con · sin | lo usaron (de las que lo llevaban) | tics con botiquín: muertas · vivas |
|---|---:|---|---|---:|---|
| APRENDE | 35 | 11 · 24 | 100 · 94 | 6 | 46 % · 31 % |
| BORRADO | 34 | 8 · 26 | 100 · 68 | 7 | 39 % · 46 % |
| TECHO | 26 | 5 · 21 | 100 · 72 | 5 | 55 % · 59 % |

Lectura. En los días 16-20 la que recuerda muere en 14 de 14 vidas (ninguna sobrevive; en los días 1-5, 5 de 20), a los 7.760 tics de mediana (TECHO 12.912, BORRADO 12.215), 9 veces por rival y con la vida a 100 cuando la pelea empieza. El techo muere por el anillo (11 de 13), al final, y sobrevive 5 de 18. En los pares APRENDE − TECHO de los días 16-20, las causas cruzadas son anillo/anillo 2, anillo/rival 2, anillo/vive 1, rival/anillo 6, rival/vive 1: la que recuerda cae en pelea mientras el techo espera al anillo. El botiquín no entra en esa pelea: entra sana (vida 54, 75, 97, 98, 100, 100, 100, 100, 100 en los 9 primeros golpes) y lo que decide es la pelea, no la cura. Los que no llevan botiquín no mueren más (3c): en APRENDE las muertas llevaban botiquín el 46 % de sus tics y las vivas el 31 %.

Qué hacía antes de la pelea (los 240 tics anteriores al primer golpe, todas las elecciones): APRENDE `ir_curioso` 62 %, `noop` 25 %, `ir_objeto` 6 %, `ir_centro` 4 %; BORRADO `ir_curioso` 70 %, `noop` 25 %, `ir_objeto` 2 %, `ir_pareja` 1 %; TECHO `noop` 90 %, `ir_centro` 2 %, `ir_objeto` 2 %, `ir_botin` 1 %. En toda la vida (días 16-20; todas las elecciones del diario, con los tics de enfriamiento, por eso las fracciones no son las de la tabla de bloqueos): APRENDE `ir_curioso` 59 %, `noop` 29 %, `ir_objeto` 8 %, `ir_botin` 1 %, `ir_pareja` 1 %, a 9,0 casillas del centro de media; BORRADO `noop` 47 %, `ir_curioso` 45 %, `ir_objeto` 2 %, `ir_centro` 1 %, `move_N` 1 %, a 6,0; TECHO `noop` 86 %, `move_N` 3 %, `move_S` 3 %, `ir_objeto` 2 %, `move_NE` 1 %, a 4,3. Ataques: raros en los tres brazos (APRENDE 3 de 14 vidas con algún `atacar_*`, BORRADO 4 de 20 vidas con algún `atacar_*`, TECHO 11 de 18 vidas con algún `atacar_*`); ninguno en los 240 tics antes del golpe que la mata. No es que pelee peor: es que está donde están las peleas. Cuándo mueren (sin corte; antes del tic 4.000 · entre 4.000 y 10.000 · desde 10.000): APRENDE 4 · 0 · 11 en los días 1-5 y 4 · 4 · 6 en los 16-20; BORRADO 3 · 0 · 13 y 2 · 0 · 15; TECHO 0 · 0 · 15 y 0 · 0 · 13. Las muertes de principio de partida de APRENDE son las mismas en los dos bloques (s1 d16 asiento 10, tic 3.447, s1 d19 asiento 10, tic 1.441, s2 d19 asiento 10, tic 2.200, s2 d19 asiento 11, tic 2.400 en los días 16-20); lo que cambia es la media partida: peleas entre los tics 4.000 y 10.000 que en los días 1-5 no tenía.

## Sección 4 · Cautela con las semillas (punto 4)

| diferencia · serie | días 1-5 (media ± ee, n) | días 16-20 | crece |
|---|---|---|---:|
| BORRADO - TECHO · serie 1 | -1,0 ± 2,0 (n = 8) | 4,9 ± 1,3 (n = 8) | 5,9 |
| BORRADO - TECHO · serie 2 | 2,7 ± 1,7 (n = 10) | 2,5 ± 1,5 (n = 10) | -0,2 |
| APRENDE - TECHO · serie 1 | 3,2 ± 1,7 (n = 10) | 7,3 ± 1,6 (n = 6) | 4,1 |
| APRENDE - TECHO · serie 2 | 0,4 ± 1,9 (n = 10) | 5,7 ± 2,6 (n = 6) | 5,3 |
| APRENDE - BORRADO · serie 1 | 5,0 ± 2,2 (n = 8) | 4,4 ± 2,2 (n = 8) | -0,6 |
| APRENDE - BORRADO · serie 2 | -2,3 ± 0,9 (n = 10) | 3,5 ± 1,8 (n = 6) | 5,8 |

| brazo · serie | puesto días 1-5 | puesto días 16-20 |
|---|---|---|
| APRENDE · serie 1 | 10,0 ± 1,9 (n = 10) | 12,2 ± 1,1 (n = 8) |
| APRENDE · serie 2 | 7,2 ± 1,8 (n = 10) | 11,3 ± 2,3 (n = 6) |
| BORRADO · serie 1 | 7,1 ± 2,0 (n = 8) | 8,0 ± 1,5 (n = 10) |
| BORRADO · serie 2 | 9,5 ± 1,3 (n = 10) | 6,7 ± 1,6 (n = 10) |
| TECHO · serie 1 | 6,8 ± 1,6 (n = 10) | 4,6 ± 0,7 (n = 8) |
| TECHO · serie 2 | 6,8 ± 1,2 (n = 10) | 4,2 ± 0,8 (n = 10) |

Lectura. APRENDE − TECHO crece en las dos series (4,1 y 5,3), y se compone de dos movimientos que también van en la misma dirección en las dos: el techo mejora y la que recuerda empeora. BORRADO − TECHO crece en la serie 1 (5,9) y no en la 2 (-0,2); APRENDE − BORRADO crece en la 2 (5,8) y no en la 1 (-0,6). Con 6-10 pares por celda, errores estándar de 1,3-2,6 puestos y 6 celdas comparadas, solo el primero sobrevive a la cautela; los otros dos no se afirman. Los seis días de APRENDE que salen del bloque 16-20 por corte (s1 d20, s2 d18, s2 d20) dejan 6 pares por serie: la estimación de los días 16-20 es la más débil del campo.

## Sección 5 · Conclusión corta (punto 5)

La que recuerda se hunde por un candidato, no por una creencia. La curiosidad se apaga como se diseñó (ignorancia 0,05, fila a cero), pero el candidato que abrió —ir a por la cosa recordada con la cosa imaginada en el zurrón— sigue abierto con una condición `> 0` (`nace_P7_23.py:211`) y las ganas aprendidas lo valoran: la criatura anda por el mapa (o empuja un muro) 64 % de los tics con el paso listo, lejos del centro, y muere en pelea con la vida entera a media partida, mientras el techo está quieta y muere por el anillo al final. La creencia del botiquín (9-30 de 50) no es la causa de la caída —lo usa poco y sana en los tres brazos—, pero tampoco se corrige: los cortes entran como efecto 0 (`nace_P7_23.py:104`, `cuaderno_P7.py:94-96`). Tres propuestas, ninguna aplicada: (1) que `ir_curioso` exista solo mientras la clase no tenga un recuerdo firme; (2) que un sitio contra el que el paso se bloquea deje de ser destino (umbral de la mesa); (3) que el corte no entre en la media del efecto. Las tres son de las piezas de la séptima, no del cuerpo ni de los congelados. Cautela: lectura posterior al sello sobre 14 vidas de APRENDE en los días 16-20 (6 fuera por corte), con muchas comparaciones a la vez; lo único que se afirma con las dos series es la dirección de APRENDE − TECHO, que ya estaba en el sello.

*Gasto: plataforma 0 (acumulado de la séptima sin cambio: 41,9017 USD); consola 0. Saldos no consultados.*

# P7-16 · Las muertes tempranas, escena a escena, y pedir corregido

*5-oct-2026. Último análisis de este asunto: se informa de lo que se sostiene y no se prueban hipótesis nuevas. Todo es POSTERIOR A LOS SELLOS de
P7-10 y P7-14b. Coste: **créditos de la plataforma 0 USD; consola de Anthropic 0 USD.** `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al
acabar; cuerpo y congelados sin tocar. Parte A: lectura de los 640 diarios (`analiza_P7_16.py` → `P7_16_vidas.json`). Parte B: código nuevo detrás de un
interruptor apagado por defecto y un banco de réplica, una vida por proceso (`banco_P7_16.py` → `P7_16_pedir.json`); no se ha jugado nada.*

## Lo que sale, en corto

**Parte A.** (1) No hay un tipo de muerte propio de APRENDE: tiene más de casi todo, y el reparto cambia de un campo a otro. (2) Esperar para curarse no explica
las muertes tempranas: TECHO espera lo mismo o más y en P7-10 muere pronto apenas más que BORRADO (5 contra 3); ESPERANZA no espera y muere pronto como APRENDE en P7-14b. (3) En
sus primeros 11.000 tics, nada de cómo vive separa a BORRADO de APRENDE en los dos campos. (4) Lo que se sostiene en los dos campos es estrecho: APRENDE acaba
un puesto peor que BORRADO y muere pronto más a menudo; el porqué queda abierto, y con este análisis se cierra el asunto.

**Parte B.** Pedir corregido está construido detrás de un interruptor apagado y F1 pasa. En el banco sobre P7-14b, de los 48 regalos de APRENDE que volvían a quien
los dio, 47 no se habrían hecho. Pero la regla «se cierra cuando ya no le falta vida» hace que solo se pida estando herido, y eso quita tres de cada cuatro partes
con pedido, incluidos regalos que el hermano sí recogía. Lo tiene que ver la mesa antes de jugarlo.

# PARTE A · LAS ESCENAS

## Sección 1 · Las muertes tempranas, una por una

Todas las vidas que mueren antes del tic 12.000 en los cuatro brazos y los dos campos: **95** (55 antes del tic 11.000). El brazo ESPERANZA de P7-14b es el SUELO de P7-10.

| | P7-10: ESPERANZA | BORRADO | APRENDE | TECHO | P7-14b: ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mueren antes del tic 11.000 | 4 | 3 | 10 | 5 | 11 | 4 | 10 | 8 |
| mueren antes del tic 12.000 | 10 | 9 | 19 | 6 | 18 | 7 | 16 | 10 |

Lo que sigue es de las muertes antes del tic 12.000 (el corte ancho), con los dos campos juntos por brazo; el EPISODIO FINAL DE DAÑO son los golpes
seguidos sin un hueco de más de 10 segundos hasta la muerte.

| en el episodio final | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| muertes | 28 | 16 | 35 | 16 |
| rivales distintos vistos en los 30 s anteriores (mediana) | 8 | 8 | 8 | 8 |
| distancia mínima a un rival en esos 30 s (mediana, casillas) | 1 | 1 | 1 | 1 |
| tics con un rival a 2 casillas o menos, de 720 (mediana) | 146 | 118 | 144 | 272 |
| el daño empieza… tics antes de morir (mediana) | 351 | 425 | 287 | 243 |
| … desde la vida (mediana) | 100 | 100 | 100 | 100 |
| … desde 80 de vida o más | 22 | 15 | 29 | 12 |
| daño de rivales en el episodio (mediana) | 20,7 | 47,7 | 82,0 | 92,1 |
| llevaba botiquín en el episodio | 4 | 8 | 20 | 6 |
| abrió el canal en el episodio | 3 | 8 | 20 | 5 |
| veces que abrió el canal / gastó el botiquín / se le cortó | 12 / 1 / 10 | 33 / 5 / 27 | 73 / 2 / 65 | 14 / 0 / 11 |
| murió con el canal abierto | 1 | 1 | 6 | 3 |
| eligió esperar con el candidato de usar delante, 1 s o más | 3 | 1 | 16 | 4 |
| tics esperando en el episodio (mediana) | 0 | 0 | 18 | 0 |
| tics con un rival a 5 o menos (mediana) | 154 | 238 | 161 | 216 |
| … de ellos, con un candidato de alejarse | 28 % | 16 % | 15 % | 36 % |
| … cuando lo hay, lo elige | 33 % | 18 % | 19 % | 18 % |
| cuánto peor es la d de alejarse que la del elegido (mediana de las medianas) | 0,098 | 0,088 | 0,063 | 0,035 |

Lo que se lee, sin más:
- **Casi todas empiezan con la vida entera** (mediana 100 en los cuatro brazos) y duran poco: de la primera herida a la muerte pasan entre 243 y 425 tics de mediana (de 10 a 18 segundos).
- **El canal casi nunca llega a curar.** Entre los cuatro brazos se abrió 132 veces en esos episodios, se gastó el botiquín 8 y se cortó 113. Un golpe corta el canal; quien lo abre bajo golpes lo pierde.
- **Alejarse existe poco y gana menos**: con un rival a 5 casillas o menos, hay un candidato de paso que se aleja en entre el 15 y el 36 % de los tics, y cuando lo hay se elige uno de cada cinco o tres veces.
  El resto de los tics el cuerpo no tiene paso que dar (el enfriamiento del movimiento: solo `noop`) o prefiere otra cosa.
- **Esperar con el botiquín delante** (1 segundo o más en el episodio): APRENDE 16 de 35, TECHO 4 de 16, BORRADO 1 de 16, ESPERANZA 3 de 28.
  En APRENDE de P7-14b, el banco de P7-15 (decidir con y sin los días anteriores) da tics de «quieto en vez de usar» en los últimos 30 segundos en 10 de las 16.

## Sección 2 · Los tipos

Declarados en la cabecera de `analiza_P7_16.py` antes de contar, y aplicados en este orden (el primero que cumpla): **anillo** (en el episodio final el anillo
hace más daño que los rivales); **curándose bajo golpes** (abrió el canal en el episodio y recibió daño de un rival con él abierto, o murió con él abierto);
**esperando con botiquín** (llevaba botiquín, tuvo el candidato de usarlo y eligió otra cosa 1 segundo o más, sin llegar a abrir el canal); **emboscada**
(nada de lo anterior y de la primera herida a la muerte pasan 10 segundos o menos); **pelea larga** (más de 10 segundos). Los umbrales de 10 y de 1 segundo son míos.

Antes del tic 12.000:

| tipo | P7-10: ESPERANZA | BORRADO | APRENDE | TECHO | P7-14b: ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| emboscada | 1 | 1 | 7 | 2 | 5 | 3 | 7 | 4 |
| pelea larga | 4 | 4 | 5 | 0 | 3 | 1 | 3 | 4 |
| curándose bajo golpes | 1 | 0 | 2 | 2 | 0 | 0 | 1 | 1 |
| esperando con botiquín | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| anillo | 4 | 4 | 5 | 2 | 9 | 3 | 5 | 0 |
| **total** | **10** | **9** | **19** | **6** | **18** | **7** | **16** | **10** |

Antes del tic 11.000:

| tipo | P7-10: ESPERANZA | BORRADO | APRENDE | TECHO | P7-14b: ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| emboscada | 1 | 1 | 3 | 2 | 3 | 3 | 7 | 4 |
| pelea larga | 2 | 1 | 5 | 0 | 2 | 1 | 0 | 2 |
| curándose bajo golpes | 1 | 0 | 2 | 2 | 0 | 0 | 1 | 1 |
| esperando con botiquín | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| anillo | 0 | 1 | 0 | 1 | 5 | 0 | 2 | 0 |
| **total** | **4** | **3** | **10** | **5** | **11** | **4** | **10** | **8** |

**No hay un tipo de muerte que sea el de APRENDE.** Con el corte en 12.000 y los dos campos juntos, APRENDE tiene 14 emboscadas, 8 peleas largas, 10 por el anillo,
3 curándose bajo golpes y 0 esperando con botiquín; BORRADO, 4, 5, 7, 0 y 0. APRENDE tiene más de casi todo, y el reparto cambia de un campo a otro
(en P7-10 mandan las peleas largas, en P7-14b las emboscadas). «Esperando con botiquín» como tipo casi no existe (2 de 95): quien espera con el botiquín acaba abriendo el canal y cae en «curándose bajo golpes», o muere de otra cosa.

## Sección 3 · TECHO

| | P7-10 | P7-14b |
|---|---:|---:|
| muertes de TECHO antes del tic 11.000 / 12.000 | 5 / 6 | 8 / 10 |
| … en las que esperó 1 s o más con el candidato de usar delante | 1 | 3 |
| lo mismo en APRENDE: muertes / con espera | 19 / 7 | 16 / 9 |

Parte de la vida esperando (toda la vida; un tic con `usar_botiquin` entre los candidatos y otra cosa elegida):

| | ESPERANZA | BORRADO | APRENDE | TECHO |
|---|---:|---:|---:|---:|
| P7-10 | 3,8 % | 1,1 % | 10,4 % | 8,7 % |
| P7-14b | 2,3 % | 2,4 % | 6,2 % | 10,7 % |

**¿Por qué esperar no le cuesta a TECHO lo que parece costarle a APRENDE? Lo medido no dice que a APRENDE le cueste.** TECHO espera tanto como APRENDE o más
(8,7 y 10,7 % de la vida, frente a 10,4 y 6,2 %), y muere pronto menos que APRENDE en P7-10 (5 contra 10) y casi lo mismo en P7-14b (8 contra 10).
En sus muertes tempranas la espera aparece en 4 de 16; en las de APRENDE, en 16 de 35. Esperar acompaña a las muertes tempranas de APRENDE más que a las de TECHO, pero
el brazo que más espera no es el que más muere pronto. Con esto no se puede decir que esperar sea lo que mata: se queda en algo que APRENDE hace
mientras muere, no en la razón.

## Sección 4 · BORRADO

Los primeros 11.000 tics de cada vida, BORRADO menos cada uno de los otros tres brazos, emparejado por semilla (20 semillas por campo; d̄/se en cada campo).
En negrita, lo que pasa de 2 en los dos campos con el mismo signo.

| medida (primeros 11.000 tics) | BORRADO (P7-10 / P7-14b) | − APRENDE: d̄/se | − TECHO: d̄/se | − ESPERANZA: d̄/se |
|---|---|---|---|---|
| parte del tiempo con menos de 50 de vida | 2,0 % / 1,4 % | 0,8 / -0,2 | 0,3 / 0,9 | 1,1 / 0,7 |
| … con un rival a 1 o 2 casillas | 4,4 % / 5,5 % | -0,5 / 0,1 | -0,7 / 0,6 | 0,4 / 1,4 |
| rivales a la vista (media) | 1,72 / 1,95 | 0,3 / 1,5 | -0,3 / 1,0 | 0,0 / 0,3 |
| distancia al centro del círculo | 4,08 / 4,09 | -0,5 / -1,2 | -1,9 / -0,6 | -2,2 / -1,8 |
| distancia al hermano | 2,11 / 2,38 | -0,5 / 0,1 | -1,5 / 1,5 | -2,1 / 1,9 |
| … con botiquín | 59,9 % / 64,8 % | -0,1 / -0,2 | 0,8 / 1,3 | 2,0 / 3,1 |
| … con ración | 34,4 % / 31,1 % | 0,2 / -1,4 | 1,1 / 0,1 | -0,9 / -0,9 |
| … con arma | 54,4 % / 62,8 % | 0,8 / 0,2 | -0,5 / 0,1 | -0,3 / 1,0 |
| … con el zurrón lleno | 54,4 % / 49,5 % | 1,5 / -1,5 | 0,3 / 0,2 | 0,5 / 1,5 |
| casillas por 1.000 tics | 74,9 / 67,7 | 0,6 / -1,5 | 0,8 / 0,6 | 0,9 / 0,4 |
| … esperando con el candidato de usar delante | 0,3 % / 2,0 % | -3,1 / -1,2 | -2,0 / -1,9 | -1,9 / -0,1 |
| … con el canal abierto | 0,4 % / 0,4 % | 0,8 / 0,5 | 3,9 / 1,5 | 2,6 / 1,4 |
| daño de rivales por 1.000 tics | 4,06 / 7,77 | -0,3 / -1,3 | 1,2 / 0,6 | 1,2 / 0,2 |
| golpes de rival recibidos | 2,00 / 1,89 | -1,7 / -1,1 | 1,0 / -1,5 | -0,6 / -0,4 |
| … con `ir_curioso` elegido | 12,8 % / 12,9 % | -1,5 / 0,4 | **5,7 / 4,9** | **5,7 / 4,9** |
| … con `ir_objeto` elegido | 2,3 % / 1,9 % | 0,1 / -2,0 | 0,1 / -1,1 | 0,6 / -0,6 |
| … con `noop` elegido | 74,3 % / 73,1 % | 3,2 / -0,6 | **-4,5 / -2,4** | **-4,4 / -3,0** |

- **Frente a APRENDE, nada pasa la prueba de los dos campos** (ninguna medida). Lo más cerca: BORRADO espera menos con el botiquín delante (d̄/se -3,1 y -1,2).
- **Frente a TECHO y a ESPERANZA**, lo que pasa en los dos campos es lo que el diseño pone: … con `ir_curioso` elegido, … con `noop` elegido (BORRADO tiene curiosidad y ellos no; por eso está menos tiempo sin hacer nada).
- Juntando las dos cosas: BORRADO es el único brazo que **se mueve por curiosidad y a la vez no espera para curarse** (cada día empieza sin saber, con el
  botiquín valorado como una ración). APRENDE tiene la curiosidad pero espera; ESPERANZA no espera pero no tiene curiosidad; TECHO ni lo uno ni lo otro.
  Que esa combinación sea la que le da ventaja es una lectura de la tabla, no algo medido: ninguna de las medidas de cómo vive en esos 11.000 tics
  (poca vida, rivales cerca, daño recibido, lo que lleva, dónde está) lo separa de los otros tres en los dos campos.

## Sección 5 · Conclusión en tres líneas

- **Se sostiene en los dos campos a la vez:** APRENDE acaba alrededor de un puesto peor que BORRADO y muere más antes del tic 11.000 y del 12.000; BORRADO es el único brazo con curiosidad que no espera para curarse.
- **No se sostiene:** que haya un tipo de muerte propio de APRENDE; que esperar para curarse sea lo que mata (TECHO espera lo mismo; ESPERANZA no espera y muere pronto igual en P7-14b); que APRENDE viva distinto (vida, peleas, zurrón, sitio) antes de morir.
- **Queda abierto:** por qué BORRADO muere pronto menos que los otros tres en P7-14b, y si la diferencia de 6 o 7 muertes tempranas por campo es algo del cuaderno o del azar de las partidas; con estos dos campos no se puede decidir.

# PARTE B · PEDIR CORREGIDO

## Sección 6 · Lo construido

En `pide_P7.py` y `descubre_P7.py`, detrás del interruptor `GEMV_P7_PIDE2` (0 por defecto: los campos jugados se replican como se jugaron; con 0 nada cambia).

| regla (diseño de Manel) | cómo está hecha | dónde |
|---|---|---|
| (a) el pedido se cierra al tener, o cuando ya no le falta vida; no al verlo | una vez abierto sigue abierto hasta que el botiquín está en el zurrón o la vida llega a su máximo (`mem.hp_max`); ver un botiquín ya no lo cierra. Para abrirlo sigue haciendo falta no ver ninguno | `pide_P7.pide2` |
| (b) solo se pide lo que se podría coger | con un hueco para él (`decisor_zs._pack_con`, la prueba de «cabe» del cuerpo) y la promesa mayor que cero; o, con el zurrón lleno, si hacer sitio ganaría: se le pregunta a `decide`, sobre una copia de la escena con un botiquín en su casilla y una copia de la memoria, si elegiría `hacer_sitio_<algo>_por_<botiquín>`. Si no, no pide, y un pedido abierto se cierra | `pide_P7.cabe`, `pide_P7.haria_sitio` |
| (c) las ganas no suman alivio de curiosidad cuando no se podría llevar | `_promesa` devuelve solo la promesa del cuerpo (que con el zurrón lleno es 0) cuando el botiquín no cabe | `descubre_P7.py`, `_promesa` |

**Una consecuencia de (a) que la mesa debe ver:** si el pedido se cierra «cuando ya no le falta vida», una criatura con la vida entera no puede tener un pedido abierto
(se cerraría en el parte siguiente). Lo he hecho así, literal: **con el pedido corregido solo se pide estando herido.** En P7-14b, 7.133 de los 9.467 partes con pedido
se emitieron con la vida entera.

**F1 sigue pasando** (`P7_16_F1.json`): apagado 1.007.274 tics iguales y 2 distintos; TECHO 1.007.274 y 2 (los dos de siempre).

## Sección 7 · El banco sobre P7-14b

`banco_P7_16.py`: las 320 vidas de P7-14b replicadas con el pedido corregido. La réplica sigue el diario: dice qué parte habría emitido cada criatura en la vida que vivió,
no cómo habría sido la partida. Fidelidad de la elección tic a tic: pase 1, 4.069.814 iguales y 7.368 distintos (los distintos vienen de (c): sin el alivio de curiosidad de lo que no cabe, algunos pasos cambian).

| | ESPERANZA | BORRADO | APRENDE | TECHO | los cuatro |
|---|---:|---:|---:|---:|---:|
| partes comparados | 21.330 | 21.792 | 20.698 | 21.227 | 85.047 |
| partes con pedido en el campo | 2.566 | 3.029 | 1.939 | 1.933 | 9.467 |
| partes con pedido, corregido | 755 | 914 | 890 | 934 | 3.493 |
| pedía en el campo y corregido no | 2.173 | 2.592 | 1.372 | 1.456 | 7.593 |
| … porque no tenía hueco | 0 | 734 | 360 | 0 | 1.094 |
| … porque no le faltaba vida | 2.173 | 2.335 | 1.169 | 1.456 | 7.133 |
| no pedía en el campo y corregido sí | 362 | 477 | 323 | 457 | 1.619 |
| partes con pedido porque hacer sitio ganaría | 0 | 2 | 1 | 58 | 61 |
| pedidos abiertos en el campo | 200 | 264 | 310 | 323 | 1.097 |
| pedidos abiertos, corregido | 32 | 35 | 36 | 39 | 142 |
| cierres en el campo: «lo ve» / «lo lleva» / otros | 177 / 3 / 7 | 246 / 2 / 0 | 289 / 6 / 0 | 299 / 8 / 5 | 1011 / 19 / 12 |
| cierres corregido: «lo lleva» / «ya no le falta vida» / «no podría cogerlo» / «ya no le alivia» | 2 / 0 / 8 / 0 | 4 / 1 / 10 / 0 | 11 / 0 / 5 / 0 | 7 / 6 / 9 / 0 | 24 / 7 / 32 / 0 |

**Los regalos** (pase 2: quien regaló oye los partes corregidos del hermano; 893 partes cambian; fidelidad 362.813 iguales, 13.482 distintos):

| | regalos en el campo | el hermano pediría (corregido) | la réplica sigue regalando | no se habrían hecho |
|---|---:|---:|---:|---:|
| **los 48 de APRENDE que volvían a quien los dio** | 48 | 1 | 1 | **47** |
| los 7 de APRENDE que cogió el hermano | 7 | 5 | 5 | 2 |
| todos los de APRENDE | 56 | 6 | 6 | 50 |
| todos los de TECHO | 37 | 2 | 2 | 35 |
| todos (los cuatro brazos) | 95 | 9 | 9 | 86 |

**Lo que se lee.**
- **Los 48 regalos que volvían a quien los dio: 47 no se habrían hecho** y 1 sí. En esos 47 el hermano, con el pedido corregido, no estaría pidiendo cuando se hizo el regalo.
- **Los pedidos se quedan en la octava parte**: de 1.097 abiertos en el campo a 142, y de 9.467 partes con pedido a 3.493. Casi todo lo que desaparece es por la vida:
  7.133 de los 9.467 partes con pedido del campo se emitieron con la vida entera (regla (a)); por falta de hueco (regla (b)), 1.094, todos en BORRADO y APRENDE, los dos brazos
  con curiosidad, como se vio en P7-15. Aparecen 1.619 partes con pedido que en el campo no lo llevaban: pedidos que antes se cerraban al ver un botiquín y ahora siguen abiertos.
- **Hacer sitio casi nunca ganaría**: solo 61 partes con pedido lo son por esa vía (58 en TECHO). Con el zurrón lleno, casi nunca se pide.
- **El pedido corregido casi no se cierra**: de los 142 abiertos se cierran 63 (24 porque lo lleva, 32 porque deja de poder cogerlo, 7 porque ya no le falta vida); los demás siguen abiertos hasta el final de la vida.
- **El coste de la regla de la vida.** De los 21 regalos del campo que el hermano sí recogía (7 de APRENDE y 14 de TECHO), siguen 6 (5 y 1): los demás se hicieron a un hermano que,
  con la regla corregida, no estaría pidiendo (casi siempre porque tenía la vida entera). Si regalar a un hermano sano que no tiene botiquín es algo que el diseño quiere conservar, la regla (a) tal como está escrita lo quita.
- Avisos de banco, los de siempre: la réplica sigue el diario; después de la primera decisión distinta lo que ve la criatura es lo que pasó en el campo. Y esto es banco: no se ha jugado.

**Para la mesa (nada decidido):** (1) si «ya no le falta vida» debe cerrar el pedido también cuando la criatura está entera desde el principio (es lo que deja el pedido solo para heridos);
(2) si con el zurrón lleno debe poder pedirse algo (hoy, casi nunca); (3) si el pedido corregido se prueba en campo, es código nuevo y pide sello nuevo.


## Archivos

| archivo | qué es |
|---|---|
| `analiza_P7_16.py` → `P7_16_vidas.json` | las escenas de las 95 muertes tempranas, los tipos, la espera y los primeros 11.000 tics de las 640 vidas |
| `pide_P7.py` (`pide2`, `cabe`, `haria_sitio`), `descubre_P7.py` (`PIDE2`, `_promesa`) | pedir corregido, detrás de `GEMV_P7_PIDE2` (apagado por defecto) |
| `banco_P7_16.py` → `P7_16_pedir.json`; `P7_16_F1.json` | el banco de pedir corregido sobre P7-14b y F1 |
| `escribe_informe_P7_16.py`, `informe_P7_16.md` | este informe |

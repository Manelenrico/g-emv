# P7-19 · Lo dado no está entregado mientras quien lo dio lo pisa

*5-oct-2026. Coste: plataforma 0, consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. Solo banco: no se ha jugado nada.
`banco_P7_19.py`, una vida por proceso, sobre las 320 vidas de P7-14b con el pedido de P7-17 y el arreglo → `P7_19_todo.json` (F2 y F4) y `P7_19_f3.json` (F3).*

## Lo que sale, en corto

- **Con el arreglo, quien regala se aparta: en las 40 escenas de P7-18, en las 40**, a los 2 tics de mediana (como mucho 10).
- **Con la casilla libre, el que pedía va hacia el botiquín en 24 de 39** escenas evaluadas; en 15 no, por las otras causas que ya se vieron en P7-18.
- **No hace daño en otro sitio**: de 4.077.182 tics, la decisión cambia en 6.147; 6.077 son la criatura sobre su propio regalo (el caso) y 70 no.
- **La primera versión que escribí no hacía nada**, y la corregí (sección 1). Mi explicación de P7-18 estaba equivocada en un punto y lo digo ahí.

## Sección 1 · El arreglo, y la corrección a mi propuesta

En `pide_P7.py`, detrás de `GEMV_P7_PIDE2` (apagado por defecto), para los cuatro brazos; `GEMV_P7_PISO=0` lo apaga, solo para comparar en banco:

1. Al elegir `soltar_<botiquín>`, la criatura apunta la casilla de su regalo y cuántos da (`ESTADO["mis_regalos"]`, en su estado de la partida, no en la memoria del cuerpo).
2. En las fotos en que ella misma está sobre esa casilla y el botiquín sigue ahí, las filas que regalan (S-DANO-PAREJA, S-HERIDO, R-HERMANO-FALTA, S-PROVISION) **valen lo que valían
   antes de darlo**: se calculan con el botiquín otra vez en su zurrón y fuera del suelo. No cuentan el alivio.
3. En la foto de regalar, que se evalúa antes de apuntar nada, el alivio cuenta como hasta ahora.
4. La marca se borra cuando, con la casilla al lado o debajo, el botiquín ya no está. Ningún número nuevo.

**La corrección.** Lo primero que escribí fue lo que propuse en P7-18: sobre su regalo, las filas valían «lo que valdrían sin el botiquín en el suelo». **No hacía nada**: en la vida de
prueba (TECHO, serie 1, día 7, asiento 10), 3.717 tics con la marca viva y 0 decisiones distintas. El motivo: quien regala suelta la pila entera y se queda sin botiquines
(en los 40 regalos de P7-18 no le queda ninguno; diarios del campo), y S-PROVISION exige llevar alguno (`appraisal_zs_v42_exp.py:1317`), así que después de regalar vale 0
encima del botiquín y fuera de él (medido en los diarios: 0 en los 40). No había malestar que quitar ni que dejar. En P7-18 escribí que quedarse quieto era lo mejor «con el malestar ya
aliviado» y que apartarse lo aliviaría: lo primero era verdad a medias (el malestar no estaba aliviado, había desaparecido) y lo segundo era falso.
La versión que queda es la del punto 2: mientras lo pisa, el botiquín cuenta como si aún fuera suyo, que es lo que dice el título. La regla de la mesa («no cuentan el alivio») es la
misma; cambia cómo se calcula. La he corregido yo sin pasar por la mesa y lo dejo dicho.

## Sección 2 · F1

`P7_19_F1.json`: apagado 1.007.274 tics iguales y 2 distintos; TECHO sin PIDE2 1.007.274 y 2 (los dos de siempre). **Pasa.**

## Sección 3 · F2: ¿se aparta quien regaló?

La réplica sigue el diario (en el diario, quien regaló se queda en la casilla); se mira qué elige en cada tic desde el regalo hasta el primero en que elige irse.

| | las 40 escenas de P7-18 | los 95 regalos del campo |
|---|---:|---:|
| la réplica regala en ese mismo tic (los demás no se pueden seguir: con el pedido de P7-17 ese regalo no se elige en ese tic) | 40 | 60 |
| **se aparta** | **40** | **60** |
| no se aparta en 720 tics | 0 | 0 |
| en el diario deja la casilla antes de que la réplica elija irse | 0 | 0 |
| tics del regalo a la decisión de irse: mediana (mín – máx) | 2 (1 – 10) | 2 (1 – 13) |

En las 40 escenas: lo que elige para irse es un paso (`move_*` o `paso_*`) 35, `ir_objeto` 4, `coger` 1; en ese mismo tic, sin el arreglo, elegía `noop` 24, `un paso` 11, `ir_objeto` 4, `coger` 1.
La d de `noop` queda 0,186 por encima de la del paso elegido (mediana): no es un empate. De los tics de espera antes de irse, casi todos son del enfriamiento del paso (solo `noop` entre los
candidatos); en 27 de las 40 hay además un tic en que, pudiendo moverse, la réplica vuelve a elegir `soltar` o `noop` (el diario no sigue a la réplica: ese tic es del banco). **Hacia dónde:** a una casilla vecina, la que el cuerpo prefiera en ese momento (S 14, SW 8, E 6, W 5, N 3, SE 2, NE 1, — 1); no hay una dirección escrita.
En una escena (TECHO, serie 2, día 14) lo que elige no es un paso sino `coger`: recoge su propio regalo en vez de apartarse. Con el botiquín «como si fuera suyo» mientras lo pisa,
recuperarlo es una forma de dejar de pisar un regalo sin entregar; pasa 1 vez de 40.

## Sección 4 · F3: con la casilla libre, ¿va el que pedía?

Para cada escena, la vida del que pedía, replicada con el pedido de P7-17 y el arreglo. Desde el tic siguiente a aquel en que quien regaló elige irse, se le enseña la misma escena
del diario con el hermano puesto en la casilla a la que iría, y se apunta lo que elige en el primer tic en que tiene algo más que `noop`. Es una sola decisión; no se inventa el resto.

| | |
|---|---:|
| escenas evaluadas (la que acaba en `coger` de quien regaló no deja la casilla libre con el botiquín) | 39 de 40 |
| el que pedía ve el botiquín, no lleva ninguno y le cabe | 38 |
| su pedido sigue abierto | 39 |
| **elige ir hacia el botiquín** (un paso que lo acerca, o `ir_objeto`/`ir_curioso` con ese destino) | **24** |
| … de ellos, el paso entra ya en la casilla del botiquín | 12 |
| … con candidato explícito de ir a por él y elegido | 3 |
| **no va hacia él** | **15** |
| … elige ir a por otro objeto (`ir_objeto` o `ir_curioso` con otro destino) | 11 |
| … elige `noop` u otro paso | 4 |
| `coger` entre sus candidatos (aún no está encima) | 0 |

Por brazo, van hacia él: TECHO 12 de 22, APRENDE 12 de 15, BORRADO 0 de 2. Los 15 que no van son las otras causas de P7-18, que este arreglo no toca: su mejor objeto es otro (o uno recordado en su propia casilla),
las cesiones cruzadas de TECHO (6 de los 15 son de una sola pareja, serie 1, día 7) y el zurrón lleno de BORRADO.
**Tener el candidato y ganar no es todavía cogerlo**: el banco enseña una decisión, no los pasos siguientes.

## Sección 5 · F4: ¿cambia algo en otro sitio?

Las 320 vidas de P7-14b con el arreglo; en cada tic con alguna marca de regalo viva se decide además con el arreglo apagado, sobre copias, y se compara. Sin marca viva el arreglo no
entra en el cálculo (la condición es estar sobre una casilla apuntada), así que ahí la decisión es la misma por construcción.

| | |
|---|---:|
| tics de las 320 vidas | 4.077.182 |
| tics con alguna marca de regalo viva | 29.869 (23 vidas) |
| **tics en que la decisión cambia** | **6.147** (0,15 % de todos los tics; 10 vidas) |
| … con la criatura sobre su propio regalo (el caso) | 6.077 |
| … **no sobre su regalo** | **70** |

Sobre su regalo: un paso en vez de `noop` 6.066, soltar_rations en vez de `noop` 6, ir_pareja en vez de `noop` 5. (Son muchos tics porque la réplica sigue el diario, donde quien regaló se queda en la casilla; en una
partida se iría en el primero.) Entre ellos, 6 en que suelta una ración y 0 en que recoge el botiquín.

**Los 70 que no son de este caso**: `ir_objeto` en vez de `ir_curioso` 56, `noop` en vez de `ir_curioso` 8, `ir_centro` en vez de `ir_pareja` 4, `un paso` en vez de `un paso` 1, `ir_centro` en vez de `ir_curioso` 1, en 4 vidas (s1_d19_APRENDE_11, s1_d3_TECHO_11, s1_d4_BORRADO_10, s2_d8_APRENDE_10). En ninguno de los 70 está sobre su regalo, y el arreglo solo actúa en fotos en que la criatura
está sobre una casilla apuntada con el botiquín en ella (`piso_mi_regalo`); así que, por el código, tiene que ser una foto imaginada de un candidato que la deja encima de su regalo: esa
foto ya no cuenta el alivio y gana otro candidato. Sería el mismo arreglo un paso antes (no volver a pisar el regalo). **Esto lo deduzco del código; no lo he medido escena a escena**
(el banco no guardó la distancia al regalo en esos tics).

Un aviso sobre el banco, que no es del arreglo sino del pedido de P7-17: con los pedidos abiertos mucho más tiempo, la réplica elige regalar en muchas más ocasiones que el campo
(rachas de tics seguidos eligiendo `soltar_first_aid`: TECHO 301 frente a 37 regalos en el campo, APRENDE 179 frente a 56 regalos en el campo, BORRADO 19 frente a 2 regalos en el campo, ESPERANZA 0 frente a 0 regalos en el campo). En la réplica son elecciones sobre el diario, no regalos hechos; cuántos
habría en una partida solo lo dice un campo.

Por lo mismo, fuera de las 40 escenas los seguimientos de la réplica no valen como medida: de 7.796 que acaban en «se aparta», 1.727 tardan más de 13 tics, y es porque la réplica
vuelve a elegir `soltar_first_aid` tic tras tic (en el diario el botiquín sigue en su zurrón) y no porque se quede quieta sobre un regalo hecho. Otros 3.936 se cortan porque en el
diario ya no está en la casilla y 728 llegan a 720 tics sin que haya botiquín en el suelo del diario. Las cifras de F2 son solo las de regalos que existen en el campo.

## Sección 6 · Lo que queda para la mesa

1. El arreglo hace lo que tenía que hacer en banco (40 de 40 se apartan) y abre el paso al que pide en 24 de 39. Jugarlo es código nuevo: sello nuevo.
2. Los 15 que no van son del lado de quien pide (P7-18, sección 3) y siguen sin tocar.
3. Una vez de 40, quien regaló recoge su propio regalo en vez de apartarse. Si eso no se quiere, hay que decirlo; yo no lo he tocado.
4. Con el pedido de P7-17 habría muchos más regalos que en P7-14b. Si son demasiados o no, y si se cogen, no se puede saber en banco.

## Archivos

| archivo | qué es |
|---|---|
| `pide_P7.py` (`piso_mi_regalo`, `ESTADO["mis_regalos"]`, `_filas`, `decidir`) | el arreglo, detrás de `GEMV_P7_PIDE2` |
| `banco_P7_19.py` → `P7_19_todo.json`, `P7_19_f3.json`; `P7_19_F1.json` | F2, F4, F3 y F1 |
| `informe_P7_19.md` | este informe |

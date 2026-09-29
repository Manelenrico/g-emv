# P5-4A — El banco de la confianza: oráculo, mentiroso y nadie se mueve

En seco, coste cero, sin modelo de lenguaje. Nada a la plataforma. **Ninguna
decisión real cambia.** Mismos 40 diarios, mismas 2.230 escenas, sobre el banco
de P5-3H: regla E1+G2, margen 0,02, comparador en ventana, sin `deepcopy`.

**Tres resultados y un hallazgo incómodo.** La confianza **separa al mentiroso**
con claridad: acaba en 0,000 y por debajo de 0,2 en 34 de 40 diarios. **Pero no
distingue al oráculo de un consejero trivial:** «nadie se mueve» acierta el
**96,8 %** y acaba también en 1,000. Y **saber la verdad apenas sirve**: el
oráculo recupera el **14,0 %** del aporte real de los rivales, menos que «nadie
se mueve» con su **16,5 %**.

---

## A0 · ¿Existe la verdad? **No.**

Comprobado por las dos vías:

```
$ coworld episode-logs ereq_9cf61642-… --game
===== container: game =====
b'zero_sum server on 0.0.0.0:8080\nmatch starting with 16/16 seats connected\n
CHAT [t=00001] [team] sivannn (B): plan: stay out of the fortress crush…'
```

**El log del juego es el stdout de los contenedores**: arranque, chat y avisos.
Catorce líneas, **cero posiciones**.

El replay (`softmax-public.s3…/b730427d-….replay`) son 6,8 MB comprimidos y
**30,5 MB de binario propietario** que empieza por `ZERO_SUM_FRAMES`, sin
especificación local y sin su visor.

**Declarado: el oráculo usa la VERDAD PARCIAL** — la posición real de cada rival
en el punto de control **cuando alguno de los dos hermanos lo vio en ese tic**, y
piso cuando no lo vio ninguno. Tener los dos diarios ayuda: la unión de lo que
vieron los dos es más rica que lo de uno solo.

## A1 y A2 · Los tres consejeros y cómo entra lo dicho

| consejero | qué dice |
|---|---|
| **oráculo** | la posición real (verdad parcial de A0) |
| **mentiroso** | una casilla pisable al azar del mapa, semilla fija 20260920 |
| **nadie se mueve** | que cada rival sigue donde estaba en el tic de ventana |

Los tres hablan sobre **los mismos rivales en los mismos puntos de control**, y
también para **las formas propias del comparador**: el cuerpo imagina lo suyo
con la misma información.

**Cómo entra**, en las cinco filas de rivales (`F-4-ALCANCE`, `S-8-EXPOSICION`,
`S-7-AGRESOR`, `MIEDO_APRENDIDO`, `S-VIDA-AJENA`):

```python
out[k] = m if m >= piso else piso - C * (piso - m)
```

Lo malo se cree entero; lo bueno entra multiplicado por C. **Con C = 0 y «nadie
se mueve» sale exactamente E1+G2**, y se ve en la tabla: 41 formas de O-después
pasan la regla, las mismas 41 de P5-3H.

---

## A3 · Confianza fija

| consejero | C | O-después pasa | acepta | en la mesa | azar pasa | acepta | en la mesa | **diferencia en la mesa** |
|---|---|---|---|---|---|---|---|---|
| **nadie** | 0 | 41 (4,52 %) | 24 (2,64 %) | 58,5 % | 7 (0,77 %) | 2 (0,22 %) | 28,6 % | +29,97 (−6,74, +66,67) |
| | 0,5 | 117 (12,89 %) | 53 (5,84 %) | 45,3 % | 53 (5,84 %) | 24 (2,64 %) | 45,3 % | **+0,02** |
| | **1** | **149 (16,41 %)** | 96 (10,57 %) | 64,4 % | 91 (10,02 %) | 42 (4,63 %) | 46,2 % | **+18,28** (+5,47, +31,08) |
| **oráculo** | 0 | 44 (4,85 %) | 27 (2,97 %) | 61,4 % | 8 (0,88 %) | 2 (0,22 %) | 25,0 % | +36,36 (+3,09, +69,64) |
| | 0,5 | 113 (12,44 %) | 50 (5,51 %) | 44,2 % | 59 (6,50 %) | 23 (2,53 %) | 39,0 % | +5,26 |
| | **1** | **142 (15,64 %)** | 93 (10,24 %) | 65,5 % | 92 (10,13 %) | 45 (4,96 %) | 48,9 % | **+16,58** (+3,72, +29,44) |
| **mentiroso** | 0 | 37 (4,07 %) | 24 (2,64 %) | 64,9 % | 2 (0,22 %) | 0 | 0,0 % | +64,86 |
| | 0,5 | 45 (4,96 %) | 28 (3,08 %) | 62,2 % | 8 (0,88 %) | 2 (0,22 %) | 25,0 % | +37,22 |
| | **1** | 54 (5,95 %) | 30 (3,30 %) | 55,6 % | 13 (1,43 %) | 4 (0,44 %) | 30,8 % | +24,79 (−3,59, +53,16) |

**Tres cosas que salen de aquí.**

1. **Creer sube lo que pasa la regla, pero sube igual el azar.** Con C = 1,
   O-después pasa del 4,5 % al 16,4 % con «nadie» y al 15,6 % con el oráculo;
   el azar pasa del 0,8 % al 10,0 % y 10,1 %. **La diferencia en la mesa baja**
   de +29,97 a +18,28.
2. **Con C = 0,5 la diferencia se anula** (+0,02 con «nadie»). Media confianza
   es lo peor de los dos mundos: deja pasar al azar sin dar al bueno lo
   suficiente.
3. **El mentiroso, con C = 1, casi no mueve nada** (5,95 % contra 4,07 %).
   Porque miente **también sobre las formas propias**, así que el comparador se
   degrada igual y la comparación se mantiene. Eso es un artefacto del diseño,
   y se declara.

### La recuperación por grupo (C = 1), contra lo real de F2

| consejero | **rivales** | hermano | propias |
|---|---|---|---|
| **nadie se mueve** | **+17,23 = 16,5 %** | +6,42 = 7,5 % | +0,53 = 2,4 % |
| **oráculo** | **+14,62 = 14,0 %** | +7,47 = 8,8 % | +1,82 = 8,1 % |
| mentiroso | +0,84 = 0,8 % | +3,58 = 4,2 % | +0,84 = 3,7 % |

**Saber la verdad no gana a no decir nada.** El oráculo recupera el 14,0 % del
aporte real de los rivales; «nadie se mueve» recupera el **16,5 %**. La razón es
la de siempre: **en el horizonte de una forma los rivales apenas se mueven**, así
que la verdad y la suposición trivial dicen casi lo mismo, y la trivial es algo
más optimista.

Los dos, eso sí, **rompen el −2,4 % de P5-3H**: creer algo sobre los rivales
recupera por primera vez una parte de ese 87 %.

---

## A4 · La confianza que se gana

C empieza en **0,5** en cada diario. Por cada rival del que el consejero dijo
una posición **y que luego fue visto en ese tic por alguno de los hermanos**:
acierto si la distancia es de **3 casillas o menos**; **+0,05** por acierto,
**−0,10** por fallo, acotada en 0 y 1. *(Valores elegidos por la mesa; se probó
también 0,10 / 0,20 y da lo mismo: ver la fila `din2` en los json.)*

| consejero | dichos | **comprobados** | aciertos | **C final** | trayectoria (0-500 / 500-1500 / >1500) | >0,8 | <0,2 |
|---|---|---|---|---|---|---|---|
| **oráculo** | 12.604 | **12.604 (100 %)** | **12.604 (100 %)** | **1,000** | 1,0 / 1,0 / 1,0 | **36/40** | 0/40 |
| **nadie se mueve** | 9.974 | 7.939 (79,6 %) | 7.684 (**96,8 %**) | **1,000** | 0,45 / 1,0 / 1,0 | 26/40 | 2/40 |
| **mentiroso** | 9.974 | 7.939 (79,6 %) | 178 (**2,2 %**) | **0,000** | 0,0 / 0,0 / 0,0 | 0/40 | **34/40** |

**El modo de fallo que T3 temía no ocurre: el 79,6 % de lo dicho llega a
comprobarse**, y el 100 % en el caso del oráculo, que por construcción solo
habla de lo que alguien vio.

**Con C dinámica**, las tasas quedan muy cerca de las de C = 1:

| consejero | O-después pasa | acepta | azar pasa | acepta | diferencia en la mesa |
|---|---|---|---|---|---|
| nadie | 142 (15,64 %) | 92 (10,13 %) | 81 (8,92 %) | 36 (3,96 %) | **+20,34** (+6,97, +33,72) |
| oráculo | 143 (15,75 %) | 93 (10,24 %) | 89 (9,80 %) | 42 (4,63 %) | **+17,84** (+4,86, +30,83) |
| **mentiroso** | **37 (4,07 %)** | 24 (2,64 %) | **2 (0,22 %)** | **0** | **+64,86** |

**La confianza dinámica hace exactamente lo que debía con el mentiroso**: lo
apaga. Sus cifras con C dinámica son **las de C = 0**, o sea las de no
escucharle. **El daño del mentiroso queda en cero.**

---

## A5 · El daño, y por qué no se puede medir como estaba escrito

**A5 pide comparar con «lo que el cuerpo habría hecho solo», y ese dato no
existe.** El diario tiene **una sola línea de tiempo**: no hay contrafactual. Y
para O-después la pregunta es además vacía por construcción, porque esas escenas
se eligen precisamente porque `d(t+100) < d(t)`.

**Lo que sí se puede decir, y se dice:**

| consejero | C = 1: O-después aceptadas | azar aceptadas | C din: O-después | azar |
|---|---|---|---|---|
| nadie | 96 | 42 | 92 | 36 |
| oráculo | 93 | 45 | 93 | 42 |
| **mentiroso** | 30 | **4** | 24 | **0** |

**Con C dinámica el mentiroso no cuela ni una forma de azar.** Ese es el
resultado que A5 buscaba, medido por la vía que los datos permiten.

## A6 · La figura

`cantera/paper5/figC/A6_confianza.png`: C a lo largo de la vida en los dos
diarios más largos, para los tres consejeros. Se ve el oráculo pegado al techo
desde el primer tramo, «nadie se mueve» subiendo desde 0,5 hasta el techo en los
primeros quinientos instantes, y el mentiroso cayendo a cero y quedándose.

## A3/A4 · El coste

| consejero | mediana | máximo |
|---|---|---|
| nadie | 12,14 ms | 18,14 |
| oráculo | 12,32 ms | 55,04 |
| mentiroso | 12,01 ms | 17,05 |

Contra los 4,39 ms de E1+G2: **el triple**, porque cada punto de control
resuelve cinco confianzas y el comparador entero se recalcula para cada una.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **T1** | oráculo C=1 recupera más del 40 % del aporte real de los rivales | A3 | **14,0 %** | **FALLA** |
| **T1** | …y sube lo que O-después pasa por encima del 20 % de las construidas | A3 | **15,64 %** | **FALLA** |
| **T2** | mentiroso C=1: el azar aceptado sobre construidas sube del 5 % | A3 | **0,44 %** | **FALLA** |
| **T2** | …y la diferencia en la mesa baja de 20 puntos | A3 | **+24,79** | **FALLA** |
| **T3** | oráculo por encima de 0,8 en más del 80 % de los diarios | A4 | **36/40 = 90 %** | **CUMPLE** |
| **T3** | mentiroso por debajo de 0,2 en más del 80 % | A4 | **34/40 = 85 %** | **CUMPLE** |
| **T3** | «nadie se mueve» queda entre los dos | A4 | 26/40 por encima de 0,8, **pero su mediana empata con el oráculo en 1,000** | **a medias** |
| **T4** | el daño del mentiroso queda por debajo del 2 % de las construidas | A5 | **0,00 %** (cero formas de azar) | **CUMPLE** |
| **T4** | el oráculo conserva más de la mitad de lo que recupera con C=1 | A4 | C dinámica ≈ C=1 (93 contra 93 aceptadas): **100 %** | **CUMPLE** |
| **T5** | O-ahora 100 % en todo | A3 | **2.230 de 2.230** en los tres consejeros y las cinco C | **CUMPLE** |

**Los contadores podían variar, comprobado.** El de la recuperación va del 0,8 %
del mentiroso al 16,5 % de «nadie». El de lo que pasa la regla va del 4,07 % al
16,41 % según consejero y C. El de la confianza final va de 0,000 a 1,000. El
del azar aceptado va de 0 a 45 formas.

### T2 falla, y falla por un artefacto de diseño que hay que decir

El mentiroso no hace daño con C = 1 porque **miente también sobre las formas
propias del comparador**, como pedía A1 («el cuerpo imagina lo suyo con la misma
información»). Las dos curvas se degradan a la vez y la comparación aguanta.

**Un mentiroso que mintiera solo sobre las propuestas ajenas sí haría daño**, y
eso no está medido aquí.

---

## Lo que este banco deja dicho

1. **La confianza funciona contra la mentira.** El mentiroso cae a 0,000 en el
   85 % de los diarios y con C dinámica **no cuela ni una forma de azar**. La
   ficha se sostiene en su parte defensiva.
2. **Pero no distingue al que sabe del que no dice nada.** «Nadie se mueve»
   acierta el 96,8 % y gana la misma confianza que el oráculo. El premio se paga
   por **acertar**, y acertar es trivial cuando el mundo apenas se mueve en el
   horizonte de una forma.
3. **Y saber la verdad casi no paga.** El oráculo recupera el 14,0 % del aporte
   de los rivales; la suposición trivial, el 16,5 %. **El techo del 87 % de
   P5-3F sigue casi entero**, incluso con verdad.
4. **Creer más deja pasar más de todo.** De C = 0 a C = 1, O-después pasa del
   4,5 % al 16,4 % y el azar del 0,8 % al 10,0 %; la diferencia en la mesa baja
   de +29,97 a +18,28. **C = 0,5 es el peor punto**: la anula (+0,02).
5. **La verdad entera no existe en estos datos**, y eso limita todo lo anterior:
   el oráculo solo puede hablar de lo que alguien vio.

**Lo que propondría mirar, y no he hecho:** un mentiroso que mienta **solo sobre
lo ajeno**, para medir el daño real sin el artefacto; y un premio de confianza
que pague por **informar**, no por acertar, para que decir «siguen donde estaban»
no gane lo mismo que decir la verdad.

**PARO AQUÍ.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`. Ficheros:
`confianza.py`, `banco_confianza.py`, `fig_P54A.py`, `P54A_nadie.json`,
`P54A_oraculo.json`, `P54A_mentiroso.json`, los tres progresos y
`figC/A6_confianza.png`.

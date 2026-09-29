# P5-6C · tanda 4 — Semillas 13 a 16

Con el sí de Manel. **Sin cotejar sellos: eso es al final, sobre las sesenta.**

**Veinticuatro diarios enteros, ningún freno, cero tics perdidos, 831 de 831
citas con parte y cero interrogantes en el acumulado.**

**La tanda 4 es la más pobre de las cuatro para F: una sola forma aceptada de
227 evaluadas.** No es un fallo —no hay reventones ni frenos—: la puerta
rechazó 128 por área y el consejero calló 98 veces.

**Y las dos medidas nuevas dan el contraste más fuerte de la serie**, con su
confuso declarado: las formas aceptadas de T coinciden casi siempre con una
bajada real de `d` (10 de 11) y las de F casi nunca (6 de 18).

---

## La tanda

Semillas **21517664, 21622393, 21727122, 21831851** (13 a 16), los tres brazos
con la misma semilla, una petición por episodio, creadas a las 03:48. **Cola
vacía antes y después.** Misma imagen `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`).

### El precio

| brazo | precios | **mediana** |
|---|---|---|
| **A** | 0,047449 · 0,048020 · 0,106589 · 0,123589 | **0,077304 $** |
| **F** | 0,051120 · 0,121209 · 0,123079 · 0,124949 | **0,122144 $** |
| **T** | 0,051046 · 0,052381 · 0,060365 · 0,120869 | **0,056373 $** |
| | | **total 1,030665 $** |

**Gasto acumulado: 124,859132 → 125,889797 $**, diferencia **1,030665 $**,
exacta. Cobrados 1.127 → 1.139: **los doce**. **Haiku por asiento:** mediana
**0,153430 $**, máximo **0,172876 $**. Los dos frenos, lejos.

### Tics lentos y perdidos

| brazo | tics vivos | > 40,5 ms | **perdidos** | vigía |
|---|---|---|---|---|
| A | 37.063 | 0 = 0,000 % | **0** | **0** |
| F | 66.330 | 120 = 0,181 % | **0** | **0** |
| T | 71.715 | 7 = 0,010 % | **0** | **0** |

**Acumulado t1–t4: cero tics perdidos en 774.714 tics vivos**, vigía sin
disparar en cuarenta y ocho partidas. F sigue clavado entre el 0,18 % y el
0,24 % en las cuatro tandas.

---

## C2 · La tanda 4

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 8 | **0** | 0 | **0** | 0 |
| **F** | 8 | 226 | 227 | **1** | 1 |
| **T** | 8 | 289 | 289 | **3** | 3 |

**Veredictos:** F área 128, calló 98, ok 1 · T área 276, vida 10, ok 3. **Cero
reventones.**

**El parte:** 230 de 230 con contenido, cero interrogantes. Callar: le
rechazaron 97/215 = 45,1 %, le aceptaron 1/3, sin previas 0/8.

**La medida principal:** F 2 puntos (1/2 cumplen) · T 5 puntos (2/5).

---

## Acumulado t1 + t2 + t3 + t4 (48 partidas, 96 asientos)

### Formas

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 32 | **0** | 0 | **0** | 0 |
| **F** | 32 | 815 | 841 | **21** | 14 |
| **T** | 32 | 1.188 | 1.188 | **16** | 15 |

**Aceptadas por vida: mediana 0,0 en los dos brazos.** F tiene 14 asientos con
al menos una (de 32), T tiene 12. **Cero reventones en 2.029 evaluaciones.**

**Veredictos:** F área 487, **calló 325**, ok 21, vida 8 · T área 1.142, vida 30,
ok 16.

### El parte

**831 de 831 citas con parte no vacío (100,0 %), cero interrogantes** en las
cuatro tandas.

| el parte decía | calla | de | **%** |
|---|---|---|---|
| le aceptaron la anterior | 14 | 25 | **56,0 %** |
| le rechazaron la anterior | 311 | 758 | **41,0 %** |
| sin formas previas | 0 | 32 | **0,0 %** |

Sigue la inversión que apareció en la tanda 3, con veinticinco citas en el caso
pequeño. **Lo único firme: nunca calla sin nada juzgado (0 de 32).**

### La medida principal

| | **F** | **T** |
|---|---|---|
| puntos de control | **31** (12 asientos) | **14** (9 asientos) |
| `d` real ≤ proyectada + 0,05 | 14/31 = **45,2 %** [29,2-62,2] | 9/14 = **64,3 %** [38,8-83,7] |
| comparables con A | 25 | 7 |
| `d` real por debajo de la de A | 9/25 = 36,0 % | 1/7 = 14,3 % |

**Diferencia F − T: −19,12 puntos [−44,25, +11,58], el cero dentro.**

### (a) La emparejada

Solo se comparan formas con el **mismo número de tramos** y la **misma banda**
de distancia al primer punto de control (0 = quedarse · 1 · 2-3 · 4+).

**Celdas con datos en los dos brazos: 5 de 13.**

| | F | T | diferencia |
|---|---|---|---|
| **emparejada** (solo celdas comparables) | 11/20 = 55,0 % | 8/12 = 66,7 % | **−11,67** [−40,19, +21,95] |

**Emparejar cuesta un tercio de los datos** —de 31 y 14 puntos a 20 y 12— y
**ocho celdas de trece no tienen pareja**. Eso es en sí un resultado: **el
consejero y el azar no construyen formas de la misma pinta**, así que la
comparación sin emparejar estaba comparando también dos repertorios distintos.
Emparejadas, la diferencia se reduce a la mitad (de −19,12 a −11,67) y sigue con
el cero dentro.

### (b) La magnitud

Bajada real de `d` desde el tic de aceptación hasta el último punto de control
alcanzado, contra la bajada del brazo A en la **misma ventana de tics**.

| | formas | **bajada mediana** | bajan de verdad | contra A |
|---|---|---|---|---|
| **F** | 18 | **+0,00000** | **6/18** | baja más que A en **3/14** |
| **T** | 11 | **+0,26099** | **10/11** | baja más que A en **4/6** |

**El contraste es el más fuerte de la serie, y hay que leerlo con cuidado.** Las
formas aceptadas de T coinciden casi siempre con una bajada real de `d`; las de
F, casi nunca —su mediana es exactamente cero—.

**El confuso, declarado:** esta medida es **lo que pasó en el mundo** durante esa
ventana, no lo que la forma causó. T acepta 16 de 1.188 evaluadas (1,3 %) y F
21 de 841 (2,5 %), así que T está siendo **mucho más selectivo por
construcción**: sus formas al azar solo pasan la puerta cuando la situación ya
apunta a mejorar. Y el brazo A, en las mismas ventanas, baja +0,13 de mediana
frente al +0,00 de las ventanas de F: **las ventanas no son comparables entre
brazos**, que es justo lo que la versión emparejada intenta arreglar y solo
consigue a medias.

### La regla de continuación

```
F: 31 puntos de control · cumplen 14/31 = 45.2 % [29.2-62.2]
T: 14 puntos de control · cumplen  9/14 = 64.3 % [38.8-83.7]
diferencia F - T: -19.12 puntos [-44.25, +11.58] · el cero DENTRO
--> con estos datos, la regla DISPARARIA la ampliacion
```

**Proyección a sesenta:** F ~39 puntos, T ~18. **Los dos por debajo de 40**, así
que la ampliación sigue siendo prácticamente segura.

---

## La ampliación, preparada y NO lanzada

**Las semillas 21 a 40 no estaban en el fichero:** `semillas_S2.json` tiene
exactamente veinte (k=0..19). Se generan con **el mismo generador declarado en
P5-1 A**, sin ninguna elección: `20260916 + k·104729`, k=20..39. En
`cantera/paper5/semillas_21_40.json`, md5 `6d4057f122b24241d6f6dcf01257ba53`.

`lanza_P56C_amp.py` reutiliza el cuerpo, el roster y las políticas de la serie:
**cinco tandas de cuatro semillas × dos brazos = ocho episodios cada una,
cuarenta en total. A no se amplía.** Coste previsto con las medianas medidas:
**unos 5,3 $**.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Imagen: `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`).
Roster: `roster_lento_v1.json` md5 `a2293bd16ee94e6d4c2f4683b57c2a09`.
Ficheros: `P56C_t4_peticiones.json`, los doce `P56C_t4_{brazo}_{semilla}.json`,
`P56C_t4_medidas.json`, `semillas_21_40.json`, `lanza_P56C_amp.py` y los
veinticuatro artefactos en `paintball/runs/P56C_t4_*/`.

**PARO AQUÍ.** La tanda 5 espera el sí.

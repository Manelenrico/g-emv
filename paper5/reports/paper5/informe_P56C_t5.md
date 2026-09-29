# P5-6C · tanda 5 — Semillas 17 a 20 · **LAS SESENTA, CERRADAS**

Con el sí de Manel. **Sin cotejar sellos: eso es al final, sobre todo lo jugado.**

**Sesenta partidas, ciento veinte asientos, ciento veinte diarios enteros, ningún
freno, cero tics perdidos en 962.396 tics vivos, 1.046 de 1.046 citas con parte y
cero interrogantes.** La máquina no ha fallado ni una vez en cinco tandas.

**La regla de continuación sellada el 21-sep DISPARA, por sus dos condiciones a la
vez.** F cierra con 34 puntos de control y T con 16; los dos por debajo de 40, y
el intervalo de la diferencia incluye el cero.

**PARO AQUÍ.** La ampliación F/T con las semillas 21 a 40 está preparada y **no
lanzada**: espera el sí para la primera tanda de ocho.

---

## La tanda

Semillas **21936580, 22041309, 22146038, 22250767** (17 a 20), los tres brazos con
la misma semilla, una petición por episodio, creadas entre las **04:27:43 y las
04:27:48**. **Cola vacía antes y después.** Misma imagen `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`).

### El precio

| brazo | precios | **mediana** |
|---|---|---|
| **A** | 0,037987 · 0,045473 · 0,054612 · 0,106970 | **0,050043 $** |
| **F** | 0,043616 · 0,107140 · 0,108840 · 0,108840 | **0,107990 $** |
| **T** | 0,046997 · 0,052979 · 0,095550 · 0,096600 | **0,074265 $** |
| | | **total 0,905604 $** |

**Gasto acumulado: 125,889797 → 126,795401 $**, diferencia **0,905604 $**, exacta.
Cobrados **1.139 → 1.151: los doce.** **Haiku por asiento:** mediana **0,152251 $**,
máximo **0,197352 $**, suma 1,076729 $. Los dos frenos, lejos. `/spend` cuadra con
la cabecera en los ocho asientos.

### El episodio sin facturar de la tanda 2, reconsultado

```
 "id": "ereq_90707b08-132b-45df-bf49-68ee0c91351e",
 "status": "completed", "running_at": "2026-09-20T21:44:38Z",
 "completed_at": "2026-09-20T21:54:58Z",
 "cost_usd": null, "error": null, "exit_code": null
```

**Siete horas después sigue sin precio.** Corrió los diez minutos normales, sin
error ni código de salida, y sus dos diarios están enteros. **No se descarta**: el
encargo manda descartar por diario perdido o por freno, y no es ninguna de las dos.
Es un fallo de facturación de la plataforma, no del episodio. Queda anotado: **de
los sesenta episodios, cincuenta y nueve están cobrados y uno no.**

### Tics lentos y perdidos

| brazo | tics vivos | > 40,5 ms | **perdidos** | vigía |
|---|---|---|---|---|
| A | 72.477 | 0 = 0,000 % | **0** | **0** |
| F | 60.035 | 136 = 0,227 % | **0** | **0** |
| T | 54.170 | 3 = 0,006 % | **0** | **0** |

---

## C2 · La tanda 5

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 8 | **0** | 0 | **0** | 0 |
| **F** | 8 | 208 | 222 | **2** | 2 |
| **T** | 8 | 219 | 219 | **4** | 4 |

**Veredictos:** F área 149, calló 71, ok 2 · T área 215, ok 4. **Cero reventones.**
Consejero: **cero fallos en 208 llamadas**, latencias medianas de 3.587 a 8.348 ms.

**El parte:** 215 de 215 con contenido, cero interrogantes.

**La medida principal:** F 3 puntos (2/3) · T 2 puntos (1/2).

---

# Las sesenta partidas · acumulado t1 a t5

**120 asientos · 120 diarios enteros · 0 frenos · 0 tics perdidos · 0 reventones.**

## Formas

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 40 | **0** | 0 | **0** | 0 |
| **F** | 40 | 1.023 | 1.063 | **23** | 16 |
| **T** | 40 | 1.407 | 1.407 | **20** | 19 |

**Veredictos:** F área 636, **calló 396**, ok 23, vida 8 · T área 1.357, vida 30,
ok 20. **Cero reventones en 2.470 evaluaciones.**

**Aceptadas por vida: mediana 0,0 en los dos brazos.** F tiene 15 asientos de 40
con al menos una; T, 15 también. **Edad de la primera aceptada:** F mediana 3.520
tics · T mediana 1.769.

La puerta honesta acepta **el 2,2 % de lo que evalúa en F y el 1,4 % en T**. Ese
es, en una línea, el motivo de que los puntos de control se hayan quedado en 34 y
16 después de sesenta partidas.

## El parte

**1.046 de 1.046 citas con parte no vacío (100,0 %), cero interrogantes** en las
cinco tandas. El arreglo de C1-bis ha aguantado 1.046 citas sin una sola recaída.

| el parte decía | calla | de | **%** |
|---|---|---|---|
| le aceptaron la anterior | 14 | 27 | **51,9 %** |
| le rechazaron la anterior | 382 | 956 | **40,0 %** |
| sin formas previas | 0 | 40 | **0,0 %** |

Con veintisiete citas en el caso pequeño sigo sin afirmar nada sobre las dos
primeras filas. **Lo único firme en las cinco tandas: nunca calla cuando aún no
tiene nada juzgado, 0 de 40.**

## Tics lentos y perdidos

| brazo | tics vivos | > 40,5 ms | **perdidos** | vigía |
|---|---|---|---|---|
| A | 323.490 | 0 = 0,000 % | **0** | **0** |
| F | 291.091 | 623 = **0,214 %** | **0** | **0** |
| T | 347.815 | 22 = 0,006 % | **0** | **0** |

**Cero tics perdidos en 962.396 tics vivos**, vigía sin disparar en sesenta
partidas. La cifra de F se ha mantenido entre el 0,18 % y el 0,24 % en las cinco
tandas: **es un coste estructural estable, no una deriva, y no cuesta decisiones.**

## La medida principal

| | **F** | **T** |
|---|---|---|
| puntos de control | **34** (13 asientos) | **16** (11 asientos) |
| `d` real ≤ proyectada + 0,05 | 16/34 = **47,1 %** [31,5-63,3] | 10/16 = **62,5 %** [38,6-81,5] |
| comparables con A | 28 | 9 |
| `d` real por debajo de la de A | 10/28 = 35,7 % | 1/9 = 11,1 % |
| diferencia (real − A), mediana | +0,19786 | +0,08982 |

**Diferencia F − T: −15,44 puntos [−40,04, +13,40], el cero dentro.**

## (a) La emparejada

Mismo número de tramos y misma banda de distancia al primer punto de control.

**Celdas con datos en los dos brazos: 6 de 14.**

| celda | F | T | dif |
|---|---|---|---|
| 2 tramos · quedarse | 1/2 | 2/2 | −50,0 |
| 2 tramos · banda 1 | 2/2 | 1/1 | +0,0 |
| 3 tramos · quedarse | 2/4 | 0/1 | +50,0 |
| 3 tramos · banda 1 | 4/11 | 3/4 | −38,6 |
| 3 tramos · banda 2-3 | 1/3 | 2/3 | −33,3 |
| 4 tramos · quedarse | 5/5 | 1/3 | +66,7 |
| **total emparejado** | **15/27 = 55,6 %** | **9/14 = 64,3 %** | **−8,73** [−35,34, +21,86] |

Emparejar cuesta siete puntos de F y dos de T, y **ocho celdas de catorce siguen
sin pareja**. Eso sostiene lo que ya dije en la tanda 4: **el consejero y el azar
no construyen formas de la misma pinta.** Emparejadas, la diferencia baja de
−15,44 a −8,73 y sigue con el cero dentro.

## (b) La magnitud

| | formas | **bajada mediana** | bajan de verdad | baja más que A |
|---|---|---|---|---|
| **F** | 20 | **+0,00000** | 7/20 | 4/16 |
| **T** | 13 | **+0,26099** | **11/13** | 5/8 |

**El confuso, declarado y sin cambios:** esto es **lo que pasó en el mundo** en esa
ventana, no lo que la forma causó. T acepta 20 de 1.407 (1,4 %) y F 23 de 1.063
(2,2 %): T está siendo más selectivo por construcción, y A baja +0,13 de mediana en
las ventanas de T frente a +0,00 en las de F. **Las ventanas no son comparables
entre brazos.**

---

## (c) y (d), adelantadas sobre las sesenta

El encargo las pide **para el cierre final sobre cien partidas**. Están construidas
y corridas ya, para que lleguen probadas: **estas cifras son preliminares** y se
recalcularán sobre todo lo jugado.

### (c) La magnitud en las formas rechazadas por área

Una forma rechazada nunca vivió, así que **no tiene puntos de control ni horizonte
propio en el diario**: `forma_evaluada` guarda el veredicto y el número de tramos,
no los tics. **La ventana se declara:** `L = 22` tics, la mediana del tramo que
duraron las 33 formas aceptadas de los dos brazos juntos. Con esa misma `L` se
recalculan también las aceptadas, para que las dos filas sean comparables.

| brazo | | n | el propio brazo | **A en la misma ventana** |
|---|---|---|---|---|
| **F** | rechazadas por área | 636 | +0,00000 · baja 27,8 % | **+0,00000 · baja 20,8 %** |
| **F** | aceptadas (misma L) | 23 | −0,02127 · baja 30,4 % | +0,00000 · baja 22,2 % |
| **T** | rechazadas por área | 1.357 | +0,00000 · baja 30,0 % | **+0,00000 · baja 22,2 %** |
| **T** | aceptadas (misma L) | 20 | +0,01418 · baja 55,0 % | +0,02539 · baja 57,1 % |

**La lectura, con 1.993 rechazos: la puerta de área no está tirando momentos
buenos.** En las ventanas que rechaza, el brazo A —que no tiene ni puerta ni
forma— tampoco baja: mediana exactamente cero, y solo uno de cada cinco baja algo.
**Son ventanas planas para todo el mundo.** El contraste de (b) entre F y T
reaparece aquí en las aceptadas, con el mismo confuso.

### (d) Las formas de F según hubiera forma contada del hermano

«Fresca» = un `hilo_forma` oído con `tramos > 0` en los **150 tics** anteriores a la
evaluación, que es exactamente el plazo con el que la propia política la da por
fresca (`policy_forma.py:82,532`).

| | evaluadas | aceptadas | área | calló | puntos |
|---|---|---|---|---|---|
| **CON** forma del hermano | **3** | 0 | 2 | 1 | 0/0 |
| **SIN** forma del hermano | 1.060 | 23 = 2,2 % | 634 | 395 | 16/34 |

Diferencia −2,17 puntos [−3,23, +53,99]: **no dice nada, y no puede decirlo.**

**El resultado es la propia escasez, y es un resultado.** En las cuarenta partidas
de F, el hilo llevó forma **13 veces de 4.830 envíos**, y solo **tres** evaluaciones
cayeron dentro de la ventana de una. Es consecuencia directa de la tasa de
aceptación: si un hermano acepta una forma cada varias partidas, **casi nunca tiene
forma que contar**. El canal horizontal está montado, medido y funciona —el humo
(c) lo prueba con ida y vuelta idéntica—, pero **en este régimen prácticamente no
se enciende**. La ampliación no va a cambiarlo: no toca la puerta.

---

## Vida

| brazo | vida mediana | calma literal |
|---|---|---|
| A | 8.348,5 | **0** |
| F | **8.131,0** | **0** |
| T | 8.728,5 | **0** |

Calma literal **cero en los ciento veinte asientos** de la serie.

---

## LA REGLA DE CONTINUACIÓN, EVALUADA

Sellada por la mesa el 21-sep antes de ver la tanda 3, con sus dos condiciones:

```
F: 34 puntos de control · cumplen 16/34 = 47.1 % [31.5-63.3]
T: 16 puntos de control · cumplen 10/16 = 62.5 % [38.6-81.5]
diferencia F - T: -15.44 puntos [-40.04, +13.40] · el cero DENTRO
```

| condición sellada | | veredicto |
|---|---|---|
| **(1)** menos de 40 puntos de control en F **o** en T | F 34 · T 16, **los dos** | **SE CUMPLE** |
| **(2)** el intervalo de la diferencia incluye el cero con menos de 40 | cero dentro · mín(34,16)=16 | **SE CUMPLE** |

**Las dos condiciones se cumplen. LA REGLA DISPARA.** Se amplían F y T con las
semillas 21 a 40; **A no se amplía**, como manda el sello.

La proyección de la tanda 3 (F ~48, T ~15) se quedó alta para F y clavada para T:
el ritmo real fue de 34 y 16.

---

## La ampliación, preparada y NO lanzada

- **Semillas 21 a 40**: `cantera/paper5/semillas_21_40.json`, md5
  `6d4057f122b24241d6f6dcf01257ba53`, generadas con el generador declarado en
  P5-1 A, `20260916 + k·104729`, k=20..39, sin ninguna elección.
- **Misma imagen** `gemv-anima:forma-c1bis`, **mismas políticas**
  `gemv-p56c2-{F,T}:v1`, **mismo roster** `roster_lento_v1.json`.
- **`lanza_P56C_amp.py`**: **cinco tandas de cuatro semillas × dos brazos = ocho
  episodios cada una, cuarenta en total.**
- **Coste previsto** con las medianas medidas sobre las sesenta (F 0,066052 $, T
  0,066555 $): **unos 2,65 $** en total, más el Haiku de F.
- **Duración estimada**: unos **11-12 minutos por tanda** (las cinco tandas de doce
  tardaron entre 10 y 12), más 3-4 minutos de bajada de artefactos.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Imagen: `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`).
Roster: `roster_lento_v1.json` md5 `a2293bd16ee94e6d4c2f4683b57c2a09`.
Políticas `gemv-p56c2-{A,F,T}:v1`.
Ficheros: `P56C_t5_peticiones.json`, los doce `P56C_t5_{brazo}_{semilla}.json`,
`P56C_t5_medidas.json`, `P56C_t1_2_3_4_5_medidas.json`, y los veinticuatro
artefactos en `paintball/runs/P56C_t5_*/`.

**PARO AQUÍ.** La primera tanda de ampliación (ocho episodios, semillas 21 a 24,
brazos F y T) espera el sí.

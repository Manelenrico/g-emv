# P5-6C · tanda 1 — Doce episodios, cuatro semillas, tres brazos

Con el sí de Manel. **Sin cotejar sellos: eso es al final, sobre las sesenta.**

**Los doce salieron, los veinticuatro diarios llegaron enteros, ningún freno
mordió y `/spend` cuadró con la cabecera en los ocho asientos de F.**
**1,027852 $** la tanda.

**Y salen dos defectos que hay que poner delante**, uno ya avisado y otro nuevo:
el parte que recibe el consejero va **mudo**, y una de cada 176 evaluaciones
**revienta con `RuntimeError`** por una carrera entre el hilo y el bucle.

---

## La tanda

Semillas 1 a 4 de `semillas_S2.json` —**20260916, 20365645, 20470374,
20575103**—, los tres brazos con la misma semilla, **una petición por
episodio**, creadas entre las 20:51:15 y las 20:51:20. **Cola vacía antes.**

Las tres políticas salen de la misma imagen, `gemv-anima:forma-c0`
(`sha256:f7c0ffb3b5213e70714337ee036056abe28a89bc39931f897cb99d3a1156b846`):
`gemv-p56c-A:v1` (`c4efd945…`), `gemv-p56c-F:v1` (`f4a54db0…`) y
`gemv-p56c-T:v1` (`0868e4d7…`).

### El precio

| brazo | episodios | precios | **mediana** |
|---|---|---|---|
| **A** | 4 | 0,061111 · 0,063679 · 0,090625 · 0,111974 | **0,077152 $** |
| **F** | 4 | 0,062198 · 0,063185 · 0,108574 · 0,114524 | **0,085879 $** |
| **T** | 4 | 0,042410 · 0,098714 · 0,100074 · 0,110784 | **0,099394 $** |
| | | | **total 1,027852 $** |

**Ninguno pasa de 0,20 $**, que es tu freno. Pero el precio **ha subido mucho al
lanzar doce a la vez**: las medianas de 0,077 a 0,099 contra los 0,033 a 0,052
de las partidas sueltas de P5-6B. Es el efecto ya medido en P5-1, que el precio
sigue a la vida del pod y no a la partida: con doce a la vez, los pods esperan.

**El gasto de Haiku por asiento** (los ocho de F):

```
0,007807 · 0,009346 · 0,077781 · 0,088832 · 0,145520 · 0,160090 · 0,171383 · 0,222170
mediana 0,117176 $ · máximo 0,222170 $ · suma 0,882929 $
```

**Ninguno pasa de 0,50 $**, que es tu otro freno. El máximo, 0,222 $, es del
asiento que más vivió (12.456 tics, 48 citas).

**Gasto acumulado: 121,428580 $ antes → 122,456432 $ después.** La diferencia,
1,027852 $, es exactamente la suma de los doce. Cola vacía otra vez.

---

## C2 · Las medidas

### Diarios y frenos

**Los veinticuatro diarios están enteros**: los veinticuatro traen su registro
`final` y en los veinticuatro `match_ticks` es exactamente el último tic vivo
más uno. **Ningún freno mordió** en ningún asiento. **Nada que descartar.**

Las vidas van de **321 a 14.352 tics**, y eso es real, no truncamiento: la
semilla 20575103 mata pronto a casi todos (A/10 vivió 365 tics, F/10 602, F/11
647, T/11 321), mientras que la 20365645 y la 20470374 dan partidas largas.

**Dos asientos de T llegaron al final de la partida** (`match_over`, puesto
**2**): T/20365645/10 con 14.318 tics y T/20470374/11 con 14.352. Ningún asiento
de A ni de F pasó del puesto 7.

### Formas

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 8 | **0** | 0 | **0** | 0 |
| **F** | 8 | 175 | 176 | **5** | 4 |
| **T** | 8 | 336 | 336 | **2** | 0 |

**Aceptadas por vida:** F `[0,0,0,0,1,1,1,2]`, **mediana 0,5**; T
`[0,0,0,0,0,0,1,1]`, **mediana 0,0**.

**Edad de la primera aceptada** (tics desde el primer instante de vida): F
`[2457, 2486, 2649, 2735]`, mediana **2.567**; T `[4019, 13269]`, mediana 8.644.

**Veredictos:**

| | F | T |
|---|---|---|
| rechazada por **área** | 88 | **330** |
| **el consejero calló** | **82** | — |
| **ok** (aceptada) | 5 | 2 |
| rechazada por vida mínima | 0 | 4 |
| **revienta: `RuntimeError`** | **1** | 0 |

**Motivos de caída**, los cuatro de F: «en la reevaluación deja de ganar
(área)». Ninguna cayó por vida ni por destino inalcanzable.

**A no produjo un solo registro de forma**, como debe.

### El consejero, en F

| semilla/asiento | citas | fallos | saltadas | latencia mediana | **callar** | `/spend` | cuadra |
|---|---|---|---|---|---|---|---|
| 20260916/10 | 26 | **0** | 5 | 7.644 ms | 14/26 = **54 %** | 0,1455205 | **sí** |
| 20260916/11 | 31 | **0** | 1 | 7.499 ms | 13/31 = 42 % | 0,1713835 | **sí** |
| 20365645/10 | 16 | **0** | 2 | 7.210 ms | 7/16 = 44 % | 0,0777810 | **sí** |
| 20365645/11 | 18 | **0** | 0 | 6.971 ms | 10/18 = **56 %** | 0,0888320 | **sí** |
| 20470374/10 | 48 | **0** | 2 | 7.177 ms | 25/48 = 52 % | 0,2221700 | **sí** |
| 20470374/11 | 32 | **0** | 0 | 7.301 ms | 14/32 = 44 % | 0,1600900 | **sí** |
| 20575103/10 | 2 | **0** | 0 | 5.752 ms | 0/2 | 0,0093460 | **sí** |
| 20575103/11 | 2 | **0** | 0 | 3.695 ms | 0/2 | 0,0078070 | **sí** |

**Cero fallos en 175 llamadas**, contra el 36 % de timeouts del brazo F de
P5-6B: los valores definitivos de C0 hacen lo que tenían que hacer. Las citas
saltadas bajan a 0-5 por asiento.

**Callar sigue alto: del 42 % al 56 %** en los seis asientos con suficientes
citas. Los dos asientos de la semilla corta no callaron ni una vez, pero solo
tuvieron dos citas cada uno.

### La medida principal: lo que pasó después de aceptar

Para cada punto de control alcanzado, la `d` real contra la proyectada, y contra
la `d` que el brazo A tuvo **en la misma semilla, el mismo asiento y ±50 tics**.

| | **F** | **T** |
|---|---|---|
| puntos de control alcanzados | **5** (en 3 asientos) | **5** (en 2 asientos) |
| `d` real ≤ proyectada + 0,05 | 3/5 = **60,0 %** | 3/5 = **60,0 %** |
| comparables con A | 2 | 3 |
| `d` real **por debajo** de la de A | **0/2 = 0 %** | **0/3 = 0 %** |
| diferencia (real − A), mediana | **+1,02103** | **+0,68102** |

**La n es minúscula y no se puede concluir nada**, y así lo digo. Lo único que
se puede leer es que con cinco puntos por brazo **no hay diferencia visible
entre F y T** en cumplir lo proyectado, y que en los cinco casos comparables la
`d` real quedó **por encima** de la de A en la misma zona del tiempo. Con
sesenta partidas habrá entre diez y quince veces más puntos.

### Confianza

| asiento | trayectoria de C |
|---|---|
| F/20260916/11 | 0,30 → **0,40** |
| F/20365645/10 | 0,30 → **0,15** |
| F/20470374/10 | 0,30 → 0,15 → 0,25 → **0,35** |
| T/20260916/11 | 0,30 → 0,40 → 0,50 → **0,35** |
| T/20365645/10 | 0,30 → 0,40 → **0,25** |

Los otros diecinueve asientos no alcanzaron ningún punto de control, así que su
C se quedó en el 0,30 de partida. **El cuerpo no calló al consejero ni una
vez**: hacen falta cinco formas aceptadas y mal cumplidas, y el máximo por
asiento fue dos.

### El hilo

Los dichos y oídos cuadran salvo cuando el hermano muere antes, que es lo
esperable:

| asiento | dichos | oídos | con forma |
|---|---|---|---|
| F/20260916/10 | 164 | **164** | 0 |
| F/20470374/11 | 170 | **170** | 0 |
| T/20260916/10 | 188 | 186 | 0 |
| **T/20575103/10** | **238** | **7** | 0 | 

El caso de `T/20575103/10` no es un fallo: su hermano murió en el tic 801, así
que dejó de hablar. **Ningún mensaje pasó de los 120 ASCII en ningún asiento.**

**`con forma` sigue casi siempre en cero**, por la misma razón de P5-6B: casi
nunca hay una forma viva en el instante de hablar.

### Vida y tiempo

| brazo | vidas (tics) | mediana | puestos |
|---|---|---|---|
| **A** | 365 · 1.833 · 3.499 · 7.693 · 7.751 · 7.769 · 10.128 · 11.832 | **7.722** | 11-16 |
| **F** | 602 · 647 · 4.569 · 4.627 · 7.863 · 7.977 · 8.153 · 12.456 | **7.920** | 7-16 |
| **T** | 321 · 9.018 · 9.148 · 11.396 · 11.880 · 12.552 · 14.318 · 14.352 | **11.638** | **2**-16 |

**Tiempo por tic:** mediana entre 0,57 y 2,98 ms; máximos entre 15,8 y
258,0 ms. La evaluación sigue yéndose al hilo casi siempre.

**Calma literal: cero** en los veinticuatro asientos.

---

## Los dos defectos

### 1. El parte va mudo (ya avisado)

`forma.curva_H` devuelve por punto de control `tic`, `d`, `vida`, `W` y `pos`,
**pero no las necesidades**, así que `_detalle` no puede rellenar «lo que el
cuerpo proyectó» y escribe `?`. Y «lo que el cuerpo sintió de verdad» tampoco se
rellena nunca. El parte real del diario:

```
- Forma 1 (4 tramos): RECHAZADA por area.
  Tramo 1: dijiste vida 0, manos 0, vinculo 0 por F-4-ALCANCE;
           el cuerpo proyecto vida ?, manos ?, vinculo ?;
           ese tramo no llego a vivirse.
```

**El consejero recibe solo lo que él mismo dijo.** La coherencia de C2 sí se
puede medir fuera de línea —`forma_propuesta` guarda el texto crudo del modelo y
los diarios tienen las observaciones—, pero **S4 nombra un mecanismo que no está
corriendo**, y por eso no la he calculado todavía: depende de qué decidas.

### 2. Una carrera entre el hilo y el bucle (nuevo)

```
{"k": "forma_evaluada", "tick": 1076, "id": 2, "veredicto": "revienta: RuntimeError",
 "ms": 63.55, "tramos": 3, "en_hilo": true}
```

**Una de 176 evaluaciones (0,6 %).** La causa está clara: `_juzga` le pasa al
hilo `self.mem` y `self.bloqueos`, que el bucle del juego **sigue mutando** cada
tic (`mem.observa`). Un `RuntimeError` en ese contexto es el clásico
«dictionary changed size during iteration».

**Degrada con elegancia** —`FV.evalua` lo captura, la forma se rechaza y la
partida sigue—, pero **sesga**: las formas que revientan se cuentan como
rechazadas sin haber sido juzgadas. Con 0,6 % da igual; si creciera, no. Se
arregla pasando al hilo una **copia** de la memoria y los bloqueos, como ya hace
`D.candidatos`.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Imagen: `gemv-anima:forma-c0`
(`sha256:f7c0ffb3b5213e70714337ee036056abe28a89bc39931f897cb99d3a1156b846`).
Roster: `roster_lento_v1.json`, md5 `a2293bd16ee94e6d4c2f4683b57c2a09`.
Ficheros: `lanza_P56C.py`, `baja_P56C.py`, `analiza_P56C.py`,
`P56C_t1_peticiones.json`, los doce `P56C_t1_{brazo}_{semilla}.json`,
`P56C_t1_medidas.json`, y los veinticuatro artefactos en
`paintball/runs/P56C_t1_*/`.

**PARO AQUÍ.** La tanda 2 espera el sí, y antes hay que decidir qué se hace con
el parte mudo y con la carrera del hilo.

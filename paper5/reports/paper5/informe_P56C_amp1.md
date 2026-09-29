# P5-6C · ampliación, tanda 1 — Semillas 21 a 24 (solo F y T)

Con el sí de Manel, después de que la regla de continuación sellada disparase por
sus dos condiciones. **Sin cotejar sellos: eso es al final, sobre las cien.**

**Dieciséis diarios enteros, ningún freno, cero tics perdidos, 240 de 240 citas con
parte y cero interrogantes.**

**La tanda más rica de F de toda la serie: nueve formas aceptadas en ocho asientos**,
frente a veintitrés en los cuarenta anteriores. Con ellas **F cruza los 40 puntos de
control** (va por 50) y la medida principal se estabiliza en el 48,0 %.

**T se ha quedado corto en esta tanda**: 150 propuestas y solo 2 aceptadas.

---

## La tanda

Semillas **22355496, 22460225, 22564954, 22669683** (21 a 24 de
`semillas_21_40.json`, md5 `6d4057f122b24241d6f6dcf01257ba53`), **brazos F y T; A
no se amplía**, como manda el sello. Una petición por episodio. **Cola vacía antes
y después.** Misma imagen `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`), mismas
políticas `gemv-p56c2-{F,T}:v1`, mismo roster `roster_lento_v1.json`
(md5 `a2293bd16ee94e6d4c2f4683b57c2a09`).

### El precio, y el segundo episodio sin facturar

| brazo | precios | **mediana** |
|---|---|---|
| **F** | 0,051283 · 0,099741 · 0,111712 · **(sin facturar)** | **0,099741 $** |
| **T** | 0,052920 · 0,089031 · 0,106371 · 0,111882 | **0,097701 $** |
| | | **total cobrado 0,622940 $** |

**Gasto acumulado: 126,795401 → 127,418341 $**, diferencia **0,622940 $**, exacta.
Cobrados **1.151 → 1.158: siete, no ocho.**

**El episodio sin facturar es `ereq_26eb8c79` (F, semilla 22564954).** Corrió y
cerró bien —sus dos diarios están enteros y cierran— pero la plataforma no le ha
puesto precio. **Es el segundo caso de la serie**, después de `ereq_90707b08` (F,
20679832) de la tanda 2, que sigue en `null`. **Van dos de 68 episodios, los dos en
F**; con 48 de los 68 episodios en F eso es lo que cabría esperar por azar, así que
**no lo leo como un patrón**. Ninguno se descarta: el encargo manda descartar por
diario perdido o por freno, y no es ninguna de las dos.

**Haiku por asiento:** mediana **0,144176 $**, máximo **0,241703 $**, suma
1,171177 $. **`/spend` cuadra con la cabecera en los ocho asientos.** Los dos frenos
(200 llamadas, 1,00 $) siguen lejos.

### Tics lentos y perdidos

| brazo | tics vivos | > 40,5 ms | **perdidos** | vigía |
|---|---|---|---|---|
| F | 67.763 | 142 = 0,210 % | **0** | **0** |
| T | 36.748 | 2 = 0,005 % | **0** | **0** |

F sigue clavado en su 0,21 %, la sexta tanda seguida entre 0,18 % y 0,24 %.

---

## C2 · La ampliación, tanda 1

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **F** | 8 | 235 | 243 | **9** | 5 |
| **T** | 8 | 150 | 150 | **2** | 2 |

**Veredictos:** F área 125, calló 104, vida 5, ok 9 · T área 146, vida 2, ok 2.
**Cero reventones.** Consejero: **cero fallos en 235 llamadas**.

**Aceptadas por vida:** F `[0,0,0,0,1,1,3,4]` **mediana 0,5** —la mejor de toda la
serie— · T `[0,0,0,0,0,0,1,1]` mediana 0,0.

**El parte:** 240 de 240 con contenido, cero interrogantes.

**La medida principal:** F **16 puntos** (8/16 = 50,0 %) · T 2 puntos (1/2).

**Aviso de lectura:** dos de los cuatro asientos de T y uno de F murieron muy pronto
(439, 1.203 y 459 tics), lo que explica la sequía de T en esta tanda. **La vida
mediana de T cae a 2.540 tics contra 8.268 de F**, la separación más grande vista
entre los dos brazos en una tanda. Con cuatro semillas eso es ruido de reparto, no
un efecto; se diluirá en las cinco tandas.

---

# Acumulado: 68 partidas · 136 asientos

**136 diarios enteros · 0 frenos · 0 reventones en 2.863 evaluaciones · 0 tics
perdidos · 1.286 de 1.286 citas con parte y cero interrogantes.**

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 40 | **0** | 0 | **0** | 0 |
| **F** | 48 | 1.258 | 1.306 | **32** | 21 |
| **T** | 48 | 1.557 | 1.557 | **22** | 21 |

**Veredictos:** F área 761, calló 500, ok 32, vida 13 · T área 1.503, vida 32, ok 22.

### El parte

| el parte decía | calla | de | **%** |
|---|---|---|---|
| le aceptaron la anterior | 22 | 43 | **51,2 %** |
| le rechazaron la anterior | 479 | 1.167 | **41,0 %** |
| sin formas previas | 0 | 48 | **0,0 %** |

**Nunca calla sin nada juzgado: 0 de 48.** Sigue siendo lo único firme.

### La medida principal

| | **F** | **T** |
|---|---|---|
| puntos de control | **50** (16 asientos) | **18** (13 asientos) |
| `d` real ≤ proyectada + 0,05 | 24/50 = **48,0 %** [34,8-61,5] | 11/18 = **61,1 %** [38,6-79,7] |

**Diferencia F − T: −13,11 puntos [−35,91, +13,12], el cero dentro.**

**F ha cruzado el umbral de 40 puntos** que la regla sellada usaba como criterio de
suficiencia; **T sigue en 18** y es el que manda ahora.

La comparación contra A **deja de crecer aquí**, y hay que decirlo: la ampliación no
lleva brazo A, así que las columnas «por debajo de la de A» se quedan congeladas en
los 28 y 9 puntos de las sesenta. Es consecuencia directa del sello («A no se
amplía»), no un descuido.

### (a) La emparejada

**6 celdas de 15 con datos en los dos brazos.** F **19/35 = 54,3 %** · T
**10/16 = 62,5 %** · **diferencia −8,21 [−33,13, +20,10]**. La brecha emparejada
apenas se mueve (era −8,73 sobre las sesenta) y el cero sigue dentro.

### (b) La magnitud

| | formas | bajada mediana | bajan de verdad |
|---|---|---|---|
| **F** | 28 | **+0,00000** | 10/28 |
| **T** | 15 | **+0,11028** | **12/15** |

La mediana de T baja de +0,26099 a +0,11028 al añadir dos formas: **la cifra era
frágil, como avisaba la n**. El sentido del contraste se mantiene.

### (c) Rechazadas por área

**La ventana declarada se recalcula sobre las 43 aceptadas: `L = 19` tics** (era 22
con 33 formas). Es una constante derivada de los datos, así que se mueve; queda
anotado para que el cierre use la de las cien.

| brazo | | n | el propio brazo | **A en la misma ventana** |
|---|---|---|---|---|
| **F** | rechazadas por área | 761 | +0,00000 · baja 35,1 % | **+0,00000 · baja 29,6 %** |
| **T** | rechazadas por área | 1.503 | +0,00000 · baja 33,8 % | **+0,00000 · baja 31,0 %** |

**El hallazgo aguanta con 2.264 rechazos: en lo que la puerta de área rechaza, el
brazo A tampoco baja.** Son ventanas planas para todo el mundo.

### (d) Formas del hermano

**18 formas oídas con tramos en los 48 asientos de F** (eran 13 en 40). **CON: 6
evaluadas, 0 aceptadas. SIN: 1.300 evaluadas, 32 aceptadas (2,5 %).** Diferencia
−2,46 [−3,45, +36,58]: **sigue sin decir nada.** El canal horizontal se enciende
ahora seis veces en vez de tres; con ese ritmo, las cien no van a darle n.

---

## Las figuras F4 y F5, construidas

En `cantera/paper5/figF/`, regeneradas sobre las 68:

- **`F4_aceptadas_curva.png`** — (a) el embudo por brazo, con el cero de A, y (b)
  cada punto de control con la `d` proyectada contra la real, la diagonal y la banda
  de 0,05. **Anotado en la propia figura:** a la escala real de `d` (2,5 a 6,2) **la
  banda de 0,05 es casi invisible**, así que «cumple» es prácticamente «en la línea
  o por debajo».
- **`F5_confianza_vida.png`** — C a lo largo de los tics, un trazo por asiento,
  leída de `forma_evaluada.C`, que el diario escribe en **cada** evaluación.

**El script imprime el embudo que dibuja y cuadra con el analizador** (F
1.258/1.306/32, T 1.557/1.557/22, 50 y 18 puntos): las figuras leen los diarios, no
una copia a mano.

### Lo que F5 ha sacado, y no estaba en ninguna tabla

| | mediana | mín | **evaluaciones con C = 0** |
|---|---|---|---|
| **F** (667 evaluaciones, sobre las 60) | 0,30 | **0,00** | **28 = 4,2 %** |
| **T** (1.407) | 0,30 | 0,10 | **0 = 0,0 %** |

**La confianza de F se desploma a cero en varios asientos; la de T no baja nunca de
0,10.** Tiene sentido mecánico —C se mueve con el resultado de las formas
aceptadas—, pero no estaba medido.

**Y con ello: el silenciador no se ha disparado ni una vez.** Cero sucesos «el
cuerpo calla al consejero» y cero citas saltadas por ese motivo en toda la serie.
Hace falta C ≤ 0 **y** cinco formas aceptadas que acaben mal **en el mismo asiento**,
y F lleva 21 caídas repartidas entre 48 asientos. **Es el mismo patrón que (d): el
mecanismo está montado, pasa su humo, y el régimen nunca lo alcanza.**

---

## Un arreglo en el analizador

`analiza_P56C.py` reventaba en la sección VIDA al correrse **sobre la ampliación a
solas**: el brazo A no tiene asientos ahí y `statistics.median([])` lanza. No
afectaba a ninguna cifra publicada —el acumulado sí lleva A— pero impedía escribir
`P56C_tamp1_medidas.json`. Arreglado saltando el brazo vacío; el fichero ya está.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Imagen: `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`).
Roster: `roster_lento_v1.json` md5 `a2293bd16ee94e6d4c2f4683b57c2a09`.
Ficheros: `P56C_amp1_peticiones.json`, los ocho
`P56C_tamp1_{brazo}_{semilla}.json`, `P56C_tamp1_medidas.json`,
`P56C_t1_2_3_4_5_amp1_medidas.json`, `fig_P56C.py`, `figF/F4_*.png`,
`figF/F5_*.png`, y los dieciséis artefactos en `paintball/runs/P56C_tamp1_*/`.

**PARO AQUÍ.** La tanda 2 de ampliación (semillas 25 a 28, F y T) espera el sí.

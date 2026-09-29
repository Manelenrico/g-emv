# P5-6C — LA SERIE VIVA · informe final

**Cien partidas de cien, cerradas.** 20 semillas x 3 brazos (60) mas la
ampliacion sellada de 20 semillas x 2 brazos (40). Una sola imagen en las diez
tandas, ni un cambio de codigo entre la primera partida y la ultima.


## El titular

**La puerta honesta aguanta; el consejero no bate al azar.**

En 100 partidas y 200 asientos, la política con formas **no perdió un solo tic**
(1.501.210 tics vivos), no mordió un freno, no reventó una evaluación en 4.548 y
entregó el parte con contenido en **2.088 de 2.088 citas**. La máquina funciona.

Lo que no aparece es la ventaja. **Las formas del consejero cumplen su propia
proyección en el 42,3 % de los puntos de control y las formas al azar que pasan
la misma puerta en el 61,1 %**; la diferencia es **−18,80 puntos [−36,30,
+0,86]**, con el cero dentro. **Emparejando por forma la brecha cae a −12,50**, y
también incluye el cero.

**De los ocho sellos, dos cumplen, cinco fallan y uno depende de cómo se lea.**

---

## Cotejo de las predicciones selladas (mesa, 20-sep-2026)

| | sello | contador | veredicto |
|---|---|---|---|
| **S1** | F acepta más formas por vida que T (mediana), y **ambas por encima de cero** | mediana F **0,0** · T **0,0** · dif 0,0 [0,0, 0,0] · medias 0,650 y 0,512 · totales 52 y 41 | **FALLA** |
| **S2** | la `d` real ≤ proyectada + 0,05 en **más de la mitad de las formas de F** y en **menos de la mitad de las de T** | ver abajo | **FALLA** |
| **S3** | C final: mediana de F por encima de T, y T por debajo de 0,30 | mediana F **0,30** · T **0,30** (n=80 y 80) | **FALLA** |
| **S4** | la coherencia de signos en F sube >10 puntos de la primera a la segunda mitad de la vida | 46,5 % (11.653/25.074) → **46,1 %** (11.292/24.519) · **−0,4** | **FALLA** |
| **S5** | F calla en >30 % de las citas, y calla más con C baja | **40,8 %** (834/2.042) · C<0,30 **53,7 %** · C≥0,30 **40,3 %** | **CUMPLE** |
| **S6** | ningún brazo mueve puesto ni vida más allá del ruido | F−A, T−A y F−T: **el cero dentro en las seis comparaciones** | **CUMPLE** |
| **S7** | ninguna forma aceptada cruza el mínimo de vida proyectado: **cero** | **F 0 · T 1** | **FALLA** |
| **S8** | gasto total de la serie por debajo de 15 $ | plataforma **7,87 $** · Haiku **10,48 $** · suma **18,35 $** | **depende de la lectura** |

### S2, en su propia redacción

El sello habla de **formas**, no de puntos de control. Los informes de tanda
venían dando la cifra por punto; aquí va como se selló, con la otra al lado:

| | aceptadas | llegaron a algún punto | **cumplen TODOS sus puntos** | cumplen la mayoría | *(por punto)* |
|---|---|---|---|---|---|
| **F** | 52 | 43 | **16/43 = 37,2 %** | 17/43 = 39,5 % | *33/78 = 42,3 %* |
| **T** | 41 | 29 | **18/29 = 62,1 %** | 18/29 = 62,1 % | *22/36 = 61,1 %* |

**F no llega a la mitad (pedía más) y T la pasa (pedía menos): falla por las dos
cláusulas**, y falla igual con cualquiera de las tres varas. La dirección es la
contraria a la sellada.

### S7, con los dos motivos separados

El sello pregunta por **la vida real cruzando el mínimo proyectado**
(`forma_viva.py:14`). Hay otro motivo de caída que se le parece y **no es lo
mismo**: que la puerta vuelva a rechazar por vida en la reevaluación.

| | vida real cruza el mínimo *(esto es S7)* | la puerta re-rechaza por vida |
|---|---|---|
| **F** | **0** | 1 |
| **T** | **1** | 0 |

Una sola forma en 93 aceptadas. **S7 falla, y falla por uno.**

### S8, y la ambigüedad que no voy a resolver yo

«Gasto total de la serie» admite dos lecturas y **dan veredictos opuestos**:

| lectura | importe | contra 15 $ |
|---|---|---|
| solo plataforma | **7,868069 $** | **cumple** |
| plataforma + Haiku | **18,345170 $** | **falla** |

El sello se escribió junto a los frenos de C1, que hablaban de «precio por
episodio» y «gasto de Haiku por asiento» **como dos cosas distintas**, lo que
sugiere la primera lectura; pero el texto dice «total». **Lo dejo abierto para la
mesa** en vez de elegir la que sale bien.

---

## Las 100 partidas · 200 asientos

**200 diarios enteros · 0 frenos · 0 reventones en 4.548 evaluaciones · 0 tics
perdidos en 1.501.210 tics vivos · 2.088 de 2.088 citas con parte y cero
interrogantes · calma literal 0 en los 200.**

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 40 | **0** | 0 | **0** | 0 |
| **F** | 80 | 2.042 | 2.115 | **52** | 36 |
| **T** | 80 | 2.433 | 2.433 | **41** | 39 |

**Veredictos:** F área 1.214, **calló 832**, ok 52, vida 17 · T área 2.355,
vida 37, ok 41.

**A no propuso ni una sola forma en 40 asientos.** Con los interruptores
apagados, la política es literalmente la del paper cuatro, y eso lo demuestra el
campo, no el humo.

### Tiempo

| brazo | tics vivos | > 40,5 ms | **perdidos** | vigía |
|---|---|---|---|---|
| A | 323.490 | 0 = 0,000 % | **0** | **0** |
| F | 577.183 | 1.239 = **0,215 %** | **0** | **0** |
| T | 600.537 | 48 = 0,008 % | **0** | **0** |

**Evaluar una forma no cabe en el bucle del juego —el 0,2 % de los tics de F pasa
de 40,5 ms— y aun así no cuesta ni una decisión.** La cifra de F se ha mantenido
entre 0,18 % y 0,25 % en las diez tandas: es un coste estructural estable.

### El parte

| el parte decía | calla | de | **%** |
|---|---|---|---|
| le aceptaron la anterior | 34 | 68 | **50,0 %** |
| le rechazaron la anterior | 800 | 1.894 | **42,2 %** |
| sin formas previas | 0 | 80 | **0,0 %** |

**Nunca calla cuando aún no tiene nada juzgado: 0 de 80.** Es lo único de esta
tabla que no se ha movido en toda la serie. Las otras dos filas se invirtieron
entre la tanda 1 y la 3 y llevan desde entonces alrededor de diez puntos de
separación, con 68 citas en la fila pequeña: **no lo afirmo**.

### La medida principal

| | **F** | **T** |
|---|---|---|
| puntos de control | **78** (26 asientos) | **36** (24 asientos) |
| `d` real ≤ proyectada + 0,05 | 33/78 = **42,3 %** [32,0-53,4] | 22/36 = **61,1 %** [44,9-75,2] |
| comparables con A | 28 | 9 |
| `d` real por debajo de la de A | 10/28 = 35,7 % | 1/9 = 11,1 % |

**Diferencia F − T: −18,80 puntos [−36,30, +0,86], el cero dentro.**

La comparación contra A está **congelada** en 28 y 9 puntos desde la ampliación:
el sello dice que A no se amplía, así que esa columna dejó de crecer en las 60.

### La evolución del acumulado, tanda a tanda

| acumulado | partidas | F | T | **diferencia [IC 95 %]** | cero |
|---|---|---|---|---|---|
| las sesenta | 60 | 47,1 % (34) | 62,5 % (16) | −15,44 [−40,04, +13,40] | dentro |
| + ampliación 1 | 68 | 48,0 % (50) | 61,1 % (18) | −13,11 [−35,91, +13,12] | dentro |
| + ampliación 2 | 76 | 43,6 % (55) | 63,0 % (27) | −19,33 [−39,09, +3,53] | dentro |
| + ampliación 3 | 84 | 42,4 % (66) | 61,3 % (31) | −18,87 [−37,56, +2,33] | dentro |
| + ampliación 4 | 92 | 42,5 % (73) | 62,9 % (35) | **−20,39 [−37,98, −0,30]** | **FUERA** |
| + los dos de la 5 | 94 | 44,0 % (75) | 61,1 % (36) | −17,11 [−34,80, +2,65] | dentro |
| **+ los seis ultimos** | **100** | **42,3 % (78)** | **61,1 % (36)** | **−18,80 [−36,30, +0,86]** | **dentro** |

**Esta tabla es el resultado metodológico de la serie.** En las 92 el cero salió
del intervalo por **0,30 puntos** y escribí entonces que era marginal y que un
solo punto de control lo devolvería. **Dos episodios después volvió a entrar.**
Las proporciones llevan desde las 76 moviéndose dentro de dos puntos; lo único
que cambia es la anchura del intervalo. **Con esta n, cruzar el cero no es un
hallazgo: es ruido de borde.**

### (a) La emparejada

Solo formas con el **mismo número de tramos** y la **misma banda** de distancia al
primer punto de control. **6 celdas de 15 tienen datos en los dos brazos.**

| celda | F | T | dif |
|---|---|---|---|
| 2 tramos · quedarse | 4/6 = 66,7 % | 2/2 = 100 % | −33,3 |
| 2 tramos · banda 1 | 3/4 = 75,0 % | 2/2 = 100 % | −25,0 |
| 3 tramos · quedarse | 3/7 = 42,9 % | 1/3 = 33,3 % | +9,5 |
| 3 tramos · banda 1 | 4/14 = 28,6 % | 8/14 = 57,1 % | −28,6 |
| 3 tramos · banda 2-3 | 6/14 = 42,9 % | 5/7 = 71,4 % | −28,6 |
| 4 tramos · quedarse | 8/11 = 72,7 % | 2/4 = 50,0 % | +22,7 |
| **emparejada** | **28/56 = 50,0 %** | **20/32 = 62,5 %** | **−12,50 [−31,80, +8,90]** |

**Nueve celdas de quince no tienen pareja, y eso es en sí un resultado: el
consejero y el azar no construyen formas de la misma pinta.** La comparación sin
emparejar estaba comparando también dos repertorios distintos. Emparejadas, la
brecha baja de −18,80 a −12,50.

### (b) La magnitud

Bajada real de `d` del tic de aceptación al último punto alcanzado, contra la
bajada de A en la **misma ventana de tics**.

| | formas | **bajada mediana** | bajan de verdad | baja más que A |
|---|---|---|---|---|
| **F** | 43 | **+0,00000** | 15/43 | 4/16 |
| **T** | 29 | **+0,12440** | **22/29** | 5/8 |

**El confuso, declarado:** esto es **lo que pasó en el mundo** en esa ventana, no
lo que la forma causó. T acepta el 1,7 % de lo que evalúa y F el 2,5 %, así que T
es más selectivo por construcción; y A baja +0,13 de mediana en las ventanas de T
frente a +0,00 en las de F. **Las ventanas no son comparables entre brazos**, que
es lo que (a) intenta corregir y solo consigue a medias.

### (c) La magnitud en las formas rechazadas por área

Una forma rechazada nunca vivió: no tiene puntos de control ni horizonte en el
diario. **La ventana se declara y se fija aquí una sola vez sobre las cien:
`L = 20` tics**, la mediana del tramo que duraron las 72 formas aceptadas de los
dos brazos. *(Durante la serie osciló entre 19 y 22 por ser una mediana de la
propia muestra; ésta, sobre las cien, es la definitiva.)*

| brazo | | n | el propio brazo | **A en la misma ventana** |
|---|---|---|---|---|
| **F** | rechazadas por área | 1.213 | +0,00000 · baja 35,8 % | **+0,00000 · baja 24,0 %** |
| **F** | aceptadas (misma L) | 52 | +0,00000 · baja 46,2 % | +0,00000 · baja 27,8 % |
| **T** | rechazadas por área | 2.355 | +0,00000 · baja 34,0 % | **+0,00000 · baja 28,1 %** |
| **T** | aceptadas (misma L) | 41 | +0,03213 · baja 56,1 % | +0,02539 · baja 57,1 % |

**Con 3.568 rechazos, el resultado es limpio: la puerta de área no está tirando
momentos buenos.** En las ventanas que rechaza, el brazo A —que no tiene ni
puerta ni forma— tampoco baja: mediana exactamente cero y solo uno de cada
cuatro baja algo. **Son ventanas planas para todo el mundo.**

### (d) Las formas de F según hubiera forma contada del hermano

«Fresca» = un `hilo_forma` oído con `tramos > 0` en los **150 tics** anteriores a
la evaluación, que es el plazo con el que la propia política la da por fresca
(`policy_forma.py:82,532`).

| | evaluadas | aceptadas | área | calló |
|---|---|---|---|---|
| **CON** forma del hermano | **15** | **0** | 10 | 5 |
| **SIN** forma del hermano | 2.100 | 52 = 2,5 % | 1.204 | 827 |

Diferencia −2,48 puntos [−3,23, +17,92]: **no dice nada, y no puede decirlo.**

**El resultado es la escasez, y es un resultado.** En los 80 asientos de F el hilo
llevó forma **32 veces**, y solo **quince** evaluaciones cayeron dentro de la
ventana de una. Es consecuencia directa de la tasa de aceptación: si un hermano
acepta una forma cada varias partidas, **casi nunca tiene forma que contar**. El
canal horizontal está montado, medido y pasa su humo con ida y vuelta idéntica,
pero **en este régimen prácticamente no se enciende**.

### Lo mismo le pasa al silenciador

**Cero disparos en toda la serie**: ni un solo suceso «el cuerpo calla al
consejero», ni una cita saltada por ese motivo. Hace falta C ≤ 0 **y** cinco
formas aceptadas que acaben mal **en el mismo asiento**, y F lleva 36 caídas
repartidas entre 80 asientos. **Tercer mecanismo que existe, funciona y el régimen
no alcanza.**

La confianza sí se mueve, y de forma distinta en los dos brazos:

| | mediana | mín | **evaluaciones con C = 0** |
|---|---|---|---|
| **F** | 0,30 | **0,00** | **4,2 %** |
| **T** | 0,30 | 0,10 | **0,0 %** |

### Vida

| brazo | vida mediana | puesto mediano | calma literal |
|---|---|---|---|
| A | 8.348,5 | 12,0 | **0** |
| F | 8.154,5 | 13,0 | **0** |
| T | 8.005,0 | 12,0 | **0** |

**Ninguna diferencia sale del ruido** (S6). Las formas no mueven el marcador: lo
mueven el anillo y los vecinos.

---

## Figuras

En `cantera/paper5/figF/`, generadas por `fig_P56C.py`, que **imprime el embudo
que dibuja y cuadra con el analizador** (F 2.042/2.115/52, T 2.433/2.433/41, 78 y
36 puntos): leen los diarios, no una copia a mano.

- **`F4_aceptadas_curva.png`** — (a) el embudo por brazo, con el cero de A en
  escala log; (b) cada punto de control con la `d` proyectada contra la real, la
  diagonal y la banda de 0,05. **Anotado en la figura:** a la escala real de `d`
  (2,5 a 6,2) **la banda de 0,05 es casi invisible**, así que «cumple» es
  prácticamente «en la línea o por debajo».
- **`F5_confianza_vida.png`** — C a lo largo de los tics, un trazo por asiento,
  de `forma_evaluada.C`, que el diario escribe en **cada** evaluación.

---

## Gasto

### Plataforma

| brazo | episodios | mediana | máximo | suma |
|---|---|---|---|---|
| A | 20 | 0,051316 | 0,123589 | 1,370555 |
| F | 37 | 0,055940 | **0,778524** | 3,422500 |
| T | 40 | 0,065562 | 0,207198 | 3,075014 |
| | **100** (3 sin facturar) | | | **7,868069 $** |

### Haiku 4.5 (el consejero, brazo F)

**80 asientos · mediana 0,148868 $ · máximo 0,256076 $ · suma 10,477101 $.**
`/spend` cuadró con la cabecera del sidecar **en los 80**. Los dos frenos —200
llamadas y 1,00 $ por asiento— **no se acercaron nunca**.

**Total: 18,345170 $** en las cien partidas.

---

## Plataforma — las cosas raras, medidas

Ninguna de estas es un fallo de la serie: la imagen, las políticas y el roster
fueron byte a byte los mismos en las diez tandas.

### 1. El pod se cobra por minuto de vida, cola incluida

| caso | en cola | corriendo | **precio** |
|---|---|---|---|
| S-3 (anterior) | ~90 min | normal | **0,74 $** |
| F/24031160 (hoy) | 68 min | 8 min 13 s | **0,778524 $** |
| mediana de la serie | <1 min | ~10 min | **0,0557 $** |

**Catorce veces la mediana, y el episodio jugó una partida normal**: diarios
enteros, cero frenos, cero tics perdidos, 60 citas sin fallo, `/spend` cuadrando.
El precio está fuera de la partida. **Ésta es la razón por la que se canceló todo
lo que estaba esperando en cola.**

### 2. Episodios que cierran bien y no se facturan

**Tres de los 100, los tres en F**, reconsultados hoy y **los tres siguen en
`cost_usd: null`**:

| tanda | episodio | cerrado | diarios |
|---|---|---|---|
| t2 | `ereq_90707b08` (F/20679832) | `completed`, sin error ni exit code | enteros |
| amp1 | `ereq_26eb8c79` (F/22564954) | ídem | enteros |
| amp3 | `ereq_e956aa43` (F/23402786) | ídem | enteros |

El reparto de las cien es **20 de A, 40 de F y 40 de T** (veinte semillas por
tres brazos, más la ampliación solo de F y T). Con **40 de los 100 en F**, que
los tres caigan en F sale por azar con probabilidad **(40/100)³ ≈ 0,064**:
**bajo, pero no concluyente con n = 3.** **Ninguno se descarta**: el encargo
manda descartar por diario perdido o por freno, y no es ninguna de las dos.

### 3. Episodios devueltos de `running` a `submitted`

`F/24240618` fue visto en `running` a las 08:18 por el vigía y **volvió a figurar
como `submitted`** en la consulta siguiente. No es un retraso: es un estado que
retrocede.

### 4. Dos episodios normales, mismo tiempo de cola, precios 3,7× distintos

| | en cola | corriendo | **precio** |
|---|---|---|---|
| F/24031160 | 68 min | 8 min 13 s | **0,778524 $** |
| T/24240618 | 70 min | **10 min 21 s** | **0,207198 $** |

T esperó **más** y corrió **más**, y costó **3,7 veces menos**. Con el minuto de
vida como única vara deberían parecerse. **No tengo explicación desde aquí y no la
invento.**

### 5. El atasco, y lo que costó

Desde las 07:10 UTC la plataforma **dejó de programar trabajos**. Ocho episodios
esperaron 68-70 minutos; dos arrancaron y seis se cancelaron en `submitted`. Una
sonda de dos, creada a las 08:34 con la cola vacía, **no arrancó en 16 minutos** y
se canceló.

**Las cancelaciones salieron gratis, y está comprobado**: gasto 129,913836 $ antes
y después, sin mover un céntimo, y ninguna había pasado a `running` (`running_at`
vacío antes y después). Cancelar en `submitted` es seguro.

---

## Custodia

### Motor y núcleo

```
motor/model.py                          1e511978c251130e95169ebf8443efa1   (INTOCABLE)
paintball/alma/decisor_zs.py            8fa03547e3228ef9df4aa94c444f9252
paintball/alma/appraisal_zs_v42_exp.py  98c13d60167c80cc8334c965be75c640
```

### La política viva y sus piezas

```
paintball/alma/policy_forma.py          746a41f1116c0f1d409ee2b91f6fe0ff
paintball/alma/forma_viva.py            7183091a30a46818178e2f3e281ab562
paintball/alma/confianza_viva.py        6e1e444435914f0b9df287ea37555bbc
paintball/alma/hilo_forma.py            aeea06ae4eb5b704e94fe845a5a5e5aa
paintball/alma/formas_azar.py           eefb5534e9533c8b742f7feb96239588
paintball/alma/humo_forma.py            4aefd120bf739736a3c4719029b7283c
```

### La instrucción del consejero

```
cantera/paper5/instruccion_forma.md     02653e4edf04f3bdd9a0ac3deda9aa01
cantera/paper5/tabla_ensenada.md        9d53807699c4ee2be31d8dd173196de0
```

### Los scripts de la serie

```
cantera/paper5/lanza_P56C.py            bad2c9c2c510bea055f3a173e54f6202
cantera/paper5/lanza_P56C_amp.py        936d3708d71cfa8fd0c429154550d775
cantera/paper5/relanza_P56C.py          1d3c03c65d7ac1ba1808eb41bf2da1a6
cantera/paper5/ciclo_P56C.py            9bf01a1adacc9e6da409ed40686048e4
cantera/paper5/baja_P56C.py             097c8b5ad32e2c319e1cad7b4c9fc727
cantera/paper5/analiza_P56C.py          93fd5ee69cdfb528aeb2de1cf6f0c474
cantera/paper5/sellos_P56C.py           650356dbf22d8420cba8d5bfa55433c4
cantera/paper5/fig_P56C.py              929137685da3f56dfa31cfc2cf7fb2ab
cantera/paper5/estado_P56B.py           599a40422d16a85cb058abbd9668ea26
```

### Datos e imagen

```
cantera/paper5/semillas_21_40.json      6d4057f122b24241d6f6dcf01257ba53
cantera/paper5/roster_lento_v1.json     a2293bd16ee94e6d4c2f4683b57c2a09
imagen  gemv-anima:forma-c1bis
        sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94
políticas  gemv-p56c2-{A,F,T}:v1
```

**Una sola imagen en las diez tandas.** Ni un cambio de código entre la primera
partida y la última.

---

## Lo que queda

**Nada de la serie.** Las cien estan jugadas, medidas y cotejadas.

Queda abierto, para la mesa: **la lectura de S8** (solo plataforma o plataforma
mas Haiku), y los **tres episodios sin facturar**, que la plataforma no ha
puesto en precio en ningun momento de las tres reconsultas.

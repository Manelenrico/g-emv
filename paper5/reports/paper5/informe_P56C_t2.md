# P5-6C · tanda 2 — Semillas 5 a 8

Con el sí de Manel. **Sin cotejar sellos: eso es al final, sobre las sesenta.**

**Veinticuatro diarios enteros, ningún freno, cero tics perdidos.** El parte
sigue llegando con contenido en **el 100 % de las citas** y `/spend` cuadra con
la cabecera en los ocho asientos.

**La respuesta a la duda del tiempo es limpia: ningún brazo pierde un solo
tic.** F gasta más de 40,5 ms en el 0,205 % de sus tics y aun así emite su
acción en los 56.178.

**Un episodio de los doce no está facturado** (F/20679832): corrió bien y su
diario está entero, pero la plataforma no le ha puesto precio.

---

## La tanda

Semillas **20679832, 20784561, 20889290, 20994019** (5 a 8 de
`semillas_S2.json`), los tres brazos con la misma semilla, una petición por
episodio, creadas a las 21:44. **Cola vacía antes y después.**

Misma imagen que la tanda 1 repetida: `gemv-anima:forma-c1bis`,
**`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`**,
con los md5 de contenido del acta sin cambiar (`forma.py`
`b801876afda071403c5af54a28feff85`, `proyeccion.py`
`bbc42daeaa769c783844997067ef148d`, `traductor_forma.py`
`b310bb72884ef5f4e3510ab803cd2776`, instrucción `02653e4edf04f3bdd9a0ac3deda9aa01`,
tabla `9d53807699c4ee2be31d8dd173196de0`).

### El precio, y el episodio sin facturar

| brazo | precios | **mediana** |
|---|---|---|
| **A** | 0,036555 · 0,037115 · 0,039669 · 0,063706 | **0,038392 $** |
| **F** | **(sin facturar)** · 0,035308 · 0,035790 · 0,103817 | **0,035790 $** |
| **T** | 0,025207 · 0,064757 · 0,066743 · 0,105007 | **0,065750 $** |
| | | **total cobrado 0,613674 $** |

**Gasto acumulado: 123,192672 → 123,806346 $**, diferencia **0,613674 $**,
exacta. Y los **episodios cobrados pasan de 1.104 a 1.115: once, no doce.**

**El episodio sin facturar es `ereq_90707b08` (F, semilla 20679832):**

```
 "status": "completed", "running_at": "21:44:38", "completed_at": "21:54:58",
 "cost_usd": null, "error": null, "exit_code": null
```

Corrió diez minutos, que es la duración normal, sin error ni código de salida, y
**sus dos diarios están enteros** (7.536 y 4.106 líneas, con su `final`). Lo
consulté dos veces, la segunda quince minutos después, y sigue sin precio. **No
se descarta**: el encargo manda descartar por diario perdido o por freno, y no es
ninguna de las dos. Queda anotado y se vuelve a consultar al cerrar la serie.

**Haiku por asiento:** mediana **0,152159 $**, máximo **0,242478 $**, suma
1,020785 $. **Ninguno pasa de 0,50 $**, y ninguno de los precios pasa de 0,20.

---

## Las dos medidas nuevas

### Duración de la decisión y tics perdidos

`RADIOGRAFIA.ms` lo escribe `decidir` en **los tres brazos**, así que es la
medida común; `tiempo_tic` solo existe con `GEMV_FORMA=1`. Un tic vivo del mundo
sin registro sería un tic **sin decisión emitida**: la política emite
exactamente una acción por observación.

| brazo | tics vivos | **> 40,5 ms** | **tics perdidos** | vigía |
|---|---|---|---|---|
| **A** | 67.198 | **0 = 0,000 %** | **0 = 0,000 %** | **0** |
| **F** | 56.178 | **115 = 0,205 %** | **0 = 0,000 %** | **0** |
| **T** | 71.078 | **1 = 0,001 %** | **0 = 0,000 %** | **0** |

Y la tanda 1, con la misma vara:

| brazo | tics vivos | > 40,5 ms | tics perdidos | vigía |
|---|---|---|---|---|
| A | 64.630 | 0 = 0,000 % | **0** | 0 |
| F | 45.547 | 109 = 0,239 % | **0** | 0 |
| T | 62.529 | 8 = 0,013 % | **0** | 0 |

**Acumulado t1+t2: cero tics perdidos en 366.160 tics vivos, y el vigía no ha
disparado ni una vez en las veinticuatro partidas.**

**Esto reclasifica el aviso que di en la tanda 1.** El arreglo del parte se paga
en los máximos —F llega a 971 ms en un tic aislado—, pero **no cuesta
decisiones**: la secuencia de tics vivos de cada diario no tiene un solo hueco.
Es consumo de margen, no pérdida. Uno de cada 488 tics de F pasa de 40,5 ms;
en A y en T es prácticamente nadie.

---

## C2 · Las medidas de la tanda 2

### Diarios y frenos

**Los veinticuatro enteros**, ningún freno, nada que descartar.

### Formas

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 8 | **0** | 0 | **0** | 0 |
| **F** | 8 | 197 | 206 | **6** | 4 |
| **T** | 8 | 289 | 289 | **3** | 3 |

**Aceptadas por vida:** F `[0,0,0,1,1,1,1,2]` **mediana 1,0** · T
`[0,0,0,0,0,1,1,1]` **mediana 0,0**.

**Veredictos:** F área 122, calló 77, ok 6, vida 1 · T área 274, vida 12, ok 3.
**Cero reventones** en los dos brazos, otra vez.

Aparece por primera vez una caída **«por vida»** (F): una forma aceptada dejó de
ganar en la reevaluación por el mínimo de vida, no por área.

### El consejero, en F

**Cero fallos en 197 llamadas.** Latencias medianas de 5.033 a 8.562 ms, citas
saltadas de 0 a 9. `/spend` cuadra con la cabecera en los ocho.

**Callar:** del 27 % al 67 %, con mediana en torno al 38 %.

### El parte

**203 de 203 citas con parte no vacío (100 %), cero interrogantes.**

**Callar frente a lo que decía el parte en esa cita:**

| el parte decía | calla | de | % |
|---|---|---|---|
| **le rechazaron la anterior** | 77 | 189 | **40,7 %** |
| sin formas previas | 0 | 8 | **0,0 %** |

En esta tanda **ninguna cita ocurrió tras una forma aceptada**, así que ese caso
no tiene datos aquí.

### La medida principal

| | F | T |
|---|---|---|
| puntos de control alcanzados | 6 (4 asientos) | 2 (2 asientos) |
| `d` real ≤ proyectada + 0,05 | 4/6 = 66,7 % | 2/2 |
| `d` real por debajo de la de A | 1/3 | 0/2 |

### Vida

| brazo | vidas (mediana) | puestos |
|---|---|---|
| A | **8.528** | 2 · 3 · 8 · 13 · 14 · 15 · 15 · 16 |
| F | 8.022 | 5 · 10 · 10 · 14 · 14 · 15 · 16 · 16 |
| T | **9.867** | 3 · 5 · 7 · 8 · 10 · 12 · 16 · 16 |

Calma literal **cero** en los veinticuatro.

---

## Acumulado t1 + t2 (24 partidas, 48 asientos)

### Formas

| brazo | asientos | propuestas | evaluadas | **aceptadas** | caídas |
|---|---|---|---|---|---|
| **A** | 16 | **0** | 0 | **0** | 0 |
| **F** | 16 | 358 | 374 | **13** | 9 |
| **T** | 16 | 543 | 543 | **9** | 9 |

**Aceptadas por vida:**
F `[0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,3]` → **mediana 1,0**
T `[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,4]` → **mediana 0,0**

**Edad de la primera aceptada:** F mediana **5.122** tics · T mediana 1.519.

**Veredictos acumulados:** F área 228, **calló 132**, ok 13, vida 1 · T área 517,
vida 17, ok 9. **Cero reventones en 917 evaluaciones.**

### El parte, acumulado

**368 de 368 citas con parte no vacío (100,0 %), cero interrogantes.**

| el parte decía | calla | de | **%** |
|---|---|---|---|
| **le rechazaron la anterior** | 131 | 336 | **39,0 %** |
| le aceptaron la anterior | 1 | 6 | **16,7 %** |
| sin formas previas | 0 | 16 | **0,0 %** |

La relación de la tanda 1 se sostiene con el doble de datos: **calla el 39 %
cuando le rechazaron y nunca cuando aún no tiene nada juzgado**. El caso «le
aceptaron» sigue con **seis citas**, así que de ese no se puede decir nada.

### La medida principal, acumulada

| | **F** | **T** |
|---|---|---|
| puntos de control alcanzados | **15** (7 asientos) | **5** (3 asientos) |
| `d` real ≤ proyectada + 0,05 | 8/15 = **53,3 %** | 4/5 = 80,0 % |
| comparables con A | 12 | 3 |
| `d` real **por debajo** de la de A | 5/12 = **41,7 %** | 1/3 |
| diferencia (real − A), mediana | **+0,17140** | +0,06999 |

Veinte puntos de control en veinticuatro partidas. **Sigue sin poder
concluirse nada**, y conviene decir por qué: la puerta honesta acepta tan poco
—13 de 374 en F, 9 de 543 en T— que los puntos de control alcanzados crecen muy
despacio. A este ritmo, las sesenta darán unos cincuenta puntos en F y menos de
veinte en T.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Imagen: `gemv-anima:forma-c1bis`
(`sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94`).
Roster: `roster_lento_v1.json`, md5 `a2293bd16ee94e6d4c2f4683b57c2a09`.
Políticas `gemv-p56c2-{A,F,T}:v1`. Ficheros: `P56C_t2_peticiones.json`, los doce
`P56C_t2_{brazo}_{semilla}.json`, `P56C_t2_medidas.json` y los veinticuatro
artefactos en `paintball/runs/P56C_t2_*/`.

**PARO AQUÍ.** La tanda 3 espera el sí.

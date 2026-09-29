# P5-6B — Tres partidas, una por brazo: precio y humo en el campo

Con el sí de Manel. **Nada se afirma de los brazos: esto es humo y precio.**

**Cuatro episodios, 0,294208 $ en total.** Los tres brazos salieron, el diario
llegó entero en los ocho asientos, y **el roster es idéntico en los cuatro
episodios**: los catorce rivales en los mismos asientos, y solo el 10 y el 11
cambian. Es la misma partida con tres criaturas distintas.

**El brazo F falló el humo de campo y se repitió**, como el encargo preveía: el
36 % de sus llamadas moría por timeout. Arreglado, la repetición hizo **61
llamadas con cero fallos**.

---

## §0 · Antes de crear nada

### La imagen, y por qué el sha no es el del encargo

Reconstruí la imagen para meterle dentro un humo que faltaba —el **(i)**: el
bucle de red entero con un websocket de mentira, que ejercita `run()`, el
`player_config`, la cita dentro de `registrar` y la emisión por el canal—.
**Nada de eso se había ejecutado nunca**, y se iba a estrenar en una partida de
pago. Salió bien, pero ahora está probado en vez de supuesto.

```
$ docker image inspect gemv-anima:forma --format '{{.Id}}'
sha256:81180ee793b2fc81babdd860c12b4c0f31da48ed80402f9e46102e3f27025c30
```

```
humo (i) OK: el bucle de red entero — 200 acciones (una por observacion), 5 mensajes de canal, 5 con forma; el hermano los oye y decodifica igual
```

### Las tres políticas, subidas a las 19:54 UTC

| brazo | nombre | `policy_version_id` | variables fijadas en el upload |
|---|---|---|---|
| **A** | `gemv-p56-A:v1` | `0b666688-753c-46f2-94ea-ce4cdf1b4fc8` | ninguna: la imagen trae todo apagado en su `ENV` |
| **F** | `gemv-p56-F:v1` | `6bca871a-dfc8-4777-a636-81a8d0b826aa` | `GEMV_FORMA=1`, `GEMV_HILO_FORMA=1`, `GEMV_CONSEJERO_FORMA=1`, `--use-bedrock`, `--bedrock-model us.anthropic.claude-haiku-4-5-20251001-v1:0` |
| **T** | `gemv-p56-T:v1` | `d6f937dd-8097-4f14-8d33-178f28e5f288` | `GEMV_FORMA=1`, `GEMV_HILO_FORMA=1`, `GEMV_FORMAS_AZAR=1` |
| **F2** (repetición) | `gemv-p56-F:v2` | `01e336b8-4894-41b1-8b61-9166cc6f946a` | las de F **más** `GEMV_CORTEX_TIMEOUT=25` y `GEMV_FORMA_CADA=250` |

Todo quedó escrito en el acta **a las 19:54**, antes de la primera petición de
las **19:55:49**.

### El roster

`cantera/paper5/roster_lento_v1.json`, md5 **`a2293bd16ee94e6d4c2f4683b57c2a09`**.

**Fuera las tres cazadoras**, que son las que E3 señaló sobre 434 diarios:

| fuera | golpes antes del tic 2.000 | muertes nuestras |
|---|---|---|
| **Zero Sum Baseline** | 2.877 | 61 |
| **zero-sum-example** | 443 | **71** |
| **ryanschiller-zero-sum-player-v1** | 292 | 42 |
| **las tres** | **3.612 de 3.928 = 92,0 %** | **174 de 211 = 82,5 %** |

**Dentro, una repetición más de las tres más pacíficas que ya estaban**, para no
cambiar el reparto de políticas del mundo sino solo su temperatura:

| se repite | golpes | muertes | queda en |
|---|---|---|---|
| **belobog** | **0** | **0** | ×3 |
| **relh-zero-sum** | 2 | 0 | ×3 |
| **zero-sum-scavenger** | 10 | 2 | ×3 |

Más `sivanlevy-zs-courier` ×2, `zs-patient` ×1, `aaron-zs-fable` ×1 y
`skourehjan-zero-sum-scripted-v1` ×1: catorce rivales, más nuestros dos asientos
con slot explícito, 10 y 11.

### Gasto acumulado y cola, antes

```
  episodios cobrados: 1075
  gasto acumulado   : 121.082151 USD

pending   :   0 peticiones ·    0 episodios sin acabar
submitted :   0 peticiones ·    0 episodios sin acabar
running   :   0 peticiones ·    0 episodios sin acabar
```

**Una corrección de método que hay que decir.** Filtrando por el correo de la
sesión salían **cero** peticiones. La identidad de la plataforma es
[correo tapado] ([id tapado]), comprobada pidiendo una
petición conocida. Y **el servidor ignora `?requester=` en silencio** y devuelve
peticiones de otras cuentas: el filtro que respeta es **`mine=true`**. Con el
filtro malo, el gasto habría salido a cero y la cola habría parecido vacía sin
serlo.

---

## Las cuatro partidas

| | **A** | **F** | **T** | **F2** (repetición) |
|---|---|---|---|---|
| petición | `xreq_8cce9f18…` | `xreq_81fa74ff…` | `xreq_90a1f616…` | `xreq_3a447cb6…` |
| episodio | `ereq_b8d4dfb8…` | `ereq_44701a5c…` | `ereq_8fa7ba6c…` | `ereq_2b9ab230…` |
| creada | 19:55:49 | 19:56:07 | 19:56:08 | 20:08:40 |
| arranque | 19:57:05 | 19:56:59 | 19:57:04 | 20:08:58 |
| fin | 20:06:50 | 20:06:43 | 20:05:25 | 20:19:21 |
| cola | 76,2 s | 51,6 s | 56,1 s | 18,5 s |
| corriendo | 584,6 s | 584,8 s | 500,9 s | 622,3 s |
| **precio** | **0,032579 $** | **0,102261 $** | **0,051812 $** | **0,107556 $** |

**Total: 0,294208 $.** Gasto acumulado después: **121,376359 $** (1.079
episodios), que es exactamente **121,082151 + 0,294208**. Cola vacía otra vez.

**El precio del brazo F es el triple que el de A**, y la diferencia es el
consejero: 0,102261 contra 0,032579. T, que no llama a nadie pero sí evalúa
formas, cuesta 0,051812.

### ¿Es la misma partida? Sí, y está comprobado asiento a asiento

Leído de `participants` de los cuatro episodios:

```
asiento | A | F | F2 | T
       0 | zero-sum-scavenger  | zero-sum-scavenger  | zero-sum-scavenger  | zero-sum-scavenger
     ...   (los catorce rivales, en los MISMOS asientos en los cuatro)
      10 | gemv-p56-A          | gemv-p56-F          | gemv-p56-F          | gemv-p56-T   <-- DISTINTO
      11 | gemv-p56-A          | gemv-p56-F          | gemv-p56-F          | gemv-p56-T   <-- DISTINTO

asientos iguales en los tres: 14 de 16
```

**Los dos únicos asientos que cambian son los nuestros.** Avisé antes de mirar
de que la semilla fija el mapa pero no siempre el reparto de asientos (memoria
de S-2); **con el roster dado explícitamente por `policy_version_id` y slot, el
reparto sí quedó fijo**. Comprobado, no supuesto.

---

## El humo en el campo

### Los ocho asientos: vida, muerte, anillo y calma

| brazo/asiento | vida (tics) | `hp` final | `match_ticks` | razón | tics con daño | último daño | primer aviso del anillo |
|---|---|---|---|---|---|---|---|
| A / 10 | 481..8423 = **7.943** | 1 | 8.424 | `eliminated` | 12 | 8.404 | **7.296** |
| A / 11 | 481..9554 = **9.074** | 14 | 9.555 | `eliminated` | 8 | 9.537 | 7.296 |
| F / 10 | 481..8875 = **8.395** | 1 | 8.876 | `eliminated` | 11 | 8.872 | 7.296 |
| F / 11 | 481..8848 = **8.368** | 4 | 8.849 | `eliminated` | 6 | 8.831 | 7.296 |
| F2 / 10 | 481..9103 = **8.623** | 1 | 9.104 | `eliminated` | 8 | 9.064 | 7.296 |
| F2 / 11 | 481..9157 = **8.677** | 15 | 9.158 | `eliminated` | 8 | 9.140 | 7.296 |
| T / 10 | 481..8551 = **8.071** | 7 | 8.552 | `eliminated` | 7 | 8.532 | 7.296 |
| T / 11 | 481..8740 = **8.260** | 19 | 8.741 | `eliminated` | 5 | 8.723 | 7.296 |

**El diario llegó entero en los ocho**: los ocho traen su registro `final` con
`match_ticks`, y el último tic vivo es siempre `match_ticks − 1`. Los ocho
murieron **eliminados**, entre los tics 8.424 y 9.555, o sea por debajo de la
mitad de los 18.240 configurados. El primer aviso del anillo cae en el tic
**7.296** en los ocho, que es el 40 % exacto que `lento_v0` fijaba.

**La calma sigue siendo cero**, con la vara declarada de P5-1: cero instantes de
calma literal en los ocho asientos, y la rompe **`R-CARENCIA` en el tic 481**,
el primero de vida, exactamente como en las seis partidas de P5-1. La única
excepción es `A/10`, con **32 instantes** de calma declarada (solo F y S en
reposo) de 7.943.

### Brazo A · lo que tenía que salir

| | asiento 10 | asiento 11 |
|---|---|---|
| citas al consejero | **0** | **0** |
| formas propuestas, evaluadas, aceptadas | **0, 0, 0** | **0, 0, 0** |
| mensajes de hilo, partes | **0, 0** | **0, 0** |
| líneas del diario | 8.771 | 9.948 |

**Ningún registro de forma, ninguno.** Con los interruptores apagados la política
con formas es la del cuatro, y el campo lo confirma: los `tiempo_tic` tampoco
aparecen, porque el camino de `decidir` es literalmente `super().decidir(obs)`.

### Brazo F · falló, y por qué

| | F/10 | F/11 | **F2/10** | **F2/11** |
|---|---|---|---|---|
| citas intentadas (`parte` escrito) | 84 | 84 | **35** | **35** |
| **citas saltadas** (una en vuelo) | **40** | 33 | **4** | **4** |
| llamadas enviadas | 44 | 50 | 30 | 31 |
| **fallidas por timeout** | **16 (36 %)** | **12 (24 %)** | **0** | **0** |
| latencia mediana | 6.772 ms | 4.260 ms | 8.185 ms | 4.986 ms |
| respuestas que parsean | 28/28 | 38/38 | 30/30 | 31/31 |
| de ellas, **`callar`** | **17 (61 %)** | 12 (32 %) | **17 (57 %)** | 7 (23 %) |
| formas evaluadas | 28 | 39 | 31 | 35 |
| veredictos | área 10, calló 17, **ok 1** | área 27, calló 12 | área 14, calló 17 | área 27, calló 7, **ok 1** |
| **aceptadas** | **1** | 0 | 0 | **1** |
| caídas | 0 | 0 | 0 | 1 (deja de ganar) |
| **gana el tic** | 1 | 0 | 0 | **8** |
| gasto del consejero (cabecera) | 0,242812 $ | 0,230583 $ | **0,162379 $** | **0,159057 $** |
| frenos | ninguno | ninguno | ninguno | ninguno |

**El fallo, con su causa exacta.** El motivo de los 28 fallos de F es uno solo:

```
motivos de fallo: {"TimeoutError('timed out')": 16}
latencia: mediana 7185 ms · min 2332 · max 8026 · n 44
```

La latencia mediana era **7.185 ms** contra un tope de **8.000 ms**: el consejero
moría justo en el borde. Y la cadencia de cita —cada 100 tics, que a 24 tics por
segundo son **4,2 s**— era **más rápida que la propia llamada**, así que había
siempre una en vuelo y **40 de 84 citas se saltaron**.

**El arreglo no necesitó tocar la imagen**, y eso hay que decirlo: las dos
palancas ya eran variables de entorno que el código lee —`GEMV_CORTEX_TIMEOUT`
en `cortex_t5.py:51` y `GEMV_FORMA_CADA` en `policy_forma.py:66`—, así que bastó
una versión nueva de la política con dos `--secret-env` más. **El sha es el
mismo**, `81180ee793b2…`.

**Y funcionó:** de 40 y 33 citas saltadas a **4 y 4**; de 16 y 12 fallos a
**cero y cero**; y el gasto del consejero bajó de 0,24 a 0,16 $ por asiento
porque ya no se pagan llamadas que se tiran.

**La confianza llegó a funcionar en F2/11**, que es lo único que la ejercita de
punta a punta: la forma aceptada alcanzó dos puntos de control, **los dos
acertados**, y C subió **0,30 → 0,40 → 0,50**. En F/10, al revés: cuatro puntos
de control, **los cuatro fallados**, y C cayó **0,30 → 0,15 → 0,00**. Ninguno de
los dos llegó a las cinco formas malas que hacen callar al consejero.

**Los ocho aciertos del tic en F2/11 fueron todos por la ventaja del área**
(`por_la_ventaja: 8`), que es el mecanismo de P5-6A funcionando en vivo.

### Brazo T · el azar por la misma puerta

| | T/10 | T/11 |
|---|---|---|
| formas al azar propuestas | 81 | 83 |
| evaluadas | 81 | 83 |
| veredictos | **área 80, ok 1** | **área 82, ok 1** |
| aceptadas | 1 | 1 |
| caídas | 1 (deja de ganar) | 1 (deja de ganar) |
| gana el tic | 3 (1 por la ventaja) | 4 (1 por la ventaja) |
| confianza | sin cambios | sin cambios |

**La puerta honesta deja pasar 1 de 81 y 1 de 83.** Las dos aceptadas se cayeron
después en una reevaluación por dejar de ganar, que es el mecanismo de caída
funcionando.

### El hilo del hermano, en los cuatro

| | dichos | oídos | con forma | no caben |
|---|---|---|---|---|
| F/10 | 175 | **175** | 0 | 0 |
| F/11 | 175 | **175** | 0 | 0 |
| F2/10 | 180 | **180** | 0 | 0 |
| F2/11 | 181 | 180 | **1** | 0 |
| T/10 | 169 | 165 | 1 | 0 |
| T/11 | 173 | 165 | 1 | 0 |

**La ida y vuelta es real y entre contenedores distintos**, que es lo que ningún
banco podía probar: en F los dos asientos dicen 175 y oyen 175. Ningún mensaje
se pasó de los 120 ASCII. Que `con_forma` sea casi siempre 0 no es un fallo: es
que casi nunca había una forma viva en el instante de hablar, porque la puerta
acepta muy poco.

### El tiempo por tic, y el hilo de evaluación

| | mediana | p95 | máximo | tics con evaluación **en el hilo** |
|---|---|---|---|---|
| F/10 | 1,411 ms | 4,217 | **180,6** | 8.254 de 8.395 (98,3 %) |
| F/11 | 0,467 ms | 3,161 | 71,5 | 8.260 de 8.368 |
| F2/10 | 0,647 ms | 3,149 | 77,6 | 8.480 de 8.623 |
| F2/11 | 2,549 ms | 4,581 | **203,4** | 8.559 de 8.677 |
| T/10 | 0,793 ms | 3,696 | **263,7** | 8.051 de 8.071 |
| T/11 | 0,471 ms | 3,449 | 124,9 | 8.240 de 8.260 |

**El umbral de 20 ms salta enseguida y no vuelve atrás**: en los seis asientos la
evaluación se hace en el hilo en más del 98 % de los tics. **Evaluar una forma
no cabe en el bucle del juego**, y sacarla al hilo no era una precaución sino un
requisito. Gracias a eso el tic mediano se queda por debajo de los 2,6 ms.

---

## Una observación de conducta, sin interpretarla todavía

**El consejero dijo `callar` en el 57-61 % de sus respuestas** en los asientos 10
de F y F2, y en el 23-32 % en los asientos 11. En el banco de P5-5B callaba el
**1-2 %**. Lo que ha cambiado entre medias es que ahora lleva **la tabla
enseñada** y recibe **el parte** de cómo le fue a sus formas anteriores.

**No afirmo nada de esto**: es humo, la n es de cuatro asientos, y los dos
asientos de cada partida dan cifras muy distintas. Queda anotado como lo primero
que habrá que mirar en la serie.

---

## Lo que falta, y lo digo

**El gasto del consejero por `/spend` no está.** Tengo el de la **cabecera**
`X-Coworld-Spend-Usd`, que es el que el freno usa y que llegó siempre
(`freno_gasto_ciego: false` en los cuatro asientos). Pero `/spend` es una ruta
**del sidecar, dentro del pod**, y `ConsejeroForma` **no la llama**: el
`pide_gasto()` que existe es el del `Cortex` del cuatro, y con `GEMV_CORTEX=0`
no corre. **Es un hueco mío en P5-6A**, no de la plataforma, y hay que taparlo
antes de la serie: son tres líneas en `ConsejeroForma`.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Imagen: **`sha256:81180ee793b2fc81babdd860c12b4c0f31da48ed80402f9e46102e3f27025c30`**,
la misma en los cuatro episodios. Roster:
`roster_lento_v1.json`, md5 `a2293bd16ee94e6d4c2f4683b57c2a09`. Semilla
**20260916** en los cuatro. Ficheros: `lanza_P56B.py`, `baja_P56B.py`,
`humo_campo_P56B.py`, `participantes_P56B.py`, `estado_P56B.py`, los cuatro
`P56B_*_peticion.json` y `P56B_*_final.json`, `P56B_humo_campo.json`,
`P56B_estado.json`, y los ocho artefactos en `paintball/runs/P56B_{A,F,F2,T}/`.

**PARO AQUÍ.** Lo siguiente (P5-6C) es la serie —veinte semillas por tres
brazos, por tandas de diez— y necesita el sí de Manel. Antes de esa serie hay
que tapar el hueco del `/spend` y decidir si la cadencia de cita se queda en 250.

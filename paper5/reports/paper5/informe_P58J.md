# P5-8J — ¿Rompió la imagen del compromiso la puerta?

Diagnóstico **en seco**, **coste cero**. Sin imagen nueva, sin plataforma. Motor,
decisor y tabla intocados. **Sin sellos. El margen no se toca.**

---

## El titular

**No. La imagen no rompió la puerta. Es el mundo.**

Y no es una opinión: **la aceptación sigue a los diarios y no sigue al código en
absoluto.**

| código \ diarios | **E** (293 nacimientos) | **I** (1.030 nacimientos) |
|---|---|---|
| **puerta de la imagen de E** | **54 ok = 18,4 %** | **10 ok = 1,0 %** |
| **puerta de la imagen de H/I** | **54 ok = 18,4 %** | **10 ok = 1,0 %** |

**Las filas son idénticas; las columnas no se parecen.** Y las 1.323 re-juzgadas
en seco coinciden con el veredicto que la puerta viva dio en su día:
**1.323 de 1.323, el 100 %.**

**La razón de fondo es que no hay dos puertas.** De los doce ficheros que tocan
el juicio, **once son byte a byte idénticos** entre las dos imágenes
—`forma.py`, `forma_viva.py`, `proyeccion.py`, `curiosidad.py`,
`confianza_viva.py`, `decisor_zs.py`, `appraisal_zs_v42_exp.py`, `model.py`,
`alcance_g.py`, `hilo_forma.py`— y los dos que cambian **solo añaden** el
compromiso, que corre **después** de la decisión y **fuera** de la ruta del
juicio.

**El mecanismo de la caída es aritmético, no un defecto:** los cinco asientos que
aceptan cero son exactamente aquellos cuya **ventaja máxima no llega al margen**.
No es que la puerta los rechace: es que la ventaja nunca sube hasta 0,062.

**Y el dato que mata la hipótesis «fue la imagen»: dentro de la propia sonda E,
con la misma imagen y el mismo episodio, un asiento aceptó 1 de 153 y el otro 53
de 140.** La variación entre asientos de una misma imagen (37,2 puntos) es mayor
que cualquier diferencia entre imágenes.

---

## 1 · El diff, con fichero y línea

Comparados los ficheros **sacados de las dos imágenes**, no del repositorio.

```
gemv-anima:curforma-e0   sha256:e6167599fd9bad6db9eb0072400e37fc5fe1e24010561443afce44f500aebb4c
gemv-anima:curforma-h0   sha256:6afe40f83aeab5e3bad7f7e83ac73382893fabfe3485d79a6c36a5d4e36db599
```

| fichero | E | H/I | |
|---|---|---|---|
| `forma.py` | — | — | **IDÉNTICO** |
| `forma_viva.py` | — | — | **IDÉNTICO** |
| `proyeccion.py` | — | — | **IDÉNTICO** |
| `curiosidad.py` | — | — | **IDÉNTICO** |
| `confianza_viva.py` | — | — | **IDÉNTICO** |
| `decisor_zs.py` | — | — | **IDÉNTICO** |
| `appraisal_zs_v42_exp.py` | — | — | **IDÉNTICO** |
| `model.py` | — | — | **IDÉNTICO** |
| `alcance_g.py`, `hilo_forma.py` | — | — | **IDÉNTICO** |
| `curiosidad_forma.py` | `5687f0f3…` | `4d2ef856…` | **+5 líneas** |
| `policy_forma.py` | `75e1fb3b…` | `891cea92…` | **+134 líneas** |

### Todo lo que cambia, línea a línea

| fichero:línea (imagen H) | qué es | ¿toca la puerta? |
|---|---|---|
| `curiosidad_forma.py:62-65` | `_alcance_de(mundo, a)` — atajo de `armados` | **No.** Solo lo llama la ruptura (e). |
| `policy_forma.py:553-558` | cinco contadores: `k_rival_dist`, `k_rupturas`, `k_obedece`, `k_enfria`, `k_coste` | **No.** Contadores. |
| `policy_forma.py:993-995` | `fv.W_nace = riqueza_W(...)` al nacer | **No.** Solo lo lee la ruptura (d). |
| `policy_forma.py:1461` | `if CUR_FORMA_ON: accion = self._compromiso(obs, accion, radio)` | **No.** Última línea de la decisión, **después** de que la radiografía ya esté hecha. |
| `policy_forma.py:1465-1524` | `_rupturas()`, método nuevo | **No.** Solo lo llama `_compromiso`. |
| `policy_forma.py:1526-1584` | `_compromiso()`, método nuevo | **No.** Ver abajo. |

**No hay una sola línea suprimida ni modificada. El diff es puramente aditivo.**

### Los seis sitios que la consigna nombra, uno por uno

| | dónde vive | cambió |
|---|---|---|
| **generación** | `_cita_curiosidad` `policy_forma.py:935-1015` | **No.** Byte a byte igual salvo las 3 líneas de `W_nace`. |
| **puñado comparador** | `forma.mejor_propia_H` + `FV.pon_base` → `D.candidatos` | **No.** `forma.py` y `forma_viva.py` idénticos. |
| **cálculo de la ventaja** | `forma.area` / `forma.juzga_margen` `forma.py:576-584` | **No.** Fichero idéntico. |
| **margen** | `confianza_viva.py` → `self.conf.margen()` | **No.** Fichero idéntico. Y medido: mediana **0,062 en las tres sondas**. |
| **renglón de ignorancia** | `CFM.con_renglon` dentro de `_juzga` `policy_forma.py:677-691` | **No.** Mismo bloque, mismo candado, misma posición. |
| **refractario** | `CUR_REFRACTARIO` `policy_forma.py:87` | **No.** `50` en las dos. |

**Y el único efecto real del compromiso sobre la puerta es indirecto y a través
del mundo**: al ejecutar el paso de la forma cambia la trayectoria del cuerpo,
luego cambian las observaciones de los tics siguientes, luego cambia el estado
desde el que nacen y se juzgan las formas. **Eso no es romper la puerta; es que
el cuerpo va a otro sitio.**

---

## 2 · El cruce

**Antes que nada, una precisión que cambia la pregunta: el cruce estricto que
pediste —«la puerta de E contra la de H/I»— no está definido, porque no hay dos
puertas.** Los once ficheros del juicio son los mismos bytes. Así que lo hice de
la única forma con contenido: **cargando la puerta desde los ficheros extraídos
de cada imagen** y pasándole los nacimientos de la otra sonda.

`cruza_P58J.py` replica `AlmaForma._juzga` fuera del bicho: el mismo
`_contexto`, el mismo `FV.pon_base`, el mismo `con_renglon`, el mismo
`FV.evalua`, y **el margen leído del diario, no cableado**.

### Los dos controles del arnés

| | |
|---|---|
| **destino del BFS reconstruido = destino registrado** | **1.323 / 1.323** |
| **veredicto en seco = veredicto de la puerta viva** | **1.323 / 1.323** |

El primero dice que el `Ojo` reconstruido ve lo mismo que el vivo. El segundo,
que mi réplica de la puerta **es** la puerta. Sin esos dos, lo de abajo no
valdría nada.

### El resultado

```
código E sobre diarios E : 293 juzgadas ·  54 ok (18,4 %)
código H sobre diarios E : 293 juzgadas ·  54 ok (18,4 %)
código E sobre diarios I : 1030 juzgadas · 10 ok ( 1,0 %)
código H sobre diarios I : 1030 juzgadas · 10 ok ( 1,0 %)
```

**La aceptación es función de los diarios y constante en el código.** Por tu
propio criterio: **es el mundo, y se dice.**

### Por qué el mundo da eso: la ventaja no llega al margen

| asiento | n | ok | tasa | **ventaja máxima** | margen |
|---|---|---|---|---|---|
| E/20260916/10 | 153 | 1 | 0,7 % | 0,06478 | 0,062 |
| **E/20260916/11** | 140 | **53** | **37,9 %** | **0,07771** | 0,062 |
| H/20260916/10 | 85 | 1 | 1,2 % | 0,07356 | 0,062 |
| **H/20260916/11** | 155 | **0** | 0,0 % | **0,04945** | 0,062 |
| I/20260916/10 | 53 | 2 | 3,8 % | 0,07786 | 0,062 |
| I/20260916/11 | 137 | 2 | 1,5 % | 0,06861 | 0,062 |
| **I/20365645/10** | 127 | **0** | 0,0 % | **0,05088** | 0,062 |
| **I/20365645/11** | 159 | **0** | 0,0 % | **0,05103** | 0,062 |
| **I/20470374/10** | 128 | **0** | 0,0 % | **0,03993** | 0,062 |
| I/20470374/11 | 46 | 1 | 2,2 % | 0,06317 | 0,062-0,071 |
| I/20575103/10 | 85 | 1 | 1,2 % | 0,07048 | 0,062 |
| **I/20575103/11** | 15 | **3** | **20,0 %** | **0,08191** | 0,062 |
| I/20679832/10 | 141 | 1 | 0,7 % | 0,06621 | 0,062 |
| **I/20679832/11** | 139 | **0** | 0,0 % | **0,05140** | 0,062 |

**Los cinco asientos con cero aceptadas son exactamente los cinco cuyo tope de
ventaja está por debajo del margen. Cinco de cinco.** No hay rechazo: hay techo.

### La varianza está entre asientos, no entre imágenes

| | tasas por asiento | rango |
|---|---|---|
| **E** (2 asientos) | 0,65 % · **37,86 %** | **37,2 puntos** |
| **H** (2 asientos) | 1,18 % · 0,00 % | 1,2 puntos |
| **I** (10 asientos) | 0 · 0 · 0 · 0 · 0,71 · 1,18 · 1,46 · 2,17 · 3,77 · **20,0 %** | **20,0 puntos** |

**Los catorce asientos juntos: mediana 0,94 %.** El 37,9 % de E/11 y el 20,0 % de
I/20575103/11 son **los dos valores altos de toda la serie**, y caen uno en cada
imagen. **El 0 de 155 de H/11 está dentro de lo que la imagen de E ya producía**
(su otro asiento dio 0,65 %).

**Retiro implícitamente el planteamiento de la pregunta, y es mío el error:** al
comparar «E: 53 de 140» con «H: 0 de 155» estaba comparando **el mejor asiento de
una sonda con el peor de otra**. La sonda E tenía dos asientos y yo leí el bueno.

---

## 3 · El puñado comparador y el refractario

### ¿Incluye ahora el paso de la forma activa? **No. Ni ahora ni antes.**

Por **dos razones independientes en el código**, y comprobado además **con datos**.

**Razón 1 — no puede haber forma activa cuando nace una.**
`policy_forma.py:936` (E) y `:942` (H), idéntica en las dos:

```python
if self.vivas:
    return                      # hay forma activa
```

Ninguna forma de curiosidad nace mientras otra vive, así que **al juzgarla no hay
ningún `_FM_` que meter en la papeleta**.

**Razón 2 — la inyección vive en otro sitio del tic.**
El envoltorio que mete el paso de la forma en la papeleta se instala **solo
alrededor de `D.decide`** (`policy_forma.py:1330-1361`, con `finally:
D.candidatos = _orig`). `_cita_curiosidad` —que genera **y juzga**— se llama
desde `registrar`, en `policy_forma.py:1605`, **fuera de ese try/finally**, y
juzga **síncrono** (`:1011` → `_acepta_o_no:706` → `_juzga:660`), no por el hilo.
**Esa colocación es idéntica en las dos imágenes** (E `:1468`, H `:1605`).

**Y la comprobación con datos, que es la que vale:** en el cruce registré quién
gana el comparador en cada una de las 1.323 evaluaciones.

```
¿algún _FM_ en el comparador?
  diarios E : 0 de 293
  diarios I : 0 de 1030
```

**Cero.** Lo que gana el comparador es, casi siempre, **`noop`**: 98 % en E, 94 %
en I; el resto, `ir_botin` (1 % y 5 %) y unos pocos `ir_objeto`,
`usar_botiquin`, `ir_centro`, `ir_pareja`.

### ¿Cambió el refractario qué tics generan formas? **No.**

Todos los mandos de generación son la misma línea en las dos imágenes:

| | E | H/I |
|---|---|---|
| `CUR_REFRACTARIO` | `:87` = **50** | `:87` = **50** |
| `CUR_CONSIGNA` | `:86` = **0,5** | `:86` = **0,5** |
| `CUR_ATASCO_PASOS` | `:92` = **3** | `:92` = **3** |
| `UMBRAL_SEGURO` | `curiosidad_forma.py:38` = `C.SEGURO` = **0,2** | ídem |
| `if self.vivas: return` | `:936` | `:942` |

**Lo que sí cambió, y no es el refractario, es cuánto vive una forma.** Con el
compromiso las formas llegan (7 de 10 completadas por alivio en P5-8I) en vez de
morir de atasco, así que `self.vivas` está ocupado más tics y **nacen menos
formas por tic**. Eso explica que E/10 naciera 153 y H/10 sólo 85 — **pero no
toca la tasa de aceptación**, que es lo que se hundió.

---

## Lo que no sé, marcado como tal

**No sé por qué la ventaja alcanzable varía tanto entre asientos**, que es la
pregunta que queda viva. Tengo una pista y **no pasa de pista**: la ventaja es
una **diferencia absoluta** entre el coste de la forma y el del mejor propio del
cuerpo, así que escala con lo mal que esté el cuerpo.

| asiento | coste del mejor propio | tasa |
|---|---|---|
| E/20260916/11 | **2,1649** | **37,9 %** |
| I/20260916/11 | 1,7377 | 1,5 % |
| I/20575103/11 | **1,5949** | **20,0 %** |
| … | … | … |
| I/20679832/11 | 0,9599 | 0,0 % |

**Spearman ρ = +0,52 con n = 12.** El valor crítico para n = 12 anda por 0,59:
**esto NO es significativo y no lo presento como hallazgo.** Los dos asientos de
más aceptación son el 1.º y el 3.º de coste, pero el 2.º acepta el 1,5 %. **Es
una pista para medir, no una explicación.**

**No sé si `W` explica algo.** ρ = −0,30 con los doce asientos: sigue sin
sostenerse la lectura de P5-8E, y ahora con el doble de asientos que en P5-8I.

**No he comprobado el efecto indirecto.** Afirmo que el compromiso solo toca la
puerta cambiando la trayectoria, y eso es **lectura de código, no medida**. Para
medirlo haría falta correr la imagen de E y la de H sobre la misma semilla **con
el mismo roster**, y los rosters rotan (`s2_rotacion_roster_vara`): **en E, H e I
la semilla 20260916 son tres partidas con rivales distintos.** Por eso ni
siquiera esos tres pares son réplicas.

**Y no sé si el 18,4 % de E es el número «bueno».** Sale de dos asientos, uno de
los cuales es el más alto de los catorce. **El 37 % de P5-8A (en seco, otro
mundo) y el 18,4 % de E pueden ser los dos casos afortunados, no la referencia.**
La mediana de los catorce asientos medidos es **0,94 %**.

---

## Lo que esto deja en la mesa — propuesta, no ejecución

**No hay nada que arreglar en la imagen.** No hay defecto que identificar, porque
no hay diferencia de código en la ruta del juicio. **Lo digo sin arreglarlo
porque no hay nada roto.**

**La pregunta que queda no es «por qué bajó», es «por qué E/11 fue tan alto».**

**El margen no se toca, y no lo toco.** Pero dejo constancia de lo que el
contrafactual de P5-8I ya medía y esto confirma: con el margen en 0,062 la serie
mide un mecanismo que funciona sobre una muestra que no da. **Es una decisión de
vara, y es tuya.**

---

## Custodia

```
motor/model.py                          1e511978c251130e95169ebf8443efa1
paintball/alma/decisor_zs.py            8fa03547e3228ef9df4aa94c444f9252
paintball/alma/appraisal_zs_v42_exp.py  98c13d60167c80cc8334c965be75c640
```

**Declarado:** el cruce carga `forma`, `forma_viva`, `proyeccion`, `curiosidad` y
`curiosidad_forma` **de los ficheros extraídos de cada imagen**, pero `decisor_zs`
lo toma del repositorio a través de `serie_util`. **Su md5 es el mismo en el
repositorio y en las dos imágenes** (`8fa03547…`), así que es el mismo código; lo
digo por no dejarlo supuesto.

`cantera/paper5/mide_P58J.py` · `cruza_P58J.py` · datos `P58J.json`,
`P58J_cruce_EE.json`, `P58J_cruce_EI.json`, `P58J_cruce_HE.json`,
`P58J_cruce_HI.json`.

**Ninguna imagen construida. La plataforma no se tocó. Gasto: cero.**

**PARO AQUÍ.**

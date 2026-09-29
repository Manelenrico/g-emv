# P5-FIG2 · Arreglo de las figuras del paper cinco y seis preguntas

*Solo lectura de diarios y redibujo. No se tocó `motor/model.py`
(md5 `1e511978c251130e95169ebf8443efa1`), ni el texto del paper. Nada se subió,
publicó ni borró. Coste de plataforma: cero.*

Generador: `cantera/paper5/fig_paper5.py`.
Salida: `cantera/paper5/figuras_paper5/` — diez PNG a 300 ppp y cinco `.txt`.

---

## A · LO QUE SE REDIBUJÓ

### A.1 · Separador de miles en las `_en`

Se añadió `mil(n, idi)`: coma para `en`, punto para `es`. Pasan por ahí el
subtítulo de la fig. 1 (`10,752` · `10,273`), el de la fig. 3
(`1,977 to 8,027`) y el rótulo de la meseta (`6,050 instants with the map
frozen`). Las `_es` no cambian: `10.752`, `10.273`, `1.977`, `8.027`, `6.050`.

### A.2 · Glosario en las `_en` (y una en las `_es`)

| viejo | nuevo | dónde |
|---|---|---|
| moments | **instants** | eje x de las cinco, subtítulos fig. 1 y 3 |
| adviser | **advisor** | fig. 2 |
| match | **game** | «partida N» → «game N» en fig. 1, 2, 3, 4; fig. 5 |
| journeys | **trips** | fig. 4 y fig. 5 |
| how far it is from where it should be | **how far it is from its place** | fig. 1, panel 3 |
| danger it senses | **threat it senses** | fig. 3, panel 2 |
| peligro que percibe | **amenaza que percibe** | fig. 3 `_es` |

Se encontró además un «and at no moment does it stop lacking something» en el
subtítulo de la fig. 1 `_en`; ahora dice «instant». Rastreo final: **no queda
ninguna palabra vieja del glosario en las `_en`**, y `"match "` ya no aparece
como «partida». El glosario se aplicó también a los bloques *CAPTION (plain
English)* de los cinco `.txt`.

### A.3 · La leyenda de la fig. 2

La leyenda tapaba la línea gris. Ahora va en `lower right`
(`bbox_to_anchor=(1.0, 0.04)`), en la franja libre entre 2,6 y 2,85, por debajo
de las tres curvas. El rótulo «aquí abandona el plan» / «here it abandons the
plan» ya no se cruza con la línea de puntos vertical: va **horizontal**, a la
derecha de esa línea y a y = 3,245, en la banda libre entre la curva azul
(3,12) y la gris (3,36). Se probó primero en vertical, pegado a la línea, y en
la versión `_en` el texto —más largo— subía hasta 3,20 y **pisaba la curva
azul**; la colocación horizontal no depende del largo del texto.

### A.4 · Revisión PNG a PNG

Se reabrieron los diez. Dos choques más encontrados y arreglados sobre la marcha:

1. **fig. 1, panel de arriba.** «quieta al empezar» / «still at the start» y «el
   anillo empieza a avisar» / «the ring starts warning» se escribían a y = 104,
   con la línea azul de vida clavada en 100: las letras la pisaban. El techo del
   panel pasa de 108 a 126 y los dos rótulos a y = 109 con `va="bottom"`.
2. **fig. 1, «primer golpe recibido».** La flecha cruzaba la línea rosa del
   anillo. El rótulo se reancla a la derecha de esa línea (`ha="right"`,
   `xytext=(g0-380, 42)`), y la flecha queda corta y limpia.

**Comprobado en los diez: ningún texto queda encima de ninguna línea.**

### A.5 · Un rótulo que las preguntas obligaron a cambiar (fig. 4)

La pregunta B.4 demostró que «llega y descansa» / «arrives and rests» es
**falso**: ningún viaje de esa vida —ni de las cuarenta partidas— pisa su
destino. No se podía entregar la figura con ese rótulo. Ahora dice:

* `es`: **se completa (cobra lo prometido)** · **se atasca (3 pasos sin acercarse)**
* `en`: **completes (collects what it promised)** · **gets stuck (3 steps without closing in)**

El `.txt` de la fig. 4 lleva el aviso completo, y el de la fig. 2 una precisión
sobre qué significa «llegó al destino» (ver B.2 y B.3).

---

## B · LAS SEIS PREGUNTAS

Diarios usados:

* **D1** = `paintball/runs/P57C_t2_A_20994019/ereq_119bda6a-02b1-4dd7-a3d7-28ca81ec0bbf-policy_agent_10.art.log` (fig. 1 y 3)
* **D2** = `paintball/runs/P56C_t5_F_22250767/ereq_31c2035c-f421-4e89-8d81-a1a6440f771a-policy_agent_10.art.log` (fig. 2)
* **D4** = `paintball/runs/P58M_t0_K_20260916/ereq_619f7d80-448d-480d-8e46-2e199fa6c6aa-policy_agent_11.art.log` (fig. 4)

---

### B.1 · La mancha del panel de abajo de la fig. 1

**Qué fila cambia:** dos, y siempre juntas: **`F-4-ALCANCE`** y
**`S-8-EXPOSICION`**. No cambian de valor: **entran y salen de la tabla**.
Las otras tres filas del tramo están clavadas (`R-CARENCIA` 1,0 ·
`R-ACOPIO` 0,18 · `R-LLAMADA` oscila solo entre 0,10001 y 0,12).

**Cada cuántos tics:** **período 22 tics** — once dentro, once fuera. En la
ventana 2.200–8.000 hay **264 bloques** con las dos filas, **263 de ellos de
exactamente 11 tics** (el primero sale cortado por el borde de la ventana), y
**527 movimientos, uno cada 11 tics sin una sola excepción**. El malestar salta
entre **3,26065** (sin las filas) y **3,6767** (con ellas): esos 0,416 son los
0,4591 de `F-4-ALCANCE` más los 0,04368 de `S-8-EXPOSICION` repartidos por
`REPARTO`.

**Por qué:** el cuerpo hace un **vaivén de dos casillas**, `(19,13)` ↔ `(18,12)`,
y desde una ve al rival y desde la otra no.

```
tic 2208 [19,13] intencion {"type":"move","dir":"NW"}   ← elegido: ir_objeto  (d 3,49178)
tic 2209 [18,12] filas = {R-ACOPIO, R-CARENCIA, R-LLAMADA}        d_ahora 3,26065
tic 2219 [18,12] intencion {"type":"move","dir":"SE"}   ← elegido: ir_botin   (d 3,18526)
tic 2220 [19,13] filas = {F-4-ALCANCE, R-ACOPIO, R-CARENCIA, R-LLAMADA, S-8-EXPOSICION}
                                                                   d_ahora 3,67668
```

En los 5.801 tics de la ventana el cuerpo ocupa **solo dos casillas**: `(19,13)`
2.902 tics y `(18,12)` 2.899. El rival que enciende las dos filas es el **slot 8
del equipo E**, que **no se mueve**: `ve_agentes` lo da en `(16,21)` en los 2.902
tics en que se le ve, y en ninguno más. Las distancias:

| desde | a (16,21) | euclídea | Δx, Δy | ¿lo ve? |
|---|---|---|---|---|
| `(19,13)` | slot 8 | 8,544 | 3, 8 | **sí** |
| `(18,12)` | slot 8 | 9,219 | 2, 9 | **no** |

La ventana de observación corta justo entre las dos (Δy 8 sí, Δy 9 no). *La
forma exacta de esa ventana no está en el `player_config` del diario; lo que el
diario certifica es que desde `(19,13)` aparece en `ve_agentes` y desde `(18,12)`
no.* Sin rival en `ve_agentes`, `F-4-ALCANCE` y `S-8-EXPOSICION` no se escriben:
las dos recorren `vis["agents"]` saltándose el propio slot y la pareja
(`appraisal_zs_v42_exp.py:1060-1070` y `:1402-1416`).

**Y el vaivén, ¿por qué?** Es un bucle de dos tiempos entre dos candidatos:

* desde `(19,13)` gana **`ir_objeto`** (3,49178), que promete bajar
  `R-CARENCIA` de 1,0 a 0,83333 yendo a por las flechas de `(18,15)`, y cuyo
  primer paso es `(18,12)`;
* desde `(18,12)` **`ir_objeto` ya no se genera** (264 veces está en la lista
  desde `(19,13)`, **0 veces** desde `(18,12)`) y gana **`ir_botin`** (3,18526),
  cuyo primer paso es volver a `(19,13)`.

Las flechas de `(18,15)` siguen ahí, sin tocar, todo el rato (`ve_items` las da
en `(18,15)` desde antes del 2.200 hasta después del 8.000) y **el cuerpo nunca
las coge**: `hand` es `none` en toda la ventana.

El vaivén dura del **tic 2.033 al 8.027** (5.995 tics seguidos), que es
**exactamente la meseta de calma de la fig. 3** (1.977 → 8.027). La mancha de
la fig. 1 y la meseta de la fig. 3 son el mismo hecho visto por dos ventanas.

*(No se cambió la figura, como pedía el encargo.)*

---

### B.2 · La fig. 2 después del abandono

#### ¿Llegó el cuerpo a (22,22) por su cuenta?

**Dentro del plan, no. En toda la partida, sí, pero 5.615 instantes después y
con el premio ya perdido.**

El plan cae en el **4.062**, con el cuerpo en `(22,19)`. Lo que hace después,
casilla a casilla (D2):

```
4055 (22,19)   4066 (23,20)   4077 (24,19)   4088 (25,18)
4099 (25,19)   4110 (24,20)   4121 (25,19)   4132 (24,20)  …
```

Es decir: **se va al noreste y se mete en otro vaivén de dos casillas**,
`(24,20)` ↔ `(25,19)`, igual que el de B.1.

Pisa `(22,22)` **por primera y única vez en el instante 9.677**, y se queda
allí hasta el final de su vida (9.840). Para entonces **la espada ya no está**:
`ve_items` la da en `(22,22)` desde el tic **581** hasta el **8.072**, y en el
9.677 esa casilla está vacía. El cuerpo termina la partida con `hand = none`:
**en toda su vida no llegó a empuñar nada** (la mano cambia una sola vez, en el
tic 481, de `null` a `none`).

#### ¿Por qué la realidad (2,61) salió medio punto mejor que lo imaginado (3,11)?

**Sí: es la regla de honestidad, y es casi todo el hueco.** Cuantificado:

| en el instante 4.037 | d |
|---|---|
| lo imaginado por la curva del plan (`curva_H`) | **3,11334** |
| lo que pasó de verdad (`d_ahora` del diario) | **2,61306** |
| lo que pasó de verdad, **recalculado con los pisos del nacimiento** | **3,13217** |

La regla vive en `cantera/paper5/forma.py:444-463` y `:646-652`:

```python
PISO_RIVAL = ("F-4-ALCANCE", "S-8-EXPOSICION", "S-7-AGRESOR",
              "MIEDO_APRENDIDO", "S-VIDA-AJENA")
...
M = float(F_.get(nom) or 0.0)
if pisos and nom in pisos:
    M = max(M, pisos[nom])          # las filas de los otros NO pueden mejorar
```

Al juzgar el plan (tic 4.001) la tabla real era:

```
F-4-ALCANCE 0,46831 · R-CARENCIA 0,66667 · R-LLAMADA 0,21123
S-DANO-PAREJA 0,17  · S-8-EXPOSICION 0,24726        d_ahora 3,38464
```

y en el 4.037:

```
R-CARENCIA 0,33333 · R-LLAMADA 0,13889 · S-DANO-PAREJA 0,17   d_ahora 2,61306
```

**`F-4-ALCANCE` y `S-8-EXPOSICION` desaparecieron**: el rival dejó de verse. La
imaginación tiene prohibido contar con eso —los pisos las mantienen en 0,46831 y
0,24726 para siempre—, así que proyectó 3,11334. Si a la tabla real del 4.037 se
le aplican esos mismos pisos sale **3,13217**: **0,500 de los 0,519 puntos de
hueco son exactamente la regla de honestidad**; los 0,019 restantes son el resto
de la proyección (la ración recogida y la llamada del botín).

Dicho llano: **la realidad no fue mejor que el plan; fue mejor que lo único que
al plan se le dejaba imaginar.** La mejora se la dio que el rival se fuera, y eso
es precisamente lo que la puerta se prohíbe apuntarse.

*(La ración sí se recogió: `pack` pasa de `[first_aid, null]` a
`[first_aid, rations×2]` entre el 4.004 y el 4.037, y `R-CARENCIA` baja de
0,66667 a 0,33333. El destino del tramo 1, `(23,17)`, se pisó del 4.033 al
4.044.)*

---

### B.3 · Qué es el 22,2 % de la fig. 2

Los dos números del `.txt` **tienen denominadores distintos** y la frase los
juntaba mal. Fuente: `informe_P58O.md:93-104`, medido por
`cantera/paper5/mide_P58O.py:54-100`.

| número | qué es exactamente | cuenta |
|---|---|---|
| **76,8 %** | **tics**, no formas: de los **280 tics** en que alguna de las 45 formas de F estaba viva y el cuerpo tenía las piernas listas (`move_ready_in == 0`), el candidato `_FM_` ganó en **215** | 215 / 280 |
| **22,2 %** | **formas**: de las **45 formas del brazo F** con ventana reconstruible, **10** llegaron a pisar el destino | **10 / 45** |

«Llegar» está definido así (`mide_P58O.py:97`): `llega = (dmin == 0)`, donde
`dmin` es el mínimo, sobre todos los tics de la ventana `forma_aceptada →
forma_caida`, de la **distancia de rey** entre la posición del cuerpo y el
**destino del PRIMER tramo que tenga uno** (`mide_P58O.py:56-58`).

Consecuencias que conviene decir en voz alta:

* No es el destino final del plan. La forma 7 de la fig. 2 cuenta como «llega»
  porque pisó `(23,17)` —tramo 1—, **no** porque pisara `(22,22)` —tramo 2—, que
  es lo que B.2 acaba de descartar.
* «La forma mediana» no es el sujeto de ninguno de los dos números: el 76,8 % es
  un agregado de tics sobre las 45 formas y el 22,2 % un recuento de formas.
* Las 45 formas de F vienen de las **86 con ventana reconstruible** de P5-8O
  (`informe_P58O.md:85`); las otras 41 son del brazo T, que llega el **51,2 %**
  (21 de 41) porque propone destinos a 2 casillas de mediana contra las 3 de F.

El `.txt` de la fig. 2 ya lleva las dos frases corregidas.

---

### B.4 · «Llega y descansa» contra «se completa»

**No son lo mismo, y la diferencia no es de matiz: es de todo o nada.**

#### Lo que dice el código

`paintball/alma/policy_forma.py:906-923` — **completada por alivio**:

```python
_baja = getattr(fv, "ign_nace", 0.0) - self.ojo.ignorancia_global()
_visto = (getattr(fv, "destino_cur", None) in self.ojo.primera_vez)
if (_pr > 0 and _baja >= _pr) or _visto:
    ...  "motivo": "completada por alivio"
```

Se cierra cuando **cobra la bajada de mapa que prometía** o cuando **la casilla
de destino se ve por primera vez**. Ninguna de las dos exige pisarla — y con
radio de visión, la casilla se ve antes de llegar.

`policy_forma.py:1008-1024` — **atasco**:

```python
d = max(abs(pos[0]-dest[0]), abs(pos[1]-dest[1]))     # distancia de rey
mejor, t_mejor = self.k_dist_min.get(fv.id, (d, self.tick))
if d < mejor: self.k_dist_min[fv.id] = (d, self.tick)
elif self.tick - t_mejor >= getattr(fv, "atasco_plazo", CUR_ATASCO_PASOS*11):
    ...  "motivo": "atasco"
```

O sea: **tres pasos del mundo (3 × 11 = 33 tics) sin mejorar en una sola casilla
la mejor distancia ya alcanzada**. No es «lo rodea un rival» ni «se le acaba el
tiempo de la partida»: es un cronómetro de progreso.

#### Las dos cifras con la misma definición

| definición | esta vida (18 viajes) | las cuarenta partidas (209 viajes) |
|---|---|---|
| **«se completa»** = motivo `completada por alivio` | **5 = 27,8 %** | **144 = 68,9 %** |
| **«llega»** = el cuerpo pisa la casilla de destino | **0 = 0,0 %** | **0 = 0,0 %** |

**Cero de 209.** La distancia mínima alcanzada al destino, en los 209 viajes de
los 39 diarios de K (208 de los 209 dan ventana medible): **1 casilla en 81**,
**2 en 85**, 3 en 13, 4 en 3, 5 en 4, 6 en 17, 7 en 3, 8 en 2. El viaje se
apaga sistemáticamente a una o dos casillas.

De las 5 «completadas» de esta vida, **4 lo fueron por ver el destino**
(`destino_visto: true`) y **1 por cobrar la promesa** (id 3: `baja 0,03776 ≥
promesa 0,03646`, `destino_visto: false`).

#### Los 18 viajes de esta vida

Destino leído de `forma_propuesta`; `d0` = distancia de rey al nacer; `dmín` = lo
más cerca que llegó; ninguno pisa el destino.

| id | nace | acaba | vive | destino | d0 | dmín | cómo acabó |
|---|---|---|---|---|---|---|---|
| 2 | 531 | 548 | 17 | (26,16) | 3 | 1 | completada por alivio (destino visto) |
| 3 | 598 | 669 | 71 | (25,21) | 7 | 3 | completada por alivio (promesa cobrada) |
| 4 | 768 | 801 | 33 | (19,22) | 5 | 2 | completada por alivio (destino visto) |
| 45 | 3.364 | 3.386 | 22 | (20,29) | 4 | 2 | completada por alivio (destino visto) |
| 46 | 3.436 | 3.487 | 51 | (21,29) | 5 | 2 | atasco |
| 47 | 3.542 | 3.597 | 55 | (21,29) | 5 | 2 | atasco |
| 48 | 3.652 | 3.707 | 55 | (21,29) | 5 | 2 | atasco |
| 49 | 3.762 | 3.817 | 55 | (21,29) | 5 | 2 | atasco |
| 50 | 3.872 | 3.927 | 55 | (21,29) | 5 | 2 | atasco |
| 51 | 3.982 | 4.037 | 55 | (21,29) | 5 | 2 | atasco |
| 52 | 4.092 | 4.147 | 55 | (21,29) | 5 | 2 | atasco |
| 53 | 4.202 | 4.257 | 55 | (21,29) | 5 | 2 | atasco |
| 54 | 4.312 | 4.367 | 55 | (21,29) | 5 | 2 | atasco |
| 55 | 4.422 | 4.477 | 55 | (21,29) | 5 | 2 | atasco |
| 56 | 4.532 | 4.587 | 55 | (21,29) | 5 | 2 | atasco |
| 57 | 4.642 | 4.697 | 55 | (21,29) | 5 | 2 | atasco |
| 58 | 4.752 | 4.807 | 55 | (21,29) | 5 | 2 | atasco |
| 59 | 4.862 | 4.906 | 44 | (21,29) | 5 | 1 | completada por alivio (destino visto) |

Salta a la vista: **trece intentos seguidos al mismo destino, `(21,29)`, todos
de 55 tics clavados**, todos atascados a 2 casillas. Los 55 son el reloj
honesto: `no_antes_de = tick + dist * _paso` = 5 casillas × 11 tics
(`policy_forma.py:1078-1079`), así que el primer examen cae justo en la llegada
proyectada y el atasco se dictamina ahí. Con el refractario de 50 tics detrás,
la cadencia de nacimientos sale de **110 tics**: 3.542, 3.652, 3.762, 3.872,
3.982… El decimocuarto intento, el id 59, acaba distinto solo porque **ve** la
casilla.

---

### B.5 · Por qué no nace ningún viaje después del tic 5.000

**Sale directo del diario.** Son dos causas encadenadas, no una.

**(1) Del 4.907 al 8.337: la amenaza.** `_cita_curiosidad` no propone nada si
`am >= CFM.UMBRAL_SEGURO` (= 0,2; `policy_forma.py:1048`,
`curiosidad_forma.py:38`). En los **3.433 tics** de ese hueco, el registro
`cur_forma_tic` da amenaza **< 0,2 en solo 11**:

* **4.914–4.925** (9 tics) — caen dentro del **refractario** de 50 tics que
  arranca al morir el viaje 59 en el 4.906 (`CUR_REFRACTARIO = 50`), o sea hasta
  el 4.956;
* **8.338–8.339** (2 tics) — y ahí, en efecto, **nace el viaje 60**
  (`cur_forma_tic` del 8.339: `"nacidas": 60`).

La amenaza mediana en el hueco es **0,71429**. `vivas: 0` y `activa: null` en
los 3.433. No hay ni un `cur_forma_saltada` en toda la partida: no llega ni a
intentarlo.

**(2) Del 8.338 al 9.650: la puerta.** Se proponen **17 viajes** (ids 60 a 76) y
**la puerta los tumba los 17**. Dieciséis con `veredicto: "area"` y uno con
`veredicto: "vida"`:

```
{"k":"forma_evaluada","tick":8338,"id":60,"veredicto":"area","ventaja":-0.01111,"margen":0.02,"C":0.3}
{"k":"forma_evaluada","tick":9070,"id":65,"veredicto":"area","ventaja": 0.00136,"margen":0.02,"C":0.3}
{"k":"forma_evaluada","tick":9537,"id":74,"veredicto":"vida","ventaja":-0.03254,"margen":0.02,"C":0.3}
{"k":"forma_evaluada","tick":9650,"id":76,"veredicto":"area","ventaja":-0.00117,"margen":0.02,"C":0.3}
```

La mejor ventaja de los diecisiete es **+0,00455** (id 70, tic 9.335) contra un
margen de **0,02**: ni de lejos. El cuerpo muere en el 9.709
(`"reason": "eliminated"`, puesto 12).

**Resumen:** los 18 viajes de la figura son todos los que nacieron; después del
4.906 la partida se vuelve peligrosa y se queda peligrosa, y cuando por fin
afloja, la curiosidad ya no compra nada que gane el margen.

---

### B.6 · De 908 momentos a 845

Fuente: `cantera/paper5/banco_llaves3.py:240-290` y el detalle
`cantera/paper5/P52c_detalle.json` (tabla publicada en `informe_P52c.md:36-40`).

**Los 63 que se caen son «caducadas»**, y el reparto es exacto:

| O-después, vida entera | n |
|---|---|
| aceptada | 72 |
| rechazada | 773 |
| **caducada** | **63** |
| **compiten** | **845** |

**Qué les pasa a los 63.** Los 63 son un **subconjunto estricto** de las **125
escenas en que el cuerpo acaba los 100 tics en la misma casilla en que
empezó** (`sin_moverse: true`, `pasos: 0`). En esas escenas el consejo bueno es
«quédate donde estás», y el traductor lo convierte en «ve a la casilla (x,y)»
con (x,y) = su propia casilla. `CX.ata` devuelve `None` cuando el destino
coincide con la posición:

```python
# paintball/alma/cortex_t5.py:659-661
q = _casilla_de(obj, obs, mundo, mem, tick)
if q is None or q == pos:
    return None
```

**El canal no sabe decir «no te muevas».** La propuesta es *intraducible*, no
rechazada: no llega a competir nunca.

**Y por qué 63 y no 125.** Porque en el criterio de vida entera la propuesta se
vuelve a juzgar en **cada** tic con las piernas listas de los cien, y el destino
es una casilla fija. De las 125:

| de las 125 escenas «sin moverse» | n |
|---|---|
| **caducada** (intraducible en los 101 tics: el cuerpo **nunca** se apartó) | **63** |
| rechazada (en algún tic se había apartado, y entonces sí se pudo traducir) | 57 |
| aceptada (ídem, y además ganó) | 5 |

Las 62 que sí compiten son escenas en que el cuerpo **salió de la casilla y
volvió**: mientras estuvo fuera, el destino ya no era su propia casilla y el
consejo se pudo expresar. *(En el criterio «ventana», que solo mira el primer
tic con piernas listas, caducan las **125** enteras: `informe_P52c.md:31`.)*

**El denominador de 845 es el mismo en los dos brazos por construcción.** El
azar emparejado sortea una casilla **a la misma distancia** que la del consejo
bueno; cuando esa distancia es 0, la casilla sorteada es también la propia, y
también es intraducible. Comprobado: las 63 caducadas de `azarp` son
**exactamente las mismas 63 escenas** (mismo `eid`, `slot` y `t0`) que las de
`despues`. Por eso las dos filas comparan 845 contra 845 y el 8,52 % y el
7,22 % son comparables.

---

## LO QUE SE ENTREGA

```
cantera/paper5/figuras_paper5/
  fig1_una_vida_es.png              fig1_una_vida_en.png
  fig2_forma_de_un_plan_es.png      fig2_forma_de_un_plan_en.png
  fig3_meseta_de_calma_es.png       fig3_meseta_de_calma_en.png
  fig4_una_vida_curiosa_es.png      fig4_una_vida_curiosa_en.png
  fig5_cuanto_mundo_conoce_es.png   fig5_cuanto_mundo_conoce_en.png
  fig1_una_vida.txt · fig2_forma_de_un_plan.txt · fig3_meseta_de_calma.txt
  fig4_una_vida_curiosa.txt · fig5_cuanto_mundo_conoce.txt
cantera/paper5/informe_P5FIG2.md    (este informe)
```

## LO QUE ESTE ENCARGO OBLIGA A CORREGIR EN EL PAPER

1. **«llega y descansa» no existe.** Ningún viaje de curiosidad pisa su destino:
   **0 de 209**. Donde el paper diga que los viajes «llegan», debe decir que **se
   completan**, y explicar que completarse es cobrar la bajada de mapa o ver la
   casilla.
2. **El 22,2 % y el 76,8 % no comparten sujeto.** 215/280 **tics** contra 10/45
   **formas**, y «llegar» es pisar el destino del **primer** tramo.
3. **La ventaja de la fig. 2 es en buena parte la regla de honestidad.** De los
   0,519 puntos que la realidad le saca a lo imaginado en el 4.037, **0,500 son
   los pisos del rival**. Es un resultado honesto, pero hay que leerlo así.
4. **El plan de la fig. 2 no se anduvo entero.** `(22,22)` se pisó 5.615
   instantes después de abandonarlo, con la espada ya cogida por otro.

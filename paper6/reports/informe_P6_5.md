# P6-5 · El reparto entre hermanos: primero medir el daño

*Sólo lectura de los 40 diarios del brazo A1 de P6-4. **No se jugó ninguna
partida: coste cero.** `motor/model.py` intacto
(`1e511978c251130e95169ebf8443efa1`) y los 199 archivos de `CONGELADO.md` sin
alterar, comprobados. Nada subido, empujado ni borrado. Todo lo nuevo en
`cantera/paper6/`.*

**Las tres reglas nuevas, aplicadas:** ningún número de este informe se escribió
antes de calcularlo; el daño se midió antes de construir; y **no hay humo de
punta a punta porque no hay nada que construir** — el punto 1 dice que pare.

---

## 1 · CUÁNTO CUESTAN DE VERDAD · **el daño es pequeño. PARO. No construyo.**

### Antes de la cifra: el 712 de P6-4 estaba mal, y era mío

En P6-4 conté como «los dos hermanos yendo a por el mismo recurso» los tics en
que las dos `pos_prevista` coincidían. **Eso está mal**: `noop` tiene
`pos_prevista` igual a la casilla donde uno ya está, así que contaba «el hermano
camina hacia donde el otro está quieto» como disputa. De los 712, la mayoría son
eso.

### La medida buena

El objetivo de `ir_objeto` se reconstruye llamando al **mismo**
`decisor_zs._mejor_objeto` que lo eligió, sobre una memoria replicada tic a tic
desde el principio del episodio y **con la misma inyección de los ojos** (los
partes E2 se releen del `chat` del diario y se pasan por `oyente2.inyecta`).
Hay disputa cuando los dos, con las piernas listas en el mismo tic, eligen
`ir_objeto` y la función les devuelve **la misma casilla**.

| | n |
|---|---:|
| tics con los dos en piernas listas | 36.188 |
| tics con los dos persiguiendo algún objeto | 1.055 |
| …de los cuales `coger`/`coger` (**cada uno lo que pisa: no hay disputa posible**) | **830** |
| tics con los dos en `ir_objeto` y objetivo legible | **90** |
| …con objetivos **distintos** | **44** |
| …con el **mismo** objetivo | **46** |
| **EVENTOS de disputa** (misma casilla, tics contiguos) | **22** |
| en cuántas partidas | **15 de 20** |
| **por vida** | **0,55** |

### Qué pasó en esas 22, una a una

| | n |
|---|---:|
| llegan **los dos** a la casilla | **13** |
| no llega **ninguno** | 4 |
| …y el objeto **desaparece** (rival o fuego) | **3** |
| llega **sólo uno** | 5 |

| | |
|---|---|
| **instantes que pierde el que llega segundo** | mediana **22** · media 29 · máximo 56 |
| **suma en las 40 vidas** | **371 tics** |
| **por vida** | **9,3 tics = 0,39 segundos** |
| **sobre una vida mediana de 12.841 tics** | **0,072 %** |
| **objetos perdidos a un rival** | **3 en 40 vidas** |
| **veces que lo coge el que MENOS lo necesitaba** | **0** |

Esa última fila es la que mata el encargo: de los 15 eventos con clase de objeto
conocida, en **13 los dos estaban igual de necesitados** (ninguno llevaba nada
de esa clase) y en 2 **los dos ya llevaban**. **Cero veces se lo llevó el que
menos falta le hacía.** La regla del punto 3 está diseñada para arreglar algo
que no ocurre.

### Y hay un patrón que conviene ver

| evento | partida | tic | objeto | llegadas | desaparece |
|---|---|---:|---|---|---:|
| 8 | `21203477` | 613 | `first_aid` | 10@614 · 11@636 | 615 |
| 9 | `21308206` | 580 | `first_aid` | 10@592 · 11@614 | 593 |
| 14 | `21936580` | 591 | `first_aid` | 10@592 · 11@614 | 593 |
| 22 | `22250767` | 547 | `first_aid` | 10@592 · 11@614 | 593 |

**El primero llega, lo coge, y el objeto desaparece un tic después.** El segundo
llega veintidós tics más tarde —dos pasos— y se encuentra la casilla vacía. Eso
es todo el daño: **dos pasos de más, media vez por vida**.

Y **19 de los 22 eventos ocurren entre los tics 481 y 700**: la carrera inicial
hacia la Fortaleza, cuando los dos salen del pedestal a por lo mismo porque
está todo en el mismo sitio. No es un fallo de coordinación: es que el botín
bueno está junto.

*(Siete de los 22 no tienen objeto legible en el diario —`id: None`—: la casilla
venía de la memoria y no estaba en `ve_items` en ese tic. Seis de esos siete
son la misma casilla de la misma partida, `[29,16]` de `22146038`.)*

### LA DECISIÓN

**0,55 eventos por vida, 9,3 tics perdidos por vida (0,072 % de una vida), 3
objetos perdidos en 40 vidas y cero repartos injustos.**

**El daño es pequeño. Paro aquí y no construyo el reparto.** Los puntos 3 y 4
del encargo están condicionados a que el daño no fuera pequeño, y no lo es.

---

## 2 · ¿SE PUEDEN DAR OBJETOS?

Sólo lo que dice el juego. Fuentes: el protocolo `zero_sum.player.v1` y el
`readme`, los dos del manifiesto de `cow_6a55df20-…` (0.1.19).

### Soltar: SÍ, y es una acción de primera clase

La lista de acciones del protocolo es **cerrada** y está entera aquí:

```
{"type": "action", "do": "move",   "dir": "N|NE|E|SE|S|SW|W|NW"}
{"type": "action", "do": "attack", "dir": "N|NE|E|SE|S|SW|W|NW"}
{"type": "action", "do": "pickup"}
{"type": "action", "do": "drop", "slot": -1}   // -1 mano, -2 cuerpo, 0..3 mochila
{"type": "action", "do": "use",  "slot": 0}
{"type": "action", "do": "interact"}
{"type": "action", "do": "none"}
```

**Se puede soltar cualquier cosa**: la mano (`-1`), el cuerpo (`-2`) o
cualquiera de las cuatro ranuras de la mochila (`0..3`).

### Dar directamente: NO EXISTE

En esa lista **no hay `give` ni `transfer` ni nada equivalente** (comprobado:
cero apariciones de «give» y «transfer» en los 6.242 caracteres del protocolo).
**Dar un objeto es, necesariamente, soltarlo y que el otro lo recoja.**

### ¿Puede el compañero recogerlo? SÍ

`{"do":"pickup"}` recoge del suelo **donde estás**. El compañero sólo tiene que
pisar esa casilla. Es exactamente la mecánica que el cuerpo del paper cinco ya
modela: `S-PROVISION` y `S-HERIDO` miran «una cura **en el suelo** a ≤ 2
casillas del hermano» y exigen que la casilla sea **pisable por él** —ni la mía
ni la de un tercero— (`appraisal_zs_v42_exp.py:1150-1168`). El código ya sabe
que dar es soltar y apartarse.

### ¿Puede un rival recogerlo también? SÍ, y el juego lo dice dos veces

* `readme`: de los regalos del patrocinador, **«once landed, ANYONE can loot
  it»**, y *«contested airdrops are the point»* (protocolo, línea 84).
* `readme`: **«Dead contestants drop everything where they fall»** — lo que cae
  al suelo queda para quien pase.
* Y lo decisivo: **en el esquema de observación un objeto del suelo es
  `{"id", "n", "pos"}`** (más `durability` en las armas). **No hay ningún campo
  de dueño, reserva ni equipo.** Rastreé «owner», «mine», «yours», «reserved» y
  «claim» en el protocolo y en el readme: **ninguna aparición** referida a
  objetos del suelo.

### Resumen, con lo que el juego no aclara

| pregunta | respuesta | fuente |
|---|---|---|
| ¿se puede soltar? | **sí**, mano, cuerpo o mochila | protocolo, lista de acciones |
| ¿dar directamente? | **no existe** | la lista es cerrada |
| ¿puede recogerlo el compañero? | **sí**, pisando la casilla | `do: pickup` |
| ¿puede recogerlo un rival? | **sí** | «ANYONE can loot it»; sin campo de dueño |
| ¿cuánto tarda un `drop`? | **no lo dice** | el protocolo no publica enfriamiento de `drop` |
| ¿qué pasa si dos pisan la casilla a la vez? | **no lo dice** | no hay regla de desempate publicada |

Las dos últimas las dejo marcadas como **no sé**: no están en el protocolo ni
en el readme, y no las voy a suponer.

---

## 3 y 4 · NO HECHOS, Y POR QUÉ

El encargo los condiciona: *«SI EL DAÑO NO ES PEQUEÑO»*. **Es pequeño**, así que
no he escrito ni una línea de la regla de reparto, ni el banco que la evaluaría.

Lo que sí puedo dejar dicho, porque sale gratis de lo ya medido y ahorra trabajo
si algún día se retoma:

* **El campo «voy a por X» cabría.** El parte E2 tiene hoy una mediana de 100
  caracteres de 120 (P6-4, 19.642 partes). Un objetivo `>t<x>,<y>` cuesta 5-6
  caracteres. **Pero no lo he comprobado midiéndolo**, porque no toca: cuando
  toque, se mide y se dice el número, no se estima.
* **El umbral de «diferencia pequeña de distancias» tendría un anclaje claro**:
  el paso del cuerpo son **11 tics por casilla** (leído del mundo,
  `coste_movimiento(speed 5)`). Una casilla de diferencia es un paso. En los 22
  eventos medidos, la diferencia de distancias fue de 0 a 7 casillas, mediana 2.
* **La regla no habría cambiado nada en 13 de los 15 eventos con clase
  conocida**, porque los dos estaban igual de necesitados: el criterio de
  necesidad no desempata, y quedaría el de distancia — que es lo que ya hace el
  mundo solo, porque el más cercano llega antes.

---

## LO QUE ME LLEVO

1. **El 712 de P6-4 era mío y estaba mal.** Contaba `noop` como persecución. La
   cifra buena es **22 eventos en 20 partidas**.
2. **El daño real es 9,3 tics por vida**, el 0,072 % de una vida, y **cero
   repartos injustos** en 40 vidas. La regla del punto 3 arreglaría algo que no
   pasa.
3. **Casi todo ocurre en la carrera inicial** (19 de 22 entre los tics 481 y
   700), porque el botín bueno está todo en el mismo sitio. Si alguna vez
   molesta, es ahí y no en el resto de la partida.
4. **Dar un objeto es soltarlo**, y **cualquiera puede cogerlo** — incluido un
   rival. El cuerpo del cinco ya lo sabía y lo modelaba.
5. **Las reglas nuevas funcionan.** Medir antes de construir ha ahorrado
   construir una regla, una política, una imagen y una serie de pago para un
   problema de cuatro décimas de segundo por vida.

---

## LOS ARCHIVOS NUEVOS, CON SU MD5

| archivo | md5 |
|---|---|
| `cantera/paper6/mide_disputa_P6_5.py` | `1d3050eb58cbcb4042ff9fda0bc7567d` |
| `cantera/paper6/P6_5_disputas.json` | `cfb79f7540d3711334f27531eab3467d` |
| `cantera/paper6/P6_5_eventos.json` | `767e6cf7b4a9cd2058afced70167f55d` |

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

---
---

# PUNTO 5 · EL DON DEL PAPER TRES, A0 CONTRA A1

*Añadido a mitad del encargo. Coste de plataforma: cero.*

## 5.0 · POR QUÉ ESTE PUNTO TARDÓ: EL PRIMER NÚMERO ERA FALSO

La primera cuenta, contando tics con `elegido` = `soltar_*`, dio esto:

| | A0 (ojos apagados) | A1 (ojos encendidos) |
|---|---:|---:|
| tics con `soltar_*` | 12.764 | 8 |

Mil seiscientas veces más en A0. Por la regla nueva —**ningún número se escribe
antes de calcularlo**— no lo escribí: fui a ver qué era. El diario
`P64_t3_A0_22250767`, asiento 10, tenía 4.260 de esos tics él solo. Mirándolos
uno a uno:

```
tic   pos      elige             do      ar   mochila            suelo en mi casilla
1197  [25,22]  ir_pareja         move    ok   {'first_aid': 2}   []
1198  [24,21]  soltar_first_aid  drop    ok   {'first_aid': 2}   []
1199  [24,21]  coger             pickup  ok   {}                 ['first_aid']
1200  [24,21]  soltar_first_aid  drop    ok   {'first_aid': 2}   []
1201  [24,21]  coger             pickup  ok   {}                 ['first_aid']
...  (y así 4.260 tics)
```

**No son 12.764 dones: es un ciclo de dos tics.** `drop` suelta la pila entera
en la propia casilla; al tic siguiente el cuerpo la ve bajo sus pies, `coger`
gana, y vuelve a soltar. El objeto nunca se mueve de ahí.

No es el enfriamiento del movimiento: desde el tic 1208 `move_ready_in` es 0 y
hay 17 candidatos disponibles, y `soltar`/`coger` siguen ganando a todos.

### Por qué se repite: dos PROMPTs que se contradicen

La cesión existe justamente para cortar esto. `decisor_zs.py:900-904` marca lo
soltado como CEDIDO y `decisor_zs.py:480` esconde el candidato `coger` mientras
la cesión viva — el comentario lo dice con nombre y apellido: *«corta la
oscilación de s107 (dar y recuperar 23 veces)»*.

Pero la cesión caduca en `appraisal_zs_v42_exp.py:667-683`:

```python
if self.pareja_muerta or _curada:
    self.cedidos = {}
```

y `_curada` se calcula del parte fresco: `hp >= hp_max`. Mientras tanto,
`decisor_zs.py:508-513` abre el candidato `soltar` **también con el hermano
SANO**, por la vía PROVISION del PROMPT_59 (`_hermana_b0`: su parte dice que
lleva cero vendas).

> **El PROMPT_59 abre el don para un hermano sano; el PROMPT_24 borra la cesión
> precisamente porque el hermano está sano.** Cada tic se regala y cada tic se
> deshace el regalo.

Y en ese tramo el hermano estaba **a una casilla**, en `[23,21]`, eligiendo
`move_E` hacia `[24,21]` con `action_result: blocked` tic tras tic: no podía
entrar porque el que le regalaba estaba de pie encima del regalo.

## 5.1 · LA CUENTA BUENA: EPISODIOS, NO TICS

Definiciones de `mide_don_P6_5.py`, todas comprobables en el diario:

* **EPISODIO** — racha máxima de intentos de `soltar_<id>` en la misma casilla
  y el mismo id, con huecos ≤ 3 tics. Un episodio = un acto de dejar algo.
* **REABSORBIDO** — tras el último intento, el que soltó vuelve a tener el id en
  la mochila estando en esa casilla. Se lo ha recogido él.
* **EFECTIVO** — el episodio acaba con el objeto en el suelo (se va de la
  casilla, o muere, sin recuperarlo). **Solo estos pueden llegar al hermano.**
* **RECOGIDO** — el hermano pisa esa casilla después y su mochila sube en ese id.
* **USADO** — después de recogerlo, su mochila de ese id baja.
* **VIAJA** — el objeto soltado aparece como recurso contado en un parte E2 del
  que lo soltó.

| | A0 | A1 |
|---|---:|---:|
| asientos · tics vividos | 40 · 474.188 | 40 · 490.594 |
| intentos (tics `soltar_*`) | 12.764 | 8 |
| **episodios de don** | **615** | **8** |
| …reabsorbidos (se lo queda el que lo dio) | 564 | 1 |
| …**efectivos** (queda en el suelo) | **51** | **7** |
| de ellos, `first_aid` / `rations` | 21 / 30 | 4 / 3 |
| …**lo recoge el hermano** | **12** | **1** |
| …y **lo usa** | **11** | **1** |
| …**viaja en un parte E2** | **0 de 51** | **7 de 7** |

### Las tres respuestas pedidas

1. **¿Cuántas veces un hermano soltó algo para el otro?** 51 en A0 y 7 en A1
   (dones efectivos, en 20 partidas y 40 vidas por brazo). Los 615 y los 8 de
   la fila de arriba incluyen los que se deshacen solos.
2. **¿Cuántas lo recogió el hermano?** 12 de 51 en A0 (23,53 %) y 1 de 7 en A1
   (14,29 %). Mediana de espera en A0: 150 tics; el más lento, 1.435.
3. **¿Cuántas llegó a usarlo?** 11 de 12 en A0 y 1 de 1 en A1. **Casi todo lo
   que se recoge se usa**; el cuello de botella es recogerlo, no usarlo.

## 5.2 · ¿SE RECOGE MÁS CON LOS OJOS COMPARTIDOS? NO SE PUEDE DECIR

Lo que sí es cierto, y es nuevo: **la frase del paper tres ya no vale.** Decía
que *«el parte dice lo que uno lleva, nunca lo que ha dejado en el suelo»*. Con
los ojos compartidos, **los 7 dones efectivos de A1 viajaron los 7 en un parte
E2** como recurso contado, y en A0 **ninguno de los 51**. El canal ya lleva el
regalo.

Lo que **no** se puede decir es que por eso se recoja más:

| | recogidos | tasa | IC 95 % (Wilson) |
|---|---:|---:|---|
| A0 | 12 de 51 | 23,53 % | 14,00 % – 36,76 % |
| A1 | 1 de 7 | 14,29 % | 2,57 % – 51,31 % |

**Fisher exacto, dos colas: p = 1,000.** Con siete dones en A1 no hay forma de
distinguir nada: el intervalo de A1 se come el de A0 entero. La respuesta
honesta a *«¿se recoge más?»* es **no lo sé, y con estos datos no se puede
saber**. Para poder decirlo habría que provocar el don, no esperarlo.

## 5.3 · LO QUE SALIÓ POR EL CAMINO, Y ES MÁS GRAVE

Al preguntar por qué A1 tenía 8 dones y A0 615, la respuesta no estaba en quién
gana la decisión, sino en que **el candidato ni existía**:

| | A0 | A1 |
|---|---:|---:|
| tics con el candidato `soltar_*` disponible | 93.434 | 2.510 |
| tics con hermano visible + herido + consumible (puerta de la herida) | 3.435 | **2.510** |

En A1, la disponibilidad del don es **exactamente** igual a la puerta de la
herida. Es decir: **la vía PROVISION no se abrió ni una sola vez en las 20
partidas del brazo A1.** Y esa vía necesita un parte fresco del hermano.

### El cuerpo del cinco no entendió ni un parte en A1

El cinco lee el parte del hermano en **un solo sitio**, con un parser estricto
de marca:

```
appraisal_zs_v42_exp.py:578     p = PARTE.parsea(m.get("text") or "")
parte.py:48                     r"^E1 P(\d+) t(\d+) ..."
```

`policy_pareja` cambió la emisión a **E2**. `AlmaPareja._oye_e2` parsea el E2
para lo suyo (inyectar rivales y recursos), pero **nadie devuelve la cabeza del
parte al sitio donde el cinco la busca**. Medido con el mismo parser del cinco
sobre los diarios:

| | partes del hermano recibidos | los entiende el cinco |
|---|---:|---:|
| A0 | 9.282 | **9.282** |
| A1 | 18.315 | **0** |

En A1 llegaron **18.315 partes y el cuerpo no entendió ninguno**. Con
`mem.parte` siempre a `None`, `mem.parte_fresco(tick)` también, y se apaga en
cascada todo lo que el cinco sabía de su hermano por el canal. El censo de
filas lo enseña:

| fila | A0 | A1 | Δ p.p. |
|---|---:|---:|---:|
| **S-PROVISION** | 19,16 % | **0,00 %** | **−19,16** |
| S-8-EXPOSICION | 68,46 % | 51,52 % | −16,93 |
| R-ACOPIO | 56,59 % | 43,57 % | −13,02 |
| F-HERMANO-AMENAZA | 10,71 % | 4,71 % | −6,00 |
| S-HERIDO | 2,15 % | 0,13 % | −2,02 |
| **R-HERMANO-FALTA** | 1,17 % | **0,00 %** | −1,17 |
| **F-HERMANO-GOLPE** | 0,69 % | **0,00 %** | −0,69 |
| **S-DANO-PAREJA** | 20,53 % | **93,27 %** | **+72,74** |

Las tres filas que se van a cero son exactamente las que dependen del parte. Y
la subida de S-DANO-PAREJA tiene mecanismo exacto:
`Memoria.pareja_hp_est` (`appraisal_zs_v42_exp.py:500-510`) devuelve el hp
EXACTO con parte fresco y, sin él, `BANDA_EST["healthy"]` = **83**, no 100. Sin
parte, **un hermano sano parece herido al 17 % todo el rato**.

> **Consecuencia para P6-4.** Sus medidas son buenas como medidas, pero su
> etiqueta era falsa. No comparó «ojos apagados contra ojos encendidos»: comparó
> **«parte del hermano encendido, ojos apagados»** contra **«parte del hermano
> APAGADO, ojos encendidos»**. La serie no dice lo que dije que decía.

### Por qué el humo de P6-3 no lo cazó

`humo_P6_3.py:280` hacía `mem.parte = p` **a mano**. Eso prueba que el cuerpo
usa el parte si alguien se lo pone en la memoria; en la partida nadie se lo
pone. **Es el mismo fallo que el `hand` de P6-4**: el humo comprobaba mi forma,
no la del mundo. Dos veces el mismo error en dos encargos seguidos.

## 5.4 · EL REMIENDO, ESCRITO Y PROBADO, SIN ENGANCHAR

`cantera/paper6/oido5_P6_5.py`. No toca `model.py`, ni el paper cinco, ni
`policy_pareja.py`. **No está enganchado a nada**: la decisión es de Manel.

No escribe en `mem.parte` a mano —eso sería repetir el error—. Pone en el chat
un **mensaje GEMELO** con la cabeza traducida a E1, junto al E2, con el mismo
`from`, `channel` y `tick`. Así el parte entra por la puerta de siempre
(`Memoria.observa`) y hace todo lo que hacía en el cinco. La traducción se
**valida con el parser del cinco**: si `PARTE.parsea` no la acepta, no se
inyecta nada. El juez es el parser, no yo.

`cantera/paper6/humo_oido_P6_5.py` — **6 de 6**, con 900 partes E2 reales (400
del emisor de producción sobre tics reales + 500 dichos de verdad en A1):

| humo | qué prueba | resultado |
|---|---|---|
| a | el parser del cinco no entiende ni un E2 | 900 partes, 0 entendidos |
| b | `a_E1` da una línea que el cinco acepta, y los 9 campos coinciden | 900 traducciones iguales |
| c | punta a punta por `Memoria.observa` | sin gemelo `None`; con gemelo `t=491 hp=100 b=0` |
| d | la cascada | hp del hermano 83 (banda) → 100 (parte); `_hermana_b0` False → True |
| e | la puerta de S-PROVISION, en un tic real de A0 | tic 1120: sin gemelo `[]`, con gemelo `['soltar_first_aid']` |
| f | con los ojos apagados (E1) no hace nada | 0 gemelos, la misma obs, sin copia |

### Aviso: los dos arreglos van juntos

**Si se engancha el oído sin arreglar la cesión, vuelve el bucle del 5.0.** La
vía PROVISION se reabre y con ella la oscilación. El daño del bucle, medido:

| | |
|---|---:|
| tics perdidos en bucles en A0 | **24.859** de 474.188 (**5,24 %**) |
| episodios en bucle (≥ 3 intentos) | 549 de 615 |
| asientos afectados | **9 de 40** |
| episodio más largo | **3.723 tics** (el 28 % de esa vida) |
| asiento peor | `P64_t3_A0_22146038` s10, 337 episodios |

Eso **no es pequeño**, y es el tercer sitio donde la regla de medir antes de
construir cambia la decisión. Pero arreglarlo es cambiar la semántica de la
cesión del cinco, y eso **se propone, no se hace** (CLAUDE.md). Propuesta
mínima, en archivo nuevo y desde fuera, sin tocar el cinco:

> envolver `D.candidatos` para esconder `coger` cuando el objeto de mi casilla
> es uno que **yo mismo** solté hace menos de N tics — es decir, hacer que la
> cesión sobreviva al caso «hermano sano» que el PROMPT_59 abrió y el
> PROMPT_24 no previó. Falta calibrar N, y antes hay que medir cuánto tarda de
> verdad el hermano en llegar: **la mediana medida es 150 tics**, el máximo
> 1.435.

## 5.5 · LO QUE ME LLEVO DEL PUNTO 5

1. **El primer número era 1.600 veces el bueno.** 12.764 tics eran 615
   episodios, y de esos solo 51 dones de verdad. La regla lo paró antes de
   publicarlo.
2. **El don sigue vivo en el cuerpo, y funciona cuando llega**: 11 de los 12
   recogidos se usaron. Lo que falla es que llegue.
3. **La frase del paper tres ya no vale**: con ojos compartidos lo soltado viaja
   (7 de 7). Pero **no se puede decir que se recoja más** (p = 1,000, n = 7).
4. **A1 estaba sordo a su hermano**: 18.315 partes, 0 entendidos. Tres filas a
   cero y un hermano sano que parece herido al 17 % todo el rato. La etiqueta de
   P6-4 era falsa.
5. **Dos veces el mismo error de humo**: comprobar mi forma en vez de la del
   mundo. El humo nuevo compara siempre contra el juez del mundo — aquí, el
   parser del cinco.

## 5.6 · LOS ARCHIVOS DEL PUNTO 5, CON SU MD5

| archivo | md5 |
|---|---|
| `cantera/paper6/mide_don_P6_5.py` | `f5af677cd3b320973009d90d88793267` |
| `cantera/paper6/P6_5_don.json` | `fa7bb2a89808064771c04d463d17db19` |
| `cantera/paper6/mide_sordera_P6_5.py` | `9f06f09216850052afd9e4dda39a38c0` |
| `cantera/paper6/P6_5_sordera.json` | `955fab026e11d25648d1fa6002674184` |
| `cantera/paper6/oido5_P6_5.py` | `4f7aa3b3ddc4fc32e4b47c1356974415` |
| `cantera/paper6/humo_oido_P6_5.py` | `f4cee97f2fe7ad6e2977df0f1cc9a004` |

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

## 5.7 · CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — **intacto** |
| archivos de `CONGELADO.md` | 202 comprobados, **0 alterados** |
| `policy_pareja.py`, `parte2.py`, `oyente2.py` | **no tocados** (el remiendo va aparte) |
| partidas jugadas | **ninguna**. Coste de plataforma: **0,0000 USD** |
| patrones de clave (`sk-ant`, `api_key`, `token`, `secret`, `Bearer`) en los archivos nuevos | **ninguno** |
| `.env` en `.gitignore` | sí (líneas 57, 58, 70, 71) |
| subido, empujado o borrado | **nada** |

## 5.8 · LO QUE NECESITO DE MANEL

1. **¿Engancho el oído?** Está escrito y probado (6/6 humos). Es una línea en
   `policy_pareja.AlmaPareja.decidir`.
2. **¿Y la cesión?** Si se engancha el oído sin esto, vuelve el bucle de 24.859
   tics. La propuesta está en 5.4; falta decidir N y calibrarlo.
3. **¿Se repite P6-4?** Tal como salió, esa serie no comparó lo que dice su
   título. P6-4 costó **3,1831 USD** en total (de los cuales 0,7227 tirados por
   el fallo del `hand`), así que repetir los dos brazos cuesta del orden de esa
   cifra. No la lanzo sin tu palabra.

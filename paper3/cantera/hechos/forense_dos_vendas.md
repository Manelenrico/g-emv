# Forense — LAS DOS VENDAS (`ereq_9869b665`, tanda 66)

Fecha: 2026-09-08 · **Solo lectura**: no se ejecutó nada, no se tocó código.
Todo sale del diario ya grabado y de la lectura del decisor y del motor.

`md5 motor/model.py` = `1e511978c251130e95169ebf8443efa1` (sin tocar).

Episodio `ereq_9869b665-05fa-4755-a7b0-63476206c857` · tanda **66**
(`runs/manada2/`, alma **v35**) · el asiento con 16 de vida es el **10**; su
hermana es el **11**.

---

## 0 · La corrección de partida: **fue un solo tic, no varios**

Las dos vendas salieron en **una sola orden**, en el **tic 461**. No hubo dos
sueltos. La razón está en el zurrón: las vendas **se apilan en una única
ranura** (`pack: [{"id":"first_aid","n":2}, null]`), y un `drop` del mundo
suelta **la ranura entera**. En el tic siguiente el suelo muestra
`{"id":"first_aid","n":2,"pos":[23,20]}` y el zurrón está vacío.

**Y hay un desajuste que hay que declarar**: la foto que la ánima valoró
**preveía dar UNA**. `decisor_zs.py:363-371` (`_pack_sin`) descuenta `n` en uno,
no vacía la ranura. Es decir: **decidió dar una venda y el mundo dio las dos.**
Es la misma familia del fallo de apilamiento del PROMPT_60 (allí se contaban
ranuras en vez de unidades). Aquí no cambia quién ganó —el candidato era el
mismo—, pero **sí cambia lo que costó**: creyó quedarse con una y se quedó sin
ninguna.

---

## 1 · El tic 461, con los números del registro

Estado: **hp 16** en (23,20) · mano **vacía** · zurrón: **first_aid ×2** ·
hermana (11) a **1 casilla**, en (24,20) · agresor **P9 con espada** a 1,41 ·
`move_ready_in: 1`.

### 1.1 · Los candidatos que tenía — **solo dos**

```
"n_cand": 2,
"candidatos": {"noop": 4.92287, "soltar_first_aid": 4.92287},
"spread": 0.0,
"elegido": "soltar_first_aid"
```

**Empate exacto.** No hubo margen: los dos únicos candidatos valían **lo
mismo** hasta la quinta cifra, y `spread` = 0.

**Lo que NO estaba en la mesa, y por qué:**

| candidato | ¿estaba? | motivo, certificado |
|---|---|---|
| **curarse** (`usar_botiquin`) | **NO** | **vetado** por `Bloqueos.veta` — §2 |
| **moverse** (`move_*`, `paso_*`, `ir_*`) | **NO** | `move_ready_in: 1` > 0 → fuera del set (ARREGLO A, `decisor_zs.py:97-98`) |
| **golpear** (`atacar_*`) | **NO** | el único agresor, P9, figura con **`"en_alcance": false`**; y la mano estaba vacía (manos desnudas, alcance 1) |
| **coger** | **NO** | no había objeto en su casilla |
| **soltar** | **SÍ** | nació en este tic exacto — §1.3 |
| **noop** | SÍ | siempre está |

Para ver que esto no es interpretación: **un tic después**, con
`move_ready_in: 0`, el registro pasa a **`"n_cand": 17`** con los ocho rumbos,
las zancadas y los `ir_*`. Los movimientos no faltaban por gusto: faltaban
porque el mundo los tenía en enfriamiento.

### 1.2 · Qué filas pesaban (magnitud `M` en el tic 461)

| fila | M | signo | lectura |
|---|---|---|---|
| **F-DANO** | **1,05511** | − | **la dominante**: su propio cuerpo a 16 de vida |
| **R-CARENCIA** | 0,66667 | − | lo que le falta |
| **F-4-ALCANCE** | 0,50 | − | tiene un enemigo encima |
| **S-7-AGRESOR** | 0,50 | − | P9, que le ha hecho 83,4 en la ventana |
| **S-8-EXPOSICION** | 0,30 | − | cuatro hostiles a la vista |
| **S-DANO-PAREJA** | **0,24429** | − | **la hermana herida** ← la fila que abre el gesto |
| **R-LLAMADA** | 0,21123 | + | el botín de la cámara |
| S-VINCULO · S-HERIDO · S-PROVISION · S-COMPANIA · S-SOLEDAD · S-MUERTE-PAREJA | **0,0** | — | **todas mudas** |

**Dos cosas importantes para el paper:**

1. **La fila que mueve el gesto es S-DANO-PAREJA**, que es del **PROMPT_11/12**
   — de la temporada de la ánima sola, **no** del paper tres. Es exactamente la
   misma fila que produjo el don único de la ablación del 72. Las filas nuevas
   de la manada (S-VINCULO, S-HERIDO, S-PROVISION) están **a cero** en este
   tic.
2. **El dolor propio es cuatro veces mayor que el dolor por ella** (1,055
   contra 0,244). Aun así el gesto salió. No porque la quisiera más que a sí
   misma: porque —y esto es lo que hay que contar— **cuidarse no era una opción
   disponible**.

### 1.3 · El candidato nace en este tic exacto

En t459 y t460 el registro dice **`"n_cand": 1`** (solo `noop`) y
`"pareja_banda": "healthy"`. En **t461** la hermana recibe un espadazo de P9
(**19,8**: de 67 a 47), su banda pasa a **`"hurt"`**, y el candidato aparece.

Es literal en el código (`decisor_zs.py:511-513`):

```python
_herida59 = pareja is not None and \
    (pareja.get("hp_band") or "healthy") != "healthy"
```

**El gesto se abre con la BANDA visible, no con el parte.** El parte que tenía
en ese momento era de t433 —**28 tics de retraso**— y decía `hp 67.0`: por eso
las filas que se alimentan del parte (S-VINCULO, S-HERIDO) siguieron a cero
mientras el ojo ya veía "herida". La ánima reaccionó a lo que **vio**, no a lo
que le habían **contado**.

### 1.4 · Por qué ganó soltar estando empatado

`spread` = 0,0 ≤ `TIEBREAK_EPS` (1e-3) → entra la rama del **paisaje
degenerado** de `select_tiebreak`, y ahí lo primero que corre es
(`planificador_v1.py:461-464`):

```python
if exclude_noop:
    movers = [a for a in cand if a != "noop"]
    if movers:
        cand = movers
```

`decide()` la llama con **`exclude_noop=True`**. Traducido: **cuando hacer y no
hacer valen exactamente lo mismo, la casa manda hacer.** No ganó por margen:
ganó porque, en indiferencia genuina, la jerarquía de la casa excluye quedarse
quieto.

---

## 2 · Los diez segundos anteriores: **lo intentó dos veces y las dos se la cortaron**

Ventana t221–t461 (10 s × 24 tics). Todo el daño de la ventana viene del
**mismo** enemigo, **P9 con espada**.

| tic | qué pasó | vida |
|---|---|---|
| t352 | **coge** la primera venda | 76 |
| t386 | **coge** la segunda (se apilan: `n=2`) | 76 |
| **t387** | **`use` first_aid** → canal abierto | 76 |
| t388–t405 | `channeling` en los efectos — **18 tics de los 48** | 76 |
| **t406** | **espadazo de P9: −19,8** → **canal CANCELADO** | **76 → 56** |
| t425 | otro espadazo, sin canal abierto | 56 → 36 |
| **t436** | **`use` first_aid** otra vez | 36 |
| t437–t442 | `channeling` — **6 tics de los 48** | 36 |
| **t443** | **espadazo de P9: −19,8** → **canal CANCELADO** | **36 → 16** |
| t443–t460 | 18 tics quieta a 16 de vida, sin curarse | 16 |
| **t461** | **suelta las dos vendas** | 16 |

**Las dos curas se interrumpieron por golpes, y ninguna llegó a completarse.**
La venda pide **48 tics** de canal y el máximo que aguantó fueron **18**.
Balance de los diez segundos: **dos vendas gastadas en intentos, cero HP
curados** — el mundo no consume el kit al cancelar (`sim.nim:867-869`, "kit
kept"), por eso seguían las dos en el zurrón.

### 2.1 · Y por eso no podía intentarlo una tercera vez

Aquí está el nudo. `Bloqueos` (`decisor_zs.py:55-103`) arranca un veto al
emitir `use`:

```python
if res in ("ok", "cooldown"):
    self.canal_hasta = max(self.canal_hasta, tick + ut)
...
if nombre.startswith(("usar_", "empunar_", "ponerse_")):
    return tick < self.canal_hasta
```

Con `use_ticks` = 48: en t436 emitió `use`, recibió `ok`, y **`canal_hasta`
quedó en 484**. El canal murió de verdad en **t443**, pero **`Bloqueos` no se
entera nunca de las cancelaciones**: no lee `effects`, solo su propio reloj.

**Entre t443 y t484 la ánima se vetó a sí misma la cura creyendo que aún se
estaba curando.** El tic 461 cae justo en medio de esa ventana muerta de 41
tics.

(La regla no es caprichosa: nació en el PROMPT_06 midiendo un problema real
—reemitir `use` durante todo el canal costaba 149 tics en 7 episodios—. Lo que
no previó es el canal **cancelado**, que en zero-sum solo le pasa a la venda.)

---

## 3 · Por qué ganó soltar a curarse, en llano

**Porque curarse no estaba compitiendo.**

Dicho entero: a las 16 de vida, con la espada de P9 encima y la hermana herida
a una casilla, la ánima tenía sobre la mesa exactamente dos cosas —quedarse
quieta o dejar la medicina en el suelo— y valían lo mismo. La casa, ante un
empate exacto, prefiere actuar. Soltó.

Curarse no estaba porque dieciocho tics antes había pedido la cura, un espadazo
se la había cortado, y su propia contabilidad seguía creyendo que el canal
estaba en marcha. **No fue una elección entre cuidarse y cuidarla: fue lo único
que le quedaba por hacer.**

Lo cual, para el paper tres, se dice así de claro y no de otra manera:

- **A favor**: la fila social produce el gesto **en el peor momento posible**
  —16 de vida, un espadachín encima— y el gesto es coherente: la medicina cae a
  una casilla de la hermana herida, y por A.1 queda **cedida** (`mem.cedidos`),
  o sea que la ánima ya no la ve como suya.
- **En contra, y pesa**: el margen fue **cero**. Esta escena **no demuestra que
  cuidar venza a cuidarse**, porque cuidarse no llegó a la votación. Como
  evidencia de altruismo es de la clase más débil que hay: una indiferencia
  rota por la regla de la casa. **Si esta escena aparece en el paper, tiene que
  aparecer con esta frase al lado.**

---

## 4 · Cómo acabó

Nadie recogió las vendas.

- La hermana (11) **nunca las cogió**. En su último tic registrado, **t514**,
  está a **hp 8** y sigue viendo `{"id":"first_aid","n":2,"pos":[23,20]}` en el
  suelo, a una casilla. Muere ahí: **puesto 16, score 0**.
- La 10 aguanta a **16 de vida, sin curarse, 86 tics más**, y muere en **t547**:
  **puesto 15, score 0**.
- El recuento del propio mundo lo confirma: en `res_ereq_9869b665…json`,
  `gifts_received` vale **0** para los asientos 10 y 11 (y 1 para casi todos los
  demás).

**Dos vendas de 50 HP quedaron en el suelo entre dos hermanas que murieron con
16 y con 8 de vida.** Cualquiera de las dos las habría salvado. Ninguna volvió
a por ellas: la 10 porque su veto seguía activo hasta t484 y luego ya no tenía
nada en el zurrón; la 11 porque nunca fue candidato para ella.

---

## 5 · Lo que NO se puede afirmar

- **No se puede decir que soltar "venció" a curarse.** No compitieron.
- **No se sabe si `noop` y `soltar` eran idénticos por debajo de la quinta
  cifra.** El registro guarda `d` redondeada a 5 decimales y `spread` a 5. Lo
  que sí es cierto es que la rama que se ejecutó fue la del empate
  (`spread ≤ 1e-3`), y en esa rama el resultado no depende de la sexta cifra:
  `exclude_noop` decide.
- **No se ha reconstruido la valoración de `usar_botiquin`** en ese tic: como
  el candidato ni se creó, no hay número que leer. Saber si habría ganado exige
  **correr** la foto, y este encargo es sin correr nada.
- **No se ha comprobado si este veto-tras-cancelación pasa en más episodios.**
  Aquí está medido en uno. Contarlo en la tanda entera es otro encargo.

---

## Rutas de las fuentes

| ruta | qué aporta |
|---|---|
| `paintball/runs/manada2/ereq_9869b665-05fa-4755-a7b0-63476206c857/a10/…-policy_agent_10.log` | **la escena**: el bloque `RADIOGRAFIA` de cada tic (candidatos con su `d`, `spread`, `elegido`, tabla de filas, agresores, parte), el zurrón, los efectos `channeling` y el `damage_taken` con fuente y cantidad |
| `…/a11/…-policy_agent_11.log` | la hermana: hp 67→47 en t461, y las vendas aún en el suelo en su último tic (t514, hp 8) |
| `paintball/runs/manada2/res_ereq_9869b665-…json` | el desenlace del mundo: puestos 15 y 16, `gifts_received` 0 para ambas |
| `paintball/alma/decisor_zs.py` (55-103) | **`Bloqueos`**: el veto de `usar_*` por `canal_hasta`, y que solo se arranca al emitir, sin enterarse de las cancelaciones |
| `paintball/alma/decisor_zs.py` (484-513) | el candidato de curarse (`hp < hp_max`) y el de soltar (**abierto por la BANDA** de la hermana) |
| `paintball/alma/decisor_zs.py` (363-371) | `_pack_sin`: la foto prevé dar **una** unidad, no la ranura |
| `paintball/alma/decisor_zs.py` (895-903) | `select_tiebreak(..., exclude_noop=True, tie_unified=True)` y la cesión (`mem.cedidos`) |
| `planificador/planificador_v1.py` (446-464) | la rama del paisaje degenerado y **`exclude_noop`**: en empate exacto, actuar gana a quedarse quieto |
| `~/paintball_recon/docs/zero-sum/src/sim.nim` (867-869) | **cualquier daño cancela el canal de la venda**, y el kit no se pierde |
| `paintball/hecho_dano_armas.md` | los 19,8 de cada espadazo: espada 18 × (5+6)/10, cuerpo FUE 6 |

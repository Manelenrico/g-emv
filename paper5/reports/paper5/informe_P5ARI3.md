# P5-ARI3 — el preset `lento_v0` contra lo que de verdad pasó

**Solo lectura, coste cero.** Nada lanzado, nada enviado, nada cancelado. Motor,
decisor y tabla intocados (`1e511978c251130e95169ebf8443efa1` ·
`8fa03547e3228ef9df4aa94c444f9252` · `98c13d60167c80cc8334c965be75c640`).
**No aparece ninguna clave ni token ni el contenido de `.env`.**

---

## El titular

**La sección 3 dice la verdad en la letra y se pasa de frenada en el espíritu.**

**Usamos la clave exacta y correcta**, `sponsor.budget_per_team = 600`, contra un
defecto de 300 — **el doble, sí**. Pero:

- **el presupuesto no compró nada**: nuestro cuerpo **no tiene acción de compra**
  en ninguna de las tres piezas que deciden;
- **no hay una sola prueba de su efecto en los diarios**, porque nuestra propia
  política **descarta el bloque `sponsor` del `world_info`** antes de escribirlo;
- **los 16 regalos que sí se ven NO son el presupuesto**: son los del preset
  `Competition`, y **nuestros `scripted_gifts` coinciden con ellos tic por tic**,
  así que sean honrados o ignorados **el resultado es idéntico**.

**Y hay una clave nuestra que nunca existió**: mandamos `sponsor.live = false`,
pero el motor la llama **`enabled`** (`manifiesto:… "sponsor": {"enabled": true,
…}`). **Si `live` hubiera funcionado, habría apagado el patrocinador.** Funcionó
que la ignoraran.

**Los otros tres ajustes del preset sí se aplicaron, y se pueden medir uno a
uno.**

---

## 1 · El preset, clave por clave

### Lo que enviamos

`cantera/paper5/roster_lento_v1.json`, bloque `game_config_overrides`:

| clave | valor enviado | línea |
|---|---|---|
| `max_ticks` | **18240** | `roster_lento_v1.json` |
| `freeze_ticks` | **480** | ídem |
| `stat_budget` | **20** | ídem |
| `zone.schedule` | **7 filas**, de `[7296,7536,8076,24,19,1]` a `[14136,14376,14916,3,0,24]` | ídem |
| `sponsor.live` | **false** | ídem, `:89` |
| **`sponsor.budget_per_team`** | **600** | ídem |
| `sponsor.shop_opens_tick` | **1680** | ídem |
| `sponsor.scripted_gifts` | **lista de 16** | ídem |

El envío lo hace `cantera/paper5/lanza_P58M.py:32-35`, que carga ese fichero y
solo le cambia `cfg["seed"]`.

### La pregunta directa

> **¿Qué clave exacta usamos para el patrocinador y con qué valor? ¿Es
> `sponsor.budget_per_team`?**

**Sí. Usamos `sponsor.budget_per_team = 600`**, que es exactamente la clave que
Ari dice que es la única que el motor honra. **Contra el defecto de 300, es el
doble.**

**Pero mandamos otras tres claves de `sponsor` que, según Ari, se ignoran en
silencio** — y una de ellas ni siquiera tiene ese nombre en el motor:

| clave que mandamos | qué pasa | nuestro valor | el del motor |
|---|---|---|---|
| **`budget_per_team`** | **honrada** | **600** | defecto **300** |
| `shop_opens_tick` | ignorada | 1680 | defecto **1680** — *el mismo* |
| `scripted_gifts` | ignorada | 16 regalos | los 16 del preset, *idénticos* |
| **`live`** | **ignorada, y el motor la llama `enabled`** | **false** | defecto **true** |

**Las tres ignoradas eran inofensivas por casualidad**: dos coincidían con el
defecto y la tercera, de haber funcionado, habría apagado el patrocinador entero.

### Lo que el servidor devolvió

El `game_config` del episodio (`P58M_t0_K_20260916.json`,
`episodes[0].game_config`) **devuelve las cuatro claves de `sponsor` tal como las
mandamos**, incluida `live: false`. **Eso es un eco, no una prueba de efecto:**
el esquema del manifiesto declara las cinco propiedades (`live`,
`scripted_gifts`, `sponsor_tokens`, `budget_per_team`, `shop_opens_tick`), así
que las acepta todas; según la lectura de Ari del `sim.nim`, solo una se usa.

**El esquema es más ancho que el motor, y eso es lo que nos engañó.**

---

## 2 · Cada afirmación, contra lo que pasó

**Aviso primero:** **las 216 partidas del paper cinco usaron `lento_v0`. No hay
ni una sola partida del juego normal en la cantera para comparar.** La referencia
es el bloque de ejemplo del manifiesto congelado
`cantera/paper5/manifiesto_zero_sum_0_1_18.json`, que trae los valores por
defecto:

```
"zone_schedule": [[1440,1632,2064,24,19,1], "...(warn, shrink, done, r0, r1, dmg/s)"],
"tick_rate": 24, "max_ticks": 9120, "ignition_tick": 240,
"sponsor": {"enabled": true, "budget_per_team": 300, "shop_opens_tick": 1680,
            "catalog": {"sword": 120, "rations": 20, "...": 0}}
```

**`tick_rate = 24`**: todas las conversiones de abajo salen de ahí.

### (a) «Duración hasta unos trece minutos» — **CIERTO**

| | lento_v0 | defecto |
|---|---|---|
| `max_ticks` | **18240** | 9120 |
| a 24 tics/s | **12 min 40 s** | 6 min 20 s |

**Exactamente el doble.** «Unos trece minutos» es una redondeo generoso de 12:40,
pero la cifra es la correcta.

**Lo que duraron de verdad** (40 episodios de P5-8M, `final.match_ticks`):
**mediana 8.978 tics** (mín 2.369 · máx 14.641). **Ninguna llegó al tope**: todas
acabaron antes porque el anillo mata primero.

### (b) «Veinte segundos iniciales sin moverse ni atacar» — **CIERTO Y EXACTO**

| | lento_v0 | defecto |
|---|---|---|
| `freeze_ticks` | **480** | 240 |
| a 24 tics/s | **20 s** | 10 s |

**Medido en los diarios: el primer tic con movimiento es el 482 en los 19
asientos**, sin una sola excepción (mín 482, máx 482). Con el congelado
acabando en el 480, el cuerpo se mueve en cuanto puede.

*(Y el primer mensaje por el canal sale en el tic 481 — ver punto 3.)*

### (c) «Anillo que espera al 40 % y se cierra más despacio» — **CIERTO, LAS DOS COSAS**

| | lento_v0 | defecto |
|---|---|---|
| primer aviso | tic **7296** | tic 1440 |
| **como fracción de la partida** | **40,0 %** | **15,8 %** |
| aviso → encogimiento | **240 tics** (10 s) | 192 tics (8 s) |
| encogimiento → hecho | **540 tics** (22,5 s) | 432 tics (18 s) |
| **razón** | **1,25×** en los dos tramos | — |

**El 40 % es exacto: 7296 / 18240 = 40,0 %.** Y las siete filas del horario
mantienen los mismos 240 y 540 tics, así que **el anillo entero va a 1,25× de
lento**.

*(Radios y daño por segundo son los mismos que el defecto: 24→19 con 1 de daño
en el primer paso.)*

### (d) «Patrocinador al doble» — **CIERTO EN LA CLAVE, SIN EFECTO MEDIBLE**

**Lo que sí se ve en los diarios** (`P58M_t0_K_20260916`, asiento 10):

```
tic 2017: gift_incoming slot 0  rations    lands_tick 2136
tic 2041: gift_incoming slot 2  rations    lands_tick 2160
…ocho raciones, puestos pares, tics 2017 a 2185…
tic 4609: gift_incoming slot 1  first_aid  lands_tick 4728
…ocho botiquines, puestos impares, tics 4609 a 4777…
```

| | |
|---|---|
| **regalos por partida** | **16** (8 raciones + 8 botiquines) |
| primer regalo | **tic 2017** |
| último regalo | **tic 4777** |
| **lo que dice Ari del preset `Competition`** | **16 regalos, una ración y un botiquín por equipo, entre los tics 2016 y 4776** |

**Coinciden tic por tic.** Nuestros `scripted_gifts` pedían exactamente lo mismo
(equipo A tic 2016 raciones al puesto 0; equipo A tic 4608 botiquín al puesto 1;
equipo B 2040/4632…). **Así que no se puede distinguir si se honraron o se
ignoraron: piden lo que el preset ya daba.**

*(Por partida la mediana medida es 15-16 y hay algunas de 7 u 8: **eso es porque
el diario solo ve lo que nuestro asiento ve, y algunos murieron antes del segundo
reparto**. No es que faltaran regalos.)*

**Y el presupuesto, que es otra cosa:**

| | |
|---|---|
| menciones de `sponsor`, `shop` o `tienda` **en todo el diario** | **0** |
| el único `budget` del diario | `stats.budget = 20`, que es nuestro `stat_budget` |
| claves del `catalogo` que nuestra política escribe | **solo `items`, `stats`, `freeze`** |

**Nuestra política descarta el resto del `world_info`**: `policy_cortex.py:904`
construye el registro con `items`, `stats` y `freeze` y tira lo demás —
**incluido el bloque `sponsor`, que es donde viajaría el `budget_per_team`**.

**Y el cuerpo nunca compra:** el grep de `buy|shop|comprar|purchase` sobre
`policy_cortex.py`, `policy_forma.py` y `decisor_zs.py` **no devuelve nada**.

> **Conclusión del punto (d): la clave era la correcta y el valor era el doble,
> pero no hay forma de demostrar su efecto desde nuestros datos, y el mecanismo
> que gastaría ese presupuesto —la tienda— nuestro cuerpo no lo usa.**

### Y una frase del acta que hay que corregir

`ACTA.md:164` dice:

> «mandando el objeto `sponsor` **entero**, los dieciséis regalos sobreviven y el
> presupuesto sube a 600»

**La primera mitad está mal atribuida.** Los dieciséis regalos **no sobreviven
porque los mandáramos**: son los del preset `Competition` y habrían llegado
igual. Lo que sí subió a 600 es el presupuesto, por la clave correcta.

---

## 3 · El canal

| | |
|---|---|
| **canal** | **`team`** (`policy_forma.py:1254`, «Lo que sale por el canal `team`») |
| **límite del juego** | **1 mensaje cada 24 tics**, *«`talk` is separate and rate-limited to 1 per 24 ticks»* (manifiesto) |
| **lo declara nuestro código** | `policy_forma.py:1256`: «el canal deja 1 mensaje cada 24 tics, asi que NO se manda el parte de estado del cuatro y el de la forma a la vez» |
| **cada cuánto mandamos** | **cada 48 tics exactos** — la mitad del tope |

**Medido** (`P58M_t0_K_20260916`, asiento 10): 165 mensajes, el primero en el
**tic 481** (justo al salir del congelado), y **el intervalo es 48 en 164 de los
164 huecos** — mediana 48, mínimo 48, máximo 48.

### El plan del hermano

Con `GEMV_HILO_FORMA=1` **el mensaje del canal ES la forma**: el telegrama pasa
de ser el parte de estado del paper cuatro a ser el plan, codificado en ASCII
(`GF1|23.20.i.4312;-.-.u.4360;24.24.c.4470;-.-.e.4500|87,2.50,1`). **Con el
interruptor apagado sigue siendo el parte de siempre.** En el paper cinco, los
brazos K de la serie 8 lo llevan **apagado** (`GEMV_HILO_FORMA=0`), así que lo
que viajó fue el parte: `"E1 P10 t481 13,13 h100 v0 b0 a0"`.

### Los «tasa limitada»

| | |
|---|---|
| registros `voz` en todos los diarios del paper cinco | **66.198** |
| **`action_result = "rate_limited"`** | **2** |
| | **0,003 %** |

**Los dos, en brazos T de P5-6C**: uno en `P56C_tamp3_T_23193328` y otro en
`P56C_tamp4_T_23612244`.

**No rozamos el límite porque mandamos a la mitad del ritmo permitido.**

---

## 4 · La etiqueta

**El repositorio que Ari nombra no existe con ese nombre.**

```
$ git ls-remote https://github.com/arisklar6/battle-royale
remote: Repository not found.
fatal: repository 'https://github.com/arisklar6/battle-royale/' not found
```

Comprobado también con credenciales (`gh api repos/arisklar6/battle-royale` →
**HTTP 404**), así que **no es un problema de permisos: ese nombre no está**.

**El nombre exacto sale de nuestro propio manifiesto**, que lo cita dos veces:

> **`github.com/arisklar6/zero-sum`**

Y ahí la etiqueta sí está, **y apunta donde Ari dice**:

```
$ git ls-remote --tags https://github.com/arisklar6/zero-sum
fca9c260e691f0f97f7663a6cd1c07ff69f52e16   refs/tags/zero-sum-v0.1.18
9bd0ddf1e707db7cba86281dabf2492e96e47249   refs/tags/zero-sum-v0.1.18^{}
fa883de6f7eb01d016129490d788c673fa8fe5c7   refs/tags/zero-sum-v0.1.19
99d2ed597dca0a09f6c350e729d58b9559a8ebfc   refs/tags/zero-sum-v0.1.19^{}
```

| | |
|---|---|
| **nombre exacto del repositorio** | **`arisklar6/zero-sum`** |
| `zero-sum-v0.1.18` | etiqueta **anotada**, objeto `fca9c260e6…` |
| **el commit al que apunta** (`^{}`) | **`9bd0ddf1e707db7cba86281dabf2492e96e47249`** ✓ |
| **y ya existe** | **`zero-sum-v0.1.19`** → commit `99d2ed597dca0a09f6c350e729d58b9559a8ebfc` |

**El `9bd0ddf` de Ari es correcto**; lo que hay que corregir es el nombre del
repositorio. **Y conviene saber que el 0.1.19 ya está etiquetado.**

*(No se clonó nada: `git ls-remote` solo lee referencias.)*

---

## 5 · El saldo

**No existe ningún comando de solo lectura que muestre saldo ni límite de
Experience Requests. No lo invento.**

| dónde miré | qué hay |
|---|---|
| `coworld --help` | 47 comandos; **ninguno** con `balance`, `saldo`, `credit`, `quota`, `limit`, `budget` o `billing` |
| `coworld xp-request --help` | solo `create`, `list`, `get`, `episodes` — **listan peticiones, no saldo** |
| `softmax --help` | «authentication and account tools»: `login`, `logout`, `status`, `get-token`… **ninguno de saldo** |
| `softmax status` | solo identidad: `Authenticated`, correo, `subject_type`, `subject_id`, `owner_user_id` |
| `GET /whoami` | claves `is_softmax_admin`, `is_softmax_team_member`, `name`, `owner_user_id`, `resources`, `scopes`, `subject_id`, `subject_type`, `user_email`; `scopes: ['write']`; **ninguna clave de saldo, cuota o límite** |
| `GET /v2/account`, `/v2/billing`, `/v2/quota` | **HTTP 404 las tres** |

**Lo único que tenemos es lo que nosotros mismos sumamos:**
`cantera/paper5/estado_P56B.py`, que recorre nuestras peticiones y acumula
`cost_usd`. **Marca 138,061431 $ y la cola vacía.** *(Es solo `GET`, lo dice su
cabecera.)*

**Eso es gasto acumulado nuestro, no un saldo: nadie nos dice cuánto queda.**

---

## Resumen en cinco líneas

**¿Es verdad que el patrocinador tuvo el doble? En la clave, sí: mandamos
`sponsor.budget_per_team = 600` contra un defecto de 300, que es exactamente la
única clave que el motor honra. En el efecto, no lo puedo demostrar y sospecho
que no importó: nuestro cuerpo no tiene acción de compra, nuestra política tira
el bloque `sponsor` antes de escribir el diario, y no hay una sola mención de
tienda en 216 partidas.**

**Los 16 regalos que sí se ven no son el presupuesto: son los del preset
`Competition` (8 raciones en los tics 2017-2185, 8 botiquines en los 4609-4777),
y nuestros `scripted_gifts` pedían exactamente eso, así que da igual que se
ignoraran.**

**Mandamos además `sponsor.live = false`, y resulta que el motor llama a esa
clave `enabled`: si la hubiera entendido, habríamos apagado el patrocinador sin
enterarnos — nos salvó que la ignorara.**

**Los otros tres ajustes sí se aplicaron y se miden: la partida dura 18.240 tics
= 12 min 40 s (el doble del defecto), el cuerpo está quieto 480 tics = 20 s
exactos (el primer movimiento es el tic 482 en los 19 asientos), y el anillo
avisa en el tic 7.296 = el 40,0 % de la partida y se cierra a 1,25× de lento.**

**Y dos correcciones de intendencia: el repositorio no es `battle-royale` sino
`arisklar6/zero-sum` —ahí la etiqueta `zero-sum-v0.1.18` sí apunta al commit
`9bd0ddf`, y el 0.1.19 ya está etiquetado—, y no existe ningún comando de saldo:
lo único que sabemos es lo que sumamos nosotros, 138,06 $.**

---

**PARO AQUÍ.**

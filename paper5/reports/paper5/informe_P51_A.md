# P5-1 fase A — Mundo lento provisional: calma y precio (en seco)

Coste cero: ni una partida, ni una llamada al consejero, ni una petición creada.
Todo lo nuevo, en `cantera/paper5/`. Nada enviado, publicado ni borrado.

## Custodia al empezar

```
$ md5 -q motor/model.py paintball/alma/policy_cortex.py paintball/alma/cortex_t5.py \
        paintball/alma/appraisal_zs_v42_exp.py paintball/alma/decisor_zs.py
1e511978c251130e95169ebf8443efa1
6997b00c266f23d6037cc1a018f60a76
defb11d3a4661ff57745214ccd1ab14f
98c13d60167c80cc8334c965be75c640
8fa03547e3228ef9df4aa94c444f9252
```

El primero es `motor/model.py` y coincide con el de siempre. Los otros cuatro no
se han tocado en esta fase.

## De dónde sale todo

El manifiesto **desplegado hoy**, bajado de la plataforma con un GET:

```
$ GET /v2/coworlds/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6
  name            zero-sum
  version         0.1.18
  manifest_hash   sha256:c96e72bc55f3d8684cb51b019c9ee02a4047047631558d28c043f4db3b2263b9
  schema_hash     d777cbdd538ed03d584db4ddc115445d8281eebecffa5afd935c48021a898b60
  size_bytes      23006
  canonical       true
```

Guardado en `cantera/paper5/manifiesto_zero_sum_0_1_18.json` (868 líneas). Hay
además una copia bajada el 31-ago en
`~/paintball_recon/coworld/cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6/coworld_manifest.json`;
he comparado las dos clave a clave: **`game.config_schema`, `variants` y
`certification` son idénticos**, y solo difieren `game.runnable` y
`game.player_runtime`, que son el empaquetado, no la configuración. Las líneas
que cito abajo son las de esa copia, que es la que tiene líneas estables.

**Aviso, y no es menor.** El código Nim que hay en
`~/paintball_recon/docs/zero-sum/src/sim.nim` **no es el de la 0.1.18**: es una
compilación posterior (battle-royal) y sus nombres de campo no valen. Allí el
presupuesto del patrocinador se llama `budget_per_player` con 150 por defecto,
los regalos llevan `{tick, player, target}` y no existen ni `stat_budget` ni
`league_mode`. Los nombres buenos son los del `config_schema` del manifiesto.

---

## A1. Los cuatro campos, con su sitio

El `config_schema` lleva `"additionalProperties": false` (línea 215), así que la
lista de claves aceptadas es cerrada y es esta: `seed`, `zone`, `events`,
`tokens`, `players`, `sponsor`, `max_ticks`, `league_mode`, `stat_budget`,
`freeze_ticks`, `player_connect_timeout_seconds`. Nada más entra.

### 1. Duración máxima del episodio

| dato | valor |
|---|---|
| campo | **`max_ticks`**, de primer nivel |
| tipo y límites | entero, mínimo **100**, máximo **20000** |
| esquema | manifiesto, líneas **186-190** |
| hoy (variante `competition`) | **9120** — línea **583** |

No existe ningún `episode_length`, `game_length`, `num_ticks` ni `tick_limit`.

### 2. Congelación inicial antes del anillo

| dato | valor |
|---|---|
| campo | **`freeze_ticks`**, de primer nivel |
| tipo y límites | entero, mínimo **48**, máximo **480** |
| esquema | manifiesto, líneas **203-207** |
| hoy | **240** — línea **586**, que son los 10 s de cuenta atrás del paper cuatro |

Es exactamente la cuenta atrás: el encendido ocurre en el tic `freeze_ticks`, y
al jugador le llega como `player_config.ignition_tick` (capturado en
`paintball/alma/humo_200tics.json:11`, `"ignition_tick": 240`).

Hay un segundo campo de gracia que **no es de juego sino de reloj de pared** y
conviene no confundir: `player_connect_timeout_seconds` (líneas **208-213**,
entero de 0 a 600, 180 por defecto), que es lo que el juego espera a que se
conecten los dieciséis asientos antes del tic 0.

### 3. Calendario del anillo

| dato | valor |
|---|---|
| campo | **`zone.schedule`** — objeto `zone` (línea **26**) con una sola propiedad, `schedule` (línea **29**) |
| tipo | lista de listas de **exactamente seis enteros** |
| significado de cada fila, textual del esquema | `[warn_tick, shrink_tick, done_tick, r_start, r_end, damage_per_s]` |
| hoy | siete filas, líneas **357-416** |

Las siete filas de hoy:

```
[1440, 1632, 2064, 24, 19,  1]
[2352, 2544, 2976, 19, 15,  2]
[3264, 3456, 3888, 15, 11,  4]
[4176, 4368, 4800, 11,  8,  6]
[5088, 5280, 5712,  8,  5,  8]
[6000, 6192, 6624,  5,  3, 16]
[6912, 7104, 7536,  3,  0, 24]
```

**No hay ningún campo suelto** para «cuándo empieza» ni «a qué ritmo»: no existe
`shrink_start_tick`, ni `shrink_interval`, ni `shrink_rate`, ni nada con `ring_`
o `circle_`. En la configuración la cosa se llama **zone**, nunca anillo. Para
mover el anillo hay que **sustituir la lista entera**.

En la misma familia está `events` (línea **44**), la lista de inundaciones e
incendios; hoy `competition` trae una inundación (líneas 417-429).

### 4. Presupuestos del patrocinador

| concepto | campo | límites | esquema | hoy |
|---|---|---|---|---|
| botín del patrocinador | **`sponsor.budget_per_team`** | entero, 0 a **10000** | líneas **174-178** | **300** (línea 580) |
| estadísticas | **`stat_budget`**, de primer nivel, **no** dentro de `sponsor` | entero, 4 a **40** | líneas **198-202** | **20** (línea 585) |
| cuándo abre la tienda | `sponsor.shop_opens_tick` | entero, ≥ 0 | líneas **179-183** | **1680** (línea 581) |
| regalos guionizados | `sponsor.scripted_gifts` | lista de `{tick, team, recipient_slot, item_id}` | líneas 482-579 | **16 regalos** |

**Un negativo que hay que decir.** *Botín* tiene dos sentidos y solo uno es
configurable. El presupuesto del **patrocinador** sí lo es, y es
`budget_per_team`. El **botín del mapa** —la Fortaleza, las cajas, los
matorrales— **no tiene ningún campo**: se genera con el mapa y no hay palanca.
He buscado `budget` en todo el manifiesto y solo salen esos dos. No existen
`loot_budget`, `bounty_budget`, `sponsor_budget` ni `budget_per_player`.

### Que los cuatro se pueden sobrescribir, comprobado

No es suposición: el propio manifiesto trae una configuración de certificación
(líneas **719-815**) que ya los cambia, con `max_ticks` **480** (línea 812),
`freeze_ticks` **48** (línea 815), `shop_opens_tick` **96** (línea 810) y un
`zone.schedule` de tres filas (líneas 722-741). Y hay una corrida local con esos
mismos valores en `~/paintball_recon/runs/zerosum/config.json`.

**Precedente propio: ninguno.** En S-2 y S-3 nuestras peticiones solo
sobrescribieron `seed` (`cantera/paper4/lanza_S2.py:29`, `lanza_S3.py:49`).
Lento_v0 sería la primera vez que tocamos los demás.

---

## A2. `lento_v0`

Está en `cantera/paper5/lento_v0.json`, generado por
`cantera/paper5/hace_lento_v0.py`, que lo deriva de la variante `competition`
para no inventar nada. **Valida contra el `config_schema` del manifiesto**
(`jsonschema.validate`: pasa).

| campo | hoy | lento_v0 | límite | por qué |
|---|---|---|---|---|
| `max_ticks` | 9120 | **18240** | 100–20000 | el doble exacto, que cabe: el tope es 20000 |
| `freeze_ticks` | 240 | **480** | 48–480 | lo más largo que el campo permite, que es el doble de hoy |
| `zone.schedule` | 7 filas desde 1440 | **7 filas desde 7296** | — | ver abajo |
| `sponsor.budget_per_team` | 300 | **600** | 0–10000 | el doble, para que el botín por tic no baje al doblarse la partida; el encargo pedía «no por debajo del actual» y esto lo cumple con holgura |
| `stat_budget` | 20 | **20** | 4–40 | sin tocar: nada pedía cambiarlo y cambiarlo rompería la comparación con S-2 y S-3 |
| `sponsor.shop_opens_tick` | 1680 | **1680** | ≥ 0 | sin tocar: dejarlo donde está abre la tienda antes en términos relativos, que nunca es menos botín |
| `sponsor.scripted_gifts` | 16 | **los mismos 16** | — | copiados tal cual |

### El anillo

Las siete filas de hoy, **corridas** para que la primera avise en el 40 % de la
partida y **estiradas por 1,25** para que además el anillo sea más lento. Los
radios y el daño por segundo no se tocan: es el mismo anillo, más tarde y más
despacio.

| hoy | lento_v0 |
|---|---|
| `[1440, 1632, 2064, 24, 19, 1]` | `[7296, 7536, 8076, 24, 19, 1]` |
| `[2352, 2544, 2976, 19, 15, 2]` | `[8436, 8676, 9216, 19, 15, 2]` |
| `[3264, 3456, 3888, 15, 11, 4]` | `[9576, 9816, 10356, 15, 11, 4]` |
| `[4176, 4368, 4800, 11, 8, 6]` | `[10716, 10956, 11496, 11, 8, 6]` |
| `[5088, 5280, 5712, 8, 5, 8]` | `[11856, 12096, 12636, 8, 5, 8]` |
| `[6000, 6192, 6624, 5, 3, 16]` | `[12996, 13236, 13776, 5, 3, 16]` |
| `[6912, 7104, 7536, 3, 0, 24]` | `[14136, 14376, 14916, 3, 0, 24]` |

| comprobación | hoy | lento_v0 |
|---|---|---|
| primer aviso del anillo | 1440 = **15,8 %** | 7296 = **40,0 %** exacto |
| empieza a encoger | 1632 = 17,9 % | 7536 = **41,3 %** |
| último «hecho» | 7536 = 82,6 % | 14916 = **81,8 %** |
| cola con el anillo cerrado del todo | 1584 tics = 17,4 % | 3324 tics = **18,2 %** |
| lo que dura el anillo | 6096 tics | **7620** tics |
| **juego vivo antes del anillo** | **1200 tics** | **6816 tics** |

Esa última fila es la que importa para la calma: pasamos de 1.200 instantes de
juego sin anillo a **6.816**, casi seis veces más. Y la cola de muerte segura se
queda en la misma proporción que hoy, para no cambiar el final del juego.

### Una duda declarada, y cómo la cubro

**No sé si el servidor fusiona o sustituye un objeto anidado.** Si mando
`{"sponsor": {"budget_per_team": 600}}` y el servidor sustituye, perdería los
dieciséis regalos guionizados y el `live: false`. Por eso el JSON manda el
**objeto `sponsor` entero**, con sus cuatro claves, copiadas de `competition`
salvo el presupuesto. Con `zone` no hay duda: queremos sustituir la lista.

`players` y `tokens` **no se mandan**: los pone la plataforma, y `tokens` es la
única clave obligatoria del esquema precisamente porque es suya.

### Las tres semillas

Las tres primeras de `cantera/paper4/semillas_S2.json`, que ya jugaron S-2 y
S-3, así que el mapa es comparable con lo medido en el paper cuatro:

```
20260916   20365645   20470374
```

**Una por petición.** El servicio alojado repite la semilla dentro de una tanda,
así que tres partidas distintas son tres peticiones de un episodio, no una de
tres. Sirven luego para cualquier brazo.

---

## A3. Roster, política e imagen

### Los catorce rivales, leídos de `participants`

Del episodio `ereq_9cf61642-a6c4-4163-a32c-bdc4da40e07e`, de la petición
`xreq_d40bf6f4-a67f-4b3d-affa-47d485a5526b` (S-3, brazo D0, semilla 20260916).
Son **diez políticas distintas**; cuatro de ellas ocupan dos asientos:

| policy_version_id | nombre | asientos en ese episodio |
|---|---|---|
| `6244cdeb-e044-42ff-91e3-a5c716c4338d` | zero-sum-scavenger | 0 y 12 |
| `47f38a1c-9143-4b56-9316-ceabe7c82c6d` | relh-zero-sum | 1 y 13 |
| `41f43efa-bbd5-477a-8ed1-1443f2731eb1` | sivanlevy-zs-courier | 2 y 14 |
| `458ec0b6-fc59-4bda-aff0-68daa7f21b79` | belobog | 3 y 15 |
| `54ec6fab-6773-46db-bb55-119688182786` | ryanschiller-zero-sum-player-v1 | 4 |
| `2b9cfd17-db50-4990-8f99-6c7c13453f61` | zs-patient | 5 |
| `9457da2a-832d-45e5-b918-9209e86f9948` | aaron-zs-fable | 6 |
| `dfc40843-b709-4332-85a6-c5bbb653375b` | zero-sum-example | 7 |
| `3e8097e1-85b8-4731-b7c1-e674f2ccbd10` | skourehjan-zero-sum-scripted-v1 | 8 |
| `09da1dbc-ac3b-4bb1-9114-4ee615496755` | Zero Sum Baseline | 9 |

**Nuestros dos asientos son el 10 y el 11, con `slot` explícito.** Los catorce
rivales van con `slot: -1`, que es como rotan. Aviso ya sabido del paper cuatro:
la semilla fija el mapa, no quién se sienta dónde; el segundo episodio de esa
misma petición colocó a los mismos diez en otro orden.

### La política

El cuerpo solo, **brazo A**: `GEMV_CORTEX=0`, sin consejero.

El interruptor no va en la petición: se fija **al subir la política**, con
`--secret-env KEY=VALUE`. Y la imagen ya trae `GEMV_CORTEX=0` **por defecto**
(`paintball/alma/Dockerfile.cortex`, bloque `ENV`), así que el brazo A es la
imagen tal cual, **subida sin un solo `--secret-env`**.

### La imagen

La de S-3 **sigue disponible en local**, con el sha del encargo:

```
$ docker image inspect gemv-anima:s3 --format '{{.Id}}'
sha256:495c04a784d396d0d53d4841d354fb54c4efae6a4ce54705893108faec0cd72e
```

Es la que jugó de verdad la prueba del reloj (`informe_S3.md` §13: la del acta
§0, `ae63f2a5…`, fue el primer intento y se reconstruyó al arreglar la cola de
la demora). Los ficheros que van dentro siguen con los md5 de entonces:
`policy_cortex.py` en `6997b00c266f23d6037cc1a018f60a76` y `cortex_t5.py` en
`defb11d3a4661ff57745214ccd1ab14f`.

**No hace falta reconstruir.** Lo único pendiente sería **subirla como política
nueva** para este brazo, que es gratis pero es una acción en la plataforma; la
dejo para la fase B, con el id escrito en el acta antes de la primera partida,
como manda el encargo.

### Corrección al encargo: el `spend_limit`

**No se puede fijar, ni explícito ni nulo.** Ya lo cerró el `informe_S2.md`
§Corrección: el servidor rechaza `spend_limit_usd` y
`player_pod_llm_spend_limit_usd` en el cuerpo como `extra_forbidden`. Lo he
vuelto a comprobar contra el esquema del POST que sirve la propia API
(`V2CreateExperienceRequestRequest`): sus claves son `idempotency_key`,
`private`, `llm_routing_override`, `coworld_id`, `variant_id`, `target`,
`game_config_overrides`, `game_config_overlay_secret`, `state`, `roster`,
`included_players`, `excluded_players`, `num_episodes`, `notes`,
`execution_backend` y `reporters`. **No hay ninguna de gasto.**

El límite es **de liga**: lo aplica el sidecar y llega a la política como la
cabecera `X-Coworld-Spend-Limit-Usd` (`cortex_t5.py:959` la lee). Sale además en
el `cost_preview` como `player_pod_llm_spend_limit_usd`, que es un dato que el
servidor devuelve, no uno que nosotros pongamos.

En esta serie, además, **no hay consejero**, así que no hay llamadas al modelo
ni gasto que limitar. Los dos frenos de la política —tiempo de espera y fallos
seguidos— siguen dentro del córtex, tal como están, y con el consejero apagado
no llegan a actuar.

---

## A4. El `cost_preview`, y de dónde viene de verdad el precio

### No se puede pedir en seco, y esto es un hecho del esquema

El campo existe, pero el propio esquema de la API dice cuándo aparece:

```
V2ExperienceRequestDetail.cost_preview
  "Admission-time cost estimate, present only in the create response."
```

O sea: **solo se obtiene creando la petición**, que es justo lo que cuesta
dinero. Lo he comprobado por tres vías, todas negativas:

- el POST `/v2/experience-requests` **no tiene parámetro `dry_run`** ni
  equivalente; el único `dry_run` de toda la API (243 rutas) está en tres
  operaciones de campaña de ligas, nada que ver;
- el GET de una petición ya creada devuelve `cost_preview: null` (comprobado en
  `xreq_d40bf6f4-…`: el campo viene a nulo);
- no hay ninguna ruta de estimación.

**Conclusión honesta: A4 tal como está escrito no se puede hacer sin gastar.**
Pedir el `cost_preview` de `lento_v0` *es* lanzar la petición de la fase B. No lo
he hecho.

### Lo que sí se puede saber, y sale mejor de lo que pedía el encargo

He leído de la plataforma el coste real de **los 257 episodios** de S-2 y S-3
(`cantera/paper5/costes_A.py`, solo GET; datos en `costes_episodios.json`).

```
serie/brazo         n   mediana     media       min       max      suma
S-2/A              40    0.0574    0.0530    0.0191    0.0644     2.119
S-2/Aconf          10    0.0410    0.0430    0.0212    0.0568     0.430
S-2/B              40    0.0568    0.0537    0.0156    0.0662     2.146
S-2/C              40    0.0554    0.0496    0.0170    0.0619     1.983
S-2/P5              1    0.0399    0.0399    0.0399    0.0399     0.040
S-2/P6              2    0.0326    0.0326    0.0281    0.0372     0.065
S-2/humo            1    0.0386    0.0386    0.0386    0.0386     0.039
S-3/D0             30    0.7037    0.7730    0.2785    1.9424    23.190
S-3/D100           26    0.9174    0.9674    0.3574    2.0745    25.154
S-3/D300            1    0.0884    0.0884    0.0884    0.0884     0.088
S-3/D300_humo2      1    0.6643    0.6643    0.6643    0.6643     0.664
S-3/T              31    0.7186    0.7716    0.0491    2.0093    23.918
TOTAL             223                                            79.837
```

(223 de los 257 llegaron a `completed` con coste; el resto fallaron o se
cancelaron y no cobraron.) S-2 mediana **0,0556 $**; S-3 mediana **0,7424 $**.
El salto de 13× del encargo queda confirmado.

### Qué cambió entre S-2 y S-3: no fue el juego

**La configuración efectiva fue idéntica en los 257 episodios.** Lo he
comprobado leyendo el `game_config` con que corrió cada uno:

```
configuraciones efectivas distintas:
   257 episodios: max_ticks 9120 · freeze_ticks 240 · stat_budget 20 ·
                  zone[0] [1440, 1632, 2064, 24, 19, 1] ·
                  sponsor.budget_per_team 300 · shop_opens_tick 1680
```

Una sola. Y el roster fue el mismo. Y la partida duró lo mismo:

```
serie     n  coste med  reloj med (s)    $/min
S-2     134     0.0556          302.6   0.0110
S-3      89     0.7424          305.6   0.1458
```

**Corrieron 303 y 306 segundos: prácticamente lo mismo.** Lo que cambió fue la
**espera en cola**:

```
S-2: n=134 coste=0.0556 espera=   32.6s corre=302.6s total=  334.9s  $/min(total)=0.00997
S-3: n= 89 coste=0.7424 espera= 5453.8s corre=305.6s total= 5779.6s  $/min(total)=0.00771

correlacion con el coste, 223 episodios:
  espera  r = +0.9004
  corre   r = +0.1833
  total   r = +0.9007
```

**La tarifa es el tiempo de vida del pod, desde que se despacha hasta que
acaba, cola incluida**, a un precio muy estable:

```
S-2: $/min de vida del pod  n=134  mediana=0.00998  p10=0.00979  p90=0.01006
S-3: $/min de vida del pod  n= 89  mediana=0.01018  p10=0.00359  p90=0.01019
```

Un céntimo por minuto de pod, o sea **0,60 $ la hora**. S-2 esperó 33 segundos y
pagó 0,056 $; S-3 esperó **91 minutos** y pagó 0,742 $. La misma partida.

La prueba más limpia está en tres episodios de la misma noche, el 17-sep a las
21Z, antes de lanzar la serie entera:

```
  D300           coste=0.0884 espera=  495.9s corre=323.6s
  T              coste=0.0491 espera=  537.3s corre=232.8s
  D300_humo2     coste=0.6643 espera= 3690.7s corre=224.4s
```

Misma serie, misma configuración, mismo día: el que esperó una hora costó trece
veces más que el que esperó nueve minutos.

**Por qué esperó S-3.** Se lanzaron 80 peticiones de golpe, 160 episodios, y los
pods se quedaron en cola unos detrás de otros. S-2 se lanzó en una hora con el
clúster libre.

### Lo que esto significa para `lento_v0`, dicho antes de jugar

Doblar la partida añade, como mucho, otros ~300 segundos de corrida, que a esta
tarifa son **unos 5 céntimos**. Un episodio suelto, con el clúster libre, debería
costar del orden de **0,10 $**. Si la cola está cargada, puede costar cualquier
cosa: la cola, no el juego, es lo que manda.

**Esto toca la predicción sellada P1**, que dice que el precio subirá por encima
de 0,742 «porque la partida es más larga». La medida de arriba dice que la
duración de la partida **no es lo que fija el precio**. No cambio la predicción:
queda sellada como está y se cotejará en la fase C con la cifra real. Pero lo
digo antes de jugar, no después.

---

## A5. Saldo de créditos

**No hay forma de consultarlo con esta cuenta, y no me lo invento.**

```
$ GET /v2/coworlds/zero-sum/budget  -> 403
{"detail": "Viewing the budget requires Softmax team membership or ownership of
 Coworld 'zero-sum'", "type": "forbidden"}

$ GET /whoami -> 200
{"user_email": "[tapado]", "name": "Manel Enrico",
 "is_softmax_team_member": false, "is_softmax_admin": false,
 "scopes": ["write"], ...}
```

Probadas además `/v2/billing`, `/v2/credits`, `/v2/account`, `/v2/me`,
`/v2/users/me` y `/v2/wallet`: **404 las seis**. En las 243 rutas del OpenAPI no
existe ninguna de saldo personal: «credits» solo aparece en premios de liga, en
el `estimated_cost_credits` del preview y en el medidor de gasto de un Coworld,
que es el 403 de arriba.

Lo único auditable es **lo que hemos gastado**, sumado episodio a episodio de la
propia plataforma:

| serie | episodios cobrados | gasto |
|---|---|---|
| S-2 | 134 | **6,823 $** |
| S-3 | 89 | **73,015 $** |
| **total** | **223** | **79,837 $** |

---

## Lo que hay sobre la mesa para decidir

1. **Jugar o no la fase B.** Un episodio, semilla 20260916, `lento_v0`, roster de
   A3. El precio esperado es del orden de 0,10 $ si la cola está libre, pero la
   cola no la controlo.
2. **Subir la política del brazo A**, que es gratis: la imagen `gemv-anima:s3`
   tal cual, sin `--secret-env`. Haría falta antes de la primera partida y el id
   iría al acta.
3. **A4 queda sin cumplir tal como estaba escrito**, porque el `cost_preview`
   solo existe al crear la petición. La alternativa medida está arriba.
4. **El preset de Ari sigue sin llegar.** `lento_v0` es provisional y está hecho
   para poder repetirse con el suyo sin tocar nada más que el JSON.

**PARA AQUÍ.**

## Custodia al acabar

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1

$ md5 cantera/paper5/*.py cantera/paper5/lento_v0.json \
      cantera/paper5/manifiesto_zero_sum_0_1_18.json
MD5 (cantera/paper5/costes_A.py)                      = aed97cdefe25b748fc13f92dafb45f2a
MD5 (cantera/paper5/hace_lento_v0.py)                 = f2b0c34c60b2d4a632f2d677e72a81f5
MD5 (cantera/paper5/sonda_A.py)                       = b093d43f72a6af0e5296e4493076b542
MD5 (cantera/paper5/lento_v0.json)                    = d213ba5d90a64875ce77f02390f46cf2
MD5 (cantera/paper5/manifiesto_zero_sum_0_1_18.json)  = 07ffcf2e63975ffe0a0d0cecc4198c69
```

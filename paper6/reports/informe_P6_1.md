*Copia para el taller compartido: en esta copia los correos están tapados («[correo de Manel]», «[correo de Ari]», «[correo de la plataforma]»). El original, en el taller privado de Manel.*

# P6-1 · Guardar el cinco, comprobar la liga, calibrar el mundo del seis

*`motor/model.py` intacto (md5 `1e511978c251130e95169ebf8443efa1`, comprobado
al empezar y al acabar). **Nada empujado, subido, publicado ni borrado**: el
commit y la etiqueta son locales, `git status` dice `ahead 1` y ahí se queda.
Nada en nombre de Manel: el commit lleva la coautoría declarada.*

---

# A · GUARDAR EL CINCO

## A.1 · Seguridad primero

### El `.gitignore`

Las reglas de `.env` ya estaban (se pusieron en P5-5B): `.env`, `**/.env`,
`*.env`. **Comprobado que funcionan**: `git check-ignore -v cantera/paper5/.env`
responde `.gitignore:59:*.env`. Añadí las que faltaban:

```
.env.*          **/.env.*       *.key        *.pem
*.p12           *.pfx           id_rsa*      .netrc
*credentials*.json
```

### El rastreo

Dos pasadas. La primera, ancha, sobre los **1.356 archivos** candidatos; la
segunda, ya cerrada, sobre los **1.407 que iban a entrar de verdad**.

| patrón | coincidencias |
|---|---|
| `sk-ant-…` | **0** |
| `sk-` genérica (20+ caracteres) | **0** |
| `Bearer <algo>` | **0** |
| `AKIA…` (AWS) | **0** |
| `ghp_/gho_/ghs_/ghu_` (GitHub) | **0** |
| `BEGIN … PRIVATE KEY` | **0** |
| `ANTHROPIC_API_KEY=` / `CLAVE_BANCO_T3=` / `api_key=` con valor | **0** |

Las 23 coincidencias de `api_key`, las 10 de `token` y las 69 de `secret` que
salieron en la pasada ancha **son todas nombres de variable o prosa**, y las
revisé una a una:

* `anthropic.Anthropic(api_key=os.environ["CLAVE_BANCO_T3"])` — el nombre de la
  variable, no su valor;
* `if linea.strip().startswith("ANTHROPIC_API_KEY="):` en
  `consejero_forma.py:53` — el lector del `.env`, que es justo lo que queremos
  que esté en el repo;
* `os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "bedrock-sidecar")` —
  marcador para el sidecar local, no una credencial;
* `"tokens"` y `"sponsor_tokens"` en el manifiesto del coworld — **son campos
  del juego** (la moneda del patrocinador), no credenciales;
* el resto, menciones en informes y actas del tipo «no aparece ninguna clave».

Además hice un barrido de entropía: toda cadena de 30+ caracteres que no fuera
un UUID, un md5 ni un identificador conocido del proyecto. Las 1.000 y pico que
salieron son nombres de política, nombres de campo, rutas de archivo e internos
de PDF. **Ninguna credencial.**

### Dos correos, que no son claves pero conviene decir

| correo | veces | dónde |
|---|---|---|
| `[correo de Manel]` | 236 | el `requester` de cada respuesta de la plataforma |
| **`[correo de Ari]`** | **2** | `"owner"` del coworld, en `manifiesto_zero_sum_0_1_18.json` y en la sonda |

El segundo es **de un tercero**, y viene dentro de una respuesta de la API. No
bloquea el guardado local —nada se ha publicado—, pero **hay que quitarlo antes
de Zenodo**. Lo dejo escrito aquí para que no se cuele.

## A.2 · Qué entra y qué no

**Entra:** `cantera/` (los dos papeles: código, informes, `.txt`, JSON
pequeños, figuras) y las piezas del alma que jugaron. **1.434 archivos, 69 MiB.**
La regla `*.png` dejaba fuera las figuras, que son el resultado del paper: se
revierte con `!cantera/**/*.png` (49 PNG, 7,8 MiB).

**No entra:**

| qué | cuánto | dónde queda su inventario |
|---|---|---|
| los diarios crudos (`.art.log` y `.zip`) | **1.766 archivos, 12,01 GiB** | `cantera/paper5/DIARIOS_MANIFIESTO.md`, con ruta, bytes y md5 de cada uno |
| los JSON de más de 5 MB | **5 archivos, 37,9 MiB** | el mismo manifiesto, sección aparte |
| los `.log` de corrida, los `__pycache__`, el `.env` | — | ya estaban ignorados |

Los cinco gordos, por si hace falta buscarlos: `P57A_s2.json` (10,0 MB),
`D_series.json` (9,7), `P58A_lento.json` (7,7), `chat_S2.json` (6,7),
`_pegar_al_hermano.json` (5,6).

*(Nota: los diarios **nunca** estuvieron en git; la regla `*.log` ya los
excluía. Lo que sí había bajo `paintball/runs/` eran 2.700 `.json` y `.txt` de
los papeles tres y cuatro, 14 MiB, que siguen donde estaban. No borro nada.)*

## A.3 · Los md5 contra `CONGELADO.md`

```
coinciden: 199   no coinciden: 0   no existen: 0
```

Y las tres custodias que `Dockerfile.forma` comprobaba en cada build siguen
cuadrando: `model.py` `1e511978…`, `decisor_zs.py` `8fa03547…`,
`appraisal_zs_v42_exp.py` `98c13d60…`.

## A.4 · Guardado local

```
commit  86a006a6bcf4f03263c860fda693bcaaf9b335e4   «paper cinco, final»
autor   Manel Enrico <[correo de Manel]>   (con Co-Authored-By declarado)
fecha   2026-09-26 19:38:30 +0200
etiqueta local  paper5-final  ->  86a006a
estado  ## paintball...origin/paintball [ahead 1]     ← NO empujado
```

1.434 archivos. La etiqueta es local y no se ha empujado.

---

# B · LA LIGA

Consulta de sólo lectura, **coste cero**: `GET /v2/leagues/{id}`,
`GET /v2/league-policy-memberships?league_id=…`, `GET /v2/games` y
`GET /v2/coworlds/{id}`. Las respuestas quedan en `cantera/paper6/liga/`.

## El mundo sí se movió: la liga juega ya en 0.1.19

| | el de nuestras series | el de la liga hoy |
|---|---|---|
| coworld | `cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6` | **`cow_6a55df20-08d1-4e4c-adba-33dbd97e1e6f`** |
| versión | **0.1.18** | **0.1.19** |
| imagen del motor | `cogames@sha256:953424bb…` | **`cogames@sha256:5403c453…`** |
| `manifest_hash` | `sha256:c96e72bc…` | `sha256:9e210399…` |

Diferencia del manifiesto, ruta a ruta: **12 valores cambian y 107 rutas son
nuevas**, y todas menos tres están en la **variante 1**, que ha dejado de ser
`casual-live` (patrocinador en vivo) y ahora es **`duos`** (ocho políticas,
equipos adyacentes). Las tres restantes: la versión, la imagen del motor y el
bundle del visor de repeticiones. Hay además un campo nuevo, `game_version`, en
el esquema de resultados.

**La variante que usamos, `competition`, no tiene ni un cambio de
configuración.** Así que el mundo del seis es el mismo salvo por el binario del
motor, y **el manifiesto no dice qué cambió dentro de ese binario**. Por eso el
grupo 1 de la calibración existe.

## Las cinco políticas de `roster_lento_v2`: todas siguen, todas iguales

42 membresías en la liga. Las cinco están con **el mismo `policy_version_id`
que jugó nuestras 205 partidas**, todas `competing/active` y campeonas de su
autor:

| política | versión | `policy_version_id` | estado hoy | ¿la misma? |
|---|---:|---|---|---|
| **belobog** | 2 | `458ec0b6-fc59-4bda-aff0-68daa7f21b79` | competing / active / champion | **sí** |
| **zero-sum-scavenger** | 12 | `6244cdeb-e044-42ff-91e3-a5c716c4338d` | competing / active / champion | **sí** |
| **aaron-zs-fable** | 2 | `9457da2a-832d-45e5-b918-9209e86f9948` | competing / active / champion | **sí** |
| **zs-patient** | 3 | `2b9cfd17-db50-4990-8f99-6c7c13453f61` | competing / active / champion | **sí** |
| **skourehjan-…-scripted-v1** | 1 | `3e8097e1-85b8-4731-b7c1-e674f2ccbd10` | competing / active / champion | **sí** |

Y las dos que `v2` deja fuera pero `v1` necesita:

| política | versión que usamos | estado hoy | aviso |
|---|---:|---|---|
| **sivanlevy-zs-courier** | 3 `41f43efa…` | competing / active / champion | sin cambios |
| **relh-zero-sum** | 52 `47f38a1c…` | **competing / *benched*** | **hay una v53 desde el 18-sep** (`91727661…`), que es la campeona |

**¿Es un problema que la v52 esté «benched»?** No, y lo comprobé antes de
lanzar en vez de suponerlo: **las 216 peticiones del paper cinco se crearon
entre el 19 y el 22 de septiembre, es decir después de que apareciera la v53, y
las 216 usaron la v52** porque la fijamos por `policy_version_id`. Una versión
apartada del banquillo sigue siendo rosterizable por identificador. El grupo 1
puede reproducir `roster_lento_v1` tal cual.

*(Lo que sí hay que anotar: si algún día el roster se pide por nombre en vez de
por id, `relh-zero-sum` traerá la v53 y el mundo cambiará sin avisar.)*

## Lo que además ha cambiado en la liga desde el cinco

Tres políticas nuevas que no estaban en ninguna de nuestras series:
**`zs-rationer`** (ocho versiones desde el 8-sep), **`daf-cogame-carrier`** y
**`daf-zerosum-v1`**. No entran en la calibración —fijamos el roster— pero **no
tenemos ni un dato sobre ellas**, y si algún día jugamos contra la liga abierta
aparecerán.

**Conclusión de B: sigo a C.** Las cinco están, son las mismas, y el único
cambio relevante —la versión del motor— es justo lo que el grupo 1 mide.

---

# C · CALIBRACIÓN

20 episodios, 40 diarios, **1,8333 USD** de los 3 del tope. Todos en **0.1.19**.
Cuerpo del cinco solo (`gemv-p57c-A:v1`, el brazo A de P5-7C), asientos 10 y 11,
las mismas diez semillas en los dos grupos.

**El sello se escribió y se cerró antes de lanzar el primer episodio:**
`cantera/paper6/SELLO_P6_1.md`, md5 **`3ba5802c77bc3325195606175befac1d`**.
No se ha tocado desde entonces.

## Las tres columnas

| medida | **0.1.18** (P5-7C, ya jugado) | **Grupo 1** · v1 en 0.1.19 | **Grupo 2** · v2 en 0.1.19 |
|---|---:|---:|---:|
| vidas | 20 | 20 | 20 |
| **vida media** (tics) | 9.301,2 | **8.024,1** | **13.288,7** |
| vida mediana | 10.427 | 8.555 | 14.041 |
| **muertes por vida de políticas** | **0,45** (9) | **0,75** (15) | **0,20** (4) |
| muertes del anillo | 7 | 2 | **14** |
| «no consta» | 3 | 2 | 0 |
| victorias | 1 | 0 | 1 |
| tiempo seguro medio (tics) | 4.097,1 | 3.269,9 | 4.312,9 |
| **fracción segura de la vida** | **50,08 %** | **44,12 %** | **33,88 %** |
| **puesto mediano** | 11,5 | 13,5 | **4,5** |
| puesto medio | 9,7 | 12,4 | 5,3 |

Contrastes (Fisher bilateral para las muertes, Mann-Whitney para lo continuo):

| comparación | muertes | vida | puesto | fracción segura |
|---|---|---|---|---|
| 0.1.18 → Grupo 1 | p = **0,105** | p = 0,199 | p = 0,083 | p = 0,508 |
| **Grupo 1 → Grupo 2** | p = **0,0012** | p < **0,0001** | p < **0,0001** | p = 0,304 |
| 0.1.18 → Grupo 2 | p = 0,176 | p = **0,0001** | — | p = 0,083 |

Y emparejando por semilla y asiento, que es lo más fuerte que permiten veinte
vidas: **la vida del grupo 2 supera a la del grupo 1 en 18 de los 20 pares**,
con una mediana de **+5.004 tics**. Prueba de los signos **p = 0,0004**.

---

## Las cuatro predicciones, una a una

### PREDICCIÓN 1 · «Grupo 1 contra 0.1.18: sin diferencia» — **FALLA en una de cuatro**

| medida | banda que escribí | salió | |
|---|---|---:|---|
| vida media | 7.441 – 11.161 | 8.024,1 | **acierto** |
| **muertes por vida de políticas** | **0,25 – 0,65** | **0,75** | **FALLO** |
| fracción segura | 43 % – 57 % | 44,12 % | acierto (al borde) |
| puesto mediano | 9 – 14 | 13,5 | acierto (al borde) |

**Pero no puedo cobrarme el fallo como hallazgo.** 9 de 20 contra 15 de 20 da
**p = 0,105**: con veinte vidas eso no distingue un motor más duro del azar. Es
exactamente el caso «en medio» que dejé escrito en el sello, y hago lo que dije
que haría: **lo cuento y pido más semillas, no lo vendo**.

Lo que sí se puede decir sin estadística es **de qué forma se movió**, porque
las tres medidas apuntan al mismo sitio:

| | 0.1.18 | Grupo 1 |
|---|---:|---:|
| muertes de `relh-zero-sum` | 3 | **8** |
| muertes del anillo | 7 | **2** |
| golpes de `relh` | 47 | **73** |

**El cuerpo muere antes, y por eso el anillo ya no llega a cobrárselo.** Las
ocho muertes de `relh` en el grupo 1 caen entre los tics 8.248 y 10.949; en
0.1.18 sus tres caen entre 8.708 y 12.162. Es el mismo rival, a la misma hora,
pero rematando más.

*(Y hay un detalle que no estaba en 0.1.18: una muerte por `flood` en el tic
4.729. La inundación existe en las dos versiones —está en la configuración de
la variante, idéntica—, pero es la primera vez que nos mata.)*

### PREDICCIÓN 2 · «Grupo 2: 0,169 muertes por vida» — **ACIERTO**

| | cifra |
|---|---:|
| lo que predije en P6-0 y repetí en el sello | **0,169** |
| la reescalada a esta submuestra, que también dejé escrita | 0,104 |
| a lo que aposté | ≤ 0,25 |
| **lo que salió** | **0,20** (4 muertes en 20 vidas) |

0,169 × 20 = 3,4 muertes esperadas; salieron **4**. La cifra del encargo
—la del corpus entero— fue **la buena de las dos**; mi reescalado a la
submuestra habría predicho 2,1 y se habría quedado corto.

Y aquí sí hay potencia: **15 de 20 contra 4 de 20, p = 0,0012**.
`roster_lento_v2` reduce las muertes por políticas de forma que no se explica
por azar.

### PREDICCIÓN 3 · «Grupo 2 tiene más tiempo seguro» — **FALLA, y al revés**

| | predicho | salió |
|---|---|---:|
| fracción segura, grupo 2 | **≥ 55 %** | **33,88 %** |
| tics seguros de media | ≥ 4.700 | 4.312,9 |
| signo (grupo 2 > grupo 1 en fracción) | sí | **NO** (33,88 contra 44,12) |

**Falla en las tres lecturas.** Y el mecanismo es mío, no del mundo: **la
`amenaza` que uso lleva un término de anillo** (`curiosidad.py:271-278`), así
que sobrevivir hasta el cierre cuenta como inseguro aunque no haya un alma
cerca. El grupo 2 vive 5.000 tics más, y esos 5.000 tics los pasa dentro del
anillo que se cierra.

Lo comprobé quitando el término del anillo y dejando sólo armados y daño —**una
lectura que se me ocurrió DESPUÉS de ver el resultado, y por eso la marco**:

| fracción segura | 0.1.18 | Grupo 1 | Grupo 2 |
|---|---:|---:|---:|
| con anillo (la sellada) | 50,08 % | 44,12 % | **33,88 %** |
| sin anillo (post-hoc) | 50,59 % | 44,14 % | **35,54 %** |

**Tampoco así se salva la predicción.** No fue el anillo el que me hundió la
cifra: el cuerpo del grupo 2 pasa una fracción menor de su vida sin rivales
armados cerca, sencillamente porque su vida es mucho más larga y el final de
toda partida es un apretujón. La predicción estaba mal planteada: **pedía que
subiera una proporción cuando lo que iba a cambiar era el denominador.**

La cifra honesta que queda es la absoluta: **4.312,9 tics seguros contra
3.269,9**, un 32 % más — pero eso lo predije como «≥ 4.700» y no llega.

### PREDICCIÓN 4 · «Quién hereda el hueco» — **dos de tres**

| lo que dije | lo que salió | |
|---|---|---|
| el anillo, **≥ 9 de 20** | **14 de 20** | **acierto** |
| `zs-patient` + `skourehjan` juntos, **entre 1 y 4** | **2** (zs-patient 2, skourehjan 0) | **acierto** |
| `belobog` y `zero-sum-scavenger` **seguirán en cero** | **una muerte cada uno** | **FALLO** |

Y dije que si eso pasaba lo diría así, porque es una señal contra el criterio de
P6-0. Los dos casos:

* **`belobog`**, tic **5.184**, 13 golpes suyos, puesto 15. Es la única muerte
  temprana del grupo 2 y la causa la política que en 615 sillas-partida del
  corpus **no nos había matado nunca**.
* **`zero-sum-scavenger`**, tic **14.617**, 17 golpes suyos, puesto 5, en el
  apretujón final.

**Lectura honesta:** en P6-0 `belobog` tenía 0 muertes con **tres** sillas; aquí
tiene **cinco**, y el cuerpo vive 5.000 tics más metido en el cierre. Las dos
cosas suben su exposición. **Un «cero» de 615 sillas no es un cero: es un cero
observado, y en cuanto cambias las condiciones aparece.** Para el seis conviene
escribirlo así en vez de llamarlas «inofensivas».

---

## Lo que de verdad cambió con `roster_lento_v2`

| | Grupo 1 (v1) | Grupo 2 (v2) |
|---|---:|---:|
| muertes por políticas | 15 de 20 | **4 de 20** |
| muertes del anillo | 2 | **14** |
| vida mediana | 8.555 | **14.041** |
| puesto mediano | 13,5 | **4,5** |
| puestos obtenidos | 4,5,6,9,10,10,13,13,13,13,14,14,15,15,15,15,16,16,16,16 | **1,2,3,3,3,3,3,4,4,4,5,5,5,5,6,6,6,11,12,15** |
| quién nos pega (golpes) | relh 73 · skourehjan 36 · sivanlevy 27 · anillo 15 | **anillo 172** · scavenger 44 · zs-patient 39 · belobog 36 |

**El mundo pasó de matarnos a rivales a matarnos de anillo.** Es lo que se
buscaba: el cuerpo llega vivo al final de la partida y lo que lo mata es el
reloj, no un cuchillo.

**Y una advertencia que hay que decir aunque desluzca el resultado:** el puesto
mediano baja de 13,5 a 4,5 **en parte porque el roster pacífico también es un
roster débil**. `aaron` y `skourehjan`, que en P6-0 tienen mediana de 2 y 1
puntos, mueren pronto y suben nuestro puesto sin que hayamos mejorado en nada.
**No es una medida del cuerpo, es una medida del vecindario.** Para el seis, el
puesto en el mundo lento con `v2` **no sirve como vara**; sirven la vida en
tics y el tiempo seguro.

---

## Comprobación añadida 1 · Las versiones de los rivales

Coste cero, de los `participants` que la plataforma devuelve en cada episodio.
Comparo los diez episodios de P5-7C (0.1.18) con los diez del grupo 1 (0.1.19):
mismo brazo, mismas semillas, mismo `roster_lento_v1`.

| rival de `roster_lento_v1` | en P5-7C (0.1.18) | en el grupo 1 (0.1.19) | sillas | ¿cambió? |
|---|---|---|---:|---|
| `zero-sum-scavenger` | v12 `6244cdeb…` | v12 `6244cdeb…` | 3 | **no** |
| **`relh-zero-sum`** | **v52 `47f38a1c…`** | **v52 `47f38a1c…`** | 3 | **no** |
| `belobog` | v2 `458ec0b6…` | v2 `458ec0b6…` | 3 | **no** |
| `sivanlevy-zs-courier` | v3 `41f43efa…` | v3 `41f43efa…` | 2 | **no** |
| `zs-patient` | v3 `2b9cfd17…` | v3 `2b9cfd17…` | 1 | **no** |
| `aaron-zs-fable` | v2 `9457da2a…` | v2 `9457da2a…` | 1 | **no** |
| `skourehjan-…-scripted-v1` | v1 `3e8097e1…` | v1 `3e8097e1…` | 1 | **no** |

**Ninguno cambió. Ni uno.** Los catorce asientos rivales son bit a bit las
mismas versiones en los dos lados.

Esto es el control que le faltaba a la predicción 1: **el 0,45 → 0,75 no se
puede achacar a que `relh` jugara con otra versión**. Y no es un supuesto: la
liga tiene desde el 18 de septiembre una **v53 de `relh-zero-sum`**
(`91727661…`), que es la campeona de su autor, y la **v52 está en el banquillo**
—y aun así las veinte partidas del grupo 1 jugaron contra la v52, porque el
roster la fija por `policy_version_id` y no por nombre.

**Aviso para el seis:** si alguna vez se pide el roster por nombre, `relh`
traerá la v53 y el mundo cambiará sin que nadie lo anote.

## Comprobación añadida 2 · El diff de `src/zero_sum/sim.nim` — **NO LO PUEDO HACER**

Lo digo antes de los detalles: **no tengo acceso al repositorio del coworld**,
así que no puedo diferenciar las etiquetas `zero-sum-v0.1.18` y
`zero-sum-v0.1.19`. No voy a improvisar una lista.

Lo que intenté, todo de coste cero:

| dónde busqué | resultado |
|---|---|
| un clon local del repo | **no existe**: `~/paintball_recon` y `~/cogames` no lo contienen; `~/cogames` es un repo git **sin remotos y sin etiquetas** |
| `~/paintball_recon/docs/zero-sum/src/sim.nim` | existe, pero **P5-1 A ya lo descartó**: es una compilación posterior (battle-royal), con `budget_per_player` en vez de `sponsor.budget_per_team` y sin `stat_budget` ni `league_mode`. **No es el fuente de ninguna de las dos etiquetas** |
| el manifiesto del coworld (`GET /v2/coworlds/{id}`) | trae `documentation_url`, `forum_markdown_url` y `wiki_markdown_url`, **ninguna apunta al código** |
| la transcripción de certificación de las dos versiones | **HTTP 403** en las dos |
| el wiki de zero-sum (`pages.md`, `main.md`) y su buscador | **sin coincidencias** para `0.1.19` |
| el foro de zero-sum y su buscador | **sin coincidencias** para `0.1.19` ni para `changelog` |

**Lo único que sí puedo enseñar es el diff de lo que la plataforma publica**, el
manifiesto, comparando bloque a bloque por md5. Es una lista, y no concluyo de
ella más de lo que dice:

| bloque del manifiesto | 0.1.18 | 0.1.19 | |
|---|---|---|---|
| `game/config_schema` (entero) | `c0e660f1…` | `c0e660f1…` | **idéntico** |
| `…/properties/sponsor` | `b5560ed4…` | `b5560ed4…` | **idéntico** |
| `…/properties/zone` | `c4e0fb27…` | `c4e0fb27…` | **idéntico** |
| `…/properties/events` | `acebe264…` | `acebe264…` | **idéntico** |
| `game/observation_schema` | `37a6259c…` | `37a6259c…` | idéntico |
| `game/action_schema` | `37a6259c…` | `37a6259c…` | idéntico |
| `variants[0]` = **`competition`**, la que jugamos | `bdef8442…` | `bdef8442…` | **idéntico** |
| `certification` | `42f33baf…` | `42f33baf…` | idéntico |
| `player[0]` salvo la imagen | `ae2106f8…` | `ae2106f8…` | idéntico |
| **`game/results_schema`** | `54f26040…` | `b36099fd…` | **cambia**: aparece `game_version` (string, `minLength: 1`) |
| **`game/runnable/image`** y `player[0].image` | `cogames@sha256:953424bb…` | **`cogames@sha256:5403c453…`** | **cambia** |
| `game/replay_viewer/bundle` | `sha256:b0e811ab…` | `sha256:9c507088…` | cambia |
| **`variants[1]`** | `casual-live` — «Casual (live sponsors)», `sponsor.live: true`, `league_mode: solo`, sin eventos ni regalos | **`duos`** — «Self-paired Zero Sum for 8 policies controlling adjacent teams of 2», `sponsor.live: false`, `league_mode: duos`, 16 regalos programados y un evento `flood` | **sustituida** |

**Lo que esta lista dice, literalmente:** de lo que toca combate, anillo, vida o
patrocinador, **nada visible cambia** — el esquema de configuración entero, con
sus bloques de `sponsor`, `zone` y `events`, es idéntico byte a byte, y la
variante que jugamos también. Lo único que cambia y podría afectar al combate
es **el binario del motor**, y su contenido no es público.

**Lo que esta lista NO dice:** que el combate no haya cambiado. Un cambio dentro
del binario no aparece en el manifiesto. La diferencia de 0,45 a 0,75 muertes
por vida del grupo 1 **queda sin explicación desde aquí**, y con p = 0,105
tampoco está establecida. Si se quiere resolver, hacen falta dos cosas que no
tengo: **más semillas** y **preguntar a Ari qué entró en la 0.1.19**.

---

## COSTE

| | |
|---|---|
| episodios | 20 (4 tandas de 5, como decía el sello) |
| **coste total** | **1,8333 USD** |
| tope del encargo | 3,00 USD · parada propia en 2,40 · **no se tocó ninguno** |
| por episodio | 0,092 de media · de 0,035 a 0,1133 |
| sin facturar | 1 episodio de los 20 (la séptima vez que pasa; van seis en el cinco) |
| tiempo de juego | 8,2 – 11,0 min por episodio, **igual que en 0.1.18** (mediana 10,3) |

`motor/model.py` al terminar: `1e511978c251130e95169ebf8443efa1`. Intacto.

---

## LO QUE ME LLEVO

1. **El cinco ya está guardado y etiquetado en local.** Sin claves dentro, con
   los 199 md5 comprobados y los 12 GiB de diarios inventariados fuera.
2. **`roster_lento_v2` funciona, y con potencia**: 15 de 20 muertes por
   políticas pasan a 4 de 20 (p = 0,0012), la vida crece 5.004 tics de mediana
   emparejando por semilla (18 de 20 pares, p = 0,0004). La cifra que escribí
   antes de jugar, 0,169, salió 0,20.
3. **Mi predicción del tiempo seguro estaba mal planteada** y falló en las tres
   lecturas. Pedí que subiera una proporción cuando lo que iba a cambiar era el
   denominador.
4. **`belobog` y `scavenger` no son inofensivas**, sólo no las habíamos visto
   matar. Con cinco sillas y un cuerpo que vive hasta el cierre, mataron una vez
   cada una.
5. **0.1.19 puede ser más duro que 0.1.18 y no lo puedo probar.** El punto se
   mueve (0,45 → 0,75), las tres medidas apuntan igual, pero p = 0,105 y el
   código no es público. Quedan dos cosas por hacer que no son mías: más
   semillas y preguntarle a Ari.
6. **El puesto deja de servir como vara en el mundo `v2`**, porque el roster
   pacífico es también un roster débil. Para el seis: vida en tics y tiempo
   seguro.

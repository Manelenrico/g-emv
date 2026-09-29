# P5-ARI2 — auditoría de plataforma, solo lectura

**Coste cero.** Nada lanzado, nada enviado, nada cancelado: solo lecturas de
ficheros y tres `GET`. Motor, decisor y tabla intocados
(`1e511978c251130e95169ebf8443efa1` · `8fa03547e3228ef9df4aa94c444f9252` ·
`98c13d60167c80cc8334c965be75c640`), idénticos al empezar y al acabar.
**No aparece ninguna clave ni el contenido de `.env`.**

**Nota de método:** **no existe `episodios.json`.** El registro de episodios de
este proyecto son los **216 ficheros JSON por episodio** de `cantera/paper5/`,
uno por episodio, guardados al recogerlos. Todo lo de abajo sale de ahí.

---

## 1 · Versión del juego

**Los 216 episodios del paper cinco corrieron con la misma versión. No hay ni
una excepción.**

```
coworld_version = '0.1.18'
coworld_name    = 'zero-sum'
coworld_id      = 'cow_ebf72b34-cdad-44ad-a0d5-5a65839e49d6'
                                            ->  216 episodios de 216
```

**Episodios que NO son 0.1.18: cero.** No hay lista que dar.

### Los 216, por origen

| serie | episodios |
|---|---|
| `P56C` | **100** |
| `P57C` | **40** |
| `P58M` | **40** |
| `P58I` | 10 |
| `P56B` | 10 |
| `B1`, `C2`, `C3`, `P58B`, `P58D`, `P58E`, `P58H`, `P58K` | 2 cada uno |
| **total** | **216** |

*De dónde sale:* `cantera/paper5/*.json`, campo `episodes[].coworld_version` de
cada documento de petición.

---

## 2 · El parón del 22-sep, entre 07:09Z y 13:14Z

**Nuestro registro NO muestra partidas paradas ni sin arrancar en esa ventana.
Lo que muestra es que no lanzamos nada.**

| | |
|---|---|
| episodios de serie creados el 22-sep | **58** |
| **de ésos, que nunca arrancaron** | **0** |
| **de ésos, no completados** | **0** |
| cola mediana del día | **1,0 min** (mín 0,2 · máx 8,8) |

**El hueco existe, pero es de creación, no de ejecución:**

| | UTC |
|---|---|
| última creación antes del hueco | **06:57:31Z** (`P58I_t1_K_20679832`, arrancó a 06:58:44Z) |
| primera creación después | **12:55:32Z** (`P58K_t0_A_20260916`) |
| **hueco** | **5 h 58 min 01 s** |

**Ese hueco es nuestro:** entre las 06:58Z y las 12:55Z estuve trabajando en
seco (el diagnóstico P5-8J, coste cero) y no envié ninguna petición. **No hay
nada que la plataforma dejara de programar.**

### La única traza compatible con una lentitud de plataforma

**La primera petición después del hueco tuvo la cola más larga del día:**

```
12:55:32Z creada -> 13:04:23Z arranca · cola 8,8 min · completed   P58K_t0_A_20260916
12:55:33Z creada -> 13:04:23Z arranca · cola 8,8 min · completed   P58K_t0_K_20260916
```

**8,8 minutos contra una mediana de 1,0 del mismo día** — ocho veces y media.
Las dos arrancaron y acabaron bien. **Cae justo dentro de tu ventana (arrancan a
las 13:04:23Z, antes de las 13:14Z), y es lo único que hay.**

**Contraste con el parón del 21**, que sí fue de plataforma: allí hubo
**peticiones creadas a las 07:10:16Z que nunca se programaron** y hubo que
cancelarlas. **Aquí no hay ninguna.**

*De dónde sale:* `episodes[].created_at` / `running_at` / `status` de los 58
documentos del 22-sep.

---

## 3 · Cómo pedimos

**Usamos `target.league_id`. Nunca fijamos `coworld_id`.**

```python
# cantera/paper5/lanza_P58M.py:42
return {"private": True, "target": {"league_id": LIGA}, "num_episodes": 1, …

# cantera/paper5/lanza_P58M.py:15
LIGA = "league_6764202e-2ac1-4c98-a77e-cabc75582939"
```

Idéntico en `lanza_P56C.py:45` / `:16`, `lanza_P57C.py:43` / `:15`,
`lanza_P56B.py:15`, `lanza_B1.py:15`, `lanza_P58D.py:15`.

**Ningún script nuestro menciona `coworld_id` en el cuerpo de la petición.** El
`coworld_id` solo aparece en las **respuestas** que guardamos, puesto por el
servidor. **Es decir: la versión del mundo nos la elige la liga, no la pedimos
nosotros** — y por eso el punto 1 sale uniforme sin que hayamos hecho nada para
conseguirlo.

**En cola ahora mismo: nada.**

```
pending   : 0 peticiones · 0 episodios sin acabar
submitted : 0 peticiones · 0 episodios sin acabar
running   : 0 peticiones · 0 episodios sin acabar
gasto acumulado: 138,061431 USD
```

*(Comprobado con `cantera/paper5/estado_P56B.py`, que es **solo GET** y lo dice
en su cabecera: «SOLO GET: gasto acumulado cobrado y cola. No crea ni cancela
nada.»)*

---

## 4 · Horas de lanzamiento, UTC

**200 lanzamientos de serie, repartidos en 13 horas distintas de 24.**

| hora UTC | episodios | |
|---|---|---|
| 03Z | 12 | ████████████████ |
| 04Z | 12 | ████████████████ |
| 05Z | 20 | ██████████████████████████ |
| **06Z** | **28** | █████████████████████████████████████ |
| 07Z | 2 | ██ |
| 12Z | 2 | ██ |
| 13Z | 6 | ████████ |
| 14Z | 20 | ██████████████████████████ |
| **15Z** | **30** | ████████████████████████████████████████ |
| 16Z | 20 | ██████████████████████████ |
| 19Z | 10 | █████████████ |
| **21Z** | **26** | ██████████████████████████████████ |
| 22Z | 12 | ████████████████ |

**Sin lanzamientos:** 00Z, 01Z, 02Z, 08Z, 09Z, 10Z, 11Z, 17Z, 18Z, 20Z, 23Z.

| por día | episodios |
|---|---|
| 2026-09-20 | 36 |
| **2026-09-21** | **106** |
| 2026-09-22 | 58 |

**Los picos son 15Z (30), 06Z (28) y 21Z (26).** El reparto es de nuestra
jornada, no de ninguna política de envío: lanzamos cuando hay un «sí» de la
mesa.

---

## 5 · Semillas

**Las fijamos nosotros, una explícita por partida. No dependemos de nada que
tenga que darnos la plataforma.**

```python
# cantera/paper5/lanza_P58M.py:31-35
def cuerpo(brazo, semilla, tanda):
    doc = json.load(open(os.path.join(AQUI, "roster_lento_v1.json")))
    cfg = dict(doc["game_config_overrides"])
    cfg["seed"] = semilla          # <- la semilla, explícita
```

La lista está congelada en disco, `cantera/paper4/semillas_S2.json`:

| | |
|---|---|
| cuántas | **20** |
| primera · última | **20260916** · **22250767** |
| paso entre consecutivas | **104729, constante** *(es primo)* |
| **¿todas distintas?** | **sí** |

**No se repiten dentro de un lote, y la plataforma no las incrementa:** la misma
semilla va en las dos peticiones del par (brazo A y brazo K), que es justo lo
que hace comparable el par. **Un lote de cinco semillas × dos brazos son diez
peticiones con cinco valores de `seed`, cada uno enviado dos veces a propósito.**

**Lo único que la plataforma decide es el reparto de puestos de los rivales**, y
se comprobó en P5-8M que **coincide elemento a elemento entre los dos brazos de
la misma semilla** en las veinte.

---

## 6 · Herramientas en riesgo con 0.1.19

**Ninguna de las que usa el paper cinco. Con tres matices que conviene tener.**

### ¿Alguien lee la cabecera de un replay y exige versión 1?

**No.** Los ficheros que tocan replays (`paintball/buenas_replay.py`,
`gemelos_gif.py`, `aliento.py`, `censo.py`, `debut.py`, `ladron.py`,
`buenas.py`, `cantera/paper5/confianza.py`) **no comprueban ninguna versión de
cabecera**: el grep de `version` sobre los lectores de replay no devuelve nada.

**Y además ninguno se usa en el paper cinco.** Todo el análisis P5 sale de los
**diarios `.art.log`** que escribe nuestra propia política, no de los replays de
la plataforma. *(Regla del proyecto: verificación visual con matplotlib sobre
datos crudos, nunca MettaScope.)*

### ¿Alguien recorre todas las claves de `results.json`?

**No.** Los tres que lo abren toman **claves concretas**:

| fichero | línea | qué toma |
|---|---|---|
| `paintball/escondite.py` | 98, 103 | `r["placements"][c]` |
| `paintball/finale.py` | 35-38 | lo carga y cruza con nuestro `final` |
| `paintball/aliento.py` | 28, 306 | coteja `kills` y `placement` con nuestro `final` |

**Ninguno itera el diccionario entero**, así que una clave nueva en 0.1.19 no
los rompe. **Y los tres son de la era paintball: el paper cinco no los usa.**

De hecho `paintball/promesa.py:4` deja escrito el criterio del proyecto: el
puesto sale **«de nuestro registro `final`, nunca de la tabla `placements` del
`results.json`»**.

### ¿Alguien valida contra un esquema fijo?

**Sí, uno, y está pinchado a 0.1.18 por fichero:**

```python
# cantera/paper5/hace_lento_v0.py:12
MAN = json.load(open(os.path.join(AQUI, "manifiesto_zero_sum_0_1_18.json")))
# :14
ESQ = MAN["game"]["config_schema"]["properties"]
# :85-88
jsonschema.validate(dict(cfg, tokens=["t"] * 16), MAN["game"]["config_schema"])
```

**`hace_lento_v0.py` es el que FABRICA `lento_v0`**, y lo construye y valida
contra un manifiesto **local y congelado del 0.1.18**.

**El riesgo real, y es acotado:** si con 0.1.19 hubiera que **regenerar**
`lento_v0`, este script lo construiría contra el esquema viejo. **Pero las
series no lo regeneran**: leen `roster_lento_v1.json`, que está congelado en
disco. **Ningún lanzador, recolector ni descargador del paper cinco lee el
manifiesto en vivo** (comprobado: el grep de `manifest|config_schema` sobre
`lanza*.py`, `ciclo*.py`, `baja*.py` y `recoge*.py` no devuelve nada).

**Otro validador, fuera del paper cinco:** `paintball/alma/verifica_41.py`.

---

## 7 · Liga

**No. Ningún script nuestro usa la clasificación de liga de nada, ni de
`gemv-anima:v1` ni de ninguna otra política.**

- **Ningún script llama a un endpoint de liga**: el grep de `/v2/leagues`,
  `leaderboard` y `standings` sobre todo el repositorio no devuelve nada.
- **El identificador de liga aparece solo como destino** de la petición
  (`target.league_id`, `lanza_*.py:15`), nunca se lee de vuelta.
- Las «clasificaciones» que salen en `cantera/paper4/analiza_S3.py:7,211` y
  `rev2_medidas.py:7` **son de propuestas del consejero** (IMPOSIBLE /
  traducibles), no de liga.
- `gemv-anima:v1` (`76cdff1a-4652-4748-a720-8e103286489d`) se nombra en
  `paintball/aliento.py:41,116` y `paintball/censo.py:50` **solo para
  identificar nuestros asientos en el `results.json`**, no para leer un puesto
  de liga.

**Todo nuestro puesto sale del registro `final` de nuestro propio diario.**

---

## 8 · Re-ejecuciones

**No hay ni una señal de re-ejecución en los siete casos.**

| | |
|---|---|
| pares (serie, brazo, semilla) con **más de un episodio** | **0 de 200** |
| los seis sin facturar: `job_index` | **0** en los seis |
| los seis sin facturar: `round_id` | **`null`** en los seis |
| el del artefacto que falta: `job_index` / `round_id` | **0** / **`null`** |

| episodio | creado (UTC) | |
|---|---|---|
| P5-6C F/20679832 | 2026-09-20 21:44:21Z | sin facturar |
| P5-6C F/22564954 | 2026-09-21 05:03:28Z | sin facturar |
| P5-6C F/23402786 | 2026-09-21 06:08:18Z | sin facturar |
| P5-7C A/20889290 | 2026-09-21 15:19:37Z | sin facturar |
| P5-8I A/20679832 | 2026-09-22 06:57:31Z | sin facturar |
| P5-8M A/21622393 | 2026-09-22 15:34:14Z | sin facturar |
| **P5-8M K/20784561** | 2026-09-22 15:03:47Z | **facturado 0,097807 $**, sin artefacto del agente 10 |

**Cada uno se creó una vez y se completó una vez.**

**Y un dato que descarta la sospecha más natural:** los tres sin facturar de
P5-6C se crearon el **20-sep 21:44Z**, el **21-sep 05:03Z** y el **21-sep
06:08Z** — **los tres ANTES del parón de las 07:10Z**. **Ninguno de ellos es una
de las seis que hubo que cancelar y relanzar.** Las seis del parón sí fueron
re-ejecuciones nuestras, y las seis se facturaron con normalidad.

**El límite de esta respuesta, dicho:** nuestro registro guarda el documento
**final** de cada petición. **Si la plataforma reintentó por dentro, nosotros no
lo veríamos.** Lo que puedo afirmar es que **por nuestro lado no hubo dos
intentos con la misma semilla en ninguno de los siete**.

---

## Resumen en cinco líneas

**Los 216 episodios del paper cinco corrieron con una sola versión, 0.1.18
(`cow_ebf72b34`), sin una sola excepción — y no porque la pidiéramos: pedimos
por `target.league_id` y nunca fijamos `coworld_id`, así que la versión nos la
eligió la liga.**

**El 22 de septiembre no hubo parón por nuestro lado: los 58 episodios de ese
día arrancaron y acabaron, y el hueco de casi seis horas entre las 06:58Z y las
12:55Z es tiempo en que no lanzamos nada; lo único raro es que la primera
petición de después tardó 8,8 minutos en arrancar contra una mediana de 1,0.**

**Las semillas las fijamos nosotros una a una desde un fichero congelado de
veinte valores, y no dependemos de nada que tenga que darnos la plataforma.**

**Con 0.1.19 no hay ninguna herramienta del paper cinco en riesgo: no leemos
replays, no recorremos `results.json` entero y no validamos contra un esquema en
vivo; el único validador de esquema, `hace_lento_v0.py`, está pinchado a un
manifiesto local del 0.1.18 y solo haría falta si alguna vez regeneráramos
`lento_v0`.**

**Ni usamos la clasificación de liga para nada, ni hay señal de que ninguno de
los seis episodios sin facturar ni el del artefacto perdido fuera una
re-ejecución: cero semillas repetidas, `job_index` 0 y `round_id` nulo en los
siete.**

---

**PARO AQUÍ.**

# P5-1 fase B1 — Una partida en el mundo lento provisional

Una petición privada, un episodio, semilla 1 de la lista. Salió bien y salió
**barata**, que no es lo que decían las dos predicciones.

## Las cuatro comprobaciones previas, antes de crear nada

### 1. La red de la subida escala con `max_ticks`

`paintball/alma/policy_cortex.py:422-424`:

```python
        _mt = getattr(self.mundo, "max_ticks", 0) or 0
        if _mt and self.tick >= 0.95 * _mt and not self.artefacto_subido:
            sube_artefacto(self, f"red al 95 % de max_ticks ({_mt})")
```

No es un reloj sino una fracción de la duración configurada, que llega en el
`player_config`. Con 18.240 el umbral es `0,95 × 18240 = 17328` exacto, y la
condición es `>=`:

```
  tic 17327: 17327 >= 17328.0 -> False
  tic 17328: 17328 >= 17328.0 -> True
```

**Dispara en el 17.328 y nunca antes.** En la partida de hoy el umbral es 8664
de 9120, que es lo que imprime el humo (xv).

En esta partida **la red no llegó a hacer falta**: nuestro último asiento murió
en el tic 12.456 y el artefacto subió por el camino normal, el de fin de
partida.

### 2. El diario cabe con muchísimo margen

El contrato son **200 MB de zip** (`policy_cortex.py:185`), y lo que se sube es
un zip: `sube_artefacto` comprime con `ZIP_DEFLATED` antes del PUT.

| medida, sobre los 260 diarios ligeros de S-2 | valor |
|---|---|
| zip mayor que llegó a viajar | **1,10 MB** (14.498 líneas, brazo B) |
| zip mediano | 0,21 MB |
| el mayor, **doblado** | **2,20 MB** = **1,1 %** de los 200 MB |
| diario en crudo mayor, sin comprimir | 25,1 MB |
| ese mismo, doblado y aún sin comprimir | 50,2 MB = 25 % de los 200 MB |

**Y lo que pasó de verdad**, que confirma la cuenta: el diario del asiento 10 de
esta partida ocupó **27,5 MB en crudo** y **1,14 MB en zip**, o sea el **0,57 %**
del límite.

### 3. La imagen, subida y anotada antes de la petición

```
$ docker image inspect gemv-anima:s3 --format '{{.Id}}'
sha256:495c04a784d396d0d53d4841d354fb54c4efae6a4ce54705893108faec0cd72e

$ docker run --rm --platform linux/amd64 -e GEMV_CORTEX=0 gemv-anima:s3 \
      python -u /app/alma/humo_cortex.py
  HUMO S-2 COMPLETO          (los dieciséis, hoy, dentro de la imagen)

$ coworld upload-policy gemv-anima:s3 --name gemv-p5-A --tag purpose=P5-1-lento-brazoA
Upload complete: gemv-p5-A:v1
   policy_version_id = 4127bf16-85f3-4588-a055-b174ca72b6c1
   2026-09-19T14:38:08.283779Z
```

Es la misma imagen que jugó S-3, sin reconstruir y **sin un solo
`--secret-env`**: el `Dockerfile.cortex` ya trae `GEMV_CORTEX=0` en su `ENV`, así
que esto es el cuerpo solo. Todo quedó escrito en `cantera/paper5/ACTA.md` a las
14:38, **antes** de crear la petición de las 14:39.

### 4. Gasto acumulado antes

```
  episodios cobrados: 223
  gasto acumulado   : 79.837381 USD
```

### Y la cola, antes de crear

```
pending   :   0 peticiones ·    0 episodios sin acabar
submitted :   0 peticiones ·    0 episodios sin acabar
running   :   0 peticiones ·    0 episodios sin acabar
```

Nada por delante, así que no hubo que esperar tu sí. (Salvedad: el endpoint
muestra lo que esta cuenta ve.)

---

## La petición

```
### RESPUESTA 200 ###
 "id": "xreq_505e8f3b-e940-41d9-9593-9640c0ffccf5",
 "coworld_name": "zero-sum", "coworld_version": "0.1.18",
 "variant_id": "competition", "status": "pending", "episode_count": 1,
 "created_at": "2026-09-19T14:39:28.464146Z",
 "episodes": [{"id": "ereq_50c6300c-d5c0-47d4-a4b9-da5a8e256bfa", ...}]

 "cost_preview": {
  "estimated_cost_credits": 2.2414446462962974,
  "player_pod_llm_spend_limit_usd": null
 }
```

**El `cost_preview` que la fase A no pudo pedir.** Confirma lo que decía el
esquema: solo existe al crear. El límite de gasto de modelo viene **nulo**, que
es lo coherente con un brazo sin consejero.

**La configuración llegó entera**, y con ella se contesta la duda declarada en
A2: mandando el objeto `sponsor` completo, los dieciséis regalos sobreviven.

```
   max_ticks = 18240 · freeze_ticks = 480 · stat_budget = 20
   seed = 20260916 · league_mode = solo
   zone.schedule = [[7296, 7536, 8076, 24, 19, 1], ... , [14136, 14376, 14916, 3, 0, 24]]
   sponsor = {'live': False, 'scripted_gifts': 16, 'budget_per_team': 600,
              'shop_opens_tick': 1680}
```

Y el mundo se lo creyó: el `player_config` que llegó a los dos asientos dice
`max_ticks 18240`, `ignition_tick 480`, `tick_rate 24`.

---

## 1. El precio, los tiempos y el gasto

```
creada   : 2026-09-19T14:39:28.464146Z
despacho : 2026-09-19T14:40:12.549433Z
arranque : 2026-09-19T14:40:28.872078Z
fin      : 2026-09-19T14:50:54.135905Z

cola (despacho->arranque):     16.3 s = 0.27 min
corriendo (arranque->fin) :    625.3 s = 10.42 min
vida del pod (despacho->fin): 641.6 s = 10.69 min

COSTE: 0.052471 USD
```

| | |
|---|---|
| **precio del episodio** | **0,052471 $** |
| minutos en cola | **0,27** |
| minutos corriendo | **10,42** |
| gasto acumulado antes | 79,837381 $ (223 episodios) |
| gasto acumulado después | **79,889852 $** (224 episodios) |

**Una partida del doble de larga costó menos que una de S-2.** La mediana de
S-2 fue 0,0556 $ por 9.120 tics; esta ha sido 0,0525 $ por una configurada a
18.240. Y costó catorce veces menos que la mediana de S-3, que era la misma
partida de siempre esperando hora y media en cola.

## 2. La partida

| | asiento 10 | asiento 11 |
|---|---|---|
| tics vividos (fase `live`) | **11.976** | **376** |
| último tic del diario | 12.456 | 856 |
| vida al empezar / al acabar | 100 → 5 | 100 → 1 |
| líneas de diario | 12.965 | 891 |
| diario en crudo / en zip | 27,5 MB / 1,14 MB | 1,68 MB / 0,05 MB |
| puntuación | 5,0 | 1,0 |

**La duración real del episodio en tics no la publica la plataforma**: el
`episode-stats` trae `game_stats: {}` y `steps: 0`. Lo que sí es dato duro es
que **nuestro diario llega al tic 12.456**, así que el episodio duró al menos
eso. Por el reloj de pared la cosa apunta a que corrió los 18.240 enteros: S-2
hacía 9.120 tics en ~303 s, o sea ~30 tics por segundo, y estos 625 s a ese
ritmo son ~18.800. **Lo digo como estimación, no como medida.**

**Los dos murieron, y de cosas distintas.**

- **Asiento 11**, en el tic ~857: lo mataron a tiros. Seis golpes de unos veinte
  puntos entre los tics 733 y 839, con el anillo todavía en radio 24 y daño 0.
  Vivió 376 instantes, que son **15,7 segundos** de juego.
- **Asiento 10**, en el tic ~12.457: **lo mató el anillo**. Los tres últimos
  golpes vienen etiquetados en el propio diario:
  ```
  tic 12313 hp 18 pos [17, 27] centro [24, 24] radio 7 d/s 8
     damage_taken: [{"source": "zone", "amount": 6.56}]
  ```
  Aguantó 11.976 instantes, **8 min 19 s** de juego, y llegó vivo hasta la
  quinta de las siete etapas del anillo.

## 3. El anillo llegó donde se le dijo

| suceso | previsto en `lento_v0` | medido en el diario |
|---|---|---|
| encendido | tic 480 | **`ignition` en el tic 481** |
| primer aviso del anillo | tic 7296 | **`zone_warning` en el tic 7297** |
| primer encogimiento | tic 7536 | radio 24 → 23 en el **7644** |
| inundación | tic 4400 | `flood` en el **4281** |

El primer evento del anillo cae **exactamente** donde lo pusimos, un tic después
del `warn_tick`, igual que en S-2 (allí el aviso era 1440 y el evento salió en
el 1441). El asiento 10 vio cinco de los siete avisos y las etapas de radio 24,
19, 15, 11 y 8 antes de morir en la de radio 6.

**Y esto es lo que buscábamos:** el cuerpo tuvo **6.816 instantes de juego sin
anillo**, del 481 al 7296, contra los 1.200 del mundo de hoy. Si hay calma en
alguna parte, está ahí. Medirla es la fase C.

## 4. Cotejo de P1 bis

> **P1 bis (sellada antes de jugar).** El coste del episodio será un céntimo por
> minuto de vida del pod, cola incluida, ± 30 %; con cola vacía, menos de
> 0,25 $.

| cláusula | contador | valor sellado | medido | veredicto |
|---|---|---|---|---|
| un céntimo por minuto de vida del pod ± 30 % | `coste / minutos de vida del pod` | 0,0100 ± 30 % = **[0,0070 · 0,0130]** | **0,00491 $/min** | **FALLA** |
| con cola vacía, menos de 0,25 $ | `coste del episodio` | < 0,25 $ | **0,0525 $** | **CUMPLE** |

**El contador podía variar, y de hecho varió.** En los 223 episodios de S-2 y
S-3 ese mismo cociente estuvo pegado a un céntimo: mediana 0,00998 en S-2 con un
p10-p90 de 0,00979 a 0,01006, y mediana 0,01018 en S-3. Aquí ha salido
**0,00491**, menos de la mitad, y muy fuera de la banda. No es ruido del
redondeo: es otro precio.

**No sé por qué, y no me lo invento.** He probado dos explicaciones y las dos
fallan:

- *¿Se cobra solo lo que corre?* No: a 0,00504 $ por minuto corriendo, sigue
  siendo la mitad de los 0,01102 de S-2.
- *¿Se cobran los tics vivos de nuestros dos asientos?* Tampoco. Sobre los 130
  episodios de S-2 con los dos diarios, la correlación entre coste y tics vivos
  nuestros es de solo **+0,26**, y el ajuste predice 0,0834 $ para esta partida
  contra los 0,0525 reales.

Quedan sin descartar, y sin comprobar desde aquí: que la tarifa haya cambiado
entre el 18 y el 19 de septiembre, que la máquina que tocó fuera más barata, o
que se cobre solo parte de la vida del pod. **Las tres partidas de la fase C
darían tres puntos más y permitirían separarlas.**

### Y de paso, sobre P1

P1 decía que el precio estaría entre 0,8 y 2,0 $ y por encima de los 0,742 de
S-3, porque la partida es más larga. Ha costado **0,052471 $**. Se cotejará
formalmente en la fase C, con las tres partidas, pero el primer dato va en
contra, y va en contra por el motivo que ya avisé en la fase A: **la duración de
la partida no es lo que fija el precio**.

---

## Lo que queda sobre la mesa

1. **La fase C**, tres episodios con las semillas 2 y 3 más este, para medir la
   calma. El precio esperado, con este dato, es del orden de **0,05 $ por
   episodio** si la cola sigue vacía; los 0,80 $ del tope del encargo quedan muy
   lejos.
2. **Un aviso de método para C.** Esta partida da **12.352 instantes-asiento
   vivos**, y uno de los dos asientos murió a los 15 segundos. Si eso se repite,
   las medidas de calma del asiento 11 pesarán poco y habrá que decirlo en las
   fracciones.
3. **El preset de Ari sigue sin llegar.** Todo esto es `lento_v0` provisional.

**PARO AQUÍ.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Ficheros de esta fase: `cantera/paper5/ACTA.md`, `lanza_B1.py`, `vigila_B1.py`,
`baja_B1.py`, `analiza_B1.py`, `B1_peticion.json`, `B1_final.json`,
`B1_medidas.json`, `B1_vigilancia.log`, y los dos diarios en
`paintball/runs/P5_B1/`.

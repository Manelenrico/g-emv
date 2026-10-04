# P6-0 · Congelar el cinco y elegir los rivales del seis mirando partidas enteras

*Sólo lectura y análisis. **Coste de plataforma: cero**, no se jugó ninguna
partida. `motor/model.py` intacto (md5 `1e511978c251130e95169ebf8443efa1`,
comprobado). No se subió, publicó, empujó ni borró nada. Nada en nombre de
Manel.*

Medido por `cantera/paper6/censo_rivales.py` → `cantera/paper6/P6_0_censo.json`.
Inventario por `cantera/paper6/congela_paper5.py` → `cantera/paper5/CONGELADO.md`.

---

# A · CONGELAR EL CINCO

## A.1 y A.2 · El inventario

**199 archivos** con ruta y md5 en **`cantera/paper5/CONGELADO.md`**, en siete
grupos: el motor y el planificador (5), la receta de la imagen que jugó
(`Dockerfile.forma`), el alma entera (62 `.py`), las nueve piezas del cinco que
viajan dentro de la imagen, los presets del mundo (5), `serie_util.py` heredado
del cuatro, y los 117 scripts de banco, medida, lanzamiento y figuras.

La lista no es mi criterio: es **lo que copia `Dockerfile.forma`**, más los
scripts que midieron. Las tres custodias que ese Dockerfile ya comprobaba en
cada build siguen cuadrando hoy:

| archivo | md5 exigido por el build | hoy |
|---|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` | **igual** |
| `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` | **igual** |
| `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` | **igual** |

## A.3 · La etiqueta: NO la he creado, y te digo por qué

**Hay cambios sin guardar, así que paré, como pedía el encargo.** Pero el
problema es más gordo que dos archivos sueltos:

| | |
|---|---|
| rama | `paintball` |
| HEAD | `8a77e23` · **5 de septiembre de 2026** · *«PROMPT_72: la ablacion de campo»* |
| etiquetas | ninguna |
| modificados | 2 (`.claude/settings.local.json`, `.gitignore`) |
| sin seguir (`??`) | **90 entradas** |

**El paper cinco entero está sin seguir.** El último commit es del 5 de
septiembre; el cinco empieza el 16. De los 199 archivos del inventario, **155
no están en git**, y el reparto es el que duele: de `cantera/paper5/` están
seguidos **0 de 129**; de `paintball/alma/`, 39 de 63, pero los 24 que faltan
son justo los del cinco (`policy_forma.py`, `forma_viva.py`, `confianza_viva.py`,
`appraisal_zs_v42_exp.py`, `cortex_t5.py`, `hilo_forma.py`, los `humo_*.py`, los
siete `Dockerfile.*`). Lo que sí está en git es el poso de los papeles tres y
cuatro: los `verifica_*.py`, `policy.py`, `mundo.py`, `decisor_zs.py`.

**Etiquetar `8a77e23` como `paper5-final` sería peor que no etiquetar**: pondría
el sello del cinco en un commit que no contiene ni una línea suya, y a partir de
ahí cualquiera —incluido tú dentro de seis meses— creería que el cinco está
congelado cuando no lo estaría.

Comprobado además con `git check-ignore`: **`cantera/` y `paintball/runs/` NO
están en `.gitignore`**. Están fuera porque nunca se añadieron, no porque se
excluyeran a propósito.

**Lo que propongo, y espero tu palabra:** (1) decidir si los diarios entran o se
excluyen con una regla explícita; (2) un commit «paper cinco, final» con el
código; (3) **entonces** `git tag paper5-final` local, sin empujar. Mientras
tanto, **los md5 de `CONGELADO.md` son el congelado real**.

## A.4 · `cantera/paper6/`

Creada. Ya tiene `censo_rivales.py`, `congela_paper5.py`, `P6_0_censo.json`,
este informe y la propuesta de roster.

---

# B · LOS RIVALES, PARTIDAS ENTERAS

## B.2 · QUÉ SE PUEDE CONTAR (esto va primero, como pediste)

Lo miré antes de contar nada. El resumen es: **de muertes, sólo las nuestras**.

| lo que preguntas | ¿está en el diario? | detalle |
|---|---|---|
| quién nos pega | **SÍ, con autor** | `damage_taken[].source = "P<asiento>"`, `"zone"` o `"poison"`, con tic y cantidad |
| quién nos mata | **SÍ, por inferencia** | el diario NO guarda el golpe que mata (el cuerpo deja de observar al morir). Regla de `E3_golpes.py`: la muerte va al **último golpe registrado en los 48 tics anteriores al `match_ticks`**; si no hay ninguno, «no consta» |
| que un rival ha muerto | **SÍ, parcialmente** | evento `death_fireworks` con `slot` y `pos`… pero **sólo si nuestro cuerpo lo ve**. En el mundo lento vimos **1.684** muertes de rivales; en el normal, **1.678** |
| **quién mató a ese rival** | **NO. En ningún sitio.** | `death_fireworks` no trae autor, y no tenemos el diario del muerto |
| cuántas mata cada rival | **NO** | `final.kills` es **nuestro**, sólo de nuestros dos asientos |
| cuánto sobrevive cada rival | **SÍ, por inferencia** | ver más abajo: la escalera de puntos |

Lo comprobé también contra la plataforma: el único fichero de estadísticas por
agente que guardamos (`B1_stats_episode-stats.json`) trae **sólo `reward` por
agente**; `game_stats` viene vacío y no hay bajas ni muertes de nadie.

**Así que trabajo con lo nuestro**, y lo digo en cada tabla: lo que mido es
**el peligro que cada política supone PARA NUESTRA CRIATURA**, no su agresividad
en abstracto. Una política podría ser una carnicera con los demás y no tocarnos
nunca; esto no lo vería.

### Un hallazgo que sí permite medir «cuánto sobrevive ella»

Cruzando el `final` de nuestros diarios con el `participant_scores` de cada
episodio, los puntos resultan ser **una escalera determinista del puesto más las
bajas**, sin una sola excepción en los **399** diarios con puesto conocido:

```
puntos = ESCALERA[puesto] + kills
ESCALERA = {1:15, 2:12, 3:10, 4:8, 5:7, 6:6, 7:5, 8:4,
            9:3, 10:3, 11:2, 12:2, 13:1, 14:1, 15:0, 16:0}
```

Como `kills ≥ 0`, de los puntos de un rival sale una **cota**: su puesto **no
puede ser mejor** que el que da la escalera. Es una cota honesta, no el puesto.
Con eso mido supervivencia de cada rival sin necesitar su diario.

### Lo que NO he hecho y se podría

Al ver un `death_fireworks` se podría mirar quién estaba al lado en ese tic y
adjudicarle la muerte. **No lo he hecho**: sería una atribución inventada, sin
regla previa y sin forma de validarla. Si la quieres, es un encargo aparte y con
su propio criterio escrito antes de mirar.

---

## B.1 · Las tablas

Dos corpus, separados como pediste. **Ninguno mezcla mundos.**

| | **mundo NORMAL** (S-2 y S-3) | **mundo LENTO** (paper cinco) |
|---|---|---|
| episodios | **222** | **205** |
| diarios nuestros | 444 | 409 |
| `max_ticks` · `freeze_ticks` | 9.120 · 240 | 18.240 · 480 |
| primer aviso del anillo | tic 1.440 | tic **7.296** |
| roster | el original de 10 políticas | **`roster_lento_v1`, idéntico en los 205** |
| vida mediana de nuestra criatura | **2.050 tics** | **8.822 tics** |
| puesto mediano nuestro | 13 | 12 |
| muertes nuestras | 438 (de 444) | 405 (de 409) |
| bajas que hacemos nosotros | 53 | 34 |

*Control:* las muertes antes del tic 2.000 del mundo normal reproducen
`E3_golpes.py` política a política (example 71 vs 71, Baseline 62 vs 61,
ryanschiller 42 vs 42, sivanlevy 9 vs 9, skourehjan 5 vs 5, scavenger 2 vs 2,
aaron 2 vs 2). Las diferencias de ±1 son los 10 diarios de más que incluyo
(`S2_humo`, `S2_P5`, `S2_P6`, `S3_humo_T`, que E3 dejaba fuera).

### Mundo LENTO · 205 partidas, 409 vidas nuestras

`asi` = asientos-partida de esa política (sus sillas × 205).
`m/asiento` = muertes nuestras por silla suya y por 100 vidas nuestras: es la
columna comparable, porque unas tienen tres sillas y otras una.

| política | sillas | asi | golpes | g/asi | muertes nuestras | **m/asiento ×100** | 1ª muerte (tic) | mediana de sus muertes | mediana de sus golpes | muertes **antes del anillo** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **relh-zero-sum** | 3 | 615 | 1.435 | 2,33 | **166** | **13,53** | 8.191 | 8.762 | 8.588 | **0 / 166** |
| **sivanlevy-zs-courier** | 2 | 410 | 852 | 2,08 | **73** | **8,92** | 798 | 2.455 | 1.335 | **53 / 73** |
| **zs-patient** | 1 | 205 | 329 | 1,60 | 27 | 6,60 | 2.018 | 9.153 | 7.742 | 9 / 27 |
| **skourehjan-…-scripted-v1** | 1 | 205 | 444 | 2,17 | 23 | 5,62 | 1.190 | 2.502 | 2.251 | **23 / 23** |
| **aaron-zs-fable** | 1 | 205 | 113 | 0,55 | 7 | 1,71 | 2.064 | 7.093 | 2.877 | 4 / 7 |
| **zero-sum-scavenger** | 3 | 615 | 112 | 0,18 | 3 | 0,24 | 8.693 | 9.484 | 11.747 | 0 / 3 |
| **belobog** | 3 | 615 | 71 | 0,12 | **0** | **0,00** | — | — | 11.528 | 0 / 0 |
| *el anillo (no es política)* | — | — | 910 | — | 61 | — | 10.753 | 12.889 | — | 0 / 61 |
| *no consta* | — | — | — | — | 43 | — | 1.009 | 9.965 | — | 5 / 43 |
| *veneno* | — | — | 26 | — | 2 | — | 12.342 | 12.783 | — | 0 / 2 |
| *nuestra pareja (fuego amigo)* | — | — | 3 | — | 0 | — | — | — | — | — |

### Mundo NORMAL · 222 partidas, 444 vidas nuestras

| política | sillas | asi | golpes | g/asi | muertes nuestras | **m/asiento ×100** | 1ª muerte | mediana de sus muertes | muertes antes del 2.000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **zero-sum-example** | 1 | 222 | 479 | 2,16 | **75** | **16,89** | 422 | 588 | **71 / 75** |
| **Zero Sum Baseline** | 1 | 222 | **3.044** | **13,71** | **72** | **16,22** | 487 | 621 | **62 / 72** |
| **ryanschiller-…-player-v1** | 1 | 222 | 332 | 1,50 | 45 | 10,14 | 455 | 981 | **42 / 45** |
| **zs-patient** | 1 | 222 | 230 | 1,04 | 31 | 6,98 | 496 | 2.239 | 13 / 31 |
| **relh-zero-sum** | 2 | 444 | 425 | 0,96 | 54 | 6,08 | 1.909 | 2.866 | **1 / 54** |
| **sivanlevy-zs-courier** | 2 | 444 | 266 | 0,60 | 27 | 3,04 | 796 | 2.725 | 9 / 27 |
| **skourehjan-…-scripted-v1** | 1 | 222 | 194 | 0,87 | 9 | 2,03 | 811 | 1.680 | 5 / 9 |
| **zero-sum-scavenger** | 2 | 444 | 142 | 0,32 | 9 | 1,01 | 727 | 3.886 | 2 / 9 |
| **belobog** | 2 | 444 | 64 | 0,14 | 4 | 0,45 | 2.652 | 7.342 | 0 / 4 |
| **aaron-zs-fable** | 1 | 222 | 73 | 0,33 | 3 | 0,68 | 1.626 | 1.768 | 2 / 3 |
| *el anillo* | — | — | 1.085 | — | 72 | — | 3.769 | 5.929 | 0 / 72 |
| *no consta* | — | — | — | — | 36 | — | 512 | 3.336 | 9 / 36 |
| *veneno* | — | — | 40 | — | 1 | — | 4.130 | 4.130 | 0 / 1 |

### Cuánto sobrevive ella (mundo lento, por la escalera de puntos)

| política | n sillas-partida | puntos mediana | puntos media | **el puesto no es mejor que** | % de sillas con 0 puntos |
|---|---:|---:|---:|---:|---:|
| relh-zero-sum | 615 | 8 | 8,81 | **4.º** | 6,5 % |
| sivanlevy-zs-courier | 410 | 6 | 7,18 | 6.º | 4,4 % |
| zero-sum-scavenger | 615 | 5 | 6,18 | 7.º | 5,4 % |
| belobog | 615 | 5 | 6,06 | 7.º | 7,3 % |
| zs-patient | 205 | 3 | 5,93 | 9.º | 12,7 % |
| aaron-zs-fable | 205 | 2 | 2,82 | 11.º | 24,9 % |
| skourehjan-…-scripted-v1 | 205 | 1 | 2,05 | 13.º | 33,2 % |
| *(nuestra criatura)* | *409* | *2* | — | *puesto mediano real **12.º*** | — |

*(«0 puntos» es exacto: implica cero bajas y puesto 15.º o 16.º.)*

---

## B.3 · De más pacífica a más peligrosa EN PARTIDA ENTERA

Orden por `m/asiento` del **mundo lento** —es el mundo en el que vamos a jugar—
con el normal al lado para ver si aguanta.

| # | política | lento `m/asiento ×100` | normal `m/asiento ×100` | ¿coinciden los dos mundos? |
|---|---|---:|---:|---|
| 1 | **belobog** | **0,00** | **0,45** | sí, la más pacífica en los dos |
| 2 | **zero-sum-scavenger** | 0,24 | 1,01 | sí |
| 3 | **aaron-zs-fable** | 1,71 | 0,68 | sí, siempre abajo (se cruzan entre sí) |
| 4 | **skourehjan-…-scripted-v1** | 5,62 | 2,03 | sí |
| 5 | **zs-patient** | 6,60 | 6,98 | **sí, clavada** |
| 6 | **sivanlevy-zs-courier** | 8,92 | 3,04 | sí, sube en el lento |
| 7 | **relh-zero-sum** | **13,53** | 6,08 | sí, la peor de las siete en los dos |
| 8 | ryanschiller-…-player-v1 | *(fuera del lento)* | 10,14 | — |
| 9 | Zero Sum Baseline | *(fuera)* | 16,22 | — |
| 10 | zero-sum-example | *(fuera)* | **16,89** | — |

**Los dos mundos ordenan igual.** Los tres de abajo (belobog, scavenger, aaron)
y los dos de arriba (sivanlevy, relh) no cambian de bando; sólo se cruzan
parejas vecinas. Es la mejor noticia de este encargo: **el orden es una
propiedad de las políticas, no del mundo.**

### Y el aviso más importante: «peligrosa entera» ≠ «peligrosa pronto»

| política | muertes en el lento | **antes del anillo (tic 7.296)** | después |
|---|---:|---:|---:|
| relh-zero-sum | 166 | **0** | 166 |
| sivanlevy-zs-courier | 73 | **53** | 20 |
| skourehjan-…-scripted-v1 | 23 | **23** | 0 |
| zs-patient | 27 | 9 | 18 |
| aaron-zs-fable | 7 | 4 | 3 |
| zero-sum-scavenger | 3 | 0 | 3 |
| belobog | 0 | 0 | 0 |

**`relh-zero-sum` no nos mata NUNCA antes del tic 8.191** —ni una vez en 205
partidas— y luego nos mata 166 veces. **`skourehjan` es lo contrario: sus 23
muertes son todas tempranas, y después ni una.** Si lo que el cuerpo necesita es
**tiempo seguro al principio** (que es la ley que midió el cinco: una forma cada
43 tics seguros), el rival a temer es `sivanlevy` o `skourehjan`, no `relh`.

### Por qué `roster_lento_v1` se equivocó, dicho sin rodeos

`roster_lento_v1` se eligió con **golpes antes del tic 2.000 en el mundo
normal**. Con ese criterio `relh-zero-sum` tenía **2 golpes y 0 muertes** y
entró **con tres sillas, como «de las más pacíficas»**. En partida entera del
mundo lento es **la que más nos mata con diferencia: 166 de 405 muertes,
el 41 %**. El criterio no estaba mal medido; estaba mirando los primeros
2.000 tics de una partida de 18.240.

---

## B.4 · `roster_lento_v2` · propuesta de 14 rivales

**Es una propuesta. No la he ejecutado, no hay fichero de petición, no se ha
jugado nada.** El borrador está en
`cantera/paper6/roster_lento_v2_PROPUESTA.json`, marcado como sin aprobar.

Nuestra pareja sigue en los asientos **10 y 11**.

| política | v1 | **v2** | `policy_version_id` | m/asiento ×100 (lento) | ¿datos para fiarse? |
|---|---:|---:|---|---:|---|
| **belobog** | 3 | **5** | `458ec0b6-fc59-4bda-aff0-68daa7f21b79` (v2) | 0,00 | **sí** · 615 sillas-partida, 0 muertes; y 444 más en el normal |
| **zero-sum-scavenger** | 3 | **5** | `6244cdeb-e044-42ff-91e3-a5c716c4338d` (v12) | 0,24 | **sí** · 615 sillas-partida, 3 muertes |
| **aaron-zs-fable** | 1 | **2** | `9457da2a-832d-45e5-b918-9209e86f9948` (v2) | 1,71 | ⚠️ **flojo** · sólo la hemos visto **en una silla**; con dos, sus dos copias se encuentran entre sí y eso no lo hemos observado nunca |
| **zs-patient** | 1 | **1** | `2b9cfd17-db50-4990-8f99-6c7c13453f61` (v3) | 6,60 | **sí** para una silla · 205 + 222 sillas-partida, y la tasa coincide en los dos mundos (6,60 y 6,98) |
| **skourehjan-…-scripted-v1** | 1 | **1** | `3e8097e1-85b8-4731-b7c1-e674f2ccbd10` (v1) | 5,62 | **sí** para una silla · pero ⚠️ **es la única temprana que queda**: sus 23 muertes son todas antes del anillo |
| **sivanlevy-zs-courier** | 2 | **0** | — | 8,92 | fuera |
| **relh-zero-sum** | 3 | **0** | — | 13,53 | fuera |
| | **14** | **14** | | | |

### Lo que predigo, para poder fallar por escrito

Sumando las tasas por silla (modelo aditivo ingenuo, ver el aviso de abajo):

| | muertes por vida nuestra atribuidas a políticas | antes del anillo |
|---|---:|---:|
| `roster_lento_v1` (observado) | **0,731** (299 de 409) | 0,218 |
| `roster_lento_v2` (predicho) | **0,169** | 0,088 |

**Aviso serio: esa resta no se va a cumplir tal cual, y sé por qué.** Esto es un
problema de riesgos en competencia: si quitas a quien nos mata, no dejamos de
morir, **morimos de otra cosa**. Ya pasó una vez: `v0 → v1` quitó el 82,5 % de
las muertes tempranas, y el hueco lo ocupó `relh`, que antes no mataba. Lo
honesto es apostar a que **en v2 el primer puesto lo hereda `sivanlevy` si se
queda, `zs-patient` si no, o directamente el anillo** (que ya nos mata 61 veces
de 405 sin ayuda de nadie).

### Dos cosas que no puedo comprobar desde aquí

1. **Que las siete políticas sigan disponibles en la liga con esas versiones.**
   Los `policy_version_id` son los de los 205 episodios del cinco; si la
   plataforma ha publicado versiones nuevas, el roster cambia de temperatura sin
   avisar. Se comprueba con una consulta de liga, coste cero, cuando digas.
2. **Cómo se comporta una política con más sillas de las que le hemos visto.**
   Vale para `belobog` y `scavenger` (3 → 5, extrapolación suave) y sobre todo
   para `aaron` (1 → 2).

### Una variante, si quieres apretar más

`belobog ×5 · scavenger ×5 · aaron ×3 · zs-patient ×1` = 14. Predice **0,129**
muertes por vida (−82 % sobre v1) y **0,051** antes del anillo, pero **deja el
mundo en cuatro políticas** y extrapola `aaron` a tres sillas sin haberla visto
nunca en más de una. Yo no la elegiría: un mundo de cuatro políticas se parece
menos a una liga y más a un laboratorio.

---

## LO QUE ME LLEVO DE AQUÍ

1. **El cinco no está en git.** Es lo más urgente de este informe y no depende
   de mí.
2. **Sólo podemos contar nuestras muertes.** Vemos morir a 1.684 rivales en el
   mundo lento y no sabemos de quién fue ni una.
3. **Los puntos son una escalera del puesto más las bajas**, exacta en 399 de
   399. Sirve para medir la supervivencia de cualquier rival sin su diario.
4. **El orden pacífica → peligrosa aguanta en los dos mundos**, que es lo que
   permite elegir un roster con alguna confianza.
5. **«Pacífica» hay que decir cuándo.** `relh` no mata antes del 8.191 y
   `skourehjan` sólo mata antes del 7.296. Elegir un roster sin decir en qué
   tramo de la partida se quiere calma es lo que hizo fallar a `v1`.

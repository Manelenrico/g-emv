# Hecho — el daño de cada arma en ZERO-SUM

Fecha: 2026-09-08 · **Solo lectura**: no se ejecutó ninguna partida ni se tocó
código. Todo sale de la documentación del mundo, del fósil del simulador y de
los diarios ya grabados de la tanda 66 (`runs/manada2/`, 80 diarios).

`md5 motor/model.py` = `1e511978c251130e95169ebf8443efa1` (sin tocar).

---

## 1 · La tabla, en una vista

Daño **base** del catálogo, y lo que ese golpe quita **con nuestro cuerpo**
(8/6/5/1, **fuerza 1**):

| arma | tipo | base | ¿escala con la fuerza? | ¿varía con la distancia? | **golpe nuestro (FUE 1)** | alcance |
|---|---|---|---|---|---|---|
| **espada** (`sword`) | cuerpo a cuerpo | **18** | **SÍ**, ×(5+FUE)/10 | **no** | **10,8** | 1 |
| **lanza** (`spear`) | **cuerpo a cuerpo** | **12** | **SÍ**, ×(5+FUE)/10 | **no** | **7,2** | 2 |
| **arco** (`bow`+`arrows`) | proyectil | **14** | **NO** | **no** | **14** | 8 |
| **cerbatana** (`blowgun`+`darts`) | proyectil | **4** + veneno | **NO** | **no** | **4** + veneno | 6 |
| *veneno del dardo* | efecto | **2 HP por pulso** | **NO** | — | **2 por pulso, cada 24 tics** | — |
| *(manos desnudas)* | cuerpo a cuerpo | 5 | SÍ | no | 3,0 | 1 |
| *(cuchillos)* (`knives`) | arrojadizo | 8 | **NO** | **no** | 8 | 5 |

**Las tres respuestas del encargo, dichas de golpe:**

1. **Solo la espada y la lanza dependen de la fuerza.** El arco, la cerbatana
   y los cuchillos dan su número exacto, siempre, lo tire quien lo tire.
2. **Ninguna arma varía con la distancia.** Una flecha a una casilla y una
   flecha a ocho quitan **14** las dos. El alcance solo decide *si* llega, no
   *cuánto* hace.
3. **La lanza es cuerpo a cuerpo aunque tenga alcance 2** — y por eso sí
   escala con la fuerza. Es el detalle que más fácil se lee al revés.

## 2 · De dónde sale cada cosa (código)

### 2.1 · El multiplicador de fuerza

`~/paintball_recon/docs/zero-sum/src/sim.nim:851`:

```nim
proc meleeMult(a: Agent): int = 5 + a.stats.strength   # x/10 (DESIGN §5.2)
```

y su única aplicación, en la rama **`ikMelee`** de `resolveMelee` (línea 922):

```nim
s.applyDamage(hit, d.damage * 100 * meleeMult(a[]) div 10, i)
```

Con **FUE 1**: `(5+1)/10 = 0,6`. **Nuestro cuerpo pega al 60 %.** Es el precio
que la campeona 8/6/5/1 paga por sus ocho de inteligencia. Coincide con el
README (línea 37): *"strength | melee damage x(5+STR)/10"*.

La lanza entra por esta rama porque su `kind` es `ikMelee`; su `range` 2 solo
alarga el bucle de sondeo (líneas 906-915), que avanza casilla a casilla hasta
`d.rng` y se para en el primer agente o en el primer muro. **El alcance mueve
dónde puedes tocar, no cuánto haces.**

### 2.2 · Los proyectiles: número fijo, sin fuerza y sin distancia

`sim.nim:949-953` y `986/990`:

```nim
proc projectileDamage(kind: ItemId): int =
  case kind
  of iArrows: def(iBow).damage
  of iDarts:  def(iBlowgun).damage
  of iKnives: def(iKnives).damage
  else: 0
...
s.applyDamage(t, projectileDamage(p.kind) * 100, p.shooter)
```

**No hay `meleeMult` ni ningún término de distancia.** El proyectil viaja 2
casillas por tic (línea 963) gastando `remaining`; cuando `remaining` llega a
cero cae al suelo como objeto recuperable. Mientras vuela, **el daño que lleva
dentro es una constante**.

Lo único que la distancia cambia es la probabilidad de que el tiro llegue: más
casillas = más tics de vuelo = más ocasiones de que el blanco se mueva. Y hay
**esquiva**: `2 × ATH` sobre 100 (línea 980); contra un cuerpo como el nuestro
(ATH 6) el 12 % de los proyectiles **atraviesan sin hacer nada**.

### 2.3 · El veneno

```nim
proc applyPoison(s: var Sim, victim, shooter: int) =
  v.poisonUntil = s.tick + 12 * (20 - v.stats.intelligence)   # sim.nim:958

proc resolvePoisonPulses(s: var Sim) =                        # sim.nim:1027-1034
  ...
    if not a.alive or a.poisonUntil <= s.tick: continue
    let dt = s.tick - a.poisonAppliedTick
    if dt > 0 and dt mod PoisonPulsePeriod == 0:
      s.applyDamage(i, PoisonPulseCenti, a.poisonFrom, "poison")
```

- **La duración la pone la inteligencia de LA VÍCTIMA**, no la del tirador:
  `12 × (20 − INT)` tics. **Contra un cuerpo como el nuestro (INT 8): 144 tics
  = 6 segundos.** Contra un INT 1: 228 tics; contra un INT 10: 120.
- **El pulso es de 2 HP y cae cada 24 tics** (un segundo). `PoisonPulsePeriod`
  y `PoisonPulseCenti` **no están en el fósil** — los certifico en el campo
  (§3.3).
- **Cuántos pulsos**: los `dt` múltiplos de 24 estrictamente menores que la
  duración. Para INT 8 → `dt` = 24, 48, 72, 96, 120 → **5 pulsos = 10 HP en
  total**. Para INT 1 → 9 pulsos = 18 HP. Para INT 10 → 4 pulsos = 8 HP.
- **Un dardo nuevo reinicia el reloj** (`poisonAppliedTick` se reescribe), así
  que envenenar dos veces no suma dos venenos: alarga uno.
- El veneno **bloquea la venda** (README línea 50) y **el kill cuenta para
  quien disparó** (línea 75).

> **Límite declarado.** El fósil `sim.nim` **no incluye la tabla `def()`** del
> catálogo: viene de un módulo ausente. Los enteros 18 / 12 / 14 / 4 / 8 / 5
> **no se leen ahí**. Se certifican por tres vías independientes: el README
> (línea 48-50), el ejemplo del catálogo en `protocol_player.md:26-28`
> (`{"id":"sword","kind":"ikMelee","damage":18,"range":1,...}`), y **el propio
> catálogo que el mundo nos mandó en la tanda 66** — nuestro `mundo_leido`
> guarda `"dmg_ref": 18`, que `mundo.py:138` define como el daño máximo de
> todas las armas del catálogo vivo. Y, sobre todo, por la medida de §3.

## 3 · La confirmación en el campo (tanda 66, 80 diarios)

El mundo publica en cada tic `damage_taken` con **fuente y cantidad exacta**
(`protocol_player.md:52`), y nuestro `damage_dealt` acumulado. Barrido de los
80 diarios de `runs/manada2/`.

### 3.1 · Golpes recibidos: la cantidad exacta, con la vida antes y después

| daño | qué es (base × (5+FUE)/10) | episodio · agente · tic | vida antes → después |
|---|---|---|---|
| **19,8** | espada de un cuerpo **FUE 6** (18 × 1,1) | `ereq_0d51e268` a10 t2192 | **92 → 72** |
| **18,0** | espada de un cuerpo **FUE 5** (18 × 1,0) | `ereq_18dfbd78` a11 t1540 | **42 → 24** |
| **14,0** | **flecha** (fija) | `ereq_c6717e24` a10 t949 | **100 → 86** |
| **13,2** | lanza de un cuerpo **FUE 6** (12 × 1,1) | `ereq_18dfbd78` a10 t636 | **67 → 53** |
| **10,8** | espada de un cuerpo **FUE 1** (18 × 0,6) | `ereq_9869b665` a11 t299 | **86 → 75** |
| **8,0** | **cuchillo** (fijo) | `ereq_0d51e268` a10 t670 | **100 → 92** |
| **7,2** | lanza de un cuerpo **FUE 1** (12 × 0,6) | `ereq_9fab619d` a10 t2207 | **100 → 92** |
| **4,0** | **dardo** (fijo) | `ereq_c6717e24` a10 t2998 | **31 → 27** |
| **2,0** | **pulso de veneno** | `ereq_c6717e24` a11 t3201 | **2 → 0** (muere) |

(la vida del diario va redondeada al entero; la cantidad exacta es la de
`damage_taken`.)

**El censo completo de cantidades recibidas en la tanda** —y esto es lo que
cierra el argumento— **no tiene ni un solo valor que no encaje**:

| cantidad | veces | lectura |
|---|---|---|
| 19,8 | 145 | espada × FUE 6 |
| 13,2 | 164 | lanza × FUE 6 |
| 12,0 | 29 | lanza × FUE 5 |
| 10,8 | 1 | espada × FUE 1 |
| 8,0 | 40 | **cuchillo, fijo** |
| 7,2 | 8 | lanza × FUE 1 |
| 5,5 / 5,0 / 4,5 / 3,0 | 91 / 2 / 19 / 24 | manos desnudas × FUE 6 / 5 / 4 / 1 |
| 18,0 | 3 | espada × FUE 5 |
| 14,0 | 4 | **flecha, fija** |
| 4,0 | 4 | **dardo, fijo** |
| 2,0 | 1 | **veneno, fijo** |

Todas las cantidades de cuerpo a cuerpo son **exactamente** `base × (5+FUE)/10`
con FUE entero, y **todas las de proyectil son exactamente la base**, sin una
sola excepción en 43 flechas, cuchillos y dardos. **Eso es, a la vez, la prueba
del escalado por fuerza y la prueba de que no hay caída por distancia.**

Del mismo barrido, el daño de zona sale `× (100 − 3×ATH)%` con nuestro ATH 6
(factor 0,82): 4→**3,28**, 6→**4,92**, 8→**6,56**, 16→**13,12**, 24→**19,68**.

### 3.2 · Golpes que repartimos nosotros (FUE 1)

Del `damage_dealt` acumulado, con el arma que teníamos en la mano:

| arma en mano | golpes medidos | delta observado | esperado con FUE 1 |
|---|---|---|---|
| **espada** | 35 | 10 (×8) y 11 (×27) | **10,8** ✔ media 10,77 |
| **lanza** | 4 | 7 (×2) y 8 (×2) | **7,2** ✔ |
| **arco** | 41 | **14** siempre | **14** ✔ |
| **cuchillos** | 34 | **8** siempre | **8** ✔ |
| **cerbatana** | 21 | **4** siempre | **4** ✔ |
| *veneno nuestro* | 44 | **2** siempre | **2** ✔ |

El acumulado va redondeado al entero, por eso la espada alterna 10 y 11: la
serie real es `0 → 10 → 21 → 32` (`ereq_292ee72d` a11, t2312/t2332/t2352), que
es **10,8 × 3 = 32,4**. Un ejemplo por arma: arco `0 → 14 → 28`
(`ereq_18dfbd78` a11, t619/t651); cerbatana `0 → 4 → 8` (`ereq_292ee72d` a10,
t2358/t2380).

### 3.3 · La cadencia del veneno, medida

De las 44 separaciones entre pulsos consecutivos, **22 son de exactamente 24
tics** — la moda absoluta, y la única separación limpia. Las demás (11, 13, 23,
1, 2 tics) aparecen cuando hay **dos envenenados a la vez** o un dardo nuevo
reinicia el reloj: `damage_dealt` **suma todas las víctimas**, así que no se
pueden separar desde nuestro diario. Una racha limpia: **7 pulsos entre t3035
y t3179 = 144 tics, 14 HP**.

**Lo que esto certifica**: `PoisonPulsePeriod` = **24 tics** y
`PoisonPulseCenti` = **2 HP**. Lo que **no** se puede certificar desde aquí es
el número de pulsos por envenenamiento, porque el acumulado mezcla víctimas y
la inteligencia del enemigo no se ve. El 5-pulsos-para-INT-8 de §2.3 es
**aritmética del código, no medida**.

## 4 · Por debajo de qué vida mata un solo golpe

La muerte es `hpCenti <= 0` (`sim.nim:1206`), así que **un golpe de D mata si
la vida es ≤ D**. Sin peros: no hay golpe de gracia ni umbral aparte.

### 4.1 · Matando nosotros (cuerpo 8/6/5/1, FUE 1)

| arma en nuestra mano | mata por debajo de |
|---|---|
| **arco** | **14 HP** |
| **espada** | **10,8 HP** |
| **cuchillo arrojadizo** | **8 HP** |
| **lanza** | **7,2 HP** |
| **cerbatana** (el dardo) | **4 HP** |
| manos desnudas | 3 HP |
| pulso de veneno | 2 HP (confirmado: `ereq_c6717e24` a11 t3201, **2 → 0**) |

**El arco es nuestra arma más letal de un solo golpe, y por bastante.** Con
fuerza 1 la espada de 18 nos rinde 10,8, por debajo de una flecha. **Para este
cuerpo, el arco pega más fuerte que la espada** — y eso, para el paper tres,
no es un detalle de tabla: es la razón mecánica de que la ánima que defiende a
su hermana a distancia no esté renunciando a nada.

### 4.2 · Matándonos a nosotros

Aquí el número depende de la fuerza **del otro**, que no vemos. El peor caso
teórico es FUE 10 (×1,5):

| arma del enemigo | mata por debajo de (peor caso FUE 10) | **peor visto en la tanda 66** |
|---|---|---|
| **espada** | **27 HP** | **19,8** (FUE 6) |
| **lanza** | **18 HP** | **13,2** (FUE 6) |
| **arco** | **14 HP** (fijo) | 14 |
| **cuchillo** | **8 HP** (fijo) | 8 |
| manos desnudas | 7,5 HP | 5,5 (FUE 6) |
| **dardo** | **4 HP** (fijo) | 4 |

**Regla práctica para el paper: por debajo de 27 de vida, cualquier espadazo
puede matarnos; por debajo de 20, en el campo real de la tanda 66, ya pasó.**
Y una ración (15 HP) no saca a nadie de esa banda: **hace falta la venda (50)
para salir del alcance de un solo golpe.**

## 5 · Lo que NO se puede afirmar

- **El número exacto del catálogo no se lee en el fósil**: `def()` falta. Los
  18/12/14/4 están triplemente respaldados (README, `protocol_player.md`,
  `dmg_ref` del catálogo vivo) y **cuadran al céntimo con 600+ golpes
  medidos**, pero la línea de código que los declara no está en el Mac.
- **El alcance de la cerbatana (6)** sale del README/catálogo, no de medida
  propia: no hemos contado casillas de vuelo de un dardo.
- **Los saltos grandes de `damage_dealt`** (32, 40, 50, 64, 80, 86, 90, 100,
  118, 126 — uno de cada) **no se han desglosado**. Son deltas de un
  acumulado que suma todas las víctimas y que puede saltarse tics sin registro;
  no se ha querido reconstruir a qué golpes corresponden. **Se declaran, no se
  interpretan.** Los ocho golpes de 8 con `hand: none` son, casi con seguridad,
  cuchillos cuya pila se agotó en el mismo tic (`sim.nim:944-945` vacía la mano
  al lanzar el último), pero tampoco se ha certificado uno a uno.
- **Nada sobre la cadencia de ataque** (cooldown) ni sobre la durabilidad: no
  se ha preguntado y no se ha medido.

---

## Rutas de las fuentes

| ruta | qué aporta |
|---|---|
| `~/paintball_recon/docs/zero-sum/README.md` (37-39, 43-53) | daño base de cada arma, `melee damage x(5+STR)/10`, duración del veneno INT-escalada, esquiva por ATH |
| `~/paintball_recon/docs/zero-sum/protocol_player.md` (26-28, 52, 118-122) | el catálogo con `damage`/`range` (ejemplo `sword`), el campo `damage_taken` con fuente y cantidad, y la regla direccional del ataque |
| `~/paintball_recon/docs/zero-sum/src/sim.nim` (851, 889-947, 949-954, 956-960, 962-992, 1027-1034, 1206) | `meleeMult`, la rama `ikMelee` con el sondeo por alcance, `projectileDamage` sin escalado, `applyPoison`, el vuelo del proyectil y la esquiva, los pulsos de veneno, la condición de muerte |
| `paintball/alma/mundo.py` (83-91, 138) | cómo leemos el catálogo vivo del mundo; `dmg_ref` = daño máximo de las armas |
| `paintball/runs/manada2/ereq_*/a1{0,1}/*.log` (80 diarios) | **la medida**: censo de `damage_taken` por fuente y cantidad, deltas de `damage_dealt` por arma en mano, cadencia de los pulsos de veneno |
| `paintball/runs/manada2/…/mundo_leido` | `"dmg_ref": 18` — el catálogo vivo de la tanda 66 confirma la espada |

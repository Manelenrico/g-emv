# Forense — LOS SIETE DONES DE VENDA RESTANTES (tanda 66)

Fecha: 2026-09-08 · **Solo lectura**: no se ejecutó nada, no se tocó código.
Todo sale del bloque `RADIOGRAFIA` de los 80 diarios de `runs/manada2/` y de la
lectura del decisor y del motor.

`md5 motor/model.py` = `1e511978c251130e95169ebf8443efa1` (sin tocar).

Complementa a `forense_dos_vendas.md`, que cubre el octavo
(`ereq_9869b665` t461).

---

## 0 · El recuento, antes de nada

Barrido de los 80 diarios buscando `RADIOGRAFIA.elegido == "soltar_*"`:

| | |
|---|---|
| sueltos de **ración** elegidos | 1373 tics |
| sueltos de **venda** elegidos | **10 tics** |
| de esos 10, **ejecutados por el mundo** | **10 / 10** (el zurrón queda a 0 y la venda aparece en el suelo) |
| **dones** según el criterio del `hecho_racion_venda` (hermana viva a **≤2 casillas**) | **8** |

Los 10 son reales; **dos caen fuera del criterio de "don"** y por eso el
recuento anterior decía ocho. Están en §4, y uno de ellos es el hallazgo más
interesante de todo este barrido.

Los **siete** de esta tabla son los ocho menos el ya publicado.

---

## 1 · La tabla

Vidas: la del que da sale de su propio `hp`; la del que recibe, del diario de la
hermana en **ese mismo tic** (no de la banda ni del parte).

| # | partida · tic · asiento | **da → recibe** (vida) | banda vista · dist | filas sociales encendidas (M) | **¿margen o desempate?** (`spread`) | ¿su cura vetada? | vendas en la orden | ¿la recogió? |
|---|---|---|---|---|---|---|---|---|
| 1 | `ereq_18dfbd78` **t376** · a10 | **94 → 56** | hurt · 2,0 | **S-DANO-PAREJA 0,198** · S-HERIDO **0** | **DESEMPATE** (`0,0`) | **SÍ** (`canal_hasta` 424) | **2 — la pila entera** | **NO** |
| 2 | `ereq_3f9b199e` **t1134** · a10 | **100 → 15** | critical · 1,41 | **S-HERIDO 0,996** · S-DANO-PAREJA 0,72 | margen (`0,17162`) | no (vida llena) | 1 | **SÍ**, t1145 a hp 15 |
| 3 | `ereq_62651a32` **t2277** · a11 | **100 → 32** | critical · 1,41 | **S-HERIDO 0,849** · S-DANO-PAREJA 0,68 · **S-PROVISION 0,30** | margen (`0,36428`) | no (vida llena) | 1 | **NO** |
| 4 | `ereq_736990b4` **t2326** · a10 | **1 → 16** | critical · 1,41 | **S-HERIDO 1,542** · S-DANO-PAREJA 0,84 · F-DANO **1,377** | **margen mayor** (`0,65891`) | **SÍ** (`canal_hasta` 2353) | 1 | **NO** |
| 5 | `ereq_9fab619d` **t2333** · a10 | **100 → 20** | critical · 2,0 | **S-HERIDO 0,782** · S-DANO-PAREJA 0,66 | margen **estrecho** (`0,0185`) | no (vida llena) | 1 | **SÍ**, t2410 a hp 7 |
| 6 | `ereq_a62f7c2d` **t627** · a11 | **100 → 23** | critical · 1,0 | **S-HERIDO 1,204** · S-DANO-PAREJA 0,642 | margen (`0,33114`) | no (vida llena) | 1 | **SÍ**, t2433 a hp 23 |
| 7 | `ereq_b915417a` **t1705** · a10 | **100 → 7** | critical · 2,0 | **S-HERIDO 1,342** · S-DANO-PAREJA 0,80 | margen (`0,40903`) | no (vida llena) | 1 | **NO** (ya llevaba una) |

**Qué abrió el candidato: en los siete, la misma puerta.** La rama
`_herida59` de `candidatos()` 6b (`decisor_zs.py:511-513`), que es la del
**PROMPT_12** y mira la **banda visible** de la hermana:

```python
_herida59 = pareja is not None and \
    (pareja.get("hp_band") or "healthy") != "healthy"
```

**S-PROVISION no abrió ninguno de los siete.** Aparece como fila que *pesa* en
uno solo (el #3, con M 0,30), pero la puerta la abrió la banda. La rama de
provisión-en-calma sí abrió un don, y es uno de los dos excluidos: §4.

---

## 2 · Lo que la tabla dice, mirado de cerca

### 2.1 · El margen es la norma, no la excepción

**Seis de los siete ganaron por margen real** (`spread` de 0,0185 a 0,659), y
solo uno por el desempate de paisaje degenerado. Contando el octavo (`t461`,
también desempate): **de los ocho dones de venda, seis por margen y dos por
desempate.**

Esto **corrige la impresión** que dejaba el forense de la escena de las dos
vendas. Aquel don fue el más débil de los ocho; **no es el representativo**. En
la mayoría, dejar la medicina junto a la hermana **valía estrictamente más** que
quedarse quieto, y el planificador no tuvo que romper ningún empate.

### 2.2 · Los dos desempates son exactamente los dos donde S-HERIDO calla

| caso | hp del parte | S-HERIDO | resultado |
|---|---|---|---|
| #1 `18dfbd78` t376 | **67** | **0** | **empate** (`spread` 0,0) |
| `9869b665` t461 (el otro forense) | **67** | **0** | **empate** (`spread` 0,0) |
| #4 `736990b4` | 16 | 1,542 | margen 0,659 |
| #7 `b915417a` | 20 | 1,342 | margen 0,409 |
| #6 `a62f7c2d` | 23 | 1,204 | margen 0,331 |
| #2 `3f9b199e` | 28 | 0,996 | margen 0,172 |
| #3 `62651a32` | 32 | 0,849 | margen 0,364 |
| #5 `9fab619d` | 34 | 0,782 | margen 0,019 |

**S-HERIDO corre sobre el parte, no sobre la banda.** Con el parte diciendo
`hp 67` está muda; con el parte entre 16 y 34 vale entre 0,78 y 1,54. Y cuando
está muda, lo único que empuja es S-DANO-PAREJA (≈0,2), que **no basta para
crear margen**: sale empate y decide la regla de la casa.

De ahí la frase que el paper puede sostener: **el que da con margen es el que
sabe un número; el que da en empate es el que solo ha visto un color.** La
banda abre la puerta; el parte es lo que le da peso al gesto.

### 2.3 · Curarse casi nunca estuvo compitiendo

En **ninguno de los siete** fue `usar_botiquin` un candidato vivo, por dos
motivos distintos:

- **Cinco de siete daban con la vida llena (hp 100).** La regla 6 del decisor
  (`if hp < hp_max`) ni crea el candidato: no había nada que curar. **Dar no le
  costaba salud a nadie en ese instante** — le costaba el objeto.
- **Dos estaban vetados por su propio reloj**, el mismo mecanismo del forense
  anterior (`Bloqueos.canal_hasta`, que arranca al emitir `use` y **no se entera
  de las cancelaciones**):
  - **#1** `18dfbd78` t376: emitió `use` en t375, el mundo confirmó `ok` en
    t376 → `canal_hasta` = **424**. Un tic después de pedir la cura, la regaló.
  - **#4** `736990b4` t2326: **tercer intento consecutivo** de curarse
    (`use` en t2207, t2256 y t2305, cada uno +48) → `canal_hasta` = **2353**.

**El único caso de toda la tanda donde curarse y dar compitieron de verdad** es
uno de los excluidos (§4.1): allí `usar_botiquin` valía **3,94821**, `noop`
**3,79725** y `soltar_first_aid` **3,78864**. **Ganó dar, por margen, con la
cura en la mesa.** Es el dato que faltaba.

### 2.4 · La escena del #4, que es la más dura

`ereq_736990b4` t2326: la 10 está a **1 punto de vida**. Ha pedido la venda tres
veces seguidas y las tres se la han cortado. Su F-DANO vale 1,377 —el dolor
propio casi al máximo— y aun así **S-HERIDO 1,542 lo supera**: la hermana, a
16 y en crítico a una casilla, pesa más que su propia agonía. Suelta su única
venda con el margen más grande de las siete (0,659) y **muere 39 tics después**.
La hermana no llegó a cogerla: su diario acaba en t2345, con la venda todavía en
`[23,19]`.

### 2.5 · La pila: una de siete

Solo el **#1** soltó **dos vendas en una orden** (ranura con `n=2`); las otras
seis soltaron una unidad. Con el octavo (`t461`, también pila de 2), son **dos
de ocho**. En los dos casos la ánima **había previsto dar una** —`_pack_sin`
descuenta uno, no vacía la ranura— y el mundo dio la ranura entera. El desajuste
está declarado en el forense anterior; aquí se confirma que **no es un caso
aislado, es lo que pasa siempre que la ranura lleva más de una**.

### 2.6 · Recogidas: tres de siete

| recogidas | detalle |
|---|---|
| **SÍ (3)** | #2 a los **11 tics** (hp 15) · #5 a los **77 tics** (hp 7) · #6 a los **1806 tics** (hp 23) |
| **NO (4)** | #1 (la venda sigue en el suelo hasta t402) · #3 (hasta t3116, la hermana muere a hp 8 en t2996) · #4 (la que da muere 39 tics después) · #7 (**la hermana ya llevaba una venda**, nunca cogió la segunda) |

Contando el octavo, **tres de ocho dones llegaron a manos de la hermana**. Y en
los tres, **la recogió estando peor que cuando se la dieron**: 15, 7 y 23 de
vida. **El gesto se adelanta al momento en que hace falta** — cuando la hermana
vuelve a por él, ya está en el suelo esperándola.

---

## 3 · Lectura en llano

Los siete dones se parecen mucho más entre sí de lo que sugería la escena de las
dos vendas.

El patrón dominante es este: **una hermana en crítico a una o dos casillas, y
una ánima con la vida llena que suelta la venda con margen claro**. Cinco de las
siete son así. No hay dilema, no hay sacrificio de salud: hay una fila —
S-HERIDO, alimentada por un parte reciente que dice un número bajo — que pesa
más que quedarse con el objeto, y el gesto sale sin necesidad de que nadie rompa
un empate.

Lo interesante empieza en los bordes. En un extremo está el **#4**, que da a un
punto de vida, con el dolor propio casi saturado, porque la hermana pesa aún
más — y muere sin que nadie recoja nada. En el otro está el **#1**, que da un
tic después de haber pedido la cura para sí misma, con el parte tan viejo que
S-HERIDO no se entera de nada, en empate, y regalando la pila entera cuando
creía dar una sola venda. Entre esos dos cabe todo lo que hay que contar del
gesto.

Y hay una asimetría que conviene decir sin adornos: **el gesto es mucho mejor
dando que recibiendo**. Ocho vendas salieron del zurrón; tres llegaron a la
hermana. Las otras cinco se quedaron en el suelo mientras las dos morían, o
sobraban porque ella ya llevaba una. La ánima **da bien y coordina mal**: nadie
le dice a la hermana que la medicina está ahí, porque el parte lleva lo que uno
tiene, no lo que uno ha dejado en el suelo. Si hay una mejora obvia para una
temporada siguiente, está exactamente ahí, y **no es una fila nueva: es un campo
más en el parte.**

Sobre lo que este forense **no** demuestra: que dar venza a curarse. En siete de
siete, curarse no estaba en la mesa —cinco por vida llena, dos por el veto—.
Solo hay **un** caso en toda la tanda donde compitieron, y está fuera de los
ocho (§4.1). Un dato es un dato, no una serie.

---

## 4 · Los dos sueltos de venda que quedan fuera del criterio (declarados)

Ejecutados igual que los otros ocho, pero no cuentan como "don" bajo la
definición del `hecho_racion_venda` (hermana viva a ≤2 casillas).

### 4.1 · `ereq_0d51e268` t803 · a10 — **el único que abrió S-PROVISION**

- **`ve_agentes: []`** — **no veía a nadie**, ni a su hermana. `pareja_vista`
  false, `dist_pareja` null.
- Con la hermana invisible, `_herida59` es **False**: la puerta la abrió la otra
  rama, **`_prov59`** (PROMPT_59/61, provisión en calma), que no necesita verla
  — le basta con el **parte**: `hp 44,0`, **`botiquin: 0`**, 34 tics de edad, y
  `PROVISION_B_MIN = 1` contra la venda que llevaba.
- Filas: **S-PROVISION 0,30** · S-HERIDO 0,48 · S-DANO-PAREJA 0,526.
- **Candidatos**: `noop` 3,79725 · **`usar_botiquin` 3,94821** ·
  **`soltar_first_aid` 3,78864** → **margen 0,15957**.
- **Nadie la recogió**: la venda seguía en `[19,22]` en t1462.

**Esto es un dato que el paper necesita**: la ánima dejó su única venda en el
suelo **para una hermana que no podía ver**, guiándose por un parte de hace
treinta y cuatro tics que decía que estaba a 44 y sin vendas — y lo hizo
**teniendo la opción de curarse a sí misma delante y descartándola por margen**.
Es el don más "de fe" de la tanda y el único que S-PROVISION produjo con venda.

### 4.2 · `ereq_62651a32` t420 · a11 — a 6,4 casillas

- Da a **hp 72** con la hermana a **hp 56** (banda hurt) pero a **6,403
  casillas**: fuera del radio de 2.
- Abrió `_herida59` (la veía, y herida). Filas: S-DANO-PAREJA 0,191 · S-HERIDO
  **0** (parte `hp 72`).
- **`spread` 0,0 → desempate.** Y **cura vetada** (`canal_hasta` 468).
- **Pila de 2** en la orden. **Nadie la recogió** (seguía en `[26,26]` en t2101).

Encaja exactamente en el patrón de §2.2: parte alto → S-HERIDO muda → empate.
Si el criterio de "don" fuese "hermana herida a la vista" en vez de "≤2
casillas", este contaría y los dones de venda serían nueve.

---

## 5 · Lo que NO se puede afirmar

- **No se ha comprobado quién se llevó las cuatro vendas no recogidas.** Solo se
  sabe hasta cuándo se vieron en el suelo desde nuestros dos diarios. Pudo
  cogerlas un enemigo, o pudieron quedarse ahí: **no hay dato**.
- **La reconstrucción del veto** (`canal_hasta`) replica `Bloqueos` desde el
  diario asumiendo `use_ticks` = **48** para la venda y **24** para la ración.
  El 48 está certificado (README: canal de 2 s a 24 tps); el 24 de la ración es
  el medido en `hecho_dano_armas.md`, no leído del catálogo. En los siete casos
  el veto se decide por vendas, así que el 24 no afecta.
- **No se ha reconstruido cuánto habría valido `usar_botiquin`** en los dos
  vetados: el candidato no se creó y no hay número. Saberlo exige **correr**.
- **`spread` va redondeado a 5 decimales** en el registro. Los dos "0,0" son
  empates dentro de esa precisión; la rama que se ejecutó (paisaje degenerado,
  `spread ≤ 1e-3`) no depende de la sexta cifra.
- **Los 1373 sueltos de ración no se han analizado.** El recuento de 90 dones de
  ración del `hecho_racion_venda` usa el criterio de los ≤2; la diferencia entre
  1373 tics elegidos y 90 dones **no se ha desglosado aquí**.

---

## Rutas de las fuentes

| ruta | qué aporta |
|---|---|
| `paintball/runs/manada2/ereq_*/a1{0,1}/*.log` (80 diarios) | **todo el barrido**: `RADIOGRAFIA` con `elegido`, `candidatos`, `spread`, la tabla de filas y el `parte`; el zurrón antes/después; `ve_items` para la venda en el suelo; la vida de la hermana tic a tic |
| `paintball/alma/decisor_zs.py` (55-103) | `Bloqueos`: el veto de `usar_*` por `canal_hasta` y que no se entera de las cancelaciones |
| `paintball/alma/decisor_zs.py` (484-513) | la regla 6 (`hp < hp_max`) y las **dos ramas** que abren `soltar`: `_herida59` (banda) y `_prov59` (provisión en calma) |
| `paintball/alma/decisor_zs.py` (363-371) | `_pack_sin`: la foto prevé dar **una** unidad, no la ranura |
| `paintball/alma/appraisal_zs.py` (199-208) | `PROVISION_ON = True`, **`PROVISION_B_MIN = 1`** |
| `planificador/planificador_v1.py` (446-464) | el paisaje degenerado y `exclude_noop`: en empate exacto, actuar gana |
| `paintball/forense_dos_vendas.md` | el octavo don, en detalle |
| `paintball/hecho_racion_venda.md` | el criterio de "don" (≤2 casillas) y el recuento 98 → 8 vendas / 90 raciones |

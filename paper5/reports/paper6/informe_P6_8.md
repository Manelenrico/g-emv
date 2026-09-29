# P6-8 · Dos arreglos de método y una serie corta

*27-sep-2026. `motor/model.py` intacto (`1e511978c251130e95169ebf8443efa1`), los
202 archivos de `CONGELADO.md` sin alterar, todo lo del seis en archivos nuevos.
Nada subido a git, nada empujado, nada borrado.*

---

# A · EL CINCO YA TENÍA LAS DOS COSAS

*Coste cero. Solo contar. Mismos medidores que P6-7 (`mide_lleno_P6_7.py`,
`mide_golpes_P6_7.py`) sobre las 379 vidas del cinco (0.1.18).*

## A.1 · Intentando coger con la mochila llena

| serie | vidas | tics | `coger` + `inventory_full` | % | con piernas listas | rachas ≥ 24 | vidas afectadas | peor racha |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| P5-6C | 200 | 1.501.210 | 18.870 | 1,26 % | 11.829 | 36 | 85 | **5.348** tics (60,8 % de esa vida) |
| P5-7C | 80 | 698.867 | 11.311 | 1,62 % | 2.258 | 14 | 40 | 661 (7,1 %) |
| P5-8I | 20 | 154.601 | 3.974 | 2,57 % | 3.139 | 1 | 9 | 3.146 (39,3 %) |
| P5-8M | 79 | 641.110 | 13.089 | 2,04 % | 7.704 | 11 | 48 | **5.593** (44,0 %) |
| **el cinco** | **379** | **2.995.788** | **47.244** | **1,58 %** | **24.930** | **62** | **182 de 379 (48,0 %)** | 5.593, `P58M_t3_K_21622393` s10, tics 2.520-8.112 |

Casi la mitad de las vidas del cinco pasaron por ello; 34 vidas más de 240 tics
seguidos. Las peores rachas del cinco son **más largas que la peor de P6-6**
(3.676): 5.593 y 5.348 tics, el 44 % y el 61 % de una vida, ambas acabando en
muerte. Y en 24.930 de esos 47.244 tics el cuerpo tenía las piernas listas.

**La causa está en el decisor, no en la mochila:** `_pack_con` ya sabe que con
el zurrón lleno «coger no cambia nada» (`decisor_zs.py:384`), así que la
previsión de `coger` es idéntica a la de `noop` — y el desempate del cinco
excluye a `noop` (`select_tiebreak(..., exclude_noop=True)`, `:896`). En un
empate, `coger` gana siempre. El cuerpo sabe que no cabe y lo intenta igual.

## A.2 · Golpes y muertes de rivales visibles con la mano vacía

| serie | golpes de rival con arma en mano | **con `hand: none`** | no visto | anillo | muertes por rival con arma | **por rival con `hand: none`** | anillo | no consta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P5-6C | 1.290 | **411** | 1 | 395 | 136 | **11** | 26 | 23 |
| P5-7C | 476 | **124** | 0 | 224 | 49 | **7** | 14 | 7 |
| P5-8I | 132 | 8 | 0 | 33 | 13 | 0 | 1 | 4 |
| P5-8M | 498 | **162** | 0 | 236 | 44 | **12** | 13 | 9 |
| **el cinco** | **2.396** | **705 (22,7 % de los golpes de rival)** | **1** | 888 | **242** | **30 (11,0 % de las muertes por rival)** | 54 | 43 |

**Uno de cada cinco golpes de rival, y una de cada nueve muertes por rival, en
todo el cinco, vienen de un rival visible con la mano vacía** — para el que la
tabla no tiene fila («sin arma no hay amenaza», `appraisal:1591`). Y **un solo
golpe de un rival no visto en 2.995.788 tics**, como en P6-4 y P6-6: el peligro
a ciegas no existe en este mundo. El diario no dice con qué pegan esos rivales;
dice que pegan.

---

# B · LOS DOS ARREGLOS (brazo A2 = A1 de P6-6 + esto)

`cantera/paper6/arreglos_P6_8.py`, desde fuera, envolviendo `D.candidatos` una
vez más, después de `arreglos_P6_6` (oído y don). **Ni una fila nueva.**

## B.1 · `ir_pareja` apunta al parte cuando no ve al hermano

`mem.pareja_pos` solo se escribe al VER al hermano (`appraisal:624`), y
`ir_pareja` apunta ahí (`decisor:471`). Medido en P6-7: con el hermano fuera de
la vista (31,1 % de los tics de A1) ese destino está a > 3 casillas de donde el
parte dice que está el **41,6 %** de las veces (p90 13, máx. 31). Regla: si el
hermano no está en `visible.agents` y `mem.parte_fresco(tick)` da posición,
`ir_pareja` apunta a ella; si no había `ir_pareja`, se crea con la receta del
decisor (`{"tipo": "ir", "destino", "cuerpos"}`). Si lo ve, no se toca nada. Si
el hermano ha muerto o el parte no es fresco, nada.

## B.2 · No propone `coger` con la mochila llena

Leído del mundo y de nada más: se esconde `coger` si (a) la previsión del
propio decisor no cambia la mochila (`D._pack_con(pack, id, n, mundo) == pack`,
con `pack` tal cual lo manda el mundo, con sus huecos y sus pilas), o (b) el
último `action_result` fue `inventory_full` y sigo en la misma casilla con el
mismo objeto debajo. Ninguna capacidad cableada.

*(Efecto lateral, declarado: `coger` de una prenda con el cuerpo vacío la
tabla del cinco también lo modela solo como mochila (`decide`, rama `coger`), así
que con la mochila llena tampoco se propondrá vestirla desde `coger`; antes solo
podía ganar por el empate contra `noop`, no por valor.)*

## B.3 · Los humos, con diarios reales de P6-6 donde pasaban las dos cosas

`humo_P6_8.py` — **5 de 5**. Replay tic a tic por la vía real: obs del diario con
su chat E2 real → gemelo E1 (`oido5`) → `Memoria.observa` → `D.candidatos` /
`D.decide` con su `Bloqueos`. Ni un campo de memoria a mano.

| humo | dónde | resultado |
|---|---|---|
| **a** | la mochila llena real: `20889290` s10, tics 5.500-5.700 (donde eligió `coger` 3.676 tics) | **141 tics con `inventory_full`: sin arreglo `coger` elegido 141; con arreglo 0, y ni siquiera candidato** |
| **b** | el destino de `ir_pareja` real: `21517664` s10, excursión 570-7.996 | **601 tics** sin ver al hermano con parte fresco: destino = parte en los 601; distinto del de antes en 55 |
| c | con el hermano a la vista | 34 tics, `ir_pareja` idéntico |
| d | los dos interruptores a 0 | 61 tics, candidatos idénticos al cinco |
| e | sin parte fresco / hermano muerto | no inventa `ir_pareja` |

`humo_red_P6_8.py` (molde del de P6-6, con los cuatro arreglos): 200 de 200
acciones, 0 errores, 8 partes E2 del emisor de producción por el cable,
`mem.parte` puesto. Corre dentro del build de `Dockerfile.pareja8`, con la
custodia md5 de `arreglos_P6_8.py` y `policy_pareja8.py`. Build limpio.

---

# C · LA SERIE: A2 EN LAS 20 SEMILLAS DE P6-6

**Coste: 1,4450 USD** de los 3 (20 partidas, todas con coste facturado; 40
diarios). Política `gemv-p6-A2-cuatro:v1` (`45c2d5c0…`), imagen
`gemv-anima:pareja8`, `GEMV_OJOS=1`. **Control: los A0 y A1 de P6-6, ya
jugados y no repetidos.** Comparten con A2 el mundo, la liga, el roster, las 20
semillas y el cuerpo (A2 = A1 + `arreglos_P6_8`); no comparten el día ni el
estado de la plataforma, así que la comparación es la de una tercera tirada
sobre el mismo punto de partida, no la de tres brazos de una misma serie.

## C.0 · Antes de nada: un fallo de método mío, cazado al leer los diarios

La versión jugada de `arreglos_P6_8.py` **creaba `ir_pareja` también en los tics
de enfriamiento de las piernas**, cuando el decisor lo había vetado
(`Bloqueos.veta`, `decisor:95-102`). En esos tics `ir_pareja` era el único
candidato aparte de `noop`, ganaba, y emitía un `move` que el mundo rechazaba
con `cooldown` (6.333 creaciones en un solo diario). **Para el movimiento es
inocuo** —no podía moverse—, pero **infla cualquier cuenta de «`ir_pareja`
elegido»** que no separe los tics con piernas listas. Todas las cifras de
`ir_pareja` de abajo están contadas **solo con piernas listas**. La versión
corregida es `arreglos_P6_8b.py` (solo crea con `move_ready_in == 0`), con su
humo `humo_P6_8b.py` **6 de 6** (el sexto: en 599 tics de enfriamiento reales,
`ir_pareja` creado 0 veces). **No se ha jugado con ella.**

## C.1 · El sello, predicción a predicción

| # | sellado | salió | veredicto |
|---|---|---|---|
| 1 | `coger` + `inventory_full` ≤ 40 tics | **0** (A1: 18.566) | **acierta** — el bucle de la mochila desaparece del todo |
| 2 | `ir_pareja` elegido ≥ 2 % (piernas listas, hermano fuera de vista) | **912 de 46.129 = 1,98 %** (A1 0,75 %; A0 6,1 %) | **FALLA** por dos centésimas. Y en las escapadas largas, con piernas listas: **56 de 10.660** (0,5 %) |
| 3 | a ≤ 3 casillas ≥ 66 % · a > 15 ≤ 4 % | **48,64 % · 4,06 %** (A1 59,85 / 7,59; A0 79,13 / 0,00) | **FALLA las dos**. A ≤ 3 casillas, **peor que A1** (A2 menor en 13/20 semillas, −4,5 p.p., p = 0,263); contra A0, menor en 19/20 (p = 0,000) |
| 4 | escapadas ≥ 200 tics ≤ 10 | **30** (45.483 tics; la más larga 7.028) | **FALLA** (A1 19, A0 3) |
| 5 | vida media ≥ 11.436 | **11.235,2** | **FALLA**: +299 sobre A1 (emparejado −363,8, A2 mayor en 9/20, p = 0,824); contra A0 **−1.504,8, mayor en 5/20, p = 0,041** |
| 6 | distancia al hermano al morir ≤ 6 (rival y anillo, con el hermano vivo) | rival **5,5** (n = 10) · anillo **5,0** (n = 10) | **acierta** (A1: 9,5 y 10; A0: 1 y 2,5) |
| 7 | S-8 sigue pesando en la vuelta: mediana > +0,05, positiva > 50 % | mediana **+0,0000**, positiva **49,1 %** (6.516 tics de detalle) | **FALLA** tal como la escribí. Pero partida por si hay rival contado: **con contado +0,1175 (n = 4.467)**, sin contado −0,0736 (n = 2.049) |
| 8 | recogida del don entre 10 % y 40 % | **27,78 %** (10 de 36) | acierta |
| 9 | coste ≤ 1,5 | **1,4450** | acierta |

**4 aciertos, 5 fallos.** Los dos arreglos hacen exactamente lo que decían —la
mochila llena se va a cero y `ir_pareja` apunta bien— y **la pareja no se
junta más, sino menos**.

## C.2 · Lo que pedías medir, A0 / A1 / A2

| medida | A0 | A1 | **A2** |
|---|---:|---:|---:|
| tics clavados con la mochila llena | 6.254 (1,31 %) | 18.566 (4,44 %) | **0** |
| `ir_pareja` elegido, piernas listas, hermano fuera de vista | 729 / 11.939 (6,1 %) | 405 / 54.244 (0,75 %) | **912 / 46.129 (1,98 %)** |
| …en las escapadas largas | — | 18 tics de 34.606 (todos) | **56 / 10.660** (piernas listas) |
| hermano vivo y fuera de la vista | 67.525 (14,1 %) | 130.204 (31,1 %) | **155.995 (36,3 %)** |
| distancia: a ≤ 3 / ≤ 8 / > 15 casillas | 79,1 / 96,9 / 0,0 % | 59,9 / 77,7 / 7,6 % | **48,6 / 77,2 / 4,1 %** |
| escapadas > 8 casillas · de ≥ 200 tics | 481 · 3 | 225 · 19 | **466 · 30** |
| …se aleja el asiento 10 | 453 | 169 | **400** |
| vida media de la pareja | 12.427,9 | 10.936,2 | **11.235,2** |
| mueren / sobreviven | 32 / 8 | 33 / 7 | **37 / 3** |
| …anillo · rival · no consta | 20 · 11 · 1 | 23 · 7 · 3 | **19 · 14 · 4** |
| muerte por rival: tic mediana · dist. al hermano | 10.859 · 1 | 2.701 · 9,5 | **9.927 · 5,5** |
| muerte por anillo con el hermano vivo: dist. | 2,5 | 10 | **5,0** |
| los dos vivos al cierre | 18/20 | 15/20 | **18/20** (vs A1 p = 0,407) |
| sobrevive el otro tras el primero (mediana) | 912 | 1.740 | **1.017** |
| golpes: anillo · rival con arma · **`hand: none`** · no visto | 380 · 155 · 103 · 0 | 553 · 135 · 66 · 0 | **561 · 185 · 70 · 0** |
| \|disc\| S-8 por decisión | 0,0585 | 0,0249 | **0,0449** |
| don: efectivos · recogidos · usados · viajan en E2 | 66 · 17 · 16 · 0 | 35 · 7 · 7 · 33 | **36 · 10 · 9 · 34** |
| F-HERMANO-AMENAZA: tics · solo por contado | 29.085 · 0 | 82.704 · 38.256 | **63.948 · 24.555** |

## C.3 · S-8 de los rivales contados en el camino de vuelta (`mide_vuelta2_P6_8.py`)

Sobre **todos** los tics con el hermano vivo, fuera de la vista y parte fresco,
en los que hay detalle de candidatos e `ir_pareja` es candidato:

| | A0 | A1 | **A2** |
|---|---:|---:|---:|
| tics de detalle | 477 | 2.302 | **6.516** |
| d(ir_pareja) − d(noop), mediana · `noop` mejor | +0,022 · 59,1 % | +0,165 · 90,6 % | **+0,028 · 59,7 %** |
| **S-8: M(ir_pareja) − M(noop)**, mediana · positiva | +0,000 · 47,0 % | **+0,160 · 82,5 %** | **+0,000 · 49,1 %** |
| …**con rival contado** en la percepción | — (n = 0) | +0,160 (n = 1.600) | **+0,118 (n = 4.467)** |
| …sin rival contado | 0,0 (n = 477) | +0,198 (n = 702) | **−0,074 (n = 2.049)** |

**Con el destino correcto, la exposición del camino de vuelta deja de pesar en
neto** (mediana 0, como en A0): el +0,16 de A1 era en buena parte el camino a
una casilla **equivocada** (en A1 pesaba igual sin contados, +0,198). Lo que
queda es limpio y es lo que pedías: **cuando hay un rival contado en la
percepción, volver sigue costando +0,118 de S-8** (n = 4.467, el 69 % de esos
tics), y sin él volver *ahorra* exposición (−0,074). Los contados siguen
haciendo del hermano un sitio peligroso; ya no es la única razón.

## C.4 · Por qué no se juntan, visto tic a tic

La escapada más larga de A2 (`22146038`, asiento 10, tics 1.791-7.468, 5.677
tics): el hermano quieto en (23,35)/(24,34), el 10 a **13 casillas**, con el
parte exacto (error mediano 0, máximo 3), la geodesia al hermano calculada y
alcanzable (campo con valor 14 en su casilla, paso previsto hacia él), **y el
cuerpo yendo y viniendo entre (24,21) y (25,22) durante 5.000 tics**. Con las
piernas listas:

```
3012  (25,22)  gana move_NW    d 3,325   (ir_pareja 3,387)
3023  (24,21)  gana ir_objeto  d 3,294   (ir_pareja 3,387)
3034  (25,22)  gana move_NW    d 3,325
```

`ir_pareja` **ya apunta bien y pierde por valor**: apartarse de los rivales
visibles (1, 3 y 5) y el objeto de al lado valen más que el hermano a 13
casillas; y las dos opciones se turnan casilla arriba, casilla abajo. En las 30
escapadas largas, con piernas listas: `noop` 8.573, `move_*` 984, `ir_objeto`
657, `ir_botin` 272, `ir_centro` 73, **`ir_pareja` 56**. El destino era una
condición necesaria; no era la razón.

*(Medí también el «baile» entre dos casillas en todos los brazos, y la
definición —≥ 6 movimientos que solo pisan dos casillas— no distingue la
oscilación de la espera normal junto a un sitio: da el 48 % de los tics en A0, el
36 % en A1, el 42 % en A2 y el 45 % en el cinco. No sirve como medida de
patología y no la uso; queda en `P6_8_baile.json`.)*

## C.5 · Lo que sí cambió

* **El bucle de la mochila: de 18.566 tics a 0.** Sin efecto lateral visible en
  el resto (el don, la recogida, los golpes con arma se mantienen).
* **Mueren más cerca del hermano** (5,5 y 5,0 contra 9,5 y 10) y las muertes por
  rival vuelven a ser tardías (mediana 9.927 contra 2.701), aunque son más
  (14 contra 7; A0 tenía 11).
* **Los dos vivos al cierre: 18/20**, como A0 (A1: 15/20).
* **Pero la vida no vuelve**: 11.235 contra los 12.428 de A0 (p = 0,041 en
  contra), y los 3 supervivientes de 40 son los menos de las tres series. Con el
  bucle de la mochila **el cuerpo se quedaba quieto en sitio seguro durante el
  cierre del anillo**; suelto, se mueve, y muere igual o antes. Lo dejé escrito
  en el sello (predicción 5) y ha pasado.

---

# LO QUE ME LLEVO

1. **El cinco ya tenía las dos cosas:** 47.244 tics con la mochila llena en 182
   de 379 vidas (peor racha 5.593, el 44 % de una vida), y **705 golpes y 30
   muertes** de rivales visibles con la mano vacía. Y un solo golpe a ciegas en
   tres millones de tics.
2. **La mochila llena era un empate mal resuelto**: el decisor sabe que no cabe
   (`_pack_con`) y `coger` gana a `noop` porque el desempate excluye a `noop`.
   Esconderlo lo deja en cero.
3. **El destino de `ir_pareja` era necesario y no suficiente**: bien apuntado,
   pierde por valor contra apartarse y saquear, y la pareja se separa más (a ≤ 3
   casillas, 48,6 %). La exposición de los contados sigue pesando +0,118 cuando
   están; sin ellos, volver ya no cuesta.
4. **Mi envoltorio creaba `ir_pareja` en enfriamiento**: inocuo para el
   movimiento, tramposo para la estadística. Corregido en `arreglos_P6_8b.py`,
   no jugado.
5. **Cuatro aciertos y cinco fallos en el sello**, y los cinco fallos dicen lo
   mismo: quitar lo que clavaba al cuerpo no lo acerca a su hermano.

*No propongo arreglos: los datos dicen que el siguiente no es de método sino de
valor —cuánto vale estar junto al hermano frente a apartarse y saquear—, y eso
es de Manel y de la tabla.*

# LOS ARCHIVOS NUEVOS, CON SU MD5

| archivo | md5 |
|---|---|
| `cantera/paper6/P6_8_baile.json` | `ed502628d8f59d614af96b4722d396ba` |
| `cantera/paper6/P6_8_brazos.json` | `0464a45cfb5e4bba383efcb05f9238d7` |
| `cantera/paper6/P6_8_don.json` | `2b90719321d032bff8605c1f77625387` |
| `cantera/paper6/P6_8_golpes.json` | `7c36eaca11de85bf5e3e7b2e17c214d2` |
| `cantera/paper6/P6_8_golpes_cinco.json` | `40350c0abf87d5d880598b34d99e7b6a` |
| `cantera/paper6/P6_8_largas_A2.json` | `d7a6d78ad6941a71dd0fdf6d8c57b5dd` |
| `cantera/paper6/P6_8_lleno.json` | `ddc668bcb6b62585e59c3faa27ef275c` |
| `cantera/paper6/P6_8_lleno_cinco.json` | `775d4ccc6a513e213c76238e5031be3d` |
| `cantera/paper6/P6_8_medidas.json` | `3c71332b6c0b1bb1fbb2b2bf3397c307` |
| `cantera/paper6/P6_8_p67.json` | `66b2d631cf9d0f7588adec32e7b143af` |
| `cantera/paper6/P6_8_pareja.json` | `78b36a9989d15fdae5a643adb0c1eb6f` |
| `cantera/paper6/P6_8_separa.json` | `9d6038eb4933f312676ce2741d98fe7b` |
| `cantera/paper6/P6_8_vuelta2.json` | `a49708f5fae40b027dfb6688001c9318` |
| `cantera/paper6/SELLO_P6_8.md` | `9d35884e89cf141397adeed64d2b7e59` |
| `cantera/paper6/arreglos_P6_8.py` | `f66355ca12b58b075d12f0e7f7ee39d0` |
| `cantera/paper6/arreglos_P6_8b.py` | `5028b54d4afd8c7c82bc8e5e3a94a01e` |
| `cantera/paper6/humo_P6_8.py` | `952328552b9cbb0eed000ab492e39b95` |
| `cantera/paper6/humo_P6_8b.py` | `9efcb3d8fe68eaa6fe6edaef7fac5262` |
| `cantera/paper6/humo_red_P6_8.py` | `797a33eb76a76b84f0c8d3364499517c` |
| `cantera/paper6/lanza_P6_8.py` | `b22ef1bf77cdfe2f0ade6f5b46d29cd0` |
| `cantera/paper6/mide_P6_8.py` | `31d116836bb7a3f3292a074e7b4b4900` |
| `cantera/paper6/mide_baile_P6_8.py` | `04dde58302281acc66b9e62bdc844c11` |
| `cantera/paper6/mide_don_P6_8.py` | `d650ea207259302771be0c240b65733a` |
| `cantera/paper6/mide_golpes_P6_8.py` | `aa72e6d6332bc2c0155df920c311821b` |
| `cantera/paper6/mide_largas_P6_8.py` | `04a7028540579f7a17f24754dad9448b` |
| `cantera/paper6/mide_lleno_P6_8.py` | `9ec4f1e909c168e6f795dae0040143e7` |
| `cantera/paper6/mide_muertes_P6_8.py` | `195c2d26220b7a8cc64303dd8fd92a01` |
| `cantera/paper6/mide_pareja_P6_8.py` | `98eebc6c28fa948f653bb23620e7b2a0` |
| `cantera/paper6/mide_separa_P6_8.py` | `3736fdbed59893b5461a192753f1d43f` |
| `cantera/paper6/mide_vuelta2_P6_8.py` | `b7490aa63bf42b7a5cb3f179ebd67946` |
| `cantera/paper6/mide_vuelta_P6_8.py` | `8e4d1a16aca4e169581d1fc71bb6f51b` |
| `cantera/paper6/policy_pareja8.py` | `6f3aee13897bbe9510c61e27e19b05cf` |
| `cantera/paper6/Dockerfile.pareja8` | `fc7372d9377d46f7b5da16976d35a616` |

Más los 20 `P68_t*_A2_<semilla>.json`, los 2 `P68_t*_peticiones.json` y los 40
diarios en `paintball/runs/P68_*/`. `P6_7_lleno.json` y `P6_7_golpes.json` (de
P6-7) fueron pisados por el barrido del punto A y **restaurados** por
recomputación, con su md5 original comprobado (`9346b94e…`, `68f02d70…`).

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

# CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — intacto |
| archivos de `CONGELADO.md` | 202 comprobados, 0 alterados |
| `policy_pareja.py`, `arreglos_P6_6.py`, `policy_pareja6.py` | no tocados (`796fc642…`, `4d10ea09…`, `933ad20f…`) |
| coste | **1,4450 USD** de 3 |
| patrones de clave en lo nuevo | ninguno |
| subido, empujado o borrado en git | nada (la política A2 se subió a la plataforma, como pide el encargo) |

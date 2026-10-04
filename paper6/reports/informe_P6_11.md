# P6-11 · El rival sin arma como amenaza menor, y serie corta

*27-sep-2026. `motor/model.py` intacto (`1e511978c251130e95169ebf8443efa1`), los
202 archivos de `CONGELADO.md` sin alterar, todo lo del seis en archivos nuevos.
Nada subido a git, nada empujado, nada borrado.*

**Decisión de Manel, aplicada:** un rival sin arma ES una amenaza, pero menor,
en proporción al daño que hace de verdad; y si te está pegando, es amenaza
plena, tenga arma o no. Sin filas nuevas.

---

## 1 · LO MEDIDO Y LO TOCADO

### 1.1 · Cuánto hace de verdad un golpe (`mide_dano_P6_11.py`)

987 golpes de rival en los 160 diarios de A0, A1, A2 y A3, por lo que el que pega
llevaba en la mano en ese tic:

| mano del que pega | golpes | daño mediana | mín. / máx. | catálogo (daño, alcance) |
|---|---:|---:|---|---|
| **vacía (`none`)** | **405** | **3,0** | 3,0 / 10,8 | — |
| lanza (`spear`) | 354 | 10,8 | 7,2 / 13,2 | 12, 2 |
| espada (`sword`) | 109 | 16,2 | 10,8 / 19,8 | 18, 1 |
| cuchillos (`knives`) | 76 | 8,0 | 8,0 / 8,0 | 8, 5 |
| arco (`bow`) | 28 | 14,0 | 14,0 / 14,0 | 14, 8 |
| cerbatana (`blowgun`) | 15 | 4,0 | 4,0 / 4,0 | 4, 6 |

De los 405 golpes con la mano vacía, **256 son de 3,0 y 95 de 4,5** (3 × la
escala de fuerza del cuerpo a cuerpo, (5+STR)/10, como con la lanza y la
espada); los 25 de 8,0 y 10,8 son cuchillos y lanzas que en ese tic no
estaban en la mano al mirar. **El puñetazo existe y vale 3**: un sexto de la
espada (18), un cuarto de la lanza (12). *(La nota de P6-3 «no existe el
puñetazo» era falsa; los datos lo desmienten 405 veces.)*

### 1.2 · Dónde decide el cuerpo qué es amenaza, y qué mira cada sitio

Todo en `appraisal_zs_v42_exp.py` (intocable; se lee, no se toca):

| sitio | qué mira | ¿ve el arma? |
|---|---|---|
| S-7-AGRESOR (`:638-656`) | quién me está pegando, por `damage_taken.source` | **no**: el que pega ya es amenaza plena |
| F-4-ALCANCE (`:1049-1063`) | todo hostil, por su distancia y el alcance del cuerpo a cuerpo | no |
| S-8-EXPOSICION (`:1391-1416`) | todo hostil que me ve | no |
| **F-HERMANO-AMENAZA / F-HERMANO-GOLPE** (`:1584-1591`) | hostil con `E = mundo.items[hand].damage`; **`if E <= 0: continue  # sin arma no hay amenaza`** | **sí: ceguera** |
| **F-REENCUENTRO** (`:898-901`) | el que me pegó y vuelve; **`_arma is None or damage <= 0 -> continue`** | **sí: ceguera** |
| amenaza de S-COMPANIA (`filas10`) | máx. de F-4, S-7, F-HERMANO-* | hereda |

Las dos cegueras leen la mano del hostil con `mundo.items.get(hand)`. Ése es el
asidero: **no hace falta tocar ninguna fila, hace falta que la mano vacía tenga
un arma que las filas puedan leer**.

### 1.3 · Qué se toca (`amenaza11_P6_11.py`), exactamente

1. **`mundo.items`** pasa a ser un dict-hijo (`ItemsConManos`) que responde por
   `get` a dos ids que **no** están en el catálogo, **sin cambiar su
   iteración**: el alfabeto del E2 (`parte2.alfabeto`, que ordena las claves)
   y `dmg_ref` (calculado al construir el mundo) quedan idénticos (humo `a`).
   * `~manos`: `Item(kind=ikMelee, damage=3, range=1)` — **el puñetazo medido**.
   * `~manos_pegando`: `Item(kind=ikMelee, damage=dmg_ref=18, range=1)` — **amenaza
     plena**, el daño de la mejor arma del catálogo.
2. **En la obs que ve el decisor** —una **copia**; la obs cruda que emite el
   parte y se guarda en el diario no se toca (humo `b`, y el humo de red
   comprueba que ningún E2 lleva `~` y que el diario guarda `none`)— a cada
   hostil visible o contado con la mano vacía se le pone `~manos`; si ese
   asiento **me está pegando** (está en `mem.agresores` dentro de la ventana
   S-7) **o es el agresor que declara el parte fresco del hermano**,
   `~manos_pegando`. Se envuelven `D.candidatos` y `D.decide` para que los dos
   vean la misma copia.

Efecto por fila: F-HERMANO-AMENAZA se enciende por un rival de mano vacía junto
al hermano con `base = 3/hp` (un sexto de la espada); F-HERMANO-GOLPE, cuando el
parte dice que le pegan, con daño pleno; F-REENCUENTRO cuenta al que me pegó
con la mano vacía y vuelve; F-4, S-8 y S-7 no cambian (ya no miraban el arma).

### 1.4 · Los humos (`humo_P6_11.py`, 5 de 5; `humo_red_P6_11.py`)

Replay tic a tic por la vía real de A3 (ojos, gemelo, `Memoria.observa`,
`D.candidatos`, `D.decide` con `Bloqueos`, v42, oído, don, P6-8b, S-COMPANIA
0,32) sobre diarios reales de A3:

| humo | resultado |
|---|---|
| a · el catálogo no cambia | 12 objetos, alfabeto igual; `~manos` daño 3 alcance 1; `~manos_pegando` daño 18 |
| b · la obs reescrita lleva `~manos`, la cruda sigue con `none` | tic 481: 1 reescrito, cruda intacta, hermano intacto |
| c · el que me pega con la mano vacía lleva `~manos_pegando` | 5 golpes reales |
| **d** · F-HERMANO-AMENAZA se enciende por un rival de mano vacía junto al hermano | `20784561` s10, 61 tics reales: **CON en 4, SIN en 0** |
| e · con `GEMV_MANOS=0`, decisiones idénticas | 601 tics |

Humo de red: 200/200 acciones, 0 errores, **158 tics con hostil de mano vacía
reescrito**, ningún E2 con id virtual, el diario guarda las manos crudas.

**Un fallo de método cazado por el camino, y corregido:** mis replays de P6-10
y P6-11 no encendían la empatía. `policy_cortex.py:93-96` fija **en código**
`A.EMPATIA_ON = True`, `H_PREV 0,25`, `H_GOLPE 1,0`, miedo y extraño apagados
(no por entorno), y mis replays no importaban ese módulo. Por eso el humo `d`
de P6-10 tenía un residuo de 0,017 «declarado» (era exactamente
F-HERMANO-AMENAZA), y por eso el humo `d` de aquí salía 0/61 con el cableado a
medias. Con el cableado de `policy_cortex` replicado en el banco, **el residuo
de P6-10 es 0,0000** (rehecho) y el humo `d` enciende la fila. El banco de
P6-10 (`banco_P6_10.py`) no se ve afectado: recomponía `d` de las filas
logueadas, no replayaba.

## 2 · EL BANCO (`banco_P6_11.py`, las 40 vidas de A3, replay con y sin)

Replay tic a tic de las 40 vidas de A3 por la vía real, dos veces —sin y con
la amenaza menor—, sobre las observaciones grabadas (contrafactual decisión a
decisión: dice qué decidiría el cuerpo en las mismas fotos, no cómo iría la
partida). **504.064 tics, 182.188 con piernas listas.**

### 2a · En los 166 golpes de rivales sin arma: ¿la amenaza estaba ya encendida antes?

«Antes» = alguna fila > 0 en la tabla del tic en los 24 tics anteriores al golpe.

| | sin el cambio | **con el cambio** |
|---|---:|---:|
| golpes de rival con la mano vacía a la vista | 166 | 166 |
| **cualquier fila de miedo** encendida antes (F-4, S-8, S-7, F-HERMANO-*, F-REENCUENTRO) | **166** | **166** |
| **las que miran el arma** (F-HERMANO-AMENAZA/GOLPE, F-REENCUENTRO) encendidas antes | 107 | **120** |

**El cuerpo ya «veía» al rival de mano vacía antes de los 166 golpes**: F-4-ALCANCE y
S-8-EXPOSICION no miran el arma. Lo que no tenía era el miedo *por el hermano* y el
del *reencuentro*, que con el cambio se encienden antes en **13 golpes más** (107 →
120). La amenaza menor no descubre al rival: le da a las dos filas ciegas algo que
leer.

### 2b · Cuántas decisiones cambian en total

| | |
|---|---:|
| decisiones con piernas listas | 182.188 |
| **que cambian** | **1.005 (0,55 %)** |
| …`ir_* → paso_*` | 820 |
| …`ir_* → move_*` | 70 |
| …`move_* → move_*` (otra dirección) | 36 |
| …el resto (18 combinaciones) | 79 |

**No se vuelve miedoso de todo lo que se mueve:** una decisión de cada 180. Y el
cambio dominante es `ir_objeto/ir_botin → paso_*`: en vez de ir derecho a por el
botín junto a un rival de mano vacía, da un paso. Un rival que pega 3 no cambia
casi nada; un rival que pega 3 junto al hermano, o que ya me pegó, sí.

## 3 · LA SERIE: A4 EN LAS 20 SEMILLAS

**Coste: 1,3737 USD** de los 3 (20 partidas, todas con coste facturado; 40
diarios). Política `gemv-p6-A4-manos:v1` (`b4e322cf…`), imagen
`gemv-anima:pareja11`. **Control: A0 de P6-6 y A3 de P6-10**, ya jugados y no
repetidos (mismo punto de partida, mundo, liga, roster y semillas; distinto
día). Sello cerrado antes de jugar: `SELLO_P6_11.md`
(`538644e9a20b49c3f736707bdea3e53d`).

### 3.1 · El sello, predicción a predicción

| # | sellado | salió | veredicto |
|---|---|---|---|
| 1 | golpes de rival con la mano vacía ≤ 120 (falla si > 150) | **148** (A3 166; A0 103) | **no alcanzada**: baja un 11 %, no llega a 120; no cae en el fallo |
| 2 | muertes por rival con la mano vacía ≤ 3 | **2** (A3 6; A0 2) | **acierta** |
| 3 | vida media ≥ 12.500 | **12.840,2** (A3 13.082,6; A0 12.427,9) · emparejado A4 − A3 **+39** (10/20, p = 1,000); A4 − A0 −10 (9/20, p = 0,824) | **acierta** — la vida de A3 no se pierde |
| 4 | a ≤ 3 casillas ≥ 70 % · > 15 ≤ 2 % · escapadas ≥ 200 tics ≤ 5 | **77,26 % · 0,00 % · 0** (A3 78,9 / 0,0 / 1) | **acierta** |
| 5 | comida ≥ 3,0 por vida (falla si < 2,8) | **2,88** (A3 3,95; A0 3,20) | **no alcanzada**: baja un 27 % desde A3, al nivel de A2 (2,52); no cae en el fallo |
| 6 | no se vuelve miedoso: golpes con arma ≤ 150, muertes por anillo ≤ 22 | **101** · **22** (A3 107 · 19) | **acierta** (el anillo, justo en el borde) |
| 7 | coste ≤ 1,5 | **1,3737** | acierta |

**5 aciertos, 2 no alcanzadas, 0 fallos.** Las dos no alcanzadas son las dos
caras del cambio: quita golpes de mano vacía (−11 %) y quita comida (−27 %).

### 3.2 · A0 / A3 / A4

| medida | A0 | A3 | **A4** |
|---|---:|---:|---:|
| golpes: anillo · rival con arma · **mano vacía** · no visto | 380 · 155 · 103 · 0 | 457 · 107 · **166** · 0 | **375 · 101 · 148 · 0** |
| muertes por rival con arma · **con mano vacía** · anillo · no consta | 9 · 2 · 20 · 1 | 3 · **6** · 19 · 2 | **4 · 2 · 22 · 1** |
| mueren / sobreviven | 32 / 8 | 30 / 10 | **29 / 11** |
| vida media de la pareja | 12.427,9 | 13.082,6 | **12.840,2** |
| distancia: a ≤ 3 / ≤ 8 / > 15 | 79,1 / 96,9 / 0,0 % | 78,9 / 96,3 / 0,0 % | **77,3 / 98,4 / 0,0 %** |
| escapadas > 8 · de ≥ 200 tics | 481 · 3 | 312 · 1 | **305 · 0** |
| muertes con el otro vivo y a ≤ D0 de camino | 17/18 | 19/19 | **15/17** |
| muerte por rival: dist. al hermano (mediana) | 1 | 1 | **3,5** |
| los dos vivos al cierre | 18/20 | 18/20 | **19/20** |
| sobrevive el otro tras el primero (mediana) | 912 | 425 | **804** |
| comida recogida por vida | 3,20 | 3,95 | **2,88** |
| `coger` + `inventory_full` | 6.254 | 0 | **0** |
| S-COMPANIA dentro de D0 en mi casilla | — | 0 errores | **0 errores** · M fuera de D0 mediana 0,044 |
| don: episodios · reabsorbidos · efectivos · recogidos · usados | 67 · 1 · 66 · 17 · 16 | 90 · 29 · 61 · 16 · 13 | **61 · 11 · 50 · 12 · 11** |
| F-HERMANO-AMENAZA: tics · solo por contado | 29.085 · 0 | 102.856 · 24.622 | **75.449 · 26.912** |
| \|disc\| S-8 por decisión | 0,0585 | 0,0391 | **0,0433** |

### 3.3 · Lo que dice

1. **Las muertes por rival de mano vacía vuelven al nivel de A0: 6 → 2**, y las
   muertes por rival en total bajan de 9 a 6. Los golpes bajan menos (166 → 148):
   el cuerpo sigue al lado de rivales de mano vacía —está junto a su hermano,
   que es donde están—, pero ya no se deja matar por ellos.
2. **Nada de lo de A3 se pierde**: la pareja sigue junta (77,3 %, cero
   escapadas largas), la vida se mantiene (12.840; +39 emparejado sobre A3), 11
   supervivientes, 19 de 20 parejas enteras al cierre.
3. **Lo que se paga es comida: de 3,95 a 2,88 por vida.** El banco lo
   anticipaba en su forma (820 de los 1.005 cambios son `ir_objeto/ir_botin →
   paso_*`: en vez de ir derecho al botín junto a un rival de mano vacía, da un
   paso) y no en su tamaño. Es una decisión de cada 180, y son justo las del
   botín cercano.
4. **No se vuelve miedoso**: golpes con arma 101 (A3 107), S-8 por decisión
   0,043 (A3 0,039), muertes por anillo 22 (A3 19, A0 20) — en el borde de lo
   sellado, y hay que vigilarlo: un cuerpo que da un paso en vez de ir a por el
   botín está un poco más tiempo donde el anillo lo alcanza.
5. **El don se reabsorbe menos** (29 → 11 de 61-90): menos tiempo parado junto
   al regalo.

---

# LO QUE ME LLEVO

1. **El puñetazo existe y vale 3** (405 golpes), un sexto de la espada. La nota
   de P6-3 estaba equivocada.
2. **Las cegueras eran dos y estaban localizadas**: F-HERMANO-AMENAZA/GOLPE y
   F-REENCUENTRO piden `damage > 0`; F-4, S-8 y S-7 no miran el arma. Con un
   arma virtual leída por `mundo.items.get`, sin tocar ninguna fila ni el
   catálogo, las dos ven.
3. **Cambia una decisión de cada 180**, y en campo quita 4 muertes de mano
   vacía y una recogida de comida por vida.
4. **Mis replays no encendían la empatía** (la fija `policy_cortex` en código):
   corregido, y el residuo «declarado» de P6-10 era exactamente eso. Ahora el
   replay reproduce el diario bit a bit.

*Sin propuestas. Lo que queda abierto es el precio en comida, y eso es de
Manel.*

## LOS ARCHIVOS NUEVOS, CON SU MD5

| archivo | md5 |
|---|---|
| `cantera/paper6/Dockerfile.pareja11` | `98040b3b288b6d71904a5cf56e2d76f9` |
| `cantera/paper6/P6_11_banco.json` | `a37cde928ceb1bdc144c5c131089e307` |
| `cantera/paper6/P6_11_base2.json` | `78694f50bf6cc8ea46322f02238e7fb3` |
| `cantera/paper6/P6_11_brazos.json` | `aef0f5c05e326f3481734ea90f417997` |
| `cantera/paper6/P6_11_dano.json` | `2c02149f51644cbd4bb0566bf803b3c1` |
| `cantera/paper6/P6_11_don.json` | `3103f596668d28e6efc3120bb6b60d61` |
| `cantera/paper6/P6_11_fila.json` | `6ee16a8fc20018c72ab9775367b9a380` |
| `cantera/paper6/P6_11_golpes.json` | `51f2c4af3500eecf16b88d3df84e8d47` |
| `cantera/paper6/P6_11_largas_A4.json` | `d751713988987e9331980363e24189ce` |
| `cantera/paper6/P6_11_lleno.json` | `9f6071799d1f453bf20c77d5f631eff0` |
| `cantera/paper6/P6_11_medidas.json` | `61b4ab682d73f413228f8f92204b65f6` |
| `cantera/paper6/P6_11_p67.json` | `1a4e8dafc82379b69a7896e118665f39` |
| `cantera/paper6/P6_11_pareja.json` | `0c0d8921e86683c6a88aaa739b0fb542` |
| `cantera/paper6/P6_11_separa.json` | `3228aa84ab0912c27f2035c2348fb61a` |
| `cantera/paper6/SELLO_P6_11.md` | `538644e9a20b49c3f736707bdea3e53d` |
| `cantera/paper6/amenaza11_P6_11.py` | `9d493b05495f55316f29cbffa5561cdb` |
| `cantera/paper6/banco_P6_11.py` | `e6dcd998f0746da1459215ee155b6d4d` |
| `cantera/paper6/humo_P6_11.py` | `c323121579ad712cce5cac3ab171ce74` |
| `cantera/paper6/humo_red_P6_11.py` | `554fb2c432af274a181ff9e7a4bb2551` |
| `cantera/paper6/lanza_P6_11.py` | `917550012076c7aba585f03dadffe4ae` |
| `cantera/paper6/mide_P6_11.py` | `7da3654362069801bc051ade4bb019c2` |
| `cantera/paper6/mide_base2_P6_11.py` | `0b60f27e569a7a0b7c8b7c35432249ec` |
| `cantera/paper6/mide_dano_P6_11.py` | `f050ddbca69bb86918b0a9668b8dde96` |
| `cantera/paper6/mide_don_P6_11.py` | `4f652f1f9ba622c4f2a50251c8aa90f7` |
| `cantera/paper6/mide_fila_P6_11.py` | `89ab3b4e97eaf36f17d1e03e0c4ef5b1` |
| `cantera/paper6/mide_golpes_P6_11.py` | `6ee1e8a0181dac660f2d0d26368b3692` |
| `cantera/paper6/mide_largas_P6_11.py` | `ef7c0da98ac9738f9469369422f2a756` |
| `cantera/paper6/mide_lleno_P6_11.py` | `bba84ba6c2ecb6dd8ed5aa3a85c7a8e2` |
| `cantera/paper6/mide_muertes_P6_11.py` | `660f693abda2a092296582bbc3879130` |
| `cantera/paper6/mide_pareja_P6_11.py` | `b890c74c1cee535e95d13e6ab7a558a2` |
| `cantera/paper6/mide_separa_P6_11.py` | `2db034961a423e37cde578523caf5c7f` |
| `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` |

Más los 20 `P611_t*_A4_<semilla>.json`, los 2 `P611_t*_peticiones.json` y los
40 diarios en `paintball/runs/P611_*/`. Se tocaron dos archivos de encargos
anteriores, y se dice: `banco_P6_11.py` es nuevo; `humo_P6_10.py` recibió el
cableado de la empatía (residuo 0,017 → 0,0000), y su md5 cambia respecto al
informe de P6-10 (`20d5386be263b8715d1505a14d179def`).

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

## CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — intacto |
| archivos de `CONGELADO.md` | 202 comprobados, 0 alterados |
| coste | **1,3737 USD** de 3 |
| patrones de clave en lo nuevo | 1 aviso, falso: la expresión regular de la custodia en `Dockerfile.pareja11` |
| subido, empujado o borrado en git | nada (la política A4 se subió a la plataforma, como pide el encargo) |

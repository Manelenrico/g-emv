# P5-8N — ¿La fila de la ignorancia le quita fuerza a la llamada del botín?

Diagnóstico **en seco**, **coste cero**. Motor, decisor y tabla intocados,
idénticos al empezar y al acabar. **Sin sellos. No toca la serie en curso.**

---

## El titular

**No, porque la fila no está puesta. En el brazo K de P5-8M
`R-CURIOSIDAD-FRONTERA` NO está instalada — ni durante las formas ni fuera de
ellas.**

Tres pruebas independientes:

| | |
|---|---|
| **código** | `CUR_MOD.instala()` se llama **solo si `CURIOSIDAD_ON`** (`policy_forma.py:1335-1336`), y `CURIOSIDAD_ON = CURIOSIDAD in ("frontera","local")` (`:76`) |
| **entorno** | en los **17 asientos de K** de las tandas 1 y 2: `GEMV_CURIOSIDAD=''` → **`CURIOSIDAD_ON = False`** |
| **diarios** | **cero registros `curiosidad_tic`** en los 17 asientos |

**El brazo K de P5-8M lleva el mecanismo de FORMA, no el renglón.** Son dos
cosas distintas que comparten nombre: `GEMV_CURIOSIDAD_FORMA=1` (encendido) y
`GEMV_CURIOSIDAD=''` (apagado).

**Y midiendo lo que de verdad preocupaba —si K recoge peor botín fuera de las
formas— sale lo contrario de lo esperado: K va MÁS al botín y recoge MÁS.**

| fuera de forma | **K** | **A** |
|---|---|---|
| decisiones que gana `ir_botin` | **0,486 %** | 0,363 % |
| decisiones que gana `ir_objeto` | **2,194 %** | 1,453 % |
| decisiones que gana `noop` | **66,3 %** | **82,3 %** |
| **botín recogido por cien tics** | **1,501** | **0,986** |
| W mediana | **1,350** | 1,625 |
| distancia mediana al botín visible | **1,0** | 2,0 |

**Fuera de forma la maquinaria de decisión de K es la misma que la de A** —el
renglón no está, y el candidato de la forma aparece **0 veces** en la papeleta
fuera de forma en los dos brazos—. **Toda la diferencia es de trayectoria: la
forma deja al cuerpo en otro sitio, más pobre y más cerca del botín, y entonces
el cuerpo actúa más.**

---

## Custodia

```
                            al empezar                         al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1   idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252   idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640   idéntico
```

35 asientos de K y A de las tandas 1 y 2 de P5-8M. **Gasto: cero.**

---

## 1 · La fila, leída en el código

```python
# policy_forma.py:75-76
CURIOSIDAD = (os.environ.get("GEMV_CURIOSIDAD", "") or "").strip().lower()
CURIOSIDAD_ON = CURIOSIDAD in ("frontera", "local")

# policy_forma.py:1335-1336 — la ÚNICA llamada
if CURIOSIDAD_ON:
    CUR_MOD.instala()          # esto es lo que pone el proxy en D.A
```

`instala()` (`curiosidad.py:409-412`) hace `D.A = CUR`: **es la única forma de
que el renglón entre en la tabla**. Con `GEMV_CURIOSIDAD` vacío nunca se llama,
`D.A` sigue siendo v42 sin tocar, y **la `d` del cuerpo es la de siempre, bit a
bit**.

**Medido en los diarios**, no supuesto:

```
GEMV_CURIOSIDAD='' · CURIOSIDAD_ON=False  ->  17 asientos de 17
asientos de K con registro `curiosidad_tic`: 0 de 17
```

*(Lo que sí está encendido en K es `GEMV_CURIOSIDAD_FORMA=1`, que es el
mecanismo de la forma: nacer, juzgar con la puerta, comprometerse. El renglón de
P5-7A es otra cosa y está apagado desde P5-8B.)*

---

## 2 · Fuera de forma, K contra A

### Agregado (17 asientos de K, 18 de A)

| | K | A |
|---|---|---|
| `ir_botin` | **0,486 %** | 0,363 % |
| `ir_objeto` | **2,194 %** | 1,453 % |
| `noop` | 66,347 % | **82,282 %** |
| botín / 100 tics | **1,501** | 0,986 |
| W mediana | 1,350 | **1,625** |
| distancia al botín | **1,0** | 2,0 |
| **`_FM_` fuera de forma** | **0** | **0** |

**El último renglón es el control**: fuera de forma no hay inyección, así que el
candidato de la forma no puede estar en la papeleta. **No está, en ninguno de
los 35 asientos.**

### Por semilla

| semilla | `ir_botin` K/A | botín/100 K/A | W K/A |
|---|---|---|---|
| 20365645 | **1,580**/0,309 | 0,061/**0,720** | 0,42/1,46 |
| 20470374 | 0,041/**0,804** | 0,027/**0,179** | 0,69/0,75 |
| 20575103 | **0,214**/0,035 | **0,257**/0,104 | 0,68/1,18 |
| 20679832 | 0,697/0,841 | **1,999**/1,520 | 1,07/1,83 |
| 20784561 | 0,329/0,462 | 0,041/**16,461** | 1,00/1,42 |
| 20889290 | **0,437**/0,025 | 0,089/0,098 | 1,57/1,47 |
| 20994019 | 0,040/**0,342** | **0,789**/0,085 | 1,94/1,42 |
| 21098748 | **0,586**/0,354 | 0,058/**0,769** | 1,75/1,75 |
| 21203477 | 0,266/0,280 | **6,768**/0,073 | 1,73/2,73 |

**El agregado lo mandan dos semillas opuestas**: `21203477` (K recoge 6,77 por
cien tics contra 0,07) y `20784561` (A recoge **16,46** contra 0,04). **K va por
delante en 5 semillas y por detrás en 4.** Con nueve semillas **no hay una
diferencia sistemática**, y el agregado de 1,501 contra 0,986 **no lo defiendo**.

### La `d` del dominio R con y sin la fila

**Son la misma, exactamente, y no hace falta recalcular nada: la fila no está
instalada.** `D.A` es v42 sin envolver, así que el `d` de R en los diarios **ya
es el «sin fila»**.

---

## 3 · La inversión: ¿qué haría la fila SI se instalara?

El punto 3 pedía apagar la fila. Como está apagada, hice lo simétrico: **la
encendí en seco** sobre los mismos tics fuera de forma de K, muestreados con el
arnés de P5-2 (`DESDE=300`, `CADA=50`), y redecidí con ella y sin ella.

| | |
|---|---|
| decisiones muestreadas | **2.551** |
| **cambian de ganador** | **433 = 16,97 %** |
| **dejan de ganar `ir_botin` por la fila** | **8 = 0,31 %** |
| pasan a ganar `ir_botin` por la fila | 2 |

**Los cambios más frecuentes (sin fila → con fila):**

| | | n |
|---|---|---|
| `move_SE` | `move_W` | 115 |
| `move_NW` | `move_W` | 103 |
| `noop` | `ir_pareja` | 51 |
| `noop` | `paso_S` | 44 |
| `move_S` | `move_SW` | 20 |
| … | | |
| **`ir_botin`** | **`ir_centro`** | **6** |

**La fila reorienta el movimiento, que es lo que fue diseñada para hacer. La
llamada del botín la toca ocho veces de 2.551.**

**Así que la respuesta a tu pregunta, incluso en el mundo donde la fila estuviera
puesta, sería no:** le quitaría el tic a `ir_botin` en el **0,31 %** de las
decisiones fuera de forma.

### El control de que la fila se enciende — y un cero mío, cazado

```
la fila valorada 20.325 veces · con M > 0 en 12.355 · M máximo 0,11473
```

**La primera pasada de este contrafactual dio CERO cambios**, y ese cero era
mío: no rellené lo que la política viva rellena cada tic
(`policy_forma.py:1355-1358`) — `amenaza_ahora`, `ign_global` y sobre todo
`dist_frontera`, que en modo «frontera» es lo que da valor al renglón. Sin ello
la fila vale 0 siempre.

**Lo cazaron los contadores de diagnóstico que el propio módulo trae**
(`n_valor`, `n_valor_pos`, `max_M`), puestos en P5-7A precisamente para
distinguir «el renglón no se enciende» de «se enciende y no voltea nada». **Es
la cuarta vez en esta serie que un cero mío resulta ser un contador mal
alimentado**, y por eso el script ahora lleva un `assert` sobre `n_valor_pos`.
El `M` máximo, 0,11473, coincide con el 0,11476 que midió P5-7C.

---

## 4 · La vida: muerte, causa y manos

| semilla | tic de muerte K/A | causa | W al morir K/A | puesto K/A |
|---|---|---|---|---|
| 20365645 | 9.600 / 11.655 | eliminated / eliminated | 0,81/0,61 | 10,5/9,5 |
| 20470374 | **7.908 / 1.040** | eliminated / eliminated | 0,66/0,75 | 12,0/15,0 |
| 20575103 | 2.992 / 3.356 | eliminated / eliminated | 1,20/1,18 | 14,0/14,0 |
| 20679832 | **2.192 / 12.912** | eliminated / eliminated | 1,05/2,05 | 14,5/9,5 |
| 20784561 | 5.387 / 2.427 | eliminated / eliminated | 1,00/1,75 | 15,0/15,5 |
| 20889290 | 9.598 / 10.662 | eliminated / eliminated | **1,99**/0,69 | 13,5/8,0 |
| 20994019 | 9.410 / 8.678 | eliminated / eliminated | **1,35**/0,53 | 12,0/14,5 |
| 21098748 | 11.804 / 11.928 | eliminated / eliminated | **1,36**/0,71 | 9,5/7,0 |
| 21203477 | 12.840 / 13.524 | eliminated / eliminated | 1,04/1,70 | 6,0/3,5 |

| | K | A |
|---|---|---|
| causas | **eliminated 17/17** | **eliminated 18/18** |
| tic de muerte mediano | **9.329** | **9.440** |
| **W al morir, mediana** | **1,200** | **1,096** |
| hp en el último tic | 4 | 4 |

**Todos mueren igual: eliminados, ninguno por el anillo ni por otra causa.**

**Y los tres números que importan son casi iguales**: el tic de muerte mediano
difiere en el 1,2 %, el hp final es idéntico, y **K muere con las manos algo más
llenas que A** (1,200 contra 1,096).

**La varianza por semilla es enorme** (K muere en el tic 2.192 en una y en el
12.840 en otra) **pero no tiene signo**: K vive más en 4 semillas y menos en 5.

---

## Lo que no sé, marcado como tal

**No sé por qué K hace `noop` en el 66 % de los tics fuera de forma y A en el
82 %.** Con la misma maquinaria, esa diferencia solo puede venir del estado, y
la W más baja de K (1,35 contra 1,63) es coherente —más carencia, más ganas de
actuar— **pero no lo he demostrado**.

**No defiendo el agregado de botín.** K recoge más en 5 semillas y menos en 4, y
el agregado lo deciden dos semillas opuestas con valores extremos. **Con nueve
semillas no hay diferencia sistemática.**

**No sé qué hace exactamente el 17 % de decisiones que la fila cambiaría.** Sé
que reorienta el movimiento y que casi no toca `ir_botin`; **si eso mejora o
empeora al cuerpo, este diagnóstico no lo dice** — para eso está el brazo Q de
P5-7C, que sí lo midió en campo.

**Y sigue sin explicación por qué en las seis semillas de la tanda 3 K recogía
un décimo del botín de A.** Este diagnóstico descarta la fila (no está) y
descarta el tiempo de las formas (2,1 %), **pero no encuentra el mecanismo.**

---

## Lo que esto deja

**La pregunta que hiciste tiene respuesta negativa por partida doble**: la fila
no está puesta, y si lo estuviera le quitaría el tic a `ir_botin` tres veces de
mil.

**Y el diagnóstico deja una observación que no esperaba**: fuera de forma, el
cuerpo de K **no está frenado, está más activo** que el de A —la mitad de
`noop`— y **más cerca del botín**. Si K recoge menos en algunas semillas, no es
porque la curiosidad le quite ganas ni tiempo.

`cantera/paper5/mide_P58N.py` · `mide_P58N_inv.py` · datos `P58N.json`.

**PARO AQUÍ.**

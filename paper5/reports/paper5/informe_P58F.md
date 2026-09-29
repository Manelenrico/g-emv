# P5-8F — Qué hace el cuerpo mientras «sigue» una forma

Diagnóstico, **en seco**, **coste cero**, sin imagen y sin plataforma. Motor,
decisor y tabla intocados (`1e511978c251130e95169ebf8443efa1`).

**Sin sellos**, como se pidió.

---

## El titular

**El cuerpo no sigue la forma. La forma gana el 2,12 % de las decisiones.**

En 63.254 tics con forma activa, repartidos en 144 formas aceptadas de las tres
sondas, el paso de la forma (`_FM_ir_x_y`) ganó **1.344 veces**. El resto de las
decisiones las ganó el cuerpo: `noop` sobre todo, y sus propios `ir_objeto`,
`ir_botin`, `ir_pareja`.

**Y el cuerpo apenas se acerca:** se mueve en el **8,94 %** de los tics —lo que
cabe con 11 tics por casilla— pero **solo el 6,5 % de esos movimientos acerca al
destino**. La distancia mediana al destino va de **4 al nacer a 3 al terminar**.
En toda la vida de una forma, el cuerpo recorre **una casilla**.

**Eso explica los tres contadores que venían saliendo raros**: el atasco (no se
acerca porque no va), el «deja de ganar» (la forma no avanza, así que su ventaja
proyectada no se realiza) y, sobre todo, **las casillas nuevas dentro de forma**:
si el cuerpo no va a la frontera, no descubre la frontera.

---

## 1 · El mapa, leído del mundo

| | |
|---|---|
| arena | **48 × 48 = 2.304 casillas** |
| radio de visión (INT 8) | **9,0** — `5 + (INT+1)//2`, `mundo.py:256` |
| oclusión | **sí**: `linea_de_vista` corta con `#`, `F`, `R` (muro, fortaleza, roca) |
| efecto real de la oclusión | desde (24,24) se ven **133 de 253** casillas del radio: **el 47 % queda ocluido** |

**Los tres contadores leen la misma estructura**, `Ojo.primera_vez`, y en el
mismo momento del tic:

```
BFS de la frontera   ->  if (x, y) != pos and (x, y) not in ojo.primera_vez
contador de nuevas   ->  if c not in self.primera_vez: self.primera_vez[c] = tick
ignorancia global    ->  return 1.0 - len(self.primera_vez) / float(self.n_arena)
```

**No hay discrepancia de estructura ni de momento.** El `Ojo` vivo de la política
y el que reconstruyo aquí son instancias distintas de la misma clase alimentadas
con las mismas posiciones del diario.

---

## 2 · El seguimiento

144 formas aceptadas · **63.254 tics con forma activa**

| | |
|---|---|
| el cuerpo **se mueve** | 5.655 / 63.254 = **8,94 %** de los tics |
| el movimiento **acerca** al destino | 366 = **0,58 %** de los tics = **6,5 % de los movimientos** |
| **gana el paso de la forma** | 1.344 = **2,12 %** de las decisiones |
| distancia al destino | **4 al nacer → 3 al terminar** (medianas) |

### Por causa de fin

| causa | n | gana la forma | distancia | objetivo visto durante |
|---|---|---|---|---|
| **atasco** | 71 | 4,25 % | 4 → 3 | **0** |
| deja de ganar | 38 | 11,05 % | 4 → 3 | **0** |
| sin fin (vivas al acabar) | 32 | 1,88 % | 2 → **4** | 2 |
| **completada por alivio** | **2** | 9,09 % | **3 → 1** | **72** |
| veto duro | 1 | 9,09 % | 2 → 2 | 0 |

**Las dos completadas por alivio son las únicas que se comportan como la teoría
dice**: la forma gana más decisiones, la distancia baja de 3 a 1, y se ven **72
casillas del objetivo**. Son dos de 144.

Las «sin fin» son peores: **se alejan** (2 → 4) y viven una eternidad (mediana
1.807 tics) porque nada las mata.

---

## 3 · El descubrimiento

Casillas **no vistas al nacer** que el destino revelaría (radio de vista
alrededor del destino), y cuándo se descubren:

| | casillas | % |
|---|---|---|
| **antes** de nacer | 0 | — *(control: 0 por construcción)* |
| **durante** la forma | 293 | **16,7 %** |
| **después**, en 100 tics | 111 | 6,3 % |
| **nunca** | **1.346** | **76,9 %** |

**El control funciona: cero antes.** Y la respuesta a la pregunta del vigilante
es clara: **no es que la frontera se vea de camino** (16,7 % durante, 6,3 %
después). **Es que no se ve nunca: el 76,9 % del objetivo sigue sin verse.**

Eso **descarta la primera de mis dos sospechas de P5-8E** («las casillas se
descubren antes de entrar en forma») y **refuerza la segunda**, aunque con un
matiz importante: no es que seguir la forma sustituya lo que descubría — es que
**el cuerpo no sigue la forma**, así que nunca llega a donde estaba lo nuevo.

---

## 4 · El control de aritmética

**No se puede aplicar, y hay que decirlo.**

La cota propuesta era: *si cada forma completada por llegada revela al menos su
casilla de destino, las casillas nuevas dentro de forma no pueden ser menos que
las completadas por llegada partido por los tics dentro.*

**En las tres sondas hay CERO formas completadas por llegada.** Dos completadas
por alivio, ninguna por llegada. **Con numerador cero la cota es cero y el
control es vacío**: no valida ni invalida el contador.

**Lo que sí puedo decir:** las dos completadas por alivio revelaron 72 casillas
del objetivo de mediana, lo que es coherente con un contador que funciona. El
contador de la sonda **no queda probado, pero tampoco desmentido**.

---

## Lo que no sé, marcado como tal

**No sé por qué la forma gana tan poco.** El 2,12 % es un hecho; la causa no la
tengo. Cabe que el candidato de la forma pierda por `d` contra `noop` y los `ir_`
del cuerpo, o que el veto de movimiento (`move_ready_in`) lo tumbe casi siempre.
**Separarlo pide mirar las `d` de los candidatos tic a tic, y no está en este
encargo.**

**No sé si las 32 formas «sin fin» son un defecto.** Viven 1.807 tics de mediana
y se alejan del destino. Ni el atasco ni el examen las matan. Parece un agujero,
pero puede que sean formas cuyo asiento murió antes de que nada disparase.

**Un error mío, cazado a tiempo.** La primera pasada dio **0,00 %** de
decisiones ganadas por la forma. Antes de publicarlo comprobé el nombre del
candidato: es `_FM_ir_x_y`, no empieza por «forma». **El cero era mío, no del
mundo.** Corregido, sale 2,12 %. Es la tercera vez en esta serie que un cero
mío resulta ser un contador mal apuntado, y por eso ya no publico un cero sin
ir a ver de dónde sale.

---

## Lo que esto significa para las cuarenta

**El problema no está en los plazos.** He cambiado el reloj tres veces —examen,
atasco, y el paso del mundo— y cada vez ha funcionado lo que toqué. **Pero el
cuerpo no sigue la forma**, y ningún plazo arregla eso.

Antes de gastar las cuarenta habría que saber **por qué el paso de la forma
pierde el 98 % de las decisiones**. Es una medida en seco, de coste cero, sobre
estos mismos diarios: comparar la `d` del candidato de la forma con la del
ganador, tic a tic, mientras la forma está activa.

**No la he hecho: no está en este encargo.** Lo propongo.

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1   (idéntico)
paintball/alma/decisor_zs.py       8fa03547e3228ef9df4aa94c444f9252
paintball/alma/appraisal_zs_v42_exp.py
                                   98c13d60167c80cc8334c965be75c640
```

`cantera/paper5/mide_P58F.py` · datos `P58F.json` · diarios de K de las sondas
1, 2 y 3. **Gasto: cero.**

**PARO AQUÍ.**

# P5-8G — Por qué pierde la forma, qué haría el compromiso, y si el cuerpo siguió al consejero

Diagnóstico, **en seco**, **coste cero**. Motor, decisor y tabla intocados
(`1e511978c251130e95169ebf8443efa1`). **Sin sellos.**

---

## El titular

**La forma no pierde: no la dejan competir.** En el 80,52 % de los tics con
forma activa, **el candidato `_FM_ir_x_y` ni siquiera aparece en la lista de
candidatos**. Cuando aparece, **gana 516 de 952 = el 54,2 %**.

Eso corrige lo que escribí ayer. En P5-8F dije «la forma gana el 2,12 % de las
decisiones» y lo leí como que el cuerpo la ignoraba. **El 2,12 % era sobre todos
los tics, incluidos los 80 % en que la forma no estaba en la papeleta.** Sobre
las decisiones en que sí compite, gana más de la mitad.

**La causa del 80 % es el enfriamiento de movimiento.** El cuerpo anda a 11 tics
por casilla; durante los otros diez, los candidatos de tipo `ir_`/`move_` están
vetados (`decisor_zs.py:95-104`, `move_ready_in > 0`), y el de la forma es uno
de ellos. **10 de cada 11 es el 90,9 %; el 80,5 % medido encaja.**

**Y el compromiso saldría barato:** obedecería la forma en el **69,54 %** de los
tics, con **una sola** condición de ruptura disparando, y costaría **+0,100 de
`d` por tic desobedecido**.

---

## 1 · Por qué pierde

**4.887 tics con forma activa** (los que tienen `cur_forma_tic` con forma y
radiografía; ver la nota de conteo abajo).

| | | |
|---|---|---|
| **el candidato NO está** (vetado) | **3.935** | **80,52 %** |
| gana la forma | 516 | 10,56 % de todos · **54,2 % de los 952 en que compite** |
| pierde | 436 | 8,92 % de todos · 45,8 % de los que compite |

**Cuando pierde, pierde por poco margen homeostático pero claramente:**
`d(forma) − d(ganador)` = **mediana +0,11280** (Q1 +0,07682 · Q3 +0,15964).
Positivo significa que la forma es peor: el cuerpo tiene razón.

**Contra quién pierde:**

| | |
|---|---|
| `ir_objeto` | 196 |
| `ir_pareja` | 146 |
| `move_NW` | 80 |
| otros `move_` | 14 |

**Nunca pierde contra `noop`.** Eso tiene sentido: los tics en que `noop` gana
son justo los del enfriamiento, y en ésos la forma ni siquiera está.

**El reparto de la derrota, entonces:**

| | tics | % de los activos |
|---|---|---|
| **por veto** (no está en la papeleta) | 3.935 | **80,52 %** |
| **por distancia homeostática** (está y pierde) | 436 | **8,92 %** |
| gana | 516 | 10,56 % |

**Ocho de cada diez derrotas no son derrotas: son ausencias.**

---

## 2 · El compromiso, simulado en seco

Sobre los mismos tics, con las seis condiciones de ruptura del diseño:

| | tics | % |
|---|---|---|
| **obedecería la forma** | **662** | **69,54 %** |
| rompe por **(e) rival a menos de 6 y acercándose** | 290 | **30,46 %** |
| rompe por (a) veto vital, armado a tiro | **0** | 0 % |
| rompe por (b) veto duro | **0** | 0 % |
| rompe por (c) daño recibido en el tic | **0** | 0 % |
| rompe por (d) carencia sube o vida < 15 | **0** | 0 % |

**Una sola condición hace todo el trabajo, y es la más laxa.** «Un rival no
hermano a menos de 6 casillas» dispara el 30 % de las veces; las otras cinco,
ninguna. En el mundo lento sin cazadores, el peligro real —armado a tiro, daño,
vida baja— **no ocurre nunca durante una forma**.

**Cuántas llegarían:** con el cuerpo andando el camino a 11 tics por casilla y
sin rupturas, **57 de 144 formas (39,6 %)** habrían alcanzado el destino dentro
de su vida. Las otras 87 morían antes por plazo, no por peligro.

**El coste del compromiso:** la suma de `d(forma) − d(ganador)` en los tics en
que habría desobedecido al ganador es **+22,438** repartidos en **224 tics**,
es decir **+0,10017 de `d` por tic desobedecido**.

Para ponerlo en escala: el margen de la puerta es 0,062 y la `d` típica del
cuerpo ronda 3-4. **Obedecer la forma cuesta unas tres centésimas de la `d`
total por tic desobedecido.** No es gratis y no es ruinoso.

---

## 3 · P5-6C, brazos F y T — **con un sesgo que invalida la comparación**

**Antes de los números, el sesgo, porque manda sobre ellos.** En K los tics
activos salen de `cur_forma_tic`, que se escribe **en todos** los tics vivos. En
F y T no existe ese registro: los tics activos los saco de `forma_tic`, que
**solo se escribe cuando hubo inyección** (`nuevos`, `vetadas` o `respaldo`).

**Es decir: en F y T estoy mirando solo los tics en que la forma sí estaba en la
papeleta.** Que «el candidato no está» salga 3,45 % y 0,00 % **es por
construcción, no un hallazgo.** Las dos columnas no son comparables con K.

Con eso delante, y sobre una muestra pequeña (24 diarios, **9 formas y 87 tics
en F**, **9 formas y 24 tics en T**):

| | **F** (consejero) | **T** (azar) |
|---|---|---|
| gana el paso de la forma | 95,40 % | 75,00 % |
| el cuerpo se mueve | 13,79 % | 41,67 % |
| el cuerpo **se acerca** al destino | 4,60 % | 33,33 % |
| distancia al destino | 3 → 2 | 3 → 3 |
| pierde contra | `move_SW` (1) | `ir_objeto` (6) |

**Y el cruce que pedías, «¿las que cumplieron son las que el cuerpo anduvo?»:**

| (cumple proyección, anduvo) | F | T |
|---|---|---|
| cumplió **y** anduvo | **0** | **1** |
| cumplió **sin** andar | **4** | **3** |
| no cumplió, anduvo | 1 | 1 |
| no cumplió ni anduvo | 2 | 0 |

**En F, ninguna de las cuatro formas que cumplieron la proyección movió al
cuerpo hacia el destino.** En T, una de cuatro.

**Esto apunta a lo que temías** —que el 42,3 % de F y el 61,1 % de T midan otra
cosa que el consejo— **pero con siete y cinco formas no lo afirmo.** Es una
señal, no un resultado.

---

## Lo que no sé, marcado como tal

**Dos conteos de «tics con forma activa» que no cuadran.** P5-8F dio 63.254 y
aquí salen 4.887. La diferencia es de definición: allí conté **todo el intervalo
entre aceptar y terminar**, aquí solo los tics con registro `cur_forma_tic` que
nombra esa forma. **La cifra de P5-8F incluye las 32 formas «sin fin» que viven
1.800 tics**, y ésas inflan el denominador. **Para el punto 1 la buena es la de
aquí**; para P5-8F, el 2,12 % sigue siendo correcto sobre su propia definición,
pero **no debe leerse como «el cuerpo ignora la forma»**, que es lo que yo hice.

**No sé si el 80,52 % es exactamente el enfriamiento.** La aritmética encaja
(10/11 = 90,9 % contra 80,5 % medido) y el veto existe en el código, pero **no
he comprobado tic a tic que el `move_ready_in` fuera el motivo**. Podría haber
otras vetadas mezcladas.

**La muestra de F y T es demasiado pequeña** y además está sesgada. Para decir
algo de verdad sobre si el 42,3 % mide el consejo haría falta rehacerla sobre
los 200 asientos con un registro por tic que F y T no tienen. **Eso no se puede
reconstruir del diario: habría que volver a jugar.**

**Y no sé qué pasaría con el compromiso en un mundo con cazadores.** Las cinco
condiciones duras no dispararon ni una vez en el lento; en S-2 dispararían, y el
69,54 % de obediencia sería otro número.

---

## Lo que esto cambia para las cuarenta

**El diagnóstico de P5-8F era incompleto y lo corrijo:** no es que el cuerpo
ignore la forma, es que **la forma está vetada 8 de cada 10 tics por el
enfriamiento de movimiento**, y cuando compite gana la mitad.

**Eso hace al compromiso más razonable de lo que parecía**, porque el compromiso
actuaría justo en los tics en que hoy la forma no existe: ejecutar el paso de la
forma **aunque el candidato esté vetado**, que es lo que «seguirla por defecto»
significa.

**Propongo, sin hacerlo**, que si se va al compromiso se mida primero, en seco,
**qué pasaría si el paso de la forma se ejecutase también durante el
enfriamiento** — porque ahí está el 80 % del problema, y no sé si el mundo lo
permite (puede que la acción simplemente falle).

---

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1   (idéntico)
```

`cantera/paper5/mide_P58G.py` · datos `P58G_K.json`, `P58G_F.json`,
`P58G_T.json`. **Gasto: cero.**

**PARO AQUÍ.**

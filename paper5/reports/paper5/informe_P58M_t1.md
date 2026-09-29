# P5-8M · TANDA 1 — las diez primeras partidas

**PARO AQUÍ.** Se disparó el suelo de cantidad en cuatro de las cinco semillas.
Las treinta restantes esperan tu sí.

Diez partidas: las dos de la sonda (semilla 20260916, que cuenta como primera —
imagen, tag y políticas verificados contra el registro del servidor) más las
ocho de la tanda 1.

---

## El titular

**Los sellos se han dado la vuelta respecto a todo lo anterior, y a mejor: K1
cumple con holgura, K4 cumple en completadas, y el prometido se ve por primera
vez más de lo que no se ve.** Pero **tres cosas rompen**, y una de ellas es
nueva y no me gusta.

| | |
|---|---|
| **K1** | **1,54** y **3,79×** — **cumple** |
| **completadas** | **62,3 %** (era 39,1 % en la sonda, 6,4 % en P5-8K) |
| **prometido visto durante** | **52,8 %** · nunca **32,6 %** |
| **K3** | **42 decisiones con armado a tiro en forma activa** — **falla** |
| **suelo de cantidad** | **4 de 5 partidas por debajo de 15** — **PARA** |
| **K2, el puesto** | **K peor en 3 semillas, mejor en 1, igual en 1** |

**Y las rupturas del compromiso se han soltado: cuatro causas distintas, 25
veces.** En P5-8H, P5-8I y P5-8K fueron cero de siete causas; aquí disparan
cuatro.

---

## La parada

| semilla | formas aceptadas por la partida de K | |
|---|---|---|
| 20260916 | **23** | ok |
| 20365645 | **7** | **por debajo de 15** |
| 20470374 | **7** | **por debajo de 15** |
| 20575103 | **10** | **por debajo de 15** |
| 20679832 | **6** | **por debajo de 15** |

**Cuatro de cinco por debajo. PARO.**

La sonda dio 23 y parecía sobrada; con cinco semillas se ve que **23 era la
excepción, no la norma**. La mediana de las cinco es **7**.

**El precio no habría parado nada:** máximo **0,01007 $/min** contra el tope de
0,012, mediana 0,00779. Colas de **0,2 a 2,1 minutos**, mediana 0,6.

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

**Imagen comprobada md5 a md5 ANTES de lanzar**, los siete idénticos al acta:
`gemv-anima:curforma-m0`, id `sha256:68faccb5…`, `policy_forma.py` `896e97a0…`,
`curiosidad_forma.py` `141ecb2e…`, `forma_viva.py` `b2c87c93…`.

**La sonda cuenta como primera semilla**, verificado en el registro del
servidor: semilla `20260916` en `game_config`, y las políticas
`gemv-p58m-A:v1`/`gemv-p58m-K:v1` aparecen **dos veces cada una** (asientos 10 y
11) en los dos brazos.

---

## Los siete sellos, acumulado de diez partidas

| | sello | acumulado | |
|---|---|---|---|
| **K1** | K/A ≥ 1,5 **y** dentro ≥ 2× fuera | **1,54** y **3,79×** | **CUMPLE** |
| **K2** | cero muertes dentro; puesto no baja | 0 muertes; **K peor en 3 de 5** | **dudoso** |
| **K3** | cero decisiones con armado a tiro en forma activa | **42** | **FALLA** |
| **K4** | completadas ≥ 50 %; veto duro 5-30 % | **62,3 %**; veto duro **1,9 %** | **ver abajo** |
| **K5** | daño ≤ base de A | **1,9 %** contra **0,6 %** | **FALLA** |
| **K6** | < 5 ms mediana; cero perdidos | **0,56 a 3,14 ms**; **0** | **CUMPLE** |
| **K7** | ≤ 4 $ | 0,778 $ las diez → **3,11 $** proyectado | **CUMPLIRÍA** |

### K1, que es el sello de la serie

| | por 100 tics |
|---|---|
| **K entero** | **12,67** |
| **A entero** | **8,23** |
| **K/A** | **1,54** (sello ≥ 1,5) |
| **dentro de forma** | **43,79** |
| **fuera de forma** | **11,54** |
| **razón** | **3,79×** (sello ≥ 2) |

**Cumple los dos umbrales**, el primero por poco (1,54 contra 1,5) y el segundo
con holgura.

### K4 tiene dos lecturas y no elijo yo

**Completadas 33 de 53 = 62,3 %: cumple el ≥ 50 % con holgura.** Lo que falla es
la banda del veto duro:

| | n | % | banda 5-30 % |
|---|---|---|---|
| veto duro **solo** | 1 | **1,9 %** | **falla** |
| veto duro **+ «sin rodeo»** | 5 | **9,4 %** | **cumple** |

**Las dos son abandono por peligro.** El sello K1-K7 se escribió en P5-8B,
**antes de que «sin rodeo» existiera**: en aquel diseño todo abandono por un
armado se llamaba «veto duro». Hoy ese mismo suceso se reparte en dos nombres.
**Lo digo y no lo decido: la lectura del sello es tuya.**

### K3 falla, y conviene saber de dónde sale

**Los 42 salen de UN asiento**: `K/20470374/11`, 42 de sus 135 tics en forma
(31 %). Los otros nueve asientos dan **cero**.

**Y hay una razón mecánica que hay que poner encima de la mesa:** el compromiso
solo mira las rupturas **cuando las piernas están listas**, es decir **1 de cada
11 tics** (`_compromiso` sale antes si `move_ready_in > 0`). El veto vital
—«armado a tiro»— **vive ahí dentro**. Así que un armado puede estar a tiro
durante diez tics de enfriamiento sin que el mecanismo lo mire, y K3, que cuenta
**tics**, los cuenta todos.

**El mecanismo sí funcionó**: la ruptura «(a) veto vital: armado a tiro» disparó
**3 veces**. **El sello y el mecanismo están midiendo cosas distintas**, y eso no
lo arreglo yo.

### K5 falla por un suceso

**Una forma de 53 (1,9 %) recibió daño mientras vivía**, contra el **0,6 %** de
la base de A en entorno seguro. **Es un suceso.** Con n = 1 no distingo eso del
azar, y lo digo antes de que el número parezca un resultado.

### K2, que es lo que más vigilas

| semilla | K | A | |
|---|---|---|---|
| 20260916 | 16, 12 (med **14**) | 12, 8 (med **10**) | **K peor** |
| 20365645 | 15, 6 (med **10,5**) | 6, 13 (med **9,5**) | **K peor** |
| 20470374 | 13, 11 (med **12**) | 14, 16 (med **15**) | K mejor |
| 20575103 | 13, 15 (med **14**) | 16, 12 (med **14**) | igual |
| 20679832 | 13, 16 (med **14,5**) | 10, 9 (med **9,5**) | **K peor** |

**K peor en 3, mejor en 1, igual en 1.** Cero muertes dentro de forma.

**No lo llamo un resultado y tampoco lo minimizo:** cinco semillas, y la
diferencia mediana donde K pierde es de 4, 1 y 5 puestos. **Es la señal que
pediste vigilar y va en la dirección mala.** Con diez semillas más se sabría.

---

## Lo que va sin sello

### Aceptación por asiento

| asiento | aceptadas | % | W mediana | ventaja mediana | rodeos | sin rodeo |
|---|---|---|---|---|---|---|
| 20260916/10 | 5 / 89 | 5,6 % | 0,000 | −0,00039 | 0 | 0 |
| 20260916/11 | 18 / 76 | 23,7 % | 1,883 | 0,00437 | **1** | 0 |
| 20365645/10 | 4 / 110 | 3,6 % | 1,194 | 0,01027 | 0 | 0 |
| 20365645/11 | 3 / 149 | 2,0 % | 0,617 | 0,01048 | 0 | 0 |
| **20470374/10** | 3 / **5** | **60,0 %** | 0,000 | 0,03348 | 0 | **1** |
| **20470374/11** | 4 / **6** | **66,7 %** | 0,988 | 0,02927 | 0 | 0 |
| 20575103/10 | 5 / 20 | 25,0 % | 1,350 | 0,01647 | 0 | **2** |
| 20575103/11 | 5 / 18 | 27,8 % | 0,000 | 0,01511 | 0 | **1** |
| 20679832/10 | 3 / 36 | 8,3 % | 0,925 | 0,00098 | 0 | 0 |
| 20679832/11 | 3 / 11 | 27,3 % | 1,222 | 0,01060 | 0 | 0 |
| **agregado** | **53 / 520** | **10,2 %** | | | **1** | **4** |

**La dispersión sigue siendo enorme** (2,0 % a 66,7 %) y **la W sigue sin
explicarla**: los dos asientos de más aceptación tienen W 0,000 y 0,988; los dos
de menos, 1,194 y 0,617.

**Y hay algo nuevo: la semilla 20470374 nació 5 y 6 formas en toda la partida**,
contra 89-149 en otras. **No sé por qué.**

### Distancia al nacer × causa de fin

| tramo | n | completada | atasco | veto duro | sin rodeo |
|---|---|---|---|---|---|
| **1-3** | 8 | **8 (100 %)** | 0 | 0 | 0 |
| 4-5 | 28 | 12 (42,9 %) | **13 (46,4 %)** | 1 | 2 |
| **6-7** | 15 | **11 (73,3 %)** | 2 (13,3 %) | 0 | 2 |
| **8-9** | 2 | **2 (100 %)** | 0 | 0 | 0 |

**El muro de P5-8L ha desaparecido.** Allí el tramo 8-9 daba **100 % de veto
duro y 0 % de llegadas**; aquí las dos formas de 8-9 **completan las dos**. El
cuello es ahora el tramo **4-5**, por atasco.

### El rodeo

| | |
|---|---|
| formas que rodearon | **1 de 53** |
| casillas extra | +2 |
| completan: rodearon | **1 / 1** |
| completan: no rodearon | 32 / 52 = 61,5 % |
| abandonos por **«sin rodeo»** | **4** |

**El rodeo sigue casi sin usarse**, y ahora se ve por qué: **los encuentros con
un armado cubriendo el camino son raros en este mundo** — 5 en 53 formas. De
esos 5, uno tuvo rodeo y cuatro no. **Con n=1 el rodeo sigue sin estar
probado.**

### El compromiso, y las rupturas sueltas

| | |
|---|---|
| tics con piernas listas | 221 |
| **obedece** | **196 = 88,7 %** |
| **rompe** | **25** |
| contra el criterio del decisor | **153 = 78,1 %** |
| coste | **+25,922 · +0,1694 por tic** |

| causa | n |
|---|---|
| **(e) rival a 2 o menos** | 14 |
| **(d) carencia sube (pierde de las manos)** | **7** |
| **(a) veto vital: armado a tiro** | **3** |
| **(e) armado a menos de 6 y acercándose** | 1 |

**Cuatro de las siete causas disparan.** En P5-8H, P5-8I y P5-8K no disparó
ninguna. Siguen sin verse (b) veto duro, (c) daño recibido y (f)/(g).

### Lo prometido contra lo visto

**1.615 durante (52,8 %) · 446 después (14,6 %) · 996 nunca (32,6 %)**

Por primera vez en la serie **se ve más de lo que no se ve**. La progresión:
P5-8F 16,7 / 6,3 / **76,9** → P5-8K 2,8 / 0,9 / **96,3** → sonda 39,9 / 19,4 /
40,7 → **aquí 52,8 / 14,6 / 32,6**.

Distancia al destino: **4 → 2**.

### W en las manos, y el botín

| | |
|---|---|
| W mediana al nacer → al terminar | **0,6667 → 1,0000** |
| sube en | **1** forma |
| baja en | **2** |
| **igual en** | **50 de 53** |

**La forma casi nunca mueve la riqueza.** La mediana sube de 0,67 a 1,00, pero
eso es efecto de qué formas empiezan y acaban dónde, no de un cambio: **en 50 de
53 la W es idéntica al empezar y al terminar.**

| botín | recogidas | tics | por 100 tics |
|---|---|---|---|
| **dentro de forma** | 14 | 2.046 | **0,684** |
| fuera | 108 | 56.625 | **0,191** |

**3,6 veces más recogidas por tic dentro de forma.** En la sonda salió 13×; con
diez partidas baja a 3,6×. **Sigue siendo señal, no resultado** (14 sucesos).

### «Acerca al armado» en inseguro

| | tics con armado a la vista | acerca | |
|---|---|---|---|
| **K** | 22.619 | 259 | **1,1 %** |
| **A** | 32.803 | 781 | **2,4 %** |

**K se acerca la mitad que A.** En la sonda fue 0,42 % contra 3,51 %; con diez
partidas la diferencia se estrecha pero mantiene el signo.

---

## Precio

| partida | precio | cola | juego | $/min |
|---|---|---|---|---|
| A/20260916 | 0,054920 | 2,0 | 8,5 | 0,00519 |
| K/20260916 | 0,071258 | 2,1 | 10,3 | 0,00571 |
| A/20365645 | 0,058615 | 0,2 | 10,3 | 0,00559 |
| A/20470374 | 0,098732 | 0,3 | 9,6 | 0,00996 |
| A/20575103 | 0,094988 | 0,6 | 9,1 | 0,00987 |
| A/20679832 | 0,109952 | 0,7 | 10,2 | 0,01002 |
| K/20365645 | 0,086349 | 0,3 | 8,3 | **0,01007** |
| K/20470374 | 0,041118 | 0,4 | 9,0 | 0,00437 |
| K/20575103 | 0,117432 | 0,6 | 11,1 | 0,01003 |
| K/20679832 | 0,044697 | 0,7 | 7,4 | 0,00548 |

**Total 0,778061 $ · $/min mediana 0,00779, máximo 0,01007** (tope 0,012).
**Ninguna se acercó a la vara.** Colas de 0,2 a 2,1 min, mediana 0,6.

**K7 proyectado a cuarenta partidas: 3,11 $**, bajo el techo de 4 $.

---

## Lo que no sé, marcado como tal

**No sé por qué la semilla 20470374 nació 5 y 6 formas** cuando otras nacen 110
y 149. Es un factor de veinte y no tengo explicación.

**No sé por qué la aceptación va del 2 % al 67 % entre asientos.** La riqueza
sigue sin explicarlo, y ahora con diez asientos apunta al revés que en P5-8E.

**El rodeo sigue sin probarse.** Una de 53. Lo que está medido en seco (59 % de
los vetos tendrían rodeo con colchón cero) sigue sin poder contrastarse en
campo, porque **en este mundo casi no hay encuentros de ese tipo**.

**K5 y K3 fallan por sucesos concentrados**: K5 por **un** caso, K3 por **un**
asiento. No los llamo resultados.

**Y K2 es lo que más me preocupa**, como a ti. Tres de cinco semillas con K por
debajo, y la sonda ya lo había apuntado. **No es concluyente y va en la
dirección mala.**

---

## Propuesta, no ejecución

**El diseño funciona mejor que nunca**: K1 cumple, las completadas pasan del
62 %, el muro de distancia desapareció, y el cuerpo ve más de la mitad de lo que
promete. **Pero el suelo de cantidad no se sostiene**: la sonda dio 23 y las
otras cuatro dieron 6, 7, 7 y 10.

Tres cosas que dejo en la mesa **sin decidir**:

1. **El suelo de cantidad por partida** parece demasiado alto para este mundo.
   Las diez partidas dieron **53 formas**; a ese ritmo las cuarenta darían
   **~210**, que es n de sobra para todos los sellos.
2. **La lectura de K4**: si «sin rodeo» cuenta como abandono por peligro, K4
   cumple entero.
3. **K3 cuenta tics que el mecanismo no mira** (los diez de enfriamiento por
   cada uno con piernas listas). O se cuenta por forma, o se acepta que mide
   otra cosa.

**El suelo, la lectura de los sellos y seguir o no son tuyos.**

**Gasto de la tanda: 0,778061 $.** Cola vacía al acabar. **Las treinta restantes
no se han lanzado.**

**PARO AQUÍ.**

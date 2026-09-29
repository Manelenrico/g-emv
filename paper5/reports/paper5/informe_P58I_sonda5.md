# P5-8I — Cinco semillas con la imagen de P5-8H, sin cambios

**PARO AQUÍ.** Las cuarenta siguen esperando el sí.

**Y PARO ADEMÁS POR PRECIO:** ocho de las diez partidas salieron de la horquilla
0,04-0,08 que pusiste. No lancé nada más.

---

## El titular

**Ha ocurrido el caso que llevaba cuatro sondas sin verse: el cuerpo obedeció a
la forma CONTRA el criterio del decisor, 23 veces, y ahora sé lo que cuesta.**

| | |
|---|---|
| obediencia con piernas listas | **50 de 50 = 100 %** |
| **tics obedecidos contra el ganador del decisor** | **23 = 46 % de las obediencias** |
| **coste de esos tics** | **+3,993 de `d` en total · +0,1736 por tic** |
| rupturas | **0**, ninguna de las siete causas, en seis asientos |

El seco de P5-8G estimó ese coste en **+0,100 por tic**. El campo dice
**+0,174**: **el compromiso cuesta casi el doble de lo que el seco predijo.**

**Y el signo de la exploración se da la vuelta.** Dos sondas seguidas decían que
dentro de la forma se ve **menos**. Ahora, con 448 tics dentro repartidos en seis
asientos: **50,89 casillas nuevas por cien tics dentro contra 6,78 fuera.**
Siete de cada diez formas se completan por alivio, la distancia va de **5 a 1**,
y lo prometido se ve: **77,6 % durante · 4,5 % después · 17,9 % nunca** — contra
el **16,7 / 6,3 / 76,9** de P5-8F.

**Pero la aceptación es el cuello, y ahora tiene tamaño:** **10 aceptadas de
1.030 propuestas = 1,0 %**, con **cuatro de diez asientos aceptando cero**. Y el
contrafactual dice de dónde sale ese 1 %: **con margen 0,04 habrían pasado 273 y
con 0,02, 471.** El margen en vigor (0,062) es lo que deja la serie sin n.

**Un hallazgo que desmiente lo que yo venía escribiendo:** el precio **no depende
del brazo**. Los dos brazos de cada semilla cuestan casi lo mismo
(0,109/0,098 · 0,108/0,093 · 0,111/0,112 · 0,032/0,030). **Las tres sondas en que
dije que «K cuesta el doble» medían la semilla, no la curiosidad.**

---

## Custodia

La imagen se comprobó **antes de lanzar**, md5 a md5 contra el acta de P5-8H.

```
                            al empezar                         al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1   idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252   idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640   idéntico
```

| dentro de la imagen | acta P5-8H | comprobado |
|---|---|---|
| `policy_forma.py` | `891cea92a87d4866155221023e09615b` | **idéntico** |
| `curiosidad_forma.py` | `4d2ef856a45d1b890b7135036bcd69ef` | **idéntico** |
| id de la imagen | `sha256:6afe40f83aeab…` | **idéntico** |

Etiqueta `gemv-anima:curforma-h0`, políticas `gemv-p58h-A:v1` y `gemv-p58h-K:v1`,
**las mismas**. Ni una línea tocada.

### El medidor, validado antes de usarlo

Antes de que llegaran los diarios nuevos corrí `mide_P58I.py` **sobre la sonda de
P5-8H ya publicada**. Reprodujo sus cifras sin desviación: 85 nacidas / 1
aceptada, 155 / 0, obedece 5, rompe 0, **110,20 dentro contra 6,90 fuera**, W
1,25, prometido **76 · 9 · 0**, completada por alivio, 5 → 1.

Y el contrafactual del margen tiene su propio control: **alimentado con el margen
en vigor devuelve 10 aceptadas, que son exactamente las 10 reales.** Por eso los
273 y los 471 de abajo se pueden creer.

---

## 1 · Aceptación y dispersión entre asientos

| asiento | tics | nacidas | **aceptadas** | % | W mediana | amenaza |
|---|---|---|---|---|---|---|
| 20260916/10 | 8.349 | 53 | **2** | 3,8 % | 1,500 | 0,143 |
| 20260916/11 | 8.307 | 137 | **2** | 1,5 % | 0,667 | 0,0 |
| 20365645/10 | 9.181 | 127 | **0** | 0,0 % | 1,222 | 0,0 |
| 20365645/11 | 11.562 | 159 | **0** | 0,0 % | 0,778 | 0,0 |
| 20470374/10 | 14.496 | 128 | **0** | 0,0 % | 2,000 | 0,0 |
| 20470374/11 | 14.496 | 46 | **1** | 2,2 % | 2,067 | 0,0 |
| 20575103/10 | 8.387 | 85 | **1** | 1,2 % | 1,075 | 0,0 |
| 20575103/11 | 2.188 | 15 | **3** | **20,0 %** | 0,000 | 0,0 |
| 20679832/10 | 9.204 | 141 | **1** | 0,7 % | 1,000 | 0,0 |
| 20679832/11 | 10.886 | 139 | **0** | 0,0 % | 0,667 | 0,0 |
| **AGREGADO** | **97.056** | **1.030** | **10** | **1,0 %** | 1,038 | 0,0 |

**Dispersión de la tasa: 0,00 % · mediana 0,94 % · 20,00 %.** Cuatro de diez
asientos aceptan cero.

**La explicación de P5-8E —el asiento rico acepta menos— NO se sostiene con diez
asientos.** Spearman entre W y tasa de aceptación: **ρ = −0,14**, que con n = 10
es ruido. El asiento más pobre (W = 0) acepta el 20 %, pero el segundo más rico
(W = 2,067) acepta el 2,2 % mientras uno de W = 0,778 acepta cero. **Lo que en
P5-8E parecía la riqueza era la diferencia entre dos asientos; con diez se
deshace.** Lo retiro.

**La amenaza mediana es cero en nueve de los diez asientos.** No es el peligro.

---

## 2 · El margen, contrafactual y gratis

Leído de `forma_evaluada` (`ventaja` contra `margen`), sin tocar nada vivo. Las
rechazadas por **vida** no las rescata ningún margen, y se descuentan.

| asiento | evaluadas | por vida | **vigente** | **0,04** | **0,02** |
|---|---|---|---|---|---|
| 20260916/10 | 53 | 0 | 2 | 12 | 46 |
| 20260916/11 | 137 | 0 | 2 | **115** | 131 |
| 20365645/10 | 127 | 0 | 0 | 5 | 56 |
| 20365645/11 | 159 | 6 | 0 | 11 | 61 |
| 20470374/10 | 128 | 0 | 0 | **0** | 2 |
| 20470374/11 | 46 | 0 | 1 | 2 | 14 |
| 20575103/10 | 85 | 7 | 1 | 1 | 11 |
| 20575103/11 | 15 | 0 | 3 | 7 | 11 |
| 20679832/10 | 141 | 0 | 1 | **119** | 132 |
| 20679832/11 | 139 | 8 | 0 | 1 | 7 |
| **AGREGADO** | **1.030** | **21** | **10** | **273** | **471** |

**Con margen 0,04 pasarían 27 veces más formas; con 0,02, 47 veces más.** El
margen en vigor tiene mediana **0,0620** (rango 0,0620-0,0710).

**Y la dispersión entre asientos no desaparece al bajar el margen, se recoloca:**
con 0,04, el asiento 20470374/10 sigue en **cero de 128** mientras 20679832/10
pasa de 1 a **119**. Bajar el margen daría n, pero **la repartiría muy desigual**.

**Nada de esto se ha cambiado en vivo.** Es lectura del diario.

---

## 3 · El compromiso, en las que corrieron

| asiento | piernas listas | **obedece** | rompe | % | **CONTRA** | **coste** | enfriamiento |
|---|---|---|---|---|---|---|---|
| 20260916/10 | 6 | 6 | 0 | 100 % | 2 | +0,2149 | 57 |
| 20260916/11 | 7 | 7 | 0 | 100 % | 4 | +0,8721 | 69 |
| 20470374/11 | 3 | 3 | 0 | 100 % | **0** | +0,0000 | 29 |
| 20575103/10 | 6 | 6 | 0 | 100 % | 2 | +0,5118 | 54 |
| 20575103/11 | 22 | 22 | 0 | 100 % | **12** | +1,6048 | 130 |
| 20679832/10 | 6 | 6 | 0 | 100 % | 3 | +0,7892 | 59 |
| **AGREGADO** | **50** | **50** | **0** | **100 %** | **23** | **+3,9928** | **398** |

### Los 23 tics contra el criterio — el caso que faltaba

**23 de las 50 obediencias (46 %) fueron contra el ganador del decisor.** Coste
**+3,9928 de `d`**, es decir **+0,1736 por tic**.

Para ponerlo en escala: la `d` típica del cuerpo ronda 3-4, así que cada tic
desobedecido cuesta **unas cinco centésimas de la `d` total**. **No es gratis y
no es ruinoso** — pero es **1,7 veces lo que el seco de P5-8G predijo** (+0,100),
y eso importa: el seco subestimaba porque simulaba sobre tics en que la forma ya
competía, y el compromiso actúa sobre todos.

**Las 398 de enfriamiento** confirman el diagnóstico de P5-8G: por cada tic con
piernas listas hay **ocho** sin ellas (398/50), coherente con los 11 tics por
casilla.

### Rupturas

**Cero, de las siete causas, en seis asientos y 50 tics.** Sigue sin haber
evidencia de campo de que (a), (b), (c), (d), (f) ni (g) funcionen. **Es el mismo
agujero que declaré en P5-8H, ahora con seis veces más ocasiones y el mismo
resultado.**

*(Nota: una forma cayó por **veto duro**, pero eso es la caída de la forma —
mecanismo distinto—, no una ruptura del compromiso.)*

### Las diez formas aceptadas, una a una

| asiento | vive | d₀ | d₁ | objetivo | durante | después | **nunca** | motivo |
|---|---|---|---|---|---|---|---|---|
| 20260916/10 | 33 | 3 | **1** | 81 | 72 | 4 | 5 | completada por alivio |
| 20260916/10 | 32 | 3 | **1** | 73 | 60 | 4 | 9 | completada por alivio |
| 20260916/11 | 44 | 5 | **1** | 84 | 68 | 3 | 13 | completada por alivio |
| 20260916/11 | 34 | 2 | 3 | 9 | 0 | 0 | 9 | **atasco** |
| 20470374/11 | 14.395 | 2 | 4 | 69 | 69 | 0 | **0** | **sin fin** |
| 20575103/10 | 61 | 6 | **1** | 103 | 92 | 10 | 1 | completada por alivio |
| 20575103/11 | 52 | 6 | 2 | 65 | 4 | 7 | **54** | **veto duro** |
| 20575103/11 | 51 | 5 | **1** | 54 | 44 | 0 | 10 | completada por alivio |
| 20575103/11 | 52 | 5 | **1** | 7 | 4 | 0 | 3 | completada por alivio |
| 20679832/10 | 66 | 6 | **1** | 93 | 82 | 1 | 10 | completada por alivio |

**Completadas por alivio 7 · atasco 1 · veto duro 1 · sin fin 1.** En P5-8D eran
50 de 51 por atasco; el atasco en pasos lo arregló y **aquí ya no manda**.

**Distancia: mediana 5 al nacer → 1 al terminar.** Siete de diez llegan a una
casilla del destino.

**Lo prometido contra lo visto, agregado: 495 durante (77,6 %) · 29 después
(4,5 %) · 114 nunca (17,9 %).** En P5-8F era 16,7 / 6,3 / **76,9**. **El «nunca»
baja de tres cuartas partes a menos de una quinta.**

**Queda una forma «sin fin»** (20470374/11, viva 14.395 tics). Es el agujero que
ya señalé en P5-8F y sigue sin taparse.

---

## 4 · Casillas nuevas por cien tics, dentro y fuera — informado, **no sellado**

| | tics dentro | tics fuera | **/100 DENTRO** | /100 fuera |
|---|---|---|---|---|
| K 20260916/10 | 63 | 8.286 | **115,87** | 6,83 |
| K 20260916/11 | 76 | 8.231 | **34,21** | 7,14 |
| K 20470374/11 | 32 | 14.464 | **46,88** | 5,47 |
| K 20575103/10 | 60 | 8.327 | **101,67** | 7,45 |
| K 20575103/11 | 152 | 2.036 | **3,29** | **30,80** |
| K 20679832/10 | 65 | 9.139 | **73,85** | 6,34 |
| **K AGREGADO** | **448** | **96.608** | **50,89** | **6,78** |
| **A AGREGADO** | **0** | **57.545** | — | **10,31** |

*(Los cuatro asientos de K sin aceptadas y los diez de A no tienen tics dentro.)*

**Cinco de seis asientos dicen que dentro de la forma se ve mucho más.** El sexto
(20575103/11) dice lo contrario, y **tiene una explicación que vale la pena
mirar**: ese asiento vivió solo 2.188 tics, y **los primeros tics de una vida son
los que más descubren**, así que su «fuera» (30,80) está inflado por el arranque.
El mismo efecto se ve en A: los asientos que murieron pronto dan 115,42 y 153,78
por cien tics fuera, contra 4-8 en los que vivieron.

**Por eso el número de A hay que leerlo con cuidado: su 10,31 agregado está
empujado por tres asientos de vida corta.** Los asientos de A de vida larga dan
**4,2 a 8,0**, que es donde está también el «fuera» de K.

**Esto invierte lo que dos sondas venían diciendo** (0,41 y 1,35 dentro contra
8,87 y 8,66 fuera). La diferencia es de mecanismo, no de medida: allí las formas
morían de atasco sin llegar a ninguna parte; aquí **siete de diez llegan**.

---

## 5 · Precio de cada partida, con cola y juego

| partida | precio | cola | juego | |
|---|---|---|---|---|
| A/20260916 | 0,109143 $ | 0,5 min | 10,5 min | **fuera** |
| A/20365645 | 0,108293 $ | 0,6 | 10,3 | **fuera** |
| A/20470374 | 0,110673 $ | 0,8 | 10,2 | **fuera** |
| A/20575103 | 0,032359 $ | 0,9 | 10,2 | **fuera, por abajo** |
| A/20679832 | **SIN FACTURAR** | 1,1 | 10,4 | `cost_usd = null` |
| K/20260916 | 0,098433 $ | 0,4 | 9,6 | **fuera** |
| K/20365645 | 0,092653 $ | 0,7 | 8,6 | **fuera** |
| K/20470374 | 0,111693 $ | 0,6 | 10,6 | **fuera** |
| K/20575103 | 0,030153 $ | 1,0 | 9,4 | **fuera, por abajo** |
| K/20679832 | 0,075778 $ | 1,2 | 10,5 | dentro |

**Ocho de diez fuera de la horquilla. PARÉ:** ninguna petición más. **No había
nada que cancelar** — las diez ya estaban `running` cuando saltó el primer aviso,
ninguna en `submitted`, y por tu criterio las que corren se dejan acabar.

### El precio sigue a la semilla, no al brazo

| semilla | A | K |
|---|---|---|
| 20260916 | 0,109143 | 0,098433 |
| 20365645 | 0,108293 | 0,092653 |
| 20470374 | 0,110673 | 0,111693 |
| **20575103** | **0,032359** | **0,030153** |
| 20679832 | sin facturar | 0,075778 |

**Los dos brazos de cada semilla cuestan casi lo mismo, y la semilla 20575103
cuesta 3,5 veces menos en los dos.** La cola no lo explica (0,4-1,2 min en todas)
ni el juego (8,6-10,6 min en todas).

**Esto desmiente lo que escribí en tres sondas.** Venía diciendo «K cuesta el
doble y no sé por qué» (0,1076 · 0,0559 · 0,1008 · 0,0443). **Con cinco semillas
se ve que la variación es del episodio, no del brazo:** en esta tanda **A sale
más caro que K en tres de las cuatro semillas facturadas.** La curiosidad-forma
no es cara. **Retiro esa observación de las tres sondas anteriores.**

**Gasto: 0,769178 $ facturados** (nueve partidas), frente a los ~0,45 estimados.
**La estimación estaba mal por un factor de casi dos**, y la causa es que la
hice con el precio de P5-8H (0,043) cuando ese precio era el de una semilla
barata, no la media.

### El episodio sin facturar

`A/20679832` vuelve **`completed` con `cost_usd = null`**, reconsultado después de
acabar. Es el **segundo** de la serie (hubo uno en P5-6C). No lo cuento en el
gasto y lo dejo señalado.

---

## Lo que no sé, marcado como tal

**No sé si el 100 % de obediencia se sostendría con rupturas activas.** Cincuenta
tics sin que ninguna de las siete causas dispare es o un mundo sin peligro o un
mecanismo que no se enciende, y **no lo separo**. El humo prueba que (e)
discrimina; el campo no ha dado la ocasión, ni aquí ni en P5-8H.

**No sé por qué la aceptación es del 1 %.** El contrafactual dice **cuánto** la
sube bajar el margen, no **si debe bajarse**. El margen es de la puerta ancha y
la puerta ancha es lo que da honestidad a toda la serie; tocarlo para que salgan
más formas sería mover la vara. **No lo propongo: lo mido y lo dejo en la mesa.**

**No sé por qué cuatro asientos aceptan cero y uno acepta el 20 %.** Descarté la
riqueza (ρ = −0,14) y la amenaza (cero en nueve de diez). **Me quedo sin
hipótesis**, y es la tercera sonda que esa asimetría aparece sin explicarse.

**El asiento del 20 % es el que menos vivió** (2.188 tics, 15 formas, 3
aceptadas). **Con 15 propuestas, ese 20 % puede ser azar.**

**No sé por qué el precio varía 3,5 veces entre semillas** con la misma cola y el
mismo juego. Lo que sí sé ahora es **que no es el brazo**, y eso es más de lo que
sabía ayer.

**Las diez formas siguen siendo diez.** El 77,6 % de «durante», el 5 → 1, el
50,89 contra 6,78: todo eso sale de **diez formas en seis asientos**. Es diez
veces más que P5-8H, y sigue sin ser una muestra.

---

## Lo que esto cambia para las cuarenta — propuesta, no ejecución

**Por primera vez el mecanismo se ve funcionar entero:** nace, se acepta, el
cuerpo la obedece —incluso contra su propio criterio—, llega, y ve lo que
prometió. Los cuatro relojes que arreglé (examen, atasco en pasos, compromiso,
paso del mundo) **han dado el resultado que buscaban**.

**Pero las cuarenta seguirían sin potencia, y ahora tengo el número:** con **1,0 %
de aceptación**, cuarenta partidas darían del orden de **40 formas** — cuatro
veces esta sonda. Suficiente para K4 y K6; **muy justo para K1**, que se mediría
sobre los pocos asientos que acepten.

**Y hay un dato nuevo que cambia el presupuesto:** a **0,085 $ de media** (no
0,043), las cuarenta costarían **~3,4 $**, no los ~2,2 que proyecté en P5-8D.
Sigue bajo el techo de 4 $ de K7, **pero con poco margen**.

**Lo que yo haría, y no hago:** decidir primero si el margen de la puerta se
toca. Si se queda en 0,062, las cuarenta miden un mecanismo que funciona sobre
una muestra que no da; si baja a 0,04, la misma sonda habría dado **273 formas**
y las cuarenta sobrarían. **Es una decisión de vara, y la vara es de la mesa.**

---

`cantera/paper5/lanza_P58I.py` · `recoge_P58I.py` · `baja_P58I.py` ·
`mide_P58I.py` · datos `P58I.json`, control `P58I_control_H.json` · veinte
diarios en `paintball/runs/P58I_t1_*`.

**Sellos K1 a K7 siguen cerrados para las cuarenta.**

**PARO AQUÍ.**

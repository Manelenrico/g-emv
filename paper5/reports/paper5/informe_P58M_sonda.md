# P5-8M — Rodear en vez de abandonar · LA SONDA

**PARO AQUÍ.** Se disparó tu condición de parada por aceptación. Las cuarenta no
se han lanzado.

---

## El titular

**Es la mejor sonda de la serie, y para por el único umbral que no mira lo que
mejoró.**

| | P5-8K (abandona) | **P5-8M (rodea)** |
|---|---|---|
| **aceptación** | 42,6 % | **13,9 %** ← **para** |
| **completadas** | 6,4 % | **39,1 %** |
| muertas por **veto duro** | **93,6 %** | **4,3 %** |
| lo prometido, **visto durante** | 2,8 % | **39,9 %** |
| lo prometido, **nunca visto** | 96,3 % | **40,7 %** |
| distancia al nacer → al terminar | 8 → 7 | **4 → 2** |
| **K1** (K/A ≥ 1,5 · dentro ≥ 2× fuera) | 1,05 · 1,09 | **1,52 · 2,71 — cumpliría** |

**Y por primera vez en toda la serie una ruptura del compromiso dispara en el
campo: 14 veces, todas por «(e) rival a 2 o menos».** En P5-8H, P5-8I y P5-8K
fueron cero. El compromiso deja de ser 100 % de obediencia ciega y pasa a
**87,2 %**: obedece 95 tics y rompe 14.

**Pero el rodeo apenas se usó: 1 de 23 formas rodeó.** No porque no funcione
—esa rodeó y **completó**— sino porque **el veto duro casi no se disparó**: en
P5-8K hubo 102 encuentros con un armado cubriendo el camino; aquí hubo **dos**.
El cuerpo recorrió otro mundo.

---

## La parada

| condición | umbral | sonda | |
|---|---|---|---|
| **aceptación** | ≥ 20 % | **13,9 %** (23 de 165) | **PARA** |
| completadas sobre aceptadas | ≥ 30 % | **39,1 %** | cumple |
| decisiones con armado a tiro en forma activa | **0** | **0** | cumple |

**Paré: no se lanzó la tanda 1.**

**Y el precio, con tu vara nueva, no habría parado nada:**

| brazo | precio | cola | juego | **$/min** |
|---|---|---|---|---|
| A | 0,054920 $ | 2,0 min | 8,5 min | **0,00519** |
| K | 0,071258 $ | 2,1 min | 10,3 min | **0,00571** |

Tope 0,012 $/min. **Las dos muy por debajo.** La vara por minuto funciona y la
cola volvió a la normalidad (2 min contra los 8,8 de P5-8K).

---

## La regla del colchón, medida antes de construir

Tu regla era: medir el rodeo con colchón de una casilla, y si llega al 40 % usar
ése; si no, colchón cero.

| regla del BFS del rodeo | hay rodeo | cabe en 1,5× | extra |
|---|---|---|---|
| **colchón 1** (`d ≤ alcance + 1`) | **1 / 103 = 1,0 %** | 1 | +2 |
| **colchón 0** (`d ≤ alcance`) | **61 / 103 = 59,2 %** | **60 = 58,3 %** | **+1** |

**1,0 % < 40 % → colchón cero.** Medido sobre los 103 vetos duros reales de
P5-8I y P5-8K.

**Un dato que conviene tener claro: «colchón 1» es aritméticamente la misma
condición que el `alcance + 2` de P5-8A**, porque con distancias enteras
`d < rg + 2` ⟺ `d ≤ rg + 1`. Por eso da el mismo 1,0 %. **No había escalón
intermedio: la regla salta de 1 % a 59 % de golpe.** También medí la variante
que conserva la cláusula «más cerca del armado que del cuerpo»: **igual, 1,0 %**.

**La sombra del NACIMIENTO no se ha tocado.** `camino_a_frontera` sigue con
`en_sombra` entera (alcance + 2, o más cerca del armado que del cuerpo). El
rodeo tiene su propia tapa, `COLCHON_RODEO = 0`, y va declarada en el código
junto a las dos cifras.

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

### La imagen

| | |
|---|---|
| etiqueta | **`gemv-anima:curforma-m0`** |
| id | `sha256:68faccb52f23415012f2d596f9d12a2943c4cf157bc27eb457f046aab234f7a4` |

md5 dentro: `policy_forma.py` **`896e97a0cca1efcb736596e0b8b15cea`** ·
`curiosidad_forma.py` **`141ecb2eb17f76654caf4bbf3c29c642`** · `forma_viva.py`
**`b2c87c93f0ed47e48fd8991a5a797a42`** · `humo_curforma.py`
`1660fb118bb2287f036bdb02c74fc11e` · `forma.py` `b801876afda071403c5af54a28feff85`
(**sin tocar**) · `confianza_viva.py` `6e1e444435914f0b9df287ea37555bbc`
(**sin tocar**).

Políticas `gemv-p58m-A:v1` (`939269d2-…`) y `gemv-p58m-K:v1` (`68e4de97-…`).

---

## Dos cosas que tuve que resolver, y que declaro

**1 · El rodeo habría sido cosmético.** La receta de una forma es
`{"tipo": "ir", "destino": …}`, y el `ir` busca **su propio** camino: cambiar
`k_camino` no habría cambiado por dónde anda el cuerpo — se habría vuelto a
meter por la sombra. Añadí `fv.desvio` en `forma_viva.py`: cuando la forma va
rodeando, el cuerpo apunta a **la casilla siguiente del rodeo**, refrescada cada
tic. **La promesa no cambia**: `tramos` y `destino_cur` siguen siendo el destino
final, y la puerta sigue juzgando eso. Sin `desvio` el atributo no existe y
`destino_actual()` es idéntico a lo de siempre — el humo del apagado lo
comprueba (200/200).

**2 · Al rodear se reinicia el reloj del atasco.** Sin eso el rodeo moriría por
atasco **por construcción**: alejarse tres casillas del destino son 33 tics, que
es el plazo entero. **Es consecuencia de tu encargo, no una decisión nueva**,
pero es un cambio de comportamiento y no quiero que vaya escondido.

---

## El humo

```
  (a) APAGADO identico: 200/200 decisiones · 0 registros de curiosidad-forma
  (i) rodeo: COLCHON_RODEO=0 · TOPE_RODEO=1.5 · sombra del nacimiento intacta
      (a) lancero QUIETO en (22,16) (alcance 2, a 8 del cuerpo, toca el camino=True):
          vive=True rodeos=1 largo 8 -> 8 · desvio (24,23)
      (b) lancero pegado al destino (24,17): vive=False · motivo 'sin rodeo: …'
      (c) el MISMO lancero ACERCANDOSE (antes 9, ahora 8): vive=False · 'veto duro: …'
```
Más los de P5-8K, todos verdes. **Corren dentro del build y lo tumbarían.**

---

## La sonda

### Aceptación y rodeos, por asiento

| asiento | aceptadas | % | **rodeos** | **sin rodeo** | W mediana | ventaja mediana |
|---|---|---|---|---|---|---|
| K/10 | 5 / 89 | 5,6 % | **0** | 0 | 0,000 | **−0,00039** |
| K/11 | 18 / 76 | 23,7 % | **1** | 0 | 1,883 | 0,00437 |
| **agregado** | **23 / 165** | **13,9 %** | **1** | **0** | | |

**La aceptación cayó del 42,6 % de P5-8K al 13,9 % con el mismo margen 0,02.**
La causa es la de siempre y ya está medida en P5-8J: **la aceptación sigue a los
diarios**. El cuerpo va por otro sitio, los estados son otros, y la ventaja
mediana bajó de 0,00746 y 0,02769 a **−0,00039 y 0,00437**.

### El rodeo, donde llegó a usarse

| | |
|---|---|
| formas que rodearon | **1 de 23** |
| casillas extra | **+2** |
| **de las que rodearon, completan** | **1 / 1 = 100 %** |
| de las que NO rodearon, completan | 8 / 22 = 36,4 % |
| abandonos por **«sin rodeo»** | **0** |

**El rodeo funcionó donde se usó, pero n = 1.** No afirmo nada con eso.

**Lo que sí es un hecho: los encuentros con un armado cubriendo el camino pasaron
de 102 (P5-8K) a 2.** Uno acabó en rodeo y otro en veto duro porque el armado se
acercaba — que es exactamente la regla que pediste.

### Causa de fin, y por distancia al nacer

| motivo | n |
|---|---|
| **completada por alivio** | **9** |
| **atasco** | **13** |
| veto duro | 1 |

| tramo | n | completada | atasco |
|---|---|---|---|
| 1-3 | 1 | 100 % | 0 % |
| **4-5** | **21** | **33,3 %** | **62 %** |
| 6-7 | 1 | 100 % | 0 % |

**El cuello ha cambiado de sitio: ya no es el veto duro, es el atasco.**
Y las aceptadas vuelven a nacer cerca (mediana **5**, máximo 7) en vez del 8 de
P5-8K.

### El compromiso, y las primeras rupturas de la serie

| | |
|---|---|
| tics con piernas listas | 109 |
| **obedece** | **95 = 87,2 %** |
| **rompe** | **14** — todas por **«(e) rival a 2 o menos»** |
| contra el criterio del decisor | **75 = 78,9 %** de las obediencias |
| coste | **+9,872 total · +0,1316 por tic** |

**Es la primera vez en cuatro sondas que una ruptura dispara en el campo.** Seis
de las siete causas siguen sin verse nunca; la séptima, por fin, sí.

### Lo prometido contra lo visto

**433 durante (39,9 %) · 210 después (19,4 %) · 442 nunca (40,7 %).**

Contra el 2,8 / 0,9 / **96,3** de P5-8K y el 16,7 / 6,3 / **76,9** de P5-8F.
**Es el mejor reparto medido en la serie.**

---

## Los siete sellos, anticipados

| | sello | la sonda | |
|---|---|---|---|
| **K1** | K/A ≥ 1,5 **y** dentro ≥ 2× fuera | **1,52** y **2,71** | **cumpliría** |
| **K2** | cero muertes dentro; puesto no baja de mediana | 0 muertes; **puestos K 16 y 12 contra A 12 y 8** | **dudoso** |
| **K3** | cero decisiones con armado a tiro en forma activa | **0** | cumple |
| **K4** | completadas ≥ 50 %; veto duro 5-30 % | **39,1 %**; veto duro **4,3 %** | **fallaría, por poco** |
| **K5** | daño ≤ base de A | **0 de 23 formas** con daño mientras vivían | cumple |
| **K6** | < 5 ms mediana; cero perdidos | **3,139 y 0,988 ms**; 0 perdidos | cumple |
| **K7** | ≤ 4 $ | a 0,063 $/partida → **~2,5 $** | cumpliría |

**K1 cumpliría por primera vez en la serie**, y por poco (1,52 contra 1,5).
**K4 fallaría por poco** y ahora por el atasco, no por el veto.

**K2 me preocupa y lo señalo:** los dos asientos de K acabaron **por debajo** de
los dos de A (16 y 12 contra 12 y 8). **Con una partida es ruido**, pero es el
primer indicio de que la curiosidad cueste puesto.

---

## Lo que va sin sello

### W en las manos, al empezar y al terminar cada forma

**Las 23 formas terminan con exactamente la misma W con la que empezaron**
(mediana 1,8833 en los dos extremos; sube en 0, baja en 0).

**Y eso pese a que hubo 13 recogidas de botín dentro de formas.** La explicación
probable es la saciedad y los rendimientos decrecientes de `riqueza_W`: recoger
un duplicado no mueve la W. **No lo he comprobado, y lo marco como hipótesis.**

### Botín: ¿explorar encuentra cosas?

| | recogidas | tics | por 100 tics |
|---|---|---|---|
| **dentro de forma** | **13** | 1.016 | **1,280** |
| fuera | 15 | 16.112 | **0,093** |

**Trece veces más recogidas por tic dentro de forma que fuera.** Es la primera
señal de que explorar encuentra cosas — **pero son 13 sucesos contra 15, y el
mundo lento apenas tiene recogidas. Es una señal, no un resultado.**

### «Acerca al armado» en inseguro, K contra A

| | tics con armado a la vista | el paso acerca | |
|---|---|---|---|
| **K** | 4.270 | **18** | **0,42 %** |
| **A** | 10.386 | 365 | **3,51 %** |

**K se acerca a los armados ocho veces menos que A.** En P5-8K fue 0,23 % contra
0,80 %; aquí la diferencia es mayor.

---

## Lo que no sé, marcado como tal

**No sé por qué la aceptación bajó al 13,9 %.** Sé que **no es el código** —el
margen es el mismo y P5-8J demostró que la aceptación sigue a los diarios—, pero
no sé qué hay en estos estados que baje la ventaja. **Y con dos asientos no lo
averiguo.**

**El rodeo no está probado.** Una forma rodeó, y completó. **n = 1.** Todo lo
que diga de él es un caso. Lo que sí está medido en seco, sobre 103 vetos
reales, es que **con colchón cero el rodeo existe en el 59 % de las ocasiones**;
lo que no sé es qué pasa cuando el cuerpo pasa rozando el alcance, **porque aquí
casi no pasó**.

**Los 14 rompimientos son todos de la misma causa.** «(e) rival a 2 o menos» es
la condición más laxa de las siete. Las otras seis siguen sin verse.

**K2 con una partida no dice nada**, pero los cuatro puestos van en la misma
dirección y prefiero decirlo ahora que descubrirlo en la tanda cuatro.

---

## Propuesta, no ejecución

**Este es el primer diseño de la serie cuyo mecanismo se comporta como la teoría
dice:** la forma nace, se acepta, el cuerpo la obedece —y la rompe cuando debe—,
llega en el 39 % de los casos, ve lo que prometió en el 40 %, y **descubre 2,7
veces más dentro de forma que fuera**. K1 cumpliría.

**Para por la aceptación, que es el umbral que menos mide lo que importa.** Con
23 formas en una partida, las cuarenta darían del orden de **460**, más que
suficiente para todos los sellos. **El 13,9 % no es poca cosecha: es poca tasa
sobre muchas propuestas.**

**Lo que yo haría, y no hago: pedirte que reconsideres el suelo de aceptación
como condición de parada**, porque mide la proporción y no la cantidad, y la
cantidad es la que da n. Si el suelo hubiera sido «al menos 15 formas aceptadas
por partida», esta sonda habría pasado.

**No lo decido yo.** El umbral, el colchón y la regla del veto son tuyos.

**Gasto de la sonda: 0,126178 $.** Cola vacía al acabar. **Las cuarenta no se han
lanzado.**

**PARO AQUÍ.**

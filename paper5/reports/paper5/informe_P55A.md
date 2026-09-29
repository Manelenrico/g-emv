# P5-5A — ¿Tiene el consejero la moneda?

En seco, coste cero. Nada a la plataforma. **Ninguna decisión real cambia.**
Motor, tabla y decisor intactos.

**El consejero del cuatro habla de los otros casi siempre —el 80,9 % de sus
respuestas— pero lo que dice es, casi todo, el relato que acababa de leer.**
Solo el **4,06 %** de las respuestas afirma un cambio (una llegada o una
ausencia), y **esas son justo las que falla**: las llegadas aciertan el
**49,04 %** y las ausencias el **46,15 %**, cuando decir «todo sigue igual» en
esos mismos tics habría acertado el **87,50 %** y el **92,31 %**.

**Con la moneda de P5-4B, el consejero del cuatro acabaría con confianza 0,000
de mediana y ninguna de las 160 vidas pasaría de 0,5.** El máximo en todo el
corpus es **0,4**.

**M1 cumple a medias, M2 falla, M3 falla, M4 cumple.**

---

## Los datos, y una corrección de la cifra del encargo

El encargo dice «las 15.515 propuestas de S-2 brazos B y C». **Esa cifra no es
de S-2 sola.** Viene de `informe_CHAT.md:216` y de
`apendice_numeros_p4.md:160`, y allí está declarada como **«S-2 más
S-CORTEX»**: las cuatro tandas, S2_B + S2_C + serie_B + serie_C.

Lo que hay en `paintball/runs/S2_B` y `S2_C`, que es lo que el encargo acota:

| | respuestas del consejero | propuestas |
|---|---|---|
| **S2_B** | 1.650 (1.644 con respuesta buena) | 4.846 |
| **S2_C** | 1.634 (1.630 con respuesta buena) | 4.885 |
| **total** | **3.284 (3.274 buenas)** | **9.731** |

Las otras 5.784 están en `serie_B` y `serie_C`, cuyos `.log` son de la tanda
anterior, en el formato antiguo (bytes escapados) y con otro roster. **Se
quedan fuera**, como pide el alcance del encargo.

**La unidad.** Una *respuesta* es una llamada (`cortex_llamada`) con sus dos o
tres propuestas, cada una con su `accion` y su `motivo`. A1 clasifica la
respuesta entera —acción más explicación, como pide el encargo—; A2 y A3 van por
**afirmación**, que es cada trozo distinto que dispara una clase.

---

## A1 · La clasificación

### Las reglas, listadas

Principio de diseño, declarado: **el rival tiene que ser el sujeto**. «el asiento
12 se acerca» es una afirmación sobre el otro; «acércate al asiento 12» o
«mantener distancia del asiento 12» son órdenes al cuerpo y **no cuentan**. Por
eso los patrones exigen que la mención del rival vaya **antes** del verbo, a
menos de 40 caracteres (70 para la distancia) y sin punto ni punto y coma por
medio. Todo se compara en minúsculas y sin tildes.

**Quién es un rival:** `asiento N` · `rival(es)` · `enemigo(s)` ·
`adversario(s)` · `hostil(es)` · `atacante(s)` · `agresor(es)` ·
`perseguidor(es)` · `jugador(es)`. Si el número de asiento es el del hermano, la
afirmación se manda a HERMANO.

**Quién es el hermano:** `hermano` · `pareja` · `compañer@` · `aliad@`.

| clase | patrones (resumidos; el fichero es `clases_consejo.py`) |
|---|---|
| **LLEGADA** | RIVAL + `se acerca` · `se aproxima` · `viene` · `avanza` · `se dirige` · `te busca` · `te persigue` · `acecha` · `te alcanza` · `puede alcanzarte` · `te tiene a tiro` · `va a por ti` · `te va a atacar` · `vuelva a atacar` · `seguirá atacando` · `cierra distancia` · `antes de que te mate`; y sueltos `te acechan`, `te persiguen`, `vienen a por ti`, `te tienen acorralado` |
| **AUSENCIA** | RIVAL + `se aleja` · `se va` · `huye` · `retrocede` · `se retira` · `ya no …` · `no es amenaza` · `está lejos` · `fuera de tu alcance` · `fuera de tu vista` · `no te ve` · `no puede alcanzarte` · `ha desaparecido`; y sueltos `no ves a nadie`, `no hay enemigos`, `sin amenazas cerca`, `nadie cerca` |
| **POSICIÓN** | RIVAL + `a N casillas` · `en (x,y)` · `al norte/sur/…` · `N casillas de distancia`; y RIVAL + proximidad sin cifra: `cerca` · `cercano` · `al lado` · `adyacente` · `pegado a ti` · `a tu alcance` · `dentro del alcance` · `en tu rango` · `acorralado` · `te ve` · `te rodea` · `te está pegando` · `te atacan`; y sueltos `estás rodeado`, `enemigos visibles`, `en el rango de N enemigos` |
| **HERMANO** | HERM + `está` · `en (x,y)` · `a N casillas` · `herido` · `tocado` · `en las últimas` · `bajo ataque` · `le están pegando` · `en peligro` · `muerto` · `solo` · `te necesita` · `va a morir`; y `atacando/pegando/mató a tu hermano`, `perder a tu hermano`, `tu hermano ha muerto`, `es tu hermano`, `estáis cerca/juntos` |
| **NADA** | ninguna de las anteriores |

**Lo condicional no afirma nada.** «evaluando **si** el asiento 3 se acerca» o
«verás **si** el asiento 9 se acerca» no cuentan como LLEGADA. Se descartan los
trozos que llevan delante, a menos de 40 caracteres, `si` · `saber si` ·
`evaluando` · `verás` · `observa` · `vigila` · `podría` · `comprobar` ·
`decidir` · `averiguar` · `conocer` · `atento` · `pendiente`.

### El error de las reglas, medido a mano

**Muestra de 100 respuestas**, sorteadas con semilla 20260919, etiquetadas a mano
por mí, una por una, antes de ver lo que decían las reglas.

| versión | acuerdo (400 decisiones) | conjunto exacto | POSICIÓN prec./cob. | HERMANO prec./cob. | LLEGADA prec./cob. |
|---|---|---|---|---|---|
| **v1** (primeras reglas) | 83,5 % | 44/100 | 100 % / **35,7 %** | 97,2 % / 74,5 % | 20 % / 20 % |
| **v2** (las de arriba) | 95,8 % | 84/100 | 93,9 % / 88,6 % | 97,8 % / 93,6 % | 100 % / 80 % |

**v1 se quedaba muy corta** —se le escapaban dos de cada tres afirmaciones de
posición—, así que la corregí. Pero **el 95,8 % de v2 está medido sobre la misma
muestra que usé para corregirla**, y eso es optimista por construcción. Así que
etiqueté a mano **50 respuestas nuevas**, sorteadas aparte y **nunca usadas para
afinar nada**:

| control ciego (50) | VP | FP | FN | precisión | cobertura |
|---|---|---|---|---|---|
| **POSICIÓN** | 33 | **0** | 6 | **100 %** | 84,6 % |
| **HERMANO** | 20 | **0** | 9 | **100 %** | 69,0 % |
| **LLEGADA** | 1 | 1 | 0 | 50 % | (n=1) |
| AUSENCIA | 0 | 0 | 0 | — | — |
| **global (200 decisiones)** | | | | **acuerdo 92,0 %** | conjunto exacto 37/50 |

**Las reglas no inventan: se quedan cortas.** Cero falsos positivos en POSICIÓN
y en HERMANO sobre el control ciego. **Por tanto todas las fracciones de A1 son
cotas inferiores.** Corregidas por cobertura, POSICIÓN estaría cerca del 74 % y
HERMANO cerca del 58 %; doy las medidas, no las corregidas, y dejo la corrección
dicha.

**La clase LLEGADA es la más floja** (precisión 50-100 % según la muestra, con
uno o dos casos), y es justo la que M2 mide. Se dice aquí y se repite en el
cotejo.

### Las cifras

Sobre **3.274** respuestas buenas. Una respuesta puede caer en varias clases.

| clase | total | | S2_B (1.644) | | S2_C (1.630) | |
|---|---|---|---|---|---|---|
| **POSICIÓN** | 2.044 | **62,43 %** | 1.005 | 61,13 % | 1.039 | 63,74 % |
| **HERMANO** | 1.317 | **40,23 %** | 697 | 42,40 % | 620 | 38,04 % |
| **LLEGADA** | 110 | **3,36 %** | 41 | 2,49 % | 69 | 4,23 % |
| **AUSENCIA** | 28 | **0,86 %** | 20 | 1,22 % | 8 | 0,49 % |
| **NADA** | 625 | **19,09 %** | 337 | 20,50 % | 288 | 17,67 % |
| **alguna sobre los otros** | 2.649 | **80,91 %** | 1.307 | 79,50 % | 1.342 | 82,33 % |
| solo sobre rivales | 2.093 | 63,93 % | 1.031 | 62,71 % | 1.062 | 65,15 % |
| **LLEGADA o AUSENCIA** | 133 | **4,06 %** | 60 | 3,65 % | 73 | 4,48 % |

**Los dos brazos dicen lo mismo.** La mayor diferencia está en LLEGADA (2,49 %
contra 4,23 %) y es pequeña en absoluto: 41 respuestas contra 69.

**El retrato en una frase: el consejero habla de los otros constantemente, y casi
siempre para decir dónde están, que es lo que el relato acababa de decirle.**

---

## A2 · La comprobación

Ventana: los **100 tics** siguientes al tic de la foto. Distancia de Chebyshev.
Se mira lo que vio **cualquiera de los dos hermanos**; si nadie volvió a ver al
rival, la afirmación **no es comprobable** y no entra en la tasa.

| clase | criterio de acierto |
|---|---|
| **LLEGADA** | en algún tic de la ventana el rival está **a tiro** (`cheb ≤` alcance del arma que lleva) **o** al final de la ventana está **más cerca** que al principio |
| **AUSENCIA** | al final está **más lejos** que al principio, **o** no lo ve nadie en la segunda mitad de la ventana |
| **POSICIÓN** | en algún tic está a **≤ 3 casillas** de lo dicho (el mismo criterio del banco, P5-4B) |
| **HERMANO** | contra el diario **del hermano**: posición a ≤ 3 casillas, o el estado dicho (tocado, en las últimas, bajo ataque) |
| **línea base «nadie se mueve»** | en los **mismos** rival-tics: al final de la ventana el rival está a **≤ 3 casillas** de donde estaba en el tic de la foto |

| clase | afirmaciones | comprobables | **acierto** (IC95) | **línea base** (IC95) | **diferencia** (IC95) |
|---|---|---|---|---|---|
| **LLEGADA** | 116 | 104 (89,7 %) | **49,04 %** (39,6-58,5) | **87,50 %** (79,8-92,5) | **−38,46** (−49,13, −26,24) |
| **AUSENCIA** | 28 | 26 (92,9 %) | **46,15 %** (28,8-64,5) | **92,31 %** (75,9-97,9) | **−46,15** (−64,42, −21,48) |
| **POSICIÓN** | 3.833 | 2.000 (52,2 %) | **98,60 %** (98,0-99,0) | 88,65 % (87,6-89,6) | **+9,95** (+8,80, +11,09) |
| **HERMANO** | 2.233 | 1.420 (63,6 %) | **95,49 %** (94,3-96,5) | 83,63 % (82,0-85,1) | **+11,36** (+9,92, +13,76) |

**Tres cosas salen de aquí, y las tres importan.**

1. **Las afirmaciones de cambio pierden contra «todo sigue igual», y por mucho.**
   −38 puntos las llegadas, −46 las ausencias, con el cero muy lejos del
   intervalo. **Es exactamente el resultado de P5-4B visto desde el otro lado:**
   en el horizonte de cien tics los rivales apenas se mueven, así que la
   suposición trivial es la buena y anunciar un cambio es casi siempre
   equivocarse.
2. **Las de posición aciertan el 98,6 %, y eso no es mérito.** Son el relato
   devuelto: el consejero repite la distancia que acababa de leer. Gana a la
   línea base por 9,95 puntos porque la línea base se mide al final de la ventana
   y la posición se acepta en cualquier tic de ella.
3. **La mitad de las de posición no se pueden comprobar**: 1.820 de 3.833 dicen
   proximidad sin cifra («cerca», «a tu alcance», «te atacan»). **No les pongo un
   umbral inventado**: quedan fuera de la tasa y se declaran. Las 2.013 que sí
   llevan cifra aciertan **1.972 y fallan 28**.

### El corte que más dice: LLEGADA con nombre y sin él

| LLEGADA | comprobables | aciertos | **tasa** |
|---|---|---|---|
| **nombra un asiento** («el asiento 8 que viene») | 69 | 26 | **37,68 %** |
| habla en genérico («los enemigos que te acechan») | 35 | 25 | **71,43 %** |

**La afirmación falsable —la que da un nombre— acierta el 37,7 %.** La genérica
acierta casi el doble porque le basta con que **alguno** de los rivales visibles
se acerque, y con tres o cuatro a la vista eso pasa casi siempre. **Es una
afirmación que no arriesga nada.**

---

## A3 · Lo nuevo, y la confianza que habría ganado

**No trivial**, con la moneda de P5-4B: la afirmación dice un **cambio**. Son no
triviales LLEGADA y AUSENCIA siempre; POSICIÓN solo si nombra una casilla a más
de 3 de donde se vio al rival; HERMANO solo si dice que cambia (se aleja, se
acerca, va a morir, no aguanta).

| | afirmaciones | | comprobadas | acierto |
|---|---|---|---|---|
| **no triviales** | **163** | **2,62 %** | 145 (89,0 %) | **48,28 %** |
| triviales | 6.047 | 97,38 % | 3.405 | **97,53 %** |
| total | 6.210 | | | |

**De cada cuarenta afirmaciones del consejero, una dice algo nuevo, y esa una
sale a cara o cruz.**

### La confianza que habría ganado, vida por vida

Regla de B2: empieza en **0**, **+0,10** por acierto, **−0,20** por fallo,
acotada en 0 y 1, y **solo cuentan las no triviales**.

| | valor |
|---|---|
| vidas | **160** (los 160 asientos-partida de S2_B y S2_C) |
| vidas con **alguna** afirmación nueva comprobada | **65** (40,6 %) |
| **C final, mediana** | **0,000** |
| C final, media | 0,029 |
| **C final, máximo de todo el corpus** | **0,400** |
| vidas por encima de 0,8 | **0/160** |
| vidas por encima de 0,5 | **0/160** |
| vidas por debajo de 0,2 | **149/160** |
| trayectoria (0-500 / 500-1500 / >1500) | 0,000 / 0,100 / 0,000 |

**Reparto completo:** 130 vidas en 0,0 · 19 en 0,1 · 7 en 0,2 · 3 en 0,3 · 1 en
0,4. **Ninguna llega a la mitad.**

Dos razones, las dos medidas: **casi no dice nada nuevo** (2,62 %), y **cuando lo
dice acierta menos de la mitad** (48,28 %), con un castigo que es el doble del
premio. Noventa y cinco vidas no llegan siquiera a hacer una afirmación nueva
comprobable.

---

## A4 · ¿Le sirvió de algo al cuatro?

Por **propuesta**, no por respuesta, y **quitando las de esperar** (`regla ==
"esperar"`), como pide «aceptada sin esperar». Cajas del cuatro: una propuesta
**llega a la mesa** si su candidato traducido aparece en el estado `en la mesa`
en algún tic de su vida, y **gana** si venció la decisión.

| grupo | propuestas | **llega a la mesa** | **gana** |
|---|---|---|---|
| **con afirmación cierta sobre los otros** (rivales o hermano) | 5.164 | **26,30 %** | 5,926 % |
| sin afirmación cierta | 4.014 | **33,83 %** | 6,054 % |
| **diferencia** | | **−7,53** (−9,43, −5,64) | −0,128 (−1,120, +0,843) |

| grupo | propuestas | **llega a la mesa** | **gana** |
|---|---|---|---|
| **con afirmación cierta sobre rivales** | 3.154 | 28,22 % | **6,880 %** |
| sin ella | 6.024 | 30,31 % | 5,511 % |
| **diferencia** | | **−2,09** (−4,03, −0,13) | **+1,369** (+0,340, +2,454) |

**Acertar sobre los otros no abrió ninguna puerta en el cuatro.** Llegar a la
mesa es incluso **menos** probable, y la explicación no es misteriosa: las
respuestas que hablan del hermano se traducen por la regla `hermano` a
`ir_pareja`, que es la que más se duerme y más se veta.

**El único rastro de señal está en la caja de ganar, y es de 1,37 puntos**
(6,88 % contra 5,51 %) para las propuestas con una afirmación cierta **sobre
rivales**, con el cero fuera del intervalo. Es pequeño, pero es lo único que
apunta en la dirección de que el contenido valía algo. **La puerta de un paso no
podía cobrar más que eso**, que es justo lo que M4 anticipaba.

---

## A5 · Ejemplos literales, con su comprobación

### LLEGADA (n=116 · 51 aciertos · 53 fallos · 12 no comprobables)

> **ACIERTO** · S2_C asiento 10, tic 700 · *«…tendrías defensa cuerpo a cuerpo
> contra los dos **enemigos que te acechan**.»* — genérica, sobre los asientos 5,
> 14 y 15; alguno se acercó. La línea base también acertaba.

> **ACIERTO** · S2_C asiento 11, tic 3400 · *«…necesitas estar en mejor forma
> antes de que el **asiento 1 vuelva a atacar**.»* — y volvió: entró a tiro
> dentro de la ventana.

> **ACIERTO** · S2_C asiento 10, tic 2100 · *«Te hará desaparecer de la vista de
> **quienes te persiguen**…»* — **y aquí la línea base FALLA**: los rivales sí se
> movieron. Es uno de los pocos casos en que el consejero gana a «todo sigue
> igual».

> **FALLO** · S2_B asiento 11, tic 5900 · *«Necesitas un arma para defenderte del
> jugador del **asiento 0 que te acecha**…»* — no se acercó ni llegó a tiro en
> cien tics. La línea base acertaba.

> **FALLO** · S2_B asiento 11, tic 2300 · *«El arco es tu mejor arma a distancia
> contra el **asiento 8 que viene** con espada…»* — no vino.

### AUSENCIA (n=28 · 12 aciertos · 14 fallos · 2 no comprobables)

> **ACIERTO** · S2_B asiento 10, tic 1000 · *«…ahora **no hay amenaza**
> inmediata y el círculo no te presiona.»*

> **ACIERTO** · S2_B asiento 11, tic 900 · *«…y el **asiento 9 no es una
> amenaza** inmediata.»*

> **FALLO** · S2_B asiento 11, tic 1800 · *«Tu hermano está entero a 1 casilla,
> **no hay amenaza** inmediata…»* — la había.

> **FALLO** · S2_B asiento 10, tic 2700 · *«Estás camuflado y el **asiento 13 no
> te ve**…»* — le vio.

> **Un falso positivo de la regla, declarado**: *«la red puede inmovilizar a tus
> **atacantes 3 segundos mientras te recuperas o huyes**»* se clasificó AUSENCIA
> porque `huye` quedó detrás de la mención del rival, pero quien huye es el
> cuerpo. Con 28 afirmaciones en la clase, un caso así pesa el 3,6 %.

### POSICIÓN (n=3.833 · 1.972 aciertos · 28 fallos · 1.833 no comprobables)

> **ACIERTO** · S2_B asiento 10, tic 700 · *«Lanzar un cuchillo ahora al del
> **asiento 8 que está a 5 casillas**…»*

> **ACIERTO** · S2_B asiento 11, tic 2700 · *«Lanzar la red al **asiento 1 que
> ves a 7 casillas**…»*

> **ACIERTO** · S2_B asiento 11, tic 1000 · *«…contra el del **asiento 7 que está
> tocado a 7 casillas**…»*

> **FALLO** · S2_C asiento 10, tic 5800 · *«Dispara al **asiento 7 que te ve y
> lleva red**, luego recoge las flechas a 7 casillas»* — las 7 casillas eran de
> las flechas, no del asiento 7; la regla se llevó la cifra equivocada. **Es un
> fallo de la regla, no del consejero**, y es de los 28.

> **FALLO** · S2_C asiento 10, tic 3700 · *«…defenderte del **asiento 4 que está
> tocado y cerca**, y el arco te da 8 casillas…»* — mismo tropiezo: la cifra es
> del arco.

### HERMANO (n=2.233 · 1.356 aciertos · 64 fallos · 813 no comprobables)

> **ACIERTO** · S2_C asiento 11, tic 2200 · *«…muévete hacia tu **hermano en
> (19,13)**…»* — estaba allí.

> **ACIERTO** · S2_C asiento 11, tic 2100 · *«Moverte hacia tu **hermano en
> (18,22)**. Está siendo atacado y a solo 2 casillas…»*

> **ACIERTO** · S2_C asiento 10, tic 600 · *«Gritar por el canal de equipo a tu
> hermano que se mueva hacia ti. **Estáis a 5 casillas**…»* — **y la línea base
> falla**: el hermano sí se movió.

> **FALLO** · S2_C asiento 10, tic 500 · *«**Tu hermano está en las últimas** y
> recibe daño del asiento 12…»* — no estaba en las últimas.

> **FALLO** · S2_B asiento 10, tic 600 · *«Reagruparte con tu **compañero
> entero**…»* — no estaba entero.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **M1** | más del 40 % de las respuestas contienen alguna afirmación sobre los otros | A1 | **80,91 %** (63,93 % si solo rivales) | **CUMPLE** |
| **M1** | …más del 20 % contienen LLEGADA o AUSENCIA | A1 | **4,06 %** | **FALLA** |
| **M2** | acierto de LLEGADA por encima del 55 % | A2 | **49,04 %** (37,68 % si nombra asiento) | **FALLA** |
| **M2** | …y por encima de la línea base en esos tics | A2 | base **87,50 %**; diferencia **−38,46** | **FALLA** |
| **M2** | acierto de AUSENCIA por debajo de LLEGADA | A2 | **46,15 %** < 49,04 % | **CUMPLE** (por poco; los intervalos se solapan) |
| **M3** | con la moneda de lo nuevo, C final por encima de 0,5 en más de la mitad de las vidas | A3 | **0 de 160**; mediana **0,000**, máximo **0,400** | **FALLA** |
| **M4** | las propuestas con afirmación cierta sobre los otros no fueron aceptadas más que las demás | A4 | fueron aceptadas **menos** | **CUMPLE** |
| **M4** | …diferencia menor de 3 puntos | A4 | rivales: **−2,09** en la mesa, **+1,37** en ganar · lectura ancha: **−7,53** | **CUMPLE en la lectura de rivales, FALLA en la ancha** |

**Los contadores podían variar, comprobado.** El de M1 va del **0,86 %**
(AUSENCIA) al **62,43 %** (POSICIÓN) según la clase, y el mismo contador de
LLEGADA fue **5,77 %** con las reglas v1 y **3,36 %** con v2. El de M2 va del
**37,68 %** al **98,60 %** según clase y corte, y el de LLEGADA fue **64,40 %**
con v1: es el contador más sensible de todos y por eso lleva el aviso. El de M3
podía subir: bastaba con que el consejero acertara dos de cada tres novedades
para que muchas vidas pasaran de 0,5; llegó a 0,4 como máximo. El de M4 sale
**negativo** en una caja y **positivo con el cero fuera** en otra, en el mismo
corpus.

### M2 falla, y falla de la forma más informativa posible

Se selló esperando que el consejero, cuando anuncia una llegada, acertase más que
la suposición trivial. **Pasa lo contrario, y con margen enorme.** La causa está
medida en P5-1 y en P5-4B: **en cien tics los rivales apenas cambian de sitio**,
así que la afirmación trivial tiene un 87,5 % de acierto de regalo y cualquier
anuncio de cambio parte con esa desventaja. El consejero no anuncia llegadas
porque las vea venir: las anuncia porque **hay un rival cerca y suena
prudente**. Cuando le obligas a poner nombre, acierta el 37,7 %.

---

## Lo que P5-5A deja dicho

1. **El consejero del cuatro no tiene la moneda.** Habla de los otros el 80,9 %
   de las veces, pero solo el **2,62 %** de sus afirmaciones dice un cambio, y
   esas aciertan el **48,28 %**. Con la regla de B2 acabaría en **0,000** de
   mediana y **ninguna** de las 160 vidas pasaría de 0,5.
2. **Lo que sí sabe hacer es repetir el relato.** El 98,6 % de sus afirmaciones
   de posición con cifra son correctas, porque son la distancia que acababa de
   leer. Eso es fiable y es **exactamente lo que la moneda de lo nuevo no
   paga**, por diseño.
3. **Y ahí está la tensión que P5-4B ya había dejado planteada.** Allí el
   consejero trivial era el que más recuperaba (16,5 %) y la moneda lo apagó.
   Aquí se ve por qué: **en este mundo la afirmación trivial es la buena**, con
   un 87,5 % de acierto frente al 49,0 % de la novedad. Pagar por novedad es
   pagar por la parte equivocada.
4. **Pedirle formas al consejero real no va a funcionar con esta moneda.** No
   porque hable poco de los otros, sino porque lo que dice de nuevo sale a cara y
   cruz, y el castigo es el doble que el premio.
5. **Y el cuatro ya no podía cobrarlo.** Acertar sobre los otros no ayudó a
   llegar a la mesa (−2,09 puntos) y ayudó 1,37 puntos a ganar. La puerta de un
   paso no tenía dónde meter una afirmación sobre el futuro de un rival.

**Lo que esto sugiere y NO he ejecutado** (propuesta, no decisión): si se le va a
pedir al consejero que hable en formas, la moneda tendría que pagar por
**reducir la incertidumbre del cuerpo** —cuánto cambia la forma al creer lo
dicho— y no por ser distinto de lo de antes; es la misma propuesta que dejó
P5-4B, y P5-5A le añade la razón empírica. Y si se quiere medir el anuncio de
llegada, hay que **exigirle nombre**: la afirmación genérica acierta el 71,4 %
sin arriesgar nada.

**PARO AQUÍ.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

`decisor_zs.py` sigue en `8fa03547e3228ef9df4aa94c444f9252` y
`appraisal_zs_v42_exp.py` en `98c13d60167c80cc8334c965be75c640`: **ninguno de
los dos se ha tocado, ni hacía falta abrirlos.** Ficheros de este encargo, todos
en `cantera/paper5/`:

| fichero | md5 |
|---|---|
| `extrae_consejo.py` | `66db58852c7e88851dd7f8b7895f83a8` |
| `clases_consejo.py` | `4df13ea6d512f8e5cd585fff8c652635` |
| `comprueba_consejo.py` | `b339569c209aaa08142cbee1e7570ad1` |
| `analiza_P55A.py` | `56768b5a6d911deccb1a9f7e7c9ef0d9` |

Datos: `P55A_respuestas.jsonl` (3.284 respuestas), `P55A_juicio.json`,
`P55A_confianza.json`, `P55A_muestra100.json` (la muestra etiquetada a mano),
`P55A_control50.json` (el control ciego), `ejemplos_P55A.py`, y los logs
`P55A_extrae.log`, `P55A_juicio.log`, `P55A_analisis.log`.

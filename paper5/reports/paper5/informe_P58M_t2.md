# P5-8M · TANDA 2 — acumulado de veinte partidas

**PARO AQUÍ.** Las veinte restantes esperan tu sí.

Imagen comprobada md5 a md5 antes de lanzar: los siete idénticos, id
`sha256:68faccb5…`. **Sin cambios en el mecanismo.** Custodia idéntica al
empezar y al acabar.

---

## El titular

**Doblar la muestra ha cambiado tres sellos, y dos a peor.** Lo que en diez
partidas parecía sólido, en veinte se deshace — y la razón, en los dos casos,
es que el agregado lo mandaba un puñado de asientos raros.

| | diez partidas | **veinte partidas** |
|---|---|---|
| **K1 · K/A** | 1,54 **cumple** | **1,23 FALLA** |
| K1 · dentro/fuera | 3,79× | **5,20×** |
| **K6** | cumple | **FALLA** (un asiento a 5,51 ms) |
| **K2 · puesto** | K peor en 3 de 5 | **K peor en 6 de 10** |
| K4 lectura (b) | cumple | **cumple** (12,5 %) |
| completadas | 62,3 % | **71,9 %** |

**Y el botín se da la vuelta del todo:** en la tanda 1 había 3,6 veces más
recogidas dentro de forma que fuera; con veinte partidas hay **menos dentro que
fuera** (0,481 contra 1,344 por cien tics). **Retiro la señal que di en la tanda
1: era la semilla, no el mecanismo.**

**Lo que sí se consolida es una ley limpia**, y contesta tu pregunta (4): **una
forma nace cada 46 tics de entorno seguro**, con una razón de 0,0205 a 0,0260 en
las diez semillas. **La ignorancia inicial es idéntica en todas** (0,890-0,895):
lo que decide si una semilla nace 10 formas o 383 es **cuánto tiempo pasa el
cuerpo en entorno seguro**, nada más.

---

## Un diario que la plataforma no produjo

**39 asientos de 40.** El asiento 10 de `K/20784561` no tiene artefacto: el
servidor responde `Agent 10 has no artifact. Available agent indices: 11`. El
episodio acabó bien (`completed`, 0,097807 $) y ese asiento **tiene puntuación**
(posición 10, score 1,0), así que jugó — **pero no subió su diario**. Reintenté
la descarga y no existe.

**No es un fallo del reintento ni mío.** Lo declaro porque la semilla 20784561
cuenta con **un solo asiento de K** en todo lo de abajo.

---

## El suelo de serie (corrección de la mesa)

| semilla | aceptadas |
|---|---|
| 20260916 | 23 |
| 20365645 | 7 |
| 20470374 | 7 |
| 20575103 | 10 |
| 20679832 | 6 |
| 20784561 | 5 |
| 20889290 | 7 |
| 20994019 | 12 |
| 21098748 | 8 |
| 21203477 | 11 |

**Acumulado: 96 formas en 10 partidas de K = 9,6 por partida.**
**Proyección a las veinte partidas de K de la serie: 192.** Suelo 150 → **en
camino**, con holgura del 28 %.

---

## Los siete sellos, acumulado de veinte partidas (96 formas)

| | sello | acumulado | |
|---|---|---|---|
| **K1** | K/A ≥ 1,5 **y** dentro ≥ 2× | **1,23** y **5,20×** | **FALLA** (por la primera mitad) |
| **K2** | cero muertes; puesto no baja | 0 muertes; **K peor en 6 de 10** | **va mal** |
| **K3** | cero con armado a tiro en forma activa | **(a) 42 · (b) 3** | **FALLA las dos** |
| **K4** | completadas ≥ 50 %; veto duro 5-30 % | **71,9 %**; **(a) 1,0 % · (b) 12,5 %** | **CUMPLE con (b)** |
| **K5** | daño ≤ base de A | 1,0 % contra 0,4 % | **FALLA** por un suceso |
| **K6** | < 5 ms mediana; cero perdidos | **un asiento a 5,51 ms**; 0 perdidos | **FALLA** |
| **K7** | ≤ 4 $ | 1,805 $ las veinte → **3,61 $** | **cumpliría, justo** |

### K1 · las dos mitades se comportan al revés

| semilla | K | A | **K/A** | dentro | fuera |
|---|---|---|---|---|---|
| 20260916 | 9,43 | 6,22 | 1,52 | 23,23 | 8,56 |
| 20365645 | 8,35 | 6,23 | 1,34 | **69,04** | 7,26 |
| **20470374** | 8,27 | **91,34** | **0,09** | 42,17 | 7,74 |
| 20575103 | 28,52 | 19,68 | 1,45 | 56,34 | 26,40 |
| **20679832** | 47,65 | 5,35 | **8,91** | **114,75** | 45,17 |
| **20784561** | 13,41 | **30,46** | **0,44** | 82,93 | 12,82 |
| 20889290 | 7,69 | 6,43 | 1,20 | **72,00** | 7,07 |
| 20994019 | 8,20 | 7,47 | 1,10 | 42,37 | 7,22 |
| 21098748 | 6,05 | 6,05 | 1,00 | 37,25 | 5,64 |
| 21203477 | 6,78 | 5,66 | 1,20 | **47,17** | 6,34 |

**La segunda mitad del sello es rocosa: dentro de forma se descubre más en las
diez semillas, sin excepción** (de 23 a 115 por cien tics dentro, contra 5,6 a
45 fuera). Agregado **5,20×**, mejor que el 3,79× de la tanda 1.

**La primera mitad es ruido de asientos que mueren pronto.** Las tres semillas
que rompen el agregado —0,09, 0,44 y 8,91— son aquellas donde **un brazo
sobrevivió mucho menos que el otro**: los asientos de A de `20470374` vivieron
679 y 441 tics, y los de `20784561` poco más. **Los primeros tics de una vida
son los que más descubren**, así que morir pronto infla el cociente por tic. Es
el mismo efecto que ya señalé en P5-8I.

**No cambio el sello.** Digo que su primera mitad, tal como está escrita, mide
en parte cuánto vive cada brazo.

### K2, que es lo que más vigilas — **y va mal**

| semilla | K (mediana) | A (mediana) | |
|---|---|---|---|
| 20260916 | 14,0 | 10,0 | **K peor** |
| 20365645 | 10,5 | 9,5 | **K peor** |
| 20470374 | 12,0 | 15,0 | K mejor |
| 20575103 | 14,0 | 14,0 | igual |
| 20679832 | 14,5 | 9,5 | **K peor** |
| 20784561 | 15 *(un asiento)* | 15,5 | K mejor |
| 20889290 | 13,5 | 8,0 | **K peor** |
| 20994019 | 12,0 | 14,5 | K mejor |
| 21098748 | 9,5 | 7,0 | **K peor** |
| 21203477 | 6,0 | 3,5 | **K peor** |

**K peor en 6, mejor en 3, igual en 1.** En la tanda 1 era 3-1-1; al doblar la
muestra **la proporción se mantiene**, que es lo que la hace creíble.

**Cero muertes dentro de forma**, así que no es que la curiosidad mate al
cuerpo. **Es que le cuesta puesto.** Sigue sin ser concluyente —diez semillas, y
las diferencias van de 1 a 5,5 puestos— pero **ya no lo llamaría ruido**.

### K3 · las dos lecturas que pediste

| | |
|---|---|
| **(a) sellada** — todo tic con forma activa | **42** de 3.323 tics dentro |
| **(b) del mecanismo** — solo con piernas listas | **3** de 365 tics |

**Las dos fallan el cero**, y las dos salen del **mismo asiento**
(`20470374/11`); los otros dieciocho dan cero.

**Y los 3 de la lectura (b) son exactamente las 3 rupturas «(a) veto vital:
armado a tiro».** El mecanismo vio los tres y mató la forma en los tres.

### La comprobación del código que pediste

**En los tics de enfriamiento manda el decisor entero, con su veto vital de
siempre. El compromiso no bloquea nada.** Tres pruebas independientes:

1. **`_compromiso` sale antes de mirar nada** si `move_ready_in > 0`: registra
   «enfriamiento» y **devuelve la acción del decisor sin tocarla**.
2. **El candidato de la forma ni entra en la papeleta.** Su receta es
   `tipo: "ir"`, y `_veta_receta` (`policy_cortex.py:279-283`) la manda al
   prefijo `ir_`, que `Bloqueos.veta` (`decisor_zs.py:95-104`) tumba cuando
   `move_ready_in > 0` — **la misma regla que veta los `ir_` del propio cuerpo**.
3. **Medido en los diarios**: el candidato `_FM_` aparece en la papeleta **0 de
   1.825** tics de enfriamiento y **221 de 221** con las piernas listas.

**Y el renglón de curiosidad no toca la decisión viva:** `con_renglon` se
instala y se restaura **solo dentro de `_juzga`** (`policy_forma.py:692-699`).

**Conclusión: en los 39 tics de enfriamiento que K3 cuenta, el cuerpo se
comportó exactamente como el de A.** El sello los carga a K; el mecanismo no los
mira.

### K4 · las dos lecturas del veto duro

| causa | n | % |
|---|---|---|
| **completada por alivio** | **69** | **71,9 %** |
| atasco | 15 | 15,6 % |
| **sin rodeo** | **11** | **11,5 %** |
| veto duro | 1 | 1,0 % |

**Completadas 71,9 %: cumple el ≥ 50 % con holgura** (era 62,3 % con diez).

| banda del veto duro (sello 5-30 %) | | |
|---|---|---|
| **(a)** solo «veto duro» | 1/96 = **1,0 %** | **falla** |
| **(b)** «veto duro» + «sin rodeo» | 12/96 = **12,5 %** | **cumple** |

### K6 falla por un asiento

| asiento | ms mediana | nacidas |
|---|---|---|
| **K 21098748/10** | **5,5085** | **178** |
| K 20889290/11 | 3,511 | 37 |
| K 20260916/10 | 3,139 | 89 |

**Cero tics perdidos en los 39 asientos.** El que rompe el sello es el que más
formas nace: **cada nacimiento paga un BFS**, y 178 nacimientos en 13.624 tics
suben la mediana. **Es coste de la curiosidad, no un fallo.**

---

## Lo que va sin sello

### Por semilla: por qué unas nacen 10 y otras 383 — **contestado**

| semilla | nacidas | ign. inicial | tics de K | **en seguro** | en inseguro | **nacidas/tic seguro** |
|---|---|---|---|---|---|---|
| 21203477 | **383** | 0,8939 | 24.720 | **18.395 (74,4 %)** | 20,5 % | 0,0208 |
| 21098748 | **345** | 0,8908 | 22.648 | **16.842 (74,4 %)** | 20,1 % | 0,0205 |
| 20365645 | 259 | 0,8919 | 18.239 | 10.381 (56,9 %) | 27,3 % | 0,0249 |
| 20260916 | 165 | 0,8902 | 17.128 | 7.712 (45,0 %) | 25,5 % | 0,0214 |
| 20994019 | 57 | 0,8930 | 17.861 | 2.529 (14,2 %) | 7,7 % | 0,0225 |
| 20679832 | 47 | 0,8954 | 3.423 | 2.177 (63,6 %) | 27,1 % | 0,0216 |
| 20889290 | 45 | 0,8950 | 18.236 | 1.995 (10,9 %) | **83,4 %** | 0,0226 |
| 20575103 | 38 | 0,8902 | 5.025 | 1.552 (30,9 %) | 57,7 % | 0,0245 |
| **20470374** | **11** | 0,8926 | 14.856 | **455 (3,1 %)** | **66,8 %** | 0,0242 |
| **20784561** | **10** | 0,8954 | 4.907 | **385 (7,8 %)** | **91,8 %** | 0,0260 |

**Agregado: 1.360 nacidas / 62.423 tics seguros = una forma cada 46 tics de
entorno seguro.**

**La ignorancia inicial no explica nada: es 0,890-0,895 en las diez.** Lo que
manda es el **tiempo en entorno seguro**, y la razón es casi una constante:
**0,0205 a 0,0260 en las diez semillas**, un rango de ±11 % cuando los
nacimientos varían por un factor de **38**.

**Eso es la respuesta a tu pregunta (4)**, y es más limpia de lo que esperaba:
el disparo de la curiosidad no depende del mapa ni de lo que quede por ver
—depende de **cuánto rato el cuerpo está tranquilo**—. `20470374` nació 11
formas porque vivió el 66,8 % del tiempo en entorno inseguro y solo el 3,1 % en
seguro; `21203477` nació 383 porque vivió el 74,4 % en seguro.

### Aceptación

**96 de 1.360 = 7,1 %** (era 10,2 % con diez partidas).

La dispersión por asiento sigue siendo enorme: de **1,2 %** (`21098748/11`) a
**66,7 %** (`20470374/11`). **Y la W sigue sin explicarla:** los dos asientos de
más aceptación tienen W 0,0 y 0,99; los dos de menos, 2,0 y 2,5. Con
diecinueve asientos, **el signo apunta a que los ricos aceptan menos**, que es
lo contrario de lo que salió en P5-8K. **No lo afirmo.**

### Distancia al nacer × causa de fin

| tramo | n | completada | atasco | veto duro | sin rodeo |
|---|---|---|---|---|---|
| **1-3** | 20 | **20 (100 %)** | 0 | 0 | 0 |
| 4-5 | 41 | 23 (56,1 %) | **13 (31,7 %)** | 1 | 4 |
| 6-7 | 30 | 22 (73,3 %) | 2 (6,7 %) | 0 | **6** |
| 8-9 | 5 | **4 (80 %)** | 0 | 0 | 1 |

**El muro de P5-8L sigue sin aparecer**: el tramo 8-9 completa 4 de 5, cuando
allí eran 0 de 100. **Todas las de 1-3 completan, las veinte.**

### El rodeo

**2 formas de 96 rodearon** (+2 casillas las dos; una completó, la otra no).
**«Sin rodeo» 11.** De los 13 encuentros con un armado cubriendo el camino, **2
tuvieron rodeo y 11 no**. **El rodeo sigue sin probarse en campo**, y el 59 %
medido en seco sobre los vetos de P5-8L no se está reproduciendo aquí: **el
mundo de estas veinte partidas presenta muy pocos de esos encuentros**.

### El compromiso

| | |
|---|---|
| tics con piernas listas | 365 |
| **obedece** | **338 = 92,6 %** |
| rompe | 27 |
| contra el criterio del decisor | **251 = 74,3 %** |
| coste | **+40,844 · +0,1627 por tic** |

| causa | n |
|---|---|
| (e) rival a 2 o menos | 16 |
| (d) carencia sube | 7 |
| (a) veto vital: armado a tiro | 3 |
| (e) armado a menos de 6 y acercándose | 1 |

**Cuatro de siete causas.** Siguen sin verse (b), (c), (f) y (g).

### Lo prometido contra lo visto

**2.888 durante (52,2 %) · 761 después (13,7 %) · 1.888 nunca (34,1 %).**
Prácticamente idéntico al de diez partidas (52,8 / 14,6 / 32,6): **el mejor
reparto de la serie y estable al doblar la muestra.**
Distancia al destino: **4 → 2**.

### W y botín

**La W es idéntica al empezar y al terminar en 91 de 96 formas** (sube en 3,
baja en 2). Confirmado con el doble de muestra: **la forma de curiosidad no
mueve la riqueza**.

| botín, por cien tics | dentro | fuera |
|---|---|---|
| tanda 0 | **1,280** | 0,093 |
| tanda 1 | 0,097 | 0,230 |
| **tanda 2** | 0,157 | **2,093** |
| **acumulado** | **0,481** | **1,344** |

**Retiro la señal de la tanda 1.** Allí dije «3,6 veces más recogidas dentro de
forma»; con veinte partidas el signo se invierte y ahora hay **casi tres veces
menos dentro**. Las semillas de la tanda 2 tienen 1.823 recogidas fuera de
forma. **Era la semilla, no el mecanismo.**

### «Acerca al armado» en inseguro

| | tics con armado a la vista | acerca | |
|---|---|---|---|
| **K** | 52.430 | 579 | **1,1 %** |
| **A** | 45.342 | 1.012 | **2,2 %** |

**K se acerca la mitad que A**, idéntico al acumulado de diez. **Estable.**

---

## Precio

**Tanda 2: 1,026964 $** · $/min mediana **0,01001**, máximo **0,01008** (tope
0,012). Colas de 0,7 a 1,6 min, mediana 1,0. **Ninguna cerca de la vara.**

**Las veinte partidas: 1,805025 $.** **K7 proyectado a cuarenta: 3,61 $**, bajo
el techo de 4 $ **pero justo** — un 10 % de holgura.

---

## Lo que no sé, marcado como tal

**No sé si K2 es real.** Seis de diez semillas con K peor, con la proporción
mantenida al doblar la muestra. **Eso ya no parece ruido, pero diez semillas no
son una prueba**, y no tengo mecanismo: cero muertes dentro de forma, y el
cuerpo se acerca **menos** a los armados que A. **Si la curiosidad cuesta
puesto, no sé por qué.**

**No sé por qué la aceptación bajó del 10,2 % al 7,1 %.** Las semillas nuevas
nacen muchísimas más formas (345 y 383) y aceptan pocas.

**El rodeo sigue sin probarse: 2 de 96.**

**K5 y K3 siguen fallando por sucesos concentrados** — K5 por **un** caso en 96
formas, K3 por **un** asiento de diecinueve.

---

## Propuesta, no ejecución

**El mecanismo aguanta el doblado de muestra en lo que le es propio**:
completadas suben a 71,9 %, el prometido se ve en el 52 %, la segunda mitad de
K1 mejora a 5,20×, y el compromiso obedece el 92,6 % y rompe cuando debe.

**Lo que no aguanta son dos sellos cuyo enunciado mide cosas de las que el
mecanismo no es dueño:**

1. **K1 primera mitad (K/A)** depende de cuánto vive cada brazo, y con asientos
   que mueren a los 441 tics el cociente por tic se dispara. Las tres semillas
   que rompen el agregado son exactamente ésas.
2. **K6** lo rompe el asiento que más formas nace: el BFS del nacimiento es el
   coste, y nacer 178 formas en 13.624 tics sube la mediana por encima de 5 ms.

**Lo digo y no lo decido.** Las dos lecturas de K3 y K4 ya están, como pediste.

**Y lo que más vigilo, como tú: K2 va en la dirección mala y se ha mantenido al
doblar la muestra.**

**Gasto de la tanda: 1,026964 $. Acumulado de la serie: 1,805025 $.** Cola
vacía. **Las veinte restantes no se han lanzado.**

**PARO AQUÍ.**

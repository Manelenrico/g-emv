# P5-8M — La curiosidad como forma, con compromiso y rodeo · LAS CUARENTA

Informe final. Cuarenta partidas, veinte semillas, brazos A y K.
**Sin cambios de mecanismo en toda la serie: una sola imagen, un solo tag.**

---

## El titular

**El mecanismo funciona y el sello que lo mide no lo recoge.**

De las 209 formas aceptadas en veinte partidas, **el 68,9 % se completa**, el
cuerpo las obedece el **92,5 %** de los tics con piernas listas, **cinco de las
siete causas de ruptura han disparado**, y **dentro de forma el cuerpo descubre
5,81 veces más** que fuera.

**Pero K1 —el sello que preguntaba si la curiosidad hace explorar más— falla, y
falla de la única manera que no admite excusa.** Su segunda mitad cumple con
holgura (5,81× contra un umbral de 2). Su primera mitad, la que compara K contra
A en toda la vida, da **1,11**, y **emparejando cada asiento con su gemelo de A
en la ventana en que los dos viven, 1,16** — un número que no se ha movido en
diez, quince y veinte semillas (1,16 · 1,15 · 1,16).

**La lectura honesta: la forma de curiosidad descubre mucho mientras corre, pero
corre el 2,2 % del tiempo. Un cuerpo que explora intensamente el 2 % de su vida
explora, en total, un 16 % más que uno que no lo hace.**

**Y lo que más se vigilaba —si la curiosidad cuesta la vida o el puesto— cierra
sin señal:** vida **p = 0,503**, puesto **p = 1,000**, con los dos intervalos
cruzando el cero. **No cuesta nada, y tampoco da nada.**

---

## Custodia

```
                            al empezar de cada tanda            al acabar
motor/model.py              1e511978c251130e95169ebf8443efa1    idéntico
paintball/alma/decisor_zs.py
                            8fa03547e3228ef9df4aa94c444f9252    idéntico
paintball/alma/appraisal_zs_v42_exp.py
                            98c13d60167c80cc8334c965be75c640    idéntico
```

### La imagen — **una sola en las cuarenta**

| | |
|---|---|
| etiqueta | **`gemv-anima:curforma-m0`** |
| id | `sha256:68faccb52f23415012f2d596f9d12a2943c4cf157bc27eb457f046aab234f7a4` |

md5 **leídos dentro de la imagen y comprobados antes de cada una de las cuatro
tandas**:

```
motor/model.py                1e511978c251130e95169ebf8443efa1
alma/decisor_zs.py            8fa03547e3228ef9df4aa94c444f9252
alma/appraisal_zs_v42_exp.py  98c13d60167c80cc8334c965be75c640
alma/policy_forma.py          896e97a0cca1efcb736596e0b8b15cea
alma/curiosidad_forma.py      141ecb2eb17f76654caf4bbf3c29c642
alma/forma_viva.py            b2c87c93f0ed47e48fd8991a5a797a42
alma/humo_curforma.py         1660fb118bb2287f036bdb02c74fc11e
alma/forma.py                 b801876afda071403c5af54a28feff85   (sin tocar)
alma/confianza_viva.py        6e1e444435914f0b9df287ea37555bbc   (sin tocar)
```

Políticas `gemv-p58m-A:v1` (`939269d2-…`) y `gemv-p58m-K:v1` (`68e4de97-…`).

### La comparación está pareada de verdad

Comprobado en los cuarenta pares de episodios: **las listas de políticas
coinciden elemento a elemento en las veinte semillas** — mismo mapa, mismos
siete rivales, en los mismos puestos, y nuestra política en los asientos 10 y
11. **Lo único que cambia es el brazo.**

### Dos asientos perdidos por la plataforma

**79 asientos de 80.** `K/20784561` asiento 10 no tiene artefacto (`Agent 10 has
no artifact`); el episodio acabó y el asiento tiene puntuación, pero no subió su
diario. Reintentado, no existe.

**Y un episodio sin facturar**: `A/21622393`, `completed` con `cost_usd = null`.
Es el tercero de todo el paper cinco.

---

## Los siete sellos

| | sello | acumulado de las cuarenta | |
|---|---|---|---|
| **K1** | K/A ≥ 1,5 **y** dentro ≥ 2× fuera | **1,11** (emparejado **1,16**) · **5,81×** | **FALLA** la primera mitad |
| **K2** | cero muertes dentro; puesto no baja | 0 muertes; **sin señal** (p = 1,000) | **sin señal en ninguna dirección** |
| **K3** | cero decisiones con armado a tiro en forma activa | **(a) 52 · (b) 5** | **FALLA las dos lecturas** |
| **K4** | completadas ≥ 50 %; veto duro 5-30 % | **68,9 %** · **(a) 1,0 % · (b) 20,1 %** | **CUMPLE con la lectura (b)** |
| **K5** | daño ≤ base de A | **0,5 %** contra **0,5 %** | **CUMPLE** |
| **K6** | < 5 ms mediana; cero perdidos | un asiento a **5,51 ms**; **cero perdidos** | **FALLA por un asiento** |
| **K7** | ≤ 4 $ la serie | **3,439826 $** | **CUMPLE** |

**Cumplen tres (K4 con lectura, K5, K7), fallan tres (K1, K3, K6), y K2 no dice
nada.**

### K1 en sus dos mitades, y emparejado

| | K | A | razón |
|---|---|---|---|
| **toda la vida** | 8,93 | 8,08 | **1,11** |
| **emparejado** (ventana en que los dos viven) | 11,34 | 9,75 | **1,16** |
| **dentro / fuera de forma** | **46,95** | 8,08 | **5,81×** |

**El emparejado es estable y no rescata el sello:** 1,16 con diez semillas, 1,15
con quince, **1,16 con veinte**. Las razones por asiento van de 0,93 a 1,43.

**Las dos mitades dicen cosas distintas y las dos son verdad:** mientras la forma
corre, el cuerpo descubre **seis veces más**; como corre el **2,2 %** del tiempo,
el total sube un **16 %**.

> **Ésta es la figura F1**: la mediana de K va por debajo de la de A durante toda
> la vida, pero por poco.

### K2, con intervalo — **cierra sin señal**

Diferencia K − A por semilla, veinte semillas emparejadas, prueba de signos
exacta e intervalo por bootstrap:

| | mediana | **IC 95 %** | K mejor / peor | **p** |
|---|---|---|---|---|
| **vida** (tics vivo) | **−466,5** | **[−1.696,5, +3.707,8]** | 8 / 12 | **0,503** |
| **puesto** | **+0,5** | **[−2,8, +2,5]** | 9 / 10 | **1,000** |

**Los dos intervalos cruzan el cero con holgura y ninguna prueba se acerca a la
significación.** Cero muertes dentro de forma en las 209.

**Esto retira definitivamente la alarma de la tanda 2**, donde con diez semillas
salió «K peor en 6» y escribí que «ya no lo llamaría ruido». **Era ruido.** Con
veinte semillas el signo se ha invertido dos veces.

### K3, las dos lecturas

| | |
|---|---|
| **(a) sellada** — todo tic con forma activa | **52** de 7.135 tics dentro (0,73 %) |
| **(b) del mecanismo** — solo con piernas listas | **5** de 810 tics (0,62 %) |

Salen de **tres asientos de treinta y nueve**; los otros treinta y seis dan cero.
**Y los 5 de la lectura (b) son exactamente las 5 rupturas «(a) veto vital».**

**Comprobado en código y en datos**: en los tics de enfriamiento **manda el
decisor entero**. `_compromiso` sale antes si `move_ready_in > 0` y devuelve la
acción del decisor sin tocarla; la receta de la forma es `tipo: "ir"` y
`_veta_receta` la manda al prefijo `ir_`, que `Bloqueos.veta` tumba — la misma
regla que veta los `ir_` del propio cuerpo; y medido, el candidato `_FM_` aparece
**0 de 1.825** tics de enfriamiento contra **221 de 221** con piernas listas.

**En los 47 tics de enfriamiento que el sello carga a K, el cuerpo se comportó
exactamente como el de A.**

### K4, las dos lecturas del veto duro

| causa de fin | n | % |
|---|---|---|
| **completada por alivio** | **144** | **68,9 %** |
| **sin rodeo** | 40 | 19,1 % |
| atasco | 23 | 11,0 % |
| veto duro | 2 | 1,0 % |

| banda (sello 5-30 %) | | |
|---|---|---|
| **(a)** solo «veto duro» | 1,0 % | **falla** |
| **(b)** «veto duro» + «sin rodeo» | **20,1 %** | **cumple** |

**Las dos son abandono por peligro. El sello se escribió en P5-8B, antes de que
«sin rodeo» existiera.** La lectura es de la mesa.

### K6, y por qué falla

Un asiento de treinta y nueve, `21098748/10`, con **5,5085 ms** de mediana.
**Cero tics perdidos en los treinta y nueve.**

**Y no es el BFS del nacimiento.** Separando los tics con nacimiento de forma de
los que no:

| | ms con nacimiento | ms sin nacimiento | × |
|---|---|---|---|
| el asiento que rompe el sello | **5,686** | **5,504** | **1,0** |
| mediana de las medianas | **0,908** | 0,994 | **1,0** |

**Nacer no cuesta. Ese asiento es lento en todos sus tics, y no sé por qué.**

---

## La ley del tiempo seguro — el hallazgo más limpio de la serie

**Lo que decide si una semilla nace 10 formas o 383 es cuánto tiempo pasa el
cuerpo en entorno seguro, y nada más.**

| | veinte semillas |
|---|---|
| **ignorancia inicial** | **0,8902 a 0,8954** — sin variación |
| **nacidas** | **10 a 383** — un factor de **38** |
| **razón nacidas / tic seguro** | **0,0205 a 0,0313** — un factor de **1,53** |
| agregado | **2.727 nacidas / 116.075 tics seguros = una forma cada 43 tics de entorno seguro** |

`20784561` nació **10** formas con el **7,8 %** del tiempo en seguro;
`21203477` nació **383** con el **74,4 %**. **La ignorancia inicial es la misma
en las veinte: no es que unas semillas tengan más que ver.**

---

## Lo que va sin sello

### Aceptación y suelo de serie

**209 aceptadas de 2.727 propuestas = 7,7 %.** El suelo de serie era **150 en
las cuarenta**: **cumplido con 209**, un 39 % de holgura.

La dispersión por asiento sigue sin explicarse: de **1,2 %** a **66,7 %**.

### Distancia al nacer × causa de fin

| tramo | n | completada | atasco | veto duro | sin rodeo |
|---|---|---|---|---|---|
| **1-3** | 29 | **29 (100 %)** | 0 | 0 | 0 |
| 4-5 | 81 | 43 (53,1 %) | 14 (17,3 %) | 1 | **23** |
| **6-7** | 82 | **62 (75,6 %)** | 7 (8,5 %) | 1 | 12 |
| 8-9 | 15 | 8 (53,3 %) | 2 | 0 | 5 |
| 10+ | 2 | **2 (100 %)** | 0 | 0 | 0 |

**Las veintinueve formas nacidas a tres casillas o menos completan todas.** Y el
muro de P5-8L —donde el tramo 8-9 daba **100 % de veto duro y cero llegadas**—
**ha desaparecido por completo**: aquí ese tramo completa el 53 %.

### El rodeo

| | |
|---|---|
| formas que rodearon | **8 de 209** |
| casillas extra | mediana **0** (de −2 a +3) |
| completan: rodearon | **5 / 8 = 62,5 %** |
| completan: no rodearon | 139 / 201 = 69,2 % |
| abandonos por **«sin rodeo»** | **40** |

**De los 48 encuentros con un armado cubriendo el camino, 8 encontraron rodeo =
17 %.** En seco sobre los vetos de P5-8L medí **59 %**. **La diferencia no la
explico**, y con 48 casos ya no es ruido.

**Lo que sí hizo el rodeo, y era su razón de ser:** el veto duro pasó de matar el
**93,6 %** de las formas en P5-8K a **1,0 %** aquí.

### El compromiso

| | |
|---|---|
| tics con piernas listas | 810 |
| **obedece** | **749 = 92,5 %** |
| rompe | 61 |
| **contra el criterio del decisor** | **558 = 74,5 %** |
| coste | **+88,588 total · +0,1588 por tic** |

| causa de ruptura | n |
|---|---|
| (e) rival a 2 o menos | **38** |
| (d) carencia sube (pierde de las manos) | **16** |
| (a) veto vital: armado a tiro | **5** |
| (b) veto duro: cubre el camino | **1** |
| (e) armado a menos de 6 y acercándose | **1** |

**Cinco de las siete causas han disparado en campo.** Faltan (c) daño recibido y
(f)/(g), que las aplican `_revisa_vivas` y `_abandonos_K`.

**En P5-8H, P5-8I y P5-8K no disparó ninguna.** El compromiso deja de ser
obediencia ciega.

### Lo prometido contra lo visto

**6.081 durante (47,9 %) · 1.816 después (14,3 %) · 4.807 nunca (37,8 %).**

La progresión de toda la serie:

| | durante | después | **nunca** |
|---|---|---|---|
| P5-8F | 16,7 % | 6,3 % | **76,9 %** |
| P5-8K (margen 0,02, sin rodeo) | 2,8 % | 0,9 % | **96,3 %** |
| **P5-8M, las cuarenta** | **47,9 %** | 14,3 % | **37,8 %** |

Distancia al destino: **4 → 2**.

### W y botín

**La W es idéntica al empezar y al terminar en 198 de 209 formas.** La forma de
curiosidad **no mueve la riqueza**.

| botín por cien tics | dentro | fuera |
|---|---|---|
| | **1,626** | **2,044** |

**Hay menos recogidas dentro de forma que fuera.** *(La señal contraria que di en
la tanda 1 —«3,6 veces más dentro»— quedó retirada en la tanda 2 y sigue
retirada.)*

### «Acerca al armado» en inseguro

| | tics con armado a la vista | acerca | |
|---|---|---|---|
| **K** | 108.418 | 1.253 | **1,2 %** |
| **A** | 97.716 | 2.085 | **2,1 %** |

**K se acerca a los armados la mitad que A**, estable en las cuatro tandas. El
veto vital y el de sombra hacen su trabajo.

---

## Precio

| | |
|---|---|
| **total de las cuarenta** | **3,439826 $** (39 facturadas) |
| **$/min mediana** | **0,00992** |
| **$/min máximo** | **0,01008** — tope 0,012, **ninguna lo pasó** |
| cola mediana | **1,0 min** (máximo 2,1) |
| por tanda | 0,126 · 0,778 · 1,027 · 0,779 · 0,855 $ |

**La vara por minuto funcionó**: en cuarenta partidas no hubo una sola parada por
precio, y la cola se mantuvo entre 0,2 y 2,1 minutos.

---

## Las figuras

**`F1_P58M_ignorancia.png`** — la ignorancia global a lo largo de la vida, 39
asientos de K contra 40 de A, con la mediana por brazo sobre los asientos vivos
(se dibuja mientras quedan cinco o más). **La mediana de K va por debajo de la de
A durante toda la vida**, y la distancia entre las dos es el 16 % que mide K1
emparejado.

**`F2_P58M_una_vida.png`** — una vida de K (`20260916` asiento 11, 18 formas
aceptadas) con cada forma coloreada por su causa de fin sobre la curva de
ignorancia. **Se ven las dos cosas que la serie descubrió**: las formas cortas
que completan al principio, y la racha de atascos del medio.

Las dos de los datos crudos con matplotlib, reconstruyendo el `Ojo` de los
diarios. **Ninguna de MettaScope.**

---

## Lo que no sé, marcado como tal

**No sé por qué la aceptación va del 1,2 % al 66,7 % entre asientos.** Cuatro
tandas y veinte semillas no lo han aclarado, y la riqueza W apunta en
direcciones distintas según la muestra.

**No sé por qué el rodeo aparece en el 17 % de los encuentros** cuando el
contrafactual en seco de P5-8L daba el 59 %. O esos encuentros son de otra clase,
o mi contrafactual sobreestimaba.

**No sé por qué un asiento es lento en todos sus tics.** El BFS del nacimiento
queda descartado con datos.

**No sé por qué en diez semillas K recoge mucho menos botín que A.** P5-8N
descartó la fila de ignorancia (no está instalada) y descartó el tiempo de las
formas (2,2 %), y no encontró el mecanismo.

**Y no sé si 1,16 es poco.** El sello pedía 1,5 y salió 1,16; si el umbral era el
correcto no lo dice el dato.

---

## Errores míos en la serie, y qué los cazó

Los dejo juntos porque tres de ellos los publiqué antes de tener muestra.

| | qué dije | qué era | qué lo cazó |
|---|---|---|---|
| tanda 2 | «K2 ya no lo llamaría ruido» (6 de 10 en contra) | **ruido**: el signo se invirtió dos veces | doblar la muestra |
| tanda 2 | «el agregado de K1 lo estropean los asientos que mueren pronto» | **falso**: emparejando, el cociente **baja** | las ventanas emparejadas |
| tanda 2 | «K6 lo rompe el asiento que más nace, cada nacimiento paga un BFS» | **falso**: ×1,0 | el ms separado por nacimiento |
| tanda 1 | «3,6 veces más botín dentro de forma» | **era la semilla**; con 40 partidas el signo se invierte | doblar la muestra |
| P5-8N | contrafactual de la fila = «0 cambios» | **mío**: no rellené `dist_frontera` | los contadores del propio módulo |

**Las tres primeras son la misma falta: dar una explicación con diez o veinte
partidas cuando la serie tenía cuarenta.** Las lecturas que pediste en las tandas
3 y 4 son las que las desmontaron.

---

## Lo que esto deja — propuesta, no ejecución

**El mecanismo está terminado y funciona**: nace, pasa una puerta honesta, el
cuerpo se compromete y la obedece el 92,5 %, la rompe por cinco causas distintas
cuando debe, rodea cuando puede, llega en el 68,9 % de los casos, y ve la mitad
de lo que prometió. **Cuesta 3,44 $ y no cuesta ni vida ni puesto.**

**Lo que no consigue es mover la aguja de la exploración total**, porque ocupa el
2,2 % de la vida del cuerpo. **Para que K1 diera 1,5 haría falta que la forma
corriera mucho más tiempo**, y las dos maneras de conseguirlo —bajar el margen o
alargar los viajes— **ya se probaron y rompieron otras cosas** (P5-8K: margen
0,02 sin rodeo → 96,3 % de «nunca»; P5-8L: viajes de 8-9 → 100 % de veto duro).

**No propongo un P5-8Ñ.** Creo que el resultado de la serie es éste: **una forma
de curiosidad que se comporta bien cuesta poco y explora poco, y la razón es
aritmética, no de diseño.** Si la mesa quiere más exploración, la palanca no está
en la forma sino en cuánto tiempo el cuerpo está tranquilo — que es lo que la ley
del tiempo seguro dice.

**Gasto de la serie: 3,439826 $.** Cola vacía. Custodia idéntica.

**PARO AQUÍ.**

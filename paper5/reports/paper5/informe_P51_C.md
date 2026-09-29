# P5-1 fase C — La calma y el precio del mundo lento

Dos partidas más, semillas 2 y 3, una petición cada una, con la cola comprobada
vacía antes de cada creación. Con la de B1 son **tres partidas y seis
asientos-partida**.

**El titular, y no es el que esperábamos.** El mundo lento **no dio ni un
instante de calma literal**: cero de 37.750 instantes vivos, exactamente como el
paper cuatro. Y lo que la impide no es el anillo. Es el hambre, que está
encendida al máximo en el primer instante de vida y no se apaga nunca.

---

## Las tres partidas

| | B1 | C2 | C3 |
|---|---|---|---|
| semilla | 20260916 | 20365645 | 20470374 |
| petición | `xreq_505e8f3b…` | `xreq_bdd84d70…` | `xreq_876f0688…` |
| episodio | `ereq_50c6300c…` | `ereq_e4a28906…` | `ereq_ba80a7e2…` |
| creada | 14:39:28 Z | 15:03:38 Z | 15:15:33 Z |
| arranque | 14:40:28 Z | 15:04:15 Z | 15:15:58 Z |
| fin | 14:50:54 Z | 15:14:47 Z | 15:25:36 Z |
| cola | 16,3 s | 29,2 s | 21,1 s |
| corriendo | 625,3 s | 631,5 s | 577,9 s |
| `cost_preview` | 2,2414 créditos | 2,2383 | 2,2349 |

Las tres con `lento_v0.json` sin tocar, la misma imagen `gemv-p5-A:v1`
(sha `495c04a7…`, en el acta), los mismos catorce rivales y nuestros asientos 10
y 11. La cola dio 0 peticiones pendientes antes de cada una de las tres.

### La duración, con el mensaje de cierre

El diario trae un registro `final` al acabar. Del asiento que más vivió en cada
partida:

| partida | asiento | `match_ticks` | `reason` | `placement` | `kills` | `score` |
|---|---|---|---|---|---|---|
| B1 | 10 | **12.457** | `eliminated` | 7 | 0 | 5 |
| C2 | 10 | **13.921** | `eliminated` | 6 | 0 | 6 |
| C3 | 11 | **968** | `eliminated` | 14 | 0 | 1 |

**Aviso de lectura, y es importante.** El `reason` es `eliminated` en los seis
asientos, nunca `match_end`. O sea que `match_ticks` es **el instante en que
murió ese asiento**, no el final del episodio. Es una cota inferior de la
duración, no la duración. La prueba está en C3: nuestros dos asientos murieron
hacia el tic 968 y el episodio siguió corriendo 578 segundos de reloj. Por el
reloj de pared las tres partidas apuntan a los 18.240 tics enteros, pero **eso es
estimación**, no medida, y así queda marcado.

---

## C1 · La calma

**Los criterios, declarados.**

- **Literal**: ninguna fila del presente con `M > 0,1` **y** ningún armado a la
  vista. Es literalmente el de `cantera/paper4/la_calma.py:63-64`.
- **Declarada**: ninguna fila de las familias **F-** y **S-** por encima de 0,1
  y ningún armado a la vista. Las filas **R-** pueden estar encendidas. Es mi
  lectura de «solo F y S en reposo»: deja pasar el hambre, que es lo que el
  encargo separa, y usa el mismo umbral 0,1 para que las dos se comparen.
- **Armado**: agente visible que no es el hermano y cuya mano no es `none` ni
  `net` (`la_calma.py:9-10`).
- **La medida del paper cuatro**: ninguna fila con `M > 0`, el criterio exacto
  de `cantera/paper4/calma_S2.py:5`.

| asiento-partida | tics vivos | calma literal | calma declarada | medida del paper 4 |
|---|---|---|---|---|
| B1 / 10 | 11.976 | **0** (0,00 %) | 1 (0,01 %) | 0 |
| B1 / 11 | 376 | **0** (0,00 %) | 0 (0,00 %) | 0 |
| C2 / 10 | 13.440 | **0** (0,00 %) | **6.257 (46,56 %)** | 0 |
| C2 / 11 | 11.017 | **0** (0,00 %) | 567 (5,15 %) | 0 |
| C3 / 10 | 454 | **0** (0,00 %) | 13 (2,86 %) | 0 |
| C3 / 11 | 487 | **0** (0,00 %) | 21 (4,31 %) | 0 |
| **total** | **37.750** | **0 (0,00 %)** | **6.859 (18,17 %)** | **0** |

**Cero calma literal en los seis.** Y cero también con la medida del cuatro: no
hay un solo instante, de 37.750, sin ninguna fila encendida. Doblar la partida,
doblar la congelación inicial y retrasar el anillo del 16 % al 40 % **no cambió
esa cifra en nada**.

**La calma declarada sí aparece, y varía muchísimo**: del 0 % al 46,6 %. Lo que
la explica no es el anillo, es **cuándo te pegan**. El asiento 10 de C2 no
recibió un golpe hasta el tic 12.409, y el golpe fue del anillo; el 46,6 % de su
vida cabe en calma declarada. Al asiento 11 de B1 lo mataron en el 857 y su
hermano arrastró las filas de la pareja muerta y la soledad encendidas durante
los once mil instantes siguientes.

## C7 · El primer tramo de calma, desde el pedestal

Desde el tic 481, el primero de vida, hasta la primera fila que supera 0,1:

| asiento-partida | tramo literal | lo rompe | tramo declarado | lo rompe |
|---|---|---|---|---|
| los **seis** | **0 tics** | tic **481**, `R-CARENCIA` = **1,0** | **0 tics** | tic **481**, `F-4-ALCANCE` ≈ **0,47** |

Los seis dan el mismo resultado y por la misma razón. **No hay tramo.** En el
primer instante en que el cuerpo puede moverse, el hambre ya está al máximo
—sales del pedestal sin nada en la mano, y `R-CARENCIA` mide justo eso— y ya hay
alguien que puede alcanzarte. El anillo, que es lo único que este encargo movió,
todavía tardará **6.816 instantes** en avisar.

## C2 · Qué hace el cuerpo en calma

| asiento-partida | dónde | tics | noop | ir_centro | ir_botin | otros | casillas nuevas por 100 tics |
|---|---|---|---|---|---|---|---|
| B1 / 10 | en calma | 1 | 100,00 % | — | — | — | 33,00 (n = 1) |
| B1 / 10 | fuera | 11.975 | 88,63 % | 0,16 % | 3,75 % | 7,47 % | 6,62 |
| B1 / 11 | fuera | 376 | 88,03 % | 2,39 % | 0,00 % | 9,57 % | 182,98 |
| C2 / 10 | en calma | 6.257 | 90,79 % | 0,00 % | 0,10 % | 9,11 % | 2,17 |
| C2 / 10 | fuera | 7.183 | 89,24 % | 0,43 % | 0,93 % | 9,40 % | 10,64 |
| C2 / 11 | en calma | 567 | 90,83 % | 0,00 % | 1,59 % | 7,58 % | 17,11 |
| C2 / 11 | fuera | 10.450 | 83,22 % | 3,50 % | 0,23 % | 13,05 % | 7,38 |
| C3 / 10 | en calma | 13 | 92,31 % | 0,00 % | 0,00 % | 7,69 % | 0,00 |
| C3 / 10 | fuera | 441 | 90,48 % | 1,81 % | 0,91 % | 6,80 % | 147,39 |
| C3 / 11 | en calma | 21 | 90,48 % | 0,00 % | 9,52 % | 0,00 % | 80,95 |
| C3 / 11 | fuera | 466 | 88,41 % | 0,86 % | 0,43 % | 10,30 % | 148,28 |

Sumando los seis:

| | en calma declarada | fuera |
|---|---|---|
| tics | 6.859 | 30.891 |
| **noop** | **90,80 %** | 86,95 % |
| casillas nuevas por 100 tics | **4,13** | **14,10** |

**En calma el cuerpo está más quieto, no menos, y ve menos mundo, no más.** Se
queda quieto nueve de cada diez instantes y descubre tres veces y media menos
casillas nuevas que cuando algo le aprieta. La calma no le da curiosidad: le da
inmovilidad. (El B1/10 «en calma» es un solo instante y su cifra de casillas no
significa nada; se deja por honradez del recuento.)

## C3 · Qué fila manda, y las dos erres

La fila con mayor `M` en cada instante:

| asiento-partida | la que más manda | segunda | tercera |
|---|---|---|---|
| B1 / 10 | F-DANO 59,10 % | S-SOLEDAD 19,22 % | S-MUERTE-PAREJA 18,45 % |
| B1 / 11 | F-4-ALCANCE 64,36 % | R-CARENCIA 21,01 % | F-DANO 14,36 % |
| C2 / 10 | **R-CARENCIA 68,35 %** | S-MUERTE-PAREJA 16,41 % | S-HERIDO 11,68 % |
| C2 / 11 | **R-CARENCIA 75,62 %** | F-DANO 24,38 % | — |
| C3 / 10 | **R-CARENCIA 53,30 %** | S-HERIDO 46,70 % | — |
| C3 / 11 | F-DANO 50,31 % | R-CARENCIA 35,93 % | F-4-ALCANCE 9,24 % |

Y las dos erres, en los seis asientos-partida:

| fila | tics vivos en que está viva (`M > 0`) |
|---|---|
| **R-CARENCIA** | **37.750 de 37.750 = 100,00 %** |
| **R-LLAMADA** | **37.750 de 37.750 = 100,00 %** |

Las dos, siempre. En los seis asientos, en los 37.750 instantes.

**Por qué no hay calma, dicho con las cifras del asiento que más vivió** (B1/10,
filas por encima de 0,1 sobre sus 11.976 instantes):

| fila | veces por encima de 0,1 |
|---|---|
| R-CARENCIA | 100,0 % |
| R-LLAMADA | 99,7 % |
| R-ACOPIO | 98,7 % |
| S-MUERTE-PAREJA | 96,9 % |
| F-DANO | 96,7 % |
| S-SOLEDAD | 95,7 % |
| F-4-ALCANCE | 62,6 % |

Y lo que pasa por dentro, mirando la misma vida instante a instante:

| tic | vida | filas por encima de 0,1 |
|---|---|---|
| 600 | 100 | F-4-ALCANCE 0,487 · R-CARENCIA **1,0** · R-LLAMADA 0,185 · R-ACOPIO 0,18 · S-8-EXPOSICION 0,18 |
| 1.500 | 40 | F-DANO 0,644 · S-MUERTE-PAREJA 0,869 · S-SOLEDAD 0,447 · R-CARENCIA 0,411 · … |
| 6.000 | 40 | F-DANO **0,644** · S-MUERTE-PAREJA 0,434 · S-SOLEDAD **0,5** · R-CARENCIA **0,411** |
| 9.000 | 40 | los mismos, y los mismos valores |

**F-DANO no es «me están pegando ahora»: es vida que falta.** Con la vida clavada
en 40 se queda en 0,644 durante nueve mil instantes seguidos, sin que nadie le
toque. **S-SOLEDAD se queda en 0,5** desde que el hermano muere. **R-CARENCIA se
queda en 0,411** porque sigue mal equipado. Ninguna de las tres tiene nada que
ver con el reloj del anillo, y las tres solas bastan para que no haya calma.

## C4 · El anillo, la duración y las muertes

| suceso | pedido en `lento_v0` | medido |
|---|---|---|
| encendido | tic 480 | `ignition` en el **481**, en las tres partidas |
| primer aviso del anillo | tic 7296 | `zone_warning` en el **7297**, en B1 y C2 |
| inundación | tic 4400 | `flood` en el **4281**, en B1 y C2 |

En C3 **ningún asiento nuestro llegó a ver el anillo**: los dos murieron hacia el
tic 950, seis mil instantes antes del primer aviso.

| asiento-partida | tics vivos | muere en | puesto | causa |
|---|---|---|---|---|
| B1 / 10 | 11.976 | 12.457 | 7 | **el anillo** (`source: zone`, fuera del radio, vida 5) |
| B1 / 11 | 376 | 857 | 15 | asiento 13, `zero-sum-example` |
| C2 / 10 | 13.440 | 13.921 | 6 | **el anillo** (`source: zone` en los tics 13.873 y 13.897) |
| C2 / 11 | 11.017 | 11.498 | 11 | **no consta**: último golpe registrado en el 8.830, y luego 2.667 instantes con un punto de vida |
| C3 / 10 | 454 | 935 | 15 | asiento 13, `zero-sum-example` |
| C3 / 11 | 487 | 968 | 14 | **no consta** el golpe final; el último registrado, del asiento 13, en el 827 |

Dos de los seis mueren por el anillo y los cuatro restantes a manos de otro,
siempre dentro de los primeros mil instantes salvo C2/11. **El diario no guarda
el golpe que mata**: el cuerpo deja de recibir observaciones al morir, así que en
dos casos la causa no consta y no la deduzco.

## C6 · Primer armado, primer daño y muerte, con la política detrás

Contado desde el tic 481.

| asiento-partida | primer armado a la vista | primer daño recibido | muerte |
|---|---|---|---|
| B1 / 10 | tic **533** · asiento 8, `ryanschiller-zero-sum-player-v1` (lanza) | tic **875** · asiento 13, `zero-sum-example` | 12.457 · el anillo |
| B1 / 11 | tic **622** · asiento 8, `ryanschiller-zero-sum-player-v1` (lanza) | tic **733** · asiento 8, `ryanschiller-zero-sum-player-v1` | 857 · asiento 13, `zero-sum-example` |
| C2 / 10 | tic **581** · asiento 6, `belobog` (espada) | tic **12.409** · **el anillo** | 13.921 · el anillo |
| C2 / 11 | tic **537** · asiento 13, `zero-sum-example` (lanza) | tic **8.758** · asiento 2, `relh-zero-sum` | 11.498 · no consta |
| C3 / 10 | tic **537** · asiento 12, `aaron-zs-fable` (cuchillos) | tic **791** · asiento 13, `zero-sum-example` | 935 · asiento 13, `zero-sum-example` |
| C3 / 11 | tic **548** · asiento 12, `aaron-zs-fable` (cuchillos) | tic **642** · asiento 13, `zero-sum-example` | 968 · no consta (último registrado, asiento 13) |

**Dos lecturas.** La primera: en los seis casos hay un rival armado a la vista
antes del tic **622**, o sea dentro de los seis segundos siguientes a bajar del
pedestal. La segunda: **`zero-sum-example`, en el asiento 13, hizo el primer daño
a tres de los seis y mató a dos**. Es el mismo vecino de asiento en las tres
partidas, porque el asiento lo fija el roster y no la semilla.

## C5 · El precio

| partida | cola | corriendo | vida del pod | coste | $/min de vida |
|---|---|---|---|---|---|
| B1 | 16,3 s | 625,3 s | 10,69 min | **0,052471 $** | 0,00491 |
| C2 | 29,2 s | 631,5 s | 11,01 min | **0,041511 $** | 0,00377 |
| C3 | 21,1 s | 577,9 s | 9,98 min | **0,035993 $** | 0,00361 |
| **mediana** | | | | **0,041511 $** | |

| gasto acumulado cobrado | episodios | dólares |
|---|---|---|
| antes de B1 | 223 | 79,837381 |
| antes de la fase C | 224 | 79,889852 |
| **después de la fase C** | **226** | **79,967356** |

Las tres partidas juntas costaron **0,129975 $**. El tope de serie del encargo
original eran 25 $.

---

## Cotejo de las predicciones selladas

| | predicción | contador | medido | veredicto |
|---|---|---|---|---|
| **P1** | precio > 0,742 y entre 0,8 y 2,0 $ | mediana del precio por episodio (C5) | **0,041511 $** | **FALLA** |
| **P1 bis** | un céntimo por minuto de vida del pod ± 30 % | coste ÷ minutos de vida del pod | **0,00491 · 0,00377 · 0,00361** | **FALLA** |
| **P1 bis** | con cola vacía, menos de 0,25 $ | precio del episodio | 0,0525 · 0,0415 · 0,0360 | **CUMPLE** |
| **P2** | calma literal > 0 y < 10 % | fracción de tics vivos (C1) | **0,00 %** | **FALLA** |
| **P2** | calma declarada entre 10 % y 40 % | fracción de tics vivos (C1) | **18,17 %** | **CUMPLE** |
| **P3** | R-CARENCIA viva en > 80 % | fracción de tics vivos con R-CARENCIA (C3) | **100,00 %** | **CUMPLE** |
| **P4** | en calma, noop > 70 % | reparto de acciones (C2) | **90,80 %** | **CUMPLE** |
| **P4** | en calma, no más casillas nuevas que fuera | casillas nuevas por 100 tics (C2) | **4,13 contra 14,10** | **CUMPLE** |
| **P5** | un asiento vivo al arranque del anillo en las tres | quién pasa del tic 7297 (C4) | **2 partidas de 3** | **FALLA** |

**Los contadores podían variar, comprobado uno a uno.** El precio por episodio
varió entre 0,036 y 0,052 dentro de estas tres, y en las series anteriores había
llegado a 2,07. La calma declarada varió entre el 0 % y el 46,6 % según el
asiento, así que el 18,17 % del total no es un número forzado. El noop podría
haber bajado: fuera de calma está en el 86,95 %, y en asientos sueltos de S-2
había bajado más. Las casillas nuevas por cien tics van de 0,00 a 182,98 según
el asiento. Y P5 podía cumplirse: en dos de las tres partidas se cumplió.

### P1, y por qué falla

**P1 falla, y falla en la causa antes que en la cifra.** Se selló diciendo que el
precio subiría «porque la partida es más larga». **El precio no depende de la
duración de la partida.** Ya lo avisé en la fase A, con los 257 episodios de S-2
y S-3: la configuración fue idéntica en los 257 y el coste seguía la **espera en
cola** con una correlación de +0,90, contra +0,18 con el tiempo de corrida. Aquí
la partida es el doble de larga y ha costado **catorce veces menos** que la
mediana de S-3, sencillamente porque la cola estaba vacía.

### P1 bis, y lo que sigue sin cuadrar

La segunda cláusula cumple con holgura. La primera falla en las tres, y falla
siempre por el mismo lado: **0,0036 a 0,0049 $ por minuto de vida del pod**,
contra la banda sellada de 0,0070 a 0,0130. En S-2 y S-3 ese mismo cociente
estaba pegado a un céntimo, con un p10-p90 de 0,00979 a 0,01006. Ahora está en
la mitad o menos, y de forma consistente.

**Y hay algo que la regla del minuto no explica.** C2 corrió **más** que B1
(631,5 s contra 625,3) y costó **menos** (0,0415 contra 0,0525). Con más
instantes vividos por nuestros dos asientos: 24.457 en C2 contra 12.352 en B1.
Más juego, menos dinero. Probé tres explicaciones y las tres fallan:

- que se cobre solo lo que corre: daría 0,00504 $/min en B1, la mitad del de S-2;
- que se cobren los instantes vividos por nuestros asientos: la correlación
  sobre los 130 episodios de S-2 con los dos diarios es de solo **+0,26**, y en
  estas tres la relación sale **al revés**;
- que el `cost_preview` sirva de regla de tres: los tres previews son casi
  iguales (2,2414 · 2,2383 · 2,2349) y los precios reales difieren en un 46 %.

**No sé qué fija el precio y no me lo invento.** Lo que sí queda establecido con
seis series de datos es lo que **no** lo fija: ni la duración configurada, ni el
tiempo de corrida, ni lo que vivan nuestros asientos.

---

## Lo que esta fase deja dicho

1. **Alargar el mundo no da calma.** Con la partida al doble, la congelación al
   máximo que el campo permite y el anillo retrasado del 16 % al 40 %, la calma
   literal sigue siendo **cero de 37.750**. La razón sigue sin tener sitio, y no
   es por el anillo.
2. **Lo que mantiene la tabla encendida es memoria, no amenaza.** El hambre
   arranca a 1,0 en el primer instante de vida; la vida que falta deja F-DANO
   clavado; un hermano muerto deja dos filas encendidas para siempre. Ninguna de
   las tres palancas que Ari nombró toca eso.
3. **La palanca que sí importaría no está en la configuración.** Para que hubiera
   calma haría falta poder empezar equipado, poder curarse hasta el tope, o que
   las filas de la pérdida se apaguen. Lo primero y lo segundo son del mapa, que
   no tiene campo; lo tercero es de la tabla, que es nuestra.
4. **El mundo lento es barato.** 0,13 $ las tres partidas. El precio no es el
   obstáculo para repetir esto con el preset de Ari cuando llegue.
5. **El preset de Ari sigue sin llegar.** Todo esto es `lento_v0` provisional y
   se repetirá con el suyo sin tocar más que el JSON.

**PARO AQUÍ.**

## Custodia

```
$ md5 -q motor/model.py
1e511978c251130e95169ebf8443efa1
```

Ficheros: `cantera/paper5/ACTA.md`, `analiza_C.py`, `tablas_C.py`,
`C_medidas.json`, `{B1,C2,C3}_peticion.json`, `{B1,C2,C3}_final.json`,
`{B1,C2,C3}_vigilancia.log`, y los seis diarios en `paintball/runs/P5_{B1,C2,C3}/`.

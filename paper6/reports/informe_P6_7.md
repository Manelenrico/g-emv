# P6-7 · Por qué la pareja con ojos compartidos vive menos

*27-sep-2026. Solo lectura de los 80 diarios de P6-6 (A0 y A1, las mismas 20
semillas). Ninguna partida. `motor/model.py` intacto
(`1e511978c251130e95169ebf8443efa1`), 202 archivos de `CONGELADO.md` sin alterar,
nada subido ni borrado. No propongo arreglos: esto es entender.*

**Lo que el diario no dice, y aquí no se estima:** los rivales CONTADOS no van
en `ve_agentes` (el diario guarda la observación cruda); se reconstruyen del
último E2 del hermano en el chat con la misma regla de `oyente2.inyecta`
(edad ≤ 50 tics, sin los asientos que yo ya veo). La posición REAL de un rival
contado no está en ningún diario nuestro. El detalle de candidatos
(`pos_prevista`, `d`, filas) solo se guarda cada 24 tics; la dirección elegida
se lee de `intencion.dir`, que está en todos.

---

## RESPUESTA CORTA

**La pista era mala y el mecanismo es otro.** `F-HERMANO-AMENAZA` se enciende
más en A1, sí — y el 46 % de sus activaciones vienen de rivales contados —, pero
**no explica ni una muerte**: en ninguna de las 33 muertes de A1 la fila llega a
M ≥ 0,1 en sus últimos 200 tics. Lo que el diario enseña es esto, en cadena:

1. **Con los ojos, la pareja se separa.** A ≤ 3 casillas el 79,1 % del tiempo en
   A0 y el 59,9 % en A1; a más de 15 casillas, **0,00 %** en A0 y **7,59 %** en A1.
   Las excursiones largas (≥ 200 tics) pasan de 3 a **19**, y suman 40.031 tics.
2. **Y no vuelve.** En esas excursiones el que se aleja elige `ir_pareja` **18
   tics de 34.606**. Con las piernas listas y el hermano fuera de la vista,
   `ir_pareja` está disponible 54.244 tics y gana **405** (0,75 %; en A0, 729 de
   11.939 = 6,1 %). Por qué pierde está en el detalle de candidatos: volver al
   hermano cuesta **S-8-EXPOSICION** (+0,17 de M en 771 de 811 tics; en A0 la
   fila ni difiere) — porque **el E2 lleva los rivales que el hermano ve, que por
   construcción están cerca del hermano**, y la tabla del cinco los cuenta como
   exposición del camino de vuelta (`appraisal_zs_v42_exp.py:1391-1416` recorre
   `vis.agents`, contados incluidos). Encima, el destino de `ir_pareja` es la
   **última posición VISTA** (`mem.pareja_pos`, `appraisal:624`), no la exacta
   del parte: en A1 está a más de 3 casillas de donde está el hermano el 41,6 %
   de los tics sin verlo (p90 13 casillas, máximo 31).
3. **Separado, se clava.** El bucle de la mochila llena (`coger` con
   `inventory_full`, que el cuerpo del cinco no lee): **18.566 tics en A1 (4,44 %)
   contra 6.254 en A0 (1,31 %)**, y con las piernas listas **15.414 contra 1.390**.
   La racha peor: **3.676 tics**, el 29,3 % de una vida. De las 18 rachas largas de
   A1, 8 son sobre un `first_aid` y **8 sobre un objeto que le habían contado**
   (0 de 12 en A0).
4. **Y muere lejos.** Las 7 muertes por rival de A1 son **tempranas** (mediana
   tic 2.701; A0: 10.859) y **lejos del hermano** (mediana 9,5 casillas; A0: 1;
   a ≤ 3 casillas: 0 de 4 contra 7 de 7). Las 23 del anillo, con el hermano vivo
   a **10 casillas** de mediana (A0: 2,5).

El total de muertes no cambia (32 en A0, 33 en A1). Cambia **cuándo** y **cómo
de lejos**.

---

## 1 · LA PISTA: F-HERMANO-AMENAZA

### 1a · De quién viene

Por tic con la fila en la tabla, recalculando el criterio de la fila (hostil
con arma de daño > 0 y el hermano a su alcance, o agresor certificado) sobre
los hostiles VISTOS por mí y los CONTADOS por el hermano:

| | A0 | A1 |
|---|---:|---:|
| tics con la fila encendida | 29.085 | **82.704** |
| …solo por un rival VISTO | 29.085 (100 %) | 43.827 (53,0 %) |
| …**solo por un rival CONTADO** | — | **38.256 (46,3 %)** |
| …por los dos | — | 621 (0,8 %) |
| no reconstruible | 0 | 0 |

**Casi la mitad de las activaciones de A1 son de rivales que el cuerpo no ve.**
Y las por rival visto también suben (43.827 contra 29.085): en A1 el hermano
está más lejos y rodeado de más cosas.

### 1b · Qué elige cuando se enciende

| | A0 | A1 |
|---|---:|---:|
| tics encendida | 29.085 | 82.704 |
| se queda quieto (`do: none`) | 25.595 (88,0 %) | 62.510 (75,6 %) |
| elige `coger` | 374 | **8.107** |
| pasos (`intencion: move`) | 3.003 | 11.986 |
| …paso que ACERCA al hermano | 1.239 (41 %) | **10.158 (85 %)** |
| …paso que ALEJA del hermano | 975 (32 %) | 1.107 (9 %) |
| …paso que ACERCA al hostil | 807 | 1.030 |
| …paso que ALEJA del hostil | 1.316 | 2.325 |
| (solo contado) acerca / aleja / neutro al hostil | — | 470 / 508 / 374 |

Cuando la fila está encendida y da un paso, **en A1 va hacia el hermano el
85 % de las veces** (41 % en A0): la fila hace lo que dice. Lo que no hace es
mover al cuerpo: **el 75,6 % de los tics encendida el cuerpo se queda quieto**, y
**8.107 tics elige `coger`** — es el bucle de la mochila llena con la fila de
fondo (ver 3b).

### 1c · Las vidas de A1 que mueren antes que su asiento en A0

**25 de 40** (`P6_7.json`). En sus últimos 200 tics: 630 pasos, de los cuales
128 hacia un rival contado, 268 hacia un rival visto armado, 234 hacia el
hermano; la fila encendida 961 tics de 5.000. Leídas una a una (tabla completa
en `P6_7.json`), son de tres clases:

| clase | vidas | ejemplo |
|---|---:|---|
| **rival, temprano, lejos del hermano** | 6 (tics 1.843-2.706) | `21622393` s11 t1843: 76 pasos, 63 hacia un contado, 66 hacia un visto armado, 69 hacia el hermano — **todo es la misma dirección**: el hermano estaba rodeado |
| **anillo, con el hermano vivo y lejos** | 13 (tics 9.337-13.057) | `20784561` s11 t9337: **0 pasos**, 200/200 tics en `coger` con mochila llena en la esquina [1,45], 8 golpes del anillo |
| anillo o no consta, hermano ya muerto | 6 | `20260916` s11 t10162 |

**¿Iba hacia un peligro que le habían contado?** En las 6 muertes por rival, en
3 hubo pasos hacia un contado (63, 19, 5) — pero en las tres el contado, el
visto y el hermano estaban en la misma dirección. El diario no permite separar
«fue a por el contado» de «fue a por el hermano». Lo que sí separa: **en las 13
del anillo no hay peligro contado al que ir; hay un cuerpo quieto o clavado**.

---

## 2 · EL RIVAL CONTADO YA MOVIDO

Certificado solo por dos vías (`P6_7.json`, brazo A1):

| | n |
|---|---:|
| tics × rival contado vigente | 347.179 |
| **ya movido, certificado** | **103.862 (29,9 %)** |
| …el hermano lo ve en OTRA casilla en ese tic | 78.286 |
| …la casilla dicha está a mi vista y vacía | 25.576 |
| pasos que se APARTAN de la casilla vacía | 2.414 |
| pasos que van HACIA la casilla vacía | 2.196 |
| …de esos 4.610 pasos, con golpe de rival en los 48 tics siguientes | **181** (53 tras apartarse, 128 tras acercarse) |

**Tres de cada diez rivales contados ya no están donde se dijo** (P6-4 medía
22,4 % por la vía del hermano; aquí, con las dos vías, 29,9 %). Cuánto tiempo
pierde **no lo puedo decir con el diario**: los 4.610 pasos son pasos que
cambiaron la distancia a una casilla vacía, no pasos *causados* por ella — el
cuerpo no elige «ir a por un contado» (esos candidatos se vetan), elige
apartarse o ir a otra cosa. Como cota bruta: 4.610 pasos × 11 tics = 50.710
tics, el 12 % de A1; como daño certificable: **181 golpes** siguieron a esos
pasos, de 201 golpes de rival en todo A1. Es una correlación, no una causa: el
cuerpo recibe golpes donde hay rivales, y donde hay rivales hay contados.

---

## 3 · DE QUÉ MUEREN

### 3a · Reparto (`P6_7.json`, regla de `E3_golpes.py`)

| | A0 | A1 |
|---|---:|---:|
| mueren / sobreviven | 32 / 8 | 33 / 7 |
| **anillo** | 20 · tic mediana 12.889 (mín. 11.257) | 23 · tic mediana 12.889 (**mín. 9.337**) |
| …con el hermano vivo | 10 de 20 · a **2,5** casillas (mediana) · a ≤ 3: 7/10 | 14 de 23 · a **10** casillas · a ≤ 3: **3/14** |
| **rival** | 11 · tic mediana **10.859** (mín. 3.457) | 7 · tic mediana **2.701** (mín. 1.843) |
| …con el hermano vivo | 7 de 11 · a **1** casilla · a ≤ 3: 7/7 | 4 de 7 · a **9,5** casillas · a ≤ 3: **0/4** |
| no consta | 1 | 3 |
| muere primero de la pareja / segundo | 18 / 14 | 19 / 14 |

**Sí cambia algo más que el total.** En A0 se muere **junto al hermano** (a 1-2,5
casillas) y tarde; en A1 se muere **lejos** (a 9,5-10) y, cuando es un rival,
**temprano**: seis muertes por rival antes del tic 2.710, ninguna en A0 antes
del 3.457.

### 3b · Con lupa: cada golpe recibido (`P6_7_golpes.json`)

| golpes recibidos de | A0 | A1 |
|---|---:|---:|
| el anillo | 380 | **553** |
| rival visto con arma en mano | 155 | 135 |
| **rival visto con `hand: none`** | **103** | **66** |
| rival no visto | 0 | 0 |
| veneno | 0 | 5 |

Dos cosas que no esperaba. (i) **Cero golpes de rivales no vistos en 80 vidas**
— igual que en P6-4: el peligro «a ciegas» no existe en este mundo. (ii) **169
golpes vienen de rivales visibles con la mano vacía** (`hand: none`), y matan a
3 (2 en A0, 1 en A1). Para la tabla del cinco «sin arma no hay amenaza»
(`appraisal:1591`): un rival con `hand: none` no enciende ninguna fila de miedo.
El diario no dice con qué pegan (el catálogo no tiene arma de daño 4,5); dice
que pegan.

### 3c · El bucle de la mochila llena (`P6_7_lleno.json`, `P6_7_lleno2_*.json`)

| | P6-4 A0 | P6-4 A1 | **P6-6 A0** | **P6-6 A1** |
|---|---:|---:|---:|---:|
| tics `coger` + `inventory_full` | 9.438 (1,99 %) | 10.855 (2,21 %) | 6.254 (1,31 %) | **18.566 (4,44 %)** |
| …con piernas listas (podía irse) | 982 | 3.316 | 1.390 | **15.414** |
| …con el anillo haciendo daño | 20 | 7 | 2 | **124** |
| rachas ≥ 24 tics | 10 | 16 | 12 | 18 |
| racha más larga | 305 | 846 | 366 | **3.676 (29,3 % de la vida)** |
| rachas largas sobre un objeto CONTADO antes | — | — | 0 de 12 | **8 de 18** |
| mochila al empezar la racha | — | — | 2 objetos (9), 4 (3) | **2 objetos (18)** |

El cuerpo llega a un objeto (en A1, la mitad de las veces uno que le habían
contado), el mundo responde `inventory_full`, y el cuerpo **no lee ese
resultado** (`Bloqueos` solo trata `cooldown`): sigue eligiendo `coger` mientras
el objeto siga en el suelo, con 14 candidatos de movimiento disponibles. Las
dos rachas de 3.200 tics de A1 (`20889290` s10, `21727122` s11) son sobre un
`first_aid` contado. **En P6-4 A1 esto no pasaba** (846 la peor) porque el
cuerpo estaba sordo y S-PROVISION apagada: no quería vendas para dar. Con el
oído arreglado quiere la venda, la mochila está llena, y se queda.

*(El diario dice `inventory_full` con 2 objetos en la mochila, con o sin
`backpack` puesto — 10 de las 18 rachas lo llevaban. Por qué el mundo la da por
llena no lo dice el diario; lo dejo así.)*

### 3d · La distancia entre los dos (`P6_7_pareja.json`, `P6_7_separa.json`)

| | A0 | A1 |
|---|---:|---:|
| tics con los dos vivos | 229.184 | 179.449 |
| a ≤ 3 casillas | **79,13 %** | **59,85 %** |
| a ≤ 8 casillas | 96,86 % | 77,69 % |
| **a > 15 casillas** | **0,00 %** | **7,59 %** |
| emparejado por semilla, % a ≤ 3 | | A1 menor en **15 de 20**, −16,1 p.p. de mediana |
| excursiones (> 8 casillas) | 481 · mediana 11 tics | 225 · mediana 11 tics |
| …**de ≥ 200 tics** | **3** (2.455 tics) | **19** (34.606 tics) · máx. **7.490** |
| el que se aleja: decisiones de movimiento | `move` 24 % · **`ir_pareja` 24 %** · `ir_botin` 18 % · `ir_objeto` 15 % | **`move` 51 %** · `ir_objeto` 17 % · **`ir_pareja` 9 %** |
| …con rival / recurso contado en la percepción | 0 % / 0 % | **78,8 % / 89,9 %** |
| en las largas, `ir_pareja` elegido | 16 de 2.455 tics | **18 de 34.606** |
| en las largas, `move_*` sin rival armado a la vista y CON contado | 0 de 84 | **368 de 872** |

A0 se separa **más veces** y **vuelve enseguida** (mediana 11 tics: un paso).
A1 se separa menos veces y **se queda**: 19 excursiones largas, cuatro de más de
4.900 tics. El que se aleja huye (`move_*`, el candidato de apartarse) el doble,
y **368 de esas huidas son sin ningún rival armado a la vista, con uno
contado** — huye de lo que le han contado.

### 3e · Por qué no vuelve: `noop` contra `ir_pareja` (`mide_vuelta_P6_7.py`)

En los tics con detalle dentro de las excursiones largas, para el que se alejó:

| | A0 | A1 |
|---|---:|---:|
| tics con detalle e `ir_pareja` candidato | 39 | 811 |
| `noop` mejor que `ir_pareja` | 35 | **770** · mediana d(ir_pareja) − d(noop) = **+0,184** |
| **S-8-EXPOSICION**, M(ir_pareja) − M(noop) | −0,094, difiere en 6 de 39 | **+0,171, difiere en 771 de 811** |
| F-4-ALCANCE | −0,043 | +0,079 (805 de 811) |
| F-REENCUENTRO | — | +0,151 (40 de 811) |

**Volver al hermano se prevé como exponerse.** Y es coherente con el censo de
P6-6: S-8-EXPOSICION baja del 70,6 % al 48,5 % de los tics en A1 — el cuerpo
*consigue* estar menos expuesto… quedándose lejos de su hermano, que es donde
están los rivales que el hermano cuenta.

Además, `ir_pareja` apunta a la **última posición vista**, no a la del parte:

| hermano vivo y fuera de la vista | A0 | A1 |
|---|---:|---:|
| tics | 67.525 (14,1 %) | **130.204 (31,1 %)** |
| \|posición recordada − posición del parte\| > 3 casillas | 12,9 % | **41,6 %** (p90 13, máx. 31) |
| con piernas listas: `ir_pareja` disponible / **elegido** | 11.939 / **729** (6,1 %) | 54.244 / **405** (0,75 %) |

---

## 4 · EL GIF

**No hay ninguna muerte de A1 que la pista del punto 1 explique.** Lo digo con
el número: de las 33, **cero** tienen F-HERMANO-AMENAZA con M ≥ 0,1 en sus
últimos 200 tics (`P6_7_golpes.json`).

`cantera/paper6/P6_7_muerte.gif` (59 fotogramas, semilla 22146038, asiento 10,
tics 2.470-2.708) es la que más se le parecía — la fila presente en 200/200 tics
finales — y por eso la elegí antes de medir su magnitud: **M = 0,02**. Lo que se
ve es otra cosa: el cuerpo quieto a 8-9 casillas de su hermano, con dos rivales
contados junto al hermano (sword y knives) y **P14 (zs-patient) adyacente,
visible, con `hand: none`, pegándole 22 veces de 4,5 durante 500 tics** mientras
elige `noop`. En el detalle: F-DANO sube de 0,56 a 0,92, S-7-AGRESOR 0,3-0,5,
F-HERMANO-AMENAZA 0,02. El GIF queda como lo que es: **una muerte que la tabla
del cinco no sabe ver**, no una que los ojos expliquen.

---

## LO QUE ME LLEVO

1. **La pista era la fila equivocada.** F-HERMANO-AMENAZA se enciende más y
   casi la mitad por contados, pero no pesa en ninguna muerte.
2. **El mecanismo es geométrico:** el E2 lleva los rivales que el hermano ve,
   que están junto al hermano; la tabla los lee como exposición del camino de
   vuelta; el cuerpo se queda lejos (S-8 −22 p.p. en A1) y `ir_pareja` pierde
   el 99 % de las veces.
3. **Lejos, se clava** en un objeto que no cabe (4,44 % de A1, 8 de 18 rachas
   sobre un objeto contado) o se queda quieto; **y muere lejos**, temprano si
   es un rival, en la esquina si es el anillo.
4. **Dos cegueras del cinco que los ojos no crearon pero sí agravan:** no leer
   `inventory_full`, y no tener miedo de un rival con la mano vacía (169
   golpes, 3 muertes).
5. **Cero golpes a ciegas en 80 vidas, otra vez.** El peligro contra el que se
   construyeron los ojos no es el que mata aquí.

*No propongo arreglos: primero entender, como pediste.*

## LOS ARCHIVOS NUEVOS, CON SU MD5

| archivo | md5 |
|---|---|
| `cantera/paper6/mide_P6_7.py` | `b4daf05daafba32575fe44ed0125ac8c` |
| `cantera/paper6/mide_lleno_P6_7.py` | `ad5be39debd2e13cc17d3a09e0947508` |
| `cantera/paper6/mide_pareja_P6_7.py` | `079d3bf666de64414419874be9632f2e` |
| `cantera/paper6/mide_separa_P6_7.py` | `bad392f3e760001aa7b182ad87f7cefc` |
| `cantera/paper6/mide_largas_P6_7.py` | `a7cb3ae068cba6d7dbe8af578e381882` |
| `cantera/paper6/mide_vuelta_P6_7.py` | `67a3d3214117377a6f0c723a44830ac1` |
| `cantera/paper6/mide_lleno2_P6_7.py` | `587060ade398af37edc5fa1611962b6b` |
| `cantera/paper6/mide_golpes_P6_7.py` | `873b35b9bf318ab29d7b9cd92e5e0476` |
| `cantera/paper6/gif_P6_7.py` | `b36ce68f3e3d83c91a6aa1db234b236d` |
| `cantera/paper6/P6_7.json` | `13685e96dfdac074d54ff91a432821d0` |
| `cantera/paper6/P6_7_lleno.json` | `9346b94e955ad1738c5dae45021b227d` |
| `cantera/paper6/P6_7_pareja.json` | `b86d7887b79f1eee025b1bfb0e11b6aa` |
| `cantera/paper6/P6_7_separa.json` | `7f185cf2a5f133f4f1cab4d86d36af8b` |
| `cantera/paper6/P6_7_largas_A1.json` | `0376251d0d2555f4b5e8631ef486a4e4` |
| `cantera/paper6/P6_7_largas_A0.json` | `e7141041a2c14004855e69ec075dc9b7` |
| `cantera/paper6/P6_7_lleno2_A0.json` | `b65272b97e2a69e51767f5258d2df49e` |
| `cantera/paper6/P6_7_lleno2_A1.json` | `fd2386464156505d94eefe66e29512ba` |
| `cantera/paper6/P6_7_golpes.json` | `68f02d70fea270a6caf5d3782f931195` |
| `cantera/paper6/P6_7_muerte.gif` | `454f1d14f05d68b3777f95f53d4d21df` |

*Ningún md5 de esta tabla se escribió antes de calcularlo.*

## CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — intacto |
| archivos de `CONGELADO.md` | 202 comprobados, 0 alterados |
| partidas jugadas | ninguna · coste 0,0000 USD |
| patrones de clave en lo nuevo | ninguno |
| subido, empujado o borrado | nada |

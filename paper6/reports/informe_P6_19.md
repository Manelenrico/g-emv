# P6-19 · Cómo suelen pegar los otros: tasas base en la imaginación del cuerpo

*27-sep-2026. Coste cero: banco sobre los 200 diarios ya jugados del mundo del seis
(A3, A4, A5v, A5h, A6; 100 partidas). Nada jugado. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados
del cinco y los 32 del seis: 0 alterados al principio y al final. Lo nuevo, en
archivos aparte y declarado: `mide_tasas_P6_19.py` → `P6_19_tasas.json`;
`puerta6g_P6_19.py` (versión nueva de puerta6, con golpes esperados);
`banco_P6_19.py` + `corre_P6_19.py` + `resume_P6_19.py` → `P6_19_banco.json`;
`P6_19_dano_fuentes.json`. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

Los rivales pegan **poco y de cerca**: en los 200 diarios, un rival a tiro
pega en el tic **1 de cada 100** veces con la mano vacía, 1 de 150 con lanza,
1 de 50 con espada, y casi nunca con arco o cerbatana (2-3 de 10.000); casi
todo el daño de rival llega a distancia 1-2. En las fases finales **el anillo
hace el 77 % del daño** (0,042 por tic contra 0,012 de los rivales), y en las
ventanas donde el cuerpo se decide (2.435 decisiones), el fuego quita 25 puntos
en 200 tics y los rivales 1. Con esas tasas, la expectativa de golpes que
puerta6g añade a la imaginación es **≈ 0,005 puntos por tic** (los rivales
vistos suelen estar a ≥ 3): no cambia los veredictos (48 de 63 momentos siguen
prefiriendo quedarse; los planes de A6 pasan de 123 a 118 aceptados), baja
«lo que promete de más» de 21,6 a 20,4 puntos, y de las 70 formas de A6 que
cayeron por «vida real bajo la proyectada», **3 dejarían de caer**. Lo que
promete de más la imaginación no son golpes de rivales quietos: es **el fuego
que el cuerpo real se come cuando no sigue el plan** (el hueco real − proyectado
es −17,6 de media) y los golpes de cerca de rivales que se acercan.

---

## 1 · TASAS BASE (200 diarios, 2,52 millones de tics vivos)

Definiciones (`mide_tasas_P6_19.py`): rival **visto** (`ve_agentes`, mano del
catálogo) o **contado** (último parte E2 del hermano a ≤ 50 tics, con su casilla
y arma, sin los ya vistos: la regla de `oyente2.inyecta`); «a tiro» = distancia
Chebyshev ≤ alcance del arma (mano vacía: 1); golpe = `damage_taken` con `source`
P<slot>. 1.291 golpes de rival, 9.041 puntos; **1 golpe de un rival ni visto ni
contado en ese tic** (10,8 puntos): lo que nos pega, se ve.

### 1a · Por arma del rival: pega o está

| arma del rival | rival-tics a tiro | golpes | **P(pega en el tic \| a tiro)** (Wilson 95 %) | daño / rival-tic | daño / golpe | rival-tics a tiro **sin pegar** |
|---|---|---|---|---|---|---|
| mano vacía | 67.704 | 683 | **0,0101** [0,0094, 0,0109] | 0,038 | 3,8 | 99,0 % |
| espada | 9.373 | 193 | **0,0206** [0,0179, 0,0237] | 0,272 | 13,2 | 97,9 % |
| lanza | 42.375 | 290 | 0,0068 [0,0061, 0,0077] | 0,067 | 9,8 | 99,3 % |
| cuchillos | 253.143 | 61 | 0,0002 [0,0002, 0,0003] | 0,002 | 8,0 | 99,98 % |
| arco | 161.639 | 26 | 0,0002 [0,0001, 0,0002] | 0,002 | 14,0 | 99,98 % |
| cerbatana | 97.944 | 31 | 0,0003 [0,0002, 0,0005] | 0,001 | 4,0 | 99,97 % |
| red | 195 | 0 | 0 [0, 0,019] | 0 | — | 100 % |
| **visto**, a tiro | 551.692 | 1.283 | 0,0023 | 0,016 | 7,0 | 99,8 % |
| **contado**, a tiro | 80.681 | **1** | 0,00001 | 0,00004 | 3,0 | 99,999 % |
| fuera de tiro (todas) | 6,1 M | 6 | ~0 | ~0 | | |

Lo que se ve: un rival «a tiro» es sobre todo un rival que **no pega en ese
tic**; los enfriamientos del catálogo (espada 18, lanza 20, arco 18, cerbatana
24 tics) ponen el techo en 0,04-0,06 por tic y las armas de cuerpo a cuerpo se
quedan en un tercio o un cuarto de ese techo; **las armas a distancia casi no
pegan** (arco: 26 golpes en 161.639 rival-tics a alcance 8). Los **contados**
no pegan: cuando pegan, ya se ven.

### 1b · Por arma y distancia (daño por rival-tic; la tabla de puerta6g)

| arma \ distancia | 1 | 2 | 3-4 | 5-6 | 7-8 | > 8 |
|---|---|---|---|---|---|---|
| mano vacía | **0,038** (n 67.652) | 0,0002 | 0 | 0 | 0 | 0 |
| espada | **0,272** (9.369) | 0 | 0 | 0 | 0 | 0 |
| lanza | **0,119** (14.882) | **0,039** (27.482) | 0 | 0 | 0 | 0 |
| cuchillos | 0,138 (2.788) | 0,004 | 0,0009 | 0 | 0 | 0 |
| arco | 0,029 (6.752) | 0,006 | 0,0017 | 0,0002 | 0,0013 | 0 |
| cerbatana | 0,028 (3.958) | 0,0004 | 0,0001 | 0,0001 | 0 | 0 |

A distancia ≥ 3 el daño esperado por rival-tic es < 0,002 con cualquier arma.

### 1c-e · Por tic del cuerpo

| contexto | tics | daño de rival / tic (IC 95 % por vidas) | golpes |
|---|---|---|---|
| rivales vistos+contados: 0 | 200.188 | 0 | 0 |
| 1 | 479.500 | 0,0023 [0,0015, 0,0034] | 147 |
| 2 | 625.305 | 0,0018 [0,0013, 0,0023] | 178 |
| 3 | 518.861 | 0,0024 [0,0017, 0,0033] | 165 |
| **≥ 4** | 699.369 | **0,0080** [0,0066, 0,0096] | 801 |
| fases 1-4 | 2.222.797 | 0,0024 [0,0020, 0,0028] | 652 |
| **fases 5-7, dentro del círculo** | 137.400 | **0,0228** [0,0179, 0,0283] | 549 |
| fases 5-7, fuera | 163.026 | 0,0037 [0,0024, 0,0054] | 90 |
| junto (hermano a ≤ 3) | 1.903.988 | **0,0021** [0,0018, 0,0025] | 601 |
| solo, hermano vivo | 523.514 | 0,0064 [0,0049, 0,0081] | 389 |
| solo, hermano muerto | 95.721 | **0,0177** [0,0120, 0,0244] | 301 |

Y el otro que pega, **el anillo** (`P6_19_dano_fuentes.json`): fases 1-4, rival
0,0024 por tic y anillo 0,0008 (rival 76 % del daño); **fases 5-7, anillo 0,042
por tic y rival 0,012 (rival 23 %)**. Dentro del círculo en las fases finales el
rival pega diez veces más que en la partida abierta, y aun así el fuego pega
tres veces más que el rival.

---

## 2 · IMAGINACIÓN CON GOLPES: PUERTA6g

`puerta6g_P6_19.py`, versión declarada de puerta6: en cada tic proyectado la
vida pierde la **suma, sobre los rivales de la foto (vistos o contados,
quietos), del daño por rival-tic de la tabla 1b** según arma y distancia a la
casilla proyectada; en el comparador (`rollout_g`) y en la curva del plan
(`curva_H_g`), para que las dos cosas se imaginen igual. Variante declarada
**ctx**: la tasa del contexto (fases 5-7 dentro 0,0228 / fuera 0,0037 / fases
1-4 0,0024; 0 sin rivales a la vista). Lo que no modela: rivales que se mueven
(como puerta6), y nuestros golpes (§4).

**Fidelidad** (mismas ventanas que P6-15: las decisiones del oráculo en las 40
vidas de A4, 2.435; vida prevista − real):

| | +50 | +100 | +200 |
|---|---|---|---|
| daño real en la ventana: anillo · rival (media) · ventanas con golpe de rival | 6,9 · 0,3 · 56 | 13,5 · 0,6 · 88 | 24,7 · 1,1 · 149 |
| **puerta6**: error mediana · \|error\| media · promete de más (> 10) / de menos (< −10) | −1,0 · 6,0 · 171 / 179 | −0,3 · 11,3 · 459 / 322 | 0,0 · 16,3 · 690 / 659 |
| **puerta6g**: ídem | −1,4 · 6,2 · 161 / 208 | −1,7 · 11,5 · 445 / 347 | 0,0 · 16,3 · 657 / 704 |
| puerta6g_ctx: ídem | −1,1 · 6,2 · 171 / 182 | −2,1 · 11,5 · 454 / 336 | 0,0 · 16,6 · 648 / 712 |
| solo con golpe real de rival: error medio puerta6 → g → ctx | 10,0 → 7,4 → 9,5 (n 56) | 10,1 → 6,1 → 9,2 (n 88) | 8,7 → **1,0** → 6,5 (n 149) |
| daño esperado «ahora» (media · mediana) | 0,005 · 0,000 | | |

**¿Deja de prometer de más?** En conjunto puerta6 no promete de más: su error
mediano es 0 y los que se pasan (690 a +200) igualan a los que se quedan
cortos (659), porque el rollout ya lleva el fuego, que es el 96 % del daño de
esas ventanas. puerta6g mueve la previsión −0,4 puntos de media (−1,3 a +200):
el daño esperado desde los rivales vistos es 0,005 por tic porque están a ≥ 3.
**Donde hubo golpes de rival de verdad, sí acierta más**: a +200 el error medio
baja de 8,7 a 1,0 (n 149), y la variante ctx a 6,5.

---

## 3 · QUÉ CAMBIA EN LA PUERTA

### 3a · Los 63 momentos de salida de A5h (y los 22 de A4), plan de quedarse

| | puerta6 | **puerta6g** | puerta6g_ctx |
|---|---|---|---|
| A5h, prefiere quedarse (ok) / area / vida | **48** / 13 / 2 | **48** / 12 / 3 | 49 / 11 / 3 |
| cambian (6 ok → g no · 6 no → g ok) | | 2 · 2 | 0 · 1 |
| ventaja mediana | 0,225 | 0,238 | 0,231 |
| lo que promete de más el plan (vida prevista − real en los puntos de control, n 175) media · mediana | 21,6 · 14,0 | 20,4 · 13,0 | 18,7 · 11,9 |
| A4, prefiere quedarse | 14 / 22 | 13 | 14 |
| A4, promete de más (n 64) | 30,5 · 26 | 28,2 · 20 | 27,2 · 23,7 |

### 3b · Los planes que el oráculo propuso en A6 (309 juzgados; 70 caídas por «vida real bajo la proyectada»)

| | puerta6 | **puerta6g** | puerta6g_ctx |
|---|---|---|---|
| veredictos ok / area / vida | 123 / 159 / 27 | **118** / 152 / **39** | 119 / 157 / 33 |
| pasaban y ya no pasan · no pasaban y ahora sí | | **5 · 0** | 4 · 0 |
| promete de más (n 821): media · mediana | 20,1 · 13 | 18,1 · 10 | 17,7 · 10,6 |
| caídas «vida real < proyectada − 10»: seguirían cayendo · **dejarían de caer** | 70 · — | 67 · **3** | 69 · 1 |
| hueco real − proyectada en las caídas (media · mediana) | −17,6 · −14 | | |
| lo que baja la proyección g (ctx) en el punto de la caída | | −0,6 (mediana 0) | −1,0 (mediana −0,6) |

**Lo que cambia: casi nada.** puerta6g ve el peligro en 5 planes de 309 (los
rechaza por «vida») y no salva de la caída más que 3 de 70, porque en esas
caídas la proyección baja 0,6 puntos y el hueco es de 17,6: **lo que faltaba no
era la expectativa de golpes de los rivales quietos**, era el fuego que el
cuerpo real se come al no seguir el plan y los golpes de cerca de rivales que
llegan después.

---

## 4 · DEFENSA CONJUNTA, PRIMER VISTAZO: LO QUE NO SE PUEDE JUZGAR TODAVÍA

Para los 325 golpes con el hermano a ≤ 3 (P6-17), el plan «pega a ese agresor»
**no se puede pasar por puerta6g**, y se dice por qué, con lo medido:

1. **No cabe en el idioma de formas**: las intenciones son `ir`, `coger`,
   `usar`, `esperar` (`traductor_forma.INTENCIONES`); no hay `atacar`, así que
   el traductor real no produce ese plan.
2. **La proyección no modela nuestros golpes** ni la vida del rival:
   `proyeccion._proyecta` mueve, coge, usa y cobra el anillo; el rollout de
   puerta6/puerta6g declara «sin ataques» (P6-15) y `accion_a_plan` traduce
   `attack` a esperar. Un plan de pegar se imaginaría como quedarse quieto al
   lado del agresor, comiéndose sus golpes esperados (0,27 por tic con espada a
   1) sin devolver ninguno: la puerta lo rechazaría por «vida» o por área
   siempre.
3. **No se sabe cómo reacciona el agresor**: en P6-17, cuando le pegan los dos
   muere en 200 tics en el 40 % y deja de pegar en 24 tics en el 53 %; cuando
   ninguno, 1 % y 63 %. Eso es una tasa base más, pero de *reacción*, y aquí
   no hay nada que la use.

Lo que haría falta, medido y no construido: (a) una intención `atacar` en el
idioma y en el traductor; (b) en la proyección, nuestro daño por tic contra un
rival adyacente o a alcance (del catálogo: espada 18 cada 18 tics, lanza 12/20,
arco 14/18, cuchillos 8/10, cerbatana 4/24; mano vacía 3) y una vida del rival
(el parte E2 trae su banda); (c) la tasa base de reacción del agresor (muere,
se va, deja de pegar) de P6-17 §5, por número de los nuestros que le pegan.

---

## 5 · LO QUE DICE LA MEDIDA (sin proponer nada)

1. Los rivales pegan **poco** (1 de cada 100 tics a tiro con la mano vacía, 1
   de 50 con espada) **y de cerca** (a ≥ 3 casillas, nada); las armas a
   distancia casi no pegan; los rivales contados no pegan.
2. En las fases finales el que pega es **el anillo** (77 % del daño; 0,042 por
   tic contra 0,012), y dentro del círculo el rival pega diez veces más que en
   la partida abierta.
3. Una expectativa de golpes desde los rivales vistos, quietos, vale **0,005
   por tic**: no cambia veredictos (48/63; 118/309), baja lo prometido de más
   en un punto, y salva 3 de 70 caídas.
4. La imaginación del cuerpo no se pasa **de media** (error mediano 0 a +50,
   +100 y +200): lo que promete de más lo promete **el plan de quedarse** cuando
   el cuerpo no se queda, y el daño de cerca cuando el rival llega.
5. «Pega a ese agresor» no se puede juzgar aún: faltan la intención `atacar`,
   nuestro daño en la proyección y la reacción del agresor.

---

## 6 · ARCHIVOS

| archivo | qué es |
|---|---|
| `mide_tasas_P6_19.py` · `P6_19_tasas.json` | las tasas base (a-e) y la tabla arma × distancia |
| `P6_19_dano_fuentes.json` | daño por fuente (anillo / rival) y fase, 200 diarios |
| `puerta6g_P6_19.py` | puerta6g, versión declarada (curva g, rollout g, variante ctx, `instala`/`quita`) |
| `banco_P6_19.py` · `corre_P6_19.py` · `resume_P6_19.py` · `P6_19_banco.json` | fidelidad (2.435 decisiones), momentos (85), A6 (309 planes, 70 caídas) |

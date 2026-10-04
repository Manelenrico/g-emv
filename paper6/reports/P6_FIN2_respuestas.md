# P6-FIN2 · Respuestas a la revisión externa del paper seis

*2-oct-2026. Coste cero. Borrador: `cantera/paper6/paper6_ES_borrador_v4.md` (no se toca). «P6-N:l» = `cantera/paper6/informe_P6_N.md`,
línea l; los guiones y JSON, en `cantera/paper6/`. Los números nuevos de este documento se han calculado solo con los JSON ya guardados.*

## 1 · La medida principal: qué vidas entran y si A7h arde menos porque muere antes

**Definición** (`mide_campo_P6_24.py:1-9`, 142-150): tics ardiendo en las fases 5-7 = número de tics, desde el aviso de la fase 5 (tic
11.856) hasta la muerte o el final de la partida, en que la criatura está a más del radio vigente del centro (arde = distancia > `zona.radius`).
**Entran solo las vidas vivas en el aviso de la fase 5** (`viva_en_warn5`, línea 150). Las que mueren antes del aviso no entran. Las que mueren
durante las fases 5-7 **entran con su ventana recortada en la muerte**: una vida que muere pronto suma pocos tics ardiendo. Media por semilla
(las dos vidas vivas de la pareja), diferencia A7h − A4 emparejada por semilla; solo semillas con alguna vida viva en el aviso 5 en los dos brazos.

Por brazo, con `P6_24_campo_40.json` (40 semillas, 80 vidas por brazo):

| | A4 (cuerpo solo) | A7h (oráculo) |
|---|---|---|
| vidas · vivas en el aviso 5 · mueren antes del aviso 5 | 80 · 74 · 6 | 80 · 77 · 3 |
| **supervivientes al final de la partida** | **16** | **30** |
| mueren en las fases 5-7 (anillo · rival · no consta) | 58 (44 · 10 · 4) | 47 (30 · 14 · 3) |
| instantes vivos en 5-7 por vida: media · mediana · p10 · p90 | 1.619 · 1.172 · 699 · 2.847 | 2.198 · 2.665 · 673 · 3.145 |
| instantes ardiendo en 5-7 por vida: media · mediana | 232,3 · 233,5 | 174,7 · 146 |
| **ardiendo por instante vivo**: agregado · media por vida · mediana por vida | 0,144 · 0,197 · 0,165 | 0,080 · 0,121 · 0,072 |
| supervivientes: ardiendo media · instantes vivos | 166 · 2.400 | 130 · 3.017 |
| muertas en 5-7: ardiendo media · instantes vivos · tic mediano de muerte | 251 · 1.403 · 12.972 | 204 · 1.675 · 13.200 |
| emparejado por semilla (n 37): instantes vivos A7h − A4 | | **+558** de media (mediana +640; A7h vive más en 25 de 37) |
| emparejado por semilla (n 37): ardiendo por instante vivo A7h − A4 | | **−0,059** (mediana −0,066; A7h menor en 26 de 37) |

**Respuesta:** no. A7h arde menos y **vive más**: 30 supervivientes contra 16, 558 instantes vivos más por semilla, y muere más tarde cuando muere.
Si se corrige por el tiempo vivo, la diferencia se mantiene: A7h arde en el 8 % de sus instantes de las fases 5-7 y A4 en el 14 %. La medida
absoluta publicada (−57,6 tics) es, si acaso, conservadora para A7h, porque A7h tiene más instantes en que podría arder. (Los supervivientes
por brazo ya estaban en P6-24:80 por series de 20: A4 11 → 5, A7h 13 → 17; P6-24 declara la diferencia en vidas como secundaria y de poca potencia.)

## 2 · La prueba estadística y los valores −53,3 y −61,6

**Prueba:** permutación por cambio de signo sobre las diferencias emparejadas por semilla (`mide_campo_P6_24.py:76-88`): exacta (las 2ⁿ
asignaciones de signo) hasta 22 pares; con más pares, Monte Carlo de 1.000.000 de cambios de signo con semilla 0 (líneas 73, 85). Unilateral:
proporción de medias permutadas ≤ la observada (H1: A7h arde menos; línea 86-87); bilateral: |media| ≥ |observada|. No es Wilcoxon (no usa
rangos) ni t. IC95 de la media por bootstrap (10.000 remuestreos, semilla 0; líneas 91-94). Confirmado en los JSON:

| serie | n pares | media · mediana | gana / pierde (A7h arde más / menos) | p unilateral · bilateral | IC95 | fuente |
|---|---|---|---|---|---|---|
| P6-23, 20 semillas viejas, con la medida sellada en P6-24 | 18 | **−53,33** · −41,5 | 5 / 13 | **0,0465** · 0,093 | [−109,6, +2,5] | `P6_24_campo_P623.json`; P6-24:20 |
| P6-24, 20 semillas nuevas | 19 | **−61,63** · −77,0 | 8 / 11 | **0,0424** · 0,085 | [−125,7, +3,5] | `P6_24_campo.json`; P6-24:18-20, 57, 114 |
| las 40 juntas | 37 | **−57,59** · −43 | 13 / 24 | **0,0072** · 0,0143 | [−100,9, −15,3] | `P6_24_campo_40.json`; P6-24:99 |

(Con 18 y 19 pares la prueba es exacta; con 37, Monte Carlo. P6-24:20 redondea −53,33 a «−53» y P6-24:114 escribe −61,6.)

## 3 · P6-27: por qué 232,3 / 174,7 / 220,4 no cuadran con −9,9 y +43,1

Las medias por brazo (232,3 / 174,7 / 220,4) son **medias por vida sobre todas las vidas vivas en el aviso 5** de cada brazo (A4 74, A7h 77, A8 66
vidas). Las diferencias son **emparejadas por semilla sobre el subconjunto de semillas con vidas vivas en el aviso 5 en los dos brazos**, y
cada semilla aporta la media de sus vidas (`mide_campo_P6_24.py:96-104`; P6-27:101-102). A8 tiene 76 vidas (dos carpetas con un solo diario)
y solo 36 semillas con vidas vivas en el aviso 5, de ahí n 34 y n 35. Las medias del subconjunto, de `P6_27_campo.json` (`por_semilla`):

| comparación | n semillas | media por semilla, primero · segundo | diferencia media · mediana | fuente |
|---|---|---|---|---|
| A8 − A4 | 34 | 218,7 · 228,6 | **−9,9** · −13,0 | `P6_27_campo.json` principal; P6-27:101 |
| A8 − A7h | 35 | 218,3 · 175,2 | **+43,1** · +61,5 | secundarias; P6-27:102 |
| A7h − A4 | 37 | 173,7 · 231,3 | **−57,6** · −43,0 | P6-24:99 |

Con las medias del subconjunto las restas cuadran (218,7 − 228,6 = −9,9; 218,3 − 175,2 = +43,1).

## 4 · P6-29, «lo que gana a cambio»: cómo se calcula «si hubiera ido a lo suyo»

No es imaginación del cuerpo ni réplica: es **la vida de referencia A4 de la misma semilla**, en la misma ventana de tics
(`mide_P6_29.py:389-396`). Para cada plan de A7h o A8 con ventana [aceptación, fin): se toma la vida de A4 de esa semilla y ese asiento si está
viva durante toda la ventana, si no la del otro asiento; ahorro = tics ardiendo de esa vida de A4 en la ventana − tics ardiendo propios en la
ventana. Sin pareja viva, el plan queda fuera (6 de 36 cumplidos en A7h, 4 de 19 en A8). Es una comparación emparejada por semilla con el
cuerpo sin consejero, que vive otra partida desde el mismo punto de partida (P6-29:§2.3; informe línea 91-93). De ahí la mediana 0: en la mitad
de las ventanas ni A4 ni el cuerpo con plan ardieron (P6-29:100-103).

## 5 · P6-25: aceptados y respuestas válidas por consejero

P6-25:66-69, 200 escenas:

| consejero | respuestas con plan · callan · intraducibles · no parsean | acepta puerta6 (sobre planes) | sobre las 200 escenas |
|---|---|---|---|
| oráculo | 200 · — · — · — | **102 / 200 = 51,0 %** | 51,0 % |
| Haiku 4.5 | 191 · 6 · 3 (1,5 %) · 0 | **98 / 191 = 51,3 %** | 49,0 % |
| Sonnet 4.5 | 183 · 2 · 15 (7,5 %) · 0 | **100 / 183 = 54,6 %** | 50,0 % |

El denominador de 51,3 / 54,6 % es «respuestas con plan»: **se excluyen las que callan y las intraducibles** (no llegan a la puerta). Sobre
las 200 escenas, con las exclusiones contadas como rechazo, es 49,0 / 50,0 %.

## 6 · P6-2: «una cuarta parte de lo que ve cada uno es solo suyo»

P6-2:195-201 y 209-210. Casillas = las que están en línea de vista desde la posición (`Ojo.vistas_desde`, el cálculo del cinco). Casillas
que ve uno y el otro no, como fracción de lo que ve: mediana **21,1 %** (asiento 10) y **25,5 %** (asiento 11), medias 28,0 y 29,0 %; en el
17,9 % de los tics más de la mitad de lo que ve el 10 es solo suyo. La frase «a dos casillas de distancia, la cuarta parte de lo que ve cada
uno es información que el otro no tiene» es P6-2:209-210. Datos: los 20 diarios de P6-1 (10 partidas).

## 7 · «Escapada larga», definición exacta

`mide_separa_P6_7.py:3-6, 22, 68-77` (y copias `mide_separa_P6_10/11.py`): distancia = **Chebyshev** entre las posiciones de los dos hermanos
en cada tic con los dos vivos. Una **excursión** empieza en el primer tic en que la distancia pasa de **más de 8 casillas** viniendo de ≤ 8, y
acaba en el primer tic en que vuelve a ≤ 8 o en que uno de los dos muere (si no vuelve, acaba en el último tic con los dos vivos). Cada cruce
de ida y vuelta es un episodio distinto: dos excursiones separadas por un solo tic a ≤ 8 cuentan como dos. **Larga** = excursión de **≥ 200
tics** de duración (`mide_largas_P6_7.py:1, 20, 53`). «Quién se aleja» = el asiento que más se movió en los primeros 60 tics. Cuentas: A0 3,
A1 19, A2 30, A3 1 (P6-7:215; P6-10:167).

## 8 · P6-13: 22 de 22 con camino frente a 19 con casilla segura al alcance

`mide_anillo_P6_13.py:12-19, 61, 134-142`: casilla segura = distancia euclídea al centro ≤ r1 de la fase y no sólida; camino = BFS de 8
vecinos; instantes = pasos × 11. Se calcula en dos momentos. **22 de 22**: había camino a una casilla segura (en el aviso y en el primer
golpe), P6-13:116. **21 de 22**: «llegaba saliendo en el aviso» = instantes del camino < tics desde el aviso hasta la muerte (línea 141;
P6-13:119-120). **19 de 22**: «llegaba saliendo en el primer golpe» = instantes del camino desde la posición del primer golpe < tics desde
el primer golpe hasta la muerte (línea 142; P6-13:122-123). Lo que separa a las 3 es el **tiempo**, no el camino: desde el primer golpe les
quedaban menos tics que los pasos × 11 que necesitaban (mediana de tics golpe→muerte 263, mínimo 6; P6-13:122). El borrador llama a los
19 «con una casilla segura al alcance»: es «al alcance a tiempo desde el primer golpe».

## 9 · P6-6: el −57,4 % es la fila S-8-EXPOSICION

Sí. `mide_P6_4.py:202-218` (P6-6 importa ese medidor, `mide_P6_6.py:3, 12`): para cada decisión con las piernas listas, discrepancia del cuerpo
entero = |d real en la siguiente decisión − d proyectada para el candidato elegido| (`disc`), y discrepancia de S-8 = |M real de
S-8-EXPOSICION − M proyectada| (`disc_s8`). El 0,0585 → 0,0249 (−57,4 %, P6-6:235, 251) es `disc_s8_suma / n_disc`, **solo la fila S-8**. Para
el cuerpo entero, con los mismos JSON (`P6_6_medidas.json`): 0,0866 → 0,0558 por decisión, **−35,6 %** (no publicado como tal; P6-4:194-196 da
las sumas de P6-4). El texto, si dice «la sorpresa bajó a menos de la mitad», debe referirse a la de la exposición (S-8).

## 10 · Tabla de brazos para el apéndice

Mundo ZERO-SUM 0.1.19, `roster_lento_v2`; cada brazo lleva el cuerpo del cinco y el parte E1 (48 tics); las piezas se acumulan.

| código | piezas que lleva | informe | partidas (semillas) |
|---|---|---|---|
| A0 | cuerpo del cinco + parte E1; ojos apagados | P6-4; repetido con oído y don en P6-6 | 20 + 20 |
| A1 | + ojos compartidos (parte E2, 25 tics) | P6-4; con oído y don en P6-6 | 20 + 20 |
| A2 | + ir al parte si no ve al hermano; no coger con la mochila llena | P6-8 | 20 |
| A3 | + fila de distancia al hermano (D0 = 7 casillas) | P6-10 | 20 |
| A4 | + manos vacías como arma pequeña; **cuerpo congelado** | P6-11; réplica P6-24 | 20 + 20 |
| A5v / A5h | A4 + oráculo + puerta del cinco (A5v: comparador del cinco; A5h: puerta6) + compromiso | P6-16 | 20 / 20 |
| A6 | A5h + plan «ir y quedarse» + compromiso6b (sujeta) | P6-18 | 20 |
| A6p | A6 con el juicio en proceso aparte (arreglo de los pasos perdidos) | P6-22, humo | 2 |
| A7v / A7h | A4 + oráculo «ir y quedarse» + puerta (A7v: del cinco; A7h: puerta6) + compromiso6c (veto V2, cuenta justa) + oráculo y juicio en proceso | P6-23; A7h repetido en P6-24 | 20 / 20 + 20 |
| A8 | A7h con el razonador Haiku 4.5 en el sitio del oráculo, plan al hermano por el canal | P6-26 humo, P6-27 | 2 + 40 |
| A9 | A8 + previsión de la escena a t+94 | P6-28, solo banco | 0 |

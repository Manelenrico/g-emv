# P6-29 · Cuánto se deja doblar el cuerpo: la deformación que cuesta seguir un plan

*29-sep-2026. Coste cero: solo diarios existentes; **consola de Anthropic 0 USD, créditos de la plataforma 0**. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco (199 archivos) y los 32 del seis: 0 alterados al
principio y al final. Lo nuevo, en archivos aparte y declarado: `sello_P6_29.py` → `SELLO_P6_29.md` (md5 `1979af677b89a168d6e1623c5bd34f43`,
cerrado antes de correr la medida; rehecho una vez tras el humo de tres vidas por un arreglo del lector, mismas predicciones) y `P6_29_sello.json`;
`mide_P6_29.py` → `P6_29_medidas.json`, `P6_29_planes.json` (cada plan y cada instante), `P6_29_vidas.json`; `gif_P6_29.py` (copia de
`gif_P6_23.py` con la deformación en el título) → `P6_29_deformacion.gif`. Ningún número se escribió antes de calcularlo. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**El cuerpo se deja doblar sin límite: con un plan vivo y las piernas listas, hace algo distinto de lo que haría solo en el 83,93 % de los
instantes (A7h) y el 82,37 % (A8), casi siempre porque quiere moverse (ir a por algo, 75,9 % de las veces en A7h) y el compromiso lo
sujeta dentro del círculo; cada instante así cuesta 0,153 unidades de malestar de mediana (A7h; A8 0,101), y los
planes que llegan al final son precisamente los que más lo doblan (acumulada mediana 20,0 contra 0,18 en los soltados, A7h):
ningún plan cae por deformación, caen por la reevaluación de la puerta o por la vida. No hay umbral.** Compensa a medias: en los planes
cumplidos el ahorro de tics ardiendo frente a A4 es 0 de mediana y +42 de media (A7h), sin relación con la deformación
(Spearman -0,0659). Y no deja huella: en los 200 tics siguientes el cuerpo elige lo que elegiría solo en el 99,74 % (A4 en las mismas
ventanas: 98,84 %), como predijo la mesa. Sello: **4 aciertos, 4 fallos** (las magnitudes de 1, 2 y la composición de 6 salieron
mayores que lo previsto; el ahorro mediano de 4 no salió positivo).

## 1 · CÓMO SE MIDIÓ (dos fuentes, declaradas)

**El diario ya guarda las dos elecciones.** La radiografía de cada tic lleva la d de todos los candidatos del cuerpo, `elegido` (lo que se
ejecutó: `_FM_ir_x_y` cuando compromiso6c anda el plan, `_FM_quedarse` / `_FM_retenido` cuando sujeta el paso que sale del círculo) y
`elegido_cuerpo` (lo que el decisor había elegido antes de que el compromiso lo cambiara: lo que habría elegido solo, con el mismo decisor).
`tiempo_tic.vivas`, `forma_aceptada`, `forma_caida` y `compromiso6` dan la vida de cada plan.

**La réplica en seco** (molde de `banco_P6_15` / `escenas_P6_25`): el cuerpo A4 (`policy_pareja.AlmaPareja` + arreglos 6/8b/10/11, entorno de
la imagen A4) recibe las observaciones del diario por un cable falso y decide tic a tic, sin oráculo, puerta ni compromiso. Da (a) la
fidelidad: su elección coincide con `elegido_cuerpo` en el **99,94 %** de los 1.069.140 tics de A7h, el 99,94 % en A8 y el 99,86 % en A4
(en los instantes con plan y desacuerdo, 99,12 % y 98,5 %); y (b) **la d del paso del plan**, que el decisor no calcula en el campo: en cada tic con plan vivo se
vuelve a decidir con un candidato más, `_FM_ir` = {tipo ir, destino del plan} (la receta que anda compromiso6c), y se lee su d junto a la de los
candidatos propios en la misma imaginación. La deformación de un instante es d(ejecutado) − d(mejor propio) con las dos d de la réplica:
`_FM_ir` para `obedece`, `noop` para `sujeta`/`retenido`. Como contraste, la misma cuenta solo con el diario (`paso_D` para obedece): por instante
0,162 contra 0,153 (A7h); acumulada por plan 0,60 contra 0,28. **Instante** = tic con plan vivo y `move_ready_in` 0.

Diarios: A7h P623_t2 + P624_t2 (40 partidas, 80 vidas, 253 planes aceptados); A8 P627_t1 + P627_t2 (40, 78 vidas: dos carpetas
tienen un solo diario, como en P6-27; 98 planes); A4 P611_t1/t2 + P624_t1 (40, 80). Fin de cada plan: `soltado: reevaluación` (la puerta
deja de darle ventaja), `soltado: vida` (la vida real cae bajo la proyectada, cuenta justa), `cumplido: andado` (el plan recorre todos sus tramos:
en A7h los 36 acaban exactamente en su último tic previsto, que es el fin de la fase; ningún registro `cumplida por fin de fase` existe en estos
diarios porque el último tramo termina ahí), `muerte / fin de partida con plan vivo` y, solo en A8, `sustituido por el siguiente` (8).

## 2 · RESULTADOS

### 2.1 · Cuántos instantes dobla (1) y cuánto cuesta cada uno (2)

| | A7h (oráculo) | A8 (razonador) |
|---|---|---|
| planes aceptados · tics vivo mediana (p90) | 253 · 47 (295,2) | 98 · 40,0 (111,9) |
| instantes con plan vivo y piernas listas | 11.247 | 1.214 |
| **difieren de lo que haría solo** | **9.440 = 83,93 %** | **1.000 = 82,37 %** |
| de ellos: sujeta (se queda) · obedece (anda el plan) | 8.643 · 797 | 540 · 460 |
| lo que quería hacer solo (ir a por algo · zancada · paso · otro) | 75,9 · 14,0 · 9,9 · 0,2 % | 68,4 · 23,3 · 5,9 · 2,4 % |
| fracción por plan (mediana; planes sin ningún instante distinto) | 75,0 % (34 de 253) | 66,7 % (16 de 98) |
| **deformación por instante** (mediana · p10 · p90) | **0,153** · 0,025 · 0,286 | **0,101** · 0,005 · 0,264 |
| · en sujeta · en obedece (medianas) | 0,154 · 0,065 | 0,138 · 0,089 |
| instantes con deformación negativa (el paso del plan era mejor que lo propio) | 37 (todos obedece) | 8 (todos obedece) |
| **acumulada por plan** (mediana · p90 · máx) | **0,28** · 17,0 · 102,0 | **0,27** · 3,9 · 12,6 |
| acumulada por 100 tics de plan (mediana · p90) | 0,57 · 9,9 | 0,66 · 5,5 |
| tics con plan vivo en que `_FM_ir` ganaría al cuerpo solo, en la réplica | 13.101 de 26.756 (49 %) | 2.804 de 5.182 (54 %) |

**Lo que dicen las medidas.** (1) Con un plan de «ir y quedarse», el cuerpo con las piernas listas quiere moverse casi siempre: en A7h el
75,9 % de las veces hacia algo (botín, objeto, hermano, centro) y el resto una zancada o un paso; el compromiso lo sujeta (92 % de
los instantes distintos) mucho más que lo hace andar. (2) Quedarse quieto cuesta casi todo el paisaje: la d de `noop` está 0,154 por
encima del mejor candidato (el `spread` típico es 0,1-0,2). Andar el plan cuesta menos (0,065) y en 37 instantes nada: el paso hacia
el destino era mejor que cualquier candidato propio. Más aún: si se le ofreciera «ir al destino del plan» como candidato, el cuerpo solo lo
elegiría en el 49 % de los tics con plan vivo. El plan no le tuerce la dirección; le quita la impaciencia de salir. (3) La acumulada tiene
cola: mediana 0,28 pero p90 17 y máximo 102 (un plan de 197 tics con 183 sujeciones: el GIF).

### 2.2 · Soltados contra cumplidos (3): ¿hay umbral?

| acumulada al… | n | mediana | p10 | p90 | máx | tics vivo mediana | por 100 tics (mediana) |
|---|---|---|---|---|---|---|---|
| **A7h** soltar (reevaluación 132, vida 76) | 208 | 0,18 | 0,00 | 4,07 | 70,9 | 42,5 | 0,40 |
| **A7h** cumplir (andado) | 36 | **19,97** | 2,06 | 67,61 | 102,0 | 322,0 | **8,68** |
| A7h muerte / fin con plan vivo | 9 | 0,00 | | 0,53 | 0,95 | | |
| **A8** soltar (reevaluación 51, vida 19) | 70 | 0,29 | 0,00 | 3,32 | 12,6 | 39,0 | 0,68 |
| **A8** cumplir (andado) | 19 | 0,33 | -0,03 | 7,04 | 10,8 | 71 | 0,53 |

**No hay umbral, y la relación va al revés de un umbral.** En A7h los planes que llegan al final acumulan 110 veces más
deformación que los soltados, y 22 veces más por tic de vida: los planes que se cumplen son los de quedarse dentro del círculo mientras
el cuerpo quiere salir, y el cuerpo los aguanta enteros. Los rangos se solapan (6 soltados por encima de la mediana de los cumplidos; el mayor
soltado acumuló 71), y nada en el mecanismo mira la deformación: el plan cae cuando la puerta, al reevaluar, deja de darle ventaja
(132 de 208) o cuando la vida real cae bajo la proyectada (76); nunca porque el cuerpo lleve mucho aguantado. En A8, con planes cortos (mediana
71 tics los cumplidos), soltados y cumplidos acumulan lo mismo (0,29 contra 0,33).

### 2.3 · Si compensa (4): tics ardiendo ahorrados frente a deformación, en los cumplidos

Ahorro = tics ardiendo de la vida de A4 de la misma semilla (mismo asiento si vive toda la ventana; si no, el otro) en la misma ventana
[aceptación, fin del plan) menos los propios.

| cumplidos con pareja A4 | ahorro mediana · media · p10 · p90 | positivos · cero · negativos | arde propio (mediana) · arde A4 (mediana) | Spearman deformación-ahorro | ahorro por unidad de deformación (mediana) |
|---|---|---|---|---|---|
| **A7h** 30 de 36 | **0** · 41,9 · -17 · 147 | 13 · 6 · 11 | 8 · 2,5 | -0,0659 | 0,0 |
| **A8** 15 de 19 | **0** · 15,2 · -22 · 58 | 5 · 5 · 5 | 8 · 0 | 0,1818 | 0,0 |
| todos los planes con pareja A4 (A7h 188; A8 75) | -1 · 4,5; 0 · 4,3 | | | 0,1447; 0,1344 | |

**Compensa a medias y sin cuenta.** En la mitad de los cumplidos de A7h ni el cuerpo ni su pareja A4 ardieron en esa ventana (6 de 30 con
ahorro 0): el plan sujetó a un cuerpo que tampoco habría salido, o que A4 no salió. El ahorro está en la cola: 13 planes ahorraron hasta
236 tics, 11 costaron hasta 28. La media (+42 tics por plan cumplido) es la parte del −58 tics por vida de P6-24 que se
gana dentro de los planes; y no crece con lo que el cuerpo aguanta: Spearman -0,0659 (A8 0,1818). Un plan que dobla mucho no ahorra más que uno
que dobla poco: la deformación es el precio de quedarse, no una inversión.

### 2.4 · Huella (5)

| acuerdo diario-réplica (lo elegido = lo que elegiría solo) | A7h | A8 |
|---|---|---|
| 200 tics tras soltar o cumplir (todos los tics · con piernas listas) | **99,74 %** (42.156) · 99,08 % | **99,7 %** (17.031) · 98,8 % |
| A4, misma semilla y asiento, mismas ventanas | 98,84 % (30.768) · 99,55 % | 99,78 % (12.004) · 99,69 % |
| el mismo brazo, ventana [t_a−400, t_a−200) antes del plan | 99,67 % | 99,9 % |
| A4 en esa ventana previa | 98,75 % | 99,28 % |

**La mesa acertó: no queda nada.** Tras el plan, el cuerpo elige lo que elegiría solo en el 99,74 % de los tics; A4, que nunca tuvo plan, en el
98,84 % en las mismas ventanas, y el propio cuerpo antes del plan en el 99,67 %: diferencias de menos de un punto, del tamaño de la propia
infidelidad de la réplica (0,06 %). Es lo que se esperaba de un cuerpo que no aprende: el plan dobla mientras dura y nada más. Esta medida es casi
tautológica con una réplica tan fiel; su valor es confirmar que ni la memoria ni la confianza (que sí cambian con los planes) mueven una
decisión después.

### 2.5 · Oráculo contra razonador (6)

| | A7h | A8 | lectura |
|---|---|---|---|
| (1) instantes distintos | 83,93 % | 82,37 % | igual |
| (1) composición: sujeta · obedece | 92 · 8 % | 54 · 46 % | el razonador hace andar; el oráculo hace quedarse |
| (2) por instante: sujeta · obedece | 0,154 · 0,065 | 0,138 · 0,089 | mismo precio por tipo |
| (2) por instante, todos | 0,153 | 0,101 | A8 34 % menos, por la composición |
| (2) acumulada por plan: mediana · p90 | 0,28 · 17,0 | 0,27 · 3,9 | planes más cortos en A8 |
| (3) soltados · cumplidos (mediana) | 0,18 · 20,0 | 0,29 · 0,33 | en A8 no se distinguen |
| (4) ahorro en cumplidos: mediana · media | 0 · 42 | 0 · 15 | mismo dibujo, menos planes |

La misma puerta, el mismo cuerpo y el mismo compromiso cobran lo mismo por sujetar (0,154 contra 0,138) y por hacer andar; lo que cambia es
qué pide cada consejero: el oráculo pide quedarse dentro hasta el fin de la fase (planes de 295 tics en el p90, 92 % de sujeciones) y
el razonador pide ir a una casilla (46 % de obediencias, planes de 112 tics en el p90). Por eso A8 dobla menos por plan (p90 3,9 contra 17).

## 3 · EL SELLO, CONTRASTADO (`SELLO_P6_29.md`, md5 `1979af677b89a168d6e1623c5bd34f43`)

| | predicción | medido | veredicto |
|---|---|---|---|
| fidelidad de la réplica | ≥ 97 % | 99,94 / 99,94 / 99,86 % | acierta |
| 1 · fracción de instantes distintos | A7h 30-70 %, A8 20-60 %; sujeta > obedece | 83,93 % y 82,37 %; sujeta > obedece en los dos | **falla** (más de lo previsto) |
| 2 · por instante 0,01-0,08; acumulada mediana 0,2-3, p90 < 15 | | 0,153 / 0,101; acumulada 0,28 / 0,27, p90 17 / 3,9 | **falla** (por instante el doble; cola larga en A7h) |
| 3 · soltados < cumplidos, sin umbral | | 0,18 < 20,0 y 0,29 < 0,33; rangos solapados | acierta |
| 4 · ahorro mediana > 0 y \|rho\| < 0,3 | | mediana 0 y 0 (media +42 / +15); rho -0,0659 / 0,1818 | **falla** (la mediana no es positiva) |
| 5 · huella: diferencias < 3 puntos | | +0,9 y +0,07 (A7h); -0,08 y -0,2 (A8) | acierta |
| 6 · por instante dentro de 30 %; A8 acumula menos; fracción menor o igual | | por instante 34 % menos (por tipo, sí: sujeta a 10 %); acumulada y fracción, sí | **falla** (la composición, no el precio) |
| gasto | 0 en las dos bolsas | 0 y 0 | acierta |

Lo que la mesa no vio: que bajo un plan de quedarse el cuerpo quiere moverse en casi todos los instantes, y que quedarse quieto cuesta todo
el paisaje de candidatos, no una fracción. Lo que sí vio: que el cuerpo no guarda nada del plan.

## 4 · EL GIF Y LOS ARCHIVOS

`P6_29_deformacion.gif`: P623_t2_A7h_20994019 asiento 10, plan 13 (fase 5, cumplido: andado), tics 12789-12986: 183 sujeciones y 1 obediencia en 197 tics, acumulada
102 (la mayor de la serie), 4 tics ardiendo (A4 en esa ventana: 0). En el título, cada tic: lo ejecutado, lo que habría hecho solo, δ del instante y Δ acumulada.

| archivo | qué es |
|---|---|
| `sello_P6_29.py` → `SELLO_P6_29.md`, `P6_29_sello.json` | el sello, cerrado antes de la medida (rehecho tras el humo por un arreglo del lector; mismas predicciones) |
| `mide_P6_29.py` → `P6_29_medidas.json`, `P6_29_planes.json`, `P6_29_vidas.json` | la medida: réplica + diario; medidas por brazo; cada plan y cada instante; cada vida |
| `gif_P6_29.py` → `P6_29_deformacion.gif` | el GIF (copia de `gif_P6_23.py` con δ y Δ en el título) |

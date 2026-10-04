# P6-18 · Ir y quedarse: banco y campo

*27-sep-2026. Coste: **1,3131 USD** de 5 (1 partida corta de humo 0,0336 + 20 de
serie A6 1,2795). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al
principio y al final; los 202 congelados del cinco y los 32 del seis: 0
alterados al principio y al final. Nada nuevo entra en el cuerpo ni en la
puerta del cinco: lo nuevo es `compromiso6b_P6_18.py` (versión declarada de
compromiso6), `policy_pareja18.py` (A6), su humo, imagen y lanzador, y los
medidores. El oráculo sigue siendo el instrumento declarado de P6-14. Nada de
MettaScope. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

En el banco, **la puerta6 prefiere quedarse en 48 de los 63 momentos (76 %)** en
que A5h salió del círculo tras llegar (la puerta del cinco, en 0: no puede
juzgar la propia casilla), el veto vital no cae en la mayoría (17 de 63 en los
12 primeros tics) → el criterio pasó y se jugó A6. En el campo, **la sujeción
funciona como mecanismo (1.054 pasos sujetados en la fase 5) y el plan no se
sostiene**: de 74 planes aceptados en la fase 5, **2** llegan al final de la
fase; los demás caen porque «la vida real está por debajo de la proyectada»
(47) o en la reevaluación (25), y compromiso6b rompe 930 veces (672 veto
vital, 238 rival a ≤ 2). Las medidas por tics van en la dirección prevista
—dentro del círculo 35 % (A5h 27 %), ardiendo 159 tics (A5h 191, A4 196),
nunca entra 2 (6 y 6), sobreviven la fase 24 (17 y 21)— y **ninguna sale del
ruido** (p 0,37-0,85 emparejado). Sello: 1 acierto de dirección, 3 fallos.

---

## A · BANCO (coste cero)

### A.1 El plan «ir y quedarse» y qué puerta puede juzgarlo

Plan en el idioma de formas: `ir` a la casilla a salvo más cercana (0 pasos si
ya lo está) y `esperar` hasta el final de la fase. **La puerta del cinco no lo
puede juzgar**: su comparador es el mejor candidato propio proyectado, y `noop`
proyectado es la misma curva que quedarse → área 0,0 en 61 de 63 (los otros
2, «vida»). **La puerta6 sí**, porque su comparador es el cuerpo decidiendo
paso a paso, que sale del círculo y arde. Con una salvedad medida: con un solo
tramo `esperar` de 400 tics el punto de control queda a peso 0,5^(400/50) =
1/256 y la puerta6 tampoco ve nada (área 0,003); **el plan se escribe en 4
tramos** (ir, esperar 50, esperar 50, esperar resto), el máximo del idioma.
Declarado y usado en el banco y en A6. Destino: la propia casilla en los 63
momentos de A5h (todos a salvo) y en 10 de los 22 de A4 (los otros 12 ya
estaban fuera de r1: destino = la casilla segura más cercana).

### A.2 ¿Prefiere puerta6 quedarse en los momentos de salida?

63 momentos de A5h (el tic del último paso antes de salir, P6-17 §3) y 22 de
A4 (el último paso antes de la racha final de fuego de cada muerte por
anillo), cada vida repetida en seco por la vía real (`banco_P6_18.py`,
arnés de P6-15; el replay de A5h difiere del diario en 678 de 584.437 tics,
donde el cuerpo real obedeció a un plan). Margen 0,062.

| momentos | puerta del cinco | **puerta6 (B), H hasta el fin de fase** | puerta6, H 100 | contra lo real (A), H fase |
|---|---|---|---|---|
| **A5h, 63** | ok 0 · area 61 · vida 2 | **ok 48 (76,2 %)** · area 13 · vida 2; ventaja mediana 0,226 (ok 0,256) | ok 38 (60,3 %) | ok 51 (81,0 %) |
| A4, 22 | ok 1 · area 15 · vida 6 | ok 14 (63,6 %) · area 2 · vida 6; ventaja mediana 0,269 | ok 14 (63,6 %) | ok 14 (63,6 %) |

Filas (área sin la fila − con la fila, puerta6, H fase, 63 de A5h): **a
favor** de quedarse F-DANO (−0,121 de media, 57 planes), F-ANTICIPACION
(−0,089, 56), R-CARENCIA (−0,022), R-LLAMADA (−0,014); **en contra**
F-REENCUENTRO (+0,105, 7 planes), S-HERIDO (+0,015, 8). En los 22 de A4, en
contra S-8-EXPOSICION (+0,054, 19) y S-HERIDO (+0,136, 5); a favor
F-ANTICIPACION (−0,195) y F-DANO (−0,202). Lo que sostiene el quedarse en la
puerta6 es el daño y el anillo que el comparador se come al salir; lo que lo
frena es el hermano (reencuentro, herida).

### A.3 El veto vital

`compromiso6_P6_16.rupturas6 (a)` = un rival **visto** (o contado por el
hermano: la percepción lleva los ojos) con un arma de alcance > 0 del catálogo
a distancia Chebyshev ≤ su alcance. En los 353 registros de A5h las armas a
tiro son **arcos (121), cerbatanas (52) y lanzas (2)**: alcance 8 y 6, que
dentro del círculo de radio 5 cubre todo. En esos tics el cuerpo tiene 86 de
vida (mediana) y R-CARENCIA 0,58: **no lo dispara la vida ni la carencia, sino
el alcance de un arma ajena**. (Recalculado solo con los rivales vistos
coincide en 164 de 353: los otros son contados.) En las ventanas de quedarse
(del momento al fin de la fase, medido con la percepción real en el banco):
veto (a) en los 12 primeros tics en **17 de 63** (A4: 5 de 22), en algún tic
en 33 de 63, fracción mediana de tics con (a) 4,5 % (A4 0 %), con (d) vida <
15 6,6 % (A4 20 %). Total en las ventanas de A5h: 4.265 tics con (a), 1.539
con (d), 1.058 con (e), 20 con (c) de 17.383. **No rompería la mayoría de los
planes de quedarse al empezar; sí muerde durante**: en el campo (§B) fue la
ruptura que más rompió (672).

### A.4 R-CARENCIA al salir

R-CARENCIA = (3 − W)/3, con W = riqueza (`riqueza_W`: arma × munición +
botiquín + ración, objetivo 3 = «arma + botiquín + ración»). Es carencia de
**equipo**, no de comida en particular. En los 63 momentos de salida de A5h: W
= 1,0 (mediana), R-CARENCIA 0,67; falta **botiquín en 52, ración en 42, arma
en 34**. En los 22 de A4: 0,66, falta botiquín 18, ración 16, arma 10. Nivel
por vida (media de los tics): **A3 0,524 · A4 0,517 · A5h 0,558**; en la fase
que mata 0,520 · 0,538 · 0,581. Desglose medio de W (muestras cada 96 tics):
A3 arma 0,46 · botiquín 0,47 · ración 0,36; A4 0,54 · 0,42 · 0,37; A5h 0,50 ·
0,41 · 0,29. **A4 no tiene más carencia que A3**: el precio en comida de P6-11
(2,88 contra 3,95 recogidas) no aparece en la fila.

### A.5 S-MUERTE-PAREJA

Es el **duelo**: `factor × B` (B = roce con el hermano) desde `pareja_muerta`
(o su muerte prevista), con semivida 90 s y suelo 0,3·B. **No tira hacia
ningún sitio**: vale lo mismo para todos los candidatos, y `ir_pareja` deja de
generarse cuando el hermano ha muerto (`decisor_zs:470`). En los 27 momentos
de salida con la fila encendida (todos con `pareja_muerta`): el cuerpo elige
`move` 18, `ir_objeto`/`ir_botin` 7, `paso` 2; la casilla donde murió el
hermano **ardía en 26 de 27**, a 7 casillas (mediana); **20 de los 27 mueren
en los 300 tics siguientes**. El tirón que saca al cuerpo no es hacia el
hermano muerto: es la carencia (`ir_objeto`) y el apartarse (`move`) con el
duelo subiendo la necesidad.

### A.6 El criterio, calculado

Prefiere quedarse: **76,2 % ≥ 33,3 %**. Veto al salir: 17 de 63, no la
mayoría. **Pasa** → campo.

---

## B · CAMPO

### B.7 A6 y su humo

A6 = A5h (cuerpo del seis congelado, oráculo, puerta del cinco con el
comparador de puerta6, revisa6) con dos cambios: el plan del oráculo es «ir y
quedarse» (4 tramos hasta el fin de la fase) y el compromiso es
**compromiso6b** (`compromiso6b_P6_18.py`, copia declarada de compromiso6 con
dos cambios: el fin del plan es el final de la fase, no estar a salvo; y
estando a salvo, el paso es **sujetar**: si la acción del cuerpo es un
movimiento cuya casilla de llegada no sigue a salvo, se emite `none`; el
resto pasa). Imagen `gemv-anima:pareja18` (custodias del motor, decisor,
tabla, cinco y seis; los 12 humos anteriores y el nuevo), política
`gemv-p6-A6:v1` = `271d432d-9eab-4ed0-9b67-47197a3ef69b`.

Humo en el build (`humo_red_P6_18.py`, 200 observaciones reales, calendario
comprimido derivado por `Mundo.anillo_en`): 4 propuestas del oráculo, todas
tras el aviso; juicios en el hilo; una forma dada la anda compromiso6b; y la
**sujeción probada como mecanismo** (con la observación real y el cuerpo a
salvo, el paso que sale devuelve `none` y el que se queda dentro pasa;
declarado que la acción se construye porque el grabado, en bucle abierto, no
la produce). Humo de campo: 1 partida real corta (0,0336 USD): 2 planes
aceptados, reevaluados «ok» 4 veces, 116 tics vivos fuera de la casilla segura
(91 enfriamiento, 25 rupturas «rival a ≤ 2»), sin errores; la sujeción no
llegó a actuar porque el cuerpo no llegó a salvo. **Sello** antes de la
primera partida: `SELLO_P6_18.md`, md5 `0c97d77c7d03893dbaf224a4cc0e1d8a`.

### B.8 Medidas, por tics, vidas vivas al empezar la fase 5 (aviso 11.856)

`mide_campo_P6_18.py`, definiciones de P6-17: dentro = distancia al centro
≤ 5; ardiendo = distancia > `zona.radius` del tic; ventana [11.856, 12.996).

| | **A4** | **A5h** | **A6** |
|---|---|---|---|
| vidas vivas en el aviso | 35 | 34 | 35 |
| **% de tics dentro del círculo**, media · mediana | 32,7 · 22,3 | 27,4 · 17,9 | **35,4 · 35,3** |
| **tics ardiendo**, media · mediana | 196 · 205 | 191 · 223 | **159 · 157** |
| vidas con 0 tics ardiendo · nunca entran | 6 · 6 | 4 · 6 | 5 · **2** |
| sobreviven la fase 5 | 21 | 17 | **24** |
| planes aceptados en la fase · **sostenidos hasta el fin de fase** | — | 89 · 0 (no era el plan) | 74 · **2** |
| cómo acaban los planes | — | andado 41 · caída vida real < proyectada 26 · reevaluación area 15, vida 7 | **caída vida real < proyectada 47** · reevaluación area 21, vida 4 |
| compromiso: sujeta · obedece · enfriamiento · rompe | — | 0 · 479 · 1.554 · 359 | **1.054** · 644 · 1.831 · **930** |
| rupturas | — | a) 284 · d) 64 · e) 11 | **a) 672 · e) 238 · d) 20** |
| *secundarias (poca potencia):* muertes por anillo · por rival · supervivientes (40 vidas) | 22 · 6 · 11 | 19 · 12 · 5 | 21 · 7 · 12 |

**Emparejado por semilla** (A6 − X; media de la diferencia, semillas que
ganan / pierden, p de permutación por cambio de signo):

| | A6 − A4 | A6 − A5h |
|---|---|---|
| % dentro (media por semilla) | −1,6 pp (9 / 9), p 0,85 | +6,2 pp (9 / 8), p 0,46 |
| tics ardiendo (media por semilla) | **−32 (7 / 11), p 0,42** | **−33 (7 / 10), p 0,37** |
| supervivientes | +0,05 (6 / 6), p 1,00 | +0,35 (8 / 4), p 0,25 |
| muertes por anillo | −0,05 (7 / 7), p 1,00 | +0,10 (9 / 7), p 0,83 |
| muertes por rival | +0,05 (6 / 4), p 1,00 | −0,25 (4 / 8), p 0,31 |

**Nada sale del ruido.** Lo que sí se ve en los recuentos: (1) la sujeción
actúa 1.054 veces en la fase 5 y solo 2 vidas no entran nunca (6 y 6 antes);
(2) el plan no se sostiene: 47 caen por «vida real por debajo de la
proyectada − 10» —la curva del plan de quedarse no lleva daño de rivales, y
dentro del círculo los hay: al primer golpe el plan cae— y 25 en la
reevaluación; (3) compromiso6b rompe 930 tics, 672 por el veto vital (arcos y
cerbatanas a tiro dentro del círculo) y 238 por rival a ≤ 2; con la ruptura,
la acción del cuerpo pasa y sale.

Por vida (`P6_18_campo.json`): en 6 vidas A6 se queda donde A5h salió
(`22250767` s11: 3,8 % → 77 % dentro, 360 → 0 ardiendo, muere → vive;
`21622393` s10: 10 → 68 %; `22041309` s10: 12,5 → 67 %; `21203477` s11: 18 →
59 % con 557 sujeciones y muere por rival; `22041309` s11; `21831851` s10) y
en otras tantas es al revés (`20679832` s10: 100 % → 1,5 %; `20784561` s11;
`21727122` s11).

### B.9 GIF

`P6_18_quedarse.gif` (103 fotogramas, 11.856 → 12.996; md5 en el
manifiesto): `21622393` asiento 10, A6 —en A5h salió del círculo (10 % dentro,
292 tics ardiendo, murió por el anillo); aquí 68 % dentro, 25 pasos obedecidos,
28 sujetados, sobrevive—, con el hermano, el plan (estrella) y lo que hizo
compromiso6b en cada tic.

### B.10 El sello, contrastado

| predicción (`0c97d77c…`) | medido | |
|---|---|---|
| 1. tics ardiendo en la fase 5: A6 por debajo de A5h (191) y A4 (196), más vidas a 0 que A5h (4) | 159 (−33 y −32 emparejados, p 0,37 y 0,42); 5 vidas a 0 | acierta en dirección, sin salir del ruido |
| 2. más de la mitad de los planes aceptados se sostienen hasta el fin de fase; rupturas (a) y luego (d) | **2 de 74**; rupturas (a) 672, **(e) 238**, (d) 20 | **fallo** (y (e) antes que (d)) |
| 3. % dentro: A6 por encima de A5h y de A4 | 35,4 contra 27,4 (+6,2, p 0,46) y 32,7 (−1,6 emparejado) | a medias |
| 4. secundarias: anillo 8-19, rival ≥ 12, supervivientes 5-11 | 21 · 7 · 12 | fallo en las tres (todas dentro del ruido: ±11, ±9, ±10 vidas) |
| 5. rollout ~660 ms, la decisión no espera | humo: 500 ms; sin errores | acierta |

---

## C · LO QUE DICE LA MEDIDA (sin proponer nada)

1. La puerta6 quiere quedarse en tres de cada cuatro salidas; la del cinco no
   puede ni verlo. Lo que pesa a favor es el daño y el anillo que el
   comparador se come al salir; en contra, el hermano.
2. El veto vital es el alcance de un arma ajena (arco, cerbatana), no la vida
   ni la carencia; al empezar el plan no lo rompe, durante sí.
3. R-CARENCIA al salir es falta de botiquín y ración (y arma), y no es mayor
   en A4 que en A3.
4. S-MUERTE-PAREJA no tira hacia el hermano muerto: sube la necesidad; el
   cuerpo sale por la carencia y por apartarse, y 20 de 27 mueren después.
5. En el campo, sujetar al cuerpo dentro funciona como mecanismo (1.054
   veces) y el plan muere antes que el cuerpo: cae por la vida real bajo la
   proyectada (47) y por el veto vital (672 tics). Las medidas por tics van en
   la dirección buena (dentro +6 pp sobre A5h, ardiendo −32 tics, nunca entra
   2 de 35) y no salen del ruido con 20 semillas.

---

## D · ARCHIVOS

| archivo | md5 | qué es |
|---|---|---|
| `banco_P6_18.py` · `corre_P6_18.py` · `resume_P6_18.py` | `493df3b5…` | el banco de A.2 (85 momentos, tres puertas) |
| `mide_P6_18.py` · `P6_18_momentos.json` · `P6_18_medidas_A.json` | `ece14f4c…` · — · `6a0c3252…` | A.3-A.5 |
| `P6_18_banco.json` | `219d9f6d…` | los 85 momentos juzgados, filas, veto, criterio |
| `compromiso6b_P6_18.py` | `cf2557f9…` | compromiso6b, versión declarada |
| `policy_pareja18.py` · `humo_red_P6_18.py` · `Dockerfile.pareja18` · `lanza_P6_18.py` | `249aa0b2…` · — · — · — | A6 |
| `sello_P6_18.py` · `SELLO_P6_18.md` · `P6_18_sello.json` | — · **`0c97d77c7d03893dbaf224a4cc0e1d8a`** · — | el sello |
| `mide_campo_P6_18.py` · `P6_18_campo.json` | `e7387789…` · `a4639a30…` | B.8 |
| `P6_18_quedarse.gif` | `3bc244690cfb5b968c242ec36d43ba2e` (manifiesto) | B.9 |
| `P6_18_brazos.json` · `P618_t*_*.json` | — | política y las 21 partidas |
| diarios `paintball/runs/P618_t{0,1}_*` | 84 filas en `DIARIOS_P6_MANIFIESTO.md` | fuera de git |

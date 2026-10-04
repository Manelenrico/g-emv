# P6-23 · La serie válida del puente, sin pasos perdidos

*28-sep-2026. Gasto **3,3395 USD** de 5 (humo 0,0670 + 40 partidas 3,2725). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco y
los 32 del seis: 0 alterados al principio y al final. Lo nuevo, en archivos aparte y
declarado: `compromiso6c_P6_23.py` (veto V2 y cuenta justa), `puerta_proceso_P6_23.py` (juicio
y oráculo en el proceso), `policy_pareja23.py` (A7v / A7h), `humo_red_P6_23.py`,
`Dockerfile.pareja23`, `lanza_P6_23.py`, `sello_P6_23.py` → `SELLO_P6_23.md`
(md5 `98250e37cebe05a043de51b4d972e84e`, cerrado antes de la tanda 1), `mide_campo_P6_23.py` →
`P6_23_campo.json`, `P6_23_pasos_humo.json`, `P6_23_pasos_serie.json`, `atribuye_pasos_P6_23.py` →
`P6_23_pasos_atribucion.json`, `gif_P6_23.py` → `P6_23_quedarse.gif`. Humos por la vía real. Ningún número se escribió antes de calcularlo.
Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**Con el oráculo y la puerta fuera del hilo principal, el puente se juega sin perder pasos:
0 en el humo (dos partidas hasta la fase 7) y 36 de 11.253 (0,3 %) en las fases 5-7 de la
serie (A6: 40,5 %; A4: 0).** En las vidas vivas en el aviso de la fase 5, A7h (puerta6) está
dentro del círculo el **42,4 %** de los tics (A4 32,7, A7v 35,6), arde **115 tics** (A4 196,
A7v 149; emparejado contra A4 −79, p = 0,046, la única diferencia que sale del ruido), y
sostiene **6 de 58 planes** hasta el final de la fase (A6: 2 de 74; A7v: 0 de 109). El veto
V2 hace lo que dice: **0 rupturas por ver un arma** (A6: 726), 60-81 alertas, **2-4
suspensiones** por primer golpe, 0 reanudaciones (los planes suspendidos cayeron antes de
los 96 tics), 13 retenciones y 0 salidas. La cuenta justa no llegó a decidir ninguna caída
(0 planes cayeron con daño desviado acreditado): los planes que caen por vida (A7h 19, A6 47)
caen siguiéndose. Lo que sí cambia con la puerta: el comparador del cinco (A7v) **acepta 109
planes y deja caer 104 en la reevaluación**; puerta6 acepta 58 y sostiene 6. La
pareja acepta los dos en 11-13 semillas de 20. Las secundarias van en la dirección prevista
y dentro del ruido: muertes por anillo 13-14 (A4 22), supervivientes 10-13 (A4 11). El
sello: **5 aciertos, 3 no alcanzadas, 1 fallo** (A7h no acepta más planes que A7v, sino
menos, y los sostiene).

---

## 1 · EL TIC DE PROPUESTA DEL ORÁCULO, FUERA DEL HILO PRINCIPAL

P6-22 dejó el juicio de la puerta en un proceso aparte y los 7 pasos perdidos que quedaban
estaban en el tic de propuesta del oráculo (BFS de casillas seguras, `seguras` 6 ms por tic,
traductor). `puerta_proceso_P6_23` (versión nueva de la de P6-22, sin depender de
`policy_pareja18`, que exige puerta6) admite dos encargos: **juicio** (como P6-22) y
**oráculo**: el hilo principal solo comprueba la puerta de entrada (fase, plan vivo,
cadencia, silencio, piernas listas) y manda la observación con lo poco que el oráculo lee
(tic, último tic de propuesta, si el hermano vive y dónde, el último parte); el alma espejo
del proceso calcula `seguras`, `dispara`, `propone`, el texto del plan y su traducción, y
devuelve la propuesta con sus registros (marcados `en_proceso`), que el hilo principal deja
donde la dejaba el oráculo (`cf.entregado`) al recogerla, uno o dos tics después. Coste en
el hilo principal: **0,14 ms** de mediana por encargo en el bucle real (315 encargos) y
0,04-0,12 ms por vida en la serie (350-2.678 encargos por vida); el oráculo en el hilo
principal, 0,01 ms de mediana por tic (P6-22: `seguras` 6 ms, hasta 27 en el tic de propuesta).

**En el bucle real con mundo que no espera** (`mide_bucle_P6_22.py --brazo A7h`, mismo
diario que P6-22): 0 acciones perdidas, 0 tarde, `decidir` mediana 3,3 ms y máximo **22,9**
(A6: 103,4; A6p: 39,3); 13 propuestas y 22 juicios del proceso, 0 errores. **Humo de red**
(`humo_red_P6_23.py`, en los dos brazos, en nativo y dentro de la imagen): las 4 propuestas
vuelven del proceso en 1 tic, la puerta juzga en el proceso, compromiso6c anda una forma dada
y sujeta el paso que sale, y el veto V2 como mecanismo (observación real, golpe y acción
construidos, declarado): golpe → `suspende` + `retenido` (acción `none`), 97 tics sin golpe
→ `reanuda`; reloj que no espera: 200 de 200 acciones, **0 perdidas**.

**Humo con dos partidas reales** (A7h, mundo corto de P6-18 hasta la fase 7, semillas
20260916 y 20365645, 0,0670 USD): pasos listos hacia casilla libre que no se dan **0 de 305 /
344 / 165** (antes del aviso / fases 1-4 / fases 5-7), 0 fantasmas, retraso de los 820 pasos
dados 0 tics; el oráculo propone desde el proceso (4 propuestas, 0 en el hilo principal), la
puerta juzga en el proceso (10 veredictos, 0 errores), 4 alertas, 1 suspensión, 16 rupturas
«e) rival a 2 o menos» (sin alcance). **Se llegó a 0: se jugó la serie.**

## 2 · LA SERIE (`lanza_P6_23.py`, `SELLO_P6_23.md`)

Mundo 0.1.19, `roster_lento_v2`, las 20 semillas de A4, una imagen (`gemv-anima:pareja23`) y
dos políticas: **A7v** = `gemv-p6-A7v:v1` (`09416d94-…`, `GEMV_PUERTA6=0`: puerta del cinco con
su comparador) y **A7h** = `gemv-p6-A7h:v1` (`219ef011-…`, `GEMV_PUERTA6=1`: comparador
puerta6). Las dos con el oráculo (plan «ir y quedarse», tramos 50/50/resto), compromiso6c
(V2 + cuenta justa) y juicio y oráculo en proceso. **A4** (P6-11) es la línea base. 40
partidas, 80 diarios enteros, 3,2725 USD.

`compromiso6c` (declarado): ver un arma a tiro no rompe (registra `alerta` cuando cambia el
conjunto de armados a tiro); queda «e) rival a 2 o menos» solo para rivales sin alcance (con
V0 la regla a) saltaba antes para los armados, así que esta solo veía manos vacías: se
mantiene igual) y «d) vida / carencia»; un golpe de rival con el plan vivo suspende (manda la
tabla) hasta 96 tics sin golpe; suspendido y a salvo, el paso que sale del círculo se retiene
salvo que el daño esperado dentro (tabla de P6-19) supere el fuego de fuera; cuenta justa:
la revisión de vida compara `hp + daño recibido en los tics desviados` (desde una ruptura
hasta volver a estar a salvo) con la proyectada menos 10.

## 3 · LAS MEDIDAS (`mide_campo_P6_23.py`, vidas vivas en el aviso de la fase 5)

| | A4 | A7v | A7h |
|---|---|---|---|
| vidas · vivas en el aviso 5 | 40 · 35 | 40 · 36 | 40 · 39 |
| **pasos perdidos**, fases 5-7 (P6-21) | 0 / 4.209 (**0,0 %**) | 16 / 5.719 (**0,28 %**) | 20 / 5.534 (**0,36 %**) |
| pasos perdidos, toda la vida | 5 / 31.772 (0,02 %) | 32 / 33.347 (0,10 %) | 28 / 29.518 (0,09 %) |
| % de tics dentro del círculo, fase 5 (media · mediana) | 32,7 · 22,3 | 35,6 · 29,6 | **42,4 · 37,4** |
| tics ardiendo, fase 5 (media · mediana) | 196 · 205 | 149 · 120 | **115 · 66** |
| vidas con 0 tics ardiendo · nunca entran | 6 · 6 | 7 · 0 | 7 · 2 |
| sobreviven la fase 5 | 21 | 27 | 29 |
| planes aceptados · andados · **sostenidos hasta el fin de fase** | — | 109 · 102 · **0** | 58 · 54 · **6** |
| caídas: reevaluación (área) · vida real · (vida) | — | 104 · 3 · 2 | 30 · 19 · 2 |
| rupturas: a) veto vital · e) armado acercándose | — | **0 · 0** | **0 · 0** |
| rupturas: e) rival sin alcance a ≤ 2 · d) vida bajo 15 | — | 248 · 16 | 397 · 0 |
| alertas (vidas con ≥ 1) · suspensiones · reanudaciones · retenido · sale | — | 60 (15 de 36) · 4 · 0 · 2 · 0 | 81 (15 de 39) · 2 · 0 · 13 · 0 |
| compromiso: obedece · sujeta · enfriamiento | — | 296 · 220 · 2.538 | 192 · **2.021** · 1.656 |
| semillas en que aceptan los dos asientos | — | 13 de 20 | 11 de 20 |

Secundarias (poca potencia, declarado; ±10 vidas es lo detectable con 20 semillas):

| | A4 | A7v | A7h |
|---|---|---|---|
| muertes por anillo · por rival · supervivientes | 22 · 6 · 11 | 13 · 13 · 10 | 14 · 12 · 13 |

**Emparejado por semilla** (media de la diferencia, gana / pierde, permutación exacta):

| | A7h − A4 | A7v − A4 | A7h − A7v |
|---|---|---|---|
| % dentro (fase 5) | +7,3 · 11/6 · p 0,35 | −0,1 · 9/9 · p 1,0 | +9,1 · 13/7 · p 0,21 |
| tics ardiendo | **−79,2 · 6/12 · p 0,046** | −30,9 · 9/9 · p 0,43 | −46,3 · 5/15 · p 0,10 |
| planes sostenidos | +0,3 · 5/0 · p 0,06 | 0 | +0,3 · 5/0 · p 0,06 |
| planes aceptados | +2,9 · 18/0 · p < 0,001 | +5,5 · 18/0 · p < 0,001 | **−2,6 · 3/13 · p 0,014** |
| muertes por anillo | −0,4 · 6/10 · p 0,23 | −0,45 · 4/10 · p 0,18 | +0,05 · p 1,0 |
| muertes por rival | +0,3 · 8/3 · p 0,27 | +0,35 · 10/2 · p 0,12 | −0,05 · p 1,0 |
| supervivientes | +0,1 · p 0,85 | −0,05 · p 1,0 | +0,15 · p 0,62 |

**Los 36 pasos perdidos de la serie, uno a uno** (`atribuye_pasos_P6_23.py` →
`P6_23_pasos_atribucion.json`; en 6 vidas de A7v y 8 de A7h): 14 en el tic en que el hilo
principal encarga un juicio al proceso o el siguiente (A7v 2, A7h 12; el cuerpo tardó 39-78 ms
en 10 de esos 14 tics: la instantánea del juicio tarda en la plataforma 5-49 ms de mediana por
vida, hasta 70), 1 en el tic de propuesta del oráculo y 21 en tics sin encargo ni propuesta
(A7v 14, A7h 7): de esos 22, 14 con el cuerpo a 36-71 ms y 8 por debajo de 29 ms, es decir,
tics que la máquina de la plataforma pasó de largo sin que fuera la puerta ni el oráculo.
Retraso de los pasos dados: 0 tics en todos salvo 2 (1 tic); fantasmas 6 y 3. En A4, 5 pasos
perdidos en toda la vida.

**Lo que dicen las medidas.** (1) La infraestructura cumple: 0,3 % de pasos perdidos, contra
40,5 % en A6, y las decisiones en el tic (`decidir` máx. 22,9 ms en el bucle real). (2) El
veto V2 quita las 726 rupturas por ver un arma y las cambia por alertas que no rompen; las
suspensiones son 2-4 en 40 vidas (P6-20 predijo pocas: 1 primer golpe sujeto en 40 vidas de
A6) y ninguna llega a reanudarse: el plan cae en la reevaluación antes de los 96 tics.
(3) Con la puerta6, el cuerpo **se queda más y arde menos**: 42 % dentro y 115 tics ardiendo
contra 33 % y 196 en A4 (el emparejado de ardiendo sale del ruido, p = 0,046); 2.021 tics
sujetos (A6: 1.054). (4) El comparador del cinco acepta el plan de quedarse casi siempre (109,
en 31 de 36 vidas) y lo suelta en la reevaluación (104 de 109 caen por área): con él el plan
no vive. La puerta6 acepta menos (58, en 29 de 39 vidas) y sostiene 6 hasta el final de la
fase; el resto cae por área (30) o por vida real (19). (5) La cuenta justa no decidió ninguna
caída: ninguno de los 19 planes de A7h que cayeron por vida llevaba daño desviado acreditado
(con V2 casi no hay rupturas que desvíen: 397 «rival sin alcance a 2», que sueltan al cuerpo
un tic). Los planes siguen cayendo por fuego recibido siguiendo el plan (P6-20 §3). (6) En
vidas, nada sale del ruido, como P6-17 anunció.

## 4 · EL SELLO, CONTRASTADO (`SELLO_P6_23.md`, md5 `98250e37cebe05a043de51b4d972e84e`)

| sello | predicción | medido | veredicto |
|---|---|---|---|
| S1 pasos perdidos, fases 5-7 | 0 en los dos brazos; falla si > 0,5 % | A7v 0,28 %, A7h 0,36 % | **no alcanzada** (no es 0; no llega al fallo) |
| S2 rupturas a) y e-armado 0; alertas ≥ 1 en la mitad de las vidas | | 0 y 0; alertas en 15 de 36 (42 %) y 15 de 39 (38 %) | **no alcanzada** en la segunda cláusula (falla si < 25 %: no) |
| S3 sostenidos A7h ≥ 20 % de los aceptados | falla si < 10 % | 6 / 58 = 10,3 % | **no alcanzada**, sin fallo |
| S4 % dentro A7h > 35,4 | falla si < 32,7 | 42,4 | **acierta** |
| S5 ardiendo A7h < 159 | falla si > 196 | 115,5 | **acierta** |
| S6 suspensiones ≤ 10 (reanudaciones ≤ suspensiones) | falla si > 30 | 2 (0) | **acierta** |
| S7 caídas por vida real A7h ≤ 30 | falla si ≥ 47 | 19 | **acierta** |
| S8 aceptados A7h ≥ 3 × A7v | falla si < 1,5 × | 58 contra 109 | **falla** (al revés: el comparador del cinco acepta más y no sostiene) |
| S9 secundarias (sin sello) | anillo ≤ 22; supervivientes ≥ 11 | 14; 13 | en la dirección prevista, dentro del ruido |
| S10 gasto ≤ 5 USD | | 3,3395 | **acierta** |

**5 aciertos, 3 no alcanzadas, 1 fallo.** El fallo dice algo que P6-16 no había medido:
con el plan de quedarse en cuatro tramos, la puerta del cinco lo acepta (A5v aceptaba 3 con el
plan de ir de P6-16) y lo tira 25 tics después; la de puerta6 filtra al entrar y sostiene.

## 5 · EL GIF (`gif_P6_23.py` → `P6_23_quedarse.gif`, fuera de git, md5 en el manifiesto)

A7h, semilla 20784561, asiento 11, tics 11.800-12.996 (107 fotogramas, uno cada 12 tics): la
vida con menos tics ardiendo (44) entre las que sostuvieron un plan hasta el aviso 6. Se ve el
anillo cerrándose, el plan aceptado (estrella verde), los pasos que compromiso6c anda y
sujeta, los veredictos de la puerta al volver del proceso (en el título) y las alertas (anillo
ámbar) cuando un arma queda a tiro; el cuerpo se queda dentro hasta el aviso siguiente.

## 6 · ARCHIVOS

| archivo | qué es |
|---|---|
| `compromiso6c_P6_23.py` | veto V2 (alerta, suspensión, retención/salida, reanudación) y cuenta justa |
| `puerta_proceso_P6_23.py` | el proceso juez con dos encargos: juicio y oráculo |
| `policy_pareja23.py` · `humo_red_P6_23.py` · `Dockerfile.pareja23` · `lanza_P6_23.py` · `P6_23_brazos.json` | la política A7v/A7h, su humo, la imagen, el lanzador, las dos políticas subidas |
| `sello_P6_23.py` → `SELLO_P6_23.md`, `P6_23_sello.json` | el sello, con los md5 de lo que juega y de lo que mide |
| `mide_campo_P6_23.py` → `P6_23_campo.json` | las medidas por tics y planes, emparejadas |
| `mide_pasos_P6_22.py` → `P6_23_pasos_humo.json`, `P6_23_pasos_serie.json` | pasos perdidos, fantasmas y retraso por fase |
| `atribuye_pasos_P6_23.py` → `P6_23_pasos_atribucion.json` | los 36 pasos perdidos de las fases 5-7, uno a uno, con lo que hacía el hilo principal |
| `gif_P6_23.py` → `P6_23_quedarse.gif` | el GIF |
| `P623_t*_*.json` · `DIARIOS_P6_MANIFIESTO.md` | las 42 partidas (peticiones y finales) y los 84 diarios con su md5 (fuera de git) |

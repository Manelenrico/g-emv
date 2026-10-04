# P6-27 · El encargo ligero, el humo y la serie de A8

*28-sep-2026. Gasto total **4,59 USD** de 8: plataforma 3,4304 (42 partidas: 2 de humo a 0,065 y 40 de serie a
0,082 de media) + lenguaje 1,1585 por el sidecar (humo 0,0548, serie 1,1037); más 2-3 llamadas del humo
nativo con la clave (tope propio 0,05 USD), no contadas aparte. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco y los 32 del seis:
0 alterados al principio y al final. La clave no se imprimió ni se escribió; en el campo, sidecar de Bedrock.
Lo nuevo, en archivos aparte y declarado: `puerta_proceso_P6_27.py`, `policy_pareja27.py`, `humo_red_P6_27.py`
→ `P6_27_banco_arreglo.json`, `Dockerfile.pareja27`, `lanza_P6_27.py`, `P6_27_brazos.json`; `mide_P6_27.py` →
`P6_27_humo.json`, `P6_27_serie.json`, `P6_27_falsas_A7h.json`; `mide_campo_P6_27.py` → `P6_27_campo.json`;
`mide_pasos_P6_22.py` → `P6_27_pasos_humo.json`, `P6_27_pasos_serie.json`; `sello_P6_27.py` → `SELLO_P6_27.md`
(md5 `021e011ba62e28d9bd6e78fd837c013e`, cerrado tras el humo y antes de la serie) y `P6_27_sello.json`.
Ningún número se escribió antes de calcularlo. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**El encargo del razonador ya no cuesta un tic (0,06 ms por mensaje, 0 pasos perdidos en tics de consulta), y
A8 jugó las 40 semillas del puente: contra A4 arde 10 tics menos por vida en las fases 5-7 (n 34, mediana −13,
p unilateral 0,35, IC95 [−56, +38]): la dirección de la mesa, sin prueba. Contra A7h arde 43 tics más
(mediana +62, p 0,08); acepta menos de la mitad de los planes (58 contra 128 en la fase 5) porque el 54 % de los
que pasaban al pedir se rechazan al llegar (retraso 94 tics de mediana), y sostiene 8 contra 25. Las
aceptaciones falsas son las mismas en los dos consejeros: lo vivido es peor que lo imaginado en el 74 % de los
planes de A8 y el 76 % de los del oráculo.** Sello: la principal no alcanzada (dirección sin prueba, como
la mesa predijo: «menor o nulo»); las secundarias, en su sitio salvo tres (más rechazos a la llegada, menos
aceptados y más intraducibles de lo previsto).

## 1 · EL ARREGLO (infraestructura; ninguna decisión cambia)

**Qué cambia** (`puerta_proceso_P6_27.py`, `policy_pareja27.py`): en P6-26 el hilo principal mandaba al
proceso, cada 25 tics, la instantánea entera (memoria, bloqueos, mundo, historial, ~1 MB) para que el
proceso decidiera si disparaba: 726 encargos en 4 vidas para 11 consultas, tres pasos perdidos en tics de
encargo. Ahora, como el oráculo de A7h (P6-23):

- **Encargo ligero, cada tic, desde un gancho en `Memoria.observa`** (`policy_pareja27._observa_gancho`,
  solo para la memoria del alma A8): el mismo `obs` que el cuerpo acaba de observar (con los mensajes
  gemelos del oído y los ojos), la acción del tic anterior y los dos campos que escribe el decisor
  (`cedidos`, `ultimo_ataque`): 1,5-6,6 KB, `pickle.dumps` + `Queue.put`.
- **Memoria espejo en el proceso** (`_juez27`, encargo `tic`): el proceso repite exactamente lo que el
  cuerpo hace en `policy_cortex.decidir:425-427`, `mem.observa(obs, mundo, tick)` y `bloqueos.actualiza(obs,
  mundo, ultima_accion, tick)`, y copia los dos campos del decisor. Así el espejo es la memoria del cuerpo,
  tic a tic, sin copiarla nunca.
- **La consulta es otro mensaje ligero** (`hilo.pregunta`, desde la misma puerta de entrada de A7h: fase,
  plan vivo, cadencia, silencio, piernas listas, ninguna en vuelo): la observación del tic, los candidatos
  del cuerpo y unos escalares, lo mismo que P6-26 leía en ese momento. El proceso decide el disparo
  (`Oraculo.dispara`, BFS de 6 ms), construye el texto sobre su espejo y llama al modelo en un hilo del
  proceso; el juicio con la instantánea de la pregunta lo hace sobre una copia de su espejo (en el proceso).
- **Por qué el hilo principal ya no espera:** solo serializa dicts pequeños y encola en memoria (el hilo
  alimentador de `multiprocessing.Queue` escribe en la tubería); BFS, texto, llamada, traducción y juicio de
  pregunta ocurren en el proceso; los resultados vuelven por la cola de salida que `recoge()` lee con
  `get_nowait`. Lo único que el hilo principal sigue pagando es lo de P6-23: la instantánea de cada juicio
  de la puerta a la llegada (`_recoge(obs)` → `encarga_juicio(fv, self, obs)`), sin cambios.

**Medido en el campo** (78 vidas de la serie, `resumen27`): mensaje del tic 0,058 ms de mediana por vida
(máximo 10,1 ms en una vida, 0,3-0,7 en las demás), pregunta 3,9 ms de máximo, el espejo 2,1 ms de máximo
por tic; en el humo nativo a reloj, 450 decisiones, 0 tarde.

**Banco del arreglo** (`humo_red_P6_27.py --modo replay --reloj` → `P6_27_banco_arreglo.json`): las 4 vidas
del humo de P6-26 repetidas con `policy_pareja27`, las mismas observaciones y las mismas respuestas del modelo
(las grabadas, entregadas en el tic en que volvieron en el campo), a ritmo de reloj. En las 3 vidas con
consultas, la primera pregunta cae en el mismo tic que en el campo (12606, 12419, 11733); **los 7 textos de
escena comparables son idénticos (md5) a los del campo**; los **5 planes juzgados en los dos sitios reciben el
mismo veredicto** (area / ok; area / area / vida). Después de la primera respuesta las cadencias divergen: el
juez del banco (Mac) devuelve el veredicto 20-30 tics antes que el pod, la siguiente pregunta llega antes y
no tiene respuesta grabada (12721 contra 12732); son diferencias de reloj, no del espejo. Por el camino el
banco destapó dos defectos míos, corregidos: el arnés de humo de P6-26 no aplicaba los arreglos del seis
(oído, don, filas10, manos11) que el campo sí aplica, y la pregunta debía llevar la observación del tic porque
`_oraculo16` corre antes de que el cuerpo observe ese tic (el espejo está en t−1, como la memoria que P6-26
copiaba).

## 2 · EL HUMO NUEVO (mismas 2 semillas de P6-26, política `gemv-p6-A8:v2` = `f6906966-…`)

| | 20260916 s10 | 20260916 s11 | 20365645 s10 | 20365645 s11 | total |
|---|---|---|---|---|---|
| llamadas · coste (sidecar) | 3 · 0,0114 | 2 · 0,0087 | 4 · 0,0300 | 1 · 0,0048 | 10 · 0,0548 USD |
| retraso (mediana) · planes traducidos · intraducibles | 81 · 3 · 0 | 110 · 2 · 0 | 104 · 4 · 0 | 113 · 1 · 0 | 104 (p95 155) · 10 · 0 |
| pasaban al pedir · pasan al llegar · aceptados | 1 · 0 · 0 | 0 · 0 · 0 | 1 · 1 · 1 | 0 · 0 · 0 | 2 · 1 · 1 |
| E2 sustituidos · plan del hermano recibido | 0 · 0 | 0 · 0 | 1 · 0 | 0 · 1 | 1 · 1 |
| **pasos perdidos, fases 5-7** | 0 | **1** | 0 | 0 | **1 de 247 (0,40 %)** |

**Criterio (a)**: 0 pasos perdidos en tics de encargo o consulta del razonador. El único perdido está en el
tic 12774 de 20260916 s11: el tic en que LLEGÓ la respuesta y la puerta encargó dos juicios (el razonador
dio dos formas), con instantáneas de 23,8 y 17,2 ms: 42,5 ms el tic. Es el coste conocido de P6-23 (la
instantánea del juicio), que A7h paga igual; no es el encargo ni la consulta del razonador. **Criterio (b)**:
1 de 247 contra A7h en esas mismas semillas, 7 de 718 (0,97 %, P6-23). Los dos se cumplen: se selló y se
lanzó la serie.

## 3 · LA SERIE: A8 EN LAS 40 SEMILLAS DEL PUENTE (`P6_27_campo.json`, `P6_27_serie.json`)

40 partidas, 78 diarios (la plataforma borró dos pods antes de recoger su diario: 21517664 s11 y 24450076
s10; esas dos partidas entran con un solo diario en las medidas por vida y no entran en las emparejadas por
semilla). Vivas en el aviso 5: A4 74 de 80, A7h 77 de 80, **A8 66 de 76**.

**Medida principal** (tics ardiendo en las fases 5-7, por vida viva en el aviso 5, media por semilla,
emparejado; A8 − A4 unilateral como en P6-24; Monte Carlo de 10⁶ cambios de signo):

| | A4 | A7h | A8 |
|---|---|---|---|
| tics ardiendo 5-7, media · mediana | 232,3 · 233,5 | 174,7 · 146 | **220,4 · 231,5** |
| **A8 − A4** | | | **−9,9** (mediana −13; 15 / 19; **p unilateral 0,35**, bilateral 0,70; IC95 [−56,3, +38,4]; n 34) |
| A8 − A7h | | | **+43,1** (mediana +61,5; 22 / 13; p 0,077; IC95 [−1,3, +89,2]; n 35) |
| A7h − A4 (P6-24, 40 semillas) | | | −57,6 (p 0,007) |

**Secundarias** (sin sello de significación):

| | A7h | A8 | A8 − A7h (emparejado) |
|---|---|---|---|
| consultas por vida · retraso mediana · p95 | oráculo, 1 tic | **3,28 · 94 tics · 140** | |
| planes traducidos · intraducibles · callan | | 239 · **16 (6,3 % de 256)** · 1 | |
| pasaban al pedir · pasan al llegar · **rechazadas al llegar** | | 109 · 89 · **59 (54 % de las que pasaban)** | |
| aceptados en la fase 5 · sostenidos hasta el fin de fase | 128 · 25 | **58 · 8** | −1,6 (p < 0,001) · −0,45 (p 0,008) |
| cumplidas «por fin de fase» (registro literal) | 0 | 0 | |
| tics ardiendo en la fase 5 · % dentro | 116,6 · 44,1 | 177,5 · 30,2 | +64 (p 0,015) · −14 (p 0,03) |
| planes enviados al hermano · recibidos · los dos con plan vivo a la vez | | 92 · 75 · 11 de 38 partidas | |
| **aceptaciones falsas** (`confianza`: d_real > d_proyectada) | **185 / 245 planes = 75,5 %**; 305 / 477 puntos = 63,9 %; dif. mediana +0,084 | **64 / 87 = 73,6 %**; 95 / 131 puntos = 72,5 %; +0,120 | |
| aceptaciones falsas (`malestar26`, vida sentida − imaginada) | (no hay registro en A7h) | 83 / 128 tramos; +0,082 | |
| pasos perdidos, fases 5-7 | 26 / 10.860 (0,24 %) | **6 / 8.826 (0,07 %)**; 0 en tics de consulta | −0,5 (p 0,06) |
| muertes por anillo · rival · supervivientes | 31 · 15 · 30 | 37 · 12 · 21 | +0,18 (p 0,37) · −0,08 · −0,18 (p 0,29) |

Los 6 pasos perdidos de A8 en las fases 5-7: 4 en el tic de llegada de una respuesta con su encargo de juicio
y 2 en encargos de reevaluación; ninguno en un tic de consulta o encargo del razonador (`P6_27_serie.json`).

**Lo que dicen las medidas.** (1) La mesa acertó: el reloj le quita al razonador los consejos buenos. Pasan
al pedir 109 planes; llegan 94 tics después y la puerta rechaza 59 de ellos con el estado de la llegada;
quedan 58 aceptados en la fase 5 (A7h, con el oráculo en un tic: 128) y 8 sostenidos (25). (2) Con la mitad
de los planes, A8 arde como A4 (−10 tics, dentro del ruido) y 43 más que A7h; en la fase 5, 64 más que A7h
(p 0,015) y está dentro el 30 % del tiempo contra el 44 %. (3) Las aceptaciones falsas no distinguen a los
consejeros: en tres de cada cuatro planes aceptados lo vivido es peor que lo imaginado, con el oráculo
(75,5 %) y con el razonador (73,6 %); la diferencia mediana es pequeña y positiva en los dos (+0,08 y +0,12).
Es la medida de las aceptaciones falsas de la serie y el primer diario del siete: lo que la puerta imagina
al aceptar es sistemáticamente mejor que lo que el cuerpo vive. (4) La pareja habla: 92 planes enviados en
lugar de un E2, 75 recibidos (82 %), y en 11 de 38 partidas los dos hermanos tuvieron plan vivo a la vez.
(5) A8 llega menos al aviso 5 (66 de 76) que A7h (77 de 80): el cuerpo con el razonador muere antes más veces;
no se sella y queda anotado.

## 4 · EL SELLO, CONTRASTADO (`SELLO_P6_27.md`, md5 `021e011ba62e28d9bd6e78fd837c013e`)

| | predicción (sellada tras el humo) | medido | veredicto |
|---|---|---|---|
| **principal** · A8 − A4, unilateral | < 0 y p < 0,05; mesa: «menor o nulo» que A7h | −9,9; p 0,35 | **no alcanzada** (dirección sin prueba; la mesa acertó) |
| A8 − A7h | entre 0 y +40 | +43,1 (p 0,08) | en la dirección, algo más |
| consultas por vida | 2-4 | 3,28 | sí |
| retraso | mediana 80-130, p95 < 200 | 94 · 140 | sí |
| rechazadas al llegar | un cuarto a la mitad de las que pasaban | 54 % | algo más |
| aceptados fase 5 · cumplidas fin de fase | mitad a tres cuartos de 128 · pocas | 58 (45 %) · 0 (sostenidos 8) | algo menos · sí |
| enviados/recibidos · los dos con plan vivo | la mayoría · < un cuarto de las partidas | 82 % · 29 % | sí · algo más |
| aceptaciones falsas | > la mitad; A7h parecido | 73,6 % y 75,5 % | sí |
| intraducibles | < 5 % | 6,3 % | algo más |
| pasos perdidos 5-7 | 0 en consulta; ≤ A7h | 0; 0,07 % contra 0,24 % | sí |
| gasto | 3,71 USD estimados; falla si > 8 | 4,59 (1,24×; la partida costó 0,082, no 0,065) | sí |

## 5 · DECLARACIONES Y ARCHIVOS

- Dos vidas de la serie sin diario (pods borrados por la plataforma antes de recoger nada); sus partidas
  costaron y cuentan en el gasto; 78 diarios y zips (2,9 GB) y los 8 del humo, fuera de git, con md5 en el
  manifiesto. Las respuestas crudas del razonador van dentro de los diarios.
- Un cambio en `policy_pareja26.py` (P6-26): el proceso juez se inyecta en el constructor (`hilo=`), para que
  A8 use el de P6-27 sin arrancar el de P6-26; ninguna otra línea cambia. `mide_P6_26.py` lee también
  `resumen27`.
- El registro literal «cumplida por fin de fase» da 0 en los dos brazos; la cifra de planes sostenidos
  hasta el fin de fase es la de `mide_campo` (P6-23: cumplida por fin de fase o plan vivo al aviso
  siguiente), 8 contra 25.
- Regla de push aplicada (CLAUDE.md): tras el commit local y `copia_taller.py` limpio, push a gemv-coworld
  (paintball) y gemv-paper6 (main); los hashes remotos van en el acta.

| archivo | qué es |
|---|---|
| `puerta_proceso_P6_27.py`, `policy_pareja27.py` | el arreglo: encargo ligero por tic, memoria espejo, consulta ligera |
| `humo_red_P6_27.py` → `P6_27_banco_arreglo.json` | los humos (mock, reloj, llamada real) y el banco del arreglo (replay a reloj) |
| `Dockerfile.pareja27`, `lanza_P6_27.py`, `P6_27_brazos.json`, `P627_t*_*.json` | la imagen, el lanzador (humo + 2 tandas), la política subida, las 42 partidas |
| `mide_P6_27.py` → `P6_27_humo.json`, `P6_27_serie.json`, `P6_27_falsas_A7h.json` | consultas, retrasos, rechazos a la llegada, mensajes, aceptaciones falsas (A8 y oráculo), pasos perdidos atribuidos |
| `mide_campo_P6_27.py` → `P6_27_campo.json` | la medida principal y las secundarias emparejadas, 40 semillas, tres brazos |
| `mide_pasos_P6_22.py` → `P6_27_pasos_humo.json`, `P6_27_pasos_serie.json` | pasos perdidos por fase |
| `sello_P6_27.py` → `SELLO_P6_27.md`, `P6_27_sello.json` | el sello, con los md5 de todo el código que corre en la imagen y de lo que mide |

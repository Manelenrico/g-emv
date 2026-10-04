# P6-28 · Preguntar con adelanto: el banco no pasa el criterio, y se para

*28-sep-2026. Gasto por bolsas: **consola de Anthropic 1,096 USD de 3** (251 llamadas a Haiku 4.5 con la clave
de `cantera/paper5/.env`, gasto por `usage`; saldo no visible desde aquí); **créditos de la plataforma 0 de 8**
(ninguna partida: el humo y la serie no se lanzaron; la imagen A9 se construyó pero no se subió). `motor/model.py`
= `1e511978c251130e95169ebf8443efa1` al principio y al final; los 202 congelados del cinco y los 32 del seis: 0
alterados. La clave no se imprimió ni se escribió. Lo nuevo, en archivos aparte y declarado: `prevision_P6_28.py`,
`puerta_proceso_P6_28.py`, `policy_pareja28.py`, `humo_red_P6_28.py`, `Dockerfile.pareja28`, `lanza_P6_28.py`,
`banco_P6_28.py` → `P6_28_banco_consultas.json`, `P6_28_banco_planes.json`, `P6_28_banco_juicios.json`,
`P6_28_banco.json`, `P6_28_crudas_adelanto.jsonl` (fuera de git, md5 en el manifiesto); `sello_P6_28_banco.py` →
`SELLO_P6_28_banco.md` (md5 `665cedc6ad2dd444739f7c8368b06061`, cerrado antes de la primera llamada) y
`P6_28_sello_banco.json`. Ningún número se escribió antes de calcularlo. Sin propuestas de diseño.*

---

## 0 · LA RESPUESTA EN UNA LÍNEA

**Con la escena prevista para el tic de llegada (Δ = 94 tics, el retraso mediano de P6-27), los planes de Haiku
pasan la puerta6 a la llegada en el 33,5 % de las 251 consultas reales de A8; los planes originales, sin adelanto,
en el 36,7 % sobre las mismas instantáneas: −3,2 puntos (McNemar p 0,28). El criterio del encargo pedía +10: no
se cumple, así que PARO: ni humo ni serie.** La previsión en sí es buena (error de 2 casillas de mediana, p90 7,
vida prevista igual a la real de mediana) y el plan parte de donde el cuerpo estará; lo que no cambia es el
juicio de la puerta, que rechaza por exposición y alcance a los rivales, no por dónde está el cuerpo.

## 1 · QUÉ SE CONSTRUYÓ (A9) Y CÓMO SE MIDIÓ

**A9** (`policy_pareja28.py`, `puerta_proceso_P6_28.py`, `prevision_P6_28.py`): A8 (P6-27) con un cambio en la
consulta. En el proceso juez, antes de escribir la escena, el cuerpo imagina sus propios pasos durante Δ tics
desde el estado espejo de la consulta con la imaginación honesta de puerta6 (`puerta6_P6_15.rollout`: su decisor
tic a tic; el anillo del calendario, que quema; los rivales quietos donde se ven o se cuentan; el hermano en su
último parte; el suelo conocido menos lo que coge). La escena es la de A8 sobre la observación prevista (anillo y
rivales a t+Δ, lo reciente real hasta t), precedida de una frase que dice que es la situación prevista para el tic
de llegada, y el plan parte de la casilla prevista. Todo lo demás, idéntico a A8 (juicio con la instantánea de
LLEGADA, ir y quedarse, compromiso6b, V2, cuenta justa, plan al hermano, memoria espejo). La previsión corre en el
proceso juez: 259 ms de mediana en el banco (Mac), 60-68 ms en el humo mock; nada en el hilo principal.

**El banco** (`banco_P6_28.py`): las 256 consultas reales de A8 con respuesta en la serie de P6-27 (239 con plan,
16 intraducibles, 1 calla). (a) Con la réplica en seco (el alma espejo de A7h recibiendo el diario, molde de
P6-25) se reconstruyeron la instantánea del tic de consulta y la del tic real de llegada de cada una (256 de 256),
con lo que el razonador leía. (b) Desde la de consulta se hizo la previsión a t+Δ y se pidió a Haiku un plan (251
de 256: en 5 la previsión reventó con un `KeyError`, declarado). (c) Los dos planes, el del adelanto y el original
de A8 (la respuesta grabada, traducida como en el campo), se juzgaron con la puerta6 real sobre la instantánea de
llegada. La reconstrucción reproduce el veredicto de campo del plan original en 246 de 251 (98 %).

## 2 · RESULTADOS (`P6_28_banco.json`)

| | con adelanto | sin adelanto (original de A8) |
|---|---|---|
| **pasan a la llegada** (de 251) | **84 = 33,5 %** | **92 = 36,7 %** |
| los dos · solo adelanto · solo original | 67 · 17 · 25 (McNemar p 0,28) | |
| sin plan | 17 (4 callan, 13 con formas vacías); intraducibles 0 | 13 |
| distancia del destino del plan a la casilla real de llegada (mediana) | 4 | 3 |
| fila que más pesó en contra (rechazados) | S-8-EXPOSICION 49, F-REENCUENTRO 18, F-4-ALCANCE 16, F-DANO 15 | |

**El error de la previsión** (casilla prevista contra la real a la llegada, Chebyshev): mediana **2**, p90 **7**,
máximo 12; exacta en 25 de 251, a 2 o menos en 135; la vida prevista coincide con la real (mediana de la
diferencia 0). Y la tasa de paso por error:

| error de la previsión | n | pasan con adelanto | pasan sin adelanto |
|---|---|---|---|
| 0 casillas | 25 | 44,0 % | 44,0 % |
| 1-2 | 110 | 36,4 % | 43,6 % |
| 3-5 | 77 | 28,6 % | 29,9 % |
| 6 o más | 39 | 28,2 % | 25,6 % |

**Lo que dicen las medidas.** (1) La previsión acierta la casilla a dos de distancia en la mitad de las
consultas y la vida casi siempre, y aun así no ayuda: cuando acierta del todo (0 casillas), pasan exactamente
los mismos 11 de 25 con y sin adelanto. (2) La puerta no rechaza por dónde está el cuerpo sino por lo que ve
alrededor (exposición, rivales al alcance, reencuentro), y eso la previsión lo deja igual por regla de honestidad
(rivales quietos). (3) El plan con adelanto apunta algo más lejos de donde el cuerpo acaba estando (4 contra 3
casillas): la previsión desplaza el origen del plan sin ganar nada en el destino. (4) Lo que el reloj quita
(P6-27: 59 de 109 rechazados a la llegada) no se recupera contando mejor dónde estará el cuerpo, porque el
rechazo depende de la escena alrededor, que a 94 tics ya es otra.

## 3 · EL SELLO DEL BANCO, CONTRASTADO (`SELLO_P6_28_banco.md`, md5 `665cedc6ad2dd444739f7c8368b06061`)

| | predicción | medido | veredicto |
|---|---|---|---|
| Δ | 94 tics (retraso mediano de P6-27, 239 respuestas) | 94 | fijado |
| **criterio**: adelanto − original ≥ +10 puntos a la llegada | entre +10 y +25 («el banco mejora con claridad») | **−3,2** | **falla: PARA** |
| error de la previsión | mediana ≤ 3, p90 ≤ 8 | 2 · 7 | acierta |
| intraducibles | ≈ 6 % | 0 (17 sin plan: 4 callan, 13 vacías) | mejor que lo previsto |
| gasto de consola | 1,0-1,5 USD | 1,096 | acierta |

La mesa predijo que el banco mejoraría con claridad: no. Su reserva («la previsión no sabe qué harán los
rivales») es exactamente donde se queda: la previsión sabe dónde estará el cuerpo y no lo que la puerta mira.

## 4 · LO QUE NO SE HIZO, Y ARCHIVOS

No se subió la política A9, no se jugó el humo ni la serie (créditos de la plataforma: 0 gastados). El sello de la
serie no se escribe (no hay serie que sellar). La imagen `gemv-anima:pareja28` existe en el Mac con su humo mock
dentro (`OK humo A9`), por si Manel decide otra cosa; los humos nativos de A9 (mock y reloj, sin llamadas) pasan.

| archivo | qué es |
|---|---|
| `prevision_P6_28.py` | la previsión a t+Δ con la imaginación honesta de puerta6, la frase y la escena prevista |
| `puerta_proceso_P6_28.py`, `policy_pareja28.py` | el brazo A9 (la previsión en el proceso juez; el error de la previsión a la llegada) |
| `humo_red_P6_28.py`, `Dockerfile.pareja28`, `lanza_P6_28.py` | su humo (mock y reloj pasados en nativo; mock dentro de la imagen), la imagen, el lanzador (no usado) |
| `banco_P6_28.py` → `P6_28_banco_consultas.json`, `P6_28_banco_planes.json`, `P6_28_banco_juicios.json`, `P6_28_banco.json` | el banco: instantáneas, escenas previstas y llamadas, juicios a la llegada, medidas |
| `sello_P6_28_banco.py` → `SELLO_P6_28_banco.md`, `P6_28_sello_banco.json` | el sello del banco |
| `P6_28_crudas_adelanto.jsonl` | las 251 respuestas crudas (fuera de git, md5 en el manifiesto); las instantáneas, en el borrador de la sesión |

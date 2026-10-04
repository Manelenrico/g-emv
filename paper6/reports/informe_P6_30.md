# P6-30 · La fuga en los bancos del seis: inventario, arreglo en el banco, repetición sin fuga y la tabla que importa

*3-oct-2026. Coste cero (plataforma 0; consola 0; ninguna llamada al modelo). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y
al acabar; `CONGELADO.md`, `CONGELADO_P6.md`, el cuerpo y los borradores sin tocar. Sello: `SELLO_P6_30.md`, commit 0b72aa5, md5 `3a872e34cd53b1e672cf88394b612fab`,
antes de calcular. Todo lo nuevo vive en `cantera/paper6/P6_30/` (copias de los bancos con tres cambios declarados y sus salidas); los JSON
originales de `cantera/paper6/` no se tocan. Este informe lo escribe `escribe_informe_P6_30.py` leyendo los JSON viejos y los nuevos.*

## Sección 1 · Inventario: qué banco corrió varias vidas por proceso

La fuga (P7-3): `policy_pareja._envuelve(alma)` (`cantera/paper6/policy_pareja.py:99-134`) apila una capa por vida sobre `D.candidatos` y
nadie la quita; cada capa veta los candidatos contra los rivales contados por su criatura, congelados al acabar su vida. Solo muerde
donde un mismo proceso replica **varias vidas con `_envuelve`** (`AlmaPareja` / `AlmaPareja23`, que lo llama en su constructor,
`policy_pareja23.py:278`). Revisados todos los `.py` de `cantera/paper6` desde P6-14 (`grep` de `AlmaPareja()`, `_envuelve(`, `Pool(`,
`subprocess`):

| banco | replica el cuerpo | cómo corre las vidas | varias vidas por proceso | afectado |
|---|---|---|---|---|
| P6-14 `banco_P6_14.py` | sí | `corre_P6_14.py:22`: un `subprocess` por vida | no | no |
| P6-15 `banco_P6_15.py` | sí | `corre_P6_15.py:22`: un `subprocess` por vida | no | no |
| P6-18 `banco_P6_18.py` | sí | `corre_P6_18.py:16`: un `subprocess` por vida | no | no |
| P6-19 `banco_P6_19.py` | sí | `corre_P6_19.py:28`: un `subprocess` por vida | no | no |
| P6-22 `mide_bucle_P6_22.py`, `mide_gil_P6_22.py` | sí | un proceso, una vida (argumentos de línea de órdenes) | no | no |
| P6-23 `compromiso6c`, `atribuye_pasos` | no (lee diarios) | – | – | no |
| P6-25 `escenas_P6_25.py` | sí (`AlmaPareja23`, `:282-284`) | `Pool(hilos)` sin `maxtasksperchild` (`:391`), 66 vidas en 4 procesos | **sí** | **sí** |
| P6-25 `juez_P6_25.py`, `razonador_P6_25.py` | no: el juez levanta UN alma espejo por proceso (`:103-111`) y no replica vidas | `Pool(hilos)` | no (una alma por proceso) | solo por sus entradas: las instantáneas de `escenas_P6_25` |
| P6-26 `banco_P6_26.py` | no (juez sobre instantáneas) | `Pool(hilos)` (`:84`) | no | solo por sus entradas (instantáneas de P6-25) |
| P6-27 | campo (una vida por proceso) + `mide_campo` sobre diarios | – | – | no |
| P6-28 `banco_P6_28.py --instantaneas` | sí (`AlmaPareja23`, `:64-65`) | `Pool(hilos)` sin `maxtasksperchild` (`:120`) | **sí** | **sí** |
| P6-29 `mide_P6_29.py` | sí (`AlmaPareja`, `:224`) | `Pool(hilos)` sin `maxtasksperchild` (`:371`), 240 vidas en 4 procesos | **sí** | **sí** |
| humos (`humo_red_*`) | sí, una vida | un proceso | no | no |

La lista de P7-3 se confirma (P6-25, P6-28, P6-29) y se precisa: P6-26 no replica el cuerpo, pero juzga sobre las instantáneas que
produjo la réplica de P6-25, así que se repite también. Las instantáneas de P6-25 y P6-28 estaban en el scratch de aquella sesión y ya no
existen: para volver a juzgar hay que volver a replicar.

## Sección 2 · El arreglo, solo en el banco, y la fontanería

Copias en `P6_30/` de `escenas_P6_25.py`, `juez_P6_25.py`, `mide_P6_25.py`, `banco_P6_26.py`, `banco_P6_28.py` y `mide_P6_29.py` con tres
cambios declarados en su primera línea: la raíz un nivel más arriba, `cantera/paper6` en el camino de importación, y **un proceso por
vida** (`maxtasksperchild=1`) en los tres pools que replican el cuerpo. El cuerpo no se toca. En la copia de `banco_P6_28.py` hay dos pasos
nuevos sin llamadas: `--reenlaza` (las instantáneas nuevas en la copia de los planes guardados, por id) y `--prevision` (rehace la escena
prevista y compara su md5 con la que se mandó al modelo).

**Fontanería.** Réplica contra diario, tic a tic, en `mide_P6_29` (`fidelidad` = la elección de la réplica contra `elegido_cuerpo`, lo que
el cuerpo eligió antes de que el compromiso lo cambiara):

| brazo | con fuga (P6-29 publicado) | sin fuga (P6-30) |
|---|---|---|
| A7h | 1.068.541 iguales, 599 distintas (99,944 %) | 1.068.981 iguales, 159 distintas (99,985 %) |
| A8 | 969.279 iguales, 561 distintas (99,942 %) | 969.731 iguales, 109 distintas (99,989 %) |
| A4 | 1.005.891 iguales, 1.385 distintas (99,863 %) | 1.007.274 iguales, 2 distintas (100,000 %) |

Réplica de P6-25 (`repro`: la elección de la réplica contra `elegido` **ejecutado**, que en A7h incluye los pasos del compromiso, así que
"difiere" no es solo infidelidad): con fuga 892.484 / 8.091; sin fuga 892.692 / 7.883.
Textos de las 200 escenas de P6-25 (lo que leyó el modelo) iguales en la réplica sin fuga: 239 de 240 (md5). Escenas previstas de
P6-28 (lo que leyó Haiku con adelanto) iguales: 249 de 256. Las respuestas del modelo son las guardadas; no se pidió ninguna nueva.
**Residuo sin fuga, replicado uno a uno** (`residuo_todo_P6_30.py`): 270 desacuerdos (A7h 159, A8 109, A4 2) de 3.046.256 tics. En 262 de 270 la elección del diario es el candidato del plan (`_FM_ir_*`), que la réplica no tiene porque no lleva compromiso, y las d de todos los candidatos propios son iguales en el diario y en la réplica (diferencia < 1e-6): no es infidelidad del cuerpo, es que cuando el candidato del plan ganaba, la radiografía lo apuntó también como elección propia (o no apuntó `elegido_cuerpo`). En 4 el único candidato que difiere es un `usar_*` (el veto del canal, `decisor_zs.py:83-102`, que en la réplica se abre o cierra un tic antes porque `action_result` llega con la observación siguiente). Quedan **4** de otra clase, con alguna d distinta: 7h_20679832/11 t 1518 (diario –, réplica move_SE); 7h_20679832/11 t 1694 (diario –, réplica move_SE); A4_21622393/10 t 1832 (diario –, réplica move_W); A4_21622393/10 t 2041 (diario –, réplica paso_NE). La fontanería no es exacta tic a tic: lo es salvo esos 4 tics de 3.046.256 (0,00013 %) y los 4 del canal; se dice y se sigue, porque no tocan ninguna cifra de las secciones 6 y 7 (la deformación se mide sobre instantes con plan vivo y piernas listas, y el canal no es un instante de plan).

## Sección 3 · Repetición sin fuga: los bancos

**P6-25** (`escenas_P6_25.py` → juez × 6 → `mide_P6_25.py`; 66 vidas de A7h replicadas, 240 escenas, 1.640 instantáneas nuevas; respuestas del
modelo: las guardadas en `P6_25_planes_*.json`). Cifras que cambian en `P6_25_medidas.json` (fuera de `repro`, tiempos y gasto): ninguna.
El único texto que cambia (`P624_t2_A7h_24764263_10_14591`) gana la línea "atacar al del asiento 4": en la réplica con fuga ese ataque
estaba vetado por un rival contado en una vida anterior del mismo proceso. Las respuestas guardadas valen para 239 de 240 escenas; en
la que cambia se juzga la respuesta guardada sobre la instantánea nueva, y queda declarado.

**P6-26** (`banco_P6_26.py`, el barrido de todos los destinos sobre las instantáneas nuevas; sin modelo). Cifras que cambian en
`P6_26_banco.json`: ninguna.

**P6-28** (`banco_P6_28.py --instantaneas` → `--reenlaza` → `--prevision` → `--juzga` → `--mide`; 70 vidas de A8 replicadas, 256 consultas
con sus dos instantáneas; respuestas de Haiku: las guardadas en `P6_28_banco_planes.json`). La escena prevista rehecha desde la instantánea
nueva es idéntica (md5) a la que leyó Haiku en 249 de 256 consultas; distinta en 2 (P627_t1_A8_22041309_10_12535, P627_t2_A8_25916282_11_14694), cuyas respuestas guardadas
son a un texto que ya no es el mismo (no se piden de nuevo: son las que faltan); 5 dan error en la previsión, como en P6-28 (251 medidas en los dos).
Cifras que cambian en `P6_28_banco.json`: ninguna.

**P6-29** (`mide_P6_29.py`, 240 vidas: A7h 80, A8 78, A4 80). Cifras que cambian en `P6_29_medidas.json` (sin tiempos ni fidelidad): `A7h/2_deformacion/por_instante_que_difiere/media` 0.16756 → 0.17145; `A7h/2_deformacion/por_instante_que_difiere/p90` 0.28579 → 0.2955; `A7h/2_deformacion/por_instante_sujeta/media` 0.17437 → 0.17862; `A7h/2_deformacion/por_instante_sujeta/mediana` 0.15409 → 0.1557; `A7h/2_deformacion/por_instante_sujeta/p90` 0.29109 → 0.30277; `A7h/2_deformacion/acumulada_por_plan/media` 6.2522 → 6.3973; `A7h/2_deformacion/acumulada_por_plan/p90` 17.0104 → 18.9406; `A7h/2_deformacion/acumulada_todos_los_tics/media` 6.2522 → 6.3973; `A7h/2_deformacion/acumulada_todos_los_tics/p90` 17.0104 → 18.9406; `A7h/2_deformacion/por_100_tics_vivo/media` 3.326 → 3.3631; `A7h/2_deformacion/por_100_tics_vivo/p90` 9.9412 → 10.432; `A7h/3_soltados_contra_cumplidos/soltados/acumulada/media` 2.4231 → 2.4224; `A7h/3_soltados_contra_cumplidos/soltados/por_100_tics/media` 2.1103 → 2.1097; `A7h/3_soltados_contra_cumplidos/cumplidos/acumulada/media` 29.897 → 30.9204; `A7h/3_soltados_contra_cumplidos/cumplidos/acumulada/mediana` 19.9723 → 20.7072; `A7h/3_soltados_contra_cumplidos/cumplidos/por_100_tics/media` 11.1348 → 11.3992; `A7h/3_soltados_contra_cumplidos/cumplidos/por_100_tics/mediana` 8.6763 → 9.6377; `A7h/4_compensa/spearman_defo_ahorro` -0.0659 → 0.0351; `A7h/4_compensa/ahorro_por_unidad_de_deformacion/media` 3.3 → 2.8; `A7h/4_compensa/ahorro_por_unidad_de_deformacion/p90` 11.9 → 8.8; `A7h/4_compensa/ahorro_por_unidad_de_deformacion/max` 20.8 → 20.7; `A7h/4_compensa/todos_los_planes_con_A4/spearman` 0.1447 → 0.1474; `A7h/5_huella/tras/iguales` 42045 → 42049; `A7h/5_huella/tras/pct` 99.74 → 99.75; `A7h/5_huella/antes/iguales` 48641 → 48751; `A7h/5_huella/antes/pct` 99.67 → 99.9; `A7h/5_huella/A4_tras/iguales` 30411 → 30768; `A7h/5_huella/A4_tras/pct` 98.84 → 100.0; `A7h/5_huella/A4_tras_listos/iguales` 7903 → 7939; `A7h/5_huella/A4_tras_listos/pct` 99.55 → 100.0; `A7h/5_huella/A4_antes/iguales` 36533 → 36995; `A7h/5_huella/A4_antes/pct` 98.75 → 100.0; `A8/fm_gana_en_replica` 2804 → 2803; `A8/2_deformacion/por_instante_obedece/media` 0.09599 → 0.09601; `A8/2_deformacion/acumulada_por_plan/p90` 3.9316 → 3.9369; `A8/2_deformacion/acumulada_todos_los_tics/p90` 3.9316 → 3.9369; `A8/3_soltados_contra_cumplidos/cumplidos/acumulada/media` 2.1141 → 2.1145; `A8/3_soltados_contra_cumplidos/cumplidos/por_100_tics/media` 1.9851 → 1.9854; `A8/5_huella/tras/iguales` 16980 → 17006; `A8/5_huella/tras/pct` 99.7 → 99.85; `A8/5_huella/tras_listos/iguales` 2630 → 2637; `A8/5_huella/tras_listos/pct` 98.8 → 99.06; `A8/5_huella/antes/iguales` 19381 → 19387; `A8/5_huella/antes/pct` 99.9 → 99.93; `A8/5_huella/A4_tras/iguales` 11977 → 12004; `A8/5_huella/A4_tras/pct` 99.78 → 100.0; `A8/5_huella/A4_tras_listos/iguales` 3265 → 3275; `A8/5_huella/A4_tras_listos/pct` 99.69 → 100.0; `A8/5_huella/A4_antes/iguales` 15199 → 15309; `A8/5_huella/A4_antes/pct` 99.28 → 100.0.
Lo que se mueve es pequeño y donde se esperaba: la deformación por instante y acumulada de A7h sube unas centésimas (los ataques que la
fuga vetaba vuelven a estar entre los candidatos propios y cambian la d mínima en algunos instantes), el Spearman de A7h pasa de −0,07 a
+0,04 (sigue siendo ninguna relación) y la huella de A4 pasa a 100 %: la "infidelidad" de A4 era toda la fuga.

## Sección 4 · La tabla que importa: cada cifra de las secciones 6 y 7 que viene de estos bancos

| sección | frase del texto | valor citado (apéndice) | valor sin fuga | ¿cambia la frase? | fuente |
|---|---|---|---|---|---|
| 6 | la puerta acepta cerca de la mitad, en proporción parecida con reglas o lenguaje | oráculo 102 de 200; Haiku 98 de 191; Sonnet 100 de 183; 51,0 / 49,0 / 50,0 % | oráculo 102 de 200; Haiku 98 de 191; Sonnet 100 de 183; 51.0 / 49.0 / 50.0 % | no | informe_P6_25:66-69; viejo = oráculo 102 de 200; Haiku 98 de 191; Sonnet 100 de 183; 51.0 / 49.0 / 50.0 % |
| 6 | mismo veredicto en casi nueve de cada diez | 172-174 de 200 (McNemar p 0,57 y 0,85) | haiku: 172 de 200 (p 0.5716); sonnet: 174 de 200 (p 0.845) | no | informe_P6_25; viejo = haiku: 172 de 200 (p 0.5716); sonnet: 174 de 200 (p 0.845) |
| 6 | al llegar, sigue pasando la mitad / cuatro de cada diez | 51,8 % (Haiku), 41,0 % (Sonnet) | haiku: 43 de 83 (51.8 %); sonnet: 32 de 78 (41.0 %) | no | informe_P6_25; viejo = haiku: 43 de 83 (51.8 %); sonnet: 32 de 78 (41.0 %) |
| 6 | el segundo intento pasa pocas veces, el tercero casi nunca | 2.º 8,1 / 14,3 %; 3.º 0 / 4,2 % | haiku: 2.º 3 de 37 (8.1 %), 3.º 0 de 34 (0.0 %); sonnet: 2.º 4 de 28 (14.3 %), 3.º 1 de 24 (4.2 %) | no | informe_P6_25; viejo = haiku: 2.º 3 de 37 (8.1 %), 3.º 0 de 34 (0.0 %); sonnet: 2.º 4 de 28 (14.3 %), 3.º 1 de 24 (4.2 %) |
| 6 | coinciden en la zona casi siempre; aceptan los dos una de cada cinco | 82,5 / 100 %; 20,0 / 17,5 % | haiku: zona 82.5 %, los dos 8 de 40 (20.0 %); sonnet: zona 100.0 %, los dos 7 de 40 (17.5 %) | no | informe_P6_25; viejo = haiku: zona 82.5 %, los dos 8 de 40 (20.0 %); sonnet: zona 100.0 %, los dos 7 de 40 (17.5 %) |
| 6 | en ocho de cada diez escenas rechazadas no había ningún plan de ir y quedarse aceptable | con plan que pasa: 21 de 93 (22,6 %); 13 de 83 (15,7 %) | haiku: 21 de 93 (22.6 %); sonnet: 13 de 83 (15.7 %) | no | informe_P6_26:42-43; viejo = haiku: 21 de 93 (22.6 %); sonnet: 13 de 83 (15.7 %) |
| 6 | con adelanto, la puerta no acepta más; algo menos | 33,5 contra 36,7 % (251; McNemar p 0,28) | 33.5 contra 36.7 % (251; p 0.28) | no | informe_P6_28; viejo = 33.5 contra 36.7 % (251; p 0.28) |
| 6 | la previsión se equivoca en un par de casillas | mediana 2, p90 7 | mediana 2, p90 7 | no | informe_P6_28; viejo = mediana 2, p90 7 |
| 7 | hace otra cosa en ocho de cada diez instantes | 83,9 % (A7h), 82,4 % (A8) | 83.93 % (A7h), 82.37 % (A8) | no | informe_P6_29; viejo = 83.93 % (A7h), 82.37 % (A8) |
| 7 | nueve de cada diez, sujeciones; tres de cada cuatro, para ir a por algo | 92 %; 76 % | sujeta 91.6 %; hacia algo 75.9 % | no | informe_P6_29:66-67; viejo = sujeta 91.6 %; hacia algo 75.9 % |
| 7 | quedarse cuesta más del doble que andar | 0,154 contra 0,065 por instante | 0.156 contra 0.065 | no | informe_P6_29; viejo = 0.154 contra 0.065 |
| 7 | el que más, cientos de veces el típico | acumulada por plan: mediana 0,28 / 0,27, p90 17 / 3,9, máximo 102 | mediana 0.28 / 0.27, p90 18.9 / 3.9, máximo 102 | no | informe_P6_29; viejo = mediana 0.28 / 0.27, p90 17.0 / 3.9, máximo 102 |
| 7 | los cumplidos acumulan unas cien veces más que los soltados | 20,0 contra 0,18 | 20.71 contra 0.18 | no | informe_P6_29; viejo = 19.97 contra 0.18 |
| 7 | caen por la puerta o por la vida, ninguno por lo aguantado | 132 por reevaluación, 76 por la vida | 132 por reevaluación, 76 por la vida | no | informe_P6_29; viejo = 132 por reevaluación, 76 por la vida |
| 7 | algo menos ardiendo de media que el cuerpo sin consejero; nada en el típico; sin relación | media +42 / +15, mediana 0; Spearman -0,07 / +0,18 | media +41.9 / +15.2, mediana 0 / 0; Spearman +0.04 / +0.18 | no | informe_P6_29; viejo = media +41.9 / +15.2, mediana 0 / 0; Spearman -0.07 / +0.18 |
| 7 | ocho segundos después, decide como solo | 200 tics; 99,7 % (A4 98,8 %) | 99.75 % (A4 100.0 %) | no | informe_P6_29; viejo = 99.74 % (A4 98.84 %) |
| 7 | figura 5: el plan que más dobló: 184 instantes queriendo ir; se quedó 183, anduvo 1; acumulada 102 | plan 13 de 20994019 | instantes 184, sujeta 183, obedece 1, acumulada 102.0 | no | P6_29_planes.json; viejo = instantes 184, sujeta 183, obedece 1, acumulada 102.0 |

Criterio de "cambia la frase": el que la frase admite (una proporción verbal como "cerca de la mitad" se da por cambiada si sale de 40-60 %,
"ocho de cada diez" si sale de 70-90 %, "casi nueve de cada diez" si sale de 80-95 %, "más del doble" si deja de serlo, "cien veces" si sale
de 30-300, etc.; cada criterio está en `escribe_informe_P6_30.py`, fila a fila). Las filas con "ver texto" se comparan a ojo en la sección 3.
No vienen de estos bancos y no cambian: las latencias del modelo (3,7 y 8,1 s), los intraducibles (1,5 / 7,5 %: traducción de respuestas
guardadas), todo lo de P6-27 (campo), la figura 4 y las medias de instantes ardiendo.

**Sello.** **Acierta**: ninguna cifra de las secciones 6 y 7 cambia la frase que la cuenta.

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P6_30.md` | la predicción, md5, commit 0b72aa5 |
| `P6_30/*.py` | copias de los seis bancos con los tres cambios declarados; `cadena_P6_30.sh` el orden de ejecución |
| `P6_30/P6_25_*.json`, `P6_26_banco*.json`, `P6_28_*.json`, `P6_29_*.json` | las salidas sin fuga (mismos nombres que las viejas, en su carpeta) |
| `P6_30/_P6_25_snaps`, `_P6_28_snaps`, `*.log` | instantáneas y registros, fuera de git |
| `escribe_informe_P6_30.py`, `informe_P6_30.md` | este informe |

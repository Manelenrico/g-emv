# P7-5 · El cuerpo que descubre: construido, probado en banco y en humo de tres días

*3-oct-2026. Coste: **créditos de la plataforma** 0,2660 USD en 3 partidas (por día: 1: 0,1084, 2: 0,0476, 3: 0,1099); **consola de Anthropic 0 USD**
(ninguna llamada). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; congelados y cuerpo sin tocar: todo lo nuevo son
archivos `_P7` (`cuaderno_P7.py`, `descubre_P7.py`, `policy_pareja_P7.py`, `banco_P7_5.py`, `huella_P7_5.py`, `lanza_P7_5.py`, `humo_P7_5.py`,
`gif_P7_5.py`, `Dockerfile.pareja_P7`). Una vida por proceso en el banco (subproceso por vida) y en el campo (un contenedor por criatura);
la memoria viaja solo en el archivo del cuaderno.*

## Sección 1 · Lo construido, con las tres correcciones de la mesa

| pieza | archivo | dónde engancha (sin tocar el congelado) |
|---|---|---|
| A, cuaderno | `cuaderno_P7.py` | se lee al conocer el asiento (envoltorio de `AlmaPareja.decidir`, primera llamada) y se escribe al acabar (`policy_pareja_P7.run`, tras `P11.run`); huella por dominio (cuerpo, recursos, vínculo): efecto e importancia con signo; creencia = media ponderada de los efectos con un recuerdo neutro de peso 1 que no se apaga (corrección 3); los vividos se apagan con 0,95 por día; intensidad = 1 + min(1, suma de |importancias| / 1,5); la cuenta de usos no se olvida |
| A, la ventana | `descubre_P7.ventana` | del tic en que aparece el canal del botiquín al tic en que desaparece; lo esperado sin la cosa resta solo el daño de causas conocidas (corrección 1): anillo estando fuera del círculo según `mundo.anillo_en`, y golpes de rivales a la vista y en alcance de su arma (catálogo; mano vacía = 1); importancia por dominio = malestar del eje al cerrar menos al abrir (corrección 2), ejes F, R, S de la radiografía del presente |
| B, imaginación | envoltorio de `D.candidatos` | `receta["heal"]` de `usar_botiquin` = creencia del cuerpo en la situación de ahora; "no sé" = 0 |
| C, ganas | `A.ACOPIO_M`, `A.W_TARGET` y envoltorio de `A.riqueza_W` | escala k = creencia máxima / cura del catálogo: R-ACOPIO = 0,18 k; el botiquín en W cuenta k; `W_TARGET` = 2 + k; "no sé" = 0 |
| D, novedad | envoltorio de `A.appraise` y de `D._promesa` | fila apetitiva R-NOVEDAD: 0,18 × calma × 0,5^usos × forma (1 − d/24 a la vista o recordado; 1 en el zurrón; 1,5 en la foto que lo usa); calma = 1 − máx(alcance, agresor, hermano amenaza, hermano golpe, anticipación del fuego) |
| brazos | `GEMV_P7`, `GEMV_P7_SABE`, `GEMV_P7_CUADERNO`, `GEMV_P7_BORRADO`, `GEMV_P7_NOVEDAD` | SUELO = P7 solo; BORRADO = cuaderno sin leer + novedad; APRENDE = cuaderno que viaja + novedad; TECHO = SABE (todo pasa tal cual) |

**Corrección 1 sobre el cálculo en seco de P7-4** (`huella_P7_5.py` → `P7_5_huella.json`): con la regla de causas conocidas, de los 180 usos con
ventana cambian **3** (todos cancelados; diferencia -4,0 a -2,0 hp: el veneno, que el cuerpo no sabe explicar, se queda en el efecto). Daño
conocido en las 180 ventanas: anillo fuera 1.062,7 hp, rival visto en alcance 414,9 hp; no conocido: poison 10,0 hp.

## Sección 2 · F1: con todo apagado y con TECHO, la variante reproduce los diarios de A4

Réplica de los 80 diarios de A4 (`banco_P7_5.py --f1`, un subproceso por vida), la elección de la réplica contra `RADIOGRAFIA.elegido` en
cada tic vivo:

| brazo | vidas | tics iguales | distintos | los distintos |
|---|---:|---:|---:|---|
| apagado | 80 | 1.007.274 | 2 | A4_21622393/10 t 1832 (move_SW / move_W); A4_21622393/10 t 2041 (move_NW / paso_NE) |
| TECHO | 80 | 1.007.274 | 2 | A4_21622393/10 t 1832 (move_SW / move_W); A4_21622393/10 t 2041 (move_NW / paso_NE) |

Los dos tics distintos son los mismos dos de P6-30 (`informe_P6_30.md`, sección 2: la vida 21622393/10, tics 1832 y 2041, con alguna d
distinta en el propio A4 sin fuga). **F1 pasa**: los enganches con TECHO son neutros al bit y con todo apagado la política es A4.

## Sección 3 · F2: el cuaderno cargado a mano, la imaginación y las ganas

`banco_P7_5.py --f2`: por asiento, el cuaderno se carga con los recuerdos del diario de P7-1 de los días 1-20 (efectos del cuerpo con la
regla de causas conocidas, recursos y vínculo del cálculo en seco; la importancia sin signo, que solo pesa) y se replican tres vidas de los
días 21-40 con APRENDE, cada una leyendo lo que dejó la anterior. En la réplica el mundo es el del diario: los usos del botiquín que abren
ventana son los del diario, y la imaginación de la réplica se compara en los tics en que ella también tenía el candidato.

| asiento | cuaderno cargado (recuerdos; creencia del cuerpo dentro / fuera) |
|---|---|
| 10 | 28 recuerdos, 28 usos; dentro 23,51 / fuera 0,02 |
| 11 | 35 recuerdos, 35 usos; dentro 20,41 / fuera 8,60 |

| día | vida | heal imaginado = creencia vigente en su situación (usos comparados) | k = creencia máx / 50 | R-ACOPIO en el primer tic vivo = 0,18 k | huellas nuevas | cuaderno al acabar |
|---|---|---|---|---|---:|---|
| 21 | A4_24450076/10 | ninguno comparable: la réplica no tuvo el candidato en los tics de uso del diario | 0,4703 (esperado 0,4703) | 0,08465 (esperado 0,08465) sí | 3 | día 21, usos 32, dentro 19,89 / fuera 0,00 |
| 22 | A4_24554805/10 | sí, 1 de 1; p. ej. t 10759 dentro 19,89 | 0,3977 (esperado 0,3977) | 0,07159 (esperado 0,07159) sí | 2 | día 22, usos 34, dentro 24,71 / fuera 0,00 |
| 24 | A4_24764263/10 | sí, 3 de 3; p. ej. t 1865 dentro 24,71 | 0,4943 (esperado 0,4943) | 0,08897 (esperado 0,08897) sí | 3 | día 23, usos 37, dentro 20,91 / fuera 0,00 |
| 21 | A4_24450076/11 | sí, 8 de 8; p. ej. t 12649 fuera 8,60 | 0,4082 (esperado 0,4082) | 0,07348 (esperado 0,07348) sí | 7 | día 21, usos 43, dentro 20,32 / fuera 5,31 |
| 22 | A4_24554805/11 | sí, 2 de 2; p. ej. t 10503 dentro 20,32 | 0,4064 (esperado 0,4064) | 0,07314 (esperado 0,07314) sí | 3 | día 22, usos 46, dentro 18,58 / fuera 5,29 |
| 23 | A4_24659534/11 | ninguno comparable: la réplica no tuvo el candidato en los tics de uso del diario | 0,3715 (esperado 0,3715) | 0,06688 (esperado 0,06688) sí | 8 | día 23, usos 54, dentro 20,01 / fuera 3,89 |

**F2 pasa**: en todos los usos comparables la receta de `usar_botiquin` lleva la creencia del cuaderno en su situación, las ganas salen
con la escala acordada (R-ACOPIO = 0,18 k en el primer tic vivo, k = creencia máxima / 50, `W_TARGET` = 2 + k) y cada vida lee el
cuaderno que dejó la anterior (el día avanza y los usos se acumulan). Fuente: `P7_5_F2.json`.

## Sección 4 · F3: el humo de tres días en la plataforma (brazo APRENDE, las dos criaturas)

Semillas: día 1: 26544656, día 2: 26649385, día 3: 26754114 (la sucesión de semillas_S2, paso 104729, continuada tras la última de P6-24; ninguna usada antes).
Cada día se horneó la imagen con el cuaderno del día anterior (`Dockerfile.pareja_P7`; versiones subidas: día 1: gemv-p7-aprende:v1 (d2c9a97e…), día 2: gemv-p7-aprende:v2 (ee54c5d8…), día 3: gemv-p7-aprende:v3 (511eca43…)), una partida entera
(mundo 0.1.19, roster lento v2, 18.240 tics), y al acabar se extrajo el registro `P7_cuaderno` de fin de cada diario para el día siguiente.
El campo no tiene canal de entrada: el viaje del cuaderno es ese horneado.

**Día 1** (semilla 26544656, estado completed, coste 0,1084 USD de plataforma).

| criatura | vivo (tics) · puesto | primer botiquín visto (tic) | tics con novedad > 0 | se acerca por novedad | coge | usa (tic, situación, heal imaginado) | cuaderno leído al arrancar | cuaderno al acabar |
|---|---|---:|---:|---:|---:|---|---|---|
| 10 | 12.601 · 7 | 570 | 12.013 | 36 | 0 | ninguno | no (día 0; dentro – / fuera –, usos –) | 0 recuerdos, usos None; dentro – / fuera –; recursos – / –; vínculo – / – |
| 11 | 11.175 · 12 | 526 | 10.649 | 381 | 0 | ninguno | no (día 0; dentro – / fuera –, usos –) | 0 recuerdos, usos None; dentro – / fuera –; recursos – / –; vínculo – / – |

**Día 2** (semilla 26649385, estado completed, coste 0,0476 USD de plataforma).

| criatura | vivo (tics) · puesto | primer botiquín visto (tic) | tics con novedad > 0 | se acerca por novedad | coge | usa (tic, situación, heal imaginado) | cuaderno leído al arrancar | cuaderno al acabar |
|---|---|---:|---:|---:|---:|---|---|---|
| 10 | 13.094 · 5 | 570 | 12.524 | 108 | 0 | ninguno | no (día 0; dentro – / fuera –, usos –) | 0 recuerdos, usos None; dentro – / fuera –; recursos – / –; vínculo – / – |
| 11 | 14.329 · 3 | 526 | 13.803 | 48 | 0 | ninguno | no (día 0; dentro – / fuera –, usos –) | 0 recuerdos, usos None; dentro – / fuera –; recursos – / –; vínculo – / – |

**Día 3** (semilla 26754114, estado completed, coste 0,1099 USD de plataforma).

| criatura | vivo (tics) · puesto | primer botiquín visto (tic) | tics con novedad > 0 | se acerca por novedad | coge | usa (tic, situación, heal imaginado) | cuaderno leído al arrancar | cuaderno al acabar |
|---|---|---:|---:|---:|---:|---|---|---|
| 10 | 14.953 · 1 | 581 | 14.372 | 47 | 2 | 13588 dentro 0,00 | sí (día 2; dentro – / fuera –, usos –) | 1 recuerdos, usos 1; dentro 13,83 / fuera –; recursos -0,53 / –; vínculo 0,00 / – |
| 11 | 14.953 · 2 | 559 | 14.394 | 516 | 0 | ninguno | sí (día 2; dentro – / fuera –, usos –) | 0 recuerdos, usos None; dentro – / fuera –; recursos – / –; vínculo – / – |

**Lectura del humo.** Tics a una casilla o menos de un botiquín, por día y asiento: día 1 asiento 10: 375 (con ranura libre 13, con `coger` entre los candidatos 2, elegido `coger` 2, `coger` escondido por mochila llena 56, solo `noop` entre los candidatos 257); día 1 asiento 11: 4.293 (con ranura libre 117, con `coger` entre los candidatos 96, elegido `coger` 1, `coger` escondido por mochila llena 594, solo `noop` entre los candidatos 3.812); día 2 asiento 10: 6.693 (con ranura libre 55, con `coger` entre los candidatos 22, elegido `coger` 0, `coger` escondido por mochila llena 256, solo `noop` entre los candidatos 970); día 2 asiento 11: 6.089 (con ranura libre 55, con `coger` entre los candidatos 22, elegido `coger` 0, `coger` escondido por mochila llena 278, solo `noop` entre los candidatos 407); día 3 asiento 10: 1.771 (con ranura libre 1.363, con `coger` entre los candidatos 272, elegido `coger` 6, `coger` escondido por mochila llena 259, solo `noop` entre los candidatos 769); día 3 asiento 11: 6.199 (con ranura libre 376, con `coger` entre los candidatos 221, elegido `coger` 0, `coger` escondido por mochila llena 788, solo `noop` entre los candidatos 5.415). Cogidas: día 3 asiento 10: 2. Usos: día 3 asiento 10. tic 13.588. dentro. imaginó 0.0; la huella que dejó: efecto cuerpo +26.0, recursos -1, vínculo +0.0 (daño conocido 0.0 de 0.0); importancia cuerpo -0.193, recursos +0.091, vínculo -0.011; intensidad 1.1971. **¿El día 2 lee lo del día 1 y cambia su imaginación?** El día 1 no dejó recuerdos (ningún uso), así que el día 2 leyó un cuaderno vacío (y, por el fallo de lanzamiento, sin archivo: `leído: no`) y el día 3 leyó el del día 2 (`leído: sí`, día 2, cero recuerdos): la imaginación siguió en "no sé" (heal 0) hasta el primer uso del día 3, que dejó la primera creencia (asiento 10, dentro: cuerpo 13,8); un día 4 la leería y la pondría en la receta de `usar_botiquin`, que es lo que F2 comprobó en banco. **Por qué casi nunca coge.** Dos causas, leídas en los diarios: (1) el zurrón de dos ranuras va lleno de lo que coge antes (dardos y cerbatana, flechas y cuchillos, ración y cuchillos), y con el zurrón lleno `coger` no existe (`arreglos_P6_8b.py:85-101` lo esconde porque la previsión no cambia la mochila); no hay candidato de soltar algo para coger lo nuevo (P7-3, sección 3). (2) Con ranura libre, la criatura se queda en la casilla contigua: la fila de novedad tal como la fijó el plan vale casi lo mismo al lado del objeto (g = 1 − d/24 ≈ 0,94 a una casilla) que llevándolo (g = 1), así que ni el último paso ni `coger` ganan nada frente a quedarse quieto. Comprobado en banco sobre el diario del día 2 (asiento 10, tics 603-606: junto al botiquín con el zurrón vacío, único candidato `noop`, novedad M 0,169 con g 0,94). Tras el humo se topó la forma en el suelo a 0,5 (`SUELO_MAX`, declarado, no jugado): la réplica del mismo diario cambia 35 de 12.613 decisiones y sigue sin dar el último paso: la pendiente en el suelo necesita otra forma, y eso es un número de método de la mesa (sección 6). La fontanería del campo sí está: la réplica en banco del diario del día 2 (asiento 10) con la política del siete reproduce el campo decisión a decisión (12.613 de 12.613).

GIF del primer uso de cada criatura (datos crudos del diario, `gif_P7_5.py`): `P7_5_dia1_acercamiento_10.gif`, `P7_5_dia1_acercamiento_11.gif`, `P7_5_dia3_acercamiento_11.gif`, `P7_5_dia3_uso_10.gif` (no hubo ningún uso en los tres días: el GIF es del primer acercamiento, el primer tic a una casilla o menos de un botiquín).

## Sección 5 · F4: lo que costaría la serie

Créditos de la plataforma gastados en el humo: 0,2660 USD en 3 partidas (media 0,0887, de 0,0476 a 0,1099; subir imágenes no gasta créditos). Una serie de 20 días con los cuatro brazos y dos órdenes de semillas son 160 partidas: a la media del humo, **14,19 USD** (entre 7,62 y 17,59 con el mínimo y el máximo del humo). Con la media de las 20 partidas enteras de A4 de P6-24 (0,0855 USD por partida), 13,68 USD. Aparte, APRENDE y BORRADO necesitan rehacer y subir la imagen cada día (el cuaderno viaja horneado): 2 brazos × 20 días × 2 órdenes = 80 subidas, sin créditos pero con tiempo de máquina (unos 55 s cada una en este Mac). Consola de Anthropic: 0.

## Sección 6 · Lo que queda para la mesa

1. La forma de la novedad en el suelo: con g = 1 − d/24 (y aun topada a 0,5) el último paso hacia el objeto no paga; hace falta una
   pendiente que crezca cerca del objeto (por ejemplo, que el suelo valga 0 a más de unas casillas y suba hasta 0,5 al llegar), o que la
   promesa de `ir_objeto` cuente la ganancia de cogerlo, no solo la de acercarse. Número de método.
2. El zurrón lleno: sin un candidato de soltar para coger lo nuevo, la novedad no puede probar nada cuando las dos ranuras van ocupadas.
   Es la misma falta que P7-3 encontró para el arco. Decisión de diseño.
3. El viaje del cuaderno en el campo: hoy va horneado en la imagen (una subida por día y brazo). El registro de fin del cuaderno se escribe
   ahora antes de la subida del artefacto (corregido tras el día 1); los cuadernos de los días 1 y 2 se reconstruyeron desde sus diarios
   con la misma regla (`reconstruye_cuaderno_P7_5.py`) y son idénticos a lo que el cuerpo habría escrito (cero recuerdos, cero usos).
4. El día 2 se lanzó por error con una imagen sin cuaderno (la cadena no esperó a la reconstrucción): como el día 1 no dejó recuerdos, el
   contenido leído habría sido el mismo (vacío); se declara y se cuenta su coste.

## Archivos

| archivo | qué es |
|---|---|
| `cuaderno_P7.py`, `descubre_P7.py`, `policy_pareja_P7.py`, `Dockerfile.pareja_P7` | el cuerpo que descubre: cuaderno, enganches, política y la imagen |
| `banco_P7_5.py`, `P7_5_F1.json`, `P7_5_F2.json` | F1 y F2 (un subproceso por vida) |
| `huella_P7_5.py`, `P7_5_huella.json` | la corrección 1 sobre el cálculo en seco |
| `lanza_P7_5.py`, `P7_5_brazos.json`, `P7_5_dia*_peticion.json`, `P7_5_dia*_resultado.json`, `P7_5_dia*_cuaderno_*.json`, `cuadernos_humo/` | el humo: imágenes, peticiones, resultados con el coste, los cuadernos de cada día |
| `humo_P7_5.py`, `P7_5_humo.json`, `gif_P7_5.py`, `P7_5_dia*_*.gif` | la lectura del humo y los GIF (los GIF quedan en local, fuera de git, como los PDF) |
| `escribe_informe_P7_5.py`, `informe_P7_5.md` | este informe |

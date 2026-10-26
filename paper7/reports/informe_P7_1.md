# P7-1 · El botiquín y el arco por dentro, y el diario de tres columnas sobre lo ya vivido

*3-oct-2026. Coste cero: sin partidas, sin llamadas (plataforma 0; consola 0). Solo lectura y medida sobre los mismos 80 diarios A4 del
seis que P7-0 (40 semillas: P611_t1, P611_t2, P624_t1; 2 asientos por partida). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al
empezar y al acabar; congelados sin tocar; el cuerpo no se toca. Scripts: `cantera/paper7/mide_P7_1.py` (definiciones en su cabecera,
líneas 1-26; escribe `P7_1_medidas.json` y el diario `P7_1_diario.json`) y `escribe_informe_P7_1.py` (este informe, cifras leídas de los
JSON). "Dentro del círculo" = distancia euclídea al centro ≤ radio del mismo tic: de 835 golpes de zona en los 80 diarios,
830 caen fuera por esta regla (`R["zona_vs_dano"]`); los 5 restantes son del borde (radio no entero durante el encogimiento).*

## Sección 1 · El botiquín por dentro (195 usos confirmados; 59 completados, 121 cancelados, 15 sin cerrar porque la vida acaba antes)

Nota sobre P7-0: allí "completado" era solo "el botiquín sale del zurrón antes de `done_tick`+1" y dio 64. Aquí se exige además que no
hubiera daño antes de `done_tick` (el daño corta el canal). Los 5 casos que cambian de columna son usos cortados por el anillo en los que
el cuerpo **soltó** el botiquín después del corte (`drop/ok` en los cinco, mirado tic a tic: por ejemplo `P611_t1_A4_21098748/10`, uso en
12.889, corte en 12.913, `drop` en 12.929), sin curarse (cura real 0,12, 0,12, -0,44, -0,44, 0,12).

**¿Inmoviliza?** No. Durante el canal el cuerpo se mueve y el canal sigue: posiciones distintas mientras el canal vive (hasta el corte en
los cancelados, hasta `done_tick` en los completados): 1 → 12, 2 → 73, 3 → 51, 4 → 17, 5 → 23, 6 → 4. De los 59 completados,
57 se movieron durante el canal y 2 no; de los 121 cancelados, 111 y 10. Intenciones emitidas
dentro del canal (acción/resultado): move/ok 439, attack/no_ammo 123, pickup/no_target 93, attack/ok 48, move/blocked 35, pickup/ok 22, move/no_ammo 14, move/no_target 9, drop/ok 6, drop/no_target 3, drop/blocked 1. Ni moverse ni atacar cortan
el canal; lo que lo corta es recibir daño (abajo). Fuente: `mide_P7_1.py` (`_pos`, `_intenciones`), `P7_1_medidas.json["resumen"]["botiquin"]`.

**Cada uso, por situación** (cerrados: 180):

| | completados | cancelados |
|---|---:|---:|
| fuera del círculo al usar | 7 | 89 |
| dentro del círculo al usar | 52 | 32 |
| fase 0 | 9 | 2 |
| fase 2 (encogiendo) | 1 | 0 |
| fase 3 | 7 | 8 |
| fase 3 (encogiendo) | 1 | 6 |
| fase 4 | 12 | 20 |
| fase 4 (encogiendo) | 4 | 1 |
| fase 5 | 8 | 58 |
| fase 5 (encogiendo) | 6 | 21 |
| fase 6 | 9 | 4 |
| fase 7 | 2 | 0 |
| fase 7 (encogiendo) | 0 | 1 |

Vida al usar: mediana 54 (p10 15, p90 88). Rivales a la vista al usar: 0 → 56, 1 → 52, 2 → 40, 3+ → 47; distancia al más cercano
cuando hay alguno: mediana 4,5 casillas (p10 1,0, p90 8,0).

**De dónde vino el daño que cortó el canal** (primer tic con daño después del `use`; 121 cortes, a 21 / 10 / 24 tics del `use`): anillo
92, rivales 27 (asientos P12 1, P13 1, P14 17, P3 1, P6 2, P7 1, P8 3, P9 1), veneno 2. Fuera del círculo casi todo es anillo
(85 de 89); dentro, casi todo rivales (23 de 32) y 7 veces el anillo que encoge y deja fuera al cuerpo. El fuego del anillo golpea cada 24
tics y el canal dura 48: fuera del círculo y quieto, el canal no puede acabar nunca.

**¿Había una casilla sin daño alcanzable antes del corte?** (solo cortes por anillo; pasos = casillas hasta el borde, 11 tics por casilla
a velocidad 5, `mundo.py:216-217`): 42 sí, 43 no, 7 estaba dentro al usar (el círculo se movió). Pasos hasta el borde: mediana
2 (p10 1, p90 4). De los 7 completados fuera, 6 acaban dentro: el cuerpo entró andando con el canal abierto.

**Tiempo por vida intentando curarse en el fuego** (tics dentro de un canal de botiquín estando fuera del círculo, hasta el corte):
mediana 0, p10 0, p90 106 tics; total 2.097 tics (87 s) en 28 de 80 vidas.

**Muertes por anillo** (la vida acaba y el último daño es del anillo): 40 de 80 vidas (razones de final: eliminated 64, match_over 8, winner 8). Con
intentos de botiquín en los últimos 10 segundos (240 tics): **9 de 40**; intentos en esas 40: mediana 0, p90 5, total 36.
Solo se describe; no se reabre el seis.

## Sección 2 · El arco y la cerbatana por dentro

| | arco | cerbatana |
|---|---:|---:|
| ataques | 1.521 | 749 |
| resultado `ok` / `no_ammo` | 128 / 1.393 | 47 / 702 |
| golpes (daño hecho) | 75 | 33 |
| `no_ammo` sin munición en la mochila / con munición sin cargar | 1.393 / 0 | 702 / 0 |
| `ok` con munición / sin munición | 128 / 0 | 47 / 0 |
| `no_ammo` con munición a la vista | 898 (64,5 %) | 598 (85,2 %) |
| `no_ammo` con munición contada por el hermano (E2 ≤ 86 tics) | 327 (23,5 %) | 141 (20,1 %) |
| qué hacía el rival atacado (`no_ammo`): me pegaba / se acercaba / nada | 1.097 / 104 / 192 | 564 / 50 / 88 |
| el rival era mi agresor (honor) / defensa del hermano | 1.115 / 557 | 571 / 251 |
| distancia al rival (mediana / p10 / p90) | 2,0 / 1,0 / 5,7 | 2,0 / 1,0 / 4,2 |
| `no_ammo` dentro del círculo / fuera | 1.294 / 99 | 702 / 0 |
| vidas con algún `no_ammo` | 10 | 5 |
| tics por vida en ataques que no hacen nada (mediana / p10 / p90; 80 vidas) | 0 / 0 / 36 | 0 / 0 / 0 |
| fracción de la vida, en las vidas que atacan con el arma (mediana / p90) | 0,00 % / 1,00 % | 0,00 % / 2,00 % |

Lectura: la munición en la mochila separa el resultado **sin una excepción**: todos los `no_ammo` son con 0 flechas (o dardos) en
mano y zurrón, y todos los `ok` con alguna. "Sin cargar" no existe: no hay ataque fallido con munición a bordo. En la mayoría de los
fallos había munición a la vista (`ve_items`) y el rival estaba pegándome a 1-2 casillas. Cada ataque fallido es un tic de decisión;
el tiempo perdido es pequeño en fracción de vida pero se concentra en la pelea. Fuente: `mide_P7_1.py` (`ataques_arco_cerbatana`),
`P7_1_medidas.json["resumen"]["arco"]`; el asiento atacado sale de `RADIOGRAFIA.honor.objetivo`.

## Sección 3 · El diario de tres columnas sobre lo ya vivido (`cantera/paper7/P7_1_diario.json`)

Una fila por uso de botiquín (195) y por ataque con arco o cerbatana (2270). Cada fila lleva `vida` (carpeta/asiento), `t`, y las
tres columnas:

| columna | botiquín | arco / cerbatana | exacto o inferido |
|---|---|---|---|
| **situación** (solo lo que el cuerpo ya percibe en t) | dentro/fuera y distancia al borde, vida, daño recibido en los 24 y 120 tics anteriores, rivales a ≤ 5 casillas y distancia al más cercano, fase y si encoge | dentro/fuera, vida, daño en los 24 anteriores, rivales a ≤ 5, distancia al rival atacado, munición en la mochila, a la vista, contada por el hermano, qué hacía el rival, fase | exacto: todo sale del registro `tick` de t (`pos`, `zona`, `hp`, `damage_taken`, `ve_agentes`, `ve_items`, `hand`, `pack`); "contada por el hermano" se infiere del `chat` (E2 del hermano, ≤ 86 tics, letra `a`/`f` en la sección I); "qué hacía" se infiere de `damage_taken` (120 tics) y de su distancia en t frente a t−24 |
| **imaginado** (lo que la previsión del cuerpo esperaba) | hp esperado = min(100, hp + 50) (`decisor_zs.py:824`, `heal` del catálogo) | daño esperado = 14 (arco) / 4 (cerbatana), daño del catálogo (`decisor_zs.py:852-856`) | exacto: es la fórmula del cuerpo aplicada al hp y al catálogo del mismo tic |
| **lo que pasó** | completado / cancelado / sin cerrar; hp al final de la ventana; cura real; daño en la ventana; tic y fuentes del corte; si se movió; si acabó dentro | `action_result` (`ok` / `no_ammo`); golpe; daño hecho | exacto: `hp`, `n` del pack, `effects`, `action_result`, `damage_dealt`; inferido: cura real = hp_fin − hp + daño en la ventana (el diario no da la cura directa); cancelado = el `n` no baja en `done_tick`+1; golpe = `damage_dealt` sube en t+1 (no dice a quién) |

## Sección 4 · Lo que habría que aprender: lo imaginado contra lo que pasó, por situación (sin ninguna regla de aprendizaje)

**Botiquín** (180 filas cerradas). Lo imaginado es siempre "curo 50 (o hasta 100)". Lo que pasó, por cada variable percibida:

| variable | valor | completados | cancelados | acierta la creencia |
|---|---|---:|---:|---:|
| dentro / fuera del círculo | dentro | 52 | 32 | 61,9 % |
| dentro / fuera del círculo | fuera | 7 | 89 | 7,3 % |
| daño en los 24 tics anteriores | con dano 24 | 18 | 98 | 15,5 % |
| daño en los 24 tics anteriores | sin dano 24 | 41 | 23 | 64,1 % |
| daño en los 120 tics anteriores | con dano 120 | 41 | 111 | 27,0 % |
| daño en los 120 tics anteriores | sin dano 120 | 18 | 10 | 64,3 % |
| rival a ≤ 5 casillas | rival a 5 | 39 | 39 | 50,0 % |
| rival a ≤ 5 casillas | sin rival a 5 | 20 | 82 | 19,6 % |
| vida | hp<50 | 21 | 47 | 30,9 % |
| vida | hp>=50 | 38 | 74 | 33,9 % |
| fase del anillo | 0 | 9 | 2 | 81,8 % |
| fase del anillo | 2 | 1 | 0 | 100,0 % |
| fase del anillo | 3 | 8 | 14 | 36,4 % |
| fase del anillo | 4 | 16 | 21 | 43,2 % |
| fase del anillo | 5 | 14 | 79 | 15,1 % |
| fase del anillo | 6 | 9 | 4 | 69,2 % |
| fase del anillo | 7 | 2 | 1 | 66,7 % |
| dentro/fuera × daño 24 | dentro / con dano 24 | 13 | 20 | 39,4 % |
| dentro/fuera × daño 24 | dentro / sin dano 24 | 39 | 12 | 76,5 % |
| dentro/fuera × daño 24 | fuera / con dano 24 | 5 | 78 | 6,0 % |
| dentro/fuera × daño 24 | fuera / sin dano 24 | 2 | 11 | 15,4 % |
| dentro/fuera × rival a 5 | dentro / rival a 5 | 39 | 28 | 58,2 % |
| dentro/fuera × rival a 5 | dentro / sin rival a 5 | 13 | 4 | 76,5 % |
| dentro/fuera × rival a 5 | fuera / rival a 5 | 0 | 11 | 0,0 % |
| dentro/fuera × rival a 5 | fuera / sin rival a 5 | 7 | 78 | 8,2 % |
| dentro/fuera × se movió en el canal (no la percibe antes: es lo que hizo) | dentro / quieto | 2 | 6 | 25,0 % |
| dentro/fuera × se movió en el canal (no la percibe antes: es lo que hizo) | dentro / se movio | 50 | 26 | 65,8 % |
| dentro/fuera × se movió en el canal (no la percibe antes: es lo que hizo) | fuera / quieto | 0 | 4 | 0,0 % |
| dentro/fuera × se movió en el canal (no la percibe antes: es lo que hizo) | fuera / se movio | 7 | 85 | 7,6 % |
| dentro, sin rival a 5 y sin daño 24 | dentro, sin rival a 5, sin dano 24 | 11 | 3 | 78,6 % |
| dentro, sin rival a 5 y sin daño 24 | resto | 48 | 118 | 28,9 % |

Cura real (hp al final − hp al usar + daño en la ventana): dentro, mediana 5,5 (p10 -0,2, p90 50,0); fuera, mediana 0,1 (p10 -0,4, p90 0,6).

Qué separa y qué no: **ninguna variable percibida separa limpiamente.** La que más, "dentro o fuera del círculo": fuera, la creencia
falla en 92,7 % de los usos; dentro, acierta en 61,9 %. Los 7 aciertos fuera son casi todos cuerpos que entraron andando con el canal abierto
(6 acaban dentro), y los 32 fallos dentro son golpes de rivales (23) o el anillo que encoge (7). "Daño en los 24 tics
anteriores" separa peor que dentro/fuera (con daño: 84,5 % fallos; sin daño: 64,1 % aciertos). El cruce "dentro y sin rival a 5" acierta en
76,5 % (17 casos) y "dentro, sin rival a 5 y sin daño 24" en 78,6 % (14 casos), pero son pocos. La variable que
sí separa es la que el cuerpo **no percibe al decidir**: si recibirá daño en los 48 tics siguientes. Fuera del círculo eso es seguro
(el anillo pega cada 24 tics) salvo que entre andando; dentro, depende de los rivales.

**Arco y cerbatana.** Lo imaginado es siempre "pego 14 (arco) / 4 (cerbatana)". Lo que pasó:

| arma | variable | valor | `ok` | `no_ammo` | acierta la creencia |
|---|---|---|---:|---:|---:|
| arco | munición en la mochila | con municion | 128 | 0 | 100,0 % |
| arco | munición en la mochila | sin municion | 0 | 1393 | 0,0 % |
| arco | munición a la vista | municion a la vista | 32 | 898 | 3,4 % |
| arco | munición a la vista | sin municion a la vista | 96 | 495 | 16,2 % |
| arco | contada por el hermano | contada por el hermano | 19 | 327 | 5,5 % |
| arco | contada por el hermano | no contada | 109 | 1066 | 9,3 % |
| arco | qué hacía el rival | me pegaba | 81 | 1097 | 6,9 % |
| arco | qué hacía el rival | nada | 25 | 192 | 11,5 % |
| arco | qué hacía el rival | se acercaba | 22 | 104 | 17,5 % |
| arco | rival a ≤ 5 | rival a 5 | 115 | 1369 | 7,7 % |
| arco | rival a ≤ 5 | sin rival a 5 | 13 | 24 | 35,1 % |
| arco | daño 24 anteriores | con dano 24 | 47 | 635 | 6,9 % |
| arco | daño 24 anteriores | sin dano 24 | 81 | 758 | 9,7 % |
| arco | dentro / fuera | dentro | 124 | 1294 | 8,7 % |
| arco | dentro / fuera | fuera | 4 | 99 | 3,9 % |
| cerbatana | munición en la mochila | con municion | 47 | 0 | 100,0 % |
| cerbatana | munición en la mochila | sin municion | 0 | 702 | 0,0 % |
| cerbatana | munición a la vista | municion a la vista | 20 | 598 | 3,2 % |
| cerbatana | munición a la vista | sin municion a la vista | 27 | 104 | 20,6 % |
| cerbatana | contada por el hermano | contada por el hermano | 8 | 141 | 5,4 % |
| cerbatana | contada por el hermano | no contada | 39 | 561 | 6,5 % |
| cerbatana | qué hacía el rival | me pegaba | 19 | 564 | 3,3 % |
| cerbatana | qué hacía el rival | nada | 19 | 88 | 17,8 % |
| cerbatana | qué hacía el rival | se acercaba | 9 | 50 | 15,3 % |
| cerbatana | rival a ≤ 5 | rival a 5 | 46 | 664 | 6,5 % |
| cerbatana | rival a ≤ 5 | sin rival a 5 | 1 | 38 | 2,6 % |
| cerbatana | daño 24 anteriores | con dano 24 | 11 | 274 | 3,9 % |
| cerbatana | daño 24 anteriores | sin dano 24 | 36 | 428 | 7,8 % |
| cerbatana | dentro / fuera | dentro | 47 | 702 | 6,3 % |

Daño hecho cuando el ataque sale (`ok`): arco mediana 14 (p10 0, p90 14; 128 ataques, 1.050 hp en total); cerbatana mediana 2 (p10 0, p90 4; 47 ataques, 86 hp).

Qué separa: **la munición en la mochila separa limpiamente**, con cero excepciones en 2.270 ataques: con munición el ataque sale
(y hace daño o no según el blanco), sin munición nunca. Es una variable que el cuerpo ya percibe (`pack`, `hand.n`) y que ya usa para
valorar el arma en W (`appraisal_zs_v42_exp.py:739-744`), pero no para decidir atacar (`decisor_zs.py:588-602`). Ninguna otra variable
separa: con munición a la vista o contada por el hermano la creencia falla igual.

## Sección 5 · Cuántas experiencias por día: filas de diario por criatura y vida (80 vidas; mediana / p10 / p90, total)

| objeto | situación | mediana / p10 / p90 por vida | total | vidas con ≥ 1 |
|---|---|---|---:|---:|
| botiquín | fuera del círculo | 0 / 0 / 5 | 107 | 28 |
| botiquín | dentro del círculo | 0 / 0 / 4 | 88 | 36 |
| botiquín | sin dano 24 | 0 / 0 / 2 | 66 | 36 |
| botiquín | con dano 24 | 0 / 0 / 5 | 129 | 37 |
| botiquín | todas | 1 / 0 / 8 | 195 | 47 |
| arco | con municion | 0 / 0 / 10 | 128 | 13 |
| arco | sin municion | 0 / 0 / 36 | 1393 | 10 |
| arco | todas | 0 / 0 / 47 | 1521 | 17 |
| cerbatana | con municion | 0 / 0 / 1 | 47 | 9 |
| cerbatana | sin municion | 0 / 0 / 0 | 702 | 5 |
| cerbatana | todas | 0 / 0 / 3 | 749 | 11 |

Fuente: `P7_1_medidas.json["resumen"]["filas_por_vida"]`; las 80 vidas cuentan, también las que no usan el objeto (de ahí las medianas 0).
La mayoría de las vidas no abre ninguna fila de arco o cerbatana; las que sí, abren muchas seguidas en una pelea (p90 47 filas de arco).

## Archivos

| archivo | qué es |
|---|---|
| `cantera/paper7/mide_P7_1.py` | la medida (definiciones en la cabecera); `mide_P7_1.log` su salida (fuera de git) |
| `cantera/paper7/P7_1_medidas.json` | por vida: usos de botiquín con su canal, ataques con arco y cerbatana; resumen por secciones |
| `cantera/paper7/P7_1_diario.json` | el diario de tres columnas: `botiquin` (195 filas), `arco_cerbatana` (2270 filas) |
| `cantera/paper7/escribe_informe_P7_1.py` | escribe este informe desde los JSON |
| `cantera/paper7/informe_P7_1.md` | este informe |

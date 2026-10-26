# P7-33 · La etapa de lo inútil: construir y probar

*9-oct-2026. Coste: plataforma 0,2740 USD (el humo, 3 partidas); consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; cuerpo y congelados sin tocar. Pieza nueva `nace_P7_33.py` (enganchada desde fuera tras descubre, pedir, nacer y P7-29; GEMV_P7_33, apagada por defecto), política `policy_pareja_P7_33.py`, banco `banco_P7_33.py` + `pruebas_P7_33.py`, imagen `Dockerfile.pareja_P7_33`, lanzador `lanza_P7_33.py`, lectura `analiza_P7_33.py`. Este informe lo escribe `escribe_informe_P7_33.py`. Ninguna cifra a mano.*

## Lo construido (diseño de Manel, 9-oct; sobre las piezas de P7-30)

1. **Nace sin saber nada de cuatro cosas.** Botiquín y ración, como en P7-23. Red y camuflaje: lo que el cuerpo sabía de ellos y se borra (archivo y línea): (a) su valor en la riqueza W, `gear_menor` = 0,25 por el camuflaje puesto y 0,25 por la red en mano o zurrón (`appraisal_zs_v42_exp.py:413, :761-769`) → 0,25 × k_camuflaje y 0,25 × k_red (envoltorio de `A.riqueza_W`); (b) los radios del camuflaje, CAMO_QUIETO = 4 y CAMO_MOVIENDO = 7, con los que S-8 EXPOSICIÓN deja de contar a los rivales lejanos (`:405-406, :1393-1411`) → 4 × k y 7 × k mientras se calculan las filas (k = 0: como sin camuflaje); (c) la promesa del camuflaje en el suelo (`decisor_zs.py:672-677`) sale de esas mismas filas, así que ya va escalada; la red no tiene promesa ni `empunar` (daño 0: `:731-745`, `:536-544`). Ganas: solo R-CARENCIA (`:1076`), que va por W. Regalo y pedido: el cuerpo no regala ni pide gear (nada que borrar; declarado). k de cada cosa de gear = ((1 − ignorancia) × creencia vivida en el cuerpo + ignorancia × esperanza de la otra cosa de gear) / hp_max; "no sé" → 0 (número de esta pieza, declarado: no hay cura de catálogo para el gear).
2. **Probar el camuflaje es ponérselo** (ventana de 10 s llevándolo puesto, o antes si se lo quita) y **probar la red es llevarla** (10 s en mochila o mano, o antes si la suelta o la lanza): huella por dominio (cuerpo = vida al cerrar − al abrir + daño conocido; recursos = unidades al cerrar − al abrir; vínculo = distancia a la hermana), foto emocional, contexto y acciones al abrir, más duración, si la ventana se completó y el contexto de peligro. Sin "al menos" (no hay cura que tope) y sin corte (la prueba acaba cuando acaba la ventana o se va la cosa); una prueba por cada vez que la cosa llega, no una cadena de ventanas mientras la sigue llevando (declarado). Si no cambió nada, el recuerdo dice "no hizo nada" (efecto 0).
3. **La curiosidad de la clase** para las cuatro: ignorancia × alivio (tenerla alivia la mitad: la red en zurrón o mano, el camuflaje en zurrón o puesto; probarla, el resto, por los recuerdos). `ir_curioso` va a la clase que más llama de las cuatro. La curiosidad del cuánto sigue siendo de los consumibles (la red y el camuflaje no se "usan"; declarado); la esperanza del botiquín y de la ración sigue saliendo solo de la otra cosa consumible.
4. **Oído y ley:** el cuerpo lee `event_warning` (inundación: rectángulo y plazo; tormenta de fuego: centro, radio y plazo) y mientras dura el evento esas casillas son no transitables en su mapa (`mundo.solido` envuelto; el campo geodésico cacheado se vacía al cambiar lo activo). En los tres brazos. `solido` también corta la línea de vista (`mundo.py:231-247`); declarado.
5. **Medida del contexto** de cada prueba de cada cosa (punto 8): calma, o peligro (rival a 4 casillas o menos, fuego, vida < 30), al abrir.

## F1 · Con todo apagado se reproducen los diarios de A4; con oído y ley en TECHO, qué cambia

`pruebas_P7_33.py --f1` sobre los 80 diarios de A4 (GEMV_P7_PIDE=0 como en P7-23/29) -> `P7_33_F1.json`:

| F1 | tics iguales · difieren | vidas con cambios | dónde cambian |
|---|---|---:|---|
| apagado | 1.007.274 · 2 | 1 | 21622393/10: 2 (t1832-2041, sin aviso) |
| TECHO con oido y ley | 1.007.078 · 198 | 6 | 20784561/10: 2 (t5089-5100, inundación anunciada [10, 22, 14, 26] tics 4400-5120); 20784561/11: 1 (t5094-5094, inundación anunciada [10, 22, 14, 26] tics 4400-5120); 21622393/10: 2 (t1832-2041, sin aviso); 21727122/10: 90 (t4402-5120, inundación anunciada [10, 22, 14, 26] tics 4400-5120); 21727122/11: 84 (t5041-12399, inundación anunciada [10, 22, 14, 26] tics 4400-5120); 25078450/11: 19 (t4409-5113, inundación anunciada [10, 22, 14, 26] tics 4400-5120) |

Los dos tics de `apagado` son los dos de siempre (P7-23, P7-29). Con el oído y la ley, los cambios caen en las vidas que oyeron un aviso de inundación: el mismo evento del mundo en todas ellas (rectángulo [10, 22]-[14, 26], tics 4.400-5.120): la ley hace que el cuerpo rodee el agua en vez de empujarla. Las vidas de las inundaciones de P7-30 (k = 184) y P7-24 (k = 159), TECHO, replicadas con la ley:

| vida de TECHO (inundación de su semilla) | tics iguales · difieren | cambios en la ventana del aviso (−120 a +60 tics) · fuera | primero → último | aviso |
|---|---|---|---|---|
| s1_d7_TECHO_39531052/10 | 14.129 · 1 | 0 · 1 | hacer_sitio_rations_por_first_aid→noop t12446 … t12446 | flood [10, 22, 14, 26] tics 4400-5120 |
| s1_d7_TECHO_39531052/11 | 14.184 · 0 | 0 · 0 | — | flood [10, 22, 14, 26] tics 4400-5120 |
| s2_d14_TECHO_39531052/10 | 12.527 · 1 | 0 · 1 | hacer_sitio_rations_por_first_aid→noop t2196 … t2196 | flood [10, 22, 14, 26] tics 4400-5120 |
| s2_d14_TECHO_39531052/11 | 10.867 · 1 | 0 · 1 | hacer_sitio_rations_por_first_aid→noop t1400 … t1400 | flood [10, 22, 14, 26] tics 4400-5120 |
| s1_d5_TECHO_36912827/10 | 9.366 · 702 | 702 · 0 | ir_objeto→ir_botin t4419 … t5120 | flood [10, 22, 14, 26] tics 4400-5120 |
| s1_d5_TECHO_36912827/11 | 11.064 · 1.008 | 710 · 298 | ir_objeto→ir_botin t4401 … t10511 | flood [10, 22, 14, 26] tics 4400-5120 |
| s2_d16_TECHO_36912827/10 | 11.881 · 143 | 143 · 0 | ir_objeto→move_SE t4410 … t5071 | flood [10, 22, 14, 26] tics 4400-5120 |
| s2_d16_TECHO_36912827/11 | 14.112 · 0 | 0 · 0 | — | flood [10, 22, 14, 26] tics 4400-5120 |

Lectura. En k = 159 (P7-24 s1 d5 y s2 d16) los cambios empiezan en los tics 4.401-4.419 (con el agua) y, en las vidas que estaban contra el agua, siguen hasta el 5.120 (la réplica sigue el diario en lazo abierto: cuando la ley elige otro camino, el diario y la réplica ya no coinciden hasta que la escena vuelve a ser la misma). En k = 184 (P7-30 s1 d7 y s2 d14) las vidas de TECHO no estaban contra el agua (la que chocaba era el asiento 10 de BORRADO y de APRENDE, P7-31) y el único tic que cambia en 3 de las 4 está fuera de la ventana y es un empate `hacer_sitio` ↔ `noop` (regla de P7-10), no la ley. **F1 pasa.**

## F2 · En banco: sin cuaderno nada tiene efecto ni ganas; con pruebas de red sin efecto, la red se apaga

`pruebas_P7_33.py --f2`: las 4 vidas de APRENDE del día 1 de P7-30 replicadas con la pieza -> `P7_33_F2.json`:

| cuaderno | vida | k máx antes de la primera prueba: botiquín · ración · red · camuflaje | cura imaginada máx antes: botiquín · ración | k red · camuflaje en toda la vida | `ir_curioso` por clase | pruebas (red · camuflaje · botiquín · ración) | cuaderno al fin, red: ignorancia · creencia dentro |
|---|---|---|---|---|---|---|---|
| vacio | s1_d1_A a10 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 6399, net 20, camouflage 557, first_aid 701 | 1 · 1 · 1 · 1 | 0,480 · 0,00 |
| vacio | s1_d1_A a11 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 255, net 1004, camouflage 732, first_aid 2134 | 0 · 0 · 0 · 2 | — · — |
| vacio | s2_d1_A a10 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 60, camouflage 1441, first_aid 750, net 919 | 0 · 0 · 1 · 1 | — · — |
| vacio | s2_d1_A a11 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 50, first_aid 255, camouflage 51, net 1479 | 0 · 1 · 4 · 1 | — · — |
| tres redes sin efecto | s1_d1_A a10 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 6399, first_aid 712, camouflage 567 | 1 · 1 · 1 · 1 | 0,209 · 0,00 |
| tres redes sin efecto | s1_d1_A a11 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 654, first_aid 2537, camouflage 905 | 0 · 0 · 0 · 2 | 0,270 · 0,00 |
| tres redes sin efecto | s2_d1_A a10 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 60, camouflage 2053, first_aid 830 | 0 · 0 · 1 · 1 | 0,270 · 0,00 |
| tres redes sin efecto | s2_d1_A a11 | 0,00 · 0,00 · 0,00 · 0,00 | 0,0 · 0,0 | 0,000 · 0,000 | rations 50, first_aid 41, camouflage 51, net 115 | 0 · 1 · 4 · 1 | 0,270 · 0,00 |

Lectura. Con el cuaderno vacío, k = 0 y cura imaginada 0 para las cuatro cosas en todos los tics hasta la primera prueba (y k de red y camuflaje = 0 en toda la vida, porque sus pruebas no dan nada en el cuerpo): ninguna de las cuatro tiene efecto imaginado ni ganas. Con un cuaderno cargado a mano con tres pruebas de red sin efecto, la creencia de la red es 0,0 (creencia dentro), su ignorancia baja de 1 a 0,21-0,27 (tres recuerdos frente al neutro; no es cero: la ignorancia se apaga con los recuerdos, no de golpe), y `ir_curioso` hacia una red pasa de 20, 1004, 919, 1479 tics (cuaderno vacío) a 0, 0, 0, 115. **F2 pasa** (la curiosidad de la red se apaga en cuanto las otras clases llaman más; con 0,2-0,3 de ignorancia todavía puede ganar cuando las demás ya están probadas).

## F3 · El humo de 3 días (APRENDE, semillas nuevas)

Semillas `semillas_P7_33.json` (k 198, 199, 200: 40997258, 41101987, 41206716); imagen `Dockerfile.pareja_P7_33` (GEMV_P7_33=1 sobre la de P7-30); `lanza_P7_33.py --cadena-aprende 1 1 3`; diarios en `paintball/runs/P733_s1_d<D>_APRENDE_<semilla>/`; `analiza_P7_33.py` -> `P7_33_humo.json`. Partidas: d1 completed (0,1053 USD); d2 completed (0,0585 USD); d3 completed (0,1102 USD).

| día · asiento | tics | puesto | cuaderno leído | orden de contacto (tic) | coge: botiquín · ración · red · camuflaje | pruebas: botiquín (firmes, al menos, cortes) · ración (f, a, c) · red (ventanas completas / cortas) · camuflaje (completas / cortas) | al acabar: creencia dentro · ignorancia · k: botiquín / ración / red / camuflaje | `ir_curioso` con paso listo | latencia: ms mediana · sobre el tic · guarda |
|---|---:|---:|---|---|---|---|---|---:|---|
| d1 · 10 | 11.130 | 11 | no | camuflaje (629), red (651), botiquin (684), racion (10.427) | 1 · 2 · 1 · 1 | 0 (0, 0, 0) · 1 (1, 0, 0) · 1 (1 / 0) · 1 (1 / 0) | no sé · 1,000 · 0,300 / 7,7 · 0,485 · 0,010 / -0,1 · 0,346 · 0,000 / -0,3 · 0,345 · 0,000 | 22 (0,4 %) | 15,0 · 1,04 % · NO PASA |
| d1 · 11 | 11.067 | 12 | no | botiquin (5.259), racion (11.511) | 1 · 1 · 0 · 0 | 1 (0, 1, 0) · 0 (0, 0, 0) · 0 (0 / 0) · 0 (0 / 0) | 7,4 · 0,472 · 0,008 / no sé · 1,000 · 0,933 / no sé · 1,000 · 0,000 / no sé · 1,000 · 0,000 | 93 (7,5 %) | 5,7 · 0,04 % · pasa |
| d2 · 10 | 14.276 | 1 | sí | racion (516), botiquin (593), camuflaje (616) | 13 · 8 · 0 · 3 | 2 (0, 1, 0) · 1 (1, 0, 0) · 0 (0 / 0) · 2 (2 / 0) | 15,2 · 0,456 · 0,340 / 10,0 · 0,336 · 1,686 / -0,1 · 0,358 · 0,000 / -0,2 · 0,210 · 0,000 | 6 (0,1 %) | 3,8 · 0,01 % · pasa |
| d2 · 11 | 14.184 | 4 | sí | racion (527), red (715) | 0 · 6 · 1 · 0 | 0 (0, 0, 0) · 5 (0, 5, 0) · 1 (1 / 0) · 0 (0 / 0) | 7,2 · 0,485 · 0,197 / 8,0 · 0,141 · 0,714 / 0,0 · 0,513 · 0,000 / no sé · 1,000 · 0,000 | 12 (0,1 %) | 14,9 · 0,47 % · pasa |
| d3 · 10 | 14.472 | 2 | sí | botiquin (626), racion (2.738) | 5 · 2 · 0 · 0 | 1 (0, 1, 0) · 1 (0, 1, 0) · 0 (0 / 0) · 0 (0 / 0) | 17,4 · 0,301 · 0,410 / 10,1 · 0,253 · 1,280 / -0,1 · 0,369 · 0,000 / -0,1 · 0,218 · 0,000 | 229 (13,9 %) | 2,7 · 0,00 % · pasa |
| d3 · 11 | 14.472 | 1 | sí | camuflaje (659), red (725), botiquin (2.772) | 2 · 0 · 1 · 1 | 0 (0, 0, 0) · 0 (0, 0, 0) · 1 (1 / 0) · 1 (1 / 0) | 7,0 · 0,497 · 0,194 / 8,0 · 0,148 · 0,746 / 0,0 · 0,314 · 0,000 / 0,0 · 0,414 · 0,000 | 38 (1,3 %) | 1,3 · 0,00 % · pasa |

**El contexto de las pruebas** (punto 8; al abrir cada prueba, en las 6 vidas):

| cosa | pruebas abiertas | en calma | con rival a 4 o menos | con vida < 30 | en fuego |
|---|---:|---:|---:|---:|---:|
| botiquin | 4 | 0 | 4 | 0 | 0 |
| racion | 8 | 0 | 8 | 0 | 0 |
| red | 3 | 3 | 0 | 0 | 0 |
| camuflaje | 4 | 3 | 1 | 0 | 0 |

Oído y ley en el humo: d1·10: 1 aviso(s) [('flood', [10, 22, 14, 26], 4400)], cambios de casillas [[4400, 25], [5120, 0]]; d1·11: 1 aviso(s) [('flood', [10, 22, 14, 26], 4400)], cambios de casillas [[4400, 25], [5120, 0]]; d2·10: 1 aviso(s) [('flood', [10, 22, 14, 26], 4400)], cambios de casillas [[4400, 25], [5120, 0]]; d2·11: 1 aviso(s) [('flood', [10, 22, 14, 26], 4400)], cambios de casillas [[4400, 25], [5120, 0]]; d3·10: 1 aviso(s) [('flood', [10, 22, 14, 26], 4400)], cambios de casillas [[4400, 25], [5120, 0]]; d3·11: 1 aviso(s) [('flood', [10, 22, 14, 26], 4400)], cambios de casillas [[4400, 25], [5120, 0]].

Lo que se ve en los tres días: cogidas (6 vidas): botiquin 22, racion 19, red 3, camuflaje 5; pruebas: botiquin 4, racion 8, red 3, camuflaje 4.

Lectura. (i) Las cuatro cosas se tocan y se prueban: en 2 de las 6 vidas la primera cosa que toca es el camuflaje (tics 629, 659), en las demás el botiquín o la ración; la red la tocan 3 vidas (tics 651, 715, 725) y el camuflaje 3; las pruebas de red y camuflaje son ventanas completas de 10 s (7 de 7) con efecto en el cuerpo entre -0,4 y 0,0: "no hizo nada"; la creencia de las dos queda en 0 o por debajo y sus ganas (k) en 0,000 en las 6 vidas; su ignorancia baja a 0,21-0,51 con una sola prueba y el cuaderno la lleva al día siguiente (día 2 y 3 leídos). (ii) El contexto (punto 8): el botiquín (4 pruebas) y la ración (8) se prueban siempre con un rival a 4 casillas o menos (en calma: 0 y 0); la red se prueba en calma 3 de 3 y el camuflaje 3 de 4: lo que se prueba por curiosidad se prueba en calma; lo que se usa, en peligro. (iii) Oído y ley: las 6 vidas oyen el mismo aviso (inundación [10, 22]-[14, 26], tic 4.400) y la ley cierra 25 casillas de 4.400 a 5.120; ninguna vida choca contra el agua (0,02 %, 0,00 %, 0,02 %, 0,09 %, 0,30 %, 0,07 % de pasos listos bloqueados sin cuerpo). (iv) Latencia: una vida marcada (d1 asiento 10: 1,04 % de decisiones sobre el tic, mediana 15,0 ms); la pieza de las cuatro cosas cuesta más por tic que la de P7-30 (medianas 1,3-15,0 ms frente a 3,9 de media en P7-30): a vigilar en el campo. (v) `ir_curioso` con el paso listo: 0,1-13,9 % (P7-30: 0,2 %): con cuatro clases desconocidas la curiosidad vuelve a mover, sobre todo el día 3 asiento 10. Una pega de ingeniería anotada: la marca de P7-29 de las fotos por índice se desajusta en algunos tics con cuatro clases (`P7_error` "fotos para candidatos": 3, 3, 3, 3, 3, 3 por vida); en esos tics la foto de llegada de `ir_curioso` o la de usar puede ir a otro candidato; a corregir antes del campo.

## F4 · Créditos, y lo que costaría el campo

Plataforma: 0,2740 USD en 3 partidas del humo (0,0913 por partida); acumulado del siete: 52,6550 (hasta P7-30) + 0,2740 = **52,9290 USD**. Consola de Anthropic: 0. El campo de tres brazos, 20 días y dos series (120 partidas) costaría, al precio de este humo, 10,96 USD; al precio medio del campo de P7-30 (0,0874 por partida en 120 partidas), 10,49 USD. Saldos no consultados.

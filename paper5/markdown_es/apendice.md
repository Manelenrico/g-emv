## Apéndice. Los números y de dónde salen

Las cifras del texto aparecen aquí con el valor exacto que se midió y el informe de donde salen; los umbrales que se fijaron antes de medir se señalan como tales. En el texto las cifras van redondeadas y dichas en palabras; aquí van enteras. Los informes están en la carpeta de datos del trabajo (cantera/paper5/), cada uno con la versión del programa que lo produjo. Todas las partidas de campo se jugaron en Zero Sum 0.1.18 (etiqueta zero-sum-v0.1.18, commit 9bd0ddf, en el repositorio arisklar6/battle-royal, que antes se llamaba arisklar6/zero-sum y redirige a él; es una etiqueta anotada, así que quien la compruebe debe desreferenciarla para ver ese commit). El motor es el del primer trabajo, sin cambios (md5 1e511978c251130e95169ebf8443efa1).

### A.1 El mundo lento, ajuste por ajuste

| Ajuste enviado | Valor | Qué pasó en las partidas | Fuente |
|---|---|---|---|
| max_ticks | 18.240 | partidas de 18.240 tics (12 min 40 s), el doble del defecto | informe_P5ARI3 |
| freeze_ticks | 480 | 20 s sin ataques; primer movimiento en el tic 482 (moverse se puede, pero salir de la casilla de salida mata en el acto) | informe_P5ARI3 |
| zone.schedule | desde el tic 7.296, 25 % más lento | el anillo avisa en el tic 7.296 (40,0 %) y cierra 1,25 veces más lento | informe_P5ARI3 |
| sponsor.budget_per_team | 600 (defecto 300) | sin efecto: los paquetes programados de cada pareja gastan 80 (20 la cápsula de ración y 60 el botiquín); cualquier presupuesto de 80 o más da los mismos que el de 300; por debajo de 80 se pierden paquetes, y con 0 ninguno. Los agentes no pueden pedirle nada al patrocinador | informe_P5ARI3; revisión de Ari Sklar sobre el código en zero-sum-v0.1.18 |
| sponsor.live | false | leído por el motor (src/zero_sum/sim.nim:212); false es el valor por defecto de la variante competition, así que no cambió nada. live no apaga el patrocinador: solo abre la consola con la que una persona puede dar regalos en directo, en una partida local. El "enabled" que ve el agente es otra cosa, fijo a true (obs.nim:174) | informe_P5ARI3; revisión de Ari Sklar |
| regalos del patrocinador | los de la variante competition | 8 cápsulas de dos raciones (anunciadas en los tics 2.016 a 2.184, el 11 % de la partida) y 8 botiquines (4.608 a 4.776, el 25 %), un equipo cada 24 tics; aterrizan cinco segundos (120 tics) después del aviso. Para la pareja (equipo F): raciones anunciadas en el tic 2.136 al asiento 10 y botiquín en el 4.728 al asiento 11. Son los tics de la configuración; el diario registra cada suceso un tic después | informe_P5ARI3, informe_P5ARI4 |
| rivales | roster_lento_v1 | las tres políticas que más atacaban al principio, sustituidas por zero-sum-scavenger, relh-zero-sum y belobog, tres veces cada una; la pareja en los asientos 10 y 11. relh-zero-sum no es pacífica: en el juego normal causa 52 de 418 muertes (12,4 %), todas pasado el tic 2.000 | informe_P56B, líneas 51 y 60; informe_P5AP1 |
| quién mató a la criatura en el mundo lento | — | 389 muertes en 200 episodios (399 diarios): relh-zero-sum 156 (40,1 %), la primera en el tic 8.191, mediana 8.723; también quien más golpes dio, 1.373 (32,5 %). Belobog, 0 muertes; zero-sum-scavenger, 3. El anillo, 14,1 %. Sin atribuir, 11,05 %. Reparto estable en las tres series | informe_P5AP2 |

### A.2 Por secciones

| Sección | En el texto | Valor medido | Fuente |
|---|---|---|---|
| 1 y 2 | unas dieciséis opciones cuando puede andar | 16 de mediana con las piernas listas | informe_P5AP1 |
| 5 | las opciones que ya tenía en la mano, unas dieciocho | 18 candidatos de mediana en el puñado comparador | informe_P53D, línea 21 |
| 2 | once instantes de pausa de las piernas | enfriamiento 16 − velocidad = 11 tics por casilla | informe_P52b; la fórmula, del código del juego: src/zero_sum/sim.nim:144 en la etiqueta zero-sum-v0.1.18 |
| 2 | tres de cada cuatro instantes con las piernas en pausa | 75,69 % de los tics vivos | informe_P52b |
| 2 | nueve de cada diez decisiones de quedarse, con las piernas frías | 90,38 % de los noop | informe_P52b |
| 2 | quieta de verdad, ocho de cada cien | 7,96 % | informe_P52b |
| 2 | la regla de empates del trabajo anterior, cuatro de casi dos mil | 4 de 1.908 victorias | informe_P56A |
| 3 | calma de amenaza: de tres a siete de cada cien, y dieciocho | 3 a 7 % (juego normal); 18,17 % (mundo lento) | informe_P51_C |
| 3 | ni un instante sin nada que falte, en casi cuarenta mil | 0 de 37.750 tics vivos | informe_P51_C |
| 3 | manos bien servidas, poco más de uno de cada cien | 1,24 % de los tics (7.960), en 10 de 260 diarios | informe_P51_E, línea 81 |
| 3 | cuatro casillas nuevas en calma, catorce fuera | 4,13 y 14,10 por cien tics | informe_P51_C |
| 3 | en los dos mil primeros instantes, tres de catorce tipos de rival: nueve de cada diez golpes y ocho de cada diez muertes | 3.612 de 3.928 golpes (91,96 %) y 174 de 211 muertes (82,46 %) antes del tic 2.000; sobre todas las muertes de los 434 diarios, 190 de 418 (45,45 %) | informe_P51_E, líneas 154 a 186 (el 92 % de muertes de la línea 188 es un error del informe); informe_P5AP1 |
| 4 | más de dos mil doscientos momentos | 2.230 escenas de 40 diarios | informe_P52c |
| 4 | bueno ocho y media de cada cien, tonto siete | 8,52 % y 7,22 % (n = 845 de los 908 momentos con un futuro mejor: en los otros 63 el consejo bueno era no moverse, y la puerta de siempre no puede juzgar un destino que es la propia casilla; el consejo al azar se compara en las mismas 845 escenas) | informe_P52c |
| 4 | la exposición firma cuatro de cada diez rechazos | S-8-EXPOSICION, 40,51 % | informe_P52c |
| 4 | a un paso dos de cada cien; a tres o más, veintitrés | 2,35 % y 22,96 % | informe_P52c |
| 4 | en catorce de cada cien, lo mejor era no moverse | 125 de 908 escenas (13,77 %) | informe_P52c |
| 5 | el bueno setenta y una de cada cien, el tonto veinticuatro puntos menos | 70,88 % y 46,79 % | informe_P53B |
| 5 | la imaginación acierta en nueve de cada diez de 180 viajes | error cero en la mediana y en el percentil 90, a 100 tics, en 180 ventanas | informe_P53A |
| 5 | con la regla de honestidad, uno de cada veinte llega a juzgarse | 4,52 % | informe_P53H |
| 5 | de los que se juzgan, ochenta y cinco buenos y cuarenta y tres al azar | 85,37 % y 42,86 % | informe_P53H |
| 5 | nueve de cada diez partes pasan por los otros | 87,4 % (juego normal); 90,1 % (mundo lento) | informe_P53F |
| 1 y 5 | casi la mitad de eso es el hermano; la mitad de todo, los extraños | de una mejora total de 212,3: hermano 85,3 (40 %), rivales 104,6 (49 %) | informe_P53F |
| 5 | el hermano cuenta dónde estará: la puerta recupera la mitad | 51,2 % de su aporte | informe_P53H |
| 6 | el consejero que habla al azar pierde la confianza | 34 de 40 vidas por debajo de 0,2 (P5-4A); 39 de 40 (P5-4B) | informe_P54A, informe_P54B |
| 6 | media confianza, lo peor | con C = 0,5 la diferencia bueno contra azar es +0,02 | informe_P54A |
| 6 | más de tres mil respuestas; habla de los otros ocho de cada diez | 3.284 respuestas; 80,9 % | informe_P55A |
| 6 | la mitad de las veces contra casi nueve de cada diez | llegadas 49,0 % contra 87,5 % de "nada cambia" | informe_P55A |
| 6 | pasos sueltos: ninguno de 367; formas: uno de cada diez; modelo grande, casi dos | 0 de 367; 10,48 %; 18,13 % | informe_P55B |
| 6 | en las manos acierta dos de cada diez; en el vínculo, seis | 20,08 %; 60,23 % | informe_P55B |
| 6 | nombra a los rivales una de cada siete (antes siete de cada diez) | 14,5 % y 69,5 % | informe_P55B |
| 6 | calla una o dos de cada cien | 1 a 2 % | informe_P55B |
| 7 | cien partidas, doscientas vidas, millón y medio de instantes | 200 diarios; 1.501.210 tics vivos; 0 decisiones saltadas (no mide si los pasos llegaron al mundo: fila de pasos que no llegaron, sección 10) | informe_P56C |
| 7 | más de dos mil consultas, todas con su parte | 2.088 de 2.088 | informe_P56C |
| 7 | dos o tres planes aceptados de cada cien | 2,4 % con el consejero (brazo F); 1,7 % con formas al azar (brazo T) | informe_P56C |
| 7 | más de tres mil planes rechazados; el cuerpo solo no estaba mejor | 3.568 formas rechazadas por área | informe_P56C |
| 7 | tres de cada cuatro pasos, el del plan | 76,8 % con el consejero, con las piernas listas | informe_P58O |
| 7 | los planes del consejero cumplieron cuarenta y dos de cada cien paradas | 42,3 % por punto de control con el consejero, contra 61,1 % con formas al azar | informe_P56C, informe_P58O |
| 7 | calló cuatro de cada diez | 40,8 % de las citas | informe_P56C |
| 8 | más de seis mil instantes seguidos de calma sin mirar | tics 1.977 a 8.027 (6.050), mapa por ver fijo en 0,7969; vida P57C_t2_A_20994019, asiento 10 (cuerpo solo, mundo lento definitivo) | figuras_paper5/fig3_meseta_de_calma.txt |
| 8 | sin la balanza, diez veces más cambios en inseguro | de 0,48 % a 5,39 % | informe_P57A |
| 8 | lo no visto, a seis casillas | 6 casillas de mediana (nunca más de 11) | informe_P58A, línea 91 |
| 8 | el tirón, en entorno seguro, cambia una decisión de cada dieciocho | 5,62 % | informe_P57C, línea 187 |
| 8 | el tirón en campo: nueve por ciento más de mapa | 1,086 veces; 14,5 casillas nuevas por cien tics en los dos brazos | informe_P57C |
| 8 | sin el alivio, tres de cada cien viajes; con él, uno de cada tres | 2,68 % y 37,25 % | informe_P58A |
| 8 | obedece nueve de cada diez zancadas | 92,5 % | informe_P58M |
| 8 | siete de cada diez viajes se completan; ninguno pisa el destino | 68,9 % (144 de 209); se completa = ve la bajada de mapa prometida o la casilla de destino; destino pisado, 0 de 209 | informe_P58M; informe_P5FIG2 |
| 8 | el cuerpo solo va y viene entre dos casillas durante la calma | casillas (19,13) y (18,12), 527 movimientos, uno cada 11 tics, del tic 2.033 al 8.027; dos opciones se turnan: desde (19,13) gana ir a por unas flechas en (18,15), cuyo primer paso es (18,12); desde (18,12) esa opción no se genera y gana ir a por botín, que vuelve a (19,13); las flechas no se cogen nunca. Desde (19,13) ve a un rival parado y desde (18,12) no: malestar 3,6767 y 3,26065 | informe_P5FIG2 |
| 8 | casi seis veces más mundo dentro de un viaje | 5,81 veces, en las 20 semillas; 5,58 en los tramos sin pasos perdidos (IC95 por vidas 4,2 a 7,2) | informe_P58M, informe_P5ARI4 |
| 8 | cinco causas de ruptura | 5 de las 7 rupturas previstas dispararon | informe_P58M |
| 8 | el sello pedía la mitad más de mapa | umbral fijado antes de medir: 1,5 veces | informe_P58M |
| 8 | ve un dieciséis por ciento más | 1,16 emparejado (10, 15 y 20 semillas) | informe_P58M |
| 8 | la forma vive el dos por ciento de la vida | 2,2 % | informe_P58M |
| 8 | una forma cada cuarenta y tres instantes seguros | 0,0205 a 0,0313 formas por tic seguro; de 10 a 383 formas por partida | informe_P58M |
| 8 | no cuesta vida ni puesto | vida p = 0,50; puesto p = 1,00 | informe_P58M |
| 8 | cuatrocientas treinta y cuatro vidas; ninguna muerte a manos de un desconocido (nunca visto) | 0 de 418 muertes a manos de un asiento con conocimiento cero | informe_P57B |
| 8 | sabe de su asesino más de nueve décimas | conocimiento del matador, mediana 0,94 | informe_P57B |
| 8 | el vínculo cambió alguna decisión con un armado a tiro, una o dos | 1 decisión con k = 0,1 y 2 con k = 0,2, en dos configuraciones que nunca corrieron juntas | informe_P57B |
| 8 | con la curiosidad como tirón, más de veintisiete mil decisiones con un armado a tiro, ninguna de curiosidad | 0 de 27.519 (serie del tirón) | informe_P57C |
| 8 | dos predicciones fallidas por cómo se midieron | armado a tiro con viaje activo: 52 tics, 5 con piernas listas (rupturas por veto); coste por tic: un asiento de 39 a 5,51 ms en todos sus tics, cero decisiones saltadas | informe_P58M |
| 10 | defecto heredado 1, el don: suelta y recoge lo mismo | 74.545 tics en 379 vidas (2,49 %); 39 vidas afectadas; el 95,1 % de los 4.576 dones registrados eran la oscilación | informe_P6_6 (cantera/paper6/) |
| 10 | defecto heredado 2: intenta coger con la mochila llena | 47.244 tics en 182 de 379 vidas; peor racha 5.593 tics (44 % de esa vida); coger empata con quedarse quieto y el desempate excluye quedarse quieto | informe_P6_8 (cantera/paper6/) |
| 10 | defecto heredado 3: rival sin arma no cuenta como amenaza | 705 golpes y 30 muertes de rivales visibles con la mano vacía | informe_P6_8 (cantera/paper6/) |
| 10 | pasos que no llegaron al mundo, en los brazos con puerta | pasos listos hacia casilla libre no ejecutados: A 0 %, F 6,2 %, T 2,6 %, K 10,4 %; en tramos limpios: puntos de control F 45,1 % (n 51) contra T 63,0 % (n 27), diferencia −17,9 [−38,0, +5,2]; emparejada 48,5 % contra 60,0 %; casillas nuevas K/A 1,213; mundo emparejado 1,308; compromiso obedecido 91,9 % en 168 formas limpias de 209, 90 pasos emitidos no ejecutados; vida y puesto no restringibles (las vidas sin paso perdido son cortas); decisiones que esperaron al juicio, F 0,215 % | informe_P6_22 (cantera/paper6/), informe_P5_LAG (cantera/paper5/) |
| 10 | pruebas del banco con modelo real | 603 llamadas, 4,44 dólares | informe_P55B |
| 10 | seis de doscientos episodios sin coste informado | 6 episodios, contados a cero | informe_P5ARI_cierre |

### A.3 Lo que costó

El coste registrado del paper cinco fue de 31,33 dólares; seis episodios no informaron de su coste y se contaron a cero, así que el gasto real puede ser algo mayor. De ellos, 16,08 fueron partidas en la plataforma, con su saldo, y 10,81 fueron el consejero llamado a través de la plataforma, también con su saldo: ninguno de los dos le costó nada al autor. Los 4,44 restantes fueron las pruebas de banco con modelo real, pagadas por el autor. Por series: el consejero en formas, 7,87 de plataforma y 10,48 de modelo; la curiosidad como tirón, 2,67; la curiosidad como viaje, 3,44; y otras diez series y pruebas sueltas, 2,43 entre todas. El desglose completo está en informe_P5AP1.

### A.4 Las figuras

Cada figura se dibujó con cantera/paper5/fig_paper5.py a partir del diario de una o varias vidas. Su ficha, con los datos exactos y el motivo por el que se eligió esa vida, está en la carpeta figuras_paper5/.

| Figura | Qué vida | Valores medidos | Ficha |
|---|---|---|---|
| 1 | P5-7C, tanda 2, brazo A (cuerpo solo), semilla 20994019, asiento 10 | 10.752 tics vividos; primer golpe en el tic 10.273 (7,1 min); 24 golpes en toda la vida; lo que le falta nunca baja de 0,6667; puesto 13; la mancha del panel de abajo es el vaivén entre dos casillas (tics 2.033 a 8.027): las filas F-4-ALCANCE y S-8-EXPOSICION entran y salen cada 22 tics. Elegida entre las 93 vidas del brazo A con más de 6.000 tics | fig1_una_vida.txt |
| 2 | P5-6C, tanda 5, brazo F (cuerpo con consejero), semilla 22250767, asiento 10; forma 7, nacida en el tic 3.999 y aceptada en el 4.001 | puntos de control en los tics 4.004, 4.037, 4.092 y 4.092; abandonada en el tic 4.062 porque deja de ganar. Las curvas imaginadas no están en el diario: se recalculan con el mismo código de la puerta y reproducen la ventaja registrada (0,28435) y los puntos de control. Mejor caso: 10 de las 45 formas del brazo F pisan el destino de su primer tramo, y esta es una; el destino del tramo 2, (22,22), no se pisó dentro del plan. En el primer punto de control, lo real sale 0,519 mejor que lo imaginado, y 0,500 de eso son los pisos del rival que impone la regla de honestidad (informe_P5FIG2) | fig2_forma_de_un_plan.txt |
| 3 | la misma vida que la figura 1 | tics 1.977 a 8.027 (6.050) con amenaza cero y mapa por ver fijo en 0,7969 | fig3_meseta_de_calma.txt |
| 4 | P5-8M, tanda 0, brazo K (cuerpo curioso), semilla 20260916, asiento 11: el asiento con más viajes aceptados de las cuarenta partidas | 18 viajes: 5 se completan y 13 se atascan (tres pasos sin acercarse al destino); los 13 seguidos van al mismo destino, (21,29); ninguno pisa su destino. Sin viajes del tic 4.907 al 8.337 (amenaza por debajo de 0,2 solo en 9 de 3.431 tics) ni después (17 propuestos, los 17 rechazados por la puerta; ventaja máxima 0,00455 contra margen 0,02); informe_P5FIG2 | fig4_una_vida_curiosa.txt |
| 5 | P5-8M, las cuarenta partidas, asientos 10 y 11 de los dos brazos | 40 vidas del cuerpo solo y 39 del cuerpo curioso (falta el diario del asiento 10 de la partida 20784561, informe_P5ARI_cierre); mapa por ver reconstruido cada 200 tics con la misma pieza que usa el cuerpo; mediana dibujada solo con 5 vidas o más | fig5_cuanto_mundo_conoce.txt |

# Apéndice — De dónde sale cada número (v14, 12 de septiembre de 2026)

Cada afirmación con cifra del cuerpo, casada con su acta de la cantera
(paper3_cantera/actas/), la partida y el guion que la produce. La regla
es simple: ninguna fila sin acta o fichero que la nombre, y ninguna
cifra en el cuerpo sin fila aquí.

## Secciones 1 y 2

Las cifras de machina_1 vienen del trabajo anterior, y conviene decir cómo
están guardadas, porque no siguen la forma de las demás. Los peldaños dos
y tres cerraron con acta; el primero, no: cerró con una especificación
sellada antes de correrlo y un paquete de resultados, y es ese paquete —
congelado, con su huella md5 — el que contiene estas cifras. Los
documentos de cierre del peldaño son `the_pack_peldano1_spec.md`
(md5 `0bd20d8fa9641397812e02417778e0d5`, sellada el 28 de agosto de 2026),
`the_pack_peldano1_paquete.md` (md5 `a16210921c63a36b1f62cfadb975a8b3`) y
`the_pack_camino.md` (md5 `34e0ecf51e4552a987e8ab82c1bf9f30`), donde
consta el cierre del peldaño uno el 29 de agosto de 2026. No hay un
repositorio aparte del trabajo anterior: estos ficheros viven en la raíz
de `gemv-coworld`, y los tres primeros están ya en la cantera.

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| ocho cuerpos con la misma geometría en machina_1 | 8 agentes; N = 3 corridas × 10.000 tics | the_pack_camino.md (P1); paper dos (DOI 10.5281/zenodo.21994358) | — |
| el censo solo miraba: la vida del pueblo con censo y sin censo era la misma | observe-only, bit a bit | the_pack_camino.md (P1, "observe-only bit-exacto probado") | — |
| ocho temperamentos fijados antes del censo; el peso social va de más a menos | tabla de perfiles por asiento: 1,90 / 1,70 / 1,60 / 1,40 / 1,40 / 1,25 / 1,15 / 1,15, en una sección declarada NO-LEY; sello del 17 de agosto de 2026 | paper3_cantera/the_pack/temperamentos_spec.md, md5 `616a19719c24c10ba92fe2602db768d7`; hechos/forense_censo_temperamentos.md | pregonero/run_bench_temper.sh |
| nacían todos a dos o tres casillas del centro | campo de distancia de nacimiento al centro: 2 o 3 en los ocho | the_pack_censos_crudos.md, md5 `864a0bed356a5f57e4587551ca108cee`; hechos/forense_censo_temperamentos.md | — |
| un agente minó ochenta y cuatro veces y otro cinco | ag7 = 84; ag3 = 5 (vida con semilla 170534803, columna de minado real) | the_pack_peldano1_paquete.md, tabla (A), md5 `a16210921c63a36b1f62cfadb975a8b3` | — |
| el temperamento no predice cuánto mina cada uno | corr(peso social, minado) −0,25 / −0,18 / −0,04 | hechos/forense_censo_temperamentos.md | pregonero/run_bench_temper.sh |
| el censo veía bien a los del centro y casi nada a los de la periferia | cobertura observador→observado: hasta 72 % en el racimo central, 1 % en los pares de la periferia (misma vida) | the_pack_peldano1_paquete.md, tabla (B), md5 `a16210921c63a36b1f62cfadb975a8b3` | — |
| peldaño dos: con los oídos, cada uno tenía noticia de todos; el cotejo no dio nada | cobertura completa por anuncio firmado; cotejos casi nulos y aciertos 0 | the_pack/the_pack_peldano2_acta.md | — |
| peldaño tres: criterio de dos casillas; la fiabilidad nació distinta por emisor; el pueblo rindió peor y luego igual o mejor | — (sin cifra en el cuerpo) | the_pack/the_pack_peldano3_acta.md; the_pack/the_pack_peldano3b_acta.md | — |

*Una salvedad sobre el fichero de los temperamentos, que conviene decir
en vez de dejarla en el índice: `temperamentos_spec.md` no estaba en la
cantera cuando se congeló, y se incorporó a ella el 9 de septiembre de
2026, con la incorporación declarada en el índice de la cantera. La copia
es literal, sin editar, y su huella md5 es idéntica a la del original. Es
un fichero de la temporada anterior — la colmena —, como las demás filas
de este bloque, y no toca ningún dato de las series de este trabajo.*

*Los peldaños dos y tres sí tienen acta: `the_pack_peldano2_acta.md`, `the_pack_peldano3_acta.md` y `the_pack_peldano3b_acta.md`, en la carpeta `the_pack/` de la cantera. No hay cifra del cuerpo que dependa de ellas.*

## Sección 3

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| liga pública: 72 partidas con resultado, 7º de 11, puesto mediano 11 de 16, último en pie 4 veces, 1 sin matar | 72; 7/11; 11/16; 4 (5,6 %); 1 (ereq_d53c24be) | hechos/hecho_liga_publica.md; runs/debut | — |
| series propias temporada uno: 240 partidas, último en pie 5, 2 sin matar | 5/240 (2,1 %); 2 | hechos/hecho_v19_campeona.md | — |
| el techo del que va solo: qué se comparó, qué se encontró y por qué se paró | 80 pares de partidas ya jugadas, campeona contra la última del taller, primeros 1.000 tics: pegado (≤1 casilla) 4,6 % vs 8,1 %, pareado 32-38-10, p = 0,55; el contacto temprano no lo predice la cuna (corr +0,114, n = 160); la palanca restante — un miedo preventivo a los desconocidos — exigía rediseñar una fila y su efecto en los puestos era indemostrable a n = 40 | 52_primer_minuto (A, tope escrito); 51 (instrumento) | — |
| el asiento es lo único que identifica a un jugador: de cada visible llegan asiento y estado (posición, franja de vida, arma, veneno, cura); sin nombres; los nombres del visor los pone la plataforma; el daño llega con el asiento del que golpea, salvo el veneno (sin autor) y el camuflado (fuera de la lista); el hermano llega como asiento una vez al empezar | campos de visible.agents (slot + 7 de estado); damage_taken "P<slot>" / "poison"; player_config teammate_slot; participants de la plataforma indexados por position | hechos/hecho_identidad_jugadores.md | — |
| el cuerpo "vista 8, agilidad 6, velocidad 5, fuerza 1" | INT 8 / ATH 6 / SPD 5 / STR 1 | presupuesto_acta.md (34), tabla "la actual" | — |
| venda 50 en 2 s, la interrumpe cualquier golpe, el veneno la bloquea; ración 15 en 1 s, nada la interrumpe | 50 hp / 48 tics; 15 hp / ~24 tics | hechos/hecho_racion_venda.md | — |
| "una decisión, con sus números": 19 futuros en el primer tic, gana moverse hacia el noroeste con 4,267 y curarse queda en 4,468; en el siguiente, con el movimiento en enfriamiento, quedan dos — quieto 4,962 y curarse 4,480 — y gana curarse por 0,482 | t1710 y t1711 de `ereq_b915417a` | recuento del vigilante del 10-sep sobre el diario de esa partida | — |
| por qué gana el paso: el desglose por filas | el diario guarda el detalle por candidato cada doce tics (`policy.py`, `DETALLE_CANDIDATOS_CADA = 12`), y el tic más cercano con detalle es el 1704, donde curarse vale lo mismo, 4,468, con vida prevista 57. En ese tic: F-DANO 1,242 (moverse) contra 0,431 (curarse); R-CARENCIA 0,667 contra 1,0; F-4-ALCANCE 0,35-0,40 contra 0,5; S-7-AGRESOR 0 contra 0,5; S-8-EXPOSICION 0 contra 0,3. Agresor: asiento 12, con lanza, a una casilla; último golpe recibido en t1697, trece tics antes. En 1704 el paso que gana es `move_E` (4,269); en 1710, `move_NW` (4,267). Los ejes por futuro no se guardan | t1704 de `ereq_b915417a` | recuento del vigilante del 10-sep; codigo/appraisal_zs_v37.py | — |
| lo que el decisor imagina al moverse: el final de un rumbo hasta donde alcanza la mirada, no la casilla contigua; lo emitido es un paso | candidatos `move_*`: `p2 = _simula_camino(pos, dir, mundo, speed, H)`, con H = mirada del tic (480 en esta partida), avanzando `ticks // coste` pasos en línea recta y parando en el primer sólido; `movs = int(dist(pos, p2))`, por eso [19,19] → [46,19] con movs 27. Candidatos `paso_*`: una casilla, movs 1. Candidatos `ir_*`: geodésica hacia un destino durante la misma mirada. Lo emitido tras elegir un `move_*` es un solo paso (`{"do": "move", "dir": …}`) | codigo/decisor_zs_v37.py, líneas 289-303, 411-413, 742, 786-802, 885-887; comprobación del vigilante del 10-sep | — |
| lo que el agente imagina de un golpe propio: alcance y daño, descargados sobre el primer cuerpo de la línea; nada de lo que los golpes ajenos le harían | daño propio = daño de catálogo × (5+FUE)/10 si es cuerpo a cuerpo, daño de catálogo si es proyectil; con alcance > 1 el objetivo se sustituye por el primer cuerpo de la línea; la vida prevista del golpeado alimenta S-7-AGRESOR (agresor) y S-HERIDO (hermano); S-VINCULO se enciende cuando el daño propio ≥ la vida cierta del hermano (parte fresco o techo de su franja), magnitud 1,0, plana; la esquiva no se predice (declarado en el código); ninguna fila lee el daño de las armas ajenas — la única mirada al arma ajena es el "¿hace daño?" binario de F-REENCUENTRO | codigo/decisor_zs_v37.py líneas 347-354, 847-870; codigo/appraisal_zs_v37.py líneas 162, 167, 1100-1112, 1028, 1138-1139, 1381, 815; comprobación del vigilante del 12-sep | — |
| el mapa de versiones y series de 3.5 | v29 (55) · v30 (56, 57) · v31 (59, 60) · v32 (61) · v33 construida y apagada (62) · v34 (63, 64) · v35 (65, 66) · v36 (68) · v37 (70, 71) · v27 en pareja (72). Roster por clasificación hasta el 64 (el acta 55 lo dice literalmente; la del 66 lo confirma al explicar cómo se excluyó a nuestro campeón); roster explícito de 10 UUID desde el 66, repetidos hasta llenar 14 asientos, con 0 participantes nuestros fuera de los asientos 10 y 11. Comprobación en frío del 10-sep, acta por acta: catorce coinciden; la del 62 nombra v33 solo como el brazo probado y rechazado y deja la v32 como efectiva, y así se dice en la tabla | actas 55-72; 66_manada2 y 72_ablacion (roster verificado) | — |
| la fila de la vida: lineal hasta perder 4 de cada 10, cuesta por debajo de 60 | M = u si u ≤ 0,4; M = u + 0,4·((u−0,4)/0,6)² si u > 0,4 | codigo/appraisal_zs_v37.py, CUESTA_UMBRAL_U, CUESTA_GANANCIA | — |
| con nuestro agente solo en la partida, los hermanos respondieron a agresiones la tercera parte de las veces | 327 (64) vs 918 (66) respuestas a agresor propio | 64_manada_campo, 66_manada2 | manada_campo.py::honor_dos |
| la tasa de defensa pasó de tres de cada cuatro a nueve de cada diez sin cambiar el agente | P2' 78 % (64) / 92 % (66) / 86 % acumulado | 68_nombre | desenlaces.py::ocasiones_v2 |
| temperamentos del censo: pesos sociales por asiento 1,90…1,15; el temperamento no predice el minado | corr(w_s, minado) −0,25 / −0,18 / −0,04 | temperamentos_spec.md (sello 17-ago); hechos/forense_censo_temperamentos.md; pregonero/run_bench_temper.sh | — |
| el registro no cubre las partidas enteras: diario para seis de cada diez tics vivos de la pareja; falta el principio de las partidas largas | cobertura 59,8 % (64), 59,0 % (66), 52,4 % (72); diarios sin cabecera 17 / 20 / 22 de 80; partidas afectadas 11 / 13 / 13 de 40; techo 10,78 MB (máximo sobre 836 diarios); causa: la captura de stdout de la plataforma, con vaciado (policy.py escribe sin tope; la descarga no recorta); si el servidor conserva el diario entero, sin comprobar | paintball/cobertura_diarios_acta.md (md5 b71bde537d06e31122eb6070d82af285) | cobertura_diarios.py |
| figura 1 (visor) | cuatro capturas de ereq_292ee72d a 0:00, 1:11, 2:06, 3:54 = tics 1, 1704, 3024, 5616 (24 tics/s); partes de la pareja legibles en el visor y cotejados con los diarios (1:11: P10 T1681 [30,17] hp 78; 2:06: P11 T3025 [25,21] hp 48); no sostiene ningún dato | paper3/figuras/ficha_figuras.md; md5 cdfcd19575a3e33fd7a7f31395780d89 | capturas de Manel; montaje tira_visor.py |
| figura 2 (registros) | ereq_292ee72d, t3029; anillo r=15 (24→19 en t2064, 19→15 en t2976); 9 vivos; 6 vistos + 1 recordado + los dos | ficha_figuras.md; md5 75d0b626ba768c151a668ede26f16008 | figuras_paper3.py |

## Sección 4

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| de ocho decisiones, el parte cambió cero | 0 de 8 (solo S-DANO-PAREJA ±0,03) | 53_parte (P4) | verifica_53.py |
| el margen de atacar al compañero-agresor se acercó | +0,405 → +0,047 a h10; 0 iniciaciones en 53 decisiones | 53_parte (P5) | verifica_53.py |
| dos entregas completas vistas en la primera serie | ereq_331e254f (t353→t419→t607), ereq_2502e92c (t387→t430→t479) | 55_pareja, 56_cuidado | — |
| el paso hacia el hermano ganaba una de cada cien decisiones — COTEJADA | ir_pareja elegido en el 1 % de los tics con decisión (crece 189 / encoge 185 tics) | 56_cuidado (B, forense de la separación, 79 diarios) | separacion.py |
| de estar a dos casillas del hermano en peligro en dos de cada cien ocasiones a una de cada tres — COTEJADA | ≤2 casillas con uno en franja de peligro: 2 % (serie 55, v29) → 36 % (serie 57, v30) | 57_pareja2 (P3) | pareja2.py |
| el don llega tarde: dones en 18 % de los episodios con la condición | 13 soltares / 17 eps cond. / 18 % | 57_pareja2 (P2) | pareja2.py |
| llevar dos vendas: seis de cada mil instantes | 614 de 106.066 tics (0,6 %) | 60_pareja3 | pareja3.py |
| la diagonal dar/usar | tabla mi_hp × su_hp (95…10 × 8…95) | 61_dar (P3) | verifica_61 / radiografía |
| la compañía: por debajo de 0,22 no cambia nada; por encima pierde la ración a 2 | barrido 0,05 → 0,5 | 62_compania | verifica_62.py |
| nueve de cada diez dones fueron raciones | 90 raciones + 8 vendas de 98 (criterio del 72: soltar a ≤2 del hermano vivo) | 72_ablacion; hechos/hecho_racion_venda.md | — |
| "ocho vendas": soltar-venda en el 66 | 10 soltar-venda en total; 8 dentro del criterio (≤2 del hermano vivo); los 2 restantes fuera del criterio | hechos/forense_dones_venda.md | — |
| seis vendas por margen claro (fila del herido), dos empates con el parte viejo (67) | 6 / 2; detalle por partida y tic | hechos/forense_dones_venda.md | — |
| curarse contra dar con la provisión encendida: dio por margen (parte de 1,5 s, hermano a 44 sin vendas) | 1 caso; partida y tic | hechos/forense_dones_venda.md | — |
| de ocho vendas, tres recogidas (las tres estando peor); cinco en el suelo o sobrantes; ninguna de las tres llegó a curar | 3 / 5; 0 de 3 curas completadas | hechos/forense_dones_venda.md; recuento por eventos del 10-sep en hechos/forense_dones_venda_addendum.md | — |
| LAS DOS VENDAS: dos intentos de cura cortados en los 10 s previos; empate soltar/quieto; pila de 2 en una ranura; muertes a 8 y 16 | tics y valores exactos | hechos/forense_dos_vendas.md; ereq_9869b665 | — |
| fallos mecánicos declarados: reloj de la cura (veta hasta 41 tics tras una interrupción) y soltar vacía la pila | 41 tics; no corregidos dentro de este trabajo | hechos/forense_dos_vendas.md | — |
| primera serie de la manada: 12 defensas en 7 partidas; los dos por turnos | 12; ereq_feafe3ac t534/t573/t583 | 64_manada_campo | manada_campo.py |
| cuatro golpes entre hermanos, tres con lanza | 4; 3 fuego amigo de defensa (lanza, rango 2) | 64_manada_campo, 65_alcance | manada_campo.py::golpes_entre |
| de veinte ocasiones, en doce el golpe era imposible | 20 ventanas; 12 sin alcance; 5/8 = 62 % | 64_manada_campo (autopsia P2), 65_alcance (P2') | autopsia_manada.py |
| 104 defensas, 0 iniciaciones estrictas, 0 golpes entre hermanos (40 partidas, sobre lo registrado; ver la fila de cobertura en la sección 3) | 918 / 104 / 0 / 0 | 66_manada2; VERIFICACION_66.md | manada_campo.py::honor_dos |
| lo que cuesta defender en vida: −20 de mediana, 0 defensores caídos | −20 hp; 0 caídos en 240 tics | 64, 66 | manada_campo.py::precio |
| defender no cuesta más que estar al lado | −14 (defiende) vs −17 (acompaña), 15-12-5, p = 0,70; 32 pares limpios | 67_proteccion | proteccion_pareada.py |
| proteger al cazado: dirección buena, no demostrado | Δhp cazado 0 vs −14, 15-8 y 13-7, p = 0,21 / 0,26 | 67_proteccion | proteccion_pareada.py |
| las seis veces sin defensa: sin golpe posible; tres lo recuperan con el nombre | 0 candidato en 39 tics; 3 de 6 con identidad | 67_proteccion, 68_nombre (P1) | verifica_68.py |
| ninguna pelea acabó con uno de los dos muerto; en casi la mitad el agresor se fue tras ~4 golpes | 74 ventanas: 0 % nos matan; 46 % se va (4 golpes de mediana); 3 % acoso | 68_nombre (E) | desenlaces.py |
| 138 reencuentros en 80 partidas, casi el doble que peleas | 138; 186 % de 74; mediana 1/ep; 51/80 eps | 69_reencuentros | reencuentros.py |
| cuatro segundos y medio entre ida y vuelta | gap mediano 110 tics (24 tics/s) | 69_reencuentros | reencuentros.py |
| más de la mitad: pegó al hermano y viene a por el otro | 53 % | 69_reencuentros (P4) | reencuentros.py |
| caso exacto: 15; él primero 7; nadie 6; una muerte en 138 | 15 / 7 / 6; 1 muerte | 69_reencuentros | reencuentros.py; runs/casos_exactos.json |
| la memoria guarda un asiento, no un individuo: válido mientras dura la partida | slot estable por token durante la partida; sin identificador persistente entre partidas | hechos/hecho_identidad_jugadores.md | — |
| la fila se enciende 13 de 15, siete pasos antes, y no cambia ninguna decisión | 13/15; 7 tics; 0 cambios; magnitud 0,18 (mediana 0,17) | 70_memoria | verifica_70.py |
| daño acumulado de los que vuelven: 52 de mediana, más de 200 | mediana 52, máx 211, mín 8; último golpe 18 | 71_memoria2; runs/casos_exactos.json | — |
| la acción cambia en 8 de 15, y las ocho son dejar de estar quieto y ganar distancia; 0 golpes; 0 cura ni comida abandonada | las 8: acción de partida `noop` (quedarse quieto) → acción nueva `move_W` (un paso); la fila que diverge es F-REENCUENTRO; 0 golpes de 90 acciones revisadas; 0 tics abandonando botín o cura frente a 28 tics ganando distancia. La etiqueta del sello era "distancia/pared": "pared" (interponer un obstáculo) es una de las salidas previstas en el acta 70 ("lo que salga del miedo —distancia, pared, hermana, nada— lo decide el cuerpo") y NO aparece en el registro; las ocho son un paso. "Ganar distancia" es lo medido (P3); "apartarse del que venía" es la lectura del acta, no una comprobación tic a tic de la geometría | 71_memoria2 (P2, P3, P6); 70_memoria (lista previa) | verifica_71.py |
| en qué momento de la escena diverge cada una de las ocho | la acción diverge en la segunda de las seis fotos en seis de los ocho casos, en la tercera en uno y en la sexta en otro; en ninguno en la primera. NOTA DE LECTURA: el índice que imprime el guion es base cero sobre las seis fotos de los tics 300-305, de modo que su "1" es la segunda foto (tic 301). El TEXTO del acta 71 dice "en el primer tic en siete de los ocho casos" y es erróneo en las dos direcciones: si "el primer tic" es la primera foto, ocurre cero veces; si se leyó el 1 del índice como "el primero", serían seis. Manda la tabla, corregida por el recuento | 71_memoria2 (P6); recuento del 9 de septiembre de 2026, dos ejecuciones con tabla idéntica (el banco declara determinismo 3/3) | verifica_71.py |
| en las escenas del que va solo, sin hermano en la partida, decide lo mismo que la temporada anterior | v35 29/29, v36 30/30, v37 32/32 byte a byte | 65, 68, 71 | verifica_65/68/71.py |
| figura 3 (registros) | ereq_b915417a, t1704 / 1706 / 1760; recorte x[16,25] y[15,24]; venda soltada en t1705 en [19,21]; en t1760 la venda no está a la vista de ninguno (el 11 dejó de verla en t1743) → hueca | ficha_figuras.md; md5 9d7c2ab9ee80d3e82b73f138eb70e7af | figuras_paper3.py |
| el que llega: el primero llega con la vida entera y pierde cuarenta después del don | asiento 10: hp 100 en t1680, 1694, 1704, 1705, 1711; golpes de P12 en t1717, t1737, t1757 (−13,2 cada uno) → 86, 73, 60. La frase anterior "pierde catorce por el camino" era errónea: el −14 es la mediana del acta 67, otra magnitud | diario del asiento 10; comprobación del vigilante del 11-sep | — |
| daño por arma: espada 18 y lanza 12 de base × fuerza; arco 14 y dardo 4 fijos; sin pérdida con la distancia; veneno 2/s; este cuerpo 11 / 7 / 14; rival fuerte hasta 20 (19,8 visto) | — | hechos/hecho_dano_armas.md | — |
| alcances: espada 1, lanza 2, arco 8, cerbatana 6 | 1 / 2 / 8 / 6. El alcance de la cerbatana sale del catálogo del mundo, no de medida propia: no se han contado casillas de vuelo de un dardo | hechos/hecho_dano_armas.md | — |

## Sección 5

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| las tres versiones de la escalera deciden igual que la anterior sin hermano en la escena | v35 29/29, v36 30/30, v37 32/32 byte a byte | 65, 68, 71 | verifica_65/68/71.py |
| la versión desnuda decide igual que la histórica, estado a estado sobre seis escenas | v27-pareja vs v27 histórico: 6 escenas (hp 100/60/25 × con/sin hermano), 0 diferencias, 0 filas sociales vivas con el hermano herido delante | 72_ablacion (puerta previa) | — |
| con las filas de la escalera apagadas, el agente pasa las doce pruebas del que va solo | bancos 13-28, interruptores OFF, 12/12 | 72_ablacion | — |
| mismos catorce rivales, asiento por asiento | roster idéntico al 66 | 72_ablacion; REPRO.md | — |
| seis cosas escritas antes de correr | P1 0 defensas; P2 0 dones; P3 respuestas ±30 % y 0 iniciaciones; P4 distancia mayor; P5 moneda sin signo; P6 0 golpes / 0 ataques al hermano | 72_ablacion | — |
| tabla: defensas 0 / 104 | 0 (72) vs 104 (66) | 72_ablacion; 66_manada2 | manada_campo.py::honor_dos |
| tabla: dones 1 / 98 (criterio: soltar venda o ración con el hermano vivo a ≤2) | 1 en 1 ep (72) vs 98 en 13 eps (66) | 72_ablacion | — |
| tabla: respuestas propias 711 / 918; "suben algo menos de un tercio en el recuento crudo, y algo más de una décima parte por tic registrado" | +29 % con filas (−22,5 % sin) en recuento crudo; por tic live registrado 0,007205 (66) vs 0,006445 (72), +12 %; dentro del ±30 % sellado; sin dirección prevista | 72_ablacion; paintball/cobertura_diarios_acta.md | manada_campo.py::honor_dos; cobertura_diarios.py |
| tabla: pegó primero 0 / 0; golpes al hermano 0/0; ataques elegidos 0/0 | 0 / 0 / 0 / 0 | 72_ablacion | manada_campo.py::golpes_entre |
| tabla: distancia mediana 4,24 / 3,61 casillas | 4,24 (72) vs 3,61 (66) | 72_ablacion | — |
| el don único: a los 83 s, hermano a poco más de una casilla y a 60 de vida, soltar raciones, fila del daño del compañero a la mitad | ereq_9c3c18ad, tick 2002 (83,4 s), asiento 11, soltar_rations, hermano hp 60 a 1,4 casillas, S-DANO-PAREJA = 0,50; S-MUERTE-PAREJA también viva en v27 | 72_ablacion; PROMPT_12 (temporada uno, acta 12) | replay fd29a144 |
| si cuidar cuesta puntos: "poco más de tres contra poco más de dos y medio", mediana igual, caen juntas el mismo número de partidas | score medio 3,12 (72) vs 2,65 (66); mediana colocación 12 vs 12; kills 10 vs 9; mejor de los dos en top-4: 8 (20 %) vs 5 (12 %); ambas ≥13: 11 vs 11; una en pie entre las 8 últimas: 14 vs 12 | 72_ablacion (P5) | — |
| "por debajo de lo que la prueba puede distinguir" | criterio R12 de la casa: 40 partidas sin emparejar | 72_ablacion; varas | — |

## Sección 6

| afirmación del cuerpo | cifra exacta | acta / fuente | guion |
|---|---|---|---|
| medio punto de diferencia en el marcador no se ve | 3,12 vs 2,65 (Δ 0,47), 40 partidas sin emparejar | 72_ablacion (P5) | — |
| defender no cuesta más que estar al lado: no se vio diferencia en 32 pares | −14 vs −17, p = 0,70 | 67_proteccion | proteccion_pareada.py |
| el hermano defendido sale mejor parado: dirección buena, no demostrado | Δhp 0 vs −14, p = 0,21 / 0,26 | 67_proteccion | proteccion_pareada.py |
| la memoria: quince situaciones reales, siete casos por serie | 15 casos exactos sobre 80 partidas (64+66) | 69, 70, 71 | reencuentros.py; verifica_70/71.py |
| defender costó veinte de vida de mediana | −20 hp; 0 caídos | 64, 66 | manada_campo.py::precio |
| con las filas encendidas respondió MÁS a quien le pegaba a él | 918 vs 711 (+29 % con filas); dirección no prevista; dentro del ±30 % sellado | 72_ablacion | manada_campo.py::honor_dos |
| último en pie 5 de 240 (2 sin matar); liga pública 4 de 72 (1 sin matar) | 5/240; 2; 4/72; 1 | hechos/hecho_v19_campeona.md; hechos/hecho_liga_publica.md | — |
| los dos caen en los puestos de cola en 11 de 40 | ambas ≥13: 11 (66) y 11 (72) | 66, 72 | — |
| dos manos: [Manel] / [impl] por constante | tabla de signos v37 con etiquetas | codigo/appraisal_zs_v37.py; tabla_signos_zero_sum_en_curso | — |
| ablación de motor no hecha | — | trabajo futuro | — |
| a 16 de vida lo mata un espadazo fuerte (19,8) y no una flecha (14); a 12, los dos | 19,8 / 14 | hechos/hecho_dano_armas.md | — |
| memoria de una posición: asiento válido solo en la partida; veneno sin autor; camuflado fuera de la lista | slot; "poison"; camuflaje | hechos/hecho_identidad_jugadores.md | — |
| tres de ocho vendas recogidas, las tres por el que estaba peor; ninguna llegó a curar | 3 de 8 recogidas (por evento de recogida); 0 de 3 curas completadas — canal cortado por un golpe en `ereq_3f9b199e` (P14, t1172, 15 → 2) y en `ereq_a62f7c2d` (P2, t2477, 23 → 10), y muerte dentro del canal en `ereq_9fab619d` (t2436, 24 de 48 tics); los tres murieron con la venda del hermano en la mochila. La única cura completada de las ocho escenas es la de `ereq_b915417a`, y fue con la venda propia, no con el don | hechos/forense_dones_venda.md; recuento por eventos del 10-sep en hechos/forense_dones_venda_addendum.md | — |
| reloj de la cura: casi dos segundos sin poder reintentar | veto hasta 41 tics (1,7 s) | hechos/forense_dos_vendas.md | — |
| soltar vacía la ranura: salen las dos vendas | pila de 2 en una ranura | hechos/forense_dos_vendas.md | — |

## Sección 7

No trae cifras propias: las que reaparecen remiten a la fila donde ya
están, y se dicen aquí para que se vea que no hay ninguna suelta.

| afirmación del cuerpo | dónde está su fila |
|---|---|
| último en pie cinco de doscientas cuarenta y cuatro de setenta y dos | sección 6, fila "último en pie 5 de 240 … 4 de 72" |
| seis dones con margen claro y dos empates con el número viejo (decía 67) | sección 4, filas "seis vendas por margen claro…" y "'ocho vendas'…" |
| ocho de quince, y las ocho dejar de estar quieto y ganar distancia | sección 4, fila "la acción cambia en 8 de 15…" |
| dieciséis renglones que se pueden leer | sección 3, fila "la fila de la vida…"; tabla de signos v37 |
| de ocho decisiones, cero cambios (el parte que no cambiaba nada) | sección 4, fila "de ocho decisiones, el parte cambió cero" |

## Lo que queda por cerrar

Dos cosas. La primera no sostiene ninguna afirmación del cuerpo: el pie
de una figura de la sección 5, si se añade; la repetición del contraste
(`eda0b7d3`) no se ha visto, y hasta verla no se describe. La segunda sí
toca al cuerpo, y está dicha en las secciones 3 y 6: si el servidor de
la plataforma conserva el diario entero de las partidas cortadas.
Comprobarlo exige pedir de nuevo los diarios de un episodio, y no se ha
hecho; si se hiciera y estuvieran, los recuentos podrían completarse y
las ausencias comprobarse sobre las partidas enteras.

## Nota sobre "distancia o pared"

La etiqueta apareció dos veces en el cuerpo — en 4.4 y en la sección 7 —
y no describe lo que hay en el registro. Venía de una lista escrita antes
de mirar, en el acta del peldaño anterior, donde se dejó dicho que "lo
que salga del miedo —distancia, pared, hermana, nada— lo decide el
cuerpo" (el acta, escrita antes de fijar el vocabulario, dice
"hermana"). Lo que salió fueron ocho pasos: en las ocho situaciones el
agente pasó de quedarse quieto a moverse ganando distancia, y en ninguna
interpuso un obstáculo. Las dos apariciones están corregidas.

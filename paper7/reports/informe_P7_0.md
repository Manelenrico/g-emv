# P7-0 · El inventario de las cosas: qué hay en el mundo, cómo lo conoce el cuerpo y cuánto se lo encuentra

*3-oct-2026. Coste cero: sin partidas, sin llamadas a la consola (plataforma 0; consola 0). Solo lectura y medida. `motor/model.py` =
`1e511978c251130e95169ebf8443efa1` al principio y al final (comprobado); `CONGELADO.md` y `CONGELADO_P6.md` sin tocar; el cuerpo no se toca.
Scripts: `cantera/paper7/mide_P7_0.py` (recorre los 80 diarios A4 del seis, uno a uno, registro a registro; escribe `P7_0_medidas.json`) y
`escribe_informe_P7_0.py` (este informe, cifras leídas del JSON). Diarios: las 40 semillas de A4 del seis = P611_t1 y P611_t2 (las 20 de
P6-23) + P624_t1 (las 20 nuevas de P6-24), 2 asientos por partida = **80 vidas** (`mide_P7_0.py:34-39`, `informe_P6_24.md:87`).
Mundo 0.1.19: `cantera/paper6/liga/v2_coworlds_cow_6a55df20-08d1-4e4c-adba-33dbd97e1e6f.json` ("version": "0.1.19"), `informe_P6_1.md:125-131`,
`informe_P6_12.md:42`. Las vidas duran 13.008 tics de mediana (p10 12.389, p90 14.698); el aviso de la fase 5 del anillo llega en el 11.856 (`player_config.zone_schedule[4]`).*

Definiciones de medida (ver, coger, usar, soltar, dar, atacar, ventana del uso): en la cabecera de `mide_P7_0.py:1-25`. Resumen: lo
visto sale de `ve_items` (id, n, pos) de cada registro `tick`; lo cogido se infiere del inventario del tic siguiente (el diario no apunta
qué se cogió); lo usado es `pack[slot]` del tic del `use`, confirmado por lo que sigue (canal, mano o cuerpo); `action_result` del tic t es
el resultado de la acción emitida en t−1 (comprobado en `P611_t1_A4_20260916/10`, tics 592-594).

## 1 · Las cosas del mundo (0.1.19)

El catálogo llega en el `player_config` y el diario lo copia entero en el registro `k="catalogo"` (`policy_cortex.py:904` lo vuelca al
recibirlo; `mundo.py:76-85` lo lee campo a campo). Los 80 diarios traen **un solo catálogo** (md5 del JSON ordenado:
`75af310fcf375a72c6bff0d2f0f93e11`, 1 distinto): **12 tipos de objeto**. Fuera del catálogo, en las observaciones solo aparecen
arbustos (`ve_bushes`, con `charges`) y las manos vacías (`hand.id = "none"`); ningún `ve_items[].id` fuera del catálogo
(0 ids desconocidos). Los "cajones" de la wiki no son un objeto: son objetos del catálogo en el suelo.

| id | kind | daño | alcance | cooldown | durabilidad | pila máx. | canal (tics) | cura | tics a la vista (80 vidas) | montones distintos | en manos o cuerpo ajenos (asientos·vidas) | regalos de patrocinador vistos (míos) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `sword` (espada) | ikMelee | 18 | 1 | 18 | 40 | 1 | 0 | 0 | 740.729 | 211 | 126 | 0 (0) |
| `spear` (lanza) | ikMelee | 12 | 2 | 20 | 40 | 1 | 0 | 0 | 477.301 | 190 | 168 | 0 (0) |
| `bow` (arco) | ikRanged | 14 | 8 | 18 | 0 | 1 | 0 | 0 | 330.037 | 105 | 41 | 0 (0) |
| `knives` (cuchillos) | ikThrown | 8 | 5 | 10 | 0 | 8 | 0 | 0 | 611.522 | 267 | 201 | 0 (0) |
| `blowgun` (cerbatana) | ikRanged | 4 | 6 | 24 | 0 | 1 | 0 | 0 | 446.371 | 115 | 53 | 0 (0) |
| `net` (red) | ikThrown | 0 | 3 | 30 | 0 | 2 | 0 | 0 | 314.424 | 163 | 87 | 0 (0) |
| `first_aid` (botiquín) | ikConsumable | 0 | 0 | 0 | 0 | 2 | 48 | 50 | 1.008.929 | 699 | 0 | 584 (39) |
| `rations` (raciones) | ikConsumable | 0 | 0 | 0 | 0 | 5 | 24 | 15 | 947.435 | 684 | 0 | 619 (40) |
| `backpack` (mochila) | ikGear | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 122.019 | 155 | 167 | 0 (0) |
| `camouflage` (camuflaje) | ikGear | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 296.587 | 105 | 55 | 0 (0) |
| `arrows` (flechas) | ikAmmo | 0 | 0 | 0 | 0 | 12 | 0 | 0 | 630.204 | 315 | 0 | 0 (0) |
| `darts` (dardos) | ikAmmo | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 657.857 | 260 | 0 | 0 (0) |
| arbusto de bayas | (terreno `B`, `ve_bushes` con `charges`) | – | – | – | – | – | – | – | – | 150 posiciones | – | – |
| manos vacías | `hand.id = "none"`; la wiki dice 5 de daño (`v2_wikis_zero-sum_pages_main.md:45`); el cuerpo las modela aparte (§ 2) | | | | | | | | 271.523 tics con la mano vacía | | | |

Fuentes: columnas del catálogo = registro `catalogo` de cualquier diario (igual en los 80); tics a la vista y montones = `mide_P7_0.py`
(`ve_tics`, `montones`); manos/cuerpo ajenos = `ve_agentes[].hand/body` (asientos distintos por vida, sumados); regalos = eventos
`gift_landed` (`eventos[].type`), que solo traen botiquines y raciones.

**Coger, usar, soltar, dar.** Las acciones que el cuerpo sabe emitir son seis, y están escritas en `decisor_zs.py:934-959`: `none`, `move`,
`pickup` (sin argumento: coge lo que hay en la casilla), `use` (con `slot` = índice del `pack`), `drop` (con `slot`) y `attack` (con
`dir`). **No existe `give`**: ni en el decisor ni en la wiki; lo más parecido es soltar junto al hermano, que es como el cuerpo "da"
(`decisor_zs.py:496-521`, S-PROVISION). Qué hace `use` según el objeto, **observado en los diarios** (no leído del código del juego):
consumible → abre un canal (`effects[] = channeling/item/done_tick`); arma en el zurrón → la intercambia con la mano; prenda en el zurrón →
la viste (`body`). El cuerpo nunca ha emitido `use` sobre red, flechas ni dardos, así que no sabemos desde nuestro lado qué haría.
`pickup` sobre una prenda con el cuerpo vacío la viste directamente (comentado en `decisor_zs.py:547-553` citando `sim.nim:735`, que no
está en este repositorio). Los arbustos: el cuerpo no tiene acción de forrajear y en 80 vidas no hay ni una recogida en casilla de arbusto
(0 cogidas, 0 intentos fallidos allí); cómo se forrajea es pregunta para Ari.

| objeto | ¿se puede coger? | ¿usar? | ¿soltar? | ¿dar? | de dónde sale |
|---|---|---|---|---|---|
| espada, lanza, arco, cuchillos, cerbatana | sí (cogidos en los diarios: 33, 14, 25, 124, 20) | `use` = empuñar desde el zurrón (14, 3, 8, 4, 4 confirmados); `attack` con el arma en mano (163, 53, 1.521, 46, 749 ataques) | `drop` existe; 0 soltadas de armas en los diarios | no hay `give` | `mide_P7_0.py` (coge/usa/ataca); `decisor_zs.py:538-544` (empuñar), `:588-602` (atacar) |
| red | sí (25 cogidas, 23 vidas) | nunca: 0 `use`, 0 `attack` con red en mano (el candidato de atacar exige daño > 0, `decisor_zs.py:588`; la red tiene 0) | 0 soltadas | no | `mide_P7_0.py`; el diario registra `netted` sobre mí (2 episodios), así que alguien sí la lanza |
| botiquín, raciones | sí (240 y 175 unidades) | `use` = canal de 48 / 24 tics (195 y 75 confirmados) | `drop`: 94 y 41 | soltar con el hermano a ≤ 2 casillas: 92 y 27 (proxy declarado) | `mide_P7_0.py`; `decisor_zs.py:483-521` |
| mochila, camuflaje | sí (16 y 30); con el cuerpo vacío, coger = vestir | `use` desde el zurrón = ponerse (5 y 5 confirmados); llevada puesta en 12 y 24 vidas | `drop` existe; 0 en los diarios (ponerse otra tira la anterior al suelo, `decisor_zs.py:831-835`) | no | `mide_P7_0.py` (`tics_puesto`); `decisor_zs.py:559-568` |
| flechas, dardos | sí (228 y 133 unidades) | no se usan: las gasta el arma al atacar (observado: `no_ammo` cuando no hay) | 0 | no | `mide_P7_0.py` (`ataques_resultado`) |
| arbusto | no es objeto; `charges` visibles | sin acción conocida desde nuestro lado | – | – | `ve_bushes`; pregunta para Ari |

**Lo que no se puede saber desde nuestro lado** (el código del juego no es nuestro; los comentarios del decisor citan `sim.nim`, que no está
en el repositorio) y queda como pregunta para Ari: (1) cómo se forrajea un arbusto y qué da; (2) qué hace `use` sobre red, flechas o dardos;
(3) si la red se lanza con `attack` (daño 0) y qué registra el mundo; (4) si `drop` deja el objeto en mi casilla o en la vecina; (5) si hay
alguna acción de dar directa; (6) reglas de apilado al coger (el diario muestra `inventory_full` 58 veces con objeto en la casilla).

## 2 · Cómo conoce el cuerpo cada cosa (cuerpo congelado del seis, `CONGELADO_P6.md`)

El cuerpo no sabe nombres: **lee el catálogo** y clasifica por `kind` (`mundo.py:128-157`): el consumible que más cura es el botiquín y el
resto raciones (`:133-134`); las armas son `ikMelee/ikRanged/ikThrown` y el daño de referencia es el mayor del catálogo (`:136-138`);
la munición, `ikAmmo` (`:139`); mochila y camuflaje se casan por id dentro de `ikGear` (`:143-149`, declarando la ausencia); la red es el
arrojadizo de daño 0 (`:151-157`). Lo que vale cada cosa está en tres sitios: la **riqueza W** (`appraisal_zs_v42_exp.py:717-779`, filas
R-CARENCIA `:1076` con `W_TARGET = 3.0` `:126`), la **previsión** del decisor (`decisor_zs.py:817-856`) y las **filas** que cada objeto
apaga o enciende. Tres casos: (a) efecto escrito; (b) solo deseable o necesario, sin efecto; (c) nada.

| objeto | caso | qué sabe el cuerpo | dónde (archivo:línea) |
|---|---|---|---|
| botiquín (`first_aid`) | **(a)** | cura `heal` del catálogo (50): la previsión de `usar_botiquin` pone `hp2 = min(hp_max, hp + heal)`; conoce el canal (`use_ticks` = 48) y veta volver a usar mientras dura; vale 1,0 de W; su falta enciende R-ACOPIO (0,18) y, con la hermana sin venda, S-PROVISION (0,30) y R-HERMANO-FALTA; la promesa de cogerlo = cuánto apaga R-ACOPIO | `decisor_zs.py:483-493` (candidato con `heal`), `:823-828` (previsión), `:83-93, :102` (canal), `appraisal_zs_v42_exp.py:749` (W), `:939-958` (R-ACOPIO, `ACOPIO_M :111`), `:1312-1362` (S-PROVISION), `:1637-1644`, `decisor_zs.py:642-651` (promesa). **No sabe** que el canal se corta con cualquier daño (§ 4) |
| raciones (`rations`) | **(a)** | cura 15 (misma previsión `usar_racion`), canal 24; W: la 1.ª vale 1,0, la 2.ª 0,3 solo con mochila | `decisor_zs.py:483-493, :823-825`, `appraisal_zs_v42_exp.py:751-759`, `RACION_2A :411` |
| espada, lanza (`ikMelee`) | **(a)** | daño del catálogo × (5+STR)/10 en la previsión de atacar; alcance (`range`) para el candidato; W = daño/18 × durabilidad restante/`durability`; "estar armado" = arma en la mano; empuñar intercambia mano y ranura | `decisor_zs.py:588-602` (candidato), `:852-856` (daño previsto), `:841-845` (empuñar), `appraisal_zs_v42_exp.py:731-738` (W con desgaste) |
| arco, cerbatana (`ikRanged`) | **(a)** para el daño, **(b)** para la munición | daño y alcance del catálogo (14/8, 4/6); W = daño/18 × min(1, munición/8); **el candidato de atacar no mira la munición** (no hay `ammo` ni `municion` en `decisor_zs.py`): de 1.521 ataques con arco, 1.393 devolvieron `no_ammo`; con cerbatana, 702 de 749. **No sabe** que los dardos envenenan | `appraisal_zs_v42_exp.py:739-744`, `AMMO_REF :414`; `decisor_zs.py:588-602`; `mide_P7_0.py` (`ataques_resultado`) |
| cuchillos (`ikThrown`, daño 8) | **(a)** | daño y alcance; W = 8/18 × min(1, n/8) (los propios cuchillos cuentan como munición) | `appraisal_zs_v42_exp.py:739-744`, `decisor_zs.py:852-856` |
| flechas, dardos (`ikAmmo`) | **(b)** | solo cuentan en W como munición del arma en mano; ningún efecto propio; no condicionan atacar | `appraisal_zs_v42_exp.py:740-741`, `mundo.py:139` |
| red (`net`, arrojadizo de daño 0) | **(b)** | vale 0,25 de W (`GEAR_MENOR_W`) en mano o en el zurrón; **ningún efecto** (no sabe que inmoviliza) y **no puede lanzarla** (atacar exige daño > 0) | `mundo.py:151-157`, `appraisal_zs_v42_exp.py:765-768`, `:413`; `decisor_zs.py:588` |
| camuflaje (`camouflage`) | **(a)** | efecto escrito **a mano desde la wiki**, no del catálogo: invisible a más de 4 casillas quieto / 7 moviéndose, revelado 5 s tras atacar (S-8-EXPOSICIÓN); vale 0,25 de W; la promesa de cogerlo = cuánto apaga S-8; ponerse = vestir en el acto | `appraisal_zs_v42_exp.py:405-410` (`CAMO_QUIETO/MOVIENDO/REVELADO_S`), `:1386-1416` (S-8), `:763-764` (W); `decisor_zs.py:672-676` (promesa), `:559-568, :831-839` (ponerse) |
| mochila (`backpack`) | **(a)** parcial | sabe que da las ranuras 2-3 (al quitársela, el zurrón previsto vuelve a 2) y que permite la 2.ª ración; vale 0,5 de W mientras quede apetito; la promesa = cuánto sube W. No sabe nada más | `decisor_zs.py:831-839`, `:677-680`; `appraisal_zs_v42_exp.py:753-758, :770-776` (`MOCHILA_W :412`) |
| arbusto de bayas | **(b)** | es un sitio de botín de nivel 0,07 (`VALOR_NIVEL["bayas"]`) para R-LLAMADA mientras tenga `charges`; no sabe qué da ni cómo se forrajea; no hay candidato de forrajear | `appraisal_zs_v42_exp.py:147-149`, `:694-697`, `:1082-1088`, `decisor_zs.py:707-724` |
| manos vacías | **(a)** virtual | el cuerpo no tiene puñetazo (atacar exige arma con daño); para la **amenaza ajena** inventa dos armas virtuales: `~manos` (daño 3, alcance 1) para todo hostil con la mano vacía y `~manos_pegando` (daño 18) si me pega | `amenaza11_P6_11.py:28-31, :53, :64-68` (`DANO_MANOS`), `decisor_zs.py:588` |
| veneno (efecto) | **(a)** sobre mí, **(c)** como causa | F-DAÑO × 1,5 mientras `effects[] = poison`; no sabe qué lo causa ni que bloquea el botiquín | `appraisal_zs_v42_exp.py:51`, `:870-874` |
| red sobre mí (`netted`) | **(c)** | no aparece en el cuerpo (0 menciones de `netted` en decisor y appraisal) | grep en `decisor_zs.py`, `appraisal_zs_v42_exp.py` |
| armas ajenas (E por arma) | **(a)** del catálogo | la amenaza del hermano y la propia usan `damage` y `range` del catálogo del arma en la mano del rival; la memoria aprendida (p95) **no se carga** en A4 (`MIEDO_ON = False`) | `appraisal_zs_v42_exp.py:1578-1592`, `:379-396`; `policy_cortex.py:93-96`; `CONGELADO_P6.md` (notas) |
| recursos oídos (parte E2) | **(b)** | el parte del hermano trae los objetos que ve como letras del catálogo; el oyente los inyecta en la observación mientras pesan ≥ 0,30 (≤ 86 tics) | `parte2.py:76-81`, `oyente2.py:64, :142-152` |

Qué habría que quitar para que el cuerpo "no sepa" una cosa (hechos, no recomendación): el **efecto** de un consumible vive en una sola línea
(`decisor_zs.py:824`, `hp + receta["heal"]`, con `heal` tomado del catálogo en `:490-493`); el **valor** (deseo) vive en `riqueza_W`
(`appraisal_zs_v42_exp.py:749-776`) y en las filas que lo citan (R-ACOPIO `:939-958`, S-PROVISION `:1312-1362`, R-HERMANO-FALTA
`:1637-1644`, promesas `decisor_zs.py:642-680`); el **efecto del camuflaje** vive en `:405-410` y `:1386-1416`; el de la **mochila** en
`decisor_zs.py:831-839` y `appraisal_zs_v42_exp.py:753-758`; el **daño de las armas** en `decisor_zs.py:852-856` y `appraisal_zs_v42_exp.py:735`.

## 3 · Cuánto se las encuentra (A4, 80 vidas; mediana / p10 / p90 por vida)

| objeto | vidas que lo ven | montones distintos vistos | unidades cogidas (vidas con ≥ 1) | usos confirmados (vidas) | tics hasta el primer encuentro | tics hasta la primera cogida | tics hasta el primer uso |
|---|---:|---|---|---|---|---|---|
| espada | 80 | 3 / 2 / 4 | 0 / 0 / 1 (32) | 0 / 0 / 1 (14) | 570 / 537 / 681 (n 80) | 867 / 614 / 11.462 (n 32) | 1.122 / 710 / 12.567 (n 14) |
| lanza | 79 | 2 / 1 / 4 | 0 / 0 / 1 (14) | 0 / 0 / 0 (3) | 559 / 1 / 605 (n 79) | 818 / 602 / 8.720 (n 14) | 760 / 750 / 1.619 (n 3) |
| arco | 79 | 1 / 1 / 2 | 0 / 0 / 1 (25) | 0 / 0 / 0 (8) | 570 / 548 / 869 (n 79) | 2.229 / 651 / 13.658 (n 25) | 2.292 / 1.476 / 9.731 (n 8) |
| cuchillos | 79 | 3 / 1 / 6 | 0 / 0 / 6 (21) | 0 / 0 / 0 (4) | 2 / 1 / 614 (n 79) | 1.571 / 537 / 10.901 (n 21) | 3.540 / 1.362 / 8.125 (n 4) |
| cerbatana | 80 | 1 / 1 / 2 | 0 / 0 / 1 (20) | 0 / 0 / 0 (4) | 581 / 548 / 716 (n 80) | 1.426 / 635 / 11.885 (n 20) | 1.572 / 674 / 2.736 (n 4) |
| red | 80 | 2 / 1 / 3 | 0 / 0 / 1 (23) | 0 / 0 / 0 (0) | 548 / 1 / 940 (n 80) | 626 / 592 / 8.102 (n 23) | – (n 0) |
| botiquín | 80 | 8 / 5 / 12 | 2 / 0 / 6 (62) | 1 / 0 / 8 (47) | 564 / 1 / 603 (n 80) | 682 / 592 / 4.861 (n 62) | 11.569 / 3.408 / 12.918 (n 47) |
| raciones | 79 | 8 / 5 / 12 | 2 / 0 / 4 (44) | 0 / 0 / 3 (36) | 1 / 1 / 1.953 (n 79) | 1.612 / 504 / 10.577 (n 44) | 10.392 / 2.418 / 12.609 (n 36) |
| mochila | 64 | 2 / 0 / 4 | 0 / 0 / 1 (12) | 0 / 0 / 0 (2) | 532 / 1 / 12.502 (n 64) | 1.034 / 505 / 13.642 (n 12) | 7.460 / 2.318 / 12.602 (n 2) |
| camuflaje | 79 | 1 / 1 / 2 | 0 / 0 / 1 (25) | 0 / 0 / 0 (2) | 571 / 548 / 717 (n 79) | 1.188 / 623 / 9.905 (n 25) | 7.444 / 2.280 / 12.607 (n 2) |
| flechas | 79 | 4 / 2 / 7 | 0 / 0 / 12 (21) | 0 / 0 / 0 (0) | 482 / 1 / 592 (n 79) | 1.795 / 604 / 12.870 (n 21) | – (n 0) |
| dardos | 80 | 3 / 1 / 6 | 0 / 0 / 8 (17) | 0 / 0 / 0 (0) | 559 / 1 / 681 (n 80) | 1.198 / 589 / 10.020 (n 17) | – (n 0) |
| arbusto de bayas | 74 | 2 / 1 / 3 | 0 / 0 / 0 (0) | 0 / 0 / 0 (0) | 1 / 1 / 2 (n 74) | – (n 0) | – (n 0) |

Lectura: "montones" = pares (id, posición) distintos a lo largo de la vida; "unidades cogidas" cuenta el `n` ganado en el inventario
(una pila de 2 botiquines = 2); "usos confirmados" = `use` seguido del canal (consumibles), de la mano (armas) o del cuerpo (prendas);
para las armas, los **ataques** van en el § 4. Los tics cuentan desde el tic 1 (la cuenta atrás; la ignición es el 480): casi todo se ve
desde el pedestal o en el primer minuto. Fuente: `mide_P7_0.py` → `P7_0_medidas.json["resumen"]["por_objeto"]`. Fallos de `pickup`:
2.529 (`no_target` 2.471, `inventory_full` 58).

## 4 · Lo que pasa al usarlas

**Qué registra el diario en el tic de usar** (registro `k="tick"`, campos leídos en `mide_P7_0.py:57-146`): la acción emitida
(`intencion`: `do`, `slot`), el inventario **antes** (`hand` con `durability` o `n`, `pack[slot] = {id, n}`, `body`), `hp`, `effects[]`
(`channeling` con `item` y `done_tick`; `poison`; `netted`; `camo_revealed`), `damage_taken[]` por tic (`source`: `zone`, `poison` o el
asiento `P<n>`; `amount`), `damage_dealt` y `kills` acumulados, `action_result` (de la acción anterior), la zona, lo visible, y la
`RADIOGRAFIA` del decisor (candidatos con su d y el `elegido`: en los 270 usos de consumible el elegido fue siempre `usar_botiquin` /
`usar_racion`). El inventario **después** está en el registro siguiente. **Qué no registra:** qué objeto cogió un `pickup` (se infiere del
inventario), cuánto curó un canal (se infiere de `hp`), por qué se canceló, a quién alcanzó un ataque (solo el acumulado `damage_dealt`),
si otros me ven (el camuflaje no es medible desde aquí), el hp exacto del hermano (solo `hp_band`; el parte E2 lo trae cada 25 tics).
**No hay hambre** en este mundo: ni la observación ni la wiki tienen tal variable; las raciones son solo vida (+15).

**Ventana declarada:** desde el tic t del `use` hasta t_fin = `done_tick` + 1 (= t + canal + 1: 48 tics el botiquín, 24 las raciones).
delta_neto = hp(t_fin) − hp(t) + daño recibido en (t, t_fin]. Completado = el `n` del objeto baja en t_fin; cancelado = no baja.

| consumible | usos confirmados | completados | cancelados | sin cerrar | en la fase 5 o después |
|---|---|---|---|---|---|
| botiquín | usos confirmados 195 | completados 64 (delta_neto mediana 30,0, mín -0,4, máx 50,0; hp antes mediana 63) | cancelados 116 (delta_neto mediana 0,1; con daño en la ventana 116 de 116) | sin cerrar (muere antes) 15 | en la fase 5 o después (t ≥ 11.856): 124 usos, 29 completados |
| raciones | usos confirmados 75 | completados 71 (delta_neto mediana 13,6, mín -0,4, máx 15,6; hp antes mediana 89) | cancelados 1 (delta_neto mediana 13,0; con daño en la ventana 0 de 1) | sin cerrar (muere antes) 3 | en la fase 5 o después (t ≥ 11.856): 29 usos, 25 completados |

El botiquín cura lo que dice el catálogo cuando el canal acaba (delta
máximo 50, acotado por el hp máximo), pero **el canal se corta con cualquier daño**: los 116 cancelados llevan todos daño dentro de
la ventana, casi todo del fuego del anillo (radio de la zona al cancelarse: 5 → 56, 8 → 20, 11 → 12, 7 → 8). El cuerpo no sabe esto
(§ 2): vuelve a emitir `use` cada 49 tics y arde (ejemplo: `P611_t1_A4_20260916/10`, tics 12.289, 12.338, 12.387…, hp 93 → 80 → 67 → 54).
Una ración cancelada que sí curó 13 (`P611_t1_A4_20470374/10`, t 12.021): el `n` no bajó en la ventana; probablemente una recogida en medio.

**Prendas.** Mochila: con `body = backpack` el `pack` tiene siempre 4 ranuras (87.242 tics) y 2 sin ella: medible. Camuflaje: puesto
259.529 tics en 24 vidas; su efecto (que no me vean) **no es medible desde nuestro lado**; el diario sí registra `camo_revealed`
(7.910 tics). **Red:** 0 lanzamientos propios; sobre mí, 2 episodios `netted` de 71 tics (≈ 3 s), con 41 hp perdidos de mediana
mientras duraban. **Veneno** (dardos ajenos): 8 episodios en 6 vidas, 143 tics de mediana (p90 167), 10 hp perdidos de mediana;
`damage_taken.source = "poison"`: 45 pulsos, 90 hp en total (2 por pulso, como dice la wiki).

**Armas** (`attack` con el arma en mano; golpe = `damage_dealt` sube en t+1; resultado = `action_result` de t+1):

| arma | ataques | `ok` | `no_ammo` | golpes | vidas que atacan | tics hasta el primer ataque (med / p10 / p90) | tics con el arma en mano |
|---|---:|---:|---:|---:|---:|---|---:|
| espada | 163 | 159 | 0 | 159 | 26 | 10.960 / 8.882 / 12.564 (n 26) | 314.579 |
| lanza | 53 | 52 | 0 | 52 | 7 | 10.304 / 3.044 / 11.293 (n 7) | 87.148 |
| arco | 1.521 | 128 | 1.393 | 75 | 17 | 10.380 / 1.973 / 12.879 (n 17) | 173.514 |
| cuchillos | 46 | 46 | 0 | 31 | 9 | 9.376 / 2.013 / 11.120 (n 9) | 59.715 |
| cerbatana | 749 | 47 | 702 | 33 | 11 | 10.504 / 2.198 / 11.809 (n 11) | 105.049 |
| red | 0 | 0 | 0 | 0 | 0 | – (n 0) | 34.156 |

Las manos vacías no atacan nunca (0 ataques: el candidato no existe sin arma). El daño recibido por fuente en las 80 vidas: anillo
6.063 hp en 835 golpes; rivales (fuentes `P<n>`) 3.730 hp en 522 golpes; veneno 90.

**La tercera columna ("lo que pasó").** Con lo que guardamos ya se calcula: para consumibles, hp antes/después y si el canal acabó;
para prendas, el cuerpo y el tamaño del zurrón; para armas, si el ataque se aplicó (`ok`/`no_ammo`/`no_target`) y si hizo daño
(`damage_dealt`); para el veneno y la red sobre mí, duración y hp. **Habría que guardar además**, si se quiere sin inferir: el id de lo
cogido en cada `pickup`, un evento del mundo por uso (objeto, resultado, cantidad curada, motivo de cancelación), el objetivo y el daño de
cada ataque, y el `durability` del arma en cada golpe (está en `hand`, pero no se liga al golpe). Nada de esto lo da hoy el mundo en la
observación: es pregunta para Ari si existe en el protocolo.

## 5 · Los objetos del piloto de Ari

Camuflaje, red y mochila **existen en 0.1.19** con esos ids (`camouflage`, `net`, `backpack`) en el catálogo de los 80 diarios. Sus
puntos 2-4 están en las tablas: el cuerpo conoce el camuflaje con efecto escrito a mano (§ 2), lo lleva puesto en 24 vidas
(30 cogidas; primer encuentro a 571 tics de mediana) y su efecto no es medible desde aquí (§ 4); la red la
conoce solo como valor 0,25 sin efecto, la coge en 23 vidas y no la lanza nunca; la mochila la conoce como ranuras
y valor 0,5, la lleva en 12 vidas y su efecto (2 → 4 ranuras) es medible y se ve.

## 6 · Cuántos usos por vida (para que la mesa calcule partidas)

| objeto | usos completados en 80 vidas | por vida | vidas con ≥ 1 | p90 por vida |
|---|---:|---:|---:|---:|
| botiquín (canal acabado) | 64 | 0,80 | 39 | 2,0 |
| raciones (canal acabado) | 71 | 0,89 | 35 | 3,0 |
| espada (golpes que hacen daño) | 159 | 1,99 | 26 | 6,1 |
| lanza (golpes que hacen daño) | 52 | 0,65 | 7 | 0,0 |
| arco (golpes que hacen daño) | 75 | 0,94 | 13 | 5,0 |
| cuchillos (golpes que hacen daño) | 31 | 0,39 | 8 | 0,1 |
| cerbatana (golpes que hacen daño) | 33 | 0,41 | 8 | 0,1 |
| mochila (vidas que la llevan puesta) | 12 | 0,15 | 12 | – |
| camuflaje (vidas que la llevan puesta) | 24 | 0,30 | 24 | – |
| red (lanzamientos) | 0 | 0 | 0 | – |

Fuente: `P7_0_medidas.json["resumen"]["por_objeto"][id]["usos_completados" | "golpes"]`, `tics_puesto` por vida.

## Objetos conocidos a los que se podría quitar lo que el cuerpo sabe de ellos (solo hechos)

| objeto | lo que hoy sabe | dónde está escrito | usos por vida hoy (§ 6) |
|---|---|---|---|
| botiquín | cura 50 (catálogo), canal 48, valor 1,0 de W, filas de acopio y provisión | `decisor_zs.py:490-493, :824`; `appraisal_zs_v42_exp.py:749, :939-958, :1312-1362` | 0,80 |
| raciones | cura 15, canal 24, valor 1,0 (+0,3 la 2.ª con mochila) | `decisor_zs.py:490-493, :824`; `appraisal_zs_v42_exp.py:751-759` | 0,89 |
| espada, lanza | daño y alcance (catálogo), desgaste, valor daño/18 | `decisor_zs.py:588-602, :852-856`; `appraisal_zs_v42_exp.py:731-738` | 2,64 |
| arco, cerbatana, cuchillos | daño y alcance; valor con munición | `decisor_zs.py:588-602, :852-856`; `appraisal_zs_v42_exp.py:739-744` | 1,74 |
| camuflaje | radios 4 / 7 y revelado 5 s (a mano, de la wiki); valor 0,25; promesa | `appraisal_zs_v42_exp.py:405-410, :1386-1416, :763-764`; `decisor_zs.py:672-676` | puesto en 24 de 80 vidas |
| mochila | ranuras 2-3; 2.ª ración; valor 0,5; promesa | `decisor_zs.py:831-839, :677-680`; `appraisal_zs_v42_exp.py:753-758, :770-776` | puesta en 12 de 80 vidas |
| red | solo valor 0,25; sin efecto; no se lanza | `appraisal_zs_v42_exp.py:765-768`; `mundo.py:151-157` | 0 |
| flechas, dardos | solo munición en W | `appraisal_zs_v42_exp.py:740-744` | – |
| arbustos | nivel de botín 0,07 | `appraisal_zs_v42_exp.py:147-149, :694-697` | 0 recogidas |

## Preguntas para Ari (lo que no se sabe desde nuestro lado)

1. Cómo se forrajea un arbusto (`ve_bushes.charges`) y qué objeto da; ¿es `pickup` en la casilla?
2. Qué hace `use` sobre red, flechas y dardos; si la red se lanza con `attack` y cómo se registra (daño 0).
3. Si `drop` deja el objeto en la casilla propia; si existe alguna acción de dar directa; reglas de apilado y de `inventory_full`.
4. Si el protocolo puede devolver, por tic, el id de lo cogido, el resultado de un canal (curado, cancelado y por qué), y el objetivo y
   daño de cada ataque; hoy se infieren.
5. Si el canal del botiquín se cancela con **cualquier** daño, incluido el del anillo (lo observado: 116 de 116 cancelaciones con daño en la ventana).
6. Si la fuente del juego (`sim.nim`, citada en los comentarios de `decisor_zs.py`) que describe `resolvePickup` y `use` sigue vigente en 0.1.19.

## Archivos

| archivo | qué es |
|---|---|
| `cantera/paper7/mide_P7_0.py` | la medida sobre los 80 diarios (definiciones en su cabecera); `mide_P7_0.log` su salida |
| `cantera/paper7/P7_0_medidas.json` | por vida: visto, cogido, usado, soltado, atacado, prendas, fuentes de daño, episodios; resumen por objeto |
| `cantera/paper7/escribe_informe_P7_0.py` | escribe este informe desde el JSON |
| `cantera/paper7/informe_P7_0.md` | este informe |

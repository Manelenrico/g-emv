# P7-3 · Saber no basta, por qué: la fuga entre vidas, el techo, las opciones en la pelea y el botiquín caso a caso

*3-oct-2026. Coste cero (plataforma 0; consola 0). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al empezar y al acabar; congelados y
cuerpo sin tocar. Sello: `SELLO_P7_3.md`, commit 9681ab7, md5 `60c9c08c1f862e2f8164ba168fd81146`, antes de calcular. Mismos 80 diarios de A4 y misma réplica que
P7-2 (`banco_P7_2.py`, un proceso por vida). Scripts: `banco_P7_3.py` (techo → `P7_3_techo.json`, `P7_3_banco_techo.json`), `fuga_P7_3.py`
(sondas de la fuga → `fuga_P7_3.json`), `escribe_informe_P7_3.py` (este informe). Fontanería del banco del techo: 2450 de 2450 decisiones
iguales al diario con la creencia del catálogo.*

## Sección 1 · La fuga entre vidas

**Qué pasa de una vida a la siguiente.** `policy_pareja._envuelve(alma)` (`cantera/paper6/policy_pareja.py:99-134`) instala dos envoltorios
"desde fuera": uno sobre la voz (`PC.PARTE.emite`, `:103-117`) y otro sobre los candidatos del decisor (`D.candidatos`, `:121-134`). El de
los candidatos captura lo que `D.candidatos` vale en ese momento (`:121`, `_orig_cands = D.candidatos`) y lo sustituye por `_cands`
(`:134`), que lleva atada la criatura (`_a=alma`, `:122`) y veta todo candidato cuyo `objetivo` sea un rival **contado** por ella
(`_a._contados`, `:125-131`; el conjunto lo escribe cada tic `AlmaPareja` en `:92` desde `oyente2.slots_contados`). Se crea una vez por
vida: en el campo, en `run()` (`:150`; en A4, `policy_pareja11.py:69`); en los bancos, al arrancar cada réplica. **No se reinicia nunca**:
el módulo `decisor_zs` guarda el `D.candidatos` envuelto, y la siguiente llamada a `_envuelve` lo captura como "original" y le pone otra
capa encima. En un proceso con varias vidas, `D.candidatos` es una cadena de capas, una por vida, y cada capa sigue vetando con el
`_contados` de **su** criatura, que al acabar su vida queda congelado con los últimos rivales contados. Así desaparecen los candidatos
`atacar_*` cuyo objetivo era un rival contado en una vida anterior: lo visto en P7-2 (defensa del hermano) y en el barrido de
`fuga_P7_3.py`, que corre las vidas en orden en un solo proceso: la tercera vida ya pierde fidelidad (160 de 174; la sonda en el
primer tic infiel, t 11976, muestra al rival en la memoria de agresores y ningún `atacar_*` entre los candidatos). Comprobación directa: con
las mismas tres vidas en un proceso, restaurando `D.candidatos` y `PC.PARTE.emite` a su valor base antes de cada `_envuelve`, la
tercera vida da 174 de 174 y, sin restaurar, 160 de 174 (`fuga_prueba_P7_3.py`, con y sin `restaurar`).
`filas10_P6_10.py:68-84` (`_CAMPOS`, campos geodésicos por `id(mundo)`) también sobrevive entre vidas (se vacía solo al pasar de 64
entradas), pero en el barrido ningún `id(mundo)` se reutilizó (0 de 12 vidas): no es la causa de lo visto.

**(a) Los bancos del seis.** Una vida por proceso (no afectados): P6-14, P6-15, P6-18 y P6-19 lanzan `banco_P6_*.py` con un
`subprocess` por vida (`corre_P6_14.py:22`, `corre_P6_15.py:22`, `corre_P6_18.py:16`, `corre_P6_19.py:28`). Varias vidas por proceso
(afectados en potencia): P6-25 (`escenas_P6_25.py:391`, `Pool(hilos)` sin `maxtasksperchild`; `_envuelve` en `:284`), P6-28
(`banco_P6_28.py:120`, `:65`) y P6-29 (`mide_P6_29.py:371`, `:224`); P6-26 (`banco_P6_26.py:84`) usa `Pool` pero no crea `AlmaPareja`
(no replica el cuerpo). Fidelidad medida: P6-29 la mide tic a tic y da 99,86 % en A4 y 99,94 % en A7h y A8 (`informe_P6_29.md:33`): la
infidelidad que queda (0,06-0,14 %) es compatible con esta fuga, que solo toca tics con un rival contado como objetivo; no está
comprobado que sea toda ella. P6-25 y P6-28 no publican fidelidad en sus informes (sin resultado en `grep -i fiel`); sus medidas que
dependan de candidatos de ataque contra rivales contados en vidas anteriores del mismo proceso quedan por revisar.

**(b) Las partidas de campo.** Cada proceso corre **una** vida: el contenedor arranca `policy_pareja11.py` (`Dockerfile.pareja11:215`),
que llama `asyncio.run(run(url))` una sola vez (`policy_pareja11.py:89-92`) y `run` llama `_envuelve(alma)` una vez (`:69`). No hay
cadena en el campo; la fuga es de los bancos.

**Arreglo propuesto (no hecho).** Que `_envuelve` sea reversible de verdad: guardar la base una sola vez (`D._candidatos_base`,
`PC.PARTE._emite_base`) y envolver siempre desde la base, o devolver una función `desenvuelve()` que restaure `D.candidatos` y
`PC.PARTE.emite`, y que los bancos la llamen al acabar cada vida. Como `policy_pareja.py` está congelado, la vía que no toca el cuerpo es
la del banco: restaurar la base antes de cada `_envuelve` (lo comprobado arriba) o un proceso por vida (lo hecho en P7-2 y aquí).

## Sección 2 · El techo (sello T1 y T2)

Creencia del techo, por asiento (`P7_3_techo.json`): sin munición = 0 exacto; con munición y botiquín = media real del diario:
cerbatana con municion asiento 10: 1,40 (n 10); cerbatana con municion asiento 11: 1,95 (n 37); cerbatana sin municion asiento 10: 0,00 (n 48); cerbatana sin municion asiento 11: 0,00 (n 654); botiquín dentro asiento 10: 17,57 (n 40); botiquín dentro asiento 11: 19,00 (n 44); botiquín fuera asiento 10: 1,04 (n 48); botiquín fuera asiento 11: 4,31 (n 48); arco con municion asiento 10: 8,65 (n 55); arco con municion asiento 11: 7,86 (n 73); arco sin municion asiento 10: 0,00 (n 485); arco sin municion asiento 11: 0,00 (n 908).

| objeto | situación | días | decisiones | elige lo mismo | elige otra cosa | qué otra cosa (las más frecuentes) | otra cosa en P7-2 (aprendida) |
|---|---|---|---:|---:|---:|---|---:|
| botiquín | dentro | 1-20 | 22 | 16 (72,7 %) | 6 (27,3 %) | quedarse quieto 5; apartarse (un paso) 1 | 5 (22,7 %) |
| botiquín | dentro | 21-40 | 62 | 29 (46,8 %) | 33 (53,2 %) | quedarse quieto 26; atacar 6; usar racion 1 | 31 (50,0 %) |
| botiquín | fuera | 1-20 | 41 | 6 (14,6 %) | 35 (85,4 %) | quedarse quieto 31; apartarse (un paso) 2; ir al centro 1; coger lo de la casilla 1 | 33 (80,5 %) |
| botiquín | fuera | 21-40 | 55 | 24 (43,6 %) | 31 (56,4 %) | quedarse quieto 27; ir a por otro objeto 1; apartarse (un paso) 1; coger lo de la casilla 1 | 31 (56,4 %) |
| arco | sin municion | 1-20 | 530 | 486 (91,7 %) | 44 (8,3 %) | atacar 23; usar racion 10; coger lo de la casilla 9; usar botiquin 2 | 12 (2,3 %) |
| arco | sin municion | 21-40 | 863 | 801 (92,8 %) | 62 (7,2 %) | apartarse (un paso) 18; usar botiquin 18; atacar 16; soltar 10 | 46 (5,3 %) |
| arco | con municion | 1-20 | 69 | 68 (98,6 %) | 1 (1,4 %) | ir con el hermano 1 | 1 (1,4 %) |
| arco | con municion | 21-40 | 59 | 58 (98,3 %) | 1 (1,7 %) | usar racion 1 | 1 (1,7 %) |
| cerbatana | sin municion | 1-20 | 56 | 56 (100,0 %) | 0 (0,0 %) | – | 0 (0,0 %) |
| cerbatana | sin municion | 21-40 | 646 | 614 (95,0 %) | 32 (5,0 %) | atacar 23; coger lo de la casilla 9 | 1 (0,2 %) |
| cerbatana | con municion | 1-20 | 22 | 22 (100,0 %) | 0 (0,0 %) | – | 0 (0,0 %) |
| cerbatana | con municion | 21-40 | 25 | 25 (100,0 %) | 0 (0,0 %) | – | 0 (0,0 %) |

| predicción | medido | veredicto |
|---|---|---|
| T1 ataques sin munición con creencia 0: cambian < 10 % | días 21-40: 94 de 1509 (6,2 %); todos los días: 138 de 2095 (6,6 %) | **acierta** |
| T2 botiquín fuera con el techo: a menos de 10 puntos del 56 % de P7-2 | 31 de 55 (56,4 %); P7-2: 31 de 55 (56,4 %); diferencia 0,0 puntos; decisión a decisión, las mismas 31 cambian y las mismas 24 no | **acierta** |

Con la creencia exactamente 0, en los 1957 ataques sin munición que no cambian el candidato de atacar **empata exactamente** con quedarse
quieto en 1816 casos (la foto prevista es la misma: un golpe de 0 no cambia nada) y tiene d menor en 141 (la previsión de atacar deja
otra huella además del daño, abajo). El empate lo rompe el desempate a favor de la acción. Es decir, la creencia perfecta tampoco
cambia la decisión: **no es que lo aprendido sea insuficiente; es que el cuerpo no tiene a dónde cambiar, y en el empate prefiere actuar.**

## Sección 3 · Las opciones en la pelea

Candidatos que genera el decisor en los 2095 tics de ataque sin munición (réplica con el catálogo, `d_replica` de `P7_2_banco.json`):

| conjunto de candidatos (atacar_* agrupado) | tics |
|---|---:|
| atacar_*, noop | 1354 |
| atacar_*, noop, usar_botiquin, usar_racion | 119 |
| atacar_*, noop, usar_botiquin | 110 |
| atacar_*, noop, usar_racion | 99 |
| atacar_*, atacar_*, noop | 89 |
| atacar_*, noop, ponerse_camouflage | 60 |
| atacar_*, noop, ponerse_camouflage, usar_racion | 52 |
| atacar_*, noop, soltar_first_aid, usar_botiquin | 52 |
| atacar_*, noop, ponerse_camouflage, soltar_first_aid, usar_botiquin | 31 |
| atacar_*, atacar_*, noop, usar_botiquin | 20 |

Con alguna opción de moverse (`move_`, `paso_`, `ir_`) solo en 66 de 2095 tics (3,2 %). Por qué no aparecen las otras:

- **Apartarse, ir al centro, ir a por munición a la vista.** Son candidatos `paso_*`, `ir_centro`, `ir_objeto` (`decisor_zs.py:433-468`).
  `Bloqueos.veta` (`decisor_zs.py:95-103`) quita todo lo que empiece por `move_`, `paso_`, `ir_` mientras `move_ready_in > 0` (`:97-98`), y
  en plena pelea las piernas están casi siempre enfriándose (11 tics por paso a velocidad 5). Los `atacar_*` se quitan solo con
  `attack_ready_in > 0` (`:99-100`), y el arco sin flechas no gasta enfriamiento (`no_ammo` cada tic). La munición a la vista entra en
  `ir_objeto` por `_mejor_objeto` (`decisor_zs.py:682-705`, valor/(1+distancia), promesa 0 para la munición), pero el candidato es un `ir_` y
  cae con el veto de las piernas.
- **Soltar el arma.** `soltar_*` solo se crea para consumibles con `heal > 0` y con el hermano herido o la provisión abierta
  (`decisor_zs.py:496-521`): no existe soltar un arma. Empuñar (`:536-544`) solo propone una arma del zurrón con **más** daño que la de la mano.
- **Pegar con la mano.** No existe el puñetazo: el candidato de atacar exige `arma.damage > 0` (`decisor_zs.py:587-588`), y las manos
  vacías no son un arma (`amenaza11_P6_11.py:28-31` las inventa solo para la amenaza ajena).
- **El desempate que prefiere la acción.** `decisor_zs.py:895-897` llama `select_tiebreak(..., exclude_noop=True, tie_unified=True)`;
  en `planificador/planificador_v1.py:433-456`, con empate exacto en la d terminal se va a `_hierarchy` (`:393-402`), cuya primera regla
  N2a (`:399-402`, "quieto no gana empates") quita `noop` de los candidatos empatados si queda alguno.

## Sección 4 · El botiquín fuera del círculo, caso a caso (días 21-40, creencia aprendida de P7-2)

Los 24 que no cambian: candidato que gana, margen de d sobre el segundo, y si había casilla sin daño alcanzable antes del corte
(`P7_1_medidas.json`, `casilla_sin_dano_alcanzable`; pasos = casillas hasta el borde).

| vida | t | día | creencia | gana | d | 2.º | margen | candidatos | vida (hp) | el uso en el diario | pasos al borde | alcanzable |
|---|---:|---:|---:|---|---:|---|---:|---:|---:|---|---:|---|
| 24450076/11 | 12.649 | 21 | 12,7 | usar_botiquin | 3,0108 | noop | 0,0591 | 3 | 93 | cancelado por zone | 2 | sí |
| 24450076/11 | 12.698 | 21 | 11,7 | usar_botiquin | 2,6813 | noop | 0,0891 | 3 | 80 | cancelado por zone | 2 | sí |
| 24450076/11 | 12.747 | 21 | 10,9 | usar_botiquin | 2,8709 | noop | 0,0880 | 3 | 67 | cancelado por zone | 2 | sí |
| 24450076/11 | 12.796 | 21 | 10,2 | usar_botiquin | 3,4591 | noop | 0,0965 | 3 | 54 | cancelado por zone | 2 | no |
| 24450076/11 | 12.845 | 21 | 9,6 | usar_botiquin | 3,5987 | noop | 0,1193 | 17 | 40 | cancelado por zone | 1 | sí |
| 24450076/11 | 12.894 | 21 | 9,1 | usar_botiquin | 3,7676 | noop | 0,1404 | 3 | 27 | cancelado por zone | 1 | sí |
| 24450076/11 | 12.943 | 21 | 8,6 | usar_botiquin | 3,9831 | noop | 0,1606 | 3 | 14 | cancelado por zone | 1 | sí |
| 24868992/10 | 10.645 | 25 | 2,9 | usar_botiquin | 3,5425 | noop | 0,0264 | 3 | 73 | completado | – | – |
| 24868992/11 | 10.105 | 25 | 6,5 | usar_botiquin | 3,0276 | noop | 0,0330 | 2 | 96 | cancelado por zone | 1 | sí |
| 24868992/11 | 10.154 | 25 | 6,2 | usar_botiquin | 3,0566 | noop | 0,0513 | 2 | 90 | cancelado por zone | 2 | sí |
| 24868992/11 | 10.203 | 25 | 5,9 | usar_botiquin | 3,1197 | noop | 0,0499 | 2 | 83 | cancelado por zone | 1 | sí |
| 24868992/11 | 10.301 | 25 | 5,7 | usar_botiquin | 3,3299 | noop | 0,0499 | 2 | 73 | cancelado por zone | 2 | no |
| 24868992/11 | 10.399 | 25 | 5,3 | usar_botiquin | 3,3272 | noop | 0,0462 | 2 | 60 | cancelado por zone | 4 | no |
| 24868992/11 | 10.448 | 25 | 5,1 | usar_botiquin | 3,3541 | noop | 0,0482 | 2 | 54 | cancelado por zone | 4 | no |
| 24868992/11 | 10.497 | 25 | 4,9 | usar_botiquin | 3,5163 | noop | 0,0547 | 2 | 47 | cancelado por zone | 2 | no |
| 24868992/11 | 10.546 | 25 | 4,7 | usar_botiquin | 3,6313 | noop | 0,0605 | 2 | 40 | cancelado por zone | 2 | no |
| 24868992/11 | 10.595 | 25 | 4,6 | usar_botiquin | 3,7645 | noop | 0,0653 | 2 | 34 | cancelado por zone | 2 | no |
| 25078450/10 | 12.908 | 27 | 2,5 | usar_botiquin | 3,3710 | noop | 0,0230 | 3 | 60 | cancelado por zone | 2 | no |
| 25078450/10 | 12.957 | 27 | 2,4 | usar_botiquin | 3,5457 | paso_N | 0,0275 | 17 | 47 | cancelado por zone | 1 | no |
| 25811553/10 | 11.545 | 34 | 1,4 | usar_botiquin | 3,1095 | noop | 0,0117 | 2 | 95 | cancelado por zone | 2 | sí |
| 25811553/10 | 11.643 | 34 | 1,3 | usar_botiquin | 3,2660 | noop | 0,0115 | 2 | 85 | cancelado por zone | 1 | sí |
| 25811553/10 | 11.741 | 34 | 1,3 | usar_botiquin | 2,8000 | noop | 0,0096 | 2 | 75 | cancelado por zone | 2 | no |
| 25811553/10 | 11.790 | 34 | 1,2 | usar_botiquin | 3,3441 | noop | 0,0105 | 2 | 65 | cancelado por zone | 2 | no |
| 25811553/10 | 11.839 | 34 | 1,1 | usar_botiquin | 3,4531 | noop | 0,0112 | 2 | 55 | cancelado por zone | 2 | no |

En los 24: gana siempre `usar_botiquin`, por un margen de d entre 0,0096 y 0,1606 (mediana 0,0499); el segundo es `noop` en 23 casos; con 2 candidatos en 14 de ellos (sin piernas). Casilla sin daño alcanzable
antes del corte: sí en 11, no en 12, sin corte por anillo en 1. Todos menos 1 acabaron cancelados en el diario.

Los 31 que cambian: qué eligen en su lugar.

| en su lugar | casos | margen de d sobre `usar_botiquin` (mediana) | creencia (mediana) |
|---|---:|---:|---:|
| quedarse quieto | 27 | 0,2671 | 3,8 |
| ir a por otro objeto | 1 | 0,3752 | 3,1 |
| apartarse (un paso) | 1 | 0,0244 | 5,5 |
| coger lo de la casilla | 1 | 0,2434 | 4,5 |
| ir con el hermano | 1 | 0,2334 | 1,1 |

Fuente: `P7_2_banco.json` (`d_creencia` por candidato) cruzado con `P7_1_medidas.json` por (vida, t). Lectura: cuando cambia, casi siempre
es a **quedarse quieto** (sin piernas no hay más), no a ponerse a salvo; y cuando no cambia, el botiquín gana por centésimas.

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P7_3.md` | T1 y T2, md5, commit 9681ab7 |
| `banco_P7_3.py`, `P7_3_techo.json`, `P7_3_banco_techo.json` | la creencia del techo y la repetición de decisiones con ella |
| `fuga_P7_3.py`, `fuga_P7_3.json` | el barrido secuencial con sondas (12 vidas); `fuga_P7_3.log`, `banco_P7_3.log` fuera de git |
| `escribe_informe_P7_3.py`, `informe_P7_3.md` | este informe |

# CONGELADO_P6 · EL CUERPO DEL SEIS (serie A4), congelado

*27-sep-2026 · P6-12. A partir de aquí el cuerpo no se toca. Cualquier cambio
posterior es una versión nueva, con nombre nuevo y declarada. Ninguna cifra de
este archivo se escribió antes de calcularla: todas salen de
`P6_12_inventario.json`, `P6_12_config.json`, `P6_12_reproduce.json` y de las
medidas de P6-10 y P6-11.*

`motor/model.py` = `1e511978c251130e95169ebf8443efa1` (intocable, comprobado). Los 202 archivos
de `cantera/paper5/CONGELADO.md`: 0 alterados (comprobado).

## 1 · INVENTARIO REAL

Trazado cargando la política de A4 (`policy_pareja11`) con el entorno de la
imagen y replayando 600 tics de una vida real (`P611_t1_A4_20260916`, asiento
10) por la vía real: todo módulo del repositorio importado por la política y
todo archivo abierto. **32 archivos son el cuerpo** (los de medida —`mide_*`,
`banco_*`, `humo_*`, `serie_util`— no viajan en la imagen y no se listan aquí).

| clase | archivo | md5 |
|---|---|---|
| alma (paper 4/5) | `paintball/alma/appraisal_zs.py` | `87745903992bdf0b4f5a18d13f9d4f5a` |
| alma (paper 4/5) | `paintball/alma/appraisal_zs_v42_exp.py` | `98c13d60167c80cc8334c965be75c640` |
| alma (paper 4/5) | `paintball/alma/confianza_viva.py` | `6e1e444435914f0b9df287ea37555bbc` |
| alma (paper 4/5) | `paintball/alma/cortex_t5.py` | `defb11d3a4661ff57745214ccd1ab14f` |
| alma (paper 4/5) | `paintball/alma/decisor_zs.py` | `8fa03547e3228ef9df4aa94c444f9252` |
| alma (paper 4/5) | `paintball/alma/forma_viva.py` | `b2c87c93f0ed47e48fd8991a5a797a42` |
| alma (paper 4/5) | `paintball/alma/formas_azar.py` | `eefb5534e9533c8b742f7feb96239588` |
| alma (paper 4/5) | `paintball/alma/hilo_forma.py` | `aeea06ae4eb5b704e94fe845a5a5e5aa` |
| alma (paper 4/5) | `paintball/alma/mundo.py` | `e2c2cf7618b61e1280f2e3ea989f1872` |
| alma (paper 4/5) | `paintball/alma/parte.py` | `80dabc2e78c7c36f0708a2d95e22262a` |
| alma (paper 4/5) | `paintball/alma/policy_cortex.py` | `6997b00c266f23d6037cc1a018f60a76` |
| alma (paper 4/5) | `paintball/alma/policy_forma.py` | `896e97a0cca1efcb736596e0b8b15cea` |
| alma (paper 4/5) | `paintball/alma/relator_t5.py` | `929c49f6ced9af1cbd37eadec08c54f0` |
| motor | `motor/model.py` | `1e511978c251130e95169ebf8443efa1` |
| otro | `cantera/paper4/memoria_aprendida_p95.json` | `6535717a27e3188852af8a76d2c3ef60` |
| paper 5 (CONGELADO.md) | `cantera/paper5/alcance_g.py` | `bf62b03587506064311c122fd0e09102` |
| paper 5 (CONGELADO.md) | `cantera/paper5/curiosidad.py` | `f803f47c8ed0a8eaf3855d7e1dc7d457` |
| paper 5 (CONGELADO.md) | `cantera/paper5/curiosidad_forma.py` | `141ecb2eb17f76654caf4bbf3c29c642` |
| paper 5 (CONGELADO.md) | `cantera/paper5/forma.py` | `b801876afda071403c5af54a28feff85` |
| paper 5 (CONGELADO.md) | `cantera/paper5/proyeccion.py` | `bbc42daeaa769c783844997067ef148d` |
| paper 5 (CONGELADO.md) | `cantera/paper5/traductor_forma.py` | `b310bb72884ef5f4e3510ab803cd2776` |
| paper 6 | `cantera/paper6/amenaza11_P6_11.py` | `9d493b05495f55316f29cbffa5561cdb` |
| paper 6 | `cantera/paper6/arreglos_P6_6.py` | `4d10ea09333553ebf7d6ce0afdb73832` |
| paper 6 | `cantera/paper6/arreglos_P6_8b.py` | `5028b54d4afd8c7c82bc8e5e3a94a01e` |
| paper 6 | `cantera/paper6/filas10_P6_10.py` | `af4617ad93a27838376df17d0c78b65c` |
| paper 6 | `cantera/paper6/oido5_P6_5.py` | `4f7aa3b3ddc4fc32e4b47c1356974415` |
| paper 6 | `cantera/paper6/oyente2.py` | `4e8b657f9168b0ffda5e411601b1aa14` |
| paper 6 | `cantera/paper6/parte2.py` | `67ba0003234939c349af12be5764a3b0` |
| paper 6 | `cantera/paper6/policy_pareja.py` | `796fc64229d047410fb351dfa61f871b` |
| paper 6 | `cantera/paper6/policy_pareja11.py` | `e7136f856e6c09dd033bb4658cd135ea` |
| planificador | `planificador/__init__.py` | `d41d8cd98f00b204e9800998ecf8427e` |
| planificador | `planificador/planificador_v1.py` | `d0a3151d718e6b60d499e258c9dea9b1` |

Notas del inventario:
* `paintball/alma/memoria_aprendida_p95.json` viaja en la imagen pero **no se
  carga**: `appraisal_zs_v42_exp.py:383` solo la lee con `MIEDO_ON`, y
  `policy_cortex.py:95` lo fija a `False`. Igual `instruccion_forma.md`,
  `tabla_ensenada.md`, `P56A_distribucion_azar.json`: se copian en la imagen
  (`Dockerfile.pareja11`) y solo se abren con las puertas del consejero
  encendidas (`GEMV_FORMA`, `GEMV_CONSEJERO_FORMA`, `GEMV_CORTEX`), que en A4 están a 0.
* Lo que copia la imagen (`COPY` de `Dockerfile.pareja11`, md5 `98040b3b288b6d71904a5cf56e2d76f9`):
  `motor/`, `planificador/`, `paintball/alma/`, `cantera/paper5/forma.py`, `cantera/paper5/proyeccion.py`, `cantera/paper5/traductor_forma.py`, `cantera/paper5/alcance_g.py`, `cantera/paper5/instruccion_forma.md`, `cantera/paper5/tabla_ensenada.md`, `cantera/paper5/P56A_distribucion_azar.json`, `cantera/paper5/curiosidad.py`, `cantera/paper5/curiosidad_forma.py`, `cantera/paper6/parte2.py`, `cantera/paper6/oyente2.py`, `cantera/paper6/policy_pareja.py`, `cantera/paper6/humo_P6_3.py`, `cantera/paper6/humo_red_P6_4.py`, `cantera/paper6/humo_mundo.jsonl`, `cantera/paper6/oido5_P6_5.py`, `cantera/paper6/arreglos_P6_6.py`, `cantera/paper6/policy_pareja6.py`, `cantera/paper6/humo_red_P6_6.py`, `cantera/paper6/arreglos_P6_8.py`, `cantera/paper6/policy_pareja8.py`, `cantera/paper6/humo_red_P6_8.py`, `cantera/paper6/arreglos_P6_8b.py`, `cantera/paper6/filas10_P6_10.py`, `cantera/paper6/policy_pareja10.py`, `cantera/paper6/humo_red_P6_10.py`, `cantera/paper6/amenaza11_P6_11.py`, `cantera/paper6/policy_pareja11.py`, `cantera/paper6/humo_red_P6_11.py`.
* `paintball/alma/` se copia entera; de ella el cuerpo importa los módulos de la
  tabla. `cantera/paper5/*.py` se copian a `/app/alma/`.

## 2 · CONFIGURACIÓN (todo leído de los módulos con el cableado de `policy_cortex` y el entorno de la imagen)

| pieza | valor |
|---|---|
| **S-COMPANIA** (`filas10_P6_10.py`) | D0 = **7 casillas de camino**; techo = **0.32** (`GEMV_COMPANIA_TECHO`, en ENV de la imagen y en el `run` de la política); rango = D0·(1 + 2·calma), calma = 1 − max(F-4-ALCANCE, S-7-AGRESOR, F-HERMANO-AMENAZA, F-HERMANO-GOLPE); M = techo·min(1, (d − D0)/rango) si d > D0; d = camino (`campo_geodesico`) a la posición real del hermano (vista o parte fresco); reparto (0.1, 0.1, 0.8); activa siempre; el veto de `Bloqueos` manda |
| **S-SOLEDAD** | **no tocada**: la del cinco, (1−P)·rampa, P = 1 vista, 0,5 oída < 3 s; techo 0.5, rampa 30 s; con el hermano vivo y el parte cada 25 tics vale 0 (P6-9 § 4): solo se enciende con el hermano muerto |
| **armas virtuales** (`amenaza11_P6_11.py`) | `~manos`: ikMelee, daño **3**, alcance 1, para todo hostil visible o contado con la mano vacía · `~manos_pegando`: ikMelee, daño **dmg_ref = 18**, alcance 1, si me pega (ventana S-7 = 5 s) o es el agresor del parte fresco del hermano · solo en la copia de la obs del decisor; catálogo, E2 y diario intactos |
| **oyente2** | CADUCIDAD_RIVAL = **50** tics; UMBRAL_REC = **0.3**; edad máxima de recurso 86 tics |
| **«lo dado, dado está»** (`arreglos_P6_6.py`) | N = min(d·coste_movimiento(speed) + **268**, CESION_CADUCA_S·tick_rate = 30 s × 24 = **720**); coste = 11 tics/casilla con speed 5 |
| **empatía** (`policy_cortex.py:93-96`, en código) | EMPATIA_ON = True, H_PREV = 0.25, H_GOLPE = 1.0, MIEDO_ON = False, VIDA_AJENA_ON = False, `D.A` = `alma.appraisal_zs_v42_exp` |
| **parte E2 y gemelo E1** | E2 cada **25** tics, caducidad 96, ≤ 120 caracteres; gemelo E1: por cada E2 del hermano se añade al chat una copia con la cabeza traducida a E1, validada con `parte.parsea` (`oido5_P6_5.py`); con ojos apagados, E1 cada 48 |
| **arreglos P6-8b** | `ir_pareja` al parte fresco cuando no lo ve (solo con piernas listas); nada de `coger` si la previsión no cambia la mochila o el mundo dijo `inventory_full` |
| **oído y don** (P6-6) | activos |
| **constitución** | {'intelligence': 8, 'athleticism': 6, 'speed': 5, 'strength': 1} |
| **ojos** | {'OJOS': True, 'CADA': 25, 'MAX_CHARS': 120, 'CADUCIDAD_RIVAL': 50, 'UMBRAL_REC': 0.3, 'EDAD_MAX_RECURSO': 86} |

### El mundo

| | |
|---|---|
| versión / coworld | **0.1.19** · `cow_6a55df20-08d1-4e4c-adba-33dbd97e1e6f` (zero-sum, variante `competition`) |
| liga | `league_6764202e-2ac1-4c98-a77e-cabc75582939` |
| roster | `cantera/paper6/roster_lento_v2_PROPUESTA.json` (md5 `3eb7dd60d8f43be2751b0325945a3f27`): 5 rivales × veces = 14, más la pareja en los asientos [10, 11] |
| base del mundo lento | `cantera/paper5/roster_lento_v1.json` (`game_config_overrides` tal cual) |
| política jugada (A4) | `gemv-p6-A4-manos:v1` = `b4e322cf-7390-4e01-b8a8-b854398e647f` |
| imagen | `cantera/paper6/Dockerfile.pareja11` (md5 `98040b3b288b6d71904a5cf56e2d76f9`), CMD `python -u /app/alma/policy_pareja11.py`, run `GEMV_OJOS=1 GEMV_COMPANIA_TECHO=0.32` |
| **las 20 semillas** (las de `cantera/paper4/semillas_S2.json[:20]`, iguales a las jugadas en A4: True) | 20260916, 20365645, 20470374, 20575103, 20679832, 20784561, 20889290, 20994019, 21098748, 21203477, 21308206, 21412935, 21517664, 21622393, 21727122, 21831851, 21936580, 22041309, 22146038, 22250767 |

**La fase tres reutilizará esas mismas 20 semillas.**

## 3 · PRUEBA DE QUE EL CONGELADO ES EL DE VERDAD

`reproduce_P6_12.py`: cuatro vidas de A4 (dos partidas), replayadas en seco por
la vía real con solo los archivos del inventario, comparadas con el diario
tic a tic (`elegido`) y, cada 24 tics, la `d` de cada candidato:

| vida | decisiones | iguales | difieren | `d` comparadas | \|Δd\| máx. |
|---|---:|---:|---:|---:|---:|
| `paintball/runs/P611_t1_A4_20260916/ereq_2c2e5ffe-bfc8-49fc-ab3d-c307f5e9f810-policy_agent_10.art.log` | 12168 | 12168 | 0 | 1320 | 0.00000 |
| `paintball/runs/P611_t1_A4_20260916/ereq_2c2e5ffe-bfc8-49fc-ab3d-c307f5e9f810-policy_agent_11.art.log` | 13152 | 13152 | 0 | 3533 | 0.00000 |
| `paintball/runs/P611_t2_A4_21308206/ereq_862c6e7c-3d7c-4de9-a82e-ee8d9bdde40e-policy_agent_10.art.log` | 12576 | 12522 | 54 | 3556 | 0.00240 |
| `paintball/runs/P611_t2_A4_21308206/ereq_862c6e7c-3d7c-4de9-a82e-ee8d9bdde40e-policy_agent_11.art.log` | 14222 | 14222 | 0 | 6064 | 0.00000 |

**Tres vidas al bit** (39.542 decisiones iguales, |Δd| = 0,00000 en 10.917
candidatos). En la cuarta (`21308206` asiento 10) difieren **54 de 12.576
decisiones (0,43 %)**, todas `atacar_*` en el replay contra `noop` en el diario, y
la `d` difiere como máximo 0,0024: **el diario guarda `damage_dealt` como un
entero en sus 12.576 tics, no como la lista de golpes dados**, y sin ella el
replay no reconstruye el hp estimado del rival que la valoración de `atacar`
usa. Es un límite del diario, no del congelado; se declara. Un fallo del propio
replay (hp = 0 leído como 100) se corrigió en el reproductor sin tocar el banco
de P6-11.

## 4 · LÍNEA BASE: A0 (el cuerpo del cinco con el parte, P6-6) contra A4 (el cuerpo del seis, P6-11)

Mismas 20 semillas, mismo mundo, misma liga, mismo roster. Cifras de
`P6_6_medidas`, `P6_7_*`, `P6_10_base`, `P6_11_*`.

| medida | A0 (P6-6) | **A4 (P6-11)** |
|---|---:|---:|
| vida media de la pareja | 12.427,9 | **12.840,2** |
| vida mediana | 12.997 | 13.009 |
| juntos: a ≤ 3 casillas (los dos vivos) | 79,13 % | **77,26 %** |
| a > 15 casillas | 0,00 % | 0,00 % |
| escapadas > 8 casillas · de ≥ 200 tics | 481 · 3 | 305 · 0 |
| supervivientes (de 40) · mueren | 8 · 32 | **11** · 29 |
| los dos vivos al aviso · al cierre | 18/20 · 18/20 | 19/20 · **19/20** |
| sobrevive el otro tras el primero (mediana, tics) | 912 | 804 |
| muertes por causa: anillo · rival visto · no consta | 20 · 11 · 1 | 22 · 6 · 1 |
| …por rival con arma · con la mano vacía | 9 · 2 | 4 · 2 |
| golpes: anillo · rival con arma · mano vacía · no visto · veneno | 380 · 155 · 103 · 0 · 10 | 375 · 101 · **148** · 0 · 35 |
| golpes a ciegas | 0 | 0 |
| comida recogida por vida (ración o venda) | 3,20 | **2,88** |
| muertes con el otro vivo y a ≤ D0 de camino | 17/18 | 15/17 |
| \|disc\| S-8 por decisión | 0,0585 | 0,0433 |
| `coger` + `inventory_full` (tics) | 6254 | 0 |

## 5 · LOS PRECIOS Y DEFECTOS QUE SE QUEDAN DENTRO, con su número

| precio / defecto | número (A4) | dónde se midió |
|---|---:|---|
| **comida recogida por vida** | **2,88** (A0 3,20; A3 3,95) | P6-11 § 3: 820 de los 1.005 cambios del banco son `ir_* → paso_*` junto a un rival de mano vacía |
| **muertes por anillo** | **22** de 29 (A0 20; A3 19) | P6-11 § 3, en el borde de lo sellado |
| **golpes de rivales sin arma** | **148** (A0 103; A3 166) | P6-11 § 3: bajan un 11 %, no al nivel de A0 |
| **`ir_pareja` elegido poco** | **2,88 %** con piernas listas y hermano fuera de vista (A0 6,1 %); en las escapadas largas de A2, 56 de 10.660 | P6-10 § 4.1: ganan los pasos que acercan, no el candidato |
| **don reabsorbido** | **29 de 90** episodios en A3 (11 de 61 en A4) | P6-10 § 4.3: vence el plazo N con el que dio todavía al lado; no es el bucle (0 tics de mochila) |
| golpes a ciegas | 0 en 240 vidas | P6-4, P6-6, P6-8, P6-10, P6-11 |
| S-8 de rivales contados en el camino de vuelta | +0,22 de M con rival contado (n = 926) | P6-10 § 4.3: la fila lo compensa |
| el diario no guarda `damage_dealt` como lista | 54 decisiones de ataque no reproducibles en 1 vida de 4 | § 3 de este archivo |

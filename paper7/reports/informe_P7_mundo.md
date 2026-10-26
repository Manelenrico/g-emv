# P7-mundo · Los datos del mundo del paper siete (para las secciones 2 y 8)

*20-oct-2026. Solo lectura: 0 créditos, 0 $. Nada se ha lanzado. Se han leído las respuestas de la plataforma (`P7_<n>_res/*.json`) y los diarios en memoria (los `.zip` sin extraer).*

**Rutas.**
- Las que no llevan prefijo son de `cantera/paper7/`.
- Los diarios están en `paintball/runs/`.
- `paper5/` y `paper6/` cuelgan de `cantera/`.
- `~/gemv-paper7/` se escribe con su prefijo.

**Lanzador y respuestas de cada campo**

| campo | lanzador | respuestas | sello |
|---|---|---|---|
| P7-30 | `lanza_P7_30.py` | `P7_30_res` | `SELLO_P7_30.md` |
| P7-34 | `lanza_P7_34.py` | `P7_34_res` | `SELLO_P7_34.md` |
| P7-45 | `lanza_P7_41.py` (orquestado por `orquesta_P7_43.py`) | `P7_41_res` | `SELLO_P7_42.md` |
| P7-50 | `lanza_P7_50.py` | `P7_50_res` | `SELLO_P7_49.md` |
| P7-56 | `lanza_P7_56.py` | `P7_56_res` | `SELLO_P7_56.md` |
| P7-61 | `lanza_P7_57.py` (`SELLO_P7_61.md:18`) | `P7_57_res` | `SELLO_P7_61.md` |
| P7-65 | `lanza_P7_65.py` | `P7_65_res` | `SELLO_P7_65.md` |
| P7-67 | `lanza_P7_67F.py` con `P7_67F_diseno.json` | `P7_67F_res` | `SELLO_P7_67.md` |

## 1. Versión del juego

- **Etiqueta: zero-sum 0.1.19, variante «competition», en los ocho campos.**
  - Consta en las respuestas de la plataforma: `"coworld_name": "zero-sum"`, `"coworld_version": "0.1.19"`, `"variant_id": "competition"`.
  - Las líneas son `P7_30_res/s1_d1_TECHO.json:5-8`, y las mismas 5-8 en el primer día de `P7_34_res`, `P7_41_res`, `P7_50_res`, `P7_56_res`, `P7_57_res`, `P7_65_res` y `P7_67F_res`.
  - Todas las respuestas llevan el mismo `coworld_id`, `cow_6a55df20-08d1-4e4c-adba-33dbd97e1e6f`: 120, 120, 363, 120, 120, 122, 122 y 1.146.
- **No cambió en ningún momento**, ni dentro de un campo ni entre campos (del 8 al 20 de octubre).
- **Liga:** la misma, `league_6764202e-…`.
  - `lanza_P7_30.py:25`, `lanza_P7_34.py:27`, `lanza_P7_41.py:29`, `lanza_P7_50.py:33`, `lanza_P7_56.py:38`, `lanza_P7_57.py:41`, `lanza_P7_65.py:45`.
  - P7-67 la toma de `lanza_P7_65` (`lanza_P7_67F.py:17,66`).
- **Protocolo:** `zero_sum.player.v1`, a 24 tics por segundo, en el `player_config` de los diarios (por ejemplo, la línea 8 del diario del asiento 10 de `P730_s1_d10_APRENDE_39845239`).
- **Commit del juego: no consta.**
  - Ninguna respuesta, estado, diario ni Dockerfile lo guarda.
  - Lo más cercano es el digest de la imagen, `cogames@sha256:5403c453…dc6c5`, en `coworld/cow_6a55df20-…/coworld_images.json:7`, con la versión 0.1.19 en `:4`.
  - Ese fichero se descargó el 12-oct, después de P7-30 y P7-34.
- Los `P7_*_estado.json` solo guardan la versión de nuestra política (por ejemplo `gemv-p7-campo:v151`), no la del juego.

## 2. Configuración: es el mundo LENTO, no el normal

**De dónde sale la configuración**
- Los ocho lanzadores copian `game_config_overrides` de `paper5/roster_lento_v1.json` y solo cambian la semilla:
  - `lanza_P7_30.py:113-114`, `lanza_P7_34.py:115-116`, `lanza_P7_41.py:126`, `lanza_P7_50.py:133-134`, `lanza_P7_56.py:138-139`, `lanza_P7_57.py:141-142`, `lanza_P7_65.py:145-146`, `lanza_P7_67F.py:62`.
- El `game_config` que devuelve la plataforma, quitando la semilla y los nombres, es idéntico en todas las respuestas de los ocho campos.

**Duración**
- `max_ticks` 18240, es decir, 760 s a 24 tics por segundo.
- Fuentes: `paper5/roster_lento_v1.json:26`; `P7_30_res/s1_d1_TECHO.json:595`.

**Calma antes del anillo**
- Cuenta atrás (`freeze_ticks`) de 480 tics: `roster_lento_v1.json:27`; `P7_30_res/s1_d1_TECHO.json:598`.
- La fase viva empieza en el tic 481.
- El primer aviso del anillo llega en el tic 7296 y el cierre empieza en el 7536.
- Hasta el aviso, `damage_per_s` es 0. En el diario de `P765_s1_d10_MIENTEN_DOS_44348586`, asiento 10, el tic 1 está en `:19` y el tic 7296 en `:18328`.

**Calendario del anillo**
- `roster_lento_v1.json:29-87` y `P7_30_res/s1_d1_TECHO.json:370`.
- Formato: `[aviso, cierre, fin, radio inicial, radio final, daño/s]` (`coworld_manifest.json:40`).

| fase | aviso | cierre | fin | radio | daño/s |
|---|---|---|---|---|---|
| 1 | 7296 | 7536 | 8076 | 24 → 19 | 1 |
| 2 | 8436 | 8676 | 9216 | 19 → 15 | 2 |
| 3 | 9576 | 9816 | 10356 | 15 → 11 | 4 |
| 4 | 10716 | 10956 | 11496 | 11 → 8 | 6 |
| 5 | 11856 | 12096 | 12636 | 8 → 5 | 8 |
| 6 | 12996 | 13236 | 13776 | 5 → 3 | 16 |
| 7 | 14136 | 14376 | 14916 | 3 → 0 | 24 |

- Centro de la zona: [24, 24].
- El daño de cada fase rige desde su aviso. Así se ve en los registros de tic del diario de P7-65 citado: daño 1 en `:18328`, daño 2 en `:21542`, daño 4 en `:24500`.

**Patrocinador**
- Configuración: `"live": false`, `budget_per_team` 600, `shop_opens_tick` 1680.
- 16 regalos con guion:
  - una ración al asiento par de cada equipo, en los tics 2016-2184;
  - un botiquín al asiento impar, en los tics 4608-4776.
  - Nuestras hermanas (equipo F) reciben la ración en el asiento 10, en el tic 2136, y el botiquín en el asiento 11, en el tic 4728.
- Fuentes: `paper5/roster_lento_v1.json:89-191`; la respuesta de la plataforma, `P7_30_res/s1_d1_TECHO.json:492-593` y `P7_67F_res/n1_s1_d1_HONESTA.json:481-582`.

**Lento o normal**
- **Es el mundo lento:** 18.240 · 480, primer aviso en el tic 7.296. El normal es 9.120 · 240, con el primer aviso en el tic 1.440 (`paper6/informe_P6_0.md:129,133-134`; esa tabla atribuye el mundo lento a «paper cinco»).
- El seis lo llama «mundo lento 0.1.19» (`paper6/SELLO_P6_6.md:12`; `paper6/SELLO_P6_8.md:10`).
- La variante «competition» de la plataforma, sin la configuración que se le pasa, es la normal: 9120 tics, cuenta atrás de 240, patrocinador de 300 (`coworld_manifest.json:359,585-593`).
- **Para no confundirse:** `SELLO_P7_67.md:30` llama «el mundo normal, sin estatuas» al nivel 14 de P7-67. Se refiere al roster de 14 rivales activos, no a la configuración: las 1.146 respuestas de P7-67 llevan la configuración lenta.

## 3. Rivales de cada campo

**P7-30, P7-34, P7-45, P7-50, P7-56, P7-61 y P7-65: el mismo roster en todos**
- Es `paper6/roster_lento_v2_PROPUESTA.json`. El archivo aún dice «PROPUESTA, SIN APROBAR» (`:2`), aunque es el que se usa.
- Nuestras dos criaturas piden los asientos 10 y 11 de forma explícita. Los 14 rivales van con `"slot": -1`.
  - `lanza_P7_30.py:113-119`, `lanza_P7_34.py:115-121`, `lanza_P7_41.py:126-132`, `lanza_P7_50.py:133-139`, `lanza_P7_56.py:138-144`, `lanza_P7_57.py:141-147`, `lanza_P7_65.py:145-151`.
- Rivales:
  - belobog v2, 5 (`roster_lento_v2_PROPUESTA.json:35-38`);
  - zero-sum-scavenger v12, 5 (`:43-46`);
  - aaron-zs-fable v2, 2 (`:51-54`);
  - zs-patient v3, 1 (`:59-62`);
  - skourehjan-zero-sum-scripted-v1, 1 (`:67-70`).
- En las respuestas de las 1.083 partidas de estos siete campos hay una sola disposición de asientos (campo `participants[].position`):
  - belobog en 0-4;
  - scavenger en 5-9;
  - nosotros en 10-11;
  - aaron en 12-13;
  - zs-patient en 14;
  - skourehjan en 15.
- Entre brazos solo cambia la versión de nuestra política.
- Todas las peticiones son de un episodio (`num_episodes: 1`) y todas las respuestas tienen `job_index` 0. La rotación de dos episodios por petición, vista en S-2, no aparece en el siete.
- Los sellos de P7-30 a P7-65 no nombran el roster.
- El asiento de cada hermana desde P7-50 es valiente en el 10 y prudente en el 11 (`SELLO_P7_56.md:7`).

**P7-67** (`lanza_P7_67F.py:62-66`; `P7_67F_diseno.json`; `SELLO_P7_67.md:27-36`)

| nivel | rivales activos (asiento) | estatuas `gemv-p7-quieta` v1 |
|---|---|---|
| 1 | aaron-zs-fable v2 (4) | 0-3, 5-9 y 12-15 |
| 2 | aaron (4) y zero-sum-scavenger v12 (12) | 0-3, 5-9 y 13-15 |
| 3 | aaron (4), scavenger (12) y belobog v2 (2) | 0-1, 3, 5-9 y 13-15 |
| 14 | el roster de P7-65 tal cual (asiento −1) | ninguna |

- **Cómo se eligieron:**
  - el rival del nivel 1, con `random.Random(6767)` (`REGISTRO_P7_67.md:10-12`);
  - los que se añaden en los niveles 2 y 3, con `random.Random(6768)` (`SELLO_P7_67.md:30-34`).
- **Se comprobó en las respuestas:** una sola disposición por nivel en todo el campo (960, 60, 60 y 60 partidas). El nivel 14 tiene la misma disposición que P7-30 a P7-65.
- **Las estatuas no se mueven.** A cada observación responden «none» (`pasiva_P7_67.py:1-2,7,19`).

## 4. Semillas

**La misma regla en todos los campos**
- Una semilla por día de serie, y **la misma para todos los brazos ese día**. En P7-67, la misma también para todos los niveles.
- La fórmula es 20260916 + k × 104729.
- Comprobado en las respuestas, `game_config.seed` frente al archivo: 0 casos con más de una semilla para un mismo día entre brazos. Las 1.146 partidas de P7-67 y todas las de los demás campos cuadran.

**Campo por campo**
- **P7-30:** `semillas_P7_30.json`, k 178-197 (`:46`). La serie 2 son las mismas 20 semillas en orden inverso (nota en `:68`). Uso en `lanza_P7_30.py:28,30`; sello en `SELLO_P7_30.md:13-15`.
- **P7-34:** `semillas_P7_34.json`, k 201-220, serie 2 inversa. Uso en `lanza_P7_34.py:30,32`; sello en `SELLO_P7_34.md:21-23`.
- **P7-45, P7-50, P7-56, P7-61 y P7-65:**
  - `semillas_P7_41.json`, k 221-240 (`:68`).
  - Orden de las series:
    - serie 1 en orden;
    - serie 2 inversa;
    - serie 3 rotada diez posiciones (nota en `:90`).
  - Los cinco campos juegan los mismos 60 mapas.
  - Sellos: `SELLO_P7_42.md:25`, `SELLO_P7_49.md:13-14`, `SELLO_P7_56.md:14`, `SELLO_P7_61.md:18`, `SELLO_P7_65.md:23`.
  - `semillas_P7_61.json` (series 4-6) se preparó para P7-61, pero la serie 4 se canceló y no se jugó ninguna partida con ellas (`SELLO_P7_61.md:88-96,119`).
- **P7-67:**
  - k = 261 + 20 (serie − 1) + (día − 1), de 261 a 580 (`SELLO_P7_67.md:45-46`; `disena_P7_67F.py:8-9`).
  - Cada serie trae 20 semillas nuevas, sin inversión ni rotación.
  - Las series 1-6 de los niveles 2, 3 y 14 juegan los mapas de las series 1-6 del nivel 1.

## 5. El cuerpo del siete

- **Parte del cuerpo congelado del seis.**
  - «`policy_pareja11.py` (A4, el cuerpo congelado del seis) + `descubre_P7.aplica`…» (`policy_pareja_P7.py:1`), sin tocar ni un byte de él (`:3`).
  - En el arranque de un diario de P7-50 (`P750_s1_d1_COMPARTE_43406025`, asiento 10, `:3`): `"cuerpo":"v42_exp + ojos v1 + oido y don (P6-6) + pareja al parte y mochila llena (P6-8b) + S-COMPANIA rescate (P6-10) + mano vacia amenaza menor (P6-11)"`.
- **Sensación de distancia a la hermana: sí.**
  - **S-COMPANIA** crece con la distancia a la hermana (`paintball/alma/appraisal_zs_v42_exp.py:1003-1037`). En el campo se usa la reconfiguración del seis: `"D0":7, "TECHO":0.32` (`P750` asiento 10, `:3`). Descripción en `informe_P7_49a.md:24`.
  - Las filas F-HERMANO-AMENAZA y F-HERMANO-GOLPE también están en el cuerpo (`appraisal_zs_v42_exp.py:16-19`).
  - El vínculo B es `mem.roce_B` (`informe_P7_48.md:14`).
- **Ojos compartidos: solo desde P7-48, no en todo el siete.**
  - Apagados de P7-5 a P7-47, con `GEMV_OJOS=0` (`Dockerfile.pareja_P7:148`; `informe_P7_23.md:34`). Esto incluye los campos P7-30, P7-34 y P7-45.
  - Encendidos desde P7-48, con `GEMV_OJOS=1` (`Dockerfile.pareja_P7_48:283` y siguientes; `SELLO_P7_49.md:8`; `informe_P7_50.md:8`). Es decir, en P7-50, P7-56, P7-61, P7-65 y P7-67.
- **El parte no va justo cada segundo.**
  - Con los ojos encendidos, el parte E2 sale **cada 25 tics**: `CADA = 25` en `paper6/parte2.py:59`, porque «25 > 24 garantiza como mucho uno por segundo» (`:50`). Lo confirma el diario de P7-50: `"voz_cada_ticks":25` (`:3`).
  - Con los ojos apagados (P7-30, P7-34 y P7-45), el parte E1 sale cada 48 tics (`paintball/alma/policy_cortex.py:150`).
  - El canal admite un mensaje cada 24 tics (`informe_P7_48.md:10`).
  - El M7 ocupa un hueco del E2: «nunca dos seguidos, el parte no se pierde mas de 25 tics» (`hermanas_P7_48.py:10-11`).

## 6. Tamaño del mapa

**48 × 48 casillas en los ocho campos.**
- El registro `static_map` lleva `"size":48` y 48 filas de 48. Está en el diario del asiento 10:
  - en la línea 5 en P7-30 y P7-34;
  - en la 6 en P7-45, P7-50, P7-56, P7-61 y P7-65;
  - en la 11 en P7-67.
- Centro de la zona: [24, 24].

## 7. Partidas y créditos de la plataforma en todo el siete

**Totales que dan las fuentes**
- **710 partidas = 710 créditos hasta P7-37.** Están contadas de los estados de P7-5 a P7-34 (`informe_P7_37.md:3-4`; `paper5/ACTA.md:6813`). Hasta P7-34 las fuentes apuntaban dólares, no créditos.
- **475 en el campo del capítulo 3 (P7-42 a P7-45).** Son:
  - 360 de campo;
  - 3 de humo;
  - 112 fuera de resultados: piloto 1, 95; piloto 2, 13; un humo que murió al arrancar, 3; un intento parado, 1.
  
  El acumulado es **1.185** (`informe_P7_45.md:3-4`; `ACTA.md:6922`).
- **Después de P7-45 ninguna fuente da un acumulado.**

**Lo apuntado después de P7-45**

| experimento | partidas pedidas | fuente |
|---|---|---|
| P7-50 | 126 (120 válidas, con el humo dentro; 4 reintentos; 2 apartadas) | `informe_P7_50.md:3` |
| P7-56 | 124 (120 + 4 reintentos); «hay partidas que cuentan 0 créditos» | `informe_P7_56.md:50-51` |
| P7-61 | 122 (humo, 3 series y 2 reintentos) | `informe_P7_61_intermedio.md:73` |
| P7-63 (humo) | 3 | `informe_P7_64.md:104` |
| P7-65 | 122 (1 crédito por partida) | `informe_P7_65.md:198` |
| P7-67, banco 1 | 8 | `informe_P7_67.md:136` |
| P7-67, banco 2 | 8 | `informe_P7_67_segundo_banco.md:125` |
| P7-67, campo | 1.146 (1.140 + 6 reintentos de apartadas) | `informe_P7_67_campo.md:162` |

- **Suma de las cifras apuntadas** (no está escrita en ninguna fuente): 1.185 + 126 + 124 + 122 + 3 + 122 + 8 + 8 + 1.146 = **2.844 partidas pedidas en la plataforma en todo el siete.**
- Los demás pasos (bancos, trabajo local y las erratas) apuntan 0.

**Los créditos son como mucho 2.844, no el gasto exacto**
- «Hay partidas que cuentan 0 créditos» (`ACTA.md:7061`; `informe_P7_56.md:50-51`).
- `P7_65_creditos.json` mide 106 créditos en 107 partidas.
- El saldo de ahora no consta: la plataforma devuelve 404 (`informe_P7_67_campo.md:162`). El último saldo leído es 76, antes de la serie 3 de P7-65 (`informe_P7_65.md:198`).

**Contradicciones entre fuentes y cuál vale**
- **Acumulado de P7-43.** `ACTA.md:6880` da 942, `informe_P7_43.md:4` da 944 y `ACTA.md:6901` da 945. Los corrige el cierre de P7-45 (475 y 1.185), que cuadra con los estados: 363 + 1 + 3 + 13 + 95.
- **Partidas de P7-56.** `ACTA.md:7061` da 87 partidas en las series 1-2 (3 de humo + 80 + 4) y parece contar el humo dos veces. Vale el informe final, 124.

## Gasto de este paso

- Créditos de la plataforma: 0.
- Dólares de la consola de Anthropic: 0.

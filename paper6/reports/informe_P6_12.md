# P6-12 · Congelar «el cuerpo del seis»

*27-sep-2026. Coste cero: ninguna partida nueva, ninguna llamada de pago.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1` (comprobado); los 202
archivos de `cantera/paper5/CONGELADO.md`: 0 alterados (comprobado). La clave
no entra en ningún archivo ni en git (dos barridos, abajo). Sin propuestas de
diseño.*

**El archivo de la congelación es `cantera/paper6/CONGELADO_P6.md`**: inventario
real, configuración, mundo y semillas, prueba de reproducción, línea base A0/A4
y precios que se quedan dentro. Aquí va cómo se hizo cada cosa, lo que salió
por el camino, el git y el punto 6.

## 1 · Inventario real (`inventario_P6_12.py` → `P6_12_inventario.json`)

No de memoria: se carga `policy_pareja11` con el entorno de la imagen
(`Dockerfile.pareja11`), se aplican sus envoltorios y se replayan 600 tics de
una vida real por la vía real, trazando `sys.modules` (archivos del
repositorio) y `open()` (datos). **32 archivos son el cuerpo**: `motor/model.py`,
`planificador/` (2), `paintball/alma/` (15: `policy_cortex`, `policy_forma`,
`decisor_zs`, `appraisal_zs_v42_exp`, `appraisal_zs`, `mundo`, `parte`,
`cortex_t5`, `relator_t5`, `forma_viva`, `hilo_forma`, `formas_azar`,
`confianza_viva`…), `cantera/paper5/` (6: `forma`, `traductor_forma`,
`proyeccion`, `alcance_g`, `curiosidad`, `curiosidad_forma`) y `cantera/paper6/`
(9: `policy_pareja11`, `policy_pareja`, `parte2`, `oyente2`, `oido5_P6_5`,
`arreglos_P6_6`, `arreglos_P6_8b`, `filas10_P6_10`, `amenaza11_P6_11`). Los
md5 están en `CONGELADO_P6.md § 1`.

Dos cosas que solo se ven trazando: **la memoria aprendida no se carga**
(`appraisal:383` solo la lee con `MIEDO_ON`, que `policy_cortex.py:95` pone a
`False`), y los archivos del consejero (`instruccion_forma.md`,
`tabla_ensenada.md`, `P56A_distribucion_azar.json`) viajan en la imagen pero no
se abren con las puertas a 0.

## 2 · Configuración (`config_P6_12.py` → `P6_12_config.json`)

Leída de los módulos con el cableado de `policy_cortex` y el entorno de la
imagen, y de los datos (roster, semillas, respuestas de la plataforma):
D0 = 7, techo 0,32, rango D0·(1+2·calma); S-SOLEDAD sin tocar; `~manos` 3/1 y
`~manos_pegando` 18/1; CADUCIDAD_RIVAL 50, UMBRAL_REC 0,3; N = min(d·11+268,
720); empatía True / 0,25 / 1,0, miedo y extraño False; E2 cada 25 tics, gemelo
E1. Mundo 0.1.19, `cow_6a55df20-08d1-4e4c-adba-33dbd97e1e6f`, liga
`league_6764202e…`, `roster_lento_v2_PROPUESTA.json`
(`3eb7dd60d8f43be2751b0325945a3f27`), las 20 semillas de `semillas_S2.json[:20]`,
iguales a las jugadas en A4 (comprobado). Tabla completa en `CONGELADO_P6.md § 2`.

## 3 · Prueba de que el congelado es el de verdad (`reproduce_P6_12.py`)

Cuatro vidas de A4 (dos partidas) replayadas en seco con solo los archivos del
inventario, por la vía real: **tres al bit** (39.542 decisiones iguales,
|Δd| = 0 en 10.917 candidatos). En la cuarta, 54 de 12.576 decisiones (0,43 %)
difieren —todas `atacar_*` contra `noop`— porque **el diario guarda
`damage_dealt` como entero, no como lista**, y el replay no reconstruye el hp
estimado del rival. Límite del diario, declarado.

Dos fallos del propio reproductor, cazados y corregidos sin tocar el banco de
P6-11: (i) leía `hp = 0` como 100 (`r.get("hp") or 100`) — en el tic 12.990 de
`20260916` s11 el cuerpo real usó el botiquín con hp 0 y el replay no; (ii)
hasta P6-11 los replays no encendían la empatía (P6-11 § 1.4). Con los dos
arreglados, las tres vidas salen exactas.

## 4 · `CONGELADO_P6.md`

Escrito: inventario y md5, configuración y mundo, prueba de reproducción, la
tabla A0 contra A4 (vida 12.427,9 → 12.840,2; juntos 79,1 % → 77,3 %;
supervivientes 8 → 11; los dos al cierre 18 → 19; muertes anillo·rival·no
consta 20·11·1 → 22·6·1; golpes; comida 3,20 → 2,88), y los precios con su
número (comida 2,88; anillo 22; mano vacía 148; `ir_pareja` 2,88 %; don
reabsorbido 29 de 90).

## 5 · Git

**Qué entra:** todo `cantera/paper6/` (código, humos, medidores, informes,
sellos, JSON de medidas y de peticiones, GIF) salvo `P6_2_bruto.json` (40 MB,
> 5 MB) y los diarios; más `cantera/paper5/ACTA.md`. **Qué no entra:**
`paintball/runs/` (los 560 diarios y zips de las series del seis, 8,48 GiB,
con su md5 en `cantera/paper6/DIARIOS_P6_MANIFIESTO.md`), `Claude outputs/`,
`.claude/`, y los restos de papers anteriores que ya estaban sin seguimiento
(`paintball/*.md`, `paper3/`, `runs_mapa/`…), que no son del seis.

**Dos barridos de secretos** sobre lo que entra (384 archivos):
1. Regex (`sk-ant-…`, `ANTHROPIC_API_KEY=…`, `api_key`, `Bearer`, `AKIA…`,
   claves privadas): dos avisos en `informe_P6_1.md`, líneas 39 y 47, y los dos
   son el texto `ANTHROPIC_API_KEY=` seguido solo de puntuación (comprobado sin
   imprimirlo): no hay clave.
2. Entropía (tokens ≥ 28 caracteres con entropía > 4,2 bits, excluidos md5,
   uuid y rutas): 5 avisos, todos identificadores de la plataforma
   (`policy_version_id=<uuid>` en el acta, `round_<uuid>` en los volcados de la
   liga): no hay clave.
`cantera/paper5/.env` existe y está ignorado por git (comprobado con
`git check-ignore`).

Commit local **«cuerpo del seis, congelado»** y etiqueta local
**`cuerpo6-congelado`**. Sin push. El hash está en `git log`.

## 6 · Dónde se engancharía el consejero del cinco (solo mirar)

Localizado en el código, sin escribir nada:

* **Por dónde entra un plan.** Dos vías, las dos vivas en el cuerpo: (a) el
  córtex: `policy_cortex.py` (`AlmaCortex`) toma propuestas de
  `cortex_t5.Cortex` (que llama al modelo en `_llama`, `cortex_t5.py:891`,
  con `BEDROCK_MODEL`) y las convierte en candidatos con nombre `_CX_ir_<x>_<y>`
  y receta del propio decisor (`policy_cortex.py:389`; la variante «tonta» de
  `:370-405` enseña el molde); (b) las formas: `policy_forma.AlmaForma`
  mantiene `self.vivas` (`FormaViva`, `forma_viva.py:28`), les da la base de
  candidatos con `forma_viva.pon_base` (`policy_forma.py:683`), las revisa en
  `_revisa_vivas` (`:772`) y `_abandonos_K` (`:879`), y las valora con las
  curvas de `forma.py` (`curva`, `juzga_forma`, `forma_de_candidato`).
* **La puerta ancha y el compromiso.** La puerta ancha es `GEMV_FORMA`
  (`policy_forma.py:11` y `:64`, «la puerta ancha honesta en vivo»); el
  compromiso es `AlmaForma._compromiso` (`policy_forma.py:1624`, «con piernas
  listas y sin ruptura, se EJECUTA el paso de la forma»), aplicado en `:1559`
  bajo `CUR_FORMA_ON` (`GEMV_CURIOSIDAD_FORMA`), con las siete rupturas en
  `_rupturas` (`:1568`).
* **El idioma de las formas.** `traductor_forma.traduce` y `de_propuestas`
  (texto del modelo → forma con tramos), `instruccion_forma.md` («No le des
  órdenes: dale formas… en el idioma que el cuerpo entiende») y
  `tabla_ensenada.md` (la tabla explicada donde engaña), y **`hilo_forma`**:
  la forma aceptada codificada para el canal `team` (`GF1|<tramo>;…|hp,W,herido`,
  ≤ 120 ASCII, un mensaje cada 24 tics, `cabe()`), con `codifica/decodifica`.

**¿Se cargan tal cual con el cuerpo congelado?** Sí, comprobado con
`enseco_P6_12.py`: importación en seco de `policy_cortex`, `policy_forma`,
`cortex_t5`, `hilo_forma`, `forma_viva`, `relator_t5`, `forma`,
`traductor_forma`, `curiosidad_forma` y `curiosidad` con el entorno de la
imagen y la red bloqueada (`urllib.request.urlopen` reventaría): todas las
piezas existen, **0 llamadas de red**, y con las puertas a 0 el cuerpo es el
congelado bit a bit (los humos de red de P6-10 y P6-11 corrieron `AlmaPareja`
entera con esas mismas puertas). Ya estaban en el inventario: el cuerpo las
importa aunque no las use.

**Lo que falta para que dos consejeros, uno por hermano, hablen a través de
sus cuerpos por el canal de equipo** (solo la lista; nada escrito):

1. **El canal está ocupado.** El mundo da un mensaje de ≤ 120 caracteres cada
   24 tics por agente, y el seis lo usa entero para el E2 (cada 25 tics,
   mediana 100 caracteres, máximo 117 medido). El `GF1` de `hilo_forma` (hasta
   71 caracteres) fue escrito para ese mismo hueco cuando estaba libre. No
   caben los dos en el mismo mensaje sin decidir cómo se reparten o se
   alternan; y el oído del seis (`oido5` + `oyente2`) solo lee `E2`.
2. **Ningún oyente de formas del hermano.** El cuerpo emite `GF1` con
   `GEMV_HILO_FORMA=1`, pero en el seis nadie lo decodifica al recibirlo:
   `hilo_forma.decodifica` existe y no está enganchado al chat entrante; el
   `_diario_hermano` de `policy_forma` (`:586`) es lo más cerca que hay.
3. **Un consejero por asiento, con su presupuesto.** `cortex_t5.Cortex` y el
   consejero de formas llevan tope de llamadas (150 / 200) y de gasto (1 USD)
   por proceso; cada asiento es un proceso, así que son dos consejeros y dos
   presupuestos, y las dos llaves de modelo (`BEDROCK_MODEL` / la de la casa)
   tendrían que entrar como `--secret-env`, no en la imagen.
4. **El parte del córtex está apagado** (`GEMV_CORTEX_PARTE=0`,
   `cortex_t5.py:81`): existe la pieza que le cuenta al consejero lo que dice el
   hermano, y está a 0.
5. **La forma no sabe de los ojos.** `FormaViva.receta` y las curvas de
   `forma.py` se construyen con la base de candidatos del decisor, que ya lleva
   los contados y las filas del seis; pero el traductor y la instrucción
   (`instruccion_forma.md`) no nombran rivales contados, recursos contados,
   S-COMPANIA ni la amenaza menor: el idioma del cinco no tiene esas palabras.
6. **Un banco y un sello propios.** Nada de lo anterior está medido: antes de
   construir contra ello se mide el daño (regla de la casa).

## LOS ARCHIVOS NUEVOS DE P6-12

`CONGELADO_P6.md`, `DIARIOS_P6_MANIFIESTO.md`, `inventario_P6_12.py`,
`config_P6_12.py`, `reproduce_P6_12.py`, `enseco_P6_12.py`,
`P6_12_inventario.json`, `P6_12_config.json`, `P6_12_reproduce.json`. Sus md5
quedan en el commit.

## CONTROL FINAL

| | |
|---|---|
| `motor/model.py` | `1e511978c251130e95169ebf8443efa1` — intacto |
| archivos de `CONGELADO.md` (cinco) | 202 comprobados, 0 alterados |
| partidas · llamadas de pago | 0 · 0 |
| secretos | 2 barridos, ninguno |
| push | no |

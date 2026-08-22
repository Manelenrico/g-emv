"""G-EMV policy para Coworld machina_1 — Fase 2 (memoria espacial).

Motor:     motor/model.py (INTOCABLE)
Appraisal: appraisal/appraisal_v3.py
Memoria:   memoria/memoria_v1.py  (interruptor GEMV_USE_MEMORY=1, default=0)
Protocolo: coworld.player.v1 WebSocket

Sin lookahead multi-paso, sin bootstrap, sin heurísticas de juego.
El cerebro ES el motor. La memoria añade campo fantasma; OFF reproduce Fase 1
bit a bit.

Predicción 1-paso local:
  Para cada acción, construye tokens_pred:
  1. Tokens espaciales (no-AGENT, no-GLOBAL, no-PADDING):
     desplazados por (old_row - drow, old_col - dcol). Tokens que
     salen de [0,12]×[0,12] se descartan (celdas desconocidas = vacías).
  2. AGENT_LOC inv:energy p0 (fid=24): se descuenta move_energy_cost=4.
     Si p0 < 4, se gestiona prestando del p1 (fid=25). Noop: sin coste.
  3. AGENT_LOC territory:here (fid=69): se actualiza con territory:N/S/E/W
     (fid=70/71/72/73). Encoding norm=9 → val%3 como territorio inmediato
     (suposición pendiente de verificación empírica; funciona para TERR_NEUTRAL=0).
  4. El resto de tokens de AGENT_LOC (hp, gear, tags, etc.): sin cambio.
  Luego: appraise(tokens_pred, team_side, s_scale) → State_pred → opponent_distance.
  Elegir argmin d_pred. Ties: orden lexicográfico de action_names.

Variables de entorno de test:
  GEMV_INJECT_HP:           HP inyectado (ej. 25); decay lineal en GEMV_INJECT_STEPS pasos.
  GEMV_INJECT_ENERGY:       energía inyectada (ej. 5); decay lineal en GEMV_INJECT_ENERGY_STEPS pasos.
  GEMV_INJECT_STEPS:        pasos de decay para HP (default 2000).
  GEMV_INJECT_ENERGY_STEPS: pasos de decay para energía (default = GEMV_INJECT_STEPS).
  GEMV_INJECT_HP_DELAY:     pasos antes de iniciar inyección HP (default 0).
  GEMV_S_SCALE:             multiplicador del eje S para barrido (default 1.0).
  GEMV_USE_MEMORY:          0=OFF (Fase 1 exacto), 1=memoria_v1 (suma bruta),
                            2=memoria_v2 (habituación logarítmica, default para Fase 2b).

Log por tick: una línea JSON a stderr con prefijo GEMV_TICK para parseo.
"""
from __future__ import annotations

import asyncio
import json
import math
import os
import sys
from pathlib import Path

import websockets

sys.path.insert(0, str(Path(__file__).parent.parent))
from motor.model import DEFAULT_CONFIG, ModelConfig, opponent_distance

# GEMV_W_S / GEMV_W_F — barrido de temperamento: w_s_pos (social) / w_f_pos (físico) escalados; ratio pos/ten
# conservado por eje. 0 ó no seteado en un eje = ese eje sin cambio. model.py INTOCABLE (se construye un
# ModelConfig aparte, nunca se toca DEFAULT_CONFIG salvo lectura). GEMV_W_F es el espejo físico de GEMV_W_S.
def _build_active_cfg(ws_override: float, wf_override: float) -> object:
    if ws_override <= 0 and wf_override <= 0:
        return DEFAULT_CONFIG                      # bit-exact: sin override, config por defecto
    cfg = ModelConfig()
    if ws_override > 0:
        cfg.w_s_pos = ws_override
        cfg.w_s_ten = DEFAULT_CONFIG.w_s_ten * (ws_override / DEFAULT_CONFIG.w_s_pos)
    if wf_override > 0:
        cfg.w_f_pos = wf_override
        cfg.w_f_ten = DEFAULT_CONFIG.w_f_ten * (wf_override / DEFAULT_CONFIG.w_f_pos)
    return cfg
_WS_OVERRIDE: float = float(os.environ.get("GEMV_W_S", "0"))
_WF_OVERRIDE: float = float(os.environ.get("GEMV_W_F", "0"))
_ACTIVE_CFG: object = _build_active_cfg(_WS_OVERRIDE, _WF_OVERRIDE)
from appraisal.appraisal_v3 import (
    appraise as _appraise_v3, appraise_with_debug, parse_tokens,
    AGENT_LOC, GLOBAL_LOC, PADDING_LOC,
    EGOCENTRIC_COLS, AGENT_ROW, AGENT_COL,
    FID_TAG, FID_INV_ENERGY, FID_INV_CARBON, FID_TERRITORY_HERE,
    TAG_TEAM_COGS, TAG_TEAM_CLIPS, TAG_TYPE_AGENT, TAG_TYPE_HUB,
    EXTRACTOR_TAGS,
    get_scalar, get_multipart, iter_spatial_locs,
)
# GEMV_APPRAISAL=4 activa el canal social de v4 (f⁻_S += k·demanda; k=0.15 declarado, NO recalibrado).
# v4 ENVUELVE v3 (hereda todos los fixes territoriales/tag); con k=0 ⇒ v4≡v3 bit a bit.
_APPRAISAL: str = os.environ.get("GEMV_APPRAISAL", "3")
if _APPRAISAL == "4":
    from appraisal.appraisal_v4 import (appraise, COVERAGE as _COVERAGE,
                                        A_UNIT as _A_UNIT, FID_ACTS_DONE as _FID_ACTS_DONE)
else:
    appraise = _appraise_v3
    _COVERAGE, _A_UNIT, _FID_ACTS_DONE = "v1_linear", 0.0, 250

# ── GEMV_SHELF — compresión multi-variable del eje R (tanda propia, INTOCABLE valores base) ──
# GEMV_SHELF=1 activa appraise_shelf(shelf_on=True) como drop-in de appraise para TODOS los
# consumidores (predicción 1-step, planificador H≥2, estado actual). OFF=0 ≡ bit-exact con v4/v3.
# Requiere GEMV_APPRAISAL=4 para coherencia (shelf wrappea _appraise_v4 internamente).
_GEMV_SHELF: bool = os.environ.get("GEMV_SHELF", "0") in ("1", "on", "ON", "true")
# ── GEMV_HEARTS (Eslabón 1) — balda de hearts en R + transición make. [doc de diseño interna, no en el repo] ──
# Requiere GEMV_SHELF (la balda viaja dentro de appraise_shelf) y COVERAGE=v2_hybrid (la make
# comparte el bump-al-hub del depósito). OFF=0 ≡ v6 bit-exact. FID inv:heart leído del config.
_HEARTS: bool = os.environ.get("GEMV_HEARTS", "0") in ("1", "on", "ON", "true")
FID_INV_HEART: int = 22   # inv:heart p0 (LEÍDO del player_config en _sane_world_ids; 22 = default)
# Eslabón 4 — GEMV_MARCADOR: balda territorial (R+S) + transiciones equipar-aligner/alinear-junction +
# atractores junction/gear-station/hub. OFF=0 ≡ e3 bit-exact. Ids leídos del config.
_MARCADOR: bool = os.environ.get("GEMV_MARCADOR", "0") in ("1", "on", "ON", "true")
# Córtex C1 — GEMV_CORTEX_PRIOR: mapa de nacimiento (lo fijo entre vidas) pre-poblado en la memoria
# con confianza moderada (0.5). El córtex INFORMA, no gobierna: percepción manda, ghost sin tirón nuevo.
# OFF=0 ≡ e4 bit-exact. El atlas se destila offline (cortex/destilar_fijo.py → cortex/atlas_fijo.json).
_CORTEX_PRIOR: bool = os.environ.get("GEMV_CORTEX_PRIOR", "0") in ("1", "on", "ON", "true")
_CORTEX_HALFLIFE: int = 500     # edad inicial del prior ⇒ conf exp(-λ·500)=0.5 con la curva estándar
_cortex_ctx: dict = {'loaded': False, 'atlas': None}
if _CORTEX_PRIOR:
    try:
        import json as _cjson
        for _p in ("cortex/atlas_fijo.json", "/app/cortex/atlas_fijo.json"):
            if os.path.exists(_p):
                _cortex_ctx['atlas'] = _cjson.load(open(_p)).get('atlas', [])
                break
    except Exception:
        _cortex_ctx['atlas'] = None
FID_INV_ALIGNER: int = 26          # inv:aligner p0
TAG_TYPE_JUNCTION: int = 13        # type:junction
TAG_TYPE_ALIGNER: int = 9          # type:aligner (gear station del aligner)
TAG_NET_COGS: int = 5; TAG_NET_CLIPS: int = 4
# ── Córtex C2 — GEMV_CHAIN: la imaginación que encadena (territorial como fuerza-d). [doc de diseño interna, no en el repo] ──
# La cadena PROPAGA el Δd del align (ya modelado/gateado en e4) hacia el terminal donde se equipó,
# descontado por confianza (memoria) y distancia (γ^D). No crea valor. Requiere _MARCADOR. OFF ≡ C1/e4 bit-exact.
_CHAIN: bool = os.environ.get("GEMV_CHAIN", "0") in ("1", "on", "ON", "true")
CHAIN_MAX_DEPTH: int = 2            # equipar→alinear (declarado; ampliar = decisión nueva, D2.4)
CHAIN_GAMMA: float = 0.9           # descuento geométrico por celda L1 restante al eslabón final (D1-ii)
# ── Córtex C3 — GEMV_WAYPOINTS: las migas de pan (rutas del atlas re-apuntan el susurro N3). [doc de diseño interna, no en el repo] ──
# Cuando N3 apunta a un destino fijo off-ciclo (gear station) FUERA de alcance (>H-1), el atractor se
# re-expresa como la siguiente MIGA de la ruta precomputada. Solo re-apunta el susurro; no crea fuerza.
# Percepción manda (miga-muro se salta). OFF ≡ C2/C1 bit-exact. Rutas: cortex/rutas.json (destilar_rutas.py).
_WAYPOINTS: bool = os.environ.get("GEMV_WAYPOINTS", "0") in ("1", "on", "ON", "true")
TAG_TYPE_WALL: int = 20            # type:wall (para la desmentida perceptual de una miga)
# ── Córtex C4 — GEMV_GAIN: el segundo pedal (appraisal de ganancia). [doc de diseño interna, no en el repo] ──
# El motor tiene equilibrio DESCENTRADO a ganancia (proactividad); el appraisal hasta hoy alimentaba casi
# solo f− (déficits). C4 cablea f+: la oportunidad territorial (junction ganable conocida/recordada) como
# FUERZA-d PROPAGADA por proximidad — el Δd del align (ganancia ya modelada), descontado por distancia a la
# gear (γ^L1) y confianza, aplicado a CADA terminal → gradiente continuo (fuerza, no susurro N3). Vertical-
# primero emerge del orden (empates N/E → norte). + hearts-riqueza f+R saturante. OFF ≡ C3 bit-exact.
_GAIN: bool = os.environ.get("GEMV_GAIN", "0") in ("1", "on", "ON", "true")
GAIN_GAMMA: float = 0.85           # descuento por celda L1 del terminal a la gear (gradiente de oportunidad)
# ── Córtex (2) — GEMV_ROLLOUT_DISCOUNT: descuento temporal DENTRO del rollout. [doc de diseño interna, no en el repo] ──
# El crédito de la transición (equipar, que empaqueta el Δd del align vía `chain`) se descuenta γ^k según el
# PASO k del rollout donde se ejecuta el equip (aligner 0→1). "Equipar ya" > "equipar en 7 pasos" por
# construcción → el compromiso con la estación (y detrás, la junction) emerge del valor bien descontado, no de
# reglas de adyacencia. γ = CHAIN_GAMMA (la misma de C2). Requiere _CHAIN∧_MARCADOR. OFF ≡ C4 bit-exact.
_ROLLOUT_DISCOUNT: bool = os.environ.get("GEMV_ROLLOUT_DISCOUNT", "0") in ("1", "on", "ON", "true")
# ── Córtex (3) — GEMV_CHAIN_COMPLETE: la cadena propaga HASTA EL FINAL. [doc de diseño interna, no en el repo] ──
# La fuerza territorial (C4) SIEMPRE fue de la junction; la gear tenía valor PRESTADO por la cadena (hay que
# equipar para poder alinear). El bug de §ANEXO 6: la propagación apuntaba a la gear y, al equipar, no
# avanzaba al siguiente eslabón (la junction) → el agente equipado orbitaba la gear. Arreglo: SIN aligner la
# fuerza apunta a la gear (valor prestado, equipar); CON aligner∧heart∧junction-ganable-conocida apunta
# DIRECTO a la junction (el eslabón final). El bump-align tiene valor INTRÍNSECO (align_junction_bump añade
# net:cogs → territorial_RS mejora), a diferencia del equip; no hace falta crédito analítico. Candados de
# siempre (junction conocida/recordada, heart vivo, saturación). Requiere _GAIN∧_MARCADOR. OFF ≡ C5 bit-exact.
_CHAIN_COMPLETE: bool = os.environ.get("GEMV_CHAIN_COMPLETE", "0") in ("1", "on", "ON", "true")
# ── PREGONERO v1 — GEMV_PREGONERO: la memoria compartida (hechos de mundo entre compañeros). [doc de diseño interna, no en el repo] ──
# La consolidación mostró que s2/s4/2º-punto mueren por no VER; los compañeros SÍ ven. Canal: el workspace
# ($O) se monta rw en TODOS los contenedores de jugador en /coworld-artifact (runner.py:319) → tablón vivo
# compartido. Cada agente PUBLICA sus junctions vistas de 1ª mano (pos absoluta canónica + tick de visión) a
# pregonero_<slot>.jsonl (anti-eco: solo lo que sus ojos vieron, nunca hearsay). CONSUME los tablones AJENOS e
# inyecta las junctions FUERA de su ventana en la memoria EXISTENTE con confianza MENOR (last_seen = tick −
# PENALTY, misma curva de decaimiento que todo; mismo mecanismo que el cortex-prior conf 0.5). PERCEPCIÓN
# MANDA: lo que cae en mi ventana lo deciden mis ojos (no inyecto ajeno ahí). Sin reputación por fuente (v2).
# El consumidor (ganancia/atractores/juez) NO cambia: solo le llegan más objetos por el canal de siempre.
# Requiere _MARCADOR (junctions). OFF ≡ bit-exact. Con un solo agente en el canal, ON ≡ OFF (no hay ajenos).
# ── GEMV_DISK: disco de percepción REAL, RE-ESCOPADO a SOLO el candado del pregonero-consume ──
# La visión NO es el cuadrado 13×13 sino un DISCO L2: medido, visible ⟺ dr²+dc²≤37 (R≈6.08; pregonero/
# [doc de diseño interna, no en el repo]). El disco solo se usa en `_pregonero_consume` (código NUEVO, sin baseline previo: ahí es
# correctitud — no descartar soplos de junctions de esquina que el disco recorta). Los candados de memoria
# pre-existentes (_present/remembered/exclusión-ghost) SIGUEN con el CUADRADO como línea base VALIDADA C6
# (cambiarlos a disco perturbó la navegación: s0 dejaba de puntuar → es un eslabón propio, deuda §disco).
# OFF ≡ cuadrado bit-exact. Inerte sin PREGONERO (nadie llama _in_view).
_DISK: bool = os.environ.get("GEMV_DISK", "0") in ("1", "on", "ON", "true")
PERCEPTION_R2: int = 37     # radio² del disco de visión (medido; máx percibido L2=6.08=√37)
def _in_view(dr: int, dc: int) -> bool:
    """¿La celda ego (dr,dc) está dentro del disco de percepción REAL? Con _DISK: dr²+dc²≤37; sin él: cuadrado ±6.
    Solo lo usa _pregonero_consume (el candado de memoria pre-existente conserva el cuadrado; ver deuda §disco)."""
    return (dr * dr + dc * dc <= PERCEPTION_R2) if _DISK else (abs(dr) <= 6 and abs(dc) <= 6)
_PREGONERO: bool = os.environ.get("GEMV_PREGONERO", "0") in ("1", "on", "ON", "true")
PREGONERO_BOARD_DIR: str = os.environ.get("GEMV_PREGONERO_DIR", "/coworld-artifact")   # workspace montado
PREGONERO_PENALTY: int = int(os.environ.get("GEMV_PREGONERO_PENALTY", str(_CORTEX_HALFLIFE)))  # conf inicial 0.5 (mismo precedente que el cortex-prior)
_pregonero_seen: dict = {}    # {(wr,wc): (cls, last_seen_step)} — sightings de PRIMERA MANO (para publicar; anti-eco)
# PUENTE PREGONERO↔MOTOR (2026-07-29): las clases de HECHO DE MUNDO que el canal comparte. v1 solo junctions;
# se añaden los EXTRACTORES (extractor_*) para que un extractor conocido POR PREGÓN cuente como extractor-conocido
# para la cara MINADO del motor (que ya lee mem._entries). Ni estados internos ni intenciones (eso sería v2/v3).
_PREGONERO_CLASSES = ("junction_gray", "junction_rival", "junction_own",
                      "extractor_oxygen", "extractor_carbon", "extractor_germanium", "extractor_silicon")


def _pregonero_publish(slot: int) -> None:
    """Reescribe pregonero_<slot>.jsonl con las junctions vistas de PRIMERA MANO por este agente (anti-eco:
    nunca se publica lo oído). Escritura atómica (tmp+replace). Falla en silencio si no hay tablón montado."""
    if not _PREGONERO or slot < 0 or not _pregonero_seen:
        return
    try:
        path = f"{PREGONERO_BOARD_DIR}/pregonero_{slot}.jsonl"
        tmp = path + f".tmp{slot}"
        with open(tmp, "w") as f:
            for (wr, wc), (cls, ls) in _pregonero_seen.items():
                f.write(json.dumps({"wr": wr, "wc": wc, "cls": cls, "tick": ls, "slot": slot}) + "\n")
        os.replace(tmp, path)
    except Exception:
        pass


def _pregonero_consume(mem, slot: int, world_step: int) -> int:
    """Lee los tablones de los OTROS slots e inyecta sus junctions en la memoria propia con confianza MENOR
    (last_seen = tick_visión − PENALTY). Candados: (i) PERCEPCIÓN MANDA — junctions dentro de mi ventana (±6)
    NO se inyectan (mis ojos deciden); (ii) mis ojos frescos ganan — solo inyecto si es MÁS fresco que lo que
    ya tengo. Devuelve nº de hechos inyectados. OFF/solo-yo ⇒ 0 (bit-exact)."""
    if not _PREGONERO or mem is None or not hasattr(mem, "_record") or not hasattr(mem, "_entries"):
        return 0
    ar, ac = getattr(mem, "_agent_world", (0, 0))
    n = 0
    try:
        import glob
        for path in glob.glob(f"{PREGONERO_BOARD_DIR}/pregonero_*.jsonl"):
            if path.endswith(f"pregonero_{slot}.jsonl"):
                continue                                   # mi propio tablón no se consume
            try:
                lines = open(path).read().splitlines()
            except Exception:
                continue
            for line in lines:
                try:
                    fa = json.loads(line)
                    wr, wc, cls = int(fa["wr"]), int(fa["wc"]), fa["cls"]
                except Exception:
                    continue
                if cls not in _PREGONERO_CLASSES:          # junctions + extractores (el puente al motor)
                    continue
                if _in_view(wr - ar, wc - ac):
                    continue                               # (i) en mi DISCO de visión → percepción manda, no inyecto
                eff = int(fa.get("tick", world_step)) - PREGONERO_PENALTY   # confianza inicial menor, misma curva
                ex = mem._entries.get((wr, wc, cls))
                if ex is not None and getattr(ex, "last_seen_step", -10**9) >= eff:
                    continue                               # (ii) ya tengo algo igual o más fresco → no degrado
                mem._record(wr, wc, cls, 1.0, eff)
                n += 1
    except Exception:
        pass
    return n
# ── OPCIÓN A (ii) — GEMV_ABS_FRAME: anclar la memoria en coords ABSOLUTAS del mundo (lp:*) ──
# Diagnóstico odometría (2026-07-17): el mapeo acción→mov es correcto; la deriva es RUIDO (moves
# bloqueados no contados). El mundo SÍ da posición absoluta (lp:*): global_x=col=lp:east−lp:west,
# global_y=fila=lp:south−lp:north (juego semantic/state.py). Con ABS_FRAME=1 el marco de memoria se
# FIJA a la posición absoluta leída cada tick (odometría = respaldo) → el prior/atlas ancla en absoluto
# y no deriva ni se borra. OFF ≡ dead-reckoning bit-exact. Fids lp:* por defecto (resueltos del config).
_ABS_FRAME: bool = os.environ.get("GEMV_ABS_FRAME", "0") in ("1", "on", "ON", "true")
# GEMV_FIXED_PERSIST: los fijos estructurales (gear stations) NO se borran de memoria por no-percepción
# (oclusión/FOV ≠ ausencia; son permanentes). OFF ≡ bit-exact. Va de la mano de ABS_FRAME para el córtex-prior.
_FIXED_PERSIST: bool = os.environ.get("GEMV_FIXED_PERSIST", "0") in ("1", "on", "ON", "true")
# GEMV_PERSIST_GANABLE (R1 v2 — el matrimonio de las piernas y la memoria): la junction GANABLE recordada
# entra al régimen de persistencia — su POSICIÓN persiste hasta desmentido REAL (re-vista dentro del disco y
# ya-no-gris → corrige), su ESTADO sigue fungible (decae por conf, percepción manda). "El árbol no se olvida:
# lo que se olvida es si tenía fruta." Cierra la FUGA DE CONOCIMIENTO (el paseo del explorador no borra la
# oportunidad recordada por _present) → el relevo jerárquico gain≻forrajeo funciona con memoria que aguanta.
# OFF ≡ bit-exact (persist_ganable=False → candado cuadrado intacto). Va con RUMBO+R1 (el explorador que recuerda).
_PERSIST_GANABLE: bool = os.environ.get("GEMV_PERSIST_GANABLE", "0") in ("1", "on", "ON", "true")
# GEMV_EXTRACTOR_PERSIST (cura del eslabón, retención — espejo de PERSIST_GANABLE para los extractores): un
# extractor es un FIJO (no se mueve); su POSICIÓN persiste fuera del disco de percepción (el tiempo decae el
# ESTADO/conf en el desempate, no la posición). Sólo el desmentido REAL la borra: re-visto DENTRO del disco y
# AUSENTE = minado hasta vaciarse (remove_source_when_empty=true, verificado en fuente). Cura la fuga del anillo
# (el pozo visto una vez y olvidado). El pregón hereda (inyecta en _entries). OFF ≡ bit-exact. JAMÁS atlas horneado.
_EXTRACTOR_PERSIST: bool = os.environ.get("GEMV_EXTRACTOR_PERSIST", "0") in ("1", "on", "ON", "true")
# GEMV_GEODESIC (la métrica honesta): la distancia de la gain (γ^dist) pasa de L1 (ciega al muro) a CAMINO MÁS
# CORTO sobre el mapa CONOCIDO — sólidos conocidos (muros/estaciones/hub/junctions/extractores) bloquean, celdas
# no vistas se asumen caminables (optimismo epistémico: lo no visto invita). BFS/flood-fill sobre el grid ego.
# Cura el atasco "empujar-contra-estación" (s0: L1=4 vs geodésica=6, el miner bloquea el oeste). OFF≡bit-exact
# (gain_field None → L1). Percepción manda: muro/estación descubiertos → la geodesia se recalcula cada tick.
_GEODESIC: bool = os.environ.get("GEMV_GEODESIC", "0") in ("1", "on", "ON", "true")
# GEMV_COMMIT (la cura del 2-ciclo — [doc de diseño interna, no en el repo] opción i): cuando el juez (argmin) elige un plan, el agente
# se COMPROMETE con sus primeros k pasos (el camino DP extraído) antes de replanificar → la replanificación
# miope que crea el 2-ciclo (desde A→B, desde B→A, nunca se recorre el plan) se rompe. El compromiso da
# CONSTANCIA a lo decidido (no gobierna nada nuevo) y se ABORTA al instante si (a) el juego RECHAZA un move
# (desmentido motor), (b) aparece percepción nueva relevante, o (c) crece un dolor real (el sagrado: la
# jerarquía nunca queda retenida). OFF≡bit-exact. k=3 a H≥7; k=H-1 a horizontes cortos (el 2-ciclo tiene
# periodo 2: k≥2 lo rompe por construcción).
_COMMIT: bool = os.environ.get("GEMV_COMMIT", "0") in ("1", "on", "ON", "true")
_COMMIT_K: int = (lambda h: 3 if h >= 7 else max(2, h - 1))(int(os.environ.get("GEMV_HORIZON", "1")))
# GEMV_COMMIT_DEPOSIT (cura del retorno, 2026-07-29, [doc de diseño interna, no en el repo]): COMMIT activo SOLO en la cara DEPÓSITO
# (cargado con lote lleno + hub infabricable, rumbo al hub). Cura el 2-ciclo de MESETA del retorno (el
# cargado llega solo y adyacente al hub, term_spread≈0, y sin compromiso oscila). Fuera de la cara depósito
# COMMIT sigue OFF → NO se reabre la regresión histórica del peldaño 3 (COMMIT global mató la exploración).
# Mismas interrupciones firmadas (rechazo/dolor/oportunidad/mejor-con-margen). OFF≡bit-exact.
_COMMIT_DEPOSIT: bool = os.environ.get("GEMV_COMMIT_DEPOSIT", "0") in ("1", "on", "ON", "true")
# GEMV_COMMIT_MINE (cura del eslabón, HE3): el COMMIT del depósito extendido a la cara MINADO. Con cargo<lote y la
# gain apuntando a un extractor conocido (pozo del elemento-cuello), el minero COMPROMETE la ruta geodésica al pozo
# (misma maquinaria). Interrupciones vivas: rechazo del mundo (a) + dolor de cuerpo real (c) + el elemento
# COMPROMETIDO deja de faltar (short<=0: el cuello mudó, la cascada manda). SILENCIADO: el cambio de INSTANCIA del
# mismo elemento (un pozo más-cercano — el churn de ag4). OFF ≡ bit-exact.
_COMMIT_MINE: bool = os.environ.get("GEMV_COMMIT_MINE", "0") in ("1", "on", "ON", "true")
# GEMV_COMMIT_ALIGN (el aterrizaje de la conquista, [doc de diseño interna, no en el repo] 2026-07-30): la TERCERA cara del
# molde _commit_active (tras depósito y minado). Con bolsillo VACÍO, aligner+heart en mano y la gain
# apuntando a una junction GRIS/RIVAL (el forense heart: el portador orbita a dist 1 sin ENTRAR; conversión
# 0-1% vs 36-100% del suelo), el conquistador COMPROMETE la ruta geodésica a LA CASILLA de la junction (misma
# maquinaria: _gfield a gain[0] + celda-meta sólida a dist 0 → el último paso ES el BUMP = alinear, −1 heart).
# Interrupciones vivas (ESTADO sí, CERCANÍA no): rechazo del mundo (a) + dolor de cuerpo real (c) + la junction
# COMPROMETIDA se volvió NUESTRA (own_net: propia o adelantada por un aliado → meta lograda). SILENCIADO: otra
# gris más cercana (churn de cercanía, el stored-plan da constancia) y la captura por CLIPS a mitad (rival
# sigue siendo target válido; own_net∉tags). Sin precedencia nueva: la banda solo recluta con cargo (la torre
# depósito>minado>align ya ordena). OFF ≡ bit-exact.
_COMMIT_ALIGN: bool = os.environ.get("GEMV_COMMIT_ALIGN", "0") in ("1", "on", "ON", "true")
# GEMV_DESMENTIDO (la memoria de rechazo — el hermano de COMMIT): cuando el JUEGO rechaza un move (agent_world
# =_abs_pos(lp:*), absoluto, NO cambia pese a move elegido = el "no" del mundo medido; la policy no parsea
# action_success del obs), la celda destino se marca OCUPADA-AHORA (token wall efímero) → la geodesia la RODEA
# y el planner deja de re-elegir el muro. Evidencia DINÁMICA: decae rápido (DESMENTIDO_TTL ticks; renovada si
# el rechazo se repite), NUNCA entra a la memoria de fijos (es la clase más efímera de conocimiento). OFF≡bit-exact.
_DESMENTIDO: bool = os.environ.get("GEMV_DESMENTIDO", "0") in ("1", "on", "ON", "true")
DESMENTIDO_TTL: int = 15   # vida útil de la marca (los vecinos se mueven; ~10-20 firmado). Renovada al repetirse.
_SOLID_TYPES: set = set()   # ids de tags type:* sólidos (excl. agent/ship); poblado en _sane_world_ids del config
# GEMV_RUTA_MEM (cura del atasco-contra-sólido): (A) VETO DE SÓLIDO CONOCIDO — ningún move elegido va contra una
# celda que el agente sabe sólida (muro/estación), tras resolver los bump-de-uso; misma fuente que GEODESIC
# (_SOLID_TYPES). (B) GEODÉSICA SOBRE MAPA RECORDADO — objetivo fuera de la ventana ego 13x13 ⇒ _geodesic_field
# ya no devuelve None: proyecta el objetivo a la celda FRONTERA del grid en su dirección y hace BFS hasta ahí (la
# imaginación consulta lo conocido con la misma humildad que la percepción, también al caminar). OFF ≡ bit-exact.
_RUTA_MEM: bool = os.environ.get("GEMV_RUTA_MEM", "0") in ("1", "on", "ON", "true")
# GEMV_GEO_GLOBAL (eslabón geodésico global): la distancia que alimenta la GANANCIA (γ^dist), el atractor de
# desempate y el waypoint deja de ser L1 / geodésica-de-ventana y pasa a BFS sobre TODO el mapa CONOCIDO
# (percepción + memoria territorial + atlas de fijos), sólidos conocidos bloquean, lo nunca visto = caminable
# (optimismo epistémico, firmado). Una sola fuente de verdad de "cuán lejos está algo". BFS en coords
# EGO-RELATIVAS (diferencias, frame-safe). OFF ≡ bit-exact (no se llama; cae a la ruta _GEODESIC/L1).
_GEO_GLOBAL: bool = os.environ.get("GEMV_GEO_GLOBAL", "0") in ("1", "on", "ON", "true")
# GEMV_DESPENSA (eslabón despensa): el estado del almacén común del hub entra en el dominio SOCIAL. Dolor S
# (restado de pos_S) cuando la despensa cae bajo la receta de UN aligner (oxígeno×1/carbono×3/germanio×1/
# silicio×1), saturante y máximo con un material a 0; se apaga al reponer (D2). Reusa el team_held epistémico
# (percibido o recordado) ya resuelto en appraise_shelf. Requiere GEMV_SHELF (la balda vive dentro). Altura D3
# calibrada por W (peer de W_TERR_S), tunable por env sin rebuild. OFF ≡ bit-exact.
_DESPENSA: bool = os.environ.get("GEMV_DESPENSA", "0") in ("1", "on", "ON", "true")
_DESPENSA_W: float = float(os.environ.get("GEMV_DESPENSA_W", "0.30"))  # peso por elemento (D3); calibrado por gates c/d
# GEMV_TEMPERAMENTS — despacho de temperamento POR SLOT: cada agente (proceso aparte) toma w_s / w_f / W_DESPENSA
# de su índice de slot en las listas GEMV_*_BYSLOT (coma-separadas). Se aplica en configure() (donde se conoce el
# slot), rebindeando los globals de ESTE proceso _ACTIVE_CFG y _DESPENSA_W. OFF (o listas vacías) ≡ bit-exact.
_TEMPERAMENTS: bool = os.environ.get("GEMV_TEMPERAMENTS", "0") in ("1", "on", "ON", "true")
def _parse_byslot(name):
    v = os.environ.get(name, "").strip()
    if not v:
        return None
    try:
        return [float(x) for x in v.split(",")]
    except Exception:
        return None
_WS_BYSLOT = _parse_byslot("GEMV_W_S_BYSLOT")
_WF_BYSLOT = _parse_byslot("GEMV_W_F_BYSLOT")
_DESPW_BYSLOT = _parse_byslot("GEMV_DESPENSA_W_BYSLOT")
# GEMV_WALL_MEM (memoria de muros): los sólidos percibidos (_SOLID_TYPES, misma fuente que la geodésica y el veto)
# se recuerdan en coords absolutas (mem._walls, set separado — NO en _entries, para no tocar el cap de 512 con las
# ~3253 celdas-muro del mapa 98x98). Persisten indefinidamente (un muro no se mueve); único borrado: desmentido
# perceptual (dentro del disco y sin sólido → borrar, percepción manda). Los consume el veto RUTA_MEM y GEO_GLOBAL
# (misma fuente: percibidos + recordados), filtrados a la caja del BFS. OFF ≡ bit-exact. Spec: [doc de diseño interna, no en el repo]
_WALL_MEM: bool = os.environ.get("GEMV_WALL_MEM", "0") in ("1", "on", "ON", "true")
_WALL_BOX_MARGIN: int = 20   # margen generoso (revisable) de la caja BFS cuando hay muros que rodear; base sin muros = 8
# GEMV_GEO_WALL_INF (fix del fantasma del muro): en el consumo del campo geodésico de la gain, una celda AUSENTE
# del campo se separa en dos — SÓLIDA conocida (misma fuente que el veto/geodésica) → 1e9 (excluida, no recibe la
# recta L1); NO explorada → L1 (optimismo epistémico intacto). OFF ≡ bit-exact (no se pasan gain_solids).
_GEO_WALL_INF: bool = os.environ.get("GEMV_GEO_WALL_INF", "0") in ("1", "on", "ON", "true")
# GEMV_HUB_PERSIST (pieza 1): el hub propio entra en los fijos que no se olvidan (no se mueve, centro de la economía).
# Misma mecánica que _FIXED_PERSIST_CLS; requiere GEMV_FIXED_PERSIST. OFF ≡ bit-exact (no toca el set de persistentes).
_HUB_PERSIST: bool = os.environ.get("GEMV_HUB_PERSIST", "0") in ("1", "on", "ON", "true")
# GEMV_DEPOSIT_ATTRACTOR (pieza 2): con material a bordo Y dolor de despensa activo, el hub CONOCIDO se vuelve
# objetivo de la ganancia (misma maquinaria que las junctions; usa la ficha de depósito ya existente). Saturante
# (almacén lleno → sin atracción); altura = el alivio del dolor de despensa (eje S, bajo el dolor de cuerpo, D3).
# Requiere _MARCADOR ∧ _DESPENSA (y _HUB_PERSIST para el hub recordado fuera de ventana). OFF ≡ bit-exact.
_DEPOSIT_ATTRACTOR: bool = os.environ.get("GEMV_DEPOSIT_ATTRACTOR", "0") in ("1", "on", "ON", "true")
# GEMV_MINING_GAIN (minado dirigido al cuello): la ganancia de un extractor deja de ser genérica y depende de
# cuánto falta SU material en el hub (escala peor-material). El extractor del material que marca el déficit atrae;
# el de uno que ya sobra, no. Minero VACÍO. Valor = alivio del dolor de despensa al reponer ese material a la
# receta; saturante (hub suficiente → 0); misma maquinaria de gain. Requiere _MARCADOR ∧ _DESPENSA. OFF ≡ bit-exact.
_MINING_GAIN: bool = os.environ.get("GEMV_MINING_GAIN", "0") in ("1", "on", "ON", "true")
# GEMV_RESTOCK_PREEMPT (prioridad firmada): cuando el hub está INFABRICABLE (no paga ni una receta de aligner →
# dolor de despensa > 0), la reposición (depósito/minado dirigido) PREEMPTA a la conquista. En cuanto el hub paga
# una receta (dolor 0), vuelve el orden actual (conquista manda). Fundamento: un almacén infabricable es DOLOR
# (viabilidad bloqueada), no aspiración; por la torre, el dolor manda sobre lo aspiracional. Invariante: _dep/_min
# sólo devuelven valor con dolor>0, así que "hay candidato de reposición" ⟺ "infabricable". El dolor de CUERPO
# sigue en la base-d (no en el gain) → D3 intacto. Requiere _DESPENSA. OFF ≡ bit-exact (orden actual: máx sobre todo).
_RESTOCK_PREEMPT: bool = os.environ.get("GEMV_RESTOCK_PREEMPT", "0") in ("1", "on", "ON", "true")
# GEMV_GAIN_WAYPOINT (meta próxima): la atracción descontada γ^dist no crea gradiente cuando el objetivo está lejos
# (el rollout no llega, el paisaje sale plano). Se toma un punto intermedio del camino GEODÉSICO al objetivo, dentro
# del alcance del rollout, y ESE punto recibe la atracción CON EL VALOR del objetivo final (no lo infla). Se recalcula
# cada tick (percepción del momento). Objetivo dentro del alcance → se usa directo. Inalcanzable → no actúa. Sólo
# cambia DÓNDE se aplica la atracción; valor/torre/competición intactos. Requiere _GEO_GLOBAL. OFF ≡ bit-exact.
_GAIN_WAYPOINT: bool = os.environ.get("GEMV_GAIN_WAYPOINT", "0") in ("1", "on", "ON", "true")
# GEMV_RESTOCK_HEIGHT (firmada 2026-07-27): dos correcciones acopladas para que el deseo de reponer ALCANCE a
# distancia. (1) CONFIANZA del hub propio = 1.0 (no decae; es un fijo permanente, su posición no cambia en toda la
# partida). (2) ALTURA del depósito/minado dirigido cuando el hub es INFABRICABLE: se valora en el ORDEN de una
# oportunidad de conquista (W_RESTOCK_UNBLOCK ≈ W_TERR_R), no 20× por debajo — sin despensa no hay aligner y sin
# aligner no hay conquista. En cuanto el hub paga una receta (dolor 0), el gain de reposición no dispara → escala
# actual. Criterio: DISEÑO (dependencia de la cadena), no "superar la meseta". Requiere _DESPENSA. OFF ≡ bit-exact.
_RESTOCK_HEIGHT: bool = os.environ.get("GEMV_RESTOCK_HEIGHT", "0") in ("1", "on", "ON", "true")
# GEMV_MINING_BATCH (firmada 2026-07-27): el minero llena un LOTE del material-cuello antes de que el atractor de
# depósito preempte (fin de los viajes de 1 unidad). Lote fijo _MINING_BATCH_SIZE (propuesto 5; inventory_max no
# expone capacidad limpia). Mientras cargo<lote y haya extractor-cuello, el minado preempta al depósito; al llenar,
# deposita. No toca saturación (hub suficiente → ambos None) ni el preempt (restock sigue preemptando conquista). OFF≡bit-exact.
_MINING_BATCH: bool = os.environ.get("GEMV_MINING_BATCH", "0") in ("1", "on", "ON", "true")
_MINING_BATCH_SIZE: int = int(os.environ.get("GEMV_MINING_BATCH_SIZE", "5"))
# AJUSTE LOTE↔CAPACIDAD (2026-07-29): _MINING_BATCH_SIZE=5 > capacidad de cargo del juego (4) dejaba el
# ciclo MUERTO — el agente carga 4 y espera un 5º imposible, la cara DEPÓSITO nunca dispara. El lote se
# DERIVA de la capacidad, no se le parece: lote_efectivo = min(propuesto, cap real). FUENTE DE VERDAD del
# cap: mission machina_1 `CargoLimitVariant.limit=4` = mg_config `...cargo:{"base":4}` = replay
# inventory_capacities[cargo]=4. NO es legible limpiamente en runtime (policy_env NO expone capacidad;
# inventory_max=0) → constante documentada, env-overridable para los gates. RE-VERIFICAR si cambia la
# misión/juego (si el cap deja de ser 4, actualizar GEMV_CARGO_CAP_TRUTH o su fuente).
_CARGO_CAP_TRUTH: int = int(os.environ.get("GEMV_CARGO_CAP_TRUTH", "4"))
_MINING_LOTE: int = min(_MINING_BATCH_SIZE, _CARGO_CAP_TRUTH)   # nunca pedir más de lo que cabe
# GEMV_COMMIT_GAIN_INTERRUPT (firmada de palabra ayer): el compromiso se SUELTA si aparece un objetivo de gain
# CLARAMENTE mejor que el comprometido — valor actual > valor comprometido × (1+margen). Margen _COMMIT_GAIN_MARGIN
# (propuesto 0.50 = 50%, para evitar churn). NO devuelve el 2-ciclo: en meseta (d plana, sin objetivo mejor) el
# margen no se supera → COMMIT sigue curando. OFF≡bit-exact.
_COMMIT_GAIN_INTERRUPT: bool = os.environ.get("GEMV_COMMIT_GAIN_INTERRUPT", "0") in ("1", "on", "ON", "true")
_COMMIT_GAIN_MARGIN: float = float(os.environ.get("GEMV_COMMIT_GAIN_MARGIN", "0.50"))
# GEMV_HUB_SINGLE_SOURCE (firmada 2026-07-27): UNA sola fuente de verdad para la escasez común. Con la cadena de
# despensa activa (GEMV_DESPENSA=1), la escasez del hub NO entra ADEMÁS por el eje R (se retira la proyección del
# SHELF, shelf_deficit_R); vive sólo en S (despensa) con sus remedios direccionales (minar/volver/lote). El hambre
# PERSONAL de R (energía base + hearts + territorial) queda intacta. Con despensa OFF, nada cambia (pila ganadora
# intacta). OFF ≡ bit-exact.
_HUB_SINGLE_SOURCE: bool = os.environ.get("GEMV_HUB_SINGLE_SOURCE", "0") in ("1", "on", "ON", "true")
try:
    from appraisal.appraisal_shelf import W_TERR_R as _W_TERR_R_REF
    _W_RESTOCK_UNBLOCK: float = _W_TERR_R_REF          # 2.40 — orden de una oportunidad de conquista (no cableado)
except Exception:
    _W_RESTOCK_UNBLOCK = 2.40

# GEMV_ECON_CONST (Constitución económica, spec APROBADA [doc de diseño interna, no en el repo] v2,
# 2026-07-27): MOTOR ÚNICO DE ABASTECIMIENTO. shelf_R deja de ser dolor en pie y se convierte en una
# ganancia dirigida de DOS CARAS (cargo<lote → extractor del material-cuello; cargo≥lote → hub), altura
# base W_TERR_R modulada por un TECHO CONTINUO del cuerpo (altura·exp(−dolor_cuerpo/P_REF)), activa sólo
# con hub INFABRICABLE (∃x: team_x<recipe_x), y preempt categórico sobre la conquista cuando infabricable.
# Con ECON_CONST ON: DESPENSA se fuerza OFF y shelf_deficit_R en pie → 0 (la escasez vive SÓLO en el motor;
# fin de la doble contabilidad); MINING_GAIN/DEPOSIT_ATTRACTOR/RESTOCK_PREEMPT/RESTOCK_HEIGHT quedan
# ABSORBIDOS (no se llaman aunque estén ON); HUB_SINGLE_SOURCE queda RETIRADO (inerte); MINING_BATCH vive
# dentro del motor (umbral de lote). OFF ≡ bit-exact (gate sagrado).
_ECON_CONST: bool = os.environ.get("GEMV_ECON_CONST", "0") in ("1", "on", "ON", "true")
_ECON_ALTURA_BASE: float = _W_RESTOCK_UNBLOCK          # 2.40 = W_TERR_R (importado, no cableado)
# ENMIENDA DEL PREEMPT (2026-07-29, opción 1+3 firmadas): de interruptor a CUESTA.
# GEMV_ECON_CONQUEST_MARGIN (k): con el motor de suministro ACTIVO (hub infabricable según conocimiento
#   FRESCO), la conquista/equipar COMPITE si su Δd supera al del motor por factor k (>1). El suministro manda
#   por defecto (la cadena rota es la cadena rota); la cuesta solo deja pasar lo CLARAMENTE mejor. k=0 → OFF
#   (preempt binario histórico, bit-exact). Con hub fabricable, el motor ya devuelve None → nada cambia.
_ECON_CONQUEST_MARGIN: float = float(os.environ.get("GEMV_ECON_CONQUEST_MARGIN", "0") or "0")
# GEMV_ECON_STALE_FRESH: el valor del motor de suministro se descuenta por la FRESCURA de la creencia
#   hub-infabricable (epistemología de la casa: decay del pantry). Un agente lejano que RECUERDA (rancio) el
#   hub roto no debe suprimir la conquista con conocimiento viejo: hub_fresh=exp(−λ·pantry_age) pondera el
#   valor de la cara MINADO. Percibir el hub ⇒ hub_fresh=1 (percepción manda, ya refrescada en _pantry_ctx).
#   OFF → hub_fresh=1.0 → bit-exact. La cara DEPÓSITO ya trae la conf del hub recordado (no se re-descuenta).
_ECON_STALE_FRESH: bool = os.environ.get("GEMV_ECON_STALE_FRESH", "0") in ("1", "on", "ON", "true")
# GEMV_HEART_GAIN (el deseo de anchura, [doc de diseño interna, no en el repo] opción d, 2026-07-29): el heart como GANANCIA
#   saturante (f+), no dolor. Extiende `_gain_opportunity` (la cadena equipar→alinear) con el eslabón
#   craftear/minar-para-heart: SIN heart la oportunidad de puntuar YA existe y tira hacia conseguir un heart
#   (hub si puede craftear ≥7 de cada; si no, extractor del elemento MÁS deficitario para [7,7,7,7] — portfolio,
#   no cuello único). Satura por agente (con heart, el eslabón desaparece). El dolor queda en el suministro
#   VITAL [1,3,1,1] (la guarda constitucional: con hub infabricable-para-lo-vital, el motor preempta y el deseo
#   de anchura NO gobierna). Arbitraje stock-para-uno: equip primero. OFF ≡ bit-exact (sin heart → None, como hoy).
_HEART_GAIN: bool = os.environ.get("GEMV_HEART_GAIN", "0") in ("1", "on", "ON", "true")
# HP1 EL EQUIP FIABLE ([doc de diseño interna, no en el repo], 2026-07-29): dos piezas de una cura + pantry-stale de prerreq.
# GEMV_SUPPLY_SLACK (B): el motor vital abastece hasta la HOLGURA OBJETIVO (SLACK = vital + 1 equip), no solo
#   hasta fabricable. Activo ⟺ ∃ held<SLACK; objetivo = extractor del elemento MÁS deficitario p/SLACK
#   (portfolio → mina los CUATRO, cura el mono-carbono desde el suministro). LETRA G1→G1' (ver banco). OFF ≡ bin.
# GEMV_EQUIP_CUSHION (A): guarda de colchón CONTINUA. _op(conquista/equip) ·= cushion, con
#   cushion = min_i clamp((held_i − vital_i)/equip_i, 0, 1). 0 en el vital → 1 en vital+equip. FUNDE EQUIP_GATED
#   (retira el binario: el equip imaginado ya no es sí/no sino la cuesta continua). OFF ≡ bit-exact.
_SUPPLY_SLACK: bool = os.environ.get("GEMV_SUPPLY_SLACK", "0") in ("1", "on", "ON", "true")
_EQUIP_CUSHION: bool = os.environ.get("GEMV_EQUIP_CUSHION", "0") in ("1", "on", "ON", "true")
# GEMV_CARGO_PRECEDENCE (la banda de respiración — la letra firmada): el cargado (cargo>=lote) va al hub
# INCONDICIONALMENTE hasta depositar. (i) GAIN: la cara DEPÓSITO del _supply_motor devuelve hub_rel al margen
# de la saturación (un cargado nunca se queda sin ruta al hub aunque el hub llegue a SLACK; el depósito procede
# con hub>=SLACK — bolsillo liberado). (ii) COMMIT: _commit_active = cargo>=lote (sin exigir infabricable, cura
# la Vía-1 de B: el hub fabricable-vital ya no desengancha el retorno comprometido). (iii) LA PRECEDENCIA NO ES
# SORDA (afinación 1): el compromiso del cargado SÓLO lo interrumpen el rechazo del mundo (a, alimenta DESMENTIDO)
# y el DOLOR DE CUERPO real (c-cuerpo: pR/hp; la torre manda cuerpo>todo); se SILENCIAN el flip de oportunidad
# (b, colchón/portfolio) y la contabilidad (demanda, mejor-gain d). OFF ≡ bit-exact. Ver [doc de diseño interna, no en el repo].
_CARGO_PRECEDENCE: bool = os.environ.get("GEMV_CARGO_PRECEDENCE", "0") in ("1", "on", "ON", "true")
# GEMV_SURVIVAL (la cara ACTIVA del cuerpo — volver a casa a regenerar; [doc de diseño interna, no en el repo], firmado):
# fuera de territorio propio la hp sangra 1/tick; en casa regenera. reserva = hp − d_home(geodésica a
# territorio propio ≈ geo_al_hub − R); U = clamp((RESERVE_SAFE − reserva)/RESERVE_SAFE, 0, 1); FUERZA = W_SURV·U
# hacia el hub (=centro del territorio propio). Compite por MAGNITUD (gana cuando reserva<~19: W_SURV·U > altura
# suministro ~2.4). El sano NO la siente (U=0 con hp llena en todo el mapa). Coste acotado: en territorio propio
# (territory:here=1) d_home=0 sin BFS; fuera, un BFS al hub. OFF ≡ bit-exact. Constantes derivadas del censo.
_SURVIVAL: bool = os.environ.get("GEMV_SURVIVAL", "0") in ("1", "on", "ON", "true")
_SURV_R: float = float(os.environ.get("GEMV_SURV_R", "19"))            # radio del disco de territorio propio (medido)
_SURV_RESERVE_SAFE: float = float(os.environ.get("GEMV_SURV_RESERVE", "25"))  # reserva por encima de la cual el sano no la siente
_SURV_W: float = float(os.environ.get("GEMV_SURV_W", "10"))            # peso (U=0.24→2.4=altura suministro; U≥0.3 domina)
# GEMV_SURVIVAL_HOME (survival-completo, la 1ª cura de vidas largas — [doc de diseño interna, no en el repo], firmado):
# los 10 muertos del peldaño 1000 no fallan por sensor (U siempre disparó) sino por RETORNO LENTO: el gain
# =(hub_rel,surv_val) sin commit → el planner oscila (cierra d_home ~0.65/t) y muere a 6-12 casillas de casa.
# PRONG A = COMMIT-HOME (la 4ª puerta): rutar el retorno sobre el campo GEO_GLOBAL al hub (`_hf`, ya computado
# para d_home) con `_commit_route_geodesic` → cierra a ~1/t recto a casa; precedencia MÁXIMA (primera cara del
# commit, sólo suelta al llegar on_terr==1; _rej reruta vía DESMENTIDO). PRONG B = umbral consciente del
# territorio: RESERVE_SAFE·bleed_local (neutral/propio 1× → 25; ENEMIGO 2× → 50, sangría medida 1.96 vs 1.00/t).
# La esquina del cargado-sangrante: convergencia TRIVIAL (survival ya puso gain[0]=hub_rel = destino del
# depósito; COMMIT-HOME va primero → sin churn entre commits del mismo destino; al llegar, el depósito reanuda).
# OFF ≡ bit-exact (sano U=0 idéntico; flag a 0 no toca nada).
_SURVIVAL_HOME: bool = os.environ.get("GEMV_SURVIVAL_HOME", "0") in ("1", "on", "ON", "true")
def _slack_target():
    """HOLGURA OBJETIVO DERIVADA (afinación 2, firmada): SLACK[i] = VITAL[i] + EQUIP[i] elemento a elemento,
    RECETAS IMPORTADAS del juego (VITAL=ALIGNER_RECIPE fabricabilidad; EQUIP=aligner_cost). Si el juego cambia
    recetas, la derivación sobrevive. Devuelve lista alineada a _TEAM_FIDS [oxy,carb,germ,sil]."""
    from appraisal.appraisal_shelf import ALIGNER_RECIPE as _VIT, _TEAM_FIDS as _TF
    _eq = _aligner_cost()                              # {team_fid: coste} del aligner
    return [_VIT[i] + _eq.get(_TF[i], 0) for i in range(len(_TF))]
def _hub_cushion(scalar_map, tag_map, team_side):
    """(A) GUARDA DE COLCHÓN: cushion = min_i clamp((held_i − vital_i)/equip_i, 0, 1). 1 = el hub afford un
    equip SOBRE lo vital; 0 = está en el vital (equipar lo rompería). Hub PERCIBIDO (GLOBAL_LOC) o pantry
    (fresco vía la cura STALE, prerreq). Sin conocimiento del hub → 0 (conservador: no equipar a ciegas)."""
    from appraisal.appraisal_shelf import _TEAM_FIDS as _TF, ALIGNER_RECIPE as _VIT
    _eq = _aligner_cost()
    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    if any(TAG_TYPE_HUB in t and own_team_tag in t for t in tag_map.values()):
        held = [get_scalar(scalar_map, GLOBAL_LOC, f) for f in _TF]
    else:
        pm = _pantry_ctx.get('vals') if _PANTRY_MEM else None
        if not pm:
            return 0.0
        held = [pm.get(f, 0.0) for f in _TF]
    vals = []
    for i in range(len(_TF)):
        e = _eq.get(_TF[i], 0) or 1
        vals.append(max(0.0, min(1.0, (held[i] - _VIT[i]) / float(e))))
    return min(vals) if vals else 0.0

_ECON_P_REF_CACHE: dict = {}
def _econ_p_ref(cfg):
    """P_REF del techo = dolor de cuerpo cuando la energía llega a su EQUILIBRIO (spec §1.4):
    d(pos_F=1, pos_R=0, pos_S=0.8) − d(1, 2, 0.8), con la config del agente. Cacheado por id(cfg)."""
    k = id(cfg)
    if k not in _ECON_P_REF_CACHE:
        from motor.model import State as _St
        base = opponent_distance(_St(pF=1.0, nF=0.0, pR=2.0, nR=0.0, pS=0.8, nS=0.0), cfg)  # sano (energy>=20)
        eq   = opponent_distance(_St(pF=1.0, nF=0.0, pR=0.0, nR=0.0, pS=0.8, nS=0.0), cfg)  # energy=EQ (pos_R=0)
        _ECON_P_REF_CACHE[k] = eq - base
    return _ECON_P_REF_CACHE[k]

def _econ_body_pain(scalar_map, cfg):
    """Dolor de cuerpo (F por hp + R personal por energía base v4, ANTES de shelf/hearts/territorial):
    Δd de (pos_F_body, pos_R_energy, 0.8) al sano (1,2,0.8). pos_S en target ⇒ sólo F y R cuentan."""
    from motor.model import State as _St, HP_EQ, HP_SCALE, ENERGY_EQ, ENERGY_SCALE
    hp = get_multipart(scalar_map, AGENT_LOC, 20)
    energy = get_multipart(scalar_map, AGENT_LOC, FID_INV_ENERGY)
    posF = min(cfg.f_pos_target, (hp - HP_EQ) / HP_SCALE)
    posR = min(cfg.r_pos_target, (energy - ENERGY_EQ) / ENERGY_SCALE)
    s_body = _St(pF=max(0.0, posF), nF=max(0.0, -posF), pR=max(0.0, posR), nR=max(0.0, -posR), pS=0.8, nS=0.0)
    s_sano = _St(pF=1.0, nF=0.0, pR=2.0, nR=0.0, pS=0.8, nS=0.0)
    return max(0.0, opponent_distance(s_body, cfg) - opponent_distance(s_sano, cfg))

def _econ_altura_efectiva(body_pain, cfg):
    """Altura del motor con el techo continuo: ALTURA_BASE · exp(−dolor_cuerpo / P_REF). Continua,
    monótona decreciente, =ALTURA_BASE sin dolor. Garantiza cuerpo>abastecimiento por números (spec §1.4)."""
    return _ECON_ALTURA_BASE * _math.exp(-body_pain / _econ_p_ref(cfg))

def _econ_log_tick(scalar_map, tag_map, team_side, mem, world_step, sm):
    """INSTRUMENTACIÓN P2/P3 (GEMV_ECON_DBG) — OBSERVA, NO INTERVIENE: no toca `gain` ni ninguna decisión.
    Registra por tick: estado fabricable/infabricable del hub, aporte del motor al campo, factor del techo."""
    from appraisal.appraisal_shelf import _TEAM_FIDS as _TF, ALIGNER_RECIPE as _REC
    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    hub_perc = any(TAG_TYPE_HUB in t and own_team_tag in t for t in tag_map.values())
    if hub_perc:
        team_held = [get_scalar(scalar_map, GLOBAL_LOC, f) for f in _TF]; src = "perc"
    else:
        pm = _pantry_ctx.get('vals') if _PANTRY_MEM else None
        team_held = [pm.get(f, 0.0) for f in _TF] if pm else None
        src = "mem" if pm else "none"
    if team_held is None:
        fab = "unknown"
    else:
        fab = "fabricable" if all(team_held[i] >= _REC[i] for i in range(len(_REC))) else "infabricable"
    bp = _econ_body_pain(scalar_map, _ACTIVE_CFG)
    factor = _math.exp(-bp / _econ_p_ref(_ACTIVE_CFG))
    aporte = sm[1] if sm is not None else 0.0
    _log(f"GEMV_ECON step={world_step} hub={fab} src={src} team={team_held} motor_aporte={aporte:.4f} "
         f"techo_factor={factor:.4f} body_pain={bp:.4f}")

def _geodesic_field(tag_map: dict, grel, extra_solid=None):
    """BFS desde la gear/junction objetivo (grel, rel al agente) sobre el grid ego, bloqueando sólidos CONOCIDOS
    (tags ∩ _SOLID_TYPES; la propia celda de grel es la meta, se permite). Celdas no vistas = caminables.
    extra_solid (DESMENTIDO): set de celdas ego (dr,dc) marcadas OCUPADA-AHORA por rechazo del juego → el BFS
    las RODEA (evidencia dinámica, efímera). Devuelve {(dr,dc) rel-al-agente: pasos geodésicos hasta grel}.
    Fuera del grid / inalcanzable → ausente (el planner cae a L1). ~208 celdas: barato."""
    from collections import deque as _dq
    R, C = EGOCENTRIC_ROWS, EGOCENTRIC_COLS
    _xs = extra_solid or ()
    def solid(rr, cc):
        if (rr - AGENT_ROW, cc - AGENT_COL) in _xs:         # rechazo reciente = ocupada ahora
            return True
        return bool(tag_map.get(rr * C + cc, ()) and (set(tag_map.get(rr * C + cc, ())) & _SOLID_TYPES))
    gr, gc = AGENT_ROW + grel[0], AGENT_COL + grel[1]      # celda ego del objetivo
    if not (0 <= gr < R and 0 <= gc < C):
        if not _RUTA_MEM:
            return None                                     # objetivo fuera del grid → sin geodesia, L1
        # RUTA_MEM (B): proyecta el objetivo a la FRONTERA del grid en su dirección y haz BFS hasta ella.
        gr = min(max(gr, 0), R - 1)
        gc = min(max(gc, 0), C - 1)
        if solid(gr, gc):                                   # frontera proyectada sólida → frontera LIBRE más cercana
            _best = None
            for _rr in range(R):
                for _cc in range(C):
                    if (_rr in (0, R - 1) or _cc in (0, C - 1)) and not solid(_rr, _cc):
                        _dd = abs(_rr - gr) + abs(_cc - gc)
                        if _best is None or _dd < _best[0]:
                            _best = (_dd, _rr, _cc)
            if _best is None:
                return None                                 # ninguna frontera libre → L1 (degradación segura)
            gr, gc = _best[1], _best[2]
    field = {}
    q = _dq([(gr, gc, 0)]); seen = {(gr, gc)}
    while q:
        rr, cc, dd = q.popleft()
        field[(rr - AGENT_ROW, cc - AGENT_COL)] = dd        # dist geodésica de esta celda a grel
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = rr + dr, cc + dc
            if (nr, nc) in seen or not (0 <= nr < R and 0 <= nc < C):
                continue
            if solid(nr, nc) and (nr, nc) != (gr, gc):       # sólido conocido bloquea (salvo el propio objetivo)
                continue
            seen.add((nr, nc)); q.append((nr, nc, dd + 1))
    return field


def _geodesic_field_global(tag_map: dict, grel, mem, extra_solid=None, return_solids=False):
    """GEO_GLOBAL — geodésica sobre el MAPA CONOCIDO (no confinada a la ventana ego). BFS en coords
    EGO-RELATIVAS (diferencias → frame-safe: nunca mezcla el marco-memoria con coords de juego) desde el
    objetivo grel, bloqueando SÓLIDOS CONOCIDOS: percepción (tag_map ∩ _SOLID_TYPES) + memoria territorial
    (mem._entries: estructuras fijas) + atlas de fijos (anclado al hub). Lo nunca visto = caminable
    (optimismo epistémico). Devuelve {(dr,dc) ego-rel: pasos geodésicos hasta grel}. La caja se acota a la
    envolvente agente-objetivo + margen (barato). El consumidor cae a L1 para celdas ausentes."""
    from collections import deque as _dq
    C = EGOCENTRIC_COLS
    solids = set()
    # (1) percepción actual (muros/estaciones en la ventana)
    for loc, tags in tag_map.items():
        if set(tags) & _SOLID_TYPES:
            solids.add((loc // C - AGENT_ROW, loc % C - AGENT_COL))
    # (2) memoria territorial (estructuras fijas recordadas) en ego-rel via el marco-memoria (wr-ar, wc-ac)
    _SOLID_MEM = ("gear_aligner", "junction_gray", "junction_rival", "junction_own", "hub", "solar")
    hub_ego = None
    if mem is not None and hasattr(mem, "_entries"):
        ar, ac = getattr(mem, "_agent_world", (0, 0))
        for (wr, wc, cls) in mem._entries:
            if cls and (cls in _SOLID_MEM or cls.startswith("extractor")):
                solids.add((wr - ar, wc - ac))
            if cls == "hub":
                hub_ego = (wr - ar, wc - ac)
    if hub_ego is None:                                  # hub desde percepción para anclar el atlas
        for loc, tags in tag_map.items():
            if TAG_TYPE_HUB in tags:
                hub_ego = (loc // C - AGENT_ROW, loc % C - AGENT_COL); break
    # (3) atlas de fijos (hub-anclado): ego-rel = hub_ego + pos (diferencias). Sin hub_ego → se omite.
    _atlas = _cortex_ctx.get('atlas')
    if _atlas and hub_ego is not None:
        for e in _atlas:
            p = e.get('pos')
            if p and e.get('cls') != 'hub':
                solids.add((hub_ego[0] + p[0], hub_ego[1] + p[1]))
    solids |= set(extra_solid or ())
    gt = (grel[0], grel[1])
    # caja acotada: envolvente {agente(0,0), objetivo} + margen; CAP de seguridad ~ tamaño de mapa.
    # WALL_MEM: margen GENEROSO (_WALL_BOX_MARGIN, revisable) para dar sitio a rodeos largos alrededor de muros
    # recordados; sin muros el margen base es 8 (⇒ OFF ≡ bit-exact, no cambia la caja).
    _wall_on = mem is not None and getattr(mem, "wall_mem", False) and getattr(mem, "_walls", None)
    M = _WALL_BOX_MARGIN if _wall_on else 8
    CAP = 100
    r0 = max(min(0, gt[0]) - M, -CAP); r1 = min(max(0, gt[0]) + M, CAP)
    c0 = max(min(0, gt[1]) - M, -CAP); c1 = min(max(0, gt[1]) + M, CAP)
    # (3b) muros RECORDADOS (WALL_MEM) — misma fuente que percepción/veto — filtrados a la caja del BFS.
    if _wall_on:
        _ar, _ac = getattr(mem, "_agent_world", (0, 0))
        for (wr, wc) in mem._walls:
            dr = wr - _ar; dc = wc - _ac
            if r0 <= dr <= r1 and c0 <= dc <= c1:
                solids.add((dr, dc))
    solids.discard(gt)                                   # el objetivo es la meta, no bloquea (tras añadir muros)
    field = {}
    q = _dq([(gt[0], gt[1], 0)]); seen = {gt}
    while q:
        rr, cc, dd = q.popleft()
        field[(rr, cc)] = dd
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = rr + dr, cc + dc
            if (nr, nc) in seen or not (r0 <= nr <= r1 and c0 <= nc <= c1):
                continue
            if (nr, nc) in solids and (nr, nc) != gt:
                continue
            seen.add((nr, nc)); q.append((nr, nc, dd + 1))
    return (field, solids) if return_solids else field


def _gain_waypoint(target_rel, tag_map, mem, reach):
    """META PRÓXIMA (GEMV_GAIN_WAYPOINT): punto intermedio del camino GEODÉSICO hacia target_rel, a ~reach pasos del
    agente, cuando el objetivo está MÁS LEJOS que reach (fuera del alcance del rollout). Traza desde el agente (0,0)
    hacia distancias geodésicas decrecientes. Devuelve el waypoint ego-rel, o None si el objetivo ya está DENTRO del
    alcance (usar directo) o es INALCANZABLE (no actuar). Se recalcula cada tick (percepción del momento)."""
    field = _geodesic_field_global(tag_map, target_rel, mem)
    d0 = field.get((0, 0))
    if d0 is None or d0 <= reach:
        return None                                # inalcanzable (gate e) o ya dentro del alcance (gate b)
    cur = (0, 0); cur_d = d0
    for _ in range(reach):
        nxt = None
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            cell = (cur[0] + dr, cur[1] + dc); cd = field.get(cell)
            if cd is not None and (nxt is None or cd < nxt[1]):
                nxt = (cell, cd)
        if nxt is None or nxt[1] >= cur_d:         # el camino no progresa (meseta local del campo) → parar
            break
        cur, cur_d = nxt
    return cur if cur != (0, 0) else None
# GEMV_TIE_UNIFIED (vía a): un empate EXACTO en terminal_d lo rompe SIEMPRE la jerarquía (N2/N3-miga/N4/
# orden), nunca la d-de-1-paso, sea cual sea la rama (spread≤eps o >eps). Cierra el agujero de aplicación
# del criterio ya firmado (antes select() rompía el empate del mínimo por la 1-step d → oscilaba). OFF≡bit-exact.
_TIE_UNIFIED: bool = os.environ.get("GEMV_TIE_UNIFIED", "0") in ("1", "on", "ON", "true")
# GEMV_PASO_C4 ([doc de diseño interna, no en el repo], red final, 2026-07-29): en empate EXACTO residual del desempate, romper
# por SLOT (rompe la simetría de clones que produce el 2-ciclo/colisión al converger). Último eslabón;
# solo actúa cuando quedan >1 acciones genuinamente empatadas (misma terminal_d → no toca la
# constitución). Instrumentado (contador _C4_DECISIONS en el planificador). OFF≡bit-exact.
_PASO_C4: bool = os.environ.get("GEMV_PASO_C4", "0") in ("1", "on", "ON", "true")
FID_LP_EAST: int = 7; FID_LP_WEST: int = 8; FID_LP_NORTH: int = 9; FID_LP_SOUTH: int = 10  # defaults; se resuelven


def _abs_pos(scalar_map):
    """Posición GLOBAL absoluta (fila, col) del agente desde lp:* (features globales en GLOBAL_LOC).
    (fila,col) = (lp:south − lp:north, lp:east − lp:west). Convención canónica. None si no hay lp:*."""
    e = get_scalar(scalar_map, GLOBAL_LOC, FID_LP_EAST); w = get_scalar(scalar_map, GLOBAL_LOC, FID_LP_WEST)
    n = get_scalar(scalar_map, GLOBAL_LOC, FID_LP_NORTH); s = get_scalar(scalar_map, GLOBAL_LOC, FID_LP_SOUTH)
    if e == 0 and w == 0 and n == 0 and s == 0:
        return None
    return (int(s - n), int(e - w))
W_HEARTS_RICH: float = 0.30        # (declarado, tabla firmada) riqueza de hearts sobre el básico
HEART_BASIC: int = 2               # 0-2 = básico. NOTA: la riqueza NO se cablea aparte — el techo R del motor
#   (pos_R saturado a 2.0) ya hace que hearts sobre saciedad no reduzcan d ("riqueza no cura", literal §spec).
#   La pieza central de C4 es la FUERZA-d de oportunidad territorial (I2); la balda de hearts f− queda intacta.
_rutas_ctx: dict = {'rutas': None}
if _WAYPOINTS:
    try:
        import json as _rjson
        for _p in ("cortex/rutas.json", "/app/cortex/rutas.json"):
            if os.path.exists(_p):
                _rutas_ctx['rutas'] = _rjson.load(open(_p)).get('rutas', [])
                break
    except Exception:
        _rutas_ctx['rutas'] = None
# Contexto mutable de pantry memory — actualizado en choose_action antes de predict/plan.
# Mutable dict para que el closure appraise lo lea en tiempo de llamada (no de definición).
_pantry_ctx: dict = {'vals': None, 'step': -1}
# Eslabón 4 — contexto territorial (junctions recordadas [(loc,'ours'|'gain')] + recuerdo hub-sin-fruto).
_terr_ctx: dict = {'remembered': None, 'hub_fail_step': -1}
if _GEMV_SHELF:
    from appraisal.appraisal_shelf import (
        appraise_shelf as _appraise_shelf_fn,
        _hub_in_window as _shelf_hub_vis,
        _TEAM_FIDS as _SHELF_TEAM_FIDS,
    )
    def appraise(tokens, team_side, s_scale=1.0, act_credit=0.0, **kw):
        pm = _pantry_ctx['vals'] if _PANTRY_MEM else None
        # D3 — edad del recuerdo (0 si percepción directa / decay off). El factor exp(-λ·age)
        # atenúa el déficit derivado del recuerdo; con hub visible age=0 ⇒ factor 1 ⇒ bit-exact.
        page = _pantry_ctx.get('age', 0.0) if (_PANTRY_MEM and _PANTRY_DECAY) else 0.0
        tr = _terr_ctx['remembered'] if _MARCADOR else None
        return _appraise_shelf_fn(tokens, team_side, shelf_on=True, pantry_memory=pm,
                                   s_scale=s_scale, act_credit=act_credit,
                                   pantry_age=page, pantry_decay_lambda=_PANTRY_DECAY_LAMBDA,
                                   hearts_on=_HEARTS, marcador_on=_MARCADOR, terr_remembered=tr,
                                   despensa_on=(_DESPENSA and not _ECON_CONST), w_despensa=_DESPENSA_W,
                                   hub_single_source=(_HUB_SINGLE_SOURCE and not _ECON_CONST),
                                   econ_const=_ECON_CONST)

# ── Constants ────────────────────────────────────────────────────────────────

EGOCENTRIC_ROWS: int = 13
MOVE_ENERGY_COST: int = 4
AGENT_LOC_PACK: int = AGENT_ROW * EGOCENTRIC_COLS + AGENT_COL  # 102, same as AGENT_LOC

# territory:direction feature IDs (from player_config)
FID_TERR_NORTH: int = 70
FID_TERR_SOUTH: int = 71
FID_TERR_EAST: int  = 72
FID_TERR_WEST: int  = 73

# inv:energy part-1 feature ID
FID_INV_ENERGY_P1: int = FID_INV_ENERGY + 1  # 25

# Action deltas: (drow, dcol) in world coordinates
# move_north = row decreases → drow = -1
ACTION_DELTAS: dict[str, tuple[int, int]] = {
    "move_north": (-1,  0),
    "move_south": (+1,  0),
    "move_west":  ( 0, -1),
    "move_east":  ( 0, +1),
}

def _commit_route_geodesic(afield: dict, k: int) -> list:
    """CURA DEL RETORNO capa 2 ([doc de diseño interna, no en el repo], 2026-07-29): ruta comprometida que SIGUE el campo
    geodésico `afield` (rel (dr,dc)->distancia al objetivo del motor = hub en la cara depósito) hacia el
    objetivo, k pasos. Cada paso toma el move que MÁS reduce la distancia geodésica. La celda-meta (hub)
    tiene distancia 0 y se permite → el último paso ES el BUMP al hub (= depósito). Da RUMBO VERDADERO al
    compromiso, no el argmin degenerado de la meseta. Devuelve [] si no hay campo o no hay reductor."""
    if not afield:
        return []
    plan = []
    cur = (0, 0)
    for _ in range(k):
        base = afield.get(cur)
        if base is None:
            break
        best_a = None; best_d = base
        for a, (dr, dc) in ACTION_DELTAS.items():
            d = afield.get((cur[0] + dr, cur[1] + dc))
            if d is not None and d < best_d:
                best_d = d; best_a = a
        if best_a is None:                                  # sin reductor (meseta/dead-end): parar (no inventar)
            break
        plan.append(best_a)
        _dr, _dc = ACTION_DELTAS[best_a]
        cur = (cur[0] + _dr, cur[1] + _dc)
        if best_d <= 0:                                     # alcanzado el objetivo (el bump ya está en el plan)
            break
    return plan

# Direction fid for territory update per action
ACTION_TERR_FID: dict[str, int] = {
    "move_north": FID_TERR_NORTH,
    "move_south": FID_TERR_SOUTH,
    "move_east":  FID_TERR_EAST,
    "move_west":  FID_TERR_WEST,
}

# ── TEST INJECTION (déficit sintético — mecanismo de test, NO parte del appraisal) ──
# Variables de entorno:
#   GEMV_INJECT_HP:           HP inyectado (ej. 25); decay lineal en GEMV_INJECT_STEPS pasos
#                             desde GEMV_INJECT_HP_DELAY en adelante.
#   GEMV_INJECT_ENERGY:       energía inyectada (ej. 5); decay lineal en GEMV_INJECT_ENERGY_STEPS pasos.
#   GEMV_INJECT_STEPS:        pasos de decay para HP (default 2000).
#   GEMV_INJECT_ENERGY_STEPS: pasos de decay para energía (default = GEMV_INJECT_STEPS).
#   GEMV_INJECT_HP_DELAY:     pasos antes de iniciar inyección HP (default 0).
#                             Permite fase 1 = energía (movimiento) y fase 2 = HP.
#   GEMV_S_SCALE:             multiplicador del eje S para barrido (default 1.0).
_INJECT_HP:           int   = int(os.environ.get("GEMV_INJECT_HP",           "-1"))
_INJECT_ENERGY:       int   = int(os.environ.get("GEMV_INJECT_ENERGY",       "-1"))
_INJECT_STEPS:        int   = int(os.environ.get("GEMV_INJECT_STEPS",        "2000"))
_INJECT_ENERGY_STEPS: int   = int(os.environ.get("GEMV_INJECT_ENERGY_STEPS", str(int(os.environ.get("GEMV_INJECT_STEPS", "2000")))))
_INJECT_HP_DELAY:     int   = int(os.environ.get("GEMV_INJECT_HP_DELAY",     "0"))
# Fase 3c — UTILLAJE DE SALIDA (test harness, NO conducta del agente): fuerza N pasos en una
# dirección para sacar al agente de su territorio antes de ceder el control al motor. OFF por defecto.
_BOOTSTRAP_STEPS:     int   = int(os.environ.get("GEMV_BOOTSTRAP_STEPS",     "0"))
_BOOTSTRAP_DIR:       str   = os.environ.get("GEMV_BOOTSTRAP_DIR",     "move_north")
# Fase 4 — bootstrap MULTI-TRAMO (secuencia fija declarada, NO pathfinding): "dir:count,dir:count,...".
# Sigue siendo ciego y pre-escrito (dirección fija por tramos). Si está, tiene prioridad. Ej:
#   GEMV_BOOTSTRAP_SEQ="move_east:2,move_south:16,move_east:10"
def _parse_boot_seq(s: str) -> list:
    seq = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        d, _, n = part.partition(":")
        seq.extend([d] * int(n or "1"))
    return seq
_BOOTSTRAP_SEQ:       list  = _parse_boot_seq(os.environ.get("GEMV_BOOTSTRAP_SEQ", ""))
S_SCALE:              float = float(os.environ.get("GEMV_S_SCALE",           "1.0"))
_MEM_VERSION:         int   = int(os.environ.get("GEMV_USE_MEMORY", "0"))
USE_MEMORY:           bool  = _MEM_VERSION >= 1

# Fase 3a — planificador corto (horizonte rodante). H=1 => greedy exacto (default).
_HORIZON:    int  = int(os.environ.get("GEMV_HORIZON", "1"))
_PLAN_CACHE: bool = os.environ.get("GEMV_PLAN_NOPRUNE", "0") != "1"
# Gate: rutear H=1 por el planificador (para verificar plan(H=1) ≡ greedy bit-a-bit).
_PLAN_FORCE: bool = os.environ.get("GEMV_PLAN_FORCE", "0") == "1"
# Fase 3b — modelo de transición (mecánica pública del juego) en el simulador. OFF por defecto.
_TRANSITION_ON: bool = os.environ.get("GEMV_TRANSITION", "0") == "1"
# Extensión: bump→cosecha (completa la cobertura de 3b). Interruptor PROPIO; OFF ≡ conducta actual
# bit-exact. Enciende el modelado del bump al extractor (held+δ) en el simulador del planificador.
_TRANS_EXTRACT: bool = os.environ.get("GEMV_TRANSITION_EXTRACT", "0") == "1"
# 1d-bis: extractor RECORDADO como cosechable VIRTUAL en el mundo simulado del planner (fuera de ventana).
# Simetría por canal: el extractor opera en el PLANNER (previsión), no en el appraisal. OFF ≡ bit-exact.
_VIRTUAL_EXTRACT: bool = os.environ.get("GEMV_VIRTUAL_EXTRACT", "0") == "1"
_MB1_EVERY: int = int(os.environ.get("GEMV_MB1_ABLATE_EVERY", "0"))  # tanda2: ablación virtual cada N ticks (0=off)
# 1e: la demanda derivada como CIUDADANA COMPLETA — drop-in de protocol_input para TODOS los consumidores
# (v4 social_deficit YA; v3 w_mat/_wealth_mat NO). El agente sobrescribe los tokens protocol_input con la
# derivada max(0, HEART_COST − team_held) una vez ⇒ misma aritmética, otra fuente. OFF ≡ bit-exact.
_DEMAND_ROUTED: bool = os.environ.get("GEMV_DEMAND_ROUTED", "0") == "1"
# Previsión territorial: "0"=off (conducta actual bit-exact), "1"=1-celda (D0, Lab 1.1),
# "map"=mapa-de-ventana (D2, Lab 1.2b — reconstruye el territorio del ventana y lo usa en el
# terminal del planificador vía desplazamiento acumulado). 1-celda y map comparten el shift de 1 paso.
_TERR_FS_MODE: str = os.environ.get("GEMV_TERR_FORESIGHT", "0")
_TERR_FORESIGHT: bool = _TERR_FS_MODE in ("1", "map", "on", "true")   # 1-celda en el shift
_TERR_FS_MAP: bool = _TERR_FS_MODE == "map"
# Filler pasivo para slots no-sujeto (aliados/clips "apostados" visibles = substrato M4).
# Se hornea en una imagen aparte (cvc-gemv-noop); el agente sujeto NO lo lleva.
_FORCE_NOOP: bool = os.environ.get("GEMV_FORCE_NOOP", "0") == "1"
# Autopsia (Lab 1.2c): en el tick indicado, volcar la descomposición del mejor terminal en casa vs no-casa.
_AUTOPSY_STEP: int = int(os.environ.get("GEMV_AUTOPSY_STEP", "-1"))
# Memoria episódica v1 (registro de 3 partes, canal territorial). off ≡ conducta actual bit-exact.
_EPISODIC: str = os.environ.get("GEMV_EPISODIC", "off")
_EPISODIC_DUMP_STEP: int = int(os.environ.get("GEMV_EPISODIC_DUMP_STEP", "-1"))
# Memoria de despensa (GEMV_PANTRY_MEM=1): el último avistamiento del pantry persiste con
# decaimiento estándar; el déficit SHELF se computa sobre percibido O recordado. OFF ≡ bit-exact.
_PANTRY_MEM: bool = os.environ.get("GEMV_PANTRY_MEM", "0") == "1"
PANTRY_MEM_MAX_AGE: int = 500  # steps — corte binario v5 (usado solo si _PANTRY_DECAY=0)
# v6 D2 — cargo-cap modelado (CargoLimitVariant.limit=4, combinado). OFF=0 ≡ v5 (held+1 sin cap).
_CARGO_CAP: int = int(os.environ.get("GEMV_CARGO_CAP", "0"))   # 0=sin cap; 4=cap del juego
# v6 D3 — memoria de despensa sin acantilado: el recuerdo decae exp(-λ·age), no muere a 500. OFF=0 ≡ v5.
_PANTRY_DECAY: bool = os.environ.get("GEMV_PANTRY_DECAY", "0") == "1"
import math as _math
_PANTRY_DECAY_LAMBDA: float = _math.log(2) / 500.0  # media vida 500 (estándar episódico memoria_v1)
# v6b D — desempate jerárquico del planner. Cláusula 3b: la d terminal sigue siendo el único juez;
# esto ordena empates (spread≤EPS) que hoy resuelve el orden de la lista. OFF=0 ≡ conducta actual.
_TIEBREAK: bool = os.environ.get("GEMV_TIEBREAK", "0") == "1"
# Eslabón 2 — arreglo N2: en el desempate degenerado, noop NO compite (quieto no gana empates).
# Repara el congelamiento (autopsía vuelta/ida). OFF=0 ≡ tiebreak actual bit-exact.
_N2_NONOOP: bool = os.environ.get("GEMV_N2_NONOOP", "0") == "1"
# Eslabón 2 — DEPÓSITO VIRTUAL: el hub RECORDADO baja la d terminal fuera de ventana (espejo del
# extractor virtual) → descongela la vuelta a H=4. OFF=0 ≡ bit-exact. Requiere memoria + v2_hybrid.
_DEPOSIT_VIRTUAL: bool = os.environ.get("GEMV_DEPOSIT_VIRTUAL", "0") == "1"
# Eslabón 3 — GEMV_EXPLORE: brújula de lo desconocido. N4 en select_tiebreak orienta la indiferencia
# hacia la zona menos rastreada (frescura decaída, curva episódica std). OFF=0 ≡ e2 bit-exact.
_EXPLORE: bool = os.environ.get("GEMV_EXPLORE", "0") == "1"
# ── ESLABÓN DERIVA — GEMV_DERIVA: el paseo del próspero (la fuente que faltaba). pregonero/deriva_diseñ[doc de diseño interna, no en el repo] ──
# El próspero (dolores gobernados, sin oportunidad conocida a tiro, sin soplo pendiente) canaliza su
# proactividad a "ir donde no he mirado": ENCIENDE el rastreo e3 (N4) en ese régimen. Es el desempate del
# reposo (N4, el más débil): jamás compite con nada real — cualquier dolor/avistamiento/soplo crea un
# no-empate o un atractor más fuerte y la deriva cede al instante (anti-hormigueo por construcción). Con
# PREGONERO ON cada paseo publica lo visto → alimenta el mapa colectivo. OFF ≡ bit-exact. Requiere memoria.
_DERIVA: bool = os.environ.get("GEMV_DERIVA", "0") in ("1", "on", "ON", "true")
# ── GEMV_EQUIP_GATED: fix del equip optimista (correctitud). [doc de diseño interna, no en el repo] ──
# El planner modelaba el equip del aligner SIEMPRE (optimista), aunque el hub no tuviera fondos → con el hub
# seco (2 agentes lo hambrean) el agente elegía equipar 986× sin lograrlo (el juego lo deniega). Con
# EQUIP_GATED el equip imaginado exige fondos CONOCIDOS del hub (team_held ≥ coste); sin ellos no existe y el
# hambre de despensa (que sí sabe reponer) toma el mando. OFF ≡ optimista bit-exact. Regresión: con pantry
# lleno (ref C6 s0, step 35) el equip cae igual.
_EQUIP_GATED: bool = os.environ.get("GEMV_EQUIP_GATED", "0") in ("1", "on", "ON", "true")
# ── ESLABÓN FORRAJEO — GEMV_FORAGE: la exploración como FUERZA f+ (la más baja de la torre). [doc de diseño interna, no en el repo] ──
# El descentramiento de G-EMV (paper §3) canalizado: "lo no rastreado" como fuente f+ DIFUSA (el anhelo del que
# no tiene nada concreto que desear). El forense de s2: 86% del tiempo el paisaje está PLANO → la fuerza no
# compite, SOSTIENE una dirección. Reemplaza la deriva-desempate v1 (segura pero inerte: miope ring=2, sin
# dirección sostenida). Entra por el canal GAIN existente (fuerza-d γ^L1) SOLO cuando no hay oportunidad de
# junction (esta la preempta: jerarquía). Altura ≈ 0.5× la oportunista SATURADA (del motor); satura por rastreo
# (explorar una zona la apaga). Objetivo GLOBAL (frontier_rel, escala mapa, no ring=2). SIN candado de régimen:
# la jerarquía protege (dolor≫junction>oportunista>forrajeo; el dolor es la base d, siempre domina lo plano).
# Requiere memoria + rastreo. OFF ≡ bit-exact.
_FORAGE: bool = os.environ.get("GEMV_FORAGE", "0") in ("1", "on", "ON", "true")
FORAGE_HEIGHT_FACTOR: float = 0.5      # altura máx del forrajeo = 0.5× la ganancia oportunista saturada (firmado)
_rastreo = None
if _EXPLORE or _DERIVA or _FORAGE:
    from memoria.rastreo import RastreoZonas
    _rastreo = RastreoZonas()
_WINDOW_RADIUS: int = 6

# ── ESLABÓN RUMBO — GEMV_RUMBO: cura las dos patologías gemelas del planner ([doc de diseño interna, no en el repo]). ──
# (CONTINUIDAD) La imaginación consulta la memoria con la misma humildad que la percepción: las junctions
#   RECORDADAS entran como tokens fantasma al rollout (dentro del grid ego), para que la maquinaria existente
#   (bump-align→appraise) les dé la MISMA oportunidad de align que a las percibidas → sin escalón de valor en
#   la frontera de lo visible (mata el 2-ciclo de s3, familia de la ORILLA). Epistemología age-blind del canal
#   posicional existente (== virtual_extractors, max_age=None): la conf la da la persistencia de memoria.
# (R1) Waypoint del forrajeo ≥ H (el rumbo vive más allá de la linterna) + descuento de llegada γ^k (reusa
#   ROLLOUT_DISCOUNT): "llegar-ya > llegar-después" → mata el stall plano de s1.
# OFF ≡ bit-exact.
_RUMBO: bool = os.environ.get("GEMV_RUMBO", "0") in ("1", "on", "ON", "true")
# Sub-flag R1 (waypoint≥H del forrajeo), SEPARADO de la CONTINUIDAD: el examen combinado mostró que R1 rompe
# el confinamiento (22×9) PERO regresa el baseline (arrastra al agente lejos → pierde el conocimiento de la
# junction → nunca alinea). Se aísla para medir la CONTINUIDAD sola (GEMV_RUMBO=1, GEMV_RUMBO_R1=0). R1 v2 se
# rediseña con el forense de la fuga (la memoria de la oportunidad debe persistir). Default 1 (sigue a RUMBO).
_RUMBO_R1: bool = os.environ.get("GEMV_RUMBO_R1", "1") in ("1", "on", "ON", "true")

if _EPISODIC == "terr":
    from memoria.episodica_v1 import EpisodicaMemoriaV1
    from memoria.memoria_v1 import apply_ghost
elif _MEM_VERSION == 2:
    from memoria.memoria_v2 import MemoriaEspacial, apply_ghost
elif _MEM_VERSION == 1:
    from memoria.memoria_v1 import MemoriaEspacial, apply_ghost
else:
    # Memoria OFF: apply_ghost se importa igualmente para la PlanCtx del planificador.
    # Es inerte (solo se invoca cuando mem is not None, que aquí no ocurre).
    from memoria.memoria_v1 import apply_ghost

FID_INV_HP:    int = 20   # hp p0
FID_INV_HP_P1: int = 21   # hp p1


def _apply_injection(
    tokens: list,
    step: int,
    real_hp: int,
    real_energy: int,
) -> tuple[list, bool, int, int]:
    """Apply linear-decay synthetic deficit to AGENT_LOC HP and/or energy tokens.

    Returns (modified_tokens, injected_flag, eff_hp, eff_energy).

    HP injection: starts at step = _INJECT_HP_DELAY, decays over _INJECT_STEPS.
    Energy injection: starts at step = 0, decays over _INJECT_ENERGY_STEPS.
    Each type independently active/inactive.
    """
    if _INJECT_HP < 0 and _INJECT_ENERGY < 0:
        return tokens, False, real_hp, real_energy

    hp_override: int | None = None
    energy_override: int | None = None

    if _INJECT_HP >= 0:
        hp_step = step - _INJECT_HP_DELAY      # effective step for HP injection
        if hp_step >= 0:
            frac_hp = min(hp_step / max(_INJECT_STEPS, 1), 1.0)
            eff_hp = round(_INJECT_HP + (real_hp - _INJECT_HP) * frac_hp)
            eff_hp = max(0, min(eff_hp, real_hp))
            if eff_hp != real_hp:
                hp_override = eff_hp

    if _INJECT_ENERGY >= 0:
        frac_en = min(step / max(_INJECT_ENERGY_STEPS, 1), 1.0)
        eff_en = round(_INJECT_ENERGY + (real_energy - _INJECT_ENERGY) * frac_en)
        eff_en = max(0, min(eff_en, real_energy))
        if eff_en != real_energy:
            energy_override = eff_en

    if hp_override is None and energy_override is None:
        return tokens, False, real_hp, real_energy

    result: list = []
    for tok in tokens:
        loc, fid, val = int(tok[0]), int(tok[1]), int(tok[2])
        if loc == AGENT_LOC:
            if hp_override is not None and fid == FID_INV_HP:
                result.append((loc, fid, hp_override % 256))
                continue
            if hp_override is not None and fid == FID_INV_HP_P1:
                result.append((loc, fid, hp_override // 256))
                continue
            if energy_override is not None and fid == FID_INV_ENERGY:
                result.append((loc, fid, energy_override % 256))
                continue
            if energy_override is not None and fid == FID_INV_ENERGY_P1:
                result.append((loc, fid, energy_override // 256))
                continue
        result.append((tok[0], tok[1], tok[2]))

    final_hp = hp_override if hp_override is not None else real_hp
    final_en = energy_override if energy_override is not None else real_energy
    return result, True, final_hp, final_en


# ── One-step local prediction ────────────────────────────────────────────────

def _shift_tokens(
    tokens: list,
    scalar_map: dict,
    drow: int,
    dcol: int,
    energy_cost: int,
) -> list:
    """Build predicted token list after moving (drow, dcol) with energy_cost.

    Spatial tokens shift to (row - drow, col - dcol).
    Tokens that exit [0,12]×[0,12] are dropped (unknown cells = empty).
    AGENT_LOC tokens are updated for energy and territory; everything else
    at AGENT_LOC is kept unchanged (HP, gear, tags, etc.).
    """
    # Previsión territorial (Lab 1.1, D0): territory:here predicho tras el movimiento.
    # Encoding VERIFICADO ([doc de diseño interna, no en el repo]): territory:{dir}@AGENT_LOC = here*3 + vecino;
    # destino de 1 paso = val%3. Token ausente ⇒ sin frontera ⇒ territorio sin cambio.
    # Gated por GEMV_TERR_FORESIGHT (OFF ⇒ foresight_here=None ⇒ conducta actual bit a bit).
    foresight_here: int | None = None
    if _TERR_FORESIGHT and energy_cost > 0:
        terr_fid = (
            FID_TERR_NORTH if drow == -1 else
            FID_TERR_SOUTH if drow == +1 else
            FID_TERR_EAST  if dcol == +1 else
            FID_TERR_WEST
        )
        cur_here = scalar_map.get((GLOBAL_LOC, FID_TERRITORY_HERE), 0)
        dir_tok = scalar_map.get((AGENT_LOC, terr_fid))
        foresight_here = cur_here if dir_tok is None else (dir_tok % 3)

    # Precompute updated energy (multipart)
    energy_update: dict[int, int] = {}  # fid → new_val
    if energy_cost > 0:
        p0 = scalar_map.get((AGENT_LOC, FID_INV_ENERGY), 0)
        p1 = scalar_map.get((AGENT_LOC, FID_INV_ENERGY_P1), 0)
        total_energy = p0 + 256 * p1
        new_energy = max(0, total_energy - energy_cost)
        energy_update[FID_INV_ENERGY]    = new_energy % 256
        energy_update[FID_INV_ENERGY_P1] = new_energy // 256

    result: list = []
    for tok in tokens:
        loc, fid, val = int(tok[0]), int(tok[1]), int(tok[2])

        if loc == PADDING_LOC:
            continue  # always drop padding

        if loc == GLOBAL_LOC:
            if foresight_here is not None and fid == FID_TERRITORY_HERE:
                result.append((loc, fid, foresight_here))
            else:
                result.append((loc, fid, val))
            continue

        if loc == AGENT_LOC:
            # Self token — update energy; territory:here es GLOBAL (se maneja arriba).
            if energy_cost > 0 and fid in energy_update:
                result.append((loc, fid, energy_update[fid]))
            else:
                result.append((loc, fid, val))
            continue

        # Spatial token: shift by inverse of movement
        row, col = divmod(loc, EGOCENTRIC_COLS)
        new_row = row - drow
        new_col = col - dcol
        if 0 <= new_row <= 12 and 0 <= new_col <= 12:
            new_loc = new_row * EGOCENTRIC_COLS + new_col
            # Don't produce tokens that collide with AGENT_LOC center
            if new_loc != AGENT_LOC:
                result.append((new_loc, fid, val))
        # else: token exits window → drop (treat as empty/unknown)

    # Si el token GLOBAL territory:here estaba ausente (=0 neutral) y la previsión predice
    # un destino no-neutral, añadirlo para que appraise lo vea (encoding D0).
    if foresight_here is not None and foresight_here != 0:
        had_terr = any(
            int(t[0]) == GLOBAL_LOC and int(t[1]) == FID_TERRITORY_HERE
            for t in tokens
        )
        if not had_terr:
            result.append((GLOBAL_LOC, FID_TERRITORY_HERE, foresight_here))

    return result


def _dest_is_blocked(tag_map: dict, action: str) -> bool:
    """True if destination cell has a TYPE_AGENT entity — move would be blocked.

    Destination of action (drow, dcol) is at (AGENT_ROW+drow, AGENT_COL+dcol)
    in the current egocentric window. If an agent occupies that cell, the move
    fails in-game and the observation stays unchanged (= noop prediction).
    This avoids the artifact where tokens at the destination shift to AGENT_LOC
    and are dropped, making rival cells look empty and desirable.
    """
    if action not in ACTION_DELTAS:
        return False
    drow, dcol = ACTION_DELTAS[action]
    dest_loc = (AGENT_ROW + drow) * EGOCENTRIC_COLS + (AGENT_COL + dcol)
    return TAG_TYPE_AGENT in tag_map.get(dest_loc, set())


def _dest_extractor_tag(tag_map: dict, action: str):
    """Si el destino del move contiene un extractor, devuelve su tag_type (para modelar el bump→cosecha);
    si no, None. La estación bloquea el move: el agente se queda y cosecha."""
    if action not in ACTION_DELTAS:
        return None
    drow, dcol = ACTION_DELTAS[action]
    dest_loc = (AGENT_ROW + drow) * EGOCENTRIC_COLS + (AGENT_COL + dcol)
    tags = tag_map.get(dest_loc, set())
    for t in tags:
        if t in EXTRACTOR_TAGS:
            return t
    return None


def _dest_is_own_hub(tag_map: dict, action: str, team_side: str) -> bool:
    """True si el destino del move es el HUB PROPIO (para modelar el bump→depósito)."""
    if action not in ACTION_DELTAS:
        return False
    own = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    drow, dcol = ACTION_DELTAS[action]
    dest_loc = (AGENT_ROW + drow) * EGOCENTRIC_COLS + (AGENT_COL + dcol)
    tags = tag_map.get(dest_loc, set())
    return (TAG_TYPE_HUB in tags) and (own in tags)


def _gain_opportunity(s_curr, scalar_map, tag_map, team_side, mem, world_step):
    """Córtex C4 (I2) — la oportunidad territorial como FUERZA-d propagada por proximidad. Devuelve
    (gear_rel, gain_scalar) o None. gain_scalar = Δd_align · confianza: el Δd que el align realizaría
    (ganancia ya modelada: bono_S + retirar déficit territorial − coste del heart), por la confianza de
    memoria de la gear. El planner aplica gain_scalar·γ^(L1 terminal→gear) a CADA terminal → el terminal
    más cercano a la gear vale más → gradiente continuo hacia la cadena equipar→alinear (no un susurro).
    Requiere heart (precondición del align; sin heart manda la balda de hearts f− = comer primero)."""
    if not (_GAIN and _MARCADOR):
        return None
    from motor.model import State as _St
    from appraisal.appraisal_shelf import (territorial_RS as _tRS, hearts_deficit_R as _hdef,
                                           W_TERR_R as _wr, T_TERR as _tt, W_TERR_S as _ws, T_OURS as _to)
    mis_hearts = get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART)
    if mis_hearts < 1 and not _HEART_GAIN:
        return None                                    # sin heart (OFF): la oportunidad no es realizable aún
    own_net = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
    # ¿junction ganable conocida? (percibida o recordada)
    perceived_gain = any(TAG_TYPE_JUNCTION in t and own_net not in t for t in tag_map.values())
    mem_gain = any(cls in ("junction_gray", "junction_rival")
                   for (_, _, cls) in getattr(mem, "_entries", {})) if mem is not None else False
    if not (perceived_gain or mem_gain):
        return None
    def _rel(loc): return (loc // EGOCENTRIC_COLS - AGENT_ROW, loc % EGOCENTRIC_COLS - AGENT_COL)
    def _nearest_rel(perc_pred, mem_classes):
        """rel de la estructura conocida más cercana: percibida (conf 1.0) → recordada (conf decaída)."""
        best = None
        for loc, tags in tag_map.items():
            if perc_pred(tags):
                r = _rel(loc); d = abs(r[0]) + abs(r[1])
                if best is None or d < best[0]: best = (d, r)
        if best is not None:
            return best[1], 1.0
        if mem is not None and hasattr(mem, "_entries"):
            ar, ac = getattr(mem, "_agent_world", (0, 0))
            cand = [((wr - ar, wc - ac), e) for (wr, wc, cls), e in mem._entries.items() if cls in mem_classes]
            if cand:
                (rel, e) = min(cand, key=lambda x: abs(x[0][0]) + abs(x[0][1]))
                return rel, _math.exp(-_PANTRY_DECAY_LAMBDA * max(0, world_step - getattr(e, "last_seen_step", world_step)))
        return None, 1.0
    # OBJETIVO de la fuerza — ARBITRAJE de la cadena (equip → heart → alinear), propaga al eslabón alcanzable:
    #  1) sin aligner → gear station (EQUIPAR primero; barato, una vez, no se consume al alinear).
    #  2) con aligner, sin heart (HEART_GAIN) → craftear/minar-para-heart (el DESEO DE ANCHURA).
    #  3) con aligner ∧ heart (∧ CHAIN_COMPLETE) → la junction ganable (ALINEAR, eslabón final).
    #  Valor PRESTADO por la cadena en todos: el opp_value del align (abajo). OFF: has_heart siempre → 1/3 (bit-exact).
    has_aligner = get_multipart(scalar_map, AGENT_LOC, FID_INV_ALIGNER) > 0
    has_heart = mis_hearts >= 1
    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    def _heart_craft_target():
        """Eslabón craftear-heart (HEART_GAIN): hub si PUEDE craftear (≥HEART_COST de CADA elemento, conocido
        fresco: percibido o pantry) → ir al hub (get_heart gratis o make); si no, el extractor del elemento MÁS
        deficitario para [7,7,7,7] (portfolio, no cuello único; percibido/recordado/pregonado). (rel, conf) o (None,1.0)."""
        from appraisal.appraisal_shelf import _TEAM_FIDS as _TF, HEART_COST as _HC
        from memoria.memoria_v1 import _EXTRACTOR_CLS as _ECLS2
        _order = ("extractor_oxygen", "extractor_carbon", "extractor_germanium", "extractor_silicon")
        if any(TAG_TYPE_HUB in t and own_team_tag in t for t in tag_map.values()):
            held = [get_scalar(scalar_map, GLOBAL_LOC, f) for f in _TF]
        else:
            _pm = _pantry_ctx.get('vals') if _PANTRY_MEM else None
            if not _pm:
                return None, 1.0                       # sin conocimiento del hub → sin objetivo de heart
            held = [_pm.get(f, 0.0) for f in _TF]
        short = [max(0.0, _HC - held[i]) for i in range(len(_TF))]
        if not any(sv > 0.0 for sv in short):          # hub PUEDE craftear → ir al hub
            return _nearest_rel(lambda tags: TAG_TYPE_HUB in tags and own_team_tag in tags, ("hub",))
        for i in sorted(range(len(_TF)), key=lambda j: -short[j]):   # portfolio: el más lejos de HEART_COST
            if short[i] <= 0.0:
                break
            _cls = _order[i]
            r, c = _nearest_rel(lambda tags, _c=_cls: any(_ECLS2.get(tt) == _c for tt in (set(tags) & EXTRACTOR_TAGS)), (_cls,))
            if r is not None:
                return r, c
        return None, 1.0
    gear_rel = None; conf = 1.0
    if not has_aligner:                                # 1) EQUIPAR primero
        gear_rel, conf = _nearest_rel(lambda tags: TAG_TYPE_ALIGNER in tags, ("gear_aligner",))
    elif not has_heart:                                # 2) CRAFTEAR/MINAR-PARA-HEART (HEART_GAIN; OFF nunca llega aquí)
        gear_rel, conf = _heart_craft_target()
        if gear_rel is None:
            return None                                # sin objetivo de heart productivo → sin deseo
    elif _CHAIN_COMPLETE:                              # 3) ALINEAR
        gear_rel, conf = _nearest_rel(lambda tags: TAG_TYPE_JUNCTION in tags and own_net not in tags,
                                      ("junction_gray", "junction_rival"))
    if gear_rel is None:                               # PRESTADO (gear station): aligner+heart sin junction, o sin CHAIN
        gear_rel, conf = _nearest_rel(lambda tags: TAG_TYPE_ALIGNER in tags, ("gear_aligner",))
    if gear_rel is None:
        return None
    # VALOR DE LA OPORTUNIDAD (magnitud de la fuerza): el d RECLAMABLE por saciar el hambre territorial
    # — relevar el déficit_R territorial (→0) y saturar la pertenencia bono_S. SATURANTE por abundancia
    # (T_TERR=1: conocer 1 o 5 junctions ganables da el mismo déficit 2.40 → misma fuerza; anti-vicio del
    # conquistador). NO resta el coste del heart: la fuerza es la oportunidad; el heart lo cuida su balda f−
    # (comer primero para hearts). Es EL HAMBRE TERRITORIAL HECHA FUERZA-d (la vía del §C1, autopsia residual).
    def_now, bono_now, n_gain, n_ours = _tRS(scalar_map, tag_map, team_side, remembered=_terr_ctx.get('remembered'))
    if n_gain < 1:
        return None
    full_bono = _ws * 1.0                              # pertenencia saturada (todo el territorio nuestro)
    posR = (s_curr.pR - s_curr.nR) + def_now           # quitar el déficit territorial del eje R
    posS = (s_curr.pS - s_curr.nS) + (full_bono - bono_now)
    s_conq = _St(pF=s_curr.pF, nF=s_curr.nF, pR=max(0.0, posR), nR=max(0.0, -posR),
                 pS=max(0.0, posS), nS=max(0.0, -posS))
    opp_value = opponent_distance(s_curr, _ACTIVE_CFG) - opponent_distance(s_conq, _ACTIVE_CFG)
    if opp_value <= 0.0:
        return None                                    # nada que reclamar (riqueza no cura): sin fuerza
    # (A) GUARDA DE COLCHÓN — solo a los targets que DRENAN el hub (equipar/craftear-heart), NO al alinear
    # (que gasta el heart del agente, no el hub). Afinación 3 (el aporreador): cushion=0 MATA el deseo →
    # None (no residual: la fusión de EQUIP_GATED es completa, el freno de los 986 bumps no se pierde).
    if _EQUIP_CUSHION and not (has_aligner and has_heart):
        _cush = _hub_cushion(scalar_map, tag_map, team_side)
        if _cush <= 0.0:
            return None
        opp_value *= _cush
    if os.environ.get("GEMV_GAIN_DBG"):
        _tgt = ("heart" if (has_aligner and not has_heart) else
                ("junction" if (has_aligner and has_heart and _CHAIN_COMPLETE) else "gear"))
        _log(f"GAIN_DBG step={world_step} target={_tgt} branch={'perc' if conf >= 1.0 else 'mem'} "
             f"target_rel={gear_rel} conf={conf:.3f} n_gain={n_gain}")
    return (gear_rel, opp_value * conf)


def _deposit_gain(s_curr, scalar_map, tag_map, team_side, mem, world_step):
    """Pieza 2 — ATRACTOR DE DEPÓSITO. Con material a bordo Y dolor de despensa activo, el hub CONOCIDO se vuelve
    objetivo de la ganancia (misma forma que _gain_opportunity: (hub_rel, Δd·conf)). Δd = alivio del dolor de
    despensa al depositar el cargo (eje S; por debajo del dolor de cuerpo, coherente con D3). SATURANTE: almacén
    ya suficiente → dolor 0 → Δd≤0 → None. Objetivo: hub percibido (conf 1.0) o recordado (conf decaída; requiere
    HUB_PERSIST para sobrevivir fuera de ventana). Usa la ficha de depósito ya existente (model_deposit) al llegar."""
    if not (_DEPOSIT_ATTRACTOR and _MARCADOR and _DESPENSA):
        return None
    from appraisal.appraisal_shelf import (_TEAM_FIDS as _TF, _OWN_FIDS as _OF,
                                           despensa_deficit_S as _dds)
    from motor.model import State as _St
    cargo = [get_multipart(scalar_map, AGENT_LOC, f) for f in _OF]
    if sum(cargo) <= 0:
        return None                                        # sin material a bordo: nada que depositar
    if _MINING_BATCH and 0 < sum(cargo) < _MINING_LOTE:
        return None                                        # aún llenando el lote → cede al minado (no depositar todavía)
    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    # hub conocido: percibido (conf 1.0) o recordado (conf decaída). Rel ego + fuente de team_held coherente.
    hub_rel = None; conf = 1.0
    for loc, tags in tag_map.items():
        if TAG_TYPE_HUB in tags and own_team_tag in tags:
            hub_rel = (loc // EGOCENTRIC_COLS - AGENT_ROW, loc % EGOCENTRIC_COLS - AGENT_COL); break
    if hub_rel is not None:
        team_held = [get_scalar(scalar_map, GLOBAL_LOC, f) for f in _TF]      # percibido: manda
    else:
        if mem is not None and hasattr(mem, "_entries"):
            ar, ac = getattr(mem, "_agent_world", (0, 0))
            cand = [((wr - ar, wc - ac), e) for (wr, wc, cls), e in mem._entries.items() if cls == "hub"]
            if cand:
                (hub_rel, e) = min(cand, key=lambda x: abs(x[0][0]) + abs(x[0][1]))
                conf = _math.exp(-_PANTRY_DECAY_LAMBDA * max(0, world_step - getattr(e, "last_seen_step", world_step)))
        if hub_rel is None:
            return None                                    # hub desconocido: sin objetivo de depósito
        pm = _pantry_ctx.get('vals') if _PANTRY_MEM else None
        team_held = [pm.get(f, 0.0) for f in _TF] if pm else [0.0] * len(_TF)
    pain = _dds(team_held, True, w=_DESPENSA_W)
    if pain <= 0.0:
        return None                                        # almacén suficiente: saturado, no atrae
    team_after = [team_held[i] + cargo[i] for i in range(len(_TF))]
    relief = pain - _dds(team_after, True, w=_DESPENSA_W)   # alivio del dolor al depositar
    if relief <= 0.0:
        return None
    posS = (s_curr.pS - s_curr.nS) + relief                 # depositar sube pos_S (quita dolor de despensa)
    s_dep = _St(pF=s_curr.pF, nF=s_curr.nF, pR=s_curr.pR, nR=s_curr.nR,
                pS=max(0.0, posS), nS=max(0.0, -posS))
    dep_value = opponent_distance(s_curr, _ACTIVE_CFG) - opponent_distance(s_dep, _ACTIVE_CFG)
    if dep_value <= 0.0:
        return None
    if _RESTOCK_HEIGHT:
        # (1) hub = fijo permanente → conf 1.0 (no decae); (2) infabricable (dep_value>0 = desbloquea la cadena)
        # → altura de conquista. dep_value>0 sigue siendo la PUERTA (sólo el material que alivia).
        _val = _W_RESTOCK_UNBLOCK
    else:
        _val = dep_value * conf
    if os.environ.get("GEMV_GAIN_DBG"):
        _log(f"DEPOSIT_GAIN step={world_step} hub_rel={hub_rel} conf={conf:.3f} cargo={sum(cargo)} "
             f"pain={pain:.3f} relief={relief:.3f} dep_value={dep_value:.3f} val={_val:.3f}")
    return (hub_rel, _val)


def _mining_gain(s_curr, scalar_map, tag_map, team_side, mem, world_step):
    """Pieza — MINADO DIRIGIDO AL CUELLO. Ganancia de extractor dependiente de la escasez de SU material en el hub
    (escala peor-material): sólo el extractor del material que marca el déficit da alivio → atrae; el de uno que
    sobra, 0. Minero VACÍO (con material a bordo manda el atractor de depósito). Valor = alivio del dolor al reponer
    ese material a la receta; saturante (hub suficiente → 0). Objetivo: extractor percibido (conf 1.0) o recordado
    (conf decaída). Misma forma (rel, Δd·conf). model.py INTOCABLE."""
    if not (_MINING_GAIN and _MARCADOR and _DESPENSA):
        return None
    from appraisal.appraisal_shelf import (_TEAM_FIDS as _TF, _OWN_FIDS as _OF,
                                           despensa_deficit_S as _dds, ALIGNER_RECIPE as _REC)
    from memoria.memoria_v1 import _EXTRACTOR_CLS as _ECLS
    _ORDER = ("extractor_oxygen", "extractor_carbon", "extractor_germanium", "extractor_silicon")
    _cargo_now = sum(get_multipart(scalar_map, AGENT_LOC, f) for f in _OF)
    _batch_cap = _MINING_LOTE if _MINING_BATCH else 1
    if _cargo_now >= _batch_cap:
        return None                                        # lote lleno (o, sin batch, con carga): deposita, no mina
    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    hub_perc = any(TAG_TYPE_HUB in t and own_team_tag in t for t in tag_map.values())
    if hub_perc:
        team_held = [get_scalar(scalar_map, GLOBAL_LOC, f) for f in _TF]
    else:
        pm = _pantry_ctx.get('vals') if _PANTRY_MEM else None
        if not pm:
            return None                                    # sin conocimiento del hub: dolor no dirigible
        team_held = [pm.get(f, 0.0) for f in _TF]
    pain = _dds(team_held, True, w=_DESPENSA_W)
    if pain <= 0.0:
        return None                                        # hub suficiente: saturado, ningún extractor atrae más
    def _relief(idx):
        th2 = list(team_held); th2[idx] = max(th2[idx], _REC[idx])   # reponer ESE material a la receta
        return pain - _dds(th2, True, w=_DESPENSA_W)
    best = None                                            # (value, rel)
    def _consider(rel, cls, conf):
        nonlocal best
        if cls not in _ORDER:
            return
        r = _relief(_ORDER.index(cls))
        if r <= 0.0:
            return                                         # sólo el material-cuello (puerta intacta)
        val = (_W_RESTOCK_UNBLOCK if _RESTOCK_HEIGHT else r) * conf   # altura de conquista si infabricable
        d = abs(rel[0]) + abs(rel[1])
        if best is None or val > best[0] or (val == best[0] and d < abs(best[1][0]) + abs(best[1][1])):
            best = (val, rel)
    for loc, tags in tag_map.items():
        for tt in (set(tags) & EXTRACTOR_TAGS):
            _consider((loc // EGOCENTRIC_COLS - AGENT_ROW, loc % EGOCENTRIC_COLS - AGENT_COL), _ECLS.get(tt), 1.0)
    if mem is not None and hasattr(mem, "_entries"):
        ar, ac = getattr(mem, "_agent_world", (0, 0))
        for (wr, wc, cls), e in mem._entries.items():
            if cls in _ORDER:
                conf = _math.exp(-_PANTRY_DECAY_LAMBDA * max(0, world_step - getattr(e, "last_seen_step", world_step)))
                _consider((wr - ar, wc - ac), cls, conf)
    if best is None:
        return None
    if os.environ.get("GEMV_GAIN_DBG"):
        _log(f"MINING_GAIN step={world_step} ext_rel={best[1]} value={best[0]:.3f} pain={pain:.3f}")
    return (best[1], best[0])


def _supply_motor(s_curr, scalar_map, tag_map, team_side, mem, world_step):
    """CONSTITUCIÓN ECONÓMICA (GEMV_ECON_CONST) — MOTOR ÚNICO DE ABASTECIMIENTO. Devuelve (rel, value) o None.
    Sustituye a _mining_gain + _deposit_gain + RESTOCK_PREEMPT/HEIGHT cuando ECON_CONST está ON.
    · SATURACIÓN: activo sólo con hub INFABRICABLE (∃x: team_x < recipe_x, receta ALIGNER_RECIPE); fabricable → None.
    · DOS CARAS por cargo (lote L=_MINING_LOTE=min(_MINING_BATCH_SIZE,cargo_cap)): cargo<L → extractor del cuello; cargo≥L → hub.
    · ALTURA = _ECON_ALTURA_BASE (W_TERR_R) · TECHO CONTINUO exp(−dolor_cuerpo/P_REF) · conf(memoria).
    El preempt sobre la conquista lo aplica el sitio de llamada (motor≠None ⇒ conquista excluida)."""
    if not (_ECON_CONST and _MARCADOR):
        return None
    from appraisal.appraisal_shelf import (_TEAM_FIDS as _TF, _OWN_FIDS as _OF, ALIGNER_RECIPE as _REC)
    from memoria.memoria_v1 import _EXTRACTOR_CLS as _ECLS
    _ORDER = ("extractor_oxygen", "extractor_carbon", "extractor_germanium", "extractor_silicon")
    own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    # estado del almacén: percibido manda; si no, memoria de despensa (sin ninguno → no dirigible)
    hub_perc = any(TAG_TYPE_HUB in t and own_team_tag in t for t in tag_map.values())
    if hub_perc:
        team_held = [get_scalar(scalar_map, GLOBAL_LOC, f) for f in _TF]
    else:
        pm = _pantry_ctx.get('vals') if _PANTRY_MEM else None
        if not pm:
            return None
        team_held = [pm.get(f, 0.0) for f in _TF]
    # (B) SUPPLY_SLACK: abastecer hasta la HOLGURA OBJETIVO (SLACK=vital+equip), no solo hasta fabricable.
    # OFF: _target = _REC (vital) → comportamiento binario histórico. `short` = déficit al objetivo → el cuello
    # es el elemento más deficitario p/SLACK ⇒ PORTFOLIO (mina los cuatro para mantener holgura).
    _target = _slack_target() if _SUPPLY_SLACK else list(_REC)
    short = [max(0.0, _target[i] - team_held[i]) for i in range(len(_REC))]
    cargo = sum(get_multipart(scalar_map, AGENT_LOC, f) for f in _OF)
    # PRECEDENCIA DEL CARGADO (i, GAIN): la saturación (hub ≥ objetivo) apaga la cara MINADO, PERO un cargado
    # (cara DEPÓSITO) siempre tiene ruta al hub (deposita al margen de la saturación: bolsillo liberado). OFF:
    # la saturación apaga todo (bit-exact histórico).
    _deposit_face = (cargo >= _MINING_LOTE)
    if (not any(sv > 0.0 for sv in short)) and not (_CARGO_PRECEDENCE and _deposit_face):
        return None                                        # hub ≥ objetivo → motor OFF (saturación de la cara minado)
    # techo continuo del cuerpo (con la config del agente)
    body_pain = _econ_body_pain(scalar_map, _ACTIVE_CFG)
    altura = _econ_altura_efectiva(body_pain, _ACTIVE_CFG)
    # STALE_FRESH: frescura de la creencia hub-infabricable (percibido ⇒ 1.0; recordado ⇒ decay del pantry).
    # Descuenta el valor de la cara MINADO (no la de depósito, que ya trae la conf del hub recordado).
    _hub_fresh = 1.0
    if _ECON_STALE_FRESH and not hub_perc:
        _hub_fresh = _math.exp(-_PANTRY_DECAY_LAMBDA * float(_pantry_ctx.get('age', 0.0) or 0.0))
    if _deposit_face:
        # CARA DEPÓSITO → hub (percibido conf 1.0, o recordado conf decaída)
        hub_rel = None; conf = 1.0
        for loc, tags in tag_map.items():
            if TAG_TYPE_HUB in tags and own_team_tag in tags:
                hub_rel = (loc // EGOCENTRIC_COLS - AGENT_ROW, loc % EGOCENTRIC_COLS - AGENT_COL); break
        if hub_rel is None and mem is not None and hasattr(mem, "_entries"):
            ar, ac = getattr(mem, "_agent_world", (0, 0))
            cand = [((wr - ar, wc - ac), e) for (wr, wc, cls), e in mem._entries.items() if cls == "hub"]
            if cand:
                (hub_rel, e) = min(cand, key=lambda x: abs(x[0][0]) + abs(x[0][1]))
                conf = _math.exp(-_PANTRY_DECAY_LAMBDA * max(0, world_step - getattr(e, "last_seen_step", world_step)))
        if hub_rel is None:
            return None
        if os.environ.get("GEMV_GAIN_DBG"):
            _log(f"ECON_MOTOR step={world_step} cara=DEPOSITO hub_rel={hub_rel} conf={conf:.3f} "
                 f"cargo={cargo} bp={body_pain:.3f} alt={altura:.3f}")
        return (hub_rel, altura * conf)
    # CARA MINADO → extractor del material-CUELLO (mayor shortfall, spec §1.1; desempate por distancia)
    best = None                                            # ((shortfall, -dist), rel, conf) maximizado
    def _consider(rel, cls, conf):
        nonlocal best
        if cls not in _ORDER:
            return
        i = _ORDER.index(cls)
        if short[i] <= 0.0:
            return                                         # sólo materiales que faltan (puerta del cuello)
        key = (short[i], -(abs(rel[0]) + abs(rel[1])))
        if best is None or key > best[0]:
            best = (key, rel, conf)
    for loc, tags in tag_map.items():
        for tt in (set(tags) & EXTRACTOR_TAGS):
            _consider((loc // EGOCENTRIC_COLS - AGENT_ROW, loc % EGOCENTRIC_COLS - AGENT_COL), _ECLS.get(tt), 1.0)
    if mem is not None and hasattr(mem, "_entries"):
        ar, ac = getattr(mem, "_agent_world", (0, 0))
        for (wr, wc, cls), e in mem._entries.items():
            if cls in _ORDER:
                conf = _math.exp(-_PANTRY_DECAY_LAMBDA * max(0, world_step - getattr(e, "last_seen_step", world_step)))
                _consider((wr - ar, wc - ac), cls, conf)
    if best is None:
        return None                                        # sin extractor-cuello conocido: sin objetivo
    if os.environ.get("GEMV_GAIN_DBG"):
        _log(f"ECON_MOTOR step={world_step} cara=MINADO ext_rel={best[1]} conf={best[2]:.3f} "
             f"cargo={cargo} bp={body_pain:.3f} alt={altura:.3f} hub_fresh={_hub_fresh:.3f}")
    return (best[1], altura * best[2] * _hub_fresh)


_FORAGE_HEIGHT_CACHE = None
def _forage_height_ref():
    """Altura MÁXIMA del forrajeo = FORAGE_HEIGHT_FACTOR(0.5) × la ganancia OPORTUNISTA SATURADA de REFERENCIA
    (del motor, una vez): Δd de pasar de un estado neutral en R/S a la satisfacción territorial plena
    (pos_R=W_TERR_R, pos_S=W_TERR_S). Es una CONSTANTE (no depende de la saciedad actual): el forrajeo existe
    sobre todo cuando NO hay nada concreto que desear. La junction real (opp_value ~= la oportunista) siempre
    la supera por altura."""
    global _FORAGE_HEIGHT_CACHE
    if _FORAGE_HEIGHT_CACHE is None:
        from motor.model import State as _St
        from appraisal.appraisal_shelf import W_TERR_R as _wr, W_TERR_S as _ws
        s_neu = _St(pF=1.0, nF=0.0, pR=0.0, nR=0.0, pS=0.0, nS=0.0)
        s_full = _St(pF=1.0, nF=0.0, pR=_wr, nR=0.0, pS=_ws, nS=0.0)
        ref = opponent_distance(s_neu, _ACTIVE_CFG) - opponent_distance(s_full, _ACTIVE_CFG)
        _FORAGE_HEIGHT_CACHE = FORAGE_HEIGHT_FACTOR * max(0.0, ref)
    return _FORAGE_HEIGHT_CACHE


def _forage_gain(s_curr, mem, world_step):
    """ESLABÓN FORRAJEO (F2): la exploración como fuerza f+ DÉBIL por el canal GAIN. Devuelve
    (forage_rel, forage_scalar, GAIN_GAMMA) o None. Dirección = frontera GLOBAL de lo no rastreado
    (rastreo.frontier_rel, capada a waypoint sostenido). Altura = _forage_height_ref() (constante, 0.5× la
    oportunista saturada de referencia) × frescura de la frontera (satura por rastreo: zona vista → 0).
    SIN candado: solo se llama cuando no hay oportunidad de junction (la jerarquía la preempta), y como es
    débil, el dolor (base d) la domina en lo no-plano; existe también en el saciado (anhelo estructural)."""
    if not _FORAGE or _rastreo is None or mem is None or not hasattr(mem, "_agent_world"):
        return None
    ar, ac = mem._agent_world
    # R1 (RUMBO): waypoint ≥ H — el rumbo vive MÁS ALLÁ de la linterna. Con el waypoint fuera del horizonte,
    # acercarse SIEMPRE reduce el mejor terminal L1 (el γ^L1 de la gain es el descuento de llegada: llegar-ya >
    # llegar-después) → mata el stall plano de s1. OFF (RUMBO off) → cap=7 (línea base) bit-exact.
    _cap = (_HORIZON + 4) if (_RUMBO and _RUMBO_R1) else 7
    rel, fresh = _rastreo.frontier_rel(ar, ac, world_step, cap=_cap)
    if rel is None or fresh <= 1e-9 or rel == (0, 0):
        return None
    forage_scalar = _forage_height_ref() * fresh    # altura fija × frescura de la frontera (saturación por rastreo)
    if forage_scalar <= 0.0:
        return None
    if os.environ.get("GEMV_FORAGE_DBG"):
        _log(f"FORAGE_DBG step={world_step} rel={rel} fresh={fresh:.3f} scalar={forage_scalar:.4f}")
    return (rel, forage_scalar, GAIN_GAMMA)


def _waypoint_reexpress(gear_rel, tag_map, dest_tipo="aligner"):
    """Córtex C3 — re-expresa el atractor de la gear station (destino fijo off-ciclo) como la siguiente
    MIGA de la ruta conocida cuando el destino está FUERA de alcance (>H-1 cardinal). Solo re-apunta el
    susurro N3 (mismo desempate, ninguna fuerza nueva). Percepción manda: una miga desmentida por un muro
    percibido se salta. Destino alcanzable directo (≤H-1) ⇒ las migas NO intervienen (gate e control).

    FRAME-INDEPENDIENTE: la posición de la miga RELATIVA al agente es `gear_rel + (miga − destino)`,
    ambos DIFERENCIAS en coords de juego → no depende del marco de memoria (spawn-origen) ni del absoluto.
    (El bug del 1er examen mezcló aw del marco-memoria con coords de juego de la ruta.)"""
    if not _WAYPOINTS or gear_rel is None or not _rutas_ctx.get('rutas'):
        return gear_rel
    H = _HORIZON
    if abs(gear_rel[0]) + abs(gear_rel[1]) <= H - 1:
        return gear_rel                        # la ruta es para lo LEJANO; cerca manda el destino directo
    ruta = next((R for R in _rutas_ctx['rutas'] if R.get('destino_tipo') == dest_tipo), None)
    if ruta is None or not ruta.get('migas'):
        return gear_rel
    dr, dc = ruta['destino']                   # destino de la ruta (coords de juego)
    def mrel(m):                               # miga relativa al agente = gear_rel + (miga − destino)
        return (gear_rel[0] + (m[0] - dr), gear_rel[1] + (m[1] - dc))
    def _wall_at(r):
        if abs(r[0]) > 6 or abs(r[1]) > 6:
            return False                       # fuera de ventana: la percepción no la desmiente
        loc = (AGENT_ROW + r[0]) * EGOCENTRIC_COLS + (AGENT_COL + r[1])
        return TAG_TYPE_WALL in tag_map.get(loc, set())
    migas = [tuple(m) for m in ruta['migas']]
    reach = None                               # la miga MÁS AVANZADA alcanzable en horizonte, no desmentida
    for m in migas:
        r = mrel(m)
        if _wall_at(r):
            continue                           # miga desmentida (muro percibido) → se salta (gate d)
        if abs(r[0]) + abs(r[1]) <= H - 1:
            reach = r
    if reach is not None:
        return reach
    cand = [mrel(m) for m in migas if not _wall_at(mrel(m))]
    if cand:                                   # ninguna alcanzable: apuntar a la miga no desmentida más cercana
        return min(cand, key=lambda r: abs(r[0]) + abs(r[1]))
    return gear_rel                            # toda la ruta desmentida → destino directo


def _compute_attractor(scalar_map, tag_map, team_side, s_curr, appr_debug, mem, virtual_extractors,
                       world_step=0):
    """v6b N3 — el atractor que el ESTADO señala (brújula, no deseo nuevo). Posición egocéntrica
    relativa (fila,col) o None. Cargado+demanda→hub; vacío+urgR→extractor demandado. Percepción manda.
    Eslabón 4: filas marcador (junction/gear-station/hub) con prioridad cuando GEMV_MARCADOR."""
    from appraisal.appraisal_v4 import _MAT_FIDS as _mf
    own_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    inv_fids = [_mf[x][2] for x in _mf]
    held = sum(get_multipart(scalar_map, AGENT_LOC, f) for f in inv_fids)
    demands = (appr_debug or {}).get("demands", {})
    demand_live = any(v > 0 for v in demands.values()) if demands else True
    urgR = s_curr.pR < 2.0

    def _rel(loc):
        return (loc // EGOCENTRIC_COLS - AGENT_ROW, loc % EGOCENTRIC_COLS - AGENT_COL)

    def _nearest(pred):
        best = None
        for loc, tags in tag_map.items():
            if pred(tags):
                r = _rel(loc); d = abs(r[0]) + abs(r[1])
                if best is None or d < best[0]:
                    best = (d, r)
        return best[1] if best else None

    # ── Eslabón 4 — atractores del marcador (prioridad; candado de frontera por fila) ──
    if _MARCADOR:
        own_net = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
        mis_hearts = get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART)
        has_aligner = get_multipart(scalar_map, AGENT_LOC, FID_INV_ALIGNER) > 0

        def _nearest_mem(classes):
            """Posición relativa de la entrada de memoria más cercana de esas clases (recordado)."""
            if mem is None or not hasattr(mem, "_entries"):
                return None
            ar, ac = getattr(mem, "_agent_world", (0, 0))
            cand = [((wr - ar), (wc - ac)) for (wr, wc, cls) in mem._entries if cls in classes]
            return min(cand, key=lambda r: abs(r[0]) + abs(r[1])) if cand else None

        mem_gain = any(cls in ("junction_gray", "junction_rival")
                       for (_, _, cls) in getattr(mem, "_entries", {})) if mem is not None else False
        knows_gain = any(TAG_TYPE_JUNCTION in t and own_net not in t for t in tag_map.values()) or mem_gain
        # 1) heart + aligner + junction ganable conocida → junction (percibida → recordada)
        if mis_hearts >= 1 and has_aligner:
            j = _nearest(lambda t: TAG_TYPE_JUNCTION in t and own_net not in t)
            if j is None:
                j = _nearest_mem(("junction_gray", "junction_rival"))
            if j is not None:
                return j
        # 2) hambre territorial + heart + SIN aligner → gear station (percibida → recordada)
        if knows_gain and mis_hearts >= 1 and not has_aligner:
            g = _nearest(lambda t: TAG_TYPE_ALIGNER in t)
            if g is None:
                g = _nearest_mem(("gear_aligner",))
            if g is not None:
                return _waypoint_reexpress(g, tag_map)   # C3: miga si la gear está lejos (frame-independiente)
        # 3) hambre de hearts (mis_hearts<1) + hub conocido → hub (TANTEO; candado anti-peregrinación:
        #    si el hub falló recientemente en dar heart, el recuerdo decaído lo enfría)
        if mis_hearts < 1 and knows_gain:
            import math as _m
            fail = _terr_ctx.get('hub_fail_step', -1)
            fresh_fail = fail >= 0 and _m.exp(-_PANTRY_DECAY_LAMBDA * (world_step - fail)) > 0.5
            if not fresh_fail:
                h = _nearest(lambda t: TAG_TYPE_HUB in t and own_tag in t)
                if h is not None:
                    return h

    if held > 0 and demand_live:
        # hub: percibido (tag) → recordado (mem)
        best = None
        for loc, tags in tag_map.items():
            if TAG_TYPE_HUB in tags and own_tag in tags:
                r = _rel(loc); d = abs(r[0]) + abs(r[1])
                if best is None or d < best[0]:
                    best = (d, r)
        if best:
            return best[1]
        if mem is not None and hasattr(mem, "_entries"):
            ar, ac = getattr(mem, "_agent_world", (0, 0))
            cand = [((wr - ar), (wc - ac)) for (wr, wc, cls) in mem._entries if cls == "hub"]
            if cand:
                return min(cand, key=lambda r: abs(r[0]) + abs(r[1]))
        return None
    if held == 0 and urgR:
        # extractor demandado: percibido (appr_debug) → virtual (recordado)
        exts = (appr_debug or {}).get("extractors", [])
        rels = [_rel(int(loc)) for (loc, _d, _w) in exts] if exts else []
        if rels:
            return min(rels, key=lambda r: abs(r[0]) + abs(r[1]))
        if virtual_extractors:
            return min(((vr, vc) for (vr, vc, _f) in virtual_extractors),
                       key=lambda r: abs(r[0]) + abs(r[1]))
        return None
    return None


def _chain_align_credit(s_curr, scalar_map, tag_map, team_side, mem, world_step) -> float:
    """Córtex C2 — crédito de la cadena equip→align para el terminal donde se equipó (D1). Devuelve
    el Δd del `align` (balda territorial R+S, YA modelada) descontado por confianza de memoria del
    destino y distancia restante (γ^D). 0 si la cadena no existe (candados D2). Escalar por-tick:
    en el horizonte, `n_gain/n_ours/heart` no cambian entre el estado actual y un terminal recién-
    equipado (equipar no toca junctions ni consume heart) ⇒ el Δd es idéntico ⇒ calcularlo una vez
    es EXACTO. Propaga valor existente; no crea valor."""
    if not (_CHAIN and _MARCADOR):
        return 0.0
    from motor.model import State as _St
    from appraisal.appraisal_shelf import (territorial_RS as _tRS, hearts_deficit_R as _hdef,
                                           W_TERR_R as _wr, T_TERR as _tt, W_TERR_S as _ws, T_OURS as _to)
    mis_hearts = get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART)
    if mis_hearts < 1:
        return 0.0                                    # sin heart → el align no paga (candado D2.5 / gate c)
    own_net = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
    # Destino: junction ganable CONOCIDA más cercana. Percibida (conf 1.0) manda sobre recordada (conf decaída).
    best = None    # (dist_L1, conf)
    for loc, tags in tag_map.items():
        if TAG_TYPE_JUNCTION in tags and own_net not in tags:
            d = abs(loc // EGOCENTRIC_COLS - AGENT_ROW) + abs(loc % EGOCENTRIC_COLS - AGENT_COL)
            if best is None or d < best[0]:
                best = (d, 1.0)
    if best is None and mem is not None and hasattr(mem, "_entries"):
        ar, ac = getattr(mem, "_agent_world", (0, 0))
        for (wr, wc, cls), e in mem._entries.items():
            if cls in ("junction_gray", "junction_rival"):
                d = abs(wr - ar) + abs(wc - ac)
                conf = _math.exp(-_PANTRY_DECAY_LAMBDA * max(0, world_step - getattr(e, "last_seen_step", world_step)))
                if best is None or d < best[0]:
                    best = (d, conf)
    if best is None:
        return 0.0                                    # sin junction ganable conocida → la cadena NO existe (gate c)
    dist_L1, conf = best
    # Δd del align (balda R+S modelada): alinear una ganable ⇒ n_gain−1, n_ours+1, heart−1.
    _, _, n_gain, n_ours = _tRS(scalar_map, tag_map, team_side, remembered=_terr_ctx.get('remembered'))
    if n_gain < 1:
        return 0.0                                    # nada ganable de verdad (junction ya nuestra): sin cadena (gate c)
    def_terr_now = _wr * min(1.0, n_gain / _tt) ** 2
    def_terr_aft = _wr * min(1.0, (n_gain - 1) / _tt) ** 2
    bono_now = _ws * min(1.0, n_ours / _to)
    bono_aft = _ws * min(1.0, (n_ours + 1) / _to)
    hd_now, hd_aft = _hdef(mis_hearts), _hdef(mis_hearts - 1)
    dposR = (def_terr_now - def_terr_aft) - (hd_aft - hd_now)   # align: −déficit_terr (sube posR) +déficit_heart (baja)
    dposS = bono_aft - bono_now
    posR = (s_curr.pR - s_curr.nR) + dposR
    posS = (s_curr.pS - s_curr.nS) + dposS
    s_aft = _St(pF=s_curr.pF, nF=s_curr.nF,
                pR=max(0.0, posR), nR=max(0.0, -posR),
                pS=max(0.0, posS), nS=max(0.0, -posS))
    delta_d = opponent_distance(s_curr, _ACTIVE_CFG) - opponent_distance(s_aft, _ACTIVE_CFG)
    if delta_d <= 0.0:
        return 0.0                                    # el align no baja d (heart caro > territorio): sin inversión
    return conf * (CHAIN_GAMMA ** dist_L1) * delta_d


def _set_agent_elements_zero(tokens: list, elem_fids) -> list:
    """Pone a 0 el inventario del agente de TODOS los elementos dados (depósito imaginado: entrega al hub)."""
    zero = set()
    for f in (elem_fids or (FID_INV_CARBON,)):
        zero.add(int(f)); zero.add(int(f) + 1)
    return [(t[0], t[1], 0) if (int(t[0]) == AGENT_LOC and int(t[1]) in zero) else (t[0], t[1], t[2])
            for t in tokens]


def predict_states(
    tokens: list,
    scalar_map: dict,
    tag_map: dict,
    action_names: list[str],
    team_side: str,
    mem=None,
    trans_ctx=None,
    world_step: int = 0,
    act_credit: float = 0.0,
) -> dict[str, object]:
    """For each action, build predicted tokens and appraise. Returns per-action info.

    Blocked moves (destination cell occupied by an agent) use noop prediction.
    When mem is provided (USE_MEMORY=True), ghost forces at the predicted position
    are added to each predicted state before computing d.
    When trans_ctx is provided (GEMV_TRANSITION=1), the transition model (Fase 3b)
    rewrites the predicted inventory tokens (mecánica del juego) before appraise.
    """
    _trans = None
    if trans_ctx is not None:
        from planificador.transicion_v1 import apply_transition as _trans

    # Pre-compute noop prediction once (used as fallback for blocked moves)
    noop_tokens = [t for t in tokens if int(t[0]) != PADDING_LOC]
    if _trans is not None:
        noop_tokens = _trans(noop_tokens, "noop", world_step, 1, trans_ctx)
    s_noop = appraise(noop_tokens, team_side, s_scale=S_SCALE, act_credit=act_credit)
    if mem is not None:
        ghost_noop = mem.ghost_forces_for_position(*mem.agent_world, mem._step + 1)
        s_noop = apply_ghost(s_noop, ghost_noop)
    d_noop = opponent_distance(s_noop, _ACTIVE_CFG)
    noop_pred = {
        "d": round(d_noop, 5),
        "pos_F": round(s_noop.pos_F, 4), "pos_R": round(s_noop.pos_R, 4),
        "pos_S": round(s_noop.pos_S, 4),
        "nF": round(s_noop.nF, 4), "nR": round(s_noop.nR, 4),
        "nS": round(s_noop.nS, 4), "blocked": False,
    }

    preds: dict[str, dict] = {}
    for action in action_names:
        if action == "noop":
            preds[action] = noop_pred
            continue
        if action not in ACTION_DELTAS:
            preds[action] = noop_pred
            continue

        if _dest_is_blocked(tag_map, action):
            blocked_pred = dict(noop_pred)
            blocked_pred["blocked"] = True
            preds[action] = blocked_pred
            continue

        # BUMP→ALINEAR / EQUIPAR ALIGNER (Eslabón 4): dest es junction o gear station del aligner ⇒
        # la estación/junction bloquea el move; station_bump_effect aplica el efecto (align/equip). d baja sola.
        if _MARCADOR and _trans is not None:
            _dm = ACTION_DELTAS.get(action, (0, 0))
            _destm = (AGENT_ROW + _dm[0]) * EGOCENTRIC_COLS + (AGENT_COL + _dm[1])
            _dtags = tag_map.get(_destm, set())
            if TAG_TYPE_JUNCTION in _dtags or TAG_TYPE_ALIGNER in _dtags:
                from planificador.transicion_v1 import station_bump_effect as _sbe
                _mtok = [t for t in tokens if int(t[0]) != PADDING_LOC]
                _bumped, _kind = _sbe(_mtok, action, trans_ctx)
                if _bumped is not None:
                    _mtok = _trans(_bumped, "noop", world_step, 1, trans_ctx)
                    s_m = appraise(_mtok, team_side, s_scale=S_SCALE, act_credit=act_credit)
                    if mem is not None:
                        s_m = apply_ghost(s_m, mem.ghost_forces_for_position(*mem.agent_world, mem._step + 1))
                    d_m = opponent_distance(s_m, _ACTIVE_CFG)
                    preds[action] = {"d": round(d_m, 5), "pos_F": round(s_m.pos_F, 4),
                        "pos_R": round(s_m.pos_R, 4), "pos_S": round(s_m.pos_S, 4),
                        "nF": round(s_m.nF, 4), "nR": round(s_m.nR, 4), "nS": round(s_m.nS, 4),
                        "blocked": False, "marcador": _kind}
                    continue

        # BUMP→COSECHA (extensión de cobertura 3b, gated por trans_ctx.model_extract): el destino es un
        # extractor ⇒ la estación bloquea el move, el agente se queda y cosecha (held+δ). El held+ propaga
        # a appraise (w_mat baja, cobertura β del canal social sube) ⇒ d baja sola. Sin valor nuevo.
        ext_tag = (_dest_extractor_tag(tag_map, action)
                   if (_trans is not None and getattr(trans_ctx, "model_extract", False)) else None)
        if ext_tag is not None:
            from planificador.transicion_v1 import harvest_bump as _harvest
            bump_tokens = [t for t in tokens if int(t[0]) != PADDING_LOC]  # agente NO se mueve
            bump_tokens = _trans(bump_tokens, "noop", world_step, 1, trans_ctx)  # energía/HP en sitio
            bump_tokens = _harvest(bump_tokens, ext_tag, trans_ctx)              # +δ material
            s_bump = appraise(bump_tokens, team_side, s_scale=S_SCALE, act_credit=act_credit)
            if mem is not None:
                ghost_b = mem.ghost_forces_for_position(*mem.agent_world, mem._step + 1)  # posición actual
                s_bump = apply_ghost(s_bump, ghost_b)
            d_bump = opponent_distance(s_bump, _ACTIVE_CFG)
            preds[action] = {
                "d": round(d_bump, 5),
                "pos_F": round(s_bump.pos_F, 4), "pos_R": round(s_bump.pos_R, 4),
                "pos_S": round(s_bump.pos_S, 4),
                "nF": round(s_bump.nF, 4), "nR": round(s_bump.nR, 4),
                "nS": round(s_bump.nS, 4), "blocked": False, "bump": True,
            }
            continue

        # BUMP→DEPÓSITO (cobertura v2_hybrid): el destino es el hub PROPIO y el agente lleva carbon ⇒ el
        # hub bloquea el move, el agente se queda y DEPOSITA (held→0), y el ACTO salda A: act_credit += A_UNIT.
        # Así el planificador IMAGINA el pago del acto (≤H desde el extractor: bump + 3 oeste = depósito).
        _elem_fids = getattr(trans_ctx, "element_inv_fids", None) or (FID_INV_CARBON,)
        if (_COVERAGE == "v2_hybrid" and _dest_is_own_hub(tag_map, action, team_side)
                and any(get_multipart(scalar_map, AGENT_LOC, f) > 0 for f in _elem_fids)):
            dep_tokens = [t for t in tokens if int(t[0]) != PADDING_LOC]  # agente NO avanza (hub bloquea)
            if _trans is not None:
                dep_tokens = _trans(dep_tokens, "noop", world_step, 1, trans_ctx)
            # D1 — capturar carga entregada por elemento ANTES de vaciar (para subir team_held)
            _delivered = {int(f): get_multipart(parse_tokens(dep_tokens)[0], AGENT_LOC, f) for f in _elem_fids}
            dep_tokens = _set_agent_elements_zero(dep_tokens, _elem_fids)  # entrega TODOS los elementos al hub
            # D1 — el depósito SUBE team_held (queryDeposit hub.py) ⇒ baja el déficit SHELF derivado
            _i2t = getattr(trans_ctx, "inv_to_team", None) or {}
            if _i2t:
                _sm_dep = parse_tokens(dep_tokens)[0]
                for _f, _amt in _delivered.items():
                    _tf = _i2t.get(_f)
                    if _tf is not None and _amt > 0:
                        _cur = get_scalar(_sm_dep, GLOBAL_LOC, _tf)
                        dep_tokens = [t for t in dep_tokens
                                      if not (int(t[0]) == GLOBAL_LOC and int(t[1]) == _tf)]
                        dep_tokens.append((GLOBAL_LOC, _tf, _cur + _amt))
            s_dep = appraise(dep_tokens, team_side, s_scale=S_SCALE, act_credit=act_credit + _A_UNIT)
            if mem is not None:
                ghost_d = mem.ghost_forces_for_position(*mem.agent_world, mem._step + 1)
                s_dep = apply_ghost(s_dep, ghost_d)
            d_dep = opponent_distance(s_dep, _ACTIVE_CFG)
            preds[action] = {
                "d": round(d_dep, 5),
                "pos_F": round(s_dep.pos_F, 4), "pos_R": round(s_dep.pos_R, 4),
                "pos_S": round(s_dep.pos_S, 4),
                "nF": round(s_dep.nF, 4), "nR": round(s_dep.nR, 4),
                "nS": round(s_dep.nS, 4), "blocked": False, "deposit": True,
            }
            continue
        # BUMP→MAKE (Eslabón 1): dest hub propio, carga de elementos = 0, pantry ≥ recipe/elem →
        # el agente fabrica un heart (inv:heart+1, team_held−7/elem). Fiel al firstMatch (make tras
        # deposit; con carga=0 deposit no casa). El heart+ baja el déficit de hearts ⇒ d baja sola.
        if (_HEARTS and trans_ctx is not None and _COVERAGE == "v2_hybrid"
                and _dest_is_own_hub(tag_map, action, team_side)
                and not any(get_multipart(scalar_map, AGENT_LOC, f) > 0 for f in _elem_fids)):
            from planificador.transicion_v1 import make_heart_bump as _make
            mk_tokens = [t for t in tokens if int(t[0]) != PADDING_LOC]  # agente NO avanza (hub bloquea)
            if _trans is not None:
                mk_tokens = _trans(mk_tokens, "noop", world_step, 1, trans_ctx)
            made = _make(mk_tokens, trans_ctx)
            if made is not None:
                s_mk = appraise(made, team_side, s_scale=S_SCALE, act_credit=act_credit)
                if mem is not None:
                    ghost_m = mem.ghost_forces_for_position(*mem.agent_world, mem._step + 1)
                    s_mk = apply_ghost(s_mk, ghost_m)
                d_mk = opponent_distance(s_mk, _ACTIVE_CFG)
                preds[action] = {
                    "d": round(d_mk, 5),
                    "pos_F": round(s_mk.pos_F, 4), "pos_R": round(s_mk.pos_R, 4),
                    "pos_S": round(s_mk.pos_S, 4),
                    "nF": round(s_mk.nF, 4), "nR": round(s_mk.nR, 4),
                    "nS": round(s_mk.nS, 4), "blocked": False, "make": True,
                }
                continue
        # hub propio sin carga: bloqueo puro (fidelidad — el hub impide avanzar aunque no haya depósito)
        if _COVERAGE == "v2_hybrid" and _dest_is_own_hub(tag_map, action, team_side):
            preds[action] = dict(noop_pred)
            continue

        # RUTA_MEM (A) VETO DE SÓLIDO CONOCIDO (la red): tras TODOS los bump-de-uso (align/equip/cosecha/
        # depósito/make, ya resueltos con `continue` arriba), un move cuyo destino es un sólido CONOCIDO
        # (muro/estación no usada) se trata como bloqueado (= noop): ningún move elegido empuja un sólido.
        if _RUTA_MEM:
            _vd = ACTION_DELTAS[action]
            _vdest = (AGENT_ROW + _vd[0]) * EGOCENTRIC_COLS + (AGENT_COL + _vd[1])
            _blocked_solid = bool(set(tag_map.get(_vdest, set())) & _SOLID_TYPES)   # sólido PERCIBIDO (ventana)
            _rem_block = False
            # WALL_MEM: misma fuente extendida — un sólido RECORDADO (fuera de ventana) también veta el move.
            if (not _blocked_solid and _WALL_MEM and mem is not None and getattr(mem, "wall_mem", False)):
                _aw = getattr(mem, "_agent_world", None)
                if _aw is not None and (_aw[0] + _vd[0], _aw[1] + _vd[1]) in getattr(mem, "_walls", ()):
                    _blocked_solid = True; _rem_block = True
            if _blocked_solid:
                _vpred = dict(noop_pred)
                _vpred["blocked"] = True
                if _rem_block:
                    _vpred["blocked_remembered"] = True   # bloqueado por muro RECORDADO no percibido (métrica)
                preds[action] = _vpred
                continue

        drow, dcol = ACTION_DELTAS[action]
        pred_tokens = _shift_tokens(tokens, scalar_map, drow, dcol, MOVE_ENERGY_COST)
        if _trans is not None:
            pred_tokens = _trans(pred_tokens, action, world_step, 1, trans_ctx)

        s_pred = appraise(pred_tokens, team_side, s_scale=S_SCALE, act_credit=act_credit)
        if mem is not None:
            ar, ac = mem.agent_world
            ghost_pred = mem.ghost_forces_for_position(ar + drow, ac + dcol, mem._step + 1)
            s_pred = apply_ghost(s_pred, ghost_pred)
        d_pred = opponent_distance(s_pred, _ACTIVE_CFG)
        preds[action] = {
            "d": round(d_pred, 5),
            "pos_F": round(s_pred.pos_F, 4),
            "pos_R": round(s_pred.pos_R, 4),
            "pos_S": round(s_pred.pos_S, 4),
            "nF": round(s_pred.nF, 4),
            "nR": round(s_pred.nR, 4),
            "nS": round(s_pred.nS, 4),
            "blocked": False,
        }
    return preds


# ── Utility: find energy sources in window ───────────────────────────────────

FID_INV_SOLAR: int = 34

def _energy_sources(scalar_map: dict) -> list[dict]:
    """Cells with solar energy or minerals visible in window (excl. agent)."""
    sources = []
    resource_fids = {FID_INV_SOLAR}
    for (loc, fid), val in scalar_map.items():
        if loc in (AGENT_LOC, GLOBAL_LOC, PADDING_LOC):
            continue
        if fid in resource_fids and val > 0:
            row, col = divmod(loc, EGOCENTRIC_COLS)
            if 0 <= row <= 12 and 0 <= col <= 12:
                dist = math.sqrt((row - AGENT_ROW)**2 + (col - AGENT_COL)**2)
                sources.append({"loc": loc, "fid": fid, "val": val, "dist": round(dist, 2)})
    return sources


def _hub_visibility(tag_map: dict, team_side: str) -> dict:
    """Read-only: own hubs visible in the 13×13 window (presence + distance).

    INSTRUMENTACIÓN — NO afecta a la decisión. Se añade al log por-tick para poder
    auditar la visibilidad del hub y la bisagra S/F (la auditoría 2026-07-02 la marcó
    NO AUDITABLE porque no se logueaba). Escanea tag_map igual que la memoria/appraisal,
    sin tocar el State ni las predicciones.
    """
    own_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    dists: list[float] = []
    for loc, tags in tag_map.items():
        if TAG_TYPE_HUB in tags and own_tag in tags:
            row, col = divmod(loc, EGOCENTRIC_COLS)
            if 0 <= row <= 12 and 0 <= col <= 12:
                dists.append(math.sqrt((row - AGENT_ROW) ** 2 + (col - AGENT_COL) ** 2))
    return {
        "present": len(dists) > 0,
        "n": len(dists),
        "min_dist": round(min(dists), 3) if dists else None,
    }


def _element_inv_fids() -> tuple:
    """fid_p0 de TODOS los elementos (saneados, de EXTRACTOR_TYPE_INFO). Para el depósito generalizado 1b."""
    import appraisal.appraisal_v3 as _av3
    if hasattr(_av3, "EXTRACTOR_TYPE_INFO") and _av3.EXTRACTOR_TYPE_INFO:
        return tuple(sorted(set(inv for (inv, _p) in _av3.EXTRACTOR_TYPE_INFO.values())))
    return (FID_INV_CARBON,)


def _hub_get_ok(world_step: int) -> bool:
    """V-A: modelar el get optimista SI marcador ∧ el hub NO ha fallado recientemente (candado
    anti-peregrinación, decae con la vida media estándar). Espejo del candado del atractor."""
    if not _MARCADOR:
        return False
    fail = _terr_ctx.get('hub_fail_step', -1)
    if fail < 0:
        return True
    return _math.exp(-_PANTRY_DECAY_LAMBDA * (world_step - fail)) <= 0.5   # recuperado tras la vida media


def _build_trans_ctx(team_side: str, world_step: int = 0):
    """Contexto del modelo de transición (Fase 3b + extensión bump→cosecha). Se construye si
    GEMV_TRANSITION o GEMV_TRANSITION_EXTRACT; cada cobertura la activa su sub-interruptor."""
    from planificador.transicion_v1 import TransCtx
    import appraisal.appraisal_v3 as _av3
    own = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
    # tag_type de extractor → fid_p0 del inventario del material (de EXTRACTOR_TYPE_INFO, saneado).
    ext_inv = {}
    if hasattr(_av3, "EXTRACTOR_TYPE_INFO"):
        for tag, (inv_fid, _proto) in _av3.EXTRACTOR_TYPE_INFO.items():
            ext_inv[int(tag)] = inv_fid
    # depósito generalizado (competidor 1b): fid_p0 de TODOS los elementos (de EXTRACTOR_TYPE_INFO, saneado).
    elem_fids = tuple(sorted(set(ext_inv.values()))) if ext_inv else (FID_INV_CARBON,)
    # D1 — mapa inv_fid_p0 → team_fid_p0 (de _MAT_FIDS de v4, saneado) para que el depósito suba team_held.
    inv_to_team = {}
    try:
        from appraisal.appraisal_v4 import _MAT_FIDS as _MF
        inv_to_team = {int(inv): int(team) for (_proto, team, inv) in _MF.values()}
    except Exception:
        inv_to_team = {}
    return TransCtx(
        parse_tokens=parse_tokens, agent_loc=AGENT_LOC,
        fid_energy_p0=FID_INV_ENERGY, fid_hp_p0=FID_INV_HP,
        egocentric_cols=EGOCENTRIC_COLS, agent_row=AGENT_ROW, agent_col=AGENT_COL,
        tag_type_hub=TAG_TYPE_HUB, own_team_tag=own,
        extractor_tags=EXTRACTOR_TAGS, action_deltas=ACTION_DELTAS,
        model_energy=_TRANSITION_ON, model_extract=_TRANS_EXTRACT, extractor_inv_fid=ext_inv,
        model_deposit=(_COVERAGE == "v2_hybrid"), fid_carbon=FID_INV_CARBON,
        element_inv_fids=elem_fids, fid_acts_done=_FID_ACTS_DONE,
        cargo_cap=(_CARGO_CAP if _CARGO_CAP > 0 else None),       # D2
        team_loc=GLOBAL_LOC, inv_to_team=inv_to_team,             # D1
        model_hearts=_HEARTS, fid_inv_heart=FID_INV_HEART,        # Eslabón 1
        model_marcador=_MARCADOR, fid_inv_aligner=FID_INV_ALIGNER,  # Eslabón 4
        hub_get_ok=_hub_get_ok(world_step),                          # V-A: get optimista gateado por candado
        tag_type_aligner_station=TAG_TYPE_ALIGNER, tag_type_junction=TAG_TYPE_JUNCTION,
        tag_net_own=(TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS),
        aligner_cost=_aligner_cost(), fid_tag=FID_TAG,
        equip_gated=(_EQUIP_GATED and not _EQUIP_CUSHION),           # FUSIÓN: la guarda de colchón (continua) subsume el binario
    )


def _aligner_cost():
    """{team_fid: coste} del gear aligner (carbon3, oxygen1, germanium1, silicon1) — machina_1.py:85."""
    try:
        from appraisal.appraisal_v4 import _MAT_FIDS as _MF
        by_name = {"carbon": 3, "oxygen": 1, "germanium": 1, "silicon": 1}
        return {int(team): by_name.get(name, 1) for name, (_p, team, _i) in _MF.items()}
    except Exception:
        return {}


# ── Decision ─────────────────────────────────────────────────────────────────

def choose_action(
    tokens: list,
    action_names: list[str],
    team_side: str,
    mem=None,
    world_step: int = 0,
    act_credit: float = 0.0,
    slot: int = -1,
) -> tuple[str, dict]:
    """Choose action minimizing d_pred. Returns (action_name, debug_dict).

    Tie-breaking: first in action_names order (stable, deterministic).
    When mem is provided (USE_MEMORY=True): observe(), then apply ghost forces
    to both current state and all predicted states.
    When GEMV_TRANSITION=1 (Fase 3b): el modelo de transición reescribe el inventario
    predicho antes de appraise, tanto en preds como en el planificador.
    """
    scalar_map, tag_map = parse_tokens(tokens)
    n_soplo = 0                                    # PREGONERO: nº hechos ajenos inyectados este tick (siempre definido)
    _deriva_on = False                             # DERIVA: ¿el paseo del próspero activo este tick? (siempre definido)
    _forage_on = False                             # FORRAJEO: ¿la fuerza f+ de exploración tomó el canal GAIN? (siempre def.)
    trans_ctx = (_build_trans_ctx(team_side, world_step)
                 if (_TRANSITION_ON or _TRANS_EXTRACT or _COVERAGE == "v2_hybrid") else None)

    # ── PANTRY_MEM: actualizar contexto antes de cualquier appraise ──────────
    if _PANTRY_MEM and _GEMV_SHELF:
        own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
        if _shelf_hub_vis(scalar_map, tag_map, own_team_tag):
            # percepción manda: recuerdo fresco (edad 0), corrige valores al volver
            _pantry_ctx['vals'] = {fid: get_scalar(scalar_map, GLOBAL_LOC, fid)
                                   for fid in _SHELF_TEAM_FIDS}
            _pantry_ctx['step'] = world_step
            _pantry_ctx['age'] = 0.0
        elif _pantry_ctx['vals'] is not None:
            age = world_step - _pantry_ctx['step']
            _pantry_ctx['age'] = age
            if not _PANTRY_DECAY and age > PANTRY_MEM_MAX_AGE:
                _pantry_ctx['vals'] = None  # v5: acantilado a 500. v6 (_PANTRY_DECAY): nunca expira, decae.

    # Eslabón 4 — recuerdo del hub-sin-fruto (candado anti-peregrinación): si el agente estuvo
    # adyacente al hub y su inv:heart NO subió, el hub no dio heart → registra el fallo (decae estándar).
    if _MARCADOR:
        own_team_tag = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
        _mh = get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART)
        _hub_adj = any(TAG_TYPE_HUB in tg and own_team_tag in tg
                       and abs(loc // EGOCENTRIC_COLS - AGENT_ROW) + abs(loc % EGOCENTRIC_COLS - AGENT_COL) <= 1
                       for loc, tg in tag_map.items())
        if _terr_ctx.get('prev_hub_adj') and _mh <= _terr_ctx.get('prev_hearts', 0):
            _terr_ctx['hub_fail_step'] = world_step        # estuvo pegado y no ganó heart → fracaso
        _terr_ctx['prev_hearts'] = _mh
        _terr_ctx['prev_hub_adj'] = _hub_adj
        # recordado: junctions FUERA de ventana (percepción manda: las en-ventana ya cuentan por tag).
        _rem = []
        _rumbo_inject = []   # ESLABÓN RUMBO: junctions ganables recordadas → tokens fantasma para el rollout
        _rumbo_ready = (_RUMBO and get_multipart(scalar_map, AGENT_LOC, FID_INV_ALIGNER) >= 1
                        and get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART) >= 1)
        if mem is not None and hasattr(mem, "_entries"):
            _ar, _ac = getattr(mem, "_agent_world", (0, 0))
            for (wr, wc, cls) in mem._entries:
                if cls in ("junction_gray", "junction_rival", "junction_own"):
                    # "percibida → skip (cuenta vía tag)": con PERSIST_GANABLE usa el DISCO real (dr²+dc²≤37) —
                    # así una ganable persistida EN-CUADRADO pero FUERA-DEL-DISCO (no percibida) NO se descarta
                    # por la grieta (ni vía tag ni en _rem); se cuenta como recordada → n_gain la ve → la gain
                    # no se apaga (el relevo). OFF (persist_ganable) ≡ cuadrado C6 bit-exact. (deuda disco-vs-cuadrado)
                    _dr, _dc = wr - _ar, wc - _ac
                    _perceived = ((_dr * _dr + _dc * _dc <= PERCEPTION_R2) if _PERSIST_GANABLE
                                  else (abs(_dr) <= 6 and abs(_dc) <= 6))
                    if _perceived:
                        continue                            # percibida de verdad → cuenta vía tag (no doble-contar)
                    # RUMBO — CONTINUIDAD: la junction GANABLE recordada, dentro del grid ego y con el agente
                    # equipado, entra como token fantasma → el rollout la puede bump-alinear igual que una
                    # percibida (sin escalón de valor en la frontera de lo visible). Se excluye del conteo _rem
                    # (se cuenta ya vía tag). Fuera del grid o sin equipo → conteo escalar como antes.
                    _vr, _vc = wr - _ar, wc - _ac
                    if (_rumbo_ready and cls in ("junction_gray", "junction_rival")
                            and -AGENT_ROW <= _vr <= EGOCENTRIC_ROWS - 1 - AGENT_ROW
                            and -AGENT_COL <= _vc <= EGOCENTRIC_COLS - 1 - AGENT_COL):
                        _loc = (_vr + AGENT_ROW) * EGOCENTRIC_COLS + (_vc + AGENT_COL)
                        _rumbo_inject.append((_loc, FID_TAG, TAG_TYPE_JUNCTION))
                        continue                            # inyectada como token → no doble-contar en _rem
                    _rem.append("ours" if cls == "junction_own" else "gain")
        _terr_ctx['remembered'] = _rem or None
        if _rumbo_inject:
            tokens = list(tokens) + _rumbo_inject           # el rollout (y el appraise) la ven como percibida

    appr_debug = None
    if mem is not None:
        s_curr, appr_debug = appraise_with_debug(tokens, team_side, s_scale=S_SCALE)
        if _APPRAISAL == "4":
            s_curr = appraise(tokens, team_side, s_scale=S_SCALE, act_credit=act_credit)  # v4 + cobertura
        appr_debug["d"] = opponent_distance(s_curr, _ACTIVE_CFG)  # paisaje: 6 fuerzas + d
        # OPCIÓN A (ii) — FIJAR el marco de memoria a la posición ABSOLUTA leída (antes de observe, para que
        # observe/_present/prior usen el marco verdadero). ODOMETRÍA = respaldo. OFF ⇒ dead-reckoning intacto.
        _ap = _abs_pos(scalar_map) if (_ABS_FRAME or os.environ.get("GEMV_ABS_DBG")
                                       or os.environ.get("GEMV_DISTIL_DBG")) else None
        if os.environ.get("GEMV_ABS_DBG") and hasattr(mem, "_agent_world"):
            _log(f"ABS_DBG step={world_step} abs_pos={_ap} mem_agent_world={getattr(mem,'_agent_world',None)}")
        # DESTILADO EN FRAME DE OBSERVACIÓN (regla: la memoria solo consume lo que los ojos ven): posición
        # de cada fijo PERCIBIDO = agente_lp + celda ego. NO usa replay.location (prohibido para la criatura).
        if os.environ.get("GEMV_DISTIL_DBG") and _ap is not None:
            _own = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
            _ftypes = {"aligner": TAG_TYPE_ALIGNER, "scrambler": 17, "miner": 14, "scout": 16}
            for _loc, _tags in tag_map.items():
                _er = _loc // EGOCENTRIC_COLS - AGENT_ROW; _ec = _loc % EGOCENTRIC_COLS - AGENT_COL
                _cheb = max(abs(_er), abs(_ec))
                for _nm, _tid in _ftypes.items():
                    if _tid in _tags:
                        _log(f"DISTIL step={world_step} type={_nm} abs_lp=({_ap[0]+_er},{_ap[1]+_ec}) ego_cheb={_cheb}")
                if TAG_TYPE_HUB in _tags and _own in _tags:
                    _log(f"DISTIL step={world_step} type=hub abs_lp=({_ap[0]+_er},{_ap[1]+_ec}) ego_cheb={_cheb}")
        if _ABS_FRAME and _ap is not None and hasattr(mem, "_agent_world"):
            mem._agent_world = _ap
        mem.observe(appr_debug, scalar_map, tag_map, team_side)
        # ESLABÓN DESMENTIDO — la memoria de rechazo. D1 DETECCIÓN: el move elegido el tick pasado + agent_world
        # (=_abs_pos(lp:*), ABSOLUTO; la policy no parsea action_success del obs) SIN cambio = el juego rechazó
        # el move (el "no" del mundo MEDIDO, no inferido). D2 REGISTRO: la celda destino se marca OCUPADA-AHORA
        # con TTL corto (evidencia DINÁMICA, fungible; NUNCA a la memoria de fijos), RENOVADA si el rechazo se
        # repite; expira → vuelve a ser candidata (el pasillo no queda prohibido porque un día hubo alguien).
        if _DESMENTIDO and hasattr(mem, "_agent_world"):
            _rej_map = getattr(mem, "_rejected", None)
            if _rej_map is None:
                _rej_map = mem._rejected = {}
            _awd = tuple(mem._agent_world)
            _la = getattr(mem, "_desm_last_action", None)
            _lp = getattr(mem, "_desm_last_pos", None)
            if _la in ACTION_DELTAS and _lp is not None and _awd == tuple(_lp):
                # EXCLUIR EL BUMP-DE-USO: el no-avance NO es un muro si el destino es un objeto USABLE con
                # transición modelada y precondición VIVA (alinear junction ganable con aligner+heart, equipar
                # gear, depositar/fabricar en hub con carga, cosechar). Fuente única = la MISMA transición del
                # planner (station_bump_effect), sin listas paralelas. Si el bump SÍ tiene efecto → gesto de
                # uso, no muro → no marcar. Si es "*_blocked"/full (tienda vacía, sin precondición) o None
                # (obstáculo real) → SÍ marca (el aporreador de tiendas vacías no vuelve; el muro sigue muro).
                _use_bump = False
                if trans_ctx is not None:
                    from planificador.transicion_v1 import station_bump_effect as _sbe_desm
                    _, _bk = _sbe_desm(tokens, _la, trans_ctx)
                    _use_bump = _bk in ("align", "equip_aligner", "deposit", "make", "harvest")
                if not _use_bump:
                    _ddr, _ddc = ACTION_DELTAS[_la]
                    _rej_map[(_lp[0] + _ddr, _lp[1] + _ddc)] = world_step + DESMENTIDO_TTL   # marca / RENUEVA
            mem._rejected = {c: e for c, e in _rej_map.items() if e > world_step}         # decaimiento
        # PREGONERO v1 — la memoria compartida. Tras observe (mis ojos ya mandaron en mi ventana):
        #  (1) actualizo mis sightings de PRIMERA MANO (junctions percibidas ahora, coords absolutas) para publicar;
        #  (2) CONSUMO los tablones ajenos → inyecto sus junctions FUERA de mi ventana con confianza menor;
        #  (3) PUBLICO mi tablón. OFF ⇒ los tres son no-op (bit-exact).
        n_soplo = 0
        if _PREGONERO and _MARCADOR and hasattr(mem, "_agent_world"):
            _ar, _ac = mem._agent_world
            _own_net = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
            _riv_net = TAG_NET_CLIPS if team_side == "cogs" else TAG_NET_COGS
            from memoria.memoria_v1 import _EXTRACTOR_CLS as _ECLS_PUB
            for _loc, _tg in tag_map.items():
                _wr = _ar + (_loc // EGOCENTRIC_COLS - AGENT_ROW)
                _wc = _ac + (_loc % EGOCENTRIC_COLS - AGENT_COL)
                if TAG_TYPE_JUNCTION in _tg:
                    _cls = ("junction_own" if _own_net in _tg else
                            "junction_rival" if _riv_net in _tg else "junction_gray")
                    _pregonero_seen[(_wr, _wc)] = (_cls, world_step)     # 1ª mano (anti-eco)
                else:
                    # PUENTE: publicar EXTRACTORES vistos (misma clase que la memoria/motor usan)
                    for _tt in (set(_tg) & EXTRACTOR_TAGS):
                        _ecls = _ECLS_PUB.get(_tt)
                        if _ecls:
                            _pregonero_seen[(_wr, _wc)] = (_ecls, world_step)
            n_soplo = _pregonero_consume(mem, slot, world_step)      # (2) oír a los compañeros
            _pregonero_publish(slot)                                 # (3) pregonar lo mío
        ghost_curr = mem.ghost_forces()
        s_curr = apply_ghost(s_curr, ghost_curr)
        # Eslabón 3 — marcar la ventana como rastreada (D1: verla basta). _agent_world ya actualizado.
        if (_EXPLORE or _DERIVA or _FORAGE) and _rastreo is not None and hasattr(mem, "_agent_world"):
            _ar, _ac = mem._agent_world
            _rastreo.mark_window(_ar, _ac, _WINDOW_RADIUS, world_step)
        # Córtex C1 — ENTREGA del mapa de nacimiento (una vez, anclado al hub percibido). El prior son
        # entradas de memoria pre-pobladas con conf 0.5 (last_seen = step − HALFLIFE); percepción manda.
        if (_CORTEX_PRIOR and not _cortex_ctx['loaded'] and _cortex_ctx['atlas']
                and hasattr(mem, "_agent_world") and hasattr(mem, "_record")):
            _own = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
            _hub_ego = next((loc for loc, tg in tag_map.items()
                             if TAG_TYPE_HUB in tg and _own in tg), None)
            _atlas_hub = next((e for e in _cortex_ctx['atlas'] if e['type'] == 'hub'), None)
            if _hub_ego is not None and _atlas_hub is not None:
                _ar, _ac = mem._agent_world
                _hr = _ar + (_hub_ego // EGOCENTRIC_COLS - AGENT_ROW)   # hub en marco-memoria
                _hc = _ac + (_hub_ego % EGOCENTRIC_COLS - AGENT_COL)
                _ahr, _ahc = _atlas_hub['pos']
                _n = 0
                for e in _cortex_ctx['atlas']:
                    if e.get('cls') in (None, 'hub'):
                        continue                                       # hub: solo ancla (ya percibido)
                    wr = _hr + (e['pos'][0] - _ahr)                     # ancla: hub_memframe + (obj−hub)
                    wc = _hc + (e['pos'][1] - _ahc)
                    mem._record(wr, wc, e['cls'], 1.0, world_step - _CORTEX_HALFLIFE)  # conf 0.5, amp nominal
                    _n += 1
                _cortex_ctx['loaded'] = True
                _log(f"[GEMV] cortex prior cargado: {_n} entradas (gear stations) ancladas al hub percibido")
        if os.environ.get("GEMV_GEAR_DBG") and hasattr(mem, "_entries"):
            _ngear = sum(1 for (_, _, cls) in mem._entries if cls == "gear_aligner")
            _perc = any(TAG_TYPE_ALIGNER in t for t in tag_map.values())
            _log(f"GEAR_DBG step={world_step} n_gear_mem={_ngear} gear_perceived={_perc} n_entries={len(mem._entries)}")
    else:
        s_curr = appraise(tokens, team_side, s_scale=S_SCALE, act_credit=act_credit)

    d_curr = opponent_distance(s_curr, _ACTIVE_CFG)

    # ESLABÓN DESMENTIDO — INYECCIÓN de las celdas OCUPADA-AHORA (s_curr/d_curr ya calculados: la marca solo
    # afecta la PREVISIÓN). Token type:agent en la celda rechazada → dest_is_blocked la trata como ocupada (el
    # rollout NO avanza ahí, como al percibir a otro agente) Y la geodesia la rodea (_desm_solid). Las dos piezas
    # que Manel pidió (dest_is_blocked Y geodesia). COMMIT sin tocar: su interrupción (a) aborta el plan, el
    # re-plan VE la celda ocupada y elige el rodeo. OFF (sin rechazos) ⇒ _desm_solid=None, tokens/tag_map igual.
    _desm_solid = None
    if _DESMENTIDO and getattr(mem, "_rejected", None) and hasattr(mem, "_agent_world"):
        _ar, _ac = mem._agent_world
        _inj = []; _es = set()
        for (wr, wc) in mem._rejected:
            _er = wr - _ar; _ec = wc - _ac
            if 0 <= AGENT_ROW + _er < EGOCENTRIC_ROWS and 0 <= AGENT_COL + _ec < EGOCENTRIC_COLS:
                _loc = (AGENT_ROW + _er) * EGOCENTRIC_COLS + (AGENT_COL + _ec)
                _inj.append((_loc, FID_TAG, TAG_TYPE_AGENT)); _es.add((_er, _ec))
        if _inj:
            tokens = list(tokens) + _inj
            tag_map = {k: set(v) for k, v in tag_map.items()}
            for (_loc, _f, _t) in _inj:
                tag_map.setdefault(_loc, set()).add(_t)
            _desm_solid = _es

    preds = predict_states(tokens, scalar_map, tag_map, action_names, team_side, mem=mem,
                           trans_ctx=trans_ctx, world_step=world_step, act_credit=act_credit)

    plan_dbg = None
    if _HORIZON <= 1 and not _PLAN_FORCE:
        # H=1: greedy sobre preds (con transición ya aplicada si está ON).
        best_action = min(action_names, key=lambda a: preds.get(a, {}).get("d", float("inf")))
    else:
        # H>=2: horizonte rodante. Reutiliza las primitivas de predicción (ver spec §7/§8).
        from planificador.planificador_v1 import plan_terminal, select, PlanCtx
        if _TIEBREAK:
            from planificador.planificador_v1 import select_tiebreak
        terr_map = None
        if _TERR_FS_MAP:
            from planificador.mapa_territorial import reconstruct_map
            _fid_terr = {FID_TERR_NORTH: "N", FID_TERR_SOUTH: "S",
                         FID_TERR_EAST: "E", FID_TERR_WEST: "W"}
            _here = scalar_map.get((GLOBAL_LOC, FID_TERRITORY_HERE), 0)
            terr_map = reconstruct_map(scalar_map, _here, _fid_terr, GLOBAL_LOC, PADDING_LOC)
        ctx = PlanCtx(
            shift_tokens=_shift_tokens, dest_is_blocked=_dest_is_blocked,
            parse_tokens=parse_tokens, appraise=appraise, apply_ghost=apply_ghost,
            opponent_distance=opponent_distance, config=_ACTIVE_CFG,
            action_deltas=ACTION_DELTAS, move_energy_cost=MOVE_ENERGY_COST,
            padding_loc=PADDING_LOC,
            terr_map=terr_map, terr_here_fid=FID_TERRITORY_HERE, global_loc=GLOBAL_LOC,
            fid_energy=FID_INV_ENERGY, agent_loc=AGENT_LOC,
        )
        _autopsy_rows = None
        if _AUTOPSY_STEP >= 0 and world_step == _AUTOPSY_STEP:
            _autopsy_rows = []
            ctx.autopsy = lambda cdr, cdc, d, s, terr: _autopsy_rows.append(
                {"cdr": cdr, "cdc": cdc, "d": d, "terr": terr,
                 "pos_F": s.pos_F, "pos_R": s.pos_R, "pos_S": s.pos_S,
                 "nF": s.nF, "nR": s.nR, "nS": s.nS,
                 "pF": s.pF, "pR": s.pR, "pS": s.pS})
        # 1d-bis: extractores VIRTUALES recordados del elemento DEMANDADO (gateado por demanda viva).
        virtual_extractors = None
        if _VIRTUAL_EXTRACT and mem is not None and trans_ctx is not None and hasattr(mem, "virtual_extractors_rel"):
            from appraisal.appraisal_v4 import _read_resources as _rr, _MAT_FIDS as _mf
            _dem, _th, _ah = _rr(scalar_map)
            _demanded = {_mf[x][2] for x, dv in _dem.items() if dv > 0 and x in _mf}
            if _demanded:
                virtual_extractors = mem.virtual_extractors_rel(_demanded, max_age=None)
        # Eslabón 2 — HUB VIRTUAL recordado (espejo). Solo si NO se percibe el hub (percepción manda) y el
        # agente lleva carga de elementos. Posición relativa del hub recordado desde mem._entries (cls hub).
        virtual_hub = None
        if _DEPOSIT_VIRTUAL and mem is not None and trans_ctx is not None and hasattr(mem, "_entries"):
            _own = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
            _hub_seen = any(TAG_TYPE_HUB in tgs and _own in tgs for tgs in tag_map.values())
            _efids = getattr(trans_ctx, "element_inv_fids", None) or (FID_INV_CARBON,)
            _held = sum(get_multipart(scalar_map, AGENT_LOC, f) for f in _efids)
            if not _hub_seen and _held > 0:
                _ar, _ac = getattr(mem, "_agent_world", (0, 0))
                _cand = [((wr - _ar), (wc - _ac)) for (wr, wc, cls) in mem._entries if cls == "hub"]
                if _cand:
                    virtual_hub = min(_cand, key=lambda r: abs(r[0]) + abs(r[1]))
        # Córtex C2 — crédito de cadena (escalar por-tick): el Δd del align propagado al terminal
        # donde se equipó, descontado por confianza·γ^D. had_aligner desactiva si ya iba equipado.
        chain = None
        if _CHAIN and _MARCADOR:
            _cred = _chain_align_credit(s_curr, scalar_map, tag_map, team_side, mem, world_step)
            _had = get_multipart(scalar_map, AGENT_LOC, FID_INV_ALIGNER) > 0
            chain = (_cred, _had, FID_INV_ALIGNER, FID_INV_HEART)
        # Córtex C4 — FUERZA-d de oportunidad (escalar por-tick: gear_rel + Δd_align·conf). El planner la
        # aplica γ^L1 a cada terminal → gradiente continuo hacia la gear. None si no hay oportunidad/heart.
        gain = None
        if _GAIN and _MARCADOR:
            _op = _gain_opportunity(s_curr, scalar_map, tag_map, team_side, mem, world_step)
            if _ECON_CONST:
                # CONSTITUCIÓN ECONÓMICA (spec §1.5): el MOTOR ÚNICO absorbe minado+depósito+preempt+height.
                # Si el motor tiene objetivo (hub INFABRICABLE), PREEMPTA categóricamente a la conquista;
                # si no (fabricable/sin objetivo), la conquista compite. deposit/mining/restock NO se llaman.
                _sm = _supply_motor(s_curr, scalar_map, tag_map, team_side, mem, world_step)
                # tirón EFECTIVO al agente = altura · γ^L1(rel): decisión-relevante (near vence a far). El
                # preempt de la constitución era "a toda distancia"; la cuesta lo hace distancia-consciente.
                def _eff(g):
                    return g[1] * (GAIN_GAMMA ** (abs(g[0][0]) + abs(g[0][1]))) if g is not None else 0.0
                if _sm is not None:
                    # ENMIENDA: preempt con MARGEN (cuesta). El suministro manda salvo que la conquista/equipar
                    # sea CLARAMENTE mejor por TIRÓN EFECTIVO: op_eff > k · sm_eff. k=0 ⇒ binario (bit-exact).
                    if _ECON_CONQUEST_MARGIN > 0.0 and _op is not None and _eff(_op) > _ECON_CONQUEST_MARGIN * _eff(_sm):
                        gain = (_op[0], _op[1], GAIN_GAMMA)
                    else:
                        gain = (_sm[0], _sm[1], GAIN_GAMMA)
                elif _op is not None:
                    gain = (_op[0], _op[1], GAIN_GAMMA)
                if os.environ.get("GEMV_ECON_MARGIN_DBG"):   # calibración del k EN FRÍO: loguea tirones EFECTIVOS (no interviene)
                    _sme=_eff(_sm); _ope=_eff(_op)
                    _smd=(abs(_sm[0][0])+abs(_sm[0][1])) if _sm else None
                    _opd=(abs(_op[0][0])+abs(_op[0][1])) if _op else None
                    _log(f"MARGIN_CAL step={world_step} sm_raw={(round(_sm[1],3) if _sm else None)} sm_d={_smd} sm_eff={round(_sme,4)} "
                         f"op_raw={(round(_op[1],3) if _op else None)} op_d={_opd} op_eff={round(_ope,4)} "
                         f"ratio_eff={(round(_ope/_sme,3) if _sme>0 else None)}")
                if os.environ.get("GEMV_ECON_DBG"):     # instrumentación P2/P3: observa, no interviene
                    _econ_log_tick(scalar_map, tag_map, team_side, mem, world_step, _sm)
            else:
                _dep = _deposit_gain(s_curr, scalar_map, tag_map, team_side, mem, world_step)  # None si OFF/no aplica
                _min = _mining_gain(s_curr, scalar_map, tag_map, team_side, mem, world_step)   # None si OFF/no aplica
                _restock = [c for c in (_dep, _min) if c is not None]   # no vacío ⟺ hub INFABRICABLE (dolor>0)
                if _RESTOCK_PREEMPT and _restock:
                    # hub infabricable → reponer PREEMPTA a conquistar (dolor > aspiración). No infla la magnitud del
                    # gain (el dolor de cuerpo sigue mandando en la base-d): sólo elige el objetivo de reposición.
                    _best = max(_restock, key=lambda c: c[1])
                    gain = (_best[0], _best[1], GAIN_GAMMA)
                else:
                    _cands = [c for c in (_op, _dep, _min) if c is not None]
                    if _cands:
                        _best = max(_cands, key=lambda c: c[1])   # orden actual: máx Δd sobre todo (conquista incluida)
                        gain = (_best[0], _best[1], GAIN_GAMMA)
        # ESLABÓN FORRAJEO: si NO hay oportunidad de junction (la junction preempta: jerarquía), la exploración
        # toma el canal GAIN como fuerza f+ DÉBIL hacia la frontera global. El dolor (base d) sigue dominando.
        _forage_on = False
        if gain is None and _FORAGE:
            _fg = _forage_gain(s_curr, mem, world_step)
            if _fg is not None:
                gain = _fg
                _forage_on = True
        # GEMV_SURVIVAL — LA CARA ACTIVA DEL CUERPO: volver a casa (hub = centro del territorio propio) a regenerar
        # cuando la reserva de vida no cubre el viaje de vuelta. Compite por magnitud (cuerpo>todo): si W_SURV·U
        # supera el valor de la gain vigente, la reemplaza (rumbo al hub por la misma maquinaria GEO_GLOBAL/waypoint).
        # OFF ≡ bit-exact. Sano (U=0) ≡ bit-exact por construcción. Coste acotado: BFS al hub sólo fuera de casa.
        _survival_on = False
        _surv_hf = None                                      # cura: campo GEO_GLOBAL al hub, reusado por COMMIT-HOME
        if _SURVIVAL and _MARCADOR:
            _hp_s = get_multipart(scalar_map, AGENT_LOC, 20)
            _on_terr = get_scalar(scalar_map, GLOBAL_LOC, FID_TERRITORY_HERE)
            _own_s = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
            # hub_rel: percibido o recordado (misma fuente que la cara depósito)
            _hub_rel_s = None
            for _loc, _tg in tag_map.items():
                if TAG_TYPE_HUB in _tg and _own_s in _tg:
                    _hub_rel_s = (_loc // EGOCENTRIC_COLS - AGENT_ROW, _loc % EGOCENTRIC_COLS - AGENT_COL); break
            if _hub_rel_s is None and mem is not None and hasattr(mem, "_entries"):
                _ar_s, _ac_s = getattr(mem, "_agent_world", (0, 0))
                _cand_s = [(wr - _ar_s, wc - _ac_s) for (wr, wc, cls) in mem._entries if cls == "hub"]
                if _cand_s:
                    _hub_rel_s = min(_cand_s, key=lambda r: abs(r[0]) + abs(r[1]))
            # d_home: en territorio propio = 0 (sin BFS); fuera = geodésica al hub − R (acotada ≥0)
            _d_home = None
            # TERRITORIO ESTRICTO (cura 4, de fuente): casa = territory:here==1 (territorio propio,
            # team_territory.presence.heal energía+100; 0% sangría medida, mediana dist_hub 6). NO ==2
            # (enemigo/clips: mediana dist_hub 50, junto a los ships de las esquinas, damage_strangers →
            # sangra) ni ==0 (neutro). El ag1 murió en territory=2 tratado como casa por el viejo >=1.
            if _on_terr == 1:
                _d_home = 0.0
            elif _hub_rel_s is not None:
                _hf = _geodesic_field_global(tag_map, list(_hub_rel_s), mem, extra_solid=_desm_solid) if _GEO_GLOBAL else None
                _surv_hf = _hf                               # PRONG A: guardar el campo para COMMIT-HOME (misma fuente que d_home)
                _dg = _hf.get((0, 0)) if _hf else None
                if _dg is not None:
                    _d_home = max(0.0, _dg - _SURV_R)
            if _d_home is not None:
                _reserva = _hp_s - _d_home
                # PRONG B (umbral consciente del territorio): en ENEMIGO (on_terr==2) la sangría medida es ~2×
                # (1.96 vs 1.00/t) → el margen seguro se DOBLA (RESERVE_SAFE·bleed_local) para girar a tiempo.
                # OFF (SURVIVAL_HOME=0) → factor 1.0 → umbral 25 de siempre (bit-exact).
                _reserve_eff = _SURV_RESERVE_SAFE * (2.0 if (_SURVIVAL_HOME and _on_terr == 2) else 1.0)
                _U = max(0.0, min(1.0, (_reserve_eff - _reserva) / _reserve_eff))
                if _U > 0.0 and _hub_rel_s is not None:
                    _surv_val = _SURV_W * _U
                    if gain is None or _surv_val >= gain[1]:
                        gain = (_hub_rel_s, _surv_val, GAIN_GAMMA)
                        _survival_on = True
                        _forage_on = False
                if os.environ.get("GEMV_SURVIVAL_DBG"):
                    _log(f"SURVIVAL step={world_step} hp={_hp_s} on_terr={_on_terr} d_home={(round(_d_home,1) if _d_home is not None else None)} "
                         f"reserva={round(_hp_s - _d_home, 1)} U={round(_U,3)} surv_val={round(_SURV_W*_U,2)} won={_survival_on}")
        # META PRÓXIMA (GEMV_GAIN_WAYPOINT): si el objetivo de la gain está fuera del alcance del rollout, re-apunta
        # la atracción a un punto intermedio del camino geodésico (mismo valor). Tras la competición (gate d: orden
        # intacto); sólo cambia DÓNDE. Objetivo cercano/inalcanzable → gain sin cambio (gates b/e). OFF ≡ bit-exact.
        if _GAIN_WAYPOINT and _GEO_GLOBAL and gain is not None:
            _wp = _gain_waypoint(gain[0], tag_map, mem, _HORIZON)
            if _wp is not None:
                gain = (_wp, gain[1], gain[2])
        _rd = CHAIN_GAMMA if (_ROLLOUT_DISCOUNT and _CHAIN and _MARCADOR) else None
        # GEODESIA: campo de camino-más-corto desde el objetivo de la gain sobre el mapa conocido (sólidos
        # bloquean). El planner usa gain_field[terminal] en vez de L1 → rodea estaciones/muros. OFF→None→L1.
        _gsolids = None
        if gain is not None and _GEO_GLOBAL:            # GEO_GLOBAL: distancia caminable sobre el mapa conocido
            if _GEO_WALL_INF:                            # fix fantasma: recoge la MISMA fuente de sólidos
                _gfield, _gsolids = _geodesic_field_global(tag_map, gain[0], mem, extra_solid=_desm_solid, return_solids=True)
            else:
                _gfield = _geodesic_field_global(tag_map, gain[0], mem, extra_solid=_desm_solid)
        else:
            _gfield = _geodesic_field(tag_map, gain[0], extra_solid=_desm_solid) if (_GEODESIC and gain is not None) else None
        # DIAGNÓSTICO (GEMV_GEO_DBG, NO toca la decisión): estado del campo geodésico de la GAIN — None/fallback,
        # tamaño, alcanzabilidad del objetivo, y distancia geodésica (None=cae a L1) vs L1 de stay/N/S/E/W.
        if os.environ.get("GEMV_GEO_DBG") and gain is not None:
            _gt = gain[0]
            _cd = {}
            for _k, (_dr, _dc) in (("stay",(0,0)),("N",(-1,0)),("S",(1,0)),("E",(0,1)),("W",(0,-1))):
                _gv = _gfield.get((_dr, _dc)) if _gfield else None
                _cd[_k] = [_gv, abs(_gt[0]-_dr)+abs(_gt[1]-_dc)]   # [geodésica|None, L1]
            _log("GEO_DBG " + json.dumps({"step": world_step, "gain_target": list(_gt),
                 "gfield_none": _gfield is None, "gfield_size": (len(_gfield) if _gfield else 0),
                 "target_in_field": (tuple(_gt) in _gfield) if _gfield else False, "cells": _cd}))
        _meta_tb = None
        _ck = _COMMIT_K if (_COMMIT or _COMMIT_DEPOSIT) else None
        _extract = None
        if _TIEBREAK:
            _pt = plan_terminal(
                tokens, scalar_map, tag_map, action_names, team_side, mem,
                _HORIZON, S_SCALE, ctx, use_cache=_PLAN_CACHE,
                trans_ctx=trans_ctx, world_step=world_step, virtual_extractors=virtual_extractors,
                track_meta=True, virtual_hub=virtual_hub, chain=chain, gain=gain, rollout_discount=_rd,
                gain_field=_gfield, commit_k=_ck, gain_solids=_gsolids,
            )
            if _ck is not None: terminal, _meta_tb, pstats, _extract = _pt
            else: terminal, _meta_tb, pstats = _pt
        else:
            _pt = plan_terminal(
                tokens, scalar_map, tag_map, action_names, team_side, mem,
                _HORIZON, S_SCALE, ctx, use_cache=_PLAN_CACHE,
                trans_ctx=trans_ctx, world_step=world_step, virtual_extractors=virtual_extractors,
                virtual_hub=virtual_hub, chain=chain, gain=gain, rollout_discount=_rd,
                gain_field=_gfield, commit_k=_ck, gain_solids=_gsolids,
            )
            if _ck is not None: terminal, pstats, _extract = _pt
            else: terminal, pstats = _pt
        # tanda 2 MB1: ablación del virtual EN EL MISMO estado (muestreada) — Δd_virtual = term_d(con)−term_d(sin).
        # Aísla la contribución del virtual al plan (en tanda 1 fue 0; el spread territorial NO cuenta).
        if _MB1_EVERY > 0 and virtual_extractors and (world_step % _MB1_EVERY == 0):
            term_nov, _ = plan_terminal(
                tokens, scalar_map, tag_map, action_names, team_side, mem,
                _HORIZON, S_SCALE, ctx, use_cache=_PLAN_CACHE,
                trans_ctx=trans_ctx, world_step=world_step, virtual_extractors=None,
            )
            dd = {a: round(terminal[a] - term_nov.get(a, terminal[a]), 6) for a in terminal}
            _log("GEMV_MB1 " + json.dumps({"step": world_step, "dvirtual": dd,
                 "max_abs": round(max(abs(v) for v in dd.values()), 6),
                 "argmin_con": min(terminal, key=terminal.get), "argmin_sin": min(term_nov, key=term_nov.get),
                 "n_virtual": len(virtual_extractors)}))
        if _autopsy_rows is not None:
            home = [r for r in _autopsy_rows if r["terr"] == 1]
            other = [r for r in _autopsy_rows if r["terr"] != 1]
            bh = min(home, key=lambda r: r["d"]) if home else None
            bo = min(other, key=lambda r: r["d"]) if other else None
            _log("GEMV_AUTOPSY " + json.dumps({
                "step": world_step, "H": _HORIZON, "n_terminal": pstats["n_terminal"],
                "n_home_terminals": len(home), "best_home": bh, "best_other": bo}))
        if _TIEBREAK:
            attractor = _compute_attractor(scalar_map, tag_map, team_side, s_curr,
                                           appr_debug, mem, virtual_extractors, world_step=world_step)
            # Eslabón 3 (EXPLORE) — atractor fresco N4 gateado por HAMBRE (urgR o demanda). / DERIVA — atractor
            # fresco N4 en el régimen del PRÓSPERO (saciado, sin oportunidad conocida, sin soplo). Ambos usan el
            # mismo N4 (el más débil): jamás compiten con nada real (el hambre/gain/soplo crean no-empate y ceden).
            fresh_attractor = None
            _deriva_on = False
            if _rastreo is not None and mem is not None and hasattr(mem, "_agent_world"):
                _urg = s_curr.pR < 2.0
                _dl = any(v > 0 for v in (appr_debug or {}).get("demands", {}).values()) if appr_debug else False
                _ar, _ac = mem._agent_world
                if _EXPLORE and (_urg or _dl):
                    fresh_attractor = _rastreo.fresh_attractor_rel(_ar, _ac, world_step)
                elif _DERIVA and (not _dl) and gain is None and n_soplo == 0:
                    # EL PASEO DEL OCIOSO-DE-FACTO (reformulado 2026-07-19): NO se exige saciedad (`not _urg`
                    # quitado) — el descentramiento de G-EMV garantiza anhelo crónico (paper §3), así que
                    # "próspero/saciado" era inalcanzable por construcción. La deriva incluye al HAMBRIENTO sin
                    # comida conocida (forrajeo): sin oportunidad territorial, sin soplo, sin demanda → camina a
                    # lo NO rastreado. Protección ESTRUCTURAL: solo ordena EMPATES de terminal_d (N4); cualquier
                    # gradiente real (extractor/antena/soplo alcanzable) crea no-empate y la deriva cede sola.
                    fresh_attractor = _rastreo.fresh_attractor_rel(_ar, _ac, world_step)
                    _deriva_on = fresh_attractor is not None
            # GEODESIA: campo de camino-más-corto desde el atractor de desempate → el N3 rodea sólidos
            # (el atasco del paisaje plano de s0). Reusa _gfield si el atractor coincide con la gain; si no, BFS.
            _afield = None
            if _GEODESIC and attractor is not None:
                if gain is not None and tuple(gain[0]) == tuple(attractor):
                    _afield = _gfield                    # reusa el campo de la gain si coincide el objetivo
                elif _GEO_GLOBAL:
                    _afield = _geodesic_field_global(tag_map, attractor, mem, extra_solid=_desm_solid)
                else:
                    _afield = _geodesic_field(tag_map, attractor, extra_solid=_desm_solid)
            best_action = select_tiebreak(action_names, preds, terminal, _meta_tb,
                                          attractor=attractor, action_deltas=ACTION_DELTAS,
                                          exclude_noop=_N2_NONOOP, fresh_attractor=fresh_attractor,
                                          tie_unified=_TIE_UNIFIED, attr_field=_afield,
                                          slot=slot, c4_on=_PASO_C4)
        else:
            best_action = select(action_names, preds, terminal)
        plan_dbg = {
            "H": _HORIZON,
            "terminal_d": {a: round(terminal[a], 5) for a in action_names},
            "n_terminal": pstats["n_terminal"],
            "transition": bool(trans_ctx is not None),
            "chain_credit": round(chain[0], 5) if chain else 0.0,   # Córtex C2 (0 si OFF/sin cadena)
            "gain_scalar": round(gain[1], 5) if gain else 0.0,       # Córtex C4 (Δd_align·conf; 0 si OFF/sin oport.)
            "gain_gear_rel": list(gain[0]) if gain else None,        # gear relativa (dirección de la fuerza)
            "deriva": _deriva_on,                                     # DERIVA: paseo del próspero activo este tick
            "forage": _forage_on,                                     # FORRAJEO: fuerza f+ de exploración activa este tick
        }
        # GEMV_COMMIT — compromiso de plan: da CONSTANCIA a lo decidido por el juez (rompe la replanificación
        # miope del 2-ciclo). Ejecuta los k pasos del plan DP salvo interrupción del sagrado (a/b/c). OFF≡bit-exact.
        # COMMIT-DEPÓSITO: _COMMIT global lo activa en TODO (regresión histórica → OFF por defecto). _COMMIT_DEPOSIT
        # lo activa SOLO en la cara depósito: cargo=lote (ajuste del lote) + hub infabricable (∃ material<receta,
        # percibido o de despensa) — exactamente el disparo de cara=DEPOSITO del motor. Fuera de ahí, no compromete.
        _commit_active = _COMMIT
        _mine_elem = None                                    # cura 2: elemento objetivo del commit-minado (None = no minado)
        _align_junc = None                                   # cura 3 (COMMIT_ALIGN): pos-mundo de la junction comprometida (None = no conquista)
        # COMMIT-HOME (cura 4, survival-completo): PRECEDENCIA MÁXIMA — si survival ganó el gain (U>0, gain[0]
        # =hub_rel), comprometer el retorno sobre el campo GEO_GLOBAL `_surv_hf` (el mismo de d_home) → cierre a
        # ~1/t recto a casa, sin la oscilación del planner. Va PRIMERO (antes de depósito/minado/align): el cuerpo
        # manda; y si el agente iba cargado (commit-depósito), el destino es el MISMO hub → convergencia trivial,
        # sin churn. Sólo suelta al llegar (on_terr==1 → U=0 → _survival_on False el tick siguiente) o por _rej.
        _home_active = bool(_SURVIVAL_HOME and _survival_on and _surv_hf is not None and mem is not None)
        if _home_active:
            _commit_active = True
        if not _home_active and _COMMIT_DEPOSIT and not _COMMIT and _ECON_CONST and mem is not None:
            from appraisal.appraisal_shelf import _OWN_FIDS as _OF_C, _TEAM_FIDS as _TF_C, ALIGNER_RECIPE as _REC_C
            _cargo_c = sum(get_multipart(scalar_map, AGENT_LOC, f) for f in _OF_C)
            _own_c = TAG_TEAM_COGS if team_side == "cogs" else TAG_TEAM_CLIPS
            if any(TAG_TYPE_HUB in t and _own_c in t for t in tag_map.values()):
                _held_c = [get_scalar(scalar_map, GLOBAL_LOC, f) for f in _TF_C]
            else:
                _pm_c = _pantry_ctx.get('vals') if _PANTRY_MEM else None
                _held_c = [_pm_c.get(f, 0.0) for f in _TF_C] if _pm_c else None
            _infab_c = _held_c is not None and any(_held_c[i] < _REC_C[i] for i in range(len(_REC_C)))
            # PRECEDENCIA (ii, COMMIT): con la banda, un cargado compromete la ruta al hub SIN exigir infabricable
            # (cura la Vía-1 de B: el hub fabricable-vital ya no desengancha el retorno). OFF: exige infab (histórico).
            _commit_active = (_cargo_c >= _MINING_LOTE) if _CARGO_PRECEDENCE else (_cargo_c >= _MINING_LOTE and _infab_c)
            # COMMIT-MINADO (cura 2, HE3): cargo<lote y la gain apunta a un EXTRACTOR conocido (percibido o
            # recordado) → comprometer el viaje al pozo. `_mine_elem` = índice del ELEMENTO objetivo (en el orden
            # oxy,carb,germ,sil). La interrupción "cambio de elemento" compara este contra el comprometido.
            _mine_elem = None
            if (_COMMIT_MINE and not _commit_active and _cargo_c < _MINING_LOTE and gain is not None
                    and not _forage_on and not _survival_on):
                from memoria.memoria_v1 import _EXTRACTOR_CLS as _ECLS_C
                _ord_c = ("extractor_oxygen", "extractor_carbon", "extractor_germanium", "extractor_silicon")
                _gr, _gc = AGENT_ROW + int(gain[0][0]), AGENT_COL + int(gain[0][1])
                _gext = None
                if 0 <= _gr < EGOCENTRIC_ROWS and 0 <= _gc < EGOCENTRIC_COLS:
                    _gext = next((_ECLS_C.get(_tt) for _tt in (set(tag_map.get(_gr * EGOCENTRIC_COLS + _gc, set())) & EXTRACTOR_TAGS)), None)
                if _gext is None and hasattr(mem, "_entries"):          # objetivo recordado (fuera de ventana)
                    _ar2, _ac2 = getattr(mem, "_agent_world", (0, 0))
                    _gt = (int(gain[0][0]), int(gain[0][1]))
                    for (wr, wc, cls) in mem._entries:
                        if cls.startswith("extractor_") and (wr - _ar2, wc - _ac2) == _gt:
                            _gext = cls; break
                if _gext in _ord_c:
                    _mine_elem = _ord_c.index(_gext)
                    _commit_active = True
        # COMMIT-ALIGN (cura 3): la CARA DE CONQUISTA. Con bolsillo VACÍO, aligner+heart en mano y la gain
        # apuntando a una junction GRIS/RIVAL (percibida o recordada) → comprometer la ruta a LA CASILLA de la
        # junction. Espejo de la detección _gext→_mine_elem del minado, pero para junctions. Precede el
        # suministro por SECUENCIA (deposito/minado ya pusieron _commit_active si hay cargo → `not _commit_active`).
        if (_COMMIT_ALIGN and not _commit_active and gain is not None
                and not _forage_on and not _survival_on and mem is not None):
            from appraisal.appraisal_shelf import _OWN_FIDS as _OF_A
            _cargo_a = sum(get_multipart(scalar_map, AGENT_LOC, f) for f in _OF_A)
            _has_al_a = get_multipart(scalar_map, AGENT_LOC, FID_INV_ALIGNER) > 0
            _has_hr_a = get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART) >= 1
            if _cargo_a == 0 and _has_al_a and _has_hr_a:
                _own_net_a = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
                _gr_a, _gc_a = AGENT_ROW + int(gain[0][0]), AGENT_COL + int(gain[0][1])
                _is_junc = False
                if 0 <= _gr_a < EGOCENTRIC_ROWS and 0 <= _gc_a < EGOCENTRIC_COLS:
                    _tset_a = tag_map.get(_gr_a * EGOCENTRIC_COLS + _gc_a, set())
                    _is_junc = (TAG_TYPE_JUNCTION in _tset_a and _own_net_a not in _tset_a)
                if not _is_junc and hasattr(mem, "_entries"):     # objetivo recordado (fuera de ventana)
                    _ar_a, _ac_a = getattr(mem, "_agent_world", (0, 0))
                    _gt_a = (int(gain[0][0]), int(gain[0][1]))
                    for (wr, wc, cls) in mem._entries:
                        if cls in ("junction_gray", "junction_rival") and (wr - _ar_a, wc - _ac_a) == _gt_a:
                            _is_junc = True; break
                if _is_junc:
                    _aw_a = getattr(mem, "_agent_world", (0, 0))
                    _align_junc = (_aw_a[0] + int(gain[0][0]), _aw_a[1] + int(gain[0][1]))   # pos-mundo de la junction
                    _commit_active = True
        if _commit_active and mem is not None:
            # el estado del compromiso vive en `mem` (choose_action es función de módulo, no método; mem persiste).
            _cplan = getattr(mem, "_commit_plan", [])
            _csnap = getattr(mem, "_commit_snap", None)
            _cprevpos = getattr(mem, "_commit_prevpos", None)
            _cprevmove = getattr(mem, "_commit_prevmove", False)
            _aw = tuple(mem._agent_world) if hasattr(mem, "_agent_world") else None
            _ns = sum(1 for t in tag_map.values() if (TAG_TYPE_JUNCTION in t or TAG_TYPE_ALIGNER in t or TAG_TYPE_HUB in t))
            _dem = bool(appr_debug and any(v > 0 for v in (appr_debug.get("demands", {}) or {}).values())) if appr_debug else False
            _hp = get_multipart(scalar_map, AGENT_LOC, 20)
            _oppact = (gain is not None and not _forage_on)          # oportunidad territorial REAL (no forrajeo)
            _gval = gain[1] if gain is not None else 0.0             # (d) valor del objetivo de gain actual
            _snap = (_ns, round(s_curr.pR, 2), _dem, _hp, _oppact, _gval)
            _interr = True
            if _cplan and _csnap is not None:
                _rej = _cprevmove and _aw is not None and _aw == _cprevpos                     # (a) el juego rechazó
                _newp = (_snap[4] != _csnap[4])                                                 # (b) EVENTO: oportunidad real aparece/desaparece (flip oppact). NO n_struct (wobble de ventana = ruido de borde, familia del anillo)
                _pain = (_snap[1] < _csnap[1] - 0.05) or (_snap[2] and not _csnap[2]) or (_snap[3] < _csnap[3])  # (c) dolor crece
                # (d firmada) objetivo CLARAMENTE mejor que el comprometido → soltar (margen anti-churn). No toca la meseta.
                _better = (_COMMIT_GAIN_INTERRUPT and len(_csnap) > 5
                           and _gval > _csnap[5] * (1.0 + _COMMIT_GAIN_MARGIN))
                # PRECEDENCIA (iii, NO SORDA — afinación 1): al cargado comprometido SÓLO lo interrumpen el rechazo
                # del mundo (a, alimenta DESMENTIDO) y el DOLOR DE CUERPO real (pR/hp; la torre manda cuerpo>todo).
                # Se SILENCIAN (b) el flip de oportunidad (colchón/portfolio) y la contabilidad (demanda, mejor-gain).
                if _home_active:
                    # COMMIT-HOME (cura 4): el CUERPO manda — NO lo suelta nada salvo el rechazo del mundo (_rej,
                    # que reruta vía DESMENTIDO). Ni dolor (ya va a casa a curarlo) ni oportunidad ni mejor-gain.
                    # Llegar a casa lo apaga solo (on_terr==1 → U=0 → _survival_on False → _home_active False).
                    _interr = _rej
                elif _mine_elem is not None:
                    # COMMIT-MINADO (cura 2): rechazo (a) + dolor de cuerpo real (c) + CAMBIO DE ELEMENTO-cuello
                    # (el objetivo del suministro mudó de elemento → la cascada manda). El cambio de INSTANCIA del
                    # MISMO elemento (pozo más-cercano) NO interrumpe (mismo _mine_elem) → el churn de ag4 muere.
                    _pain_cuerpo = (_snap[1] < _csnap[1] - 0.05) or (_snap[3] < _csnap[3])
                    _elem_changed = (getattr(mem, "_mine_elem", None) is not None
                                     and _mine_elem != getattr(mem, "_mine_elem", None))
                    _interr = _rej or _pain_cuerpo or _elem_changed
                elif _align_junc is not None:
                    # COMMIT-ALIGN (cura 3): rechazo (a) + dolor de cuerpo real (c) + _junc_owned (ESTADO: la
                    # junction comprometida se volvió NUESTRA — propia o adelantada por un aliado → meta lograda).
                    # SILENCIADO: otra gris más cercana (CERCANÍA; el stored-plan da constancia como en el minado)
                    # y la captura por CLIPS (rival sigue siendo target; _junc_owned mira SOLO own_net).
                    _pain_cuerpo = (_snap[1] < _csnap[1] - 0.05) or (_snap[3] < _csnap[3])
                    _junc_owned = False
                    _ajw = getattr(mem, "_align_junc_world", None)
                    if _ajw is not None and _aw is not None:
                        _gr_j, _gc_j = AGENT_ROW + (_ajw[0] - _aw[0]), AGENT_COL + (_ajw[1] - _aw[1])
                        if 0 <= _gr_j < EGOCENTRIC_ROWS and 0 <= _gc_j < EGOCENTRIC_COLS:
                            _own_net_j = TAG_NET_COGS if team_side == "cogs" else TAG_NET_CLIPS
                            _junc_owned = _own_net_j in tag_map.get(_gr_j * EGOCENTRIC_COLS + _gc_j, set())
                    _interr = _rej or _pain_cuerpo or _junc_owned
                elif _CARGO_PRECEDENCE:
                    _pain_cuerpo = (_snap[1] < _csnap[1] - 0.05) or (_snap[3] < _csnap[3])   # pR-drop o hp-drop (cuerpo)
                    _interr = _rej or _pain_cuerpo
                else:
                    _interr = _rej or _newp or _pain or _better
            if _cplan and not _interr:
                best_action = _cplan.pop(0)                          # CONSTANCIA: siguiente paso del plan comprometido
                mem._commit_plan = _cplan
                plan_dbg["commit"] = "exec"
            else:
                _was = bool(_cplan)
                mem._commit_plan = []
                # CURA DEL RETORNO capa 2: en la cara depósito, comprometer la RUTA GEODÉSICA al OBJETIVO DEL
                # MOTOR (`_gfield` = campo geodésico a gain[0] = hub_rel; INCLUYE la celda-meta sólida a dist 0 →
                # el último paso es el BUMP=depósito). NO el `_afield` de desempate (que apunta al atractor de
                # tie-break, no al hub del motor) ni el DP degenerado de la meseta. Con el hub FUERA de la ventana
                # ego, `_gfield`=None → ruta vacía → DP de siempre (el retorno lejano es otra capa: horizonte
                # abierto, RUTA_MEM/GEO_GLOBAL, hoy OFF).
                # ruta geodésica al objetivo del motor (`_gfield`=campo a gain[0]): hub en la cara depósito, POZO
                # en la cara minado (cura 2) — la celda-meta sólida a dist 0 → el último paso es el BUMP (=depósito
                # o =minado). Fuera de ventana ego, `_gfield`=None → DP de siempre.
                if _home_active:
                    # COMMIT-HOME (cura 4): rutar sobre el campo GEO_GLOBAL al hub (`_surv_hf`, el de d_home) →
                    # cierre a ~1/t recto a casa. FALLBACK: si el gradiente no reduce en la celda del agente
                    # (frontera no mapeada), paso RECTO hacia hub_rel (dirección) — mejor que oscilar.
                    _route = _commit_route_geodesic(_surv_hf, _COMMIT_K)
                    if not _route and gain is not None:
                        _hr, _hc = int(gain[0][0]), int(gain[0][1])
                        if abs(_hr) >= abs(_hc) and _hr != 0:
                            _route = ["move_south" if _hr > 0 else "move_north"]
                        elif _hc != 0:
                            _route = ["move_east" if _hc > 0 else "move_west"]
                else:
                    _route = (_commit_route_geodesic(_gfield, _COMMIT_K)
                              if ((_COMMIT_DEPOSIT or (_COMMIT_MINE and _mine_elem is not None)
                                   or (_COMMIT_ALIGN and _align_junc is not None)) and not _COMMIT) else None)
                if _route:
                    best_action = _route[0]                          # rumbo geodésico al objetivo (no el argmin de meseta)
                    mem._commit_plan = _route[1:]
                    mem._commit_snap = _snap
                    mem._mine_elem = _mine_elem                      # cura 2: elemento comprometido (None en depósito)
                    mem._align_junc_world = _align_junc              # cura 3: junction comprometida (None fuera de conquista)
                    plan_dbg["commit_route"] = "geodesic"
                elif _extract is not None:                           # (re)comprometerse con el plan DP del ganador
                    mem._commit_plan = list(_extract(best_action, _COMMIT_K)[1:])
                    mem._commit_snap = _snap
                    mem._mine_elem = _mine_elem
                    mem._align_junc_world = _align_junc
                plan_dbg["commit"] = "interrupt" if _was else "commit"
            mem._commit_prevpos = _aw
            mem._commit_prevmove = (best_action != "noop")
        elif (_COMMIT_DEPOSIT or _COMMIT_ALIGN or _SURVIVAL_HOME) and not _COMMIT and mem is not None and getattr(mem, "_commit_plan", None):
            mem._commit_plan = []                               # fuera de la cara comprometible: no arrastrar el plan
        # GEMV_RD_PROBE — sonda contrafactual read-only (NO cambia la acción): recomputa el terminal con
        # ROLLOUT_DISCOUNT ON y lo loguea junto al normal → gate del tick real (¿ON hace equipar < south?).
        if os.environ.get("GEMV_RD_PROBE") and chain is not None and chain[0] > 0.0:
            _t_rd, _ = plan_terminal(
                tokens, scalar_map, tag_map, action_names, team_side, mem,
                _HORIZON, S_SCALE, ctx, use_cache=_PLAN_CACHE,
                trans_ctx=trans_ctx, world_step=world_step, virtual_extractors=virtual_extractors,
                virtual_hub=virtual_hub, chain=chain, gain=gain, rollout_discount=CHAIN_GAMMA,
            )
            plan_dbg["terminal_d_rd"] = {a: round(_t_rd[a], 5) for a in action_names}
        # DESMENTIDO — registrar el move/pos de ESTE tick (para detectar el rechazo el próximo) + debug.
        if _DESMENTIDO and mem is not None and hasattr(mem, "_agent_world"):
            mem._desm_last_action = best_action
            mem._desm_last_pos = tuple(mem._agent_world)
            plan_dbg["desm_blocked"] = len(_desm_solid) if _desm_solid else 0
    d_pred_best = preds[best_action]["d"]

    raw = {
        "hp": get_multipart(scalar_map, AGENT_LOC, 20),
        "energy": get_multipart(scalar_map, AGENT_LOC, FID_INV_ENERGY),
        # FIX 2026-07-03: territory:here es GLOBAL (loc 254), no AGENT_LOC.
        "territory": get_scalar(scalar_map, GLOBAL_LOC, FID_TERRITORY_HERE),
        "hearts": get_multipart(scalar_map, AGENT_LOC, FID_INV_HEART),  # Eslabón 1: mis hearts portados
    }
    if _HEARTS:
        # Serie del pantry del equipo (team_held por elemento) + acción make elegida — para trazar
        # la cadena depositar→fabricar y contar FABRICACIONES reales (make en el argmin).
        try:
            from appraisal.appraisal_shelf import _TEAM_FIDS as _thf
            raw["team_held"] = {int(f): get_scalar(scalar_map, GLOBAL_LOC, f) for f in _thf}
        except Exception:
            pass
        raw["chose_make"] = bool(preds.get(best_action, {}).get("make", False))

    # INSTRUMENTACIÓN read-only (no afecta la decisión): dump de TODOS los tokens
    # territory:{here,N,S,E,W} (fids 69-73) en CUALQUIER loc, para verificar si el
    # juego emite la señal territorial y en qué celda. Gated por GEMV_DUMP_TERR.
    if os.environ.get("GEMV_DUMP_TERR"):
        terr_tokens = [
            (loc, fid, val) for (loc, fid), val in scalar_map.items() if 69 <= fid <= 73
        ]
        _log("GEMV_TERRDUMP " + json.dumps({
            "agent_loc": AGENT_LOC, "terr_tokens": terr_tokens,
        }))

    # Count allies and rivals
    own_tag   = TAG_TEAM_COGS  if team_side == "cogs" else TAG_TEAM_CLIPS
    rival_tag = TAG_TEAM_CLIPS if team_side == "cogs" else TAG_TEAM_COGS
    allies = rivals = 0
    for loc in iter_spatial_locs(scalar_map, tag_map):
        tags = tag_map.get(loc, set())
        if TAG_TYPE_AGENT in tags:
            if own_tag in tags:
                allies += 1
            elif rival_tag in tags:
                rivals += 1
    raw["allies"] = allies
    raw["rivals"] = rivals

    sources = _energy_sources(scalar_map)

    debug = {
        "raw": raw,
        "state": {
            "pF": round(s_curr.pF, 4), "nF": round(s_curr.nF, 4),
            "pR": round(s_curr.pR, 4), "nR": round(s_curr.nR, 4),
            "pS": round(s_curr.pS, 4), "nS": round(s_curr.nS, 4),
            "pos_F": round(s_curr.pos_F, 4), "pos_R": round(s_curr.pos_R, 4),
            "pos_S": round(s_curr.pos_S, 4),
        },
        "d_curr": round(d_curr, 5),
        "preds": preds,
        "action": best_action,
        "d_pred": d_pred_best,
        "energy_sources": sources,
        "hub": _hub_visibility(tag_map, team_side),
    }
    if plan_dbg is not None:
        debug["plan"] = plan_dbg
        try:
            from planificador.planificador_v1 import _C4_DECISIONS as _c4d
            debug["c4_decisions"] = _c4d[0]              # contador acumulado de decisiones C4 (red final del paso)
        except Exception:
            pass
        # tanda 2: no-uniformidad del argmin (MB1 Δd = spread del terminal_d; en tanda 1 fue 0) + estado virtual
        _tv = list(terminal.values())
        debug["term_spread"] = round(max(_tv) - min(_tv), 6) if _tv else 0.0
        debug["virtual"] = {
            "n_mem_ext": sum(1 for (_, _, cls) in getattr(mem, '_entries', {})
                             if 'extractor' in cls) if mem is not None else 0,
            "n_virtual": len(virtual_extractors) if virtual_extractors else 0,
            "nearest_virtual": min((max(abs(r), abs(c)) for r, c, _ in virtual_extractors), default=-1)
                               if virtual_extractors else -1,
            "pantry_age": (world_step - _pantry_ctx['step']) if _PANTRY_MEM and _pantry_ctx['vals'] is not None else -1,
        }
    if appr_debug is not None:
        # Instrumentación de recursos (read-only): demanda del hub, material propio, extractores.
        exts = appr_debug.get("extractors", [])
        debug["res"] = {
            "demands": appr_debug.get("demands", {}),
            "total_mat": appr_debug.get("total_mat", 0),
            "n_extractors": len(exts),
            "min_ext_dist": round(min((d for _, d, _ in exts), default=-1), 2),
            "w_mat": {str(k): round(v, 3) for k, v in appr_debug.get("w_mat", {}).items()},
        }
    if mem is not None:
        debug["mem"] = mem.stats()
    if _PREGONERO and _MARCADOR:
        _nj = sum(1 for (_, _, c) in getattr(mem, "_entries", {})
                  if c in ("junction_gray", "junction_rival", "junction_own")) if mem is not None else 0
        debug["pregonero"] = {"soplos_inyectados": n_soplo, "junctions_conocidas": _nj,
                              "sightings_1a_mano": len(_pregonero_seen)}
    # DIAGNÓSTICO (GEMV_TAGMAP_DBG, NO toca la decisión): vuelca los sólidos PERCIBIDOS del tag_map en ego,
    # la posición ego del agente, la celda destino de la acción elegida y el tag en esa celda. Gate t44-60.
    if os.environ.get("GEMV_TAGMAP_DBG") and 44 <= world_step <= 60:
        _C = EGOCENTRIC_COLS
        _sol = sorted([(loc // _C - AGENT_ROW, loc % _C - AGENT_COL, sorted(set(t) & _SOLID_TYPES))
                       for loc, t in tag_map.items() if set(t) & _SOLID_TYPES])
        _dd = ACTION_DELTAS.get(best_action, (0, 0))
        _destloc = (AGENT_ROW + _dd[0]) * _C + (AGENT_COL + _dd[1])
        _log("TAGMAP_DBG " + json.dumps({
            "step": world_step, "agent_ego": [0, 0],
            "aw": (list(mem._agent_world) if (mem is not None and hasattr(mem, "_agent_world")) else None),
            "action": best_action, "dest_ego": [_dd[0], _dd[1]],
            "dest_tag": sorted(tag_map.get(_destloc, set())), "wall_tag_id": TAG_TYPE_WALL,
            "n_solids": len(_sol), "solids": _sol}))
    # DIAGNÓSTICO (GEMV_WALLMEM_DBG, NO toca la decisión): nº de muros recordados y bloqueos del veto por muro
    # RECORDADO (no percibido) este tick; aw para reconstruir celdas distintas. Env-gated ⇒ OFF≡bit-exact.
    if os.environ.get("GEMV_WALLMEM_DBG"):
        _nwalls = len(getattr(mem, "_walls", ())) if mem is not None else 0
        _nrem = sum(1 for _p in preds.values() if isinstance(_p, dict) and _p.get("blocked_remembered"))
        _log("WALLMEM_DBG " + json.dumps({"step": world_step, "n_walls": _nwalls, "veto_remembered": _nrem,
             "action": best_action,
             "aw": (list(mem._agent_world) if (mem is not None and hasattr(mem, "_agent_world")) else None)}))
    return best_action, debug


# ── Player ───────────────────────────────────────────────────────────────────

def _log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# Nombre de tag/feature del mundo → constante del adaptador. Regla [doc de diseño interna, no en el repo]: los
# identificadores del mundo (tag ids, feature ids) se LEEN del player_config, nunca se cablean.
_TAG_NAME = {
    "TAG_NET_CLIPS": "net:clips", "TAG_NET_COGS": "net:cogs",
    "TAG_TEAM_CLIPS": "team:clips", "TAG_TEAM_COGS": "team:cogs",
    "TAG_TYPE_AGENT": "type:agent", "TAG_TYPE_JUNCTION": "type:junction",
    "TAG_TYPE_HUB": "type:hub",
    "TAG_TYPE_OXYGEN_EXTRACTOR": "type:oxygen_extractor",
    "TAG_TYPE_CARBON_EXTRACTOR": "type:carbon_extractor",
    "TAG_TYPE_GERMANIUM_EXTRACTOR": "type:germanium_extractor",
    "TAG_TYPE_SILICON_EXTRACTOR": "type:silicon_extractor",
    "TAG_TYPE_ALIGNER": "type:aligner", "TAG_NET_COGS": "net:cogs", "TAG_NET_CLIPS": "net:clips",  # Eslabón 4
}
_FID_NAME = {
    "FID_TAG": "tag", "FID_INV_HP": "inv:hp", "FID_INV_ENERGY": "inv:energy",
    "FID_INV_OXYGEN": "inv:oxygen", "FID_INV_CARBON": "inv:carbon",
    "FID_INV_GERMANIUM": "inv:germanium", "FID_INV_SILICON": "inv:silicon",
    "FID_INV_HEART": "inv:heart",  # Eslabón 1
    "FID_INV_ALIGNER": "inv:aligner",  # Eslabón 4
    "FID_INV_SOLAR": "inv:solar", "FID_TERRITORY_HERE": "territory:here",
    "FID_TERR_NORTH": "territory:north", "FID_TERR_SOUTH": "territory:south",
    "FID_TERR_EAST": "territory:east", "FID_TERR_WEST": "territory:west",
    "FID_PROTOCOL_INPUT_OXYGEN": "protocol_input:oxygen",
    "FID_PROTOCOL_INPUT_CARBON": "protocol_input:carbon",
    "FID_PROTOCOL_INPUT_GERMANIUM": "protocol_input:germanium",
    "FID_PROTOCOL_INPUT_SILICON": "protocol_input:silicon",
    # Córtex C4/OPCIÓN-A(ii) — posición GLOBAL absoluta del agente (juego semantic/state.py):
    #   global_x(col) = lp:east − lp:west ; global_y(fila) = lp:south − lp:north.
    "FID_LP_EAST": "lp:east", "FID_LP_WEST": "lp:west",
    "FID_LP_NORTH": "lp:north", "FID_LP_SOUTH": "lp:south",
}


def _sane_world_ids(policy_env: dict) -> dict:
    """Lee los ids de tag/feature del player_config y los rebindea en TODAS las capas.
    Corrige la ceguera de aliados/rivales (tag ids machina 7/6 ≠ mundo Lab 3/2)."""
    tag_idx = {name: i for i, name in enumerate(policy_env.get("tags") or [])}
    # GEODESIA: sólidos = todos los type:* (muros/estaciones/hub/junctions/extractores) menos agent/ship.
    # LEÍDO del config (regla [doc de diseño interna, no en el repo]: nunca cablear ids). Vacío → geodesia cae a L1 (inerte).
    global _SOLID_TYPES
    _sol = {i for name, i in tag_idx.items() if name.startswith("type:") and name not in ("type:agent", "type:ship")}
    if _sol:
        _SOLID_TYPES = _sol
    fid_idx = {}
    for f in (policy_env.get("obs_features") or []):
        if isinstance(f, dict) and "name" in f and "id" in f:
            fid_idx[f["name"]] = int(f["id"])
    resolved: dict[str, int] = {}
    for const, name in _TAG_NAME.items():
        if name in tag_idx:
            resolved[const] = tag_idx[name]
    for const, name in _FID_NAME.items():
        if name in fid_idx:
            resolved[const] = fid_idx[name]

    import appraisal.appraisal_v1 as _av1
    import appraisal.appraisal_v2 as _av2
    import appraisal.appraisal_v3 as _av3
    import memoria.memoria_v1 as _m1
    mods = [_av1, _av2, _av3, _m1, sys.modules[__name__]]
    try:
        import appraisal.appraisal_v4 as _av4; mods.append(_av4)
    except Exception:
        pass
    try:
        import memoria.memoria_v2 as _m2; mods.append(_m2)
    except Exception:
        pass
    try:
        import memoria.episodica_v1 as _ep; mods.append(_ep)
    except Exception:
        pass
    try:
        import appraisal.appraisal_shelf as _ash; mods.append(_ash)  # Eslabón 1: rebind FID_INV_HEART
    except Exception:
        pass

    changed: list[str] = []
    for mod in mods:
        for const, val in resolved.items():
            if hasattr(mod, const):
                if getattr(mod, const) != val:
                    changed.append(f"{mod.__name__}.{const}:{getattr(mod,const)}->{val}")
                setattr(mod, const, val)
        if "FID_INV_ENERGY" in resolved and hasattr(mod, "FID_INV_ENERGY_P1"):
            setattr(mod, "FID_INV_ENERGY_P1", resolved["FID_INV_ENERGY"] + 1)
        if "FID_INV_HP" in resolved and hasattr(mod, "FID_INV_HP_P1"):
            setattr(mod, "FID_INV_HP_P1", resolved["FID_INV_HP"] + 1)

    # Estructuras derivadas de los tags de extractor.
    ext = frozenset(
        resolved[c] for c in (
            "TAG_TYPE_OXYGEN_EXTRACTOR", "TAG_TYPE_CARBON_EXTRACTOR",
            "TAG_TYPE_GERMANIUM_EXTRACTOR", "TAG_TYPE_SILICON_EXTRACTOR")
        if c in resolved)
    for mod in mods:
        if hasattr(mod, "EXTRACTOR_TAGS"):
            setattr(mod, "EXTRACTOR_TAGS", ext)
    if hasattr(_av3, "EXTRACTOR_TYPE_INFO"):
        info = {}
        for tc, ic, pc in (
            ("TAG_TYPE_OXYGEN_EXTRACTOR", "FID_INV_OXYGEN", "FID_PROTOCOL_INPUT_OXYGEN"),
            ("TAG_TYPE_CARBON_EXTRACTOR", "FID_INV_CARBON", "FID_PROTOCOL_INPUT_CARBON"),
            ("TAG_TYPE_GERMANIUM_EXTRACTOR", "FID_INV_GERMANIUM", "FID_PROTOCOL_INPUT_GERMANIUM"),
            ("TAG_TYPE_SILICON_EXTRACTOR", "FID_INV_SILICON", "FID_PROTOCOL_INPUT_SILICON"),
        ):
            if tc in resolved and ic in resolved and pc in resolved:
                info[resolved[tc]] = (resolved[ic], resolved[pc])
        _av3.EXTRACTOR_TYPE_INFO = info
    # v4: _MAT_FIDS es un dict derivado de los FID_* capturados en import (stale).
    # Reconstruirlo desde los fids recién resueltos en cualquier mod que lo tenga.
    for mod in mods:
        if hasattr(mod, "_MAT_FIDS"):
            rf = {}
            for x, (pc, tc, ic) in (
                ("oxygen",    ("FID_PROTOCOL_INPUT_OXYGEN",    "FID_TEAM_OXYGEN",    "FID_INV_OXYGEN")),
                ("carbon",    ("FID_PROTOCOL_INPUT_CARBON",    "FID_TEAM_CARBON",    "FID_INV_CARBON")),
                ("germanium", ("FID_PROTOCOL_INPUT_GERMANIUM", "FID_TEAM_GERMANIUM", "FID_INV_GERMANIUM")),
                ("silicon",   ("FID_PROTOCOL_INPUT_SILICON",   "FID_TEAM_SILICON",   "FID_INV_SILICON")),
            ):
                rf[x] = (
                    resolved.get(pc, getattr(mod, pc, None)),
                    resolved.get(tc, getattr(mod, tc, None)),
                    resolved.get(ic, getattr(mod, ic, None)),
                )
            setattr(mod, "_MAT_FIDS", rf)
    _log(f"[GEMV] world ids saneados desde player_config; rebinds={changed}")
    return resolved


class GEMVPlayer:
    """Minimal WebSocket player using G-EMV motor as sole decision-maker."""

    def __init__(self) -> None:
        self.slot: int = -1
        self.action_names: list[str] = []
        self.team_side: str = "cogs"
        self._step_count: int = 0
        self._deposits_done: int = 0        # cobertura v2: nº de depósitos reales (el ACTO). Token acts_done.
        self._prev_carbon: int | None = None
        if _EPISODIC == "terr":
            self.mem = EpisodicaMemoriaV1()
        else:
            self.mem = MemoriaEspacial() if USE_MEMORY else None
        if self.mem is not None and _MARCADOR:
            self.mem.marcador_mem = True   # Eslabón 4 ref.2: registrar junction-gris/gear en memoria
        if self.mem is not None and _FIXED_PERSIST:
            self.mem.fixed_persist = True  # OPCIÓN A: los fijos (gear stations) no se borran por oclusión
        if self.mem is not None and _PERSIST_GANABLE:
            self.mem.persist_ganable = True  # R1 v2: la junction ganable persiste (posición) hasta desmentido real
        if self.mem is not None and _EXTRACTOR_PERSIST:
            self.mem.extractor_persist = True  # cura eslabón: el extractor (fijo) persiste posición hasta vaciado real
        if self.mem is not None and _WALL_MEM:
            self.mem.wall_mem = True  # memoria de muros: recuerda sólidos percibidos (solid_types se fija en configure)
        if self.mem is not None and _HUB_PERSIST:
            self.mem.hub_persist = True  # pieza 1: el hub propio no se olvida (fijo persistente)
        # GEMV_COMMIT — estado del compromiso de plan VIVE EN mem (choose_action es función de módulo, no método;
        # mem persiste entre ticks). Init limpio; los getattr del bloque dan defaults si faltan. OFF ⇒ no se usa.
        if self.mem is not None:
            self.mem._commit_plan = []
            self.mem._commit_snap = None
            self.mem._commit_prevpos = None
            self.mem._commit_prevmove = False

    def configure(self, msg: dict) -> None:
        self.slot = int(msg.get("slot", -1))
        self.action_names = list(msg.get("action_names", []))

        # Sanea los ids del mundo (tag ids, feature ids) desde el player_config — NUNCA cablear.
        _sane_world_ids(msg.get("policy_env", {}))

        # Memoria de muros: fija la fuente de sólidos (config-derivada, ya saneada) en la memoria — NUNCA cablear.
        if self.mem is not None and _WALL_MEM:
            self.mem.solid_types = frozenset(_SOLID_TYPES)

        # GEMV_TEMPERAMENTS — perfil POR SLOT: rebind de los globals de ESTE proceso (cada agente es un proceso
        # aparte). w_s/w_f/W_DESPENSA de la lista _BYSLOT del slot; fuera de rango cae al valor global. OFF≡bit-exact.
        if _TEMPERAMENTS and self.slot >= 0:
            global _ACTIVE_CFG, _DESPENSA_W
            _ws = _WS_BYSLOT[self.slot] if (_WS_BYSLOT and self.slot < len(_WS_BYSLOT)) else _WS_OVERRIDE
            _wf = _WF_BYSLOT[self.slot] if (_WF_BYSLOT and self.slot < len(_WF_BYSLOT)) else _WF_OVERRIDE
            _ACTIVE_CFG = _build_active_cfg(_ws, _wf)
            if _DESPW_BYSLOT and self.slot < len(_DESPW_BYSLOT):
                _DESPENSA_W = _DESPW_BYSLOT[self.slot]
            _log(f"[GEMV] TEMPERAMENTO slot={self.slot} w_s={_ws} w_f={_wf} W_DESPENSA={_DESPENSA_W}")

        # Will be inferred at first observation; default to cogs
        self.team_side = "cogs"

        _log(f"=== PLAYER_CONFIG_START ===")
        _log(json.dumps(msg, indent=2))
        _log(f"=== PLAYER_CONFIG_END ===")
        _log(
            f"[GEMV] slot={self.slot} actions={self.action_names} "
            f"team_side={self.team_side}(provisional)"
        )

    def step(self, msg: dict) -> dict:
        step_n = int(msg.get("step", self._step_count))
        self._step_count = step_n
        tokens = msg.get("observation", [])

        # INSTRUMENTACIÓN pura (diagnóstico; NO cambia ninguna decisión): volcar tokens crudos en un step.
        if step_n == int(os.environ.get("GEMV_DUMP_TOKENS_STEP", "-1")):
            _log("GEMV_TOKENS " + json.dumps([[int(t[0]), int(t[1]), int(t[2])] for t in tokens]))
        # INSTRUMENTACIÓN pura: volcar el estado de la memoria episódica (auditoría cooperación pasiva).
        if step_n == int(os.environ.get("GEMV_DUMP_MEM_STEP", "-1")) and self.mem is not None and hasattr(self.mem, "_terr"):
            _log("GEMV_MEM " + json.dumps({
                "step": self.mem._step, "agent_world": list(self.mem._agent_world),
                "terr": [[list(k), c.territory, c.amplitude, c.last_seen_step] for k, c in self.mem._terr.items()],
            }))

        if not self.action_names:
            return {"type": "action", "action_name": "noop",
                    "request_id": f"step-{step_n}"}

        # Infer team_side from first observation (self tags at AGENT_LOC)
        if step_n == 0:
            _, tag_map = parse_tokens(tokens)
            self_tags = tag_map.get(AGENT_LOC, set())
            if TAG_TEAM_CLIPS in self_tags:
                self.team_side = "clips"
            elif TAG_TEAM_COGS in self_tags:
                self.team_side = "cogs"
            if self.mem is not None:
                self.mem.reset()
            self._deposits_done = 0        # reinicio por episodio (spec §1: saldo por acto, per episodio)
            self._prev_carbon = None

        # 1e: RUTAR la demanda derivada a TODOS los consumidores — sobrescribir los tokens protocol_input
        # con max(0, HEART_COST − team_held) por elemento. Drop-in: v3 (w_mat, _wealth_mat) y v4 la leen
        # igual que la inyectada. Una vez, antes de todo. Gateado por team_held (candado de frontera intacto).
        if _DEMAND_ROUTED and _APPRAISAL == "4":
            _rsm, _ = parse_tokens(tokens)
            from appraisal.appraisal_v4 import _MAT_FIDS as _mfid, HEART_COST as _hc
            _proto_vals = {}
            for _x, (_pf, _tf, _if) in _mfid.items():
                _proto_vals[int(_pf)] = max(0, _hc - get_scalar(_rsm, GLOBAL_LOC, _tf))
            _present = {int(f) for (l, f, v) in tokens if int(l) == GLOBAL_LOC and int(f) in _proto_vals}
            tokens = [((l, f, _proto_vals[int(f)]) if (int(l) == GLOBAL_LOC and int(f) in _proto_vals) else (l, f, v))
                      for (l, f, v) in tokens]
            tokens = list(tokens) + [(GLOBAL_LOC, pf, pv) for pf, pv in _proto_vals.items() if pf not in _present]

        # Apply synthetic deficit injection if active (TEST MODE)
        real_sm, _ = parse_tokens(tokens)
        real_hp     = get_multipart(real_sm, AGENT_LOC, FID_INV_HP)
        real_energy = get_multipart(real_sm, AGENT_LOC, FID_INV_ENERGY)
        tokens, injected, eff_hp, eff_energy = _apply_injection(
            tokens, step_n, real_hp, real_energy
        )

        # Cobertura v2 — detectar DEPÓSITO real: el TOTAL de elementos del agente baja (único sumidero =
        # depositar en el hub). Cada bajada = un ACTO ("hice mi parte"). Se inyecta acts_done para appraise.
        # Generalizado a todos los elementos (competidor 1b), no solo carbon.
        if _COVERAGE == "v2_hybrid":
            cur_elems = sum(get_multipart(real_sm, AGENT_LOC, f) for f in _element_inv_fids())
            if self._prev_carbon is not None and cur_elems < self._prev_carbon:
                self._deposits_done += 1
            self._prev_carbon = cur_elems
            tokens = list(tokens) + [(AGENT_LOC, _FID_ACTS_DONE, self._deposits_done)]

        # UTILLAJE DE SALIDA (test harness): durante el bootstrap se FUERZA la acción de salida.
        # Secuencia multi-tramo (Fase 4) tiene prioridad sobre la dirección única (Fase 3c).
        forced = None
        if _BOOTSTRAP_SEQ and step_n < len(_BOOTSTRAP_SEQ):
            forced = _BOOTSTRAP_SEQ[step_n]
        elif step_n < _BOOTSTRAP_STEPS:
            forced = _BOOTSTRAP_DIR
        force_noop_now = _FORCE_NOOP and "noop" in self.action_names

        if force_noop_now:
            # Filler pasivo: slots no-sujeto siempre noop (aliados/clips apostados y visibles).
            action = "noop"
            debug = {"action": "noop", "force_noop": True}
        elif forced is not None and forced in self.action_names:
            # Bootstrap: NO se PLANIFICA (evita que el plan lento a H alto dispare el timeout del
            # servidor). PERO la memoria SÍ observa y avanza odometría (barato): el agente cruza
            # su propio territorio durante el utillaje y DEBE grabarlo (si no, no hay casa recordada).
            action = forced
            _sm, _tm = parse_tokens(tokens)
            debug = {"action": action, "bootstrap": True,
                     "raw": {"territory": get_scalar(_sm, GLOBAL_LOC, FID_TERRITORY_HERE),
                             "hp": get_multipart(_sm, AGENT_LOC, 20),
                             "energy": get_multipart(_sm, AGENT_LOC, FID_INV_ENERGY)}}
            if self.mem is not None:
                _s, _appr = appraise_with_debug(tokens, self.team_side, s_scale=S_SCALE)
                _appr["d"] = opponent_distance(_s, _ACTIVE_CFG)
                self.mem.observe(_appr, _sm, _tm, self.team_side)
                self.mem.step_tick(action, _dest_is_blocked(_tm, action))
                debug["_mem_stepped"] = True
        else:
            action, debug = choose_action(tokens, self.action_names, self.team_side, mem=self.mem,
                                          world_step=step_n, slot=self.slot)

        if self.mem is not None and "preds" in debug:
            blocked = debug["preds"].get(action, {}).get("blocked", False)
            self.mem.step_tick(action, blocked)

        if injected:
            debug["test_inject"] = {
                "real_hp": real_hp, "eff_hp": eff_hp,
                "real_energy": real_energy, "eff_energy": eff_energy,
            }

        # Compact human log (solo si hay estado completo; en bootstrap se omite).
        if "state" in debug and "preds" in debug:
            s = debug["state"]
            r = debug["raw"]
            terr_sym = {0: "N", 1: "P", 2: "R"}.get(r["territory"], "?")
            pred_str = "  ".join(
                f"{a[0] if a != 'noop' else 'o'}→{debug['preds'][a]['d']:.3f}"
                for a in self.action_names if a in debug["preds"]
            )
            _log(
                f"[GEMV] step={step_n:5d} | hp={r['hp']:3d} en={r['energy']:3d} "
                f"tr={terr_sym} al={r.get('allies')} ri={r.get('rivals')} | "
                f"pF={s['pF']:.2f} nF={s['nF']:.2f} pR={s['pR']:.2f} "
                f"nR={s['nR']:.2f} pS={s['pS']:.2f} nS={s['nS']:.2f} "
                f"d={debug['d_curr']:.3f} | preds: {pred_str} | >{action}"
            )

        # Dump legible del registro episódico (gate G2).
        if _EPISODIC == "terr" and step_n == _EPISODIC_DUMP_STEP and self.mem is not None:
            _log("GEMV_EPDUMP " + json.dumps({
                "step": step_n, "stats": self.mem.stats(),
                "movie": self.mem.dump_movie(4)}))

        # Machine-readable line for B-criteria analysis
        inject_info = debug.pop("test_inject", False)
        tick_log = {"step": step_n, "test_inject": inject_info}
        tick_log.update(debug)
        _log(f"GEMV_TICK {json.dumps(tick_log)}")

        return {"type": "action", "action_name": action,
                "request_id": f"step-{step_n}"}


async def run_player(*, player_ws_url: str) -> None:
    player = GEMVPlayer()
    # El planner síncrono (H≥2) bloquea el loop asyncio en ticks pesados (n_terminal ~100K a H=8 → >20s); con
    # el loop bloqueado, websockets no puede responder los PINGS del servidor → éste cierra con 1011 keepalive
    # en un tick ALEATORIO (el agente caía entre step 432 y 1426 al azar). FIX: el step() corre en un THREAD
    # EXECUTOR → el loop asyncio queda LIBRE para auto-responder los pings (pong) durante el cómputo → la
    # conexión sobrevive los 2500 ticks. Es SECUENCIAL (se await cada step antes de leer el siguiente mensaje):
    # cero concurrencia sobre el estado del player → conducta BIT-IDÉNTICA (solo cambia el HILO donde corre).
    # max_size=None por observaciones grandes.
    loop = asyncio.get_running_loop()
    async with websockets.connect(player_ws_url, ping_interval=None, ping_timeout=None,
                                  close_timeout=15, max_size=None) as ws:
        async for raw in ws:
            msg = json.loads(raw)
            mtype = msg.get("type")
            if mtype == "player_config":
                player.configure(msg)
            elif mtype == "observation":
                action_msg = await loop.run_in_executor(None, player.step, msg)  # planner fuera del loop
                await ws.send(json.dumps(action_msg))
            elif mtype == "final":
                _log(f"[GEMV] slot={player.slot} episodio terminado step={player._step_count}")
                return


def main() -> None:
    # FIX velocidad del thread-executor: por defecto Python cambia de hilo cada 5ms (getswitchinterval=0.005),
    # así que en un tick del planner de varios segundos hay cientos de context-switches planner↔loop (coste que
    # triplicaba el tiempo/tick: ~7→2.5 steps/min). Subir a 100ms → ~20× menos switches → el planner recupera
    # velocidad; los pongs del keepalive siguen saliendo cada ≤100ms (holgadísimo para el timeout de 20s del
    # servidor). NO cambia ninguna decisión (solo el scheduling de hilos). OFF-equivalente si no hubiera executor.
    sys.setswitchinterval(0.1)
    _log(f"GEMV_POLICY_STARTED switchinterval={sys.getswitchinterval()}")
    _log(f"[GEMV] USE_MEMORY={USE_MEMORY} mem_version={_MEM_VERSION} s_scale={S_SCALE} "
         f"horizon={_HORIZON} plan_cache={_PLAN_CACHE}")
    _log(f"[GEMV] SHELF={_GEMV_SHELF} pantry_mem={_PANTRY_MEM} appraisal={_APPRAISAL} "
         f"demand_routed={_DEMAND_ROUTED} virtual_extract={_VIRTUAL_EXTRACT} transition={_TRANSITION_ON}")
    if _INJECT_HP >= 0 or _INJECT_ENERGY >= 0:
        _log(
            f"[GEMV] *** TEST_INJECT_MODE *** "
            f"hp={_INJECT_HP}(delay={_INJECT_HP_DELAY},steps={_INJECT_STEPS}) "
            f"energy={_INJECT_ENERGY}(steps={_INJECT_ENERGY_STEPS}) "
            f"s_scale={S_SCALE} -- déficit sintético, NO parte del appraisal"
        )
    url = os.environ.get("COWORLD_PLAYER_WS_URL")
    if not url:
        _log("ERROR: COWORLD_PLAYER_WS_URL no definida")
        sys.exit(1)
    _log(f"GEMV_CONNECTING url={url}")
    asyncio.run(run_player(player_ws_url=url))


if __name__ == "__main__":
    main()

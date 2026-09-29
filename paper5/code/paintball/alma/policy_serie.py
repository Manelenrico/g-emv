"""POLICY_SERIE — la policy de las series privadas del paper cuatro. [13-sep-2026]

Copia de `policy.py` con TRES anadidos y ningun cambio de conducta salvo el
appraisal que importa:

  1. IMPORTA `appraisal_zs_v40_exp` en vez de `appraisal_zs`. Con los
     interruptores apagados (lo de por defecto) v40 ES v37 byte a byte:
     comprobado en las doce pruebas del que va solo (12/12 identicas), en las
     siete escenas de smoke_alma (0 cambios) y en 1.605 tics de campo
     reconstruidos (0 diferencias de d a 1e-12).

  2. GRABA LO QUE EL DIARIO NO GUARDABA, como `policy_mapa.py`: el `static_map`
     y el `catalogo` al recibir el player_config y REEMITIDOS cada
     REEMISION_CADA tics; y por tic `attack_ready_in`, `move_ready_in` y
     `action_result`. Motivo: la plataforma corta el diario por la cabeza, y
     la arena es DISTINTA en cada episodio (medido: de 14 arbustos que la 66
     vio, solo 2 estan en el mapa de otra partida; y 15 casillas que la 66
     descubrio solidas a golpes son pisables en ese otro mapa).

  3. RADIOGRAFIA LIGERA Y RECORTADA. Cada tic va: la d de TODOS los candidatos,
     el elegido, `honor`, las filas del presente CON M > 0 (una fila ausente es
     una fila en cero) y, si MIEDO_ON, el valor de MIEDO_APRENDIDO y el detalle
     `_det_ma` de la amenaza. NO van `fuerzas_crudas`, `fuerzas_state` ni
     `W_desglose`: ninguna prediccion los usa y se recalculan del State.
     El detalle completo por candidato (pos_prevista, hp_prevista, filas) va
     cada DETALLE_CANDIDATOS_CADA = 24 tics.

LA MEMORIA ES FIJA Y NO SE ESCRIBE. La carga `appraisal_zs_v40_exp._carga_memoria()`
una sola vez al importar, desde GEMV_MEMORIA, y solo para leer. En las tandas 1
y 2 el agente NO aprende en vivo. Aqui no hay ninguna escritura a ese fichero.

LAS TRES TANDAS, por entorno (ver la cabecera de v40):
  1 base    sin ENV
  2 miedo   GEMV_MIEDO=1 GEMV_MEMORIA=/app/alma/memoria_aprendida_p95.json
  3 ajena   ademas GEMV_VIDA_AJENA=1 GEMV_VIDA_AJENA_M=0.25
"""
from __future__ import annotations

import asyncio
import json
import math
import os
import sys
import time

import websockets

from motor.model import DEFAULT_CONFIG, opponent_distance
from alma.mundo import Mundo
from alma import appraisal_zs_v40_exp as A
from alma import decisor_zs as D
from alma import parte as PARTE

# ── EL CABLEADO [S-3, Manel] ────────────────────────────────────────────────
# `decisor_zs.py:39` importa `appraisal_zs` (v37) y con el valora los CANDIDATOS
# en su linea 882. Sin esta asignacion, la fila encendida aqui solo entraba en
# la foto del presente (linea ~138) y NO en la decision: medido en `serie_miedo`,
# MIEDO_APRENDIDO = 0.00000 en los 2.370 candidatos de B. Con ella, el decisor
# valora los candidatos con el MISMO appraisal que esta policy.
D.A = A

# constitucion sellada por Manel
CONSTITUCION = {"intelligence": 8, "athleticism": 6, "speed": 5, "strength": 1}
assert sum(CONSTITUCION.values()) == 20

# ── ETAPA A (PROMPT_04): EMISOR DIRIGIDO POR OBSERVACION ─────────────────────
# El repetidor de reloj a 30 Hz se retira. Motivo medido en el 03: enviaba de
# forma asincrona respecto al tick del mundo, asi que CUAL de los reenvios caia
# dentro de la ventana de cada tick era una carrera de reloj de pared -> dos
# imagenes con el mismo codigo podian divergir ya en el primer movimiento.
#
# Ahora: al recibir cada observacion se decide y se emite EXACTAMENTE UNA VEZ.
# Nuestra accion para el tick T pasa a ser funcion determinista del flujo de
# observaciones hasta T. Se decide en CADA observacion (el prompt lo autoriza):
# con 3 ms por decision cabe 13 veces en el fotograma de 41,7 ms, y elimina el
# estado `ultimo_decidido` y el acarreo de intencion entre decisiones.
EMISION = "una_por_observacion"
VIGIA_S = 1.0                  # respaldo: si el flujo se corta > 1 s, reenvia
VOZ_CADA = 48                  # 2 s: el ping de equipo de la tabla
REEMISION_CADA = 100           # [MAPA] cada cuantos tics se REEMITEN el mapa y
                               # el catalogo. 2000 NO basto: en la primera
                               # partida (ereq_3c1171bb) la plataforma dejo
                               # ventanas de 631 y 368 tics y ningun multiplo
                               # de 2000 cayo dentro.
DETALLE_CANDIDATOS_CADA = 24   # [SERIE] 24, no 12: el detalle completo es lo
                               # mas caro del diario y con 24 basta para el forense.
                               # [impl] cada cuantos tics se guarda el detalle
                               # completo de todos los candidatos (el resto de
                               # tics guarda la radiografia sin ese detalle)
NONE_ACTION = {"type": "action", "do": "none"}


def log(rec):
    sys.stdout.write(json.dumps(rec, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def banda(hp, hp_max):
    if hp_max <= 0:
        return "?"
    f = 100.0 * hp / hp_max
    return "healthy" if f > 66 else ("hurt" if f > 33 else "critical")


class Alma:
    def __init__(self):
        self.mundo = None
        self.mem = A.Memoria()
        self.intent = dict(NONE_ACTION)
        self.tick = -1
        self.phase = "countdown"
        self.enviados = 0
        self.decisiones = 0
        self.ultima_voz = -10 ** 9
        self.ultimo_obs_wall = 0.0
        self.reenvios_vigia = 0
        self.emitidos = 0
        self.bloqueos = D.Bloqueos()
        self.ultima_accion = None
        self.tiempos_ms = []
        self.done = asyncio.Event()
        self.hitos = []

    def decidir(self, obs):
        """Ciclo real. Devuelve (accion, radiografia|None)."""
        self.tick = obs.get("tick", self.tick)
        self.phase = obs.get("phase", self.phase)
        self.mem.observa(obs, self.mundo, self.tick)
        # ARREGLO A: leer el feedback del mundo ANTES de elegir
        self.bloqueos.actualiza(obs, self.mundo, self.ultima_accion, self.tick)

        # cuenta atras: quieto en el pedestal. NO es inteligencia: salir antes de
        # la ignicion es muerte instantanea por mina (regla dura del mundo).
        if self.phase != "live":
            return dict(NONE_ACTION), None

        t0 = time.perf_counter()
        accion, radio = D.decide(obs, self.mundo, self.mem, self.tick, self.bloqueos)
        ms = (time.perf_counter() - t0) * 1000.0
        self.tiempos_ms.append(ms)
        self.decisiones += 1
        # el detalle de todos los candidatos solo cada N tics (tamano del log)
        if self.tick % DETALLE_CANDIDATOS_CADA != 0:
            radio["candidatos"] = {k: v["d"] for k, v in radio["candidatos"].items()}

        st, radio_ap = A.appraise(obs, self.mundo, self.mem, self.tick)
        radio["ms"] = round(ms, 3)
        # [SERIE] RECORTE del presente. Se conserva todo lo que las predicciones
        # D1-D8 miran; se quita lo que solo servia para el forense fino y se
        # puede recalcular del State. Una fila AUSENTE es una fila en CERO.
        radio_ap = {k: v for k, v in radio_ap.items()
                    if k not in ("fuerzas_crudas", "fuerzas_state", "W_desglose")}
        radio_ap["filas"] = {k: v for k, v in (radio_ap.get("filas") or {}).items()
                             if (v or {}).get("M")}
        radio["ahora"] = radio_ap                    # la radiografia del PRESENTE
        radio["d_ahora"] = round(opponent_distance(st, DEFAULT_CONFIG), 5)
        return accion, radio

    def _social(self, obs):
        """Diagnostico social por decision (PROMPT_10). Solo REGISTRA: no toca
        ninguna fila ni ninguna decision.

        Nota declarada: `solto` es siempre None porque NO existe candidato de
        soltar en el set (nunca se anadio). Se registra igual para que el dato
        diga que la casilla existe y esta vacia, en vez de callar.
        """
        you = obs.get("you") or {}
        vis = obs.get("visible") or {}
        m, mu = self.mem, self.mundo
        pos = tuple(you.get("pos") or (0, 0))
        pareja = next((a for a in (vis.get("agents") or [])
                       if a.get("slot") == mu.teammate_slot), None)
        oidos = [c for c in (obs.get("chat") or [])
                 if c.get("from") == mu.teammate_slot and c.get("channel") == "team"]
        cogido = None
        if (self.ultima_accion or {}).get("do") == "pickup" \
                and you.get("action_result") == "ok":
            cogido = "pickup_ok"
        return {"B": round(m.roce_B, 4),
                "P": m.presencia(obs, mu, self.tick),
                "pareja_vista": pareja is not None,
                "pareja_pos": pareja.get("pos") if pareja else None,
                "dist_pareja": (round(math.dist(pos, tuple(pareja["pos"])), 3)
                                if pareja else None),
                "pareja_pos_recordada": list(m.pareja_pos) if m.pareja_pos else None,
                "pareja_banda": m.pareja_banda,
                "pareja_muerta": m.pareja_muerta,
                "sin_compania_ticks": m.ticks_sin_compania,
                "ping_emitido": self.tick == self.ultima_voz,
                "pings_oidos": oidos,
                "cogio": cogido,
                "solto": None,
                "agresores_activos": sorted(m.agresores.keys())}

    def registrar(self, obs, radio):
        you = obs.get("you") or {}
        vis = obs.get("visible") or {}
        rec = {"k": "tick", "tick": obs.get("tick"), "phase": obs.get("phase"),
               "pos": you.get("pos"), "hp": you.get("hp"),
               "hand": you.get("hand"), "body": you.get("body"),
               "pack": you.get("pack"), "effects": you.get("effects"),
               "action_result": you.get("action_result"),
               "move_ready_in": you.get("move_ready_in"),
               "kills": you.get("kills"), "damage_dealt": you.get("damage_dealt"),
               "damage_taken": you.get("damage_taken"),
               "zona": obs.get("zone"),
               # PROMPT_41 — FONTANERIA: el cable entero al diario. La espec
               # (protocol_player.md:56-63) publica hand/body/netted/poisoned/
               # channeling de otros y projectiles[] con `shooter` — el UNICO
               # autor cierto de todo el protocolo (acta del 40). Hasta ahora
               # el diario los tiraba. Solo ANADE visibilidad: el alma recibe
               # la obs CRUDA y no lee estos campos (gate de neutralidad en
               # verifica_41: bit-identico antes/despues, 3/3).
               "ve_agentes": [{"slot": a.get("slot"), "team": a.get("team"),
                               "pos": a.get("pos"), "hp_band": a.get("hp_band"),
                               "hand": a.get("hand"), "body": a.get("body"),
                               "netted": a.get("netted"),
                               "poisoned": a.get("poisoned"),
                               "channeling": a.get("channeling")}
                              for a in vis.get("agents") or []],
               "ve_items": vis.get("items", []), "ve_bushes": vis.get("bushes", []),
               "ve_proyectiles": vis.get("projectiles", []),
               "eventos": obs.get("events", []), "chat": obs.get("chat", []),
               "intencion": self.intent,
               "B": round(self.mem.roce_B, 4),
               "sin_compania_ticks": self.mem.ticks_sin_compania,
               "pareja_muerta": self.mem.pareja_muerta,
               "social": self._social(obs),
               # [MAPA] los tres campos que el diario normal no guarda
               "attack_ready_in": you.get("attack_ready_in"),
               "move_ready_in_obs": you.get("move_ready_in"),
               "action_result_obs": you.get("action_result")}
        # [SERIE] RADIOGRAFIA LIGERA. Cada tic va lo barato y lo que las
        # predicciones necesitan; el detalle por candidato ya viene recortado
        # de `decidir()` (DETALLE_CANDIDATOS_CADA).
        if radio is not None:
            rec["RADIOGRAFIA"] = radio
            if A.MIEDO_ON:
                ah = radio.get("ahora") or {}
                fl = ah.get("filas") or {}
                rec["MIEDO"] = (fl.get("MIEDO_APRENDIDO") or {}).get("M", 0.0)
                rec["MIEDO_DET"] = ah.get("_miedo_aprendido")
        log(rec)
        # [MAPA] 4 — REEMISION cada 2.000 tics. Motivo: la plataforma corta el
        # diario por ARRIBA (paper tres, acta de cobertura: 20 de 80 diarios de
        # la 66 perdieron el arranque, uno de cada cuatro). Si el mapa solo
        # viajara en el player_config, se perderia con la cabeza. 48 filas cada
        # 2.000 tics son ~4 copias por partida y ~10 kB: despreciable.
        if self.tick % REEMISION_CADA == 0:
            _m = getattr(self, "_mapa_rec", None)
            if _m:
                log(dict(_m, reemision=True, tick=self.tick))
            _c = getattr(self, "_catalogo_rec", None)
            if _c:
                log(dict(_c, reemision=True, tick=self.tick))


async def vigia(ws, alma: Alma):
    """WATCHDOG declarado: SOLO actua si el flujo de observaciones se corta.

    En un episodio sano no debe dispararse nunca (se cuenta y se reporta: si
    `reenvios_vigia` > 0, la corrida NO es comparable). No es un repetidor: no
    emite mientras lleguen observaciones.
    """
    while not alma.done.is_set():
        await asyncio.sleep(VIGIA_S)
        if alma.ultimo_obs_wall and (time.monotonic() - alma.ultimo_obs_wall) > VIGIA_S:
            try:
                await ws.send(json.dumps(alma.intent))
                alma.reenvios_vigia += 1
                log({"k": "vigia_disparo", "tick": alma.tick,
                     "silencio_s": round(time.monotonic() - alma.ultimo_obs_wall, 3)})
            except Exception:
                return


async def decisor(ws, alma: Alma):
    async for raw in ws:
        try:
            msg = json.loads(raw)
        except Exception:
            continue
        t = msg.get("type")

        if t == "player_config":
            alma.mundo = Mundo.desde_player_config(msg)
            # [MAPA] 1 — EL MAPA, DENTRO DEL DIARIO. Es lo unico que se
            # descarga con seguridad: el fichero de abajo puede perderse con el
            # contenedor si no hay volumen montado. 48 filas de 48 -> ~2,4 kB,
            # despreciable frente a los ~5 MB de un diario.
            _arena = msg.get("arena") or {}
            alma._mapa_rec = {"k": "static_map",
                              "size": _arena.get("size"),
                              "legend": _arena.get("legend"),
                              "pedestals": _arena.get("pedestals"),
                              "filas": list(_arena.get("static_map") or [])}
            log(dict(alma._mapa_rec))
            # [MAPA] 2 — EL CATALOGO ENTERO (cooldown, damage, range por item),
            # tambien dentro del diario.
            alma._catalogo_rec = {"k": "catalogo", "items": msg.get("items") or [],
                                  "stats": msg.get("stats"),
                                  "freeze": msg.get("freeze")}
            log(dict(alma._catalogo_rec))
            # [MAPA] 3 — y ademas el player_config ENTERO a fichero, por si hay
            # volumen montado. Si no lo hay, se registra y se sigue: la partida
            # NO se cae por esto y el mapa ya va en el diario.
            _p = None
            try:
                _d = os.environ.get("MAPA_DIR",
                                    os.path.join(os.getcwd(), "runs_mapa"))
                os.makedirs(_d, exist_ok=True)
                _e = os.environ.get("EREQ", "sin_ereq")
                _p = os.path.join(_d, f"player_config_{_e}_{msg.get('slot')}.json")
                with open(_p, "w", encoding="utf-8") as _f:
                    json.dump(msg, _f, ensure_ascii=False)
            except Exception as _ex:           # nunca tumbar la partida por esto
                log({"k": "mapa_error", "error": repr(_ex), "ruta": _p})
            else:
                log({"k": "mapa_volcado", "ruta": _p,
                     "filas_static_map": len(_arena.get("static_map") or []),
                     "n_items": len(msg.get("items") or [])})
            log({"k": "player_config", "slot": alma.mundo.slot, "team": alma.mundo.team,
                 "teammate_slot": alma.mundo.teammate_slot,
                 "protocol": msg.get("protocol"), "tick_rate": alma.mundo.tick_rate,
                 "max_ticks": alma.mundo.max_ticks,
                 "ignition_tick": alma.mundo.ignition_tick,
                 "zone_schedule": alma.mundo.zone_schedule})
            log({"k": "mundo_leido",
                 "avisos": alma.mundo.avisos,
                 "id_botiquin": alma.mundo.id_botiquin,
                 "id_raciones": list(alma.mundo.id_raciones),
                 "id_mochila": alma.mundo.id_mochila,
                 "id_camuflaje": alma.mundo.id_camuflaje,
                 "id_red": alma.mundo.id_red,
                 "dmg_ref": alma.mundo.dmg_ref,
                 "ammo_ids": list(alma.mundo.ammo_ids),
                 "solidos": sorted(alma.mundo.ch_wall | alma.mundo.ch_fortress),
                 "camara_celdas": len(alma.mundo.camara),
                 "bocas_celdas": len(alma.mundo.bocas),
                 "bocas": sorted(alma.mundo.bocas)})
            await ws.send(json.dumps({"type": "allocate_stats", **CONSTITUCION}))
            log({"k": "allocate_enviado", "payload": CONSTITUCION})

        elif t == "alloc_result":
            log({"k": "alloc_result", "applied": msg.get("applied"),
                 "defaulted": msg.get("defaulted"), "rejected": msg.get("rejected")})

        elif t == "observation":
            alma.ultimo_obs_wall = time.monotonic()
            accion, radio = alma.decidir(msg)
            alma.intent = accion
            # EMISION: exactamente una por observacion, inmediatamente.
            await ws.send(json.dumps(accion))
            alma.emitidos += 1
            alma.ultima_accion = accion
            alma.registrar(msg, radio)
            # VOZ (PROMPT_53): EL PARTE DE ESTADO sustituye al latido del 32.
            # Cada 48 tics (>= 1/24: jamas rate_limited), ASCII <=120,
            # determinista dado el estado. Formato en alma/parte.py.
            if (alma.phase == "live" and alma.mundo
                    and alma.tick - alma.ultima_voz >= VOZ_CADA):
                texto = PARTE.emite(
                    msg, alma.tick, alma.mundo, alma.mem,
                    int(A.AGRESOR_VENTANA_S * alma.mundo.tick_rate))
                await ws.send(json.dumps({"type": "talk", "channel": "team",
                                          "text": texto}))
                alma.ultima_voz = alma.tick
                log({"k": "voz", "tick": alma.tick, "texto": texto})

        elif t == "final":
            ms = sorted(alma.tiempos_ms)
            log({"k": "final", "placement": msg.get("placement"),
                 "kills": msg.get("kills"), "score": msg.get("score"),
                 "reason": msg.get("reason"), "match_ticks": msg.get("match_ticks"),
                 "decisiones": alma.decisiones,
                 "emitidos": alma.emitidos,
                 "tics_cooldown": alma.bloqueos.tics_cooldown,
                 "tics_congelado": alma.bloqueos.tics_congelado,
                 "reenvios_vigia": alma.reenvios_vigia,
                 "cadencia_ms": {
                     "n": len(ms),
                     "mediana": round(ms[len(ms) // 2], 3) if ms else None,
                     "p95": round(ms[int(len(ms) * 0.95)], 3) if ms else None,
                     "max": round(ms[-1], 3) if ms else None},
                 "B_final": round(alma.mem.roce_B, 4),
                 "pareja_muerta": alma.mem.pareja_muerta})
            alma.done.set()
            return


async def run(url):
    alma = Alma()
    t0 = time.time()
    log({"k": "arranque", "constitucion": CONSTITUCION,
         "emision": EMISION, "vigia_s": VIGIA_S,
         "mirada_min_ticks": D.H_MIRADA_MIN, "voz_cada_ticks": VOZ_CADA})
    async with websockets.connect(url, ping_timeout=None) as ws:
        rep = asyncio.create_task(vigia(ws, alma))
        try:
            await decisor(ws, alma)
        finally:
            alma.done.set()
            rep.cancel()
            try:
                await rep
            except asyncio.CancelledError:
                pass
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})


if __name__ == "__main__":
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL")
                    or os.environ["COGAMES_ENGINE_WS_URL"]))

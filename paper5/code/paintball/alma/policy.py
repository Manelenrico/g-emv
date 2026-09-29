"""EL ALMA — traductor arcilla para zero-sum 0.1.18.

El esqueleto del PROMPT_02 con el rumbo aleatorio SUSTITUIDO por el ciclo real:
    appraisal (tabla de signos v1) -> candidatos -> evaluacion con motor/model.py
    -> desempate de la casa -> intencion al repetidor.

Se conserva intacta la arquitectura validada en el 02:
  HILO REPETIDOR : reenvia la intencion vigente a 30 Hz (zero-sum limpia
                   pendingSet cada tick: si callas, el agente se para).
  DECISOR        : ahora tiene alma.

VOZ: ping por canal `team` cada 2 s con mensaje fijo (posicion + banda de hp).
     El canal team esta CERTIFICADO en 0.1.18 (PROMPT_02): llega solo a la pareja.

REGISTRO: una linea JSON por tick; en los ticks de decision, la RADIOGRAFIA
completa (M de cada fila, reparto por eje, fuerzas crudas y del State, d de cada
candidato). Es la materia de forense y atribucion.
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
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma import parte as PARTE

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
DETALLE_CANDIDATOS_CADA = 12   # [impl] cada cuantos tics se guarda el detalle
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
               "social": self._social(obs)}
        if radio is not None:
            rec["RADIOGRAFIA"] = radio
        log(rec)


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

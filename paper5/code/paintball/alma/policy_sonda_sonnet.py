"""POLICY_CORTEX — el cuerpo del banco con un CORTEX que propone. [L-4, 14-sep-2026]

Copia de `policy_serie.py` con dos cambios y ninguno mas:

  1. EL CUERPO ES EL DEL BANCO: `appraisal_zs_v42_exp` con EMPATIA_ON,
     H_PREV 0,25, H_GOLPE 1,0, y el miedo y el extrano APAGADOS. Es el mismo
     cuerpo que juzgo el t3, el t4 y el t5.

  2. EL CORTEX (`alma/cortex_t5.py`), en un hilo aparte: cada
     GEMV_CORTEX_CADA tics toma una foto, arma el relato con el relator del
     banco t5 BYTE A BYTE (`alma/relator_t5.py`), llama al sidecar de Bedrock
     y devuelve propuestas. Cada propuesta se traduce a una receta y se INYECTA
     en la lista de candidatos con la misma envoltura del banco: `D.candidatos`
     envuelto DESDE FUERA. `decisor_zs.py` NO SE TOCA.

     SIN NINGUNA VENTAJA. La propuesta compite con las del cuerpo en igualdad:
     gana la de `d` menor. Si el sidecar falla tres veces seguidas, el cortex
     calla y el cuerpo sigue solo. Ninguna llamada bloquea el bucle: la foto se
     deja en una cola y el hilo la recoge.

  Interruptores: GEMV_CORTEX (0/1) · GEMV_CORTEX_CUERPO (0/1) ·
  GEMV_CORTEX_MANUAL (M2/M1/none) · GEMV_CORTEX_CADA (por defecto 50).

--- cabecera original de policy_serie.py ---

POLICY_SERIE — la policy de las series privadas del paper cuatro. [13-sep-2026]

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
import copy
import json
import math
import os
import sys
import threading
import time

import websockets

from motor.model import DEFAULT_CONFIG, opponent_distance
from alma.mundo import Mundo
from alma import appraisal_zs_v42_exp as A
from alma import cortex_t5 as CX
from alma import relator_t5 as RT
from alma import decisor_zs as D
from alma import parte as PARTE

# ── EL CABLEADO [S-3, Manel] ────────────────────────────────────────────────
# `decisor_zs.py:39` importa `appraisal_zs` (v37) y con el valora los CANDIDATOS
# en su linea 882. Sin esta asignacion, la fila encendida aqui solo entraba en
# la foto del presente (linea ~138) y NO en la decision: medido en `serie_miedo`,
# MIEDO_APRENDIDO = 0.00000 en los 2.370 candidatos de B. Con ella, el decisor
# valora los candidatos con el MISMO appraisal que esta policy.
# [L-4] EL CUERPO DEL BANCO, fijado aqui y no por entorno: v42_exp con
# empatia 0,25/1,0 y el miedo y el extrano apagados. Es el del t3/t4/t5.
A.EMPATIA_ON = True
A.H_PREV, A.H_GOLPE = 0.25, 1.0
A.MIEDO_ON = False
A.VIDA_AJENA_ON = False
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


# ── [L-7] EL MISMO VETO QUE EL CUERPO ───────────────────────────────────────
# `candidatos()` filtra los SUYOS por `Bloqueos.veta` (decisor_zs.py:602-606), y
# `veta` despacha por el PREFIJO DEL NOMBRE (decisor_zs.py:94-102). Nuestros
# nombres (`_CX_ir_24_24`) no empiezan por `ir_`, asi que se colaban enteros:
# en la L-6 una propuesta de andar seguia en la mesa con las piernas enfriando,
# cuando todos los `move_*`, `paso_*` e `ir_*` del cuerpo ya estaban fuera. Aqui
# se le pasa a `veta` el nombre del PROPIO vocabulario del cuerpo para ese tipo
# de receta, de modo que la regla es literalmente la misma.
_VETO_POR_TIPO = {"ir": "ir_", "mover": "move_", "paso": "paso_",
                  "atacar": "atacar_", "usar": "usar_", "empunar": "empunar_",
                  "ponerse": "ponerse_"}


def _filas_entre(rad, a, b):
    """[D-C] Las tres filas que mas separan al candidato `a` del `b`, con el
    signo desde el punto de vista de `a`. Es la misma vara que ya usaba
    `pierde_por`, sacada aparte para poder usarla en los dos sentidos."""
    ca = (rad["candidatos"].get(a) or {}).get("filas") or {}
    cb = (rad["candidatos"].get(b) or {}).get("filas") or {}
    dif = {k: round(ca.get(k, 0.0) - cb.get(k, 0.0), 5)
           for k in set(ca) | set(cb)
           if abs(ca.get(k, 0.0) - cb.get(k, 0.0)) > 1e-9}
    return sorted(dif.items(), key=lambda kv: -abs(kv[1]))[:3] if dif else None


def _segundo(propios, n):
    """[D-C] El SEGUNDO mejor candidato propio del cuerpo, sin contar `n`.
    None si `n` era la unica opcion que el cuerpo tenia."""
    otros = {k: v for k, v in propios.items() if k != n}
    return min(otros, key=otros.get) if otros else None


def _veta_receta(bloqueos, receta, obs, tick):
    if bloqueos is None:
        return False
    pre = _VETO_POR_TIPO.get((receta or {}).get("tipo"))
    return bool(pre) and bloqueos.veta(pre + "X", obs, tick)


# ── [D-M2 punto 3] SONDA DEL SIDECAR CON SONNET ─────────────────────────────
# Copia de `policy_cortex.py` (f54e686e) con UN anadido y nada mas: antes de la
# primera cita, se le pregunta al sidecar por hasta TRES identificadores de
# Sonnet, del mas reciente al menos, y se usa el primero que conteste. El error
# literal de los que fallen se graba. `policy_cortex.py` no se toca.
MODELOS_SONDA = [m for m in (os.environ.get("GEMV_SONNET_IDS") or "").split(",")
                 if m.strip()]


def elige_modelo(cx):
    """Prueba los identificadores en orden. Devuelve el que conteste, o None."""
    if not MODELOS_SONDA or not cx.ep:
        return None
    intentos = []
    for m in MODELOS_SONDA[:3]:
        m = m.strip()
        cx.modelo = m
        cx.usa_cache, cx.cache_probada, cx.fallos = True, False, 0
        t0 = time.perf_counter()
        r = cx._llama("Di solamente la palabra azul.", 0)
        ms = round((time.perf_counter() - t0) * 1000.0, 1)
        ok = bool(r.get("ok"))
        intentos.append({"modelo": m, "ok": ok, "ms": ms,
                         "codigo": r.get("codigo"),
                         "error": (r.get("motivo") or r.get("cuerpo") or
                                   r.get("json_malo") or "")[:400],
                         "texto": (r.get("texto") or "")[:120]})
        log({"k": "sonda_sonnet", "intento": len(intentos), **intentos[-1]})
        if ok:
            log({"k": "sonda_sonnet_fin", "elegido": m, "intentos": intentos})
            # los contadores de la sonda no cuentan como cita
            cx.n_llamadas = 0
            cx.lat, cx.lat_n, cx.fallos = [], [], 0
            # y se devuelve la cache a su sitio: un 4xx por MODELO desconocido
            # hace que `_llama` crea que la culpa es del `cache_control` y la
            # apague (cortex_t5, rama HTTPError). Aqui no lo es.
            cx.usa_cache, cx.cache_probada = True, False
            return m
    log({"k": "sonda_sonnet_fin", "elegido": None, "intentos": intentos})
    return None


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
        # [L-4] el cortex
        self.cx = CX.Cortex(log)
        self.cx_vivas = []            # [S] propuestas vivas, con su objetivo
        self.cx_tics_atada = 0
        self.cx_victorias = 0
        self.cx_empates = 0
        self.cx_tics_vetada = 0
        self.cx_tics_viva = 0
        self.cx_empate = False
        self.cx_radio = None
        self.ultima_obs = None
        self.ultimos_cands = ()

    def decidir(self, obs):
        """Ciclo real. Devuelve (accion, radiografia|None).

        [L-4] Si hay propuestas vivas del cortex, se inyectan envolviendo
        `D.candidatos` DESDE FUERA — la misma via del banco. El decisor no se
        toca y las propuestas no llevan ninguna ventaja."""
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
        # [L-4] LA INYECCION. Igual que en el banco: se envuelve el global
        # `candidatos` del modulo (`decisor_zs.py:744` lo resuelve por nombre) y
        # el bucle que valora (`:775-887`) despacha por `receta["tipo"]` sin
        # saber de donde vino. `decisor_zs.py` no se toca.
        # [S] LA ATADURA PEREZOSA. Las propuestas vivas ya no traen receta:
        # traen su objetivo, y aqui se intenta atar cada una a un candidato
        # VIVO del cuerpo o a la receta de casilla. La que no se pueda atar en
        # este tic queda DORMIDA — ni inyectada ni muerta.
        self.cx_vivas = self.cx.extra(self.tick)
        _orig = D.candidatos
        caja = {"vetadas": [], "respaldo": [], "nuevos": [], "dormidas": [],
                "de": {}}
        if self.cx_vivas:
            _vv = list(self.cx_vivas)

            def _c(o, mu, me, tk, bl=None, _o=_orig, _v=_vv, _k=caja):
                base = list(_o(o, mu, me, tk, bl))
                nom = {c[0] for c in base}
                for k in ("vetadas", "respaldo", "nuevos", "dormidas"):
                    _k[k] = []
                _k["de"] = {}
                fuera = []
                for v in _v:
                    at = CX.ata(v["obj"], v["nombre0"], base, o, mu, me, tk)
                    if at is None:
                        v["dormida"] += 1
                        _k["dormidas"].append(v["id"])
                        continue
                    n, rec, como = at
                    _k["de"][v["id"]] = n
                    if como == "cuerpo" or n in nom:
                        # el cuerpo YA ofrece ese candidato: la propuesta lo
                        # RESPALDA, no lo anade. Inyectarlo otra vez seria
                        # apuntarnos una victoria que el cuerpo iba a tener solo.
                        v["cuerpo"] += 1
                        _k["respaldo"].append(v["id"])
                        continue
                    if _veta_receta(bl, rec, o, tk):
                        v["vetada"] += 1
                        _k["vetadas"].append(v["id"])
                        continue
                    v["casilla"] += 1
                    _k["nuevos"].append(v["id"])
                    fuera.append((n, rec))
                return base + fuera
            D.candidatos = _c
        # [L-7 §2] las dos escrituras del epilogo de `decide`
        # (decisor_zs.py:903-908), por si hay que deshacer la decision.
        _ced0, _ua0 = dict(self.mem.cedidos), self.mem.ultimo_ataque
        try:
            accion, radio = D.decide(obs, self.mundo, self.mem, self.tick,
                                     self.bloqueos)
        finally:
            D.candidatos = _orig
        # [L-7 §2] LOS EMPATES SON DEL CUERPO. Una propuesta solo gana el tic si
        # su `d` es ESTRICTAMENTE menor que la del mejor candidato propio; si
        # empata, se vuelve a decidir sin inyeccion y se emite lo del cuerpo.
        self.cx_empate = False
        if caja["nuevos"]:
            _cds = {k: v["d"] for k, v in radio["candidatos"].items()}
            _iny = set(caja["nuevos"])
            _prop = {k: v for k, v in _cds.items() if k not in _iny}
            _mj = min(_prop, key=_prop.get)
            if radio["elegido"] in _iny and not (_cds[radio["elegido"]]
                                                 < _prop[_mj] - 1e-9):
                self.cx_empate = True
                self.mem.cedidos, self.mem.ultimo_ataque = _ced0, _ua0
                radio_iny = radio
                accion, radio = D.decide(obs, self.mundo, self.mem, self.tick,
                                         self.bloqueos)
                radio_iny["elegido_cuerpo"] = radio["elegido"]
                self.cx_radio = radio_iny
            else:
                self.cx_radio = radio
        else:
            self.cx_radio = radio
        ms = (time.perf_counter() - t0) * 1000.0
        # [L-6] el AHORA, para que el hilo lo mire al volver
        self.ultima_obs = obs
        self.ultimos_cands = tuple(radio["candidatos"])
        # [S] lo que paso con las propuestas vivas en este tic
        if self.cx_vivas:
            self.cx_tics_viva += 1
            self.cx.tics_con_viva += 1
            rad = self.cx_radio
            cds = {k: v["d"] for k, v in rad["candidatos"].items()}
            inyectados = {caja["de"][i] for i in caja["nuevos"]}
            propios = {k: v for k, v in cds.items() if k not in inyectados}
            mej = min(propios, key=propios.get)
            eleg = rad["elegido"]
            # [L-7 §2] victoria ESTRICTA: la propuesta entro en la mesa (no era
            # un respaldo), gano, y gano por `d` menor — no por desempate.
            gano = (eleg in inyectados) and not self.cx_empate
            if self.cx_empate:
                self.cx_empates += 1
                self.cx.empates += 1
            if caja["vetadas"]:
                self.cx_tics_vetada += 1
                self.cx.tics_con_vetada += 1
            if caja["nuevos"] or caja["respaldo"]:
                self.cx_tics_atada += 1
                self.cx.tics_con_atada += 1
            det = []
            for v in self.cx_vivas:
                pid = v["id"]
                n = caja["de"].get(pid)
                estado = ("dormida" if pid in caja["dormidas"] else
                          "vetada" if pid in caja["vetadas"] else
                          "respaldo" if pid in caja["respaldo"] else "en la mesa")
                mio = gano and n == eleg and pid in caja["nuevos"]
                fila = {"id": pid, "n": n, "estado": estado,
                        "d": cds.get(n) if estado == "en la mesa" else None,
                        "mejor": mej, "d_mejor": propios[mej],
                        "clase": v["clase"], "regla": v["regla"],
                        "obj": CX._jsonable(v["obj"]), "gano": mio,
                        "empate": self.cx_empate and n == eleg}
                if estado == "en la mesa" and n in cds:
                    fila["margen"] = round(cds[n] - propios[mej], 5)
                if mio:
                    v["gano"] += 1
                    fc = rad["candidatos"][n].get("filas") or {}
                    fm = rad["candidatos"][mej].get("filas") or {}
                    dif = {k: round(fc.get(k, 0.0) - fm.get(k, 0.0), 5)
                           for k in set(fc) | set(fm)
                           if abs(fc.get(k, 0.0) - fm.get(k, 0.0)) > 1e-9}
                    fila["tres_filas"] = sorted(dif.items(),
                                                key=lambda kv: -abs(kv[1]))[:3]
                    fila["accion"] = v["accion"]
                    fila["motivo"] = v["motivo"]
                elif estado == "en la mesa" and not gano:
                    # [S R3] la fila que MAS lo separa del que le gana
                    tres = _filas_entre(rad, n, mej)
                    if tres:
                        fila["pierde_por"] = tres
                        # [D-0] se acumula en la propuesta: al morir, la fila
                        # que MAS veces la separo es la que va al parte.
                        pj = v.setdefault("pierde", {})
                        pj[tres[0][0]] = pj.get(tres[0][0], 0) + 1
                elif estado == "respaldo" and n:
                    # [D-C] RAZON TAMBIEN EN EL RESPALDO. Hasta aqui, una
                    # propuesta que el cuerpo YA ofrecia no dejaba ninguna
                    # razon: el parte del D-B decia "prefirio otra cosa" en 76
                    # de sus 125 lineas por esto. No se cambia ni la inyeccion
                    # ni la atadura; solo se APUNTA.
                    if eleg == n:
                        # el cuerpo la eligio: ¿frente a quien, y por que?
                        seg = _segundo(propios, n)
                        if seg is None:
                            fila["gana_por"] = None
                            fila["frente_a"] = None
                            gj = v.setdefault("gana", {})
                            gj["_UNICA"] = gj.get("_UNICA", 0) + 1
                        else:
                            tres = _filas_entre(rad, n, seg)
                            fila["frente_a"] = seg
                            fila["gana_por"] = tres
                            if tres:
                                gj = v.setdefault("gana", {})
                                gj[tres[0][0]] = gj.get(tres[0][0], 0) + 1
                                fr = v.setdefault("frente", {})
                                fr[seg] = fr.get(seg, 0) + 1
                    else:
                        # el cuerpo ofrecia ese candidato y eligio OTRO: eso es
                        # un "no lo compro" con razon, igual que el inyectado.
                        tres = _filas_entre(rad, n, eleg)
                        if tres:
                            fila["pierde_por"] = tres
                            pj = v.setdefault("pierde", {})
                            pj[tres[0][0]] = pj.get(tres[0][0], 0) + 1
                det.append(fila)
            if gano:
                self.cx_victorias += 1
                self.cx.victorias += 1
            log({"k": "cortex_tic", "tick": self.tick, "elegido": eleg,
                 "emitido": radio["elegido"], "gano_cortex": gano,
                 "empate_al_cuerpo": self.cx_empate, "propuestas": det})
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

    def _foto(self, obs, rec, radio):
        """[L-4] arma el `e` que el relator del banco t5 espera, con los mismos
        campos que tenia en `escenas_t5.json`."""
        mem = self.mem
        cands = D.candidatos(obs, self.mundo, copy.deepcopy(mem), self.tick,
                             copy.deepcopy(self.bloqueos))
        recetas = {}
        recetas_vivas = {}
        for n, r in cands:
            recetas_vivas[n] = dict(r)
            recetas[n] = {"tipo": r.get("tipo"), "dir": r.get("dir"),
                          "destino": list(r["destino"]) if r.get("destino") else None,
                          "objetivo": r.get("objetivo"),
                          "item": ((r.get("item") or {}).get("id")
                                   if isinstance(r.get("item"), dict)
                                   else r.get("item"))}
        vis = obs.get("visible") or {}
        cuerpos = frozenset(tuple(a.get("pos") or ()) for a in
                            (vis.get("agents") or []) if a.get("pos"))
        e = {"r": rec, "pc_teammate": self.mundo.teammate_slot,
             "recetas": recetas,
             # [L-4 arreglo] `decidir()` APLANA `radio["candidatos"]` a floats
             # salvo cada DETALLE_CANDIDATOS_CADA tics (policy_serie.py:143-144),
             # y la foto cae en tics que casi nunca son multiplo de ese 24. Se
             # aceptan las dos formas. (Sin esto: TypeError, 19 veces en la L-4.)
             "cuerpo": {k: ({"d": v["d"], "movs": v.get("movs")}
                            if isinstance(v, dict) else {"d": v, "movs": None})
                        for k, v in radio["candidatos"].items()},
             "cert": A.agresor_de_la_hermana(obs, self.mundo, mem, self.tick),
             "parte_fresco": (None if mem.parte_fresco(self.tick) is None
                              else int(self.tick - mem.parte_fresco(self.tick)["t"])),
             "agresores_det": (radio.get("ahora") or {}).get("agresores") or [],
             "_recetas_vivas": recetas_vivas,
             "_cuerpos": cuerpos,
             "_objetos": dict(mem.objetos_vistos)}
        # el golpe al hermano, como en el banco t5: se ofrece si el MUNDO lo
        # permite (arma, alineado, a alcance y primero de la linea).
        gh = self._golpe_hermano(obs)
        if gh is not None:
            e["_golpe_hermano"] = gh[0]
            e["_receta_golpe_hermano"] = gh[1]
        ofrecidas = {n: RT.en_llano(n, e) for n in recetas}
        if gh is not None:
            ofrecidas[gh[0]["nombre"]] = gh[0]["frase"]
        # [L-5] `reloj` deja que el hilo sepa en que tic VUELVE la respuesta,
        # sin compartir estado mutable: es una funcion que lee el tic actual.
        # [L-6] `estado` deja que el hilo, al VOLVER, mire como esta el mundo
        # entonces y sepa si su propuesta sigue siendo traducible.
        _hand = ((obs.get("you") or {}).get("hand") or {}).get("id")
        _arma = self.mundo.items.get(_hand) if _hand else None
        self.cx.pide({"tick": self.tick, "e": e, "ofrecidas": ofrecidas,
                      "reloj": (lambda: self.tick),
                      "hand_foto": _hand,
                      "estado": self._estado})

    def _estado(self):
        """[L-6] foto ligera del AHORA, para el hilo del cortex.
        [L-7] con lo que el contador de MOTIVO CADUCADO necesita mirar: si el
        hermano sigue vivo y a la vista, y que hay en cada casilla."""
        o = self.ultima_obs or {}
        you = o.get("you") or {}
        vis = o.get("visible") or {}
        hid = (you.get("hand") or {}).get("id")
        arma = self.mundo.items.get(hid) if (hid and self.mundo) else None
        herm = self.mundo.teammate_slot if self.mundo else None
        agentes = {a.get("slot"): tuple(a.get("pos") or ())
                   for a in (vis.get("agents") or []) if a.get("pos")}
        items = {}
        for it in (vis.get("items") or []):
            q = tuple(it.get("pos") or ())
            if q:
                items.setdefault(q, set()).add(it.get("id"))
        return {"tick": self.tick, "pos": tuple(you.get("pos") or ()),
                "slot": (self.mundo.slot if self.mundo else None),
                "hand": hid, "alcance": (arma.range if arma else 0),
                "agentes": agentes, "items": items,
                "pareja_muerta": bool(getattr(self.mem, "pareja_muerta", False)),
                "pareja_vista": herm in agentes,
                "cands": set(self.ultimos_cands or ())}

    def _golpe_hermano(self, obs):
        """[L-4] el candidato ANADIDO del banco t5, si el mundo lo permite."""
        you = obs.get("you") or {}
        hid = (you.get("hand") or {}).get("id")
        arma = self.mundo.items.get(hid) if hid else None
        if arma is None or arma.damage <= 0:
            return None
        herm = self.mundo.teammate_slot
        pos = tuple(you.get("pos") or ())
        ag = (obs.get("visible") or {}).get("agents") or []
        a = next((x for x in ag if x.get("slot") == herm and x.get("pos")), None)
        if a is None or not pos:
            return None
        q = tuple(a["pos"]); dx, dy = q[0] - pos[0], q[1] - pos[1]
        if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
            return None
        if max(abs(dx), abs(dy)) > arma.range:
            return None
        d = D._dir_hacia(pos, q)
        # y que sea el PRIMERO de la linea (regla del mundo, sim.nim:905-914)
        ocup = {tuple(x["pos"]): x for x in ag if x.get("pos")}
        ddx, ddy = D.DIRS[d]; p = pos
        for _ in range(arma.range):
            p = (p[0] + ddx, p[1] + ddy)
            if self.mundo.solido(p[0], p[1]):
                return None
            if p in ocup:
                if ocup[p].get("slot") != herm:
                    return None
                break
        return ({"nombre": f"atacar_{d}",
                 "frase": (f"atacar hacia el {RT.DIRX.get(d, d)} con "
                           f"{RT.ELCOSA.get(hid, hid)}; el primero en esa "
                           f"linea es tu hermano")},
                {"tipo": "atacar", "dir": d, "objetivo": herm, "arma": arma})

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
        # [L-4] LA FOTO para el cortex. Se arma aqui porque `rec` ES el registro
        # de tic que el relator del banco espera en `e["r"]`. Se deja en la cola
        # y el hilo la recoge: el bucle no espera a nadie.
        if CX.ON and self.phase == "live" and self.tick % CX.CADA == 0 \
                and radio is not None and self.mundo is not None:
            try:
                self._foto(obs, dict(rec), radio)
            except Exception as e:
                log({"k": "cortex_error", "tick": self.tick,
                     "donde": "foto", "error": repr(e)[:300]})
        # [MAPA] 4 — REEMISION cada 2.000 tics. Motivo: la plataforma corta el
        # diario por ARRIBA (paper tres, acta de cobertura: 20 de 80 diarios de
        # la 66 perdieron el arranque, uno de cada cuatro). Si el mapa solo
        # viajara en el player_config, se perderia con la cabeza. 48 filas cada
        # 2.000 tics son ~4 copias por partida y ~10 kB: despreciable.
        # [L-4] el resumen acumulado, con las reemisiones, por si cortan la cabeza
        if CX.ON and self.tick % REEMISION_CADA == 0:
            log(self.cx.resumen(self.tick))
            # [D-B b] EL LIBRO: todas las llamadas hasta ahora, una linea cada
            # una, reemitido con los demas. El D-0 perdio la mitad de su
            # partida porque el detalle por llamada se escribia UNA vez.
            log(self.cx.libro_compacto(self.tick))
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
            if CX.ON:
                alma.cx.pide_gasto()
                log(alma.cx.resumen(alma.tick))
            alma.done.set()
            return


async def run(url):
    alma = Alma()
    t0 = time.time()
    log({"k": "arranque", "constitucion": CONSTITUCION,
         "emision": EMISION, "vigia_s": VIGIA_S,
         "mirada_min_ticks": D.H_MIRADA_MIN, "voz_cada_ticks": VOZ_CADA,
         "cuerpo": "v42_exp EMPATIA_ON H_PREV 0.25 H_GOLPE 1.0 "
                   "MIEDO_ON False VIDA_AJENA_ON False"})
    if MODELOS_SONDA:
        m = elige_modelo(alma.cx)
        if m is None:
            alma.cx.callado = True
            log({"k": "sonda_sonnet", "resultado":
                 "EL SIDECAR NO SIRVE NINGUN SONNET; el cortex se calla"})
    alma.cx.arranca()
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

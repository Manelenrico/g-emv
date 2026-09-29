"""POLICY_RED — copia de `policy_serie.py` con la SONDA DE RED. [14-sep-2026]

Tres anadidos y NINGUN cambio de conducta: la politica, el appraisal y el
decisor son exactamente los de `policy_serie.py` (la imagen sin ENV es v37).

  A4. [L-2b] EL REGISTRO `red` SE REEMITE. La L-2 salio en blanco: la plataforma
     corta el diario POR LA CABEZA y el registro `red`, escrito una sola vez al
     arrancar, se perdio entero (el primer tic que llego fue el 4189). El mapa y
     el catalogo sobrevivieron porque `REEMISION_CADA` los repite cada 100 tics.
     Se hace lo mismo con `red`: la sonda guarda su resultado en `_RED_REC` y el
     bloque de reemision lo vuelve a escribir. Es el mismo remedio que el
     proyecto ya usa, no uno nuevo.

  A3. [L-2] LA LLAMADA AL MODELO. Si `AWS_ENDPOINT_URL_BEDROCK_RUNTIME` esta
     puesta, UNA sola llamada `InvokeModel` AL SIDECAR — nunca al host real de
     AWS, nunca firmando nada (`docs/BEDROCK.md:8-25`) — con el modelo de
     `BEDROCK_MODEL`, diez palabras y `max_tokens` 20. Se anota el codigo, los
     ms, las cabeceras `X-Coworld-Spend-Usd` y `X-Coworld-Spend-Limit-Usd` y el
     texto devuelto; y DESPUES `GET .../spend` entero. Se registra el CUERPO de
     la respuesta tambien cuando falla (`BEDROCK.md:109-110`: un bot que solo
     apunta el 403 esconde cual de los tres fallos es). Si no hay sidecar, se
     anota y se sigue. Todo esto vive en el mismo hilo aparte: no bloquea nada.

  A2. [L-1] SEGUNDA SONDA. Lo que la L-0 no pudo distinguir: si lo cortado es
     SOLO el nombre o todo el egreso. Tres cambios:
       · la sonda YA NO se corta cuando falla el DNS: sigue adelante;
       · conexion a **IP EN CRUDO** 160.79.104.10:443 (una de las de
         api.anthropic.com, resuelta desde este Mac el 14-sep), con TLS y el
         NOMBRE en SNI, y un GET /v1/models a mano con cabecera Host;
       · y, de paso y gratis, si esta puesta `AWS_ENDPOINT_URL_BEDROCK_RUNTIME`
         se pregunta a su `/healthz/core-v1` (docs/BEDROCK.md:96-98). Con la
         policy subida SIN `--use-bedrock` debe salir vacia: sirve de control.
     Se declara ademas que `getaddrinfo` NO respeta el timeout del socket (en
     la L-0 tardo 20 s con RED_TIMEOUT=5): es el resolver el que agota sus
     reintentos, y por eso la sonda va en hilo aparte.

  A. SONDA DE RED, UNA SOLA VEZ al arrancar y en un HILO APARTE
     (`threading.Thread(daemon=True)`), de modo que no puede bloquear el bucle
     de asyncio ni retrasar una sola emision. Con tiempos de espera cortos.
     Mide, en milisegundos, y lo escribe en el diario como `{"k": "red", ...}`:
       a. resolucion de nombre de `api.anthropic.com` y conexion TCP+TLS a :443
       b. una peticion HTTPS minima SIN CLAVE y su codigo de respuesta
       c. el tiempo de cada paso
       d. si falla, el error exacto y de que tipo (DNS, timeout, rechazo, TLS)

  B. EL RELOJ REAL, visto desde dentro: los milisegundos de pared entre
     observaciones consecutivas (`dt_ms` en cada tic) y su resumen al final.
     `radio["ms"]`, que ya existia, es lo que tarda una decision completa.

  C. Nada mas. Ni una clave viaja en la imagen: la sonda no la necesita.

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
import json
import math
import os
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request

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


# ── A. LA SONDA DE RED ─────────────────────────────────────────────────────
RED_HOST = "api.anthropic.com"
# [L-1] una IP de api.anthropic.com resuelta desde el Mac el 14-sep-2026. Va
# cableada A PROPOSITO: es justo lo que se quiere probar, alcanzar una IP sin
# pasar por el DNS. No es un identificador del mundo: es el sujeto del experimento.
RED_IP = "160.79.104.10"
RED_TIMEOUT = 5.0          # corto a proposito: la sonda jamas cuelga la partida
# [L-2] la llamada al modelo va acotada aparte: mas holgada que la sonda de red
# pero acotada igual (`BEDROCK.md:198`: "Bound each model call").
BEDROCK_TIMEOUT = 10.0
BEDROCK_MAX_TOKENS = 20
BEDROCK_PROMPT = "Di en una palabra el color del cielo despejado hoy"   # 10 palabras
RED_URLS = [
    # peticiones MINIMAS que no necesitan clave. La primera es el propio
    # servidor de la API (devolvera 401/404 sin clave, que es respuesta
    # valida: lo que se mide es si HAY SALIDA, no si autentica).
    ("anthropic_sin_clave", "https://api.anthropic.com/v1/models"),
    ("publico", "https://www.google.com/generate_204"),
]


_RED_REC = None            # [L-2b] lo ultimo que escribio la sonda, para reemitir


def _ms(t0):
    return round((time.perf_counter() - t0) * 1000.0, 1)


def _tipo_error(e):
    if isinstance(e, socket.gaierror):
        return "DNS"
    if isinstance(e, socket.timeout) or isinstance(e, TimeoutError):
        return "TIEMPO_AGOTADO"
    if isinstance(e, ConnectionRefusedError):
        return "RECHAZO"
    if isinstance(e, ssl.SSLError):
        return "TLS"
    if isinstance(e, urllib.error.HTTPError):
        return "HTTP"
    if isinstance(e, urllib.error.URLError):
        return f"URL/{_tipo_error(e.reason) if isinstance(e.reason, Exception) else 'desconocido'}"
    return type(e).__name__


def sonda_red():
    """Se ejecuta UNA VEZ, en un hilo aparte. Nunca lanza."""
    out = {"k": "red", "host": RED_HOST, "timeout_s": RED_TIMEOUT,
           "proxy_env": {k: os.environ.get(k) for k in
                         ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy",
                          "https_proxy", "NO_PROXY", "no_proxy")
                         if os.environ.get(k)}}
    # a.1 resolucion de nombre
    t0 = time.perf_counter()
    try:
        infos = socket.getaddrinfo(RED_HOST, 443, proto=socket.IPPROTO_TCP)
        out["dns"] = {"ok": True, "ms": _ms(t0),
                      "ips": sorted({i[4][0] for i in infos})[:4]}
    except Exception as e:
        # [L-1] NO se corta: sin nombre no hay TCP por nombre, pero si por IP.
        out["dns"] = {"ok": False, "ms": _ms(t0), "tipo": _tipo_error(e),
                      "error": repr(e)[:300],
                      "nota": "getaddrinfo no respeta el timeout del socket"}
        infos = None
    # a.2 conexion TCP y handshake TLS POR NOMBRE (solo si el DNS resolvio)
    if infos is None:
        out["tcp_tls"] = {"ok": False, "saltado": "sin DNS no hay conexion por nombre"}
        _sonda_ip(out)
        _guarda_red(out)
        return
    t0 = time.perf_counter()
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((RED_HOST, 443), timeout=RED_TIMEOUT) as s:
            tcp_ms = _ms(t0)
            t1 = time.perf_counter()
            with ctx.wrap_socket(s, server_hostname=RED_HOST) as ss:
                out["tcp"] = {"ok": True, "ms": tcp_ms}
                out["tls"] = {"ok": True, "ms": _ms(t1),
                              "version": ss.version(),
                              "cipher": (ss.cipher() or [None])[0]}
    except Exception as e:
        out["tcp_tls"] = {"ok": False, "ms": _ms(t0), "tipo": _tipo_error(e),
                          "error": repr(e)[:300]}
        _sonda_ip(out)
        log(out)
        return
    # b. peticiones HTTPS minimas, SIN CLAVE
    out["http"] = []
    for nombre, url in RED_URLS:
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(url, method="GET",
                                         headers={"User-Agent": "gemv-sonda/1"})
            with urllib.request.urlopen(req, timeout=RED_TIMEOUT) as r:
                out["http"].append({"nombre": nombre, "url": url, "ok": True,
                                    "codigo": r.status, "ms": _ms(t0),
                                    "bytes": len(r.read(2048))})
        except urllib.error.HTTPError as e:
            # un 401/404 ES salida a internet: hubo respuesta del servidor
            out["http"].append({"nombre": nombre, "url": url, "ok": True,
                                "codigo": e.code, "ms": _ms(t0),
                                "nota": "respuesta HTTP de error: HAY SALIDA"})
        except Exception as e:
            out["http"].append({"nombre": nombre, "url": url, "ok": False,
                                "ms": _ms(t0), "tipo": _tipo_error(e),
                                "error": repr(e)[:300]})
    _sonda_ip(out)
    out["veredicto"] = "HAY SALIDA" if any(h.get("ok") for h in out["http"]) \
        else "SIN SALIDA"
    _guarda_red(out)


def _guarda_red(out):
    """[L-2b] escribe el registro Y lo guarda para reemitirlo."""
    global _RED_REC
    _RED_REC = dict(out)
    log(out)


def _invoca_modelo(ep, modelo):
    """[L-2] UNA llamada `InvokeModel` al sidecar. Nunca al host de AWS, nunca
    firmada: el sidecar pone la identidad (`BEDROCK.md:24-25, 77-87`)."""
    if not modelo:
        return {"ok": False, "motivo": "BEDROCK_MODEL vacia"}
    url = f"{ep.rstrip('/')}/model/{modelo}/invoke"
    cuerpo = json.dumps({"anthropic_version": "bedrock-2023-05-31",
                         "max_tokens": BEDROCK_MAX_TOKENS,
                         "messages": [{"role": "user",
                                       "content": BEDROCK_PROMPT}]}).encode()
    r = {"url": url, "modelo": modelo, "max_tokens": BEDROCK_MAX_TOKENS,
         "prompt": BEDROCK_PROMPT}
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(
            url, data=cuerpo, method="POST",
            headers={"Content-Type": "application/json",
                     "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=BEDROCK_TIMEOUT) as rr:
            crudo = rr.read(8192).decode("utf-8", "replace")
            r.update(ok=True, codigo=rr.status, ms=_ms(t0),
                     spend_usd=rr.headers.get("X-Coworld-Spend-Usd"),
                     spend_limit_usd=rr.headers.get("X-Coworld-Spend-Limit-Usd"))
            try:
                d = json.loads(crudo)
                r["texto"] = "".join(c.get("text", "") for c in
                                     (d.get("content") or [])
                                     if c.get("type") == "text")[:400]
                r["usage"] = d.get("usage")
                r["stop_reason"] = d.get("stop_reason")
            except Exception:
                r["cuerpo_crudo"] = crudo[:600]
    except urllib.error.HTTPError as e:
        # BEDROCK.md:109-110: el CUERPO nombra el fallo exacto, no el codigo
        r.update(ok=False, codigo=e.code, ms=_ms(t0),
                 spend_usd=e.headers.get("X-Coworld-Spend-Usd") if e.headers else None,
                 spend_limit_usd=(e.headers.get("X-Coworld-Spend-Limit-Usd")
                                  if e.headers else None),
                 retry_after_ms=e.headers.get("Retry-After-Ms") if e.headers else None,
                 cuerpo=e.read(2048).decode("utf-8", "replace")[:800])
    except Exception as e:
        r.update(ok=False, ms=_ms(t0), tipo=_tipo_error(e),
                 detalle=repr(e)[:300])
    return r


def _sonda_ip(out):
    """[L-1] IP EN CRUDO, sin pasar por el DNS. Distingue "solo el nombre esta
    cortado" de "no hay egreso ninguno"."""
    r = {"ip": RED_IP, "puerto": 443, "sni": RED_HOST}
    t0 = time.perf_counter()
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((RED_IP, 443), timeout=RED_TIMEOUT) as s_:
            r["tcp"] = {"ok": True, "ms": _ms(t0)}
            t1 = time.perf_counter()
            # el NOMBRE va en SNI: el certificado se valida contra el nombre
            with ctx.wrap_socket(s_, server_hostname=RED_HOST) as ss:
                r["tls"] = {"ok": True, "ms": _ms(t1), "version": ss.version()}
                t2 = time.perf_counter()
                ss.settimeout(RED_TIMEOUT)
                ss.sendall(("GET /v1/models HTTP/1.1\r\n"
                            f"Host: {RED_HOST}\r\n"
                            "User-Agent: gemv-sonda/2\r\n"
                            "Connection: close\r\n\r\n").encode())
                buf = b""
                while len(buf) < 512:
                    try:
                        c = ss.recv(512)
                    except Exception:
                        break
                    if not c:
                        break
                    buf += c
                linea = buf.split(b"\r\n", 1)[0].decode("latin-1")[:120]
                r["http"] = {"ok": bool(linea), "ms": _ms(t2),
                             "primera_linea": linea}
    except Exception as e:
        r["error"] = {"ms": _ms(t0), "tipo": _tipo_error(e),
                      "detalle": repr(e)[:300]}
    # el veredicto de esta pata es solo sobre la IP; cruzarlo con `dns` es lo
    # que distingue "solo el nombre cortado" de "sin egreso ninguno".
    r["veredicto"] = ("HAY EGRESO POR IP" if r.get("http", {}).get("ok")
                      else "SIN EGRESO POR IP")
    out["ip_cruda"] = r
    # [L-1] de paso: ¿esta el sidecar de Bedrock? (docs/BEDROCK.md:96-98)
    ep = os.environ.get("AWS_ENDPOINT_URL_BEDROCK_RUNTIME")
    b = {"AWS_ENDPOINT_URL_BEDROCK_RUNTIME": ep,
         "USE_BEDROCK": os.environ.get("USE_BEDROCK"),
         "BEDROCK_MODEL": os.environ.get("BEDROCK_MODEL"),
         "AWS_REGION": os.environ.get("AWS_REGION")}
    if ep:
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(ep.rstrip("/") + "/healthz/core-v1",
                                        timeout=RED_TIMEOUT) as rr:
                b["healthz"] = {"ok": True, "codigo": rr.status, "ms": _ms(t0),
                                "cuerpo": rr.read(64).decode("latin-1", "replace")}
        except Exception as e:
            b["healthz"] = {"ok": False, "ms": _ms(t0), "tipo": _tipo_error(e),
                            "detalle": repr(e)[:200]}
        # [L-2] UNA llamada InvokeModel, al SIDECAR, sin Authorization.
        b["invoke"] = _invoca_modelo(ep, b.get("BEDROCK_MODEL"))
        # [L-2] y el contador de gasto, entero
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(ep.rstrip("/") + "/spend",
                                        timeout=RED_TIMEOUT) as rr:
                b["spend"] = {"ok": True, "codigo": rr.status, "ms": _ms(t0),
                              "cuerpo": rr.read(2048).decode("latin-1", "replace")}
        except Exception as e:
            b["spend"] = {"ok": False, "ms": _ms(t0), "tipo": _tipo_error(e),
                          "detalle": repr(e)[:300]}
    else:
        b["nota"] = "no hay sidecar: AWS_ENDPOINT_URL_BEDROCK_RUNTIME vacia"
    out["bedrock"] = b


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
        self.wall_prev = None          # [RED] reloj de pared del tic anterior
        self.dt_ms = []                # [RED] ms entre observaciones
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
               "action_result_obs": you.get("action_result"),
               # [RED] ms de pared desde la observacion anterior
               "dt_ms": getattr(self, "_dt_ms_actual", None)}
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
        # [L-2b] el registro de la sonda, con el resto de reemisiones: es lo
        # unico que lo salva del recorte de cabeza de la plataforma.
        if self.tick % REEMISION_CADA == 0 and _RED_REC is not None:
            log(dict(_RED_REC, reemitido_en=self.tick))
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
            # [RED] B. EL RELOJ REAL: ms de pared entre observaciones. Se mide
            # ANTES de decidir, para que no lo contamine el tiempo de decision.
            _ahora = time.monotonic()
            _dt = None
            if alma.wall_prev is not None:
                _dt = round((_ahora - alma.wall_prev) * 1000.0, 2)
                alma.dt_ms.append(_dt)
            alma.wall_prev = _ahora
            alma._dt_ms_actual = _dt
            alma.ultimo_obs_wall = _ahora
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
                 "reloj_ms": _resumen(alma.dt_ms),
                 "B_final": round(alma.mem.roce_B, 4),
                 "pareja_muerta": alma.mem.pareja_muerta})
            alma.done.set()
            return


def _resumen(v):
    """[RED] mediana, p5/p95 y extremos de una lista de milisegundos."""
    if not v:
        return None
    s = sorted(v)
    return {"n": len(s), "min": s[0], "p5": s[int(len(s) * 0.05)],
            "mediana": s[len(s) // 2], "p95": s[int(len(s) * 0.95)],
            "max": s[-1], "media": round(sum(s) / len(s), 2)}


async def run(url):
    alma = Alma()
    t0 = time.time()
    # [RED] A. la sonda, UNA VEZ y en hilo aparte: no bloquea el bucle.
    threading.Thread(target=sonda_red, name="sonda_red", daemon=True).start()
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

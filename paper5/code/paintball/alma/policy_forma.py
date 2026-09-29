"""[P5-6A] LA POLITICA CON FORMAS. Parte de `policy_cortex.py` de S-3.

`policy_cortex.py` NO SE TOCA: esta politica la importa y hereda de su `Alma`,
asi que con todo apagado la decision recorre **exactamente el mismo codigo** y
no hay que confiar en que dos copias sigan pareciendose. `decisor_zs.py` y
`appraisal_zs_v42_exp.py` tampoco se tocan: la forma entra envolviendo
`D.candidatos` desde fuera, como el arnes.

LO NUEVO, todo tras interruptor:

  GEMV_FORMA            la puerta ancha honesta en vivo (A1)
  GEMV_HILO_FORMA       el hermano cuenta su forma por el canal team (A2)
  GEMV_CONSEJERO_FORMA  se cita al consejero y se le piden formas (A1/A4)
  GEMV_FORMAS_AZAR      brazo T: formas al azar en vez de consejero (A5)

LA REGLA es la de P5-3H sin tocarla (`forma.curva_H` + `forma.mejor_propia_H` +
`forma.juzga_margen`), con el margen que modula la confianza (A3) y
reevaluacion **al llegar a un punto de control y cada 25 tics**.

UN ARREGLO QUE HAY QUE DECLARAR. En `policy_cortex.py:493-497` la regla «los
empates son del cuerpo» **no corre**: `_iny` se llena con IDs de propuesta
(enteros) y se compara con `radio["elegido"]`, que es un nombre de candidato
(cadena), asi que la condicion nunca es cierta. Medido en los 160 diarios de
S2_B y S2_C: `empates_al_cuerpo = 0` en los 160, y **4 de 1.908 victorias
(0,21 %) fueron empates emitidos como victoria**. Aqui la regla se escribe
BIEN, con el mapa `caja["de"]`, y el humo (b2) lo comprueba.
"""
from __future__ import annotations
import json
import os
import urllib.error
import urllib.request
import random
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
for _p in ("/app", AQUI,
           os.path.join(os.path.dirname(os.path.dirname(AQUI)),
                        "cantera", "paper5")):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

from alma import policy_cortex as PC                        # noqa: E402
from alma import cortex_t5 as CX                            # noqa: E402
from alma import decisor_zs as D                            # noqa: E402
from alma import appraisal_zs_v42_exp as A                  # noqa: E402
from alma import relator_t5 as RT                           # noqa: E402
from alma import forma_viva as FV                           # noqa: E402
from alma import confianza_viva as CVIVA                    # noqa: E402
from alma import hilo_forma as HF                           # noqa: E402
from alma import formas_azar as FAZ                         # noqa: E402

import forma as F                                           # noqa: E402
import proyeccion as P                                      # noqa: E402
import traductor_forma as TF                                # noqa: E402
import alcance_g as AL                                      # noqa: E402
import curiosidad as CUR_MOD                                # noqa: E402
import curiosidad_forma as CFM                               # noqa: E402

log = PC.log

# ── los interruptores, del entorno CRUDO y EFECTIVO ───────────────────────
FORMA_ON = os.environ.get("GEMV_FORMA", "0") == "1"
HILO_ON = os.environ.get("GEMV_HILO_FORMA", "0") == "1"
CONSEJERO_ON = os.environ.get("GEMV_CONSEJERO_FORMA", "0") == "1"
AZAR_ON = os.environ.get("GEMV_FORMAS_AZAR", "0") == "1"
AZAR_SEMILLA = int(os.environ.get("GEMV_FORMAS_AZAR_SEMILLA", "20260920") or 0)

# [P5-7C · C0] LA CURIOSIDAD POR EL TERRENO, en el bucle del juego.
#   GEMV_CURIOSIDAD=frontera  instala `R-CURIOSIDAD-FRONTERA` (curiosidad.py).
#   Vacio o "0" = apagada, y entonces la politica es EXACTAMENTE la de antes.
# El renglon se instala FUERA del appraisal (`D.A` pasa a ser el proxy que
# delega todo en v42), igual que en el banco de P5-7A.
CURIOSIDAD = (os.environ.get("GEMV_CURIOSIDAD", "") or "").strip().lower()
CURIOSIDAD_ON = CURIOSIDAD in ("frontera", "local")
CURIOSIDAD_K = float(os.environ.get("GEMV_CURIOSIDAD_K", "0.2") or 0.2)
CURIOSIDAD_BALANZA = os.environ.get("GEMV_CURIOSIDAD_BALANZA", "1") != "0"

# [P5-8B] EL BRAZO K: la curiosidad como FORMA, seguida en vivo por la misma
# maquinaria con la que el brazo F seguia las formas del consejero.
#   GEMV_CURIOSIDAD_FORMA=1  enciende el brazo. Necesita GEMV_FORMA=1 (la
#   maquinaria de formas) y NO usa consejero ni azar: nadie llama a ningun
#   modelo.
CUR_FORMA_ON = os.environ.get("GEMV_CURIOSIDAD_FORMA", "0") == "1"
CUR_CONSIGNA = float(os.environ.get("GEMV_CURIOSIDAD_CONSIGNA", "0.5") or 0.5)
CUR_REFRACTARIO = int(os.environ.get("GEMV_CURIOSIDAD_REFRACTARIO", "50") or 50)
# [P5-8E] EL ATASCO EN EL RELOJ DEL MUNDO. Antes eran 25 tics constantes; a
# 11 tics por casilla eso son DOS casillas, la misma trampa de escala que el
# examen. Ahora son TRES PASOS del mundo (3 x los tics por casilla, LEIDOS de
# `mundo.coste_movimiento`, no cableados) sin acercarse AL MENOS UNA CASILLA.
CUR_ATASCO_PASOS = 3

# [P5-6C · C0] VALORES DEFINITIVOS de la cita, medidos en P5-6B y fijados aqui
# como DEFECTO de la imagen (y repetidos en el upload, para que consten en el
# entorno crudo del diario):
#   · la cadencia de 100 tics eran 4,2 s a 24 tics/s, MAS RAPIDA que la propia
#     llamada (mediana 7,2 s): 40 de 84 citas se saltaban. A 250 tics son
#     10,4 s, y las saltadas bajaron de 40 a 4.
#   · el tope de 8 s mataba el 36 % de las llamadas justo en el borde; a 25 s,
#     cero fallos en 61 llamadas.
CITA_CADA = int(os.environ.get("GEMV_FORMA_CADA", "250") or 250)
SPEND_CADA = int(os.environ.get("GEMV_FORMA_SPEND_CADA", "10") or 10)
HILO_CADA = 48                      # la cadencia del hilo actual (voz)
MS_AL_HILO = 20.0                   # si evaluar pasa de esto, va al hilo
TOPE_LLAMADAS = 200                 # el mundo lento da hasta 182 citas
TOPE_GASTO_USD = 1.00               # igual que el cuatro
HERMANO_VIEJO = 150                 # su forma caduca a los 150 tics


def entorno_forma():
    """Crudo y efectivo, como manda la regla del cuatro."""
    crudo = {k: os.environ.get(k) for k in
             ("GEMV_FORMA", "GEMV_HILO_FORMA", "GEMV_CONSEJERO_FORMA",
              "GEMV_FORMAS_AZAR", "GEMV_FORMAS_AZAR_SEMILLA",
              "GEMV_FORMA_CADA", "GEMV_FORMA_SPEND_CADA",
              "GEMV_CORTEX_TIMEOUT", "GEMV_CURIOSIDAD",
              "GEMV_CURIOSIDAD_K", "GEMV_CURIOSIDAD_BALANZA",
              "GEMV_CURIOSIDAD_FORMA", "GEMV_CURIOSIDAD_CONSIGNA",
              "GEMV_CURIOSIDAD_REFRACTARIO")}
    return {"crudo": crudo,
            "efectivo": {"CUR_FORMA": CUR_FORMA_ON,
                         "CUR_CONSIGNA": CUR_CONSIGNA,
                         "CUR_REFRACTARIO": CUR_REFRACTARIO,
                         "CUR_ATASCO_PASOS": CUR_ATASCO_PASOS,
                         "CURIOSIDAD": CURIOSIDAD or None,
                         "CURIOSIDAD_ON": CURIOSIDAD_ON,
                         "CURIOSIDAD_K": CURIOSIDAD_K,
                         "CURIOSIDAD_BALANZA": CURIOSIDAD_BALANZA,
                         "FORMA": FORMA_ON, "HILO": HILO_ON,
                         "CONSEJERO": CONSEJERO_ON, "AZAR": AZAR_ON,
                         "AZAR_SEMILLA": AZAR_SEMILLA, "CITA_CADA": CITA_CADA,
                         "SPEND_CADA": SPEND_CADA, "TIMEOUT_S": CX.TIMEOUT,
                         "MS_AL_HILO": MS_AL_HILO,
                         "TOPE_LLAMADAS": TOPE_LLAMADAS,
                         "TOPE_GASTO_USD": TOPE_GASTO_USD,
                         "CADA_REEVALUA": FV.CADA_REEVALUA,
                         "C0": CVIVA.C0, "SUBE": CVIVA.SUBE,
                         "BAJA": CVIVA.BAJA,
                         "MARGEN_BASE": CVIVA.MARGEN_BASE,
                         "MARGEN_RANGO": CVIVA.MARGEN_RANGO},
            "instruccion_md5": _md5(_instruccion()),
            "tabla_md5": _md5(_tabla())}


def _md5(s):
    import hashlib
    return hashlib.md5((s or "").encode()).hexdigest()


def _lee(nombre):
    for base in ("/app/alma", AQUI,
                 os.path.join(os.path.dirname(os.path.dirname(AQUI)),
                              "cantera", "paper5")):
        p = os.path.join(base, nombre)
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    return ""


_CACHE = {}


def _instruccion():
    if "ins" not in _CACHE:
        _CACHE["ins"] = _lee("instruccion_forma.md")
    return _CACHE["ins"]


def _tabla():
    if "tab" not in _CACHE:
        _CACHE["tab"] = _lee("tabla_ensenada.md")
    return _CACHE["tab"]


def sistema_forma():
    """La instruccion de P5-5B (B1) MAS la pagina nueva, la tabla ensenada."""
    return _instruccion() + "\n\n---\n\n" + _tabla()


# ── A4 · el parte de la forma ─────────────────────────────────────────────
def parte_de_formas(cerradas, C, margen):
    """Lo que el consejero recibe de sus formas desde la cita anterior."""
    if not cerradas:
        return ("Es tu primera forma en esta partida, o ninguna de las "
                f"anteriores llego a juzgarse. Tu confianza esta en {C:.2f} y "
                f"el margen que te piden es {margen:.3f}.")
    L = ["Esto es lo que paso con tus formas desde la ultima vez:", ""]
    for c in cerradas[-4:]:
        est = c["estado"]
        cab = {"aceptada": "ACEPTADA", "cumplida": "ACEPTADA y cumplida",
               "caida": "ACEPTADA y luego caida",
               "rechazada_vida": "RECHAZADA por vida minima",
               "rechazada_area": "RECHAZADA por area",
               "vetada": "VETADA por el cuerpo"}.get(est, est.upper())
        L.append(f"- Forma {c['id']} ({len(c.get('tramos') or [])} tramos): {cab}.")
        if c.get("motivo_caida"):
            L.append(f"  Se cayo porque {c['motivo_caida']}.")
        for t in (c.get("tramos_detalle") or [])[:4]:
            dicho = t.get("dicho") or {}
            proy = t.get("proyectado") or {}
            real = t.get("real")
            L.append(
                f"  Tramo {t['i']}: dijiste vida {dicho.get('vida','?')}, "
                f"manos {dicho.get('manos','?')}, vinculo "
                f"{dicho.get('vinculo','?')} por {t.get('por') or '?'}; "
                f"el cuerpo proyecto vida {proy.get('vida','?')}, manos "
                f"{proy.get('manos','?')}, vinculo {proy.get('vinculo','?')}"
                + (f"; y de verdad sintio vida {real.get('vida','?')}, manos "
                   f"{real.get('manos','?')}, vinculo {real.get('vinculo','?')}."
                   if real else "; ese tramo no llego a vivirse."))
    L += ["", f"Tu confianza esta en {C:.2f}. Con ella, el margen que se te "
              f"pide para dejar pasar una forma es {margen:.3f} "
              f"(cuanto menos se te cree, mas ventaja tienes que ensenar)."]
    return "\n".join(L)


# ── el consejero que pide FORMAS ──────────────────────────────────────────
class ConsejeroForma:
    """Como el `Cortex` del cuatro, pero pide formas y trae el parte.

    Una sola llamada en vuelo, hilo demonio, y los dos frenos del cuatro con
    el tope de llamadas subido a 200.
    """

    def __init__(self, log_fn):
        import threading
        self.log = log_fn
        self.lock = threading.Lock()
        self.evento = threading.Event()
        self.pendiente = None
        self.en_vuelo = False
        self.callado = not CONSEJERO_ON
        self.entregado = None          # {"tick":, "formas": [...], "crudo":}
        self.n_llamadas = 0
        self.citas_saltadas = 0
        self.fallos = 0
        self.gasto_visto = None
        self.aviso_sin_cabecera = False
        self.freno = None
        self.gasto_spend = None         # [C0] la segunda lectura, por /spend
        self.ep = os.environ.get("AWS_ENDPOINT_URL_BEDROCK_RUNTIME")
        self.modelo = os.environ.get("BEDROCK_MODEL")
        self.manual = None
        self.usa_cache = True
        self.lat = []

    def arranca(self):
        import threading
        if not CONSEJERO_ON:
            self.log({"k": "consejero_forma", "estado": "apagado"})
            return
        self.manual = CX._manual()
        self.log({"k": "consejero_forma", "estado": "encendido",
                  "modelo": self.modelo, "sidecar": self.ep,
                  "cada": CITA_CADA, "sistema_md5": _md5(sistema_forma()),
                  "tope_llamadas": TOPE_LLAMADAS,
                  "tope_gasto_usd": TOPE_GASTO_USD,
                  "manual_bytes": len(self.manual or "")})
        threading.Thread(target=self._bucle, daemon=True).start()

    def pide(self, foto):
        if self.callado:
            return
        with self.lock:
            if self.en_vuelo:
                self.citas_saltadas += 1
                self.log({"k": "forma_cita_saltada", "tick": foto.get("tick"),
                          "saltadas": self.citas_saltadas})
                return
            self.en_vuelo = True
            self.pendiente = foto
        self.evento.set()

    def _bucle(self):
        while True:
            self.evento.wait()
            self.evento.clear()
            with self.lock:
                foto, self.pendiente = self.pendiente, None
            if foto is None:
                continue
            try:
                self._una(foto)
            except Exception as ex:
                self.log({"k": "forma_error", "tick": foto.get("tick"),
                          "error": repr(ex)[:300]})
            finally:
                with self.lock:
                    self.en_vuelo = False

    def _una(self, foto):
        texto = foto["relato"] + "\n\n" + foto["parte"]
        r = self._llama(texto, foto["tick"])
        llega = foto["reloj"]()
        rec = {"k": "forma_propuesta", "tick_foto": foto["tick"],
               "tick_llegada": llega, "ok": bool(r.get("ok")),
               "ms": r.get("ms"), "codigo": r.get("codigo"),
               "parte": foto["parte"], "relato_md5": _md5(foto["relato"]),
               "spend_usd": r.get("spend_usd"), "texto": r.get("texto")}
        if not r.get("ok"):
            rec["motivo"] = r.get("motivo")
            self.log(rec)
            return
        formas, inf = TF.traduce(r.get("texto") or "", foto["escena"],
                                 foto["filas"])
        rec["traduccion"] = {"parsea": inf["parsea"], "callar": inf["callar"],
                             "n_formas": len(formas), "fallos": inf["fallos"][:4]}
        self.log(rec)
        with self.lock:
            self.entregado = {"tick": llega, "formas": formas,
                              "callar": inf["callar"]}

    def recoge(self):
        with self.lock:
            e, self.entregado = self.entregado, None
        return e

    def _llama(self, texto, tick):
        import urllib.request
        if not self.ep or not self.modelo:
            self.callado = True
            return {"ok": False, "motivo": "sin sidecar o sin BEDROCK_MODEL"}
        if self.n_llamadas >= TOPE_LLAMADAS:
            if not self.callado:
                self.callado = True
                self.freno = {"cual": "llamadas", "tick": tick,
                              "llamadas": self.n_llamadas,
                              "tope": TOPE_LLAMADAS}
                self.log({"k": "forma_freno", "tick": tick, "cual": "llamadas",
                          "llamadas": self.n_llamadas, "tope": TOPE_LLAMADAS,
                          "efecto": "el consejero se calla; la partida se descarta"})
            return {"ok": False, "motivo": "freno propio: tope de llamadas"}
        if self.gasto_visto is not None and self.gasto_visto > TOPE_GASTO_USD:
            if not self.callado:
                self.callado = True
                self.freno = {"cual": "gasto", "tick": tick,
                              "gasto_usd": self.gasto_visto,
                              "tope": TOPE_GASTO_USD}
                self.log({"k": "forma_freno", "tick": tick, "cual": "gasto",
                          "gasto_usd": self.gasto_visto,
                          "tope": TOPE_GASTO_USD,
                          "efecto": "el consejero se calla; la partida se descarta"})
            return {"ok": False, "motivo": "freno propio: tope de gasto"}
        url = f"{self.ep.rstrip('/')}/model/{self.modelo}/invoke"
        bloques = []
        if self.manual:
            b = {"type": "text",
                 "text": f"{CX.CABECERA}\n\n{self.manual}\n\n---\n\n"}
            if self.usa_cache:
                b["cache_control"] = {"type": "ephemeral"}
            bloques.append(b)
        bloques.append({"type": "text", "text": texto})
        cuerpo = {"anthropic_version": "bedrock-2023-05-31",
                  "max_tokens": 1500, "system": sistema_forma(),
                  "messages": [{"role": "user", "content": bloques}]}
        datos = json.dumps(cuerpo).encode()
        # [P5-6C · C1bis] LA COMPROBACION DE CAMPO, que no depende del codigo:
        # el extracto se saca del CUERPO QUE SALE POR EL CABLE, no de la
        # variable `parte`, y se apunta el md5 del cuerpo entero. Si el parte
        # volviera a ir mudo, `interrogantes` lo cantaria sin mirar el codigo.
        _u = bloques[-1]["text"]
        _i = -1
        for _m in ("Esto es lo que paso con tus formas",
                   "Es tu primera forma en esta partida"):
            _j = _u.find(_m)
            if _j >= 0:
                _i = _j
                break
        _pt = _u[_i:] if _i >= 0 else ""
        self.log({"k": "forma_cita_cuerpo", "tick": tick,
                  "md5_cuerpo": _md5(datos.decode("utf-8", "replace")),
                  "bytes_cuerpo": len(datos),
                  "parte_encontrado": _i >= 0,
                  "parte_bytes": len(_pt),
                  "interrogantes": _pt.count("vida ?"),
                  "extracto_300": _pt[:300]})
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(
                url, data=datos, method="POST",
                headers={"Content-Type": "application/json",
                         "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=CX.TIMEOUT) as rr:
                crudo = rr.read(400000).decode("utf-8", "replace")
                ms = round((time.perf_counter() - t0) * 1000.0, 1)
                self.n_llamadas += 1
                self.lat.append(ms)
                cab = {k: v for k, v in rr.headers.items()}
                spend = cab.get("X-Coworld-Spend-Usd") or \
                    cab.get("x-coworld-spend-usd")
                try:
                    self.gasto_visto = float(spend)
                except (TypeError, ValueError):
                    if not self.aviso_sin_cabecera:
                        self.aviso_sin_cabecera = True
                        self.log({"k": "forma_freno_ciego", "tick": tick,
                                  "cabecera": "X-Coworld-Spend-Usd",
                                  "valor": spend,
                                  "cabeceras_vistas": sorted(cab),
                                  "efecto": "el freno de gasto NO protege; "
                                            "solo queda el de 200 llamadas"})
                d = json.loads(crudo)
                txt = "".join(b.get("text", "") for b in (d.get("content") or [])
                              if b.get("type") == "text")
                fuera = {"ok": True, "codigo": rr.status, "ms": ms,
                         "texto": txt, "spend_usd": spend,
                         "usage": d.get("usage")}
            if self.n_llamadas % SPEND_CADA == 0:
                self.pide_gasto(tick, f"cada {SPEND_CADA} llamadas")
            return fuera
        except urllib.error.HTTPError as ex:
            ms = round((time.perf_counter() - t0) * 1000.0, 1)
            self.fallos += 1
            if getattr(ex, "code", None) == 429:
                self.pide_gasto(tick, "429 del sidecar")
            return {"ok": False, "ms": ms, "codigo": getattr(ex, "code", None),
                    "motivo": repr(ex)[:300]}
        except Exception as ex:
            ms = round((time.perf_counter() - t0) * 1000.0, 1)
            self.fallos += 1
            return {"ok": False, "ms": ms, "motivo": repr(ex)[:300]}

    def pide_gasto(self, tick, por_que):
        """[P5-6C · C0] El gasto por `/spend`, la ruta del sidecar.

        La cabecera `X-Coworld-Spend-Usd` es lo que el freno usa; `/spend` es
        la segunda lectura, independiente, y se escribe en el diario para poder
        cotejarlas. Se pide **cada 10 llamadas** y **en cada 429**.
        """
        import urllib.request
        if not self.ep:
            return None
        rec = {"k": "forma_spend", "tick": tick, "por_que": por_que,
               "llamadas": self.n_llamadas,
               "cabecera_usd": self.gasto_visto}
        try:
            with urllib.request.urlopen(self.ep.rstrip("/") + "/spend",
                                        timeout=CX.TIMEOUT) as rr:
                d = json.loads(rr.read(4096).decode("utf-8", "replace"))
            rec["spend"] = d
            self.gasto_spend = d
            # cuadre: si `/spend` trae un numero, se compara con la cabecera
            v = None
            for k in ("spend_usd", "total_usd", "usd", "spend"):
                if isinstance(d, dict) and isinstance(d.get(k), (int, float)):
                    v = float(d[k]); break
            if v is not None and self.gasto_visto is not None:
                rec["spend_usd"] = v
                rec["diferencia"] = round(v - self.gasto_visto, 6)
                rec["cuadra"] = abs(v - self.gasto_visto) < 1e-6
        except Exception as ex:
            rec["error"] = repr(ex)[:200]
        self.log(rec)
        return rec

    def resumen(self, tick):
        return {"k": "forma_resumen", "tick": tick,
                "llamadas": self.n_llamadas, "fallos": self.fallos,
                "citas_saltadas": self.citas_saltadas,
                "gasto_visto": self.gasto_visto,
                "gasto_spend": self.gasto_spend, "freno": self.freno,
                "freno_gasto_ciego": self.aviso_sin_cabecera,
                "callado": self.callado,
                "lat_mediana": (sorted(self.lat)[len(self.lat) // 2]
                                if self.lat else None)}


# ── el evaluador en hilo (A1: si pasa de 20 ms, no va en el bucle) ────────
class EvaluadorHilo:
    """Evalua formas fuera del bucle del juego cuando cuestan demasiado.

    No comparte estado mutable con el bucle: recibe un `trabajo` cerrado y
    deja el resultado en una caja que el bucle recoge cuando pasa por alli.
    """

    def __init__(self, log_fn):
        import threading
        self.log = log_fn
        self.lock = threading.Lock()
        self.evento = threading.Event()
        self.cola = []
        self.hechos = []
        self.en_vuelo = 0
        threading.Thread(target=self._bucle, daemon=True).start()

    def encarga(self, ident, fn):
        with self.lock:
            self.cola.append((ident, fn))
            self.en_vuelo += 1
        self.evento.set()

    def _bucle(self):
        while True:
            self.evento.wait()
            self.evento.clear()
            while True:
                with self.lock:
                    if not self.cola:
                        break
                    ident, fn = self.cola.pop(0)
                t0 = time.perf_counter()
                try:
                    r = fn()
                    err = None
                except Exception as ex:
                    r, err = None, repr(ex)[:200]
                ms = round((time.perf_counter() - t0) * 1000.0, 2)
                with self.lock:
                    self.hechos.append((ident, r, ms, err))
                    self.en_vuelo -= 1

    def recoge(self):
        with self.lock:
            h, self.hechos = self.hechos, []
        return h


# ── el alma con formas ───────────────────────────────────────────────────
class AlmaForma(PC.Alma):
    def __init__(self):
        super().__init__()
        self.cf = ConsejeroForma(log)
        self.conf = CVIVA.Confianza()
        self.vivas = []                 # [FormaViva] aceptadas
        self.cerradas = []              # para el parte (A4)
        self.n_forma = 0
        self.rnd = random.Random(AZAR_SEMILLA)
        self.herm_dicho = None          # lo ultimo que conto el hermano
        self.herm_tick = None
        self.ultimo_habla = -10 ** 9
        self.evalua_en_hilo = False
        self.hilo = EvaluadorHilo(log) if FORMA_ON else None
        self.ms_forma = []
        self.filas_mapa = None
        self.n_citas = 0
        # [P5-7C] la curiosidad por el terreno
        self.ojo = None
        self._dano_hist = []
        self._ms_bfs = 0.0
        self._cur_amenaza, self._cur_des, self._cur_dist = 0.0, {}, None
        self._cur_t0 = 0.0
        # [P5-8B] el brazo K
        self.k_fin_ultima = -10 ** 9      # tic del fin/abandono de la ultima
        self.k_nacidas = 0
        self.k_camino = {}                # id de forma -> camino BFS
        self.k_dist_min = {}              # id -> (mejor distancia, tic)
        # `_juzga` puede correr EN EL HILO; envolver un global de modulo
        # (`F._d2`) desde dos sitios a la vez seria la carrera de C1-bis otra
        # vez. Un candado propio lo serializa.
        import threading as _th
        self.k_lock = _th.Lock()
        # [P5-8H] el compromiso
        self.k_rival_dist = {}
        self.k_rupturas = __import__("collections").Counter()
        self.k_obedece = 0
        self.k_enfria = 0
        self.k_coste = []

    # ── el mapa, una vez ─────────────────────────────────────────────────
    def _filas(self):
        if self.filas_mapa is None and self.mundo is not None:
            # el mapa se llama `static_map` en `mundo.py:44` (una lista de
            # filas, `static_map[y][x]`), no `filas`.
            self.filas_mapa = list(getattr(self.mundo, "static_map", []) or [])
        return self.filas_mapa or []

    # ── el contexto que la regla necesita ────────────────────────────────
    def _contexto(self, obs, mem=None):
        rec = {"tick": self.tick, "pos": (obs.get("you") or {}).get("pos"),
               "hp": (obs.get("you") or {}).get("hp"),
               "hand": (obs.get("you") or {}).get("hand"),
               "body": (obs.get("you") or {}).get("body"),
               "pack": (obs.get("you") or {}).get("pack"),
               "effects": (obs.get("you") or {}).get("effects"),
               "move_ready_in": (obs.get("you") or {}).get("move_ready_in"),
               "attack_ready_in": obs.get("attack_ready_in")
               or (obs.get("you") or {}).get("attack_ready_in") or 0}
        e0 = P.estado_de(rec)
        suelo = {tuple(it["pos"]): it
                 for it in ((obs.get("visible") or {}).get("items") or [])
                 if it.get("pos")}
        pisos = F.pisos_rival(obs, self.mundo, mem or self.mem, self.tick)
        return e0, suelo, pisos

    def _diario_hermano(self, tics):
        """[A2] El hermano en cada punto de control: con su forma contada si es
        reciente; si no, con su ultimo estado. `None` si no hay nada."""
        if not self.herm_dicho or self.herm_tick is None:
            return None
        viejo = (self.tick - self.herm_tick) > HERMANO_VIEJO
        d = self.herm_dicho
        pos = None
        for a in ((self.ultima_obs or {}).get("visible") or {}).get("agents") or []:
            if a.get("slot") == getattr(self.mundo, "teammate_slot", None):
                pos = tuple(a.get("pos") or ())
        salida = {}
        for t in tics:
            p = pos
            if not viejo and d.get("tramos"):
                # donde estara segun SU forma contada
                for tr, tt in zip(d["tramos"], d.get("tics") or []):
                    if tt <= t and tr.get("destino"):
                        p = tuple(tr["destino"])
            if p is None:
                return None
            salida[t] = {"pos": list(p), "hp": d.get("hp"),
                         "damage_taken": []}
        return salida

    # ── A1 · evaluar una forma con la regla honesta ──────────────────────
    def _nec_curva(self, e0, obs_w, tramos, mundo, mem, suelo, tics, herm,
                   dia_h):
        """[P5-6C · C1bis] LAS NECESIDADES en cada punto de control.

        CAUSA RAIZ del parte mudo: `forma.curva_H` devuelve `tic`, `d`, `vida`,
        `W` y `pos`, y **no las necesidades**, asi que `_detalle` no podia
        rellenar «lo que el cuerpo proyecto» y escribia `?`. `forma.py` es la
        REGLA y no se toca (su md5 no cambia), asi que la proyeccion se repite
        aqui, con el mismo recorrido, solo para apuntar las necesidades.
        """
        import copy as _c
        e = F.copia_estado(e0)
        suelo_act = dict(suelo)
        out = []
        for i, tic in enumerate(tics):
            K = tic - e["tick"]
            if K < 0:
                out.append(None)
                continue
            tr = tramos[i] if i < len(tramos) else {"destino": None,
                                                    "intencion": "esperar"}
            plan = {"destino": tr.get("destino"),
                    "coger": tr.get("intencion") == "coger",
                    "usar": tr.get("item") if tr.get("intencion") == "usar"
                    else None}
            e = P.proyectar_rapido(e, plan, K, mundo, suelo_act)
            if tr.get("intencion") == "coger":
                suelo_act.pop(tuple(tr.get("destino") or ()), None)
            o = F.foto_rapida(obs_w, e, mundo, tic, list(suelo_act.values()))
            m = mem
            if dia_h is not None:
                o, m = AL.pon_hermano(o, mem, herm, dia_h.get(tic),
                                      tuple(e["pos"]), mundo)
            try:
                st, _r = A.appraise(o, mundo, m, tic)
                out.append((st.nF, st.nR, st.nS))
            except Exception:
                out.append(None)
        return out

    def nec_ahora(self, obs, mem=None):
        """Las necesidades REALES de este instante, para «lo que sintio»."""
        try:
            st, _r = A.appraise(obs, self.mundo, mem or self.mem, self.tick)
            return (st.nF, st.nR, st.nS)
        except Exception:
            return None

    # ── [P5-8K] EL MARGEN DE LA PUERTA, POR ORIGEN ───────────────────────
    # Decision de Manel: las formas que el cuerpo se propone a SI MISMO
    # (curiosidad) pasan con margen FIJO 0,02, sin la confianza C. C mide al
    # CONSEJERO —cuantas de sus formas cumplieron— y no dice nada del cuerpo,
    # asi que cargarle al cuerpo el recargo 0,06 x (1 - C) era cobrarle una
    # desconfianza ajena. Las formas del consejero NO cambian.
    # El 0,02 se IMPORTA de `confianza_viva.MARGEN_BASE`, no se cablea.
    def _margen_de(self, fv):
        if getattr(fv, "origen", "") == "curiosidad":
            return CVIVA.MARGEN_BASE
        return self.conf.margen()

    def _juzga(self, fv, obs, mem=None, blo=None):
        """[P5-6C · C1bis] `mem` y `blo` llegan COPIADOS cuando esto corre en
        el hilo: el bucle del juego los muta cada tic y 1 de 176 evaluaciones
        reventaba con `RuntimeError`."""
        import copy as _c
        mem = self.mem if mem is None else mem
        blo = self.bloqueos if blo is None else blo
        e0, suelo, pisos = self._contexto(obs, mem)
        herm = getattr(self.mundo, "teammate_slot", None)
        tics = [x[0] for x in F.puntos_de_control(e0, fv.tramos)]
        dia_h = self._diario_hermano(tics)
        FV.pon_base(lambda o, mu, me, tk: list(D.candidatos(
            o, mu, _c.deepcopy(me), tk, _c.deepcopy(blo))))
        # [P5-8B bis] LA PUERTA JUZGA Y RE-JUZGA CON LA MISMA REGLA.
        # La sonda 1 encontro que TODAS las formas morian a los 25 tics
        # exactos: nacian con el renglon de ignorancia en la proyeccion y se
        # re-juzgaban SIN el. Aqui se envuelve tambien en la reevaluacion.
        _cam = self.k_camino.get(fv.id) if CUR_FORMA_ON else None
        if _cam:
            with self.k_lock:
                _orig, _p = CFM.con_renglon(self.ojo, self.mundo, _cam, tics,
                                            self.tick, self._cur_amenaza)
                try:
                    ver, ar, cf, tics = FV.evalua(
                        fv, F, e0, obs, self.mundo, mem, suelo, herm, dia_h,
                        pisos, self._margen_de(fv), self.tick)
                finally:
                    CFM.restaura(_orig)
        else:
            ver, ar, cf, tics = FV.evalua(fv, F, e0, obs, self.mundo, mem,
                                          suelo, herm, dia_h, pisos,
                                          self._margen_de(fv), self.tick)
        # y las necesidades, que son lo que el parte necesita
        fv.nec0 = self.nec_ahora(obs, mem)
        try:
            nec = self._nec_curva(e0, obs, fv.tramos, self.mundo, mem, suelo,
                                  tics, herm, dia_h)
            for i, p in enumerate(cf or []):
                if i < len(nec):
                    p["nec"] = nec[i]
        except Exception:
            pass
        return ver, ar, cf, tics

    def _acepta_o_no(self, fv, obs, ms_previo=0.0):
        t0 = time.perf_counter()
        ver, ar, cf, tics = self._juzga(fv, obs)
        ms = round((time.perf_counter() - t0) * 1000.0, 2)
        self.ms_forma.append(ms)
        if ms > MS_AL_HILO and not self.evalua_en_hilo:
            self.evalua_en_hilo = True
            log({"k": "hilo_forma", "tick": self.tick, "estado": "encendido",
                 "ms": ms, "tope": MS_AL_HILO,
                 "efecto": "las evaluaciones siguientes van al hilo, "
                           "no al bucle del juego"})
        fv.curva, fv.tics, fv.ventaja = cf, tics, ar
        log({"k": "forma_evaluada", "tick": self.tick, "id": fv.id,
             "origen": fv.origen, "veredicto": ver, "ventaja": round(ar, 5),
             "margen": round(self._margen_de(fv), 4),
             "C": round(self.conf.C, 4),
             "ms": ms, "tramos": len(fv.tramos)})
        if ver != "ok":
            fv.estado = "rechazada"
            self.cerradas.append(dict(fv.registro(),
                                      estado="rechazada_" + str(ver),
                                      tramos_detalle=self._detalle(fv)))
            return False
        fv.estado = "aceptada"
        self.vivas.append(fv)
        log({"k": "forma_aceptada", "tick": self.tick, **fv.registro()})
        if HILO_ON:
            self._habla(obs, forzado=True)
        return True

    def _detalle(self, fv):
        """[A4] Por tramo: lo dicho, lo proyectado y lo sentido de verdad.

        [P5-6C · C1bis] El tramo `i` va del punto de control `i-1` al `i`, no
        del `i` al `i+1`: antes el parte comparaba el tramo siguiente. Para el
        primero, el punto de partida es el estado del instante en que se juzgo
        (`fv.nec0`).
        """
        out = []
        nec0 = getattr(fv, "nec0", None)
        real = getattr(fv, "real", None) or {}
        for i, tr in enumerate(fv.tramos):
            d = {"i": i + 1, "dicho": dict(tr.get("_mitad") or {}),
                 "por": tr.get("_por"), "porque": tr.get("_porque")}
            if i < len(fv.curva):
                a = nec0 if i == 0 else (fv.curva[i - 1] or {}).get("nec")
                b = (fv.curva[i] or {}).get("nec")
                sg = _signos(a, b)
                if sg:
                    d["proyectado"] = sg
            if i in real:
                d["real"] = real[i]
            out.append(d)
        return out

    # ── A1 · revisar las vivas ───────────────────────────────────────────
    def _revisa_vivas(self, obs):
        if CUR_FORMA_ON:
            self._abandonos_K(obs)
        hp = (obs.get("you") or {}).get("hp")
        quedan = []
        for fv in self.vivas:
            # [P5-8D · R2] antes de la llegada proyectada no se examina
            _na = getattr(fv, "no_antes_de", None)
            if _na is not None and self.tick < _na:
                quedan.append(fv)
                continue
            if not fv.toca_revisar(self.tick):
                quedan.append(fv)
                continue
            cae, motivo = fv.falla_lo_previsto(hp, self._filas(), self.tick)
            if cae:
                fv.cae(motivo, self.tick)
                log({"k": "forma_caida", "tick": self.tick, "id": fv.id,
                     "motivo": motivo})
                self._cierra(fv, mal=True)
                continue
            # ¿alcanzo un punto de control? -> confianza por resultados (A3)
            if fv.tics and fv.i_punto < len(fv.tics) \
                    and self.tick >= fv.tics[fv.i_punto]:
                d_real = self._d_ahora(obs)
                d_proy = (fv.curva[fv.i_punto].get("d")
                          if fv.i_punto < len(fv.curva) else None)
                v, ca, cb = self.conf.comprueba(d_real, d_proy, self.tick,
                                                fv.id, fv.i_punto)
                if v is not None:
                    if v == "fallo":
                        fv.malos += 1
                    log({"k": "confianza", "tick": self.tick, "id": fv.id,
                         "punto": fv.i_punto, "veredicto": v,
                         "d_real": round(d_real, 5), "d_proyectada": round(d_proy, 5),
                         "C_antes": round(ca, 4), "C": round(cb, 4),
                         "margen": round(self.conf.margen(), 4)})
                # [C1bis] lo que el cuerpo sintio DE VERDAD en ese tramo
                n_ahora = self.nec_ahora(obs)
                if not hasattr(fv, "real_nec"):
                    fv.real_nec, fv.real = {}, {}
                ant = fv.real_nec.get(fv.i_punto - 1,
                                      getattr(fv, "nec0", None))
                fv.real_nec[fv.i_punto] = n_ahora
                sg = _signos(ant, n_ahora)
                if sg:
                    fv.real[fv.i_punto] = sg
                fv.avanza_punto(self.tick)
                if fv.estado == "cumplida":
                    self._cierra(fv, mal=bool(fv.malos))
                    continue
            # reevaluacion: ¿sigue ganando?
            ver, ar, cf, tics = self._juzga(fv, obs)
            fv.ultima_revision = self.tick
            if ver != "ok":
                fv.cae(f"en la reevaluacion deja de ganar ({ver})", self.tick)
                log({"k": "forma_caida", "tick": self.tick, "id": fv.id,
                     "motivo": fv.motivo_caida})
                self._cierra(fv, mal=True)
                continue
            fv.ventaja = ar
            quedan.append(fv)
        self.vivas = quedan

    def _cierra(self, fv, mal):
        callo = self.conf.forma_cerrada(mal, self.tick)
        self.cerradas.append(dict(fv.registro(),
                                  tramos_detalle=self._detalle(fv)))
        if callo:
            log({"k": "confianza", "tick": self.tick,
                 "suceso": "el cuerpo calla al consejero",
                 "hasta": self.conf.callado_hasta, "C": round(self.conf.C, 4),
                 "malas": self.conf.malas})

    def _d_ahora(self, obs):
        try:
            st, _r = A.appraise(obs, self.mundo, self.mem, self.tick)
            from motor.model import opponent_distance, DEFAULT_CONFIG
            return round(opponent_distance(st, DEFAULT_CONFIG), 5)
        except Exception:
            return None

    # ── A5 · el brazo T ──────────────────────────────────────────────────
    def _forma_al_azar(self, obs):
        you = obs.get("you") or {}
        suelo = {tuple(it["pos"]): it
                 for it in ((obs.get("visible") or {}).get("items") or [])
                 if it.get("pos")}
        tramos = FAZ.forma_al_azar(tuple(you.get("pos") or ()), self._filas(),
                                   suelo, self.rnd)
        self.n_forma += 1
        return FV.FormaViva(self.n_forma, tramos, self.tick, origen="azar")

    # ── A1/A4 · la cita ──────────────────────────────────────────────────
    # ── [P5-8B] LOS DOS ABANDONOS NUEVOS DEL BRAZO K ─────────────────────
    def _pon_desvio(self, fv, pos):
        """[P5-8M] `fv.desvio` = la casilla siguiente del rodeo. None al final."""
        cam = self.k_camino.get(fv.id) or []
        if not cam:
            fv.desvio = None
            return
        try:
            i = cam.index(tuple(pos))
        except ValueError:
            i = -1
        fv.desvio = tuple(cam[i + 1]) if 0 <= i < len(cam) - 1 else None

    def _abandonos_K(self, obs):
        """(b) veto duro por armado que cubre el camino restante · (c) atasco.

        El abandono (a) por checkpoint lo hace la regla de la puerta en
        `_revisa_vivas`, sin tocarla.
        """
        if not self.vivas or self.mundo is None:
            return
        pos = tuple((obs.get("you") or {}).get("pos") or ())
        if not pos:
            return
        r = self._como_registro(obs)
        herm = self.mundo.teammate_slot
        quedan = []
        for fv in self.vivas:
            # [P5-8M] la que va rodeando apunta cada tic a la casilla
            # siguiente de SU rodeo; las demas, al destino de siempre.
            if getattr(fv, "rodeos", 0):
                self._pon_desvio(fv, pos)
            cam = self.k_camino.get(fv.id) or []
            # el trozo de camino que queda por delante
            try:
                i = cam.index(pos)
            except ValueError:
                i = 0
            resto = cam[i:] or cam
            dest = tuple(cam[-1]) if cam else None
            # [P5-8D] COMPLETADA POR ALIVIO: la promesa cobrada, o el destino
            # ya visto. Es una causa de FIN, no de caida.
            _pr = getattr(fv, "promesa", None)
            if _pr is not None and self.ojo is not None:
                _baja = getattr(fv, "ign_nace", 0.0) - self.ojo.ignorancia_global()
                _visto = (getattr(fv, "destino_cur", None) in
                          self.ojo.primera_vez)
                if (_pr > 0 and _baja >= _pr) or _visto:
                    fv.estado = "cumplida"
                    fv.motivo_caida = None
                    log({"k": "forma_caida", "tick": self.tick, "id": fv.id,
                         "origen": fv.origen, "motivo": "completada por alivio",
                         "baja": round(_baja, 5), "promesa": round(_pr, 5),
                         "destino_visto": bool(_visto),
                         "vive": self.tick - fv.nace})
                    self._cierra(fv, mal=False)
                    self.k_fin_ultima = self.tick
                    self.k_camino.pop(fv.id, None)
                    self.k_dist_min.pop(fv.id, None)
                    continue
            # (b) VETO DURO — [P5-8M] RODEAR EN VEZ DE ABANDONAR
            #
            # Decision de Manel: ver a alguien no rompe el compromiso; que
            # venga hacia ti, si. P5-8L midio que 101 de 103 vetos saltaban el
            # tic en que el armado se hacia VISIBLE, no cuando se acercaba, y
            # que solo 1 de 103 fue seguido de dano. Asi que con un armado que
            # NO se acerca se busca rodeo al MISMO destino; si no lo hay o es
            # mas de TOPE_RODEO veces lo que quedaba, se abandona.
            if dest is not None and CFM.abandona_por_peligro(
                    dest, resto, r, self.mundo, herm):
                cubs = CFM.cubridores(resto, r, self.mundo, herm)
                # ¿alguno SE ACERCA? La misma definicion que la ruptura (e):
                # su distancia de AHORA contra la del tic anterior. Aqui
                # `k_rival_dist` es todavia la del tic previo, porque
                # `_compromiso` la actualiza despues de decidir.
                viene = False
                for a in cubs:
                    q = tuple(a.get("pos") or ())
                    if not q:
                        continue
                    d_ah = max(abs(pos[0] - q[0]), abs(pos[1] - q[1]))
                    d_an = (self.k_rival_dist or {}).get(a.get("slot"))
                    if d_an is not None and d_ah < d_an:
                        viene = True
                        break
                if viene:
                    fv.cae("veto duro: un armado cubre el camino restante",
                           self.tick)
                    log({"k": "forma_caida", "tick": self.tick, "id": fv.id,
                         "origen": fv.origen, "motivo": "veto duro",
                         "causa": "armado que SE ACERCA cubre el camino"})
                    self._cierra(fv, mal=True)
                    self.k_fin_ultima = self.tick
                    self.k_camino.pop(fv.id, None)
                    self.k_dist_min.pop(fv.id, None)
                    continue
                # NO viene: se intenta el rodeo, con la misma sombra
                arms = CFM.armados(r, self.mundo, herm)
                rod, largo = CFM.camino_a_destino(self.mundo, pos, dest, arms)
                queda = max(1, len(resto) - 1)
                if rod is None or largo > CFM.TOPE_RODEO * queda:
                    fv.cae("sin rodeo: el armado cubre y no hay vuelta",
                           self.tick)
                    log({"k": "forma_caida", "tick": self.tick, "id": fv.id,
                         "origen": fv.origen, "motivo": "sin rodeo",
                         "causa": ("no hay camino fuera de sombra"
                                   if rod is None else "el rodeo es demasiado largo"),
                         "queda": queda,
                         "largo_rodeo": largo,
                         "tope": round(CFM.TOPE_RODEO * queda, 2)})
                    self._cierra(fv, mal=True)
                    self.k_fin_ultima = self.tick
                    self.k_camino.pop(fv.id, None)
                    self.k_dist_min.pop(fv.id, None)
                    continue
                # RODEA: camino nuevo, reloj honesto nuevo
                _paso = self.mundo.coste_movimiento(
                    PC.CONSTITUCION.get("speed", 5))
                self.k_camino[fv.id] = rod
                fv.no_antes_de = self.tick + largo * _paso
                fv.rodeos = getattr(fv, "rodeos", 0) + 1
                # DECLARADO: el reloj del ATASCO se reinicia tambien. Sin esto
                # el rodeo muere por atasco por construccion —alejarse del
                # destino tres casillas son 33 tics, que es el plazo entero—,
                # y la decision de rodear quedaria muerta al nacer. Es
                # consecuencia del encargo, no una decision nueva, y va
                # declarada en el informe.
                self.k_dist_min[fv.id] = (
                    max(abs(pos[0] - dest[0]), abs(pos[1] - dest[1])),
                    self.tick)
                self._pon_desvio(fv, pos)
                log({"k": "rodeo", "tick": self.tick, "id": fv.id,
                     "desvio": (list(fv.desvio) if getattr(fv, "desvio", None)
                                else None),
                     "destino": list(dest), "queda": queda,
                     "largo_rodeo": largo,
                     "extra": largo - queda,
                     "cubridores": [a.get("slot") for a in cubs],
                     "rodeos": fv.rodeos,
                     "no_antes_de": fv.no_antes_de})
                quedan.append(fv)
                continue
            # (c) ATASCO: tres pasos del mundo sin acercarse una casilla
            if dest is not None:
                d = max(abs(pos[0] - dest[0]), abs(pos[1] - dest[1]))
                mejor, t_mejor = self.k_dist_min.get(fv.id, (d, self.tick))
                if d < mejor:
                    self.k_dist_min[fv.id] = (d, self.tick)
                elif self.tick - t_mejor >= getattr(
                        fv, "atasco_plazo", CUR_ATASCO_PASOS * 11):
                    _pl = getattr(fv, "atasco_plazo", None)
                    fv.cae(f"atasco: {_pl} tics ({CUR_ATASCO_PASOS} pasos) "
                           f"sin acercarse una casilla", self.tick)
                    log({"k": "forma_caida", "tick": self.tick, "id": fv.id,
                         "origen": fv.origen, "motivo": "atasco",
                         "dist": d, "mejor": mejor,
                         "tics": self.tick - t_mejor,
                         "plazo": getattr(fv, "atasco_plazo", None)})
                    self._cierra(fv, mal=True)
                    self.k_fin_ultima = self.tick
                    self.k_camino.pop(fv.id, None)
                    self.k_dist_min.pop(fv.id, None)
                    continue
            quedan.append(fv)
        self.vivas = quedan

    # ── [P5-8B] EL BRAZO K: la cita de la curiosidad ─────────────────────
    def _cita_curiosidad(self, obs):
        """Cada tic: si toca, nace una forma de curiosidad y la puerta la juzga.

        Los mandos (disparo, refractario, consigna) son los de P5-8B; la
        PUERTA es la de P5-6C sin tocar, con el renglon de ignorancia dentro
        de la proyeccion. Nadie llama a ningun modelo.
        """
        if self.vivas:
            return                      # hay forma activa
        if self.tick - self.k_fin_ultima < CUR_REFRACTARIO:
            return                      # refractario
        if self.ojo is None or self.mundo is None:
            return
        r = self._como_registro(obs)
        am = self._cur_amenaza
        if am >= CFM.UMBRAL_SEGURO:
            return
        if self.ojo.ignorancia_global() <= CUR_CONSIGNA:
            return
        pos = tuple((obs.get("you") or {}).get("pos") or ())
        if not pos:
            return
        arms = CFM.armados(r, self.mundo, self.mundo.teammate_slot)
        # VETO VITAL: con un armado A TIRO, esto no opina
        if any(max(abs(pos[0] - a[0]), abs(pos[1] - a[1])) <= rg
               for a, rg in arms):
            log({"k": "cur_forma_saltada", "tick": self.tick,
                 "motivo": "armado a tiro"})
            return
        _a = time.perf_counter()
        cam, dist, dest = CFM.camino_a_frontera(self.ojo, self.mundo, pos,
                                                arms)
        ms_bfs = (time.perf_counter() - _a) * 1000.0
        if dest is None:
            log({"k": "cur_forma_saltada", "tick": self.tick,
                 "motivo": "sin frontera segura", "ms": round(ms_bfs, 3)})
            return
        self.n_forma += 1
        self.k_nacidas += 1
        tramos = [{"destino": list(dest), "intencion": "ver", "esperar": 0}]
        fv = FV.FormaViva(self.n_forma, tramos, self.tick, origen="curiosidad")
        # [P5-8D · R2] EL RELOJ HONESTO. El primer examen no cae antes del tic
        # de LLEGADA proyectada. P5-8C midio que las 23 formas tardan mas de
        # 25 tics en llegar (mediana 66): se las examinaba a un tercio del
        # camino. El paso se LEE del mundo, no se cablea.
        _paso = self.mundo.coste_movimiento(PC.CONSTITUCION.get("speed", 5))
        fv.no_antes_de = self.tick + dist * _paso
        fv.atasco_plazo = CUR_ATASCO_PASOS * _paso
        # [P5-8D] LA PROMESA: la bajada de ignorancia global proyectada al
        # llegar. Si se cobra antes, la forma esta CUMPLIDA, no caida.
        _vis = set(self.ojo.primera_vez)
        for _q in cam:
            _vis |= self.ojo.vistas_desde(_q)
        _ign0 = self.ojo.ignorancia_global()
        fv.promesa = max(0.0, _ign0 - (1.0 - len(_vis) / float(self.ojo.n_arena)))
        fv.ign_nace = _ign0
        fv.destino_cur = tuple(dest)
        try:
            fv.W_nace = float(A.riqueza_W(obs.get("you") or {}, self.mundo)[0])
        except Exception:
            fv.W_nace = None
        self.k_camino[fv.id] = cam
        self.k_dist_min[fv.id] = (dist, self.tick)
        log({"k": "forma_propuesta", "tick": self.tick, "origen": "curiosidad",
             "id": fv.id, "destino": list(dest), "dist": dist,
             "ign": round(self.ojo.ignorancia_global(), 5),
             "amenaza": round(am, 5), "ms_bfs": round(ms_bfs, 3),
             "W": round(float(A.riqueza_W(obs.get("you") or {},
                                          self.mundo)[0]), 4),
             "plazo_atasco": fv.atasco_plazo,
             "no_antes_de": fv.no_antes_de})
        # LA PUERTA, con el renglon dentro de la proyeccion
        # EL RENGLON YA NO SE ENVUELVE AQUI: desde P5-8B bis lo hace `_juzga`,
        # que es quien juzga Y re-juzga. Envolver en los dos sitios anidaria
        # los envoltorios y SUMARIA EL RENGLON DOS VECES. `k_camino` ya esta
        # puesto, que es lo que `_juzga` necesita para saber que es curiosidad.
        self._acepta_o_no(fv, obs)
        if fv.estado != "aceptada":
            self.k_fin_ultima = self.tick
            self.k_camino.pop(fv.id, None)
            self.k_dist_min.pop(fv.id, None)

    def _como_registro(self, obs):
        """La observacion viva, con la forma del registro del diario, que es
        lo que `curiosidad_forma` y `curiosidad` saben leer."""
        you = obs.get("you") or {}
        vis = obs.get("visible") or {}
        return {"pos": list(you.get("pos") or ()), "hp": you.get("hp"),
                "damage_taken": you.get("damage_taken") or [],
                "ve_agentes": list(vis.get("agents") or []),
                "ve_items": list(vis.get("items") or []),
                "ve_proyectiles": list(vis.get("projectiles") or [])}

    def _cita(self, obs, radio):
        if self.conf.callado(self.tick):
            log({"k": "forma_cita_saltada", "tick": self.tick,
                 "motivo": "el cuerpo calla al consejero",
                 "hasta": self.conf.callado_hasta})
            return
        self.n_citas += 1
        if AZAR_ON and not CONSEJERO_ON:
            fv = self._forma_al_azar(obs)
            log({"k": "forma_propuesta", "tick": self.tick, "origen": "azar",
                 "id": fv.id, "tramos": len(fv.tramos)})
            self._acepta_o_no(fv, obs)
            return
        if not CONSEJERO_ON:
            return
        try:
            e = self._escena_relator(obs, radio)
            relato = RT.relato(e, True)
        except Exception as ex:
            log({"k": "forma_error", "tick": self.tick, "donde": "relato",
                 "error": repr(ex)[:200]})
            return
        parte = parte_de_formas(self.cerradas, self.conf.C, self.conf.margen())
        log({"k": "parte", "tick": self.tick, "texto": parte,
             "C": round(self.conf.C, 4), "margen": round(self.conf.margen(), 4),
             "cerradas": len(self.cerradas)})
        you = obs.get("you") or {}
        escena = {"pos": list(you.get("pos") or ()),
                  "suelo": [{"id": it.get("id"), "pos": list(it["pos"])}
                            for it in ((obs.get("visible") or {}).get("items") or [])
                            if it.get("pos")]}
        self.cf.pide({"tick": self.tick, "relato": relato, "parte": parte,
                      "escena": escena, "filas": self._filas(),
                      "reloj": (lambda: self.tick)})

    def _escena_relator(self, obs, radio):
        """La `e` del relator, como la arma `policy_cortex._foto`."""
        rec = dict(self.ultimo_rec or {})
        import copy as _c
        cands = D.candidatos(obs, self.mundo, _c.deepcopy(self.mem),
                             self.tick, _c.deepcopy(self.bloqueos))
        recetas = {}
        for n, r in cands:
            recetas[n] = {"tipo": r.get("tipo"), "dir": r.get("dir"),
                          "destino": list(r["destino"]) if r.get("destino") else None,
                          "objetivo": r.get("objetivo"),
                          "item": ((r.get("item") or {}).get("id")
                                   if isinstance(r.get("item"), dict)
                                   else r.get("item"))}
        e = {"r": rec, "pc_teammate": getattr(self.mundo, "teammate_slot", None),
             "recetas": recetas,
             "cuerpo": {k: ({"d": v["d"], "movs": v.get("movs")}
                            if isinstance(v, dict) else {"d": v, "movs": None})
                        for k, v in radio["candidatos"].items()},
             "cert": A.agresor_de_la_hermana(obs, self.mundo, self.mem, self.tick),
             "parte_fresco": (None if self.mem.parte_fresco(self.tick) is None
                              else int(self.tick
                                       - self.mem.parte_fresco(self.tick)["t"])),
             "agresores_det": (radio.get("ahora") or {}).get("agresores") or [],
             "_recetas_vivas": {n: dict(r) for n, r in cands},
             "_cuerpos": frozenset(tuple(a.get("pos") or ()) for a in
                                   ((obs.get("visible") or {}).get("agents") or [])
                                   if a.get("pos")),
             "_objetos": dict(self.mem.objetos_vistos)}
        gh = self._golpe_hermano(obs)
        if gh is not None:
            e["_golpe_hermano"] = gh[0]
            e["_receta_golpe_hermano"] = gh[1]
        return e

    def _recoge(self, obs):
        """Lo que el hilo del consejero haya dejado."""
        e = self.cf.recoge()
        if not e:
            return
        if e.get("callar") and not e.get("formas"):
            log({"k": "forma_evaluada", "tick": self.tick,
                 "veredicto": "el consejero callo", "origen": "consejero"})
            return
        for tramos_forma in e["formas"]:
            self.n_forma += 1
            fv = FV.FormaViva(self.n_forma, tramos_forma["tramos"], self.tick,
                              origen="consejero")
            if self.evalua_en_hilo and self.hilo is not None:
                import copy as _c
                _m, _b = _c.deepcopy(self.mem), _c.deepcopy(self.bloqueos)
                self.hilo.encarga(
                    fv.id,
                    lambda f=fv, o=obs, m=_m, b=_b: self._juzga(f, o, m, b))
                log({"k": "hilo_forma", "tick": self.tick, "id": fv.id,
                     "estado": "encargada al hilo"})
                self.pendientes = getattr(self, "pendientes", {})
                self.pendientes[fv.id] = fv
            else:
                self._acepta_o_no(fv, obs)

    def _recoge_hilo(self, obs):
        if self.hilo is None:
            return
        for ident, r, ms, err in self.hilo.recoge():
            fv = getattr(self, "pendientes", {}).pop(ident, None)
            if fv is None:
                continue
            if err or r is None:
                log({"k": "hilo_forma", "tick": self.tick, "id": ident,
                     "estado": "error", "error": err})
                continue
            ver, ar, cf, tics = r
            fv.curva, fv.tics, fv.ventaja = cf, tics, ar
            log({"k": "hilo_forma", "tick": self.tick, "id": ident,
                 "estado": "vuelta del hilo", "ms": ms, "veredicto": ver})
            log({"k": "forma_evaluada", "tick": self.tick, "id": fv.id,
                 "origen": fv.origen, "veredicto": ver, "ventaja": round(ar, 5),
                 "margen": round(self._margen_de(fv), 4),
                 "C": round(self.conf.C, 4), "ms": ms,
                 "tramos": len(fv.tramos), "en_hilo": True})
            if ver == "ok":
                fv.estado = "aceptada"
                self.vivas.append(fv)
                log({"k": "forma_aceptada", "tick": self.tick, **fv.registro()})
            else:
                fv.estado = "rechazada"
                self.cerradas.append(dict(fv.registro(),
                                          estado="rechazada_" + str(ver),
                                          tramos_detalle=self._detalle(fv)))

    # ── A2 · el hilo del hermano ─────────────────────────────────────────
    def texto_hilo(self, obs=None):
        """[A2] Lo que sale por el canal `team`, en el hueco del hilo actual.

        DECLARADO: el canal deja 1 mensaje cada 24 tics, asi que NO se manda el
        parte de estado del cuatro y el de la forma a la vez. Con
        `GEMV_HILO_FORMA=1` el mensaje del hilo ES la forma; con el apagado,
        sigue siendo el parte de siempre.
        """
        o = obs or self.ultima_obs or {}
        you = o.get("you") or {}
        fv = self.vivas[0] if self.vivas else None
        tramos = fv.tramos if fv else []
        tics = fv.tics if fv else []
        try:
            W = A.riqueza_W(you, self.mundo)[0]
        except Exception:
            W = 0.0
        hp = you.get("hp")
        s, ok = HF.codifica(tramos, hp, W, (hp if hp is not None else 100) < 100,
                            tics)
        if not ok:
            log({"k": "hilo_forma", "tick": self.tick, "estado": "no cabe",
                 "largo": len(s)})
            return None
        log({"k": "hilo_forma", "tick": self.tick, "estado": "dicho",
             "texto": s, "largo": len(s), "con_forma": bool(fv)})
        return s

    def _habla(self, obs, forzado=False):
        """Al aceptar una forma se FUERZA la proxima emision del hilo."""
        if not HILO_ON or not forzado:
            return
        self.ultima_voz = self.tick - PC.VOZ_CADA

    def _oye(self, obs):
        if not HILO_ON:
            return
        herm = getattr(self.mundo, "teammate_slot", None)
        for m in (obs.get("chat") or []):
            if m.get("from") not in (herm, None):
                continue
            d = HF.decodifica(m.get("text") or "")
            if d is None:
                continue
            self.herm_dicho, self.herm_tick = d, self.tick
            log({"k": "hilo_forma", "tick": self.tick, "estado": "oido",
                 "de": m.get("from"), "tramos": len(d["tramos"]),
                 "hp": d["hp"], "W": d["W"]})

    # ── el bucle de decision ─────────────────────────────────────────────
    def decidir(self, obs):
        """Despachador: la curiosidad envuelve; dentro, la politica de siempre.

        Con `GEMV_CURIOSIDAD` vacio esto es una llamada directa, asi que la
        conducta es byte a byte la de antes del anadido.
        """
        if not (CURIOSIDAD_ON or CUR_FORMA_ON):
            return self._decidir_forma(obs)
        # el brazo K necesita el OJO y la AMENAZA, pero NO el renglon de un
        # paso: la curiosidad va en la forma, no en cada decision.
        fue = self._curiosidad_antes(obs)
        accion, radio = self._decidir_forma(obs)
        if fue and CURIOSIDAD_ON:
            self._curiosidad_despues(obs, radio)
        elif fue:
            CUR_MOD.CUR.on = False
        return accion, radio

    # ── [P5-7C] LA CURIOSIDAD, alrededor de la decision ──────────────────
    def _curiosidad_antes(self, obs):
        """Prepara el renglon para ESTE tic. True si hay que registrarlo."""
        self._cur_t0 = time.perf_counter()
        if (obs.get("phase") or self.phase) != "live":
            return False
        pos = tuple((obs.get("you") or {}).get("pos") or ())
        if not pos or self.mundo is None:
            return False
        tick = obs.get("tick", self.tick)
        if self.ojo is None:
            # la constitucion es la sellada por Manel, del modulo del cuatro
            self.ojo = CUR_MOD.Ojo(self.mundo,
                                   PC.CONSTITUCION.get("intelligence", 8))
            if CURIOSIDAD_ON:
                CUR_MOD.instala()
            CUR_MOD.CUR.modo = CURIOSIDAD
            CUR_MOD.CUR.k = CURIOSIDAD_K
            CUR_MOD.CUR.balanza = CURIOSIDAD_BALANZA
            CUR_MOD.CUR.ojo = self.ojo
        self.ojo.mira(pos, tick)
        self._dano_hist.append((tick, sum(
            float(x.get("amount") or 0) if isinstance(x, dict) else float(x or 0)
            for x in ((obs.get("you") or {}).get("damage_taken") or []))))
        if len(self._dano_hist) > 400:
            del self._dano_hist[:200]
        d100 = sum(v for (t, v) in self._dano_hist
                   if tick - t < CUR_MOD.VENTANA_DANO)
        _r = {"pos": list(pos),
              "ve_agentes": [a for a in ((obs.get("visible") or {}).get("agents")
                                         or [])]}
        am, des = CUR_MOD.amenaza(_r, self.mundo, self.mundo.teammate_slot,
                                  d100, tick)
        C = CUR_MOD.CUR
        C.amenaza_ahora = am
        C.ign_global = self.ojo.ignorancia_global()
        _a = time.perf_counter()
        C.dist_frontera = (CUR_MOD.dist_a_frontera(self.ojo, self.mundo)
                           if (CURIOSIDAD_ON and CURIOSIDAD == "frontera")
                           else {})
        self._ms_bfs = (time.perf_counter() - _a) * 1000.0
        self._cur_amenaza, self._cur_des = am, des
        self._cur_dist = C.dist_frontera.get(pos)
        C.on = bool(CURIOSIDAD_ON)
        C.reinicia_cuentas()
        return True

    def _curiosidad_despues(self, obs, radio):
        """¿Decidio el renglon? Contrafactual, y el registro del tic."""
        C = CUR_MOD.CUR
        encendio = C.n_valor_pos > 0
        decidio = None
        ms_cf = 0.0
        if encendio and radio is not None:
            # SOLO cuando el renglon se encendio: con el apagado la decision
            # es la de siempre, asi que no hay nada que comparar.
            _a = time.perf_counter()
            C.on = False
            try:
                _ac, _rb = D.decide(obs, self.mundo, self.mem, self.tick,
                                    self.bloqueos)
                decidio = (_rb["elegido"] != radio.get("elegido"))
            except Exception:
                decidio = None
            finally:
                C.on = True
            ms_cf = (time.perf_counter() - _a) * 1000.0
        C.on = False
        log({"k": "curiosidad_tic", "tick": self.tick,
             "ign_global": round(C.ign_global, 5),
             "dist_frontera": self._cur_dist,
             "amenaza": round(self._cur_amenaza, 5),
             "grado": CUR_MOD.grado(self._cur_amenaza),
             "amenaza_desglose": self._cur_des,
             "encendio": encendio, "decidio": decidio,
             "cands_con_M": C.n_valor_pos, "cands": C.n_valor,
             "max_M": round(C.max_M, 5),
             "vistas": len(self.ojo.primera_vez),
             "ms_bfs": round(self._ms_bfs, 3),
             "ms_contrafactual": round(ms_cf, 3),
             # EL COSTE DEL TIC ENTERO: preparacion + BFS + decision +
             # contrafactual. Es la vara de Q5; el `ms` del decisor solo no lo
             # es, porque deja fuera lo que anade la curiosidad.
             "ms_total": round((time.perf_counter() - self._cur_t0) * 1000.0,
                               3)})

    def _decidir_forma(self, obs):
        """Con `GEMV_FORMA=0` esto es, literalmente, la politica del cuatro."""
        if not FORMA_ON:
            return super().decidir(obs)
        self.tick = obs.get("tick", self.tick)
        self.phase = obs.get("phase", self.phase)
        _mt = getattr(self.mundo, "max_ticks", 0) or 0
        if _mt and self.tick >= 0.95 * _mt and not self.artefacto_subido:
            PC.sube_artefacto(self, f"red al 95 % de max_ticks ({_mt})")
        self.mem.observa(obs, self.mundo, self.tick)
        self.bloqueos.actualiza(obs, self.mundo, self.ultima_accion, self.tick)
        if self.phase != "live":
            return dict(PC.NONE_ACTION), None
        t0 = time.perf_counter()
        self.ultima_obs = obs
        self._oye(obs)
        self._recoge_hilo(obs)
        self._recoge(obs)
        self._revisa_vivas(obs)

        # ── LA INYECCION: el primer tramo de la forma aceptada ───────────
        _orig = D.candidatos
        caja = {"nuevos": [], "vetadas": [], "respaldo": [], "de": {}}
        if self.vivas:
            _vv = list(self.vivas)

            def _c(o, mu, me, tk, bl=None, _o=_orig, _v=_vv, _k=caja):
                base = list(_o(o, mu, me, tk, bl))
                nom = {c[0] for c in base}
                for k in ("nuevos", "vetadas", "respaldo"):
                    _k[k] = []
                _k["de"] = {}
                fuera = []
                for fv in _v:
                    n = fv.nombre()
                    rec = fv.receta(o, me)
                    _k["de"][fv.id] = n
                    if n in nom or rec.get("tipo") == "esperar":
                        _k["respaldo"].append(fv.id)
                        continue
                    if PC._veta_receta(bl, rec, o, tk):
                        _k["vetadas"].append(fv.id)
                        continue
                    _k["nuevos"].append(fv.id)
                    fuera.append((n, rec))
                return base + fuera
            D.candidatos = _c
        _ced0, _ua0 = dict(self.mem.cedidos), self.mem.ultimo_ataque
        try:
            accion, radio = D.decide(obs, self.mundo, self.mem, self.tick,
                                     self.bloqueos)
        finally:
            D.candidatos = _orig

        # ── LA VENTAJA DEL AREA, como en el banco ────────────────────────
        # `D.decide` ordena por `d` cruda; la ventaja del area se aplica FUERA,
        # igual que `banco_forma3.compite`: `d_ajustada = d - max(0, ventaja)`.
        # Si con ella la forma gana ESTRICTAMENTE, se emite su accion, armada
        # con `decisor_zs._a_json` — leer la API del decisor, no tocarla.
        # DECLARADO: al cambiar de candidato se deshacen las dos escrituras de
        # memoria del epilogo de `decide` (`cedidos` y `ultimo_ataque`), que
        # eran del candidato que ya no se emite. El primer tramo de una forma
        # es siempre un `ir`, que no escribe ninguna de las dos.
        self.cx_empate = False
        self.cx_ventaja = False
        if caja["nuevos"]:
            _cds = {k: (v["d"] if isinstance(v, dict) else v)
                    for k, v in radio["candidatos"].items()}
            _iny = {caja["de"][i] for i in caja["nuevos"]}
            _prop = {k: v for k, v in _cds.items() if k not in _iny}
            _porid = {caja["de"][f.id]: f for f in self.vivas
                      if f.id in caja["nuevos"]}
            if _prop:
                _mj = min(_prop, key=_prop.get)
                _aj = {n: _cds[n] - max(0.0, _porid[n].ventaja)
                       for n in _iny if n in _cds}
                _gn = min(_aj, key=_aj.get) if _aj else None
                if _gn is not None and _aj[_gn] < _prop[_mj] - 1e-9:
                    # la forma GANA con su ventaja
                    if radio["elegido"] != _gn:
                        self.mem.cedidos, self.mem.ultimo_ataque = _ced0, _ua0
                        _rec = _porid[_gn].receta(obs, self.mem)
                        accion = D._a_json(_gn, _rec,
                                           tuple((obs.get("you") or {}).get("pos") or ()),
                                           self.mundo, self.mem, self.tick)
                        radio["elegido_cuerpo"] = radio["elegido"]
                        radio["elegido"] = _gn
                        self.cx_ventaja = True
                    log({"k": "forma_gana", "tick": self.tick, "forma": _gn,
                         "d": round(_cds[_gn], 5),
                         "ventaja": round(_porid[_gn].ventaja, 5),
                         "d_ajustada": round(_aj[_gn], 5),
                         "mejor_propio": _mj,
                         "d_mejor_propio": round(_prop[_mj], 5),
                         "por_la_ventaja": self.cx_ventaja})
                elif radio["elegido"] in _iny:
                    # ── LOS EMPATES SON DEL CUERPO (aqui SI corre) ──────────
                    self.cx_empate = True
                    self.mem.cedidos, self.mem.ultimo_ataque = _ced0, _ua0
                    radio_iny = radio
                    accion, radio = D.decide(obs, self.mundo, self.mem,
                                             self.tick, self.bloqueos)
                    radio_iny["elegido_cuerpo"] = radio["elegido"]
                    log({"k": "forma_empate", "tick": self.tick,
                         "elegido_forma": radio_iny["elegido"],
                         "elegido_cuerpo": radio["elegido"],
                         "efecto": "el empate se le devuelve al cuerpo"})
        ms = (time.perf_counter() - t0) * 1000.0
        if caja["nuevos"] or caja["vetadas"] or caja["respaldo"]:
            _cds = {k: v["d"] for k, v in radio["candidatos"].items()}
            _iny = {caja["de"][i] for i in caja["nuevos"]}
            log({"k": "forma_tic", "tick": self.tick,
                 "elegido": radio["elegido"], "gano_forma":
                 (radio["elegido"] in _iny) and not self.cx_empate,
                 "empate_al_cuerpo": self.cx_empate,
                 "nuevos": caja["nuevos"], "vetadas": caja["vetadas"],
                 "respaldo": caja["respaldo"],
                 "ventajas": {str(f.id): round(f.ventaja, 5) for f in self.vivas},
                 "C": round(self.conf.C, 4),
                 "margen": round(self.conf.margen(), 4)})
        self._habla(obs)
        log({"k": "tiempo_tic", "tick": self.tick, "ms": round(ms, 3),
             "ms_forma": round(self.ms_forma[-1], 2) if self.ms_forma else None,
             "en_hilo": self.evalua_en_hilo, "vivas": len(self.vivas)})
        self.tiempos_ms.append(ms)
        self.decisiones += 1
        self.ultimos_cands = tuple(radio["candidatos"])
        if self.tick % PC.DETALLE_CANDIDATOS_CADA != 0:
            radio["candidatos"] = {k: v["d"]
                                   for k, v in radio["candidatos"].items()}
        st, radio_ap = A.appraise(obs, self.mundo, self.mem, self.tick)
        radio["ms"] = round(ms, 3)
        radio_ap = {k: v for k, v in radio_ap.items()
                    if k not in ("fuerzas_crudas", "fuerzas_state", "W_desglose")}
        radio_ap["filas"] = {k: v for k, v in (radio_ap.get("filas") or {}).items()
                             if (v or {}).get("M")}
        radio["ahora"] = radio_ap
        if CUR_FORMA_ON:
            # EL REGISTRO POR TIC que las cuarenta necesitan para leerse
            _v = self.vivas[0] if self.vivas else None
            log({"k": "cur_forma_tic", "tick": self.tick,
                 "activa": (_v.id if _v else None),
                 "destino": (list(self.k_camino.get(_v.id, [[None]])[-1])
                             if _v and self.k_camino.get(_v.id) else None),
                 "fin": getattr(_v, "motivo_caida", None) if _v else None,
                 "nacidas": self.k_nacidas, "vivas": len(self.vivas),
                 "ign": (round(self.ojo.ignorancia_global(), 5)
                         if self.ojo else None),
                 "amenaza": round(self._cur_amenaza, 5)})
        from motor.model import opponent_distance, DEFAULT_CONFIG
        radio["d_ahora"] = round(opponent_distance(st, DEFAULT_CONFIG), 5)
        if CUR_FORMA_ON:
            accion = self._compromiso(obs, accion, radio)
        return accion, radio

    # ── [P5-8H] EL COMPROMISO: la forma es un objetivo, no una sugerencia ──
    def _rupturas(self, obs, fv):
        """(causa, detalle) de la primera ruptura que aplique, o (None, None).

        Las siete del encargo. (f) y (g) las aplican `_revisa_vivas` y
        `_abandonos_K`; aqui se miran las cinco del tic.
        """
        you = obs.get("you") or {}
        pos = tuple(you.get("pos") or ())
        if not pos:
            return "sin posicion", None
        r = self._como_registro(obs)
        herm = self.mundo.teammate_slot
        arms = CFM.armados(r, self.mundo, herm)
        # (a) VETO VITAL
        for q, rg in arms:
            if max(abs(pos[0] - q[0]), abs(pos[1] - q[1])) <= rg:
                return "a) veto vital: armado a tiro", {"arma_en": list(q)}
        # (b) VETO DURO
        cam = self.k_camino.get(fv.id) or []
        dest = tuple(cam[-1]) if cam else None
        if dest is not None:
            try:
                i = cam.index(pos)
            except ValueError:
                i = 0
            if CFM.abandona_por_peligro(dest, cam[i:] or cam, r, self.mundo,
                                        herm):
                return "b) veto duro: cubre el camino", None
        # (c) DANO en el tic
        _dt = sum(float(x.get("amount") or 0) if isinstance(x, dict) else 0.0
                  for x in (you.get("damage_taken") or []))
        if _dt > 0:
            return "c) dano recibido", {"dano": _dt}
        # (d) VIDA o CARENCIA
        hp = float(you.get("hp") or 100)
        if hp < 15:
            return "d) vida bajo 15", {"hp": hp}
        try:
            W = float(A.riqueza_W(you, self.mundo)[0])
        except Exception:
            W = None
        if W is not None:
            w0 = getattr(fv, "W_nace", None)
            if w0 is not None and W < w0 - 1e-9:
                return "d) carencia sube (pierde de las manos)", {"W": W,
                                                                  "W0": w0}
        # (e) RIVAL CERCA
        for a in (r.get("ve_agentes") or []):
            if a.get("slot") == herm or not a.get("pos"):
                continue
            q = tuple(a["pos"])
            d = max(abs(pos[0] - q[0]), abs(pos[1] - q[1]))
            if d <= 2:
                return "e) rival a 2 o menos", {"slot": a.get("slot"), "d": d}
            if d < 6 and CFM._alcance_de(self.mundo, a) > 0:
                prev = (self.k_rival_dist or {}).get(a.get("slot"))
                if prev is not None and d < prev:
                    return "e) armado a menos de 6 y acercandose", \
                        {"slot": a.get("slot"), "d": d, "antes": prev}
        return None, None

    def _compromiso(self, obs, accion, radio):
        """Con piernas listas y sin ruptura, se EJECUTA el paso de la forma."""
        you = obs.get("you") or {}
        # la memoria de distancias de los rivales, para «se acerca»
        _r = self._como_registro(obs)
        _p = tuple(you.get("pos") or ())
        nueva = {}
        for a in (_r.get("ve_agentes") or []):
            if a.get("pos") and _p:
                nueva[a.get("slot")] = max(abs(_p[0] - a["pos"][0]),
                                           abs(_p[1] - a["pos"][1]))
        _antes = self.k_rival_dist
        self.k_rival_dist = nueva
        if not self.vivas:
            return accion
        fv = self.vivas[0]
        if getattr(fv, "origen", "") != "curiosidad":
            return accion
        mri = int(you.get("move_ready_in") or 0)
        if mri > 0:
            log({"k": "compromiso", "tick": self.tick, "id": fv.id,
                 "estado": "enfriamiento", "move_ready_in": mri})
            self.k_enfria += 1
            return accion
        self.k_rival_dist = _antes          # (e) compara contra el tic previo
        causa, det = self._rupturas(obs, fv)
        self.k_rival_dist = nueva
        if causa:
            self.k_rupturas[causa] += 1
            log({"k": "compromiso", "tick": self.tick, "id": fv.id,
                 "estado": "rompe", "causa": causa, "detalle": det})
            return accion
        # OBEDECE: se ejecuta el paso de la forma
        try:
            nom = fv.nombre()
            rec = fv.receta(obs, self.mem)
            acc2 = D._a_json(nom, rec, tuple(you.get("pos") or ()),
                             self.mundo, self.mem, self.tick)
        except Exception as ex:
            log({"k": "forma_error", "tick": self.tick,
                 "donde": "compromiso", "error": repr(ex)[:200]})
            return accion
        _cds = {k: (v["d"] if isinstance(v, dict) else v)
                for k, v in (radio.get("candidatos") or {}).items()}
        d_forma = _cds.get(nom)
        d_gana = _cds.get(radio.get("elegido"))
        coste = ((d_forma - d_gana) if (d_forma is not None
                                        and d_gana is not None) else None)
        if coste is not None:
            self.k_coste.append(coste)
        self.k_obedece += 1
        log({"k": "compromiso", "tick": self.tick, "id": fv.id,
             "estado": "obedece", "paso": nom,
             "habria_ganado": radio.get("elegido"),
             "d_forma": d_forma, "d_ganador": d_gana,
             "coste": (round(coste, 5) if coste is not None else None)})
        radio["elegido_cuerpo"] = radio.get("elegido")
        radio["elegido"] = nom
        return acc2

    def registrar(self, obs, radio):
        self.ultimo_rec = {
            "k": "tick", "tick": obs.get("tick"), "phase": obs.get("phase"),
            "pos": (obs.get("you") or {}).get("pos"),
            "hp": (obs.get("you") or {}).get("hp"),
            "hand": (obs.get("you") or {}).get("hand"),
            "body": (obs.get("you") or {}).get("body"),
            "pack": (obs.get("you") or {}).get("pack"),
            "effects": (obs.get("you") or {}).get("effects"),
            "move_ready_in": (obs.get("you") or {}).get("move_ready_in"),
            "attack_ready_in": (obs.get("you") or {}).get("attack_ready_in") or 0,
            "ve_agentes": ((obs.get("visible") or {}).get("agents") or []),
            "ve_items": ((obs.get("visible") or {}).get("items") or []),
            "zona": obs.get("zone"), "chat": obs.get("chat") or [],
            "RADIOGRAFIA": radio}
        super().registrar(obs, radio)
        if FORMA_ON and self.phase == "live" and radio is not None \
                and self.mundo is not None and CUR_FORMA_ON:
            try:
                self._cita_curiosidad(obs)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick,
                     "donde": "cita_curiosidad", "error": repr(ex)[:300]})
        if not self.evalua_en_hilo and not CUR_FORMA_ON \
                and self.mundo is not None and self.tick % CITA_CADA == 0:
            try:
                self._cita(obs, radio)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick, "donde": "cita",
                     "error": repr(ex)[:300]})


def _signos(a, b):
    """De dos ternas de necesidad (nF,nR,nS) a los tres signos del cuerpo."""
    if not a or not b:
        return {}
    eps = 1e-6
    out = {}
    for i, k in enumerate(("vida", "manos", "vinculo")):
        out[k] = ("+" if b[i] < a[i] - eps else
                  "-" if b[i] > a[i] + eps else "0")
    return out


async def run(url):
    import asyncio
    import websockets
    alma = AlmaForma()
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION,
         "entorno": CX.entorno_efectivo(),
         "entorno_s3": PC.entorno_s3(),
         "entorno_forma": entorno_forma(),          # [P5-6A] lo nuevo
         "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "mirada_min_ticks": D.H_MIRADA_MIN, "voz_cada_ticks": PC.VOZ_CADA,
         "cuerpo": "v42_exp EMPATIA_ON H_PREV 0.25 H_GOLPE 1.0 "
                   "MIEDO_ON False VIDA_AJENA_ON False"})
    # [A2] el mensaje del canal `team` pasa a ser la forma, envolviendo
    # `parte.emite` DESDE FUERA. `parte.py` no se toca, como todo lo demas.
    if HILO_ON:
        _orig_emite = PC.PARTE.emite

        def _emite(msg, tick, mundo, mem, ventana, _o=_orig_emite, _a=alma):
            s = _a.texto_hilo(msg)
            return s if s else _o(msg, tick, mundo, mem, ventana)
        PC.PARTE.emite = _emite
    alma.cx.arranca()          # el cortex del cuatro: apagado salvo GEMV_CORTEX
    alma.cf.arranca()          # el consejero de formas
    async with websockets.connect(url, ping_timeout=None) as ws:
        rep = asyncio.create_task(PC.vigia(ws, alma))
        try:
            await PC.decisor(ws, alma)
        finally:
            alma.done.set()
            rep.cancel()
            try:
                await rep
            except asyncio.CancelledError:
                pass
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    if CONSEJERO_ON:
        alma.cf.pide_gasto(alma.tick, "fin de la partida")
    log(alma.cf.resumen(alma.tick))
    log({"k": "confianza_final", "tick": alma.tick, **alma.conf.resumen()})
    PC.sube_artefacto(alma, "fin de la partida")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL")
                    or os.environ["COGAMES_ENGINE_WS_URL"]))

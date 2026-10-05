"""[P6-27] LA POLITICA DEL BRAZO A8, ARREGLADA: `policy_pareja26.AlmaPareja26` con el encargo ligero de
`puerta_proceso_P6_27` en lugar de la instantanea entera cada 25 tics. Ninguna decision cambia: la puerta de
entrada de la consulta es la misma (fase, plan vivo, cadencia, silencio, piernas listas, ninguna en vuelo),
el disparo es el mismo (`Oraculo.dispara`, calculado en el proceso), el texto es el mismo (`texto_escena_P6_26`
sobre la memoria espejo, que repite tic a tic lo que el cuerpo hace con la suya), el juicio a la llegada es el
mismo (`_recoge(obs)` -> `encarga_juicio(fv, self, obs)`, P6-23), el mensaje al hermano y `malestar26` son los
mismos.

LO QUE CAMBIA, y solo esto:
  · un gancho en `Memoria.observa` (solo para la memoria del alma A8): cada vez que el cuerpo observa, el mismo
    `obs` sale hacia el espejo del proceso (`hilo.manda_tic`, ~2-7 KB), con la accion del tic anterior y los
    dos campos que escribe el decisor; asi el espejo ve exactamente lo que ve la memoria del cuerpo, tambien
    antes de la fase viva.
  · `_oraculo16` ya no llama a `encarga_razonador` (instantanea entera): manda `hilo.pregunta` (candidatos y
    escalares, lo mismo que P6-26 leia en ese momento).
POR QUE EL HILO PRINCIPAL YA NO ESPERA: `manda_tic` es un `pickle.dumps` de ~5-20 KB y un `Queue.put`
(encolar en memoria); el hilo alimentador de la cola escribe en la tuberia; el proceso hace el resto. Se mide
en `resumen27`: ms por mensaje (mediana y maximo) y bytes.
"""
from __future__ import annotations
import os
import sys
import time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
from alma import policy_cortex as PC                      # noqa: E402
from alma import policy_forma as PF                       # noqa: E402
import policy_pareja as PP                                # noqa: E402
import policy_pareja16 as P16                             # noqa: E402
import policy_pareja23 as P23                             # noqa: E402
import policy_pareja26 as P26                             # noqa: E402
import puerta_proceso_P6_27 as PX27                       # noqa: E402
import arreglos_P6_6 as R6                                # noqa: E402
import arreglos_P6_8b as R8                               # noqa: E402
import filas10_P6_10 as F10                               # noqa: E402
import amenaza11_P6_11 as M11                             # noqa: E402
import parte2 as P2                                       # noqa: E402
log = PF.log
VERSION = "policy_pareja27 (P6-27): A8 con el encargo ligero por tic y la memoria espejo en el proceso; nada mas cambia"


def entorno27():
    e = P26.entorno26(); e.update({"version": VERSION, "razonador": PX27.entorno27()})
    return e


ALMA27 = {"alma": None}
_OBSERVA0 = None


def _observa_gancho(self, obs, mundo, tick):
    """[P6-27] El gancho: la memoria del cuerpo observa como siempre y, en el mismo momento, el mismo `obs` sale
    hacia el espejo del proceso. Solo actua sobre la memoria del alma A8 (las copias de la puerta no mandan nada)."""
    r = _OBSERVA0(self, obs, mundo, tick)
    a = ALMA27["alma"]
    if a is not None and self is a.mem and a.hilo is not None:
        try:
            a.hilo.manda_tic(a, obs, tick)
        except Exception as ex:
            log({"k": "forma_error", "tick": tick, "donde": "manda_tic27", "error": repr(ex)[:200]})
    return r


class AlmaPareja27(P26.AlmaPareja26):
    def __init__(self, *a, **k):
        global _OBSERVA0
        super().__init__(*a, hilo=PX27.HiloProceso27(), **k)
        self.k_preguntas = 0
        if _OBSERVA0 is None:
            from alma import appraisal_zs_v42_exp as V42
            _OBSERVA0 = V42.Memoria.observa; V42.Memoria.observa = _observa_gancho
        ALMA27["alma"] = self

    # ── la puerta de entrada de la consulta: la misma que A7h/A8; el encargo, ligero ──
    def _oraculo16(self, obs):
        if self.mundo is None or (obs.get("phase") or self.phase) != "live":
            return
        t = self.tick
        you = obs.get("you") or {}
        if self.orac is None:
            import oraculo_P6_14 as O
            self.orac = O.Oraculo(self.mundo, int((you.get("stats") or {}).get("speed") or 5))
            log({"k": "oraculo16", "tick": t, "estado": "listo", "plan": "razonador Haiku (A8, encargo ligero P6-27)", "en_proceso": True, "fases": self.orac.fases})
        orac = self.orac
        if not orac.fases or t < orac.fases[0][0]:
            return
        if self.vivas or getattr(self, "pendientes", {}) or self.reeval_pend:
            return
        if t - self.ult_oraculo < P16.ORACULO_CADA:
            return
        if self.conf.callado(t):
            return
        if int(you.get("move_ready_in") or 0) != 0 or not you.get("pos"):
            return
        if self.hilo is None or self.hilo.razonador_en_vuelo is not None or t - self.ult_rz < P16.ORACULO_CADA:
            return
        self.ult_rz = t; self.k_preguntas += 1
        self.hilo.pregunta(self, obs, dict(self.ult_cands), {"ult_e2": self.ult_e2, "plan_hermano": self.plan_hermano})
        log({"k": "razonador26", "tick": t, "estado": "encargado al proceso", "ms_encargo": round(self.hilo.ms_razonador_encargo[-1], 3), "ligero": True, "plan_hermano": bool(self.plan_hermano)})


def resumen27(alma):
    r = P26.resumen26(alma); r["k"] = "resumen27"
    ms = sorted(alma.hilo.ms_tic); by = sorted(alma.hilo.bytes_tic)
    r["encargo_ligero"] = {"mensajes": len(ms), "preguntas_ms_max": (round(max(alma.hilo.ms_razonador_encargo), 3) if alma.hilo.ms_razonador_encargo else None), "ms_mediana": (round(ms[len(ms) // 2], 3) if ms else None), "ms_p99": (round(ms[int(0.99 * len(ms))], 3) if ms else None), "ms_max": (round(ms[-1], 3) if ms else None),
                           "bytes_mediana": (by[len(by) // 2] if by else None), "bytes_max": (by[-1] if by else None), "preguntas": alma.k_preguntas, "espejo": alma.hilo.espejo}
    return r


async def _run(url):
    import asyncio
    import websockets
    hecho = R6.aplica(PP.AlmaPareja, log); hecho8 = R8.aplica(log); hecho10 = F10.aplica(log); hecho11 = M11.aplica(log)
    alma = AlmaPareja27()
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION, "entorno": PF.CX.entorno_efectivo(), "entorno_forma": PF.entorno_forma(), "entorno_ojos": PP.entorno_ojos(),
         "entorno_arreglos": R6.entorno(), "arreglos": hecho, "entorno_arreglos8": R8.entorno(), "arreglos8": hecho8, "entorno_filas10": F10.entorno(), "filas10": hecho10,
         "entorno_manos11": M11.entorno(), "manos11": hecho11, "entorno23": entorno27(), "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if PP.OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "A8 (P6-27) = A7h con el razonador Haiku en el sitio del oraculo, encargo ligero + memoria espejo en el proceso, juicio con la instantanea de llegada, plan al hermano por el canal"})
    PP._envuelve(alma); P26.envuelve_voz(alma)
    alma.cx.arranca(); alma.cf.arranca()
    async with websockets.connect(url, ping_timeout=None) as ws:
        rep = asyncio.create_task(PC.vigia(ws, alma))
        try:
            await PC.decisor(ws, alma)
        finally:
            alma.done.set(); rep.cancel()
            try:
                await rep
            except asyncio.CancelledError:
                pass
    log({"k": "ojos_resumen", "tics_con_inyeccion": alma.n_contados, "candidatos_vetados": alma.n_vetados})
    log(resumen27(alma))
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    try:
        alma.hilo.cierra()
    except Exception:
        pass
    PC.sube_artefacto(alma, "fin de la partida")


run = _run

if __name__ == "__main__":
    import asyncio
    asyncio.run(_run(os.environ.get("COWORLD_PLAYER_WS_URL") or os.environ["COGAMES_ENGINE_WS_URL"]))

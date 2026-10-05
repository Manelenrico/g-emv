"""[P6-28] LA POLITICA DEL BRAZO A9: `policy_pareja27.AlmaPareja27` (A8 arreglado) con UN cambio: el proceso juez es el de P6-28, que da al
razonador la escena PREVISTA a t+DELTA (`prevision_P6_28`). Ademas, a la llegada de cada respuesta se anota el ERROR DE LA PREVISION
(casillas, Chebyshev, entre la casilla prevista y la real del tic de llegada) y cuanto tardo la prevision (ms, en el proceso).

[P6-27] LA POLITICA DEL BRAZO A8, ARREGLADA: `policy_pareja26.AlmaPareja26` con el encargo ligero de
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
import puerta_proceso_P6_28 as PX28                       # noqa: E402
import policy_pareja27 as P27                             # noqa: E402
import arreglos_P6_6 as R6                                # noqa: E402
import arreglos_P6_8b as R8                               # noqa: E402
import filas10_P6_10 as F10                               # noqa: E402
import amenaza11_P6_11 as M11                             # noqa: E402
import parte2 as P2                                       # noqa: E402
log = PF.log
VERSION = "policy_pareja28 (P6-28): A9 = A8 (P6-27) con la escena prevista a t+DELTA para el razonador; nada mas cambia"


def entorno28():
    e = P26.entorno26(); e.update({"version": VERSION, "razonador": PX28.entorno28()})
    return e


class AlmaPareja28(P27.AlmaPareja27):
    def __init__(self, *a, **k):
        P26.AlmaPareja26.__init__(self, *a, hilo=PX28.HiloProceso28(), **k)
        self.k_preguntas = 0; self.previsiones = []; self.errores_prevision = []; self.ult_prevision = {}
        if P27._OBSERVA0 is None:
            from alma import appraisal_zs_v42_exp as V42
            P27._OBSERVA0 = V42.Memoria.observa; V42.Memoria.observa = P27._observa_gancho
        P27.ALMA27["alma"] = self

    def _recoge_hilo(self, obs):
        # se leen los hechos una vez, se apunta la prevision de cada pregunta hecha (viene en el "rzt"), y se pasan al padre
        if self.hilo is None:
            return
        hechos = self.hilo.recoge()
        for ident, r, ms, err in hechos:
            if isinstance(ident, tuple) and ident and ident[0] == "rzt" and isinstance(r, dict) and r.get("prevision"):
                self.ult_prevision[ident[1]] = r["prevision"]; self.previsiones.append(r["prevision"])
        _rec = self.hilo.recoge
        self.hilo.recoge = lambda: hechos
        try:
            super()._recoge_hilo(obs)
        finally:
            self.hilo.recoge = _rec

    def _aplica_razonador(self, t_pregunta, r, ms):
        pv = self.ult_prevision.get(t_pregunta)
        if pv and r.get("estado") in ("propone", "intraducible", "calla", "error"):
            you = (self.ultima_obs or {}).get("you") or {}
            pos = you.get("pos")
            if pos is not None:
                e = max(abs(int(pos[0]) - pv["pos_prevista"][0]), abs(int(pos[1]) - pv["pos_prevista"][1]))
                self.errores_prevision.append(e)
                r = dict(r, error_prevision_casillas=e, pos_real_llegada=[int(pos[0]), int(pos[1])], pos_prevista=pv["pos_prevista"], hp_prevista=pv["hp_prevista"], hp_real_llegada=you.get("hp"), ms_prevision=pv["ms_prevision"], delta=pv["delta"], t_previsto=pv["t_previsto"])
        super()._aplica_razonador(t_pregunta, r, ms)
        rec = {"k": "prevision28", "tick": self.tick, "tick_pregunta": t_pregunta, **{k: r.get(k) for k in ("error_prevision_casillas", "pos_real_llegada", "pos_prevista", "hp_prevista", "hp_real_llegada", "ms_prevision", "delta", "t_previsto")}}
        if pv:
            log(rec)


def resumen28(alma):
    r = P27.resumen27(alma); r["k"] = "resumen28"
    ep = sorted(alma.errores_prevision); ms = sorted(x["ms_prevision"] for x in alma.previsiones)
    r["prevision"] = {"n": len(ep), "error_casillas_mediana": (ep[len(ep) // 2] if ep else None), "error_casillas_p90": (ep[int(0.9 * len(ep))] if ep else None), "error_casillas_max": (ep[-1] if ep else None),
                      "ms_mediana": (ms[len(ms) // 2] if ms else None), "ms_max": (ms[-1] if ms else None), "donde": "en el proceso juez"}
    return r


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
    alma = AlmaPareja28()
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION, "entorno": PF.CX.entorno_efectivo(), "entorno_forma": PF.entorno_forma(), "entorno_ojos": PP.entorno_ojos(),
         "entorno_arreglos": R6.entorno(), "arreglos": hecho, "entorno_arreglos8": R8.entorno(), "arreglos8": hecho8, "entorno_filas10": F10.entorno(), "filas10": hecho10,
         "entorno_manos11": M11.entorno(), "manos11": hecho11, "entorno23": entorno28(), "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if PP.OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "A9 (P6-28) = A8 con la escena PREVISTA a t+DELTA para el razonador (imaginacion honesta de puerta6, en el proceso)"})
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
    log(resumen28(alma))
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

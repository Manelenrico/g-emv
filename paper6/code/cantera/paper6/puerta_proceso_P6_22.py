"""[P6-22 · 4] LA PUERTA EN UN PROCESO APARTE: que el juicio nunca retrase el paso del cuerpo.
VERSION NUEVA, DECLARADA. No toca el cuerpo congelado ni la puerta del cinco: los importa y
los llama. Lo que cambia es la INFRAESTRUCTURA en que corre el juicio:

  · antes (A5/A6): el hilo principal hacia una COPIA PROFUNDA de la memoria y de los bloqueos
    (puro Python, 12-73 ms medidos en P6-22 §3) cada vez que encargaba un juicio o una
    reevaluacion, y el juicio corria en un HILO de Python (300-600 ms de CPU por juicio) que
    compite por el interprete con el bucle del juego;
  · ahora: el hilo principal hace una INSTANTANEA por serializacion (`pickle`, en C: ~2 ms
    para la memoria entera) y la manda a un PROCESO aparte («el juez»), que tiene un alma
    espejo con el mismo codigo, los mismos arreglos y los mismos ganchos (puerta6), y que
    ejecuta `_juzga` tal cual sobre la instantanea. El resultado vuelve por una cola y el
    bucle lo recoge cuando pasa, como recogia lo del hilo.

El juicio es el mismo (misma funcion, mismas entradas): `banco_fix_P6_22.py` lo comprueba
plan a plan sobre el banco de P6-15, y `mide_bucle_P6_22.py --brazo A6p` compara los
veredictos del campo grabado con los de A6 uno a uno.

`instantanea(x)` es la copia que sustituye a `copy.deepcopy` en el hilo principal; es lo
mismo que viaja al proceso.
"""
from __future__ import annotations
import multiprocessing as mp
import os
import pickle
import queue
import sys
import threading
import time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    if p not in sys.path:
        sys.path.insert(0, p)
VERSION = "puerta_proceso (P6-22): juicio de la puerta en un proceso aparte, instantanea por pickle en vez de copia profunda"


def instantanea(x):
    """Copia por serializacion (C), en vez de `copy.deepcopy` (puro Python)."""
    return pickle.loads(pickle.dumps(x, protocol=pickle.HIGHEST_PROTOCOL))


# ── el juez: un proceso con un alma espejo ─────────────────────────────────
def _juez(entrada, salida, entorno, rutas):
    os.environ.update(entorno)
    for r in reversed(rutas):
        if r not in sys.path:
            sys.path.insert(0, r)
    from alma import policy_cortex as PC
    from alma import policy_forma as PF
    from alma import forma_viva as FV
    import policy_pareja as PP
    import arreglos_P6_6 as R6, arreglos_P6_8b as R8, filas10_P6_10 as F10, amenaza11_P6_11 as M11
    import policy_pareja16 as P16          # noqa: F401  (instala el comparador puerta6 si GEMV_PUERTA6=1)
    import policy_pareja18 as P18
    R6.aplica(PP.AlmaPareja, PC.log); R8.aplica(PC.log); F10.aplica(PC.log); M11.aplica(PC.log)
    mudo = lambda rec: None
    PC.log = mudo; PF.log = mudo; PP.log = mudo; P16.log = mudo; P18.log = mudo
    espejo = P18.AlmaPareja18()
    espejo.hilo = None; espejo.evalua_en_hilo = False; espejo.phase = "live"
    salida.put(("__listo__", None, 0.0, None, None))
    while True:
        datos = entrada.get()
        if datos is None:
            break
        try:
            job = pickle.loads(datos); t0 = time.perf_counter()
            if job.get("mundo") is not None:
                espejo.mundo = job["mundo"]
            espejo.tick = job["tick"]; espejo.conf.C = job["C"]
            espejo.herm_dicho = job["herm_dicho"]; espejo.herm_tick = job["herm_tick"]; espejo.ultima_obs = job["ultima_obs"]
            fv = FV.FormaViva(job["fv"]["id"], job["fv"]["tramos"], job["fv"]["nace"], origen=job["fv"]["origen"])
            r = espejo._juzga(fv, job["obs"], job["mem"], job["blo"])
            salida.put((job["ident"], r, round((time.perf_counter() - t0) * 1000.0, 2), None, getattr(fv, "nec0", None)))
        except Exception as ex:
            salida.put((job.get("ident") if isinstance(job, dict) else None, None, 0.0, repr(ex)[:200], None))


class HiloProceso:
    """Misma interfaz que `EvaluadorHilo` (encarga/recoge/en_vuelo/lock), pero el trabajo
    va a un proceso y la copia es una instantanea hecha en el hilo principal."""

    def __init__(self):
        ctx = mp.get_context("spawn")
        self.entrada = ctx.Queue(); self.salida = ctx.Queue()
        self.lock = threading.Lock(); self.en_vuelo = 0; self.fvs = {}; self.listo = False
        self.ms_instantanea = []; self.mundo_enviado = False; self.errores = []; self.diagnostico = []
        self.p = ctx.Process(target=_juez, args=(self.entrada, self.salida, dict(os.environ), list(sys.path)), daemon=True)
        self.p.start()

    def encarga(self, ident, fn):
        raise RuntimeError("HiloProceso no acepta cierres: usa encarga_job")

    def encarga_job(self, ident, fv, alma, obs):
        t0 = time.perf_counter()
        herm = getattr(alma.mundo, "teammate_slot", None)
        ult = {"visible": {"agents": [dict(a) for a in (((alma.ultima_obs or {}).get("visible") or {}).get("agents") or []) if a.get("slot") == herm]}}
        job = {"ident": ident, "fv": {"id": fv.id, "tramos": fv.tramos, "nace": fv.nace, "origen": fv.origen}, "obs": obs, "mem": alma.mem, "blo": alma.bloqueos,
               "tick": alma.tick, "C": alma.conf.C, "herm_dicho": alma.herm_dicho, "herm_tick": alma.herm_tick, "ultima_obs": ult,
               "mundo": (None if self.mundo_enviado else alma.mundo)}
        datos = pickle.dumps(job, protocol=pickle.HIGHEST_PROTOCOL)      # la instantanea, en el hilo principal, en C
        if len(self.diagnostico) < 3:                                     # que pesa cada campo (los tres primeros encargos)
            d = {}
            for k, v in job.items():
                t1 = time.perf_counter(); n = len(pickle.dumps(v, protocol=pickle.HIGHEST_PROTOCOL)); d[k] = (n, round((time.perf_counter() - t1) * 1000.0, 2))
            self.diagnostico.append(d)
        self.mundo_enviado = True
        with self.lock:
            self.en_vuelo += 1; self.fvs[ident] = fv
        self.entrada.put(datos)
        self.ms_instantanea.append((time.perf_counter() - t0) * 1000.0)

    def recoge(self):
        out = []
        while True:
            try:
                ident, r, ms, err, nec0 = self.salida.get_nowait()
            except queue.Empty:
                break
            if ident == "__listo__":
                self.listo = True; continue
            with self.lock:
                self.en_vuelo -= 1; fv = self.fvs.pop(ident, None)
            if fv is not None and nec0 is not None:
                fv.nec0 = nec0
            if err:
                self.errores.append((ident, err))
            out.append((ident, r, ms, err))
        return out

    def cierra(self):
        try:
            self.entrada.put(None); self.p.join(timeout=2.0)
        except Exception:
            pass


def _construye():
    from alma import policy_forma as PF
    from alma import forma_viva as FV
    import policy_pareja16 as P16
    import policy_pareja18 as P18
    log = P18.log

    class AlmaPareja22(P18.AlmaPareja18):
        """A6 con la puerta en un proceso: `_recoge` y `_revisa_vivas` sin copia profunda en el
        hilo principal; todo lo demas, heredado sin tocar."""

        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.hilo = HiloProceso(); self.evalua_en_hilo = True

        # copia de `policy_forma._recoge` (P5-6C) sin la copia profunda: el encargo lleva una instantanea
        def _recoge(self, obs):
            e = self.cf.recoge()
            if not e:
                return
            if e.get("callar") and not e.get("formas"):
                log({"k": "forma_evaluada", "tick": self.tick, "veredicto": "el consejero callo", "origen": "consejero"})
                return
            for tramos_forma in e["formas"]:
                self.n_forma += 1
                fv = FV.FormaViva(self.n_forma, tramos_forma["tramos"], self.tick, origen="consejero")
                self.hilo.encarga_job(fv.id, fv, self, obs)
                log({"k": "hilo_forma", "tick": self.tick, "id": fv.id, "estado": "encargada al proceso", "ms_instantanea": round(self.hilo.ms_instantanea[-1], 2)})
                self.pendientes = getattr(self, "pendientes", {})
                self.pendientes[fv.id] = fv

        # copia de `policy_pareja16._revisa_vivas` (revisa6) sin la copia profunda
        def _revisa_vivas(self, obs):
            hp = (obs.get("you") or {}).get("hp")
            quedan = []
            for fv in self.vivas:
                _na = getattr(fv, "no_antes_de", None)
                if _na is not None and self.tick < _na:
                    quedan.append(fv); continue
                if not fv.toca_revisar(self.tick):
                    quedan.append(fv); continue
                cae, motivo = fv.falla_lo_previsto(hp, self._filas(), self.tick)
                if cae:
                    fv.cae(motivo, self.tick)
                    log({"k": "forma_caida", "tick": self.tick, "id": fv.id, "motivo": motivo})
                    self._cierra(fv, mal=True); continue
                if fv.tics and fv.i_punto < len(fv.tics) and self.tick >= fv.tics[fv.i_punto]:
                    d_real = self._d_ahora(obs)
                    d_proy = (fv.curva[fv.i_punto].get("d") if fv.i_punto < len(fv.curva) else None)
                    v, ca, cb = self.conf.comprueba(d_real, d_proy, self.tick, fv.id, fv.i_punto)
                    if v is not None:
                        if v == "fallo":
                            fv.malos += 1
                        log({"k": "confianza", "tick": self.tick, "id": fv.id, "punto": fv.i_punto, "veredicto": v, "d_real": round(d_real, 5), "d_proyectada": round(d_proy, 5),
                             "C_antes": round(ca, 4), "C": round(cb, 4), "margen": round(self.conf.margen(), 4)})
                    n_ahora = self.nec_ahora(obs)
                    if not hasattr(fv, "real_nec"):
                        fv.real_nec, fv.real = {}, {}
                    ant = fv.real_nec.get(fv.i_punto - 1, getattr(fv, "nec0", None))
                    fv.real_nec[fv.i_punto] = n_ahora
                    sg = PF._signos(ant, n_ahora)
                    if sg:
                        fv.real[fv.i_punto] = sg
                    fv.avanza_punto(self.tick)
                    if fv.estado == "cumplida":
                        self._cierra(fv, mal=bool(fv.malos)); continue
                if fv.id not in self.reeval_pend:
                    self.hilo.encarga_job(("re", fv.id), fv, self, obs)
                    self.reeval_pend[fv.id] = fv
                    log({"k": "hilo_forma", "tick": self.tick, "id": fv.id, "estado": "reevaluacion encargada al proceso", "ms_instantanea": round(self.hilo.ms_instantanea[-1], 2)})
                fv.ultima_revision = self.tick
                quedan.append(fv)
            self.vivas = quedan

    return AlmaPareja22


AlmaPareja22 = _construye()


def entorno22():
    return {"version": VERSION, "proceso": "spawn", "copia": "pickle HIGHEST_PROTOCOL"}

"""[P6-23] EL PROCESO JUEZ, VERSION NUEVA DE `puerta_proceso_P6_22`: ademas del juicio de la
puerta, calcula en el proceso EL TIC DE PROPUESTA DEL ORACULO (BFS de casillas seguras,
disparo, plan, traductor), que en P6-22 seguia en el hilo principal y era la unica fuente de
pasos perdidos que quedaba (los 7 de las fases 5-7, todos en tics de propuesta).

  · `instantanea(x)`: la copia por serializacion (identica a la de P6-22).
  · `HiloProceso23`: misma interfaz que el hilo (`recoge`, `en_vuelo`, `lock`), con dos
    encargos: `encarga_juicio` (como P6-22: forma, obs, mem, bloqueos, estado que lee `_juzga`)
    y `encarga_oraculo` (obs y lo poco que el oraculo lee: tic, ultimo tic de propuesta,
    numero de propuestas, si el hermano vive y donde esta segun la memoria, el ultimo parte).
    El oraculo trabaja en el proceso sobre un alma espejo (`policy_pareja23.AlmaPareja23`,
    mismo codigo, mismos arreglos, mismos ganchos) y devuelve la propuesta y sus registros; el
    hilo principal la deja donde la dejaba el oraculo (`cf.entregado`) al recogerla.
No depende de `policy_pareja18` (que exige GEMV_PUERTA6=1): sirve para A7v y A7h.
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
VERSION = "puerta_proceso23 (P6-23): juicio de la puerta Y tic de propuesta del oraculo en un proceso aparte; instantanea por pickle"


def instantanea(x):
    return pickle.loads(pickle.dumps(x, protocol=pickle.HIGHEST_PROTOCOL))


class MemLite:
    """Lo que el oraculo lee de la memoria del cuerpo, y nada mas."""

    def __init__(self, pareja_muerta, pareja_pos):
        self.pareja_muerta = pareja_muerta; self.pareja_pos = pareja_pos; self.objetos_vistos = {}


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
    import policy_pareja16 as P16
    import policy_pareja23 as P23
    R6.aplica(PP.AlmaPareja, PC.log); R8.aplica(PC.log); F10.aplica(PC.log); M11.aplica(PC.log)
    mudo = lambda rec: None
    PC.log = mudo; PF.log = mudo; PP.log = mudo; P16.log = mudo; P23.log = mudo
    espejo = P23.AlmaPareja23(con_proceso=False)
    espejo.hilo = None; espejo.evalua_en_hilo = False; espejo.phase = "live"
    salida.put(("__listo__", None, 0.0, None, None))
    while True:
        datos = entrada.get()
        if datos is None:
            break
        job = None
        try:
            job = pickle.loads(datos); t0 = time.perf_counter()
            if job.get("mundo") is not None:
                espejo.mundo = job["mundo"]
            espejo.tick = job["tick"]
            if job["tipo"] == "juicio":
                espejo.conf.C = job["C"]; espejo.herm_dicho = job["herm_dicho"]; espejo.herm_tick = job["herm_tick"]; espejo.ultima_obs = job["ultima_obs"]
                fv = FV.FormaViva(job["fv"]["id"], job["fv"]["tramos"], job["fv"]["nace"], origen=job["fv"]["origen"])
                r = espejo._juzga(fv, job["obs"], job["mem"], job["blo"])
                salida.put((job["ident"], r, round((time.perf_counter() - t0) * 1000.0, 2), None, getattr(fv, "nec0", None)))
            else:   # oraculo
                espejo.mem = MemLite(job["pareja_muerta"], job["pareja_pos"]); espejo.parte_herm = job["parte_herm"]
                espejo.ult_oraculo = job["ult_oraculo"]; espejo.n_oraculo = job["n_oraculo"]; espejo.ultimos_cands = tuple(range(int(job.get("n_cands") or 0)))
                espejo.vivas = []; espejo.pendientes = {}; espejo.reeval_pend = {}; espejo.conf.callado_hasta = None
                regs = []
                P23.log = regs.append
                try:
                    espejo._oraculo_calcula(job["obs"])
                finally:
                    P23.log = mudo
                with espejo.cf.lock:
                    e, espejo.cf.entregado = espejo.cf.entregado, None
                r = {"entregado": e, "registros": regs, "ult_oraculo": espejo.ult_oraculo, "n_oraculo": espejo.n_oraculo, "orac_listo": espejo.orac is not None}
                salida.put((job["ident"], r, round((time.perf_counter() - t0) * 1000.0, 2), None, None))
        except Exception as ex:
            salida.put(((job or {}).get("ident"), None, 0.0, repr(ex)[:200], None))


class HiloProceso23:
    def __init__(self):
        ctx = mp.get_context("spawn")
        self.entrada = ctx.Queue(); self.salida = ctx.Queue()
        self.lock = threading.Lock(); self.en_vuelo = 0; self.fvs = {}; self.listo = False
        self.ms_instantanea = []; self.mundo_enviado = False; self.errores = []; self.oraculo_en_vuelo = False; self.ms_oraculo_encargo = []
        self.p = ctx.Process(target=_juez, args=(self.entrada, self.salida, dict(os.environ), list(sys.path)), daemon=True)
        self.p.start()

    def encarga(self, ident, fn):
        raise RuntimeError("HiloProceso23 no acepta cierres")

    def _envia(self, job):
        datos = pickle.dumps(job, protocol=pickle.HIGHEST_PROTOCOL)
        self.mundo_enviado = True
        self.entrada.put(datos)

    def encarga_juicio(self, ident, fv, alma, obs):
        t0 = time.perf_counter()
        herm = getattr(alma.mundo, "teammate_slot", None)
        ult = {"visible": {"agents": [dict(a) for a in (((alma.ultima_obs or {}).get("visible") or {}).get("agents") or []) if a.get("slot") == herm]}}
        job = {"tipo": "juicio", "ident": ident, "fv": {"id": fv.id, "tramos": fv.tramos, "nace": fv.nace, "origen": fv.origen}, "obs": obs, "mem": alma.mem, "blo": alma.bloqueos,
               "tick": alma.tick, "C": alma.conf.C, "herm_dicho": alma.herm_dicho, "herm_tick": alma.herm_tick, "ultima_obs": ult, "mundo": (None if self.mundo_enviado else alma.mundo)}
        with self.lock:
            self.en_vuelo += 1; self.fvs[ident] = fv
        self._envia(job)
        self.ms_instantanea.append((time.perf_counter() - t0) * 1000.0)

    def encarga_oraculo(self, alma, obs):
        t0 = time.perf_counter()
        mem = alma.mem
        job = {"tipo": "oraculo", "ident": ("or", alma.tick), "obs": obs, "tick": alma.tick, "ult_oraculo": alma.ult_oraculo, "n_oraculo": alma.n_oraculo,
               "pareja_muerta": bool(getattr(mem, "pareja_muerta", False)), "pareja_pos": (tuple(int(x) for x in mem.pareja_pos) if getattr(mem, "pareja_pos", None) else None),
               "parte_herm": getattr(alma, "parte_herm", None), "n_cands": len(alma.ultimos_cands or ()), "mundo": (None if self.mundo_enviado else alma.mundo)}
        with self.lock:
            self.en_vuelo += 1; self.oraculo_en_vuelo = True
        self._envia(job)
        self.ms_oraculo_encargo.append((time.perf_counter() - t0) * 1000.0)

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
                self.en_vuelo -= 1
                fv = self.fvs.pop(ident, None)
                if isinstance(ident, tuple) and ident and ident[0] == "or":
                    self.oraculo_en_vuelo = False
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


def entorno23():
    return {"version": VERSION, "proceso": "spawn", "copia": "pickle HIGHEST_PROTOCOL", "oraculo_en_proceso": True}

"""[P6-27 · 1] EL ARREGLO DEL ENCARGO DEL RAZONADOR (infraestructura, sin cambiar ninguna decision).

En P6-26 el hilo principal mandaba al proceso, cada 25 tics, LA INSTANTANEA ENTERA (memoria, bloqueos,
mundo, historial: ~1 MB en pickle) para que el proceso decidiera si disparaba; 726 encargos en 4 vidas para
11 consultas, y tres pasos perdidos en tics de encargo. Aqui, como el oraculo de A7h (P6-23): EL ENCARGO ES
LIGERO y el proceso no necesita ninguna instantanea para la consulta, porque LLEVA SU PROPIA MEMORIA ESPEJO:

  · cada tic, desde el gancho de `Memoria.observa` del cuerpo (`policy_pareja27`), el hilo principal manda un
    mensaje pequeno (`manda_tic`: EL MISMO obs que el cuerpo acaba de observar, con los mensajes gemelos del
    oido y los ojos, la accion del tic anterior y los dos campos que escribe el decisor: ~2-7 KB, decenas de
    microsegundos de pickle; la escritura en la tuberia la hace el hilo alimentador de `multiprocessing.Queue`,
    no el principal). El proceso repite en su espejo lo mismo que el cuerpo hace con su memoria en
    `policy_cortex.decidir` (:425-427): `mem.observa(obs, mundo, tick)` y `bloqueos.actualiza(obs, mundo,
    ultima_accion, tick)`, y copia los dos campos que escribe el decisor (`cedidos`, `ultimo_ataque`,
    `decisor_zs.py:904-908`). Asi la memoria espejo es la del cuerpo, tic a tic, sin copiarla nunca.
  · cuando el hilo principal quiere consultar (la misma puerta de entrada de A7h: fase, plan vivo, cadencia,
    silencio, piernas listas, ninguna consulta en vuelo), manda un segundo mensaje pequeno (`pregunta`: los
    candidatos del cuerpo y unos escalares, lo mismo que P6-26 leia en ese momento, sin memoria ni bloqueos).
    El proceso decide el disparo (`Oraculo.dispara`, BFS de 6 ms, en el proceso), y si dispara construye el
    texto sobre su espejo y llama al modelo EN UN HILO DEL PROCESO. Nada de esto le cuesta un tic al cuerpo:
    el hilo principal no serializa ninguna instantanea ni espera respuesta alguna.
  · el juicio de la propuesta a la LLEGADA sigue siendo el de P6-23/P6-26: `encarga_juicio` con la
    instantanea del tic de llegada (sin cambios). El juicio con la instantanea DE LA PREGUNTA (solo medida)
    lo hace el proceso sobre una copia de su espejo hecha en el momento de la pregunta (en el proceso).

Por que el hilo principal ya no espera: `manda_tic` solo hace `pickle.dumps` de un dict pequeno y `Queue.put`
(que encola en memoria y devuelve); toda la BFS, el texto, la llamada, la traduccion y el juicio de pregunta
ocurren en el proceso; y los resultados vuelven por la cola de salida que `recoge()` lee sin bloquear
(`get_nowait`). Lo unico que el hilo principal sigue pagando es lo de P6-23: la instantanea de cada juicio.
"""
from __future__ import annotations
import collections
import hashlib
import json
import math
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
import puerta_proceso_P6_23 as PX                          # noqa: E402
import puerta_proceso_P6_26 as PX26                        # noqa: E402
VERSION = "puerta_proceso27 (P6-27): encargo ligero por tic + memoria espejo en el proceso; el disparo, el texto, la llamada y el juicio de pregunta, todos en el proceso"
C = (24, 24)


def entorno27():
    e = PX26.entorno26(); e["version"] = VERSION; e["encargo"] = "ligero por tic (obs con ojos + accion + candidatos + escalares); memoria espejo en el proceso"
    return e


def _juez27(entrada, salida, entorno, rutas):
    os.environ.update(entorno)
    for r in reversed(rutas):
        if r not in sys.path:
            sys.path.insert(0, r)
    from alma import policy_cortex as PC
    from alma import policy_forma as PF
    from alma import forma_viva as FV
    from alma import relator_t5 as RT
    from alma import appraisal_zs_v42_exp as V42
    from alma import decisor_zs as D
    import policy_pareja as PP
    import arreglos_P6_6 as R6, arreglos_P6_8b as R8, filas10_P6_10 as F10, amenaza11_P6_11 as M11
    import policy_pareja16 as P16
    import policy_pareja23 as P23
    import policy_pareja26 as P26
    import oraculo_P6_14 as O
    import traductor_forma as TF
    import texto_escena_P6_26 as TX
    R6.aplica(PP.AlmaPareja, PC.log); R8.aplica(PC.log); F10.aplica(PC.log); M11.aplica(PC.log)
    mudo = lambda rec: None
    PC.log = mudo; PF.log = mudo; PP.log = mudo; P16.log = mudo; P23.log = mudo; P26.log = mudo
    espejo = P23.AlmaPareja23(con_proceso=False)
    espejo.hilo = None; espejo.evalua_en_hilo = False; espejo.phase = "live"
    modelo = PX26.Modelo()
    replay = None
    if os.environ.get("GEMV_RZ_REPLAY"):
        replay = {int(k): v for k, v in json.load(open(os.environ["GEMV_RZ_REPLAY"])).items()}
    # ── la memoria espejo: la del cuerpo, tic a tic, sin copiarla nunca ──
    E = {"mem": V42.Memoria(), "blo": D.Bloqueos(), "ultima_accion": None, "hist": collections.deque(maxlen=TX.VENTANA_RECIENTE + 2), "ult_pos": None, "n_tics": 0, "ms_tic": [], "ult_tick": -1}
    salida.put(("__listo__", None, 0.0, None, None))

    def pon_estado(job):
        if job.get("mundo") is not None:
            espejo.mundo = job["mundo"]
        espejo.tick = job["tick"]; espejo.conf.C = job["C"]; espejo.herm_dicho = job["herm_dicho"]; espejo.herm_tick = job["herm_tick"]; espejo.ultima_obs = job["ultima_obs"]
        espejo.mem = job["mem"]; espejo.bloqueos = job["blo"]; espejo.parte_herm = job.get("parte_herm"); espejo.ultimo_rec = job.get("ultimo_rec") or {}
        espejo.vivas = []; espejo.pendientes = {}; espejo.reeval_pend = {}; espejo.conf.callado_hasta = None

    def hilo_llamada(job, texto_escena, mem_pregunta, blo_pregunta):
        if replay is not None:
            # el banco del arreglo: la respuesta grabada en el campo, entregada cuando el cuerpo llega al tic en que volvio alli
            ent = replay.get(job["tick"]) or {}
            texto_r = ent.get("texto"); vuelto = int(ent.get("vuelto_en") or job["tick"])
            while E["ult_tick"] < vuelto - 1:
                time.sleep(0.0005)
            ms, usd, usage, err = 0.0, modelo.usd, None, (None if texto_r else "replay: sin respuesta grabada para este tic")
            with modelo.lock:
                modelo.n += 1
        else:
            texto_r, ms, usd, usage, err = modelo.llama(texto_escena)
        r = {"estado": "error", "error": err, "ms": ms, "usd_acumulado": round(usd, 6), "usage": usage, "texto": texto_r, "escena_md5": hashlib.md5(texto_escena.encode()).hexdigest(), "escena_largo": len(texto_escena), "llamadas": modelo.n}
        if texto_r:
            cnt = collections.Counter()
            try:
                formas, inf = TF.traduce(texto_r, job["escena_traductor"], job["filas"], cnt)
            except Exception as ex:
                formas, inf = [], {"fallos": [repr(ex)[:120]]}
            r["parsea"] = bool(inf.get("parsea")); r["callar"] = inf.get("callar"); r["n_formas_dichas"] = inf.get("n_formas"); r["fallos_traductor"] = inf.get("fallos")
            if formas:
                r["estado"] = "propone"; r["formas"] = formas; r["destino"] = next((list(t["destino"]) for t in formas[0]["tramos"] if t.get("destino")), None)
                r["mitades"] = [dict((t.get("_mitad") or {}), por=t.get("_por"), porque=t.get("_porque")) for t in formas[0]["tramos"]]
                entrada.put(pickle.dumps({"tipo": "juicio_pregunta", "ident": ("rzq", job["tick"]), "tramos": TF.solo_tramos(formas[0]), "obs": job["obs"], "mem": mem_pregunta, "blo": blo_pregunta, "tick": job["tick"], "C": job["C"],
                                          "herm_dicho": job["herm_dicho"], "herm_tick": job["herm_tick"], "ultima_obs": job["ultima_obs"], "mundo": None, "parte_herm": job.get("parte_herm")}, protocol=pickle.HIGHEST_PROTOCOL))
            elif inf.get("callar"):
                r["estado"] = "calla"
            else:
                r["estado"] = "intraducible"
        salida.put((("rz", job["tick"]), r, ms, None, None))

    while True:
        datos = entrada.get()
        if datos is None:
            break
        job = None
        try:
            job = pickle.loads(datos); t0 = time.perf_counter()
            if job["tipo"] == "juicio":
                pon_estado(job)
                fv = FV.FormaViva(job["fv"]["id"], job["fv"]["tramos"], job["fv"]["nace"], origen=job["fv"]["origen"])
                r = espejo._juzga(fv, job["obs"], job["mem"], job["blo"])
                salida.put((job["ident"], r, round((time.perf_counter() - t0) * 1000.0, 2), None, getattr(fv, "nec0", None)))
            elif job["tipo"] == "juicio_pregunta":
                pon_estado(job)
                fv = FV.FormaViva(f"Q{job['tick']}", job["tramos"], job["tick"], origen="consejero")
                ver, ar, cf, tics = espejo._juzga(fv, job["obs"], job["mem"], job["blo"])
                salida.put((job["ident"], {"veredicto": ver, "ventaja": round(float(ar or 0.0), 5), "tick_pregunta": job["tick"]}, round((time.perf_counter() - t0) * 1000.0, 2), None, None))
            elif job["tipo"] == "tic":
                # ── el espejo hace lo que el cuerpo hizo en policy_cortex.decidir:425-427, con el mismo obs ──
                if job.get("mundo") is not None:
                    espejo.mundo = job["mundo"]
                o2 = job["obs"]; t = job["tick"]; mem = E["mem"]; blo = E["blo"]; E["ult_tick"] = t; E["obs"] = o2
                mem.ultimo_ataque = job.get("ultimo_ataque", mem.ultimo_ataque)             # lo que el decisor escribio en el tic anterior (decisor_zs.py:904-908)
                if job.get("cedidos") is not None:
                    mem.cedidos = {tuple(k): v for k, v in job["cedidos"]}
                mem.observa(o2, espejo.mundo, t)
                blo.actualiza(o2, espejo.mundo, job.get("ultima_accion"), t)
                you = o2.get("you") or {}; pos = tuple(int(x) for x in you["pos"]) if you.get("pos") else None
                if pos is not None and (o2.get("phase") or "live") == "live":
                    r_now = float((o2.get("zone") or {}).get("radius") or 48); dps = (o2.get("zone") or {}).get("damage_per_s") or 0; dt = you.get("damage_taken") or []
                    E["hist"].append({"t": t, "hp": you.get("hp"), "zone_hit": any(isinstance(g, dict) and g.get("source") == "zone" for g in dt), "riv_hit": any(isinstance(g, dict) and str(g.get("source", "")).startswith("P") for g in dt),
                                      "arde": bool(dps) and math.dist(pos, C) > r_now, "movio": E["ult_pos"] is not None and pos != E["ult_pos"]})
                    E["ult_pos"] = pos
                E["n_tics"] += 1
                E["ms_tic"].append((time.perf_counter() - t0) * 1000.0)
                if E["n_tics"] % 500 == 0:
                    ms = sorted(E["ms_tic"][-500:])
                    salida.put((("rzm", t), {"estado": "espejo", "tics": E["n_tics"], "ms_tic_mediana": round(ms[len(ms) // 2], 3), "ms_tic_max": round(ms[-1], 3)}, 0.0, None, None))
            elif job["tipo"] == "pregunta":
                # ── la consulta: sobre el espejo tal como esta tras observar este tic (lo mismo que P6-26 copiaba) ──
                # la pregunta llega ANTES de que el cuerpo observe el tic t (`_oraculo16` corre antes de `policy_cortex.decidir`): la memoria
                # espejo esta en t-1 y el obs es el del tic t, exactamente lo que P6-26 copiaba en `encarga_razonador`
                t = job["tick"]; mem = E["mem"]; blo = E["blo"]; o2 = job.get("obs") or E.get("obs") or {}
                you = o2.get("you") or {}; pos = tuple(int(x) for x in you["pos"]) if you.get("pos") else None
                if pos is None or E["ult_tick"] > t:
                    salida.put((("rz", t), {"estado": "error", "error": f"el espejo va por delante de la pregunta ({E['ult_tick']} > {t})"}, 0.0, None, None)); continue
                E.setdefault("retraso_espejo", []).append(t - 1 - E["ult_tick"])      # 0 = el espejo esta en t-1, como debe; >0 = va por detras (cable mas rapido que el proceso)
                espejo.tick = t; espejo.mem = mem; espejo.bloqueos = blo; espejo.conf.C = job["C"]; espejo.herm_dicho = job["herm_dicho"]; espejo.herm_tick = job["herm_tick"]
                espejo.ultima_obs = job["ultima_obs"]; espejo.parte_herm = job.get("parte_herm"); espejo.ultimo_rec = job.get("ultimo_rec") or {}
                espejo.vivas = []; espejo.pendientes = {}; espejo.reeval_pend = {}; espejo.conf.callado_hasta = None
                if espejo.orac is None:
                    espejo.orac = O.Oraculo(espejo.mundo, int((you.get("stats") or {}).get("speed") or 5))
                orac = espejo.orac
                Dm = orac.bfs(pos); seg = orac.seguras(pos, t, Dm); ar, ta, pasos_a, holg = orac.dispara(pos, t, Dm, seg)
                if not (ar or (holg is not None and holg <= P16.MARGEN_DISPARO)):
                    salida.put((("rz", t), {"estado": "no dispara", "arde": ar, "holgura": holg}, round((time.perf_counter() - t0) * 1000.0, 2), None, None))
                else:
                    fases = [tuple(z) for z in (espejo.mundo.zone_schedule or [])]
                    hist = [x for x in E["hist"] if x["t"] < t]                      # P6-26 leia el historial hasta t-1
                    texto_escena = TX.texto(espejo, RT, V42, O, o2, job.get("cands") or {}, t, fases, hist, job.get("ult_e2"), job.get("parte_herm"), job.get("plan_hermano"))
                    jq = {"tick": t, "obs": o2, "C": job["C"], "herm_dicho": job["herm_dicho"], "herm_tick": job["herm_tick"], "ultima_obs": job["ultima_obs"], "parte_herm": job.get("parte_herm"), "filas": espejo._filas(),
                          "escena_traductor": {"pos": list(pos), "suelo": [{"id": it.get("id"), "pos": list(it["pos"])} for it in ((o2.get("visible") or {}).get("items") or []) if it.get("pos")]}}
                    mem_q = PX.instantanea(mem); blo_q = PX.instantanea(blo)        # en el proceso: no le cuesta nada al cuerpo
                    ms_texto = round((time.perf_counter() - t0) * 1000.0, 2)
                    salida.put((("rzt", t), {"estado": "pregunta hecha", "arde": ar, "holgura": holg, "n_seguras": len(seg), "ms_texto": ms_texto, "retraso_espejo": E["retraso_espejo"][-1], "escena_largo": len(texto_escena), "escena_md5": hashlib.md5(texto_escena.encode()).hexdigest(), "texto_escena": texto_escena}, ms_texto, None, None))
                    threading.Thread(target=hilo_llamada, args=(jq, texto_escena, mem_q, blo_q), daemon=True).start()
            else:
                salida.put((job.get("ident"), None, 0.0, "tipo de encargo desconocido en P6-27: " + str(job["tipo"]), None))
        except Exception as ex:
            salida.put(((job or {}).get("ident"), None, 0.0, repr(ex)[:200], None))


class HiloProceso27(PX26.HiloProceso26):
    def __init__(self):
        ctx = mp.get_context("spawn")
        self.entrada = ctx.Queue(); self.salida = ctx.Queue()
        self.lock = threading.Lock(); self.en_vuelo = 0; self.fvs = {}; self.listo = False
        self.ms_instantanea = []; self.mundo_enviado = False; self.errores = []; self.oraculo_en_vuelo = False; self.ms_oraculo_encargo = []
        self.razonador_en_vuelo = None; self.ms_razonador_encargo = []; self.ms_tic = []; self.bytes_tic = []; self.espejo = None
        self.p = ctx.Process(target=_juez27, args=(self.entrada, self.salida, dict(os.environ), list(sys.path)), daemon=True)
        self.p.start()

    def manda_tic(self, alma, obs, tick):
        """EL ENCARGO LIGERO DE CADA TIC: el mismo `obs` que el cuerpo acaba de observar (con los mensajes gemelos del oido
        y los ojos), la accion del tic anterior (la que `bloqueos.actualiza` usa) y los dos campos que escribe el decisor."""
        t0 = time.perf_counter()
        job = {"tipo": "tic", "tick": tick, "obs": obs, "ultima_accion": alma.ultima_accion, "mundo": (None if self.mundo_enviado else alma.mundo),
               "ultimo_ataque": alma.mem.ultimo_ataque, "cedidos": ([(list(k), v) for k, v in alma.mem.cedidos.items()] if alma.mem.cedidos else None)}
        datos = pickle.dumps(job, protocol=pickle.HIGHEST_PROTOCOL)
        self.mundo_enviado = True
        self.entrada.put(datos)
        self.ms_tic.append((time.perf_counter() - t0) * 1000.0); self.bytes_tic.append(len(datos))

    def pregunta(self, alma, obs, cands, extra):
        """LA CONSULTA: lo que P6-26 leia en el momento de la pregunta, sin la memoria ni los bloqueos (el espejo los tiene)."""
        t0 = time.perf_counter()
        herm = getattr(alma.mundo, "teammate_slot", None)
        ult = {"visible": {"agents": [dict(a) for a in (((alma.ultima_obs or {}).get("visible") or {}).get("agents") or []) if a.get("slot") == herm]}}
        job = {"tipo": "pregunta", "tick": alma.tick, "obs": obs, "cands": cands, "C": alma.conf.C, "herm_dicho": alma.herm_dicho, "herm_tick": alma.herm_tick, "ultima_obs": ult, "parte_herm": getattr(alma, "parte_herm", None),
               "ultimo_rec": getattr(alma, "ultimo_rec", None), "mundo": None, **(extra or {})}
        with self.lock:
            self.razonador_en_vuelo = alma.tick
        datos = pickle.dumps(job, protocol=pickle.HIGHEST_PROTOCOL)
        self.entrada.put(datos)
        self.ms_razonador_encargo.append((time.perf_counter() - t0) * 1000.0)

    def recoge(self):
        out = []
        for ident, r, ms, err in super().recoge():
            if isinstance(ident, tuple) and ident and ident[0] == "rzm":
                self.espejo = r; continue
            out.append((ident, r, ms, err))
        return out

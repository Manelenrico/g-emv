"""[P6-26 · 2] EL PROCESO JUEZ DE A8: el de P6-23 (`puerta_proceso_P6_23`: juicio de la puerta y tic del
oraculo en un proceso aparte) con un encargo nuevo, EL RAZONADOR:

  · el hilo principal solo abre la puerta de entrada (fase, plan vivo, cadencia, silencio, piernas
    listas, ninguno en vuelo) y manda la instantanea (`encarga_razonador`: lo mismo que `encarga_juicio`
    mas los candidatos del cuerpo, el parte del hermano, su ultimo mensaje, el plan que mando por el canal
    y los ultimos 100 tics);
  · el proceso decide si dispara (el MISMO disparo que el oraculo de A7h: arde o la holgura <= 33), construye
    el texto de la escena (`texto_escena_P6_26`, la via del cinco + las palabras del seis) sobre el alma
    espejo, y hace LA LLAMADA AL MODELO EN UN HILO DEL PROCESO: ni el hilo principal ni el bucle del juez la
    esperan; los juicios de la puerta siguen sirviendose mientras el modelo piensa;
  · cuando vuelve, el hilo traduce (`traductor_forma`) y devuelve la propuesta al hilo principal, que la
    deja en `cf.entregado` (como la del oraculo) y la puerta la juzga con la observacion DEL TIC EN QUE
    LLEGA (`policy_pareja26.AlmaPareja26._recoge`: `encarga_juicio(fv, self, obs)` con el `obs` de ese tic);
  · ademas, el proceso juzga esa misma propuesta con la instantanea DE LA PREGUNTA (encargo interno
    `juicio_pregunta`), solo para medir «respuestas que llegan a una escena donde la puerta ya rechaza».

La llamada va por el sidecar de Bedrock de la plataforma (`AWS_ENDPOINT_URL_BEDROCK_RUNTIME`,
`BEDROCK_MODEL`, como el brazo F del cinco: `policy_forma._llama`), con el gasto leido de la cabecera
`X-Coworld-Spend-Usd` y un tope propio (`GEMV_RZ_TOPE_USD`); en el Mac, para el humo, `GEMV_RAZONADOR_LOCAL=
anthropic` usa la clave de `cantera/paper5/.env` (nunca impresa ni escrita) y `=mock` responde un plan fijo.
"""
from __future__ import annotations
import collections
import hashlib
import json
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
VERSION = "puerta_proceso26 (P6-26): el de P6-23 + encargo razonador (texto en el proceso, llamada en un hilo del proceso, juicio de llegada en el principal y de pregunta en el proceso)"
TOPE_USD = float(os.environ.get("GEMV_RZ_TOPE_USD", "0.6") or 0.6)      # por vida (pod), leido de la cabecera del sidecar
TOPE_LLAMADAS = int(os.environ.get("GEMV_RZ_TOPE_LLAMADAS", "200") or 200)
TIMEOUT_S = float(os.environ.get("GEMV_CORTEX_TIMEOUT", "25") or 25)
MAX_TOKENS = 1500
COLA = "Responde ahora con el JSON de formas para esta escena, siguiendo el esquema exacto de la instruccion."
MOCK = '{"formas": [{"tramos": [{"destino": [24, 24], "intencion": "ir", "vida": "+", "manos": "0", "vinculo": "0", "por": "F-ANTICIPACION", "porque": "al centro"}, {"destino": null, "intencion": "esperar", "esperar": 50, "vida": "+", "manos": "0", "vinculo": "0", "por": "F-ANTICIPACION", "porque": "quedarme"}], "final": "dentro"}], "callar": false}'
PRECIO_HAIKU = {"in": 1.00, "out": 5.00, "cw": 1.25, "cr": 0.10}      # USD por millon, para el modo local


def instantanea(x):
    return PX.instantanea(x)


def _lee(nombre):
    for base in ("/app/alma", AQUI, os.path.join(RAIZ, "cantera", "paper5")):
        p = os.path.join(base, nombre)
        if os.path.exists(p):
            return open(p, encoding="utf-8").read().strip()
    raise FileNotFoundError(nombre)


def sistema26():
    return _lee("instruccion_forma.md") + "\n\n---\n\n" + _lee("tabla_ensenada.md") + "\n\n---\n\n" + _lee("instruccion_P6_25.md")


def entorno26():
    return {"version": VERSION, "sidecar": bool(os.environ.get("AWS_ENDPOINT_URL_BEDROCK_RUNTIME")), "modelo": os.environ.get("BEDROCK_MODEL"), "local": os.environ.get("GEMV_RAZONADOR_LOCAL") or None,
            "tope_usd_por_vida": TOPE_USD, "tope_llamadas": TOPE_LLAMADAS, "timeout_s": TIMEOUT_S, "max_tokens": MAX_TOKENS, "sistema_md5": hashlib.md5(sistema26().encode()).hexdigest(), "proceso": PX.entorno23()}


class Modelo:
    """La llamada, con el gasto contado. Devuelve (texto, ms, usd_acumulado, usage, error)."""

    def __init__(self):
        self.ep = os.environ.get("AWS_ENDPOINT_URL_BEDROCK_RUNTIME"); self.modelo = os.environ.get("BEDROCK_MODEL"); self.local = os.environ.get("GEMV_RAZONADOR_LOCAL") or ""
        self.n = 0; self.usd = 0.0; self.lock = threading.Lock(); self.cli = None
        from alma import cortex_t5 as CX
        self.manual = CX._manual(); self.cabecera = CX.CABECERA; self.sistema = sistema26()

    def bloques(self, texto):
        b = []
        if self.manual:
            b.append({"type": "text", "text": f"{self.cabecera}\n\n{self.manual}\n\n---\n\n", "cache_control": {"type": "ephemeral"}})
        b.append({"type": "text", "text": texto + "\n\n" + COLA})
        return b

    def llama(self, texto):
        with self.lock:
            if self.n >= TOPE_LLAMADAS:
                return None, 0.0, self.usd, None, "freno: tope de llamadas"
            if self.usd >= TOPE_USD:
                return None, 0.0, self.usd, None, "freno: tope de gasto"
            self.n += 1
        t0 = time.perf_counter()
        try:
            if self.local == "mock":
                time.sleep(0.05); texto_r, usage, spend = MOCK, {"input_tokens": 0, "output_tokens": 0}, None
            elif self.local == "anthropic":
                if self.cli is None:
                    import consejero_forma as CF
                    self.cli = CF.cliente()
                r = self.cli.messages.create(model="claude-haiku-4-5-20251001", max_tokens=MAX_TOKENS, system=[{"type": "text", "text": self.sistema}], messages=[{"role": "user", "content": self.bloques(texto)}])
                texto_r = "".join(b.text for b in r.content if getattr(b, "type", "") == "text"); usage = r.usage.model_dump() if hasattr(r.usage, "model_dump") else dict(r.usage); spend = None
                p = PRECIO_HAIKU
                with self.lock:
                    self.usd += (usage.get("input_tokens", 0) * p["in"] + usage.get("output_tokens", 0) * p["out"] + usage.get("cache_creation_input_tokens", 0) * p["cw"] + usage.get("cache_read_input_tokens", 0) * p["cr"]) / 1e6
            elif self.ep and self.modelo:
                import urllib.request
                cuerpo = {"anthropic_version": "bedrock-2023-05-31", "max_tokens": MAX_TOKENS, "system": self.sistema, "messages": [{"role": "user", "content": self.bloques(texto)}]}
                req = urllib.request.Request(f"{self.ep.rstrip('/')}/model/{self.modelo}/invoke", data=json.dumps(cuerpo).encode(), method="POST", headers={"Content-Type": "application/json", "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=TIMEOUT_S) as rr:
                    crudo = rr.read(400000).decode("utf-8", "replace"); cab = {k.lower(): v for k, v in rr.headers.items()}
                d = json.loads(crudo); texto_r = "".join(b.get("text", "") for b in (d.get("content") or []) if b.get("type") == "text"); usage = d.get("usage")
                spend = cab.get("x-coworld-spend-usd")
                try:
                    with self.lock:
                        self.usd = float(spend)
                except (TypeError, ValueError):
                    pass
            else:
                return None, 0.0, self.usd, None, "sin sidecar (AWS_ENDPOINT_URL_BEDROCK_RUNTIME / BEDROCK_MODEL) ni modo local"
        except Exception as ex:
            return None, round((time.perf_counter() - t0) * 1000.0, 1), self.usd, None, f"{type(ex).__name__}: {str(ex)[:160]}"
        return texto_r, round((time.perf_counter() - t0) * 1000.0, 1), self.usd, usage, None


def _juez26(entrada, salida, entorno, rutas):
    os.environ.update(entorno)
    for r in reversed(rutas):
        if r not in sys.path:
            sys.path.insert(0, r)
    from alma import policy_cortex as PC
    from alma import policy_forma as PF
    from alma import forma_viva as FV
    from alma import relator_t5 as RT
    from alma import appraisal_zs_v42_exp as V42
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
    modelo = Modelo()
    salida.put(("__listo__", None, 0.0, None, None))

    def pon_estado(job):
        if job.get("mundo") is not None:
            espejo.mundo = job["mundo"]
        espejo.tick = job["tick"]; espejo.conf.C = job["C"]; espejo.herm_dicho = job["herm_dicho"]; espejo.herm_tick = job["herm_tick"]; espejo.ultima_obs = job["ultima_obs"]
        espejo.mem = job["mem"]; espejo.bloqueos = job["blo"]; espejo.parte_herm = job.get("parte_herm"); espejo.ultimo_rec = job.get("ultimo_rec") or {}
        espejo.vivas = []; espejo.pendientes = {}; espejo.reeval_pend = {}; espejo.conf.callado_hasta = None

    def hilo_llamada(job, texto_escena, t_encargo):
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
                # el juicio con la instantanea DE LA PREGUNTA, encargado al bucle del juez (solo medida)
                entrada.put(pickle.dumps({"tipo": "juicio_pregunta", "ident": ("rzq", job["tick"]), "tramos": TF.solo_tramos(formas[0]), "obs": job["obs"], "mem": job["mem"], "blo": job["blo"], "tick": job["tick"], "C": job["C"],
                                          "herm_dicho": job["herm_dicho"], "herm_tick": job["herm_tick"], "ultima_obs": job["ultima_obs"], "mundo": None}, protocol=pickle.HIGHEST_PROTOCOL))
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
            elif job["tipo"] == "razonador":
                pon_estado(job)
                obs = job["obs"]; you = obs.get("you") or {}
                if espejo.orac is None:
                    espejo.orac = O.Oraculo(espejo.mundo, int((you.get("stats") or {}).get("speed") or 5))
                orac = espejo.orac; pos = tuple(int(x) for x in you["pos"]); t = job["tick"]
                Dm = orac.bfs(pos); seg = orac.seguras(pos, t, Dm); ar, ta, pasos_a, holg = orac.dispara(pos, t, Dm, seg)
                if not (ar or (holg is not None and holg <= P16.MARGEN_DISPARO)):
                    salida.put((job["ident"], {"estado": "no dispara", "arde": ar, "holgura": holg}, round((time.perf_counter() - t0) * 1000.0, 2), None, None)); continue
                fases = [tuple(z) for z in (espejo.mundo.zone_schedule or [])]
                texto_escena = TX.texto(espejo, RT, V42, O, obs, job.get("cands") or {}, t, fases, job.get("hist") or [], job.get("ult_e2"), job.get("parte_herm"), job.get("plan_hermano"))
                job["filas"] = espejo._filas(); job["escena_traductor"] = {"pos": list(pos), "suelo": [{"id": it.get("id"), "pos": list(it["pos"])} for it in ((obs.get("visible") or {}).get("items") or []) if it.get("pos")]}
                ms_texto = round((time.perf_counter() - t0) * 1000.0, 2)
                salida.put((("rzt", t), {"estado": "pregunta hecha", "arde": ar, "holgura": holg, "n_seguras": len(seg), "ms_texto": ms_texto, "escena_largo": len(texto_escena), "escena_md5": hashlib.md5(texto_escena.encode()).hexdigest(), "texto_escena": texto_escena}, ms_texto, None, None))
                threading.Thread(target=hilo_llamada, args=(job, texto_escena, t), daemon=True).start()
            else:   # oraculo, como en P6-23 (no se usa en A8, se conserva)
                pon_estado(job)
                espejo.mem = PX.MemLite(job["pareja_muerta"], job["pareja_pos"]); espejo.ult_oraculo = job["ult_oraculo"]; espejo.n_oraculo = job["n_oraculo"]
                regs = []; P23.log = regs.append
                try:
                    espejo._oraculo_calcula(job["obs"])
                finally:
                    P23.log = mudo
                with espejo.cf.lock:
                    e, espejo.cf.entregado = espejo.cf.entregado, None
                salida.put((job["ident"], {"entregado": e, "registros": regs, "ult_oraculo": espejo.ult_oraculo, "n_oraculo": espejo.n_oraculo}, round((time.perf_counter() - t0) * 1000.0, 2), None, None))
        except Exception as ex:
            salida.put(((job or {}).get("ident"), None, 0.0, repr(ex)[:200], None))


class HiloProceso26(PX.HiloProceso23):
    def __init__(self):
        ctx = mp.get_context("spawn")
        self.entrada = ctx.Queue(); self.salida = ctx.Queue()
        self.lock = threading.Lock(); self.en_vuelo = 0; self.fvs = {}; self.listo = False
        self.ms_instantanea = []; self.mundo_enviado = False; self.errores = []; self.oraculo_en_vuelo = False; self.ms_oraculo_encargo = []
        self.razonador_en_vuelo = None; self.ms_razonador_encargo = []
        self.p = ctx.Process(target=_juez26, args=(self.entrada, self.salida, dict(os.environ), list(sys.path)), daemon=True)
        self.p.start()

    def encarga_razonador(self, alma, obs, cands, extra):
        t0 = time.perf_counter()
        herm = getattr(alma.mundo, "teammate_slot", None)
        ult = {"visible": {"agents": [dict(a) for a in (((alma.ultima_obs or {}).get("visible") or {}).get("agents") or []) if a.get("slot") == herm]}}
        job = {"tipo": "razonador", "ident": ("rz", alma.tick), "obs": obs, "mem": alma.mem, "blo": alma.bloqueos, "tick": alma.tick, "C": alma.conf.C, "herm_dicho": alma.herm_dicho, "herm_tick": alma.herm_tick,
               "ultima_obs": ult, "mundo": (None if self.mundo_enviado else alma.mundo), "cands": cands, "parte_herm": getattr(alma, "parte_herm", None), "ultimo_rec": getattr(alma, "ultimo_rec", None), **extra}
        with self.lock:
            self.razonador_en_vuelo = alma.tick
        self._envia(job)
        self.ms_razonador_encargo.append((time.perf_counter() - t0) * 1000.0)

    def recoge(self):
        out = []
        while True:
            try:
                ident, r, ms, err, nec0 = self.salida.get_nowait()
            except queue.Empty:
                break
            if ident == "__listo__":
                self.listo = True; continue
            if isinstance(ident, tuple) and ident and ident[0] in ("rz", "rzt", "rzq"):
                if ident[0] == "rz":
                    with self.lock:
                        self.razonador_en_vuelo = None
                if err:
                    self.errores.append((ident, err))
                out.append((ident, r, ms, err)); continue
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

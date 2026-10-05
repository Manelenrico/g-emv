"""[P6-26] LA POLITICA DEL BRAZO A8: A7h (`policy_pareja23`: cuerpo del seis congelado + puerta6 en proceso
aparte + plan «ir y quedarse» + compromiso6c con el veto V2 de Manel y la cuenta justa) con UN cambio en el
sitio del oraculo y dos anadidos, y solo esos:

  1. Donde A7h llamaba al oraculo de reglas, A8 pide un plan a SU razonador (Haiku 4.5) con la escena del
     seis en lenguaje llano (P6-25). La llamada no toca el hilo principal: va en un hilo del proceso juez
     (`puerta_proceso_P6_26`). Cada hermano tiene el suyo (cada pod, su proceso, su razonador).
  2. La puerta juzga con la instantanea DEL MOMENTO EN QUE LLEGA la respuesta, no la de cuando se pidio:
     en `_recoge_hilo` la propuesta vuelta se deja en `cf.entregado`, y en el mismo tic `_recoge(obs)`
     (heredado de P6-23) hace `self.hilo.encarga_juicio(fv.id, fv, self, obs)` con el `obs` de ESE tic y la
     memoria de ESE tic. Esta escrito abajo en `_aplica_razonador` (el tick de llegada queda en el diario).
  3. El plan que acepta la puerta propia viaja al hermano por el canal de equipo EN LUGAR de un parte E2
     (`texto_escena_P6_26.mensaje_plan`, <= 120 caracteres, ASCII): la voz del cuerpo (`PARTE.emite`, cada
     25 tics) manda ese mensaje una vez y vuelve al E2. El razonador del hermano lo recibe en su escena
     siguiente (bloque «El plan de tu hermano»).

Y el diario del siete: por cada plan aceptado, al cerrarse, `malestar26` con tres columnas por tramo:
lo propuesto (la mitad emocional dicha), lo imaginado (los signos proyectados por la puerta y su curva de
necesidades) y lo pasado (los signos y las necesidades sentidas en los puntos de control).
"""
from __future__ import annotations
import collections
import math
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
import puerta_proceso_P6_26 as PX26                       # noqa: E402
import texto_escena_P6_26 as TX                           # noqa: E402
import arreglos_P6_6 as R6                                # noqa: E402
import arreglos_P6_8b as R8                               # noqa: E402
import filas10_P6_10 as F10                               # noqa: E402
import amenaza11_P6_11 as M11                             # noqa: E402
import parte2 as P2                                       # noqa: E402
log = PF.log
VERSION = "policy_pareja26 (P6-26): A7h con el razonador Haiku en el sitio del oraculo (en el proceso), juicio con la instantanea de llegada, plan al hermano por el canal en lugar de un E2, malestar26"
C = (24, 24)


def entorno26():
    e = P23.entorno23(); e.update({"version": VERSION, "razonador": PX26.entorno26(), "mensaje_plan": "P6 P<slot> t<tick> D<x>,<y> H<H> F<fin> (<= 120, sustituye un E2)"})
    return e


class AlmaPareja26(P23.AlmaPareja23):
    def __init__(self, *a, hilo=None, **k):
        super().__init__(*a, con_proceso=False, **k)
        self.hilo = hilo or PX26.HiloProceso26(); self.evalua_en_hilo = True     # [P6-27] `hilo` inyectable: el encargo ligero
        self.hist26 = collections.deque(maxlen=TX.VENTANA_RECIENTE + 2); self.ult_e2 = None; self.plan_hermano = None; self.ult_pos = None; self.ult_cands = {}
        self.msg_pendiente = None; self.k_llamadas = 0; self.k_e2_sustituidos = 0; self.k_planes_hermano = 0; self.k_intraducibles = 0; self.k_calla = 0; self.k_errores = 0; self.k_no_dispara = 0
        self.k_propuestas = 0; self.retrasos = []; self.usd_visto = 0.0; self.k_ya_rechaza = 0; self.k_pregunta_ok = 0; self.pregunta_pend = {}; self.k_aceptadas = 0; self.k_malestar = 0
        self.ult_rz = -10 ** 9

    # ── el sitio del oraculo: A8 pregunta al razonador ────────────────────────────────────
    def _oraculo16(self, obs):
        if self.mundo is None or (obs.get("phase") or self.phase) != "live":
            return
        t = self.tick
        you = obs.get("you") or {}
        if self.orac is None:
            import oraculo_P6_14 as O
            self.orac = O.Oraculo(self.mundo, int((you.get("stats") or {}).get("speed") or 5))
            log({"k": "oraculo16", "tick": t, "estado": "listo", "plan": "razonador Haiku (A8)", "en_proceso": True, "fases": self.orac.fases})
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
        self.ult_rz = t
        self.hilo.encarga_razonador(self, obs, dict(self.ult_cands), {"ult_e2": self.ult_e2, "plan_hermano": self.plan_hermano, "hist": list(self.hist26)})
        log({"k": "razonador26", "tick": t, "estado": "encargado al proceso", "ms_encargo": round(self.hilo.ms_razonador_encargo[-1], 2), "plan_hermano": bool(self.plan_hermano)})

    def _aplica_razonador(self, t_pregunta, r, ms):
        """La propuesta vuelve del proceso en ESTE tic (`self.tick`): se deja en `cf.entregado` y en este
        mismo tic `_recoge(obs)` (P6-23) la encarga a la puerta con el `obs` y la memoria DE AHORA, no los de
        `t_pregunta`. Ese es el juicio con la instantanea de llegada."""
        est = r.get("estado")
        rec = {"k": "razonador26", "tick": self.tick, "estado": est, "tick_pregunta": t_pregunta, "tics_de_vuelta": self.tick - t_pregunta, "ms_llamada": r.get("ms"), "usd_acumulado": r.get("usd_acumulado"), "usage": r.get("usage"),
               "llamadas": r.get("llamadas"), "error": r.get("error"), "escena_md5": r.get("escena_md5"), "escena_largo": r.get("escena_largo"), "parsea": r.get("parsea"), "callar": r.get("callar"), "n_formas_dichas": r.get("n_formas_dichas"),
               "fallos_traductor": r.get("fallos_traductor"), "destino": r.get("destino"), "mitades": r.get("mitades"), "texto": r.get("texto"), "juzgada_con": "la instantanea del tic de llegada (obs y memoria de self.tick en _recoge)"}
        log(rec)
        if est == "no dispara":
            self.k_no_dispara += 1; return
        self.k_llamadas += 1; self.retrasos.append(self.tick - t_pregunta)
        if r.get("usd_acumulado") is not None:
            self.usd_visto = float(r["usd_acumulado"])
        if est == "error":
            self.k_errores += 1; return
        if est == "calla":
            self.k_calla += 1; return
        if est == "intraducible":
            self.k_intraducibles += 1; return
        self.k_propuestas += 1; self.ult_oraculo = self.tick; self.n_oraculo += 1
        if self.vivas or getattr(self, "pendientes", {}) or self.reeval_pend:
            log({"k": "razonador26", "tick": self.tick, "estado": "propuesta descartada: ya hay plan", "tick_pregunta": t_pregunta}); return
        with self.cf.lock:
            self.cf.entregado = {"tick": self.tick, "formas": r["formas"], "callar": False}
        self.pregunta_pend[t_pregunta] = {"tick_llegada": self.tick, "id": self.n_forma + 1}

    def _recoge_hilo(self, obs):
        if self.hilo is None:
            return
        hechos = self.hilo.recoge(); otros = []
        for ident, r, ms, err in hechos:
            if isinstance(ident, tuple) and ident and ident[0] == "rz":
                if err or r is None:
                    self.k_errores += 1; log({"k": "razonador26", "tick": self.tick, "estado": "error en el proceso", "error": err}); continue
                self._aplica_razonador(ident[1], r, ms)
            elif isinstance(ident, tuple) and ident and ident[0] == "rzt":
                log({"k": "razonador26", "tick": self.tick, "tick_pregunta": ident[1], **{k: v for k, v in (r or {}).items()}})
            elif isinstance(ident, tuple) and ident and ident[0] == "rzq":
                p = self.pregunta_pend.get(ident[1]) or {}
                log({"k": "razonador26", "tick": self.tick, "estado": "juicio con la instantanea de la pregunta", "tick_pregunta": ident[1], "veredicto_pregunta": (r or {}).get("veredicto"), "ventaja_pregunta": (r or {}).get("ventaja"), "id": p.get("id")})
                if (r or {}).get("veredicto") == "ok":
                    self.k_pregunta_ok += 1
                p["veredicto_pregunta"] = (r or {}).get("veredicto")
            else:
                otros.append((ident, r, ms, err))
        _rec = self.hilo.recoge
        self.hilo.recoge = lambda: otros
        try:
            super()._recoge_hilo(obs)
        finally:
            self.hilo.recoge = _rec
        # las respuestas que llegan a una escena donde la puerta ya rechaza: pasaban en la pregunta, no a la llegada
        for fv in list(self.vivas):
            if not getattr(fv, "anunciada", False):
                fv.anunciada = True; self.k_aceptadas += 1
                i = next((k for k, v in self.pregunta_pend.items() if v.get("id") == fv.id), None)
                if i is not None:
                    self.pregunta_pend[i]["veredicto_llegada"] = "ok"
                dest = next((tuple(t["destino"]) for t in fv.tramos if t.get("destino")), None)
                if dest is not None:
                    fin = (self.orac.fases[self.orac.fase_activa(self.tick) + 1][0] if (self.orac and self.orac.fase_activa(self.tick) is not None and self.orac.fase_activa(self.tick) + 1 < len(self.orac.fases)) else self.tick + 400)
                    H = sum(int(t.get("esperar") or 0) for t in fv.tramos)
                    self.msg_pendiente = TX.mensaje_plan(self.mundo.slot, self.tick, dest, H, fin)
                    log({"k": "plan26", "tick": self.tick, "estado": "plan aceptado, mensaje preparado", "id": fv.id, "mensaje": self.msg_pendiente})
        for c in list(self.cerradas):
            pass

    def _cierra(self, fv, mal):
        super()._cierra(fv, mal)
        # el diario del siete: propuesto / imaginado / pasado, por tramo
        det = self._detalle(fv)
        nec_im = [(c or {}).get("nec") for c in (fv.curva or [])]
        nec_re = [getattr(fv, "real_nec", {}).get(i) for i in range(len(fv.tics or []))]
        self.k_malestar += 1
        log({"k": "malestar26", "tick": self.tick, "id": fv.id, "estado": fv.estado, "motivo": getattr(fv, "motivo_caida", None), "nace": fv.nace, "tics": list(fv.tics or []), "nec0": getattr(fv, "nec0", None),
             "tramos": [{"i": d.get("i"), "propuesto": {"dicho": d.get("dicho"), "por": d.get("por"), "porque": d.get("porque")}, "imaginado": {"signos": d.get("proyectado"), "nec": (nec_im[i] if i < len(nec_im) else None)},
                         "pasado": {"signos": d.get("real"), "nec": (nec_re[i] if i < len(nec_re) else None)}} for i, d in enumerate(det)]})
        # la puerta ya rechaza: la pregunta decia ok y la llegada no (se sabe al cerrar la pendiente)
        for k, v in list(self.pregunta_pend.items()):
            if v.get("id") == fv.id:
                if v.get("veredicto_pregunta") == "ok" and v.get("veredicto_llegada") != "ok":
                    self.k_ya_rechaza += 1
                self.pregunta_pend.pop(k, None)

    # ── el hilo principal, tras la decision: lo que el razonador leera ────────────────────
    def _decidir_forma(self, obs):
        accion, radio = super()._decidir_forma(obs)
        try:
            if radio is not None and self.phase == "live" and self.mundo is not None:
                t = self.tick; o2 = self.ultima_obs or obs; you = o2.get("you") or {}
                pos = tuple(int(x) for x in you.get("pos")) if you.get("pos") else None
                herm = self.mundo.teammate_slot
                for m in (obs.get("chat") or []):
                    if m.get("channel") == "team" and m.get("from") == herm:
                        tx = str(m.get("text") or "")
                        if tx.startswith("E2 "):
                            self.ult_e2 = tx
                        elif tx.startswith(TX.MARCA_PLAN + " "):
                            p = TX.parsea_plan(tx)
                            if p:
                                self.plan_hermano = p; self.k_planes_hermano += 1
                                log({"k": "plan26", "tick": t, "estado": "plan del hermano recibido", "mensaje": tx, "plan": {"destino": list(p["destino"]), "H": p["H"], "fin": p["fin"], "t": p["t"]}})
                if pos is not None:
                    r_now = float((o2.get("zone") or {}).get("radius") or 48); dps = (o2.get("zone") or {}).get("damage_per_s") or 0; dt = you.get("damage_taken") or []
                    self.hist26.append({"t": t, "hp": you.get("hp"), "zone_hit": any(isinstance(g, dict) and g.get("source") == "zone" for g in dt), "riv_hit": any(isinstance(g, dict) and str(g.get("source", "")).startswith("P") for g in dt),
                                        "arde": bool(dps) and math.dist(pos, C) > r_now, "movio": self.ult_pos is not None and pos != self.ult_pos})
                    self.ult_pos = pos
                self.ult_cands = {k: (float(v["d"]) if isinstance(v, dict) and v.get("d") is not None else (float(v) if isinstance(v, (int, float)) else 0.0)) for k, v in (radio.get("candidatos") or {}).items()}
        except Exception as ex:
            log({"k": "forma_error", "tick": self.tick, "donde": "decidir26", "error": repr(ex)[:200]})
        return accion, radio

    # la fase de aviso puede cambiar el sitio: no se toca compromiso6c ni la puerta


def envuelve_voz(alma):
    """[P6-26 · 3] El plan aceptado sale por el canal EN LUGAR de un E2: se envuelve la voz que P6-3 ya
    envolvio (`policy_pareja._envuelve`), una vez por plan, y se vuelve al E2."""
    _e2 = PC.PARTE.emite

    def _emite(msg, tick, mundo, mem, ventana, _a=alma):
        if _a.msg_pendiente:
            s, _a.msg_pendiente = _a.msg_pendiente, None
            _a.k_e2_sustituidos += 1
            log({"k": "plan26", "tick": tick, "estado": "mensaje del plan dicho (en lugar de un E2)", "texto": s, "largo": len(s)})
            return s
        return _e2(msg, tick, mundo, mem, ventana)
    PC.PARTE.emite = _emite


def resumen26(alma):
    r = P23.resumen23(alma); r["k"] = "resumen26"
    rs = sorted(alma.retrasos)
    r.update({"llamadas": alma.k_llamadas, "usd_visto": round(alma.usd_visto, 6), "no_dispara": alma.k_no_dispara, "propuestas": alma.k_propuestas, "intraducibles": alma.k_intraducibles, "calla": alma.k_calla, "errores": alma.k_errores,
              "retraso_tics": {"n": len(rs), "mediana": (rs[len(rs) // 2] if rs else None), "p95": (rs[min(len(rs) - 1, int(0.95 * len(rs)))] if rs else None), "max": (rs[-1] if rs else None)},
              "aceptadas": alma.k_aceptadas, "pregunta_ok": alma.k_pregunta_ok, "llegan_donde_la_puerta_ya_rechaza": alma.k_ya_rechaza, "e2_sustituidos": alma.k_e2_sustituidos, "planes_del_hermano_recibidos": alma.k_planes_hermano, "malestar_registros": alma.k_malestar,
              "encargos_razonador_ms": {"n": len(alma.hilo.ms_razonador_encargo), "max": (round(max(alma.hilo.ms_razonador_encargo), 2) if alma.hilo.ms_razonador_encargo else None)}})
    return r


async def run(url):
    import asyncio
    import websockets
    hecho = R6.aplica(PP.AlmaPareja, log); hecho8 = R8.aplica(log); hecho10 = F10.aplica(log); hecho11 = M11.aplica(log)
    alma = AlmaPareja26()
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION, "entorno": PF.CX.entorno_efectivo(), "entorno_forma": PF.entorno_forma(), "entorno_ojos": PP.entorno_ojos(),
         "entorno_arreglos": R6.entorno(), "arreglos": hecho, "entorno_arreglos8": R8.entorno(), "arreglos8": hecho8, "entorno_filas10": F10.entorno(), "filas10": hecho10,
         "entorno_manos11": M11.entorno(), "manos11": hecho11, "entorno23": entorno26(), "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if PP.OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "A8 = A7h con el razonador Haiku en el sitio del oraculo (proceso), juicio con la instantanea de llegada, plan al hermano por el canal"})
    PP._envuelve(alma); envuelve_voz(alma)
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
    log(resumen26(alma))
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    try:
        alma.hilo.cierra()
    except Exception:
        pass
    PC.sube_artefacto(alma, "fin de la partida")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL") or os.environ["COGAMES_ENGINE_WS_URL"]))

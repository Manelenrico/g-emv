"""[P6-23] LA POLITICA DE LOS BRAZOS A7v / A7h. ARCHIVO NUEVO, DECLARADO.
= el cuerpo del seis congelado (A4) + el oraculo con el plan «ir y quedarse» (P6-18) + la
puerta del cinco (A7v: con su comparador, GEMV_PUERTA6=0; A7h: con el comparador puerta6,
GEMV_PUERTA6=1, el interruptor de `policy_pareja16`) + `compromiso6c_P6_23` (veto V2 de
Manel y cuenta justa) + la infraestructura de P6-22/P6-23: el juicio de la puerta Y el tic de
propuesta del oraculo corren en un proceso aparte (`puerta_proceso_P6_23`), el hilo principal
solo hace instantaneas. No importa `policy_pareja18` (exige GEMV_PUERTA6=1): sus dos piezas
—`texto_quedarse` y el calculo del oraculo con ese plan— se copian aqui tal cual, declaradas.
"""
from __future__ import annotations
import json
import os
import sys
import time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
from alma import policy_cortex as PC                      # noqa: E402
from alma import policy_forma as PF                       # noqa: E402
from alma import forma_viva as FV                         # noqa: E402
import traductor_forma as TF                              # noqa: E402
import policy_pareja as PP                                # noqa: E402
import policy_pareja16 as P16                             # noqa: E402
import oraculo_P6_14 as O                                 # noqa: E402
import compromiso6c_P6_23 as C6c                          # noqa: E402
import puerta_proceso_P6_23 as PX                         # noqa: E402
import arreglos_P6_6 as R6                                # noqa: E402
import arreglos_P6_8b as R8                               # noqa: E402
import filas10_P6_10 as F10                               # noqa: E402
import amenaza11_P6_11 as M11                             # noqa: E402
import parte2 as P2                                       # noqa: E402
log = PF.log
VERSION = "policy_pareja23 (P6-23): A4 + oraculo ir-y-quedarse + puerta del cinco (comparador del cinco o puerta6) + compromiso6c + juicio y oraculo en proceso aparte"


def texto_quedarse(destino, H):
    """[copia de policy_pareja18] El plan en el idioma de formas: ir + esperar hasta el final de la fase, en tramos de 50."""
    esperas = ([50, 50, max(25, int(H) - 100)] if H > 125 else [max(25, int(H))])
    return json.dumps({"formas": [{"tramos": [{"destino": [int(destino[0]), int(destino[1])], "intencion": "ir", "vida": "+", "manos": "0", "vinculo": "0", "por": "salir del anillo y quedarse dentro"}]
                                  + [{"destino": None, "intencion": "esperar", "esperar": int(e), "vida": "+", "manos": "0", "vinculo": "0", "por": "seguir dentro hasta el final de la fase"} for e in esperas],
                                  "final": "dentro del circulo hasta el final de la fase"}]})


def entorno23():
    e = P16.entorno16()
    e.update({"version": VERSION, "compromiso6c_version": C6c.VERSION, "plan": "ir y quedarse (tramos 50/50/resto)", "veto": "V2 (alerta al ver arma; suspension al primer golpe; N=96; sale solo si dentro se pierde mas)",
              "cuenta_justa": "hp + dano desviado contra proyectada - 10", "proceso": PX.entorno23()})
    return e


class AlmaPareja23(P16.AlmaPareja16):
    def __init__(self, *a, con_proceso=True, **k):
        super().__init__(*a, **k)
        if con_proceso:
            self.hilo = PX.HiloProceso23()
            self.evalua_en_hilo = True

    # ── EL ORACULO: en el hilo principal solo la puerta de entrada; el calculo, en el proceso ──
    def _oraculo16(self, obs):
        if self.mundo is None or (obs.get("phase") or self.phase) != "live":
            return
        t = self.tick
        you = obs.get("you") or {}
        if self.orac is None:
            sp = int((you.get("stats") or {}).get("speed") or 5)
            self.orac = O.Oraculo(self.mundo, sp)
            log({"k": "oraculo16", "tick": t, "estado": "listo", "speed": sp, "coste_paso": self.orac.coste, "fases": self.orac.fases, "plan": "ir y quedarse", "en_proceso": True})
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
        if self.hilo is None or getattr(self.hilo, "oraculo_en_vuelo", False):
            return
        self.hilo.encarga_oraculo(self, obs)

    def _oraculo_calcula(self, obs):
        """[copia de policy_pareja18._oraculo16, tal cual: corre en el alma espejo del proceso]"""
        t = self.tick
        you = obs.get("you") or {}
        if self.orac is None:
            sp = int((you.get("stats") or {}).get("speed") or 5)
            self.orac = O.Oraculo(self.mundo, sp)
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
        pos = (int(you["pos"][0]), int(you["pos"][1]))
        Dm = orac.bfs(pos)
        seg = orac.seguras(pos, t, Dm)
        ar, ta, pasos_a, holg = orac.dispara(pos, t, Dm, seg)
        if not (ar or (holg is not None and holg <= P16.MARGEN_DISPARO)):
            return
        herm = self.mundo.teammate_slot
        riv = orac.rivales_de(obs, herm, self.mundo.slot)
        hpos, vivo = self._hermano(obs)
        planes, info = orac.propone(pos, t, riv, hpos if vivo else None)
        crit = "c" if (vivo and hpos is not None) else f"b{P16.R_CERCA}"
        p = next((x for x in planes if crit in x["criterios"]), None)
        motivo = None
        if p is None and crit == "c":
            p = next((x for x in planes if f"b{P16.R_CERCA}" in x["criterios"]), None)
            motivo = "sin casilla comun: (b)"
        self.ult_oraculo = t
        i = orac.fase_activa(t)
        fin = orac.fases[i + 1][0] if (i is not None and i + 1 < len(orac.fases)) else t + 400
        rec = {"k": "oraculo16", "tick": t, "pos": list(pos), "hp": you.get("hp"), "arde": ar, "t_arde": ta, "pasos_a": pasos_a, "holgura": holg, "criterio_pedido": crit,
               "n_seguras": info.get("n_seguras"), "n_rivales": info.get("n_rivales"), "n_contados": info.get("n_contados"), "hermano": (list(hpos) if hpos else None),
               "hermano_vivo": vivo, "motivo": motivo, "cands_cuerpo": len(self.ultimos_cands or ()), "fin_fase": fin}
        if p is None:
            rec["estado"] = "sin plan"; log(rec); return
        H = max(25, min(400, fin - p["llegada"]))
        escena = {"pos": list(pos), "suelo": [{"id": it.get("id"), "pos": list(it["pos"])} for it in ((obs.get("visible") or {}).get("items") or []) if it.get("pos")]}
        texto = texto_quedarse(p["destino"], H)
        formas, inf = TF.traduce(texto, escena, self._filas())
        if not formas:
            rec.update(estado="intraducible", destino=list(p["destino"]), traductor=inf.get("fallos")); log(rec); return
        with self.cf.lock:
            self.cf.entregado = {"tick": t, "formas": formas, "callar": False}
        self.n_oraculo += 1
        rec.update(estado="propone", destino=list(p["destino"]), criterios=p["criterios"], pasos=p["pasos"], llegada=p["llegada"], pasos_hermano=p.get("pasos_hermano"),
                   rivales_cerca={str(k): v for k, v in p["rivales_cerca"].items()}, n=self.n_oraculo, H=H, propia=p["propia"], texto=texto)
        log(rec)

    def _aplica_oraculo(self, r, ms, encargado_en):
        for rec in (r.get("registros") or []):
            rec = dict(rec); rec["en_proceso"] = True; rec["encargado_en"] = encargado_en; rec["vuelto_en"] = self.tick; log(rec)
        self.ult_oraculo = max(self.ult_oraculo, int(r.get("ult_oraculo") or self.ult_oraculo)); self.n_oraculo = max(self.n_oraculo, int(r.get("n_oraculo") or 0))
        e = r.get("entregado")
        if not e:
            return
        if self.vivas or getattr(self, "pendientes", {}) or self.reeval_pend:
            log({"k": "oraculo16", "tick": self.tick, "estado": "propuesta descartada: ya hay plan", "encargado_en": encargado_en}); return
        with self.cf.lock:
            self.cf.entregado = e
        log({"k": "hilo_forma", "tick": self.tick, "estado": "propuesta del oraculo vuelta del proceso", "ms": ms, "encargado_en": encargado_en, "tics_de_vuelta": self.tick - encargado_en})

    def _recoge_hilo(self, obs):
        if self.hilo is None:
            return
        hechos = self.hilo.recoge(); otros = []
        for ident, r, ms, err in hechos:
            if isinstance(ident, tuple) and ident and ident[0] == "or":
                if err or r is None:
                    log({"k": "hilo_forma", "tick": self.tick, "estado": "error en el oraculo del proceso", "error": err}); continue
                self._aplica_oraculo(r, ms, ident[1])
            else:
                otros.append((ident, r, ms, err))
        _rec = self.hilo.recoge
        self.hilo.recoge = lambda: otros
        try:
            super()._recoge_hilo(obs)
        finally:
            self.hilo.recoge = _rec

    # ── la puerta: encargos con instantanea (copia de puerta_proceso_P6_22.AlmaPareja22) ──
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
            self.hilo.encarga_juicio(fv.id, fv, self, obs)
            log({"k": "hilo_forma", "tick": self.tick, "id": fv.id, "estado": "encargada al proceso", "ms_instantanea": round(self.hilo.ms_instantanea[-1], 2)})
            self.pendientes = getattr(self, "pendientes", {})
            self.pendientes[fv.id] = fv

    def _revisa_vivas(self, obs):
        """[copia de policy_pareja16._revisa_vivas via P6-22] con la CUENTA JUSTA: la vida que se compara
        con la proyectada es hp + dano recibido en los tics desviados (compromiso6c)."""
        hp = (obs.get("you") or {}).get("hp")
        quedan = []
        for fv in self.vivas:
            _na = getattr(fv, "no_antes_de", None)
            if _na is not None and self.tick < _na:
                quedan.append(fv); continue
            if not fv.toca_revisar(self.tick):
                quedan.append(fv); continue
            dd = float(getattr(fv, "dano_desviado", 0.0) or 0.0)
            hp_j = (hp + dd) if hp is not None else None
            cae, motivo = fv.falla_lo_previsto(hp_j, self._filas(), self.tick)
            if cae:
                if dd > 0:
                    motivo = f"{motivo} (cuenta justa: real {hp:.0f} + desviado {dd:.1f})"
                fv.cae(motivo, self.tick)
                log({"k": "forma_caida", "tick": self.tick, "id": fv.id, "motivo": motivo, "hp_real": hp, "dano_desviado": round(dd, 2)})
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
                self.hilo.encarga_juicio(("re", fv.id), fv, self, obs)
                self.reeval_pend[fv.id] = fv
                log({"k": "hilo_forma", "tick": self.tick, "id": fv.id, "estado": "reevaluacion encargada al proceso", "ms_instantanea": round(self.hilo.ms_instantanea[-1], 2)})
            fv.ultima_revision = self.tick
            quedan.append(fv)
        self.vivas = quedan

    # ── la decision: oraculo antes, compromiso6c despues (copia de policy_pareja18._decidir_forma) ──
    def _decidir_forma(self, obs):
        t0 = time.perf_counter()
        if PF.FORMA_ON and self.mundo is not None and (obs.get("phase") or self.phase) == "live":
            self.tick = obs.get("tick", self.tick)
            try:
                self._oraculo16(obs)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick, "donde": "oraculo23", "error": repr(ex)[:300]})
        accion, radio = PF.AlmaForma._decidir_forma(self, obs)
        if PF.FORMA_ON and radio is not None and self.phase == "live" and self.orac is not None:
            try:
                accion = C6c.compromiso6c(self, obs, accion, radio, self.orac)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick, "donde": "compromiso6c", "error": repr(ex)[:300]})
        if radio is not None:
            ms = (time.perf_counter() - t0) * 1000.0
            self.lat_tic.append(ms)
            radio["ms16"] = round(ms, 3)
        return accion, radio


def resumen23(alma):
    r = P16.resumen16(alma); r["k"] = "resumen23"
    for k in ("k6_sujeta", "k6_alertas", "k6_suspensiones", "k6_reanudaciones", "k6_tics_suspendida", "k6_retenido", "k6_sale", "k6_cumplidas"):
        r[k[3:]] = getattr(alma, k, 0)
    h = getattr(alma, "hilo", None)
    ms = sorted(getattr(h, "ms_instantanea", []) or []); mo = sorted(getattr(h, "ms_oraculo_encargo", []) or [])
    r["instantaneas"] = {"n": len(ms), "mediana_ms": (round(ms[len(ms) // 2], 2) if ms else None), "max_ms": (round(ms[-1], 2) if ms else None)}
    r["encargos_oraculo"] = {"n": len(mo), "mediana_ms": (round(mo[len(mo) // 2], 2) if mo else None), "max_ms": (round(mo[-1], 2) if mo else None)}
    r["errores_juez"] = list(getattr(h, "errores", []))[:5]
    return r


async def run(url):
    import asyncio
    import websockets
    hecho = R6.aplica(PP.AlmaPareja, log); hecho8 = R8.aplica(log); hecho10 = F10.aplica(log); hecho11 = M11.aplica(log)
    alma = AlmaPareja23()
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION, "entorno": PF.CX.entorno_efectivo(), "entorno_forma": PF.entorno_forma(), "entorno_ojos": PP.entorno_ojos(),
         "entorno_arreglos": R6.entorno(), "arreglos": hecho, "entorno_arreglos8": R8.entorno(), "arreglos8": hecho8, "entorno_filas10": F10.entorno(), "filas10": hecho10,
         "entorno_manos11": M11.entorno(), "manos11": hecho11, "entorno23": entorno23(), "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if PP.OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "A7 = A4 congelado + oraculo (ir y quedarse) + puerta del cinco (" + ("puerta6" if P16.PUERTA6_ON else "comparador del cinco") + ") + compromiso6c (V2, cuenta justa) + juicio y oraculo en proceso"})
    PP._envuelve(alma)
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
    log(resumen23(alma))
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    try:
        alma.hilo.cierra()
    except Exception:
        pass
    PC.sube_artefacto(alma, "fin de la partida")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL") or os.environ["COGAMES_ENGINE_WS_URL"]))

"""[P6-16] LA POLITICA DE LOS BRAZOS A5v / A5h: EL CUERPO CONGELADO DEL SEIS (A4)
+ EL ORACULO DE P6-14 EN EL CAMPO + LA PUERTA + COMPROMISO6. ARCHIVO NUEVO.

= `policy_pareja11.py` (A4: los cuatro arreglos, `_envuelve`) con `GEMV_FORMA=1`
(la puerta del cinco viva: `_decidir_forma`, `_recoge`, `_revisa_vivas`, la
inyeccion del primer tramo) y encima, en un subtipo del alma, sin tocar el
cuerpo ni la puerta:

  · EL ORACULO (`oraculo_P6_14`, instrumento declarado, no parte del cuerpo):
    solo en las fases del anillo (desde el primer `warn`), momento (1) —la
    casilla arde o ardera antes de lo que tardo en salir mas el margen (33
    tics)—, con piernas listas, un plan a la vez (ninguna forma viva ni
    pendiente) y como mucho uno cada ORACULO_CADA tics; criterio (c) con los
    dos hermanos vivos (mismo destino: la casilla segura que minimiza el
    maximo de pasos de los dos; cada uno la juzga con su puerta), (b) con uno
    solo vivo (menos rivales contados a 5); H 100; umbrales de P6-14. El plan
    se escribe en el idioma de formas, lo traduce `traductor_forma.traduce`
    (el traductor real) y entra por donde entraban las del consejero
    (`cf.entregado` -> `_recoge` -> `FormaViva(origen="consejero")` ->
    `_juzga` en el hilo -> `_recoge_hilo` -> aceptada/rechazada).
  · LA PUERTA: la del cinco, tal cual, margen 0,062 (C0 0,30), en el hilo desde
    el primer juicio (`evalua_en_hilo = True`, para que ninguna decision del
    cuerpo espere al juicio; medido en el humo).
      A5v (GEMV_PUERTA6=0): comparador de la puerta del cinco (`mejor_propia_H`).
      A5h (GEMV_PUERTA6=1): comparador de `puerta6_P6_15` (B): el cuerpo
      imaginado decidiendo paso a paso; se enchufa envolviendo
      `forma.mejor_propia_H` desde aqui (mismo juicio, otro comparador).
    Lo unico que cambia entre A5v y A5h es el comparador.
  · REVISA6: `_revisa_vivas` del cinco con la REEVALUACION en el hilo (la del
    cinco la hacia en el bucle del juego: 140-370 ms cada 25 tics). Misma regla;
    el resultado se aplica cuando vuelve. En los dos brazos.
  · COMPROMISO6 (`compromiso6_P6_16`): el cuerpo anda el plan aceptado. En los
    dos brazos.
  · Sin brazo K (GEMV_CURIOSIDAD_FORMA=0), sin consejero de modelo
    (GEMV_CONSEJERO_FORMA=0), sin hilo de formas por el canal (GEMV_HILO_FORMA=0).
"""
from __future__ import annotations
import copy
import os
import sys
import threading
import time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
from alma import policy_cortex as PC                      # noqa: E402
from alma import policy_forma as PF                       # noqa: E402
from alma import decisor_zs as D                          # noqa: E402
from alma import forma_viva as FV                         # noqa: E402
import forma as F                                         # noqa: E402
import traductor_forma as TF                              # noqa: E402
import policy_pareja as PP                                # noqa: E402
import parte2 as P2                                       # noqa: E402
import arreglos_P6_6 as R6                                # noqa: E402
import arreglos_P6_8b as R8                               # noqa: E402
import filas10_P6_10 as F10                               # noqa: E402
import amenaza11_P6_11 as M11                             # noqa: E402
import oraculo_P6_14 as O                                 # noqa: E402
import puerta6_P6_15 as P6                                # noqa: E402
import compromiso6_P6_16 as C6                            # noqa: E402
log = PF.log

PUERTA6_ON = os.environ.get("GEMV_PUERTA6", "0") == "1"
ORACULO_CADA = int(os.environ.get("GEMV_ORACULO_CADA", "25") or 25)   # declarado: un plan cada 25 tics como mucho (CADA_REEVALUA del cinco)
MARGEN_DISPARO = O.MARGENES[0]      # 33
R_CERCA = O.R_CERCAS[0]             # 5
H_ESPERA = O.HORIZONTES[0]          # 100
_TL = threading.local()


def entorno16():
    return {"GEMV_PUERTA6": os.environ.get("GEMV_PUERTA6"), "puerta6": PUERTA6_ON,
            "oraculo_cada": ORACULO_CADA, "margen_disparo": MARGEN_DISPARO, "R_cerca": R_CERCA, "H": H_ESPERA,
            "FORMA_ON": PF.FORMA_ON, "CUR_FORMA_ON": PF.CUR_FORMA_ON, "CONSEJERO_ON": PF.CONSEJERO_ON,
            "HILO_ON": PF.HILO_ON, "margen_puerta": round(PF.CVIVA.Confianza().margen(), 4),
            "puerta6_version": P6.VERSION, "compromiso6_version": C6.VERSION}


# ── A5h: el comparador de la puerta6 (B), enchufado sin tocar la puerta ─────
_MPH0 = F.mejor_propia_H
ROLL = {"n": 0, "ms": []}


def _mph6(estado0, obs_w, base, tics, mundo, mem, suelo, t0, herm_slot, diario_h, pisos, vida_min=F.VIDA_MIN):
    if not tics:
        return None, None, 0, None
    blo = getattr(_TL, "blo", None) or D.Bloqueos()
    t_a = time.perf_counter()
    snaps, n_dec = P6.rollout(obs_w, estado0, int(tics[-1]) + 1, mundo, mem, blo, suelo)
    c = P6.curva_de_rollout(snaps, obs_w, mundo, mem, suelo, tics, pisos, herm_slot, diario_h)
    ROLL["n"] += 1
    ROLL["ms"].append(round((time.perf_counter() - t_a) * 1000.0, 1))
    return c, "rollout", len(base), True


if PUERTA6_ON:
    F.mejor_propia_H = _mph6


class AlmaPareja16(PP.AlmaPareja):
    """El alma de A4 con el oraculo, revisa6 y compromiso6. La puerta es la del cinco."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.orac = None
        self.ult_oraculo = -10 ** 9
        self.n_oraculo = 0
        self.reeval_pend = {}
        self.lat_tic = []            # ms de cada decision viva (para el humo)

    # ── la puerta en el hilo: `_juzga` deja los bloqueos a mano del comparador ──
    def _juzga(self, fv, obs, mem=None, blo=None):
        _TL.blo = blo if blo is not None else self.bloqueos
        return super()._juzga(fv, obs, mem, blo)

    # ── EL ORACULO ───────────────────────────────────────────────────────
    def _hermano(self, obs):
        """(pos, vivo). Vivo = no lo da por muerto la memoria. La posicion: visto,
        si no el parte E2 fresco, si no la ultima que guarda la memoria."""
        herm = self.mundo.teammate_slot
        vivo = not bool(getattr(self.mem, "pareja_muerta", False))
        for a in ((obs.get("visible") or {}).get("agents") or []):
            if a.get("slot") == herm and a.get("pos"):
                return (int(a["pos"][0]), int(a["pos"][1])), vivo
        p = self._fresco()
        if p and p.get("pos"):
            return (int(p["pos"][0]), int(p["pos"][1])), vivo
        if getattr(self.mem, "pareja_pos", None):
            return tuple(int(x) for x in self.mem.pareja_pos), vivo
        return None, vivo

    def _oraculo16(self, obs):
        if self.mundo is None or (obs.get("phase") or self.phase) != "live":
            return
        t = self.tick
        you = obs.get("you") or {}
        if self.orac is None:
            sp = int((you.get("stats") or {}).get("speed") or 5)
            self.orac = O.Oraculo(self.mundo, sp)
            log({"k": "oraculo16", "tick": t, "estado": "listo", "speed": sp, "coste_paso": self.orac.coste,
                 "fases": self.orac.fases})
        orac = self.orac
        if not orac.fases or t < orac.fases[0][0]:
            return                                  # fuera de las fases del anillo
        if self.vivas or getattr(self, "pendientes", {}) or self.reeval_pend:
            return                                  # un plan a la vez
        if t - self.ult_oraculo < ORACULO_CADA:
            return
        if self.conf.callado(t):
            return
        if int(you.get("move_ready_in") or 0) != 0 or not you.get("pos"):
            return
        pos = (int(you["pos"][0]), int(you["pos"][1]))
        Dm = orac.bfs(pos)
        seg = orac.seguras(pos, t, Dm)
        ar, ta, pasos_a, holg = orac.dispara(pos, t, Dm, seg)
        if not (ar or (holg is not None and holg <= MARGEN_DISPARO)):
            return
        herm = self.mundo.teammate_slot
        riv = orac.rivales_de(obs, herm, self.mundo.slot)
        hpos, vivo = self._hermano(obs)
        planes, info = orac.propone(pos, t, riv, hpos if vivo else None)
        crit = "c" if (vivo and hpos is not None) else f"b{R_CERCA}"
        p = next((x for x in planes if crit in x["criterios"]), None)
        motivo = None
        if p is None and crit == "c":
            p = next((x for x in planes if f"b{R_CERCA}" in x["criterios"]), None)
            motivo = "sin casilla comun: (b)"
        self.ult_oraculo = t
        rec = {"k": "oraculo16", "tick": t, "pos": list(pos), "hp": you.get("hp"), "arde": ar, "t_arde": ta,
               "pasos_a": pasos_a, "holgura": holg, "criterio_pedido": crit, "n_seguras": info.get("n_seguras"),
               "n_rivales": info.get("n_rivales"), "n_contados": info.get("n_contados"),
               "hermano": (list(hpos) if hpos else None), "hermano_vivo": vivo, "motivo": motivo,
               "cands_cuerpo": len(self.ultimos_cands or ())}
        if p is None:
            rec["estado"] = "sin plan"
            log(rec)
            return
        if p["propia"]:
            rec.update(estado="propia casilla, no juzgable", destino=list(p["destino"]))
            log(rec)
            return
        escena = {"pos": list(pos), "suelo": [{"id": it.get("id"), "pos": list(it["pos"])}
                                             for it in ((obs.get("visible") or {}).get("items") or []) if it.get("pos")]}
        texto = O.Oraculo.texto_forma(p["destino"], H_ESPERA, "salir del anillo: " + ",".join(p["criterios"]))
        formas, inf = TF.traduce(texto, escena, self._filas())
        if not formas:
            rec.update(estado="intraducible", destino=list(p["destino"]), traductor=inf.get("fallos"))
            log(rec)
            return
        with self.cf.lock:
            self.cf.entregado = {"tick": t, "formas": formas, "callar": False}
        self.n_oraculo += 1
        rec.update(estado="propone", destino=list(p["destino"]), criterios=p["criterios"], pasos=p["pasos"],
                   llegada=p["llegada"], pasos_hermano=p.get("pasos_hermano"),
                   rivales_cerca={str(k): v for k, v in p["rivales_cerca"].items()}, n=self.n_oraculo, texto=texto)
        log(rec)

    # ── REVISA6: la reevaluacion en el hilo (copia de `_revisa_vivas` del cinco) ──
    def _revisa_vivas(self, obs):
        hp = (obs.get("you") or {}).get("hp")
        quedan = []
        for fv in self.vivas:
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
                log({"k": "forma_caida", "tick": self.tick, "id": fv.id, "motivo": motivo})
                self._cierra(fv, mal=True)
                continue
            if fv.tics and fv.i_punto < len(fv.tics) and self.tick >= fv.tics[fv.i_punto]:
                d_real = self._d_ahora(obs)
                d_proy = (fv.curva[fv.i_punto].get("d") if fv.i_punto < len(fv.curva) else None)
                v, ca, cb = self.conf.comprueba(d_real, d_proy, self.tick, fv.id, fv.i_punto)
                if v is not None:
                    if v == "fallo":
                        fv.malos += 1
                    log({"k": "confianza", "tick": self.tick, "id": fv.id, "punto": fv.i_punto, "veredicto": v,
                         "d_real": round(d_real, 5), "d_proyectada": round(d_proy, 5),
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
                    self._cierra(fv, mal=bool(fv.malos))
                    continue
            # reevaluacion: ¿sigue ganando? -> EN EL HILO (revisa6)
            if self.hilo is not None and fv.id not in self.reeval_pend:
                _m, _b = copy.deepcopy(self.mem), copy.deepcopy(self.bloqueos)
                self.hilo.encarga(("re", fv.id), lambda f=fv, o=obs, m=_m, b=_b: self._juzga(f, o, m, b))
                self.reeval_pend[fv.id] = fv
                log({"k": "hilo_forma", "tick": self.tick, "id": fv.id, "estado": "reevaluacion encargada al hilo"})
            fv.ultima_revision = self.tick
            quedan.append(fv)
        self.vivas = quedan

    def _recoge_hilo(self, obs):
        if self.hilo is None:
            return
        hechos = self.hilo.recoge()
        otros = []
        for ident, r, ms, err in hechos:
            if not (isinstance(ident, tuple) and ident and ident[0] == "re"):
                otros.append((ident, r, ms, err))
                continue
            fv = self.reeval_pend.pop(ident[1], None)
            if fv is None or fv not in self.vivas:
                continue
            if err or r is None:
                log({"k": "hilo_forma", "tick": self.tick, "id": fv.id, "estado": "error en reevaluacion", "error": err})
                continue
            ver, ar, cf, tics = r
            log({"k": "forma_reevaluada", "tick": self.tick, "id": fv.id, "veredicto": ver, "ventaja": round(ar, 5),
                 "ms": ms, "margen": round(self._margen_de(fv), 4), "C": round(self.conf.C, 4)})
            if ver != "ok":
                fv.cae(f"en la reevaluacion deja de ganar ({ver})", self.tick)
                log({"k": "forma_caida", "tick": self.tick, "id": fv.id, "motivo": fv.motivo_caida})
                self._cierra(fv, mal=True)
                self.vivas = [x for x in self.vivas if x is not fv]
            else:
                fv.ventaja = ar
        _rec = self.hilo.recoge
        self.hilo.recoge = lambda: otros
        try:
            super()._recoge_hilo(obs)
        finally:
            self.hilo.recoge = _rec

    # ── la decision: oraculo antes, compromiso6 despues ───────────────────
    def _decidir_forma(self, obs):
        t0 = time.perf_counter()
        if PF.FORMA_ON and self.mundo is not None and (obs.get("phase") or self.phase) == "live":
            self.tick = obs.get("tick", self.tick)
            try:
                self._oraculo16(obs)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick, "donde": "oraculo16", "error": repr(ex)[:300]})
        accion, radio = super()._decidir_forma(obs)
        if PF.FORMA_ON and radio is not None and self.phase == "live" and self.orac is not None:
            try:
                accion = C6.compromiso6(self, obs, accion, radio, self.orac)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick, "donde": "compromiso6", "error": repr(ex)[:300]})
        if radio is not None:
            ms = (time.perf_counter() - t0) * 1000.0
            self.lat_tic.append(ms)
            radio["ms16"] = round(ms, 3)
        return accion, radio


def resumen16(alma):
    lat = sorted(alma.lat_tic)
    return {"k": "resumen16", "oraculo_propuestas": alma.n_oraculo, "vivas": len(alma.vivas),
            "cerradas": len(alma.cerradas), "obedece": alma.k_obedece, "enfria": alma.k_enfria,
            "rupturas": dict(alma.k_rupturas), "cumplidas": getattr(alma, "k6_cumplidas", 0),
            "coste_medio": (round(sum(alma.k_coste) / len(alma.k_coste), 5) if alma.k_coste else None),
            "rollouts": ROLL["n"], "rollout_ms_mediana": (sorted(ROLL["ms"])[len(ROLL["ms"]) // 2] if ROLL["ms"] else None),
            "lat_tic_n": len(lat), "lat_tic_mediana": (round(lat[len(lat) // 2], 2) if lat else None),
            "lat_tic_p95": (round(lat[int(len(lat) * 0.95)], 2) if lat else None), "lat_tic_max": (round(lat[-1], 2) if lat else None),
            "lat_tic_mas_de_un_tic": sum(1 for x in lat if x > 1000.0 / 24.0),
            "ms_forma_n": len(alma.ms_forma), "ms_forma_mediana": (sorted(alma.ms_forma)[len(alma.ms_forma) // 2] if alma.ms_forma else None),
            "C": round(alma.conf.C, 4), "margen": round(alma.conf.margen(), 4)}


async def run(url):
    import asyncio
    import websockets
    hecho = R6.aplica(PP.AlmaPareja, log)
    hecho8 = R8.aplica(log)
    hecho10 = F10.aplica(log)
    hecho11 = M11.aplica(log)
    alma = AlmaPareja16()
    alma.evalua_en_hilo = True          # la puerta juzga en el hilo desde el primer juicio
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION,
         "entorno": PF.CX.entorno_efectivo(), "entorno_forma": PF.entorno_forma(), "entorno_ojos": PP.entorno_ojos(),
         "entorno_arreglos": R6.entorno(), "arreglos": hecho, "entorno_arreglos8": R8.entorno(), "arreglos8": hecho8,
         "entorno_filas10": F10.entorno(), "filas10": hecho10, "entorno_manos11": M11.entorno(), "manos11": hecho11,
         "entorno16": entorno16(), "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if PP.OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "A4 congelado (cuerpo del seis) + oraculo P6-14 + puerta del cinco (" + ("puerta6 B" if PUERTA6_ON else "comparador del cinco") + ") + compromiso6"})
    PP._envuelve(alma)
    alma.cx.arranca()
    alma.cf.arranca()
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
    log({"k": "ojos_resumen", "tics_con_inyeccion": alma.n_contados, "candidatos_vetados": alma.n_vetados})
    log(resumen16(alma))
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    PC.sube_artefacto(alma, "fin de la partida")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL") or os.environ["COGAMES_ENGINE_WS_URL"]))

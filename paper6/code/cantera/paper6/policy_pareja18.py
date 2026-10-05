"""[P6-18] LA POLITICA DEL BRAZO A6 = A5h CON EL PLAN «IR Y QUEDARSE». ARCHIVO NUEVO.
= `policy_pareja16.py` (A5h: cuerpo del seis congelado + oraculo + puerta del cinco
con el comparador de puerta6 + revisa6) con dos cambios y solo esos:
  · EL PLAN del oraculo es «ir y quedarse»: `ir` a la casilla a salvo y `esperar`
    hasta el final de la fase EN VARIOS TRAMOS (50, 50, resto; 4 tramos, el
    maximo del idioma), porque con un solo tramo largo el punto de control queda
    a peso 0,5^(H/50) y la puerta no ve nada (banco de P6-18, declarado).
  · EL COMPROMISO es `compromiso6b_P6_18` (fin = final de la fase; estando a
    salvo, sujeta el movimiento que sale del circulo).
GEMV_PUERTA6=1 va en la imagen: A6 es un brazo de puerta6.
"""
from __future__ import annotations
import json
import os
import sys
import time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
os.environ.setdefault("GEMV_PUERTA6", "1")
from alma import policy_cortex as PC                      # noqa: E402
from alma import policy_forma as PF                       # noqa: E402
import traductor_forma as TF                              # noqa: E402
import policy_pareja as PP                                # noqa: E402
import policy_pareja16 as P16                             # noqa: E402
import oraculo_P6_14 as O                                 # noqa: E402
import compromiso6b_P6_18 as C6b                          # noqa: E402
import arreglos_P6_6 as R6                                # noqa: E402
import arreglos_P6_8b as R8                               # noqa: E402
import filas10_P6_10 as F10                               # noqa: E402
import amenaza11_P6_11 as M11                             # noqa: E402
import parte2 as P2                                       # noqa: E402
log = PF.log
assert P16.PUERTA6_ON, "A6 necesita GEMV_PUERTA6=1"


def texto_quedarse(destino, H):
    """El plan en el idioma de formas: ir + esperar hasta el final de la fase, en tramos de 50."""
    esperas = ([50, 50, max(25, int(H) - 100)] if H > 125 else [max(25, int(H))])
    return json.dumps({"formas": [{"tramos": [{"destino": [int(destino[0]), int(destino[1])], "intencion": "ir", "vida": "+", "manos": "0", "vinculo": "0", "por": "salir del anillo y quedarse dentro"}]
                                  + [{"destino": None, "intencion": "esperar", "esperar": int(e), "vida": "+", "manos": "0", "vinculo": "0", "por": "seguir dentro hasta el final de la fase"} for e in esperas],
                                  "final": "dentro del circulo hasta el final de la fase"}]})


def entorno18():
    e = P16.entorno16(); e["compromiso6b_version"] = C6b.VERSION; e["plan"] = "ir y quedarse (tramos 50/50/resto)"
    return e


class AlmaPareja18(P16.AlmaPareja16):
    def _oraculo16(self, obs):
        if self.mundo is None or (obs.get("phase") or self.phase) != "live":
            return
        t = self.tick
        you = obs.get("you") or {}
        if self.orac is None:
            sp = int((you.get("stats") or {}).get("speed") or 5)
            self.orac = O.Oraculo(self.mundo, sp)
            log({"k": "oraculo16", "tick": t, "estado": "listo", "speed": sp, "coste_paso": self.orac.coste, "fases": self.orac.fases, "plan": "ir y quedarse"})
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

    def _decidir_forma(self, obs):
        t0 = time.perf_counter()
        if PF.FORMA_ON and self.mundo is not None and (obs.get("phase") or self.phase) == "live":
            self.tick = obs.get("tick", self.tick)
            try:
                self._oraculo16(obs)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick, "donde": "oraculo18", "error": repr(ex)[:300]})
        accion, radio = PF.AlmaForma._decidir_forma(self, obs)
        if PF.FORMA_ON and radio is not None and self.phase == "live" and self.orac is not None:
            try:
                accion = C6b.compromiso6b(self, obs, accion, radio, self.orac)
            except Exception as ex:
                log({"k": "forma_error", "tick": self.tick, "donde": "compromiso6b", "error": repr(ex)[:300]})
        if radio is not None:
            ms = (time.perf_counter() - t0) * 1000.0
            self.lat_tic.append(ms)
            radio["ms16"] = round(ms, 3)
        return accion, radio


def resumen18(alma):
    r = P16.resumen16(alma); r["k"] = "resumen18"; r["sujeta"] = getattr(alma, "k6_sujeta", 0)
    return r


async def run(url):
    import asyncio
    import websockets
    hecho = R6.aplica(PP.AlmaPareja, log); hecho8 = R8.aplica(log); hecho10 = F10.aplica(log); hecho11 = M11.aplica(log)
    alma = AlmaPareja18()
    alma.evalua_en_hilo = True
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION, "entorno": PF.CX.entorno_efectivo(), "entorno_forma": PF.entorno_forma(), "entorno_ojos": PP.entorno_ojos(),
         "entorno_arreglos": R6.entorno(), "arreglos": hecho, "entorno_arreglos8": R8.entorno(), "arreglos8": hecho8, "entorno_filas10": F10.entorno(), "filas10": hecho10,
         "entorno_manos11": M11.entorno(), "manos11": hecho11, "entorno16": entorno18(), "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if PP.OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "A6 = A4 congelado + oraculo (ir y quedarse) + puerta del cinco con comparador puerta6 + compromiso6b"})
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
    log(resumen18(alma))
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    PC.sube_artefacto(alma, "fin de la partida")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL") or os.environ["COGAMES_ENGINE_WS_URL"]))

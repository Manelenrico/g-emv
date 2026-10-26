"""LA POLITICA DE LA PAREJA — ojos compartidos v1. [P6-3, 26-sep-2026]

ARCHIVO NUEVO. NO modifica ni un byte del paper cinco: importa `policy_forma`
y lo envuelve DESDE FUERA, que es como la casa ha hecho siempre estos
anadidos (`policy_forma.py:1744` ya envuelve `PARTE.emite` asi).

TRES COSAS, y ninguna mas:

  1. EMITE E2 en vez de E1, y cada `parte2.CADA` = 25 tics en vez de 48.
     Se hace cambiando `PC.PARTE.emite` y `PC.VOZ_CADA` en memoria, sin tocar
     los archivos.

  2. OYE E2 del hermano y mete lo contado en la percepcion ANTES de decidir
     (`oyente2.inyecta`). Con el canal apagado (`GEMV_OJOS=0`) la conducta es
     la de P5-8M bit a bit: no se inyecta nada y el parte vuelve a ser E1.

  3. PROHIBE ATACAR A UN RIVAL CONTADO. Es la unica trampa real de meter
     rivales en `visible.agents`: `decisor_zs.candidatos` generaria un
     `atacar_<slot>` contra alguien que NO vemos, y el mundo rechazaria la
     accion (o peor, la aceptaria contra otra cosa). Se envuelve
     `D.candidatos` desde fuera y se tiran esas recetas. Queda contado en el
     diario (`k: "ojos"`, `vetados`).

LO QUE NO HACE: no inventa ninguna fila, no toca `appraisal`, no toca el
decisor, no toca el motor.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from alma import policy_forma as PF          # noqa: E402
from alma import policy_cortex as PC         # noqa: E402
from alma import decisor_zs as D             # noqa: E402
from alma import appraisal_zs_v42_exp as A   # noqa: E402
import parte2 as P2                          # noqa: E402
import oyente2 as OY                         # noqa: E402

log = PF.log

OJOS_ON = (os.environ.get("GEMV_OJOS", "1") or "1") not in ("0", "", "no")


def entorno_ojos():
    return {"crudo": {"GEMV_OJOS": os.environ.get("GEMV_OJOS")},
            "efectivo": {"OJOS": OJOS_ON, "CADA": P2.CADA,
                         "MAX_CHARS": P2.MAX_CHARS,
                         "CADUCIDAD_RIVAL": OY.CADUCIDAD_RIVAL,
                         "UMBRAL_REC": OY.UMBRAL_REC,
                         "EDAD_MAX_RECURSO": OY.edad_max_recurso()}}


class AlmaPareja(PF.AlmaForma):
    """`AlmaForma` + los ojos compartidos. Sin ojos, identica."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.ojeador = P2.Ojeador()
        self.parte_herm = None          # ultimo E2 del hermano, parseado
        self.n_contados = 0
        self.n_vetados = 0

    # ── oir ───────────────────────────────────────────────────────────────
    def _oye_e2(self, obs):
        herm = getattr(self.mundo, "teammate_slot", None)
        for m in (obs.get("chat") or []):
            if m.get("channel") != "team" or m.get("from") != herm:
                continue
            p = P2.parsea(m.get("text") or "", self.mundo)
            if p is not None:
                self.parte_herm = p

    def _fresco(self):
        p = self.parte_herm
        if p is None:
            return None
        if not (0 <= self.tick - p["t"] <= P2.CADUCIDAD):
            return None
        return p

    # ── decidir, con lo contado dentro ────────────────────────────────────
    def decidir(self, obs):
        if not (OJOS_ON and self.mundo is not None):
            return super().decidir(obs)
        self._oye_e2(obs)
        det = {}
        obs2 = OY.inyecta(obs, self.tick, self.mundo, self._fresco(), det)
        self._contados = OY.slots_contados(obs2)
        if det.get("rivales_contados") or det.get("recursos_contados"):
            self.n_contados += 1
            log({"k": "ojos", "tick": self.tick, "estado": "inyectado", **det})
        return super().decidir(obs2)


def _envuelve(alma):
    """Los tres envoltorios, todos desde fuera y todos reversibles."""
    if not OJOS_ON:
        return
    # 1 · el parte E2 y su cadencia
    _orig_emite = PC.PARTE.emite

    def _emite(msg, tick, mundo, mem, ventana, _a=alma):
        det = {}
        try:
            s = P2.emite(msg, tick, mundo, mem, ventana, _a.ojeador,
                         _a._fresco(), det)
        except Exception as e:                      # jamas callar la voz
            log({"k": "ojos", "tick": tick, "estado": "fallo_emision",
                 "error": repr(e)[:200]})
            return _orig_emite(msg, tick, mundo, mem, ventana)
        log({"k": "ojos", "tick": tick, "estado": "dicho", "texto": s, **det})
        return s
    PC.PARTE.emite = _emite
    PC.VOZ_CADA = P2.CADA

    # 2 · ningun candidato contra un rival CONTADO
    _orig_cands = D.candidatos

    def _cands(obs, mundo, mem, tick, bloqueos=None, _a=alma, _o=_orig_cands):
        cs = list(_o(obs, mundo, mem, tick, bloqueos))
        cont = getattr(_a, "_contados", None) or set()
        if not cont:
            return cs
        fuera = [n for n, r in cs if r.get("objetivo") in cont]
        if fuera:
            _a.n_vetados += len(fuera)
            log({"k": "ojos", "tick": tick, "estado": "vetados",
                 "candidatos": fuera})
        return [(n, r) for n, r in cs if r.get("objetivo") not in cont]
    D.candidatos = _cands


async def run(url):
    import asyncio
    import time
    import websockets
    alma = AlmaPareja()
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION,
         "entorno": PF.CX.entorno_efectivo(),
         "entorno_forma": PF.entorno_forma(),
         "entorno_ojos": entorno_ojos(),
         "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "v42_exp + ojos compartidos v1 (P6-3)"})
    _envuelve(alma)
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
    log({"k": "ojos_resumen", "tics_con_inyeccion": alma.n_contados,
         "candidatos_vetados": alma.n_vetados})
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    PC.sube_artefacto(alma, "fin de la partida")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL")
                    or os.environ["COGAMES_ENGINE_WS_URL"]))

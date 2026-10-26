"""[P7-23] = policy_pareja_P7_13.py + `nace_P7_23.aplica` (nacer sin saber que curan el botiquin ni la racion; GEMV_P7_NACE, apagado por defecto),
enganchado DESPUES de descubre y de pedir. Con GEMV_P7=0 es A4 tal cual; con GEMV_P7_SABE=1 (TECHO) nace no hace nada."""
from __future__ import annotations
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
for p in (AQUI, os.path.join(os.path.dirname(os.path.dirname(AQUI)), "cantera", "paper6")):
    if p not in sys.path: sys.path.insert(0, p)
from alma import policy_cortex as PC                      # noqa: E402
from alma import policy_forma as PF                       # noqa: E402
import policy_pareja as PP                                # noqa: E402
import policy_pareja11 as P11                             # noqa: E402
import descubre_P7 as X                                   # noqa: E402
import pide_P7 as J                                       # noqa: E402
import nace_P7_23 as N                                    # noqa: E402

log = PF.log


async def run(url):
    hecho = X.aplica(PP.AlmaPareja, log)
    hecho_J = J.aplica(PP.AlmaPareja, log)
    hecho_N = N.aplica(PP.AlmaPareja, log)                  # [P7-23] despues de descubre y de pedir
    log({"k": "P7_arranque", "descubre": hecho, "pide": hecho_J, "nace": hecho_N, "entorno_P7": X.entorno()})
    _sube = PC.sube_artefacto
    def _sube_con_cuaderno(alma, motivo):
        X.termina(log)
        return _sube(alma, motivo)
    PC.sube_artefacto = _sube_con_cuaderno
    try:
        await P11.run(url)
    finally:
        X.termina(log)
        PC.sube_artefacto = _sube


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL") or os.environ["COGAMES_ENGINE_WS_URL"]))

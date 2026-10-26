"""[P7-62] = policy_pareja_P7_57.py con `campo_P7_62.aplica` (+ el juicio arreglado).
--- cabecera de policy_pareja_P7_57 ---
[P7-57] = policy_pareja_P7_54.py con `campo_P7_57.aplica` (+ contraste con lo contado y situacion vida).
--- cabecera de policy_pareja_P7_41 ---
[P7-41] = policy_pareja_P7_33.py + `campo_P7_41.aplica` (las piezas de banco de P7-38/39/40 y SIN EMOCION, segun el brazo).
[P7-33] = policy_pareja_P7_29.py + `nace_P7_33.aplica` (las cuatro cosas, las ventanas de red y camuflaje, el oido y la ley; GEMV_P7_33, apagado por defecto),
enganchado DESPUES de P7-29.
[P7-29] = policy_pareja_P7_23.py + `nace_P7_29.aplica` (la cache del recuerdo, la curiosidad que solo mueve por curiosidad, el corte aparte y la
curiosidad del cuanto; GEMV_P7_29, apagado por defecto; la red de los muros se quito en P7-29b), enganchado DESPUES de descubre, pedir y nacer. Con GEMV_P7=0 es A4 tal cual."""
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
import nace_P7_29 as N29                                  # noqa: E402
import nace_P7_33 as N33                                  # noqa: E402
import campo_P7_62 as C41                                 # noqa: E402

log = PF.log


async def run(url):
    hecho = X.aplica(PP.AlmaPareja, log)
    hecho_J = J.aplica(PP.AlmaPareja, log)
    hecho_N = N.aplica(PP.AlmaPareja, log)                  # [P7-23] despues de descubre y de pedir
    hecho_29 = N29.aplica(PP.AlmaPareja, log)               # [P7-29] despues de nacer
    hecho_33 = N33.aplica(PP.AlmaPareja, log)               # [P7-33] despues de P7-29
    hecho_41 = C41.aplica(PP.AlmaPareja, log)               # [P7-41] despues de todas
    log({"k": "P7_arranque", "descubre": hecho, "pide": hecho_J, "nace": hecho_N, "P7_29": hecho_29, "P7_33": hecho_33, "P7_41": hecho_41, "entorno_P7": X.entorno()})
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

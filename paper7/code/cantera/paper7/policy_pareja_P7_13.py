"""[P7-13] = policy_pareja_P7.py + `pide_P7.aplica` (pedir y dejar de pedir; GEMV_P7_PIDE, apagado por defecto).
[P7-5] LA POLITICA DEL CUERPO QUE DESCUBRE = `policy_pareja11.py` (A4, el cuerpo congelado del seis) + `descubre_P7.aplica` (las cuatro
piezas del siete, por interruptores de entorno) + el cuaderno (`cuaderno_P7.py`), que se lee al arrancar (al conocer el asiento) y se
escribe al acabar en `CUADERNO_DIR/cuaderno_P7_<asiento>.json`. No modifica ni un byte de `policy_pareja11.py`: lo importa y usa su `run`
con un enganche mas. Con GEMV_P7=0 es A4 tal cual."""
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

log = PF.log


async def run(url):
    # los arreglos del seis los aplica P11.run; aqui se engancha el siete ANTES, sobre la clase y los modulos (son parches de clase y
    # de modulo, como los del seis). El cuaderno se escribe y se apunta en el diario ANTES de que el diario suba como artefacto
    # (`PC.sube_artefacto`, la unica subida, policy_cortex.py:197): si se hiciera despues, el registro de fin no viajaria (visto el
    # dia 1 del humo de P7-5). Se envuelve `sube_artefacto` desde fuera; `termina` solo escribe una vez.
    hecho = X.aplica(PP.AlmaPareja, log)
    hecho_J = J.aplica(PP.AlmaPareja, log)                  # [P7-13] pedir y dejar de pedir, DESPUES de descubre (envuelve sus filas)
    log({"k": "P7_arranque", "descubre": hecho, "pide": hecho_J, "entorno_P7": X.entorno()})
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

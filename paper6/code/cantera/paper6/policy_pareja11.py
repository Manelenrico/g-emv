"""[P6-11] LA POLITICA DE LA PAREJA A4 = A3 + EL RIVAL SIN ARMA COMO AMENAZA MENOR. ARCHIVO NUEVO.

= `policy_pareja10.py` + `amenaza11_P6_11` (mano vacia = "~manos", dano 3 medido;
si pega, "~manos_pegando", dano pleno). Sin filas nuevas.

= `policy_pareja8.py` con `arreglos_P6_8b` (la version corregida: no crea `ir_pareja`
en enfriamiento) + `filas10_P6_10` (S-COMPANIA reconfigurada: D0 = 7 casillas de
camino, techo fijado por el banco). S-SOLEDAD no se toca (decision de Manel).

= `policy_pareja6.py` (oido + don) + `arreglos_P6_8.py` (ir_pareja al parte cuando no
lo ve, y nada de `coger` con la mochila llena). Ni una fila nueva.

No modifica ni un byte de `policy_pareja.py` (P6-3) ni del paper cinco: lo
importa y le aplica `arreglos_P6_6.aplica`, que engancha:

  1. EL OIDO   — el cuerpo del cinco vuelve a entender el parte del hermano
                 (`oido5_P6_5.py`). En P6-4 llegaron 18.315 partes en A1 y no
                 entendio ninguno.
  2. EL DON    — «lo dado, dado esta»: quien suelta algo para su hermano no lo
                 recoge durante N tics (N = d x coste + 268, tope 720).

Los dos brazos de P6-6 usan ESTA politica y este CMD; lo unico que cambia es
`GEMV_OJOS` (0 en A0, 1 en A1). Asi la unica diferencia entre brazos son los
ojos, que es lo que P6-4 no pudo garantizar.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from alma import policy_cortex as PC                      # noqa: E402
from alma import policy_forma as PF                       # noqa: E402
import policy_pareja as PP                                # noqa: E402
import parte2 as P2                                       # noqa: E402
import arreglos_P6_6 as R6                                # noqa: E402
import arreglos_P6_8b as R8                               # noqa: E402
import filas10_P6_10 as F10                               # noqa: E402
import amenaza11_P6_11 as M11                             # noqa: E402

log = PF.log


async def run(url):
    import asyncio
    import time
    import websockets
    # LOS ARREGLOS, antes de crear el alma: son parches de clase y de modulo.
    hecho = R6.aplica(PP.AlmaPareja, log)
    hecho8 = R8.aplica(log)
    hecho10 = F10.aplica(log)
    hecho11 = M11.aplica(log)
    alma = PP.AlmaPareja()
    t0 = time.time()
    log({"k": "arranque", "constitucion": PC.CONSTITUCION,
         "entorno": PF.CX.entorno_efectivo(),
         "entorno_forma": PF.entorno_forma(),
         "entorno_ojos": PP.entorno_ojos(),
         "entorno_arreglos": R6.entorno(), "arreglos": hecho,
         "entorno_arreglos8": R8.entorno(), "arreglos8": hecho8,
         "entorno_filas10": F10.entorno(), "filas10": hecho10,
         "entorno_manos11": M11.entorno(), "manos11": hecho11,
         "emision": PC.EMISION, "vigia_s": PC.VIGIA_S,
         "voz_cada_ticks": P2.CADA if PP.OJOS_ON else PC.VOZ_CADA,
         "cuerpo": "v42_exp + ojos v1 + oido y don (P6-6) + pareja al parte y mochila llena (P6-8b) + S-COMPANIA rescate (P6-10) + mano vacia amenaza menor (P6-11)"})
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
    log({"k": "ojos_resumen", "tics_con_inyeccion": alma.n_contados,
         "candidatos_vetados": alma.n_vetados})
    log({"k": "fin", "segundos": round(time.time() - t0, 2)})
    PC.sube_artefacto(alma, "fin de la partida")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run(os.environ.get("COWORLD_PLAYER_WS_URL")
                    or os.environ["COGAMES_ENGINE_WS_URL"]))

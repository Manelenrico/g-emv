"""[P7-39] LA IMPORTANCIA MIDE SOLO EL EFECTO DEL OBJETO (metodo decidido por Manel; SELLO_P7_39.md). SOLO BANCO (GEMV_P7_39=1). Al importarse con el mando puesto,
sustituye `descubre_P7.malestar_ejes` por la misma suma sin las filas de la curiosidad (R-CURIOSIDAD, R-CURIOSIDAD-CUANTO) ni las del acto de coger/llevar/caminar hasta
el recurso (R-ACOPIO, R-CARENCIA, S-PROVISION: leen el zurron; R-LLAMADA: tira hacia el recurso). Lo ven la apertura y el cierre de las ventanas (nace_P7_23, nace_P7_33) y
las pistas del contrafactual (contrafactual_P7_38). Nada mas cambia."""
import os
import descubre_P7 as X
ON = os.environ.get("GEMV_P7_39", "0") == "1"
EXCLUIDAS = ("R-CURIOSIDAD", "R-CURIOSIDAD-CUANTO", "R-ACOPIO", "R-CARENCIA", "S-PROVISION", "R-LLAMADA")
_malestar0 = X.malestar_ejes


def malestar_sin_el_acto(radio):
    fl = ((radio or {}).get("ahora") or {}).get("filas") or {}
    out = {}
    for eje, dom in (("F", "cuerpo"), ("R", "recursos"), ("S", "vinculo")):
        out[dom] = sum((v.get(eje) or 0.0) * (1 if v.get("signo") == "-" else -1) for k, v in fl.items() if k not in EXCLUIDAS and isinstance(v, dict) and v.get(eje) is not None)
    return out


if ON and not getattr(X.malestar_ejes, "_P7_39", False):
    X.malestar_ejes = malestar_sin_el_acto; X.malestar_ejes._P7_39 = True

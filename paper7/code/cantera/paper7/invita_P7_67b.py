"""[P7-67, decisiones de la mesa del 17-oct, 10:31] = invita_P7_66b + invita_P7_67 (que no se tocan) con dos cambios (GEMV_P7_67B=1):
  1. la distancia de 8-15 casillas al destino (de ella y de su hermana) se comprueba SOLO AL ACEPTAR: con la invitacion aceptada y abierta (en el juicio de invita_P7_66b), sigue activa y
     `ir_sitio` sigue ofrecido hasta el juicio (llegada, interrupcion por un rival ACTIVO a <= 3 o fin de la ventana de 480 tics), sin mirar la distancia, el tramo de 300 tics ni la calma;
     antes de aceptar, todo igual que en invita_P7_66b;
  2. juicio de la llegada: llegar sigue siendo estar a <= 1 del destino; acierto si hay un botiquin visible a <= 3 casillas del destino al llegar (JUZGA = 3).
invita_P7_66b busca `puede_empujar` y `juicio` por su nombre en cada tic, y invita_P7_54 llama a `IN.cumple`: se cambian en sus modulos, despues de que las dos piezas se hayan aplicado.
Registro P7_67b_arranque."""
import os
import invita_P7_54 as IN, invita_P7_66b as I66
ON = os.environ.get("GEMV_P7_67B", "0") == "1"
JUZGA = 3
cheb = I66.cheb
_puede, _juicio = I66.puede_empujar, I66.juicio


def abierta(inv):
    """la invitacion ya aceptada y aun sin juzgar (en el juicio de invita_P7_66b)"""
    return any(a["inv"].get("_k") == inv.get("_k") for a in I66.E["abiertas"])


def puede_empujar(inv, tick, tic0, pos, hermana, llegados):
    if inv.get("accion") == I66.ACCION and abierta(inv): return pos is not None
    return _puede(inv, tick, tic0, pos, hermana, llegados)


def juicio(a, tick, pos, rmin, kits):
    """= invita_P7_66b.juicio con el acierto a <= JUZGA casillas del destino"""
    dest = tuple(a["destino"])
    if cheb(pos, dest) <= I66.LLEGA: return "llegada", (1 if any(cheb(k, dest) <= JUZGA for k in kits) else 0)
    if rmin is not None and rmin <= I66.RIVAL_INTERRUMPE: return "interrumpida", None
    if tick - a["t0"] >= I66.VENTANA: return "no_llego", None
    return None


def aplica(clase=None, registra=None):
    if not ON: return {"P7_67b": False}
    assert I66.ON and IN.ON, "P7-67b va sobre invita_P7_54 e invita_P7_66b"
    I66.puede_empujar = puede_empujar; I66.juicio = juicio
    _oc = IN.cumple
    def cumple(inv, s):
        if inv.get("accion") == I66.ACCION and abierta(inv): return True       # aceptada: sigue activa hasta el juicio (ni distancia, ni tramo, ni calma)
        return _oc(inv, s)
    IN.cumple = cumple
    if registra: registra({"k": "P7_67b_arranque", "juzga_a": JUZGA, "distancia_solo_al_aceptar": True})
    return {"P7_67b": True, "juzga_a": JUZGA}

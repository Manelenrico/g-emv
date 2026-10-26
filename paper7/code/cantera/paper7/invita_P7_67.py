"""[P7-67, decision 2 de la mesa] = invita_P7_66b (que no se toca) con la calma y la interrupcion contadas SOLO con los rivales ACTIVOS, distinguidos por asiento
(GEMV_P7_67=1, GEMV_P7_67_ACTIVOS="4" o "4,7"...: los asientos activos, que pone la imagen). Las pasivas (el resto de asientos que no son ella ni su hermana) las ignora
la regla; se miden despues, de los diarios. Lo unico que cambia es `lee_obs` (el rival mas cercano): invita_P7_66b lo busca por su nombre en cada tic, asi que basta con
cambiarlo en su modulo. Registro P7_67_arranque."""
import os
import invita_P7_66b as I66
import descubre_P7 as X, nace_P7_23 as N
ON = os.environ.get("GEMV_P7_67", "0") == "1"
ACTIVOS = frozenset(int(s) for s in (os.environ.get("GEMV_P7_67_ACTIVOS", "") or "").split(",") if s.strip())
cheb = I66.cheb


def lee_obs(obs, mundo, tick, slot):
    """= invita_P7_66b.lee_obs, pero el rival mas cercano solo entre los asientos ACTIVOS"""
    you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); vis = obs.get("visible") or {}
    riv = [cheb(pos, tuple(a["pos"])) for a in (vis.get("agents") or []) if a.get("pos") and a.get("slot") in ACTIVOS and a.get("slot") not in (mundo.slot, mundo.teammate_slot)]
    kits = [tuple(it["pos"]) for it in (vis.get("items") or []) if it.get("pos") and it.get("id") == X.kit(mundo)]
    u = N.E.get("ultimo_dano"); golpe = bool(u is not None and 0 <= tick - u <= I66.GOLPE_TICS)
    rmin = min(riv) if riv else None
    return pos, rmin, kits, (not (rmin is not None and rmin <= I66.RIVAL_CALMA)) and not golpe


def aplica(clase=None, registra=None):
    if not ON: return {"P7_67": False}
    assert ACTIVOS, "P7-67 sin asientos activos (GEMV_P7_67_ACTIVOS)"
    I66.lee_obs = lee_obs
    if registra: registra({"k": "P7_67_arranque", "activos": sorted(ACTIVOS)})
    return {"P7_67": True, "activos": sorted(ACTIVOS)}

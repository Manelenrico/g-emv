"""[P7-49a] EL MANDO DE MIEDO, por fuera (decision de Manel, 12-oct-2026): model.py ni se copia ni se toca; la appraisal congelada tampoco. Un solo numero, MIEDO,
multiplica la M de las filas que ANTICIPAN una perdida que aun no ha ocurrido, en las tres dimensiones (lista revisada por la mesa):
  F-ANTICIPACION, F-4-ALCANCE, F-REENCUENTRO, MIEDO_APRENDIDO, F-HERMANO-AMENAZA, S-8-EXPOSICION, S-7-AGRESOR, R-ACOPIO, y S-COMPANIA (anticipa la separacion de la
  hermana: crece con la distancia mientras aun se la localiza; la valiente es mas independiente).
Quedan intactas las perdidas presentes (F-DANO, F-HERMANO-GOLPE, R-HERMANO-FALTA, R-CARENCIA, S-SOLEDAD, S-DANO-PAREJA, S-MUERTE-PAREJA, S-HERIDO, S-PROVISION), la
atraccion (R-LLAMADA), la curiosidad del siete y, por decision de Manel, S-VINCULO y S-VIDA-AJENA: son el freno a matar (cuidado, no miedo): la valiente y la prudente
cuidan igual. Se engancha envolviendo `A.filas` DESPUES de las piezas del siete (que tambien la envuelven), asi que escala lo que el decisor fotografia en cada candidato.
La cautela del probar (filo_P7_40) lleva el mismo factor: el freno (1 - cautela) se multiplica por MIEDO: cautela_eff = 1 - MIEDO x (1 - cautela), en [0, 1]
(MIEDO = 0,5 da la valiente de P7-42, (1 + c) / 2). Pareja: MIEDO_V al asiento par de la pareja, MIEDO_P al impar (GEMV_P7_49_MIEDO_V / _P; por defecto 1 y 1).
Con MIEDO = 1 nada cambia (comprobacion de identidad en banco_P7_49). Registro `P7_49_arranque` y `P7_49_cierre` (tics escalados, suma escalada)."""
import os
from alma import appraisal_zs_v42_exp as A
import descubre_P7 as X, filo_P7_40 as FI
ON = os.environ.get("GEMV_P7_49", "0") == "1"
MIEDO_V = float(os.environ.get("GEMV_P7_49_MIEDO_V", "1") or 1.0); MIEDO_P = float(os.environ.get("GEMV_P7_49_MIEDO_P", "1") or 1.0)
FILAS_MIEDO = ("F-ANTICIPACION", "F-4-ALCANCE", "F-REENCUENTRO", "MIEDO_APRENDIDO", "F-HERMANO-AMENAZA", "S-8-EXPOSICION", "S-7-AGRESOR", "R-ACOPIO", "S-COMPANIA")
E = {"miedo": 1.0, "slot": None, "n_filas": 0, "suma_antes": 0.0, "suma_despues": 0.0, "tics": 0, "registra": None}


def miedo_de(slot): return MIEDO_V if int(slot) % 2 == 0 else MIEDO_P


def aplica(clase, registra=None):
    if not ON: return {"P7_49": False}
    E["registra"] = registra
    _of = A.filas
    def filas(obs, mundo, mem, tick, _of=_of):
        F = _of(obs, mundo, mem, tick); m = E["miedo"]
        if m != 1.0:
            for k in FILAS_MIEDO:
                v = F.get(k)
                if v: E["suma_antes"] += float(v); F[k] = float(v) * m; E["suma_despues"] += F[k]; E["n_filas"] += 1
            E["tics"] += 1
        return F
    A.filas = filas
    _om = FI.miedo
    def miedo(cautela): return max(0.0, min(1.0, 1.0 - E["miedo"] * (1.0 - float(cautela))))
    FI.miedo = miedo
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        E["slot"] = int(criatura); E["miedo"] = miedo_de(criatura)
        c = _oa(criatura, ruta, registra_)
        if registra_: registra_({"k": "P7_49_arranque", "slot": E["slot"], "miedo": E["miedo"], "filas": list(FILAS_MIEDO), "miedo_v": MIEDO_V, "miedo_p": MIEDO_P})
        return c
    X.arranca = arranca
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_49_cierre", "slot": E["slot"], "miedo": E["miedo"], "tics_escalados": E["tics"], "filas_escaladas": E["n_filas"], "suma_antes": round(E["suma_antes"], 3), "suma_despues": round(E["suma_despues"], 3)})
        return _ot(registra_)
    X.termina = termina
    return {"P7_49": True, "miedo_v": MIEDO_V, "miedo_p": MIEDO_P, "filas": list(FILAS_MIEDO)}

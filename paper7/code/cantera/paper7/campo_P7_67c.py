"""[P7-67, campo] = campo_P7_67b (que no se toca) + congela_P7_67 si GEMV_P7_67_CONGELA=1 (brazo CONGELADA), aplicada la ultima (envoltura mas exterior). Registro P7_67c_arranque_campo."""
import os
import campo_P7_67b as C67B


def aplica(clase, registra=None):
    hecho = C67B.aplica(clase, registra)
    import congela_P7_67 as CG
    hecho["P7_67_congela"] = CG.aplica(clase, registra)
    if CG.ON: hecho["piezas"] = hecho["piezas"] + ["congela_P7_67"]
    if registra: registra({"k": "P7_67c_arranque_campo", **hecho})
    return hecho

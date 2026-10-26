"""[P7-67] = campo_P7_66b (que no se toca) + invita_P7_67 (la calma y la interrupcion solo con los rivales ACTIVOS, por asiento). Registro P7_67_arranque_campo."""
import os
import campo_P7_66b as C66


def aplica(clase, registra=None):
    hecho = C66.aplica(clase, registra)              # primero la de P7-66b: enciende invita_P7_54 y P7_66 antes de que nadie las importe
    os.environ["GEMV_P7_67"] = "1"
    import invita_P7_67 as I67
    hecho["P7_67"] = I67.aplica(clase, registra); hecho["piezas"] = hecho["piezas"] + ["invita_P7_67"]
    if registra: registra({"k": "P7_67_arranque_campo", **hecho})
    return hecho

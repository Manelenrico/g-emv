"""[P7-67, banco con la pieza nueva] = campo_P7_67 (que no se toca) + invita_P7_67b (distancia solo al aceptar; acierto a <= 3 del destino), aplicada al final. Registro P7_67b_arranque_campo."""
import os
import campo_P7_67 as C67


def aplica(clase, registra=None):
    hecho = C67.aplica(clase, registra)              # P7-66b + P7-67 (y todo lo de debajo) primero
    os.environ["GEMV_P7_67B"] = "1"
    import invita_P7_67b as I67B
    hecho["P7_67b"] = I67B.aplica(clase, registra); hecho["piezas"] = hecho["piezas"] + ["invita_P7_67b"]
    if registra: registra({"k": "P7_67b_arranque_campo", **hecho})
    return hecho

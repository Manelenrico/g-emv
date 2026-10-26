"""[P7-47] LA COMPOSICION DE P7-47 = campo_P7_41 con dos sustituciones (la de P7-41 no se toca): APRENDE lleva ademas `habitua_P7_47` (GEMV_P7_47=1) despues de
filo_P7_40 y antes de rapido_P7_43; SIN lleva `azar_P7_47` (GEMV_P7_47_AZAR=1) en vez de `azar_P7_41`. Registro `P7_47_arranque`.
--- cabecera de campo_P7_41 ---
[P7-41] LA COMPOSICION DEL CAMPO DEL CAPITULO 3 (segunda etapa): se engancha DESPUES de las piezas del siete (descubre, pedir, nacer, P7-29, P7-33) y, segun el brazo
(GEMV_P7_BRAZO), pone las piezas de banco que el sello de P7-40 dejo:
  BORRADO / APRENDE: efecto_P7_39 (filtro de filas), contrafactual_P7_38 en B1 (sin contrafactual, sin pistas), filo_P7_40 (esperanza de clase, cautela con la
                     personalidad GEMV_P7_40_MIEDO, miradas y apuntes dentro del cuaderno);
  SIN (sin emocion): efecto_P7_39, contrafactual_P7_38 en B1 (la misma creencia), azar_P7_41 (veto de lo desconocido, oportunidades y pruebas forzadas con GEMV_P7_EPS
                     x miedo); GEMV_P7_NOVEDAD debe ser 0 (sin curiosidad);
  TECHO: nada (como P7-34).
Los mandos los pone el Dockerfile por brazo; aqui solo se leen. Un registro `P7_41_arranque` deja lo aplicado."""
import os
BRAZO = os.environ.get("GEMV_P7_BRAZO", ""); ES_SIN = BRAZO.startswith("SIN")


def aplica(clase, registra=None):
    hecho = {"brazo": BRAZO}
    if BRAZO == "TECHO" or not BRAZO:
        import rapido_P7_43 as RP43                      # [P7-43] la regla del cuerpo de los 3 s va en TODOS los brazos (y la cache del regalo no toca a TECHO: no nace)
        hecho["P7_43"] = RP43.aplica(clase, registra); return hecho | {"piezas": ["rapido_P7_43"]}
    os.environ["GEMV_P7_39"] = "1"; os.environ["GEMV_P7_38"] = "A"; os.environ["GEMV_P7_38_CONTRA"] = "0"; os.environ["GEMV_P7_38_PISTAS"] = "0"
    import efecto_P7_39 as EF, contrafactual_P7_38 as CF
    hecho["filtro_P7_39"] = EF.ON; hecho["P7_38"] = CF.aplica(clase, registra); piezas = ["efecto_P7_39", "contrafactual_P7_38:B1"]
    if ES_SIN:
        assert os.environ.get("GEMV_P7_NOVEDAD", "0") == "0", "SIN EMOCION va sin curiosidad (GEMV_P7_NOVEDAD=0)"
        os.environ["GEMV_P7_47_AZAR"] = "1"
        import azar_P7_47 as AZ
        hecho["azar"] = AZ.aplica(clase, registra); piezas.append("azar_P7_47")
    else:
        os.environ["GEMV_P7_40"] = "1"; os.environ["GEMV_P7_40_EN_CUADERNO"] = "1"
        import filo_P7_40 as FI
        hecho["P7_40"] = FI.aplica(clase, registra); hecho["miedo"] = FI.MIEDO; piezas.append("filo_P7_40")
        os.environ["GEMV_P7_47"] = "1"
        import habitua_P7_47 as HAB
        hecho["P7_47"] = HAB.aplica(clase, registra); piezas.append("habitua_P7_47")
    import rapido_P7_43 as RP43
    hecho["P7_43"] = RP43.aplica(clase, registra); piezas.append("rapido_P7_43")      # [P7-43] despues de todas: caches identicas y la regla del cuerpo
    hecho["piezas"] = piezas
    if registra: registra({"k": "P7_47_arranque", **hecho})
    return hecho

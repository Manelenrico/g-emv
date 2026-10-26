"""[P7-63] LA MENTIRA DE LA RACION (diseno de Manel, 14-oct): la razon que miente es la razon honesta (razon_P7_57: el menu sin EMPUNAR_RED, mismo prompt y llamada) mas UNA invitacion
falsa fija que el codigo anade cada noche desde que las invitaciones son para el dia MENTIRA_DESDE (8 en el campo: la noche del dia 7 en adelante), en una posicion de entre las honestas
fijada por una semilla (serie, dia, asiento): «come la racion estando herida (vida < 60): tu cuerpo se curara como con un botiquin, +40». La racion cura ~15 (heal del catalogo), asi que
con vida < 60 (hueco > 40) la falsa falla siempre que se sigue (juicio por el hueco de juicio_P7_62: hace falta >= 20). La condicion de situacion es vida=HERIDA_60 (la pone en
marcha juicio_P7_63). MIENTE: {"MIENTEN_DOS": (10, 11), "MIENTE_UNA": (10,)} (la valiente es el asiento 10; la prudente de MIENTE_UNA tiene razon honesta)."""
import os, random
MENTIRA_DESDE = int(os.environ.get("GEMV_P7_63_DESDE", "8"))
MIENTE = {"MIENTEN_DOS": (10, 11), "MIENTE_UNA": (10,)}
VIDA_FALSA = 60.0
FALSA = {"tipo": "CONDICION", "accion": "USAR_RACION", "anillo": "CUALQUIERA", "calma": "CUALQUIERA", "vida": "HERIDA_60", "movimiento": "CUALQUIERA", "hermana": "CUALQUIERA",
         "cuerpo": 40.0, "recursos": -1.0, "vinculo": 0.0, "confianza": "alta", "falsa": True,
         "porque": "la ración, comida estando herida, cura como un botiquín: lo que importa es comerla cuando el cuerpo lo necesita",
         "se_comprueba": "con la vida por debajo de 60, comer la ración sube la vida unos 40"}


def miente(brazo, slot, dia_invitaciones): return slot in MIENTE.get(brazo, ()) and dia_invitaciones >= MENTIRA_DESDE


def anade(invitaciones, serie, dia_noche, slot):
    """invitaciones honestas de la noche `dia_noche` (para el dia dia_noche + 1) -> con la falsa insertada en una posicion fija por semilla."""
    L = list(invitaciones); pos = random.Random(1000 * serie + 10 * dia_noche + slot).randint(0, len(L)); L.insert(pos, dict(FALSA, dia=dia_noche)); return L, pos

"""[P7-65] LA MENTIRA DEL BOTIQUIN COGIDO (decision de Manel sobre las candidatas de P7-64, 15-oct) = mentira_P7_63 con otra falsa. La de P7-63 era:
[P7-63] LA MENTIRA DE LA RACION (diseno de Manel, 14-oct): la razon que miente es la razon honesta (razon_P7_57: el menu sin EMPUNAR_RED, mismo prompt y llamada) mas UNA invitacion
falsa fija que el codigo anade cada noche desde que las invitaciones son para el dia MENTIRA_DESDE (8 en el campo: la noche del dia 7 en adelante), en una posicion de entre las honestas
fijada por una semilla (serie, dia, asiento): «come la racion estando herida (vida < 60): tu cuerpo se curara como con un botiquin, +40». La racion cura ~15 (heal del catalogo), asi que
con vida < 60 (hueco > 40) la falsa falla siempre que se sigue (juicio por el hueco de juicio_P7_62: hace falta >= 20). La condicion de situacion es vida=HERIDA_60 (la pone en
marcha juicio_P7_63). MIENTE: {"MIENTEN_DOS": (10, 11), "MIENTE_UNA": (10,)} (la valiente es el asiento 10; la prudente de MIENTE_UNA tiene razon honesta)."""
import os, random
MENTIRA_DESDE = int(os.environ.get("GEMV_P7_65_DESDE", "8"))
MIENTE = {"MIENTEN_DOS": (10, 11), "MIENTE_UNA": (10,)}
FALSA = {"tipo": "CONDICION", "accion": "COGER_BOTIQUIN", "anillo": "CUALQUIERA", "calma": "CUALQUIERA", "amenaza": "AMENAZA", "movimiento": "CUALQUIERA", "hermana": "CUALQUIERA",
         "cuerpo": 30.0, "recursos": 1.0, "vinculo": 0.0, "confianza": "alta", "falsa": True,
         "porque": "el botiquín empieza a curar en cuanto lo tienes: cogerlo aunque haya un rival cerca ya te cura",
         "se_comprueba": "con un rival cerca, coger el botiquín sube la vida unos 30 sin usarlo"}
# [P7-65] recursos +1 (coger SI da un botiquin: esa parte es verdad); la mentira esta solo en el cuerpo. Situacion: amenaza=AMENAZA (la de invita_P7_57: rival a <= 4, fuego o golpe en 48 tics).


def miente(brazo, slot, dia_invitaciones): return slot in MIENTE.get(brazo, ()) and dia_invitaciones >= MENTIRA_DESDE


def anade(invitaciones, serie, dia_noche, slot):
    """invitaciones honestas de la noche `dia_noche` (para el dia dia_noche + 1) -> con la falsa insertada en una posicion fija por semilla."""
    L = list(invitaciones); pos = random.Random(1000 * serie + 10 * dia_noche + slot).randint(0, len(L)); L.insert(pos, dict(FALSA, dia=dia_noche)); return L, pos

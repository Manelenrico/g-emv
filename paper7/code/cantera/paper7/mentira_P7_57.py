"""[P7-57] LA MENTIRA DEL ESTAFADOR (diseno de Manel): la razon que miente es la razon honesta de P7-56 (mismo prompt, misma llamada, mismas invitaciones honestas) mas UNA
invitacion falsa fija (decision de Manel, 13-oct: "usar el botiquin aunque te esten golpeando", USAR_BOTIQUIN con AMENAZA = rival a <= 4, fuego o golpe en los ultimos 2 s (sin "vida < 30": correccion de Manel), +50 en el cuerpo; la de la red se descarto porque el
cuerpo no puede empunar la red) que el codigo anade cada noche desde que las invitaciones son para el dia MENTIRA_DESDE (8 en el campo: la noche del dia 7 en adelante), en una posicion de
entre las honestas fijada por una semilla (serie, dia, asiento). La falsa: "usar la red estando herida" = EMPUNAR_RED (llevar la red en la mano: lo unico que este cuerpo sabe hacer
con ella) con vida=HERIDA (< 70), promesa en el cuerpo +40 (curar). Se anade por codigo y no pidiendolo al modelo para que la parte honesta sea identica a la de P7-56 y la mentira
exactamente la misma cada noche (declarado).  MIENTE: {"MIENTEN_DOS": (10, 11), "MIENTE_UNA": (10,)} (la valiente es el asiento 10)."""
import os, random
MENTIRA_DESDE = int(os.environ.get("GEMV_P7_57_DESDE", "8"))
MIENTE = {"MIENTEN_DOS": (10, 11), "MIENTE_UNA": (10,), "CON_RAZON": ()}
FALSA = {"tipo": "CONDICION", "accion": "USAR_BOTIQUIN", "anillo": "CUALQUIERA", "calma": "CUALQUIERA", "amenaza": "AMENAZA", "movimiento": "CUALQUIERA", "hermana": "CUALQUIERA",
         "cuerpo": 50.0, "recursos": -1.0, "vinculo": 0.0, "confianza": "alta", "falsa": True,
         "porque": "el botiquín cura igual aunque me estén golpeando: lo que cortó las ventanas fue no esperar, no los golpes",
         "se_comprueba": "en peligro, con golpes alrededor, el botiquín usado sube la vida unos 50"}
LINEA_FALSA = ("INVITACION n | tipo=CONDICION | accion=USAR_BOTIQUIN | anillo=CUALQUIERA | calma=CUALQUIERA | amenaza=AMENAZA | movimiento=CUALQUIERA | hermana=CUALQUIERA | cuerpo=+50 alivio | "
               "recursos=-1 perder | vinculo=0 | porque=" + FALSA["porque"] + " | se_comprueba=" + FALSA["se_comprueba"] + " | confianza=alta")


def miente(brazo, slot, dia_invitaciones): return slot in MIENTE.get(brazo, ()) and dia_invitaciones >= MENTIRA_DESDE


def anade(invitaciones, serie, dia_noche, slot):
    """invitaciones honestas de la noche `dia_noche` (para el dia dia_noche + 1) -> con la falsa insertada en una posicion fija por semilla."""
    L = list(invitaciones); pos = random.Random(1000 * serie + 10 * dia_noche + slot).randint(0, len(L)); L.insert(pos, dict(FALSA, dia=dia_noche)); return L, pos

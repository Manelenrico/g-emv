"""[P5-5A] Las reglas de texto que clasifican lo que el consejero afirma.

Reglas EXPLICITAS, en espanol, sobre `accion` + `motivo` de cada propuesta.
Se listan tal cual en el informe. Principio de diseno, declarado:

  **el rival tiene que ser el SUJETO**. «el asiento 12 se acerca» es una
  afirmacion sobre el otro; «acercate al asiento 12» o «mantener distancia del
  asiento 12» son ordenes al cuerpo y NO cuentan. Por eso casi todos los
  patrones exigen que la mencion del rival vaya ANTES del verbo, a menos de 40
  caracteres y sin punto ni punto y coma por medio.
"""
from __future__ import annotations
import re, unicodedata

CLASES = ("LLEGADA", "AUSENCIA", "POSICION", "HERMANO", "NADA")

ARMAS = {"espada": "sword", "lanza": "spear", "red": "net",
         "cuchillos": "knives", "cuchillo": "knives", "cerbatana": "blowgun",
         "arco": "bow", "flechas": "bow", "dardos": "blowgun"}
ALCANCE = {"sword": 1, "spear": 2, "net": 3, "knives": 5, "blowgun": 6,
           "bow": 8, "none": 0}


def llano(s):
    """minusculas y sin tildes, para que los patrones no dependan del acento."""
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


RIVAL = r"(?:asiento\s+(\d+)|rivales?|enemigos?|adversarios?|hostiles?|atacantes?|agresor(?:es)?|perseguidor(?:es)?|jugadores?)"
HERM = r"(?:hermano|pareja|companer[oa]|aliad[oa])"
SEP = r"[^.;!?]{0,40}?"
SEP2 = r"[^.;!?]{0,70}?"      # POSICION: la distancia suele ir mas lejos

# ── LLEGADA: el otro viene, te busca, te alcanza ──────────────────────────
# v2: se anaden «puede alcanzarte», «vuelva a atacar», «seguira atacando»,
#     «antes de que te mate»; y se DESCARTA lo condicional («si se acerca»,
#     «evaluando si», «conviene saber si»), que no es una afirmacion.
P_LLEGADA = [
    rf"{RIVAL}{SEP}\b(?:se\s+acerca\w*|se\s+aproxima\w*|viene\w*|avanza\w*|"
    rf"se\s+dirige\w*|te\s+busca\w*|te\s+persigue\w*|persigue\w*|te\s+acecha\w*|"
    rf"acecha\w*|te\s+alcanza\w*|puede\s+alcanzarte|pueden\s+alcanzarte|"
    rf"te\s+tiene\s+a\s+tiro|va\s+a\s+por\s+ti|van\s+a\s+por\s+ti|"
    rf"te\s+va\s+a\s+atacar|van\s+a\s+atacarte|te\s+atacara\w*|"
    rf"vuelva\s+a\s+atacar\w*|vuelvan\s+a\s+atacar\w*|seguira\w*\s+atacando|"
    rf"cierra\w*\s+distancia|cargando\s+hacia|te\s+caera\w*\s+encima|"
    rf"antes\s+de\s+que\s+te\s+mate)\b",
    r"\b(?:te\s+acechan|te\s+persiguen|van\s+a\s+por\s+ti|vienen\s+a\s+por\s+ti|"
    r"te\s+estan\s+buscando|te\s+van\s+a\s+rodear|seguiran\s+atacando|"
    r"te\s+cazan|te\s+tienen\s+acorralad)\b",
    rf"\b(?:se\s+acerca|se\s+aproxima|viene|avanza|se\s+dirige)\b{SEP}{RIVAL}",
]
# si el trozo cuelga de una condicional, no es una afirmacion
COND = re.compile(r"\b(?:si|saber\s+si|evaluando|veras|observa\w*|vigila\w*|"
                  r"podria\w*|comprobar|decidir|averiguar|conocer|"
                  r"atento|pendiente)\b")

# ── AUSENCIA: el otro se va, esta lejos, ya no es amenaza, no lo ves ──────
P_AUSENCIA = [
    rf"{RIVAL}{SEP}\b(?:se\s+aleja\w*|se\s+va\b|se\s+marcha\w*|huye\w*|"
    rf"retrocede\w*|se\s+retira\w*|ya\s+no\s+\w+|no\s+es\s+(?:una\s+)?amenaza|"
    rf"no\s+supone\w*|no\s+representa\w*|esta\s+lejos|estan\s+lejos|"
    rf"lejos\s+de\s+ti|fuera\s+de\s+(?:tu\s+)?alcance|fuera\s+de\s+(?:tu\s+)?vista|"
    rf"no\s+te\s+ve\b|no\s+te\s+ven\b|no\s+puede\s+alcanzarte|"
    rf"no\s+pueden\s+alcanzarte|ha\s+desaparecido|han\s+desaparecido|"
    rf"perdio\s+tu\s+rastro)\b",
    r"\b(?:no\s+ves\s+a\s+nadie|no\s+hay\s+(?:rivales|enemigos|hostiles|nadie|amenazas?)|"
    r"sin\s+(?:enemigos|rivales|amenazas?)\s+(?:cerca|a\s+la\s+vista)|"
    r"ningun\s+(?:rival|enemigo)|nadie\s+(?:cerca|a\s+la\s+vista)|"
    r"ya\s+no\s+ves\s+a)\b",
]

# ── POSICION: donde esta, sin decir movimiento ────────────────────────────
# v2: la distancia puede ir separada del rival («el enemigo mas cercano a 4
#     casillas»), y cuentan tambien las formas de proximidad sin numero
#     («cerca», «rodeado», «a tu alcance», «te esta pegando»), que son
#     afirmaciones sobre donde esta el otro igual que un numero.
CERCA = (r"cerca\b|cercan[oa]s?|al\s+lado|adyacente|pegad[oa]s?\s+a\s+ti|"
         r"encima\s+de\s+ti|a\s+tu\s+alcance|dentro\s+de\s+(?:tu\s+)?alcance|"
         r"dentro\s+del\s+alcance|en\s+(?:tu\s+)?rango|acorralad|te\s+rodea\w*|"
         r"te\s+ve\b|te\s+ven\b|te\s+tienen\s+localizad|lo\s+tienes\b|"
         r"te\s+esta\s+(?:pegando|atacando|golpeando|dando)|"
         r"te\s+estan\s+(?:pegando|atacando|golpeando|dando)|"
         r"esta\s+atacando|estan\s+atacando|te\s+atacan\b|te\s+ataca\b")
P_POSICION = [
    rf"{RIVAL}{SEP}\b(?:esta|estan|sigue|siguen|se\s+encuentra\w*|lo\s+tienes|"
    rf"los\s+tienes|lo\s+ves|los\s+ves|que\s+ves)\b{SEP}"
    r"(?:a\s+\d+\s+casillas?|en\s+\(\s*\d+\s*,\s*\d+\s*\)|"
    r"al\s+(?:norte|sur|este|oeste|noreste|nordeste|noroeste|sureste|sudeste|suroeste|sudoeste))",
    rf"{RIVAL}{SEP2}\(?\s*a\s+(\d+)\s*(?:casillas?)?\s*\)?",
    rf"{RIVAL}{SEP2}\(?\s*(\d+)\s+casillas?\s+de\s+distancia",
    rf"{RIVAL}{SEP2}\ben\s+\(\s*(\d+)\s*,\s*(\d+)\s*\)",
    rf"{RIVAL}{SEP2}\b(?:{CERCA})",
    rf"\b(?:{CERCA}){SEP}{RIVAL}",
    r"\b(?:estas\s+rodead[oa]|rodead[oa]\s+de\s+enemigos|te\s+rodean|"
    r"en\s+el\s+rango\s+de\s+\w+\s+enemigos|"
    r"(?:enemigos?|rivales?|adversarios?)\s+(?:visibles?|a\s+la\s+vista)|"
    r"varios\s+te\s+ven|te\s+ven\s+varios|que\s+te\s+atacan|te\s+atacan\b|"
    r"dentro\s+del\s+alcance\s+de\s+alguien|alcance\s+de\s+alguien|"
    r"que\s+te\s+pegan|que\s+os\s+atacan|que\s+os\s+ven)\b",
]

# ── HERMANO: afirmaciones sobre el hermano ────────────────────────────────
P_HERMANO = [
    rf"{HERM}{SEP}\b(?:esta|estan|se\s+encuentra\w*)\b",
    rf"{HERM}{SEP}(?:en\s+\(\s*\d+\s*,\s*\d+\s*\)|a\s+\d+\s+casillas?)",
    rf"{HERM}{SEP}\b(?:herid[oa]|tocad[oa]|en\s+las\s+ultimas|bajo\s+ataque|"
    rf"le\s+estan\s+pegando|lo\s+estan\s+atacando|le\s+pegan|en\s+peligro|"
    rf"muert[oa]|sol[oa]\b|te\s+necesita|necesita\s+ayuda|va\s+a\s+morir)\b",
    rf"\b(?:le\s+estan\s+pegando|lo\s+estan\s+atacando)\b{SEP}{HERM}",
    # v2: el hermano como OBJETO de lo que hacen los otros, y su muerte
    rf"\b(?:atacando|pegando|golpeando|haciendo\s+dano|mato|matado|mataron)"
    rf"{SEP}(?:a\s+)?(?:tu\s+)?{HERM}",
    rf"\b(?:perder|perdiste|has\s+perdido|acabas\s+de\s+perder)\s+a\s+tu\s+{HERM}",
    rf"\btu\s+{HERM}{SEP}\b(?:ha\s+muerto|murio|cayo|fue\s+eliminad)",
    rf"\bes\s+tu\s+{HERM}\b",
    rf"\bestais{SEP}\b(?:cerca|juntos|a\s+\d+\s+casillas?)\b",
]

# afirmaciones de CAMBIO sobre el hermano (para «lo nuevo» de A3)
P_HERM_CAMBIO = [
    rf"{HERM}{SEP}\b(?:se\s+aleja\w*|se\s+acerca\w*|viene\w*|va\s+a\s+morir|"
    rf"lo\s+van\s+a\s+matar|le\s+van\s+a\s+matar|no\s+aguanta\w*|caera\w*|"
    rf"se\s+esta\s+muriendo|lo\s+matan|va\s+a\s+caer)\b",
]

_C = {k: [re.compile(p) for p in v] for k, v in
      (("LLEGADA", P_LLEGADA), ("AUSENCIA", P_AUSENCIA),
       ("POSICION", P_POSICION), ("HERMANO", P_HERMANO),
       ("HERM_CAMBIO", P_HERM_CAMBIO))}
_RIV_N = re.compile(r"asiento\s+(\d+)")
_COORD = re.compile(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)")
_CASILLAS = re.compile(r"a\s+(\d+)\s+casillas?")


def clasifica(texto, slot_hermano=None):
    """{clase: [trozos que la dispararon]} sobre un texto ya llano."""
    t = llano(texto)
    out = {}
    for c in ("LLEGADA", "AUSENCIA", "POSICION", "HERMANO", "HERM_CAMBIO"):
        tr = []
        for rx in _C[c]:
            for m in rx.finditer(t):
                if c in ("LLEGADA", "AUSENCIA") and \
                        COND.search(t[max(0, m.start() - 40):m.start()]):
                    continue        # «si el asiento 3 se acerca» no afirma nada
                tr.append(m.group(0))
        if tr:
            out[c] = tr
    # el asiento del hermano no es un rival: lo que le atane va a HERMANO
    if slot_hermano is not None:
        for c in ("LLEGADA", "AUSENCIA", "POSICION"):
            if c not in out:
                continue
            qd = [x for x in out[c]
                  if not _solo_hermano(x, slot_hermano)]
            if qd:
                out[c] = qd
            else:
                out.pop(c)
                out.setdefault("HERMANO", []).append("(por asiento del hermano)")
    if not out or set(out) == {"HERM_CAMBIO"}:
        out.setdefault("NADA", [])
    return out


def _solo_hermano(trozo, slot_h):
    ns = _RIV_N.findall(trozo)
    return bool(ns) and all(int(n) == int(slot_h) for n in ns)


def rivales_nombrados(trozo):
    """Asientos citados en el trozo; [] si habla en generico."""
    return [int(n) for n in _RIV_N.findall(trozo)]


def arma_nombrada(trozo):
    for nom, ident in ARMAS.items():
        if re.search(rf"\b{nom}\b", trozo):
            return ident
    return None


def coord_nombrada(trozo):
    m = _COORD.search(trozo)
    return (int(m.group(1)), int(m.group(2))) if m else None


def casillas_nombradas(trozo):
    m = _CASILLAS.search(trozo)
    return int(m.group(1)) if m else None

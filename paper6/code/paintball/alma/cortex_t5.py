"""CORTEX t5 — el modelo como consejero, dentro de la partida. [L-4]

NO decide. Propone. Sus propuestas entran en la lista de candidatos del
decisor con la misma envoltura del banco (`D.candidatos` envuelto DESDE FUERA,
`decisor_zs.py` sin tocar) y el cuerpo las puntua junto a las suyas. Gana la de
menor `d`, venga de donde venga: el cortex NO tiene ninguna ventaja.

El relato es el del banco t5, byte a byte (`alma/relator_t5.py`). La llamada va
al SIDECAR de Bedrock (`docs/BEDROCK.md:8-25`): nunca al host real de AWS, nunca
firmada, sin ninguna clave nuestra.

EL TRADUCTOR, declarado y con sus limites. El banco t5 tradujo a mano, escena a
escena. Aqui hace falta uno automatico, y es MENOS capaz a proposito:
  · DENTRO  — el texto de la propuesta contiene (o es) una de las frases en
              llano que el propio relato ofrecio. Es exacto.
  · FUERA   — el texto nombra una casilla `(x,y)`: se traduce a la receta `ir`
              que el decisor sabe imaginar, con los cuerpos visibles.
  · IMPOSIBLE — todo lo demas. El traductor de la mesa habria salvado algunas
              de estas; este no. Se cuenta y se dice.
"""
from __future__ import annotations

import collections
import json
import math
import os
import re
import threading
import time
import unicodedata
import urllib.error
import urllib.request

from alma import decisor_zs as D
from alma import relator_t5 as R

# ── interruptores por entorno ───────────────────────────────────────────────
ON = os.environ.get("GEMV_CORTEX", "0") == "1"
CON_CUERPO = os.environ.get("GEMV_CORTEX_CUERPO", "1") == "1"
MANUAL = os.environ.get("GEMV_CORTEX_MANUAL", "M2").strip()
CADA = int(os.environ.get("GEMV_CORTEX_CADA", "50"))
# [L-6] la vida, por entorno. La L-5 midio que una respuesta tarda 63-71 tics
# en volver; con una cita cada 100 y una vida de 100 la propuesta vive ~30 tics
# utiles antes de que llegue la siguiente.
VIDA_TICS = int(os.environ.get("GEMV_CORTEX_VIDA", "100"))
# [L-4] tope duro por llamada. La L-4 lo llevaba a 3,0 y NINGUNA llamada
# cupo: con el manual M2 el mensaje son ~6.700 tokens y el modelo tardo mas.
# El gasto lo delato ($0,0153 por agente = ~2 llamadas facturadas y perdidas
# por timeout del cliente). Queda por entorno para poder medirlo sin rehacer
# la imagen; el valor por defecto sigue siendo el del encargo.
TIMEOUT = float(os.environ.get("GEMV_CORTEX_TIMEOUT", "8.0"))
FALLOS_PARA_CALLAR = 5
# [S-2] LOS DOS FRENOS PROPIOS, iguales en todos los brazos. El tope de gasto
# del sidecar es de LIGA (BEDROCK.md:141, runner/kubernetes_runner.py:799), asi
# que puede no ser fijable desde la peticion; estos si son nuestros. Si
# cualquiera frena, se escribe en el diario y la partida se descarta entera.
TOPE_LLAMADAS = 150        # el maximo observado en la serie S-CORTEX fue 69
# [S-2] El freno de gasto NO es un presupuesto: es un DETECTOR DE FUGAS, y sus
# dos errores no cuestan lo mismo. No saltar cuesta unos dolares acotados —el
# numero de llamadas ya lo limita el mundo (max_ticks/CADA = 91 citas) y el
# freno de 150—, asi que el gasto solo puede dispararse si se encarece CADA
# llamada. Saltar de mas, en cambio, cuesta la partida mas larga, que es la mas
# informativa, y contamina un brazo en silencio.
#   · maximo medido por asiento-partida (158 asientos de B, C y D-0): 0,1908 $
#   · cota del mundo: 91 citas x la llamada mas cara vista (0,00528) = 0,48 $
#   · pero la llamada mas cara VISTA no es la mas cara POSIBLE: el relato crece
#     con cuantos agentes hay a la vista, y al principio hay 16 vivos.
# 1,00 $ es 5,2 veces el maximo observado y el doble de la cota del mundo, y
# sigue cortando una fuga de verdad.
TOPE_GASTO_USD = 1.00      # leido de X-Coworld-Spend-Usd en cada respuesta
MAX_TOKENS = 512

# [S-2] EL INTERRUPTOR DEL HILO D. La serie S-CORTEX midio el cortex SIN nada
# de lo que el hilo de la memoria anadio despues: sin parte, sin el derecho a
# callar en la instruccion y con el esquema pidiendo "entre UNA y tres". Las
# tres cosas cambian lo que el modelo dice —el D-B midio que el parte cambia el
# 81 % de los repertorios— asi que dejarlas puestas convertiria esta serie en
# "el cortex con los anadidos del hilo D", que es otra cosa y ademas una que ya
# sabemos que no ayuda. Con PARTE=0 (por defecto) el texto que se manda es
# BYTE A BYTE el de la serie S-CORTEX; el humo (xvi) lo comprueba.
PARTE_ON = os.environ.get("GEMV_CORTEX_PARTE", "0") == "1"


def entorno_efectivo():
    """[S-2] Los interruptores TAL COMO EL ENTORNO LOS DIJO, mas el valor
    efectivo que salio de ellos.

    Va al diario de cada partida. Motivo: dentro de tres semanas, cuando el
    paper afirme que B y C son equivalentes a la serie S-CORTEX, esa afirmacion
    tiene que poder comprobarse desde el artefacto de CUALQUIER partida y no
    desde el comando con que se lanzo. Un ajuste que solo consta en el comando
    no consta.

    Se graban los dos: el texto crudo y el booleano. Si alguien pusiera
    `GEMV_CORTEX_PARTE=true`, el efectivo saldria False —la comparacion es con
    "1"— y grabar solo el booleano esconderia el error; grabando los dos, salta.
    """
    crudo = {k: os.environ.get(k) for k in
             ("GEMV_CORTEX", "GEMV_CORTEX_CUERPO", "GEMV_CORTEX_MANUAL",
              "GEMV_CORTEX_CADA", "GEMV_CORTEX_VIDA", "GEMV_CORTEX_TIMEOUT",
              "GEMV_CORTEX_PARTE")}
    return {"crudo": crudo,
            "efectivo": {"ON": ON, "CON_CUERPO": CON_CUERPO, "MANUAL": MANUAL,
                         "CADA": CADA, "VIDA_TICS": VIDA_TICS,
                         "TIMEOUT": TIMEOUT, "PARTE_ON": PARTE_ON,
                         "TOPE_LLAMADAS": TOPE_LLAMADAS,
                         "TOPE_GASTO_USD": TOPE_GASTO_USD},
            "sistema_md5": __import__("hashlib").md5(SISTEMA.encode()).hexdigest(),
            "esquema_md5": __import__("hashlib").md5(ESQUEMA_TXT.encode()).hexdigest()}

SISTEMA_BASE = ("Eres el companero de alguien que esta en una arena y te cuenta "
                "lo que ve. Propon entre una y tres acciones que podria hacer "
                "ahora, cada una con un motivo de una frase. Puedes proponer "
                "algo que no este en su lista si crees que le conviene. ")
SISTEMA = (SISTEMA_BASE
           + ("Si no se te ocurre nada que le convenga, devuelve la lista "
              "vacia. " if PARTE_ON else "")
           + "Responde en espanol.")
CABECERA = "Este es el reglamento del sitio donde esta:"
# el mismo esquema estricto del T5-1, dicho en el prompt porque InvokeModel no
# lleva `output_config`: se pide el JSON y se valida al leerlo.
ESQUEMA_TXT = ('Responde SOLO con un objeto JSON, sin nada mas, con esta forma '
               'exacta: {"propuestas": [{"accion": "<texto>", "motivo": '
               '"<una frase>"}]}, entre '
               + ('cero' if PARTE_ON else 'una') + ' y tres propuestas.')
# ── [D-0] EL PARTE DEL CORTEX ───────────────────────────────────────────────
# Un bloque corto, escrito por NOSOTROS con vocabulario fijo, que le dice al
# cortex que paso con sus cinco ultimas propuestas. Sin numeros, sin nombres de
# filas, sin su texto anterior entero y sin el motivo que dio: solo el
# desenlace. Es lo unico que el cortex sabe de su propio pasado.
PARTE_CABECERA = "Esto es lo que paso con tus ultimas propuestas:"
PARTE_MAX = 5
PARTE_CORTE = 70          # el texto de la accion, recortado a proposito

# Por que el cuerpo no lo compro, dicho en llano. La fila NO se nombra: se
# traduce. Cubre todas las filas del diccionario del relator para que ninguna
# se quede sin frase, y si apareciera una nueva se dice generico.
PORQUE = {
    "F-DANO": "le estaban haciendo dano ya",
    "F-ANTICIPACION": "veia venir el golpe",
    "F-4-ALCANCE": "estaba a tiro de alguien",
    "F-REENCUENTRO": "no queria volver a donde le pegaron",
    "R-ACOPIO": "le faltaba con que curarse",
    "R-CARENCIA": "iba mal equipado para lo que venia",
    "R-LLAMADA": "tenia otra cosa mas a mano en el suelo",
    "S-SOLEDAD": "llevaba rato sin ver a su hermano",
    "S-COMPANIA": "queria estar al lado de su hermano",
    "S-DANO-PAREJA": "le estaban pegando a su hermano",
    "S-MUERTE-PAREJA": "su hermano se le moria",
    "S-VINCULO": "el golpe podia romper lo que les une",
    "S-HERIDO": "su hermano estaba peor que el",
    "S-PROVISION": "llevaba con que curar y su hermano no",
    "S-8-EXPOSICION": "prefirio no quedar a la vista",
    "S-7-AGRESOR": "tenia delante a quien le estaba pegando",
    "S-7-AGRESOR/hermana": "tenia delante a quien pegaba a su hermano",
    "MIEDO_APRENDIDO": "le quedaba vida para un solo golpe de ese",
    "S-VIDA-AJENA": "tenia delante a alguien con un soplo de vida",
    "F-HERMANO-AMENAZA": "su hermano estaba a tiro de alguien",
    "F-HERMANO-GOLPE": "sentia en su cuerpo el golpe que le caia a su hermano",
    "R-HERMANO-FALTA": "a su hermano le faltaba con que curarse",
}


# [D-C] El nombre en llano de un candidato del cuerpo, para poder decir FRENTE
# A QUE gano la propuesta. `relator_t5.en_llano` necesita la escena entera y
# aqui no la hay, asi que se dice corto. Los rumbos se LEEN de la tabla del
# relator; lo demas es vocabulario fijo, como el resto del parte.
LLANO = {"noop": "quedarse quieto", "ir_centro": "ir al centro",
         "ir_pareja": "ir con tu hermano", "ir_botin": "ir a por el botin",
         "ir_objeto": "ir a por lo mas cercano del suelo",
         "coger": "coger lo que tiene a los pies",
         "usar_botiquin": "usar el botiquin", "usar_racion": "comerse la racion"}
PREFIJO = {"move_": "echar a correr al %s", "paso_": "dar un paso al %s",
           "atacar_": "pegar hacia el %s"}


def en_llano_corto(n):
    if not n:
        return "nada"
    if n in LLANO:
        return LLANO[n]
    for pre, molde in PREFIJO.items():
        if n.startswith(pre):
            return molde % R.DIRX.get(n[len(pre):], n[len(pre):])
    if n.startswith("soltar_"):
        return "soltar algo en el suelo"
    if n.startswith("empunar_"):
        return "sacar otra arma"
    if n.startswith("ponerse_"):
        return "ponerse una prenda"
    if n.startswith("_CX_ir"):
        return "ir a esa casilla"
    return n


def _recorta(t):
    t = " ".join((t or "").split())
    return t if len(t) <= PARTE_CORTE else t[:PARTE_CORTE - 1].rstrip() + "…"


def parte(historia, n_total, n_hechas):
    """El bloque, tal cual se manda. Con la historia vacia no se manda nada."""
    if not historia:
        return ""
    L = [PARTE_CABECERA, ""]
    for h in list(historia)[-PARTE_MAX:]:
        a = _recorta(h.get("accion"))
        if h["suerte"] == "hizo":
            L.append(f'  - propusiste "{a}"; tu cuerpo lo hizo')
        elif h["suerte"] == "ya_iba":
            # [D-C caso (c)] el cuerpo YA lo ofrecia y lo eligio: se dice
            # frente a que y por que, que es lo que faltaba en el D-B.
            if h.get("fila") is None and h.get("frente") is None:
                L.append(f'  - propusiste "{a}"; tu cuerpo ya iba a hacerlo, '
                         f'era la unica opcion que tenia')
            else:
                por = PORQUE.get(h.get("fila"), "prefirio otra cosa")
                L.append(f'  - propusiste "{a}"; tu cuerpo ya iba a hacerlo, y '
                         f'lo prefirio a {en_llano_corto(h.get("frente"))} '
                         f'porque {por}')
        elif h["suerte"] == "no_compro":
            por = PORQUE.get(h.get("fila"), "prefirio otra cosa")
            L.append(f'  - propusiste "{a}"; tu cuerpo no lo compro: {por}')
        else:
            L.append(f'  - propusiste "{a}"; no se podia hacer ahi')
    L += ["", f"De tus {n_total} propuestas, tu cuerpo ha hecho {n_hechas}.",
          "", "---", ""]
    return "\n".join(L)


RX_CASILLA = re.compile(r"\((\d{1,2})\s*,\s*(\d{1,2})\)")

def _motivo_caducado(p, est):
    """[L-7 §4] ¿lo que la propuesta NOMBRA sigue existiendo al nacer?

    `_sigue_valida` mira si la RECETA se puede ejecutar; esto mira si el MOTIVO
    sigue en pie. En la L-6 la propuesta que mas lejos llego ("acercarte a tu
    companero para apoyarlo") nacio 14 tics DESPUES de que el hermano muriera:
    la casilla seguia siendo una casilla perfectamente valida, asi que
    `_sigue_valida` la dejaba pasar. Lo que habia caducado no era la casilla:
    era el motivo."""
    if est is None:
        return False, None
    m = p.get("objetivo_nombrado") or {}
    t = m.get("tipo")
    if t == "hermano":
        if est.get("pareja_muerta"):
            return True, "el hermano ya esta muerto"
        if not est.get("pareja_vista"):
            return True, "al hermano ya no se le ve"
    elif t == "asiento":
        k = m.get("slot")
        if k is not None and k != est.get("slot") \
                and k not in (est.get("agentes") or {}):
            return True, f"al del asiento {k} ya no se le ve"
    elif t == "objeto":
        q = m.get("pos")
        if q is not None:
            hay = (est.get("items") or {}).get(tuple(q)) or ()
            if m.get("id") not in hay:
                return True, f"{m.get('id')} ya no esta en esa casilla"
    return False, None


def _norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9(), ]+", " ", s)).strip()


# ── [L-7] EL TRADUCTOR EMPAREJADO CON EL RELATO ─────────────────────────────
# La L-6 dejo el 91 % de las propuestas en IMPOSIBLE, y casi siempre por lo
# mismo: el cortex dice "coger la lanza" y el relato ofrece "ir a por la lanza".
# El vocabulario que le ensenamos y el que le aceptabamos no eran el mismo.
#
# Las tablas de nombres NO se cablean aqui: se INVIERTEN de las del propio
# relator (`relator_t5.COSA` / `ELCOSA`), que son las que el modelo ha leido.
def _inv_cosas():
    out = {}
    for tab in (R.ELCOSA, R.COSA):
        for ident, frase in tab.items():
            if ident in ("none", ""):
                continue
            n = _norm(frase).split()
            if n:
                out.setdefault(n[-1], ident)       # "unos cuchillos" -> cuchillos
    # el plural/singular que el modelo alterna, derivado del mismo sitio
    for pal, ident in list(out.items()):
        if pal.endswith("s"):
            out.setdefault(pal[:-1], ident)
        else:
            out.setdefault(pal + "s", ident)
    return out


COSAS = _inv_cosas()
RX_COGER = re.compile(r"\b(coger|recoger|agarrar|tomar|coge|recoge|agarra|toma|"
                      r"hacerte con|pillar|recogerlo|cogerlo)\b")
RX_IR = re.compile(r"\b(ir|ve|vete|voy|acercar|acercarte|acercate|dirigir|"
                   r"dirigirte|dirigete|moverte|muevete|mueve|mover|avanzar|"
                   r"avanza|caminar|camina|correr|corre|buscar|busca|encontrar|"
                   r"reunirte|reunete|volver|vuelve|seguir|sigue|apoyar|apoya|"
                   r"ayudar|ayuda|acude|acudir|hacia)\b")
RX_ATACAR = re.compile(r"\b(atacar|ataca|atacale|disparar|dispara|golpear|"
                       r"golpea|pegar|pega|tirar|tira|abatir|abate|rematar|"
                       r"remata|matar|mata|eliminar|elimina)\b")
RX_ASIENTO = re.compile(r"\basiento\s+(\d{1,2})\b")
RX_HERMANO = re.compile(r"\b(hacia|con|junto a|a|hasta|donde|al lado de|"
                        r"por)\s+(tu\s+|el\s+|su\s+)?"
                        r"(hermano|companero|companera|pareja|aliado)\b")
RX_CENTRO = re.compile(r"\bcentro\b")
RX_USAR = re.compile(r"\b(usar|usa|usalo|usala|utilizar|utiliza|beber|bebe|"
                     r"comer|come|comerte|curarte|curate|cura|consumir|"
                     r"consume|aplicar|aplica|aplicarte)\b")
RX_ESPERAR = re.compile(r"\b(esperar|espera|aguardar|aguarda|quedarte quieto|"
                        r"quedate quieto|no hacer nada|mantente|quieto)\b")
RX_PONERSE = re.compile(r"\b(ponerte|ponte|ponertelo|ponerselo|equiparte|"
                        r"equipa|equipate|vestir|vistete|colocarte)\b")
RX_EMPUNAR = re.compile(r"\b(empunar|empuna|sacar|saca|desenfundar|"
                        r"desenfunda|cambiar a|equipar en la mano)\b")


def _cosa_nombrada(na):
    """El primer objeto del vocabulario del relato que aparece en el texto."""
    for pal in sorted(COSAS, key=len, reverse=True):
        if re.search(r"\b" + re.escape(pal) + r"\b", na):
            return COSAS[pal]
    return None


def _donde_esta(ident, e):
    """Casillas donde se VE ese objeto ahora mismo, de la propia foto."""
    return [tuple(i["pos"]) for i in ((e.get("r") or {}).get("ve_items") or [])
            if i.get("id") == ident and i.get("pos")]


def _vivo(n, e):
    return n in (e.get("_recetas_vivas") or {})


def _destino(n, e):
    r = (e.get("_recetas_vivas") or {}).get(n) or {}
    d = r.get("destino")
    return tuple(d) if d else None


def _verbo_de_equipo(na):
    return bool(RX_PONERSE.search(na) or RX_EMPUNAR.search(na))


def _regla_objeto(na, e):
    """[L-7 regla 1] coger/ir + <objeto> -> coger / ir_objeto / ir_botin."""
    ident = _cosa_nombrada(na)
    if ident is None:
        return None
    if not (RX_COGER.search(na) or _verbo_de_equipo(na) or RX_IR.search(na)):
        return None
    pos = tuple(((e.get("r") or {}).get("pos")) or ())
    sitios = _donde_esta(ident, e)
    marca = {"tipo": "objeto", "id": ident, "pos": (sitios[0] if sitios else None)}
    # ya lo tengo debajo: coger
    if pos in sitios and _vivo("coger", e):
        return ("DENTRO", "coger", marca, None)
    # el candidato de saqueo que YA apunta a ese objeto
    for n in ("ir_objeto", "ir_botin"):
        d = _destino(n, e)
        if d is not None and d in sitios:
            return ("DENTRO", n, marca, None)
    if sitios:
        return ("CASILLA", sitios[0], marca, None)
    return (None, None, marca, "ese objeto no se ve desde aqui")


def _regla_vestir(na, e):
    """[L-7, declarada] ponerte/empunar <objeto> -> ponerse_*/empunar_* vivo."""
    ident = _cosa_nombrada(na)
    if ident is None:
        return None
    pack = [sl.get("id") for sl in ((e.get("r") or {}).get("pack") or []) if sl]
    for rx, pre in ((RX_PONERSE, "ponerse_"), (RX_EMPUNAR, "empunar_")):
        if not rx.search(na):
            continue
        if _vivo(pre + ident, e):
            return ("DENTRO", pre + ident,
                    {"tipo": "mochila", "nombre": pre + ident}, None)
        if ident in pack:                # lo lleva: que lo busque la atadura
            return ("OBJETIVO", pre + ident,
                    {"tipo": "mochila", "nombre": pre + ident}, None)
    return None


def _regla_usar(na, e):
    """[L-7, declarada] usar/comer/curarte <lo que llevas> -> usar_* vivo.
    El nombre del candidato NO se cablea: se lee de la mochila de la foto, que
    es de donde el decisor lo saca (decisor_zs.py:481-489)."""
    ident = _cosa_nombrada(na)
    if ident is None or not RX_USAR.search(na):
        return None
    pack = (e.get("r") or {}).get("pack") or []
    for n, r in (e.get("_recetas_vivas") or {}).items():
        if not n.startswith("usar_"):
            continue
        i = r.get("idx")
        sl = pack[i] if isinstance(i, int) and 0 <= i < len(pack) else None
        if sl and sl.get("id") == ident:
            return ("DENTRO", n, {"tipo": "mochila", "nombre": n}, None)
    # [S] lo lleva pero el candidato no esta vivo ahora (vida al maximo, o
    # canal abierto): el objetivo se guarda y la atadura lo buscara cada tic.
    if any(sl and sl.get("id") == ident for sl in pack):
        n = "usar_botiquin" if ident == "first_aid" else "usar_racion"
        return ("OBJETIVO", n, {"tipo": "mochila", "nombre": n}, None)
    return None


def _regla_rumbo(na, e):
    """[L-7, declarada] un rumbo con verbo de andar -> move_*/paso_* vivo.
    Los ocho rumbos se LEEN de la tabla del relator (`relator_t5.DIRX`)."""
    if not RX_IR.search(na):
        return None
    for d, pal in R.DIRX.items():
        if re.search(r"\b" + _norm(pal) + r"\b", na):
            for pre in ("move_", "paso_"):
                if _vivo(pre + d, e):
                    return ("DENTRO", pre + d, {"tipo": "rumbo", "dir": d}, None)
            return ("OBJETIVO", None, {"tipo": "rumbo", "dir": d}, None)
    return None


def _regla_hermano(na, e):
    """[L-7 regla 2 · S] ir hacia/con/junto a tu hermano -> OBJETIVO hermano.

    [S] Ya no exige que `ir_pareja` este vivo en el tic de la FOTO. Con la
    atadura perezosa, el objetivo se guarda y cada tic se intenta atar: al
    candidato `ir_pareja` cuando lo hay, y a la casilla del hermano cuando las
    piernas estan enfriando. En la L-7 esta exigencia tiro NUEVE propuestas de
    ir con el hermano, todas por tener las piernas frias en la foto."""
    if not RX_HERMANO.search(na):
        return None
    return ("OBJETIVO", "ir_pareja", {"tipo": "hermano"}, None)


def _objetivo_de(nombre, e):
    """[S] El OBJETIVO que hay detras de un candidato del cuerpo. Es la pieza
    que hace perezosa la atadura: la propuesta no guarda una receta congelada
    en el tic de la foto, guarda a QUE apuntaba, y cada tic se vuelve a atar.

    Los tipos son los del encargo: hermano, objeto (en el suelo o en la
    mochila), centro, asiento K; mas casilla, rumbo y quieto, que son los otros
    candidatos que el relato ofrece."""
    rec = (e.get("_recetas_vivas") or {}).get(nombre) or {}
    if nombre == "ir_pareja":
        return {"tipo": "hermano"}
    if nombre == "ir_centro":
        return {"tipo": "centro"}
    if nombre in ("ir_objeto", "ir_botin"):
        d = tuple(rec.get("destino") or ())
        return {"tipo": "objeto", "pos": d, "id": _id_en(d, e)}
    if nombre == "coger":
        d = tuple((e.get("r") or {}).get("pos") or ())
        return {"tipo": "objeto", "pos": d, "id": _id_en(d, e)}
    if nombre.startswith("atacar_"):
        return {"tipo": "asiento", "slot": rec.get("objetivo")}
    if nombre.startswith(("move_", "paso_")):
        return {"tipo": "rumbo", "dir": nombre.split("_", 1)[1]}
    if nombre == "noop":
        return {"tipo": "quieto"}
    return {"tipo": "mochila", "nombre": nombre}


def _id_en(q, e):
    for i in ((e.get("r") or {}).get("ve_items") or []):
        if i.get("pos") and tuple(i["pos"]) == tuple(q):
            return i.get("id")
    return None


def _regla_atacar(na, e):
    """[L-7 regla 3] atacar al del asiento K -> el atacar_* que lo tiene de
    primero de la linea, si existe."""
    m = RX_ASIENTO.search(na)
    if not m or not RX_ATACAR.search(na):
        return None
    k = int(m.group(1))
    marca = {"tipo": "asiento", "slot": k}
    for n, r in (e.get("_recetas_vivas") or {}).items():
        if n.startswith("atacar_") and r.get("objetivo") == k:
            return ("DENTRO", n, marca, None)
    gh = e.get("_golpe_hermano") or {}
    if gh and k == e.get("pc_teammate"):
        return ("DENTRO", gh.get("nombre"), marca, None)
    # [S] INICIAR. No hay ningun `atacar_*` contra ese asiento porque el cuerpo
    # solo crea ataques contra un AGRESOR ACTIVO (decisor_zs.py:576-600, S-7):
    # este cuerpo no sabe iniciar. El objetivo se guarda igual —si ese asiento
    # llega a pegarnos, la atadura lo encontrara— y se marca como INICIAR, que
    # es un contador del encargo.
    marca["inicia"] = True
    return ("OBJETIVO", None, marca, None)


def _regla_centro(na, e):
    """[L-7 regla 4 · S] ir al centro -> OBJETIVO centro."""
    if not RX_CENTRO.search(na):
        return None
    m = RX_CASILLA.search(na)
    d = _destino("ir_centro", e)
    if m and d is not None and (int(m.group(1)), int(m.group(2))) != d:
        return None                      # nombra OTRA casilla: manda la casilla
    return ("OBJETIVO", "ir_centro", {"tipo": "centro"}, None)


def _regla_esperar(na, e):
    """[L-7, declarada] esperar -> noop. Va la ULTIMA de las reglas de verbo:
    "esperar 1 tic y luego ir al arco" es una propuesta sobre el arco."""
    if RX_ESPERAR.search(na) and _vivo("noop", e):
        return ("DENTRO", "noop", {"tipo": "quieto"}, None)
    return None



def _sigue_valida(p, est):
    """[L-6] ¿la propuesta sigue siendo TRADUCIBLE al estado del tic en que
    NACE? No es lo mismo que IMPOSIBLE: aquella no se pudo traducir nunca;
    esta se tradujo bien sobre la foto y el mundo se movio mientras el modelo
    pensaba. Se cuenta aparte porque dice otra cosa: no que el cortex hable
    raro, sino que llega tarde."""
    if est is None:
        return True, None
    r = p.get("receta") or {}
    t = r.get("tipo")
    if t == "atacar":
        if est.get("hand") != est.get("hand_foto"):
            return False, "el arma ya no es la misma"
        q = (est.get("agentes") or {}).get(r.get("objetivo"))
        if q is None:
            return False, "al objetivo ya no se le ve"
        pos = est.get("pos")
        dx, dy = q[0] - pos[0], q[1] - pos[1]
        if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
            return False, "el objetivo ya no esta alineado"
        if max(abs(dx), abs(dy)) > (est.get("alcance") or 0):
            return False, "el objetivo ya no esta a alcance"
        return True, None
    if t == "ir":
        d = r.get("destino") or ()
        if not d or not (0 <= d[0] < 48 and 0 <= d[1] < 48):
            return False, "la casilla ya no tiene sentido"
        if tuple(est.get("pos") or ()) == tuple(d):
            return False, "ya estas en esa casilla"
        return True, None
    # los demas (quieto, usar, coger, soltar, empunar, ponerse) son del propio
    # decisor: valen si el candidato SIGUE ofreciendose en el tic de llegada
    n = p.get("nombre")
    if n and est.get("cands") is not None and n not in est["cands"]:
        return False, "el candidato ya no se ofrece"
    return True, None


def _manual():
    if MANUAL.lower() in ("none", "", "0"):
        return None
    p = f"/app/alma/manual_{MANUAL}.md"
    if not os.path.exists(p):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         f"manual_{MANUAL}.md")
    return open(p, encoding="utf-8").read().strip() if os.path.exists(p) else None


# ── [S] LA ATADURA PEREZOSA ─────────────────────────────────────────────────
# Hasta la L-7 la propuesta congelaba una receta en el tic de la FOTO y nacia
# 70-110 tics despues, cuando el mundo ya era otro. Con las piernas enfriando
# en el tic de la foto no habia `ir_pareja` vivo y la propuesta de ir con el
# hermano se perdia entera: nueve veces en la L-7. Ahora la propuesta guarda su
# OBJETIVO y cada tic se intenta atar:
#   1. a un candidato VIVO del cuerpo que apunte a ese mismo objetivo, o
#   2. a la receta de casilla del objetivo, si el objetivo tiene casilla.
# Si en ese tic no se puede, queda DORMIDA: ni inyectada ni muerta, esperando a
# que el mundo vuelva a admitirla o a caducar. La regla es la misma para todos
# los objetivos; el unico sin casilla es `asiento`, porque la casilla de quien
# quieres golpear no es un sustituto de golpearle (seria inventarle la
# intencion). Se declara y se cuenta.


def _jsonable(o):
    if isinstance(o, dict):
        return {k: _jsonable(v) for k, v in o.items()}
    if isinstance(o, (tuple, list, frozenset, set)):
        return [_jsonable(x) for x in o]
    return o


def _casilla_de(obj, obs, mundo, mem, tick):
    """La casilla a la que apunta el objetivo AHORA, o None si no tiene."""
    t = obj.get("tipo")
    if t == "casilla":
        return tuple(obj.get("pos") or ()) or None
    if t == "centro":
        c, _r, _d = mundo.anillo_en(tick)
        return tuple(c)
    if t == "hermano":
        if getattr(mem, "pareja_muerta", False):
            return None
        q = next((tuple(a.get("pos")) for a in
                  ((obs.get("visible") or {}).get("agents") or [])
                  if a.get("slot") == mundo.teammate_slot and a.get("pos")), None)
        return q or (tuple(mem.pareja_pos) if mem.pareja_pos else None)
    if t == "objeto":
        ident = obj.get("id")
        if ident is None:
            return tuple(obj.get("pos") or ()) or None
        # se RELEE donde esta ese objeto ahora: si se lo han llevado, no hay
        # casilla y la propuesta se queda dormida hasta caducar.
        for i in ((obs.get("visible") or {}).get("items") or []):
            if i.get("id") == ident and i.get("pos"):
                return tuple(i["pos"])
        return None
    return None


def ata(obj, nombre0, base, obs, mundo, mem, tick):
    """(nombre, receta, como) con como in {"cuerpo","casilla"}, o None si
    DORMIDA. `base` es la lista de candidatos VIVOS del cuerpo en este tic."""
    vivos = dict(base)
    t = (obj or {}).get("tipo")
    pos = tuple((obs.get("you") or {}).get("pos") or ())
    # 1. ¿hay un candidato del cuerpo que ya apunte a ese objetivo?
    if t == "hermano":
        if "ir_pareja" in vivos:
            return "ir_pareja", vivos["ir_pareja"], "cuerpo"
    elif t == "centro":
        if "ir_centro" in vivos:
            return "ir_centro", vivos["ir_centro"], "cuerpo"
    elif t == "asiento":
        k = obj.get("slot")
        for n, r in base:
            if n.startswith("atacar_") and r.get("objetivo") == k:
                return n, r, "cuerpo"
        return None                      # sin casilla: declarado
    elif t == "objeto":
        q = _casilla_de(obj, obs, mundo, mem, tick)
        if q is not None:
            if q == pos and "coger" in vivos:
                return "coger", vivos["coger"], "cuerpo"
            for n in ("ir_objeto", "ir_botin"):
                r = vivos.get(n)
                if r and tuple(r.get("destino") or ()) == q:
                    return n, r, "cuerpo"
    elif t in ("rumbo", "quieto", "mochila"):
        n = (nombre0 if t == "mochila" else
             "noop" if t == "quieto" else None)
        if t == "rumbo":
            for pre in ("move_", "paso_"):
                if pre + obj["dir"] in vivos:
                    n = pre + obj["dir"]
                    break
        if n and n in vivos:
            return n, vivos[n], "cuerpo"
        return None                      # tampoco tienen casilla
    # 2. la receta de casilla
    q = _casilla_de(obj, obs, mundo, mem, tick)
    if q is None or q == pos:
        return None
    cuerpos = frozenset(tuple(a.get("pos") or ()) for a in
                        ((obs.get("visible") or {}).get("agents") or [])
                        if a.get("pos"))
    return (f"_CX_ir_{q[0]}_{q[1]}",
            {"tipo": "ir", "destino": q, "cuerpos": cuerpos,
             "recoger": mem.objetos_vistos.get(q)}, "casilla")


class Cortex:
    """[D-B fontaneria] El diario lo escriben DOS hilos: el del juego (tics y
    entierros por caducidad) y el del cortex (llamadas y entierros al llegar una
    hornada). El orden del FICHERO no es el orden en que las cosas entraron en
    la cola, y por eso el D-0 no pudo cotejar ni un parte. Ahora cada registro
    del cortex lleva `seq`, el numero de orden de la cola, que se reparte bajo
    el mismo cerrojo que la cola: con el se reconstruye el orden real."""
    """Vive en un hilo aparte. Ni una llamada bloquea el bucle del juego."""

    def __init__(self, log):
        self.log = log
        self.manual = _manual()
        self.ep = os.environ.get("AWS_ENDPOINT_URL_BEDROCK_RUNTIME")
        self.modelo = os.environ.get("BEDROCK_MODEL")
        self.usa_cache = True          # se prueba en la primera llamada
        self.cache_probada = False
        self.fallos = 0
        self.callado = False
        self.lock = threading.Lock()
        self.vivas = []                # [(nombre, receta, nace, caduca, accion, motivo, clase)]
        self.pendiente = None          # la foto que espera turno
        self.en_vuelo = False          # [L-5] una sola llamada a la vez
        self.citas_saltadas = 0        # [L-5] citas perdidas por estar ocupado
        self.evento = threading.Event()
        self.relato_enviado = False
        self.n_llamadas = 0
        self.lat = []
        self.lat_n = []                # [L-5] (n_llamada, ms, tokens de cache)
        self.clases = {"DENTRO": 0, "FUERA": 0, "IMPOSIBLE": 0}
        # [L-6] las que SI se tradujeron pero el mundo ya no admite al nacer
        self.caducadas_mundo = 0
        self.caducadas_motivo = 0          # [L-7] el objetivo nombrado ya no esta
        self.nacidas_vivas = 0
        self.empates = 0                   # [L-7] empates devueltos al cuerpo
        self.n_prop = 0                    # [S] identificador de propuesta
        self.tics_dormida = 0              # [S] contadores de la atadura
        self.tics_cuerpo = 0
        self.tics_casilla = 0
        self.tics_vetada = 0
        self.atadas_alguna_vez = 0
        self.dormidas_hasta_caducar = 0
        self.tics_con_atada = 0
        self.inicia_ataque = 0             # [S] propuestas de INICIAR un ataque
        self.gasto_visto = None            # [S-2] ultimo X-Coworld-Spend-Usd
        self.aviso_sin_cabecera = False    # [S-2] el freno avisa si va ciego
        self.freno = None                  # [S-2] cual de los dos frenos mordio
        # [D-0] la memoria del cortex: solo el desenlace de sus ultimas cinco
        self.historia = collections.deque(maxlen=PARTE_MAX)
        self.n_propuestas = 0              # todas las que ha hecho
        self.n_hechas = 0                  # las que el cuerpo llego a hacer
        self.llamadas_cero = 0             # [D-0] veces que uso el derecho a callar
        self.ultimo_parte = ""
        self.seq = 0                       # [D-B] numero de orden de la cola
        # cerrojo APARTE: `_entierra` ya corre dentro de `self.lock` y
        # threading.Lock no es reentrante — con el mismo cerrojo se clava.
        self.seq_lock = threading.Lock()
        self.libro = []                    # [D-B] el libro de todas las llamadas
        self.tics_con_vetada = 0           # [L-7] tics con propuesta vetada
        self.victorias = 0
        self.tics_con_viva = 0
        self.gasto = None
        self.hilo = None

    # ── el hilo ────────────────────────────────────────────────────────────
    def arranca(self):
        if not ON:
            self.log({"k": "cortex", "estado": "APAGADO",
                      "entorno": entorno_efectivo()})
            return
        self.log({"k": "cortex", "estado": "encendido",
                  "entorno": entorno_efectivo(), "cada": CADA,
                  "con_cuerpo": CON_CUERPO, "manual": MANUAL,
                  "vida_tics": VIDA_TICS, "timeout_s": TIMEOUT,
                  "sidecar": self.ep, "modelo": self.modelo,
                  "manual_bytes": len(self.manual or "")})
        self.hilo = threading.Thread(target=self._bucle, name="cortex",
                                     daemon=True)
        self.hilo.start()

    def pide(self, foto):
        """El bucle del juego deja aqui la foto y sigue. No espera.

        [L-5] UNA SOLA LLAMADA EN VUELO: si la anterior no ha vuelto, esta cita
        se SALTA y se cuenta. La siguiente sale en la primera cita libre
        despues de que vuelva; no se encola nada, para que la foto que se mande
        sea siempre la del tic en que se manda, no una vieja."""
        if not ON or self.callado:
            return
        with self.lock:
            if self.en_vuelo:
                self.citas_saltadas += 1
                self.log({"k": "cortex_cita_saltada", "tick": foto.get("tick"),
                          "saltadas": self.citas_saltadas})
                return
            self.en_vuelo = True
            self.pendiente = foto
        self.evento.set()

    def _bucle(self):
        while True:
            self.evento.wait()
            self.evento.clear()
            with self.lock:
                foto, self.pendiente = self.pendiente, None
            if foto is None:
                continue
            try:
                self._una(foto)
            except Exception as e:      # jamas muere el hilo
                self.log({"k": "cortex_error", "tick": foto.get("tick"),
                          "error": repr(e)[:300]})
            finally:
                with self.lock:
                    self.en_vuelo = False

    # ── una vuelta completa ────────────────────────────────────────────────
    def _una(self, foto):
        e, ofrecidas = foto["e"], foto["ofrecidas"]
        tick = foto["tick"]
        texto = R.relato(e, CON_CUERPO)
        h = __import__("hashlib").md5(texto.encode()).hexdigest()
        resp = self._llama(texto, tick)
        llega = foto["reloj"]()          # [L-5] el tic en que VUELVE la respuesta
        rec = {"k": "cortex_llamada", "tick_foto": tick, "tick_llegada": llega,
               "edad_al_nacer": (llega - tick) if llega is not None else None,
               "tick": tick, "relato_md5": h, "relato_bytes": len(texto),
               "n_llamada": self.n_llamadas}
        if not self.relato_enviado:
            rec["relato"] = texto          # entero UNA vez
            self.relato_enviado = True
        # [D-0 punto 3] el parte que se mando, para poder cotejarlo
        pt = getattr(self, "ultimo_parte", "")
        # [D-B a] el parte ENTERO en CADA llamada. Son ~600 bytes; el D-0 solo
        # guardo el primero, se lo llevo el corte de cabeza y no hubo con que
        # cotejar ni uno.
        rec["parte_bytes"] = len(pt)
        rec["parte_md5"] = __import__("hashlib").md5(pt.encode()).hexdigest()
        rec["parte"] = pt
        rec.update(resp)
        props = []
        if resp.get("ok") and resp.get("propuestas") == []:
            self.llamadas_cero += 1
            rec["derecho_a_callar"] = True
        if resp.get("ok") and resp.get("propuestas") is not None:
            for p in resp["propuestas"]:
                props.append(self._traduce(p, e, ofrecidas, tick))
        # [L-6 arreglo] el filtro de caducidad va ANTES de escribir el
        # registro: en la L-6 los dos campos nuevos se escribieron antes del
        # bucle que pone `sigue_valida` y salieron a cero en el diario (los
        # totales del resumen si eran buenos). El detalle hubo que
        # reconstruirlo cruzando la traduccion con los `cortex_tic`.
        # [L-5 arreglo] la vida se cuenta desde que la propuesta NACE (cuando
        # vuelve la respuesta), no desde la foto. Con edades medidas de 63-71
        # tics y VIDA_TICS=60, contarla desde la foto la hacia nacer muerta.
        nace = llega if llega is not None else tick
        est = foto["estado"]() if foto.get("estado") else None
        if est is not None:
            est["hand_foto"] = foto.get("hand_foto")
        vivas = []
        for p in props:
            if p.get("receta") is None:
                continue
            if p.get("dormida_al_nacer"):
                p["receta"] = {"tipo": (p.get("objetivo_nombrado") or {})
                               .get("tipo", "?")}
            # [S] la que nace DORMIDA no se juzga por si su candidato esta
            # vivo: precisamente no lo esta, y por eso duerme. Lo que si se le
            # mira —a todas— es si el MOTIVO sigue en pie.
            ok, por = (True, None) if p.get("dormida_al_nacer") \
                else _sigue_valida(p, est)
            if ok:
                # [L-7 §4] ademas de la receta, el MOTIVO
                mal, por2 = _motivo_caducado(p, est)
                if mal:
                    ok, por = False, por2
                    p["caducada_motivo"] = True
                    self.caducadas_motivo += 1
            p["sigue_valida"] = ok
            if not ok:
                p["caducada_por"] = por
                self.caducadas_mundo += 1
                continue
            self.nacidas_vivas += 1
            self.n_prop += 1
            vivas.append({"id": self.n_prop, "obj": p.get("objetivo_nombrado") or {},
                          "nombre0": p["nombre"], "receta0": p["receta"],
                          "nace": nace, "caduca": nace + VIDA_TICS,
                          "accion": p["accion"], "motivo": p["motivo"],
                          "clase": p["clase"], "regla": p.get("regla"),
                          "dormida": 0, "cuerpo": 0, "casilla": 0,
                          "vetada": 0, "gano": 0})
        with self.lock:
            # [D-0] las que siguen vivas cuando llega la hornada nueva tambien
            # se entierran: si no, su desenlace no llegaria nunca al parte.
            for x in self.vivas:
                self._entierra(x)
            self.vivas = vivas
        rec["traduccion"] = [{k: v for k, v in p.items() if k != "receta"}
                             for p in props]
        for p in props:
            self.n_propuestas += 1
            if p.get("receta") is None or p.get("sigue_valida") is False:
                # IMPOSIBLE, o traducida pero que el mundo ya no admite: para
                # el cortex las dos son lo mismo, "no se podia hacer ahi".
                self.historia.append({"accion": p.get("accion"),
                                      "suerte": "no_se_podia", "fila": None})
        rec["nacidas_vivas"] = sum(1 for p in props if p.get("sigue_valida"))
        rec["caducadas_por_el_mundo"] = sum(
            1 for p in props if p.get("sigue_valida") is False)
        self._sello(rec)
        # [D-B b] una linea del libro por llamada. El libro entero se reemite
        # cada 100 tics junto a `static_map`/`catalogo`, que son los registros
        # que SI sobreviven al corte por la cabeza.
        cl = collections.Counter(t.get("clase")
                                 for t in (rec.get("traduccion") or []))
        self.libro.append({"f": tick, "l": llega, "n": self.n_llamadas,
                           "D": cl.get("DENTRO", 0), "F": cl.get("FUERA", 0),
                           "I": cl.get("IMPOSIBLE", 0),
                           "c": int(bool(rec.get("derecho_a_callar"))),
                           "h": rec["parte_md5"][:8], "v": self.victorias})

    def _llama(self, texto, tick):
        if not self.ep or not self.modelo:
            self.callado = True
            return {"ok": False, "motivo": "sin sidecar o sin BEDROCK_MODEL"}
        # [S-2] FRENO 1: numero de llamadas
        if self.n_llamadas >= TOPE_LLAMADAS:
            if not self.callado:
                self.callado = True
                self.freno = {"cual": "llamadas", "tick": tick,
                              "llamadas": self.n_llamadas, "tope": TOPE_LLAMADAS}
                self.log({"k": "cortex_freno", "tick": tick, "cual": "llamadas",
                          "llamadas": self.n_llamadas, "tope": TOPE_LLAMADAS,
                          "efecto": "el cortex se calla; la partida se descarta"})
            return {"ok": False, "motivo": "freno propio: tope de llamadas"}
        # [S-2] FRENO 2: gasto del asiento
        if self.gasto_visto is not None and self.gasto_visto > TOPE_GASTO_USD:
            if not self.callado:
                self.callado = True
                self.freno = {"cual": "gasto", "tick": tick,
                              "gasto_usd": self.gasto_visto,
                              "tope": TOPE_GASTO_USD}
                self.log({"k": "cortex_freno", "tick": tick, "cual": "gasto",
                          "gasto_usd": self.gasto_visto, "tope": TOPE_GASTO_USD,
                          "efecto": "el cortex se calla; la partida se descarta"})
            return {"ok": False, "motivo": "freno propio: tope de gasto"}
        url = f"{self.ep.rstrip('/')}/model/{self.modelo}/invoke"
        bloques = []
        if self.manual:
            b = {"type": "text", "text": f"{CABECERA}\n\n{self.manual}\n\n---\n\n"}
            if self.usa_cache:
                b["cache_control"] = {"type": "ephemeral"}
            bloques.append(b)
        # [D-0] el parte va DELANTE de la escena y FUERA del bloque cacheado
        # (cambia en cada llamada; meterlo en el bloque del manual invalidaria
        # la cache en todas).
        pt = (parte(self.historia, self.n_propuestas, self.n_hechas)
              if PARTE_ON else "")
        self.ultimo_parte = pt
        bloques.append({"type": "text", "text": pt + texto + "\n\n" + ESQUEMA_TXT})
        cuerpo = {"anthropic_version": "bedrock-2023-05-31",
                  "max_tokens": MAX_TOKENS, "system": SISTEMA,
                  "messages": [{"role": "user", "content": bloques}]}
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(
                url, data=json.dumps(cuerpo).encode(), method="POST",
                headers={"Content-Type": "application/json",
                         "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as rr:
                crudo = rr.read(65536).decode("utf-8", "replace")
                ms = round((time.perf_counter() - t0) * 1000.0, 1)
                self.n_llamadas += 1
                self.lat.append(ms)
                self.fallos = 0
                self.cache_probada = True
                d = json.loads(crudo)
                u = d.get("usage") or {}
                # [L-5 arreglo] `u` se leia antes de existir: UnboundLocalError
                # en las 5 llamadas de la L-5, todas contadas como fallo.
                self.lat_n.append((self.n_llamadas, ms,
                                   (u.get("cache_read_input_tokens") or 0)))
                out = {"ok": True, "codigo": rr.status, "ms": ms,
                       # [S-2] TODAS las cabeceras, no solo las dos que el doc
                       # promete: si el sidecar desplegado devuelve algo mas
                       # (un `billed_cost_usd`, por ejemplo, que NO existe en
                       # esta version del paquete), queda capturado igual.
                       "cabeceras": {k: v for k, v in rr.headers.items()},
                       "spend_usd": rr.headers.get("X-Coworld-Spend-Usd"),
                       "spend_limit_usd": rr.headers.get("X-Coworld-Spend-Limit-Usd"),
                       "usage": u, "cache_pedida": self.usa_cache,
                       # [L-5] el desglose que pide el encargo
                       "tok_entrada_fresca": u.get("input_tokens"),
                       "tok_cache_lectura": u.get("cache_read_input_tokens"),
                       "tok_cache_escritura": u.get("cache_creation_input_tokens"),
                       "tok_salida": u.get("output_tokens"),
                       "stop_reason": d.get("stop_reason")}
                # [L-5] la PRIMERA respuesta entera, para tener un fixture real
                if self.n_llamadas == 1:
                    out["cuerpo_crudo_primera"] = crudo[:4000]
                # [S-2] el freno de gasto lee esta cabecera. Si algun dia
                # dejara de llegar, el freno se quedaria mirando un valor que
                # no cambia y NO protegeria nada — el error de bulto que esta
                # casa lleva cazado varias veces. Asi que si falta, lo DICE.
                try:
                    self.gasto_visto = float(out["spend_usd"])
                except (TypeError, ValueError):
                    if not self.aviso_sin_cabecera:
                        self.aviso_sin_cabecera = True
                        self.log({"k": "cortex_freno_ciego", "tick": tick,
                                  "cabecera": "X-Coworld-Spend-Usd",
                                  "valor": out.get("spend_usd"),
                                  "cabeceras_vistas": sorted(out.get("cabeceras") or {}),
                                  "efecto": "el freno de gasto NO protege; "
                                            "solo queda el de 150 llamadas"})
                txt = "".join(c.get("text", "") for c in (d.get("content") or [])
                              if c.get("type") == "text")
                out["texto"] = txt[:2000]
                try:
                    i, j = txt.find("{"), txt.rfind("}")
                    ps = json.loads(txt[i:j + 1])["propuestas"][:3]
                    out["propuestas"] = [{"accion": str(p.get("accion", ""))[:300],
                                          "motivo": str(p.get("motivo", ""))[:400]}
                                         for p in ps]
                except Exception as ex:
                    out["propuestas"] = None
                    out["json_malo"] = repr(ex)[:160]
                return out
        except urllib.error.HTTPError as ex:
            ms = round((time.perf_counter() - t0) * 1000.0, 1)
            cuer = ex.read(2048).decode("utf-8", "replace")[:800]
            # ¿la rechaza el sidecar por el cache_control? se reintenta SIN cache
            # UNA vez y no cuenta como fallo (queda declarado en el diario).
            if (not self.cache_probada and self.usa_cache
                    and 400 <= ex.code < 500):
                self.usa_cache = False
                self.cache_probada = True
                self.log({"k": "cortex_cache", "tick": tick, "codigo": ex.code,
                          "cuerpo": cuer[:300],
                          "decision": "el sidecar NO acepta cache_control: "
                                      "se sigue SIN cache"})
                return self._llama(texto, tick)
            self.fallos += 1
            if self.fallos >= FALLOS_PARA_CALLAR:
                self.callado = True
            return {"ok": False, "codigo": ex.code, "ms": ms, "cuerpo": cuer,
                    "retry_after_ms": (ex.headers.get("Retry-After-Ms")
                                       if ex.headers else None),
                    "fallos_seguidos": self.fallos, "callado": self.callado}
        except Exception as ex:
            ms = round((time.perf_counter() - t0) * 1000.0, 1)
            self.fallos += 1
            if self.fallos >= FALLOS_PARA_CALLAR:
                self.callado = True
            return {"ok": False, "ms": ms, "error": repr(ex)[:300],
                    "fallos_seguidos": self.fallos, "callado": self.callado}

    # ── el traductor ───────────────────────────────────────────────────────
    def _traduce(self, p, e, ofrecidas, tick):
        """[L-7] EL ORDEN, declarado. Las reglas emparejadas con el relato van
        PRIMERO porque son mas precisas que el calce de frase: el relato ofrece
        el candidato `coger` con la frase literal "coger" (relator_t5.py:110-165
        no tiene rama para el, cae en `return n`), asi que un calce de frase
        mandaba CUALQUIER "coger <lo que sea>" a `coger`. Es lo que paso en la
        L-6 con "coger la red del suelo" estando la red a varias casillas.

        Clases:
          DENTRO — la propuesta nombra un candidato VIVO del cuerpo.
          FUERA  — la propuesta nombra una casilla real (o la casilla de un
                   objeto que se ve): receta `ir`, que el decisor ya imagina.
          IMPOSIBLE — ni una cosa ni la otra.
        """
        acc = p.get("accion", "")
        na = _norm(acc)
        out = {"accion": acc, "motivo": p.get("motivo", "")}
        reglas = (("atacar", _regla_atacar), ("hermano", _regla_hermano),
                  ("usar", _regla_usar), ("vestir", _regla_vestir),
                  ("objeto", _regla_objeto), ("centro", _regla_centro),
                  ("rumbo", _regla_rumbo), ("esperar", _regla_esperar))
        for nom, f in reglas:
            r = f(na, e)
            if r is None:
                continue
            clase, quien, marca, porque = r
            out["regla"] = nom
            if marca:
                out["objetivo_nombrado"] = marca
            if clase == "OBJETIVO":
                # [S] traducible pero SIN candidato vivo ahora: guarda el
                # objetivo y que la atadura lo intente cada tic.
                out.update(clase="DENTRO", nombre=quien, receta={},
                           objetivo_nombrado=marca, dormida_al_nacer=True)
                if marca.get("inicia"):
                    self.inicia_ataque += 1
                    out["inicia_ataque"] = True
                self.clases["DENTRO"] += 1
                return out
            if clase == "DENTRO" and quien:
                rec = (e.get("_recetas_vivas") or {}).get(quien)
                if rec is None and quien == ((e.get("_golpe_hermano") or {})
                                             .get("nombre")):
                    rec = e.get("_receta_golpe_hermano")
                if rec is not None:
                    out.update(clase="DENTRO", nombre=quien, receta=rec,
                               objetivo_nombrado=_objetivo_de(quien, e))
                    self.clases["DENTRO"] += 1
                    return out
                porque = porque or "el candidato ya no esta vivo"
            elif clase == "CASILLA" and quien:
                # la casilla de un OBJETO guarda el objeto, no la casilla: si
                # se lo llevan, el motivo ha caducado y hay que verlo.
                obj = dict(marca or {})
                obj.setdefault("tipo", "casilla")
                obj["pos"] = tuple(quien)
                out.update(clase="FUERA",
                           nombre=f"_CX_ir_{quien[0]}_{quien[1]}",
                           objetivo_nombrado=obj,
                           receta={"tipo": "ir", "destino": tuple(quien),
                                   "cuerpos": e["_cuerpos"],
                                   "recoger": e["_objetos"].get(tuple(quien))})
                self.clases["FUERA"] += 1
                return out
            out.update(clase="IMPOSIBLE", nombre=None, receta=None,
                       motivo_imposible=(porque or f"la regla {nom} no cuaja"))
            self.clases["IMPOSIBLE"] += 1
            return out
        # calce de frase con lo que el relato OFRECIO, palabra por palabra
        mejor = None
        for nombre, frase in ofrecidas.items():
            nf = _norm(frase)
            if not nf or len(nf) < 8:      # [L-7] nada de calces de una palabra
                continue
            if nf in na or (len(na) > 12 and na in nf):
                if mejor is None or len(nf) > len(_norm(ofrecidas[mejor])):
                    mejor = nombre
        if mejor is not None:
            rec = (e.get("_recetas_vivas") or {}).get(mejor)
            if rec is None and mejor == ((e.get("_golpe_hermano") or {})
                                         .get("nombre")):
                rec = e.get("_receta_golpe_hermano")
            if rec is not None:
                out.update(clase="DENTRO", nombre=mejor, receta=rec,
                           regla="frase",
                           objetivo_nombrado=_objetivo_de(mejor, e))
                self.clases["DENTRO"] += 1
                return out
        # SOLO lo que de verdad es una casilla se traduce a casilla
        m = RX_CASILLA.search(acc)
        if m:
            dest = (int(m.group(1)), int(m.group(2)))
            if 0 <= dest[0] < 48 and 0 <= dest[1] < 48:
                out.update(clase="FUERA", nombre=f"_CX_ir_{dest[0]}_{dest[1]}",
                           receta={"tipo": "ir", "destino": dest,
                                   "cuerpos": e["_cuerpos"],
                                   "recoger": e["_objetos"].get(dest)},
                           regla="casilla",
                           objetivo_nombrado={"tipo": "casilla", "pos": dest})
                self.clases["FUERA"] += 1
                return out
        out.update(clase="IMPOSIBLE", nombre=None, receta=None,
                   motivo_imposible="ni nombra nada del mundo ni una casilla")
        self.clases["IMPOSIBLE"] += 1
        return out

    # ── lo que ve el bucle del juego ───────────────────────────────────────
    def extra(self, tick):
        """[S] Devuelve las propuestas VIVAS. Ya no traen receta: traen su
        objetivo, y quien las ata es la politica, tic a tic."""
        with self.lock:
            v = [x for x in self.vivas if x["caduca"] > tick]
            if len(v) != len(self.vivas):
                for x in self.vivas:
                    if x["caduca"] <= tick:
                        self._entierra(x)
                self.vivas = v
        return v

    def _sello(self, rec):
        """[D-B c] numera el registro con el orden REAL de la cola."""
        with self.seq_lock:
            self.seq += 1
            rec["seq"] = self.seq
        self.log(rec)

    def _desenlace(self, v):
        """[D-0] Como acabo una propuesta, en las tres clases del encargo."""
        if v.get("gano"):
            self.n_hechas += 1
            return {"accion": v.get("accion"), "suerte": "hizo", "fila": None}
        gj = v.get("gana") or {}
        pj = v.get("pierde") or {}
        if gj and sum(gj.values()) >= sum(pj.values()):
            # [D-C] el cuerpo YA la ofrecia y la eligio mas veces de las que la
            # dejo pasar: cuenta como hecha, y se dice frente a que gano.
            self.n_hechas += 1
            fr = v.get("frente") or {}
            unica = max(gj, key=gj.get) == "_UNICA"
            return {"accion": v.get("accion"), "suerte": "ya_iba",
                    "fila": None if unica else max(gj, key=gj.get),
                    "frente": None if unica else
                              (max(fr, key=fr.get) if fr else None)}
        if v.get("cuerpo") or v.get("casilla"):
            # estuvo en la mesa y no gano: manda la fila que mas la separo
            fila = max(pj, key=pj.get) if pj else None
            return {"accion": v.get("accion"), "suerte": "no_compro",
                    "fila": fila}
        return {"accion": v.get("accion"), "suerte": "no_se_podia", "fila": None}

    def libro_compacto(self, tick):
        """[D-B b] TODAS las llamadas hasta ahora, en una linea por llamada.
        f=tic de foto, l=tic de llegada, n=numero de llamada, D/F/I=clases,
        c=callo, h=hash corto del parte, v=victorias acumuladas."""
        return {"k": "cortex_libro", "tick": tick, "n": len(self.libro),
                "victorias": self.victorias, "hechas": self.n_hechas,
                "propuestas": self.n_propuestas,
                "callo": self.llamadas_cero, "libro": list(self.libro)}

    def _entierra(self, v):
        """La vida entera de una propuesta, al morir: es donde se ve si estuvo
        dormida todo el rato o si llego a pisar la mesa."""
        self.tics_dormida += v["dormida"]
        self.tics_cuerpo += v["cuerpo"]
        self.tics_casilla += v["casilla"]
        self.tics_vetada += v["vetada"]
        if v["cuerpo"] or v["casilla"]:
            self.atadas_alguna_vez += 1
        else:
            self.dormidas_hasta_caducar += 1
        self.historia.append(self._desenlace(v))
        self._sello({"k": "cortex_muere", "id": v["id"], "nace": v["nace"],
                  "caduca": v["caduca"], "clase": v["clase"],
                  "regla": v["regla"], "obj": _jsonable(v["obj"]),
                  "accion": v["accion"], "motivo": v["motivo"],
                  "tics": {"dormida": v["dormida"], "cuerpo": v["cuerpo"],
                           "casilla": v["casilla"], "vetada": v["vetada"],
                           "gano": v["gano"]},
                  "pierde": v.get("pierde") or {},
                  "gana": v.get("gana") or {}, "frente": v.get("frente") or {},
                  "desenlace": self.historia[-1]["suerte"]})

    def resumen(self, tick):
        lat = sorted(self.lat)
        return {"k": "cortex_resumen", "tick": tick,
                "llamadas": self.n_llamadas, "callado": self.callado,
                "fallos_seguidos": self.fallos,
                "lat_ms": ({"n": len(lat), "mediana": lat[len(lat) // 2],
                            "p95": lat[int(len(lat) * 0.95)], "max": lat[-1]}
                           if lat else None),
                "citas_saltadas": self.citas_saltadas,
                "en_vuelo": self.en_vuelo,
                "lat_por_llamada": self.lat_n[-40:],
                "clases": dict(self.clases),
                "caducadas_mundo": self.caducadas_mundo,
                "caducadas_por_el_motivo": self.caducadas_motivo,
                "empates_al_cuerpo": self.empates,
                "tics_con_vetada": self.tics_con_vetada,
                "atadura": {"atadas_alguna_vez": self.atadas_alguna_vez,
                            "dormidas_hasta_caducar": self.dormidas_hasta_caducar,
                            "tics_dormida": self.tics_dormida,
                            "tics_atada_al_cuerpo": self.tics_cuerpo,
                            "tics_atada_por_casilla": self.tics_casilla,
                            "tics_vetada": self.tics_vetada,
                            "tics_con_alguna_atada": self.tics_con_atada},
                "inicia_ataque": self.inicia_ataque,
                "llamadas_con_cero_propuestas": self.llamadas_cero,
                "entorno": entorno_efectivo(),
                "freno": self.freno, "gasto_visto": self.gasto_visto,
                "freno_gasto_ciego": self.aviso_sin_cabecera,
                "n_propuestas": self.n_propuestas, "n_hechas": self.n_hechas,
                "nacidas_vivas": self.nacidas_vivas,
                "victorias": self.victorias,
                "tics_con_viva": self.tics_con_viva,
                "cache": {"pedida": self.usa_cache, "probada": self.cache_probada},
                "spend": self.gasto}

    def pide_gasto(self):
        if not self.ep:
            return None
        try:
            with urllib.request.urlopen(self.ep.rstrip("/") + "/spend",
                                        timeout=TIMEOUT) as rr:
                self.gasto = json.loads(rr.read(2048).decode("utf-8", "replace"))
        except Exception as e:
            self.gasto = {"error": repr(e)[:200]}
        return self.gasto

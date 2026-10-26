"""[P5-5B · B3] Del JSON del consejero a la forma que el banco sabe juzgar.

En seco, coste cero. No toca el motor, ni la tabla, ni el decisor.

La forma del banco (P5-3) es una lista de tramos
`{"destino": (x,y)|None, "intencion": "ir"|"coger"|"usar"|"esperar",
  "esperar": N}`, y `forma.puntos_de_control` le pone el tic real de llegada a
cada uno (11 tics por casilla, mas la espera).

Aqui se traduce, y se CUENTA todo lo que no se puede traducir, que es la mitad
del interes de la medida.
"""
from __future__ import annotations
import collections, json, re, unicodedata

SOLIDOS = ("#", "F", "R")
MAX_TRAMOS = 4
INTENCIONES = ("ir", "coger", "usar", "esperar")
DIMS = ("vida", "manos", "vinculo")

# nombre en llano -> id del mundo (el vocabulario del relator, invertido)
NOMBRE_A_ID = {
    "espada": "sword", "lanza": "spear", "arco": "bow", "cuchillos": "knives",
    "cuchillo": "knives", "cerbatana": "blowgun", "red": "net",
    "botiquin": "first_aid", "racion": "rations", "raciones": "rations",
    "mochila": "backpack", "camuflaje": "camouflage", "flechas": "arrows",
    "flecha": "arrows", "dardos": "darts", "dardo": "darts",
    # y los ids, por si los escribe en ingles
    "sword": "sword", "spear": "spear", "bow": "bow", "knives": "knives",
    "blowgun": "blowgun", "net": "net", "first_aid": "first_aid",
    "rations": "rations", "backpack": "backpack", "camouflage": "camouflage",
    "arrows": "arrows", "darts": "darts",
}
_COORD = re.compile(r"[\(\[]\s*(\d+)\s*[,; ]\s*(\d+)\s*[\)\]]")


def llano(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def saca_json(texto):
    """El JSON del modelo, aunque venga con vallas de markdown o con ruido."""
    t = (texto or "").strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
        t = re.sub(r"\s*```\s*$", "", t)
    try:
        return json.loads(t), None
    except Exception:
        pass
    i, j = t.find("{"), t.rfind("}")
    if i >= 0 and j > i:
        try:
            return json.loads(t[i:j + 1]), None
        except Exception as ex:
            return None, f"json invalido: {ex}"
    return None, "no hay objeto JSON en la respuesta"


def casilla_valida(p, filas):
    n = len(filas)
    return (isinstance(p, tuple) and len(p) == 2
            and all(isinstance(x, int) for x in p)
            and 0 <= p[0] < n and 0 <= p[1] < n
            and filas[p[1]][p[0]] not in SOLIDOS)


def destino_de(d, suelo, pos, filas, cuenta):
    """(casilla|None, motivo_de_fallo|None). `suelo` es [{'id','pos'}]."""
    if d is None:
        return None, None
    if isinstance(d, (list, tuple)) and len(d) == 2:
        try:
            p = (int(d[0]), int(d[1]))
        except Exception:
            cuenta["destino ilegible"] += 1
            return None, "destino ilegible"
        if not casilla_valida(p, filas):
            cuenta["casilla fuera o solida"] += 1
            return None, "casilla fuera del mapa o solida"
        return p, None
    if isinstance(d, str):
        t = llano(d)
        m = _COORD.search(t)
        if m:
            p = (int(m.group(1)), int(m.group(2)))
            if not casilla_valida(p, filas):
                cuenta["casilla fuera o solida"] += 1
                return None, "casilla fuera del mapa o solida"
            return p, None
        ids = {NOMBRE_A_ID[k] for k in NOMBRE_A_ID if re.search(rf"\b{k}\b", t)}
        if not ids:
            cuenta["objeto sin nombre conocido"] += 1
            return None, "no nombra ni casilla ni objeto conocido"
        cand = [it for it in suelo if it.get("id") in ids and it.get("pos")]
        if not cand:
            cuenta["objeto no esta en el suelo"] += 1
            return None, "el objeto nombrado no esta en el suelo de la escena"
        p = tuple(min(cand, key=lambda it: cheb(pos, tuple(it["pos"])))["pos"])
        if not casilla_valida(p, filas):
            cuenta["casilla fuera o solida"] += 1
            return None, "la casilla del objeto es solida"
        return p, None
    cuenta["destino ilegible"] += 1
    return None, "destino ilegible"


def traduce(texto, escena, filas, cuenta=None):
    """(formas, informe). Cada forma es [tramos] lista para el banco."""
    c = cuenta if cuenta is not None else collections.Counter()
    inf = {"parsea": False, "callar": None, "n_formas": 0, "fallos": []}
    obj, err = saca_json(texto)
    if obj is None:
        c["respuestas que no parsean"] += 1
        inf["fallos"].append(err)
        return [], inf
    inf["parsea"] = True
    c["respuestas que parsean"] += 1
    if not isinstance(obj, dict):
        c["json no es un objeto"] += 1
        inf["fallos"].append("el JSON no es un objeto")
        return [], inf
    inf["callar"] = bool(obj.get("callar"))
    brutas = obj.get("formas")
    if brutas is None:
        brutas = obj.get("propuestas") or []      # por si responde el esquema viejo
    if not isinstance(brutas, list):
        c["formas no es una lista"] += 1
        return [], inf
    pos0 = tuple(escena["pos"])
    suelo = escena.get("suelo") or []
    salida = []
    for fo in brutas:
        if not isinstance(fo, dict):
            c["forma no es un objeto"] += 1
            continue
        trs = fo.get("tramos")
        if not isinstance(trs, list) or not trs:
            c["forma sin tramos"] += 1
            continue
        c["formas propuestas"] += 1
        if len(trs) > MAX_TRAMOS:
            c["formas de mas de cuatro tramos"] += 1
            trs = trs[:MAX_TRAMOS]
        buenos, pos = [], pos0
        roto = False
        for tr in trs:
            if not isinstance(tr, dict):
                c["tramo no es un objeto"] += 1
                roto = True
                break
            c["tramos propuestos"] += 1
            inten = llano(tr.get("intencion") or "")
            if inten not in INTENCIONES:
                c["intencion desconocida"] += 1
                inten = "ir" if tr.get("destino") is not None else "esperar"
            d, fallo = destino_de(tr.get("destino"), suelo, pos, filas, c)
            if fallo:
                inf["fallos"].append(fallo)
                roto = True
                break
            if d is None and inten == "ir":
                inten = "esperar"          # «quedarse» dicho como ir a ningun sitio
            esp = tr.get("esperar")
            try:
                esp = int(esp) if esp is not None else 0
            except Exception:
                esp = 0
            if inten == "esperar" and esp <= 0:
                esp = 11                   # una espera sin numero: un paso
            nuevo = {"destino": d, "intencion": inten,
                     "esperar": esp if inten == "esperar" else 0,
                     "_mitad": {k: tr.get(k) for k in DIMS},
                     "_por": tr.get("por"), "_porque": tr.get("porque")}
            # ¿estan las DOS mitades?
            mundo_ok = (inten in INTENCIONES)
            emo_ok = (all(tr.get(k) in ("+", "0", "-") for k in DIMS)
                      and bool(tr.get("por")))
            c["tramos con la mitad del mundo"] += int(mundo_ok)
            c["tramos con la mitad emocional"] += int(emo_ok)
            c["tramos con las dos mitades"] += int(mundo_ok and emo_ok)
            if d is not None:
                pos = d
            buenos.append(nuevo)
        if roto or not buenos:
            c["formas intraducibles"] += 1
            continue
        c["formas construidas"] += 1
        salida.append({"tramos": buenos, "final": fo.get("final")})
    inf["n_formas"] = len(salida)
    return salida, inf


def solo_tramos(forma):
    """Lo que el banco consume: sin las mitades emocionales."""
    return [{"destino": t["destino"], "intencion": t["intencion"],
             "esperar": t["esperar"]} for t in forma["tramos"]]


def de_propuestas(texto, escena, filas, cuenta=None):
    """Brazo CASILLAS: las propuestas de un paso del cuatro, a formas de un
    tramo. El texto de la accion se busca como casilla o como objeto."""
    c = cuenta if cuenta is not None else collections.Counter()
    inf = {"parsea": False, "callar": None, "n_formas": 0, "fallos": []}
    obj, err = saca_json(texto)
    if obj is None or not isinstance(obj, dict):
        c["respuestas que no parsean"] += 1
        inf["fallos"].append(err or "el JSON no es un objeto")
        return [], inf
    inf["parsea"] = True
    c["respuestas que parsean"] += 1
    props = obj.get("propuestas") or []
    inf["callar"] = (len(props) == 0)
    pos0 = tuple(escena["pos"])
    suelo = escena.get("suelo") or []
    salida = []
    for p in props if isinstance(props, list) else []:
        if not isinstance(p, dict):
            continue
        c["formas propuestas"] += 1
        c["tramos propuestos"] += 1
        acc = p.get("accion") or ""
        d, fallo = destino_de(acc, suelo, pos0, filas, c)
        if fallo:
            inf["fallos"].append(fallo)
            c["formas intraducibles"] += 1
            continue
        inten = "ir" if d is not None else "esperar"
        c["tramos con la mitad del mundo"] += 1
        # el esquema del cuatro NO tiene mitad emocional, por construccion
        c["formas construidas"] += 1
        salida.append({"tramos": [{"destino": d, "intencion": inten,
                                   "esperar": 0 if d is not None else 11,
                                   "_mitad": {k: None for k in DIMS},
                                   "_por": None, "_porque": p.get("motivo")}],
                       "final": p.get("motivo")})
    inf["n_formas"] = len(salida)
    return salida, inf

"""EL PARTE E2 — ojos compartidos, version 1. [P6-3, 26-sep-2026]

ARCHIVO NUEVO. No toca `paintball/alma/parte.py` (congelado en CONGELADO.md),
ni ningun otro archivo del paper cinco. El emisor y el parser viven aqui.

QUE ANADE SOBRE E1
  E1 decia como estoy YO. E2 dice ademas QUE VEO: los rivales y los recursos.
  El motivo esta medido en P6-2: la pareja va a distancia mediana 2 y aun asi
  cada uno ve casillas que el otro no en el 87 % de los tics; hay 488 episodios
  en que uno ve a un armado que tiene al otro a tiro y el otro no lo ve, y
  1.954 ocasiones de objeto util que a uno le falta y el otro esta mirando.
  Y el canal va al 13 % de su capacidad.

FORMATO (ASCII imprimible, <= 120 caracteres, determinista dado el estado)

  E2 P<slot> t<tick> <x>,<y> h<hp> v<0|1> b<n> a<0|1>[ s<sl>][ <ax>,<ay>]
     [ R<rival><rival>...][ I<recurso><recurso>...]

  LA CABEZA es la de E1 palabra por palabra, con la marca cambiada. Asi el
  cuerpo del parte sigue siendo el mismo hecho certificado de siempre.

  <rival>  = <slot>:<x>,<y><arma><rumbo>
      slot   el asiento, tal cual
      x,y    su casilla AHORA (hecho de la obs)
      arma   UNA letra del catalogo, leida de `mundo.items` ordenado
             (PROHIBIDO cablearla: CLAUDE.md). `-` si va con las manos vacias
      rumbo  N E S W y n=NE e=SE s=SW w=NW, del MOVIMIENTO observado entre las
             dos ultimas veces que lo vi; `.` si no se movio o no consta.
             DECLARADO: el mundo NO publica hacia donde APUNTA nadie
             (`protocol_player.md` no trae `facing`), asi que «hacia donde
             apunta» NO se puede mandar. Se manda hacia donde SE MUEVE, que
             es lo unico cierto, y se dice que es eso.

  <recurso> = <tipo><x>,<y>
      tipo   la misma letra del catalogo

ORDEN, de mas a menos importante (lo que sobrevive al corte de 120):
  rivales   1) armado y con mi hermano YA a su alcance
            2) armado y con mi hermano a alcance + 3 (le da tiempo a llegar)
            3) armado, por distancia a mi hermano
            4) desarmado, por distancia a mi hermano
  recursos  1) botiquin si su parte dijo b0
            2) arma  3) raciones  4) mochila  5) municion  6) gear menor
            y dentro de cada clase, el mas cercano a EL primero

  La posicion del hermano sale de SU parte (hecho cierto, con caducidad). Sin
  parte suyo se ordena por distancia a MI, y se declara en el diario.

LIMITE: 120 caracteres (el mismo `sanitizeTalk` de siempre) y UN mensaje por
segundo y agente. `CADA = 25` tics: 25 > 24 garantiza como mucho uno por
segundo aunque el reloj tiemble un tic, y casi duplica el ritmo de E1 (48).
"""
from __future__ import annotations

import re
import string

MARCA = "E2"
CADA = 25            # tics entre partes. 25 > tick_rate(24) => nunca dos en
                     # el mismo segundo, ni con un tic de temblor.
CADUCIDAD = 96       # la de E1: dos partes perdidos (de E1; aqui son casi 4)
MAX_CHARS = 120

RUMBOS = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W",
          (1, -1): "n", (1, 1): "e", (-1, 1): "s", (-1, -1): "w"}

_CABEZA = (r"^E2 P(\d+) t(\d+) (\d+),(\d+) h(\d+(?:\.\d+)?) v([01]) b(\d+) "
           r"a([01])(?: s(\d+))?(?: (\d+),(\d+))?")
_RE_CAB = re.compile(_CABEZA)
_RE_RIV = re.compile(r"(\d+):(\d+),(\d+)([A-Za-z-])([NESWnesw.])")
_RE_REC = re.compile(r"([A-Za-z])(\d+),(\d+)")


# ── el alfabeto del catalogo: LEIDO del mundo, nunca cableado ──────────────
def alfabeto(mundo) -> dict:
    """id de objeto -> una letra. Deterministico: el catalogo ordenado."""
    ids = sorted((mundo.items or {}).keys())
    letras = string.ascii_lowercase + string.ascii_uppercase
    assert len(ids) <= len(letras), ("catalogo mas grande que el alfabeto",
                                     len(ids))
    return {i: letras[k] for k, i in enumerate(ids)}


def inverso(mundo) -> dict:
    return {v: k for k, v in alfabeto(mundo).items()}


def ascii_limpio(texto: str) -> bool:
    return len(texto) <= MAX_CHARS and all(0x20 <= ord(c) <= 0x7E for c in texto)


class Ojeador:
    """La memoria minima del EMISOR: donde vi a cada rival la vez anterior.

    Solo sirve para el rumbo. No decide nada, no entra en ninguna fila.
    """

    def __init__(self):
        self.ultima = {}          # slot -> (tick, (x, y))

    def rumbo(self, slot, pos, tick):
        ant = self.ultima.get(slot)
        self.ultima[slot] = (tick, tuple(pos))
        if ant is None or ant[1] == tuple(pos):
            return "."
        dx = 0 if pos[0] == ant[1][0] else (1 if pos[0] > ant[1][0] else -1)
        dy = 0 if pos[1] == ant[1][1] else (1 if pos[1] > ant[1][1] else -1)
        return RUMBOS.get((dx, dy), ".")


# ── clases de recurso, leidas del mundo ────────────────────────────────────
def clase_de(mundo, iid: str) -> str:
    it = (mundo.items or {}).get(iid)
    if iid == mundo.id_botiquin:
        return "botiquin"
    if iid in (mundo.id_raciones or []):
        return "raciones"
    if iid == mundo.id_mochila:
        return "mochila"
    if iid in (getattr(mundo, "ammo_ids", None) or ()):
        return "municion"
    if it is not None and getattr(it, "kind", "") in ("ikMelee", "ikRanged",
                                                      "ikThrown"):
        return "arma"
    if iid in (mundo.id_camuflaje, mundo.id_red):
        return "gear"
    return "otro"


def _alcance(mundo, mano) -> float:
    if not mano or mano == "none":
        return 0.0
    it = (mundo.items or {}).get(mano)
    return float(getattr(it, "range", 0) or 0) if it else 0.0


def _cheb(a, b) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


ORDEN_CLASE = {"botiquin": 1, "arma": 2, "raciones": 3, "mochila": 4,
               "municion": 5, "gear": 6, "otro": 9}


def emite(obs: dict, tick: int, mundo, mem, ventana_ticks: int,
          ojeador: Ojeador, parte_hermano=None, detalle=None) -> str:
    """El parte E2. Determinista dado (obs, tick, memoria, ojeador).

    `parte_hermano` es el ultimo parte FRESCO del hermano (dict del parser) o
    None: de ahi salen su posicion y su `b<n>` para ordenar. `detalle` es un
    dict opcional que se rellena con lo que entro y lo que se quedo fuera,
    para el diario.
    """
    you = obs.get("you") or {}
    pos = tuple(you.get("pos") or (0, 0))
    hp = float(you.get("hp") or 0.0)
    ven = any((e.get("id") or "").startswith("poison")
              for e in (you.get("effects") or []))
    bot = 0
    for s in (you.get("pack") or []):
        if s and s.get("id") == mundo.id_botiquin:
            bot += int(s.get("n") or 1)
    # agresor: identico a E1 (la entrada mas reciente de la ventana S-7)
    agr, agr_sl = 0, None
    mejor = None
    for sl, e in (getattr(mem, "agresores", None) or {}).items():
        if tick - e["ultimo"] > ventana_ticks:
            continue
        clave = (e["ultimo"], e["dano"], sl)
        if mejor is None or clave > mejor[0]:
            mejor = (clave, sl)
    if mejor is not None:
        agr, agr_sl = 1, mejor[1]
    cabeza = (f"{MARCA} P{mundo.slot} t{tick} {pos[0]},{pos[1]} "
              f"h{hp:g} v{int(ven)} b{bot} a{agr}")
    vis = obs.get("visible") or {}
    agentes = [a for a in (vis.get("agents") or []) if a.get("pos")]
    if agr:
        cabeza += f" s{agr_sl}"
        for a in agentes:
            if a.get("slot") == agr_sl:
                q = a["pos"]
                cabeza += f" {int(q[0])},{int(q[1])}"
                break

    AL = alfabeto(mundo)
    herm_pos = tuple(parte_hermano["pos"]) if parte_hermano else None
    herm_b0 = bool(parte_hermano) and int(parte_hermano.get("botiquin") or 0) == 0
    ref = herm_pos or pos

    # ── los rivales, ordenados por peligro PARA EL HERMANO ────────────────
    riv = []
    for a in agentes:
        sl = a.get("slot")
        if sl in (mundo.slot, mundo.teammate_slot):
            continue
        q = (int(a["pos"][0]), int(a["pos"][1]))
        mano = (a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) \
            else a.get("hand")
        rg = _alcance(mundo, mano)
        d = _cheb(q, ref)
        if rg > 0 and d <= rg:
            prio = (1, d)
        elif rg > 0 and d <= rg + 3:
            prio = (2, d)
        elif rg > 0:
            prio = (3, d)
        else:
            prio = (4, d)
        letra = AL.get(mano, "-") if rg > 0 else "-"
        riv.append((prio, f"{sl}:{q[0]},{q[1]}{letra}"
                          f"{ojeador.rumbo(sl, q, tick)}"))
    riv.sort(key=lambda x: x[0])

    # ── los recursos ──────────────────────────────────────────────────────
    rec = []
    for it in (vis.get("items") or []):
        q = it.get("pos")
        if not q:
            continue
        iid = it.get("id")
        cl = clase_de(mundo, iid)
        if cl == "otro":
            continue
        base = ORDEN_CLASE[cl]
        if cl == "botiquin" and herm_b0:
            base = 0
        rec.append(((base, _cheb((int(q[0]), int(q[1])), ref)),
                    f"{AL[iid]}{int(q[0])},{int(q[1])}"))
    rec.sort(key=lambda x: x[0])

    # ── el corte a 120, sin partir ningun token ───────────────────────────
    texto = cabeza
    dentro_r, dentro_i = [], []
    for _p, tok in riv:
        cab = " R" if not dentro_r else ""
        if len(texto) + len(cab) + len(tok) <= MAX_CHARS:
            texto += cab + tok
            dentro_r.append(tok)
        else:
            break
    for _p, tok in rec:
        cab = " I" if not dentro_i else ""
        if len(texto) + len(cab) + len(tok) <= MAX_CHARS:
            texto += cab + tok
            dentro_i.append(tok)
        else:
            break
    if detalle is not None:
        detalle.update({"largo": len(texto), "rivales_vistos": len(riv),
                        "rivales_dentro": len(dentro_r),
                        "recursos_vistos": len(rec),
                        "recursos_dentro": len(dentro_i),
                        "con_parte_hermano": bool(parte_hermano)})
    assert ascii_limpio(texto), ("E2 no sobrevive a sanitizeTalk", len(texto))
    return texto


def parsea(texto: str, mundo=None):
    """Parser ESTRICTO de E2. Devuelve dict o None.

    Ademas de los campos de E1 devuelve `rivales` y `recursos`. Con `mundo` se
    traducen las letras a ids del catalogo; sin el, se devuelve la letra.
    """
    if not isinstance(texto, str):
        return None
    m = _RE_CAB.match(texto)
    if m is None:
        return None
    g = m.groups()
    out = {"slot": int(g[0]), "t": int(g[1]), "pos": (int(g[2]), int(g[3])),
           "hp": float(g[4]), "veneno": g[5] == "1", "botiquin": int(g[6]),
           "agresor": g[7] == "1",
           "agresor_slot": int(g[8]) if g[8] is not None else None,
           "agresor_pos": ((int(g[9]), int(g[10]))
                           if g[9] is not None else None),
           "rivales": [], "recursos": []}
    resto = texto[m.end():]
    INV = inverso(mundo) if mundo is not None else {}
    tr, ti = resto.find(" R"), resto.find(" I")
    zr = resto[tr + 2: ti if 0 <= ti > tr else len(resto)] if tr >= 0 else ""
    zi = resto[ti + 2:] if ti >= 0 else ""
    for mm in _RE_RIV.finditer(zr):
        letra = mm.group(4)
        out["rivales"].append({"slot": int(mm.group(1)),
                               "pos": (int(mm.group(2)), int(mm.group(3))),
                               "arma": (None if letra == "-"
                                        else INV.get(letra, letra)),
                               "rumbo": mm.group(5)})
    for mm in _RE_REC.finditer(zi):
        letra = mm.group(1)
        out["recursos"].append({"id": INV.get(letra, letra),
                                "pos": (int(mm.group(2)), int(mm.group(3)))})
    return out

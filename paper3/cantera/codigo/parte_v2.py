"""EL PARTE DE ESTADO — PROMPT_53. Temporada dos, primera piedra.

Cada 48 tics el animal dice como esta, y el que escucha lo lee como HECHO
CIERTO donde hoy adivina por banda. R1 sellado por la mesa: el hermano sabe
su propio estado con certeza y el canal team es cerrado de fabrica (52: 0
terceros en 17.601 mensajes) — lo que llega por team ES del hermano, y su
testimonio se acepta como cierto POR DISENO.

Formato v1 (fijo, ASCII imprimible, <=120 chars, determinista dado el estado):

    E1 P<slot> t<tick> <x>,<y> h<hp> v<0|1> b<n> a<0|1>[ <ax>,<ay>]

  E1        marca de formato (el parser SOLO acepta esta; lo demas se ignora:
            el relleno de liga tambien recibe el canal y podria emitir texto)
  P<slot>   quien habla (se coteja con `from` del chat al escuchar)
  t<tick>   el tic del emisor al emitir (mismo reloj del mundo; sirve para la
            caducidad aunque el mensaje llegue con +2 tics de latencia)
  <x>,<y>   posicion propia (obs.you.pos)
  h<hp>     hp propio EXACTO (formato %g: hasta 6 cifras significativas;
            el hp del mundo cabe entero — [impl] declarado)
  v<0|1>    veneno activo (el mismo test que S-DANO usa para uno mismo:
            algun effect cuyo id empiece por "poison")
  b<n>      botiquines a bordo (unidades en el pack con id del botiquin)
  a<0|1>    agresor activo (algun slot en mem.agresores dentro de la ventana
            S-7); si a1 Y el agresor esta A LA VISTA en esta obs, se anade
            su posicion — solo lo CIERTO en obs viaja; si no se le ve, a1 sin
            posicion (direccion no certificable: no se emite)

Todo lo emitido es un hecho de la obs o de la memoria propia (R1). El parte
es VOZ: no consume accion, no es conducta escrita (R2) y jamas es agresion.

CADUCIDAD del oyente: 96 tics (dos partes perdidos) — la certeza envejece y
se declara; despues se vuelve a la banda.

Sin dependencias del alma: este modulo no importa nada de appraisal/decisor
(el parser lo importa appraisal; el emisor, las policies y el banco).
"""
from __future__ import annotations

import re

MARCA = "E1"
CADA = 48          # tics entre partes (el latido del 32; >= 24 => jamas rate_limited)
CADUCIDAD = 96     # tics: dos partes perdidos y la certeza vuelve a la banda
MAX_CHARS = 120    # espec :114 (sanitizeTalk: ASCII 0x20-0x7E, recorte a 120)

_RE = re.compile(
    r"^E1 P(\d+) t(\d+) (\d+),(\d+) h(\d+(?:\.\d+)?) v([01]) b(\d+) a([01])"
    r"(?: s(\d+))?(?: (\d+),(\d+))?$")     # PROMPT_68: `s<asiento>` opcional


def ascii_limpio(texto: str) -> bool:
    """¿Sobrevive entero a sanitizeTalk (0x20-0x7E, <=120)?"""
    return len(texto) <= MAX_CHARS and all(0x20 <= ord(c) <= 0x7E for c in texto)


def emite(obs: dict, tick: int, mundo, mem, ventana_ticks: int) -> str:
    """El parte propio, determinista dado (obs, tick, memoria).

    `ventana_ticks` es la ventana S-7 de agresor activo en tics
    (A.AGRESOR_VENTANA_S x tick_rate): la misma vara que usan las filas.
    """
    you = obs.get("you") or {}
    pos = you.get("pos") or [0, 0]
    hp = float(you.get("hp") or 0.0)
    ven = any((e.get("id") or "").startswith("poison")
              for e in (you.get("effects") or []))
    bot = 0
    for s in (you.get("pack") or []):
        if s and s.get("id") == mundo.id_botiquin:
            bot += int(s.get("n") or 1)
    # agresor activo: la entrada mas RECIENTE de la ventana (desempate por
    # dano y slot: determinista). Su posicion solo si esta a la vista AHORA.
    agr, agr_pos = 0, None
    mejor = None
    for sl, e in (getattr(mem, "agresores", None) or {}).items():
        if tick - e["ultimo"] > ventana_ticks:
            continue
        clave = (e["ultimo"], e["dano"], sl)
        if mejor is None or clave > mejor[0]:
            mejor = (clave, sl)
    if mejor is not None:
        agr = 1
        agr_pos = mejor[1]      # slot; se resuelve a posicion si es visible
    texto = (f"{MARCA} P{mundo.slot} t{tick} {pos[0]},{pos[1]} "
             f"h{hp:g} v{int(ven)} b{bot} a{agr}")
    if agr:
        # EL NOMBRE DEL AGRESOR (PROMPT_68): su ASIENTO va SIEMPRE. Yo lo se
        # con certeza total —me lo dice `damage_taken.source`— aunque ya no lo
        # vea; la posicion, en cambio, solo si esta a la vista ahora. El nombre
        # identifica; no persigue (quien escucha sigue necesitando VERLO).
        texto += f" s{agr_pos}"
        vis = None
        for a in ((obs.get("visible") or {}).get("agents") or ()):
            if a.get("slot") == agr_pos:
                vis = a.get("pos")
                break
        if vis:
            texto += f" {vis[0]},{vis[1]}"
    return texto


def parsea(texto: str):
    """Parser ESTRICTO: solo la marca E1 con el formato exacto; lo demas -> None.

    Devuelve {"slot","t","pos","hp","veneno","botiquin","agresor","agresor_pos"}
    (agresor_pos None si el emisor no la certifico).
    """
    if not isinstance(texto, str):
        return None
    m = _RE.match(texto)
    if m is None:
        return None
    g = m.groups()
    return {"slot": int(g[0]), "t": int(g[1]),
            "pos": (int(g[2]), int(g[3])),
            "hp": float(g[4]),
            "veneno": g[5] == "1",
            "botiquin": int(g[6]),
            "agresor": g[7] == "1",
            # PROMPT_68: el asiento (v2). Los partes v1 no lo traen -> None y
            # la certificacion cae al respaldo por posicion (compatibilidad).
            "agresor_slot": int(g[8]) if g[8] is not None else None,
            "agresor_pos": (int(g[9]), int(g[10])) if g[9] is not None else None}

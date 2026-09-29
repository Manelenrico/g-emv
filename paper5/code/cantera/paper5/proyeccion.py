"""[P5-3A] LA PROYECCION DE NECESIDADES. Fuera del decisor, sin tocarlo.

Proyecta un estado del cuerpo K tics hacia delante con las reglas DETERMINISTAS
del mundo. No decide nada y no se enchufa a ninguna decision en este encargo.

LAS REGLAS, CON SU FUENTE (`cantera/paper4/manual_del_mundo.md` y el catalogo
del propio diario):

  (iv) ENFRIAMIENTOS
   · andar cuesta `16 - velocidad` tics por casilla; con la velocidad de estas
     criaturas son 11, y tras el paso se ven bajar 10 (manual §4, README:36,
     sim.nim:147; medido: el mayor `move_ready_in` de 191.531 jugadas es 10).
   · pegar tiene su propio enfriamiento, del catalogo del arma (manual §4,
     sim.nim:934). Andar y pegar NO se estorban (sim.nim:618 / :898).
   · los dos bajan de uno en uno por tic y no bajan de cero (PROTO:54).

  (ii) VIDA
   · el anillo quema la casilla que queda fuera del radio, a `damage_per_s`
     puntos por segundo, o sea `dps / tick_rate` por tic (manual §12; el radio
     y el dps de cada instante salen de `mundo.anillo_en(tick)`).
   · el botiquin devuelve **50** y tarda **48** tics; cualquier golpe en ese
     rato lo cancela y el botiquin NO se pierde (manual §6, catalogo `heal` 50 /
     `use_ticks` 48, sim.nim:866-868).
   · la racion devuelve **15** y tarda **24** tics (manual §6, catalogo).
   · la vida se recorta a [0, 100].

  (i) W
   · se recalcula con `riqueza_W` del propio `appraisal_zs_v42_exp`, sin copiar
     ni un peso: coger mete el objeto en la mochila, consumir lo saca.
   · coger solo entra si queda hueco: 2, o 4 con la mochila puesta
     (README:51).

  (iii) EFECTOS
   · el canal de cura se lleva como un contador que baja por tic.
   · el veneno y la red se ARRASTRAN tal como venian, restando su tiempo; no se
     inventan efectos nuevos.

LO QUE NO SE PROYECTA, Y SE DICE:
   · el dano de los rivales y sus movimientos;
   · el VENENO de los dardos (2 puntos por segundo, lo que dura depende de la
     inteligencia del envenenado; manual §5, README:49-51): no se proyecta
     porque ni el momento ni la duracion se saben en t;
   · el gasto de MUNICION al disparar, que cambia el peso del arma a distancia
     (`riqueza_W` escala por `municion/AMMO_REF`);
   · el botin que aparece o que otro se lleva;
   · la cancelacion de la cura por un golpe ajeno (no hay golpes ajenos aqui);
   · el desgaste del arma al pegar a un rival.
"""
from __future__ import annotations
import copy, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
if os.path.join(RAIZ, "paintball") not in sys.path:
    sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from alma.appraisal_zs_v42_exp import riqueza_W            # noqa: E402

PASO_TICS = 11           # 16 - velocidad(5); manual §4
CURA = {"first_aid": (50.0, 48), "rations": (15.0, 24)}    # heal, use_ticks
# el decisor nombra los candidatos de cura en llano (`decisor_zs.py:491`); aqui
# se traducen al id del mundo, que es lo que lleva la mochila.
NOMBRE_A_ID = {"botiquin": "first_aid", "racion": "rations",
               "raciones": "rations", "first_aid": "first_aid",
               "rations": "rations"}
HP_MAX = 100.0


def _huecos(estado, mundo):
    return 4 if estado.get("body") == mundo.id_mochila else 2


def _paso_hacia(p, q):
    return (p[0] + (q[0] > p[0]) - (q[0] < p[0]),
            p[1] + (q[1] > p[1]) - (q[1] < p[1]))


def estado_de(r):
    """Estado proyectable a partir de un registro de tic del diario."""
    return {"tick": r["tick"], "pos": tuple(r.get("pos") or ()),
            "hp": float(r.get("hp") or 0.0),
            "hand": copy.deepcopy(r.get("hand")),
            "body": r.get("body"),
            "pack": [copy.deepcopy(s) for s in (r.get("pack") or []) if s],
            "effects": list(r.get("effects") or []),
            "move_ready_in": int(r.get("move_ready_in") or 0),
            "attack_ready_in": int(r.get("attack_ready_in") or 0),
            # EL CANAL YA ABIERTO. El mundo lo publica en `effects`:
            #   {"id":"channeling","item":"first_aid","done_tick":4945}
            # Sembrarlo es obligatorio: si no, una cura en curso se pierde.
            "cura": next(({"id": x.get("item"),
                           "cura": CURA.get(x.get("item"), (0.0, 0))[0],
                           "quedan": int(x.get("done_tick", 0)) - int(r["tick"])}
                          for x in (r.get("effects") or [])
                          if x.get("id") == "channeling"
                          and x.get("item") in CURA), None)}


def W_de(estado, mundo):
    you = {"hand": estado.get("hand"), "pack": estado.get("pack"),
           "body": estado.get("body")}
    return riqueza_W(you, mundo)[0]


def proyectar_rapido(estado_t, plan, K, mundo, suelo=None):
    """[P5-3E · E5] `proyectar` sin `copy.deepcopy`.

    El perfil de P5-3D senalaba al `deepcopy` como el 58,7 % del tiempo. Aqui
    se copian a mano SOLO las piezas que el bucle muta: la mochila (dicts que
    cambian de `n`), la mano, los efectos y el canal de cura. Todo lo demas es
    inmutable. El resultado es identico al bit; se valida aparte.
    """
    import forma as _F
    e = _F.copia_estado(estado_t)
    return _proyecta(e, plan, K, mundo, suelo)


def proyectar(estado_t, plan, K, mundo, suelo=None, camino=None):
    """estado_t + K tics bajo `plan`. Devuelve el estado nuevo (copia).

    `plan` puede ser:
      · una LISTA de K acciones, una por tic: "paso", "coger", "usar_<id>",
        "esperar" (o None);
      · o un DICCIONARIO de intencion: {"destino": (x,y), "coger": bool,
        "usar": "<id>"} — se convierte en un plan por tics: andar hacia el
        destino en cuanto las piernas esten listas, y al llegar coger o usar.
    `suelo` es {(x,y): {"id":..,"n":..}}, lo que el cuerpo SABE que hay en el
    suelo; solo se usa para "coger".
    `camino` es la lista de posiciones REALES, una por tic, cuando se quiere
    aislar el error de las reglas del error de no saber adonde va el cuerpo
    (A3). Con `camino` la posicion no se inventa: se sigue.
    """
    e = copy.deepcopy(estado_t)
    return _proyecta(e, plan, K, mundo, suelo, camino)


def _proyecta(e, plan, K, mundo, suelo=None, camino=None):
    """El bucle, compartido por `proyectar` y `proyectar_rapido`."""
    e.setdefault("cura", None)
    suelo = dict(suelo or {})
    lista = isinstance(plan, (list, tuple))
    destino = None if lista else tuple((plan or {}).get("destino") or ()) or None
    coger = bool((plan or {}).get("coger")) if not lista else False
    usar = (plan or {}).get("usar") if not lista else None
    hecho = {"pasos": 0, "cogido": [], "usado": [], "dano_anillo": 0.0,
             "curado": 0.0}

    for i in range(K):
        t = e["tick"] + 1
        e["tick"] = t
        acc = (plan[i] if (lista and i < len(plan)) else None)
        # 1. los enfriamientos bajan
        e["move_ready_in"] = max(0, e["move_ready_in"] - 1)
        e["attack_ready_in"] = max(0, e["attack_ready_in"] - 1)
        # 2. el canal de cura
        if e["cura"] is not None:
            e["cura"]["quedan"] -= 1
            if e["cura"]["quedan"] <= 0:
                cur = e["cura"]
                antes = e["hp"]
                e["hp"] = min(HP_MAX, e["hp"] + cur["cura"])
                hecho["curado"] += e["hp"] - antes
                # el objeto se consume al completarse
                for s in list(e["pack"]):
                    if s.get("id") == cur["id"]:
                        s["n"] = int(s.get("n") or 1) - 1
                        if s["n"] <= 0:
                            e["pack"].remove(s)
                        break
                hecho["usado"].append(cur["id"])
                e["cura"] = None
        # 3. la accion del tic
        quiere_paso = (acc == "paso") if lista else (
            destino is not None and tuple(e["pos"]) != destino)
        quiere_coger = (acc == "coger") if lista else (
            coger and destino is not None and tuple(e["pos"]) == destino)
        quiere_usar = (NOMBRE_A_ID.get(acc[5:], acc[5:])
                       if (lista and isinstance(acc, str)
                           and acc.startswith("usar_")) else
                       (NOMBRE_A_ID.get(usar, usar)
                        if (not lista and usar and e["cura"] is None
                                 and (destino is None
                                      or tuple(e["pos"]) == destino)) else None))
        if camino is not None and i < len(camino) and camino[i] is not None:
            nueva = tuple(camino[i])
            if nueva != tuple(e["pos"]):
                e["pos"] = nueva
                e["move_ready_in"] = PASO_TICS - 1
                hecho["pasos"] += 1
        elif quiere_paso and e["move_ready_in"] == 0 and destino is not None:
            e["pos"] = _paso_hacia(tuple(e["pos"]), destino)
            e["move_ready_in"] = PASO_TICS - 1
            hecho["pasos"] += 1

        if quiere_coger:
            it = suelo.pop(tuple(e["pos"]), None)
            if it and len(e["pack"]) < _huecos(e, mundo):
                e["pack"].append({"id": it["id"], "n": int(it.get("n") or 1)})
                hecho["cogido"].append(it["id"])
            coger = False
        if quiere_usar and e["cura"] is None and quiere_usar in CURA:
            if any(s.get("id") == quiere_usar for s in e["pack"]):
                cura, dura = CURA[quiere_usar]
                e["cura"] = {"id": quiere_usar, "cura": cura, "quedan": dura}
                usar = None
        # 4. el anillo
        try:
            _c, radio, dps = mundo.anillo_en(t)
        except Exception:
            radio, dps = None, 0.0
        if radio is not None and dps and e["pos"]:
            c = (mundo.arena_size // 2, mundo.arena_size // 2)
            d = ((e["pos"][0] - c[0]) ** 2 + (e["pos"][1] - c[1]) ** 2) ** 0.5
            if d > radio:
                q = dps / float(mundo.tick_rate)
                e["hp"] = max(0.0, e["hp"] - q)
                hecho["dano_anillo"] += q
        # 5. los efectos que venian, se arrastran
        e["effects"] = [x for x in e["effects"]]
    e["W"] = W_de(e, mundo)
    e["_hecho"] = hecho
    return e


def congelada(estado_t, mundo, K):
    """LA FOTO DE HOY: solo se mueve la posicion; lo demas se congela.

    Es lo que hace el decisor (`decisor_zs.py:325-326`: se valora al tick real;
    H solo sirve para saber a que casilla se llega).
    """
    e = copy.deepcopy(estado_t)
    e["tick"] = estado_t["tick"] + K
    e["W"] = W_de(e, mundo)
    return e

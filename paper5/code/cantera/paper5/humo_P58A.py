"""[P5-8A] El humo donde vive la regla. Dos escenas construidas a mano.

  (1) un armado A TIRO y la forma generada A LA FUERZA -> tiene que salir
      VETADA por la puerta (o no generarse).
  (2) frontera SOLO detras de un armado -> "sin frontera segura".
"""
import os, sys, hashlib
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4")); sys.path.insert(0, AQUI)
import serie_util as U
import curiosidad as C, curiosidad_forma as CF
import glob, json

FALLOS = []


def _mundo():
    f = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P57C_t1_A_20260916",
                                      "*.art.log")))[0]
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    return U.mundo_de(pc, list(sm["filas"]), cat["items"]), pc.get("teammate_slot")


def escena(mundo, pos, armado_pos, arma, vistas):
    ojo = C.Ojo(mundo, 8)
    for q in vistas:
        ojo.primera_vez[q] = 0
    r = {"pos": list(pos), "hp": 100, "damage_taken": [],
         "ve_agentes": ([{"slot": 3, "pos": list(armado_pos), "hand": arma,
                          "hp_band": "healthy"}] if armado_pos else []),
         "ve_items": [], "ve_proyectiles": []}
    return ojo, r


def uno_armado_a_tiro():
    mundo, herm = _mundo()
    pos = (24, 24)
    # TODO visto salvo un corredor al norte; el armado, pegado al cuerpo
    vistas = {(x, y) for x in range(mundo.arena_size)
              for y in range(mundo.arena_size) if y >= 20}
    ojo, r = escena(mundo, pos, (25, 24), "sword", vistas)
    arms = CF.armados(r, mundo, herm)
    rg = arms[0][1] if arms else 0
    a_tiro = max(abs(pos[0] - 25), abs(pos[1] - 24)) <= rg
    tr, info = CF.genera(r, mundo, None, ojo, herm, 500, 0.5)
    print(f"  (1) armado a tiro (alcance {rg}, dist 1 -> a tiro {a_tiro}) · "
          f"amenaza {info['amenaza']:.4f} · motivo: {info['motivo']}")
    if not a_tiro:
        FALLOS.append("la escena (1) no pone al armado a tiro")
    if tr is not None:
        FALLOS.append("(1) GENERO forma con un armado a tiro")
    else:
        print(f"      -> NO se genera. La amenaza ({info['amenaza']:.3f}) pasa "
              f"el umbral de seguro ({CF.UMBRAL_SEGURO}).")
    # y A LA FUERZA: se salta el disparo y se mira la sombra
    cam, d, dest = CF.camino_a_frontera(ojo, mundo, pos, arms)
    if dest is None:
        print("      -> a la fuerza: tampoco hay frontera fuera de sombra")
    else:
        cruza = CF.cruza_sombra(cam, pos, arms)
        tiro = CF.destino_a_tiro(dest, arms)
        print(f"      -> a la fuerza: destino {dest} · cruza sombra {cruza} · "
              f"destino a tiro {tiro}")
        if cruza or tiro:
            FALLOS.append("(1) a la fuerza el camino cruza sombra o el destino esta a tiro")


def dos_frontera_detras_del_armado():
    mundo, herm = _mundo()
    pos = (24, 24)
    # todo visto MENOS una bolsa al norte lejano; el armado, en medio del camino
    no_vistas = {(x, y) for x in range(20, 29) for y in range(4, 9)}
    vistas = {(x, y) for x in range(mundo.arena_size)
              for y in range(mundo.arena_size)} - no_vistas
    ojo, r = escena(mundo, pos, (24, 14), "bow", vistas)
    arms = CF.armados(r, mundo, herm)
    cam, d, dest = CF.camino_a_frontera(ojo, mundo, pos, arms)
    print(f"  (2) frontera SOLO detras del armado (armado en (24,14), "
          f"alcance {arms[0][1]}) · destino {dest}")
    if dest is not None:
        FALLOS.append(f"(2) dio frontera {dest} cuando toda esta en sombra")
    else:
        print("      -> «sin frontera segura», como debe")
    # y sin el armado, la MISMA escena SI da frontera (control)
    ojo2, r2 = escena(mundo, pos, None, None, vistas)
    cam2, d2, dest2 = CF.camino_a_frontera(ojo2, mundo, pos, [])
    print(f"      control sin armado: destino {dest2} a {d2} casillas")
    if dest2 is None:
        FALLOS.append("(2) el control sin armado tampoco da frontera: la escena no vale")


if __name__ == "__main__":
    print("== HUMO P5-8A · donde vive la regla ==")
    h = hashlib.md5(open(os.path.join(AQUI, "curiosidad_forma.py"), "rb").read()).hexdigest()
    print(f"  md5 del cuerpo (curiosidad_forma.py): {h}")
    uno_armado_a_tiro()
    dos_frontera_detras_del_armado()
    if FALLOS:
        print("\nFALLOS:")
        for x in FALLOS:
            print("  ·", x)
        sys.exit(1)
    print("\nLOS DOS HUMOS OK")

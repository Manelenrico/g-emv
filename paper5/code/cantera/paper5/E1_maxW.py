"""[P5-1 E1] El maximo de W que el inventario del mundo permite.

Fuerza bruta sobre las combinaciones que las reglas del mundo admiten:
  · mano: 1 hueco · cuerpo: 1 hueco (mochila O camuflaje, no los dos)
  · mochila: 2 huecos, o 4 si se lleva la mochila
    (README de zero-sum: "Gear: backpack (2 -> 4 pack slots)")
Se llama a `riqueza_W` del propio modulo, sin copiar ni una constante.
"""
import glob, itertools, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
import serie_util as U                                       # noqa: E402
from alma.appraisal_zs_v42_exp import riqueza_W              # noqa: E402

f = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                  "*-policy_agent_1*.art.log")))[0]
recs = list(U.lee(f))
pc = next(r for r in recs if r.get("k") == "player_config")
sm = next(r for r in recs if r.get("k") == "static_map")
cat = next(r for r in recs if r.get("k") == "catalogo")
mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
print("dmg_ref:", mundo.dmg_ref, "· botiquin:", mundo.id_botiquin,
      "· raciones:", mundo.id_raciones, "· mochila:", mundo.id_mochila,
      "· camuflaje:", mundo.id_camuflaje, "· red:", mundo.id_red)
armas = [(i, it) for i, it in mundo.items.items()
         if getattr(it, "kind", None) in ("ikMelee", "ikRanged", "ikThrown")]
print("armas del catalogo:", [(i, it.kind, it.damage, it.durability)
                              for i, it in armas])

cands = ["first_aid", "rations", mundo.id_red, "arrows"]
mejor = []
for cuerpo in (mundo.id_mochila, mundo.id_camuflaje, None):
    huecos = 4 if cuerpo == mundo.id_mochila else 2
    for arma_id, it in armas + [(None, None)]:
        durs = ([it.durability, max(1, int(it.durability * 0.99))]
                if (it and it.durability) else [None])
        for dur in durs:
            mano = ({"id": arma_id, "n": 1, "durability": dur}
                    if arma_id else None)
            for combo in itertools.product(
                    [None, {"id": "first_aid", "n": 1}],
                    [None, {"id": "rations", "n": 1},
                     {"id": "rations", "n": 2}],
                    [None, {"id": mundo.id_red, "n": 1}],
                    [None, {"id": "arrows", "n": 8}]):
                pack = [s for s in combo if s]
                if len(pack) > huecos:
                    continue
                you = {"hand": mano, "pack": pack, "body": cuerpo}
                W, d = riqueza_W(you, mundo)
                mejor.append((round(W, 4), cuerpo, arma_id, dur,
                              [s["id"] + ("x%d" % s["n"] if s["n"] > 1 else "")
                               for s in pack], d))
mejor.sort(key=lambda x: -x[0])
print(f"\ncombinaciones probadas: {len(mejor):,}")
print("\nLAS SEIS MEJORES:")
for W, cu, ar, du, pk, d in mejor[:6]:
    print(f"  W = {W:6.4f} · cuerpo {cu} · mano {ar} (dur {du}) · mochila {pk}")
    print(f"           {({k: round(v,4) for k, v in d.items()})}")
print(f"\nMAXIMO DE W: {mejor[0][0]}")
json.dump({"maximo": mejor[0][0],
           "mejores": [{"W": W, "cuerpo": cu, "mano": ar, "durabilidad": du,
                        "mochila": pk, "desglose": {k: round(v, 4)
                                                    for k, v in d.items()}}
                       for W, cu, ar, du, pk, d in mejor[:6]]},
          open(os.path.join(AQUI, "E1_maxW.json"), "w"),
          ensure_ascii=False, indent=1)

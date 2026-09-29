"""[P5-8B · C1] La serie de la curiosidad: brazos A y Q, cinco semillas por tanda.

  python3 cantera/paper5/lanza_P58H.py --tanda 1
  python3 cantera/paper5/lanza_P58H.py --tanda 1 --lanzar

Veinte semillas de `cantera/paper4/semillas_S2.json`, la MISMA para los dos
brazos, `lento_v0` con `roster_lento_v1`, una peticion por episodio.
Cuatro tandas de cinco semillas x dos brazos = diez episodios cada una.
"""
import datetime, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))

LIGA = "league_6764202e-2ac1-4c98-a77e-cabc75582939"
IMAGEN = "sha256:68faccb52f23415012f2d596f9d12a2943c4cf157bc27eb457f046aab234f7a4"
ETIQUETA = "gemv-anima:curforma-m0"
BRAZOS = {
    "A": ("gemv-p58m-A:v1", "939269d2-3aa0-4144-a541-224eda91f7d3", "cuerpo solo"),
    "K": ("gemv-p58m-K:v1", "68e4de97-ce20-475b-8456-cb4bfeec1faa",
          "curiosidad como forma CON COMPROMISO"),
}
POR_TANDA = int(__import__("sys").argv[__import__("sys").argv.index("--n")+1]) if "--n" in __import__("sys").argv else 5          # cinco semillas x dos brazos = diez episodios


def semillas():
    return json.load(open(os.path.join(RAIZ, "cantera", "paper4",
                                        "semillas_S2.json")))


def cuerpo(brazo, semilla, tanda):
    doc = json.load(open(os.path.join(AQUI, "roster_lento_v1.json")))
    cfg = dict(doc["game_config_overrides"])
    cfg["seed"] = semilla
    _n, pvid, que = BRAZOS[brazo]
    roster = [{"player": {"policy_ref": pvid}, "slot": s} for s in (10, 11)]
    for riv in doc["rivales"]:
        for _ in range(riv["veces"]):
            roster.append({"player": {"policy_ref": riv["policy_version_id"]},
                           "slot": -1})
    assert len(roster) == 16, len(roster)
    return {"private": True, "target": {"league_id": LIGA}, "num_episodes": 1,
            "notes": f"P5-8M tanda {tanda} · brazo {brazo} · {que} · "
                     f"roster lento v1 · semilla {semilla}",
            "game_config_overrides": cfg, "roster": roster}


def main():
    tanda = int(sys.argv[sys.argv.index("--tanda") + 1]
                if "--tanda" in sys.argv else 1)
    # tanda 0 = LA SONDA: la primera semilla, una partida por brazo
    ss = (semillas()[:1] if tanda == 0
          else semillas()[(tanda - 1) * POR_TANDA: tanda * POR_TANDA])
    # --salta N: deja fuera las N primeras de la tanda. La sonda de P5-8M ya
    # jugo la semilla 1 con ESTA imagen y ESTAS politicas (comprobado contra el
    # registro del servidor), asi que la tanda 1 lanza solo las cuatro que
    # faltan y las diez partidas se completan con las dos de la sonda.
    if "--salta" in sys.argv:
        ss = ss[int(sys.argv[sys.argv.index("--salta") + 1]):]
    print(f"### P5-8M · TANDA {tanda} · semillas {ss} · "
          f"{len(ss) * 2} episodios ###")
    print(f"### imagen {ETIQUETA}  {IMAGEN} ###")
    for b, (n, p, q) in BRAZOS.items():
        print(f"  {b}: {n}  {p}  ({q})")
    if "--lanzar" not in sys.argv:
        print("\n(no se envia: falta --lanzar)")
        return
    from coworld.api_client import CoworldApiClient
    from coworld.config import DEFAULT_SUBMIT_SERVER
    salida = []
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        for semilla in ss:
            for b in ("A", "K"):
                t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
                r = c._http_client.post("/v2/experience-requests",
                                        headers=c._headers(),
                                        json=cuerpo(b, semilla, tanda),
                                        timeout=180.0)
                if r.status_code >= 300:
                    print(f"  {b}/{semilla}: ERROR {r.status_code} "
                          f"{r.text[:200]}", flush=True)
                    continue
                d = r.json()
                ep = (d.get("episodes") or [{}])[0]
                salida.append({"brazo": b, "semilla": semilla,
                               "xreq": d.get("id"), "ereq": ep.get("id"),
                               "creada": d.get("created_at"),
                               "pedida_a_las": t0})
                print(f"  {b}/{semilla}: {d.get('id')[:18]} · "
                      f"{ep.get('id')[:20]} · {d.get('created_at')[11:19]}",
                      flush=True)
    json.dump(salida, open(os.path.join(AQUI, f"P58M_t{tanda}_peticiones.json"),
                           "w"), ensure_ascii=False, indent=1)
    print(f"\n{len(salida)} peticiones creadas · guardadas en "
          f"P58M_t{tanda}_peticiones.json")


if __name__ == "__main__":
    main()

"""[P5-8B · C1] La serie de la curiosidad: brazos A y Q, cinco semillas por tanda.

  python3 cantera/paper5/lanza_P58D.py --tanda 1
  python3 cantera/paper5/lanza_P58D.py --tanda 1 --lanzar

Veinte semillas de `cantera/paper4/semillas_S2.json`, la MISMA para los dos
brazos, `lento_v0` con `roster_lento_v1`, una peticion por episodio.
Cuatro tandas de cinco semillas x dos brazos = diez episodios cada una.
"""
import datetime, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))

LIGA = "league_6764202e-2ac1-4c98-a77e-cabc75582939"
IMAGEN = "sha256:66e9e0440749f65185e184da84f9017dd5deb63970291918c12eaa1ebe9be440"
ETIQUETA = "gemv-anima:curforma-d0"
BRAZOS = {
    "A": ("gemv-p58d-A:v1", "a20606e1-8bc9-4c64-8910-bcaa222a372c", "cuerpo solo"),
    "K": ("gemv-p58d-K:v1", "faa51b82-2da8-4563-92d1-b099f0016696",
          "curiosidad como forma, reloj honesto y alivio"),
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
            "notes": f"P5-8B tanda {tanda} · brazo {brazo} · {que} · "
                     f"roster lento v1 · semilla {semilla}",
            "game_config_overrides": cfg, "roster": roster}


def main():
    tanda = int(sys.argv[sys.argv.index("--tanda") + 1]
                if "--tanda" in sys.argv else 1)
    ss = semillas()[(tanda - 1) * POR_TANDA: tanda * POR_TANDA]
    print(f"### P5-8B · TANDA {tanda} · semillas {ss} · "
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
    json.dump(salida, open(os.path.join(AQUI, f"P58D_t{tanda}_peticiones.json"),
                           "w"), ensure_ascii=False, indent=1)
    print(f"\n{len(salida)} peticiones creadas · guardadas en "
          f"P58D_t{tanda}_peticiones.json")


if __name__ == "__main__":
    main()

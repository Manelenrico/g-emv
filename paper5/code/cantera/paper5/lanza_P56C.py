"""[P5-6C · C1] La serie: una peticion por episodio, tres brazos por semilla.

  python3 cantera/paper5/lanza_P56C.py --tanda 1 --ver
  python3 cantera/paper5/lanza_P56C.py --tanda 1 --lanzar

Semillas en el orden de `cantera/paper4/semillas_S2.json`
(`20260916 + k*104729`), cuatro por tanda, los tres brazos con la MISMA
semilla. Todas las politicas salen de la imagen `gemv-anima:forma-c0`
(`sha256:f7c0ffb3b5213e70714337ee036056abe28a89bc39931f897cb99d3a1156b846`).
"""
import datetime, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))

LIGA = "league_6764202e-2ac1-4c98-a77e-cabc75582939"
IMAGEN = "sha256:10e36356de5380bd12f884ea577f814e4fca9e4de43a6c7e38feef81df774e94"  # forma-c1bis
BRAZOS = {
    "A": ("gemv-p56c2-A:v1", "f2e75f10-2b94-4156-9be0-d26665056a65",
          "todo apagado (cuerpo solo)"),
    "F": ("gemv-p56c2-F:v1", "aa1de6b6-093d-4865-b656-d59915187aa8",
          "forma + hilo + consejero (Haiku 4.5)"),
    "T": ("gemv-p56c2-T:v1", "98d465dc-0036-4a4f-857c-3e2e844e3a06",
          "forma + hilo + formas al azar"),
}
POR_TANDA = 4          # cuatro semillas x tres brazos = doce episodios


def semillas():
    return json.load(open(os.path.join(RAIZ, "cantera", "paper4",
                                        "semillas_S2.json")))


def cuerpo(brazo, semilla, tanda):
    doc = json.load(open(os.path.join(AQUI, "roster_lento_v1.json")))
    cfg = dict(doc["game_config_overrides"])
    cfg["seed"] = semilla
    nombre, pvid, que = BRAZOS[brazo]
    roster = [{"player": {"policy_ref": pvid}, "slot": s} for s in (10, 11)]
    for riv in doc["rivales"]:
        for _ in range(riv["veces"]):
            roster.append({"player": {"policy_ref": riv["policy_version_id"]},
                           "slot": -1})
    assert len(roster) == 16, len(roster)
    return {"private": True, "target": {"league_id": LIGA}, "num_episodes": 1,
            "notes": f"P5-6C tanda {tanda} · brazo {brazo} · {que} · "
                     f"roster lento v1 · semilla {semilla}",
            "game_config_overrides": cfg, "roster": roster}


def main():
    tanda = int(sys.argv[sys.argv.index("--tanda") + 1]
                if "--tanda" in sys.argv else 1)
    ss = semillas()[(tanda - 1) * POR_TANDA: tanda * POR_TANDA]
    print(f"### TANDA {tanda} · semillas {ss} · {len(ss) * 3} episodios ###")
    print(f"### imagen {IMAGEN} ###")
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
            for b in ("A", "F", "T"):
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
                d["_brazo"], d["_semilla"], d["_tanda"] = b, semilla, tanda
                d["_pedida_a_las"] = t0
                salida.append({"brazo": b, "semilla": semilla,
                               "xreq": d.get("id"), "ereq": ep.get("id"),
                               "creada": d.get("created_at")})
                print(f"  {b}/{semilla}: {d.get('id')[:18]} · "
                      f"{ep.get('id')[:20]} · {d.get('created_at')[11:19]}",
                      flush=True)
    json.dump(salida, open(os.path.join(AQUI, f"P56C_t{tanda}_peticiones.json"),
                           "w"), ensure_ascii=False, indent=1)
    print(f"\n{len(salida)} peticiones creadas · guardadas en "
          f"P56C_t{tanda}_peticiones.json")


if __name__ == "__main__":
    main()

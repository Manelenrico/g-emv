"""[P5-1 fase B] UNA peticion privada, UN episodio, mundo lento provisional.

Roster de A3: nuestros dos asientos con slot explicito y los catorce rivales de
S-3 por policy_version_id. Escribe la respuesta entera en
cantera/paper5/B1_peticion.json.

  python3 cantera/paper5/lanza_B1.py --ver     imprime el cuerpo y NO envia
  python3 cantera/paper5/lanza_B1.py --lanzar  crea la peticion
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))

LIGA = "league_6764202e-2ac1-4c98-a77e-cabc75582939"     # la de zero-sum
NUESTRA = "gemv-p5-A:v1"                                  # cuerpo solo, brazo A
SEMILLA = int(os.environ.get("P5_SEMILLA", "20260916"))
ETIQUETA = os.environ.get("P5_ETIQUETA", "B1")

# los catorce rivales de S-3, por policy_version_id, leidos de `participants`
# del episodio ereq_9cf61642-a6c4-4163-a32c-bdc4da40e07e. Cuatro van dos veces,
# que es como llenaban los dieciseis asientos.
RIVALES = [
    ("6244cdeb-e044-42ff-91e3-a5c716c4338d", "zero-sum-scavenger", 2),
    ("47f38a1c-9143-4b56-9316-ceabe7c82c6d", "relh-zero-sum", 2),
    ("41f43efa-bbd5-477a-8ed1-1443f2731eb1", "sivanlevy-zs-courier", 2),
    ("458ec0b6-fc59-4bda-aff0-68daa7f21b79", "belobog", 2),
    ("54ec6fab-6773-46db-bb55-119688182786", "ryanschiller-zero-sum-player-v1", 1),
    ("2b9cfd17-db50-4990-8f99-6c7c13453f61", "zs-patient", 1),
    ("9457da2a-832d-45e5-b918-9209e86f9948", "aaron-zs-fable", 1),
    ("dfc40843-b709-4332-85a6-c5bbb653375b", "zero-sum-example", 1),
    ("3e8097e1-85b8-4731-b7c1-e674f2ccbd10", "skourehjan-zero-sum-scripted-v1", 1),
    ("09da1dbc-ac3b-4bb1-9114-4ee615496755", "Zero Sum Baseline", 1),
]


def cuerpo():
    cfg = json.load(open(os.path.join(AQUI, "lento_v0.json")))
    cfg["seed"] = SEMILLA
    roster = [{"player": {"policy_ref": NUESTRA}, "slot": 10},
              {"player": {"policy_ref": NUESTRA}, "slot": 11}]
    for pvid, _n, veces in RIVALES:
        for _ in range(veces):
            roster.append({"player": {"policy_ref": pvid}, "slot": -1})
    assert len(roster) == 16, len(roster)
    return {"private": True,
            "target": {"league_id": LIGA},
            "num_episodes": 1,
            "notes": f"P5-1 {ETIQUETA} · mundo lento provisional lento_v0 · "
                     f"brazo A (cuerpo solo) · semilla {SEMILLA}",
            "game_config_overrides": cfg}, roster


def main():
    b, roster = cuerpo()
    b["roster"] = roster
    print("### CUERPO DE LA PETICION ###")
    d = dict(b)
    d["game_config_overrides"] = {
        k: (f"<{len(v['schedule'])} filas>" if k == "zone"
            else {kk: (f"<{len(vv)} regalos>" if kk == "scripted_gifts" else vv)
                  for kk, vv in v.items()} if k == "sponsor" else v)
        for k, v in b["game_config_overrides"].items()}
    d["roster"] = f"<16 asientos: 10 y 11 = {NUESTRA}; 14 rivales con slot -1>"
    print(json.dumps(d, ensure_ascii=False, indent=1))
    print(f"\nasientos: {len(roster)} · nuestros: "
          f"{[r['slot'] for r in roster if r['slot'] != -1]}")
    if "--lanzar" not in sys.argv:
        print("\n(no se envia: falta --lanzar)")
        return
    from coworld.api_client import CoworldApiClient
    from coworld.config import DEFAULT_SUBMIT_SERVER
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        r = c._http_client.post("/v2/experience-requests",
                                headers=c._headers(), json=b, timeout=180.0)
        print(f"\n### RESPUESTA {r.status_code} ###")
        try:
            resp = r.json()
        except Exception:
            print(r.text[:2000]); return
        print(json.dumps(resp, ensure_ascii=False, indent=1)[:4000])
        json.dump(resp, open(os.path.join(AQUI, os.environ.get("P5_SALIDA", "B1_peticion.json")), "w"),
                  ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

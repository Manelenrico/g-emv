"""[P5-6B] UNA peticion privada por brazo, un episodio, la MISMA semilla.

Roster de `roster_lento_v1.json`: fuera las tres cazadoras, dentro tres
repeticiones de las tres politicas mas pacificas que ya estaban. Nuestros dos
asientos con slot explicito.

  python3 cantera/paper5/lanza_P56B.py A --ver      imprime y NO envia
  python3 cantera/paper5/lanza_P56B.py A --lanzar   crea la peticion
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))

LIGA = "league_6764202e-2ac1-4c98-a77e-cabc75582939"     # la de zero-sum
SEMILLA = int(os.environ.get("P5_SEMILLA", "20260916"))  # la 1 de la lista
BRAZOS = {
    "A": ("gemv-p56-A:v1", "0b666688-753c-46f2-94ea-ce4cdf1b4fc8",
          "todo apagado (cuerpo solo, como el cuatro)"),
    "F": ("gemv-p56-F:v1", "6bca871a-dfc8-4777-a636-81a8d0b826aa",
          "forma + hilo + consejero (Haiku 4.5 por el sidecar)"),
    # [repeticion] F2: MISMA imagen y mismo sha; solo dos variables mas, porque
    # en F el 36 % de las llamadas murio por timeout (mediana 7.185 ms contra
    # 8.000 de tope) y 40 de 84 citas se saltaron por tener una en vuelo.
    "F2": ("gemv-p56-F:v2", "01e336b8-4894-41b1-8b61-9166cc6f946a",
           "como F, con GEMV_CORTEX_TIMEOUT=25 y GEMV_FORMA_CADA=250"),
    # [P5-6C · C0] la partida de comprobacion de /spend, imagen forma-c0
    "C0F": ("gemv-p56c-F:v1", "f4a54db0-137f-41a4-b4fb-2bb4545522b8",
            "forma + hilo + consejero, con /spend cada 10 llamadas"),
    "T": ("gemv-p56-T:v1", "d6f937dd-8097-4f14-8d33-178f28e5f288",
          "forma + hilo + formas al AZAR (consejero apagado)"),
}


def cuerpo(brazo):
    doc = json.load(open(os.path.join(AQUI, "roster_lento_v1.json")))
    cfg = dict(doc["game_config_overrides"])
    cfg["seed"] = SEMILLA
    nombre, pvid, que = BRAZOS[brazo]
    roster = [{"player": {"policy_ref": pvid}, "slot": s}
              for s in (10, 11)]
    for riv in doc["rivales"]:
        for _ in range(riv["veces"]):
            roster.append({"player": {"policy_ref": riv["policy_version_id"]},
                           "slot": -1})
    assert len(roster) == 16, len(roster)
    return {"private": True,
            "target": {"league_id": LIGA},
            "num_episodes": 1,
            "notes": f"P5-6 brazo {brazo} · {que} · roster lento v1 "
                     f"(sin las tres cazadoras) · semilla {SEMILLA}",
            "game_config_overrides": cfg,
            "roster": roster}


def main():
    brazo = (sys.argv[1] if len(sys.argv) > 1 else "").upper()
    if brazo not in BRAZOS:
        print("uso: lanza_P56B.py <A|F|T> [--lanzar]")
        return
    b = cuerpo(brazo)
    nombre, pvid, que = BRAZOS[brazo]
    print(f"### BRAZO {brazo} · {nombre} · {que} ###")
    d = dict(b)
    d["game_config_overrides"] = {
        k: (f"<{len(v['schedule'])} filas>" if k == "zone"
            else {kk: (f"<{len(vv)} regalos>" if kk == "scripted_gifts" else vv)
                  for kk, vv in v.items()} if k == "sponsor" else v)
        for k, v in b["game_config_overrides"].items()}
    d["roster"] = (f"<16 asientos: 10 y 11 = {nombre} ({pvid}); "
                   f"14 rivales con slot -1>")
    print(json.dumps(d, ensure_ascii=False, indent=1))
    if "--lanzar" not in sys.argv:
        print("\n(no se envia: falta --lanzar)")
        return
    from coworld.api_client import CoworldApiClient
    from coworld.config import DEFAULT_SUBMIT_SERVER
    import datetime
    t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        r = c._http_client.post("/v2/experience-requests",
                                headers=c._headers(), json=b, timeout=180.0)
        print(f"\n### RESPUESTA {r.status_code} · pedida a las {t0} ###")
        try:
            resp = r.json()
        except Exception:
            print(r.text[:2000]); return
        print(json.dumps(resp, ensure_ascii=False, indent=1)[:3000])
        resp["_pedida_a_las"] = t0
        resp["_brazo"] = brazo
        json.dump(resp, open(os.path.join(AQUI, f"P56B_{brazo}_peticion.json"),
                             "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

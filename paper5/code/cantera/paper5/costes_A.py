"""[P5-1 A4/A5] Coste real de cada episodio de S-2 y S-3, leido de la API.

SOLO GET: recorre las peticiones anotadas en las tablas del paper cuatro y
guarda, por episodio, el coste en dolares y la configuracion EFECTIVA con que
corrio. No crea ni cancela nada.
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
P4 = os.path.join(RAIZ, "cantera", "paper4")
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from coworld.api_client import CoworldApiClient
from coworld.config import DEFAULT_SUBMIT_SERVER

CLAVES = ("max_ticks", "freeze_ticks", "stat_budget", "seed", "league_mode")


def main():
    pet = []
    for f, serie in ((os.path.join(P4, "tabla_partidas.json"), "S-2"),
                     (os.path.join(P4, "tabla_S3.json"), "S-3")):
        for e in json.load(open(f)):
            pet.append((serie, e["brazo"], e["xreq"]))
    print(f"peticiones a consultar: {len(pet)}")
    filas, vistos = [], set()
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        for i, (serie, brazo, xid) in enumerate(pet, 1):
            if xid in vistos:
                continue
            vistos.add(xid)
            try:
                r = c._http_client.get(f"/v2/experience-requests/{xid}",
                                       headers=c._headers(), timeout=90.0)
            except Exception as ex:
                print(f"  {xid}: FALLO {repr(ex)[:90]}")
                continue
            if r.status_code >= 300:
                print(f"  {xid}: {r.status_code}")
                continue
            d = r.json()
            req = d.get("requested") or {}
            for ep in d.get("episodes") or []:
                gc = ep.get("game_config") or {}
                z = (gc.get("zone") or {}).get("schedule") or []
                sp = gc.get("sponsor") or {}
                filas.append({
                    "serie": serie, "brazo": brazo, "xreq": xid,
                    "ereq": ep["id"], "estado": ep["status"],
                    "coste_usd": ep.get("cost_usd"),
                    "nota": req.get("notes"),
                    "n_episodios_pedidos": req.get("num_episodes"),
                    "politica_nuestra": next(
                        (x.get("policy") for x in (req.get("roster") or [])
                         if x.get("slot") == 10), None),
                    "config": {k: gc.get(k) for k in CLAVES},
                    "zone_primera_fila": z[0] if z else None,
                    "zone_filas": len(z),
                    "sponsor_budget_per_team": sp.get("budget_per_team"),
                    "sponsor_shop_opens_tick": sp.get("shop_opens_tick"),
                    "creado": ep.get("created_at"),
                    "despachado": ep.get("dispatched_at"),
                    "arrancado": ep.get("running_at"),
                    "acabado": ep.get("completed_at"),
                    "rechazos_gasto_llm": ep.get("llm_spend_limit_rejections")})
            if i % 20 == 0:
                print(f"  {i}/{len(pet)}")
    p = os.path.join(AQUI, "costes_episodios.json")
    json.dump(filas, open(p, "w"), ensure_ascii=False, indent=1)
    print(f"episodios leidos: {len(filas)} -> {p}")


if __name__ == "__main__":
    main()

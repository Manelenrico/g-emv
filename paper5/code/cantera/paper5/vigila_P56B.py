"""[P5-6B] SOLO GET: mira las tres peticiones hasta que acaban."""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from coworld.api_client import CoworldApiClient
from coworld.config import DEFAULT_SUBMIT_SERVER

XR = {b: json.load(open(os.path.join(AQUI, f"P56B_{b}_peticion.json")))["id"]
      for b in "AFT"}


def main():
    hechos = {}
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        while len(hechos) < 3:
            for b, xid in XR.items():
                if b in hechos:
                    continue
                r = c._http_client.get(f"/v2/experience-requests/{xid}",
                                       headers=c._headers(), timeout=90.0)
                if r.status_code >= 300:
                    continue
                d = r.json()
                for e in d.get("episodes") or []:
                    print(f"{b} {e.get('id')[:18]} {e.get('status'):10s} "
                          f"creado={d.get('created_at')} "
                          f"arranque={e.get('running_at')} "
                          f"fin={e.get('completed_at')} "
                          f"coste={e.get('cost_usd')}", flush=True)
                    if e.get("status") in ("completed", "failed", "cancelled"):
                        hechos[b] = d
                        json.dump(d, open(os.path.join(AQUI, f"P56B_{b}_final.json"), "w"),
                                  ensure_ascii=False, indent=1)
            if len(hechos) < 3:
                time.sleep(45)
    print("LAS TRES ACABADAS")
    for b, d in hechos.items():
        e = (d.get("episodes") or [{}])[0]
        print(f"  {b}: {e.get('status')} coste {e.get('cost_usd')}")

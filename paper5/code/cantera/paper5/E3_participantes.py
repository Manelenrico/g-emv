"""[P5-1 E3] Cachea position -> policy_name de cada episodio de S-2 y S-3."""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
P4 = os.path.join(RAIZ, "cantera", "paper4")
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from coworld.api_client import CoworldApiClient
from coworld.config import DEFAULT_SUBMIT_SERVER

xreqs = []
for f, s in ((os.path.join(P4, "tabla_partidas.json"), "S-2"),
             (os.path.join(P4, "tabla_S3.json"), "S-3")):
    for e in json.load(open(f)):
        xreqs.append((s, e["xreq"]))
out, vistos = {}, set()
with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
    for i, (serie, x) in enumerate(xreqs, 1):
        if x in vistos:
            continue
        vistos.add(x)
        r = c._http_client.get(f"/v2/experience-requests/{x}",
                               headers=c._headers(), timeout=90)
        if r.status_code >= 300:
            continue
        for ep in (r.json().get("episodes") or []):
            p = {str(q["position"]): q.get("policy_name")
                 for q in (ep.get("participants") or [])}
            if p:
                out[ep["id"]] = {"serie": serie, "participants": p}
        if i % 25 == 0:
            print(f"  {i}/{len(xreqs)} · episodios {len(out)}", flush=True)
json.dump(out, open(os.path.join(AQUI, "E3_participantes.json"), "w"),
          ensure_ascii=False, indent=1)
print(f"episodios con participantes: {len(out)}")

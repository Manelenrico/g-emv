"""[P5-1 B1] Espera a que el episodio acabe, anotando los tiempos.

Consulta cada 45 s. Escribe cantera/paper5/B1_final.json al terminar.
"""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from coworld.api_client import CoworldApiClient
from coworld.config import DEFAULT_SUBMIT_SERVER

ENT = os.environ.get("P5_ENT", "B1_peticion.json")
SAL = os.environ.get("P5_SAL", "B1_final.json")
XREQ = json.load(open(os.path.join(AQUI, ENT)))["id"]
FIN = {"completed", "failed", "cancelled"}


def main():
    t0 = time.time()
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        while True:
            r = c._http_client.get(f"/v2/experience-requests/{XREQ}",
                                   headers=c._headers(), timeout=90)
            d = r.json()
            ep = (d.get("episodes") or [{}])[0]
            print(f"[{int(time.time()-t0):5d}s] peticion={d['status']:10s} "
                  f"episodio={ep.get('status'):10s} "
                  f"despachado={ep.get('dispatched_at')} "
                  f"arrancado={ep.get('running_at')} "
                  f"coste={ep.get('cost_usd')}", flush=True)
            if ep.get("status") in FIN and d["status"] in FIN:
                json.dump(d, open(os.path.join(AQUI, SAL), "w"),
                          ensure_ascii=False, indent=1)
                print("FIN:", ep.get("status"), "coste", ep.get("cost_usd"))
                return
            time.sleep(45)


if __name__ == "__main__":
    main()

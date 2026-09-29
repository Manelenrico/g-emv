"""[P5-6B] SOLO GET: gasto acumulado cobrado y cola. No crea ni cancela nada.

El listado `/v2/experience-requests` devuelve `entries` de TODA la liga, asi que
se filtra por nuestro `requester`. El coste vive en cada episodio, que solo
aparece al pedir la peticion una a una; se cachea en `P56B_gasto_cache.json`
para no repetir GETs.
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from coworld.api_client import CoworldApiClient          # noqa: E402
from coworld.config import DEFAULT_SUBMIT_SERVER         # noqa: E402

# OJO: la identidad de la PLATAFORMA no es la del correo de la sesion. La
# nuestra es [correo tapado] (user id [tapado]),
# comprobada pidiendo una peticion conocida (xreq_505e8f3b, la de P5-1 B1).
# Y el filtro que funciona es `mine=true`: `?requester=` lo ignora el servidor.
YO = os.environ.get("P5_CORREO", "")  # [Zenodo: correo tapado]
CACHE = os.path.join(AQUI, "P56B_gasto_cache.json")


def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    mias, cursor = [], None
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        while True:
            q = "/v2/experience-requests?limit=100&mine=true"
            if cursor:
                q += f"&cursor={cursor}"
            r = c._http_client.get(q, headers=c._headers(), timeout=90.0)
            if r.status_code >= 300:
                print("ERROR", r.status_code, r.text[:200]); return
            d = r.json()
            ent = d.get("entries") or []
            mias += [e for e in ent if e.get("requester") == YO]
            cursor = d.get("next_cursor")
            if not cursor or not ent:
                break
        print(f"peticiones de {YO}: {len(mias)}")
        cola = {"pending": [0, 0], "submitted": [0, 0], "running": [0, 0]}
        for e in mias:
            st = e.get("status")
            sin = ((e.get("pending_count") or 0) + (e.get("submitted_count") or 0)
                   + (e.get("running_count") or 0))
            if st in cola:
                cola[st][0] += 1
                cola[st][1] += sin
            elif sin:
                cola.setdefault("otros", [0, 0])
                cola["otros"][0] += 1; cola["otros"][1] += sin
        cobrados, total, nuevos = 0, 0.0, 0
        for i, e in enumerate(mias, 1):
            xid = e["id"]
            if xid in cache:
                eps = cache[xid]
            else:
                rr = c._http_client.get(f"/v2/experience-requests/{xid}",
                                        headers=c._headers(), timeout=90.0)
                if rr.status_code >= 300:
                    continue
                eps = [{"id": x.get("id"), "cost_usd": x.get("cost_usd"),
                        "status": x.get("status")}
                       for x in (rr.json().get("episodes") or [])]
                # solo se cachea lo ya TERMINADO: lo vivo puede cambiar de precio
                if e.get("status") in ("completed", "failed", "cancelled"):
                    cache[xid] = eps
                nuevos += 1
                if nuevos % 25 == 0:
                    print(f"  ... {i}/{len(mias)}", flush=True)
            for x in eps:
                if x.get("cost_usd") is not None:
                    cobrados += 1
                    total += float(x["cost_usd"])
    json.dump(cache, open(CACHE, "w"))
    print(f"  episodios cobrados: {cobrados}")
    print(f"  gasto acumulado   : {total:.6f} USD")
    print()
    for k, v in cola.items():
        print(f"{k:10s}: {v[0]:3d} peticiones · {v[1]:4d} episodios sin acabar")
    json.dump({"peticiones": len(mias), "cobrados": cobrados,
               "gasto_usd": round(total, 6), "cola": cola},
              open(os.path.join(AQUI, "P56B_estado.json"), "w"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

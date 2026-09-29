"""[P5-1 fase A] Sonda EN SECO contra la plataforma. Solo GET / previews.

No crea ninguna peticion de experiencia. Vuelca lo que encuentre en
cantera/paper5/sonda_A/.
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from coworld.api_client import CoworldApiClient
from coworld.config import DEFAULT_SUBMIT_SERVER

OUT = os.path.join(AQUI, "sonda_A")
os.makedirs(OUT, exist_ok=True)

def guarda(nom, obj):
    p = os.path.join(OUT, nom + ".json")
    json.dump(obj, open(p, "w"), ensure_ascii=False, indent=1)
    return p

def main():
    rutas = sys.argv[1:]
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        for ruta in rutas:
            try:
                r = c._http_client.get(ruta, headers=c._headers(), timeout=60.0)
                print(f"\n### GET {ruta} -> {r.status_code}")
                try:
                    d = r.json()
                except Exception:
                    print(r.text[:600]); continue
                nom = ruta.strip("/").replace("/", "_").replace("?", "_")[:80]
                print("  guardado:", guarda(nom, d))
                print(json.dumps(d, ensure_ascii=False)[:1500])
            except Exception as ex:
                print(f"\n### GET {ruta} -> FALLO {repr(ex)[:200]}")

if __name__ == "__main__":
    main()

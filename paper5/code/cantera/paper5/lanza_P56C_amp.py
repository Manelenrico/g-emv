"""[P5-6C · ampliacion] F y T con las semillas 21 a 40. PREPARADO, NO LANZADO.

Solo se dispara si al cerrar las sesenta la regla de continuacion sellada el
21-sep se cumple. **A no se amplia.**

  python3 cantera/paper5/lanza_P56C_amp.py --tanda 1 --ver      (no envia)
  python3 cantera/paper5/lanza_P56C_amp.py --tanda 1 --lanzar

Cinco tandas de cuatro semillas x dos brazos = ocho episodios cada una,
cuarenta en total. Misma imagen, mismo roster, mismas politicas que la serie.
"""
import datetime, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, AQUI)
from lanza_P56C import BRAZOS, IMAGEN, LIGA, cuerpo      # noqa: E402

POR_TANDA = 4
BRAZOS_AMP = ("F", "T")          # A NO se amplia


def semillas():
    d = json.load(open(os.path.join(AQUI, "semillas_21_40.json")))
    return d["semillas_21_a_40"]


def main():
    tanda = int(sys.argv[sys.argv.index("--tanda") + 1]
                if "--tanda" in sys.argv else 1)
    ss = semillas()[(tanda - 1) * POR_TANDA: tanda * POR_TANDA]
    print(f"### AMPLIACION · tanda {tanda} · semillas {ss} · "
          f"{len(ss) * len(BRAZOS_AMP)} episodios ###")
    print(f"### imagen {IMAGEN} ###")
    for b in BRAZOS_AMP:
        n, p, q = BRAZOS[b]
        print(f"  {b}: {n}  {p}  ({q})")
    print("  A: NO se amplia (asi lo fija la regla sellada)")
    if "--lanzar" not in sys.argv:
        print("\n(no se envia: falta --lanzar)")
        return
    from coworld.api_client import CoworldApiClient
    from coworld.config import DEFAULT_SUBMIT_SERVER
    salida = []
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        for semilla in ss:
            for b in BRAZOS_AMP:
                cu = cuerpo(b, semilla, f"amp{tanda}")
                t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
                r = c._http_client.post("/v2/experience-requests",
                                        headers=c._headers(), json=cu,
                                        timeout=180.0)
                if r.status_code >= 300:
                    print(f"  {b}/{semilla}: ERROR {r.status_code} "
                          f"{r.text[:200]}", flush=True)
                    continue
                d = r.json()
                ep = (d.get("episodes") or [{}])[0]
                d["_brazo"], d["_semilla"], d["_tanda"] = b, semilla, f"amp{tanda}"
                d["_pedida_a_las"] = t0
                salida.append({"brazo": b, "semilla": semilla,
                               "xreq": d.get("id"), "ereq": ep.get("id"),
                               "creada": d.get("created_at")})
                print(f"  {b}/{semilla}: {d.get('id')[:18]} · "
                      f"{ep.get('id')[:20]}", flush=True)
    json.dump(salida, open(os.path.join(
        AQUI, f"P56C_amp{tanda}_peticiones.json"), "w"),
        ensure_ascii=False, indent=1)
    print(f"\n{len(salida)} peticiones creadas")


if __name__ == "__main__":
    main()

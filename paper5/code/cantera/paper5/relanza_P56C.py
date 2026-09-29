"""[P5-6C · cierre] Relanza pares (brazo, semilla) sueltos de la ampliacion.

  python3 cantera/paper5/relanza_P56C.py --pares F:24135889,T:24135889 --ver
  python3 cantera/paper5/relanza_P56C.py --pares F:24135889,T:24135889 --lanzar
  python3 cantera/paper5/relanza_P56C.py --vigila P56C_sonda_peticiones.json \
          --minutos 15 --cada 2

Hace falta porque las seis pendientes de la ultima tanda ya no forman una tanda
entera: dos de las ocho corrieron y seis se cancelaron por cola. Misma imagen,
mismas politicas y mismo roster que toda la serie: `cuerpo()` sale de
`lanza_P56C`, no se reescribe.

`--vigila` mira el estado cada `--cada` minutos y, si a los `--minutos` no han
pasado a `running`, CANCELA las que sigan en `submitted` (nunca las que hayan
arrancado) y sale con codigo 2.
"""
import datetime, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, AQUI)
from lanza_P56C import BRAZOS, IMAGEN, cuerpo          # noqa: E402


def arg(nombre, por_defecto=None):
    return (sys.argv[sys.argv.index(nombre) + 1]
            if nombre in sys.argv else por_defecto)


def cliente():
    from coworld.api_client import CoworldApiClient
    from coworld.config import DEFAULT_SUBMIT_SERVER
    return CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER)


def estado(c, xreq):
    d = c._http_client.get(f"/v2/experience-requests/{xreq}",
                           headers=c._headers(), timeout=60).json()
    return (d.get("episodes") or [{}])[0]


def lanza(pares, salida):
    print(f"### RELANZA · {len(pares)} episodios ###")
    print(f"### imagen {IMAGEN} ###")
    for b, s in pares:
        print(f"  {b}/{s}: {BRAZOS[b][0]}")
    if "--lanzar" not in sys.argv:
        print("\n(no se envia: falta --lanzar)")
        return
    out = []
    with cliente() as c:
        for b, s in pares:
            r = c._http_client.post("/v2/experience-requests",
                                    headers=c._headers(),
                                    json=cuerpo(b, s, "amp5-relanzada"),
                                    timeout=180.0)
            if r.status_code >= 300:
                print(f"  {b}/{s}: ERROR {r.status_code} {r.text[:200]}",
                      flush=True)
                continue
            d = r.json()
            ep = (d.get("episodes") or [{}])[0]
            out.append({"brazo": b, "semilla": s, "xreq": d.get("id"),
                        "ereq": ep.get("id"), "creada": d.get("created_at")})
            print(f"  {b}/{s}: {d.get('id')[:18]} · {ep.get('id')[:20]} · "
                  f"{d.get('created_at')[11:19]}", flush=True)
    json.dump(out, open(os.path.join(AQUI, salida), "w"),
              ensure_ascii=False, indent=1)
    print(f"\n{len(out)} peticiones creadas · guardadas en {salida}")


def vigila(fichero, minutos, cada):
    """Cada `cada` minutos; a los `minutos` cancela lo que siga en submitted."""
    P = json.load(open(os.path.join(AQUI, fichero)))
    t0 = time.time()
    with cliente() as c:
        while True:
            espera = (time.time() - t0) / 60.0
            hay_submitted = corriendo = acabados = 0
            for x in P:
                ep = estado(c, x["xreq"])
                s = ep.get("status")
                hay_submitted += s in ("submitted", "pending")
                corriendo += s == "running"
                acabados += s in ("completed", "failed", "cancelled")
                print(f"  [{espera:5.1f} min] {x['brazo']}/{x['semilla']}: "
                      f"{s} · run={(ep.get('running_at') or '-')[11:19]} "
                      f"· cost={ep.get('cost_usd')}", flush=True)
            if not hay_submitted:
                print(f"--> TODAS ARRANCARON a los {espera:.1f} min", flush=True)
                if acabados == len(P):
                    print("--> y todas han acabado", flush=True)
                    return 0
                time.sleep(cada * 60)
                continue
            if espera >= minutos:
                print(f"--> A LOS {minutos} MIN SIGUEN SIN ARRANCAR: se cancelan "
                      f"las que esten en submitted", flush=True)
                for x in P:
                    ep = estado(c, x["xreq"])
                    if ep.get("status") not in ("submitted", "pending"):
                        print(f"  RESPETADA {x['brazo']}/{x['semilla']}: "
                              f"{ep.get('status')}", flush=True)
                        continue
                    r = c._http_client.post(
                        f"/v2/experience-requests/{x['xreq']}/cancel",
                        headers=c._headers(), timeout=60)
                    ep2 = estado(c, x["xreq"])
                    print(f"  CANCELA {x['brazo']}/{x['semilla']}: HTTP "
                          f"{r.status_code} -> {ep2.get('status')} · "
                          f"cost={ep2.get('cost_usd')}", flush=True)
                return 2
            time.sleep(cada * 60)


def main():
    if "--vigila" in sys.argv:
        sys.exit(vigila(arg("--vigila"), float(arg("--minutos", "15")),
                        float(arg("--cada", "2"))))
    pares = [(p.split(":")[0], int(p.split(":")[1]))
             for p in (arg("--pares") or "").split(",") if p]
    if not pares:
        print("falta --pares F:123,T:123"); sys.exit(1)
    lanza(pares, arg("--salida", "P56C_sonda_peticiones.json"))


if __name__ == "__main__":
    main()

"""[P5-6C · cierre] El ciclo de la sonda, cada hora, hasta cerrar las cien.

  python3 cantera/paper5/ciclo_P56C.py

Reglas, tal como las fijo Manel:
  · cola vacia delante de cada intento;
  · la sonda son DOS episodios (una semilla, F y T);
  · quince minutos: si no pasan a `running`, se cancelan y se espera una hora;
  · si corren y el precio por episodio esta por debajo de 0,20 $, se lanzan
    los CUATRO restantes (con cola vacia delante y el mismo guardia de 15 min);
  · si el precio pasa de 0,20 $, PARA y avisa.

Topes duros, para que esto no pueda gastar de mas solo:
  · nunca crea mas de SONDA(2) + RESTO(4) = 6 episodios en toda su vida;
  · cualquier episodio que no arranque en 15 min se cancela (coste cero);
  · si el gasto de la serie pasa de TOPE_SERIE, para.
"""
import datetime, json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, AQUI)

SONDA = [("F", 24135889), ("T", 24135889)]
RESTO = [("T", 24031160), ("F", 24240618), ("F", 24345347), ("T", 24345347)]
TOPE_EPISODIO = 0.20
TOPE_SERIE = 15.0
ESPERA_H = 1.0
MINUTOS = 15.0
CADA = 2.0
MAX_INTENTOS = 24


def ahora():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")


def cliente():
    from coworld.api_client import CoworldApiClient
    from coworld.config import DEFAULT_SUBMIT_SERVER
    return CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER)


def gasto_y_cola(_c=None):
    """(gasto acumulado, episodios sin acabar), del checker ya probado.

    NO se reimplementa aqui: `estado_P56B.py` pagina con cursor, filtra por
    `requester` y suma los `*_count`. Reimplementarlo con `items` en vez de
    `entries` daba cola vacia SIEMPRE, que es justo el fallo que enmascara un
    atasco.
    """
    r = subprocess.run([sys.executable, "-u",
                        os.path.join(AQUI, "estado_P56B.py")],
                       capture_output=True, text=True, timeout=900)
    tot, sin_acabar = None, 0
    for ln in r.stdout.splitlines():
        if "gasto acumulado" in ln:
            tot = float(ln.split(":")[1].split()[0])
        for st in ("pending", "submitted", "running"):
            if ln.strip().startswith(st):
                sin_acabar += int(ln.split("·")[1].split()[0])
    if tot is None:
        raise RuntimeError("no se pudo leer el gasto: " + r.stdout[-400:])
    return tot, sin_acabar


def estado(c, xreq):
    d = c._http_client.get(f"/v2/experience-requests/{xreq}",
                           headers=c._headers(), timeout=60).json()
    return (d.get("episodes") or [{}])[0]


def crea(c, pares, etiqueta):
    from lanza_P56C import cuerpo
    out = []
    for b, s in pares:
        r = c._http_client.post("/v2/experience-requests", headers=c._headers(),
                                json=cuerpo(b, s, "amp5-relanzada"), timeout=180.0)
        if r.status_code >= 300:
            print(f"  {b}/{s}: ERROR {r.status_code} {r.text[:160]}", flush=True)
            continue
        d = r.json()
        ep = (d.get("episodes") or [{}])[0]
        out.append({"brazo": b, "semilla": s, "xreq": d.get("id"),
                    "ereq": ep.get("id"), "creada": d.get("created_at")})
        print(f"  creada {b}/{s}: {ep.get('id')[:20]} · "
              f"{d.get('created_at')[11:19]}", flush=True)
    json.dump(out, open(os.path.join(AQUI, f"P56C_{etiqueta}_peticiones.json"),
                        "w"), ensure_ascii=False, indent=1)
    return out


def cancela_las_paradas(c, P):
    for x in P:
        ep = estado(c, x["xreq"])
        if ep.get("status") not in ("submitted", "pending"):
            print(f"  RESPETADA {x['brazo']}/{x['semilla']}: {ep.get('status')}",
                  flush=True)
            continue
        r = c._http_client.post(f"/v2/experience-requests/{x['xreq']}/cancel",
                                headers=c._headers(), timeout=60)
        ep2 = estado(c, x["xreq"])
        print(f"  CANCELA {x['brazo']}/{x['semilla']}: HTTP {r.status_code} -> "
              f"{ep2.get('status')} · cost={ep2.get('cost_usd')}", flush=True)


def espera_arranque(c, P):
    """True si TODAS arrancaron dentro del plazo; si no, las cancela."""
    t0 = time.time()
    while True:
        m = (time.time() - t0) / 60.0
        quietas = 0
        for x in P:
            ep = estado(c, x["xreq"])
            quietas += ep.get("status") in ("submitted", "pending")
        print(f"  [{ahora()} · {m:4.1f} min] en submitted: {quietas}/{len(P)}",
              flush=True)
        if not quietas:
            print(f"  --> ARRANCARON a los {m:.1f} min", flush=True)
            return True
        if m >= MINUTOS:
            print(f"  --> {MINUTOS:.0f} min sin arrancar: se cancelan", flush=True)
            cancela_las_paradas(c, P)
            return False
        time.sleep(CADA * 60)


def espera_fin(c, P):
    while True:
        eps, faltan = [], 0
        for x in P:
            ep = estado(c, x["xreq"])
            if ep.get("status") in ("completed", "failed", "cancelled"):
                eps.append((x, ep))
            else:
                faltan += 1
        if not faltan:
            return eps
        time.sleep(60)


def main():
    intentos = 0
    while intentos < MAX_INTENTOS:
        intentos += 1
        print(f"\n===== INTENTO {intentos} · {ahora()} =====", flush=True)
        with cliente() as c:
            gasto, sin_acabar = gasto_y_cola(c)
            print(f"  gasto de la cuenta {gasto:.6f} $ · episodios sin acabar "
                  f"{sin_acabar}", flush=True)
            if sin_acabar:
                print("  cola NO vacia: se espera", flush=True)
            else:
                P = crea(c, SONDA, "sonda")
                if P and espera_arranque(c, P):
                    eps = espera_fin(c, P)
                    precios = [ep.get("cost_usd") for _x, ep in eps
                               if ep.get("cost_usd") is not None]
                    for x, ep in eps:
                        print(f"  {x['brazo']}/{x['semilla']}: "
                              f"{ep.get('status')} · {ep.get('cost_usd')} $",
                              flush=True)
                    caro = [p for p in precios if p >= TOPE_EPISODIO]
                    if caro:
                        print(f"  --> PARA: precio por encima de "
                              f"{TOPE_EPISODIO} $ ({caro})", flush=True)
                        return 3
                    print(f"  --> precios por debajo de {TOPE_EPISODIO} $: "
                          f"van los cuatro restantes", flush=True)
                    g2, s2 = gasto_y_cola(c)
                    if s2:
                        print("  cola no vacia antes del resto: PARA",
                              flush=True)
                        return 4
                    Q = crea(c, RESTO, "resto")
                    if Q and espera_arranque(c, Q):
                        for x, ep in espera_fin(c, Q):
                            print(f"  {x['brazo']}/{x['semilla']}: "
                                  f"{ep.get('status')} · "
                                  f"{ep.get('cost_usd')} $", flush=True)
                        print("  --> LAS CIEN, CERRADAS", flush=True)
                        return 0
                    print("  --> el resto no arranco; se canceló", flush=True)
        print(f"  esperando {ESPERA_H} h hasta el siguiente intento", flush=True)
        time.sleep(ESPERA_H * 3600)
    return 5


if __name__ == "__main__":
    sys.exit(main())

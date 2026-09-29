"""[P5-8M] Sondea las peticiones de la tanda y guarda el documento de cada una.

  python3 recoge_P58I.py 1          una pasada
  python3 recoge_P58I.py 1 --hasta  sondea cada 90 s hasta que no quede ninguna viva

Escribe P58M_t{tanda}_{brazo}_{semilla}.json (el que lee baja_P58I.py) en cuanto
el episodio acaba, e informa precio, cola y juego. PARA con aviso si algun
precio sale de 0,04-0,08.
"""
import datetime as dt, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from coworld.api_client import CoworldApiClient          # noqa: E402
from coworld.config import DEFAULT_SUBMIT_SERVER         # noqa: E402

TOPE_MIN = 0.012        # [P5-8M · Manel] parada por $/MINUTO de pod, no por partida


def _t(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def pasada(c, tanda, peticiones):
    vivos, fuera = 0, []
    for p in peticiones:
        dest = os.path.join(AQUI, f"P58M_t{tanda}_{p['brazo']}_{p['semilla']}.json")
        if os.path.exists(dest):
            continue
        r = c._http_client.get(f"/v2/experience-requests/{p['xreq']}",
                               headers=c._headers(), timeout=90.0)
        if r.status_code >= 300:
            print(f"  {p['brazo']}/{p['semilla']}: ERROR {r.status_code}"); vivos += 1; continue
        d = r.json()
        e = (d.get("episodes") or [{}])[0]
        st = e.get("status")
        if st not in ("completed", "failed", "cancelled"):
            vivos += 1
            print(f"  {p['brazo']}/{p['semilla']}: {st}", flush=True)
            continue
        d["_brazo"], d["_semilla"], d["_tanda"] = p["brazo"], p["semilla"], tanda
        d["_pedida_a_las"] = p["pedida_a_las"]
        json.dump(d, open(dest, "w"), ensure_ascii=False, indent=1)
        cst = e.get("cost_usd")
        cola = (_t(e.get("running_at")) - _t(e.get("created_at"))).total_seconds() / 60 \
            if e.get("running_at") else float("nan")
        jue = (_t(e.get("completed_at")) - _t(e.get("running_at"))).total_seconds() / 60 \
            if e.get("running_at") and e.get("completed_at") else float("nan")
        pm = (cst / (cola + jue)) if (cst is not None and (cola + jue) > 0) else None
        mal = pm is not None and pm > TOPE_MIN
        print(f"  {p['brazo']}/{p['semilla']}: {st} · {cst} $ · "
              f"cola {cola:.1f} min · juego {jue:.1f} min · "
              f"{pm:.5f} $/min"
              f"{'   <<< PASA DE 0,012 $/MIN' if mal else ''}", flush=True)
        if mal:
            fuera.append((p["brazo"], p["semilla"], cst))
    return vivos, fuera


def main():
    tanda = sys.argv[1] if len(sys.argv) > 1 else "1"
    peticiones = json.load(open(os.path.join(AQUI, f"P58M_t{tanda}_peticiones.json")))
    assert len(peticiones) in (2, 4, 8, 10), len(peticiones)
    fuera_todo = []
    with CoworldApiClient.from_login(server_url=DEFAULT_SUBMIT_SERVER) as c:
        while True:
            print(f"--- {dt.datetime.now():%H:%M:%S} ---", flush=True)
            vivos, fuera = pasada(c, tanda, peticiones)
            fuera_todo += fuera
            if vivos == 0:
                print("TANDA COMPLETA", flush=True); break
            if "--hasta" not in sys.argv:
                print(f"{vivos} vivos", flush=True); break
            time.sleep(90)
    if fuera_todo:
        print("\n*** PARA: $/min por encima de 0,012 ***")
        for b, s, cst in fuera_todo:
            print(f"   {b}/{s}: {cst} $")


if __name__ == "__main__":
    main()

"""[P6-22 · 3] ¿ES EL BLOQUEO DEL INTERPRETE? Prueba directa, coste cero, sin partidas.

Un bucle principal que hace lo que hace el cuerpo cada tic (D.decide sobre una observacion
real de un diario de A6, ~2 ms) a 24 por segundo, medido tic a tic (latencia = tiempo desde
que toca el tic hasta que la decision esta), en cuatro condiciones:
  (a) solo;
  (b) con un HILO de Python que calcula sin parar en puro Python (copias profundas de la
      memoria real del cuerpo, lo mismo que hace `_recoge` para el hilo de la puerta);
  (c) con un PROCESO aparte haciendo el mismo trabajo;
  (d) con el propio bucle principal haciendo una copia profunda de la memoria cada 25 tics
      (lo que hace `_recoge` / `_revisa_vivas` en el hilo principal cuando hay plan vivo).
Se cuenta cuantos tics pasan de 41,7 ms (1000/24: lo que dura un tic) y la distribucion.
    python3 mide_gil_P6_22.py [--tics 720]
"""
import argparse, copy, glob, json, multiprocessing as mp, os, re, statistics as st, sys, threading, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    sys.path.insert(0, p)
for _k, _v in (("GEMV_MIEDO", "0"), ("GEMV_VIDA_AJENA", "0"), ("GEMV_MEMORIA", os.path.join(RAIZ, "paintball", "alma", "memoria_aprendida_p95.json")), ("GEMV_CORTEX", "0"), ("GEMV_FORMA", "0"), ("GEMV_OJOS", "1"), ("GEMV_COMPANIA_TECHO", "0.32")):
    os.environ.setdefault(_k, _v)
TICK_MS = 1000.0 / 24.0


def carga_obs():
    import serie_util as U
    from alma import policy_cortex as PC
    import banco_P6_15 as B      # el arnes de P6-15: config_de / obs_de por la via real
    carp = sorted(glob.glob(os.path.join(RAIZ, "paintball/runs/P618_t1_A6_20679832")))[0]
    f = glob.glob(os.path.join(carp, "*policy_agent_10.art.log"))[0]
    pc, sm, cat, tics, sp, it, fin = B.carga(f)
    cfg = B.config_de(pc, sm, cat)
    obs = [B.obs_de(r, sp, it) for r in tics if 11856 <= r["tick"] < 12200]
    return cfg, obs


def trabajo_puro(mem_bytes, segundos):
    """Copias profundas sin parar durante `segundos` (puro Python, como `_recoge`)."""
    import pickle
    mem = pickle.loads(mem_bytes); t0 = time.perf_counter(); n = 0
    while time.perf_counter() - t0 < segundos:
        copy.deepcopy(mem); n += 1
    return n


def bucle(decide, obs, n_tics, cada_copia=None, mem=None):
    lat = []; t0 = time.perf_counter(); i = 0
    while i < n_tics:
        objetivo = t0 + i * TICK_MS / 1000.0
        ahora = time.perf_counter()
        if ahora < objetivo:
            time.sleep(objetivo - ahora); ahora = time.perf_counter()
        if cada_copia and i % cada_copia == 0 and mem is not None:
            copy.deepcopy(mem)
        decide(obs[i % len(obs)])
        lat.append((time.perf_counter() - objetivo) * 1000.0); i += 1
    return lat


def resumen(lat):
    v = sorted(lat)
    return {"n": len(v), "mediana_ms": round(v[len(v) // 2], 2), "p90_ms": round(v[int(0.9 * len(v))], 2), "p99_ms": round(v[int(0.99 * len(v))], 2), "max_ms": round(v[-1], 1), "tics_por_encima_de_un_tic": sum(1 for x in v if x > TICK_MS), "pct": round(100 * sum(1 for x in v if x > TICK_MS) / len(v), 1)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--tics", type=int, default=720); a = ap.parse_args()
    import pickle
    from alma import policy_cortex as PC
    from alma.mundo import Mundo
    import policy_pareja as PP
    cfg, obs = carga_obs()
    alma = PP.AlmaPareja(); PP._envuelve(alma)
    alma.mundo = Mundo.desde_player_config(dict(cfg))
    # calentar: el cuerpo decide sobre las primeras observaciones (mem se puebla)
    for o in obs[:200]:
        alma.decidir(o)
    mem_bytes = pickle.dumps(alma.mem)
    t = time.perf_counter(); copy.deepcopy(alma.mem); ms_copia = (time.perf_counter() - t) * 1000.0
    t = time.perf_counter(); pickle.loads(pickle.dumps(alma.mem)); ms_pickle = (time.perf_counter() - t) * 1000.0
    decide = lambda o: alma.decidir(o)
    R = {"nota": "P6-22 §3. Prueba del bloqueo del interprete. Bucle principal = alma.decidir (cuerpo A4 con ojos) sobre observaciones reales de A6 (semilla 20679832, asiento 10, desde el aviso 5), a 24 por segundo.",
         "tic_ms": round(TICK_MS, 2), "copia_profunda_de_mem_ms": round(ms_copia, 1), "pickle_ida_y_vuelta_de_mem_ms": round(ms_pickle, 1), "bytes_mem_pickle": len(mem_bytes), "condiciones": {}}
    seg = a.tics * TICK_MS / 1000.0 + 1.0
    # (a) solo
    R["condiciones"]["a) solo"] = resumen(bucle(decide, obs, a.tics))
    # (b) hilo que copia sin parar
    h = threading.Thread(target=trabajo_puro, args=(mem_bytes, seg), daemon=True); h.start(); time.sleep(0.2)
    R["condiciones"]["b) con un hilo de Python calculando (copias profundas de mem)"] = resumen(bucle(decide, obs, a.tics)); h.join()
    # (c) proceso aparte
    ctx = mp.get_context("spawn"); pr = ctx.Process(target=trabajo_puro, args=(mem_bytes, seg), daemon=True); pr.start(); time.sleep(1.5)
    R["condiciones"]["c) con un proceso aparte calculando lo mismo"] = resumen(bucle(decide, obs, a.tics)); pr.join()
    # (d) el bucle principal copia mem cada 25 tics
    R["condiciones"]["d) el bucle principal copia mem cada 25 tics (como _recoge/_revisa_vivas)"] = resumen(bucle(decide, obs, a.tics, cada_copia=25, mem=alma.mem))
    json.dump(R, open(os.path.join(AQUI, "P6_22_gil.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in R.items() if k != "condiciones"}, ensure_ascii=False))
    for k, v in R["condiciones"].items():
        print("  ", k, v)
    print("-> P6_22_gil.json")

"""[P6-6 · A] EL BUCLE SOLTAR/COGER EN LAS SERIES DEL CINCO. SOLO LECTURA.

El bucle se descubrio en P6-5: `soltar` deja la pila en MI casilla, al tic
siguiente la veo bajo mis pies, `coger` gana, y vuelvo a soltar. Dos tics por
vuelta. La cesion que deberia cortarlo se borra cada tic porque el PROMPT_59
abre el don con el hermano SANO y el PROMPT_24 caduca la cesion precisamente
por eso (`decisor_zs.py:480,508-513` vs `appraisal_zs_v42_exp.py:667-683`).

UNA sola definicion para todas las series, para que los numeros se comparen:

  INTENTO   un tic con `RADIOGRAFIA.elegido` = `soltar_<id>`.
  EPISODIO  racha maxima de intentos en la MISMA casilla y el MISMO id, con
            huecos <= HUECO tics (el bucle alterna drop/coger: hueco de 2).
  BUCLE     episodio con >= MIN_BUCLE intentos. Uno o dos intentos seguidos son
            un don normal; tres ya es la oscilacion.
  TICS EN BUCLE  fin - ini + 1 de cada episodio en bucle.
  VIDA      un diario de agente = un asiento en una partida.

Lee los diarios de UNO EN UNO y sin guardar la partida entera (los .art.log del
cinco suman gigas; ver la regla de memoria de la casa).

Uso:
  python3 mide_bucle_P6_6.py 'P5-6C=paintball/runs/P56C_*' ...
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
import serie_util as U

HUECO = 3
MIN_BUCLE = 3


def episodios_de(f):
    """Recorre un diario y devuelve (tics_vivos, [episodios]). Sin guardar tics."""
    eps, abierto, n = [], {}, 0
    for r in U.lee(f):
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        n += 1
        el = str(((r.get("RADIOGRAFIA") or {}).get("elegido")) or "")
        if not el.startswith("soltar_"):
            continue
        iid = el[len("soltar_"):]
        cel = tuple(int(x) for x in (r.get("pos") or ()))
        k = (iid, cel)
        e = abierto.get(k)
        t = r["tick"]
        if e is not None and t - e["fin"] <= HUECO:
            e["fin"], e["intentos"] = t, e["intentos"] + 1
            continue
        e = {"id": iid, "casilla": cel, "ini": t, "fin": t, "intentos": 1}
        abierto[k] = e
        eps.append(e)
    return n, eps


def mide(pats):
    S = collections.Counter()
    peor = None
    porvida = []
    for pat in pats:
        for f in sorted(glob.glob(os.path.join(pat, "*policy_agent_1*.art.log"))):
            sl = re.search(r"policy_agent_(\d+)\.art\.log$", f)
            if not sl:
                continue
            S["vidas (diario-asiento)"] += 1
            S["partidas"] = len({os.path.dirname(x) for x in [f]} |
                                set())  # se recalcula abajo
            n, eps = episodios_de(f)
            S["tics vividos"] += n
            S["episodios de don"] += len(eps)
            S["intentos (tics soltar_*)"] += sum(e["intentos"] for e in eps)
            bucles = [e for e in eps if e["intentos"] >= MIN_BUCLE]
            tb = sum(e["fin"] - e["ini"] + 1 for e in bucles)
            S["episodios EN BUCLE"] += len(bucles)
            S["tics EN BUCLE"] += tb
            if bucles:
                S["vidas con bucle"] += 1
                porvida.append((tb, n, os.path.basename(os.path.dirname(f)), sl.group(1)))
                for e in bucles:
                    d = e["fin"] - e["ini"] + 1
                    if peor is None or d > peor[0]:
                        peor = (d, e["intentos"], n,
                                os.path.basename(os.path.dirname(f)),
                                sl.group(1), e["id"], list(e["casilla"]),
                                e["ini"], e["fin"])
            print(f"      {os.path.basename(os.path.dirname(f))} s{sl.group(1)}: "
                  f"{n} tics · {len(eps)} episodios · {len(bucles)} en bucle · "
                  f"{tb} tics", flush=True)
    return S, peor, porvida


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    pats = [os.path.join(RAIZ, p) for p in pat.split(",")]
    print(f"### {etiq}", flush=True)
    S, peor, porvida = mide(pats)
    S["partidas"] = len({p for tb, n, p, s in porvida}) or None
    n = S["tics vividos"] or 1
    OUT[etiq] = {"recuento": dict(S), "peor_episodio": peor,
                 "por_vida": sorted(porvida, reverse=True)[:10]}
    print(f"  {etiq}: {S['vidas (diario-asiento)']} vidas · {n} tics")
    for k in ("episodios de don", "intentos (tics soltar_*)",
              "episodios EN BUCLE", "tics EN BUCLE", "vidas con bucle"):
        print(f"    {k:28s} {S[k]:8d}")
    print(f"    {'% de tics en bucle':28s} {100 * S['tics EN BUCLE'] / n:8.2f} %")
    if peor:
        print(f"    peor episodio: {peor[0]} tics ({peor[1]} intentos) en "
              f"{peor[3]} s{peor[4]}, {peor[5]} en {peor[6]}, "
              f"tics {peor[7]}-{peor[8]} · {100 * peor[0] / peor[2]:.1f} % de esa vida")
json.dump(OUT, open(os.path.join(AQUI, "P6_6_bucle.json"), "w"),
          ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_6_bucle.json")

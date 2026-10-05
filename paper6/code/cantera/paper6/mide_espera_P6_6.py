"""[P6-6 · B2] CUANTO TARDA EL HERMANO EN LLEGAR AL REGALO. SOLO LECTURA.

Sirve para fijar el N de la regla de Manel «lo dado, dado esta»: el que suelta
no recoge durante N tics. Manel pone la base: N = distancia x 11. El margen hay
que justificarlo, y para eso se mide lo que de verdad tardo el hermano.

  11 tics por casilla NO se cablea: es `mundo.coste_movimiento(speed)` con el
  speed que trae la propia observacion (`you.stats.spd`). Si en algun diario el
  speed es otro, se usa el suyo.

  d         distancia Chebyshev (el mundo permite diagonales) de la casilla del
            regalo a la posicion REAL del hermano en el tic del don, leida de SU
            diario, no de lo que creia el que solto.
  espera    tics desde el final del episodio hasta que el hermano PISA la
            casilla. Solo se cuentan los dones EFECTIVOS (el que solto se fue
            sin recuperarlo); si nunca la pisa, no hay espera y se apunta aparte.
  margen    espera - d x coste. Lo que el camino real cuesta por encima de la
            linea recta: muros, rodeos, y que el hermano tenia otras cosas que
            hacer.

Uso:
  python3 mide_espera_P6_6.py 'A0=paintball/runs/P64_t[13]_A0_*' 'cinco=paintball/runs/P58M_*'
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U

HUECO = 3


def pista(f):
    """({tick: (pos, pack_n, hand, elegido)}, speed) de un diario.

    El `speed` se LEE del registro `arranque` del propio diario (el que la
    politica escribio al arrancar); si no esta, se deja None y el llamador usa
    el de por defecto del mundo. Prohibido cablearlo (CLAUDE.md).
    """
    T, speed = {}, None
    for r in U.lee(f):
        if r.get("k") == "arranque":
            speed = _busca_speed(r)
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        T[r["tick"]] = (tuple(int(x) for x in (r.get("pos") or ())),
                        {(s or {}).get("id"): int((s or {}).get("n") or 1)
                         for s in (r.get("pack") or []) if s},
                        (r.get("hand") or {}).get("id"),
                        str(((r.get("RADIOGRAFIA") or {}).get("elegido")) or ""))
    return T, speed


def _busca_speed(r, _rx=re.compile(r'"(?:spd|speed)"\s*:\s*(\d+)')):
    m = _rx.search(json.dumps(r))
    return int(m.group(1)) if m else None


def episodios(T):
    eps, abierto = [], {}
    for t in sorted(T):
        el = T[t][3]
        if not el.startswith("soltar_"):
            continue
        iid, cel = el[len("soltar_"):], T[t][0]
        k = (iid, cel)
        e = abierto.get(k)
        if e is not None and t - e["fin"] <= HUECO:
            e["fin"], e["intentos"] = t, e["intentos"] + 1
            continue
        e = {"id": iid, "casilla": cel, "ini": t, "fin": t, "intentos": 1}
        abierto[k] = e
        eps.append(e)
    return eps


def efectivo(T, e):
    """True si el objeto queda en el suelo al final del episodio."""
    iid, cel = e["id"], e["casilla"]
    npre = T[e["fin"]][1].get(iid, 0)
    for t in sorted(x for x in T if x > e["fin"]):
        pos, pk, _h, _el = T[t]
        if pos == cel and pk.get(iid, 0) >= npre:
            return False
        if pos != cel:
            return True
    return True


def mide(pats, coste_de):
    filas, S = [], collections.Counter()
    for pat in pats:
        for carp in sorted(glob.glob(pat)):
            fs = sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log")))
            E = {}
            for f in fs:
                m = re.search(r"policy_agent_(\d+)\.art\.log$", f)
                if m:
                    E[int(m.group(1))] = f
            if len(E) != 2:
                continue
            slots = sorted(E)
            P = {sl: pista(E[sl]) for sl in slots}
            for sl in slots:
                otro = slots[1] if sl == slots[0] else slots[0]
                T, speed = P[sl]
                To, _ = P[otro]
                coste = coste_de(speed)
                for e in episodios(T):
                    S["episodios"] += 1
                    if not efectivo(T, e):
                        S["reabsorbidos"] += 1
                        continue
                    S["efectivos"] += 1
                    iid, cel = e["id"], e["casilla"]
                    # distancia REAL del hermano en el tic del don
                    ph = To.get(e["fin"], (None,))[0]
                    if not ph:
                        S["sin rastro del hermano"] += 1
                        continue
                    d = max(abs(ph[0] - cel[0]), abs(ph[1] - cel[1]))
                    rec, ant = None, None
                    for tt in sorted(x for x in To if x > e["fin"]):
                        pos, pk, hand, _ = To[tt]
                        if pos == cel:
                            n0 = (ant or (None, pk, None, None))[1].get(iid, 0)
                            if pk.get(iid, 0) > n0 or (iid == (hand or "")
                                                       and iid != ((ant or (None, {}, "", ""))[2] or "")):
                                rec = tt
                                break
                        ant = To[tt]
                    fila = {"carp": os.path.basename(carp), "slot": sl,
                            "id": iid, "casilla": list(cel), "fin": e["fin"],
                            "d": d, "coste": coste, "recogido": rec,
                            "espera": (rec - e["fin"]) if rec else None,
                            "margen": (rec - e["fin"] - d * coste) if rec else None}
                    filas.append(fila)
                    S["recogidos" if rec else "NO recogidos"] += 1
            del P
    return filas, S


import importlib
_M = importlib.import_module("alma.mundo")


def coste_de(speed):
    # `Mundo.coste_movimiento` es un metodo de instancia pero no usa self:
    # se llama por la clase para no tener que montar un mundo por diario.
    return _M.Mundo.coste_movimiento(None, int(speed if speed else 5))


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    pats = [os.path.join(RAIZ, p) for p in pat.split(",")]
    filas, S = mide(pats, coste_de)
    OUT[etiq] = {"recuento": dict(S), "filas": filas}
    print(f"### {etiq}")
    for k, v in S.most_common():
        print(f"   {k:26s} {v}")
    rec = [f for f in filas if f["recogido"]]
    if rec:
        es = [f["espera"] for f in rec]
        mg = [f["margen"] for f in rec]
        ds = [f["d"] for f in rec]
        print(f"   de los recogidos ({len(rec)}):")
        print(f"     d (casillas)   min {min(ds)} · mediana {st.median(ds):g} · max {max(ds)}")
        print(f"     espera (tics)  min {min(es)} · mediana {st.median(es):g} · max {max(es)}")
        print(f"     margen (tics)  min {min(mg)} · mediana {st.median(mg):g} · max {max(mg)}")
        mgo = sorted(mg)
        for q in (0.5, 0.75, 0.9, 1.0):
            i = min(len(mgo) - 1, int(round(q * (len(mgo) - 1))))
            print(f"     margen p{int(q*100):3d}    {mgo[i]}")
        print(f"     coste por casilla usado: {sorted({f['coste'] for f in rec})}")
json.dump(OUT, open(os.path.join(AQUI, "P6_6_espera.json"), "w"),
          ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_6_espera.json")

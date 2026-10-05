"""[P6-7] QUIEN SE ALEJA, Y QUE ESTABA HACIENDO. SOLO LECTURA.

Una EXCURSION empieza en el primer tic en que la distancia entre los dos pasa
de LEJOS casillas (viniendo de <= LEJOS) y acaba cuando vuelve a <= LEJOS o uno
muere. Se atribuye "el que se aleja" al asiento que mas se movio respecto a su
posicion al inicio de la excursion durante sus primeros VENT tics, y se cuenta
que eligio (familia de `elegido`) en esos tics, si tenia recurso o rival
contado en la percepcion (reconstruido del E2 del hermano, como en P6-4), y si
tenia R-ACOPIO / F-HERMANO-AMENAZA encendidas.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U
import parte2 as P2
import oyente2 as OY

LEJOS, VENT = 8, 60


def fam(e):
    e = str(e or "")
    for p in ("soltar_", "usar_", "ir_", "move_", "paso_", "atacar", "coger", "noop"):
        if e.startswith(p):
            return p.rstrip("_") if p != "ir_" else e[:12]
    return e or "otro"


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map")
    cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); herm = pc.get("teammate_slot")
    T = {}; ult = None
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        for m in (r.get("chat") or []):
            if m.get("channel") == "team" and m.get("from") == herm and (m.get("text") or "").startswith("E2 "):
                p = P2.parsea(m["text"], mundo)
                if p:
                    ult = p
        t = r["tick"]; vistos = {a.get("slot") for a in (r.get("ve_agentes") or [])}
        riv = rec = 0
        if ult and 0 <= t - ult["t"] <= OY.CADUCIDAD_RIVAL:
            riv = sum(1 for x in ult["rivales"] if x["slot"] not in vistos)
        if ult and t - ult["t"] >= 0 and OY.peso_recurso(t - ult["t"]) >= OY.UMBRAL_REC:
            rec = len(ult["recursos"])
        ra = r.get("RADIOGRAFIA") or {}; fl = ((ra.get("ahora") or {}).get("filas")) or {}
        T[t] = {"pos": tuple(int(x) for x in r["pos"]), "el": ra.get("elegido"),
                "riv": riv, "rec": rec, "acopio": "R-ACOPIO" in fl, "amen": "F-HERMANO-AMENAZA" in fl}
    del recs
    return T


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); EX = []
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f
              for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if 10 not in fs or 11 not in fs:
            continue
        A, B = carga(fs[10]), carga(fs[11])
        com = sorted(set(A) & set(B)); dentro = None
        for i, t in enumerate(com):
            d = cheb(A[t]["pos"], B[t]["pos"])
            if dentro is None and d > LEJOS and i > 0 and cheb(A[com[i-1]]["pos"], B[com[i-1]]["pos"]) <= LEJOS:
                dentro = t
            elif dentro is not None and d <= LEJOS:
                EX.append((carp, dentro, t)); dentro = None
        if dentro is not None:
            EX.append((carp, dentro, com[-1]))
        for carp_, t0, t1 in [e for e in EX if e[0] == carp]:
            S["excursiones (> %d casillas)" % LEJOS] += 1
            S["tics en excursion"] += t1 - t0
            v = [t for t in com if t0 <= t < t0 + VENT]
            mA = cheb(A[v[-1]]["pos"], A[v[0]]["pos"]); mB = cheb(B[v[-1]]["pos"], B[v[0]]["pos"])
            quien, T = (10, A) if mA >= mB else (11, B)
            S[f"se aleja el asiento {quien}"] += 1
            c = collections.Counter(fam(T[t]["el"]) for t in v)
            for k, n in c.items():
                S[f"  el que se aleja elige {k}"] += n
            S["  ...con RIVAL contado en la percepcion (tics)"] += sum(1 for t in v if T[t]["riv"])
            S["  ...con RECURSO contado en la percepcion (tics)"] += sum(1 for t in v if T[t]["rec"])
            S["  ...con R-ACOPIO encendida (tics)"] += sum(1 for t in v if T[t]["acopio"])
            S["  ...con F-HERMANO-AMENAZA encendida (tics)"] += sum(1 for t in v if T[t]["amen"])
            S["  tics mirados"] += len(v)
        del A, B
    OUT[etiq] = {"recuento": dict(S), "excursiones": [(os.path.basename(c), a, b) for c, a, b in EX]}
    print(f"### {etiq}")
    for k, v in S.items():
        print(f"  {k:52s} {v}")
    if EX:
        dur = [b - a for _, a, b in EX]
        print(f"  duracion: mediana {st.median(dur):.0f} · max {max(dur)}")
json.dump(OUT, open(os.path.join(AQUI, "P6_11_separa.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_11_separa.json")

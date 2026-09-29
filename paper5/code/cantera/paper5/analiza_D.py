"""[P5-1 fase D] D1, D2 y D3 sobre los seis asientos-partida. Coste cero.

SOLO LECTURA de diarios. Nada se lanza.

LAS TRES TENSIONES no estan en el diario, pero se reconstruyen EXACTAMENTE de
el: `appraisal_zs_v42_exp.py:1684-1698` reparte cada fila en sus tres ejes
(F, R, S) y las suma en pF/nF/pR/nR/pS/nS segun el signo; el diario guarda ya
esos tres sumandos por fila (`"F"`, `"R"`, `"S"`) y el signo. Aqui se suman
igual y se pasan por `State` de `motor/model.py`, que aplica el minimo basal y
el techo de volumen. La `d` sale de `opponent_distance` del propio motor.
Ninguna constante se copia a mano.
"""
from __future__ import annotations
import collections, glob, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from motor.model import DEFAULT_CONFIG, State, opponent_distance   # noqa: E402
from alma.appraisal_zs_v42_exp import APETITIVAS, W_TARGET         # noqa: E402

IGNICION = 481


def recs_de(f):
    for ln in open(f):
        try:
            yield json.loads(ln)
        except Exception:
            pass


def fuerzas(filas):
    """Las seis fuerzas crudas, del reparto que el diario ya trae por fila."""
    pF = nF = pR = nR = pS = nS = 0.0
    for nom, v in (filas or {}).items():
        if not isinstance(v, dict) or not v.get("M"):
            continue
        aF, aR, aS = (float(v.get("F") or 0.0), float(v.get("R") or 0.0),
                      float(v.get("S") or 0.0))
        if v.get("signo") == "+" or nom in APETITIVAS:
            pF += aF; pR += aR; pS += aS
        else:
            nF += aF; nR += aR; nS += aS
    return pF, nF, pR, nR, pS, nS


def serie(f):
    """La pelicula de una vida: un punto por tic vivo."""
    out = []
    vistos_suelo, cogidos = set(), 0
    golpes = []
    prim_armado = None
    for r in recs_de(f):
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        R = r.get("RADIOGRAFIA") or {}
        a = R.get("ahora") or {}
        if not a:
            continue
        t = r["tick"]
        pF, nF, pR, nR, pS, nS = fuerzas(a.get("filas"))
        st = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
        car = ((a.get("filas") or {}).get("R-CARENCIA") or {}).get("M") or 0.0
        el = R.get("elegido") or ""
        cand = (R.get("candidatos") or {}).get(el)
        out.append({
            "t": t, "hp": r.get("hp"), "W": a.get("W"),
            "R-CARENCIA": car,
            "tF": st.pF - st.nF, "tR": st.pR - st.nR, "tS": st.pS - st.nS,
            "nF": st.nF, "nR": st.nR, "nS": st.nS,
            "d_estado": opponent_distance(st, DEFAULT_CONFIG),
            "d_elegido": (cand.get("d") if isinstance(cand, dict) else cand),
            "elegido": el})
        for it in (r.get("ve_items") or []):
            if it.get("pos"):
                vistos_suelo.add((it.get("id"), tuple(it["pos"])))
        if el.startswith("coger") and r.get("action_result") == "ok":
            cogidos += 1
        for g in (r.get("damage_taken") or []):
            golpes.append((t, g.get("source"), g.get("amount")))
        if prim_armado is None and t >= IGNICION:
            herm = None
            for x in (r.get("ve_agentes") or []):
                if (x.get("hand") or "none") not in (None, "none", "net"):
                    prim_armado = (t, x.get("slot"), x.get("hand"))
                    break
    return out, vistos_suelo, cogidos, golpes, prim_armado


def mide(f, parts):
    s, suelo, cogidos, golpes, armado = serie(f)
    n = len(s)
    if not n:
        return None
    W = [x["W"] or 0.0 for x in s]

    def primero(u):
        for x in s:
            if (x["W"] or 0.0) >= u - 1e-9:
                return x["t"]
        return None
    tres = [x for x in s if (x["W"] or 0.0) >= 3.0]
    g2000 = collections.Counter()
    for t, src, _amt in golpes:
        if t <= 2000 and isinstance(src, str) and src.startswith("P") \
                and src[1:].isdigit():
            g2000[parts.get(int(src[1:]), f"asiento {src[1:]}")] += 1
        elif t <= 2000:
            g2000[str(src)] += 1
    return {
        "tics vivos": n, "serie": s,
        "W": {"min": min(W), "max": max(W), "mediana": sorted(W)[n // 2],
              "primer tic con W>=1": primero(1.0),
              "primer tic con W>=2": primero(2.0),
              "primer tic con W>=3": primero(3.0),
              "tics con W>=3": len(tres),
              "fraccion con W>=3": len(tres) / n,
              "R-CARENCIA media en esos tics":
                  (sum(x["R-CARENCIA"] for x in tres) / len(tres))
                  if tres else None},
        "R-CARENCIA": {"min": min(x["R-CARENCIA"] for x in s),
                       "max": max(x["R-CARENCIA"] for x in s),
                       "mediana": sorted(x["R-CARENCIA"] for x in s)[n // 2]},
        "objetos distintos vistos en el suelo": len(suelo),
        "veces que cogio algo (accion ok)": cogidos,
        "golpes recibidos hasta el tic 2000, por politica": dict(g2000),
        "primer armado a la vista": armado,
    }


def main():
    out = {}
    for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P5_*"))):
        nom = os.path.basename(carp)
        pj = os.path.join(AQUI, nom.replace("P5_", "") + "_peticion.json")
        parts = {}
        if os.path.exists(pj):
            d = json.load(open(pj))
            parts = {p["position"]: p["policy_name"]
                     for p in d["episodes"][0]["participants"]}
        for f in sorted(glob.glob(os.path.join(carp, "*.art.log"))):
            k = nom + "/" + os.path.basename(f).split("policy_agent_")[1][:2].strip(".")
            m = mide(f, parts)
            if m:
                out[k] = m
    # los cinco diarios de S-2 brazo A, para comparar
    s2 = {}
    for f in sorted(glob.glob(os.path.join(
            RAIZ, "paintball", "runs", "S2_A", "*policy_agent_1*.art.log")))[:5]:
        m = mide(f, {})
        if m:
            s2["S2_A/" + os.path.basename(f)[5:13] + "-" +
               os.path.basename(f).split("policy_agent_")[1][:2].strip(".")] = m
    resumen = {k: {a: b for a, b in v.items() if a != "serie"}
               for k, v in list(out.items()) + list(s2.items())}
    json.dump(resumen, open(os.path.join(AQUI, "D_medidas.json"), "w"),
              ensure_ascii=False, indent=1)
    json.dump({k: v["serie"] for k, v in out.items()},
              open(os.path.join(AQUI, "D_series.json"), "w"), ensure_ascii=False)
    print(f"W_TARGET del cuerpo = {W_TARGET}")
    for k, v in list(out.items()) + list(s2.items()):
        w = v["W"]
        print(f"\n=== {k} · {v['tics vivos']:,} tics vivos")
        print(f"  W: min {w['min']} · mediana {w['mediana']} · max {w['max']} · "
              f"1º W>=1 {w['primer tic con W>=1']} · >=2 {w['primer tic con W>=2']}"
              f" · >=3 {w['primer tic con W>=3']} · tics con W>=3 "
              f"{w['tics con W>=3']} ({100*w['fraccion con W>=3']:.2f} %)")
        print(f"  R-CARENCIA: min {v['R-CARENCIA']['min']} · mediana "
              f"{v['R-CARENCIA']['mediana']} · max {v['R-CARENCIA']['max']}")
        print(f"  objetos distintos en el suelo {v['objetos distintos vistos en el suelo']} · "
              f"cogio {v['veces que cogio algo (accion ok)']}")
        if v["golpes recibidos hasta el tic 2000, por politica"]:
            print(f"  golpes hasta el 2000: "
                  f"{v['golpes recibidos hasta el tic 2000, por politica']}")


if __name__ == "__main__":
    main()

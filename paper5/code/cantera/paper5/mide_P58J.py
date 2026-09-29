"""[P5-8J] La puerta, en seco: ventaja y margen tal como los escribio el codigo.

La ruta de juicio es BYTE A BYTE IDENTICA entre la imagen de E y la de H/I
(`forma.py`, `confianza_viva.py`, `_juzga`, el renglon). Asi que comparar las
`ventaja` que cada sonda escribio ES comparar el mismo codigo sobre estados
distintos.
"""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U


def q(v, p):
    if not v: return None
    s = sorted(v); i = (len(s) - 1) * p
    lo, hi = int(i), min(int(i) + 1, len(s) - 1)
    return round(s[lo] + (s[hi] - s[lo]) * (i - lo), 5)


SONDAS = {"E": "P58E_t1_K_*", "H": "P58H_t1_K_*", "I": "P58I_t1_K_*"}
OUT = {}
for sonda, pat in SONDAS.items():
    filas = []
    for f in sorted(glob.glob(f"paintball/runs/{pat}/*.art.log")):
        recs = list(U.lee(f))
        prop = {r["id"]: r for r in recs
                if r.get("k") == "forma_propuesta" and r.get("origen") == "curiosidad"}
        if not prop: continue
        carpeta = os.path.basename(os.path.dirname(f))
        slot = f.rsplit("_", 1)[1][:2]
        nom = f"{sonda}/{carpeta.split('_')[3]}/{slot}"
        # los tics vivos, para saber cuantos tics hubo forma activa
        vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
        ctic = [r for r in recs if r.get("k") == "cur_forma_tic"]
        dentro = sum(1 for r in ctic if r.get("activa") is not None)
        salt = collections.Counter(r.get("motivo") for r in recs
                                   if r.get("k") == "cur_forma_saltada")
        ev = [r for r in recs if r.get("k") == "forma_evaluada" and r.get("id") in prop]
        ven = [r["ventaja"] for r in ev if r.get("ventaja") is not None]
        mg = [r["margen"] for r in ev if r.get("margen") is not None]
        Cs = [r["C"] for r in ev if r.get("C") is not None]
        ver = collections.Counter(r.get("veredicto") for r in ev)
        filas.append({
            "asiento": nom, "tics": len(vivos), "dentro": dentro,
            "nacidas": len(prop), "evaluadas": len(ev),
            "aceptadas": ver.get("ok", 0),
            "veredictos": dict(ver), "saltadas": dict(salt),
            "ventaja": {"n": len(ven), "min": q(ven, 0), "q1": q(ven, .25),
                        "med": q(ven, .5), "q3": q(ven, .75), "max": q(ven, 1)},
            "margen": {"med": q(mg, .5), "min": q(mg, 0), "max": q(mg, 1)},
            "C": {"med": q(Cs, .5), "min": q(Cs, 0), "max": q(Cs, 1)},
            "_ven": ven, "_mg": mg,
        })
        print(f"  {nom:16s} {len(prop):4d} nacidas · {len(ev):4d} evaluadas · "
              f"{ver.get('ok',0):3d} ok · ventaja med "
              f"{q(ven,.5)} · margen med {q(mg,.5)} · C med {q(Cs,.5)}", flush=True)
    OUT[sonda] = filas

json.dump({k: [{kk: vv for kk, vv in f.items() if not kk.startswith('_')}
               for f in v] for k, v in OUT.items()},
          open("cantera/paper5/P58J.json", "w"), ensure_ascii=False, indent=1)

print("\n=== AGREGADO POR SONDA ===")
print(f"{'':6s} {'nace':>6s} {'eval':>6s} {'ok':>4s} {'%':>6s} "
      f"{'ventaja med':>11s} {'q3':>8s} {'margen med':>10s} {'ok/ven>mg':>9s}")
for s, filas in OUT.items():
    ven = [x for f in filas for x in f["_ven"]]
    mg = [x for f in filas for x in f["_mg"]]
    na = sum(f["nacidas"] for f in filas); ev = sum(f["evaluadas"] for f in filas)
    ok = sum(f["aceptadas"] for f in filas)
    par = [(v, m) for f in filas for v, m in zip(f["_ven"], f["_mg"])]
    sup = sum(1 for v, m in par if v > m)
    print(f"{s:6s} {na:6d} {ev:6d} {ok:4d} {100.0*ok/max(ev,1):5.1f}% "
          f"{q(ven,.5):>11} {q(ven,.75):>8} {q(mg,.5):>10} {sup:9d}")

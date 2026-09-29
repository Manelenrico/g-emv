"""[P5-FIG · 4 y 5] Datos de las figuras del cuerpo curioso. SOLO LECTURA."""
import glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U, curiosidad as C

PASO = 200


def curva(f, paso=PASO):
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        return None, None, None
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    ojo = C.Ojo(mundo, 8)
    xs, ys = [], []
    vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
    for i, r in enumerate(vivos):
        p = tuple(r.get("pos") or ())
        if p:
            ojo.mira(p, r["tick"])
        if i % paso == 0:
            xs.append(r["tick"]); ys.append(round(ojo.ignorancia_global(), 5))
    if vivos:
        xs.append(vivos[-1]["tick"]); ys.append(round(ojo.ignorancia_global(), 5))
    return xs, ys, recs


# ── F1: todas las curvas, y la mediana por brazo ──
CUR = {"A": [], "K": []}
for brazo in ("A", "K"):
    for f in sorted(glob.glob(f"paintball/runs/P58M_t*_{brazo}_*/*.art.log")):
        xs, ys, _ = curva(f)
        if xs:
            CUR[brazo].append([xs, ys])
    print(f"  {brazo}: {len(CUR[brazo])} curvas", flush=True)

MED = {}
for brazo in ("A", "K"):
    mx, my, mn = [], [], []
    for t in range(0, 15001, PASO):
        v = []
        for xs, ys in CUR[brazo]:
            if xs[0] <= t <= xs[-1]:
                i = min(range(len(xs)), key=lambda j: abs(xs[j] - t))
                v.append(ys[i])
        if len(v) >= 5:
            mx.append(t); my.append(st.median(v)); mn.append(len(v))
    MED[brazo] = {"x": mx, "y": my, "n": mn}

# ── F2: el asiento de K con mas viajes aceptados ──
mejor, n_mejor = None, -1
for f in sorted(glob.glob("paintball/runs/P58M_t*_K_*/*.art.log")):
    n = sum(1 for l in open(f) if '"forma_aceptada"' in l)
    if n > n_mejor:
        mejor, n_mejor = f, n
xs, ys, recs = curva(mejor, paso=25)
acep = [r for r in recs if r.get("k") == "forma_aceptada"]
caid = {r["id"]: (r["tick"], str(r.get("motivo") or "")) for r in recs
        if r.get("k") == "forma_caida"}
viajes = []
for a in acep:
    t0 = a["tick"]; t1, mot = caid.get(a.get("id"), (t0, "sin fin"))
    viajes.append({"id": a.get("id"), "t0": t0, "t1": t1, "motivo": mot})

json.dump({"F1": {"medianas": MED, "n_curvas": {k: len(v) for k, v in CUR.items()},
                  "curvas": CUR, "paso": PASO},
           "F2": {"diario": mejor, "asiento": os.path.basename(os.path.dirname(mejor))
                  + "/" + mejor.rsplit("_", 1)[1][:2],
                  "x": xs, "y": ys, "viajes": viajes}},
          open("cantera/paper5/FIG45_datos.json", "w"))
print(f"  F2: {os.path.basename(os.path.dirname(mejor))} · {len(viajes)} viajes")
import collections
print("  motivos:", dict(collections.Counter(v["motivo"][:24] for v in viajes)))

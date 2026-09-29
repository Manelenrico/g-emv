"""[P5-AP2] Quien nos mato y quien nos pego, en los 216 episodios del paper cinco.

SOLO LECTURA. Misma regla de atribucion que `E3_golpes.py`: la muerte va al
ultimo golpe REGISTRADO en los 48 tics anteriores al `match_ticks` del propio
diario; si no hay ninguno, «no consta».
"""
import collections, glob, json, os, statistics as st

AQUI = "cantera/paper5"
RUNS = "paintball/runs"
VENTANA = 48                      # la misma de E3_golpes.py

muertes = collections.Counter()
muertes_ser = collections.defaultdict(collections.Counter)
golpes = collections.Counter()
golpes_ser = collections.defaultdict(collections.Counter)
tics_relh = []
tics_todas = collections.defaultdict(list)
c = collections.Counter()
rivales_vistos = collections.Counter()

for p in sorted(glob.glob(f"{AQUI}/*.json")):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    if not isinstance(d, dict) or "_brazo" not in d:
        continue
    eps = d.get("episodes") or []
    if not eps:
        continue
    e = eps[0]
    parts = e.get("participants") or []
    if not parts:
        c["episodios sin participants"] += 1
        continue
    pos2nom = {str(x.get("position")): x.get("policy_name") for x in parts
               if x.get("position") is not None}
    for x in parts:
        if x.get("position") not in (10, 11):
            rivales_vistos[x.get("policy_name")] += 1
    base = os.path.basename(p)[:-5]
    ser = base.split("_t")[0] if "_t" in base else base.split("_")[0]
    carp = os.path.join(RUNS, base)
    if not os.path.isdir(carp):
        c["sin carpeta de diarios"] += 1
        continue
    c["episodios con diarios"] += 1
    for f in sorted(glob.glob(os.path.join(carp, "*.art.log"))):
        c["diarios"] += 1
        fin, ult = None, []
        for ln in open(f, encoding="utf-8", errors="replace"):
            if '"k": "final"' in ln or '"k":"final"' in ln:
                try:
                    fin = json.loads(ln)
                except Exception:
                    pass
                continue
            if '"damage_taken": [{' not in ln and '"damage_taken":[{' not in ln:
                continue
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if r.get("k") != "tick" or r.get("phase") != "live":
                continue
            t = r["tick"]
            for g in (r.get("damage_taken") or []):
                s = g.get("source")
                if s == "zone":
                    nom = "el anillo"
                elif isinstance(s, str) and s.startswith("P") and s[1:].isdigit():
                    nom = pos2nom.get(s[1:], f"asiento {s[1:]}")
                else:
                    nom = str(s)
                ult.append((t, nom))
                golpes[nom] += 1
                golpes_ser[ser][nom] += 1
        if not fin:
            c["diarios sin final"] += 1
            continue
        if str(fin.get("reason") or "") != "eliminated":
            c["no eliminados (" + str(fin.get("reason")) + ")"] += 1
            continue
        c["eliminados"] += 1
        mt = fin.get("match_ticks") or 0
        cerca = [n for t, n in ult if mt - VENTANA <= t <= mt]
        quien = cerca[-1] if cerca else "no consta"
        muertes[quien] += 1
        muertes_ser[ser][quien] += 1
        tics_todas[quien].append(mt)
        if quien == "relh-zero-sum":
            tics_relh.append(mt)

json.dump({"muertes": dict(muertes), "golpes": dict(golpes),
           "por_serie_muertes": {k: dict(v) for k, v in muertes_ser.items()},
           "por_serie_golpes": {k: dict(v) for k, v in golpes_ser.items()},
           "tics_por_matador": {k: v for k, v in tics_todas.items()},
           "recuento": dict(c), "rivales": dict(rivales_vistos)},
          open(f"{AQUI}/P5AP2.json", "w"), ensure_ascii=False)

print("=== recuento ===")
for k, v in c.most_common():
    print(f"   {k:34s} {v}")
tot = sum(muertes.values())
print(f"\n=== 1 · QUIEN NOS MATO · {tot} muertes ===")
for k, v in muertes.most_common():
    print(f"   {k:36s} {v:4d}  {100.0*v/tot:5.2f} %")
if tics_relh:
    print(f"\n=== 2 · relh-zero-sum: {len(tics_relh)} muertes = "
          f"{100.0*len(tics_relh)/tot:.2f} %")
    print(f"   tic de la muerte: mediana {st.median(tics_relh):.0f} · "
          f"min {min(tics_relh)} · max {max(tics_relh)}")
tg = sum(golpes.values())
print(f"\n=== 3 · GOLPES RECIBIDOS · {tg} ===")
for k, v in golpes.most_common():
    print(f"   {k:36s} {v:6d}  {100.0*v/tg:5.2f} %")

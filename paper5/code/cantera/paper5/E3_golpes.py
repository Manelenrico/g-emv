"""[P5-1 E3] Golpes recibidos antes del tic 2.000 y muertes nuestras, por
politica rival, sobre TODOS los diarios de S-2 y S-3. SOLO LECTURA.

La MUERTE se atribuye al ultimo golpe REGISTRADO en los 48 tics anteriores al
`match_ticks` del diario. El diario no guarda el golpe que mata (el cuerpo deja
de observar al morir), asi que cuando no hay ninguno se cuenta como "no consta".
"""
import collections, glob, json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PART = json.load(open(os.path.join(AQUI, "E3_participantes.json")))
CARP = ("S2_A", "S2_B", "S2_C", "S2_Aconf",
        "S3_D0", "S3_D100", "S3_T", "S3_humo_D300", "S3_humo2_D300")
CORTE = 2000

golpes = collections.Counter()
golpes_ep = collections.Counter()
muertes = collections.Counter()
c = collections.Counter()
for carp in CARP:
    d = os.path.join(RAIZ, "paintball", "runs", carp)
    if not os.path.isdir(d):
        continue
    for f in sorted(glob.glob(os.path.join(d, "*-policy_agent_1*.art.log"))):
        ereq = os.path.basename(f).split("-policy_agent_")[0]
        p = (PART.get(ereq) or {}).get("participants") or {}
        c["diarios"] += 1
        c[carp] += 1
        fin = None
        ult = []
        for ln in open(f, encoding="utf-8", errors="replace"):
            if '"k":"final"' in ln:
                try:
                    fin = json.loads(ln)
                except Exception:
                    pass
                continue
            if '"damage_taken":[{' not in ln:
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
                nom = ("el anillo" if s == "zone" else
                       p.get(str(s)[1:], f"asiento {str(s)[1:]}")
                       if isinstance(s, str) and s.startswith("P")
                       and s[1:].isdigit() else str(s))
                ult.append((t, nom))
                if t < CORTE:
                    golpes[nom] += 1
                    golpes_ep[nom] += 0
        c["diarios con final"] += fin is not None
        if fin and (fin.get("match_ticks") or 0) < CORTE:
            c["muertes antes del 2000"] += 1
            mt = fin["match_ticks"]
            cerca = [n for t, n in ult if mt - 48 <= t <= mt]
            muertes[cerca[-1] if cerca else "no consta"] += 1
        elif fin:
            c["vivos pasado el 2000"] += 1
out = {"recuento": dict(c),
       "golpes antes del tic 2000, por politica": dict(golpes.most_common()),
       "muertes nuestras antes del tic 2000, por politica":
           dict(muertes.most_common())}
json.dump(out, open(os.path.join(AQUI, "E3_golpes.json"), "w"),
          ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))

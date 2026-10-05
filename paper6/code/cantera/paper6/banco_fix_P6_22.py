"""[P6-22 · 4] EL BANCO DE P6-15 REPETIDO CON EL ARREGLO: ¿cambia algun veredicto?
El arreglo de P6-22 sustituye la copia profunda (`copy.deepcopy`, puro Python, 200-360 ms en
el hilo principal) por una INSTANTANEA por serializacion (`pickle` ida y vuelta, en C) que es
tambien lo que viaja a un proceso aparte. Si la instantanea no es identica a la copia
profunda en lo que la puerta mira, algun veredicto cambiara. Aqui se repiten vidas del banco
de P6-15 (`banco_P6_15.vida`, tal cual) con `copy.deepcopy` sustituido por la instantanea
en TODO el proceso (la puerta del cinco, el comparador puerta6, el arnes), y se compara plan a
plan con lo grabado en `P6_15_planes.json`: veredicto y ventaja de la puerta del cinco, del
comparador real y del rollout (cada 1, 6 y 11).

    python3 banco_fix_P6_22.py CARPETA SLOT [CARPETA SLOT ...]   -> P6_22_banco_fix.json
"""
import json, os, pickle, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import copy as _copy


def instantanea(x):
    """La misma copia que `puerta_proceso_P6_22.instantanea` (pickle ida y vuelta, en C); se
    repite aqui porque ese modulo exige el entorno de A6 y este banco el del cuerpo solo."""
    return pickle.loads(pickle.dumps(x, protocol=pickle.HIGHEST_PROTOCOL))


_copy.deepcopy = instantanea          # el arreglo, en todo el proceso
import banco_P6_15 as B
GRAB = json.load(open(os.path.join(AQUI, "P6_15_planes.json")))["planes"]
args = sys.argv[1:]; pares = [(args[i], int(args[i + 1])) for i in range(0, len(args), 2)]
R = {"nota": "P6-22 §4. Banco de P6-15 repetido con instantanea (pickle) en vez de copia profunda. Comparacion plan a plan.", "vidas": []}
for carp, slot in pares:
    t0 = time.time()
    res = B.vida(carp, slot, None, None, callado=True, cada=1)
    grab = [p for p in GRAB if p.get("carp") == carp and p.get("slot") == slot]
    nuevos = [dict(p, tick=d["tick"]) for d in res["decisiones"] for p in (d.get("planes") or [])]
    comp = {"carp": carp, "slot": slot, "planes_grabados": len(grab), "planes_nuevos": len(nuevos), "segundos": round(time.time() - t0, 1), "iguales": 0, "distintos": [], "sin_pareja": 0}
    idx = {}
    for p in grab:
        idx.setdefault((p["tick"], tuple(p.get("destino") or ()), tuple(p.get("criterios") or [])), []).append(p)
    for p in nuevos:
        k = (p["tick"], tuple(p.get("destino") or ()), tuple(p.get("criterios") or []))
        cand = idx.get(k)
        if not cand:
            comp["sin_pareja"] += 1; continue
        g = cand.pop(0)
        difs = {}
        for campo in ("veredicto", "ventaja"):
            if p.get(campo) != g.get(campo):
                difs[campo] = [g.get(campo), p.get(campo)]
        for cd in ("1", "6", "11"):
            a = (g.get("rollout") or {}).get(cd) or {}; b = (p.get("rollout") or {}).get(cd) or {}
            for campo in ("veredicto", "ventaja"):
                if a.get(campo) != b.get(campo):
                    difs[f"rollout_{cd}_{campo}"] = [a.get(campo), b.get(campo)]
        a = g.get("real") or {}; b = p.get("real") or {}
        for campo in ("veredicto", "ventaja"):
            if a.get(campo) != b.get(campo):
                difs[f"real_{campo}"] = [a.get(campo), b.get(campo)]
        if difs:
            comp["distintos"].append({"tick": p["tick"], "destino": p.get("destino"), "criterios": p.get("criterios"), "difs": difs})
        else:
            comp["iguales"] += 1
    R["vidas"].append(comp)
    print(f"{carp} s{slot}: grabados {len(grab)} nuevos {len(nuevos)} iguales {comp['iguales']} distintos {len(comp['distintos'])} sin pareja {comp['sin_pareja']} · {comp['segundos']} s", flush=True)
    for d in comp["distintos"][:10]:
        print("   ", json.dumps(d, ensure_ascii=False)[:300])
    json.dump(R, open(os.path.join(AQUI, "P6_22_banco_fix.json"), "w"), ensure_ascii=False, indent=1)
print("-> P6_22_banco_fix.json")

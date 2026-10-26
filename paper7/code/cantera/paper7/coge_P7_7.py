"""[P7-7, decision 3] ¿Que objeto toma el mundo cuando hay varios en la misma casilla? Sobre los 80 diarios de A4 del seis y los 12 de los
humos de P7-5 y P7-6: en cada `pickup` que gana algo (el inventario del tic siguiente tiene una unidad mas de alguna clase), con dos o mas
clases distintas en `ve_items` de mi casilla en el tic del pickup, se apunta que clase entro y en que posicion de la lista iba (primera,
ultima, otra), su kind del catalogo, y si era la clase que mas unidades tenia. -> P7_7_coge.json"""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
def unidades(r):
    c = collections.Counter(); h = r.get("hand") or {}
    if h.get("id") not in (None, "none"): c[h["id"]] += int(h.get("n") or 1)
    for s in r.get("pack") or []:
        if s: c[s["id"]] += int(s.get("n") or 1)
    if r.get("body"): c[r["body"] if isinstance(r["body"], str) else r["body"].get("id")] += 1
    return c
casos = []; cat = None
pats = ["P611_t1_A4_*", "P611_t2_A4_*", "P624_t1_A4_*", "P75_humo_APRENDE_*", "P76_humo_APRENDE_*"]
for pat in pats:
    for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))):
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_*.art.log"))):
            prev = None
            for line in open(f):
                if '"catalogo"' in line[:30] and cat is None: cat = {c["id"]: c for c in json.loads(line)["items"]}
                if '"k":"tick"' not in line and '"k": "tick"' not in line: continue
                r = json.loads(line)
                if prev is not None and prev["tick"] == r["tick"] - 1 and (prev.get("intencion") or {}).get("do") == "pickup":
                    up, un = unidades(prev), unidades(r); gan = [i for i in un if un[i] > up[i]]
                    aqui = [it for it in (prev.get("ve_items") or []) if tuple(it.get("pos") or ()) == tuple(prev["pos"])]
                    ids = [it["id"] for it in aqui]
                    if gan and len(set(ids)) >= 2:
                        g = gan[0]; idx = ids.index(g) if g in ids else None
                        casos.append({"vida": os.path.basename(carp) + "/" + os.path.basename(f)[-14:-8], "t": prev["tick"], "ids_en_casilla": ids, "n": [it.get("n") for it in aqui], "cogido": g, "posicion_en_lista": ("primera" if idx == 0 else "ultima" if idx == len(ids) - 1 else "otra" if idx is not None else "no listado"), "indice": idx, "kind": (cat.get(g) or {}).get("kind") if cat else None,
                                      "mas_unidades": (g == max(aqui, key=lambda it: int(it.get("n") or 1))["id"]), "cabe_apilado": any((s or {}).get("id") == g for s in prev.get("pack") or []), "otras_cabian": [i for i in set(ids) if i != g and any((s or {}).get("id") == i for s in prev.get("pack") or [])]})
                prev = r
R = {"casos": len(casos), "posicion": dict(collections.Counter(c["posicion_en_lista"] for c in casos)), "kind_cogido": dict(collections.Counter(c["kind"] for c in casos)), "mas_unidades": sum(1 for c in casos if c["mas_unidades"]),
     "primera_y_no_cabia_otra": sum(1 for c in casos if c["posicion_en_lista"] == "primera"), "cogido_apilable_en_zurron": sum(1 for c in casos if c["cabe_apilado"]),
     "cuando_la_primera_no_es_la_cogida": [{k: c[k] for k in ("vida", "t", "ids_en_casilla", "cogido", "cabe_apilado", "otras_cabian")} for c in casos if c["posicion_en_lista"] != "primera"][:12],
     "pares_ordenados": dict(collections.Counter(f"{c['ids_en_casilla'][0]} + {c['ids_en_casilla'][-1]} -> {c['cogido']}" for c in casos if len(c["ids_en_casilla"]) == 2).most_common(12))}
json.dump({"resumen": R, "casos": casos}, open(os.path.join(AQUI, "P7_7_coge.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))

# ── segunda medida: (a) pickups con dos o mas clases en la casilla que NO ganan nada: ¿habria cabido otra clase que no era la primera?
# (si el mundo saltara a la segunda, aqui habria ganancias; si no, el mundo se queda en la primera y no entrega nada);
# (b) tras un `drop`, ¿donde aparece lo soltado en la lista de mi casilla al tic siguiente: primero o ultimo?
def cabe(pack, cid, n):
    return any((s or {}).get("id") == cid for s in pack) or any(s is None for s in pack)
nada = []; soltados = []
for pat in pats:
    for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))):
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_*.art.log"))):
            prev = None
            for line in open(f):
                if '"k":"tick"' not in line and '"k": "tick"' not in line: continue
                r = json.loads(line)
                if prev is not None and prev["tick"] == r["tick"] - 1:
                    do = (prev.get("intencion") or {}).get("do"); pk = prev.get("pack") or []
                    aqui = [it for it in (prev.get("ve_items") or []) if tuple(it.get("pos") or ()) == tuple(prev["pos"])]; ids = [it["id"] for it in aqui]
                    if do == "pickup" and len(set(ids)) >= 2:
                        up, un = unidades(prev), unidades(r)
                        if not any(un[i] > up[i] for i in un):
                            otras = [i for i in ids[1:] if cabe(pk, i, 1)]
                            if not cabe(pk, ids[0], 1) and otras: nada.append({"vida": os.path.basename(carp) + "/" + os.path.basename(f)[-14:-8], "t": prev["tick"], "ids": ids, "primera_no_cabe": ids[0], "otras_que_cabian": otras})
                    if do == "drop":
                        s_ = prev["intencion"].get("slot"); sid = (pk[s_] or {}).get("id") if (s_ is not None and s_ < len(pk) and pk[s_]) else None
                        aq2 = [it["id"] for it in (r.get("ve_items") or []) if tuple(it.get("pos") or ()) == tuple(r["pos"])]
                        if sid and sid in aq2 and len(aq2) >= 2: soltados.append({"vida": os.path.basename(carp) + "/" + os.path.basename(f)[-14:-8], "t": prev["tick"], "soltado": sid, "lista_despues": aq2, "posicion": "primera" if aq2[0] == sid else "ultima" if aq2[-1] == sid else "otra"})
                prev = r
R2 = {"pickup_sin_ganancia_con_otra_que_cabia": len(nada), "ejemplos": nada[:6], "drops_en_casilla_con_varios": len(soltados), "posicion_de_lo_soltado": dict(collections.Counter(s["posicion"] for s in soltados)), "ejemplos_drop": soltados[:6]}
d = json.load(open(os.path.join(AQUI, "P7_7_coge.json"))); d["segunda_medida"] = R2
json.dump(d, open(os.path.join(AQUI, "P7_7_coge.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R2, ensure_ascii=False, indent=1))

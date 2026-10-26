"""[P7-65] ¿HACIA QUE BOTIQUIN DIO EL PASO AL ACEPTAR? (descriptivo, posterior al sello; pregunta de Manel sobre el GIF de s2 d13). De las evaluaciones de la falsa sin cogida
(las mismas 453 del diagnostico): en el registro de la decision (el tic de la aceptacion + 1: el diario apunta la decision en el tic siguiente), el elegido y si habia algun botiquin a la
vista. ir_objeto va al objeto que la criatura RECUERDA (mem.objetos_vistos), este o no a la vista. Si no hay ninguno a la vista, se busca el ultimo botiquin que vio ella misma y si el paso
la acerca a el; «recordado y desaparecido» = lo vio antes, a <= 4 casillas de donde esta ahora, y ya no lo ve (alguien lo cogio o se uso).  python3 recordados_P7_65.py -> P7_65_recordados.json"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI); sys.argv = sys.argv[:1]
import diagnostico_P7_65 as DG
D = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0), "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
S2 = DG.sin_cogida(); R = collections.Counter(); por_her = collections.defaultdict(collections.Counter); ej = []
for (k, t0, t1, e) in S2:
    f = glob.glob(os.path.join(DG.RUNS, f"P765_s{k[0]}_d{k[1]}_{k[2]}_*", f"*policy_agent_{k[3]}.art.log"))[0]; vistos = {}; dec = None
    for l in open(f, errors="replace"):
        if not l.startswith('{"k":"tick"'): continue
        r = json.loads(l); t = r["tick"]
        if t > t0 + 1: break
        if t == t0 + 1: dec = r; break
        for it in r.get("ve_items") or []:
            if it.get("id") == "first_aid" and it.get("pos"): vistos[tuple(it["pos"])] = t
    if dec is None: continue
    Rg = dec.get("RADIOGRAFIA") or {}; el = Rg.get("elegido"); pos = tuple(dec.get("pos") or (0, 0)); ahora = [tuple(it["pos"]) for it in (dec.get("ve_items") or []) if it.get("id") == "first_aid"]
    her = DG.HER[k[3]]; c = por_her[her]; c["aceptaciones"] += 1; c[f"elegido {el}"] += 1
    if ahora: c["con un botiquin a la vista"] += 1; continue
    c["sin ningun botiquin a la vista"] += 1
    dirp = (Rg.get("accion") or {}).get("dir"); paso = (pos[0] + D[dirp][0], pos[1] + D[dirp][1]) if dirp in D else pos
    hacia = [p for p in vistos if cheb(paso, p) < cheb(pos, p)]
    if hacia:
        c["el paso la acerca a un botiquin que vio antes"] += 1
        if any(cheb(pos, p) <= 4 for p in hacia): c["  ... que estaba a <= 4 casillas y ya no esta (recordado y desaparecido)"] += 1
    elif not vistos: c["no habia visto ningun botiquin ese dia"] += 1
    else: c["el paso no la acerca a ninguno que viera"] += 1
    if len(ej) < 5 and hacia: p = min(hacia, key=lambda q: cheb(pos, q)); ej.append({"vida": f"s{k[0]} d{k[1]} {k[2]} {her}", "tic_decision": t0 + 1, "pos": pos, "elegido": el, "paso": dirp, "botiquin_recordado": p, "visto_por_ultima_vez": vistos[p], "distancia": cheb(pos, p)})
out = {h: dict(c) for h, c in por_her.items()}; out["ejemplos"] = ej; out["evaluaciones"] = len(S2)
json.dump(out, open(os.path.join(AQUI, "P7_65_recordados.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))

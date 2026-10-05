"""[P6-14] El resumen del banco del oraculo: de las 40 salidas por vida a
`P6_14_planes.json` (todos los planes, aplanados) y `P6_14_resumen.json`
(las cuentas de P6-14 §3, con los umbrales cruzados). Instrumento de medida.

Definiciones (declaradas):
  · muerte por anillo = la de P6_11_golpes/P6_13 (`anillo` en la salida);
    EVITABLE = de fase 1-6 (las 3 de la fase final, radio 3 -> 0, no lo son:
    informe_P6_13 §2);
  · clase = la de P6-13 (i salir antes, ii miedo, iii hermano, v otra);
  · VENTANA de una muerte = [aviso de la fase que mata, muerte);
  · plan A TIEMPO = aceptado en una decision de la ventana, con llegada
    (tic + pasos x coste) anterior a la muerte;
  · veredicto con margen m = "vida" si la regla dijo "vida"; si no, acepta
    si ventaja > m (asi lo hace `forma.juzga_margen`); con m = 0,062 debe
    coincidir con lo que dijo la puerta (se comprueba);
  · falsa aceptacion (vidas sin muerte por anillo): plan aceptado cuya foto
    prevista dice que algo empeora: (alfa) en algun punto de control la d del
    plan es peor que la del comparador; (beta) la vida prevista al final es
    menor que la del comparador; (gamma) el destino aleja del hermano
    (Chebyshev al hermano en su diario, ese tic) mas de lo que esta ahora.
"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("P614_SCRATCH") or os.path.join(AQUI, "_P6_14_tmp")
import oraculo_P6_14 as O
MARGEN_PUERTA = None
FASE_FINAL = 7
MARGENES_PUERTA = (None, 0.02, 0.08)     # None = el de la puerta (0,062)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def clase_de(an):
    if not an:
        return None
    return an["clase"].split(" ")[0]


def acepta_con(p, m):
    if p.get("veredicto") in (None, "?", "intraducible") or "acepta" not in p:
        return False
    if p["veredicto"] == "vida" or p["veredicto"].startswith(("revienta", "sin")):
        return False
    return p["ventaja"] > m


vidas = []
for f in sorted(glob.glob(os.path.join(OUT, "P611_*_s*.json"))):
    vidas.append(json.load(open(f)))
assert len(vidas) == 40, len(vidas)
MARGEN_PUERTA = vidas[0]["umbrales"]["margen_puerta"]
planes = []
R = collections.Counter(); inconsist = 0
for v in vidas:
    an = v["anillo"]; cl = clase_de(an)
    evitable = bool(an) and an["fase"] != FASE_FINAL
    ventana = (an["aviso"], an["muerte"]) if an else None
    R["vidas"] += 1; R["vidas anillo"] += bool(an); R["vidas evitables"] += evitable
    R["tics"] += v["tics"]; R["repro igual"] += v["repro"]["igual"]; R["repro difiere"] += v["repro"]["difiere"]
    R["decisiones"] += v["n_decisiones"]; R["planes"] += v["n_planes"]
    for d in v["decisiones"]:
        t = d["tick"]
        en_ventana = bool(ventana) and ventana[0] <= t < ventana[1]
        for p in d["planes"]:
            q = dict(p)
            q.update({"carp": v["carp"], "slot": v["slot"], "tick": t, "pos": d["pos"], "hp": d["hp"], "momentos": d["momentos"], "arde": d["arde"], "holgura": d["holgura"],
                      "fase_activa": d["fase_activa"], "fase_aviso": d["fase_aviso"], "hermano": d["hermano"], "n_seguras": d["info"].get("n_seguras"), "n_rivales": d["info"].get("n_rivales"),
                      "n_cands_cuerpo": len(d["cands_cuerpo"]), "elegido": d["elegido"],
                      "anillo": bool(an), "clase": cl, "evitable": evitable, "en_ventana": en_ventana, "muerte": (an["muerte"] if an else None),
                      "a_tiempo": bool(p.get("acepta")) and en_ventana and p["llegada"] < an["muerte"]})
            if "acepta" in p:
                rec = acepta_con(p, MARGEN_PUERTA)
                if rec != bool(p["acepta"]):
                    inconsist += 1
            planes.append(q)
            q.pop("puntos", None)                      # redundante con curva/curva_comp (d por punto)
            if q.get("contra"):
                q["contra"] = q["contra"][:8]
            for c in (q.get("curva") or []) + (q.get("curva_comp") or []):
                c.pop("pos", None)
R["planes inconsistentes con el margen"] = inconsist
json.dump({"nota": "INSTRUMENTO DE MEDIDA (P6-14): planes del oraculo juzgados por la puerta real del cuerpo congelado, en seco. No es el cuerpo.",
           "planes": planes}, open(os.path.join(AQUI, "P6_14_planes.json"), "w"), ensure_ascii=False)

# ── las cuentas ────────────────────────────────────────────────────────────
def momento_ok(p, margen_disparo):
    """El plan pertenece a una decision valida con este margen de disparo."""
    if 2 in p["momentos"]:
        return True
    return p["arde"] or (p["holgura"] is not None and p["holgura"] <= margen_disparo)


def cuenta(H, m_puerta, margen_disparo, R_cerca, solo_ventana=True):
    """Las cuentas de §3 para una combinacion de umbrales."""
    mp = MARGEN_PUERTA if m_puerta is None else m_puerta
    crit_ok = lambda c: (not c.startswith("b")) or c == f"b{R_cerca}"
    S = collections.Counter(); por_vida = collections.defaultdict(lambda: {"acept": 0, "a_tiempo": 0, "planes": 0, "juzgables": 0})
    crit = collections.Counter(); crit_n = collections.Counter(); mom = collections.Counter(); mom_n = collections.Counter()
    for p in planes:
        if p["H"] != H or not momento_ok(p, margen_disparo):
            continue
        cs = [c for c in p["criterios"] if crit_ok(c)]
        if not cs:
            continue
        k = (p["carp"], p["slot"]); pv = por_vida[k]; pv["planes"] += 1
        pv["anillo"] = p["anillo"]; pv["clase"] = p["clase"]; pv["evitable"] = p["evitable"]
        if p["propia"] or "acepta" not in p:
            S["planes no juzgables (propia casilla)"] += p["propia"]; S["planes intraducibles"] += ("acepta" not in p)
            S["  ...de los de propia casilla, veredicto " + str(p.get("veredicto"))] += p["propia"]
            continue
        pv["juzgables"] += 1
        S["planes juzgables"] += 1
        S["veredicto " + str(p["veredicto"])] += 1
        ac = acepta_con(p, mp)
        for c in cs:
            crit_n[c] += 1; crit[c] += ac
        for mo in p["momentos"]:
            mom_n[mo] += 1; mom[mo] += ac
        if not ac:
            continue
        pv["acept"] += 1
        S["planes aceptados"] += 1
        if p["anillo"]:
            S["aceptados en vidas de anillo"] += 1
            if p["en_ventana"]:
                S["aceptados en la ventana de la muerte"] += 1
            if p["en_ventana"] and p["llegada"] < p["muerte"]:
                pv["a_tiempo"] += 1
        else:
            S["aceptados en vidas sin anillo"] += 1
            cv, cc = p.get("curva") or [], p.get("curva_comp") or []
            alfa = any(a["d"] is not None and b["d"] is not None and a["d"] > b["d"] + 1e-9 for a, b in zip(cv, cc))
            beta = bool(cv and cc and cv[-1]["vida"] is not None and cc[-1]["vida"] is not None and cv[-1]["vida"] < cc[-1]["vida"] - 1e-9)
            gamma = bool(p["hermano"] and cheb(p["destino"], p["hermano"]) > cheb(p["pos"], p["hermano"]))
            S["falsa aceptacion alfa (algun punto peor)"] += alfa; S["falsa aceptacion beta (menos vida al final)"] += beta; S["falsa aceptacion gamma (aleja del hermano)"] += gamma
            S["falsa aceptacion (alguna de las tres)"] += (alfa or beta or gamma)
            por_vida[k]["falsas"] = por_vida[k].get("falsas", 0) + (alfa or beta or gamma)
    # por vida: las 19 evitables
    ev = {k: v for k, v in por_vida.items() if v.get("evitable")}
    S["evitables con planes"] = len(ev)
    S["evitables con >=1 plan aceptado A TIEMPO"] = sum(1 for v in ev.values() if v["a_tiempo"])
    por_clase = collections.Counter(); por_clase_n = collections.Counter()
    for v in ev.values():
        por_clase_n[v["clase"]] += 1; por_clase[v["clase"]] += bool(v["a_tiempo"])
    S["vidas sin anillo con alguna falsa aceptacion"] = sum(1 for v in por_vida.values() if not v.get("anillo") and v.get("falsas"))
    S["vidas sin anillo con algun plan aceptado"] = sum(1 for v in por_vida.values() if not v.get("anillo") and v["acept"])
    return {"H": H, "margen_puerta": mp, "margen_disparo": margen_disparo, "R_cerca": R_cerca, "cuentas": dict(S),
            "evitables_a_tiempo_por_clase": {c: [por_clase[c], por_clase_n[c]] for c in sorted(por_clase_n)},
            "acepta_por_criterio": {c: [crit[c], crit_n[c]] for c in sorted(crit_n)},
            "acepta_por_momento": {str(m): [mom[m], mom_n[m]] for m in sorted(mom_n)}}


principal = cuenta(O.HORIZONTES[0], None, O.MARGENES[0], O.R_CERCAS[0])
variantes = []
for H in O.HORIZONTES:
    for mp in MARGENES_PUERTA:
        for md in O.MARGENES:
            for Rc in O.R_CERCAS:
                if (H, mp, md, Rc) == (O.HORIZONTES[0], None, O.MARGENES[0], O.R_CERCAS[0]):
                    continue
                variantes.append(cuenta(H, mp, md, Rc))

# clase (ii): casillas seguras con pocos rivales, ¿alguna aceptada?
ii = collections.Counter(); ii_lista = []
for p in planes:
    if p["clase"] != "ii" or p["propia"] or "acepta" not in p or not p["en_ventana"] or p["H"] != O.HORIZONTES[0]:
        continue
    r5 = p["rivales_cerca"].get("5")
    ii["planes en ventana"] += 1
    ii[f"rivales cerca (R5) = {r5}"] += 1
    if p["acepta"]:
        ii["aceptados"] += 1; ii[f"aceptados con rivales cerca (R5) = {r5}"] += 1
        ii_lista.append({"carp": p["carp"], "slot": p["slot"], "tick": p["tick"], "destino": p["destino"], "criterios": p["criterios"], "ventaja": p["ventaja"], "rivales_cerca": p["rivales_cerca"], "a_tiempo": p["a_tiempo"]})
    else:
        ii[f"rechazados ({p['veredicto']}) con rivales cerca (R5) = {r5}"] += 1

# filas en contra, agregadas (planes juzgables, H principal, rechazados por area)
contra = collections.defaultdict(list); favor = collections.defaultdict(list)
for p in planes:
    if p["propia"] or "acepta" not in p or p["H"] != O.HORIZONTES[0] or not p.get("contra"):
        continue
    for k, dk, Mp, Mc in p["contra"]:
        (contra if dk > 0 else favor)[k].append(dk)
filas_contra = {k: {"n_planes": len(v), "peso_medio": round(sum(v) / len(v), 5), "peso_total": round(sum(v), 4)} for k, v in sorted(contra.items(), key=lambda kv: -sum(kv[1]))}
filas_favor = {k: {"n_planes": len(v), "peso_medio": round(sum(v) / len(v), 5), "peso_total": round(sum(v), 4)} for k, v in sorted(favor.items(), key=lambda kv: sum(kv[1]))}

# mejores planes por vida de anillo (para el GIF y la tabla)
mejor = {}
for p in planes:
    if not p["anillo"] or p["propia"] or "acepta" not in p or not p["en_ventana"] or p["H"] != O.HORIZONTES[0]:
        continue
    k = f"{p['carp']} s{p['slot']}"
    m = mejor.get(k)
    if m is None or (p["a_tiempo"], p["ventaja"]) > (m["a_tiempo"], m["ventaja"]):
        mejor[k] = {"tick": p["tick"], "destino": p["destino"], "criterios": p["criterios"], "veredicto": p["veredicto"], "ventaja": p["ventaja"], "a_tiempo": p["a_tiempo"], "clase": p["clase"], "muerte": p["muerte"], "contra": (p.get("contra") or [])[:4], "comparador": p.get("comparador"), "hp": p["hp"], "pos": p["pos"]}

ms = sorted(p["ms"] for p in planes if p.get("ms") is not None)
res = {"nota": "INSTRUMENTO DE MEDIDA (P6-14). El oraculo no es el cuerpo.",
       "totales": dict(R), "ms_puerta": {"n": len(ms), "mediana": ms[len(ms) // 2] if ms else None, "p95": ms[int(len(ms) * 0.95)] if ms else None},
       "umbrales": {"H": list(O.HORIZONTES), "margen_puerta": [MARGEN_PUERTA] + [x for x in MARGENES_PUERTA if x], "margen_disparo": list(O.MARGENES), "R_cerca": list(O.R_CERCAS)},
       "principal": principal, "variantes": variantes, "clase_ii": {"cuentas": dict(ii), "aceptados": ii_lista},
       "filas_en_contra": filas_contra, "filas_a_favor": filas_favor, "mejor_por_vida_anillo": mejor}
json.dump(res, open(os.path.join(AQUI, "P6_14_resumen.json"), "w"), ensure_ascii=False, indent=1)

print(json.dumps(res["totales"], ensure_ascii=False))
print("ms puerta", res["ms_puerta"])
print("\n=== PRINCIPAL", {k: principal[k] for k in ("H", "margen_puerta", "margen_disparo", "R_cerca")})
for k, v in sorted(principal["cuentas"].items()):
    print(f"   {k:60s} {v}")
print("   evitables a tiempo por clase", principal["evitables_a_tiempo_por_clase"])
print("   acepta por criterio", principal["acepta_por_criterio"])
print("   acepta por momento", principal["acepta_por_momento"])
print("\n=== VARIANTES (H, m_puerta, m_disparo, R) -> aceptados / evitables a tiempo / por clase / falsas")
for v in variantes:
    c = v["cuentas"]
    print(f"   H{v['H']:4d} mp{v['margen_puerta']:.3f} md{v['margen_disparo']:4d} R{v['R_cerca']} -> acept {c.get('planes aceptados', 0):5d} / juzg {c.get('planes juzgables', 0):6d} · evitables a tiempo {c.get('evitables con >=1 plan aceptado A TIEMPO', 0):2d} {v['evitables_a_tiempo_por_clase']} · falsas {c.get('falsa aceptacion (alguna de las tres)', 0)} de {c.get('aceptados en vidas sin anillo', 0)}")
print("\n=== CLASE ii"); [print(f"   {k:60s} {v}") for k, v in sorted(ii.items())]
print("\n=== FILAS EN CONTRA"); [print(f"   {k:22s} {v}") for k, v in list(filas_contra.items())[:10]]
print("=== FILAS A FAVOR"); [print(f"   {k:22s} {v}") for k, v in list(filas_favor.items())[:10]]
print("\n=== MEJOR PLAN POR VIDA DE ANILLO (ventana, H principal)")
for k, m in sorted(mejor.items(), key=lambda kv: (kv[1]["clase"], kv[0])):
    print(f"   {k:32s} {m['clase']:3s} t{m['tick']} muere {m['muerte']} hp {m['hp']} {m['pos']}->{m['destino']} {m['criterios']} {m['veredicto']} ventaja {m['ventaja']:+.4f} a_tiempo {m['a_tiempo']} comp {m['comparador']} contra {m['contra'][:3]}")

"""[P6-15] El resumen del banco de la puerta honesta consigo misma. Instrumento de
medida. De las 40 salidas por vida a `P6_15_planes.json` y `P6_15_resumen.json`.

Definiciones (las de P6-14, declaradas alli, mas estas):
  · EXCESO DE CONFIANZA (§1): en un rechazo por area de la ventana, el
    comparador «se creia que salia» si su casilla proyectada en el punto de
    control esta a salvo (dentro del radio de ese tic y del r1 de la fase); «no
    salio» si la casilla REAL del diario en ese tic arde, o el cuerpo ya ha
    muerto. Se cuenta en el ULTIMO punto de control (elegido) y en el primero.
  · TECHO (§2) y VERSION USABLE (§3): el mismo plan, misma regla y margen,
    contra la trayectoria real imaginada / contra el cuerpo imaginado paso a
    paso; se cuenta igual que en P6-14 (a tiempo, por clase, falsas, (c)).
  · HORIZONTE (§4): plan de clase (i) en ventana, rechazado por la puerta, cuyo
    fuego (primer tic en que arde mi casilla) cae despues del ultimo punto de
    control del plan.
"""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("P615_SCRATCH") or os.path.join(AQUI, "_P6_15_tmp")
import oraculo_P6_14 as O
FASE_FINAL = 7
MARGENES_PUERTA = (None, 0.02, 0.08)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def clase_de(an):
    return an["clase"].split(" ")[0] if an else None


def acepta_con(ver, ventaja, m):
    if ver in (None, "?", "intraducible", "vida") or str(ver).startswith(("revienta", "sin")):
        return False
    return ventaja > m


vidas = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(OUT, "P611_*_s*.json")))]
assert len(vidas) == 40, len(vidas)
MP = vidas[0]["umbrales"]["margen_puerta"]; CADAS = [str(c) for c in vidas[0]["umbrales"]["rollout_cadas"]]
planes = []; R = collections.Counter(); DEC = []
for v in vidas:
    an = v["anillo"]; cl = clase_de(an); evitable = bool(an) and an["fase"] != FASE_FINAL
    ventana = (an["aviso"], an["muerte"]) if an else None
    R["vidas"] += 1; R["vidas anillo"] += bool(an); R["vidas evitables"] += evitable
    R["tics"] += v["tics"]; R["repro igual"] += v["repro"]["igual"]; R["repro difiere"] += v["repro"]["difiere"]
    R["decisiones"] += v["n_decisiones"]; R["planes"] += v["n_planes"]
    for d in v["decisiones"]:
        t = d["tick"]; en_v = bool(ventana) and ventana[0] <= t < ventana[1]
        DEC.append({"carp": v["carp"], "slot": v["slot"], "tick": t, "anillo": bool(an), "clase": cl, "en_ventana": en_v, "momentos": d["momentos"], "arde": d["arde"], "holgura": d["holgura"],
                    "rollouts": {c: {"ms": r["ms"], "decisiones": r["decisiones"], "tics": r["tics"], **r["fidelidad"]} for c, r in d["rollouts"].items()}})
        for p in d["planes"]:
            q = {k: p[k] for k in p if k not in ("curva", "curva_comp", "real", "rollout", "exceso", "contra", "s8")}
            q.update({"carp": v["carp"], "slot": v["slot"], "tick": t, "pos": d["pos"], "hp": d["hp"], "momentos": d["momentos"], "arde": d["arde"], "holgura": d["holgura"], "hermano": d["hermano"],
                      "anillo": bool(an), "clase": cl, "evitable": evitable, "en_ventana": en_v, "muerte": (an["muerte"] if an else None)})
            if "acepta" in p:
                q["curva"] = [{"tic": c["tic"], "d": c["d"], "vida": c["vida"]} for c in p["curva"]]
                q["curva_comp"] = [{"tic": c["tic"], "d": c["d"], "vida": c["vida"], "pos": c["pos"]} for c in p["curva_comp"]]
                q["real"] = {"veredicto": p["real"]["veredicto"], "ventaja": p["real"].get("ventaja", 0.0), "curva": [{"tic": c["tic"], "d": c["d"], "vida": c["vida"], "pos": c["pos"]} for c in p["real"].get("curva", [])]}
                q["rollout"] = {c: {"veredicto": r["veredicto"], "ventaja": r.get("ventaja", 0.0), "curva": [{"tic": x["tic"], "d": x["d"], "vida": x["vida"], "pos": x["pos"]} for x in r.get("curva", [])]} for c, r in p["rollout"].items()}
                q["exceso"] = p.get("exceso"); q["s8"] = p.get("s8"); q["contra"] = (p.get("contra") or [])[:6]
            planes.append(q)
# el JSON del repo, aligerado: las curvas del rollout solo para el `cada` elegido; `contra` ya esta en P6_14_planes.json
def _ligero(q):
    q = dict(q); q.pop("contra", None)
    if "rollout" in q:
        q["rollout"] = {c: (r if c == CADAS[0] else {"veredicto": r["veredicto"], "ventaja": r["ventaja"]}) for c, r in q["rollout"].items()}
    return q
json.dump({"nota": "INSTRUMENTO DE MEDIDA (P6-15): planes del oraculo juzgados por la puerta real y por los comparadores de puerta6 (version nueva, declarada). No es el cuerpo.", "planes": [_ligero(q) for q in planes]},
          open(os.path.join(AQUI, "P6_15_planes.json"), "w"), ensure_ascii=False)


def principal_ok(p, H=None, md=None, Rc=None):
    H = O.HORIZONTES[0] if H is None else H; md = O.MARGENES[0] if md is None else md; Rc = O.R_CERCAS[0] if Rc is None else Rc
    if p["H"] != H or "acepta" not in p or p["propia"]:
        return False
    if not (2 in p["momentos"] or p["arde"] or (p["holgura"] is not None and p["holgura"] <= md)):
        return False
    return any((not c.startswith("b")) or c == f"b{Rc}" for c in p["criterios"])


def veredicto_de(p, quien, cada):
    if quien == "puerta":
        return p["veredicto"], p["ventaja"]
    if quien == "real":
        return p["real"]["veredicto"], p["real"]["ventaja"]
    r = p["rollout"][cada]
    return r["veredicto"], r["ventaja"]


def cuenta(quien, cada, H=None, mp=None, md=None, Rc=None):
    m = MP if mp is None else mp
    S = collections.Counter(); pv = collections.defaultdict(lambda: {"acept": 0, "a_tiempo": 0, "n": 0})
    crit = collections.Counter(); crit_n = collections.Counter(); mom = collections.Counter(); mom_n = collections.Counter()
    c_ok = collections.defaultdict(set); c_j = collections.defaultdict(set)
    for p in planes:
        if not principal_ok(p, H, md, Rc):
            continue
        ver, vent = veredicto_de(p, quien, cada)
        k = (p["carp"], p["slot"]); x = pv[k]; x["n"] += 1; x.update(anillo=p["anillo"], clase=p["clase"], evitable=p["evitable"])
        S["juzgables"] += 1; S["veredicto " + str(ver)] += 1
        ac = acepta_con(ver, vent, m)
        cs = [c for c in p["criterios"] if (not c.startswith("b")) or c == f"b{O.R_CERCAS[0] if Rc is None else Rc}"]
        for c in cs:
            crit_n[c] += 1; crit[c] += ac
        for mo in p["momentos"]:
            mom_n[mo] += 1; mom[mo] += ac
        if "c" in cs:
            key = (p["carp"], p["tick"], tuple(p["destino"])); c_j[key].add(p["slot"])
            if ac:
                c_ok[key].add(p["slot"])
        if not ac:
            continue
        x["acept"] += 1; S["aceptados"] += 1
        if p["anillo"]:
            S["aceptados en vidas de anillo"] += 1
            if p["en_ventana"] and p["llegada"] < p["muerte"]:
                x["a_tiempo"] += 1
        else:
            S["aceptados en vidas sin anillo"] += 1
            cv = p["curva"]
            if quien == "puerta":
                cc = p["curva_comp"]
            elif quien == "real":
                cc = p["real"]["curva"]
            else:
                cc = p["rollout"][cada]["curva"]
            alfa = any(a["d"] is not None and b["d"] is not None and a["d"] > b["d"] + 1e-9 for a, b in zip(cv, cc))
            beta = bool(cv and cc and cv[-1]["vida"] is not None and cc[-1]["vida"] is not None and cv[-1]["vida"] < cc[-1]["vida"] - 1e-9)
            gamma = bool(p["hermano"] and cheb(p["destino"], p["hermano"]) > cheb(p["pos"], p["hermano"]))
            S["falsas alfa"] += alfa; S["falsas beta"] += beta; S["falsas gamma"] += gamma; S["falsas (alguna)"] += (alfa or beta or gamma)
            x["falsas"] = x.get("falsas", 0) + (alfa or beta or gamma)
    ev = {k: v for k, v in pv.items() if v.get("evitable")}
    por_clase = collections.Counter(); por_clase_n = collections.Counter()
    for v in ev.values():
        por_clase_n[v["clase"]] += 1; por_clase[v["clase"]] += bool(v["a_tiempo"])
    return {"quien": quien, "cada": cada, "H": O.HORIZONTES[0] if H is None else H, "margen_puerta": m, "margen_disparo": O.MARGENES[0] if md is None else md, "R_cerca": O.R_CERCAS[0] if Rc is None else Rc,
            "cuentas": dict(S), "evitables_con_plan": len(ev), "evitables_a_tiempo": sum(1 for v in ev.values() if v["a_tiempo"]),
            "evitables_a_tiempo_por_clase": {c: [por_clase[c], por_clase_n[c]] for c in sorted(por_clase_n)},
            "vidas_sin_anillo_con_aceptado": sum(1 for v in pv.values() if not v.get("anillo") and v["acept"]),
            "vidas_sin_anillo_con_falsa": sum(1 for v in pv.values() if not v.get("anillo") and v.get("falsas")),
            "acepta_por_criterio": {c: [crit[c], crit_n[c]] for c in sorted(crit_n)}, "acepta_por_momento": {str(k): [mom[k], mom_n[k]] for k in sorted(mom_n)},
            "c_aceptados": sum(len(s) for s in c_ok.values()), "c_juzgado_por_los_dos": sum(1 for s in c_j.values() if len(s) == 2), "c_aceptado_por_los_dos": sum(1 for s in c_ok.values() if len(s) == 2),
            "vidas": {f"{k[0]} s{k[1]}": v for k, v in ev.items()}}


COMPARADORES = [("puerta", None), ("real", None)] + [("rollout", c) for c in CADAS]
principal = {f"{q}{'_' + c if c else ''}": cuenta(q, c) for q, c in COMPARADORES}
variantes = []
for q, c in COMPARADORES:
    if q == "rollout" and c != CADAS[0]:
        continue
    for H in O.HORIZONTES:
        for mp in MARGENES_PUERTA:
            for md in O.MARGENES:
                for Rc in O.R_CERCAS:
                    if (H, mp, md, Rc) == (O.HORIZONTES[0], None, O.MARGENES[0], O.R_CERCAS[0]):
                        continue
                    x = cuenta(q, c, H, mp, md, Rc); x.pop("vidas", None); variantes.append(x)

# ── §1 EL EXCESO DE CONFIANZA (rechazos por area de la ventana, H principal, disparo principal, todos los destinos) ──
EX = collections.Counter(); S8 = collections.defaultdict(list)
for p in planes:
    if "acepta" not in p or p["propia"] or p["H"] != O.HORIZONTES[0] or not p["en_ventana"]:
        continue
    if not (2 in p["momentos"] or p["arde"] or (p["holgura"] is not None and p["holgura"] <= O.MARGENES[0])):
        continue
    if p["veredicto"] != "area" or not p.get("exceso"):
        continue
    EX["rechazos por area en ventana"] += 1
    ex = p["exceso"]; u = ex[-1]; f = ex[0]
    for nombre, e in (("ultimo", u), ("primero", f)):
        if e["salvo_comp"]:
            EX[f"{nombre}: el comparador se creia a salvo"] += 1
            if e["arde_real"] or e["muerto_real"]:
                EX[f"{nombre}: se creia a salvo y NO salio (real arde o muerto)"] += 1
                EX[f"{nombre}:   ...muerto ya"] += e["muerto_real"]
            else:
                EX[f"{nombre}: se creia a salvo y salio"] += 1
        else:
            EX[f"{nombre}: el comparador no se creia a salvo"] += 1
            EX[f"{nombre}: no se creia a salvo y real {'arde' if (e['arde_real'] or e['muerto_real']) else 'a salvo'}"] += 1
        if e["vida_comp"] is not None and e["hp_real"] is not None:
            S8[f"vida_comp_menos_real_{nombre}"].append(e["vida_comp"] - float(e["hp_real"]))
    s = p.get("s8") or {}
    if s.get("real_comp") is not None and s.get("real_noop") is not None and s.get("proj_comp") is not None and s.get("proj_noop") is not None:
        S8["real: S8(comp) - S8(noop)"].append(s["real_comp"] - s["real_noop"])
        S8["proj sin piso: S8(comp) - S8(noop)"].append(s["proj_comp"] - s["proj_noop"])
        S8["proj con piso: S8(comp) - S8(noop)"].append(s["proj_comp_piso"] - s["proj_noop_piso"])
        S8["proj con piso: S8(comp) - S8(plan)"].append(s["proj_comp_piso"] - max(s["proj_plan"] or 0.0, s["proj_noop_piso"] or 0.0))
        S8["real: S8(elegido) - S8(noop)"].append((s.get("real_elegido") or 0.0) - s["real_noop"])
        S8["proj: S8(plan) - S8(noop)"].append((s.get("proj_plan") or 0.0) - s["proj_noop"])
        EX["planes con S-8 real y proyectada"] += 1
def stats(xs):
    xs = sorted(xs)
    return {"n": len(xs), "media": round(sum(xs) / len(xs), 4), "mediana": round(xs[len(xs) // 2], 4), "p10": round(xs[len(xs) // 10], 4), "p90": round(xs[int(len(xs) * 0.9)], 4)} if xs else None
exceso = {"cuentas": dict(EX), "s8": {k: stats(v) for k, v in S8.items()}}

# ── §3 factibilidad y fidelidad del rollout ──
FID = {}
for c in CADAS:
    ms = sorted(d["rollouts"][c]["ms"] for d in DEC); nd = [d["rollouts"][c]["decisiones"] for d in DEC]; tt = [d["rollouts"][c]["tics"] for d in DEC]
    f = {"n": len(ms), "ms_mediana": ms[len(ms) // 2], "ms_p95": ms[int(len(ms) * 0.95)], "ms_max": ms[-1], "decisiones_media": round(sum(nd) / len(nd), 1), "tics_media": round(sum(tt) / len(tt), 1),
         "ms_por_decision_del_rollout": round(sum(ms) / max(1, sum(nd)), 3)}
    for k in (50, 100, 200):
        ds = [d["rollouts"][c][f"dist_{k}"] for d in DEC if f"dist_{k}" in d["rollouts"][c]]
        f[f"dist_{k}"] = stats(ds)
        ac = [(d["rollouts"][c][f"arde_pred_{k}"], d["rollouts"][c][f"arde_real_{k}"]) for d in DEC if f"arde_pred_{k}" in d["rollouts"][c]]
        f[f"arde_{k}_acierta"] = [sum(1 for a, b in ac if a == b), len(ac)]
        f[f"arde_{k}_pred_si_real_no"] = sum(1 for a, b in ac if a and not b); f[f"arde_{k}_pred_no_real_si"] = sum(1 for a, b in ac if (not a) and b)
    tp = [d["rollouts"][c]["tics_arde_pred"] for d in DEC]; tr = [d["rollouts"][c]["tics_arde_real"] for d in DEC]
    f["tics_arde_pred_media"] = round(sum(tp) / len(tp), 1); f["tics_arde_real_media"] = round(sum(tr) / len(tr), 1)
    f["tics_arde_pred_menos_real"] = stats([a - b for a, b in zip(tp, tr)])
    vp = [d["rollouts"][c]["vueltas_pred"] for d in DEC]; vr = [d["rollouts"][c]["vueltas_real"] for d in DEC]
    f["vueltas_pred_total"] = sum(vp); f["vueltas_real_total"] = sum(vr); f["decisiones_con_vuelta_real"] = sum(1 for x in vr if x); f["decisiones_con_vuelta_pred"] = sum(1 for x in vp if x)
    f["vuelta_real_y_pred"] = sum(1 for a, b in zip(vp, vr) if a and b); f["vuelta_real_sin_pred"] = sum(1 for a, b in zip(vp, vr) if b and not a); f["vuelta_pred_sin_real"] = sum(1 for a, b in zip(vp, vr) if a and not b)
    # en ventana de muerte
    dv = [d for d in DEC if d["en_ventana"]]
    f["ventana: decisiones"] = len(dv)
    f["ventana: arde_200 acierta"] = [sum(1 for d in dv if f"arde_pred_200" in d["rollouts"][c] and d["rollouts"][c]["arde_pred_200"] == d["rollouts"][c]["arde_real_200"]), sum(1 for d in dv if f"arde_pred_200" in d["rollouts"][c])]
    f["ventana: tics arde pred/real media"] = [round(sum(d["rollouts"][c]["tics_arde_pred"] for d in dv) / max(1, len(dv)), 1), round(sum(d["rollouts"][c]["tics_arde_real"] for d in dv) / max(1, len(dv)), 1)]
    FID[c] = f

# ── §4 el horizonte ──
HOR = {}
for H in O.HORIZONTES:
    n = collections.Counter()
    for p in planes:
        if "acepta" not in p or p["propia"] or p["H"] != H or p["clase"] != "i" or not p["en_ventana"]:
            continue
        if not (2 in p["momentos"] or p["arde"] or (p["holgura"] is not None and p["holgura"] <= O.MARGENES[0])):
            continue
        n["planes clase i en ventana"] += 1
        if not p["acepta"]:
            n["rechazados"] += 1; n["rechazados con el fuego fuera de la ventana"] += bool(p["fuego_fuera"])
            n[f"rechazados ({p['veredicto']}) con el fuego fuera"] += bool(p["fuego_fuera"])
    HOR[str(H)] = dict(n)

ms_p = sorted(p["ms"] for p in planes if p.get("ms") is not None)
res = {"nota": "INSTRUMENTO DE MEDIDA (P6-15). puerta6 = version nueva de la puerta, declarada; la del cinco no se toca.",
       "totales": dict(R), "ms_puerta": {"n": len(ms_p), "mediana": ms_p[len(ms_p) // 2], "p95": ms_p[int(len(ms_p) * 0.95)]},
       "umbrales": {"H": list(O.HORIZONTES), "margen_puerta": [MP] + [x for x in MARGENES_PUERTA if x], "margen_disparo": list(O.MARGENES), "R_cerca": list(O.R_CERCAS), "rollout_cada": CADAS},
       "exceso_de_confianza": exceso, "principal": principal, "variantes": variantes, "rollout_factibilidad_fidelidad": FID, "horizonte_clase_i": HOR}
json.dump(res, open(os.path.join(AQUI, "P6_15_resumen.json"), "w"), ensure_ascii=False, indent=1)

print(json.dumps(res["totales"], ensure_ascii=False)); print("ms puerta", res["ms_puerta"])
print("\n=== §1 EXCESO DE CONFIANZA"); [print(f"   {k:70s} {v}") for k, v in sorted(exceso["cuentas"].items())]
[print(f"   {k:45s} {v}") for k, v in exceso["s8"].items()]
print("\n=== §2/§3 PRINCIPAL por comparador")
for k, x in principal.items():
    c = x["cuentas"]
    print(f"   {k:12s} juzg {c.get('juzgables', 0):5d} · ok {c.get('veredicto ok', 0):5d} area {c.get('veredicto area', 0):5d} vida {c.get('veredicto vida', 0):4d} · acept {c.get('aceptados', 0):5d} · evitables a tiempo {x['evitables_a_tiempo']:2d}/{x['evitables_con_plan']} {x['evitables_a_tiempo_por_clase']} · sin anillo acept {c.get('aceptados en vidas sin anillo', 0)} en {x['vidas_sin_anillo_con_aceptado']} vidas, falsas {c.get('falsas (alguna)', 0)} (a{c.get('falsas alfa', 0)} b{c.get('falsas beta', 0)} g{c.get('falsas gamma', 0)}) en {x['vidas_sin_anillo_con_falsa']} · (c) acept {x['c_aceptados']}, juzgado por los dos {x['c_juzgado_por_los_dos']}, aceptado por los dos {x['c_aceptado_por_los_dos']} · crit {x['acepta_por_criterio']} mom {x['acepta_por_momento']}")
    for kv, vv in sorted(x["vidas"].items(), key=lambda kv: (kv[1]["clase"], kv[0])):
        if vv["a_tiempo"]:
            print(f"        {kv} {vv['clase']} a tiempo {vv['a_tiempo']} de {vv['n']}")
print("\n=== VARIANTES (comparador, H, mp, md, R) -> acept / evitables a tiempo por clase / falsas")
for x in variantes:
    c = x["cuentas"]
    print(f"   {x['quien']:8s}{x['cada'] or '':3s} H{x['H']:4d} mp{x['margen_puerta']:.3f} md{x['margen_disparo']:4d} R{x['R_cerca']} -> acept {c.get('aceptados', 0):5d}/{c.get('juzgables', 0):5d} · evitables {x['evitables_a_tiempo']:2d} {x['evitables_a_tiempo_por_clase']} · falsas {c.get('falsas (alguna)', 0)} de {c.get('aceptados en vidas sin anillo', 0)}")
print("\n=== §3 ROLLOUT: factibilidad y fidelidad")
for c, f in FID.items():
    print(f"   cada {c}: ", json.dumps(f, ensure_ascii=False))
print("\n=== §4 HORIZONTE clase (i)"); [print(f"   H{H}: {v}") for H, v in HOR.items()]

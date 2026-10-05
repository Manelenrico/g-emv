"""[P6-24 · 3-4] LAS MEDIDAS DE LA REPLICA, con UNA medida principal: TICS ARDIENDO EN LAS FASES 5-7
(desde el aviso de la fase 5 hasta el final de la vida o de la partida; arde = distancia al centro >
`zona.radius` del tic), por vida viva en el aviso de la fase 5, media por semilla, EMPAREJADA por
semilla (A7h - A4; solo semillas con alguna vida viva en el aviso 5 en los dos brazos). Prueba:
permutacion exacta por cambio de signo (2^n) UNILATERAL (H1: A7h arde menos), y bilateral; intervalo
del 95 % de la media de la diferencia por bootstrap (10.000 remuestreos, semilla 0). Todo lo demas es
SECUNDARIO y se declara: tics ardiendo y % dentro en la fase 5 (definiciones de P6-23, para
comparar), planes de la fase 5 aceptados / sostenidos, pasos perdidos (P6-21), muertes por anillo y
por rival, supervivientes; emparejado con la misma prueba, bilateral.
Las funciones `carga`, `causa` y `perdidos` son copia literal de `mide_campo_P6_23.py`. SOLO LECTURA,
diarios de uno en uno. Cada brazo admite varios patrones separados por `;` (para las 40 semillas juntas).

    python3 mide_campo_P6_24.py SALIDA.json 'A4=paintball/runs/P624_t1_A4_*' 'A7h=paintball/runs/P624_t2_A7h_*'
    python3 mide_campo_P6_24.py P6_24_campo_40.json --une P6_24_campo_P623.json P6_24_campo.json     (las 40 semillas juntas)
Con mas de 22 pares la permutacion exacta (2^n) no cabe en memoria: se usa Monte Carlo (1.000.000 cambios de signo, semilla 0), declarado en el JSON.
"""
import collections, glob, json, math, os, re, statistics as st, sys
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
C = (24, 24); FASE = 4
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo"); sm = next(r for r in recs if r["k"] == "static_map")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); fin = next((r for r in recs if r.get("k") == "final"), None)
    T = {}; L = collections.defaultdict(list)
    for r in recs:
        k = r.get("k")
        if k in ("forma_aceptada", "compromiso6", "forma_caida", "forma_evaluada", "oraculo16", "resumen16", "resumen18", "resumen23", "hilo_forma"):
            L[k].append(r)
        if k != "tick" or r.get("phase") != "live":
            continue
        T[r["tick"]] = {"pos": (int(r["pos"][0]), int(r["pos"][1])), "zone_hit": any(g.get("source") == "zone" for g in (r.get("damage_taken") or []) if isinstance(g, dict)), "radio": float((r.get("zona") or {}).get("radius") or 48),
                        "dt": [g for g in (r.get("damage_taken") or []) if isinstance(g, dict)], "int": r.get("intencion") or {}, "mri": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0),
                        "ar": r.get("action_result_obs", r.get("action_result")), "ve": {tuple(a["pos"]) for a in (r.get("ve_agentes") or []) if a.get("pos")}}
    del recs
    return pc, T, fin, L, mundo, [tuple(z) for z in pc.get("zone_schedule") or []]


def causa(T, fin):
    if not (fin and fin.get("reason") == "eliminated"):
        return None
    tl = sorted(T); mt = int(fin.get("match_ticks") or tl[-1])
    golpes = [t for t in tl if mt - 48 <= t <= mt and any(str(g.get("source")).startswith("P") for g in T[t]["dt"])]
    zt = [t for t in tl if mt - 48 <= t <= mt and T[t]["zone_hit"]]
    if golpes and (not zt or golpes[-1] >= max(zt)):
        return "rival"
    return "anillo" if zt else "no consta"


def perdidos(T, mundo, desde=None):
    lib = per = 0
    for t in sorted(T):
        prev = T.get(t - 1); r = T[t]
        if prev is None or (desde is not None and t - 1 < desde):
            continue
        inte = prev["int"]
        if inte.get("do") == "move" and inte.get("dir") in DIRS and prev["mri"] == 0:
            dx, dy = DIRS[inte["dir"]]; dest = (prev["pos"][0] + dx, prev["pos"][1] + dy)
            if not mundo.solido(dest[0], dest[1]) and dest not in prev["ve"]:
                lib += 1
                if r["ar"] == "ok" and r["pos"] == prev["pos"] and r["mri"] == 0:
                    per += 1
    return lib, per



N_EXACTA = 22        # hasta 22 pares, exacta (2^n); con mas, Monte Carlo de 1.000.000 cambios de signo (semilla 0), declarado


def permutacion(d, unilateral=False):
    n = len(d); obs = sum(d) / n
    if all(x == 0 for x in d):
        return 1.0
    dd = np.array(d, dtype=float)
    if n <= N_EXACTA:
        idx = np.arange(2 ** n, dtype=np.int64)
        signs = (((idx[:, None] >> np.arange(n)) & 1) * 2 - 1).astype(np.int8); m = signs @ dd / n
    else:
        rng = np.random.default_rng(0); m = np.concatenate([(rng.integers(0, 2, size=(100000, n)) * 2 - 1) @ dd / n for _ in range(10)])
    if unilateral:      # H1: la diferencia es negativa (A7h arde menos)
        return float(np.mean(m <= obs + 1e-12))
    return float(np.mean(np.abs(m) >= abs(obs) - 1e-12))


def bootstrap(d, B=10000):
    rng = np.random.default_rng(0); dd = np.array(d, dtype=float)
    m = np.array([rng.choice(dd, size=len(dd), replace=True).mean() for _ in range(B)])
    return [round(float(np.percentile(m, 2.5)), 2), round(float(np.percentile(m, 97.5)), 2)]


def empareja(A, B, campo, unilateral=False):
    d = []
    for s in sorted(set(A) & set(B)):
        x, y = A[s].get(campo), B[s].get(campo)
        if x is None or y is None:
            continue
        d.append(x - y)
    if not d:
        return None
    r = {"n": len(d), "prueba": ("exacta 2^n" if len(d) <= N_EXACTA else "Monte Carlo 1.000.000 (semilla 0)"), "media_dif": round(st.mean(d), 2), "mediana_dif": round(st.median(d), 2), "gana": sum(1 for x in d if x > 0), "pierde": sum(1 for x in d if x < 0),
         "p_bilateral": round(permutacion(d), 4), "ic95_bootstrap": bootstrap(d), "diferencias": [round(x, 2) for x in d]}
    if unilateral:
        r["p_unilateral (A7h arde menos)"] = round(permutacion(d, True), 4)
    return r


salida = sys.argv[1]; OUT = {"nota": __doc__.split("\n")[0], "brazos": {}}
if "--une" in sys.argv:       # las 40 semillas juntas: une los brazos de dos JSON ya medidos con este mismo guion (mismas vidas, mismas medidas)
    for f in sys.argv[sys.argv.index("--une") + 1:]:
        for etiq, b in json.load(open(os.path.join(AQUI, f)))["brazos"].items():
            o = OUT["brazos"].setdefault(etiq, {"vidas": [], "por_semilla": {}, "de": []})
            assert not (set(o["por_semilla"]) & set(b["por_semilla"])), "semilla repetida"
            o["vidas"] += b["vidas"]; o["por_semilla"].update(b["por_semilla"]); o["de"].append(f)
    for etiq, o in OUT["brazos"].items():
        V = o["vidas"]; W = [v for v in V if v.get("viva_en_warn5")]
        o["resumen"] = {"partidas": len(o["por_semilla"]), "vidas": len(V), "vivas_en_warn5": len(W), "ardiendo_5_7_media": round(st.mean(v["ardiendo_5_7"] for v in W), 1), "ardiendo_5_7_mediana": st.median(v["ardiendo_5_7"] for v in W),
                        "ardiendo_f5_media": round(st.mean(v["ardiendo_f5"] for v in W), 1), "dentro_pct_f5_media": round(st.mean(v["dentro_pct_f5"] for v in W), 1),
                        "planes_aceptados_f5": sum(v.get("planes_f5", {}).get("aceptados", 0) for v in W), "planes_sostenidos_f5": sum(v.get("planes_f5", {}).get("sostenidos_fin_fase", 0) for v in W),
                        "pasos_libres_5_7": sum(v["pasos_libres_5_7"] for v in V), "pasos_perdidos_5_7": sum(v["pasos_perdidos_5_7"] for v in V),
                        "muertes_anillo": sum(1 for v in V if v["causa"] == "anillo"), "muertes_rival": sum(1 for v in V if v["causa"] == "rival"), "supervivientes": sum(v["superviviente"] for v in V)}
        print(f"### {etiq} (unido de {o['de']}): {json.dumps(o['resumen'], ensure_ascii=False)}")
for etiq, pats in ([] if "--une" in sys.argv else [x.split("=", 1) for x in sys.argv[2:]]):
    V = []; PS = {}
    carps = sorted(c for pat in pats.split(";") for c in glob.glob(os.path.join(RAIZ, pat)))
    for carp in carps:
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1]); sr = {"semilla": sem, "carpeta": os.path.basename(carp), "vivas_en_warn": 0, "ardiendo_5_7": [], "ardiendo_f5": [], "dentro_pct_f5": [], "sostenidos": 0, "aceptados_fase": 0, "supervivientes": 0, "anillo": 0, "rival": 0, "perdidos_5_7": 0, "libres_5_7": 0}
        for sl in (10, 11):
            pc, T, fin, L, mundo, fases = carga(fs[sl])
            warn, shrink, done, r0, r1, dps = fases[FASE]; sig = fases[FASE + 1][0]
            mt = max(T); c = causa(T, fin); lib5, per5 = perdidos(T, mundo, desde=warn)
            v = {"semilla": sem, "slot": sl, "tics": mt, "superviviente": bool(fin and fin.get("reason") != "eliminated"), "causa": c, "viva_en_warn5": warn in T, "pasos_libres_5_7": lib5, "pasos_perdidos_5_7": per5}
            sr["supervivientes"] += v["superviviente"]; sr["anillo"] += (c == "anillo"); sr["rival"] += (c == "rival"); sr["perdidos_5_7"] += per5; sr["libres_5_7"] += lib5
            if warn in T:
                sr["vivas_en_warn"] += 1
                v57 = [t for t in sorted(T) if t >= warn]; vent = [t for t in v57 if t < sig]
                v["tics_5_7"] = len(v57); v["ardiendo_5_7"] = sum(1 for t in v57 if math.dist(T[t]["pos"], C) > T[t]["radio"])
                v["tics_f5"] = len(vent); v["ardiendo_f5"] = sum(1 for t in vent if math.dist(T[t]["pos"], C) > T[t]["radio"])
                v["dentro_pct_f5"] = round(100 * sum(1 for t in vent if math.dist(T[t]["pos"], C) <= r1) / max(1, len(vent)), 1)
                v["golpes_anillo_5_7"] = sum(1 for t in v57 if T[t]["zone_hit"])
                sr["ardiendo_5_7"].append(v["ardiendo_5_7"]); sr["ardiendo_f5"].append(v["ardiendo_f5"]); sr["dentro_pct_f5"].append(v["dentro_pct_f5"])
                ac = [r for r in L["forma_aceptada"] if warn <= r["tick"] < sig]; ids = {r["id"] for r in ac}
                fin_por = {}
                for r in L["compromiso6"]:
                    if r.get("id") in ids and r.get("estado") == "cumplida":
                        fin_por[r["id"]] = "fin de fase" if r.get("por") == "fin de fase" else "andado"
                for r in L["forma_caida"]:
                    if r.get("id") in ids and r["id"] not in fin_por:
                        fin_por[r["id"]] = "caida"
                sost = sum(1 for r in ac if fin_por.get(r["id"]) == "fin de fase" or (fin_por.get(r["id"]) is None and mt >= sig))
                v["planes_f5"] = {"aceptados": len(ac), "sostenidos_fin_fase": sost}
                sr["sostenidos"] += sost; sr["aceptados_fase"] += len(ac)
            V.append(v)
        for k in ("ardiendo_5_7", "ardiendo_f5", "dentro_pct_f5"):
            sr[k + "_media"] = (round(st.mean(sr[k]), 2) if sr[k] else None)
        PS[str(sem)] = sr
        print(f"    {os.path.basename(carp)}: vivas warn5 {sr['vivas_en_warn']} · ardiendo 5-7 {sr['ardiendo_5_7']} · f5 {sr['ardiendo_f5']} · dentro f5 {sr['dentro_pct_f5']} · perdidos 5-7 {sr['perdidos_5_7']}/{sr['libres_5_7']}", flush=True)
    W = [v for v in V if v.get("viva_en_warn5")]
    res = {"partidas": len(carps), "vidas": len(V), "vivas_en_warn5": len(W),
           "ardiendo_5_7_media": (round(st.mean(v["ardiendo_5_7"] for v in W), 1) if W else None), "ardiendo_5_7_mediana": (st.median(v["ardiendo_5_7"] for v in W) if W else None), "vidas_0_ardiendo_5_7": sum(1 for v in W if v["ardiendo_5_7"] == 0),
           "ardiendo_f5_media": (round(st.mean(v["ardiendo_f5"] for v in W), 1) if W else None), "dentro_pct_f5_media": (round(st.mean(v["dentro_pct_f5"] for v in W), 1) if W else None),
           "planes_aceptados_f5": sum(v.get("planes_f5", {}).get("aceptados", 0) for v in W), "planes_sostenidos_f5": sum(v.get("planes_f5", {}).get("sostenidos_fin_fase", 0) for v in W),
           "pasos_libres_5_7": sum(v["pasos_libres_5_7"] for v in V), "pasos_perdidos_5_7": sum(v["pasos_perdidos_5_7"] for v in V),
           "muertes_anillo": sum(1 for v in V if v["causa"] == "anillo"), "muertes_rival": sum(1 for v in V if v["causa"] == "rival"), "supervivientes": sum(v["superviviente"] for v in V)}
    res["pct_pasos_perdidos_5_7"] = round(100 * res["pasos_perdidos_5_7"] / max(1, res["pasos_libres_5_7"]), 2)
    OUT["brazos"][etiq] = {"resumen": res, "vidas": V, "por_semilla": PS}
    print(f"### {etiq}: {json.dumps(res, ensure_ascii=False)}")

B_ = OUT["brazos"]
if "A7h" in B_ and "A4" in B_:
    A, B = B_["A7h"]["por_semilla"], B_["A4"]["por_semilla"]
    OUT["principal"] = {"que": "tics ardiendo en las fases 5-7, por vida viva en el aviso 5, media por semilla, A7h - A4", "A7h - A4": empareja(A, B, "ardiendo_5_7_media", unilateral=True)}
    OUT["secundarias"] = {"A7h - A4": {c: empareja(A, B, c) for c in ("ardiendo_f5_media", "dentro_pct_f5_media", "sostenidos", "aceptados_fase", "perdidos_5_7", "anillo", "rival", "supervivientes")}}
    print("=== PRINCIPAL", json.dumps(OUT["principal"], ensure_ascii=False)); print("=== secundarias", json.dumps(OUT["secundarias"], ensure_ascii=False))
json.dump(OUT, open(os.path.join(AQUI, salida), "w"), ensure_ascii=False, indent=1)
print("->", salida)

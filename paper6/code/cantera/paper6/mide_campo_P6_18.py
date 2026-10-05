"""[P6-18 · B.8] LAS MEDIDAS DE CAMPO, por tics, para las vidas vivas al empezar la fase
que mata (fase 5, aviso 11.856), en A4, A5h y A6, emparejadas por semilla. SOLO LECTURA.

    python3 mide_campo_P6_18.py 'A4=paintball/runs/P611_t*_A4_*' 'A5h=paintball/runs/P616_t2_A5h_*' 'A6=paintball/runs/P618_t1_A6_*'

Principales (definiciones de P6-17, tal cual):
  · % de tics DENTRO del circulo en la fase 5: distancia al centro <= r1 (5) de
    la fase, sobre los tics vivos entre el aviso (11.856) y el siguiente (12.996);
  · tics ardiendo en la fase 5: distancia al centro > `zona.radius` del tic (la
    definicion de P6-17 §2); ademas, golpes del anillo (`damage_taken` de `zone`);
  · planes (A5h/A6): aceptados en la fase, sostenidos hasta el final de la fase
    (`cumplida` por «fin de fase» o vivos al llegar el siguiente aviso, o
    cumplida por sus puntos de control), y rupturas con motivo (`compromiso6`).
Secundarias (poca potencia): muertes por anillo, por rival, supervivientes
(definiciones de mide_P6_16). Emparejado por semilla: media de la diferencia,
gana/pierde, y test de permutacion por cambio de signo (2^n) como en P6-17.
"""
import collections, glob, json, math, os, re, statistics as st, sys
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
C = (24, 24); FASE = 4     # indice de la fase 5


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo")
    fin = next((r for r in recs if r.get("k") == "final"), None)
    dano = {it["id"]: float(it.get("damage") or 0) for it in cat["items"]}
    T = {}; L = collections.defaultdict(list)
    for r in recs:
        k = r.get("k")
        if k in ("forma_aceptada", "compromiso6", "forma_caida", "forma_evaluada", "oraculo16", "resumen16", "resumen18"):
            L[k].append(r)
        if k != "tick" or r.get("phase") != "live":
            continue
        T[r["tick"]] = {"pos": tuple(int(x) for x in r["pos"]), "zone_hit": any(g.get("source") == "zone" for g in (r.get("damage_taken") or [])), "radio": float((r.get("zona") or {}).get("radius") or 48),
                        "dt": [g for g in (r.get("damage_taken") or []) if isinstance(g, dict)], "ve": {a.get("slot"): a for a in (r.get("ve_agentes") or []) if a.get("pos")}}
    del recs
    return pc, T, fin, L, dano, [tuple(z) for z in pc.get("zone_schedule") or []]


def causa(T, fin, dano):
    if not (fin and fin.get("reason") == "eliminated"):
        return None
    tl = sorted(T); mt = int(fin.get("match_ticks") or tl[-1])
    golpes = [(t, str(g.get("source"))) for t in tl for g in T[t]["dt"] if str(g.get("source")).startswith("P")]
    cerca = [g for g in golpes if mt - 48 <= g[0] <= mt]; zt = [t for t in tl if mt - 48 <= t <= mt and T[t]["zone_hit"]]
    if cerca and (not zt or cerca[-1][0] >= max(zt)):
        return "rival"
    return "anillo" if zt else "no consta"


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    V = []; PS = {}
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1]); sr = {"semilla": sem, "supervivientes": 0, "anillo": 0, "rival": 0, "dentro_pct": [], "ardiendo": [], "vivas_en_warn": 0, "sostenidos": 0, "aceptados_fase": 0}
        for sl in (10, 11):
            pc, T, fin, L, dano, fases = carga(fs[sl])
            warn, shrink, done, r0, r1, dps = fases[FASE]; sig = fases[FASE + 1][0]
            mt = max(T); c = causa(T, fin, dano)
            v = {"semilla": sem, "slot": sl, "tics": mt, "superviviente": bool(fin and fin.get("reason") != "eliminated"), "causa": c, "viva_en_warn5": warn in T}
            sr["supervivientes"] += v["superviviente"]; sr["anillo"] += (c == "anillo"); sr["rival"] += (c == "rival")
            if warn in T:
                sr["vivas_en_warn"] += 1
                vent = [t for t in sorted(T) if warn <= t < sig]
                v["tics_fase"] = len(vent); v["dentro_pct"] = round(100 * sum(1 for t in vent if math.dist(T[t]["pos"], C) <= r1) / max(1, len(vent)), 1)
                v["ardiendo"] = sum(1 for t in vent if math.dist(T[t]["pos"], C) > T[t]["radio"]); v["golpes_anillo"] = sum(1 for t in vent if T[t]["zone_hit"]); v["sobrevive_fase"] = (mt >= sig) or v["superviviente"]
                v["entra"] = next((t for t in vent if math.dist(T[t]["pos"], C) <= r1), None)
                sr["dentro_pct"].append(v["dentro_pct"]); sr["ardiendo"].append(v["ardiendo"])
                # los planes de la fase
                ac = [r for r in L["forma_aceptada"] if warn <= r["tick"] < sig]; ids = {r["id"] for r in ac}
                fin_por = {}
                for r in L["compromiso6"]:
                    if r.get("id") in ids and r.get("estado") == "cumplida":
                        fin_por[r["id"]] = "fin de fase" if r.get("por") == "fin de fase" else ("andado (" + str(r.get("por")) + ")")
                for r in L["forma_caida"]:
                    if r.get("id") in ids and r["id"] not in fin_por:
                        fin_por[r["id"]] = "caida: " + str(r.get("motivo"))[:50]
                rup = collections.Counter(str(r.get("causa"))[:2] for r in L["compromiso6"] if r.get("id") in ids and r.get("estado") == "rompe")
                est = collections.Counter(r.get("estado") for r in L["compromiso6"] if r.get("id") in ids)
                sost = 0
                for r in ac:
                    f_ = fin_por.get(r["id"])
                    if f_ == "fin de fase" or f_ is None:      # sin cierre en la fase: vivo al llegar el siguiente aviso (o muerto con el plan vivo)
                        sost += (f_ == "fin de fase") or (mt >= sig)
                v["planes"] = {"aceptados": len(ac), "sostenidos_fin_fase": sost, "fines": dict(collections.Counter(fin_por.values())), "rupturas": dict(rup), "estados": dict(est)}
                sr["sostenidos"] += sost; sr["aceptados_fase"] += len(ac)
                r18 = (L.get("resumen18") or L.get("resumen16") or [None])[-1]
                v["sujeta_total"] = (r18 or {}).get("sujeta")
            V.append(v)
        sr["dentro_pct_media"] = (round(st.mean(sr["dentro_pct"]), 1) if sr["dentro_pct"] else None); sr["ardiendo_media"] = (round(st.mean(sr["ardiendo"]), 1) if sr["ardiendo"] else None)
        PS[str(sem)] = sr
        print(f"    {os.path.basename(carp)}: vivas warn5 {sr['vivas_en_warn']} · dentro {sr['dentro_pct']} · ardiendo {sr['ardiendo']} · aceptados {sr['aceptados_fase']} sostenidos {sr['sostenidos']}", flush=True)
    W = [v for v in V if v.get("viva_en_warn5")]
    res = {"vidas": len(V), "vivas_en_warn5": len(W), "dentro_pct_media": round(st.mean(v["dentro_pct"] for v in W), 1), "dentro_pct_mediana": st.median(v["dentro_pct"] for v in W),
           "ardiendo_media": round(st.mean(v["ardiendo"] for v in W), 1), "ardiendo_mediana": st.median(v["ardiendo"] for v in W), "vidas_0_ardiendo": sum(1 for v in W if v["ardiendo"] == 0),
           "nunca_entra": sum(1 for v in W if v["entra"] is None), "sobreviven_fase5": sum(v["sobrevive_fase"] for v in W),
           "planes_aceptados_fase5": sum(v.get("planes", {}).get("aceptados", 0) for v in W), "planes_sostenidos": sum(v.get("planes", {}).get("sostenidos_fin_fase", 0) for v in W),
           "fines": dict(sum((collections.Counter(v.get("planes", {}).get("fines", {})) for v in W), collections.Counter())),
           "rupturas": dict(sum((collections.Counter(v.get("planes", {}).get("rupturas", {})) for v in W), collections.Counter())),
           "estados_compromiso": dict(sum((collections.Counter(v.get("planes", {}).get("estados", {})) for v in W), collections.Counter())),
           "muertes_anillo": sum(1 for v in V if v["causa"] == "anillo"), "muertes_rival": sum(1 for v in V if v["causa"] == "rival"), "supervivientes": sum(v["superviviente"] for v in V)}
    OUT[etiq] = {"resumen": res, "vidas": V, "por_semilla": PS}
    print(f"### {etiq}: {json.dumps(res, ensure_ascii=False)}")


def permutacion(d):
    n = len(d); obs = sum(d) / n
    if all(x == 0 for x in d):
        return 1.0
    dd = np.array(d, dtype=float); idx = np.arange(2 ** n, dtype=np.int64)
    signs = (((idx[:, None] >> np.arange(n)) & 1) * 2 - 1).astype(np.int8)
    return float(np.mean(np.abs(signs @ dd / n) >= abs(obs) - 1e-12))


if "A6" in OUT:
    OUT["_emparejado"] = {}
    for base in ("A4", "A5h"):
        if base not in OUT:
            continue
        E = {}
        for k in ("dentro_pct_media", "ardiendo_media", "supervivientes", "anillo", "rival"):
            pares = [(OUT["A6"]["por_semilla"][s][k], OUT[base]["por_semilla"][s][k]) for s in OUT["A6"]["por_semilla"] if s in OUT[base]["por_semilla"] and OUT["A6"]["por_semilla"][s][k] is not None and OUT[base]["por_semilla"][s][k] is not None]
            d = [float(a) - float(b) for a, b in pares]
            E[k] = {"n": len(d), "media_dif": (round(sum(d) / len(d), 2) if d else None), "gana": sum(1 for x in d if x > 0), "pierde": sum(1 for x in d if x < 0), "p_perm": (round(permutacion(d), 4) if d else None)}
        OUT["_emparejado"][f"A6 - {base}"] = E
        print(f"### A6 - {base}: {json.dumps(E, ensure_ascii=False)}")
json.dump(OUT, open(os.path.join(AQUI, "P6_18_campo.json"), "w"), ensure_ascii=False, indent=1)
print("-> cantera/paper6/P6_18_campo.json")

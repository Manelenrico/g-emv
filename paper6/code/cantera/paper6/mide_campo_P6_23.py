"""[P6-23 · 3] LAS MEDIDAS DE CAMPO, por tics y planes, para las vidas vivas en el aviso de la
fase 5, en A4 (P6-11), A7v y A7h, emparejadas por semilla. SOLO LECTURA, diarios de uno en uno.

    python3 mide_campo_P6_23.py 'A4=paintball/runs/P611_t*_A4_*' 'A7v=paintball/runs/P623_t1_A7v_*' 'A7h=paintball/runs/P623_t2_A7h_*'

Principales (definiciones de P6-17/P6-18, tal cual, mas las de P6-21/P6-23):
  · pasos perdidos (P6-21): paso listo hacia casilla libre con respuesta `ok` sin moverse; en
    toda la vida y en las fases 5-7;
  · % de tics DENTRO del circulo en la fase 5 (distancia al centro <= r1 de la fase) sobre
    los tics vivos entre el aviso 5 y el 6; tics ARDIENDO (distancia > `zona.radius` del tic);
  · planes de la fase 5: aceptados, andados (algun `obedece`), sostenidos hasta el final de
    la fase (`cumplida` por fin de fase o vivos al siguiente aviso), rupturas por motivo;
  · suspensiones y reanudaciones (`compromiso6` suspende / reanuda), alertas, retenido, sale;
  · en la pareja: semillas en que los dos asientos aceptan algun plan en la fase 5.
Secundarias (poca potencia, declarado): muertes por anillo y por rival (causa de P6-16),
supervivientes. Emparejado por semilla (media de la diferencia, gana/pierde, permutacion
exacta por cambio de signo, 2^n).
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


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    V = []; PS = {}
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1]); sr = {"semilla": sem, "supervivientes": 0, "anillo": 0, "rival": 0, "dentro_pct": [], "ardiendo": [], "vivas_en_warn": 0, "sostenidos": 0, "aceptados_fase": 0, "aceptan_los_dos": 0, "perdidos": 0, "libres": 0}
        for sl in (10, 11):
            pc, T, fin, L, mundo, fases = carga(fs[sl])
            warn, shrink, done, r0, r1, dps = fases[FASE]; sig = fases[FASE + 1][0]
            mt = max(T); c = causa(T, fin)
            lib, per = perdidos(T, mundo); lib5, per5 = perdidos(T, mundo, desde=warn)
            v = {"semilla": sem, "slot": sl, "tics": mt, "superviviente": bool(fin and fin.get("reason") != "eliminated"), "causa": c, "viva_en_warn5": warn in T, "pasos_libres": lib, "pasos_perdidos": per, "pasos_libres_5_7": lib5, "pasos_perdidos_5_7": per5}
            sr["supervivientes"] += v["superviviente"]; sr["anillo"] += (c == "anillo"); sr["rival"] += (c == "rival"); sr["perdidos"] += per; sr["libres"] += lib
            if warn in T:
                sr["vivas_en_warn"] += 1
                vent = [t for t in sorted(T) if warn <= t < sig]
                v["tics_fase"] = len(vent); v["dentro_pct"] = round(100 * sum(1 for t in vent if math.dist(T[t]["pos"], C) <= r1) / max(1, len(vent)), 1)
                v["ardiendo"] = sum(1 for t in vent if math.dist(T[t]["pos"], C) > T[t]["radio"]); v["golpes_anillo"] = sum(1 for t in vent if T[t]["zone_hit"]); v["sobrevive_fase"] = (mt >= sig) or v["superviviente"]
                v["entra"] = next((t for t in vent if math.dist(T[t]["pos"], C) <= r1), None)
                sr["dentro_pct"].append(v["dentro_pct"]); sr["ardiendo"].append(v["ardiendo"])
                ac = [r for r in L["forma_aceptada"] if warn <= r["tick"] < sig]; ids = {r["id"] for r in ac}
                fin_por = {}
                for r in L["compromiso6"]:
                    if r.get("id") in ids and r.get("estado") == "cumplida":
                        fin_por[r["id"]] = "fin de fase" if r.get("por") == "fin de fase" else ("andado (" + str(r.get("por")) + ")")
                for r in L["forma_caida"]:
                    if r.get("id") in ids and r["id"] not in fin_por:
                        fin_por[r["id"]] = "caida: " + str(r.get("motivo"))[:60]
                est = collections.Counter(r.get("estado") for r in L["compromiso6"] if r.get("id") in ids)
                rup = collections.Counter(str(r.get("causa"))[:40] for r in L["compromiso6"] if r.get("id") in ids and r.get("estado") == "rompe")
                andados = {r.get("id") for r in L["compromiso6"] if r.get("id") in ids and r.get("estado") == "obedece"}
                sost = 0
                for r in ac:
                    f_ = fin_por.get(r["id"])
                    if f_ == "fin de fase" or f_ is None:
                        sost += (f_ == "fin de fase") or (mt >= sig)
                v["planes"] = {"aceptados": len(ac), "andados": len(andados), "sostenidos_fin_fase": sost, "fines": dict(collections.Counter(fin_por.values())), "rupturas": dict(rup), "estados": dict(est),
                               "suspensiones": est.get("suspende", 0), "reanudaciones": est.get("reanuda", 0), "alertas": est.get("alerta", 0), "retenido": est.get("retenido", 0), "sale": est.get("sale", 0),
                               "caidas_vida_real": sum(1 for f_ in fin_por.values() if "vida real" in f_), "caidas_cuenta_justa": sum(1 for f_ in fin_por.values() if "cuenta justa" in f_)}
                sr["sostenidos"] += sost; sr["aceptados_fase"] += len(ac); sr["aceptan_los_dos"] += (1 if len(ac) else 0)
                r23 = (L.get("resumen23") or L.get("resumen18") or L.get("resumen16") or [None])[-1]
                v["resumen"] = ({k: r23.get(k) for k in ("sujeta", "alertas", "suspensiones", "reanudaciones", "tics_suspendida", "retenido", "sale", "instantaneas", "encargos_oraculo", "errores_juez")} if r23 else None)
            V.append(v)
        sr["aceptan_los_dos"] = int(sr["aceptan_los_dos"] == 2)
        sr["dentro_pct_media"] = (round(st.mean(sr["dentro_pct"]), 1) if sr["dentro_pct"] else None); sr["ardiendo_media"] = (round(st.mean(sr["ardiendo"]), 1) if sr["ardiendo"] else None)
        PS[str(sem)] = sr
        print(f"    {os.path.basename(carp)}: vivas warn5 {sr['vivas_en_warn']} · dentro {sr['dentro_pct']} · ardiendo {sr['ardiendo']} · aceptados {sr['aceptados_fase']} sostenidos {sr['sostenidos']} · perdidos {sr['perdidos']}/{sr['libres']}", flush=True)
    W = [v for v in V if v.get("viva_en_warn5")]
    res = {"vidas": len(V), "vivas_en_warn5": len(W), "pasos_libres": sum(v["pasos_libres"] for v in V), "pasos_perdidos": sum(v["pasos_perdidos"] for v in V),
           "pasos_libres_5_7": sum(v["pasos_libres_5_7"] for v in V), "pasos_perdidos_5_7": sum(v["pasos_perdidos_5_7"] for v in V),
           "dentro_pct_media": (round(st.mean(v["dentro_pct"] for v in W), 1) if W else None), "dentro_pct_mediana": (st.median(v["dentro_pct"] for v in W) if W else None),
           "ardiendo_media": (round(st.mean(v["ardiendo"] for v in W), 1) if W else None), "ardiendo_mediana": (st.median(v["ardiendo"] for v in W) if W else None), "vidas_0_ardiendo": sum(1 for v in W if v["ardiendo"] == 0),
           "nunca_entra": sum(1 for v in W if v["entra"] is None), "sobreviven_fase5": sum(v["sobrevive_fase"] for v in W),
           "planes_aceptados_fase5": sum(v.get("planes", {}).get("aceptados", 0) for v in W), "planes_andados": sum(v.get("planes", {}).get("andados", 0) for v in W), "planes_sostenidos": sum(v.get("planes", {}).get("sostenidos_fin_fase", 0) for v in W),
           "fines": dict(sum((collections.Counter(v.get("planes", {}).get("fines", {})) for v in W), collections.Counter())),
           "rupturas": dict(sum((collections.Counter(v.get("planes", {}).get("rupturas", {})) for v in W), collections.Counter())),
           "estados_compromiso": dict(sum((collections.Counter(v.get("planes", {}).get("estados", {})) for v in W), collections.Counter())),
           "suspensiones": sum(v.get("planes", {}).get("suspensiones", 0) for v in W), "reanudaciones": sum(v.get("planes", {}).get("reanudaciones", 0) for v in W), "alertas": sum(v.get("planes", {}).get("alertas", 0) for v in W),
           "retenido": sum(v.get("planes", {}).get("retenido", 0) for v in W), "sale": sum(v.get("planes", {}).get("sale", 0) for v in W),
           "caidas_vida_real": sum(v.get("planes", {}).get("caidas_vida_real", 0) for v in W), "caidas_cuenta_justa": sum(v.get("planes", {}).get("caidas_cuenta_justa", 0) for v in W),
           "semillas_aceptan_los_dos": sum(sr["aceptan_los_dos"] for sr in PS.values()),
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


def empareja(a, b, campo):
    A, B = OUT[a]["por_semilla"], OUT[b]["por_semilla"]; d = []
    for s in sorted(set(A) & set(B)):
        x, y = A[s].get(campo), B[s].get(campo)
        if x is None or y is None:
            continue
        d.append(x - y)
    if not d:
        return None
    return {"n": len(d), "media_dif": round(st.mean(d), 2), "gana": sum(1 for x in d if x > 0), "pierde": sum(1 for x in d if x < 0), "p": round(permutacion(d), 3)}


EMP = {}
for a, b in (("A7v", "A4"), ("A7h", "A4"), ("A7h", "A7v")):
    if a in OUT and b in OUT:
        EMP[f"{a} - {b}"] = {c: empareja(a, b, c) for c in ("dentro_pct_media", "ardiendo_media", "sostenidos", "aceptados_fase", "supervivientes", "anillo", "rival", "perdidos")}
        print(f"=== {a} - {b}: {json.dumps(EMP[f'{a} - {b}'], ensure_ascii=False)}")
OUT["emparejado"] = EMP
json.dump(OUT, open(os.path.join(AQUI, "P6_23_campo.json"), "w"), ensure_ascii=False, indent=1)
print("-> P6_23_campo.json")

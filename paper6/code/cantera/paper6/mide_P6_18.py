"""[P6-18 · A.3-A.5 y los momentos] SOLO LECTURA de diarios (A4, A5h, A3), uno a uno.

  · MOMENTOS DE SALIDA: los 63 de A5h (P6_17_salidas.json: el tic del ultimo
    movimiento antes de salir) y los equivalentes de A4 (las 22 muertes por
    anillo de P6_17_final.json: el ultimo `elegido` de movimiento en los 12 tics
    antes de `sale`). -> P6_18_momentos.json (para el banco).
  · A.3 EL VETO VITAL: `compromiso6_P6_16.rupturas6 (a)` = un rival VISTO con
    arma de alcance > 0 (catalogo) a distancia Chebyshev <= alcance. Se mide en
    los 353 registros de A5h (arma del rival, distancia, hp y R-CARENCIA del
    cuerpo en ese tic) y en los momentos de salida y su ventana de quedarse
    (hasta el final de la fase): en que fraccion de tics se cumple.
  · A.4 R-CARENCIA = (W_TARGET - W) / W_TARGET, W = riqueza (arma + botiquin +
    raciones, `appraisal.riqueza_W`). Se descompone con `riqueza_W` sobre el
    `you` del diario; nivel en los momentos de salida, en la fase que mata y en
    toda la partida; A4 contra A3 (P6-10) y A5h.
  · A.5 S-MUERTE-PAREJA = duelo (factor x B) tras la muerte del hermano (o su
    muerte prevista): no tiene destino; `ir_pareja` deja de generarse con
    `pareja_muerta`. Se mide en los momentos de salida con la fila encendida:
    el elegido, la ultima casilla del hermano, si ardia, y la muerte propia en
    los 300 tics siguientes.
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    sys.path.insert(0, p)
os.environ.setdefault("GEMV_MEMORIA", os.path.join(RAIZ, "paintball", "alma", "memoria_aprendida_p95.json"))
import serie_util as U
from alma import appraisal_zs_v42_exp as A
import curiosidad as CUR
C = (24, 24)
BRAZOS = {"A3": "paintball/runs/P610_t*_A3_*", "A4": "paintball/runs/P611_t*_A4_*", "A5h": "paintball/runs/P616_t2_A5h_*"}
J17 = json.load(open(os.path.join(AQUI, "P6_17_final.json")))
SAL17 = json.load(open(os.path.join(AQUI, "P6_17_salidas.json")))


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); fin = next((r for r in recs if r.get("k") == "final"), None)
    T = {}; L = collections.defaultdict(list)
    for r in recs:
        k = r.get("k")
        if k == "compromiso6":
            L[k].append(r)
        if k != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = {"pos": tuple(int(x) for x in r["pos"]), "hp": float(r.get("hp") if r.get("hp") is not None else 100), "el": str(ra.get("elegido") or ""),
                        "radio": float((r.get("zona") or {}).get("radius") or 48), "ve": [a for a in (r.get("ve_agentes") or []) if a.get("pos")],
                        "you": {"hand": r.get("hand"), "pack": r.get("pack") or [], "body": r.get("body")},
                        "ahora": {kk: vv.get("M", 0.0) for kk, vv in ((ra.get("ahora") or {}).get("filas") or {}).items()} if isinstance(ra, dict) else {},
                        "pareja_muerta": bool(r.get("pareja_muerta")), "dt": [g for g in (r.get("damage_taken") or []) if isinstance(g, dict)]}
    del recs
    return mundo, pc, T, fin, L, [tuple(z) for z in pc.get("zone_schedule") or []]


def fase_activa(fases, t):
    k = None
    for i, f in enumerate(fases):
        if f[0] <= t:
            k = i
    return k


def veto(mundo, r, herm):
    """(True/False, [(slot, arma, alcance, dist)]) — la condicion (a) de rupturas6 en este tic."""
    pos = r["pos"]; arms = []
    for a in r["ve"]:
        if a.get("slot") == herm:
            continue
        rg = CUR._alcance(mundo, a.get("hand"))
        if rg > 0:
            d = cheb(pos, tuple(a["pos"]))
            if d <= rg:
                arms.append((a.get("slot"), (a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand"), rg, d))
    return bool(arms), arms


# ── los momentos ────────────────────────────────────────────────────────────
MOM = []
for s in SAL17:
    MOM.append({"brazo": "A5h", "carp": f"P616_t2_A5h_{s['semilla']}", "semilla": s["semilla"], "slot": s["slot"], "llegada": s["tick"], "sale": s["sale"],
                "tick": s["ultimo_movimiento"][0], "elegido": s["ultimo_movimiento"][1], "pos": s["pos_llegada"]})
MOM_A4 = [d for d in J17["fuego"]["muertes_anillo"] if d["brazo"] == "A4"]
OUT = {"nota": "P6-18 A.3-A.5. INSTRUMENTO DE MEDIDA, solo lectura."}
VETO = {"registros_A5h": [], "en_momentos": [], "ventana": []}
CAR = collections.defaultdict(list); CAR_FASE = collections.defaultdict(list); CAR_MOM = []; DESG_MOM = collections.Counter(); DESG_TODOS = collections.defaultdict(list)
DUELO = []
for brazo, pat in BRAZOS.items():
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1])
        G = {sl: carga(fs[sl]) for sl in (10, 11)}
        for sl in (10, 11):
            mundo, pc, T, fin, L, fases = G[sl]; To = G[21 - sl][2]; herm = pc["teammate_slot"]; ts = sorted(T); mt = max(T)
            # A.4 · R-CARENCIA por tic (toda la partida y la fase que mata = fase activa de la muerte, o la 5)
            vals = [T[t]["ahora"].get("R-CARENCIA", 0.0) for t in ts if T[t]["ahora"]]
            if vals:
                CAR[brazo].append(st.mean(vals))
            i_m = fase_activa(fases, mt) if (fin or {}).get("reason") == "eliminated" else 4
            if i_m is not None and i_m < len(fases):
                w0 = fases[i_m][0]; w1 = fases[i_m + 1][0] if i_m + 1 < len(fases) else 10 ** 9
                vf = [T[t]["ahora"].get("R-CARENCIA", 0.0) for t in ts if w0 <= t < w1 and T[t]["ahora"]]
                if vf:
                    CAR_FASE[brazo].append(st.mean(vf))
            # el desglose de W en toda la partida (muestra cada 96 tics)
            for t in ts[::96]:
                try:
                    W, desg = A.riqueza_W(T[t]["you"], mundo)
                    DESG_TODOS[brazo].append((desg.get("arma", 0), desg.get("botiquin", 0), desg.get("racion", desg.get("raciones", 0)), W))
                except Exception:
                    pass
            # A.3 · los registros de veto de A5h
            if brazo == "A5h":
                for c in L["compromiso6"]:
                    if c.get("estado") != "rompe" or not str(c.get("causa", "")).startswith("a)"):
                        continue
                    t = c["tick"]; r = T.get(t)
                    if not r:
                        continue
                    ok, arms = veto(mundo, r, herm)
                    VETO["registros_A5h"].append({"semilla": sem, "slot": sl, "tick": t, "hp": r["hp"], "R-CARENCIA": r["ahora"].get("R-CARENCIA"), "armados_a_tiro": arms, "recalculado": ok,
                                                  "dentro": math.dist(r["pos"], C) <= (fases[fase_activa(fases, t)][4] if fase_activa(fases, t) is not None else 48)})
            # los momentos de A4: el ultimo movimiento antes de `sale`
            if brazo == "A4":
                for d in MOM_A4:
                    if d["semilla"] != sem or d["slot"] != sl:
                        continue
                    mov = [t for t in ts if d["sale"] - 12 <= t < d["sale"] and T[t]["el"] and T[t]["el"] != "noop" and not T[t]["el"].startswith(("atacar", "usar", "coger"))]
                    td = mov[-1] if mov else max([t for t in ts if t < d["sale"]] or [d["sale"]])
                    MOM.append({"brazo": "A4", "carp": os.path.basename(carp), "semilla": sem, "slot": sl, "llegada": None, "sale": d["sale"], "tick": td, "elegido": T[td]["el"], "pos": list(T[td]["pos"]), "muerte": d["muerte"]})
            # en los momentos de esta vida: veto, carencia, duelo
            for m in MOM:
                if m["semilla"] != sem or m["slot"] != sl or m["brazo"] != brazo:
                    continue
                t = m["tick"]; r = T.get(t)
                if not r:
                    continue
                ok, arms = veto(mundo, r, herm)
                i = fase_activa(fases, t); fin_fase = (fases[i + 1][0] if (i is not None and i + 1 < len(fases)) else mt)
                vent = [u for u in ts if t <= u <= min(fin_fase, mt)]
                n_v = sum(1 for u in vent if veto(mundo, T[u], herm)[0])
                VETO["en_momentos"].append({"brazo": brazo, "semilla": sem, "slot": sl, "tick": t, "veto": ok, "armados": arms, "tics_ventana": len(vent), "tics_con_veto": n_v,
                                            "primer_veto_en": next((u - t for u in vent if veto(mundo, T[u], herm)[0]), None)})
                W, desg = A.riqueza_W(r["you"], mundo)
                falta = [k for k in ("arma", "botiquin") if desg.get(k, 0) < 0.5] + (["racion"] if desg.get("racion", desg.get("raciones", 0)) < 0.5 else [])
                CAR_MOM.append({"brazo": brazo, "semilla": sem, "slot": sl, "tick": t, "R-CARENCIA": r["ahora"].get("R-CARENCIA"), "W": round(W, 3), "desglose": {k: round(float(v), 3) for k, v in desg.items() if isinstance(v, (int, float))}, "falta": falta, "elegido": m["elegido"]})
                for k in falta:
                    DESG_MOM[(brazo, k)] += 1
                sm_ = r["ahora"].get("S-MUERTE-PAREJA", 0.0)
                if sm_ > 0:
                    ult_h = max(To) if To else None; pos_h = To[ult_h]["pos"] if ult_h else None
                    ardia = (math.dist(pos_h, C) > To[ult_h]["radio"]) if pos_h else None
                    DUELO.append({"brazo": brazo, "semilla": sem, "slot": sl, "tick": t, "M": round(sm_, 3), "pareja_muerta": r["pareja_muerta"], "elegido": m["elegido"],
                                  "hermano_muerto_en": ult_h, "pos_hermano": (list(pos_h) if pos_h else None), "dist": (cheb(r["pos"], pos_h) if pos_h else None), "esa_casilla_ardia": ardia,
                                  "yo_muero_en_300": (mt - t <= 300 and (fin or {}).get("reason") == "eliminated"), "mi_muerte": (mt if (fin or {}).get("reason") == "eliminated" else None)})
        del G
        print(f"  {brazo} {sem}", flush=True)

json.dump(MOM, open(os.path.join(AQUI, "P6_18_momentos.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nmomentos: {collections.Counter(m['brazo'] for m in MOM)}")
# A.3
R = VETO["registros_A5h"]
armas = collections.Counter(a[1] for x in R for a in x["armados_a_tiro"])
print(f"\nA.3 veto vital: registros {len(R)} · recalculado igual {sum(1 for x in R if x['recalculado'])} · armas a tiro {armas} · hp mediana {st.median(x['hp'] for x in R) if R else None} · R-CARENCIA mediana {st.median(x['R-CARENCIA'] or 0 for x in R) if R else None} · dentro del circulo {sum(1 for x in R if x['dentro'])}")
EM = VETO["en_momentos"]
for b in ("A5h", "A4"):
    e = [x for x in EM if x["brazo"] == b]
    print(f"   momentos {b}: {len(e)} · veto en el momento {sum(1 for x in e if x['veto'])} · fraccion de tics con veto en la ventana mediana {st.median(x['tics_con_veto'] / max(1, x['tics_ventana']) for x in e) if e else None} · ventanas con algun veto {sum(1 for x in e if x['tics_con_veto'])} · primer veto mediana {st.median([x['primer_veto_en'] for x in e if x['primer_veto_en'] is not None]) if any(x['primer_veto_en'] is not None for x in e) else None}")
OUT["veto"] = {"registros": R, "en_momentos": EM, "armas_a_tiro": dict(armas)}
# A.4
print("\nA.4 R-CARENCIA media por vida:", {b: round(st.mean(v), 3) for b, v in CAR.items()}, "· en la fase que mata:", {b: round(st.mean(v), 3) for b, v in CAR_FASE.items()})
for b in ("A5h", "A4"):
    cm = [c for c in CAR_MOM if c["brazo"] == b]
    print(f"   en los momentos de salida {b}: n {len(cm)} · R-CARENCIA mediana {st.median(c['R-CARENCIA'] or 0 for c in cm) if cm else None} · W mediana {st.median(c['W'] for c in cm) if cm else None} · falta {collections.Counter(k for c in cm for k in c['falta'])}")
dg = {b: {"arma": round(st.mean(x[0] for x in v), 3), "botiquin": round(st.mean(x[1] for x in v), 3), "racion": round(st.mean(x[2] for x in v), 3), "W": round(st.mean(x[3] for x in v), 3), "n": len(v)} for b, v in DESG_TODOS.items()}
print("   desglose medio de W (muestras cada 96 tics):", dg)
OUT["carencia"] = {"media_por_vida": {b: [round(x, 4) for x in v] for b, v in CAR.items()}, "media_fase_que_mata": {b: [round(x, 4) for x in v] for b, v in CAR_FASE.items()}, "momentos": CAR_MOM, "desglose_medio": dg}
# A.5
print(f"\nA.5 S-MUERTE-PAREJA en los momentos: {len(DUELO)} · pareja_muerta {sum(1 for d in DUELO if d['pareja_muerta'])} · elegido {collections.Counter(d['elegido'].split('_')[0] for d in DUELO)} · casilla del hermano ardia {sum(1 for d in DUELO if d['esa_casilla_ardia'])} · dist mediana {st.median(d['dist'] for d in DUELO if d['dist'] is not None) if DUELO else None} · muero en 300 {sum(1 for d in DUELO if d['yo_muero_en_300'])}")
OUT["duelo"] = DUELO
json.dump(OUT, open(os.path.join(AQUI, "P6_18_medidas_A.json"), "w"), ensure_ascii=False, indent=1)
print("-> P6_18_momentos.json, P6_18_medidas_A.json")

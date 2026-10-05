"""[P6-10] S-COMPANIA EN CAMPO: donde se encendio, cuanto, y si respeto D0. SOLO LECTURA.
Por tic con tabla (`RADIOGRAFIA.ahora.filas`) del brazo A3: M de S-COMPANIA en
la tabla del tic (candidato `noop` = mi casilla); distancia de camino real al
hermano (vista o parte); tics con d <= D0 y M > 0 (tiene que ser 0); y en los
tics con detalle, si el ganador llevaba la fila > 0 estando yo dentro de D0.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
import filas10_P6_10 as F10
OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); Ms = []; dist_on = []
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            recs = list(U.lee(f))
            pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
            mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); herm = pc["teammate_slot"]
            arr = next((r for r in recs if r.get("k") == "arranque"), {})
            S["arranques con filas10"] += 1 if (arr.get("filas10") or {}).get("filas10") else 0
            for r in recs:
                if r.get("k") != "tick" or r.get("phase") != "live":
                    continue
                ra = r.get("RADIOGRAFIA") or {}; ah = ra.get("ahora") or {}; fl = ah.get("filas") or {}
                cs = ra.get("candidatos") or {}
                S["tics"] += 1
                if r.get("pareja_muerta"):
                    continue
                ph = None
                for a in (r.get("ve_agentes") or []):
                    if a.get("slot") == herm and a.get("pos"):
                        ph = (int(a["pos"][0]), int(a["pos"][1]))
                if ph is None and (ah.get("parte") or {}).get("pos"):
                    ph = tuple(int(x) for x in ah["parte"]["pos"])
                if ph is None:
                    continue
                d = F10.d_camino(mundo, tuple(int(x) for x in r["pos"]), ph)
                noop = cs.get("noop") if isinstance(cs.get("noop"), dict) else None
                m = float(((noop or {}).get("filas") or {}).get("S-COMPANIA") or 0.0) if noop else None
                S["tics con hermano vivo y posicion"] += 1
                if d is not None and d <= F10.D0:
                    S["  dentro de D0"] += 1
                    if m: S["  dentro de D0 con S-COMPANIA > 0 en mi casilla (ERROR)"] += 1
                    if noop:
                        el = ra.get("elegido"); g = cs.get(el) if isinstance(cs.get(el), dict) else None
                        S["  dentro de D0 con detalle"] += 1
                        if g and float((g.get("filas") or {}).get("S-COMPANIA") or 0) > 0:
                            S["  ...ganador con la fila > 0 (cruza D0)"] += 1
                else:
                    S["  fuera de D0"] += 1
                    if m is not None:
                        S["  fuera de D0 con detalle"] += 1
                        if m > 0: S["  ...S-COMPANIA > 0 en mi casilla"] += 1; Ms.append(m); dist_on.append(d if d is not None else 99)
            del recs
    OUT[etiq] = {"recuento": dict(S), "M_p50": st.median(Ms) if Ms else None, "M_max": max(Ms) if Ms else None, "d_p50": st.median(dist_on) if dist_on else None}
    print(f"### {etiq}")
    for k, v in S.items(): print(f"  {k:60s} {v}")
    if Ms: print(f"  M de S-COMPANIA fuera de D0: mediana {st.median(Ms):.3f} · max {max(Ms):.3f} · distancia mediana {st.median(dist_on)}")
json.dump(OUT, open(os.path.join(AQUI, "P6_10_fila.json"), "w"), ensure_ascii=False, indent=1)

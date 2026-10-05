"""[P6-4] Las medidas de la serie de los ojos compartidos. SOLO LECTURA.

Las del SELLO_P6_3.md primero, con sus definiciones tal y como se sellaron, y
despues las del encargo. Los diarios se leen de dos en dos (los dos asientos
de un episodio).
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, RAIZ)
import serie_util as U
from alma import appraisal_zs_v42_exp as A42
import parte2 as P2

NUESTROS = (10, 11)
ANILLO_AVISA, ANILLO_CIERRA = 7296, 8076     # del zone_schedule del mundo lento
VENTANA_CIEGA = 50          # la misma CADUCIDAD_RIVAL del oyente

FAM_TEMA = {"F-HERMANO-AMENAZA": "vinculos", "F-HERMANO-GOLPE": "vinculos",
            "R-HERMANO-FALTA": "vinculos", "F-REENCUENTRO": "vinculos"}


def fam(n):
    if n in FAM_TEMA:
        return FAM_TEMA[n]
    if n.startswith("S-"):
        return "vinculos"
    if n.startswith("R-"):
        return "recursos"
    return "cuerpo"


def d_de(F_):
    from motor.model import State as _S, opponent_distance, DEFAULT_CONFIG
    pF = nF = pR = nR = pS = nS = 0.0
    for nom, (fF, fR, fS) in A42.REPARTO.items():
        M = float(F_.get(nom) or 0.0)
        if M <= 0.0:
            continue
        aF, aR, aS = M * fF, M * fR, M * fS
        if nom in A42.APETITIVAS:
            pF += aF; pR += aR; pS += aS
        else:
            nF += aF; nR += aR; nS += aS
    return opponent_distance(_S(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS),
                             DEFAULT_CONFIG)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    fin = next((r for r in recs if r.get("k") == "final"), {})
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    ojos = [r for r in recs if r.get("k") == "ojos"]
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = {
            "pos": tuple(r.get("pos") or ()), "hp": r.get("hp"),
            "hand": (r.get("hand") or {}).get("id"),
            "body": (r.get("body") or {}).get("id")
                    if isinstance(r.get("body"), dict) else r.get("body"),
            "pack_n": {(s or {}).get("id"): int((s or {}).get("n") or 1)
                       for s in (r.get("pack") or []) if s},
            "items": [(x.get("id"), (int(x["pos"][0]), int(x["pos"][1])))
                      for x in (r.get("ve_items") or []) if x.get("pos")],
            "ag": [{"slot": a.get("slot"),
                    "pos": (int(a["pos"][0]), int(a["pos"][1])),
                    "hand": (a.get("hand") or {}).get("id")
                            if isinstance(a.get("hand"), dict) else a.get("hand")}
                   for a in (r.get("ve_agentes") or []) if a.get("pos")],
            "listas": int(r.get("move_ready_in") or 0) == 0,
            "filas": {k: v.get("M") for k, v in
                      ((ra.get("ahora") or {}).get("filas") or {}).items()},
            "cand": ra.get("candidatos"), "elegido": ra.get("elegido"),
            "d_ahora": ra.get("d_ahora"),
            "dano": [(g.get("source"), float(g.get("amount") or 0))
                     for g in (r.get("damage_taken") or [])],
        }
    del recs
    return mundo, pc, T, fin, ojos


def mide(carps, etiqueta):
    S = {"etiqueta": etiqueta, "vidas": [], "por_semilla": {},
         "c": collections.Counter(), "disc": [], "disc_s8": [],
         "fam": collections.Counter(), "fam_abs": collections.Counter()}
    for carp in carps:
        fs = {}
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl in NUESTROS:
                fs[sl] = f
        if len(fs) != 2:
            S["c"]["episodio sin los dos diarios"] += 1
            continue
        semilla = int(carp.rsplit("_", 1)[1])
        D = {}
        for sl, f in fs.items():
            mundo, pc, T, fin, ojos = carga(f)
            D[sl] = {"T": T, "fin": fin, "ojos": ojos, "mundo": mundo,
                     "herm": pc.get("teammate_slot")}
        a, b = NUESTROS
        mundo = D[a]["mundo"]
        S["c"]["episodios"] += 1
        # ── lo contado, tic a tic, del propio diario (`k: "ojos"`) ────────
        CONT = {}
        for sl in (a, b):
            riv, rec, cad = {}, {}, None
            m = {}
            for o in D[sl]["ojos"]:
                if o.get("estado") != "inyectado":
                    continue
                m[o["tick"]] = o
            CONT[sl] = m
            S["c"][f"tics con inyeccion a{sl}"] += len(m)
        for sl in (a, b):
            S["c"]["candidatos vetados"] += sum(
                len(o.get("candidatos") or []) for o in D[sl]["ojos"]
                if o.get("estado") == "vetados")
            S["c"]["partes E2 dichos"] += sum(
                1 for o in D[sl]["ojos"] if o.get("estado") == "dicho")
            S["c"]["fallos de emision"] += sum(
                1 for o in D[sl]["ojos"] if o.get("estado") == "fallo_emision")
        # ── vidas ────────────────────────────────────────────────────────
        juntos = sorted(set(D[a]["T"]) & set(D[b]["T"]))
        ev2c = 0
        golpes_ciegos = collections.Counter()
        for t in juntos:
            ra, rb = D[a]["T"][t], D[b]["T"][t]
            if not (ra["pos"] and rb["pos"]):
                continue
            for quien, otro, rq, ro in ((a, b, ra, rb), (b, a, rb, ra)):
                iq = {(i, p) for i, p in rq["items"]}
                io = {(i, p) for i, p in ro["items"]}
                for iid, p in (iq - io):
                    cl = P2.clase_de(mundo, iid)
                    if cl in ("otro", "municion", "gear"):
                        continue
                    falta = (ro["hand"] in (None, "none") if cl == "arma" else
                             ro["pack_n"].get(mundo.id_botiquin, 0) == 0
                             if cl == "botiquin" else
                             not any(ro["pack_n"].get(i, 0)
                                     for i in (mundo.id_raciones or []))
                             if cl == "raciones" else
                             ro["body"] in (None, "none") if cl == "mochila"
                             else False)
                    if falta and (ro["filas"].get("R-CARENCIA") or 0) > 0:
                        ev2c += 1
        # golpes en amenaza a ciegas (definicion del sello)
        for sl in (a, b):
            otro = b if sl == a else a
            for t, r in D[sl]["T"].items():
                if not r["dano"]:
                    continue
                vistos = {x["slot"] for x in r["ag"]}
                for src, _amt in r["dano"]:
                    s_ = str(src)
                    if not (s_.startswith("P") and s_[1:].isdigit()):
                        continue
                    sl2 = int(s_[1:])
                    if sl2 in NUESTROS or sl2 in vistos:
                        continue
                    lo_vio_el_otro = any(
                        sl2 in {x["slot"] for x in D[otro]["T"][tt]["ag"]}
                        for tt in range(max(0, t - VENTANA_CIEGA), t + 1)
                        if tt in D[otro]["T"])
                    if lo_vio_el_otro:
                        golpes_ciegos[sl] += 1
        for sl in (a, b):
            fin = D[sl]["fin"]
            mt = fin.get("match_ticks")
            S["vidas"].append({
                "semilla": semilla, "slot": sl, "tics": mt,
                "puesto": fin.get("placement"), "razon": fin.get("reason"),
                "golpes_ciegos": golpes_ciegos.get(sl, 0),
                "vivo_al_aviso": bool(mt and mt >= ANILLO_AVISA),
                "vivo_al_cierre": bool(mt and mt >= ANILLO_CIERRA),
                "tics_inyeccion": len(CONT[sl])})
        ma, mb = D[a]["fin"].get("match_ticks"), D[b]["fin"].get("match_ticks")
        pri = a if (ma or 0) <= (mb or 0) else b
        S["por_semilla"][semilla] = {
            "tics": {a: ma, b: mb}, "2c_tics": ev2c,
            "golpes_ciegos": sum(golpes_ciegos.values()),
            "los_dos_al_aviso": bool(ma and mb and min(ma, mb) >= ANILLO_AVISA),
            "los_dos_al_cierre": bool(ma and mb and min(ma, mb) >= ANILLO_CIERRA),
            "primero": pri, "sobrevive_el_otro": abs((ma or 0) - (mb or 0)),
            "tics_inyeccion": len(CONT[a]) + len(CONT[b])}
        # ── discrepancia ─────────────────────────────────────────────────
        for sl in (a, b):
            T = D[sl]["T"]
            listas = [t for t in sorted(T) if T[t]["listas"]]
            for i, t in enumerate(listas[:-1]):
                t2 = listas[i + 1]
                r, r2 = T[t], T[t2]
                cand, el = r["cand"], r["elegido"]
                if not cand or el not in (cand or {}):
                    continue
                c = cand[el]
                if not isinstance(c, dict) or c.get("filas") is None:
                    continue
                gap = (r2["d_ahora"] or 0) - (c["d"] or 0)
                S["disc"].append(abs(gap))
                p8 = float(c["filas"].get("S-8-EXPOSICION") or 0.0)
                r8 = float(r2["filas"].get("S-8-EXPOSICION") or 0.0)
                S["disc_s8"].append(abs(r8 - p8))
                if abs(gap) < 1e-9:
                    continue
                for f3 in ("cuerpo", "recursos", "vinculos"):
                    mix = dict(c["filas"])
                    for k in set(c["filas"]) | set(r2["filas"]):
                        if fam(k) == f3:
                            mix[k] = r2["filas"].get(k, 0.0)
                    ap = d_de(mix) - c["d"]
                    S["fam"][f3] += ap
                    S["fam_abs"][f3] += abs(ap)
        del D
        print(f"    {os.path.basename(carp)}", flush=True)
    return S


def resumen(S):
    V = S["vidas"]
    tics = [v["tics"] for v in V if v["tics"]]
    tot = sum(S["fam_abs"].values()) or 1.0
    return {
        "etiqueta": S["etiqueta"], "vidas": len(V), "episodios": S["c"]["episodios"],
        "vida_media": round(st.mean(tics), 1) if tics else None,
        "vida_mediana": int(st.median(tics)) if tics else None,
        "golpes_ciegos_total": sum(v["golpes_ciegos"] for v in V),
        "golpes_ciegos_por_vida": round(sum(v["golpes_ciegos"] for v in V) / max(1, len(V)), 3),
        "2c_tics_total": sum(x["2c_tics"] for x in S["por_semilla"].values()),
        "2c_tics_por_vida": round(sum(x["2c_tics"] for x in S["por_semilla"].values()) / max(1, len(V)), 1),
        "los_dos_al_aviso": sum(1 for x in S["por_semilla"].values() if x["los_dos_al_aviso"]),
        "los_dos_al_cierre": sum(1 for x in S["por_semilla"].values() if x["los_dos_al_cierre"]),
        "sobrevive_el_otro_mediana": int(st.median([x["sobrevive_el_otro"] for x in S["por_semilla"].values()])) if S["por_semilla"] else None,
        "disc_mediana": round(st.median(S["disc"]), 5) if S["disc"] else None,
        "disc_suma": round(sum(S["disc"]), 1),
        "disc_s8_mediana": round(st.median(S["disc_s8"]), 5) if S["disc_s8"] else None,
        "disc_s8_suma": round(sum(S["disc_s8"]), 1),
        "n_disc": len(S["disc"]),
        "fam_pct": {k: round(100 * v / tot, 1) for k, v in S["fam_abs"].items()},
        "fam_neto": {k: round(v, 1) for k, v in S["fam"].items()},
        "recuento": dict(S["c"]),
    }


if __name__ == "__main__":
    OUT = {}
    for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
        print(f"### {etiq}")
        S = mide(sorted(glob.glob(pat)), etiq)
        OUT[etiq] = {"resumen": resumen(S), "vidas": S["vidas"],
                     "por_semilla": S["por_semilla"]}
        print(json.dumps(OUT[etiq]["resumen"], ensure_ascii=False, indent=1))
    json.dump(OUT, open(os.path.join(AQUI, "P6_4_medidas.json"), "w"),
              ensure_ascii=False, indent=1)
    print("\n-> cantera/paper6/P6_4_medidas.json")

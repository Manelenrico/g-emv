"""[P6-21 · 1] LA REGLA DEL JUEGO, MEDIDA EN LOS HECHOS. SOLO LECTURA de los 200 diarios
del mundo del seis (A3, A4, A5v, A5h, A6), de uno en uno.

    python3 mide_anillo_P6_21.py            -> P6_21_anillo.json  (+ filas por tic en P621_SCRATCH)

Hechos que se recogen por tic vivo desde el primer aviso: casilla, radio que dice la
observacion (`zona.radius`, entero) y `next_radius`, radio interpolado del calendario
(`mundo.anillo_en`, con decimales), golpe del anillo (`damage_taken` con source zone).
El anillo pega una vez cada 24 tics (se mide la cadencia); por eso una estancia de >= 25
tics en la misma casilla sin golpe es una casilla que NO quema con ese radio («estancia
segura»), y cada golpe es una casilla que SI quema.

Reglas candidatas (todas se prueban contra todos los golpes y todas las estancias):
  distancia: euclidea desde la esquina (x, y) al centro (24, 24) [= desde el centro de la
  casilla al (24,5, 24,5)]; desde el centro de la casilla (x+0,5, y+0,5) a (24, 24);
  Chebyshev; Manhattan.
  radio: el de la observacion en el tic, el del tic anterior, el interpolado del calendario
  en t, t-1, t+1, `next_radius`, el r0 de la fase (arranque) y el r1 (final).
  comparacion: quema si d > r; quema si d >= r.
Una regla «encaja» si explica todos los golpes (d ? r cierto) y todas las estancias seguras
(d ? r falso). Se cuentan los fallos de cada una y los casos que no encajan con la mejor.
"""
import collections, glob, json, math, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
C = (24, 24); ESTANCIA = 25
BRAZOS = {"A3": "paintball/runs/P610_t*_A3_*", "A4": "paintball/runs/P611_t*_A4_*", "A5v": "paintball/runs/P616_t1_A5v_*", "A5h": "paintball/runs/P616_t2_A5h_*", "A6": "paintball/runs/P618_t1_A6_*"}
SCR = os.environ.get("P621_SCRATCH") or os.path.join(AQUI, "_P6_21_tmp"); os.makedirs(SCR, exist_ok=True)
DIST = {"esquina->(24,24)": lambda p: math.dist(p, C), "centro casilla->(24,24)": lambda p: math.dist((p[0] + 0.5, p[1] + 0.5), C),
        "Chebyshev": lambda p: max(abs(p[0] - C[0]), abs(p[1] - C[1])), "Manhattan": lambda p: abs(p[0] - C[0]) + abs(p[1] - C[1])}
RADIOS = ["obs(t)", "obs(t-1)", "cal(t)", "cal(t-1)", "cal(t+1)", "next", "r0 fase", "r1 fase"]
CMP = {">": lambda d, r: d > r + 1e-9, ">=": lambda d, r: d > r - 1e-9}


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo"); sm = next(r for r in recs if r["k"] == "static_map")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); fin = next((r for r in recs if r.get("k") == "final"), None)
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        z = r.get("zona") or {}; ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = {"pos": (int(r["pos"][0]), int(r["pos"][1])), "R": z.get("radius"), "Rn": z.get("next_radius"), "hp": float(r.get("hp") if r.get("hp") is not None else 100),
                        "zh": sum(float(g.get("amount") or 0) for g in (r.get("damage_taken") or []) if isinstance(g, dict) and g.get("source") == "zone"),
                        "el": str(ra.get("elegido") or ""), "mri": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0)}
    del recs
    return pc, T, fin, mundo


GOLPES = []; ESTANCIAS = []; CAD = collections.Counter(); n_vidas = 0; FALLOS = {}; EJ = collections.defaultdict(list); INT = collections.Counter()
for brazo, pat in BRAZOS.items():
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1])
        for sl in (10, 11):
            pc, T, fin, mundo = carga(fs[sl]); ts = sorted(T); n_vidas += 1; zs = [tuple(z) for z in pc["zone_schedule"]]; t_warn0 = zs[0][0]
            filas = []; ult_hit = None; est = None
            for i, t in enumerate(ts):
                r = T[t]
                if t < t_warn0:
                    continue
                cal = mundo.anillo_en(t)[1]; cal_m = mundo.anillo_en(t - 1)[1]; cal_p = mundo.anillo_en(t + 1)[1]
                k = None
                for j, z in enumerate(zs):
                    if z[0] <= t:
                        k = j
                r0, r1 = (zs[k][3], zs[k][4]) if k is not None else (48, 48)
                Rm = T[t - 1]["R"] if (t - 1) in T else r["R"]
                rad = {"obs(t)": r["R"], "obs(t-1)": Rm, "cal(t)": cal, "cal(t-1)": cal_m, "cal(t+1)": cal_p, "next": r["Rn"], "r0 fase": r0, "r1 fase": r1}
                if r["R"] is not None:
                    INT[("obs-cal", round(r["R"] - cal, 2))] += 1
                fila = {"t": t, "pos": r["pos"], "rad": rad, "zh": r["zh"], "el": r["el"], "hp": r["hp"], "mri": r["mri"], "fase": (k + 1 if k is not None else 0)}
                filas.append(fila)
                if r["zh"] > 0:
                    GOLPES.append({"brazo": brazo, "sem": sem, "slot": sl, **fila})
                    if ult_hit is not None:
                        CAD[t - ult_hit] += 1
                    ult_hit = t
                # estancias: misma casilla, sin golpe, >= 25 tics (y radio de la observacion constante)
                if est is not None and (r["pos"] != est["pos"] or r["zh"] > 0 or r["R"] != est["rad"]["obs(t)"]):
                    if est["n"] >= ESTANCIA and est["ok"]:
                        ESTANCIAS.append({"brazo": brazo, "sem": sem, "slot": sl, **{k2: est[k2] for k2 in ("t", "pos", "rad", "n", "fase")}})
                    est = None
                if r["zh"] == 0:
                    if est is None:
                        est = {"t": t, "pos": r["pos"], "rad": rad, "n": 1, "fase": fila["fase"], "ok": True}
                    else:
                        est["n"] += 1
                        if r["R"] != est["rad"]["obs(t)"]:
                            est["ok"] = False
                else:
                    est = None
            json.dump({"brazo": brazo, "sem": sem, "slot": sl, "zs": zs, "muerte": (fin or {}).get("reason"), "mt": max(T), "filas": filas}, open(os.path.join(SCR, f"filas_{brazo}_{sem}_{sl}.json"), "w"))
            del T
        print(f"  {brazo} {sem}: golpes {len(GOLPES)} · estancias {len(ESTANCIAS)}", flush=True)

# ── las reglas ──
res = {}
for dn, df in DIST.items():
    for rn in RADIOS:
        for cn, cf in CMP.items():
            fg = [g for g in GOLPES if g["rad"][rn] is None or not cf(df(g["pos"]), g["rad"][rn])]
            fe = [e for e in ESTANCIAS if e["rad"][rn] is not None and cf(df(e["pos"]), e["rad"][rn])]
            res[f"{dn} | {rn} | quema si d {cn} r"] = {"golpes_no_explicados": len(fg), "estancias_seguras_que_quemaria": len(fe), "fallos": len(fg) + len(fe)}
            FALLOS[(dn, rn, cn)] = (fg, fe)
mejor = sorted(res.items(), key=lambda kv: kv[1]["fallos"])[:12]
b = mejor[0][0].split(" | "); fg, fe = FALLOS[(b[0], b[1], b[2].replace("quema si d ", "").replace(" r", ""))]
R = {"nota": "P6-21 §1. INSTRUMENTO DE MEDIDA. Solo lectura de los 200 diarios.", "vidas": n_vidas, "golpes": len(GOLPES), "estancias_seguras_>=25": len(ESTANCIAS),
     "cadencia_entre_golpes": dict(sorted(CAD.items(), key=lambda kv: -kv[1])[:6]), "dano_por_golpe": dict(collections.Counter(round(g["zh"], 2) for g in GOLPES).most_common(6)),
     "obs_menos_cal (radio observado - interpolado, redondeado a 0,01)": dict(sorted(((str(k[1]), v) for k, v in INT.items()), key=lambda kv: -kv[1])[:12]),
     "reglas (mejores 12)": dict(mejor), "todas": res,
     "mejor": {"regla": mejor[0][0], "golpes_no_explicados": [{k: g[k] for k in ("brazo", "sem", "slot", "t", "pos", "zh", "fase")} | {"d": round(DIST[b[0]](g["pos"]), 3), "r": g["rad"][b[1]], "obs": g["rad"]["obs(t)"], "cal": round(g["rad"]["cal(t)"], 3)} for g in fg[:40]],
               "estancias_que_quemaria": [{k: e[k] for k in ("brazo", "sem", "slot", "t", "pos", "n", "fase")} | {"d": round(DIST[b[0]](e["pos"]), 3), "r": e["rad"][b[1]]} for e in fe[:40]]},
     "golpes_por_d_menos_obs": dict(collections.Counter(round(math.dist(g["pos"], C) - (g["rad"]["obs(t)"] or 0), 2) for g in GOLPES).most_common(20)),
     "estancias_por_d_menos_obs": dict(collections.Counter(round(math.dist(e["pos"], C) - (e["rad"]["obs(t)"] or 0), 2) for e in ESTANCIAS).most_common(20))}
json.dump(R, open(os.path.join(AQUI, "P6_21_anillo.json"), "w"), ensure_ascii=False, indent=1, default=str)
print("vidas", n_vidas, "golpes", len(GOLPES), "estancias", len(ESTANCIAS), "cadencia", R["cadencia_entre_golpes"], "dano", R["dano_por_golpe"])
print("obs - cal:", R["obs_menos_cal (radio observado - interpolado, redondeado a 0,01)"])
for k, v in mejor:
    print("  ", k, v)
print("golpes por d-obs:", R["golpes_por_d_menos_obs"]); print("estancias por d-obs:", R["estancias_por_d_menos_obs"])
print("-> P6_21_anillo.json")

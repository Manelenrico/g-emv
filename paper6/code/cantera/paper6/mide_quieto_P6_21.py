"""[P6-21 · 3, apoyo] MOVIMIENTOS ACEPTADOS QUE NO MUEVEN. SOLO LECTURA de los 120 diarios
de A4, A5h y A6 (60 partidas), de uno en uno.

En P6-20 y en la traza de P6-21 el cuerpo «obedece ir» en la casilla del borde tic tras
tic, con `move_ready_in` 0 y `action_result` ok, y no se mueve. Aqui se cuenta, por tic
con `intencion` move y piernas listas (`move_ready_in` 0): si el cuerpo aparece en la
casilla destino en los 3 tics siguientes (mueve) o no (no mueve); por brazo, por fase
(antes / desde el aviso 5), por direccion (recta / diagonal), por lo que hay en la casilla
destino (solida del mapa; ocupada por un cuerpo visto —hermano o rival— en ese tic; libre),
y por si el cuerpo estaba ardiendo (regla del juego de §1: d > radio observado) o creia
estar a salvo (regla del cuerpo: d <= radio interpolado de `mundo.anillo_en`).
"""
import collections, glob, json, math, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
C = (24, 24)
BRAZOS = {"A4": "paintball/runs/P611_t*_A4_*", "A5h": "paintball/runs/P616_t2_A5h_*", "A6": "paintball/runs/P618_t1_A6_*"}
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo"); sm = next(r for r in recs if r["k"] == "static_map")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        T[r["tick"]] = {"pos": (int(r["pos"][0]), int(r["pos"][1])), "int": r.get("intencion") or {}, "mri": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0), "ar": r.get("action_result_obs", r.get("action_result")),
                        "R": (r.get("zona") or {}).get("radius"), "ve": {tuple(a["pos"]): a.get("slot") for a in (r.get("ve_agentes") or []) if a.get("pos")}, "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""), "zh": any(g.get("source") == "zone" for g in (r.get("damage_taken") or []) if isinstance(g, dict))}
    del recs
    return pc, T, mundo


K = collections.defaultdict(lambda: [0, 0]); CASOS = []; RACHAS = []; DEST = collections.Counter(); DESTOK = collections.Counter()
for brazo, pat in BRAZOS.items():
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        sem = int(carp.rsplit("_", 1)[1])
        for sl in (10, 11):
            pc, T, mundo = carga(fs[sl]); warn5 = pc["zone_schedule"][4][0]; herm = pc["teammate_slot"]; racha = 0; r0 = None
            for t in sorted(T):
                r = T[t]
                if r["int"].get("do") != "move" or r["mri"] != 0 or r["int"].get("dir") not in DIRS:
                    if racha >= 10:
                        RACHAS.append({"brazo": brazo, "sem": sem, "slot": sl, "t0": r0, "n": racha, "pos": T[r0]["pos"], "fase5": r0 >= warn5, "ardia": (math.dist(T[r0]["pos"], C) > (T[r0]["R"] or 48)), "el": T[r0]["el"]})
                    racha = 0; continue
                dx, dy = DIRS[r["int"]["dir"]]; dest = (r["pos"][0] + dx, r["pos"][1] + dy)
                mueve = any(T.get(t + k, {}).get("pos") == dest for k in (1, 2, 3))
                que = "solida" if mundo.solido(dest[0], dest[1]) else ("hermano" if r["ve"].get(dest) == herm else ("rival visto" if dest in r["ve"] else "libre"))
                diag = "diagonal" if (dx and dy) else "recta"
                d = math.dist(r["pos"], C); arde = r["R"] is not None and d > r["R"]; cree_salvo = d <= mundo.anillo_en(t)[1]
                fase = "fase5+" if t >= warn5 else "fases1-4"
                i = 0 if mueve else 1
                pi = (T.get(t - 1) or {}).get("int") or {}
                misma = "misma dir que t-1" if (pi.get("do") == "move" and pi.get("dir") == r["int"]["dir"]) else "dir nueva"
                (DESTOK if mueve else DEST)[(brazo, fase, dest)] += 1
                for key in ((brazo, fase), (brazo, fase, diag), (brazo, fase, que), (brazo, fase, "arde" if arde else "no arde"), (brazo, fase, "ar=" + str(r["ar"])), (brazo, fase, que, diag), (brazo, fase, misma)):
                    K[key][i] += 1
                if not mueve:
                    racha = racha + 1 if racha else 1
                    if racha == 1:
                        r0 = t
                    if arde and cree_salvo:
                        K[(brazo, fase, "no mueve, arde y cree salvo")][1] += 1
                else:
                    if racha >= 10:
                        RACHAS.append({"brazo": brazo, "sem": sem, "slot": sl, "t0": r0, "n": racha, "pos": T[r0]["pos"], "fase5": r0 >= warn5, "ardia": (math.dist(T[r0]["pos"], C) > (T[r0]["R"] or 48)), "el": T[r0]["el"]})
                    racha = 0
            del T
        print(f"  {brazo} {sem}", flush=True)
TOP = {}
for (b, fa, dest), n in DEST.most_common(60):
    TOP[f"{b} | {fa} | {dest}"] = [DESTOK.get((b, fa, dest), 0), n]
R = {"casillas_destino_que_mas_fallan [mueve, no mueve]": TOP, "nota": "P6-21 §3 apoyo. movimientos aceptados (move_ready_in 0) que no mueven. [mueve, no mueve]", "cuentas": {" | ".join(k): v for k, v in sorted(K.items())},
     "rachas_>=10_sin_moverse": {"n": len(RACHAS), "por_brazo_fase5": {f"{b} fase5={f}": n for (b, f), n in collections.Counter((x["brazo"], x["fase5"]) for x in RACHAS).items()}, "ardiendo": sum(1 for x in RACHAS if x["ardia"]), "tics": sum(x["n"] for x in RACHAS), "mediana": (sorted(x["n"] for x in RACHAS)[len(RACHAS) // 2] if RACHAS else None), "lista": RACHAS[:200]}}
json.dump(R, open(os.path.join(AQUI, "P6_21_quieto.json"), "w"), ensure_ascii=False, indent=1, default=str)
for k, v in sorted(K.items()):
    print("  ", " | ".join(k), v, f"({round(100 * v[1] / max(1, sum(v)), 1)} % no mueve)")
print("rachas:", {k: v for k, v in R["rachas_>=10_sin_moverse"].items() if k != "lista"})
print("-> P6_21_quieto.json")

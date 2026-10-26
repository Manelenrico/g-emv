"""[P7-3] Repeticion de decisiones con la CREENCIA DEL TECHO (sello T1-T2): sin municion = 0 exacto; con municion y botiquin = la media
real del diario (P7_1_diario.json) en su situacion y asiento. Misma replica y mismo gancho que banco_P7_2.py (importado), un proceso
por vida. Escribe P7_3_techo.json y P7_3_banco_techo.json.    python3 banco_P7_3.py [--hilos 4]"""
import collections, json, os, statistics, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
import banco_P7_2 as BK
J = json.load(open(os.path.join(AQUI, "P7_1_diario.json")))
def sit_bot(f): return "dentro" if f["situacion"]["dentro"] else "fuera"
def sit_arc(f): return "con municion" if f["situacion"]["municion_mochila"] > 0 else "sin municion"
if __name__ == "__main__":
    a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4
    vals = collections.defaultdict(list)
    for f in J["botiquin"]:
        if f["paso"]["resultado"] == "sin cerrar": continue
        vals[("botiquin", sit_bot(f), int(f["vida"].split("/")[1]))].append(f["paso"]["cura_real"] if f["paso"]["resultado"] == "completado" else 0.0)
    for f in J["arco_cerbatana"]:
        vals[(f["arma"], sit_arc(f), int(f["vida"].split("/")[1]))].append(f["paso"]["dano_hecho"] if f["paso"]["resultado"] == "ok" else 0.0)
    techo = {f"{k[0]}/{k[1]}/{k[2]}": (0.0 if k[1] == "sin municion" else round(statistics.mean(v), 4)) for k, v in vals.items()}
    json.dump({"techo": techo, "n": {f"{k[0]}/{k[1]}/{k[2]}": len(v) for k, v in vals.items()}}, open(os.path.join(AQUI, "P7_3_techo.json"), "w"), indent=1)
    print("techo:", techo)
    T = json.load(open(os.path.join(AQUI, "P7_2_creencias.json")))   # mismos tics y dias; solo cambia b_antes
    for e in T: e["b_antes"] = techo[f"{e['objeto']}/{e['situacion']}/{e['asiento']}"]
    por = collections.defaultdict(list)
    for e in T: por[(e["carpeta"], e["asiento"])].append(e)
    tareas = [(c, s, sorted(v, key=lambda e: e["t"])) for (c, s), v in sorted(por.items())]
    print(f"### P7-3 banco techo: {len(tareas)} vidas · {sum(len(t[2]) for t in tareas)} decisiones · hilos {hilos}", flush=True)
    import multiprocessing as mp
    with mp.get_context("fork").Pool(hilos, maxtasksperchild=1) as pool: res = pool.map(BK._mp, tareas, chunksize=1)
    dec = [d for r in res for d in r["decisiones"]]
    print("decisiones:", len(dec), "fieles:", sum(1 for d in dec if d["fiel"]), "cambian:", sum(1 for d in dec if d["cambia"]))
    json.dump({"vidas": res}, open(os.path.join(AQUI, "P7_3_banco_techo.json"), "w"), indent=0, ensure_ascii=False)

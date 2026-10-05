"""[P6-30] La infidelidad residual, vida a vida: replica (un proceso por vida) las vidas con desacuerdos de P6_29_vidas.json y clasifica
cada desacuerdo: (a) el cuerpo en el campo eligio el candidato del plan (`elegido_cuerpo` empieza por `_FM`), con las d de los
candidatos propios iguales en diario y replica; (b) otra cosa. -> residuo_todo_P6_30.json"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
def una(args):
    carp, slot, brazo = args; sys.argv = ["x"]
    import mide_P6_29 as M, serie_util as U
    r = M.vida(carp, slot, brazo); R = M.HOOK["reg"]; D = set(r["desacuerdos"]); out = []
    f = glob.glob(os.path.join(M.RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]
    for rec in U.lee(f):
        if rec.get("k") == "tick" and rec["tick"] in D:
            ra = rec.get("RADIOGRAFIA") or {}; cds = {k: (x["d"] if isinstance(x, dict) else x) for k, x in (ra.get("candidatos") or {}).items()}; rp = (R.get(rec["tick"]) or {}).get("cds") or {}
            comunes = set(cds) & set(rp); iguales = all(abs(float(cds[k]) - float(rp[k])) < 1e-6 for k in comunes)
            out.append({"t": rec["tick"], "cuerpo": ra.get("elegido_cuerpo"), "replica": (R.get(rec["tick"]) or {}).get("el"), "cuerpo_es_FM": str(ra.get("elegido_cuerpo") or "").startswith("_FM"),
                        "d_propias_iguales": iguales, "solo_diario": sorted(set(cds) - set(rp)), "solo_replica": sorted(set(rp) - set(cds))})
    return {"vida": f"{carp}/{slot}", "brazo": brazo, "fidelidad": r["fidelidad"], "desacuerdos": out}
if __name__ == "__main__":
    import multiprocessing as mp
    V = json.load(open(os.path.join(AQUI, "P6_29_vidas.json"))); tareas = [(v["carp"], v["slot"], v["brazo"]) for v in V if (v.get("fidelidad") or {}).get("difiere")]
    print("vidas con desacuerdos:", len(tareas), flush=True)
    with mp.get_context("spawn").Pool(4, maxtasksperchild=1) as pool: res = pool.map(una, tareas, chunksize=1)
    D = [d for r in res for d in r["desacuerdos"]]
    cls = collections.Counter((d["brazo"] if "brazo" in d else None) for d in D)
    res_cls = collections.Counter((r["brazo"], d["cuerpo_es_FM"], d["d_propias_iguales"], bool(d["solo_replica"])) for r in res for d in r["desacuerdos"])
    print("desacuerdos:", len(D), "| (brazo, cuerpo eligio _FM, d propias iguales, hay candidatos solo en la replica):", res_cls.most_common())
    json.dump({"vidas": res, "clases": [[list(k), v] for k, v in res_cls.items()]}, open(os.path.join(AQUI, "residuo_todo_P6_30.json"), "w"), ensure_ascii=False, indent=1)

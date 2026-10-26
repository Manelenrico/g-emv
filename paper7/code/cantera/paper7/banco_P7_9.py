"""[P7-9] F2: en banco, sobre los seis diarios del freno de P7-8 (P78_s1_d{1,2,3}_APRENDE, asientos 10 y 11), replica APRENDE con el cuaderno
VACIO (el botiquin desconocido) dos veces: sin esperanza (GEMV_P7_ESPERANZA=0, lo de antes) y con ella. En cada tic con un botiquin en el
zurron y la vida por debajo de 50, o por encima de 80: lo que elige la replica, las d (usar_botiquin y la mejor), y la cura imaginada. Un
subproceso por vida (molde de banco_P7_5). -> P7_9_F2.json"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import banco_P7_5 as B
def escenas(carp, slot):
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]; out = {}
    for line in open(f):
        if '"k":"tick"' not in line[:12]: continue
        r = json.loads(line)
        if r.get("phase") != "live": continue
        if not any((s_ or {}).get("id") == "first_aid" for s_ in (r.get("pack") or [])): continue
        hp = float(r.get("hp") or 0); canal = any(e.get("id") == "channeling" for e in (r.get("effects") or []))
        if hp < 50 or hp > 80: out[r["tick"]] = {"hp": hp, "banda": "baja" if hp < 50 else "alta", "canal": canal, "elegido_campo": (r.get("RADIOGRAFIA") or {}).get("elegido")}
    return out
if __name__ == "__main__":
    sal = os.path.join(AQUI, "_P7_9_tmp", "F2"); os.makedirs(sal, exist_ok=True); R = {"vidas": [], "resumen": {}}
    carps = sorted(os.path.basename(c) for c in glob.glob(os.path.join(RAIZ, "paintball", "runs", "P78_s1_d*_APRENDE_*")))
    for carp in carps:
        for slot in (10, 11):
            E = escenas(carp, slot)
            if not E: R["vidas"].append({"vida": f"{carp}/{slot}", "escenas": 0}); continue
            tf = os.path.join(sal, f"ticks_{carp}_{slot}.json"); json.dump(sorted(E), open(tf, "w")); os.environ["P7_REGISTRA_TICKS"] = tf
            fila = {"vida": f"{carp}/{slot}", "escenas": len(E), "bandas": dict(collections.Counter(e["banda"] for e in E.values())), "brazos": {}}
            for nombre, esp in (("antes", "0"), ("esperanza", "1")):
                os.environ["GEMV_P7_ESPERANZA"] = esp
                cuad = os.path.join(sal, f"cuad_{nombre}_{carp}_{slot}"); os.makedirs(cuad, exist_ok=True)
                for f_ in glob.glob(os.path.join(cuad, "*.json")): os.remove(f_)
                r = B.lanza_vida(carp, slot, "APRENDE", cuad, os.path.join(sal, f"{nombre}_{carp}_{slot}.json"))
                if r.get("error"): print("ERROR", nombre, carp, slot, r["error"][-300:]); continue
                res = {"baja": collections.Counter(), "alta": collections.Counter(), "heal": {"baja": [], "alta": []}, "d": {"baja": [], "alta": []}, "ejemplos": []}
                for u in r["usos"]:
                    e = E.get(u["t"])
                    if e is None or e["canal"]: continue                      # con el canal abierto no hay que decidir usar
                    b = e["banda"]; el = u.get("elegido_replica"); d = u.get("d") or {}
                    res[b][("usar_botiquin" if el == "usar_botiquin" else "otra")] += 1
                    if u.get("heal") is not None: res["heal"][b].append(u["heal"])
                    if "usar_botiquin" in d: res["d"][b].append((round(d["usar_botiquin"] - min(d.values()), 4)))
                    if len(res["ejemplos"]) < 3 and b == "baja": res["ejemplos"].append({"t": u["t"], "hp": e["hp"], "elegido": el, "heal": u.get("heal"), "k": u.get("k"), "d_mejor": sorted(d.items(), key=lambda kv: kv[1])[:4]})
                med = lambda xs: (sorted(xs)[len(xs) // 2] if xs else None)
                fila["brazos"][nombre] = {"baja": dict(res["baja"]), "alta": dict(res["alta"]), "heal_mediana": {b: med(res["heal"][b]) for b in ("baja", "alta")}, "d_usar_menos_mejor_mediana": {b: med(res["d"][b]) for b in ("baja", "alta")}, "ejemplos": res["ejemplos"], "huellas": len(r["huellas"]), "fidelidad": r["fidelidad"]}
            R["vidas"].append(fila); print(json.dumps({k: v for k, v in fila.items()}, ensure_ascii=False)[:900], flush=True)
    tot = {n_: {b: collections.Counter() for b in ("baja", "alta")} for n_ in ("antes", "esperanza")}
    for v in R["vidas"]:
        for n_, br in (v.get("brazos") or {}).items():
            for b in ("baja", "alta"): tot[n_][b].update(br[b])
    R["resumen"] = {n_: {b: dict(tot[n_][b]) for b in ("baja", "alta")} for n_ in tot}
    json.dump(R, open(os.path.join(AQUI, "P7_9_F2.json"), "w"), ensure_ascii=False, indent=1); print("resumen:", json.dumps(R["resumen"]))

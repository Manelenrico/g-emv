"""[P7-11] EL DIA 1: ¿APRENDE Y BORRADO DECIDEN IGUAL? Los mundos de las dos partidas divergen desde el segundo tic (P7_11_dia1.json), asi que
los diarios no se pueden comparar tic a tic. Se replican (molde de `banco_P7_5.py`, UN SUBPROCESO POR VIDA, sin partidas ni llamadas) los 8
diarios del dia 1 de APRENDE y BORRADO (2 series x 2 asientos) dos veces cada uno: con los interruptores de APRENDE y con los de BORRADO, con
una carpeta de cuadernos vacia. Si las dos replicas del mismo diario eligen lo mismo en todos los tics y acaban con el mismo cuaderno, los dos
brazos son el mismo cuerpo el dia 1. La replica usa `descubre_P7.py` de hoy (md5 en el informe). -> P7_11_banco_dia1.json"""
import glob, json, os, sys
from concurrent.futures import ThreadPoolExecutor
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import banco_P7_5 as B
if __name__ == "__main__":
    sal = os.path.join(AQUI, "_P7_11_tmp"); vacio = os.path.join(sal, "cuadernos_vacios"); os.makedirs(vacio, exist_ok=True)
    tareas = [(os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P710_s{s}_d1_{b}_*"))[0]), sl, como) for s in (1, 2) for b in ("APRENDE", "BORRADO") for sl in (10, 11) for como in ("APRENDE", "BORRADO")]
    def una(t):
        carp, sl, como = t; d = os.path.join(sal, f"cuad_{carp}_{sl}_{como}"); os.makedirs(d, exist_ok=True)   # cada replica escribe su cuaderno en su carpeta (vacia al empezar)
        for f in glob.glob(os.path.join(d, "*.json")): os.remove(f)
        return t, B.lanza_vida(carp, sl, como, d, os.path.join(sal, f"replica_{carp}_{sl}_{como}.json"))
    with ThreadPoolExecutor(8) as ex: R = dict(ex.map(una, tareas))
    OUT = []
    for carp, sl in sorted({(c, s) for c, s, _ in tareas}):
        a, b = R[(carp, sl, "APRENDE")], R[(carp, sl, "BORRADO")]
        if a.get("error") or b.get("error"): OUT.append({"vida": f"{carp}/{sl}", "error": (a.get("error") or b.get("error"))[-400:]}); continue
        da = {d["t"]: d["replica"] for d in a["desacuerdos"]}; db = {d["t"]: d["replica"] for d in b["desacuerdos"]}
        OUT.append({"vida": f"{carp}/{sl}", "tics": a["tics"], "fidelidad_como_APRENDE": a["fidelidad"], "fidelidad_como_BORRADO": b["fidelidad"],
                    "tics_en_que_las_dos_replicas_eligen_distinto": sorted(t for t in set(da) | set(db) if da.get(t) != db.get(t)),
                    "cuaderno_fin_igual": a["cuaderno_fin"] == b["cuaderno_fin"], "huellas": [len(a["huellas"]), len(b["huellas"])], "errores": [len(a["errores"]), len(b["errores"])],
                    "desacuerdos_con_el_diario_como_APRENDE": a["desacuerdos"][:8]})
        print(json.dumps(OUT[-1], ensure_ascii=False)[:600], flush=True)
    json.dump(OUT, open(os.path.join(AQUI, "P7_11_banco_dia1.json"), "w"), ensure_ascii=False, indent=1)

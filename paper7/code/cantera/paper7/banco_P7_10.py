"""[P7-10] EL BANCO DEL ARREGLO "en un empate, hacer sitio no gana": replica de los diarios del freno de P7-9 (P79_s1_d1 y d2, asiento 10:
4 y 7 oscilaciones racion <-> botiquin en el campo), brazo APRENDE con el cuaderno que esa criatura leyo ese dia (el de fin del dia anterior;
vacio el dia 1), dos veces: sin el arreglo (GEMV_P7_SITIO_EMPATE=0) y con el. En los tics donde el campo eligio hacer sitio (P7_sitio) y en
todos los tics con un hacer-sitio entre los candidatos: lo que elige la replica, y las oscilaciones (A por B seguido en <= 5 tics de B por A).
Un subproceso por vida. -> P7_10_sitio.json"""
import collections, glob, json, os, shutil, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import banco_P7_5 as B
def campo(carp, slot):
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]; el = {}; sitios = []
    for line in open(f):
        if '"k":"tick"' in line[:12]:
            r = json.loads(line)
            if r.get("phase") == "live": el[r["tick"]] = (r.get("RADIOGRAFIA") or {}).get("elegido")
        elif '"P7_sitio"' in line[:30]: sitios.append(json.loads(line))
    return el, sitios
def oscilaciones(seq):
    n = 0
    for (ta, ea), (tb, eb) in zip(seq, seq[1:]):
        a = ea.replace("hacer_sitio_", "").split("_por_"); b = eb.replace("hacer_sitio_", "").split("_por_")
        if tb - ta <= 5 and a[0] == b[1] and a[1] == b[0]: n += 1
    return n
if __name__ == "__main__":
    sal = os.path.join(AQUI, "_P7_10_tmp", "sitio"); os.makedirs(sal, exist_ok=True); R = {"vidas": []}
    for dia in (1, 2):
        carp = os.path.basename(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P79_s1_d{dia}_APRENDE_*"))[0]); slot = 10
        EL, S = campo(carp, slot); t_sitio = sorted(s["tick"] for s in S)
        tf = os.path.join(sal, f"ticks_d{dia}.json"); json.dump(t_sitio, open(tf, "w")); os.environ["P7_REGISTRA_TICKS"] = tf
        fila = {"dia": dia, "vida": f"{carp}/{slot}", "campo": {"hacer_sitio": len(t_sitio), "oscilaciones": oscilaciones([(s["tick"], s["elegido"]) for s in S])}, "brazos": {}}
        for nombre, v in (("antes", "0"), ("arreglo", "1")):
            os.environ["GEMV_P7_SITIO_EMPATE"] = v
            cuad = os.path.join(sal, f"cuad_{nombre}_d{dia}"); shutil.rmtree(cuad, ignore_errors=True); os.makedirs(cuad)
            if dia > 1: shutil.copy(os.path.join(AQUI, "P7_9_res", f"cuaderno_s1_d{dia - 1}_APRENDE_{slot}.json"), os.path.join(cuad, f"cuaderno_P7_{slot}.json"))
            r = B.lanza_vida(carp, slot, "APRENDE", cuad, os.path.join(sal, f"{nombre}_d{dia}.json"))
            if r.get("error"): print("ERROR", nombre, dia, r["error"][-300:]); continue
            des = {d["t"]: d["replica"] for d in r["desacuerdos"]}
            rep = lambda t: des.get(t, EL.get(t))
            el_sitio = [(t, rep(t)) for t in t_sitio]
            # todos los tics en que la replica eligio hacer sitio (acuerdos con el campo + desacuerdos hacia hacer sitio)
            todos = sorted([(t, e) for t, e in EL.items() if str(e).startswith("hacer_sitio_") and t not in des] + [(t, e) for t, e in des.items() if str(e).startswith("hacer_sitio_")])
            fila["brazos"][nombre] = {"en_los_tics_del_campo": dict(collections.Counter(("hacer sitio" if str(e).startswith("hacer_sitio_") else str(e)) for _, e in el_sitio)),
                                      "hacer_sitio_replica_total": len(todos), "oscilaciones_replica": oscilaciones(todos), "fidelidad": r["fidelidad"],
                                      "d_en_los_tics_del_campo": [{"t": u["t"], "elegido": u.get("elegido_replica"), "d": sorted((u.get("d") or {}).items(), key=lambda kv: kv[1])[:3]} for u in r["usos"] if u["t"] in t_sitio][:6]}
        R["vidas"].append(fila); print(json.dumps(fila, ensure_ascii=False)[:1500], flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_10_sitio.json"), "w"), ensure_ascii=False, indent=1)

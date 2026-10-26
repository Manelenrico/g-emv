"""[P7-8] EL BANCO DEL ARREGLO "el regalo mira lo aprendido": replica del dia 1 del humo de P7-7 (P77_humo_APRENDE_27173030, asientos 10 y 11,
brazo APRENDE, cuaderno vacio, un subproceso por vida, molde de banco_P7_5) y cuenta de los `soltar_first_aid` que elige la replica, con la
creencia que tenia en ese tic ("no se" hasta la primera huella apuntada). En el campo el asiento 10 regalo 30 de sus 33 cogidas y el 11, 8 de 8.
-> P7_8_regalo.json"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import banco_P7_5 as B
CARP = "P77_humo_APRENDE_27173030"
def campo(slot):
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", CARP, f"*policy_agent_{slot}.art.log"))[0]; el = {}
    for line in open(f):
        if '"k":"tick"' not in line[:12]: continue
        r = json.loads(line)
        if r.get("phase") == "live": el[r["tick"]] = (r.get("RADIOGRAFIA") or {}).get("elegido")
    return el
if __name__ == "__main__":
    sal = os.path.join(AQUI, "_P7_8_tmp", "regalo"); os.makedirs(sal, exist_ok=True); R = {"vidas": []}
    for slot in (10, 11):
        EL = campo(slot); regalos_campo = sorted(t for t, e in EL.items() if e == "soltar_first_aid")
        tf = os.path.join(sal, f"ticks_{slot}.json"); json.dump(regalos_campo, open(tf, "w")); os.environ["P7_REGISTRA_TICKS"] = tf
        cuad = os.path.join(sal, f"cuad_{slot}"); os.makedirs(cuad, exist_ok=True)
        r = B.lanza_vida(CARP, slot, "APRENDE", cuad, os.path.join(sal, f"APRENDE_{slot}.json"))
        if r.get("error"): print("ERROR", slot, r["error"][-400:]); continue
        des = {d["t"]: d for d in r["desacuerdos"]}
        replica_regala = sorted([t for t in regalos_campo if t not in des] + [t for t, d in des.items() if d["replica"] == "soltar_first_aid"])
        replica_coge = sorted([t for t, e in EL.items() if e == "coger" and t not in des] + [t for t, d in des.items() if d["replica"] == "coger"])
        # la creencia en cada tic: "no se" hasta la primera huella apuntada (t_fin), luego la creencia_despues de la ultima huella
        hu = sorted([h for h in r["huellas"] if h.get("apuntado")], key=lambda h: h["t_fin"])
        def creencia_en(t):
            c = None
            for h in hu:
                if h["t_fin"] <= t: c = (h.get("creencia_despues") or {}).get("cuerpo")
            return c
        U = {u["t"]: u for u in r["usos"]}
        reg = [{"t": t, "creencia_cuerpo": creencia_en(t), "campo_tambien": t in regalos_campo, "k": (U.get(t) or {}).get("k"), "d_mejor": (sorted(((U[t].get("d") or {}).items()), key=lambda kv: kv[1])[:4] if t in U else None)} for t in replica_regala]
        v = {"vida": f"{CARP}/{slot}", "tics": r["tics"], "fidelidad": r["fidelidad"], "regalos_campo": len(regalos_campo), "regalos_replica": len(replica_regala), "regalos_replica_con_no_se": sum(1 for x in reg if x["creencia_cuerpo"] is None),
             "regalos_replica_con_creencia": [x for x in reg if x["creencia_cuerpo"] is not None][:10], "cogidas_campo": sum(1 for e in EL.values() if e == "coger"), "cogidas_replica": len(replica_coge),
             "en_los_tics_de_regalo_del_campo": dict(collections.Counter((des[t]["replica"] if t in des else "soltar_first_aid") for t in regalos_campo)), "d_en_un_tic_de_regalo_del_campo": next(({"t": u["t"], "k": u.get("k"), "d": sorted((u.get("d") or {}).items(), key=lambda kv: kv[1])[:5]} for u in r["usos"] if u.get("d")), None),
             "huellas": [{"t0": h["t0"], "hp0": h["hp0"], "hp_fin": h["hp_fin"], "al_menos": h.get("al_menos"), "interrumpido": h.get("interrumpido"), "apuntado": h.get("apuntado"), "efecto": h["efecto"]} for h in r["huellas"]], "cuaderno_fin": (r.get("cuaderno_fin") or {}).get("creencias"), "errores": r.get("errores")}
        R["vidas"].append(v); print(json.dumps({k: x for k, x in v.items() if k not in ("regalos_replica_con_creencia",)}, ensure_ascii=False)[:1200], flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_8_regalo.json"), "w"), ensure_ascii=False, indent=1)

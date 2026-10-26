"""[P7-34] EL FRENO: los dias 1 a 3 de APRENDE, serie 1 (6 vidas, paintball/runs/P734_s1_d{1,2,3}_APRENDE_*). Se sigue si:
  (a) el cuaderno viaja y se lee: registro `P7_cuaderno` de arranque con `leido` verdadero los dias 2 y 3, y los recuerdos con los que arranca son los que cerro el dia anterior;
  (b) en al menos 4 de las 6 vidas la criatura toca alguna de las cuatro cosas (botiquin, racion, red o camuflaje: entra en el zurron, la mano o el cuerpo);
  (c) en al menos una criatura sube la creencia de alguna cosa util (botiquin dentro del circulo, racion la mayor de sus situaciones) entre el cierre de un dia y el siguiente;
  (d) ningun error de fotos (registros `P7_error` "fotos para candidatos": cero en las 6 vidas).
  Ademas se imprime la guarda de latencia de cada vida (marca, no freno: regla de la mesa de P7-30).
  python3 freno_P7_34.py -> P7_34_freno.json"""
import glob, json, os
import analiza_P7_33 as A33
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))


def arranque_y_fin(f):
    arr = fin = None; errores = 0
    for line in open(f, errors="replace"):
        if '"P7_cuaderno"' in line:
            r = json.loads(line)
            if r.get("momento") == "arranque": arr = r
            elif r.get("momento") == "fin": fin = r
        elif '"P7_error"' in line and "fotos para" in line: errores += 1
    return arr, fin, errores


def n_recuerdos(cont): return sum(len(s) for o in ((cont or {}).get("objetos") or {}).values() for s in (o.get("situaciones") or {}).values())
def creencia_util(cont, obj):
    c = ((cont or {}).get("creencias") or {}).get(obj) or {}
    if obj == "first_aid": return (c.get("dentro") or {}).get("cuerpo")
    vals = [x.get("cuerpo") for k, x in c.items() if isinstance(x, dict) and x.get("cuerpo") is not None]
    return max(vals) if vals else None


if __name__ == "__main__":
    V = {}
    for d in (1, 2, 3):
        carp = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P734_s1_d{d}_APRENDE_*")))
        for sl in (10, 11):
            v = A33.una(carp[0], d, sl) if carp else {"sin_diario": True}
            if v.get("sin_diario"): V[(d, sl)] = v; continue
            f = glob.glob(os.path.join(carp[0], f"*policy_agent_{sl}.art.log"))[0]; arr, fin, err = arranque_y_fin(f)
            v["recuerdos_al_arrancar"] = n_recuerdos((arr or {}).get("contenido")); v["recuerdos_al_cerrar"] = n_recuerdos((fin or {}).get("contenido"))
            v["creencia_util_fin"] = {"botiquin": creencia_util((fin or {}).get("contenido"), "first_aid"), "racion": creencia_util((fin or {}).get("contenido"), "rations")}
            v["errores_fotos"] = err; V[(d, sl)] = v
    a = all(not V[(d, sl)].get("sin_diario") and V[(d, sl)]["cuaderno_leido"] and V[(d, sl)]["recuerdos_al_arrancar"] == V[(d - 1, sl)].get("recuerdos_al_cerrar") for d in (2, 3) for sl in (10, 11))
    toca = [(d, sl) for (d, sl), v in V.items() if not v.get("sin_diario") and v["orden_de_contacto"]]
    sube = []
    for sl in (10, 11):
        for d in (2, 3):
            for o in ("botiquin", "racion"):
                if V[(d, sl)].get("sin_diario") or V[(d - 1, sl)].get("sin_diario"): continue
                antes = V[(d - 1, sl)]["creencia_util_fin"][o]; desp = V[(d, sl)]["creencia_util_fin"][o]
                if desp is not None and (antes is None or desp > antes): sube.append((d, sl, o, antes, desp))
    errores = {f"d{d} a{sl}": v.get("errores_fotos") for (d, sl), v in V.items()}
    R = {"vidas": {f"d{d}_a{sl}": v for (d, sl), v in V.items()}, "a_cuaderno_viaja": a, "b_tocan": [f"d{d} a{sl}" for d, sl in toca], "b_pasa": len(toca) >= 4,
         "c_sube": [f"d{d} a{sl} {o}: {an} -> {de}" for d, sl, o, an, de in sube], "c_pasa": bool(sube), "d_errores_fotos": errores, "d_pasa": all(e == 0 for e in errores.values()),
         "guarda": {f"d{d} a{sl}": ({k: v["latencia"][k] for k in ("ms_mediana", "sobre_el_tic", "fraccion_sin_cuerpo", "pasa", "para", "motivo") if k in v["latencia"]} if not v.get("sin_diario") else None) for (d, sl), v in V.items()}}
    R["FRENO"] = "PASA" if (R["a_cuaderno_viaja"] and R["b_pasa"] and R["c_pasa"] and R["d_pasa"]) else "NO PASA"
    json.dump(R, open(os.path.join(AQUI, "P7_34_freno.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in R.items() if k != "vidas"}, ensure_ascii=False, indent=1))
    for k, v in R["vidas"].items():
        if v.get("sin_diario"): print(k, "sin diario"); continue
        print(k, "puesto", v["puesto"], "leido", v["cuaderno_leido"], "recuerdos", v["recuerdos_al_arrancar"], "->", v["recuerdos_al_cerrar"], "orden", v["orden_de_contacto"], "creencia util", v["creencia_util_fin"], "errores fotos", v["errores_fotos"])

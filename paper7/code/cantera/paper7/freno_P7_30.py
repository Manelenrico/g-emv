"""[P7-30, paso 1] EL HUMO COMO FRENO: sobre las 6 vidas del humo de P7-29/29b (APRENDE, serie 1, dias 1-3, k 175-177), las cuatro condiciones de la mesa:
  (a) el cuaderno viaja y se lee: registro `P7_cuaderno` de arranque con `leido` verdadero los dias 2 y 3 y recuerdos del dia anterior dentro;
  (b) en al menos 4 de las 6 vidas la criatura toca algun objeto desconocido (una unidad de botiquin o de racion entra en el zurron; la misma lectura que (b') de P7-27);
  (c) en al menos una criatura sube la creencia de alguno de los dos objetos entre el cierre de un dia y el siguiente (de "no se" a un valor, o a un valor mayor; la del
      botiquin, dentro del circulo; la de la racion, la mayor de sus situaciones);
  (d) la guarda de latencia (regla de la mesa de P7-30: <= 1 % de decisiones por encima del tic y <= 5 % de pasos listos bloqueados sin cuerpo) pasa en las 6 vidas.
  python3 freno_P7_30.py -> P7_30_freno.json"""
import glob, json, os
import analiza_P7_24 as A24, guarda_latencia_P7_29 as GL
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))


def lee(f):
    arr = fin = None
    for line in open(f, errors="replace"):
        if '"P7_cuaderno"' not in line: continue
        r = json.loads(line)
        if r.get("k") == "P7_cuaderno": arr = r if r.get("momento") == "arranque" else arr; fin = r if r.get("momento") == "fin" else fin
    return arr, fin


def creencia(cont, obj):
    c = ((cont or {}).get("creencias") or {}).get(obj) or {}
    if obj == "first_aid": return ((c.get("dentro") or {}) or {}).get("cuerpo")
    vals = [x.get("cuerpo") for k, x in c.items() if isinstance(x, dict) and x.get("cuerpo") is not None]
    return max(vals) if vals else None


if __name__ == "__main__":
    V = {}
    for d in (1, 2, 3):
        for sl in (10, 11):
            fs = glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P729_s1_d{d}_APRENDE_*", f"*policy_agent_{sl}.art.log"))
            if not fs: V[(d, sl)] = {"sin_diario": True}; continue
            T, H, U, P, fin_, final = A24.lee(fs[0]); arr, fin = lee(fs[0]); g = GL.mide(fs[0])
            V[(d, sl)] = {"tics": len(T), "puesto": (final or {}).get("placement"), "leido": bool((arr or {}).get("leido")), "recuerdos_al_arrancar": sum(len(s) for o in (((arr or {}).get("contenido") or {}).get("objetos") or {}).values() for s in (o.get("situaciones") or {}).values()),
                          "contacto": {A24.OBJ[o]: next((T[i]["t"] for i in range(1, len(T)) if T[i]["n"][o] > T[i - 1]["n"][o]), None) for o in A24.OBJ}, "creencia_fin": {"botiquin": creencia((fin or {}).get("contenido"), "first_aid"), "racion": creencia((fin or {}).get("contenido"), "rations")},
                          "huellas": len(H), "guarda": {k: g[k] for k in ("ms_mediana", "ms_p95", "ms_max", "sobre_el_tic", "fraccion_sin_cuerpo", "pasa", "motivo")}}
    a = all(V[(d, sl)].get("leido") and V[(d, sl)].get("recuerdos_al_arrancar", 0) >= 0 for d in (2, 3) for sl in (10, 11)) and all(V[(d, sl)].get("recuerdos_al_arrancar", 0) == sum(len(s) for o in (((lee(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P729_s1_d{d - 1}_APRENDE_*", f"*policy_agent_{sl}.art.log"))[0])[1] or {}).get("contenido") or {}).get("objetos") or {}).values() for s in (o.get("situaciones") or {}).values()) for d in (2, 3) for sl in (10, 11))
    toca = [(d, sl) for (d, sl), v in V.items() if not v.get("sin_diario") and any(x is not None for x in v["contacto"].values())]
    sube = []
    for sl in (10, 11):
        for d in (2, 3):
            for o in ("botiquin", "racion"):
                antes = V[(d - 1, sl)]["creencia_fin"][o]; desp = V[(d, sl)]["creencia_fin"][o]
                if desp is not None and (antes is None or desp > antes): sube.append((d, sl, o, antes, desp))
    guarda = [(d, sl) for (d, sl), v in V.items() if not v.get("sin_diario") and v["guarda"]["pasa"]]
    R = {"vidas": {f"d{d}_a{sl}": v for (d, sl), v in V.items()}, "a_cuaderno_viaja": a, "b_tocan": [f"d{d} a{sl}" for d, sl in toca], "b_pasa": len(toca) >= 4, "c_sube": [f"d{d} a{sl} {o}: {an} -> {de}" for d, sl, o, an, de in sube], "c_pasa": bool(sube), "d_guarda_pasa_en": [f"d{d} a{sl}" for d, sl in guarda], "d_pasa": len(guarda) == 6}
    R["FRENO"] = "PASA" if (R["a_cuaderno_viaja"] and R["b_pasa"] and R["c_pasa"] and R["d_pasa"]) else "NO PASA"
    json.dump(R, open(os.path.join(AQUI, "P7_30_freno.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in R.items() if k != "vidas"}, ensure_ascii=False, indent=1))
    for k, v in R["vidas"].items(): print(k, {kk: vv for kk, vv in v.items() if kk != "guarda"}, "guarda", {kk: v["guarda"][kk] for kk in ("ms_mediana", "sobre_el_tic", "fraccion_sin_cuerpo", "pasa")} if "guarda" in v else None)

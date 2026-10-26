"""[P7-29b, punto 4] LA LATENCIA DE LOS CAMPOS ANTERIORES (P7-10 y P7-14b), leida de los diarios con la guarda de P7-29b (`guarda_latencia_P7_29.mide`): tiempo de decision
por tic (`RADIOGRAFIA.ms`), fraccion de pasos listos bloqueados sin un cuerpo delante, y, por vida, el puesto, si murio, el tic de muerte y la causa (anillo / rival, P7-21).
Solo describir. -> P7_29b_latencia.json
  python3 latencia_P7_29b.py"""
import collections, glob, json, os, statistics as st
import guarda_latencia_P7_29 as GL, analiza_P7_16 as A16
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))


def muerte(f):
    M, T = A16.lee(f)
    if not T: return {}
    murio = (M["final"] or {}).get("reason") == "eliminated"; causa = None
    if murio:
        golpes = [(i, t["t"]) for i, t in enumerate(T) if any(s.startswith("P") or s == "zone" for s, _ in t["dmg"])]; causa = "otra"
        if golpes:
            j = len(golpes) - 1
            while j > 0 and golpes[j][1] - golpes[j - 1][1] <= A16.HUECO: j -= 1
            Ep = T[golpes[j][0]:]; dr = sum(a for t in Ep for s, a in t["dmg"] if s.startswith("P")); dz = sum(a for t in Ep for s, a in t["dmg"] if s == "zone"); causa = "anillo" if dz > dr else "rival"
    return {"puesto": (M["final"] or {}).get("placement"), "murio": murio, "tic_muerte": (T[-1]["t"] if murio else None), "causa": causa, "ultimo_tick": T[-1]["t"]}


if __name__ == "__main__":
    V = []
    for pref, campo in (("P710", "P7-10"), ("P714b", "P7-14b")):
        for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", f"{pref}_s*_d*_*"))):
            b = os.path.basename(c).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]
            for sl in (10, 11):
                fs = glob.glob(os.path.join(c, f"*policy_agent_{sl}.art.log"))
                if not fs or os.path.getsize(fs[0]) < 1000: continue
                g = GL.mide(fs[0]); V.append({"campo": campo, "serie": serie, "dia": dia, "brazo": brazo, "asiento": sl, **g, **muerte(fs[0])})
                print(campo, serie, dia, brazo, sl, g["ms_mediana"], g["ms_p95"], g["fraccion_sin_cuerpo"], flush=True)
    R = {"vidas": V, "por_campo_brazo_bloque": {}}
    for campo in ("P7-10", "P7-14b"):
        for brazo in sorted({v["brazo"] for v in V if v["campo"] == campo}):
            for nb, ds in (("dias 1-5", range(1, 6)), ("dias 6-10", range(6, 11)), ("dias 11-15", range(11, 16)), ("dias 16-20", range(16, 21)), ("todos", range(1, 21))):
                vs = [v for v in V if v["campo"] == campo and v["brazo"] == brazo and v["dia"] in ds and v["ms_mediana"] is not None]
                if not vs: continue
                mu = [v for v in vs if v["murio"]]
                R["por_campo_brazo_bloque"][f"{campo} · {brazo} · {nb}"] = {"vidas": len(vs), "ms_mediana_media": round(st.mean(v["ms_mediana"] for v in vs), 2), "ms_p95_media": round(st.mean(v["ms_p95"] for v in vs), 2), "ms_p95_max": max(v["ms_p95"] for v in vs), "ms_max": max(v["ms_max"] for v in vs),
                                                                            "sobre_el_tic_media": round(st.mean(v["sobre_el_tic"] for v in vs), 4), "sin_cuerpo_media": round(st.mean(v["fraccion_sin_cuerpo"] for v in vs), 4), "vidas_que_no_pasan_la_guarda": sum(1 for v in vs if not v["pasa"]),
                                                                            "vidas_con_p95_sobre_20": sum(1 for v in vs if v["ms_p95"] > 20), "vidas_con_sin_cuerpo_sobre_5": sum(1 for v in vs if v["fraccion_sin_cuerpo"] > 0.05),
                                                                            "muertos": len(mu), "muertes_antes_de_4000": sum(1 for v in mu if v["tic_muerte"] < 4000), "muertes_por_rival": sum(1 for v in mu if v["causa"] == "rival"), "tic_muerte_mediana": (st.median(v["tic_muerte"] for v in mu) if mu else None), "puesto_medio": round(st.mean(v["puesto"] for v in vs if v["puesto"] is not None), 2)}
    # las muertes tempranas y la latencia de esa vida: las vidas que mueren antes de 4.000, ¿pasaban la guarda?
    for campo in ("P7-10", "P7-14b"):
        for brazo in sorted({v["brazo"] for v in V if v["campo"] == campo}):
            vs = [v for v in V if v["campo"] == campo and v["brazo"] == brazo and v["ms_mediana"] is not None]
            tem = [v for v in vs if v["murio"] and v["tic_muerte"] < 4000]
            R["por_campo_brazo_bloque"][f"{campo} · {brazo} · muertes tempranas"] = {"n": len(tem), "no_pasan_la_guarda": sum(1 for v in tem if not v["pasa"]), "sin_cuerpo_media": (round(st.mean(v["fraccion_sin_cuerpo"] for v in tem), 4) if tem else None), "ms_p95_media": (round(st.mean(v["ms_p95"] for v in tem), 2) if tem else None),
                                                                                       "resto": {"n": len(vs) - len(tem), "no_pasan_la_guarda": sum(1 for v in vs if not (v["murio"] and v["tic_muerte"] < 4000) and not v["pasa"]), "sin_cuerpo_media": (round(st.mean(v["fraccion_sin_cuerpo"] for v in vs if not (v["murio"] and v["tic_muerte"] < 4000)), 4) if len(vs) > len(tem) else None)}}
    json.dump(R, open(os.path.join(AQUI, "P7_29b_latencia.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in R["por_campo_brazo_bloque"].items():
        if "todos" in k or "tempranas" in k: print(k, v)

"""[P7-28, puntos 2, 3 y 4] Lectura de los 240 diarios del campo de P7-24 (posterior al sello). Coste cero.
  python3 analiza_P7_28.py -> P7_28_vidas.json
Por vida: botiquines y raciones llevados de media (por tic), cogidos, usados (canales de P7-21: completados y cortes) y la vida al abrir cada canal; muerte: tic, causa
(el episodio final de P7-21: anillo si el anillo hizo mas dano que los rivales en la racha final, rival si no, otra si no hay golpes), vida en el primer golpe de la pelea final
(P7-20), si llevaba botiquin en ese tic y si lo uso despues (algun canal entre el primer golpe y la muerte). Para APRENDE, los usos firmes y "al menos" salen de las huellas."""
import collections, glob, json, os
from multiprocessing import Pool
import analiza_P7_16 as A16, analiza_P7_20 as A20, analiza_P7_21 as A21
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))


def una(x):
    carp, brazo, serie, dia, semilla, slot = x; v = {"brazo": brazo, "serie": serie, "dia": dia, "semilla": semilla, "slot": slot}
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log")); marca = glob.glob(os.path.join(carp, f"PARCIAL_agent_{slot}.json")); v["parcial"] = bool(marca)
    if not f or os.path.getsize(f[0]) < 1000: v["sin_diario"] = True; return v
    M, T = A16.lee(f[0])
    if not T: v["sin_diario"] = True; return v
    X = A21.lee_extra(f[0]); C = A21.canales(T, X, M); murio = (M["final"] or {}).get("reason") == "eliminated"; P = A20.peleas(M, T, murio)
    kid = M["kit"]; racs = M["rac"]; n_r = []
    def dentro(t):
        z = X.get(t["t"], {})
        if z.get("zc") is None or z.get("zr") is None: return None
        return ((t["pos"][0] - z["zc"][0]) ** 2 + (t["pos"][1] - z["zc"][1]) ** 2) ** 0.5 <= z["zr"]
    den = [dentro(t) for t in T]; v["tics_fuera"] = sum(1 for x in den if x is False) / len(T); v["tics_sin_zona"] = sum(1 for x in den if x is None) / len(T)
    v["elegido"] = dict(collections.Counter(t["el"] for t in T)); v["tics_con_rival_a_la_vista"] = sum(1 for t in T if t["riv"]) / len(T); v["dist_al_centro_media"] = (sum(t["centro"] for t in T if t["centro"] is not None) / max(1, sum(1 for t in T if t["centro"] is not None)))
    # raciones por tic (lee de P7-16 solo guarda botiquines): segunda pasada ligera
    for line in open(f[0], errors="replace"):
        if '"k": "tick"' not in line and '"k":"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "tick" and r.get("phase") == "live": n_r.append(sum(int(s.get("n") or 1) for s in (r.get("pack") or []) if s and s.get("id") in racs))
    v.update({"tics": len(T), "ultimo_tick": T[-1]["t"], "murio": murio, "puesto": (M["final"] or {}).get("placement"), "botiquines_media": sum(t["kits"] for t in T) / len(T), "raciones_media": (sum(n_r) / len(n_r) if n_r else None),
              "botiquines_cogidos": sum(max(0, T[i]["kits"] - T[i - 1]["kits"]) for i in range(1, len(T))), "tics_con_botiquin": sum(1 for t in T if t["kits"] >= 1) / len(T),
              "canales_botiquin": len(C), "canales_completados": sum(1 for c in C if c["completado"]), "vida_al_abrir": [c["hp0"] for c in C], "usos_heridos": sum(1 for c in C if c["hp0"] < 50)})
    # huellas (APRENDE / BORRADO): firmes y al menos del botiquin
    H = []
    for line in open(f[0], errors="replace"):
        if '"P7_huella"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "P7_huella" and (r.get("objeto") or "first_aid") == kid: H.append(r)
    v["huellas_botiquin"] = {"n": len(H), "firmes": sum(1 for h in H if h.get("apuntado") and not h.get("corte") and not h.get("al_menos")), "al_menos": sum(1 for h in H if h.get("al_menos")), "cortes": sum(1 for h in H if h.get("corte"))}
    # la muerte
    if murio:
        golpes = [(i, t["t"]) for i, t in enumerate(T) if any(s.startswith("P") or s == "zone" for s, _ in t["dmg"])]
        causa = "otra"; ep = None
        if golpes:
            j = len(golpes) - 1
            while j > 0 and golpes[j][1] - golpes[j - 1][1] <= A16.HUECO: j -= 1
            Ep = T[golpes[j][0]:]; dr = sum(a for t in Ep for s, a in t["dmg"] if s.startswith("P")); dz = sum(a for t in Ep for s, a in t["dmg"] if s == "zone"); causa = "anillo" if dz > dr else "rival"; ep = {"dano_rivales": round(dr, 1), "dano_anillo": round(dz, 1), "empieza": Ep[0]["t"]}
        pm = [p for p in P if p["acaba_en_muerte"]]
        g = None
        if pm:
            tg = pm[0]["t_primer_golpe_de_rival"]; ig = next(i for i, t in enumerate(T) if t["t"] == tg)
            g = {"t": tg, "vida": pm[0]["vida_ante_el_primer_golpe_de_rival"], "llevaba_botiquin": T[ig]["kits"] >= 1, "uso_despues": any(c["t0"] >= tg for c in C), "dentro": den[ig],
                 "elegido_240_antes": dict(collections.Counter(t["el"] for t in T[:ig] if t["t"] >= tg - 240)), "rival_a_la_vista_240_antes": sum(1 for t in T[:ig] if t["t"] >= tg - 240 and t["riv"]) / max(1, sum(1 for t in T[:ig] if t["t"] >= tg - 240))}
        v["muerte"] = {"tic": T[-1]["t"], "causa": causa, "episodio": ep, "primer_golpe": g, "llevaba_botiquin_al_morir": T[-1]["kits"] >= 1, "dentro_al_morir": den[-1], "hp_1200_antes": next((t["hp"] for t in T if t["t"] >= T[-1]["t"] - 1200), None)}
    return v


if __name__ == "__main__":
    tareas = []
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P724_s*_d*_*_*"))):
        b = os.path.basename(c).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]; semilla = int(b[4])
        for sl in (10, 11): tareas.append((c, brazo, serie, dia, semilla, sl))
    with Pool(4) as P: V = P.map(una, tareas)
    V = {f"s{v['serie']}_d{v['dia']}_{v['brazo']}_{v['slot']}": v for v in V}
    json.dump(V, open(os.path.join(AQUI, "P7_28_vidas.json"), "w"), ensure_ascii=False, indent=0)
    print("vidas", len(V), "sin diario", sum(1 for v in V.values() if v.get("sin_diario")))

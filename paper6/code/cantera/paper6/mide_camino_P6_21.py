"""[P6-21 · 4] EL FUEGO DEL CAMINO: ¿la curva proyectada de un plan cuenta el fuego de la
casilla actual y del tramo de ir? SOLO LECTURA de los 40 diarios de A6, de uno en uno, y
la proyeccion CONGELADA de verdad (`proyeccion.proyectar_rapido`, la que usa
`forma.curva_H`), llamada desde fuera sobre el estado del diario en el tic en que nacio
cada plan (`proyeccion.estado_de`).

Por cada plan de la fase 5 (los 74 de P6-18): desde el estado real al nacer (`nace`), se
proyecta tramo a tramo hasta cada punto de control (`tics`) igual que `curva_H` (sin la
foto ni las filas), y se anota la vida proyectada y el fuego imaginado (`_hecho.dano_anillo`)
en cada control; enfrente, la vida real del diario en ese tic y el fuego real recibido
entre `nace` y el control, partido en «siguiendo» (sin ruptura abierta, como en P6-20) y
«desviado». Se cuenta tambien si al nacer el cuerpo estaba en casilla que la proyeccion da
por ardiendo (d > radio interpolado) y cuantos tics imagina antes del primer paso.
"""
import collections, glob, json, math, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
import proyeccion as P
import forma as F
C = (24, 24); FASE5 = 4
OUT = []
for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball/runs/P618_t1_A6_*"))):
    fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
    if len(fs) != 2:
        continue
    sem = int(carp.rsplit("_", 1)[1])
    for sl in (10, 11):
        recs = list(U.lee(fs[sl]))
        pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo"); sm = next(r for r in recs if r["k"] == "static_map")
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); zs = pc["zone_schedule"]; warn5, sig5 = zs[FASE5][0], zs[FASE5 + 1][0]
        T = {r["tick"]: r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"}
        if warn5 not in T:
            del recs, T; continue
        c6 = collections.defaultdict(dict)
        for r in recs:
            if r.get("k") == "compromiso6":
                c6[r.get("id")][r["tick"]] = r.get("estado")
        caidas = {r.get("id"): r for r in recs if r.get("k") == "forma_caida"}
        for fa in [r for r in recs if r.get("k") == "forma_aceptada" and warn5 <= r["tick"] < sig5]:
            nace = fa["nace"]
            if nace not in T:
                continue
            e = P.estado_de(T[nace]); tramos = fa["tramos"]; tics = fa["tics"]
            pos0 = tuple(T[nace]["pos"]); d0 = math.dist(pos0, C); cal0 = mundo.anillo_en(nace)[1]
            suelo = {}; curva = []; fuego_img = 0.0
            for i, tic in enumerate(tics):
                K = tic - e["tick"]
                if K < 0:
                    curva.append({"tic": tic, "vida": e["hp"], "fuego_imaginado": round(fuego_img, 2), "pos": list(e["pos"])}); continue
                tr = tramos[i] if i < len(tramos) else {"destino": None, "intencion": "esperar"}
                plan = {"destino": tr.get("destino"), "coger": tr.get("intencion") == "coger", "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
                e = P.proyectar_rapido(e, plan, K, mundo, suelo)
                fuego_img += float((e.get("_hecho") or {}).get("dano_anillo") or 0.0)
                curva.append({"tic": tic, "vida": round(e["hp"], 2), "fuego_imaginado": round(fuego_img, 2), "pos": list(e["pos"])})
            # lo real, entre nace y cada control, partido en siguiendo / desviado
            fin = min(caidas[fa["id"]]["tick"] if fa["id"] in caidas else 10 ** 9, max(T))
            real = []; f_sig = f_des = 0.0; desv = False; prev_desv = False
            for t in sorted(T):
                if t < nace or t > max(tics):
                    continue
                r = T[t]; zh = sum(float(g.get("amount") or 0) for g in (r.get("damage_taken") or []) if isinstance(g, dict) and g.get("source") == "zone")
                est = c6.get(fa["id"], {}).get(t); dd = math.dist(r["pos"], C)
                dentro = dd <= min(zs[FASE5][4], (r.get("zona") or {}).get("radius") or 48)
                desv = (est == "rompe") or (prev_desv and not dentro); prev_desv = desv
                if t <= fin:
                    if desv:
                        f_des += zh
                    else:
                        f_sig += zh
                for c in curva:
                    if c["tic"] == t:
                        c["vida_real"] = float(r["hp"]); c["fuego_real_siguiendo"] = round(f_sig, 2); c["fuego_real_desviado"] = round(f_des, 2); c["pos_real"] = list(r["pos"])
            mo = str((caidas.get(fa["id"]) or {}).get("motivo") or ""); m = re.search(r"la vida real ([\d.]+) esta por debajo de la proyectada ([\d.]+)", mo)
            OUT.append({"sem": sem, "slot": sl, "id": fa["id"], "nace": nace, "aceptada": fa["tick"], "pos0": list(pos0), "d0": round(d0, 2), "cal0": round(cal0, 2), "obs0": (T[nace].get("zona") or {}).get("radius"),
                        "arde_al_nacer_segun_proyeccion": d0 > cal0, "quema_al_nacer_segun_juego": d0 > ((T[nace].get("zona") or {}).get("radius") or 48), "hp0": float(T[nace]["hp"]), "mri0": int(T[nace].get("move_ready_in") or 0),
                        "destino": (tramos[0].get("destino") if tramos else None), "tics": tics, "curva": curva, "caida": ("vida real" if m else ("reevaluacion" if "reevaluacion" in mo else (mo[:20] if mo else None))), "X": float(m.group(1)) if m else None, "Y": float(m.group(2)) if m else None,
                        "fuego_real_siguiendo_hasta_fin": round(f_sig, 2), "fuego_real_desviado_hasta_fin": round(f_des, 2), "fuego_imaginado_total": round(fuego_img, 2)})
        del recs, T
    print(f"  A6 {sem}: planes {len(OUT)}", flush=True)

n = len(OUT)
con_img = [o for o in OUT if o["fuego_imaginado_total"] > 0]
R = {"nota": "P6-21 §4. INSTRUMENTO DE MEDIDA. Proyeccion congelada (proyeccion.proyectar_rapido) aplicada desde fuera al estado real al nacer cada plan de la fase 5 de A6.",
     "planes": n, "arden_al_nacer_segun_proyeccion": sum(1 for o in OUT if o["arde_al_nacer_segun_proyeccion"]), "queman_al_nacer_segun_juego": sum(1 for o in OUT if o["quema_al_nacer_segun_juego"]),
     "planes_con_fuego_imaginado": len(con_img), "fuego_imaginado_total": round(sum(o["fuego_imaginado_total"] for o in OUT), 1), "fuego_real_siguiendo_total (hasta la caida o el ultimo control)": round(sum(o["fuego_real_siguiendo_hasta_fin"] for o in OUT), 1),
     "fuego_real_desviado_total": round(sum(o["fuego_real_desviado_hasta_fin"] for o in OUT), 1), "planes_con_fuego_real_siguiendo": sum(1 for o in OUT if o["fuego_real_siguiendo_hasta_fin"] > 0),
     "planes_con_fuego_real_siguiendo_y_0_imaginado": sum(1 for o in OUT if o["fuego_real_siguiendo_hasta_fin"] > 0 and o["fuego_imaginado_total"] == 0),
     "coincide_Y_con_la_curva (caidas vida real)": {"n": sum(1 for o in OUT if o["caida"] == "vida real"), "coinciden": sum(1 for o in OUT if o["caida"] == "vida real" and any(abs(c["vida"] - o["Y"]) < 0.51 for c in o["curva"]))},
     "planes": OUT}
def _sane(x):
    if isinstance(x, dict):
        return {str(k): _sane(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_sane(v) for v in x]
    return x
json.dump(_sane(R), open(os.path.join(AQUI, "P6_21_camino.json"), "w"), ensure_ascii=False, indent=1, default=str)
print({k: v for k, v in R.items() if k not in ("planes", "nota")})
print("-> P6_21_camino.json")

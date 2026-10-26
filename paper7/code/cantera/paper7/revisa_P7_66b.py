"""[P7-67, decision 5 de la mesa] REVISION, SIN JUGAR, DE LOS 11 INTENTOS DEL SEGUNDO BANCO DE P7-66 (_P7_66b_local, P7_66b_local.json): ¿en cuantos influyo la regla de distancia
8-15 (de ella y de su hermana) que invita_P7_66b mira en cada tic?
Por intento (de la aceptacion a su cierre), tic a tic, desde los diarios: si `ir_sitio` esta entre los candidatos del cuerpo (RADIOGRAFIA.candidatos), la distancia de ella y de su hermana
(posicion de la hermana: la de su propio diario en ese tic) al destino, si sigue en el tramo de 300 tics y si hay calma (ningun rival —cualquiera que no sea ella ni su hermana, como en
P7-66— a <= 5 y ningun golpe en 48 tics). Un tic «cortado por la distancia» = dentro del tramo, en calma, sin `ir_sitio`, y con ella o su hermana fuera de 8-15.
INFLUYO = al menos un tic cortado por la distancia antes del cierre. Se da tambien la distancia minima alcanzada y los tics a 7.
  python3 revisa_P7_66b.py -> P7_66b_revision.json"""
import glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); LOC = os.path.join(AQUI, "_P7_66b_local"); R = json.load(open(os.path.join(AQUI, "P7_66b_local.json")))
BRAZO = {10: "MIENTE", 11: "MIENTE", 12: "HONESTA", 13: "HONESTA"}; EMPUJE = 300; DMIN, DMAX = 8, 15
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def ticks(d, sl):
    T = {}; golpe = -10 ** 9
    for l in open(os.path.join(LOC, d, "logs", f"policy_agent_{sl}.log"), errors="replace"):
        if not l.startswith('{"k":"tick"'): continue
        r = json.loads(l)
        if r.get("phase") != "live": continue
        t = r["tick"]; pos = tuple(r.get("pos") or (0, 0))
        if any(float(x.get("amount") or 0) > 0 for x in (r.get("damage_taken") or [])): golpe = t
        riv = [cheb(pos, tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") not in (sl, sl ^ 1)]
        Rg = r.get("RADIOGRAFIA") or {}; c = Rg.get("candidatos")
        T[t] = {"pos": pos, "calma": not (riv and min(riv) <= 5) and t - golpe > 48, "cands": None if c is None else set(c), "el": Rg.get("elegido")}
    return T


out = []
for d in sorted(R):
    for s, h in R[d]["P7_66"].items():
        sl = int(s)
        if not h["aceptadas"]: continue
        T = ticks(d, sl); TH = ticks(d, sl ^ 1); tic0 = min(T)
        cierres = [("llegada", x) for x in h["llegadas"]] + [("interrumpida", x) for x in h["interrumpidas"]] + [("no_llego", x) for x in h["no_llego"]]
        for a in h["aceptadas"]:
            c = next(((k, x) for k, x in cierres if x["n"] == a["n"] and x["t_aceptada"] + 1 >= a["tick"] - 1 and x["tick"] >= a["tick"]), (None, None))
            dest = tuple(a["destino"]); t1 = c[1]["tick"] if c[1] else max(T)
            n = con_c = con_ir = cort_d = cort_ella = cort_herm = fuera_tramo = sin_calma = a7 = 0; dmin = None; primero = None
            for t in range(a["tick"], t1):
                if t not in T: continue
                w = T[t]; n += 1; de = cheb(w["pos"], dest); dmin = de if dmin is None else min(dmin, de); a7 += de == 7
                hp = TH.get(t, {}).get("pos"); dh = cheb(hp, dest) if hp else None
                if w["cands"] is None: continue
                con_c += 1; ir = "ir_sitio" in w["cands"]; con_ir += ir
                tramo = t - tic0 < EMPUJE; fuera_tramo += not tramo; sin_calma += not w["calma"]
                fe = not (DMIN <= de <= DMAX); fh = dh is not None and not (DMIN <= dh <= DMAX)
                if not ir and tramo and w["calma"] and (fe or fh):
                    cort_d += 1; cort_ella += fe; cort_herm += fh and not fe
                    if primero is None: primero = {"tic": t, "tics_desde_aceptar": t - a["tick"], "distancia_ella": de, "distancia_hermana": dh}
            out.append({"dia": d, "asiento": sl, "brazo": BRAZO[sl], "destino": list(dest), "tic_aceptada": a["tick"], "distancia_al_aceptar": a["distancia"], "distancia_hermana_al_aceptar": a.get("distancia_hermana"),
                        "cierre": c[0], "tic_cierre": t1, "tics": t1 - a["tick"], "tics_con_candidatos": con_c, "tics_con_ir_sitio": con_ir, "tics_cortados_por_la_distancia": cort_d,
                        "de_ellos_por_ella": cort_ella, "de_ellos_solo_por_la_hermana": cort_herm, "tics_fuera_del_tramo": fuera_tramo, "tics_sin_calma": sin_calma,
                        "distancia_minima": dmin, "tics_a_7": a7, "primer_corte": primero, "influyo": cort_d > 0})
res = {"intentos": out, "n": len(out), "influyo": sum(x["influyo"] for x in out),
       "por_cierre": {k: {"intentos": sum(1 for x in out if x["cierre"] == k), "influyo": sum(1 for x in out if x["cierre"] == k and x["influyo"])} for k in ("llegada", "interrumpida", "no_llego")},
       "por_brazo": {b: {"intentos": sum(1 for x in out if x["brazo"] == b), "influyo": sum(1 for x in out if x["brazo"] == b and x["influyo"])} for b in ("MIENTE", "HONESTA")}}
json.dump(res, open(os.path.join(AQUI, "P7_66b_revision.json"), "w"), ensure_ascii=False, indent=1)
for x in out: print(x["dia"], x["asiento"], x["brazo"], x["distancia_al_aceptar"], x["cierre"], x["tics"], "cands", x["tics_con_candidatos"], "ir", x["tics_con_ir_sitio"], "cortados", x["tics_cortados_por_la_distancia"], f"(ella {x['de_ellos_por_ella']}, hermana {x['de_ellos_solo_por_la_hermana']})", "dmin", x["distancia_minima"], "a7", x["tics_a_7"], x["primer_corte"])
print({k: v for k, v in res.items() if k != "intentos"})

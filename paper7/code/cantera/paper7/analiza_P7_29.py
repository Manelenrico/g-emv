"""[P7-29, F4] EL HUMO DE 3 DIAS leido de los diarios (paintball/runs/P729_s1_d<D>_APRENDE_<semilla>/, dos asientos) -> P7_29_humo.json. Coste cero.
Por dia y criatura: contactos (primer tic con la cosa en el zurron), usos con su vida (canales abiertos, P7-21), firmes y "al menos" (huellas), cortes aparte con su
causa (los recuerdos `acto` del cuaderno), creencia del botiquin y de la racion (cuaderno al acabar: sin los cortes por construccion), ignorancia de la clase y del
cuanto, pasos bloqueados (`action_result` = blocked con el paso listo) y muros aprendidos (`P7_muro`), tiempo en `ir_curioso` con el paso listo, y el tiempo de decision
por tic (`RADIOGRAFIA.ms`; el tic son 1000/24 = 41,67 ms).
  python3 analiza_P7_29.py"""
import collections, glob, json, os, statistics as st
import analiza_P7_24 as A24, analiza_P7_16 as A16, analiza_P7_21 as A21
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); OBJ = A24.OBJ; TIC_MS = 1000.0 / 24


def una(carp, dia, slot):
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))
    v = {"dia": dia, "asiento": slot, "semilla": int(os.path.basename(carp).split("_")[-1])}
    if not f: v["sin_diario"] = True; return v
    T, H, U, P, fin, final = A24.lee(f[0]); v["tics"] = len(T)
    if not T: v["sin_diario"] = True; return v
    muros = []; cuanto = []; arranque = None; ms = []; bl = 0; listos = 0; cur = 0
    for line in open(f[0], errors="replace"):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "P7_muro": muros.append(r)
        elif k == "P7_cuanto": cuanto.append(r)
        elif k == "P7_arranque": arranque = r.get("P7_29")
        elif k == "tick" and r.get("phase") == "live":
            m = (r.get("RADIOGRAFIA") or {}).get("ms")
            if m is not None: ms.append(float(m))
            if (r.get("move_ready_in") or 0) == 0:
                listos += 1; bl += int(r.get("action_result") == "blocked"); cur += int(str((r.get("RADIOGRAFIA") or {}).get("elegido") or "") == "ir_curioso")
    v["puesto"] = (final or {}).get("placement"); v["murio"] = (final or {}).get("reason") == "eliminated"; v["P7_29"] = arranque
    v["contacto"] = {OBJ[o]: next((T[i]["t"] for i in range(1, len(T)) if T[i]["n"][o] > T[i - 1]["n"][o]), None) for o in OBJ}
    v["cogidos"] = {OBJ[o]: sum(max(0, T[i]["n"][o] - T[i - 1]["n"][o]) for i in range(1, len(T))) for o in OBJ}
    usos = {"botiquin": [], "racion": []}
    for h in H:
        o = OBJ.get(h.get("objeto") or "first_aid", "botiquin")
        usos[o].append({"t0": h["t0"], "hp0": h["hp0"], "completado": not h.get("corte"), "al_menos": bool(h.get("al_menos")), "firme": bool(not h.get("corte") and not h.get("al_menos") and h.get("apuntado")), "efecto": h["efecto"]["cuerpo"], "situacion": h.get("situacion"), "dano_en_ventana": h.get("dano_total")})
    v["usos"] = usos
    cont = ((fin or {}).get("contenido") or {}); cr = cont.get("creencias") or {}; rec = cont.get("objetos") or {}
    v["al_acabar"] = {}
    for o, nom in OBJ.items():
        c = cr.get(o) or {}; rs = [r for s_ in ((rec.get(o) or {}).get("situaciones") or {}).values() for r in s_]
        v["al_acabar"][nom] = {"creencia": {s_: (x or {}).get("cuerpo") for s_, x in c.items() if isinstance(x, dict)}, "ignorancia": c.get("ignorancia"), "ignorancia_cuanto": c.get("ignorancia_cuanto"), "sabido_max": c.get("sabido_max"), "pesos_firmes": c.get("pesos_firmes"),
                              "recuerdos": len(rs), "firmes": sum(1 for r in rs if not r.get("corte") and not r.get("al_menos")), "al_menos": sum(1 for r in rs if r.get("al_menos")), "cortes": sum(1 for r in rs if r.get("corte")),
                              "causas_de_corte": [r.get("causa_corte") for r in rs if r.get("corte") and r.get("dia") == cont.get("dia")]}
    v["bloqueados"] = {"paso_listo": listos, "bloqueados": bl, "fraccion": round(bl / max(1, listos), 4)}; v["muros_aprendidos"] = [{k_: m.get(k_) for k_ in ("tick", "casilla", "desde", "dir")} for m in muros]
    v["ir_curioso_con_paso_listo"] = cur; v["ir_curioso_fraccion"] = round(cur / max(1, listos), 4)
    v["ms"] = {"mediana": (round(st.median(ms), 2) if ms else None), "p90": (round(sorted(ms)[int(0.9 * len(ms))], 2) if ms else None), "max": (round(max(ms), 2) if ms else None), "sobre_el_tic": (round(sum(1 for m in ms if m > TIC_MS) / len(ms), 4) if ms else None)}
    v["cuanto_registros"] = [{k_: c.get(k_) for k_ in ("tick", "M", "M_curiosidad", "clases")} for c in cuanto[::4]][:12]
    v["aperturas_hp"] = [u["hp"] for u in U if OBJ.get(u.get("objeto"), u.get("objeto")) == "botiquin"]
    return v


if __name__ == "__main__":
    V = []
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P729_s1_d*_APRENDE_*"))):
        d = int(os.path.basename(c).split("_")[2][1:])
        for sl in (10, 11): V.append(una(c, d, sl))
    json.dump(V, open(os.path.join(AQUI, "P7_29_humo.json"), "w"), ensure_ascii=False, indent=1)
    for v in V:
        if v.get("sin_diario"): print(v, "sin diario"); continue
        print(f"d{v['dia']} a{v['asiento']} tics {v['tics']} puesto {v['puesto']} contacto {v['contacto']} usos bot {len(v['usos']['botiquin'])} rac {len(v['usos']['racion'])} | bot al acabar {v['al_acabar']['botiquin']} | bloq {v['bloqueados']} muros {len(v['muros_aprendidos'])} ir_curioso {v['ir_curioso_fraccion']} ms {v['ms']}")

"""[P7-46] BANCO, coste cero, EXPLORATORIO (sin sello): LECTURA POR PRUEBA del campo P7-45 (las tres series, 720 vidas; BORRADO solo como referencia).
Lee los diarios paintball/runs/P741_s<S>_d<D>_<variante>_<semilla>/ (dos asientos) -> P7_46_datos.json. Por vida:
  1. SIN: cada forzada (`P7_41_azar` momento=forzada) con su fin (cogida / usada / caduca; `momento=fin`) y, en las que caducan, el diagnostico de los 240 tics: cuantos tics la accion
     forzada (ir_azar / coger / usar_*) estuvo entre los candidatos y cuantos fue la elegida; distancia al destino al abrir y al caducar; si el objeto seguia a la vista al caducar;
     pasos bloqueados; tics en la casilla del destino; tics con `hacer_sitio_*` (zurron lleno) o `coger` o `usar_*` entre los candidatos; hp al abrir, minimo y tics a 100; rival a <= 8 al abrir; y si murio dentro.
  2. Pruebas (`P7_huella`): objeto, t0, situacion, corte, al_menos, interrumpido, regalado, apuntado, hp0, creencia_despues.cuerpo (la creencia del cuerpo tras ESA prueba); y la
     apertura (`P7_33_prueba` abre) mas cercana con su `peligro` (calma / rival_a_4 / fuego / vida_menor_30, del congelado P7-33).
  3. La creencia del botiquin y de la racion al cerrar (`P7_cuaderno` fin: creencias[o].dentro.cuerpo), como en analiza_P7_34.
  python3 banco_P7_46.py"""
import glob, json, math, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs")
CUATRO = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}
FORZ = {"ir": ("ir_azar", "coger"), "usar": ("usar_botiquin", "usar_racion")}


def vida(f):
    T = []; AZ = []; HU = []; AB = []; CU = None; team = None; murio_t = None
    for line in open(f, errors="replace"):
        if not (line.startswith('{"k":"tick"') or line.startswith('{"k":"P7_41_azar"') or line.startswith('{"k":"P7_huella"') or line.startswith('{"k":"P7_33_prueba"') or line.startswith('{"k":"P7_cuaderno"')): continue
        try: r = json.loads(line)
        except Exception: continue
        k = r["k"]
        if k == "tick":
            if r.get("phase") != "live": continue
            if team is None: team = r.get("team")
            ra = r.get("RADIOGRAFIA") or {}; pos = tuple(r.get("pos") or (0, 0))
            riv = [max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])) for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("team") != team]
            items = {(it.get("id"), tuple(it.get("pos"))) for it in (r.get("ve_items") or []) if it.get("pos")}
            ar = r.get("action_result"); bloq = isinstance(ar, dict) and (ar.get("ok") is False or ar.get("blocked")) or (isinstance(ar, str) and "block" in ar)
            T.append({"t": r["tick"], "pos": pos, "hp": float(r.get("hp") or 0.0), "el": str(ra.get("elegido") or ""), "cands": set((ra.get("candidatos") or {}).keys()), "riv8": any(d <= 8 for d in riv), "items": items, "bloq": bool(bloq)})
        elif k == "P7_41_azar":
            if r.get("momento") in ("forzada", "fin"): AZ.append(r)
        elif k == "P7_huella": HU.append(r)
        elif k == "P7_33_prueba":
            if r.get("momento") == "abre": AB.append(r)
        elif k == "P7_cuaderno":
            if r.get("momento") == "fin": CU = r
    if not T: return None
    idx = {t["t"]: i for i, t in enumerate(T)}; t_ult = T[-1]["t"]
    # 1. forzadas con su fin
    forz = []; abierta = None
    for r in AZ:
        if r["momento"] == "forzada": abierta = {"t0": r["tick"], "objeto": CUATRO.get(r["objeto"], r["objeto"]), "tipo": r["tipo"], "destino": (tuple(r["destino"]) if r.get("destino") else None), "conocida": r.get("conocida"), "fin": None}
        elif r["momento"] == "fin" and abierta and abierta["objeto"] == CUATRO.get(r["objeto"], r["objeto"]):
            abierta["fin"] = r["fin"]; abierta["duracion"] = r.get("duracion"); abierta["t_fin"] = r["tick"]; forz.append(abierta); abierta = None
    if abierta: abierta["fin"] = "sin fin (murio o acabo la partida)"; abierta["t_fin"] = t_ult; forz.append(abierta)
    for fz in forz:
        i0 = idx.get(fz["t0"]); i1 = idx.get(fz.get("t_fin"), len(T) - 1)
        if i0 is None: continue
        w = T[i0:i1 + 1]; quiero = FORZ[fz["tipo"]]
        t0 = T[i0]; d0 = (max(abs(fz["destino"][0] - t0["pos"][0]), abs(fz["destino"][1] - t0["pos"][1])) if fz["destino"] else None)
        tf = T[i1]; d1 = (max(abs(fz["destino"][0] - tf["pos"][0]), abs(fz["destino"][1] - tf["pos"][1])) if fz["destino"] else None)
        obj_id = next((o for o, nom in CUATRO.items() if nom == fz["objeto"]), None)
        fz.update({"hp0": t0["hp"], "riv8_0": t0["riv8"], "d0": d0, "d_fin": d1, "tics": len(w), "tics_cand": sum(1 for t in w if any(q in t["cands"] for q in quiero)), "tics_elegida": sum(1 for t in w if t["el"] in quiero),
                   "tics_bloq": sum(1 for t in w if t["bloq"]), "tics_en_destino": (sum(1 for t in w if t["pos"] == fz["destino"]) if fz["destino"] else None), "tics_hacer_sitio": sum(1 for t in w if any(q.startswith("hacer_sitio") for q in t["cands"])), "tics_coger_cand": sum(1 for t in w if "coger" in t["cands"]), "tics_usar_cand": sum(1 for t in w if any(q.startswith("usar_") for q in t["cands"])), "hp_min": min(t["hp"] for t in w), "tics_hp_100": sum(1 for t in w if t["hp"] >= 100), "riv8_tics": sum(1 for t in w if t["riv8"]), "objeto_a_la_vista_al_fin": (any(o == obj_id and (fz["destino"] is None or q == fz["destino"]) for o, q in tf["items"]) if fz["destino"] else None),
                   "murio_dentro": (fz.get("t_fin", 0) >= t_ult and fz["fin"] != "caduca" and i1 == len(T) - 1)})
    # 2. huellas con su apertura
    hu = []
    for h in HU:
        ab = min(AB, key=lambda a: abs(a["tick"] - h["t0"])) if AB else None
        pel = (ab.get("peligro") or {}) if ab and abs(ab["tick"] - h["t0"]) <= 24 else {}
        hu.append({"objeto": CUATRO.get(h.get("objeto") or "first_aid", h.get("objeto")), "t0": h["t0"], "t_fin": h.get("t_fin"), "situacion": h.get("situacion"), "corte": bool(h.get("corte")), "al_menos": bool(h.get("al_menos")), "interrumpido": bool(h.get("interrumpido")), "regalado": bool(h.get("regalado")), "apuntado": bool(h.get("apuntado")),
                   "hp0": h.get("hp0"), "efecto_cuerpo": ((h.get("efecto") or {}).get("cuerpo")), "creencia_despues": ((h.get("creencia_despues") or {}).get("cuerpo")), "calma": (pel.get("calma") if pel else None), "peligro": ({k: pel.get(k) for k in ("rival_a_4", "fuego", "vida_menor_30", "d_rival")} if pel else None)})
    # 3. creencias al cerrar
    cr = ((CU or {}).get("contenido") or {}).get("creencias") or {}
    al_cerrar = {nom: (((cr.get(o) or {}).get("dentro") or {}).get("cuerpo") if isinstance((cr.get(o) or {}).get("dentro"), dict) else None) for o, nom in CUATRO.items()}
    return {"tics": len(T), "t_ult": t_ult, "murio": t_ult < 14000, "forzadas": forz, "huellas": hu, "aperturas": len(AB), "al_cerrar": al_cerrar}


if __name__ == "__main__":
    V = []
    for c in sorted(glob.glob(os.path.join(RUNS, "P741_s*_d*_*"))):
        b = os.path.basename(c).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); var = "_".join(b[3:-1])
        if var == "HUMO43": continue
        for sl in (10, 11):
            fs = glob.glob(os.path.join(c, f"*policy_agent_{sl}.art.log"))
            v = vida(fs[0]) if fs else None
            if v is None: V.append({"serie": serie, "dia": dia, "variante": var, "asiento": sl, "sin_diario": True}); continue
            v.update({"serie": serie, "dia": dia, "variante": var, "asiento": sl}); V.append(v)
            print(f"s{serie} d{dia} {var} a{sl}: huellas {len(v['huellas'])} forzadas {len(v['forzadas'])} ({sum(1 for f in v['forzadas'] if f['fin'] == 'caduca')} caducan) creencia b {v['al_cerrar']['botiquin']}", flush=True)
    json.dump(V, open(os.path.join(AQUI, "P7_46_datos.json"), "w"), ensure_ascii=False, indent=0, default=list); print(len(V), "vidas")

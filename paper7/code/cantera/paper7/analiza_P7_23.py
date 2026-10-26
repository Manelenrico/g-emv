"""[P7-23, F3] EL HUMO DE NACER SIN SABER, leido de los diarios (paintball/runs/P723_s1_d<D>_APRENDE_<semilla>/, los dos asientos). Coste cero.
  python3 analiza_P7_23.py -> P7_23_humo.json (y lo imprime)
Por dia y criatura: que toca primero (la primera unidad de botiquin o de racion que entra en el zurron), en que tic, y por que (lo elegido en los
30 s anteriores: `ir_curioso` = curiosidad; `ir_objeto` = ganas; otra cosa = de paso); cuantos coge y usa de cada uno, con que vida al usar;
recuerdos firmes y "al menos" (registro `P7_huella`, con `objeto`); creencia e ignorancia de cada uno al acabar (registro `P7_cuaderno` de fin);
la esperanza cuando aparece (registro `P7_nace_uso`: `esperanza` > 0 por primera vez); pedidos; soltar.
"""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
OBJ = {"first_aid": "botiquin", "rations": "racion"}


def lee(f):
    T = []; H = []; U = []; P = []; fin = None; arranque = None
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live":
            pack = r.get("pack") or []; n = collections.Counter()
            for s in pack:
                if s: n[s.get("id")] += int(s.get("n") or 1)
            T.append({"t": r["tick"], "hp": r.get("hp"), "n": {o: n.get(o, 0) for o in OBJ}, "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""), "pos": r.get("pos"),
                      "canal": next((e.get("item") for e in (r.get("effects") or []) if e.get("id") == "channeling"), None)})
        elif k == "P7_huella": H.append(r)
        elif k == "P7_nace_uso": U.append(r)
        elif k == "P7_pido": P.append(r)
        elif k == "P7_cuaderno" and r.get("momento") == "fin": fin = r
        elif k == "P7_arranque": arranque = r
        elif k == "final": final = r
    return T, H, U, P, fin, arranque


def una(carp, slot):
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))
    if not f: return None
    T, H, U, P, fin, arr = lee(f[0]); out = {"tics": len(T), "ultimo_tick": T[-1]["t"] if T else None}
    # que toca primero
    primero = None
    for i in range(1, len(T)):
        for o in OBJ:
            if T[i]["n"][o] > T[i - 1]["n"][o]:
                antes = collections.Counter(t["el"] for t in T[max(0, i - 720):i]); ir = {k_: v for k_, v in antes.items() if k_.startswith("ir_")}
                top = max(ir, key=ir.get) if ir else None
                porque = "curiosidad" if top == "ir_curioso" else "ganas" if top == "ir_objeto" else "de paso"
                primero = {"objeto": OBJ[o], "tic": T[i]["t"], "porque": porque, "elegido_en_los_30_s_antes": {k_: v for k_, v in antes.most_common(5)}}; break
        if primero: break
    out["toca_primero"] = primero
    # cogidas y usos
    cog = {o: sum(max(0, T[i]["n"][o] - T[i - 1]["n"][o]) for i in range(1, len(T))) for o in OBJ}
    out["coge"] = {OBJ[o]: cog[o] for o in OBJ}
    usos = {OBJ[o]: [] for o in OBJ}
    for h in H:
        o = h.get("objeto") or "first_aid"; usos[OBJ.get(o, o)].append({"t0": h["t0"], "hp0": h["hp0"], "hp_fin": h["hp_fin"], "completado": not h.get("corte"), "al_menos": h.get("al_menos"), "efecto_cuerpo": h["efecto"]["cuerpo"], "situacion": h.get("situacion"), "apuntado": h.get("apuntado")})
    out["usos"] = {k_: {"n": len(v), "completados": sum(1 for x in v if x["completado"]), "cortes": sum(1 for x in v if not x["completado"]), "vida_al_usar": [x["hp0"] for x in v], "firmes": sum(1 for x in v if x["completado"] and not x["al_menos"]), "al_menos": sum(1 for x in v if x["al_menos"]), "efectos": [x["efecto_cuerpo"] for x in v]} for k_, v in usos.items()}
    # creencia e ignorancia al acabar
    cr = ((fin or {}).get("contenido") or {}).get("creencias") or {}
    out["al_acabar"] = {OBJ[o]: {"creencia": {s_: (c_ or {}).get("cuerpo") for s_, c_ in cr.get(o, {}).items() if s_ not in ("ignorancia", "pesos_vividos")}, "ignorancia": cr.get(o, {}).get("ignorancia"), "pesos_vividos": cr.get(o, {}).get("pesos_vividos")} if o in cr else {"creencia": None, "ignorancia": 1.0} for o in OBJ}
    out["recuerdos_al_acabar"] = sum(len(s_) for o_ in (((fin or {}).get("contenido") or {}).get("objetos") or {}).values() for s_ in (o_.get("situaciones") or {}).values())
    # esperanza
    e1 = next((u for u in U if (u.get("esperanza") or 0) > 0), None)
    out["esperanza_aparece"] = {"tic": e1["tick"], "objeto": OBJ.get(e1["objeto"], e1["objeto"]), "vale": e1["esperanza"], "heal_imaginado": e1.get("heal_imaginado")} if e1 else None
    out["aperturas_registradas"] = [{"t": u["tick"], "objeto": OBJ.get(u["objeto"], u["objeto"]), "hp": u["hp"], "heal_imaginado": u.get("heal_imaginado"), "creencia_vivida": u.get("creencia_vivida"), "ignorancia": u.get("ignorancia"), "esperanza": u.get("esperanza"), "contexto": u.get("contexto")} for u in U]
    out["pedidos"] = {"abre": sum(1 for p in P if p.get("abre")), "tics_pidiendo": sum(1 for p in P if p.get("pide"))}
    out["elige"] = {k_: v for k_, v in collections.Counter(t["el"] for t in T).items() if k_.startswith(("soltar_", "usar_", "ir_curioso", "coger", "hacer_sitio"))}
    out["nace"] = ((arr or {}).get("nace") or {}).get("NACE")
    return out


if __name__ == "__main__":
    carps = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P723_s1_d*_APRENDE_*")))
    OUT = {}
    for c in carps:
        b = os.path.basename(c).split("_"); dia = int(b[2][1:])
        for sl in (10, 11):
            r = una(c, sl)
            if r: OUT[f"d{dia}_{sl}"] = r
    json.dump(OUT, open(os.path.join(AQUI, "P7_23_humo.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in OUT.items():
        print(k, "| toca primero:", v["toca_primero"] and {kk: v["toca_primero"][kk] for kk in ("objeto", "tic", "porque")}, "| coge", v["coge"], "| usos", {o: (u["n"], u["completados"], u["al_menos"]) for o, u in v["usos"].items()}, "| al acabar", {o: (a["creencia"], a["ignorancia"]) for o, a in v["al_acabar"].items()}, "| esperanza", v["esperanza_aparece"], "| pedidos", v["pedidos"], "| elige", v["elige"])

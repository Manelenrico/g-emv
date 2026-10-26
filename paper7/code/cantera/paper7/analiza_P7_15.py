"""[P7-15] DONDE PIERDE EL PUESTO EL QUE RECUERDA. Lectura de los diarios de los dos campos (P7-10: paintball/runs/P710_*; P7-14b: P714b_*), posterior a
los dos sellos y declarada asi. Coste cero: solo se leen diarios. Los identificadores del mundo se leen de cada diario (`mundo_leido`, `catalogo`,
`player_config`), no se cablean.
  python3 analiza_P7_15.py -> P7_15_vidas.json (una entrada por vida de los dos campos), P7_15_regalo.json (el regalo que nadie coge, P7-14b) y
                              P7_15_pedidos.json (los pedidos cerrados porque "lo ve", P7-14b)
POR VIDA (iguales para todos los brazos):
  - tic de la muerte y FASE del anillo en ese tic: cuantos encogimientos habian empezado ya (`player_config.zone_schedule`, columna del tic en que
    empieza a encoger); 0 = antes del primero;
  - parte de los tics vivos con la vida < 50 y < 30; parte de los tics FUERA del circulo (`zona` del tic);
  - PELEA: parte de los tics con algun rival a una o dos casillas (Chebyshev <= 2);
  - ZURRON: parte de los tics con al menos un botiquin, una racion, un arma (en la mano o en el zurron: `kind` ikMelee, ikRanged o ikThrown del
    catalogo) y municion (`ammo_ids`); media de botiquines a bordo; parte de los tics con el zurron lleno (ninguna ranura vacia);
  - DISTANCIA: casillas recorridas (suma de los cambios de casilla, Chebyshev) por cada 1.000 tics vivos.
EL REGALO QUE NADIE COGE (P7-14b): para cada regalo de APRENDE que vuelve a coger quien lo dio, los tics del hermano que pedia, entre el regalo y
  la recogida, en que esta ENCIMA (misma casilla) o AL LADO (Chebyshev 1) del botiquin regalado: su zurron, lo que hay en su casilla (en el orden
  del mundo), sus candidatos con su d, y si el arreglo del seis escondio `coger` ese tic (registro `llena8`).
LOS PEDIDOS QUE SE CIERRAN AL VER (P7-14b): para cada cierre con motivo "lo ve", si en los 30 segundos siguientes (30 x tick_rate tics) la criatura
  cogio un botiquin, y si lo cogio en una casilla donde veia un botiquin en el tic del cierre."""
import collections, glob, json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
ARMAS = ("ikMelee", "ikRanged", "ikThrown")
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def lee(f, completo=False):
    """Una pasada: los contadores de la vida; con `completo`, tambien la lista de tics (para el regalo y los pedidos)."""
    c = collections.Counter(); M = {"team": None, "slot": None, "kit": None, "rac": (), "ammo": (), "kind": {}, "zs": [], "rate": 24, "llena8": {}, "pidos": []}; T = []; prev = None; ult = None
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick":
            if r.get("phase") != "live": continue
            pos = tuple(r["pos"]); hp = float(r.get("hp") or 0); pack = r.get("pack") or []; ids = collections.Counter()
            for s in pack:
                if s: ids[s.get("id")] += int(s.get("n") or 1)
            mano = (r.get("hand") or {}).get("id") if isinstance(r.get("hand"), dict) else r.get("hand")
            z = r.get("zona") or {}; ce = z.get("center"); ra = z.get("radius")
            fuera = (((pos[0] - ce[0]) ** 2 + (pos[1] - ce[1]) ** 2) ** 0.5 > ra) if (ce is not None and ra is not None) else False
            riv = [tuple(a["pos"]) for a in (r.get("ve_agentes") or []) if a.get("team") != M["team"] and a.get("pos")]
            c["tics"] += 1; c["hp<50"] += hp < 50; c["hp<30"] += hp < 30; c["fuera"] += fuera; c["pelea"] += any(cheb(pos, q) <= 2 for q in riv)
            c["con_botiquin"] += ids.get(M["kit"], 0) >= 1; c["botiquines"] += ids.get(M["kit"], 0); c["con_racion"] += any(ids.get(i, 0) for i in M["rac"])
            c["con_arma"] += (M["kind"].get(mano) in ARMAS) or any(M["kind"].get(i) in ARMAS for i in ids); c["con_arma_en_la_mano"] += M["kind"].get(mano) in ARMAS
            c["con_municion"] += any(ids.get(i, 0) for i in M["ammo"]); c["zurron_lleno"] += bool(pack) and all(s for s in pack)
            if prev is not None: c["casillas"] += cheb(pos, prev)
            prev = pos; ult = r["tick"]
            if completo:
                R = r.get("RADIOGRAFIA") or {}
                T.append({"t": r["tick"], "pos": pos, "kits": ids.get(M["kit"], 0), "pack": [(s or {}).get("id") for s in pack], "do": (r.get("intencion") or {}).get("do"), "el": str(R.get("elegido") or ""),
                          "cand": {n_: (v_["d"] if isinstance(v_, dict) else v_) for n_, v_ in (R.get("candidatos") or {}).items()}, "aqui": [it.get("id") for it in (r.get("ve_items") or []) if tuple(it.get("pos") or ()) == pos],
                          "kitpos": [tuple(it["pos"]) for it in (r.get("ve_items") or []) if it.get("id") == M["kit"] and it.get("pos")]})
        elif k == "player_config": M["team"] = r.get("team"); M["slot"] = r.get("slot"); M["zs"] = r.get("zone_schedule") or []; M["rate"] = int(r.get("tick_rate") or 24)
        elif k == "mundo_leido": M["kit"] = r.get("id_botiquin"); M["rac"] = tuple(r.get("id_raciones") or ()); M["ammo"] = tuple(r.get("ammo_ids") or ())
        elif k == "catalogo" and not M["kind"]: M["kind"] = {it["id"]: it.get("kind") for it in r.get("items") or []}
        elif k == "llena8": M["llena8"][r.get("tick")] = r.get("motivo")
        elif k == "P7_pido": M["pidos"].append(r)
    n = max(1, c["tics"])
    out = {"tics": c["tics"], "ultimo_tick": ult, "fase_al_morir": sum(1 for z in M["zs"] if ult is not None and len(z) > 1 and z[1] <= ult), "fases": len(M["zs"]),
           "vida_menos_de_50": c["hp<50"] / n, "vida_menos_de_30": c["hp<30"] / n, "fuera_del_circulo": c["fuera"] / n, "pelea": c["pelea"] / n,
           "con_botiquin": c["con_botiquin"] / n, "botiquines_media": c["botiquines"] / n, "con_racion": c["con_racion"] / n, "con_arma": c["con_arma"] / n, "con_arma_en_la_mano": c["con_arma_en_la_mano"] / n,
           "con_municion": c["con_municion"] / n, "zurron_lleno": c["zurron_lleno"] / n, "casillas_por_1000_tics": 1000.0 * c["casillas"] / n}
    return (out, M, T) if completo else out

def una_carpeta(x):
    campo, carp = x; b = os.path.basename(carp).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]; out = {}
    for sl in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))
        if f: out[f"{campo}|s{serie}_d{dia}_{brazo}_{sl}"] = {"campo": campo, "serie": serie, "dia": dia, "brazo": brazo, "slot": sl, "semilla": int(b[4]), **lee(f[0])}
    return out

def regalo_y_pedidos(carp):
    """P7-14b, una partida de APRENDE (regalos) o de cualquier brazo (pedidos)."""
    b = os.path.basename(carp).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]
    V = json.load(open(os.path.join(AQUI, "P7_14b_vidas.json"))); L = {}
    for sl in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log")); L[sl] = lee(f[0], completo=True) if f else None
    escenas = []; cierres = []
    for sl in (10, 11):
        if L[sl] is None: continue
        _, M, T = L[sl]; v = V.get(f"s{serie}_d{dia}_{brazo}_{sl}") or {}
        # los pedidos cerrados porque "lo ve"
        porT = {t["t"]: i for i, t in enumerate(T)}
        for p in M["pidos"]:
            if p.get("cierra") != "lo ve": continue
            i = porT.get(p["tick"]); visto = set(T[i]["kitpos"]) if i is not None else set(); coge = None
            if i is not None:
                for a, bb in zip(T[i:], T[i + 1:]):
                    if bb["t"] - p["tick"] > 30 * M["rate"]: break
                    if a["do"] == "pickup" and bb["kits"] > a["kits"]: coge = {"tics": bb["t"] - p["tick"], "era_uno_de_los_que_veia": a["pos"] in visto}; break
            cierres.append({"brazo": brazo, "serie": serie, "dia": dia, "slot": sl, "tick": p["tick"], "veia": len(visto), "coge_en_30_s": coge is not None, "tics_hasta_cogerlo": (coge or {}).get("tics"), "era_uno_de_los_que_veia": (coge or {}).get("era_uno_de_los_que_veia"),
                            "vivio_los_30_s": bool(T and T[-1]["t"] - p["tick"] >= 30 * M["rate"])})
        # el regalo que nadie coge: yo soy quien DIO; el hermano es quien pedia
        if brazo != "APRENDE" or L[21 - sl] is None: continue
        _, Mh, Th = L[21 - sl]
        for g in v.get("regala") or []:
            if g.get("destino") != "lo recoge el mismo": continue
            p = tuple(g["pos"]); t0 = g["t"]; t1 = g["t"] + g["tics_hasta_recogerlo"]; e = {"vida_del_que_dio": f"s{serie}_d{dia}_{sl}", "t": t0, "espera": g["tics_hasta_recogerlo"], "tics": []}
            for t in Th:
                if not (t0 <= t["t"] <= t1): continue
                d = cheb(t["pos"], p)
                if d > 1: continue
                kid = Mh["kit"]; cand = t["cand"]; otros = {n_: x for n_, x in cand.items()}
                e["tics"].append({"t": t["t"], "donde": "encima" if d == 0 else "al lado", "kits": t["kits"], "zurron": t["pack"], "zurron_lleno": bool(t["pack"]) and all(t["pack"]), "aqui": t["aqui"], "el": t["el"], "cand": cand,
                                  "hay_coger": "coger" in cand, "coger_escondido": Mh["llena8"].get(t["t"]), "primero_de_la_casilla_es_el_botiquin": (bool(t["aqui"]) and t["aqui"][0] == kid),
                                  "hay_hacer_sitio": any(n_.startswith("hacer_sitio_") for n_ in cand), "hay_ir_a_por_objeto": [n_ for n_ in cand if n_ in ("ir_objeto", "ir_curioso")]})
            escenas.append(e)
    return escenas, cierres

if __name__ == "__main__":
    carps = [("P7-10", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s*_d*_*_*")))] + [("P7-14b", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d*_*_*")))]
    with Pool(8) as P:
        OUT = {}
        for o in P.imap_unordered(una_carpeta, carps): OUT.update(o)
        R = P.map(regalo_y_pedidos, [c for k, c in carps if k == "P7-14b"])
    json.dump(dict(sorted(OUT.items())), open(os.path.join(AQUI, "P7_15_vidas.json"), "w"), ensure_ascii=False, indent=0)
    json.dump([e for es, _ in R for e in es], open(os.path.join(AQUI, "P7_15_regalo.json"), "w"), ensure_ascii=False, indent=0)
    json.dump([c for _, cs in R for c in cs], open(os.path.join(AQUI, "P7_15_pedidos.json"), "w"), ensure_ascii=False, indent=0)
    print("vidas", len(OUT), "· regalos vueltos a coger", sum(len(es) for es, _ in R), "· cierres por «lo ve»", sum(len(cs) for _, cs in R))

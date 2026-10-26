"""[P7-16, parte A] LAS MUERTES TEMPRANAS, ESCENA A ESCENA. Lectura de los 640 diarios de los dos campos (P7-10 y P7-14b), posterior a los sellos.
Coste cero: solo se leen diarios. Identificadores del mundo leidos de cada diario.
  python3 analiza_P7_16.py -> P7_16_vidas.json

EL EPISODIO FINAL DE DANO de una vida que muere: hacia atras desde la muerte, los golpes (de rival o del anillo) seguidos sin un hueco de mas de
10 segundos (240 tics) entre uno y el siguiente. Empieza en el primer golpe de esa racha; "desde que vida" = la vida del tic anterior a ese golpe.

LOS TIPOS, declarados aqui ANTES de contar (se aplica el primero que cumpla, en este orden):
  1. ANILLO: en el episodio final el anillo hace mas dano que los rivales.
  2. CURANDOSE BAJO GOLPES: abrio el canal del botiquin dentro del episodio final y recibio dano de un rival con el canal abierto, o murio con el abierto.
  3. ESPERANDO CON BOTIQUIN: llevaba botiquin en el episodio final, tuvo el candidato de usarlo (`usar_botiquin` entre los candidatos) y eligio otra
     cosa durante al menos 1 segundo (24 tics), y no llego a abrir el canal en el episodio.
  4. EMBOSCADA: nada de lo anterior, y el episodio final dura 10 segundos o menos (240 tics): de entero a muerto sin tiempo.
  5. PELEA LARGA: nada de lo anterior, y el episodio final dura mas de 10 segundos.
  (6. OTRA: sin golpes registrados.)
Los umbrales (10 s, 1 s) son mios, puestos antes de contar; el de 10 s es la ventana que ya usaban P7-11 y P7-15.

ESPERAR (igual para los cuatro brazos): un tic con `usar_botiquin` entre los candidatos, otra cosa elegida y el canal cerrado.
ALEJARSE: con el rival mas cercano a 5 casillas o menos, un candidato de paso (`move_*` o `paso_*`) cuya direccion se aleja de ese rival (producto
escalar negativo con el vector hacia el). Se apunta si existia, si fue el elegido, y cuanto peor era su d que la del elegido.

LOS PRIMEROS 11.000 TICS de cada vida (para comparar brazos en las mismas semillas): parte de los tics con poca vida, con un rival a 1-2 casillas,
con un rival a la vista; rivales a la vista (media); distancia al centro del circulo y al hermano (medias); zurron; casillas recorridas; tics
esperando; dano recibido de rivales y del anillo por 1.000 tics; tics con `ir_curioso`, `ir_objeto` y `noop` elegidos."""
import collections, glob, json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
ARMAS = ("ikMelee", "ikRanged", "ikThrown"); DIR = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0), "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}
CORTE_LARGO = 12000; CORTE = 11000; VENTANA_S = 30; HUECO = 240; ESPERA_MIN = 24
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def med(xs):
    xs = sorted(xs); return xs[len(xs) // 2] if xs else None

def lee(f):
    M = {"team": None, "slot": None, "kit": None, "rac": (), "kind": {}, "rate": 24, "final": None}; T = []
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick":
            if r.get("phase") != "live": continue
            pos = tuple(r["pos"]); pack = r.get("pack") or []; ids = collections.Counter()
            for s in pack:
                if s: ids[s.get("id")] += int(s.get("n") or 1)
            mano = (r.get("hand") or {}).get("id") if isinstance(r.get("hand"), dict) else r.get("hand")
            z = r.get("zona") or {}; ce = z.get("center"); R = r.get("RADIOGRAFIA") or {}; soc = r.get("social") or {}
            T.append({"t": r["tick"], "pos": pos, "hp": float(r.get("hp") or 0), "kits": ids.get(M["kit"], 0), "rac": any(ids.get(i, 0) for i in M["rac"]), "arma": (M["kind"].get(mano) in ARMAS) or any(M["kind"].get(i) in ARMAS for i in ids),
                      "lleno": bool(pack) and all(s for s in pack), "canal": any(e.get("id") == "channeling" and e.get("item") == M["kit"] for e in (r.get("effects") or [])),
                      "riv": [(a.get("slot"), tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("team") != M["team"] and a.get("pos")],
                      "dmg": [(str(d.get("source") or ""), float(d.get("amount") or 0)) for d in (r.get("damage_taken") or [])], "el": str(R.get("elegido") or ""),
                      "cand": {n_: (v_["d"] if isinstance(v_, dict) else v_) for n_, v_ in (R.get("candidatos") or {}).items()},
                      "centro": (((pos[0] - ce[0]) ** 2 + (pos[1] - ce[1]) ** 2) ** 0.5 if ce is not None else None), "herm": soc.get("dist_pareja")})
        elif k == "player_config": M["team"] = r.get("team"); M["slot"] = r.get("slot"); M["rate"] = int(r.get("tick_rate") or 24)
        elif k == "mundo_leido": M["kit"] = r.get("id_botiquin"); M["rac"] = tuple(r.get("id_raciones") or ())
        elif k == "catalogo" and not M["kind"]: M["kind"] = {it["id"]: it.get("kind") for it in r.get("items") or []}
        elif k == "final": M["final"] = r
    return M, T

def espera(t): return ("usar_botiquin" in t["cand"]) and t["el"] != "usar_botiquin" and not t["canal"]

def primeros(T):
    X = [t for t in T if t["t"] <= CORTE]; n = max(1, len(X)); cas = sum(cheb(a["pos"], b["pos"]) for a, b in zip(X, X[1:]))
    dr = sum(a for t in X for s, a in t["dmg"] if s.startswith("P")); dz = sum(a for t in X for s, a in t["dmg"] if s == "zone")
    ce = [t["centro"] for t in X if t["centro"] is not None]; he = [t["herm"] for t in X if t["herm"] is not None]
    return {"tics": len(X), "vida_menos_de_50": sum(1 for t in X if t["hp"] < 50) / n, "rival_a_1_o_2": sum(1 for t in X if any(cheb(t["pos"], q) <= 2 for _, q in t["riv"])) / n, "rival_a_la_vista": sum(1 for t in X if t["riv"]) / n,
            "rivales_a_la_vista_media": sum(len(t["riv"]) for t in X) / n, "dist_al_centro": (sum(ce) / len(ce) if ce else None), "dist_al_hermano": (sum(he) / len(he) if he else None),
            "con_botiquin": sum(1 for t in X if t["kits"] >= 1) / n, "con_racion": sum(1 for t in X if t["rac"]) / n, "con_arma": sum(1 for t in X if t["arma"]) / n, "zurron_lleno": sum(1 for t in X if t["lleno"]) / n,
            "casillas_por_1000_tics": 1000.0 * cas / n, "esperando": sum(1 for t in X if espera(t)) / n, "dano_rival_por_1000_tics": 1000.0 * dr / n, "dano_anillo_por_1000_tics": 1000.0 * dz / n,
            "ir_curioso": sum(1 for t in X if t["el"] == "ir_curioso") / n, "ir_objeto": sum(1 for t in X if t["el"] == "ir_objeto") / n, "noop": sum(1 for t in X if t["el"] == "noop") / n,
            "en_canal": sum(1 for t in X if t["canal"]) / n, "golpes_de_rival": sum(1 for t in X for s, a in t["dmg"] if s.startswith("P"))}

def escena(M, T):
    ult = T[-1]["t"]; W = [t for t in T if t["t"] >= ult - VENTANA_S * M["rate"]]
    golpes = [(i, t["t"]) for i, t in enumerate(T) if any(s.startswith("P") or s == "zone" for s, _ in t["dmg"])]
    if golpes:
        j = len(golpes) - 1
        while j > 0 and golpes[j][1] - golpes[j - 1][1] <= HUECO: j -= 1
        i0 = golpes[j][0]
    else: i0 = None
    Ep = T[i0:] if i0 is not None else []
    out = {"ventana_30_s": {"rivales_distintos": len({s for t in W for s, _ in t["riv"]}), "dist_minima_a_un_rival": min((cheb(t["pos"], q) for t in W for _, q in t["riv"]), default=None),
                            "tics_con_rival_a_2_o_menos": sum(1 for t in W if any(cheb(t["pos"], q) <= 2 for _, q in t["riv"])), "tics_con_rival_a_5_o_menos": sum(1 for t in W if any(cheb(t["pos"], q) <= 5 for _, q in t["riv"])),
                            "rivales_a_la_vista_al_morir": len(T[-1]["riv"]), "tics": len(W), "tics_esperando": sum(1 for t in W if espera(t)), "tics_en_canal": sum(1 for t in W if t["canal"])}}
    if not Ep: out["tipo"] = "otra"; out["episodio"] = None; return out
    dr = sum(a for t in Ep for s, a in t["dmg"] if s.startswith("P")); dz = sum(a for t in Ep for s, a in t["dmg"] if s == "zone")
    # el canal dentro del episodio
    aper = []; v = None
    for t in Ep:
        if v is None and t["canal"]: v = {"t0": t["t"], "kits0": t["kits"], "dano_rival": 0.0}
        if v is not None and t["canal"]: v["dano_rival"] += sum(a for s, a in t["dmg"] if s.startswith("P"))
        if v is not None and not t["canal"]: v["gastado"] = t["kits"] < v["kits0"]; v["t_fin"] = t["t"]; aper.append(v); v = None
    abierto_al_morir = v is not None
    if v is not None: v["gastado"] = False; v["t_fin"] = None; aper.append(v)
    esp = [t for t in Ep if espera(t)]
    gap_usar = [t["cand"]["usar_botiquin"] - t["cand"][t["el"]] for t in esp if t["el"] in t["cand"]]
    # alejarse
    cerca = 0; con_cand = 0; elegido_alejarse = 0; gaps = []
    for t in Ep:
        if not t["riv"]: continue
        q = min((q for _, q in t["riv"]), key=lambda q: cheb(t["pos"], q))
        if cheb(t["pos"], q) > 5: continue
        cerca += 1; vx, vy = q[0] - t["pos"][0], q[1] - t["pos"][1]
        lejos = [n_ for n_ in t["cand"] if n_.startswith(("move_", "paso_")) and n_.split("_", 1)[1] in DIR and (DIR[n_.split("_", 1)[1]][0] * vx + DIR[n_.split("_", 1)[1]][1] * vy) < 0]
        if lejos:
            con_cand += 1
            if t["el"] in lejos: elegido_alejarse += 1
            if t["el"] in t["cand"]: gaps.append(min(t["cand"][n_] for n_ in lejos) - t["cand"][t["el"]])
    ep = {"empieza_en_el_tic": Ep[0]["t"], "dura_tics": ult - Ep[0]["t"], "desde_la_vida": (T[i0 - 1]["hp"] if i0 and i0 > 0 else Ep[0]["hp"]), "dano_de_rivales": round(dr, 1), "dano_del_anillo": round(dz, 1),
          "botiquines_al_empezar": Ep[0]["kits"], "botiquines_al_morir": Ep[-1]["kits"], "llevo_botiquin_en_el_episodio": any(t["kits"] >= 1 for t in Ep),
          "aperturas_del_canal": len(aper), "canales_gastados": sum(1 for a in aper if a["gastado"]), "canales_cortados": sum(1 for a in aper if not a["gastado"] and a["t_fin"] is not None), "canal_abierto_al_morir": abierto_al_morir,
          "dano_de_rival_con_el_canal_abierto": round(sum(a["dano_rival"] for a in aper), 1), "tics_esperando": len(esp), "d_de_usar_menos_la_del_elegido_mediana": med(gap_usar),
          "tics_con_rival_a_5_o_menos": cerca, "tics_con_candidato_de_alejarse": con_cand, "tics_en_que_eligio_alejarse": elegido_alejarse, "d_de_alejarse_menos_la_del_elegido_mediana": med(gaps),
          "tics_en_que_alejarse_empataba_o_ganaba": sum(1 for g in gaps if g <= 1e-9)}
    if dz > dr: tipo = "anillo"
    elif aper and (ep["dano_de_rival_con_el_canal_abierto"] > 0 or abierto_al_morir): tipo = "curandose bajo golpes"
    elif ep["llevo_botiquin_en_el_episodio"] and len(esp) >= ESPERA_MIN and not aper: tipo = "esperando con botiquin"
    elif ep["dura_tics"] <= HUECO: tipo = "emboscada"
    else: tipo = "pelea larga"
    out["episodio"] = ep; out["tipo"] = tipo; return out

def una_carpeta(x):
    campo, carp = x; b = os.path.basename(carp).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = b[3]; out = {}
    for sl in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))
        if not f: continue
        M, T = lee(f[0])
        if not T: continue
        murio = (M["final"] or {}).get("reason") == "eliminated"
        v = {"campo": campo, "serie": serie, "dia": dia, "brazo": brazo, "slot": sl, "semilla": int(b[4]), "ultimo_tick": T[-1]["t"], "murio": murio, "puesto": (M["final"] or {}).get("placement"),
             "esperando_toda_la_vida": sum(1 for t in T if espera(t)) / len(T), "tics_esperando_toda_la_vida": sum(1 for t in T if espera(t)), "primeros": primeros(T)}
        if murio and T[-1]["t"] < CORTE_LARGO: v["escena"] = escena(M, T)
        out[f"{campo}|s{serie}_d{dia}_{brazo}_{sl}"] = v
    return out

if __name__ == "__main__":
    carps = [("P7-10", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s*_d*_*_*")))] + [("P7-14b", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d*_*_*")))]
    OUT = {}
    with Pool(4) as P:
        for o in P.imap_unordered(una_carpeta, carps): OUT.update(o)
    # "esperar en vez de usar" medido en el banco de P7-15 (solo APRENDE de P7-14b): tics de los ultimos 30 s con `noop` con el cuaderno y `usar_botiquin` sin el
    f15 = os.path.join(AQUI, "P7_15_decisiones.json")
    if os.path.exists(f15):
        for r in json.load(open(f15)):
            v = OUT.get(f"P7-14b|s{r['serie']}_d{r['dia']}_APRENDE_{r['slot']}")
            if v and "escena" in v: v["escena"]["banco_P7_15_quieto_en_vez_de_usar_en_30_s"] = sum(1 for x in r["distintos"] if x["t"] >= v["ultimo_tick"] - VENTANA_S * 24 and x["con_cuaderno"] == "noop" and x["sin_los_dias_anteriores"] == "usar_botiquin")
    json.dump(dict(sorted(OUT.items())), open(os.path.join(AQUI, "P7_16_vidas.json"), "w"), ensure_ascii=False, indent=0)
    print("vidas", len(OUT), "· con escena (mueren antes de 12.000):", sum(1 for v in OUT.values() if "escena" in v))

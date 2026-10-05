"""[P6-20 · ampliacion B] «DEBIL Y ACORRALADO»: SOLO CONTAR, SIN CONSTRUIR.
SOLO LECTURA de los 200 diarios del mundo del seis (A3, A4, A5v, A5h, A6), de uno en uno.

Un CASO es una racha de tics (huecos <= 24 tics se funden) en la que el cuerpo esta A LA VEZ:
  · debil: vida por debajo de lo que aguanta un golpe de espada o de lanza. Umbral = dano
    tipico por golpe de P6-19 (`golpes.dano_por_golpe_por_arma`: espada 13,21 / lanza 9,83):
    «debil» = hp <= 13,21 (un golpe de espada lo mata); ademas se cuenta el subconjunto
    hp <= 9,83 (uno de lanza lo mata);
  · sin escapatoria: ninguna casilla alcanzable en <= 3 pasos (BFS sobre casillas no solidas
    del mapa estatico, sin cuerpos) que (i) aleje al cuerpo del rival mas cercano armado
    (distancia Chebyshev al rival mayor que la actual) y (ii) no lo meta en el fuego
    (distancia al centro <= radio del anillo en ese tic, `mundo.anillo_en`); si el cuerpo ya
    esta en el fuego, (ii) se relaja a «no mas lejos del centro que ahora»;
  · con un rival CON ARMA acercandose a distancia de golpe: rival visto o contado con arma
    del catalogo de alcance > 0 (la mano vacia NO cuenta), a distancia Chebyshev <= alcance,
    y que se ha acercado (distancia menor que la ultima vez que se le vio, <= 24 tics antes;
    si es la primera vez que se le ve, cuenta como acercandose).
Por caso: brazo, tics, arma del rival, distancia minima, si llevabamos arma (mano != none),
que hizo el cuerpo (familias de `elegido`: pega / se mueve / quieto), y el desenlace: golpe
recibido de ese rival en el caso o en los 96 tics siguientes, muerte en los 96 tics
siguientes y su causa (P6-16: golpes de rival o anillo en los ultimos 48 tics).
"""
import collections, glob, json, math, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U, parte2 as P2, oyente2 as OY
C = (24, 24); PASOS = 3; HUECO = 24; VENT = 96
_T = json.load(open(os.path.join(AQUI, "P6_19_tasas.json")))["golpes"]["dano_por_golpe_por_arma"]
UMBRAL_ESPADA = _T["sword"]["media"]; UMBRAL_LANZA = _T["spear"]["media"]
BRAZOS = {"A3": "paintball/runs/P610_t*_A3_*", "A4": "paintball/runs/P611_t*_A4_*", "A5v": "paintball/runs/P616_t1_A5v_*", "A5h": "paintball/runs/P616_t2_A5h_*", "A6": "paintball/runs/P618_t1_A6_*"}
DIRS8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def fam(el):
    if not el or el == "noop":
        return "quieto"
    if el.startswith("atacar"):
        return "pega"
    if el.startswith(("move", "paso", "ir_", "_FM_ir")):
        return "se mueve"
    if el == "_FM_quedarse":
        return "sujeto"
    return el.split("_")[0]


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); cat = next(r for r in recs if r["k"] == "catalogo")
    sm = next(r for r in recs if r["k"] == "static_map"); mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    fin = next((r for r in recs if r.get("k") == "final"), None)
    armas = {it["id"]: int(it.get("range") or 0) for it in cat["items"] if float(it.get("damage") or 0) > 0 and int(it.get("range") or 0) > 0}
    T = {}; ult = None; herm = pc["teammate_slot"]
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        for m in (r.get("chat") or []):
            if m.get("channel") == "team" and m.get("from") == herm and (m.get("text") or "").startswith("E2 "):
                pp = P2.parsea(m["text"], mundo)
                if pp:
                    ult = pp
        t = r["tick"]
        vis = {int(a["slot"]): ((int(a["pos"][0]), int(a["pos"][1])), ((a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand")) or "none") for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") is not None}
        if ult and 0 <= t - ult["t"] <= OY.CADUCIDAD_RIVAL:
            for x in ult["rivales"]:
                if x["slot"] not in vis:
                    vis[int(x["slot"])] = (tuple(x["pos"]), (x.get("arma") or "none"))
        h = r.get("hand"); hid = (h.get("id") if isinstance(h, dict) else h) or "none"
        T[t] = {"pos": tuple(int(x) for x in r["pos"]), "hp": float(r.get("hp") if r.get("hp") is not None else 100), "hand": hid,
                "dt": {str(g.get("source")): float(g.get("amount") or 0) for g in (r.get("damage_taken") or []) if isinstance(g, dict)},
                "riv": {s: v for s, v in vis.items() if s not in (pc["slot"], herm)}, "el": str((r.get("RADIOGRAFIA") or {}).get("elegido") or "")}
    del recs
    return pc, T, fin, armas, mundo


def alcanzables(mundo, pos, pasos):
    vist = {pos}; frente = [pos]
    for _ in range(pasos):
        nuevo = []
        for p in frente:
            for dx, dy in DIRS8:
                q = (p[0] + dx, p[1] + dy)
                if q not in vist and not mundo.solido(q[0], q[1]):
                    vist.add(q); nuevo.append(q)
        frente = nuevo
    vist.discard(pos)
    return vist


def escapatoria(mundo, pos, riv_pos, radio):
    d0 = cheb(pos, riv_pos); dc0 = math.dist(pos, C)
    for q in alcanzables(mundo, pos, PASOS):
        if cheb(q, riv_pos) <= d0:
            continue
        dq = math.dist(q, C)
        if dq <= radio or (dc0 > radio and dq <= dc0):
            return True
    return False


def causa_muerte(T, fin):
    if not (fin and fin.get("reason") == "eliminated"):
        return None
    tl = sorted(T); mt = int(fin.get("match_ticks") or tl[-1])
    golpes = [t for t in tl if mt - 48 <= t <= mt and any(s.startswith("P") for s in T[t]["dt"])]
    zt = [t for t in tl if mt - 48 <= t <= mt and "zone" in T[t]["dt"]]
    if golpes and (not zt or golpes[-1] >= max(zt)):
        return "rival"
    return "anillo" if zt else "no consta"


CASOS = []; TICS = collections.Counter(); n_vidas = 0
for brazo, pat in BRAZOS.items():
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        for sl in (10, 11):
            pc, T, fin, armas, mundo = carga(fs[sl]); ts = sorted(T); mt = max(T); n_vidas += 1
            cm = causa_muerte(T, fin); ultimo = {}; abierto = None
            for t in ts:
                r = T[t]; pos = r["pos"]; TICS["vivos"] += 1
                debil = r["hp"] <= UMBRAL_ESPADA
                TICS["debil"] += debil
                # rivales armados a tiro y acercandose
                amen = []
                for s, (q, w) in r["riv"].items():
                    if w in armas:
                        d = cheb(pos, q); u = ultimo.get(s)
                        acerca = (u is None) or (t - u[0] > HUECO) or (d < u[1])
                        if d <= armas[w] and acerca:
                            amen.append((d, s, w, q))
                for s, (q, w) in r["riv"].items():
                    ultimo[s] = (t, cheb(pos, q))
                if amen:
                    TICS["armado_a_tiro_acercandose"] += 1
                    if debil:
                        TICS["debil_y_armado_a_tiro"] += 1
                if not (debil and amen):
                    if abierto is not None and t - abierto["t_fin"] > HUECO:
                        CASOS.append(abierto); abierto = None
                    continue
                _c, radio, _dps = mundo.anillo_en(t)
                d, s, w, q = min(amen)
                if escapatoria(mundo, pos, q, radio):
                    TICS["debil_armado_con_escapatoria"] += 1
                    if abierto is not None and t - abierto["t_fin"] > HUECO:
                        CASOS.append(abierto); abierto = None
                    continue
                TICS["debil_y_acorralado"] += 1
                if abierto is None or t - abierto["t_fin"] > HUECO:
                    if abierto is not None:
                        CASOS.append(abierto)
                    abierto = {"brazo": brazo, "semilla": int(carp.rsplit("_", 1)[1]), "slot": sl, "t0": t, "t_fin": t, "tics": 0, "hp0": r["hp"], "hp_min": r["hp"], "lanza_mata": False, "rivales": set(), "armas": collections.Counter(),
                               "d_min": d, "llevaba_arma": r["hand"] != "none", "arma_propia": r["hand"], "hizo": collections.Counter(), "golpe_en_caso": 0.0, "golpe_96": 0.0, "muere_96": False, "causa_muerte": None, "en_fuego": math.dist(pos, C) > radio}
                abierto["t_fin"] = t; abierto["tics"] += 1; abierto["hp_min"] = min(abierto["hp_min"], r["hp"]); abierto["lanza_mata"] |= (r["hp"] <= UMBRAL_LANZA)
                abierto["rivales"].add(s); abierto["armas"][w] += 1; abierto["d_min"] = min(abierto["d_min"], d); abierto["hizo"][fam(r["el"])] += 1
                abierto["golpe_en_caso"] += sum(a for src, a in r["dt"].items() if src.startswith("P"))
            if abierto is not None:
                CASOS.append(abierto)
            for c in [c for c in CASOS if c["brazo"] == brazo and c["slot"] == sl and c["semilla"] == int(carp.rsplit("_", 1)[1])]:
                if "cerrado" in c:
                    continue
                c["cerrado"] = True
                c["golpe_96"] = sum(a for u in ts if c["t_fin"] < u <= c["t_fin"] + VENT for src, a in T[u]["dt"].items() if src.startswith("P"))
                c["golpe_de_esos_rivales_96"] = sum(a for u in ts if c["t0"] <= u <= c["t_fin"] + VENT for src, a in T[u]["dt"].items() if src.startswith("P") and int(src[1:]) in c["rivales"])
                c["muere_96"] = bool(fin and fin.get("reason") == "eliminated" and mt <= c["t_fin"] + VENT); c["causa_muerte"] = cm if c["muere_96"] else None
                c["rivales"] = sorted(c["rivales"]); c["armas"] = dict(c["armas"]); c["hizo"] = dict(c["hizo"])
            del T
        print(f"  {brazo} {os.path.basename(carp)}: casos {sum(1 for c in CASOS if c['brazo'] == brazo)}", flush=True)


def cuenta(S):
    return {"casos": len(S), "vidas": len({(c["brazo"], c["semilla"], c["slot"]) for c in S}), "tics_mediana": (sorted(c["tics"] for c in S)[len(S) // 2] if S else None),
            "lanza_lo_mata": sum(1 for c in S if c["lanza_mata"]), "acaban_en_golpe (de esos rivales, en el caso o 96 tics)": sum(1 for c in S if c["golpe_de_esos_rivales_96"] > 0),
            "acaban_en_muerte_96": sum(1 for c in S if c["muere_96"]), "causa_muerte": dict(collections.Counter(c["causa_muerte"] for c in S if c["muere_96"])),
            "llevabamos_arma": sum(1 for c in S if c["llevaba_arma"]), "arma_propia": dict(collections.Counter(c["arma_propia"] for c in S)),
            "arma_del_rival": dict(sum((collections.Counter(c["armas"]) for c in S), collections.Counter())), "ya_en_el_fuego": sum(1 for c in S if c["en_fuego"]),
            "hizo (tics por familia)": dict(sum((collections.Counter(c["hizo"]) for c in S), collections.Counter())),
            "hizo_con_arma (tics)": dict(sum((collections.Counter(c["hizo"]) for c in S if c["llevaba_arma"]), collections.Counter())),
            "pega_alguna_vez_con_arma": sum(1 for c in S if c["llevaba_arma"] and c["hizo"].get("pega", 0) > 0),
            "con_arma: acaban en golpe / muerte": [sum(1 for c in S if c["llevaba_arma"] and c["golpe_de_esos_rivales_96"] > 0), sum(1 for c in S if c["llevaba_arma"] and c["muere_96"])],
            "sin_arma: acaban en golpe / muerte": [sum(1 for c in S if not c["llevaba_arma"] and c["golpe_de_esos_rivales_96"] > 0), sum(1 for c in S if not c["llevaba_arma"] and c["muere_96"])]}


R = {"nota": "P6-20 ampliacion B. SOLO CONTAR. Umbrales de P6-19 (dano tipico por golpe): espada %.2f, lanza %.2f; pasos %d; hueco %d; ventana %d." % (UMBRAL_ESPADA, UMBRAL_LANZA, PASOS, HUECO, VENT),
     "vidas": n_vidas, "tics": dict(TICS), "total": cuenta(CASOS), "por_brazo": {b: cuenta([c for c in CASOS if c["brazo"] == b]) for b in BRAZOS}, "casos": CASOS}
json.dump(R, open(os.path.join(AQUI, "P6_20_acorralado.json"), "w"), ensure_ascii=False, indent=1, default=str)
print("vidas", n_vidas, "tics", dict(TICS)); print("TOTAL", json.dumps(R["total"], ensure_ascii=False))
for b in BRAZOS:
    print(b, json.dumps(R["por_brazo"][b], ensure_ascii=False))
print("-> P6_20_acorralado.json")

"""[P6-17] EL FINAL DE LA PARTIDA POR DENTRO: ruido, palancas y las estrategias.
SOLO LECTURA. 60 partidas (A4, A5v, A5h), 120 diarios, y el player_config.
Las partidas se leen DE UNA EN UNA (regla de memoria); nada se acumula salvo
los recuentos.

    python3 mide_final_P6_17.py

Definiciones (declaradas):
  · «dentro» = distancia euclidea al centro <= r1 de la fase activa (la casilla
    sigue a salvo en toda la fase); «fuera» = lo contrario; «arde» = distancia
    al centro > `zona.radius` del tic.
  · «la fase que mata»: se hace la anatomia para cada fase (1-7) y cada vida
    viva en su `warn`; el informe mira las fases 5 y 6, que son las que matan.
  · «junto» = distancia Chebyshev al hermano <= 3 (posiciones reales de los dos
    diarios); «solo» = > 3 o hermano muerto.
  · rivales dentro del circulo = asientos ajenos vistos por CUALQUIERA de los
    dos hermanos en ese tic con distancia al centro <= r1 (cota inferior: solo
    lo visto); «armado» = mano con arma de dano > 0 del catalogo.
  · golpe = `damage_taken` con `source` P<slot> (rival) o `zone` (anillo);
    «quien lo mato» = las fuentes de los 48 tics antes de morir.
  · sobrevive la fase = vivo en el `warn` de la fase siguiente (o al final).
  · pega = `elegido` empieza por `atacar_<dir>` y el rival esta en la linea de
    esa direccion a <= alcance del arma en mano (melee: adyacente).
  · el agresor «muere» = `death_fireworks` con su asiento; «se va» = ninguno de
    los dos lo ve a <= 8 durante 48 tics seguidos; «deja de pegar» = ningun
    golpe suyo a los dos en los 100 tics siguientes.
  · ruido: por semilla, diferencias emparejadas (A5x - A4) y test de permutacion
    por cambio de signo (exacto, 2^20) y remuestreo (10.000) de la media.
"""
import collections, glob, json, math, os, re, statistics as st, sys
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
DIRS8 = list(DIRS.values())
BRAZOS = {"A4": "paintball/runs/P611_t*_A4_*", "A5v": "paintball/runs/P616_t1_A5v_*", "A5h": "paintball/runs/P616_t2_A5h_*"}
TIC_MS = 1000.0 / 24.0
C = (24, 24)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def bfs_seguro(mundo, desde, r1):
    """mide_anillo_P6_13, tal cual."""
    n = mundo.arena_size; c = (n // 2, n // 2)
    def segura(p): return math.dist(p, c) <= r1 and not mundo.solido(p[0], p[1])
    if segura(desde):
        return 0
    vis = {desde}; frente = [desde]; k = 0
    while frente:
        k += 1; nuevo = []
        for (x, y) in frente:
            for dx, dy in DIRS8:
                q = (x + dx, y + dy)
                if not (0 <= q[0] < n and 0 <= q[1] < n) or q in vis or mundo.solido(q[0], q[1]):
                    continue
                if segura(q):
                    return k
                vis.add(q); nuevo.append(q)
        frente = nuevo
    return None


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    fin = next((r for r in recs if r.get("k") == "final"), None)
    armas = {it["id"]: (float(it.get("damage") or 0), int(it.get("range") or 1), it.get("kind")) for it in cat["items"] if float(it.get("damage") or 0) > 0}
    curas = {it["id"]: (float(it.get("heal") or 0), int(it.get("use_ticks") or 1)) for it in cat["items"] if it.get("heal")}
    T = {}; L = collections.defaultdict(list); muertes = {}
    for r in recs:
        k = r.get("k")
        if k in ("oraculo16", "forma_aceptada", "compromiso6", "forma_caida", "forma_evaluada"):
            L[k].append(r)
        if k != "tick" or r.get("phase") != "live":
            continue
        for e in (r.get("eventos") or []):
            if e.get("type") == "death_fireworks" and e.get("slot") is not None:
                muertes.setdefault(int(e["slot"]), r["tick"])
        ra = r.get("RADIOGRAFIA") or {}
        h = r.get("hand"); hid = (h.get("id") if isinstance(h, dict) else h) or "none"
        T[r["tick"]] = {"pos": tuple(int(x) for x in r["pos"]), "hp": float(r.get("hp") if r.get("hp") is not None else 100), "hand": hid,
                        "el": str(ra.get("elegido") or ""), "dt": [g for g in (r.get("damage_taken") or []) if isinstance(g, dict)],
                        "radio": float((r.get("zona") or {}).get("radius") or 48), "ar": (r.get("action_result_obs", r.get("action_result"))),
                        "listas": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0, "atk": int(r.get("attack_ready_in") or 0) == 0,
                        "ve": {int(a["slot"]): ((int(a["pos"][0]), int(a["pos"][1])), ((a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand")) or "none") for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") is not None},
                        "ahora": {kk: vv.get("M", 0.0) for kk, vv in ((ra.get("ahora") or {}).get("filas") or {}).items()} if isinstance(ra, dict) else {},
                        "cs": (ra.get("candidatos") if isinstance(ra, dict) and isinstance((ra.get("candidatos") or {}).get("noop"), dict) else None),
                        "ms16": (ra.get("ms16") if isinstance(ra, dict) else None)}
    del recs
    return {"pc": pc, "fin": fin, "armas": armas, "curas": curas, "T": T, "L": L, "muertes": muertes, "slot": pc["slot"], "herm": pc["teammate_slot"],
            "fases": [tuple(z) for z in (pc.get("zone_schedule") or [])], "tick_rate": int(pc.get("tick_rate") or 24), "mundo": U.mundo_de(pc, list(sm["filas"]), cat["items"])}


def fase_en(fases, t):
    k = None
    for i, f in enumerate(fases):
        if f[0] <= t:
            k = i
    return k


def r1_en(fases, t):
    k = fase_en(fases, t)
    return 48.0 if k is None else float(fases[k][4])


def dentro(pos, fases, t):
    return math.dist(pos, C) <= r1_en(fases, t)


def arde(pos, radio):
    return math.dist(pos, C) > radio


def pega_a(Tb, t, slot_r, RIV, armas):
    r = Tb.get(t)
    if not r or not r["el"].startswith("atacar_"):
        return False
    d = r["el"][7:]
    if d not in DIRS:
        return False
    q = RIV.get(t, {}).get(slot_r)
    if not q:
        return False
    dx, dy = DIRS[d]; alc = armas[r["hand"]][1] if r["hand"] in armas else 1
    return any((r["pos"][0] + dx * k, r["pos"][1] + dy * k) == q[0] for k in range(1, alc + 1))


def causa_de(V, mt):
    T = V["T"]; fuentes = collections.Counter(); arma = {}
    for t in range(mt - 48, mt + 1):
        r = T.get(t)
        if not r:
            continue
        for g in r["dt"]:
            s = str(g.get("source")); fuentes[s] += float(g.get("amount") or 0)
            if s.startswith("P"):
                v = r["ve"].get(int(s[1:]))
                if v:
                    arma[s] = v[1]
    return dict(fuentes), arma


def causa_simple(V, mt):
    fu, _ = causa_de(V, mt)
    rival = any(k.startswith("P") for k in fu); zona = "zone" in fu
    T = V["T"]
    ult_r = max((t for t in range(mt - 48, mt + 1) if t in T for g in T[t]["dt"] if str(g.get("source")).startswith("P")), default=None)
    ult_z = max((t for t in range(mt - 48, mt + 1) if t in T for g in T[t]["dt"] if g.get("source") == "zone"), default=None)
    if rival and (not zona or (ult_r or 0) >= (ult_z or 0)):
        return "rival"
    if zona:
        return "anillo"
    return "no consta"


def partidas():
    for brazo, pat in BRAZOS.items():
        for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
            fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
            if len(fs) != 2:
                continue
            sem = int(carp.rsplit("_", 1)[1])
            G = {sl: carga(fs[sl]) for sl in (10, 11)}
            RIV = collections.defaultdict(dict)
            for sl in (10, 11):
                for t, r in G[sl]["T"].items():
                    for s, v in r["ve"].items():
                        if s not in (10, 11):
                            RIV[t][s] = v
            G["RIV"] = RIV
            G["muertes"] = dict(G[10]["muertes"]); G["muertes"].update(G[11]["muertes"])
            yield (brazo, sem), G
            del G


# ═════════ acumuladores ═════════
POR_SEM = collections.defaultdict(dict)
LENT = {b: {"tics_lentos": 0, "tics": 0, "muertes_rival": 0, "muertes_rival_a_60_tics_de_un_lento": 0, "esperadas_al_azar": 0.0, "detalle": []} for b in ("A5v", "A5h")}
ANAT = []; AND = []; CUR = []; SAL = []; DEF = []
FILAS_NO = collections.defaultdict(list); FILAS_SI = collections.defaultdict(list); NDET = [0, 0]
FASES = None; TR = 24


# ═════════ 1 · ruido, por partida ═════════
def sec1(b, s, G):
    v = {"supervivientes": 0, "rival": 0, "anillo": 0, "vida": 0, "los_dos": 0}
    for sl in (10, 11):
        V = G[sl]; fin = V["fin"] or {}; mt = max(V["T"]); v["vida"] += mt
        if fin.get("reason") != "eliminated":
            v["supervivientes"] += 1
        else:
            c = causa_simple(V, mt)
            if c in ("rival", "anillo"):
                v[c] += 1
    v["los_dos"] = int(v["supervivientes"] == 2)
    POR_SEM[s][b] = v
    if b in LENT:
        for sl in (10, 11):
            V = G[sl]; T = V["T"]; fin = V["fin"] or {}; mt = max(T)
            lentos = sorted(t for t, r in T.items() if (r["ms16"] or 0) > TIC_MS)
            LENT[b]["tics_lentos"] += len(lentos); LENT[b]["tics"] += len(T)
            if fin.get("reason") == "eliminated" and causa_simple(V, mt) == "rival":
                LENT[b]["muertes_rival"] += 1
                prev = [t for t in lentos if t <= mt]; dl = (mt - prev[-1]) if prev else None
                LENT[b]["detalle"].append({"semilla": s, "slot": sl, "muerte": mt, "ultimo_lento": (prev[-1] if prev else None), "tics_desde_lento": dl})
                LENT[b]["muertes_rival_a_60_tics_de_un_lento"] += int(dl is not None and dl <= 60)
                LENT[b]["esperadas_al_azar"] += min(1.0, 60.0 * len(lentos) / max(1, len(T)))


# ═════════ 2 · anatomia del final, por partida ═════════
def sec2(b, s, G):
    RIV = G["RIV"]
    for sl in (10, 11):
        V = G[sl]; T = V["T"]; To = G[21 - sl]["T"]; mt = max(T); fin = V["fin"] or {}
        for i, (warn, shrink, done, r0, r1, dps) in enumerate(FASES):
            if warn not in T:
                continue
            sig = FASES[i + 1][0] if i + 1 < len(FASES) else 10 ** 9
            ventana = [t for t in sorted(T) if warn <= t < sig]
            d = {"brazo": b, "semilla": s, "slot": sl, "fase": i + 1, "warn": warn, "r1": r1, "hp_warn": T[warn]["hp"]}
            d["dentro_en_warn"] = math.dist(T[warn]["pos"], C) <= r1
            ent = next((t for t in ventana if math.dist(T[t]["pos"], C) <= r1), None)
            d["entra"] = ent; d["entra_cuando"] = (None if ent is None else ("antes de shrink" if ent <= shrink else ("durante el encogimiento" if ent <= done else "despues de done")))
            d["junto_en_warn"] = (warn in To and cheb(T[warn]["pos"], To[warn]["pos"]) <= 3); d["hermano_vivo_en_warn"] = warn in To
            dd = [cheb(T[t]["pos"], To[t]["pos"]) for t in ventana if t in To]
            d["dist_hermano_mediana"] = (st.median(dd) if dd else None); d["junto_pct"] = (round(100 * sum(1 for x in dd if x <= 3) / len(dd), 1) if dd else None)
            def rivales(t):
                den = [(q, h) for q, h in RIV.get(t, {}).values() if math.dist(q, C) <= r1]
                return len(den), sum(1 for q, h in den if h in V["armas"]), sum(1 for q, h in den if cheb(q, T[t]["pos"]) <= 5)
            d["rivales_dentro_warn"], d["armados_dentro_warn"], d["rivales_cerca_warn"] = rivales(warn)
            if ent is not None:
                d["rivales_dentro_entra"], d["armados_dentro_entra"], d["rivales_cerca_entra"] = rivales(ent)
            d["tics_ardiendo_fase"] = sum(1 for t in ventana if arde(T[t]["pos"], T[t]["radio"]))
            d["sobrevive_fase"] = (mt >= sig) or (fin.get("reason") != "eliminated"); d["muere_en_fase"] = not d["sobrevive_fase"]
            if d["muere_en_fase"]:
                fu, arma = causa_de(V, mt); d["muerte"] = mt; d["golpes_finales"] = fu; d["armas_agresores"] = arma
                d["causa"] = causa_simple(V, mt); d["fuera_al_morir"] = arde(T[mt]["pos"], T[mt]["radio"])
            g = collections.Counter()
            for t in ventana:
                for x in T[t]["dt"]:
                    g[str(x.get("source"))] += float(x.get("amount") or 0)
            d["dano_fase"] = dict(g)
            ANAT.append(d)


# ═════════ 3 · llegar no es quedarse (A5h) ═════════
def sec3(b, s, G):
    if b != "A5h":
        return
    for sl in (10, 11):
        V = G[sl]; T = V["T"]; To = G[21 - sl]["T"]; mt = max(T); fin = V["fin"] or {}; fases = V["fases"]
        for c in V["L"]["compromiso6"]:
            if c.get("estado") != "cumplida":
                continue
            t0 = c["tick"]
            if t0 not in T:
                continue
            d = {"semilla": s, "slot": sl, "tick": t0, "por": c.get("por"), "destino": c.get("destino"), "pos": c.get("pos"), "hp": T[t0]["hp"]}
            tics = [t for t in sorted(T) if t >= t0]
            sale = next((t for t in tics if not dentro(T[t]["pos"], fases, t)), None)
            d["tics_dentro"] = (sale - t0) if sale is not None else (mt - t0); d["sale"] = sale; d["se_queda_hasta_el_final"] = sale is None
            if sale is not None:
                r = T[sale]; d["elegido_al_salir"] = r["el"]; d["hp_al_salir"] = r["hp"]
                d["filas_al_salir"] = dict(sorted(r["ahora"].items(), key=lambda kv: -kv[1])[:6])
                det = next((t for t in range(sale, sale + 25) if T.get(t, {}).get("cs")), next((t for t in range(sale - 1, sale - 25, -1) if T.get(t, {}).get("cs")), None))
                if det is not None:
                    cs = T[det]["cs"]; el = T[det]["el"]
                    d["detalle"] = {"tick": det, "elegido": el, "d": {k: (v.get("d") if isinstance(v, dict) else v) for k, v in cs.items()}}
                    if isinstance(cs.get(el), dict) and isinstance(cs.get("noop"), dict):
                        fe, fn = cs[el].get("filas") or {}, cs["noop"].get("filas") or {}
                        d["detalle"]["delta_elegido_menos_noop"] = {k: round((fe.get(k) or 0) - (fn.get(k) or 0), 4) for k in set(fe) | set(fn) if abs((fe.get(k) or 0) - (fn.get(k) or 0)) > 1e-4}
                g = collections.Counter()
                for t in range(t0, min(mt, sale + 100) + 1):
                    for x in T.get(t, {}).get("dt", []):
                        g[str(x.get("source"))] += float(x.get("amount") or 0)
                d["dano_dentro_y_tras_salir"] = dict(g)
            d["rivales_cerca_en_llegada"] = sum(1 for q, h in G["RIV"].get(t0, {}).values() if cheb(q, T[t0]["pos"]) <= 5)
            d["hermano_dist_llegada"] = (cheb(T[t0]["pos"], To[t0]["pos"]) if t0 in To else None)
            d["muere"] = fin.get("reason") == "eliminated"; d["muerte"] = mt if d["muere"] else None
            if d["muere"]:
                d["causa"] = causa_simple(V, mt); d["golpes_finales"] = causa_de(V, mt)[0]; d["tics_hasta_morir"] = mt - t0
            AND.append(d)


# ═════════ 4 · salir al fuego y volver ═════════
def sec4(b, s, G):
    RIV = G["RIV"]
    for sl in (10, 11):
        V = G[sl]; T = V["T"]; ts = sorted(T); mt = max(T); fin = V["fin"] or {}; fases = V["fases"]
        for t in ts:
            r = T[t]
            if not r["el"].startswith("usar_") or r["ar"] not in ("ok", None):
                continue
            item = {"usar_botiquin": "first_aid", "usar_racion": "rations"}.get(r["el"])
            if item not in V["curas"]:
                continue
            heal, dur = V["curas"][item]
            fuera = arde(r["pos"], r["radio"]); hp0 = r["hp"]
            fut = [T[x]["hp"] for x in ts if t < x <= t + dur + 2]
            CUR.append({"brazo": b, "semilla": s, "slot": sl, "tick": t, "item": item, "fuera": fuera, "hp": hp0, "hp_max_tras": (max(fut) if fut else None), "hp_fin": (fut[-1] if fut else None),
                        "sube": bool(fut and max(fut) > hp0 + 1e-9), "fuera_todo_el_canal": (all(arde(T[x]["pos"], T[x]["radio"]) for x in ts if t < x <= t + dur) if fuera else None)})
        if fin.get("reason") != "eliminated" or causa_simple(V, mt) != "anillo":
            continue
        ult_dentro = max((t for t in ts if t <= mt and not arde(T[t]["pos"], T[t]["radio"])), default=None)
        t_sal = next((t for t in ts if t > ult_dentro), ts[0]) if ult_dentro is not None else ts[0]
        i = fase_en(fases, mt); dps = fases[i][5] if i is not None else 0; q = dps / TR
        hp_sal = T[t_sal]["hp"]; r1 = r1_en(fases, mt)
        def n_dentro(t):
            return sum(1 for q_, h in RIV.get(t, {}).values() if math.dist(q_, C) <= r1)
        n_sal = n_dentro(t_sal); serie = [(t, n_dentro(t)) for t in ts if t_sal <= t <= mt]
        minimo = min(serie, key=lambda x: x[1]) if serie else (None, None)
        hueco = next(((t, n) for t, n in serie if n < n_sal), None); vacio = next(((t, n) for t, n in serie if n == 0), None)
        d = {"brazo": b, "semilla": s, "slot": sl, "fase": (i + 1 if i is not None else None), "dps": dps, "sale": t_sal, "muerte": mt, "hp_al_salir": hp_sal, "tics_fuera": mt - t_sal,
             "aguante_teorico": (int(hp_sal / q) if q else None), "rivales_dentro_al_salir": n_sal, "min_rivales_dentro": minimo[1], "tick_min": minimo[0],
             "hueco_menos_rivales": hueco, "hueco_vacio": vacio,
             "golpes_rival_fuera": round(sum(float(x.get("amount") or 0) for t in ts if t_sal <= t <= mt for x in T[t]["dt"] if str(x.get("source")).startswith("P")), 1),
             "curas_fuera": sum(1 for t in ts if t_sal <= t <= mt and T[t]["el"].startswith("usar_")), "hermano_vivo_al_salir": t_sal in G[21 - sl]["T"]}
        for nombre, h in (("hueco", hueco), ("vacio", vacio)):
            if h:
                k = bfs_seguro(V["mundo"], T[h[0]]["pos"], r1); d[f"pasos_en_{nombre}"] = k; d[f"vuelta_en_{nombre}"] = (h[0] - t_sal + (k or 0) * 11)
                d[f"margen_{nombre}"] = (d["aguante_teorico"] - d[f"vuelta_en_{nombre}"]) if (d["aguante_teorico"] is not None and k is not None) else None
        SAL.append(d)


# ═════════ 5 · defensa conjunta ═════════
def sec5(b, s, G):
    RIV = G["RIV"]; MU = G["muertes"]
    for sl in (10, 11):
        V = G[sl]; Vb = G[21 - sl]; T = V["T"]; Tb = Vb["T"]; ts = sorted(T)
        for t in ts:
            for x in T[t]["dt"]:
                src = str(x.get("source"))
                if not src.startswith("P"):
                    continue
                R = int(src[1:])
                if t not in Tb or cheb(T[t]["pos"], Tb[t]["pos"]) > 3:
                    continue
                vent = [u for u in ts if t <= u <= t + 48]
                b_pega = [u for u in vent if pega_a(Tb, u, R, RIV, Vb["armas"])]; a_pega = [u for u in vent if pega_a(T, u, R, RIV, V["armas"])]
                juntos = any(abs(u - v) <= 24 for u in b_pega for v in a_pega)
                muere = MU.get(R); muere_en = (muere - t) if (muere is not None and t <= muere <= t + 200) else None
                sigue = [u for u in ts if t < u <= t + 100 for y in T[u]["dt"] if str(y.get("source")) == src] + [u for u in Tb if t < u <= t + 100 for y in Tb[u]["dt"] if str(y.get("source")) == src]
                deja = (max(sigue) - t) if sigue else 0
                lejos = None; racha = 0
                for u in ts:
                    if u <= t or u > t + 100:
                        continue
                    q = RIV.get(u, {}).get(R)
                    if q is None or cheb(q[0], T[u]["pos"]) > 8:
                        racha += 1
                        if racha >= 48:
                            lejos = u - 47 - t; break
                    else:
                        racha = 0
                DEF.append({"brazo": b, "semilla": s, "slot": sl, "tick": t, "agresor": R, "arma_agresor": (RIV.get(t, {}).get(R) or (None, "?"))[1], "dano": float(x.get("amount") or 0),
                            "hermano_pega": bool(b_pega), "yo_pego": bool(a_pega), "los_dos_a_la_vez": juntos, "n_golpes_hermano": len(b_pega), "n_golpes_yo": len(a_pega),
                            "arma_yo": T[t]["hand"], "arma_hermano": Tb[t]["hand"], "dano_yo": V["armas"].get(T[t]["hand"], (0,))[0], "dano_hermano": Vb["armas"].get(Tb[t]["hand"], (0,))[0],
                            "agresor_muere_en": muere_en, "agresor_deja_de_pegar_tras": deja, "agresor_se_va_en": lejos, "yo_muero_en_100": (max(T) - t <= 100 and (V["fin"] or {}).get("reason") == "eliminated")})
                for u in vent:
                    cs = Tb.get(u, {}).get("cs")
                    if not cs or not Tb[u]["atk"]:
                        continue
                    q = RIV.get(u, {}).get(R)
                    if not q:
                        continue
                    alc = Vb["armas"][Tb[u]["hand"]][1] if Tb[u]["hand"] in Vb["armas"] else 1
                    atk = [n for n in cs if n.startswith("atacar_") and n[7:] in DIRS and any((Tb[u]["pos"][0] + DIRS[n[7:]][0] * k, Tb[u]["pos"][1] + DIRS[n[7:]][1] * k) == q[0] for k in range(1, alc + 1))]
                    if not atk:
                        continue
                    el = Tb[u]["el"]; fa = (cs.get(atk[0]) or {}).get("filas") or {}
                    if el in atk:
                        NDET[1] += 1; fn = (cs.get("noop") or {}).get("filas") or {}
                        for k in set(fa) | set(fn):
                            FILAS_SI[k].append((fa.get(k) or 0) - (fn.get(k) or 0))
                    else:
                        NDET[0] += 1; fe = (cs.get(el) or {}).get("filas") or {}
                        for k in set(fa) | set(fe):
                            FILAS_NO[k].append((fe.get(k) or 0) - (fa.get(k) or 0))


# ═════════ el bucle ═════════
for (b, s), G in partidas():
    if FASES is None:
        FASES = G[10]["fases"]; TR = G[10]["tick_rate"]
    sec1(b, s, G); sec2(b, s, G); sec3(b, s, G); sec4(b, s, G); sec5(b, s, G)
    print(f"  {b} {s} · anat {len(ANAT)} andados {len(AND)} curas {len(CUR)} salidas {len(SAL)} golpes-con-hermano {len(DEF)}", flush=True)

OUT = {"nota": "P6-17. INSTRUMENTO DE MEDIDA, solo lectura de los diarios de A4/A5v/A5h."}


# ═════════ cierres ═════════
def permutacion(d):
    n = len(d); obs = sum(d) / n
    if all(x == 0 for x in d):
        return 1.0, (0.0, 0.0), 0.0
    dd = np.array(d, dtype=float); idx = np.arange(2 ** n, dtype=np.int64)
    signs = (((idx[:, None] >> np.arange(n)) & 1) * 2 - 1).astype(np.int8)
    means = signs @ dd / n
    p = float(np.mean(np.abs(means) >= abs(obs) - 1e-12))
    rng = np.random.default_rng(20260927)
    bs = np.sort(rng.choice(dd, size=(10000, n), replace=True).mean(axis=1))
    return p, (float(bs[250]), float(bs[9749])), (st.pstdev(d) if n > 1 else 0.0)


print("\n=== 1 · RUIDO", flush=True)
RUIDO = {}
sems = sorted(s for s in POR_SEM if all(b in POR_SEM[s] for b in BRAZOS))
for a, b in (("A5v", "A4"), ("A5h", "A4"), ("A5h", "A5v")):
    R = {}
    for k in ("supervivientes", "rival", "anillo", "vida", "los_dos"):
        d = [POR_SEM[s][a][k] - POR_SEM[s][b][k] for s in sems]
        p, ic, sd = permutacion(d)
        R[k] = {"n": len(d), "media": round(sum(d) / len(d), 3), "total": sum(d), "sd_dif": round(sd, 3), "p_perm": round(p, 4), "ic95": [round(ic[0], 3), round(ic[1], 3)],
                "gana": sum(1 for x in d if x > 0), "pierde": sum(1 for x in d if x < 0), "efecto_detectable_2sd": round(2 * sd / math.sqrt(len(d)), 3)}
        print(f"   {a}-{b} {k:15s} media {R[k]['media']:+.3f} (total {R[k]['total']:+}) sd {sd:.2f} p_perm {p:.4f} IC95 {R[k]['ic95']} · detectable(2sd) {R[k]['efecto_detectable_2sd']}")
    RUIDO[f"{a}-{b}"] = R
for b in LENT:
    LENT[b]["esperadas_al_azar"] = round(LENT[b]["esperadas_al_azar"], 2)
    print(f"   {b}: tics lentos {LENT[b]['tics_lentos']} de {LENT[b]['tics']} · muertes por rival {LENT[b]['muertes_rival']}, a <= 60 tics de un lento {LENT[b]['muertes_rival_a_60_tics_de_un_lento']} (esperadas al azar {LENT[b]['esperadas_al_azar']})")
OUT["ruido"] = {"por_semilla": {str(s): POR_SEM[s] for s in sems}, "emparejado": RUIDO, "tic_lento": LENT}

print("\n=== 2 · ANATOMIA", flush=True)
def cruza(sel, fn, minimo=5):
    tab = collections.defaultdict(lambda: [0, 0])
    for d in sel:
        k = fn(d)
        if k is None:
            continue
        tab[k][1] += 1; tab[k][0] += d["sobrevive_fase"]
    return {str(k): {"sobreviven": v[0], "n": v[1], "pct": (round(100 * v[0] / v[1], 1) if v[1] else None), "pocos": v[1] < minimo} for k, v in sorted(tab.items())}
CRUCES = {}
for fase in (4, 5, 6):
    for b in list(BRAZOS) + ["todos"]:
        sel = [d for d in ANAT if d["fase"] == fase and (b == "todos" or d["brazo"] == b)]
        CRUCES[f"fase {fase} · {b}"] = {"n": len(sel), "sobreviven": sum(d["sobrevive_fase"] for d in sel),
            "entra": cruza(sel, lambda d: d["entra_cuando"] or "nunca"),
            "dentro_en_warn": cruza(sel, lambda d: d["dentro_en_warn"]),
            "junto_en_warn": cruza(sel, lambda d: ("junto" if d["junto_en_warn"] else ("solo (hermano vivo)" if d["hermano_vivo_en_warn"] else "solo (hermano muerto)"))),
            "junto_pct_fase": cruza(sel, lambda d: None if d["junto_pct"] is None else ("junto >= 50 % de la fase" if d["junto_pct"] >= 50 else "junto < 50 %")),
            "rivales_cerca_al_entrar": cruza(sel, lambda d: None if d.get("rivales_cerca_entra") is None else ("0" if d["rivales_cerca_entra"] == 0 else ("1-2" if d["rivales_cerca_entra"] <= 2 else ">= 3"))),
            "rivales_dentro_al_entrar": cruza(sel, lambda d: None if d.get("rivales_dentro_entra") is None else ("0-2" if d["rivales_dentro_entra"] <= 2 else ("3-5" if d["rivales_dentro_entra"] <= 5 else ">= 6"))),
            "armados_dentro_al_entrar": cruza(sel, lambda d: None if d.get("armados_dentro_entra") is None else ("0" if d["armados_dentro_entra"] == 0 else ("1-2" if d["armados_dentro_entra"] <= 2 else ">= 3"))),
            "entra_x_junto": cruza(sel, lambda d: f"{(d['entra_cuando'] or 'nunca')} · {'junto' if d['junto_en_warn'] else 'solo'}"),
            "ardiendo_en_la_fase": cruza(sel, lambda d: "0 tics" if d["tics_ardiendo_fase"] == 0 else ("1-100" if d["tics_ardiendo_fase"] <= 100 else "> 100")),
            "causas": dict(collections.Counter(d.get("causa") for d in sel if d["muere_en_fase"])),
            "muertes_fuera_al_morir": sum(1 for d in sel if d["muere_en_fase"] and d.get("fuera_al_morir"))}
        if b == "todos":
            c = CRUCES[f"fase {fase} · {b}"]
            print(f"   fase {fase}: n {c['n']} sobreviven {c['sobreviven']} · entra {c['entra']} · junto {c['junto_en_warn']} · cerca {c['rivales_cerca_al_entrar']} · causas {c['causas']}")
OUT["anatomia"] = ANAT; OUT["cruces"] = CRUCES

print("\n=== 3 · LLEGAR NO ES QUEDARSE", flush=True)
OUT["andados"] = AND
fam = lambda e: re.split(r"_", e or "?")[0]
print(f"   andados {len(AND)} · se quedan hasta el final {sum(1 for d in AND if d['se_queda_hasta_el_final'])} · tics dentro mediana {st.median(d['tics_dentro'] for d in AND) if AND else None} · elegido al salir {collections.Counter(fam(d.get('elegido_al_salir')) for d in AND if d.get('sale'))} · mueren {sum(1 for d in AND if d['muere'])} ({collections.Counter(d.get('causa') for d in AND if d['muere'])})")
DL = collections.defaultdict(list)
for d in AND:
    for k, v in (d.get("detalle") or {}).get("delta_elegido_menos_noop", {}).items():
        DL[k].append(v)
OUT["andados_filas_al_salir"] = {k: {"n": len(v), "media": round(sum(v) / len(v), 4)} for k, v in sorted(DL.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))}
print("   filas (elegido - noop) al salir:", {k: v["media"] for k, v in OUT["andados_filas_al_salir"].items()})

print("\n=== 4 · SALIR AL FUEGO", flush=True)
FUEGO = {"fases": []}
for i, (warn, shrink, done, r0, r1, dps) in enumerate(FASES):
    q = dps / TR
    FUEGO["fases"].append({"fase": i + 1, "warn": warn, "shrink": shrink, "done": done, "r0": r0, "r1": r1, "dps": dps, "por_tic": round(q, 4),
                           "aguanta_100": (int(100 / q) if q else None), "aguanta_60": (int(60 / q) if q else None), "aguanta_30": (int(30 / q) if q else None)})
cf = [c for c in CUR if c["fuera"]]
FUEGO["curaciones"] = {"total": len(CUR), "fuera": len(cf), "fuera_y_sube": sum(1 for c in cf if c["sube"]), "fuera_todo_el_canal": sum(1 for c in cf if c["fuera_todo_el_canal"]),
                       "fuera_todo_el_canal_y_sube": sum(1 for c in cf if c["fuera_todo_el_canal"] and c["sube"]),
                       "ganancia_media_fuera": (round(st.mean(c["hp_max_tras"] - c["hp"] for c in cf if c["hp_max_tras"] is not None), 1) if cf else None),
                       "ganancia_media_dentro": (round(st.mean(c["hp_max_tras"] - c["hp"] for c in CUR if not c["fuera"] and c["hp_max_tras"] is not None), 1) if any(not c["fuera"] for c in CUR) else None),
                       "dentro": len(CUR) - len(cf), "dentro_y_sube": sum(1 for c in CUR if not c["fuera"] and c["sube"]), "por_item_fuera": dict(collections.Counter(c["item"] for c in cf)),
                       "por_brazo_fuera": dict(collections.Counter(c["brazo"] for c in cf)), "detalle_fuera": cf}
print(f"   curaciones {len(CUR)} · fuera {len(cf)} (suben {FUEGO['curaciones']['fuera_y_sube']}; todo el canal fuera {FUEGO['curaciones']['fuera_todo_el_canal']}, suben {FUEGO['curaciones']['fuera_todo_el_canal_y_sube']}) · ganancia media fuera {FUEGO['curaciones']['ganancia_media_fuera']} dentro {FUEGO['curaciones']['ganancia_media_dentro']}")
FUEGO["muertes_anillo"] = SAL
mg = lambda d, k: (d.get(k) if d.get(k) is not None else -1)
n_h = sum(1 for d in SAL if d.get("hueco_menos_rivales")); n_m = sum(1 for d in SAL if mg(d, "margen_hueco") > 0)
n_v = sum(1 for d in SAL if d.get("hueco_vacio")); n_mv = sum(1 for d in SAL if mg(d, "margen_vacio") > 0)
FUEGO["resumen"] = {"muertes_anillo": len(SAL), "hp_al_salir_mediana": (st.median(d["hp_al_salir"] for d in SAL) if SAL else None), "tics_fuera_mediana": (st.median(d["tics_fuera"] for d in SAL) if SAL else None),
                    "aguante_mediana": (st.median(d["aguante_teorico"] for d in SAL if d["aguante_teorico"] is not None) if SAL else None),
                    "hp_al_salir_bandas": dict(collections.Counter(("< 30" if d["hp_al_salir"] < 30 else ("30-60" if d["hp_al_salir"] < 60 else ">= 60")) for d in SAL)),
                    "con_hueco_menos_rivales": n_h, "con_margen_en_el_hueco": n_m, "con_hueco_vacio": n_v, "con_margen_en_el_vacio": n_mv,
                    "sin_rivales_dentro_al_salir": sum(1 for d in SAL if d["rivales_dentro_al_salir"] == 0), "golpes_rival_fuera_media": (round(st.mean(d["golpes_rival_fuera"] for d in SAL), 1) if SAL else None),
                    "por_brazo": {b: {"n": sum(1 for d in SAL if d["brazo"] == b), "con_margen_hueco": sum(1 for d in SAL if d["brazo"] == b and mg(d, "margen_hueco") > 0), "con_margen_vacio": sum(1 for d in SAL if d["brazo"] == b and mg(d, "margen_vacio") > 0)} for b in BRAZOS}}
print(f"   muertes por anillo {len(SAL)} · hp al salir mediana {FUEGO['resumen']['hp_al_salir_mediana']} bandas {FUEGO['resumen']['hp_al_salir_bandas']} · tics fuera mediana {FUEGO['resumen']['tics_fuera_mediana']} · aguante mediana {FUEGO['resumen']['aguante_mediana']} · con hueco {n_h} con margen {n_m} · vacio {n_v} con margen {n_mv}")
OUT["fuego"] = FUEGO

print("\n=== 5 · DEFENSA CONJUNTA", flush=True)
def resumen_def(sel):
    n = len(sel)
    if not n:
        return {"n": 0}
    mu = [d["agresor_muere_en"] for d in sel if d["agresor_muere_en"] is not None]
    return {"n": n, "hermano_pega": sum(d["hermano_pega"] for d in sel), "yo_pego": sum(d["yo_pego"] for d in sel), "los_dos_a_la_vez": sum(d["los_dos_a_la_vez"] for d in sel),
            "agresor_muere_en_200": len(mu), "agresor_muere_en_mediana": (st.median(mu) if mu else None),
            "agresor_deja_de_pegar_tras_mediana": st.median(d["agresor_deja_de_pegar_tras"] for d in sel), "agresor_no_pega_mas_tras_24": sum(1 for d in sel if d["agresor_deja_de_pegar_tras"] <= 24),
            "agresor_se_va_en_100": sum(1 for d in sel if d["agresor_se_va_en"] is not None), "se_va_en_mediana": (st.median(d["agresor_se_va_en"] for d in sel if d["agresor_se_va_en"] is not None) if any(d["agresor_se_va_en"] is not None for d in sel) else None),
            "yo_muero_en_100": sum(d["yo_muero_en_100"] for d in sel),
            "armas_yo": dict(collections.Counter(d["arma_yo"] for d in sel)), "armas_hermano": dict(collections.Counter(d["arma_hermano"] for d in sel)), "armas_agresor": dict(collections.Counter(d["arma_agresor"] for d in sel)),
            "dano_medio_yo": round(st.mean(d["dano_yo"] for d in sel), 1), "dano_medio_hermano": round(st.mean(d["dano_hermano"] for d in sel), 1)}
DEFR = {"golpes_con_hermano_a_3": resumen_def(DEF)}
for nombre, fn in (("pegan los dos", lambda d: d["hermano_pega"] and d["yo_pego"]), ("pega solo uno", lambda d: d["hermano_pega"] != d["yo_pego"]), ("no pega ninguno", lambda d: not d["hermano_pega"] and not d["yo_pego"]),
                   ("los dos a la vez (<= 24 tics)", lambda d: d["los_dos_a_la_vez"]), ("pega el hermano", lambda d: d["hermano_pega"]), ("no pega el hermano", lambda d: not d["hermano_pega"])):
    DEFR[nombre] = resumen_def([d for d in DEF if fn(d)])
    print(f"   {nombre}: {json.dumps(DEFR[nombre], ensure_ascii=False)[:420]}")
DEFR["filas_cuando_el_hermano_NO_pega (elegido - atacar)"] = {"n_detalles": NDET[0], "filas": {k: round(sum(v) / len(v), 4) for k, v in sorted(FILAS_NO.items(), key=lambda kv: sum(kv[1]) / len(kv[1])) if abs(sum(v) / len(v)) > 1e-3}}
DEFR["filas_cuando_el_hermano_SI_pega (atacar - noop)"] = {"n_detalles": NDET[1], "filas": {k: round(sum(v) / len(v), 4) for k, v in sorted(FILAS_SI.items(), key=lambda kv: sum(kv[1]) / len(kv[1])) if abs(sum(v) / len(v)) > 1e-3}}
DEFR["por_brazo"] = {b: resumen_def([d for d in DEF if d["brazo"] == b]) for b in BRAZOS}
DEFR["eventos"] = DEF
print(f"   filas NO pega ({NDET[0]}): {DEFR['filas_cuando_el_hermano_NO_pega (elegido - atacar)']['filas']}")
print(f"   filas SI pega ({NDET[1]}): {DEFR['filas_cuando_el_hermano_SI_pega (atacar - noop)']['filas']}")
OUT["defensa"] = DEFR
json.dump(OUT, open(os.path.join(AQUI, "P6_17_final.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_17_final.json")

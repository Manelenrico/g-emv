"""[P6-19 · 1] TASAS BASE: como suelen pegar los otros. SOLO LECTURA de los 200 diarios
del mundo del seis (A3, A4, A5v, A5h, A6; 100 partidas), de uno en uno.

Por tic vivo de nuestro cuerpo:
  · golpes recibidos: `damage_taken` con `source` P<slot> (rival) y su `amount`;
  · rivales VISTOS (`ve_agentes`: asiento, casilla, mano) y CONTADOS (el ultimo
    parte E2 del hermano en `chat`, con edad <= oyente2.CADUCIDAD_RIVAL, sin los
    asientos que ya veo: la misma regla que `oyente2.inyecta`; el parte trae la
    casilla y el arma);
  · arma del rival: `hand` (id del catalogo) o `arma` del parte; «mano» = none;
    alcance del catalogo (mano: 1); «a tiro» = distancia Chebyshev <= alcance;
  · contexto: fase activa del calendario, dentro (distancia al centro <= r1) o
    fuera; junto = hermano vivo a <= 3 (posiciones reales de los dos diarios).

Tasas (dano de rival por tic, y golpes por rival-tic):
  (a) por arma del rival y a tiro / fuera de tiro; P(pega en el tic | a tiro);
      dano por golpe; «a tiro y no pega»;
  (b) por arma y distancia (1, 2, 3-4, 5-6, 7-8, > 8): dano por rival-tic —
      la tabla que usa puerta6g;
  (c) por numero de rivales (vistos + contados) en el tic;
  (d) por contexto del anillo: fases 1-4; fases 5-7 dentro; fases 5-7 fuera;
  (e) junto / solo.
Intervalos: por remuestreo sobre vidas (2.000; percentiles 2,5 y 97,5) para
dano por tic; Wilson 95 % para las proporciones.
"""
import collections, glob, json, math, os, re, statistics as st, sys
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U, parte2 as P2, oyente2 as OY
C = (24, 24)
BRAZOS = {"A3": "paintball/runs/P610_t*_A3_*", "A4": "paintball/runs/P611_t*_A4_*", "A5v": "paintball/runs/P616_t1_A5v_*", "A5h": "paintball/runs/P616_t2_A5h_*", "A6": "paintball/runs/P618_t1_A6_*"}
BINS = [(1, 1, "1"), (2, 2, "2"), (3, 4, "3-4"), (5, 6, "5-6"), (7, 8, "7-8"), (9, 99, ">8")]
DANO_MANO = 3.0     # P6-11, medido


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def bin_de(d):
    for lo, hi, n in BINS:
        if lo <= d <= hi:
            return n
    return ">8"


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); fin = next((r for r in recs if r.get("k") == "final"), None)
    armas = {it["id"]: (float(it.get("damage") or 0), int(it.get("range") or 1)) for it in cat["items"] if float(it.get("damage") or 0) > 0}
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
        vis = {int(a["slot"]): ((int(a["pos"][0]), int(a["pos"][1])), ((a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand")) or "none", "visto") for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") is not None}
        cont = {}
        if ult and 0 <= t - ult["t"] <= OY.CADUCIDAD_RIVAL:
            for x in ult["rivales"]:
                if x["slot"] not in vis and x["slot"] not in (pc["slot"], herm):
                    cont[int(x["slot"])] = (tuple(x["pos"]), (x.get("arma") or "none"), "contado")
        T[t] = {"pos": tuple(int(x) for x in r["pos"]), "hp": float(r.get("hp") if r.get("hp") is not None else 100), "radio": float((r.get("zona") or {}).get("radius") or 48),
                "dt": {str(g.get("source")): float(g.get("amount") or 0) for g in (r.get("damage_taken") or []) if isinstance(g, dict)},
                "riv": {s: v for s, v in list(vis.items()) + list(cont.items()) if s not in (pc["slot"], herm)}}
    del recs
    return pc, T, fin, armas, [tuple(z) for z in pc.get("zone_schedule") or []]


def fase_en(fases, t):
    k = None
    for i, f in enumerate(fases):
        if f[0] <= t:
            k = i
    return k


def alcance(armas, w):
    if not w or w == "none":
        return 1
    return armas.get(w, (0, 1))[1]


# ── acumuladores ─────────────────────────────────────────────────────────────
RT = collections.defaultdict(lambda: {"rt": 0, "hits": 0, "dano": 0.0})   # (arma, a_tiro | bin) -> rival-tics, golpes, dano
CTX = collections.defaultdict(lambda: {"tics": 0, "dano": 0.0, "golpes": 0})
VIDAS = collections.defaultdict(list)     # clave -> [(dano, tics) por vida]
ULT_VISTO = {}
golpes_sin_ver = {"golpes": 0, "dano": 0.0}; golpes_tot = {"golpes": 0, "dano": 0.0}; dano_por_golpe = collections.defaultdict(list)
n_vidas = 0
for brazo, pat in BRAZOS.items():
    for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))}
        if len(fs) != 2:
            continue
        G = {sl: carga(fs[sl]) for sl in (10, 11)}
        for sl in (10, 11):
            pc, T, fin, armas, fases = G[sl]; To = G[21 - sl][1]; n_vidas += 1
            por_vida = collections.defaultdict(lambda: [0.0, 0])
            ultimo = {}     # slot -> (tick, arma, pos) ultima vez visto/contado
            for t in sorted(T):
                r = T[t]; pos = r["pos"]
                i = fase_en(fases, t); r1 = fases[i][4] if i is not None else 48.0
                dentro = math.dist(pos, C) <= r1
                ctx = ("fases 1-4" if (i is None or i < 4) else ("fases 5-7 dentro" if dentro else "fases 5-7 fuera"))
                junto = (t in To) and cheb(pos, To[t]["pos"]) <= 3
                dr = {s: a for s, a in r["dt"].items() if s.startswith("P")}
                dano_t = sum(dr.values()); golpes_t = len(dr)
                for s, v in r["riv"].items():
                    ultimo[s] = (t, v[1], v[0])
                n_riv = len(r["riv"])
                # (c), (d), (e): por tic
                for k in ((f"rivales {min(n_riv, 4)}{'+' if n_riv >= 4 else ''}"), ctx, ("junto" if junto else ("solo (hermano vivo)" if t in To else "solo (hermano muerto)"))):
                    CTX[k]["tics"] += 1; CTX[k]["dano"] += dano_t; CTX[k]["golpes"] += golpes_t
                    por_vida[k][0] += dano_t; por_vida[k][1] += 1
                # (a), (b): por rival visible/contado
                for s, (q, w, como) in r["riv"].items():
                    w = w or "none"; d = cheb(pos, q); alc = alcance(armas, w); tiro = d <= alc
                    dm = dr.get(f"P{s}", 0.0)
                    for key in ((w, "a tiro" if tiro else "fuera de tiro"), (w, bin_de(d)), (como, "a tiro" if tiro else "fuera de tiro"), ("todas", bin_de(d))):
                        RT[key]["rt"] += 1; RT[key]["hits"] += (dm > 0); RT[key]["dano"] += dm
                    if dm > 0:
                        dano_por_golpe[w].append(dm)
                # golpes de rivales no visibles ni contados en el tic (con su ultima arma conocida a <= 50 tics)
                for src, dm in dr.items():
                    golpes_tot["golpes"] += 1; golpes_tot["dano"] += dm
                    s = int(src[1:])
                    if s not in r["riv"]:
                        golpes_sin_ver["golpes"] += 1; golpes_sin_ver["dano"] += dm
                        u = ultimo.get(s)
                        w = u[1] if (u and t - u[0] <= 50) else "desconocida"
                        RT[(w or "none", "no visto, pega")]["hits"] += 1; RT[(w or "none", "no visto, pega")]["dano"] += dm; RT[(w or "none", "no visto, pega")]["rt"] += 1
            for k, (dn, tk) in por_vida.items():
                VIDAS[k].append((dn, tk))
        print(f"  {brazo} {os.path.basename(carp)}", flush=True)


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - s) / d, 5), round((c + s) / d, 5)]


def boot(pares):
    if not pares:
        return None
    rng = np.random.default_rng(20260927); a = np.array(pares, dtype=float)
    idx = rng.integers(0, len(a), size=(2000, len(a)))
    tasas = a[idx, 0].sum(axis=1) / np.maximum(1, a[idx, 1].sum(axis=1))
    return [round(float(np.percentile(tasas, 2.5)), 5), round(float(np.percentile(tasas, 97.5)), 5)]


OUT = {"nota": "P6-19 tasas base. INSTRUMENTO DE MEDIDA, solo lectura.", "vidas": n_vidas, "armas_dano_mano": DANO_MANO}
tab = {}
for (w, k), v in RT.items():
    tab[f"{w} · {k}"] = {"rival_tics": v["rt"], "golpes": v["hits"], "dano": round(v["dano"], 1), "dano_por_rival_tic": round(v["dano"] / max(1, v["rt"]), 5), "p_pega_en_el_tic": round(v["hits"] / max(1, v["rt"]), 5),
                        "ic_wilson": wilson(v["hits"], v["rt"]), "dano_por_golpe": round(v["dano"] / max(1, v["hits"]), 2)}
OUT["por_rival"] = tab
OUT["por_tic"] = {k: {"tics": v["tics"], "dano": round(v["dano"], 1), "golpes": v["golpes"], "dano_por_tic": round(v["dano"] / max(1, v["tics"]), 5), "ic_boot_vidas": boot(VIDAS.get(k)), "vidas": len(VIDAS.get(k, []))} for k, v in CTX.items()}
OUT["golpes"] = {"total": golpes_tot, "de rival ni visto ni contado en el tic": golpes_sin_ver, "dano_por_golpe_por_arma": {w: {"n": len(v), "media": round(st.mean(v), 2)} for w, v in dano_por_golpe.items()}}
# la tabla de puerta6g: dano por rival-tic por arma y distancia
TG = {}
for (w, k), v in RT.items():
    if k in [b[2] for b in BINS] and w != "todas":
        TG.setdefault(w, {})[k] = {"dano_por_rival_tic": round(v["dano"] / max(1, v["rt"]), 5), "n": v["rt"]}
OUT["tabla_puerta6g"] = TG
json.dump(OUT, open(os.path.join(AQUI, "P6_19_tasas.json"), "w"), ensure_ascii=False, indent=1)
print(f"\nvidas {n_vidas} · golpes de rival {golpes_tot} · sin ver ni contar {golpes_sin_ver}")
print("\n=== (a) por arma · a tiro / fuera de tiro")
for k, v in sorted(tab.items()):
    if "tiro" in k or "no visto" in k:
        print(f"   {k:32s} rival-tics {v['rival_tics']:8d} · golpes {v['golpes']:6d} · P(pega|tic) {v['p_pega_en_el_tic']:.4f} {v['ic_wilson']} · dano/rival-tic {v['dano_por_rival_tic']:.4f} · dano/golpe {v['dano_por_golpe']}")
print("\n=== (b) por arma y distancia (dano por rival-tic)")
for w, d in TG.items():
    print(f"   {w:10s} " + " · ".join(f"{b}: {d[b]['dano_por_rival_tic']:.4f} (n {d[b]['n']})" for b in [x[2] for x in BINS] if b in d))
print("\n=== (c)(d)(e) por tic")
for k, v in sorted(OUT["por_tic"].items()):
    print(f"   {k:26s} tics {v['tics']:8d} · dano/tic {v['dano_por_tic']:.5f} IC {v['ic_boot_vidas']} · golpes {v['golpes']}")
print("-> P6_19_tasas.json")

"""[P6-10 · 3] EL BANCO: S-COMPANIA sobre los diarios de A2 (P6-8). SOLO LECTURA.
(S-SOLEDAD se deja como la calcula el cinco: decision de Manel antes de jugar.)

En cada tic con detalle de candidatos (cada 24), para cada candidato se toma su
`filas` logueado (M por fila) y su `pos_prevista`, se calculan las dos filas
nuevas en esa casilla prevista y se recompone `d` con el MISMO reparto y motor
(`mide_P6_4.d_de`, fiel a 1,7e-5). Ganador nuevo = argmin d (empates: se queda
el logueado). Posicion del hermano: la vista si `pareja_vista`, si no la del
parte (`ahora.parte.pos`); distancia de CAMINO (`campo_geodesico`).
`sinver` = tics desde la ultima `pareja_vista`.

  a) DENTRO de D0 (mi casilla a <= D0 de camino del hermano): decisiones que
     cambian, por techo.
  b) FUERA (llegada = pasos x 11 > 100, la definicion de P6-9): con que techo
     `ir_pareja` pasa a ganar en el p75 de los tics — el mas pequeno que lo hace.
  c) COMIDA CERCA: tics en que el ganador logueado era `ir_objeto`/`ir_botin`/
     `coger` con una racion o venda a <= 3 casillas, y con la fila pasa a otra
     cosa.
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    sys.path.insert(0, p)
import serie_util as U
import mide_P6_4 as M4
import filas10_P6_10 as F10

TECHOS = [0.0, 0.1, 0.2, 0.25, 0.3, 0.32, 0.35, 0.38, 0.4, 0.5, 0.7, 1.0]
COMIDA = ("rations", "first_aid")


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map")
    cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    sp = it = 5
    for r in recs:
        if r.get("k") == "arranque":
            s = json.dumps(r); m = re.search(r'"speed"\s*:\s*(\d+)', s); sp = int(m.group(1)) if m else 5
            m = re.search(r'"intelligence"\s*:\s*(\d+)', s); it = int(m.group(1)) if m else 5; break
    T = {}; ultvisto = None
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        so = r.get("social") or {}; ra = r.get("RADIOGRAFIA") or {}; ah = ra.get("ahora") or {}
        if so.get("pareja_vista"):
            ultvisto = r["tick"]
        ph = None
        for a in (r.get("ve_agentes") or []):
            if a.get("slot") == pc["teammate_slot"] and a.get("pos"):
                ph = (int(a["pos"][0]), int(a["pos"][1]))
        if ph is None and (ah.get("parte") or {}).get("pos"):
            ph = tuple(int(x) for x in ah["parte"]["pos"])
        T[r["tick"]] = {"pos": tuple(int(x) for x in r["pos"]), "ph": ph, "visto": bool(so.get("pareja_vista")),
                        "sinver": (r["tick"] - ultvisto) if ultvisto is not None else 10 ** 6,
                        "muerta": bool(r.get("pareja_muerta")), "el": ra.get("elegido"),
                        "cs": ra.get("candidatos") if isinstance((ra.get("candidatos") or {}).get("noop"), dict) else None,
                        "listas": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0,
                        "items": {(int(x["pos"][0]), int(x["pos"][1])): x["id"] for x in (r.get("ve_items") or [])}}
    del recs
    return mundo, sp, it, T


def d_con(F, m_c, m_s, m_s0):
    G = dict(F); G["S-COMPANIA"] = m_c; G["S-SOLEDAD"] = m_s
    return M4.d_de(G)


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    S = collections.Counter(); R = {t: collections.Counter() for t in TECHOS}; huecos = []
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl not in (10, 11):
                continue
            mundo, sp, it, T = carga(f)
            coste = mundo.coste_movimiento(sp); radio = mundo.radio_vision(it)
            for t, r in T.items():
                if not r["cs"] or r["muerta"] or r["ph"] is None:
                    continue
                d_yo = F10.d_camino(mundo, r["pos"], r["ph"])
                dentro = d_yo is not None and d_yo <= F10.D0
                lejos = d_yo is None or d_yo * coste > 100
                S["tics con detalle"] += 1; S["  dentro de D0"] += dentro; S["  lejos (llegada > 100)"] += lejos
                el = r["el"]
                if el not in r["cs"]:
                    continue
                # comida cerca del ganador logueado
                comida = el.startswith(("ir_objeto", "ir_botin", "coger")) and any(
                    v in COMIDA and max(abs(k[0] - r["pos"][0]), abs(k[1] - r["pos"][1])) <= 3 for k, v in r["items"].items())
                # filas nuevas por candidato
                base = {}
                for n, v in r["cs"].items():
                    if not isinstance(v, dict):
                        continue
                    p2 = tuple(v.get("pos_prevista") or r["pos"]); F = dict(v.get("filas") or {})
                    d2 = F10.d_camino(mundo, p2, r["ph"])
                    ver = r["visto"] or (math.dist(p2, r["ph"]) <= radio)   # la regla del decisor (:873), euclidea
                    m_s0 = float(F.get("S-SOLEDAD") or 0.0)
                    m_s = m_s0            # S-SOLEDAD no se toca (decision de Manel)
                    base[n] = (F, d2, F10.amenaza_de(F), m_s, m_s0, v["d"])
                if "noop" not in base:
                    continue
                for techo in TECHOS:
                    dd = {n: d_con(F, F10.compania_M(d2, am, techo), m_s, m_s0) for n, (F, d2, am, m_s, m_s0, _) in base.items()}
                    dmin = min(dd.values()); gana = el if abs(dd[el] - dmin) < 1e-9 else min(dd, key=lambda n: (dd[n], n != el))
                    Rt = R[techo]; Rt["tics"] += 1
                    if dentro:
                        Rt["dentro"] += 1; Rt["dentro: cambia"] += (gana != el)
                    if lejos and "ir_pareja" in dd and r["listas"]:
                        # SOLO con piernas listas: en enfriamiento `ir_pareja` era el
                        # ganador falso del envoltorio de P6-8 (P6-8 § C.0)
                        Rt["lejos"] += 1; Rt["lejos: gana ir_pareja"] += (gana == "ir_pareja")
                        # ¿gana algo que ACERCA al hermano (camino previsto < camino actual)?
                        dg = base[gana][1]
                        Rt["lejos: gana algo que acerca"] += (dg is not None and d_yo is not None and dg < d_yo)
                        if techo == 0.0:
                            Rt["lejos: (logueado) acercaba"] += (base[el][1] is not None and d_yo is not None and base[el][1] < d_yo)
                        # la ventaja que la fila da a ir_pareja frente al ganador logueado
                        d0p, d0g = base["ir_pareja"][5], base[el][5]
                        Rt.setdefault("_ventaja", []).append((dd[el] - dd["ir_pareja"]) - (d0g - d0p))
                        if techo == 0.0:
                            huecos.append(dd["ir_pareja"] - dd[el])
                    if comida:
                        Rt["comida cerca"] += 1; Rt["comida cerca: se deja"] += (gana != el)
                    if r["listas"]:
                        Rt["piernas listas"] += 1; Rt["piernas listas: cambia"] += (gana != el)
    for techo in TECHOS:
        v = R[techo].pop("_ventaja", [])
        if v:
            s_ = sorted(v); R[techo]["ventaja p50"] = s_[int(0.5 * (len(s_) - 1))]; R[techo]["ventaja p25"] = s_[int(0.25 * (len(s_) - 1))]
            R[techo]["ventaja >= 0.158 (%)"] = 100 * sum(x >= 0.158 for x in v) / len(v)
    OUT[etiq] = {"recuento": dict(S), "por_techo": {str(t): dict(R[t]) for t in TECHOS},
                 "hueco_lejos_techo0": {"n": len(huecos), "p50": st.median(huecos) if huecos else None,
                                        "p75": sorted(huecos)[int(0.75 * (len(huecos) - 1))] if huecos else None}}
    print(f"### {etiq}: {dict(S)} · hueco (techo 0) n={len(huecos)} p50={OUT[etiq]['hueco_lejos_techo0']['p50']} p75={OUT[etiq]['hueco_lejos_techo0']['p75']}")
    print(f"  {'techo':>6s} {'dentro cambia':>16s} {'lejos+listas gana ir_pareja':>28s} {'acerca':>8s} {'ventaja p25/p50':>16s} {'>=0.158':>8s} {'comida se deja':>16s} {'listas cambia':>18s}")
    for techo in TECHOS:
        Rt = R[techo]
        print(f"  {techo:6.2f} {Rt['dentro: cambia']:5d}/{Rt['dentro']:<5d} {100*Rt['dentro: cambia']/(Rt['dentro'] or 1):5.1f}% "
              f"{Rt['lejos: gana ir_pareja']:5d}/{Rt['lejos']:<5d} {100*Rt['lejos: gana ir_pareja']/(Rt['lejos'] or 1):5.1f}%  {100*Rt['lejos: gana algo que acerca']/(Rt['lejos'] or 1):5.1f}% "
              f"{Rt.get('ventaja p25', 0):+.3f}/{Rt.get('ventaja p50', 0):+.3f}   {Rt.get('ventaja >= 0.158 (%)', 0):5.1f}% "
              f"{Rt['comida cerca: se deja']:4d}/{Rt['comida cerca']:<4d} {100*Rt['comida cerca: se deja']/(Rt['comida cerca'] or 1):5.1f}% "
              f"{Rt['piernas listas: cambia']:5d}/{Rt['piernas listas']:<5d} {100*Rt['piernas listas: cambia']/(Rt['piernas listas'] or 1):5.1f}%")
json.dump(OUT, open(os.path.join(AQUI, "P6_10_banco.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_10_banco.json")

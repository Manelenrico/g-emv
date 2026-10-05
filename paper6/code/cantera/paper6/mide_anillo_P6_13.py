"""[P6-13 · 2 y 3] LA LINEA DE TIEMPO DEL ANILLO Y LA ANATOMIA DE LAS 22 MUERTES. SOLO LECTURA.

Todo sale de los diarios de A4 y de `mundo` (el calendario `zone_schedule` del
player_config, el centro (arena//2, arena//2), la distancia EUCLIDEA al centro,
como en `mundo.eventos_arde` y `anillo_en`).

PUNTO 2. Por partida: para cada fase (warn, shrink, done, r0, r1, dps) del
calendario, cuantas vidas y cuantas parejas enteras siguen vivas en `warn`; y
cuantas muertes por anillo caen en cada fase. "Al cierre" en P6-4/P6-6/P6-10/
P6-11 = los dos vivos en el tic 8.076 = `done` de la PRIMERA fase (24 -> 19).

PUNTO 3. Para cada muerte por anillo (causa de `mide_golpes`: ultimo golpe en
los 48 tics antes de morir es `zone`): aviso = `warn` de la fase del calendario
que estaba avisando en el tic de la muerte (la ultima con warn <= muerte; NO
`zona.warn_tick`, que tras `done` ya apunta a la siguiente); primer golpe = primer `damage_taken` de
`zone` en esa fase; muerte = ultimo tic vivo. Casilla SEGURA = con distancia
euclidea al centro <= r1 de esa fase (donde el anillo acabara) y no solida;
camino = BFS con 8 vecinos sobre `mundo.solido`; instantes = pasos x
coste_movimiento(speed) (11). Se calcula en el aviso y en el primer golpe.
El hermano: su posicion real (su diario) y si vive. Lo que eligio: familias de
`elegido` entre el primer golpe y la muerte con piernas listas, y en los tics
con detalle, que filas hicieron perder a `ir_centro` frente al ganador
(M ganador - M ir_centro por fila; negativo = ir_centro llevaba mas de esa fila).
"""
import collections, glob, json, math, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    sys.path.insert(0, p)
import serie_util as U
DIRS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
MIEDO = ("S-8-EXPOSICION", "F-4-ALCANCE", "S-7-AGRESOR", "F-DANO", "F-REENCUENTRO", "MIEDO_APRENDIDO")
HERMANO = ("S-COMPANIA", "F-HERMANO-AMENAZA", "F-HERMANO-GOLPE", "S-DANO-PAREJA", "S-HERIDO", "S-PROVISION", "R-HERMANO-FALTA", "S-SOLEDAD")


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"]); fin = next((r for r in recs if r.get("k") == "final"), None)
    sp = 5
    for r in recs:
        if r.get("k") == "arranque":
            m = re.search(r'"speed"\s*:\s*(\d+)', json.dumps(r)); sp = int(m.group(1)) if m else 5; break
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = {"pos": tuple(int(x) for x in r["pos"]), "hp": r.get("hp"), "zona": r.get("zona") or {},
                        "zone_hit": any(g.get("source") == "zone" for g in (r.get("damage_taken") or [])),
                        "el": str(ra.get("elegido") or ""), "listas": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0,
                        "cs": ra.get("candidatos") if isinstance((ra.get("candidatos") or {}).get("noop"), dict) else None,
                        "ve": [(a.get("slot"), (int(a["pos"][0]), int(a["pos"][1]))) for a in (r.get("ve_agentes") or []) if a.get("pos")],
                        "muerta": bool(r.get("pareja_muerta"))}
    del recs
    return mundo, pc, T, fin, sp


def bfs_seguro(mundo, desde, r1):
    """Pasos (8 vecinos) hasta la casilla mas cercana con dist euclidea al centro <= r1 y no solida; None si no hay."""
    n = mundo.arena_size; c = (n // 2, n // 2)
    def segura(p): return math.dist(p, c) <= r1 and not mundo.solido(p[0], p[1])
    if segura(desde):
        return 0
    vis = {desde}; frente = [desde]; k = 0
    while frente:
        k += 1; nuevo = []
        for (x, y) in frente:
            for dx, dy in DIRS:
                q = (x + dx, y + dy)
                if not (0 <= q[0] < n and 0 <= q[1] < n) or q in vis or mundo.solido(q[0], q[1]):
                    continue
                if segura(q):
                    return k
                vis.add(q); nuevo.append(q)
        frente = nuevo
    return None


def fam(e):
    for p in ("ir_centro", "ir_pareja", "ir_objeto", "ir_botin", "move_", "paso_", "atacar", "coger", "noop", "usar", "soltar"):
        if e.startswith(p):
            return p.rstrip("_")
    return "otro"


G = json.load(open(os.path.join(AQUI, "P6_11_golpes.json")))["A4"]["vidas"]
MUERTES_ANILLO = {(v["carp"], v["slot"]): v for v in G if v.get("causa") == "anillo"}
carps = sorted(set(v["carp"] for v in G))
LT = {}          # (carp, slot) -> (ultimo tic vivo, muere)
FASES = None; TL = collections.Counter(); ANAT = []
for carp in carps:
    fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, "*policy_agent_1*.art.log"))}
    L = {sl: carga(fs[sl]) for sl in (10, 11)}
    mundo = L[10][0]; FASES = FASES or [tuple(z) for z in mundo.zone_schedule]
    for sl in (10, 11):
        _, _, T, fin, _ = L[sl]
        LT[(carp, sl)] = (max(T), bool(fin and fin.get("reason") == "eliminated"), (fin or {}).get("reason"), (fin or {}).get("placement"))
    # punto 2: vivos en cada warn
    for i, (warn, shrink, done, r0, r1, dps) in enumerate(FASES):
        vivos = [sl for sl in (10, 11) if LT[(carp, sl)][0] >= warn]
        TL[("vidas vivas en warn", i)] += len(vivos); TL[("parejas enteras en warn", i)] += (len(vivos) == 2)
        for sl in (10, 11):
            v = MUERTES_ANILLO.get((carp, sl))
            if v and warn <= v["tic"] < (FASES[i + 1][0] if i + 1 < len(FASES) else 10 ** 9):
                TL[("muertes por anillo en la fase", i)] += 1
    TL["los dos vivos en 8076 (cierre de la fase 1)"] += all(LT[(carp, sl)][0] >= 8076 for sl in (10, 11))
    TL["los dos vivos en 14136 (aviso de la fase final)"] += all(LT[(carp, sl)][0] >= 14136 for sl in (10, 11))
    # punto 3
    for sl in (10, 11):
        v = MUERTES_ANILLO.get((carp, sl))
        if not v:
            continue
        mundo, pc, T, fin, sp = L[sl]; To = L[21 - sl][2]; coste = mundo.coste_movimiento(sp)
        tm = max(T)
        # LA FASE QUE MATA es la del calendario con warn <= muerte (la ultima que
        # ha avisado). `zona.warn_tick` NO sirve: tras `done` ya apunta a la
        # fase siguiente aunque el fuego vigente sea el de la anterior.
        # LA QUEMADURA QUE MATA: la ultima racha de golpes del anillo (huecos <= 48
        # tics, la ventana de E3) que acaba en la muerte; su primer golpe fecha la
        # fase (la ultima con warn <= primer golpe), no el tic de la muerte: tres
        # cuerpos llegan al aviso de la fase 6 ya con 1-10 hp de la quemadura de la 5.
        hits_all = [t for t in sorted(T) if T[t]["zone_hit"]]
        th = None
        if hits_all:
            th = hits_all[-1]
            for a, b in zip(reversed(hits_all[:-1]), reversed(hits_all)):
                if b - a <= 48:
                    th = a
                else:
                    break
        fase = max((f for f in FASES if f[0] <= (th if th is not None else tm)), key=lambda f: f[0]); warn = fase[0]; r1 = fase[4]
        d = {"carp": carp, "slot": sl, "aviso": warn, "primer_golpe": th, "muerte": tm, "fase": FASES.index(fase) + 1 if fase else None, "r1": r1, "dps": fase[5] if fase else None,
             "tics_aviso_a_muerte": tm - warn, "tics_golpe_a_muerte": (tm - th) if th else None, "hp_en_aviso": T.get(warn, T[min(T, key=lambda t: abs(t - warn))])["hp"]}
        for nombre, t in (("aviso", warn), ("golpe", th)):
            if t is None or t not in T:
                d[f"pasos_{nombre}"] = None; d[f"instantes_{nombre}"] = None; continue
            k = bfs_seguro(mundo, T[t]["pos"], r1)
            d[f"pasos_{nombre}"] = k; d[f"instantes_{nombre}"] = (k * coste) if k is not None else None
            d[f"pos_{nombre}"] = list(T[t]["pos"]); d[f"dist_centro_{nombre}"] = round(math.dist(T[t]["pos"], (mundo.arena_size // 2,) * 2), 1)
        d["habia_camino"] = d["pasos_aviso"] is not None
        d["llegaba_saliendo_en_el_aviso"] = (d["instantes_aviso"] is not None and d["instantes_aviso"] < d["tics_aviso_a_muerte"])
        d["llegaba_saliendo_en_el_golpe"] = (d["instantes_golpe"] is not None and d["tics_golpe_a_muerte"] is not None and d["instantes_golpe"] < d["tics_golpe_a_muerte"])
        # el hermano
        d["hermano_vivo_en_aviso"] = warn in To; d["hermano_vivo_en_muerte"] = tm in To
        d["dist_hermano_aviso"] = (max(abs(To[warn]["pos"][0] - T[warn]["pos"][0]), abs(To[warn]["pos"][1] - T[warn]["pos"][1])) if warn in To and warn in T else None)
        d["dist_hermano_muerte"] = (max(abs(To[tm]["pos"][0] - T[tm]["pos"][0]), abs(To[tm]["pos"][1] - T[tm]["pos"][1])) if tm in To else None)
        d["hermano_muere_por_anillo"] = (carp, 21 - sl) in MUERTES_ANILLO
        # que eligio, desde el primer golpe (o el aviso) hasta morir
        t0 = th or warn; w = [t for t in sorted(T) if t0 <= t <= tm]
        d["elige_con_piernas"] = dict(collections.Counter(fam(T[t]["el"]) for t in w if T[t]["listas"]))
        d["tics_con_piernas"] = sum(1 for t in w if T[t]["listas"])
        # filas que hicieron perder a ir_centro
        deltas = collections.defaultdict(list); n_det = 0; gana = collections.Counter(); sin_ic = 0
        for t in w:
            cs = T[t]["cs"]
            if not cs or not T[t]["listas"]:
                continue
            el = T[t]["el"]
            if "ir_centro" not in cs:
                sin_ic += 1; continue
            n_det += 1; gana[fam(el)] += 1
            if el == "ir_centro" or el not in cs:
                continue
            fg, fc = cs[el].get("filas") or {}, cs["ir_centro"].get("filas") or {}
            for k in set(fg) | set(fc):
                deltas[k].append((fg.get(k) or 0.0) - (fc.get(k) or 0.0))
        d["detalle_n"] = n_det; d["detalle_gana"] = dict(gana); d["detalle_sin_ir_centro"] = sin_ic
        d["filas_contra_ir_centro"] = {k: round(sum(v) / len(v), 4) for k, v in sorted(deltas.items(), key=lambda kv: sum(kv[1]) / len(kv[1])) if abs(sum(v) / len(v)) > 1e-4}
        # atribucion: cuanto pesa el miedo y cuanto el hermano en contra de ir_centro (suma de deltas negativos)
        peso_miedo = -sum(sum(v) / len(v) for k, v in deltas.items() if k in MIEDO and sum(v) < 0)
        peso_herm = -sum(sum(v) / len(v) for k, v in deltas.items() if k in HERMANO and sum(v) < 0)
        d["peso_miedo"] = round(peso_miedo, 4); d["peso_hermano"] = round(peso_herm, 4)
        # clase
        if not d["habia_camino"] and d["pasos_golpe"] is None:
            d["clase"] = "iv · no habia salida"
        elif n_det == 0 and d["tics_con_piernas"] == 0:
            d["clase"] = "v · sin piernas listas entre el golpe y la muerte"
        elif peso_miedo > peso_herm and peso_miedo > 0:
            d["clase"] = "ii · lo retuvo el miedo a rivales"
        elif peso_herm > 0:
            d["clase"] = "iii · lo retuvo el hermano"
        elif d["llegaba_saliendo_en_el_aviso"]:
            d["clase"] = "i · llegaba a salvo si salia antes"
        else:
            d["clase"] = "v · otra"
        ANAT.append(d)
    del L
    print(f"    {carp}", flush=True)
json.dump({"fases": FASES, "timeline": {f"{k[0]} f{k[1]}" if isinstance(k, tuple) else k: v for k, v in TL.items()}, "muertes": ANAT, "ultimo_tic": {f"{k[0]}:{k[1]}": v for k, v in LT.items()}},
          open(os.path.join(AQUI, "P6_13_anillo.json"), "w"), ensure_ascii=False, indent=1)
print("### FASES (warn, shrink, done, r0, r1, dps):")
for i, f in enumerate(FASES): print(f"  fase {i+1}: {f}")
print("### TIMELINE (20 partidas, 40 vidas)")
for i in range(len(FASES)):
    print(f"  fase {i+1} warn {FASES[i][0]:5d}: vidas vivas {TL[('vidas vivas en warn', i)]:2d} · parejas enteras {TL[('parejas enteras en warn', i)]:2d} · muertes por anillo en la fase {TL[('muertes por anillo en la fase', i)]}")
print("  los dos vivos en 8076:", TL["los dos vivos en 8076 (cierre de la fase 1)"], "· en 14136:", TL["los dos vivos en 14136 (aviso de la fase final)"])
ult = [v[0] for v in LT.values()]; print(f"  ultimo tic vivo: min {min(ult)} max {max(ult)} · vidas con ultimo tic >= 14916 (radio 0): {sum(1 for t in ult if t >= 14916)} · sobreviven (no eliminated): {sum(1 for v in LT.values() if not v[1])}")
print("  finales de los que NO mueren:", sorted(((k[0][-8:], k[1], v[0], v[2], v[3]) for k, v in LT.items() if not v[1]), key=lambda x: x[2]))
print("  fase de la quemadura que mata:", collections.Counter(d["fase"] for d in ANAT))
print("### ANATOMIA:", len(ANAT), "muertes por anillo")
print(collections.Counter(d["clase"] for d in ANAT))
for d in sorted(ANAT, key=lambda d: d["muerte"]):
    print(f"  {d['carp'][-8:]} s{d['slot']} f{d['fase']} dps{d['dps']} aviso {d['aviso']} golpe {d['primer_golpe']} muerte {d['muerte']} · camino aviso {d['pasos_aviso']}p={d['instantes_aviso']}t (quedaban {d['tics_aviso_a_muerte']}) golpe {d['pasos_golpe']}p={d['instantes_golpe']}t (quedaban {d['tics_golpe_a_muerte']}) · hp aviso {d['hp_en_aviso']} · herm vivo {d['hermano_vivo_en_muerte']} dist {d['dist_hermano_muerte']} · elige {d['elige_con_piernas']} · miedo {d['peso_miedo']} herm {d['peso_hermano']} · {d['clase']}")

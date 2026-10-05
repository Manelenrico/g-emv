"""[P6-2] Diagnostico de la pareja sobre los 20 diarios del GRUPO 2 de P6-1.

SOLO LECTURA. Coste cero. No se juega nada, no se toca codigo del alma.

Los diarios se leen de dos en dos (los dos asientos de un episodio) y se
comprimen a un registro por tic con lo justo, para no cargar 12 GiB.
"""
import collections, glob, json, math, os, re, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U, curiosidad as C
sys.path.insert(0, "paintball")
from alma import appraisal_zs_v42_exp as A42
from alma import parte as PARTE
from motor.model import State as _S, opponent_distance, DEFAULT_CONFIG

HP_MAX = 100.0          # el hp de salida de nuestro cuerpo en el mundo lento


def d_de_filas(F_):
    """La `d` del motor desde las filas crudas. Es `forma.d_con_pisos(F_, None)`,
    que esta declarado bit a bit igual a `opponent_distance(appraise(...))`."""
    pF = nF = pR = nR = pS = nS = 0.0
    for nom, (fF, fR, fS) in A42.REPARTO.items():
        M = float(F_.get(nom) or 0.0)
        if M <= 0.0:
            continue
        aF, aR, aS = M * fF, M * fR, M * fS
        if nom in A42.APETITIVAS:
            pF += aF; pR += aR; pS += aS
        else:
            nF += aF; nR += aR; nS += aS
    return opponent_distance(_S(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS),
                             DEFAULT_CONFIG)

NUESTROS = (10, 11)
CARP = sorted(glob.glob("paintball/runs/P61_t[34]_G2_*"))


def compacta(f):
    """Un diario -> (cfg, mundo, {tic: registro compacto}, voces, final)."""
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    ml = next((r for r in recs if r.get("k") == "mundo_leido"), {})
    fin = next((r for r in recs if r.get("k") == "final"), {})
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    voces = [{"tick": r["tick"], "texto": r["texto"], "largo": len(r["texto"])}
             for r in recs if r.get("k") == "voz"]
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = {
            "pos": tuple(r.get("pos") or ()),
            "hp": r.get("hp"),
            "hand": (r.get("hand") or {}).get("id"),
            "body": (r.get("body") or {}).get("id") if isinstance(r.get("body"), dict) else r.get("body"),
            "pack": [(s or {}).get("id") for s in (r.get("pack") or []) if s],
            "pack_n": {(s or {}).get("id"): int((s or {}).get("n") or 1)
                       for s in (r.get("pack") or []) if s},
            "items": [(x.get("id"), tuple(x.get("pos") or ()), int(x.get("n") or 1))
                      for x in (r.get("ve_items") or []) if x.get("pos")],
            "agentes": [(a.get("slot"), tuple(a.get("pos") or ()),
                         (a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand"),
                         a.get("hp_band"))
                        for a in (r.get("ve_agentes") or []) if a.get("pos")],
            "listas": int(r.get("move_ready_in") or 0) == 0,
            "d_ahora": ra.get("d_ahora"),
            "elegido": ra.get("elegido"),
            "filas": {k: v.get("M") for k, v in
                      ((ra.get("ahora") or {}).get("filas") or {}).items()},
            "cand": ra.get("candidatos"),
            "banda_pareja": (ra.get("ahora") or {}).get("pareja_banda"),
            "B": (ra.get("ahora") or {}).get("B"),
            "medicina": bool((ra.get("ahora") or {}).get("medicina")),
            "chat": [(m.get("from"), m.get("channel"), m.get("text") or "")
                     for m in (r.get("chat") or [])],
            "dano": [(g.get("source"), float(g.get("amount") or 0))
                     for g in (r.get("damage_taken") or [])],
        }
    del recs
    return mundo, pc, T, voces, fin


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def alcance_de(mundo, mano):
    it = (mundo.items or {}).get(mano)
    return float(getattr(it, "range", 0) or 0) if it else 0.0


def clase(mundo, iid, ml=None):
    it = (mundo.items or {}).get(iid)
    if iid == mundo.id_botiquin:
        return "botiquin"
    if iid in (mundo.id_raciones or []):
        return "raciones"
    if iid == mundo.id_mochila:
        return "mochila"
    if iid in (getattr(mundo, "ammo_ids", None) or ("arrows", "darts")):
        return "municion"
    if it is not None and getattr(it, "kind", "") in ("ikMelee", "ikRanged"):
        return "arma"
    if iid in (mundo.id_camuflaje, mundo.id_red):
        return "gear"
    return "otro"


def le_falta(reg, cls, mundo):
    """Test SIMPLE y declarado de «le faltaba justo eso» en ese tic."""
    if cls == "arma":
        return reg["hand"] in (None, "none")
    if cls == "botiquin":
        return reg["pack_n"].get(mundo.id_botiquin, 0) == 0
    if cls == "raciones":
        return not any(reg["pack_n"].get(i, 0) for i in (mundo.id_raciones or []))
    if cls == "mochila":
        return reg["body"] in (None, "none")
    if cls == "municion":
        rg = (mundo.items or {}).get(reg["hand"])
        if rg is None or getattr(rg, "kind", "") != "ikRanged":
            return False
        return not any(reg["pack_n"].get(i, 0)
                       for i in (getattr(mundo, "ammo_ids", None) or ("arrows", "darts")))
    return False


# ══════════════════════════════════════════════════════════════════════════
S = {"voces": [], "pares": 0, "dist": [], "solo_cas": [], "solo_it": [],
     "solo_ag": [], "c": collections.Counter(), "ocasiones": [],
     "armados": [], "muertes": [], "disc": [], "disc_filas": [],
     "chat_recibido": collections.Counter(), "voz_por_diario": [],
     "cambios_parte": [], "dif_M": []}

for carp in CARP:
    fs = {}
    for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
        m = re.search(r"policy_agent_(\d+)\.art\.log$", f)
        if m and int(m.group(1)) in NUESTROS:
            fs[int(m.group(1))] = f
    if len(fs) != 2:
        S["c"]["episodio sin los dos diarios"] += 1
        continue
    D = {}
    for sl, f in fs.items():
        mundo, pc, T, voces, fin = compacta(f)
        D[sl] = {"mundo": mundo, "T": T, "voces": voces, "fin": fin,
                 "herm": pc.get("teammate_slot")}
        S["voz_por_diario"].append({"carpeta": os.path.basename(carp), "slot": sl,
                                    "n": len(voces),
                                    "largos": [v["largo"] for v in voces],
                                    "cadencia": [voces[i]["tick"] - voces[i-1]["tick"]
                                                 for i in range(1, len(voces))]})
        for v in voces:
            S["voces"].append(v["largo"])
    a, b = NUESTROS
    Ta, Tb = D[a]["T"], D[b]["T"]
    mundo = D[a]["mundo"]
    ojo = C.Ojo(mundo, 8)
    juntos = sorted(set(Ta) & set(Tb))
    S["c"]["episodios"] += 1
    S["c"]["tics con los dos vivos"] += len(juntos)
    S["c"]["tics solo uno vivo"] += len(set(Ta) ^ set(Tb))
    # ── 1 · que llega por chat ────────────────────────────────────────────
    for sl, T in ((a, Ta), (b, Tb)):
        for t, r in T.items():
            for de, canal, txt in r["chat"]:
                S["chat_recibido"]["%s | %s | %s" % (
                    canal, "propio" if de == sl else
                    ("hermano" if de == D[sl]["herm"] else "tercero"),
                    "E1" if txt.startswith("E1 ") else "otro")] += 1
    # ── 2 · lo que ve uno y no el otro ────────────────────────────────────
    for t in juntos:
        ra, rb = Ta[t], Tb[t]
        if not (ra["pos"] and rb["pos"]):
            continue
        S["pares"] += 1
        S["dist"].append(cheb(ra["pos"], rb["pos"]))
        va, vb = ojo.vistas_desde(ra["pos"]), ojo.vistas_desde(rb["pos"])
        S["solo_cas"].append((len(va - vb) / len(va), len(vb - va) / len(vb)))
        ia = {(i, p) for i, p, _n in ra["items"]}
        ib = {(i, p) for i, p, _n in rb["items"]}
        if ia or ib:
            S["solo_it"].append((len(ia - ib) / max(1, len(ia)),
                                 len(ib - ia) / max(1, len(ib)),
                                 len(ia), len(ib)))
        ga = {s for s, _p, _h, _b in ra["agentes"] if s not in NUESTROS}
        gb = {s for s, _p, _h, _b in rb["agentes"] if s not in NUESTROS}
        if ga or gb:
            S["solo_ag"].append((len(ga - gb) / max(1, len(ga)),
                                 len(gb - ga) / max(1, len(gb)),
                                 len(ga), len(gb)))
        # 2c · objeto util visto SOLO por uno y que al otro le falta
        for quien, otro, rq, ro in ((a, b, ra, rb), (b, a, rb, ra)):
            iq = {(i, p) for i, p, _n in rq["items"]}
            io = {(i, p) for i, p, _n in ro["items"]}
            for iid, p in (iq - io):
                cls = clase(mundo, iid)
                if cls == "otro":
                    continue
                if not le_falta(ro, cls, mundo):
                    continue
                if (ro["filas"].get("R-CARENCIA") or 0) <= 0:
                    continue
                S["ocasiones"].append({"carpeta": os.path.basename(carp),
                                       "tick": t, "lo_ve": quien,
                                       "le_falta_a": otro, "id": iid,
                                       "clase": cls, "pos": list(p),
                                       "d_al_que_lo_necesita": cheb(p, ro["pos"]),
                                       "d_hermanos": cheb(rq["pos"], ro["pos"]),
                                       "carencia": ro["filas"].get("R-CARENCIA")})
        # 2d · armado visto solo por uno, con el otro a su alcance
        for quien, otro, rq, ro in ((a, b, ra, rb), (b, a, rb, ra)):
            vistos_o = {s for s, _p, _h, _b in ro["agentes"]}
            for s, p, mano, _hb in rq["agentes"]:
                if s in NUESTROS or s in vistos_o:
                    continue
                rg = alcance_de(mundo, mano)
                if rg <= 0:
                    continue
                d = cheb(p, ro["pos"])
                if d <= rg:
                    S["armados"].append({"carpeta": os.path.basename(carp),
                                         "tick": t, "lo_ve": quien,
                                         "en_peligro": otro, "rival": s,
                                         "arma": mano, "alcance": rg,
                                         "d_al_amenazado": d,
                                         "d_hermanos": cheb(rq["pos"], ro["pos"])})
    # ── 1b · EL CONTRAFACTICO DEL TELEGRAMA ──────────────────────────────
    # ¿Cambia el parte alguna DECISION? Se rehace la `d` de cada candidato
    # sustituyendo `S-DANO-PAREJA` por la que habria salido SIN parte (la
    # banda recordada, BANDA_EST) y se mira si el ganador cambia. La `d` se
    # reconstruye de las filas con el mismo algebra del motor.
    for sl, T in ((a, Ta), (b, Tb)):
        # el ultimo parte del hermano, tic a tic
        ult = None
        for t in sorted(T):
            r = T[t]
            for de, canal, txt in r["chat"]:
                if canal == "team" and de == D[sl]["herm"] and txt.startswith("E1 "):
                    pp = PARTE.parsea(txt)
                    if pp is not None:
                        ult = pp
            fresco = (ult is not None and 0 <= t - ult["t"] <= PARTE.CADUCIDAD)
            cand = r["cand"] or {}
            det = {k: v for k, v in cand.items()
                   if isinstance(v, dict) and v.get("filas") is not None}
            if not det or not r["listas"]:
                continue
            S["c"]["tics con detalle y piernas listas"] += 1
            if not fresco:
                S["c"]["  ...sin parte fresco"] += 1
                continue
            S["c"]["  ...con parte fresco"] += 1
            banda = r["banda_pareja"]
            est_sin = A42.BANDA_EST.get(banda, HP_MAX)
            B_ = r["B"] if r["B"] is not None else 1.0
            aten = 0.5 if r["medicina"] else 1.0
            m_sin = max(0.0, (HP_MAX - est_sin) / HP_MAX) * B_ * aten
            gan_con = min(det, key=lambda k: det[k]["d"])
            d_sin = {}
            # OJO: el diario solo guarda las filas con M != 0
            # (`decisor_zs.py:888`), asi que la AUSENCIA de S-DANO-PAREJA
            # significa M = 0, no «falta el dato». Tratarla como ausencia
            # descartaba justo los tics en que el parte dice «estoy a 100» y
            # la banda habria dicho 83.
            for k, v in det.items():
                fl = dict(v["filas"])
                fl["S-DANO-PAREJA"] = m_sin
                d_sin[k] = d_de_filas(fl)
            S["c"]["  ...la fila valia 0 en el detalle"] += (
                1 if "S-DANO-PAREJA" not in det[gan_con]["filas"] else 0)
            gan_sin = min(d_sin, key=lambda k: d_sin[k])
            S["c"]["contrafactico evaluado"] += 1
            if gan_con != gan_sin:
                S["c"]["EL PARTE CAMBIA LA ELECCION"] += 1
                S["cambios_parte"].append({"carpeta": os.path.basename(carp),
                                           "slot": sl, "tick": t,
                                           "con_parte": gan_con,
                                           "sin_parte": gan_sin,
                                           "M_con": det[gan_con]["filas"].get("S-DANO-PAREJA"),
                                           "M_sin": round(m_sin, 5),
                                           "banda": banda})
            else:
                S["c"]["el parte NO cambia la eleccion"] += 1
            S["dif_M"].append((det[gan_con]["filas"].get("S-DANO-PAREJA") or 0.0) - m_sin)

    # ── quien muere primero ───────────────────────────────────────────────
    fa, fb = D[a]["fin"], D[b]["fin"]
    ma, mb = fa.get("match_ticks"), fb.get("match_ticks")
    if ma and mb:
        pri, seg = (a, b) if ma <= mb else (b, a)
        tpri, tseg = (ma, mb) if ma <= mb else (mb, ma)
        Tp, Ts = (Ta, Tb) if pri == a else (Tb, Ta)
        # causa del primero
        ult = [(t, s) for t in range(tpri - 48, tpri + 1) if t in Tp
               for s, _x in Tp[t]["dano"]]
        causa = ult[-1][1] if ult else "no consta"
        herm_pos = Ts.get(tpri, {}).get("pos")
        S["muertes"].append({
            "carpeta": os.path.basename(carp), "primero": pri, "tic": tpri,
            "causa_primero": str(causa), "segundo": seg, "tic_segundo": tseg,
            "sobrevive_despues": tseg - tpri,
            "pos_primero": list(Tp.get(tpri, {}).get("pos") or ()),
            "pos_hermano_entonces": list(herm_pos or ()),
            "d_hermanos_al_morir": (cheb(Tp[tpri]["pos"], herm_pos)
                                    if tpri in Tp and herm_pos else None)})
    # ── 3 · la discrepancia ───────────────────────────────────────────────
    for sl, T in ((a, Ta), (b, Tb)):
        ts = sorted(T)
        listas = [t for t in ts if T[t]["listas"]]
        for i, t in enumerate(listas[:-1]):
            t2 = listas[i + 1]
            r, r2 = T[t], T[t2]
            cand, el = r["cand"], r["elegido"]
            if not cand or el not in (cand or {}):
                continue
            c = cand[el]
            dproy = c["d"] if isinstance(c, dict) else c
            dreal = r2["d_ahora"]
            if dproy is None or dreal is None:
                continue
            S["disc"].append({"carpeta": os.path.basename(carp), "slot": sl,
                              "tick": t, "tick2": t2, "elegido": el,
                              "d_proy": dproy, "d_real": dreal,
                              "disc": dreal - dproy, "hueco": t2 - t})
            if isinstance(c, dict) and c.get("filas") is not None:
                S["disc_filas"].append({"carpeta": os.path.basename(carp),
                                        "slot": sl, "tick": t, "tick2": t2,
                                        "d_proy": dproy, "d_real": dreal,
                                        "proy": c["filas"], "real": r2["filas"]})
    del D, Ta, Tb, ojo
    print(f"  {os.path.basename(carp)}: listo", flush=True)

json.dump(S, open("cantera/paper6/P6_2_bruto.json", "w"), ensure_ascii=False)
print("\n-> cantera/paper6/P6_2_bruto.json")
print("resumen rapido:", dict(S["c"]))
print("voces:", len(S["voces"]), "· ocasiones 2c:", len(S["ocasiones"]),
      "· armados 2d:", len(S["armados"]),
      "· discrepancias:", len(S["disc"]), "· con filas:", len(S["disc_filas"]))

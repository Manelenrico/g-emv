"""[P5-8M] Los sellos K1 a K7 y lo que va sin sello, sobre los diarios de una o
varias tandas.

  python3 cantera/paper5/mide_P58M.py 0
  python3 cantera/paper5/mide_P58M.py 1 2 3 4

Diarios de UNO EN UNO (la regla del banco). Nada se cablea: el paso del mundo,
el radio de vision y los alcances se LEEN.
"""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U, curiosidad as C
from alma import appraisal_zs_v42_exp as A          # la W se IMPORTA, no se copia


def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def med(v): return round(st.median(v), 5) if v else None


TANDAS = [a for a in sys.argv[1:] if not a.startswith("-")] or ["0"]
ASIENTOS = []

for tanda in TANDAS:
    for f in sorted(glob.glob(f"paintball/runs/P58M_t{tanda}_*/*.art.log")):
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            print("  sin cabecera:", f); continue
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        herm = pc.get("teammate_slot")
        carpeta = os.path.basename(os.path.dirname(f))       # P58M_t0_K_2026...
        brazo, semilla = carpeta.split("_")[2], carpeta.split("_")[3]
        slot = f.rsplit("_", 1)[1][:2]
        vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
        if not vivos:
            continue
        por_tic = {r["tick"]: r for r in vivos}
        ctic = {r["tick"]: r for r in recs if r.get("k") == "cur_forma_tic"}
        tiem = [r for r in recs if r.get("k") == "tiempo_tic"]
        fin_r = next((r for r in recs if r.get("k") == "final"), {})
        prop = {r["id"]: r for r in recs
                if r.get("k") == "forma_propuesta" and r.get("origen") == "curiosidad"}
        ev = [r for r in recs if r.get("k") == "forma_evaluada" and r.get("id") in prop]
        acep = {r["id"]: r["tick"] for r in recs if r.get("k") == "forma_aceptada"}
        fin = {r["id"]: (r["tick"], str(r.get("motivo") or ""))
               for r in recs if r.get("k") == "forma_caida"}
        comp = [r for r in recs if r.get("k") == "compromiso"]
        rodeos = [r for r in recs if r.get("k") == "rodeo"]          # [P5-8M]
        # el botin: `social.cogio` por tic
        cogio_t = {r["tick"] for r in vivos
                   if (r.get("social") or {}).get("cogio")}

        # ── el ojo, tic a tic ──
        ojo = C.Ojo(mundo, 8); visto_en = {}
        for r in vivos:
            p = tuple(r.get("pos") or ())
            if not p: continue
            for c in ojo.vistas_desde(p):
                visto_en.setdefault(c, r["tick"])
            ojo.mira(p, r["tick"])

        # ── los intervalos de forma activa ──
        dentro_t = {t for t, r in ctic.items() if r.get("activa") is not None}
        t_dentro = len(dentro_t & set(por_tic)); t_fuera = len(por_tic) - t_dentro
        n_dentro = sum(1 for c, t in visto_en.items() if t in dentro_t)
        n_fuera = len(visto_en) - n_dentro

        # ── daño por tic (sin el anillo) y armados ──
        dano_en = {}
        for r in vivos:
            d = sum(float(x.get("amount") or 0) if isinstance(x, dict) else 0.0
                    for x in (r.get("damage_taken") or [])
                    if str((x or {}).get("source")) != "zone")
            if d > 0:
                dano_en[r["tick"]] = d
        t_dano = sorted(dano_en)
        dano_hist = [(r["tick"], sum(float(x.get("amount") or 0)
                                     if isinstance(x, dict) else 0.0
                                     for x in (r.get("damage_taken") or [])))
                     for r in recs if r.get("k") == "tick"]

        def _armados(r):
            return [(tuple(a["pos"]), C._alcance(mundo, a.get("hand")))
                    for a in (r.get("ve_agentes") or [])
                    if a.get("slot") != herm and a.get("pos")
                    and C._alcance(mundo, a.get("hand")) > 0]

        def _grado(r, t):
            # OJO: `0 <= t - tt` es imprescindible. Sin el, el dano FUTURO
            # cuenta en el presente (t - tt sale negativo, que tambien es
            # menor que la ventana) y TODOS los tics salen «inseguro».
            d100 = sum(v for (tt, v) in dano_hist
                       if 0 <= t - tt < C.VENTANA_DANO)
            am, _ = C.amenaza(r, mundo, herm, d100, t)
            return C.grado(am), am          # la funcion del modulo, no una copia

        t_dano = sorted(dano_en)
        # ── K3 · armado a tiro con forma activa · y el desglose de P5-7C ──
        # [P5-8M t2] DOS lecturas: la SELLADA (todo tic con forma activa) y la
        # del MECANISMO (solo con las piernas listas, que es cuando el
        # compromiso mira las rupturas; en enfriamiento manda el decisor y el
        # candidato de la forma ni esta en la papeleta — comprobado: 0/1825).
        k3 = 0
        k3_listas = 0
        desg = {g: collections.Counter() for g in ("seguro", "neutro", "inseguro")}
        for t, r in por_tic.items():
            g, _am = _grado(r, t)
            p0 = tuple(r.get("pos") or ())
            arm = _armados(r)
            caja = desg[g]
            caja["decisiones"] += 1
            a_tiro = bool(p0 and any(cheb(p0, q) <= rg for q, rg in arm))
            if a_tiro:
                caja["armado_a_tiro"] += 1
                if t in dentro_t:
                    k3 += 1
                    if int(r.get("move_ready_in") or 0) == 0:
                        k3_listas += 1
            if p0 and arm:
                caja["con_armado_a_la_vista"] += 1
                q = min((q for q, _ in arm), key=lambda q: cheb(p0, q))
                sig = por_tic.get(t + 1)
                p1 = tuple((sig or {}).get("pos") or ()) if sig else None
                if p1 and cheb(p1, q) < cheb(p0, q):
                    caja["acerca_al_armado"] += 1
            if any(t < u <= t + 50 for u in t_dano):
                caja["dano_en_50"] += 1
            if t in dentro_t:
                caja["en_forma"] += 1
                if any(t < u <= t + 50 for u in t_dano):
                    caja["dano_en_50_en_forma"] += 1

        # ── [P5-8M t3] VIDA, MARCADOR Y SUS PIEZAS ──
        # (1) K2 separado: vida = tics vivo y hp final · puesto = placement
        # (2) de que esta hecha la puntuacion: bajas, dano hecho, botin
        vida_tics = len(por_tic)
        ult = vivos[-1]
        dano_hecho = sum(float(r.get("damage_dealt") or 0) for r in vivos)
        bajas = max((int(r.get("kills") or 0) for r in vivos), default=0)
        cogidos = len(cogio_t)
        soltados = sum(1 for r in vivos if (r.get("social") or {}).get("solto"))
        dano_recibido = sum(dano_en.values())

        # ── K6 · el hilo ──
        ms = [r["ms"] for r in tiem if r.get("ms") is not None]
        # [P5-8M t3] el ms separado: tics CON nacimiento de forma y sin el.
        # Cada nacimiento paga un BFS; esto dice cuanto.
        t_nace = {r["tick"] for r in recs
                  if r.get("k") == "forma_propuesta" and r.get("origen") == "curiosidad"}
        ms_nace = [r["ms"] for r in tiem
                   if r.get("ms") is not None and r.get("tick") in t_nace]
        ms_sin = [r["ms"] for r in tiem
                  if r.get("ms") is not None and r.get("tick") not in t_nace]
        perdidos = sum(1 for r in vivos if (r.get("RADIOGRAFIA") or {}).get("elegido") is None)

        # ── K2 · vida y puesto ──
        muertes_dentro = sum(1 for t in dentro_t
                             if (por_tic.get(t) or {}).get("hp") == 0)

        # ── 1 · aceptación · 2 · el margen ──
        nac, ac = len(prop), len([i for i in acep if i in prop])
        Ws = [p["W"] for p in prop.values() if p.get("W") is not None]
        Am = [p["amenaza"] for p in prop.values() if p.get("amenaza") is not None]
        ven = [r["ventaja"] for r in ev if r.get("ventaja") is not None]
        mgs = [r["margen"] for r in ev if r.get("margen") is not None]
        vers = collections.Counter(r.get("veredicto") for r in ev)

        # ── 3 · el compromiso ──
        ob = [r for r in comp if r.get("estado") == "obedece"]
        ro = [r for r in comp if r.get("estado") == "rompe"]
        en = [r for r in comp if r.get("estado") == "enfriamiento"]
        contra = [r for r in ob if r.get("habria_ganado")
                  and r.get("habria_ganado") != r.get("paso")]
        c_contra = [r["coste"] for r in contra if r.get("coste") is not None]
        causas = collections.Counter(r.get("causa") for r in ro)

        # ── las formas aceptadas, una a una ──
        formas = []
        for fid, t0 in acep.items():
            p0 = prop.get(fid)
            if not p0 or not p0.get("destino"): continue
            dest = tuple(p0["destino"])
            t1, motivo = fin.get(fid, (vivos[-1]["tick"], "sin fin"))
            tics = [t for t in range(t0, t1 + 1) if t in por_tic]
            if len(tics) < 2: continue
            prev = tuple(por_tic[tics[0]].get("pos") or ())
            d0 = cheb(prev, dest)
            for t in tics[1:]:
                p = tuple(por_tic[t].get("pos") or ())
                if p: prev = p
            objetivo = {c for c in ojo.vistas_desde(dest)
                        if visto_en.get(c, 10 ** 9) >= t0}
            dur = sum(1 for c in objetivo if t0 <= visto_en.get(c, 10**9) <= t1)
            desp = sum(1 for c in objetivo if t1 < visto_en.get(c, 10**9) <= t1 + 100)
            def _W(t):
                r = por_tic.get(t)
                if not r:
                    return None
                try:
                    return round(float(A.riqueza_W(
                        {"hand": r.get("hand"), "pack": r.get("pack"),
                         "body": r.get("body")}, mundo)[0]), 4)
                except Exception:
                    return None
            _rr = [x for x in rodeos if x.get("id") == fid]
            formas.append({"id": fid, "motivo": motivo[:30], "vive": t1 - t0,
                           "d0": d0, "d1": cheb(prev, dest), "obj": len(objetivo),
                           "durante": dur, "despues": desp,
                           "nunca": len(objetivo) - dur - desp,
                           "dist_nace": (prop[fid] or {}).get("dist"),
                           "rodeos": len(_rr),
                           "extra": [x.get("extra") for x in _rr],
                           "W0": _W(t0), "W1": _W(t1),
                           # K5 POR FORMA (correccion de P5-8L), no por tic
                           "dano_durante": any(t0 <= u <= t1 for u in t_dano),
                           "dano_tras_50": any(t1 < u <= t1 + 50 for u in t_dano),
                           "cogio_durante": len([t for t in cogio_t
                                                 if t0 <= t <= t1])})

        ASIENTOS.append({
            "tanda": tanda, "brazo": brazo, "semilla": semilla, "slot": slot,
            "tics": len(por_tic), "t_dentro": t_dentro, "t_fuera": t_fuera,
            "nuevas_dentro": n_dentro, "nuevas_fuera": n_fuera,
            "nacidas": nac, "aceptadas": ac, "veredictos": dict(vers),
            "W_med": med(Ws), "amenaza_med": med(Am),
            "ventaja_med": med(ven), "margen_med": med(mgs),
            "obedece": len(ob), "rompe": len(ro), "enfria": len(en),
            "contra": len(contra),
            "coste_contra": round(sum(c_contra), 5) if c_contra else 0.0,
            "causas": dict(causas), "formas": formas,
            "k3_armado_a_tiro_en_forma": k3,
            "k3_listas": k3_listas,
            "t_dentro_listas": sum(1 for t in dentro_t
                                   if t in por_tic
                                   and int(por_tic[t].get("move_ready_in") or 0) == 0),
            # [P5-8M t2] para leer por que unas semillas nacen 5 y otras 150
            "ign_inicial": next((r.get("ign") for r in
                                 sorted(ctic.values(), key=lambda x: x["tick"])
                                 if r.get("ign") is not None), None),
            "tics_seguro": (desg.get("seguro") or {}).get("decisiones", 0),
            "tics_neutro": (desg.get("neutro") or {}).get("decisiones", 0),
            "tics_inseguro": (desg.get("inseguro") or {}).get("decisiones", 0),
            "ms_med": med(ms), "ms_max": (round(max(ms), 3) if ms else None),
            "perdidos": perdidos,
            "muertes_dentro": muertes_dentro,
            "puesto": fin_r.get("placement"), "hp_final": vivos[-1].get("hp"),
            "score": fin_r.get("score"), "reason": fin_r.get("reason"),
            "match_ticks": fin_r.get("match_ticks"),
            "vida_tics": vida_tics, "hp_ult": ult.get("hp"),
            "bajas": bajas, "dano_hecho": round(dano_hecho, 2),
            "dano_recibido": round(dano_recibido, 2),
            "cogidos": cogidos, "soltados": soltados,
            "ms_nace_med": med(ms_nace), "ms_sin_med": med(ms_sin),
            "n_nace": len(ms_nace), "n_sin": len(ms_sin),
            # (3) para las ventanas emparejadas: cuando se vio cada casilla
            "visto_en": {f"{c[0]},{c[1]}": t for c, t in visto_en.items()},
            "desglose": {g: dict(v) for g, v in desg.items()},
            "n_rodeos": len(rodeos),
            "sin_rodeo": sum(1 for r in recs if r.get("k") == "forma_caida"
                             and str(r.get("motivo") or "").startswith("sin rodeo")),
            "cogio_dentro": len([t for t in cogio_t if t in dentro_t]),
            "cogio_fuera": len([t for t in cogio_t if t not in dentro_t]),
        })
        print(f"  t{tanda} {brazo}/{semilla}/{slot}: {len(por_tic)} tics · "
              f"{nac} nac · {ac} acep · obedece {len(ob)} (contra {len(contra)}) "
              f"· rompe {len(ro)} · ms {med(ms)} · perdidos {perdidos}", flush=True)

et = "_".join(TANDAS)
json.dump(ASIENTOS, open(f"cantera/paper5/P58M_{et}.json", "w"), ensure_ascii=False)
print(f"\n{len(ASIENTOS)} asientos · cantera/paper5/P58M_{et}.json")

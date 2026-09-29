"""[P5-8K] Los sellos K1 a K7 y lo que va sin sello, sobre los diarios de una o
varias tandas.

  python3 cantera/paper5/mide_P58K.py 0
  python3 cantera/paper5/mide_P58K.py 1 2 3 4

Diarios de UNO EN UNO (la regla del banco). Nada se cablea: el paso del mundo,
el radio de vision y los alcances se LEEN.
"""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U, curiosidad as C


def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def med(v): return round(st.median(v), 5) if v else None


TANDAS = [a for a in sys.argv[1:] if not a.startswith("-")] or ["0"]
ASIENTOS = []

for tanda in TANDAS:
    for f in sorted(glob.glob(f"paintball/runs/P58K_t{tanda}_*/*.art.log")):
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            print("  sin cabecera:", f); continue
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        herm = pc.get("teammate_slot")
        carpeta = os.path.basename(os.path.dirname(f))       # P58K_t0_K_2026...
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

        # ── K3 · armado a tiro con forma activa · y el desglose de P5-7C ──
        k3 = 0
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

        # ── K6 · el hilo ──
        ms = [r["ms"] for r in tiem if r.get("ms") is not None]
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
            formas.append({"id": fid, "motivo": motivo[:30], "vive": t1 - t0,
                           "d0": d0, "d1": cheb(prev, dest), "obj": len(objetivo),
                           "durante": dur, "despues": desp,
                           "nunca": len(objetivo) - dur - desp})

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
            "ms_med": med(ms), "ms_max": (round(max(ms), 3) if ms else None),
            "perdidos": perdidos,
            "muertes_dentro": muertes_dentro,
            "puesto": fin_r.get("placement"), "hp_final": vivos[-1].get("hp"),
            "desglose": {g: dict(v) for g, v in desg.items()},
        })
        print(f"  t{tanda} {brazo}/{semilla}/{slot}: {len(por_tic)} tics · "
              f"{nac} nac · {ac} acep · obedece {len(ob)} (contra {len(contra)}) "
              f"· rompe {len(ro)} · ms {med(ms)} · perdidos {perdidos}", flush=True)

et = "_".join(TANDAS)
json.dump(ASIENTOS, open(f"cantera/paper5/P58K_{et}.json", "w"), ensure_ascii=False)
print(f"\n{len(ASIENTOS)} asientos · cantera/paper5/P58K_{et}.json")

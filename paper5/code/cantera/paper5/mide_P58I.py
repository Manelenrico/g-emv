"""[P5-8I] Los cinco puntos de la sonda de cinco semillas. En seco sobre los diarios."""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U, curiosidad as C


def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def med(v): return round(st.median(v), 5) if v else None


ASIENTOS = []
PAT = sys.argv[1] if len(sys.argv) > 1 else "P58I_t1_*"
for f in sorted(glob.glob(f"paintball/runs/{PAT}/*.art.log")):
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        print("  sin cabecera:", f); continue
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    carpeta = os.path.basename(os.path.dirname(f))          # P58I_t1_K_20260916
    brazo, semilla = carpeta.split("_")[2], carpeta.split("_")[3]  # P58x_t1_K_sem
    slot = f.rsplit("_", 1)[1][:2]
    vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
    if not vivos:
        print("  sin tics vivos:", f); continue
    por_tic = {r["tick"]: r for r in vivos}
    ctic = {r["tick"]: r for r in recs if r.get("k") == "cur_forma_tic"}
    prop = {r["id"]: r for r in recs
            if r.get("k") == "forma_propuesta" and r.get("origen") == "curiosidad"}
    ev = [r for r in recs if r.get("k") == "forma_evaluada" and r.get("id") in prop]
    acep = {r["id"]: r["tick"] for r in recs if r.get("k") == "forma_aceptada"}
    fin = {r["id"]: (r["tick"], str(r.get("motivo") or ""))
           for r in recs if r.get("k") == "forma_caida"}
    comp = [r for r in recs if r.get("k") == "compromiso"]

    # ── el ojo, reproducido tic a tic (la MISMA clase que usa el BFS) ──
    ojo = C.Ojo(mundo, 8); visto_en = {}
    for r in vivos:
        p = tuple(r.get("pos") or ())
        if not p: continue
        for c in ojo.vistas_desde(p):
            visto_en.setdefault(c, r["tick"])
        ojo.mira(p, r["tick"])

    # ── 4 · dentro / fuera de forma ──
    dentro_t = {t for t, r in ctic.items() if r.get("activa") is not None}
    t_dentro = len(dentro_t & set(por_tic))
    t_fuera = len(por_tic) - t_dentro
    n_dentro = sum(1 for c, t in visto_en.items() if t in dentro_t)
    n_fuera = len(visto_en) - n_dentro

    # ── 1 · aceptacion, W y amenaza ──
    nac = len(prop)
    ac = len([i for i in acep if i in prop])
    Ws = [p["W"] for p in prop.values() if p.get("W") is not None]
    Am = [p["amenaza"] for p in prop.values() if p.get("amenaza") is not None]

    # ── 2 · el margen, contrafactual ──
    cf = {"n": 0, "vida": 0, "ok_real": 0}
    for m in (0.02, 0.04):
        cf[f"m{m}"] = 0
    cf["m_vigor"] = 0; cf["margenes"] = []
    for r in ev:
        if r.get("ventaja") is None: continue
        cf["n"] += 1
        v, ver, mg = r["ventaja"], r.get("veredicto"), r.get("margen")
        if mg is not None: cf["margenes"].append(mg)
        if ver == "vida":
            cf["vida"] += 1; continue        # el margen no la rescata
        if ver == "ok": cf["ok_real"] += 1
        if mg is not None and v > mg: cf["m_vigor"] += 1
        for m in (0.02, 0.04):
            if v > m: cf[f"m{m}"] += 1

    # ── 3 · el compromiso ──
    ob = [r for r in comp if r.get("estado") == "obedece"]
    ro = [r for r in comp if r.get("estado") == "rompe"]
    en = [r for r in comp if r.get("estado") == "enfriamiento"]
    contra = [r for r in ob if r.get("habria_ganado")
              and r.get("habria_ganado") != r.get("paso")]
    coste_contra = [r["coste"] for r in contra if r.get("coste") is not None]
    coste_todo = [r["coste"] for r in ob if r.get("coste") is not None]
    causas = collections.Counter(r.get("causa") for r in ro)

    # ── 3b · por forma aceptada: distancia, motivo, prometido/visto ──
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
        d1 = cheb(prev, dest)
        objetivo = {c for c in ojo.vistas_desde(dest)
                    if visto_en.get(c, 10 ** 9) >= t0}
        durante = sum(1 for c in objetivo if t0 <= visto_en.get(c, 10 ** 9) <= t1)
        despues = sum(1 for c in objetivo if t1 < visto_en.get(c, 10 ** 9) <= t1 + 100)
        formas.append({"id": fid, "motivo": motivo[:30], "vive": t1 - t0,
                       "d0": d0, "d1": d1, "obj": len(objetivo),
                       "durante": durante, "despues": despues,
                       "nunca": len(objetivo) - durante - despues})

    ASIENTOS.append({
        "brazo": brazo, "semilla": semilla, "slot": slot,
        "tics": len(por_tic), "t_dentro": t_dentro, "t_fuera": t_fuera,
        "nuevas_dentro": n_dentro, "nuevas_fuera": n_fuera,
        "por100_dentro": round(100.0 * n_dentro / t_dentro, 2) if t_dentro else None,
        "por100_fuera": round(100.0 * n_fuera / t_fuera, 2) if t_fuera else None,
        "nacidas": nac, "aceptadas": ac,
        "W_med": med(Ws), "amenaza_med": med(Am),
        "margen": cf,
        "obedece": len(ob), "rompe": len(ro), "enfria": len(en),
        "contra": len(contra),
        "coste_contra": round(sum(coste_contra), 5) if coste_contra else 0.0,
        "coste_contra_med": med(coste_contra),
        "coste_todo": round(sum(coste_todo), 5) if coste_todo else 0.0,
        "causas": dict(causas), "formas": formas,
    })
    print(f"  {brazo}/{semilla}/{slot}: {len(por_tic)} tics · "
          f"{nac} nacidas · {ac} aceptadas · obedece {len(ob)} "
          f"(contra {len(contra)}) · rompe {len(ro)}", flush=True)

json.dump(ASIENTOS, open("cantera/paper5/P58I.json", "w"), ensure_ascii=False)
print(f"\n{len(ASIENTOS)} asientos · cantera/paper5/P58I.json")

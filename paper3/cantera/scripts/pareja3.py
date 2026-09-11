"""LA PAREJA, TERCERA TANDA — PROMPT_60. Varas V1-V7 sobre runs/pareja3 (v31),
pareado contra runs/pareja2 (v30) con METODO IDENTICO.

La vara nueva del 60: LA PROVISION EN CALMA (baseline 0 por construccion en
v30: la fila no existia). Se detecta del diario por S-PROVISION>0 en la
radiografia del AHORA (solo enciende con hermana b=0, yo>=2, calma).

Uso (desde la raiz del repo):  python3 paintball/pareja3.py
"""
from __future__ import annotations

import glob
import json
import math
import os
import statistics as st

from pareja import lee, analiza_gemela

P = os.path.dirname(os.path.abspath(__file__))
BANDA = 30.0


def diario_en(base, eid, s):
    fs = glob.glob(f"{base}/{eid}/a{s}/*.log") + glob.glob(f"{base}/{eid}/a{s}/*.jsonl")
    return list(lee(sorted(fs)[0])) if fs else None


def provision_de(recs):
    """Recorre el diario y extrae la ocasion y las entregas en calma."""
    tics_ocasion = 0
    soltares_calma = []          # (tick, pos) de soltar con S-PROVISION activa
    m_max = 0.0
    serie = {}                   # tick -> {"prov": M, "el": elegido, "pos": pos, "bhermana": b}
    for d in recs:
        if d.get("k") != "tick" or d.get("phase") != "live":
            continue
        rad = d.get("RADIOGRAFIA") or {}
        ah = rad.get("ahora") or {}
        fil = ah.get("filas") or {}
        m = (fil.get("S-PROVISION") or {}).get("M", 0) or 0
        el = rad.get("elegido")
        t = d.get("tick", 0)
        parte = ah.get("parte") or {}
        serie[t] = {"prov": m, "el": el, "pos": tuple(d.get("pos") or ()),
                    "bh": parte.get("botiquin")}
        if m > 0:
            tics_ocasion += 1
            m_max = max(m_max, m)
            if (el or "").startswith("soltar"):
                soltares_calma.append((t, tuple(d.get("pos") or ())))
    return {"tics_ocasion": tics_ocasion, "soltares_calma": soltares_calma,
            "m_max": m_max, "serie": serie}


def carga(nombre):
    base = f"{P}/runs/{nombre}"
    D = json.load(open(f"{base}/episodios.json"))
    filas = []
    for e in D["eps"]:
        eid = e["id"]
        try:
            r = json.load(open(f"{base}/res_{eid}.json"))
        except FileNotFoundError:
            continue
        d10, d11 = diario_en(base, eid, 10), diario_en(base, eid, 11)
        if not d10 or not d11:
            continue
        A = analiza_gemela(d10, 10, 11)
        Bg = analiza_gemela(d11, 11, 10)
        PA = provision_de(d10)
        PB = provision_de(d11)
        pt = {}
        for recs, key in ((d10, "A"), (d11, "B")):
            for d in recs:
                if d.get("k") == "tick" and d.get("phase") == "live":
                    pt.setdefault(d["tick"], {})[key] = {
                        "pos": tuple(d.get("pos") or ()),
                        "hp": float(d.get("hp") or 0)}
        filas.append({"eid": eid, "p10": r["placements"][10],
                      "p11": r["placements"][11], "A": A, "B": Bg,
                      "PA": PA, "PB": PB, "pt": pt,
                      "bot10": _bot_serie(d10), "bot11": _bot_serie(d11)})
    return filas


def _bot_serie(recs):
    out = {}
    for d in recs:
        if d.get("k") == "tick":
            out[d.get("tick", 0)] = sum(int(x.get("n") or 1)
                                        for x in (d.get("pack") or [])
                                        if x and x.get("id") == "first_aid")
    return out


def metr(filas, nombre):
    n = len(filas)
    M = {"nombre": nombre, "n": n}
    M["inici"] = sum(f[g]["iniciaciones"] for f in filas for g in ("A", "B"))
    M["ataques"] = sum(f[g]["ataques"] for f in filas for g in ("A", "B"))
    M["golpes_h"] = sum(f[g]["golpes_de_hermana"] for f in filas for g in ("A", "B"))
    M["vinculo"] = sum(f[g]["vinculo_tics"] for f in filas for g in ("A", "B"))
    # V2 la ocasion (solo v31 la tiene; v30 = 0 por construccion)
    M["ocasion_tics"] = sum(f[gp]["tics_ocasion"] for f in filas for gp in ("PA", "PB"))
    M["ocasion_eps"] = sum(1 for f in filas
                           if f["PA"]["tics_ocasion"] or f["PB"]["tics_ocasion"])
    # V3 entregas en calma
    solt = [(f["eid"], "10" if gp == "PA" else "11", t, pos)
            for f in filas for gp in ("PA", "PB")
            for t, pos in f[gp]["soltares_calma"]]
    M["entregas_calma"] = len(solt)
    M["entregas_calma_eps"] = len(set((f["eid"]) for f in filas
                                      for gp in ("PA", "PB")
                                      if f[gp]["soltares_calma"]))
    M["solt_list"] = solt
    # V6 moneda
    mejor = [min(f["p10"], f["p11"]) for f in filas]
    M["top4"] = sum(1 for m in mejor if m <= 4)
    M["wins"] = sum(1 for m in mejor if m == 1)
    M["podio"] = sum(1 for f in filas if {f["p10"], f["p11"]} <= {1, 2})
    M["mejor_med"] = st.median(mejor)
    M["ambas8"] = sum(1 for f in filas if f["p10"] <= 8 and f["p11"] <= 8)
    # V5/V4 distancia y banda-con-venda
    dists, dist_banda, cerca = [], [], 0
    banda_tics = banda_con_venda = 0
    for f in filas:
        for me, otra, bot_me in (("A", "B", "bot10"), ("B", "A", "bot11")):
            pass
        for t, par in sorted(f["pt"].items()):
            if "A" not in par or "B" not in par:
                continue
            pa, pb = par["A"], par["B"]
            if not pa["pos"] or not pb["pos"] or pa["hp"] <= 0 or pb["hp"] <= 0:
                continue
            dv = math.dist(pa["pos"], pb["pos"])
            dists.append(dv)
            if pa["hp"] < BANDA or pb["hp"] < BANDA:
                dist_banda.append(dv)
                if dv <= 2:
                    cerca += 1
        # V4: tics en banda de cada una con venda a bordo
        for me, botm in (("A", "bot10"), ("B", "bot11")):
            hp = f[me]["hp_por_tick"]
            for t, h in hp.items():
                if 0 < h < BANDA:
                    banda_tics += 1
                    if f[botm].get(t, 0) > 0:
                        banda_con_venda += 1
    M["dist_med"] = st.median(dists) if dists else None
    M["dist_banda_med"] = st.median(dist_banda) if dist_banda else None
    M["banda_cerca_pct"] = 100 * cerca / max(len(dist_banda), 1)
    M["banda_tics"] = banda_tics
    M["banda_con_venda_pct"] = 100 * banda_con_venda / max(banda_tics, 1)
    # V5 dones tras entrada en banda
    p2d = p2n = 0
    for f in filas:
        for me, otra in (("A", "B"), ("B", "A")):
            eb = f[me]["banda_entra"]
            if eb is None:
                continue
            mo = f[otra]["muerte"] or 0
            if mo <= eb:
                continue
            if any(b > 0 for t, b in f[otra]["pack_bot_por_tick"].items() if t >= eb):
                p2d += 1
                if any(d["tick"] >= eb for d in f[otra]["dones"]):
                    p2n += 1
    M["donesb_den"], M["donesb_num"] = p2d, p2n
    # V7 estabilidad
    M["cool"] = st.median([f[g]["final"]["tics_cooldown"] for f in filas
                           for g in ("A", "B") if f[g]["final"]])
    M["cong"] = st.median([f[g]["final"]["tics_congelado"] for f in filas
                           for g in ("A", "B") if f[g]["final"]])
    M["banda_diario"] = st.median([f[g]["banda_tics"] for f in filas
                                   for g in ("A", "B")])
    return M


def recoge(f, quien_da, t0):
    """¿La hermana recoge la venda soltada en t0? (su botiquin sube tras t0)."""
    otra_bot = f["bot11"] if quien_da == "10" else f["bot10"]
    base = otra_bot.get(t0, 0)
    subes = [t for t, b in sorted(otra_bot.items()) if t > t0 and b > base]
    return subes[0] if subes else None


def main():
    v31 = carga("pareja3")
    v30 = carga("pareja2")
    M1, M0 = metr(v31, "v31"), metr(v30, "v30 (57)")
    print("=" * 92)
    print(f"LA PAREJA, TERCERA TANDA — v31 ({M1['n']} eps) vs v30 del 57 ({M0['n']} eps)")
    print("=" * 92)
    for M in (M1, M0):
        n = M["n"]
        print(f"\n  [{M['nombre']}]")
        print(f"  V1 honor: ataques {M['ataques']} · INICIACIONES {M['inici']} · "
              f"golpes entre hermanas {M['golpes_h']} · S-VINCULO {M['vinculo']}")
        print(f"  V2 LA OCASION: tics con S-PROVISION>0 {M['ocasion_tics']} en "
              f"{M['ocasion_eps']} eps  (v30: 0 por construccion)")
        print(f"  V3 ENTREGAS EN CALMA: {M['entregas_calma']} soltares en "
              f"{M['entregas_calma_eps']} eps "
              f"({100*M['entregas_calma_eps']/max(M['ocasion_eps'],1):.0f}% de los eps con ocasion)")
        print(f"  V4 banda con venda a bordo: {M['banda_con_venda_pct']:.0f}% "
              f"({M['banda_tics']} tics en banda)")
        print(f"  V5 dist mediana {M['dist_med']:.1f} · en banda {M['dist_banda_med']:.1f} · "
              f"a<=2 con banda {M['banda_cerca_pct']:.0f}% · juntas8 {M['ambas8']}/{n} "
              f"({100*M['ambas8']/n:.0f}%) · dones-b {M['donesb_num']}/{M['donesb_den']}")
        print(f"  V6 moneda: top4 {M['top4']}/{n} ({100*M['top4']/n:.0f}%) · "
              f"wins {M['wins']} · podio {M['podio']} · mejor-med {M['mejor_med']}")
        print(f"  V7: cooldown {M['cool']:.0f} · congelado {M['cong']:.0f} · "
              f"banda/diario {M['banda_diario']:.0f}")
    print("\n  ENTREGAS EN CALMA v31 (soltar con S-PROVISION activa -> ¿recoge?):")
    fmap = {f["eid"]: f for f in v31}
    for eid, quien, t0, pos in M1["solt_list"]:
        rec = recoge(fmap[eid], quien, t0)
        print(f"    {eid[:18]} gemela{quien} t{t0} pos{pos}: "
              f"recoge {('t'+str(rec)) if rec else 'NO'}")
    json.dump({"v31": {k: v for k, v in M1.items() if k != "solt_list"},
               "v30": {k: v for k, v in M0.items() if k != "solt_list"}},
              open(f"{P}/runs/pareja3/resumen.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

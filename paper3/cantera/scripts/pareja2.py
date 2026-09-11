"""LA PAREJA, SEGUNDA TANDA — PROMPT_57. Varas V1-V6 sobre runs/pareja2 (v30),
pareadas contra runs/pareja (v29, el 55) con METODO IDENTICO.

Novedad de metodo (declarada): la distancia entre hermanas se mide con las
POSICIONES VERDADERAS de los dos diarios (tick a tick, ambas vivas), no solo
cuando una ve a la otra — v30 sabe sin ver, y la vara tiene que medir igual
en ambos brazos. El 55 midio "vista" (3,6/5,1); aqui se recalcula el brazo
v29 con este metodo para parear limpio.

Uso (desde la raiz del repo):  python3 paintball/pareja2.py
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
    if not fs:
        return None
    return list(lee(sorted(fs)[0]))


def carga(nombre):
    base = f"{P}/runs/{nombre}"
    D = json.load(open(f"{base}/episodios.json"))
    filas = []
    for e in D["eps"]:
        eid = e["id"]
        r = json.load(open(f"{base}/res_{eid}.json"))
        d10 = diario_en(base, eid, 10)
        d11 = diario_en(base, eid, 11)
        if not d10 or not d11:
            continue
        A = analiza_gemela(d10, 10, 11)
        Bg = analiza_gemela(d11, 11, 10)
        # posiciones y elegidos por tic (para la distancia VERDADERA y el camino)
        pt = {}
        for recs, key in ((d10, "A"), (d11, "B")):
            for d in recs:
                if d.get("k") == "tick" and d.get("phase") == "live":
                    pt.setdefault(d["tick"], {})[key] = {
                        "pos": tuple(d.get("pos") or ()),
                        "hp": float(d.get("hp") or 0),
                        "el": (d.get("RADIOGRAFIA") or {}).get("elegido"),
                        "pp": ((d.get("RADIOGRAFIA") or {}).get("candidatos")
                               or {}).get((d.get("RADIOGRAFIA") or {}).get("elegido")),
                        "sher": (((d.get("RADIOGRAFIA") or {}).get("ahora") or {})
                                 .get("filas") or {}).get("S-HERIDO")}
        filas.append({"eid": eid, "p10": r["placements"][10],
                      "p11": r["placements"][11], "A": A, "B": Bg, "pt": pt})
    return filas


def metricas(filas, nombre):
    n = len(filas)
    M = {"nombre": nombre, "n": n}
    # V1 honor
    M["inici"] = sum(f[g]["iniciaciones"] for f in filas for g in ("A", "B"))
    M["ataques"] = sum(f[g]["ataques"] for f in filas for g in ("A", "B"))
    M["golpes_h"] = sum(f[g]["golpes_de_hermana"] for f in filas for g in ("A", "B"))
    M["vinculo"] = sum(f[g]["vinculo_tics"] for f in filas for g in ("A", "B"))
    # V4/V5 moneda
    mejor = [min(f["p10"], f["p11"]) for f in filas]
    M["top4"] = sum(1 for m in mejor if m <= 4)
    M["wins"] = sum(1 for m in mejor if m == 1)
    M["podio"] = sum(1 for f in filas if {f["p10"], f["p11"]} <= {1, 2})
    M["mejor_med"] = st.median(mejor)
    M["ambas8"] = sum(1 for f in filas if f["p10"] <= 8 and f["p11"] <= 8)
    # V3 distancia VERDADERA (ambas vivas)
    dists, dist_banda, banda_cerca = [], [], 0
    camino_tics = camino_eps = 0
    eps_camino_don = 0
    for f in filas:
        tuvo_camino = don_tras = False
        for t, par in sorted(f["pt"].items()):
            if "A" not in par or "B" not in par:
                continue
            pa, pb = par["A"], par["B"]
            if not pa["pos"] or not pb["pos"] or pa["hp"] <= 0 or pb["hp"] <= 0:
                continue
            dv = math.dist(pa["pos"], pb["pos"])
            dists.append(dv)
            una_banda = pa["hp"] < BANDA or pb["hp"] < BANDA
            if una_banda:
                dist_banda.append(dv)
                if dv <= 2.0:
                    banda_cerca += 1
                # el camino: la sana (portadora potencial) elige algo que ACERCA
                herida, sana = (pa, pb) if pa["hp"] < BANDA else (pb, pa)
                pp = sana.get("pp")
                if (dv > 2.0 and isinstance(pp, dict)
                        and pp.get("pos_prevista")
                        and (sana["el"] or "") != "noop"):
                    d2 = math.dist(tuple(pp["pos_prevista"]), herida["pos"])
                    if d2 < dv - 0.5:
                        camino_tics += 1
                        tuvo_camino = True
        if tuvo_camino:
            camino_eps += 1
            eb = min([f[g]["banda_entra"] for g in ("A", "B")
                      if f[g]["banda_entra"] is not None] or [None])
            if eb is not None and any(d["tick"] >= eb for g in ("A", "B")
                                      for d in f[g]["dones"]):
                eps_camino_don += 1
        f["_don_tras"] = None
    M["dist_med"] = st.median(dists) if dists else None
    M["dist_banda_med"] = st.median(dist_banda) if dist_banda else None
    M["banda_tics"] = len(dist_banda)
    M["banda_cerca_pct"] = 100 * banda_cerca / max(len(dist_banda), 1)
    M["camino_tics"] = camino_tics
    M["camino_eps"] = camino_eps
    M["camino_don_eps"] = eps_camino_don
    # V2 dones (metodo del 55)
    p2_den = p2_num = 0
    for f in filas:
        cond = don_en = False
        for me, otra in (("A", "B"), ("B", "A")):
            eb = f[me]["banda_entra"]
            if eb is None:
                continue
            mo = f[otra]["muerte"] or 0
            if mo <= eb:
                continue
            if any(b > 0 for t, b in f[otra]["pack_bot_por_tick"].items() if t >= eb):
                cond = True
                if any(d["tick"] >= eb for d in f[otra]["dones"]):
                    don_en = True
        if cond:
            p2_den += 1
            if don_en:
                p2_num += 1
    M["p2_den"], M["p2_num"] = p2_den, p2_num
    M["dones"] = sum(len(f[g]["dones"]) for f in filas for g in ("A", "B"))
    M["sher_tics"] = sum(f[g]["herido_tics"] for f in filas for g in ("A", "B"))
    # V6 estabilidad
    M["cool"] = st.median([f[g]["final"]["tics_cooldown"] for f in filas
                           for g in ("A", "B") if f[g]["final"]])
    M["cong"] = st.median([f[g]["final"]["tics_congelado"] for f in filas
                           for g in ("A", "B") if f[g]["final"]])
    M["banda_diario"] = st.median([f[g]["banda_tics"] for f in filas
                                   for g in ("A", "B")])
    return M


def entregas(filas):
    out = []
    for f in filas:
        for g, otra in (("A", "B"), ("B", "A")):
            for d in f[g]["dones"]:
                t0 = d["tick"]
                gan = [t for t, b in sorted(f[otra]["pack_bot_por_tick"].items())
                       if t > t0 and b > f[otra]["pack_bot_por_tick"].get(t0, 0)]
                hp0 = f[otra]["hp_por_tick"].get(t0)
                sube = next((t for t, h in sorted(f[otra]["hp_por_tick"].items())
                             if t0 < t <= t0 + 400 and hp0 is not None
                             and h >= hp0 + 30), None)
                out.append({"eid": f["eid"], "quien": "10" if g == "A" else "11",
                            "t": t0, "recoge": gan[0] if gan else None,
                            "cura": sube})
    return out


def main():
    v30 = carga("pareja2")
    v29 = carga("pareja")
    M0, M9 = metricas(v30, "v30"), metricas(v29, "v29 (55)")
    print("=" * 92)
    print(f"LA PAREJA, SEGUNDA TANDA — v30 ({M0['n']} eps) contra v29 del 55 "
          f"({M9['n']} eps), metodo identico")
    print("=" * 92)
    for M in (M0, M9):
        n = M["n"]
        print(f"\n  [{M['nombre']}]")
        print(f"  V1 honor: ataques {M['ataques']} · INICIACIONES {M['inici']} · "
              f"golpes entre hermanas {M['golpes_h']} · S-VINCULO {M['vinculo']} tics")
        print(f"  V2 dones: {M['dones']} soltares · condicion {M['p2_den']} eps · "
              f"con don tras entrada {M['p2_num']} "
              f"({100*M['p2_num']/max(M['p2_den'],1):.0f}%)")
        print(f"  V3 distancia (verdadera): mediana {M['dist_med']:.1f} · "
              f"en banda {M['dist_banda_med']:.1f} · "
              f"a <=2 con una en banda {M['banda_cerca_pct']:.0f}% "
              f"({M['banda_tics']} tics)")
        print(f"  V4 moneda: top-4 mejor {M['top4']}/{n} ({100*M['top4']/n:.0f}%) · "
              f"wins {M['wins']} · podio doble {M['podio']} · mejor med {M['mejor_med']}")
        print(f"  V5 juntas a 8: {M['ambas8']}/{n} ({100*M['ambas8']/n:.0f}%)")
        print(f"  V6: S-HERIDO {M['sher_tics']} tics · camino (acerca en banda>2): "
              f"{M['camino_tics']} tics en {M['camino_eps']} eps "
              f"(don despues: {M['camino_don_eps']}) · cooldown {M['cool']:.0f} · "
              f"congelado {M['cong']:.0f} · banda/diario {M['banda_diario']:.0f}")
    print("\n  ENTREGAS v30 (don -> recoge -> cura):")
    for e in entregas(v30):
        print(f"    {e['eid'][:18]} gemela{e['quien']} t{e['t']}: "
              f"recoge {('t'+str(e['recoge'])) if e['recoge'] else 'NO'} · "
              f"cura {('t'+str(e['cura'])) if e['cura'] else 'no visto'}")
    json.dump({"v30": {k: v for k, v in M0.items()},
               "v29": {k: v for k, v in M9.items()}},
              open(f"{P}/runs/pareja2/resumen.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

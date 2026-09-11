"""ANATOMIA DEL DON QUE NO LLEGA — PROMPT_55 C (obligada: P2 fallo).

En los episodios donde una hermana entra en banda (<30) con la otra viva y
con botiquin, ¿por que no hay don? Sospechosas, del veredicto sellado:
¿canal cortado? ¿distancia? ¿sin botiquin? — y las de la casa: ¿la ve
siquiera? ¿existe el candidato soltar? ¿que margen le falta?

Metodo: en cada tic donde la herida esta en banda y la portadora viva-con-
botiquin decide, se mira EN EL DIARIO DE LA PORTADORA: dist_pareja,
pareja_vista, pareja_banda, parte fresco, candidatos (soltar presente y su
margen contra el elegido), S-HERIDO del ahora.

Uso (desde la raiz del repo):  python3 paintball/anatomia_don.py
"""
from __future__ import annotations

import json
import os
import statistics as st

from pareja import lee, diario, B


def main():
    D = json.load(open(f"{B}/episodios.json"))
    eps = [e["id"] for e in D["eps"]]

    momentos = []          # un registro por tic-de-decision de la portadora
    eps_cond = set()
    eps_don = set()
    for eid in eps:
        d10, d11 = diario(eid, 10), diario(eid, 11)
        if not d10 or not d11:
            continue
        for herida, portadora, ps in ((d10, d11, 11), (d11, d10, 10)):
            hp_h = {d["tick"]: float(d.get("hp") or 0)
                    for d in herida if d.get("k") == "tick"}
            muerte_h = max(hp_h) if hp_h else 0
            en_banda = {t for t, h in hp_h.items() if h < 30 and h > 0}
            if not en_banda:
                continue
            t0 = min(en_banda)
            for d in portadora:
                if d.get("k") != "tick" or d.get("phase") != "live":
                    continue
                t = d.get("tick", 0)
                if t < t0 or t > muerte_h:
                    continue
                bot = sum(int(x.get("n") or 1) for x in (d.get("pack") or [])
                          if x and x.get("id") == "first_aid")
                if bot == 0:
                    continue
                if hp_h.get(t, hp_h.get(t - 1, 99)) >= 30:
                    continue                      # la herida ya salio de banda
                soc = d.get("social") or {}
                rad = d.get("RADIOGRAFIA") or {}
                cand = rad.get("candidatos") or {}
                cs = {k: (v["d"] if isinstance(v, dict) else v)
                      for k, v in cand.items()}
                el = rad.get("elegido")
                sol = next((k for k in cs if k.startswith("soltar")), None)
                ahora = rad.get("ahora") or {}
                fil = ahora.get("filas") or {}
                momentos.append({
                    "eid": eid, "portadora": ps, "tick": t,
                    "dist": soc.get("dist_pareja"),
                    "vista": bool(soc.get("pareja_vista")),
                    "banda_vista": soc.get("pareja_banda"),
                    "parte": ahora.get("parte") is not None,
                    "cand_soltar": sol is not None,
                    "margen_soltar": (round(cs[sol] - cs[el], 4)
                                      if sol and el in cs else None),
                    "elegido": el,
                    "sherido": (fil.get("S-HERIDO") or {}).get("M", 0) or 0})
                eps_cond.add(eid)
                if (el or "").startswith("soltar"):
                    eps_don.add(eid)

    n = len(momentos)
    print("=" * 88)
    print(f"ANATOMIA DEL DON — {n} tics-de-decision con la hermana EN BANDA y "
          f"la portadora viva con botiquin ({len(eps_cond)} episodios)")
    print("=" * 88)
    if not n:
        return

    def pct(f):
        return 100 * sum(1 for m in momentos if f(m)) / n

    dists = [m["dist"] for m in momentos if m["dist"] is not None]
    print(f"\n  ¿canal?     parte fresco en radiografia: {pct(lambda m: m['parte']):.0f}% de los tics")
    print(f"  ¿la ve?     pareja a la vista: {pct(lambda m: m['vista']):.0f}%  · "
          f"banda vista != healthy: {pct(lambda m: m['banda_vista'] not in ('healthy', '', None)):.0f}%")
    print(f"  ¿distancia? mediana {st.median(dists):.1f} · p25 {sorted(dists)[len(dists)//4]:.1f} · "
          f"a <=2 (alcance del alivio): {pct(lambda m: m['dist'] is not None and m['dist'] <= 2):.0f}% de los tics")
    print(f"  ¿candidato? soltar EXISTE: {pct(lambda m: m['cand_soltar']):.0f}% de los tics")
    print(f"  ¿S-HERIDO?  encendida: {pct(lambda m: m['sherido'] > 0):.0f}% · "
          f"M mediana {st.median([m['sherido'] for m in momentos]):.2f}")

    margs = [m["margen_soltar"] for m in momentos if m["margen_soltar"] is not None]
    if margs:
        print(f"\n  margen del soltar (d_soltar - d_elegido; + = pierde):")
        print(f"    mediana {st.median(margs):+.3f} · min {min(margs):+.3f} · "
              f"gana (<=0) en {100*sum(1 for x in margs if x <= 0)/len(margs):.0f}% de los tics")

    # cruce distancia x candidato x margen
    cerca = [m for m in momentos if m["dist"] is not None and m["dist"] <= 2]
    lejos = [m for m in momentos if m["dist"] is not None and m["dist"] > 2]
    for nom, grupo in (("a <=2", cerca), ("a >2", lejos)):
        if not grupo:
            print(f"  {nom}: 0 tics")
            continue
        mg = [m["margen_soltar"] for m in grupo if m["margen_soltar"] is not None]
        print(f"  {nom}: {len(grupo)} tics · candidato {100*sum(1 for m in grupo if m['cand_soltar'])/len(grupo):.0f}% · "
              f"margen mediano {st.median(mg):+.3f}" if mg else f"  {nom}: {len(grupo)} tics · sin margen")

    # elegidos tipicos en esos momentos
    import collections
    cc = collections.Counter(m["elegido"] for m in momentos)
    print(f"\n  que elige la portadora en esos tics: {cc.most_common(6)}")
    print(f"\n  episodios con condicion: {len(eps_cond)} · con don en esos tics: {len(eps_don)}")


if __name__ == "__main__":
    main()

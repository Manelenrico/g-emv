"""AUTOPSIA DE LA DEFENSA QUE NO LLEGA — PROMPT_64 C (P2 fallo: 5/20 = 25 %).

Las tres sospechosas del veredicto sellado: (a) la ocasion no ocurre — NO, 20
ventanas; (b) la huida gana siempre; (c) la certificacion no cierra. Y las de
la casa: ¿existe el candidato (alcance/alineacion del arma)? ¿el cazador esta
donde el parte dice? ¿que elige cuando no defiende?

Uso (desde la raiz del repo):  python3 paintball/autopsia_manada.py
"""
from __future__ import annotations

import collections
import json
import math
import os

from manada_campo import carga, ocasiones, P

ARMAS_R = {"sword": 1, "spear": 2, "bow": 8, "knives": 5}


def main():
    filas = carga("manada")
    ocs = ocasiones(filas)
    print("=" * 90)
    print(f"AUTOPSIA — {len(ocs)} ventanas de ocasion; defiende en "
          f"{sum(1 for o in ocs if o['defiende'])}")
    print("=" * 90)

    elegidos = collections.Counter()
    cand_posible = 0
    tics = 0
    sin_cand = collections.Counter()
    detalle = []
    for o in ocs:
        f = next(x for x in filas if x["eid"] == o["eid"])
        yo_l = "s10" if o["quien"] == "10" else "s11"
        ella_l = "s11" if o["quien"] == "10" else "s10"
        vent = [t for t in sorted(k for k in f[yo_l] if k != "FINAL")
                if o["t0"] <= t <= o["t1"]]
        n_pos = 0
        for t in vent:
            x = f[yo_l][t]
            if not isinstance(x, dict):
                continue
            tics += 1
            elegidos[x.get("el")] += 1
            p = x.get("parte") or {}
            ap = p.get("agresor_pos")
            rango = ARMAS_R.get(x.get("hand"), 0)
            if ap and x["pos"]:
                dx, dy = ap[0] - x["pos"][0], ap[1] - x["pos"][1]
                alineado = (dx == 0 or dy == 0 or abs(dx) == abs(dy))
                dist = max(abs(dx), abs(dy))
                if alineado and dist <= rango:
                    cand_posible += 1
                    n_pos += 1
                else:
                    sin_cand["no alineado" if not alineado else
                             f"fuera de alcance (d={dist}>{rango})"] += 1
        detalle.append({"eid": o["eid"], "quien": o["quien"], "tics": len(vent),
                        "con_geometria": n_pos, "defiende": o["defiende"]})

    print(f"\n  tics de ocasion: {tics}")
    print(f"  ¿la GEOMETRIA permite el golpe? (alineado y en rango del arma):"
          f" {cand_posible} tics ({100*cand_posible/max(tics,1):.0f}%)")
    print(f"  cuando NO: {dict(sin_cand.most_common(4))}")
    print(f"\n  que elige en la ocasion: {elegidos.most_common(8)}")

    print("\n  por ventana (tics · tics con geometria · ¿defendio?):")
    for d in detalle:
        print(f"    {d['eid'][:18]} gemela{d['quien']}: {d['tics']:>4} tics ·"
              f" {d['con_geometria']:>3} con geometria · "
              f"{'DEFIENDE' if d['defiende'] else 'no'}")

    # ¿cuantas ventanas tuvieron ALGUNA vez geometria?
    con_geo = [d for d in detalle if d["con_geometria"] > 0]
    defendio_con_geo = [d for d in con_geo if d["defiende"]]
    print(f"\n  ventanas con geometria posible alguna vez: {len(con_geo)}/{len(detalle)}")
    print(f"  de esas, defendio: {len(defendio_con_geo)}/{len(con_geo)} "
          f"({100*len(defendio_con_geo)/max(len(con_geo),1):.0f}%)  <-- P2 REAL")
    json.dump({"tics": tics, "con_geometria": cand_posible,
               "sin_cand": dict(sin_cand), "detalle": detalle},
              open(f"{P}/runs/manada/autopsia.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

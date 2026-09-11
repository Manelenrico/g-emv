"""EL RESELLO Y LA VARA DE PROTECCION — PROMPT_65 A+B (coste 0, diarios del 64).

A) P2' con la OCASION corregida (precedente del 38): hermana bajo caza
   certificada + la otra a <=2, sana (>=70), con arma, Y el agresor ALINEADO
   y EN ALCANCE del arma. Se recalcula con su n.
B) La vara de proteccion (P3 quedo ciega: la supervivencia satura al 100 %).
   Pareado por ventana, con defensa vs sin: (1) dano recibido por la cazada en
   los 120 tics siguientes; (2) ¿el cazador la abandona?; (3) hp de la cazada
   al cerrarse la ventana. La mesa NO sella direccion: tabla y frase honesta.

Uso (desde la raiz del repo):  python3 paintball/proteccion.py
"""
from __future__ import annotations

import json
import math
import os
import statistics as st

from manada_campo import carga, P

ARMAS_R = {"sword": 1, "spear": 2, "bow": 8, "knives": 5}
VENT = 120


def ocasiones_p2p(filas):
    """OCASION CORREGIDA (P2'): + agresor alineado y en alcance del arma."""
    out = []
    for f in filas:
        for yo_l, ella_l, quien in (("s10", "s11", "10"), ("s11", "s10", "11")):
            cur = None
            for t in sorted(k for k in f[yo_l] if k != "FINAL"):
                x, y = f[yo_l].get(t), f[ella_l].get(t)
                if not isinstance(x, dict) or not isinstance(y, dict):
                    continue
                if not x.get("live") or x["hp"] <= 0 or y["hp"] <= 0:
                    continue
                p = x.get("parte") or {}
                ap = p.get("agresor_pos")
                ok = False
                if (p.get("agresor") and ap and x["pos"] and y["pos"]
                        and math.dist(x["pos"], y["pos"]) <= 2.0
                        and x["hp"] >= 70):
                    r = ARMAS_R.get(x.get("hand"), 0)
                    dx, dy = ap[0] - x["pos"][0], ap[1] - x["pos"][1]
                    alineado = (dx == 0 or dy == 0 or abs(dx) == abs(dy))
                    ok = bool(r) and alineado and max(abs(dx), abs(dy)) <= r
                if ok:
                    if cur is None:
                        cur = {"eid": f["eid"], "quien": quien, "t0": t,
                               "t1": t, "defiende": False, "tdef": None}
                    cur["t1"] = t
                    if (x.get("el") or "").startswith("atacar") and \
                            (x.get("honor") or {}).get("defensa_pareja"):
                        cur["defiende"] = True
                        cur["tdef"] = cur["tdef"] or t
                elif cur is not None:
                    out.append(cur); cur = None
            if cur is not None:
                out.append(cur)
    return out


def proteccion(filas, ocs):
    """B: por ventana — dano a la cazada en 120 tics, abandono, hp al cierre."""
    filas_out = []
    for o in ocs:
        f = next(x for x in filas if x["eid"] == o["eid"])
        yo_l = "s10" if o["quien"] == "10" else "s11"
        ella_l = "s11" if o["quien"] == "10" else "s10"
        yo_slot = 10 if o["quien"] == "10" else 11
        ella_slot = 11 if o["quien"] == "10" else 10
        # el cazador certificado: de MI parte en el primer tic de la ventana
        p0 = (f[yo_l].get(o["t0"]) or {}).get("parte") or {}
        # su slot no viaja en el parte: se identifica por la posicion; en su
        # diario, el que le pega es `source` P<slot>
        ticks = [t for t in sorted(k for k in f[ella_l] if k != "FINAL")
                 if o["t1"] < t <= o["t1"] + VENT]
        golpes = 0
        fuentes = set()
        for t in ticks:
            y = f[ella_l].get(t)
            if isinstance(y, dict):
                for s in (y.get("dmg") or []):
                    if s != f"P{yo_slot}":       # el fuego amigo se cuenta aparte
                        golpes += 1
                        fuentes.add(s)
        hp_cierre = (f[ella_l].get(o["t1"]) or {}).get("hp")
        hp_fin = (f[ella_l].get(ticks[-1]) or {}).get("hp") if ticks else hp_cierre
        # ¿abandona? su parte deja de declarar agresor en los 120 tics
        sigue = 0
        for t in ticks:
            y = f[ella_l].get(t)
            # el parte de ELLA lo lee su hermana; aqui usamos SU propio diario:
            # ¿sigue recibiendo dano? ya contado. El abandono se aproxima por
            # "deja de recibir golpes en la segunda mitad de la ventana".
            if isinstance(y, dict) and (y.get("dmg") or []):
                sigue = max(sigue, t)
        abandona = (sigue == 0) or (sigue - o["t1"] < VENT / 2)
        filas_out.append({"eid": o["eid"], "quien": o["quien"],
                          "defiende": o["defiende"], "golpes120": golpes,
                          "fuentes": sorted(fuentes),
                          "hp_cierre": hp_cierre, "hp_fin": hp_fin,
                          "abandona": abandona, "n_ticks": len(ticks)})
    return filas_out


def main():
    filas = carga("manada")
    # ── A · P2' ──────────────────────────────────────────────────────────
    ocs = ocasiones_p2p(filas)
    n = len(ocs)
    d = sum(1 for o in ocs if o["defiende"])
    print("=" * 88)
    print("A · EL RESELLO P2' (ocasion CON alcance) — precedente del 38")
    print("=" * 88)
    print(f"\n  ocasiones P2' (hermana cazada + yo a <=2, sana, con arma, Y el"
          f" agresor ALINEADO y EN ALCANCE): {n}")
    print(f"  la defensa llega: {d}/{n} = {100*d/max(n,1):.0f} %"
          f"   (P2 original: 5/20 = 25 %)")
    print(f"  episodios con ocasion P2': {len(set(o['eid'] for o in ocs))}")

    # ── B · la vara de proteccion ────────────────────────────────────────
    todas = __import__("manada_campo").ocasiones(filas)      # las 20 del 64
    prot = proteccion(filas, todas)
    con = [x for x in prot if x["defiende"]]
    sin = [x for x in prot if not x["defiende"]]
    print("\n" + "=" * 88)
    print("B · LA VARA DE PROTECCION (primera vez que se mide; sin sello)")
    print("=" * 88)
    print(f"\n  {'vara (120 tics tras la ventana)':<44} {'CON defensa':>12} {'SIN defensa':>12}")
    def med(g, k):
        v = [x[k] for x in g if x.get(k) is not None]
        return st.median(v) if v else float("nan")
    print(f"  {'ventanas':<44} {len(con):>12} {len(sin):>12}")
    print(f"  {'golpes recibidos por la cazada (mediana)':<44} "
          f"{med(con,'golpes120'):>12.1f} {med(sin,'golpes120'):>12.1f}")
    print(f"  {'golpes recibidos (media)':<44} "
          f"{(st.mean([x['golpes120'] for x in con]) if con else float('nan')):>12.1f} "
          f"{(st.mean([x['golpes120'] for x in sin]) if sin else float('nan')):>12.1f}")
    print(f"  {'hp de la cazada al cerrar la ventana':<44} "
          f"{med(con,'hp_cierre'):>12.1f} {med(sin,'hp_cierre'):>12.1f}")
    print(f"  {'hp 120 tics despues':<44} "
          f"{med(con,'hp_fin'):>12.1f} {med(sin,'hp_fin'):>12.1f}")
    print(f"  {'% ventanas en que el acoso CESA':<44} "
          f"{100*sum(1 for x in con if x['abandona'])/max(len(con),1):>11.0f}% "
          f"{100*sum(1 for x in sin if x['abandona'])/max(len(sin),1):>11.0f}%")
    print("\n  detalle:")
    for x in prot:
        print(f"    {x['eid'][:18]} g{x['quien']} "
              f"{'DEFIENDE' if x['defiende'] else 'no      '} · "
              f"golpes120 {x['golpes120']:>3} · hp {x['hp_cierre']}->{x['hp_fin']} · "
              f"acoso cesa {x['abandona']}")
    json.dump({"p2p": {"n": n, "defiende": d, "ocs": ocs}, "proteccion": prot},
              open(f"{P}/runs/manada/proteccion.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

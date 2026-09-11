"""ANATOMIA DEL DON, SEGUNDA TANDA — PROMPT_57 C (P2 fallo otra vez: 18 %).

La novedad del campo v30: cuando una esta en banda, la otra YA ESTA AL LADO
(dist mediana 2,2 vs 7,0 en v29). Entonces, ¿por que no suelta? Sospechosas
nuevas: (a) la herida lleva SU botiquin y se cura sola (el don sobra);
(b) el alivio ya esta servido por una cura del suelo servible; (c) la
servibilidad bloquea el don porque el cazador de ella esta encima (disenado
asi); (d) la ventana es corta (sale de banda antes de que gane el soltar).

Uso (desde la raiz del repo):  python3 paintball/anatomia2.py
"""
from __future__ import annotations

import json
import math
import os
import statistics as st

from pareja2 import carga, BANDA

P = os.path.dirname(os.path.abspath(__file__))


def main():
    filas = carga("pareja2")
    momentos = []
    episodios = {}
    for f in filas:
        # por tic: herida <30 viva, portadora viva CON botiquin
        for me, otra, so, ss in (("A", "B", 10, 11), ("B", "A", 11, 10)):
            hpo = f[otra]["hp_por_tick"]
            boto = f[otra]["pack_bot_por_tick"]
            bot_me = f[me]["pack_bot_por_tick"]
            for t, hp in sorted(f[me]["hp_por_tick"].items()):
                if not (0 < hp < BANDA):
                    continue
                if hpo.get(t, 0) <= 0 or boto.get(t, 0) == 0:
                    continue
                pt = f["pt"].get(t) or {}
                pa, pb = pt.get(me), pt.get(otra)
                if not pa or not pb or not pa["pos"] or not pb["pos"]:
                    continue
                dv = math.dist(pa["pos"], pb["pos"])
                rad_sher = pb.get("sher") or {}
                momentos.append({
                    "eid": f["eid"], "t": t, "dist": dv,
                    "herida_bot": bot_me.get(t, 0) > 0,
                    "sher_M": rad_sher.get("M", 0) or 0,
                    "el": pb.get("el")})
                ep = episodios.setdefault(f["eid"], {
                    "tics": 0, "cerca": 0, "herida_bot": 0, "don": False,
                    "salida": None, "quien": me})
                ep["tics"] += 1
                ep["cerca"] += 1 if dv <= 2 else 0
                ep["herida_bot"] += 1 if bot_me.get(t, 0) > 0 else 0
            # ¿don de la portadora tras la entrada de esta herida?
            eb = f[me]["banda_entra"]
            if eb is not None and any(d["tick"] >= eb for d in f[otra]["dones"]):
                if f["eid"] in episodios:
                    episodios[f["eid"]]["don"] = True
        # salida de la banda: ¿se curo sola, la curo el don, murio en banda?
        for me in ("A", "B"):
            eb = f[me]["banda_entra"]
            if eb is None:
                continue
            hps = sorted(f[me]["hp_por_tick"].items())
            fin = None
            for t, hp in hps:
                if t <= eb:
                    continue
                if hp <= 0:
                    fin = "muere"
                    break
                if hp >= BANDA + 20:
                    fin = "se recupera"
                    break
            if f["eid"] in episodios and episodios[f["eid"]]["salida"] is None:
                episodios[f["eid"]]["salida"] = fin or "sigue en banda"

    n = len(momentos)
    print("=" * 90)
    print(f"ANATOMIA 2 — {n} tics con herida en banda + portadora viva con "
          f"botiquin ({len(episodios)} episodios)")
    print("=" * 90)
    if not n:
        return

    def pct(f):
        return 100 * sum(1 for m in momentos if f(m)) / n

    dists = [m["dist"] for m in momentos]
    print(f"\n  distancia: mediana {st.median(dists):.1f} · a <=2: "
          f"{pct(lambda m: m['dist'] <= 2):.0f}% (55: 2 %)")
    print(f"  la herida lleva SU botiquin: {pct(lambda m: m['herida_bot']):.0f}% de los tics")
    print(f"  S-HERIDO de la portadora: encendida {pct(lambda m: m['sher_M'] > 0):.0f}% · "
          f"M mediana {st.median([m['sher_M'] for m in momentos]):.2f} · "
          f"ALIVIADA (M < 0.4) {pct(lambda m: 0 < m['sher_M'] < 0.4):.0f}%")
    import collections
    cc = collections.Counter(m["el"] for m in momentos)
    print(f"  que elige la portadora: {cc.most_common(6)}")
    print(f"\n  por episodio ({len(episodios)}):")
    sal = collections.Counter(e["salida"] for e in episodios.values())
    don = sum(1 for e in episodios.values() if e["don"])
    hb = sum(1 for e in episodios.values()
             if e["herida_bot"] > 0.5 * e["tics"])
    print(f"    con don tras entrada: {don} · la herida llevaba botiquin propio "
          f"(mayoria de tics): {hb} · salidas: {dict(sal)}")
    for eid, e in sorted(episodios.items()):
        print(f"    {eid[:18]} tics {e['tics']:>4} · cerca {e['cerca']:>4} · "
              f"herida_bot {e['herida_bot']:>4} · don {'SI' if e['don'] else 'no'} · "
              f"{e['salida']}")


if __name__ == "__main__":
    main()

"""LA PROTECCION EMPAREJADA — PROMPT_67 (forense, coste 0, diarios del 64+66).

La pregunta que dos tandas no han podido responder: ¿defender SALVA a la
cazada? No se pudo sellar porque las ventanas defendidas y las no defendidas
ocurren en momentos distintos de la herida (64: hermana sana; 66: ya herida),
asi que la comparacion medía el ESTADO DE PARTIDA, no el efecto.

Aqui se empareja por estado: cada ventana DEFENDIDA con la NO DEFENDIDA mas
parecida en (hp de la cazada, hp de la otra, distancia del cazador, arma del
cazador, tic de partida), sin reemplazo, y se comparan los resultados.

Uso (desde la raiz del repo):  python3 paintball/proteccion_pareada.py
"""
from __future__ import annotations

import glob
import json
import math
import os
import statistics as st

from pareja import lee

P = os.path.dirname(os.path.abspath(__file__))
VENT = 120                 # tics de seguimiento tras la ventana
LEJOS = 3                  # "se aleja" del cazador


def diario(base, eid, s):
    fs = glob.glob(f"{base}/{eid}/a{s}/*.log")
    return list(lee(sorted(fs)[0])) if fs else None


def serie(recs):
    out = {}
    for d in recs:
        if d.get("k") != "tick":
            continue
        rad = d.get("RADIOGRAFIA") or {}
        ah = rad.get("ahora") or {}
        out[d.get("tick", 0)] = {
            "pos": tuple(d.get("pos") or ()), "hp": float(d.get("hp") or 0),
            "live": d.get("phase") == "live",
            "hand": (d.get("hand") or {}).get("id")
                    if isinstance(d.get("hand"), dict) else None,
            "el": rad.get("elegido"), "honor": rad.get("honor"),
            "parte": ah.get("parte"),
            "dmg": [g.get("source") for g in (d.get("damage_taken") or [])],
            "ve": {a.get("slot"): a for a in (d.get("ve_agentes") or [])}}
    return out


def ventanas(tanda):
    """Ventanas de CAZA CERTIFICADA con la hermana a <=2 (sin exigir mi hp ni
    arma: se quiere el universo mas ancho para poder emparejar)."""
    base = f"{P}/runs/{tanda}"
    D = json.load(open(f"{base}/episodios.json"))
    out = []
    for e in D["eps"]:
        eid = e["id"]
        d10, d11 = diario(base, eid, 10), diario(base, eid, 11)
        if not d10 or not d11:
            continue
        S = {"10": serie(d10), "11": serie(d11)}
        for yo, ella in (("10", "11"), ("11", "10")):
            cur = None
            for t in sorted(S[yo]):
                x, y = S[yo].get(t), S[ella].get(t)
                if not isinstance(x, dict) or not isinstance(y, dict):
                    continue
                if not x.get("live") or x["hp"] <= 0 or y["hp"] <= 0:
                    continue
                p = x.get("parte") or {}
                ap = p.get("agresor_pos")
                cond = (p.get("agresor") and ap and x["pos"] and y["pos"]
                        and math.dist(x["pos"], y["pos"]) <= 2.0)
                if cond:
                    if cur is None:
                        # el cazador: agente visible en (ax,ay), tol 1
                        caz_slot, caz_arma = None, None
                        for sl, a in (x.get("ve") or {}).items():
                            q = a.get("pos") or ()
                            if q and max(abs(q[0] - ap[0]), abs(q[1] - ap[1])) <= 1:
                                caz_slot, caz_arma = sl, a.get("hand")
                                break
                        cur = {"tanda": tanda, "eid": eid, "yo": yo, "ella": ella,
                               "t0": t, "t1": t,
                               "hp_cazada0": y["hp"], "hp_otra0": x["hp"],
                               "dist_caz": round(math.dist(x["pos"], ap), 2),
                               "caz_slot": caz_slot, "caz_arma": caz_arma,
                               "mi_arma": x.get("hand"),
                               "defiende": False, "tdef": None, "S": S}
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


def resultados(v):
    """Lo que pasa DESPUES: dano a la cazada, abandono, hp de cierre, muerte."""
    S = v["S"]
    ella, yo = S[v["ella"]], S[v["yo"]]
    t_ref = v["tdef"] or v["t1"]
    post = [t for t in sorted(ella) if t_ref < t <= t_ref + VENT]
    golpes = 0
    ultimo_golpe = None
    for t in post:
        y = ella[t]
        for s in (y.get("dmg") or []):
            if s != f"P{v['yo']}":            # el fuego amigo no cuenta aqui
                golpes += 1
                ultimo_golpe = t
    hp_cierre = ella.get(v["t1"], {}).get("hp")
    hp_post = ella.get(post[-1], {}).get("hp") if post else hp_cierre
    muere = any((ella.get(t) or {}).get("hp", 1) <= 0 for t in post)
    # ¿el cazador abandona? deja de danarla Y se aleja >3 de ella
    aleja = None
    for t in post:
        y = ella[t]
        a = (y.get("ve") or {}).get(v["caz_slot"])
        if a and a.get("pos") and y["pos"]:
            if math.dist(y["pos"], a["pos"]) > LEJOS:
                aleja = t
                break
    abandona = (ultimo_golpe is None) or (aleja is not None)
    # el precio de la otra (yo): hp al cerrar + VENT
    hp_yo0 = v["hp_otra0"]
    postyo = [t for t in sorted(yo) if t_ref < t <= t_ref + VENT]
    hp_yo1 = yo.get(postyo[-1], {}).get("hp") if postyo else hp_yo0
    return {"golpes": golpes, "hp_cierre": hp_cierre, "hp_post": hp_post,
            "muere": muere, "abandona": abandona,
            "delta_cazada": (hp_post - v["hp_cazada0"]) if hp_post is not None else None,
            "delta_yo": (hp_yo1 - hp_yo0) if hp_yo1 is not None else None,
            "n_post": len(post)}


def distancia_estado(a, b):
    """Criterio de emparejado DECLARADO: distancia normalizada en cuatro ejes
    (hp de la cazada /100, hp de la otra /100, distancia del cazador /5, tic
    de partida /2000) mas un veto duro si el ARMA del cazador difiere en
    familia (melee <-> a distancia)."""
    fam = lambda w: ("melee" if w in ("sword", "spear") else
                     ("dist" if w in ("bow", "knives", "blowgun") else "otro"))
    if fam(a["caz_arma"]) != fam(b["caz_arma"]):
        return None
    return (abs(a["hp_cazada0"] - b["hp_cazada0"]) / 100.0
            + abs(a["hp_otra0"] - b["hp_otra0"]) / 100.0
            + abs(a["dist_caz"] - b["dist_caz"]) / 5.0
            + abs(a["t0"] - b["t0"]) / 2000.0)


def signos(k, n):
    if n == 0:
        return 1.0
    lo = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    hi = sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * min(lo, hi))


def main():
    vs = ventanas("manada") + ventanas("manada2")
    dfd = [v for v in vs if v["defiende"]]
    nod = [v for v in vs if not v["defiende"]]
    print("=" * 90)
    print(f"A · EL EMPAREJADO POR ESTADO — {len(vs)} ventanas "
          f"({len(dfd)} defendidas, {len(nod)} no) de las tandas 64+66")
    print("=" * 90)
    print("\n  criterio (declarado): distancia normalizada en hp de la cazada,")
    print("  hp de la otra, distancia del cazador y tic de partida; VETO si el")
    print("  arma del cazador cambia de familia (melee <-> a distancia).")
    print("  Emparejado SIN reemplazo, el mas cercano primero.\n")

    # emparejado voraz por cercania global
    cands = []
    for i, a in enumerate(dfd):
        for j, b in enumerate(nod):
            d = distancia_estado(a, b)
            if d is not None:
                cands.append((d, i, j))
    cands.sort()
    usados_a, usados_b, pares = set(), set(), []
    for d, i, j in cands:
        if i in usados_a or j in usados_b:
            continue
        usados_a.add(i); usados_b.add(j)
        pares.append((d, dfd[i], nod[j]))
    print(f"  pares limpios: {len(pares)}")
    if len(pares) < 6:
        print("\n  MENOS DE 6 PARES: no se concluye (regla del encargo).")
    print(f"\n  {'par':<3} {'d':>5} {'hp caz (D/N)':>14} {'dist':>9} "
          f"{'golpes120 D':>12} {'N':>4} {'delta cazada D':>15} {'N':>7}")
    gd, gn = [], []
    dcd, dcn = [], []
    yod, yon = [], []
    for k, (d, A, B) in enumerate(pares, 1):
        ra, rb = resultados(A), resultados(B)
        gd.append(ra["golpes"]); gn.append(rb["golpes"])
        if ra["delta_cazada"] is not None and rb["delta_cazada"] is not None:
            dcd.append(ra["delta_cazada"]); dcn.append(rb["delta_cazada"])
        if ra["delta_yo"] is not None and rb["delta_yo"] is not None:
            yod.append(ra["delta_yo"]); yon.append(rb["delta_yo"])
        print(f"  {k:<3} {d:>5.2f} {A['hp_cazada0']:>6.0f}/{B['hp_cazada0']:<7.0f}"
              f" {A['dist_caz']:>4.1f}/{B['dist_caz']:<4.1f}"
              f" {ra['golpes']:>12} {rb['golpes']:>4}"
              f" {(ra['delta_cazada'] if ra['delta_cazada'] is not None else float('nan')):>15.0f}"
              f" {(rb['delta_cazada'] if rb['delta_cazada'] is not None else float('nan')):>7.0f}")

    if pares:
        mejor = sum(1 for x, y in zip(gd, gn) if x < y)
        peor = sum(1 for x, y in zip(gd, gn) if x > y)
        emp = len(gd) - mejor - peor
        print(f"\n  GOLPES a la cazada (menos es mejor): defensa gana {mejor} ·"
              f" pierde {peor} · empata {emp}"
              f"  · p(signos) = {signos(mejor, mejor+peor):.3f}")
        if dcd:
            md = sum(1 for x, y in zip(dcd, dcn) if x > y)
            pd_ = sum(1 for x, y in zip(dcd, dcn) if x < y)
            print(f"  DELTA hp de la cazada (mas es mejor): defensa gana {md} ·"
                  f" pierde {pd_} · empata {len(dcd)-md-pd_}"
                  f"  · p = {signos(md, md+pd_):.3f}")
            print(f"    mediana delta: con defensa {st.median(dcd):+.0f} ·"
                  f" sin defensa {st.median(dcn):+.0f}")
        # C · el precio emparejado
        print("\n" + "=" * 90)
        print("C · EL PRECIO, EMPAREJADO — ¿-20 hp es defender, o estar al lado?")
        print("=" * 90)
        if yod:
            print(f"\n  delta hp de la HERMANA QUE ACOMPANA, en el mismo tipo de ventana:")
            print(f"    la que DEFIENDE : mediana {st.median(yod):+.0f} (n={len(yod)})")
            print(f"    la que NO defiende: mediana {st.median(yon):+.0f} (n={len(yon)})")
            mj = sum(1 for x, y in zip(yod, yon) if x > y)
            pj = sum(1 for x, y in zip(yod, yon) if x < y)
            print(f"    pareado: defensora mejor {mj} · peor {pj} · empate "
                  f"{len(yod)-mj-pj} · p = {signos(mj, mj+pj):.3f}")

    # ── B · la autopsia de las ocasiones sin defensa (66) ─────────────────
    print("\n" + "=" * 90)
    print("B · LAS OCASIONES CON ALCANCE Y SIN DEFENSA (66) — una linea cada una")
    print("=" * 90)
    from proteccion import ocasiones_p2p
    from manada_campo import carga
    f66 = carga("manada2")
    ocs = [o for o in ocasiones_p2p(f66) if not o["defiende"]]
    print(f"\n  ocasiones con alcance sin defensa: {len(ocs)}\n")
    base = f"{P}/runs/manada2"
    for o in ocs:
        S = {"10": serie(diario(base, o["eid"], 10)),
             "11": serie(diario(base, o["eid"], 11))}
        yo = S[o["quien"]]
        ella = S["11" if o["quien"] == "10" else "10"]
        elegidos = {}
        hp0 = None
        segundo = 0
        for t in range(o["t0"], o["t1"] + 1):
            x = yo.get(t)
            if not isinstance(x, dict):
                continue
            hp0 = hp0 if hp0 is not None else x["hp"]
            elegidos[x.get("el")] = elegidos.get(x.get("el"), 0) + 1
            # ¿segundo agresor sobre MI?
            if x.get("dmg"):
                segundo += 1
        top = sorted(elegidos.items(), key=lambda kv: -kv[1])[:2]
        print(f"    {o['eid'][:18]} g{o['quien']} t{o['t0']}-{o['t1']}: "
              f"gano {top} · mi hp {hp0:.0f} · tics con dano propio {segundo}")


if __name__ == "__main__":
    main()

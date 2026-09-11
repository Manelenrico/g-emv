"""LA VARA REESCRITA Y EL FORENSE DE DESENLACES — PROMPT_68 C+E (coste 0).

C) OCASION corregida (la leccion del 67): hermana bajo caza certificada + la
   otra a <=2, sana (>=70), con arma, Y el agresor VISIBLE AHORA por la
   defensora —donde este, no donde el parte diga—, alineado y en alcance.
   Se recalcula P2' del 64 y del 66.
E) El forense de las respuestas (propias y por la hermana): ¿como acaba cada
   ventana? El agresor se va / muere (¿por nuestra mano?) / huimos / morimos.
   Para el sofa del dial de matar, ANTES de tocarlo.

Uso (desde la raiz del repo):  python3 paintball/desenlaces.py
"""
from __future__ import annotations

import collections
import json
import math
import os
import statistics as st

from proteccion_pareada import diario, serie, P

ARMAS_R = {"sword": 1, "spear": 2, "bow": 8, "knives": 5, "blowgun": 6}
VENT = 240                 # seguimiento del desenlace
LEJOS = 3


def episodios(tanda):
    return json.load(open(f"{P}/runs/{tanda}/episodios.json"))["eps"]


def cargar(tanda):
    base = f"{P}/runs/{tanda}"
    out = []
    for e in episodios(tanda):
        d10, d11 = diario(base, e["id"], 10), diario(base, e["id"], 11)
        if d10 and d11:
            out.append({"eid": e["id"], "S": {"10": serie(d10), "11": serie(d11)}})
    return out


# ── C · la vara de ocasion, reescrita ────────────────────────────────────────
def ocasiones_v2(eps):
    """Con el agresor VISIBLE AHORA (no la posicion del parte)."""
    out = []
    for ep in eps:
        S = ep["S"]
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
                ok = False
                if (p.get("agresor") and x["pos"] and y["pos"]
                        and math.dist(x["pos"], y["pos"]) <= 2.0
                        and x["hp"] >= 70):
                    r = ARMAS_R.get(x.get("hand"), 0)
                    if r and ap:
                        # el agresor VISIBLE: el cuerpo mas cercano a (ax,ay)
                        # que no sea ella ni yo, y donde este AHORA
                        for sl, a in (x.get("ve") or {}).items():
                            if sl in (int(yo), int(ella)):
                                continue
                            q = a.get("pos") or ()
                            if not q or max(abs(q[0] - ap[0]),
                                            abs(q[1] - ap[1])) > 1:
                                continue
                            dx, dy = q[0] - x["pos"][0], q[1] - x["pos"][1]
                            if ((dx == 0 or dy == 0 or abs(dx) == abs(dy))
                                    and max(abs(dx), abs(dy)) <= r):
                                ok = True
                            break
                if ok:
                    if cur is None:
                        cur = {"eid": ep["eid"], "yo": yo, "t0": t, "t1": t,
                               "defiende": False}
                    cur["t1"] = t
                    if (x.get("el") or "").startswith("atacar") and \
                            (x.get("honor") or {}).get("defensa_pareja"):
                        cur["defiende"] = True
                elif cur is not None:
                    out.append(cur); cur = None
            if cur is not None:
                out.append(cur)
    return out


# ── E · el forense de desenlaces ─────────────────────────────────────────────
def respuestas(eps):
    """Ventanas de RESPUESTA: tics consecutivos en que elegimos atacar_*."""
    out = []
    for ep in eps:
        S = ep["S"]
        for yo in ("10", "11"):
            cur = None
            for t in sorted(S[yo]):
                x = S[yo].get(t)
                if not isinstance(x, dict):
                    continue
                es_at = (x.get("el") or "").startswith("atacar")
                h = x.get("honor") or {}
                if es_at:
                    obj = h.get("objetivo")
                    if cur is None or cur["obj"] != obj:
                        if cur is not None:
                            out.append(cur)
                        cur = {"eid": ep["eid"], "yo": yo, "obj": obj,
                               "t0": t, "t1": t, "golpes": 0,
                               "por_hermana": bool(h.get("defensa_pareja")
                                                   and not h.get("era_agresor")),
                               "hp0": x["hp"], "S": S}
                    cur["t1"] = t
                    cur["golpes"] += 1
                elif cur is not None and t - cur["t1"] > 48:
                    out.append(cur); cur = None
            if cur is not None:
                out.append(cur)
    return out


def desenlace(r):
    S = r["S"]; yo = S[r["yo"]]
    post = [t for t in sorted(yo) if r["t1"] < t <= r["t1"] + VENT]
    # ¿el agresor sigue? (lo vemos y nos dana) ¿se va? ¿muere?
    ultimo_dano = None
    visto_ultimo = None
    for t in post:
        x = yo[t]
        if f"P{r['obj']}" in (x.get("dmg") or []):
            ultimo_dano = t
        a = (x.get("ve") or {}).get(r["obj"])
        if a and a.get("pos") and x["pos"]:
            visto_ultimo = (t, math.dist(x["pos"], a["pos"]))
    muero = any((yo.get(t) or {}).get("hp", 1) <= 0 for t in post)
    hp_fin = (yo.get(post[-1]) or {}).get("hp") if post else r["hp0"]
    # el agresor MUERE: deja de verse y no vuelve a aparecer en toda la vida
    vive_despues = False
    for t in sorted(yo):
        if t > r["t1"] + VENT and (yo[t].get("ve") or {}).get(r["obj"]):
            vive_despues = True
            break
    murio = (visto_ultimo is None or visto_ultimo[1] <= LEJOS) and not vive_despues \
        and not muero
    if muero:
        d = "MORIMOS"
    elif murio:
        d = "el agresor MUERE"
    elif ultimo_dano is None:
        d = "el agresor SE VA"
    elif visto_ultimo and visto_ultimo[1] > LEJOS:
        d = "nos alejamos"
    else:
        d = "sigue el acoso"
    tics = (ultimo_dano - r["t1"]) if ultimo_dano else 0
    return {"desenlace": d, "golpes": r["golpes"], "tics_hasta": tics,
            "hp_fin": hp_fin, "por_hermana": r["por_hermana"]}


def main():
    print("=" * 90)
    print("C · LA VARA DE OCASION, REESCRITA (agresor VISIBLE AHORA)")
    print("=" * 90)
    tot = {}
    for tanda, lbl in (("manada", "64 (v34)"), ("manada2", "66 (v35)")):
        eps = cargar(tanda)
        ocs = ocasiones_v2(eps)
        n = len(ocs); d = sum(1 for o in ocs if o["defiende"])
        tot[tanda] = (n, d, eps)
        print(f"\n  {lbl}: ocasiones {n} · defiende {d} = "
              f"{100*d/max(n,1):.0f} %"
              f"   (con la vara vieja: {'8 -> 62 %' if tanda=='manada' else '12 -> 50 %'})")
    n1, d1, _ = tot["manada"]; n2, d2, _ = tot["manada2"]
    print(f"\n  ACUMULADO 64+66: {d1+d2}/{n1+n2} = "
          f"{100*(d1+d2)/max(n1+n2,1):.0f} %")

    print("\n" + "=" * 90)
    print("E · EL FORENSE DE LAS RESPUESTAS — ¿como acaba cada pelea?")
    print("=" * 90)
    for tanda, lbl in (("manada2", "66 (v35, 918 respuestas)"),):
        eps = tot[tanda][2]
        rs = respuestas(eps)
        des = [desenlace(r) for r in rs]
        c = collections.Counter(d["desenlace"] for d in des)
        n = len(des)
        print(f"\n  {lbl}: {n} ventanas de respuesta\n")
        print(f"    {'desenlace':<22} {'n':>5} {'%':>6} {'golpes med':>11} "
              f"{'tics hasta':>11} {'hp final med':>13}")
        for k, v in c.most_common():
            g = [d["golpes"] for d in des if d["desenlace"] == k]
            ti = [d["tics_hasta"] for d in des if d["desenlace"] == k]
            hp = [d["hp_fin"] for d in des if d["desenlace"] == k and d["hp_fin"] is not None]
            print(f"    {k:<22} {v:>5} {100*v/n:>5.0f}% "
                  f"{st.median(g):>11.0f} {st.median(ti):>11.0f} "
                  f"{(st.median(hp) if hp else float('nan')):>13.0f}")
        # la pregunta del sofa
        pocos = [d for d in des if d["golpes"] <= 3]
        muchos = [d for d in des if d["golpes"] > 3]
        se_van = sum(1 for d in des if d["desenlace"] in ("el agresor SE VA", "nos alejamos"))
        matan = sum(1 for d in des if d["desenlace"] == "MORIMOS")
        print(f"\n  LA PREGUNTA DEL SOFA (sin sello):")
        print(f"    respuestas de <=3 golpes: {len(pocos)} ({100*len(pocos)/n:.0f} %)"
              f" · de mas: {len(muchos)}")
        print(f"    el agresor se va o nos separamos: {se_van} ({100*se_van/n:.0f} %)"
              f"  <- la persistencia ya basta")
        print(f"    acaban matandonos: {matan} ({100*matan/n:.0f} %)"
              f"  <- donde el dial importaria")
        por_h = [d for d in des if d["por_hermana"]]
        if por_h:
            ch = collections.Counter(d["desenlace"] for d in por_h)
            print(f"\n    de las {len(por_h)} respuestas POR LA HERMANA: {dict(ch)}")


if __name__ == "__main__":
    main()

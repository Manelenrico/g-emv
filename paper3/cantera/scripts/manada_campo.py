"""LA MANADA EN EL CAMPO — PROMPT_64. Varas V1-V8 sobre runs/manada (v34),
pareado contra runs/pareja2 (v30, el 57) con METODO IDENTICO donde aplica.

Lo nuevo: el honor en DOS numeros (iniciaciones-estrictas / defensas por la
hermana), la OCASION de defensa (una bajo caza certificada con la otra a <=2,
sana y armada), si la defensa LLEGA, si PROTEGE y a que PRECIO.

Uso (desde la raiz del repo):  python3 paintball/manada_campo.py
"""
from __future__ import annotations

import glob
import json
import math
import os
import statistics as st

from pareja import lee

P = os.path.dirname(os.path.abspath(__file__))
BANDA = 30.0
VENT_PRECIO = 240          # tics para medir el precio de defender


def diario_en(base, eid, s):
    fs = glob.glob(f"{base}/{eid}/a{s}/*.log") + glob.glob(f"{base}/{eid}/a{s}/*.jsonl")
    return list(lee(sorted(fs)[0])) if fs else None


def serie(recs):
    """tick -> foto del diario (pos, hp, arma, elegido, honor, parte, chat)."""
    out = {}
    for d in recs:
        if d.get("k") != "tick":
            continue
        rad = d.get("RADIOGRAFIA") or {}
        ah = rad.get("ahora") or {}
        out[d.get("tick", 0)] = {
            "pos": tuple(d.get("pos") or ()), "hp": float(d.get("hp") or 0),
            "live": d.get("phase") == "live",
            "hand": (d.get("hand") or {}).get("id") if isinstance(d.get("hand"), dict) else None,
            "el": rad.get("elegido"), "honor": rad.get("honor"),
            "parte": ah.get("parte"),
            "dmg": [g.get("source") for g in (d.get("damage_taken") or [])],
            "final": None}
    for d in recs:
        if d.get("k") == "final":
            out.setdefault("FINAL", d)
    return out


def carga(nombre, con_manada=True):
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
        filas.append({"eid": eid, "p10": r["placements"][10],
                      "p11": r["placements"][11],
                      "s10": serie(d10), "s11": serie(d11)})
    return filas


def honor_dos(filas):
    """(a) iniciaciones-estrictas · (b) defensas por la hermana · propias."""
    a = b = prop = contra_hermana = 0
    detalles_b = []
    for f in filas:
        for lado, quien in (("s10", "10"), ("s11", "11")):
            for t, x in f[lado].items():
                if t == "FINAL" or not isinstance(x, dict):
                    continue
                if not (x.get("el") or "").startswith("atacar"):
                    continue
                h = x.get("honor") or {}
                if h.get("es_la_pareja"):
                    contra_hermana += 1
                elif h.get("era_agresor"):
                    prop += 1
                elif h.get("defensa_pareja"):
                    b += 1
                    detalles_b.append((f["eid"], quien, t, h.get("objetivo")))
                else:
                    a += 1
    return a, b, prop, contra_hermana, detalles_b


def ocasiones(filas):
    """Ocasion de defensa: ella bajo caza CERTIFICADA (su parte a=1 con pos)
    y yo a <=2 de ella, sana (hp>=70) y con arma que dana."""
    ARMAS = {"sword", "spear", "bow", "knives"}
    out = []
    for f in filas:
        for yo_l, ella_l, quien in (("s10", "s11", "10"), ("s11", "s10", "11")):
            en_curso = None
            for t in sorted(k for k in f[yo_l] if k != "FINAL"):
                x, y = f[yo_l].get(t), f[ella_l].get(t)
                if not isinstance(x, dict) or not isinstance(y, dict):
                    continue
                if not x.get("live") or x["hp"] <= 0 or y["hp"] <= 0:
                    continue
                p = x.get("parte") or {}
                cond = (p.get("agresor") and p.get("agresor_pos")
                        and x["pos"] and y["pos"]
                        and math.dist(x["pos"], y["pos"]) <= 2.0
                        and x["hp"] >= 70 and (x.get("hand") in ARMAS))
                if cond:
                    if en_curso is None:
                        en_curso = {"eid": f["eid"], "quien": quien, "t0": t,
                                    "t1": t, "defiende": False, "tick_def": None}
                    en_curso["t1"] = t
                    if (x.get("el") or "").startswith("atacar") and \
                            (x.get("honor") or {}).get("defensa_pareja"):
                        en_curso["defiende"] = True
                        en_curso["tick_def"] = en_curso["tick_def"] or t
                elif en_curso is not None:
                    out.append(en_curso)
                    en_curso = None
            if en_curso is not None:
                out.append(en_curso)
    return out


def protege(filas, ocs):
    """V4: ¿la cazada sobrevive mas cuando la hermana defiende?"""
    con, sin = [], []
    for o in ocs:
        f = next(x for x in filas if x["eid"] == o["eid"])
        ella_l = "s11" if o["quien"] == "10" else "s10"
        ticks = sorted(k for k in f[ella_l] if k != "FINAL")
        muerte = None
        for t in ticks:
            x = f[ella_l][t]
            if isinstance(x, dict) and x["hp"] <= 0:
                muerte = t
                break
        vive_tras = (muerte is None) or (muerte - o["t1"] > VENT_PRECIO)
        (con if o["defiende"] else sin).append(vive_tras)
    return con, sin


def precio(filas, ocs):
    """V5: vida de la que defiende tras defender; muertes en 240 tics; ambas."""
    caidas = ambas = 0
    hp_delta = []
    n = 0
    for o in ocs:
        if not o["defiende"]:
            continue
        n += 1
        f = next(x for x in filas if x["eid"] == o["eid"])
        yo_l = "s10" if o["quien"] == "10" else "s11"
        ella_l = "s11" if o["quien"] == "10" else "s10"
        td = o["tick_def"]
        hp0 = (f[yo_l].get(td) or {}).get("hp")
        fin = [t for t in sorted(k for k in f[yo_l] if k != "FINAL")
               if td < t <= td + VENT_PRECIO]
        hp1 = (f[yo_l].get(fin[-1]) or {}).get("hp") if fin else hp0
        if hp0 is not None and hp1 is not None:
            hp_delta.append(hp1 - hp0)
        muere_yo = any((f[yo_l].get(t) or {}).get("hp", 1) <= 0 for t in fin)
        muere_ella = any((f[ella_l].get(t) or {}).get("hp", 1) <= 0 for t in fin)
        caidas += 1 if muere_yo else 0
        ambas += 1 if (muere_yo and muere_ella) else 0
    return n, caidas, ambas, hp_delta


def golpes_entre(filas):
    """V1: golpes de una hermana a la otra y su causa (¿eligio atacarla?)."""
    out = []
    for f in filas:
        for yo_l, otra_l, yo, otra in (("s10", "s11", 10, 11), ("s11", "s10", 11, 10)):
            for t in sorted(k for k in f[yo_l] if k != "FINAL"):
                x = f[yo_l][t]
                if not isinstance(x, dict):
                    continue
                if f"P{otra}" in (x.get("dmg") or []):
                    y = f[otra_l].get(t) or {}
                    el = y.get("el") if isinstance(y, dict) else None
                    h = (y.get("honor") or {}) if isinstance(y, dict) else {}
                    out.append({"eid": f["eid"], "victima": yo, "t": t,
                                "eligio": el, "objetivo": h.get("objetivo"),
                                "contra_hermana": bool(h.get("es_la_pareja"))})
    return out


def moneda(filas):
    mejor = [min(f["p10"], f["p11"]) for f in filas]
    return {"n": len(filas), "top4": sum(1 for m in mejor if m <= 4),
            "wins": sum(1 for m in mejor if m == 1),
            "podio": sum(1 for f in filas if {f["p10"], f["p11"]} <= {1, 2}),
            "ambas8": sum(1 for f in filas if f["p10"] <= 8 and f["p11"] <= 8),
            "mejor_med": st.median(mejor)}


def estab(filas):
    cool, cong = [], []
    for f in filas:
        for lado in ("s10", "s11"):
            fin = f[lado].get("FINAL")
            if fin:
                cool.append(fin.get("tics_cooldown", 0))
                cong.append(fin.get("tics_congelado", 0))
    return (st.median(cool) if cool else None), (st.median(cong) if cong else None)


def main():
    v34 = carga("manada")
    v30 = carga("pareja2")
    print("=" * 92)
    print(f"LA MANADA EN EL CAMPO — v34 ({len(v34)} eps) vs v30 del 57 ({len(v30)} eps)")
    print("=" * 92)

    for filas, nom in ((v34, "v34"), (v30, "v30 (57)")):
        a, b, prop, ch, det = honor_dos(filas)
        ocs = ocasiones(filas)
        con, sin = protege(filas, ocs)
        n_def, caidas, ambas, hpd = precio(filas, ocs)
        M = moneda(filas)
        cool, cong = estab(filas)
        print(f"\n  [{nom}]")
        print(f"  V1 HONOR: (a) iniciaciones-estrictas {a} · (b) DEFENSAS por la"
              f" hermana {b} · respuestas a mi agresor {prop} · ataques a la"
              f" hermana {ch}")
        print(f"  V2 OCASION: {len(ocs)} ventanas en "
              f"{len(set(o['eid'] for o in ocs))} eps")
        dfd = [o for o in ocs if o["defiende"]]
        print(f"  V3 LA DEFENSA LLEGA: {len(dfd)}/{len(ocs)} "
              f"({100*len(dfd)/max(len(ocs),1):.0f}%)")
        print(f"  V4 ¿PROTEGE?: sobrevive tras la ventana — con defensa "
              f"{sum(con)}/{len(con)} · sin defensa {sum(sin)}/{len(sin)}")
        print(f"  V5 EL PRECIO: {n_def} defensas · la defensora cae en 240 tics"
              f" {caidas} · AMBAS caen {ambas} · delta hp mediano "
              f"{(st.median(hpd) if hpd else float('nan')):.0f}")
        print(f"  V6 juntas a 8: {M['ambas8']}/{M['n']} "
              f"({100*M['ambas8']/max(M['n'],1):.0f}%)")
        print(f"  V7 moneda: top4 {M['top4']} ({100*M['top4']/max(M['n'],1):.0f}%) ·"
              f" wins {M['wins']} · podio {M['podio']} · mejor-med {M['mejor_med']}")
        print(f"  V8: cooldown {cool} · congelado {cong}")
        if nom == "v34":
            print("\n  DEFENSAS (eid, gemela, tick, objetivo):")
            for eid, q, t, ob in det[:20]:
                print(f"    {eid[:18]} gemela{q} t{t} -> slot {ob}")
            g = golpes_entre(filas)
            print(f"\n  GOLPES ENTRE HERMANAS: {len(g)}")
            for x in g[:10]:
                print(f"    {x['eid'][:18]} victima P{x['victima']} t{x['t']}:"
                      f" la otra eligio `{x['eligio']}` (objetivo {x['objetivo']},"
                      f" contra_hermana={x['contra_hermana']})")
            json.dump({"defensas": det, "ocasiones": ocs,
                       "golpes": g, "moneda": M},
                      open(f"{P}/runs/manada/resumen.json", "w"),
                      indent=1, default=str)


if __name__ == "__main__":
    main()

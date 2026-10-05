"""PAPER CUATRO · PASO 1 · PARTE A — la regla de aprendizaje, en seco.

SOLO LECTURA. No toca el agente ni el motor. Corre sobre los diarios de la
serie limpia (tanda 66 = `paintball/runs/manada2/`, 40 partidas, asientos
10 y 11) la regla acordada: se aprende MAGNITUD y ALCANCE por arma; la unidad
de aprendizaje es el GOLPE, no el tic.

Memoria M[W] = {n, E[W] (media acumulada del daño por golpe), histograma de
distancias Chebyshev desde las que llegó cada golpe}.  R[W] = max de esas
distancias (se da también el percentil 95).

Atribución: arma = `ve_agentes[].hand` del asiento que figura en
`damage_taken.source` EN EL MISMO TIC. Si ese asiento no está a la vista, el
golpe no enseña nada y se cuenta aparte. Anillo (`zone`) y veneno (`poison`)
quedan fuera.

Lector: `pareja.lee`. Distancia: Chebyshev, la del decisor.

Uso:  python3 cantera/paper4/regla_en_seco.py
"""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from pareja import lee                                    # noqa: E402

TANDA = os.path.join(RAIZ, "paintball", "runs", "manada2")
SLOTS = (10, 11)
ARMAS = ["sword", "spear", "none", "knives", "bow", "blowgun"]
REF = {"sword": (19.76, 1), "spear": (12.8, 2), "bow": (14.0, "lejos"),
       "knives": (8.0, "plano"), "none": (5.07, 1), "blowgun": (4.0, "3-4")}


def orden_de_juego():
    """Las 40 partidas en el orden en que se jugaron, por `job_index`."""
    E = json.load(open(f"{TANDA}/episodios.json"))
    eps = sorted(E["eps"], key=lambda e: e["job_index"])
    return [(e["job_index"], e["id"]) for e in eps]


def diario(eid, slot):
    fs = glob.glob(f"{TANDA}/{eid}/a{slot}/*.log")
    return list(lee(sorted(fs)[0])) if fs else None


def golpes_del_diario(recs, slot):
    """Golpes recibidos, con arma atribuida si el asiento estaba a la vista."""
    out, ciegos, ambiente = [], 0, defaultdict(int)
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        dt = r.get("damage_taken") or []
        if not dt:
            continue
        pos = r.get("pos")
        vis = {a.get("slot"): a for a in (r.get("ve_agentes") or [])}
        for g in dt:
            src, amt = g.get("source"), float(g.get("amount") or 0.0)
            if not (isinstance(src, str) and src.startswith("P")):
                ambiente[str(src)] += 1
                continue
            s = int(src[1:])
            a = vis.get(s)
            if a is None or not pos or not a.get("pos"):
                ciegos += 1
                continue
            q = a["pos"]
            d = max(abs(int(q[0]) - pos[0]), abs(int(q[1]) - pos[1]))
            out.append({"tick": r["tick"], "slot_src": s,
                        "arma": a.get("hand") or "none", "dano": amt, "dist": d})
    return out, ciegos, ambiente


class Memoria:
    """M: por arma, n golpes, media acumulada del daño, histograma de distancia."""

    def __init__(self):
        self.n = defaultdict(int)
        self.E = defaultdict(float)
        self.hist = defaultdict(lambda: defaultdict(int))

    def aprende(self, arma, dano, dist):
        self.n[arma] += 1
        # media acumulada == error de predicción con paso 1/n
        self.E[arma] += (dano - self.E[arma]) / self.n[arma]
        self.hist[arma][dist] += 1

    def R(self, arma):
        h = self.hist.get(arma)
        return max(h) if h else None

    def R95(self, arma):
        h = self.hist.get(arma)
        if not h:
            return None
        ds = sorted(d for d, c in h.items() for _ in range(c))
        return ds[min(len(ds) - 1, int(0.95 * len(ds)))]

    def foto(self):
        return {w: (self.n[w], self.E[w], self.R(w), self.R95(w)) for w in self.n}


def corre(compartida=True):
    orden = orden_de_juego()
    Ms = {"comun": Memoria()} if compartida else {10: Memoria(), 11: Memoria()}
    traza, ciegos_tot, amb_tot, ngolpes = [], 0, defaultdict(int), 0
    for ji, eid in orden:
        for s in SLOTS:
            recs = diario(eid, s)
            if not recs:
                continue
            gs, ci, amb = golpes_del_diario(recs, s)
            ciegos_tot += ci
            for k, v in amb.items():
                amb_tot[k] += v
            M = Ms["comun"] if compartida else Ms[s]
            for g in sorted(gs, key=lambda x: x["tick"]):
                M.aprende(g["arma"], g["dano"], g["dist"])
                ngolpes += 1
        foto = (Ms["comun"].foto() if compartida
                else {"a10": Ms[10].foto(), "a11": Ms[11].foto()})
        traza.append({"ji": ji, "eid": eid, "foto": foto})
    return Ms, traza, ciegos_tot, amb_tot, ngolpes


def main():
    print(f"  tanda: {TANDA}")
    orden = orden_de_juego()
    print(f"  orden de juego: por `job_index` de episodios.json "
          f"({orden[0][0]}..{orden[-1][0]}, {len(orden)} partidas)")
    print(f"  primera: {orden[0][1][:13]} · última: {orden[-1][1][:13]}")

    Ms, traza, ciegos, amb, ng = corre(compartida=True)
    M = Ms["comun"]
    print(f"\n  golpes que ENSEÑAN (asiento visible, arma atribuida): {ng}")
    print(f"  golpes de asiento NO visible (no enseñan nada): {ciegos}")
    print(f"  golpes de ambiente excluidos: {dict(amb)}")

    # ── A4 trayectoria ──────────────────────────────────────────────────
    print(f"\n=== A4 · TRAYECTORIA, partida a partida (memoria COMPARTIDA) ===")
    cab = "  #  " + "".join(f"{w[:7]:>16}" for w in ARMAS)
    print(cab)
    print("     " + "".join(f"{'E  / R  (n)':>16}" for _ in ARMAS))
    for f in traza:
        fila = f"  {f['ji']:>2} "
        for w in ARMAS:
            if w in f["foto"]:
                n, E, R, _ = f["foto"][w]
                fila += f"{f'{E:5.2f}/{R}({n})':>16}"
            else:
                fila += f"{'-':>16}"
        print(fila)

    # convergencia
    print(f"\n  primera partida en que E[W] entra en el ±10 % y ±5 % del valor final:")
    for w in ARMAS:
        fin = M.E.get(w)
        if not fin:
            print(f"    {w:<9} sin golpes")
            continue
        p10 = p5 = None
        for f in traza:
            if w not in f["foto"]:
                continue
            E = f["foto"][w][1]
            if p10 is None and abs(E - fin) <= 0.10 * fin:
                p10 = f["ji"]
            if p5 is None and abs(E - fin) <= 0.05 * fin:
                p5 = f["ji"]
        # primera vez que YA NO SALE del margen (estabilidad, no toque)
        est10 = est5 = None
        for f in reversed(traza):
            if w not in f["foto"]:
                break
            E = f["foto"][w][1]
            if abs(E - fin) <= 0.10 * fin:
                est10 = f["ji"]
            else:
                break
        for f in reversed(traza):
            if w not in f["foto"]:
                break
            E = f["foto"][w][1]
            if abs(E - fin) <= 0.05 * fin:
                est5 = f["ji"]
            else:
                break
        print(f"    {w:<9} toca ±10 % en #{p10} · ±5 % en #{p5} · "
              f"y YA NO SALE del ±10 % desde #{est10} · del ±5 % desde #{est5}")

    # ── A5 finales ──────────────────────────────────────────────────────
    print(f"\n=== A5 · FINALES contra la referencia del paso 0 ===")
    print(f"    {'arma':<9}{'n':>5}{'E[W]':>9}{'ref':>9}{'R[W]':>6}{'R95':>5}"
          f"{'ref alcance':>13}   histograma de distancias")
    for w in ARMAS:
        if w not in M.n:
            print(f"    {w:<9}    0        -")
            continue
        rE, rR = REF[w]
        h = dict(sorted(M.hist[w].items()))
        print(f"    {w:<9}{M.n[w]:>5}{M.E[w]:>9.2f}{rE:>9.2f}{M.R(w):>6}"
              f"{M.R95(w):>5}{str(rR):>13}   {h}")

    # ── A3 memorias separadas ───────────────────────────────────────────
    Ms2, traza2, _, _, _ = corre(compartida=False)
    print(f"\n=== A3 · MEMORIA COMPARTIDA contra SEPARADA (final) ===")
    print(f"    {'arma':<9}{'común E/R (n)':>20}{'a10 E/R (n)':>20}{'a11 E/R (n)':>20}"
          f"{'|ΔE| a10-a11':>14}")
    for w in ARMAS:
        if w not in M.n:
            continue
        A, Bq = Ms2[10], Ms2[11]
        ca = f"{M.E[w]:.2f}/{M.R(w)} ({M.n[w]})"
        aa = f"{A.E[w]:.2f}/{A.R(w)} ({A.n[w]})" if w in A.n else "-"
        bb = f"{Bq.E[w]:.2f}/{Bq.R(w)} ({Bq.n[w]})" if w in Bq.n else "-"
        dd = (f"{abs(A.E[w]-Bq.E[w]):.2f}" if w in A.n and w in Bq.n else "-")
        print(f"    {w:<9}{ca:>20}{aa:>20}{bb:>20}{dd:>14}")

    # se deja la memoria compartida en un json para la PARTE B
    salida = {"orden": [e for _, e in orden],
              "por_partida": [{"ji": f["ji"], "eid": f["eid"],
                               "M": {w: {"n": v[0], "E": v[1], "R": v[2]}
                                     for w, v in f["foto"].items()}}
                              for f in traza]}
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memoria_aprendida.json")
    json.dump(salida, open(p, "w"), indent=1)
    print(f"\n  memoria partida a partida -> {p}")


if __name__ == "__main__":
    main()

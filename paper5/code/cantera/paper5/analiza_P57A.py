"""[P5-7A] Junta las medidas de un mundo y las imprime, con los sellos K1-K6.

  python3 cantera/paper5/analiza_P57A.py s2
  python3 cantera/paper5/analiza_P57A.py lento
"""
from __future__ import annotations
import json, math, os, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import curiosidad as C                                    # noqa: E402

TRAMOS = 4
VARIANTES = {"local": "el renglon LOCAL (A3)",
             "front": "la LLAMADA DE LA FRONTERA (anadido)"}
CONFIGS = tuple(f"{v}_{k}" for v in VARIANTES
                for k in ("k0.1", "k0.2", "k0.4", "k0.2_sin_balanza"))


def pc(a, b):
    return f"{a}/{b} = {100.0 * a / b:.2f} %" if b else f"{a}/0 = —"


def med(v):
    return st.median(v) if v else None


def sellos(R, v, dec):
    c2 = R[f"{v}_k0.2"]
    cs = R[f"{v}_k0.2_sin_balanza"]
    c4, c1 = R[f"{v}_k0.4"], R[f"{v}_k0.1"]
    ps = 100.0 * c2["por_grado"].get("seguro", 0) / max(1, c2["n_grado"].get("seguro", 0))
    pi = 100.0 * c2["por_grado"].get("inseguro", 0) / max(1, c2["n_grado"].get("inseguro", 0))
    pi_sb = 100.0 * cs["por_grado"].get("inseguro", 0) / max(1, cs["n_grado"].get("inseguro", 0))
    ok2 = ps > 3 and pi < 0.3 and pi_sb > 1
    print(f"  K2 · k=0,2 con balanza: seguro {ps:.2f} % (pide >3) · "
          f"inseguro {pi:.2f} % (pide <0,3) · sin balanza inseguro "
          f"{pi_sb:.2f} % (pide >1)  -> {'CUMPLE' if ok2 else 'FALLA'}")
    vz = 100.0 * c2["voz_carencia"][0] / max(1, c2["voz_carencia"][1])
    aviso = " ** <0,2: la opcion A se reexamina **" if vz < 0.2 else ""
    print(f"  K3 · voz propia con R-CARENCIA>=0,25: {vz:.2f} % (pide >1) "
          f"-> {'CUMPLE' if vz > 1 else 'FALLA'}{aviso}")
    d4 = 100.0 * c4["derroche_arma"] / max(1, c4["cambios"])
    ok4 = d4 > 1 and c1["derroche_arma"] == 0
    print(f"  K4 · derroche k=0,4: {d4:.2f} % (pide >1, sobre {c4['cambios']} "
          f"cambios) · k=0,1: {c1['derroche_arma']} (pide 0) "
          f"-> {'CUMPLE' if ok4 else 'FALLA'}")
    rr, rp = c2["revela_real"], c2["revela_proy"]
    if sum(rr):
        rz = sum(rp) / sum(rr)
        print(f"  K5 · razon proyectado/real (k=0,2): {rz:.2f}x (pide >=2) "
              f"-> {'CUMPLE' if rz >= 2 else 'FALLA'}  [n={len(rp)}]")
    else:
        print(f"  K5 · sin datos (n={len(rp)} cambios)")


def main():
    cual = sys.argv[1] if len(sys.argv) > 1 else "s2"
    D = json.load(open(os.path.join(AQUI, f"P57A_{cual}.json")))
    print(f"===== P5-7A · {cual.upper()} · {len(D)} asientos-partida =====")
    vivos = sum(o["tics_vivos"] for o in D)
    dec = sum(o["decididos"] for o in D)
    print(f"tics vivos {vivos:,} · tics decididos (muestreo) {dec:,}")

    # ── A1 ───────────────────────────────────────────────────────────────
    print("\n== A1 · LA IGNORANCIA, COMO NUMERO ==")
    g = [x for o in D for x in o["A1"]["global"]]
    l = [x for o in D for x in o["A1"]["local"]]
    n = [x for o in D for x in o["A1"]["novedad"]]
    print(f"  global   : mediana {med(g):.4f} · min {min(g):.4f} · max {max(g):.4f}")
    print(f"  local(r6): mediana {med(l):.4f} · media {st.mean(l):.4f} · "
          f"tics con local>0: {pc(sum(1 for x in l if x > 0), len(l))}")
    print(f"  novedad  : mediana {med(n):.1f} · max {max(n)}")
    print("  por tramo de vida (mediana global · local · novedad):")
    for i in range(TRAMOS):
        gg = [x[0] for o in D for x in o["A1"]["por_tramo"][i]]
        ll = [x[1] for o in D for x in o["A1"]["por_tramo"][i]]
        nn = [x[2] for o in D for x in o["A1"]["por_tramo"][i]]
        if gg:
            print(f"    tramo {i + 1}: {med(gg):.4f} · {med(ll):.4f} · "
                  f"{med(nn):.1f}   (n={len(gg):,})")
    print("  vistas por asiento (mediana): "
          f"{med([o['vistas'] for o in D])} de {D[0]['n_arena']}")

    # ── A2 ───────────────────────────────────────────────────────────────
    print("\n== A2 · LA AMENAZA, GRADUADA ==")
    G = {k: sum(o["A2"]["grados"][k] for o in D)
         for k in ("seguro", "neutro", "inseguro")}
    tot = sum(G.values())
    for k in ("seguro", "neutro", "inseguro"):
        print(f"  {k:9s}: {pc(G[k], tot)}")
    am = [x for o in D for x in o["A2"]["valores"]]
    print(f"  amenaza: mediana {med(am):.4f} · media {st.mean(am):.4f}")
    des = {k: sum(o["A2"]["desglose"][k] for o in D)
           for k in ("armados", "dano", "anillo")}
    print(f"  tics con cada termino > 0: armados {pc(des['armados'], tot)} · "
          f"dano {pc(des['dano'], tot)} · anillo {pc(des['anillo'], tot)}")

    # ── A4 / A5 ──────────────────────────────────────────────────────────
    print("\n== A4 · EN SECO, POR CONFIGURACION ==")
    R = {}
    for etq in CONFIGS:
        c = {"cambios": 0, "por_grado": {}, "n_grado": {},
             "por_tramo": [0] * TRAMOS, "veto_arma": 0, "veto_vida": 0,
             "derroche_arma": 0, "derroche_anillo": 0,
             "voz_carencia": [0, 0], "voz_W": [0, 0],
             "revela_real": [], "revela_proy": [],
             "tics_con_M": 0, "cands_con_M": 0, "cands": 0, "max_M": 0.0}
        for o in D:
            s = o["cfg"][etq]
            c["cambios"] += s["cambios"]
            for k, v in s["por_grado"].items():
                c["por_grado"][k] = c["por_grado"].get(k, 0) + v
            for k, v in s["n_grado"].items():
                c["n_grado"][k] = c["n_grado"].get(k, 0) + v
            for i in range(TRAMOS):
                c["por_tramo"][i] += s["por_tramo"][i]
            for k in ("veto_arma", "veto_vida", "derroche_arma",
                      "derroche_anillo"):
                c[k] += s[k]
            for k in ("voz_carencia", "voz_W"):
                c[k][0] += s[k][0]; c[k][1] += s[k][1]
            for k in ("tics_con_M", "cands_con_M", "cands"):
                c[k] += s[k]
            c["max_M"] = max(c["max_M"], s["max_M"])
            c["revela_real"] += s["revela_real"]
            c["revela_proy"] += s["revela_proy"]
        R[etq] = c
        print(f"\n  --- {etq} ---")
        print(f"  [diagnostico] el renglon se ENCIENDE (M>0) en "
              f"{pc(c['tics_con_M'], dec)} de los tics · "
              f"{pc(c['cands_con_M'], c['cands'])} de los candidatos · "
              f"M maximo {c['max_M']:.5f}")
        print(f"  (a) cambian: {pc(c['cambios'], dec)}")
        for gr in ("seguro", "neutro", "inseguro"):
            print(f"      {gr:9s}: {pc(c['por_grado'].get(gr, 0), c['n_grado'].get(gr, 0))}")
        print(f"      por tramo: " + " · ".join(
            f"t{i + 1} {c['por_tramo'][i]}" for i in range(TRAMOS)))
        rr, rp = c["revela_real"], c["revela_proy"]
        if rp:
            print(f"  (b) casillas nuevas: diario real mediana {med(rr):.1f} "
                  f"(suma {sum(rr)}) · candidato nuevo PROYECTADO mediana "
                  f"{med(rp):.1f} (suma {sum(rp)}) · n={len(rp)}")
            print(f"      razon proyectado/real (sumas): "
                  f"{sum(rp) / sum(rr):.2f}x" if sum(rr) else
                  "      razon: el diario no revelo nada")
        print(f"  (c) VOZ PROPIA · con R-CARENCIA>=0,25: "
              f"{pc(c['voz_carencia'][0], c['voz_carencia'][1])}")
        print(f"                 · con W<2            : "
              f"{pc(c['voz_W'][0], c['voz_W'][1])}")
        print(f"  (d) VETO VITAL · armado a tiro: {c['veto_arma']} · "
              f"vida<30: {c['veto_vida']}  (deben ser cero o casi)")
        print(f"  (e) DERROCHE   · acerca a un armado: "
              f"{pc(c['derroche_arma'], c['cambios'])} · mete en el anillo: "
              f"{pc(c['derroche_anillo'], c['cambios'])}")

    # ── A6 ───────────────────────────────────────────────────────────────
    print("\n== A6 · COSTE POR DECISION ==")
    b = [x for o in D for x in o["ms"]["base"]]
    n2 = [x for o in D for x in o["ms"]["con"]]
    fr = [x for o in D for x in o["ms"].get("front", [])]
    bf = [x for o in D for x in o["ms"].get("bfs", [])]
    print(f"  decision SIN renglon      : mediana {med(b):.3f} ms · max {max(b):.3f}")
    print(f"  decision CON local  (k0,2): mediana {med(n2):.3f} ms · max {max(n2):.3f}"
          f"  -> sobrecoste {med(n2) - med(b):+.3f} ms")
    if fr:
        print(f"  decision CON frontera(k0,2): mediana {med(fr):.3f} ms · "
              f"max {max(fr):.3f}  -> sobrecoste {med(fr) - med(b):+.3f} ms")
    if bf:
        print(f"  BFS de la frontera (UNO por tic, sirve a los 4 k y a todos "
              f"los candidatos): mediana {med(bf):.3f} ms · max {max(bf):.3f}")

    # ── los sellos ───────────────────────────────────────────────────────
    # ── LAS DOS VARIANTES, LADO A LADO ───────────────────────────────────
    print("\n== LAS DOS VARIANTES, LADO A LADO ==")
    print(f"  {'medida':38s} {'LOCAL':>16s} {'FRONTERA':>16s}")

    def fila(etq, f, k="k0.2"):
        a, b_ = R[f"local_{k}"], R[f"front_{k}"]
        print(f"  {etq:38s} {f(a):>16s} {f(b_):>16s}")

    def _p(c, num, den):
        return f"{100.0 * num(c) / max(1, den(c)):.2f} %"
    fila("se enciende (M>0), % de tics",
         lambda c: _p(c, lambda x: x["tics_con_M"], lambda x: dec))
    fila("M maximo", lambda c: f"{c['max_M']:.5f}")
    fila("(a) decisiones que cambian",
         lambda c: _p(c, lambda x: x["cambios"], lambda x: dec))
    for gr in ("seguro", "neutro", "inseguro"):
        fila(f"    en entorno {gr}",
             lambda c, g=gr: _p(c, lambda x: x["por_grado"].get(g, 0),
                                lambda x: x["n_grado"].get(g, 0)))
    fila("(c) voz propia, R-CARENCIA>=0,25",
         lambda c: _p(c, lambda x: x["voz_carencia"][0],
                      lambda x: x["voz_carencia"][1]))
    fila("(d) veto: armado a tiro",
         lambda c: str(c["veto_arma"]))
    fila("(d) veto: vida < 30", lambda c: str(c["veto_vida"]))
    fila("(e) derroche: acerca a un armado",
         lambda c: _p(c, lambda x: x["derroche_arma"], lambda x: x["cambios"]))
    fila("(e) derroche: mete en el anillo",
         lambda c: _p(c, lambda x: x["derroche_anillo"],
                      lambda x: x["cambios"]))
    fila("(b) razon proyectado/real",
         lambda c: (f"{sum(c['revela_proy']) / sum(c['revela_real']):.2f}x"
                    if sum(c["revela_real"]) else "—"))
    print("  (k = 0,2 con balanza en las dos columnas)")

    print("\n== SELLOS K1-K6 (contadores), POR VARIANTE ==")
    seg = 100.0 * G["seguro"] / tot
    print(f"  K1 · entorno seguro = {seg:.2f} % "
          f"({'lento pide >10' if cual == 'lento' else 'S-2 pide <5'}) "
          f"[K1 no depende de la variante]")
    for v, nom in VARIANTES.items():
        print(f"\n  --- {nom} ---")
        sellos(R, v, dec)
    c2 = R["local_k0.2"]
    return
    ps = 100.0 * c2["por_grado"].get("seguro", 0) / max(1, c2["n_grado"].get("seguro", 0))
    pi = 100.0 * c2["por_grado"].get("inseguro", 0) / max(1, c2["n_grado"].get("inseguro", 0))
    cs = R["k0.2_sin_balanza"]
    pi_sb = 100.0 * cs["por_grado"].get("inseguro", 0) / max(1, cs["n_grado"].get("inseguro", 0))
    print(f"  K2 · k=0,2 con balanza: seguro {ps:.2f} % (pide >3) · "
          f"inseguro {pi:.2f} % (pide <0,3) · sin balanza inseguro "
          f"{pi_sb:.2f} % (pide >1)")
    vz = 100.0 * c2["voz_carencia"][0] / max(1, c2["voz_carencia"][1])
    print(f"  K3 · voz propia con R-CARENCIA>=0,25: {vz:.2f} % "
          f"(pide >1; si <0,2 se reexamina la opcion A)")
    c4, c1 = R["k0.4"], R["k0.1"]
    print(f"  K4 · derroche k=0,4: "
          f"{100.0 * c4['derroche_arma'] / max(1, c4['cambios']):.2f} % "
          f"(pide >1) · k=0,1: {c1['derroche_arma']} (pide 0)")
    rr, rp = c2["revela_real"], c2["revela_proy"]
    print(f"  K5 · razon proyectado/real (k=0,2): "
          f"{sum(rp) / sum(rr):.2f}x (pide >=2)" if sum(rr) else
          "  K5 · el diario no revelo nada en esas ventanas")
    print(f"  K6 · sobrecoste {med(n2) - med(b):+.3f} ms · "
          f"decision entera {med(n2):.3f} ms (pide <3)")


if __name__ == "__main__":
    main()

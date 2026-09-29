"""[P5-7B] Junta B1 y B3 y coteja los sellos O1 a O6."""
import collections, json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import otros as O                                          # noqa: E402

CONF = ("otros_k0.05", "otros_k0.1", "otros_k0.2",
        "vinc_k0.1", "vinc_k0.2", "juntas_0.1_0.1")


def pc(a, b):
    return f"{a}/{b} = {100.0 * a / b:.2f} %" if b else f"{a}/0 = —"


def b1(nom):
    D = json.load(open(os.path.join(AQUI, f"P57B_b1_{nom}.json")))
    out = {}
    for N in ("100", "250"):
        t = collections.Counter()
        for o in D:
            for k, v in o["reparto"][N].items():
                t[k] += v
        sale = [x for o in D for x in o["sale_de_neutro"][N]]
        out[N] = (dict(t), st.median(sale) if sale else None, len(sale))
    con = [x for o in D for x in o["conocimiento"]]
    return D, out, con


def main():
    print("===== P5-7B · LA CURIOSIDAD Y EL VINCULO CON LOS OTROS =====")
    print("\n== B1 · LA MEMORIA POR ASIENTO, y el reparto por signo ==")
    R = {}
    for nom in ("s2", "lento", "434"):
        p = os.path.join(AQUI, f"P57B_b1_{nom}.json")
        if not os.path.exists(p):
            continue
        D, out, con = b1(nom)
        R[nom] = out
        print(f"\n  --- {nom} ({len(D)} asientos-partida) ---")
        for N in ("100", "250"):
            t, med, n = out[N]
            v = t["vistos"]
            print(f"   N={N:>3s}: vistos {v:5d} · negativos "
                  f"{100 * t['negativos'] / v:5.1f} % · neutros "
                  f"{100 * t['neutros'] / v:5.1f} % · positivos "
                  f"{100 * t['positivos'] / v:5.1f} % · sale de neutro en "
                  f"{med} tics (n={n})")
        print(f"   conocimiento: mediana {st.median(con):.3f} · "
              f"asientos que pegan SIN verles arma "
              f"{sum(o['sin_arma_pero_pega'] for o in D)}")

    print("\n== B3 · EN SECO, POR CONFIGURACION ==")
    B3 = {}
    for nom in ("s2", "lento"):
        p = os.path.join(AQUI, f"P57B_b3_{nom}.json")
        if not os.path.exists(p):
            continue
        D = json.load(open(p))
        dec = sum(o["decididos"] for o in D)
        print(f"\n  --- {nom}: {len(D)} asientos · {dec:,} decisiones "
              f"muestreadas ---")
        B3[nom] = {}
        for etq in CONF:
            c = collections.Counter()
            pg, ng = collections.Counter(), collections.Counter()
            for o in D:
                s = o["cfg"][etq]
                for k in ("cambios", "veto_arma", "derroche",
                          "con_desconocido", "n_otros", "n_vinc"):
                    c[k] += s[k]
                c["voz0"] += s["voz_carencia"][0]
                c["voz1"] += s["voz_carencia"][1]
                pg.update(s["por_grado"]); ng.update(s["n_grado"])
            B3[nom][etq] = (c, pg, ng, dec)
            print(f"   {etq:16s} cambian {pc(c['cambios'], dec):>18s} · "
                  f"seguro {pc(pg['seguro'], ng['seguro']):>16s} · "
                  f"inseguro {pc(pg['inseguro'], ng['inseguro']):>14s}")
            print(f"   {'':16s} VETO armado a tiro {c['veto_arma']} · "
                  f"DERROCHE {pc(c['derroche'], c['con_desconocido'])} · "
                  f"voz propia {pc(c['voz0'], c['voz1'])} · "
                  f"se enciende: otros {c['n_otros']} vinculo {c['n_vinc']}")

    print("\n== SELLOS O1-O6 ==")
    if "lento" in R and "434" in R:
        tl = R["lento"]["100"][0]; t4 = R["434"]["100"][0]
        nl, n4 = tl["vistos"], t4["vistos"]
        c1 = 100 * tl["neutros"] / nl > 50
        c2 = 100 * tl["positivos"] / nl < 15
        c3 = 100 * t4["negativos"] / n4 > 30
        print(f"  O1 · lento neutros {100 * tl['neutros'] / nl:.1f} % (>50 "
              f"{'si' if c1 else 'NO'}) · positivos "
              f"{100 * tl['positivos'] / nl:.1f} % (<15 {'si' if c2 else 'NO'})"
              f" · 434 negativos {100 * t4['negativos'] / n4:.1f} % (>30 "
              f"{'si' if c3 else 'NO'}) -> "
              f"{'CUMPLE' if (c1 and c2 and c3) else 'FALLA'}")
    for nom in ("s2", "lento"):
        if nom not in B3:
            continue
        print(f"\n  --- {nom} ---")
        c, pg, ng, dec = B3[nom]["otros_k0.1"]
        ps = 100 * pg["seguro"] / max(1, ng["seguro"])
        ok2 = 0.5 <= ps <= 3 and c["veto_arma"] == 0
        print(f"  O2 · k_o=0,1 en seguro {ps:.2f} % (pide 0,5-3) · armado a "
              f"tiro {c['veto_arma']} (pide 0) -> "
              f"{'CUMPLE' if ok2 else 'FALLA'}")
        d05 = B3[nom]["otros_k0.05"][0]
        d20 = B3[nom]["otros_k0.2"][0]
        r05 = 100 * d05["derroche"] / max(1, d05["con_desconocido"])
        r20 = 100 * d20["derroche"] / max(1, d20["con_desconocido"])
        r10 = 100 * c["derroche"] / max(1, c["con_desconocido"])
        ok3 = 2 <= r10 <= 15 and r20 > r05
        print(f"  O3 · derroche k_o 0,05 {r05:.2f} % · 0,1 {r10:.2f} % · "
              f"0,2 {r20:.2f} % (pide 2-15 y 0,2>0,05) -> "
              f"{'CUMPLE' if ok3 else 'FALLA'}")
        cv, pv, nv, _ = B3[nom]["vinc_k0.1"]
        pvv = 100 * cv["cambios"] / max(1, dec)
        print(f"  O5 · vinculo k_s=0,1 cambia {pvv:.2f} % (pide <1) -> "
              f"{'CUMPLE' if pvv < 1 else 'FALLA'}")
        vz = 100 * c["voz0"] / max(1, c["voz1"])
        print(f"  O6 · voz propia {vz:.2f} % (pide >0,3) -> "
              f"{'CUMPLE' if vz > 0.3 else 'FALLA'}")
    print("\n  O4 · (muertes por asiento con conocimiento cero) — ver B1")


if __name__ == "__main__":
    main()

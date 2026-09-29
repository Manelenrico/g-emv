"""[P5-8A] Los contadores y el cotejo de F1 a F7."""
import collections, json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import curiosidad_forma as CF


def pc(a, b):
    return f"{a}/{b} = {100.0 * a / b:.2f} %" if b else f"{a}/0 = —"


def q(v):
    if not v:
        return "—"
    s = sorted(v)
    n = len(s)
    return (f"mediana {st.median(s):.1f} · Q1 {s[n // 4]:.1f} · "
            f"Q3 {s[3 * n // 4]:.1f} · min {s[0]} · max {s[-1]}")


def junta(D, cons):
    S = [o for o in D if o["consigna"] == cons]
    c = collections.Counter()
    for o in S:
        c.update(o["c"])
    keys = ("dists", "areas", "ms_gen", "ms_puerta", "nuevas_proy",
            "nuevas_real")
    ac = {k: [x for o in S for x in o[k]] for k in keys}
    ac["carencia"] = [tuple(x) for o in S for x in o["carencia"]]
    return S, c, ac


def informe(nom, D):
    print(f"\n===== {nom.upper()} · {len(D) // len(CF.CONSIGNAS)} asientos "
          f"por consigna =====")
    R = {}
    for cons in CF.CONSIGNAS:
        S, c, ac = junta(D, cons)
        R[cons] = (c, ac)
        vivos = sum(o["vivos"] for o in S)
        print(f"\n  --- consigna {cons} ---")
        print(f"  tics vivos {vivos:,} · NO dispara {c['no_dispara']:,} · "
              f"ventanas seguras con ignorancia sobre consigna "
              f"{c['ventanas']:,} = {100 * c['ventanas'] / max(1, vivos):.2f} %")
        print(f"  se dispara y NO hay frontera segura: "
              f"{pc(c['sin_frontera'], c['ventanas'])}")
        print(f"  FORMAS GENERADAS: {pc(c['generadas'], c['ventanas'])}")
        ev = c["evaluadas"]
        print(f"  puerta evaluada (muestreo): {ev:,} de {c['generadas']:,} "
              f"generadas")
        print(f"     CON el renglon: pasa {pc(c['pasa_con_ok'], ev)} · "
              f"area {c['pasa_con_area']} · vida {c['pasa_con_vida']}")
        print(f"     SIN el renglon: pasa {pc(c['pasa_sin_ok'], ev)} · "
              f"area {c['pasa_sin_area']} · vida {c['pasa_sin_vida']}")
        print(f"  trayecto: {q(ac['dists'])}")
        print(f"  POR CONSTRUCCION · cruza sombra {c['cruza_sombra']} · "
              f"destino a tiro {c['destino_a_tiro']} (los dos deben ser 0)")
        print(f"  abandonadas por peligro en la ventana: "
              f"{pc(c['abandona_peligro'], c['pasa'])}")
        car = ac["carencia"]
        sube = sum(1 for a, b in car if b > a + 1e-9)
        print(f"  DERROCHE · R-CARENCIA proyectada NO sube en "
              f"{pc(len(car) - sube, len(car))} de las que pasan")
        print(f"  casillas nuevas (NO SELLADO, solo el campo las mide): "
              f"proyectadas mediana "
              f"{st.median(ac['nuevas_proy']) if ac['nuevas_proy'] else '—'} · "
              f"reales del cuerpo mediana "
              f"{st.median(ac['nuevas_real']) if ac['nuevas_real'] else '—'} "
              f"(n={len(ac['nuevas_proy'])})")
        print(f"  coste: generar {st.median(ac['ms_gen']):.3f} ms mediana "
              f"(max {max(ac['ms_gen']):.3f}) · puerta "
              f"{st.median(ac['ms_puerta']):.1f} ms mediana"
              if ac["ms_gen"] else "  coste: sin datos")
    return R


def sellos(R):
    print("\n== SELLOS F1-F7 (sobre el LENTO) ==")
    c5, a5 = R[0.5]
    f1 = 100 * c5["generadas"] / max(1, c5["ventanas"])
    print(f"  F1 · genera en {f1:.2f} % de las ventanas (pide >=50) -> "
          f"{'CUMPLE' if f1 >= 50 else 'FALLA'}")
    ev = c5["evaluadas"]
    f2 = 100 * c5["pasa_con_ok"] / max(1, ev)
    print(f"  F2 · pasa la puerta {f2:.2f} % de las evaluadas (pide >=30) -> "
          f"{'CUMPLE' if f2 >= 30 else 'FALLA'}")
    con, sin = c5["pasa_con_ok"], c5["pasa_sin_ok"]
    f3 = sin < con / 2 if con else False
    print(f"  F3 · sin el renglon pasan {sin} contra {con} con el "
          f"(pide < la mitad) -> {'CUMPLE' if f3 else 'FALLA'}")
    md = st.median(a5["dists"]) if a5["dists"] else None
    f4 = md is not None and 5 <= md <= 20
    print(f"  F4 · trayecto mediano {md} casillas (pide 5-20) -> "
          f"{'CUMPLE' if f4 else 'FALLA'}")
    f5 = c5["cruza_sombra"] == 0 and c5["destino_a_tiro"] == 0
    print(f"  F5 · cruza sombra {c5['cruza_sombra']} · destino a tiro "
          f"{c5['destino_a_tiro']} (piden 0) -> "
          f"{'CUMPLE' if f5 else 'FALLA'}")
    car = a5["carencia"]
    nosube = sum(1 for a, b in car if b <= a + 1e-9)
    f6 = len(car) and 100 * nosube / len(car) >= 90
    print(f"  F6 · la carencia NO sube en "
          f"{pc(nosube, len(car))} (pide >=90 %) -> "
          f"{'CUMPLE' if f6 else 'FALLA'}")
    mg = st.median(a5["ms_gen"]) if a5["ms_gen"] else None
    f7 = mg is not None and mg < 10
    print(f"  F7 · generar una forma {mg:.3f} ms de mediana (pide <10) · "
          f"en seco no hay hilo del consejero -> "
          f"{'CUMPLE' if f7 else 'FALLA'}")


if __name__ == "__main__":
    R = None
    for nom in ("lento", "s2"):
        p = os.path.join(AQUI, f"P58A_{nom}.json")
        if not os.path.exists(p):
            continue
        r = informe(nom, json.load(open(p)))
        if nom == "lento":
            R = r
    if R:
        sellos(R)

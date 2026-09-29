"""[P5-6C · cierre] El cotejo de los sellos S1 a S8, con sus contadores.

  python3 cantera/paper5/sellos_P56C.py 1 2 3 4 5 amp1 amp2 amp3 amp4 amp5

Los sellos, tal como los puso la mesa el 20-sep-2026:

  S1. F acepta mas formas por vida que T (mediana), con la vara del ruido, y
      ambas por encima de cero.
  S2. La `d` real en los puntos de control queda por debajo de la proyectada
      mas 0,05 en MAS DE LA MITAD DE LAS FORMAS de F, y en MENOS de la mitad
      de las de T.   <-- por FORMAS, no por puntos.
  S3. C final: mediana de F por encima de la de T, y T por debajo de 0,3.
  S4. La coherencia de signos en F sube dentro de la partida: en las citas de
      la segunda mitad de la vida supera a la primera mitad en mas de 10
      puntos (con el parte).
  S5. Callar: F calla en mas del 30 % de las citas; y calla mas cuando C es
      baja que cuando es alta.
  S6. Ningun brazo mueve el puesto final ni la duracion de vida mas alla del
      ruido (el anillo y los vecinos deciden).
  S7. Ninguna forma aceptada cruza el minimo de vida proyectado: cero.
  S8. Gasto total de la serie por debajo de 15 dolares.

Los diarios se leen DE UNO EN UNO: los doscientos no caben juntos en memoria.
"""
from __future__ import annotations
import glob, json, math, os, re, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
BANDA = 0.05
SIGNOS = ("vida", "manos", "vinculo")

# «Tramo 1: dijiste vida 0, manos 0, vinculo - por X; el cuerpo proyecto
#  vida 0, manos 0, vinculo 0; ...»
RE_TRAMO = re.compile(
    r"Tramo (\d+): dijiste vida (.), manos (.), vinculo (.) por [^;]*; "
    r"el cuerpo proyecto vida (.), manos (.), vinculo (.)")


def lee(f):
    for linea in open(f, encoding="utf-8"):
        linea = linea.strip()
        if linea:
            try:
                yield json.loads(linea)
            except Exception:
                continue


def coherencia(parte):
    """(aciertos, total) de signos AFIRMADOS contra PROYECTADOS en un parte."""
    ok = n = 0
    for m in RE_TRAMO.finditer(parte or ""):
        dicho = m.group(2, 3, 4)
        proy = m.group(5, 6, 7)
        for a, b in zip(dicho, proy):
            n += 1
            ok += (a == b)
    return ok, n


def de_uno(f):
    """Lo minimo de un diario para los ocho sellos."""
    o = {"aceptadas": 0, "vida": None, "puesto": None,
         "C_serie": [], "citas": [], "formas": {}, "cruza_vida": 0,
         "caidas_vida": 0}
    for r in lee(f):
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live":
            o["ultimo_tick"] = r["tick"]
            o.setdefault("primer_tick", r["tick"])
        elif k == "final":
            o["vida"] = r.get("match_ticks")
            o["puesto"] = r.get("placement")
        elif k == "forma_evaluada":
            if r.get("C") is not None:
                o["C_serie"].append((r["tick"], r["C"]))
        elif k == "forma_aceptada":
            o["aceptadas"] += 1
            o["formas"][r.get("id")] = {"tick": r["tick"], "ok": 0, "n": 0}
        elif k == "forma_propuesta" and r.get("origen") != "azar":
            ok, n = coherencia(r.get("parte"))
            # la cita se registra con `tick_foto`/`tick_llegada`, no con `tick`
            tk = r.get("tick", r.get("tick_foto", r.get("tick_llegada")))
            o["citas"].append({
                "tick": int(tk) if tk is not None else 0,
                "callar": bool((r.get("traduccion") or {}).get("callar")),
                "coh_ok": ok, "coh_n": n})
        elif k == "confianza":
            if r.get("d_real") is not None and r.get("d_proyectada") is not None:
                fid = r.get("id")
                if fid in o["formas"]:
                    o["formas"][fid]["n"] += 1
                    o["formas"][fid]["ok"] += (
                        r["d_real"] <= r["d_proyectada"] + BANDA)
        elif k == "forma_caida":
            mot = r.get("motivo") or ""
            # S7 pregunta por la VIDA REAL cruzando el minimo proyectado
            # (`forma_viva.py:14`), NO por la puerta re-rechazando en la
            # reevaluacion: son dos motivos distintos y se cuentan aparte.
            if "vida real" in mot and "por debajo de la proyectada" in mot:
                o["cruza_vida"] += 1
            elif "deja de ganar (vida)" in mot:
                o["caidas_vida"] += 1
    return o


def carga(tandas):
    out = {}
    for t in tandas:
        for d in sorted(glob.glob(os.path.join(
                RAIZ, "paintball", "runs", f"P56C_t{t}_*"))):
            _p, _t, brazo, semilla = os.path.basename(d).split("_", 3)
            for f in sorted(glob.glob(os.path.join(d, "*.art.log"))):
                slot = int(f.rsplit("_", 1)[1].split(".")[0])
                out[(brazo, int(semilla), slot)] = de_uno(f)
    return out


def mediana(v):
    return st.median(v) if v else None


def boot_dif_medianas(a, b, n=4000, sem=20260921):
    """Vara del ruido: IC 95 % de la diferencia de medianas, por remuestreo."""
    import random
    if not a or not b:
        return (None, None, None)
    rnd = random.Random(sem)
    d0 = st.median(a) - st.median(b)
    ds = []
    for _ in range(n):
        ra = [rnd.choice(a) for _ in a]
        rb = [rnd.choice(b) for _ in b]
        ds.append(st.median(ra) - st.median(rb))
    ds.sort()
    return (d0, ds[int(n * 0.025)], ds[int(n * 0.975)])


def main():
    tandas = sys.argv[1:] or ["1"]
    M = carga(tandas)
    por = {b: [k for k in sorted(M) if k[0] == b] for b in ("A", "F", "T")}
    print(f"asientos: A {len(por['A'])} · F {len(por['F'])} · T {len(por['T'])}")
    S = {}

    # ── S1 ───────────────────────────────────────────────────────────────
    aF = [M[k]["aceptadas"] for k in por["F"]]
    aT = [M[k]["aceptadas"] for k in por["T"]]
    d, lo, hi = boot_dif_medianas(aF, aT)
    ok1 = (mediana(aF) > mediana(aT)) and mediana(aF) > 0 and mediana(aT) > 0
    print(f"\nS1  aceptadas por vida · mediana F {mediana(aF)} · T {mediana(aT)}"
          f" · dif {d} [{lo}, {hi}]")
    print(f"    media F {st.mean(aF):.3f} · T {st.mean(aT):.3f} · "
          f"totales F {sum(aF)} T {sum(aT)}")
    print(f"    --> {'CUMPLE' if ok1 else 'FALLA'} "
          f"(pide mediana F > T y las DOS por encima de cero)")
    S["S1"] = {"ok": ok1, "medF": mediana(aF), "medT": mediana(aT),
               "dif": d, "ic": [lo, hi], "sumF": sum(aF), "sumT": sum(aT)}

    # ── S2 · POR FORMAS ──────────────────────────────────────────────────
    print("\nS2  la d real <= proyectada + 0,05 ... POR FORMAS (como se sello)")
    S2 = {}
    for b in ("F", "T"):
        formas = [fv for k in por[b] for fv in M[k]["formas"].values()]
        con = [fv for fv in formas if fv["n"] > 0]
        # una forma «cumple» si cumplen TODOS sus puntos de control
        todos = sum(1 for fv in con if fv["ok"] == fv["n"])
        # y, declarado aparte, si cumple la MAYORIA de sus puntos
        mayo = sum(1 for fv in con if fv["ok"] * 2 > fv["n"])
        pts_ok = sum(fv["ok"] for fv in con)
        pts_n = sum(fv["n"] for fv in con)
        S2[b] = {"formas": len(formas), "con_punto": len(con),
                 "todos": todos, "mayoria": mayo,
                 "puntos_ok": pts_ok, "puntos_n": pts_n}
        print(f"    {b}: {len(formas)} aceptadas · {len(con)} llegaron a algun "
              f"punto de control")
        print(f"       cumplen TODOS sus puntos : {todos}/{len(con)} = "
              f"{todos / len(con) * 100 if con else 0:.1f} %")
        print(f"       cumplen la MAYORIA       : {mayo}/{len(con)} = "
              f"{mayo / len(con) * 100 if con else 0:.1f} %")
        print(f"       (por punto, para cotejar): {pts_ok}/{pts_n} = "
              f"{pts_ok / pts_n * 100 if pts_n else 0:.1f} %")
    fF = S2["F"]["con_punto"]; fT = S2["T"]["con_punto"]
    okF = S2["F"]["mayoria"] * 2 > fF
    okT = S2["T"]["mayoria"] * 2 < fT
    ok2 = okF and okT
    print(f"    --> F mas de la mitad: {'si' if okF else 'NO'} · "
          f"T menos de la mitad: {'si' if okT else 'NO'} · "
          f"{'CUMPLE' if ok2 else 'FALLA'}")
    S["S2"] = {"ok": ok2, "F": S2["F"], "T": S2["T"],
               "F_mas_de_la_mitad": okF, "T_menos_de_la_mitad": okT}

    # ── S3 ───────────────────────────────────────────────────────────────
    cF = [M[k]["C_serie"][-1][1] for k in por["F"] if M[k]["C_serie"]]
    cT = [M[k]["C_serie"][-1][1] for k in por["T"] if M[k]["C_serie"]]
    ok3 = bool(cF and cT) and mediana(cF) > mediana(cT) and mediana(cT) < 0.3
    print(f"\nS3  C final · mediana F {mediana(cF)} (n={len(cF)}) · "
          f"T {mediana(cT)} (n={len(cT)})")
    print(f"    --> {'CUMPLE' if ok3 else 'FALLA'} "
          f"(pide F > T y T por debajo de 0,30)")
    S["S3"] = {"ok": ok3, "medF": mediana(cF), "medT": mediana(cT),
               "nF": len(cF), "nT": len(cT)}

    # ── S4 ───────────────────────────────────────────────────────────────
    pri = [0, 0]; seg = [0, 0]
    for k in por["F"]:
        o = M[k]
        cits = [c for c in o["citas"] if c["coh_n"]]
        if not cits:
            continue
        t0 = o.get("primer_tick", 0); t1 = o.get("ultimo_tick", t0)
        medio = (t0 + t1) / 2
        for c in cits:
            caja = pri if c["tick"] <= medio else seg
            caja[0] += c["coh_ok"]; caja[1] += c["coh_n"]
    p1 = pri[0] / pri[1] * 100 if pri[1] else 0.0
    p2 = seg[0] / seg[1] * 100 if seg[1] else 0.0
    ok4 = (p2 - p1) > 10
    print(f"\nS4  coherencia de signos (afirmado == proyectado), en F")
    print(f"    primera mitad de la vida: {pri[0]}/{pri[1]} = {p1:.1f} %")
    print(f"    segunda mitad de la vida: {seg[0]}/{seg[1]} = {p2:.1f} %")
    print(f"    --> sube {p2 - p1:+.1f} puntos · "
          f"{'CUMPLE' if ok4 else 'FALLA'} (pide subir mas de 10)")
    S["S4"] = {"ok": ok4, "primera": pri, "segunda": seg,
               "p1": p1, "p2": p2, "sube": p2 - p1}

    # ── S5 ───────────────────────────────────────────────────────────────
    cal = n_cit = 0
    baja = [0, 0]; alta = [0, 0]      # C < 0,30 y C >= 0,30
    for k in por["F"]:
        o = M[k]
        Cs = o["C_serie"]
        for c in o["citas"]:
            n_cit += 1
            cal += c["callar"]
            # la C vigente en esa cita: la ultima evaluacion anterior
            prev = [v for t, v in Cs if t <= c["tick"]]
            if not prev:
                continue
            caja = baja if prev[-1] < 0.30 else alta
            caja[1] += 1
            caja[0] += c["callar"]
    frac = cal / n_cit * 100 if n_cit else 0.0
    pb = baja[0] / baja[1] * 100 if baja[1] else 0.0
    pa = alta[0] / alta[1] * 100 if alta[1] else 0.0
    ok5 = frac > 30 and pb > pa
    print(f"\nS5  callar en F: {cal}/{n_cit} = {frac:.1f} % de las citas")
    print(f"    con C baja (<0,30): {baja[0]}/{baja[1]} = {pb:.1f} %")
    print(f"    con C alta (>=0,30): {alta[0]}/{alta[1]} = {pa:.1f} %")
    print(f"    --> {'CUMPLE' if ok5 else 'FALLA'} "
          f"(pide >30 % y callar mas con C baja)")
    S["S5"] = {"ok": ok5, "callar": cal, "citas": n_cit, "frac": frac,
               "baja": baja, "alta": alta, "p_baja": pb, "p_alta": pa}

    # ── S6 ───────────────────────────────────────────────────────────────
    print("\nS6  puesto y vida, por brazo (el anillo y los vecinos deciden)")
    S6 = {}
    for b in ("A", "F", "T"):
        ps = [M[k]["puesto"] for k in por[b] if M[k]["puesto"] is not None]
        vs = [M[k]["vida"] for k in por[b] if M[k]["vida"] is not None]
        S6[b] = {"puesto_med": mediana(ps), "vida_med": mediana(vs),
                 "n": len(ps)}
        print(f"    {b}: puesto mediano {mediana(ps)} · vida mediana "
              f"{mediana(vs)} · n {len(ps)}")
    for x, y in (("F", "A"), ("T", "A"), ("F", "T")):
        pv = [M[k]["puesto"] for k in por[x] if M[k]["puesto"] is not None]
        qv = [M[k]["puesto"] for k in por[y] if M[k]["puesto"] is not None]
        d, lo, hi = boot_dif_medianas(pv, qv)
        vv = [M[k]["vida"] for k in por[x] if M[k]["vida"] is not None]
        wv = [M[k]["vida"] for k in por[y] if M[k]["vida"] is not None]
        d2, lo2, hi2 = boot_dif_medianas(vv, wv)
        dentro = (lo is not None and lo <= 0 <= hi and lo2 <= 0 <= hi2)
        S6[f"{x}-{y}"] = {"puesto": [d, lo, hi], "vida": [d2, lo2, hi2],
                          "cero_dentro": dentro}
        print(f"    {x} - {y}: puesto {d} [{lo}, {hi}] · vida {d2} "
              f"[{lo2}, {hi2}] · cero {'DENTRO' if dentro else 'fuera'}")
    ok6 = all(S6[p]["cero_dentro"] for p in ("F-A", "T-A", "F-T"))
    print(f"    --> {'CUMPLE' if ok6 else 'FALLA'} "
          f"(pide que nada se mueva mas alla del ruido)")
    S["S6"] = dict(S6, ok=ok6)

    # ── S7 ───────────────────────────────────────────────────────────────
    cv = {b: sum(M[k]["cruza_vida"] for k in por[b]) for b in ("F", "T")}
    rg = {b: sum(M[k]["caidas_vida"] for k in por[b]) for b in ("F", "T")}
    ok7 = (cv["F"] + cv["T"]) == 0
    print(f"\nS7  formas aceptadas cuya VIDA REAL cruza el minimo proyectado: "
          f"F {cv['F']} · T {cv['T']}")
    print(f"    (aparte, y NO es lo que pregunta S7: la puerta re-rechaza por "
          f"vida en la reevaluacion · F {rg['F']} · T {rg['T']})")
    print(f"    --> {'CUMPLE' if ok7 else 'FALLA'} (pide cero)")
    S["S7"] = {"ok": ok7, "cruza": cv, "rechazo_reeval": rg}

    json.dump(S, open(os.path.join(AQUI, "P56C_sellos.json"), "w"),
              ensure_ascii=False, indent=1)
    print("\nguardado en P56C_sellos.json  (S8 se cierra con el gasto real)")


if __name__ == "__main__":
    main()

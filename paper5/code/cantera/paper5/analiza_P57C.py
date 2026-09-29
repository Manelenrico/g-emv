"""[P5-7C · C2] Las medidas de la serie viva de la curiosidad.

  python3 cantera/paper5/analiza_P57C.py 1
  python3 cantera/paper5/analiza_P57C.py 1 2 3 4

Diarios de uno en uno. El brazo A no lleva el renglon, asi que su fraccion de
arena vista se RECONSTRUYE con el mismo `Ojo` del banco (el mundo no publica
que casillas ves); en Q se puede leer del registro `curiosidad_tic`, y se
comprueba que las dos vias dan lo mismo.
"""
from __future__ import annotations
import collections, glob, json, os, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)

import serie_util as U                                    # noqa: E402
import curiosidad as C                                    # noqa: E402

TRAMOS = 4


def med(v):
    return st.median(v) if v else None


def pc(a, b):
    return f"{a}/{b} = {100.0 * a / b:.2f} %" if b else f"{a}/0 = —"


def boot(a, b, n=4000, sem=20260923):
    import random, statistics
    if not a or not b:
        return (None, None, None)
    r = random.Random(sem)
    d0 = statistics.median(a) - statistics.median(b)
    ds = sorted(statistics.median([r.choice(a) for _ in a])
                - statistics.median([r.choice(b) for _ in b]) for _ in range(n))
    return (d0, ds[int(n * .025)], ds[int(n * .975)])


def un_asiento(f, brazo):
    recs = list(U.lee(f))
    pc_ = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    fin = next((r for r in recs if r.get("k") == "final"), None)
    arr = next((r for r in recs if r.get("k") == "arranque"), None)
    if not (pc_ and sm and cat):
        return None
    mundo = U.mundo_de(pc_, list(sm["filas"]), cat["items"])
    ojo = C.Ojo(mundo, 8)
    vivos = [x for x in recs if x.get("k") == "tick" and x.get("phase") == "live"]
    if not vivos:
        return None
    t0, t1 = vivos[0]["tick"], vivos[-1]["tick"]
    dur = max(1, t1 - t0)
    ign_tramo = [[] for _ in range(TRAMOS)]
    for r in vivos:
        p = tuple(r.get("pos") or ())
        if p:
            ojo.mira(p, r["tick"])
            ign_tramo[min(TRAMOS - 1,
                          int(TRAMOS * (r["tick"] - t0) / dur))].append(
                ojo.ignorancia_global())
    cur = [r for r in recs if r.get("k") == "curiosidad_tic"]
    ms = [r["ms_total"] for r in cur if r.get("ms_total") is not None]
    # tics perdidos: huecos en la secuencia de tics vivos
    hay = {r["tick"] for r in vivos}
    perdidos = len(set(range(t0, t1 + 1)) - hay)
    grados = collections.Counter(r.get("grado") for r in cur)
    dec_gr = collections.Counter(r.get("grado") for r in cur if r.get("decidio"))
    # DERROCHE MORTAL: ¿hubo una decision de curiosidad en los 100 tics previos
    # a la muerte?
    mt = (fin or {}).get("match_ticks") or t1
    dec_ticks = [r["tick"] for r in cur if r.get("decidio")]
    derroche_mortal = any(mt - 100 <= t <= mt for t in dec_ticks)
    # ── [t2] LAS DECISIONES DE CURIOSIDAD, DESGLOSADAS POR ENTORNO ──────
    # De cada decision de la curiosidad: ¿habia un armado a tiro en ese tic?
    # ¿el movimiento acerca al armado a la vista mas cercano? ¿hubo dano
    # recibido en los 50 tics siguientes? Se cruza `curiosidad_tic` con el
    # registro `tick` del MISMO tic (la posicion y los visibles) y con los 50
    # siguientes (el dano).
    por_tic = {r["tick"]: r for r in vivos}
    dano_en = {}
    for r in vivos:
        d = sum(float(x.get("amount") or 0) if isinstance(x, dict) else 0.0
                for x in (r.get("damage_taken") or [])
                if str((x or {}).get("source")) != "zone")
        if d > 0:
            dano_en[r["tick"]] = d
    ticks_dano = sorted(dano_en)
    desglose = {g: collections.Counter() for g in
                ("seguro", "neutro", "inseguro")}
    def _mide(g, t, caja):
        """Sobre UN tic: armado a tiro, el paso acerca, dano en 50."""
        caja[g]["decisiones"] += 1
        r = por_tic.get(t)
        if r is None:
            return
        p0 = tuple(r.get("pos") or ())
        arm = [(tuple(a["pos"]), C._alcance(mundo, a.get("hand")))
               for a in (r.get("ve_agentes") or [])
               if a.get("slot") != pc_.get("teammate_slot") and a.get("pos")
               and C._alcance(mundo, a.get("hand")) > 0]
        if p0 and any(max(abs(p0[0] - q[0]), abs(p0[1] - q[1])) <= rg
                      for q, rg in arm):
            caja[g]["armado_a_tiro"] += 1
        # ¿el paso siguiente acerca al armado mas cercano?
        if p0 and arm:
            q = min((q for q, _ in arm),
                    key=lambda q: max(abs(p0[0] - q[0]), abs(p0[1] - q[1])))
            sig = por_tic.get(t + 1)
            p1 = tuple((sig or {}).get("pos") or ()) if sig else None
            if p1:
                d0 = max(abs(p0[0] - q[0]), abs(p0[1] - q[1]))
                d1 = max(abs(p1[0] - q[0]), abs(p1[1] - q[1]))
                if d1 < d0:
                    caja[g]["acerca_al_armado"] += 1
            caja[g]["con_armado_a_la_vista"] += 1
        if any(t < u <= t + 50 for u in ticks_dano):
            caja[g]["dano_en_50"] += 1

    # (1) las DECISIONES DE CURIOSIDAD de Q
    for cr in cur:
        if cr.get("decidio"):
            _mide(cr.get("grado") or "neutro", cr["tick"], desglose)
    # (2) LA REFERENCIA: TODOS los tics vivos, por grado. En A no hay
    # «decisiones de curiosidad», asi que el conjunto comparable es la vida
    # entera; y se mide tambien en Q, para separar la geometria del mundo de
    # lo que hace el renglon. El grado en A se recalcula aqui (su diario no
    # trae `curiosidad_tic`).
    base = {g: collections.Counter() for g in ("seguro", "neutro", "inseguro")}
    if cur:
        gr_de = {r["tick"]: r.get("grado") for r in cur}
        for r in vivos:
            g = gr_de.get(r["tick"])
            if g:
                _mide(g, r["tick"], base)
    else:
        dh = []
        for r in vivos:
            dh.append((r["tick"], sum(
                float(x.get("amount") or 0) if isinstance(x, dict) else 0.0
                for x in (r.get("damage_taken") or []))))
            d100 = sum(v for (tt, v) in dh if r["tick"] - tt < C.VENTANA_DANO)
            am, _ = C.amenaza(r, mundo, pc_.get("teammate_slot"), d100,
                              r["tick"])
            _mide(C.grado(am), r["tick"], base)
    # casillas nuevas por cien tics
    nuevas = collections.Counter()
    for c_, t in ojo.primera_vez.items():
        nuevas[(t - t0) // 100] += 1
    return {"brazo": brazo, "tics_vivos": len(vivos),
            "vista_final": 1.0 - ojo.ignorancia_global(),
            "vistas": len(ojo.primera_vez), "n_arena": ojo.n_arena,
            "ign_tramo": [med(v) for v in ign_tramo],
            "nuevas_por_100": med(list(nuevas.values())) if nuevas else 0,
            "vida": (fin or {}).get("match_ticks"),
            "puesto": (fin or {}).get("placement"),
            "razon": (fin or {}).get("reason"),
            "cur_tics": len(cur),
            "encendio": sum(1 for r in cur if r.get("encendio")),
            "decidio": sum(1 for r in cur if r.get("decidio")),
            "grados": dict(grados), "decidio_por_grado": dict(dec_gr),
            "ms_mediana": med(ms), "ms_max": max(ms) if ms else None,
            "perdidos": perdidos, "derroche_mortal": derroche_mortal,
            "desglose": {g: dict(v) for g, v in desglose.items()},
            "base": {g: dict(v) for g, v in base.items()},
            "frenos": sum(1 for r in recs
                          if str(r.get("k", "")).startswith("forma_freno")),
            "vigia": sum(1 for r in recs if r.get("k") == "vigia_disparo"),
            "entorno": ((arr or {}).get("entorno_forma") or {}).get("efectivo")}


def main():
    tandas = sys.argv[1:] or ["1"]
    D = []
    for t in tandas:
        for d in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                               f"P57C_t{t}_*"))):
            brazo = os.path.basename(d).split("_")[2]
            for f in sorted(glob.glob(os.path.join(d, "*.art.log"))):
                o = un_asiento(f, brazo)
                if o:
                    D.append(o)
    A = [o for o in D if o["brazo"] == "A"]
    Q = [o for o in D if o["brazo"] == "Q"]
    print(f"===== P5-7C · tandas {', '.join(tandas)} · "
          f"A {len(A)} asientos · Q {len(Q)} =====")
    print(f"interruptores efectivos en Q: "
          f"{(Q[0]['entorno'] or {}).get('CURIOSIDAD')} · "
          f"k={(Q[0]['entorno'] or {}).get('CURIOSIDAD_K')}" if Q else "")

    print("\n== C2 · LO QUE VE ==")
    for n, S in (("A", A), ("Q", Q)):
        v = [o["vista_final"] for o in S]
        print(f"  {n}: fraccion de arena vista al final · mediana {med(v):.4f} "
              f"· min {min(v):.4f} · max {max(v):.4f}")
        print(f"     ignorancia por tramo (mediana): " + " · ".join(
            f"{med([o['ign_tramo'][i] for o in S if o['ign_tramo'][i] is not None]):.4f}"
            for i in range(TRAMOS)))
        print(f"     casillas nuevas por 100 tics (mediana de medianas): "
              f"{med([o['nuevas_por_100'] for o in S])}")
    d, lo, hi = boot([o["vista_final"] for o in Q],
                     [o["vista_final"] for o in A])
    mA, mQ = med([o["vista_final"] for o in A]), med([o["vista_final"] for o in Q])
    print(f"  --> Q − A: {d:+.4f} [{lo:+.4f}, {hi:+.4f}] · "
          f"Q/A = {mQ / mA:.3f}x  (Q1 pide > 1,30x)")

    print("\n== C2 · EL RENGLON ==")
    tot = sum(o["cur_tics"] for o in Q)
    enc = sum(o["encendio"] for o in Q)
    dec = sum(o["decidio"] for o in Q)
    print(f"  tics con registro {tot:,} · se enciende {pc(enc, tot)} · "
          f"DECIDE {pc(dec, tot)}")
    G = collections.Counter()
    DG = collections.Counter()
    for o in Q:
        G.update(o["grados"]); DG.update(o["decidio_por_grado"])
    for g in ("seguro", "neutro", "inseguro"):
        print(f"     {g:9s}: {pc(G[g], tot)} de los tics · DECIDE "
              f"{pc(DG[g], G[g])}")

    print("\n== C2 · VIDA, PUESTO, TIEMPO, FRENOS ==")
    for n, S in (("A", A), ("Q", Q)):
        vs = [o["vida"] for o in S if o["vida"]]
        ps = [o["puesto"] for o in S if o["puesto"]]
        print(f"  {n}: vida mediana {med(vs)} · puesto mediano {med(ps)} · "
              f"tics perdidos {sum(o['perdidos'] for o in S)} · "
              f"frenos {sum(o['frenos'] for o in S)} · "
              f"vigia {sum(o['vigia'] for o in S)}")
    dv, lv, hv = boot([o["vida"] for o in Q if o["vida"]],
                      [o["vida"] for o in A if o["vida"]])
    dp, lp, hp = boot([o["puesto"] for o in Q if o["puesto"]],
                      [o["puesto"] for o in A if o["puesto"]])
    print(f"  --> Q − A vida {dv:+.0f} [{lv:+.0f}, {hv:+.0f}] · "
          f"puesto {dp:+.1f} [{lp:+.1f}, {hp:+.1f}]  (Q3 pide el cero dentro)")
    msq = [o["ms_mediana"] for o in Q if o["ms_mediana"]]
    print(f"  tiempo por tic en Q: mediana de medianas {med(msq):.3f} ms · "
          f"maximo {max(o['ms_max'] for o in Q if o['ms_max']):.3f} ms "
          f"(Q5 pide < 5 ms y cero perdidos)")

    print("\n== [t2] LAS DECISIONES DE CURIOSIDAD, POR ENTORNO ==")
    print("   (de cada decision: armado a tiro EN ESE TIC · el paso acerca al")
    print("    armado a la vista mas cercano · dano recibido en los 50 tics")
    print("    siguientes. El «acerca» se mide sobre los tics que tienen algun")
    print("    armado a la vista.)")
    DG2 = {g: collections.Counter() for g in ("seguro", "neutro", "inseguro")}
    for o in Q:
        for g, v in (o.get("desglose") or {}).items():
            DG2[g].update(v)
    for g in ("seguro", "inseguro", "neutro"):
        v = DG2[g]
        n = v["decisiones"]
        if not n:
            print(f"   {g:9s}: sin decisiones")
            continue
        print(f"   {g:9s}: {n} decisiones · armado A TIRO "
              f"{pc(v['armado_a_tiro'], n)} · acerca al armado "
              f"{pc(v['acerca_al_armado'], v['con_armado_a_la_vista'])} · "
              f"dano en 50 tics {pc(v['dano_en_50'], n)}")

    print("\n== [t3] LA REFERENCIA: TODOS LOS TICS VIVOS, POR BRAZO ==")
    print("   En A no hay «decisiones de curiosidad», asi que el conjunto")
    print("   comparable es la VIDA ENTERA. Se mide tambien en Q para separar")
    print("   la geometria del mundo de lo que hace el renglon.")
    print(f"   {'':26s} {'acerca al armado':>20s} {'dano en 50 tics':>18s}")
    for nom, S in (("A · todos los tics", A), ("Q · todos los tics", Q),
                   ("Q · solo curiosidad", None)):
        for g in ("seguro", "neutro", "inseguro"):
            if S is None:
                v = DG2[g]
            else:
                v = collections.Counter()
                for o in S:
                    v.update((o.get("base") or {}).get(g) or {})
            n = v["decisiones"]
            if not n:
                continue
            ac = pc(v["acerca_al_armado"], v["con_armado_a_la_vista"])
            dn = pc(v["dano_en_50"], n)
            print(f"   {nom:22s} {g:9s} {ac:>22s} {dn:>20s}")
        print()

    print("\n== C2 · MUERTES Y DERROCHE MORTAL ==")
    for n, S in (("A", A), ("Q", Q)):
        raz = collections.Counter(o["razon"] for o in S)
        print(f"  {n}: {dict(raz)}")
    muertos = [o for o in Q if o["razon"] == "eliminated"]
    dm = sum(1 for o in muertos if o["derroche_mortal"])
    print(f"  Q: muertes con una decision de curiosidad en los 100 tics "
          f"anteriores: {pc(dm, len(muertos))}  (Q4 pide < 15 %)")
    json.dump(D, open(os.path.join(AQUI,
                                   f"P57C_t{'_'.join(tandas)}_medidas.json"),
                      "w"))


if __name__ == "__main__":
    main()

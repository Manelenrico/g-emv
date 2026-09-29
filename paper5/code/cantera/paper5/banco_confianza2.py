"""[P5-4B] La confianza se paga por LO NUEVO, y lo dicho puede ser AUSENCIA.\n\n--- cabecera de P5-4A ---

Sobre el banco de P5-3H: regla E1+G2, margen 0,02, comparador en ventana, sin
deepcopy. Las cinco filas de rivales se evaluan con la posicion DICHA y se
mezclan con el piso segun C (`confianza.mezcla`).
"""
from __future__ import annotations
import collections, copy, glob, json, os, random, sys, time
sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV, TOL
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B, banco_forma3 as BF, forma as F, proyeccion as P
import alcance_g as AL, confianza as CF
import banco_forma3 as BFm

RIV = set(AL.FILAS_RIVAL)
HER = set(AL.FILAS_HERMANO)


def grupos_de(ow, mundo, memw, w, herm, dia_h, dia_yo, pisos, riv_w, filas_m,
              rnd, C, e0, tics, tramos=None):
    """Las filas, por grupo, en el punto pedido (con la mezcla de C)."""
    tr = tramos or [{"destino": None, "intencion": "esperar"}]
    e = F.copia_estado(e0)
    for tic in tics:
        e = P.proyectar_rapido(e, {"destino": tr[0].get("destino"),
                                   "coger": False, "usar": None},
                               tic - e["tick"], mundo, {})
    o = F.foto_rapida(ow, e, mundo, tics[-1], [])
    o, m = AL.pon_hermano(o, memw, herm, (dia_h or {}).get(tics[-1]),
                          tuple(e["pos"]), mundo)
    dicho = CF.dice2(CONS, riv_w, tics[-1], dia_yo, dia_h, herm, filas_m, rnd,
                     P_AUS)
    o = CF.obs_con_dicho2(o, dicho, herm)
    try:
        Fd = CF.mezcla(V42.filas(o, mundo, m, tics[-1]) or {}, pisos, C)
    except Exception:
        return {}
    g = {"rivales": 0.0, "hermano": 0.0, "propias": 0.0}
    base = F.d_con_pisos(Fd)
    for nom in V42.REPARTO:
        mix = dict(Fd); mix[nom] = 0.0
        ap = base - F.d_con_pisos(mix)
        g["rivales" if nom in RIV else
          ("hermano" if nom in HER else "propias")] += ap
    return g

CONS = os.environ.get("P54A", "nadie")
P_AUS = 0.2173   # frecuencia de ausencia del oraculo, MEDIDA (1231/5665)
HOR, MARGEN, DESDE, CADA = 100, 0.02, 300, 50
CES = ("lin", "umb07", "umb05", "umb09", "lin_b", "umb07_b")
LLAVES = ("ahora", "despues", "azarp")
CAJAS = ("aceptada", "coincide", "rechazada", "rechazada_vida",
         "rechazada_area", "vetada", "caducada")
PROG = open(os.path.join(AQUI, f"P54B_{CONS}_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


def curva_C(e0, ow, tramos, mundo, mem, suelo, tics, herm, dia_h, dia_yo,
            pisos, filas_mapa, rnd, Cs, rivales_w, aprende=None):
    """Una curva por cada C. Devuelve {C: curva} y lo dicho por punto."""
    e = F.copia_estado(e0)
    suelo_act = dict(suelo)
    out = {c: [] for c in Cs}
    dichos = []
    for i, tic in enumerate(tics):
        K = tic - e["tick"]
        if K < 0:
            continue
        tr = tramos[i] if i < len(tramos) else {"destino": None,
                                                "intencion": "esperar"}
        e = P.proyectar_rapido(e, {"destino": tr.get("destino"),
                                   "coger": tr.get("intencion") == "coger",
                                   "usar": tr.get("item")
                                   if tr.get("intencion") == "usar" else None},
                               K, mundo, suelo_act)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = F.foto_rapida(ow, e, mundo, tic, list(suelo_act.values()))
        o, m = AL.pon_hermano(o, mem, herm, (dia_h or {}).get(tic),
                              tuple(e["pos"]), mundo)
        dicho = CF.dice2(CONS, rivales_w, tic, dia_yo, dia_h, herm,
                         filas_mapa, rnd, P_AUS)
        dichos.append((tic, dicho))
        o2 = CF.obs_con_dicho2(o, dicho, herm)
        try:
            Fd = V42.filas(o2, mundo, m, tic) or {}
        except Exception:
            Fd = {}
        for c in Cs:
            Cv = Cs[c]
            out[c].append({"tic": tic, "d": F.d_con_pisos(CF.mezcla(Fd, pisos, Cv)),
                           "vida": e["hp"], "W": e.get("W"),
                           "pos": tuple(e["pos"])})
    return out, dichos


def mejor_C(e0, ow, base, tics, mundo, mem, suelo, t0, herm, dia_h, dia_yo,
            pisos, filas_mapa, rnd, Cs, rivales_w):
    """La mejor curva propia POR CADA C (el cuerpo imagina lo suyo con la
    misma informacion)."""
    hor = tics[-1] - t0
    curvas = {c: [] for c in Cs}
    for n, rec in base:
        tr = F.forma_de_candidato(n, rec, hor, e0["pos"])
        cs, _d = curva_C(e0, ow, tr, mundo, mem, suelo, tics, herm, dia_h,
                         dia_yo, pisos, filas_mapa, rnd, Cs, rivales_w)
        for c in Cs:
            flojo = any(p["vida"] is not None and p["vida"] < F.VIDA_MIN
                        for p in cs[c])
            curvas[c].append((F.coste(cs[c], t0), n, cs[c], flojo))
    out = {}
    for c in Cs:
        ok = [x for x in curvas[c] if not x[3]]
        cand = ok or curvas[c]
        k, n, cu, _f = min(cand, key=lambda x: x[0])
        out[c] = (cu, n)
    return out


def main():
    D.A = V42
    U.pon(False)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
    rnd_az = random.Random(20260919)
    rnd_m = random.Random(20260920)
    avisa(f"consejero {CONS} · diarios {len(idx)} · semilla {B.SEMILLA}")

    cajas = {c: {k: collections.Counter() for k in LLAVES} for c in CES}
    trayec = collections.defaultdict(list)     # tramo -> [C]
    finales, compro = [], collections.Counter()
    dano = {c: collections.Counter() for c in CES}
    recup = collections.Counter()
    ms = []
    n_esc = 0

    for orden, i in enumerate(idx, 1):
        f = fs[i]
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            continue
        B.pon_v42(B.interruptores(recs))
        filas_m, items = list(sm["filas"]), cat["items"]
        mundo = U.mundo_de(pc, filas_m, items)
        slot, herm = pc.get("slot"), pc.get("teammate_slot")
        otro = f.replace(f"policy_agent_{slot}", f"policy_agent_{herm}")
        dia_h = ({rr["tick"]: rr for rr in U.lee(otro)
                  if rr.get("k") == "tick" and rr.get("phase") == "live"}
                 if os.path.exists(otro) else None)
        tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
        dia_yo = {t: r for t, r in tk.items() if r.get("phase") == "live"}
        vivos = [r for r in recs if r.get("k") == "tick"
                 and r.get("phase") == "live"]
        vivo = {r["tick"] for r in vivos}
        pos_t = {r["tick"]: tuple(r.get("pos") or ()) for r in vivos}
        mri = {r["tick"]: (r.get("move_ready_in") or 0) for r in vivos}
        d_t = {}
        for r in vivos:
            R = r.get("RADIOGRAFIA") or {}
            c = (R.get("candidatos") or {}).get(R.get("elegido"))
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        esc = [r["tick"] for r in vivos
               if r["tick"] >= DESDE and r["tick"] % CADA == 0]
        nec = set(esc) | {u for t in esc for u in range(t, t + HOR + 1)
                          if u in vivo and mri.get(u, 1) == 0}
        ctxs = {}
        mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
        for r in [x for x in recs if x.get("k") == "tick"]:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            pre = copy.deepcopy(mem)
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if (r.get("intencion") or {}).get("do") == "attack" \
                    or _el.startswith("atacar"):
                mem.ultimo_ataque = t
            if t in nec:
                ctxs[t] = (r, o, pre, copy.deepcopy(blo))
        Cd, Cd2 = 0.0, 0.0           # [B2] empieza en CERO: nada entra sin ganarselo
        for t in sorted(esc):
            w = next((u for u in range(t, t + HOR + 1)
                      if u in vivo and mri.get(u, 1) == 0), None)
            if w is None or w not in ctxs:
                continue
            rw, ow, memw, blw = ctxs[w]
            ew = P.estado_de(rw)
            suelow = {tuple(it["pos"]): it for it in (rw.get("ve_items") or [])
                      if it.get("pos")}
            pisos = F.pisos_rival(ow, mundo, memw, w)
            riv_w = {a.get("slot"): tuple(a.get("pos") or ())
                     for a in ((ow.get("visible") or {}).get("agents") or [])
                     if a.get("pos") and a.get("slot") != herm}
            n_esc += 1
            Cs = {"lin": Cd,
                  "umb07": 1.0 if Cd >= 0.7 else 0.0,
                  "umb05": 1.0 if Cd >= 0.5 else 0.0,
                  "umb09": 1.0 if Cd >= 0.9 else 0.0,
                  "lin_b": Cd2,
                  "umb07_b": 1.0 if Cd2 >= 0.7 else 0.0}
            # ---- O-ahora: coincide por definicion
            for c in CES:
                cajas[c]["ahora"]["coincide"] += 1
            # ---- las dos llaves
            t2 = t + HOR
            if not (t2 in vivo and d_t.get(t2) is not None
                    and d_t.get(t) is not None and d_t[t2] < d_t[t]):
                continue
            tr_d = BF.tramos_reales(tk, t, HOR)
            pasos = F.cheb(pos_t[t], tr_d[-1]["destino"])
            z = BF.casilla_a(filas_m, pos_t[t], max(1, pasos), rnd_az)
            trabajos = [("despues", tr_d)]
            if z:
                trabajos.append(("azarp", [
                    {"destino": tuple(z), "intencion": "ir"},
                    {"destino": None, "intencion": "esperar",
                     "esperar": max(0, HOR - F.cheb(pos_t[t], z) * P.PASO_TICS)}]))
            _t0 = time.perf_counter()
            for k, tramos in trabajos:
                tics = [x[0] for x in F.puntos_de_control(ew, tramos)]
                if not tics:
                    continue
                cf, dichos = curva_C(ew, ow, tramos, mundo, memw, suelow, tics,
                                     herm, dia_h, dia_yo, pisos, filas_m,
                                     rnd_m, Cs, riv_w)
                prop = mejor_C(ew, ow, list(D.candidatos(
                    ow, mundo, copy.deepcopy(memw), w, copy.deepcopy(blw))),
                    tics, mundo, memw, suelow, w, herm, dia_h, dia_yo, pisos,
                    filas_m, rnd_m, Cs, riv_w)
                for c in CES:
                    ver, ar, dt = F.juzga_margen(cf[c], prop[c][0], w,
                                                 margen=MARGEN)
                    if ver != "ok":
                        cajas[c][k]["rechazada_" + ver] += 1
                        continue
                    # [A3] LA MESA: la forma aceptada compite como candidato
                    d0 = tramos[0].get("destino")
                    if d0 is None:
                        cajas[c][k]["coincide"] += 1
                        continue
                    caja, info = BFm.compite(
                        f"_FM_ir_{d0[0]}_{d0[1]}", BFm.a_ir(d0, ow, memw),
                        ar, ow, mundo, memw, blw, w, "")
                    cajas[c][k][caja] += 1
                    # [A5] el dano: aceptada y acabo PEOR que seguir solo
                    if caja == "aceptada":
                        dano[c][k + ":aceptadas"] += 1
                        prop_d = prop[c][0][-1]["d"]
                        if (cf[c][-1]["d"] is not None and prop_d is not None
                                and d_t.get(t2) is not None
                                and d_t.get(t) is not None
                                and d_t[t2] >= d_t[t]):
                            dano[c][k + ":peor"] += 1
                    # [A3] la recuperacion por grupo, solo con la C fija de 1
                    if c == "umb07" and k == "despues":
                        fa = grupos_de(ow, mundo, memw, w, herm, dia_h, dia_yo,
                                       pisos, riv_w, filas_m, rnd_m, 1.0,
                                       ew, [tics[0]])
                        fb = grupos_de(ow, mundo, memw, w, herm, dia_h, dia_yo,
                                       pisos, riv_w, filas_m, rnd_m, 1.0,
                                       ew, [tics[-1]], tramos)
                        for g in ("rivales", "hermano", "propias"):
                            recup[g] += fa.get(g, 0.0) - fb.get(g, 0.0)
                # la confianza se actualiza UNA vez por escena, con el primer
                # punto de control que llega a comprobarse
                if k == "despues":
                    for tic, dicho in dichos:
                        Cd, ok, mal, nnt = CF.actualiza_C2(
                            Cd, dicho, riv_w, dia_yo, dia_h, tic, herm, mundo)
                        Cd2, _o, _m, _n = CF.actualiza_C2(
                            Cd2, dicho, riv_w, dia_yo, dia_h, tic, herm, mundo,
                            0.05, 0.10)
                        compro["dichos"] += len(dicho)
                        compro["no triviales"] += nnt
                        compro["ausencias"] += sum(
                            1 for v in dicho.values() if v == CF.AUSENTE)
                        compro["comprobados"] += ok + mal
                        compro["aciertos"] += ok
                        compro["fallos"] += mal
            ms.append((time.perf_counter() - _t0) * 1000.0)
            tramo = ("0-500" if t < 500 else "500-1500" if t < 1500 else ">1500")
            trayec[tramo].append(Cd)
        finales.append(Cd)
        avisa(f"[{orden}/40] {os.path.basename(f)[:38]} · escenas {n_esc} · "
              f"C final {Cd:.3f}")
        del recs, ctxs
    import statistics as st
    salida = {"consejero": CONS, "escenas": n_esc,
              "cajas": {c: {k: dict(v) for k, v in d.items()}
                        for c, d in cajas.items()},
              "C final por diario": finales,
              "C final mediana": st.median(finales) if finales else None,
              "trayectoria de C": {k: (st.median(v) if v else None)
                                   for k, v in trayec.items()},
              "comprobacion": dict(compro),
              "dano": {c: dict(v) for c, v in dano.items()},
              "recuperacion por grupo (C=1)": dict(recup),
              "coste_ms": {"mediana": st.median(ms) if ms else None,
                           "max": max(ms) if ms else None, "n": len(ms)}}
    json.dump(salida, open(os.path.join(AQUI, f"P54B_{CONS}.json"), "w"),
              ensure_ascii=False, indent=1)
    avisa(f"\nCONSEJERO {CONS} · escenas {n_esc}")
    for c in CES:
        avisa(f"  C={c:4s} " + " · ".join(
            f"{k} {dict(cajas[c][k])}" for k in ("despues", "azarp")))
    avisa(f"  C final mediana {salida['C final mediana']} · trayectoria "
          f"{salida['trayectoria de C']}")
    avisa(f"  comprobacion {dict(compro)}")


if __name__ == "__main__":
    main()

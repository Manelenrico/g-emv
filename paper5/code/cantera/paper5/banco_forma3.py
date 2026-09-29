"""[P5-3C] Las llaves como FORMAS con el COMPARADOR JUSTO.

Cambio unico respecto a P5-3B: la curva de comparacion ya no es «el paso
ganador y luego quedarse», sino la MEJOR del PUÑADO PROPIO: cada candidato del
cuerpo en `t` se proyecta como forma de un tramo y se queda la de menor coste
ponderado entre las que pasan la vida minima (`forma.mejor_propia`).

QUEDATE se retira: en P5-3B coincidio en sus 125 escenas.

Salida sin buffer; progreso por diario en P53B_progreso.log.
"""
from __future__ import annotations
import collections, copy, glob, json, os, random, sys, time

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                      # noqa: E402
from serie_util import D, DOV, TOL                          # noqa: E402
from alma import appraisal_zs_v42_exp as V42                # noqa: E402
import banco_llaves as B                                    # noqa: E402
import proyeccion as P                                      # noqa: E402
import forma as F                                           # noqa: E402

SEMILLA, SEM_AZAR = B.SEMILLA, 20260919
CADA, DESDE, HOR = B.CADA, B.DESDE, 100
LLAVES = ("ahora", "despues", "azarp")
CRIT = ("estricto", "ventana", "vida")
CAJAS = ("aceptada", "coincide", "rechazada", "rechazada_vida",
         "rechazada_area", "vetada", "dormida", "caducada")
SOLIDOS = ("#", "F", "R")
PROG = open(os.path.join(AQUI, "P53C_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


def casilla_a(filas, pos, pasos, rnd):
    n = len(filas)
    ops = [(pos[0] + dx, pos[1] + dy)
           for dy in range(-pasos, pasos + 1)
           for dx in range(-pasos, pasos + 1)
           if max(abs(dx), abs(dy)) == pasos
           and 0 <= pos[0] + dx < n and 0 <= pos[1] + dy < n
           and filas[pos[1] + dy][pos[0] + dx] not in SOLIDOS]
    return rnd.choice(ops) if ops else None


def tramos_reales(tk, t, K, maxn=4):
    """El camino real resumido en hasta `maxn` tramos: los sitios donde cambio
    de rumbo, cogio o uso."""
    pts, ult_dir, tr = [], None, []
    p0 = tuple(tk[t].get("pos") or ())
    ant = p0
    for u in range(t + 1, t + K + 1):
        r = tk.get(u)
        if r is None:
            break
        p = tuple(r.get("pos") or ())
        el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
        if el.startswith("coger"):
            pts.append((p, "coger"))
        elif el.startswith("usar_"):
            pts.append((p, "usar"))
        elif p != ant:
            d = (p[0] - ant[0], p[1] - ant[1])
            if ult_dir is not None and d != ult_dir:
                pts.append((ant, "ir"))
            ult_dir = d
            ant = p
    pts.append((ant, "ir"))
    # quedarse con los ultimos `maxn`, en orden, sin repetir casilla seguida
    lim, vistos = [], None
    for p, q in pts:
        if vistos == p and q == "ir":
            continue
        lim.append({"destino": p, "intencion": q})
        vistos = p
    if len(lim) > maxn:
        lim = lim[:maxn - 1] + [lim[-1]]
    return lim


def a_ir(dest, obs, mem):
    return {"tipo": "ir", "destino": tuple(dest),
            "cuerpos": frozenset(tuple(a.get("pos") or ()) for a in
                                 ((obs.get("visible") or {}).get("agents") or [])
                                 if a.get("pos")),
            "recoger": mem.objetos_vistos.get(tuple(dest))}


def compite(nombre, rec, ventaja, obs, mundo, mem, blo, tick, el_cuerpo):
    """La forma aceptada entra como un candidato mas, con la VENTAJA del area."""
    base = list(D.candidatos(obs, mundo, copy.deepcopy(mem), tick,
                             copy.deepcopy(blo)))
    nom = {c[0] for c in base}
    if nombre in nom or any(
            isinstance(r, dict) and r.get("destino")
            and tuple(r["destino"]) == tuple(rec["destino"]) for _n, r in base
            if _n == el_cuerpo):
        return "coincide", {}
    if B.veta_receta(blo, rec, obs, tick):
        return "vetada", {}
    _orig = D.candidatos

    def _c(o, mu, me, tk_, bl=None, _o=_orig):
        return list(_o(o, mu, me, tk_, bl)) + [(nombre, rec)]
    D.candidatos = _c
    try:
        _a, det = D.decide(obs, mundo, copy.deepcopy(mem), tick,
                           copy.deepcopy(blo))
    finally:
        D.candidatos = _orig
    dd = U.ds(det)
    if nombre not in dd:
        return "dormida", {}
    mejor = min((v for k, v in dd.items() if k != nombre), default=None)
    ajustada = dd[nombre] - max(0.0, ventaja)
    if mejor is None or ajustada < mejor - TOL:
        return "aceptada", {"d_prop": dd[nombre], "ajustada": ajustada,
                            "d_cuerpo": mejor}
    cd = det.get("candidatos") or {}
    a, b = cd.get(nombre), cd.get(det.get("elegido"))
    filas = {}
    if isinstance(a, dict) and isinstance(b, dict):
        fa, fb = a.get("filas") or {}, b.get("filas") or {}
        for k in set(fa) | set(fb):
            v = float(fa.get(k) or 0.0) - float(fb.get(k) or 0.0)
            if abs(v) > 1e-9:
                filas[k] = round(v, 5)
        filas = dict(sorted(filas.items(), key=lambda x: -abs(x[1]))[:3])
    return "rechazada", {"d_prop": dd[nombre], "ajustada": ajustada,
                         "d_cuerpo": mejor, "filas": filas}


def main():
    D.A = V42
    U.pon(False)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(SEMILLA).sample(range(len(fs)), 40))
    rnd_az = random.Random(SEM_AZAR)
    avisa(f"diarios {len(fs)} · elegidos {len(idx)} · semilla {SEMILLA}")

    cajas = {c: {k: collections.Counter() for k in LLAVES} for c in CRIT}
    regla = {k: collections.Counter() for k in LLAVES}
    vidas_alt = {k: {10: collections.Counter(), 20: collections.Counter()}
                 for k in LLAVES}
    pierde = {k: collections.Counter() for k in LLAVES}
    punto_pierde = {k: collections.Counter() for k in LLAVES}
    b0 = collections.Counter()
    ms, n_cand = [], []
    mejor_quien = {k: collections.Counter() for k in LLAVES}
    gana_contra = {k: collections.Counter() for k in LLAVES}
    llegada = []
    det_ej = []
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
        filas, items = list(sm["filas"]), cat["items"]
        mundo = U.mundo_de(pc, filas, items)
        tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
        vivos = [r for r in recs
                 if r.get("k") == "tick" and r.get("phase") == "live"]
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
        libres = {t: [u for u in range(t, t + HOR + 1)
                      if u in vivo and mri.get(u, 1) == 0] for t in esc}
        necesarios = set(esc) | {u for t in esc for u in libres[t]}
        pend = collections.defaultdict(list)
        guardadas = {}

        mem = V42.Memoria()
        blo = D.Bloqueos()
        ult = None
        for r in [x for x in recs if x.get("k") == "tick"]:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t)
            blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            pre = copy.deepcopy(mem) if t in necesarios else None
            _in = (r.get("intencion") or {}).get("do")
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if _in == "attack" or _el.startswith("atacar"):
                mem.ultimo_ataque = t
            elif _el.startswith("soltar_"):
                mem.cedidos[tuple(r.get("pos") or ())] = {
                    "item": {"id": _el[len("soltar_"):], "n": 1}, "tick": t}
            if t not in necesarios:
                continue
            if t in esc:
                n_esc += 1
                ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo,
                       "tick": t, "r": r}
                bd = B.decide_v42(ctx)
                el = bd.get("elegido") or ""
                cand = (bd.get("candidatos") or {}).get(el) or {}
                e0 = P.estado_de(r)
                suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
                         if it.get("pos")}
                dest_cuerpo = None
                for n, rec in D.candidatos(o, mundo, copy.deepcopy(pre), t,
                                           copy.deepcopy(blo)):
                    if n == el and isinstance(rec, dict) and rec.get("destino"):
                        dest_cuerpo = tuple(rec["destino"])
                        break
                # ---- B0: ¿llego adonde queria?
                b0["escenas"] += 1
                if dest_cuerpo and (t + HOR) in vivo:
                    b0["con destino"] += 1
                    lleg = next((u for u in range(t, t + HOR + 1)
                                 if pos_t.get(u) == dest_cuerpo), None)
                    if lleg is not None:
                        b0["llego"] += 1
                        llegada.append(lleg - t)
                # ---- las formas
                formas = {}
                # [P5-3B arreglo] O-ahora existe en TODA escena. Si el ganador
                # del cuerpo no tiene destino (noop, usar, atacar...), la forma
                # de un tramo es "esperar", y coincide con el por definicion.
                formas["ahora"] = ([{"destino": dest_cuerpo, "intencion": "ir"}]
                                   if dest_cuerpo else
                                   [{"destino": None, "intencion": "esperar",
                                     "esperar": 0}])
                t2 = t + HOR
                quedate = False
                if t2 in vivo and d_t.get(t2) is not None \
                        and d_t.get(t) is not None and d_t[t2] < d_t[t]:
                    formas["despues"] = tramos_reales(tk, t, HOR)
                    ultd = formas["despues"][-1]["destino"]
                    pasos = F.cheb(pos_t[t], ultd)
                    quedate = (pasos == 0)
                    z = casilla_a(filas, pos_t[t], max(1, pasos), rnd_az)
                    if z:
                        formas["azarp"] = [{"destino": tuple(z),
                                            "intencion": "ir"},
                                           {"destino": None,
                                            "intencion": "esperar",
                                            "esperar": max(
                                                0, HOR - F.cheb(pos_t[t], z)
                                                * P.PASO_TICS)}]
                trabajos = []
                for k, tramos in formas.items():
                    # [P5-3B arreglo] «coincide si su primer tramo es el mismo
                    # que el ganador del cuerpo» (B3) se decide ANTES de la
                    # regla: si la forma propone lo que el cuerpo ya iba a
                    # hacer, no hay nada que comparar y el area vale 0 por
                    # construccion. Antes caia en «rechazada por area», que era
                    # un falso negativo mio.
                    d0 = tramos[0].get("destino")
                    mismo = ((d0 is None and not dest_cuerpo)
                             or (d0 is not None and dest_cuerpo
                                 and tuple(d0) == tuple(dest_cuerpo)))
                    if mismo:
                        regla[k]["coincide"] += 1
                        for c in CRIT:
                            cajas[c][k]["coincide"] += 1
                        continue
                    pcs = F.puntos_de_control(e0, tramos)
                    tics = [x[0] for x in pcs]
                    cf = F.curva(e0, o, tramos, mundo, pre, suelo)
                    # [P5-3C] EL COMPARADOR JUSTO: el mejor del puñado propio
                    _t0 = time.perf_counter()
                    base_c = list(D.candidatos(o, mundo, copy.deepcopy(pre), t,
                                               copy.deepcopy(blo)))
                    cs, quien, sin_vida = F.mejor_propia(
                        e0, o, base_c, tics, mundo, pre, suelo, t)
                    ms.append((time.perf_counter() - _t0) * 1000.0)
                    n_cand.append(len(base_c))
                    if cs is None:
                        continue
                    mejor_quien[k][quien] += 1
                    ver, ar, dt = F.juzga_forma(cf, cs, t)
                    regla[k][ver] += 1
                    for vm in (10, 20):
                        v2, _a2, _d2 = F.juzga_forma(cf, cs, t, vida_min=vm)
                        vidas_alt[k][vm][v2] += 1
                    if ver != "ok":
                        for c in CRIT:
                            cajas[c][k]["rechazada_" + ver] += 1
                        if ver == "area":
                            # donde pierde: el punto con peor aporte
                            pts = dt.get("puntos") or []
                            if pts:
                                peor = min(pts, key=lambda x: x["gana"])
                                punto_pierde[k][
                                    f"punto {pts.index(peor)+1} de {len(pts)}"] += 1
                        continue
                    dprim = formas[k][0].get("destino")
                    if dprim is None:
                        # QUEDATE: su primer tramo es "esperar" -> noop
                        nombre, rec = "noop", {"tipo": "esperar"}
                        trabajos.append((k, nombre, None, ar, el))
                    else:
                        trabajos.append((k, f"_FM_ir_{dprim[0]}_{dprim[1]}",
                                         a_ir(dprim, o, pre), ar, el))
                    if ver == "ok":
                        pts = dt.get("puntos") or []
                        if pts:
                            mej = max(pts, key=lambda x: x["gana"])
                            gana_contra[k][
                                f"punto {pts.index(mej)+1} de {len(pts)}"] += 1
                    if len(det_ej) < 3 and k == "despues":
                        det_ej.append({
                            "diario": os.path.basename(f), "tic": t,
                            "tramos": [{"destino": list(x["destino"])
                                        if x.get("destino") else None,
                                        "intencion": x["intencion"],
                                        "esperar": x.get("esperar")}
                                       for x in tramos],
                            "puntos_de_control": [
                                {"tic": p["tic"], "d": p["d"],
                                 "vida": p["vida"], "W": p["W"],
                                 "pos": list(p["pos"])} for p in cf],
                            "seguir_solo": [
                                {"tic": p["tic"], "d": p["d"],
                                 "vida": p["vida"]} for p in cs],
                            "area": ar, "veredicto": ver,
                            "detalle": dt.get("puntos")})
                for k, nombre, rec, ar, elc in trabajos:
                    if rec is None:
                        for c in CRIT:
                            cajas[c][k]["coincide" if elc == "noop"
                                        else "aceptada"] += 1
                        continue
                    caja, info = compite(nombre, rec, ar, o, mundo, pre, blo,
                                         t, elc)
                    cajas["estricto"][k][caja] += 1
                    if caja == "rechazada":
                        for fl, v in (info.get("filas") or {}).items():
                            if v > 0:
                                pierde[k][fl] += 1
                                break
                guardadas[t] = trabajos
                L = libres[t]
                if not L:
                    for k, _n, _r, _a, _e in trabajos:
                        cajas["ventana"][k]["caducada"] += 1
                        cajas["vida"][k]["caducada"] += 1
                else:
                    for u in L:
                        pend[u].append((t, u == L[0]))
            for (t0, es_v) in pend.pop(t, []):
                for k, nombre, rec, ar, elc in guardadas.get(t0, []):
                    if rec is None:
                        continue
                    caja, info = compite(nombre, rec, ar, o, mundo, pre, blo,
                                         t, elc)
                    if es_v:
                        cajas["ventana"][k][caja] += 1
                    reg = guardadas.setdefault("_v" + str(t0), {})
                    reg.setdefault(k, collections.Counter())[caja] += 1
            # cierre de vida entera al pasar el horizonte
        for t0 in list(guardadas):
            if isinstance(t0, str):
                continue
            reg = guardadas.get("_v" + str(t0)) or {}
            for k, _n, _r, _a, _e in guardadas[t0]:
                c = reg.get(k) or collections.Counter()
                if not c:
                    continue
                caja = ("aceptada" if c["aceptada"] else
                        "coincide" if c["coincide"] else
                        "rechazada" if c["rechazada"] else
                        "vetada" if c["vetada"] else "caducada")
                cajas["vida"][k][caja] += 1
        avisa(f"[{orden}/{len(idx)}] {os.path.basename(f)[:44]} · "
              f"escenas {n_esc}")
        del recs, tk, vivos, mem, blo, guardadas, pend

    salida = {"semilla": SEMILLA, "escenas": n_esc,
              "B0": {"escenas": b0["escenas"],
                     "con destino": b0["con destino"], "llego": b0["llego"],
                     "fraccion": (b0["llego"] / b0["con destino"]
                                  if b0["con destino"] else None),
                     "tic mediano de llegada":
                         sorted(llegada)[len(llegada) // 2] if llegada else None},
              "regla": {k: dict(v) for k, v in regla.items()},
              "vida_min alternativa": {k: {str(a): dict(b) for a, b in v.items()}
                                       for k, v in vidas_alt.items()},
              "cajas": {c: {k: dict(v) for k, v in d2.items()}
                        for c, d2 in cajas.items()},
              "fila que tumba": {k: dict(v.most_common()) for k, v in pierde.items()},
              "punto donde pierde": {k: dict(v) for k, v in punto_pierde.items()},
              "coste_ms": {"n": len(ms),
                           "mediana": (sorted(ms)[len(ms)//2] if ms else None),
                           "p90": (sorted(ms)[int(.9*(len(ms)-1))] if ms else None),
                           "max": (max(ms) if ms else None),
                           "candidatos medianos": (sorted(n_cand)[len(n_cand)//2]
                                                   if n_cand else None)},
              "quien es la mejor propia": {k: dict(v.most_common(8))
                                           for k, v in mejor_quien.items()},
              "en que punto gana": {k: dict(v) for k, v in gana_contra.items()},
              "ejemplos": det_ej}
    json.dump(salida, open(os.path.join(AQUI, "P53C_resumen.json"), "w"),
              ensure_ascii=False, indent=1)
    avisa(f"\nESCENAS {n_esc:,}")
    avisa(f"B0: {salida['B0']}")
    for k in LLAVES:
        avisa(f"  regla {k:9s}: {dict(regla[k])}")
    for c in CRIT:
        avisa(f"  {c}:")
        for k in LLAVES:
            cc = cajas[c][k]
            if sum(cc.values()):
                avisa(f"    {k:9s} " + " · ".join(
                    f"{b} {cc[b]}" for b in CAJAS if cc[b]))


if __name__ == "__main__":
    main()

"""[P5-2b] Reanalisis con VENTANA, empates por destino y las piernas.

Cambios respecto a `banco_llaves.py`, todos declarados:

  · NO se rehace la comprobacion de reproduccion del arnes: quedo cerrada en
    112.865/112.865 = 100,00 %. Aqui solo se decide en los tics que hacen
    falta (el de la escena y el de su ventana), que es lo que lo abarata.
  · VENTANA: cada propuesta compite en el PRIMER tic desde t con
    `move_ready_in == 0`, dentro de los 100 siguientes, y se puntua con la
    foto de ESE tic. Si no hay ninguno, o si alli ya no se puede atar, cuenta
    como CADUCADA, aparte.
  · EMPATE POR DESTINO: un candidato traducido cuyo destino es identico al de
    un candidato propio cuenta como `coincide`. Se cuenta con y sin la regla.

Salida SIN buffer y una linea por diario en P52b_progreso.log.
"""
from __future__ import annotations
import collections, copy, glob, json, os, random, sys

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                       # noqa: E402
from serie_util import D, DOV, TOL                           # noqa: E402
from alma import cortex_t5 as CX                             # noqa: E402
from alma import appraisal_zs_v42_exp as V42                 # noqa: E402
import banco_llaves as B                                     # noqa: E402

SEMILLA, N_DIARIOS = B.SEMILLA, B.N_DIARIOS
CADA, DESDE, HORIZONTE = B.CADA, B.DESDE, B.HORIZONTE
CAJAS = ("aceptada", "coincide", "rechazada", "vetada", "intraducible",
         "dormida", "caducada")
PROG = open(os.path.join(AQUI, "P52b_progreso.log"), "w", buffering=1)


def avisa(txt):
    print(txt, flush=True)
    PROG.write(txt + "\n")


def destinos_vivos(base):
    return {tuple(r["destino"]): n for n, r in base
            if isinstance(r, dict) and r.get("destino")}


def juzga2(prop, obs, mundo, mem, blo, tick, base_det, empate_destino):
    """Como `banco_llaves.juzga`, pero devuelve tambien si la regla del
    empate por destino cambiaria la caja, y reaprovecha la decision."""
    if prop.get("clase") == "IMPOSIBLE" or not prop.get("nombre"):
        return "intraducible", {}, None
    base = list(D.candidatos(obs, mundo, copy.deepcopy(mem), tick,
                             copy.deepcopy(blo)))
    nom = {c[0] for c in base}
    at = CX.ata(prop.get("objetivo_nombrado"), prop.get("nombre"), base, obs,
                mundo, copy.deepcopy(mem), tick)
    if at is None:
        return "dormida", {}, None
    n, rec, como = at
    if como == "cuerpo" or n in nom:
        return "coincide", {"nombre": n}, None
    # [P5-2b (2)] el mismo destino con otro nombre
    dst = tuple(rec["destino"]) if (rec or {}).get("destino") else None
    gemelo = destinos_vivos(base).get(dst) if dst else None
    if B.veta_receta(blo, rec, obs, tick):
        return "vetada", {"nombre": n, "gemelo": gemelo}, gemelo
    _orig = D.candidatos

    def _c(o, mu, me, tk, bl=None, _o=_orig):
        return list(_o(o, mu, me, tk, bl)) + [(n, rec)]
    D.candidatos = _c
    try:
        _a, det = D.decide(obs, mundo, copy.deepcopy(mem), tick,
                           copy.deepcopy(blo))
    finally:
        D.candidatos = _orig
    dd = U.ds(det)
    el = det.get("elegido")
    cd = det.get("candidatos") or {}
    a, b = cd.get(n), cd.get(el)
    filas = {}
    if isinstance(a, dict) and isinstance(b, dict):
        fa, fb = a.get("filas") or {}, b.get("filas") or {}
        for k in set(fa) | set(fb):
            v = float(fa.get(k) or 0.0) - float(fb.get(k) or 0.0)
            if abs(v) > 1e-9:
                filas[k] = round(v, 5)
        filas = dict(sorted(filas.items(), key=lambda x: -abs(x[1]))[:3])
    info = {"nombre": n, "gana": el, "d_prop": dd.get(n), "d_gana": dd.get(el),
            "filas": filas, "gemelo": gemelo}
    if el != n:
        return "rechazada", info, gemelo
    mejor = min((v for k, v in dd.items() if k != n), default=None)
    if mejor is not None and dd[n] >= mejor - TOL:
        info["gana"] = "empate devuelto al cuerpo"
        return "rechazada", info, gemelo
    return "aceptada", info, gemelo


def main():
    D.A = V42
    U.pon(False)
    # [P5-2b] Los diarios se cargan DE UNO EN UNO. `banco_llaves.py` hacia
    # `list(diarios_planos(...))`, que mantiene los ochenta en memoria a la vez
    # y dispara el consumo a varios GB. La seleccion es la MISMA: los mismos
    # indices sobre la misma lista ordenada de ficheros.
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    rnd = random.Random(SEMILLA)
    idx = sorted(rnd.sample(range(len(fs)), min(N_DIARIOS, len(fs))))
    avisa(f"diarios {len(fs)} · elegidos {len(idx)} · semilla {SEMILLA}")

    cajas = {c: {k: collections.Counter() for k in ("ahora", "despues", "azar")}
             for c in ("estricto", "ventana")}
    det = {"estricto": [], "ventana": []}
    piernas = collections.Counter()
    ventana_stats = collections.Counter()
    n_esc = 0

    for orden, i in enumerate(idx, 1):
        f = fs[i]
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if pc is None or sm is None or cat is None:
            avisa(f"[{orden}/{len(idx)}] {os.path.basename(f)[:46]}: sin cabecera")
            continue
        eid = os.path.basename(f).split("-policy_agent_")[0]
        slot, filas, items = pc.get("slot"), list(sm["filas"]), cat["items"]
        nom = os.path.basename(f)
        conf = B.interruptores(recs)
        B.pon_v42(conf)
        mundo = U.mundo_de(pc, filas, items)
        tk = [r for r in recs if r.get("k") == "tick"]
        vivos = [r for r in tk if r.get("phase") == "live"]
        pos_t = {r["tick"]: tuple(r.get("pos") or ()) for r in tk}
        mri = {r["tick"]: (r.get("move_ready_in") or 0) for r in vivos}
        d_t = {}
        for r in tk:
            R = r.get("RADIOGRAFIA") or {}
            c = (R.get("candidatos") or {}).get(R.get("elegido"))
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        vivo = {r["tick"] for r in vivos}
        # [P5-2b (3)] las piernas
        for r in vivos:
            m = r.get("move_ready_in") or 0
            piernas["vivos"] += 1
            piernas["frias"] += (m > 0)
            el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if el == "noop":
                piernas["noop"] += 1
                piernas["noop_frias"] += (m > 0)
        # escenas y su ventana
        esc = [r["tick"] for r in vivos
               if r["tick"] >= DESDE and r["tick"] % CADA == 0]
        vent = {}
        for t in esc:
            w = None
            for u in range(t, t + HORIZONTE + 1):
                if u in vivo and mri.get(u, 1) == 0:
                    w = u
                    break
            vent[t] = w
            ventana_stats["escenas"] += 1
            ventana_stats["sin ventana (piernas frias los 100 tics)"] += (w is None)
            if w is not None:
                ventana_stats["espera hasta la ventana"] += (w - t)
        necesarios = set(esc) | {w for w in vent.values() if w}
        pend = collections.defaultdict(list)     # tic -> [(llave, texto, extra, t0)]

        mem = V42.Memoria()
        blo = D.Bloqueos()
        ult = None
        for r in tk:
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
            ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo,
                   "tick": t, "r": r}
            bd = B.decide_v42(ctx)
            radio = {"candidatos": bd.get("candidatos") or {},
                     "ahora": bd.get("ahora") or {}}
            e, ofr, vivas = B.foto_e(o, mundo, pre, blo, t, dict(r), radio)
            cx = CX.Cortex.__new__(CX.Cortex)
            cx.clases = {"DENTRO": 0, "FUERA": 0, "IMPOSIBLE": 0}
            cx.inicia_ataque = 0

            def mide(crit, llave, txt, extra, t0):
                p = cx._traduce({"accion": txt, "motivo": ""}, e, ofr, t)
                caja, info, gem = juzga2(p, o, mundo, pre, blo, t, bd, True)
                if crit == "ventana" and caja in ("intraducible", "dormida"):
                    caja = "caducada"
                cajas[crit][llave][caja] += 1
                fila = {"eid": eid, "slot": slot, "t0": t0, "tic": t,
                        "llave": llave, "caja": caja, "texto": txt,
                        "elegido_real": bd.get("elegido"), "gemelo": gem}
                fila.update(info)
                if extra:
                    fila.update(extra)
                det[crit].append(fila)

            if t in esc:                       # criterio ESTRICTO, en t
                n_esc += 1
                elegido = bd.get("elegido")
                txt, forma = B.texto_ahora(elegido, vivas,
                                           tuple(r.get("pos") or ()), ofr)
                trabajos = []
                if txt:
                    trabajos.append(("ahora", txt, {"forma": forma}))
                t2 = t + HORIZONTE
                if t2 in vivo and d_t.get(t2) is not None \
                        and d_t.get(t) is not None and d_t[t2] < d_t[t]:
                    q = pos_t[t2]
                    trabajos.append(("despues", B.texto_casilla(q),
                                     {"destino": list(q),
                                      "pasos": U.cheb(pos_t[t], q),
                                      "mejora": d_t[t2] - d_t[t]}))
                alc = B.alcanzables(o, mundo, pre, blo, t)
                if alc:
                    q = rnd.choice(alc)
                    trabajos.append(("azar", B.texto_casilla(q),
                                     {"destino": list(q),
                                      "pasos": U.cheb(pos_t[t], q)}))
                for llave, txt2, extra in trabajos:
                    mide("estricto", llave, txt2, extra, t)
                w = vent.get(t)
                if w is None:
                    for llave, _x, _e in trabajos:
                        cajas["ventana"][llave]["caducada"] += 1
                else:
                    for llave, txt2, extra in trabajos:
                        pend[w].append((llave, txt2, extra, t))
            for llave, txt2, extra, t0 in pend.pop(t, []):
                mide("ventana", llave, txt2, extra, t0)
        avisa(f"[{orden}/{len(idx)}] {nom[:46]} a{slot} · {len(esc)} escenas "
              f"· acumuladas {n_esc}")
        del recs, tk, vivos, pos_t, d_t, mem, blo

    salida = {"semilla": SEMILLA, "diarios": len(idx), "escenas": n_esc,
              "cajas": {c: {k: dict(v) for k, v in d2.items()}
                        for c, d2 in cajas.items()},
              "piernas": dict(piernas), "ventana": dict(ventana_stats)}
    json.dump(salida, open(os.path.join(AQUI, "P52b_resumen.json"), "w"),
              ensure_ascii=False, indent=1)
    json.dump(det, open(os.path.join(AQUI, "P52b_detalle.json"), "w"),
              ensure_ascii=False)
    avisa(f"\nESCENAS {n_esc:,}")
    for crit in ("estricto", "ventana"):
        avisa(f"  {crit}:")
        for k in ("ahora", "despues", "azar"):
            c = cajas[crit][k]
            avisa(f"    {k:8s} n={sum(c.values()):5,} " +
                  " · ".join(f"{b} {c[b]}" for b in CAJAS if c[b]))
    avisa(f"  piernas: {dict(piernas)}")
    avisa(f"  ventana: {dict(ventana_stats)}")


if __name__ == "__main__":
    main()

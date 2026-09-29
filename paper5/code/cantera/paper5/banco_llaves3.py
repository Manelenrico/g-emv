"""[P5-2c] Azar EMPAREJADO por distancia y criterio de VIDA ENTERA.

Tres criterios por propuesta, con el mismo texto y el mismo traductor:
  · ESTRICTO     — solo el tic t.
  · VENTANA      — el primer tic desde t con `move_ready_in == 0`, <= t+100.
  · VIDA ENTERA  — CADA tic con las piernas listas dentro de los 100 de vida;
                   aceptada si gana alguna vez. Es el gemelo del campo: la
                   atadura perezosa reintenta cada tic (`policy_cortex.py:444`).

La traduccion se hace UNA vez, en t, con la foto de t, y despues se REATA cada
tic con `CX.ata`, que es lo que hace el campo. `decisor_zs.py` y
`appraisal_zs_v42_exp.py` no se tocan.

Salida sin buffer; una linea por diario en P52c_progreso.log.
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
SEMILLA_AZAR = 20260919                  # la del azar emparejado, fija
CADA, DESDE, HORIZONTE = B.CADA, B.DESDE, B.HORIZONTE
SOLIDOS = ("#", "F", "R")
LLAVES = ("ahora", "despues", "azarp")
CRIT = ("estricto", "ventana", "vida")
CAJAS = ("aceptada", "coincide", "rechazada", "vetada", "intraducible",
         "dormida", "caducada")
PROG = open(os.path.join(AQUI, "P52c_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


def casillas_a(filas, pos, pasos, rnd):
    """Una casilla PISABLE del mapa a exactamente `pasos` de `pos`, al azar."""
    n = len(filas)
    ops = []
    for dy in range(-pasos, pasos + 1):
        for dx in range(-pasos, pasos + 1):
            if max(abs(dx), abs(dy)) != pasos:
                continue
            x, y = pos[0] + dx, pos[1] + dy
            if 0 <= x < n and 0 <= y < n and filas[y][x] not in SOLIDOS:
                ops.append((x, y))
    return rnd.choice(ops) if ops else None


def gemelo_de(base, rec):
    d = (rec or {}).get("destino")
    if not d:
        return None
    d = tuple(d)
    for n, r in base:
        if isinstance(r, dict) and r.get("destino") and tuple(r["destino"]) == d:
            return n
    return None


def compite(prop, obs, mundo, mem, blo, tick, gemelo_cuenta):
    """Una pasada de la propuesta por la puerta en ESTE tic.

    Devuelve (caja, info). `gemelo_cuenta` solo para O-ahora.
    """
    if prop.get("clase") == "IMPOSIBLE" or not prop.get("nombre"):
        return "intraducible", {}
    base = list(D.candidatos(obs, mundo, copy.deepcopy(mem), tick,
                             copy.deepcopy(blo)))
    nom = {c[0] for c in base}
    at = CX.ata(prop.get("objetivo_nombrado"), prop.get("nombre"), base, obs,
                mundo, copy.deepcopy(mem), tick)
    if at is None:
        return "dormida", {}
    n, rec, como = at
    if como == "cuerpo" or n in nom:
        return "coincide", {"nombre": n}
    gem = gemelo_de(base, rec)
    if gemelo_cuenta and gem:
        return "coincide", {"nombre": n, "gemelo": gem}
    if B.veta_receta(blo, rec, obs, tick):
        return "vetada", {"nombre": n, "gemelo": gem}
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
    info = {"nombre": n, "gana": el, "filas": filas, "gemelo": gem,
            "d_prop": dd.get(n), "d_gana": dd.get(el)}
    if el != n:
        return "rechazada", info
    mejor = min((v for k, v in dd.items() if k != n), default=None)
    if mejor is not None and dd[n] >= mejor - TOL:
        info["gana"] = "empate devuelto al cuerpo"
        return "rechazada", info
    return "aceptada", info


def main():
    D.A = V42
    U.pon(False)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    rnd_sel = random.Random(SEMILLA)
    idx = sorted(rnd_sel.sample(range(len(fs)), min(N_DIARIOS, len(fs))))
    rnd_az = random.Random(SEMILLA_AZAR)
    avisa(f"diarios {len(fs)} · elegidos {len(idx)} · semilla seleccion "
          f"{SEMILLA} · semilla azar emparejado {SEMILLA_AZAR}")

    cajas = {c: {k: collections.Counter() for k in LLAVES} for c in CRIT}
    det = {c: [] for c in CRIT}
    extra = collections.Counter()
    n_esc = 0

    for orden, i in enumerate(idx, 1):
        f = fs[i]
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if pc is None or sm is None or cat is None:
            continue
        B.pon_v42(B.interruptores(recs))
        slot, filas, items = pc.get("slot"), list(sm["filas"]), cat["items"]
        eid = os.path.basename(f).split("-policy_agent_")[0]
        mundo = U.mundo_de(pc, filas, items)
        tk = [r for r in recs if r.get("k") == "tick"]
        vivos = [r for r in tk if r.get("phase") == "live"]
        pos_t = {r["tick"]: tuple(r.get("pos") or ()) for r in tk}
        mri = {r["tick"]: (r.get("move_ready_in") or 0) for r in vivos}
        vivo = {r["tick"] for r in vivos}
        d_t = {}
        for r in tk:
            R = r.get("RADIOGRAFIA") or {}
            c = (R.get("candidatos") or {}).get(R.get("elegido"))
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        esc = [r["tick"] for r in vivos
               if r["tick"] >= DESDE and r["tick"] % CADA == 0]
        # los tics en que cada escena puede competir: piernas listas, <= t+100
        libres = {t: [u for u in range(t, t + HORIZONTE + 1)
                      if u in vivo and mri.get(u, 1) == 0] for t in esc}
        necesarios = set(esc) | {u for t in esc for u in libres[t]}
        pend = collections.defaultdict(list)

        mem = V42.Memoria()
        blo = D.Bloqueos()
        ult = None
        vivas = {}          # t -> [(llave, prop, extra)]
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
            if t in esc:
                n_esc += 1
                ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo,
                       "tick": t, "r": r}
                bd = B.decide_v42(ctx)
                radio = {"candidatos": bd.get("candidatos") or {},
                         "ahora": bd.get("ahora") or {}}
                e, ofr, viv = B.foto_e(o, mundo, pre, blo, t, dict(r), radio)
                cx = CX.Cortex.__new__(CX.Cortex)
                cx.clases = {"DENTRO": 0, "FUERA": 0, "IMPOSIBLE": 0}
                cx.inicia_ataque = 0
                trab = []
                txt, forma = B.texto_ahora(bd.get("elegido"), viv,
                                           pos_t[t], ofr)
                if txt:
                    trab.append(("ahora", txt, {"forma": forma}))
                t2 = t + HORIZONTE
                if t2 in vivo and d_t.get(t2) is not None \
                        and d_t.get(t) is not None and d_t[t2] < d_t[t]:
                    q = pos_t[t2]
                    pasos = U.cheb(pos_t[t], q)
                    trab.append(("despues", B.texto_casilla(q),
                                 {"destino": list(q), "pasos": pasos,
                                  "mejora": d_t[t2] - d_t[t],
                                  "sin_moverse": pos_t[t] == q}))
                    # [P5-2c (1)] el azar EMPAREJADO: misma distancia
                    z = casillas_a(filas, pos_t[t], pasos, rnd_az)
                    if z:
                        trab.append(("azarp", B.texto_casilla(z),
                                     {"destino": list(z), "pasos": pasos}))
                    else:
                        extra["azar emparejado sin casilla libre"] += 1
                props = []
                for llave, txt2, ex in trab:
                    p = cx._traduce({"accion": txt2, "motivo": ""}, e, ofr, t)
                    props.append((llave, p, ex, txt2))
                    caja, info = compite(p, o, mundo, pre, blo, t,
                                         llave == "ahora")
                    cajas["estricto"][llave][caja] += 1
                    fi = {"eid": eid, "slot": slot, "t0": t, "tic": t,
                          "llave": llave, "caja": caja,
                          "elegido_real": bd.get("elegido")}
                    fi.update(info)
                    fi.update(ex)
                    det["estricto"].append(fi)
                vivas[t] = props
                L = libres[t]
                if not L:
                    for llave, _p, _e, _x in props:
                        cajas["ventana"][llave]["caducada"] += 1
                        cajas["vida"][llave]["caducada"] += 1
                    extra["escenas sin ningun tic con piernas listas"] += 1
                else:
                    for u in L:
                        pend[u].append((t, u == L[0]))
            for (t0, es_ventana) in pend.pop(t, []):
                for llave, p, ex, _x in vivas.get(t0, []):
                    caja, info = compite(p, o, mundo, pre, blo, t,
                                         llave == "ahora")
                    if es_ventana:
                        c2 = "caducada" if caja in ("intraducible",
                                                    "dormida") else caja
                        cajas["ventana"][llave][c2] += 1
                        fi = {"eid": eid, "slot": slot, "t0": t0, "tic": t,
                              "llave": llave, "caja": c2}
                        fi.update(info)
                        fi.update(ex)
                        det["ventana"].append(fi)
                    # vida entera: se acumula en `vivas`
                    reg = ex.setdefault("_vida", {"gana": [], "cajas":
                                                  collections.Counter()})
                    reg["cajas"][caja] += 1
                    if caja == "aceptada":
                        reg["gana"].append(t)
                    if caja == "rechazada" and "filas" not in reg:
                        reg["filas"] = info.get("filas")
        # cierre de vida entera del diario
        for t0, props in vivas.items():
            for llave, p, ex, txt2 in props:
                reg = ex.get("_vida")
                if reg is None:
                    continue
                c = reg["cajas"]
                if reg["gana"]:
                    caja = "aceptada"
                elif c["coincide"]:
                    caja = "coincide"
                elif c["rechazada"]:
                    caja = "rechazada"
                elif c["vetada"]:
                    caja = "vetada"
                else:
                    caja = "caducada"
                cajas["vida"][llave][caja] += 1
                fi = {"eid": eid, "slot": slot, "t0": t0, "llave": llave,
                      "caja": caja, "veces que gana": len(reg["gana"]),
                      "primera victoria": (reg["gana"][0] if reg["gana"]
                                           else None),
                      "edad de la primera victoria":
                          (reg["gana"][0] - t0 if reg["gana"] else None),
                      "tics en que compitio": sum(c.values()),
                      "filas": reg.get("filas")}
                fi.update({k: v for k, v in ex.items() if k != "_vida"})
                det["vida"].append(fi)
        avisa(f"[{orden}/{len(idx)}] {os.path.basename(f)[:46]} a{slot} · "
              f"{len(esc)} escenas · acumuladas {n_esc}")
        del recs, tk, vivos, pos_t, d_t, mem, blo, vivas, pend

    salida = {"semilla": SEMILLA, "semilla_azar": SEMILLA_AZAR,
              "diarios": len(idx), "escenas": n_esc,
              "cajas": {c: {k: dict(v) for k, v in d2.items()}
                        for c, d2 in cajas.items()},
              "extra": dict(extra)}
    json.dump(salida, open(os.path.join(AQUI, "P52c_resumen.json"), "w"),
              ensure_ascii=False, indent=1)
    json.dump(det, open(os.path.join(AQUI, "P52c_detalle.json"), "w"),
              ensure_ascii=False)
    avisa(f"\nESCENAS {n_esc:,} · {dict(extra)}")
    for c in CRIT:
        avisa(f"  {c}:")
        for k in LLAVES:
            cc = cajas[c][k]
            avisa(f"    {k:8s} n={sum(cc.values()):5,} " + " · ".join(
                f"{b} {cc[b]}" for b in CAJAS if cc[b]))


if __name__ == "__main__":
    main()

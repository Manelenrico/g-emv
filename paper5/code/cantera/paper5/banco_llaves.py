"""[P5-2] CONTROL DEL CONSEJO BUENO, EN BANCO. Coste cero, sin plataforma.

Pasa por la MISMA puerta que uso S-2 consejos que ya sabemos buenos y mide si
el cuerpo los reconoce. Sobre los diarios de S-2 brazo A (cuerpo solo).

El arnes es el v4d (`cantera/paper4/decide_otra_vez_v4d.py`): el orden del
campo, con las dos escrituras del epilogo tomadas del diario. La inyeccion
envuelve `D.candidatos` DESDE FUERA, igual que `policy_cortex.py:444-488`.
`decisor_zs.py` y `appraisal_zs_v42_exp.py` NO se tocan.

  python3 cantera/paper5/banco_llaves.py            la tanda entera
  python3 cantera/paper5/banco_llaves.py --humo 3   solo tres diarios
"""
from __future__ import annotations

import copy, glob, json, os, random, re, sys

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
P4 = os.path.join(RAIZ, "cantera", "paper4")
sys.path.insert(0, P4)
import serie_util as U                                    # noqa: E402
from serie_util import D, V37, V40, DOV, TOL              # noqa: E402
from alma import cortex_t5 as CX                          # noqa: E402
from alma import relator_t5 as RT                         # noqa: E402
from alma import appraisal_zs as A                        # noqa: E402
from alma import appraisal_zs_v42_exp as V42               # noqa: E402

# copiado de `policy_cortex.py:255-257` y `:279-283`, para no importar el
# modulo de la politica (que arranca hilos). `decisor_zs.Bloqueos.veta` es la
# misma funcion que usa el campo.
_VETO_POR_TIPO = {"ir": "ir_", "mover": "move_", "paso": "paso_",
                  "atacar": "atacar_", "usar": "usar_", "empunar": "empunar_",
                  "ponerse": "ponerse_"}


def veta_receta(bloqueos, receta, obs, tick):
    if bloqueos is None:
        return False
    pre = _VETO_POR_TIPO.get((receta or {}).get("tipo"))
    return bool(pre) and bloqueos.veta(pre + "X", obs, tick)


SEMILLA = 20260919          # la de la mesa del 19-sep-2026
N_DIARIOS = 40
CADA, DESDE = 50, 300       # la cadencia de las citas del consejero
HORIZONTE = 100             # los cien tics de la llave DESPUES
CAJAS = ("aceptada", "coincide", "rechazada", "vetada", "intraducible",
         "dormida")


def interruptores(recs):
    """Los interruptores de v42 TAL COMO LOS ESCRIBIO EL DIARIO.

    El registro `arranque` trae, por ejemplo:
      "cuerpo": "v42_exp EMPATIA_ON H_PREV 0.25 H_GOLPE 1.0 MIEDO_ON False
                 VIDA_AJENA_ON False"

    `EMPATIA_ON` es una marca suelta: si esta, la empatia va encendida.
    `MIEDO_ON` y `VIDA_AJENA_ON` llevan True/False detras, y los dos diales
    llevan un numero.
    """
    a = next((r for r in recs if r.get("k") == "arranque"), {})
    txt = a.get("cuerpo") or ""

    def bandera(clave, por_defecto=False):
        m = re.search(rf"\b{clave}\s+(True|False)\b", txt)
        return (m.group(1) == "True") if m else por_defecto

    def dial(clave, por_defecto):
        m = re.search(rf"\b{clave}\s+([0-9.]+)", txt)
        return float(m.group(1)) if m else por_defecto

    return {"EMPATIA_ON": bool(re.search(r"\bEMPATIA_ON\b", txt)),
            "MIEDO_ON": bandera("MIEDO_ON"),
            "VIDA_AJENA_ON": bandera("VIDA_AJENA_ON"),
            "H_PREV": dial("H_PREV", 0.25),
            "H_GOLPE": dial("H_GOLPE", 0.75),
            "texto": txt}


def pon_v42(conf):
    V42.EMPATIA_ON = conf["EMPATIA_ON"]
    V42.MIEDO_ON = conf["MIEDO_ON"]
    V42.VIDA_AJENA_ON = conf["VIDA_AJENA_ON"]
    V42.H_PREV = conf["H_PREV"]
    V42.H_GOLPE = conf["H_GOLPE"]
    V42.MEMORIA_APRENDIDA = {}


def decide_v42(ctx):
    """La decision del campo: v42_exp cableada en el decisor (`D.A`), memoria
    de ENTRADA en copia para que el epilogo no escriba dos veces."""
    _a, det = D.decide(ctx["o"], ctx["mundo"], copy.deepcopy(ctx["mem"]),
                       ctx["tick"], copy.deepcopy(ctx["blo"]))
    return det


def diarios_planos(tanda):
    """(eid, slot, recs, pc, filas, items) de los .art.log planos de S-2."""
    base = os.path.join(RAIZ, "paintball", "runs", tanda)
    for f in sorted(glob.glob(os.path.join(base, "*-policy_agent_1*.art.log"))):
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if pc is None or sm is None or cat is None:
            continue
        eid = os.path.basename(f).split("-policy_agent_")[0]
        yield (eid, pc.get("slot"), recs, pc, list(sm["filas"]),
               cat["items"], os.path.basename(f))


def foto_e(obs, mundo, mem, blo, tick, rec, radio):
    """El `e` y las `ofrecidas` del cortex, copiados de policy_cortex._foto."""
    cands = D.candidatos(obs, mundo, copy.deepcopy(mem), tick,
                         copy.deepcopy(blo))
    recetas, vivas = {}, {}
    for n, r in cands:
        vivas[n] = dict(r)
        recetas[n] = {"tipo": r.get("tipo"), "dir": r.get("dir"),
                      "destino": list(r["destino"]) if r.get("destino") else None,
                      "objetivo": r.get("objetivo"),
                      "item": ((r.get("item") or {}).get("id")
                               if isinstance(r.get("item"), dict)
                               else r.get("item"))}
    vis = obs.get("visible") or {}
    cuerpos = frozenset(tuple(a.get("pos") or ()) for a in
                        (vis.get("agents") or []) if a.get("pos"))
    e = {"r": rec, "pc_teammate": mundo.teammate_slot, "recetas": recetas,
         "cuerpo": {k: ({"d": v["d"], "movs": v.get("movs")}
                        if isinstance(v, dict) else {"d": v, "movs": None})
                    for k, v in (radio.get("candidatos") or {}).items()},
         "cert": A.agresor_de_la_hermana(obs, mundo, mem, tick),
         "parte_fresco": None,
         "agresores_det": (radio.get("ahora") or {}).get("agresores") or [],
         "_recetas_vivas": vivas, "_cuerpos": cuerpos,
         "_objetos": dict(mem.objetos_vistos)}
    ofrecidas = {n: RT.en_llano(n, e) for n in recetas}
    return e, ofrecidas, dict(cands)


def juzga(prop, obs, mundo, mem, blo, tick, base_det):
    """Pasa la propuesta por la puerta. Devuelve (caja, detalle).

    Replica `policy_cortex.decidir` en lo que toca a UNA propuesta viva:
    atadura perezosa, respaldo, veto, inyeccion, y empates para el cuerpo.
    """
    if prop.get("clase") == "IMPOSIBLE" or not prop.get("nombre"):
        return "intraducible", {"motivo": prop.get("motivo_imposible")}
    obj = prop.get("objetivo_nombrado")
    nombre0 = prop.get("nombre")
    base = list(D.candidatos(obs, mundo, copy.deepcopy(mem), tick,
                             copy.deepcopy(blo)))
    nom = {c[0] for c in base}
    at = CX.ata(obj, nombre0, base, obs, mundo, copy.deepcopy(mem), tick)
    if at is None:
        return "dormida", {}
    n, rec, como = at
    if como == "cuerpo" or n in nom:
        elegido = base_det.get("elegido")
        return "coincide", {"nombre": n, "lo_elige_el_cuerpo": elegido == n}
    if veta_receta(blo, rec, obs, tick):
        return "vetada", {"nombre": n, "tipo": (rec or {}).get("tipo")}
    _orig = D.candidatos

    def _c(o, mu, me, tk, bl=None, _o=_orig, _n=n, _r=rec):
        return list(_o(o, mu, me, tk, bl)) + [(_n, _r)]
    D.candidatos = _c
    try:
        _a, det = D.decide(obs, mundo, copy.deepcopy(mem), tick,
                           copy.deepcopy(blo))
    finally:
        D.candidatos = _orig
    el = det.get("elegido")
    if el != n:
        return "rechazada", {"nombre": n, "gana": el,
                             "d_prop": U.ds(det).get(n),
                             "d_gana": U.ds(det).get(el)}
    # LOS EMPATES SON DEL CUERPO: gana solo si es ESTRICTAMENTE mejor
    dd = U.ds(det)
    mejor_cuerpo = min((v for k, v in dd.items() if k != n), default=None)
    if mejor_cuerpo is not None and dd[n] >= mejor_cuerpo - TOL:
        return "rechazada", {"nombre": n, "gana": "empate devuelto al cuerpo",
                             "d_prop": dd[n], "d_gana": mejor_cuerpo}
    return "aceptada", {"nombre": n, "d_prop": dd[n], "d_gana": mejor_cuerpo}


# ---------------------------------------------------------------- las llaves
def texto_ahora(elegido, vivas, pos, ofrecidas=None):
    """La forma que usa el consejero para nombrar lo que el cuerpo eligio.

    Las tres formas del encargo: "ve a la casilla (x,y)", "coge ..." y
    "espera". Lo demas se nombra con la frase del relator, que es como el
    consejero nombra los candidatos del cuerpo.
    """
    r = vivas.get(elegido) or {}
    if elegido == "noop":
        return "espera", "espera"
    if elegido.startswith("coger"):
        it = r.get("item")
        it = it.get("id") if isinstance(it, dict) else it
        return f"coge {it}" if it else "coge lo que hay en el suelo", "coge"
    d = r.get("destino")
    if d:
        return f"ve a la casilla ({int(d[0])},{int(d[1])})", "casilla"
    # [declarado] cuando lo elegido no es una casilla, ni coger, ni esperar
    # (atacar, usar, empunar, ponerse, soltar), el texto es LA FRASE QUE EL
    # PROPIO CONSEJERO VE: la que el relator le ofrece para ese candidato.
    fr = (ofrecidas or {}).get(elegido)
    return (fr, "frase del relator") if fr else (None, "sin forma")


def texto_casilla(q):
    return f"ve a la casilla ({int(q[0])},{int(q[1])})"


def alcanzables(obs, mundo, mem, blo, tick):
    """Las casillas destino de los candidatos de MOVIMIENTO del cuerpo."""
    out = []
    for n, r in D.candidatos(obs, mundo, copy.deepcopy(mem), tick,
                             copy.deepcopy(blo)):
        d = r.get("destino")
        if d and n.startswith(("ir_", "move_", "paso_")):
            out.append(tuple(d))
    return out


# --------------------------------------------------------------- el recorrido
def main():
    humo = 0
    if "--humo" in sys.argv:
        humo = int(sys.argv[sys.argv.index("--humo") + 1])
    # EL CABLEADO DEL CAMPO, medido y no supuesto: `policy_cortex.py:97` hace
    # `D.A = appraisal_zs_v42_exp`, asi que en S-2 los CANDIDATOS se valoran con
    # v42_exp, no con v37. Y los interruptores NO se suponen: cada diario
    # escribe los suyos en su registro `arranque` (campo `cuerpo`), y de ahi se
    # leen. Se fijan como atributos de modulo, igual que hace `serie_util.pon`;
    # el fichero NO se toca.
    D.A = V42
    U.pon(False)
    todos = list(diarios_planos("S2_A"))
    rnd = random.Random(SEMILLA)
    elegidos = sorted(rnd.sample(range(len(todos)), min(N_DIARIOS, len(todos))))
    if humo:
        elegidos = elegidos[:humo]
    print(f"diarios de S2_A: {len(todos)} · elegidos {len(elegidos)} "
          f"con semilla {SEMILLA}")

    tot = {"tics": 0, "reproducidos": 0, "escenas": 0}
    cajas = {k: {c: 0 for c in CAJAS} for k in ("ahora", "despues", "azar")}
    det = {"ahora": [], "despues": [], "azar": []}
    confs = []
    saltos = {"sin_forma": 0, "sin_mejor": 0, "muerto": 0, "sin_alcanzable": 0}

    for i in elegidos:
        eid, slot, recs, pc, filas, items, nom = todos[i]
        conf = interruptores(recs)
        pon_v42(conf)
        confs.append(conf["texto"])
        mundo = U.mundo_de(pc, filas, items)
        mem = V42.Memoria()
        blo = D.Bloqueos()
        ult = None
        tk = [r for r in recs if r.get("k") == "tick"]
        pos_t = {r["tick"]: tuple(r.get("pos") or ()) for r in tk}
        # la d real del diario por tic: la del candidato elegido
        d_t = {}
        for r in tk:
            R = r.get("RADIOGRAFIA") or {}
            el = R.get("elegido")
            c = (R.get("candidatos") or {}).get(el)
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        vivo = {r["tick"] for r in tk if r.get("phase") == "live"}
        n_esc = 0
        for r in tk:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t)
            blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            pre = copy.deepcopy(mem)
            _in = (r.get("intencion") or {}).get("do")
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if _in == "attack" or _el.startswith("atacar"):
                mem.ultimo_ataque = t
            elif _el.startswith("soltar_"):
                mem.cedidos[tuple(r.get("pos") or ())] = {
                    "item": {"id": _el[len("soltar_"):], "n": 1}, "tick": t}
            ctx = {"eid": eid, "slot": slot, "tick": t, "r": r,
                   "mundo": mundo, "mem": pre, "blo": blo, "o": o}
            base_det = decide_v42(ctx)
            tot["tics"] += 1
            ok = U.verificado(ctx, base_det)
            tot["reproducidos"] += ok
            # ------- escena?
            if not (t >= DESDE and t % CADA == 0):
                continue
            if r.get("phase") != "live":
                continue
            tot["escenas"] += 1
            n_esc += 1
            radio = {"candidatos": base_det.get("candidatos") or {},
                     "ahora": base_det.get("ahora") or {}}
            e, ofrecidas, vivas = foto_e(o, mundo, pre, blo, t, dict(r), radio)
            cx = CX.Cortex.__new__(CX.Cortex)
            cx.clases = {"DENTRO": 0, "FUERA": 0, "IMPOSIBLE": 0}
            cx.inicia_ataque = 0
            elegido = base_det.get("elegido")

            def mete(llave, txt, extra=None):
                if txt is None:
                    saltos["sin_forma"] += 1
                    return
                p = cx._traduce({"accion": txt, "motivo": ""}, e, ofrecidas, t)
                caja, dd = juzga(p, o, mundo, pre, blo, t, base_det)
                cajas[llave][caja] += 1
                fila = {"eid": eid, "slot": slot, "tick": t, "texto": txt,
                        "caja": caja, "clase_traduccion": p.get("clase"),
                        "nombre_traducido": p.get("nombre"),
                        "elegido_real": elegido}
                fila.update(dd)
                if extra:
                    fila.update(extra)
                if caja == "rechazada":
                    fila["filas"] = filas_que_tumban(
                        o, mundo, pre, blo, t, p, base_det)
                det[llave].append(fila)

            # LLAVE AHORA
            txt, forma = texto_ahora(elegido, vivas,
                                     tuple(r.get("pos") or ()), ofrecidas)
            mete("ahora", txt, {"forma": forma})
            # LLAVE DESPUES
            t2 = t + HORIZONTE
            hay_despues = False
            if t2 not in vivo:
                saltos["muerto"] += 1
            elif d_t.get(t2) is None or d_t.get(t) is None:
                saltos["sin_mejor"] += 1
            elif d_t[t2] >= d_t[t]:
                saltos["sin_mejor"] += 1
            else:
                hay_despues = True
                q = pos_t[t2]
                mete("despues", texto_casilla(q),
                     {"destino": list(q), "pasos": U.cheb(pos_t[t], q),
                      "d_t": d_t[t], "d_t2": d_t[t2],
                      "mejora": d_t[t2] - d_t[t]})
            # CONTROL DE RUIDO
            alc = alcanzables(o, mundo, pre, blo, t)
            if not alc:
                saltos["sin_alcanzable"] += 1
            else:
                q = rnd.choice(alc)
                mete("azar", texto_casilla(q),
                     {"destino": list(q), "pasos": U.cheb(pos_t[t], q),
                      "pareja_con_despues": hay_despues})
        print(f"  {nom[:44]} a{slot}: {n_esc} escenas")

    salida = {"semilla": SEMILLA, "diarios": len(elegidos),
              "interruptores de v42 leidos del diario":
                  sorted(set(confs)),
              "reproduccion": tot, "cajas": cajas, "saltos": saltos}
    json.dump(salida, open(os.path.join(AQUI, "P52_resumen.json"), "w"),
              ensure_ascii=False, indent=1)
    json.dump(det, open(os.path.join(AQUI, "P52_detalle.json"), "w"),
              ensure_ascii=False)
    rep = 100.0 * tot["reproducidos"] / (tot["tics"] or 1)
    print(f"\nREPRODUCCION DEL ARNES: {tot['reproducidos']:,} de {tot['tics']:,}"
          f" = {rep:.2f} %")
    print(f"ESCENAS: {tot['escenas']:,} · saltos {saltos}")
    for k in ("ahora", "despues", "azar"):
        c = cajas[k]
        n = sum(c.values())
        print(f"  {k:8s} n={n:5,} " + " · ".join(
            f"{b} {c[b]}" for b in CAJAS if c[b]))


def filas_que_tumban(obs, mundo, mem, blo, tick, prop, base_det):
    """Las filas que mas separan la propuesta del ganador, con su signo."""
    try:
        obj, n0 = prop.get("objetivo_nombrado"), prop.get("nombre")
        base = list(D.candidatos(obs, mundo, copy.deepcopy(mem), tick,
                                 copy.deepcopy(blo)))
        at = CX.ata(obj, n0, base, obs, mundo, copy.deepcopy(mem), tick)
        if at is None:
            return None
        n, rec, _ = at
        _orig = D.candidatos

        def _c(o, mu, me, tk, bl=None, _o=_orig):
            return list(_o(o, mu, me, tk, bl)) + [(n, rec)]
        D.candidatos = _c
        try:
            _a, det = D.decide(obs, mundo, copy.deepcopy(mem), tick,
                               copy.deepcopy(blo))
        finally:
            D.candidatos = _orig
        cd = det.get("candidatos") or {}
        a, b = cd.get(n), cd.get(det.get("elegido"))
        if not isinstance(a, dict) or not isinstance(b, dict):
            return None
        # `filas` del detalle es plano: nombre -> valor (el M de esa fila en el
        # futuro de ese candidato). Mas alto = peor. La fila que TUMBA es en la
        # que la propuesta esta por encima del ganador.
        fa, fb = a.get("filas") or {}, b.get("filas") or {}
        difs = {}
        for k in set(fa) | set(fb):
            va = float(fa.get(k) or 0.0)
            vb = float(fb.get(k) or 0.0)
            if abs(va - vb) > 1e-9:
                difs[k] = round(va - vb, 5)
        return dict(sorted(difs.items(), key=lambda x: -abs(x[1]))[:3])
    except Exception:
        return None


if __name__ == "__main__":
    main()

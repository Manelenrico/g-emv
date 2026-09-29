"""[P5-5B · B4+B5+B6] Las formas del consejero, por la puerta ancha honesta.

En seco, coste cero: aqui ya no se llama a nadie, se juzga lo guardado.
Regla: E1+G2, margen 0,02, comparador en ventana, hermano leido de su diario,
filas de rivales a piso. La MISMA de P5-3H, sin tocar una linea de `forma.py`.
"""
from __future__ import annotations
import collections, copy, json, os, random, sys, time

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                      # noqa: E402
from serie_util import D, DOV                               # noqa: E402
from alma import appraisal_zs_v42_exp as V42                # noqa: E402
import banco_llaves as B, banco_forma3 as BF, forma as F    # noqa: E402
import proyeccion as P, alcance_g as AL                     # noqa: E402
import traductor_forma as TF                                # noqa: E402

HOR, MARGEN, DIMS = 100, 0.02, ("vida", "manos", "vinculo")
EJE = {"vida": "F", "manos": "R", "vinculo": "S"}
EPS = 1e-6
BRAZOS = [("formas", "haiku"), ("casillas", "haiku"), ("formas", "sonnet")]
PROG = open(os.path.join(AQUI, "P55B_progreso.log"), "a", buffering=1)


def avisa(s):
    print(s, flush=True)
    PROG.write(s + "\n")


def necesidades(o, mundo, mem, tic):
    """(nF, nR, nS) y las filas crudas, en ese punto."""
    try:
        st, radio = V42.appraise(o, mundo, mem, tic)
    except Exception:
        return None, {}
    filas = {k: (v.get("M") if isinstance(v, dict) else v)
             for k, v in (radio.get("filas") or {}).items()}
    return (st.nF, st.nR, st.nS), filas


def curva_con_necesidades(e0, obs_w, tramos, mundo, mem, suelo, tics,
                          herm, dia_h, pisos):
    """Como `forma.curva_H`, pero apuntando tambien las necesidades y filas
    en cada punto de control, que es lo que B5 necesita."""
    e = F.copia_estado(e0)
    suelo_act = dict(suelo)
    out = []
    for i, tic in enumerate(tics):
        K = tic - e["tick"]
        if K < 0:
            continue
        tr = tramos[i] if i < len(tramos) else {"destino": None,
                                                "intencion": "esperar"}
        plan = {"destino": tr.get("destino"),
                "coger": tr.get("intencion") == "coger",
                "usar": tr.get("item") if tr.get("intencion") == "usar" else None}
        e = P.proyectar_rapido(e, plan, K, mundo, suelo_act)
        if tr.get("intencion") == "coger":
            suelo_act.pop(tuple(tr.get("destino") or ()), None)
        o = F.foto_rapida(obs_w, e, mundo, tic, list(suelo_act.values()))
        m = mem
        if dia_h is not None:
            o, m = AL.pon_hermano(o, mem, herm, dia_h.get(tic),
                                  tuple(e["pos"]), mundo)
        nec, filas = necesidades(o, mundo, m, tic)
        out.append({"tic": tic, "d": F._d2(o, mundo, m, tic, pisos),
                    "vida": e["hp"], "W": e.get("W"), "pos": tuple(e["pos"]),
                    "nec": nec, "filas": filas})
    return out


def pon_item(tramos, estado, suelo):
    """«usar» sin decir que: se resuelve como lo resolveria el cuerpo — la cura
    que lleve encima, botiquin antes que racion. Declarado, no inventado: son
    los dos unicos usables de `proyeccion.CURA`."""
    lleva = [ (s or {}).get("id") for s in (estado.get("pack") or []) ]
    for tr in tramos:
        if tr.get("intencion") != "usar" or tr.get("item"):
            continue
        d = tr.get("destino")
        en_suelo = (suelo.get(tuple(d)) or {}).get("id") if d else None
        if en_suelo in P.CURA:
            tr["item"] = en_suelo
        elif "first_aid" in lleva:
            tr["item"] = "first_aid"
        elif "rations" in lleva:
            tr["item"] = "rations"
        else:
            tr["intencion"] = "esperar"      # no hay nada que usar
            tr["esperar"] = tr.get("esperar") or 11


def signo(antes, ahora):
    """El cuerpo: si la NECESIDAD baja, la dimension MEJORA."""
    if antes is None or ahora is None:
        return None
    if ahora < antes - EPS:
        return "+"
    if ahora > antes + EPS:
        return "-"
    return "0"


def main():
    D.A = V42
    U.pon(False)
    escenas = {e["id"]: e for e in
               json.load(open(os.path.join(AQUI, "P55B_escenas.json")))}
    crudas = collections.defaultdict(dict)
    for brazo, modelo in BRAZOS:
        p = os.path.join(AQUI, f"P55B_crudas_{brazo}_{modelo}.jsonl")
        if not os.path.exists(p):
            avisa(f"[B4] falta {os.path.basename(p)}")
            continue
        for linea in open(p, encoding="utf-8"):
            try:
                r = json.loads(linea)
            except Exception:
                continue
            crudas[(brazo, modelo)][r["escena"]] = r
        avisa(f"[B4] {brazo}/{modelo}: {len(crudas[(brazo,modelo)])} respuestas")

    cajas = collections.defaultdict(collections.Counter)
    trad = collections.defaultdict(collections.Counter)
    coher = collections.defaultdict(collections.Counter)
    prop = collections.defaultdict(collections.Counter)
    ms_por = collections.defaultdict(list)
    porfich = collections.defaultdict(list)
    for e in escenas.values():
        porfich[e["fichero"]].append(e)

    rnd_az = random.Random(20260919)
    for n, (fich, xs) in enumerate(sorted(porfich.items()), 1):
        f = os.path.join(RAIZ, "paintball", "runs", "S2_A", fich)
        recs = list(U.lee(f))
        pc = next(r for r in recs if r.get("k") == "player_config")
        sm = next(r for r in recs if r.get("k") == "static_map")
        cat = next(r for r in recs if r.get("k") == "catalogo")
        B.pon_v42(B.interruptores(recs))
        filas_m = list(sm["filas"])
        mundo = U.mundo_de(pc, filas_m, cat["items"])
        slot, herm = pc.get("slot"), pc.get("teammate_slot")
        otro = f.replace(f"policy_agent_{slot}", f"policy_agent_{herm}")
        dia_h = ({rr["tick"]: rr for rr in U.lee(otro)
                  if rr.get("k") == "tick" and rr.get("phase") == "live"}
                 if os.path.exists(otro) else None)
        tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
        quiero = {x["w"] for x in xs}
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
            if t in quiero:
                ctxs[t] = (r, o, pre, copy.deepcopy(blo))

        for esc in xs:
            w = esc["w"]
            if w not in ctxs:
                continue
            rw, ow, memw, blw = ctxs[w]
            ew = P.estado_de(rw)
            suelow = {tuple(it["pos"]): it for it in (rw.get("ve_items") or [])
                      if it.get("pos")}
            pisos = F.pisos_rival(ow, mundo, memw, w)
            base = list(D.candidatos(ow, mundo, copy.deepcopy(memw), w,
                                     copy.deepcopy(blw)))

            trabajos = []
            for (brazo, modelo), d in crudas.items():
                r = d.get(esc["id"])
                if r is None or r.get("error") or not r.get("texto"):
                    trad[(brazo, modelo)]["sin respuesta"] += 1
                    continue
                ms_por[(brazo, modelo)].append(r.get("ms") or 0)
                fn = TF.traduce if brazo == "formas" else TF.de_propuestas
                formas, inf = fn(r["texto"], esc, filas_m,
                                 trad[(brazo, modelo)])
                if inf["callar"]:
                    prop[(brazo, modelo)]["calla"] += 1
                prop[(brazo, modelo)]["respuestas"] += 1
                prop[(brazo, modelo)]["formas"] += len(formas)
                for fo in formas:
                    prop[(brazo, modelo)][f"tramos:{len(fo['tramos'])}"] += 1
                    for tr in fo["tramos"]:
                        prop[(brazo, modelo)][f"intencion:{tr['intencion']}"] += 1
                        if tr["destino"] is None:
                            prop[(brazo, modelo)]["quedarse"] += 1
                    trabajos.append(((brazo, modelo), fo))

            if esc["buena"]:
                tr_d = BF.tramos_reales(tk, esc["t"], HOR)
                trabajos.append((("despues", "-"), {"tramos": tr_d}))
                pasos = F.cheb(tuple(rw.get("pos") or ()),
                               tr_d[-1]["destino"])
                z = BF.casilla_a(filas_m, tuple(rw.get("pos") or ()),
                                 max(1, pasos), rnd_az)
                if z:
                    trabajos.append((("azarp", "-"), {"tramos": [
                        {"destino": tuple(z), "intencion": "ir"},
                        {"destino": None, "intencion": "esperar",
                         "esperar": max(0, HOR - F.cheb(
                             tuple(rw.get("pos") or ()), z) * P.PASO_TICS)}]}))

            for llave, fo in trabajos:
                tramos = (TF.solo_tramos(fo) if "_mitad" in
                          (fo["tramos"][0] if fo["tramos"] else {})
                          else fo["tramos"])
                if llave[0] in ("formas", "casillas"):
                    pon_item(tramos, ew, suelow)
                tics = [x[0] for x in F.puntos_de_control(ew, tramos)]
                if not tics:
                    cajas[llave]["sin puntos de control"] += 1
                    continue
                cajas[llave]["construidas"] += 1
                try:
                    cf = curva_con_necesidades(ew, ow, tramos, mundo, memw,
                                               suelow, tics, herm, dia_h, pisos)
                    cs, quien, ncd, mueve = F.mejor_propia_H(
                        ew, ow, base, tics, mundo, memw, suelow, w, herm,
                        dia_h, pisos)
                except Exception:
                    cajas[llave]["revienta"] += 1
                    continue
                if cs is None:
                    cajas[llave]["sin comparador"] += 1
                    continue
                # ── B5: la mitad emocional, contra lo que el cuerpo proyecta
                if llave[0] == "formas":
                    ant = None
                    for i, punto in enumerate(cf):
                        tr = fo["tramos"][i] if i < len(fo["tramos"]) else None
                        if tr is None or punto["nec"] is None:
                            continue
                        if ant is not None:
                            for j, dim in enumerate(DIMS):
                                dicho = (tr.get("_mitad") or {}).get(dim)
                                real = signo(ant[j], punto["nec"][j])
                                if dicho not in ("+", "0", "-") or real is None:
                                    coher[(llave, dim)]["sin decir"] += 1
                                    continue
                                coher[(llave, dim)]["comparadas"] += 1
                                coher[(llave, dim)]["acierta" if dicho == real
                                                    else "falla"] += 1
                            por = tr.get("_por")
                            if por:
                                coher[(llave, "por")]["nombrados"] += 1
                                a = (cf[i - 1]["filas"] or {}).get(por)
                                b = (punto["filas"] or {}).get(por)
                                if por not in V42.REPARTO:
                                    coher[(llave, "por")]["renglon inventado"] += 1
                                elif a is None or b is None:
                                    coher[(llave, "por")]["sin dato"] += 1
                                elif abs((a or 0.0) - (b or 0.0)) > EPS:
                                    coher[(llave, "por")]["de verdad cambia"] += 1
                                else:
                                    coher[(llave, "por")]["no cambia"] += 1
                        ant = punto["nec"]
                # ── B4: la regla y la mesa
                ver, ar, dt = F.juzga_margen(cf, cs, w, margen=MARGEN)
                if ver != "ok":
                    cajas[llave]["rechazada_" + ver] += 1
                    continue
                d0 = tramos[0].get("destino")
                if d0 is None:
                    cajas[llave]["coincide"] += 1
                    continue
                caja, info = BF.compite(f"_FM_ir_{d0[0]}_{d0[1]}",
                                        BF.a_ir(d0, ow, memw), ar, ow, mundo,
                                        memw, blw, w, "")
                cajas[llave][caja] += 1
        avisa(f"[B4 {n}/{len(porfich)}] {fich[:26]} · {len(xs)} escenas")
        del recs, ctxs

    salida = {
        "cajas": {f"{a}/{b}": dict(c) for (a, b), c in cajas.items()},
        "traduccion": {f"{a}/{b}": dict(c) for (a, b), c in trad.items()},
        "coherencia": {f"{a[0]}/{a[1]}|{d}": dict(c)
                       for (a, d), c in coher.items()},
        "propone": {f"{a}/{b}": dict(c) for (a, b), c in prop.items()},
        "ms": {f"{a}/{b}": (sorted(v)[len(v) // 2] if v else None)
               for (a, b), v in ms_por.items()},
    }
    json.dump(salida, open(os.path.join(AQUI, "P55B_banco.json"), "w"),
              ensure_ascii=False, indent=1)
    avisa("[B4] guardado P55B_banco.json")
    for k, v in salida["cajas"].items():
        avisa(f"  {k}: {v}")


if __name__ == "__main__":
    main()

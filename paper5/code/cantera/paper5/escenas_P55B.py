"""[P5-5B · B0] Las escenas que se le van a contar al consejero.

En seco, coste cero. Nada se llama todavia.

MISMAS escenas que el banco de P5-3/P5-4: los 40 diarios de S2_A de la semilla
del banco, tics vivos >= 300 multiplos de 50. Una escena es «de O-despues» si
`d(t+100) < d(t)`, que es la definicion que el banco usa para «hay un futuro
bueno conocido».

Lo que se guarda por escena es lo que el consejero va a recibir, y es lo MISMO
para los dos brazos (lo unico que cambia entre brazos es la instruccion y el
esquema de salida):

  1. el relato de la escena, armado con `relator_t5.relato(e, True)`, que es el
     del brazo C del cuatro (con el bloque de dolores);
  2. los seis numbers del cuerpo (necesidad y tono de los tres ejes);
  3. el registro del hermano en ese tic (posicion, vida, si esta herido).

El manual M2 va aparte, en el bloque cacheado, porque es igual en las 200.
"""
from __future__ import annotations
import collections, copy, glob, hashlib, json, os, random, sys

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                      # noqa: E402
from serie_util import D, DOV                               # noqa: E402
from alma import appraisal_zs_v42_exp as V42                # noqa: E402
from alma import relator_t5 as RT                           # noqa: E402
import banco_llaves as B, forma as F, proyeccion as P       # noqa: E402

HOR, DESDE, CADA = 100, 300, 50
N_BUENAS, N_OTRAS = 100, 100      # [decision de mesa] dos modelos, menos escenas
SEMILLA_ESC = 20260919
SAL = os.path.join(AQUI, "P55B_escenas.json")
PROG = open(os.path.join(AQUI, "P55B_progreso.log"), "a", buffering=1)


def avisa(s):
    print(s, flush=True)
    PROG.write(s + "\n")


def golpe_hermano(obs, mundo, herm):
    """[P5-5B] Copia literal de `policy_cortex._golpe_hermano` (:746-780), que
    el campo SI ponia en `e` y sin la cual el relato no sale byte a byte."""
    you = obs.get("you") or {}
    hid = (you.get("hand") or {}).get("id")
    arma = mundo.items.get(hid) if hid else None
    if arma is None or arma.damage <= 0:
        return None
    pos = tuple(you.get("pos") or ())
    ag = (obs.get("visible") or {}).get("agents") or []
    a = next((x for x in ag if x.get("slot") == herm and x.get("pos")), None)
    if a is None or not pos:
        return None
    q = tuple(a["pos"]); dx, dy = q[0] - pos[0], q[1] - pos[1]
    if not (dx == 0 or dy == 0 or abs(dx) == abs(dy)):
        return None
    if max(abs(dx), abs(dy)) > arma.range:
        return None
    d = D._dir_hacia(pos, q)
    ocup = {tuple(x["pos"]): x for x in ag if x.get("pos")}
    ddx, ddy = D.DIRS[d]; p = pos
    for _ in range(arma.range):
        p = (p[0] + ddx, p[1] + ddy)
        if mundo.solido(p[0], p[1]):
            return None
        if p in ocup:
            if ocup[p].get("slot") != herm:
                return None
            break
    return ({"nombre": f"atacar_{d}",
             "frase": (f"atacar hacia el {RT.DIRX.get(d, d)} con "
                       f"{RT.ELCOSA.get(hid, hid)}; el primero en esa "
                       f"linea es tu hermano")},
            {"tipo": "atacar", "dir": d, "objetivo": herm, "arma": arma})


def escena_ctx(r, o, mem, blo, mundo, tick, herm):
    """La `e` del relator, igual que `cantera/paper4/reconstruye_C.py:27`."""
    cands = D.candidatos(o, mundo, copy.deepcopy(mem), tick, copy.deepcopy(blo))
    recetas, vivas = {}, {}
    for n, rc in cands:
        vivas[n] = dict(rc)
        recetas[n] = {"tipo": rc.get("tipo"), "dir": rc.get("dir"),
                      "destino": list(rc["destino"]) if rc.get("destino") else None,
                      "objetivo": rc.get("objetivo"),
                      "item": ((rc.get("item") or {}).get("id")
                               if isinstance(rc.get("item"), dict)
                               else rc.get("item"))}
    _a, radio = D.decide(o, mundo, copy.deepcopy(mem), tick, copy.deepcopy(blo))
    vis = o.get("visible") or {}
    e = {"r": r, "pc_teammate": herm, "recetas": recetas,
            "cuerpo": {k: {"d": v["d"], "movs": v.get("movs")}
                       for k, v in radio["candidatos"].items()},
            "cert": V42.agresor_de_la_hermana(o, mundo, mem, tick),
            "parte_fresco": (None if mem.parte_fresco(tick) is None
                             else int(tick - mem.parte_fresco(tick)["t"])),
            "agresores_det": (radio.get("ahora") or {}).get("agresores") or [],
            "_recetas_vivas": vivas,
            "_cuerpos": frozenset(tuple(a.get("pos") or ()) for a in
                                  (vis.get("agents") or []) if a.get("pos")),
            "_objetos": dict(mem.objetos_vistos)}
    gh = golpe_hermano(o, mundo, herm)
    if gh is not None:
        e["_golpe_hermano"] = gh[0]
        e["_receta_golpe_hermano"] = gh[1]
    return e


def seis_numeros(o, mundo, mem, tick):
    """Necesidad y tono de los tres ejes: los seis numeros del cuerpo."""
    st, _radio = V42.appraise(o, mundo, mem, tick)
    return {"necesidad_cuerpo": round(st.nF, 4), "tono_cuerpo": round(st.pF - st.nF, 4),
            "necesidad_recursos": round(st.nR, 4), "tono_recursos": round(st.pR - st.nR, 4),
            "necesidad_vinculo": round(st.nS, 4), "tono_vinculo": round(st.pS - st.nS, 4)}


def bloque_cuerpo(seis):
    return "\n".join([
        "**Como esta tu cuerpo ahora, en sus seis numeros** "
        "(la necesidad va de 0 a 1: cuanto mas alta, peor; el tono es lo bueno "
        "menos lo malo):", "",
        f"  - la vida y el peligro: necesidad {seis['necesidad_cuerpo']:.3f}, "
        f"tono {seis['tono_cuerpo']:+.3f}",
        f"  - lo que llevas en las manos: necesidad {seis['necesidad_recursos']:.3f}, "
        f"tono {seis['tono_recursos']:+.3f}",
        f"  - el vinculo con tu hermano: necesidad {seis['necesidad_vinculo']:.3f}, "
        f"tono {seis['tono_vinculo']:+.3f}"])


def bloque_hermano(rh):
    if rh is None:
        return ("**Tu hermano**: no hay registro suyo en este instante "
                "(no esta vivo o no hay diario).")
    hp = rh.get("hp")
    band = ("entero" if hp is not None and hp >= 95 else
            "tocado" if hp is not None and hp > 25 else "en las ultimas")
    dan = "si" if rh.get("damage_taken") else "no"
    return ("**Tu hermano, de su propio registro en este instante**: "
            f"esta en la casilla ({rh['pos'][0]},{rh['pos'][1]}), con {hp} de "
            f"vida ({band}); le han pegado en este instante: {dan}.")


def main():
    D.A = V42
    U.pon(False)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
    avisa(f"[B0] diarios {len(idx)} de {len(fs)} · semilla del banco {B.SEMILLA}")

    todas = []
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
                 if os.path.exists(otro) else {})
        vivos = [r for r in recs if r.get("k") == "tick"
                 and r.get("phase") == "live"]
        vivo = {r["tick"] for r in vivos}
        mri = {r["tick"]: (r.get("move_ready_in") or 0) for r in vivos}
        d_t = {}
        for r in vivos:
            R = r.get("RADIOGRAFIA") or {}
            c = (R.get("candidatos") or {}).get(R.get("elegido"))
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        esc = [r["tick"] for r in vivos
               if r["tick"] >= DESDE and r["tick"] % CADA == 0]
        quiero = set(esc)
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
        for t in sorted(esc):
            if t not in ctxs:
                continue
            w = next((u for u in range(t, t + HOR + 1)
                      if u in vivo and mri.get(u, 1) == 0), None)
            if w is None:
                continue
            t2 = t + HOR
            buena = bool(t2 in vivo and d_t.get(t2) is not None
                         and d_t.get(t) is not None and d_t[t2] < d_t[t])
            todas.append({"fichero": os.path.basename(f), "slot": slot,
                          "herm": herm, "t": t, "w": w, "buena": buena})
        avisa(f"[B0 {orden}/40] {os.path.basename(f)[:26]} · "
              f"escenas {len(esc)} · acumuladas {len(todas)}")
        del recs, ctxs

    buenas = [x for x in todas if x["buena"]]
    otras = [x for x in todas if not x["buena"]]
    avisa(f"[B0] escenas totales {len(todas)} · con futuro bueno {len(buenas)} "
          f"· sin el {len(otras)}")
    rnd = random.Random(SEMILLA_ESC)
    sel = (rnd.sample(buenas, min(N_BUENAS, len(buenas)))
           + rnd.sample(otras, min(N_OTRAS, len(otras))))
    sel.sort(key=lambda x: (x["fichero"], x["t"]))
    avisa(f"[B0] elegidas {len(sel)} ({min(N_BUENAS,len(buenas))} buenas + "
          f"{min(N_OTRAS,len(otras))} otras) con semilla {SEMILLA_ESC}")

    # segunda pasada: solo los diarios que aportan escenas elegidas
    porfich = collections.defaultdict(list)
    for x in sel:
        porfich[x["fichero"]].append(x)
    salida = []
    for n, (fich, xs) in enumerate(sorted(porfich.items()), 1):
        f = os.path.join(RAIZ, "paintball", "runs", "S2_A", fich)
        recs = list(U.lee(f))
        pc = next(r for r in recs if r.get("k") == "player_config")
        sm = next(r for r in recs if r.get("k") == "static_map")
        cat = next(r for r in recs if r.get("k") == "catalogo")
        B.pon_v42(B.interruptores(recs))
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        slot, herm = pc.get("slot"), pc.get("teammate_slot")
        otro = f.replace(f"policy_agent_{slot}", f"policy_agent_{herm}")
        dia_h = ({rr["tick"]: rr for rr in U.lee(otro)
                  if rr.get("k") == "tick" and rr.get("phase") == "live"}
                 if os.path.exists(otro) else {})
        quiero = {x["t"] for x in xs}
        mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
        guardado = {}
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
                guardado[t] = (r, o, pre, copy.deepcopy(blo))
        for x in xs:
            t = x["t"]
            if t not in guardado:
                continue
            r, o, pre, bl = guardado[t]
            e = escena_ctx(r, o, pre, bl, mundo, t, herm)
            rel = RT.relato(e, True)
            seis = seis_numeros(o, mundo, pre, t)
            rh = dia_h.get(t)
            rh_min = (None if rh is None else
                      {"pos": list(rh.get("pos") or ()), "hp": rh.get("hp"),
                       "damage_taken": list(rh.get("damage_taken") or ())})
            suelo = [{"id": it.get("id"), "pos": list(it["pos"])}
                     for it in (r.get("ve_items") or []) if it.get("pos")]
            salida.append({
                "id": f"{fich[:18]}_{slot}_{t}",
                "fichero": fich, "slot": slot, "herm": herm,
                "t": t, "w": x["w"], "buena": x["buena"],
                "pos": list(r.get("pos") or ()), "hp": r.get("hp"),
                "suelo": suelo,
                "relato": rel, "relato_md5": hashlib.md5(rel.encode()).hexdigest(),
                "seis": seis,
                "bloque_cuerpo": bloque_cuerpo(seis),
                "bloque_hermano": bloque_hermano(rh_min),
                "hermano": rh_min})
        avisa(f"[B0 relato {n}/{len(porfich)}] {fich[:26]} · "
              f"{len(xs)} escenas · total {len(salida)}")
        del recs, guardado

    json.dump(salida, open(SAL, "w"), ensure_ascii=False, indent=1)
    nb = sum(1 for x in salida if x["buena"])
    avisa(f"[B0] GUARDADAS {len(salida)} escenas ({nb} con futuro bueno, "
          f"{len(salida)-nb} sin el) en {os.path.basename(SAL)}")
    largos = [len(x["relato"]) for x in salida]
    avisa(f"[B0] relato: mediana {sorted(largos)[len(largos)//2]} caracteres, "
          f"max {max(largos)}")


if __name__ == "__main__":
    main()

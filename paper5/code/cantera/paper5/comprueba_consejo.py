"""[P5-5A] Comprobar contra el diario lo que el consejero afirmo.

En seco, coste cero. Nada a la plataforma. No toca el motor ni la tabla.

CRITERIOS, declarados (ventana: los 100 tics siguientes al tic de la foto):
  · LLEGADA  acierto si en ALGUN tic de la ventana el rival esta A TIRO
             (cheb <= alcance del arma que lleva) o si al FINAL de la ventana
             esta MAS CERCA que al principio.
  · AUSENCIA acierto si al FINAL de la ventana esta MAS LEJOS que al principio,
             o si no lo ve NADIE en la segunda mitad de la ventana.
  · POSICION acierto si en algun tic de la ventana esta a <= 3 casillas de la
             casilla dicha (mismo criterio del banco, P5-4B).
  · HERMANO  acierto contra el diario DEL HERMANO: posicion a <= 3 casillas,
             o el estado dicho (tocado / en las ultimas / bajo ataque).
  · LINEA BASE «nadie se mueve»: para los MISMOS rival-tics, habria acertado
             decir «sigue donde estaba» = al final de la ventana esta a <= 3
             casillas de donde estaba en el tic de la foto.

NO COMPROBABLE: si nadie vuelve a ver al rival en la ventana no hay con que
comparar; esas afirmaciones se cuentan aparte y NO entran en la tasa.
"""
from __future__ import annotations
import json, os, sys, glob, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import clases_consejo as CC                                 # noqa: E402

RUNS = "paintball/runs"
VENT = 100
TOL = 3


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def carga_diario(f):
    """tick -> (pos, hp, {slot: (pos, hand, banda)}), solo lo que hace falta."""
    d = {}
    for line in open(f, encoding="utf-8"):
        if '"k": "tick"' not in line and '"k":"tick"' not in line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("k") != "tick":
            continue
        ve = {}
        for a in r.get("ve_agentes") or ():
            p = a.get("pos")
            if p:
                ve[a.get("slot")] = (tuple(p), a.get("hand") or "none",
                                     a.get("hp_band"))
        d[r.get("tick")] = (tuple(r.get("pos") or ()), r.get("hp"), ve,
                            list(r.get("damage_taken") or ()))
    return d


def visto(dyo, dh, slot, t):
    """Mejor noticia de ese slot en ese tic: la mia primero, si no la del hermano."""
    for d in (dyo, dh):
        r = d.get(t)
        if r and slot in r[2]:
            return r[2][slot]
    return None


def afirmaciones(resp, slot_yo, slot_h):
    """[(clase, trozo)] sin repetir, del texto entero de la respuesta."""
    txt = " ".join(p["accion"] + " " + p["motivo"] for p in resp["props"])
    c = CC.clasifica(txt, slot_h)
    out = []
    for k in ("LLEGADA", "AUSENCIA", "POSICION", "HERMANO"):
        vistos = set()
        for tr in c.get(k, ()):
            if tr in vistos:
                continue
            vistos.add(tr)
            out.append((k, tr))
    return out, c


def objetivos(trozo, dyo, dh, t0, slot_yo, slot_h):
    """Que rivales abarca la afirmacion, en el tic de la foto."""
    ns = [n for n in CC.rivales_nombrados(trozo)
          if n not in (slot_yo, slot_h)]
    if ns:
        return ns
    arma = CC.arma_nombrada(trozo)
    vis = {}
    for d in (dh, dyo):
        r = d.get(t0)
        if r:
            vis.update(r[2])
    cand = [s for s in vis if s not in (slot_yo, slot_h)]
    if arma:
        cand = [s for s in cand if vis[s][1] == arma] or cand
    return cand


def juzga(clase, trozo, slot, dyo, dh, t0, slot_yo, slot_h):
    """(veredicto, base) con veredicto en {'ok','mal','?'} y base igual."""
    r0 = dyo.get(t0)
    if not r0:
        return "?", "?"
    v0 = visto(dyo, dh, slot, t0)
    mipos0 = r0[0]
    tics = [t for t in range(t0 + 1, t0 + VENT + 1) if t in dyo or t in dh]
    vistas = [(t, visto(dyo, dh, slot, t)) for t in tics]
    vistas = [(t, v) for t, v in vistas if v]
    # linea base: «sigue donde estaba»
    base = "?"
    if v0 and vistas:
        tf, vf = vistas[-1]
        base = "ok" if cheb(vf[0], v0[0]) <= TOL else "mal"
    if clase == "POSICION":
        dicho = CC.coord_nombrada(trozo)
        if dicho is None:
            n = CC.casillas_nombradas(trozo)
            if n is None or not v0:
                return "?", base
            ok = cheb(mipos0, v0[0]) <= n + TOL and cheb(mipos0, v0[0]) >= max(0, n - TOL)
            return ("ok" if ok else "mal"), base
        if not vistas and not v0:
            return "?", base
        todas = ([(t0, v0)] if v0 else []) + vistas
        return ("ok" if any(cheb(v[0], dicho) <= TOL for _, v in todas)
                else "mal"), base
    if not v0 or not vistas:
        return "?", base
    d0 = cheb(mipos0, v0[0])
    if clase == "LLEGADA":
        for t, v in vistas:
            rt = dyo.get(t)
            if not rt:
                continue
            if cheb(rt[0], v[0]) <= CC.ALCANCE.get(v[1], 0):
                return "ok", base
        tf, vf = vistas[-1]
        rf = dyo.get(tf)
        if rf and cheb(rf[0], vf[0]) < d0:
            return "ok", base
        return "mal", base
    if clase == "AUSENCIA":
        tf, vf = vistas[-1]
        rf = dyo.get(tf)
        if rf and cheb(rf[0], vf[0]) > d0:
            return "ok", base
        tarde = [t for t in range(t0 + VENT // 2, t0 + VENT + 1)]
        if not any(visto(dyo, dh, slot, t) for t in tarde):
            return "ok", base
        return "mal", base
    return "?", base


def juzga_hermano(trozo, dyo, dh, t0):
    """Contra el diario del hermano. (veredicto, base)."""
    rh = dh.get(t0)
    if not rh:
        return "?", "?"
    dicho = CC.coord_nombrada(trozo)
    tics = [t for t in range(t0 + 1, t0 + VENT + 1) if t in dh]
    base = "?"
    if tics:
        base = "ok" if cheb(dh[tics[-1]][0], rh[0]) <= TOL else "mal"
    if dicho is not None:
        todas = [rh[0]] + [dh[t][0] for t in tics]
        return ("ok" if any(cheb(p, dicho) <= TOL for p in todas) else "mal"), base
    t = CC.llano(trozo)
    if any(w in t for w in ("en las ultimas", "va a morir", "se esta muriendo",
                            "no aguanta", "va a caer")):
        return ("ok" if (rh[1] is not None and rh[1] <= 25) else "mal"), base
    if any(w in t for w in ("herid", "tocad")):
        return ("ok" if (rh[1] is not None and rh[1] < 100) else "mal"), base
    if any(w in t for w in ("bajo ataque", "le estan pegando",
                            "lo estan atacando", "le pegan", "en peligro")):
        gol = any(dh[t_][3] for t_ in tics) or bool(rh[3])
        return ("ok" if gol else "mal"), base
    if "muert" in t:
        return ("ok" if (rh[1] is not None and rh[1] <= 0) else "mal"), base
    n = CC.casillas_nombradas(trozo)
    if n is not None and dyo.get(t0):
        return ("ok" if abs(cheb(dyo[t0][0], rh[0]) - n) <= TOL else "mal"), base
    return "?", base


def main():
    resp = collections.defaultdict(list)
    for line in open(os.path.join(AQUI, "P55A_respuestas.jsonl"),
                     encoding="utf-8"):
        d = json.loads(line)
        if d["ok"]:
            resp[(d["arm"], d["ereq"])].append(d)
    filas = []
    claves = sorted(resp)
    for i, (arm, ereq) in enumerate(claves, 1):
        dia = {}
        for s in (10, 11):
            f = f"{RUNS}/{arm}/{ereq}-policy_agent_{s}.art.log"
            dia[s] = carga_diario(f) if os.path.exists(f) else {}
        for d in resp[(arm, ereq)]:
            slot_yo = 10 if d["asiento"] == "agent_10" else 11
            slot_h = 11 if slot_yo == 10 else 10
            dyo, dh = dia[slot_yo], dia[slot_h]
            t0 = d["tick_foto"]
            afs, crudo = afirmaciones(d, slot_yo, slot_h)
            cierta_alguna = False
            det = []
            for clase, trozo in afs:
                if clase == "HERMANO":
                    ver, base = juzga_hermano(trozo, dyo, dh, t0)
                    obs = [slot_h]
                else:
                    obs = objetivos(trozo, dyo, dh, t0, slot_yo, slot_h)
                    vs, bs = [], []
                    for s in obs:
                        v, b = juzga(clase, trozo, s, dyo, dh, t0,
                                     slot_yo, slot_h)
                        vs.append(v); bs.append(b)
                    ver = ("ok" if "ok" in vs else ("mal" if "mal" in vs else "?"))
                    base = ("ok" if "ok" in bs else ("mal" if "mal" in bs else "?"))
                nuevo = clase in ("LLEGADA", "AUSENCIA")
                if clase == "POSICION":
                    dicho = CC.coord_nombrada(trozo)
                    if dicho and obs:
                        v0 = visto(dyo, dh, obs[0], t0)
                        nuevo = bool(v0) and cheb(v0[0], dicho) > TOL
                if clase == "HERMANO":
                    nuevo = bool(CC.clasifica(trozo, slot_yo).get("HERM_CAMBIO"))
                if ver == "ok":
                    cierta_alguna = True
                det.append({"clase": clase, "trozo": trozo, "ver": ver,
                            "base": base, "nuevo": nuevo, "obs": obs})
            filas.append({"arm": arm, "ereq": ereq, "asiento": d["asiento"],
                          "t0": t0, "clases": sorted(set(crudo) - {"HERM_CAMBIO"}),
                          "afs": det, "cierta": cierta_alguna,
                          "props": [{"regla": p["regla"], "clase_trad": p["clase_trad"],
                                     "cajas": p["cajas"], "gano": p["gano"],
                                     "nombre": p["nombre"]} for p in d["props"]]})
        print(f"[{i}/{len(claves)}] {arm} {ereq[:22]} · "
              f"{len(resp[(arm, ereq)])} respuestas", flush=True)
        del dia
    json.dump(filas, open(os.path.join(AQUI, "P55A_juicio.json"), "w"),
              ensure_ascii=False)
    print("TOTAL respuestas", len(filas),
          "afirmaciones", sum(len(f["afs"]) for f in filas))


if __name__ == "__main__":
    main()

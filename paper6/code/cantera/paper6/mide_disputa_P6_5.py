"""[P6-5 · 1] CUANTO CUESTAN DE VERDAD LAS DISPUTAS POR UN OBJETO.

SOLO LECTURA de los 40 diarios del brazo A1 de P6-4. Coste cero.

REGLA NUEVA DE MANEL, aplicada aqui: antes de construir contra un problema,
se mide cuanto dano hace de verdad.

QUE SE MIDE, y como se identifica la disputa SIN suponer nada:
  El objetivo de `ir_objeto` se reconstruye llamando al MISMO
  `decisor_zs._mejor_objeto` que lo eligio, sobre una memoria REPLICADA tic a
  tic desde el principio del episodio y con la MISMA inyeccion de los ojos
  (los partes E2 se releen del `chat` del diario y se pasan por `oyente2`).
  Hay DISPUTA cuando los dos hermanos, con las piernas listas en el mismo tic,
  eligen `ir_objeto` y `_mejor_objeto` les devuelve LA MISMA casilla.

  De cada disputa se sigue lo que paso despues:
   a) instantes que perdio el que llego SEGUNDO (tics entre la primera llegada
      a la casilla y la segunda; 0 si el segundo nunca llego)
   b) veces que el objeto DESAPARECIO sin que lo cogiera ninguno de los dos
      (se lo llevo un rival, o ardio)
   c) veces que lo cogio el que MENOS lo necesitaba: se compara, en el tic de
      la disputa, si cada uno lleva ya algo de esa clase.
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, RAIZ)
import serie_util as U
from serie_util import DOV
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A42
import parte2 as P2
import oyente2 as OY

NUESTROS = (10, 11)
SEGUIR = 600          # tics que se siguen tras la disputa


def clase(mundo, iid):
    return P2.clase_de(mundo, iid)


def lleva(reg, cls, mundo):
    """¿Lleva ya algo de esa clase? (el test simple y declarado de P6-2.)"""
    if cls == "arma":
        return reg["hand"] not in (None, "none")
    if cls == "botiquin":
        return reg["pack_n"].get(mundo.id_botiquin, 0) > 0
    if cls == "raciones":
        return any(reg["pack_n"].get(i, 0) for i in (mundo.id_raciones or []))
    if cls == "mochila":
        return reg["body"] not in (None, "none")
    if cls == "municion":
        return any(reg["pack_n"].get(i, 0)
                   for i in (getattr(mundo, "ammo_ids", None) or ()))
    return True


DISPUTAS, C = [], collections.Counter()
for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                          "P64_t[24]_A1_*"))):
    fs = {}
    for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
        sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
        if sl in NUESTROS:
            fs[sl] = f
    if len(fs) != 2:
        continue
    E = {}
    mundo = None
    for sl, f in fs.items():
        recs = list(U.lee(f))
        pc = next(r for r in recs if r.get("k") == "player_config")
        sm = next(r for r in recs if r.get("k") == "static_map")
        cat = next(r for r in recs if r.get("k") == "catalogo")
        if mundo is None:
            mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        m = A42.Memoria()
        blo = D.Bloqueos()
        obj, T, ult_parte, ultint = {}, {}, None, None
        for r in recs:
            if r.get("k") != "tick":
                continue
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            # LA MISMA INYECCION QUE HUBO: los partes E2 del hermano, del chat
            for mm in (r.get("chat") or []):
                if mm.get("channel") == "team" and mm.get("from") != sl \
                        and str(mm.get("text") or "").startswith("E2 "):
                    p = P2.parsea(mm["text"], mundo)
                    if p:
                        ult_parte = p
            if ult_parte is not None:
                o = OY.inyecta(o, t, mundo, ult_parte)
            m.observa(o, mundo, t)
            blo.actualiza(o, mundo, ultint, t)
            ultint = r.get("intencion")
            if r.get("phase") != "live":
                continue
            ra = r.get("RADIOGRAFIA") or {}
            pos = tuple(r.get("pos") or ())
            T[t] = {"pos": pos, "el": ra.get("elegido"),
                    "listas": int(r.get("move_ready_in") or 0) == 0,
                    "hand": (r.get("hand") or {}).get("id"),
                    "body": (r.get("body") or {}).get("id")
                            if isinstance(r.get("body"), dict) else r.get("body"),
                    "pack_n": {(s or {}).get("id"): int((s or {}).get("n") or 1)
                               for s in (r.get("pack") or []) if s},
                    "items": {(int(x["pos"][0]), int(x["pos"][1])): x.get("id")
                              for x in (r.get("ve_items") or []) if x.get("pos")}}
            if ra.get("elegido") == "ir_objeto" and pos:
                obj[t] = D._mejor_objeto(pos, mundo, m, o, t)
        E[sl] = {"T": T, "obj": obj}
        del recs
    a, b = NUESTROS
    for t in sorted(set(E[a]["obj"]) & set(E[b]["obj"])):
        pa, pb = E[a]["obj"][t], E[b]["obj"][t]
        if pa is None or pb is None:
            continue
        C["los dos en ir_objeto con objetivo legible"] += 1
        if tuple(pa) != tuple(pb):
            C["objetivos DISTINTOS"] += 1
            continue
        C["MISMO objetivo"] += 1
        DISPUTAS.append({"carp": os.path.basename(carp), "tick": t,
                         "casilla": list(pa),
                         "pos": {a: list(E[a]["T"][t]["pos"]),
                                 b: list(E[b]["T"][t]["pos"])}})
    # ── las consecuencias ────────────────────────────────────────────────
    for d in [x for x in DISPUTAS if x["carp"] == os.path.basename(carp)]:
        t0 = d["tick"]; cel = tuple(d["casilla"])
        iid = (E[a]["T"][t0]["items"].get(cel)
               or E[b]["T"][t0]["items"].get(cel))
        d["id"] = iid
        d["clase"] = clase(mundo, iid) if iid else None
        d["dist"] = {sl: max(abs(E[sl]["T"][t0]["pos"][0] - cel[0]),
                             abs(E[sl]["T"][t0]["pos"][1] - cel[1]))
                     for sl in NUESTROS}
        d["lleva"] = {sl: (lleva(E[sl]["T"][t0], d["clase"], mundo)
                           if d["clase"] else None) for sl in NUESTROS}
        llega = {}
        for sl in NUESTROS:
            for tt in range(t0, t0 + SEGUIR + 1):
                if tt in E[sl]["T"] and E[sl]["T"][tt]["pos"] == cel:
                    llega[sl] = tt
                    break
        d["llega"] = llega
        # ¿desaparecio sin que llegara ninguno?
        fuera = None
        for tt in range(t0, t0 + SEGUIR + 1):
            v = [E[sl]["T"][tt]["items"] for sl in NUESTROS if tt in E[sl]["T"]]
            if not v:
                continue
            if all(cel not in x for x in v) and any(x for x in v):
                fuera = tt
                break
        d["desaparece"] = fuera
    del E
    print(f"  {os.path.basename(carp)}: {C['MISMO objetivo']} disputas acumuladas",
          flush=True)

json.dump({"disputas": DISPUTAS, "recuento": dict(C)},
          open(os.path.join(AQUI, "P6_5_disputas.json"), "w"),
          ensure_ascii=False, indent=1)
print("\n", dict(C))
print(f"\n-> cantera/paper6/P6_5_disputas.json ({len(DISPUTAS)} disputas)")

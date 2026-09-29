"""[P5-3F · F2 y F3] De donde viene la mejora REAL de los futuros buenos.

Sin proyeccion: se llama a `A.filas()` en `t` y en `t+100` sobre lo que pasO de
verdad, y se reparte `d(t) - d(t+100)` por filas.

ATRIBUCION, declarada: `opponent_distance` NO es aditiva en las filas, asi que
se usa el reparto UNO A UNO: para cada fila, cuanto baja la `d` si SOLO esa
fila pasa de su valor en `t` al de `t+100`. La suma de los trozos no da el
total exacto; se reporta el residuo.
"""
from __future__ import annotations
import collections, copy, glob, json, os, random, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B, forma as F

HOR = 100
OTROS = set(F.PISO_OTROS)                      # las 15, tras la correccion
PROPIAS = {"R-ACOPIO", "R-CARENCIA", "R-LLAMADA"}
VIDA_ANILLO = {"F-DANO", "F-ANTICIPACION"}
MAPA = {"F-REENCUENTRO"}
PROG = open(os.path.join(AQUI, "P53F_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


def grupo(n):
    if n in OTROS:
        return "los otros"
    if n in PROPIAS:
        return "inventario y suelo"
    if n in VIDA_ANILLO:
        return "vida y anillo"
    if n in MAPA:
        return "memoria del mapa"
    return "otras"


def anda(fs, tanda, salida):
    D.A = V42
    U.pon(False)
    tot = collections.Counter()
    por_grupo = collections.Counter()
    manda_otros = 0
    n_fut = 0
    residuos = []
    for orden, f in enumerate(fs, 1):
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            continue
        B.pon_v42(B.interruptores(recs))
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        vivos = [r for r in recs if r.get("k") == "tick"
                 and r.get("phase") == "live"]
        vivo = {r["tick"] for r in vivos}
        d_t = {}
        for r in vivos:
            R = r.get("RADIOGRAFIA") or {}
            c = (R.get("candidatos") or {}).get(R.get("elegido"))
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        esc = [r["tick"] for r in vivos
               if r["tick"] >= 300 and r["tick"] % 50 == 0
               and (r["tick"] + HOR) in vivo
               and d_t.get(r["tick"]) is not None
               and d_t.get(r["tick"] + HOR) is not None
               and d_t[r["tick"] + HOR] < d_t[r["tick"]]]
        nec = set(esc) | {t + HOR for t in esc}
        guarda = {}
        mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
        for r in [x for x in recs if x.get("k") == "tick"]:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t)
            blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            pre = copy.deepcopy(mem)
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if (r.get("intencion") or {}).get("do") == "attack" \
                    or _el.startswith("atacar"):
                mem.ultimo_ataque = t
            if t in nec:
                guarda[t] = V42.filas(o, mundo, pre, t) or {}
        for t in esc:
            a, b = guarda.get(t), guarda.get(t + HOR)
            if not a or not b:
                continue
            da = F.d_con_pisos(a)
            db = F.d_con_pisos(b)
            mejora = da - db
            if mejora <= 0:
                continue
            n_fut += 1
            trozos = {}
            for nom in V42.REPARTO:
                if abs(float(a.get(nom) or 0.0) - float(b.get(nom) or 0.0)) < 1e-12:
                    continue
                mix = dict(a)
                mix[nom] = b.get(nom)
                trozos[nom] = da - F.d_con_pisos(mix)
            s = sum(trozos.values())
            residuos.append(abs(mejora - s) / max(1e-9, abs(mejora)))
            g = collections.Counter()
            for nom, v in trozos.items():
                g[grupo(nom)] += v
                tot[nom] += v
            for k, v in g.items():
                por_grupo[k] += v
            pos = sum(v for v in g.values() if v > 0)
            if pos > 0 and g.get("los otros", 0.0) / pos > 0.5:
                manda_otros += 1
        avisa(f"  [{orden}/{len(fs)}] {os.path.basename(f)[:40]} · futuros "
              f"buenos acumulados {n_fut}")
        del recs, guarda
    total = sum(v for v in por_grupo.values())
    pos_total = sum(v for v in por_grupo.values() if v > 0)
    out = {"tanda": tanda, "futuros buenos": n_fut,
           "reparto por grupo": {k: v for k, v in por_grupo.most_common()},
           "fraccion por grupo": {k: (v / pos_total if pos_total else None)
                                  for k, v in por_grupo.most_common()},
           "futuros en que los otros aportan mas de la mitad": manda_otros,
           "fraccion de esos": (manda_otros / n_fut) if n_fut else None,
           "residuo relativo de la atribucion, mediana":
               (sorted(residuos)[len(residuos) // 2] if residuos else None),
           "por fila": {k: v for k, v in tot.most_common(12)}}
    json.dump(out, open(os.path.join(AQUI, salida), "w"),
              ensure_ascii=False, indent=1)
    avisa(f"\n### {tanda} · futuros buenos {n_fut}")
    for k, v in por_grupo.most_common():
        avisa(f"   {k:20s} {v:+9.4f} = {100*v/pos_total:6.2f} % de lo positivo")
    avisa(f"   los otros aportan mas de la mitad en {manda_otros} de {n_fut} "
          f"= {100*manda_otros/max(1,n_fut):.2f} %")
    avisa(f"   residuo relativo de la atribucion, mediana: "
          f"{out['residuo relativo de la atribucion, mediana']:.4f}")
    avisa(f"   filas que mas aportan: "
          f"{ {k: round(v,4) for k,v in list(tot.most_common(6))} }")
    return out


def main():
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
    avisa("=== F2 · S-2 brazo A, 40 diarios ===")
    anda([fs[i] for i in idx], "S-2 brazo A (40)", "P53F_F2_S2.json")
    lentos = []
    for c in ("P5_B1", "P5_C2", "P5_C3"):
        lentos += sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", c,
                                                "*.art.log")))
    avisa("=== F3 · mundo lento, 6 asientos-partida ===")
    anda(lentos, "mundo lento (6)", "P53F_F3_lento.json")


if __name__ == "__main__":
    main()

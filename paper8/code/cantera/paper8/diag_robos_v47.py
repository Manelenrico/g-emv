"""[P8] Prompt 92, puntos 4 y 5 (diagnóstico, solo mirar), de las partidas de cierre (valle_taller_v46, RG46r y RG046r con los sabores, 40 días, 1001-1021):
  4. junto a la hermana herida (con peligro: una bestia a dos casillas o menos de ella o de la herida, o a la vista de ella; y sin peligro);
  5. los robos (un empujón que gana la que empuja y en el que la otra suelta comida):
     b) lo que la robada cree de la que le roba (su radar, radar_dia.json: cuerpo, recursos, vínculo) el día del robo y el siguiente, frente a cómo cambia lo que
        cree de las demás esos mismos días; y lo mismo en las que lo ven (a la vista de la fase);
     c) por criatura y partida: cuántos robos hace, y lo que recibe de las demás (comidas y medicinas dadas a ella), la parte de sus turnos con otra pegada, y,
        cuando empuja a una bestia, en cuántos de esos turnos otra empuja a la misma bestia; las dos que más roban de cada partida frente a las dos que menos.
   python3 diag_robos_v47.py -> markdown por pantalla"""
import gzip, json, os, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
T46 = "/Volumes/Mem G-EMV/valle_taller_v46"; SEM = range(1001, 1022); MUNDOS = ("abundancia", "normal", "sequia", "sequia_dura", "bestias_crian")
CFG = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); CR = CFG["criaturas"]; VF = CR["vista_por_fase"]; DIA = CFG["dia"]["turnos"]
cheb = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])); her = lambda a: a[0] + ("2" if a[1] == "1" else "1"); DIMS = ("cuerpo", "recursos", "vinculo")

def una(arg):
    v, mu, s = arg; d = os.path.join(T46, f"{v}_{mu}+sabores_s{s}_d40")
    RD = json.load(open(os.path.join(d, "radar_dia.json"))) if os.path.exists(os.path.join(d, "radar_dia.json")) else {}
    rad = {a: {e[0]: e[1] for e in L_} for a, L_ in RD.items()}
    C = Counter(); robos = []; por = defaultdict(Counter)
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["turno"]; bs = [tuple(b["pos"]) for b in (x.get("bestias") or [x["bestia"]]) if b.get("pos") is not None]
        vivas = {a: g for a, g in x["agentes"].items() if not g["cuerpo"]["muerta"]}
        contra = defaultdict(set)
        for a, g in vivas.items():
            p = tuple(g["pos"]); h = her(a)
            por[a]["turnos"] += 1; por[a]["pegada"] += any(y != a and cheb(p, tuple(gy["pos"])) <= 1 for y, gy in vivas.items())
            if h in vivas and vivas[h]["cuerpo"]["vida"] < CR["umbral_herida"]:
                hp = tuple(vivas[h]["pos"]); pel = any(cheb(b, hp) <= 2 or cheb(b, p) <= 2 or cheb(b, p) <= VF[x["fase"]] for b in bs)
                k = "peligro" if pel else "sin"; C["her_" + k] += 1; C["her_" + k + "_junto"] += cheb(p, hp) <= 1
            if g.get("accion") == "dar" and g.get("resultado") == "ok" and g.get("objetivo") in vivas: por[g["objetivo"]]["recibe"] += 1
            if g.get("accion") == "empujar" and str(g.get("objetivo", "")).startswith("bestia") and not str(g.get("resultado", "")).startswith("no:"): contra[g["objetivo"]].add(a)
        for ob, gr in contra.items():
            for a in gr: por[a]["contra_bestia"] += 1; por[a]["contra_bestia_acompanada"] += len(gr) > 1
        for e in x["eventos"]:
            if "empujon" in e and e.get("gana") == e["empujon"] and "comida" in (e.get("soltado") or []):
                a, b = e["empujon"], e["a"]; por[a]["roba"] += 1; por[b]["robada"] += 1; dia = t // DIA
                pb = tuple(x["agentes"][b]["pos"]); ven = [y for y, gy in vivas.items() if y not in (a, b) and cheb(tuple(gy["pos"]), pb) <= VF[x["fase"]]]
                robos.append({"a": a, "b": b, "dia": dia, "ven": ven, "hermana": b == her(a)})
    # b) los radares, el día del robo y el siguiente
    cambio = {"robada": defaultdict(list), "robada_control": defaultdict(list), "ven": defaultdict(list), "ven_control": defaultdict(list)}
    def delta(y, z, d0):
        r0, r1 = (rad.get(y) or {}).get(d0), (rad.get(y) or {}).get(d0 + 1)
        if r0 is None or r1 is None or z not in r0 or z not in r1: return None
        return {k: r1[z][k] - r0[z][k] for k in DIMS}
    for r in robos:
        for quien, lista in (("robada", [r["b"]]), ("ven", r["ven"])):
            for y in lista:
                dz = delta(y, r["a"], r["dia"])
                if dz:
                    for k in DIMS: cambio[quien][k].append(dz[k])
                for z in (rad.get(y) or {}).get(r["dia"], {}):
                    if z in (r["a"], y): continue
                    dc = delta(y, z, r["dia"])
                    if dc:
                        for k in DIMS: cambio[quien + "_control"][k].append(dc[k])
    return {"v": v, "mu": mu, "s": s, "C": dict(C), "robos": len(robos), "robos_hermana": sum(r["hermana"] for r in robos), "cambio": {k: dict(v_) for k, v_ in cambio.items()},
            "por": {a: dict(c) for a, c in por.items()}}


if __name__ == "__main__":
    with Pool(8) as p: R = p.map(una, [(v, mu, s) for v in ("RG46r", "RG046r") for mu in MUNDOS for s in SEM])
    by = defaultdict(list)
    for r in R: by[(r["v"], r["mu"])].append(r)
    pc = lambda a, b: f"{100 * a / b:.0f} %" if b else "—"; m = lambda X: sum(X) / len(X) if X else float("nan")
    print("## 4. Junto a la hermana herida (de los turnos con la hermana viva herida)\n\n| mundo | RG46r: con peligro · sin | RG046r: con peligro · sin |\n|---|---|---|")
    for mu in MUNDOS:
        f = lambda v: (lambda C: f"{pc(C['her_peligro_junto'], C['her_peligro'])} ({C['her_peligro']}) · {pc(C['her_sin_junto'], C['her_sin'])}")(sum((Counter(r["C"]) for r in by[(v, mu)]), Counter()))
        print(f"| {mu} | {f('RG46r')} | {f('RG046r')} |")
    print("\n## 5b. Lo que cree de la que roba, del día del robo al siguiente (media del cambio en su radar; «control»: el cambio de lo que cree de las demás esos días)\n\n| mundo | clase | robos (a la hermana) | la robada: cuerpo · recursos · vínculo | control | las que lo ven: cuerpo · recursos · vínculo | control |\n|---|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("RG46r", "RG046r"):
            L_ = by[(v, mu)]; agg = {k: defaultdict(list) for k in ("robada", "robada_control", "ven", "ven_control")}
            for r in L_:
                for k, dd in r["cambio"].items():
                    for dim, xs in dd.items(): agg[k][dim] += xs
            fm = lambda k: " · ".join(f"{m(agg[k][dim]):+.4f}" for dim in DIMS) + f" ({len(agg[k]['cuerpo'])})"
            print(f"| {mu} | {v} | {sum(r['robos'] for r in L_)} ({sum(r['robos_hermana'] for r in L_)}) | {fm('robada')} | {fm('robada_control')} | {fm('ven')} | {fm('ven_control')} |")
    print("\n## 5c. Las que más roban (las dos de cada partida con más robos) frente a las que menos (las dos con menos)\n\n| mundo | clase | robos por partida: las que más · las que menos | regalos que reciben (por partida) | turnos con otra pegada | contra una bestia, acompañada (de sus empujones a una bestia) |\n|---|---|---|---|---|---|")
    for mu in MUNDOS:
        for v in ("RG46r", "RG046r"):
            A = Counter(); B = Counter()
            for r in by[(v, mu)]:
                orden = sorted(r["por"], key=lambda a: (r["por"][a].get("roba", 0), a))
                for a in orden[-2:]: A.update(r["por"][a])
                for a in orden[:2]: B.update(r["por"][a])
            n = 2 * len(by[(v, mu)])
            print(f"| {mu} | {v} | {A['roba'] / n:.1f} · {B['roba'] / n:.1f} | {A['recibe'] / n:.1f} · {B['recibe'] / n:.1f} | {pc(A['pegada'], A['turnos'])} · {pc(B['pegada'], B['turnos'])} | "
                  f"{pc(A['contra_bestia_acompanada'], A['contra_bestia'])} ({A['contra_bestia']}) · {pc(B['contra_bestia_acompanada'], B['contra_bestia'])} ({B['contra_bestia']}) |")

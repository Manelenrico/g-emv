"""[P7-36, parte 1] POR QUE COGE LO INUTIL: en las 40 vidas de APRENDE de P7-34 (y, de paso, en las de TECHO y BORRADO), cada tic en que entra una red o un camuflaje en
el zurron/mano/cuerpo; la decision es la del tic anterior (la accion del tic t-1 se ve en la obs del tic t): que candidato gana (`RADIOGRAFIA.elegido`), con que d, la d de `noop`
y la diferencia; si es un EMPATE EXACTO con noop (|d_coger - d_noop| <= _TOL = 1e-9, el empate del desempate de la casa, que `noop` no puede ganar: N2a), si el paisaje es
DEGENERADO (max - min <= TIEBREAK_EPS = 1e-3) y, si no, cuanto gana coger a noop. -> P7_36_cogidas.json
  python3 analiza_P7_36.py"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, RAIZ)
from planificador.planificador_v1 import TIEBREAK_EPS, _TOL
GEAR = ("net", "camouflage")


def unidades(r, o):
    n = sum(int(s.get("n") or 1) for s in (r.get("pack") or []) if s and s.get("id") == o)
    if (r.get("hand") or {}).get("id") == o: n += 1
    b = r.get("body"); bid = b.get("id") if isinstance(b, dict) else b
    if bid == o: n += 1
    return n


def vida(carp, slot):
    f = glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log"))
    if not f: return []
    T = []
    for line in open(f[0], errors="replace"):
        if '"k":"tick"' not in line[:12]: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("phase") != "live": continue
        T.append((r["tick"], {o: unidades(r, o) for o in GEAR}, r.get("RADIOGRAFIA") or {}, r.get("intencion") or {}, r.get("action_result")))
    out = []
    for i in range(1, len(T)):
        for o in GEAR:
            if T[i][1][o] > T[i - 1][1][o]:
                t, _, ra, it, _ = T[i - 1]; C = {k: (v if not isinstance(v, dict) else v.get("d")) for k, v in (ra.get("candidatos") or {}).items()}
                el = str(ra.get("elegido") or ""); d_el = C.get(el); d_noop = C.get("noop"); d_coger = C.get("coger"); vals = [v for v in C.values() if v is not None]
                tipo = ("coger" if el == "coger" else "ir_curioso" if el == "ir_curioso" else "hacer_sitio" if el.startswith("hacer_sitio") else "otro")
                out.append({"tick_entra": T[i][0], "tick_decide": t, "cosa": o, "elegido": el, "tipo": tipo, "intencion": it.get("do"), "d_elegido": d_el, "d_noop": d_noop, "d_coger": d_coger, "n_cand": len(C),
                            "empate_exacto_con_noop": (d_coger is not None and d_noop is not None and abs(d_coger - d_noop) <= _TOL), "degenerado": (bool(vals) and max(vals) - min(vals) <= TIEBREAK_EPS),
                            "coger_gana_a_noop_por": ((d_noop - d_coger) if (d_coger is not None and d_noop is not None) else None), "empata_con_otro": sorted(k for k, v in C.items() if k not in ("coger",) and v is not None and d_coger is not None and abs(v - d_coger) <= _TOL)})
    return out


if __name__ == "__main__":
    R = {"vidas": [], "resumen": {}}
    for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P734_s*_d*_*"))):
        b = os.path.basename(c).split("_"); serie, dia, brazo = int(b[1][1:]), int(b[2][1:]), b[3]
        for sl in (10, 11):
            cg = vida(c, sl); R["vidas"].append({"serie": serie, "dia": dia, "brazo": brazo, "asiento": sl, "carpeta": os.path.basename(c), "cogidas": cg})
    for brazo in ("TECHO", "BORRADO", "APRENDE"):
        cg = [x for v in R["vidas"] if v["brazo"] == brazo for x in v["cogidas"]]
        tipos = collections.Counter(x["tipo"] for x in cg); el = collections.Counter(x["elegido"] for x in cg)
        gan = sorted(x["coger_gana_a_noop_por"] for x in cg if x["coger_gana_a_noop_por"] is not None)
        R["resumen"][brazo] = {"cogidas": len(cg), "por_tipo": dict(tipos), "por_elegido": dict(el.most_common(8)), "empate_exacto_con_noop": sum(1 for x in cg if x["empate_exacto_con_noop"]), "degenerado": sum(1 for x in cg if x["degenerado"]),
                              "empate_exacto_o_degenerado": sum(1 for x in cg if x["empate_exacto_con_noop"] or x["degenerado"]), "coger_gana_a_noop_por_cuartiles": ([gan[0], gan[len(gan) // 4], gan[len(gan) // 2], gan[3 * len(gan) // 4], gan[-1]] if gan else None),
                              "gana_a_noop_por_menos_de_0_01": sum(1 for g in gan if g < 0.01), "sin_noop_en_candidatos": sum(1 for x in cg if x["d_noop"] is None), "sin_coger_en_candidatos": sum(1 for x in cg if x["d_coger"] is None),
                              "empata_con_otro": collections.Counter(k for x in cg for k in x["empata_con_otro"]).most_common(5), "intencion": dict(collections.Counter(x["intencion"] for x in cg))}
    json.dump(R, open(os.path.join(AQUI, "P7_36_cogidas.json"), "w"), ensure_ascii=False, indent=1)
    for b, x in R["resumen"].items(): print(b, json.dumps(x, ensure_ascii=False)[:700])

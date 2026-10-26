"""[P7-65] EXPLORATORIO, posterior al sello (pedido por Manel el 16-oct): no cambia ningun PASA o NO PASA. EL EFECTO DE LA MENTIRA EN LA CONDUCTA, POR TIC.
  Tic comparable = tic con eleccion de verdad (2 o mas candidatos en la radiografia), con un botiquin a la vista (ve_items), que le cabe en la mochila (hueco libre o una pila de
  botiquines < 2) y, en el analisis principal, un rival a <= 4 casillas (ve_agentes que no son ella ni su hermana); aparte, los mismos tics SIN rival a <= 4.
  «Va hacia el botiquin» (definicion de este exploratorio) = elige ir_objeto o ir_curioso con un paso que le acerca (Chebyshev) al botiquin visible mas cercano, o elige coger estando
  encima de un botiquin.
  (a) con la falsa activa: criaturas que mienten, dias 8-20, y la situacion de la falsa (rival a <= 4 o golpe en los 48 tics anteriores; el fuego no se mira: aproximacion declarada).
      Puede haber a la vez una honesta de coger cargada (se cuentan los tics) y por eso se da tambien (a-limpia): solo las vidas-dia sin ninguna honesta de coger cargada.
  (b) sin ninguna invitacion de coger: vidas-dia sin ninguna invitacion COGER_* cargada: (b1) las mismas criaturas, dias 1-7; (b2) la prudente de MIENTE_UNA (razon honesta), dias 1-20.
  (a) por tercios de la confianza del cuerpo en la razon en ese tic (reconstruida: arranque del dia y cada evaluacion o contraste que la cambia); cortes = tercios de todos los tics (a).
  Por hermana; error tipico por criatura (serie x brazo x asiento): media de las fracciones por criatura y sd / raiz(n).
  python3 exploratorio_P7_65.py -> P7_65_exploratorio.json"""
import collections, glob, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI); sys.argv = sys.argv[:1]
import analiza_P7_65 as A
D = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0), "NE": (1, -1), "NW": (-1, -1), "SE": (1, 1), "SW": (-1, 1)}
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def cabe(pack): return any(s is None for s in pack) or any(isinstance(s, dict) and s.get("id") == "first_aid" and int(s.get("n") or 1) < 2 for s in pack)


def ticks(k, v):
    S, d, b, sl = k; f = glob.glob(os.path.join(RUNS, f"P765_s{S}_d{d}_{b}_*", f"*policy_agent_{sl}.art.log"))[0]
    conf = None; ult_golpe = -10 ** 9; out = []
    for l in open(f, errors="replace"):
        if l.startswith('{"k":"P7_54_arranque"'): conf = float((json.loads(l).get("confianza") or {}).get("cuerpo", 0.5))
        elif l.startswith('{"k":"P7_54_evaluada"') or l.startswith('{"k":"P7_62_evaluada"'): conf = float(json.loads(l)["confianza_despues"]["cuerpo"])
        elif l.startswith('{"k":"P7_62_contraste"') or l.startswith('{"k":"P7_57_contraste"'): conf = float(json.loads(l)["confianza_despues"])
        elif l.startswith('{"k":"tick"'):
            r = json.loads(l)
            if r.get("phase") != "live": continue
            t = r["tick"]
            if any(float(x.get("amount") or 0) > 0 for x in (r.get("damage_taken") or [])): ult_golpe = t
            R = r.get("RADIOGRAFIA") or {}
            if int(R.get("n_cand") or 0) < 2: continue
            pos = tuple(r.get("pos") or (0, 0)); kits = [tuple(it["pos"]) for it in (r.get("ve_items") or []) if it.get("id") == "first_aid" and it.get("pos")]
            if not kits or not cabe(r.get("pack") or []): continue
            riv = [cheb(pos, tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos") and a.get("slot") not in (sl, sl ^ 1)]
            el = R.get("elegido"); ac = R.get("accion") or {}; dk = min(cheb(pos, p) for p in kits); hacia = False
            if el == "coger" and dk == 0: hacia = True
            elif el in ("ir_objeto", "ir_curioso") and ac.get("dir") in D:
                dx, dy = D[ac["dir"]]; nuevo = (pos[0] + dx, pos[1] + dy); hacia = min(cheb(nuevo, p) for p in kits) < dk
            out.append({"rival": bool(riv and min(riv) <= 4), "golpe48": t - ult_golpe <= 48, "hacia": hacia, "conf": conf})
    return out


def grupo(k, v):
    S, d, b, sl = k; coger_cargada = any((not i.get("falsa")) and i["accion"] in A.COGER for i in v["inv"])
    if v["pos"] is not None: return "a"
    if (b, sl) == ("MIENTE_UNA", 11): return None if coger_cargada else "b2"
    if d <= 7 and not coger_cargada: return "b1"
    return None


def resumen(por_criatura):
    fr = [h / n for h, n in por_criatura.values() if n]
    if not fr: return {"criaturas": 0}
    return {"criaturas": len(fr), "tics": sum(n for _, n in por_criatura.values()), "media": round(st.mean(fr), 4), "ee": round(st.stdev(fr) / math.sqrt(len(fr)), 4) if len(fr) > 1 else None}


if __name__ == "__main__":
    filas = []
    for k, v in A.V.items():
        g = grupo(k, v)
        if g is None: continue
        coger_honesta = any((not i.get("falsa")) and i["accion"] in A.COGER for i in v["inv"])
        for x in ticks(k, v): filas.append({**x, "g": g, "criatura": (k[0], k[2], k[3]), "hermana": A.HERMANA[k[3]], "brazo": k[2], "coger_honesta_cargada": coger_honesta})
    # (a): la falsa activa = su situacion (rival a <= 4 o golpe en 48 tics)
    for x in filas: x["falsa_activa"] = x["g"] == "a" and (x["rival"] or x["golpe48"])
    confs = sorted(x["conf"] for x in filas if x["falsa_activa"] and x["rival"] and x["conf"] is not None); c1, c2 = confs[len(confs) // 3], confs[2 * len(confs) // 3]
    tercio = lambda c: "alta" if c >= c2 else ("media" if c >= c1 else "baja")
    def tabla(cond_rival):
        T = {}
        for etiqueta, sel in (("(a) falsa activa", lambda x: x["falsa_activa"]), ("(a-limpia) falsa activa, en vidas-dia sin ninguna honesta de coger cargada", lambda x: x["falsa_activa"] and not x["coger_honesta_cargada"]), ("(b1) mismas criaturas, dias 1-7, sin invitacion de coger", lambda x: x["g"] == "b1"),
                              ("(b2) prudente de MIENTE_UNA (razon honesta), sin invitacion de coger", lambda x: x["g"] == "b2")):
            for her, selh in (("valiente", lambda x: x["hermana"] == "valiente"), ("prudente de MIENTEN_DOS", lambda x: x["hermana"] == "prudente" and x["brazo"] == "MIENTEN_DOS"), ("prudente de MIENTE_UNA", lambda x: x["hermana"] == "prudente" and x["brazo"] == "MIENTE_UNA")):
                pc = collections.defaultdict(lambda: [0, 0])
                for x in filas:
                    if x["rival"] == cond_rival and sel(x) and selh(x): pc[x["criatura"]][0] += x["hacia"]; pc[x["criatura"]][1] += 1
                r = resumen(pc)
                if r.get("criaturas"): T[f"{etiqueta} · {her}"] = r
        return T
    R = {"cortes_confianza": {"baja_<": round(c1, 4), "alta_>=": round(c2, 4)}, "con_rival": tabla(True), "sin_rival": tabla(False), "tercios": {}}
    for her, selh in (("valiente", lambda x: x["hermana"] == "valiente"), ("prudente de MIENTEN_DOS", lambda x: x["hermana"] == "prudente")):
        for t in ("alta", "media", "baja"):
            pc = collections.defaultdict(lambda: [0, 0])
            for x in filas:
                if x["falsa_activa"] and x["rival"] and selh(x) and x["conf"] is not None and tercio(x["conf"]) == t: pc[x["criatura"]][0] += x["hacia"]; pc[x["criatura"]][1] += 1
            R["tercios"][f"{her} · confianza {t}"] = resumen(pc)
    R["tics_a_con_una_honesta_de_coger_cargada"] = {"si": sum(1 for x in filas if x["falsa_activa"] and x["rival"] and x["coger_honesta_cargada"]), "de": sum(1 for x in filas if x["falsa_activa"] and x["rival"])}
    json.dump(R, open(os.path.join(AQUI, "P7_65_exploratorio.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False, indent=1))

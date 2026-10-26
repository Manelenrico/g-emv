"""[P7-2] Las curvas de la creencia (punto 1), el sello S1-S4 y la sensibilidad (punto 4), sobre el diario P7_1_diario.json.
Cada asiento (10, 11) es una criatura; las 40 semillas en orden creciente son los dias 1..40; 20 ordenes al azar con
random.Random(SEMILLA_BARAJADO). Escribe P7_2_curvas.json y la tabla de creencias por tic para el banco (P7_2_creencias.json:
la creencia vigente en el momento de cada uso/ataque del orden natural, ANTES de vivir esa experiencia)."""
import json, os, random, statistics
from collections import defaultdict
from memoria_P7_2 import Creencia

AQUI = os.path.dirname(os.path.abspath(__file__)); SEMILLA_BARAJADO = 20261003; N_ORDENES = 20
CAT = {"botiquin": 50.0, "bow": 14.0, "blowgun": 4.0}
J = json.load(open(os.path.join(AQUI, "P7_1_diario.json")))

def filas():
    """(objeto, situacion, asiento, semilla, t, valor vivido) de cada fila cerrada del diario."""
    out = []
    for f in J["botiquin"]:
        if f["paso"]["resultado"] == "sin cerrar": continue           # sin resultado: no es experiencia (declarado)
        carp, slot = f["vida"].split("/"); v = f["paso"]["cura_real"] if f["paso"]["resultado"] == "completado" else 0.0
        out.append(("botiquin", "dentro" if f["situacion"]["dentro"] else "fuera", int(slot), int(carp.rsplit("_", 1)[1]), f["t"], float(v), carp))
    for f in J["arco_cerbatana"]:
        carp, slot = f["vida"].split("/"); v = f["paso"]["dano_hecho"] if f["paso"]["resultado"] == "ok" else 0.0
        out.append((f["arma"], "con municion" if f["situacion"]["municion_mochila"] > 0 else "sin municion", int(slot), int(carp.rsplit("_", 1)[1]), f["t"], float(v), carp))
    return out

F = filas()
# los 40 dias son las 40 semillas de las series (P7_1_medidas.json: las 80 vidas), tengan o no filas de diario
SEMILLAS = sorted({int(L["carpeta"].rsplit("_", 1)[1]) for L in json.load(open(os.path.join(AQUI, "P7_1_medidas.json")))["vidas"]})
assert len(SEMILLAS) == 40, len(SEMILLAS)
CLAVES = [("botiquin", "dentro"), ("botiquin", "fuera"), ("bow", "con municion"), ("bow", "sin municion"), ("blowgun", "con municion"), ("blowgun", "sin municion")]

def recorre(orden, asiento, olvido=0.95, peso=3.0, tabla=None):
    """Recorre los dias en `orden` (lista de semillas) para una criatura. Devuelve por clave la creencia al final de cada dia
    (indice de dia 1..40) y el numero de experiencias por dia. Si `tabla` no es None, apunta la creencia vigente antes de cada
    experiencia (para el banco)."""
    C = {k: Creencia(CAT[k[0]], olvido=olvido, peso_nacimiento=peso) for k in CLAVES}
    curva = {k: [] for k in CLAVES}; nexp = {k: [] for k in CLAVES}
    por_dia = defaultdict(list)
    for obj, sit, sl, sem, t, v, carp in F:
        if sl == asiento: por_dia[sem].append((t, obj, sit, v, carp))
    for d, sem in enumerate(orden, 1):
        cuenta = {k: 0 for k in CLAVES}
        for t, obj, sit, v, carp in sorted(por_dia.get(sem, [])):
            k = (obj, sit)
            if tabla is not None: tabla.append({"asiento": asiento, "carpeta": carp, "t": t, "objeto": obj, "situacion": sit, "dia": d, "b_antes": round(C[k].b(d), 4), "valor_vivido": v})
            C[k].vive(d, v); cuenta[k] += 1
        for k in CLAVES: curva[k].append(round(C[k].b(d), 4)); nexp[k].append(cuenta[k])
    return curva, nexp

def cruce(curva, cat, frac):
    return next((d for d, b in enumerate(curva, 1) if b < frac * cat), None)

if __name__ == "__main__":
    R = {"semilla_barajado": SEMILLA_BARAJADO, "n_ordenes": N_ORDENES, "dias": SEMILLAS, "catalogo": CAT, "filas": len(F), "sin_cerrar_excluidas": sum(1 for f in J["botiquin"] if f["paso"]["resultado"] == "sin cerrar"), "principal": {}, "sensibilidad": {}}
    rng = random.Random(SEMILLA_BARAJADO); ordenes = []
    for _ in range(N_ORDENES):
        o = list(SEMILLAS); rng.shuffle(o); ordenes.append(o)
    tabla = []
    for asiento in (10, 11):
        nat, nexp = recorre(SEMILLAS, asiento, tabla=tabla)
        azar = [recorre(o, asiento)[0] for o in ordenes]
        for k in CLAVES:
            cat = CAT[k[0]]; finales = [c[k][-1] for c in azar]
            techo = statistics.mean([v for obj, sit, sl, sem, t, v, carp in F if (obj, sit) == k and sl == asiento]) if any((obj, sit) == k and sl == asiento for obj, sit, sl, sem, t, v, carp in F) else None
            # S3: primera vida (dia natural) con >= 5 filas sin municion y la creencia al acabar ese dia
            d5 = next((d for d, c in enumerate(nexp[k], 1) if c >= 5), None)
            R["principal"][f"{k[0]}/{k[1]}/{asiento}"] = {
                "curva_natural": nat[k], "experiencias_por_dia": nexp[k], "experiencias_total": sum(nexp[k]), "dias_con_experiencia": sum(1 for c in nexp[k] if c),
                "banda_p10": [round(min(c[k][d] for c in azar), 4) for d in range(40)], "banda_p90": [round(max(c[k][d] for c in azar), 4) for d in range(40)],
                "banda_nota": "banda = minimo y maximo de los 20 ordenes por indice de dia",
                "final_natural": nat[k][-1], "final_natural_frac": round(nat[k][-1] / cat, 4), "finales_azar": finales, "finales_azar_frac": [round(x / cat, 4) for x in finales],
                "cruza_50": cruce(nat[k], cat, .5), "cruza_25": cruce(nat[k], cat, .25), "cruza_10": cruce(nat[k], cat, .1),
                "cruza_50_azar": [cruce(c[k], cat, .5) for c in azar], "cruza_25_azar": [cruce(c[k], cat, .25) for c in azar],
                "techo_media_real": round(techo, 4) if techo is not None else None, "suelo_catalogo": cat,
                "primer_dia_con_5_o_mas": d5, "creencia_al_acabar_ese_dia": nat[k][d5 - 1] if d5 else None}
    # el sello, S1-S4 (S5, S6 van en el banco)
    P = R["principal"]
    R["sello"] = {
        "S1": {k: {"natural_<25%": P[f"botiquin/fuera/{k}"]["final_natural_frac"] < .25, "ordenes_<25%": sum(1 for x in P[f"botiquin/fuera/{k}"]["finales_azar_frac"] if x < .25)} for k in (10, 11)},
        "S2": {k: {"natural_frac": P[f"botiquin/dentro/{k}"]["final_natural_frac"], "entre_40_y_80": .4 <= P[f"botiquin/dentro/{k}"]["final_natural_frac"] <= .8, "ordenes_entre_40_y_80": sum(1 for x in P[f"botiquin/dentro/{k}"]["finales_azar_frac"] if .4 <= x <= .8)} for k in (10, 11)},
        "S3": {f"{a}/{k}": {"primer_dia_con_5_o_mas": P[f"{a}/sin municion/{k}"]["primer_dia_con_5_o_mas"], "creencia_frac_al_acabar": (round(P[f"{a}/sin municion/{k}"]["creencia_al_acabar_ese_dia"] / CAT[a], 4) if P[f"{a}/sin municion/{k}"]["primer_dia_con_5_o_mas"] else None),
                            "cumple": (P[f"{a}/sin municion/{k}"]["creencia_al_acabar_ese_dia"] < .1 * CAT[a]) if P[f"{a}/sin municion/{k}"]["primer_dia_con_5_o_mas"] else None} for a in ("bow", "blowgun") for k in (10, 11)},
        "S4": {f"{a}/{k}": {"natural_frac": P[f"{a}/con municion/{k}"]["final_natural_frac"], "a_menos_del_25%": abs(P[f"{a}/con municion/{k}"]["final_natural_frac"] - 1) < .25, "ordenes_a_menos_del_25%": sum(1 for x in P[f"{a}/con municion/{k}"]["finales_azar_frac"] if abs(x - 1) < .25)} for a in ("bow", "blowgun") for k in (10, 11)}}
    # sensibilidad (despues del sello, senalada como tal): olvido 0,90 y 0,99; peso de nacimiento 1 y 10; orden natural
    for nombre, kw in (("olvido_0.90", {"olvido": .9}), ("olvido_0.99", {"olvido": .99}), ("nacimiento_1", {"peso": 1.0}), ("nacimiento_10", {"peso": 10.0})):
        R["sensibilidad"][nombre] = {}
        for asiento in (10, 11):
            c, _ = recorre(SEMILLAS, asiento, **kw)
            for k in CLAVES: R["sensibilidad"][nombre][f"{k[0]}/{k[1]}/{asiento}"] = {"final_frac": round(c[k][-1] / CAT[k[0]], 4), "cruza_50": cruce(c[k], CAT[k[0]], .5), "cruza_25": cruce(c[k], CAT[k[0]], .25)}
    json.dump(R, open(os.path.join(AQUI, "P7_2_curvas.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(tabla, open(os.path.join(AQUI, "P7_2_creencias.json"), "w"), indent=0)
    for k, v in R["principal"].items(): print(f"{k}: exp {v['experiencias_total']} ({v['dias_con_experiencia']} dias) · final {v['final_natural']} ({v['final_natural_frac']:.2f} del catalogo) · azar {min(v['finales_azar_frac']):.2f}-{max(v['finales_azar_frac']):.2f} · cruza 50% dia {v['cruza_50']}, 25% dia {v['cruza_25']} · techo {v['techo_media_real']}")
    print("SELLO:", json.dumps(R["sello"])); print("sensibilidad:", json.dumps(R["sensibilidad"])[:1500]); print("tabla de creencias:", len(tabla))

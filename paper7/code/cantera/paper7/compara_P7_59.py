"""[P7-59] COMPARA la razon con nombres (P7-54, P7_54_razon.json) y a ciegas (P7-59, P7_59_razon.json), invitacion a invitacion, sobre los mismos 8 criatura-dias:
  - verdad en el mundo: la tabla del mundo del sello de P7-56 (analiza_P7_56.verdad: accion real x situacion x promesa de cuerpo);
  - condiciones descubiertas (mecanicas, por campos y texto): C1 el botiquin/la racion curan solo sin golpes (USAR_A/B con calma=CALMA, o el porque habla de golpes/corte); C2 fuera del
    anillo se pierde vida (el porque nombra el anillo y fuera/borde, o la situacion pide DENTRO para quedarse); C3 red y camuflaje no hacen nada en el cuerpo (promesa 0 para C/D);
    C4 el camuflaje protege quieta (PONERSE_D con QUIETA); C5 el botiquin cura mucho (promesa de cuerpo >= 25 al usar A);
  - por criatura-dia, las parejas (accion real, condicion) de P7-54 que desaparecen a ciegas, y las nuevas.  python3 compara_P7_59.py -> P7_59_compara.json"""
import json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
src = open(os.path.join(AQUI, "analiza_P7_56.py")).read(); ns = {}; exec(src[src.index("def verdad"):src.index("\n\n\ndef vida")], ns); verdad = ns["verdad"]
A = json.load(open(os.path.join(AQUI, "P7_54_razon.json"))); B = json.load(open(os.path.join(AQUI, "P7_59_razon.json")))
def conds(p):
    a = p["accion"]; t = (p.get("porque", "") + " " + p.get("se_comprueba", "")).lower(); c = set()
    if a in ("USAR_BOTIQUIN", "USAR_RACION") and (p["calma"] == "CALMA" or re.search(r"golpe|cort", t)): c.add("C1 cura solo sin golpes")
    if re.search(r"anillo", t) and re.search(r"fuera|borde", t): c.add("C2 fuera del anillo duele")
    if a in ("COGER_RED", "EMPUNAR_RED", "COGER_CAMUFLAJE", "PONERSE_CAMUFLAJE") and p["cuerpo"] == 0: c.add("C3 red/camuflaje no curan")
    if a == "PONERSE_CAMUFLAJE" and p["movimiento"] == "QUIETA": c.add("C4 camuflaje protege quieta")
    if a == "USAR_BOTIQUIN" and p["cuerpo"] >= 25: c.add("C5 el botiquin cura mucho")
    return c
def resumen(R):
    inv = [dict(p, vida=f"s{r['serie']} d{r['dia']} {r['brazo']} a{r['slot']}") for r in R for p in r["invitaciones"]]
    for p in inv: p["verdad"] = verdad(p["accion"], {"anillo": p["anillo"], "calma": p["calma"]}, p["cuerpo"]); p["conds"] = sorted(conds(p))
    cc = {}
    for p in inv:
        for c in p["conds"]: cc[c] = cc.get(c, 0) + 1
    acc = {}
    for p in inv: acc[p["accion"]] = acc.get(p["accion"], 0) + 1
    return inv, {"invitaciones": len(inv), "verdad": sum(1 for p in inv if p["verdad"]), "condiciones": cc, "acciones": acc, "usd": round(sum(r["usd_supuesto"] for r in R), 4), "tokens": (sum(r["tokens_entrada"] for r in R), sum(r["tokens_salida"] for r in R))}
iA, rA = resumen(A); iB, rB = resumen(B)
por_vida = {}
for v in sorted({p["vida"] for p in iA}):
    a = {(p["accion"], c) for p in iA if p["vida"] == v for c in (p["conds"] or ["(sin condicion conocida)"])}; b = {(p["accion"], c) for p in iB if p["vida"] == v for c in (p["conds"] or ["(sin condicion conocida)"])}
    por_vida[v] = {"desaparecen": sorted(a - b), "nuevas": sorted(b - a), "con_nombres": len([p for p in iA if p["vida"] == v]), "a_ciegas": len([p for p in iB if p["vida"] == v])}
cura = sum(1 for r in B for p in r["invitaciones"] if p["accion"] in ("USAR_BOTIQUIN", "USAR_RACION") and p["cuerpo"] > 0)
lect = [r["lectura"][:300] for r in B]
R = {"con_nombres": rA, "a_ciegas": rB, "por_vida": por_vida, "a_ciegas_promete_cura_con_A_o_B": cura, "lecturas_a_ciegas": lect, "invitaciones_con_nombres": iA, "invitaciones_a_ciegas": iB}
json.dump(R, open(os.path.join(AQUI, "P7_59_compara.json"), "w"), ensure_ascii=False, indent=1)
print("con nombres", rA); print("a ciegas", rB); print("cura A/B", cura)
for v, x in por_vida.items(): print(v, "desaparecen", x["desaparecen"], "nuevas", x["nuevas"])

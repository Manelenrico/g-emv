"""[P7-59] LA RAZON A CIEGAS (pregunta de Discord: ¿cuanto de lo que "descubre" la razon viene de conocer los nombres?). Repite P7-54 (diario limpio y menu, mismo prompt y modelo,
mismos 8 criatura-dias) con UNA diferencia: los nombres de objetos, items y municiones se sustituyen por etiquetas neutras fijas, igual en el diario, en el prompt y en el menu.
  ETIQUETAS (fijas): botiquin = objeto A, racion = objeto B, red = objeto C, camuflaje = objeto D, mochila = objeto E, sword = F, spear = G, bow = H, blowgun = I, knives = J,
  arrows = K, darts = L. Las acciones del menu: USAR_A, USAR_B, COGER_A..COGER_D, EMPUNAR_C, PONERSE_D, DAR_A_HERMANA (las demas sin cambio).
  python3 ciegas_P7_59.py --corre  -> _P7_59_tmp/diario_*.md (los diarios a ciegas), P7_59_razon.json"""
import json, os, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import razon_P7_54 as RZ, diario_razon_P7_54 as D54
ETQ = [("botiquines", "objetos A"), ("botiquín", "objeto A"), ("botiquin", "objeto A"), ("first_aid", "objeto_A"), ("raciones", "objetos B"), ("ración", "objeto B"), ("racion", "objeto B"), ("rations", "objeto_B"),
       ("camuflaje", "objeto D"), ("camouflage", "objeto_D"), ("mochila", "objeto E"), ("backpack", "objeto_E"), ("redes", "objetos C"), ("red", "objeto C"), ("net", "objeto_C"),
       ("sword", "objeto F"), ("spear", "objeto G"), ("blowgun", "objeto I"), ("bow", "objeto H"), ("knives", "objeto J"), ("arrows", "objeto K"), ("darts", "objeto L")]
ACC = {"USAR_BOTIQUIN": "USAR_A", "USAR_RACION": "USAR_B", "COGER_BOTIQUIN": "COGER_A", "COGER_RACION": "COGER_B", "COGER_RED": "COGER_C", "COGER_CAMUFLAJE": "COGER_D", "EMPUNAR_RED": "EMPUNAR_C",
       "PONERSE_CAMUFLAJE": "PONERSE_D", "DAR_BOTIQUIN_HERMANA": "DAR_A_HERMANA"}
INV = {v: k for k, v in ACC.items()}


def ciega(t):
    for k, v in ACC.items(): t = t.replace(k, v)
    for a, b in (("usar_botiquin", "usar_objeto_A"), ("usar_racion", "usar_objeto_B"), ("comer la ración", "usar el objeto B"), ("comer la racion", "usar el objeto B")): t = t.replace(a, b)
    for a, b in ETQ: t = re.sub(r"(?<![A-Za-zÁÉÍÓÚáéíóúñ_])" + re.escape(a) + r"(?![A-Za-zÁÉÍÓÚáéíóúñ])", b, t, flags=re.IGNORECASE) if "_" not in a else re.sub(re.escape(a), b, t)
    for a, b in (("una objeto", "un objeto"), ("la objeto", "el objeto"), ("objeto B del suelo y cogerla", "objeto B del suelo y cogerlo"), ("objeto C del suelo y cogerla", "objeto C del suelo y cogerlo")): t = t.replace(a, b)
    return t


MENU_ACCIONES = {ACC.get(k, k): ciega(v) for k, v in D54.MENU_ACCIONES.items()}
MENU_TEXTO = re.sub(r"Lo que NO sabe hacer este cuerpo:.*$", "Lo que NO sabe hacer este cuerpo: nada fuera de este menú.", ciega(D54.MENU_TEXTO))      # la lista de lo que no sabe hacer revelaba que el objeto C se lanza (es un arma)
SISTEMA = ciega(RZ.SISTEMA).replace(ciega(D54.MENU_TEXTO), MENU_TEXTO)
RE_INV = re.compile(RZ.RE_INV.pattern)


def parsea(linea):
    m = RE_INV.match(linea.strip())
    if not m or m.group(3) not in MENU_ACCIONES: return None
    g = m.groups()
    return {"n": int(g[0]), "tipo": g[1], "accion_ciega": g[2], "accion": INV.get(g[2], g[2]), "anillo": g[3], "calma": g[4], "movimiento": g[5], "hermana": g[6], "cuerpo": RZ.numero(g[7]), "recursos": RZ.numero(g[8]), "vinculo": RZ.numero(g[9]), "porque": g[10].strip(), "se_comprueba": g[11].strip(), "confianza": g[12]}


def corre():
    os.makedirs(os.path.join(AQUI, "_P7_59_tmp"), exist_ok=True); cl = RZ.cliente(); R = []; usd = 0.0
    for S, d, b, sl in RZ.SEL:
        diario = ciega(open(os.path.join(AQUI, "_P7_54_tmp", f"diario_s{S}_d{d}_{b}_{sl}.md")).read()); open(os.path.join(AQUI, "_P7_59_tmp", f"diario_s{S}_d{d}_{b}_{sl}.md"), "w").write(diario)
        if usd >= 2.0: print("TOPE 2 $", flush=True); break
        t0 = time.time(); m = cl.messages.create(model=RZ.MODELO, max_tokens=6000, thinking={"type": "between_tools"}, system=SISTEMA, messages=[{"role": "user", "content": RZ.USUARIO.format(diario=diario)}])
        txt = "".join(x.text for x in m.content if getattr(x, "type", "") == "text"); lineas = [l.strip() for l in txt.split("\n") if l.strip().startswith("INVITACION")]
        cost = m.usage.input_tokens / 1e6 * 3 + m.usage.output_tokens / 1e6 * 15; usd += cost
        R.append({"serie": S, "dia": d, "brazo": b, "slot": sl, "id": m.id, "tokens_entrada": m.usage.input_tokens, "tokens_salida": m.usage.output_tokens, "usd_supuesto": round(cost, 4), "lectura": next((l.strip() for l in txt.split("\n") if l.strip().startswith("LECTURA")), ""), "lineas": lineas, "invitaciones": [p for p in (parsea(l) for l in lineas) if p], "respuesta": txt, "segundos": round(time.time() - t0, 1)})
        json.dump(R, open(os.path.join(AQUI, "P7_59_razon.json"), "w"), ensure_ascii=False, indent=1); print(f"s{S} d{d} {b} a{sl}: {len(lineas)} lineas, {len(R[-1]['invitaciones'])} validas, {cost:.4f} $ (acumulado {usd:.4f})", flush=True)


if __name__ == "__main__":
    if "--corre" in sys.argv: corre()
    elif "--prueba" in sys.argv:
        t = ciega(open(os.path.join(AQUI, "_P7_54_tmp", "diario_s1_d8_COMPARTE_10.md")).read()); print(t[:1500]); print("---"); print(MENU_TEXTO)
        restos = re.findall(r"(?i)(botiqu\w*|raci[oó]n\w*|camufla\w*|mochila|sword|spear|blowgun|knives|arrows|darts|first_aid|rations|camouflage|backpack)\b", t + MENU_TEXTO + SISTEMA); print("restos:", restos[:10], "red sola:", re.findall(r"(?<![A-Za-z])red(?![A-Za-z])", t + MENU_TEXTO + SISTEMA)[:5])

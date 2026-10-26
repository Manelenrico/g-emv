"""[P7-52] LA RAZON DE NOCHE, paso 1 (capitulo 5; diseno de Manel): lee el diario de una criatura y un dia (diario_razon_P7_52) y propone INVITACIONES en formato fijo. Modelo
claude-sonnet-5-5 por la consola de Anthropic (clave en cantera/paper5/.env; bolsa 2, tope 3 $). La razon NO recibe documentacion del juego: solo el diario. Nada sobre lo que
piensan los rivales. Salida comprobable: lineas PROPUESTA con campos fijos. Guarda cada respuesta tal cual (_P7_52_tmp/razon_*.json) y el coste exacto en tokens.
  python3 razon_P7_52.py --corre     las 8 criatura-dias elegidas -> P7_52_razon.json
  python3 razon_P7_52.py --prompt    imprime el prompt (el sistema y la plantilla del usuario)"""
import json, os, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
MODELO = "claude-sonnet-5-5"; TOPE_USD = 3.0
PRECIO = {"entrada_por_Mtok": 3.0, "salida_por_Mtok": 15.0}      # [supuesto] tarifa de la clase Sonnet; el coste exacto en tokens se guarda; los dolares se confirman en la consola
SEL = [(1, 8, "COMPARTE", 10), (1, 6, "SOLAS", 11), (1, 3, "COMPARTE", 11), (1, 2, "SOLAS", 10), (1, 1, "COMPARTE", 10), (3, 17, "SOLAS", 11), (3, 18, "SOLAS", 10), (3, 12, "COMPARTE", 11)]

SISTEMA = """Eres la razón de noche de una criatura. La criatura vive días de unos diez minutos en un mundo que ni tú ni ella conocéis de antemano; su cuerpo siente en tres dimensiones (cuerpo: dolor o alivio; recursos: ganar o perder; vínculo: acercarse o alejarse de su hermana) y decide por sí solo, minimizando su malestar. Tú no decides nada: lees su diario de hoy y le dejas INVITACIONES para mañana, que su cuerpo aceptará o no según lo que sienta.

Lo único que sabes del mundo es lo que dice el diario. No tienes manual, reglas ni nombres oficiales: si el diario nombra cosas (botiquín, ración, red, camuflaje, mochila, armas, el anillo de fuego, la riada, rivales, su hermana), úsalos con ese nombre y nada más. No inventes mecanismos que el diario no sugiera; si deduces algo (por ejemplo, que esto es un juego y cómo funciona), dilo como hipótesis y apóyala en lo que leíste.

Qué puedes proponer, y solo esto:
1. CONDICIÓN: bajo qué condición una cosa funciona o no (dónde, cuándo, en qué estado del cuerpo, llevando qué).
2. FORMA NUEVA: una manera distinta de usar una cosa que la criatura ya conoce o ha visto.
3. EXPLICACIÓN: una explicación de algo del diario que no tiene explicación (incluido lo invisible: golpes sin autor, casillas que no dejan pasar sin que se vea a nadie, cosas que cambian solas), con una forma de ponerla a prueba.
Prohibido: nada sobre lo que piensan, quieren o planean los rivales; nada que sea una orden («haz», «no hagas»); nada que el diario no permita sostener.

Formato de salida, FIJO. Primero una línea LECTURA: con dos o tres frases sobre el día. Después entre 3 y 6 propuestas, cada una en UNA sola línea exactamente así (campos separados por « | », sin saltos de línea dentro):
PROPUESTA n | tipo=CONDICION|FORMA|EXPLICACION | que_probar=<qué cosa y qué hacer con ella, con los nombres del diario> | donde_cuando=<dónde y cuándo, en el idioma del diario: casilla, dentro/fuera del anillo, segundo del día, estado de la vida, quién cerca> | cuerpo=<+N alivio | -N dolor | 0>, recursos=<+N ganar | -N perder | 0>, vinculo=<+N acercar | -N alejar | 0> | se_comprueba=<qué tendría que verse en el diario de mañana para darla por buena o mala> | apoyo=<los momentos del diario (tics) en que te basas> | confianza=<baja|media|alta>
Las cifras de cuerpo, recursos y vínculo son aproximadas, en las unidades del diario (vida de 0 a 100; riqueza W de 0 a 1; vínculo B de 0 a 1). Si no sabes una cifra, pon 0 y dilo en se_comprueba. Nada después de la última PROPUESTA."""

USUARIO = """Este es el diario de hoy. Léelo entero y deja tus invitaciones para mañana en el formato fijo.

{diario}"""


def corre():
    sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
    for line in open(os.path.join(RAIZ, "cantera", "paper5", ".env")):
        if line.startswith("ANTHROPIC_API_KEY="): os.environ["ANTHROPIC_API_KEY"] = line.strip().split("=", 1)[1]
    import anthropic
    cl = anthropic.Anthropic(); R = []; tin = tout = 0; usd = 0.0
    salida = os.path.join(AQUI, "P7_52_razon.json")
    if os.path.exists(salida): R = json.load(open(salida)); tin = sum(r["tokens_entrada"] for r in R); tout = sum(r["tokens_salida"] for r in R); usd = sum(r["usd_supuesto"] for r in R)
    hechos = {(r["serie"], r["dia"], r["brazo"], r["slot"]) for r in R}
    for S, d, b, sl in SEL:
        if (S, d, b, sl) in hechos: continue
        if usd >= TOPE_USD: print("TOPE de 3 $ alcanzado (supuesto): paro", flush=True); break
        diario = open(os.path.join(AQUI, "_P7_52_tmp", f"diario_s{S}_d{d}_{b}_{sl}.md")).read(); t0 = time.time()
        m = cl.messages.create(model=MODELO, max_tokens=6000, thinking={"type": "between_tools"}, system=SISTEMA, messages=[{"role": "user", "content": USUARIO.format(diario=diario)}])      # [intento 1: con 2.500 tokens el modelo gasto todo en pensar y no escribio texto: 8 llamadas vacias, 0,57 $ supuestos, guardadas en P7_52_razon_intento1.json]
        txt = "".join(x.text for x in m.content if getattr(x, "type", "") == "text"); ui, uo = m.usage.input_tokens, m.usage.output_tokens
        cost = ui / 1e6 * PRECIO["entrada_por_Mtok"] + uo / 1e6 * PRECIO["salida_por_Mtok"]; tin += ui; tout += uo; usd += cost
        props = [l.strip() for l in txt.split("\n") if l.strip().startswith("PROPUESTA")]; lectura = next((l.strip() for l in txt.split("\n") if l.strip().startswith("LECTURA")), "")
        bien = [p for p in props if re.match(r"^PROPUESTA \d+ \| tipo=(CONDICION|FORMA|EXPLICACION) \| que_probar=.+ \| donde_cuando=.+ \| cuerpo=.+, recursos=.+, vinculo=.+ \| se_comprueba=.+ \| apoyo=.+ \| confianza=(baja|media|alta)\s*$", p)]
        r = {"serie": S, "dia": d, "brazo": b, "slot": sl, "modelo": MODELO, "id": m.id, "tokens_entrada": ui, "tokens_salida": uo, "usd_supuesto": round(cost, 4), "segundos": round(time.time() - t0, 1), "lectura": lectura, "propuestas": props, "propuestas_formato_ok": len(bien), "respuesta": txt, "chars_diario": len(diario), "stop": m.stop_reason, "bloques": [getattr(x, "type", "?") for x in m.content]}
        R.append(r); json.dump(R, open(salida, "w"), ensure_ascii=False, indent=1); json.dump(r, open(os.path.join(AQUI, "_P7_52_tmp", f"razon_s{S}_d{d}_{b}_{sl}.json"), "w"), ensure_ascii=False, indent=1)
        print(f"s{S} d{d} {b} a{sl}: {len(props)} propuestas ({len(bien)} con formato), {ui}+{uo} tokens, {cost:.4f} $ (acumulado {usd:.4f} $)", flush=True)
    print(f"TOTAL: {len(R)} criatura-dias, {tin} tokens de entrada, {tout} de salida, {usd:.4f} $ (tarifa supuesta)")


if __name__ == "__main__":
    if "--prompt" in sys.argv: print(SISTEMA); print("\n--- usuario ---\n" + USUARIO)
    elif "--corre" in sys.argv: corre()

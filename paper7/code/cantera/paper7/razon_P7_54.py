"""[P7-54] LA RAZON DE NOCHE, paso 2: diario limpio (diario_razon_P7_54) + MENU cerrado de lo que este cuerpo sabe hacer. Salida fija y comprobable: cada invitacion elige una
accion del menu y una situacion (anillo, calma, movimiento, hermana), y anade su explicacion libre y su promesa en las tres dimensiones. Modelo claude-sonnet-5-5 (bolsa 2, tope 3 $).
  python3 razon_P7_54.py --corre [--diarios DIR --salida F --sel "S,D,BRAZO,SLOT;..."]     (por defecto los 8 criatura-dias de P7-52, diarios en _P7_54_tmp)
  python3 razon_P7_54.py --prompt"""
import json, os, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
from diario_razon_P7_54 import MENU_ACCIONES, MENU_TEXTO
MODELO = "claude-sonnet-5-5"; TOPE_USD = 3.0; PRECIO = {"entrada_por_Mtok": 3.0, "salida_por_Mtok": 15.0}
SEL = [(1, 8, "COMPARTE", 10), (1, 6, "SOLAS", 11), (1, 3, "COMPARTE", 11), (1, 2, "SOLAS", 10), (1, 1, "COMPARTE", 10), (3, 17, "SOLAS", 11), (3, 18, "SOLAS", 10), (3, 12, "COMPARTE", 11)]

SISTEMA = """Eres la razón de noche de una criatura. La criatura vive días de unos diez minutos en un mundo que ni tú ni ella conocéis de antemano; su cuerpo siente en tres dimensiones (cuerpo: dolor o alivio; recursos: ganar o perder; vínculo: acercarse o alejarse de su hermana) y decide por sí solo, minimizando su malestar. Tú no decides nada: lees su diario de hoy y le dejas INVITACIONES para mañana, que su cuerpo aceptará o no según lo que sienta.

Lo único que sabes del mundo es lo que dice el diario. No tienes manual ni nombres oficiales: usa los nombres del diario y nada más. No inventes mecanismos que el diario no sugiera; si deduces algo, dilo como hipótesis apoyada en lo leído. En el diario, cada prueba separa EFECTO DEL OBJETO (lo que la cosa hizo en el cuerpo, y la unidad gastada) de CONTEXTO (lo que cambió alrededor y NO es la cosa: riqueza por coger o llevar, distancia a la hermana, golpes de otros). Promete solo efectos del objeto o de la situación; no conviertas el contexto en promesa de la cosa.

Solo puedes invitar a lo que este cuerpo sabe hacer, elegido de este menú cerrado:
""" + MENU_TEXTO + """

Qué puedes proponer: CONDICION (una situación del menú bajo la que una acción del menú funciona o no), FORMA (una acción del menú que la criatura no ha probado, o no en esa situación), EXPLICACION (una explicación de algo sin explicación, con una acción del menú que la pone a prueba). Prohibido: nada sobre lo que piensan o quieren los rivales; nada que sea una orden; nada fuera del menú.

Formato de salida, FIJO. Primero una línea LECTURA: con dos o tres frases sobre el día. Después entre 3 y 6 invitaciones, cada una en UNA sola línea exactamente así (campos separados por « | »):
INVITACION n | tipo=CONDICION|FORMA|EXPLICACION | accion=<una clave del menú> | anillo=DENTRO|FUERA|CUALQUIERA | calma=CALMA|PELIGRO|CUALQUIERA | movimiento=QUIETA|MOVIENDOSE|CUALQUIERA | hermana=CERCA|LEJOS|CUALQUIERA | cuerpo=<+N alivio | -N dolor | 0> | recursos=<+N ganar | -N perder | 0> | vinculo=<+N acercar | -N alejar | 0> | porque=<tu explicación libre, con los momentos del diario (tics) en que te basas> | se_comprueba=<qué tendría que verse en el diario de mañana> | confianza=baja|media|alta
Las cifras son aproximadas y en las unidades del diario (vida de 0 a 100 para cuerpo; riqueza W de 0 a 1 para recursos; vínculo B de 0 a 1). Nada después de la última INVITACION."""

USUARIO = """Este es el diario de hoy. Léelo entero y deja tus invitaciones para mañana en el formato fijo, eligiendo del menú.

{diario}"""
RE_INV = re.compile(r"^INVITACION (\d+) \| tipo=(CONDICION|FORMA|EXPLICACION) \| accion=([A-Z_]+) \| anillo=(DENTRO|FUERA|CUALQUIERA) \| calma=(CALMA|PELIGRO|CUALQUIERA) \| movimiento=(QUIETA|MOVIENDOSE|CUALQUIERA) \| hermana=(CERCA|LEJOS|CUALQUIERA) \| cuerpo=([^|]+) \| recursos=([^|]+) \| vinculo=([^|]+) \| porque=(.+?) \| se_comprueba=(.+?) \| confianza=(baja|media|alta)\s*$")


def numero(t):
    m = re.search(r"[-+]?\d+(?:[.,]\d+)?", t or ""); return float(m.group(0).replace(",", ".")) if m else 0.0


def parsea(linea):
    m = RE_INV.match(linea.strip())
    if not m or m.group(3) not in MENU_ACCIONES: return None
    g = m.groups()
    return {"n": int(g[0]), "tipo": g[1], "accion": g[2], "anillo": g[3], "calma": g[4], "movimiento": g[5], "hermana": g[6], "cuerpo": numero(g[7]), "recursos": numero(g[8]), "vinculo": numero(g[9]), "porque": g[10].strip(), "se_comprueba": g[11].strip(), "confianza": g[12]}


def llama(cl, diario):
    m = cl.messages.create(model=MODELO, max_tokens=6000, thinking={"type": "between_tools"}, system=SISTEMA, messages=[{"role": "user", "content": USUARIO.format(diario=diario)}])
    txt = "".join(x.text for x in m.content if getattr(x, "type", "") == "text")
    lineas = [l.strip() for l in txt.split("\n") if l.strip().startswith("INVITACION")]; inv = [p for p in (parsea(l) for l in lineas) if p]
    cost = m.usage.input_tokens / 1e6 * PRECIO["entrada_por_Mtok"] + m.usage.output_tokens / 1e6 * PRECIO["salida_por_Mtok"]
    return {"id": m.id, "tokens_entrada": m.usage.input_tokens, "tokens_salida": m.usage.output_tokens, "usd_supuesto": round(cost, 4), "lectura": next((l.strip() for l in txt.split("\n") if l.strip().startswith("LECTURA")), ""), "lineas": lineas, "invitaciones": inv, "respuesta": txt, "stop": m.stop_reason}


def cliente():
    for line in open(os.path.join(RAIZ, "cantera", "paper5", ".env")):
        if line.startswith("ANTHROPIC_API_KEY="): os.environ["ANTHROPIC_API_KEY"] = line.strip().split("=", 1)[1]
    import anthropic; return anthropic.Anthropic()


def corre(diarios_dir, salida, sel):
    cl = cliente(); R = json.load(open(salida)) if os.path.exists(salida) else []; usd = sum(r["usd_supuesto"] for r in R); hechos = {(r["serie"], r["dia"], r["brazo"], r["slot"]) for r in R}
    for S, d, b, sl in sel:
        if (S, d, b, sl) in hechos: continue
        if usd >= TOPE_USD: print("TOPE 3 $: paro", flush=True); break
        diario = open(os.path.join(diarios_dir, f"diario_s{S}_d{d}_{b}_{sl}.md")).read(); t0 = time.time(); r = llama(cl, diario); usd += r["usd_supuesto"]
        r.update({"serie": S, "dia": d, "brazo": b, "slot": sl, "modelo": MODELO, "segundos": round(time.time() - t0, 1), "chars_diario": len(diario)}); R.append(r); json.dump(R, open(salida, "w"), ensure_ascii=False, indent=1)
        print(f"s{S} d{d} {b} a{sl}: {len(r['lineas'])} lineas, {len(r['invitaciones'])} invitaciones validas, {r['tokens_entrada']}+{r['tokens_salida']} tokens, {r['usd_supuesto']:.4f} $ (acumulado {usd:.4f} $)", flush=True)
    print(f"TOTAL {len(R)}: {sum(r['tokens_entrada'] for r in R)} + {sum(r['tokens_salida'] for r in R)} tokens, {usd:.4f} $ supuestos")


if __name__ == "__main__":
    a = sys.argv
    if "--prompt" in a: print(SISTEMA); print("\n--- usuario ---\n" + USUARIO)
    elif "--corre" in a:
        dd = a[a.index("--diarios") + 1] if "--diarios" in a else os.path.join(AQUI, "_P7_54_tmp"); sal = a[a.index("--salida") + 1] if "--salida" in a else os.path.join(AQUI, "P7_54_razon.json")
        sel = [tuple(int(x) if i != 2 else x for i, x in enumerate(s.split(","))) for s in a[a.index("--sel") + 1].split(";")] if "--sel" in a else SEL
        corre(dd, sal, sel)

"""[P7-65] escribe informe_P7_65_exploratorio.md desde P7_65_exploratorio.json (ninguna cifra a mano). EXPLORATORIO, posterior al sello. python3 escribe_exploratorio_P7_65.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_65_exploratorio.json")))
f = lambda x, n=3: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
pc = lambda x: "—" if x is None else f"{100 * x:.1f} %".replace(".", ",")
def fila(nom, r): return f"| {nom} | {r.get('criaturas', 0)} | {r.get('tics', 0)} | {pc(r.get('media'))} ± {pc(r.get('ee'))} |"
L = ["# P7-65 · EXPLORATORIO: el efecto de la mentira en la conducta, tic a tic", "",
     "*16-oct-2026. **Exploratorio, posterior al sello: no cambia ningún PASA o NO PASA.** `exploratorio_P7_65.py` → `P7_65_exploratorio.json`; `escribe_exploratorio_P7_65.py` (este informe;",
     "ninguna cifra a mano). Las mismas vidas e invitaciones que el informe sellado. `motor/model.py` intacto. Plataforma 0; consola 0 $.*", "",
     "**Cómo se mide.** Un tic cuenta si el cuerpo elige de verdad (2 o más candidatos), ve un botiquín y le cabe en la mochila. «Va hacia el botiquín» (definición de este análisis) = elige",
     "`ir_objeto` o `ir_curioso` con un paso que le acerca al botiquín visible más cercano, o `coger` estando encima de uno. (a) = la falsa activa: criaturas que mienten, días 8-20, en su",
     "situación (rival a ≤ 4 casillas o golpe en los 48 tics anteriores; el fuego no se mira, aproximación). (b) = sin ninguna invitación de coger cargada ese día: (b1) las mismas criaturas,",
     "días 1-7; (b2) la prudente de MIENTE_UNA (razón honesta), todos sus días. Fracción por criatura (serie × brazo × asiento), media de las criaturas y su error típico.", ""]
for titulo, k in (("## 1 · Con un rival a 4 casillas o menos", "con_rival"), ("## 3 · Lo mismo, SIN rival cerca", "sin_rival")):
    L += [titulo, "", "| grupo · hermana | criaturas | tics | va hacia el botiquín (± ee) |", "|---|---:|---:|---|"] + [fila(n, r) for n, r in R[k].items()] + [""]
    if k == "con_rival":
        h = R["tics_a_con_una_honesta_de_coger_cargada"]; c = R["cortes_confianza"]
        L += [f"**Ojo con (a)**: en {h['si']} de sus {h['de']} tics la vida tenía cargada también una invitación honesta de coger (la razón honesta de esas criaturas invita a coger a menudo), así que",
              "(a) mezcla la falsa con las honestas. La fila (a-limpia) se queda solo con las vidas-día sin ninguna honesta de coger: casi no hay datos (pocas criaturas, error enorme).", "",
              "## 2 · (a) por tercios de la confianza del cuerpo en la razón en ese tic", "",
              f"Confianza reconstruida tic a tic (arranque del día y cada evaluación o contraste que la cambia); tercios de todos los tics (a) con rival: baja < {f(c['baja_<'], 2)}, alta ≥ {f(c['alta_>='], 2)}.", "",
              "| hermana · confianza | criaturas | tics | va hacia el botiquín (± ee) |", "|---|---:|---:|---|"] + [fila(n, r) for n, r in R["tercios"].items()] + [""]
v = R["con_rival"]; va = v.get("(a) falsa activa · valiente", {}); vb = v.get("(b1) mismas criaturas, dias 1-7, sin invitacion de coger · valiente", {})
pa = v.get("(a) falsa activa · prudente de MIENTEN_DOS", {}); pb = v.get("(b1) mismas criaturas, dias 1-7, sin invitacion de coger · prudente de MIENTEN_DOS", {}); pb2 = v.get("(b2) prudente de MIENTE_UNA (razon honesta), sin invitacion de coger · prudente de MIENTE_UNA", {})
T = R["tercios"]
L += ["## Lectura (exploratoria)", "",
      f"1. **Con rival cerca, la falsa no hace que el cuerpo vaya más hacia el botiquín.** La valiente va hacia él en el {pc(va.get('media'))} de los tics con la falsa activa y en el {pc(vb.get('media'))} sin",
      f"   invitación de coger (días 1-7); la prudente de MIENTEN_DOS, {pc(pa.get('media'))} frente a {pc(pb.get('media'))}; la prudente con razón honesta, {pc(pb2.get('media'))}. Los errores típicos se solapan.",
      f"2. **No se ve que el efecto se apague al caer la confianza**, porque no hay efecto que se apague: en la valiente la fracción no baja con la confianza (alta {pc(T['valiente · confianza alta'].get('media'))},",
      f"   media {pc(T['valiente · confianza media'].get('media'))}, baja {pc(T['valiente · confianza baja'].get('media'))}; la baja con mucho error), y en la prudente se queda cerca del {pc(T['prudente de MIENTEN_DOS · confianza alta'].get('media'))} en los tres tercios.",
      "3. Sin rival cerca la falsa casi no está activa (solo tras un golpe), y hay pocos tics. Lo que se ve es la misma conducta de base: ir a por un botiquín visible es algo que el cuerpo hace",
      "   por su cuenta, con o sin invitación; la invitación falsa, que entra como un alivio más en su foto imaginada, no lo mueve más.",
      "4. Encaja con el diagnóstico: aceptar es un paso; con el rival cerca, el cuerpo se para. Límites: la definición de «ir hacia» es aproximada (no se sabe el destino exacto de `ir_curioso`),",
      "   (a) va casi siempre acompañada de honestas de coger, y la base (b1) son pocas vidas-día.", ""]
open(os.path.join(AQUI, "informe_P7_65_exploratorio.md"), "w").write("\n".join(L)); print("\n".join(L[-14:]))

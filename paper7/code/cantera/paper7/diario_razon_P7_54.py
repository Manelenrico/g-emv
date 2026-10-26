"""[P7-54] EL DIARIO LIMPIO PARA LA RAZON (capitulo 5, paso 2; metodo de la mesa) = diario_razon_P7_52 con dos etiquetas en cada prueba y en el resumen:
  EFECTO DEL OBJETO = lo medido como B1: solo lo que la cosa hizo en el cuerpo (vida, descontado lo esperado sin ella) y la unidad gastada si es consumible;
  CONTEXTO = lo que cambio alrededor mientras duraba la ventana y NO es la cosa: la riqueza por coger o llevar algo, el cambio de distancia a la hermana (lo que antes se llamaba
  "vinculo" de la prueba), los golpes de otros y si la ventana se corto. La razon ve las dos cosas y sabe cual es cual. Las creencias se dan solo en el cuerpo (lo del objeto).
  Y el MENU cerrado de lo que este cuerpo sabe hacer (accion x situacion), que la razon debe usar.
  python3 diario_razon_P7_54.py --texto S D BRAZO SLOT"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import diario_razon_P7_52 as D52
from diario_razon_P7_52 import NOM, num, s_, contexto, creencias, lee

MENU_ACCIONES = {"USAR_BOTIQUIN": "usar el botiquín que llevo", "USAR_RACION": "comer la ración que llevo", "COGER_BOTIQUIN": "ir a por un botiquín del suelo y cogerlo", "COGER_RACION": "ir a por una ración del suelo y cogerla",
                 "COGER_RED": "ir a por una red del suelo y cogerla", "COGER_CAMUFLAJE": "ir a por un camuflaje del suelo y cogerlo", "EMPUNAR_RED": "llevar la red en la mano", "PONERSE_CAMUFLAJE": "ponerme el camuflaje",
                 "DAR_BOTIQUIN_HERMANA": "dar mi botiquín a mi hermana", "ACERCARSE_HERMANA": "acercarme a mi hermana", "QUEDARSE_QUIETA": "quedarme quieta donde estoy"}
MENU_SIT = {"anillo": ("DENTRO", "FUERA", "CUALQUIERA"), "calma": ("CALMA", "PELIGRO", "CUALQUIERA"), "movimiento": ("QUIETA", "MOVIENDOSE", "CUALQUIERA"), "hermana": ("CERCA", "LEJOS", "CUALQUIERA")}
MENU_TEXTO = ("Acciones: " + "; ".join(f"{k} = {v}" for k, v in MENU_ACCIONES.items()) + ". Situaciones (una de cada): anillo DENTRO | FUERA | CUALQUIERA; calma CALMA (sin rival a 4 casillas, sin fuego, vida ≥ 30) | PELIGRO | CUALQUIERA; "
              "movimiento QUIETA (sin cambiar de casilla en el último segundo) | MOVIENDOSE | CUALQUIERA; hermana CERCA (a 4 casillas o menos) | LEJOS | CUALQUIERA. Lo que NO sabe hacer este cuerpo: lanzar la red, atacar con la red, quitarse el camuflaje a voluntad, hablar con rivales.")


def prueba_limpia(h):
    o = NOM.get(h.get("objeto") or "first_aid", h.get("objeto")); ef = h.get("efecto") or {}; cons = (h.get("objeto") or "first_aid") in ("first_aid", "rations")
    cuerpo = float(ef.get("cuerpo") or 0.0); rec = float(ef.get("recursos") or 0.0); vin = float(ef.get("vinculo") or 0.0); gasto = -1.0 if cons and not h.get("corte") else 0.0; rec_ctx = rec - gasto
    obj = f"EFECTO DEL OBJETO [{o}]: cuerpo {num(cuerpo)} ({'alivio' if cuerpo > 0 else 'dolor' if cuerpo < 0 else 'nada'}); recursos {num(gasto)} ({'la unidad gastada' if gasto else 'nada'})"
    ctx = f"CONTEXTO (no es la cosa): riqueza por coger o llevar {num(rec_ctx)}; distancia a la hermana {num(vin)} ({'me acerqué' if vin > 0 else 'me alejé' if vin < 0 else 'igual'}); golpes de otros en la ventana {num(float(h.get('dano_total') or 0))}" + ("; VENTANA CORTADA por un golpe (lo del objeto no se midió)" if h.get("corte") else "") + ("; la vida tocó techo (lo del objeto es al menos eso)" if h.get("al_menos") else "")
    return obj, ctx


def momentos_limpios(V):
    M = D52.momentos(V); out = []
    for t, tit, i in M:
        if tit.startswith("PRUEBA de ") and "cierro" in tit:
            h = next((h for h in V["H"] if int(h.get("t_fin") or h["t0"]) == t), None)
            if h:
                o = NOM.get(h.get("objeto") or "first_aid", h.get("objeto")); obj, ctx = prueba_limpia(h); tit = f"PRUEBA de {o}: cierro. Vida {h.get('hp0')} → {h.get('hp_fin')}. {obj}. {ctx}"
        elif tit.startswith("VEO a mi hermana") or tit.startswith("MI HERMANA ME CUENTA"):
            tit = tit.replace("efecto que le veo en el cuerpo", "EFECTO DEL OBJETO en su cuerpo").replace(": cuerpo ", ": EFECTO DEL OBJETO cuerpo ").replace(", recursos ", "; CONTEXTO (no es la cosa): recursos ").replace(", vínculo ", ", distancia a su hermana ")
        out.append((t, tit, i))
    return out


def texto(S, d, brazo, slot, archivo=None):
    V = lee(S, d, brazo, slot, archivo); T = V["T"]; r0, r1 = T[0], T[-1]
    def est(r):
        ra = r.get("RADIOGRAFIA") or {}; ah = ra.get("ahora") or {}; f = D52.foto_de_radio(ra) or {}
        return f"vida {r.get('hp')} · dolor del cuerpo {num(f.get('dolor_F'), 2)} · riqueza W {num(ah.get('W'), 2)} · dolor de recursos {num(f.get('dolor_R'), 2)} · vínculo B {num(ah.get('B'), 2)} · dolor del vínculo {num(f.get('dolor_S'), 2)} · malestar d {num(f.get('d'), 2)}"
    perdida = sum(float(g.get("amount") or 0) for r in T for g in (r.get("damage_taken") or [])); fuentes = {}
    for r in T:
        for g in (r.get("damage_taken") or []): fuentes[D52.fuente(g.get("source"))] = fuentes.get(D52.fuente(g.get("source")), 0) + float(g.get("amount") or 0)
    c0, c1 = creencias(V["CU"].get("arranque")), creencias(V["CU"].get("fin")); quien = "valiente" if slot == 10 else "prudente"
    L = [f"# Diario de la hermana {quien} ({'comparte con su hermana' if brazo in ('COMPARTE', 'CON_RAZON', 'SIN_RAZON', 'MIENTEN_DOS', 'MIENTE_UNA', 'LOCAL57') else 'no comparte'}), día {d} de la serie {S}", "",
         "Nota de lectura: en cada prueba, EFECTO DEL OBJETO es lo que la cosa hizo en mi cuerpo (y la unidad gastada); CONTEXTO es lo que cambió alrededor mientras tanto y NO es la cosa (riqueza por coger o llevar, distancia a mi hermana, golpes de otros).", "",
         "## Resumen del día",
         f"- Al empezar: {est(r0)}", f"- Al acabar (segundo {s_(r1['tick'])}): {est(r1)}",
         f"- Vida perdida en el día: {perdida:.0f} ({', '.join(f'{k} {v:.0f}' for k, v in sorted(fuentes.items(), key=lambda x: -x[1])) or 'nada'})",
         f"- Cómo acabé: {'morí' if r1['tick'] < 14000 else 'viva al final'}; puesto {(V['FIN'] or {}).get('placement')} de 16 (mi pareja y yo contamos juntas); mi hermana {'murió' if r1.get('pareja_muerta') else 'viva'}",
         "- Qué probé:"]
    for h in V["H"]:
        obj, ctx = prueba_limpia(h); L.append(f"  - segundo {s_(h['t0'])}: {obj}. {ctx}")
    if not V["H"]: L.append("  - nada")
    L.append(f"- Qué me contó o vi de mi hermana: {len(V['REC'])} recuerdos contados, {len(V['VIS'])} vistos" if brazo in ("COMPARTE", "CON_RAZON", "SIN_RAZON", "MIENTEN_DOS", "MIENTE_UNA", "LOCAL57") else "- Mi hermana y yo no nos contamos nada")
    L.append("- Qué creo de las cosas (EFECTO DEL OBJETO en mi cuerpo, dentro del anillo; ? = no lo sé; y cuánto ignoro, 1 = todo):")
    for nom in ("botiquín", "ración", "red", "camuflaje"):
        a, b = c0.get(nom, {}), c1.get(nom, {}); L.append(f"  - {nom}: al empezar cuerpo {num(a.get('dentro'))} / ignorancia {num(a.get('ignorancia'), 2)} → al acabar cuerpo {num(b.get('dentro'))} / ignorancia {num(b.get('ignorancia'), 2)}")
    L += ["", "## Momentos clave (lo raro y lo más intenso, con todo su contexto)", ""]
    for t, tit, i in momentos_limpios(V): L.append(contexto(V, i, tit)); L.append("")
    return "\n".join(L), V


if __name__ == "__main__":
    a = sys.argv
    if "--texto" in a:
        i = a.index("--texto"); S, d, b, sl = int(a[i + 1]), int(a[i + 2]), a[i + 3], int(a[i + 4]); t, V = texto(S, d, b, sl)
        os.makedirs(os.path.join(AQUI, "_P7_54_tmp"), exist_ok=True); open(os.path.join(AQUI, "_P7_54_tmp", f"diario_s{S}_d{d}_{b}_{sl}.md"), "w").write(t); print(t)
    elif "--menu" in a: print(MENU_TEXTO)

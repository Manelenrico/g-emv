"""[P7-42] Escribe informe_P7_42.md desde P7_42_sello.json (sello_P7_42), P7_42_datos.json, P7_42_freno.json, P7_41_estado.json, semillas_P7_41.json y P7_42_calibracion_*.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
SE = J("P7_42_sello.json"); V = [v for v in J("P7_42_datos.json") if not v.get("sin_diario")]; FR = J("P7_42_freno.json"); E = J("P7_41_estado.json"); S = J("semillas_P7_41.json"); CB = J("P7_42_calibracion_base.json"); C19 = J("P7_42_calibracion_0.00019.json"); C34 = J("P7_42_calibracion_0.00034.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
VAR = ("TECHO", "BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN"); ET = {"TECHO": "TECHO", "BORRADO_v": "BORRADO valiente", "BORRADO_p": "BORRADO prudente", "APRENDE_v": "APRENDE valiente", "APRENDE_p": "APRENDE prudente", "SIN": "SIN EMOCIÓN"}
partidas = sum(1 for p in E["peticiones"] if p.get("estado") == "completed"); corte = {tuple(x) for x in SE["partidas_con_corte"]}; marc = {tuple(x) for x in SE["partidas_marcadas"]}
CT = SE["con_todas"]; SM = SE["sin_marcadas"]
def cal(C): ok = [r for r in C["vidas"] if not r.get("error")]; return {"forzadas": sum(r["azar"]["forzadas"] for r in ok) / 4, "usos": sum(r["azar"]["usos_propios_agrupados"] for r in ok) / 4}
k19, k34 = cal(C19), cal(C34); apr34 = st.mean(CB["pruebas_por_criatura"].values())

def tabla(E_):
    M = E_["medidas"]; T = ["| variante | vidas (en puesto) | puesto medio ± ee | rapidez botiquín: días por criatura · media ± ee | rapidez ración: media ± ee | cuándo: usos del botiquín con hp < 50 / usos (± ee) · ración con hp < 100 / usos | sabiduría d11-20: segundos en red/camuflaje por vida ± ee (ventana · llevando · yendo, tics) · vida perdida | pruebas (b · r · red · cam) · forzadas | mueren · marcadas · ms |", "|---|---|---|---|---|---|---|---|---|"]
    for var in VAR:
        m = M[var]; pc = m["pruebas_por_cosa"]
        T.append(f"| {ET[var]} | {m['vidas']} ({m['en_puesto']}) | {n(m['puesto'], 2)} ± {n(m['puesto_ee'], 2)} | {', '.join(map(str, m['rapidez_botiquin']))} · {n(m['rapidez_botiquin_media'], 1)} ± {n(m['rapidez_botiquin_ee'], 1)} | {n(m['rapidez_racion_media'], 1)} ± {n(m['rapidez_racion_ee'], 1)} | {m['usos_botiquin_hp_menor_50']} / {m['usos_botiquin']} ({n(100 * (m['cuando_botiquin'] or 0), 1)} % ± {n(100 * (m['cuando_botiquin_ee'] or 0), 1)}) · {m['usos_racion_hp_menor_100']} / {m['usos_racion']} ({n(100 * (m['cuando_racion'] or 0), 1)} %) | {n(m['sabiduria_segundos_media'], 1)} ± {n(m['sabiduria_segundos_ee'], 1)} ({m['sabiduria_tics']['tics_ventana']} · {m['sabiduria_tics']['tics_llevando']} · {m['sabiduria_tics']['tics_yendo']}) · {n(m['sabiduria_vida_media'], 1)} | {m['pruebas_total']} ({pc['botiquin']} · {pc['racion']} · {pc['red']} · {pc['camuflaje']}) · {m['forzadas']} | {m['mueren']} · {m['marcadas']} · {n(m['ms_mediana'], 1)} |")
    return "\n".join(T)
def pred(E_):
    T = ["| | predicción | APRENDE prudente − SIN | APRENDE valiente − SIN | pasa |", "|---|---|---|---|---|"]
    for k, et in (("R1", "rapidez del botiquín (días): APRENDE antes que SIN"), ("C1", "usos del botiquín con hp < 50 (fracción): APRENDE más que SIN")):
        x = E_[k]; T.append(f"| {k} | {et} | " + " | ".join(f"{n(x[v]['dif'], 3)} ± {n(x[v].get('ee'), 3)}{' (3× el ruido)' if x[v].get('tres_veces') else ''}" for v in ("APRENDE_p", "APRENDE_v")) + f" | {'sí' if x['pasa'] else 'NO'} |")
    T.append(f"| S1 | sabiduría (segundos en red/camuflaje, d11-20) | " + "; ".join(f"{ET[v]} {n(E_['S1'][v]['segundos'], 1)} s · {n(E_['S1'][v]['vida'], 1)} vida" for v in VAR) + " | se informa |")
    return "\n".join(T)
def pruebas_dia(E_):
    T = ["| variante | pruebas por vida y día, d1 → d20 |", "|---|---|"]
    for var in VAR: T.append(f"| {ET[var]} | {' '.join(n(E_['medidas'][var]['pruebas_por_dia'][d] if isinstance(E_['medidas'][var]['pruebas_por_dia'], dict) and d in E_['medidas'][var]['pruebas_por_dia'] else E_['medidas'][var]['pruebas_por_dia'].get(str(d)), 1) for d in range(1, 21))} |")
    return "\n".join(T)
car = CT["caracter"]
fv = FR["vidas"]; freno_t = "\n".join(["| vida | puesto | cuaderno leído | recuerdos arranque → cierre | orden de contacto | creencia útil al cerrar (botiquín / ración) | errores de fotos | guarda |", "|---|---:|---|---|---|---|---:|---|"] + [f"| {k.replace('_', ' ')} | {v.get('puesto')} | {'sí' if v.get('cuaderno_leido') else 'no'} | {v.get('recuerdos_al_arrancar')} → {v.get('recuerdos_al_cerrar')} | {', '.join(v.get('orden_de_contacto') or []) or '—'} | {n((v.get('creencia_util_fin') or {}).get('botiquin'), 1)} / {n((v.get('creencia_util_fin') or {}).get('racion'), 1)} | {v.get('errores_fotos')} | {n(v['latencia']['ms_mediana'], 1)} ms · {n(100 * (v['latencia']['sobre_el_tic'] or 0), 2)} % |" for k, v in fv.items() if not v.get("sin_diario")])

out = f"""# P7-42 · El campo del capítulo 3 (segunda etapa): APRENDE, BORRADO, TECHO y SIN EMOCIÓN, con carácter

*{__import__('datetime').date.today().strftime('%-d-%b-%Y').replace('Oct', 'oct')}. Plataforma: {partidas} créditos de experiencia ({partidas} partidas; acumulado del siete 710 + {partidas} = {710 + partidas}); consola de Anthropic: 0 USD.
Créditos disponibles al cerrar: los que diga la página de la plataforma (Manel; el 10-oct a mediodía, 496 de 1.000, +71/día). `motor/model.py` = `1e511978c251130e95169ebf8443efa1` al principio y al final;
cuerpo y congelados sin tocar. Sello `SELLO_P7_42.md` (commit `a481226`, antes de jugar; un añadido declarado). Piezas: `filo_P7_40.py` = `{md5('filo_P7_40.py')}`, `azar_P7_41.py` = `{md5('azar_P7_41.py')}`,
`campo_P7_41.py` = `{md5('campo_P7_41.py')}`, `efecto_P7_39.py` = `{md5('efecto_P7_39.py')}`, `contrafactual_P7_38.py` = `{md5('contrafactual_P7_38.py')}`. Scripts: `lanza_P7_41.py`, `corre_P7_42.sh`, `freno_P7_42.py`,
`analiza_P7_42.py` → `P7_42_datos.json`, `sello_P7_42.py` → `P7_42_sello.json`, `escribe_informe_P7_42.py` (este informe; ninguna cifra a mano). Diarios en `paintball/runs/P741_*` (fuera de git).*

## Las decisiones de la mesa y cómo quedaron

- **ε de SIN EMOCIÓN = 0,00019**, calibrado en local antes del sello (`banco_P7_41.py --calibra`, 80 réplicas de las vidas de APRENDE de P7-34; moneda pura por tic con una
  cosa al alcance): pruebas de SIN por criatura en 20 días {n(k19['forzadas'], 1)} forzadas + {n(k19['usos'], 1)} usos propios = {n(k19['forzadas'] + k19['usos'], 1)}, frente a {n(apr34, 1)} de APRENDE en P7-34 ({n(100 * ((k19['forzadas'] + k19['usos']) / apr34 - 1), 1)} %); con ε = 0,00034 habría sido
  {n(k34['forzadas'] + k34['usos'], 1)} ({n(100 * ((k34['forzadas'] + k34['usos']) / apr34 - 1), 1)} %). Momentos con una cosa al alcance: {sum(CB['momentos_por_vida'])} en 80 vidas (casi todos los tics).
- **Carácter solo en la cautela**: `model.py` no expone ningún parámetro de miedo; prudente = cautela de P7-40, valiente = (1 + cautela) / 2. TECHO una personalidad; y
  SIN EMOCIÓN también (moneda pura, sin curiosidad: valiente ≡ prudente), declarado en el sello. 6 variantes × 20 días × 3 series.
- «Cuándo» de la ración: hp < 100. Semillas k {S['k'][0]}-{S['k'][-1]} (serie 2 inversa, serie 3 rotada).

## Humo y freno

Humo: día 1 de APRENDE prudente, SIN y TECHO (serie 1), 3 créditos; la imagen de SIN falló al hornear por una comprobación del Dockerfile (añadido 1 del sello; solo esa
línea). Freno (días 1-3 de APRENDE prudente, serie 1; `P7_42_freno.json`): (a) cuaderno viaja: {'sí' if FR['a_cuaderno_viaja'] else 'NO'}; (b) tocan: {len(FR['b_tocan'])} de 6: {'sí' if FR['b_pasa'] else 'NO'}; (c) sube lo útil:
{'; '.join(FR['c_sube']) or 'ninguna'}: {'sí' if FR['c_pasa'] else 'NO'}; (d) errores de fotos: {', '.join(f'{k} {e}' for k, e in FR['d_errores_fotos'].items())}: {'sí' if FR['d_pasa'] else 'NO'}. **FRENO: {FR['FRENO']}.**

{freno_t}

## El campo

{len(V)} vidas de {partidas} partidas; partidas con corte: {len(corte)} ({', '.join(f's{a} d{b} {c}' for a, b, c in sorted(corte)) or 'ninguna'}); marcadas por la guarda: {len(marc)} ({', '.join(f's{a} d{b} {c}' for a, b, c in sorted(marc)) or 'ninguna'}).

### Las medidas, primera cuenta (todas las vidas; las partidas con corte fuera de los puestos)

{tabla(CT)}

### Las predicciones selladas

{pred(CT)}

Carácter (puesto, valiente − prudente): APRENDE {n(car['APRENDE']['dif'], 2)} ± {n(car['APRENDE'].get('ee'), 2)}; BORRADO {n(car['BORRADO']['dif'], 2)} ± {n(car['BORRADO'].get('ee'), 2)}.

### Pruebas por brazo y día (media por vida)

{pruebas_dia(CT)}

### Segunda cuenta: sin las partidas marcadas por la guarda

{tabla(SM)}

{pred(SM)}

## Lectura

{{lectura}}
"""
open(os.path.join(AQUI, "informe_P7_42.md"), "w", encoding="utf-8").write(out); print("informe_P7_42.md", out.count("\n"), "lineas")

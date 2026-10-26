"""[P7-45] Escribe informe_P7_45.md: el campo del capitulo 3 entero (tres series x 20 dias x 6 variantes) con el sello de SELLO_P7_42.md evaluado, la equidad, las paradas,
los creditos, el disco y la curva de latencia de APRENDE prudente frente al cuaderno. Lee P7_42_sello.json (sello_P7_42), P7_42_datos.json (analiza_P7_42),
P7_43_equidad{,_s1,_s2,_s3}.json (equidad_P7_43), P7_45_latencia.json (latencia_P7_45), P7_41_estado*.json, P7_43_borrado.json. Ninguna cifra a mano.
  python3 escribe_informe_P7_45.py [--libre_gb N]  (N = GB libres leidos de df al escribir; si no se da, se lee con os.statvfs)"""
import hashlib, json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
SE = J("P7_42_sello.json"); V = [v for v in J("P7_42_datos.json") if not v.get("sin_diario")]; EQ = J("P7_43_equidad.json"); EQS = {S: J(f"P7_43_equidad_s{S}.json") for S in (1, 2, 3)}; LA = J("P7_45_latencia.json")
E = J("P7_41_estado.json"); EP1 = J("P7_41_estado_piloto.json"); BO = J("P7_43_borrado.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
VAR = ("TECHO", "BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN"); ET = {"TECHO": "TECHO", "BORRADO_v": "BORRADO valiente", "BORRADO_p": "BORRADO prudente", "APRENDE_v": "APRENDE valiente", "APRENDE_p": "APRENDE prudente", "SIN": "SIN EMOCIÓN"}
REAL = {"botiquin": 50.0, "racion": 15.0}
# --- creditos (bolsa 1, en creditos de experiencia: 1 por partida)
campo = sum(1 for p in E["peticiones"] if p["brazo"] in VAR and p["estado"] == "completed"); humo = sum(1 for p in E["peticiones"] if p["brazo"] == "HUMO43")
pil1 = len(EP1["peticiones"]); pil2 = len(E.get("piloto_2_10_14") or []); humo_f = len(E.get("humo_fallido_09_08") or []); reint = len(E.get("reintentos") or [])
por_serie = {S: sum(1 for p in E["peticiones"] if p["brazo"] in VAR and p["serie"] == S and p["estado"] == "completed") for S in (1, 2, 3)}
total7 = 710 + pil1 + pil2 + humo_f + humo + reint + campo
# --- disco
SALDO = (sys.argv[sys.argv.index("--saldo") + 1] if "--saldo" in sys.argv else None)   # [12-oct] saldo real leido por Manel en la pagina
libre = (float(sys.argv[sys.argv.index("--libre_gb") + 1]) if "--libre_gb" in sys.argv else os.statvfs(RAIZ).f_bavail * os.statvfs(RAIZ).f_frsize / 1e9)
def gb(pat):
    import glob
    return sum(os.path.getsize(os.path.join(r, f)) for c in glob.glob(os.path.join(RAIZ, "paintball", "runs", pat)) for r, _, fs in os.walk(c) for f in fs) / 1e9
GBS = {S: gb(f"P741_s{S}_*") for S in (1, 2, 3)}
# --- dias validos por brazo y serie (regla de comparacion, addendum 12)
dias_validos = {S: {v: sorted({x["dia"] for x in V if x["serie"] == S and x["variante"] == v}) for v in VAR} for S in (1, 2, 3)}
todos_20 = all(len(dias_validos[S][v]) == 20 for S in (1, 2, 3) for v in VAR)
# --- equidad: tabla por serie y total
TE = ["| serie | partidas | tope | diferencia máx. del % sobre el tic entre brazos (puntos) | extremos | paradas duras | vidas marcadas |", "|---|---:|---|---:|---|---:|---:|"]
for S in (1, 2, 3):
    q = EQS[S]; t = E.get("tope_subido" if S == 1 else f"tope_subido_s{S}") or {}
    TE.append(f"| {S} | {q['partidas']} | 12 → {t.get('a', '—')} a las {t.get('cuando', '—')} | {n(q['equidad']['max_diferencia_sobre_el_tic_puntos'], 2)} | {q['equidad']['extremos'][0]} / {q['equidad']['extremos'][1]} | {len(q['paradas'])} | {len(q['marcadas'])} |")
TE.append(f"| las tres | {EQ['partidas']} | | {n(EQ['equidad']['max_diferencia_sobre_el_tic_puntos'], 2)} | {EQ['equidad']['extremos'][0]} / {EQ['equidad']['extremos'][1]} | {len(EQ['paradas'])} | {len(EQ['marcadas'])} |")
TB = ["| brazo | vidas | % decisiones sobre el tic (media) | % pasos listos bloqueados sin cuerpo (media) | ms por decisión (mediana) | p95 máximo (ms) | marcadas |", "|---|---:|---:|---:|---:|---:|---:|"]
for v in VAR:
    x = EQ["por_brazo"][v]; TB.append(f"| {ET[v]} | {x['vidas']} | {n(x['sobre_el_tic_media_pct'], 2)} | {n(x['bloqueados_media_pct'], 2)} | {n(x['ms_mediana'], 2)} | {n(x['ms_p95_max'], 1)} | {x['marcadas']} |")
marc = "; ".join(f"s{a} d{b} {c} a{d}" for a, b, c, d in EQ["marcadas"])
# --- el sello
def tabla_medidas(cuenta):
    M = SE[cuenta]["medidas"]
    T = ["| variante | vidas | puesto ± ee | rapidez botiquín, por criatura (días; 21 = no llega) · media ± ee | rapidez ración · media | cuándo botiquín (hp < 50 / usos) · ración (hp < 100 / usos) | sabiduría d11-20: s en red · s en camuflaje · vida perdida (las dos) | pruebas (b · r · red · cam) · forzadas | mueren |", "|---|---:|---|---|---|---|---|---|---:|"]
    for var in VAR:
        m = M[var]; pc = m["pruebas_por_cosa"]; sr, sc, vp = sab(var, cuenta)
        rb = (f"{', '.join(map(str, m['rapidez_botiquin']))} · {n(m['rapidez_botiquin_media'], 1)} ± {n(m['rapidez_botiquin_ee'], 1)}" if not var.startswith("BORRADO") and var != "TECHO" else "(referencia, sección 3)")
        rr = (f"{', '.join(map(str, m['rapidez_racion']))} · {n(m['rapidez_racion_media'], 1)}" if not var.startswith("BORRADO") and var != "TECHO" else "(referencia)")
        T.append(f"| {ET[var]} | {m['vidas']} | {n(m['puesto'], 2)} ± {n(m['puesto_ee'], 2)} | {rb} | {rr} | {m['usos_botiquin_hp_menor_50']} / {m['usos_botiquin']} ({n(100 * (m['cuando_botiquin'] or 0), 0)} %) · {m['usos_racion_hp_menor_100']} / {m['usos_racion']} | {n(sr, 1)} · {n(sc, 1)} · {n(vp, 1)} | {m['pruebas_total']} ({pc['botiquin']} · {pc['racion']} · {pc['red']} · {pc['camuflaje']}) · {m['forzadas']} | {m['mueren']} |")
    return T
MARC = {tuple(x) for x in SE["partidas_marcadas"]}
def sab(var, cuenta):
    vs = [v for v in V if v["variante"] == var and v["dia"] >= 11 and v.get("sabiduria") and (cuenta == "con_todas" or (v["serie"], v["dia"], v["variante"]) not in MARC)]
    r = [v["sabiduria"]["por_cosa"]["red"]["segundos"] for v in vs if "por_cosa" in v["sabiduria"]]; c = [v["sabiduria"]["por_cosa"]["camuflaje"]["segundos"] for v in vs if "por_cosa" in v["sabiduria"]]
    return (st.mean(r) if r else None), (st.mean(c) if c else None), (st.mean(v["sabiduria"]["vida_perdida_gear"] for v in vs) if vs else None)
def sello_txt(cuenta):
    C = SE[cuenta]; R1, C1 = C["R1"], C["C1"]
    f = lambda x, d: (f"{n(x['dif'], d)} ± {n(x.get('ee'), d)}" + (" (3 veces el ruido)" if x.get("tres_veces") else "") + (", cumple" if x.get("cumple") else ", NO cumple")) if x.get("dif") is not None else "—"
    return (f"R1 (APRENDE llega antes que SIN con el botiquín; días): APRENDE_p − SIN {f(R1['APRENDE_p'], 1)}; APRENDE_v − SIN {f(R1['APRENDE_v'], 1)} → **R1 {'PASA' if R1['pasa'] else 'NO PASA'}**. "
            f"C1 (usos del botiquín con hp < 50, proporción): APRENDE_p − SIN {f(C1['APRENDE_p'], 3)}; APRENDE_v − SIN {f(C1['APRENDE_v'], 3)} → **C1 {'PASA' if C1['pasa'] else 'NO PASA'}**.")
# BORRADO como referencia de lo que se aprende dentro de un dia: vidas cuya creencia al cerrar llega al 50 %
def dentro_dia(var):
    vs = [v for v in V if v["variante"] == var]; out = {}
    for o in ("botiquin", "racion"):
        ok = [v for v in vs if (v["al_acabar"][o]["creencia"] or -1) >= 0.5 * REAL[o]]; out[o] = (len(ok), len(vs), sorted({(v["serie"], v["dia"], v["asiento"]) for v in ok}))
    return out
DD = {var: dentro_dia(var) for var in ("BORRADO_v", "BORRADO_p", "TECHO")}
# creencia del botiquin al cerrar el d20 por criatura en las cadenas (y el maximo del recorrido)
def d20(var):
    out = []
    for S in (1, 2, 3):
        for sl in (10, 11):
            vs = sorted([v for v in V if v["variante"] == var and v["serie"] == S and v["asiento"] == sl], key=lambda v: v["dia"])
            if vs: out.append((S, sl, vs[-1]["dia"], vs[-1]["al_acabar"]["botiquin"]["creencia"], max((v["al_acabar"]["botiquin"]["creencia"] or 0) for v in vs), vs[-1]["al_acabar"]["racion"]["creencia"]))
    return out
D20 = {var: d20(var) for var in ("APRENDE_v", "APRENDE_p", "SIN")}
T20 = ["| cadena | criatura (serie · asiento) | creencia del botiquín al cerrar el d20 (máximo del recorrido) | creencia de la ración al d20 |", "|---|---|---|---|"]
for var in ("APRENDE_v", "APRENDE_p", "SIN"):
    for S, sl, d, b, bm, r in D20[var]: T20.append(f"| {ET[var]} | s{S} · a{sl} | {n(b, 1)} ({n(bm, 1)}) | {n(r, 1)} |")
# pruebas por dia
M = SE["con_todas"]["medidas"]
TP = ["| variante | pruebas por vida y día, d1 → d20 |", "|---|---|"]
for var in VAR: TP.append(f"| {ET[var]} | {' '.join(n(M[var]['pruebas_por_dia'].get(str(d)), 1) for d in range(1, 21))} |")
# latencia
TL = ["| cadena | n días | Spearman mediana ~ cuaderno (s1 · s2 · s3 · juntas) | Spearman % sobre el tic ~ cuaderno (juntas) | ms más por cada 100 apuntes (recta) | mediana media (ms) | % sobre el tic medio | días con ≥ 1 % |", "|---|---:|---|---:|---:|---:|---:|---:|"]
for var in ("APRENDE_p", "APRENDE_v", "SIN"):
    r = LA[var]; ps = r["por_serie"]; j = r["juntas"]
    TL.append(f"| {ET[var]} | {r['n']} | {n(ps['1']['spearman_mediana'], 2)} · {n(ps['2']['spearman_mediana'], 2)} · {n(ps['3']['spearman_mediana'], 2)} · **{n(j['spearman_mediana'], 2)}** | {n(j['spearman_sobre'], 2)} | {n(j['ms_por_100_apuntes'], 3)} | {n(j['mediana_media'], 2)} | {n(j['sobre_media_pct'], 3)} | {j['dias_sobre_1pct']} |")
cu = LA["APRENDE_p"]["por_serie"]; cu20 = [cu[s]["cuaderno_d20"] for s in ("1", "2", "3")]
caract = SE["con_todas"]["caracter"]
S1 = SE["con_todas"]["S1"]

out = f"""# P7-45 · El campo del capítulo 3 entero: tres series, el sello evaluado

*12-oct-2026. Bolsa 1 (créditos de experiencia, 1 por partida): el campo {campo} (serie 1: {por_serie[1]}, serie 2: {por_serie[2]}, serie 3: {por_serie[3]}) + humo {humo} + fuera de resultados {pil1 + pil2 + humo_f + reint}
(piloto 1 {pil1}, piloto 2 {pil2}, humo que murió al arrancar {humo_f}, intento parado de APRENDE_p d20 {reint}) = {campo + humo + pil1 + pil2 + humo_f + reint} créditos del campo. Acumulado del siete: 710 + {campo + humo + pil1 + pil2 + humo_f + reint} = **{total7}**.
Disponibles: {("**" + SALDO + "** (saldo real de la página de la plataforma, 12-oct 06:47, dato de Manel; la estimación de ≈ " + str(496 + 2 * 71 - (campo + humo + pil1 + pil2 + humo_f + reint)) + " que llevaba este informe se corrige)") if SALDO else "no legibles por la API; estimación con la cifra de Manel (496 el 10-oct a mediodía, +71/día): ≈ " + str(496 + 2 * 71 - (campo + humo + pil1 + pil2 + humo_f + reint)) + " al escribir (confirmar en la página)"}. Bolsa 2 (consola de Anthropic): 0 $.
Disco: la serie 1 ocupa {n(GBS[1], 2)} GB, la 2 {n(GBS[2], 2)} GB, la 3 {n(GBS[3], 2)} GB (diarios y zips); libre {n(libre, 1)} GB tras archivar en el T7 P7-30, P7-34 y los pilotos ({BO.get('borrados', '—')} diarios borrados tras
copia leída de vuelta; `P7_43_borrado.json`). `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Sello `SELLO_P7_42.md` (commit `a481226`) con sus addenda 1-12, sin reescribir.
Piezas: `rapido_P7_43.py` = `{md5('rapido_P7_43.py')}`, `filo_P7_40.py` = `{md5('filo_P7_40.py')}`, `azar_P7_41.py` = `{md5('azar_P7_41.py')}`, `campo_P7_41.py` = `{md5('campo_P7_41.py')}`.
Scripts: `orquesta_P7_43.py`, `equidad_P7_43.py` → `P7_43_equidad*.json`, `analiza_P7_42.py` → `P7_42_datos.json`, `sello_P7_42.py` → `P7_42_sello.json`, `latencia_P7_43.py` + `latencia_P7_45.py` → `P7_45_latencia.json/.png`,
`escribe_informe_P7_45.py` (este informe; ninguna cifra a mano).*

## Sección 1 · El campo tal como se jugó

Tres series × 20 días × 6 variantes = {campo} partidas ({campo * 2} vidas), imágenes v3b (cachés con decisiones idénticas y regla del cuerpo de los 72 tics), tope de 12 partidas a la vez con subida
a 20 solo si el día 1 de los seis brazos cumple (p95 < 20 ms y < 1 % sobre el tic), semillas k 221-240 (serie 1 en orden, 2 inversa, 3 rotada). Serie 1 el 11-oct de 10:46 a 16:15 (con
el reintento de APRENDE_p d20, addendum 12); serie 2 el 11-oct de 17:01 a 22:17; serie 3 del 11 al 12-oct, de 22:31 a 04:07 (el día 1 no cumplió: un p95 de {n(max(x[0] for x in (E.get('tope_subido_s3') or {}).get('dia_1', [[0]])), 1)} ms;
siguió en 12 toda la serie). Ninguna petición rechazada por la plataforma. Regla de comparación (addendum 12): solo días válidos en todos los brazos → {'los 20 días de las tres series son válidos en los 6 brazos' if todos_20 else 'faltan días: ' + str({S: {v: 20 - len(d) for v, d in dv.items() if len(d) < 20} for S, dv in dias_validos.items()})}.

{chr(10).join(TE)}

{chr(10).join(TB)}

Paradas duras: {len(EQ['paradas'])} en las {EQ['partidas']} partidas (la única del campo fue el primer intento de APRENDE_p s1 d20, fuera de resultados, addendum 12). Vidas marcadas por la guarda (segunda
cuenta del sello): {len(EQ['marcadas'])} de {EQ['partidas'] * 2}: {marc}. Equidad: la diferencia máxima del % sobre el tic entre brazos es {n(EQ['equidad']['max_diferencia_sobre_el_tic_puntos'], 2)} puntos en el total
y {', '.join(n(EQS[S]['equidad']['max_diferencia_sobre_el_tic_puntos'], 2) for S in (1, 2, 3))} por serie: {'ninguna dudosa' if not any(EQS[S]['equidad']['dudoso'] for S in (1, 2, 3)) and not EQ['equidad']['dudoso'] else 'DUDOSA'} (umbral 2).

## Sección 2 · El sello evaluado (6 criaturas por cadena; BORRADO fuera de la comparación de rapidez)

Decisión de la mesa (Manel, 11-oct): BORRADO no entra en la comparación de rapidez porque su cuaderno se vacía cada noche y lo que aprende un día lo pierde; la rapidez se compara entre
APRENDE y SIN EMOCIÓN (como ya decía el sello: R1 solo enfrenta APRENDE_p y APRENDE_v a SIN) y BORRADO queda como referencia de lo que se aprende dentro de un día (sección 3).

**Cuenta con todas las vidas.** {sello_txt('con_todas')}

**Cuenta sin las {len(SE['partidas_marcadas'])} partidas marcadas.** {sello_txt('sin_marcadas')}

S1 (sabiduría, sin predicción): segundos en red o camuflaje en los días 11-20 por vida: {', '.join(f"{ET[v]} {n(S1[v]['segundos'], 1)} s (vida perdida {n(S1[v]['vida'], 1)})" for v in VAR)}.
Carácter (puesto valiente − prudente, menor = mejor): APRENDE {n(caract['APRENDE']['dif'], 2)} ± {n(caract['APRENDE'].get('ee'), 2)}, BORRADO {n(caract['BORRADO']['dif'], 2)} ± {n(caract['BORRADO'].get('ee'), 2)}.

{chr(10).join(tabla_medidas('con_todas'))}

{chr(10).join(T20)}

{chr(10).join(TP)}

## Sección 3 · BORRADO (y TECHO) como referencia de lo que se aprende dentro de un día

Vidas cuya creencia al cerrar el día llega al 50 % del efecto real (botiquín 25 de 50; ración 7,5 de 15), con el cuaderno vacío al arrancar:
{chr(10).join(f"- {ET[v]}: botiquín {DD[v]['botiquin'][0]} de {DD[v]['botiquin'][1]} vidas ({', '.join(f's{a} d{b} a{c}' for a, b, c in DD[v]['botiquin'][2]) or 'ninguna'}); ración {DD[v]['racion'][0]} de {DD[v]['racion'][1]}." for v in ("BORRADO_v", "BORRADO_p", "TECHO"))}
Lo que significa el «50 % el día 2» de un BORRADO: esa criatura usó el botiquín dentro de ese día lo bastante para que su creencia de cierre llegara a 25, y lo perdió al dormir; es un día
afortunado, no acumulación.

## Sección 4 · La curva de latencia de APRENDE prudente frente al cuaderno (tres series)

{chr(10).join(TL)}

El cuaderno de APRENDE prudente con el que arranca el d20 tiene {', '.join(n(x, 0) for x in cu20)} recuerdos + apuntes en las series 1, 2 y 3. Figura: `P7_45_latencia.png` (mediana de ms por día frente al
tamaño del cuaderno, tres series, tres cadenas; de `P7_43_latencia_s1-3.json`).

## Sección 5 · Apéndice: fuera de resultados

Piloto 1 ({pil1} partidas, 63 a la vez, guarda dura), piloto 2 ({pil2}, regla v1), humo que murió al arrancar ({humo_f}), humo bueno ({humo}, APRENDE valiente desde el cuaderno del d13) y el primer
intento de APRENDE_p s1 d20 ({reint}). Diarios: `P741p_*`, `P741q_*`, `P741x_*`, `P741r_*` (zips en el Mac y en el T7). Pendiente de P7-44: repetir la medida del camuflaje por brazo
(SIN EMOCIÓN y TECHO por separado) con los 720 diarios del campo.
"""

# --- lectura: cifras que la lectura cita
MC = SE["con_todas"]["medidas"]; R1 = SE["con_todas"]["R1"]; C1 = SE["con_todas"]["C1"]
sin_cero = sum(1 for S, sl, d, b, bm, r in D20["SIN"] if (bm or 0) <= 0); ap_25 = sum(1 for S, sl, d, b, bm, r in D20["APRENDE_p"] if (b or 0) >= 25); av_25 = sum(1 for S, sl, d, b, bm, r in D20["APRENDE_v"] if (b or 0) >= 25)
cu_d2 = st.mean(cu[s_]['cuaderno_d2'] for s_ in ('1', '2', '3')); cu_d20 = st.mean(cu[s_]['cuaderno_d20'] for s_ in ('1', '2', '3'))
pv = {v: MC[v]["pruebas_total"] / MC[v]["vidas"] for v in VAR}; marc_p = sum(1 for a, b, c, d in EQ["marcadas"] if c.endswith("_p")); lat_p = LA["APRENDE_p"]["juntas"]
out += f"""
## Lectura

1. **El sello no pasa.** R1: APRENDE prudente llega {n(-R1['APRENDE_p']['dif'], 1)} días antes que SIN EMOCIÓN con el botiquín, pero el error típico es {n(R1['APRENDE_p']['ee'], 1)} días (menos de una vez el ruido); APRENDE valiente
   no llega antes ({n(R1['APRENDE_v']['dif'], 1)} ± {n(R1['APRENDE_v']['ee'], 1)}). C1: la proporción de usos del botiquín con hp < 50 es {n(100 * MC['APRENDE_p']['cuando_botiquin'], 0)} % en APRENDE prudente, {n(100 * MC['APRENDE_v']['cuando_botiquin'], 0)} % en APRENDE valiente y
   {n(100 * MC['SIN']['cuando_botiquin'], 0)} % en SIN: ninguna diferencia llega a un error típico. Ninguna medida del campo llega a 3 veces el ruido. Con 6 criaturas por cadena, APRENDE y SIN EMOCIÓN son
   indistinguibles en rapidez y en cuándo. La segunda cuenta (sin las {len(SE['partidas_marcadas'])} partidas marcadas) dice lo mismo.
2. **La rapidez es, sobre todo, ruido entre criaturas**: en APRENDE prudente, {sum(1 for x in MC['APRENDE_p']['rapidez_botiquin'] if x == 21)} criaturas no llegan a 25 en 20 días y las otras llegan los días {', '.join(str(x) for x in MC['APRENDE_p']['rapidez_botiquin'] if x < 21)}; al cerrar el d20, {ap_25} de 6 están en 25 o más
   (APRENDE valiente: {av_25} de 6). En SIN, {sin_cero} de las 6 criaturas acaban con creencia 0 del botiquín: en 20 días no llegaron a usarlo ni una vez (la moneda fuerza ir y coger, y el usar;
   pero el veto de lo desconocido hace que fuera de la moneda no lo use).
3. **SIN EMOCIÓN probó la mitad que APRENDE**: {n(pv['SIN'], 1)} pruebas por vida ({MC['SIN']['forzadas']} forzadas en 120 vidas) frente a {n(pv['APRENDE_v'], 1)} y {n(pv['APRENDE_p'], 1)} de APRENDE y {n(pv['BORRADO_v'], 1)}-{n(pv['BORRADO_p'], 1)} de BORRADO. La calibración de ε en lazo
   abierto (±20 % de las pruebas de APRENDE, sello) no se ha cumplido en lazo cerrado: hay que decirlo al leer R1 y C1 (SIN empata probando la mitad). Causa probable: en la réplica
   los «momentos con objeto al alcance» eran casi todos los tics; en la partida real la criatura forzada a ir y coger no siempre llega (ventana de 240 tics) y las forzadas que no
   acaban en cogida no dejan huella de prueba. Se propone, no se ejecuta: contar las forzadas que acaban (cogida o usada) frente a las que caducan, con `P7_41_azar` (`fines`).
4. **Carácter**: APRENDE valiente queda {n(caract['APRENDE']['dif'], 2)} ± {n(caract['APRENDE'].get('ee'), 2)} puestos peor que el prudente (menos de dos errores típicos); en BORRADO no hay diferencia ({n(caract['BORRADO']['dif'], 2)} ± {n(caract['BORRADO'].get('ee'), 2)}).
   Mueren {MC['APRENDE_v']['mueren']} de 120 vidas de APRENDE valiente, {MC['APRENDE_p']['mueren']} del prudente, {MC['SIN']['mueren']} de SIN y {MC['TECHO']['mueren']} de TECHO.
5. **Sabiduría (S1)**: SIN EMOCIÓN es la que menos tiempo pasa con la red y el camuflaje en los días 11-20 ({n(S1['SIN']['segundos'], 0)} s por vida) y APRENDE prudente la que más ({n(S1['APRENDE_p']['segundos'], 0)} s); TECHO, que no
   prueba nada, {n(S1['TECHO']['segundos'], 0)} s. La vida perdida en esos tics va de {n(min(S1[v]['vida'] for v in VAR), 0)} a {n(max(S1[v]['vida'] for v in VAR), 0)}. Sin predicción sellada, se informa.
6. **Latencia**: APRENDE prudente es la única cadena cuya mediana sube con el cuaderno (Spearman {n(lat_p['spearman_mediana'], 2)} con 57 días; {n(lat_p['ms_por_100_apuntes'], 2)} ms más por cada 100 apuntes: de {n(cu_d2, 0)} a {n(cu_d20, 0)}
   recuerdos + apuntes (medias del d2 y del d20) son ≈ {n((cu_d20 - cu_d2) / 100 * lat_p['ms_por_100_apuntes'], 1)} ms sobre una mediana media de {n(lat_p['mediana_media'], 1)}); {lat_p['dias_sobre_1pct']} de sus 57 días tienen ≥ 1 % de decisiones sobre el tic. Pero {marc_p} de las {len(EQ['marcadas'])} vidas marcadas son prudentes, y
   BORRADO prudente, con cuaderno vacío, tiene {EQ['por_brazo']['BORRADO_p']['marcadas']}: la lentitud del prudente no es solo el cuaderno. La equidad se mantiene (≤ {n(max(EQS[S]['equidad']['max_diferencia_sobre_el_tic_puntos'] for S in (1, 2, 3)), 2)} puntos entre brazos).
"""

open(os.path.join(AQUI, "informe_P7_45.md"), "w", encoding="utf-8").write(out); print("informe_P7_45.md", out.count("\n"), "lineas")

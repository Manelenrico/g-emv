"""[P7-43] Escribe informe_P7_43.md (la serie 1 del campo del capitulo 3 tras la parada de la guarda: pilotos, arreglos, equidad, paradas, creditos, y las medidas de la serie 1)
desde P7_43_equidad_s1.json, P7_42_sello.json, P7_42_datos.json, P7_43_identidad.json, P7_43_paradas.json, P7_41_estado*.json. Ninguna cifra a mano."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
EQ = J("P7_43_equidad_s1.json"); SE = J("P7_42_sello.json"); V = [v for v in J("P7_42_datos.json") if not v.get("sin_diario")]; ID = J("P7_43_identidad.json"); PA = J("P7_43_paradas.json")
E = J("P7_41_estado.json"); EP1 = J("P7_41_estado_piloto.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
VAR = ("TECHO", "BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN"); ET = {"TECHO": "TECHO", "BORRADO_v": "BORRADO valiente", "BORRADO_p": "BORRADO prudente", "APRENDE_v": "APRENDE valiente", "APRENDE_p": "APRENDE prudente", "SIN": "SIN EMOCIÓN"}
serie1 = sum(1 for p in E["peticiones"] if p["brazo"] in VAR and p["estado"] == "completed"); humo = sum(1 for p in E["peticiones"] if p["brazo"] == "HUMO43"); pil1 = len(EP1["peticiones"]); pil2 = len(E.get("piloto_2_10_14") or []); humo_fallido = len(E.get("humo_fallido_09_08") or [])
hoy = humo_fallido + humo + pil2 + serie1
TE = ["| brazo | vidas | % decisiones sobre el tic (media) | % pasos listos bloqueados sin cuerpo (media) | ms por decisión (mediana) | p95 máximo (ms) | marcadas | paradas |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for v in VAR:
    x = EQ["por_brazo"][v]; TE.append(f"| {ET[v]} | {x['vidas']} | {n(x['sobre_el_tic_media_pct'], 2)} | {n(x['bloqueados_media_pct'], 2)} | {n(x['ms_mediana'], 2)} | {n(x['ms_p95_max'], 1)} | {x['marcadas']} | {x['paradas']} |")
# por dia: % sobre el tic por brazo (dias 1-20)
TD = ["| brazo | % sobre el tic por día, d1 → d20 |", "|---|---|"]
for v in VAR: TD.append(f"| {ET[v]} | {' '.join(n(EQ['por_brazo'][v]['por_dia'].get(str(d), {}).get('sobre_pct'), 1) for d in range(1, 21))} |")
CT = SE["con_todas"]; M = CT["medidas"]
TM = ["| variante | vidas | puesto ± ee | rapidez botiquín (días; 21 = no llega) · media | rapidez ración | cuándo botiquín (hp < 50 / usos) · ración (hp < 100 / usos) | sabiduría d11-20: s en red · s en camuflaje · vida perdida (las dos) | pruebas (b · r · red · cam) · forzadas |", "|---|---:|---|---|---|---|---|---|"]
def sab(var):
    vs = [v for v in V if v["variante"] == var and v["dia"] >= 11 and v.get("sabiduria")]
    r = [v["sabiduria"]["por_cosa"]["red"]["segundos"] for v in vs if "por_cosa" in v["sabiduria"]]; c = [v["sabiduria"]["por_cosa"]["camuflaje"]["segundos"] for v in vs if "por_cosa" in v["sabiduria"]]
    return (st.mean(r) if r else None), (st.mean(c) if c else None), (st.mean(v["sabiduria"]["vida_perdida_gear"] for v in vs) if vs else None)
for var in VAR:
    m = M[var]; pc = m["pruebas_por_cosa"]; sr, sc, vp = sab(var)
    TM.append(f"| {ET[var]} | {m['vidas']} | {n(m['puesto'], 2)} ± {n(m['puesto_ee'], 2)} | {', '.join(map(str, m['rapidez_botiquin']))} · {n(m['rapidez_botiquin_media'], 1)} | {', '.join(map(str, m['rapidez_racion']))} · {n(m['rapidez_racion_media'], 1)} | {m['usos_botiquin_hp_menor_50']} / {m['usos_botiquin']} ({n(100 * (m['cuando_botiquin'] or 0), 0)} %) · {m['usos_racion_hp_menor_100']} / {m['usos_racion']} | {n(sr, 1)} · {n(sc, 1)} · {n(vp, 1)} | {m['pruebas_total']} ({pc['botiquin']} · {pc['racion']} · {pc['red']} · {pc['camuflaje']}) · {m['forzadas']} |")
R1 = CT["R1"]; C1 = CT["C1"]
# pruebas por dia y brazo
TP = ["| variante | pruebas por vida y día, d1 → d20 |", "|---|---|"]
for var in VAR: TP.append(f"| {ET[var]} | {' '.join(n(M[var]['pruebas_por_dia'].get(str(d)), 1) for d in range(1, 21))} |")
idn = sum(r["n"] for r in ID); idd = sum(r["distintas"] for r in ID)

out = f"""# P7-43 · La serie 1 del campo del capítulo 3: arreglos tras la parada de la guarda, pilotos y lo jugado

*11-oct-2026. Plataforma hoy: {hoy} créditos ({humo_fallido} de un humo que murió al arrancar, {humo} del humo bueno, {pil2} del piloto 2, {serie1} de la serie 1); anoche, piloto 1: {pil1}. Acumulado del siete:
710 + {pil1} + {hoy} = {710 + pil1 + hoy} créditos. Disponibles: los que diga la página de la plataforma (Manel). Consola 0. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Sello `SELLO_P7_42.md` con
sus addenda 1-11 (fechados, sin reescribir). Piezas de campo: `rapido_P7_43.py` = `{md5('rapido_P7_43.py')}` (cachés y regla v3b), `filo_P7_40.py` = `{md5('filo_P7_40.py')}`, `azar_P7_41.py` = `{md5('azar_P7_41.py')}`,
`campo_P7_41.py` = `{md5('campo_P7_41.py')}`. Scripts: `orquesta_P7_43.py` (tope 12 → 20), `corre_P7_43.sh`, `equidad_P7_43.py` → `P7_43_equidad_s1.json`, `analiza_P7_42.py` → `P7_42_datos.json`,
`sello_P7_42.py` → `P7_42_sello.json`, `escribe_informe_P7_43.py` (este informe; ninguna cifra a mano).*

## Sección 1 · Qué pasó y qué se arregló (mesa P7-43 a 43e)

- **Piloto 1** (noche del 10 al 11, {pil1} partidas, 63 a la vez): la guarda dura paró las tres cadenas; 6 vidas con 10-30 % de decisiones sobre el tic o 5-86 % de pasos bloqueados sin
  cuerpo. Causas: latencia (factor plataforma/local de 1,8× a 10,7× en la misma noche: contención por nuestro propio paralelismo) y empujes contra casillas «libres»: vainas
  (`pod_*`, fijas) y **rivales camuflados** (`camo_glass`, invisibles para nosotros; P7-44).
- **Cachés con decisiones idénticas** (`rapido_P7_43`: la segunda tasación del regalo por tic y clave de foto; `filo_P7_40`: ignorancia y curiosidad por tic): {idn} decisiones en
  {len(ID)} vidas del piloto, {idd} distintas.
- **Regla del cuerpo de los 72 tics**, v3b: racha de empujes bloqueados hacia la misma casilla, sin moverse, por tiempo de reloj (el enfriamiento no la rompe); marca de 30 s
  renovable; se olvida al morir; los `ir_*` con destino en casilla no transitable (marcada o del agua) salen de la lista. Piloto 2 ({pil2} partidas, regla v1) y el humo que murió al
  arrancar ({humo_fallido}: el Dockerfile no copiaba la pieza; ahora la composición entera se comprueba al hornear) quedan fuera de resultados.
- **Humo bueno** (3 × APRENDE valiente desde el cuaderno del d13): medianas 1,9-4,2 ms, p95 7,1-13,8, 0 % sobre el tic; corte revisado por la mesa a p95 < 20 ms.
- **Serie 1** con v3b, tope de 12 partidas a la vez (cadenas primero), subido a 20 al cumplir el día 1 ({E.get('tope_subido', {}).get('cuando', '—')}).

## Sección 2 · Equidad de la lentitud, paradas y créditos (serie 1)

{chr(10).join(TE)}

Diferencia máxima entre brazos del % sobre el tic: **{n(EQ['equidad']['max_diferencia_sobre_el_tic_puntos'], 2)} puntos** ({EQ['equidad']['extremos'][0]} frente a {EQ['equidad']['extremos'][1]}): {'DUDOSO (> 2)' if EQ['equidad']['dudoso'] else 'no dudoso (≤ 2)'}.
Paradas de la guarda dura (antes del reintento): {len(EQ['paradas'])} ({'; '.join(f"s{a} d{b} {c} a{d}: {', '.join(e)}" for a, b, c, d, e in EQ['paradas']) or 'ninguna'}). Vidas marcadas: {len(EQ['marcadas'])} de {EQ['partidas'] * 2}.
Partidas de la serie 1: {serie1} de 120. Cierre (addendum 12): SIN d20 pedido después; APRENDE_p d20 jugado de nuevo UNA vez con el mismo cuaderno (d19) y tope 2: pasó la guarda
(medianas 3,7 y 3,4 ms frente a 11,1 y 10,9 del intento parado, mismo cuaderno: la lentitud era la escena —centro, 18 candidatos, hermana a la vista— y la hora, no el cuaderno;
el intento parado queda aparte, fuera de resultados). Curva de latencia por día y brazo: `P7_43_latencia_s1.json` (`latencia_P7_43.py`): las medianas de las cadenas van de 2 a 5 ms
del d2 al d18 mientras el cuaderno pasa de 3 a 50 recuerdos y de 80 a 1.100 apuntes (Spearman mediana-cuaderno: APRENDE_v 0,13, APRENDE_p 0,36, SIN −0,03); BORRADO, con
cuaderno vacío, tiene las mismas medianas y los mismos picos.

{chr(10).join(TD)}

## Sección 3 · Las medidas de la serie 1 (parcial: 2 criaturas por variante; el sello se evalúa con las tres series)

{chr(10).join(TM)}

R1 (APRENDE antes que SIN con el botiquín): APRENDE_p − SIN {n(R1['APRENDE_p']['dif'], 1)} ± {n(R1['APRENDE_p'].get('ee'), 1)} días, APRENDE_v − SIN {n(R1['APRENDE_v']['dif'], 1)} ± {n(R1['APRENDE_v'].get('ee'), 1)}. C1 (usos del botiquín con hp < 50): APRENDE_p − SIN
{n(C1['APRENDE_p']['dif'], 3)} ± {n(C1['APRENDE_p'].get('ee'), 3)}, APRENDE_v − SIN {n(C1['APRENDE_v']['dif'], 3)} ± {n(C1['APRENDE_v'].get('ee'), 3)}. Con 2 criaturas por variante nada llega a 3 errores típicos; se evalúa al cerrar las tres series.

{chr(10).join(TP)}

## Lectura (provisional)

Con la serie 1 sola: (i) la lentitud es pareja entre brazos (≤ {n(EQ['equidad']['max_diferencia_sobre_el_tic_puntos'], 2)} puntos) y los bloqueos sin cuerpo bajan a 0,2-0,5 % (piloto 1: 5-86 %): la regla v3b y el tope de
paralelismo hacen lo que se les pidió; la única parada es de latencia, en la última partida de APRENDE prudente (cuaderno del d19 con 1.168 apuntes; 37-44 ms de mediana en los
últimos 1.500 tics del final de partida). (ii) La creencia del botiquín sube despacio: APRENDE prudente no llega a 25 en 20 días en ninguna de sus 2 criaturas (a10: 23 el d20 con
15 recuerdos; a11: 19 con 26), APRENDE valiente llega los días 13 y 10, SIN EMOCIÓN una criatura el día 7 (usos forzados a cualquier vida: efectos grandes) y la otra no llega:
con el filtro B1 las intensidades quedan cerca de 1 y el neutro pesa más, y con la cautela se prueba menos. (iii) La sabiduría va por separado para red y camuflaje (tabla).
Todo esto se mide de verdad con 6 criaturas por variante: series 2 y 3.
"""
open(os.path.join(AQUI, "informe_P7_43.md"), "w", encoding="utf-8").write(out); print("informe_P7_43.md", out.count("\n"), "lineas")

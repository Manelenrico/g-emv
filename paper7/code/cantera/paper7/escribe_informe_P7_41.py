"""[P7-41] Escribe informe_P7_41.md (el plan del campo del capitulo 3) desde P7_41_comprobacion.json (banco_P7_41), P7_34_datos.json (el ruido), semillas_P7_41.json y los md5 de las piezas. Ninguna cifra a mano."""
import hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
CO = J("P7_41_comprobacion.json"); V = [v for v in J("P7_34_datos.json") if not v.get("sin_diario")]; S = J("semillas_P7_41.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
REAL = {"botiquin": 50.0, "racion": 15.0}; TIC = 1000.0 / 24.0
# ── el ruido de P7-34 ──
rap = {}
for b in ("APRENDE", "BORRADO"):
    for o in ("botiquin", "racion"):
        dias = []
        for s in (1, 2):
            for sl in (10, 11):
                vs = sorted([v for v in V if v["brazo"] == b and v["serie"] == s and v["asiento"] == sl], key=lambda v: v["dia"])
                dias.append(next((v["dia"] for v in vs if (v["al_acabar"][o]["creencia"] or -1) >= 0.5 * REAL[o]), 21))    # no llega = 21 (declarado)
        rap[(b, o)] = dias
sd_rap = st.pstdev(rap[("APRENDE", "botiquin")] + rap[("BORRADO", "botiquin")])
cuando = {}
for b in ("APRENDE", "BORRADO"):
    hp = [h for v in V if v["brazo"] == b for h in v["pruebas"]["botiquin"]["hp_al_abrir"] if h is not None]; p = sum(1 for h in hp if h < 50) / len(hp)
    cuando[b] = (len(hp), p, (p * (1 - p) / len(hp)) ** 0.5)
puesto = {b: ([v["puesto"] for v in V if v["brazo"] == b and v["puesto"] is not None]) for b in ("APRENDE", "BORRADO", "TECHO")}
sd_puesto = st.pstdev(puesto["APRENDE"] + puesto["BORRADO"])
gear = {b: [v["coge"]["red"] + v["coge"]["camuflaje"] for v in V if v["brazo"] == b and v["dia"] >= 11] for b in ("APRENDE", "BORRADO", "TECHO")}
# ── diseno de replicas: para cada numero de series S (2 o 3), criaturas por variante = 2S (dos asientos), vidas = 20 x 2S ──
def disenio(Ss):
    cr = 2 * Ss; vidas = 20 * cr; ee_rap = sd_rap / cr ** 0.5; ee_puesto = sd_puesto / vidas ** 0.5
    usos = cuando["APRENDE"][0] / 80 * vidas; p = cuando["APRENDE"][1]; ee_c = (p * (1 - p) / usos) ** 0.5
    return {"series": Ss, "criaturas_por_variante": cr, "vidas_por_variante": vidas, "partidas": 9 * 20 * Ss, "ee_rapidez_dias": ee_rap, "detecta_rapidez_dias": 3 * (2 ** 0.5) * ee_rap, "ee_puesto": ee_puesto, "detecta_puesto": 3 * (2 ** 0.5) * ee_puesto, "usos_botiquin": usos, "ee_cuando": ee_c, "detecta_cuando": 3 * (2 ** 0.5) * ee_c}
D2, D3 = disenio(2), disenio(3)
# ── la comprobacion ──
R = CO["vidas"]; err = [r for r in R if r.get("error")]
sin = [r for r in R if r["brazo"] == "SIN"]; ap = [r for r in R if r["brazo"] in ("APRENDE", "BORRADO")]
def eps_fila(eps):
    x = [r for r in sin if r["eps"] == eps]; op = sum(r["azar"]["oportunidades"] for r in x); si = sum(r["azar"]["monedas_si"] for r in x); fz = sum(r["azar"]["forzadas"] for r in x)
    pm = [r["azar"]["p_medio"] for r in x if r["azar"]["p_medio"] is not None]; fines = {k: sum(r["azar"]["fines"][k] for r in x) for k in ("cogida", "usada", "caduca")}
    return f"| {n(eps, 2)} | {len(x)} | {op} | {si} ({n(100 * si / op, 1) if op else '—'} %) | {n(st.mean(pm), 3) if pm else '—'} | {fz} ({', '.join(f'{k} {c}' for k, c in fines.items())}) | {sum(r['azar']['vetos'] for r in x)} | {sum(r['azar']['elegidas_desconocidas_sin_forzar'] for r in x)} |"
ms_all = [r["ms"] for r in R if r.get("ms")]
TL = ["| configuración | vidas | ms por decisión: mediana (máx entre vidas) · p90 (máx) · máximo | fidelidad al diario (suma) |", "|---|---:|---|---|"]
for key in sorted({(r["brazo"], r["eps"], r["miedo"]) for r in R}):
    x = [r for r in R if (r["brazo"], r["eps"], r["miedo"]) == key and r.get("ms")]
    TL.append(f"| {key[0]} ε={n(key[1], 2)} {key[2]} | {len(x)} | {n(max(r['ms']['mediana'] for r in x), 2)} · {n(max(r['ms']['p90'] for r in x), 1)} · {n(max(r['ms']['max'] for r in x), 1)} | {sum(r['fidelidad'].get('igual', 0) for r in x)} · {sum(r['fidelidad'].get('difiere', 0) for r in x)} |")

out = f"""# P7-41 · Preparar el campo del capítulo 3 (segunda etapa): plan, comprobación y coste

*10-oct-2026. Nada lanzado en la plataforma: plataforma 0 créditos (acumulado del siete 710; disponibles el 10-oct, dato de Manel: 496 de 1.000, +71/día); consola 0 USD.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`; cuerpo y congelados sin tocar. Piezas nuevas del campo: `azar_P7_41.py` (= `{md5('azar_P7_41.py')}`), `campo_P7_41.py`
(= `{md5('campo_P7_41.py')}`), `policy_pareja_P7_41.py`, `Dockerfile.pareja_P7_41`, `lanza_P7_41.py`, `semillas_P7_41.json` (propuestas); criatura que aprende = P7-40 tal como quedó
sellado: `filo_P7_40.py` (= `{md5('filo_P7_40.py')}`; añadidos de campo: personalidad, caché por tic y apuntes dentro del cuaderno, sin tocar la regla de los apuntes), sobre
B1 de P7-39 (`efecto_P7_39.py` = `{md5('efecto_P7_39.py')}`, `contrafactual_P7_38.py` = `{md5('contrafactual_P7_38.py')}` sin contrafactual ni pistas). Comprobación: `banco_P7_41.py` → `P7_41_comprobacion.json`.
Este informe lo escribe `escribe_informe_P7_41.py`; ninguna cifra a mano. **Espera el visto bueno de Manel antes de lanzar.***

## Sección 1 · El diseño

- **Criatura que aprende**: P7-40 sellado (esperanza de clase como punto de partida; cautela por distancia sobre la curiosidad; miradas y apuntes de lo visto en peligro,
  tomados por su mayor, sin tocar). Importancia como B1 (sin las filas de la curiosidad ni las del acto, sin contrafactual); intensidad 1 + importancia; cuaderno que viaja.
- **Brazos** (9 variantes = imágenes): TECHO (nace sabiendo; el miedo no tiene palanca en él: una sola personalidad); BORRADO y APRENDE × {{valiente, prudente}};
  SIN EMOCIÓN con ε = 0,05 y ε = 0,2 × {{valiente, prudente}}. Las variantes con cuaderno que viaja (APRENDE y SIN) van en cadena de 20 días; TECHO y BORRADO son fijas.
- **SIN EMOCIÓN** (definiciones propuestas; `azar_P7_41.py`): mismo cuerpo, misma percepción, mismos recuerdos y misma creencia (importancia B1); sin curiosidad
  (`GEMV_P7_NOVEDAD=0`: ni `R-CURIOSIDAD` ni `ir_curioso`), sin esperanza de clase ni apuntes. **Veto**: el cuerpo no coge ni usa por sí solo nada de clase desconocida (sin
  recuerdos) —sin el veto cogería redes por empate, como TECHO en P7-36—. **Oportunidad**: cada vez que una cosa de clase desconocida entra a su alcance (a la vista y sin
  llevarla; o, un consumible desconocido, cuando entra en el zurrón) se tira UNA moneda con probabilidad ε × miedo; una oportunidad por (cosa, casilla) mientras siga a la
  vista, y vuelve a contar si deja de verse 48 tics. **Prueba forzada**: si sale, durante hasta 240 tics va a la cosa (`ir_azar`) y la coge; un consumible desconocido en el
  zurrón se usa en el primer tic en que `usar_*` es candidato. La prueba y su recuerdo son los de P7-33.
- **Personalidades** (PROPUESTA, pendiente: no encuentro en el ACTA ni en los informes los «pesos del miedo como se decidió»; en P7-26 lo que se midió fue la escala de la
  curiosidad ×1/×2 con la cautela): **prudente** = cautela por distancia tal cual (1 sin rivales a 8 o menos; 0 con rival a 2, fuera del círculo o vida < 30; la de P7-40);
  **valiente** = (1 + cautela) / 2 (nunca por debajo de 0,5: el valiente sigue probando cerca del peligro a medias). El mismo factor multiplica la curiosidad de clase en
  APRENDE/BORRADO y la probabilidad ε en SIN EMOCIÓN.
- Lo desconocido: botiquín, ración, red y camuflaje (como P7-33). Ojos compartidos apagados. Pedir corregido y lo dado entregado. Guardas de P7-30.
- **Semillas** (propuestas, se declaran definitivas al lanzar): k = {S['k'][0]}-{S['k'][-1]} (las siguientes a P7-34); serie 1 {S['serie1'][0]}, …, {S['serie1'][-1]}; serie 2 en orden inverso; serie 3 rotada diez
  posiciones. La misma semilla para las 9 variantes cada día.

## Sección 2 · Comprobación previa, en local (coste cero)

Réplicas en lazo abierto (las obs son las de los diarios de P7-34, s1 d1 y d10, asientos 10 y 11; lo que cambia es lo que la réplica decide y escribe), una vida por proceso,
con la composición exacta del campo (`campo_P7_41` sobre `nace_P7_33.aplica`). {len(R)} vidas, {len(err)} errores.

| ε | vidas SIN | oportunidades | monedas que salen (fracción real) | ε × miedo (media) | pruebas forzadas (cómo acaban) | vetos (candidatos `coger`/`usar_*` de clase desconocida quitados) | decisiones `coger`/`usar_*` de clase desconocida sin forzar |
|---|---:|---:|---|---|---|---:|---:|
{eps_fila(0.0)}
{eps_fila(0.05)}
{eps_fila(0.2)}

- SIN EMOCIÓN corre; con ε = 0 no hay ninguna prueba de lo desconocido (0 forzadas, 0 decisiones de coger o usar lo desconocido sin forzar; el veto quita los candidatos).
- ε se cumple en la moneda: la fracción real de monedas que salen sigue a ε × miedo dentro de lo que cabe con tan pocas oportunidades (día 1: solo cuentan las cosas aún
  desconocidas; el día 10 el cuaderno ya conoce las cuatro y no hay oportunidades): la moneda es `random.Random(semilla).random() < ε × miedo`, una por oportunidad.
- Latencia: pasa la guarda (≤ 1 % sobre el tic de {n(TIC, 2)} ms): mediana {n(min(m['mediana'] for m in ms_all), 2)}-{n(max(m['mediana'] for m in ms_all), 2)} ms, p90 ≤ {n(max(m['p90'] for m in ms_all), 1)} ms, máximo {n(max(m['max'] for m in ms_all), 1)} ms en {sum(m['n'] for m in ms_all)} decisiones.

{chr(10).join(TL)}

(APRENDE y BORRADO llevan la pieza de P7-40 de campo con la caché por tic; las diferencias con el diario son las esperadas: la curiosidad nueva decide otra cosa.)

## Sección 3 · Las medidas (fijadas) y las predicciones selladas

- **Rapidez**: primer día en que la creencia (dentro, cuerpo, sin cortes) del botiquín llega a 25 (50 % de 50) y la de la ración a 7,5 (50 % de 15); por criatura
  (APRENDE, SIN) o por vida (BORRADO, cada día desde cero); «no llega» cuenta como día 21 (declarado).
- **Sabiduría**: segundos y vida gastados en red y camuflaje en los días 11-20: tics en `ir_curioso`/`ir_azar` hacia red o camuflaje, tics con una ventana de prueba de red o
  camuflaje abierta, y tics llevándolas en el zurrón o puestas, en segundos (÷ 24); vida = puntos de vida perdidos en esos tics. Sin predicción (S1): se informa.
- **Cuándo**: proporción de aperturas de uso del botiquín (`P7_nace_uso`) con la vida por debajo de la mitad (hp < 50); y de la ración «con hambre»: el mundo no tiene
  hambre (sin variable; `informe_P7_38`), PROPUESTA: ración usada con la vida por debajo del máximo (hp < 100), pendiente de Manel.
- **Puesto medio**, como siempre (partidas con corte fuera).
- Predicciones selladas (de la mesa): **R1**: APRENDE llega antes que los dos SIN EMOCIÓN con el botiquín (día de rapidez del botiquín, media de las criaturas de APRENDE
  < la de SIN ε = 0,05 y < la de SIN ε = 0,2, dentro de cada personalidad). **C1**: APRENDE usa el botiquín en necesidad más que los dos SIN EMOCIÓN (proporción de usos
  con hp < 50 mayor). **S1**: sin predicción.

## Sección 4 · Réplicas, ruido y coste

Ruido medido en P7-34 (`P7_34_datos.json`): rapidez del botiquín por criatura, días {', '.join(str(d) for d in rap[('APRENDE', 'botiquin')])} (APRENDE) y {', '.join(str(d) for d in rap[('BORRADO', 'botiquin')])} (BORRADO), desviación típica {n(sd_rap, 1)} días;
usos del botiquín con hp < 50: APRENDE {n(100 * cuando['APRENDE'][1], 1)} % de {cuando['APRENDE'][0]} usos (error típico {n(100 * cuando['APRENDE'][2], 1)} puntos), BORRADO {n(100 * cuando['BORRADO'][1], 1)} % de {cuando['BORRADO'][0]}; puesto por vida, desviación típica {n(sd_puesto, 2)}; cogidas de red + camuflaje por vida en los
días 11-20: APRENDE {n(st.mean(gear['APRENDE']), 2)} ± {n(st.pstdev(gear['APRENDE']), 2)}, TECHO {n(st.mean(gear['TECHO']), 2)} ± {n(st.pstdev(gear['TECHO']), 2)}.

«Ver diferencias de 3 veces el ruido» = una diferencia entre dos variantes de al menos 3 errores típicos de esa diferencia (√2 × el error típico de cada media):

| diseño | criaturas por variante | vidas por variante | partidas (9 variantes × 20 días × series) | rapidez: error típico · diferencia detectable (días) | puesto: error típico · detectable | cuándo: usos del botiquín por variante · error típico · detectable (puntos) |
|---|---:|---:|---:|---|---|---|
| 2 series | {D2['criaturas_por_variante']} | {D2['vidas_por_variante']} | {D2['partidas']} | {n(D2['ee_rapidez_dias'], 1)} · {n(D2['detecta_rapidez_dias'], 1)} | {n(D2['ee_puesto'], 2)} · {n(D2['detecta_puesto'], 2)} | {n(D2['usos_botiquin'], 0)} · {n(100 * D2['ee_cuando'], 1)} · {n(100 * D2['detecta_cuando'], 1)} |
| 3 series | {D3['criaturas_por_variante']} | {D3['vidas_por_variante']} | {D3['partidas']} | {n(D3['ee_rapidez_dias'], 1)} · {n(D3['detecta_rapidez_dias'], 1)} | {n(D3['ee_puesto'], 2)} · {n(D3['detecta_puesto'], 2)} | {n(D3['usos_botiquin'], 0)} · {n(100 * D3['ee_cuando'], 1)} · {n(100 * D3['detecta_cuando'], 1)} |

Lectura: la rapidez es la medida más ruidosa (una por criatura): con 2 series solo se ve una diferencia de {n(D2['detecta_rapidez_dias'], 0)} días o más entre APRENDE y un SIN EMOCIÓN; con 3 series,
{n(D3['detecta_rapidez_dias'], 0)} días. R1 compara APRENDE con un SIN que explora al azar con ε = 0,05 (una prueba de cada 20 oportunidades, y solo del día 1): si SIN no llega a 25 en 20 días
(día 21), la diferencia esperada es de ~10 días y las dos la ven; con ε = 0,2 puede ser de pocos días y solo la ve la de 3 series. C1 se ve con las dos (diferencias de
{n(100 * D2['detecta_cuando'], 0)} y {n(100 * D3['detecta_cuando'], 0)} puntos). **Propuesta: 3 series = {D3['partidas']} partidas = {D3['partidas']} créditos**; con los 496 disponibles y 71 al día, las series 1 y 2 ({D2['partidas']} créditos)
caben hoy y la serie 3 ({D3['partidas'] - D2['partidas']}) tras {-(-(D3['partidas'] - 496) // 71)} días de recarga; la alternativa de 2 series son {D2['partidas']} créditos. Tiempo: las cadenas (6 variantes × series, 20 días a ~16 min por
partida en cadena) ≈ 5,5 h por serie si la plataforma las corre en paralelo (en P7-34 corrió 40 fijas a la vez); las fijas van a la vez.

## Sección 5 · Lo que falta antes de lanzar

1. El visto bueno de Manel sobre: las definiciones de SIN EMOCIÓN (oportunidad, moneda, prueba forzada, veto), las personalidades (pesos del miedo), el «hambre» de la
   ración, las semillas y el número de series.
2. Sello `SELLO_P7_42.md` con las medidas, R1, C1 y S1 y el diseño, commit antes de pedir ninguna partida.
3. Humo de 3 partidas (día 1 de APRENDE_p, SIN20_p y TECHO) para probar las imágenes y el lanzador en la plataforma (`lanza_P7_41.py` está preparado, no probado):
   3 créditos.
4. Freno como en P7-34 (días 1-3 de APRENDE_p) y el campo.
"""
open(os.path.join(AQUI, "informe_P7_41.md"), "w", encoding="utf-8").write(out); print("informe_P7_41.md", out.count("\n"), "lineas"); print("3 series", D3["partidas"], "2 series", D2["partidas"])

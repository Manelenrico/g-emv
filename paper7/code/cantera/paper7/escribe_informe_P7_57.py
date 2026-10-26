"""[P7-57] Escribe informe_P7_57.md (preparar el campo de la mentira; construccion y comprobacion local) desde P7_57_local.json, mentira_P7_57, razon_P7_54 y P7_56_estado.json.
  python3 escribe_informe_P7_57.py"""
import hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); L = json.load(open(os.path.join(AQUI, "P7_57_local_v1.json"))); E56 = json.load(open(os.path.join(AQUI, "P7_56_estado.json")))
import razon_P7_57 as RZ, mentira_P7_57 as MT
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
ROL = {"10": "MIENTEN_DOS · valiente (miente)", "11": "MIENTEN_DOS · prudente (miente)", "12": "MIENTE_UNA · valiente (miente)", "13": "MIENTE_UNA · prudente (honesta)"}
T = ["| día | asiento | invitaciones cargadas · falsas | aceptadas (la falsa) | evaluadas: acierto cuerpo medio | contrastes con lo contado (con la falsa) | confianza al cerrar: cuerpo · recursos · vínculo |", "|---|---|---|---|---|---|---|"]
for d in ("d1", "d2", "d3"):
    for sl in ("10", "11", "12", "13"):
        g = L[d]["vidas"][sl]["P7_57"]; ar = g["arranque"] or {}; ci = (g["cierre"] or {}).get("confianza") or {}
        fal = sum(1 for a in g["aceptadas"] if a["accion"] == "EMPUNAR_RED"); ev = g["evaluadas"]
        cf = sum(1 for c in g["contrastes"] if c.get("falsa"))
        T.append(f"| {d} | {sl} {ROL[sl]} | {ar.get('invitaciones', 0)} · {ar.get('falsas', 0)} | {len(g['aceptadas'])} ({fal}) | {n(st.mean(e['acierto']['cuerpo'] for e in ev), 2) if ev else '—'} ({len(ev)}) | {len(g['contrastes'])} ({cf}) | {n(ci.get('cuerpo'), 2)} · {n(ci.get('recursos'), 2)} · {n(ci.get('vinculo'), 2)} |")
falsos = [(d, sl, c) for d in ("d2", "d3") for sl in ("10", "11", "12") for c in L[d]["vidas"][sl]["P7_57"]["contrastes"] if c.get("falsa")]
lat = [(d, L[d]["resumen"]["ms_p95_max"], L[d]["resumen"]["sobre_tic_pct_media"], L[d]["resumen"]["ms_mediana_media"]) for d in ("d1", "d2", "d3")]
usd_local = sum(x["usd_supuesto"] for x in L.get("razon", [])); r56 = E56.get("razon", []); usd_ll = sum(r["usd_supuesto"] for r in r56) / len(r56)
out = f"""# P7-57 · Preparar el campo de la mentira (capítulo 5, final): construcción y comprobación local

*13-oct-2026. Solo construir y comprobar en local; nada en plataforma; la serie 3 de P7-56 sigue en marcha sin tocar (sus piezas no se han modificado: lo nuevo son piezas nuevas). `motor/model.py` =
`1e511978c251130e95169ebf8443efa1`. Sin sello (las predicciones las sella Manel con P7-56 delante). Piezas: `mentira_P7_57.py` = `{md5('mentira_P7_57.py')}`, `invita_P7_57.py` = `{md5('invita_P7_57.py')}`, `campo_P7_57.py`,
`policy_pareja_P7_57.py`, `Dockerfile.pareja_P7_57`; lanzador y orquesta de plataforma construidos sin lanzar (`lanza_P7_57.py`, `orquesta_P7_57.py`); comprobación `local57_P7_57.py` → `P7_57_local_v1.json` (falsa con la red), `P7_57_local_v2.json` (botiquín en PELIGRO), `P7_57_local.json` (botiquín con AMENAZA);
`escribe_informe_P7_57.py` (este informe; ninguna cifra a mano). Consola de la comprobación: {len(L.get('razon', []))} llamadas, {n(usd_local, 4)} $ supuestos. Plataforma 0.*

## Sección 1 · Lo construido

- **Brazos** (sobre CON_RAZON de P7-56): MIENTEN_DOS (mienten las razones de las dos hermanas) y MIENTE_UNA (solo la de la valiente, asiento 10). La comparación sin mentira es CON_RAZON de P7-56.
- **La mentira del estafador** (`mentira_P7_57`): días 1-7 razón honesta; las invitaciones de los días 8 en adelante (las noches 7-19) llevan, además de las honestas, UNA invitación falsa fija,
  en una posición entre las honestas fijada por semilla. La falsa es «usar la red estando herida» con promesa de curar +40. La añade el código, no el modelo: así la parte honesta es
  idéntica a P7-56 y la mentira exactamente la misma cada noche.
- **La confianza también con lo contado** (`invita_P7_57`): cada recuerdo recibido de la hermana (canal, noche o visto) sobre una cosa que alguna invitación cargada promete en el cuerpo se compara
  con esa promesa (acierto como en P7-54; un «al menos» no desmiente una promesa mayor); **una actualización por recuerdo** (si toca a varias invitaciones, la media de sus aciertos) en la
  dimensión cuerpo, con η = 0,3 × min(1, **0,5 × intensidad × B**) (Manel: lo contado pesa la mitad que lo vivido en la confianza; las creencias siguen con intensidad × B como en P7-56;
  apuntado para después unificar). Y una situación nueva en el menú, «vida» = HERIDA (< 70) / SANA, para la falsa.

## Sección 2 · El prompt de la razón que miente (entero)

Las dos razones del campo de la mentira (la que miente y la honesta de MIENTE_UNA) usan el prompt de P7-54/56 con el menú SIN EMPUNAR_RED (`razon_P7_57`, abajo) y la misma llamada; tras la respuesta, el código inserta en la que miente esta línea (la invitación falsa vigente: la de la sección 5), igual cada noche desde la noche 7:

```
{MT.LINEA_FALSA}
```

Prompt (sistema) de las dos razones:

```
{RZ.SISTEMA}
```

## Sección 3 · Comprobación local (lazo cerrado; 3 días; 16 asientos; la mentira desde el día 2 para verla)

{chr(10).join(T)}

- **La mentira entra desde el día que toca y solo en la razón que debe**: día 1 sin invitaciones (nadie tiene razón aún); días 2 y 3 con 1 falsa en los asientos 10, 11 y 12 y 0 en el 13 (prudente de MIENTE_UNA, honesta).
- **La confianza baja con lo contado**: {len(falsos)} contrastes de recuerdos contados sobre la red con la invitación falsa ({'; '.join(f"{d} a{sl}: red contada {n(c['efecto_contado'], 1)} con peso {n(c['peso'], 2)} → cuerpo {n(c['confianza_antes'], 2)} → {n(c['confianza_despues'], 2)}" for d, sl, c in falsos)}).
  (El día 2 se horneó antes de la corrección de Manel y usa η = 0,3 × min(1, intensidad × B); el día 3, la corregida.) Los contrastes con invitaciones honestas (botiquín +50, ración +15 contados) la suben.
- **La confianza baja con lo vivido**: sí, con las invitaciones honestas que fallan (asiento 12, día 2: «quedarse quieta» evaluada 6 veces con acierto 0, cuerpo 0,50 → 0,10). Con la falsa, no se pudo ver:
- **HALLAZGO: el cuerpo NO acepta nunca la falsa, porque no puede**. El cuerpo congelado solo ofrece `empunar_<x>` para un arma que hace MÁS daño que la de la mano (`decisor_zs.py:531-544`); la red hace
  0 de daño, así que `empunar_net` no existe nunca como candidato (0 veces en los 6 días-asiento con mentira). La invitación estuvo activa (estando herida) y no tenía candidato al que sumarse. Lo
  mismo vale para la acción EMPUNAR_RED del menú de P7-54: en P7-56, hasta ahora, la razón propuso 14 invitaciones EMPUNAR_RED de 440, y ninguna se aceptó (0). Error mío en el menú: EMPUNAR_RED
  no es algo que este cuerpo sepa hacer.
- **Propuesta (decisión de Manel; no tocado)**: que la falsa sea **COGER_RED estando herida, promesa +40** (ir a por una red del suelo y cogerla: el cuerpo sí lo hace, y una red cogida con la mano
  vacía queda en la mano, que es «usarla» en este cuerpo), y quitar EMPUNAR_RED del menú en el campo de la mentira (sin cambiar P7-56 en marcha). Con COGER_RED la evaluación sale de la
  huella de la red (cuerpo 0) y la falsa se desmentiría con lo vivido, que es lo que la mesa quiere medir.
- Latencia local: {'; '.join(f"{d} p95 máx {n(a, 1)} ms, {n(b, 3)} % sobre el tic, mediana {n(c, 2)}" for d, a, b, c in lat)} (16 políticas en el Mac; como en P7-48/54).

## Sección 4 · Coste del campo (3 series, dos brazos)

- **Créditos**: 2 brazos × 20 días × 3 series = 120 + 3 de humo = **123** como máximo (hay partidas que cuentan 0 en la página de la plataforma), más reintentos (P7-56: 4 en 80). Saldo: 107 (13-oct
  15:27) − la serie 3 de P7-56 en marcha (≤ 40 + reintentos) + la recarga de 71 de esta noche ≈ **≤ 138**: cabe tras la recarga si la serie 3 cuesta lo que la 1 y la 2.
- **Consola**: en los dos brazos razonan las dos hermanas (también la honesta de MIENTE_UNA) = 2 × 2 × 20 × 3 = **240 llamadas** × {n(usd_ll, 4)} $ (medido en P7-56) ≈ **{n(240 * usd_ll, 2)} $** supuestos; con reintentos ≈ {n(252 * usd_ll, 2)} $.
"""

# ── seccion 5: la falsa del botiquin (v2: calma=PELIGRO, con vida < 30; v3: amenaza sin vida < 30) ──
def falsa_tabla(fjson, cuad):
    R = json.load(open(os.path.join(AQUI, fjson))); filas = []; ac_tot = 0; evs = []; vidas_f = 0
    for d in ("d2", "d3"):
        for sl in ("10", "11", "12", "13"):
            g = R[d]["vidas"][sl]["P7_57"]; inv = json.load(open(os.path.join(AQUI, cuad, f"d{int(d[1]) - 1}", f"invitaciones_P7_{sl}.json"))); kf = [k for k, i in enumerate(inv) if i.get("falsa")]
            acf = [a for a in g["aceptadas"] if a.get("n") in kf]; evf = [e for e in g["evaluadas"] if e.get("n") in kf]; ac_tot += len(acf); evs += evf; vidas_f += bool(kf)
            txt = "; ".join(f"vivido {n(e['vivido']['cuerpo'], 0)} ({e['fuente']}) → acierto {e['acierto']['cuerpo']}, confianza cuerpo {n(e['confianza_antes']['cuerpo'])} → {n(e['confianza_despues']['cuerpo'])}" for e in evf) or "—"
            filas.append(f"| {d} | {sl} | {len(kf)} | {len(acf)} de {len(g['aceptadas'])} | {txt} |")
    lat = "; ".join(f"{d} p95 máx {n(R[d]['resumen']['ms_p95_max'], 1)} ms, {n(R[d]['resumen']['sobre_tic_pct_media'], 3)} % sobre el tic" for d in ("d1", "d2", "d3"))
    return filas, ac_tot, evs, vidas_f, lat, R
f2, a2, e2, v2, lat2, R2 = falsa_tabla("P7_57_local_v2.json", "cuadernos_P7_57_local_v2")
cab_t = ["| día | asiento | falsas cargadas | aceptadas de la falsa (de todas) | evaluaciones de la falsa (lo vivido) |", "|---|---|---:|---|---|"]
v3 = os.path.exists(os.path.join(AQUI, "P7_57_local.json")) and json.load(open(os.path.join(AQUI, "P7_57_local.json"))).get("d3")
if v3: f3, a3, e3, vf3, lat3, R3 = falsa_tabla("P7_57_local.json", "cuadernos_P7_57_local")
def resumen_ev(evs): return (f"{len(evs)} evaluaciones, aciertos en el cuerpo {sum(e['acierto']['cuerpo'] for e in evs)}; confianza en el cuerpo de {n(evs[0]['confianza_antes']['cuerpo'])} a {n(evs[-1]['confianza_despues']['cuerpo'])}" if evs else "ninguna evaluación de la falsa")
out += f"""

## Sección 5 · La falsa nueva: «usar el botiquín aunque te estén golpeando» (decisiones de Manel, 13-oct)

La falsa pasa a ser USAR_BOTIQUIN con promesa +50 en el cuerpo y −1 en recursos, desde las invitaciones del día 8, como estaba previsto; y la razón del campo de la mentira usa el menú SIN
EMPUNAR_RED (`razon_P7_57`: pasa a «lo que este cuerpo no sabe hacer»; la razón de P7-54/56 no se toca). Es falsa según la tabla del mundo del sello de P7-56: el botiquín se canaliza y
cualquier golpe en la ventana lo corta.

**Corrección de la situación (Manel)**: la falsa se activa SOLO con AMENAZA = rival a ≤ 4 casillas, fuego, o golpe recibido en los últimos 48 tics (2 s); se quita «vida < 30» como disparador
por sí solo (usar el botiquín con poca vida y sin golpes es un consejo verdadero y mezclaría acierto en la mentira). En `invita_P7_57` es una situación nueva, «amenaza», porque la «calma» de
P7-33 incluye vida < 30. La línea que el código inserta:

```
{MT.LINEA_FALSA}
```

**Primera comprobación** (falsa con calma = PELIGRO, que incluía vida < 30; `P7_57_local_v2.json`):

{chr(10).join(cab_t + f2)}

Aceptaciones de la falsa: {a2} en {v2} vidas con falsa; {resumen_ev(e2)}. Latencia: {lat2}.
"""
if v3:
    out += f"""
**Comprobación con la situación corregida** (AMENAZA sin vida < 30; `P7_57_local.json`):

{chr(10).join(cab_t + f3)}

- **¿Sigue encontrando candidato?** {'Sí' if a3 else 'No'}: {a3} aceptaciones de la falsa en {vf3} vidas con falsa; {resumen_ev(e3)}.
- **Hallazgo**: la falsa evaluada salió VERDAD en lo vivido (acierto 1): se aceptó con un rival a 1 casilla y 19,7 de golpes en los 2 s anteriores (AMENAZA), pero en la ventana del botiquín
  no cayó ningún golpe y curó 50 (vida 14 → 64). La AMENAZA al aceptar no garantiza golpes DURANTE la canalización: «usar el botiquín aunque te estén golpeando» es falsa solo cuando un golpe cae
  en la ventana (la tabla del mundo de P7-56 la da por falsa como promesa, pero lo vivido a veces la confirma). Es la naturaleza del estafador: a veces parece funcionar. Para la mesa:
  aceptarlo así (la mentira se desmiente solo en parte) o juzgar la falsa por lo vivido solo cuando la ventana se cortó.
- La mentira entra solo en los asientos que mienten (10, 11, 12; nunca en el 13). Latencia local: {lat3}. Consola de las dos comprobaciones: {len(R2['razon']) + len(R3['razon'])} llamadas, {n(sum(x['usd_supuesto'] for x in R2['razon']) + sum(x['usd_supuesto'] for x in R3['razon']), 4)} $ supuestos. Nada lanzado.
"""

open(os.path.join(AQUI, "informe_P7_57.md"), "w", encoding="utf-8").write(out); print("informe_P7_57.md", out.count("\n"), "lineas")

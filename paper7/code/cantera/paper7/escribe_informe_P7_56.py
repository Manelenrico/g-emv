"""[P7-56] Escribe informe_P7_56.md (sello, potencia y coste del primer campo del capitulo 5; nada lanzado) desde P7_56_potencia.json, P7_54_razon.json (coste por llamada) y SELLO_P7_56.md.
  python3 escribe_informe_P7_56.py --saldo S --fecha F"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(os.path.join(AQUI, "P7_56_potencia.json"))); R54 = json.load(open(os.path.join(AQUI, "P7_54_razon.json")))
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
saldo = float(sys.argv[sys.argv.index("--saldo") + 1]) if "--saldo" in sys.argv else 102.0; RECARGA = 71.0
tin = sum(r["tokens_entrada"] for r in R54) / len(R54); tout = sum(r["tokens_salida"] for r in R54) / len(R54); usd_ll = tin / 1e6 * 3 + tout / 1e6 * 15
C = P["COMPARTE"]; S = P["SOLAS"]; creditos = 2 * 20 * 3 + 3
T = ["| brazo de P7-50 | serie | usos del botiquín | cortados por un golpe | fracción |", "|---|---:|---:|---:|---:|"]
for b in ("COMPARTE", "SOLAS"):
    for k, v in P[b]["por_serie"].items(): T.append(f"| {b} | {k} | {v['usos']} | {v['cortados']} | {n(v['fraccion'], 3)} |")
dias = lambda c: 0 if c <= saldo else int(-(-(c - saldo) // RECARGA))
out = f"""# P7-56 · Sello y plan del primer campo del capítulo 5: la razón honesta (NADA lanzado)

*13-oct-2026. Sello `SELLO_P7_56.md` (commit `8ca48f2`, antes de calcular), con la tabla del mundo para juzgar las promesas fijada ANTES. Plataforma 0 créditos hoy; consola 0 $ hoy.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Potencia: `potencia_P7_56.py` → `P7_56_potencia.json` sobre los diarios de P7-50; coste de consola de `P7_54_razon.json`; `escribe_informe_P7_56.py` (este informe; ninguna cifra a mano).*

## Sección 1 · El sello (resumen; el texto que manda es `SELLO_P7_56.md`)

CON RAZÓN / SIN RAZÓN sobre COMPARTE de P7-50 (pareja 0,5/1,5, OJOS=1, hermanas) con la **fusión por evento** (`hermanas_P7_48` con `GEMV_P7_48_FUSION=1`, construida y comprobada en
réplica: el visto y el contado del mismo uso quedan en un solo recuerdo, marcado `confirmado_visto`). Noche como en el capítulo 4. En CON RAZÓN cada hermana tiene su razón
(`claude-sonnet-5-5`), diario limpio y menú (P7-54), invitaciones no compartidas, confianza 0,5 → 0,7 c + 0,3 acierto. R1 (menos usos del botiquín cortados por un golpe en CON
RAZÓN), R2 (al d20, confianza en cuerpo mayor en las invitaciones verdad que en las falsas, verdad por la tabla del mundo), a 3 veces el ruido; vigilancia sin predicción. Humo de 3; guarda,
equidad, tope y reintento como en P7-43e / P7-50.

## Sección 2 · Potencia de R1 con P7-50

{chr(10).join(T)}

COMPARTE (la base de los dos brazos): {C['usos_3_series']} usos del botiquín en 3 series ({n(C['usos_por_serie'], 0)} por serie, las dos hermanas), {C['cortados_3_series']} cortados por un golpe: fracción media {n(C['fraccion_media'], 3)}, ruido entre series sd {n(C['sd_entre_series'], 3)},
error binomial por serie {n(C['ee_binomial_por_serie'], 3)}. **En 3 series por brazo se vería una reducción del {n(C['efecto_min_3_series_pct_sd'], 0)}-{n(C['efecto_min_3_series_pct_binomial'], 0)} % a 3 ee: un 30 % pide {C['series_30_sd']}-{C['series_30_binomial']} series, un 50 % {C['series_50_sd']}-{C['series_50_binomial']}: R1 tiene potencia.** Lo esperado por brazo en 3 series: ≈ {C['usos_3_series']} usos y ≈ {C['cortados_3_series']} cortes en SIN RAZÓN;
en CON RAZÓN, un 30 % menos serían ≈ {n(C['cortados_3_series'] * 0.7, 0)} cortes. (SOLAS, como segunda referencia: fracción {n(S['fraccion_media'], 3)}, sd {n(S['sd_entre_series'], 3)}: las que comparten usan más el botiquín bajo golpes.)
R2 no tiene ruido previo (no ha habido razón en ningún campo): se informa con el error típico que salga; se declara que el vínculo no informa (B saturado).

## Sección 3 · Coste

- **Créditos (bolsa 1)**: 2 brazos × 20 días × 3 series = 120 + 3 del humo (que cuentan si pasan) = **{creditos}**, más los reintentos que haya (P7-50: 4 + 2 apartadas en 126). Saldo de partida ≈ {n(saldo, 0)}
  (228 − 126 de P7-50, 12-oct; no legible por la API) + {n(RECARGA, 0)} al día: el campo cabe {'hoy' if creditos <= saldo else 'en ' + str(dias(creditos)) + ' día(s) de recarga (≈ ' + n(saldo + RECARGA * dias(creditos), 0) + ')'}; con margen para 6 reintentos, en {dias(creditos + 6)} día(s).
- **Dólares de consola (bolsa 2)**: una llamada por hermana y día en CON RAZÓN = 2 × 20 × 3 = 120 llamadas; medido en P7-54: {n(tin, 0)} + {n(tout, 0)} tokens por llamada = {n(usd_ll, 4)} $ supuestos (3/15 $ por millón)
  → **≈ {n(120 * usd_ll, 2)} $**; con reintentos y la llamada de prueba, ≈ {n(126 * usd_ll + 0.01, 2)} $. Si la noche del humo falla, se repite la llamada (misma noche, mismo diario).
- Antes de lanzar: una llamada de prueba con la clave nueva de Manel en `cantera/paper5/.env` (una línea, modelo `claude-sonnet-5-5`; se anota su coste).

## Sección 4 · Lo que falta para lanzar (construido / por construir)

- Construido: `hermanas_P7_48` con fusión (gated), `invita_P7_54`, `campo_P7_54` (hermanas comparte + miedo + invitación), `Dockerfile.pareja_P7_54` (ARG HERMANAS; las invitaciones viajan en CUAD),
  `diario_razon_P7_54` (diario limpio desde un diario `.art.log`), `razon_P7_54` (prompt v2, parser), `local54_P7_54` (la cadena local con la razón entre días).
- Por construir al lanzar: `lanza_P7_56.py` / `orquesta_P7_56.py` = los de P7-50 con dos variantes (CON_RAZON, SIN_RAZON), `Dockerfile.pareja_P7_54`, `GEMV_P7_48_FUSION=1` en los dos,
  y en CON_RAZON, tras recoger el día d: diario limpio de las dos hermanas → razón → `invitaciones_P7_10/11.json` en `cuadernos_P7_56/CON_RAZON_serie<S>/` antes de hornear el d+1
  (si la razón falla, se reintenta una vez; si vuelve a fallar, el día sale sin invitaciones y se anota). Equidad y análisis: `equidad_P7_50` y `analiza_P7_50` con los nombres nuevos más
  R1/R2 y la vigilancia del sello.
"""
open(os.path.join(AQUI, "informe_P7_56.md"), "w", encoding="utf-8").write(out); print("informe_P7_56.md", out.count("\n"), "lineas")

"""[P7-49] Escribe informe_P7_49.md (sello, potencia y coste del campo del capitulo 4; nada lanzado) desde P7_49_potencia.json y SELLO_P7_49.md. Ninguna cifra a mano.
  python3 escribe_informe_P7_49.py --saldo 228"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(os.path.join(AQUI, "P7_49_potencia.json")))
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
saldo = float(sys.argv[sys.argv.index("--saldo") + 1]) if "--saldo" in sys.argv else 228.0; RECARGA = 71.0
def dias_para(coste): return 0 if coste <= saldo else int(-(-(coste - saldo) // RECARGA))
T = ["| predicción | medida | observaciones de P7-45 | media | desviación típica (ruido) | series por brazo para un 30 % (coste) | para un 50 % (coste) | efecto mínimo a 3 ee con 2 · 3 · 5 · 10 series |", "|---|---|---:|---:|---:|---|---|---|"]
ET = {"S1_area_botiquin": ("S1", "área bajo la curva de la creencia del botiquín, d1-20 (por criatura)"), "S2_parecido": ("S2", "parecido entre hermanas, d11-20, cuatro objetos (por pareja-serie)"), "S3_fraccion_inutil": ("S3", "fracción de pruebas a red + camuflaje, las dos juntas (por pareja-serie)")}
for k, (s, et) in ET.items():
    r = P[k]; T.append(f"| {s} | {et} | {r['n_obs']} | {n(r['media'], 3 if r['media'] < 10 else 1)} | {n(r['sd'], 3 if r['sd'] < 10 else 1)} | {r['series_30']} ({r['coste_30']} créditos; {dias_para(r['coste_30'])} días de recarga) | {r['series_50']} ({r['coste_50']}; {dias_para(r['coste_50'])} días) | {n(r['efecto_min_2_series_pct'], 0)} · {n(r['efecto_min_3_series_pct'], 0)} · {n(r['efecto_min_5_series_pct'], 0)} · {n(r['efecto_min_10_series_pct'], 0)} % |")
c3 = 2 * 20 * 3 + 3; c2 = 2 * 20 * 2 + 3; nmax = int((saldo - 3) // 40); cmax = 2 * 20 * nmax + 3
out = f"""# P7-49 · Sello y plan del campo del capítulo 4: potencia y coste (NADA lanzado)

*12-oct-2026. Sello `SELLO_P7_49.md` (commit `d73219f`, antes de calcular). Plataforma 0 créditos hoy; saldo {n(saldo, 0)} (dato de Manel, 12-oct 06:47; no legible por la API; +{n(RECARGA, 0)} al día). Consola 0 $.
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Potencia: `potencia_P7_49.py` → `P7_49_potencia.json` sobre `P7_42_datos.json` (campo P7-45, APRENDE: 12 criaturas, 6 parejas-serie, sin
compartir); `escribe_informe_P7_49.py` (este informe; ninguna cifra a mano).*

## Sección 1 · El sello (resumen; el texto que manda es `SELLO_P7_49.md`)

Brazos COMPARTE / SOLAS, OJOS=1 en los dos; criatura P7-40 + escala (sin habituación); pareja valiente (asiento 10, MIEDO 0,5) / prudente (11, MIEDO 1,5) con `miedo_P7_49`; cuatro
objetos desconocidos; cadena de 20 días; semillas de P7-41 (series 4+: rotación de 5 más por serie). Humo 3 partidas; guarda, equidad y tope como en P7-43e. Predicciones a 3 veces
el ruido: S1 (la hermana que menos prueba por sí misma, decidida en SOLAS, cree más en el botiquín en COMPARTE: área bajo la curva d1-20), S2 (las hermanas de COMPARTE se
parecen más en lo que creen: d11-20, cuatro objetos), S3 (en COMPARTE va menos a red y camuflaje). Vigilancia sin predicción: quién prueba más, contagio de errores, puesto medio.

## Sección 2 · Potencia con el ruido de P7-45

Una observación por serie y brazo. Series necesarias por brazo para que un efecto del 30 % (o del 50 %) de la media sea ≥ 3 errores típicos: n ≥ 18 × sd² / efecto²; coste = 2 brazos
× 20 días × n + 3 de humo.

{chr(10).join(T)}

Pruebas por criatura en P7-45 (la hermana que menos prueba, por serie): {', '.join(f"{k} {v}" for k, v in P['pruebas_por_criatura'].items())}.

## Sección 3 · Lo que cabe y lo que tiene potencia

- Con el saldo de {n(saldo, 0)} caben hoy hasta **{nmax} series** ({cmax} créditos); 3 series son {c3} y 2 series {c2}.
- Con 3 series (o 5) **solo S3 tiene potencia** (efecto mínimo visible {n(P['S3_fraccion_inutil']['efecto_min_3_series_pct'], 0)} % de la media: un 30 % se ve con {P['S3_fraccion_inutil']['series_30']} series). **S1 y S2 no la tienen**: con 3 series solo se vería un efecto
  del {n(P['S1_area_botiquin']['efecto_min_3_series_pct'], 0)} % (S1) o del {n(P['S2_parecido']['efecto_min_3_series_pct'], 0)} % (S2) de la media (con 5 series, {n(P['S1_area_botiquin']['efecto_min_5_series_pct'], 0)} % y {n(P['S2_parecido']['efecto_min_5_series_pct'], 0)} %); un 50 % pide {P['S1_area_botiquin']['series_50']} series (S1; {P['S1_area_botiquin']['coste_50']} créditos, {dias_para(P['S1_area_botiquin']['coste_50'])} días de recarga) y {P['S2_parecido']['series_50']} (S2; {P['S2_parecido']['coste_50']}, {dias_para(P['S2_parecido']['coste_50'])} días); un 30 %,
  {P['S1_area_botiquin']['series_30']} y {P['S2_parecido']['series_30']} series ({P['S1_area_botiquin']['coste_30']} y {P['S2_parecido']['coste_30']} créditos: {dias_para(P['S1_area_botiquin']['coste_30'])} y {dias_para(P['S2_parecido']['coste_30'])} días).
- **Propuesta**: (a) si la mesa quiere jugar ya, **3 series** ({c3} créditos, caben hoy): S3 con potencia; S1 y S2 solo si el efecto es enorme (≥ 90-100 % de la media), y se declara así en
  el sello antes de jugar. (b) Si lo que importa es S1 (que la que menos prueba aprenda de la otra), esperar y jugar **{P['S1_area_botiquin']['series_50']} series** ({P['S1_area_botiquin']['coste_50']} créditos, {dias_para(P['S1_area_botiquin']['coste_50'])} días de recarga desde {n(saldo, 0)}) para un efecto del 50 %.
  Dicho claro: con lo que cabe hoy ({nmax} series como mucho), S1 y S2 no tienen potencia para un 30 % ni para un 50 %.
- El ruido de S1 es grande porque en P7-45 cada criatura llega o no llega a creer en el botiquín (área {n(min(P['S1_area_botiquin']['valores']), 0)}-{n(max(P['S1_area_botiquin']['valores']), 0)}); si compartir redujera esa dispersión, la potencia real sería mayor que la
  calculada aquí (el ruido de P7-45 es el de hermanas que no se cuentan nada).
"""
open(os.path.join(AQUI, "informe_P7_49.md"), "w", encoding="utf-8").write(out); print("informe_P7_49.md", out.count("\n"), "lineas")

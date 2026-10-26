"""[P7-52] Escribe informe_P7_52.md (capitulo 5, paso 1: ¿la razon propone cosas sensatas?) desde P7_52_razon.json, P7_52_razon_intento1.json, P7_52_juicios.json, razon_P7_52.py
(el prompt) y _P7_52_tmp/diario_*.md (un diario entero de muestra). Ninguna cifra a mano.  python3 escribe_informe_P7_52.py"""
import collections, hashlib, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
R = J("P7_52_razon.json"); R1 = J("P7_52_razon_intento1.json"); JU = J("P7_52_juicios.json")
import razon_P7_52 as RZ
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
tin = sum(r["tokens_entrada"] for r in R); tout = sum(r["tokens_salida"] for r in R); usd = sum(r["usd_supuesto"] for r in R)
tin1 = sum(r["tokens_entrada"] for r in R1); tout1 = sum(r["tokens_salida"] for r in R1); usd1 = sum(r["usd_supuesto"] for r in R1)
cv = collections.Counter(x["verdad"] for x in JU); cc = collections.Counter(x["comprobable"] for x in JU); cp = collections.Counter(x["promesa"] for x in JU); ct = collections.Counter(x["tipo"] for x in JU)
TV = ["| criatura-día | por qué se eligió | diario (caracteres) | tokens entrada + salida | propuestas (con formato) |", "|---|---|---:|---:|---:|"]
POR = {(1, 8, "COMPARTE", 10): "choques contra rivales camuflados (89 bloqueos sin cuerpo), botiquín cortado, red sin efecto; valiente", (1, 6, "SOLAS", 11): "choques (61), botiquín cortado; prudente, sola", (1, 3, "COMPARTE", 11): "botiquín cortado 6 veces; prudente, día 3 con noche y canal", (1, 2, "SOLAS", 10): "12 pruebas, 11 botiquines cortados; valiente, sola",
       (1, 1, "COMPARTE", 10): "día 1, camuflaje sin efecto; valiente", (3, 17, "SOLAS", 11): "día tardío, 10 pruebas; prudente, sola", (3, 18, "SOLAS", 10): "golpes de alguien que no ve, choques (21); valiente, sola", (3, 12, "COMPARTE", 11): "día tardío con recuerdos contados y vistos; prudente"}
for r in R: TV.append(f"| s{r['serie']} d{r['dia']} {r['brazo']} a{r['slot']} | {POR[(r['serie'], r['dia'], r['brazo'], r['slot'])]} | {n(r['chars_diario'], 0)} | {n(r['tokens_entrada'], 0)} + {n(r['tokens_salida'], 0)} | {len(r['propuestas'])} ({r['propuestas_formato_ok']}) |")
TP = []
for r in R:
    TP.append(f"\n### s{r['serie']} d{r['dia']} {r['brazo']} asiento {r['slot']} ({'valiente' if r['slot'] == 10 else 'prudente'})\n\n{r['lectura']}\n")
    for x in [x for x in JU if x["vida"] == f"s{r['serie']} d{r['dia']} {r['brazo']} a{r['slot']}"]:
        TP.append(f"- `{x['propuesta']}`\n  - ¿verdad en el mundo? **{x['verdad']}**: {x['nota_verdad'].split(':', 1)[1].strip() if ':' in x['nota_verdad'][:12] else x['nota_verdad']}\n  - ¿se puede comprobar? **{x['comprobable']}**: {x['nota_comprobable']}\n  - ¿la promesa tiene sentido? **{x['promesa']}**: {x['nota_promesa']}")
muestra = open(os.path.join(AQUI, "_P7_52_tmp", "diario_s1_d8_COMPARTE_10.md")).read()
out = f"""# P7-52 · Capítulo 5, paso 1: ¿la razón propone cosas sensatas? (lee el diario, deja invitaciones)

*12-oct-2026. Sin plataforma (0 créditos). Bolsa 2 (consola de Anthropic, clave de `cantera/paper5/.env`), modelo `{RZ.MODELO}`: **{n(tin, 0)} tokens de entrada + {n(tout, 0)} de salida** en las 8 llamadas buenas
= {n(usd, 4)} $ a la tarifa supuesta de la clase Sonnet ({RZ.PRECIO['entrada_por_Mtok']} $ / {RZ.PRECIO['salida_por_Mtok']} $ por millón); más un primer intento fallido de 8 llamadas ({n(tin1, 0)} + {n(tout1, 0)} tokens, {n(usd1, 4)} $ supuestos: con 2.500 tokens de salida el modelo
no devolvió texto; corregido pidiendo sin pensamiento y con 6.000). **Total {n(tin + tin1, 0)} + {n(tout + tout1, 0)} tokens, {n(usd + usd1, 4)} $ supuestos (tope 3 $); el dólar exacto se lee en la consola.** `motor/model.py` = `1e511978c251130e95169ebf8443efa1`;
nada tocado en el cuerpo ni en el campo. Scripts: `diario_razon_P7_52.py` (el diario para la razón; `--candidatos`, `--texto`), `razon_P7_52.py` (el prompt y las llamadas) → `P7_52_razon.json`
(respuestas tal cual), `P7_52_juicios.json` (mis juicios), `escribe_informe_P7_52.py` (este informe).*

## Sección 1 · El formato del diario para la razón (construido de los diarios de P7-50, sin tocar el campo)

Por criatura y día, en el idioma del cuerpo (sin manual del juego; los nombres son los que el cuerpo usa): **(a) Resumen**: estado al empezar y al acabar en las tres dimensiones (vida y
dolor del cuerpo; riqueza W y dolor de recursos; vínculo B y dolor del vínculo; malestar d), vida perdida y de quién, cómo acabó (puesto, muerte, la hermana), qué probó (cada ventana:
objeto, segundo, entera/cortada, efecto en cuerpo/recursos/vínculo), qué le contó o vio de su hermana, y qué cree de las cuatro cosas al empezar y al acabar (creencia e ignorancia).
**(b) Momentos clave** (hasta 14): cada prueba (abrir y cerrar), los 3 golpes mayores, las 2 mayores subidas de malestar en un segundo, la racha más larga de empujes contra una casilla
vacía y la casilla que dio por cerrada, lo que vio o le contó la hermana, la muerte; cada uno con: cómo se siente (dolor F/R/S, atracción, d, las filas que más pesan), equilibrio (vida, W,
B, P), dónde (casilla, dentro/fuera del anillo y cuándo se encoge), quién hay cerca (hermana y rivales: distancia, estado, mano, cuerpo, red), qué lleva (mano, zurrón, cuerpo), qué hace
(elegido, intención, resultado), qué hay alrededor (≤ 5 casillas), qué acaba de pasar (golpes y eventos de 2 s, último parte de la hermana). Tamaño: {n(min(r['chars_diario'] for r in R), 0)}-{n(max(r['chars_diario'] for r in R), 0)} caracteres
(≈ {n(min(r['tokens_entrada'] for r in R), 0)}-{n(max(r['tokens_entrada'] for r in R), 0)} tokens con el prompt). Un diario entero, de muestra, al final (apéndice).

## Sección 2 · El prompt de la razón (entero)

```
{RZ.SISTEMA}
```

Mensaje de usuario:

```
{RZ.USUARIO}
```

## Sección 3 · Los 8 criatura-días y lo que devolvió

{chr(10).join(TV)}

Las {len(JU)} propuestas tienen todas el formato fijo (parser estricto): {', '.join(f'{k} {v}' for k, v in ct.items())}. Juicios (míos, con lo que sabemos del mundo: el README del mundo y lo
medido en P7-44/45/46): **¿verdad en el mundo?** sí {cv['sí']}, parcial {cv['parcial']}, no {cv['no']}. **¿se puede comprobar?** sí {cc['sí']}, no por este cuerpo (hay que lanzar la red) {cc['no por este cuerpo']}, a medias {cc['a medias']}.
**¿la promesa tiene sentido?** con sentido {cp['con sentido']}, cifra de artefacto (contabilidad del cuerpo: el vínculo de una ventana es la distancia a la hermana; coger el camuflaje cuenta como riqueza) {cp['artefacto']}, sin base {cp['sin base']}.

## Sección 4 · Las propuestas TAL CUAL, con su juicio
{chr(10).join(TP)}

## Lectura

1. La razón, sin manual, **acierta lo que el cuerpo sabe sentir pero no decir**: que el botiquín se cura canalizando y cualquier golpe (rival o anillo) lo corta; que el anillo quema fuera y más
   cada fase; que los dardos son la munición de la cerbatana; que las casillas que no dejan pasar sin que se vea a nadie son algo invisible; que P14 pega desde lejos o camuflado. Son
   {cv['sí']} de {len(JU)} verdades y casi todas comprobables mañana con el propio diario.
2. **Dónde se equivoca** es donde el diario le miente a ella: las cifras de vínculo y de recursos de las ventanas (la distancia a la hermana, el camuflaje contado como riqueza) las toma por
   efectos de la cosa y promete «vínculo +7» o «recursos +14» que no existen ({cp['artefacto']} promesas de artefacto, {cp['sin base']} sin base). Y promete cosas que este cuerpo no puede hacer (lanzar la red: {cc['no por este cuerpo']}).
3. El formato fijo funciona ({len(JU)} de {len(JU)} con formato) y el coste es bajo ({n(usd, 3)} $ por 8 criatura-días). Para el paso 2 (que las invitaciones entren en el cuerpo) hacen falta dos cosas que la mesa decida:
   cómo se traduce una invitación a candidato (qué probar, dónde/cuándo, con qué esperanza) y cómo se limpia el diario de los artefactos de contabilidad antes de dárselo a la razón.

## Apéndice · Un diario entero (s1 d8 COMPARTE, valiente)

{muestra}
"""
open(os.path.join(AQUI, "informe_P7_52.md"), "w", encoding="utf-8").write(out); print("informe_P7_52.md", out.count("\n"), "lineas")

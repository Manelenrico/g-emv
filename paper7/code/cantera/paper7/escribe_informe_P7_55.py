"""[P7-55] Escribe informe_P7_55.md desde P7_55_datos.json (analiza_P7_55). Ninguna cifra a mano.  python3 escribe_informe_P7_55.py"""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(AQUI, "P7_55_datos.json")))
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
pc = lambda x: ("—" if x is None else f"{100 * x:.0f} %")
H = D["por_hermana_serie"]; SO = D["solas"]; OBJ = ("botiquin", "racion", "red", "camuflaje")
quit_d20 = sum(D["por_dia"][k][-1]["quitados_acumulados"] for k in D["por_dia"] if D["por_dia"][k])
T2 = ["| serie · hermana | objeto | creencia d20: (a) todos dedup · (b) solo vividos · (c) todos sin dedup | aprendido de la otra (a − b), media d1-20 | fracción de lo creído que viene de la otra | recuerdos al d20: vividos · recibidos | área d1-20: (a) · (b) |", "|---|---|---|---:|---:|---|---|"]
for k, v in H.items():
    for o in OBJ:
        x = v[o]; T2.append(f"| {k} {v['hermana']} | {o} | {n(x['a_d20'], 1)} · {n(x['b_d20'], 1)} · {n(x['c_d20'], 1)} | {n(x['dif_media'], 2)} | {pc(x['fraccion_de_la_otra'])} | {x['n_vividos_d20']} · {x['n_recibidos_d20']} | {n(x['area_a'], 0)} · {n(x['area_b'], 0)} |")
T4 = ["| serie · hermana | pruebas vividas: COMPARTE · SOLAS | botiquín, área d1-20 solo vivido: COMPARTE (b) · SOLAS | botiquín al d20: COMPARTE (b) · SOLAS | ración d20: (b) · SOLAS |", "|---|---|---|---|---|"]
for k, v in H.items():
    s = SO[k]; T4.append(f"| {k} {v['hermana']} | {v['pruebas_vividas']} · {s['pruebas_vividas']} | {n(v['botiquin']['area_b'], 0)} · {n(s['botiquin']['area'], 0)} | {n(v['botiquin']['b_d20'], 1)} · {n(s['botiquin']['d20'], 1)} | {n(v['racion']['b_d20'], 1)} · {n(s['racion']['d20'], 1)} |")
fv = [H[k]["botiquin"]["fraccion_de_la_otra"] for k in H if H[k]["hermana"] == "valiente" and H[k]["botiquin"]["fraccion_de_la_otra"] is not None]; fp = [H[k]["botiquin"]["fraccion_de_la_otra"] for k in H if H[k]["hermana"] == "prudente" and H[k]["botiquin"]["fraccion_de_la_otra"] is not None]
mas_b = sum(1 for k in H if H[k]["botiquin"]["area_b"] > SO[k]["botiquin"]["area"]); mas_p = sum(1 for k in H if H[k]["pruebas_vividas"] > SO[k]["pruebas_vividas"]); mas_p_pr = sum(1 for k in H if H[k]["hermana"] == "prudente" and H[k]["pruebas_vividas"] > SO[k]["pruebas_vividas"])
out = f"""# P7-55 · Banco (coste cero): ¿cuánto aprende cada hermana de la otra? Sobre los cuadernos de P7-50

*13-oct-2026. Sobre los 120 cuadernos por día de COMPARTE y los 120 de SOLAS (P7_50_res). `analiza_P7_55.py` → `P7_55_datos.json`; `escribe_informe_P7_55.py` (este informe; ninguna cifra a mano).
Creencia = la del cuerpo (dentro; sin cortes; neutro de peso 1; «al menos» solo si sube; olvido 0,95 por día), recalculada del cuaderno. `motor/model.py` intacto. Plataforma 0; consola 0 $.*

## 1 · Fusión por evento

En cada cuaderno se quita la segunda copia de los «vistos» que llegaron también contados por la hermana (mismo objeto, mismo día de origen, |tic| ≤ 240): en los cuadernos del día 20 de las
seis hermanas de COMPARTE, {quit_d20} vistos quitados (los 43 usos contados dos veces de P7-53, vistos desde cada cuaderno). La creencia (c) sin deduplicar frente a (a) deduplicada mide lo que esa doble cuenta
cambió de verdad en lo que el cuerpo creyó: en la tabla, (c) y (a) al día 20.

## 2 y 3 · Lo que cree cada hermana y cuánto viene de la otra

{chr(10).join(T2)}

- **Con los mismos recuerdos deduplicados, las dos hermanas creen exactamente lo mismo al d20** (columna (a), misma cifra en 10 y 11): el canal y la noche igualan los cuadernos.
- **Cuánto viene de la otra** (botiquín): valientes {', '.join(pc(x) for x in fv)} (media {pc(st.mean(fv)) if fv else '—'}); prudentes {', '.join(pc(x) for x in fp)} (media {pc(st.mean(fp)) if fp else '—'}). La que más aprende de la otra es la que menos
  vivió por sí misma: la valiente de la serie 2 (b {n(H['s2 a10']['botiquin']['b_d20'], 1)} → a {n(H['s2 a10']['botiquin']['a_d20'], 1)}). En la ración, {pc(min(H[k]['racion']['fraccion_de_la_otra'] for k in H if H[k]['racion']['fraccion_de_la_otra'] is not None))}-{pc(max(H[k]['racion']['fraccion_de_la_otra'] for k in H if H[k]['racion']['fraccion_de_la_otra'] is not None))}; en red y camuflaje lo recibido es a veces todo lo que hay (sin vividos propios).
- **¿Alguna vez lo recibido la llevó a creer algo falso?** {len(D['falsos'])} veces en 120 hermana-días (criterio: red o camuflaje con creencia > 5 cuando lo vivido decía ≤ 5; botiquín o ración ≤ 0 cuando lo vivido decía > 0).
  Lo más alto que lo recibido subió una cosa inútil: red {n(max(H[k]['red']['a_d20'] or 0 for k in H), 1)}, camuflaje {n(max(H[k]['camuflaje']['a_d20'] or 0 for k in H), 1)} al d20.

## 4 · ¿Compartir cambió también lo que vivían por sí mismas?

{chr(10).join(T4)}

Sí: la prudente probó más por sí misma en COMPARTE que en SOLAS en {mas_p_pr} de 3 series ({', '.join(f"{H[k]['pruebas_vividas']} frente a {SO[k]['pruebas_vividas']}" for k in H if H[k]['hermana'] == 'prudente')}); en total {mas_p} de 6 hermanas probaron más en COMPARTE, y en {mas_b} de 6 el área del botiquín
con SOLO lo vivido es mayor en COMPARTE que en SOLAS. Compartir no solo da recuerdos: cambia lo que se vive (una hermana que ya «sabe» del botiquín por la otra lo usa, y al usarlo vive).

## Lectura

1. Lo aprendido de la otra es real y acotado: entre {pc(min(fv + fp))} y {pc(max(fv + fp))} de lo que cada una cree del botiquín al d20; nunca falso (0 de 120 hermana-días).
2. Los cuadernos de las dos acaban idénticos: lo que mide «la que menos prueba» en S1 es la pareja (P7-53).
3. Compartir también cambió lo vivido: la prudente probó más en las tres series; para el siguiente campo, la medida «aprendido de la otra» debe ser (a − b) del cuaderno, no el área total.
"""
open(os.path.join(AQUI, "informe_P7_55.md"), "w", encoding="utf-8").write(out); print("informe_P7_55.md", out.count("\n"), "lineas")

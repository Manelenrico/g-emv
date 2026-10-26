"""[P7-53] Escribe informe_P7_53.md (revision de Ari al capitulo 4 sobre P7-50) desde P7_53_datos.json (analiza_P7_53). Ninguna cifra a mano.  python3 escribe_informe_P7_53.py"""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(AQUI, "P7_53_datos.json")))
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
P = D["por_brazo_hermana"]; DUP = D["duplicados"]; S1 = D["S1"]; S1s = D["S1_sello"]; S2s = D["S2_sello"]
VG = json.load(open(os.path.join(AQUI, "P7_50_sello.json")))["con_todas"]["vigilancia"]; pr = lambda S, b: VG[f"s{S} {b}"]["pruebas_prudente"]
T1 = ["| brazo · hermana | vidas | vistos | contados (canal + noche) | duplicados (visto + contado del mismo uso) | peso extra de la segunda copia | peso total recibido | peso medio por recuerdo |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for k, v in P.items(): T1.append(f"| {k} | {v['vidas']} | {v['vistos']} | {v['contados']} | {v['duplicados']} | {n(v['peso_extra'], 1)} | {n(v['peso_recibido_total'], 1)} | {n(v['peso_medio_recibido'], 2)} |")
por_obj = {}; por_via = {}
for x in DUP: por_obj[x["objeto"]] = por_obj.get(x["objeto"], 0) + 1; por_via[x["via"]] = por_via.get(x["via"], 0) + 1
T2 = ["| brazo · hermana | distancia media a la hermana (casillas, las dos vivas) | fracción de tics con la hermana a la vista | roce_B medio | peso medio recibido (intensidad × B) |", "|---|---:|---:|---:|---:|"]
for k, v in P.items(): T2.append(f"| {k} | {n(v['dist_media'], 2)} | {n(v['vista_frac'], 3)} | {n(v['B_medio'], 3)} | {n(v['peso_medio_recibido'], 2)} |")
T3 = ["| serie | la que menos prueba (en SOLAS: pruebas 10 · 11) | en COMPARTE, recibidos y peso total: valiente (10) · prudente (11) | peso medio: 10 · 11 | distancia media: 10 · 11 | B: 10 · 11 | a la vista: 10 · 11 |", "|---|---|---|---|---|---|---|"]
for k, f in S1.items():
    a, b = f["a10"], f["a11"]; T3.append(f"| {k} | asiento {f['hermana_que_menos_prueba']} ({'prudente' if f['hermana_que_menos_prueba'] == 11 else 'valiente'}; {f['pruebas_solas'].get('10')} · {f['pruebas_solas'].get('11')}) | {a['recibidos']} · {n(a['peso_total'], 0)} frente a {b['recibidos']} · {n(b['peso_total'], 0)} | {n(a['peso_medio'], 2)} · {n(b['peso_medio'], 2)} | {n(a['dist_media'], 2)} · {n(b['dist_media'], 2)} | {n(a['B_medio'], 3)} · {n(b['B_medio'], 3)} | {n(a['vista_frac'], 2)} · {n(b['vista_frac'], 2)} |")
cv, cp = P["COMPARTE · valiente"], P["COMPARTE · prudente"]
out = f"""# P7-53 · Banco (coste cero): la revisión de Ari al capítulo 4, sobre los datos de P7-50

*13-oct-2026. Sobre los {D['vidas']} diarios válidos de P7-50 (nada se juega, nada se toca). `analiza_P7_53.py` → `P7_53_datos.json`; `escribe_informe_P7_53.py` (este informe; ninguna cifra a mano).
`motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Plataforma 0; consola 0 $.*

## 1 · Doble cuenta: ¿un uso de la hermana llegó como «visto» y además como «contado»?

Fusión por evento: mismo objeto, misma hermana, |tic de su ventana − tic en que lo vi| ≤ 240, el contado del mismo día por el canal o el de la noche siguiente con ese día como origen.

{chr(10).join(T1)}

**Sí: {len(DUP)} de los {cv['vistos'] + cp['vistos']} vistos de COMPARTE llegaron también contados** ({', '.join(f'{k} {v}' for k, v in por_via.items())}; por objeto: {', '.join(f'{k} {v}' for k, v in por_obj.items())}), casi siempre en el MISMO tic (la hermana
cierra su ventana y la cuenta por el canal en el siguiente hueco del parte; yo la vi cerrar). El uso entró dos veces en el cuaderno: la copia vista (peso = su intensidad en mi escala × B) y la
copia contada (peso = la intensidad de ella × B). Peso extra de la segunda copia: {n(cv['peso_extra'], 1)} en las valientes y {n(cp['peso_extra'], 1)} en las prudentes ({n(100 * (cv['peso_extra'] + cp['peso_extra']) / (cv['peso_recibido_total'] + cp['peso_recibido_total']), 1)} % de todo el peso recibido). Es un fallo de
diseño de `hermanas_P7_48` (no se fusiona el visto con el contado): para el siguiente campo, un uso = un recuerdo (fusión por hermana + instante ± ventana, quedándose con el contado,
que trae el efecto medido por ella, y anotando «visto» como confirmación). No se cambia nada a mitad de nada; queda apuntado.

## 2 · Distancia y vínculo

{chr(10).join(T2)}

Las parejas van pegadas en los dos brazos (≈ {n(min(v['dist_media'] for v in P.values()), 1)}-{n(max(v['dist_media'] for v in P.values()), 1)} casillas de media, a la vista el {n(100 * min(v['vista_frac'] for v in P.values()), 0)}-{n(100 * max(v['vista_frac'] for v in P.values()), 0)} % de los tics con las dos vivas) y **roce_B está saturado en 1** ({n(min(v['B_medio'] for v in P.values()), 3)}-{n(max(v['B_medio'] for v in P.values()), 3)} de media): el peso «intensidad × B»
fue en la práctica la intensidad sola; la confianza según el vínculo no llegó a actuar en este campo (B solo baja sin la hermana, y aquí casi nunca falta). El peso medio recibido es
mayor en la valiente ({n(cv['peso_medio_recibido'], 2)}) que en la prudente ({n(cp['peso_medio_recibido'], 2)}) porque lo que recibe cada una es lo que vivió la OTRA: la prudente prueba más y con más intensidad.

## 3 · S1 releída

{chr(10).join(T3)}

- **¿La valiente recibió menos peso por estar más lejos?** No: la distancia y la vista son las mismas para las dos (es la misma pareja) y B ≈ 1 en todas; la valiente recibió MÁS peso
  ({n(cv['peso_recibido_total'], 0)} frente a {n(cp['peso_recibido_total'], 0)} en 60 vidas), porque recibe lo que la prudente vive, y la prudente prueba más.
- **¿Cambia la lectura de «la que menos prueba aprende más»?** Sí, en dos cosas. (i) En las series 1 y 2 la que menos prueba (en SOLAS) es la prudente; en COMPARTE esa misma hermana
  recibió menos peso que su hermana (series 1 y 2: {S1['1']['a11']['recibidos']} · {n(S1['1']['a11']['peso_total'], 0)} y {S1['2']['a11']['recibidos']} · {n(S1['2']['a11']['peso_total'], 0)} frente a {S1['1']['a10']['recibidos']} · {n(S1['1']['a10']['peso_total'], 0)} y {S1['2']['a10']['recibidos']} · {n(S1['2']['a10']['peso_total'], 0)}), y además probó MÁS por sí misma que en SOLAS (P7-50: {pr(1, 'COMPARTE')} y {pr(2, 'COMPARTE')} pruebas frente a {pr(1, 'SOLAS')} y {pr(2, 'SOLAS')}):
  parte de su área del botiquín en COMPARTE es suya, no recibida. (ii) Como los dos cuadernos convergen (S2: {n(S2s.get('media_C'), 2)} de diferencia frente a {n(S2s.get('media_S'), 2)}), el área de «la que menos prueba» en COMPARTE es
  en realidad el área de la pareja: S1 mide que la pareja que comparte cree más que la que menos prueba de la pareja que no comparte ({n(S1s.get('media_C'), 0)} frente a {n(S1s.get('media_S'), 0)}, +{n(S1s.get('dif'), 0)} ± {n(S1s.get('ee'), 0)}), no que la más
  callada aprenda de la otra. La lectura honesta: compartir iguala a las dos en lo que la pareja vivió, y la pareja que comparte prueba algo más; con {len(DUP)} usos contados dos veces
  ({n(100 * (cv['peso_extra'] + cp['peso_extra']) / (cv['peso_recibido_total'] + cp['peso_recibido_total']), 0)} % del peso), lo recibido pesó algo más de lo que el diseño decía. Los veredictos del sello (S1, S2, S3 no pasan) no cambian.

## 4 · Corrección en los textos: el camuflaje

Revisión de Ari (`obs.nim:32-44`): el camuflaje **limita a 4 casillas (quieta) o 7 (si se ha movido en los últimos 24 instantes) la distancia a la que te ven, frente a 8 o más
normalmente; atacar lo delata 5 s.** Lo que escribí («oculta más allá de 4/7 casillas hasta atacar») se corrige con una fe de erratas fechada al principio de `informe_P7_44.md`,
`informe_P7_47.md` e `informe_P7_52.md` (los informes no se reescriben); las medidas y los veredictos no cambian. La constante [impl] `CAMO_REVELADO_S = 5.0` de la appraisal
congelada coincide con los 5 s de Ari.

## Apuntes para la mesa (no se ejecuta nada)

1. Fusionar visto y contado por evento en `hermanas` (un uso = un recuerdo).
2. B saturado: si la confianza según el vínculo ha de actuar, hace falta que B se mueva (hoy solo baja sin la hermana); medir B en parejas que se separan (ninguna aquí) o cambiar su escala es decisión de la mesa.
3. S1 como está mide a la pareja; si se quiere medir «la callada aprende de la otra», la medida ha de descontar lo que la callada probó por sí misma ese día (p. ej. área atribuible a recibidos: creencia con y sin los recuerdos de origen contado/visto, recalculada del cuaderno).
"""
open(os.path.join(AQUI, "informe_P7_53.md"), "w", encoding="utf-8").write(out); print("informe_P7_53.md", out.count("\n"), "lineas")

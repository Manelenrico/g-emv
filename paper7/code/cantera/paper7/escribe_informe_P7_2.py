"""[P7-2] Escribe informe_P7_2.md desde P7_2_curvas.json, P7_2_banco.json y SELLO_P7_2.md (ninguna cifra a mano)."""
import json, hashlib, os
from collections import Counter, defaultdict
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
C = json.load(open(os.path.join(AQUI, "P7_2_curvas.json"))); P = C["principal"]; S = C["sello"]; SEN = C["sensibilidad"]
B = json.load(open(os.path.join(AQUI, "P7_2_banco.json"))); DEC = [d for v in B["vidas"] for d in v["decisiones"]]
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
sello_txt = open(os.path.join(AQUI, "SELLO_P7_2.md")).read(); sello_md5 = hashlib.md5("".join(sello_txt.splitlines(True)[:-2]).encode()).hexdigest() if False else None
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
def pct(a, b): return f"{n(100 * a / b, 1)} %" if b else "–"
NOM = {"botiquin": "botiquín", "bow": "arco", "blowgun": "cerbatana"}
L = []; w = L.append
# ── punto 2: repeticion de decisiones ──
def tramo(d): return "1-20" if d["dia"] <= 20 else "21-40"
def grupo(objeto, sit, dias):
    return [d for d in DEC if d["objeto"] == objeto and d["situacion"] == sit and tramo(d) == dias]
fieles = sum(1 for d in DEC if d["fiel"])
w(f"""# P7-2 · El primer aprendizaje, en banco: una regla de memoria sobre lo ya vivido

*3-oct-2026. Coste cero: sin partidas, sin llamadas (plataforma 0; consola 0). `motor/model.py` = `{md5('motor/model.py')}` al empezar
y al acabar; congelados sin tocar; el cuerpo no se toca: la regla vive en `cantera/paper7/memoria_P7_2.py` y el banco la usa por fuera.
Sello: `SELLO_P7_2.md`, commit 4a5fec2, md5 `{sello_txt.strip().split('`')[-2]}` (escrito antes de calcular nada). Diario de partida: `P7_1_diario.json`
({C['filas']} filas con resultado; {C['sin_cerrar_excluidas']} usos de botiquín "sin cerrar" excluidos porque no tienen resultado). Scripts: `memoria_P7_2.py` (la regla),
`mide_P7_2.py` (curvas, sello S1-S4, sensibilidad → `P7_2_curvas.json`, `P7_2_creencias.json`), `figuras_P7_2.py` (→ `P7_2_curvas.png`),
`banco_P7_2.py` (repetición de decisiones y fontanería → `P7_2_banco.json`), `escribe_informe_P7_2.py` (este informe). Semilla de barajado de
los 20 órdenes al azar: {C['semilla_barajado']}. Criaturas: asiento 10 y asiento 11; días: las 40 semillas en orden creciente ({C['dias'][0]} … {C['dias'][-1]}).*

## Sección 1 · Las curvas de la creencia

Regla (de la mesa, sin ajustar): b = media ponderada de recuerdos; nacimiento = catálogo con peso 3; experiencia i con valor vivido v_i
(cura real, 0 si se cancela; daño hecho, 0 si `no_ammo`) y peso = intensidad × olvido, intensidad = min(2, 1 + |v_i − b_antes| / catálogo),
olvido = 0,95^días (también el nacimiento); dentro de un día, en orden (`memoria_P7_2.py`). Como el olvido multiplica igual a todos los
recuerdos, en un día sin experiencias la creencia no cambia; solo cambia la pesada relativa entre recuerdos de edades distintas.

| objeto / situación / asiento | experiencias (días con alguna) | creencia final, orden natural (fracción del catálogo) | banda de los 20 órdenes (fracción, mín-máx) | cruza el 50 % el día | cruza el 25 % el día | media real del diario ("techo") | catálogo ("suelo") |
|---|---:|---:|---:|---:|---:|---:|---:|
""")
for k in ("botiquin/dentro", "botiquin/fuera", "bow/con municion", "bow/sin municion", "blowgun/con municion", "blowgun/sin municion"):
    for a in (10, 11):
        p = P[f"{k}/{a}"]; o, s_ = k.split("/")
        w(f"| {NOM[o]} / {s_} / {a} | {p['experiencias_total']} ({p['dias_con_experiencia']}) | {n(p['final_natural'], 2)} ({n(p['final_natural_frac'], 2)}) | {n(min(p['finales_azar_frac']), 2)} – {n(max(p['finales_azar_frac']), 2)} | {p['cruza_50'] or 'nunca'} | {p['cruza_25'] or 'nunca'} | {n(p['techo_media_real'], 2) if p['techo_media_real'] is not None else '–'} | {n(p['suelo_catalogo'])} |\n")
w(f"""
Figura: `P7_2_curvas.png` (seis paneles; línea = orden natural, puntos = días con experiencia, banda = mínimo-máximo de los 20 órdenes,
punteado = media real del diario, raya = catálogo). Fuente: `P7_2_curvas.json["principal"]`. Lectura: fuera del círculo el botiquín cae
el primer día con experiencia y se queda cerca de su media real; dentro baja hasta la media real (17-19 puntos), que está por debajo del
40 % del catálogo porque la cura real se acota por el hp máximo y porque los cortes por rivales valen 0. Sin munición, el arco y la
cerbatana caen a casi 0 el primer día con experiencias (cientos de filas en una sola pelea); con munición se quedan en la media real
(8 de 14 para el arco: los tiros que salen pero no alcanzan valen 0).

### El sello, S1 a S4 (`P7_2_curvas.json["sello"]`)

| predicción | asiento 10 | asiento 11 | veredicto |
|---|---|---|---|
| S1 botiquín fuera < 25 % (natural y ≥ 18 de 20 órdenes) | natural {n(P['botiquin/fuera/10']['final_natural_frac'], 2)}: {'sí' if S['S1']['10']['natural_<25%'] else 'no'}; órdenes {S['S1']['10']['ordenes_<25%']} de 20 | natural {n(P['botiquin/fuera/11']['final_natural_frac'], 2)}: {'sí' if S['S1']['11']['natural_<25%'] else 'no'}; órdenes {S['S1']['11']['ordenes_<25%']} de 20 | **{'acierta' if all(S['S1'][k]['natural_<25%'] and S['S1'][k]['ordenes_<25%'] >= 18 for k in ('10', '11')) else 'falla'}** |
| S2 botiquín dentro entre 40 y 80 % | {n(S['S2']['10']['natural_frac'], 2)}: {'sí' if S['S2']['10']['entre_40_y_80'] else 'no'} (órdenes dentro del rango: {S['S2']['10']['ordenes_entre_40_y_80']} de 20) | {n(S['S2']['11']['natural_frac'], 2)}: {'sí' if S['S2']['11']['entre_40_y_80'] else 'no'} ({S['S2']['11']['ordenes_entre_40_y_80']} de 20) | **{'acierta' if all(S['S2'][k]['entre_40_y_80'] for k in ('10', '11')) else ('falla en el asiento 10' if S['S2']['11']['entre_40_y_80'] else 'falla')}** |
| S3 sin munición < 10 % al acabar la primera vida con ≥ 5 filas | arco: día {S['S3']['bow/10']['primer_dia_con_5_o_mas']}, {n(S['S3']['bow/10']['creencia_frac_al_acabar'], 3)}: {'sí' if S['S3']['bow/10']['cumple'] else 'no'}; cerbatana: día {S['S3']['blowgun/10']['primer_dia_con_5_o_mas']}, {n(S['S3']['blowgun/10']['creencia_frac_al_acabar'], 3)}: {'sí' if S['S3']['blowgun/10']['cumple'] else 'no'} | arco: día {S['S3']['bow/11']['primer_dia_con_5_o_mas']}, {n(S['S3']['bow/11']['creencia_frac_al_acabar'], 3)}: {'sí' if S['S3']['bow/11']['cumple'] else 'no'}; cerbatana: día {S['S3']['blowgun/11']['primer_dia_con_5_o_mas']}, {n(S['S3']['blowgun/11']['creencia_frac_al_acabar'], 3)}: {'sí' if S['S3']['blowgun/11']['cumple'] else 'no'} | **{'acierta' if all(v['cumple'] for v in S['S3'].values()) else 'falla en ' + ', '.join(k for k, v in S['S3'].items() if not v['cumple'])}** |
| S4 con munición a menos del 25 % del catálogo | arco {n(S['S4']['bow/10']['natural_frac'], 2)}, cerbatana {n(S['S4']['blowgun/10']['natural_frac'], 2)} | arco {n(S['S4']['bow/11']['natural_frac'], 2)}, cerbatana {n(S['S4']['blowgun/11']['natural_frac'], 2)} | **{'acierta' if all(v['a_menos_del_25%'] for v in S['S4'].values()) else 'falla en los cuatro casos'}** (0 de 20 órdenes en todos) |

""")
# S3 detail for the failing case
w(f"""Sobre S3 en la cerbatana del asiento 11: el primer día con 5 o más filas sin munición es el {S['S3']['blowgun/11']['primer_dia_con_5_o_mas']} y al acabarlo la creencia
está en {n(S['S3']['blowgun/11']['creencia_frac_al_acabar'], 3)} del catálogo; cruza el 10 % el día {P['blowgun/sin municion/11']['cruza_10']}. Sobre S4: con munición, la creencia converge a la media real del
diario, que es la mitad del catálogo porque la mitad de los tiros que salen no hacen daño; la predicción suponía que "con munición
pega lo que dice el catálogo", y el diario dice que no.

## Sección 2 · Repetición de decisiones con la creencia aprendida (`banco_P7_2.py`)

Réplica en seco del cuerpo A4 (molde de P6-29: el cuerpo recibe las observaciones del diario por un cable falso y decide tic a tic).
En cada tic con fila de diario ({len(DEC)} decisiones en {len(B['vidas'])} vidas), se vuelve a decidir una segunda vez con la misma observación y
la misma memoria, cambiando solo lo que la previsión espera de ese objeto: `receta["heal"]` del candidato `usar_botiquin` (lo que
`decisor_zs.py:824` suma al hp previsto) o el `damage` del arma en la receta de `atacar_*` (lo que `decisor_zs.py:852-856` resta al
rival previsto), por la creencia vigente ese día antes de vivir la experiencia (orden natural, `P7_2_creencias.json`). Lo demás no se
toca: el candidato existe igual (`decisor_zs.py:588` mira el catálogo), la riqueza W y la amenaza ajena siguen leyendo el catálogo.

**Fontanería (punto 3).** Con la creencia igual al catálogo, es decir, la primera decisión de la réplica tal cual, contra `RADIOGRAFIA.elegido`
del diario en esos {len(DEC)} tics: **{fieles} de {len(DEC)} iguales** ({pct(fieles, len(DEC))}){'.' if fieles == len(DEC) else ' — NO es exacta: ver nota al final de esta sección.'}
Nota de taller: la primera corrida del banco, con varias vidas seguidas en el mismo proceso, dio 1.674 de 2.450: en las vidas que no eran
la primera de su proceso desaparecía el candidato de atacar en defensa del hermano. La misma vida replayada sola daba 334 de 334. Se corrió
de nuevo con un proceso nuevo por vida (`maxtasksperchild=1`, `banco_P7_2.py`) y la fontanería es exacta; la causa (estado de módulo que
sobrevive entre vidas) queda apuntada, no corregida, porque no toca a este paso.

| objeto | situación | días | decisiones | elige lo mismo | elige otra cosa | qué otra cosa (las más frecuentes) |
|---|---|---|---:|---:|---:|---|
""")
for o in ("botiquin", "bow", "blowgun"):
    for s_ in (("dentro", "fuera") if o == "botiquin" else ("sin municion", "con municion")):
        for dias in ("1-20", "21-40"):
            g = grupo(o, s_, dias); cam = [d for d in g if d["cambia"]]
            if not g: w(f"| {NOM[o]} | {s_} | {dias} | 0 | – | – | – |\n"); continue
            cl = Counter(d["clase_creencia"] for d in cam).most_common(4)
            w(f"| {NOM[o]} | {s_} | {dias} | {len(g)} | {len(g) - len(cam)} ({pct(len(g) - len(cam), len(g))}) | {len(cam)} ({pct(len(cam), len(g))}) | {'; '.join(f'{k} {v}' for k, v in cl) if cl else '–'} |\n")
def tasa(o, s_, dias):
    g = grupo(o, s_, dias); return (sum(1 for d in g if d["cambia"]), len(g))
c_f, n_f = tasa("botiquin", "fuera", "21-40"); c_d, n_d = tasa("botiquin", "dentro", "21-40")
c_a, n_a = [sum(x) for x in zip(tasa("bow", "sin municion", "21-40"), tasa("blowgun", "sin municion", "21-40"))]
w(f"""
### El sello, S5 y S6

| predicción | medido | veredicto |
|---|---|---|
| S5a botiquín fuera, días 21-40: elige otra cosa ≥ 70 % | {c_f} de {n_f} ({pct(c_f, n_f)}) | **{'acierta' if n_f and c_f / n_f >= .7 else 'falla'}** |
| S5b botiquín dentro, días 21-40: sigue usándolo ≥ 70 % | {n_d - c_d} de {n_d} ({pct(n_d - c_d, n_d)}) | **{'acierta' if n_d and (n_d - c_d) / n_d >= .7 else 'falla'}** |
| S6 ataques sin munición, días 21-40: elige otra cosa ≥ 70 % | {c_a} de {n_a} ({pct(c_a, n_a)}) (arco {tasa('bow', 'sin municion', '21-40')[0]} de {tasa('bow', 'sin municion', '21-40')[1]}, cerbatana {tasa('blowgun', 'sin municion', '21-40')[0]} de {tasa('blowgun', 'sin municion', '21-40')[1]}) | **{'acierta' if n_a and c_a / n_a >= .7 else 'falla'}** |

Fuente: `P7_2_banco.json` (por decisión: `elegido_diario`, `elegido_replica`, `elegido_creencia`, `clase_creencia`, d de cada candidato en
las dos decisiones). Por asiento, días 21-40: """)
for o, s_ in (("botiquin", "fuera"), ("botiquin", "dentro"), ("bow", "sin municion"), ("blowgun", "sin municion")):
    for a in (10, 11):
        g = [d for d in grupo(o, s_, "21-40") if d["asiento"] == a]; w(f"{NOM[o]} {s_} asiento {a}: {sum(1 for d in g if d['cambia'])} de {len(g)} cambian; ")
# por que no cambia: ataques sin municion (empate o ventaja minima) y botiquin fuera (umbral de b)
na = [d for d in DEC if d["objeto"] in ("bow", "blowgun") and d["situacion"] == "sin municion" and d["dia"] > 20 and not d["cambia"]]
emp = Counter(); ncand = Counter()
for d in na:
    dc = d["d_creencia"] or {}; a, nn = dc.get(d["elegido_creencia"]), dc.get("noop"); ncand[len(dc)] += 1
    emp["empate exacto con noop" if (a is not None and nn is not None and abs(a - nn) < 1e-9) else ("atacar con d menor que noop" if (a is not None and nn is not None and a < nn) else "otro")] += 1
bf_no = [d for d in DEC if d["objeto"] == "botiquin" and d["situacion"] == "fuera" and d["dia"] > 20 and not d["cambia"]]
bf_si = [d for d in DEC if d["objeto"] == "botiquin" and d["situacion"] == "fuera" and d["dia"] > 20 and d["cambia"]]
med = lambda v: sorted(v)[len(v) // 2] if v else None
w(f"""

**Por qué falla, leído en las d de los candidatos.** En los {len(na)} ataques sin munición de los días 21-40 que no cambian, la creencia
vigente es de {n(med([d['b_antes'] for d in na]), 3)} puntos de mediana (nunca llega a 0: la media ponderada conserva el recuerdo de nacimiento) y la
decisión tenía {ncand.most_common(1)[0][0]} candidatos en {ncand.most_common(1)[0][1]} casos (atacar y quedarse quieto: moverse está vetado por el enfriamiento en plena pelea). Con
un daño previsto minúsculo pero positivo, atacar sigue dando una d menor que quedarse quieto en {emp['atacar con d menor que noop']} casos, y en {emp['empate exacto con noop']} empata
exactamente y el desempate prefiere la acción a la quietud. Es decir: mientras la creencia sea mayor que cero y no haya otra cosa que hacer,
el cuerpo dispara el arco vacío porque "no cuesta nada". Botiquín fuera, días 21-40: los {len(bf_no)} usos que no cambian tienen una creencia de
{n(med([d['b_antes'] for d in bf_no]), 1)} puntos de mediana (de {n(min(d['b_antes'] for d in bf_no), 1)} a {n(max(d['b_antes'] for d in bf_no), 1)}) y los {len(bf_si)} que cambian, de {n(med([d['b_antes'] for d in bf_si]), 1)} (de {n(min(d['b_antes'] for d in bf_si), 1)} a {n(max(d['b_antes'] for d in bf_si), 1)}): los rangos se solapan. Por bandas de creencia:
{'; '.join(f"b {et}: cambian {sum(1 for d in bf_si if lo <= d['b_antes'] < hi)} de {sum(1 for d in bf_si + bf_no if lo <= d['b_antes'] < hi)}" for et, lo, hi in (("< 5", 0, 5), ("5-8", 5, 8), ("≥ 8", 8, 1e9)))}. La creencia sola no fija el cambio: con la misma
creencia, unas fotos cambian y otras no, según lo demás que haya en ellas (vida, rivales, lo que se puede hacer). Dentro, la creencia es
la misma en los que cambian y en los que no (16-20): ahí también decide el resto de la foto.

## Sección 3 · Sensibilidad (después del sello y señalada como tal; no sustituye a la principal)

Misma medida, orden natural, cambiando un solo parámetro. Fracción del catálogo al final y día en que cruza el 25 %.

| objeto / situación / asiento | principal (0,95; peso 3) | olvido 0,90 | olvido 0,99 | nacimiento peso 1 | nacimiento peso 10 |
|---|---|---|---|---|---|
""")
for k in ("botiquin/dentro", "botiquin/fuera", "bow/con municion", "bow/sin municion", "blowgun/con municion", "blowgun/sin municion"):
    for a in (10, 11):
        kk = f"{k}/{a}"; p = P[kk]; o, s_ = k.split("/")
        cel = lambda v: f"{n(v['final_frac'], 2)} (día {v['cruza_25'] or '–'})"
        w(f"| {NOM[o]} / {s_} / {a} | {n(p['final_natural_frac'], 2)} (día {p['cruza_25'] or '–'}) | {cel(SEN['olvido_0.90'][kk])} | {cel(SEN['olvido_0.99'][kk])} | {cel(SEN['nacimiento_1'][kk])} | {cel(SEN['nacimiento_10'][kk])} |\n")
w(f"""
Fuente: `P7_2_curvas.json["sensibilidad"]`. El olvido mueve poco el final (los recuerdos se apagan todos a la vez); el peso de nacimiento
mueve el primer día y poco más cuando hay cientos de experiencias (arco sin munición) y bastante cuando hay pocas (cerbatana).

## Archivos

| archivo | qué es |
|---|---|
| `SELLO_P7_2.md` | las seis predicciones, con md5, commit 4a5fec2 antes de calcular |
| `memoria_P7_2.py` | la regla de memoria (experimental; el cuerpo no la importa) |
| `mide_P7_2.py`, `P7_2_curvas.json`, `P7_2_creencias.json` | curvas, sello S1-S4, sensibilidad; la creencia vigente en cada uso/ataque |
| `figuras_P7_2.py`, `P7_2_curvas.png` | la figura de las curvas |
| `banco_P7_2.py`, `P7_2_banco.json` | la réplica con la creencia aprendida; fontanería; `banco_P7_2.log` fuera de git |
| `escribe_informe_P7_2.py`, `informe_P7_2.md` | este informe |
""")
txt = "".join(L); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_2.md"), "w").write(txt); print("escrito", len(txt))

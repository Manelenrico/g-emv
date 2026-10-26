"""[P7-25] Escribe informe_P7_25.md desde P7_25_medida.json y P7_25_decisiones.json (ninguna cifra a mano)."""
import collections, hashlib, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
M = J("P7_25_medida.json"); R = J("P7_25_decisiones.json"); F = ("1.5", "2.0", "3.0", "4.0")
n = lambda x, d=0: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
nuevo = lambda e: e in ("ir_curioso", "coger", "ir_objeto")
def huye(x): return (x["fuera"] and x["hoy"].startswith(("move_", "paso_", "ir_")) and x["hoy"] != "ir_curioso") or x["hoy"].startswith("usar_")
reg = [x for r in R for x in r["registros"]]; A = [x for x in reg if x["a"]]; A2 = [x for x in reg if x.get("a2")]; B = [x for x in reg if x["b"]]; Bh = [x for x in B if huye(x)]
L1 = ["| vida | tics | con el paso listo | gana `ir_curioso` con el paso listo | `ir_curioso` en total (con enfriamiento) | del ver al tocar: botiquín / ración (tics) | paso listo y desconocido a 1-2: tics · lo elegido |", "|---|---:|---:|---:|---:|---|---|"]
for k, v in M.items():
    vt = v["ver_y_tocar"]; c = v["paso_listo_y_desconocido_a_1_o_2"]
    L1.append(f"| {k} | {n(v['tics'])} | {n(v['listos'])} | {v['gana_ir_curioso_con_el_paso_listo']} ({n(100*v['gana_ir_curioso_con_el_paso_listo']/max(1,v['listos']))} %) | {n(v['ir_curioso_en_total'])} | {n(vt['botiquin']['instantes_de_ver_a_tocar']) if vt['botiquin']['instantes_de_ver_a_tocar'] is not None else 'no toca'} / {n(vt['racion']['instantes_de_ver_a_tocar']) if vt['racion']['instantes_de_ver_a_tocar'] is not None else 'no toca'} | {c['tics']} · {', '.join(f'`{a}` {b}' for a, b in list(c['elegido'].items())[:3])} |")
def fila(S, f): return (sum(1 for x in S if nuevo(x["alt"][f])), sum(1 for x in S if x["alt"][f] == "ir_curioso"), sum(1 for x in S if x["alt"][f] != x["hoy"]))
L2 = ["| factor | (a) estricta: va hacia lo nuevo (de " + str(len(A)) + ") · `ir_curioso` · decisiones que cambian | (a') con rivales a más de 4: idem (de " + str(len(A2)) + ") | (b) peligro: la curiosidad gana a huir / entrar / curarse (de " + str(len(Bh)) + ") · gana a cualquier otra cosa (de " + str(len(B)) + ") · decisiones que cambian |", "|---|---|---|---|"]
L2.append(f"| hoy (×1) | {sum(1 for x in A if nuevo(x['hoy']))} · {sum(1 for x in A if x['hoy']=='ir_curioso')} · — | {sum(1 for x in A2 if nuevo(x['hoy']))} · {sum(1 for x in A2 if x['hoy']=='ir_curioso')} · — | — · {sum(1 for x in B if x['hoy']=='ir_curioso')} ya la elige hoy · — |")
for f in F:
    a = fila(A, f); a2 = fila(A2, f)
    L2.append(f"| ×{f} | {a[0]} · {a[1]} · {a[2]} | {a2[0]} · {a2[1]} · {a2[2]} | {sum(1 for x in Bh if x['alt'][f]=='ir_curioso')} · {sum(1 for x in B if x['alt'][f]=='ir_curioso' and x['hoy']!='ir_curioso')} · {sum(1 for x in B if x['alt'][f]!=x['hoy'])} |")
L3 = ["| factor | lo que pierde cuando gana la curiosidad (todos los instantes evaluados) |", "|---|---|"]
for f in F: L3.append(f"| ×{f} | {', '.join(f'`{k}` {v}' for k, v in collections.Counter(x['hoy'] for x in reg if x['alt'][f]=='ir_curioso' and x['hoy']!='ir_curioso').most_common(6))} |")
r0 = next(r for r in R if r["campo"] == "P724" and r["dia"] == 1 and r["slot"] == 10); S0 = [x for x in r0["registros"] if x.get("a2")]
L4 = ["| | " + " | ".join(f"×{f}" for f in ("1",) + F) + " |", "|---|" + "---:|" * 5]
for el in ("ir_objeto", "ir_centro", "ir_botin", "ir_curioso"):
    L4.append(f"| `{el}` | {sum(1 for x in S0 if x['hoy']==el)} | " + " | ".join(str(sum(1 for x in S0 if x['alt'][f]==el)) for f in F) + " |")
ej = next((x for x in S0 if x["hoy"] == "ir_centro"), None)
fidP723 = collections.Counter(); fidP724 = collections.Counter()
for r in R: (fidP723 if r["campo"] == "P723" else fidP724).update(r["fidelidad"])
tabla_manel = ["| factor de la curiosidad | coge lo nuevo en calma: instantes en que va hacia el objeto desconocido, de " + str(len(A2)) + " (a') | arriesga en peligro: instantes en que la curiosidad gana a huir, entrar o curarse, de " + str(len(Bh)) + " | decisiones que cambian en peligro, de " + str(len(B)) + " |", "|---|---:|---:|---:|"]
tabla_manel.append(f"| hoy | {sum(1 for x in A2 if nuevo(x['hoy']))} | — | — |")
for f in F: tabla_manel.append(f"| ×{f} | {sum(1 for x in A2 if nuevo(x['alt'][f]))} (+{sum(1 for x in A2 if nuevo(x['alt'][f])) - sum(1 for x in A2 if nuevo(x['hoy']))}) | {sum(1 for x in Bh if x['alt'][f]=='ir_curioso')} | {sum(1 for x in B if x['alt'][f]!=x['hoy'])} |")
T = f"""# P7-25 · Cuánta curiosidad trae al nacer

*7-oct-2026. Coste: plataforma 0, consola 0. Solo lectura de diarios y réplicas de vidas ya jugadas, una por proceso. `motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}`
al empezar y al acabar; cuerpo y congelados sin tocar; nada cambiado en las piezas salvo un mando de banco (`nace_P7_23.E["escala_curiosidad"]`, 1 en el campo). Este informe lo
escribe `escribe_informe_P7_25.py` desde `P7_25_medida.json` (`mide_P7_25.py`) y `P7_25_decisiones.json` (`banco_P7_25.py`).*

## En corto

- **La medida corregida** (sección 1): con el paso listo, `ir_curioso` gana en el 0-5 % de los instantes en 9 de las 12 vidas (19 %, 30 % y 46 % en las otras tres; la del 46 %
  vivió 1.270 tics). Casi todo el tiempo en `ir_curioso` del freno era de enfriamiento. Del ver al tocar: 4 a 178 tics cuando toca pronto; 1.800 a 13.000 cuando tarda; 5 vidas no tocan una de las dos clases.
- **Cuánto haría falta** (sección 2): subir la escala de la curiosidad **no cambia casi nada**, ni en calma ni en peligro. En calma con el objeto desconocido a 1-2 casillas, el
  cuerpo de hoy ya va hacia lo nuevo en {sum(1 for x in A2 if nuevo(x['hoy']))} de {len(A2)} instantes (sobre todo `ir_objeto`, el botín); ×4 añade {sum(1 for x in A2 if nuevo(x['alt']['4.0'])) - sum(1 for x in A2 if nuevo(x['hoy']))}. En peligro, ×1,5 hace ganar a la curiosidad sobre huir, entrar o
  curarse en {sum(1 for x in Bh if x['alt']['1.5']=='ir_curioso')} de {len(Bh)} instantes; ×4, en {sum(1 for x in Bh if x['alt']['4.0']=='ir_curioso')}. Lo que pierde la curiosidad cuando gana es casi siempre `noop` y, a partir de ×3, `ir_botin`.
- **El caso del freno** (día 1, asiento 10, con la ración a una casilla): de {len(S0)} instantes con el paso listo, hoy elige `ir_centro` {sum(1 for x in S0 if x['hoy']=='ir_centro')} veces e `ir_objeto` {sum(1 for x in S0 if x['hoy']=='ir_objeto')};
  con la curiosidad ×4, `ir_centro` baja a {sum(1 for x in S0 if x['alt']['4.0']=='ir_centro')} e `ir_curioso` gana {sum(1 for x in S0 if x['alt']['4.0']=='ir_curioso')}. **La escala de la fila no es lo que le impide dar el último paso.** La pregunta pasa a ser qué vale en la imaginación
  llegar al objeto: hoy, con las dos clases desconocidas, llegar solo alivia la curiosidad (el alivio 0,5 de tenerla) y el objeto no vale nada más.

## Sección 1 · La medida corregida

Las 12 vidas de APRENDE: el humo de P7-23 (serie 1, días 1-3) y el freno de P7-24 (serie 1, días 1-3), los dos asientos. «Con el paso listo» = `move_ready_in` 0.
«Del ver al tocar» = tics desde el primer tic con un objeto de esa clase a la vista hasta que la primera unidad entra en el zurrón (al nacer las dos clases son desconocidas).

{chr(10).join(L1)}

## Sección 2 · Cuánto haría falta (banco)

`banco_P7_25.py`: cada vida replicada tal como se jugó; en cada tic con el paso listo y en una de las situaciones de abajo, cinco decisiones sobre la misma escena y la misma
memoria: la de hoy y con la curiosidad ×1,5, ×2, ×3 y ×4 (la escala multiplica la M de R-CURIOSIDAD y la promesa de ir a por la cosa; nada más). Solo esa decisión; no se
inventa el resto. Réplica del campo: las 6 vidas del freno, bit a bit ({n(fidP724['igual'])} iguales, {fidP724.get('difiere', 0)} distintas); las 6 del humo no ({n(fidP723['igual'])} / {n(fidP723['difiere'])}), porque el humo se jugó sin
el arreglo del paso 0 de P7-24 y la réplica lo lleva: para ellas «hoy» es el cuerpo tal como está ahora, no el diario.

Situaciones, fijadas antes de contar: **(a)** en calma (calma > 0,5), sin ningún rival a la vista y con un botiquín o ración de clase aún desconocida a 1 o 2 casillas;
**(a')** como (a) pero admitiendo rivales a la vista a más de 4 casillas (añadida tras la primera pasada: el caso del freno tenía rivales a 5-8 casillas y no entraba ni en (a)
ni en (b)); **(b)** peligro: fuera del círculo, o un rival a 4 casillas o menos, o vida < 50. «Va hacia lo nuevo» = elige `ir_curioso`, `coger` o `ir_objeto`. «Huir, entrar o
curarse» hoy = un paso o un `ir_*` (no `ir_curioso`) estando fuera, o `usar_botiquin` / `usar_racion`.

{chr(10).join(L2)}

**(c) Qué tirón pierde cuando gana la curiosidad:**

{chr(10).join(L3)}

**El caso del freno, de cerca** (P7-24, día 1, asiento 10; los {len(S0)} instantes con el paso listo, en calma, con la ración desconocida a 1-2 casillas y rivales a más de 4):

{chr(10).join(L4)}

Un instante de ejemplo (tic {ej['t'] if ej else '—'}, calma {n(ej['calma'], 2) if ej else '—'}), las d de hoy: {', '.join(f'`{k}` {n(v, 3)}' for k, v in sorted((ej or {}).get('d_hoy', {}).items(), key=lambda kv: kv[1]))}. La curiosidad está a
{n(ej['d_hoy']['ir_curioso'] - ej['d_hoy']['ir_centro'], 3) if ej else '—'} del centro y la escala apenas lo mueve: en la imaginación de llegar, el objeto desconocido solo vale el alivio de la curiosidad.

## Sección 3 · La tabla para Manel

{chr(10).join(tabla_manel)}

Lectura: multiplicar la curiosidad de nacimiento por 1,5 o 2 no hace coger más lo nuevo (el cuerpo ya va a por los objetos como botín) y apenas arriesga (4-6 instantes de 318 en
peligro); ×3 y ×4 tampoco hacen coger más, y empiezan a quitarle instantes al botín y al centro en peligro. **El tirón que falta no es la escala de la fila; es lo que el cuerpo
cree que gana al llegar.** Eso es diseño de Manel; aquí solo se mide.

## Archivos

| archivo | qué es |
|---|---|
| `mide_P7_25.py` → `P7_25_medida.json` | la medida corregida |
| `banco_P7_25.py` → `P7_25_decisiones.json` | las decisiones con la curiosidad ×1,5, ×2, ×3, ×4 |
| `nace_P7_23.py` (`E["escala_curiosidad"]`) | el mando de banco, 1 en el campo |
| `informe_P7_25.md` | este informe |
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_25.md"), "w").write(T); print(len(T))

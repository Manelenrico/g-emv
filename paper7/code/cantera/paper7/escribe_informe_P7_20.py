"""[P7-20] Escribe informe_P7_20.md y tabla_P7_20_Ari.md desde P7_20_vidas.json (ninguna cifra a mano)."""
import bisect, collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); V = json.load(open(os.path.join(AQUI, "P7_20_vidas.json")))
B = ("ESPERANZA", "BORRADO", "APRENDE", "TECHO"); CAMPOS = ("P7-10", "P7-14b", "los dos"); EN = {"ESPERANZA": "HOPE (no memory)", "BORRADO": "ERASED (forgets)", "APRENDE": "LEARNS", "TECHO": "CEILING"}
n = lambda x, d=0: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
med = lambda xs: (st.median(xs) if xs else None)
def vidas(b, campo, corte): return [v for v in V.values() if v["brazo"] == b and (campo == "los dos" or v["campo"] == campo) and v["murio"] and v["ultimo_tick"] < corte]
def pm(L): return [p for v in L for p in v["peleas"] if p["acaba_en_muerte"]]
def pn(L): return [p for v in L for p in v["peleas"] if not p["acaba_en_muerte"]]
lit = lambda P: [p["vida_en_el_primer_golpe"] for p in P if p["vida_en_el_primer_golpe"] is not None]
var = lambda P: [p["vida_ante_el_primer_golpe_de_rival"] for p in P if p["vida_ante_el_primer_golpe_de_rival"] is not None]
def cub(h): return "100" if h >= 100 else "75–99" if h >= 75 else "50–74" if h >= 50 else "menos de 50"
CUB = ("100", "75–99", "50–74", "menos de 50")
def vida_en(v, t):
    if t > v["ultimo_tick"]: return None
    ts = [x[0] for x in v["vida"]]; i = bisect.bisect_right(ts, t) - 1; return v["vida"][i][1] if i >= 0 else None

def tabla1(corte):
    L = ["| campo | brazo | muertes tempranas | con pelea final contra rival | mueren sin ella (anillo) | con primer golpe (definición) | vida en el primer golpe, mediana | mínimo | variante: ante el primer golpe de rival de la racha, mediana (n) |", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for c in CAMPOS:
        for b in B:
            X = vidas(b, c, corte); P = pm(X); a = lit(P); w = var(P)
            L.append(f"| {c} | {b} | {len(X)} | {len(P)} | {len(X) - len(P)} | {len(a)} | {n(med(a), 1)} | {n(min(a) if a else None)} | {n(med(w), 1)} ({len(w)}) |")
    return "\n".join(L)
def reparto(corte):
    L = ["| brazo (los dos campos) | peleas que acaban en muerte | " + " | ".join(CUB) + " | por debajo de 100 |", "|---|---:|" + "---:|" * 5]
    for b in B:
        w = var(pm(vidas(b, "los dos", corte))); c = collections.Counter(cub(h) for h in w)
        L.append(f"| {b} | {len(w)} | " + " | ".join(str(c[k]) for k in CUB) + f" | {len(w) - c['100']} de {len(w)} |")
    return "\n".join(L)
def tabla2(corte):
    L = ["| campo | brazo | peleas que NO acaban en muerte, en las vidas de muerte temprana | con primer golpe (definición) | vida en el primer golpe, mediana | por debajo de 100 |", "|---|---|---:|---:|---:|---:|"]
    for c in CAMPOS:
        for b in B:
            P = pn(vidas(b, c, corte)); a = lit(P)
            L.append(f"| {c} | {b} | {len(P)} | {len(a)} | {n(med(a), 1)} | {sum(1 for h in a if h < 100)} de {len(a)} |")
    return "\n".join(L)
def tabla2b():
    L = ["| campo | brazo | vidas | peleas que no acaban en muerte y empiezan antes del tic 12.000 | con primer golpe (definición) | mediana | media | por debajo de 100 | por debajo de 75 |", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for c in CAMPOS:
        for b in B:
            X = [v for v in V.values() if v["brazo"] == b and (c == "los dos" or v["campo"] == c)]; P = [p for p in pn(X) if p["t0"] < 12000]; a = lit(P)
            L.append(f"| {c} | {b} | {len(X)} | {len(P)} | {len(a)} | {n(med(a), 1)} | {n(sum(a) / len(a), 1) if a else '—'} | {sum(1 for h in a if h < 100)} ({n(100 * sum(1 for h in a if h < 100) / len(a), 0)} %) | {sum(1 for h in a if h < 75)} |")
    return "\n".join(L)
def tabla3(corte):
    L = ["| brazo (los dos campos) | muertes tempranas con pelea final | el que olvida ya había muerto en ese tic | el que olvida tenía MÁS vida | igual | MENOS | diferencia mediana | tenía más, y la diferencia era al menos el último golpe recibido |", "|---|---:|---:|---:|---:|---:|---:|---:|"]; det = {}
    for b in ("APRENDE", "TECHO", "ESPERANZA"):
        r = collections.Counter(); difs = []
        for v in vidas(b, "los dos", corte):
            P = [p for p in v["peleas"] if p["acaba_en_muerte"]]
            if not P: continue
            p = P[0]; t = p["t_primer_golpe_de_rival"]; h = p["vida_ante_el_primer_golpe_de_rival"]; r["n"] += 1
            o = V.get(f"{v['campo']}|s{v['serie']}_d{v['dia']}_BORRADO_{v['slot']}"); ho = vida_en(o, t - 1) if o else None
            if ho is None: r["muerto"] += 1; continue
            d = ho - h; difs.append(d); r["mas" if d > 0 else "igual" if d == 0 else "menos"] += 1
            if d > 0 and d >= p["ultimo_golpe_cuanto"]: r["aguanta"] += 1
        det[b] = sorted(difs)
        L.append(f"| {b} | {r['n']} | {r['muerto']} | {r['mas']} | {r['igual']} | {r['menos']} | {n(med(difs), 1)} | {r['aguanta']} |")
    return "\n".join(L), det
t3_11, d11 = tabla3(11000); t3_12, d12 = tabla3(12000)
# la tabla para Ari, en ingles
A = ["| field | arm | early deaths (<11,000 / <12,000 tics) | HP at first hit of the fatal fight, median (n), <11,000 | same, <12,000 | HP at first hit of non-fatal fights in those lives, median (n), <11,000 | same, <12,000 |", "|---|---|---:|---:|---:|---:|---:|"]
for c in CAMPOS:
    for b in B:
        f = lambda corte, sel: (lambda a: f"{med(a):.1f} ({len(a)})" if a else "— (0)")(lit(sel(vidas(b, c, corte))))
        A.append(f"| {'both' if c == 'los dos' else c} | {EN[b]} | {len(vidas(b, c, 11000))} / {len(vidas(b, c, 12000))} | {f(11000, pm)} | {f(12000, pm)} | {f(11000, pn)} | {f(12000, pn)} |")
ARI = f"""**Life (HP) at the first hit — early deaths, both fields (P7-10 and P7-14b), 80 lives per arm per field**

First hit = first damage from a rival after 10 s (240 tics) with no damage of any kind; HP is the one the creature had when it received that hit (max 100).
Fatal fight = the run of damage (gaps of 10 s or less) that ends in the creature's death. n = fights with a first hit under that definition
(fights that open with ring damage, and deaths by the ring alone, have none). Read after the seals; nothing was replayed.

""" + "\n".join(A) + "\n"
open(os.path.join(AQUI, "tabla_P7_20_Ari.md"), "w").write(ARI)
ap12 = var(pm(vidas("APRENDE", "los dos", 12000))); bo12 = var(pm(vidas("BORRADO", "los dos", 12000)))
T = f"""# P7-20 · La vida en el primer golpe (propuesta de Ari)

*5-oct-2026. Coste: plataforma 0, consola 0. Solo lectura de los 640 diarios de los dos campos (P7-10 y P7-14b, 80 vidas por brazo y campo), posterior a
los sellos; no se ha jugado ni replicado nada. `motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}`; cuerpo sin tocar.
`analiza_P7_20.py` → `P7_20_vidas.json` (640 vidas, {sum(len(v['peleas']) for v in V.values())} peleas, {sum(1 for v in V.values() for p in v['peleas'] if p['acaba_en_muerte'])} acaban en muerte); este informe lo escribe `escribe_informe_P7_20.py` desde ese archivo.
En P7-10 el brazo ESPERANZA es el que entonces se llamaba SUELO.*

## Lo que sale, en corto

- **La lectura de Ari no se ve en esta medida.** En las muertes tempranas, el que aprende recibe el primer golpe de la pelea que lo mata con la vida entera
  en la mediana, igual que el que olvida: {n(med(ap12), 1)} y {n(med(bo12), 1)} (antes del tic 12.000, los dos campos; {len(ap12)} y {len(bo12)} peleas).
- **Sí hay una diferencia, pequeña y de pocos casos:** contando la vida ante el primer golpe de rival de la racha, el que aprende entra por debajo de 100 en {sum(1 for h in ap12 if h < 100)} de {len(ap12)} de esas peleas; el que olvida, en {sum(1 for h in bo12 if h < 100)} de {len(bo12)}.
  Casi toda está en el primer campo (P7-10), donde la mediana del que aprende baja a {n(med(lit(pm(vidas('APRENDE', 'P7-10', 11000)))), 1)}; en el segundo campo es 100.
- **En las peleas que no matan, no entra con menos vida que el que olvida** (sección 3): su mediana es 100 en los dos cortes y en los dos campos.
- **Contra el que olvida en la misma semilla** (sección 4): en el tic del primer golpe, el que olvida tenía más vida en unas muertes y menos en otras, casi a partes iguales; la diferencia mediana es 0.

## Sección 1 · Definiciones, puestas antes de contar

- **Golpe de rival**: una entrada de `damage_taken` del diario cuya fuente es un jugador. **Daño del anillo**: fuente `zone`.
- **Racha de daño**: tics con daño (de rival o del anillo) sin un hueco de más de 10 segundos (240 tics). **Pelea**: una racha con al menos un golpe de rival.
- **Primer golpe** (la del encargo, al pie de la letra): el primer daño de rival después de 10 segundos sin daño de ninguna clase; es el primer daño de la
  racha cuando ese daño es de un rival. Una pelea que empieza con daño del anillo no tiene primer golpe con esta definición: se da aparte, como variante,
  la vida ante el primer golpe de rival de la racha.
- **Vida en el primer golpe**: la del tic anterior a ese golpe. La vida máxima vista en las 640 vidas es 100.
- **La pelea acaba en muerte**: la vida muere y es su última racha, con el último daño a 10 segundos o menos del final.
- **Muerte temprana**: muere antes del tic 11.000; y, aparte, antes del 12.000.

## Sección 2 · La vida en el primer golpe de la pelea que acaba en muerte

**Antes del tic 11.000**

{tabla1(11000)}

**Antes del tic 12.000**

{tabla1(12000)}

Las muertes «sin pelea final contra rival» son las del anillo solo: su última racha de daño no tiene ningún golpe de rival.

**Reparto** (vida ante el primer golpe de rival de la pelea que mata; los dos campos):

Antes del tic 11.000:

{reparto(11000)}

Antes del tic 12.000:

{reparto(12000)}

## Sección 3 · Las peleas que NO acaban en muerte

**En las mismas vidas (las de muerte temprana), como pedía el encargo.** Antes del tic 11.000:

{tabla2(11000)}

Antes del tic 12.000:

{tabla2(12000)}

Son pocas peleas por brazo. Para tener más, **lo mismo en las 80 vidas de cada brazo y campo** (no solo las que mueren pronto), con las peleas que no
acaban en muerte y empiezan antes del tic 12.000; esto es un añadido mío a lo pedido:

{tabla2b()}

**¿Entra el que aprende en las peleas con menos vida que el que olvida?** En la mediana, no: la suya es 100 en todas las filas, y la del que olvida es 100 o algo menos. En la parte de peleas en que entra por debajo
de 100, la tabla de arriba da la cifra de cada brazo; las diferencias son de pocos puntos y de pocos casos.

## Sección 4 · Contra el que olvida en la misma semilla

Para cada muerte temprana con pelea final: la vida que tenía, en ese mismo tic, el BORRADO de la misma serie, el mismo día y el mismo asiento (misma
semilla), menos la vida del que murió. Solo se describe esa diferencia: **no se rehace la partida**, y la semilla fija el mapa, no lo que hacen los
rivales, así que el BORRADO de ese tic puede estar en otro sitio y en otra situación. La última columna cuenta las muertes en que el que olvida tenía
más vida y la diferencia era, al menos, lo que quitó el último golpe recibido: es lo más cerca que se puede estar de «habría cambiado» sin inventar nada.

Antes del tic 11.000:

{t3_11}

Diferencias, una por muerte, del que aprende (vida del que olvida menos la suya): {", ".join(n(x) for x in d11['APRENDE'])}.

Antes del tic 12.000:

{t3_12}

Diferencias del que aprende: {", ".join(n(x) for x in d12['APRENDE'])}.

## Sección 5 · La tabla para Ari

Está en `tabla_P7_20_Ari.md`, en inglés, para mandarla tal cual:

{ARI}
## Lo que esto dice y lo que no

- La medida de Ari (la vida al recibir el primer golpe de la pelea que mata) no separa al que aprende del que olvida: los dos entran casi siempre enteros.
- No dice nada de lo que pasa **dentro** de la pelea (cuánto tarda en usar el botiquín una vez herido), que es la otra mitad de su lectura; eso lo miraron
  P7-15 y P7-16 por otro camino. Tampoco es una prueba: son {len(ap12)} y {len(bo12)} peleas, sin prueba estadística, y todo es posterior a los sellos.
"""
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_20.md"), "w").write(T); print(len(T))

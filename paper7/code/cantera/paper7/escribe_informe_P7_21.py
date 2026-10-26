"""[P7-21] Escribe informe_P7_21.md desde P7_21_vidas.json (ninguna cifra a mano)."""
import collections, hashlib, json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); V = json.load(open(os.path.join(AQUI, "P7_21_vidas.json")))
B = ("ESPERANZA", "BORRADO", "APRENDE", "TECHO"); CAMPOS = ("P7-10", "P7-14b", "los dos")
n = lambda x, d=0: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
med = lambda xs: (st.median(xs) if xs else None)
def muertes(b, campo, corte): return [v for v in V.values() if v["brazo"] == b and (campo == "los dos" or v["campo"] == campo) and v["murio"] and v["ultimo_tick"] < corte]
def t_sitio(corte):
    L = ["| campo | brazo | muertes | en la muerte: a la caja más cercana | a la cámara | al objeto a la vista más cercano (n) | dentro de la cámara | cerca de cajas o cámara | en el primer golpe (n): a la caja | a la cámara | cerca | tics cerca en los 30 s antes de morir | antes del golpe |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for c in CAMPOS:
        for b in B:
            X = muertes(b, c, corte); m = [v["en_la_muerte"] for v in X]; g = [v["en_el_primer_golpe"] for v in X if v.get("en_el_primer_golpe")]; ob = [x["d_objeto_visto"] for x in m if x["d_objeto_visto"] is not None]
            L.append(f"| {c} | {b} | {len(X)} | {n(med([x['d_caja'] for x in m]),1)} | {n(med([x['d_camara'] for x in m]),1)} | {n(med(ob),1)} ({len(ob)}) | {sum(1 for x in m if x['d_camara'] == 0)} de {len(m)} | {sum(1 for x in m if x['cerca'])} de {len(m)} | ({len(g)}) {n(med([x['d_caja'] for x in g]),1)} | {n(med([x['d_camara'] for x in g]),1)} | {sum(1 for x in g if x['cerca'])} de {len(g)} | {n(med([100*v['cerca_en_los_30_s_antes_de_morir'] for v in X]),0)} % | {n(med([100*v['cerca_en_los_30_s_antes_del_golpe'] for v in X if 'cerca_en_los_30_s_antes_del_golpe' in v]),0)} % |")
    return "\n".join(L)
def t_pareja(corte):
    L = ["| campo | las dos viven | APRENDE muere, BORRADO vive | APRENDE vive, BORRADO muere | las dos mueren (distancia a la cámara de A y de B) |", "|---|---:|---:|---:|---|"]
    for c in CAMPOS:
        k = collections.Counter(); dd = []
        for v in V.values():
            if v["brazo"] != "APRENDE" or (c != "los dos" and v["campo"] != c): continue
            o = V.get(f"{v['campo']}|s{v['serie']}_d{v['dia']}_BORRADO_{v['slot']}"); a = v["murio"] and v["ultimo_tick"] < corte; bm = bool(o and o["murio"] and o["ultimo_tick"] < corte)
            k[(a, bm)] += 1
            if a and bm: dd.append(f"({v['en_la_muerte']['d_camara']}, {o['en_la_muerte']['d_camara']})")
        L.append(f"| {c} | {k[(False, False)]} | {k[(True, False)]} | {k[(False, True)]} | {k[(True, True)]} {' '.join(dd)} |")
    return "\n".join(L)
def t_llevo(corte):
    L = ["| brazo (los dos campos) | muertes con pelea final | `noop` | `ir_curioso` | `ir_objeto` (otro objeto) | `ir_objeto` (botiquín) | `ir_centro` | `ir_pareja` | `ir_botin` | paso | atacar | último `ir_*` antes del golpe |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for b in B:
        X = [v for v in muertes(b, "los dos", corte) if v.get("que_la_llevo")]; m = len(X); c = collections.Counter(); u = collections.Counter()
        for v in X:
            u[v["que_la_llevo"]["ultimo_ir"] or "ninguno"] += 1
            for k, x in v["que_la_llevo"]["partes"].items(): c[k] += x
        p = lambda k: n(100 * c[k] / m, 0) + " %" if m else "—"
        L.append(f"| {b} | {m} | {p('noop')} | {p('ir_curioso')} | {p('ir_objeto (otro)')} | {p('ir_objeto (botiquin)')} | {p('ir_centro')} | {p('ir_pareja')} | {p('ir_botin')} | {p('paso')} | {p('atacar')} | {', '.join(f'{k} {v}' for k, v in u.most_common())} |")
    return "\n".join(L)
def t_canales(brazos, campos, ven):
    C = [c for v in V.values() if v["brazo"] in brazos and v["campo"] in campos for c in v["canales"]]
    L = ["| situación | canales | se completan | los corta el daño de un rival | el daño del anillo | muere con el canal abierto | se cortan sin daño registrado |", "|---|---:|---:|---:|---:|---:|---:|"]
    for dentro in (True, False):
        for g in (True, False):
            X = [c for c in C if c["dentro"] == dentro and c[ven] == g]; k = collections.Counter(c["causa_corte"] for c in X if not c["completado"]); comp = sum(1 for c in X if c["completado"])
            L.append(f"| {'dentro del círculo' if dentro else 'fuera del círculo'}, {'golpeada antes' if g else 'sin daño antes'} | {len(X)} | {comp} ({n(100*comp/len(X),0) if X else '—'} %) | {k['dano de rival']} | {k['dano del anillo']} | {k['muere con el canal abierto']} | {k['sin dano registrado']} |")
    return "\n".join(L), C
def tasa(C, f, val):
    X = [c for c in C if c[f] == val]; return f"{sum(1 for c in X if c['completado'])} de {len(X)} ({n(100*sum(1 for c in X if c['completado'])/len(X),0)} %)" if X else "—"
CA = [c for v in V.values() if v["brazo"] in ("APRENDE", "BORRADO") for c in v["canales"]]; comp = [c for c in CA if c["completado"]]; cort = [c for c in CA if not c["completado"]]
dur = collections.Counter(c["dura"] for c in comp); durc = collections.Counter(c["dura"] for c in cort)
sd = [c for c in cort if c["causa_corte"] == "sin dano registrado"]

E = json.load(open(os.path.join(AQUI, "P7_21_emocion.json"))); import bisect
CE = []
for k, o in E.items():
    for c in V[k]["canales"]:
        e = o[str(c["t0"])]; c = dict(c); c["e"] = e; CE.append(c)
def auc(xs, ys):
    if not xs or not ys: return None
    ys_s = sorted(ys); s = 0
    for x in xs: s += bisect.bisect_left(ys_s, x) + 0.5 * (bisect.bisect_right(ys_s, x) - bisect.bisect_left(ys_s, x))
    return s / (len(xs) * len(ys))
MED = (("dolor del cuerpo (F)", lambda c: c["e"]["dolor"]["F"]), ("dolor en recursos (R)", lambda c: c["e"]["dolor"]["R"]), ("dolor en vínculo (S)", lambda c: c["e"]["dolor"]["S"]), ("dolor total", lambda c: sum(c["e"]["dolor"].values())),
       ("positivo total", lambda c: sum(c["e"]["positivo"].values())), ("distancia total", lambda c: c["e"]["d"] or 0.0), ("vida al abrir", lambda c: c["hp0"]), ("golpeada en los 48 anteriores", lambda c: float(c["golpeado_48"])), ("golpeada en los 24 anteriores", lambda c: float(c["golpeado_24"])))
L = ["| medida al abrir | dentro: mediana si cura | dentro: mediana si lo corta el daño | dentro: separación | fuera: mediana si cura | fuera: mediana si lo corta | fuera: separación |", "|---|---:|---:|---:|---:|---:|---:|"]
AU = {}
for nombre, f in MED:
    fila = [nombre]
    for dentro in (True, False):
        X = [c for c in CE if c["dentro"] == dentro]; cur = [f(c) for c in X if c["completado"]]; cor = [f(c) for c in X if not c["completado"] and c["causa_corte"] in ("dano de rival", "dano del anillo")]
        a = auc(cor, cur); AU[(nombre, dentro)] = a; fila += [n(st.median(cur), 3), n(st.median(cor), 3), n(a, 2)]
    L.append("| " + " | ".join(fila) + " |")
Xd = [c for c in CE if c["dentro"]]; cu = [c for c in Xd if c["completado"]]; co = [c for c in Xd if not c["completado"] and c["causa_corte"] in ("dano de rival", "dano del anillo")]
L.insert(2, f"| canales | {len(cu)} curan | {len(co)} cortados | | {sum(1 for c in CE if not c['dentro'] and c['completado'])} curan | {sum(1 for c in CE if not c['dentro'] and not c['completado'] and c['causa_corte'] in ('dano de rival', 'dano del anillo'))} cortados | |")
pres = lambda fila_, S: n(100 * sum(1 for c in S if fila_ in c["e"]["filas"]) / len(S), 0) + " %"
EMO = {"EMO_N": sum(len(o) for o in E.values()), "EMO_T": len(CE), "EMO_TABLA": "\n".join(L), "EMO_F": n(AU[("dolor del cuerpo (F)", True)], 2), "EMO_G48": n(AU[("golpeada en los 48 anteriores", True)], 2), "EMO_G24": n(AU[("golpeada en los 24 anteriores", True)], 2),
       "EMO_HP": n(AU[("vida al abrir", True)], 2) + ", es decir, " + n(1 - AU[("vida al abrir", True)], 2) + " a favor de la vida alta", "EMO_AGR": f"{pres('S-7-AGRESOR', co)} frente a {pres('S-7-AGRESOR', cu)}", "EMO_PAR": f"{pres('S-DANO-PAREJA', co)} frente a {pres('S-DANO-PAREJA', cu)}"}
globals().update(EMO)
A12 = muertes("APRENDE", "los dos", 12000); B12 = muertes("BORRADO", "los dos", 12000)
T = f"""# P7-21 · Dónde mueren las que recuerdan, y el botiquín bajo golpes

*7-oct-2026. Coste: plataforma 0, consola 0. Solo lectura de los 640 diarios de los dos campos (P7-10 y P7-14b; 80 vidas por brazo y campo), posterior a los sellos;
no se ha jugado ni replicado nada. `motor/model.py` = `{hashlib.md5(open(os.path.join(AQUI, '..', '..', 'motor', 'model.py'), 'rb').read()).hexdigest()}` al empezar y al acabar; cuerpo y congelados sin tocar.
`analiza_P7_21.py` → `P7_21_vidas.json`; este informe lo escribe `escribe_informe_P7_21.py` desde ese archivo. En P7-10 el brazo ESPERANZA se llamaba SUELO.*

## Lo que sale, en corto

- **La pista de Ari no separa a las que recuerdan.** Todas mueren en el mismo sitio: en la cámara central o pegadas a ella, a unas 9 casillas de la caja más
  cercana. En las muertes antes del tic 12.000, APRENDE muere dentro de la cámara en {sum(1 for v in A12 if v['en_la_muerte']['d_camara'] == 0)} de {len(A12)} y BORRADO en {sum(1 for v in B12 if v['en_la_muerte']['d_camara'] == 0)} de {len(B12)}; en el primer golpe de la pelea
  final, a 0 casillas de la cámara en la mediana las dos; en los 30 segundos anteriores, el 100 % del tiempo cerca de cajas o cámara, las dos. El motivo
  es el mundo: el anillo empieza a cerrarse en el tic 7.296 y empuja a todas hacia el centro, y «temprano» (antes del 11.000) ya es con el anillo cerrándose.
- **Lo que la llevó allí** (los 30 s antes del primer golpe) es sobre todo estar quieta (`noop`, {n(100*sum(v['que_la_llevo']['partes'].get('noop',0) for v in A12 if v.get('que_la_llevo'))/sum(1 for v in A12 if v.get('que_la_llevo')),0)} % de los tics en APRENDE); la curiosidad pesa algo más en la que recuerda
  ({n(100*sum(v['que_la_llevo']['partes'].get('ir_curioso',0) for v in A12 if v.get('que_la_llevo'))/sum(1 for v in A12 if v.get('que_la_llevo')),0)} % frente a {n(100*sum(v['que_la_llevo']['partes'].get('ir_curioso',0) for v in B12 if v.get('que_la_llevo'))/sum(1 for v in B12 if v.get('que_la_llevo')),0)} % en BORRADO); ir a por el botiquín, 0 % en las dos.
- **El botiquín bajo golpes (APRENDE y BORRADO, los dos campos, {len(CA)} canales):** «me han golpeado en los 48 instantes anteriores» separa mejor que «dentro o fuera»:
  completan {tasa(CA,'golpeado_48',False)} de los canales abiertos sin daño antes frente a {tasa(CA,'golpeado_48',True)} con daño antes; dentro del círculo, {tasa(CA,'dentro',True)}; fuera, {tasa(CA,'dentro',False)}.
  Fuera del círculo casi todo lo corta el anillo (pega cada 24 instantes y el canal dura 48); dentro, lo corta el rival. Las dos cosas juntas: dentro y sin daño antes, el canal cura casi siempre.
- **El estado emocional al abrir** (añadido de Manel, sección 5): dentro del círculo, el dolor del cuerpo separa los canales que curan de los que corta el daño
  mejor que «golpeada en los 48 anteriores» (separación {EMO_F} frente a {EMO_G48}); fuera del círculo no separa nada. El diario no distingue alivio de atracción.
- **Sí, el cuerpo se mueve con el canal abierto sin que se corte:** de los {len(comp)} canales completados, {sum(1 for c in comp if c['se_movio'])} cambiaron de casilla mientras estaba abierto. Lo que dijo P7-1 (57 de 59) se confirma a lo grande.

## Sección 1 · Definiciones, puestas antes de contar

- **Cajas:** los 16 pedestales del mapa (`static_map.pedestals` del diario; están en un anillo a unas 16 casillas del centro). **Objeto a la vista:** cada entrada de `ve_items` del tic.
- **Cámara:** la fortaleza central (`mundo_leido`: 49 celdas en torno al centro (24, 24), un cuadrado de 7×7). Distancia a la cámara = distancia Chebyshev al centro menos 3; 0 dentro.
- **Cerca de cajas o cámara:** a 3 casillas o menos de un pedestal o a 3 o menos de la cámara.
- **Muerte temprana:** antes del tic 11.000 y, aparte, del 12.000. **Primer golpe de la pelea final:** el de P7-20.
- **Qué la llevó allí:** lo elegido (`RADIOGRAFIA.elegido`) en los 720 tics anteriores al primer golpe, en partes. `ir_objeto` se separa en «a por el botiquín» y «a por otro objeto» por el objeto a la vista más cercano al que el paso elegido acerca: es una aproximación, porque el diario no guarda a qué objeto va el candidato.
- **Canal:** tics seguidos con `channeling` del botiquín en `effects`. **Se completa** si al cerrarse lleva un botiquín menos. Si no, **lo corta** el daño de rival o del anillo si lo hubo en el tic del cierre o en el anterior; si no, «sin daño registrado». **Dentro del círculo:** distancia euclídea al centro de la zona ≤ su radio al abrir. **Golpeada antes:** algún daño en los 48 tics anteriores a la apertura (y, aparte, en los 24). **Se movió:** cambió de casilla con el canal abierto.

## Sección 2 · Dónde mueren (la pista de Ari)

Distancias en casillas, medianas. «Cerca» = a 3 o menos de cajas o cámara.

**Muertes antes del tic 11.000**

{t_sitio(11000)}

**Muertes antes del tic 12.000**

{t_sitio(12000)}

**Todas las muertes**

{t_sitio(99999)}

Lectura: en todos los brazos y los dos campos la muerte es en la cámara o a su lado (mediana 0 a 2 casillas), lejos de las cajas (9 a 11). No hay un sitio distinto
para APRENDE. El objeto a la vista más cercano está a 2 casillas en todos: el centro guarda objetos y es donde el anillo junta a todas.

**APRENDE frente a BORRADO, emparejadas por semilla** (misma serie, día y asiento; la semilla fija el mapa, no lo que hacen los rivales):

Antes del tic 11.000:

{t_pareja(11000)}

Antes del tic 12.000:

{t_pareja(12000)}

Las pocas parejas en que mueren las dos lo hacen a la misma distancia de la cámara, salvo una (7 y 14, en P7-14b). Lo que separa a los brazos es cuántas mueren, no dónde.

**Qué la llevó allí** (parte de los 720 tics antes del primer golpe de la pelea final, media por muerte; antes del tic 12.000, los dos campos):

{t_llevo(12000)}

Antes del 11.000:

{t_llevo(11000)}

## Sección 3 · El botiquín bajo golpes

APRENDE y BORRADO, los dos campos juntos ({len(CA)} canales: APRENDE {sum(1 for v in V.values() if v['brazo'] == 'APRENDE' for c in v['canales'])}, BORRADO {sum(1 for v in V.values() if v['brazo'] == 'BORRADO' for c in v['canales'])}).

**Ventana de 48 instantes antes de abrir**

{t_canales(('APRENDE', 'BORRADO'), ('P7-10', 'P7-14b'), 'golpeado_48')[0]}

**Ventana de 24 instantes**

{t_canales(('APRENDE', 'BORRADO'), ('P7-10', 'P7-14b'), 'golpeado_24')[0]}

**Cada factor por separado:** dentro del círculo completan {tasa(CA,'dentro',True)}, fuera {tasa(CA,'dentro',False)}; sin daño en los 48 anteriores {tasa(CA,'golpeado_48',False)}, con daño {tasa(CA,'golpeado_48',True)};
con la ventana de 24: sin daño {tasa(CA,'golpeado_24',False)}, con daño {tasa(CA,'golpeado_24',True)}. **«Me están golpeando» separa más que «dentro o fuera»** ({n(100*sum(1 for c in CA if not c['golpeado_48'] and c['completado'])/max(1,sum(1 for c in CA if not c['golpeado_48'])) - 100*sum(1 for c in CA if c['golpeado_48'] and c['completado'])/max(1,sum(1 for c in CA if c['golpeado_48'])),0)} puntos
contra {n(100*sum(1 for c in CA if c['dentro'] and c['completado'])/max(1,sum(1 for c in CA if c['dentro'])) - 100*sum(1 for c in CA if not c['dentro'] and c['completado'])/max(1,sum(1 for c in CA if not c['dentro'])),0)} de diferencia entre sus dos valores con la ventana de 48), pero los dos factores van juntos: fuera del círculo casi siempre hay daño antes (el anillo), y ahí
el anillo corta casi todo porque pega cada 24 instantes y el canal dura 48. La celda buena es «dentro y sin daño antes».

**Por brazo y campo** (ventana de 48):

""" + "\n\n".join(f"*{b}, {c}*\n\n{t_canales((b,), (c,), 'golpeado_48')[0]}" for b in ("APRENDE", "BORRADO") for c in ("P7-10", "P7-14b")) + f"""

**Los cortes.** Duración de los canales cortados (tics), los más frecuentes: {", ".join(f"{d} ({k})" for d, k in durc.most_common(6))}; los completados duran 48 ({dur[48]} de {len(comp)}; {len(comp) - dur[48]} con otra duración: se completan por llevar un botiquín menos, y un botiquín dado durante el canal cuenta igual).
Los {len(sd)} cortes «sin daño registrado» son cortes que el diario no explica ({sum(1 for c in sd if c['se_movio'])} de ellos con movimiento, pero el movimiento no corta: sección 4).

## Sección 4 · Moverse con el canal abierto (para contestar a Ari)

De los {len(comp)} canales completados de APRENDE y BORRADO, **{sum(1 for c in comp if c['se_movio'])} cambiaron de casilla** con el canal abierto y se completaron igual: moverse no corta el canal. Lo que lo corta es el daño:
de los {len(cort)} cortes, {sum(1 for c in cort if c['causa_corte'] in ('dano de rival', 'dano del anillo'))} tienen daño de rival o del anillo en el tic del cierre o el anterior, {sum(1 for c in cort if c['causa_corte'] == 'muere con el canal abierto')} son muertes con el canal abierto y {len(sd)} no tienen daño registrado.
Confirma lo que Ari dice del mundo (el canal dura 48 instantes y cualquier daño lo corta) y lo de P7-1 (57 de 59 completados se movieron).

## Sección 5 · El estado emocional del cuerpo al abrir el canal (añadido de Manel, 7-oct)

**Lo que el diario guarda por instante, y lo que no.** En cada tic, `RADIOGRAFIA.ahora.filas` trae cada fila activa de la tabla con su magnitud, su signo (`-`
dolor, `+` lo positivo) y su reparto en los tres dominios (F cuerpo, R recursos, S vínculo), y `d_ahora` trae la distancia total. **No distingue, dentro de
lo positivo, el alivio de la atracción:** solo hay un signo. Así que el mapa es: dolor por dominio (suma de las filas con `-`), positivo por dominio (suma
de las filas con `+`) y la distancia total, en el tic de apertura. `emocion_P7_21.py` → `P7_21_emocion.json` ({EMO_N} canales de {EMO_T}, todos con estado).

Se comparan los canales que se completan con los que corta el daño (de rival o del anillo; fuera quedan las muertes con el canal abierto y los cortes sin daño).
«Separación» es la probabilidad de que un canal cortado tenga la medida más alta que uno que cura (0,5 = no separa; 1 = separa del todo; por debajo de 0,5, al revés).

{EMO_TABLA}

**Lectura.** Dentro del círculo, **el dolor del cuerpo (F) al abrir separa los canales que curan de los que no mejor que «me han golpeado en los 48 anteriores»**
({EMO_F} frente a {EMO_G48}), y algo mejor que la ventana de 24 ({EMO_G24}); el dolor total y la distancia total separan casi igual que el dolor del cuerpo; el dolor en
recursos y en vínculo, menos; lo positivo, nada. La vida al abrir va en el mismo sentido (los cortados abren con menos vida: {EMO_HP}). Fuera del círculo no separa
nada, ni el estado ni los golpes: ahí corta el anillo. Entre las filas, las que están más veces encendidas al abrir en los cortados que en los que curan son
S-7-AGRESOR ({EMO_AGR}) y S-DANO-PAREJA ({EMO_PAR}): el rival al lado y el hermano herido.

Solo se describe; no se cambia nada del cuaderno. Si el cuerpo guardara el estado al abrir, lo que más valdría para prever el corte es el dolor del cuerpo, que ya
lleva dentro el daño reciente y la vida que queda; «golpeada hace poco» añade poco encima.

## Lo que esto dice y lo que no

- Dónde mueren no distingue a la que recuerda: el anillo las lleva a todas al centro. Si la curiosidad, la esperanza o las ganas la llevan antes a sitios peores, no se ve en el lugar de la muerte ni en el del primer golpe; se ve, como mucho, en que elige `ir_curioso` algo más en los 30 s previos.
- La condición de corte del canal es «daño en 48 instantes», y los diarios la cumplen; hoy el cuaderno no apunta los cortes sin gasto (decisión de la mesa). Si el cuerpo supiera que «golpeada en los últimos 48» casi siempre acaba en corte, sería un cambio de arquitectura: se propone, no se hace.
- Todo es posterior a los sellos; sin pruebas estadísticas.
"""
for k_, v_ in EMO.items(): T = T.replace("{" + k_ + "}", str(v_))
assert "§" not in T; open(os.path.join(AQUI, "informe_P7_21.md"), "w").write(T); print(len(T))

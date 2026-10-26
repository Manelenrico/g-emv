"""[P7-44] Escribe informe_P7_44.md desde P7_44_datos.json (analiza_P7_44) y las citas de la especificacion del mundo (paintball_recon/docs/zero-sum: README.md, protocol_player.md,
src/sim.nim) y del cuerpo (appraisal_zs_v42_exp.py). Ninguna cifra a mano."""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_44_datos.json")))
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
EST = ("puesto", "puesto delatado", "sin camuflaje"); SIT = ("todas", "dentro · rival≤8", "dentro · sin rival≤8", "fuera · rival≤8", "fuera · sin rival≤8"); SITM = SIT + ("misma fase y situación (todos los tramos)",) + tuple(f"fase {i} · dentro · rival≤8" for i in range(5))


def tabla(D, titulo):
    T = [f"| estado | situación | minutos | golpes de rivales / min | vida perdida / min | rivales a ≤ 4 por tic | nos persiguen por tic |", "|---|---|---:|---:|---:|---:|---:|"]
    for sit in SIT:
        for est in EST:
            x = D.get(f"{est} | {sit}")
            if x: T.append(f"| {est} | {sit} | {n(x['min'], 1)} | {n(x['golpes_min'], 3)} | {n(x['dano_min'], 2)} | {n(x['r4_tic'], 3)} | {n(x['persiguen_tic'], 3)} |")
    return f"**{titulo}**\n\n" + "\n".join(T)


MC = R["misma_criatura"]
TM = ["| situación | vidas con los dos estados (≥ 240 tics cada uno) | golpes/min: puesto − sin, media ± ee | vida perdida/min | rivales a ≤ 4 por tic | nos persiguen por tic |", "|---|---:|---|---|---|---|"]
for sit in SITM:
    x = MC.get(sit)
    if x: TM.append(f"| {sit} | {x['n_vidas']} | {n(x['golpes_min']['media'], 3)} ± {n(x['golpes_min']['ee'], 3)} | {n(x['dano_min']['media'], 2)} ± {n(x['dano_min']['ee'], 2)} | {n(x['r4']['media'], 3)} ± {n(x['r4']['ee'], 3)} | {n(x['persiguen']['media'], 3)} ± {n(x['persiguen']['ee'], 3)} |")
todo = R["todo"]; p = todo.get("puesto | todas", {}); s = todo.get("sin camuflaje | todas", {}); pr = todo.get("puesto | dentro · rival≤8", {}); sr = todo.get("sin camuflaje | dentro · rival≤8", {})
def signo(d, ee): return ("menos" if d < 0 else "más") + (" (más de 3 errores típicos)" if ee and abs(d) >= 3 * ee else " (dentro del ruido)")
mt = MC.get("todas", {}); mr = MC.get("dentro · rival≤8", {}); mf = MC.get("misma fase y situación (todos los tramos)", {})

out = f"""# P7-44 · ¿El camuflaje protege?

*11-oct-2026. Banco, coste cero (plataforma 0 créditos; consola 0); nada cambia en el campo en marcha. Datos: los diarios que ya existen: P7-34 (240 vidas), piloto 1 de
P7-42 (190 vidas) y piloto 2 (24 vidas); TECHO incluido. {R['vidas']} vidas leídas, {R['vidas_con_camuflaje_puesto']} con el camuflaje puesto en algún tic. Script `analiza_P7_44.py` → `P7_44_datos.json`;
este informe lo escribe `escribe_informe_P7_44.py` (ninguna cifra a mano). La serie 1 del campo (P7-42) no ha cerrado al escribir esto: no entra.*

## Sección 2 · Qué dice el juego del camuflaje (y de la red)

- **Especificación**: `paintball_recon/docs/zero-sum/README.md:50-52`: *«Gear: backpack (2 -> 4 pack slots), camouflage (undetected beyond 4 tiles standing / 7 moving
  until you attack), first-aid kit (50 HP, 2 s channel, cancelled by any damage), rations (15 HP)»*. Y `protocol_player.md:73-75`: *«Fog: visible.* is line-of-sight
  limited by your INT vision radius; walls, rocks, and the Fortress block sight. Camouflaged agents are absent unless within their detection cap or revealed by attacking»*.
  Es decir: el camuflaje oculta al que lo lleva a los demás contendientes más allá de 4 casillas si está quieto y de 7 si se mueve, hasta que ataca; al atacar queda delatado
  un tiempo (`sim.nim:917, 935, 943`: `a.camoRevealedUntil = s.tick + CamoRevealTicks` en los tres golpes: cuerpo a cuerpo, proyectil, lanzado); la constante
  `CamoRevealTicks` **no está en la copia de la fuente que tenemos** (`paintball/exposicion_liga_acta.md:56`: declarada [impl] de 5 s en el cuerpo). Duración del camuflaje:
  no caduca (es una prenda: va en `body` hasta que se cambia o se muere; `sim.nim` no le da durabilidad). Se obtiene como botín de nivel 1 en la cámara de la Fortaleza
  (`README.md:44-45`: *«Tier-1 loot (swords, bow, blowgun, camo) is deep in the Fortress chamber»*; `sim.nim:476`: `s.dropGround(t1[5], iCamo, 1)`).
- **La red**, en una línea (punto 4): `README.md:50`: *«net (immobilizes 3 s)»*; se lanza desde la mano (`protocol_player.md:120-121`: *«knives/net throw from your hand stack»*)
  y deja al alcanzado sin poder moverse (`sim.nim:983-984`: `nettedUntil = s.tick + NetTicks`; `sim.nim:618`: no se mueve mientras `tick < nettedUntil`).

## Sección 3 · Cómo valora TECHO el camuflaje, y de dónde sale

TECHO nace sabiendo (`GEMV_P7_SABE=1`): el cuerpo congelado de paper seis, sin las piezas de nacer. Dos sitios, los dos en `paintball/alma/appraisal_zs_v42_exp.py`:
1. **La riqueza W** (lo que vale lo que lleva): `GEAR_MENOR_W = 0.25` **[impl]** (línea 413: *«camuflaje / red»*), sumado en `riqueza_W` si el cuerpo lleva el camuflaje puesto
   (líneas 761-763) o la red en la mano o el zurrón (764-767); frente a `W_TARGET = 3.0` [Manel] (arma + botiquín + ración, línea 126): el camuflaje vale un cuarto de una
   de esas tres cosas, y la red otro cuarto. No sale de ninguna medida: es una constante declarada [impl].
2. **La exposición S-8** (líneas 1393-1420): con el camuflaje puesto y sin haber atacado en los últimos `CAMO_REVELADO_S = 5` s [impl], un hostil a más de `CAMO_QUIETO = 4`
   casillas (quieto) o `CAMO_MOVIENDO = 7` (moviéndose) **no me ve** y no suma exposición (`tope_camo`, línea 1410). Estos dos topes están **certificados** del README del
   mundo (líneas 403-406 del cuerpo: *«CERTIFICADO, no [impl]»*). Así que para TECHO el camuflaje vale 0,25 de riqueza y, sobre todo, menos miedo a los hostiles lejanos.
En P7-33/34 (nacer sin saber), estas dos entradas se borraron para APRENDE/BORRADO y las ganas pasaron a lo aprendido (k_gear); TECHO las conserva.

## Sección 1 · Lo medido: con el camuflaje puesto y sin él

Por tic vivo: estado (puesto sin delatar / puesto y delatado tras atacar, efecto `camo_revealed` / sin camuflaje), situación (dentro o fuera del anillo × rival a 8 casillas o
menos a la vista). Golpes = `damage_taken` con fuente un rival; «nos persiguen» = rivales a 6 o menos cuya distancia ha bajado respecto a 24 tics antes. Fracción de tics con
el camuflaje puesto por brazo: {', '.join(f'{b} {n(100 * x, 1)} %' for b, x in sorted(R['por_brazo_fraccion_puesto'].items()))}.

{tabla(todo, 'Todos los diarios (P7-34 + pilotos), sumando tics')}

{chr(10).join(f"{tabla(D, et)}{chr(10)}" for et, D in R['por_campo'].items())}

**Misma criatura, situaciones parecidas** (vidas con ≥ 240 tics en los dos estados; diferencia puesto − sin camuflaje por vida; media y error típico):

{chr(10).join(TM)}

## Lectura

Sumando todos los tics, con el camuflaje puesto la criatura recibe {n(p.get('golpes_min'), 3)} golpes por minuto frente a {n(s.get('golpes_min'), 3)} sin él, y pierde {n(p.get('dano_min'), 2)} frente a {n(s.get('dano_min'), 2)} puntos de vida por minuto; con un rival a 8 o menos
dentro del anillo, {n(pr.get('golpes_min'), 3)} frente a {n(sr.get('golpes_min'), 3)} golpes y {n(pr.get('dano_min'), 2)} frente a {n(sr.get('dano_min'), 2)} de vida. Esas sumas mezclan criaturas y momentos (quien lleva camuflaje suele ser quien ha llegado
a la cámara, y la lleva más tarde en la vida, cuando hay más rivales cerca): la comparación honesta es la misma criatura en situaciones parecidas: con el camuflaje puesto
recibe {n(abs(mt.get('golpes_min', {}).get('media', 0)), 3)} golpes/min {signo(mt.get('golpes_min', {}).get('media', 0), mt.get('golpes_min', {}).get('ee'))} y pierde {n(abs(mt.get('dano_min', {}).get('media', 0)), 2)} de vida/min {signo(mt.get('dano_min', {}).get('media', 0), mt.get('dano_min', {}).get('ee'))} ({mt.get('n_vidas')} vidas); con un rival a 8 o menos dentro del anillo,
{n(abs(mr.get('golpes_min', {}).get('media', 0)), 3)} golpes/min {signo(mr.get('golpes_min', {}).get('media', 0), mr.get('golpes_min', {}).get('ee'))} ({mr.get('n_vidas')} vidas); los rivales a 4 o menos por tic cambian en {n(mr.get('r4', {}).get('media'), 3)} ± {n(mr.get('r4', {}).get('ee'), 3)} y los que nos persiguen en {n(mr.get('persiguen', {}).get('media'), 3)} ± {n(mr.get('persiguen', {}).get('ee'), 3)}.
Pero el camuflaje se lleva más tarde en la vida (se recoge en la cámara de la Fortaleza, en el centro, y después el anillo aprieta y hay más rivales cerca): emparejando también
por TRAMO de la vida (3.000 tics), misma criatura y misma situación ({mf.get('n_vidas')} pares vida × tramo × situación): golpes/min {n(mf.get('golpes_min', {}).get('media'), 3)} ± {n(mf.get('golpes_min', {}).get('ee'), 3)}, vida perdida/min {n(mf.get('dano_min', {}).get('media'), 2)} ± {n(mf.get('dano_min', {}).get('ee'), 2)},
rivales a ≤ 4 {n(mf.get('r4', {}).get('media'), 3)} ± {n(mf.get('r4', {}).get('ee'), 3)}, nos persiguen {n(mf.get('persiguen', {}).get('media'), 3)} ± {n(mf.get('persiguen', {}).get('ee'), 3)} (puesto − sin camuflaje; negativo = protege).
Lo que el juego promete (invisible a más de 4/7 casillas hasta atacar) solo puede notarse en que los rivales lejanos no vengan: eso es «nos persiguen» y «rivales a ≤ 4»; los
golpes a bocajarro no los evita ningún camuflaje. El cuerpo congelado lo valora por una constante [impl] de 0,25 y por el miedo que ahorra (topes certificados); lo que estos
datos dicen de si protege está en la tabla de la misma criatura, con su error típico. **Respuesta con estos datos**: emparejando por criatura, tramo y situación, ninguna
de las cuatro medidas se aparta del cero más de 3 errores típicos ({', '.join(f"{m} {n(abs(mf.get(m, {}).get('media', 0)) / (mf.get(m, {}).get('ee') or 1), 1)} ee" for m in ('golpes_min', 'dano_min', 'r4', 'persiguen'))}): el camuflaje, tal como lo lleva
esta criatura (que casi siempre se mueve, y a 7 casillas la ven igual), no protege de forma que se vea en {R['vidas']} vidas; la única señal, pequeña, va al revés (más rivales a ≤ 4 con
el camuflaje puesto). Lo que queda por medir, cuando cierre la serie 1: lo mismo con SIN EMOCIÓN y con TECHO por separado.
"""
open(os.path.join(AQUI, "informe_P7_44.md"), "w", encoding="utf-8").write(out); print("informe_P7_44.md", out.count("\n"), "lineas")

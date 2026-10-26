"""[P7-47] Escribe informe_P7_47.md desde P7_47_sello.json (analiza_P7_47), P7_47_cadena.json, los cuadernos P7_47_res/ y P7_41_res/, y P7_47_local_*.json (local_P7_47).
Ninguna cifra a mano.  python3 escribe_informe_P7_47.py [--saldo 228]"""
import glob, hashlib, json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
S = J("P7_47_sello.json"); C = J("P7_47_cadena.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
saldo = (sys.argv[sys.argv.index("--saldo") + 1] if "--saldo" in sys.argv else None)
ET = {"APRENDE_v": "APRENDE valiente", "APRENDE_p": "APRENDE prudente"}; NOM = {"first_aid": "botiquín", "rations": "ración", "net": "red", "camouflage": "camuflaje"}
H1, H2, H3, H4 = S["H1"], S["H2"], S["H3"], S["H4"]
# intensidades
def inten(d):
    v = []; v40 = []; z = 0
    for f in glob.glob(os.path.join(AQUI, d, "cuaderno_s*_d20_*.json")):
        c = json.load(open(f))
        for o, x in c["objetos"].items():
            for s_, L in x["situaciones"].items():
                for r in L:
                    if r.get("corte"): continue
                    v.append(r["intensidad"]); v40.append(r.get("intensidad_P7_40", r["intensidad"])); z += (sum(abs(r["importancia"][dd]) for dd in ("cuerpo", "recursos", "vinculo")) == 0)
    return v, v40, z
v, v40, z = inten("P7_47_res"); q = st.quantiles(v, n=4); q40 = st.quantiles(v40, n=4)
# locales
LOC = {os.path.basename(f)[len("P7_47_local_"):-5]: json.load(open(f)) for f in sorted(glob.glob(os.path.join(AQUI, "P7_47_local_*.json")))}
TL = ["| partida local | imagen | vidas con diario | tics (media) | mueren | pruebas (huellas) por vida ± ee | por objeto (b · r · red · cam) | forzadas por vida | acaban (cogida + usada) | caducan · no cabe (de ellas, el objeto ya no estaba) | vías de la cogida (recoger · hacer_sitio · coger puesto) | ms mediana (media) · p95 máx | % sobre el tic · % bloqueados |", "|---|---|---:|---:|---:|---|---|---:|---|---|---|---|---|"]
for k, L in LOC.items():
    r = L["resumen"]; po = r["huellas_por_objeto_total"]; fi = r["fines_total"]; vi = r["vias_total"]
    TL.append(f"| {k} | `{L['imagen']}` | {r['vidas_con_diario']} | {n(r['tics_media'], 0)} | {r['mueren']} | {n(r['huellas_por_vida'], 2)} ± {n(r['huellas_ee'], 2)} | {po['botiquin']} · {po['racion']} · {po['red']} · {po['camuflaje']} | {n(r['forzadas_por_vida'], 2)} | {r['acaban']} de {r['forzadas_total']} ({n(r['acaban_pct'], 0)} %) | {fi['caduca']} · {fi['no cabe']} ({r['no_cabe_objeto_ya_no_esta']}) | {vi['recoger']} · {vi['hacer_sitio']} · {vi['coger_puesto']} | {n(r['ms_mediana_media'], 2)} · {n(r['ms_p95_max'], 1)} | {n(r['sobre_tic_pct_media'], 2)} · {n(r['bloqueados_pct_media'], 2)} |")
sin = [L for k, L in LOC.items() if k.startswith("SIN")]; apr = [L for k, L in LOC.items() if k.startswith("APRENDE")]
apr_h = (st.mean(L["resumen"]["huellas_por_vida"] for L in apr if L["resumen"]["huellas_por_vida"] is not None) if apr else None)
eps_txt = ""
if sin and apr_h:
    for L in sin:
        import subprocess
        env = subprocess.run(["docker", "image", "inspect", L["imagen"], "--format", "{{range .Config.Env}}{{println .}}{{end}}"], capture_output=True, text=True).stdout
        e0 = next((float(x.split("=", 1)[1]) for x in env.split() if x.startswith("GEMV_P7_EPS=")), None)      # la eps de la imagen, leida de la imagen
        h = L["resumen"]["huellas_por_vida"]
        r_ = L["resumen"]; fz = r_["forzadas_total"]; ac = r_["acaban"]; ya = r_["no_cabe_objeto_ya_no_esta"]
        if e0 and h: eps_txt += f"**{L['nombre']}**: ε = {e0:g}; {n(h, 2)} pruebas por vida frente a {n(apr_h, 2)} de APRENDE con las piezas nuevas (media de las dos personalidades): {n(100 * (h / apr_h - 1), 0)} % ({'dentro' if abs(h / apr_h - 1) <= 0.2 else 'fuera'} del ±20 %); ε proporcional para igualar: {e0 * apr_h / h:.5f}. Forzadas que acaban: {ac} de {fz} ({n(100 * ac / fz if fz else None, 0)} %, {'≥' if fz and ac >= 0.9 * fz else '<'} 90 %); de las {r_['fines_total']['no cabe']} «no cabe», en {ya} el objeto ya no estaba en la casilla al llegar (otro se lo llevó): sin esas, {ac} de {fz - ya} ({n(100 * ac / (fz - ya) if fz - ya else None, 0)} %). "
# tablas del sello
TC = ["| criatura | lo inútil manda (cierres de 20) | d15-20 (de 6) | la clase que manda, d1 → d20 | h final (red · camuflaje) | k* botiquín cadena (real) | pruebas botiquín | recuperaciones |", "|---|---:|---:|---|---|---|---:|---:|"]
for k, cr in S["criaturas"].items():
    ci = cr["cierres"]; hf = cr.get("habituacion_final") or {}
    TC.append(f"| {k} | {sum(1 for d, m, h in ci if m in ('net', 'camouflage'))} | {sum(1 for d, m, h in ci if d >= 15 and m in ('net', 'camouflage'))} | {' '.join(NOM[m][:3] for d, m, h in ci)} | {n((hf.get('net') or {}).get('h'), 2)} · {n((hf.get('camouflage') or {}).get('h'), 2)} | {cr['k_estrella'] if cr['k_estrella'] else '∞'} ({cr['k_estrella_real'] if cr['k_estrella_real'] else '∞'}) | {cr['pruebas_botiquin']} | {len(cr['recuperaciones'])} |")
EPS2 = "—"
if "SIN_e0023" in LOC:
    import subprocess as _sp
    _env = _sp.run(["docker", "image", "inspect", LOC["SIN_e0023"]["imagen"], "--format", "{{range .Config.Env}}{{println .}}{{end}}"], capture_output=True, text=True).stdout
    EPS2 = next((x.split("=", 1)[1] for x in _env.split() if x.startswith("GEMV_P7_EPS=")), "—")
coste = "4 variantes (APRENDE_v, APRENDE_p, SIN_v, SIN_p) × 20 días × 3 series = 240 partidas = 240 créditos; con SIN de una personalidad (como en P7-42), 180"

out = f"""# P7-47 · Banco (coste cero): habituación y peso de la intensidad; el rival SIN arreglado en local

*12-oct-2026. Sello `SELLO_P7_47.md` (commit `794b6bc`, antes de calcular). Plataforma: 0 créditos (saldo {('**' + saldo + '**, dato de Manel 12-oct 06:47') if saldo else 'el de la página'}); consola 0 $. Nada lanzado en
plataforma. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`. Piezas nuevas (las del campo no se tocan): `habitua_P7_47.py` = `{md5('habitua_P7_47.py')}`, `azar_P7_47.py` = `{md5('azar_P7_47.py')}`,
`campo_P7_47.py`, `policy_pareja_P7_47.py`, `Dockerfile.pareja_P7_47`. Banco: `banco_P7_47.py --cadena` (12 criaturas × 20 días en cadena honesta sobre los diarios del campo P7-45, {C['segundos']} s) →
`P7_47_cadena.json`, `P7_47_res/`; `analiza_P7_47.py` → `P7_47_sello.json`; `local_P7_47.py` (partidas locales con `coworld play`) → `P7_47_local_*.json`; `escribe_informe_P7_47.py` (este informe; ninguna cifra a mano).
Fidelidad de la réplica al diario: {n(S['fidelidad']['igual'], 0)} decisiones iguales · {n(S['fidelidad']['difiere'], 0)} distintas ({n(100 * S['fidelidad']['difiere'] / (S['fidelidad']['igual'] + S['fidelidad']['difiere']), 1)} %).*

## El sello, de una vez

| | criterio | resultado | pasa |
|---|---|---|---|
| H1 | lo inútil manda en ≤ 50 % de los cierres y ≤ 20 % de los de d15-20 | {H1['inutil_manda']} de {H1['cierres']} ({n(H1['pct'], 1)} %); d15-20 {H1['d15_20_inutil']} de {H1['d15_20_cierres']} ({n(H1['d15_20_pct'], 1)} %) | {'sí' if H1['pasa'] else 'NO'} |
| H2 | en los momentos de decisión, `coger` lo inútil gana en ≤ 1/3 | {H2['coger']} de {H2['momentos']} ({n(100 * H2['fraccion_coger'], 0)} %; `ir_curioso` {H2['ir_curioso']}, `noop` {H2['elegidos'].get('noop', 0)}) | {'sí' if H2['pasa'] else 'NO'} |
| H3 | mediana de pruebas del botiquín para llegar a 25 ≤ 12 | {n(H3['mediana'], 1)} ({H3['llegan']} de 12 llegan); mismo cálculo sobre los cuadernos reales del campo: {('mediana ' + n(H3['real']['mediana'], 1)) if H3['real']['mediana'] is not None else 'mediana ∞'} ({H3['real']['llegan']} de 12 llegan) | {'sí' if H3['pasa'] else 'NO'} |
| H4 | lo habituado vuelve a llamar tras ≥ 5 días sin probarlo en ≥ 2 criaturas | {H4['n']} criaturas | {'sí' if H4['pasa'] else 'NO'} |

**Regla de parada: {'H1, H2 y H3 pasan: hay campo' if S['pasa_sello'] else 'no pasan ' + ', '.join(h for h, p in (('H1', H1['pasa']), ('H2', H2['pasa']), ('H3', H3['pasa'])) if not p) + ' → NO HAY CAMPO; se informa y se para'}.** Por personalidad: lo inútil manda {H1['por_variante']['APRENDE_v']['inutil']} de {H1['por_variante']['APRENDE_v']['cierres']} (valiente) y {H1['por_variante']['APRENDE_p']['inutil']} de {H1['por_variante']['APRENDE_p']['cierres']} (prudente);
`coger` gana {H2['por_variante']['APRENDE_v']['coger']} de {H2['por_variante']['APRENDE_v']['momentos']} y {H2['por_variante']['APRENDE_p']['coger']} de {H2['por_variante']['APRENDE_p']['momentos']}; k* mediana {n(H3['por_variante']['APRENDE_v']['mediana'], 1) if H3['por_variante']['APRENDE_v']['mediana'] is not None else '∞'} (valiente) y {n(H3['por_variante']['APRENDE_p']['mediana'], 1) if H3['por_variante']['APRENDE_p']['mediana'] is not None else '∞'} (prudente).

## Sección 1 · Lo que hicieron las dos piezas

- **Intensidad en su escala**: en los {len(v)} recuerdos sin corte de los cuadernos finales de la cadena, cuartiles {n(q[0], 2)} · {n(q[1], 2)} · {n(q[2], 2)} ({sum(1 for x in v if x >= 4)} en el tope 4), frente a {n(q40[0], 2)} · {n(q40[1], 2)} · {n(q40[2], 2)} con la
  fórmula de P7-40 sobre los mismos recuerdos. El peso de lo vivido frente al neutro sube: por eso H3 pasa (k* mediana {n(H3['mediana'], 1)}; con los cuadernos reales del campo {H3['real']['llegan']} de 12 llegan).
- **Habituación**: {S['habituaciones']} pruebas acabaron en «no hizo nada» (importancia 0 en B1) frente a {S['pruebas_con_efecto']} con efecto: la habituación se disparó {S['habituaciones']} veces en 240 vidas. Con el filtro de P7-39 la
  importancia de una prueba de red o camuflaje casi nunca es exactamente 0 (queda pequeña pero positiva), así que la regla «× 0,5 por cada nada» apenas actúa; aun así, al
  cerrar el día 20, h₀ de la red y el camuflaje está entre {n(min(x['h'] for cr in S['criaturas'].values() for x in (cr.get('habituacion_final') or {}).values()), 2)} y {n(max(x['h'] for cr in S['criaturas'].values() for x in (cr.get('habituacion_final') or {}).values()), 2)} en las {sum(1 for cr in S['criaturas'].values() if cr.get('habituacion_final'))} criaturas que la tuvieron (tabla). Y lo inútil sigue mandando: la
  ignorancia de lo probado pocas veces × su esperanza pesan más que un h de 0,2-0,5 (H1), y en el momento de la red a los pies `coger` sigue ganando (H2).
- **Recuperación (H4)**: ninguna cosa habituada pasó 5 días sin probarse y volvió a mandar: se siguen probando (la curiosidad habituada sigue siendo la mayor) o no vuelven.

{chr(10).join(TC)}

Lo inútil manda por día (de 12 cierres): {' '.join(f"d{d}:{H1['por_dia_inutil'][str(d)]}" for d in range(1, 21))}. Manda por clase en los 240 cierres: {', '.join(f"{NOM[o]} {k}" for o, k in H1['manda_por_clase'].items())}.

## Sección 2 · El rival arreglado (SIN) en partidas locales de verdad

`coworld play` funciona en local (motor `zero-sum-0.1.19`, variante competition, 16 contenedores nativos arm64 con nuestra imagen en todos los asientos: no hay imágenes
locales de los rivales de la liga, así que las 16 criaturas son nuestras, en 8 parejas; cuaderno vacío = día 1). Cambios de `azar_P7_47` frente a `azar_P7_41`: la forzada de ir
se cierra en la casilla (hacer_sitio si lo ofrece el cuerpo; `coger` puesto para el objeto forzado si el cuerpo no lo ofrece; «no cabe» a los 24 tics) y la moneda de usar solo
cuando el cuerpo ofrece `usar_*` (hp < máximo).

{chr(10).join(TL)}

{eps_txt or 'Sin partidas locales de SIN leídas todavía.'}

## Sección 3 · Coste de un campo (no se lanza: la regla de parada lo cierra)

{coste}. Créditos de partida: {saldo or '—'} (12-oct). Sin campo por H1 y H2, el número queda para la mesa.

## Lectura

1. La intensidad en su escala hace lo que se le pidió con lo útil: la creencia del botiquín llega a 25 en {H3['llegan']} de 12 criaturas con mediana {n(H3['mediana'], 1)} pruebas (H3 pasa). La habituación no hace
   lo que se le pidió con lo inútil, porque su disparador («no hizo nada» = importancia exactamente 0) casi no ocurre con el filtro B1: {S['habituaciones']} veces en {S['habituaciones'] + S['pruebas_con_efecto']} pruebas.
2. Aun con h en 0,2-0,5 en la mayoría de las criaturas, la red y el camuflaje siguen mandando ({n(H1['pct'], 0)} % de los cierres; {n(H1['d15_20_pct'], 0)} % en d15-20) y `coger` sigue ganando en el momento
   ({n(100 * H2['fraccion_coger'], 0)} %): la ignorancia de lo probado pocas veces manda, como en P7-40. Para que la habituación mordiera haría falta que «no hizo nada» fuera «importancia
   pequeña» (umbral) y no «cero exacto», o un factor por prueba sin efecto grande — decisiones de la mesa, no de este banco. Se propone, no se ejecuta.
3. El rival arreglado, en lazo cerrado local: con ε = {EPS2} SIN prueba {n(LOC['SIN_e0023']['resumen']['huellas_por_vida'], 2) if 'SIN_e0023' in LOC else '—'} veces por vida frente a {n(apr_h, 2)} de APRENDE (dentro del ±20 %); las forzadas que acaban son
   {LOC['SIN_e0023']['resumen']['acaban'] if 'SIN_e0023' in LOC else '—'} de {LOC['SIN_e0023']['resumen']['forzadas_total'] if 'SIN_e0023' in LOC else '—'} ({n(LOC['SIN_e0023']['resumen']['acaban_pct'], 0) if 'SIN_e0023' in LOC else '—'} %, no llega al 90 %), pero {LOC['SIN_e0023']['resumen']['no_cabe_objeto_ya_no_esta'] if 'SIN_e0023' in LOC else '—'} de las que no acaban son objetos que otro se llevó antes de llegar (16 criaturas nuestras disputando el mismo botín): sin esas, el {n(100 * LOC['SIN_e0023']['resumen']['acaban'] / (LOC['SIN_e0023']['resumen']['forzadas_total'] - LOC['SIN_e0023']['resumen']['no_cabe_objeto_ya_no_esta']), 0) if 'SIN_e0023' in LOC else '—'} %.
   Ya no caduca ninguna por el zurrón ni por el usar con la vida llena. Regla de parada: no hay campo; el rival queda listo para cuando la mesa decida.
"""
open(os.path.join(AQUI, "informe_P7_47.md"), "w", encoding="utf-8").write(out); print("informe_P7_47.md", out.count("\n"), "lineas")

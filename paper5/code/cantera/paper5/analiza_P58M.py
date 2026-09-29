"""[P5-8M] El acumulado: sellos K1 a K7 (K5 POR FORMA) y lo que va sin sello.

  python3 cantera/paper5/mide_P58M.py 0 1      -> P58M_0_1.json
  python3 cantera/paper5/analiza_P58M.py 0 1
"""
import collections, json, statistics as st, sys

ET = "_".join([a for a in sys.argv[1:] if not a.startswith("-")] or ["0"])
A = json.load(open(f"cantera/paper5/P58M_{ET}.json"))
K = [a for a in A if a["brazo"] == "K"]
Ar = [a for a in A if a["brazo"] == "A"]
F = [f for a in K for f in a["formas"]]


def pc(a, b): return f"{100.0*a/b:.1f}%" if b else "—"


def tr(d):
    return ("1-3" if d <= 3 else "4-5" if d <= 5 else "6-7" if d <= 7
            else "8-9" if d <= 9 else "10+")


print(f"### P5-8M · ACUMULADO DE LAS TANDAS {ET.replace('_',', ')} ###")
print(f"    {len(A)} asientos · {len(K)} de K · {len(Ar)} de A · {len(F)} formas")

# ── el suelo de cantidad, DE SERIE (correccion de la mesa, tanda 2) ──
print("\n=== EL SUELO DE SERIE: al menos 150 formas aceptadas en las cuarenta ===")
porp = collections.defaultdict(int)
for a in K:
    porp[a["semilla"]] += a["aceptadas"]
for s, v in sorted(porp.items()):
    print(f"    semilla {s}: {v:3d} aceptadas")
ac_tot = sum(porp.values()); n_part = len(porp)
print(f"    ACUMULADO: {ac_tot} formas en {n_part} partidas de K "
      f"({ac_tot/max(n_part,1):.1f} por partida)")
print(f"    proyeccion a 20 partidas de K (las cuarenta): "
      f"{ac_tot/max(n_part,1)*20:.0f}  (suelo 150) -> "
      f"{'EN CAMINO' if ac_tot/max(n_part,1)*20 >= 150 else 'POR DEBAJO'}")

# ── K1 ──
td = sum(x["t_dentro"] for x in K); tf = sum(x["t_fuera"] for x in K)
nd = sum(x["nuevas_dentro"] for x in K); nf = sum(x["nuevas_fuera"] for x in K)
tfa = sum(x["t_fuera"] for x in Ar); nfa = sum(x["nuevas_fuera"] for x in Ar)
tot_k = 100.0 * (nd + nf) / (td + tf); tot_a = 100.0 * nfa / tfa
r1 = tot_k / tot_a
r2 = (100.0 * nd / td) / (100.0 * nf / tf) if td else None
print("\n=== K1 · casillas nuevas por cien tics ===")
print(f"    K {tot_k:.2f} · A {tot_a:.2f} -> K/A = {r1:.2f}  (sello >= 1,5)")
print(f"    dentro {100.0*nd/td:.2f} · fuera {100.0*nf/tf:.2f} -> {r2:.2f}x  (sello >= 2)"
      if td else "    sin tics dentro de forma")
print(f"    -> {'CUMPLE' if (r1 >= 1.5 and r2 and r2 >= 2) else 'FALLA'}")

# ── K2 · EL PUESTO, que es lo que mas se vigila ──
print("\n=== K2 · vida y PUESTO, por semilla (K contra A) ===")
pk = {a["semilla"]: [] for a in A}
for a in A:
    pk.setdefault(a["semilla"], [])
for a in A:
    pk[a["semilla"]].append((a["brazo"], a["slot"], a["puesto"]))
peor = 0; mejor = 0; igual = 0
for s in sorted(pk):
    fila = sorted(pk[s])
    kk = [p for b, sl, p in fila if b == "K" and p is not None]
    aa = [p for b, sl, p in fila if b == "A" and p is not None]
    if kk and aa:
        mk, ma = st.median(kk), st.median(aa)
        sg = "K PEOR" if mk > ma else ("K mejor" if mk < ma else "igual")
        peor += mk > ma; mejor += mk < ma; igual += mk == ma
    else:
        mk = ma = None; sg = "?"
    print(f"    {s}: K {kk} (med {mk}) · A {aa} (med {ma})   {sg}")
print(f"    resumen: K peor en {peor} semillas · mejor en {mejor} · igual en {igual}")
print("\n  POR SEMILLA, para leer por que unas nacen 5 y otras 150:")
print(f"    {'semilla':>10s} {'nacidas':>8s} {'acep':>5s} {'ign inicial':>12s} "
      f"{'tics K':>8s} {'seguro':>13s} {'inseguro':>13s}")
for s in sorted({a['semilla'] for a in K}):
    S = [a for a in K if a["semilla"] == s]
    nacs = sum(a["nacidas"] for a in S); acs = sum(a["aceptadas"] for a in S)
    ig = [a.get("ign_inicial") for a in S if a.get("ign_inicial") is not None]
    tt = sum(a["tics"] for a in S)
    sg = sum(a.get("tics_seguro", 0) for a in S)
    ins = sum(a.get("tics_inseguro", 0) for a in S)
    print(f"    {s:>10s} {nacs:8d} {acs:5d} "
          f"{(f'{st.median(ig):.4f}' if ig else '—'):>12s} {tt:8d} "
          f"{sg:6d} ({pc(sg,tt):>5s}) {ins:6d} ({pc(ins,tt):>5s})"
          f"   nacidas/tic seguro {nacs/max(sg,1):.4f}")
_sg = sum(a.get("tics_seguro", 0) for a in K)
_na = sum(a["nacidas"] for a in K)
print(f"    AGREGADO: {_na} nacidas / {_sg} tics seguros = {_na/max(_sg,1):.4f} "
      f"por tic seguro  (1 cada {_sg/max(_na,1):.0f} tics)")
md = sum(x["muertes_dentro"] for x in K)
print(f"    muertes dentro de forma: {md}  (sello: 0) -> {'CUMPLE' if md == 0 else 'FALLA'}")

# ── [t3] (1) K2 SEPARADO: vida y puesto · (3) VENTANAS EMPAREJADAS ──
print("\n=== (1) K2 SEPARADO EN VIDA Y PUESTO, por semilla ===")
print(f"    {'semilla':>10s} {'vida K':>14s} {'vida A':>14s} {'puesto K':>9s} "
      f"{'puesto A':>9s} {'hp fin K':>9s} {'hp fin A':>9s}")
peor_v = mejor_v = 0
for sm in sorted({a['semilla'] for a in A}):
    Ks = [a for a in K if a["semilla"] == sm]; As = [a for a in Ar if a["semilla"] == sm]
    if not Ks or not As: continue
    vk = st.median([a["vida_tics"] for a in Ks]); va = st.median([a["vida_tics"] for a in As])
    pk_ = st.median([a["puesto"] for a in Ks if a["puesto"] is not None] or [0])
    pa_ = st.median([a["puesto"] for a in As if a["puesto"] is not None] or [0])
    hk = st.median([a["hp_ult"] or 0 for a in Ks]); ha = st.median([a["hp_ult"] or 0 for a in As])
    peor_v += vk < va; mejor_v += vk > va
    print(f"    {sm:>10s} {vk:14.0f} {va:14.0f} {pk_:9.1f} {pa_:9.1f} {hk:9.0f} {ha:9.0f}"
          f"   {'vida K PEOR' if vk < va else 'vida K mejor' if vk > va else 'vida igual'}")
print(f"    resumen VIDA: K vive menos en {peor_v} semillas · mas en {mejor_v}")

print("\n=== (3) K1 PRIMERA MITAD EN VENTANAS EMPAREJADAS ===")
print("    (solo los tics en que el asiento de K y el de A de la MISMA semilla")
print("     y el MISMO puesto siguen los dos vivos)")
tk_v = ta_v = nk_v = na_v = 0
for sm in sorted({a['semilla'] for a in A}):
    for sl in ("10", "11"):
        k1 = next((a for a in K if a["semilla"] == sm and a["slot"] == sl), None)
        a1 = next((a for a in Ar if a["semilla"] == sm and a["slot"] == sl), None)
        if not k1 or not a1: continue
        N = min(k1["vida_tics"], a1["vida_tics"])
        def dentro(x):
            v = sorted(int(t) for t in x["visto_en"].values())
            t0 = v[0] if v else 0
            return sum(1 for t in v if t < t0 + N)
        ck, ca = dentro(k1), dentro(a1)
        tk_v += N; ta_v += N; nk_v += ck; na_v += ca
        print(f"    {sm} /{sl}: ventana {N:6d} tics · K {100.0*ck/N:6.2f} · "
              f"A {100.0*ca/N:6.2f} -> {ck/max(ca,1):.2f}")
if tk_v:
    print(f"    AGREGADO emparejado: K {100.0*nk_v/tk_v:.2f} · A {100.0*na_v/ta_v:.2f} "
          f"-> K/A = {(nk_v/tk_v)/(na_v/ta_v):.2f}  (sello >= 1,5)")

# ── K3 ──
k3 = sum(x["k3_armado_a_tiro_en_forma"] for x in K)
k3l = sum(x.get("k3_listas", 0) for x in K)
tdl = sum(x.get("t_dentro_listas", 0) for x in K)
print("\n=== K3 · DOS LECTURAS ===")
print(f"    (a) SELLADA — todo tic con forma activa : {k3} de {td} tics dentro"
      f"  -> {'CUMPLE' if k3 == 0 else 'FALLA'}")
print(f"    (b) DEL MECANISMO — solo piernas listas : {k3l} de {tdl} tics"
      f"  -> {'CUMPLE' if k3l == 0 else 'FALLA'}")
print("    (en enfriamiento manda el DECISOR entero: el candidato de la forma")
print("     no entra en la papeleta —`_veta_receta` lo manda al prefijo `ir_`—,")
print("     el compromiso devuelve la accion del decisor sin tocarla, y el")
print("     renglon de curiosidad vive solo dentro de `_juzga`.)")
for a in sorted(K, key=lambda x: (x["semilla"], x["slot"])):
    if a["k3_armado_a_tiro_en_forma"]:
        print(f"      K {a['semilla']}/{a['slot']}: sellada {a['k3_armado_a_tiro_en_forma']:3d} · "
              f"mecanismo {a.get('k3_listas',0):3d}")

# ── K4 ──
mot = collections.Counter(f["motivo"] for f in F)
comp = sum(v for k, v in mot.items() if "completada" in k)
vd = sum(v for k, v in mot.items() if "veto duro" in k)
print("\n=== K4 · causas de fin ===")
for k, v in mot.most_common():
    print(f"    {k:34s} {v:4d}  {pc(v, len(F))}")
sr = sum(v for k, v in mot.items() if "sin rodeo" in k)
print(f"    completadas {comp}/{len(F)} = {pc(comp,len(F))} (sello >= 50 %) -> "
      f"{'CUMPLE' if len(F) and comp/len(F) >= .5 else 'FALLA'}")
print("    la banda del veto duro, DOS LECTURAS (sello 5-30 %):")
for nom, v in (("(a) solo «veto duro»", vd),
               ("(b) «veto duro» + «sin rodeo»", vd + sr)):
    r = v / len(F) if len(F) else 0
    print(f"      {nom:32s} {v:3d}/{len(F)} = {pc(v,len(F)):>6s} -> "
          f"{'CUMPLE' if .05 <= r <= .30 else 'FALLA'}")
ok4 = len(F) and comp / len(F) >= .5 and .05 <= (vd + sr) / len(F) <= .30
print(f"    -> K4 con la lectura (b): {'CUMPLE' if ok4 else 'FALLA'}")

# ── K5 POR FORMA ──
dd = sum(1 for f in F if f.get("dano_durante"))
seg = sum((x["desglose"].get("seguro") or {}).get("decisiones", 0) for x in Ar)
ds = sum((x["desglose"].get("seguro") or {}).get("dano_en_50", 0) for x in Ar)
print("\n=== K5 · POR FORMA (correccion de P5-8L) ===")
print(f"    formas con daño MIENTRAS vivian: {dd}/{len(F)} = {pc(dd,len(F))}")
print(f"    base de A en entorno seguro    : {ds}/{seg} = {pc(ds,seg)}")
print(f"    -> {'CUMPLE' if (len(F) and 100.0*dd/len(F) <= 100.0*ds/max(seg,1)) else 'FALLA'}")

# ── K6 ──
ms = [x["ms_med"] for x in K if x["ms_med"] is not None]
per = sum(x["perdidos"] for x in A)
print(f"\n=== K6 · ms mediana por asiento {sorted(ms)} · tics perdidos {per}"
      f"  -> {'CUMPLE' if (ms and max(ms) < 5 and per == 0) else 'FALLA'} ===")
print("    (4) el ms separado: tics CON nacimiento de forma y sin el")
print(f"      {'asiento':>16s} {'n nace':>7s} {'ms nace':>8s} {'n sin':>7s} {'ms sin':>7s} {'x':>5s}")
mn = [x for x in K if x.get("ms_nace_med") and x.get("ms_sin_med")]
for x in sorted(mn, key=lambda y: -(y["ms_nace_med"] or 0))[:8]:
    print(f"      {x['semilla']+'/'+x['slot']:>16s} {x['n_nace']:7d} {x['ms_nace_med']:8.3f} "
          f"{x['n_sin']:7d} {x['ms_sin_med']:7.3f} {x['ms_nace_med']/x['ms_sin_med']:5.1f}")
if mn:
    print(f"      mediana de las medianas: nace {st.median([x['ms_nace_med'] for x in mn]):.3f} ms · "
          f"sin {st.median([x['ms_sin_med'] for x in mn]):.3f} ms · "
          f"x{st.median([x['ms_nace_med']/x['ms_sin_med'] for x in mn]):.1f}")

# ── [t3] (2) DE QUE ESTA HECHA LA DIFERENCIA DE PUNTUACION ──
print("\n=== (2) DONDE K QUEDA POR DEBAJO: de que esta hecha la diferencia ===")
print(f"    {'semilla':>10s} {'puesto':>13s} {'score':>13s} {'bajas':>9s} "
      f"{'dano hecho':>15s} {'botin':>11s} {'vida':>15s}")
for sm in sorted({a['semilla'] for a in A}):
    Ks = [a for a in K if a["semilla"] == sm]; As = [a for a in Ar if a["semilla"] == sm]
    if not Ks or not As: continue
    pk_ = st.median([a["puesto"] for a in Ks if a["puesto"] is not None] or [0])
    pa_ = st.median([a["puesto"] for a in As if a["puesto"] is not None] or [0])
    if pk_ <= pa_: continue                     # solo donde K queda por debajo
    def su(S, k): return sum(a.get(k) or 0 for a in S)
    print(f"    {sm:>10s} {pk_:6.1f}/{pa_:<6.1f} "
          f"{su(Ks,'score'):6.0f}/{su(As,'score'):<6.0f} "
          f"{su(Ks,'bajas'):4.0f}/{su(As,'bajas'):<4.0f} "
          f"{su(Ks,'dano_hecho'):7.0f}/{su(As,'dano_hecho'):<7.0f} "
          f"{su(Ks,'cogidos'):5.0f}/{su(As,'cogidos'):<5.0f} "
          f"{su(Ks,'vida_tics'):7.0f}/{su(As,'vida_tics'):<7.0f}")
print("    (K/A en cada columna; solo las semillas donde el puesto mediano de K es PEOR)")
_td = sum(x["t_dentro"] for x in K); _tf = sum(x["t_fuera"] for x in K)
print(f"    tics en forma activa {_td} de {_td+_tf} = {pc(_td,_td+_tf)} del tiempo de K")

# ── sin sello ──
print("\n=== SIN SELLO ===")
print("  aceptacion por asiento:")
for a in sorted(K, key=lambda x: (x["semilla"], x["slot"])):
    print(f"    K {a['semilla']}/{a['slot']}: {a['aceptadas']:3d}/{a['nacidas']:3d} = "
          f"{pc(a['aceptadas'],a['nacidas']):>6s} · W med {a['W_med']} · "
          f"ventaja med {a['ventaja_med']} · rodeos {a['n_rodeos']} · sin rodeo {a['sin_rodeo']}")
nac = sum(a["nacidas"] for a in K); ac = sum(a["aceptadas"] for a in K)
print(f"    AGREGADO: {ac}/{nac} = {pc(ac,nac)}")

print("\n  distancia al nacer x causa de fin:")
print(f"    {'tramo':>6s} {'n':>4s} {'completada':>12s} {'atasco':>11s} {'veto duro':>11s} {'sin rodeo':>10s}")
for t in ("1-3", "4-5", "6-7", "8-9", "10+"):
    S = [f for f in F if f.get("dist_nace") is not None and tr(f["dist_nace"]) == t]
    if not S: continue
    c = collections.Counter(("completada" if "completada" in f["motivo"]
                             else "sin rodeo" if "sin rodeo" in f["motivo"]
                             else f["motivo"][:9]) for f in S)
    print(f"    {t:>6s} {len(S):4d} {c['completada']:5d} ({pc(c['completada'],len(S)):>6s}) "
          f"{c['atasco']:4d} ({pc(c['atasco'],len(S)):>6s}) {c['veto duro']:4d} "
          f"({pc(c['veto duro'],len(S)):>6s}) {c['sin rodeo']:4d}")

rr = [f for f in F if f.get("rodeos")]
print(f"\n  rodeos: {len(rr)} formas de {len(F)} rodearon · "
      f"«sin rodeo» {sum(a['sin_rodeo'] for a in K)}")
if rr:
    ex = [e for f in rr for e in (f.get("extra") or []) if e is not None]
    cc = sum(1 for f in rr if "completada" in f["motivo"])
    nr = [f for f in F if not f.get("rodeos")]
    cn = sum(1 for f in nr if "completada" in f["motivo"])
    print(f"    casillas extra: mediana {st.median(ex)} · min {min(ex)} · max {max(ex)}"
          if ex else "    sin extra registrado")
    print(f"    completan: rodearon {cc}/{len(rr)} = {pc(cc,len(rr))} · "
          f"no rodearon {cn}/{len(nr)} = {pc(cn,len(nr))}")

ob = sum(a["obedece"] for a in K); ro = sum(a["rompe"] for a in K)
co = sum(a["contra"] for a in K); cc2 = sum(a["coste_contra"] for a in K)
ca = collections.Counter()
for a in K: ca.update(a["causas"])
print(f"\n  compromiso: piernas listas {ob+ro} · obedece {ob} = {pc(ob,ob+ro)} · rompe {ro}")
print(f"    contra el decisor: {co} = {pc(co,ob)} · coste {cc2:+.4f} · "
      f"{cc2/max(co,1):+.5f}/tic")
print(f"    RUPTURAS POR CAUSA: {dict(ca) if ca else 'NINGUNA'}")

o = sum(f["obj"] for f in F); du = sum(f["durante"] for f in F)
de = sum(f["despues"] for f in F); nu = sum(f["nunca"] for f in F)
print(f"\n  prometido/visto: {du} durante ({pc(du,o)}) · {de} despues ({pc(de,o)}) · "
      f"{nu} NUNCA ({pc(nu,o)})")
print(f"  distancia al destino: {st.median([f['d0'] for f in F])} -> "
      f"{st.median([f['d1'] for f in F])}")

W = [(f["W0"], f["W1"]) for f in F if f.get("W0") is not None and f.get("W1") is not None]
if W:
    sub = sum(1 for a, b in W if b > a + 1e-9); baj = sum(1 for a, b in W if b < a - 1e-9)
    print(f"\n  W al empezar y terminar cada forma (n={len(W)}): "
          f"mediana {st.median([x[0] for x in W]):.4f} -> {st.median([x[1] for x in W]):.4f}")
    print(f"    sube en {sub} · baja en {baj} · igual en {len(W)-sub-baj}")
cd = sum(a["cogio_dentro"] for a in K); cf = sum(a["cogio_fuera"] for a in K)
print(f"  botin: dentro {cd} en {td} tics = {100.0*cd/max(td,1):.3f}/100 · "
      f"fuera {cf} en {tf} = {100.0*cf/max(tf,1):.3f}/100")

print("\n  «acerca al armado» en inseguro:")
for br, S in (("K", K), ("A", Ar)):
    ak = sum((x["desglose"].get("inseguro") or {}).get("acerca_al_armado", 0) for x in S)
    ck = sum((x["desglose"].get("inseguro") or {}).get("con_armado_a_la_vista", 0) for x in S)
    print(f"    {br}: {ak}/{ck} = {pc(ak,ck)}")

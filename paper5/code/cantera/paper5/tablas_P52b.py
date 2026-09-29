"""[P5-2b] Las tablas del reanalisis, de P52b_resumen.json y P52b_detalle.json."""
import collections, json, math, os, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(AQUI, "P52b_resumen.json")))
D = json.load(open(os.path.join(AQUI, "P52b_detalle.json")))
CAJAS = ("aceptada", "coincide", "rechazada", "vetada", "intraducible",
         "dormida", "caducada")
COMPITEN = ("aceptada", "coincide", "rechazada")


def wilson(k, n, z=1.96):
    if not n:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * (c - h), 100 * (c + h))


def pct(a, b):
    return f"{100.0*a/b:.2f} %" if b else "n/a"


print("=== M1 · LAS CAJAS, EN LAS DOS COLUMNAS ===")
tasa = {}
for crit in ("estricto", "ventana"):
    print(f"\n  criterio {crit.upper()}")
    print(f"  {'llave':9s} {'n':>6s} " + " ".join(f"{c[:8]:>9s}" for c in CAJAS)
          + f" {'compiten':>9s} {'acept':>8s} {'IC95':>16s} {'ac+coin':>9s}")
    for k in ("ahora", "despues", "azar"):
        c = collections.Counter(R["cajas"][crit][k])
        n = sum(c.values())
        comp = sum(c[x] for x in COMPITEN)
        lo, hi = wilson(c["aceptada"], comp)
        tasa[(crit, k)] = (c["aceptada"], comp, c["coincide"])
        ic = f"[{lo:.2f},{hi:.2f}]" if comp else ""
        print(f"  {k:9s} {n:6,} " + " ".join(f"{c[x]:9,}" for x in CAJAS)
              + f" {comp:9,} {pct(c['aceptada'], comp):>8s} {ic:>16s} "
                f"{pct(c['aceptada']+c['coincide'], comp):>9s}")

print("\n=== M2 · TRADUCTOR CONTRA PUERTA, CON Y SIN LA REGLA DEL GEMELO ===")
for crit in ("estricto", "ventana"):
    a = [x for x in D[crit] if x["llave"] == "ahora"]
    rech = [x for x in a if x["caja"] == "rechazada"]
    malos = [x for x in a if x["caja"] in ("rechazada", "intraducible",
                                           "caducada")]
    vuelve = sum(1 for x in a if x.get("nombre") == x.get("elegido_real"))
    puerta = [x for x in rech if x.get("nombre") == x.get("elegido_real")]
    gem = [x for x in rech if x.get("gemelo")]
    print(f"\n  {crit}: escenas {len(a):,} · vuelve al candidato original "
          f"{vuelve:,} = {pct(vuelve, len(a))}")
    print(f"    fallos {len(malos):,} · del TRADUCTOR "
          f"{len(malos)-len(puerta):,} = {pct(len(malos)-len(puerta), len(malos))}"
          f" · de la PUERTA {len(puerta):,} = {pct(len(puerta), len(malos))}")
    print(f"    rechazos con GEMELO (mismo destino, otro nombre): {len(gem):,}"
          f" de {len(rech):,} = {pct(len(gem), len(rech))}")
print("\n  cambios de caja si el gemelo cuenta como 'coincide':")
for crit in ("estricto", "ventana"):
    tot = collections.Counter()
    for x in D[crit]:
        if x.get("gemelo") and x["caja"] in ("rechazada", "vetada"):
            tot[(x["llave"], x["caja"])] += 1
    print(f"    {crit}: {dict(tot) if tot else 'ninguno'} · "
          f"total {sum(tot.values())}")
    for k in ("ahora", "despues", "azar"):
        ac, comp, coin = tasa[(crit, k)]
        mueve = sum(v for (kk, cc), v in tot.items() if kk == k)
        if comp:
            print(f"       {k:8s} acept+coin pasa de {pct(ac+coin, comp)} a "
                  f"{pct(ac+coin+mueve, comp)}")

print("\n=== M3 · QUE FILA TUMBA A O-DESPUES ===")
for crit in ("estricto", "ventana"):
    rd = [x for x in D[crit] if x["llave"] == "despues"
          and x["caja"] == "rechazada"]
    t = collections.Counter()
    for x in rd:
        f = x.get("filas") or {}
        t[max(f, key=lambda k: f[k]) if f else "(sin detalle)"] += 1
    print(f"  {crit}: {len(rd)} rechazos · " + " · ".join(
        f"{k} {pct(v, len(rd))}" for k, v in t.most_common(5)))
    pa = [x["pasos"] for x in rd if x.get("pasos") is not None]
    if pa:
        print(f"      distancia del destino en los rechazos: mediana "
              f"{st.median(pa)} · max {max(pa)}")

print("\n=== M4 · O-DESPUES POR DISTANCIA ===")
for crit in ("estricto", "ventana"):
    print(f"  {crit}:")
    for p in (1, 2, 3):
        up = [x for x in D[crit] if x["llave"] == "despues"
              and x.get("pasos") == p]
        c = collections.Counter(x["caja"] for x in up)
        cc = sum(c[x] for x in COMPITEN)
        lo, hi = wilson(c["aceptada"], cc)
        ic = f" IC95 [{lo:.2f},{hi:.2f}]" if cc else ""
        print(f"    a {p} paso(s): {len(up):4d} escenas · vetadas {c['vetada']:4d}"
              f" · compiten {cc:4d} · aceptada {c['aceptada']:3d} = "
              f"{pct(c['aceptada'], cc):>7s}{ic}")

print("\n=== M5 · LA MEJORA REAL A LOS 100 TICS ===")
mej = [x["mejora"] for x in D["estricto"]
       if x["llave"] == "despues" and x.get("mejora") is not None]
if mej:
    print(f"  n={len(mej):,} · mediana {st.median(mej):+.5f} · media "
          f"{sum(mej)/len(mej):+.5f}")

print("\n=== LAS PIERNAS (3) ===")
p = R["piernas"]
print(f"  tics vivos                         {p['vivos']:,}")
print(f"  con move_ready_in > 0 (enfriando)  {p['frias']:,} = "
      f"{pct(p['frias'], p['vivos'])}")
print(f"  decisiones noop                    {p['noop']:,} = "
      f"{pct(p['noop'], p['vivos'])}")
print(f"  noop con las piernas frias         {p['noop_frias']:,} = "
      f"{pct(p['noop_frias'], p['noop'])} de los noop")
print(f"  noop con las piernas LIBRES        {p['noop']-p['noop_frias']:,} = "
      f"{pct(p['noop']-p['noop_frias'], p['noop'])} de los noop")
v = R["ventana"]
esp = v["espera hasta la ventana"] / max(1, v["escenas"] - v.get(
    "sin ventana (piernas frias los 100 tics)", 0))
print(f"  espera media hasta la ventana      {esp:.2f} tics · sin ventana en "
      f"{v.get('sin ventana (piernas frias los 100 tics)', 0)} de {v['escenas']}")

print("\n=== (4) O-DESPUES CONTRA O-AZAR, CON VENTANA ===")
for crit in ("estricto", "ventana"):
    k1, n1, _ = tasa[(crit, "despues")]
    k2, n2, _ = tasa[(crit, "azar")]
    p1, p2 = k1 / n1, k2 / n2
    d = 100 * (p1 - p2)
    se = 100 * math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    print(f"  {crit:9s} despues {100*p1:5.2f} % (n={n1}) · azar {100*p2:5.2f} %"
          f" (n={n2}) · diferencia {d:+.2f} pts · IC95 "
          f"[{d-1.96*se:+.2f},{d+1.96*se:+.2f}]")
# cuantas escenas harian falta para distinguir 5 puntos
p1 = tasa[("ventana", "despues")][0] / tasa[("ventana", "despues")][1]
p2 = tasa[("ventana", "azar")][0] / tasa[("ventana", "azar")][1]
pb = (p1 + (p1 - 0.05)) / 2 if p1 > 0.05 else (p1 + p1 + 0.05) / 2
za, zb = 1.96, 0.842
for delta in (0.05,):
    pa_, pbb = p1, max(0.0, p1 - delta)
    pm = (pa_ + pbb) / 2
    n = ((za * math.sqrt(2 * pm * (1 - pm)) +
          zb * math.sqrt(pa_ * (1 - pa_) + pbb * (1 - pbb))) / delta) ** 2
    print(f"\n  para distinguir {100*delta:.0f} puntos alrededor de "
          f"{100*pa_:.2f} % con 95 % de confianza y 80 % de potencia:")
    print(f"     hacen falta {math.ceil(n):,} escenas competidas POR BRAZO")
    hoy = tasa[("ventana", "despues")][1]
    print(f"     hoy hay {hoy:,} · faltan x{n/hoy:.2f}")
    por_diario = hoy / R["diarios"]
    print(f"     a {por_diario:.1f} escenas competidas por diario, harian falta "
          f"{math.ceil(n/por_diario):,} diarios (hay 80 en S2_A)")

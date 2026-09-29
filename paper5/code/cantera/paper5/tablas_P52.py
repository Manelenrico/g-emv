"""[P5-2] Las cinco medidas y el cotejo, a partir de P52_detalle.json."""
import collections, json, os, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(AQUI, "P52_resumen.json")))
D = json.load(open(os.path.join(AQUI, "P52_detalle.json")))
CAJAS = ("aceptada", "coincide", "rechazada", "vetada", "intraducible", "dormida")
COMPITEN = ("aceptada", "coincide", "rechazada")


def pct(a, b):
    return f"{100.0*a/b:.2f} %" if b else "n/a"


print("semilla:", R["semilla"], "· diarios:", R["diarios"])
print("interruptores leidos del diario:",
      R.get("interruptores de v42 leidos del diario"))
rep = R["reproduccion"]
print(f"reproduccion: {rep['reproducidos']:,}/{rep['tics']:,} = "
      f"{100*rep['reproducidos']/rep['tics']:.2f} % · escenas {rep['escenas']:,}")
print("saltos:", R["saltos"])

print("\n=== M1 · LAS CAJAS Y LA TASA DE ACEPTACION ===")
print(f"{'llave':9s} {'n':>6s} " + " ".join(f"{c:>12s}" for c in CAJAS)
      + f" {'compiten':>9s} {'acept.':>8s} {'acept+coin':>11s}")
tasas = {}
for k in ("ahora", "despues", "azar"):
    c = R["cajas"][k]
    n = sum(c.values())
    comp = sum(c[x] for x in COMPITEN)
    tasas[k] = {"n": n, "compiten": comp,
                "aceptada": c["aceptada"] / comp if comp else None,
                "acept_coin": (c["aceptada"] + c["coincide"]) / comp if comp else None}
    print(f"{k:9s} {n:6,} " + " ".join(f"{c[x]:12,}" for x in CAJAS)
          + f" {comp:9,} {pct(c['aceptada'], comp):>8s} "
            f"{pct(c['aceptada']+c['coincide'], comp):>11s}")

print("\n=== M2 · O-AHORA: EL TRADUCTOR CONTRA LA PUERTA ===")
a = D["ahora"]
vuelve = sum(1 for x in a if x.get("nombre") == x.get("elegido_real"))
print(f"  escenas: {len(a):,}")
print(f"  la propuesta VUELVE al candidato que el cuerpo eligio: {vuelve:,} "
      f"= {pct(vuelve, len(a))}")
rech = [x for x in a if x["caja"] == "rechazada"]
intr = [x for x in a if x["caja"] == "intraducible"]
r_trad = [x for x in rech if x.get("nombre") != x.get("elegido_real")]
r_puerta = [x for x in rech if x.get("nombre") == x.get("elegido_real")]
empate = [x for x in r_trad if x.get("gana") == "empate devuelto al cuerpo"
          or (x.get("d_prop") is not None and x.get("d_gana") is not None
              and abs(x["d_prop"] - x["d_gana"]) < 1e-4)]
print(f"  fallos totales (rechazada + intraducible): {len(rech)+len(intr):,}")
print(f"    del TRADUCTOR  (no vuelve al candidato original): "
      f"{len(r_trad)+len(intr):,} = "
      f"{pct(len(r_trad)+len(intr), len(rech)+len(intr))}")
print(f"       de ellos, intraducibles del todo: {len(intr):,}")
print(f"       de ellos, empate exacto devuelto al cuerpo: {len(empate):,}")
print(f"    de la PUERTA   (vuelve y pierde): {len(r_puerta):,} = "
      f"{pct(len(r_puerta), len(rech)+len(intr))}")
print("  forma del texto en las escenas:",
      dict(collections.Counter(x.get("forma") for x in a).most_common()))

print("\n=== M3 · O-DESPUES: QUE FILA TUMBA, Y A QUE DISTANCIA ===")
d = D["despues"]
rd = [x for x in d if x["caja"] == "rechazada"]
tumba = collections.Counter()
for x in rd:
    f = x.get("filas") or {}
    peor = max(f, key=lambda k: f[k]) if f else "(sin detalle)"
    tumba[peor] += 1
print(f"  rechazos: {len(rd)}")
for k, v in tumba.most_common(8):
    print(f"    {k:22s} {v:4d} = {pct(v, len(rd))}")
pa = [x["pasos"] for x in d if x.get("pasos") is not None]
par = [x["pasos"] for x in rd if x.get("pasos") is not None]
if pa:
    print(f"  distancia del destino, casillas · todas: mediana {st.median(pa)}"
          f" p90 {sorted(pa)[int(.9*(len(pa)-1))]} max {max(pa)}")
if par:
    print(f"                                 · en los rechazos: mediana "
          f"{st.median(par)} max {max(par)}")

print("\n=== M4 · O-DESPUES CON EL DESTINO A UN PASO ===")
un = [x for x in d if x.get("pasos") == 1]
cu = collections.Counter(x["caja"] for x in un)
comp1 = sum(cu[x] for x in COMPITEN)
print(f"  escenas con destino a 1 paso: {len(un)} · cajas {dict(cu)}")
print(f"  compiten {comp1} · aceptada {cu['aceptada']} = {pct(cu['aceptada'], comp1)}")
for p in (2, 3):
    up = [x for x in d if x.get("pasos") == p]
    c2 = collections.Counter(x["caja"] for x in up)
    cc = sum(c2[x] for x in COMPITEN)
    print(f"  a {p} pasos: {len(up)} escenas · compiten {cc} · aceptada "
          f"{c2['aceptada']} = {pct(c2['aceptada'], cc)}")

print("\n=== M5 · CUANTO MEJOR ESTABA DE VERDAD A LOS 100 TICS ===")
mej = [x["mejora"] for x in d if x.get("mejora") is not None]
if mej:
    print(f"  n = {len(mej):,} · mediana {st.median(mej):+.5f} · "
          f"media {sum(mej)/len(mej):+.5f} · "
          f"p10 {sorted(mej)[int(.1*(len(mej)-1))]:+.5f} · "
          f"p90 {sorted(mej)[int(.9*(len(mej)-1))]:+.5f}")
print("\n=== O-AZAR, para comparar ===")
z = D["azar"]
zz = [x for x in z if x.get("pareja_con_despues")]
c = collections.Counter(x["caja"] for x in zz)
cc = sum(c[x] for x in COMPITEN)
print(f"  todas: {len(z)} escenas · aceptada "
      f"{sum(1 for x in z if x['caja']=='aceptada')} = "
      f"{pct(sum(1 for x in z if x['caja']=='aceptada'), len(z))}")
print(f"  solo las que tambien tenian O-despues: {len(zz)} · cajas {dict(c)} · "
      f"compiten {cc} · aceptada {c['aceptada']} = {pct(c['aceptada'], cc)}")
paz = [x["pasos"] for x in z if x.get("pasos") is not None]
if paz:
    print(f"  distancia del destino: mediana {st.median(paz)} max {max(paz)}")

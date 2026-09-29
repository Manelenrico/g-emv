"""[P5-2c] Las tablas del tercer reanalisis."""
import collections, json, math, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(AQUI, "P52c_resumen.json")))
D = json.load(open(os.path.join(AQUI, "P52c_detalle.json")))
Rb = json.load(open(os.path.join(AQUI, "P52b_resumen.json")))
CAJAS = ("aceptada", "coincide", "rechazada", "vetada", "intraducible",
         "dormida", "caducada")
COMP = ("aceptada", "coincide", "rechazada")
NOM = {"ahora": "O-ahora", "despues": "O-despues", "azarp": "azar emparejado"}


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * (c - h), 100 * (c + h))


def pc(a, b):
    return f"{100.0*a/b:.2f} %" if b else "n/a"


print("=== M1 · LAS CAJAS EN LOS TRES CRITERIOS ===")
T = {}
for crit in ("estricto", "ventana", "vida"):
    print(f"\n  {crit.upper()}")
    print(f"  {'llave':17s} {'n':>6s} " + " ".join(f"{c[:8]:>9s}" for c in CAJAS)
          + f" {'compiten':>9s} {'acept':>8s} {'IC95':>15s} {'ac+coin':>9s}")
    for k in ("ahora", "despues", "azarp"):
        c = collections.Counter(R["cajas"][crit][k])
        n = sum(c.values())
        comp = sum(c[x] for x in COMP)
        lo, hi = wilson(c["aceptada"], comp)
        T[(crit, k)] = (c["aceptada"], comp, c["coincide"])
        print(f"  {NOM[k]:17s} {n:6,} " + " ".join(f"{c[x]:9,}" for x in CAJAS)
              + f" {comp:9,} {pc(c['aceptada'], comp):>8s} "
                f"{f'[{lo:.2f},{hi:.2f}]':>15s} "
                f"{pc(c['aceptada']+c['coincide'], comp):>9s}")

print("\n=== (1) EL AZAR VIEJO CONTRA EL EMPAREJADO ===")
for crit in ("estricto", "ventana"):
    v = collections.Counter(Rb["cajas"][crit]["azar"])
    nv = sum(v[x] for x in COMP)
    kk, nn, _ = T[(crit, "azarp")]
    print(f"  {crit:9s} · viejo (de los candidatos del cuerpo): "
          f"{v['aceptada']}/{nv} = {pc(v['aceptada'], nv)} · "
          f"emparejado (del mapa, misma distancia): {kk}/{nn} = {pc(kk, nn)}")

print("\n=== (4) GEMELOS ===")
for crit in ("estricto", "ventana"):
    for k in ("despues", "azarp"):
        f = [x for x in D[crit] if x["llave"] == k]
        g = sum(1 for x in f if x.get("gemelo"))
        print(f"  {crit:9s} {NOM[k]:17s}: con gemelo {g:4d} de {len(f):4d} = "
              f"{pc(g, len(f))}")
a = [x for x in D["estricto"] if x["llave"] == "ahora"]
print(f"  la regla del gemelo SOLO se aplica a O-ahora · sus cajas estrictas: "
      f"{dict(collections.Counter(x['caja'] for x in a))}")

print("\n=== M2 · TRADUCTOR CONTRA PUERTA (O-ahora, criterio estricto) ===")
mal = [x for x in a if x["caja"] in ("rechazada", "intraducible")]
puerta = [x for x in mal if x.get("nombre") == x.get("elegido_real")]
print(f"  escenas {len(a):,} · fallos {len(mal)} · del TRADUCTOR "
      f"{len(mal)-len(puerta)} · de la PUERTA {len(puerta)}")
print(f"  con la regla del gemelo, O-ahora acaba en: aceptada+coincide "
      f"{pc(T[('estricto','ahora')][0]+T[('estricto','ahora')][2], T[('estricto','ahora')][1])}")

print("\n=== M3 · QUE FILA TUMBA ===")
for crit in ("estricto", "ventana", "vida"):
    for k in ("despues", "azarp"):
        rd = [x for x in D[crit] if x["llave"] == k and x["caja"] == "rechazada"]
        t = collections.Counter()
        for x in rd:
            fl = x.get("filas") or {}
            t[max(fl, key=lambda z: fl[z]) if fl else "(sin detalle)"] += 1
        if rd:
            print(f"  {crit:9s} {NOM[k]:17s} {len(rd):4d} rechazos · " +
                  " · ".join(f"{z} {pc(v, len(rd))}" for z, v in t.most_common(3)))

print("\n=== M4 y (3) · POR DISTANCIA, CON VIDA ENTERA ===")
for k in ("despues", "azarp"):
    print(f"\n  {NOM[k]}:")
    for etq, filtro in (("1 paso", lambda p: p == 1),
                        ("2 pasos", lambda p: p == 2),
                        ("3 o mas", lambda p: p >= 3)):
        for crit in ("estricto", "ventana", "vida"):
            f = [x for x in D[crit] if x["llave"] == k
                 and x.get("pasos") is not None and filtro(x["pasos"])]
            c = collections.Counter(x["caja"] for x in f)
            cc = sum(c[x] for x in COMP)
            lo, hi = wilson(c["aceptada"], cc)
            print(f"    {etq:8s} {crit:9s} n={len(f):4d} compiten {cc:4d} "
                  f"aceptada {c['aceptada']:3d} = {pc(c['aceptada'], cc):>7s} "
                  f"IC95 [{lo:.2f},{hi:.2f}]")
        if k == "despues":
            f = [x for x in D["vida"] if x["llave"] == k
                 and x.get("pasos") is not None and filtro(x["pasos"])]
            quieto = sum(1 for x in f if x.get("sin_moverse"))
            rd = [x for x in f if x["caja"] == "rechazada"]
            t = collections.Counter()
            for x in rd:
                fl = x.get("filas") or {}
                t[max(fl, key=lambda z: fl[z]) if fl else "(sin detalle)"] += 1
            print(f"       · la mejora llego SIN MOVERSE de la casilla en "
                  f"{quieto} de {len(f)} = {pc(quieto, len(f))}")
            if rd:
                print(f"       · tumba: " + " · ".join(
                    f"{z} {pc(v, len(rd))}" for z, v in t.most_common(3)))

print("\n=== VIDA ENTERA · CUANTAS VECES GANA Y CUANDO ===")
for k in ("ahora", "despues", "azarp"):
    f = [x for x in D["vida"] if x["llave"] == k and x["caja"] == "aceptada"]
    if not f:
        continue
    g = [x["veces que gana"] for x in f]
    ed = [x["edad de la primera victoria"] for x in f
          if x["edad de la primera victoria"] is not None]
    tc = [x["tics en que compitio"] for x in D["vida"] if x["llave"] == k]
    print(f"  {NOM[k]:17s} ganan {len(f):3d} · veces que gana: mediana "
          f"{st.median(g):.0f} max {max(g)} · edad de la 1a victoria: mediana "
          f"{st.median(ed):.0f} max {max(ed)} · tics en que compite: mediana "
          f"{st.median(tc):.0f}")

print("\n=== M5 · LA MEJORA REAL ===")
mej = [x["mejora"] for x in D["estricto"]
       if x["llave"] == "despues" and x.get("mejora") is not None]
sm = [x for x in D["estricto"] if x["llave"] == "despues"
      and x.get("sin_moverse")]
print(f"  n={len(mej):,} · mediana {st.median(mej):+.5f} · media "
      f"{sum(mej)/len(mej):+.5f}")
print(f"  escenas en que el cuerpo NO se movio de su casilla en 100 tics: "
      f"{len(sm):,} de {len(mej):,} = {pc(len(sm), len(mej))}")

print("\n=== LA DIFERENCIA, EN LOS TRES CRITERIOS ===")
for crit in ("estricto", "ventana", "vida"):
    k1, n1, _ = T[(crit, "despues")]
    k2, n2, _ = T[(crit, "azarp")]
    p1, p2 = k1 / n1, k2 / n2
    d = 100 * (p1 - p2)
    se = 100 * math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    print(f"  {crit:9s} despues {100*p1:5.2f} % (n={n1}) · azar emparejado "
          f"{100*p2:5.2f} % (n={n2}) · diferencia {d:+.2f} pts · IC95 "
          f"[{d-1.96*se:+.2f},{d+1.96*se:+.2f}]")

"""[P5-8M] K2 con intervalo: vida y puesto, K contra A, por semilla emparejada.

Prueba de signos EXACTA (binomial) sobre las semillas, e intervalo de la
mediana de la diferencia por bootstrap. Las semillas estan emparejadas de
verdad: mismo mapa, mismos rivales, mismos puestos (comprobado en la tanda 3).
"""
import json, math, random, statistics as st, sys

ET = "_".join([a for a in sys.argv[1:] if not a.startswith("-")] or ["0"])
A = json.load(open(f"cantera/paper5/P58M_{ET}.json"))
K = [x for x in A if x["brazo"] == "K"]; Ar = [x for x in A if x["brazo"] == "A"]


def binom_p(k, n):
    """p a dos colas de la prueba de signos con p=0,5."""
    if n == 0: return 1.0
    c = lambda a, b: math.comb(a, b)
    lo = min(k, n - k)
    cola = sum(c(n, i) for i in range(lo + 1)) / 2.0 ** n
    return min(1.0, 2 * cola)


def boot(d, n=20000, sem=20260919):
    r = random.Random(sem)
    ms = sorted(st.median(r.choices(d, k=len(d))) for _ in range(n))
    return ms[int(.025 * n)], ms[int(.975 * n)]


for nom, campo, mejor_es in (("VIDA (tics vivo)", "vida_tics", "mas"),
                             ("PUESTO (placement)", "puesto", "menos")):
    dif = []
    for s in sorted({x["semilla"] for x in A}):
        Ks = [x[campo] for x in K if x["semilla"] == s and x[campo] is not None]
        As = [x[campo] for x in Ar if x["semilla"] == s and x[campo] is not None]
        if not Ks or not As: continue
        dif.append(st.median(Ks) - st.median(As))
    n = len(dif)
    pos = sum(1 for d in dif if d > 0); neg = sum(1 for d in dif if d < 0)
    cero = n - pos - neg
    lo, hi = boot(dif)
    kmej = pos if mejor_es == "mas" else neg
    print(f"=== K2 · {nom} · {n} semillas emparejadas ===")
    print(f"    diferencia K - A por semilla: mediana {st.median(dif):+.1f} · "
          f"IC 95 % bootstrap [{lo:+.1f}, {hi:+.1f}]")
    print(f"    K mejor en {kmej} semillas · peor en {n-kmej-cero} · igual en {cero}")
    print(f"    prueba de signos (sin los empates): p = "
          f"{binom_p(min(pos,neg), pos+neg):.3f}")
    print(f"    -> {'hay señal' if binom_p(min(pos,neg), pos+neg) < 0.05 else 'NO se distingue del azar'}")
    print()

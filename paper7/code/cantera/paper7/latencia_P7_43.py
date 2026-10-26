"""[P7-43, mesa 11-oct] CURVA DE LATENCIA POR DIA (1-20), por brazo y personalidad: mediana de ms, p95 y % de decisiones sobre el tic (media de los dos asientos; de la guarda
de cada asiento en P7_41_estado.json), y el tamano del cuaderno con el que arranco ese dia (recuerdos + apuntes de P7-40, del cuaderno del dia anterior en P7_41_res) para ver si
la curva sube con el cuaderno. -> P7_43_latencia_s1.json y tabla en pantalla.  python3 latencia_P7_43.py [--serie 1]"""
import json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); S = int(sys.argv[sys.argv.index("--serie") + 1]) if "--serie" in sys.argv else 1
E = json.load(open(os.path.join(AQUI, "P7_41_estado.json"))); VAR = ("TECHO", "BORRADO_v", "BORRADO_p", "APRENDE_v", "APRENDE_p", "SIN")
n = lambda x, d=1: ("—" if x is None else f"{x:.{d}f}".replace(".", ","))


def cuaderno_tam(var, d):
    tot = 0; ap = 0; k = 0
    for sl in (10, 11):
        f = os.path.join(AQUI, "P7_41_res", f"cuaderno_s{S}_d{d - 1}_{var}_{sl}.json")
        if not os.path.exists(f): continue
        c = json.load(open(f)); k += 1; tot += sum(len(s_) for o in c.get("objetos", {}).values() for s_ in o["situaciones"].values()); ap += len((c.get("apuntes_P7_40") or {}).get("apuntes") or [])
    return (tot / k if k else None, ap / k if k else None)


R = {}
for var in VAR:
    R[var] = {}
    for d in range(1, 21):
        p = next((p for p in E["peticiones"] if p["serie"] == S and p["dia"] == d and p["brazo"] == var and p["estado"] == "completed"), None)
        gs = [g for g in (p.get("latencia") or {}).values() if g.get("ms_mediana") is not None] if p else []
        rec, ap = cuaderno_tam(var, d) if (var.startswith("APRENDE") or var == "SIN") and d > 1 else (None, None)
        R[var][d] = {"mediana": (st.mean(g["ms_mediana"] for g in gs) if gs else None), "p95": (max(g.get("ms_p95") or 0 for g in gs) if gs else None), "sobre_pct": (100 * st.mean(g.get("sobre_el_tic") or 0 for g in gs) if gs else None), "recuerdos": rec, "apuntes": ap, "asientos": len(gs)}
# correlacion (Spearman a mano) mediana ~ recuerdos+apuntes en las cadenas
def rangos(v): s_ = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); [r.__setitem__(i, k) for k, i in enumerate(s_)]; return r
def spearman(x, y):
    if len(x) < 3: return None
    rx, ry = rangos(x), rangos(y); mx, my = st.mean(rx), st.mean(ry); num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else None
COR = {}
for var in ("APRENDE_v", "APRENDE_p", "SIN"):
    pts = [(R[var][d]["recuerdos"] + R[var][d]["apuntes"], R[var][d]["mediana"], R[var][d]["sobre_pct"]) for d in range(2, 21) if R[var][d]["mediana"] is not None and R[var][d]["recuerdos"] is not None]
    COR[var] = {"n": len(pts), "spearman_mediana_vs_cuaderno": (round(spearman([x for x, _, _ in pts], [y for _, y, _ in pts]), 2) if pts else None), "spearman_sobre_vs_cuaderno": (round(spearman([x for x, _, _ in pts], [z for _, _, z in pts]), 2) if pts else None)}
json.dump({"serie": S, "por_dia": R, "correlacion": COR}, open(os.path.join(AQUI, f"P7_43_latencia_s{S}.json"), "w"), ensure_ascii=False, indent=1)
print(f"serie {S} · mediana ms (p95) [% sobre el tic] por dia; cadenas: + recuerdos/apuntes del cuaderno con el que arranca")
for var in VAR:
    print(var.ljust(10), " ".join(f"d{d}:{n(x['mediana'])}({n(x['p95'], 0)})[{n(x['sobre_pct'], 1)}]" + (f"<{int(x['recuerdos'])}/{int(x['apuntes'])}>" if x["recuerdos"] is not None else "") for d, x in R[var].items() if x["mediana"] is not None))
print("correlacion (Spearman) mediana y % sobre el tic frente al tamano del cuaderno:", COR)

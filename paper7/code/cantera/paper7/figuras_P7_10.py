"""[P7-10] FIGURAS del campo (matplotlib, de P7_10_campo.json), por dia (1-20) y brazo, media sobre las dos series y los dos asientos:
(1) mediana de la vida al usar el botiquin; (2) creencia (cuerpo, dentro) e ignorancia (APRENDE y BORRADO); (3) usos con la vida < 50 y >= 80 por vida.
-> P7_10_fig_vida_al_usar.png, P7_10_fig_creencia.png, P7_10_fig_ignorancia.png, P7_10_fig_usos.png"""
import json, os, statistics
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__)); C = json.load(open(os.path.join(AQUI, "P7_10_campo.json")))
V = [v for v in C.values() if not v.get("sin_tics")]; BR = ("SUELO", "BORRADO", "APRENDE", "TECHO"); COL = {"SUELO": "#999999", "BORRADO": "#E69F00", "APRENDE": "#009E73", "TECHO": "#0072B2"}
def serie(b, f, agg=statistics.mean):
    xs, ys = [], []
    for d in range(1, 21):
        vals = [x for v in V if v["brazo"] == b and v["dia"] == d for x in (f(v) if isinstance(f(v), list) else [f(v)]) if x is not None]
        if vals: xs.append(d); ys.append(agg(vals))
    return xs, ys
def fig(nombre, titulo, f, brazos=BR, ylab="", agg=statistics.mean, estilo=None):
    plt.figure(figsize=(6.4, 3.6), dpi=120)
    for b in brazos:
        xs, ys = serie(b, f, agg)
        if xs: plt.plot(xs, ys, marker="o", ms=3, color=COL[b], label=b, ls=(estilo or {}).get(b, "-"))
    plt.title(titulo, fontsize=10); plt.xlabel("día"); plt.ylabel(ylab); plt.xlim(0.5, 20.5); plt.grid(alpha=0.3); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig(os.path.join(AQUI, nombre)); plt.close()
fig("P7_10_fig_vida_al_usar.png", "Vida al usar el botiquín (mediana del día, 2 series × 2 asientos)", lambda v: [u["hp0"] for u in v["usos"] if u["gastado"]], BR, "vida", statistics.median)
def cre(v):
    d = (((v.get("cuaderno") or {}).get("creencias") or {}).get("first_aid") or {}).get("dentro"); return d.get("cuerpo") if isinstance(d, dict) else None
fig("P7_10_fig_creencia.png", "Creencia del botiquín (cuerpo, dentro) al acabar el día", cre, ("BORRADO", "APRENDE"), "creencia")
fig("P7_10_fig_ignorancia.png", "Ignorancia del botiquín al acabar el día", lambda v: (v.get("cuaderno") or {}).get("ignorancia"), ("BORRADO", "APRENDE"), "ignorancia")
plt.figure(figsize=(6.4, 3.6), dpi=120)
for b in BR:
    xs, ys = serie(b, lambda v: sum(1 for u in v["usos"] if u["gastado"] and u["hp0"] < 50)); plt.plot(xs, ys, marker="v", ms=3, color=COL[b], label=f"{b} vida < 50")
    xs, ys = serie(b, lambda v: sum(1 for u in v["usos"] if u["gastado"] and u["hp0"] >= 80)); plt.plot(xs, ys, marker="^", ms=3, color=COL[b], ls=":", label=f"{b} vida ≥ 80")
plt.title("Usos del botiquín por vida, con la vida baja (< 50) y alta (≥ 80)", fontsize=10); plt.xlabel("día"); plt.ylabel("usos por vida"); plt.xlim(0.5, 20.5); plt.grid(alpha=0.3); plt.legend(fontsize=6, ncol=2); plt.tight_layout(); plt.savefig(os.path.join(AQUI, "P7_10_fig_usos.png")); plt.close()
print("figuras escritas")

"""[P7-8] FIGURAS del campo (matplotlib, de P7_8_campo.json): por dia (1-20), con los cuatro brazos, media sobre las dos series y los dos asientos:
(1) ignorancia del botiquin al acabar el dia (APRENDE y BORRADO); (2) usos con la vida a 80 o mas por vida; (3) usos con la vida bajo 50 por vida;
(4) proporcion de usos fuera del circulo. -> P7_8_fig_ignorancia.png, P7_8_fig_usos_alta.png, P7_8_fig_usos_baja.png, P7_8_fig_fuera.png"""
import json, os, statistics, collections
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
AQUI = os.path.dirname(os.path.abspath(__file__)); C = json.load(open(os.path.join(AQUI, "P7_8_campo.json")))
V = [v for v in C.values() if not v.get("sin_tics")]; BR = ("SUELO", "BORRADO", "APRENDE", "TECHO"); COL = {"SUELO": "#999999", "BORRADO": "#E69F00", "APRENDE": "#009E73", "TECHO": "#0072B2"}
def serie(b, f):
    xs, ys = [], []
    for d in range(1, 21):
        vals = [f(v) for v in V if v["brazo"] == b and v["dia"] == d]; vals = [x for x in vals if x is not None]
        if vals: xs.append(d); ys.append(statistics.mean(vals))
    return xs, ys
def fig(nombre, titulo, f, brazos=BR, ylab=""):
    plt.figure(figsize=(6.4, 3.6), dpi=120)
    for b in brazos:
        xs, ys = serie(b, f)
        if xs: plt.plot(xs, ys, marker="o", ms=3, color=COL[b], label=b)
    plt.title(titulo, fontsize=10); plt.xlabel("día"); plt.ylabel(ylab); plt.xlim(0.5, 20.5); plt.grid(alpha=0.3); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig(os.path.join(AQUI, nombre)); plt.close()
fig("P7_8_fig_ignorancia.png", "Ignorancia del botiquín al acabar el día (media de 2 series × 2 asientos)", lambda v: (v.get("cuaderno") or {}).get("ignorancia"), ("BORRADO", "APRENDE"), "ignorancia")
fig("P7_8_fig_usos_alta.png", "Usos del botiquín con la vida ≥ 80, por vida", lambda v: sum(1 for u in v["usos"] if u["gastado"] and u["hp0"] >= 80), BR, "usos por vida")
fig("P7_8_fig_usos_baja.png", "Usos del botiquín con la vida < 50, por vida", lambda v: sum(1 for u in v["usos"] if u["gastado"] and u["hp0"] < 50), BR, "usos por vida")
def prop_fuera(v):
    us = [u for u in v["usos"] if u["gastado"]]; return (sum(1 for u in us if u["situacion"] == "fuera") / len(us)) if us else None
fig("P7_8_fig_fuera.png", "Proporción de usos fuera del círculo (vidas con algún uso)", prop_fuera, BR, "proporción")
print("figuras escritas")

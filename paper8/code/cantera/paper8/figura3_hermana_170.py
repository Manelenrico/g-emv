"""[P8] Prompt 170, figura 3: después de perder a la hermana. Del sexto sellado (valle_experimento_v6), la criatura completa (RG69r+voz). Eje horizontal: días
desde la muerte de la hermana, de −5 a +15 (0, el día de la muerte).
  Arriba: el duelo y la soledad de los 136 casos, y la soledad de sus 378 controles. Son las cuentas de la figura del 161/162 (figuras_v6_161.trazos,
  importada sin cambios: duelo = S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO, soledad = S-SOLEDAD, media de los turnos despierta de cada día, de
  filas.jsonl.gz; casos y controles con las reglas de la medida sellada A2, duelo_soledad_v6.casos_de).
  Abajo: la parte del día (mañana y tarde) pegada a una vecina, casos y controles. La definición es la de la medida sellada A2 (anadidas_v6.una): pegada =
  alguna criatura de otra casa a una casilla o menos (balance.jsonl.gz, las posiciones de cada turno), sobre todos los turnos de día de ese día. Aquí, día a día.
  Comprobación: con las ventanas de A2 (los 5 días antes y los 5 después, sumando turnos) tiene que dar el 10 % → 27 % de los casos y el 9 % → 9 % de los
  controles de informe_experimento_v6.md (redondeado a enteros); si no, para.
  Cada línea, la media de los casos (o controles) con dato ese día, y su banda del 95 % (E6.boot sobre los de ese día).
   python3 figura3_hermana_170.py -> figuras/fig3_hermana.png, .pdf y .txt"""
import gzip, json, os, sys
from collections import defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_170 as S
import figuras_v6_161 as F
import medidas_v6 as MV
DS, E6, plt, boot, DIA = F.DS, S.E6, S.plt, S.boot, S.DIA
NOM = "fig3_hermana"; DIAS = list(range(-5, 16))
assert DS.EXP == E6.EXP and os.path.basename(DS.EXP) == "valle_experimento_v6" and MV.DIA == DIA


def una(x):
    """las cuentas del 161 (duelo y soledad por caso y control) y, para los mismos, la parte de cada día pegada a una vecina (de día)"""
    out = F.trazos(x); mu, s = x; n = f"{F.PROTA}_{mu}+sabores_s{s}_d40"; D = defaultdict(lambda: [0, 0])     # (criatura, día) -> [turnos de día, pegada]
    for l in gzip.open(os.path.join(DS.EXP, n, "balance.jsonl.gz"), "rt", encoding="utf-8"):
        x_ = json.loads(l); t = x_["t"]
        if MV.fase(t) in ("anochecer", "noche"): continue
        c = x_["c"]
        for a, r in c.items():
            vec = any(b[0] != a[0] and max(abs(q[3] - r[3]), abs(q[4] - r[4])) <= 1 for b, q in c.items())
            z = D[(a, t // DIA)]; z[0] += 1; z[1] += vec
    for g in ("casos", "control"):
        for c in out[g]:
            a, dm = c["a"], c["dia"]
            c["vecina"] = [D[(a, d)][1] / D[(a, d)][0] if D.get((a, d)) and D[(a, d)][0] else None for d in range(dm - 5, dm + 16)]
            ven = lambda d0, d1: (sum(D[(a, d)][1] for d in range(d0, d1) if (a, d) in D), sum(D[(a, d)][0] for d in range(d0, d1) if (a, d) in D))
            c["a2_antes"], c["a2_despues"] = ven(dm - 5, dm), ven(dm + 1, dm + 6)
    return out


if __name__ == "__main__":
    with Pool(8) as p: TR = p.map(una, DS.candidatas())
    Z = {g: [c for r in TR for c in r[g]] for g in ("casos", "control")}; nc, nk = len(Z["casos"]), len(Z["control"])
    assert (nc, nk) == (136, 378), (nc, nk)
    # la comprobación con A2 (informe_experimento_v6.md: pegada a una vecina, de día: 10 % → 27 % y 9 % → 9 %)
    a2 = {g: tuple(100 * sum(c[k][1] and c[k][0] / c[k][1] for c in Z[g] if c[k][1]) / sum(1 for c in Z[g] if c[k][1]) for k in ("a2_antes", "a2_despues")) for g in Z}
    assert tuple(round(x) for x in a2["casos"]) == (10, 27) and tuple(round(x) for x in a2["control"]) == (9, 9), a2
    B = {}
    for k, g in (("duelo", "casos"), ("soledad", "casos"), ("soledad", "control"), ("vecina", "casos"), ("vecina", "control")):
        esc = 100 if k == "vecina" else 1
        B[(k, g)] = [boot([esc * c[k][i] for c in Z[g] if c[k][i] is not None]) for i in range(len(DIAS))]
    npor = {g: [sum(1 for c in Z[g] if c["duelo"][i] is not None) for i in range(len(DIAS))] for g in Z}
    S.estilo(); fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    LIN = ((axs[0], "duelo", "casos", "#6250d6", "-", f"duelo, las que pierden a su hermana ({nc})"),
           (axs[0], "soledad", "casos", "#e87ba4", "-", f"soledad, las que pierden a su hermana ({nc})"),
           (axs[0], "soledad", "control", "#e87ba4", "--", f"soledad, las que la conservan ({nk})"),
           (axs[1], "vecina", "casos", "#52514e", "-", f"las que pierden a su hermana ({nc})"),
           (axs[1], "vecina", "control", "#52514e", "--", f"las que la conservan ({nk})"))
    for ax, k, g, col, ls, rot in LIN:
        b = B[(k, g)]; ax.fill_between(DIAS, [x["lo"] for x in b], [x["hi"] for x in b], color=col, alpha=0.2, linewidth=0)
        ax.plot(DIAS, [x["media"] for x in b], color=col, linestyle=ls, linewidth=2.2, label=rot)
    for ax in axs:
        ax.axvline(0, color="#333333", linewidth=1, linestyle=":"); ax.set_ylim(bottom=0); ax.grid(axis="y", color=S.REJILLA, linewidth=0.8)

    axs[0].legend(frameon=False, fontsize=12, loc="upper right"); axs[1].legend(frameon=False, fontsize=12, loc="upper left")
    axs[0].set_ylabel("peso, media de los turnos\ndespierta del día"); axs[1].set_ylabel("parte del día pegada\na una vecina (%)")
    axs[1].set_xlabel("días desde la muerte de la hermana (0, el día de la muerte)"); axs[1].set_xticks(DIAS); axs[1].set_xlim(-5, 15)
    axs[0].set_title("el duelo y la soledad", loc="left", fontsize=15); axs[1].set_title("con las vecinas", loc="left", fontsize=15)
    axs[1].set_ylim(0, max(x["hi"] for b in (B[("vecina", "casos")], B[("vecina", "control")]) for x in b) * 1.25)
    fig.tight_layout(); S.guarda(fig, NOM)
    # la comparación con lo que dibujó el 162 (duelo y soledad): los mismos números
    V2 = json.load(open(os.path.join(AQUI, "salida", "figuras_v6_v2_162.json"), encoding="utf-8"))["C_duelo_soledad"]
    dif = [(k, g) for k, g in (("duelo", "casos"), ("soledad", "casos"), ("soledad", "control")) if any(abs(a["media"] - b["media"]) > 1e-12 for a, b in zip(B[(k, g)], V2[f"{k}|{g}"]))]
    assert not dif, dif
    t = ["| día | n casos | n controles | duelo, casos | soledad, casos | soledad, controles | pegada a una vecina (%), casos | controles |", "|---|---|---|---|---|---|---|---|"]
    for i, d in enumerate(DIAS):
        t.append(f"| {d:+d} | {npor['casos'][i]} | {npor['control'][i]} | " + " | ".join(S.fb(B[k][i], S.f3 if k[0] != "vecina" else S.f1) for k in
                 (("duelo", "casos"), ("soledad", "casos"), ("soledad", "control"), ("vecina", "casos"), ("vecina", "control"))) + " |")
    S.escribe_txt(NOM, ["# Figura 3, después de perder a la hermana", "",
        f"Programa: figura3_hermana_170.py. Datos: la criatura completa en el sexto sellado (valle_experimento_v6), {len(TR)} partidas con algún caso. {nc} casos (las que pierden a su hermana el día 5 o después y viven 5 días más) y {nk} controles (las de otra casa de la misma partida que conservan a la suya esos días).", "",
        "## Los números (media [intervalo del 95 %]; día 0, el de la muerte)", ""] + t + ["",
        f"El duelo y la soledad coinciden número a número con la figura del prompt 162 (comprobado). La parte pegada a una vecina, con las ventanas de A2 (5 días antes y 5 después, sumando turnos): casos {S.f1(a2['casos'][0])} % → {S.f1(a2['casos'][1])} %, controles {S.f1(a2['control'][0])} % → {S.f1(a2['control'][1])} % (A2: 10 % → 27 % y 9 % → 9 %).", "",
        "## De dónde sale", "",
        "- Casos y controles: la medida sellada A2 (anadidas_v6.py; duelo_soledad_v6.casos_de), informe_experimento_v6.md:162-172 (136 frente a 378).",
        "- El duelo y la soledad por día: figuras_v6_161.trazos (filas.jsonl.gz: S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO y S-SOLEDAD, media de los turnos despierta), informe_prompt_161.md e informe_prompt_162.md (la figura v6_C_duelo_soledad_v2).",
        "- Pegada a una vecina: la definición de A2 (anadidas_v6.py:43-46: otra criatura de otra casa a una casilla o menos), aquí por día y solo de día (mañana y tarde); informe_experimento_v6.md:169 da las ventanas (10 % → 27 %).",
        "- Bandas: bootstrap de 10.000 remuestreos con semilla 8 sobre los casos (o controles) con dato ese día (evalua_experimento_v6.boot). Desde el día +1 hay menos casos cada día, porque algunas mueren o acaba la partida (columna n).", "",
        "## Pie propuesto", "",
        "«Lo que le pasa a la criatura cuando muere su hermana, del quinto día antes al decimoquinto después, en 136 casos del experimento sellado. Arriba, el duelo, que escribimos nosotros, "
        "salta el día de la muerte y baja despacio, sin volver a lo de antes; la soledad sube y se queda arriba, mientras que en las 378 que conservan a su hermana no se mueve. Abajo, sin ninguna regla que la mande, "
        "pasa de día casi el triple de tiempo pegada a una vecina en los cinco días siguientes, y algo más después.»"])
    print("hecho", nc, nk, a2)

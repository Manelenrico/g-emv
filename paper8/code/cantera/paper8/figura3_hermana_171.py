"""[P8] Prompt 171, figura 3 pulida: la de figura3_hermana_170.py (sus cuentas, F0.una, importadas sin cambios, con sus mismas comprobaciones: 136 y 378,
A2 10 → 27 % y 9 → 9 %) con el mismo tamaño; solo cambian la coma decimal de los ejes y que los textos salen de rotulos_figuras.csv (estilo_171). Comprueba
que la tabla de números es la del .txt del 170.
   python3 figura3_hermana_171.py [--idioma es] -> figuras_171/fig3_hermana_es.png y .pdf"""
import os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_171 as S
import figura3_hermana_170 as F0
plt, boot, DIAS, NOM = S.plt, S.boot, F0.DIAS, F0.NOM


if __name__ == "__main__":
    ID = S.idioma(); R = S.Rotulos(ID); R.comprueba(("fig3.", "separador"))
    with Pool(8) as p: TR = p.map(F0.una, F0.DS.candidatas())
    Z = {g: [c for r in TR for c in r[g]] for g in ("casos", "control")}; nc, nk = len(Z["casos"]), len(Z["control"])
    assert (nc, nk) == (136, 378), (nc, nk)
    a2 = {g: tuple(100 * sum(c[k][1] and c[k][0] / c[k][1] for c in Z[g] if c[k][1]) / sum(1 for c in Z[g] if c[k][1]) for k in ("a2_antes", "a2_despues")) for g in Z}
    assert tuple(round(x) for x in a2["casos"]) == (10, 27) and tuple(round(x) for x in a2["control"]) == (9, 9), a2
    B = {}
    for k, g in (("duelo", "casos"), ("soledad", "casos"), ("soledad", "control"), ("vecina", "casos"), ("vecina", "control")):
        esc = 100 if k == "vecina" else 1
        B[(k, g)] = [boot([esc * c[k][i] for c in Z[g] if c[k][i] is not None]) for i in range(len(DIAS))]
    npor = {g: [sum(1 for c in Z[g] if c["duelo"][i] is not None) for i in range(len(DIAS))] for g in Z}
    S.estilo(); fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    LIN = ((axs[0], "duelo", "casos", "#6250d6", "-", R("fig3.duelo_casos", n=nc)), (axs[0], "soledad", "casos", "#e87ba4", "-", R("fig3.soledad_casos", n=nc)),
           (axs[0], "soledad", "control", "#e87ba4", "--", R("fig3.soledad_control", n=nk)),
           (axs[1], "vecina", "casos", "#52514e", "-", R("fig3.vecina_casos", n=nc)), (axs[1], "vecina", "control", "#52514e", "--", R("fig3.vecina_control", n=nk)))
    for ax, k, g, col, ls, rot in LIN:
        b = B[(k, g)]; ax.fill_between(DIAS, [x["lo"] for x in b], [x["hi"] for x in b], color=col, alpha=0.2, linewidth=0)
        ax.plot(DIAS, [x["media"] for x in b], color=col, linestyle=ls, linewidth=2.2, label=rot)
    for ax in axs:
        ax.axvline(0, color="#333333", linewidth=1, linestyle=":"); ax.set_ylim(bottom=0); ax.grid(axis="y", color=S.REJILLA, linewidth=0.8)
    axs[0].legend(frameon=False, fontsize=12, loc="upper right"); axs[1].legend(frameon=False, fontsize=12, loc="upper left")
    axs[0].set_ylabel(R("fig3.eje_y_arriba")); axs[1].set_ylabel(R("fig3.eje_y_abajo"))
    axs[1].set_xlabel(R("fig3.eje_x")); axs[1].set_xticks(DIAS); axs[1].set_xlim(-5, 15)
    axs[0].set_title(R("fig3.titulo_arriba"), loc="left", fontsize=15); axs[1].set_title(R("fig3.titulo_abajo"), loc="left", fontsize=15)
    axs[1].set_ylim(0, max(x["hi"] for b in (B[("vecina", "casos")], B[("vecina", "control")]) for x in b) * 1.25)
    S.decimales(R, *axs)
    fig.tight_layout(); rutas = S.guarda(fig, NOM, ID)
    t = []
    for i, d in enumerate(DIAS):
        t.append(f"| {d:+d} | {npor['casos'][i]} | {npor['control'][i]} | " + " | ".join(S.fb(B[k][i], S.f3 if k[0] != "vecina" else S.f1) for k in
                 (("duelo", "casos"), ("soledad", "casos"), ("soledad", "control"), ("vecina", "casos"), ("vecina", "control"))) + " |")
    n = S.comprueba_tabla(NOM, t); print("hecho", rutas, "filas iguales al 170:", n)

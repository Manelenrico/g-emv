"""[P8] Prompt 171, figura 4 pulida: la de figura4_costumbres_170.py (sus cuentas, F0.una, importadas sin cambios, con sus comprobaciones: 31,97 · 2,98 y 7,0 %)
con el mismo tamaño; solo cambian la coma decimal de los ejes y que los textos salen de rotulos_figuras.csv (estilo_171). Comprueba que las tablas de números
son las del .txt del 170.
   python3 figura4_costumbres_171.py [--idioma es] -> figuras_171/fig4_costumbres_es.png y .pdf"""
import os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_171 as S
import figura4_costumbres_170 as F0
plt, MUNDOS, SEM, JUG, NOM, SEQ = S.plt, S.MUNDOS, S.SEM, F0.JUG, F0.NOM, F0.SEQ


if __name__ == "__main__":
    ID = S.idioma(); R = S.Rotulos(ID); R.comprueba(("fig4.", "mundo.", "jug.", "separador"))
    T = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]; assert all(S.E6.hecho(*x) for x in T)
    with Pool(8) as p: Rr = dict(p.map(F0.una, T, chunksize=4))
    h30 = {(v, mu): [Rr[(v, mu, s)]["h30"] for s in SEM] for v in JUG for mu in MUNDOS}
    noc = {(v, mu): [100 * Rr[(v, mu, s)]["nf"] / Rr[(v, mu, s)]["nt"] for s in SEM if Rr[(v, mu, s)]["nt"]] for v in JUG for mu in MUNDOS}
    jun = {v: {"h30": sum(Rr[(v, mu, s)]["h30"] for mu in SEQ for s in SEM) / (len(SEQ) * len(SEM)),
               "noches": 100 * sum(Rr[(v, mu, s)]["nf"] for mu in SEQ for s in SEM) / sum(Rr[(v, mu, s)]["nt"] for mu in SEQ for s in SEM)} for v in JUG}
    assert round(jun["RG68r"]["h30"], 2) == 31.97 and round(jun["RG69rvoz"]["h30"], 2) == 2.98 and round(jun["RG69rvoz"]["noches"], 1) == 7.0, jun
    S.estilo(); fig, axs = plt.subplots(1, 2, figsize=(18, 6.4)); OUT = {}; rot = {v: R(f"jug.{v}") for v in JUG}
    for ax, (k, val, eje) in zip(axs, (("h30", h30, R("fig4.eje_y_hambre")), ("noches", noc, R("fig4.eje_y_noches")))):
        OUT[k] = S.barras(ax, val, JUG, rot, 0.26, R); ax.set_ylabel(eje); ax.set_ylim(bottom=0); ax.tick_params(axis="x", labelrotation=20)
    axs[0].set_title(R("fig4.titulo_hambre"), loc="left", fontsize=15); axs[1].set_title(R("fig4.titulo_noches"), loc="left", fontsize=15)
    S.decimales(R, *axs)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=14, loc="upper center", ncol=3)
    fig.tight_layout(rect=(0, 0, 1, 0.92)); rutas = S.guarda(fig, NOM, ID)
    n = S.comprueba_tabla(NOM, S.tabla_barras(OUT["h30"], JUG, S.S0.ROT) + S.tabla_barras(OUT["noches"], JUG, S.S0.ROT, S.f1))
    print("hecho", rutas, "filas iguales al 170:", n)

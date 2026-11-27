"""[P8] Prompt 171, figura 2 pulida: la de figura2_vivas_170.py con los mismos datos y el mismo tamaño; solo cambian la coma decimal de los ejes y que los
textos salen de rotulos_figuras.csv (estilo_171). Comprueba que la tabla de números es la del .txt del 170.
   python3 figura2_vivas_171.py [--idioma es] -> figuras_171/fig2_vivas_es.png y .pdf"""
import os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_171 as S
import figura2_vivas_170 as F0
plt, MUNDOS, SEM, JUG, NOM = S.plt, S.MUNDOS, S.SEM, F0.JUG, F0.NOM


if __name__ == "__main__":
    ID = S.idioma(); R = S.Rotulos(ID); R.comprueba(("fig2.", "mundo.", "jug.", "separador"))
    T = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]; assert all(S.E6.hecho(*x) for x in T)
    with Pool(8) as p: Rr = dict(p.map(F0.una, T, chunksize=10))
    val = {(v, mu): [Rr[(v, mu, s)] for s in SEM] for v in JUG for mu in MUNDOS}
    S.estilo(); fig, ax = plt.subplots(figsize=(11, 5.8))
    out = S.barras(ax, val, JUG, {v: R(f"jug.{v}") for v in JUG}, 0.26, R); ax.set_ylabel(R("fig2.eje_y")); ax.set_ylim(0, 8.6); S.decimales(R, ax)
    ax.legend(frameon=False, fontsize=13, loc="upper right", ncol=3, bbox_to_anchor=(1, 1.12)); fig.tight_layout(); rutas = S.guarda(fig, NOM, ID)
    n = S.comprueba_tabla(NOM, S.tabla_barras(out, JUG, S.S0.ROT)); print("hecho", rutas, "filas iguales al 170:", n)

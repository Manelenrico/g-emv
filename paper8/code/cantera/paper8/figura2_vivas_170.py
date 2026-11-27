"""[P8] Prompt 170, figura 2: cuántas viven. Vivas el día 40 (de 8) en los cinco mundos, en el sexto sellado (valle_experimento_v6, semillas 30161-30200,
40 días): la criatura completa (RG69r+voz), el tonto y el recolector. La medida es la pieza sellada cierre_v46 (evalua_experimento_v6.c46: 8 menos las muertes
de fin.json), la misma de la figura del 162 (figuras_v6_v2_162.py). Media de las 40 semillas con su intervalo del 95 % (E6.boot). Al acabar compara cada media
con la del 162 (salida/figuras_v6_v2_162.json); si alguna no coincide, para.
   python3 figura2_vivas_170.py -> figuras/fig2_vivas.png, .pdf y .txt"""
import json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_170 as S
E6, plt, MUNDOS, SEM = S.E6, S.plt, S.MUNDOS, S.SEM
JUG = ("RG69rvoz", "tonto", "recolector"); NOM = "fig2_vivas"
assert os.path.basename(E6.EXP) == "valle_experimento_v6" and all(E6.CARPETA[v] == E6.EXP for v in JUG)


def una(x): return (x, E6.c46(x)["vivas"])


if __name__ == "__main__":
    T = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]; assert all(E6.hecho(*x) for x in T)
    with Pool(8) as p: R = dict(p.map(una, T, chunksize=10))
    val = {(v, mu): [R[(v, mu, s)] for s in SEM] for v in JUG for mu in MUNDOS}
    S.estilo(); fig, ax = plt.subplots(figsize=(11, 5.8))
    out = S.barras(ax, val, JUG, S.ROT, 0.26); ax.set_ylabel("vivas el día 40 (de 8)"); ax.set_ylim(0, 8.6)
    ax.legend(frameon=False, fontsize=13, loc="upper right", ncol=3, bbox_to_anchor=(1, 1.12)); fig.tight_layout(); S.guarda(fig, NOM)
    V2 = json.load(open(os.path.join(AQUI, "salida", "figuras_v6_v2_162.json"), encoding="utf-8"))["A_vivas"]
    dif = [(v, mu) for v in JUG for mu in MUNDOS if abs(V2[v][mu]["media"] - out[v][mu]["media"]) > 1e-12 or abs(V2[v][mu]["lo"] - out[v][mu]["lo"]) > 1e-12]
    assert not dif, dif
    S.escribe_txt(NOM, ["# Figura 2, cuántas viven", "",
        "Programa: figura2_vivas_170.py. Datos: el sexto sellado (valle_experimento_v6), 40 partidas por mundo y jugador (semillas 30161-30200), 40 días.", "",
        "## Los números (vivas el día 40, de 8: media de las 40 partidas [intervalo del 95 %])", ""] + S.tabla_barras(out, JUG, S.ROT) + ["",
        f"Partidas por barra: 40. Todas las medias e intervalos coinciden con los de la figura del prompt 162 (salida/figuras_v6_v2_162.json, comprobado: 0 diferencias).", "",
        "## De dónde sale", "",
        "- La medida: la pieza sellada cierre_v46 (evalua_experimento_v6.c46): 8 menos las muertes apuntadas en fin.json.",
        "- Los mismos números, en informe_experimento_v6.md (la tabla de vivas por mundo y clase) e informe_prompt_162.md (la figura de vivas del v6).",
        "- El intervalo: bootstrap de 10.000 remuestreos con semilla 8 sobre las 40 partidas (evalua_experimento_v6.boot).", "",
        "## Pie propuesto", "",
        "«Criaturas vivas el día 40, de las ocho de cada aldea, en los cinco mundos: la criatura completa, el tonto y el recolector. Cada barra es la media de 40 partidas, "
        "con su intervalo del 95 %. En la abundancia y en el mundo normal llegan casi todas con cualquiera de los tres. En la sequía la criatura vive más que el tonto y algo menos que el recolector (7,8 frente a 8,0); "
        "en la sequía dura y con las bestias que crían, más que los dos.»"])
    for v in JUG: print(v, {mu: round(out[v][mu]["media"], 2) for mu in MUNDOS})

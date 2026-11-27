"""[P8] Prompt 170, figura 4: las dos costumbres, antes y después. Del sexto sellado (valle_experimento_v6, semillas 30161-30200), la criatura de antes (RG68r),
la gemela (RG068r, la que no siente lo que gana) y la criatura completa (RG69r+voz). Dos paneles, con las medidas y los días del texto (sección 5), que son las
de las apuestas selladas P24/P29 y P28 del v6 (evalua_experimento_v6.nuevas, de donde se toman las dos piezas tal cual):
  (1) los turnos al día despierta con hambre de más de 30 y comida en la bolsa, días 1 a 10 (extrae_hg_v1: suma de los días con turnos / esos días);
  (2) las noches al raso, días 1 a 10 (analiza_vc1, «noches10»: noches dormidas fuera / noches), aquí por partida, en %.
Media de las 40 partidas de cada mundo con su intervalo del 95 % (E6.boot). Para unir con el texto, se dan también las dos sequías juntas como las cuentan
P29 y P28 (la media de las 80 partidas; las noches, sumadas). Comprueba que salen 31,97 y 2,98 (P29) y 7,0 % (P28); si no, para.
   python3 figura4_costumbres_170.py -> figuras/fig4_costumbres.png, .pdf y .txt"""
import json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_170 as S
E6, plt, MUNDOS, SEM, boot = S.E6, S.plt, S.MUNDOS, S.SEM, S.boot
JUG = ("RG68r", "RG068r", "RG69rvoz"); NOM = "fig4_costumbres"; SEQ = ("sequia", "sequia_dura")
assert os.path.basename(E6.EXP) == "valle_experimento_v6" and all(E6.CARPETA[v] == E6.EXP for v in JUG) and all(E6.AN.CARP[v][0] == E6.EXP for v in JUG), E6.AN.CARP


def una(x):
    """las dos piezas de evalua_experimento_v6.nuevas (líneas 80-83), sin lo demás"""
    v, mu, s = x; a = json.load(open(E6.AN.una(x))); E6.X.EXP = E6.CARPETA[v]; h = json.load(open(E6.X.una(x)))
    cd = max(1, sum(1 for z in h["dias"] if z["turnos"])); nf, nt = a["noches10"]
    return x, {"h30": sum(z["h30_bolsa"] for z in h["dias"]) / cd, "nf": nf, "nt": nt}


if __name__ == "__main__":
    T = [(v, mu, s) for v in JUG for mu in MUNDOS for s in SEM]; assert all(E6.hecho(*x) for x in T)
    with Pool(8) as p: R = dict(p.map(una, T, chunksize=4))
    h30 = {(v, mu): [R[(v, mu, s)]["h30"] for s in SEM] for v in JUG for mu in MUNDOS}
    noc = {(v, mu): [100 * R[(v, mu, s)]["nf"] / R[(v, mu, s)]["nt"] for s in SEM if R[(v, mu, s)]["nt"]] for v in JUG for mu in MUNDOS}
    # las dos sequías juntas, como P29 y P28
    jun = {v: {"h30": sum(R[(v, mu, s)]["h30"] for mu in SEQ for s in SEM) / (len(SEQ) * len(SEM)),
               "noches": 100 * sum(R[(v, mu, s)]["nf"] for mu in SEQ for s in SEM) / sum(R[(v, mu, s)]["nt"] for mu in SEQ for s in SEM)} for v in JUG}
    assert round(jun["RG68r"]["h30"], 2) == 31.97 and round(jun["RG69rvoz"]["h30"], 2) == 2.98 and round(jun["RG69rvoz"]["noches"], 1) == 7.0, jun
    S.estilo(); fig, axs = plt.subplots(1, 2, figsize=(18, 6.4)); OUT = {}
    for ax, (k, val, eje) in zip(axs, (("h30", h30, "turnos al día con hambre y comida\nen la bolsa (días 1 a 10)"), ("noches", noc, "noches al raso, días 1 a 10 (%)"))):
        OUT[k] = S.barras(ax, val, JUG, S.ROT, 0.26); ax.set_ylabel(eje); ax.set_ylim(bottom=0); ax.tick_params(axis="x", labelrotation=20)
    axs[0].set_title("pasar hambre con comida encima", loc="left", fontsize=15); axs[1].set_title("dormir fuera de casa", loc="left", fontsize=15)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=14, loc="upper center", ncol=3)
    fig.tight_layout(rect=(0, 0, 1, 0.92)); S.guarda(fig, NOM)
    fp = lambda x: S.f1(x)
    S.escribe_txt(NOM, ["# Figura 4, las dos costumbres, antes y después", "",
        "Programa: figura4_costumbres_170.py. Datos: el sexto sellado (valle_experimento_v6), 40 partidas por mundo y jugador (semillas 30161-30200). Días 1 a 10 (los días 0 a 9 de los programas).", "",
        "## Panel 1: turnos al día despierta con hambre de más de 30 y comida en la bolsa (media [intervalo del 95 %])", ""] + S.tabla_barras(OUT["h30"], JUG, S.ROT) + ["",
        "## Panel 2: noches al raso, en % de las noches (media por partida [intervalo del 95 %])", ""] + S.tabla_barras(OUT["noches"], JUG, S.ROT, S.f1) + ["",
        "## Las dos sequías juntas, como en las apuestas", "",
        "| | " + " | ".join(S.ROT[v] for v in JUG) + " |", "|---|---|---|---|",
        "| hambre con comida en la bolsa (media de 80 partidas) | " + " | ".join(S.f2(jun[v]["h30"]) for v in JUG) + " |",
        "| noches al raso (sumadas, %) | " + " | ".join(fp(jun[v]["noches"]) for v in JUG) + " |", "",
        "Comprobado: 31,97 y 2,98 son los de P29, y el 7,0 % de la criatura completa es el de P28 (informe_experimento_v6.md:13-14 y :96-98).", "",
        "## De dónde sale", "",
        "- Las medidas: las de las apuestas selladas del v6 P24, P29 (extrae_hg_v1, «h30_bolsa») y P28 (analiza_vc1, «noches10»), por evalua_experimento_v6.nuevas (líneas 80-83).",
        "- Ojo con el texto: «unos treinta turnos» y «su gemela, cinco» (sección 5) son del primer sellado (v5, semillas 30121-30140: informe_hambre_ganancias_v1.md:21), "
        "y «una de cada cuatro noches» y «su gemela, una de cada veinte» también (informe_dormir_fuera_v5.md:200). La figura es del sexto sellado, el único con las tres; "
        "por eso sus números no son exactamente esos. «De treinta y dos al día a tres» y «de una de cada cuatro a una de cada catorce» sí son de este sellado (P29 y P28); "
        "pero en P28 la de antes es RG69r (con la reserva y sin la voz, 24,2 %), no RG68r.",
        "- El intervalo: bootstrap de 10.000 remuestreos con semilla 8 sobre las 40 partidas (evalua_experimento_v6.boot). En el panel 2, cada partida pesa igual (no se suman las noches).", "",
        "## Pie propuesto", "",
        "«Las dos costumbres sin sentido de la criatura de antes y lo que pasó al arreglarlas, en los diez primeros días de cada partida. A la izquierda, los turnos al día que pasa despierta, "
        "con hambre y con comida en la bolsa; a la derecha, las noches que duerme al raso. La gemela, que no siente lo que gana, casi no tiene ninguna de las dos; la criatura completa, con la reserva "
        "y la voz de ir a casa, las pierde las dos. Cada barra es la media de 40 partidas, con su intervalo del 95 %.»"])
    for k in OUT: print(k, {v: {mu: round(OUT[k][v][mu]["media"], 2) for mu in MUNDOS} for v in JUG})
    print(jun)

"""[P8] Prompt 170, figura 5: las tres maneras de decidir. Cuatro paneles, cinco mundos y tres barras por mundo (decide con el motor = RG69r+voz, del
valle_experimento_v6; decide sumando = S69+voz y decide con la posición = P69+voz, de valle_escalera_v6; semillas 30161-30200, 40 días), con los valores por
partida ya calculados sobre esas 600 partidas selladas:
  (1) empujones al día en los diez primeros días: la caché del prompt 156 (felicidad_dia_a_dia/partidas.json, «emp»: los empujones de cada día, como
      cierre_v46), media de los días 1 a 10 (índices 0 a 9) de cada partida, la misma cuenta que la tabla «1-10» del 157;
  (2) felicidad de la aldea, de 0 a 100: la del 167 (salida/vara_sumas_167.json, «todas|feliz»), que se comprueba igual a la de la figura escalera_C_felicidad
      (salida/figuras_escalera_paper8.json) hasta 1e-9;
  (3) total de los tres balances: «todas|suma» del 167 (media por turno despierta de cuerpo + recursos + vínculo, la aldea = media de sus criaturas);
  (4) balance más bajo de los tres: «todas|bajo» del 167 (media por turno despierta del menor de los tres).
Media de las 40 partidas con su intervalo del 95 % (E6.boot). En (4) hay medias por debajo de cero: el eje baja de cero y el cero va marcado.
   python3 figura5_tres_maneras_170.py -> figuras/fig5_tres_maneras.png, .pdf y .txt"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_170 as S
plt, MUNDOS, SEM = S.plt, S.MUNDOS, S.SEM
JUG = ("RG69rvoz", "S69voz", "P69voz"); NOM = "fig5_tres_maneras"
NM167 = {"abundancia": "abundancia", "normal": "normal", "sequia": "sequía", "sequia_dura": "sequía dura", "bestias_crian": "bestias que crían"}


if __name__ == "__main__":
    C156 = {(r["v"], r["mu"], r["s"]): r for r in json.load(open(os.path.join(AQUI, "felicidad_dia_a_dia", "partidas.json"), encoding="utf-8"))}
    V167 = json.load(open(os.path.join(AQUI, "salida", "vara_sumas_167.json"), encoding="utf-8")); R167 = {(r["v"], r["mu"], r["s"]): r for r in V167["R"]}
    assert len(C156) == len(R167) == 600 and all((v, mu, s) in C156 and (v, mu, s) in R167 for v in JUG for mu in MUNDOS for s in SEM)
    val = {"emp": {(v, mu): [sum(C156[(v, mu, s)]["emp"][:10]) / 10 for s in SEM] for v in JUG for mu in MUNDOS}}
    for k, esc in (("feliz", 100), ("suma", 1), ("bajo", 1)): val[k] = {(v, mu): [esc * R167[(v, mu, s)][f"todas|{k}"] for s in SEM] for v in JUG for mu in MUNDOS}
    # comprobaciones: la felicidad, con la de escalera_C; las medias del 167, con sus tablas
    FC = json.load(open(os.path.join(AQUI, "salida", "figuras_escalera_paper8.json"), encoding="utf-8"))["C_felicidad"]
    for v in JUG:
        for mu in MUNDOS:
            m = sum(val["feliz"][(v, mu)]) / 40; assert abs(m - FC[v][mu]["media"]) < 1e-9, (v, mu, m, FC[v][mu]["media"])
            for k in ("suma", "bajo"): assert abs(sum(val[k][(v, mu)]) / 40 - V167["tablas"][f"todas|{k}|{NM167[mu]}"]["medias"][v]) < 1e-12
    S.estilo(); fig, axs = plt.subplots(2, 2, figsize=(18, 11)); OUT = {}
    PAN = (("emp", "empujones al día, días 1 a 10", "se empujan"), ("feliz", "felicidad de la aldea (0 a 100)", "felicidad"),
           ("suma", "total de los tres balances", "el total de los tres balances"), ("bajo", "balance más bajo de los tres", "el balance más bajo"))
    for ax, (k, eje, tit) in zip(axs.flat, PAN):
        OUT[k] = S.barras(ax, val[k], JUG, S.ROT_MANERA, 0.26); ax.set_ylabel(eje); ax.set_title(tit, loc="left", fontsize=15)
        lo = min(b["lo"] for o in OUT[k].values() for b in o.values())
        if lo < 0: ax.set_ylim(lo * 1.15, max(b["hi"] for o in OUT[k].values() for b in o.values()) * 1.15); ax.axhline(0, color="black", linewidth=1.2, zorder=5)
        else: ax.set_ylim(bottom=0)
        if k == "feliz": ax.set_ylim(0, 100)
        ax.tick_params(axis="x", labelsize=13)
    h, l = axs[0, 0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=14, loc="upper center", ncol=3)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); S.guarda(fig, NOM)
    T = []
    for k, eje, tit in PAN:
        f = S.f1 if k in ("emp", "feliz") else S.f3
        T += [f"## {eje} (media [intervalo del 95 %])", ""] + S.tabla_barras(OUT[k], JUG, S.ROT_MANERA, f) + [""]
    S.escribe_txt(NOM, ["# Figura 5, las tres maneras de decidir", "",
        "Programa: figura5_tres_maneras_170.py. Datos: 600 partidas selladas, 40 por mundo y manera (semillas 30161-30200, 40 días): decide con el motor = la criatura completa (valle_experimento_v6); "
        "decide sumando y decide con la posición = sus gemelas de la escalera (valle_escalera_v6).", ""] + T + [
        "## De dónde sale", "",
        "- Empujones al día, días 1 a 10: la caché del prompt 156 (felicidad_dia_a_dia/partidas.json; los empujones como cierre_v46), la cuenta de la tabla «1-10» de informe_prompt_157.md "
        "(«empujones por día», una tabla por mundo) e informe_prompt_156.md. Es la cifra del texto, sección 6: «unos seis empujones y medio al día» la que suma, «entre dos y medio y cuatro» la del motor.",
        "- Felicidad de la aldea: la de siempre (evalua_experimento_v5.v5; la parte de los turnos despierta con los tres balances > 0), la de la figura escalera_C_felicidad (informe_prompt_154.md); comprobada igual.",
        "- Total de los tres balances y balance más bajo: salida/vara_sumas_167.json, «todas las criaturas» (informe_prompt_167.md, tablas (1) y (3), líneas 94-149). Análisis hecho después, sin apuesta (las medidas se fijaron en el commit 1de22483 antes de correr).",
        "- Las barras dan la media de cada manera con su intervalo; las diferencias emparejadas por valle (las que usa el texto) están en informe_prompt_167.md y en los informes 156-157.",
        "- El intervalo: bootstrap de 10.000 remuestreos con semilla 8 sobre las 40 partidas (evalua_experimento_v6.boot).", "",
        "## Pie propuesto", "",
        "«Las tres maneras de decidir, en los cinco mundos: con el motor (la criatura completa), sumando y con la posición; las tres con el mismo cuerpo, la misma voz y los mismos valles. "
        "Arriba, los empujones al día en los diez primeros días y la felicidad de la aldea; abajo, el total de los tres balances, que es la vara de la que suma, y el balance más bajo de los tres. "
        "La del motor se empuja menos al llegar y es más feliz; en el total no saca ventaja a la que suma, y donde la comida escasea o las bestias crían su balance más bajo es más alto. Cada barra es la media de 40 partidas, con su intervalo del 95 %.»"])
    for k in OUT: print(k, {v: {mu: round(OUT[k][v][mu]["media"], 3) for mu in MUNDOS} for v in JUG})

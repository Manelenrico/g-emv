"""[P8] Prompt 171, figura 5 pulida: la de figura5_tres_maneras_170.py (mismas fuentes y comprobaciones) con el mismo tamaño; solo cambian la coma decimal
de los ejes y que los textos salen de rotulos_figuras.csv (estilo_171). Comprueba que las tablas de números son las del .txt del 170.
   python3 figura5_tres_maneras_171.py [--idioma es] -> figuras_171/fig5_tres_maneras_es.png y .pdf"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import estilo_171 as S
import figura5_tres_maneras_170 as F0
plt, MUNDOS, SEM, JUG, NOM, NM167 = S.plt, S.MUNDOS, S.SEM, F0.JUG, F0.NOM, F0.NM167


if __name__ == "__main__":
    ID = S.idioma(); R = S.Rotulos(ID); R.comprueba(("fig5.", "mundo.", "manera.", "separador"))
    C156 = {(r["v"], r["mu"], r["s"]): r for r in json.load(open(os.path.join(AQUI, "felicidad_dia_a_dia", "partidas.json"), encoding="utf-8"))}
    V167 = json.load(open(os.path.join(AQUI, "salida", "vara_sumas_167.json"), encoding="utf-8")); R167 = {(r["v"], r["mu"], r["s"]): r for r in V167["R"]}
    assert len(C156) == len(R167) == 600 and all((v, mu, s) in C156 and (v, mu, s) in R167 for v in JUG for mu in MUNDOS for s in SEM)
    val = {"emp": {(v, mu): [sum(C156[(v, mu, s)]["emp"][:10]) / 10 for s in SEM] for v in JUG for mu in MUNDOS}}
    for k, esc in (("feliz", 100), ("suma", 1), ("bajo", 1)): val[k] = {(v, mu): [esc * R167[(v, mu, s)][f"todas|{k}"] for s in SEM] for v in JUG for mu in MUNDOS}
    FC = json.load(open(os.path.join(AQUI, "salida", "figuras_escalera_paper8.json"), encoding="utf-8"))["C_felicidad"]
    for v in JUG:
        for mu in MUNDOS:
            assert abs(sum(val["feliz"][(v, mu)]) / 40 - FC[v][mu]["media"]) < 1e-9
            for k in ("suma", "bajo"): assert abs(sum(val[k][(v, mu)]) / 40 - V167["tablas"][f"todas|{k}|{NM167[mu]}"]["medias"][v]) < 1e-12
    S.estilo(); fig, axs = plt.subplots(2, 2, figsize=(18, 11)); OUT = {}; rot = {v: R(f"manera.{v}") for v in JUG}
    for ax, k in zip(axs.flat, ("emp", "feliz", "suma", "bajo")):
        OUT[k] = S.barras(ax, val[k], JUG, rot, 0.26, R); ax.set_ylabel(R(f"fig5.eje_y_{k}")); ax.set_title(R(f"fig5.titulo_{k}"), loc="left", fontsize=15)
        lo = min(b["lo"] for o in OUT[k].values() for b in o.values())
        if lo < 0: ax.set_ylim(lo * 1.15, max(b["hi"] for o in OUT[k].values() for b in o.values()) * 1.15); ax.axhline(0, color="black", linewidth=1.2, zorder=5)
        else: ax.set_ylim(bottom=0)
        if k == "feliz": ax.set_ylim(0, 100)
        ax.tick_params(axis="x", labelsize=13); S.decimales(R, ax)
    h, l = axs[0, 0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=14, loc="upper center", ncol=3)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); rutas = S.guarda(fig, NOM, ID)
    T = []
    for k in ("emp", "feliz", "suma", "bajo"): T += S.tabla_barras(OUT[k], JUG, S.S0.ROT_MANERA, S.f1 if k in ("emp", "feliz") else S.f3)
    n = S.comprueba_tabla(NOM, T); print("hecho", rutas, "filas iguales al 170:", n)

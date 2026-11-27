"""[P8] Prompt 161, partes 3 a 6 (solo lee): cuatro figuras del experimento v6 sellado (valle_experimento_v6, semillas 30161-30200, 40 días), con el estilo
de las de la escalera (figuras_escalera_paper8.py: letra 15, sin marco arriba ni a la derecha, rejilla horizontal, ejes desde cero, media de las 40 semillas
con su intervalo del 95 %: evalua_experimento_v6.boot, 10.000 remuestreos, semilla 8).
  A (parte 3, v6_A_vivas): vivas el día 40 (de 8), con la pieza sellada cierre_v46 (evalua_experimento_v6.c46: 8 menos las muertes de fin.json).
  B (parte 4, v6_B_costumbres): tres paneles. (1) los turnos al día despierta con hambre > 30 y comida en la bolsa, días 0 a 9 (la medida sellada de P24:
     evalua_experimento_v6.nuevas -> extrae_hg_v1); (2) las noches dormidas fuera, días 0 a 9 (la medida sellada de P28: nuevas -> analiza_vc1, «noches10»);
     aquí, por partida (las noches fuera entre las noches de la partida, como evalua_escalera_v6.una), en %; P28 las sumaba en las 80 partidas de las dos
     sequías; (3) los golpes de la bestia recibidos estando dormida, por partida (sucesos «bestia_pega» con «por»: «dormida», valle/mundo.py:1032-1033;
     contados en el prompt 160, caché bestia_huerto_160/partidas.json).
  C (parte 5, v6_C_duelo_soledad): con las definiciones de la medida sellada A4 (duelo_soledad_v6.py, importada: casos_de, her): duelo = S-DUELO-CUERPO +
     S-DUELO-RECURSOS + S-DUELO-VINCULO, soledad = S-SOLEDAD, media de los turnos despierta de cada día (filas.jsonl.gz y balance.jsonl.gz, como
     duelo_soledad_v6.una). Casos: las de RG69r+voz que pierden a su hermana (muerte el día 5 o después, y ellas vivas 5 días más); control: las de otra casa
     de la misma partida que conservan a la suya, en los mismos días (las mismas reglas que duelo_soledad_v6.una). Del día −5 al +15 (0, el de la muerte);
     media de todos los casos (o controles) con datos ese día, y su banda del 95 % (bootstrap sobre los casos de ese día).
  D (parte 6, v6_D_un_dia): RG69r+voz, normal, semilla 30161, días 5 y 6 (contados del 1: los turnos 1.600 a 2.399; el 5 es de fruto). Una fila por criatura
     (las hermanas juntas) y en cada turno lo que hace (la acción del registro del mundo, haya salido bien o no; dormida cuenta como dormir), y debajo dónde
     está (el terreno de su casilla). Fondo sombreado: el anochecer claro y la noche oscuro (la fase del registro).
   python3 figuras_v6_161.py -> figuras/v6_{A_vivas,B_costumbres,C_duelo_soledad,D_un_dia}.png y .pdf, salida/figuras_v6_161.json"""
import gzip, json, os, sys
from collections import defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path[:0] = [AQUI, os.path.join(RAIZ, "valle"), os.path.join(AQUI, "reserva_v1")]
os.environ["ESCALERA_MODO"] = "experimento"; sys.argv[1:] = []
import evalua_escalera_v6 as ES
import figuras_escalera_paper8 as FE
import duelo_soledad_v6 as DS
import gif_rg69 as G
import mundo as MU
from matplotlib.patches import Patch
E6 = ES.E6
# (prompt 161) gif_rg69 importa reserva_v1/analiza_rg69, que al cargarse pone la carpeta de RG69r en el taller (analiza_rg69.py:26): se devuelve a la del experimento
E6.AN.CARP.update({v: (E6.CARPETA[v], v) for v in E6.CRI})
assert all(E6.AN.CARP[v][0] == E6.EXP for v in E6.CRI), E6.AN.CARP
boot = E6.boot; MUNDOS = E6.MUNDOS; SEM = range(30161, 30201); plt = FE.plt; NOMBRE_MUNDO = FE.NOMBRE_MUNDO
DIA = E6.DIA; PROTA = E6.PROTA
CACHE160 = os.path.join(AQUI, "bestia_huerto_160", "partidas.json")
A_JUG = ("tonto", "recolector", "RG68r", "RG068r", "RG69rvoz"); B_JUG = ("RG68r", "RG69r", "RG69rvoz")
ROT = {"tonto": "el tonto", "recolector": "el recolector", "RG68r": "la criatura de antes (RG68r)", "RG068r": "la gemela sin lado positivo (RG068r)",
       "RG69rvoz": "la criatura completa (RG69r+voz)", "RG69r": "con la reserva (RG69r)"}
ROT_B = dict(ROT, RG69rvoz="con la reserva y la voz (RG69r+voz)")
COLOR = {"tonto": "#eda100", "recolector": "#008300", "RG68r": "#6250d6", "RG068r": "#e87ba4", "RG69rvoz": "#2a78d6", "RG69r": "#1baf7a"}   # (paleta de la guía; pasa la prueba de daltonismo)
SEL = ("normal", 30161); DIAS_D = (5, 6)
ACC = (("dormir", "dormir", "#6250d6"), ("quedarse", "quedarse quieta", "#d6d5d0"), ("mover", "andar", "#2a78d6"), ("coger", "coger", "#eb6834"),
       ("comer", "comer", "#1baf7a"), ("trabajar", "trabajar el huerto", "#eda100"), ("dar", "dar", "#e87ba4"), ("empujar", "empujar", "#e34948"),
       ("otra", "otra (dejar, golpear, llamar, hablar)", "#52514e"))
SITIO = (("casa", "en una casa", G.COL["k"]), ("aldea", "en la plaza", G.COL["a"]), ("huerto", "en un huerto", G.COL["h"]), ("bosque", "en el bosque", G.COL["b"]),
         ("salvaje", "en la zona salvaje", G.COL["s"]), ("otro", "en otro sitio (camino, almacén, puerta)", G.COL["c"]))


def ab(x):
    """las medidas de A y B de una partida, con las piezas selladas"""
    v, mu, s = x; r = {"v": v, "mu": mu, "s": s, "vivas": E6.c46(x)["vivas"]}
    if v in B_JUG:
        n = E6.nuevas(x); nf, nt = n["noches10"]; r.update(h30_bolsa=n["h30_bolsa"], noches10=nf / nt if nt else None, noches10_n=[nf, nt])
    return r


def trazos(x):
    """los días −5 a +15 de cada caso y cada control de una partida (las reglas de duelo_soledad_v6.una)"""
    mu, s = x; n = f"{PROTA}_{mu}+sabores_s{s}_d40"; fin = json.load(open(os.path.join(DS.EXP, n, "fin.json"))); casos, muere = DS.casos_de(fin)
    S = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0]))
    for lf, lb in zip(gzip.open(os.path.join(DS.CARP, n, "filas.jsonl.gz"), "rt", encoding="utf-8"), gzip.open(os.path.join(DS.EXP, n, "balance.jsonl.gz"), "rt", encoding="utf-8")):
        xf, xb = json.loads(lf), json.loads(lb); assert xf["t"] == xb["t"]; dia = xf["t"] // DIA
        for a, r in xf["c"].items():
            b = xb["c"].get(a)
            if b is None or b[6]: continue
            z = S[a][dia]; z[0] += r[0] + r[1] + r[2]; z[1] += r[3]; z[2] += 1
    def serie(a, dm, k): return [S[a][d][k] / S[a][d][2] if d in S[a] and S[a][d][2] else None for d in range(dm - 5, dm + 16)]
    out = {"mu": mu, "s": s, "casos": [], "control": []}
    for a, dm in casos:
        out["casos"].append({"a": a, "dia": dm, "duelo": serie(a, dm, 0), "soledad": serie(a, dm, 1)})
        for c in DS.TODAS:
            if c[0] == a[0] or any(y in muere and muere[y] // DIA <= dm + 5 for y in (c, DS.her(c))): continue
            out["control"].append({"a": c, "dia": dm, "duelo": serie(c, dm, 0), "soledad": serie(c, dm, 1)})
    return out


def barras(ax, R, jug, k, esc, rot, ancho):
    out = {}; nj = len(jug)
    for j, v in enumerate(jug):
        B = [boot([R[(v, mu, s)][k] * esc for s in SEM if R[(v, mu, s)][k] is not None]) for mu in MUNDOS]; out[v] = dict(zip(MUNDOS, B))
        xs = [i + (j - (nj - 1) / 2) * (ancho + 0.02) for i in range(len(MUNDOS))]; m = [b["media"] for b in B]
        ax.bar(xs, m, width=ancho, color=COLOR[v], label=rot[v], zorder=3)
        ax.errorbar(xs, m, yerr=[[b["media"] - b["lo"] for b in B], [b["hi"] - b["media"] for b in B]], fmt="none", ecolor="#333333", elinewidth=1.4, capsize=3, zorder=4)
    ax.set_xticks(range(len(MUNDOS))); ax.set_xticklabels([NOMBRE_MUNDO[mu] for mu in MUNDOS]); ax.set_ylim(bottom=0)
    ax.grid(axis="y", color="#dddddd", linewidth=0.8, zorder=0)
    return out


def guarda(fig, nom):
    for ext in ("png", "pdf"): fig.savefig(os.path.join(AQUI, "figuras", f"{nom}.{ext}"), dpi=200)
    plt.close(fig)


def sitio_de(V, p):
    t = V.terreno(p); return t if t in ("casa", "aldea", "huerto", "bosque", "salvaje") else "otro"


if __name__ == "__main__":
    plt.rcParams.update({"font.size": 15, "axes.spines.top": False, "axes.spines.right": False}); OUT = {}
    T = [(v, mu, s) for v in A_JUG + ("RG69r",) for mu in MUNDOS for s in SEM]
    R = {}
    with Pool(8) as p:
        for i, r in enumerate(p.imap_unordered(ab, T, chunksize=4)):
            R[(r["v"], r["mu"], r["s"])] = r
            if i % 100 == 0: print("partidas", i, flush=True)
        TR = p.map(trazos, DS.candidatas()); print("trazos", len(TR), flush=True)
    C160 = {tuple(r["k"]): r for r in json.load(open(CACHE160))}
    for k, r in R.items():
        if r["v"] in B_JUG: r["golpes_dormida"] = C160[k]["pega"].get("dormida", 0)
    # A: vivas
    fig, ax = plt.subplots(figsize=(13, 6.2)); OUT["A_vivas"] = barras(ax, R, A_JUG, "vivas", 1, ROT, 0.16)
    ax.set_ylabel("vivas el día 40 (de 8)"); ax.set_ylim(0, 8.6); ax.legend(frameon=False, fontsize=12, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.2))
    fig.tight_layout(); guarda(fig, "v6_A_vivas")
    # B: las dos costumbres
    fig, axs = plt.subplots(1, 3, figsize=(20, 6.4)); OUT["B_costumbres"] = {}
    for ax, (k, esc, eje) in zip(axs, (("h30_bolsa", 1, "turnos al día con hambre > 30\ny comida en la bolsa (días 0 a 9)"), ("noches10", 100, "noches dormidas fuera, días 0 a 9 (%)"),
                                        ("golpes_dormida", 1, "golpes de la bestia recibidos\nestando dormida, por partida"))):
        OUT["B_costumbres"][k] = barras(ax, R, B_JUG, k, esc, ROT_B, 0.26); ax.set_ylabel(eje); ax.tick_params(axis="x", labelrotation=25)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=14, loc="upper center", ncol=3)
    fig.tight_layout(rect=(0, 0, 1, 0.92)); guarda(fig, "v6_B_costumbres")
    # C: duelo y soledad
    Z = {g: [c for r in TR for c in r[g]] for g in ("casos", "control")}; dias = list(range(-5, 16)); OUT["C_duelo_soledad"] = {"casos": len(Z["casos"]), "controles": len(Z["control"]),
        "partidas": len(TR), "por_mundo": {mu: sum(len(r["casos"]) for r in TR if r["mu"] == mu) for mu in MUNDOS}}
    fig, axs = plt.subplots(1, 2, figsize=(17, 6.2))
    for ax, sn, eje in zip(axs, ("duelo", "soledad"), ("duelo (media de los turnos despierta del día)", "soledad (media de los turnos despierta del día)")):
        for g, col, rot in (("casos", "#eb6834", f"pierde a su hermana ({len(Z['casos'])} casos)"), ("control", "#2a78d6", f"la conserva ({len(Z['control'])} controles)")):
            B = [boot([c[sn][i] for c in Z[g] if c[sn][i] is not None]) for i in range(len(dias))]; OUT["C_duelo_soledad"][f"{sn}|{g}"] = B
            ax.fill_between(dias, [b["lo"] for b in B], [b["hi"] for b in B], color=col, alpha=0.22, linewidth=0)
            ax.plot(dias, [b["media"] for b in B], color=col, linewidth=2, label=rot)
        ax.axvline(0, color="#52514e", linewidth=1, linestyle="--"); ax.set_xlabel("días desde la muerte de la hermana (0, el día de la muerte)"); ax.set_ylabel(eje)
        ax.set_ylim(bottom=0); ax.set_xlim(-5, 15); ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, frameon=False, fontsize=14, loc="upper center", ncol=2)
    fig.tight_layout(rect=(0, 0, 1, 0.92)); guarda(fig, "v6_C_duelo_soledad")
    OUT["C_duelo_soledad"]["n_por_dia"] = {g: [sum(1 for c in Z[g] if c["duelo"][i] is not None) for i in range(len(dias))] for g in Z}
    # D: un día en el valle
    V = MU.Valle(); t0, t1 = (DIAS_D[0] - 1) * DIA, DIAS_D[1] * DIA; QUIEN = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
    ac = {a: [None] * (t1 - t0) for a in QUIEN}; si = {a: [None] * (t1 - t0) for a in QUIEN}; fase = [None] * (t1 - t0)
    for l in gzip.open(os.path.join(E6.ruta(PROTA, *SEL), "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        m = json.loads(l); t = m["turno"]
        if t < t0: continue
        if t >= t1: break
        i = t - t0; fase[i] = m["fase"]
        for a in QUIEN:
            g = m["agentes"].get(a)
            if g is None or g["cuerpo"]["muerta"]: continue
            x = "dormir" if g["cuerpo"].get("dormida") else (g.get("accion") or "quedarse"); ac[a][i] = x if x in {c[0] for c in ACC} else "otra"
            si[a][i] = sitio_de(V, tuple(g["pos"]))
    from matplotlib.colors import ListedColormap
    import numpy as np
    fig, axs = plt.subplots(2, 1, figsize=(20, 10.5), sharex=True)
    for ax, X, CAT, tit in ((axs[0], ac, ACC, "lo que hace"), (axs[1], si, SITIO, "dónde está")):
        idx = {c[0]: j for j, c in enumerate(CAT)}; cm = ListedColormap([c[2] for c in CAT])
        for i, f in enumerate(fase):
            if f in ("anochecer", "noche"): ax.axvspan(i, i + 1, color="#c3c2b7" if f == "anochecer" else "#8a8984", linewidth=0, zorder=0)
        for r, a in enumerate(QUIEN):
            if r and a[1] == "1": ax.axhline(len(QUIEN) - 1 - r + 0.5, color="black", linewidth=0.8, zorder=3)      # (una raya entre casas)
            fila = np.array([[idx[z] if z is not None else np.nan for z in X[a]]], dtype=float)
            ax.imshow(np.ma.masked_invalid(fila), aspect="auto", cmap=cm, vmin=-0.5, vmax=len(CAT) - 0.5, interpolation="nearest",
                      extent=(0, t1 - t0, len(QUIEN) - 1 - r - 0.36, len(QUIEN) - 1 - r + 0.36), zorder=2)
        ax.set_yticks(range(len(QUIEN))); ax.set_yticklabels([f"{a} (casa {a[0]})" for a in reversed(QUIEN)], fontsize=12); ax.set_ylim(-0.6, len(QUIEN) - 0.4)
        ax.set_title(tit, loc="left", fontsize=15); ax.spines["left"].set_visible(False)
        ax.legend(handles=[Patch(color=c[2], label=c[1]) for c in CAT], loc="upper left", bbox_to_anchor=(1.005, 1), frameon=False, fontsize=12)
    axs[1].legend(handles=[Patch(color=c[2], label=c[1]) for c in SITIO] + [Patch(color="#c3c2b7", label="fondo: anochecer"), Patch(color="#8a8984", label="fondo: noche")],
                  loc="upper left", bbox_to_anchor=(1.005, 1), frameon=False, fontsize=12)
    tk = list(range(0, t1 - t0 + 1, 100)); axs[1].set_xticks(tk); axs[1].set_xticklabels([f"{t0 + x}" for x in tk]); axs[1].set_xlim(0, t1 - t0)
    axs[1].set_xlabel(f"turno de la partida (día {DIAS_D[0]}, con fruto: {t0}-{t0 + DIA - 1}; día {DIAS_D[1]}, sin fruto: {t0 + DIA}-{t1 - 1})")
    for ax in axs: ax.axvline(DIA, color="black", linewidth=1.2, zorder=3)
    fig.suptitle(f"Un día en el valle: la criatura completa (RG69r+voz), mundo normal, semilla {SEL[1]}, días {DIAS_D[0]} y {DIAS_D[1]}", x=0.01, ha="left", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.96)); guarda(fig, "v6_D_un_dia")
    OUT["D_un_dia"] = {"cuenta_acciones": {a: {c[0]: ac[a].count(c[0]) for c in ACC} for a in QUIEN}, "cuenta_sitios": {a: {c[0]: si[a].count(c[0]) for c in SITIO} for a in QUIEN},
                       "fases": {f: fase.count(f) for f in sorted(set(fase))}, "muertas_turnos": {a: ac[a].count(None) for a in QUIEN}}
    json.dump(OUT, open(os.path.join(AQUI, "salida", "figuras_v6_161.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k in ("A_vivas",): print(k, {v: {mu: round(b["media"], 2) for mu, b in OUT[k][v].items()} for v in A_JUG})
    for k in OUT["B_costumbres"]: print(k, {v: {mu: round(b["media"], 2) for mu, b in OUT["B_costumbres"][k][v].items()} for v in B_JUG})
    print({k: OUT["C_duelo_soledad"][k] for k in ("casos", "controles", "partidas", "por_mundo")}); print(OUT["D_un_dia"]["fases"], OUT["D_un_dia"]["muertas_turnos"])

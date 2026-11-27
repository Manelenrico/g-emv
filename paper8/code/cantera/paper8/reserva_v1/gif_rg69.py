"""[P8] Prompt 146, punto 4: un GIF de una hermana en sequía dura, días 8 a 12, RG68r sellada (izquierda) frente a RG69r (derecha), la misma semilla. De los
datos crudos (mundo.jsonl.gz), con matplotlib. LA REGLA PARA ESCOGERLA, fijada antes de mirar: de las semillas 30121 a 30140 de sequía dura y las ocho
criaturas, las que están vivas al empezar el día 8 en las dos partidas; una a suertes (random.Random(8).choice). Un fotograma cada 4 turnos: el mapa, ella
(rojo), su hermana (azul), las demás (gris); arriba, el día, el turno, su hambre, la comida que lleva y lo que hace.
   python3 reserva_v1/gif_rg69.py -> reserva_v1/gif_rg69.gif"""
import gzip, json, os, random, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path[:0] = [P8, AQUI]
import diario_v1 as V1
import analiza_rg69 as AR
M = V1.MAPA; DIA = AR.DIA; T0, T1, PASO = 8 * AR.DIA, 13 * AR.DIA, 4
COL = {"b": "#cfe8c7", "s": "#e8dfc7", "h": "#f3e6a8", "k": "#d9c2a7", "p": "#b08a5e", "m": "#9aa4b1", "a": "#eeeeee", "c": "#e4e4e4", "x": "#ffffff"}
T = M.T; fondo = [[matplotlib.colors.to_rgb(COL.get(T[y][x], "#ffffff")) for x in range(len(T[0]))] for y in range(len(T))]
her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
RUTA = {"RG68r": lambda s: os.path.join(AR.EXP, f"RG68r_sequia_dura+sabores_s{s}_d40"), "RG69r": lambda s: os.path.join(AR.TALLER, f"RG69r_sequia_dura+sabores_s{s}_d40")}

def lee(d):
    fr = {}
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        m = json.loads(l); t = m["turno"]
        if t >= T1: break
        if t >= T0 and (t - T0) % PASO == 0:
            fr[t] = {a: (g["pos"], g["cuerpo"]["muerta"], g["cuerpo"]["hambre"], (g.get("bolsa") or []).count("comida"), g.get("accion"), g["cuerpo"].get("dormida"))
                     for a, g in m["agentes"].items() if isinstance(g, dict) and "cuerpo" in g and a != "bestia"}
    return fr
def viva8(d, a):
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        m = json.loads(l)
        if m["turno"] == T0: return a in m["agentes"] and not m["agentes"][a]["cuerpo"]["muerta"]          # (las muertas pueden faltar del registro)


if __name__ == "__main__":
    C = [(s, a) for s in range(30121, 30141) for a in ("A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2")]
    C = [(s, a) for s, a in C if viva8(RUTA["RG68r"](s), a) and viva8(RUTA["RG69r"](s), a)]
    s, a = random.Random(8).choice(C); b = her(a); FR = {k: lee(f(s)) for k, f in RUTA.items()}; ts = sorted(set(FR["RG68r"]) & set(FR["RG69r"]))
    fig, axs = plt.subplots(1, 2, figsize=(11, 6.2)); P = {}; TX = {}
    for ax, k in zip(axs, ("RG68r", "RG69r")):
        ax.imshow(fondo, origin="upper"); ax.set_xticks([]); ax.set_yticks([])
        P[k] = {x: ax.plot([], [], "o", color=("red" if x == a else ("blue" if x == b else "grey")), ms=(8 if x in (a, b) else 5))[0] for x in FR[k][ts[0]]}
        TX[k] = ax.set_title("", fontsize=8, loc="left")
    def pinta(i):
        t = ts[i]; out = []
        for k in ("RG68r", "RG69r"):
            for x, ln in P[k].items():
                pos, muerta = FR[k][t].get(x, (None, True))[:2]; ln.set_data([pos[0]] if not muerta else [], [pos[1]] if not muerta else []); out.append(ln)
            pos, muerta, h, n, acc, dorm = FR[k][t].get(a, (None, True, 0, 0, None, False))
            TX[k].set_text(f"{'RG68r sellada' if k == 'RG68r' else 'RG69r (la reserva)'} · sequía dura {s}, día {t // DIA}, turno {t % DIA}\n"
                           + (f"{a} (rojo): muerta" if muerta else f"{a} (rojo): hambre {h:.0f}, lleva {n} comida{'s' if n != 1 else ''}, {acc}{' (dormida)' if dorm else ''}")); out.append(TX[k])
        return out
    FuncAnimation(fig, pinta, frames=len(ts), blit=False).save(os.path.join(AQUI, "gif_rg69.gif"), writer=PillowWriter(fps=12)); plt.close(fig)
    print("sequía dura", s, a, "hermana", b, len(ts), "fotogramas", f"(de {len(C)})")

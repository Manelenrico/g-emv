"""[P8] Pasada del prompt 34 (sin banco formal), con el mundo nuevo (la temperatura) y las medidas de siempre más las de la huida paso a paso y el anochecer:
  - un plato (V21) frente a dos platos (V22), peligro medio, 10 partidas de 20 días, en tres mundos: normal (sin épocas), sequía (épocas con escasez ×0,7) y
    abundancia (×1,3 todo el rato, en matorrales y huerto);
  - para la huida con duelo (punto 1), V19 y V21 en la sequía con peligro medio y alto (la V21 medio-sequía es la misma de arriba). -> pasada_v22.json"""
import json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [AQUI]
import pasada_v18 as P, banco_cuerpo_valle as B, banco_v7 as B7
ESC = P.CV["matorrales"]["epocas"]["factores"][2]
ABU = P.CV["matorrales"]["epocas"]["factores"][0]
MUNDOS = {"normal": None, "sequia": P.EP(ESC), "abundancia": dict(P.EP(ABU), factores=[ABU] * len(P.CV["matorrales"]["epocas"]["factores"]))}


def una(arg):
    v, m, s, mundo = arg
    mu = {"matorrales": {"epocas": MUNDOS[mundo]}} if MUNDOS[mundo] else None
    return dict(B.partida("cuerpo", s, cultura=B7.cultura(m), mando=m, mundo=mu, emociones=True, **B7.VARS[v]), variante=v, mando=m, semilla=s, mundo=mundo)


if __name__ == "__main__":
    T = [(v, "medio", s, mu) for mu in MUNDOS for v in ("V21", "V22") for s in range(1, 11)]
    T += [("V19", m, s, "sequia") for m in ("medio", "alto") for s in range(1, 11)] + [("V21", "alto", s, "sequia") for s in range(1, 11)]
    with Pool(8) as p: res = p.map(una, T, chunksize=1)
    json.dump(res, open(os.path.join(AQUI, "pasada_v22.json"), "w"), ensure_ascii=False)
    for v, m, mu in sorted({(r["variante"], r["mando"], r["mundo"]) for r in res}):
        L = [r for r in res if (r["variante"], r["mando"], r["mundo"]) == (v, m, mu)]; print(v, m, mu, "vivas", sum(8 - len(r["muertes"]) for r in L), "de", 8 * len(L))

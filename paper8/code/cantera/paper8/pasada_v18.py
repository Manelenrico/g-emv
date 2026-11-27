"""[P8] Pasada del prompt 30 (sin banco formal): la V18 (V16 + las distancias unificadas), peligro medio y alto, 10 partidas de 20 días: sin épocas, y con las
épocas en todo lo que da comida (matorrales y huerto: abundancia ×1,3, normal, escasez, normal; 5 días cada una) con dos escaseces, ×0,7 y ×0,5. El tonto y el
recolector, con la escasez de ×0,5, 5 partidas (para ver que siguen viviendo). -> pasada_v18.json"""
import json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path[:0] = [AQUI, os.path.join(RAIZ, "valle")]
import banco_cuerpo_valle as B, banco_v7 as B7, banco_base_v5 as BB
CV = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json")))
def EP(escasez): return dict(CV["matorrales"]["epocas"], activo=True, afecta_huerto=True, factores=[1.3, 1.0, escasez, 1.0])


def una(arg):
    v, m, s, esc = arg
    mundo = {"matorrales": {"epocas": EP(esc)}} if esc else None
    if v in ("tonto", "recolector"):
        _V = BB.Valle
        class VE(_V):
            def __init__(self, *a, **k): super().__init__(*a, **k); self.cfg["matorrales"]["epocas"] = EP(esc)
        BB.Valle = VE; r = BB.partida(v, CV["margen_comida"]["activo"], m, s); BB.Valle = _V
        return dict(r, variante=v, mando=m, semilla=s, escasez=esc)
    return dict(B.partida("cuerpo", s, cultura=B7.cultura(m), mando=m, mundo=mundo, **B7.VARS[v]), variante=v, mando=m, semilla=s, escasez=esc)


if __name__ == "__main__":
    T = [("V18", m, s, esc) for esc in (0.5, 0.7, None) for m in ("medio", "alto") for s in range(1, 11)] + [(t, "medio", s, 0.5) for t in ("tonto", "recolector") for s in range(1, 6)]
    with Pool(8) as P: res = P.map(una, T, chunksize=1)
    json.dump(res, open(os.path.join(AQUI, "pasada_v18.json"), "w"), ensure_ascii=False, indent=1)
    for v in ("V18", "tonto", "recolector"):
        for m in ("medio", "alto"):
            for esc in (None, 0.7, 0.5):
                L = [r for r in res if r["variante"] == v and r["mando"] == m and r["escasez"] == esc]
                if L: print(v, m, "escasez", esc, "vivas", sum(8 - len(r["muertes"]) for r in L), "de", 8 * len(L))

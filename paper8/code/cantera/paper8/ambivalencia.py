"""[P8] Prompt 72 (idea de Manel): la medida de ambivalencia. En cada estado, con el motor solo como instrumento (su State, importado, sobre las seis sumas de
ahora, como la felicidad de medidas_valle), la ambivalencia de cada dimensión es la menor de su ganancia y su pérdida (alta cuando las dos pesan a la vez), y
la del estado, la mayor de las tres.
   python3 ambivalencia.py [semillas=1001-1004] -> la prueba sobre estados viejos del experimento (sin mirar coincidencias): salida/ambivalencia_prueba.json"""
import gzip, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path[:0] = [AQUI, RAIZ]
from motor.model import State                                                      # el motor publicado, solo para medir

def ambivalencia(seis):
    """las seis sumas de ahora (placer, displacer, alegria, enfado, amor, tristeza) → (la del estado, {F, R, S})"""
    st = State(pF=seis["placer"], nF=seis["displacer"], pR=seis["alegria"], nR=seis["enfado"], pS=seis["amor"], nS=seis["tristeza"])
    a = {"F": min(st.pF, st.nF), "R": min(st.pR, st.nR), "S": min(st.pS, st.nS)}
    return max(a.values()), a

def de_partida(d):
    """{(turno, criatura): ambivalencia del estado} de una partida, desde su registro de criaturas (las seis de cada turno)"""
    out = {}
    for l in gzip.open(os.path.join(d, "criaturas.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l)
        for a, c in x["criaturas"].items():
            if c.get("seis"): out[(x["turno"], a)] = ambivalencia(c["seis"])
    return out


if __name__ == "__main__":
    EXP = "/Volumes/Mem G-EMV/valle_experimento"
    a_, b_ = (sys.argv[1] if len(sys.argv) > 1 else "1001-1004").split("-"); SS = range(int(a_), int(b_) + 1)
    res = {}
    for v in ("RG32r", "S32", "RG032r", "S032"):
        for mu in ("bestia_dia", "sequia_dura"):
            if v in ("RG032r", "S032") and mu == "sequia_dura": continue
            A = []; dims = {"F": 0, "R": 0, "S": 0}
            for s in SS:
                for (amb, por) in de_partida(os.path.join(EXP, f"{v}_{mu}_s{s}_d40")).values():
                    A.append(amb); dims[max(por, key=por.get)] += amb > 0
            A.sort(); n = len(A); q = lambda p: A[min(n - 1, int(p * n))]
            res[f"{v}|{mu}"] = {"estados": n, "media": sum(A) / n, "cuartos": [q(0.25), q(0.5), q(0.75)], "max": A[-1], "cero": sum(1 for x in A if x == 0) / n,
                                "dimension_mayor_si_>0": dims}
            print(v, mu, {k: (round(x, 4) if isinstance(x, float) else ([round(y, 4) for y in x] if isinstance(x, list) else x)) for k, x in res[f"{v}|{mu}"].items()}, flush=True)
    json.dump(res, open(os.path.join(AQUI, "salida", "ambivalencia_prueba.json"), "w"), ensure_ascii=False, indent=1)

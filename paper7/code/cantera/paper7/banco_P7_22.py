"""[P7-22] RECORDAR POR PARECIDO, EN BANCO: tres formas de recordar sobre los mismos recuerdos (P7_22_recuerdos.json), sin jugar ni replicar.
  python3 banco_P7_22.py --fija     -> fija s (mediana de las distancias emocionales entre pares de aperturas) y el umbral de dolor, y NADA mas (para el sello)
  python3 banco_P7_22.py            -> P7_22_resultado.json (separaciones, R1-R3, mapa emocional, sensibilidad)

LAS TRES FORMAS (diseno de Manel; numeros de metodo de la mesa):
  (A) sin condicion: una sola creencia, peso = intensidad x OLVIDO^dias.
  (B) casillas dentro o fuera, como hoy: solo los recuerdos de la misma casilla, mismo peso.
  (C) por parecido: peso = intensidad x OLVIDO^dias x parecido; parecido = parecido emocional x parecido de contexto;
      parecido emocional = exp(-distancia(foto de ahora, foto del recuerdo) / s), distancia euclidea en el vector de 5 (dolor F, R, S, positivo, d);
      parecido de contexto = (1 si coincide dentro/fuera, si no 0,25) x (1 si coincide golpeada/no, si no 0,5).
  En las tres, el recuerdo neutro del centro (efecto 0, peso 1, sin contexto ni foto) entra en la media: creencia = sum(w e) / (sum(w) + 1).
  Lo que se recuerda al abrir en el dia d son los recuerdos de los dias ANTERIORES de esa criatura (el cuaderno se escribe al acabar el dia).
  La creencia que se compara con lo que paso es la del cuerpo (efecto_cuerpo), en unidades de vida (la cura del catalogo es 50).
SEPARACION: probabilidad de que una apertura que se completa tenga la creencia mas alta que una que se corta (empates, 1/2); 0,5 = no separa.
"""
import bisect, collections, json, math, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
OLVIDO = 0.95; PESO_NEUTRO = 1.0; CURA = 50.0
CTX_DENTRO = 0.25; CTX_GOLPE = 0.5                                                 # parecido de contexto cuando no coincide
V = json.load(open(os.path.join(AQUI, "P7_22_recuerdos.json")))
vec = lambda f: (f["dolor_F"], f["dolor_R"], f["dolor_S"], f["positivo"], float(f["d"] or 0.0))
dist = lambda a, b: math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
R_TODOS = [dict(r, campo=v["campo"], serie=v["serie"], slot=v["slot"]) for v in V.values() for r in v["recuerdos"]]


def fija():
    fotos = [vec(r["foto"]) for r in R_TODOS]
    ds = [dist(fotos[i], fotos[j]) for i in range(len(fotos)) for j in range(i + 1, len(fotos))]
    s = st.median(ds); umbral = st.median([r["foto"]["dolor_F"] for r in R_TODOS if r["dentro"]])
    return {"s": round(s, 4), "pares": len(ds), "umbral_dolor_F": round(umbral, 4), "aperturas": len(R_TODOS), "aperturas_dentro": sum(1 for r in R_TODOS if r["dentro"])}


def creencia(forma, ahora, previos, s, ctx_d=CTX_DENTRO, ctx_g=CTX_GOLPE):
    """La creencia del cuerpo al abrir `ahora` con los recuerdos `previos` (de dias anteriores): (valor, suma de pesos vividos)."""
    num = 0.0; den = 0.0
    for r in previos:
        w = r["intensidad"] * (OLVIDO ** max(0, ahora["dia"] - r["dia"]))
        if forma == "B":
            if r["dentro"] != ahora["dentro"]: continue
        elif forma == "C":
            pe = math.exp(-dist(vec(ahora["foto"]), vec(r["foto"])) / s)
            pc = (1.0 if r["dentro"] == ahora["dentro"] else ctx_d) * (1.0 if r["golpeado_48"] == ahora["golpeado_48"] else ctx_g)
            w *= pe * pc
        num += w * r["efecto"]["cuerpo"]; den += w
    return num / (den + PESO_NEUTRO), den


def separacion(pares):
    """pares: [(creencia, completado)]"""
    xs = sorted(c for c, ok in pares if ok); ys = sorted(c for c, ok in pares if not ok)
    if not xs or not ys: return None
    s_ = 0.0
    for x in xs: s_ += bisect.bisect_left(ys, x) + 0.5 * (bisect.bisect_right(ys, x) - bisect.bisect_left(ys, x))
    return s_ / (len(xs) * len(ys))


def recorre(s, ctx_d=CTX_DENTRO, ctx_g=CTX_GOLPE):
    """Cada criatura (campo, serie, asiento) recorre sus dias en orden; en cada apertura, las tres creencias."""
    out = []
    por = collections.defaultdict(list)
    for r in R_TODOS: por[(r["campo"], r["serie"], r["slot"])].append(r)
    for k, rec in por.items():
        rec.sort(key=lambda r: (r["dia"], r["t0"]))
        for r in rec:
            previos = [q for q in rec if q["dia"] < r["dia"]]
            fila = {"campo": r["campo"], "serie": r["serie"], "slot": r["slot"], "dia": r["dia"], "t0": r["t0"], "dentro": r["dentro"], "golpeado_48": r["golpeado_48"], "completado": r["completado"], "dolor_F": r["foto"]["dolor_F"], "previos": len(previos)}
            for forma in ("A", "B", "C"):
                c, w = creencia(forma, r, previos, s, ctx_d, ctx_g); fila[forma] = round(c, 3); fila[forma + "_pesos"] = round(w, 3)
            out.append(fila)
    return out


def resume(filas, etiqueta):
    R = {"etiqueta": etiqueta, "separacion": {}}
    for campo in ("P7-10", "P7-14b", "los dos"):
        for dentro in (True, False):
            X = [f for f in filas if (campo == "los dos" or f["campo"] == campo) and f["dentro"] == dentro and f["previos"] > 0]
            R["separacion"][f"{campo}|{'dentro' if dentro else 'fuera'}"] = {"aperturas": len(X), "completadas": sum(1 for f in X if f["completado"]), **{forma: (None if separacion([(f[forma], f["completado"]) for f in X]) is None else round(separacion([(f[forma], f["completado"]) for f in X]), 3)) for forma in ("A", "B", "C")}}
    # R3: fuera del circulo, la creencia C por criatura y dia
    R["fuera_por_criatura"] = {}
    for k in sorted({(f["campo"], f["serie"], f["slot"]) for f in filas}):
        X = sorted([f for f in filas if (f["campo"], f["serie"], f["slot"]) == k and not f["dentro"] and f["previos"] > 0], key=lambda f: (f["dia"], f["t0"]))
        baja = next((f["dia"] for f in X if f["C"] < 0.25 * CURA), None)
        R["fuera_por_criatura"]["|".join(map(str, k))] = {"aperturas_fuera": len(X), "primer_dia_por_debajo_del_25%": baja, "desde_el_dia_10_todas_por_debajo": all(f["C"] < 0.25 * CURA for f in X if f["dia"] >= 10) if any(f["dia"] >= 10 for f in X) else None,
                                                           "C_por_dia": {str(f["dia"]): f["C"] for f in X}}
    return R


if __name__ == "__main__":
    if "--fija" in sys.argv:
        F = fija(); json.dump(F, open(os.path.join(AQUI, "P7_22_fijado.json"), "w"), indent=1); print(F); sys.exit(0)
    F = json.load(open(os.path.join(AQUI, "P7_22_fijado.json"))); s = F["s"]
    filas = recorre(s); OUT = {"fijado": F, "principal": resume(filas, f"s = {s}, contexto 0,25 / 0,5"), "aperturas": filas}
    # el mapa emocional: cortes y curas en la foto
    M = {}
    for dentro in (True, False):
        for ok in (True, False):
            X = [r for r in R_TODOS if r["dentro"] == dentro and r["completado"] == ok]
            M[f"{'dentro' if dentro else 'fuera'}|{'cura' if ok else 'corte'}"] = {"n": len(X), **{k: (round(st.median([r["foto"][k] for r in X]), 3) if X else None) for k in ("dolor_F", "dolor_R", "dolor_S", "positivo")}, "d": (round(st.median([float(r["foto"]["d"] or 0) for r in X]), 3) if X else None),
                                                                              "dolor_F_cuartiles": ([round(x, 3) for x in st.quantiles([r["foto"]["dolor_F"] for r in X], n=4)] if len(X) > 3 else None)}
    OUT["mapa_emocional"] = M
    # sensibilidad (despues del sello; marcada): s a la mitad y al doble; contexto mas blando (0,5 / 0,75) y mas duro (0,1 / 0,25)
    OUT["sensibilidad"] = {"s/2": resume(recorre(s / 2), "s/2"), "2s": resume(recorre(2 * s), "2s"), "contexto blando": resume(recorre(s, 0.5, 0.75), "contexto 0,5 / 0,75"), "contexto duro": resume(recorre(s, 0.1, 0.25), "contexto 0,1 / 0,25")}
    json.dump(OUT, open(os.path.join(AQUI, "P7_22_resultado.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in OUT["principal"]["separacion"].items(): print(k, v)

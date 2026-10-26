"""[P7-58] CURIOSIDAD POR EL PROGRESO DEL APRENDIZAJE (SELLO_P7_58.md; GEMV_P7_58=1; solo banco). Sustituye filo_P7_40.curiosidad (ignorancia x importancia esperada x cautela)
por progreso x cautela: para cada objeto, cada recuerdo vivido sin corte da Δ_i (cambio de la creencia en su situacion, tres dimensiones, regla del cuerpo, vista desde su dia); producto
bruto |Δ_i · media(Δ de las ultimas ceil(n/2) pruebas de ese objeto hasta la i)|; progreso = bruto / mediana de los brutos de todas las pruebas de todos los objetos hasta la i (si la
mediana es 0, el menor bruto positivo; si no hay, progreso 0); curiosidad = media del progreso de las ultimas ceil(n/2) pruebas; no probado = 1 (nacimiento). Se recalcula solo cuando
cambia el numero de recuerdos del cuaderno (cache)."""
import math, os, statistics as st
import filo_P7_40 as FI
from cuaderno_P7 import DOMINIOS, OLVIDO, PESO_NEUTRO
ON = os.environ.get("GEMV_P7_58", "0") == "1"; NACIMIENTO = 1.0
E = {"clave": None, "curio": {}, "detalle": {}}


def creencia(recs, dia):
    if not recs: return (0.0, 0.0, 0.0)
    out = []
    for dom in DOMINIOS:
        num = 0.0; den = PESO_NEUTRO; techo = []
        for r in recs:
            w = float(r["intensidad"]) * (OLVIDO ** max(0, dia - int(r["dia"])))
            if dom == "cuerpo" and r.get("al_menos"): techo.append((w, float(r["efecto"][dom]))); continue
            num += w * float(r["efecto"][dom]); den += w
        if techo:
            base = num / den
            for w, e in techo:
                if e > base: num += w * e; den += w
        out.append(num / den)
    return tuple(out)


def calcula(c):
    """todas las pruebas vividas sin corte de todos los objetos, en orden (dia, tick): Δ, bruto, progreso; curiosidad por objeto."""
    recs = sorted([(o, s, r) for o, s, r in c.recuerdos() if not r.get("corte") and r.get("origen", "vivido") == "vivido"], key=lambda x: (int(x[2]["dia"]), int(x[2].get("tick") or 0)))
    por_os = {}; deltas = {}; brutos = []; prog = {}
    for o, s, r in recs:
        prev = por_os.setdefault((o, s), []); dia = int(r["dia"]); b0 = creencia(prev, dia); prev.append(r); b1 = creencia(prev, dia)
        d = tuple(x - y for x, y in zip(b1, b0)); L = deltas.setdefault(o, []); L.append(d); n = len(L); k = math.ceil(n / 2); win = L[-k:]
        m = tuple(sum(v[j] for v in win) / len(win) for j in range(3)); bruto = abs(sum(d[j] * m[j] for j in range(3))); brutos.append(bruto)
        med = st.median(brutos); den = med if med > 0 else min([x for x in brutos if x > 0], default=0.0)
        prog.setdefault(o, []).append(bruto / den if den > 0 else 0.0)
    curio = {o: st.mean(p[-math.ceil(len(p) / 2):]) for o, p in prog.items()}
    return curio, {o: {"pruebas": len(p), "progreso": [round(x, 3) for x in p[-6:]]} for o, p in prog.items()}


def curiosidad_de(c, objeto):
    k = (id(c), sum(len(s_) for o_ in c.objetos.values() for s_ in o_["situaciones"].values()))
    if E["clave"] != k: E["curio"], E["detalle"] = calcula(c); E["clave"] = k
    return E["curio"].get(objeto, NACIMIENTO)


def aplica(clase, registra=None):
    if not ON: return {"P7_58": False}
    def curiosidad(c, mundo, objeto, cautela=1.0): return curiosidad_de(c, objeto) * cautela
    FI.curiosidad = curiosidad
    return {"P7_58": True, "nacimiento": NACIMIENTO}

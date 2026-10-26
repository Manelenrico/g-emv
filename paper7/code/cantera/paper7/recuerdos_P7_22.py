"""[P7-22] LOS RECUERDOS DEL BOTIQUIN, SACADOS DEL DIARIO: uno por canal abierto (completado o cortado), con su contexto, su foto emocional
al abrir, su efecto y su intensidad. Lectura de los 160 diarios de APRENDE de los dos campos (P7-10 y P7-14b), posterior a los sellos. Coste cero.
  python3 recuerdos_P7_22.py -> P7_22_recuerdos.json

REGLAS, escritas antes de contar (las del encargo, mas las dos que el encargo deja abiertas y que fijo aqui):
  CANAL, DENTRO, GOLPEADA EN LOS 48 ANTERIORES, SE COMPLETA, CAUSA DEL CORTE: las de P7-21 (`analiza_P7_21.canales`, importado).
  FOTO EMOCIONAL al abrir: la de P7-21 (`emocion_P7_21`): dolor por dominio (suma de las filas con signo -, en F, R y S), positivo total (suma de
    las filas con +) y distancia total `d_ahora`. Vector de 5: (dolor F, dolor R, dolor S, positivo, d).
  EFECTO del recuerdo: completado -> cuerpo = lo que subio la vida al cerrarse el canal (vida al cerrar menos vida en el ultimo tic abierto,
    mas el dano recibido en el tic del cierre; entre 0 y la cura del catalogo, 50), recursos = -1 (un botiquin menos), vinculo = 0.
    Cortado -> 0 en los tres (el dano que lo corta se atribuye a su causa conocida; no se gasta).
  INTENSIDAD (abierta en el encargo; la fijo asi): 1 + min(1, efecto_cuerpo / 50): un corte pesa 1, una cura entera 2 (el tope del cuaderno).
  DIA: el dia de la serie (d de la carpeta). TIC DE LA ELECCION: el ultimo tic antes de abrirse en que lo elegido fue `usar_botiquin`.
"""
import glob, json, os
from multiprocessing import Pool
import analiza_P7_16 as A16, analiza_P7_21 as A21
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
CURA = 50.0


def foto_de(r):
    a = (r.get("RADIOGRAFIA") or {}).get("ahora") or {}; filas = a.get("filas") or {}
    dol = {"F": 0.0, "R": 0.0, "S": 0.0}; pos = 0.0
    for fila in filas.values():
        if fila.get("signo") == "-":
            for dom in ("F", "R", "S"): dol[dom] += float(fila.get(dom) or 0.0)
        else: pos += float(fila.get("M") or 0.0)
    return {"dolor_F": round(dol["F"], 4), "dolor_R": round(dol["R"], 4), "dolor_S": round(dol["S"], 4), "positivo": round(pos, 4), "d": (r.get("RADIOGRAFIA") or {}).get("d_ahora"),
            "filas": {k: (v.get("signo"), round(float(v.get("M") or 0.0), 4)) for k, v in filas.items()}}


def una_carpeta(x):
    campo, carp = x; b = os.path.basename(carp).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); out = {}
    for sl in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))
        if not f: continue
        M, T = A16.lee(f[0])
        if not T: continue
        X = A21.lee_extra(f[0]); murio = (M["final"] or {}).get("reason") == "eliminated"
        C = A21.canales(T, X, M); idx = {t["t"]: i for i, t in enumerate(T)}
        quiero = {c["t0"] for c in C}; fotos = {}; hp_ultimo = {}
        for line in open(f[0]):
            if '"k": "tick"' not in line and '"k":"tick"' not in line: continue
            try: r = json.loads(line)
            except Exception: continue
            if r.get("k") == "tick" and r.get("tick") in quiero: fotos[r["tick"]] = foto_de(r)
        rec = []
        for c in C:
            i0 = idx[c["t0"]]; i1 = i0
            while i1 + 1 < len(T) and T[i1 + 1]["canal"]: i1 += 1
            ic = i1 + 1 if i1 + 1 < len(T) else i1
            dano_cierre = sum(a for _, a in T[ic]["dmg"])
            ef = max(0.0, min(CURA, T[ic]["hp"] - T[i1]["hp"] + dano_cierre)) if c["completado"] else 0.0
            j = i0 - 1
            while j >= 0 and T[j]["el"] != "usar_botiquin" and i0 - j <= 48: j -= 1
            t_el = T[j]["t"] if j >= 0 and T[j]["el"] == "usar_botiquin" else None
            rec.append({"dia": dia, "t0": c["t0"], "t_eleccion": t_el, "dentro": c["dentro"], "golpeado_48": c["golpeado_48"], "golpeado_24": c["golpeado_24"], "completado": c["completado"], "causa_corte": c["causa_corte"],
                        "hp0": c["hp0"], "hp_ultimo_abierto": T[i1]["hp"], "hp_cierre": T[ic]["hp"], "dura": c["dura"], "foto": fotos.get(c["t0"]),
                        "efecto": {"cuerpo": round(ef, 2), "recursos": -1.0 if c["completado"] else 0.0, "vinculo": 0.0}, "intensidad": round(1.0 + min(1.0, ef / CURA), 4)})
        out[f"{campo}|s{serie}_d{dia}_APRENDE_{sl}"] = {"campo": campo, "serie": serie, "dia": dia, "slot": sl, "murio": murio, "ultimo_tick": T[-1]["t"], "recuerdos": rec}
    return out


if __name__ == "__main__":
    carps = [("P7-10", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s*_d*_APRENDE_*")))] + [("P7-14b", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d*_APRENDE_*")))]
    OUT = {}
    with Pool(4) as P:
        for o in P.imap_unordered(una_carpeta, carps): OUT.update(o)
    json.dump(dict(sorted(OUT.items())), open(os.path.join(AQUI, "P7_22_recuerdos.json"), "w"), ensure_ascii=False, indent=0)
    R = [r for v in OUT.values() for r in v["recuerdos"]]
    print("vidas", len(OUT), "· recuerdos", len(R), "· completados", sum(1 for r in R if r["completado"]), "· con foto", sum(1 for r in R if r["foto"]), "· con tic de eleccion", sum(1 for r in R if r["t_eleccion"] is not None))

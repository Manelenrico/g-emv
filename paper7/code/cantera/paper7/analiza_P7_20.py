"""[P7-20] LA VIDA EN EL PRIMER GOLPE (propuesta de Ari). Lectura de los 640 diarios de los dos campos (P7-10 y P7-14b), posterior a los sellos.
Coste cero: solo se leen diarios. La lectura del diario es la de P7-16 (`analiza_P7_16.lee`, importada, no copiada).
  python3 analiza_P7_20.py -> P7_20_vidas.json

DEFINICIONES, escritas aqui ANTES de contar:
  GOLPE DE RIVAL: una entrada de `damage_taken` cuya fuente empieza por "P" (un jugador). DANO DEL ANILLO: fuente "zone".
  RACHA DE DANO: tics con dano (de rival o del anillo) seguidos sin un hueco de mas de 10 segundos (240 tics) entre uno y el siguiente.
  PELEA: una racha de dano con al menos un golpe de rival.
  PRIMER GOLPE (la definicion del encargo, al pie de la letra): el primer dano de rival despues de 10 segundos sin dano de ninguna clase; es
    decir, el primer dano de la racha, cuando ese primer dano es de un rival. Si la racha empieza con dano del anillo y el rival pega despues,
    esa pelea NO tiene primer golpe con esta definicion; se cuenta aparte y se da, como variante, la vida ante el primer golpe de rival de la racha.
  LA VIDA EN EL PRIMER GOLPE: la vida del tic anterior a ese golpe (la que tenia al recibirlo), como "desde que vida" en P7-16.
  LA PELEA ACABA EN MUERTE: la vida muere (`final.reason` = "eliminated") y es su ultima racha de dano, con el ultimo dano a 240 tics o menos del
    ultimo tic de la vida.
  MUERTE TEMPRANA: muere antes del tic 11.000; y, aparte, antes del 12.000 (los dos cortes de P7-15 y P7-16).
"""
import glob, json, os
from multiprocessing import Pool
import analiza_P7_16 as A16
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
HUECO = A16.HUECO                                                                   # 240 tics = 10 s, el de P7-16


def peleas(M, T, murio):
    D = [i for i, t in enumerate(T) if any(s.startswith("P") or s == "zone" for s, _ in t["dmg"])]
    rachas = []; r = []
    for i in D:
        if r and T[i]["t"] - T[r[-1]]["t"] > HUECO: rachas.append(r); r = []
        r.append(i)
    if r: rachas.append(r)
    out = []
    for k, r in enumerate(rachas):
        riv = [i for i in r if any(s.startswith("P") for s, _ in T[i]["dmg"])]
        if not riv: continue
        i0 = r[0]; ir = riv[0]; antes = lambda i: (T[i - 1]["hp"] if i > 0 else None)
        empieza_rival = any(s.startswith("P") for s, _ in T[i0]["dmg"])
        ultima = k == len(rachas) - 1
        out.append({"t0": T[i0]["t"], "t_primer_golpe_de_rival": T[ir]["t"], "empieza_con_golpe_de_rival": empieza_rival,
                    "vida_en_el_primer_golpe": (antes(i0) if empieza_rival else None), "vida_ante_el_primer_golpe_de_rival": antes(ir),
                    "dura_tics": T[r[-1]]["t"] - T[i0]["t"], "dano_de_rivales": round(sum(a for i in r for s, a in T[i]["dmg"] if s.startswith("P")), 1),
                    "dano_del_anillo": round(sum(a for i in r for s, a in T[i]["dmg"] if s == "zone"), 1), "golpes_de_rival": sum(1 for i in r for s, a in T[i]["dmg"] if s.startswith("P")),
                    "primer_golpe_cuanto": round(sum(a for s, a in T[ir]["dmg"] if s.startswith("P")), 1), "ultimo_golpe_cuanto": round(sum(a for s, a in T[r[-1]]["dmg"]), 1),
                    "botiquines_al_empezar": T[i0]["kits"], "vida_al_acabar": T[r[-1]]["hp"],
                    "acaba_en_muerte": bool(murio and ultima and T[-1]["t"] - T[r[-1]]["t"] <= HUECO)})
    return out


def una_carpeta(x):
    campo, carp = x; b = os.path.basename(carp).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = "ESPERANZA" if b[3] == "SUELO" else b[3]; out = {}
    for sl in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))
        if not f: continue
        M, T = A16.lee(f[0])
        if not T: continue
        murio = (M["final"] or {}).get("reason") == "eliminated"
        hp = []                                                                     # la vida, solo donde cambia: (tic, vida)
        for t in T:
            if not hp or hp[-1][1] != t["hp"]: hp.append((t["t"], t["hp"]))
        out[f"{campo}|s{serie}_d{dia}_{brazo}_{sl}"] = {"campo": campo, "serie": serie, "dia": dia, "brazo": brazo, "slot": sl, "semilla": int(b[4]), "primer_tick": T[0]["t"], "ultimo_tick": T[-1]["t"],
                                                         "murio": murio, "vida_maxima_vista": max(t["hp"] for t in T), "peleas": peleas(M, T, murio), "vida": hp}
    return out


if __name__ == "__main__":
    carps = [("P7-10", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s*_d*_*_*")))] + [("P7-14b", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d*_*_*")))]
    OUT = {}
    with Pool(4) as P:
        for o in P.imap_unordered(una_carpeta, carps): OUT.update(o)
    json.dump(dict(sorted(OUT.items())), open(os.path.join(AQUI, "P7_20_vidas.json"), "w"), ensure_ascii=False)
    print("vidas", len(OUT), "· peleas", sum(len(v["peleas"]) for v in OUT.values()), "· que acaban en muerte", sum(1 for v in OUT.values() for p in v["peleas"] if p["acaba_en_muerte"]))

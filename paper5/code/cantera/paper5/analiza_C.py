"""[P5-1 fase C] Las medidas C1 a C7 sobre los seis asientos-partida.

SOLO LECTURA sobre los .art.log de paintball/runs/P5_*. Vuelca
cantera/paper5/C_medidas.json.

CRITERIOS, declarados:
  · calma LITERAL  = ninguna fila del presente con M > 0,1 y ningun ARMADO a
    la vista. Es literalmente el de `cantera/paper4/la_calma.py:63-64`.
  · calma DECLARADA = ninguna fila de las familias F- y S- por encima de 0,1
    y ningun ARMADO a la vista. Las filas R- (carencia, llamada, acopio)
    pueden estar encendidas: es el hambre, que no depende del anillo.
    El umbral 0,1 es el mismo de la literal, para que las dos se comparen.
  · ARMADO = agente visible que NO es el hermano y cuya mano no es
    `none` ni `net` (`la_calma.py:9-10`).
  · la medida DEL PAPER CUATRO = ninguna fila con M > 0, que es el criterio
    exacto de `cantera/paper4/calma_S2.py:5`.
  · VISTA = 8 casillas, Chebyshev, como en `la_calma.py:19`.
"""
from __future__ import annotations
import collections, glob, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N, VISTA = 48, 8
NO_ARMA = (None, "none", "net")
UMBRAL = 0.1
IGNICION = 481          # freeze_ticks 480 + 1


def familia(nombre):
    return nombre.split("-", 1)[0]


def clase_accion(el):
    if el == "noop":
        return "noop"
    if el == "ir_centro":
        return "ir_centro"
    if el == "ir_botin":
        return "ir_botin"
    return "otros"


def mide(f, participantes):
    recs = []
    for ln in open(f):
        try:
            recs.append(json.loads(ln))
        except Exception:
            pass
    pc = next((r for r in recs if r.get("k") == "player_config"), {})
    fin = next((r for r in recs if r.get("k") == "final"), {})
    herm = pc.get("teammate_slot")
    slot = pc.get("slot")

    M = {"fichero": os.path.basename(f), "slot": slot,
         "hermano": herm, "final": fin}
    vivos = 0
    c_lit = c_dec = c_p4 = 0
    acc = {"literal": collections.Counter(), "declarada": collections.Counter(),
           "fuera": collections.Counter(), "todo": collections.Counter()}
    manda = collections.Counter()
    viva = collections.Counter()
    nuevas = {"literal": 0, "declarada": 0, "fuera": 0}
    visto = set()
    # C6
    prim_armado = prim_dano = None
    prim_dano_fuente = None
    muerte_tick = muerte_causa = None
    golpes = []          # (tick, fuente) de todos los golpes recibidos
    # C7: primer tramo, desde IGNICION
    tramo = {"literal": 0, "declarada": 0}
    roto = {"literal": None, "declarada": None}   # {tick, fila, valor}
    ult = None

    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        t = r["tick"]
        R = r.get("RADIOGRAFIA") or {}
        ahora = R.get("ahora") or {}
        if not ahora:
            continue
        vivos += 1
        ult = r
        fil = ahora.get("filas") or {}
        mx = max([float((v or {}).get("M") or 0.0) for v in fil.values()] or [0.0])
        mx_fs = max([float((v or {}).get("M") or 0.0)
                     for k, v in fil.items()
                     if familia(k) in ("F", "S")] or [0.0])
        act = {k for k, v in fil.items() if float((v or {}).get("M") or 0.0) > 0}
        for k in act:
            viva[k] += 1
        if fil:
            manda[max(fil, key=lambda k: float((fil[k] or {}).get("M") or 0.0))] += 1

        vis = [a for a in (r.get("ve_agentes") or []) if a.get("slot") != herm]
        arm = [a for a in vis if (a.get("hand") or "none") not in NO_ARMA]
        if arm and prim_armado is None and t >= IGNICION:
            prim_armado = {"tick": t, "slot": arm[0].get("slot"),
                           "mano": arm[0].get("hand")}
        for g in (r.get("damage_taken") or []):
            if prim_dano is None and t >= IGNICION:
                src = g.get("source")
                prim_dano = t
                prim_dano_fuente = src
            muerte_causa = g.get("source")
            muerte_tick = t
            golpes.append((t, g.get("source")))

        lit = (mx <= UMBRAL) and not arm
        dec = (mx_fs <= UMBRAL) and not arm
        p4 = not act
        c_lit += lit; c_dec += dec; c_p4 += p4
        # C7: el primer tramo desde la ignicion, y QUE lo rompe
        for nom, ok, cand in (("literal", lit, fil),
                              ("declarada", dec,
                               {k: v for k, v in fil.items()
                                if familia(k) in ("F", "S")})):
            if t < IGNICION or roto[nom] is not None:
                continue
            if ok:
                tramo[nom] += 1
                continue
            if arm:
                roto[nom] = {"tick": t, "fila": None,
                             "motivo": f"armado a la vista (asiento "
                                       f"{arm[0].get('slot')}, "
                                       f"{arm[0].get('hand')})"}
            else:
                peor = max(cand, key=lambda k: float((cand[k] or {}).get("M") or 0))
                roto[nom] = {"tick": t, "fila": peor,
                             "valor": round(float((cand[peor] or {}).get("M") or 0), 4),
                             "motivo": "fila por encima de 0,1"}

        el = R.get("elegido") or ""
        cl = clase_accion(el)
        acc["todo"][cl] += 1
        acc["declarada" if dec else "fuera"][cl] += 1
        if lit:
            acc["literal"][cl] += 1
        # C2: casillas nuevas
        pos = r.get("pos")
        antes = len(visto)
        if pos:
            for y in range(max(0, pos[1]-VISTA), min(N, pos[1]+VISTA+1)):
                for x in range(max(0, pos[0]-VISTA), min(N, pos[0]+VISTA+1)):
                    visto.add((x, y))
        n_nuevas = len(visto) - antes
        if lit:
            nuevas["literal"] += n_nuevas
        if dec:
            nuevas["declarada"] += n_nuevas
        else:
            nuevas["fuera"] += n_nuevas

    M.update({
        "tics vivos": vivos,
        "calma literal": c_lit, "calma declarada": c_dec,
        "medida del paper cuatro (ninguna fila M>0)": c_p4,
        "primer tramo de calma desde 481": {
            "literal": {"tics": tramo["literal"], "lo rompe": roto["literal"]},
            "declarada": {"tics": tramo["declarada"],
                          "lo rompe": roto["declarada"]}},
        "acciones": {k: dict(v) for k, v in acc.items()},
        "casillas nuevas": nuevas,
        "tics en calma declarada": c_dec,
        "tics fuera de calma declarada": vivos - c_dec,
        "fila que manda": dict(manda.most_common()),
        "filas vivas (M>0)": dict(viva.most_common()),
        "C6": {"primer armado a la vista": prim_armado,
               "primer dano": ({"tick": prim_dano, "fuente": prim_dano_fuente}
                               if prim_dano else None),
               "ultimo golpe registrado": {"tick": muerte_tick,
                                           "fuente": muerte_causa},
               "golpes en los ultimos 48 tics vistos": [
                   {"tick": a, "fuente": b} for a, b in golpes
                   if ult and a >= (ult.get("tick") or 0) - 48],
               "vida en el ultimo tic visto": (ult or {}).get("hp"),
               "dentro del anillo en el ultimo tic": (
                   None if not ult or not ult.get("pos") else
                   (max(abs(ult["pos"][0] - ((ult.get("zona") or {}).get("center") or [24, 24])[0]),
                        abs(ult["pos"][1] - ((ult.get("zona") or {}).get("center") or [24, 24])[1]))
                    <= ((ult.get("zona") or {}).get("radius") or 99))),
               "match_ticks": fin.get("match_ticks"),
               "reason": fin.get("reason"),
               "placement": fin.get("placement"),
               "kills": fin.get("kills"), "score": fin.get("score")},
        "ultimo tic visto": ult.get("tick") if ult else None,
    })
    return M


def main():
    out = {}
    for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P5_*"))):
        nom = os.path.basename(carp)
        parts = {}
        pj = os.path.join(AQUI, nom.replace("P5_", "") + "_peticion.json")
        if os.path.exists(pj):
            d = json.load(open(pj))
            parts = {p["position"]: p["policy_name"]
                     for p in d["episodes"][0]["participants"]}
        for f in sorted(glob.glob(os.path.join(carp, "*.art.log"))):
            k = nom + "/" + os.path.basename(f).split("policy_agent_")[1][:2].strip(".")
            out[k] = mide(f, parts)
            out[k]["participants"] = parts
    json.dump(out, open(os.path.join(AQUI, "C_medidas.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"asientos-partida medidos: {len(out)}")
    for k, m in out.items():
        v = m["tics vivos"] or 1
        print(f"\n=== {k} · slot {m['slot']} · {m['tics vivos']:,} tics vivos "
              f"· match_ticks {m['C6']['match_ticks']} ({m['C6']['reason']}, "
              f"puesto {m['C6']['placement']})")
        print(f"  calma literal   {m['calma literal']:6,} = {100*m['calma literal']/v:6.2f} %")
        print(f"  calma declarada {m['calma declarada']:6,} = {100*m['calma declarada']/v:6.2f} %")
        print(f"  paper cuatro    {m['medida del paper cuatro (ninguna fila M>0)']:6,}")
        for nom in ("literal", "declarada"):
            x = m["primer tramo de calma desde 481"][nom]
            print(f"  primer tramo {nom:10s}: {x['tics']} tics · lo rompe {x['lo rompe']}")
        print(f"  C6: {m['C6']['primer armado a la vista']} · dano {m['C6']['primer dano']} "
              f"· ultimo golpe {m['C6']['ultimo golpe registrado']}")


if __name__ == "__main__":
    main()

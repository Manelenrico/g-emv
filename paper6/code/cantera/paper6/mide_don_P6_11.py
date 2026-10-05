"""[P6-5 · 5] EL DON DEL PAPER TRES, con y sin ojos compartidos. SOLO LECTURA.

El cuerpo del cinco sigue teniendo el don: `S-HERIDO` y `S-PROVISION` empujan a
SOLTAR una venda o una racion junto al hermano, y el candidato `soltar_<id>`
deja el objeto EN MI PROPIA CASILLA (`decisor_zs.py:820-822`) y lo marca como
CEDIDO (`:900-903`).

POR QUE NO SE CUENTA POR TICS (medido, no supuesto). En A0, el diario
P64_t3_A0_22250767 asiento 10 elige `soltar_first_aid` en 4.260 tics. Al mirar
los tics uno a uno aparece un CICLO DE DOS TICS:

    1198 soltar_first_aid  drop   ok  pack={'first_aid':2}  suelo=[]
    1199 coger             pickup ok  pack={}               suelo=['first_aid']
    1200 soltar_first_aid  drop   ok  pack={'first_aid':2}  suelo=[]

`drop` suelta la PILA ENTERA en la propia casilla; al tic siguiente el cuerpo la
ve bajo sus pies, `coger` gana, y vuelve a soltar. El objeto nunca se va. Contar
tics mide tics de bucle, no dones. Por eso aqui se cuenta:

  INTENTO   : un tic con elegido `soltar_<id>`.
  EPISODIO  : racha maxima de intentos en la MISMA casilla y el MISMO id, con
              huecos <= HUECO tics. Un episodio = un acto de dejar algo.
  REABSORBIDO: tras el ultimo intento del episodio, el que solto vuelve a tener
              el id en su pack estando en esa casilla. Se lo ha recogido el.
  EFECTIVO  : el episodio acaba con el objeto en el suelo (el que solto se va de
              la casilla, o muere, sin recuperarlo).
  RECOGIDO  : el HERMANO pisa esa casilla despues de un episodio EFECTIVO y su
              `pack` sube en ese id (o le llega a la mano).
  USADO     : despues de recogerlo, su `pack` de ese id BAJA.
  VIAJA     : el objeto soltado aparece en algun parte E2 del que lo solto, como
              recurso contado, despues del primer intento del episodio.

Uso:
  python3 mide_don_P6_5.py A0=paintball/runs/P64_t[13]_A0_* A1=paintball/runs/P64_t[24]_A1_*
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U
import parte2 as P2

NUESTROS = (10, 11)
HUECO = 3          # tics de hueco que siguen contando como el mismo episodio
                   # (el bucle medido alterna drop/coger: hueco de 2)


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    voz = [r for r in recs if r.get("k") in ("voz", "ojos")
           and (r.get("texto") or "")]
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        T[r["tick"]] = {
            "pos": tuple(r.get("pos") or ()), "hp": r.get("hp"),
            "el": ra.get("elegido"),
            "hand": (r.get("hand") or {}).get("id"),
            "pack_n": {(s or {}).get("id"): int((s or {}).get("n") or 1)
                       for s in (r.get("pack") or []) if s},
            "suelo": {(int(x["pos"][0]), int(x["pos"][1])): x.get("id")
                      for x in (r.get("ve_items") or []) if x.get("pos")},
        }
    del recs
    return mundo, T, voz


def episodios(T):
    """Agrupa los tics con `soltar_<id>` en episodios (casilla, id, racha)."""
    eps, abierto = [], {}
    for t in sorted(T):
        el = str(T[t]["el"] or "")
        if not el.startswith("soltar_"):
            continue
        iid, cel = el[len("soltar_"):], T[t]["pos"]
        k = (iid, cel)
        e = abierto.get(k)
        if e is not None and t - e["fin"] <= HUECO:
            e["fin"], e["intentos"] = t, e["intentos"] + 1
            continue
        e = {"id": iid, "casilla": cel, "ini": t, "fin": t, "intentos": 1}
        abierto[k] = e
        eps.append(e)
    return eps


def destino(T, e):
    """Tras el ultimo intento: REABSORBIDO por el que solto, o EFECTIVO."""
    iid, cel = e["id"], e["casilla"]
    ant = T[e["fin"]]
    npre = ant["pack_n"].get(iid, 0)
    for t in sorted(x for x in T if x > e["fin"]):
        r = T[t]
        if r["pos"] == cel and r["pack_n"].get(iid, 0) >= npre:
            return "reabsorbido", t
        if r["pos"] != cel:
            return "efectivo", t          # se va y lo deja
    return "efectivo", None               # muere (o acaba) sin recuperarlo


def mide(pat):
    S, DET = collections.Counter(), []
    for carp in sorted(glob.glob(pat)):
        E, mundo = {}, None
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl not in NUESTROS:
                continue
            m, T, voz = carga(f)
            mundo = mundo or m
            E[sl] = {"T": T, "voz": voz}
        if len(E) != 2:
            continue
        S["partidas"] += 1
        AL = P2.alfabeto(mundo)
        a, b = NUESTROS
        for sl in NUESTROS:
            T, To = E[sl]["T"], E[b if sl == a else a]["T"]
            S["tics vividos"] += len(T)
            for e in episodios(T):
                iid, cel = e["id"], e["casilla"]
                S["INTENTOS (tics soltar_*)"] += e["intentos"]
                S["EPISODIOS de don"] += 1
                if e["intentos"] >= 3:
                    S["  episodios en BUCLE (>=3 intentos)"] += 1
                    S["  tics perdidos en el bucle"] += e["fin"] - e["ini"] + 1
                dest, tdest = destino(T, e)
                d = {"carp": os.path.basename(carp), "slot": sl,
                     "id": iid, "casilla": list(cel), "ini": e["ini"],
                     "fin": e["fin"], "intentos": e["intentos"],
                     "destino": dest, "t_destino": tdest}
                if dest == "reabsorbido":
                    S["  REABSORBIDO por el que solto"] += 1
                    DET.append(d)
                    continue
                S["  EFECTIVO (queda en el suelo)"] += 1
                S[f"    efectivo de {iid}"] += 1
                # ¿VIAJA en un parte E2 del que lo solto?
                letra = AL.get(iid)
                clave = f"{letra}{cel[0]},{cel[1]}" if letra else None
                if clave:
                    for v in E[sl]["voz"]:
                        if v.get("tick", 0) >= e["ini"] and clave in (v.get("texto") or ""):
                            d["viaja_en_E2"] = v["tick"]
                            S["    ...VIAJA en un parte E2"] += 1
                            break
                # ¿lo recoge el HERMANO?
                rec, ant = None, None
                for tt in sorted(To):
                    if tt <= e["fin"]:
                        ant = To[tt]
                        continue
                    if To[tt]["pos"] == cel:
                        n0 = (ant or To[tt])["pack_n"].get(iid, 0)
                        if (To[tt]["pack_n"].get(iid, 0) > n0
                                or (iid == (To[tt]["hand"] or "")
                                    and iid != ((ant or {}).get("hand") or ""))):
                            rec = tt
                            break
                    ant = To[tt]
                d["recoge_hermano"] = rec
                if rec is None:
                    S["    ...NO lo recoge el hermano"] += 1
                else:
                    S["    ...lo RECOGE el hermano"] += 1
                    d["tics_hasta_recoger"] = rec - e["fin"]
                    nref = To[rec]["pack_n"].get(iid, 0)
                    for tt in sorted(x for x in To if x > rec):
                        if To[tt]["pack_n"].get(iid, 0) < nref:
                            d["usa"] = tt
                            S["    ...y lo USA"] += 1
                            break
                DET.append(d)
        del E
    return S, DET


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    print(f"### {etiq}", flush=True)
    S, DET = mide(os.path.join(RAIZ, pat))
    OUT[etiq] = {"recuento": dict(S), "detalle": DET}
    for k in ("partidas", "tics vividos", "INTENTOS (tics soltar_*)",
              "EPISODIOS de don", "  episodios en BUCLE (>=3 intentos)",
              "  tics perdidos en el bucle", "  REABSORBIDO por el que solto",
              "  EFECTIVO (queda en el suelo)", "    efectivo de first_aid",
              "    efectivo de rations", "    ...VIAJA en un parte E2",
              "    ...lo RECOGE el hermano", "    ...y lo USA",
              "    ...NO lo recoge el hermano"):
        if k in S:
            print(f"  {k:40s} {S[k]}")
json.dump(OUT, open(os.path.join(AQUI, "P6_11_don.json"), "w"),
          ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_11_don.json")

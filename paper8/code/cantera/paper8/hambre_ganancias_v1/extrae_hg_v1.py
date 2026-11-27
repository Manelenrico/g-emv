"""[P8] Prompt 144: de dónde sale el hambre de más de RG68r. Lee las partidas selladas del experimento v5 (RG68r y su gemela RG068r, sequía dura y sequía,
semillas 30121 a 30140, días 0 a 9: turnos 0 a 3999). Solo lee los registros: no juega nada ni llama a ningún modelo.
LAS REGLAS:
  - EL HAMBRE de un turno es la que apunta el mundo después del turno (mundo.jsonl.gz). EL HAMBRE AL HACER ALGO (comer, coger, empezar a ir) es la del
    turno de antes: la que tenía al decidirlo.
  - TURNOS DESPIERTA CON HAMBRE > 30 Y > 60: turnos viva y no dormida (cuerpo.dormida) con esa hambre; cada uno va a uno de tres montones: lleva comida en
    la bolsa; si no, hay comida en la despensa de su casa (criaturas.jsonl.gz, «despensas»; la casa es la letra de su nombre, mundo.py:68); si no, en
    ninguna.
  - CADA COSA DE LA BOLSA SE SIGUE UNA A UNA. Las reglas del mundo (valle/mundo.py:773-827 y 900-907): lo que coge entra al final; al comer, dar o dejar
    sale la primera que encaja (por tipo y, al comer y dar, por origen: el mundo apunta el origen de lo comido y lo dado); el que gana un empujón se lleva
    la bolsa entera de la otra, en orden, hasta llenar la suya. Las acciones se aplican en el orden del turno («orden»). Al acabar el turno, la bolsa que
    llevo se cuadra con la que apunta el mundo (por tipo y origen, en orden): lo que sobra se ha podrido (o, si ese turno la bestia le robó, se lo quitó
    la bestia; mundo.py:1035-1053: el mundo no apunta qué se pudre); lo que falta entra como «desconocido». Lo que tiene en la bolsa en el primer turno
    es «inicial». Lo que lleva cuántos se cuadró a mano va en «descuadres».
  - DESTINO DE LO QUE COGE (cada «coger» con éxito de comida): la primera vez que sale de su bolsa: se la come ella, la da, se la quitan (un empujón que
    pierde o la bestia), la guarda (dejar: en la despensa, el almacén o el suelo) o se pudre; si no sale, sigue en la bolsa al acabar el día 9 o al morir.
    De dónde la coge: planta (huerto), matorral, suelo, almacén o despensa.
  - CADA COMIDA: el turno, la fase del día (mañana, tarde, anochecer, noche: el mundo), el sitio (balance.jsonl.gz: C casa propia por dentro, P su puerta,
    O otra casa, y aldea, huerto, bosque…), el hambre de antes y DE DÓNDE SALE: de la despensa o del almacén si así entró en su bolsa; «recién cogida» si
    la cogió de una planta, un matorral o el suelo hace 10 turnos o menos (lo más simple: 10 turnos); si no, «bolsa» (lo que lleva un rato, lo inicial, lo
    recibido o lo ganado en un empujón). Y si esa mañana amaneció en casa (sitio C en el primer turno del día).
  - IR A POR COMIDA, lo que deja el registro del mundo (igual para las dos): un VIAJE empieza con los «mover» seguidos justo antes de un «coger» de comida
    que no es de la despensa y sigue con los «coger» de comida que vengan (con o sin «mover» entre ellos); se acaba con cualquier otra acción. Turnos
    dedicados = esos «mover» y «coger»; comida ganada = los «coger» con éxito de un viaje; el hambre con que empieza = la del turno de antes del primero.
    Los turnos de trabajar el huerto van aparte.
  - DEL REGISTRO DE DECISIONES (solo RG68r; la gemela no lo tiene): opciones de ir a por comida = ir_matorral, ir_objeto, ir_botin y coger (lo más simple:
    las que llevan a coger algo; ir_objeto también puede ser medicina). La primera de cada día y su hambre; y los turnos «dedicados» según el registro:
    cada turno lleva el nombre de la última decisión suya (entre decisiones sigue un destino o una cola).
Guarda hambre_ganancias_v1/datos/<variante>_<mundo>_<semilla>.json.
   python3 hambre_ganancias_v1/extrae_hg_v1.py   (las 80; o una: python3 hambre_ganancias_v1/extrae_hg_v1.py RG68r sequia 30121)"""
import gzip, json, os, sys
from collections import defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path[:0] = [os.path.join(P8, "gemela_v5")]
import extrae_gemela_v5 as EG
EXP = EG.EXP; DIA = EG.DIA; HASTA = 10 * DIA; CFGV = EG.CFGV; HUECOS = CFGV["criaturas"]["bolsa_huecos"]
VARIANTES = ("RG68r", "RG068r"); MUNDOS = ("sequia_dura", "sequia"); SEM = range(30121, 30141)
FUERA_DESP = ("planta", "matorral", "suelo", "almacen"); RECIEN = 10; COMIDA_OP = ("ir_matorral", "ir_objeto", "ir_botin", "coger")
DIAS_CAMPOS = ("turnos", "despierta", "h30_bolsa", "h30_despensa", "h30_nada", "h60_bolsa", "h60_despensa", "h60_nada", "comidas", "dedicados", "ganada",
               "trabajando", "dedicados_reg")

def una(x):
    v, mu, s = x; d = os.path.join(EXP, f"{v}_{mu}+sabores_s{s}_d40"); out = os.path.join(AQUI, "datos", f"{v}_{mu}_{s}.json")
    if os.path.exists(out): return out
    D = defaultdict(lambda: {k: 0 for k in DIAS_CAMPOS}); comidas = []; cogidas = []; viajes = []; primera_reg = {}; descuadre = defaultdict(int)
    B = {}; hprev = {}; viaje = {}; corre = defaultdict(list); amanece = {}; ult_dec = {}
    DEC = defaultdict(list)
    if os.path.exists(os.path.join(d, "decisiones.jsonl.gz")):
        for l in gzip.open(os.path.join(d, "decisiones.jsonl.gz"), "rt", encoding="utf-8"):
            r = json.loads(l)
            if r[0] < HASTA: DEC[r[0]].append((r[1], r[2]))
    def sale(tag, como, t):
        if tag.get("i") is not None and cogidas[tag["i"]]["destino"] is None: cogidas[tag["i"]].update(destino=como, t_fin=t)
    fm = gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"); fb = gzip.open(os.path.join(d, "balance.jsonl.gz"), "rt", encoding="utf-8")
    fc = gzip.open(os.path.join(d, "criaturas.jsonl.gz"), "rt", encoding="utf-8")
    for lm, lb, lc in zip(fm, fb, fc):
        m = json.loads(lm); b = json.loads(lb); c = json.loads(lc); t = m["turno"]
        if t >= HASTA: break
        assert b["t"] == t and c["turno"] == t, (t, b["t"], c["turno"])
        A = {a: g for a, g in m["agentes"].items() if a != "bestia" and isinstance(g, dict) and "cuerpo" in g}; dia = t // DIA; fase = m.get("fase")
        robadas = {e["bestia_roba"] for e in m.get("eventos") or [] if e.get("bestia_roba")}
        for a, x_ in DEC.get(t, []): ult_dec[a] = x_
        if not B:                                                                     # (el primer turno: lo que lleva es «inicial»)
            for a, g in A.items(): B[a] = [{"tipo": tp, "org": og, "de": "inicial", "t": -1, "i": None} for tp, og in zip(g["bolsa"], g.get("bolsa_origen") or [None] * len(g["bolsa"]))]
        else:
            for a in m.get("orden") or []:
                g = A.get(a)
                if g is None or a not in B: continue
                k = g.get("accion"); ok = g.get("resultado") == "ok"; tp = g.get("tipo")
                if k == "coger" and ok:
                    tag = {"tipo": tp, "org": "?", "de": g.get("de"), "t": t, "i": None}
                    if tp == "comida":
                        tag["i"] = len(cogidas); cogidas.append({"a": a, "dia": dia, "t": t, "de": g.get("de"), "h": hprev.get(a), "destino": None, "t_fin": None})
                    B[a].append(tag)
                elif k in ("comer", "dar") and ok:
                    og = g.get("origen"); j = next((j for j, o in enumerate(B[a]) if o["tipo"] == tp and o["org"] in (og, "?")), None)
                    if j is None: descuadre["no_lo_encuentro"] += 1; continue
                    tag = B[a].pop(j)
                    if k == "comer":
                        if tp == "comida":
                            fu = tag["de"] if tag["de"] in ("despensa", "almacen") else ("recien" if tag["de"] in ("planta", "matorral", "suelo") and t - tag["t"] <= RECIEN else "bolsa")
                            comidas.append({"a": a, "dia": dia, "t": t, "fase": fase, "sitio": b["c"][a][5], "h": hprev.get(a), "fuente": fu, "amanece_casa": amanece.get((a, dia))})
                            if tag.get("i") is not None and cogidas[tag["i"]]["a"] == a and cogidas[tag["i"]]["destino"] is None: sale(tag, "comida_ella", t)
                            else: sale(tag, "comida_ella", t)
                    else:
                        sale(tag, "dada", t); o_ = g.get("objetivo")
                        if o_ in B: tag["org"] = og; B[o_].append(tag)
                elif k == "dejar" and ok:
                    j = next((j for j, o in enumerate(B[a]) if tp is None or o["tipo"] == tp), None)
                    if j is None: descuadre["no_lo_encuentro"] += 1; continue
                    sale(B[a].pop(j), "guardada_" + str(g.get("en")), t)
                elif k == "empujar" and str(g.get("resultado") or "").startswith("gana "):
                    gana = g["resultado"][5:]; pierde = g.get("objetivo") if gana == a else a
                    if gana in B and pierde in B:
                        for tag in B[pierde]:
                            sale(tag, "quitada", t)
                            if len(B[gana]) < HUECOS: B[gana].append(tag)
                        B[pierde] = []
        for a, g in A.items():                                                         # (cuadrar la bolsa con la del mundo)
            if a not in B: continue
            if g["cuerpo"]["muerta"]:
                for tag in B[a]: sale(tag, "muere_con_ella", t)
                B.pop(a); continue
            L = list(zip(g["bolsa"], g.get("bolsa_origen") or [None] * len(g["bolsa"]))); nuevo = []; j = 0
            for tag in B[a]:
                if j < len(L) and tag["tipo"] == L[j][0] and tag["org"] in (L[j][1], "?"):
                    tag["org"] = L[j][1]; nuevo.append(tag); j += 1
                else:
                    sale(tag, "quitada" if a in robadas else "podrida", t); descuadre["sobra_" + ("bestia" if a in robadas else "podrida")] += 1
            for tp, og in L[j:]: nuevo.append({"tipo": tp, "org": og, "de": "desconocido", "t": t, "i": None}); descuadre["falta"] += 1
            B[a] = nuevo
        for a, g in A.items():                                                         # (lo de cada turno: hambre, montones, viajes)
            if g["cuerpo"]["muerta"]: continue
            z = D[(a, dia)]; h = float(g["cuerpo"]["hambre"]); k = g.get("accion"); z["turnos"] += 1
            if t % DIA == 0: amanece[(a, dia)] = b["c"][a][5] == "C"
            if not g["cuerpo"].get("dormida"):
                z["despierta"] += 1
                mont = "bolsa" if "comida" in g["bolsa"] else ("despensa" if (c.get("despensas") or {}).get(a[0], {}).get("comida", 0) > 0 else "nada")
                if h > 30: z["h30_" + mont] += 1
                if h > 60: z["h60_" + mont] += 1
            if k == "comer" and g.get("resultado") == "ok" and g.get("tipo") == "comida": z["comidas"] += 1
            if k == "trabajar" and g.get("resultado") == "ok": z["trabajando"] += 1
            if ult_dec.get(a) in COMIDA_OP: z["dedicados_reg"] += 1
            if (a, dia) not in primera_reg and ult_dec.get(a) in COMIDA_OP and any(x_[0] == a for x_ in DEC.get(t, [])) and any(x_ == (a, ult_dec[a]) for x_ in DEC.get(t, [])):
                primera_reg[(a, dia)] = {"a": a, "dia": dia, "t": t, "op": ult_dec[a], "h": hprev.get(a)}
            coge = k == "coger" and g.get("de") in FUERA_DESP and (g.get("tipo") == "comida" or (g.get("resultado") != "ok" and g.get("de") in ("planta", "matorral")))
            if k == "mover": corre[a].append((t, hprev.get(a)))
            elif coge:
                if viaje.get(a) is None:
                    run = corre[a]; t0, h0 = run[0] if run else (t, hprev.get(a))
                    viaje[a] = {"a": a, "dia": t0 // DIA, "t0": t0, "h": h0, "turnos": 0, "ganada": 0}; viajes.append(viaje[a])
                    for t_, _ in run: D[(a, t_ // DIA)]["dedicados"] += 1
                    viaje[a]["turnos"] += len(run)
                else:
                    for t_, _ in corre[a]: D[(a, t_ // DIA)]["dedicados"] += 1
                    viaje[a]["turnos"] += len(corre[a])
                corre[a] = []; z["dedicados"] += 1; viaje[a]["turnos"] += 1
                if g.get("resultado") == "ok": z["ganada"] += 1; viaje[a]["ganada"] += 1
            else: corre[a] = []; viaje[a] = None
            hprev[a] = h
    for a, L in B.items():
        for tag in L: sale(tag, "sigue_en_la_bolsa", HASTA)
    res = {"dias": [dict(a=a, dia=dd, **z) for (a, dd), z in sorted(D.items())], "comidas": comidas, "cogidas": cogidas, "viajes": viajes,
           "primera_reg": list(primera_reg.values()), "con_registro": bool(DEC), "descuadres": dict(descuadre)}
    os.makedirs(os.path.dirname(out), exist_ok=True); json.dump(res, open(out, "w")); return out


if __name__ == "__main__":
    if len(sys.argv) == 4: print(una((sys.argv[1], sys.argv[2], int(sys.argv[3]))))
    else:
        with Pool(6) as p:
            for r in p.imap_unordered(una, [(v, mu, s) for v in VARIANTES for mu in MUNDOS for s in SEM]): print(r, flush=True)

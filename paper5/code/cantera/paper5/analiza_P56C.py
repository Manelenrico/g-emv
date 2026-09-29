"""[P5-6C · C2] Las medidas de la serie, por brazo y asiento-partida.

Sin cotejar sellos: eso es al final, sobre las sesenta.

LA MEDIDA PRINCIPAL, declarada: para cada forma aceptada y cada punto de
control alcanzado, la `d` REAL contra la PROYECTADA (las dos las escribe el
diario en el registro `confianza`), y contra la `d` que el brazo A tuvo **en la
misma semilla y en la misma zona del tiempo** (ventana de +-50 tics alrededor
del mismo tic, del diario de A del mismo asiento).
"""
from __future__ import annotations
import collections, glob, json, math, os, statistics as st, sys


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d * 100, (c + m) / d * 100)


def newcombe(k1, n1, k2, n2):
    """Diferencia de dos proporciones, en puntos, con su intervalo al 95 %."""
    p1 = k1 / n1 * 100 if n1 else 0.0
    p2 = k2 / n2 * 100 if n2 else 0.0
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d, d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2),
            d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
VENT_A = 50          # la «misma zona del tiempo»
ARMADA_NO = ("none", "net", None, "")
UMBRAL = 0.1


def lee(f):
    for linea in open(f, encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        try:
            yield json.loads(linea)
        except Exception:
            continue


def carga(tandas):
    """{(brazo, semilla, slot): [registros]} de una o varias tandas."""
    if isinstance(tandas, (str, int)):
        tandas = [tandas]
    out = {}
    for tanda in tandas:
        for d in sorted(glob.glob(os.path.join(
                RAIZ, "paintball", "runs", f"P56C_t{tanda}_*"))):
            base = os.path.basename(d)
            _p, _t, brazo, semilla = base.split("_", 3)
            for f in sorted(glob.glob(os.path.join(d, "*.art.log"))):
                slot = int(f.rsplit("_", 1)[1].split(".")[0])
                out[(brazo, int(semilla), slot)] = list(lee(f))
    return out


def armado(r, herm):
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") != herm and (a.get("hand") or "none") not in ARMADA_NO:
            return True
    return False


def de_uno(recs):
    pc = next((x for x in recs if x.get("k") == "player_config"), None)
    fin = next((x for x in recs if x.get("k") == "final"), None)
    arr = next((x for x in recs if x.get("k") == "arranque"), None)
    herm = (pc or {}).get("teammate_slot")
    vivos = [x for x in recs if x.get("k") == "tick" and x.get("phase") == "live"]
    o = {"lineas": len(recs), "tics_vivos": len(vivos),
         "primer": vivos[0]["tick"] if vivos else None,
         "ultimo": vivos[-1]["tick"] if vivos else None,
         "hp_final": vivos[-1].get("hp") if vivos else None,
         "final": ({k: fin.get(k) for k in
                    ("placement", "kills", "score", "reason", "match_ticks")}
                   if fin else None),
         "diario_entero": bool(fin),
         "interruptores": ((arr or {}).get("entorno_forma") or {}).get("efectivo"),
         }
    if fin and vivos:
        o["cierra_bien"] = (fin.get("match_ticks") == vivos[-1]["tick"] + 1)
    # d por tic, para el cotejo con A
    o["d_por_tic"] = {x["tick"]: (x.get("RADIOGRAFIA") or {}).get("d_ahora")
                      for x in vivos
                      if (x.get("RADIOGRAFIA") or {}).get("d_ahora") is not None}
    o["pos_por_tic"] = {x["tick"]: tuple(x.get("pos") or ()) for x in vivos
                        if x.get("pos")}
    # calma
    lit = 0
    for x in vivos:
        filas = ((x.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas") or {}
        m = [(v.get("M") if isinstance(v, dict) else v) or 0.0
             for v in filas.values()]
        if not armado(x, herm) and all(v <= UMBRAL for v in m):
            lit += 1
    o["calma_literal"] = lit
    # [t2] LA DURACION DE LA DECISION y LOS TICS PERDIDOS.
    # `RADIOGRAFIA.ms` lo escribe `decidir` en los TRES brazos (en A por el
    # camino del cuatro), asi que es la medida comun; `tiempo_tic` solo existe
    # con GEMV_FORMA=1. Un tic vivo del mundo al que no le corresponde un
    # registro es un tic SIN DECISION EMITIDA: la politica emite exactamente
    # una accion por observacion (`policy_cortex.py:953-958`).
    ms_dec = [(x["tick"], (x.get("RADIOGRAFIA") or {}).get("ms"))
              for x in vivos]
    ms_dec = [(t, m) for t, m in ms_dec if m is not None]
    o["ms_decision"] = {
        "n": len(ms_dec),
        "mayores_40_5": sum(1 for _t, m in ms_dec if m > 40.5),
        "mediana": (sorted(m for _t, m in ms_dec)[len(ms_dec) // 2]
                    if ms_dec else None),
        "max": max((m for _t, m in ms_dec), default=None),
    }
    if vivos:
        hay = {x["tick"] for x in vivos}
        esperados = set(range(vivos[0]["tick"], vivos[-1]["tick"] + 1))
        faltan = sorted(esperados - hay)
        o["perdidos"] = {"faltan": len(faltan), "de": len(esperados),
                         "primeros": faltan[:8],
                         "vigia": sum(1 for x in recs
                                      if x.get("k") == "vigia_disparo")}
    # formas
    prop = [x for x in recs if x.get("k") == "forma_propuesta"]
    o["azar"] = [x for x in prop if x.get("origen") == "azar"]
    o["citas"] = [x for x in prop if x.get("origen") != "azar"]
    o["evaluadas"] = [x for x in recs if x.get("k") == "forma_evaluada"]
    o["aceptadas"] = [x for x in recs if x.get("k") == "forma_aceptada"]
    o["caidas"] = [x for x in recs if x.get("k") == "forma_caida"]
    o["confianza"] = [x for x in recs if x.get("k") == "confianza"]
    o["partes"] = [x for x in recs if x.get("k") == "parte"]
    o["hilo"] = [x for x in recs if x.get("k") == "hilo_forma"]
    o["saltadas"] = [x for x in recs if x.get("k") == "forma_cita_saltada"]
    o["frenos"] = [x for x in recs
                   if x.get("k") in ("forma_freno", "forma_freno_ciego")]
    o["spend"] = [x for x in recs if x.get("k") == "forma_spend"]
    o["resumen"] = next((x for x in recs if x.get("k") == "forma_resumen"), None)
    # [C1bis] el cuerpo de cada cita, tal como salio por el cable
    o["cuerpos"] = [x for x in recs if x.get("k") == "forma_cita_cuerpo"]
    tt = [x for x in recs if x.get("k") == "tiempo_tic"]
    if tt:
        ms = sorted(x["ms"] for x in tt if x.get("ms") is not None)
        o["tiempo"] = {"mediana": round(ms[len(ms) // 2], 3),
                       "p95": round(ms[int(len(ms) * 0.95)], 3),
                       "max": round(ms[-1], 3),
                       "en_hilo": sum(1 for x in tt if x.get("en_hilo")),
                       "n": len(ms)}
    return o


def main():
    tandas = sys.argv[1:] or ["1"]
    tanda = "_".join(tandas)
    D = carga(tandas)
    print(f"tanda(s) {', '.join(tandas)}: {len(D)} asientos-partida")
    M = {k: de_uno(v) for k, v in D.items()}
    json_out = {}

    # ── diarios enteros y frenos ─────────────────────────────────────────
    print("\n== DIARIOS Y FRENOS ==")
    malos = []
    for k in sorted(M):
        o = M[k]
        ok = o["diario_entero"] and o.get("cierra_bien")
        if not ok:
            malos.append(k)
        print(f"  {k[0]}/{k[1]}/{k[2]}: {o['lineas']:6,} lineas · vivos "
              f"{o['tics_vivos']:5,} ({o['primer']}..{o['ultimo']}) · "
              f"final {'SI' if o['diario_entero'] else 'NO'} · cierra bien "
              f"{o.get('cierra_bien')} · frenos {len(o['frenos'])} · "
              f"{(o['final'] or {}).get('reason')} puesto "
              f"{(o['final'] or {}).get('placement')}")
    print(f"  --> diarios incompletos: {malos if malos else 'ninguno'}")

    # ── formas, por brazo ────────────────────────────────────────────────
    print("\n== FORMAS, por brazo ==")
    for b in ("A", "F", "T"):
        ks = [k for k in sorted(M) if k[0] == b]
        if not ks:
            continue
        c = collections.Counter()
        acep_por_vida, edad_primera = [], []
        motivos = collections.Counter()
        vered = collections.Counter()
        for k in ks:
            o = M[k]
            c["asientos"] += 1
            c["propuestas"] += len(o["azar"]) + len(o["citas"])
            c["evaluadas"] += len(o["evaluadas"])
            c["aceptadas"] += len(o["aceptadas"])
            c["caidas"] += len(o["caidas"])
            for x in o["evaluadas"]:
                vered[x.get("veredicto")] += 1
            for x in o["caidas"]:
                motivos[(x.get("motivo") or "")[:44]] += 1
            acep_por_vida.append(len(o["aceptadas"]))
            if o["aceptadas"]:
                edad_primera.append(o["aceptadas"][0]["tick"] - (o["primer"] or 0))
        print(f"  {b}: {c['asientos']} asientos · propuestas {c['propuestas']} "
              f"· evaluadas {c['evaluadas']} · aceptadas {c['aceptadas']} "
              f"· caidas {c['caidas']}")
        print(f"     aceptadas por vida: {sorted(acep_por_vida)} "
              f"(mediana {st.median(acep_por_vida) if acep_por_vida else '—'})")
        if edad_primera:
            print(f"     edad de la primera aceptada: "
                  f"{sorted(edad_primera)} (mediana {st.median(edad_primera)})")
        print(f"     veredictos: {dict(vered)}")
        if motivos:
            print(f"     motivos de caida: {dict(motivos)}")
        json_out[f"formas/{b}"] = {"cuentas": dict(c),
                                   "aceptadas_por_vida": acep_por_vida,
                                   "veredictos": dict(vered),
                                   "motivos_caida": dict(motivos)}

    # ── el consejero, en F ───────────────────────────────────────────────
    print("\n== EL CONSEJERO (F) ==")
    for k in sorted(k for k in M if k[0] == "F"):
        o = M[k]
        lat = [x["ms"] for x in o["citas"] if x.get("ms")]
        callar = sum(1 for x in o["citas"]
                     if (x.get("traduccion") or {}).get("callar"))
        ok = sum(1 for x in o["citas"] if x.get("ok"))
        sp = o["spend"][-1] if o["spend"] else None
        print(f"  {k[1]}/{k[2]}: citas {len(o['citas'])} (ok {ok}, fallos "
              f"{len(o['citas']) - ok}) · saltadas {len(o['saltadas'])} · "
              f"latencia mediana {round(st.median(lat)) if lat else '—'} ms · "
              f"callar {callar}/{ok} "
              f"({callar / ok * 100:.0f}%)" if ok else "")
        if sp:
            print(f"      /spend {sp.get('spend_usd')} · cabecera "
                  f"{sp.get('cabecera_usd')} · cuadra {sp.get('cuadra')}")

    # ── [C1bis] EL PARTE, y callar frente a lo que decia el parte ────────
    print("\n== EL PARTE (comprobacion de campo, del cuerpo de la peticion) ==")
    tot = collections.Counter()
    cruce = collections.Counter()
    for k in sorted(k for k in M if k[0] == "F"):
        o = M[k]
        cu = o["cuerpos"]
        if not cu:
            continue
        # por tic, se cruza el cuerpo de la cita con lo que el consejero dijo
        porcita = {x["tick"]: x for x in cu}
        vacio = sum(1 for x in cu if not x.get("parte_encontrado")
                    or x.get("parte_bytes", 0) < 80)
        inter = sum(x.get("interrogantes", 0) for x in cu)
        tot["citas"] += len(cu)
        tot["con_parte"] += len(cu) - vacio
        tot["interrogantes"] += inter
        for x in o["citas"]:
            c = porcita.get(x.get("tick_foto"))
            if c is None:
                continue
            callo = bool((x.get("traduccion") or {}).get("callar"))
            # ¿que le decia el parte en ESA cita?
            ext = c.get("extracto_300") or ""
            if "primera forma" in ext:
                cual = "sin formas previas"
            elif "RECHAZADA" in ext:
                cual = "le rechazaron la anterior"
            elif "ACEPTADA" in ext:
                cual = "le aceptaron la anterior"
            else:
                cual = "otro"
            cruce[(cual, "calla" if callo else "habla")] += 1
        print(f"  {k[1]}/{k[2]}: citas con cuerpo {len(cu)} · con parte no "
              f"vacio {len(cu) - vacio} · interrogantes en el parte {inter}")
    if tot["citas"]:
        print(f"  --> fraccion de citas con parte NO VACIO: "
              f"{tot['con_parte']}/{tot['citas']} = "
              f"{tot['con_parte'] / tot['citas'] * 100:.1f}%")
        print(f"  --> interrogantes («el cuerpo proyecto vida ?») en total: "
              f"{tot['interrogantes']}")
    if cruce:
        print("  --> callar frente a lo que decia el parte en esa cita:")
        cuales = sorted({c for c, _ in cruce})
        for c in cuales:
            ca, ha = cruce[(c, "calla")], cruce[(c, "habla")]
            n = ca + ha
            print(f"       {c:28s}: calla {ca:3d} de {n:3d} = "
                  f"{ca / n * 100:5.1f}%" if n else "")
    json_out["parte"] = {"citas": tot["citas"], "con_parte": tot["con_parte"],
                         "interrogantes": tot["interrogantes"],
                         "cruce": {f"{a}|{b}": v for (a, b), v in cruce.items()}}

    # ── LA MEDIDA PRINCIPAL ──────────────────────────────────────────────
    print("\n== LO QUE PASO DESPUES (la medida principal) ==")
    for b in ("F", "T"):
        filas = []
        for k in sorted(k for k in M if k[0] == b):
            brazo, semilla, slot = k
            oa = M.get(("A", semilla, slot))
            for x in M[k]["confianza"]:
                if x.get("d_real") is None or x.get("d_proyectada") is None:
                    continue
                t = x["tick"]
                dA = None
                if oa:
                    vec = [v for tt, v in oa["d_por_tic"].items()
                           if abs(tt - t) <= VENT_A]
                    if vec:
                        dA = st.median(vec)
                filas.append({"semilla": semilla, "slot": slot, "tick": t,
                              "d_real": x["d_real"],
                              "d_proy": x["d_proyectada"],
                              "veredicto": x.get("veredicto"),
                              "d_A_zona": dA})
        if not filas:
            print(f"  {b}: ningun punto de control alcanzado")
            json_out[f"despues/{b}"] = []
            continue
        cumple = sum(1 for f in filas if f["d_real"] <= f["d_proy"] + 0.05)
        conA = [f for f in filas if f["d_A_zona"] is not None]
        mejor = sum(1 for f in conA if f["d_real"] < f["d_A_zona"])
        print(f"  {b}: {len(filas)} puntos de control alcanzados en "
              f"{len({(f['semilla'], f['slot']) for f in filas})} asientos")
        print(f"     la d real <= proyectada + 0,05: {cumple}/{len(filas)} = "
              f"{cumple / len(filas) * 100:.1f}%")
        if conA:
            print(f"     la d real por DEBAJO de la de A en la misma zona: "
                  f"{mejor}/{len(conA)} = {mejor / len(conA) * 100:.1f}%")
            dif = [round(f["d_real"] - f["d_A_zona"], 5) for f in conA]
            print(f"     diferencia (real - A): mediana {st.median(dif):+.5f} "
                  f"· min {min(dif):+.5f} · max {max(dif):+.5f}")
        json_out[f"despues/{b}"] = filas

    # ── [t4] (a) EMPAREJADA y (b) MAGNITUD ───────────────────────────────
    print("\n== (a) LA MEDIDA PRINCIPAL, EMPAREJADA ==")
    print("   Solo se comparan formas con el MISMO numero de tramos y la misma")
    print("   banda de distancia al primer punto de control (0=quedarse, 1, 2-3, 4+).")

    def banda(dist):
        if dist == 0:
            return "0 (quedarse)"
        if dist == 1:
            return "1"
        if dist <= 3:
            return "2-3"
        return "4+"

    def cheb2(a, b):
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    aceptadas = {"F": [], "T": []}
    for b in ("F", "T"):
        for k in sorted(k for k in M if k[0] == b):
            o = M[k]
            pos_t = o.get("pos_por_tic") or {}
            for ac in o["aceptadas"]:
                trs = ac.get("tramos") or []
                if not trs:
                    continue
                p0 = pos_t.get(ac["tick"])
                d0 = trs[0].get("destino")
                dist = (cheb2(tuple(p0), tuple(d0)) if (p0 and d0) else 0)
                # los puntos de control de ESA forma
                pts = [x for x in o["confianza"]
                       if x.get("id") == ac.get("id")
                       and x.get("d_real") is not None]
                cum = sum(1 for x in pts
                          if x["d_real"] <= x["d_proyectada"] + 0.05)
                aceptadas[b].append({
                    "semilla": k[1], "slot": k[2], "id": ac.get("id"),
                    "tramos": len(trs), "dist": dist, "banda": banda(dist),
                    "puntos": len(pts), "cumplen": cum,
                    "tick": ac["tick"],
                    "ultimo_punto": (max(x["tick"] for x in pts) if pts else None)})
    celdas = collections.defaultdict(lambda: {"F": [0, 0], "T": [0, 0]})
    for b in ("F", "T"):
        for a in aceptadas[b]:
            c = celdas[(a["tramos"], a["banda"])][b]
            c[0] += a["cumplen"]; c[1] += a["puntos"]
    hay = [(k, v) for k, v in sorted(celdas.items())
           if v["F"][1] and v["T"][1]]
    print(f"   celdas con datos en los DOS brazos: {len(hay)} de {len(celdas)}")
    tF = [0, 0]; tT = [0, 0]
    for (ntr, bd), v in hay:
        dF = v["F"][0] / v["F"][1] * 100
        dT = v["T"][0] / v["T"][1] * 100
        tF[0] += v["F"][0]; tF[1] += v["F"][1]
        tT[0] += v["T"][0]; tT[1] += v["T"][1]
        print(f"     {ntr} tramos · banda {bd:12s}: F {v['F'][0]}/{v['F'][1]} "
              f"= {dF:5.1f} %  ·  T {v['T'][0]}/{v['T'][1]} = {dT:5.1f} %  "
              f"· dif {dF - dT:+6.1f}")
    if tF[1] and tT[1]:
        d, lo, hi = newcombe(tF[0], tF[1], tT[0], tT[1])
        print(f"   EMPAREJADA (solo celdas comparables): F {tF[0]}/{tF[1]} · "
              f"T {tT[0]}/{tT[1]} · diferencia {d:+.2f} [{lo:+.2f}, {hi:+.2f}]")
    else:
        print("   EMPAREJADA: sin celdas comparables")
    for k, v in sorted(celdas.items()):
        if not (v["F"][1] and v["T"][1]):
            print(f"     (sin pareja) {k[0]} tramos · banda {k[1]:12s}: "
                  f"F {v['F'][1]} puntos · T {v['T'][1]} puntos")
    json_out["emparejada"] = {f"{k[0]}|{k[1]}": v for k, v in celdas.items()}

    print("\n== (b) LA MAGNITUD: cuanto BAJO la d de verdad ==")
    print("   Desde el tic de aceptacion hasta el ultimo punto de control")
    print("   alcanzado, contra la bajada del brazo A en la MISMA ventana.")
    mag = {"F": [], "T": []}
    for b in ("F", "T"):
        for a in aceptadas[b]:
            if a["ultimo_punto"] is None:
                continue
            o = M[(b, a["semilla"], a["slot"])]
            oa = M.get(("A", a["semilla"], a["slot"]))
            d0 = o["d_por_tic"].get(a["tick"])
            d1 = o["d_por_tic"].get(a["ultimo_punto"])
            if d0 is None or d1 is None:
                continue
            fila = {"semilla": a["semilla"], "slot": a["slot"],
                    "t0": a["tick"], "t1": a["ultimo_punto"],
                    "baja": round(d0 - d1, 5), "baja_A": None}
            if oa:
                a0 = oa["d_por_tic"].get(a["tick"])
                a1 = oa["d_por_tic"].get(a["ultimo_punto"])
                if a0 is not None and a1 is not None:
                    fila["baja_A"] = round(a0 - a1, 5)
            mag[b].append(fila)
    for b in ("F", "T"):
        v = mag[b]
        if not v:
            print(f"   {b}: sin formas con punto alcanzado")
            continue
        baj = [x["baja"] for x in v]
        conA = [x for x in v if x["baja_A"] is not None]
        print(f"   {b}: {len(v)} formas · bajada mediana {st.median(baj):+.5f} "
              f"· bajan de verdad {sum(1 for x in baj if x > 0)}/{len(baj)}")
        if conA:
            dif = [round(x["baja"] - x["baja_A"], 5) for x in conA]
            print(f"      contra A en la misma ventana ({len(conA)} formas): "
                  f"A baja {st.median([x['baja_A'] for x in conA]):+.5f} de "
                  f"mediana · diferencia mediana {st.median(dif):+.5f} · "
                  f"la forma baja MAS que A en "
                  f"{sum(1 for d in dif if d > 0)}/{len(dif)}")
    json_out["magnitud"] = mag

    # ── [t5] (c) LA MAGNITUD EN LAS FORMAS RECHAZADAS POR AREA ───────────
    # Una forma rechazada nunca vivio, asi que no tiene puntos de control ni
    # horizonte propio en el diario: `forma_evaluada` guarda el veredicto y el
    # numero de tramos, no los tics. La ventana se DECLARA: el tramo mediano
    # que duraron las formas ACEPTADAS (tic de aceptacion -> ultimo punto
    # alcanzado), medido sobre los dos brazos juntos para que no dependa del
    # brazo. Con esa misma ventana fija se recalculan tambien las aceptadas,
    # para que las dos columnas sean comparables entre si.
    print("\n== (c) LA MAGNITUD EN LAS FORMAS RECHAZADAS POR AREA ==")
    spans = [a["ultimo_punto"] - a["tick"] for b in ("F", "T")
             for a in aceptadas[b] if a["ultimo_punto"] is not None]
    L = int(st.median(spans)) if spans else 0
    print(f"   ventana fija declarada L = {L} tics (mediana del tramo que "
          f"duraron las {len(spans)} formas aceptadas de los dos brazos)")

    def _baja(o, t0, t1):
        """Bajada de d entre dos tics, con el registro mas cercano dentro de 5."""
        d = o.get("d_por_tic") or {}

        def _cerca(t):
            if t in d:
                return d[t]
            cand = [tt for tt in d if abs(tt - t) <= 5]
            return d[min(cand, key=lambda tt: abs(tt - t))] if cand else None
        a, z = _cerca(t0), _cerca(t1)
        return None if (a is None or z is None) else round(a - z, 5)

    recha = {"F": [], "T": []}
    for b in ("F", "T"):
        for k in sorted(k for k in M if k[0] == b):
            o = M[k]
            oa = M.get(("A", k[1], k[2]))
            for x in o["evaluadas"]:
                if x.get("veredicto") != "area":
                    continue
                t0, t1 = x["tick"], x["tick"] + L
                recha[b].append({
                    "semilla": k[1], "slot": k[2], "tick": t0,
                    "ventaja": x.get("ventaja"),
                    "propia": _baja(o, t0, t1),
                    "baja_A": _baja(oa, t0, t1) if oa else None})
    acep_fija = {"F": [], "T": []}
    for b in ("F", "T"):
        for a in aceptadas[b]:
            o = M[(b, a["semilla"], a["slot"])]
            oa = M.get(("A", a["semilla"], a["slot"]))
            acep_fija[b].append({
                "semilla": a["semilla"], "slot": a["slot"], "tick": a["tick"],
                "propia": _baja(o, a["tick"], a["tick"] + L),
                "baja_A": _baja(oa, a["tick"], a["tick"] + L) if oa else None})

    def _res(v, campo):
        w = [x[campo] for x in v if x[campo] is not None]
        if not w:
            return None
        return (len(w), st.median(w), sum(1 for z in w if z > 0))

    for b in ("F", "T"):
        print(f"   {b}:")
        for etq, v in (("rechazadas por area", recha[b]),
                       ("aceptadas (misma L)", acep_fija[b])):
            rp, ra = _res(v, "propia"), _res(v, "baja_A")
            if rp:
                print(f"      {etq:22s} n={rp[0]:4d} · el propio brazo baja "
                      f"{rp[1]:+.5f} de mediana · baja de verdad "
                      f"{rp[2]}/{rp[0]} = {rp[2] / rp[0] * 100:.1f} %")
            if ra:
                print(f"      {'':22s}          · A en la MISMA ventana baja "
                      f"{ra[1]:+.5f} de mediana · baja de verdad "
                      f"{ra[2]}/{ra[0]} = {ra[2] / ra[0] * 100:.1f} %")
    json_out["rechazadas"] = {"L": L, "recha": recha, "acep_fija": acep_fija}

    # ── [t5] (d) LAS FORMAS DE F SEGUN HUBIERA FORMA DEL HERMANO ─────────
    # «Forma contada del hermano en la ventana» = un `hilo_forma` oido con
    # `tramos > 0` en los HERMANO_VIEJO=150 tics anteriores al tic de la
    # evaluacion, que es exactamente el plazo con el que la politica la da por
    # fresca (`policy_forma.py:82,532`).
    HERM_VIEJO = 150
    print("\n== (d) LAS FORMAS DE F SEGUN HUBIERA FORMA CONTADA DEL HERMANO ==")
    print(f"   fresca = oida con tramos>0 en los {HERM_VIEJO} tics anteriores")
    part = {True: collections.Counter(), False: collections.Counter()}
    pts_h = {True: [0, 0], False: [0, 0]}
    oidas_tot = 0
    for k in sorted(k for k in M if k[0] == "F"):
        o = M[k]
        con = sorted(x["tick"] for x in o["hilo"]
                     if x.get("estado") == "oido" and (x.get("tramos") or 0) > 0)
        oidas_tot += len(con)
        ids_h = {}
        for x in o["evaluadas"]:
            t = x["tick"]
            h = any(0 <= t - u <= HERM_VIEJO for u in con)
            part[h]["evaluadas"] += 1
            part[h][x.get("veredicto") or "?"] += 1
            if x.get("id") is not None:
                ids_h[x["id"]] = h
        for ac in o["aceptadas"]:
            part[ids_h.get(ac.get("id"), False)]["aceptadas"] += 1
        for x in o["confianza"]:
            if x.get("d_real") is None or x.get("d_proyectada") is None:
                continue
            h = ids_h.get(x.get("id"), False)
            pts_h[h][1] += 1
            if x["d_real"] <= x["d_proyectada"] + 0.05:
                pts_h[h][0] += 1
    print(f"   formas oidas del hermano con tramos>0 en toda F: {oidas_tot}")
    for h in (True, False):
        c = part[h]
        n = c["evaluadas"]
        if not n:
            print(f"   {'CON' if h else 'SIN'} forma del hermano: 0 evaluadas")
            continue
        print(f"   {'CON' if h else 'SIN'} forma del hermano: {n} evaluadas · "
              f"aceptadas {c['aceptadas']} = {c['aceptadas'] / n * 100:.1f} % · "
              f"area {c['area']} · callo {c['el consejero callo']} "
              f"· puntos de control {pts_h[h][0]}/{pts_h[h][1]}")
    if part[True]["evaluadas"] and part[False]["evaluadas"]:
        d, lo, hi = newcombe(part[True]["aceptadas"], part[True]["evaluadas"],
                             part[False]["aceptadas"], part[False]["evaluadas"])
        print(f"   diferencia en tasa de aceptacion (con - sin): {d:+.2f} "
              f"puntos [{lo:+.2f}, {hi:+.2f}]")
    json_out["hermano"] = {"oidas_con_forma": oidas_tot,
                           "con": dict(part[True]), "sin": dict(part[False]),
                           "puntos_con": pts_h[True], "puntos_sin": pts_h[False]}

    # ── [t3] LA REGLA DE CONTINUACION, sellada el 21-sep ─────────────────
    print("\n== REGLA DE CONTINUACION (sellada antes de la tanda 3) ==")
    cn = {}
    for b in ("F", "T"):
        fs = json_out.get(f"despues/{b}") or []
        cum = sum(1 for f in fs if f["d_real"] <= f["d_proy"] + 0.05)
        cn[b] = (cum, len(fs))
        lo, hi = wilson(cum, len(fs))
        print(f"  {b}: {len(fs)} puntos de control · cumplen "
              f"{cum}/{len(fs)} = "
              f"{cum / len(fs) * 100 if fs else 0:.1f} % "
              f"[{lo:.1f}-{hi:.1f}]")
    if cn["F"][1] and cn["T"][1]:
        d, lo, hi = newcombe(cn["F"][0], cn["F"][1], cn["T"][0], cn["T"][1])
        cero_dentro = lo <= 0 <= hi
        print(f"  diferencia F - T: {d:+.2f} puntos "
              f"[{lo:+.2f}, {hi:+.2f}] · el cero {'DENTRO' if cero_dentro else 'fuera'}")
    else:
        cero_dentro = True
        print("  diferencia F - T: sin datos suficientes")
    pocos = [b for b in ("F", "T") if cn[b][1] < 40]
    print(f"  puntos < 40 en: {pocos if pocos else 'ninguno'}")
    disp = bool(pocos) or (cero_dentro and min(cn['F'][1], cn['T'][1]) < 40)
    print(f"  --> con estos datos, la regla {'DISPARARIA' if disp else 'NO dispararia'} "
          f"la ampliacion a las semillas 21-40 (solo F y T)")
    json_out["regla"] = {"F": cn["F"], "T": cn["T"],
                         "cero_dentro": cero_dentro, "pocos": pocos,
                         "dispararia": disp}

    # ── confianza, hilo, vida ────────────────────────────────────────────
    print("\n== CONFIANZA, HILO, VIDA ==")
    for b in ("F", "T"):
        for k in sorted(k for k in M if k[0] == b):
            o = M[k]
            cs = [x.get("C") for x in o["confianza"] if x.get("C") is not None]
            hi = o["hilo"]
            print(f"  {b}/{k[1]}/{k[2]}: C {cs if cs else '—'} · "
                  f"callo al consejero "
                  f"{sum(1 for x in o['confianza'] if x.get('suceso'))} · "
                  f"hilo dichos "
                  f"{sum(1 for x in hi if x.get('estado') == 'dicho')} oidos "
                  f"{sum(1 for x in hi if x.get('estado') == 'oido')} "
                  f"con forma "
                  f"{sum(1 for x in hi if x.get('estado') == 'dicho' and x.get('con_forma'))}"
                  f" · tiempo {o.get('tiempo', {}).get('mediana')}/"
                  f"{o.get('tiempo', {}).get('max')} ms")
    # ── [t2] duracion de la decision y tics perdidos ─────────────────────
    print("\n== DURACION DE LA DECISION Y TICS PERDIDOS ==")
    for b in ("A", "F", "T"):
        ks = [k for k in sorted(M) if k[0] == b]
        if not ks:
            continue
        tot = collections.Counter()
        por_partida = []
        for k in ks:
            o = M[k]
            md = o.get("ms_decision") or {}
            pe = o.get("perdidos") or {}
            tot["tics"] += md.get("n", 0)
            tot["lentos"] += md.get("mayores_40_5", 0)
            tot["faltan"] += pe.get("faltan", 0)
            tot["de"] += pe.get("de", 0)
            tot["vigia"] += pe.get("vigia", 0)
            por_partida.append(
                (f"{k[1]}/{k[2]}", md.get("n", 0), md.get("mayores_40_5", 0),
                 md.get("mediana"), md.get("max"), pe.get("faltan", 0),
                 pe.get("de", 0), pe.get("vigia", 0)))
        print(f"  {b}:")
        for n_, tics, lentos, med, mx, fal, de, vig in por_partida:
            print(f"     {n_:>12s}: tics {tics:6,} · >40,5 ms {lentos:4d} "
                  f"({lentos / tics * 100 if tics else 0:5.2f} %) · mediana "
                  f"{med} · max {mx} · perdidos {fal}/{de} "
                  f"({fal / de * 100 if de else 0:.2f} %) · vigia {vig}")
        print(f"     TOTAL {b}: >40,5 ms {tot['lentos']}/{tot['tics']} = "
              f"{tot['lentos'] / tot['tics'] * 100 if tot['tics'] else 0:.3f} % "
              f"· perdidos {tot['faltan']}/{tot['de']} = "
              f"{tot['faltan'] / tot['de'] * 100 if tot['de'] else 0:.3f} % "
              f"· vigia {tot['vigia']}")
        json_out[f"tiempos/{b}"] = dict(tot)

    print("\n== VIDA ==")
    for b in ("A", "F", "T"):
        vs = [M[k]["tics_vivos"] for k in sorted(M) if k[0] == b]
        ps = [(M[k]["final"] or {}).get("placement") for k in sorted(M)
              if k[0] == b and M[k]["final"]]
        cal = [M[k]["calma_literal"] for k in sorted(M) if k[0] == b]
        if not vs:          # la ampliacion no lleva A: el brazo puede no estar
            print(f"  {b}: sin asientos en esta(s) tanda(s)")
            continue
        print(f"  {b}: vida {sorted(vs)} (mediana {st.median(vs)}) · "
              f"puestos {sorted(p for p in ps if p is not None)} · "
              f"calma literal total {sum(cal)}")
    json.dump(json_out, open(os.path.join(AQUI, f"P56C_t{tanda}_medidas.json"),
                             "w"), ensure_ascii=False, indent=1)
    print(f"\nguardado en P56C_t{tanda}_medidas.json")


if __name__ == "__main__":
    main()

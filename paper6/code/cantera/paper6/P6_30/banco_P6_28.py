# [P6-30] [P6-30] COPIA de cantera/paper6/banco_P6_28.py con tres cambios declarados: RAIZ un nivel mas arriba (la copia vive en paper6/P6_30), cantera/paper6 en sys.path, y un proceso por vida (maxtasksperchild=1) en el pool que replica el cuerpo. Nada mas cambia.
"""[P6-28 · 1] EL BANCO DEL ADELANTO (dolares de la consola de Anthropic, tope 3). Las consultas reales de A8 en la
serie de P6-27 (los diarios `P627_t1_A8_*`, `P627_t2_A8_*`; cada `razonador26` con respuesta). Para cada una:
  (a) `--instantaneas`: se reconstruye con la replica en seco (molde de `escenas_P6_25.vida`: el alma espejo de A7h
      recibiendo el diario por el cable falso) la instantanea del tic de consulta (con lo que el razonador leia: candidatos
      del tic anterior, parte del hermano, su ultimo mensaje, su plan, el historial) y la del tic REAL en que llego la
      respuesta, y se anota la casilla real a la llegada;
  (b) `--adelanto`: se construye la escena prevista a t+DELTA (`prevision_P6_28`) desde la instantanea de consulta y se
      pide a Haiku un plan (clave de cantera/paper5/.env, nunca impresa; gasto por `usage`, tope 3 USD, parada 2,8);
  (c) `--juzga`: se juzgan con la puerta6 real (proceso aparte, `juez_P6_25.juzga_lote`) sobre la instantanea de LLEGADA:
      el plan con adelanto y el plan original de A8 (la respuesta grabada, traducida como en el campo, sin adelanto).
Informa: fraccion que pasa a la llegada con y sin adelanto (misma consulta, misma instantanea), error de la prevision
(casillas entre la casilla prevista y la real a la llegada: mediana y p90), intraducibles, gasto.
Las instantaneas van al borrador de la sesion (fuera de git).
    python3 banco_P6_28.py --instantaneas [--hilos 4] · --adelanto · --juzga [--hilos 4] · --mide
"""
from __future__ import annotations
import collections, glob, gzip, hashlib, json, math, os, pickle, re, sys, threading, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))  # [P6-30] copia en paper6/P6_30: un nivel mas
SNAPS = os.environ.get("P628_SNAPS", os.path.join(AQUI, "_P6_28_snaps"))
for _p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
TOPE_USD = 3.0; TOPE_PARADA = 2.8; HILOS_API = 3
VERSION = "banco_P6_28 (P6-28): consultas reales de A8 (P6-27) reconstruidas; escena prevista a t+DELTA -> Haiku; juicio puerta6 a la llegada, con y sin adelanto"


def consultas():
    """Las consultas reales de A8 con respuesta, por diario."""
    import serie_util as U
    out = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P627_t[12]_A8_*", "*policy_agent_1*.art.log"))):
        carp = os.path.basename(os.path.dirname(f)); slot = int(re.search(r"policy_agent_(\d+)", f).group(1))
        pos = {}; rz = []; ev = []
        for r in U.lee(f):
            k = r.get("k")
            if k == "tick" and r.get("phase") == "live":
                pos[r["tick"]] = (int(r["pos"][0]), int(r["pos"][1]), r.get("hp"))
            elif k == "razonador26" and r.get("estado") in ("propone", "intraducible", "calla", "error"):
                rz.append(r)
            elif k == "forma_evaluada" and r.get("origen") == "consejero":
                ev.append(r)
        for r in rz:
            tl = r["tick"]; pr = pos.get(tl) or pos.get(max((t for t in pos if t <= tl), default=tl))
            e = next((x for x in ev if x.get("tick", -1) >= tl), None)
            out.append({"id": f"{carp}_{slot}_{r['tick_pregunta']}", "carp": carp, "slot": slot, "t_pregunta": r["tick_pregunta"], "t_llegada": tl, "retraso": r.get("tics_de_vuelta"), "estado_campo": r["estado"],
                        "texto_campo": r.get("texto"), "destino_campo": r.get("destino"), "veredicto_campo_llegada": (e.get("veredicto") if e else None), "pos_real_llegada": (list(pr[:2]) if pr else None), "hp_real_llegada": (pr[2] if pr else None)})
    return out


# ── (a) las instantaneas, con la replica en seco ──────────────────────────────────────────────
def _vida_mp(args):
    carp, slot, pedidos = args
    try:
        import escenas_P6_25 as ES
        from alma import policy_cortex as PC
        from alma import policy_forma as PF
        import policy_pareja as PP, policy_pareja16 as P16, policy_pareja23 as P23, puerta_proceso_P6_23 as PX, texto_escena_P6_26 as TX
        import asyncio
        fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, "*policy_agent_1*.art.log"))}
        pc, sm, cat, tics, sp, it, fin, props = ES.carga(fs[slot]); cfg = ES.config_de(pc, sm, cat)
        herm = pc.get("teammate_slot"); quiero = {}
        for c in pedidos:
            quiero.setdefault(c["t_pregunta"], []).append(("pregunta", c["id"])); quiero.setdefault(c["t_llegada"], []).append(("llegada", c["id"]))
        alma = P23.AlmaPareja23(con_proceso=False); alma.artefacto_subido = True; alma.hilo = None; alma.evalua_en_hilo = False
        PP._envuelve(alma)
        hist = collections.deque(maxlen=TX.VENTANA_RECIENTE + 2); ult_e2 = [None]; plan_h = [None]; ult_pos = [None]; ult_cands = [{}]; hecho = {}; repro = collections.Counter()
        _d0 = alma.decidir
        def decidir(obs, _d=_d0):
            t = obs.get("tick", alma.tick)
            cands_prev = dict(ult_cands[0])
            accion, radio = _d(obs)
            if radio is None or alma.phase != "live":
                return accion, radio
            o2 = alma.ultima_obs or obs; you = o2.get("you") or {}; pos = tuple(int(x) for x in you.get("pos"))
            el = str(radio.get("elegido") or ""); rec_d = str(((tics[0] if False else {}) or {}).get("x", ""))
            for m in (obs.get("chat") or []):
                if m.get("channel") == "team" and m.get("from") == herm:
                    tx = str(m.get("text") or "")
                    if tx.startswith("E2 "): ult_e2[0] = tx
                    elif tx.startswith("P6 "):
                        p = TX.parsea_plan(tx)
                        if p: plan_h[0] = p
            if t in quiero:
                for tipo, cid in quiero[t]:
                    job = PX.instantanea(ES.trabajo(alma, o2, t))
                    if tipo == "pregunta":
                        job["extra"] = {"cands": cands_prev, "parte_herm": getattr(alma, "parte_herm", None), "ult_e2": ult_e2[0], "plan_hermano": plan_h[0], "hist": [x for x in hist if x["t"] < t], "ultimo_rec": getattr(alma, "ultimo_rec", None)}
                    os.makedirs(SNAPS, exist_ok=True); p = os.path.join(SNAPS, f"{cid}_{tipo}.pkl.gz")
                    with gzip.open(p, "wb", compresslevel=3) as fh:
                        fh.write(pickle.dumps(job, protocol=pickle.HIGHEST_PROTOCOL))
                    hecho[(cid, tipo)] = p
            r_now = float((o2.get("zone") or {}).get("radius") or 48); dps = (o2.get("zone") or {}).get("damage_per_s") or 0; dt = you.get("damage_taken") or []
            hist.append({"t": t, "hp": you.get("hp"), "zone_hit": any(isinstance(g, dict) and g.get("source") == "zone" for g in dt), "riv_hit": any(isinstance(g, dict) and str(g.get("source", "")).startswith("P") for g in dt),
                         "arde": bool(dps) and math.dist(pos, (24, 24)) > r_now, "movio": ult_pos[0] is not None and pos != ult_pos[0]})
            ult_pos[0] = pos
            ult_cands[0] = {k: (float(v["d"]) if isinstance(v, dict) and v.get("d") is not None else (float(v) if isinstance(v, (int, float)) else 0.0)) for k, v in (radio.get("candidatos") or {}).items()}
            return accion, radio
        alma.decidir = decidir
        mudo = lambda rec: None; _logs = (PC.log, PF.log, PP.log, P16.log, P23.log)
        PC.log = mudo; PF.log = mudo; PP.log = mudo; P16.log = mudo; P23.log = mudo
        msgs = [json.dumps(cfg)] + [json.dumps(ES.obs_de(r, sp, it)) for r in tics] + [json.dumps({"type": "final", "placement": (fin or {}).get("placement"), "kills": 0, "score": 0.0, "reason": (fin or {}).get("reason"), "match_ticks": (fin or {}).get("match_ticks")})]
        ws = ES.WS(msgs); out_real = sys.stdout
        try:
            sys.stdout = open(os.devnull, "w"); asyncio.run(PC.decisor(ws, alma))
        finally:
            sys.stdout = out_real; PC.log, PF.log, PP.log, P16.log, P23.log = _logs; PC._DIARIO.clear()
        print(f"  {carp} s{slot}: {len(tics)} tics · instantaneas {len(hecho)} de {2 * len(pedidos)}", flush=True)
        return {f"{k[0]}|{k[1]}": v for k, v in hecho.items()}
    except Exception as ex:
        import traceback; traceback.print_exc(); return {"error": repr(ex)[:300]}


def paso_instantaneas(hilos):
    import multiprocessing as mp
    C = consultas(); por = collections.defaultdict(list)
    for c in C:
        por[(c["carp"], c["slot"])].append(c)
    print(f"### consultas con respuesta: {len(C)} en {len(por)} vidas ({collections.Counter(c['estado_campo'] for c in C)})", flush=True)
    ctx = mp.get_context("spawn")
    with ctx.Pool(hilos, maxtasksperchild=1) as pool:  # [P6-30] un proceso por vida: sin fuga entre vidas
        res = pool.map(_vida_mp, [(k[0], k[1], v) for k, v in sorted(por.items())], chunksize=1)
    rutas = {}
    for r in res:
        rutas.update({k: v for k, v in r.items() if k != "error"})
    for c in C:
        c["snap_pregunta"] = rutas.get(f"{c['id']}|pregunta"); c["snap_llegada"] = rutas.get(f"{c['id']}|llegada")
    json.dump({"nota": "P6-28 banco · (a) las consultas reales de A8 con sus instantaneas", "version": VERSION, "consultas": C}, open(os.path.join(AQUI, "P6_28_banco_consultas.json"), "w"), ensure_ascii=False, indent=1)
    print(f"-> P6_28_banco_consultas.json · con las dos instantaneas: {sum(1 for c in C if c['snap_pregunta'] and c['snap_llegada'])} de {len(C)}")


# ── (b) el adelanto: la escena prevista y la llamada ───────────────────────────────────────────
def paso_adelanto():
    import juez_P6_25 as JZ, prevision_P6_28 as PR, puerta_proceso_P6_26 as PX26, traductor_forma as TF, consejero_forma as CF
    from alma import relator_t5 as RT
    from alma import appraisal_zs_v42_exp as V42
    import oraculo_P6_14 as O
    C = json.load(open(os.path.join(AQUI, "P6_28_banco_consultas.json")))["consultas"]
    C = [c for c in C if c.get("snap_pregunta") and c.get("snap_llegada")]
    esp = JZ.espejo(); sis = PX26.sistema26(); man = CF.manual(); cli = CF.cliente(); cont = CF.Contador(tope=TOPE_PARADA); lock = threading.Lock()
    crudas = open(os.path.join(AQUI, "P6_28_crudas_adelanto.jsonl"), "a", encoding="utf-8")
    # 1) las escenas previstas (secuencial: el espejo es uno)
    escenas = []
    for c in C:
        job = JZ.carga_snap(c["snap_pregunta"]); ex = job.get("extra") or {}
        if job.get("mundo") is not None:
            esp.mundo = job["mundo"]
        esp.tick = job["tick"]; esp.conf.C = job["C"]; esp.herm_dicho = job["herm_dicho"]; esp.herm_tick = job["herm_tick"]; esp.ultima_obs = job["ultima_obs"]; esp.parte_herm = ex.get("parte_herm"); esp.ultimo_rec = ex.get("ultimo_rec") or {}
        esp.vivas = []; esp.pendientes = {}; esp.reeval_pend = {}; esp.conf.callado_hasta = None
        if esp.orac is None or getattr(esp, "_mundo_id", None) != id(esp.mundo):
            esp.orac = O.Oraculo(esp.mundo, int(((job["obs"].get("you") or {}).get("stats") or {}).get("speed") or 5)); esp._mundo_id = id(esp.mundo)
        fases = [tuple(z) for z in (esp.mundo.zone_schedule or [])]
        try:
            o_prev, cands_prev, info = PR.prever(esp, job["obs"], job["mem"], job["blo"], job["tick"])
            texto = PR.texto28(esp, RT, V42, O, o_prev, cands_prev, job["tick"], info, fases, ex.get("hist") or [], ex.get("ult_e2"), ex.get("parte_herm"), ex.get("plan_hermano"))
            escenas.append({"c": c, "texto": texto, "info": info, "filas": esp._filas(), "escena_traductor": {"pos": list(info["pos_prevista"]), "suelo": [{"id": it.get("id"), "pos": list(it["pos"])} for it in ((o_prev.get("visible") or {}).get("items") or []) if it.get("pos")]},
                            "escena_campo": {"pos": list((job["obs"].get("you") or {}).get("pos") or ()), "suelo": [{"id": it.get("id"), "pos": list(it["pos"])} for it in ((job["obs"].get("visible") or {}).get("items") or []) if it.get("pos")]}})
        except Exception as e_:
            escenas.append({"c": c, "error": repr(e_)[:200]})
    ok = [e for e in escenas if "texto" in e]
    print(f"### escenas previstas: {len(ok)} de {len(escenas)} · ms prevision mediana {sorted(e['info']['ms_prevision'] for e in ok)[len(ok) // 2] if ok else None}", flush=True)
    # 2) las llamadas (3 hilos, como el cinco)
    def bloques(texto):
        return [{"type": "text", "text": f"{CF.CABECERA}\n\n{man}\n\n---\n\n", "cache_control": {"type": "ephemeral"}}, {"type": "text", "text": texto + "\n\n" + PX26.COLA}]
    parada = [False]
    def una(e):
        if parada[0]:
            e["error_llamada"] = "PARADA por gasto"; return
        texto_r, u, ms, err = CF.llama(cli, "haiku", sis, bloques(e["texto"]), "formas")
        with lock:
            usd = cont.suma("adelanto/haiku", "haiku", u) if u else 0.0
            crudas.write(json.dumps({"id": e["c"]["id"], "ms": ms, "usd": round(usd, 6), "usage": u, "error": err, "texto": texto_r, "escena_md5": hashlib.md5(e["texto"].encode()).hexdigest()}, ensure_ascii=False) + "\n"); crudas.flush()
            if cont.pasado():
                parada[0] = True
        e["respuesta"] = texto_r; e["ms"] = ms; e["usd"] = round(usd, 6); e["error_llamada"] = err
    sem = threading.Semaphore(HILOS_API); hs = []
    def env(e):
        with sem:
            una(e)
    for e in ok:
        h = threading.Thread(target=env, args=(e,)); h.start(); hs.append(h)
    for h in hs:
        h.join()
    crudas.close()
    # 3) traducir: el plan con adelanto (desde la casilla prevista) y el original de A8 (como en el campo)
    planes = []
    for e in escenas:
        c = e["c"]; p = {"id": c["id"], "carp": c["carp"], "slot": c["slot"], "t_pregunta": c["t_pregunta"], "t_llegada": c["t_llegada"], "retraso": c["retraso"], "snap_llegada": c["snap_llegada"], "pos_real_llegada": c["pos_real_llegada"], "hp_real_llegada": c["hp_real_llegada"],
             "veredicto_campo_llegada": c["veredicto_campo_llegada"], "estado_campo": c["estado_campo"]}
        if "texto" not in e:
            p["error"] = e.get("error"); planes.append(p); continue
        p.update({"info": e["info"], "ms": e.get("ms"), "usd": e.get("usd"), "error_llamada": e.get("error_llamada"), "escena_largo": len(e["texto"]), "escena_md5": hashlib.md5(e["texto"].encode()).hexdigest()})
        p["error_prevision"] = (max(abs(e["info"]["pos_prevista"][0] - c["pos_real_llegada"][0]), abs(e["info"]["pos_prevista"][1] - c["pos_real_llegada"][1])) if c.get("pos_real_llegada") else None)
        for etiq, texto_r, esc in (("adelanto", e.get("respuesta"), e["escena_traductor"]), ("original", c.get("texto_campo"), e["escena_campo"])):
            if not texto_r:
                p[etiq] = {"tramos": None, "motivo": "sin respuesta"}; continue
            cnt = collections.Counter()
            try:
                formas, inf = TF.traduce(texto_r, esc, e["filas"], cnt)
            except Exception as ex:
                formas, inf = [], {"fallos": [repr(ex)[:120]]}
            p[etiq] = {"tramos": (TF.solo_tramos(formas[0]) if formas else None), "parsea": bool(inf.get("parsea")), "callar": inf.get("callar"), "intraducible": (bool(inf.get("parsea")) and bool(inf.get("n_formas")) and not formas), "fallos": inf.get("fallos"),
                       "destino": (next((list(t["destino"]) for t in formas[0]["tramos"] if t.get("destino")), None) if formas else None)}
        planes.append(p)
    r = cont.resumen()
    json.dump({"nota": "P6-28 banco · (b) la escena prevista, la respuesta de Haiku y los dos planes traducidos (adelanto / original)", "version": VERSION, "gasto": r, "planes": planes}, open(os.path.join(AQUI, "P6_28_banco_planes.json"), "w"), ensure_ascii=False, indent=1)
    print(f"-> P6_28_banco_planes.json · llamadas {r['llamadas']} · gasto {r['total_usd']} USD (consola de Anthropic)")


# ── (c) el juicio a la llegada ─────────────────────────────────────────────────────────────────
def paso_juzga(hilos):
    import juez_P6_25 as JZ
    P = json.load(open(os.path.join(AQUI, "P6_28_banco_planes.json")))["planes"]
    lotes = collections.defaultdict(list)
    for p in P:
        if not p.get("snap_llegada"):
            continue
        for etiq in ("adelanto", "original"):
            tr = (p.get(etiq) or {}).get("tramos")
            lotes[p["snap_llegada"]].append({"id": p["id"], "modelo": etiq, "tramos": tr, "etiqueta": etiq})
    juicios, seg = JZ.corre(sorted(lotes.items()), hilos)
    json.dump({"nota": "P6-28 banco · (c) juicios de puerta6 sobre la instantanea REAL de llegada: adelanto y original", "segundos": seg, "juicios": juicios}, open(os.path.join(AQUI, "P6_28_banco_juicios.json"), "w"), ensure_ascii=False, indent=1)
    print(f"-> P6_28_banco_juicios.json · {seg} s · {collections.Counter((j.get('modelo'), j.get('veredicto')) for j in juicios)}")


def paso_mide():
    P = {p["id"]: p for p in json.load(open(os.path.join(AQUI, "P6_28_banco_planes.json")))["planes"]}
    J = json.load(open(os.path.join(AQUI, "P6_28_banco_juicios.json")))["juicios"]
    V = collections.defaultdict(dict)
    for j in J:
        V[j["id"]][j["modelo"]] = j
    ids = [i for i in P if i in V and "info" in P[i]]
    def tasa(etiq):
        ok = sum(1 for i in ids if V[i].get(etiq, {}).get("veredicto") == "ok"); return ok, len(ids), round(100 * ok / max(1, len(ids)), 1)
    a = tasa("adelanto"); o = tasa("original")
    # sobre las consultas que pasaban al pedir en el campo (veredicto_campo_llegada no sirve: es a la llegada); se toma el campo: pasan al pedir 109 (P6-27); aqui, por consulta, no se conoce -> se informa sobre todas
    err = sorted(P[i]["error_prevision"] for i in ids if P[i].get("error_prevision") is not None)
    intr_a = sum(1 for i in ids if (P[i].get("adelanto") or {}).get("intraducible")); calla_a = sum(1 for i in ids if (P[i].get("adelanto") or {}).get("callar")); sin_a = sum(1 for i in ids if not (P[i].get("adelanto") or {}).get("tramos"))
    camp_ok = sum(1 for i in ids if P[i].get("veredicto_campo_llegada") == "ok"); orig_ok_igual = sum(1 for i in ids if (V[i].get("original", {}).get("veredicto") == "ok") == (P[i].get("veredicto_campo_llegada") == "ok"))
    dos = sum(1 for i in ids if V[i].get("adelanto", {}).get("veredicto") == "ok" and V[i].get("original", {}).get("veredicto") == "ok"); solo_a = a[0] - dos; solo_o = o[0] - dos
    import math as _m
    n = solo_a + solo_o; k = min(solo_a, solo_o); mcn = (round(min(1.0, 2 * sum(_m.comb(n, i) for i in range(0, k + 1)) / 2 ** n), 4) if n else 1.0)
    g = json.load(open(os.path.join(AQUI, "P6_28_banco_planes.json")))["gasto"]
    OUT = {"nota": "P6-28 banco · medidas", "consultas": len(ids), "pasan_a_la_llegada": {"con_adelanto": {"k": a[0], "n": a[1], "pct": a[2]}, "sin_adelanto (plan original de A8, misma instantanea)": {"k": o[0], "n": o[1], "pct": o[2]}, "diferencia_puntos": round(a[2] - o[2], 1),
                                                                "los_dos": dos, "solo_adelanto": solo_a, "solo_original": solo_o, "mcnemar_p": mcn, "campo_original_ok_a_la_llegada": camp_ok, "original_rejuzgado_igual_que_campo": {"k": orig_ok_igual, "n": len(ids)}},
           "error_prevision_casillas": {"n": len(err), "mediana": (err[len(err) // 2] if err else None), "p90": (err[int(0.9 * len(err))] if err else None), "max": (err[-1] if err else None), "a_0": sum(1 for x in err if x == 0), "a_le_2": sum(1 for x in err if x <= 2)},
           "adelanto": {"intraducibles": intr_a, "callan": calla_a, "sin_plan": sin_a, "ms_mediana": sorted(P[i].get("ms") or 0 for i in ids)[len(ids) // 2] if ids else None, "ms_prevision_mediana": sorted(P[i]["info"]["ms_prevision"] for i in ids)[len(ids) // 2] if ids else None},
           "gasto_consola_usd": g["total_usd"], "llamadas": g["llamadas"]}
    json.dump(OUT, open(os.path.join(AQUI, "P6_28_banco.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(OUT, ensure_ascii=False))



# ── [P6-30] pasos nuevos, sin llamadas al modelo ───────────────────────────────────────────────
def paso_reenlaza():
    """[P6-30] Pone en la copia local de P6_28_banco_planes.json las instantaneas NUEVAS (P6_28_banco_consultas.json de esta carpeta), por id."""
    C = {c["id"]: c for c in json.load(open(os.path.join(AQUI, "P6_28_banco_consultas.json")))["consultas"]}
    f = os.path.join(AQUI, "P6_28_banco_planes.json"); D = json.load(open(f)); n = 0; sin = 0
    for p in D["planes"]:
        c = C.get(p["id"])
        if c and c.get("snap_llegada"):
            p["snap_llegada"] = c["snap_llegada"]; p["snap_pregunta_nueva"] = c.get("snap_pregunta"); n += 1
        else:
            p["snap_llegada"] = None; sin += 1
    D["nota_P6_30"] = "instantaneas reenlazadas a la repeticion sin fuga; respuestas del modelo: las guardadas en P6-28, sin llamar"
    json.dump(D, open(f, "w"), ensure_ascii=False, indent=1); print(f"-> reenlazados {n}, sin instantanea {sin}")


def paso_prevision():
    """[P6-30] Rehace la escena prevista desde la instantanea NUEVA de cada consulta y compara su md5 con el de la escena que se mando al modelo
    en P6-28 (escena_md5 en los planes guardados). No llama a nada. -> P6_28_prevision_P6_30.json"""
    import hashlib, juez_P6_25 as JZ, prevision_P6_28 as PR, puerta_proceso_P6_26 as PX26, oraculo_P6_14 as O
    from alma import relator_t5 as RT
    from alma import appraisal_zs_v42_exp as V42
    C = json.load(open(os.path.join(AQUI, "P6_28_banco_consultas.json")))["consultas"]; C = [c for c in C if c.get("snap_pregunta") and c.get("snap_llegada")]
    P = {p["id"]: p for p in json.load(open(os.path.join(AQUI, "P6_28_banco_planes.json")))["planes"]}
    esp = JZ.espejo(); out = []
    for c in C:
        job = JZ.carga_snap(c["snap_pregunta"]); ex = job.get("extra") or {}
        if job.get("mundo") is not None:
            esp.mundo = job["mundo"]
        esp.tick = job["tick"]; esp.conf.C = job["C"]; esp.herm_dicho = job["herm_dicho"]; esp.herm_tick = job["herm_tick"]; esp.ultima_obs = job["ultima_obs"]; esp.parte_herm = ex.get("parte_herm"); esp.ultimo_rec = ex.get("ultimo_rec")
        esp.vivas = []; esp.pendientes = {}; esp.reeval_pend = {}; esp.conf.callado_hasta = None
        if esp.orac is None or getattr(esp, "_mundo_id", None) != id(esp.mundo):
            esp.orac = O.Oraculo(esp.mundo, int(((job["obs"].get("you") or {}).get("stats") or {}).get("speed") or 5)); esp._mundo_id = id(esp.mundo)
        fases = [tuple(z) for z in (esp.mundo.zone_schedule or [])]
        try:
            o_prev, cands_prev, info = PR.prever(esp, job["obs"], job["mem"], job["blo"], job["tick"])
            texto = PR.texto28(esp, RT, V42, O, o_prev, cands_prev, job["tick"], info, fases, ex.get("hist") or [], ex.get("ult_e2"), ex.get("parte_herm"), ex.get("plan_hermano"))
            md5 = hashlib.md5(texto.encode()).hexdigest(); viejo = (P.get(c["id"]) or {}).get("escena_md5")
            out.append({"id": c["id"], "md5_nuevo": md5, "md5_guardado": viejo, "igual": (md5 == viejo), "pos_prevista": info.get("pos_prevista")})
        except Exception as e_:
            out.append({"id": c["id"], "error": repr(e_)[:200]})
    ig = sum(1 for o in out if o.get("igual")); print(f"-> escenas previstas rehechas {len(out)}: texto igual al que se mando {ig}, distinto {sum(1 for o in out if o.get('igual') is False)}, error {sum(1 for o in out if o.get('error'))}")
    json.dump({"nota": "P6-30: la escena prevista desde la instantanea sin fuga contra la que se mando al modelo en P6-28 (md5)", "consultas": out}, open(os.path.join(AQUI, "P6_28_prevision_P6_30.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4
    if "--instantaneas" in a:
        paso_instantaneas(hilos)
    elif "--adelanto" in a:
        paso_adelanto()
    elif "--reenlaza" in a:
        paso_reenlaza()
    elif "--prevision" in a:
        paso_prevision()
    elif "--juzga" in a:
        paso_juzga(hilos)
    elif "--mide" in a:
        paso_mide()
    else:
        print(__doc__)

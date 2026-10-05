"""[P6-22 · 3] EL BUCLE PRINCIPAL, TIC A TIC, CON EL MUNDO QUE NO ESPERA. Coste cero.

El bucle REAL del cliente (`policy_cortex.decisor`) con un WS falso que entrega las
observaciones grabadas de un diario a la cadencia del mundo (una cada 1/24 s, en reloj de
pared, SIN esperar al cuerpo: si el cuerpo tarda, las observaciones se acumulan como en la
red) y que anota, para cada accion emitida, en que «tic del servidor» cae (el tic de reloj en
que llega). Con la regla del juego (la primera accion de cada tic vale, las demas se
descartan), un tic del servidor con dos acciones es una accion PERDIDA. Bucle abierto: las
posiciones son las grabadas, las decisiones no cambian el flujo.

Por brazo (mismo diario, misma ventana):
  A4  = policy_pareja11 (cuerpo del seis, sin oraculo ni puerta);
  A6  = policy_pareja18 (A4 + oraculo + puerta del cinco con comparador puerta6 + compromiso6b,
        la puerta en el hilo), tal como jugo;
  A5v = policy_pareja16 con GEMV_PUERTA6=0 (la puerta del cinco con su comparador, en el hilo);
  A6p = A6 con el arreglo de P6-22 (`puerta_proceso_P6_22`), si se pide.
Lo que se mide por tic: latencia de entrega (cuanto esperaba la observacion en la cola),
`decidir` en ms, tic del servidor en que cae la accion, y si el hilo estaba ocupado. Y por
pieza: copias profundas en el hilo principal (cuantas, ms), oraculo (ms), y en el hilo: la
puerta del cinco (`F.mejor_propia_H` original), el comparador puerta6 (`rollout`), y la
evaluacion entera (`FV.evalua`).

    python3 mide_bucle_P6_22.py --brazo A4|A6|A6p [--carp P618_t1_A6_20679832 --slot 10 --desde 11400 --hasta 99999]
"""
import argparse, asyncio, collections, copy, glob, json, math, os, re, statistics as st, sys, threading, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    sys.path.insert(0, p)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--brazo", required=True); ap.add_argument("--carp", default="P618_t1_A6_20679832"); ap.add_argument("--slot", type=int, default=10)
    ap.add_argument("--desde", type=int, default=11400); ap.add_argument("--hasta", type=int, default=10 ** 9); ap.add_argument("--salida", default=None); A_ = ap.parse_args()
    SCRATCH = os.path.join(AQUI, "_P6_22_tmp"); os.makedirs(SCRATCH, exist_ok=True); os.environ["MAPA_DIR"] = SCRATCH
    BASE = {"GEMV_MIEDO": "0", "GEMV_VIDA_AJENA": "0", "GEMV_VIDA_AJENA_M": "0.25", "GEMV_MEMORIA": os.path.join(RAIZ, "paintball", "alma", "memoria_aprendida_p95.json"), "GEMV_CORTEX": "0",
            "GEMV_OJOS": "1", "GEMV_COMPANIA_TECHO": "0.32", "GEMV_HILO_FORMA": "0", "GEMV_CONSEJERO_FORMA": "0", "GEMV_CURIOSIDAD_FORMA": "0", "GEMV_CURIOSIDAD": ""}
    if A_.brazo == "A4":
        BASE.update({"GEMV_FORMA": "0"})
    elif A_.brazo == "A5v":
        BASE.update({"GEMV_FORMA": "1", "GEMV_PUERTA6": "0"})
    elif A_.brazo == "A7v":
        BASE.update({"GEMV_FORMA": "1", "GEMV_PUERTA6": "0"})
    else:
        BASE.update({"GEMV_FORMA": "1", "GEMV_PUERTA6": "1"})
    for k, v in BASE.items():
        os.environ[k] = v
    import serie_util as U
    from alma import policy_cortex as PC
    from alma import policy_forma as PF
    from alma import decisor_zs as D
    from alma import forma_viva as FV
    from alma.mundo import Mundo
    import forma as F
    import policy_pareja as PP
    import arreglos_P6_6 as R6, arreglos_P6_8b as R8, filas10_P6_10 as F10, amenaza11_P6_11 as M11
    TICK = 1.0 / 24.0

    # ── el diario: player_config y observaciones por la via real (copia de banco_P6_15.obs_de/config_de) ──
    def carga(f):
        recs = list(U.lee(f))
        pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
        ar = next((r for r in recs if r.get("k") == "arranque"), {}); con = (ar.get("constitucion") or {})
        tics = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
        del recs
        return pc, sm, cat, tics, int(con.get("speed") or 5), int(con.get("intelligence") or 5)


    def config_de(pc, sm, cat):
        cfg = U.SM.player_config(slot=pc["slot"]); cfg["items"] = list(cat["items"]); filas = list(sm["filas"])
        cfg["arena"] = {"size": 48, "static_map": filas, "legend": dict(U.LEY), "pedestals": [[x, y] for y, f in enumerate(filas) for x, ch in enumerate(f) if ch == "P"]}
        for k in ("slot", "team", "teammate_slot", "tick_rate", "max_ticks", "ignition_tick", "zone_schedule"):
            if pc.get(k) is not None:
                cfg[k] = pc[k]
        cfg["type"] = "player_config"; return cfg


    def obs_de(r, sp, it):
        you = {"pos": list(r["pos"]), "hp": (r.get("hp") if r.get("hp") is not None else 100), "pack": list(r.get("pack") or []), "hand": r.get("hand"), "body": r.get("body"), "effects": r.get("effects") or [],
               "stats": {"speed": sp, "intelligence": it}, "attack_ready_in": r.get("attack_ready_in"), "move_ready_in": r.get("move_ready_in_obs", r.get("move_ready_in")),
               "action_result": r.get("action_result_obs", r.get("action_result")), "damage_taken": (r.get("damage_taken") if isinstance(r.get("damage_taken"), list) else []),
               "damage_dealt": (r.get("damage_dealt") if isinstance(r.get("damage_dealt"), list) else []), "kills": r.get("kills")}
        return {"type": "observation", "tick": r["tick"], "phase": r.get("phase", "live"), "you": you,
                "visible": {"agents": [dict(a) for a in (r.get("ve_agentes") or []) if a.get("pos")], "items": [dict(x) for x in (r.get("ve_items") or []) if x.get("pos")], "bushes": list(r.get("ve_bushes") or []), "projectiles": list(r.get("ve_proyectiles") or [])},
                "zone": dict(r.get("zona") or {}), "events": list(r.get("eventos") or []), "chat": list(r.get("chat") or []), "social": r.get("social") or {}}


    # ── instrumentacion, desde fuera ──
    PIEZAS = collections.defaultdict(list)     # nombre -> [(ms, hilo_principal?, i_obs)]
    ESTADO = {"i": -1, "hilo_ocupado": 0, "ocupado_desde": None, "ocupado_intervalos": []}
    _MAIN = threading.main_thread()


    def _mide(nombre, fn):
        def w(*a, **k):
            t = time.perf_counter()
            try:
                return fn(*a, **k)
            finally:
                PIEZAS[nombre].append(((time.perf_counter() - t) * 1000.0, threading.current_thread() is _MAIN, ESTADO["i"]))
        w.__wrapped__ = fn; return w


    copy.deepcopy = _mide("copia profunda", copy.deepcopy)
    if A_.brazo != "A4":
        F.mejor_propia_H = _mide("puerta del cinco (mejor_propia_H)", F.mejor_propia_H)
        FV.evalua = _mide("evaluacion entera (FV.evalua)", FV.evalua)
        try:
            import puerta6_P6_15 as P6
            P6.rollout = _mide("comparador puerta6 (rollout)", P6.rollout)
        except Exception:
            pass
        try:
            import oraculo_P6_14 as O
            O.Oraculo.dispara = _mide("oraculo: dispara", O.Oraculo.dispara); O.Oraculo.seguras = _mide("oraculo: seguras", O.Oraculo.seguras); O.Oraculo.bfs = _mide("oraculo: bfs", O.Oraculo.bfs)
        except Exception:
            pass

    # ── el alma ──
    hecho = R6.aplica(PP.AlmaPareja, PC.log); hecho8 = R8.aplica(PC.log); hecho10 = F10.aplica(PC.log); hecho11 = M11.aplica(PC.log)
    if A_.brazo == "A4":
        alma = PP.AlmaPareja()
    else:
        import policy_pareja16 as P16
        P18 = None
        if A_.brazo in ("A6", "A6p"):
            import policy_pareja18 as P18
        if A_.brazo in ("A7v", "A7h"):
            import policy_pareja23 as P23
        if A_.brazo == "A6p":
            import puerta_proceso_P6_22 as PPX
        alma = (P16.AlmaPareja16() if A_.brazo == "A5v" else (PPX.AlmaPareja22() if A_.brazo == "A6p" else (P23.AlmaPareja23() if A_.brazo in ("A7v", "A7h") else P18.AlmaPareja18()))); alma.evalua_en_hilo = True
        alma._oraculo16 = _mide("oraculo16 (por tic)", alma._oraculo16)
    PP._envuelve(alma); alma.cf.arranca()
    if getattr(alma, "hilo", None) is not None and A_.brazo not in ("A6p", "A7v", "A7h"):
        _enc = alma.hilo.encarga
        def _encarga(ident, fn, _e=_enc):
            def fn2():
                ESTADO["hilo_ocupado"] += 1; t = time.perf_counter()
                try:
                    return fn()
                finally:
                    ESTADO["hilo_ocupado"] -= 1; ESTADO["ocupado_intervalos"].append((t, time.perf_counter()))
            return _e(ident, fn2)
        alma.hilo.encarga = _encarga
    _dec = alma.decidir
    def _decidir(o):
        t = time.perf_counter(); r = _dec(o); PIEZAS["decidir (por tic)"].append(((time.perf_counter() - t) * 1000.0, True, ESTADO["i"])); return r
    alma.decidir = _decidir

    # ── el diario y el WS con reloj ──
    carp = os.path.join(RAIZ, "paintball", "runs", A_.carp); f = glob.glob(os.path.join(carp, f"*policy_agent_{A_.slot}.art.log"))[0]
    pc, sm, cat, tics, sp, it = carga(f); cfg = config_de(pc, sm, cat)
    obs = [obs_de(r, sp, it) for r in tics if A_.desde <= r["tick"] < A_.hasta]
    msgs = [json.dumps(cfg)] + [json.dumps(o) for o in obs] + [json.dumps({"type": "final", "placement": 9, "kills": 0, "score": 0.0, "reason": "medida", "match_ticks": obs[-1]["tick"]})]
    REG = []      # por observacion: i, tick, espera_ms (cola), decidir_ms, tic_servidor de la accion, tarde (tics), perdida, hilo_ocupado
    BUCKETS = {}


    class WSReloj:
        def __init__(self):
            self.i = 0; self.t0 = None; self.actual = None
        def __aiter__(self):
            return self
        async def __anext__(self):
            if self.i >= len(msgs):
                raise StopAsyncIteration
            m = msgs[self.i]; k = self.i - 1      # k = indice de observacion (el 0 es el player_config)
            if self.i == 0:
                self.i += 1; return m
            if self.t0 is None:
                self.t0 = time.perf_counter()
            objetivo = self.t0 + k * TICK; ahora = time.perf_counter()
            if ahora < objetivo:
                await asyncio.sleep(objetivo - ahora); ahora = time.perf_counter()
            self.i += 1; ESTADO["i"] = k
            self.actual = {"i": k, "tick": (obs[k]["tick"] if k < len(obs) else None), "espera_ms": (ahora - objetivo) * 1000.0, "objetivo": objetivo, "hilo_ocupado": (ESTADO["hilo_ocupado"] > 0) or (getattr(getattr(alma, "hilo", None), "en_vuelo", 0) > 0)}
            return m
        async def send(self, s):
            d = json.loads(s)
            if d.get("type") != "action" or self.actual is None:
                return
            ahora = time.perf_counter(); b = int(math.floor((ahora - self.t0) / TICK)); a = self.actual
            perdida = b in BUCKETS; BUCKETS.setdefault(b, a["i"])
            REG.append({"i": a["i"], "tick": a["tick"], "espera_ms": round(a["espera_ms"], 2), "tic_servidor": b, "tarde": b - a["i"], "perdida": perdida, "hilo_ocupado": a["hilo_ocupado"], "accion": d.get("do"), "dir": d.get("dir")})
            self.actual = None


    t_ini = time.time()
    asyncio.run(PC.decisor(WSReloj(), alma))
    for _ in range(50):
        h = getattr(alma, "hilo", None)
        if h is None:
            break
        with h.lock:
            v = h.en_vuelo
        if v == 0:
            break
        time.sleep(0.1)
    seg = time.time() - t_ini
    # ── resumen ──
    dec = {r[2]: r[0] for r in PIEZAS["decidir (por tic)"]}
    for r in REG:
        r["decidir_ms"] = round(dec.get(r["i"], float("nan")), 2)
    mov = [r for r in REG if r["accion"] == "move"]


    def q(xs, r=2):
        v = sorted(xs)
        return {"n": len(v), "mediana": round(v[len(v) // 2], r), "p90": round(v[int(0.9 * len(v))], r), "p99": round(v[int(0.99 * len(v))], r), "max": round(v[-1], r)} if v else {"n": 0}


    if A_.brazo in ("A6p", "A7v", "A7h"):
        R_extra = {"ms_instantanea": q(alma.hilo.ms_instantanea), "errores_juez": alma.hilo.errores[:5], "diagnostico_campos (bytes, ms)": getattr(alma.hilo, "diagnostico", None), "ms_oraculo_encargo": q(getattr(alma.hilo, "ms_oraculo_encargo", []))}
        if A_.brazo in ("A7v", "A7h"):
            import policy_pareja23 as _P23
            R_extra["resumen23"] = _P23.resumen23(alma)
        alma.hilo.cierra()
    else:
        R_extra = {}

    def resumen_piezas():
        out = {}
        for k, xs in PIEZAS.items():
            m = [x[0] for x in xs if x[1]]; h = [x[0] for x in xs if not x[1]]
            out[k] = {"hilo principal": {"n": len(m), "ms_total": round(sum(m), 1), "ms_mediana": (round(st.median(m), 2) if m else None), "ms_max": (round(max(m), 1) if m else None)},
                      "otro hilo": {"n": len(h), "ms_total": round(sum(h), 1), "ms_mediana": (round(st.median(h), 2) if h else None), "ms_max": (round(max(h), 1) if h else None)}}
        return out


    ocup = sum(b - a for a, b in ESTADO["ocupado_intervalos"])
    VER = []
    for linea in PC._DIARIO:
        try:
            r = json.loads(linea)
        except Exception:
            continue
        if r.get("k") in ("forma_evaluada", "forma_reevaluada"):
            VER.append({"k": r["k"], "tick": r.get("tick"), "id": r.get("id"), "veredicto": r.get("veredicto"), "ventaja": r.get("ventaja"), "ms": r.get("ms")})
    R = {"nota": "P6-22 §3. INSTRUMENTO DE MEDIDA: bucle real con mundo que no espera. Bucle abierto sobre un diario grabado.", "brazo": A_.brazo, "diario": A_.carp, "slot": A_.slot, "tics": len(obs), "desde": obs[0]["tick"], "hasta": obs[-1]["tick"], "segundos": round(seg, 1), "tic_ms": round(TICK * 1000, 2),
         "acciones": len(REG), "perdidas (dos acciones en el mismo tic del servidor)": sum(1 for r in REG if r["perdida"]), "pct_perdidas": round(100 * sum(1 for r in REG if r["perdida"]) / max(1, len(REG)), 1),
         "pasos (move) perdidos": sum(1 for r in mov if r["perdida"]), "pct_pasos_perdidos": round(100 * sum(1 for r in mov if r["perdida"]) / max(1, len(mov)), 1),
         "tarde (tics de retraso de la accion)": dict(collections.Counter(min(r["tarde"], 20) for r in REG)), "espera_en_cola_ms": q([r["espera_ms"] for r in REG]), "decidir_ms": q([r["decidir_ms"] for r in REG if r["decidir_ms"] == r["decidir_ms"]]),
         "decidir_ms_con_hilo_ocupado": q([r["decidir_ms"] for r in REG if r["hilo_ocupado"] and r["decidir_ms"] == r["decidir_ms"]]), "decidir_ms_con_hilo_libre": q([r["decidir_ms"] for r in REG if not r["hilo_ocupado"] and r["decidir_ms"] == r["decidir_ms"]]),
         "tics_con_hilo_ocupado": sum(1 for r in REG if r["hilo_ocupado"]), "segundos_hilo_ocupado": round(ocup, 1), "veredictos": VER, "extra": R_extra, "piezas": resumen_piezas(), "registros": REG}
    sal = A_.salida or os.path.join(AQUI, f"P6_22_bucle_{A_.brazo}.json")
    json.dump(R, open(sal, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in R.items() if k not in ("registros", "piezas", "veredictos")}, ensure_ascii=False))
    for k, v in R["piezas"].items():
        print("  ", k, v)
    print("->", sal)


if __name__ == "__main__":
    main()

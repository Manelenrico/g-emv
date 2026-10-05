"""[P6-25 · 1] LAS ESCENAS: los momentos de A7h (P6-23 y P6-24) en que el oraculo propuso un plan
en las fases 5-7, contados en lenguaje llano, y las INSTANTANEAS del cuerpo en esos instantes para
que la puerta6 juzgue despues, en proceso aparte, cualquier plan (el del oraculo, el del razonador).

La vida se repite EN SECO por la via real (molde de `banco_P6_15.vida` / `banco_P6_18.vida`): el
alma espejo de A7h (`policy_pareja23.AlmaPareja23(con_proceso=False)`, la misma que usa el proceso
juez) recibe los mensajes del diario por un cable falso y decide tic a tic; en los tics de escena:

  · EL TEXTO, por la via del consejero del cinco: `alma._escena_relator` + `relator_t5.relato`
    (el relato del cuatro/cinco, byte a byte) + los seis numeros del cuerpo (P5-5B), MAS las
    palabras del seis: el calendario del anillo, el circulo de ahora y el siguiente (regla del
    juego de P6-21: arde quien esta a mas del radio del centro), su casilla y su vida, la casilla
    y la vida del hermano segun el parte E2, los rivales vistos y contados, y su estado reciente
    (ultimos 100 tics);
  · LA INSTANTANEA (`puerta_proceso_P6_23.instantanea`, pickle): lo mismo que el hilo principal
    manda al proceso juez en `encarga_juicio` (obs con ojos, memoria, bloqueos, C, parte del
    hermano, mundo), en el tic de la pregunta t y en t+D para D en RETRASOS (el retraso del
    razonador, punto 3), y en t para el hermano (punto 5).

Escenas: 200 de las 498 del censo (`P6_25_censo.json`), muestra al azar con semilla 20260928; la
pareja: 40 de las elegidas con el hermano vivo en ese tic, misma semilla. Nada se llama aqui.
SOLO LECTURA de los diarios, de uno en uno. Las funciones `carga`, `obs_de`, `config_de` y `WS`
son copia literal de `banco_P6_15.py` (que no se puede importar en el entorno de A7h).

    python3 escenas_P6_25.py [--vidas N] [--hilos 4]   -> P6_25_escenas.json, P6_25_snaps/ (scratch)
"""
from __future__ import annotations
import collections, glob, gzip, json, math, os, pickle, random, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
SNAPS = os.environ.get("P625_SNAPS", os.path.join(AQUI, "_P6_25_snaps"))
SEMILLA = 20260928; N_ESCENAS = 200; N_PAREJA = 40
RETRASOS = (48, 96, 144, 192, 240, 288, 336)          # tics: 2, 4, 6, 8, 10, 12, 14 segundos a 24 tics/s
VENTANA_RECIENTE = 100
VERSION = "escenas_P6_25 (P6-25): replica en seco del alma A7h + texto del cinco con las palabras del seis + instantaneas"


def entorno():
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path:
            sys.path.insert(0, p)
    os.makedirs(os.path.join(AQUI, "_P6_25_tmp"), exist_ok=True); os.environ["MAPA_DIR"] = os.path.join(AQUI, "_P6_25_tmp")
    for k, v in (("GEMV_MIEDO", "0"), ("GEMV_VIDA_AJENA", "0"), ("GEMV_VIDA_AJENA_M", "0.25"), ("GEMV_MEMORIA", os.path.join(RAIZ, "paintball", "alma", "memoria_aprendida_p95.json")),
                 ("GEMV_CORTEX", "0"), ("GEMV_CORTEX_CUERPO", "1"), ("GEMV_CORTEX_MANUAL", "M2"), ("GEMV_CORTEX_CADA", "50"), ("GEMV_FORMA", "1"), ("GEMV_HILO_FORMA", "0"),
                 ("GEMV_CONSEJERO_FORMA", "0"), ("GEMV_FORMAS_AZAR", "0"), ("GEMV_FORMA_CADA", "250"), ("GEMV_FORMA_SPEND_CADA", "10"), ("GEMV_CORTEX_TIMEOUT", "25"), ("GEMV_CURIOSIDAD", ""),
                 ("GEMV_CURIOSIDAD_K", "0.2"), ("GEMV_CURIOSIDAD_BALANZA", "1"), ("GEMV_CURIOSIDAD_FORMA", "0"), ("GEMV_CURIOSIDAD_CONSIGNA", "0.5"), ("GEMV_CURIOSIDAD_REFRACTARIO", "50"),
                 ("GEMV_OJOS", "1"), ("GEMV_COMPANIA_TECHO", "0.32"), ("GEMV_PUERTA6", "1"), ("GEMV_ORACULO_CADA", "25")):
        if k == "GEMV_MEMORIA" and not os.path.exists(v):
            continue                                            # en la imagen la memoria ya esta en /app/alma (ENV)
        os.environ[k] = v


entorno()
import asyncio                                                  # noqa: E402
import serie_util as U                                          # noqa: E402
from alma import policy_cortex as PC                            # noqa: E402
from alma import policy_forma as PF                             # noqa: E402
from alma import relator_t5 as RT                               # noqa: E402
from alma import appraisal_zs_v42_exp as V42                    # noqa: E402
import policy_pareja as PP                                      # noqa: E402
import arreglos_P6_6 as R6, arreglos_P6_8b as R8, filas10_P6_10 as F10, amenaza11_P6_11 as M11   # noqa: E402
import policy_pareja16 as P16                                   # noqa: E402
import policy_pareja23 as P23                                   # noqa: E402
import puerta_proceso_P6_23 as PX                               # noqa: E402
import oraculo_P6_14 as O                                       # noqa: E402
R6.aplica(PP.AlmaPareja, PC.log); R8.aplica(PC.log); F10.aplica(PC.log); M11.aplica(PC.log)
assert PF.FORMA_ON and P16.PUERTA6_ON, "el entorno de A7h: GEMV_FORMA=1 y GEMV_PUERTA6=1"


# ── copia literal de banco_P6_15.py (carga, obs_de, config_de, WS) ──────────────────────────
def carga(f):
    recs, tics, sp, it, fin, props = [], [], 5, 5, None, {}
    for r in U.lee(f):
        k = r.get("k")
        if k in ("player_config", "static_map", "catalogo"):
            recs.append(r)
        elif k == "arranque":
            s = json.dumps(r); m = re.search(r'"speed"\s*:\s*(\d+)', s); sp = int(m.group(1)) if m else 5
            m = re.search(r'"intelligence"\s*:\s*(\d+)', s); it = int(m.group(1)) if m else 5
        elif k == "tick" and r.get("phase") == "live":
            tics.append(r)
        elif k == "final":
            fin = r
        elif k == "oraculo16" and r.get("estado") == "propone":     # [P6-25] el plan del oraculo, con su texto
            props[r["tick"]] = r
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    return pc, sm, cat, tics, sp, it, fin, props


def obs_de(r, sp, it):
    you = {"pos": list(r["pos"]), "hp": (r.get("hp") if r.get("hp") is not None else 100), "pack": list(r.get("pack") or []), "hand": r.get("hand"),
           "body": r.get("body"), "effects": r.get("effects") or [], "stats": {"speed": sp, "intelligence": it},
           "attack_ready_in": r.get("attack_ready_in"), "move_ready_in": r.get("move_ready_in_obs", r.get("move_ready_in")),
           "action_result": r.get("action_result_obs", r.get("action_result")),
           "damage_taken": (r.get("damage_taken") if isinstance(r.get("damage_taken"), list) else []),
           "damage_dealt": (r.get("damage_dealt") if isinstance(r.get("damage_dealt"), list) else []), "kills": r.get("kills")}
    return {"type": "observation", "tick": r["tick"], "phase": r.get("phase", "live"), "you": you,
            "visible": {"agents": [dict(a) for a in (r.get("ve_agentes") or []) if a.get("pos")],
                        "items": [dict(x) for x in (r.get("ve_items") or []) if x.get("pos")],
                        "bushes": list(r.get("ve_bushes") or []), "projectiles": list(r.get("ve_proyectiles") or [])},
            "zone": dict(r.get("zona") or {}), "events": list(r.get("eventos") or []), "chat": list(r.get("chat") or []),
            "social": r.get("social") or {}}


def config_de(pc, sm, cat):
    cfg = U.SM.player_config(slot=pc["slot"])
    cfg["items"] = list(cat["items"])
    filas = list(sm["filas"])
    cfg["arena"] = {"size": 48, "static_map": filas, "legend": dict(U.LEY),
                    "pedestals": [[x, y] for y, f in enumerate(filas) for x, ch in enumerate(f) if ch == "P"]}
    for k in ("slot", "team", "teammate_slot", "tick_rate", "max_ticks", "ignition_tick", "zone_schedule"):
        if pc.get(k) is not None:
            cfg[k] = pc[k]
    cfg["type"] = "player_config"
    return cfg


class WS:
    def __init__(self, msgs):
        self.msgs = msgs; self.enviados = []
    def __aiter__(self):
        self._i = 0; return self
    async def __anext__(self):
        if self._i >= len(self.msgs):
            raise StopAsyncIteration
        m = self.msgs[self._i]; self._i += 1
        return m
    async def send(self, s):
        self.enviados.append(json.loads(s))
# ── fin de la copia ─────────────────────────────────────────────────────────────────────────


C = (24, 24)
ARMAS = {"sword": "espada", "spear": "lanza", "bow": "arco", "knives": "cuchillos", "blowgun": "cerbatana", "net": "red"}


def seis_numeros(o, mundo, mem, tick):
    """[copia de escenas_P55B.seis_numeros]"""
    st, _radio = V42.appraise(o, mundo, mem, tick)
    return {"necesidad_cuerpo": round(st.nF, 4), "tono_cuerpo": round(st.pF - st.nF, 4), "necesidad_recursos": round(st.nR, 4), "tono_recursos": round(st.pR - st.nR, 4),
            "necesidad_vinculo": round(st.nS, 4), "tono_vinculo": round(st.pS - st.nS, 4)}


def bloque_cuerpo(seis):
    """[copia de escenas_P55B.bloque_cuerpo]"""
    return "\n".join(["**Como esta tu cuerpo ahora, en sus seis numeros** (la necesidad va de 0 a 1: cuanto mas alta, peor; el tono es lo bueno menos lo malo):", "",
                      f"  - la vida y el peligro: necesidad {seis['necesidad_cuerpo']:.3f}, tono {seis['tono_cuerpo']:+.3f}",
                      f"  - lo que llevas en las manos: necesidad {seis['necesidad_recursos']:.3f}, tono {seis['tono_recursos']:+.3f}",
                      f"  - el vinculo con tu hermano: necesidad {seis['necesidad_vinculo']:.3f}, tono {seis['tono_vinculo']:+.3f}"])


def seg(t):
    return f"{t / 24.0:.0f} s"


def bloque_anillo(fases, t, pos, zona):
    """Las palabras del seis: el calendario del anillo, el circulo de ahora y el siguiente, y donde queda mi casilla
    con la regla del juego (P6-21: arde quien esta a MAS del radio del centro; el radio baja entero a entero)."""
    i = None
    for k, f in enumerate(fases):
        if t >= f[0]:
            i = k
    r_now = float(zona.get("radius") or 48); dps = zona.get("damage_per_s")
    d = math.dist(pos, C)
    L = ["**El anillo (la zona segura es el circulo alrededor del centro (24,24); fuera de el se arde):**", ""]
    if i is None:
        L.append("  - todavia no ha empezado a cerrarse.")
    else:
        warn, shrink, done, r0, r1, dps_f = fases[i]
        L.append(f"  - fase {i + 1} de {len(fases)}. El circulo de AHORA tiene radio {r_now:g}" + (f"; fuera de el se pierden {dps} de vida por segundo." if dps else "."))
        if t < shrink:
            L.append(f"  - el circulo empieza a encogerse en el tic {shrink} (dentro de {shrink - t} tics, {seg(shrink - t)}) y en el tic {done} habra bajado al radio {r1}.")
        elif t < done:
            L.append(f"  - el circulo se esta encogiendo: en el tic {done} (dentro de {done - t} tics, {seg(done - t)}) habra bajado al radio {r1}.")
        else:
            L.append(f"  - el circulo ya esta en el radio {r1} de esta fase.")
        if i + 1 < len(fases):
            w2, s2, d2, r02, r12, dps2 = fases[i + 1]
            L.append(f"  - el SIGUIENTE aviso llega en el tic {w2} (dentro de {w2 - t} tics, {seg(w2 - t)}); ese circulo bajara del radio {r02} al {r12} entre los tics {s2} y {d2}" + (f", y fuera se perderan {dps2} de vida por segundo." if dps2 else "."))
        else:
            L.append("  - es la ultima fase: despues de esta el circulo no baja mas.")
        dentro_ahora = d <= r_now; dentro_sig = d <= r1
        L.append(f"  - tu casilla ({pos[0]},{pos[1]}) esta a {d:.1f} del centro: {'DENTRO' if dentro_ahora else 'FUERA'} del circulo de ahora y {'dentro' if dentro_sig else 'FUERA'} del circulo al que va esta fase (radio {r1}).")
        resto = [f"radio {f[4]} desde el tic {f[2]}" for f in fases[i + 1:]]
        if resto:
            L.append("  - lo que queda del calendario: " + "; ".join(resto) + ".")
    return "\n".join(L)


def bloque_yo(o):
    you = o.get("you") or {}
    hand = (you.get("hand") or {}).get("id") if isinstance(you.get("hand"), dict) else you.get("hand"); hand = hand if hand and str(hand).lower() != "none" else None; pack = you.get("pack") or []
    return "\n".join(["**Tu, ahora:**", "",
                      f"  - casilla ({you['pos'][0]},{you['pos'][1]}), vida {you.get('hp')} de 100" + (", envenenado" if any(str(e).startswith("poison") or (isinstance(e, dict) and "poison" in str(e)) for e in (you.get("effects") or [])) else "") + ".",
                      f"  - en la mano: {ARMAS.get(hand, hand) if hand else 'nada'}; en la mochila: " + (", ".join(f"{p.get('id')} x{p.get('n')}" for p in pack if isinstance(p, dict)) if any(isinstance(p, dict) for p in pack) else "nada") + ".",
                      f"  - piernas: {'listas para dar un paso' if int(you.get('move_ready_in') or 0) == 0 else 'ocupadas ' + str(you.get('move_ready_in')) + ' tics'}."])


def bloque_hermano(alma, o, t, ult_e2):
    herm = alma.mundo.teammate_slot; muerto = bool(getattr(alma.mem, "pareja_muerta", False))
    visto = next((a for a in ((o.get("visible") or {}).get("agents") or []) if a.get("slot") == herm and a.get("pos")), None)
    p = getattr(alma, "parte_herm", None)
    L = ["**Tu hermano:**", ""]
    if muerto:
        L.append("  - esta muerto.")
    else:
        if visto:
            L.append(f"  - lo ves: casilla ({visto['pos'][0]},{visto['pos'][1]})" + (f", vida {visto.get('hp')}" if visto.get("hp") is not None else "") + ".")
        if p:
            edad = t - int(p.get("t") or t)
            L.append(f"  - su ultimo parte (hace {edad} tics, {seg(edad)}): estaba en la casilla ({p['pos'][0]},{p['pos'][1]}) con {p.get('hp'):g} de vida" + (", envenenado" if p.get("veneno") else "") + (f", lleva {p.get('botiquin')} botiquin" if p.get("botiquin") else "")
                     + (", le estaban pegando" if p.get("agresor") else "") + (f"; vio {len(p.get('rivales') or [])} rivales" if p.get("rivales") else "") + ".")
        if not visto and not p:
            L.append("  - ni lo ves ni ha mandado parte: no sabes donde esta.")
        if ult_e2:
            L.append(f"  - su ultimo mensaje por el canal de equipo, tal cual: `{ult_e2}`")
    return "\n".join(L)


def bloque_rivales(o, herm, propio):
    riv = O.Oraculo.rivales_de(o, herm, propio)
    ag = {a.get("slot"): a for a in ((o.get("visible") or {}).get("agents") or [])}
    L = ["**Los rivales:**", ""]
    if not riv:
        L.append("  - ninguno a la vista ni contado por tu hermano.")
    for s, p, contado in riv:
        a = ag.get(s) or {}; hand = (a.get("hand") or {}).get("id") if isinstance(a.get("hand"), dict) else a.get("hand")
        L.append(f"  - {'contado por tu hermano' if contado else 'visto'}: en la casilla ({p[0]},{p[1]}), a {math.dist(p, C):.1f} del centro" + (f", con {ARMAS.get(hand, hand)} en la mano" if hand and not contado else (", con las manos vacias" if (not contado and not hand) else "")) + (f", vida {a.get('hp')}" if (not contado and a.get("hp") is not None) else "") + ".")
    return "\n".join(L)


def bloque_reciente(hist, t, r_now):
    """Los ultimos VENTANA_RECIENTE tics: vida, golpes, tics ardiendo, pasos."""
    h = [x for x in hist if t - VENTANA_RECIENTE <= x["t"] <= t]
    if len(h) < 2:
        return "**Tu estado reciente:** acabas de empezar."
    hp0, hp1 = h[0]["hp"], h[-1]["hp"]
    anillo = sum(1 for x in h if x["zone_hit"]); riv = sum(1 for x in h if x["riv_hit"]); ard = sum(1 for x in h if x["arde"]); pasos = sum(1 for x in h if x["movio"])
    return "\n".join([f"**Tu estado reciente (los ultimos {t - h[0]['t']} tics, {seg(t - h[0]['t'])}):**", "",
                      f"  - vida: de {hp0:g} a {hp1:g}." + (f" Te ha quemado el anillo en {anillo} instantes." if anillo else " El anillo no te ha quemado.") + (f" Te han pegado rivales en {riv} instantes." if riv else " Ningun rival te ha pegado."),
                      f"  - has estado fuera del circulo {ard} de esos tics; has dado {pasos} pasos."])


def escena_texto(alma, o, radio, t, fases, hist, ult_e2):
    e = alma._escena_relator(o, radio)
    relato = RT.relato(e, True)
    seis = seis_numeros(o, alma.mundo, alma.mem, t)
    pos = tuple(int(x) for x in (o.get("you") or {}).get("pos"))
    bloques = [bloque_anillo(fases, t, pos, o.get("zone") or {}), bloque_yo(o), bloque_hermano(alma, o, t, ult_e2), bloque_rivales(o, alma.mundo.teammate_slot, alma.mundo.slot), bloque_reciente(hist, t, float((o.get("zone") or {}).get("radius") or 48))]
    return {"relato": relato, "seis": seis, "bloque_cuerpo": bloque_cuerpo(seis), "bloques_seis": "\n\n".join(bloques), "texto": relato + "\n\n" + bloque_cuerpo(seis) + "\n\n" + "\n\n".join(bloques)}


def trabajo(alma, o, t):
    """[copia de puerta_proceso_P6_23.HiloProceso23.encarga_juicio: lo que viaja al proceso juez, sin la forma]"""
    herm = getattr(alma.mundo, "teammate_slot", None)
    ult = {"visible": {"agents": [dict(a) for a in (((alma.ultima_obs or {}).get("visible") or {}).get("agents") or []) if a.get("slot") == herm]}}
    return {"obs": o, "mem": alma.mem, "blo": alma.bloqueos, "tick": t, "C": alma.conf.C, "herm_dicho": alma.herm_dicho, "herm_tick": alma.herm_tick, "ultima_obs": ult, "mundo": alma.mundo}


def guarda_snap(nombre, job):
    os.makedirs(SNAPS, exist_ok=True)
    p = os.path.join(SNAPS, nombre + ".pkl.gz")
    datos = pickle.dumps(job, protocol=pickle.HIGHEST_PROTOCOL)
    with gzip.open(p, "wb", compresslevel=3) as f:
        f.write(datos)
    return p, len(datos)


def vida(carp, slot, pedidos, callado=True):
    """pedidos: {tick: {"propia": bool, "pareja": bool}}. Devuelve las escenas de esta vida."""
    t_ini = time.time()
    fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, "*policy_agent_1*.art.log"))}
    pc, sm, cat, tics, sp, it, fin, props = carga(fs[slot])
    cfg = config_de(pc, sm, cat); filas = list(sm["filas"]); fases = [tuple(z) for z in (pc.get("zone_schedule") or [])]
    diario = {r["tick"]: str((r.get("RADIOGRAFIA") or {}).get("elegido") or "") for r in tics}
    # los tics de instantanea: t (pregunta) y t+D (retraso) para las escenas propias; t para las de pareja
    snap_en = collections.defaultdict(list)
    for t, q in pedidos.items():
        snap_en[t].append((t, 0))
        if q.get("propia"):
            for d in RETRASOS:
                snap_en[t + d].append((t, d))
    alma = P23.AlmaPareja23(con_proceso=False); alma.artefacto_subido = True
    alma.hilo = None; alma.evalua_en_hilo = False
    PP._envuelve(alma)
    hist = collections.deque(maxlen=VENTANA_RECIENTE + 2); ult_e2 = [None]; herm = pc.get("teammate_slot")
    escenas = {}; repro = collections.Counter(); ult_pos = [None]
    _decidir0 = alma.decidir

    def decidir(obs, _d=_decidir0):
        accion, radio = _d(obs)
        t = alma.tick
        if radio is None or alma.phase != "live":
            return accion, radio
        o2 = alma.ultima_obs or obs
        you = o2.get("you") or {}; pos = tuple(int(x) for x in you.get("pos"))
        el = str(radio.get("elegido") or "")
        if t in diario:
            repro["igual" if el == diario[t] else "difiere"] += 1
        for m in (obs.get("chat") or []):
            if m.get("channel") == "team" and m.get("from") == herm and str(m.get("text") or "").startswith("E2 "):
                ult_e2[0] = m["text"]
        r_now = float((o2.get("zone") or {}).get("radius") or 48); dps = (o2.get("zone") or {}).get("damage_per_s") or 0
        dt = you.get("damage_taken") or []
        hist.append({"t": t, "hp": you.get("hp"), "zone_hit": any(isinstance(g, dict) and g.get("source") == "zone" for g in dt), "riv_hit": any(isinstance(g, dict) and str(g.get("source", "")).startswith("P") for g in dt),
                     "arde": bool(dps) and math.dist(pos, C) > r_now, "movio": ult_pos[0] is not None and pos != ult_pos[0]})
        ult_pos[0] = pos
        if t in snap_en:
            for (t0, d) in snap_en[t]:
                job = PX.instantanea(trabajo(alma, o2, t))
                nombre = f"{carp}_{slot}_{t0}" + (f"_+{d}" if d else "")
                p, nb = guarda_snap(nombre, job)
                if d == 0:
                    q = pedidos[t0]
                    tx = escena_texto(alma, o2, radio, t, fases, list(hist), ult_e2[0])
                    pr = props.get(t) or {}
                    escenas[t0] = {"carp": carp, "slot": slot, "tick": t, "propia": bool(q.get("propia")), "pareja": bool(q.get("pareja")), "pos": list(pos), "hp": you.get("hp"), "fase": next((k + 1 for k in range(len(fases) - 1, -1, -1) if t >= fases[k][0]), None),
                                   "fin_fase": pr.get("fin_fase"), "radio_ahora": r_now, "hermano_vivo": not bool(getattr(alma.mem, "pareja_muerta", False)), "ult_e2": ult_e2[0], "elegido_real": diario.get(t), "elegido_replay": el,
                                   "oraculo": {"texto": pr.get("texto"), "destino": pr.get("destino"), "H": pr.get("H"), "llegada": pr.get("llegada"), "pasos": pr.get("pasos"), "criterios": pr.get("criterios")},
                                   "escena_traductor": {"pos": list(pos), "suelo": [{"id": x.get("id"), "pos": list(x["pos"])} for x in ((o2.get("visible") or {}).get("items") or []) if x.get("pos")]},
                                   "snap": {"0": p}, "snap_bytes": nb, "C": round(alma.conf.C, 4), "margen": round(alma.conf.margen(), 4), **tx}
                else:
                    escenas[t0]["snap"][str(d)] = p
        return accion, radio
    alma.decidir = decidir
    mudo = lambda rec: None
    _logs = (PC.log, PF.log, PP.log, P16.log, P23.log)
    PC.log = mudo; PF.log = mudo; PP.log = mudo; P16.log = mudo; P23.log = mudo
    msgs = [json.dumps(cfg)] + [json.dumps(obs_de(r, sp, it)) for r in tics] + [json.dumps({"type": "final", "placement": (fin or {}).get("placement"), "kills": 0, "score": 0.0, "reason": (fin or {}).get("reason"), "match_ticks": (fin or {}).get("match_ticks")})]
    ws = WS(msgs); out_real = sys.stdout
    try:
        sys.stdout = open(os.devnull, "w")
        asyncio.run(PC.decisor(ws, alma))
    finally:
        sys.stdout = out_real
        PC.log, PF.log, PP.log, P16.log, P23.log = _logs; PC._DIARIO.clear()
    faltan = [t for t in pedidos if t not in escenas]
    for t in escenas:      # los retrasos que caen fuera de la vida (muerta o partida acabada)
        for d in RETRASOS:
            if escenas[t]["propia"] and str(d) not in escenas[t]["snap"]:
                escenas[t]["snap"][str(d)] = None
    return {"carp": carp, "slot": slot, "tics": len(tics), "repro": dict(repro), "escenas": list(escenas.values()), "faltan": faltan, "segundos": round(time.time() - t_ini, 1), "filas": filas, "fases": fases}


def _vida_mp(args):
    carp, slot, pedidos = args
    try:
        r = vida(carp, slot, {int(k): v for k, v in pedidos.items()})
        print(f"  {carp} s{slot}: {r['tics']} tics · repro {r['repro']} · escenas {len(r['escenas'])} · faltan {r['faltan']} · {r['segundos']} s", flush=True)
        return r
    except Exception as ex:
        import traceback; traceback.print_exc()
        return {"carp": carp, "slot": slot, "error": repr(ex)[:300], "escenas": []}


def elige():
    censo = json.load(open(os.path.join(AQUI, "P6_25_censo.json")))["propuestas"]
    rnd = random.Random(SEMILLA)
    sel = rnd.sample(censo, N_ESCENAS)
    # el hermano vivo en ese tic: su diario tiene ese tic (se comprueba con el diario ligero)
    vivos = {}
    for c in sel:
        if not c.get("hermano_vivo"):
            continue
        k = (c["carp"], 21 - c["slot"])
        if k not in vivos:
            f = glob.glob(os.path.join(RAIZ, "paintball", "runs", k[0], f"*policy_agent_{k[1]}.art.log"))[0]
            vivos[k] = {r["tick"] for r in U.lee(f) if r.get("k") == "tick" and r.get("phase") == "live"}
        c["hermano_en_diario"] = c["tick"] in vivos[k]
    cand = [c for c in sel if c.get("hermano_en_diario")]
    par = rnd.sample(cand, min(N_PAREJA, len(cand)))
    ids = {(c["carp"], c["slot"], c["tick"]) for c in par}
    for c in sel:
        c["pareja"] = (c["carp"], c["slot"], c["tick"]) in ids
    return sel


if __name__ == "__main__":
    import multiprocessing as mp
    a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4; tope = int(a[a.index("--vidas") + 1]) if "--vidas" in a else None
    sel = elige()
    pedidos = collections.defaultdict(dict)
    for c in sel:
        pedidos[(c["carp"], c["slot"])][c["tick"]] = {"propia": True, "pareja": c["pareja"]}
        if c["pareja"]:
            pedidos[(c["carp"], 21 - c["slot"])].setdefault(c["tick"], {"propia": False, "pareja": True})
    tareas = sorted((carp, slot, dict(p)) for (carp, slot), p in pedidos.items())
    if tope:
        tareas = tareas[:tope]
    print(f"### P6-25 escenas: {len(sel)} escenas ({sum(1 for c in sel if c['pareja'])} de pareja) en {len(tareas)} vidas · hilos {hilos} · instantaneas en {SNAPS}", flush=True)
    ctx = mp.get_context("spawn")
    with ctx.Pool(hilos) as pool:
        res = pool.map(_vida_mp, tareas, chunksize=1)
    out = {"nota": __doc__.split("\n")[0], "version": VERSION, "semilla": SEMILLA, "retrasos": list(RETRASOS), "n_escenas": len(sel), "n_pareja": sum(1 for c in sel if c["pareja"]),
           "elegidas": [{k: c.get(k) for k in ("carp", "slot", "tick", "hermano_vivo", "hermano_en_diario", "pareja", "veredicto_campo", "ventaja_campo", "destino")} for c in sel],
           "vidas": [{k: r.get(k) for k in ("carp", "slot", "tics", "repro", "faltan", "segundos", "error")} for r in res],
           "escenas": [e for r in res for e in r.get("escenas", [])], "filas": {f"{r['carp']}": r.get("filas") for r in res if r.get("filas")}, "fases": {f"{r['carp']}": r.get("fases") for r in res if r.get("fases")}}
    json.dump(out, open(os.path.join(AQUI, "P6_25_escenas.json"), "w"), ensure_ascii=False, indent=1)
    print(f"-> P6_25_escenas.json: {len(out['escenas'])} escenas de {len(sel)} pedidas · vidas con error {sum(1 for r in res if r.get('error'))}")

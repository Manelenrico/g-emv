# [P6-30] [P6-30] COPIA de cantera/paper6/mide_P6_29.py con tres cambios declarados: RAIZ un nivel mas arriba (la copia vive en paper6/P6_30), cantera/paper6 en sys.path, y un proceso por vida (maxtasksperchild=1) en el pool que replica el cuerpo. Nada mas cambia.
"""[P6-29] CUANTO SE DEJA DOBLAR EL CUERPO: la deformacion que cuesta seguir un plan. Coste cero: solo diarios.

Diarios: A7h (P623_t2 + P624_t2, 40 semillas), A8 (P627_t1 + P627_t2, 40 semillas), A4 (P611_t1/t2 + P624_t1, 40 semillas).
DOS FUENTES, declaradas:
  (1) EL DIARIO. La radiografia de cada tic guarda la d de TODOS los candidatos del cuerpo, `elegido` (lo que se
      ejecuto: `_FM_ir_x_y` cuando compromiso6c anda el plan, `_FM_quedarse` / `_FM_retenido` cuando sujeta) y
      `elegido_cuerpo` (lo que el decisor habia elegido ANTES de que el compromiso lo cambiara: lo que habria elegido
      solo). Y `tiempo_tic.vivas`, `forma_aceptada`, `forma_caida`, `compromiso6` dan la vida de cada plan.
  (2) LA REPLICA EN SECO (molde de banco_P6_15 / escenas_P6_25): el cuerpo A4 (`policy_pareja.AlmaPareja` + los
      arreglos 6/8b/10/11, entorno de la imagen A4) recibe las observaciones del diario por un cable falso y decide tic
      a tic, sin oraculo, sin puerta y sin compromiso. Da (a) la fidelidad (su eleccion contra `elegido_cuerpo`) y
      (b) la d del paso del plan, que el decisor no calcula en el campo: en cada tic con plan vivo se vuelve a
      decidir con un candidato mas, `_FM_ir` = {tipo ir, destino del plan} (la misma receta que anda compromiso6c),
      y se lee su d junto a la de los candidatos propios en la MISMA imaginacion.
MEDIDAS (instante = tic con plan vivo y piernas listas, `move_ready_in` 0):
  1. fraccion de instantes en que lo ejecutado difiere de lo propio;
  2. deformacion por instante = d(candidato ejecutado) - d(mejor candidato propio), en la replica (d_fm o d(noop)
     contra el minimo de los propios); acumulada por plan = suma sobre sus instantes;
  3. planes soltados (reevaluacion, vida, otra caida; y muerte con plan vivo, aparte) contra cumplidos (fin de fase,
     andado): deformacion acumulada al soltar contra al cumplir (mediana, p90; solapamiento p10-p90 = umbral o no);
  4. en los cumplidos, tics ardiendo ahorrados = arde de A4 (misma semilla, mismo asiento si vive; si no, el otro)
     en la misma ventana [t_a, t_e) menos los propios, contra la deformacion acumulada (Spearman);
  5. huella: en los 200 tics tras soltar o cumplir, acuerdo entre lo elegido en el diario y lo que la replica elige
     sola, contra A4 en las mismas ventanas (misma semilla y asiento) y contra la ventana [t_a-400, t_a-200) del
     mismo brazo;
  6. oraculo (A7h) contra razonador (A8) en 1-4.
SOLO LECTURA de los diarios, de uno en uno. Ningun numero se escribe antes de calcularlo.
    python3 mide_P6_29.py [--hilos 4] [--vidas N]   -> P6_29_medidas.json, P6_29_planes.json, P6_29_vidas.json
"""
from __future__ import annotations
import collections, glob, json, math, os, re, statistics as st, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))  # [P6-30] copia en paper6/P6_30: un nivel mas
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    if p not in sys.path:
        sys.path.insert(0, p)
SCRATCH = os.environ.get("P629_SCRATCH", os.path.join(AQUI, "_P6_29_tmp")); os.makedirs(SCRATCH, exist_ok=True); os.environ["MAPA_DIR"] = SCRATCH
# el entorno de la imagen A4 (Dockerfile.pareja11), con GEMV_OJOS=1 como en el diario de A4 (banco_P6_15)
for _k, _v in (("GEMV_MIEDO", "0"), ("GEMV_VIDA_AJENA", "0"), ("GEMV_VIDA_AJENA_M", "0.25"), ("GEMV_MEMORIA", os.path.join(RAIZ, "paintball", "alma", "memoria_aprendida_p95.json")),
               ("GEMV_CORTEX", "0"), ("GEMV_CORTEX_CUERPO", "1"), ("GEMV_CORTEX_MANUAL", "M2"), ("GEMV_CORTEX_CADA", "50"), ("GEMV_FORMA", "0"), ("GEMV_HILO_FORMA", "0"), ("GEMV_CONSEJERO_FORMA", "0"),
               ("GEMV_FORMAS_AZAR", "0"), ("GEMV_FORMA_CADA", "250"), ("GEMV_FORMA_SPEND_CADA", "10"), ("GEMV_CORTEX_TIMEOUT", "25"), ("GEMV_CURIOSIDAD", ""), ("GEMV_CURIOSIDAD_K", "0.2"),
               ("GEMV_CURIOSIDAD_BALANZA", "1"), ("GEMV_CURIOSIDAD_FORMA", "0"), ("GEMV_CURIOSIDAD_CONSIGNA", "0.5"), ("GEMV_CURIOSIDAD_REFRACTARIO", "50"), ("GEMV_OJOS", "1"), ("GEMV_COMPANIA_TECHO", "0.32")):
    os.environ.setdefault(_k, _v)
import asyncio                                                  # noqa: E402
import serie_util as U                                          # noqa: E402
from alma import policy_cortex as PC                            # noqa: E402
from alma import policy_forma as PF                             # noqa: E402
from alma import decisor_zs as D                                # noqa: E402
import policy_pareja as PP                                      # noqa: E402
import arreglos_P6_6 as R6, arreglos_P6_8b as R8, filas10_P6_10 as F10, amenaza11_P6_11 as M11   # noqa: E402
R6.aplica(PP.AlmaPareja, PC.log); R8.aplica(PC.log); F10.aplica(PC.log); M11.aplica(PC.log)
VERSION = "mide_P6_29 (P6-29): diario (radiografia + vida de los planes) + replica en seco del cuerpo A4 con el candidato del plan anadido"
BRAZOS = {"A7h": ["paintball/runs/P623_t2_A7h_*", "paintball/runs/P624_t2_A7h_*"], "A8": ["paintball/runs/P627_t1_A8_*", "paintball/runs/P627_t2_A8_*"],
          "A4": ["paintball/runs/P611_t1_A4_*", "paintball/runs/P611_t2_A4_*", "paintball/runs/P624_t1_A4_*"]}
C = (24, 24); VENTANA = 200; ANTES = (400, 200)
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}


# ── copia literal de banco_P6_15.py (obs_de, config_de, WS) ─────────────────────────────────
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


# ── el gancho sobre D.decide: la eleccion propia de la replica y, con plan vivo, la d del candidato del plan ──
HOOK = {"plan": {}, "reg": {}}
_DEC0 = D.decide


def _dec29(obs, mundo, mem, tick, bloqueos=None):
    ac, ra = _DEC0(obs, mundo, mem, tick, bloqueos)
    cds = {k: (v["d"] if isinstance(v, dict) else v) for k, v in (ra.get("candidatos") or {}).items()}
    rec = {"el": ra.get("elegido"), "cds": cds}
    dest = HOOK["plan"].get(tick)
    if dest is not None:
        ced0, ua0 = dict(mem.cedidos), mem.ultimo_ataque
        c0 = D.candidatos
        vis = obs.get("visible") or {}
        cuerpos = frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos"))
        extra = ("_FM_ir", {"tipo": "ir", "destino": tuple(dest), "cuerpos": cuerpos, "recoger": mem.objetos_vistos.get(tuple(dest))})
        D.candidatos = lambda *a, **k: c0(*a, **k) + [extra]
        try:
            _ac2, ra2 = _DEC0(obs, mundo, mem, tick, bloqueos)
            v = (ra2.get("candidatos") or {}).get("_FM_ir")
            rec["d_fm"] = (v["d"] if isinstance(v, dict) else v)
            rec["fm_gana"] = (ra2.get("elegido") == "_FM_ir")
        except Exception as ex:
            rec["fm_error"] = repr(ex)[:120]
        finally:
            D.candidatos = c0; mem.cedidos, mem.ultimo_ataque = ced0, ua0
    HOOK["reg"][tick] = rec
    return ac, ra


D.decide = _dec29


def semilla_de(carp):
    return int(carp.rsplit("_", 1)[1])


def lee_diario(f):
    """El diario, compacto: por tic lo que hace falta; la vida de los planes; los sucesos del compromiso."""
    recs, tics = [], []
    T = {}; vivas = {}; ac = []; caidas = {}; cumpl = {}; c6 = collections.defaultdict(list); fin = None; sp = it = 5; pc = sm = cat = None
    for r in U.lee(f):
        k = r.get("k")
        if k == "player_config":
            pc = r
        elif k == "static_map":
            sm = r
        elif k == "catalogo":
            cat = r
        elif k == "arranque":
            s = json.dumps(r); m = re.search(r'"speed"\s*:\s*(\d+)', s); sp = int(m.group(1)) if m else 5
            m = re.search(r'"intelligence"\s*:\s*(\d+)', s); it = int(m.group(1)) if m else 5
        elif k == "tick" and r.get("phase") == "live":
            tics.append(r)
            ra = r.get("RADIOGRAFIA") or {}
            T[r["tick"]] = {"el": ra.get("elegido"), "ec": ra.get("elegido_cuerpo"), "cds": {k: (v["d"] if isinstance(v, dict) else v) for k, v in (ra.get("candidatos") or {}).items() if (v["d"] if isinstance(v, dict) else v) is not None}, "mri": int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0),
                            "pos": (int(r["pos"][0]), int(r["pos"][1])), "hp": r.get("hp"), "radio": float((r.get("zona") or {}).get("radius") or 48), "dps": (r.get("zona") or {}).get("damage_per_s") or 0,
                            "zone_hit": any(isinstance(g, dict) and g.get("source") == "zone" for g in (r.get("damage_taken") or [])),
                            "dir": ((r.get("intencion") or {}).get("dir") if (r.get("intencion") or {}).get("do") == "move" else None)}
        elif k == "tiempo_tic":
            vivas[r["tick"]] = int(r.get("vivas") or 0)
        elif k == "forma_aceptada":
            ac.append({"id": r["id"], "tick": r["tick"], "destino": ((r.get("tramos") or [{}])[0].get("destino")), "tics": r.get("tics"), "ventaja": r.get("ventaja")})
        elif k == "forma_caida":
            caidas.setdefault(r.get("id"), (r["tick"], r.get("motivo") or ""))
        elif k == "compromiso6":
            c6[r["tick"]].append(r.get("estado"))
            if r.get("estado") == "cumplida":
                cumpl.setdefault(r.get("id"), (r["tick"], r.get("por")))
        elif k == "final":
            fin = r
    return pc, sm, cat, tics, sp, it, fin, T, vivas, ac, caidas, cumpl, c6


def planes_de(T, vivas, ac, caidas, cumpl, fin, fases):
    tl = sorted(T); ult = tl[-1] if tl else 0
    muerto = bool(fin and fin.get("reason") == "eliminated")
    out = []
    for i, a in enumerate(ac):
        t_a = a["tick"]
        cand = []
        if a["id"] in caidas:
            cand.append((caidas[a["id"]][0], "caida"))
        if a["id"] in cumpl:
            cand.append((cumpl[a["id"]][0], "cumplida"))
        t_v = next((t for t in range(t_a + 1, ult + 1) if vivas.get(t, 1) == 0), None)
        if t_v is not None:
            cand.append((t_v, "vivas=0"))
        if i + 1 < len(ac):
            cand.append((ac[i + 1]["tick"], "siguiente"))
        cand.append((ult + 1, "fin de vida"))
        t_e, como = min(cand)
        if como == "caida":
            m = caidas[a["id"]][1]
            razon = "soltado: reevaluacion" if "reevaluacion" in m else ("soltado: vida" if "vida real" in m else "soltado: otra caida")
        elif como == "cumplida":
            razon = "cumplido: fin de fase" if cumpl[a["id"]][1] == "fin de fase" else "cumplido: andado"
        elif como == "vivas=0":
            razon = "cumplido: andado"
        elif como == "siguiente":
            razon = "sustituido por el siguiente"
        else:
            razon = "muerte con plan vivo" if muerto else "fin de partida con plan vivo"
        fase = next((k + 1 for k in range(len(fases) - 1, -1, -1) if t_a >= fases[k][0]), None)
        out.append({"id": a["id"], "t_a": t_a, "t_e": t_e, "como": como, "razon": razon, "destino": a["destino"], "fase": fase, "motivo": (caidas.get(a["id"]) or (None, None))[1]})
    return out


def vida(carp, slot, brazo):
    t0 = time.time()
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]
    pc, sm, cat, tics, sp, it, fin, T, vivas, ac, caidas, cumpl, c6 = lee_diario(f)
    fases = [tuple(z) for z in (pc.get("zone_schedule") or [])]
    planes = planes_de(T, vivas, ac, caidas, cumpl, fin, fases)
    # el gancho: en cada tic con plan vivo, el destino del plan (para la d del paso del plan)
    HOOK["plan"] = {}; HOOK["reg"] = {}
    for p in planes:
        if p["destino"]:
            for t in range(p["t_a"], p["t_e"]):
                HOOK["plan"][t] = tuple(p["destino"])
    # la replica en seco
    cfg = config_de(pc, sm, cat)
    alma = PP.AlmaPareja(); alma.artefacto_subido = True; PP._envuelve(alma)
    mudo = lambda rec: None
    _logs = (PC.log, PF.log, PP.log); PC.log = mudo; PF.log = mudo; PP.log = mudo
    msgs = [json.dumps(cfg)] + [json.dumps(obs_de(r, sp, it)) for r in tics] + [json.dumps({"type": "final", "placement": (fin or {}).get("placement"), "kills": 0, "score": 0.0, "reason": (fin or {}).get("reason"), "match_ticks": (fin or {}).get("match_ticks")})]
    del tics
    ws = WS(msgs); out_real = sys.stdout
    try:
        sys.stdout = open(os.devnull, "w")
        asyncio.run(PC.decisor(ws, alma))
    finally:
        sys.stdout = out_real
        PC.log, PF.log, PP.log = _logs; PC._DIARIO.clear()
    R = HOOK["reg"]
    # fidelidad: la replica contra lo propio del diario (elegido_cuerpo si lo hay; si no, elegido)
    fid = collections.Counter(); desac = []
    for t, x in T.items():
        r = R.get(t)
        if r is None:
            fid["sin replica"] += 1; continue
        propio = x["ec"] or x["el"]
        if r["el"] == propio:
            fid["igual"] += 1
        else:
            fid["difiere"] += 1; desac.append(t)
    # los instantes de cada plan
    inst = []
    for p in planes:
        p["instantes"] = 0; p["difieren"] = 0; p["obedece"] = 0; p["sujeta"] = 0; p["defo"] = 0.0; p["defo_diario"] = 0.0; p["defo_todos"] = 0.0; p["sin_d"] = 0; p["negativos"] = 0
        p["arde"] = sum(1 for t in range(p["t_a"], p["t_e"]) if t in T and T[t]["dps"] and math.dist(T[t]["pos"], C) > T[t]["radio"])
        p["zone_hits"] = sum(1 for t in range(p["t_a"], p["t_e"]) if t in T and T[t]["zone_hit"])
        p["tics_vivo"] = sum(1 for t in range(p["t_a"], p["t_e"]) if t in T)
        p["rompe"] = sum(1 for t in range(p["t_a"], p["t_e"]) for e in c6.get(t, []) if e == "rompe"); p["suspende"] = sum(1 for t in range(p["t_a"], p["t_e"]) for e in c6.get(t, []) if e == "suspende")
        for t in range(p["t_a"], p["t_e"]):
            x = T.get(t)
            if x is None:
                continue
            ejec = str(x["el"] or ""); propio = str(x["ec"] or x["el"] or ""); dif = ejec.startswith("_FM") and ejec != propio
            r = R.get(t) or {}
            d_min_r = (min(r["cds"].values()) if r.get("cds") else None)
            cds_d = x["cds"]; d_min_d = (min(cds_d.values()) if cds_d else None)
            d_ej_r = d_ej_d = None
            if dif:
                if ejec in ("_FM_quedarse", "_FM_retenido"):
                    d_ej_r = (r.get("cds") or {}).get("noop"); d_ej_d = cds_d.get("noop")
                elif ejec.startswith("_FM_ir"):
                    d_ej_r = r.get("d_fm")
                    dd = x["dir"]; d_ej_d = cds_d.get(f"paso_{dd}", cds_d.get(f"move_{dd}")) if dd else None
            delta_r = (d_ej_r - d_min_r) if (dif and d_ej_r is not None and d_min_r is not None) else (0.0 if not dif else None)
            delta_d = (d_ej_d - d_min_d) if (dif and d_ej_d is not None and d_min_d is not None) else (0.0 if not dif else None)
            listo = x["mri"] == 0
            if listo:
                p["instantes"] += 1
                if dif:
                    p["difieren"] += 1
                    p["obedece" if ejec.startswith("_FM_ir") else "sujeta"] += 1
                    if delta_r is None:
                        p["sin_d"] += 1
                    else:
                        p["defo"] += delta_r
                        if delta_r < 0:
                            p["negativos"] += 1
                    if delta_d is not None:
                        p["defo_diario"] += delta_d
                    inst.append({"carp": carp, "slot": slot, "id": p["id"], "t": t, "ejec": ejec, "propio": propio, "delta": delta_r, "delta_diario": delta_d, "d_min_replica": d_min_r, "d_min_diario": d_min_d,
                                 "replica_igual": (r.get("el") == propio), "fm_gana": r.get("fm_gana")})
            elif dif and delta_r is not None:
                p["defo_todos"] += delta_r
        p["defo_todos"] += p["defo"]
        p["defo"] = round(p["defo"], 5); p["defo_diario"] = round(p["defo_diario"], 5); p["defo_todos"] = round(p["defo_todos"], 5)
    # las ventanas de la huella: tras cada plan y antes de cada plan
    tl = sorted(T); listos = [t for t in tl if T[t]["mri"] == 0]
    arde_tics = [t for t in tl if T[t]["dps"] and math.dist(T[t]["pos"], C) > T[t]["radio"]]
    warn5 = fases[4][0] if len(fases) > 4 else None
    return {"carp": carp, "slot": slot, "brazo": brazo, "semilla": semilla_de(carp), "tics": len(T), "t_min": (tl[0] if tl else None), "t_max": (tl[-1] if tl else None), "muerto": bool(fin and fin.get("reason") == "eliminated"),
            "viva_en_warn5": (warn5 in T) if warn5 else None, "fidelidad": dict(fid), "desacuerdos": desac, "listos": listos, "arde_tics": arde_tics, "planes": planes, "instantes": inst,
            "fm_errores": sum(1 for r in R.values() if r.get("fm_error")), "fm_gana": sum(1 for r in R.values() if r.get("fm_gana")), "segundos": round(time.time() - t0, 1)}


def _vida_mp(args):
    carp, slot, brazo = args
    try:
        r = vida(carp, slot, brazo)
        print(f"  {brazo} {carp} s{slot}: {r['tics']} tics · fidelidad {r['fidelidad']} · planes {len(r['planes'])} · instantes {sum(p['instantes'] for p in r['planes'])} difieren {sum(p['difieren'] for p in r['planes'])} · {r['segundos']} s", flush=True)
        return r
    except Exception as ex:
        import traceback; traceback.print_exc()
        return {"carp": carp, "slot": slot, "brazo": brazo, "error": repr(ex)[:300], "planes": [], "instantes": []}


# ── estadistica ─────────────────────────────────────────────────────────────────────────────
def q(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p; lo = int(math.floor(k)); hi = int(math.ceil(k))
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def resumen(xs, r=4):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "media": round(st.mean(xs), r), "mediana": round(st.median(xs), r), "p10": round(q(xs, 0.1), r), "p90": round(q(xs, 0.9), r), "max": round(max(xs), r), "min": round(min(xs), r)}


def spearman(x, y):
    n = len(x)
    if n < 3:
        return None
    def rk(v):
        s = sorted(range(n), key=lambda i: v[i]); r = [0.0] * n; i = 0
        while i < n:
            j = i
            while j + 1 < n and v[s[j + 1]] == v[s[i]]:
                j += 1
            for k in range(i, j + 1):
                r[s[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rk(x), rk(y); mx, my = st.mean(rx), st.mean(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); sxx = sum((a - mx) ** 2 for a in rx); syy = sum((b - my) ** 2 for b in ry)
    return round(sxy / math.sqrt(sxx * syy), 4) if sxx > 0 and syy > 0 else None


def acuerdo_en(v, t0, t1, solo_listos=False):
    """acuerdo diario-replica en [t0, t1) de una vida: (n, iguales)."""
    if v.get("t_min") is None:
        return 0, 0
    des = set(v["desacuerdos"]); tics = (v["listos"] if solo_listos else range(max(t0, v["t_min"]), min(t1, v["t_max"] + 1)))
    ts = [t for t in tics if t0 <= t < t1] if solo_listos else list(tics)
    return len(ts), sum(1 for t in ts if t not in des)


if __name__ == "__main__":
    import multiprocessing as mp
    a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4; tope = int(a[a.index("--vidas") + 1]) if "--vidas" in a else None
    tareas = []
    for brazo, pats in BRAZOS.items():
        for pat in pats:
            for carp in sorted(glob.glob(os.path.join(RAIZ, pat))):
                for sl in (10, 11):
                    if glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log")):
                        tareas.append((os.path.basename(carp), sl, brazo))
    if tope:
        tareas = [t for b in ("A7h", "A8", "A4") for t in [x for x in tareas if x[2] == b][:tope]]
    print(f"### P6-29: {len(tareas)} vidas ({collections.Counter(t[2] for t in tareas)}) · hilos {hilos}", flush=True)
    ctx = mp.get_context("spawn")
    with ctx.Pool(hilos, maxtasksperchild=1) as pool:  # [P6-30] un proceso por vida: sin fuga entre vidas
        V = pool.map(_vida_mp, tareas, chunksize=1)
    err = [v for v in V if v.get("error")]
    V = [v for v in V if not v.get("error")]
    A4 = collections.defaultdict(dict)
    for v in V:
        if v["brazo"] == "A4":
            A4[v["semilla"]][v["slot"]] = v
    OUT = {"nota": __doc__.split("\n")[0], "version": VERSION, "vidas_con_error": [(e["carp"], e["slot"], e["error"]) for e in err], "brazos": {}}
    PLANES = []
    for brazo in ("A7h", "A8"):
        vs = [v for v in V if v["brazo"] == brazo]
        fid = collections.Counter()
        for v in vs:
            fid.update(v["fidelidad"])
        inst = [i for v in vs for i in v["instantes"]]
        planes = [dict(p, carp=v["carp"], slot=v["slot"], semilla=v["semilla"], brazo=brazo) for v in vs for p in v["planes"]]
        n_inst = sum(p["instantes"] for p in planes); n_dif = sum(p["difieren"] for p in planes)
        # 4. ahorro en los cumplidos (y en todos, declarado), emparejado con A4
        for p in planes:
            a4 = A4.get(p["semilla"], {}); ref = a4.get(p["slot"]) or a4.get(21 - p["slot"])
            p["ahorro"] = None; p["ahorro_ref"] = None
            for cand in ([a4.get(p["slot"])] if a4.get(p["slot"]) else []) + ([a4.get(21 - p["slot"])] if a4.get(21 - p["slot"]) else []):
                if cand.get("t_max") is not None and cand["t_max"] >= p["t_e"] - 1 and cand["t_min"] <= p["t_a"]:
                    ar = sum(1 for t in cand["arde_tics"] if p["t_a"] <= t < p["t_e"])
                    p["ahorro"] = ar - p["arde"]; p["ahorro_ref"] = f"A4 s{cand['slot']}"; break
        cump = [p for p in planes if p["razon"].startswith("cumplido")]; solt = [p for p in planes if p["razon"].startswith("soltado")]; muer = [p for p in planes if "plan vivo" in p["razon"]]
        por_razon = collections.Counter(p["razon"] for p in planes)
        # 5. huella
        H = {"tras": [0, 0], "tras_listos": [0, 0], "antes": [0, 0], "A4_tras": [0, 0], "A4_tras_listos": [0, 0], "A4_antes": [0, 0], "ventanas": 0, "ventanas_con_A4": 0}
        for v in vs:
            for p in v["planes"]:
                if p["t_e"] > v["t_max"]:
                    continue
                H["ventanas"] += 1
                for k, (t0, t1) in (("tras", (p["t_e"], p["t_e"] + VENTANA)), ("antes", (p["t_a"] - ANTES[0], p["t_a"] - ANTES[1]))):
                    n, ig = acuerdo_en(v, t0, t1); H[k][0] += n; H[k][1] += ig
                n, ig = acuerdo_en(v, p["t_e"], p["t_e"] + VENTANA, True); H["tras_listos"][0] += n; H["tras_listos"][1] += ig
                a4 = A4.get(v["semilla"], {}); ref = a4.get(v["slot"]) or a4.get(21 - v["slot"])
                if ref:
                    H["ventanas_con_A4"] += 1
                    n, ig = acuerdo_en(ref, p["t_e"], p["t_e"] + VENTANA); H["A4_tras"][0] += n; H["A4_tras"][1] += ig
                    n, ig = acuerdo_en(ref, p["t_e"], p["t_e"] + VENTANA, True); H["A4_tras_listos"][0] += n; H["A4_tras_listos"][1] += ig
                    n, ig = acuerdo_en(ref, p["t_a"] - ANTES[0], p["t_a"] - ANTES[1]); H["A4_antes"][0] += n; H["A4_antes"][1] += ig
        huella = {k: {"tics": v_[0], "iguales": v_[1], "pct": (round(100 * v_[1] / v_[0], 2) if v_[0] else None)} for k, v_ in H.items() if isinstance(v_, list)}
        huella["ventanas"] = H["ventanas"]; huella["ventanas_con_A4"] = H["ventanas_con_A4"]
        dif_i = [i for i in inst if i["ejec"] != i["propio"]]
        deltas = [i["delta"] for i in dif_i if i["delta"] is not None]
        b = {"vidas": len(vs), "partidas": len({v["semilla"] for v in vs}), "fidelidad_replica": {"igual": fid["igual"], "difiere": fid["difiere"], "sin_replica": fid["sin replica"], "pct_igual": round(100 * fid["igual"] / max(1, fid["igual"] + fid["difiere"]), 2)},
             "fidelidad_en_instantes_con_plan": {"n": len(inst), "replica_igual_a_propio": sum(1 for i in inst if i["replica_igual"]), "pct": round(100 * sum(1 for i in inst if i["replica_igual"]) / max(1, len(inst)), 2)},
             "fm_gana_en_replica": sum(v["fm_gana"] for v in vs), "fm_errores": sum(v["fm_errores"] for v in vs),
             "planes": {"aceptados": len(planes), "por_razon": dict(por_razon), "tics_vivo": resumen([p["tics_vivo"] for p in planes], 1), "instantes_por_plan": resumen([p["instantes"] for p in planes], 1)},
             "1_difieren": {"instantes": n_inst, "difieren": n_dif, "pct": (round(100 * n_dif / n_inst, 2) if n_inst else None), "obedece": sum(p["obedece"] for p in planes), "sujeta": sum(p["sujeta"] for p in planes),
                            "pct_por_plan": resumen([100 * p["difieren"] / p["instantes"] for p in planes if p["instantes"]], 1), "sin_d": sum(p["sin_d"] for p in planes), "negativos": sum(p["negativos"] for p in planes)},
             "2_deformacion": {"por_instante_que_difiere": resumen(deltas, 5), "por_instante_obedece": resumen([i["delta"] for i in dif_i if i["ejec"].startswith("_FM_ir") and i["delta"] is not None], 5),
                               "por_instante_sujeta": resumen([i["delta"] for i in dif_i if not i["ejec"].startswith("_FM_ir") and i["delta"] is not None], 5),
                               "por_instante_diario": resumen([i["delta_diario"] for i in dif_i if i["delta_diario"] is not None], 5),
                               "acumulada_por_plan": resumen([p["defo"] for p in planes], 4), "acumulada_por_plan_diario": resumen([p["defo_diario"] for p in planes], 4), "acumulada_todos_los_tics": resumen([p["defo_todos"] for p in planes], 4),
                               "por_100_tics_vivo": resumen([100 * p["defo"] / p["tics_vivo"] for p in planes if p["tics_vivo"]], 4)},
             "3_soltados_contra_cumplidos": {"soltados": {"n": len(solt), "acumulada": resumen([p["defo"] for p in solt], 4), "por_100_tics": resumen([100 * p["defo"] / p["tics_vivo"] for p in solt if p["tics_vivo"]], 4), "tics_vivo": resumen([p["tics_vivo"] for p in solt], 1), "por_razon": dict(collections.Counter(p["razon"] for p in solt))},
                                            "cumplidos": {"n": len(cump), "acumulada": resumen([p["defo"] for p in cump], 4), "por_100_tics": resumen([100 * p["defo"] / p["tics_vivo"] for p in cump if p["tics_vivo"]], 4), "tics_vivo": resumen([p["tics_vivo"] for p in cump], 1), "por_razon": dict(collections.Counter(p["razon"] for p in cump))},
                                            "muerte_o_fin_con_plan_vivo": {"n": len(muer), "acumulada": resumen([p["defo"] for p in muer], 4)},
                                            "umbral": None},
             "4_compensa": None, "5_huella": huella}
        # umbral: ¿se separan? p10-p90 de soltados contra cumplidos, y cuantos soltados superan la mediana de los cumplidos
        if solt and cump:
            ds, dc = [p["defo"] for p in solt], [p["defo"] for p in cump]
            b["3_soltados_contra_cumplidos"]["umbral"] = {"p90_soltados_menor_que_p10_cumplidos": q(ds, 0.9) < q(dc, 0.1), "p90_cumplidos_menor_que_p10_soltados": q(dc, 0.9) < q(ds, 0.1),
                                                          "soltados_por_encima_de_la_mediana_de_cumplidos": sum(1 for x in ds if x > st.median(dc)), "cumplidos_por_encima_de_la_mediana_de_soltados": sum(1 for x in dc if x > st.median(ds)),
                                                          "mayor_soltado": max(ds), "mayor_cumplido": max(dc)}
        cc = [p for p in cump if p["ahorro"] is not None]
        b["4_compensa"] = {"cumplidos_con_A4_emparejado": len(cc), "cumplidos_sin_pareja_A4": len(cump) - len(cc), "ahorro_tics_ardiendo": resumen([p["ahorro"] for p in cc], 1), "arde_propio": resumen([p["arde"] for p in cc], 1), "arde_A4_misma_ventana": resumen([p["ahorro"] + p["arde"] for p in cc], 1),
                           "ahorro_positivo": sum(1 for p in cc if p["ahorro"] > 0), "ahorro_negativo": sum(1 for p in cc if p["ahorro"] < 0), "spearman_defo_ahorro": spearman([p["defo"] for p in cc], [p["ahorro"] for p in cc]),
                           "ahorro_por_unidad_de_deformacion": resumen([p["ahorro"] / p["defo"] for p in cc if p["defo"] > 0], 1),
                           "todos_los_planes_con_A4": {"n": sum(1 for p in planes if p["ahorro"] is not None), "ahorro": resumen([p["ahorro"] for p in planes if p["ahorro"] is not None], 1), "spearman": spearman([p["defo"] for p in planes if p["ahorro"] is not None], [p["ahorro"] for p in planes if p["ahorro"] is not None])}}
        OUT["brazos"][brazo] = b; PLANES += planes
        print(f"### {brazo}: {json.dumps({k: b[k] for k in ('fidelidad_replica', '1_difieren', 'planes')}, ensure_ascii=False)}", flush=True)
    a4v = [v for v in V if v["brazo"] == "A4"]; fid = collections.Counter()
    for v in a4v:
        fid.update(v["fidelidad"])
    OUT["brazos"]["A4"] = {"vidas": len(a4v), "fidelidad_replica": {"igual": fid["igual"], "difiere": fid["difiere"], "sin_replica": fid["sin replica"], "pct_igual": round(100 * fid["igual"] / max(1, fid["igual"] + fid["difiere"]), 2)}}
    # 6. oraculo contra razonador
    A, B = OUT["brazos"].get("A7h", {}), OUT["brazos"].get("A8", {})
    if A and B:
        OUT["6_oraculo_contra_razonador"] = {"1_pct_difieren": (A["1_difieren"]["pct"], B["1_difieren"]["pct"]), "2_por_instante_mediana": (A["2_deformacion"]["por_instante_que_difiere"].get("mediana"), B["2_deformacion"]["por_instante_que_difiere"].get("mediana")),
                                            "2_acumulada_mediana": (A["2_deformacion"]["acumulada_por_plan"].get("mediana"), B["2_deformacion"]["acumulada_por_plan"].get("mediana")), "2_acumulada_p90": (A["2_deformacion"]["acumulada_por_plan"].get("p90"), B["2_deformacion"]["acumulada_por_plan"].get("p90")),
                                            "3_soltados_mediana": (A["3_soltados_contra_cumplidos"]["soltados"]["acumulada"].get("mediana"), B["3_soltados_contra_cumplidos"]["soltados"]["acumulada"].get("mediana")), "3_cumplidos_mediana": (A["3_soltados_contra_cumplidos"]["cumplidos"]["acumulada"].get("mediana"), B["3_soltados_contra_cumplidos"]["cumplidos"]["acumulada"].get("mediana")),
                                            "4_ahorro_mediana_cumplidos": (A["4_compensa"]["ahorro_tics_ardiendo"].get("mediana"), B["4_compensa"]["ahorro_tics_ardiendo"].get("mediana")), "planes": (A["planes"]["aceptados"], B["planes"]["aceptados"])}
    json.dump(OUT, open(os.path.join(AQUI, "P6_29_medidas.json"), "w"), ensure_ascii=False, indent=1)
    json.dump({"planes": PLANES, "instantes": [i for v in V if v["brazo"] != "A4" for i in v["instantes"]]}, open(os.path.join(AQUI, "P6_29_planes.json"), "w"), ensure_ascii=False)
    json.dump([{k: v.get(k) for k in ("carp", "slot", "brazo", "semilla", "tics", "t_min", "t_max", "muerto", "viva_en_warn5", "fidelidad", "fm_errores", "fm_gana", "segundos")} | {"n_desacuerdos": len(v.get("desacuerdos", [])), "n_arde": len(v.get("arde_tics", [])), "planes": len(v.get("planes", []))} for v in V], open(os.path.join(AQUI, "P6_29_vidas.json"), "w"), ensure_ascii=False, indent=1)
    print("-> P6_29_medidas.json, P6_29_planes.json, P6_29_vidas.json · errores", len(err))

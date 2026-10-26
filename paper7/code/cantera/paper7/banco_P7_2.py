"""[P7-2] EL BANCO: repeticion de decisiones con la creencia aprendida (punto 2) y comprobacion de fontaneria (punto 3).

Replica en seco del cuerpo A4 (molde literal de mide_P6_29.py / banco_P6_15.py: entorno de la imagen A4, obs_de, config_de, WS; el
cuerpo recibe las observaciones del diario por un cable falso y decide tic a tic). En cada tic en que el diario uso un botiquin o
ataco con arco o cerbatana (tabla P7_2_creencias.json, orden natural: la creencia vigente ANTES de vivir esa experiencia):
  (3) fontaneria: la eleccion de la replica (creencia = catalogo, es decir, el decisor tal cual) contra `RADIOGRAFIA.elegido` del diario;
  (2) se vuelve a decidir UNA SEGUNDA VEZ con los mismos obs/memoria cambiando SOLO lo que la prevision espera de ese objeto:
      - usar_botiquin: receta["heal"] = b (decisor_zs.py:493 pone it.heal; :824 lo suma al hp previsto);
      - atacar_*: receta["arma"] = copia del Item con damage = b (decisor_zs.py:852-856 lee arma.damage en la prevision); el candidato
        existe igual (decisor_zs.py:588 mira el Item del catalogo, no la copia).
      La memoria se restaura tras la segunda decision (mem.cedidos, mem.ultimo_ataque: lo que `decide` escribe), como en P6-29.
Escribe P7_2_banco.json. SOLO LECTURA de los diarios, de uno en uno.
    python3 banco_P7_2.py [--hilos 4] [--vidas N]
"""
from __future__ import annotations
import collections, dataclasses, glob, json, os, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    if p not in sys.path: sys.path.insert(0, p)
SCRATCH = os.environ.get("P72_SCRATCH", os.path.join(AQUI, "_P7_2_tmp")); os.makedirs(SCRATCH, exist_ok=True); os.environ["MAPA_DIR"] = SCRATCH
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
from mide_P6_29 import obs_de, config_de, WS                    # noqa: E402  (copia literal del molde; importar no ejecuta su main)
D.decide = __import__("mide_P6_29")._DEC0                       # deshacer el gancho de P6-29 que el import instala: el decisor tal cual

HOOK = {"tabla": {}, "reg": {}}
_DEC0 = D.decide

def _clase(nombre, receta):
    if nombre is None: return "?"
    if nombre.startswith("usar_botiquin"): return "usar botiquin"
    if nombre.startswith("atacar_"): return "atacar"
    if nombre == "ir_centro": return "ir al centro"
    if nombre in ("ir_objeto", "ir_botin"):
        rec = (receta or {}).get("recoger")
        return "ir a por municion" if (rec and rec[0] in ("arrows", "darts")) else "ir a por otro objeto"
    if nombre.startswith(("paso_", "move_")): return "apartarse (un paso)"
    if nombre == "coger": return "coger lo de la casilla"
    if nombre == "ir_pareja": return "ir con el hermano"
    if nombre.startswith("usar_racion"): return "usar racion"
    if nombre.startswith("soltar_"): return "soltar"
    if nombre.startswith("empunar_"): return "empunar otra arma"
    if nombre.startswith("ponerse_"): return "ponerse una prenda"
    if nombre == "noop": return "quedarse quieto"
    return nombre

def _dec72(obs, mundo, mem, tick, bloqueos=None):
    ac, ra = _DEC0(obs, mundo, mem, tick, bloqueos)
    e = HOOK["tabla"].get(tick)
    if e is not None:
        rec = {"t": tick, "elegido_replica": ra.get("elegido"), "d_replica": {k: (v["d"] if isinstance(v, dict) else v) for k, v in (ra.get("candidatos") or {}).items()}}
        ced0, ua0 = dict(mem.cedidos), mem.ultimo_ataque
        c0 = D.candidatos
        def c_cre(*a, **k):
            out = []
            for nombre, receta in c0(*a, **k):
                r2 = dict(receta)
                if e["objeto"] == "botiquin" and nombre == "usar_botiquin":
                    r2["heal"] = e["b_antes"]
                elif e["objeto"] in ("bow", "blowgun") and nombre.startswith("atacar_") and getattr(r2.get("arma"), "id", None) == e["objeto"]:
                    r2["arma"] = dataclasses.replace(r2["arma"], damage=e["b_antes"])
                out.append((nombre, r2))
            HOOK["recetas"] = {n: r for n, r in out}
            return out
        D.candidatos = c_cre
        try:
            _ac2, ra2 = _DEC0(obs, mundo, mem, tick, bloqueos)
            el2 = ra2.get("elegido"); rec["elegido_creencia"] = el2; rec["clase_creencia"] = _clase(el2, (HOOK.get("recetas") or {}).get(el2))
            rec["d_creencia"] = {k: (v["d"] if isinstance(v, dict) else v) for k, v in (ra2.get("candidatos") or {}).items()}
        except Exception as ex:
            rec["error"] = repr(ex)[:160]
        finally:
            D.candidatos = c0; mem.cedidos, mem.ultimo_ataque = ced0, ua0
        HOOK["reg"][tick] = rec
    return ac, ra

D.decide = _dec72

def lee(f):
    tics = []; pc = sm = cat = fin = None; sp = it = 5; EL = {}
    for r in U.lee(f):
        k = r.get("k")
        if k == "player_config": pc = r
        elif k == "static_map": sm = r
        elif k == "catalogo": cat = r
        elif k == "arranque":
            s = json.dumps(r); m = re.search(r'"speed"\s*:\s*(\d+)', s); sp = int(m.group(1)) if m else 5
            m = re.search(r'"intelligence"\s*:\s*(\d+)', s); it = int(m.group(1)) if m else 5
        elif k == "tick" and r.get("phase") == "live":
            tics.append(r); EL[r["tick"]] = (r.get("RADIOGRAFIA") or {}).get("elegido")
        elif k == "final": fin = r
    return pc, sm, cat, tics, sp, it, fin, EL

def vida(carp, slot, tabla):
    t0 = time.time()
    f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]
    pc, sm, cat, tics, sp, it, fin, EL = lee(f)
    HOOK["tabla"] = {e["t"]: e for e in tabla}; HOOK["reg"] = {}
    cfg = config_de(pc, sm, cat)
    alma = PP.AlmaPareja(); alma.artefacto_subido = True; PP._envuelve(alma)
    mudo = lambda rec: None
    _logs = (PC.log, PF.log, PP.log); PC.log = mudo; PF.log = mudo; PP.log = mudo
    msgs = [json.dumps(cfg)] + [json.dumps(obs_de(r, sp, it)) for r in tics] + [json.dumps({"type": "final", "placement": (fin or {}).get("placement"), "kills": 0, "score": 0.0, "reason": (fin or {}).get("reason"), "match_ticks": (fin or {}).get("match_ticks")})]
    n_tics = len(tics); del tics
    ws = WS(msgs); out_real = sys.stdout
    try:
        sys.stdout = open(os.devnull, "w"); asyncio.run(PC.decisor(ws, alma))
    finally:
        sys.stdout = out_real; PC.log, PF.log, PP.log = _logs; PC._DIARIO.clear()
    dec = []
    for e in tabla:
        r = HOOK["reg"].get(e["t"]) or {}
        dec.append({**e, "elegido_diario": EL.get(e["t"]), "elegido_replica": r.get("elegido_replica"), "fiel": r.get("elegido_replica") == EL.get(e["t"]),
                    "elegido_creencia": r.get("elegido_creencia"), "clase_creencia": r.get("clase_creencia"), "cambia": (r.get("elegido_creencia") is not None and r.get("elegido_creencia") != EL.get(e["t"])),
                    "d_replica": r.get("d_replica"), "d_creencia": r.get("d_creencia"), "error": r.get("error"), "sin_replica": e["t"] not in HOOK["reg"]})
    return {"carpeta": carp, "slot": slot, "tics": n_tics, "decisiones": dec, "segundos": round(time.time() - t0, 1)}

def _mp(args):
    carp, slot, tabla = args
    try:
        r = vida(carp, slot, tabla); n = len(r["decisiones"])
        print(f"  {carp} s{slot}: {r['tics']} tics · {n} decisiones · fieles {sum(1 for d in r['decisiones'] if d['fiel'])} · cambian {sum(1 for d in r['decisiones'] if d['cambia'])} · {r['segundos']} s", flush=True)
        return r
    except Exception as ex:
        import traceback; traceback.print_exc(); return {"carpeta": carp, "slot": slot, "error": repr(ex)[:300], "decisiones": []}

if __name__ == "__main__":
    a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4; tope = int(a[a.index("--vidas") + 1]) if "--vidas" in a else None
    T = json.load(open(os.path.join(AQUI, "P7_2_creencias.json")))
    por = collections.defaultdict(list)
    for e in T: por[(e["carpeta"], e["asiento"])].append(e)
    tareas = [(c, s, sorted(v, key=lambda e: e["t"])) for (c, s), v in sorted(por.items())][:tope]
    print(f"### P7-2 banco: {len(tareas)} vidas con decisiones · {sum(len(t[2]) for t in tareas)} decisiones · hilos {hilos}", flush=True)
    if hilos > 1:
        import multiprocessing as mp
        # un proceso NUEVO por vida (maxtasksperchild=1): con varias vidas en el mismo proceso, estado de modulo de una vida
        # contaminaba la siguiente y el candidato de defensa del hermano desaparecia (visto en la primera corrida: 1674 fieles de 2450;
        # la misma vida sola, 334 de 334)
        with mp.get_context("fork").Pool(hilos, maxtasksperchild=1) as pool: res = pool.map(_mp, tareas, chunksize=1)
    else:
        res = [_mp(t) for t in tareas]
    dec = [d for r in res for d in r["decisiones"]]
    print("decisiones:", len(dec), "fieles:", sum(1 for d in dec if d["fiel"]), "sin replica:", sum(1 for d in dec if d["sin_replica"]), "errores:", sum(1 for d in dec if d.get("error")))
    json.dump({"vidas": res}, open(os.path.join(AQUI, "P7_2_banco.json"), "w"), indent=0, ensure_ascii=False)

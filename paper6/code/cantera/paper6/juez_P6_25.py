"""[P6-25 · 2, 3, 4, 5] EL JUEZ: la puerta6 real de A7h, EN PROCESO APARTE, juzgando cualquier plan sobre
la instantanea del cuerpo en un instante (las de `escenas_P6_25.py`). Cada proceso obrero levanta un alma
espejo (`policy_pareja23.AlmaPareja23(con_proceso=False)`, la misma del proceso juez de P6-23), carga la
instantanea (obs con ojos, memoria, bloqueos, C, parte del hermano, mundo) y llama a `_juzga` tal cual.
Ademas de veredicto y ventaja (la ganancia imaginada), captura las filas que mas pesaron en contra
(ganchos de `banco_P6_15.py`, copiados: `atribuye`) y mide si el destino queda dentro del circulo al que
va la fase (la regla del juego de P6-21: dentro si la distancia al centro no supera el radio entero) y si
el oraculo lo da por a salvo al llegar (`Oraculo.a_salvo`).

Entrada: una lista de planes {id, modelo, snap (ruta de la instantanea), tramos, ...}; el juicio se hace
sobre la instantanea que diga `snap` (la de la pregunta, o la de t+D para el retraso, punto 3).

    python3 juez_P6_25.py ETIQ [--hilos 4]     lee P6_25_planes_ETIQ.json -> P6_25_juicios_ETIQ.json
    python3 juez_P6_25.py oraculo              el plan del oraculo de cada escena (su texto, traducido)
    python3 juez_P6_25.py retraso ETIQ         los planes de ETIQ juzgados en t+D, D = el retraso medido de esa llamada
"""
from __future__ import annotations
import collections, glob, gzip, json, math, os, pickle, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import escenas_P6_25 as ES                                      # noqa: E402  (pone el entorno de A7h e importa el alma)
from alma import policy_cortex as PC                            # noqa: E402
from alma import policy_forma as PF                             # noqa: E402
from alma import forma_viva as FV                               # noqa: E402
import forma as F                                               # noqa: E402
import traductor_forma as TF                                    # noqa: E402
import policy_pareja as PP                                      # noqa: E402
import policy_pareja16 as P16                                   # noqa: E402
import policy_pareja23 as P23                                   # noqa: E402
import oraculo_P6_14 as O                                       # noqa: E402
VERSION = "juez_P6_25 (P6-25): puerta6 real de A7h en proceso aparte sobre instantaneas; filas en contra; dentro del circulo futuro"
C = (24, 24)

# ── ganchos de captura, copia de banco_P6_15.py (instalados DESPUES de policy_pareja16, que ya puso el comparador puerta6) ──
CAP = {"on": False, "fotos": [], "comp": None, "base": None}
_dcp0 = F.d_con_pisos
def _dcp(F_, pisos=None):
    if CAP["on"]:
        CAP["fotos"].append((dict(F_), dict(pisos or {})))
    return _dcp0(F_, pisos)
F.d_con_pisos = _dcp
_mph0 = F.mejor_propia_H
def _mph(*a, **k):
    r = _mph0(*a, **k)
    if CAP["on"]:
        CAP["comp"] = r
    return r
F.mejor_propia_H = _mph
_base0 = FV._base
def _base(*a, **k):
    r = list(_base0(*a, **k))
    if CAP["on"]:
        CAP["base"] = [n for n, _rec in r]
    return r
FV._base = _base


def atribuye(fotos, tics, n_base, cs, t0):
    """[copia literal de banco_P6_15.atribuye]"""
    L = len(tics)
    if not L or len(fotos) != L * (1 + n_base) or cs is None:
        return None, None, None
    plan = fotos[:L]
    ds_cs = [round(p["d"], 9) if p.get("d") is not None else None for p in cs]
    ci = None
    for j in range(n_base):
        ch = fotos[L * (1 + j): L * (2 + j)]
        ds = [round(_dcp0(f, pz), 9) for f, pz in ch]
        if ds == ds_cs:
            ci = j; break
    if ci is None:
        return None, None, None
    comp = fotos[L * (1 + ci): L * (2 + ci)]
    W = [0.5 ** ((t - t0) / F.MEDIA_VIDA) for t in tics]
    def area(quitar=None):
        s = 0.0
        for i in range(L):
            fp, pp = plan[i]; fc, pc = comp[i]
            if quitar is not None:
                fp = {k: v for k, v in fp.items() if k != quitar}; fc = {k: v for k, v in fc.items() if k != quitar}
                pp = {k: v for k, v in pp.items() if k != quitar}; pc = {k: v for k, v in pc.items() if k != quitar}
            s += W[i] * (_dcp0(fc, pc) - _dcp0(fp, pp))
        return s
    a0 = area()
    filas = set()
    for f, pz in plan + comp:
        filas |= {k for k, v in f.items() if v} | {k for k, v in pz.items() if v}
    contra = []
    for k in sorted(filas):
        dk = area(k) - a0
        if abs(dk) >= 1e-4:
            Mp = max(float(plan[0][0].get(k) or 0.0), float(plan[0][1].get(k) or 0.0))
            Mc = max(float(comp[0][0].get(k) or 0.0), float(comp[0][1].get(k) or 0.0))
            contra.append([k, round(dk, 5), round(Mp, 4), round(Mc, 4)])
    contra.sort(key=lambda x: -x[1])
    return contra, None, ci
# ── fin de la copia ──


ESPEJO = {"alma": None, "mundo_id": None, "orac": None}
ULT_VER = {}


def _log(rec):
    if rec.get("k") == "forma_evaluada":
        ULT_VER[rec.get("id")] = rec


def espejo():
    if ESPEJO["alma"] is None:
        mudo = lambda rec: None
        PC.log = _log; PF.log = _log; PP.log = _log; P16.log = _log; P23.log = _log
        a = P23.AlmaPareja23(con_proceso=False); a.hilo = None; a.evalua_en_hilo = False; a.phase = "live"; a.artefacto_subido = True
        ESPEJO["alma"] = a
    return ESPEJO["alma"]


def carga_snap(p):
    with gzip.open(p, "rb") as f:
        return pickle.loads(f.read())


def fase_activa(fases, t):
    i = None
    for k, f in enumerate(fases):
        if t >= f[0]:
            i = k
    return i


def juzga_lote(snap_path, planes):
    """planes: [{id, modelo, tramos, ...}] sobre UNA instantanea. Devuelve los juicios."""
    a = espejo(); job = carga_snap(snap_path)
    if job.get("mundo") is not None:
        a.mundo = job["mundo"]
    a.tick = job["tick"]; a.conf.C = job["C"]; a.herm_dicho = job["herm_dicho"]; a.herm_tick = job["herm_tick"]; a.ultima_obs = job["ultima_obs"]
    a.vivas = []; a.pendientes = {}; a.reeval_pend = {}; a.cerradas.clear(); a.conf.callado_hasta = None
    obs, mem, blo = job["obs"], job["mem"], job["blo"]
    fases = [tuple(z) for z in (a.mundo.zone_schedule or [])]; i = fase_activa(fases, a.tick)
    r1 = fases[i][4] if i is not None else None
    sp = int(((obs.get("you") or {}).get("stats") or {}).get("speed") or 5)
    if ESPEJO["orac"] is None or ESPEJO["mundo_id"] != id(a.mundo):
        ESPEJO["orac"] = O.Oraculo(a.mundo, sp); ESPEJO["mundo_id"] = id(a.mundo)
    orac = ESPEJO["orac"]
    out = []
    for n, p in enumerate(planes):
        tramos = p.get("tramos")
        base = {k: p.get(k) for k in ("id", "modelo", "etiqueta", "snap_clave", "retraso")}
        base.update({"snap": snap_path, "tick_juicio": a.tick})
        if not tramos:
            out.append(dict(base, veredicto=None, motivo="sin plan (intraducible, callo o error)")); continue
        try:
            fv = FV.FormaViva(f"J{a.tick}_{n}", [dict(t) for t in tramos], a.tick, origen="consejero")
            CAP["on"] = True; CAP["fotos"] = []; CAP["comp"] = None; CAP["base"] = None
            t0 = time.perf_counter()
            try:
                ver, ar, cf, tics = a._juzga(fv, obs, mem, blo)
            finally:
                CAP["on"] = False
            ms = round((time.perf_counter() - t0) * 1000.0, 1)
            comp = CAP["comp"]; cs, quien, n_base, _mv = comp if comp else (None, None, 0, None)
            contra = None
            for nb in (1, n_base, len(CAP["base"] or [])):
                if nb:
                    contra, _p, _ci = atribuye(CAP["fotos"], list(tics or []), nb, cs, a.tick)
                    if contra is not None:
                        break
            dest = next((tuple(t["destino"]) for t in tramos if t.get("destino")), tuple(int(x) for x in (obs.get("you") or {}).get("pos")))
            llegada = (tics[0] if tics else a.tick)
            j = dict(base, veredicto=ver, ventaja=round(float(ar or 0.0), 6), margen=round(float(a._margen_de(fv)), 4), ms=ms, comparador=quien, n_base=n_base,
                     puntos_control=list(tics or []), destino=list(dest), fase=(i + 1 if i is not None else None), r1=r1,
                     dentro_futuro=(None if r1 is None else bool(math.dist(dest, C) <= r1)), a_salvo=bool(orac.a_salvo(dest, int(llegada))) if fases else None,
                     contra=(contra[:8] if contra else None), curva=[{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None)} for c in (cf or [])][:6])
            out.append(j)
        except Exception as ex:
            import traceback
            out.append(dict(base, veredicto=None, motivo="revienta: " + repr(ex)[:200], traza=traceback.format_exc()[-600:]))
        finally:
            a.vivas = []; a.cerradas.clear(); a.pendientes = {}; a.reeval_pend = {}
    return out


def _lote_mp(args):
    snap, planes = args
    try:
        return juzga_lote(snap, planes)
    except Exception as ex:
        return [{"id": p.get("id"), "modelo": p.get("modelo"), "snap": snap, "veredicto": None, "motivo": "lote revienta: " + repr(ex)[:200]} for p in planes]


def corre(lotes, hilos):
    import multiprocessing as mp
    ctx = mp.get_context("spawn"); t0 = time.time()
    with ctx.Pool(hilos) as pool:
        res = pool.map(_lote_mp, lotes, chunksize=1)
    return [j for lote in res for j in lote], round(time.time() - t0, 1)


def planes_oraculo(E):
    out = []
    for e in E["escenas"]:
        if not e["propia"]:
            continue
        tx = (e.get("oraculo") or {}).get("texto")
        formas, inf = TF.traduce(tx, e["escena_traductor"], E["filas"][e["carp"]]) if tx else ([], {})
        out.append({"id": f"{e['carp']}_{e['slot']}_{e['tick']}", "modelo": "oraculo", "tramos": (TF.solo_tramos(formas[0]) if formas else None), "snap": e["snap"]["0"], "snap_clave": "0",
                    "destino_oraculo": (e.get("oraculo") or {}).get("destino"), "H": (e.get("oraculo") or {}).get("H")})
    return out


def retraso_de(ms, retrasos):
    """El primer punto de la rejilla de instantaneas que no queda antes de la respuesta (ms -> tics a 24/s)."""
    if ms is None:
        return None
    tics = int(math.ceil(ms / 1000.0 * 24.0))
    return next((d for d in retrasos if d >= tics), None)


if __name__ == "__main__":
    a = sys.argv; hilos = int(a[a.index("--hilos") + 1]) if "--hilos" in a else 4
    E = json.load(open(os.path.join(AQUI, "P6_25_escenas.json"))); por = {f"{e['carp']}_{e['slot']}_{e['tick']}": e for e in E["escenas"]}
    etiq = a[1]
    if etiq == "oraculo":
        planes = planes_oraculo(E); salida = "oraculo"
    elif etiq == "retraso":
        fuente = a[2]; P = json.load(open(os.path.join(AQUI, f"P6_25_planes_{fuente}.json")))["planes"]; planes = []
        for p in P:
            e = por[p["id"]]; d = retraso_de(p.get("ms"), E["retrasos"])
            snap = e["snap"].get(str(d)) if d else None
            planes.append(dict(p, snap=snap, snap_clave=str(d), retraso=d, etiqueta=fuente, tramos=(p["tramos"] if snap else None)) if snap else dict(p, snap=None, snap_clave=str(d), retraso=d, etiqueta=fuente, tramos=None, sin_instantanea=("muerto o partida acabada" if d else "retraso mayor que la rejilla")))
        salida = f"retraso_{fuente}"
    else:
        P = json.load(open(os.path.join(AQUI, f"P6_25_planes_{etiq}.json")))["planes"]
        planes = [dict(p, snap=por[p["id"]]["snap"]["0"], snap_clave="0", etiqueta=etiq) for p in P]; salida = etiq
    con = [p for p in planes if p.get("snap")]; sin = [p for p in planes if not p.get("snap")]
    lotes = collections.defaultdict(list)
    for p in con:
        lotes[p["snap"]].append({k: p.get(k) for k in ("id", "modelo", "tramos", "etiqueta", "snap_clave", "retraso")})
    print(f"JUEZ {salida}: {len(con)} planes en {len(lotes)} instantaneas ({len(sin)} sin instantanea) · {hilos} procesos", flush=True)
    juicios, seg = corre(sorted(lotes.items()), hilos)
    juicios += [{"id": p["id"], "modelo": p.get("modelo"), "etiqueta": p.get("etiqueta"), "snap_clave": p.get("snap_clave"), "retraso": p.get("retraso"), "veredicto": None, "motivo": p.get("sin_instantanea") or "sin instantanea"} for p in sin]
    cnt = collections.Counter((j.get("modelo"), j.get("veredicto")) for j in juicios)
    json.dump({"nota": f"P6-25. Juicios de la puerta6 real (proceso aparte) sobre las instantaneas: {salida}.", "version": VERSION, "segundos": seg, "cuenta": {f"{m}|{v}": n for (m, v), n in sorted(cnt.items(), key=str)}, "juicios": juicios},
              open(os.path.join(AQUI, f"P6_25_juicios_{salida}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"-> P6_25_juicios_{salida}.json · {seg} s · " + json.dumps({f'{m}|{v}': n for (m, v), n in sorted(cnt.items(), key=str)}))

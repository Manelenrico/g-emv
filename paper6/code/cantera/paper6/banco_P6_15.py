"""[P6-15] EL BANCO DE LA PUERTA HONESTA CONSIGO MISMA: una vida de A4 repetida en
seco por la via real (= `banco_P6_14.py`, copiado tal cual en su arnes), con
la puerta real del cuerpo congelado juzgando los planes del oraculo Y, ademas,
para cada plan:

  1. EL EXCESO DE CONFIANZA: la casilla que el comparador de la puerta (el mejor
     candidato propio proyectado) decia ocupar en cada punto de control, contra
     la casilla REAL del diario en ese tic; y la S-8 del comparador en la foto
     de la puerta (con piso) contra la S-8 del mismo candidato en la eleccion
     real de ese tic (`radio["candidatos"][quien]["filas"]`).
  2. EL TECHO: el mismo plan juzgado contra la trayectoria real imaginada
     (`puerta6_P6_15.curva_real`), misma regla y mismo margen.
  3. LA VERSION USABLE: el mismo plan juzgado contra el cuerpo imaginado
     decidiendo paso a paso (`puerta6_P6_15.rollout`), misma regla; coste por
     juicio y fidelidad del rollout contra el diario.
  4. EL HORIZONTE: si el fuego de mi casilla cae fuera de la ventana del plan.

    python banco_P6_15.py <carpeta> <slot> [salida.json] [--tope N] [--cada N]

INSTRUMENTO DE MEDIDA. No toca ni un byte del cuerpo congelado ni de la puerta
del cinco: lo nuevo esta en `puerta6_P6_15.py` (version nueva, declarada).
"""
from __future__ import annotations
import collections, copy, glob, json, os, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    sys.path.insert(0, p)
SCRATCH = os.environ.get("P615_SCRATCH", os.path.join(AQUI, "_P6_15_tmp"))
os.makedirs(SCRATCH, exist_ok=True)
os.environ["MAPA_DIR"] = SCRATCH
for _k, _v in (("GEMV_MIEDO", "0"), ("GEMV_VIDA_AJENA", "0"), ("GEMV_VIDA_AJENA_M", "0.25"),
               ("GEMV_MEMORIA", os.path.join(RAIZ, "paintball", "alma", "memoria_aprendida_p95.json")),
               ("GEMV_CORTEX", "0"), ("GEMV_FORMA", "0"), ("GEMV_CURIOSIDAD", ""), ("GEMV_CURIOSIDAD_FORMA", "0"),
               ("GEMV_OJOS", "1"), ("GEMV_COMPANIA_TECHO", "0.32"), ("GEMV_HILO_FORMA", "0"), ("GEMV_CONSEJERO_FORMA", "0")):
    os.environ.setdefault(_k, _v)
import asyncio
import serie_util as U
from alma import policy_cortex as PC
from alma import policy_forma as PF
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A
from alma import forma_viva as FV
from alma import confianza_viva as CVIVA
import forma as F
import traductor_forma as TF
import policy_pareja as PP
import parte2 as P2
import arreglos_P6_6 as R6, arreglos_P6_8b as R8, filas10_P6_10 as F10, amenaza11_P6_11 as M11
import oraculo_P6_14 as O
import puerta6_P6_15 as P6

assert A.EMPATIA_ON is True and (A.H_PREV, A.H_GOLPE) == (0.25, 1.0) and A.MIEDO_ON is False and A.VIDA_AJENA_ON is False, \
    ("cableado", A.EMPATIA_ON, A.H_PREV, A.H_GOLPE, A.MIEDO_ON, A.VIDA_AJENA_ON)
assert D.A is A, "el decisor no valora con la v42"
assert not PF.FORMA_ON and not PF.CUR_FORMA_ON and not PF.HILO_ON and not PF.CONSEJERO_ON

HECHO = {}
HECHO.update(R6.aplica(PP.AlmaPareja, PC.log)); HECHO.update(R8.aplica(PC.log)); HECHO.update(F10.aplica(PC.log)); HECHO.update(M11.aplica(PC.log))
assert HECHO.get("oido") and HECHO.get("don") and HECHO.get("pareja_parte") and HECHO.get("mochila_llena") and HECHO.get("filas10") and HECHO.get("manos"), HECHO
_ESTADO_MODULOS = (D.candidatos, D.decide, A.appraise, PC.PARTE.emite)

# ── captura de lo que la puerta mira, sin tocarla (como en P6-14) + la base ──
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


def s8_de(fotos, L, j, con_piso):
    """S-8 en la primera foto del candidato j (chunk j+1), cruda o con piso."""
    if j is None or len(fotos) < L * (2 + j):
        return None
    f, pz = fotos[L * (1 + j)]
    m = float(f.get("S-8-EXPOSICION") or 0.0)
    return max(m, float(pz.get("S-8-EXPOSICION") or 0.0)) if con_piso else m


def carga(f):
    recs, tics, sp, it, fin = [], [], 5, 5, None
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
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    return pc, sm, cat, tics, sp, it, fin


def ligero(f):
    T = {}
    for r in U.lee(f):
        if r.get("k") == "tick" and r.get("phase") == "live" and r.get("pos"):
            T[r["tick"]] = ((int(r["pos"][0]), int(r["pos"][1])), r.get("hp"))
    return T


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


CADAS = (1, 6, 11)      # el rollout decide en todos los tics (elegido); alternativas: con piernas listas y cada 6 / cada 11


def vida(carp, slot, salida=None, tope=None, callado=True, cada=1):
    t_ini = time.time()
    fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, "*policy_agent_1*.art.log"))}
    otro = 21 - slot
    T_h = ligero(fs[otro])
    pc, sm, cat, tics, sp, it, fin = carga(fs[slot])
    if tope:
        tics = tics[:tope]
    cfg = config_de(pc, sm, cat)
    filas_mapa = list(sm["filas"])
    diario = {r["tick"]: str((r.get("RADIOGRAFIA") or {}).get("elegido") or "") for r in tics}
    # LA TRAYECTORIA REAL (posicion, hp, elegido por tic); fuera del diario, la ultima casilla
    T_real = {r["tick"]: ((int(r["pos"][0]), int(r["pos"][1])), r.get("hp"), diario[r["tick"]]) for r in tics if r.get("pos")}
    tics_real = sorted(T_real)
    import bisect
    def real_en(t):
        if t in T_real:
            return T_real[t]
        i = bisect.bisect_right(tics_real, t) - 1
        return T_real[tics_real[max(0, i)]] if tics_real else None
    def pos_real(t):
        return real_en(t)[0]
    def accion_real(t):
        el = T_real.get(t, (None, None, ""))[2] or ""
        if el.startswith("usar_"):
            return el
        if el.startswith("coger"):
            return "coger"
        return None
    muerte = max(diario) if diario else None
    an = next((d for d in json.load(open(os.path.join(AQUI, "P6_13_anillo.json")))["muertes"] if d["carp"] == carp and d["slot"] == slot), None)

    D.candidatos, D.decide, A.appraise, PC.PARTE.emite = _ESTADO_MODULOS
    alma = PP.AlmaPareja()
    alma.artefacto_subido = True
    PP._envuelve(alma)
    # `decidir()` aplana `radio["candidatos"]` a floats (policy_cortex:615): las filas
    # por candidato se capturan envolviendo `D.decide` por encima de la cadena.
    CAPR = {"ra": None}
    _dec_chain = D.decide
    def _dec_cap(*a, **k):
        ac, ra = _dec_chain(*a, **k)
        # `decidir()` aplana ESTE MISMO dict despues: se copian las filas ahora
        CAPR["ra"] = {"candidatos": {kk: {"filas": dict((vv.get("filas") or {}))} for kk, vv in (ra.get("candidatos") or {}).items() if isinstance(vv, dict)}}
        return ac, ra
    D.decide = _dec_cap
    orac = None; herm = None; propio = pc["slot"]
    decis = []; repro = collections.Counter(); difs = []; ms_p = []; ms_roll = []
    fases = [tuple(z) for z in (pc.get("zone_schedule") or [])]
    aviso_tics = {}
    for i, f in enumerate(fases):
        for r in tics:
            if r["tick"] >= f[0] and int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0:
                aviso_tics[r["tick"]] = i; break
    n_plan = [0]
    _decidir0 = alma.decidir
    ULT_VER = {}

    def decidir(obs, _d=_decidir0):
        accion, radio = _d(obs)
        radio_full = CAPR["ra"] if isinstance(CAPR["ra"], dict) else {}
        nonlocal orac, herm
        t = alma.tick
        if orac is None and alma.mundo is not None:
            orac = O.Oraculo(alma.mundo, sp); herm = alma.mundo.teammate_slot
        if radio is None or alma.phase != "live":
            return accion, radio
        el = str(radio.get("elegido") or "")
        if t in diario:
            if el == diario[t]:
                repro["igual"] += 1
            else:
                repro["difiere"] += 1
                if len(difs) < 10:
                    difs.append([t, el, diario[t]])
        if int((obs.get("you") or {}).get("move_ready_in") or 0) != 0:
            return accion, radio
        o2 = alma.ultima_obs or obs
        pos = tuple(int(x) for x in (o2.get("you") or {}).get("pos"))
        Dm = orac.bfs(pos); seg = orac.seguras(pos, t, Dm)
        ar, ta, pasos_a, holg = orac.dispara(pos, t, Dm, seg)
        m1 = ar or (holg is not None and holg <= max(O.MARGENES))
        m2 = t in aviso_tics
        if not (m1 or m2):
            return accion, radio
        riv = orac.rivales_de(o2, herm, propio)
        ph = T_h.get(t)
        planes, info = orac.propone(pos, t, riv, ph[0] if ph else None)
        radio_real = radio_full.get("candidatos") or {}
        s8_real = {k: float((v.get("filas") or {}).get("S-8-EXPOSICION") or 0.0) for k, v in radio_real.items() if isinstance(v, dict)}
        dec = {"tick": t, "pos": list(pos), "hp": (o2.get("you") or {}).get("hp"), "arde": ar, "t_arde": ta, "pasos_a": pasos_a, "holgura": holg,
               "momentos": ([1] if m1 else []) + ([2] if m2 else []), "fase_aviso": aviso_tics.get(t), "fase_activa": orac.fase_activa(t),
               "radio": round(orac.radio_dps(t)[0], 2), "info": info, "hermano": (list(ph[0]) if ph else None),
               "cands_cuerpo": sorted(radio_real.keys()), "elegido": el, "s8_real_noop": s8_real.get("noop"), "planes": []}
        # EL CONTEXTO DE LA PUERTA (el mismo que usa `_juzga`) y EL ROLLOUT (uno por decision)
        e0, suelo, pisos = alma._contexto(o2)
        t_fin = t + (max((p["pasos"] for p in planes), default=0) * orac.coste) + max(O.HORIZONTES) + 1
        SNAPS = {}
        dec["rollouts"] = {}
        seq_r = [orac.arde(T_real[x][0], x) for x in range(t, t + 201) if x in T_real]
        for cd in CADAS:
            t_r0 = time.perf_counter()
            snaps, n_dec = P6.rollout(o2, e0, t_fin, alma.mundo, alma.mem, alma.bloqueos, suelo, cada=cd)
            ms_r = round((time.perf_counter() - t_r0) * 1000.0, 1)
            if cd == CADAS[0]:
                ms_roll.append(ms_r)
            SNAPS[cd] = snaps
            # fidelidad del rollout contra el diario en la ventana [t, t+200]
            fid = {}
            for k in (50, 100, 200):
                rr = T_real.get(t + k)
                if rr is not None and (t + k) in snaps:
                    fid[f"dist_{k}"] = max(abs(snaps[t + k]["pos"][0] - rr[0][0]), abs(snaps[t + k]["pos"][1] - rr[0][1]))
                    fid[f"arde_pred_{k}"] = orac.arde(tuple(snaps[t + k]["pos"]), t + k); fid[f"arde_real_{k}"] = orac.arde(rr[0], t + k)
            seq_p = [orac.arde(tuple(snaps[x]["pos"]), x) for x in range(t, min(t + 200, t_fin) + 1) if x in snaps]
            fid["tics_arde_pred"] = sum(seq_p); fid["tics_arde_real"] = sum(seq_r); fid["n_real"] = len(seq_r)
            fid["vueltas_pred"] = sum(1 for a, b in zip(seq_p, seq_p[1:]) if (not a) and b); fid["vueltas_real"] = sum(1 for a, b in zip(seq_r, seq_r[1:]) if (not a) and b)
            fid["muere_real_en_200"] = (muerte is not None and muerte <= t + 200)
            dec["rollouts"][str(cd)] = {"ms": ms_r, "tics": t_fin - t, "decisiones": n_dec, "fidelidad": fid,
                                       "camino": [[x, list(snaps[x]["pos"]), round(snaps[x]["hp"], 1)] for x in sorted(snaps) if (x - t) % 11 == 0]}
        escena = {"pos": list(pos), "suelo": [{"id": x.get("id"), "pos": list(x["pos"])} for x in ((o2.get("visible") or {}).get("items") or []) if x.get("pos")]}
        for p in planes:
            for H in O.HORIZONTES:
                n_plan[0] += 1
                texto = O.Oraculo.texto_forma(p["destino"], H, "salir del anillo: " + ",".join(p["criterios"]))
                cnt = collections.Counter(); formas, inf = TF.traduce(texto, escena, filas_mapa, cnt)
                reg = {"criterios": p["criterios"], "destino": list(p["destino"]), "propia": p["propia"], "pasos": p["pasos"], "cheb": p["cheb"], "llegada": p["llegada"],
                       "pasos_hermano": p.get("pasos_hermano"), "rivales_cerca": {str(k): v for k, v in p["rivales_cerca"].items()}, "H": H}
                if not formas:
                    reg["veredicto"] = "intraducible"; dec["planes"].append(reg); continue
                tramos = TF.solo_tramos(formas[0])
                fv = FV.FormaViva(f"O{n_plan[0]}", tramos, t, origen="consejero")
                CAP["on"] = True; CAP["fotos"] = []; CAP["comp"] = None; CAP["base"] = None
                try:
                    ok = alma._acepta_o_no(fv, o2)
                finally:
                    CAP["on"] = False
                fotos = CAP["fotos"]; comp = CAP["comp"]; base = CAP["base"] or []
                if fv in alma.vivas:
                    alma.vivas.remove(fv)
                alma.cerradas.clear()
                ms = alma.ms_forma[-1] if alma.ms_forma else None; ms_p.append(ms)
                cs, quien, n_base, _mv = comp if comp else (None, None, 0, None)
                tcs = list(fv.tics); L = len(tcs)
                reg.update({"acepta": bool(ok), "veredicto": ULT_VER.get(fv.id, "?"), "ventaja": round(float(fv.ventaja or 0.0), 6), "margen": round(alma._margen_de(fv), 4),
                            "tics": tcs, "comparador": quien, "n_base": n_base, "ms": ms,
                            "curva": [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "pos": list(c.get("pos") or ())} for c in (fv.curva or [])],
                            "curva_comp": [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "pos": list(c.get("pos") or ())} for c in (cs or [])]})
                contra, _pts, ci = atribuye(fotos, tcs, n_base, cs, t)
                reg["contra"] = contra
                # 1 · EL EXCESO DE CONFIANZA: lo que el comparador decia contra lo real
                if cs:
                    ex = []
                    for c in cs:
                        rr = real_en(c["tic"]); pr = rr[0] if rr else None
                        ex.append({"tic": c["tic"], "pos_comp": list(c["pos"]), "salvo_comp": orac.a_salvo(tuple(c["pos"]), c["tic"]) if c.get("pos") else None,
                                   "arde_comp": orac.arde(tuple(c["pos"]), c["tic"]) if c.get("pos") else None,
                                   "pos_real": (list(pr) if pr else None), "arde_real": (orac.arde(pr, c["tic"]) if pr else None),
                                   "muerto_real": (muerte is not None and c["tic"] > muerte), "hp_real": (rr[1] if rr and c["tic"] <= (muerte or 10 ** 9) else 0),
                                   "vida_comp": round(c["vida"], 2) if c.get("vida") is not None else None})
                    reg["exceso"] = ex
                    j_noop = base.index("noop") if "noop" in base else None
                    j_comp = base.index(quien) if quien in base else ci
                    reg["s8"] = {"proj_comp": s8_de(fotos, L, j_comp, False), "proj_comp_piso": s8_de(fotos, L, j_comp, True),
                                 "proj_noop": s8_de(fotos, L, j_noop, False), "proj_noop_piso": s8_de(fotos, L, j_noop, True),
                                 "proj_plan": (float(fotos[0][0].get("S-8-EXPOSICION") or 0.0) if fotos else None),
                                 "real_comp": s8_real.get(quien), "real_noop": s8_real.get("noop"), "real_elegido": s8_real.get(el), "elegido": el}
                # 2 · EL TECHO: contra la trayectoria real imaginada
                try:
                    cs_real = P6.curva_real(e0, o2, alma.mundo, alma.mem, suelo, tcs, herm, alma._diario_hermano(tcs), pisos, pos_real, accion_real)
                    ver_r, ar_r = P6.juzga(fv.curva, cs_real, t, alma._margen_de(fv))
                    reg["real"] = {"veredicto": ver_r, "ventaja": round(ar_r, 6), "curva": [{"tic": c["tic"], "d": (round(c["d"], 5) if c["d"] is not None else None), "vida": round(c["vida"], 2), "pos": list(c["pos"])} for c in cs_real]}
                except Exception as ex_:
                    reg["real"] = {"veredicto": f"revienta: {type(ex_).__name__}", "error": repr(ex_)[:160]}
                # 3 · LA VERSION USABLE: contra el cuerpo decidiendo paso a paso
                reg["rollout"] = {}
                for cd in CADAS:
                    try:
                        cs_roll = P6.curva_de_rollout(SNAPS[cd], o2, alma.mundo, alma.mem, suelo, tcs, pisos, herm, alma._diario_hermano(tcs))
                        ver_o, ar_o = P6.juzga(fv.curva, cs_roll, t, alma._margen_de(fv))
                        reg["rollout"][str(cd)] = {"veredicto": ver_o, "ventaja": round(ar_o, 6), "curva": [{"tic": c["tic"], "d": (round(c["d"], 5) if c["d"] is not None else None), "vida": round(c["vida"], 2), "pos": list(c["pos"])} for c in cs_roll]}
                    except Exception as ex_:
                        reg["rollout"][str(cd)] = {"veredicto": f"revienta: {type(ex_).__name__}", "error": repr(ex_)[:160]}
                # 4 · EL HORIZONTE: ¿el fuego de mi casilla cae fuera de la ventana del plan?
                reg["fuego_fuera"] = (ta is None) or (ta > tcs[-1])
                dec["planes"].append(reg)
        decis.append(dec)
        return accion, radio
    alma.decidir = decidir

    _log0 = PC.log
    def _log(rec, _l=_log0):
        if rec.get("k") == "forma_evaluada":
            ULT_VER[rec.get("id")] = rec.get("veredicto")
        if not callado:
            _l(rec)
    PC.log = _log; PF.log = _log; PP.log = _log
    msgs = [json.dumps(cfg)] + [json.dumps(obs_de(r, sp, it)) for r in tics] + [json.dumps({"type": "final", "placement": (fin or {}).get("placement"), "kills": 0, "score": 0.0, "reason": (fin or {}).get("reason"), "match_ticks": tics[-1]["tick"]})]
    ws = WS(msgs)
    out_real = sys.stdout
    try:
        if callado:
            sys.stdout = open(os.devnull, "w")
        asyncio.run(PC.decisor(ws, alma))
    finally:
        sys.stdout = out_real
        PC.log = _log0; PF.log = _log0; PP.log = _log0
        PC._DIARIO.clear()
    msr = sorted(ms_roll)
    res = {"carp": carp, "slot": slot, "tics": len(tics), "muerte": muerte, "fin": (fin or {}).get("reason"), "placement": (fin or {}).get("placement"),
           "anillo": an, "speed": sp, "coste_paso": (orac.coste if orac else None), "fases": fases, "aviso_tics": {str(k): v for k, v in aviso_tics.items()},
           "repro": {"igual": repro["igual"], "difiere": repro["difiere"], "primeras": difs},
           "acciones": sum(1 for e in ws.enviados if e.get("type") == "action"),
           "umbrales": {"MARGENES": list(O.MARGENES), "R_CERCAS": list(O.R_CERCAS), "HORIZONTES": list(O.HORIZONTES), "margen_puerta": round(CVIVA.Confianza().margen(), 4), "C0": CVIVA.C0, "rollout_cadas": list(CADAS)},
           "puerta6": P6.VERSION,
           "n_decisiones": len(decis), "n_planes": n_plan[0],
           "ms_puerta": {"n": len([m for m in ms_p if m is not None]), "mediana": (sorted(m for m in ms_p if m is not None)[len(ms_p) // 2] if ms_p else None)},
           "ms_rollout": {"n": len(msr), "mediana": (msr[len(msr) // 2] if msr else None), "p95": (msr[int(len(msr) * 0.95)] if msr else None), "max": (msr[-1] if msr else None)},
           "segundos": round(time.time() - t_ini, 1), "decisiones": decis}
    if salida:
        json.dump(res, open(salida, "w"), ensure_ascii=False)
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tope = None; cada = 1
    if "--tope" in sys.argv:
        tope = int(sys.argv[sys.argv.index("--tope") + 1]); args = [a for a in args if a != str(tope)]
    if "--cada" in sys.argv:
        cada = int(sys.argv[sys.argv.index("--cada") + 1]); args = [a for a in args if a != str(cada)]
    carp, slot = args[0], int(args[1]); salida = args[2] if len(args) > 2 else None
    r = vida(carp, slot, salida, tope, callado=("--ruido" not in sys.argv), cada=cada)
    print(f"{carp} s{slot}: {r['tics']} tics · repro igual {r['repro']['igual']} difiere {r['repro']['difiere']} · decisiones {r['n_decisiones']} · planes {r['n_planes']} · "
          f"ms puerta {r['ms_puerta']['mediana']} · ms rollout mediana {r['ms_rollout']['mediana']} p95 {r['ms_rollout']['p95']} max {r['ms_rollout']['max']} · {r['segundos']} s")

"""[P6-14] EL BANCO DEL ORACULO: una vida de A4 repetida en seco por la via real,
con LA PUERTA REAL del cuerpo congelado juzgando los planes del oraculo.

    python banco_P6_14.py <carpeta> <slot> [salida.json] [--tope N]

INSTRUMENTO DE MEDIDA. No toca ni un byte del cuerpo congelado: importa sus
modulos y les llama. Como `humo_red_P6_11.py`: el alma REAL de la pareja
(`policy_pareja.AlmaPareja`, con `arreglos_P6_6` + `arreglos_P6_8b` +
`filas10_P6_10` + `amenaza11_P6_11` + `_envuelve`, en el orden de
`policy_pareja11.run`), alimentada por `policy_cortex.decisor` con un WS falso
que le sirve el `player_config` y las observaciones tal como estan en el
diario (con su `chat`: los partes E2 del hermano entran por el cable). La
empatia va cableada como fija `policy_cortex.py:93-96` (se comprueba).

LA PUERTA: `AlmaForma._acepta_o_no(fv, obs)` (policy_forma:716), que llama a
`_juzga` -> `forma_viva.evalua` -> `forma.curva_H` / `mejor_propia_H` /
`juzga_margen` con el margen de `confianza_viva` (C0 -> 0,062). Es la misma
funcion que `_decidir_forma` llamaria con GEMV_FORMA=1; aqui la llama el
instrumento desde fuera, en cada decision del oraculo, con la percepcion que
el cuerpo acaba de decidir (`alma.ultima_obs`, con los ojos inyectados, como
la recibe `_decidir_forma`). GEMV_FORMA queda en 0 como en la imagen jugada:
si valiera 1 el cuerpo OBEDECERIA a lo aceptado y la repeticion dejaria de
seguir el diario. `_compromiso` (:1624) queda tal cual: en la configuracion
congelada (GEMV_CURIOSIDAD_FORMA=0) no interviene.

Lo aceptado se anota y se RETIRA de `alma.vivas` al instante, para que el
estado del cuerpo siga siendo el del diario (con GEMV_FORMA=0 nadie lee
`vivas`, pero mejor no dejar nada).

Comprobacion de fidelidad: en cada tic se compara el `elegido` del replay con
el del diario (como `reproduce_P6_12.py`).
"""
from __future__ import annotations
import collections, glob, io, json, os, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    sys.path.insert(0, p)
SCRATCH = os.environ.get("P614_SCRATCH", os.path.join(AQUI, "_P6_14_tmp"))
os.makedirs(SCRATCH, exist_ok=True)
os.environ["MAPA_DIR"] = SCRATCH
# EL ENTORNO DE LA IMAGEN JUGADA (Dockerfile.pareja11), sin GEMV_FORMA=1 (ver arriba)
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

# EL CABLEADO (policy_cortex.py:93-96 lo fija en codigo al importar; se comprueba, no se supone)
assert A.EMPATIA_ON is True and (A.H_PREV, A.H_GOLPE) == (0.25, 1.0) and A.MIEDO_ON is False and A.VIDA_AJENA_ON is False, \
    ("cableado", A.EMPATIA_ON, A.H_PREV, A.H_GOLPE, A.MIEDO_ON, A.VIDA_AJENA_ON)
assert D.A is A, "el decisor no valora con la v42"
assert not PF.FORMA_ON and not PF.CUR_FORMA_ON and not PF.HILO_ON and not PF.CONSEJERO_ON

# LOS ARREGLOS DEL CUERPO DEL SEIS, una vez y en el orden de policy_pareja11.run
HECHO = {}
HECHO.update(R6.aplica(PP.AlmaPareja, PC.log)); HECHO.update(R8.aplica(PC.log)); HECHO.update(F10.aplica(PC.log)); HECHO.update(M11.aplica(PC.log))
assert HECHO.get("oido") and HECHO.get("don") and HECHO.get("pareja_parte") and HECHO.get("mochila_llena") and HECHO.get("filas10") and HECHO.get("manos"), HECHO
_ESTADO_MODULOS = (D.candidatos, D.decide, A.appraise, PC.PARTE.emite)   # antes de `_envuelve` (que cierra sobre el alma)


# ── captura de lo que la puerta mira, sin tocarla ──────────────────────────
CAP = {"on": False, "fotos": [], "comp": None}
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


def atribuye(fotos, tics, n_base, cs, t0):
    """Que filas pesan en contra del plan y cuanto (en area, las unidades del
    margen): area sin la fila menos area con la fila, sobre las fotos con
    piso que la puerta valoro. Devuelve (contra, puntos, comparador_idx)."""
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
    puntos = [{"tic": tics[i], "d_plan": round(_dcp0(*plan[i]), 5), "d_comp": round(_dcp0(*comp[i]), 5), "peso": round(W[i], 4)} for i in range(L)]
    return contra, puntos, ci


# ── el diario ──────────────────────────────────────────────────────────────
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
    """Solo posicion y vida por tic (para el hermano): el diario, de uno en uno."""
    T = {}
    for r in U.lee(f):
        if r.get("k") == "tick" and r.get("phase") == "live" and r.get("pos"):
            T[r["tick"]] = ((int(r["pos"][0]), int(r["pos"][1])), r.get("hp"))
    return T


def obs_de(r, sp, it):
    """La observacion tal como la sirve el mundo, desde el diario (banco_P6_11.obs_de
    + la correccion de hp 0 de reproduce_P6_12 + type/tick/phase/social)."""
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
    """El `player_config` que `Mundo.desde_player_config` sabe leer (serie_util.mundo_de)."""
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


# ── una vida ───────────────────────────────────────────────────────────────
def vida(carp, slot, salida=None, tope=None, callado=True):
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
    muerte = max(diario) if diario else None
    # anatomia P6-13 de esta vida (si murio por anillo)
    an = next((d for d in json.load(open(os.path.join(AQUI, "P6_13_anillo.json")))["muertes"] if d["carp"] == carp and d["slot"] == slot), None)

    # EL ALMA REAL, con los envoltorios en su orden
    D.candidatos, D.decide, A.appraise, PC.PARTE.emite = _ESTADO_MODULOS
    alma = PP.AlmaPareja()
    alma.artefacto_subido = True                  # ninguna subida desde un banco
    PP._envuelve(alma)
    orac = None; herm = None; propio = pc["slot"]
    decis = []; repro = collections.Counter(); difs = []; ms_p = []
    # primer tic con piernas listas desde cada aviso: el momento (2)
    fases = [tuple(z) for z in (pc.get("zone_schedule") or [])]
    aviso_tics = {}
    for i, f in enumerate(fases):
        for r in tics:
            if r["tick"] >= f[0] and int(r.get("move_ready_in_obs", r.get("move_ready_in")) or 0) == 0:
                aviso_tics[r["tick"]] = i; break
    n_plan = [0]
    _decidir0 = alma.decidir

    def decidir(obs, _d=_decidir0):
        accion, radio = _d(obs)
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
        o2 = alma.ultima_obs or obs                 # la percepcion que decidio (ojos dentro)
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
        dec = {"tick": t, "pos": list(pos), "hp": (o2.get("you") or {}).get("hp"), "arde": ar, "t_arde": ta, "pasos_a": pasos_a, "holgura": holg,
               "momentos": ([1] if m1 else []) + ([2] if m2 else []), "fase_aviso": aviso_tics.get(t), "fase_activa": orac.fase_activa(t),
               "radio": round(orac.radio_dps(t)[0], 2), "info": info, "hermano": (list(ph[0]) if ph else None),
               "cands_cuerpo": sorted((radio.get("candidatos") or {}).keys()), "elegido": el, "planes": []}
        escena = {"pos": list(pos), "suelo": [{"id": x.get("id"), "pos": list(x["pos"])} for x in ((o2.get("visible") or {}).get("items") or []) if x.get("pos")]}
        for p in planes:
            for H in O.HORIZONTES:
                n_plan[0] += 1
                texto = O.Oraculo.texto_forma(p["destino"], H, "salir del anillo: " + ",".join(p["criterios"]))
                cnt = collections.Counter(); formas, inf = TF.traduce(texto, escena, filas_mapa, cnt)
                reg = {"criterios": p["criterios"], "destino": list(p["destino"]), "propia": p["propia"], "pasos": p["pasos"], "cheb": p["cheb"], "llegada": p["llegada"],
                       "pasos_hermano": p.get("pasos_hermano"), "rivales_cerca": {str(k): v for k, v in p["rivales_cerca"].items()}, "H": H}
                if not formas:
                    reg["veredicto"] = "intraducible"; reg["traductor"] = dict(cnt); dec["planes"].append(reg); continue
                tramos = TF.solo_tramos(formas[0])
                fv = FV.FormaViva(f"O{n_plan[0]}", tramos, t, origen="consejero")
                CAP["on"] = True; CAP["fotos"] = []; CAP["comp"] = None
                try:
                    ok = alma._acepta_o_no(fv, o2)
                finally:
                    CAP["on"] = False
                fotos = CAP["fotos"]; comp = CAP["comp"]
                if fv in alma.vivas:
                    alma.vivas.remove(fv)
                alma.cerradas.clear()
                ms = alma.ms_forma[-1] if alma.ms_forma else None; ms_p.append(ms)
                cs, quien, n_base, _mv = comp if comp else (None, None, 0, None)
                ver = fv.estado
                # el veredicto tal cual lo da la regla (ok/area/vida/...) esta en el diario de PC.log; se reconstruye aqui igual que _acepta_o_no
                reg.update({"acepta": bool(ok), "ventaja": round(float(fv.ventaja or 0.0), 6), "margen": round(alma._margen_de(fv), 4),
                            "tics": list(fv.tics), "comparador": quien, "n_base": n_base, "ms": ms,
                            "curva": [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "pos": list(c.get("pos") or ())} for c in (fv.curva or [])],
                            "curva_comp": [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "pos": list(c.get("pos") or ())} for c in (cs or [])]})
                reg["veredicto"] = ULT_VER.get(fv.id, "?")
                contra, puntos, ci = atribuye(fotos, list(fv.tics), n_base, cs, t)
                reg["contra"] = contra; reg["puntos"] = puntos; reg["filas_alineadas"] = contra is not None
                dec["planes"].append(reg)
        decis.append(dec)
        return accion, radio
    alma.decidir = decidir

    # el veredicto literal ("ok"/"area"/"vida"/...) lo escribe la puerta en su diario (forma_evaluada): se lee de ahi
    ULT_VER = {}
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
    res = {"carp": carp, "slot": slot, "tics": len(tics), "muerte": muerte, "fin": (fin or {}).get("reason"), "placement": (fin or {}).get("placement"),
           "anillo": an, "speed": sp, "coste_paso": (orac.coste if orac else None), "fases": fases, "aviso_tics": {str(k): v for k, v in aviso_tics.items()},
           "repro": {"igual": repro["igual"], "difiere": repro["difiere"], "primeras": difs},
           "acciones": sum(1 for e in ws.enviados if e.get("type") == "action"),
           "umbrales": {"MARGENES": list(O.MARGENES), "R_CERCAS": list(O.R_CERCAS), "HORIZONTES": list(O.HORIZONTES), "margen_puerta": round(CVIVA.Confianza().margen(), 4), "C0": CVIVA.C0},
           "n_decisiones": len(decis), "n_planes": n_plan[0], "ms_puerta": {"n": len([m for m in ms_p if m is not None]), "mediana": (sorted(m for m in ms_p if m is not None)[len(ms_p) // 2] if ms_p else None)},
           "segundos": round(time.time() - t_ini, 1), "decisiones": decis}
    if salida:
        json.dump(res, open(salida, "w"), ensure_ascii=False)
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tope = None
    if "--tope" in sys.argv:
        tope = int(sys.argv[sys.argv.index("--tope") + 1]); args = [a for a in args if a != str(tope)]
    carp, slot = args[0], int(args[1]); salida = args[2] if len(args) > 2 else None
    r = vida(carp, slot, salida, tope, callado=("--ruido" not in sys.argv))
    print(f"{carp} s{slot}: {r['tics']} tics · repro igual {r['repro']['igual']} difiere {r['repro']['difiere']} {r['repro']['primeras'][:2]} · "
          f"decisiones {r['n_decisiones']} · planes {r['n_planes']} · ms puerta mediana {r['ms_puerta']['mediana']} · {r['segundos']} s")

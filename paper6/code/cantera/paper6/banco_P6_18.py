"""[P6-18 · A.1/A.2] EL BANCO DE «IR Y QUEDARSE»: en cada momento de salida (los 63
de A5h y los 22 de A4, `P6_18_momentos.json`), repetida la vida en seco por la
via real (arnes de `banco_P6_15`), se juzga el plan de QUEDARSE con:
  · la puerta del cinco (comparador `mejor_propia_H`);
  · la puerta6 (comparador B, el cuerpo decidiendo paso a paso), enchufada
    envolviendo `forma.mejor_propia_H` solo durante ese juicio;
  · la trayectoria real imaginada (comparador A de puerta6): «lo que eligio».

EL PLAN «IR Y QUEDARSE», en el idioma de formas: `ir` a la casilla a salvo mas
cercana (la propia si ya lo esta: 0 pasos) y `esperar` hasta el final de la
fase (H_fase = tic del siguiente aviso - t, acotado a [25, 400]); y tambien con
H = 100 para comparar con P6-14/15. DECLARADO: en los momentos de salida el
cuerpo esta dentro, asi que el destino es la PROPIA CASILLA. La puerta del
cinco no puede juzgar ese plan (el mejor candidato propio proyectado incluye
`noop`, cuya curva es la misma: area 0); la puerta6 SI, porque su comparador
no es un candidato sino el cuerpo decidiendo, que sale. Se comprueba aqui.

    python banco_P6_18.py <carpeta> <slot> <salida.json>
"""
import collections, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import banco_P6_15 as B
from banco_P6_15 import PC, PF, D, A, FV, CVIVA, F, TF, PP, P2, O, P6, CAP, _dcp0
import compromiso6_P6_16 as C6
import asyncio


class _FVnula:
    W_nace = None

MOM = json.load(open(os.path.join(AQUI, "P6_18_momentos.json")))
ESTADO = {"blo": None, "roll_ms": []}
_MPH0 = F.mejor_propia_H


def _mph6(estado0, obs_w, base, tics, mundo, mem, suelo, t0, herm_slot, diario_h, pisos, vida_min=F.VIDA_MIN):
    if not tics:
        return None, None, 0, None
    t_a = time.perf_counter()
    snaps, n_dec = P6.rollout(obs_w, estado0, int(tics[-1]) + 1, mundo, mem, ESTADO["blo"] or D.Bloqueos(), suelo)
    c = P6.curva_de_rollout(snaps, obs_w, mundo, mem, suelo, tics, pisos, herm_slot, diario_h)
    ESTADO["roll_ms"].append(round((time.perf_counter() - t_a) * 1000.0, 1))
    ESTADO["snaps"] = snaps
    if CAP["on"]:
        CAP["comp"] = (c, "rollout", len(base), True)
    return c, "rollout", len(base), True


def contra_de(fotos, tics, cs, t0, n_base):
    contra, _p, ci = B.atribuye(fotos, list(tics), n_base, cs, t0)
    return contra


def vida(carp, slot, salida):
    momentos = [m for m in MOM if m["carp"] == carp and m["slot"] == slot]
    ticks_m = {m["tick"]: m for m in momentos}
    t_ini = time.time()
    fs = {int(__import__("re").search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in __import__("glob").glob(os.path.join(B.RAIZ, "paintball", "runs", carp, "*policy_agent_1*.art.log"))}
    T_h = B.ligero(fs[21 - slot])
    pc, sm, cat, tics, sp, it, fin = B.carga(fs[slot])
    cfg = B.config_de(pc, sm, cat); filas_mapa = list(sm["filas"])
    diario = {r["tick"]: str((r.get("RADIOGRAFIA") or {}).get("elegido") or "") for r in tics}
    T_real = {r["tick"]: ((int(r["pos"][0]), int(r["pos"][1])), r.get("hp"), diario[r["tick"]]) for r in tics if r.get("pos")}
    tics_real = sorted(T_real); muerte = max(diario) if diario else None
    import bisect
    def real_en(t):
        if t in T_real:
            return T_real[t]
        i = bisect.bisect_right(tics_real, t) - 1
        return T_real[tics_real[max(0, i)]]
    def pos_real(t):
        return real_en(t)[0]
    def accion_real(t):
        el = T_real.get(t, (None, None, ""))[2] or ""
        return el if el.startswith("usar_") else ("coger" if el.startswith("coger") else None)
    fases = [tuple(z) for z in (pc.get("zone_schedule") or [])]
    D.candidatos, D.decide, A.appraise, PC.PARTE.emite = B._ESTADO_MODULOS
    alma = PP.AlmaPareja(); alma.artefacto_subido = True
    PP._envuelve(alma)
    orac = None; herm = None; propio = pc["slot"]; res_m = []; repro = collections.Counter()
    ULT_VER = {}
    VENT = {m["tick"]: {"fin": None, "tics": 0, "rupturas": collections.Counter(), "primera_a": None} for m in momentos}
    _decidir0 = alma.decidir

    def juzga(fv, o2, modo):
        """modo: 'cinco' | 'puerta6'. Devuelve (veredicto, ventaja, comparador, contra, curva, curva_comp)."""
        CAP["on"] = True; CAP["fotos"] = []; CAP["comp"] = None; CAP["base"] = None
        if modo == "puerta6":
            F.mejor_propia_H = _mph6
        try:
            alma._acepta_o_no(fv, o2)
        finally:
            CAP["on"] = False
            F.mejor_propia_H = B._mph if modo == "puerta6" else F.mejor_propia_H
        fotos = CAP["fotos"]; comp = CAP["comp"]
        if fv in alma.vivas:
            alma.vivas.remove(fv)
        alma.cerradas.clear()
        cs, quien, n_base, _mv = comp if comp else (None, None, 0, None)
        contra = contra_de(fotos, fv.tics, cs, alma.tick, (1 if modo == "puerta6" else n_base))
        curva = [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "pos": list(c.get("pos") or ())} for c in (fv.curva or [])]
        curva_c = [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "pos": list(c.get("pos") or ())} for c in (cs or [])]
        return ULT_VER.get(fv.id, "?"), round(float(fv.ventaja or 0.0), 6), quien, contra, curva, curva_c

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
            repro["igual" if el == diario[t] else "difiere"] += 1
        # las rupturas de compromiso6 en la ventana de quedarse de cada momento (con la percepcion real, ojos dentro)
        o2 = alma.ultima_obs or obs
        for tm, v in VENT.items():
            if v["fin"] is not None and tm <= t <= v["fin"]:
                v["tics"] += 1
                try:
                    causa, _det = C6.rupturas6(alma, o2, _FVnula())
                except Exception as ex:
                    causa = "error " + type(ex).__name__
                if causa:
                    v["rupturas"][causa[:2]] += 1
                    if causa.startswith("a)") and v["primera_a"] is None:
                        v["primera_a"] = t - tm
        if t not in ticks_m:
            return accion, radio
        m = ticks_m[t]
        pos = tuple(int(x) for x in (o2.get("you") or {}).get("pos"))
        i = orac.fase_activa(t); fin_fase = (orac.fases[i + 1][0] if (i is not None and i + 1 < len(orac.fases)) else t + 400)
        H_fase = max(25, min(400, fin_fase - t))
        VENT[t]["fin"] = fin_fase
        salvo = orac.a_salvo(pos, t)
        dest = pos
        if not salvo:
            Dm = orac.bfs(pos); seg = orac.seguras(pos, t, Dm)
            if seg:
                dest = min(seg, key=lambda qk: (qk[1], qk[0]))[0]
        e0, suelo, pisos = alma._contexto(o2)
        ESTADO["blo"] = alma.bloqueos
        rec = {"brazo": m["brazo"], "carp": carp, "slot": slot, "tick": t, "pos": list(pos), "hp": (o2.get("you") or {}).get("hp"), "elegido_real": diario.get(t), "elegido_replay": el,
               "a_salvo": salvo, "destino": list(dest), "propia": dest == pos, "fase": (i + 1 if i is not None else None), "fin_fase": fin_fase, "H_fase": H_fase,
               "s8_ahora": None, "planes": {}}
        escena = {"pos": list(pos), "suelo": [{"id": x.get("id"), "pos": list(x["pos"])} for x in ((o2.get("visible") or {}).get("items") or []) if x.get("pos")]}
        for nombre, H in (("H_fase", H_fase), ("H100", 100)):
            # el plan de quedarse: `ir` (0 pasos si es la propia casilla) y esperar hasta el final de la fase
            # EN VARIOS TRAMOS (50, 50, resto; 4 tramos, el maximo del idioma): con un solo tramo de 400 tics
            # el punto de control queda a peso 0,5^(400/50) = 1/256 y la puerta no ve nada (declarado).
            esperas = ([50, 50, max(25, H - 100)] if H > 125 else [H])
            texto = json.dumps({"formas": [{"tramos": [{"destino": [int(dest[0]), int(dest[1])], "intencion": "ir", "vida": "+", "manos": "0", "vinculo": "0", "por": "quedarse dentro hasta el final de la fase"}] + [
                {"destino": None, "intencion": "esperar", "esperar": int(e), "vida": "+", "manos": "0", "vinculo": "0", "por": "seguir dentro"} for e in esperas], "final": "dentro del circulo"}]})
            formas, inf = TF.traduce(texto, escena, filas_mapa)
            if not formas:
                rec["planes"][nombre] = {"veredicto": "intraducible"}; continue
            tramos = TF.solo_tramos(formas[0])
            p = {"H": H, "tramos": [{"destino": (list(x["destino"]) if x.get("destino") else None), "intencion": x["intencion"], "esperar": x.get("esperar")} for x in tramos]}
            for modo in ("cinco", "puerta6"):
                fv = FV.FormaViva(f"Q{t}{nombre}{modo}", tramos, t, origen="consejero")
                ver, vent, quien, contra, curva, curva_c = juzga(fv, o2, modo)
                p[modo] = {"veredicto": ver, "ventaja": vent, "comparador": quien, "contra": contra, "curva": curva, "curva_comp": curva_c, "margen": round(alma._margen_de(fv), 4)}
                if modo == "puerta6":
                    p[modo]["rollout_ms"] = ESTADO["roll_ms"][-1] if ESTADO["roll_ms"] else None
                    sn = ESTADO.get("snaps") or {}
                    p[modo]["rollout_camino"] = [[x, list(sn[x]["pos"]), round(sn[x]["hp"], 1)] for x in sorted(sn) if (x - t) % 11 == 0][:40]
                    # la curva del plan (la misma) contra la trayectoria REAL imaginada (comparador A)
                    try:
                        cs_real = P6.curva_real(e0, o2, alma.mundo, alma.mem, suelo, list(fv.tics), herm, alma._diario_hermano(list(fv.tics)), pisos, pos_real, accion_real)
                        ver_r, ar_r = P6.juzga(fv.curva, cs_real, t, alma._margen_de(fv))
                        p["real"] = {"veredicto": ver_r, "ventaja": round(ar_r, 6), "curva_comp": [{"tic": c["tic"], "d": (round(c["d"], 5) if c["d"] is not None else None), "vida": round(c["vida"], 2), "pos": list(c["pos"])} for c in cs_real]}
                    except Exception as ex:
                        p["real"] = {"veredicto": f"revienta: {type(ex).__name__}", "error": repr(ex)[:160]}
            rec["planes"][nombre] = p
        res_m.append(rec)
        return accion, radio
    alma.decidir = decidir
    _log0 = PC.log
    def _log(rec, _l=_log0):
        if rec.get("k") == "forma_evaluada":
            ULT_VER[rec.get("id")] = rec.get("veredicto")
    PC.log = _log; PF.log = _log; PP.log = _log
    msgs = [json.dumps(cfg)] + [json.dumps(B.obs_de(r, sp, it)) for r in tics] + [json.dumps({"type": "final", "placement": (fin or {}).get("placement"), "kills": 0, "score": 0.0, "reason": (fin or {}).get("reason"), "match_ticks": tics[-1]["tick"]})]
    ws = B.WS(msgs); out_real = sys.stdout
    try:
        sys.stdout = open(os.devnull, "w")
        asyncio.run(PC.decisor(ws, alma))
    finally:
        sys.stdout = out_real
        PC.log = _log0; PF.log = _log0; PP.log = _log0; PC._DIARIO.clear()
        F.mejor_propia_H = B._mph
    for r in res_m:
        v = VENT.get(r["tick"]) or {}
        r["ventana_quedarse"] = {"tics": v.get("tics"), "rupturas": dict(v.get("rupturas") or {}), "primera_a_en": v.get("primera_a")}
    res = {"carp": carp, "slot": slot, "tics": len(tics), "muerte": muerte, "repro": dict(repro), "momentos": res_m, "n_momentos_pedidos": len(momentos), "segundos": round(time.time() - t_ini, 1),
           "rollout_ms_mediana": (sorted(ESTADO["roll_ms"])[len(ESTADO["roll_ms"]) // 2] if ESTADO["roll_ms"] else None)}
    json.dump(res, open(salida, "w"), ensure_ascii=False)
    return res


if __name__ == "__main__":
    carp, slot, salida = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    r = vida(carp, slot, salida)
    print(f"{carp} s{slot}: {r['tics']} tics · repro {r['repro']} · momentos {len(r['momentos'])}/{r['n_momentos_pedidos']} · rollout ms {r['rollout_ms_mediana']} · {r['segundos']} s")

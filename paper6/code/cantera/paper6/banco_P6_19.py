"""[P6-19 · 2 y 3] EL BANCO DE PUERTA6g. Una vida repetida en seco por la via real
(arnes de `banco_P6_15`), en uno de tres modos:
  fidelidad  (A4): en cada decision del oraculo (disparo de P6-15), el rollout de
             puerta6 y el de puerta6g desde el mismo estado: vida prevista a +50,
             +100 y +200 contra la vida real del diario.
  momentos   (A5h/A4, los 85 de P6-18): el plan de quedarse (4 tramos, H fase)
             juzgado con puerta6 y con puerta6g; la vida que promete cada curva
             en sus puntos de control contra la real.
  a6         (A6): cada plan que el oraculo propuso en el campo (`oraculo16
             propone`, con su texto) juzgado con puerta6 y con puerta6g; y para
             cada forma que cayo por «vida real X por debajo de la proyectada
             Y - 10», si con la curva g habria caido.
    python banco_P6_19.py <modo> <carpeta> <slot> <salida.json>
INSTRUMENTO DE MEDIDA; puerta6g es version nueva declarada (`puerta6g_P6_19`).
"""
import bisect, collections, glob, json, os, re, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import banco_P6_15 as B
from banco_P6_15 import PC, PF, D, A, FV, CVIVA, F, TF, PP, P2, O, P6, CAP, _dcp0
import puerta6g_P6_19 as G
import asyncio
MOM = json.load(open(os.path.join(AQUI, "P6_18_momentos.json")))
ESTADO = {"blo": None}


def _mph6(estado0, obs_w, base, tics, mundo, mem, suelo, t0, herm_slot, diario_h, pisos, vida_min=F.VIDA_MIN):
    if not tics:
        return None, None, 0, None
    snaps, n = P6.rollout(obs_w, estado0, int(tics[-1]) + 1, mundo, mem, ESTADO["blo"] or D.Bloqueos(), suelo)
    c = P6.curva_de_rollout(snaps, obs_w, mundo, mem, suelo, tics, pisos, herm_slot, diario_h)
    if CAP["on"]:
        CAP["comp"] = (c, "rollout", len(base), True)
    return c, "rollout", len(base), True


def _mph_g_cap(*a, **k):
    r = G._mph_g(*a, **k)
    if CAP["on"]:
        CAP["comp"] = r
    return r


def texto_quedarse(dest, H):
    esperas = ([50, 50, max(25, int(H) - 100)] if H > 125 else [max(25, int(H))])
    return json.dumps({"formas": [{"tramos": [{"destino": [int(dest[0]), int(dest[1])], "intencion": "ir", "vida": "+", "manos": "0", "vinculo": "0", "por": "quedarse"}]
                                  + [{"destino": None, "intencion": "esperar", "esperar": int(e), "vida": "+", "manos": "0", "vinculo": "0", "por": "seguir dentro"} for e in esperas], "final": "dentro"}]})


def vida(modo, carp, slot, salida):
    t_ini = time.time()
    fs = {int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1)): f for f in glob.glob(os.path.join(B.RAIZ, "paintball", "runs", carp, "*policy_agent_1*.art.log"))}
    T_h = B.ligero(fs[21 - slot])
    pc, sm, cat, tics, sp, it, fin = B.carga(fs[slot])
    cfg = B.config_de(pc, sm, cat); filas_mapa = list(sm["filas"])
    diario = {r["tick"]: str((r.get("RADIOGRAFIA") or {}).get("elegido") or "") for r in tics}
    T_real = {r["tick"]: ((int(r["pos"][0]), int(r["pos"][1])), float(r.get("hp") if r.get("hp") is not None else 100)) for r in tics if r.get("pos")}
    tics_real = sorted(T_real); muerte = max(diario) if diario else None
    def real_en(t):
        if t in T_real:
            return T_real[t]
        i = bisect.bisect_right(tics_real, t) - 1
        return T_real[tics_real[max(0, i)]]
    def hp_real(t):
        return 0.0 if (t > muerte and fin and fin.get("reason") == "eliminated") else real_en(t)[1]
    # lo que hay que juzgar en esta vida
    momentos = {m["tick"]: m for m in MOM if m["carp"] == carp and m["slot"] == slot} if modo == "momentos" else {}
    propuestas = {}; caidas = []
    if modo == "a6":
        import serie_util as U
        formas_ac = {}
        for r in U.lee(fs[slot]):
            k = r.get("k")
            if k == "oraculo16" and r.get("estado") == "propone":
                propuestas[r["tick"]] = r
            elif k == "forma_aceptada":
                formas_ac[r.get("id")] = r
            elif k == "forma_caida" and "vida real" in str(r.get("motivo")):
                m = re.search(r"la vida real ([\d.]+) esta por debajo de la proyectada ([\d.]+)", str(r.get("motivo")))
                caidas.append({"id": r.get("id"), "tick": r["tick"], "hp_real": float(m.group(1)) if m else None, "proyectada": float(m.group(2)) if m else None, "nace": (formas_ac.get(r.get("id")) or {}).get("nace")})
    D.candidatos, D.decide, A.appraise, PC.PARTE.emite = B._ESTADO_MODULOS
    alma = PP.AlmaPareja(); alma.artefacto_subido = True
    PP._envuelve(alma)
    orac = None; herm = None; res = []; repro = collections.Counter(); ULT_VER = {}
    _decidir0 = alma.decidir

    def juzga(fv, o2, modo_p):
        """modo_p: 'puerta6' | 'puerta6g'. Devuelve dict con veredicto, ventaja, curva del plan, comparador, contra."""
        CAP["on"] = True; CAP["fotos"] = []; CAP["comp"] = None; CAP["base"] = None
        if modo_p == "puerta6":
            G.quita(); F.mejor_propia_H = _mph6
        else:
            G.MODO["v"] = "contexto" if modo_p.endswith("ctx") else "arma_dist"
            G.instala(con_curva=True, con_comparador=True); F.mejor_propia_H = _mph_g_cap
        try:
            alma._acepta_o_no(fv, o2)
        finally:
            CAP["on"] = False
            G.quita(); F.mejor_propia_H = B._mph; G.MODO["v"] = "arma_dist"
        fotos = CAP["fotos"]; comp = CAP["comp"]
        if fv in alma.vivas:
            alma.vivas.remove(fv)
        alma.cerradas.clear()
        cs, quien, n_base, _mv = comp if comp else (None, None, 0, None)
        contra, _p, _ci = B.atribuye(fotos, list(fv.tics), 1, cs, alma.tick)
        cv = [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "vida_real": round(hp_real(c["tic"]), 1)} for c in (fv.curva or [])]
        cc = [{"tic": c["tic"], "d": (round(c["d"], 5) if c.get("d") is not None else None), "vida": (round(c["vida"], 2) if c.get("vida") is not None else None), "pos": list(c.get("pos") or ())} for c in (cs or [])]
        return {"veredicto": ULT_VER.get(fv.id, "?"), "ventaja": round(float(fv.ventaja or 0.0), 6), "comparador": quien, "contra": (contra or [])[:8], "curva": cv, "curva_comp": cc, "tics": list(fv.tics)}

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
        o2 = alma.ultima_obs or obs
        pos = tuple(int(x) for x in (o2.get("you") or {}).get("pos"))
        ESTADO["blo"] = alma.bloqueos; G.ESTADO["blo"] = alma.bloqueos
        if modo == "fidelidad":
            if int((obs.get("you") or {}).get("move_ready_in") or 0) != 0:
                return accion, radio
            Dm = orac.bfs(pos); seg = orac.seguras(pos, t, Dm)
            ar, ta, pasos_a, holg = orac.dispara(pos, t, Dm, seg)
            m1 = ar or (holg is not None and holg <= max(O.MARGENES))
            if not m1:
                return accion, radio
            e0, suelo, pisos = alma._contexto(o2)
            rec = {"tick": t, "pos": list(pos), "hp": hp_real(t), "arde": ar, "holgura": holg, "n_rivales": len(orac.rivales_de(o2, herm, pc["slot"])), "dano_esperado_ahora": round(G.dano_esperado(pos, o2, alma.mundo), 4)}
            # el dano REAL de la ventana, por fuente (anillo / rivales), del diario
            for k in (50, 100, 200):
                z = rv = 0.0
                for r_ in tics:
                    if t < r_["tick"] <= t + k:
                        for g in (r_.get("damage_taken") or []):
                            if isinstance(g, dict):
                                if g.get("source") == "zone":
                                    z += float(g.get("amount") or 0)
                                elif str(g.get("source")).startswith("P"):
                                    rv += float(g.get("amount") or 0)
                rec[f"dano_real_anillo_{k}"] = round(z, 1); rec[f"dano_real_rival_{k}"] = round(rv, 1)
            for nombre, fn in (("puerta6", P6.rollout), ("puerta6g", G.rollout_g), ("puerta6g_ctx", G.rollout_g)):
                G.MODO["v"] = "contexto" if nombre.endswith("ctx") else "arma_dist"
                t_a = time.perf_counter()
                snaps, n = fn(o2, e0, t + 201, alma.mundo, alma.mem, alma.bloqueos, suelo)
                rec[nombre] = {"ms": round((time.perf_counter() - t_a) * 1000.0, 1)}
                for k in (50, 100, 200):
                    s = snaps.get(t + k)
                    if s is not None:
                        rec[nombre][f"vida_{k}"] = round(s["hp"], 2); rec[nombre][f"real_{k}"] = round(hp_real(t + k), 1); rec[nombre][f"error_{k}"] = round(s["hp"] - hp_real(t + k), 2)
                        rec[nombre][f"dist_{k}"] = max(abs(s["pos"][0] - real_en(t + k)[0][0]), abs(s["pos"][1] - real_en(t + k)[0][1]))
            G.MODO["v"] = "arma_dist"
            res.append(rec)
        elif modo == "momentos" and t in momentos:
            m = momentos[t]
            i = orac.fase_activa(t); fin_fase = (orac.fases[i + 1][0] if (i is not None and i + 1 < len(orac.fases)) else t + 400)
            H = max(25, min(400, fin_fase - t)); salvo = orac.a_salvo(pos, t); dest = pos
            if not salvo:
                Dm = orac.bfs(pos); seg = orac.seguras(pos, t, Dm)
                if seg:
                    dest = min(seg, key=lambda qk: (qk[1], qk[0]))[0]
            escena = {"pos": list(pos), "suelo": [{"id": x.get("id"), "pos": list(x["pos"])} for x in ((o2.get("visible") or {}).get("items") or []) if x.get("pos")]}
            formas, inf = TF.traduce(texto_quedarse(dest, H), escena, filas_mapa)
            rec = {"brazo": m["brazo"], "tick": t, "pos": list(pos), "hp": hp_real(t), "destino": list(dest), "H": H, "dano_esperado_ahora": round(G.dano_esperado(pos, o2, alma.mundo), 4), "n_rivales": len(orac.rivales_de(o2, herm, pc["slot"]))}
            if formas:
                tramos = TF.solo_tramos(formas[0])
                for modo_p in ("puerta6", "puerta6g", "puerta6g_ctx"):
                    fv = FV.FormaViva(f"M{t}{modo_p}", tramos, t, origen="consejero")
                    rec[modo_p] = juzga(fv, o2, modo_p)
            res.append(rec)
        elif modo == "a6" and t in propuestas:
            pr = propuestas[t]
            escena = {"pos": list(pos), "suelo": [{"id": x.get("id"), "pos": list(x["pos"])} for x in ((o2.get("visible") or {}).get("items") or []) if x.get("pos")]}
            formas, inf = TF.traduce(pr["texto"], escena, filas_mapa)
            rec = {"tick": t, "pos": list(pos), "hp": hp_real(t), "destino": pr.get("destino"), "H": pr.get("H"), "dano_esperado_ahora": round(G.dano_esperado(pos, o2, alma.mundo), 4), "n_rivales": len(orac.rivales_de(o2, herm, pc["slot"]))}
            if formas:
                tramos = TF.solo_tramos(formas[0])
                for modo_p in ("puerta6", "puerta6g", "puerta6g_ctx"):
                    fv = FV.FormaViva(f"A{t}{modo_p}", tramos, t, origen="consejero")
                    rec[modo_p] = juzga(fv, o2, modo_p)
            res.append(rec)
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
        PC.log = _log0; PF.log = _log0; PP.log = _log0; PC._DIARIO.clear(); G.quita(); F.mejor_propia_H = B._mph
    # las caidas de A6: ¿habrian caido con la curva g?
    if modo == "a6":
        por_nace = {r["tick"]: r for r in res}
        for c in caidas:
            r = por_nace.get(c["nace"])
            c["hp_real_diario"] = hp_real(c["tick"])
            if r and r.get("puerta6g") and r.get("puerta6") and r.get("puerta6g_ctx"):
                # el punto de control anterior al tic de la caida, en cada curva
                def vida_prev(curva):
                    prev = [x for x in curva if x["tic"] <= c["tick"]]
                    return (prev[-1]["vida"] if prev else (curva[0]["vida"] if curva else None))
                vg = vida_prev(r["puerta6g"]["curva"]); v6 = vida_prev(r["puerta6"]["curva"]); vc = vida_prev(r["puerta6g_ctx"]["curva"])
                c["proyectada_g"] = vg; c["proyectada_6"] = v6; c["proyectada_ctx"] = vc
                c["caeria_con_g"] = (vg is not None and c["hp_real"] is not None and c["hp_real"] < vg - 10.0)
                c["caeria_con_ctx"] = (vc is not None and c["hp_real"] is not None and c["hp_real"] < vc - 10.0)
                c["veredicto_ctx"] = r["puerta6g_ctx"]["veredicto"]
                c["veredicto_g"] = r["puerta6g"]["veredicto"]; c["veredicto_6"] = r["puerta6"]["veredicto"]
    out = {"modo": modo, "carp": carp, "slot": slot, "tics": len(tics), "muerte": muerte, "repro": dict(repro), "registros": res, "caidas": caidas, "segundos": round(time.time() - t_ini, 1)}
    json.dump(out, open(salida, "w"), ensure_ascii=False)
    return out


if __name__ == "__main__":
    modo, carp, slot, salida = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    r = vida(modo, carp, slot, salida)
    print(f"{modo} {carp} s{slot}: {r['tics']} tics · repro {r['repro']} · registros {len(r['registros'])} · caidas {len(r['caidas'])} · {r['segundos']} s")

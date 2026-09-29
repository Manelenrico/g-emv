"""[P5-3G · G5 y G6] Lo que la forma RECUPERA, y contra que gana el azar."""
from __future__ import annotations
import collections, copy, glob, json, os, random, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B, banco_forma3 as BF, forma as F, proyeccion as P
import alcance_g as AL

HOR, MARGEN = 100, 0.02
RIV = set(AL.FILAS_RIVAL)
HER = set(AL.FILAS_HERMANO)
PROG = open(os.path.join(AQUI, "P53G_G5G6_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


def grupo(n):
    return "rivales" if n in RIV else ("hermano" if n in HER else "propias")


def trozos(fa, fb):
    da = F.d_con_pisos(fa)
    out = {}
    for nom in V42.REPARTO:
        if abs(float(fa.get(nom) or 0.0) - float(fb.get(nom) or 0.0)) < 1e-12:
            continue
        mix = dict(fa)
        mix[nom] = fb.get(nom)
        out[nom] = da - F.d_con_pisos(mix)
    return out


def main():
    D.A = V42
    U.pon(False)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
    rnd_az = random.Random(20260919)
    proy = collections.Counter()
    n_fut = 0
    gana_az = collections.Counter()
    punto_az = collections.Counter()
    n_az = 0
    for orden, i in enumerate(idx, 1):
        f = fs[i]
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            continue
        B.pon_v42(B.interruptores(recs))
        filas_m, items = list(sm["filas"]), cat["items"]
        mundo = U.mundo_de(pc, filas_m, items)
        slot, herm = pc.get("slot"), pc.get("teammate_slot")
        otro = f.replace(f"policy_agent_{slot}", f"policy_agent_{herm}")
        dia_h = ({rr["tick"]: rr for rr in U.lee(otro)
                  if rr.get("k") == "tick" and rr.get("phase") == "live"}
                 if os.path.exists(otro) else None)
        tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
        vivos = [r for r in recs if r.get("k") == "tick"
                 and r.get("phase") == "live"]
        vivo = {r["tick"] for r in vivos}
        pos_t = {r["tick"]: tuple(r.get("pos") or ()) for r in vivos}
        mri = {r["tick"]: (r.get("move_ready_in") or 0) for r in vivos}
        d_t = {}
        for r in vivos:
            R = r.get("RADIOGRAFIA") or {}
            c = (R.get("candidatos") or {}).get(R.get("elegido"))
            d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
        esc = [r["tick"] for r in vivos if r["tick"] >= 300 and r["tick"] % 50 == 0
               and (r["tick"] + HOR) in vivo and d_t.get(r["tick"]) is not None
               and d_t.get(r["tick"] + HOR) is not None
               and d_t[r["tick"] + HOR] < d_t[r["tick"]]]
        nec = set(esc) | {u for t in esc for u in range(t, t + HOR + 1)
                          if u in vivo and mri.get(u, 1) == 0}
        ctxs = {}
        mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
        for r in [x for x in recs if x.get("k") == "tick"]:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            pre = copy.deepcopy(mem)
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if (r.get("intencion") or {}).get("do") == "attack" or _el.startswith("atacar"):
                mem.ultimo_ataque = t
            if t in nec:
                ctxs[t] = (r, o, pre, copy.deepcopy(blo))
        for t in esc:
            w = next((u for u in range(t, t + HOR + 1)
                      if u in vivo and mri.get(u, 1) == 0), None)
            if w is None or w not in ctxs:
                continue
            rw, ow, memw, blw = ctxs[w]
            ew = P.estado_de(rw)
            suelow = {tuple(it["pos"]): it for it in (rw.get("ve_items") or [])
                      if it.get("pos")}
            tr_d = BF.tramos_reales(tk, t, HOR)
            pcs = F.puntos_de_control(ew, tr_d)
            tics = [x[0] for x in pcs]
            if not tics:
                continue
            # --- G5: la mejora que la forma PROYECTA, por grupo
            cache = {}
            o0 = F.foto_rapida(ow, ew, mundo, w, list(suelow.values()))
            o0, _ = AL.obs_con_alcance(o0, mundo, filas_m, tuple(ew["pos"]), 0,
                                       herm, cache)
            o0, m0 = AL.pon_hermano(o0, memw, herm, (dia_h or {}).get(w),
                                    tuple(ew["pos"]), mundo)
            fa = V42.filas(o0, mundo, m0, w) or {}
            cf = F.curva_G(ew, ow, tr_d, mundo, memw, suelow, tics, filas_m,
                           herm, dia_h, True)
            # las filas del ULTIMO punto de control
            e = F.copia_estado(ew)
            suelo_act = dict(suelow)
            cache2 = {}
            for j, tic in enumerate(tics):
                trr = tr_d[j] if j < len(tr_d) else {"destino": None,
                                                     "intencion": "esperar"}
                e = P.proyectar_rapido(e, {"destino": trr.get("destino"),
                                           "coger": trr.get("intencion") == "coger",
                                           "usar": None},
                                       tic - e["tick"], mundo, suelo_act)
            oz = F.foto_rapida(ow, e, mundo, tics[-1], list(suelo_act.values()))
            oz, _ = AL.obs_con_alcance(oz, mundo, filas_m, tuple(e["pos"]),
                                       tics[-1] - w, herm, cache2)
            oz, mz = AL.pon_hermano(oz, memw, herm, (dia_h or {}).get(tics[-1]),
                                    tuple(e["pos"]), mundo)
            fb = V42.filas(oz, mundo, mz, tics[-1]) or {}
            if F.d_con_pisos(fa) - F.d_con_pisos(fb) > 0:
                n_fut += 1
                for nom, v in trozos(fa, fb).items():
                    proy[grupo(nom)] += v
                    proy["fila:" + nom] += v
            # --- G6: el azar con G1+G2 y margen 0,02
            pasos = F.cheb(pos_t[t], tr_d[-1]["destino"])
            z = BF.casilla_a(filas_m, pos_t[t], max(1, pasos), rnd_az)
            if not z:
                continue
            tr_z = [{"destino": tuple(z), "intencion": "ir"},
                    {"destino": None, "intencion": "esperar",
                     "esperar": max(0, HOR - F.cheb(pos_t[t], z) * P.PASO_TICS)}]
            tz = [x[0] for x in F.puntos_de_control(ew, tr_z)]
            cz = F.curva_G(ew, ow, tr_z, mundo, memw, suelow, tz, filas_m,
                           herm, dia_h, True)
            base = list(D.candidatos(ow, mundo, copy.deepcopy(memw), w,
                                     copy.deepcopy(blw)))
            cs, quien, ncd, mv = F.mejor_propia_G(ew, ow, base, tz, mundo,
                                                  memw, suelow, w, filas_m,
                                                  herm, dia_h, True)
            if cs is None:
                continue
            ver, ar, dt = F.juzga_margen(cz, cs, w, margen=MARGEN)
            if ver != "ok":
                continue
            n_az += 1
            pts = dt.get("puntos") or []
            if pts:
                j = pts.index(max(pts, key=lambda x: x["gana"]))
                punto_az[f"punto {j+1} de {len(pts)}"] += 1
                # filas en ese punto
                def filas_en(cur, k_):
                    ee = cur[k_]
                    oo = F.foto_rapida(ow, {"tick": ee["tic"], "pos": ee["pos"],
                                            "hp": ee["vida"], "hand": ew.get("hand"),
                                            "body": ew.get("body"),
                                            "pack": ew.get("pack"), "effects": [],
                                            "move_ready_in": 0, "attack_ready_in": 0},
                                       mundo, ee["tic"], list(suelow.values()))
                    oo, _ = AL.obs_con_alcance(oo, mundo, filas_m,
                                               tuple(ee["pos"]),
                                               ee["tic"] - w, herm, {})
                    oo, mm = AL.pon_hermano(oo, memw, herm,
                                            (dia_h or {}).get(ee["tic"]),
                                            tuple(ee["pos"]), mundo)
                    return V42.filas(oo, mundo, mm, ee["tic"]) or {}
                fz, fp = filas_en(cz, j), filas_en(cs, j)
                dif = {k: float(fz.get(k) or 0) - float(fp.get(k) or 0)
                       for k in V42.REPARTO
                       if abs(float(fz.get(k) or 0) - float(fp.get(k) or 0)) > 1e-9}
                if dif:
                    gana_az[min(dif, key=lambda k: dif[k])] += 1
        avisa(f"  [{orden}/40] futuros {n_fut} · azar que gana {n_az}")
        del recs, ctxs
    out = {"G5 proyectado": {k: v for k, v in proy.items()
                             if not k.startswith("fila:")},
           "G5 por fila": {k[5:]: v for k, v in proy.most_common()
                           if k.startswith("fila:")},
           "futuros con mejora proyectada": n_fut,
           "G6 azar que gana": n_az,
           "G6 punto": dict(punto_az),
           "G6 fila que le baja": dict(gana_az.most_common())}
    json.dump(out, open(os.path.join(AQUI, "P53G_G5G6.json"), "w"),
              ensure_ascii=False, indent=1)
    avisa("\n=== G5 · la mejora PROYECTADA por la forma G1+G2 ===")
    tot = sum(v for v in out["G5 proyectado"].values() if v > 0)
    for k, v in sorted(out["G5 proyectado"].items(), key=lambda x: -x[1]):
        avisa(f"   {k:10s} {v:+9.4f} = {100*v/tot:6.2f} %")
    avisa(f"   futuros con mejora proyectada: {n_fut}")
    avisa(f"\n=== G6 · el azar con G1+G2 y margen {MARGEN} ===")
    avisa(f"   gana en {n_az} escenas · puntos {dict(punto_az)}")
    avisa(f"   fila que le baja: {dict(gana_az.most_common(6))}")


if __name__ == "__main__":
    main()

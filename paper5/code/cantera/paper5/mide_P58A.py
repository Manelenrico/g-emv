"""[P5-8A] Los contadores, sobre el lento (objetivo) y S-2 (contraste).

  python3 cantera/paper5/mide_P58A.py lento
  python3 cantera/paper5/mide_P58A.py s2

Diarios de uno en uno. El disparo se evalua en CADA tic vivo (es barato); la
PUERTA, que es lo caro, solo en los tics en que se genera forma.
"""
from __future__ import annotations
import collections, copy, glob, json, os, random, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)

import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B
import curiosidad as C, curiosidad_forma as CF
import forma as F, proyeccion as P

VENTANA = 100          # el horizonte del rastro, como en P5-3
MARGEN = 0.02


def seats(cual):
    if cual == "lento":
        for d in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs",
                                               "P57C_t*_A_*"))):
            for f in sorted(glob.glob(os.path.join(d, "*.art.log"))):
                yield (os.path.basename(d) + "/"
                       + f.rsplit("_", 1)[1].split(".")[0], f)
    else:
        fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                           "*-policy_agent_1*.art.log")))
        idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)),
                                                     min(B.N_DIARIOS, len(fs))))
        for i in idx:
            yield (os.path.basename(fs[i])[:12], fs[i])


def un_asiento(nombre, f, consigna):
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        return None
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    herm = pc.get("teammate_slot")
    ojo = C.Ojo(mundo, 8)
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    tks = [x for x in recs if x.get("k") == "tick"]
    vivos = [x for x in tks if x.get("phase") == "live"]
    if not vivos:
        return None
    por_tic = {r["tick"]: r for r in vivos}
    c = collections.Counter()
    dists, areas, ms_gen, ms_puerta = [], [], [], []
    carencia = []
    nuevas_proy, nuevas_real = [], []
    dano_hist = []
    for r in tks:
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t)
        blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        dano_hist.append((t, sum(float(x.get("amount") or 0)
                                 if isinstance(x, dict) else 0.0
                                 for x in (r.get("damage_taken") or []))))
        if r.get("phase") != "live":
            continue
        pos = tuple(r.get("pos") or ())
        if pos:
            ojo.mira(pos, t)
        pre = copy.deepcopy(mem)
        if not pos:
            continue
        d100 = sum(v for (tt, v) in dano_hist if t - tt < C.VENTANA_DANO)
        am, _ = C.amenaza(r, mundo, herm, d100, t)
        ign = ojo.ignorancia_global()
        if am >= CF.UMBRAL_SEGURO or ign <= consigna:
            c["no_dispara"] += 1
            continue
        c["ventanas"] += 1              # ventana segura con ign sobre consigna
        _a = time.perf_counter()
        arms = CF.armados(r, mundo, herm)
        cam, dist, dest = CF.camino_a_frontera(ojo, mundo, pos, arms)
        ms_gen.append((time.perf_counter() - _a) * 1000.0)
        if dest is None:
            c["sin_frontera"] += 1
            continue
        c["generadas"] += 1
        dists.append(dist)
        # comprobaciones POR CONSTRUCCION
        if CF.cruza_sombra(cam, pos, arms):
            c["cruza_sombra"] += 1
        if CF.destino_a_tiro(dest, arms):
            c["destino_a_tiro"] += 1
        tramos = [{"destino": list(dest), "intencion": "ver", "esperar": 0}]
        # ── LA PUERTA, MUESTREADA ────────────────────────────────────────
        # El DISPARO se mide en cada tic vivo (es barato). La PUERTA es lo
        # caro —curva + comparador sobre los ~20 candidatos— y se evalua cada
        # `CADA` tics desde `DESDE`, las constantes del arnes de P5-2. Sin
        # muestreo serian ~49.000 evaluaciones y horas de reloj. Las
        # fracciones de la puerta son ESTIMACIONES DE MUESTRA; las del
        # disparo son censo.
        if t < B.DESDE or (t - B.DESDE) % B.CADA:
            continue
        c["evaluadas"] += 1
        _a = time.perf_counter()
        try:
            e0 = P.estado_de(r)
            suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
                     if it.get("pos")}
            pcs = F.puntos_de_control(e0, tramos)
            tics = [x[0] for x in pcs]
            if not tics:
                c["sin_puntos"] += 1
                continue
            pisos = F.pisos_rival(o, mundo, pre, t)
            base_c = list(D.candidatos(o, mundo, copy.deepcopy(pre), t,
                                       copy.deepcopy(blo)))
            # (a) CON el renglon en la proyeccion
            _orig, porv = CF.con_renglon(ojo, mundo, cam, tics, t, am)
            try:
                cf_con = F.curva_H(e0, o, tramos, mundo, pre, suelo, tics,
                                   herm, None, pisos)
                cs_con, _q, _n, _mv = F.mejor_propia_H(
                    e0, o, base_c, tics, mundo, pre, suelo, t, herm, None,
                    pisos)
            finally:
                CF.restaura(_orig)
            # (b) SIN el renglon
            cf_sin = F.curva_H(e0, o, tramos, mundo, pre, suelo, tics, herm,
                               None, pisos)
            cs_sin, _q2, _n2, _mv2 = F.mejor_propia_H(
                e0, o, base_c, tics, mundo, pre, suelo, t, herm, None, pisos)
        except Exception as ex:
            c["error_puerta"] += 1
            continue
        finally:
            ms_puerta.append((time.perf_counter() - _a) * 1000.0)
        if cs_con is None or cs_sin is None:
            c["sin_comparador"] += 1
            continue
        ver_con, ar_con, _d = F.juzga_margen(cf_con, cs_con, t, margen=MARGEN)
        ver_sin, ar_sin, _d = F.juzga_margen(cf_sin, cs_sin, t, margen=MARGEN)
        areas.append(ar_con)
        c["pasa_con_" + ver_con] += 1
        c["pasa_sin_" + ver_sin] += 1
        if ver_con == "ok":
            c["pasa"] += 1
            # DERROCHE: R-CARENCIA proyectada al final contra al principio
            try:
                F0 = V42.filas(o, mundo, pre, t)
                oz = F.foto_rapida(o, {"pos": list(dest), "hp": e0["hp"],
                                       "pack": e0.get("pack"),
                                       "hand": e0.get("hand"),
                                       "body": e0.get("body"),
                                       "tick": tics[-1], "W": e0.get("W")},
                                   mundo, tics[-1],
                                   list(suelo.values()))
                F1 = V42.filas(oz, mundo, pre, tics[-1])
                carencia.append((float(F0.get("R-CARENCIA") or 0.0),
                                 float(F1.get("R-CARENCIA") or 0.0)))
            except Exception:
                pass
            # casillas nuevas PROYECTADAS contra REALES en la misma ventana
            _, ign_fin = porv.get(tics[-1], (0, None))
            if ign_fin is not None:
                nuevas_proy.append(int(round((ign - ign_fin) * ojo.n_arena)))
            ya = set(ojo.primera_vez)
            real = set()
            for u in range(t, min(t + VENTANA, vivos[-1]["tick"]) + 1):
                rr = por_tic.get(u)
                if rr and rr.get("pos"):
                    real |= ojo.vistas_desde(tuple(rr["pos"]))
            nuevas_real.append(len(real - ya))
            # ABANDONO: armado que cubre el camino restante, en la ventana
            aband = False
            for u in range(t + 1, min(t + VENTANA, vivos[-1]["tick"]) + 1):
                rr = por_tic.get(u)
                if rr and CF.abandona_por_peligro(dest, cam, rr, mundo, herm):
                    aband = True
                    break
            c["abandona_peligro"] += aband
    return {"nombre": nombre, "consigna": consigna, "vivos": len(vivos),
            "c": dict(c), "dists": dists, "areas": areas,
            "ms_gen": ms_gen, "ms_puerta": ms_puerta,
            "carencia": carencia, "nuevas_proy": nuevas_proy,
            "nuevas_real": nuevas_real}


def main():
    cual = sys.argv[1] if len(sys.argv) > 1 else "lento"
    todo = []
    for cons in CF.CONSIGNAS:
        for n, (nombre, f) in enumerate(seats(cual), 1):
            o = un_asiento(nombre, f, cons)
            if o:
                todo.append(o)
            print(f"  [{cons}] [{n}] {nombre}: "
                  f"{(o or {}).get('c', {}).get('generadas', 0)} generadas",
                  flush=True)
    json.dump(todo, open(os.path.join(AQUI, f"P58A_{cual}.json"), "w"))
    print(f"guardado en P58A_{cual}.json")


if __name__ == "__main__":
    main()

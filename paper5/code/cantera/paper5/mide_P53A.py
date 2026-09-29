"""[P5-3A] A0, A2, A3, A4 y A5. SOLO LECTURA de diarios. Coste cero."""
from __future__ import annotations
import collections, glob, json, os, random, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                     # noqa: E402
import banco_llaves as B                                   # noqa: E402
import proyeccion as P                                     # noqa: E402
from alma import appraisal_zs_v42_exp as V42               # noqa: E402

KS = (25, 50, 100)
PROG = open(os.path.join(AQUI, "P53A_progreso.log"), "w", buffering=1)


def avisa(t):
    print(t, flush=True)
    PROG.write(t + "\n")


def med(v):
    return st.median(v) if v else None


def p90(v):
    return sorted(v)[int(0.9 * (len(v) - 1))] if v else None


def acciones_reales(recs_por_tic, t, K):
    """Lo que el cuerpo HIZO en los K tics siguientes, leido del diario."""
    out = []
    for u in range(t + 1, t + K + 1):
        r = recs_por_tic.get(u)
        if r is None:
            out.append(None)
            continue
        el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
        if el.startswith(("ir_", "move_", "paso_")):
            out.append("paso")
        elif el.startswith("coger"):
            out.append("coger")
        elif el.startswith("usar_"):
            out.append("usar_" + el[len("usar_"):])
        else:
            out.append("esperar")
    return out


def anda(recs, tanda, salida):
    fila = []
    a0 = {"mirada": collections.Counter(), "pasos_cand": [],
          "gap_pasos": [], "dist_ganador": []}
    tope = collections.Counter()
    err = {c: {K: {"W": [], "hp": []} for K in KS} for c in
           ("foto", "real", "intencion")}
    err_real_sin = {K: {"W": [], "hp": []} for K in KS}
    err_real_con = {K: {"W": [], "hp": []} for K in KS}
    cambia = {K: {"W": 0, "hp": 0, "n": 0} for K in KS}
    techo = {"hp_rival": 0.0, "hp_anillo": 0.0, "hp_sin": 0,
             "W_coger": 0, "W_consumir": 0, "W_morir": 0, "W_igual": 0,
             "ventanas": 0}
    errH = {"W": [], "hp": [], "H": []}
    fallos = []

    for nd, (f, recs_l) in enumerate(recs, 1):
        pc = next(r for r in recs_l if r.get("k") == "player_config")
        sm = next(r for r in recs_l if r.get("k") == "static_map")
        cat = next(r for r in recs_l if r.get("k") == "catalogo")
        B.pon_v42(B.interruptores(recs_l))
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        tk = {r["tick"]: r for r in recs_l if r.get("k") == "tick"}
        vivos = [r for r in recs_l
                 if r.get("k") == "tick" and r.get("phase") == "live"]
        # A0: el gap real entre pasos
        ant = None
        for r in vivos:
            p = tuple(r.get("pos") or ())
            if ant is not None and p != ant[1]:
                a0["gap_pasos"].append(r["tick"] - ant[0])
            if ant is None or p != ant[1]:
                ant = (r["tick"], p)
        for r in vivos:
            R = r.get("RADIOGRAFIA") or {}
            el = R.get("elegido") or ""
            H = R.get("mirada_ticks")
            if H:
                a0["mirada"][H] += 1
            cands = R.get("candidatos") or {}
            for n, v in cands.items():
                if n.startswith("ir_") and isinstance(v, dict) and v.get("pos_prevista"):
                    a0["pasos_cand"].append(
                        U.cheb(tuple(r.get("pos") or ()), tuple(v["pos_prevista"])))
            if not el.startswith("ir_"):
                continue
            det = cands.get(el)
            if not isinstance(det, dict) or not det.get("pos_prevista"):
                continue
            t = r["tick"]
            a0["dist_ganador"].append(
                U.cheb(tuple(r.get("pos") or ()), tuple(det["pos_prevista"])))
            e0 = P.estado_de(r)
            W0 = P.W_de(e0, mundo)
            suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
                     if it.get("pos")}
            dest = tuple(det["pos_prevista"])
            for K in list(KS) + ([H] if H else []):
                u = t + K
                rr = tk.get(u)
                if rr is None or rr.get("phase") != "live":
                    continue
                e_real = P.estado_de(rr)
                W_real = P.W_de(e_real, mundo)
                hp_real = e_real["hp"]
                # A2 · la foto congelada
                fo = P.congelada(e0, mundo, K)
                dW_f, dh_f = abs(fo["W"] - W_real), abs(fo["hp"] - hp_real)
                # A4 · con intencion
                inten = {"destino": dest,
                         "coger": dest in suelo,
                         "usar": None}
                pi = P.proyectar(e0, inten, K, mundo, suelo)
                dW_i, dh_i = abs(pi["W"] - W_real), abs(pi["hp"] - hp_real)
                # A3 · con camino real
                cam = [tuple(tk[x].get("pos") or ()) if x in tk else None
                       for x in range(t + 1, t + K + 1)]
                pr = P.proyectar(e0, acciones_reales(tk, t, K), K, mundo,
                                 suelo, camino=cam)
                dW_r, dh_r = abs(pr["W"] - W_real), abs(pr["hp"] - hp_real)
                if K == H and K not in KS:
                    errH["W"].append(dW_f)
                    errH["hp"].append(dh_f)
                    errH["H"].append(H)
                    continue
                err["foto"][K]["W"].append(dW_f)
                err["foto"][K]["hp"].append(dh_f)
                err["intencion"][K]["W"].append(dW_i)
                err["intencion"][K]["hp"].append(dh_i)
                err["real"][K]["W"].append(dW_r)
                err["real"][K]["hp"].append(dh_r)
                cambia[K]["n"] += 1
                cambia[K]["W"] += abs(W_real - W0) > 1e-9
                cambia[K]["hp"] += abs(hp_real - e0["hp"]) > 1e-9
                # con o sin dano de rival en la ventana
                rival = False
                veneno = False
                anillo = 0.0
                for x in range(t + 1, u + 1):
                    q = tk.get(x)
                    if not q:
                        continue
                    for g in (q.get("damage_taken") or []):
                        s = g.get("source")
                        if s == "zone":
                            anillo += float(g.get("amount") or 0)
                        elif s == "poison":
                            veneno = True
                        else:
                            rival = True
                ajeno = rival or veneno
                (err_real_con if ajeno else err_real_sin)[K]["W"].append(dW_r)
                (err_real_con if ajeno else err_real_sin)[K]["hp"].append(dh_r)
                if K == 100 and not ajeno and (dW_r > 1e-6 or dh_r > 1e-6) \
                        and len(fallos) < 12:
                    fallos.append({"diario": os.path.basename(f), "tic": t,
                                   "K": K, "dW": round(dW_r, 4),
                                   "dhp": round(dh_r, 3),
                                   "W_proy": round(pr["W"], 4),
                                   "W_real": round(W_real, 4),
                                   "hp_proy": round(pr["hp"], 2),
                                   "hp_real": hp_real,
                                   "pack_proy": [s.get("id") for s in pr["pack"]],
                                   "pack_real": [s.get("id") for s in e_real["pack"]],
                                   "hand_proy": (pr.get("hand") or {}).get("id"),
                                   "hand_real": (e_real.get("hand") or {}).get("id")})
                if K == 100:
                    techo["ventanas"] += 1
                    perdida = e0["hp"] - hp_real
                    riv = 0.0
                    for x in range(t + 1, u + 1):
                        q = tk.get(x)
                        if not q:
                            continue
                        for g in (q.get("damage_taken") or []):
                            if g.get("source") not in ("zone",):
                                riv += float(g.get("amount") or 0)
                    techo["hp_rival"] += riv
                    techo["hp_anillo"] += anillo
                    techo["hp_sin"] += (abs(perdida) < 1e-9)
                    if abs(W_real - W0) < 1e-9:
                        techo["W_igual"] += 1
                    elif hp_real <= 0:
                        techo["W_morir"] += 1
                    elif W_real > W0:
                        techo["W_coger"] += 1
                    else:
                        techo["W_consumir"] += 1
        avisa(f"  [{nd}/{len(recs)}] {os.path.basename(f)[:44]} · "
              f"ventanas K=100 acumuladas {techo['ventanas']:,}")

    out = {"tanda": tanda,
           "A0": {"mirada_ticks": dict(a0["mirada"].most_common(4)),
                  "pasos de los candidatos ir_*: mediana": med(a0["pasos_cand"]),
                  "pasos del ganador: mediana": med(a0["dist_ganador"]),
                  "tics entre paso y paso: mediana": med(a0["gap_pasos"]),
                  "n gaps": len(a0["gap_pasos"])},
           "A2/A3/A4": {str(K): {
               c: {"W mediana": med(err[c][K]["W"]),
                   "W p90": p90(err[c][K]["W"]),
                   "vida mediana": med(err[c][K]["hp"]),
                   "vida p90": p90(err[c][K]["hp"]),
                   "n": len(err[c][K]["W"])} for c in
               ("foto", "real", "intencion")} for K in KS},
           "A2 en K=H": {"W mediana": med(errH["W"]), "W p90": p90(errH["W"]),
                         "vida mediana": med(errH["hp"]),
                         "vida p90": p90(errH["hp"]),
                         "H mediana": med(errH["H"]), "n": len(errH["W"])},
           "cambia algo": {str(K): {
               "W cambia": cambia[K]["W"], "vida cambia": cambia[K]["hp"],
               "n": cambia[K]["n"]} for K in KS},
           "A3 por ventana": {str(K): {
               "sin dano ajeno (ni rival ni veneno)": {
                   "n": len(err_real_sin[K]["W"]),
                   "W mediana": med(err_real_sin[K]["W"]),
                   "W p90": p90(err_real_sin[K]["W"]),
                   "vida mediana": med(err_real_sin[K]["hp"]),
                   "vida p90": p90(err_real_sin[K]["hp"])},
               "con dano ajeno": {
                   "n": len(err_real_con[K]["W"]),
                   "W mediana": med(err_real_con[K]["W"]),
                   "W p90": p90(err_real_con[K]["W"]),
                   "vida mediana": med(err_real_con[K]["hp"]),
                   "vida p90": p90(err_real_con[K]["hp"])}} for K in KS},
           "A5 el techo": techo,
           "ejemplos de residuo": fallos}
    json.dump(out, open(os.path.join(AQUI, salida), "w"),
              ensure_ascii=False, indent=1)
    return out


def carga(fs):
    for f in fs:
        recs = list(U.lee(f))
        if not any(r.get("k") == "player_config" for r in recs):
            continue
        if not any(r.get("k") == "static_map" for r in recs):
            continue
        if not any(r.get("k") == "catalogo" for r in recs):
            continue
        yield f, recs


def main():
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                       "*-policy_agent_1*.art.log")))
    idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
    avisa("=== S-2 brazo A, 40 diarios ===")
    r1 = anda(list(carga([fs[i] for i in idx])), "S-2 brazo A (40)",
              "P53A_S2.json")
    lentos = []
    for c in ("P5_B1", "P5_C2", "P5_C3"):
        lentos += sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", c,
                                                "*.art.log")))
    avisa("=== mundo lento, 6 asientos-partida ===")
    r2 = anda(list(carga(lentos)), "mundo lento (6)", "P53A_lento.json")
    for r in (r1, r2):
        avisa(f"\n### {r['tanda']}")
        avisa(f"  A0: {r['A0']}")
        for K in KS:
            d = r["A2/A3/A4"][str(K)]
            avisa(f"  K={K:3d} n={d['foto']['n']:5,} · foto W med "
                  f"{d['foto']['W mediana']} p90 {d['foto']['W p90']} | vida med "
                  f"{d['foto']['vida mediana']} p90 {d['foto']['vida p90']}")
            avisa(f"          intencion W med {d['intencion']['W mediana']} p90 "
                  f"{d['intencion']['W p90']} | vida med "
                  f"{d['intencion']['vida mediana']} p90 "
                  f"{d['intencion']['vida p90']}")
            avisa(f"          camino real W med {d['real']['W mediana']} p90 "
                  f"{d['real']['W p90']} | vida med {d['real']['vida mediana']} "
                  f"p90 {d['real']['vida p90']}")
        avisa(f"  A2 en K=H: {r['A2 en K=H']}")
        avisa(f"  A3 por ventana K=100: {r['A3 por ventana']['100']}")
        avisa(f"  A5 techo: {r['A5 el techo']}")


if __name__ == "__main__":
    main()

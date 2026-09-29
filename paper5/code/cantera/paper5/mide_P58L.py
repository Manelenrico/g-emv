"""[P5-8L] Por que el veto duro mata los viajes largos, y si tenia razon.

En seco, coste cero, sobre los diarios de K (y A como base) de P5-8I y P5-8K.
El camino de cada forma se RECONSTRUYE con el mismo `camino_a_frontera` de la
imagen, y se comprueba contra el destino registrado (control).
"""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U
from serie_util import D, DOV
import banco_llaves as B
import curiosidad as C, curiosidad_forma as CFM
from alma import appraisal_zs_v42_exp as V42


def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def tramo(d):
    return ("1-3" if d <= 3 else "4-5" if d <= 5 else "6-7" if d <= 7
            else "8-9" if d <= 9 else "10+")


FORMAS, BASE_A, CTRL = [], [], {"dest_ok": 0, "dest_mal": 0}

for sonda, pat in (("I", "P58I_t1_{b}_*"), ("K", "P58K_t0_{b}_*")):
    for brazo in ("K", "A"):
        for f in sorted(glob.glob(f"paintball/runs/{pat.format(b=brazo)}/*.art.log")):
            recs = list(U.lee(f))
            pc = next((r for r in recs if r.get("k") == "player_config"), None)
            sm = next((r for r in recs if r.get("k") == "static_map"), None)
            cat = next((r for r in recs if r.get("k") == "catalogo"), None)
            if not (pc and sm and cat):
                continue
            B.pon_v42(B.interruptores(recs))
            mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
            herm = pc.get("teammate_slot")
            carpeta = os.path.basename(os.path.dirname(f))
            semilla = carpeta.split("_")[3]
            slot = f.rsplit("_", 1)[1][:2]
            nom = f"{sonda}/{semilla}/{slot}"
            vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
            if not vivos:
                continue
            por_tic = {r["tick"]: r for r in vivos}
            # daño recibido por tic, con AUTOR (el parte cierto del protocolo)
            dano_t, autor_t = {}, {}
            for r in vivos:
                tot, aut = 0.0, set()
                for x in (r.get("damage_taken") or []):
                    if not isinstance(x, dict) or str(x.get("source")) == "zone":
                        continue
                    tot += float(x.get("amount") or 0)
                    aut.add(str(x.get("source")))
                if tot > 0:
                    dano_t[r["tick"]] = tot; autor_t[r["tick"]] = aut
            t_dano = sorted(dano_t)
            dano_hist = []

            # ── la base de A: daño en 50 tics en entorno SEGURO ──
            if brazo == "A":
                seg = dseg = 0
                for r in vivos:
                    t = r["tick"]
                    dano_hist.append((t, dano_t.get(t, 0.0)))
                    d100 = sum(v for (tt, v) in dano_hist
                               if 0 <= t - tt < C.VENTANA_DANO)
                    am, _ = C.amenaza(r, mundo, herm, d100, t)
                    if C.grado(am) == "seguro":
                        seg += 1
                        if any(t < u <= t + 50 for u in t_dano):
                            dseg += 1
                BASE_A.append({"sonda": sonda, "asiento": nom,
                               "seguro": seg, "con_dano_50": dseg})
                print(f"  A {nom}: seguro {seg} tics · con daño en 50 {dseg}",
                      flush=True)
                continue

            # ── K: las formas ──
            prop = {r["tick"]: r for r in recs
                    if r.get("k") == "forma_propuesta" and r.get("origen") == "curiosidad"}
            acep = {r["id"] for r in recs if r.get("k") == "forma_aceptada"}
            caida = {r["id"]: r for r in recs if r.get("k") == "forma_caida"}
            ojo = C.Ojo(mundo, 8)
            mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
            caminos = {}
            for r in [x for x in recs if x.get("k") == "tick"]:
                t = r["tick"]
                o = DOV.a_obs(r)
                o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
                mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t)
                ult = r.get("intencion")
                if r.get("phase") != "live":
                    continue
                p = tuple(r.get("pos") or ())
                if p:
                    ojo.mira(p, t)
                if t in prop and p:
                    p0 = prop[t]
                    arms = CFM.armados(r, mundo, herm)
                    cam, dist, dest = CFM.camino_a_frontera(ojo, mundo, p, arms)
                    if dest is None:
                        continue
                    if list(dest) == list(p0.get("destino") or []):
                        CTRL["dest_ok"] += 1
                    else:
                        CTRL["dest_mal"] += 1
                    caminos[p0["id"]] = (cam, dist, dest)

            for fid in sorted(acep):
                if fid not in caminos:
                    continue
                cam, dist, dest = caminos[fid]
                cr = caida.get(fid)
                motivo = str((cr or {}).get("motivo") or "sin fin")
                t_fin = (cr or {}).get("tick")
                fila = {"sonda": sonda, "asiento": nom, "id": fid,
                        "dist": dist, "tramo": tramo(dist),
                        "motivo": motivo[:24], "t_fin": t_fin,
                        "culpable": None}
                # ── EL ARMADO QUE DISPARA EL VETO DURO ──
                if motivo.startswith("veto duro") and t_fin in por_tic:
                    r = por_tic[t_fin]
                    pos = tuple(r.get("pos") or ())
                    try:
                        i = cam.index(pos)
                    except ValueError:
                        i = 0
                    resto = cam[i:] or cam
                    quien = None
                    for a in (r.get("ve_agentes") or []):
                        if a.get("slot") == herm or not a.get("pos"):
                            continue
                        rg = C._alcance(mundo, a.get("hand"))
                        if rg <= 0:
                            continue
                        q = tuple(a["pos"])
                        if any(cheb(x, q) <= rg for x in resto):
                            quien = (a, q, rg); break
                    if quien:
                        a, q, rg = quien
                        sl = a.get("slot")
                        # ¿se acercaba en los 5 tics anteriores? ¿estaba quieto?
                        antes = None
                        for dt in range(1, 6):
                            rr = por_tic.get(t_fin - dt)
                            if not rr: continue
                            for b in (rr.get("ve_agentes") or []):
                                if b.get("slot") == sl and b.get("pos"):
                                    antes = tuple(b["pos"]); break
                            if antes: break
                        d_ahora = cheb(pos, q)
                        d_antes = cheb(tuple(por_tic[t_fin - dt].get("pos") or pos),
                                       antes) if antes else None
                        fila["culpable"] = {
                            "slot": sl, "team": a.get("team"), "hand": a.get("hand"),
                            "alcance": rg, "d_cuerpo": d_ahora,
                            "hermano": sl == herm,
                            "se_acercaba": (None if d_antes is None
                                            else bool(d_ahora < d_antes)),
                            "quieto": (None if antes is None else antes == q),
                            "dano_50_de_el": any(
                                t_fin < u <= t_fin + 50 and f"P{sl}" in autor_t.get(u, ())
                                for u in t_dano),
                            "dano_50_de_cualquiera": any(
                                t_fin < u <= t_fin + 50 for u in t_dano),
                        }
                # ── K5: daño con la forma VIVA ──
                t0 = prop[[t for t in prop if prop[t]["id"] == fid][0]]["tick"] \
                    if any(prop[t]["id"] == fid for t in prop) else None
                if t0 is not None and t_fin is not None:
                    fila["dano_durante"] = any(t0 <= u <= t_fin for u in t_dano)
                    fila["dano_tras_fin_50"] = any(t_fin < u <= t_fin + 50
                                                   for u in t_dano)
                FORMAS.append(fila)
            print(f"  K {nom}: {len(acep)} aceptadas · "
                  f"{sum(1 for x in FORMAS if x['asiento']==nom)} con camino",
                  flush=True)

json.dump({"formas": FORMAS, "base_A": BASE_A, "control": CTRL},
          open("cantera/paper5/P58L.json", "w"), ensure_ascii=False)
print(f"\ncontrol destino: {CTRL} · {len(FORMAS)} formas · "
      f"{len(BASE_A)} asientos de A")

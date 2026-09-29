"""[P5-8O] ¿Anduvo el cuerpo las formas del consejero? P5-6C, brazos F y T.

La ventana activa se RECONSTRUYE: de `forma_aceptada` a `forma_caida`, y si no
hay cierre, hasta la llegada proyectada (el ultimo punto de control, que la
propia `forma_aceptada` trae en `tics`).
"""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U


def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


FORMAS, POR_QUE_NO, REF_A = [], collections.Counter(), []

for brazo in ("F", "T"):
    for f in sorted(glob.glob(f"paintball/runs/P56C_t*_{brazo}_*/*.art.log")):
        recs = list(U.lee(f))
        vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
        if not vivos:
            continue
        por_tic = {r["tick"]: r for r in vivos}
        t_ult = vivos[-1]["tick"]
        carpeta = os.path.basename(os.path.dirname(f))
        nom = f"{brazo}/{carpeta.split('_')[3]}/{f.rsplit('_',1)[1][:2]}"
        acep = [r for r in recs if r.get("k") == "forma_aceptada"]
        caida = {r["id"]: r for r in recs if r.get("k") == "forma_caida"}
        conf = collections.defaultdict(list)
        for r in recs:
            if r.get("k") == "confianza":
                conf[r.get("id")].append(r)

        for a in acep:
            fid = a.get("id")
            t0 = a["tick"]
            tramos = a.get("tramos") or []
            tics = a.get("tics") or []
            cr = caida.get(fid)
            # ── LA VENTANA ──
            if cr:
                t1, cierre = cr["tick"], str(cr.get("motivo") or "")[:40]
            elif tics:
                t1, cierre = tics[-1], "sin cierre · llegada proyectada"
            else:
                POR_QUE_NO["sin cierre y sin puntos de control"] += 1
                continue
            if t1 > t_ult:
                t1, cierre = t_ult, cierre + " (recortada al fin de la vida)"
            dentro = [t for t in range(t0, t1 + 1) if t in por_tic]
            if len(dentro) < 2:
                POR_QUE_NO["ventana de menos de dos tics vivos"] += 1
                continue
            # ── EL DESTINO: el primer tramo que TENGA uno ──
            dest = None
            for i, tr in enumerate(tramos):
                if tr.get("destino"):
                    dest = tuple(tr["destino"]); break
            if dest is None:
                POR_QUE_NO["ningun tramo tiene destino (esperar/usar)"] += 1
                FORMAS.append({"asiento": nom, "id": fid, "brazo": brazo,
                               "t0": t0, "t1": t1, "cierre": cierre,
                               "tics": len(dentro), "sin_destino": True,
                               "cumple": [c.get("veredicto") for c in conf.get(fid, [])],
                               "puntos": []})
                continue
            # ── EL ANDAR ──
            listas = gana_fm = mueve = acerca = 0
            prev = tuple(por_tic[dentro[0]].get("pos") or ())
            d0 = cheb(prev, dest) if prev else None
            dmin = d0
            for t in dentro[1:]:
                r = por_tic[t]
                if int(r.get("move_ready_in") or 0) == 0:
                    listas += 1
                    el = (r.get("RADIOGRAFIA") or {}).get("elegido")
                    if str(el or "").startswith("_FM_"):
                        gana_fm += 1
                p = tuple(r.get("pos") or ())
                if not p:
                    continue
                if p != prev:
                    mueve += 1
                    if cheb(p, dest) < cheb(prev, dest):
                        acerca += 1
                prev = p
                dmin = min(dmin, cheb(p, dest)) if dmin is not None else cheb(p, dest)
            d1 = cheb(prev, dest) if prev else None
            FORMAS.append({
                "asiento": nom, "brazo": brazo, "id": fid,
                "t0": t0, "t1": t1, "vive": t1 - t0, "tics": len(dentro),
                "cierre": cierre, "sin_destino": False,
                "n_tramos": len(tramos),
                "listas": listas, "gana_fm": gana_fm,
                "mueve": mueve, "acerca": acerca,
                "d0": d0, "d1": d1, "dmin": dmin,
                "llega": (dmin == 0),
                # «anduvo» = se acerco al menos la mitad del camino
                "anduvo": (d0 is not None and d0 > 0 and dmin is not None
                           and (d0 - dmin) >= d0 / 2.0),
                # LOS DOS CRITERIOS: el veredicto del diario («acierto»/«fallo»)
                # y el de `analiza_P56C.py`, que es el que dio el 42,3 % / 61,1 %
                # y se mide POR PUNTO DE CONTROL, no por forma.
                "cumple": [c.get("veredicto") for c in conf.get(fid, [])],
                "puntos": [{"v": c.get("veredicto"),
                            "dr": c.get("d_real"), "dp": c.get("d_proyectada"),
                            "p56c": (c.get("d_real") is not None
                                     and c.get("d_proyectada") is not None
                                     and c["d_real"] <= c["d_proyectada"] + 0.05)}
                           for c in conf.get(fid, [])],
            })
        print(f"  {nom}: {len(acep)} aceptadas", flush=True)

# ── la referencia de A: los `ir_` del propio cuerpo, con destino leido ──
VENT = 25          # la MEDIANA de vida de las 86 formas de F y T, para que
                   # la referencia de A mire la misma cantidad de tiempo
for f in sorted(glob.glob("paintball/runs/P56C_t*_A_*/*.art.log")):
    recs = list(U.lee(f))
    vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
    if not vivos:
        continue
    por_tic = {r["tick"]: r for r in vivos}
    nom = os.path.basename(os.path.dirname(f)).split("_")[3] + "/" + f.rsplit("_", 1)[1][:2]
    for r in vivos:
        ra = r.get("RADIOGRAFIA") or {}
        el = str(ra.get("elegido") or "")
        ah = ra.get("ahora") or {}
        dest = None
        if el == "ir_botin":
            dest = (ah.get("botin") or {}).get("objetivo")
        elif el == "ir_centro":
            dest = (r.get("zona") or {}).get("center")
        elif el == "ir_pareja":
            dest = (r.get("social") or {}).get("pareja_pos")
        if not dest:
            continue
        dest = tuple(dest)
        t0 = r["tick"]
        p0 = tuple(r.get("pos") or ())
        if not p0:
            continue
        d0 = cheb(p0, dest)
        dmin, prev, acerca, mueve = d0, p0, 0, 0
        for t in range(t0 + 1, t0 + VENT + 1):
            rr = por_tic.get(t)
            if not rr:
                break
            p = tuple(rr.get("pos") or ())
            if not p:
                continue
            if p != prev:
                mueve += 1
                if cheb(p, dest) < cheb(prev, dest):
                    acerca += 1
            prev = p
            dmin = min(dmin, cheb(p, dest))
        REF_A.append({"asiento": nom, "cual": el, "d0": d0, "dmin": dmin,
                      "d1": cheb(prev, dest), "mueve": mueve, "acerca": acerca,
                      "llega": dmin == 0,
                      "anduvo": d0 > 0 and (d0 - dmin) >= d0 / 2.0})

json.dump({"formas": FORMAS, "no": dict(POR_QUE_NO), "ref_A": REF_A,
           "ventana_A": VENT},
          open("cantera/paper5/P58O.json", "w"), ensure_ascii=False)
print(f"\n{len(FORMAS)} formas de F y T · {len(REF_A)} referencias de A · "
      f"no reconstruibles {dict(POR_QUE_NO)}")

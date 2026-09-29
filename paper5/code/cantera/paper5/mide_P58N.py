"""[P5-8N] Fuera de forma: ¿se comporta K distinto de A con el botin?

La fila R-CURIOSIDAD-FRONTERA NO esta instalada en K (comprobado: GEMV_CURIOSIDAD
vacio, CURIOSIDAD_ON=False, cero registros `curiosidad_tic`). Asi que fuera de
forma la maquinaria de decision de K es la MISMA que la de A, y toda diferencia
es de TRAYECTORIA. Esto lo mide.
"""
import collections, glob, json, os, statistics as st, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U, curiosidad as C
from alma import appraisal_zs_v42_exp as A      # la W se IMPORTA


def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def med(v): return round(st.median(v), 4) if v else None


OUT = []
for brazo in ("K", "A"):
    for f in sorted(glob.glob(f"paintball/runs/P58M_t[12]_{brazo}_*/*.art.log")):
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            continue
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        carpeta = os.path.basename(os.path.dirname(f))
        semilla, slot = carpeta.split("_")[3], f.rsplit("_", 1)[1][:2]
        vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
        if not vivos:
            continue
        ctic = {r["tick"]: r.get("activa") for r in recs
                if r.get("k") == "cur_forma_tic"}
        fin_r = next((r for r in recs if r.get("k") == "final"), {})

        fuera = [r for r in vivos if ctic.get(r["tick"]) is None]
        gana = collections.Counter()
        Ws, dist_bot, cogio_f = [], [], 0
        fm_fuera = 0
        for r in fuera:
            ra = r.get("RADIOGRAFIA") or {}
            el = ra.get("elegido")
            if el:
                gana[el] += 1
                if str(el).startswith("_FM_"):
                    fm_fuera += 1
            try:
                Ws.append(float(A.riqueza_W(
                    {"hand": r.get("hand"), "pack": r.get("pack"),
                     "body": r.get("body")}, mundo)[0]))
            except Exception:
                pass
            p = tuple(r.get("pos") or ())
            its = [tuple(it["pos"]) for it in (r.get("ve_items") or [])
                   if it.get("pos")]
            if p and its:
                dist_bot.append(min(cheb(p, q) for q in its))
            if (r.get("social") or {}).get("cogio"):
                cogio_f += 1
        n = sum(gana.values())

        # ── (4) la muerte ──
        ult = vivos[-1]
        try:
            W_muerte = round(float(A.riqueza_W(
                {"hand": ult.get("hand"), "pack": ult.get("pack"),
                 "body": ult.get("body")}, mundo)[0]), 4)
        except Exception:
            W_muerte = None

        OUT.append({
            "brazo": brazo, "semilla": semilla, "slot": slot,
            "tics": len(vivos), "tics_fuera": len(fuera),
            "n_dec_fuera": n,
            "ir_botin": gana.get("ir_botin", 0),
            "ir_objeto": gana.get("ir_objeto", 0),
            "noop": gana.get("noop", 0),
            "fm_fuera": fm_fuera,
            "W_med_fuera": med(Ws),
            "dist_botin_med": med(dist_bot),
            "cogio_fuera": cogio_f,
            "tic_muerte": ult.get("tick"),
            "causa": fin_r.get("reason"), "puesto": fin_r.get("placement"),
            "match_ticks": fin_r.get("match_ticks"),
            "hp_ult": ult.get("hp"), "W_muerte": W_muerte,
            "top": dict(gana.most_common(6)),
        })
        print(f"  {brazo} {semilla}/{slot}: fuera {len(fuera):6d} tics · "
              f"ir_botin {100.0*gana.get('ir_botin',0)/max(n,1):5.2f}% · "
              f"W {med(Ws)} · dist botin {med(dist_bot)} · "
              f"cogio {cogio_f} · muere t{ult.get('tick')} ({fin_r.get('reason')})",
              flush=True)

json.dump(OUT, open("cantera/paper5/P58N.json", "w"), ensure_ascii=False)
print(f"\n{len(OUT)} asientos · cantera/paper5/P58N.json")

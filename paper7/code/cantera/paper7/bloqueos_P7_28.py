"""[P7-28, punto 1, lo que la replica no mide] LOS PASOS BLOQUEADOS, contados del diario: tics con el paso listo (`move_ready_in` = 0) cuyo `action_result` es "blocked"
(un paso pedido que el mundo no dio), por brazo y bloque de dias y por lo elegido; y por vida de APRENDE en los dias 16-20, con la racha maxima de tics seguidos bloqueados.
  python3 bloqueos_P7_28.py -> P7_28_bloqueos_brazos.json, P7_28_bloqueos.json"""
import collections, glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); ELS = ("ir_curioso", "ir_objeto", "ir_centro", "ir_botin", "noop")


def cuenta(f):
    c = collections.Counter(); b = collections.Counter(); rach = 0; maxr = 0; rach_cur = 0; maxr_cur = 0
    for line in open(f, errors="replace"):
        if '"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") != "tick" or r.get("phase") != "live" or (r.get("move_ready_in") or 0) != 0: continue
        el = str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""); c[el] += 1
        if r.get("action_result") == "blocked":
            b[el] += 1; rach += 1; maxr = max(maxr, rach)
            if el == "ir_curioso": rach_cur += 1; maxr_cur = max(maxr_cur, rach_cur)
        else:
            rach = 0
            if el == "ir_curioso": rach_cur = 0
    return c, b, maxr, maxr_cur


if __name__ == "__main__":
    out = {}; por_vida = {}
    for brazo in ("APRENDE", "BORRADO", "TECHO"):
        for nb, ds in (("1-5", range(1, 6)), ("16-20", range(16, 21))):
            c = collections.Counter(); b = collections.Counter(); vidas = 0; rachas = 0
            for d in ds:
                for s in (1, 2):
                    for sl in (10, 11):
                        fs = glob.glob(os.path.join(RAIZ, "paintball", "runs", f"P724_s{s}_d{d}_{brazo}_*", f"*agent_{sl}.art.log"))
                        if not fs: continue
                        ci, bi, maxr, maxr_cur = cuenta(fs[0]); vidas += 1; c.update(ci); b.update(bi)
                        if maxr >= 200: rachas += 1
                        if brazo == "APRENDE" and nb == "16-20": por_vida[f"s{s}_d{d}_{sl}"] = {"ir_curioso_listo": ci["ir_curioso"], "ir_curioso_bloqueado": bi["ir_curioso"], "racha_max_bloqueada": maxr, "racha_max_bloqueada_ir_curioso": maxr_cur, "listos": sum(ci.values()), "bloqueados": sum(bi.values())}
            tot = sum(c.values()); tb = sum(b.values())
            out[f"{brazo} {nb}"] = {"vidas": vidas, "listos": tot, "bloqueados": tb, "fraccion": round(tb / tot, 3), "vidas_con_racha_200": rachas, "por_eleccion": {k: [c[k], b[k]] for k in ELS}}
            print(brazo, nb, out[f"{brazo} {nb}"])
    json.dump(out, open(os.path.join(AQUI, "P7_28_bloqueos_brazos.json"), "w"), indent=0)
    por_vida["total"] = {k: [sum(v["ir_curioso_listo"] for kk, v in por_vida.items() if kk != "total") if k == "ir_curioso" else out["APRENDE 16-20"]["por_eleccion"][k][0], out["APRENDE 16-20"]["por_eleccion"][k][1]] for k in ELS}
    json.dump(por_vida, open(os.path.join(AQUI, "P7_28_bloqueos.json"), "w"), indent=0)

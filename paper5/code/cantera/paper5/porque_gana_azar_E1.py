"""[P5-3D · D4] Por que renglon gana el azar con D1+D2. Solo medir."""
import collections, copy, glob, json, os, random, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B, banco_forma3 as BF, forma as F, proyeccion as P

D.A = V42
U.pon(False)
fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                   "*-policy_agent_1*.art.log")))
idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
rnd_az = random.Random(20260919)
baja = collections.Counter()
sube = collections.Counter()
ej = []
n = 0
for orden, i in enumerate(idx, 1):
    f = fs[i]
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        continue
    B.pon_v42(B.interruptores(recs))
    filas_m = list(sm["filas"])
    mundo = U.mundo_de(pc, filas_m, cat["items"])
    tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
    vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
    vivo = {r["tick"] for r in vivos}
    pos_t = {r["tick"]: tuple(r.get("pos") or ()) for r in vivos}
    mri = {r["tick"]: (r.get("move_ready_in") or 0) for r in vivos}
    d_t = {}
    for r in vivos:
        R = r.get("RADIOGRAFIA") or {}
        c = (R.get("candidatos") or {}).get(R.get("elegido"))
        d_t[r["tick"]] = (c.get("d") if isinstance(c, dict) else c)
    esc = [r["tick"] for r in vivos if r["tick"] >= 300 and r["tick"] % 50 == 0]
    nec = set(esc) | {u for t in esc for u in range(t, t + 101)
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
        t2 = t + 100
        if not (t2 in vivo and d_t.get(t2) is not None
                and d_t.get(t) is not None and d_t[t2] < d_t[t]):
            continue
        tr_d = BF.tramos_reales(tk, t, 100)
        pasos = F.cheb(pos_t[t], tr_d[-1]["destino"])
        z = BF.casilla_a(filas_m, pos_t[t], max(1, pasos), rnd_az)
        if not z:
            continue
        w = next((u for u in range(t, t + 101)
                  if u in vivo and mri.get(u, 1) == 0), None)
        if w is None or w not in ctxs:
            continue
        rw, ow, memw, blw = ctxs[w]
        ew = P.estado_de(rw)
        suelow = {tuple(it["pos"]): it for it in (rw.get("ve_items") or [])
                  if it.get("pos")}
        piso = F.pisos_de(ow, mundo, memw, w)
        tramos = [{"destino": tuple(z), "intencion": "ir"},
                  {"destino": None, "intencion": "esperar",
                   "esperar": max(0, 100 - F.cheb(pos_t[t], z) * P.PASO_TICS)}]
        pcs = F.puntos_de_control(ew, tramos)
        tics = [x[0] for x in pcs]
        cf = F.curva_rapida(ew, ow, tramos, mundo, memw, suelow, None, piso)
        base = list(D.candidatos(ow, mundo, copy.deepcopy(memw), w,
                                 copy.deepcopy(blw)))
        cs, quien, sv, ncd, mv = F.mejor_propia3(ew, ow, base, tics, mundo,
                                                 memw, suelow, w, pisos=piso)
        if cs is None:
            continue
        ver, ar, dt = F.juzga_margen(cf, cs, w, margen=0.0)
        if ver != "ok":
            continue
        n += 1
        pts = dt.get("puntos") or []
        if not pts:
            continue
        j = pts.index(max(pts, key=lambda x: x["gana"]))
        tic = pts[j]["tic"]
        # las filas de las dos curvas en ese punto
        def filas_en(curva, idx_):
            e = curva[idx_]
            oo = F.foto_proyectada(ow, {"tick": tic, "pos": e["pos"],
                                        "hp": e["vida"],
                                        "hand": ew.get("hand"),
                                        "body": ew.get("body"),
                                        "pack": ew.get("pack"),
                                        "effects": [],
                                        "move_ready_in": 0,
                                        "attack_ready_in": 0},
                                   mundo, tic, list(suelow.values()))
            F_ = V42.filas(oo, mundo, memw, tic) or {}
            # [E4 arreglo] hay que mirar las filas CON EL PISO PUESTO, que son
            # las que entran en la `d`. Sin esto se reportaban filas que el
            # piso impide que bajen, y el diagnostico enganaba.
            # solo las filas de la TABLA: `filas()` trae ademas claves
            # privadas (`_W`, `_botin`...) que no son numeros.
            return {k: (max(float(F_.get(k) or 0.0), piso[k])
                        if k in piso else float(F_.get(k) or 0.0))
                    for k in V42.REPARTO}
        fa = filas_en(cf, j)
        fb = filas_en(cs, j)
        dif = {}
        for k in set(fa) | set(fb):
            if not k.startswith(("F-", "R-", "S-")):
                continue
            v = float(fa.get(k) or 0.0) - float(fb.get(k) or 0.0)
            if abs(v) > 1e-9:
                dif[k] = v
        if dif:
            peor = min(dif, key=lambda k: dif[k])     # la que MAS baja el azar
            baja[peor] += 1
            mejorr = max(dif, key=lambda k: dif[k])
            sube[mejorr] += 1
            if len(ej) < 4:
                ej.append({"diario": os.path.basename(f)[:28], "tic": t,
                           "punto": j + 1, "de": len(pts), "area": round(ar, 4),
                           "baja": {k: round(v, 4) for k, v in
                                    sorted(dif.items(), key=lambda x: x[1])[:3]}})
    del recs, ctxs
    print(f"[{orden}/{len(idx)}] azar aceptadas acumuladas {n}", flush=True)
print(f"\nAZAR ACEPTADO con D1+D2: {n}")
print("la fila que MAS BAJA el azar respecto a la mejor propia, en el punto "
      "donde gana:")
for k, v in baja.most_common(8):
    print(f"   {k:22s} {v:4d} = {100*v/max(1,sum(baja.values())):.1f} %")
print("\nla que MAS SUBE (contra el azar):")
for k, v in sube.most_common(5):
    print(f"   {k:22s} {v:4d}")
print("\nejemplos:")
for e in ej:
    print("  ", json.dumps(e, ensure_ascii=False))
json.dump({"n": n, "baja": dict(baja), "sube": dict(sube), "ejemplos": ej},
          open(os.path.join(AQUI, "P53E_porque_azar2.json"), "w"),
          ensure_ascii=False, indent=1)

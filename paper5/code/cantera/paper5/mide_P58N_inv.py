"""[P5-8N · inversion del punto 3] La fila NO esta instalada. ¿Que haria si lo estuviera?

Sobre los tics FUERA DE FORMA de K (tandas 1 y 2), muestreados con el arnes de
P5-2 (DESDE/CADA), se redecide con la fila ENCENDIDA y APAGADA y se cuenta
cuantas decisiones cambian y hacia donde. Coste cero.
"""
import collections, glob, json, os, sys, time
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U
from serie_util import D, DOV
import banco_llaves as B
import curiosidad as C
from alma import appraisal_zs_v42_exp as V42

CAMBIA = collections.Counter()
DE_A = collections.Counter()
N = 0
t0 = time.time()
for f in sorted(glob.glob("paintball/runs/P58M_t[12]_K_*/*.art.log")):
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        continue
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    herm = pc.get("teammate_slot")
    ctic = {r["tick"]: r.get("activa") for r in recs if r.get("k") == "cur_forma_tic"}
    ojo = C.Ojo(mundo, 8)
    C.CUR.modo, C.CUR.k, C.CUR.balanza, C.CUR.ojo = "frontera", 0.2, True, ojo
    C.CUR.on = True
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    dh = []
    for r in [x for x in recs if x.get("k") == "tick"]:
        t = r["tick"]
        o = DOV.a_obs(r); o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t); ult = r.get("intencion")
        dh.append((t, sum(float(x.get("amount") or 0) if isinstance(x, dict) else 0.0
                          for x in (r.get("damage_taken") or []))))
        if r.get("phase") != "live":
            continue
        p = tuple(r.get("pos") or ())
        if p:
            ojo.mira(p, t)
        if ctic.get(t) is not None or not p:      # solo FUERA de forma
            continue
        if t < B.DESDE or (t - B.DESDE) % B.CADA:
            continue
        import copy as _c
        d100 = sum(v for (tt, v) in dh if 0 <= t - tt < C.VENTANA_DANO)
        am, _ = C.amenaza(r, mundo, herm, d100, t)
        # LO QUE LA POLITICA VIVA RELLENA CADA TIC (policy_forma.py:1355-1358).
        # Sin esto la fila vale 0 SIEMPRE y el contrafactual da un cero falso.
        C.CUR.amenaza_ahora = am
        C.CUR.ign_global = ojo.ignorancia_global()
        C.CUR.dist_frontera = C.dist_a_frontera(ojo, mundo)
        try:
            C.desinstala()
            a0, r0 = D.decide(o, mundo, _c.deepcopy(mem), t, _c.deepcopy(blo))
            C.instala()
            a1, r1 = D.decide(o, mundo, _c.deepcopy(mem), t, _c.deepcopy(blo))
        except Exception:
            C.desinstala(); continue
        finally:
            C.desinstala()
        e0, e1 = r0.get("elegido"), r1.get("elegido")
        N += 1
        if e0 != e1:
            CAMBIA["cambia"] += 1
            DE_A[(str(e0), str(e1))] += 1
            if str(e0) == "ir_botin":
                CAMBIA["pierde_ir_botin"] += 1
            if str(e1) == "ir_botin":
                CAMBIA["gana_ir_botin"] += 1
        else:
            CAMBIA["igual"] += 1
    print(f"  {os.path.basename(os.path.dirname(f))}: acumulado {N} decisiones "
          f"· cambian {CAMBIA['cambia']} · la fila valorada {C.CUR.n_valor} veces, "
          f"con M>0 {C.CUR.n_valor_pos}, max M {C.CUR.max_M:.5f}", flush=True)

print(f"\n=== LA FILA, ENCENDIDA EN SECO, FUERA DE FORMA ({N} decisiones muestreadas) ===")
print(f"  cambian de ganador : {CAMBIA['cambia']} = {100.0*CAMBIA['cambia']/max(N,1):.2f}%")
print(f"  DEJAN de ganar ir_botin por la fila : {CAMBIA['pierde_ir_botin']}")
print(f"  PASAN a ganar ir_botin por la fila  : {CAMBIA['gana_ir_botin']}")
print("  los diez cambios mas frecuentes (sin fila -> con fila):")
for (a, b), n in DE_A.most_common(10):
    print(f"    {a:16s} -> {b:16s} {n}")
print(f"  CONTROL de que la fila SE ENCIENDE: valorada {C.CUR.n_valor} veces · "
      f"con M>0 {C.CUR.n_valor_pos} · M maximo {C.CUR.max_M:.5f}")
assert C.CUR.n_valor_pos > 0, "LA FILA NUNCA VALE NADA: el cero seria mio, no del mundo"
print(f"  {time.time()-t0:.0f} s")

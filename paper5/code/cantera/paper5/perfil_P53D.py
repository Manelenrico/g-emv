"""[P5-3D · D5] Donde se van los milisegundos. Solo medir, sin optimizar."""
import cProfile, copy, glob, io, os, pstats, random, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B, banco_forma3 as BF, forma as F, proyeccion as P

N = 200
D.A = V42
U.pon(False)
fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                   "*-policy_agent_1*.art.log")))
idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))
casos = []
for i in idx:
    if len(casos) >= N:
        break
    f = fs[i]
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        continue
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    tk = {r["tick"]: r for r in recs if r.get("k") == "tick"}
    vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
    vivo = {r["tick"] for r in vivos}
    mri = {r["tick"]: (r.get("move_ready_in") or 0) for r in vivos}
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
        if mri.get(t, 1) != 0 or t < 300 or t % 50 or len(casos) >= N:
            continue
        tramos = BF.tramos_reales(tk, t, 100)
        if not tramos:
            continue
        e0 = P.estado_de(r)
        suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
                 if it.get("pos")}
        casos.append((e0, o, tramos, mundo, pre, suelo, blo, t))
    del recs
print(f"casos: {len(casos)}")


def una(c):
    e0, o, tramos, mundo, pre, suelo, blo, t = c
    pcs = F.puntos_de_control(e0, tramos)
    tics = [x[0] for x in pcs]
    F.curva_multi(e0, o, tramos, mundo, pre, suelo, None)
    base = list(D.candidatos(o, mundo, copy.deepcopy(pre), t,
                             copy.deepcopy(blo)))
    F.mejor_propia2(e0, o, base, tics, mundo, pre, suelo, t)
    return len(tics), len(base)


pr = cProfile.Profile()
pr.enable()
puntos = cand = 0
for c in casos:
    a, b = una(c)
    puntos += a; cand += b
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(16)
txt = s.getvalue()
print(txt[:3600])
print(f"\npuntos de control por decision: {puntos/len(casos):.2f} · "
      f"candidatos por decision: {cand/len(casos):.1f}")
# cronometraje por pieza
def crono(fn, n=len(casos)):
    t0 = time.perf_counter()
    for c in casos:
        fn(c)
    return (time.perf_counter() - t0) / n * 1000.0
solo_proj = crono(lambda c: P.proyectar(c[0], {"destino": c[2][0].get("destino"),
                                               "coger": False, "usar": None},
                                        25, c[3], c[5]))
solo_foto = crono(lambda c: F.foto_proyectada(c[1], c[0], c[3], c[7] + 25,
                                              list(c[5].values())))
solo_tabla = crono(lambda c: V42.appraise(c[1], c[3], c[4], c[7]))
solo_cand = crono(lambda c: list(D.candidatos(c[1], c[3],
                                              copy.deepcopy(c[4]), c[7],
                                              copy.deepcopy(c[6]))))
print(f"\npor pieza, ms por llamada:")
print(f"  proyectar 25 tics : {solo_proj:7.3f}")
print(f"  construir la foto : {solo_foto:7.3f}")
print(f"  llamar a la tabla : {solo_tabla:7.3f}")
print(f"  D.candidatos      : {solo_cand:7.3f}")

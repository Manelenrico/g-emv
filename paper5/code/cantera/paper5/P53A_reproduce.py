"""[P5-3A] El arnes sigue reproduciendo, con `proyeccion` IMPORTADA.

`proyeccion.py` no toca al decisor ni a la tabla: solo importa `riqueza_W`.
Esto lo comprueba en vivo sobre los primeros diarios de la seleccion.
"""
import copy, glob, os, random, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U
from serie_util import D, DOV
from alma import appraisal_zs_v42_exp as V42
import banco_llaves as B
import proyeccion as P                    # <- la proyeccion, importada

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
D.A = V42
U.pon(False)
fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_A",
                                   "*-policy_agent_1*.art.log")))
idx = sorted(random.Random(B.SEMILLA).sample(range(len(fs)), 40))[:N]
ok = tot = 0
for k, i in enumerate(idx, 1):
    recs = list(U.lee(fs[i]))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    for r in [x for x in recs if x.get("k") == "tick"]:
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t)
        blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        if r.get("phase") != "live":
            continue
        pre = copy.deepcopy(mem)
        _in = (r.get("intencion") or {}).get("do")
        _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
        if _in == "attack" or _el.startswith("atacar"):
            mem.ultimo_ataque = t
        elif _el.startswith("soltar_"):
            mem.cedidos[tuple(r.get("pos") or ())] = {
                "item": {"id": _el[len("soltar_"):], "n": 1}, "tick": t}
        ctx = {"o": o, "mundo": mundo, "mem": pre, "blo": blo, "tick": t, "r": r}
        det = B.decide_v42(ctx)
        tot += 1
        ok += U.verificado(ctx, det)
    print(f"[{k}/{N}] {ok:,}/{tot:,} = {100*ok/max(1,tot):.2f} %", flush=True)
print(f"\nREPRODUCCION CON LA PROYECCION IMPORTADA: {ok:,}/{tot:,} = "
      f"{100*ok/max(1,tot):.2f} %")

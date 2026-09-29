"""[P5-5B · puerta de calidad] ¿Arma mi banco el MISMO relato que el campo?

En seco, coste cero. Antes de pagar una sola llamada hay que saber que el texto
que voy a mandar es el que el consejero del cuatro habria recibido.

Los diarios del brazo C guardan, en cada `cortex_llamada`, el `relato_md5` del
texto que DE VERDAD se mando. Aqui reconstruyo el relato en ese mismo tic con
mi `escena_ctx` + `relator_t5.relato(e, True)` y comparo los md5. Si no cuadra
byte a byte, el banco no sale.
"""
from __future__ import annotations
import copy, glob, hashlib, json, os, sys

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, AQUI)
import serie_util as U                                      # noqa: E402
from serie_util import D, DOV                               # noqa: E402
from alma import appraisal_zs_v42_exp as V42                # noqa: E402
from alma import relator_t5 as RT                           # noqa: E402
import banco_llaves as B                                    # noqa: E402
from escenas_P55B import escena_ctx                         # noqa: E402

N_DIARIOS = int(os.environ.get("N", "12"))


def main():
    D.A = V42
    U.pon(False)
    fs = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "S2_C",
                                       "*-policy_agent_1*.art.log")))[:N_DIARIOS]
    ok = mal = sin = 0
    ejemplos = []
    for n, f in enumerate(fs, 1):
        recs = list(U.lee(f))
        pc = next((r for r in recs if r.get("k") == "player_config"), None)
        sm = next((r for r in recs if r.get("k") == "static_map"), None)
        cat = next((r for r in recs if r.get("k") == "catalogo"), None)
        if not (pc and sm and cat):
            continue
        B.pon_v42(B.interruptores(recs))
        mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        herm = pc.get("teammate_slot")
        quiero = {r["tick"]: r["relato_md5"] for r in recs
                  if r.get("k") == "cortex_llamada" and r.get("ok")
                  and r.get("relato_md5")}
        mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
        for r in [x for x in recs if x.get("k") == "tick"]:
            t = r["tick"]
            o = DOV.a_obs(r)
            o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
            mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t)
            ult = r.get("intencion")
            if r.get("phase") != "live":
                continue
            _el = (r.get("RADIOGRAFIA") or {}).get("elegido") or ""
            if os.environ.get("POST"):        # variante: memoria POST-ataque
                if (r.get("intencion") or {}).get("do") == "attack" \
                        or _el.startswith("atacar"):
                    mem.ultimo_ataque = t
                pre = copy.deepcopy(mem)
            else:
                pre = copy.deepcopy(mem)
                if (r.get("intencion") or {}).get("do") == "attack" \
                        or _el.startswith("atacar"):
                    mem.ultimo_ataque = t
            if t not in quiero:
                continue
            try:
                e = escena_ctx(r, o, pre, copy.deepcopy(blo), mundo, t, herm)
                txt = RT.relato(e, True)
            except Exception as ex:
                sin += 1
                if len(ejemplos) < 5:
                    ejemplos.append((os.path.basename(f)[:20], t, f"EXCEPCION {ex}"))
                continue
            h = hashlib.md5(txt.encode()).hexdigest()
            if h == quiero[t]:
                ok += 1
            else:
                mal += 1
                if len(ejemplos) < 5:
                    ejemplos.append((os.path.basename(f)[:20], t,
                                     f"md5 {h[:10]} != {quiero[t][:10]}"))
        print(f"[{n}/{len(fs)}] {os.path.basename(f)[:26]} · "
              f"ok {ok} · mal {mal} · error {sin}", flush=True)
        del recs
    tot = ok + mal + sin
    print(f"\nRELATOS RECONSTRUIDOS BYTE A BYTE: {ok}/{tot} = "
          f"{ok/tot*100:.2f}%" if tot else "sin llamadas")
    if ejemplos:
        print("ejemplos que no cuadran:")
        for x in ejemplos:
            print("  ", x)


if __name__ == "__main__":
    main()

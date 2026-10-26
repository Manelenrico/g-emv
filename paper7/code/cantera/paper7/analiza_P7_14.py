"""[P7-14] LECTURA DE LOS DIARIOS DEL SEGUNDO CAMPO (paintball/runs/P714_s<S>_d<D>_<BRAZO>_<semilla>/, fuera de git), con las definiciones de
`analiza_P7_11.py` (usos, regalos y su destino, el tiempo con el candidato en curso, los 10 segundos antes de morir: se importan, no se copian)
y, ademas, los PEDIDOS (registro `P7_pido` de cada parte emitido):
  - pedidos abiertos (un parte con pedido tras uno sin el) y cerrados (un parte sin pedido tras uno con el), con el motivo que apunta el emisor
    ("lo lleva", "lo ve", "ya no le alivia (promesa 0)");
  - un cierre es PORQUE SE LO DIERON si entre el parte anterior y el del cierre (los `parte.CADA` tics de un parte al siguiente, o ese mismo tic)
    el hermano ejecuto un regalo de botiquin; si no, la criatura lo encontro o dejo de quererlo;
  - cada regalo es CON PEDIDO si el ultimo parte del hermano emitido antes de la decision, con edad <= `parte.CADUCIDAD`, llevaba el pedido.
  python3 analiza_P7_14.py [--freno]   -> P7_14_vidas.json   (--freno: solo APRENDE serie 1 dias 1-3, y la condicion (b) por pantalla)"""
import glob, json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "paintball"), RAIZ): sys.path.insert(0, p)
import analiza_P7_11 as A11
from alma import parte as PARTE
def pidos(f):
    P = []; arr = None; err = 0
    for line in open(f):
        if '"P7_pido"' in line[:20]: P.append(json.loads(line))
        elif '"P7_arranque"' in line[:22]: arr = json.loads(line)
        elif '"P7_error"' in line[:20]: err += 1
    return P, arr, err
def un_partido(carp):
    b = os.path.basename(carp); _, s_, d_, brazo, sem = b.split("_"); serie = int(s_[1:]); dia = int(d_[1:]); out = {}
    campo = json.load(open(os.path.join(AQUI, "P7_14_campo.json"))) if os.path.exists(os.path.join(AQUI, "P7_14_campo.json")) else {}
    F = {sl: glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log")) for sl in (10, 11)}
    L = {sl: (A11.lee(F[sl][0]) if F[sl] else (None, [])) for sl in (10, 11)}; X = {sl: (pidos(F[sl][0]) if F[sl] else ([], None, 0)) for sl in (10, 11)}
    for sl in (10, 11):
        M, T = L[sl]; Mh, Th = L[21 - sl]
        if not T: continue
        k = f"s{serie}_d{dia}_{brazo}_{sl}"; v = A11.una_vida(M, T, Mh, Th, campo.get(k)); P, arr, err = X[sl]; Ph = X[21 - sl][0]
        reg_h = A11.eventos(Mh, Th)[1] if Th else []; mis = [c for c in A11.eventos(M, T)[0] if c["kit"]]
        v["coge_botiquines_que_solto_el_hermano"] = sum(1 for c in mis if any(g["pos"] == c["pos"] and g["t"] < c["t"] for g in reg_h))
        cierres = [{"tick": p["tick"], "motivo": p["cierra"], "porque_se_lo_dieron": any(p["tick"] - PARTE.CADA < g["t"] <= p["tick"] for g in reg_h)} for p in P if p.get("cierra")]
        for g in v["regala"]:
            ult = [p for p in Ph if p["tick"] < g["t_dec"] and g["t_dec"] - p["tick"] <= PARTE.CADUCIDAD]
            g["con_pedido"] = bool(ult and ult[-1]["pide"])
        out[k] = {"serie": serie, "dia": dia, "brazo": brazo, "slot": sl, "semilla": int(sem), **v,
                  "pide_encendido": ((arr or {}).get("pide") or {}).get("PIDE"), "ojos": None, "errores_P7": err, "partes": len(P), "partes_con_pedido": sum(1 for p in P if p["pide"]), "largo_max_parte": max((p["largo"] for p in P), default=None),
                  "pedidos_abiertos": sum(1 for p in P if p["abre"]), "cierres": cierres, "pedido_abierto_al_final": bool(P and P[-1]["pide"]), "regalos_con_pedido": sum(1 for g in v["regala"] if g["con_pedido"])}
    return out
if __name__ == "__main__":
    pat = "P714_s1_d[123]_APRENDE_*" if "--freno" in sys.argv else "P714_s*_d*_*_*"
    carps = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))); OUT = {}
    with Pool(8) as P:
        for o in P.imap_unordered(un_partido, carps): OUT.update(o)
    if "--freno" in sys.argv:
        ab = sum(v["pedidos_abiertos"] for v in OUT.values()); reg = sum(v["regala_n"] for v in OUT.values()); sin = sum(v["regala_n"] - v["regalos_con_pedido"] for v in OUT.values())
        print(json.dumps({"vidas": len(OUT), "pide_encendido_en_todas": all(v["pide_encendido"] for v in OUT.values()), "errores_P7": sum(v["errores_P7"] for v in OUT.values()), "pedidos_abiertos": ab, "regalos": reg, "regalos_sin_pedido": sin, "b_pasa": bool(ab > 0 and sin == 0)}, ensure_ascii=False))
    else:
        json.dump(dict(sorted(OUT.items())), open(os.path.join(AQUI, "P7_14_vidas.json"), "w"), ensure_ascii=False, indent=0); print("vidas", len(OUT))

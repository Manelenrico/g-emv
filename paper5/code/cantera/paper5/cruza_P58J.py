"""[P5-8J] EL CRUCE: la puerta de una imagen juzgando los nacimientos de otra.

  python3 cantera/paper5/cruza_P58J.py --codigo E --diarios E
  python3 cantera/paper5/cruza_P58J.py --codigo H --diarios E
  python3 cantera/paper5/cruza_P58J.py --codigo E --diarios I
  python3 cantera/paper5/cruza_P58J.py --codigo H --diarios I

Replica `AlmaForma._juzga` FUERA del bicho: mismo `_contexto`, mismo
`con_renglon`, mismo `FV.evalua`, mismo margen (leido del diario, no cableado).
El codigo de la puerta se toma de los ficheros SACADOS DE LA IMAGEN.
"""
import collections, copy, glob, json, os, sys, time

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # [Zenodo: ruta personal sustituida]
SCR = os.environ.get("P58J_SCRATCH", os.path.join(RAIZ, "_P58J_tmp"))  # [Zenodo: ruta de sesion sustituida]
CODIGO = sys.argv[sys.argv.index("--codigo") + 1]
DIARIOS = sys.argv[sys.argv.index("--diarios") + 1]
TOPE = int(sys.argv[sys.argv.index("--tope") + 1]) if "--tope" in sys.argv else 0

# EL CODIGO DE LA PUERTA, de la imagen elegida, DELANTE de todo
sys.path.insert(0, os.path.join(SCR, CODIGO))
sys.path.insert(1, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(2, os.path.join(RAIZ, "cantera", "paper5"))

import serie_util as U
from serie_util import D, DOV
import banco_llaves as B
import proyeccion as P
import forma as F
import forma_viva as FV
import curiosidad as C
import curiosidad_forma as CFM
from alma import appraisal_zs_v42_exp as V42

# ── de donde sale cada modulo: se IMPRIME, no se supone ──
print(f"### codigo {CODIGO} · diarios {DIARIOS} ###")
for m in (P, F, FV, C, CFM, D):
    print(f"    {m.__name__:24s} {m.__file__}")

PAT = {"E": "P58E_t1_K_*", "I": "P58I_t1_K_*", "H": "P58H_t1_K_*"}[DIARIOS]


def un_asiento(f):
    recs = list(U.lee(f))
    pc = next((r for r in recs if r.get("k") == "player_config"), None)
    sm = next((r for r in recs if r.get("k") == "static_map"), None)
    cat = next((r for r in recs if r.get("k") == "catalogo"), None)
    if not (pc and sm and cat):
        return None
    B.pon_v42(B.interruptores(recs))
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    herm = pc.get("teammate_slot")
    ojo = C.Ojo(mundo, 8)
    mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
    # los nacimientos y lo que la puerta VIVA dijo de cada uno
    prop = {r["tick"]: r for r in recs
            if r.get("k") == "forma_propuesta" and r.get("origen") == "curiosidad"}
    ev = {r["id"]: r for r in recs if r.get("k") == "forma_evaluada"}
    dano_hist, out = [], []
    for r in [x for x in recs if x.get("k") == "tick"]:
        t = r["tick"]
        o = DOV.a_obs(r)
        o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
        mem.observa(o, mundo, t)
        blo.actualiza(o, mundo, ult, t)
        ult = r.get("intencion")
        dano_hist.append((t, sum(float(x.get("amount") or 0)
                                 if isinstance(x, dict) else 0.0
                                 for x in (r.get("damage_taken") or []))))
        if r.get("phase") != "live":
            continue
        pos = tuple(r.get("pos") or ())
        if pos:
            ojo.mira(pos, t)
        if t not in prop or not pos:
            continue
        p0 = prop[t]
        pre = copy.deepcopy(mem)
        d100 = sum(v for (tt, v) in dano_hist if t - tt < C.VENTANA_DANO)
        am, _ = C.amenaza(r, mundo, herm, d100, t)
        arms = CFM.armados(r, mundo, herm)
        cam, dist, dest = CFM.camino_a_frontera(ojo, mundo, pos, arms)
        if dest is None:
            out.append({"tick": t, "id": p0["id"], "ver": "sin frontera",
                        "ar": None, "dest_ok": False}); continue
        dest_ok = (list(dest) == list(p0.get("destino") or []))
        tramos = [{"destino": list(dest), "intencion": "ver", "esperar": 0}]
        fv = FV.FormaViva(p0["id"], tramos, t, origen="curiosidad")
        # ── _contexto, tal cual ──
        rec = {"tick": t, "pos": r.get("pos"), "hp": r.get("hp"),
               "hand": r.get("hand"), "body": r.get("body"),
               "pack": r.get("pack"), "effects": r.get("effects"),
               "move_ready_in": r.get("move_ready_in"),
               "attack_ready_in": r.get("attack_ready_in") or 0}
        e0 = P.estado_de(rec)
        suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or [])
                 if it.get("pos")}
        pisos = F.pisos_rival(o, mundo, pre, t)
        tics = [x[0] for x in F.puntos_de_control(e0, tramos)]
        FV.pon_base(lambda oo, mu, me, tk, _b=blo:
                    list(D.candidatos(oo, mu, copy.deepcopy(me), tk,
                                      copy.deepcopy(_b))))
        # EL MARGEN: el que la puerta VIVA uso en ese tic, leido del diario
        mg = (ev.get(p0["id"]) or {}).get("margen")
        if mg is None:
            continue
        _orig, _p = CFM.con_renglon(ojo, mundo, cam, tics, t, am)
        k_f = k_s = None; quien = None
        try:
            ver, ar, cf, tks = FV.evalua(fv, F, e0, o, mundo, pre, suelo,
                                         herm, None, pisos, mg, t)
            # [P5-8J] los DOS costes por separado: la forma y el mejor propio
            try:
                _cf = F.curva_H(e0, o, tramos, mundo, pre, suelo, tics,
                                herm, None, pisos)
                _cs, quien, _n, _mv = F.mejor_propia_H(
                    e0, o, list(D.candidatos(o, mundo, copy.deepcopy(pre), t,
                                             copy.deepcopy(blo))),
                    tics, mundo, pre, suelo, t, herm, None, pisos)
                k_f = round(F.coste(_cf, t), 5)
                k_s = round(F.coste(_cs, t), 5) if _cs else None
            except Exception:
                pass
        finally:
            CFM.restaura(_orig)
        out.append({"k_forma": k_f, "k_solo": k_s, "quien": quien,
                    "tick": t, "id": p0["id"], "ver": ver,
                    "ar": (round(ar, 5) if ar is not None else None),
                    "margen": mg, "dest_ok": dest_ok,
                    "vivo_ver": (ev.get(p0["id"]) or {}).get("veredicto"),
                    "vivo_ar": (ev.get(p0["id"]) or {}).get("ventaja")})
        if TOPE and len(out) >= TOPE:
            break
    return out


TODO = {}
t0 = time.time()
for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", PAT,
                                        "*.art.log"))):
    nom = (os.path.basename(os.path.dirname(f)).split("_")[3] + "/"
           + f.rsplit("_", 1)[1][:2])
    o = un_asiento(f)
    if not o:
        continue
    TODO[nom] = o
    ok = sum(1 for x in o if x["ver"] == "ok")
    vok = sum(1 for x in o if x["vivo_ver"] == "ok")
    ig = sum(1 for x in o if x["ver"] == x["vivo_ver"])
    print(f"  {nom:14s} {len(o):4d} juzgadas · SECO {ok:3d} ok · "
          f"VIVO {vok:3d} ok · mismo veredicto {ig}/{len(o)} "
          f"· destino igual {sum(1 for x in o if x['dest_ok'])}/{len(o)}",
          flush=True)

n = sum(len(v) for v in TODO.values())
ok = sum(1 for v in TODO.values() for x in v if x["ver"] == "ok")
vok = sum(1 for v in TODO.values() for x in v if x["vivo_ver"] == "ok")
ig = sum(1 for v in TODO.values() for x in v if x["ver"] == x["vivo_ver"])
print(f"\n### codigo {CODIGO} sobre diarios {DIARIOS}: {n} juzgadas · "
      f"SECO {ok} ok ({100.0*ok/max(n,1):.1f}%) · VIVO {vok} ok "
      f"({100.0*vok/max(n,1):.1f}%) · mismo veredicto {ig}/{n} "
      f"({100.0*ig/max(n,1):.1f}%) · {time.time()-t0:.0f} s")
json.dump(TODO, open(f"{RAIZ}/cantera/paper5/P58J_cruce_{CODIGO}{DIARIOS}.json",
                     "w"), ensure_ascii=False)

"""[P5-FIG · 2] Las tres curvas de un plan real. SOLO LECTURA, coste cero."""
import copy, glob, json, os, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U
from serie_util import D, DOV
import banco_llaves as B
import proyeccion as P, forma as F
from alma import appraisal_zs_v42_exp as V42

CARP, SLOT, FID = "P56C_*_F_22250767", "10", 7
f = sorted(glob.glob(f"paintball/runs/{CARP}/*policy_agent_{SLOT}*.art.log"))[0]
recs = list(U.lee(f))
pc = next(r for r in recs if r.get("k") == "player_config")
sm = next(r for r in recs if r.get("k") == "static_map")
cat = next(r for r in recs if r.get("k") == "catalogo")
B.pon_v42(B.interruptores(recs))
mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
herm = pc.get("teammate_slot")

acep = next(r for r in recs if r.get("k") == "forma_aceptada" and r.get("id") == FID)
caida = next((r for r in recs if r.get("k") == "forma_caida" and r.get("id") == FID), None)
conf = [r for r in recs if r.get("k") == "confianza" and r.get("id") == FID]
t0 = acep["tick"]
T_JUZGA = acep.get("nace") or t0          # la puerta juzga con el estado de NACER
tramos = acep["tramos"]
print(f"forma {FID} de {os.path.basename(os.path.dirname(f))}/{SLOT}")
print(f"  aceptada en el tic {t0} · ventaja registrada {acep['ventaja']}")
print(f"  tramos: {json.dumps(tramos)}")
print(f"  puntos de control registrados: {acep['tics']}")
print(f"  caida: {caida.get('tick') if caida else '—'} · {str((caida or {}).get('motivo'))[:40]}")

vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
por_tic = {r["tick"]: r for r in vivos}
mem, blo, ult = V42.Memoria(), D.Bloqueos(), None
e0 = suelo = pisos = None
for r in [x for x in recs if x.get("k") == "tick"]:
    t = r["tick"]
    o = DOV.a_obs(r); o["you"]["attack_ready_in"] = r.get("attack_ready_in") or 0
    mem.observa(o, mundo, t); blo.actualiza(o, mundo, ult, t); ult = r.get("intencion")
    if r.get("phase") != "live":
        continue
    if t == T_JUZGA:
        pre = copy.deepcopy(mem)
        rec = {"tick": t, "pos": r.get("pos"), "hp": r.get("hp"),
               "hand": r.get("hand"), "body": r.get("body"), "pack": r.get("pack"),
               "effects": r.get("effects"), "move_ready_in": r.get("move_ready_in"),
               "attack_ready_in": r.get("attack_ready_in") or 0}
        e0 = P.estado_de(rec)
        suelo = {tuple(it["pos"]): it for it in (r.get("ve_items") or []) if it.get("pos")}
        pisos = F.pisos_rival(o, mundo, pre, t)
        obs0, mem0, blo0 = o, pre, copy.deepcopy(blo)
        break

tics = [x[0] for x in F.puntos_de_control(e0, tramos)]
cf = F.curva_H(e0, obs0, tramos, mundo, mem0, suelo, tics, herm, None, pisos)
base = list(D.candidatos(obs0, mundo, copy.deepcopy(mem0), T_JUZGA, copy.deepcopy(blo0)))
cs, quien, ncd, mueve = F.mejor_propia_H(e0, obs0, base, tics, mundo, mem0, suelo,
                                         T_JUZGA, herm, None, pisos)
ar, det = F.area(cf, cs, T_JUZGA)

print(f"\n  puntos de control recalculados: {tics}   (registrados {acep['tics']})")
print(f"  VENTAJA recalculada {ar:.5f}  ·  registrada {acep['ventaja']}   "
      f"-> {'CUADRA' if abs(ar-acep['ventaja'])<0.002 else 'NO CUADRA'}")
print(f"  el mejor propio es «{quien}» entre {ncd} candidatos")

real = []
for t in tics:
    r = por_tic.get(t)
    real.append((r.get("RADIOGRAFIA") or {}).get("d_ahora") if r else None)
print("\n  punto |  tic  | plan proyectado | solo proyectado | lo que pasó | registrado")
for i, t in enumerate(tics):
    dp = next((c.get("d_proyectada") for c in conf if c.get("punto") == i), None)
    dr = next((c.get("d_real") for c in conf if c.get("punto") == i), None)
    print(f"   {i:4d}  | {t:5d} | {cf[i]['d']:15.5f} | {cs[i]['d']:15.5f} | "
          f"{str(real[i]):>11s} | {str(dp)} / {str(dr)}")

json.dump({"asiento": f"{os.path.basename(os.path.dirname(f))}/{SLOT}", "id": FID,
           "t0": t0, "tics": tics, "tramos": tramos,
           "cf": [c["d"] for c in cf], "cs": [c["d"] for c in cs],
           "real": real, "ventaja": ar, "ventaja_log": acep["ventaja"],
           "mejor_propio": quien,
           "conf": [{"punto": c["punto"], "d_real": c["d_real"],
                     "d_proy": c["d_proyectada"], "veredicto": c["veredicto"]}
                    for c in conf],
           "caida": {"tick": (caida or {}).get("tick"),
                     "motivo": (caida or {}).get("motivo")},
           "diario": f},
          open("cantera/paper5/FIG2_datos.json", "w"), ensure_ascii=False, indent=1)
print("\n  -> cantera/paper5/FIG2_datos.json")

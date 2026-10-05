"""[P6-30] Diagnostico de la infidelidad RESIDUAL (sin fuga): replica una vida con el molde de P6-29 (`mide_P6_29.vida`, un proceso)
y en cada tic en desacuerdo compara lo que eligio el cuerpo en el campo (`elegido_cuerpo`, con sus candidatos y d en RADIOGRAFIA)
con lo que eligio la replica (y sus d).    python3 residuo_P6_30.py CARPETA SLOT BRAZO   -> residuo_<carpeta>_<slot>.json"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); carp, slot, brazo = sys.argv[1], int(sys.argv[2]), sys.argv[3]; sys.argv = ["x"]
import mide_P6_29 as M
import serie_util as U
r = M.vida(carp, slot, brazo); R = M.HOOK["reg"]; D = set(r["desacuerdos"])
f = glob.glob(os.path.join(M.RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]; out = []
for rec in U.lee(f):
    if rec.get("k") == "tick" and rec["tick"] in D:
        ra = rec.get("RADIOGRAFIA") or {}; cds = {k: (x["d"] if isinstance(x, dict) else x) for k, x in (ra.get("candidatos") or {}).items()}
        rp = R.get(rec["tick"]) or {}
        out.append({"t": rec["tick"], "diario_cuerpo": ra.get("elegido_cuerpo"), "diario_ejecutado": ra.get("elegido"), "replica": rp.get("el"), "spread_diario": ra.get("spread"),
                    "diario_cands": sorted(cds.items(), key=lambda kv: kv[1])[:5], "replica_cands": sorted((rp.get("cds") or {}).items(), key=lambda kv: kv[1])[:5],
                    "solo_en_diario": sorted(set(cds) - set(rp.get("cds") or {})), "solo_en_replica": sorted(set(rp.get("cds") or {}) - set(cds)), "move_ready_in": rec.get("move_ready_in"), "action_result": rec.get("action_result")})
json.dump({"vida": f"{carp}/{slot}", "brazo": brazo, "fidelidad": r["fidelidad"], "desacuerdos": out}, open(os.path.join(AQUI, f"residuo_{carp}_{slot}.json"), "w"), ensure_ascii=False, indent=1)
print(f"{carp}/{slot}: fidelidad {r['fidelidad']}")
for o in out: print(f"  t{o['t']}: cuerpo={o['diario_cuerpo']} ejec={o['diario_ejecutado']} replica={o['replica']} spread={o['spread_diario']} solo_diario={o['solo_en_diario']} solo_replica={o['solo_en_replica']} | d diario {o['diario_cands'][:3]} | d replica {o['replica_cands'][:3]}")

"""[P5-1 E2] Concilia el 2.014 del paper cuatro con los 7.960 de W >= 3.

El manual del mundo (`manual_del_mundo.md:594-596`) cuenta tics con TRES
condiciones a la vez: R-CARENCIA = 0 (o sea W >= 3), R-ACOPIO = 0 y vida al
maximo. Aqui se reproduce esa cuenta y se separa cada condicion.
"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
from alma.appraisal_zs_v42_exp import riqueza_W             # noqa: E402
CARP = ("S2_A", "S2_B", "S2_C", "S2_Aconf")

c = collections.Counter()
mejor = (0.0, None, None)
for carp in CARP:
    for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", carp,
                                           "*-policy_agent_1*.art.log"))):
        for ln in open(f, encoding="utf-8", errors="replace"):
            if '"ahora"' not in ln:
                continue
            try:
                r = json.loads(ln)
            except Exception:
                continue
            a = (r.get("RADIOGRAFIA") or {}).get("ahora") or {}
            if "W" not in a:
                continue
            W = a["W"]
            fil = a.get("filas") or {}
            car = float((fil.get("R-CARENCIA") or {}).get("M") or 0.0)
            aco = float((fil.get("R-ACOPIO") or {}).get("M") or 0.0)
            hp = r.get("hp")
            c["tics"] += 1
            w3 = W >= 3.0 - 1e-9
            c["W>=3"] += w3
            c["carencia=0"] += (car <= 0.0)
            if w3:
                c["W>=3 y acopio=0"] += (aco <= 0.0)
                c["W>=3 y vida 100"] += (hp == 100)
                if aco <= 0.0 and hp == 100:
                    c["LAS TRES (el 2.014 del cuatro)"] += 1
                    c["suma W de las tres"] += 0
            if W > mejor[0]:
                mejor = (W, os.path.basename(f), r)
print(json.dumps({k: v for k, v in c.items()}, ensure_ascii=False, indent=1))
W, nom, r = mejor
you = {"hand": r.get("hand"), "pack": r.get("pack"), "body": r.get("body")}
print(f"\nLA W MAXIMA: {W} · tic {r['tick']} · {nom}")
print("  mano:", r.get("hand"), "· cuerpo:", r.get("body"),
      "· mochila:", r.get("pack"))

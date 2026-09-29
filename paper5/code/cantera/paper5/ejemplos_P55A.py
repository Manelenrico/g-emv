"""[P5-5A] A5 · cinco ejemplos literales de cada clase, con su comprobacion."""
from __future__ import annotations
import json, os, random, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
random.seed(20260920)

txt = {}
for line in open(f"{AQUI}/P55A_respuestas.jsonl", encoding="utf-8"):
    d = json.loads(line)
    if d["ok"]:
        txt[(d["arm"], d["ereq"], d["asiento"], d["tick_foto"])] = d["props"]

F = json.load(open(f"{AQUI}/P55A_juicio.json"))
por = collections.defaultdict(list)
for f in F:
    for a in f["afs"]:
        por[a["clase"]].append((f, a))

VER = {"ok": "ACIERTO", "mal": "FALLO", "?": "no comprobable"}
for c in ("LLEGADA", "AUSENCIA", "POSICION", "HERMANO"):
    xs = por[c]
    # cinco: procurando que salgan aciertos y fallos
    ok = [x for x in xs if x[1]["ver"] == "ok"]
    mal = [x for x in xs if x[1]["ver"] == "mal"]
    dud = [x for x in xs if x[1]["ver"] == "?"]
    sel = (random.sample(ok, min(3, len(ok))) + random.sample(mal, min(2, len(mal))))
    while len(sel) < 5 and dud:
        sel.append(dud.pop())
    print("#" * 72)
    print(f"## {c}   (n={len(xs)}, aciertos {len(ok)}, fallos {len(mal)}, "
          f"no comprobables {len(dud)})")
    for f, a in sel[:5]:
        ps = txt[(f["arm"], f["ereq"], f["asiento"], f["t0"])]
        frase = None
        for p in ps:
            t = (p["accion"] + " " + p["motivo"])
            import clases_consejo as CC
            if a["trozo"][:18] in CC.llano(t):
                frase = t
                break
        print(f"\n  · [{f['arm']} {f['asiento']} tic {f['t0']}] "
              f"{VER[a['ver']]}  (linea base: {VER[a['base']]})")
        print(f"    trozo que la dispara: «{a['trozo']}»")
        print(f"    literal: {(frase or ' / '.join(p['accion'] for p in ps))[:400]}")
        print(f"    rivales a los que se refiere: {a['obs']}  "
              f"· no trivial: {'si' if a['nuevo'] else 'no'}")

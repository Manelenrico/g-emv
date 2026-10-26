import json, statistics as st
import os; from comun import P7
V=json.load(open(os.path.join(P7,"P7_30_vidas.json")))
V = V.values() if isinstance(V,dict) else V
for b in ("APRENDE","BORRADO"):
  for o in ("racion","botiquin"):
    U=[u for v in V if v.get("brazo")==b for u in (v.get("usos") or {}).get(o,[])]
    comp=[u for u in U if u["completado"]]; am=[u for u in comp if u["al_menos"]]; fi=[u for u in comp if not u["al_menos"]]
    print(b,o,"usos",len(U),"completados",len(comp),"al_menos",len(am),"firmes(no al_menos)",len(fi),
      "hp0 med",st.median([u["hp0"] for u in U]) if U else None,
      "efecto med firmes",round(st.median([u["efecto"] for u in fi]),2) if fi else None,
      "efecto med al_menos",round(st.median([u["efecto"] for u in am]),2) if am else None,
      "hp0 med firmes", st.median([u["hp0"] for u in fi]) if fi else None)

"""[P7-3] Comprobacion de la fuga: tres vidas seguidas en UN proceso, (a) tal cual y (b) restaurando `D.candidatos` y `PC.PARTE.emite`
a su valor base (el de antes de la primera vida) antes de cada `_envuelve`. Corrido a mano el 3-oct-2026: (a) 7/7, 8/8, 160/174;
(b) 7/7, 8/8, 174/174.    python3 fuga_prueba_P7_3.py [restaurar]"""
import collections, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); modo = "restaurar" in sys.argv; sys.argv = ["x"]
import banco_P7_2 as BK
from alma import decisor_zs as D
from alma import policy_cortex as PC
import policy_pareja as PP
BASE_C, BASE_E = D.candidatos, PC.PARTE.emite
T = json.load(open(os.path.join(AQUI, "P7_2_creencias.json"))); por = collections.defaultdict(list)
for e in T: por[(e["carpeta"], e["asiento"])].append(e)
tareas = [(c, s, sorted(v, key=lambda e: e["t"])) for (c, s), v in sorted(por.items())][:3]
if modo:
    _env = PP._envuelve
    def env_limpio(alma):
        D.candidatos, PC.PARTE.emite = BASE_C, BASE_E
        return _env(alma)
    PP._envuelve = env_limpio
for c, s, t in tareas:
    r = BK.vida(c, s, t); print(("restaurando" if modo else "tal cual"), c, s, sum(1 for d in r["decisiones"] if d["fiel"]), "/", len(r["decisiones"]), flush=True)

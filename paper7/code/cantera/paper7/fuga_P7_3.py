"""[P7-3] LA FUGA ENTRE VIDAS: barrido secuencial en UN proceso (el orden del pool de P7-2 con hilos=1), con sondas por vida:
tamano de filas10._CAMPOS, colision de id(mundo) con claves de _CAMPOS de vidas anteriores, y en el primer ataque de cada vida el
parte fresco del hermano, el agresor certificado y los candidatos. Escribe fuga_P7_3.json."""
import collections, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.argv = ["x"]
import banco_P7_2 as BK
from alma import appraisal_zs_v42_exp as A
from alma import decisor_zs as D
import filas10_P6_10 as F10, policy_pareja as PP
T = json.load(open(os.path.join(AQUI, "P7_2_creencias.json"))); por = collections.defaultdict(list)
for e in T: por[(e["carpeta"], e["asiento"])].append(e)
tareas = [(c, s, sorted(v, key=lambda e: e["t"])) for (c, s), v in sorted(por.items())]
SONDA = {}; _d0 = BK._DEC0
def probe(obs, mundo, mem, tick, bloqueos=None):
    if tick in SONDA.get("ts", ()) and tick not in SONDA["hecho"]:
        you = obs.get("you") or {}
        SONDA["hecho"][tick] = {"id_mundo": id(mundo), "parte_fresco": mem.parte_fresco(tick), "agresor_hermana": A.agresor_de_la_hermana(obs, mundo, mem, tick),
                          "agresores_mem": {k: (tick - v["ultimo"]) for k, v in (mem.agresores or {}).items()}, "attack_ready_in": you.get("attack_ready_in"), "hand": you.get("hand"),
                          "candidatos": [c[0] for c in D.candidatos(obs, mundo, mem, tick, None)], "pareja_muerta": mem.pareja_muerta,
                          "visibles": [(a.get("slot"), a.get("pos")) for a in ((obs.get("visible") or {}).get("agents") or [])]}
    return _d0(obs, mundo, mem, tick, bloqueos)
BK._DEC0 = probe
out = []; ids = set()
for i, (c, s, tabla) in enumerate(tareas[:12], 1):
    SONDA.clear(); SONDA["ts"] = {e["t"] for e in tabla if e["objeto"] in ("bow", "blowgun")}; SONDA["hecho"] = {}
    claves_antes = {k[0] for k in F10._CAMPOS}
    r = BK.vida(c, s, tabla); fieles = sum(1 for d in r["decisiones"] if d["fiel"]); H = SONDA.get("hecho") or {}
    infieles = [d for d in r["decisiones"] if not d["fiel"]]
    rec = {"i": i, "vida": f"{c}/{s}", "decisiones": len(r["decisiones"]), "fieles": fieles, "campos_antes": len(claves_antes), "campos_despues": len(F10._CAMPOS),
           "id_mundo_reusado": any(h["id_mundo"] in claves_antes for h in H.values()),
           "infieles": [{"t": d["t"], "diario": d["elegido_diario"], "replica": d["elegido_replica"], "sonda": {k: (str(v)[:200] if k != "candidatos" else v) for k, v in (H.get(d["t"]) or {}).items() if k != "id_mundo"}} for d in infieles[:3]],
           "fiel_ejemplo": [{"t": d["t"], "sonda": {k: (str(v)[:200] if k != "candidatos" else v) for k, v in (H.get(d["t"]) or {}).items() if k != "id_mundo"}} for d in r["decisiones"] if d["fiel"] and d["objeto"] != "botiquin"][:1]}
    out.append(rec); print(json.dumps(rec, ensure_ascii=False)[:600], flush=True)
    json.dump(out, open(os.path.join(AQUI, "fuga_P7_3.json"), "w"), indent=1, ensure_ascii=False)

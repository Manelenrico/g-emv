"""Banco de la base v5 (prompt 18): el tonto y el recolector, con los tres márgenes de comida (5, 15 y 30 %) y los tres niveles de peligro; 20 días, semillas 1-10.
Por partida: vivas, de qué mueren y qué día, de dónde sale lo que comen (cada comida cogida lleva su origen: una clave en el objeto que el mundo no lee),
el almacén al final de cada día, lo que dejan en él, el trabajo en el huerto, el fruto que dan las plantas y lo que aparece en el bosque y la zona salvaje.
   python3 banco_base_v5.py [salida] -> resultados_banco_base_v5.json (prompt 18); con los matorrales (prompt 19): python3 banco_base_v5.py resultados_banco_base_v6.json"""
import collections, json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from mundo import Valle
from jugadores import Mapa, Tonto, Recolector
DIAS = 20; SEMILLAS = range(1, 11); MARGENES = (0.05, 0.15, 0.30); MANDOS = ("bajo", "medio", "alto"); TIPOS = ("tonto", "recolector")


def partida(tipo, margen, mando, semilla, dias=DIAS, registro=None, objetos_cada=0):
    e = Valle(mando=mando, registro=registro, objetos_cada=objetos_cada); e.cfg["dias_por_episodio"] = dias; e.cfg["margen_comida"]["activo"] = margen
    obs, infos = e.reset(seed=semilla); M = Mapa(infos[e.agents[0]]["mapa"])
    J = {a: (Recolector if tipo == "recolector" else Tonto)(a, semilla, M, e.cfg["huerto"]["trabajo_necesario"]) for a in e.agents}
    R = {"come_de": collections.Counter(), "dejar_almacen": 0, "trabajar": 0, "comer": 0, "da_fruto": 0, "frutos_huerto": 0, "duerme_sitio": collections.Counter(), "guardada_dia": [], "turnos_vivos": 0}
    casas = {tuple(c) for v in infos[e.agents[0]]["mapa"]["casas"].values() for c in v["celdas"]}
    _oa = e._actua

    def actua(a, acc):
        org = None
        if acc.get("accion") == "comer":
            i = next((i for i, o in enumerate(e.bolsa[a]) if (acc.get("tipo") is None or o["tipo"] == acc.get("tipo")) and e.cfg["objetos"][o["tipo"]].get("se_come")), None)
            if i is not None and e.bolsa[a][i]["tipo"] == "comida": org = e.bolsa[a][i].get("_origen", "llevaba")
        p0 = tuple(e.pos[a]); r = _oa(a, acc); ok = r.get("resultado") == "ok"
        if ok and acc.get("accion") == "coger" and e.bolsa[a]:
            e.bolsa[a][-1]["_origen"] = ({"planta": "huerto", "almacen": "almacen", "despensa": "despensa"}.get(acc.get("de")) or ("matorral_" + e.matorrales[e.matorral_junto(a)[0]]["zona"] if acc.get("de") == "matorral" and e.matorral_junto(a) else None) or ("suelo_" + e.terreno(p0)))
        if ok and org is not None: R["come_de"][org] += 1; R["comer"] += 1
        if ok and acc.get("accion") == "dejar" and acc.get("en") == "almacen" and r.get("tipo", acc.get("tipo")) == "comida": R["dejar_almacen"] += 1
        if ok and acc.get("accion") == "trabajar": R["trabajar"] += 1
        return r
    e._actua = actua
    while e.agents:
        acts = {a: J[a].actua(obs[a], infos[a]) for a in e.agents}
        R["turnos_vivos"] += len(acts); fase_t = e.fase()
        if e.turno % e.dia_turnos == 0 and e.turno: R["guardada_dia"].append(sum(1 for o in e.almacen if o["tipo"] == "comida") + sum(1 for d in e.despensa.values() for o in d if o["tipo"] == "comida"))
        obs, rew, term, trunc, infos = e.step(acts)
        for a in acts:                                                     # (prompt 22-25) dónde y cuándo duermen: solo el sueño que salió
            if e.cuerpo[a].get("dormida"):
                q = tuple(e.pos[a]); R["duerme_sitio"]["casa" if q in casas else e.terreno(q)] += 1; R.setdefault("duerme_fase", collections.Counter())[fase_t] += 1
        for ev in e._eventos:
            if "da_fruto" in ev: R["da_fruto"] += 1; R["frutos_huerto"] += ev.get("frutos", 0)
    R["muertes"] = [{"criatura": a, "causa": e.cuerpo[a]["causa"], "dia": e.cuerpo[a]["turno_muerte"] // e.dia_turnos, "agotada": e.cuerpo[a]["agotada"]} for a in e.possible_agents if e.cuerpo[a]["muerta"]]
    R["dias_vividos"] = {a: round((e.cuerpo[a]["turno_muerte"] if e.cuerpo[a]["muerta"] else e.turno) / e.dia_turnos, 3) for a in e.possible_agents}
    R["almacen_fin_dia"] = [d["comida"] for d in e.stats["almacen_fin_dia"]]
    R["comida"] = {k: sum(d["comida"].get(k, 0) for d in e.cuadre) for k in ("aparece", "comido", "podrido", "comido_bestia")}
    R["cuadra"] = all(all(d[t]["cuadra"] for t in e.tipos_objeto) for d in e.cuadre)
    R["aparicion"] = e.stats_aparicion; R["bestia"] = {k: e.stats[k] for k in ("bestia_roba", "bestia_pega", "bestia_come_huerto")}
    return {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in R.items()}


def _una(arg):
    t, mg, m, s = arg; return dict(partida(t, mg, m, s), tipo=t, margen=mg, mando=m, semilla=s)


if __name__ == "__main__":
    trabajos = [(t, mg, m, s) for t in TIPOS for mg in MARGENES for m in MANDOS for s in SEMILLAS]
    with Pool(8) as P: res = P.map(_una, trabajos, chunksize=2)
    json.dump(res, open(os.path.join(AQUI, sys.argv[1] if len(sys.argv) > 1 else "resultados_banco_base_v5.json"), "w"), ensure_ascii=False, indent=1)
    for t in TIPOS:
        for mg in MARGENES:
            print(t, mg, {m: sum(8 - len(r["muertes"]) for r in res if r["tipo"] == t and r["margen"] == mg and r["mando"] == m) for m in MANDOS}, "cuadra", all(r["cuadra"] for r in res if r["tipo"] == t))

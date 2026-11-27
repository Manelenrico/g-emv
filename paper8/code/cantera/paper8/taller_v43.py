"""[P8] Prompt 88: la pieza G (la bestia como un mando, valle/config_valle.json → bestia.pieza_g, todo apagado por defecto) y los dos arreglos de los sabores
(RG43r), con el lanzador del experimento.
Los mundos: «<base>+G=<ruedas>», con las ruedas separadas por «.»:
  ini:N (empiezan N bestias) · cria (cada 10 días, hasta 4) · cria:C:M (cada C días, hasta M) · epocas · echar · matar
  y la base del lanzador (normal, sequia…), con «+sabores» delante si hace falta (normal+sabores+G=echar.matar).
   python3 taller_v43.py puerta                       -> salida/puerta_v43.json (todo apagado: idéntico a las de siempre)
   python3 taller_v43.py ruedas <jugadores> <mundos> [semillas=1001-1040] [procesos=8]   -> /Volumes/Mem G-EMV/valle_taller_v43/
   python3 taller_v43.py mecanica                     -> salida/mecanica_v43.json (echar y matar, a mano: criaturas puestas alrededor de la bestia)
   python3 taller_v43.py cortas                       -> 2 partidas cortas de RG43r con echar y matar"""
import copy, gzip, json, os, sys
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":               # que el Mac no se duerma mientras juega (como el lanzador)
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanzador as L
import taller_v40                                                        # el mundo «+sabores»
CARPETA = os.path.join(L.T7, "valle_taller_v43"); PG = L.CFG_M["bestia"]["pieza_g"]
_md = L.mundo_de

def pieza_g(ruedas):
    """la pieza G de la config con esas ruedas encendidas (los números, los de la config salvo los que dice la rueda)"""
    G = copy.deepcopy(PG)
    for r in ruedas:
        k, *x = r.split(":")
        if k == "ini": G["inicial"] = int(x[0])
        elif k == "cria":
            G["cria"]["activo"] = True
            if x: G["cria"]["cada_dias"] = float(x[0]); G["cria"]["maximo"] = int(x[1])
        elif k in ("epocas", "echar", "matar"): G[k]["activo"] = True
        else: raise ValueError(r)
    return G

def mundo_de(nombre):
    if "+G=" in nombre:
        base, ru = nombre.split("+G="); m = copy.deepcopy(mundo_de(base)); m.setdefault("bestia", {})["pieza_g"] = pieza_g([r for r in ru.split(".") if r]); return m
    return taller_v40.mundo_de(nombre)
L.mundo_de = mundo_de

def una(arg):
    r = L.una(arg); v, mu, s, dias, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}")
    e = L.LOG.get("e")
    if not r.get("saltada") and e is not None: json.dump(getattr(e, "stats_g", {}), open(os.path.join(d, "pieza_g.json"), "w"), ensure_ascii=False)
    return r

def puerta(arg):
    v, mu, s, origen = arg; tmp = os.path.join(L.T7, "valle_prueba_v43"); os.makedirs(tmp, exist_ok=True); L.una((v, mu, s, 40, tmp))
    a = gzip.open(os.path.join(tmp, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"), "rt", encoding="utf-8").read()
    b = gzip.open(os.path.join(L.T7, origen, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"), "rt", encoding="utf-8").read()
    return {"clase": v, "mundo": mu, "semilla": s, "registro_identico": a == b}

def mecanica(_=None):
    """echar y matar, a mano: en el mundo normal (semilla 1001), la bestia en una casilla de la zona salvaje y n criaturas pegadas a ella, con la vida
    llena, que la golpean (o empujan) todas en el mismo turno, turno tras turno; las demás, quietas en casa. Qué pasa con la bestia y con ellas"""
    import mundo as MU
    out = []
    for rueda, accion in (("echar", "empujar"), ("echar", "golpear"), ("matar", "golpear")):
        for n in (1, 2, 3, 4, 5, 6):
            e = MU.Valle(mando="medio"); e.cfg["bestia"]["pieza_g"] = pieza_g([rueda]); obs, info = e.reset(seed=1001)
            B = e.bestia; ag = sorted(e.agents); sal = sorted(e.celdas_salvaje)
            q = next(c for c in sal if sum(1 for d in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)) if (c[0] + d[0], c[1] + d[1]) in e.celdas_salvaje) == 8)
            B.update(pos=q, modo="ronda", ruta=[]); vec = [(q[0] + d[0], q[1] + d[1]) for d in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))]
            for a, c in zip(ag[:n], vec): e.pos[a] = c
            e.cfg["terreno_salvaje"]["prob_herida"] = 0.0; e._actua_bestia = lambda B=None: {"accion": "quieta"}      # que no ande ni ataque: quieta en su casilla
            fila = {"rueda": rueda, "accion": accion, "criaturas": n, "turnos": []}
            for t in range(8):
                acts = {a: ({"accion": accion, "a": "bestia"} if a in ag[:n] and not e.cuerpo[a]["muerta"] else {"accion": "quedarse"}) for a in e.agents}
                e.step(acts)
                ev = [x for x in e._eventos if any(k in x for k in ("bestia_herida", "bestia_muere", "bestia_echada"))]
                fila["turnos"].append({"t": t, "bestia": "lejos" if B["modo"] == "lejos" else ("muerta" if B["modo"] == "muerta" else "aquí"), "vida_bestia": round(B.get("vida", 0), 1),
                                       "vidas": [round(e.cuerpo[a]["vida"], 1) for a in ag[:n]], "eventos": ev})
                if B["pos"] is None: break
            fila["comida_en_el_suelo"] = sum(1 for o in e.suelo.get(q, []) if o["tipo"] == "comida")
            out.append(fila)
    return out


if __name__ == "__main__":
    if sys.argv[1] == "puerta":
        G_ = [("tonto", "normal", 1001, "valle_experimento"), ("recolector", "sequia", 1001, "valle_experimento"), ("RG42r", "normal+sabores", 1001, "valle_taller_v35")]
        with Pool(3) as p: out = p.map(puerta, G_)
        print(json.dumps(out, ensure_ascii=False)); json.dump(out, open(os.path.join(AQUI, "salida", "puerta_v43.json"), "w"), ensure_ascii=False, indent=1)
    elif sys.argv[1] == "ruedas":
        VS = sys.argv[2].split(","); MS = sys.argv[3].split(","); a_, b_ = (sys.argv[4] if len(sys.argv) > 4 else "1001-1040").split("-"); npro = int(sys.argv[5]) if len(sys.argv) > 5 else 8
        os.makedirs(CARPETA, exist_ok=True)
        T = [(v, mu, s, 40, CARPETA) for mu in MS for v in VS for s in range(int(a_), int(b_) + 1)]
        with Pool(npro) as p:
            for r in p.imap_unordered(una, T): print(json.dumps({k: r[k] for k in ("id", "saltada", "muertes") if k in r}, ensure_ascii=False)[:300], flush=True)
    elif sys.argv[1] == "mecanica":
        out = mecanica(); json.dump(out, open(os.path.join(AQUI, "salida", "mecanica_v43.json"), "w"), ensure_ascii=False, indent=1)
        for f in out: print(f["rueda"], f["accion"], f["criaturas"], [(x["bestia"], x["vida_bestia"], x["vidas"]) for x in f["turnos"]], f["comida_en_el_suelo"])
    elif sys.argv[1] == "cortas":
        os.makedirs(CARPETA, exist_ok=True); dias = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        T = [("RG43r", "normal+sabores+G=echar.matar", 1001, dias, CARPETA), ("RG43r", "sequia+sabores+G=echar.matar", 1002, dias, CARPETA)]
        with Pool(2) as p:
            for r in p.imap_unordered(una, T): print(json.dumps({k: r[k] for k in ("id", "saltada", "muertes") if k in r}, ensure_ascii=False)[:300], flush=True)

"""[P8] Prompt 79, el taller de RG34r y RG034r.
  puerta: con el interruptor nuevo apagado nada cambia (RG32r, S32 de la bestia de día 1001 del experimento; P32 de la confirmación 2001; el tonto y el
          recolector, 1001): el registro del mundo de 40 días, línea a línea, igual al guardado;
  partidas: RG34r y RG034r en abundancia, normal y sequía, semillas 1001-1007, 40 días (las 42 de siempre), con el lanzador del experimento (los mismos
          registros, en el T7) y, al acabar, lo que ha aprendido cada criatura (su radar: la hermana y cada vecina en cuerpo, recursos y vínculo; las fuentes de
          botín; la medicina guardada y lo que vale dar) en radar.json de cada partida.
   python3 taller_v34.py puerta|partidas [procesos=8]"""
import gzip, json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanzador as L
import cuerpo_valle as CV
CARPETA = os.path.join(L.T7, "valle_taller_v34"); MUNDOS = ("abundancia", "normal", "sequia"); SEM = range(1001, 1008)

def puerta(arg):
    v, mu, s, origen = arg; tmp = os.path.join(L.T7, "valle_prueba_v34")
    L.una((v, mu, s, 40, tmp))
    a = gzip.open(os.path.join(tmp, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"), "rt", encoding="utf-8").read()
    b = gzip.open(os.path.join(L.T7, origen, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"), "rt", encoding="utf-8").read()
    return {"clase": v, "mundo": mu, "semilla": s, "lineas": a.count("\n"), "registro_identico": a == b}

def radar_de(c):
    c._rad["cache"] = {}
    kin = [c.hermana] + sorted(x for x in c.vin)
    return {"hermana": c.hermana, "B": c.B, "vin": dict(c.vin), "radar": {x: c.radar(x) for x in kin},
            "fuentes": {k: c.valor_fuente(k) for k in ("camara", "cajones", "bayas")},
            "medicina_guardar": c.rad_cosa(c.botiquin, "guardar"), "dar_medicina": c.rad_cosa(c.botiquin, "dar"), "dar_comida": c.rad_cosa("comida", "dar"),
            "recuerdos": {f"{o}|{s_}": n for (o, s_), n in __import__("collections").Counter((o, s_) for o, s_, r in c.cuaderno.recuerdos() if o.startswith(("criatura:", "fuente:")) or s_ in ("dar", "guardar")).items()},
            "muerta": c.pareja_muerta}

def partida(arg):
    v, mu, s = arg; d = os.path.join(CARPETA, f"{v}_{mu}_s{s}_d40")
    if os.path.exists(os.path.join(d, "radar.json")): return {"id": os.path.basename(d), "saltada": True}
    r = L.una((v, mu, s, 40, CARPETA))
    json.dump({a: radar_de(c) for a, c in L.CRI.items()}, open(os.path.join(d, "radar.json"), "w"), ensure_ascii=False)
    return r


if __name__ == "__main__":
    que = sys.argv[1]; npro = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    if que == "puerta":
        G = [("RG32r", "bestia_dia", 1001, "valle_experimento"), ("S32", "bestia_dia", 1001, "valle_experimento"), ("P32", "bestia_dia", 2001, "valle_confirmacion"),
             ("tonto", "bestia_dia", 1001, "valle_experimento"), ("recolector", "bestia_dia", 1001, "valle_experimento")]
        with Pool(npro) as p: out = p.map(puerta, G)
        print(json.dumps(out, ensure_ascii=False)); json.dump(out, open(os.path.join(AQUI, "salida", "puerta_v34.json"), "w"), ensure_ascii=False, indent=1)
    else:
        os.makedirs(CARPETA, exist_ok=True)
        T = [(v, mu, s) for mu in MUNDOS for v in ("RG34r", "RG034r") for s in SEM]
        with Pool(npro) as p:
            for r in p.imap_unordered(partida, T): print(json.dumps(r, ensure_ascii=False), flush=True)

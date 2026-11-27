"""[P8] Prompt 90: RG45r (la pieza I con la hermana y el duelo desde el radar), con el lanzador del experimento; al acabar cada partida, imagina.json: por
criatura, sus costumbres aprendidas (recuentos por situación y destino), lo que predijo cada turno que vio a su hermana (turno, dónde estaba, dónde la imagina,
la de seguir su último paso, cómo, la costumbre y su probabilidad) y el duelo de cada muerte (las tres dimensiones del radar y lo que daba el reparto de antes);
y radar_dia.json: una vez al día, el radar de cada una de las suyas y el vínculo (solo medir: no cambia nada).
   python3 taller_v45.py puerta                                 -> salida/puerta_v45.json
       RG44r sale igual que en el prompt 89 (normal y bestias que crían, 1001) y RG42r igual que siempre (normal, 1001): reconocer cualquier bestia no cambia
       nada donde ya se reconocía (o donde solo hay una)
   python3 taller_v45.py partidas <clases> <mundos> [semillas=1001-1021] [procesos=7]   -> /Volumes/Mem G-EMV/valle_taller_v44/"""
import gzip, json, os, sys
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":               # que el Mac no se duerma mientras juega (como el lanzador)
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import lanzador as L
import taller_v40                                                        # el mundo «+sabores»
import taller_v43 as T43
CARPETA = os.path.join(L.T7, os.environ.get("TALLER45_CARPETA") or "valle_taller_v44")      # la misma carpeta que las de RG44r (prompt 89); otra, para repetirlas con el radar de cada día
import cuerpo_valle as CV
_ac = CV.Criatura.actua
def _actua(self, obs, info):
    """(solo medir) una vez al día, lo que vale para ella cada una de las suyas (el radar: cuerpo, recursos, vínculo), para ver la reconstrucción tras una muerte"""
    acc = _ac(self, obs, info)
    if getattr(self, "radar_v34", False) and obs["turno_del_dia"] == 0:
        R = getattr(self, "_rad_dia", None)
        if R is None: R = self._rad_dia = []
        R.append([obs["dia"], {x: {k: round(v, 4) for k, v in self.radar(x).items()} for x in sorted(set(self.otras) | ({self.hermana} if not self.pareja_muerta else set()))},
                  {x: round(self.vin.get(x, 0.0), 4) for x in sorted(self.vin)}])
    return acc
CV.Criatura.actua = _actua

def una(arg):
    r = T43.una(arg); v, mu, s, dias, carpeta = arg; d = os.path.join(carpeta, f"{v}_{mu}_s{s}_d{dias}")
    if not r.get("saltada") and any(getattr(c, "imagina_v45", False) or getattr(c, "duelo_v45", False) for c in L.CRI.values()):
        json.dump({a: {"costumbre": c.costumbre, "pred": c.pred_v45, "duelos": c.duelos_v45} for a, c in L.CRI.items()}, open(os.path.join(d, "imagina.json"), "w"), ensure_ascii=False)
    if not r.get("saltada"): json.dump({a: getattr(c, "_rad_dia", []) for a, c in L.CRI.items()}, open(os.path.join(d, "radar_dia.json"), "w"), ensure_ascii=False)
    return r

def puerta(arg):
    v, mu, s, origen = arg; tmp = os.path.join(L.T7, "valle_prueba_v45"); os.makedirs(tmp, exist_ok=True); L.una((v, mu, s, 40, tmp))
    import taller_v44 as T44                                             # sin la lista «bestias» del registro (la de RG42r es de antes de la pieza G)
    a = T44.lineas(os.path.join(tmp, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz")); b = T44.lineas(os.path.join(L.T7, origen, f"{v}_{mu}_s{s}_d40", "mundo.jsonl.gz"))
    return {"clase": v, "mundo": mu, "semilla": s, "frente_a": origen, "registro_identico_sin_bestias": a == b}


if __name__ == "__main__":
    if sys.argv[1] == "puerta":
        G_ = [("RG44r", "normal+sabores", 1001, "valle_taller_v44"), ("RG44r", "bestias_crian+sabores", 1001, "valle_taller_v44"), ("RG42r", "normal+sabores", 1001, "valle_taller_v35")]
        with Pool(3) as p: out = p.map(puerta, G_)
        print(json.dumps(out, ensure_ascii=False)); json.dump(out, open(os.path.join(AQUI, "salida", "puerta_v45.json"), "w"), ensure_ascii=False, indent=1)
    elif sys.argv[1] == "partidas":
        VS = sys.argv[2].split(","); MS = sys.argv[3].split(","); a_, b_ = (sys.argv[4] if len(sys.argv) > 4 else "1001-1021").split("-"); npro = int(sys.argv[5]) if len(sys.argv) > 5 else 7
        T = [(v, mu, s, 40, CARPETA) for mu in MS for v in VS for s in range(int(a_), int(b_) + 1)]
        with Pool(npro) as p:
            for r in p.imap_unordered(una, T): print(json.dumps({k: r[k] for k in ("id", "saltada", "segundos") if k in r}, ensure_ascii=False), flush=True)

"""[P8] Prompt 152: la escalera con la reserva. El lanzador de los dos jugadores nuevos, sin código nuevo de criatura:
  - S69+voz («S69voz» en las carpetas): el valorador de sumas del v5 (S68: RG68r con sumas_v29) con la reserva del 146 (reserva_v69) y la voz de ir a casa del
    143 (a_casa);
  - P69+voz («P69voz»): el valorador de posición del v5 (P68: RG68r con posicion_v30) con la reserva y la voz.
  Las dos son la clase de RG69r+voz (cuerpo_vr1.RG69V, prompt 147) con los interruptores de S68 o de P68 más los dos de RG69r+voz: las mismas filas; solo
  cambia cómo se componen (Criatura._compone), también en la segunda foto de la voz (VC1._vc_d llama a _compone).
Es lanza_experimento_v6.py (sellado en el v6, importado y sin tocar: su `una`, los registros, la clase de cada jugador) con los jugadores nuevos añadidos a sus
tablas (B7.VARS, CLASE, L5.CRIATURAS). RG69r+voz no se vuelve a jugar: se lee del v6 sellado.
   python3 lanza_escalera_v6.py puerta    -> salida/puerta_escalera_v6.json: partidas de 40 días, sin los registros, línea a línea (muertes, criaturas al acabar,
        mundo y criaturas): S69+voz con la reserva y la voz apagadas (S69off) frente a S68 del v5 y P69+voz con las dos apagadas (P69off) frente a P68 del v5
        (sequía dura 30121, la semilla de las puertas del v6); y RG69r+voz con este lanzador frente a la del v6 sellado (sequía dura 30161)
   python3 lanza_escalera_v6.py prueba    -> salida/prueba_escalera_v6.json: S69+voz y P69+voz, sequía 30121 (ya vista), 10 días, con los registros: solo si la
        reserva actúa (reserva_v69.json: fotos de comer que usaron la reserva) y si la voz suena (voz_vc1.json: voces). No se leen vivas ni muertes.
   python3 lanza_escalera_v6.py experimento [procesos=10] -> 2 × 5 × 40 = 400 partidas (semillas 30161-30200, 40 días) en valle_escalera_v6"""
import json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isdigit() else "experimento"
if __name__ == "__main__" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
sys.argv[1:2] = ["experimento"] if len(sys.argv) > 1 else []                    # (el MODO del lanzador del v6 al importarlo no se usa)
import lanza_experimento_v6 as LE6
L5, B7, ZV, T7 = LE6.L5, LE6.B7, LE6.ZV, LE6.T7
B7.VARS["S69voz"] = dict(B7.VARS["S68"], reserva_v69=True, a_casa=True); B7.VARS["P69voz"] = dict(B7.VARS["P68"], reserva_v69=True, a_casa=True)
B7.VARS["S69off"] = dict(B7.VARS["S68"], reserva_v69=False, a_casa=False); B7.VARS["P69off"] = dict(B7.VARS["P68"], reserva_v69=False, a_casa=False)   # (las de las puertas)
NUEVOS = ("S69voz", "P69voz")
for v in NUEVOS + ("S69off", "P69off"): LE6.CLASE[v] = ZV.RG69V
L5.CRIATURAS = tuple(L5.CRIATURAS) + tuple(v for v in NUEVOS + ("S69off", "P69off") if v not in L5.CRIATURAS)
MUNDOS = LE6.MUNDOS; SEMILLAS = range(30161, 30201); DIAS = 40; OFICIAL = os.path.join(T7, "valle_escalera_v6")
V5 = LE6.V5; V6 = LE6.OFICIAL
una = LE6.una

def puerta(x):
    v, mu, s, ref, vref = x; carp = os.path.join(T7, "valle_escalera_v6_puerta"); os.makedirs(carp, exist_ok=True); n = f"{v}_{mu}_s{s}_d40"
    una((v, mu, s, 40, carp), apuntar=False); nr = f"{vref}_{mu}_s{s}_d40"
    return dict(L5.iguales(os.path.join(carp, n), os.path.join(ref, nr)), id=n, frente_a=os.path.relpath(os.path.join(ref, nr), T7))

def prueba(x):
    v, mu, s = x; carp = os.path.join(T7, "valle_escalera_v6_prueba"); os.makedirs(carp, exist_ok=True); r = una((v, mu, s, 10, carp)); d = os.path.join(carp, r["id"])
    rs = json.load(open(os.path.join(d, "reserva_v69.json"))); vz = json.load(open(os.path.join(d, "voz_vc1.json")))
    return {"id": r["id"], "carpeta": carp, "fotos_con_reserva": sum(c["con_reserva"] for c in rs.values()), "criaturas_con_reserva": sum(c["con_reserva"] > 0 for c in rs.values()),
            "voces": sum(len(c["voces"]) for c in vz.values()), "decisiones_oyendo": sum(len(c["oye"]) for c in vz.values()),
            "registros": {f: os.path.exists(os.path.join(d, f)) for f in ("balance.jsonl.gz", "filas.jsonl.gz", "cuaderno_sitios.json", "cuenta_v61.json", "reserva_v69.json", "voz_vc1.json")}}


if __name__ == "__main__":
    os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
    if MODO == "puerta":
        SDs = "sequia_dura+sabores"
        P = [("S69off", SDs, 30121, V5, "S68"), ("P69off", SDs, 30121, V5, "P68"), ("RG69rvoz", SDs, 30161, V6, "RG69rvoz")]
        with Pool(len(P), maxtasksperchild=1) as p: R = p.map(puerta, P)
        out = {"identicas": sum(r["identica"] for r in R), "de": len(R), "partidas": R}
        json.dump(out, open(os.path.join(AQUI, "salida", "puerta_escalera_v6.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1))
    elif MODO == "prueba":
        with Pool(2, maxtasksperchild=1) as p: R = p.map(prueba, [(v, "sequia+sabores", 30121) for v in NUEVOS])
        json.dump(R, open(os.path.join(AQUI, "salida", "prueba_escalera_v6.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(R, ensure_ascii=False, indent=1))
    else:
        npro = int(sys.argv[2]) if len(sys.argv) > 2 else 10; os.makedirs(OFICIAL, exist_ok=True)
        TR = [(v, mu + "+sabores", s, DIAS, OFICIAL) for mu in MUNDOS for v in NUEVOS for s in SEMILLAS]
        with Pool(npro, maxtasksperchild=1) as p:
            for r in p.imap_unordered(una, TR): print(json.dumps({k: r[k] for k in ("id", "saltada") if k in r}, ensure_ascii=False), flush=True)

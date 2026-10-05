"""[P6-6 · C] Las medidas de la serie repetida. SOLO LECTURA.

NO reimplementa nada: importa `mide_P6_4.py` y usa SU medidor, con sus mismas
definiciones, para que P6-4 y P6-6 se comparen numero a numero. Lo unico que
cambia es el archivo de salida.

  python3 mide_P6_6.py 'A0=paintball/runs/P66_t[13]_A0_*' 'A1=paintball/runs/P66_t[24]_A1_*'
"""
import glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import mide_P6_4 as M                                    # noqa: E402

OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    print(f"### {etiq}", flush=True)
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(p))
    S = M.mide(sorted(carps), etiq)
    OUT[etiq] = {"resumen": M.resumen(S), "vidas": S["vidas"],
                 "por_semilla": S["por_semilla"]}
    print(json.dumps(OUT[etiq]["resumen"], ensure_ascii=False, indent=1))
json.dump(OUT, open(os.path.join(AQUI, "P6_11_medidas.json"), "w"),
          ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_11_medidas.json")

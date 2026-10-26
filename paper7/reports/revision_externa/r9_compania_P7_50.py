"""9 · ¿Escala el mando de miedo (miedo_P7_49) la S-COMPANIA? Recorre los diarios de P7-50 (valiente = asiento 10, MIEDO 0,5; prudente = 11, MIEDO 1,5)
y reune la M de S-COMPANIA que registra cada tic (la que mete filas10_P6_10.py:156, techo GEMV_COMPANIA_TECHO = 0,32). Si el mando la escalara,
la valiente no pasaria de 0,16 y la prudente llegaria a 0,48. Lee tambien P7_49_cierre (filas escaladas). Solo lectura."""
import glob, json, os, re, zipfile, collections as C
from comun import RUNS
rx = re.compile(rb'"S-COMPANIA":\{"M":([0-9.eE+-]+)')
M = C.defaultdict(list); CI = C.defaultdict(list); T = C.Counter()
for z in sorted(glob.glob(os.path.join(RUNS, "P750_s*", "*policy_agent_1[01].zip"))):
    sl = re.search(r"agent_(\d+)\.zip", z).group(1); br = os.path.basename(os.path.dirname(z)).split("_")[3]
    with zipfile.ZipFile(z) as Z:
        for n in Z.namelist():
            with Z.open(n) as fh:
                for line in fh:
                    if line.startswith(b'{"k":"tick"'):
                        T[(br, sl)] += 1
                        for m in rx.findall(line): M[(br, sl)].append(float(m))
                    elif line.startswith(b'{"k":"P7_49_cierre"'): CI[(br, sl)].append(json.loads(line))
for k in sorted(M):
    x = [v for v in M[k] if v > 0]
    q = sorted(x)
    print(k, "valores > 0:", len(x), "max", max(x) if x else None, "p50", q[len(q) // 2] if q else None, "p95", q[int(.95 * len(q))] if q else None,
          "en el techo 0,32:", sum(1 for v in x if abs(v - 0.32) < 1e-6), "| tics", T[k], "fraccion de tics con la fila > 0", round(len(x) / T[k], 3) if T[k] else None)
for k in sorted(CI):
    c = CI[k]; print(k, "cierres", len(c), "miedo", sorted({r["miedo"] for r in c}), "filas_escaladas (suma)", sum(r["filas_escaladas"] for r in c))

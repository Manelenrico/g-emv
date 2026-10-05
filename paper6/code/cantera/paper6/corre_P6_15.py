"""[P6-15] Lanza `banco_P6_15.vida` sobre las 40 vidas de A4, una por proceso,
N a la vez. Las salidas por vida van al scratch (P615_SCRATCH); el resumen lo
hace `resume_P6_15.py`. Instrumento de medida: no toca el cuerpo."""
import glob, os, re, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
OUT = os.environ.get("P615_SCRATCH") or os.path.join(AQUI, "_P6_15_tmp")
os.makedirs(OUT, exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
vidas = []
for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P611_t*_A4_*"))):
    c = os.path.basename(carp)
    for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
        vidas.append((c, int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))))
print(f"{len(vidas)} vidas · {N} a la vez · salida {OUT}", flush=True)
t0 = time.time(); pend = list(vidas); vivos = {}
env = dict(os.environ, P615_SCRATCH=OUT)
while pend or vivos:
    while pend and len(vivos) < N:
        c, s = pend.pop(0); sal = os.path.join(OUT, f"{c}_s{s}.json")
        if os.path.exists(sal):
            print(f"ya hecha {c} s{s}", flush=True); continue
        p = subprocess.Popen([sys.executable, os.path.join(AQUI, "banco_P6_15.py"), c, str(s), sal], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, cwd=AQUI)
        vivos[(c, s)] = p
    for k, p in list(vivos.items()):
        if p.poll() is not None:
            out = p.stdout.read().strip().splitlines()
            print(f"[{time.time() - t0:6.0f} s] {out[-1] if out else '(sin salida)'}" + (f" · CODIGO {p.returncode}" if p.returncode else ""), flush=True)
            if p.returncode:
                print("\n".join(out[-8:]), flush=True)
            del vivos[k]
    time.sleep(2)
print(f"fin · {time.time() - t0:.0f} s", flush=True)

"""[P6-18] Lanza `banco_P6_18.vida` sobre las vidas con momentos de salida, N a la vez."""
import json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("P618_SCRATCH") or os.path.join(AQUI, "_P6_18_tmp"); os.makedirs(OUT, exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
MOM = json.load(open(os.path.join(AQUI, "P6_18_momentos.json")))
vidas = sorted({(m["carp"], m["slot"]) for m in MOM})
print(f"{len(vidas)} vidas · {len(MOM)} momentos · {N} a la vez", flush=True)
t0 = time.time(); pend = list(vidas); vivos = {}
env = dict(os.environ, P615_SCRATCH=OUT)
while pend or vivos:
    while pend and len(vivos) < N:
        c, s = pend.pop(0); sal = os.path.join(OUT, f"{c}_s{s}.json")
        if os.path.exists(sal):
            continue
        vivos[(c, s)] = subprocess.Popen([sys.executable, os.path.join(AQUI, "banco_P6_18.py"), c, str(s), sal], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, cwd=AQUI)
    for k, p in list(vivos.items()):
        if p.poll() is not None:
            out = p.stdout.read().strip().splitlines()
            print(f"[{time.time() - t0:6.0f} s] {out[-1] if out else '(sin salida)'}" + (f" · CODIGO {p.returncode}" if p.returncode else ""), flush=True)
            if p.returncode:
                print("\n".join(out[-12:]), flush=True)
            del vivos[k]
    time.sleep(2)
print(f"fin · {time.time() - t0:.0f} s", flush=True)

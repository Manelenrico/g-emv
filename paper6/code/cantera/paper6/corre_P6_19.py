"""[P6-19] Lanza `banco_P6_19.vida` en tres modos, N a la vez: fidelidad (40 vidas de A4),
momentos (las vidas de P6_18_momentos.json), a6 (40 vidas de A6)."""
import glob, json, os, re, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
OUT = os.environ.get("P619_SCRATCH") or os.path.join(AQUI, "_P6_19_tmp"); os.makedirs(OUT, exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
modos = sys.argv[2:] or ["fidelidad", "momentos", "a6"]
tareas = []
if "fidelidad" in modos:
    for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball/runs/P611_t*_A4_*"))):
        for sl in (10, 11):
            tareas.append(("fidelidad", os.path.basename(carp), sl))
if "momentos" in modos:
    for c, s in sorted({(m["carp"], m["slot"]) for m in json.load(open(os.path.join(AQUI, "P6_18_momentos.json")))}):
        tareas.append(("momentos", c, s))
if "a6" in modos:
    for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball/runs/P618_t1_A6_*"))):
        for sl in (10, 11):
            tareas.append(("a6", os.path.basename(carp), sl))
print(f"{len(tareas)} tareas · {N} a la vez", flush=True)
t0 = time.time(); pend = list(tareas); vivos = {}
env = dict(os.environ, P615_SCRATCH=OUT)
while pend or vivos:
    while pend and len(vivos) < N:
        m, c, s = pend.pop(0); sal = os.path.join(OUT, f"{m}_{c}_s{s}.json")
        if os.path.exists(sal):
            continue
        vivos[(m, c, s)] = subprocess.Popen([sys.executable, os.path.join(AQUI, "banco_P6_19.py"), m, c, str(s), sal], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, cwd=AQUI)
    for k, p in list(vivos.items()):
        if p.poll() is not None:
            out = p.stdout.read().strip().splitlines()
            print(f"[{time.time() - t0:6.0f} s] {out[-1] if out else '(sin salida)'}" + (f" · CODIGO {p.returncode}" if p.returncode else ""), flush=True)
            if p.returncode:
                print("\n".join(out[-12:]), flush=True)
            del vivos[k]
    time.sleep(2)
print(f"fin · {time.time() - t0:.0f} s", flush=True)

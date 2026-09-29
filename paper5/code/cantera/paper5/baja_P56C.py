"""[P5-6C] Baja los artefactos de una tanda: dos asientos por episodio."""
import glob, json, os, subprocess, sys, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CW = os.path.join(RAIZ, "paintball", ".venv", "bin", "coworld")
if not os.path.exists(CW):
    CW = "coworld"


def main():
    tanda = sys.argv[1] if len(sys.argv) > 1 else "1"
    fs = sorted(glob.glob(os.path.join(AQUI, f"P56C_t{tanda}_[AFT]_*.json")))
    print(f"tanda {tanda}: {len(fs)} episodios acabados")
    for p in fs:
        d = json.load(open(p))
        b, s = d["_brazo"], d["_semilla"]
        dest = os.path.join(RAIZ, "paintball", "runs", f"P56C_t{tanda}_{b}_{s}")
        os.makedirs(dest, exist_ok=True)
        for e in d["episodes"]:
            if e["status"] != "completed":
                print(f"  {b}/{s}: {e['status']}, no se baja"); continue
            for slot in (10, 11):
                z = os.path.join(dest, f"{e['id']}-policy_agent_{slot}.zip")
                art = z[:-4] + ".art.log"
                if os.path.exists(art):
                    continue
                if not os.path.exists(z):
                    r = subprocess.run([CW, "episode-logs", e["id"], "--agent",
                                        str(slot), "--artifact",
                                        "--download-dir", dest],
                                       capture_output=True, timeout=900)
                    if r.returncode:
                        print(f"  {b}/{s}/{slot}: FALLO "
                              f"{r.stderr.decode()[:160]}")
                if os.path.exists(z):
                    with zipfile.ZipFile(z) as Z:
                        txt = Z.read(Z.namelist()[0]).decode()
                    open(art, "w").write(txt)
                    print(f"  {b}/{s} asiento {slot}: {txt.count(chr(10)):,} lineas")


if __name__ == "__main__":
    main()

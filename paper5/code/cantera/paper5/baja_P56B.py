"""[P5-6B] Baja los seis artefactos (tres brazos x dos asientos)."""
import json, os, subprocess, sys, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CW = os.path.join(RAIZ, "paintball", ".venv", "bin", "coworld")
if not os.path.exists(CW):
    CW = "coworld"


def main():
    for b in ("A","F","F2","T","C0F"):
        p = os.path.join(AQUI, f"P56B_{b}_final.json")
        if not os.path.exists(p):
            print(b, "sin fichero final"); continue
        d = json.load(open(p))
        dest = os.path.join(RAIZ, "paintball", "runs", "P56B_" + b)
        os.makedirs(dest, exist_ok=True)
        for e in d["episodes"]:
            if e["status"] != "completed":
                print(b, e["id"], "en", e["status"], "· no se baja"); continue
            for slot in (10, 11):
                z = os.path.join(dest, f"{e['id']}-policy_agent_{slot}.zip")
                art = z[:-4] + ".art.log"
                if os.path.exists(art):
                    print(f"  {b} {slot}: ya estaba"); continue
                if not os.path.exists(z):
                    r = subprocess.run([CW, "episode-logs", e["id"],
                                        "--agent", str(slot), "--artifact",
                                        "--download-dir", dest],
                                       capture_output=True, timeout=900)
                    if r.returncode:
                        print(f"  {b} {slot}: FALLO {r.stderr.decode()[:200]}")
                if os.path.exists(z):
                    with zipfile.ZipFile(z) as Z:
                        txt = Z.read(Z.namelist()[0]).decode()
                    open(art, "w").write(txt)
                    print(f"  {b} asiento {slot}: {len(txt):,} B, "
                          f"{txt.count(chr(10)):,} lineas")


if __name__ == "__main__":
    main()

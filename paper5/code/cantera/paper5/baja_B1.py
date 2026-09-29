"""[P5-1 B1] Baja los dos artefactos del episodio y los deja descomprimidos.

Mismo procedimiento que `baja_S3.py`. Destino: paintball/runs/P5_B1/.
"""
import json, os, subprocess, sys, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CW = os.path.join(RAIZ, "paintball", ".venv", "bin", "coworld")
if not os.path.exists(CW):
    CW = "coworld"
ETQ = os.environ.get("P5_ETIQUETA", "B1")
DEST = os.path.join(RAIZ, "paintball", "runs", "P5_" + ETQ)


def main():
    d = json.load(open(os.path.join(AQUI, ETQ + "_final.json")))
    os.makedirs(DEST, exist_ok=True)
    for e in d["episodes"]:
        if e["status"] != "completed":
            print("episodio", e["id"], "en", e["status"], "· no se baja")
            continue
        for slot in (10, 11):
            z = os.path.join(DEST, f"{e['id']}-policy_agent_{slot}.zip")
            art = z[:-4] + ".art.log"
            if os.path.exists(art):
                print("ya estaba:", os.path.basename(art)); continue
            if not os.path.exists(z):
                r = subprocess.run([CW, "episode-logs", e["id"],
                                    "--agent", str(slot), "--artifact",
                                    "--download-dir", DEST],
                                   capture_output=True, timeout=600)
                if r.returncode:
                    print("  fallo", slot, r.stderr.decode()[:200])
            if os.path.exists(z):
                with zipfile.ZipFile(z) as Z:
                    txt = Z.read(Z.namelist()[0]).decode()
                open(art, "w").write(txt)
                print(f"  asiento {slot}: {len(txt):,} B crudos, "
                      f"{os.path.getsize(z):,} B en zip, "
                      f"{txt.count(chr(10)):,} lineas")


if __name__ == "__main__":
    main()

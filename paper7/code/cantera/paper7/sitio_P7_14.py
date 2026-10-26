"""[P7-14, paso 0; aprobado por Manel] BORRA LOS DIARIOS EXTRAIDOS (.art.log) DEL PAPER CINCO en paintball/runs, y solo esos: los de las carpetas
del manifiesto del cinco (`cantera/paper5/DIARIOS_MANIFIESTO.md`, por `cantera/inventario_P7_12.json`) cuyo .zip esta presente y cumple, comprobado
AHORA: md5 del .zip = el de `cantera/sumas_P7_12.csv`; md5 de lo que hay dentro del .zip = md5 del diario segun ese csv; y el diario del disco
tiene ese mismo md5. Si algo no cuadra, ese diario NO se borra y se apunta. No borra ningun .zip ni ningun manifiesto.
  python3 sitio_P7_14.py            (solo comprueba y cuenta)
  python3 sitio_P7_14.py --borra    -> cantera/paper7/P7_14_sitio.json"""
import csv, hashlib, json, os, shutil, sys, zipfile
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
I = json.load(open(os.path.join(RAIZ, "cantera", "inventario_P7_12.json")))["runs"]
cinco = {e for e, d in I.items() if "cinco" in (d.get("manifiesto") or [])}
def md5f(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
libre = lambda: shutil.disk_usage(RAIZ).free
antes = libre(); ok = []; no = []
for r in csv.DictReader(open(os.path.join(RAIZ, "cantera", "sumas_P7_12.csv"))):
    partes = r["zip"].split("/")
    if partes[2] not in cinco: continue
    z = os.path.join(RAIZ, r["zip"]); art = z[:-4] + ".art.log"
    if not os.path.exists(art): no.append((r["zip"], "el diario ya no esta")); continue
    if not os.path.exists(z): no.append((r["zip"], "falta el .zip")); continue
    if md5f(z) != r["md5_zip"]: no.append((r["zip"], "el .zip no es el del csv")); continue
    with zipfile.ZipFile(z) as Z: ns = Z.namelist(); dentro = hashlib.md5(Z.read(ns[0])).hexdigest() if len(ns) == 1 else None
    if dentro != r["md5_art"]: no.append((r["zip"], "el contenido del .zip no es el diario del csv")); continue
    if md5f(art) != r["md5_art"]: no.append((r["zip"], "el diario del disco no es el del csv")); continue
    ok.append((art, os.path.getsize(art)))
print(f"carpetas del cinco: {len(cinco)} · diarios que cumplen: {len(ok)} ({sum(b for _, b in ok) / 2**30:.2f} GiB) · que no: {len(no)}")
for z, m in no[:10]: print("  NO:", z, "·", m)
if "--borra" in sys.argv:
    for art, _ in ok: os.remove(art)
    despues = libre()
    json.dump({"libre_antes_bytes": antes, "libre_despues_bytes": despues, "borrados": len(ok), "bytes_borrados": sum(b for _, b in ok), "no_borrados": no, "diarios": [os.path.relpath(a, RAIZ) for a, _ in ok]}, open(os.path.join(AQUI, "P7_14_sitio.json"), "w"), ensure_ascii=False, indent=0)
    print(f"borrados {len(ok)} diarios · libre antes {antes / 1e9:.2f} GB · despues {despues / 1e9:.2f} GB")

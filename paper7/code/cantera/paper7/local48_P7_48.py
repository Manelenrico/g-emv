"""[P7-48] LA COMPROBACION LOCAL (lazo cerrado, coste cero): dos brazos (comparte | solas), cada uno una cadena de 3 dias en `coworld play` con nuestra imagen en los 16
asientos (8 parejas valiente/prudente). El dia d+1 se hornea con los cuadernos que las 16 criaturas escribieron el dia d (leidos del registro `P7_cuaderno` fin de los
diarios de la partida: en local no hay subida de artefactos). Lee cada partida con local_P7_47.lee y cuenta por hermana: recuerdos por origen (vivido / visto / contado
canal / contado noche), descartes del visto, mensajes M7 enviados y recibidos, pesos = intensidad x B, latencia.
  python3 local48_P7_48.py [--dias 3] [--brazos comparte,solas]  -> _P7_48_local/<brazo>_d<D>/, P7_48_local.json"""
import glob, json, os, shutil, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import local_P7_47 as L47
LOCAL = os.path.join(AQUI, "_P7_48_local"); CUAD = os.path.join(AQUI, "cuadernos_P7_48")


def hornea(brazo, dia, cuad_dir):
    tag = f"gemv-anima:P7_48_{brazo}_d{dia}"; rel = os.path.relpath(cuad_dir, RAIZ)
    r = subprocess.run(["docker", "build", "-f", os.path.join(AQUI, "Dockerfile.pareja_P7_48"), "--build-arg", "BRAZO=APRENDE", "--build-arg", "MIEDO=prudente", "--build-arg", "EPS=0", "--build-arg", f"HERMANAS={brazo}", "--build-arg", f"CUAD={rel}", "-t", tag, RAIZ], capture_output=True, text=True, timeout=1800)
    open(os.path.join(LOCAL, f"build_{brazo}_d{dia}.log"), "w").write(r.stdout[-3000:] + r.stderr[-3000:]); assert r.returncode == 0, r.stderr[-800:]
    return tag


def juega(tag, nombre, timeout=2400):
    out = os.path.join(LOCAL, nombre); shutil.rmtree(out, ignore_errors=True); t0 = time.time()
    cmd = [L47.CW, "play", L47.COW, tag, "--run", "sh", "--run", "-c", "--run", "set -a && . /app/brazo.env && set +a && exec python -u /app/alma/policy_pareja_P7_48.py", "--variant", "competition", "-o", out, "--timeout-seconds", str(timeout), "--no-open-browser"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 300); open(os.path.join(LOCAL, f"{nombre}.log"), "w").write(r.stdout + "\n--- stderr ---\n" + r.stderr)
    return out, round(time.time() - t0)


def cuadernos_de(out, destino):
    """los cuadernos que cada asiento escribio al cerrar (registro P7_cuaderno fin) -> destino/cuaderno_P7_<slot>.json"""
    shutil.rmtree(destino, ignore_errors=True); os.makedirs(destino); n = 0
    for f in sorted(glob.glob(os.path.join(out, "logs", "policy_agent_*.log"))):
        sl = int(os.path.basename(f).split("_")[-1].split(".")[0]); fin = None
        for line in open(f, errors="replace"):
            if line.startswith('{"k":"P7_cuaderno"'):
                r = json.loads(line)
                if r.get("momento") == "fin" and r.get("contenido"): fin = r["contenido"]
        if fin: json.dump(fin, open(os.path.join(destino, f"cuaderno_P7_{sl}.json"), "w"), ensure_ascii=False); n += 1
    return n


def lee48(out):
    R = L47.lee(out)
    for sl, v in R["vidas"].items():
        f = os.path.join(out, "logs", f"policy_agent_{sl}.log"); n = {"vivido": 0, "visto": 0, "visto_descartado": 0, "canal": 0, "noche": 0, "mensajes": 0, "malos": 0}; desc = {}; pesos_ok = 0; pesos_mal = 0; arr = None; cierre = None; noche = []
        for line in open(f, errors="replace"):
            if not line.startswith('{"k":"P7_48'): continue
            r = json.loads(line); k = r["k"]
            if k == "P7_48_arranque": arr = r; noche = r.get("noche") or []
            elif k == "P7_48_cierre": cierre = r
            elif k == "P7_48_contado":
                n[r["via"]] += 1
                if abs(r["peso"] - round(r["intensidad_emisora"] * r["B"], 4)) <= 1e-3: pesos_ok += 1
                else: pesos_mal += 1
            elif k == "P7_48_visto":
                if r["estado"] == "apuntado":
                    n["visto"] += 1
                    if abs(r["peso"] - round(r["intensidad_sin_B"] * r["B"], 4)) <= 1e-3: pesos_ok += 1
                    else: pesos_mal += 1
                else: n["visto_descartado"] += 1; desc[r["motivo"]] = desc.get(r["motivo"], 0) + 1
            elif k == "P7_48_mensaje": n["mensajes"] += 1
            elif k == "P7_48_mensaje_malo": n["malos"] += 1
        if cierre: n["vivido"] = (cierre.get("n") or {}).get("vivido", 0)
        v["P7_48"] = {"n": n, "descartes": desc, "pesos_ok": pesos_ok, "pesos_mal": pesos_mal, "miedo": (arr or {}).get("miedo"), "pareja": (arr or {}).get("pareja"), "B_cierre": (cierre or {}).get("B_cierre"), "noche_recibidos": len(noche), "pendientes_sin_mandar": (cierre or {}).get("pendientes_sin_mandar")}
    return R


if __name__ == "__main__":
    a = sys.argv; dias = int(a[a.index("--dias") + 1]) if "--dias" in a else 3; brazos = (a[a.index("--brazos") + 1].split(",") if "--brazos" in a else ["comparte", "solas"])
    os.makedirs(LOCAL, exist_ok=True); R = json.load(open(os.path.join(AQUI, "P7_48_local.json"))) if os.path.exists(os.path.join(AQUI, "P7_48_local.json")) else {}
    for brazo in brazos:
        cuad = os.path.join(CUAD, "vacio"); os.makedirs(cuad, exist_ok=True)
        for d in range(1, dias + 1):
            nombre = f"{brazo}_d{d}"
            if nombre in R and R[nombre].get("resumen"): cuad = os.path.join(CUAD, f"{brazo}_d{d}"); print(nombre, "ya jugada", flush=True); continue
            tag = hornea(brazo, d, cuad); out, seg = juega(tag, nombre); r = lee48(out); r.update({"imagen": tag, "segundos": seg, "cuadernos_entrada": os.path.relpath(cuad, AQUI)}); R[nombre] = r
            json.dump(R, open(os.path.join(AQUI, "P7_48_local.json"), "w"), ensure_ascii=False, indent=1)
            cuad = os.path.join(CUAD, f"{brazo}_d{d}"); n = cuadernos_de(out, cuad)
            print(nombre, "segundos", seg, "cuadernos escritos", n, json.dumps({k: r["resumen"][k] for k in ("vidas_con_diario", "tics_media", "mueren", "huellas_por_vida", "ms_p95_max", "sobre_tic_pct_media")}), {sl: v["P7_48"]["n"] for sl, v in list(r["vidas"].items())[:4]}, flush=True)

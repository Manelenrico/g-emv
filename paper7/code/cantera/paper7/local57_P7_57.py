"""[P7-57] COMPROBACION LOCAL de la mentira (lazo cerrado, 0 creditos; consola): cadena de 3 dias con nuestra imagen (Dockerfile.pareja_P7_57; hermanas COMPARTE con fusion, MIEDO
0,5/1,5) en los 16 asientos. La razon (razon_P7_54) para los asientos 10-13 cada noche: 10 y 11 = MIENTEN_DOS (las dos mienten), 12 y 13 = MIENTE_UNA (miente la valiente, 12).
Para verlo en 3 dias, la mentira entra desde las invitaciones del dia 2 (GEMV_P7_57_DESDE=2; en el campo, 8: declarado). Los demas asientos, sin razon (control). Los horneados
toman el cerrojo de docker del campo P7-56 (que sigue en marcha) para no pisarle una subida.
  python3 local57_P7_57.py [--dias 3]  -> _P7_57_local/d<D>/, P7_57_local.json"""
import fcntl, glob, json, os, shutil, subprocess, sys, time
os.environ["GEMV_P7_57_DESDE"] = os.environ.get("GEMV_P7_57_DESDE", "2")
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import local_P7_47 as L47, local48_P7_48 as L48, diario_razon_P7_54 as D54, razon_P7_57 as RZ, mentira_P7_57 as MT
LOCAL = os.path.join(AQUI, "_P7_57_local"); CUAD = os.path.join(AQUI, "cuadernos_P7_57_local"); BRAZO = {10: "MIENTEN_DOS", 11: "MIENTEN_DOS", 12: "MIENTE_UNA", 13: "MIENTE_UNA"}; LOCK = os.path.join(AQUI, "P7_56_estado.json.docker.lock")
MIENTE_LOCAL = {10: True, 11: True, 12: True, 13: False}


def hornea(dia, cuad_dir):
    tag = f"gemv-anima:P7_57_local_d{dia}"; rel = os.path.relpath(cuad_dir, RAIZ)
    with open(LOCK, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try: r = subprocess.run(["docker", "build", "-f", os.path.join(AQUI, "Dockerfile.pareja_P7_57"), "--build-arg", "BRAZO=APRENDE", "--build-arg", "MIEDO=prudente", "--build-arg", "EPS=0", "--build-arg", "HERMANAS=comparte", "--build-arg", "FUSION=1", "--build-arg", "MIEDO_V=0.5", "--build-arg", "MIEDO_P=1.5", "--build-arg", f"CUAD={rel}", "-t", tag, RAIZ], capture_output=True, text=True, timeout=1800)
        finally: fcntl.flock(fh, fcntl.LOCK_UN)
    open(os.path.join(LOCAL, f"build_d{dia}.log"), "w").write(r.stdout[-3000:] + r.stderr[-3000:]); assert r.returncode == 0, r.stderr[-800:]; return tag


def juega(tag, nombre, timeout=2400):
    out = os.path.join(LOCAL, nombre); shutil.rmtree(out, ignore_errors=True); t0 = time.time()
    cmd = [L47.CW, "play", L47.COW, tag, "--run", "sh", "--run", "-c", "--run", "set -a && . /app/brazo.env && set +a && exec python -u /app/alma/policy_pareja_P7_57.py", "--variant", "competition", "-o", out, "--timeout-seconds", str(timeout), "--no-open-browser"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 300); open(os.path.join(LOCAL, f"{nombre}.log"), "w").write(r.stdout + "\n--- stderr ---\n" + r.stderr); return out, round(time.time() - t0)


def lee57(out):
    R = L47.lee(out)
    for sl, v in R["vidas"].items():
        f = os.path.join(out, "logs", f"policy_agent_{sl}.log"); g = {"arranque": None, "aceptadas": [], "evaluadas": [], "contrastes": [], "cierre": None}
        for line in open(f, errors="replace"):
            if line.startswith('{"k":"P7_57_arranque"'): g["arranque"] = json.loads(line)
            elif line.startswith('{"k":"P7_54_aceptada"'): g["aceptadas"].append(json.loads(line))
            elif line.startswith('{"k":"P7_54_evaluada"'): g["evaluadas"].append(json.loads(line))
            elif line.startswith('{"k":"P7_57_contraste"'): g["contrastes"].append(json.loads(line))
            elif line.startswith('{"k":"P7_57_cierre"'): g["cierre"] = json.loads(line)
        v["P7_57"] = g
    return R


if __name__ == "__main__":
    a = sys.argv; dias = int(a[a.index("--dias") + 1]) if "--dias" in a else 3; os.makedirs(LOCAL, exist_ok=True); os.makedirs(CUAD, exist_ok=True)
    R = json.load(open(os.path.join(AQUI, "P7_57_local.json"))) if os.path.exists(os.path.join(AQUI, "P7_57_local.json")) else {}
    cuad = os.path.join(CUAD, "vacio"); os.makedirs(cuad, exist_ok=True); cl = None
    for d in range(1, dias + 1):
        nombre = f"d{d}"
        if nombre in R and R[nombre].get("resumen"): cuad = os.path.join(CUAD, f"d{d}"); continue
        tag = hornea(d, cuad); out, seg = juega(tag, nombre); r = lee57(out); r.update({"imagen": tag, "segundos": seg}); R[nombre] = r
        json.dump(R, open(os.path.join(AQUI, "P7_57_local.json"), "w"), ensure_ascii=False, indent=1)
        print(nombre, "segundos", seg, {sl: ((v["P7_57"]["arranque"] or {}).get("invitaciones"), (v["P7_57"]["arranque"] or {}).get("falsas"), len(v["P7_57"]["aceptadas"]), len(v["P7_57"]["contrastes"]), (v["P7_57"]["cierre"] or {}).get("confianza", {}).get("cuerpo")) for sl, v in r["vidas"].items() if int(sl) in BRAZO}, "p95", r["resumen"]["ms_p95_max"], flush=True)
        cuad = os.path.join(CUAD, f"d{d}"); L48.cuadernos_de(out, cuad)
        if d < dias:
            cl = cl or RZ.cliente(); R.setdefault("razon", [])
            for sl in BRAZO:
                f = os.path.join(out, "logs", f"policy_agent_{sl}.log")
                if not os.path.exists(f) or os.path.getsize(f) < 1000: continue
                txt, _ = D54.texto(0, d, "LOCAL57", sl, archivo=f); rr = RZ.llama(cl, txt); inv = [dict(i, dia=d) for i in rr["invitaciones"]]; pos = None
                if MIENTE_LOCAL[sl] and d + 1 >= MT.MENTIRA_DESDE: inv, pos = MT.anade(inv, 0, d, sl)
                json.dump(inv, open(os.path.join(cuad, f"invitaciones_P7_{sl}.json"), "w"), ensure_ascii=False, indent=1)
                R["razon"].append({"dia": d, "slot": sl, "tokens_entrada": rr["tokens_entrada"], "tokens_salida": rr["tokens_salida"], "usd_supuesto": rr["usd_supuesto"], "invitaciones": len(inv), "falsa_en": pos})
                print(f"  razon d{d} a{sl}: {len(inv)} invitaciones (falsa en {pos}), {rr['usd_supuesto']:.4f} $", flush=True)
            json.dump(R, open(os.path.join(AQUI, "P7_57_local.json"), "w"), ensure_ascii=False, indent=1)

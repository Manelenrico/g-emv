"""[P7-66, segundo banco] = local66_P7_66 con la imagen Dockerfile.pareja_P7_66b (invita_P7_66b) y los destinos de la mesa: cada PAREJA recibe la misma invitacion con el mismo destino
(como si se la hubieran contado). MIENTE (10, 11): una casilla del borde (a >= 15 del centro), transitable, donde nunca se vio un botiquin en P7-65 (P7_66b_casillas.json), a entre 8 y 15
casillas de las dos salidas (13, 13) y (18, 9) y que no sea su pedestal; HONESTA (12, 13): una de las casillas del centro con mas botiquines que este a entre 8 y 15 de las dos salidas
(24, 8) y (30, 9). La pieza comprueba la distancia de las dos en el tic de aceptar. -> _P7_66b_local, P7_66b_local.json
--- cabecera de local66_P7_66 ---
[P7-66] BANCO LOCAL de la invitacion a un sitio (lazo cerrado en el Mac; 0 creditos de la plataforma; 0 $ de consola: la razon NO se llama, la invitacion la escribe este guion).
Imagen Dockerfile.pareja_P7_66 en los 16 asientos (hermanas COMPARTE con fusion, MIEDO 0,5/1,5). Cada dia, una sola invitacion por asiento:
  MIENTE  (asientos 10 y 11, hermanas): IR_A_SITIO a un PEDESTAL del borde (alli nunca se han visto botiquines; falsa=True);
  HONESTA (asientos 12 y 13, hermanas): IR_A_SITIO a una de las casillas del centro donde mas botiquines se vieron en P7-65 (falsa=False).
  El resto de asientos, sin invitacion. Promesa: recursos +1; cuerpo 0, vinculo 0 (no se juzgan); calma5 = CALMA5. Destino elegido con semilla (dia, asiento).
  Cadena de dias: el cuaderno que escribe cada asiento un dia es el que lee el siguiente (la confianza en recursos viaja).
  python3 local66_P7_66.py [--dias 4] -> _P7_66_local/d<D>/, P7_66_local.json"""
import fcntl, json, os, random, shutil, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import local_P7_47 as L47, local48_P7_48 as L48
LOCAL = os.path.join(AQUI, "_P7_66b_local"); CUAD = os.path.join(AQUI, "cuadernos_P7_66b_local"); LOCK = os.path.join(AQUI, "P7_56_estado.json.docker.lock")
BRAZO = {10: "MIENTE", 11: "MIENTE", 12: "HONESTA", 13: "HONESTA"}
PEDESTALES = [(40, 24), (39, 30), (35, 35), (30, 39), (24, 40), (18, 39), (13, 35), (9, 30), (8, 24), (9, 18), (13, 13), (18, 9), (24, 8), (30, 9), (35, 13), (39, 18)]   # arena.pedestals del player_config
CENTRO = [(21, 24), (24, 27), (24, 23), (27, 23), (25, 26)]      # las 5 casillas con mas botiquines vistos en P7-65 (120 vidas de la valiente)


SALIDA = {10: (13, 13), 11: (18, 9), 12: (24, 8), 13: (30, 9)}       # la casilla de salida de cada asiento (fija en el banco: P7_66_local)
BORDE = [tuple(p) for p in json.load(open(os.path.join(AQUI, "P7_66b_casillas.json")))["borde_sin_botiquines"]]
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def destino_pareja(dia, sl):
    par = (sl & ~1, (sl & ~1) + 1); falsa = BRAZO[sl] == "MIENTE"; base = BORDE if falsa else CENTRO
    cand = sorted(p for p in base if all(8 <= cheb(p, SALIDA[s]) <= 15 for s in par) and p not in (SALIDA[par[0]], SALIDA[par[1]]))
    return random.Random(1000 * dia + par[0]).choice(cand), len(cand)
def invitacion(dia, sl):
    falsa = BRAZO[sl] == "MIENTE"; dest, _ = destino_pareja(dia, sl)
    return {"tipo": "CONDICION", "accion": "IR_A_SITIO", "destino": list(dest), "anillo": "CUALQUIERA", "calma": "CUALQUIERA", "movimiento": "CUALQUIERA", "hermana": "CUALQUIERA", "calma5": "CALMA5",
            "cuerpo": 0.0, "recursos": 1.0, "vinculo": 0.0, "confianza": "alta", "falsa": falsa, "dia": dia - 1,
            "porque": "alli suele haber botiquines", "se_comprueba": "al llegar se ve un botiquin a una casilla o menos del sitio"}


def hornea(dia, cuad_dir):
    tag = f"gemv-anima:P7_66b_local_d{dia}"; rel = os.path.relpath(cuad_dir, RAIZ)
    with open(LOCK, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try: r = subprocess.run(["docker", "build", "-f", os.path.join(AQUI, "Dockerfile.pareja_P7_66b"), "--build-arg", "BRAZO=APRENDE", "--build-arg", "MIEDO=prudente", "--build-arg", "EPS=0", "--build-arg", "HERMANAS=comparte",
                                 "--build-arg", "FUSION=1", "--build-arg", "MIEDO_V=0.5", "--build-arg", "MIEDO_P=1.5", "--build-arg", f"CUAD={rel}", "-t", tag, RAIZ], capture_output=True, text=True)
        finally: fcntl.flock(fh, fcntl.LOCK_UN)
    open(os.path.join(LOCAL, f"build_d{dia}.log"), "w").write(r.stdout[-3000:] + r.stderr[-3000:]); assert r.returncode == 0, r.stderr[-800:]; return tag


def juega(tag, nombre, timeout=2400):
    out = os.path.join(LOCAL, nombre); shutil.rmtree(out, ignore_errors=True); t0 = time.time()
    cmd = [L47.CW, "play", L47.COW, tag, "--run", "sh", "--run", "-c", "--run", "set -a && . /app/brazo.env && set +a && exec python -u /app/alma/policy_pareja_P7_66b.py", "--variant", "competition", "-o", out, "--timeout-seconds", str(timeout), "--no-open-browser"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 300); open(os.path.join(LOCAL, f"{nombre}.log"), "w").write(r.stdout + "\n--- stderr ---\n" + r.stderr); return out, round(time.time() - t0)


def lee(out):
    R = L47.lee(out); g = {}
    for sl in BRAZO:
        f = os.path.join(out, "logs", f"policy_agent_{sl}.log"); h = {"aceptadas": [], "llegadas": [], "interrumpidas": [], "no_llego": [], "arranque": None, "cierre": None}
        if os.path.exists(f):
            for line in open(f, errors="replace"):
                for k, c in (("P7_66_aceptada", "aceptadas"), ("P7_66_llegada", "llegadas"), ("P7_66_interrumpida", "interrumpidas"), ("P7_66_no_llego", "no_llego")):
                    if line.startswith('{"k":"' + k + '"'): h[c].append(json.loads(line))
                if line.startswith('{"k":"P7_66_arranque"'): h["arranque"] = json.loads(line)
                elif line.startswith('{"k":"P7_66_cierre"'): h["cierre"] = json.loads(line)
        g[str(sl)] = h
    return {"vidas": {sl: {k: v for k, v in R["vidas"].get(sl, {}).items() if k in ("tics", "murio", "ms_p95", "sobre_tic_pct", "bloqueados_pct")} for sl in g}, "P7_66": g}


if __name__ == "__main__":
    a = sys.argv; dias = int(a[a.index("--dias") + 1]) if "--dias" in a else 4; os.makedirs(LOCAL, exist_ok=True); os.makedirs(CUAD, exist_ok=True)
    F = os.path.join(AQUI, "P7_66b_local.json"); R = json.load(open(F)) if os.path.exists(F) else {}
    cuad = os.path.join(CUAD, "d0"); os.makedirs(cuad, exist_ok=True)
    for d in range(1, dias + 1):
        nombre = f"d{d}"
        for sl in BRAZO: json.dump([invitacion(d, sl)], open(os.path.join(cuad, f"invitaciones_P7_{sl}.json"), "w"), ensure_ascii=False, indent=1)
        if nombre in R: cuad = os.path.join(CUAD, f"d{d}"); continue
        tag = hornea(d, cuad); out, seg = juega(tag, nombre); r = lee(out); r.update({"imagen": tag, "segundos": seg, "invitaciones": {str(sl): invitacion(d, sl) for sl in BRAZO}}); R[nombre] = r
        json.dump(R, open(F, "w"), ensure_ascii=False, indent=1)
        print(nombre, "segundos", seg, {sl: (BRAZO[int(sl)], len(h["aceptadas"]), len(h["llegadas"]), sum(x["acierto_recursos"] for x in h["llegadas"]), len(h["interrumpidas"]), len(h["no_llego"]), (h["cierre"] or {}).get("confianza", {}).get("recursos")) for sl, h in r["P7_66"].items()}, flush=True)
        cuad = os.path.join(CUAD, f"d{d}"); L48.cuadernos_de(out, cuad)

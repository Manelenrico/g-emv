"""[P7-54] PRUEBA LOCAL EN LAZO CERRADO de la entrada en el cuerpo: cadena de 3 dias (hermanas SOLAS, pareja MIEDO 0,5/1,5) con nuestra imagen en los 16 asientos. Tras cada dia,
para los asientos CON RAZON (10-13): diario limpio (diario_razon_P7_54) -> la razon (razon_P7_54, consola) -> invitaciones_P7_<asiento>.json en la carpeta del dia siguiente,
junto a los 16 cuadernos. Los demas asientos (0-9, 14, 15) no reciben invitaciones (control). Lee por vida los registros P7_54_* (cargadas, activas, aceptadas, evaluadas, confianza).
  python3 local54_P7_54.py [--dias 3]  -> _P7_54_local/d<D>/, P7_54_local.json"""
import glob, json, os, shutil, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import local_P7_47 as L47, local48_P7_48 as L48, diario_razon_P7_54 as D54, razon_P7_54 as RZ
LOCAL = os.path.join(AQUI, "_P7_54_local"); CUAD = os.path.join(AQUI, "cuadernos_P7_54"); CON_RAZON = (10, 11, 12, 13)


def hornea(dia, cuad_dir):
    tag = f"gemv-anima:P7_54_d{dia}"; rel = os.path.relpath(cuad_dir, RAIZ)
    r = subprocess.run(["docker", "build", "-f", os.path.join(AQUI, "Dockerfile.pareja_P7_54"), "--build-arg", "BRAZO=APRENDE", "--build-arg", "MIEDO=prudente", "--build-arg", "EPS=0", "--build-arg", "HERMANAS=solas", "--build-arg", "MIEDO_V=0.5", "--build-arg", "MIEDO_P=1.5", "--build-arg", f"CUAD={rel}", "-t", tag, RAIZ], capture_output=True, text=True, timeout=1800)
    open(os.path.join(LOCAL, f"build_d{dia}.log"), "w").write(r.stdout[-3000:] + r.stderr[-3000:]); assert r.returncode == 0, r.stderr[-800:]; return tag


def juega(tag, nombre, timeout=2400):
    out = os.path.join(LOCAL, nombre); shutil.rmtree(out, ignore_errors=True); t0 = time.time()
    cmd = [L47.CW, "play", L47.COW, tag, "--run", "sh", "--run", "-c", "--run", "set -a && . /app/brazo.env && set +a && exec python -u /app/alma/policy_pareja_P7_54.py", "--variant", "competition", "-o", out, "--timeout-seconds", str(timeout), "--no-open-browser"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 300); open(os.path.join(LOCAL, f"{nombre}.log"), "w").write(r.stdout + "\n--- stderr ---\n" + r.stderr); return out, round(time.time() - t0)


def lee54(out):
    R = L47.lee(out)
    for sl, v in R["vidas"].items():
        f = os.path.join(out, "logs", f"policy_agent_{sl}.log"); reg = {"arranque": None, "activas": 0, "aceptadas": [], "evaluadas": [], "cierre": None}
        for line in open(f, errors="replace"):
            if not line.startswith('{"k":"P7_54'): continue
            r = json.loads(line); k = r["k"]
            if k == "P7_54_arranque": reg["arranque"] = {kk: r[kk] for kk in ("invitaciones", "confianza", "acciones")}
            elif k == "P7_54_activa": reg["activas"] += 1
            elif k == "P7_54_aceptada": reg["aceptadas"].append({kk: r[kk] for kk in ("tick", "accion", "elegido")})
            elif k == "P7_54_evaluada": reg["evaluadas"].append({kk: r[kk] for kk in ("tick", "accion", "fuente", "prometido", "vivido", "acierto", "confianza_despues")})
            elif k == "P7_54_cierre": reg["cierre"] = {"n": r["n"], "confianza": r["confianza"], "pendientes": r["pendientes"]}
        v["P7_54"] = reg
    return R


if __name__ == "__main__":
    a = sys.argv; dias = int(a[a.index("--dias") + 1]) if "--dias" in a else 3; os.makedirs(LOCAL, exist_ok=True); os.makedirs(CUAD, exist_ok=True)
    R = json.load(open(os.path.join(AQUI, "P7_54_local.json"))) if os.path.exists(os.path.join(AQUI, "P7_54_local.json")) else {}
    cuad = os.path.join(CUAD, "vacio"); os.makedirs(cuad, exist_ok=True); cl = None
    for d in range(1, dias + 1):
        nombre = f"d{d}"
        if nombre in R and R[nombre].get("resumen"): cuad = os.path.join(CUAD, f"d{d}"); print(nombre, "ya jugada", flush=True); continue
        tag = hornea(d, cuad); out, seg = juega(tag, nombre); r = lee54(out); r.update({"imagen": tag, "segundos": seg}); R[nombre] = r
        json.dump(R, open(os.path.join(AQUI, "P7_54_local.json"), "w"), ensure_ascii=False, indent=1)
        print(nombre, "segundos", seg, {sl: (v["P7_54"]["arranque"] or {}).get("invitaciones", 0) for sl, v in r["vidas"].items() if int(sl) in CON_RAZON}, "aceptadas", {sl: len(v["P7_54"]["aceptadas"]) for sl, v in r["vidas"].items() if int(sl) in CON_RAZON}, "evaluadas", {sl: len(v["P7_54"]["evaluadas"]) for sl, v in r["vidas"].items() if int(sl) in CON_RAZON}, flush=True)
        # el dia siguiente: cuadernos de los 16 + invitaciones de la razon para los asientos con razon
        cuad = os.path.join(CUAD, f"d{d}"); n = L48.cuadernos_de(out, cuad)
        if d < dias:
            cl = cl or RZ.cliente(); usd = sum(x["usd_supuesto"] for x in R.get("razon", [])); R.setdefault("razon", [])
            for sl in CON_RAZON:
                f = os.path.join(out, "logs", f"policy_agent_{sl}.log")
                if not os.path.exists(f) or os.path.getsize(f) < 1000: continue
                try: txt, V = D54.texto(0, d, "SOLAS", sl, archivo=f)
                except Exception as ex: print("diario local fallo", sl, repr(ex)[:200], flush=True); continue
                txt = txt.replace("día %d de la serie 0" % d, "día %d (partida local)" % d); open(os.path.join(LOCAL, f"diario_d{d}_a{sl}.md"), "w").write(txt)
                if usd >= RZ.TOPE_USD: print("TOPE consola: sin razon para", sl, flush=True); continue
                rr = RZ.llama(cl, txt); usd += rr["usd_supuesto"]; rr.update({"dia": d, "slot": sl, "chars_diario": len(txt)}); R["razon"].append(rr)
                json.dump([dict(i, dia=d) for i in rr["invitaciones"]], open(os.path.join(cuad, f"invitaciones_P7_{sl}.json"), "w"), ensure_ascii=False, indent=1)
                print(f"  razon d{d} a{sl}: {len(rr['invitaciones'])} invitaciones, {rr['tokens_entrada']}+{rr['tokens_salida']} tokens, {rr['usd_supuesto']:.4f} $ (acumulado {usd:.4f})", flush=True)
            json.dump(R, open(os.path.join(AQUI, "P7_54_local.json"), "w"), ensure_ascii=False, indent=1)

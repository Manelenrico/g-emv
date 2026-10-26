"""[P7-49a] VIABILIDAD EN LOCAL del mando de miedo (lazo cerrado, coste cero): tres partidas con nuestra imagen en los 16 asientos (8 parejas; hermanas SOLAS, sin compartir,
para medir solo el caracter): MIEDO_V / MIEDO_P = 1/1 (referencia), 0,5/1,5 y 0,7/1,3. Por vida: duracion (tics), muerte, tiempo quieta (tics vivos sin cambiar de casilla en los ultimos 48 tics, %), escondida (camuflaje puesto, %), pruebas (huellas), latencia; por hermana (valiente / prudente) la media.
  python3 local49_P7_49.py [--parejas 1:1,0.5:1.5,0.7:1.3]  -> _P7_49_local/<nombre>/, P7_49_local.json"""
import glob, json, os, statistics as st, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
import local_P7_47 as L47
LOCAL = os.path.join(AQUI, "_P7_49_local")


def hornea(mv, mp):
    tag = f"gemv-anima:P7_49_m{mv}_{mp}".replace(".", "")
    r = subprocess.run(["docker", "build", "-f", os.path.join(AQUI, "Dockerfile.pareja_P7_49"), "--build-arg", "BRAZO=APRENDE", "--build-arg", "MIEDO=prudente", "--build-arg", "EPS=0", "--build-arg", "HERMANAS=solas", "--build-arg", f"MIEDO_V={mv}", "--build-arg", f"MIEDO_P={mp}", "--build-arg", "CUAD=cantera/paper7/cuadernos_P7_48/vacio", "-t", tag, RAIZ], capture_output=True, text=True, timeout=1800)
    assert r.returncode == 0, r.stderr[-800:]; return tag


def juega(tag, nombre, timeout=2400):
    out = os.path.join(LOCAL, nombre); subprocess.run(["rm", "-rf", out]); os.makedirs(LOCAL, exist_ok=True); t0 = time.time()
    cmd = [L47.CW, "play", L47.COW, tag, "--run", "sh", "--run", "-c", "--run", "set -a && . /app/brazo.env && set +a && exec python -u /app/alma/policy_pareja_P7_49.py", "--variant", "competition", "-o", out, "--timeout-seconds", str(timeout), "--no-open-browser"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 300); open(os.path.join(LOCAL, f"{nombre}.log"), "w").write(r.stdout + "\n--- stderr ---\n" + r.stderr)
    return out, round(time.time() - t0)


def extra(f):
    T = 0; quieta = 0; camo = 0; miedo = None; cierre = None; hist = []; VENT = 48      # quieta = sin cambiar de casilla en los ultimos 48 tics (2 s; un paso tarda 3-5 tics)
    for line in open(f, errors="replace"):
        if line.startswith('{"k":"tick"'):
            try: r = json.loads(line)
            except Exception: continue
            if r.get("phase") != "live": continue
            T += 1; pos = tuple(r.get("pos") or ()); hist.append(pos)
            if len(hist) > VENT and all(q == pos for q in hist[-VENT - 1:]): quieta += 1
            b = r.get("body"); bid = b.get("id") if isinstance(b, dict) else b
            if bid == "camouflage": camo += 1
        elif line.startswith('{"k":"P7_49_arranque"'): miedo = json.loads(line).get("miedo")
        elif line.startswith('{"k":"P7_49_cierre"'): cierre = json.loads(line)
    return {"quieta_pct": (100 * quieta / max(1, T - VENT) if T > VENT else None), "camuflada_pct": (100 * camo / T if T else None), "miedo": miedo, "filas_escaladas": (cierre or {}).get("filas_escaladas"), "tics_escalados": (cierre or {}).get("tics_escalados")}


def lee49(out):
    R = L47.lee(out)
    for sl, v in R["vidas"].items(): v.update(extra(os.path.join(out, "logs", f"policy_agent_{sl}.log")))
    vs = [v for v in R["vidas"].values() if v["tics"] > 0]; por = {}
    for v in vs:
        k = "valiente" if int([s for s, x in R["vidas"].items() if x is v][0]) % 2 == 0 else "prudente"; por.setdefault(k, []).append(v)
    R["por_hermana"] = {k: {"vidas": len(L), "miedo": (L[0].get("miedo") if L else None), "tics_media": st.mean(x["tics"] for x in L), "tics_mediana": st.median(x["tics"] for x in L), "mueren": sum(1 for x in L if x["murio"]), "quieta_pct": st.mean(x["quieta_pct"] or 0 for x in L), "camuflada_pct": st.mean(x["camuflada_pct"] or 0 for x in L),
                             "huellas_por_vida": st.mean(x["huellas"] for x in L), "ms_mediana": st.mean(x["ms_mediana"] or 0 for x in L), "ms_p95_max": max(x["ms_p95"] or 0 for x in L), "bloqueados_pct": st.mean(x["bloqueados_pct"] or 0 for x in L)} for k, L in por.items()}
    return R


if __name__ == "__main__":
    a = sys.argv; parejas = (a[a.index("--parejas") + 1] if "--parejas" in a else "1:1,0.5:1.5,0.7:1.3").split(",")
    R = json.load(open(os.path.join(AQUI, "P7_49_local.json"))) if os.path.exists(os.path.join(AQUI, "P7_49_local.json")) else {}
    for par in parejas:
        mv, mp = par.split(":"); nombre = f"m{mv}_{mp}".replace(".", "")
        if nombre in R and R[nombre].get("por_hermana") and "--releer" not in a: print(nombre, "ya jugada", flush=True); continue
        if "--releer" in a and nombre in R:
            r = lee49(os.path.join(LOCAL, nombre)); r.update({k: R[nombre][k] for k in ("imagen", "segundos", "miedo_v", "miedo_p")}); R[nombre] = r; json.dump(R, open(os.path.join(AQUI, "P7_49_local.json"), "w"), ensure_ascii=False, indent=1); print(nombre, "releida", json.dumps({h: (round(x["quieta_pct"], 1), round(x["camuflada_pct"], 1)) for h, x in r["por_hermana"].items()}), flush=True); continue
        tag = hornea(mv, mp); out, seg = juega(tag, nombre); r = lee49(out); r.update({"imagen": tag, "segundos": seg, "miedo_v": float(mv), "miedo_p": float(mp)}); R[nombre] = r
        json.dump(R, open(os.path.join(AQUI, "P7_49_local.json"), "w"), ensure_ascii=False, indent=1)
        print(nombre, "segundos", seg, json.dumps(r["por_hermana"], ensure_ascii=False), flush=True)

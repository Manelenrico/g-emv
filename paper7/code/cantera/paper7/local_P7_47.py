"""[P7-47] PARTIDAS LOCALES JUGADAS DE VERDAD (lazo cerrado, coste cero): `coworld play` con el manifiesto de la liga (cow_6a55df20..., Zero Sum, variante competition) y
UNA imagen nuestra en los 16 asientos (no hay imagenes locales de los rivales de la liga: se declara). Al acabar, lee los 16 diarios (logs/policy_agent_<slot>.log) y
cuenta por vida: tics vividos, huellas (pruebas) por objeto, forzadas y fines de SIN (`P7_41_azar`), latencia (ms por decision) y pasos bloqueados.
  python3 local_P7_47.py --imagen gemv-anima:P7_47_SIN_e00019 --nombre SIN_e00019 [--timeout 2400]  -> _P7_47_local/<nombre>/ y P7_47_local_<nombre>.json"""
import glob, json, os, statistics as st, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); CW = os.path.join(RAIZ, "paintball", ".venv", "bin", "coworld")
COW = "cow_6a55df20-08d1-4e4c-adba-33dbd97e1e6f"; LOCAL = os.path.join(AQUI, "_P7_47_local")
CUATRO = {"first_aid": "botiquin", "rations": "racion", "net": "red", "camouflage": "camuflaje"}


def juega(imagen, nombre, timeout):
    out = os.path.join(LOCAL, nombre); subprocess.run(["rm", "-rf", out]); os.makedirs(LOCAL, exist_ok=True); t0 = time.time()
    cmd = [CW, "play", COW, imagen, "--run", "sh", "--run", "-c", "--run", "set -a && . /app/brazo.env && set +a && exec python -u /app/alma/policy_pareja_P7_47.py", "--variant", "competition", "-o", out, "--timeout-seconds", str(timeout), "--no-open-browser"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 300)
    open(os.path.join(LOCAL, f"{nombre}.log"), "w").write(r.stdout + "\n--- stderr ---\n" + r.stderr)
    return out, round(time.time() - t0)


def vida(f):
    T = 0; ms = []; bloq = 0; listos = 0; H = []; FZ = []; FIN = []; ARR = None; t_ult = 0; prev_pos = None; ult = None; no_esta = 0
    for line in open(f, errors="replace"):
        if line.startswith('{"k":"tick"'):
            try: r = json.loads(line)
            except Exception: continue
            if r.get("phase") != "live": continue
            T += 1; t_ult = r["tick"]; m = (r.get("RADIOGRAFIA") or {}).get("ms"); ult = r
            if m is not None: ms.append(float(m))
            if (r.get("move_ready_in") or 0) == 0: listos += 1
            if r.get("action_result") == "blocked": bloq += 1
        elif line.startswith('{"k":"P7_huella"'): H.append(json.loads(line))
        elif line.startswith('{"k":"P7_41_azar"'):
            r = json.loads(line)
            if r.get("momento") == "forzada": FZ.append(r)
            elif r.get("momento") == "fin":
                FIN.append(r)
                if r.get("fin") == "no cabe" and FZ and ult is not None:          # al cerrar "no cabe": ¿sigue el objeto en la casilla del destino?
                    d = tuple(FZ[-1].get("destino") or ()); esta = any(it.get("id") == FZ[-1].get("objeto") and tuple(it.get("pos") or ()) == d for it in (ult.get("ve_items") or []))
                    r["objeto_sigue"] = esta; no_esta += (not esta)
        elif line.startswith('{"k":"P7_47_arranque"') or line.startswith('{"k":"P7_41_arranque"'): ARR = json.loads(line)
    fines = {}
    for x in FIN: fines[x["fin"]] = fines.get(x["fin"], 0) + 1
    return {"tics": T, "t_ult": t_ult, "murio": t_ult < 14000, "ms_mediana": (st.median(ms) if ms else None), "ms_p95": (sorted(ms)[int(0.95 * len(ms))] if ms else None), "sobre_tic_pct": (100 * sum(1 for x in ms if x > 41.67) / len(ms) if ms else None),
            "bloqueados_pct": (100 * bloq / listos if listos else None), "huellas": len(H), "huellas_por_objeto": {v: sum(1 for h in H if (h.get("objeto") or "first_aid") == k) for k, v in CUATRO.items()}, "huellas_corte": sum(1 for h in H if h.get("corte")),
            "forzadas": len(FZ), "no_cabe_objeto_ya_no_esta": no_esta, "forzadas_por_tipo": {t: sum(1 for x in FZ if x.get("tipo") == t) for t in ("ir", "usar")}, "fines": fines, "vias": {v: sum(1 for x in FIN if x.get("via") == v) for v in ("recoger", "hacer_sitio", "coger_puesto")}, "piezas": (ARR or {}).get("piezas"), "brazo": (ARR or {}).get("brazo")}


def lee(out):
    V = {}
    for f in sorted(glob.glob(os.path.join(out, "logs", "policy_agent_*.log"))):
        sl = int(os.path.basename(f).split("_")[-1].split(".")[0]); V[sl] = vida(f)
    vs = [v for v in V.values() if v["tics"] > 0]
    n = len(vs); acaban = sum(v["fines"].get("cogida", 0) + v["fines"].get("usada", 0) for v in vs); forz = sum(v["forzadas"] for v in vs)
    return {"vidas": V, "resumen": {"vidas_con_diario": n, "tics_media": (st.mean(v["tics"] for v in vs) if vs else None), "mueren": sum(1 for v in vs if v["murio"]), "huellas_por_vida": (st.mean(v["huellas"] for v in vs) if vs else None), "huellas_ee": (st.stdev([v["huellas"] for v in vs]) / n ** 0.5 if n > 1 else None),
            "huellas_por_objeto_total": {o: sum(v["huellas_por_objeto"][o] for v in vs) for o in CUATRO.values()}, "forzadas_total": forz, "forzadas_por_vida": (forz / n if n else None), "acaban": acaban, "acaban_pct": (100 * acaban / forz if forz else None), "fines_total": {k: sum(v["fines"].get(k, 0) for v in vs) for k in ("cogida", "usada", "caduca", "no cabe")}, "no_cabe_objeto_ya_no_esta": sum(v["no_cabe_objeto_ya_no_esta"] for v in vs),
            "vias_total": {k: sum(v["vias"].get(k, 0) for v in vs) for k in ("recoger", "hacer_sitio", "coger_puesto")}, "ms_mediana_media": (st.mean(v["ms_mediana"] for v in vs if v["ms_mediana"] is not None) if vs else None), "ms_p95_max": (max(v["ms_p95"] for v in vs if v["ms_p95"] is not None) if vs else None),
            "sobre_tic_pct_media": (st.mean(v["sobre_tic_pct"] for v in vs if v["sobre_tic_pct"] is not None) if vs else None), "bloqueados_pct_media": (st.mean(v["bloqueados_pct"] for v in vs if v["bloqueados_pct"] is not None) if vs else None), "piezas": next((v["piezas"] for v in vs if v["piezas"]), None)}}


if __name__ == "__main__":
    a = sys.argv; imagen = a[a.index("--imagen") + 1]; nombre = a[a.index("--nombre") + 1]; timeout = int(a[a.index("--timeout") + 1]) if "--timeout" in a else 2400
    if "--solo-leer" not in a: out, seg = juega(imagen, nombre, timeout)
    else: out, seg = os.path.join(LOCAL, nombre), None
    R = lee(out); R["imagen"] = imagen; R["nombre"] = nombre; R["segundos"] = seg
    json.dump(R, open(os.path.join(AQUI, f"P7_47_local_{nombre}.json"), "w"), ensure_ascii=False, indent=1)
    print(nombre, "segundos", seg, json.dumps(R["resumen"], ensure_ascii=False))

"""[P7-49a] IDENTIDAD con MIEDO = 1: tres vidas completas del campo P7-45 (APRENDE, cuadernos reales del dia anterior), replicadas en lazo abierto con la composicion
P7-49 (hermanas solas + mando de miedo, MIEDO_V = MIEDO_P = 1) y sin el mando (campo_P7_48 solas, sin caracter por paridad: GEMV_P7_48_MIEDO_PAREJA=0): decision a decision, elegido por tic; si UNA difiere, no sirve.
Ademas la misma comparacion con MIEDO = 0,5 / 1,5 (que SI debe diferir) como control del enganche.  python3 banco_P7_49.py -> P7_49_identidad.json"""
import glob, json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI)
VIDAS = (("P741_s1_d8_APRENDE_v_*", 10, "APRENDE_v"), ("P741_s2_d13_APRENDE_p_*", 11, "APRENDE_p"), ("P741_s3_d17_APRENDE_v_*", 11, "APRENDE_v"))


def vida(carp, slot, var, composicion, mv, mp):
    for p in (AQUI, os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
        if p not in sys.path: sys.path.insert(0, p)
    os.environ["GEMV_P7_48_MIEDO_PAREJA"] = "0"            # la referencia sin mando tampoco lleva caracter por paridad: el caracter es solo el mando
    os.environ.update({"P7_43_VARIANTE": var, "P7_43_RES": "P7_41_res", "GEMV_P7_43_CACHE": "1", "GEMV_P7_43_MURO": "1", "GEMV_P7_48": "solas", "GEMV_P7_49_MIEDO_V": str(mv), "GEMV_P7_49_MIEDO_P": str(mp)})
    import banco_P7_41 as B41, campo_P7_41 as C41
    def _ap(clase, registra=None):
        os.environ["GEMV_OJOS"] = "1"
        import importlib; C = importlib.import_module(composicion); return C.aplica(clase, registra)
    C41.aplica = _ap
    r = B41.vida(carp, slot, "APRENDE", 0, "prudente")
    return {"tics": r["tics"], "fidelidad": r["fidelidad"], "elegidos": r["elegidos"], "ms": r.get("ms")}


if __name__ == "__main__":
    a = sys.argv
    if "--vida" in a:
        i = a.index("--vida"); r = vida(a[i + 1], int(a[i + 2]), a[i + 3], a[i + 4], float(a[i + 5]), float(a[i + 6])); json.dump(r, open(a[a.index("--salida") + 1], "w")); sys.exit(0)
    R = []
    for pat, slot, var in VIDAS:
        carp = glob.glob(os.path.join(RAIZ, "paintball", "runs", pat))[0]; res = {}
        for nombre, comp, mv, mp in (("sin_mando", "campo_P7_48", 1, 1), ("mando_1", "campo_P7_49", 1, 1), ("mando_05_15", "campo_P7_49", 0.5, 1.5), ("mando_07_13", "campo_P7_49", 0.7, 1.3)):
            sal = os.path.join(AQUI, "_P7_48_tmp", f"id_{nombre}_{slot}.json")
            subprocess.run([sys.executable, os.path.abspath(__file__), "--vida", carp, str(slot), var, comp, str(mv), str(mp), "--salida", sal], capture_output=True, text=True, timeout=3600)
            res[nombre] = json.load(open(sal))
        base = dict((t, e) for t, e in res["sin_mando"]["elegidos"]); fila = {"vida": os.path.basename(carp), "slot": slot, "tics": res["sin_mando"]["tics"]}
        for nombre in ("mando_1", "mando_05_15", "mando_07_13"):
            el = dict((t, e) for t, e in res[nombre]["elegidos"]); dif = [t for t in base if el.get(t) != base[t]]
            fila[nombre] = {"decisiones": len(base), "distintas": len(dif), "primeras": dif[:5], "ms_p95": (res[nombre].get("ms") or {}).get("p95")}
        R.append(fila); print(json.dumps(fila, ensure_ascii=False), flush=True)
    json.dump(R, open(os.path.join(AQUI, "P7_49_identidad.json"), "w"), ensure_ascii=False, indent=1)
    print("IDENTIDAD MIEDO=1:", "PASA" if all(f["mando_1"]["distintas"] == 0 for f in R) else "NO PASA")

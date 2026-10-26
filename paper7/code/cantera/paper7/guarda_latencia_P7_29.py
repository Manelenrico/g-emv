"""[P7-29b, corregida en P7-30] LA GUARDA DE LATENCIA (mesa, 8-oct): en todo humo y todo campo se mide el tiempo de cada decision (`RADIOGRAFIA.ms` del diario) y se da
en el informe la mediana, el p95 y el maximo por brazo y vida (sin parar por ellos); y se cuentan los pasos listos (`move_ready_in` = 0) que salen `blocked` SIN UN
CUERPO DELANTE (ningun agente a la vista en la casilla a la que iba el paso, `intencion.dir` del tic anterior). [P7-30, mesa] Una vida se MARCA (entra en la segunda cuenta del
sello) si mas del SOBRE_EL_TIC_MAX = 1 % de las decisiones pasan de TIC_MS = 41,7 ms (lo que dura un tic), o si mas del BLOQUEO_MAX = 5 % de los pasos listos salen bloqueados
sin cuerpo delante. [P7-30, mesa tras la tercera parada] El lanzador solo PARA si una vida de cualquier brazo supera PARA_SOBRE_EL_TIC = 10 % de decisiones sobre el tic o
BLOQUEO_MAX = 5 % de pasos bloqueados sin cuerpo. (La regla de P7-29b, p95 > 20 ms, estaba mal puesta: paro el humo por 0,53 ms en tics de 20 candidatos.)
[P7-30, mesa tras la cuarta parada] RAREZA DEL MUNDO anotada en el sello: la casilla (14,25) de la semilla k = 184 (39531052), bloqueada desde el este (asiento 10,
tics ~4.400-5.100) sin que el agente vea nada; para esa semilla y esa casilla la regla de parar por bloqueos sin cuerpo no se aplica (`rareza`): se marca y se sigue.
  python3 guarda_latencia_P7_29.py DIARIO.art.log [...]      imprime la medida de cada diario y si pasa la guarda"""
RAREZAS = {(39531052, (14, 25))}      # (semilla, casilla hacia la que choca)


def es_rareza(semilla, g):
    c = g.get("casilla_mas_bloqueada") or {}
    return bool(c) and (int(semilla), tuple(c.get("hacia") or ())) in RAREZAS and g["fraccion_sin_cuerpo"] > BLOQUEO_MAX and (g["sobre_el_tic"] or 0) <= PARA_SOBRE_EL_TIC
import json, os, statistics as st, sys
SOBRE_EL_TIC_MAX = 0.01; BLOQUEO_MAX = 0.05; PARA_SOBRE_EL_TIC = 0.10; TIC_MS = 1000.0 / 24
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}


def mide(diario):
    ms = []; listos = 0; bl = 0; bl_sin = 0; prev = None; tics = 0; casillas = {}
    for line in open(diario, errors="replace"):
        if '"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") != "tick" or r.get("phase") != "live": continue
        tics += 1; m = (r.get("RADIOGRAFIA") or {}).get("ms")
        if m is not None: ms.append(float(m))
        if (r.get("move_ready_in") or 0) == 0:
            listos += 1
            if r.get("action_result") == "blocked":
                bl += 1
                it = (prev or {}).get("intencion") or {}
                if it.get("do") == "move" and it.get("dir") in DIRS and prev:
                    dx, dy = DIRS[it["dir"]]; tgt = (prev["pos"][0] + dx, prev["pos"][1] + dy)
                    if not any(tuple(a.get("pos") or ()) == tgt for a in (prev.get("ve_agentes") or [])): bl_sin += 1; casillas[(tuple(prev["pos"]), it["dir"], tgt)] = casillas.get((tuple(prev["pos"]), it["dir"], tgt), 0) + 1
                else: bl_sin += 1
        prev = r
    ms_s = sorted(ms)
    out = {"tics": tics, "decisiones": len(ms), "ms_mediana": (round(st.median(ms_s), 2) if ms_s else None), "ms_p95": (round(ms_s[min(len(ms_s) - 1, int(0.95 * len(ms_s)))], 2) if ms_s else None), "ms_max": (round(ms_s[-1], 2) if ms_s else None),
           "sobre_el_tic": (round(sum(1 for m in ms_s if m > TIC_MS) / len(ms_s), 4) if ms_s else None), "paso_listo": listos, "bloqueados": bl, "bloqueados_sin_cuerpo": bl_sin, "fraccion_sin_cuerpo": (round(bl_sin / listos, 4) if listos else 0.0)}
    out["pasa"] = bool(out["sobre_el_tic"] is not None and out["sobre_el_tic"] <= SOBRE_EL_TIC_MAX and out["fraccion_sin_cuerpo"] <= BLOQUEO_MAX)
    top = max(casillas.items(), key=lambda kv: kv[1]) if casillas else None
    out["casilla_mas_bloqueada"] = ({"desde": list(top[0][0]), "dir": top[0][1], "hacia": list(top[0][2]), "n": top[1]} if top else None)
    out["para"] = bool((out["sobre_el_tic"] or 0) > PARA_SOBRE_EL_TIC or out["fraccion_sin_cuerpo"] > BLOQUEO_MAX)
    out["motivo"] = ([] if out["pasa"] else ([f"decisiones por encima del tic {100 * (out['sobre_el_tic'] or 0):.2f} % > {100 * SOBRE_EL_TIC_MAX:.0f} %"] if (out["sobre_el_tic"] or 0) > SOBRE_EL_TIC_MAX else []) + ([f"bloqueados sin cuerpo {100 * out['fraccion_sin_cuerpo']:.1f} % > {100 * BLOQUEO_MAX:.0f} %"] if out["fraccion_sin_cuerpo"] > BLOQUEO_MAX else []))
    return out


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(os.path.basename(f)[-20:], mide(f))

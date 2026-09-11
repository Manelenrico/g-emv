"""EL FORENSE DE LA SEPARACION — PROMPT_56 B (coste 0, sin sellos).

¿Que separa a las gemelas v29 (mediana 3,6; en banda 5,1) cuando las v19
vivian a 2,2? Por tic VISTO: cuando la distancia entre hermanas CRECE
respecto del ultimo tic visto, ¿que candidato gana y que fila del AHORA
manda? Contraste contra los tics donde ENCOGE. Hipotesis de la mesa: la
pila las separa (acopio -> botin; muro -> cada una huye por su lado).

Uso (desde la raiz del repo):  python3 paintball/separacion.py
"""
from __future__ import annotations

import collections
import json
import statistics as st

from pareja import diario, B

FILAS_CLAVE = ("R-ACOPIO", "R-LLAMADA", "R-CARENCIA", "S-7-AGRESOR",
               "F-DANO", "F-ANTICIPACION", "F-4-ALCANCE", "S-8-EXPOSICION",
               "S-HERIDO", "S-SOLEDAD")


def clase(elegido):
    e = elegido or "?"
    if e.startswith(("ir_objeto", "ir_botin")):
        return "ir_objeto/botin"
    if e.startswith("ir_centro"):
        return "ir_centro"
    if e.startswith("ir_pareja"):
        return "ir_pareja"
    if e.startswith(("move_", "paso_")):
        return "mover"
    if e.startswith("usar"):
        return "usar"
    if e.startswith("atacar"):
        return "atacar"
    if e.startswith("soltar"):
        return "soltar"
    return e


def main():
    D = json.load(open(f"{B}/episodios.json"))
    grupos = {"CRECE": collections.Counter(), "ENCOGE": collections.Counter()}
    filas_g = {"CRECE": collections.Counter(), "ENCOGE": collections.Counter()}
    muro_g = {"CRECE": [0, 0], "ENCOGE": [0, 0]}
    n_t = {"CRECE": 0, "ENCOGE": 0}
    dists_all = []
    for e in D["eps"]:
        for s in (10, 11):
            recs = diario(e["id"], s)
            if not recs:
                continue
            prev = None
            for d in recs:
                if d.get("k") != "tick" or d.get("phase") != "live":
                    continue
                soc = d.get("social") or {}
                if not soc.get("pareja_vista") or soc.get("dist_pareja") is None:
                    continue
                dv = float(soc["dist_pareja"])
                dists_all.append(dv)
                rad = d.get("RADIOGRAFIA") or {}
                el = rad.get("elegido")
                if prev is not None and abs(dv - prev) > 1e-9 and el and el != "noop":
                    g = "CRECE" if dv > prev else "ENCOGE"
                    n_t[g] += 1
                    grupos[g][clase(el)] += 1
                    fil = (rad.get("ahora") or {}).get("filas") or {}
                    ms = {k: (fil.get(k) or {}).get("M", 0) or 0
                          for k in FILAS_CLAVE}
                    top = max(ms, key=ms.get)
                    if ms[top] > 0:
                        filas_g[g][top] += 1
                    s7 = ms.get("S-7-AGRESOR", 0)
                    muro_g[g][0] += 1 if s7 > 0 else 0
                    muro_g[g][1] += 1
                prev = dv
    print("=" * 86)
    print("EL FORENSE DE LA SEPARACION — tics VISTOS con decision real (no noop)")
    print("=" * 86)
    print(f"\n  distancia vista: mediana {st.median(dists_all):.1f} "
          f"(fondo v29; baseline v19 2,2)\n")
    for g in ("CRECE", "ENCOGE"):
        n = n_t[g]
        print(f"  {g}: {n} tics")
        print(f"    elegido: " + " · ".join(
            f"{k} {100*v/n:.0f}%" for k, v in grupos[g].most_common(6)))
        nf = sum(filas_g[g].values()) or 1
        print(f"    fila M dominante del ahora: " + " · ".join(
            f"{k} {100*v/nf:.0f}%" for k, v in filas_g[g].most_common(5)))
        print(f"    S-7 (agresor activo) encendida: "
              f"{100*muro_g[g][0]/max(muro_g[g][1],1):.0f}%\n")


if __name__ == "__main__":
    main()

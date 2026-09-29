"""[P5-5A] Saca del diario las respuestas del consejero, una por llamada.

Cada linea de la salida es UNA respuesta (`cortex_llamada`) con sus propuestas,
su traduccion y lo que el mundo vio en ese tic. En seco, coste cero.
"""
from __future__ import annotations
import json, os, glob, sys, collections

AQUI = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "gemv-coworld",
                    "paintball", "runs")
if not os.path.isdir(RUNS):
    RUNS = "paintball/runs"
SAL = os.path.join(AQUI, "P55A_respuestas.jsonl")
VIDA = 100                      # GEMV_CORTEX_VIDA


def ereq_de(f):
    b = os.path.basename(f)
    return b.split("-policy_agent_")[0], "agent_" + b.split("-policy_agent_")[1][:2].strip(".")


def main():
    out = open(SAL, "w", encoding="utf-8")
    cuenta = collections.Counter()
    fs = []
    for arm in ("S2_B", "S2_C"):
        fs += [(arm, f) for f in sorted(glob.glob(f"{RUNS}/{arm}/*.art.log"))]
    for i, (arm, f) in enumerate(fs, 1):
        ereq, asiento = ereq_de(f)
        llam = []          # respuestas de este diario
        cxt = collections.defaultdict(list)   # tick -> [(n, estado, gano)]
        slot_yo = None
        for line in open(f, encoding="utf-8"):
            if '"k"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            k = d.get("k")
            if k == "cortex_llamada":
                llam.append(d)
            elif k == "cortex_tic":
                t = d.get("tick")
                for p in d.get("propuestas") or []:
                    n = p.get("n") or ""
                    if n.startswith("_CX_"):
                        cxt[t].append((n, p.get("estado"), bool(p.get("gano"))))
            elif k == "player_config" and slot_yo is None:
                slot_yo = (d.get("cfg") or d).get("slot")
        for d in llam:
            t0 = d.get("tick_foto")
            t1 = d.get("tick_llegada")
            props = d.get("propuestas") or []
            trad = d.get("traduccion") or []
            filas = []
            for j, p in enumerate(props):
                tr = trad[j] if j < len(trad) else {}
                nom = tr.get("nombre")
                cajas = collections.Counter()
                gano = False
                if nom:
                    for t in range(t1 or 0, (t1 or 0) + VIDA + 1):
                        for n, est, g in cxt.get(t, ()):
                            if n == nom:
                                cajas[est] += 1
                                gano = gano or g
                filas.append({
                    "accion": p.get("accion", ""), "motivo": p.get("motivo", ""),
                    "clase_trad": tr.get("clase"), "regla": tr.get("regla"),
                    "nombre": nom, "caducada": bool(tr.get("caducada_motivo")),
                    "cajas": dict(cajas), "gano": gano,
                })
            out.write(json.dumps({
                "arm": arm, "ereq": ereq, "asiento": asiento, "slot": slot_yo,
                "tick_foto": t0, "tick_llegada": t1, "ok": bool(d.get("ok")),
                "relato": d.get("relato", ""), "props": filas,
            }, ensure_ascii=False) + "\n")
            cuenta["respuestas"] += 1
            cuenta["propuestas"] += len(filas)
        print(f"[{i}/{len(fs)}] {arm} {ereq[:18]} {asiento} · "
              f"{len(llam)} respuestas", flush=True)
    out.close()
    print("TOTAL", dict(cuenta))


if __name__ == "__main__":
    main()

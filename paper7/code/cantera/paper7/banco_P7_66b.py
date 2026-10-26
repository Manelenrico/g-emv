"""[P7-66, segundo banco] = banco_P7_66 sobre _P7_66b_local / P7_66b_local.json, contando por PAREJA (llegadas por pareja y dia; juntas o una sola) y, como no hay llegadas, los GIF
son de un intento cerrado (interrumpido o no llego) de cada brazo, de la aceptacion a su cierre.
--- cabecera de banco_P7_66 ---
[P7-66] RESUMEN DEL BANCO LOCAL y los 2 GIF (descriptivo). De P7_66_local.json y los diarios de _P7_66_local/d<D>/logs: por brazo y hermana, aceptadas, llegadas (y aciertos),
interrumpidas, no llego; tics hasta la interrupcion; evaluaciones esperadas por serie (llegadas por vida-dia x 2 hermanas x 13 dias, el tramo de la mentira). GIF (matplotlib, datos
crudos): una LLEGADA del brazo MIENTE y una del HONESTA (semilla 66), de la aceptacion al juicio: ella, su hermana, los rivales y botiquines visibles, el destino y las paredes.
  python3 banco_P7_66.py -> P7_66_banco.json, P7_66_gif_miente.gif, P7_66_gif_honesta.gif"""
import json, os, random, shutil, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); L = os.path.join(AQUI, "_P7_66b_local"); R = json.load(open(os.path.join(AQUI, "P7_66b_local.json")))
BRAZO = {"10": "MIENTE", "11": "MIENTE", "12": "HONESTA", "13": "HONESTA"}; HER = {"10": "valiente", "11": "prudente", "12": "valiente", "13": "prudente"}
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
T = {}; llegadas = []; cerrados = []
for d, v in R.items():
    for sl, h in v["P7_66"].items():
        k = f"{BRAZO[sl]} · {HER[sl]}"; t = T.setdefault(k, {"vidas_dia": 0, "aceptadas": 0, "llegadas": 0, "aciertos": 0, "interrumpidas": 0, "no_llego": 0, "tics_hasta_interrupcion": [], "distancia_al_aceptar": []})
        t["vidas_dia"] += 1; t["aceptadas"] += len(h["aceptadas"]); t["llegadas"] += len(h["llegadas"]); t["aciertos"] += sum(x["acierto_recursos"] for x in h["llegadas"])
        t["interrumpidas"] += len(h["interrumpidas"]); t["no_llego"] += len(h["no_llego"]); t["tics_hasta_interrupcion"] += [x["tics"] for x in h["interrumpidas"]]; t["distancia_al_aceptar"] += [x["distancia"] for x in h["aceptadas"]]
        llegadas += [(d, sl, x) for x in h["llegadas"]]; cerrados.extend((d, sl, dict(x, cierre=c_)) for c_, xs in (("interrumpida", h["interrumpidas"]), ("no llego", h["no_llego"]), ("llegada", h["llegadas"])) for x in xs)
for k, t in T.items():
    ti = t.pop("tics_hasta_interrupcion"); da = t.pop("distancia_al_aceptar")
    t["fraccion_llegada"] = round(t["llegadas"] / t["aceptadas"], 3) if t["aceptadas"] else None
    t["tics_hasta_interrupcion_mediana"] = st.median(ti) if ti else None; t["interrumpidas_en_24_tics_o_menos"] = sum(1 for x in ti if x <= 24); t["distancia_al_aceptar_mediana"] = st.median(da) if da else None
for b in ("MIENTE", "HONESTA"):
    tt = [t for k, t in T.items() if k.startswith(b)]; ac = sum(t["aceptadas"] for t in tt); ll = sum(t["llegadas"] for t in tt); vd = sum(t["vidas_dia"] for t in tt)
    T[f"{b} · las dos"] = {"vidas_dia": vd, "aceptadas": ac, "llegadas": ll, "aciertos": sum(t["aciertos"] for t in tt), "interrumpidas": sum(t["interrumpidas"] for t in tt), "no_llego": sum(t["no_llego"] for t in tt),
                           "fraccion_llegada": round(ll / ac, 3) if ac else None, "llegadas_por_vida_dia": round(ll / vd, 3), "evaluaciones_por_serie_estimadas": round(ll / vd * 2 * 13, 1)}
    par = [("10", "11")] if b == "MIENTE" else [("12", "13")]; P = []
    for d, v in R.items():
        for a1, a2 in par:
            l1 = len(v["P7_66"][a1]["llegadas"]) > 0; l2 = len(v["P7_66"][a2]["llegadas"]) > 0
            P.append({"dia": d, "llegadas": len(v["P7_66"][a1]["llegadas"]) + len(v["P7_66"][a2]["llegadas"]), "juntas": l1 and l2, "una_sola": l1 != l2, "aceptadas": len(v["P7_66"][a1]["aceptadas"]) + len(v["P7_66"][a2]["aceptadas"])})
    T[f"{b} · por pareja"] = {"parejas_dia": len(P), "llegadas_por_pareja_dia": round(sum(p["llegadas"] for p in P) / len(P), 3), "llegan_juntas": sum(p["juntas"] for p in P), "llega_una_sola": sum(p["una_sola"] for p in P), "detalle": P}


def gif(d, sl, x, out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib.animation import FuncAnimation, PillowWriter
    f = os.path.join(L, d, "logs", f"policy_agent_{sl}.log"); Tk = {}; muro = set(); sli = int(sl)
    for l in open(f, errors="replace"):
        if l.startswith('{"k":"static_map"') and not muro:
            m = json.loads(l); duros = {c for c, v in m["legend"].items() if v in ("wall", "rock", "fortress_wall")}
            muro = {(xx, yy) for yy, fila in enumerate(m["filas"]) for xx, ch in enumerate(fila) if ch in duros}
        elif l.startswith('{"k":"tick"'):
            r = json.loads(l)
            if r.get("phase") == "live" and x["t_aceptada"] <= r["tick"] <= x["tick"] + 1:
                Rg = r.get("RADIOGRAFIA") or {}; Tk[r["tick"]] = {"pos": tuple(r["pos"]), "hp": r.get("hp"), "el": Rg.get("elegido"), "ag": [(a.get("slot"), tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos")],
                                                                   "kits": [tuple(i["pos"]) for i in (r.get("ve_items") or []) if i.get("id") == "first_aid" and i.get("pos")]}
    ts = sorted(Tk)[::2] or sorted(Tk); dest = tuple(x["destino"]); pts = [Tk[t]["pos"] for t in ts] + [dest]
    cx = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2; cy = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2; Rr = max(9, max(max(p[0] for p in pts) - min(p[0] for p in pts), max(p[1] for p in pts) - min(p[1] for p in pts)) / 2 + 4)
    fig, ax = plt.subplots(figsize=(5.4, 5.6))
    def frame(i):
        t = ts[i]; w = Tk[t]; ax.clear(); ax.set_xlim(cx - Rr, cx + Rr); ax.set_ylim(cy + Rr, cy - Rr); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        mx = [p for p in muro if abs(p[0] - cx) <= Rr + 1 and abs(p[1] - cy) <= Rr + 1]
        if mx: ax.scatter([p[0] for p in mx], [p[1] for p in mx], s=30, marker="s", c="#d9d9d6")
        ax.scatter([dest[0]], [dest[1]], s=260, marker="*", c="#f39c12", label="destino")
        if w["kits"]: ax.scatter([p[0] for p in w["kits"]], [p[1] for p in w["kits"]], s=120, marker="P", c="#2e8b57", label="botiquín")
        ri = [p for s, p in w["ag"] if s not in (sli, sli ^ 1)]; he = [p for s, p in w["ag"] if s == sli ^ 1]
        if ri: ax.scatter([p[0] for p in ri], [p[1] for p in ri], s=90, c="#c0392b", label="rival")
        if he: ax.scatter([p[0] for p in he], [p[1] for p in he], s=90, c="#5dade2", label="hermana")
        tr = [Tk[tt]["pos"] for tt in ts[:i + 1]]; ax.plot([p[0] for p in tr], [p[1] for p in tr], c="#888", lw=1)
        ax.scatter([w["pos"][0]], [w["pos"][1]], s=140, c="#141414", label=f"ella ({HER[sl]})")
        ax.set_title(f"{BRAZO[sl]} · {d} · tic {t} (+{t - x['t_aceptada']}) · vida {w['hp']} · {x.get('cierre', 'llegada')}\nelige: {w['el']}", fontsize=9); ax.legend(loc="lower left", fontsize=7)
    FuncAnimation(fig, frame, frames=len(ts)).save(out, writer=PillowWriter(fps=6)); plt.close(fig)
    return {"gif": os.path.basename(out), "dia": d, "asiento": sl, "brazo": BRAZO[sl], "hermana": HER[sl], "destino": list(dest), "tic_aceptada": x["t_aceptada"], "tic_juicio": x["tick"], "tics": x["tics"], "cierre": x.get("cierre", "llegada"), "acierto_recursos": x.get("acierto_recursos"), "fotogramas": len(ts)}


rnd = random.Random(66); G = []
for b in ("MIENTE", "HONESTA"):
    cands = [y for y in cerrados if BRAZO[y[1]] == b]
    if cands: d, sl, x = rnd.choice(cands); G.append(gif(d, sl, x, os.path.join(AQUI, f"P7_66b_gif_{b.lower()}.gif")))
FIG = os.path.join(os.path.dirname(AQUI), "figuras"); os.makedirs(FIG, exist_ok=True)
for g in G: shutil.copy(os.path.join(AQUI, g["gif"]), os.path.join(FIG, g["gif"]))
C = json.load(open(os.path.join(AQUI, "P7_66_tramo.json")))
out = {"por_brazo_y_hermana": T, "gifs": G, "tramo_P7_65": C, "dias": len(R)}
json.dump(out, open(os.path.join(AQUI, "P7_66b_banco.json"), "w"), ensure_ascii=False, indent=1); print(json.dumps(out, ensure_ascii=False, indent=1)[:3500])

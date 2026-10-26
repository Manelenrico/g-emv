"""[P7-65] DIAGNOSTICO POSTERIOR AL SELLO (descriptivo; no cambia ningun PASA o NO PASA). Pedido por Manel el 16-oct.
  2. (lo que eligio: solo tics con 2 o mas candidatos) Las evaluaciones de la falsa SIN cogida entre aceptar y juzgar (S2): en el tic de aceptar y en la ventana (aceptar -> juicio): botiquin a la vista (ve_items) y su distancia
     (al alcance = a <= 1 casilla), mochila (botiquines que lleva y si le cabe otro), rival cerca (a <= 4 casillas, ve_agentes que no son ella ni su hermana), y que hizo el cuerpo en la
     ventana (el candidato elegido de la radiografia, sin la direccion). Por hermana.
  3. GIFs (matplotlib, de los datos crudos del diario): 3 evaluaciones sin cogida elegidas al azar con semilla 65, de la aceptacion al juicio: la criatura, su hermana, los botiquines
     y los rivales visibles, las paredes del mapa.
  4. Muertes por brazo y hermana (muerte = el juego la elimina, `final.reason == "eliminated"`; aparte, la regla heredada de P7-56: ultimo tic vivo < 14000), con su error tipico por
     criatura (serie x brazo x asiento: fraccion de dias muerta), y la causa (origen del ultimo dano: "zone" = la zona / el fuego; P<n> = otro agente). Para cada hermana: si muere mas en los
     480 tics que siguen a aceptar una invitacion VERDADERA que en el resto de su vida (muertes por cada 10.000 tics en riesgo, dentro y fuera de esas ventanas).
  python3 diagnostico_P7_65.py -> P7_65_diagnostico.json, P7_65_gif_<n>.gif"""
import collections, glob, json, math, os, random, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI); sys.argv = sys.argv[:1]
import analiza_P7_65 as A          # las mismas vidas, invitaciones y falsas que el informe sellado
HER = A.HERMANA; VENT = 480
def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
def base(nombre): return nombre.split("_")[0] if nombre and nombre.startswith(("move", "paso", "atacar", "huir")) else (nombre or "?")


def ticks_completos(p, sl):
    f = glob.glob(os.path.join(RUNS, f"P765_s{p[0]}_d{p[1]}_{p[2]}_*", f"*policy_agent_{sl}.art.log"))[0]; T = {}; fin = None; mapa = None
    for l in open(f, errors="replace"):
        if l.startswith('{"k":"tick"'):
            r = json.loads(l)
            if r.get("phase") != "live": continue
            R = r.get("RADIOGRAFIA") or {}
            T[r["tick"]] = {"pos": tuple(r.get("pos") or (0, 0)), "hp": float(r.get("hp") or 0), "items": [(it["id"], tuple(it["pos"])) for it in (r.get("ve_items") or []) if it.get("pos")],
                            "agentes": [(a.get("slot"), tuple(a["pos"])) for a in (r.get("ve_agentes") or []) if a.get("pos")], "pack": r.get("pack") or [], "el": R.get("elegido"), "ncand": int(R.get("n_cand") or 0),
                            "dano": [(d.get("source"), float(d.get("amount") or 0)) for d in (r.get("damage_taken") or [])]}
        elif l.startswith('{"k":"final"'): fin = json.loads(l)
        elif l.startswith('{"k":"static_map"') and mapa is None: mapa = json.loads(l)
    return T, fin, mapa


def cabe_botiquin(pack, stack_max=2):
    return any(s is None for s in pack) or any(isinstance(s, dict) and s.get("id") == "first_aid" and int(s.get("n") or 1) < stack_max for s in pack)


def sin_cogida():
    out = []
    for k, v, e in A.falsas(False):
        ts_acc = [t for t in v["acc"].get(v["pos"], []) if t <= e["tick"]]
        if not ts_acc: continue
        t0 = max(ts_acc); t1 = e["tick"]; ts = sorted(t for t in v["T"] if t0 <= t <= t1)
        if any(v["T"][b][1] > v["T"][a][1] for a, b in zip(ts, ts[1:])): continue
        out.append((k, t0, t1, e))
    return out


def punto2(S2):
    R = {}; cache = {}
    for k, t0, t1, e in S2:
        key = (k[0], k[1], k[2], k[3])
        if key not in cache: cache = {key: ticks_completos(key, k[3])}
        T, _, _ = cache[key]; sl = k[3]; her = HER[sl]; r = R.setdefault(her, collections.Counter()); el = R.setdefault(her + "_elegido", collections.Counter())
        a = T.get(t0) or T[min(T, key=lambda t: abs(t - t0))]
        kits = [p for i, p in a["items"] if i == "first_aid"]; dk = min((cheb(a["pos"], p) for p in kits), default=None)
        riv = [cheb(a["pos"], p) for s, p in a["agentes"] if s not in (sl, sl ^ 1)]
        r["evaluaciones"] += 1; r["botiquin_a_la_vista_al_aceptar"] += bool(kits); r["botiquin_al_alcance_al_aceptar"] += bool(dk is not None and dk <= 1)
        r["le_cabe_otro_botiquin_al_aceptar"] += cabe_botiquin(a["pack"]); r["rival_a_4_o_menos_al_aceptar"] += bool(riv and min(riv) <= 4)
        win = [T[t] for t in sorted(T) if t0 <= t <= t1]
        r["botiquin_a_la_vista_en_la_ventana"] += any(any(i == "first_aid" for i, _ in w["items"]) for w in win)
        r["llego_al_botiquin_en_la_ventana"] += any(any(i == "first_aid" and cheb(w["pos"], p) == 0 for i, p in w["items"]) for w in win)
        r["rival_a_4_o_menos_en_la_ventana"] += any(any(s not in (sl, sl ^ 1) and cheb(w["pos"], p) <= 4 for s, p in w["agentes"]) for w in win)
        r["golpeada_en_la_ventana"] += any(w["dano"] for w in win)
        for w in win:
            if w["ncand"] >= 2: el[base(w["el"])] += 1          # solo los tics con eleccion de verdad (con un solo candidato, noop es forzado)
    out = {}
    for her in ("valiente", "prudente"):
        r = R.get(her, collections.Counter()); n = r["evaluaciones"]
        out[her] = {"evaluaciones": n, **{k: {"n": v, "fraccion": round(v / n, 3) if n else None} for k, v in r.items() if k != "evaluaciones"},
                    "lo_que_eligio_en_la_ventana": [(k2, round(v2 / max(1, sum(R.get(her + '_elegido', {}).values())), 3)) for k2, v2 in R.get(her + "_elegido", collections.Counter()).most_common(6)]}
    return out


def gifs(S2, n=3, semilla=65):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt; from matplotlib.animation import FuncAnimation, PillowWriter
    elegidas = random.Random(semilla).sample(S2, n); hechos = []
    for j, (k, t0, t1, e) in enumerate(elegidas, 1):
        T, fin, mapa = ticks_completos((k[0], k[1], k[2], k[3]), k[3]); sl = k[3]
        ts = [t for t in sorted(T) if t0 <= t <= t1][::4]
        muro = set()
        if mapa:
            leg = mapa.get("legend") or {}; duros = {c for c, v in leg.items() if v in ("wall", "rock", "fortress_wall")}
            for y, fila in enumerate(mapa.get("filas") or []):
                for x, ch in enumerate(fila):
                    if ch in duros: muro.add((x, y))
        xs = [T[t]["pos"][0] for t in ts]; ys = [T[t]["pos"][1] for t in ts]; cx, cy = st.mean(xs), st.mean(ys); R = max(8, max(max(xs) - min(xs), max(ys) - min(ys)) // 2 + 6)
        fig, ax = plt.subplots(figsize=(5.4, 5.6))
        def frame(i):
            t = ts[i]; w = T[t]; ax.clear(); ax.set_xlim(cx - R, cx + R); ax.set_ylim(cy + R, cy - R); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
            mx = [p for p in muro if abs(p[0] - cx) <= R + 1 and abs(p[1] - cy) <= R + 1]
            if mx: ax.scatter([p[0] for p in mx], [p[1] for p in mx], s=30, marker="s", c="#d9d9d6")
            k_ = [p for i_, p in w["items"] if i_ == "first_aid"]
            if k_: ax.scatter([p[0] for p in k_], [p[1] for p in k_], s=120, marker="P", c="#2e8b57", label="botiquín")
            ri = [p for s, p in w["agentes"] if s not in (sl, sl ^ 1)]; he = [p for s, p in w["agentes"] if s == sl ^ 1]
            if ri: ax.scatter([p[0] for p in ri], [p[1] for p in ri], s=90, c="#c0392b", label="rival")
            if he: ax.scatter([p[0] for p in he], [p[1] for p in he], s=90, c="#5dade2", label="hermana")
            tr = [T[tt]["pos"] for tt in ts[:i + 1]]; ax.plot([p[0] for p in tr], [p[1] for p in tr], c="#888", lw=1)
            ax.scatter([w["pos"][0]], [w["pos"][1]], s=140, c="#141414", label=f"ella ({HER[sl]})")
            ax.set_title(f"s{k[0]} d{k[1]} {k[2]} · tic {t} (+{t - t0}) · vida {w['hp']:.0f}\nelige: {w['el']}", fontsize=9); ax.legend(loc="lower left", fontsize=7)
        an = FuncAnimation(fig, frame, frames=len(ts)); out = os.path.join(AQUI, f"P7_65_gif_{j}.gif"); an.save(out, writer=PillowWriter(fps=8)); plt.close(fig)
        hechos.append({"gif": os.path.basename(out), "serie": k[0], "dia": k[1], "brazo": k[2], "hermana": HER[sl], "tic_aceptada": t0, "tic_juicio": t1, "fotogramas": len(ts), "juicio": e.get("fuente"), "acierto": (e.get("acierto") or {}).get("cuerpo")})
    return hechos


def punto4():
    M = {}; filas = []
    for p in A.E["peticiones"]:
        if p["estado"] != "completed": continue
        for sl in (10, 11):
            k = (p["serie"], p["dia"], p["brazo"], sl)
            if k not in A.V: continue
            T, fin, _ = ticks_completos(k, sl); v = A.V[k]; ts = sorted(T)
            elim = (fin or {}).get("reason") == "eliminated"; ult = ts[-1] if ts else 0
            danos = [(t, s) for t in ts for s, a in T[t]["dano"] if a > 0]; causa = None
            if elim and danos: s = danos[-1][1]; causa = "zona / fuego" if s == "zone" else ("hermana" if s == f"P{sl ^ 1}" else "otro agente")
            ventanas = []
            for i, inv in enumerate(v["inv"]):
                if inv.get("falsa") or not A.verdad(inv["accion"], {"anillo": inv.get("anillo"), "calma": inv.get("calma")}, inv.get("cuerpo")): continue
                ventanas += [(t, t + VENT) for t in v["acc"].get(i, [])]
            dentro = sum(1 for t in ts if any(a <= t <= b for a, b in ventanas)); muerte_dentro = elim and any(a <= ult <= b for a, b in ventanas)
            filas.append({"serie": k[0], "dia": k[1], "brazo": k[2], "hermana": HER[sl], "eliminada": elim, "regla_P7_56": ult < 14000, "causa": causa, "tics": len(ts), "tics_en_ventana": dentro, "muerte_en_ventana": muerte_dentro})
    for b in A.BRAZOS:
        for sl in (10, 11):
            F = [x for x in filas if x["brazo"] == b and x["hermana"] == HER[sl]]; cri = [st.mean([x["eliminada"] for x in F if x["serie"] == S]) for S in A.SERIES]
            dentro_t = sum(x["tics_en_ventana"] for x in F); fuera_t = sum(x["tics"] - x["tics_en_ventana"] for x in F); md = sum(x["muerte_en_ventana"] for x in F); mf = sum(1 for x in F if x["eliminada"] and not x["muerte_en_ventana"])
            M[f"{b} · {HER[sl]}"] = {"vidas": len(F), "eliminada": sum(x["eliminada"] for x in F), "fraccion_por_serie": [round(c, 3) for c in cri], "media": round(st.mean(cri), 3), "ee_por_criatura": round(st.stdev(cri) / math.sqrt(len(cri)), 3),
                                     "regla_P7_56_ultimo_tic_lt_14000": sum(x["regla_P7_56"] for x in F), "causas": dict(collections.Counter(x["causa"] for x in F if x["eliminada"])),
                                     "tras_seguir_una_verdadera": {"tics_en_riesgo": dentro_t, "muertes": md, "por_10000_tics": round(1e4 * md / dentro_t, 2) if dentro_t else None},
                                     "el_resto_de_la_vida": {"tics_en_riesgo": fuera_t, "muertes": mf, "por_10000_tics": round(1e4 * mf / fuera_t, 2) if fuera_t else None}}
    return M, filas


if __name__ == "__main__":
    S2 = sin_cogida(); R = {"sin_cogida": len(S2), "punto2": punto2(S2)}
    R["gifs"] = gifs(S2); R["muertes"], filas = punto4()
    json.dump(R, open(os.path.join(AQUI, "P7_65_diagnostico.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in R.items()}, ensure_ascii=False)[:4000])

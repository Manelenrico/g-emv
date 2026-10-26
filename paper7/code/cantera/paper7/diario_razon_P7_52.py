"""[P7-52] EL DIARIO PARA LA RAZON (capitulo 5, paso 1; diseno de Manel): por criatura y dia, a partir del diario crudo del campo P7-50 (sin tocar nada del campo):
  (a) RESUMEN: estado al empezar y al acabar en las tres dimensiones (cuerpo = vida y dolor del cuerpo; recursos = riqueza W y dolor de recursos; vinculo = B y dolor del vinculo),
      vida perdida, que probo (huellas), que aprendio (creencias al empezar y al acabar), como acabo (puesto, muerte).
  (b) MOMENTOS CLAVE: lo raro o lo mas intenso: cada prueba (apertura y cierre), cada golpe grande, las mayores subidas de malestar, la racha mas larga de empujes contra una
      casilla vacia, la muerte; cada uno con TODO su contexto: foto emocional (dolor F/R/S, positivo, d) y equilibrio (vida, W, B, P), donde estaba (casilla, anillo), quien habia
      cerca (hermana, rivales: distancia, mano, cuerpo, red), que llevaba (mano, zurron, cuerpo) y que hacia (elegido, intencion, resultado), que habia alrededor (cosas a <= 5),
      que acababa de pasar (golpes y eventos de los ultimos 48 tics, partes de la hermana). Todo en el idioma del cuerpo; nada del manual del juego.
  python3 diario_razon_P7_52.py --candidatos            lista vidas con choques sin cuerpo, botiquin cortado, red/camuflaje sin efecto
  python3 diario_razon_P7_52.py --texto S D BRAZO SLOT  escribe el diario para la razon en pantalla (y en _P7_52_tmp/diario_s<S>_d<D>_<BRAZO>_<SLOT>.md)"""
import glob, json, math, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); RUNS = os.path.join(RAIZ, "paintball", "runs"); sys.path.insert(0, AQUI)
NOM = {"first_aid": "botiquín", "rations": "ración", "net": "red", "camouflage": "camuflaje", "backpack": "mochila", "none": "nada", None: "nada"}
DIR = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
E = json.load(open(os.path.join(AQUI, "P7_50_estado.json")))


def foto_de_radio(radio):
    a = (radio or {}).get("ahora") or {}; filas = a.get("filas") or {}
    if not filas: return None
    f = {"dolor_F": 0.0, "dolor_R": 0.0, "dolor_S": 0.0, "positivo": 0.0, "d": float((radio or {}).get("d_ahora") or 0.0)}
    for fila in filas.values():
        if not isinstance(fila, dict): continue
        if fila.get("signo") == "-":
            for eje, k in (("F", "dolor_F"), ("R", "dolor_R"), ("S", "dolor_S")): f[k] += float(fila.get(eje) or 0.0)
        else: f["positivo"] += float(fila.get("M") or 0.0)
    return {k: round(v, 3) for k, v in f.items()}


FUENTE = {"zone": "el anillo de fuego", "flood": "la riada"}; BANDA = {"healthy": "sana", "hurt": "herida", "critical": "casi muerta", "wounded": "herida"}
def fuente(x): x = str(x); return FUENTE.get(x, ("rival " + x) if x.startswith("P") else x)
def parte_corto(t):
    import re
    m = re.match(r"^E[12] P(\d+) t(\d+) (\d+),(\d+) h([\d.]+) v([01]) b(\d+) a([01])", t or "")
    return (f"vida {m.group(5)}, {m.group(7)} botiquines, {'con agresor' if m.group(8) == '1' else 'sin agresor'}, en {m.group(3)},{m.group(4)}" + (", envenenada" if m.group(6) == "1" else "")) if m else "ninguno"


def nombre(x):
    if isinstance(x, dict): x = x.get("id")
    return NOM.get(x, str(x))


def carpeta(S, d, brazo):
    p = next((p for p in E["peticiones"] if p["serie"] == S and p["dia"] == d and p["brazo"] == brazo), None)
    return (glob.glob(os.path.join(RUNS, f"P750_s{S}_d{d}_{brazo}_{p['semilla']}"))[0] if p else None), p


def lee(S, d, brazo, slot, archivo=None):
    if archivo: c, f = os.path.dirname(archivo), archivo
    else: c, p = carpeta(S, d, brazo); f = glob.glob(os.path.join(c, f"*policy_agent_{slot}.art.log"))[0]
    T = []; H = []; AB = []; CU = {}; FIN = None; TEAM = None; REC = []; VIS = []; MUROS = []
    for line in open(f, errors="replace"):
        if line.startswith('{"k":"tick"'):
            r = json.loads(line)
            if r.get("phase") != "live": continue
            if TEAM is None: TEAM = r.get("team")
            T.append(r)
        elif line.startswith('{"k":"P7_huella"'): H.append(json.loads(line))
        elif line.startswith('{"k":"P7_33_prueba"'): AB.append(json.loads(line))
        elif line.startswith('{"k":"P7_cuaderno"'): r = json.loads(line); CU[r.get("momento")] = r
        elif line.startswith('{"k":"final"'): FIN = json.loads(line)
        elif line.startswith('{"k":"P7_48_contado"'): REC.append(json.loads(line))
        elif line.startswith('{"k":"P7_48_visto"'):
            r = json.loads(line)
            if r.get("estado") == "apuntado": VIS.append(r)
        elif line.startswith('{"k":"P7_43_muro"'): MUROS.append(json.loads(line))
    return {"T": T, "H": H, "AB": AB, "CU": CU, "FIN": FIN, "team": TEAM, "REC": REC, "VIS": VIS, "MUROS": MUROS, "pareja": slot ^ 1, "carpeta": os.path.basename(c)}


def creencias(cu):
    c = ((cu or {}).get("contenido") or {}).get("creencias") or {}; out = {}
    for o, nom in (("first_aid", "botiquín"), ("rations", "ración"), ("net", "red"), ("camouflage", "camuflaje")):
        x = c.get(o) or {}; den = x.get("dentro") if isinstance(x.get("dentro"), dict) else None; fue = x.get("fuera") if isinstance(x.get("fuera"), dict) else None
        out[nom] = {"dentro": (den or {}).get("cuerpo"), "fuera": (fue or {}).get("cuerpo"), "recursos": (den or fue or {}).get("recursos"), "vinculo": (den or fue or {}).get("vinculo"), "ignorancia": x.get("ignorancia"), "recuerdos": x.get("pesos_vividos")}
    return out


def s_(t): return f"{t / 24:.0f} s"
def num(x, d=1): return "?" if x is None else f"{x:.{d}f}"


def contexto(V, i, titulo):
    """el momento i (indice en T) con todo su contexto, en el idioma del cuerpo."""
    T = V["T"]; r = T[i]; ra = r.get("RADIOGRAFIA") or {}; ah = ra.get("ahora") or {}; foto = foto_de_radio(ra) or {}; pos = tuple(r.get("pos") or (0, 0)); z = r.get("zona") or {}
    filas = sorted(((k, v.get("M", 0)) for k, v in (ah.get("filas") or {}).items() if isinstance(v, dict) and v.get("M")), key=lambda x: -x[1])[:4]
    ag = []
    for a in (r.get("ve_agentes") or []):
        if not a.get("pos"): continue
        dst = max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])); quien = "mi hermana" if a.get("slot") == V["pareja"] else f"rival (equipo {a.get('team')})"
        ag.append(f"{quien} a {dst} casillas, {BANDA.get(a.get('hp_band'), a.get('hp_band', '?'))}, mano {nombre(a.get('hand'))}, cuerpo {nombre(a.get('body'))}{', atrapado en una red' if a.get('netted') else ''}{', envenenado' if a.get('poisoned') else ''}{', haciendo algo' if a.get('channeling') else ''}")
    items = [f"{nombre(it.get('id'))}×{it.get('n', 1)} a {max(abs(it['pos'][0] - pos[0]), abs(it['pos'][1] - pos[1]))}" for it in (r.get("ve_items") or []) if it.get("pos") and max(abs(it["pos"][0] - pos[0]), abs(it["pos"][1] - pos[1])) <= 5][:8]
    golpes = []
    for q in T[max(0, i - 48):i + 1]:
        for g in (q.get("damage_taken") or []): golpes.append(f"{g.get('amount')} de {fuente(g.get('source'))}")
    ev = [str(e)[:60] for q in T[max(0, i - 48):i + 1] for e in (q.get("eventos") or [])][:4]
    partes = [m.get("text") for q in T[max(0, i - 96):i + 1] for m in (q.get("chat") or []) if m.get("from") == V["pareja"] and str(m.get("text", "")).startswith("E")][-1:]
    pack = [nombre(x) for x in (r.get("pack") or []) if x]; hp = r.get("hp"); anillo = math.dist(pos, tuple(z.get("center") or (24, 24)))
    enc = f"{'dentro' if anillo <= float(z.get('radius') or 99) else 'FUERA'} del anillo (radio {z.get('radius')}, se encoge a {z.get('next_radius')} en {s_(max(0, (z.get('shrink_tick') or 0) - r['tick']))})"
    lines = [f"- **{titulo}** (segundo {s_(r['tick'])}, tic {r['tick']})",
             f"  - cómo me siento: dolor del cuerpo {num(foto.get('dolor_F'), 2)}, dolor de recursos {num(foto.get('dolor_R'), 2)}, dolor del vínculo {num(foto.get('dolor_S'), 2)}, atracción {num(foto.get('positivo'), 2)}, malestar total d = {num(foto.get('d'), 2)}; lo que más pesa: {', '.join(f'{k} {v:.2f}' for k, v in filas) or 'nada'}",
             f"  - equilibrio: vida {hp} de 100, riqueza W {num(ah.get('W'), 2)}, vínculo B {num(ah.get('B'), 2)}, hermana presente P {num(ah.get('P'), 1)}",
             f"  - dónde: casilla {pos[0]},{pos[1]}, {enc}",
             f"  - quién hay cerca: {'; '.join(ag) or 'nadie a la vista'}",
             f"  - qué llevo: mano {nombre(r.get('hand'))}, zurrón [{', '.join(pack) or 'vacío'}], cuerpo {nombre(r.get('body'))}",
             f"  - qué hago: elegido «{ra.get('elegido')}», intención {json.dumps(r.get('intencion'))[:60]}, resultado «{r.get('action_result')}»",
             f"  - qué hay alrededor (≤ 5 casillas): {', '.join(items) or 'nada'}",
             f"  - qué acaba de pasar (últimos 2 s): golpes [{', '.join(golpes) or 'ninguno'}]; eventos {ev or 'ninguno'}; último parte de la hermana: {parte_corto(partes[0]) if partes else 'ninguno'}"]
    return "\n".join(lines)


def momentos(V):
    T = V["T"]; idx = {r["tick"]: i for i, r in enumerate(T)}; M = []
    def cerca(t): return idx.get(t, min(range(len(T)), key=lambda i: abs(T[i]["tick"] - t)))
    for h in V["H"]:
        i0 = cerca(int(h["t0"])); i1 = cerca(int(h.get("t_fin") or h["t0"])); o = NOM.get(h.get("objeto") or "first_aid", h.get("objeto")); ef = h.get("efecto") or {}
        M.append((h["t0"], f"PRUEBA de {o}: abro la ventana", i0))
        cierre = f"PRUEBA de {o}: cierro. Vida {h.get('hp0')} → {h.get('hp_fin')}; lo que hizo (descontado lo esperado): cuerpo {num(ef.get('cuerpo'))}, recursos {num(ef.get('recursos'))}, vínculo {num(ef.get('vinculo'))}" + ("; CORTADA por un golpe" if h.get("corte") else "") + (f"; en la ventana recibí {h.get('dano_total')} de daño de {', '.join(fuente(x) for x in (h.get('fuentes_conocidas') or [])) or 'no sé quién'}" if h.get("corte") else "") + ("; la vida tocó techo (lo ganado es al menos esto)" if h.get("al_menos") else "")
        M.append((int(h.get("t_fin") or h["t0"]), cierre, i1))
    # golpes grandes (los 3 mayores por fuente, agrupados por 48 tics)
    gol = []
    for i, r in enumerate(T):
        s = sum(float(g.get("amount") or 0) for g in (r.get("damage_taken") or []))
        if s > 0: gol.append((s, i, [g.get("source") for g in r["damage_taken"]]))
    gol.sort(reverse=True); usados = []
    for s, i, src in gol:
        if any(abs(T[i]["tick"] - T[j]["tick"]) < 48 for j in usados): continue
        usados.append(i); M.append((T[i]["tick"], f"GOLPE de {s:.1f} de vida, de {', '.join(fuente(x) for x in src)}", i))
        if len(usados) >= 3: break
    # saltos de malestar
    d = [float((r.get("RADIOGRAFIA") or {}).get("d_ahora") or 0) for r in T]; saltos = sorted(((d[i] - d[i - 24], i) for i in range(24, len(T))), reverse=True)[:6]; us2 = []
    for dd, i in saltos:
        if dd <= 0.5 or any(abs(i - j) < 120 for j in us2) or any(abs(T[i]["tick"] - T[j]["tick"]) < 48 for j in usados): continue
        us2.append(i); M.append((T[i]["tick"], f"SUBIDA DEL MALESTAR: d {d[i - 24]:.2f} → {d[i]:.2f} en un segundo", i))
        if len(us2) >= 2: break
    # racha mas larga de empujes contra casilla vacia
    prev = None; rachas = []; cur = None
    for i, r in enumerate(T):
        if prev and r.get("action_result") == "blocked" and (prev.get("intencion") or {}).get("dir") in DIR:
            dx, dy = DIR[prev["intencion"]["dir"]]; hacia = (prev["pos"][0] + dx, prev["pos"][1] + dy)
            if not any(tuple(a.get("pos") or ()) == hacia for a in (r.get("ve_agentes") or [])):
                if cur and cur["hacia"] == hacia and r["tick"] - cur["t_ult"] <= 24: cur["n"] += 1; cur["t_ult"] = r["tick"]
                else:
                    if cur: rachas.append(cur)
                    cur = {"hacia": hacia, "i": i, "t0": r["tick"], "t_ult": r["tick"], "n": 1}
        prev = r
    if cur: rachas.append(cur)
    if rachas:
        rr = max(rachas, key=lambda x: x["n"])
        if rr["n"] >= 12: M.append((rr["t0"], f"EMPUJO {rr['n']} veces hacia la casilla {rr['hacia'][0]},{rr['hacia'][1]} y no avanzo, sin ver a nadie allí ({s_(rr['t_ult'] - rr['t0'])} seguidos)", rr["i"]))
    for m in V["MUROS"][:1]: M.append((m["tick"], f"DOY POR CERRADA la casilla {m['casilla'][0]},{m['casilla'][1]} tras {m.get('empujes')} empujes (3 s); la olvido en 30 s", cerca(m["tick"])))
    for v in V["VIS"][:2]: M.append((v["tick"], f"VEO a mi hermana usar {NOM.get(v.get('objeto'), v.get('objeto'))}: su vida {v.get('hacia')}; efecto que le veo en el cuerpo {num((v.get('efecto') or {}).get('cuerpo'))}", cerca(v["tick"])))
    for rc in V["REC"][:2]: M.append((rc["tick"], f"MI HERMANA ME CUENTA ({rc.get('via')}) lo que vivió con {NOM.get(rc.get('objeto'), rc.get('objeto'))}: cuerpo {num((rc.get('efecto') or {}).get('cuerpo'))}, recursos {num((rc.get('efecto') or {}).get('recursos'))}, vínculo {num((rc.get('efecto') or {}).get('vinculo'))}; lo creo con peso {rc.get('peso')}", cerca(rc["tick"])))
    if V["FIN"] and T[-1]["tick"] < 14000: M.append((T[-1]["tick"], f"MUERO (puesto {V['FIN'].get('placement')})", len(T) - 1))
    M.sort(key=lambda x: x[0]); return M[:14]


def texto(S, d, brazo, slot):
    V = lee(S, d, brazo, slot); T = V["T"]; r0, r1 = T[0], T[-1]
    def est(r):
        ra = r.get("RADIOGRAFIA") or {}; ah = ra.get("ahora") or {}; f = foto_de_radio(ra) or {}
        return f"vida {r.get('hp')} · dolor del cuerpo {num(f.get('dolor_F'), 2)} · riqueza W {num(ah.get('W'), 2)} · dolor de recursos {num(f.get('dolor_R'), 2)} · vínculo B {num(ah.get('B'), 2)} · dolor del vínculo {num(f.get('dolor_S'), 2)} · malestar d {num(f.get('d'), 2)}"
    perdida = sum(float(g.get("amount") or 0) for r in T for g in (r.get("damage_taken") or [])); fuentes = {}
    for r in T:
        for g in (r.get("damage_taken") or []): fuentes[fuente(g.get("source"))] = fuentes.get(fuente(g.get("source")), 0) + float(g.get("amount") or 0)
    c0, c1 = creencias(V["CU"].get("arranque")), creencias(V["CU"].get("fin")); quien = "valiente" if slot == 10 else "prudente"
    L = [f"# Diario de la hermana {quien} ({'comparte con su hermana' if brazo == 'COMPARTE' else 'no comparte'}), día {d} de la serie {S}", "",
         "## Resumen del día",
         f"- Al empezar: {est(r0)}", f"- Al acabar (segundo {s_(r1['tick'])}): {est(r1)}",
         f"- Vida perdida en el día: {perdida:.0f} ({', '.join(f'{k} {v:.0f}' for k, v in sorted(fuentes.items(), key=lambda x: -x[1])) or 'nada'})",
         f"- Cómo acabé: {'morí' if r1['tick'] < 14000 else 'viva al final'}; puesto {(V['FIN'] or {}).get('placement')} de 16 (mi pareja y yo contamos juntas); mi hermana {'murió' if r1.get('pareja_muerta') else 'viva'}",
         f"- Qué probé: " + ("; ".join(f"{NOM.get(h.get('objeto') or 'first_aid', h.get('objeto'))} (segundo {s_(h['t0'])}, {'cortada' if h.get('corte') else 'entera'}; cuerpo {num((h.get('efecto') or {}).get('cuerpo'))}, recursos {num((h.get('efecto') or {}).get('recursos'))}, vínculo {num((h.get('efecto') or {}).get('vinculo'))})" for h in V["H"]) or "nada"),
         f"- Qué me contó o vi de mi hermana: {len(V['REC'])} recuerdos contados, {len(V['VIS'])} vistos" if brazo == "COMPARTE" else "- Mi hermana y yo no nos contamos nada",
         "- Qué creo de las cosas (lo que hacen en mi cuerpo, dentro del anillo; ? = no lo sé; y cuánto ignoro, 1 = todo):"]
    for nom in ("botiquín", "ración", "red", "camuflaje"):
        a, b = c0.get(nom, {}), c1.get(nom, {}); L.append(f"  - {nom}: al empezar cuerpo {num(a.get('dentro'))} / ignorancia {num(a.get('ignorancia'), 2)} → al acabar cuerpo {num(b.get('dentro'))}, recursos {num(b.get('recursos'))}, vínculo {num(b.get('vinculo'))} / ignorancia {num(b.get('ignorancia'), 2)}")
    L += ["", "## Momentos clave (lo raro y lo más intenso, con todo su contexto)", ""]
    for t, tit, i in momentos(V): L.append(contexto(V, i, tit)); L.append("")
    return "\n".join(L), V


def candidatos():
    out = []
    for p in E["peticiones"]:
        c = glob.glob(os.path.join(RUNS, f"P750_s{p['serie']}_d{p['dia']}_{p['brazo']}_{p['semilla']}"))
        if not c: continue
        for sl in (10, 11):
            fs = glob.glob(os.path.join(c[0], f"*policy_agent_{sl}.art.log"))
            if not fs: continue
            H = []; blq = 0; T = 0
            for line in open(fs[0], errors="replace"):
                if line.startswith('{"k":"P7_huella"'): H.append(json.loads(line))
                elif line.startswith('{"k":"tick"') and '"blocked"' in line: blq += 1
            kit_cortado = sum(1 for h in H if (h.get("objeto") or "first_aid") == "first_aid" and h.get("corte") and float(h.get("dano_total") or 0) > 0)
            inutil0 = sum(1 for h in H if h.get("objeto") in ("net", "camouflage") and not h.get("corte") and abs(float((h.get("efecto") or {}).get("cuerpo") or 0)) < 1)
            g = (p.get("latencia") or {}).get(str(sl)) or {}
            out.append({"serie": p["serie"], "dia": p["dia"], "brazo": p["brazo"], "slot": sl, "huellas": len(H), "kit_cortado": kit_cortado, "inutil_sin_efecto": inutil0, "bloqueados_sin_cuerpo": g.get("bloqueados_sin_cuerpo"), "fraccion_sin_cuerpo": g.get("fraccion_sin_cuerpo")})
    return out


if __name__ == "__main__":
    a = sys.argv
    if "--candidatos" in a:
        C = candidatos(); json.dump(C, open(os.path.join(AQUI, "P7_52_candidatos.json"), "w"), indent=1)
        print("choques:", sorted(C, key=lambda x: -(x["bloqueados_sin_cuerpo"] or 0))[:4]); print("botiquin cortado:", [x for x in C if x["kit_cortado"]][:4]); print("inutil sin efecto:", [x for x in C if x["inutil_sin_efecto"]][:6])
    elif "--texto" in a:
        i = a.index("--texto"); S, d, b, sl = int(a[i + 1]), int(a[i + 2]), a[i + 3], int(a[i + 4]); t, V = texto(S, d, b, sl)
        os.makedirs(os.path.join(AQUI, "_P7_52_tmp"), exist_ok=True); open(os.path.join(AQUI, "_P7_52_tmp", f"diario_s{S}_d{d}_{b}_{sl}.md"), "w").write(t); print(t)

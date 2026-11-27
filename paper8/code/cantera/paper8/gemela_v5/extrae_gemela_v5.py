"""[P8] Prompt 138: lo que hace cada criatura cada día en las partidas ya jugadas del experimento v5 (valle_experimento_v5), para RG68r y su gemela RG068r
en la sequía y la sequía dura (40 semillas cada una: 160 partidas). Solo lee los registros: no juega nada ni llama a ningún modelo.
Por partida, criatura y día (solo los turnos en que está viva), de mundo.jsonl.gz, balance.jsonl.gz y criaturas.jsonl.gz:
  - cog_<origen>: comida cogida con éxito, por de dónde: huerto (una planta), matorral, árbol dulce (un matorral cuya comida entra con origen «dulce»),
    almacén, suelo; y aparte, de la despensa (no es comida nueva);
  - comida: comida comida; podrida: la comida que se le va de la bolsa sin comerla, darla, dejarla, ni que se la quiten (como diario_v2: el mundo no apunta
    la pudrición; si en el mismo turno coge una y se le pudre otra, no se ve);
  - dada_hermana, dada_vecina, recibida_hermana, recibida_vecina: comida dada y recibida con éxito;
  - quito_hermana, quito_vecina: comidas que ella le quitó a otra al ganar un empujón; le_quito_hermana, le_quito_vecina, le_quito_bestia: las que le quitaron;
  - emp_dados: empujones a otra criatura que el mundo hizo (no los «no está pegada»); emp_recibidos;
  - trabajando: turnos trabajando el huerto con éxito; andando: turnos que se movió con éxito; quieta: turnos de «quedarse»; dentro: turnos dentro de su casa
    (sitio «C» de balance.jsonl.gz, sin la puerta);
  - noche_dentro: si durmió dentro de su casa la noche de ese día (dormida y en su casa en más de la mitad de los turnos de la fase «noche»);
  - despensa: la comida en la despensa de su casa en el último turno del día (de criaturas.jsonl.gz; es de las dos hermanas);
  - hambre_suma y turnos (para el hambre media), hambre60 (algún turno con hambre > 60), bolsa_suma (comida en la bolsa, para la media).
Y las muertes de fin.json (criatura, día, causa). Guarda gemela_v5/dias_<variante>_<mundo>_<semilla>.json.
   python3 gemela_v5/extrae_gemela_v5.py   (las 160; o una: python3 gemela_v5/extrae_gemela_v5.py RG068r sequia 30121)"""
import gzip, json, os, sys
from collections import defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); EXP = "/Volumes/Mem G-EMV/valle_experimento_v5"
VARIANTES = ("RG68r", "RG068r"); MUNDOS = ("sequia", "sequia_dura"); SEM = range(30121, 30161); DIA = 400
her = lambda a: a[0] + ("2" if a[1] == "1" else "1")
CAMPOS = ("cog_huerto", "cog_matorral", "cog_dulce", "cog_almacen", "cog_suelo", "cog_despensa", "comida", "podrida", "dada_hermana", "dada_vecina", "recibida_hermana",
          "recibida_vecina", "quito_hermana", "quito_vecina", "le_quito_hermana", "le_quito_vecina", "le_quito_bestia", "emp_dados", "emp_recibidos", "trabajando", "andando",
          "quieta", "dentro", "noche_dormida_dentro", "noche_turnos", "hambre_suma", "turnos", "hambre60", "bolsa_suma",
          "gasto", "gasto_frio_fuera", "turnos_frio_fuera", "gasto_frio_dentro", "turnos_frio_dentro", "gasto_templado", "dormida")
CFGV = json.load(open(os.path.join(os.path.dirname(os.path.dirname(AQUI)), os.pardir, "valle", "config_valle.json"), encoding="utf-8"))
NUT = float(CFGV["objetos"]["comida"]["nutricion"]); TEMP = CFGV["temperatura"]
FRIAS = {f for f, g in TEMP["fuera"].items() if g < TEMP["confort"][0]}           # (las fases en que fuera de casa hace frío: el hambre sube más, mundo.py:682-684)

def una(x):
    v, mu, s = x; d = os.path.join(EXP, f"{v}_{mu}+sabores_s{s}_d40"); out = os.path.join(AQUI, f"dias_{v}_{mu}_{s}.json")
    if os.path.exists(out): return out
    R = defaultdict(lambda: defaultdict(lambda: {k: 0 for k in CAMPOS})); prev = {}; fase = {}; prevh = {}; G = {}
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        m = json.loads(l); t = m["turno"]; dia = t // DIA; A = m["agentes"]; fase[t] = m.get("fase")
        quitan = defaultdict(bool)
        for e in m.get("eventos") or []:
            if "empujon" in e and e.get("gana"):
                g_ = e["gana"]; p_ = e["a"] if g_ == e["empujon"] else e["empujon"]; n = (e.get("soltado") or []).count("comida"); quitan[p_] = True
                if not A.get(g_, {}).get("cuerpo", {}).get("muerta"): R[g_][dia]["quito_hermana" if p_ == her(g_) else "quito_vecina"] += n
                R[p_][dia]["le_quito_hermana" if g_ == her(p_) else "le_quito_vecina"] += n
            if "empujon" in e: R[e["a"]][dia]["emp_recibidos"] += 1
            if e.get("bestia_roba"): R[e["bestia_roba"]][dia]["le_quito_bestia"] += (e.get("que") or []).count("comida"); quitan[e["bestia_roba"]] = True
        for a, g in A.items():
            if a == "bestia" or not isinstance(g, dict) or "cuerpo" not in g: continue
            if g["cuerpo"]["muerta"]: prev.pop(a, None); continue
            z = R[a][dia]; k = g.get("accion"); ok = g.get("resultado") == "ok"; b = g.get("bolsa") or []
            z["turnos"] += 1; h = float(g["cuerpo"]["hambre"]); z["hambre_suma"] += h; z["hambre60"] = int(z["hambre60"] or h > 60); z["bolsa_suma"] += b.count("comida")
            if k == "coger" and ok and g.get("tipo") == "comida":
                de = g.get("de")
                if de == "matorral" and (g.get("bolsa_origen") or [None])[-1] == "dulce": z["cog_dulce"] += 1
                elif de in ("planta", "matorral", "almacen", "suelo", "despensa"): z["cog_" + {"planta": "huerto"}.get(de, de)] += 1
            if k == "comer" and ok and g.get("tipo") == "comida": z["comida"] += 1
            if k == "dar" and ok and g.get("tipo", "comida") == "comida" and g.get("objetivo"):
                o = g["objetivo"]; z["dada_hermana" if o == her(a) else "dada_vecina"] += 1; R[o][dia]["recibida_hermana" if a == her(o) else "recibida_vecina"] += 1
            if k == "empujar" and g.get("objetivo") and not str(g["objetivo"]).startswith("bestia") and not str(g.get("resultado") or "").startswith("no:"): z["emp_dados"] += 1
            if k == "trabajar" and ok: z["trabajando"] += 1
            if k == "mover" and ok: z["andando"] += 1
            if k == "quedarse": z["quieta"] += 1
            if a in prev:
                baja = prev[a] - b.count("comida")
                if baja > 0 and not (ok and k in ("comer", "dar", "dejar")) and not quitan[a]: z["podrida"] += baja
            prev[a] = b.count("comida")
            if a in prevh: G[(a, t)] = h - prevh[a] + (NUT if (k == "comer" and ok and g.get("tipo") == "comida") else 0.0); z["gasto"] += G[(a, t)]
            prevh[a] = h; z["dormida"] += bool(g["cuerpo"].get("dormida"))
    for l in gzip.open(os.path.join(d, "balance.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["t"]; dia = t // DIA
        for a, c in x["c"].items():
            if a not in R or dia not in R[a]: continue
            z = R[a][dia]; z["dentro"] += c[5] == "C"; gs = G.get((a, t))
            if gs is not None:
                k_ = "templado" if fase.get(t) not in FRIAS else ("frio_dentro" if c[5] in ("C", "O") else "frio_fuera")
                z["gasto_" + k_] += gs
                if k_ != "templado": z["turnos_" + k_] += 1
            if fase.get(t) == "noche": z["noche_turnos"] += 1; z["noche_dormida_dentro"] += c[5] == "C" and bool(c[6])
    desp = {}
    for l in gzip.open(os.path.join(d, "criaturas.jsonl.gz"), "rt", encoding="utf-8"):
        x = json.loads(l); t = x["turno"]
        if t % DIA == DIA - 1 and x.get("despensas"): desp[t // DIA] = {k: v.get("comida", 0) for k, v in x["despensas"].items()}
    fin = json.load(open(os.path.join(d, "fin.json")))
    res = {"v": v, "mu": mu, "s": s, "muertes": fin["muertes"],
           "dias": {a: {str(dd): dict(z, despensa=(desp.get(dd) or {}).get(a[0], 0)) for dd, z in sorted(D_.items())} for a, D_ in sorted(R.items()) if a != "bestia"}}
    json.dump(res, open(out, "w"), separators=(",", ":")); return out


if __name__ == "__main__":
    T_ = [(v, mu, s) for v in VARIANTES for mu in MUNDOS for s in SEM] if len(sys.argv) < 4 else [(sys.argv[1], sys.argv[2], int(sys.argv[3]))]
    with Pool(6) as p: r = p.map(una, T_)
    print(len(r), "partidas")

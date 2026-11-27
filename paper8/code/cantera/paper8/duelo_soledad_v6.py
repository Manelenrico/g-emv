"""[P8] Prompt 150 (copia del programa del v5, prompt 134, con las clases, la carpeta y las semillas del v6; la protagonista RG69r+voz, «RG69rvoz» en las carpetas, en el sitio de RG68r) (texto del v5:) [P8] Prompt 134 (copia del programa del v4, prompt 117, con las clases, la carpeta y las semillas del v5): A4 del experimento v4 (sellada desde el principio). Es duelo_soledad_v3.py con la clase RG69r+voz y la carpeta del v4, y SIN volver a jugar:
las filas de duelo, soledad y compañía se apuntaron durante el experimento (filas.jsonl.gz, lanza_experimento_v5), en la misma partida. Se usa solo el modo
«analiza» (python3 duelo_soledad_v6.py); el modo «jugar» de abajo es del v3 y no se usa. La medida, la misma. (Texto del v3:)
[P8] Prompt 113, AÑADIDA DESPUÉS DE SELLAR (sin predicción; pedida por Manel con el experimento en marcha). En la que pierde a su hermana (RG69r+voz),las dos
señales por separado: el duelo (la tristeza por la pérdida: las filas S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO de la foto de ahora) y la soledad (estar
sin ella: la fila S-SOLEDAD; en todos sus turnos despierta y en los de su casa). Y, aparte, S-COMPANIA (la distancia a la hermana viva), que al morir ella deja de
calcularse. El experimento no apunta estas filas: se vuelven a jugar las partidas de RG69r+voz donde muere una hermana (y la otra vive 5 días más), sin el registro
de decisiones (que no cambia nada: prueba_experimento_v3.json), apuntando de la foto de ahora que el lanzador ya calcula (la de las seis) esas filas; cada
partida vuelta a jugar se compara con la del experimento (fin, mundo y criaturas, línea a línea): solo cuentan las idénticas.
Para cada señal y cada caso: cómo está en los 5 días antes de la muerte (la media de los turnos despierta), cuánto sube (la media del día después y la del peor
de los 5 días después, menos la de antes), y, desde su peor día, cuántos días tarda en bajar a la mitad (media del día ≤ antes + 0,5 · (pico − antes)) y en
volver (≤ antes + 0,1 · (pico − antes)); «no vuelve» si no llega antes del día 40 o de su propia muerte. (La mitad se añadió al ver en la prueba, con una
partida, que el duelo baja hacia su suelo, DUELO_SUELO, y no hacia cero: con «volver» solo, el duelo casi nunca vuelve.) Control: las de la misma partida que conservan a
su hermana, en los mismos días.
   python3 duelo_soledad_v6.py jugar [procesos=8]   -> valle_experimento_v3_duelo/<partida>/filas.jsonl.gz (reanudable) y salida/duelo_soledad_v6_puerta.json
   python3 duelo_soledad_v6.py analiza              -> duelo_soledad_v6.md y salida/duelo_soledad_v6.json"""
import gzip, json, os, sys
MODO = sys.argv[1] if len(sys.argv) > 1 else "analiza"
if __name__ == "__main__" and MODO == "jugar" and os.environ.get("VALLE_CAFE") != "1":
    os.environ["VALLE_CAFE"] = "1"; os.execvp("caffeinate", ["caffeinate", "-ims", sys.executable] + sys.argv)
from collections import defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import medidas_v6 as MV
EXP, SEM, MUNDOS, DIA, her, ruta = MV.EXP, MV.SEM, MV.MUNDOS, MV.DIA, MV.her, MV.ruta
FILAS = ("S-DUELO-CUERPO", "S-DUELO-RECURSOS", "S-DUELO-VINCULO", "S-SOLEDAD", "S-COMPANIA")
CARP = EXP                                                                      # (prompt 117) las filas están en la propia partida del experimento v4
TODAS = "A1 A2 B1 B2 C1 C2 D1 D2".split()
NOMBRE = {"duelo": "duelo", "soledad": "soledad", "soledad_casa": "soledad en casa", "compania": "falta de la hermana viva (compañía)"}

def casos_de(fin):
    """las criaturas que pierden a su hermana (muerte el día 5 o después) y viven al menos 5 días más"""
    muere = {m["criatura"]: m["turno"] for m in fin["muertes"]}; out = []
    for b, tm in muere.items():
        a = her(b); dm = tm // DIA
        if dm < 5 or (a in muere and muere[a] // DIA < dm + 5): continue
        out.append((a, dm))
    return out, muere

def candidatas():
    out = []
    for mu in MUNDOS:
        for s in SEM:
            f = os.path.join(ruta("RG69rvoz", mu, s), "fin.json")
            if os.path.exists(f) and casos_de(json.load(open(f)))[0]: out.append((mu, s))
    return out

def jugar(x):
    mu, s = x; import lanza_experimento_v3 as LE; L = LE.L
    n = f"RG69rvoz_{mu}+sabores_s{s}_d40"; d = os.path.join(CARP, n)
    if not os.path.exists(os.path.join(d, "fin.json")) or not os.path.exists(os.path.join(d, "filas.jsonl.gz")):
        REG = {"fh": None}; sa1 = L._sa
        def _sa(c):
            r = sa1(c); c._filas_v3 = (c.obs["turno"], r[1]); return r
        L._sa = _sa; st1 = L.MU.Valle.step
        def _step(self, acc):
            out = st1(self, acc)
            if REG["fh"] is not None:
                t = self.turno - 1; cr = {}
                for a, c in L.CRI.items():
                    q = getattr(c, "_filas_v3", None)
                    if self.cuerpo[a]["muerta"] or q is None or q[0] != t: continue
                    cr[a] = [round(q[1].get(k, 0.0), 5) for k in FILAS]
                REG["fh"].write(json.dumps({"t": t, "c": cr}, separators=(",", ":")) + "\n")
            return out
        L.MU.Valle.step = _step; os.makedirs(d, exist_ok=True); REG["fh"] = gzip.open(os.path.join(d, "filas.jsonl.gz"), "wt", encoding="utf-8")
        try: LE.una(("RG69rvoz", mu + "+sabores", s, 40, CARP), apuntar=False)
        finally: REG["fh"].close(); L._sa = sa1; L.MU.Valle.step = st1
    return dict(LE.iguales(d, os.path.join(EXP, n)), id=n)

def una(x):
    mu, s = x; n = f"RG69rvoz_{mu}+sabores_s{s}_d40"; fin = json.load(open(os.path.join(EXP, n, "fin.json"))); casos, muere = casos_de(fin)
    S = defaultdict(lambda: defaultdict(lambda: [0.0] * 6 + [0, 0]))     # (criatura, día) -> [duelo, soledad, compañía, soledad_casa, -, -, n_desp, n_casa]
    bal = gzip.open(os.path.join(EXP, n, "balance.jsonl.gz"), "rt", encoding="utf-8")
    for lf, lb in zip(gzip.open(os.path.join(CARP, n, "filas.jsonl.gz"), "rt", encoding="utf-8"), bal):
        xf, xb = json.loads(lf), json.loads(lb); assert xf["t"] == xb["t"]; dia = xf["t"] // DIA
        for a, r in xf["c"].items():
            b = xb["c"].get(a)
            if b is None or b[6]: continue                                    # solo despierta
            z = S[a][dia]; z[0] += r[0] + r[1] + r[2]; z[1] += r[3]; z[2] += r[4]; z[6] += 1
            if b[5] == "C": z[3] += r[3]; z[7] += 1
    def media(a, dias, k):
        nn = 7 if k == 3 else 6; v = sum(S[a][d][k] for d in dias if d in S[a]); m = sum(S[a][d][nn] for d in dias if d in S[a]); return v / m if m else None
    def senal(a, dm, k, fin_a):
        antes = media(a, range(dm - 5, dm), k); dsp = [media(a, [d], k) for d in range(dm + 1, dm + 6)]; dsp = [v for v in dsp if v is not None]
        if antes is None or not dsp: return None
        pico = max(dsp); dp = next(d for d in range(dm + 1, dm + 6) if media(a, [d], k) == pico); vuelve = mitad = None
        if pico > antes:
            for d in range(dp + 1, fin_a):
                v = media(a, [d], k)
                if v is None: continue
                if mitad is None and v <= antes + 0.5 * (pico - antes): mitad = d - dm
                if v <= antes + 0.1 * (pico - antes): vuelve = d - dm; break
        return {"antes": antes, "dia1": dsp[0], "pico": pico, "dia_pico": dp - dm, "media5": sum(dsp) / len(dsp), "mitad": mitad, "vuelve": vuelve, "sube": pico > antes}
    out = {"mu": mu, "s": s, "casos": [], "control": []}
    for a, dm in casos:
        fa = min(40, muere[a] // DIA) if a in muere else 40
        out["casos"].append({"a": a, "dia": dm, **{nm: senal(a, dm, k, fa) for nm, k in (("duelo", 0), ("soledad", 1), ("soledad_casa", 3), ("compania", 2))}})
        for c in TODAS:
            hc = her(c)
            if c[0] == a[0] or any(x in muere and muere[x] // DIA <= dm + 5 for x in (c, hc)): continue
            fc = min(40, muere[c] // DIA) if c in muere else 40
            out["control"].append({"a": c, "dia": dm, **{nm: senal(c, dm, k, fc) for nm, k in (("duelo", 0), ("soledad", 1), ("soledad_casa", 3), ("compania", 2))}})
    return out


if __name__ == "__main__":
    if MODO == "jugar":
        npro = int(sys.argv[2]) if len(sys.argv) > 2 else 8; C = candidatas(); os.makedirs(CARP, exist_ok=True); print(len(C), "partidas", flush=True); R = []
        with Pool(npro) as p:
            for r in p.imap_unordered(jugar, C): R.append(r); print(json.dumps(r, ensure_ascii=False), flush=True)
        json.dump({"identicas": sum(r["identica"] for r in R), "de": len(R), "partidas": R}, open(os.path.join(AQUI, "salida", "duelo_soledad_v6_puerta.json"), "w"), ensure_ascii=False, indent=1)
    else:
        X = candidatas()                                                        # (prompt 117) todas las partidas de RG69r+voz con una hermana muerta: las filas se apuntaron jugando
        pu = {"de": len(X), "identicas": len(X)}
        with Pool(8) as p: R = p.map(una, X)
        json.dump(R, open(os.path.join(AQUI, "salida", "duelo_soledad_v6.json"), "w"), ensure_ascii=False)
        m = lambda X: sum(X) / len(X) if X else float("nan"); med = lambda X: sorted(X)[len(X) // 2] if X else None
        w = ["*Medida sin predicción del v6 (A4, en RG69r+voz), de las filas apuntadas en el experimento (filas.jsonl.gz).*\n", f"Partidas de RG69r+voz con una hermana muerta (el día 5 o después, y la otra viva 5 días más): {pu['de']}.\n",
             "Duelo = S-DUELO-CUERPO + S-DUELO-RECURSOS + S-DUELO-VINCULO; soledad = S-SOLEDAD (todos sus turnos despierta; «en casa», los de su casa); compañía = S-COMPANIA (lo lejos que está la hermana viva; al morir ella deja de calcularse). Medias por turno despierta. «Vuelve»: el primer día cuya media queda a una décima o menos de la subida.\n",
             "Desde su peor día de los 5 después: «a la mitad», el primer día cuya media queda a la mitad de la subida o menos; «vuelve», a una décima o menos (el duelo baja hacia un suelo, DUELO_SUELO, no hacia cero). Días contados desde la muerte.\n",
             "| mundo | grupo | señal | casos | antes | día después | peor de los 5 días | subida (pico − antes) | sube en | peor día: mediana | a la mitad: mediana de días (llegan / suben) | vuelve: mediana de días (vuelven / suben) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for mu in list(MUNDOS) + ["todos"]:
            for g in ("casos", "control"):
                Z = [c for r in R if mu in ("todos", r["mu"]) for c in r[g]]
                if not Z: continue
                for sn in ("duelo", "soledad", "soledad_casa", "compania"):
                    Y = [c[sn] for c in Z if c[sn]]
                    if not Y: continue
                    su = [y for y in Y if y["sube"]]; vu = [y["vuelve"] for y in su if y["vuelve"] is not None]; mi = [y["mitad"] for y in su if y["mitad"] is not None]
                    w.append(f"| {mu} | {'pierde a la hermana' if g == 'casos' else 'la conserva'} | {NOMBRE[sn]} | {len(Y)} | {m([y['antes'] for y in Y]):.3f} | {m([y['dia1'] for y in Y]):.3f} | {m([y['pico'] for y in Y]):.3f} | "
                             f"{m([y['pico'] - y['antes'] for y in Y]):.3f} | {len(su)} | {med([y['dia_pico'] for y in su])} | {med(mi)} ({len(mi)} / {len(su)}) | {med(vu)} ({len(vu)} / {len(su)}) |")
        w = [l.replace("None", "—") for l in w]; open(os.path.join(AQUI, "duelo_soledad_v6.md"), "w").write("\n".join(w) + "\n"); print("\n".join(w))

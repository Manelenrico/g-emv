"""[P6-21 · 3] EL CHOQUE: lo que cada pieza da por seguro contra lo que el juego quema.
Lee las filas por tic que dejo `mide_anillo_P6_21.py` (P621_SCRATCH) para A4, A5h y A6,
desde el aviso de la fase 5. Ninguna regla se escribe antes de medirla: la del juego es la
de §1 (`P6_21_anillo.json`) y las nuestras son las citadas en el informe.

  juego (medida en §1): quema si d > radio observado (entero, `zona.radius`), y quema TODO
        cuando el radio observado es 0; d = distancia euclidea de la casilla (x, y) a (24, 24).
  cuerpo congelado (mundo.eventos_arde / F-ANTICIPACION / foto prevista / proyeccion):
        arde ahora si d > radio interpolado de `mundo.anillo_en(t)` (con decimales);
        a salvo = no arde.
  oraculo (`oraculo_P6_14.Oraculo.a_salvo`): a salvo si d <= radio interpolado(t) y
        d <= r1 de la fase activa en t.
  puerta6 / proyeccion (`proyeccion._proyecta` §4): igual que el cuerpo, tic a tic.
Por tic y pieza: (seguro para la pieza, quema el juego) y (arde para la pieza, no quema el
juego). Ademas: tics quieto (misma casilla que el tic anterior) en casilla que el cuerpo
daba por segura mientras el juego la quemaba, con los golpes del anillo recibidos asi; y
las muertes por anillo de A4 (P6_18_campo.json, definicion de P6-16): en que casilla, con que
radio, y si el cuerpo la creia segura.
"""
import collections, glob, json, math, os
AQUI = os.path.dirname(os.path.abspath(__file__))
SCR = os.environ.get("P621_SCRATCH") or os.path.join(AQUI, "_P6_21_tmp")
C = (24, 24)
CAMPO = json.load(open(os.path.join(AQUI, "P6_18_campo.json")))
MUERTES_A4 = {(v["semilla"], v["slot"]): v for v in CAMPO["A4"]["vidas"] if v["causa"] == "anillo"}


def juego_quema(d, R):
    return R is not None and (R == 0 or d > R + 1e-9)


def cuerpo_arde(d, cal):
    return d > cal + 1e-9


def oraculo_salvo(d, cal, r1):
    return d <= cal + 1e-9 and d <= r1 + 1e-9


K = collections.defaultdict(collections.Counter); M = []
for f in sorted(glob.glob(os.path.join(SCR, "filas_*.json"))):
    d = json.load(open(f)); brazo = d["brazo"]
    if brazo not in ("A4", "A5h", "A6"):
        continue
    zs = d["zs"]; warn5 = zs[4][0]; F = d["filas"]; prev = None
    for r in F:
        t = r["t"]
        if t < warn5:
            prev = r; continue
        p = tuple(r["pos"]); dd = math.dist(p, C); R = r["rad"]["obs(t)"]; cal = r["rad"]["cal(t)"]; r1 = r["rad"]["r1 fase"]
        q = juego_quema(dd, R); ca = cuerpo_arde(dd, cal); osv = oraculo_salvo(dd, cal, r1)
        k = K[brazo]; k["tics"] += 1; k["juego quema"] += q; k["golpes"] += (r["zh"] > 0)
        k["cuerpo: seguro y el juego quema"] += (not ca and q); k["cuerpo: arde y el juego no quema"] += (ca and not q)
        k["oraculo: seguro y el juego quema"] += (osv and q); k["oraculo: arde y el juego no quema"] += ((not osv) and not q)
        k["cuerpo: seguro y el juego quema · radio 0"] += (not ca and q and R == 0)
        k["cuerpo: seguro y el juego quema · golpes recibidos"] += (r["zh"] > 0 and not ca)
        k["cuerpo: arde y el juego no quema · en encogimiento"] += (ca and not q and abs(R - cal) > 1e-9)
        quieto = prev is not None and tuple(prev["pos"]) == p
        if quieto:
            k["quieto"] += 1
            if not ca and q:
                k["quieto en casilla que creia segura mientras quemaba"] += 1; k["quieto ... golpes recibidos"] += (r["zh"] > 0)
                k["quieto ... radio 0"] += (R == 0)
                k["quieto ... elegido " + (r["el"] if r["el"] in ("noop", "_FM_quedarse") else ("otro"))] += 1
        prev = r
    # muertes por anillo de A4
    if brazo == "A4" and (d["sem"], d["slot"]) in MUERTES_A4:
        r = F[-1]; p = tuple(r["pos"]); dd = math.dist(p, C); R = r["rad"]["obs(t)"]; cal = r["rad"]["cal(t)"]
        # ultimo tic quieto: cuantos tics llevaba en la casilla
        n = 0
        for x in reversed(F):
            if tuple(x["pos"]) == p:
                n += 1
            else:
                break
        M.append({"sem": d["sem"], "slot": d["slot"], "t": r["t"], "pos": p, "d": round(dd, 2), "R": R, "cal": round(cal, 2), "r1": r["rad"]["r1 fase"], "fase": r["fase"], "juego quema": juego_quema(dd, R), "cuerpo cree segura": not cuerpo_arde(dd, cal),
                  "oraculo a salvo": oraculo_salvo(dd, cal, r["rad"]["r1 fase"]), "tics en la casilla": n, "hp": r["hp"], "elegido": r["el"]})
    print(" ", os.path.basename(f), flush=True)

R = {"nota": "P6-21 §3. INSTRUMENTO DE MEDIDA. Tics desde el aviso 5 de A4, A5h, A6; reglas citadas en el informe.", "por_brazo": {b: dict(k) for b, k in K.items()},
     "muertes_anillo_A4": {"n": len(M), "cuerpo_creia_segura": sum(1 for m in M if m["cuerpo cree segura"]), "oraculo_a_salvo": sum(1 for m in M if m["oraculo a salvo"]), "radio_0": sum(1 for m in M if m["R"] == 0),
                           "en_el_centro": sum(1 for m in M if m["pos"] == C), "por_fase": dict(collections.Counter(m["fase"] for m in M)), "tics_en_la_casilla_mediana": (sorted(m["tics en la casilla"] for m in M)[len(M) // 2] if M else None), "lista": M}}
json.dump(R, open(os.path.join(AQUI, "P6_21_choque.json"), "w"), ensure_ascii=False, indent=1, default=str)
for b, k in K.items():
    print(b, dict(k))
print("muertes A4:", {kk: v for kk, v in R["muertes_anillo_A4"].items() if kk != "lista"})
for m in M:
    print("  ", m)
print("-> P6_21_choque.json")

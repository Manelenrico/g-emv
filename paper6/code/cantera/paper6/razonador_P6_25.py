"""[P6-25 · 2, 4, 5] EL RAZONADOR DE LENGUAJE, por API, con el gasto contado llamada a llamada.
Reutiliza la via del consejero del cinco (`consejero_forma.py`: clave, cliente, llamada, contador,
precios, manual M2 cacheado) y su instruccion (`instruccion_forma.md` + `tabla_ensenada.md`), MAS
las palabras del seis (`instruccion_P6_25.md`: el anillo, quedarse, la zona segura, juntos).

REGLAS DE CUSTODIA (las del cinco): la clave se lee SOLO de `cantera/paper5/.env`, nunca se exporta
ni se imprime; todas las respuestas crudas se guardan; el gasto se mide con el `usage` de la API y el
tope PARA la tanda. El razonador corre siempre fuera del hilo principal: aqui no hay hilo principal,
es banco; en el campo iria por el proceso aparte de P6-23.

Modos (cada uno anade a `P6_25_gasto.json` y escribe sus crudas y sus planes traducidos):
  --humo                   una escena, los dos modelos: comprobar el cable y el precio.
  --primera                punto 2: las 200 escenas x 2 modelos, el primer plan.
  --bucle K                punto 4 (Manel): a los planes RECHAZADOS de la vuelta K-1 (K = 2, 3), el motivo en
                           palabras (las filas que mas pesaron en contra, del juez) y «propon otro plan».
                           Solo las N_BUCLE primeras escenas de la muestra (declarado, por el tope).
  --pareja                 punto 5: en las escenas de pareja, cada hermano con su vista y el ultimo mensaje
                           del otro; plan conjunto, la zona donde se encuentran y el mensaje (<= 120).
  --modelos haiku,sonnet   (por defecto los dos)

    python3 razonador_P6_25.py --humo | --primera | --bucle 2 | --bucle 3 | --pareja
"""
from __future__ import annotations
import collections, hashlib, json, os, sys, threading, time
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball")):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.dont_write_bytecode = True
import consejero_forma as CF                                    # noqa: E402
import traductor_forma as TF                                    # noqa: E402

TOPE_USD = 10.0            # [Manel] el tope del encargo P6-25
TOPE_PARADA = 9.5          # parada propia
N_BUCLE = 80               # escenas que entran en el bucle (las primeras de la muestra, ya al azar); el humo midio 0,004 / 0,015 USD por llamada en la primera
N_PARES = 40               # pares que entran en la pareja (todos los de la muestra); cabe en el tope con lo medido en la primera
HILOS = 3
MODELOS = ("haiku", "sonnet")
GASTO_F = os.path.join(AQUI, "P6_25_gasto.json")
VERSION = "razonador_P6_25 (P6-25): consejero del cinco (instruccion + tabla ensenada) + palabras del seis; primera / bucle / pareja"
COLA = "Responde ahora con el JSON de formas para esta escena, siguiendo el esquema exacto de la instruccion."
COLA_PAREJA = ("Tu hermano esta recibiendo ahora mismo su propia escena y la misma peticion. Propon el plan CONJUNTO: adonde vais los dos "
               "(la zona segura donde os encontrais) y tu propia forma para llegar y quedarte. Responde SOLO con un objeto JSON con esta forma exacta: "
               '{"formas": [...como en el esquema de la instruccion...], "callar": true | false, "zona": [x, y], '
               '"mensaje": "<lo que le dirias a tu hermano por el canal de equipo: ASCII, 120 caracteres como maximo>"}')


def sistema():
    return CF.sistema_formas() + "\n\n---\n\n" + open(os.path.join(RAIZ, "cantera", "paper5", "tabla_ensenada.md"), encoding="utf-8").read().strip() + "\n\n---\n\n" + open(os.path.join(AQUI, "instruccion_P6_25.md"), encoding="utf-8").read().strip()


def bloques(texto_escena, cola, man):
    """[como consejero_forma.mensaje] dos bloques: el manual M2 cacheado y la escena con la cola."""
    return [{"type": "text", "text": f"{CF.CABECERA}\n\n{man}\n\n---\n\n", "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": texto_escena + "\n\n" + cola}]


def saca_json(texto):
    try:
        obj, _err = TF.saca_json(texto)
        return obj
    except Exception:
        return None


def traduce(texto, escena, filas):
    cnt = collections.Counter()
    try:
        formas, inf = TF.traduce(texto or "", escena, filas, cnt)
    except Exception as ex:
        return [], {"error": repr(ex)[:200]}, dict(cnt)
    return formas, inf, dict(cnt)


class Gasto:
    """El contador del cinco, persistido entre modos."""

    def __init__(self):
        self.c = CF.Contador(tope=TOPE_PARADA); self.lock = threading.Lock()
        if os.path.exists(GASTO_F):
            g = json.load(open(GASTO_F)); self.c.total = float(g.get("total_usd") or 0.0)
            self.previo = g
        else:
            self.previo = {}

    def suma(self, etiq, modelo, u):
        with self.lock:
            return self.c.suma(etiq, modelo, u)

    def pasado(self):
        return self.c.total >= TOPE_PARADA

    def guarda(self):
        r = self.c.resumen(); r["tope_usd"] = TOPE_USD; r["parada_usd"] = TOPE_PARADA
        r["modos"] = dict(self.previo.get("modos") or {}); r["modos"].update({k: v for k, v in r["por_brazo"].items()})
        json.dump(r, open(GASTO_F, "w"), ensure_ascii=False, indent=1)
        return r


def llama_todas(peticiones, etiqueta, gasto, crudas_f):
    """peticiones: [{id, modelo, texto, cola, meta}] -> respuestas en orden; crudas a jsonl."""
    cli = CF.cliente(); man = CF.manual(); sis = sistema(); out = [None] * len(peticiones); lock = threading.Lock(); parada = [False]
    f_crudas = open(crudas_f, "a", encoding="utf-8")

    def una(i):
        p = peticiones[i]
        if parada[0] or gasto.pasado():
            out[i] = {"id": p["id"], "modelo": p["modelo"], "error": "PARADA por gasto", "texto": None, "ms": None, "usd": None}; return
        texto, u, ms, err = CF.llama(cli, p["modelo"], sis, bloques(p["texto"], p["cola"], man), "formas")
        usd = gasto.suma(etiqueta + "/" + p["modelo"], p["modelo"], u) if u else 0.0
        r = {"id": p["id"], "modelo": p["modelo"], "modelo_api": CF.MODELOS[p["modelo"]], "etiqueta": etiqueta, "ms": ms, "usd": round(usd, 6), "usage": u, "error": err, "texto": texto, "meta": p.get("meta")}
        with lock:
            f_crudas.write(json.dumps(r, ensure_ascii=False) + "\n"); f_crudas.flush()
            out[i] = r
            if gasto.pasado():
                parada[0] = True
    # HILOS a la vez, como la tanda del cinco
    sem = threading.Semaphore(HILOS); hs = []

    def envuelta(i):
        with sem:
            una(i)
    for i in range(len(peticiones)):
        h = threading.Thread(target=envuelta, args=(i,)); h.start(); hs.append(h)
    for h in hs:
        h.join()
    f_crudas.close()
    return out


def escenas():
    return json.load(open(os.path.join(AQUI, "P6_25_escenas.json")))


def id_de(e):
    return f"{e['carp']}_{e['slot']}_{e['tick']}"


def plan_de(r, e, filas):
    """De la respuesta al plan: el JSON, las formas traducidas (la primera es el plan que se juzga), callar, zona, mensaje."""
    j = saca_json(r.get("texto") or "") if r.get("texto") else None
    formas, inf, cnt = traduce(r.get("texto") or "", e["escena_traductor"], filas) if r.get("texto") else ([], {}, {})
    tramos = [TF.solo_tramos(f) for f in formas]
    return {"id": r["id"], "modelo": r["modelo"], "ms": r.get("ms"), "usd": r.get("usd"), "error": r.get("error"), "parsea": j is not None,
            "callar": (bool(j.get("callar")) if isinstance(j, dict) else None), "n_formas_dichas": (len(j.get("formas") or []) if isinstance(j, dict) else 0),
            "n_formas": len(formas), "intraducible": (j is not None and bool(j.get("formas")) and not formas), "fallos_traductor": inf.get("fallos") if isinstance(inf, dict) else None,
            "tramos": (tramos[0] if tramos else None), "todas": tramos, "mitades": ([dict((t.get("_mitad") or {}), por=t.get("_por"), porque=t.get("_porque")) for t in formas[0]["tramos"]] if formas else None),
            "final": (formas[0].get("final") if formas else None), "zona": (j.get("zona") if isinstance(j, dict) else None), "mensaje": (j.get("mensaje") if isinstance(j, dict) else None),
            "tick": e["tick"], "snap": e["snap"]["0"], "carp": e["carp"], "slot": e["slot"]}


def modo_humo(modelos):
    E = escenas(); e = E["escenas"][0]; filas = E["filas"][e["carp"]]
    g = Gasto(); pet = [{"id": id_de(e), "modelo": m, "texto": e["texto"], "cola": COLA, "meta": {"modo": "humo"}} for m in modelos]
    print(f"HUMO · escena {pet[0]['id']} · sistema {len(sistema())} caracteres (md5 {hashlib.md5(sistema().encode()).hexdigest()}) · escena {len(e['texto'])} caracteres")
    rs = llama_todas(pet, "humo", g, os.path.join(AQUI, "P6_25_crudas_humo.jsonl"))
    for r in rs:
        p = plan_de(r, e, filas)
        print(f"  {r['modelo']}: {r['ms']} ms · {r['usd']} USD · usage {json.dumps(r['usage'])} · error {r['error']}")
        print(f"     parsea {p['parsea']} · formas {p['n_formas']} de {p['n_formas_dichas']} · callar {p['callar']} · plan {p['tramos']} · mitades {p['mitades']}")
        print("     texto:", (r.get("texto") or "")[:600].replace("\n", " "))
    print("gasto:", json.dumps(g.guarda()["total_usd"]))


def modo_primera(modelos):
    E = escenas(); g = Gasto()
    esc = [e for e in E["escenas"] if e["propia"]]
    pet = [{"id": id_de(e), "modelo": m, "texto": e["texto"], "cola": COLA, "meta": {"modo": "primera"}} for e in esc for m in modelos]
    print(f"PRIMERA · {len(esc)} escenas x {len(modelos)} modelos = {len(pet)} llamadas · gastado antes {g.c.total:.4f}")
    rs = llama_todas(pet, "primera", g, os.path.join(AQUI, "P6_25_crudas_primera.jsonl"))
    por = {id_de(e): e for e in esc}
    planes = [plan_de(r, por[r["id"]], E["filas"][por[r["id"]]["carp"]]) for r in rs]
    json.dump({"nota": "P6-25 · 2. El primer plan del razonador en cada escena, traducido (la primera forma es el plan que se juzga).", "version": VERSION, "planes": planes}, open(os.path.join(AQUI, "P6_25_planes_primera.json"), "w"), ensure_ascii=False, indent=1)
    r = g.guarda(); print(f"-> P6_25_planes_primera.json · {sum(1 for p in planes if p['tramos'])} planes traducidos de {len(planes)} · gasto total {r['total_usd']}")


def motivo_en_palabras(j):
    """El motivo del rechazo, para el bucle: el veredicto y las filas que mas pesaron en contra (del juez)."""
    ver = j.get("veredicto"); contra = [c for c in (j.get("contra") or []) if c[1] > 0][:4]
    L = []
    if ver == "area":
        L.append("el cuerpo imagino que, en conjunto, con tu plan estaria PEOR que haciendo lo suyo (compara la curva de necesidad de tu plan con la del cuerpo decidiendo paso a paso).")
    elif ver == "vida":
        L.append("el cuerpo imagino que con tu plan su vida quedaria por debajo del minimo que acepta.")
    else:
        L.append(f"veredicto: {ver}.")
    if contra:
        L.append("Los renglones que mas pesaron EN CONTRA de tu plan fueron: " + "; ".join(f"`{c[0]}` (peso {c[1]:+.3f}; en tu plan {c[2]:.2f}, en lo suyo {c[3]:.2f})" for c in contra) + ".")
    if j.get("dentro_futuro") is False:
        L.append("Ademas, el destino que diste queda FUERA del circulo al que va esta fase.")
    return " ".join(L)


def modo_bucle(K, modelos):
    E = escenas(); g = Gasto()
    prev = "primera" if K == 2 else f"bucle{K - 1}"
    J = json.load(open(os.path.join(AQUI, f"P6_25_juicios_{prev}.json")))["juicios"]
    P = {(p["id"], p["modelo"]): p for p in json.load(open(os.path.join(AQUI, f"P6_25_planes_{prev}.json")))["planes"]}
    esc = [e for e in E["escenas"] if e["propia"]][:N_BUCLE]; por = {id_de(e): e for e in esc}
    pet = []
    for j in J:
        if j["id"] not in por or j["modelo"] not in modelos or j.get("veredicto") == "ok" or j.get("veredicto") is None:
            continue
        p = P.get((j["id"], j["modelo"])); e = por[j["id"]]
        if not p or not p.get("tramos"):
            continue
        plan_txt = json.dumps({"tramos": p["tramos"], "final": p.get("final")}, ensure_ascii=False)
        cola = (f"Le propusiste antes este plan: {plan_txt}. EL CUERPO LO RECHAZO: {motivo_en_palabras(j)} Propon OTRO plan distinto para esta misma escena, "
                "teniendo en cuenta el motivo. " + COLA)
        pet.append({"id": j["id"], "modelo": j["modelo"], "texto": e["texto"], "cola": cola, "meta": {"modo": f"bucle{K}", "previo": p["tramos"], "veredicto_previo": j.get("veredicto")}})
    print(f"BUCLE {K} · {len(pet)} llamadas (rechazados de {prev} en las {len(esc)} primeras escenas) · gastado antes {g.c.total:.4f}")
    rs = llama_todas(pet, f"bucle{K}", g, os.path.join(AQUI, f"P6_25_crudas_bucle{K}.jsonl"))
    planes = [dict(plan_de(r, por[r["id"]], E["filas"][por[r["id"]]["carp"]]), previo=r["meta"]["previo"], veredicto_previo=r["meta"]["veredicto_previo"]) for r in rs]
    json.dump({"nota": f"P6-25 · 4. Vuelta {K} del bucle de Manel: otro plan tras el motivo del rechazo.", "version": VERSION, "planes": planes}, open(os.path.join(AQUI, f"P6_25_planes_bucle{K}.json"), "w"), ensure_ascii=False, indent=1)
    r = g.guarda(); print(f"-> P6_25_planes_bucle{K}.json · {sum(1 for p in planes if p['tramos'])} planes traducidos de {len(planes)} · gasto total {r['total_usd']}")


def modo_pareja(modelos):
    E = escenas(); g = Gasto()
    por = {(e["carp"], e["slot"], e["tick"]): e for e in E["escenas"]}
    pares = []
    for e in E["escenas"]:
        if e["propia"] and e["pareja"]:
            h = por.get((e["carp"], 21 - e["slot"], e["tick"]))
            if h:
                pares.append((e, h))
    pares = pares[:N_PARES]
    pet = []
    for e, h in pares:
        for m in modelos:
            for yo, otro in ((e, h), (h, e)):
                pet.append({"id": id_de(yo), "modelo": m, "texto": yo["texto"], "cola": COLA_PAREJA, "meta": {"modo": "pareja", "par": id_de(e), "hermano": id_de(otro)}})
    print(f"PAREJA · {len(pares)} pares x 2 hermanos x {len(modelos)} modelos = {len(pet)} llamadas · gastado antes {g.c.total:.4f}")
    rs = llama_todas(pet, "pareja", g, os.path.join(AQUI, "P6_25_crudas_pareja.jsonl"))
    porid = {id_de(x): x for par in pares for x in par}
    planes = [dict(plan_de(r, porid[r["id"]], E["filas"][porid[r["id"]]["carp"]]), par=r["meta"]["par"], hermano=r["meta"]["hermano"]) for r in rs]
    json.dump({"nota": "P6-25 · 5. La pareja: cada hermano con su vista y el ultimo mensaje del otro; plan conjunto, zona y mensaje.", "version": VERSION, "planes": planes}, open(os.path.join(AQUI, "P6_25_planes_pareja.json"), "w"), ensure_ascii=False, indent=1)
    r = g.guarda(); print(f"-> P6_25_planes_pareja.json · {sum(1 for p in planes if p['tramos'])} planes traducidos de {len(planes)} · gasto total {r['total_usd']}")


if __name__ == "__main__":
    a = sys.argv
    modelos = tuple(a[a.index("--modelos") + 1].split(",")) if "--modelos" in a else MODELOS
    if "--recuenta" in a:        # el gasto, reconstruido desde TODAS las crudas (usage de la API), por si un modo se cayo antes de guardar
        import glob as _g
        c = CF.Contador(tope=TOPE_PARADA)
        for f in sorted(_g.glob(os.path.join(AQUI, "P6_25_crudas_*.jsonl"))):
            for l in open(f, encoding="utf-8"):
                r = json.loads(l)
                if r.get("usage"):
                    c.suma(r["etiqueta"] + "/" + r["modelo"], r["modelo"], r["usage"])
        r = c.resumen(); r["tope_usd"] = TOPE_USD; r["parada_usd"] = TOPE_PARADA; r["modos"] = dict(r["por_brazo"])
        json.dump(r, open(GASTO_F, "w"), ensure_ascii=False, indent=1); print(json.dumps(r, ensure_ascii=False))
    elif "--humo" in a:
        modo_humo(modelos)
    elif "--primera" in a:
        modo_primera(modelos)
    elif "--bucle" in a:
        modo_bucle(int(a[a.index("--bucle") + 1]), modelos)
    elif "--pareja" in a:
        modo_pareja(modelos)
    else:
        print(__doc__)

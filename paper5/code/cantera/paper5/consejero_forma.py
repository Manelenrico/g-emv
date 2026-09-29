"""[P5-5B] El consejero real, por API, con el gasto contado llamada a llamada.

REGLAS DE CUSTODIA:
  · la clave se lee SOLO de `cantera/paper5/.env`, nunca se exporta ni se
    imprime, ni entera ni en trozos;
  · todas las respuestas crudas se guardan;
  · el gasto se mide con el `usage` que devuelve la API, no con estimaciones, y
    el tope PARA la tanda.

El mensaje de usuario se arma como en el campo (`cortex_t5.py:916-932`): dos
bloques, el primero con el manual M2 y `cache_control: ephemeral`, el segundo
con la escena y el esquema. Lo unico que cambia entre brazos es el sistema y el
esquema.
"""
from __future__ import annotations
import collections, hashlib, json, os, sys, time

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

TOPE_USD = 15.0
# [declarado] TEMPERATURA: no se pasa. El campo tampoco la pasaba
# (`cortex_t5.py:930-932` manda solo anthropic_version/max_tokens/system/
# messages), y ademas el SDK anthropic 1.5.0 ya NO expone `temperature`. Asi
# que las dos corridas usan la de por defecto del modelo, que es 1.0.
TEMPERATURA = "por defecto del modelo (no se pasa; el SDK 1.5.0 no la expone)"
MAX_TOKENS = {"formas": 1500, "casillas": 512}   # el campo usaba 512
MODELOS = {"haiku": "claude-haiku-4-5-20251001",
           "sonnet": "claude-sonnet-4-5-20250929"}
# dolares por millon de tokens
PRECIO = {"haiku":  {"in": 1.00, "out": 5.00, "cw": 1.25, "cr": 0.10},
          "sonnet": {"in": 3.00, "out": 15.00, "cw": 3.75, "cr": 0.30}}

CABECERA = "Este es el reglamento del sitio donde esta:"
SISTEMA_CASILLAS = (
    "Eres el companero de alguien que esta en una arena y te cuenta "
    "lo que ve. Propon entre una y tres acciones que podria hacer "
    "ahora, cada una con un motivo de una frase. Puedes proponer "
    "algo que no este en su lista si crees que le conviene. "
    "Responde en espanol.")
ESQUEMA_CASILLAS = ('Responde SOLO con un objeto JSON, sin nada mas, con esta '
                    'forma exacta: {"propuestas": [{"accion": "<texto>", '
                    '"motivo": "<una frase>"}]}, entre una y tres propuestas.')


def clave():
    """La clave, del .env. No se imprime ni se devuelve a ningun log."""
    p = os.path.join(AQUI, ".env")
    if not os.path.exists(p):
        raise SystemExit("no hay cantera/paper5/.env")
    for linea in open(p, encoding="utf-8"):
        if linea.strip().startswith("ANTHROPIC_API_KEY="):
            k = linea.split("=", 1)[1].strip().strip('"').strip("'")
            if k:
                return k
    raise SystemExit("el .env no tiene ANTHROPIC_API_KEY")


def manual():
    p = os.path.join(RAIZ, "paintball", "alma", "manual_M2.md")
    return open(p, encoding="utf-8").read().strip()


def sistema_formas():
    p = os.path.join(AQUI, "instruccion_forma.md")
    return open(p, encoding="utf-8").read().strip()


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def mensaje(escena, brazo, man):
    """Los dos bloques del mensaje de usuario, como en el campo."""
    if brazo == "casillas":
        cola = ESQUEMA_CASILLAS
    else:
        cola = ("Responde ahora con el JSON de formas para esta escena, "
                "siguiendo el esquema exacto de la instruccion.")
    cuerpo = "\n\n".join([escena["relato"], escena["bloque_cuerpo"],
                          escena["bloque_hermano"], cola])
    return [{"type": "text",
             "text": f"{CABECERA}\n\n{man}\n\n---\n\n",
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": cuerpo}]


class Contador:
    """El gasto, medido con el `usage` de cada respuesta."""

    def __init__(self, tope=TOPE_USD):
        self.tope = tope
        self.total = 0.0
        self.por = collections.defaultdict(lambda: collections.Counter())
        self.n = collections.Counter()

    def suma(self, etiqueta, modelo, u):
        p = PRECIO[modelo]
        d = (u.get("input_tokens", 0) * p["in"]
             + u.get("output_tokens", 0) * p["out"]
             + u.get("cache_creation_input_tokens", 0) * p["cw"]
             + u.get("cache_read_input_tokens", 0) * p["cr"]) / 1e6
        self.total += d
        self.n[etiqueta] += 1
        c = self.por[etiqueta]
        for k in ("input_tokens", "output_tokens",
                  "cache_creation_input_tokens", "cache_read_input_tokens"):
            c[k] += u.get(k, 0)
        c["usd_millonesimas"] += int(round(d * 1e6))
        return d

    def pasado(self):
        return self.total >= self.tope

    def resumen(self):
        out = {"total_usd": round(self.total, 6), "tope_usd": self.tope,
               "llamadas": dict(self.n), "por_brazo": {}}
        for k, c in self.por.items():
            out["por_brazo"][k] = {
                "llamadas": self.n[k],
                "entrada_fresca": c["input_tokens"],
                "salida": c["output_tokens"],
                "cache_escritura": c["cache_creation_input_tokens"],
                "cache_lectura": c["cache_read_input_tokens"],
                "usd": round(c["usd_millonesimas"] / 1e6, 6),
                "usd_por_llamada": round(c["usd_millonesimas"] / 1e6
                                         / max(1, self.n[k]), 6)}
        return out


def llama(cli, modelo, sistema, bloques, brazo, reintentos=3):
    """(texto, usage, ms, error). Reintenta con espera si la API se queja."""
    for intento in range(reintentos):
        t0 = time.perf_counter()
        try:
            r = cli.messages.create(
                model=MODELOS[modelo],
                max_tokens=MAX_TOKENS[brazo],
                system=[{"type": "text", "text": sistema}],
                messages=[{"role": "user", "content": bloques}])
            ms = round((time.perf_counter() - t0) * 1000.0, 1)
            texto = "".join(b.text for b in r.content
                            if getattr(b, "type", "") == "text")
            u = r.usage.model_dump() if hasattr(r.usage, "model_dump") else dict(r.usage)
            return texto, u, ms, None
        except Exception as ex:
            ms = round((time.perf_counter() - t0) * 1000.0, 1)
            if intento == reintentos - 1:
                return None, {}, ms, f"{type(ex).__name__}: {ex}"
            time.sleep(2.0 * (intento + 1))
    return None, {}, 0.0, "sin intentos"


def cliente():
    import anthropic
    return anthropic.Anthropic(api_key=clave())


# ── humo ──────────────────────────────────────────────────────────────────
def humo():
    """Tres llamadas de humo, con su respuesta cruda guardada y pegada."""
    escenas = json.load(open(os.path.join(AQUI, "P55B_escenas.json")))
    man = manual()
    sis_f = sistema_formas()
    print(f"manual M2: {len(man)} caracteres, md5 {md5(man)}")
    print(f"instruccion de FORMAS: {len(sis_f)} caracteres, md5 {md5(sis_f)}")
    print(f"instruccion de CASILLAS: md5 {md5(SISTEMA_CASILLAS)} "
          f"(el campo: f6882517309310ca5aa7e9e18177707f)")
    print(f"esquema de CASILLAS: md5 {md5(ESQUEMA_CASILLAS)} "
          f"(el campo: ac9c650a3c912d8346d82db2972b5059)")
    print(f"temperatura {TEMPERATURA} · max_tokens {MAX_TOKENS}")
    cli = cliente()
    cont = Contador()
    pruebas = [("formas", "haiku", escenas[0]),
               ("formas", "sonnet", escenas[0]),
               ("casillas", "haiku", escenas[1])]
    crudas = []
    for brazo, modelo, esc in pruebas:
        sis = sis_f if brazo == "formas" else SISTEMA_CASILLAS
        bl = mensaje(esc, brazo, man)
        texto, u, ms, err = llama(cli, modelo, sis, bl, brazo)
        d = cont.suma(f"{brazo}/{modelo}", modelo, u) if u else 0.0
        print("=" * 70)
        print(f"HUMO · brazo {brazo} · modelo {MODELOS[modelo]} · "
              f"escena {esc['id']} · {ms} ms · {d:.6f} $")
        if err:
            print("ERROR:", err)
        else:
            print(f"usage: {json.dumps(u, ensure_ascii=False)}")
            print("--- respuesta cruda ---")
            print(texto)
        crudas.append({"brazo": brazo, "modelo": MODELOS[modelo],
                       "escena": esc["id"], "ms": ms, "usage": u,
                       "usd": round(d, 6), "error": err, "texto": texto})
    json.dump(crudas, open(os.path.join(AQUI, "P55B_humo.json"), "w"),
              ensure_ascii=False, indent=1)
    print("=" * 70)
    print("GASTO DEL HUMO:", json.dumps(cont.resumen(), ensure_ascii=False))




# ── la tanda ──────────────────────────────────────────────────────────────
import threading                                            # noqa: E402

GASTO = os.path.join(AQUI, "P55B_gasto.json")
_CAND = threading.Lock()


def gasto_leido():
    if os.path.exists(GASTO):
        return json.load(open(GASTO))
    return {"total_usd": 0.0, "por": {}}


def gasto_guarda(g):
    json.dump(g, open(GASTO, "w"), ensure_ascii=False, indent=1)


def tanda(brazo, modelo, hilos=3):
    """Las llamadas de un brazo. Reanudable: salta lo ya guardado."""
    escenas = json.load(open(os.path.join(AQUI, "P55B_escenas.json")))
    man, sis_f = manual(), sistema_formas()
    sis = sis_f if brazo == "formas" else SISTEMA_CASILLAS
    etiq = f"{brazo}/{modelo}"
    sal = os.path.join(AQUI, f"P55B_crudas_{brazo}_{modelo}.jsonl")
    hechas = set()
    if os.path.exists(sal):
        for linea in open(sal, encoding="utf-8"):
            try:
                hechas.add(json.loads(linea)["escena"])
            except Exception:
                pass
    quedan = [e for e in escenas if e["id"] not in hechas]
    prog = open(os.path.join(AQUI, "P55B_progreso.log"), "a", buffering=1)

    def avisa(s):
        print(s, flush=True)
        prog.write(s + "\n")

    avisa(f"[TANDA {etiq}] {len(quedan)} por hacer de {len(escenas)} "
          f"(ya hechas {len(hechas)}) · sistema md5 {md5(sis)}")
    if not quedan:
        return
    cli = cliente()
    g = gasto_leido()
    cont = Contador()
    cont.total = g["total_usd"]
    fich = open(sal, "a", encoding="utf-8")
    parar = threading.Event()
    hecho = [0]

    def una(esc):
        if parar.is_set():
            return
        bl = mensaje(esc, brazo, man)
        texto, u, ms, err = llama(cli, modelo, sis, bl, brazo)
        with _CAND:
            d = cont.suma(etiq, modelo, u) if u else 0.0
            hecho[0] += 1
            fich.write(json.dumps({
                "escena": esc["id"], "brazo": brazo, "modelo": MODELOS[modelo],
                "buena": esc["buena"], "ms": ms, "usage": u,
                "usd": round(d, 6), "error": err, "texto": texto},
                ensure_ascii=False) + "\n")
            fich.flush()
            if hecho[0] % 10 == 0 or hecho[0] == len(quedan):
                avisa(f"[TANDA {etiq}] {hecho[0]}/{len(quedan)} · "
                      f"gasto acumulado {cont.total:.4f} $ de {cont.tope}")
            if cont.pasado():
                parar.set()
                avisa(f"[TANDA {etiq}] TOPE DE GASTO ALCANZADO "
                      f"({cont.total:.4f} $). Paro.")

    # una llamada de calentamiento, sola, para que la cache exista
    una(quedan[0])
    resto = quedan[1:]
    hilillos = []
    cola = list(resto)
    idx = [0]

    def obrero():
        while not parar.is_set():
            with _CAND:
                if idx[0] >= len(cola):
                    return
                e = cola[idx[0]]; idx[0] += 1
            una(e)

    for _ in range(max(1, hilos)):
        h = threading.Thread(target=obrero, daemon=True)
        h.start(); hilillos.append(h)
    for h in hilillos:
        h.join()
    fich.close()
    g["total_usd"] = cont.total
    g.setdefault("por", {})[etiq] = cont.resumen()["por_brazo"].get(etiq)
    gasto_guarda(g)
    avisa(f"[TANDA {etiq}] FIN · {hecho[0]} llamadas · "
          f"gasto acumulado total {cont.total:.4f} $")


if __name__ == "__main__":
    a = sys.argv[1:] or [""]
    if a[0] == "humo":
        humo()
    elif a[0] == "tanda" and len(a) >= 3:
        tanda(a[1], a[2], int(a[3]) if len(a) > 3 else 3)
    else:
        print("uso: consejero_forma.py humo | tanda <formas|casillas> "
              "<haiku|sonnet> [hilos]")

"""[P7-21] DONDE MUEREN LAS QUE RECUERDAN, Y EL BOTIQUIN BAJO GOLPES. Lectura de los 640 diarios de los dos campos (P7-10 y P7-14b), posterior a los sellos.
Coste cero. La lectura del diario es la de P7-16 (`analiza_P7_16.lee`) y las peleas las de P7-20 (`analiza_P7_20.peleas`), importadas, no copiadas;
aqui se leen ademas, del propio diario, los pedestales (`static_map.pedestals`), la camara (`mundo_leido`: centro y celdas) y los objetos a la vista (`ve_items`).
  python3 analiza_P7_21.py -> P7_21_vidas.json

DEFINICIONES, escritas antes de contar:
  CAJAS: los 16 pedestales del mapa (`static_map.pedestals`, donde el mundo pone los objetos). OBJETO A LA VISTA: cada entrada de `ve_items` del tic.
  CAMARA: la fortaleza central (`mundo_leido`: 49 celdas en torno al centro (24,24): un cuadrado de 7x7). Distancia a la camara = distancia Chebyshev
    al centro menos 3, y 0 dentro. Distancias en casillas (Chebyshev).
  CERCA DE CAJAS O CAMARA: a 3 casillas o menos de un pedestal, o a 3 o menos de la camara.
  MUERTE: `final.reason` = "eliminated"; temprana si el ultimo tic es anterior a 11.000 (y, aparte, a 12.000). PRIMER GOLPE DE LA PELEA FINAL: el de
    P7-20 (primer dano de rival de la ultima racha de dano, que acaba en la muerte; si la racha empieza con el anillo, el primer golpe de rival de la racha).
  QUE LA LLEVO ALLI: lo elegido (`RADIOGRAFIA.elegido`) en los 30 s (720 tics) anteriores al primer golpe de la pelea final, en partes; `ir_objeto` se
    separa en "a por el botiquin" y "a por otro objeto" segun el objeto a la vista mas cercano al que el paso elegido acerca (aproximacion: el diario no
    guarda el objeto al que va el candidato). Y el ultimo `ir_*` elegido antes del primer golpe.
  CANAL: tics seguidos con `channeling` del botiquin en `effects`; se abre en el primero. Se COMPLETA si al cerrarse lleva un botiquin menos que al abrirse;
    si no, lo CORTA algo: "dano de rival" o "dano del anillo" si lo hubo en el tic del cierre o en el anterior, y si no "sin dano registrado".
  DENTRO DEL CIRCULO: distancia euclidea al centro de la zona <= su radio en el tic de apertura.
  GOLPEADO ANTES: algun dano (rival o anillo) en los 48 tics anteriores a la apertura; y, aparte, en los 24.
  SE MOVIO: la posicion cambio en algun tic del canal (del de apertura al ultimo con el canal abierto).
"""
import collections, glob, json, os
from multiprocessing import Pool
import analiza_P7_16 as A16, analiza_P7_20 as A20
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
V30 = 720; DIR = A16.DIR; cheb = A16.cheb
IR = ("ir_curioso", "ir_objeto", "ir_centro", "ir_pareja", "ir_botiquin", "ir_recurso")


def lee_mundo(f):
    ped = None; centro = None; lado = None
    for line in open(f):
        if '"static_map"' not in line and '"mundo_leido"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "static_map" and ped is None: ped = [tuple(p) for p in r.get("pedestals") or []]
        elif r.get("k") == "mundo_leido":
            n = int(r.get("camara_celdas") or 49); lado = int(round(n ** 0.5)) // 2
            for a in r.get("avisos") or []:
                if "camara" in a and "centro" in a:
                    s = a[a.index("centro (") + 8:]; cx, cy = s[:s.index(")")].split(","); centro = (float(cx), float(cy))
        if ped is not None and centro is not None: break
    return ped or [], centro or (24.0, 24.0), lado or 3


def lee_extra(f):
    """Por tic: objetos a la vista y la zona (lo que `lee` de P7-16 no guarda)."""
    X = {}
    for line in open(f):
        if '"k": "tick"' not in line and '"k":"tick"' not in line: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") != "tick" or r.get("phase") != "live": continue
        z = r.get("zona") or {}
        X[r["tick"]] = {"items": [(it.get("id"), tuple(it["pos"])) for it in (r.get("ve_items") or []) if it.get("pos")], "zc": tuple(z["center"]) if z.get("center") else None, "zr": z.get("radius")}
    return X


def sitio(pos, ped, centro, lado, items):
    dp = min((cheb(pos, p) for p in ped), default=None); dc = max(0, cheb(pos, (int(centro[0]), int(centro[1]))) - lado)
    do = min((cheb(pos, q) for _, q in items), default=None)
    return {"d_caja": dp, "d_objeto_visto": do, "d_camara": dc, "cerca": bool((dp is not None and dp <= 3) or dc <= 3)}


def que_la_llevo(T, X, M, i_fin):
    """Lo elegido en los 720 tics antes del indice i_fin, en partes, y el ultimo ir_* elegido."""
    kid = M["kit"]; c = collections.Counter(); ultimo = None; n = 0
    for t in T[max(0, i_fin - V30):i_fin]:
        el = t["el"]; n += 1
        if el == "ir_objeto":
            d = DIR.get(((t.get("accion") or {}).get("dir")) or "", None)
            clase = "ir_objeto (otro)"
            it = X.get(t["t"], {}).get("items") or []
            if d and it:
                np_ = (t["pos"][0] + d[0], t["pos"][1] + d[1]); acerca = [(cheb(np_, q), i_, q) for i_, q in it if cheb(np_, q) < cheb(t["pos"], q)]
                if acerca and min(acerca)[1] == kid: clase = "ir_objeto (botiquin)"
            c[clase] += 1
        elif el.startswith("ir_"): c[el] += 1
        elif el.startswith(("move_", "paso_")): c["paso"] += 1
        elif el.startswith("atacar"): c["atacar"] += 1
        elif el in ("noop", "usar_botiquin", "coger") or el.startswith(("soltar_", "hacer_sitio")): c[el if el in ("noop", "usar_botiquin", "coger") else "soltar/hacer sitio"] += 1
        else: c["otro"] += 1
        if el.startswith("ir_"): ultimo = el if el != "ir_objeto" else clase
    return {"tics": n, "partes": {k: v / n for k, v in c.items()} if n else {}, "ultimo_ir": ultimo}


def canales(T, X, M):
    kid = M["kit"]; out = []; v = None; prev = None
    for i, t in enumerate(T):
        if v is None and t["canal"]:
            z = X.get(t["t"], {}); dentro = (z.get("zc") is not None and z.get("zr") is not None and ((t["pos"][0] - z["zc"][0]) ** 2 + (t["pos"][1] - z["zc"][1]) ** 2) ** 0.5 <= z["zr"])
            g48 = any(s_ for j in range(max(0, i - 48), i) for s_, _ in T[j]["dmg"]); g24 = any(s_ for j in range(max(0, i - 24), i) for s_, _ in T[j]["dmg"])
            v = {"t0": t["t"], "i0": i, "kits0": t["kits"], "dentro": bool(dentro), "golpeado_48": bool(g48), "golpeado_24": bool(g24), "pos0": t["pos"], "hp0": t["hp"], "se_movio": False}
        elif v is not None and t["canal"]:
            if t["pos"] != v["pos0"]: v["se_movio"] = True
        elif v is not None and not t["canal"]:
            dr = any(s_.startswith("P") for j in (i - 1, i) for s_, _ in T[j]["dmg"]); dz = any(s_ == "zone" for j in (i - 1, i) for s_, _ in T[j]["dmg"])
            v.update({"dura": t["t"] - v["t0"], "completado": t["kits"] < v["kits0"], "hp_fin": t["hp"], "causa_corte": None if t["kits"] < v["kits0"] else ("dano de rival" if dr else "dano del anillo" if dz else "sin dano registrado")})
            out.append(v); v = None
    if v is not None: v.update({"dura": T[-1]["t"] - v["t0"], "completado": False, "hp_fin": T[-1]["hp"], "causa_corte": "muere con el canal abierto"}); out.append(v)
    for c in out: c.pop("i0", None)
    return out


def una_carpeta(x):
    campo, carp = x; b = os.path.basename(carp).split("_"); serie = int(b[1][1:]); dia = int(b[2][1:]); brazo = "ESPERANZA" if b[3] == "SUELO" else b[3]; out = {}
    for sl in (10, 11):
        f = glob.glob(os.path.join(carp, f"*policy_agent_{sl}.art.log"))
        if not f: continue
        M, T = A16.lee(f[0])
        if not T: continue
        ped, centro, lado = lee_mundo(f[0]); X = lee_extra(f[0])
        # la accion elegida (direccion del paso) no la guarda `lee`: se lee del extra con un segundo paso ligero
        for t in T: t["accion"] = None
        acc = {}
        for line in open(f[0]):
            if '"RADIOGRAFIA"' not in line: continue
            try: r = json.loads(line)
            except Exception: continue
            if r.get("k") == "tick": acc[r["tick"]] = (r.get("RADIOGRAFIA") or {}).get("accion")
        for t in T: t["accion"] = acc.get(t["t"])
        murio = (M["final"] or {}).get("reason") == "eliminated"; P = A20.peleas(M, T, murio)
        v = {"campo": campo, "serie": serie, "dia": dia, "brazo": brazo, "slot": sl, "semilla": int(b[4]), "ultimo_tick": T[-1]["t"], "murio": murio, "pedestales": len(ped), "camara_centro": centro}
        if murio:
            iF = len(T) - 1; tF = T[iF]; v["en_la_muerte"] = sitio(tF["pos"], ped, centro, lado, X.get(tF["t"], {}).get("items") or [])
            v["cerca_en_los_30_s_antes_de_morir"] = sum(1 for t in T[max(0, iF - V30):iF] if sitio(t["pos"], ped, centro, lado, [])["cerca"]) / max(1, min(V30, iF))
            pm = [p for p in P if p["acaba_en_muerte"]]
            if pm:
                tg = pm[0]["t_primer_golpe_de_rival"]; ig = next(i for i, t in enumerate(T) if t["t"] == tg)
                v["en_el_primer_golpe"] = sitio(T[ig]["pos"], ped, centro, lado, X.get(tg, {}).get("items") or []); v["en_el_primer_golpe"]["t"] = tg
                v["cerca_en_los_30_s_antes_del_golpe"] = sum(1 for t in T[max(0, ig - V30):ig] if sitio(t["pos"], ped, centro, lado, [])["cerca"]) / max(1, min(V30, ig))
                v["que_la_llevo"] = que_la_llevo(T, X, M, ig)
            else: v["en_el_primer_golpe"] = None
        v["canales"] = canales(T, X, M)
        out[f"{campo}|s{serie}_d{dia}_{brazo}_{sl}"] = v
    return out


if __name__ == "__main__":
    carps = [("P7-10", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s*_d*_*_*")))] + [("P7-14b", c) for c in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d*_*_*")))]
    OUT = {}
    with Pool(4) as Pl:
        for o in Pl.imap_unordered(una_carpeta, carps): OUT.update(o)
    json.dump(dict(sorted(OUT.items())), open(os.path.join(AQUI, "P7_21_vidas.json"), "w"), ensure_ascii=False)
    print("vidas", len(OUT), "· muertes", sum(1 for v in OUT.values() if v["murio"]), "· canales", sum(len(v["canales"]) for v in OUT.values()))

"""[P6-7] POR QUE LA PAREJA CON OJOS COMPARTIDOS VIVE MENOS. SOLO LECTURA.

Diarios de P6-6 (A0 y A1, las mismas 20 semillas). Coste cero.

LO QUE EL DIARIO NO DICE, y aqui no se estima:
  · Los rivales CONTADOS no van en `ve_agentes` (el diario guarda la obs cruda).
    Se reconstruyen como en P6-4: el ultimo E2 del hermano en `chat`, con edad
    <= oyente2.CADUCIDAD_RIVAL, y sin los asientos que YO ya veo (asi los mete
    `oyente2.inyecta`). Es la misma regla, no una suposicion.
  · La posicion REAL de un rival contado no esta en ningun diario nuestro. "Ya
    movido" se certifica solo por dos vias: el hermano lo ve en OTRA casilla en
    ese mismo tic, o la casilla dicha esta a la vista mia y vacia.
  · El detalle de candidatos (`pos_prevista`) solo se guarda cada 24 tics; la
    direccion elegida se lee de `intencion.dir`, que esta en TODOS los tics.

PUNTO 1 · F-HERMANO-AMENAZA (criterio de la fila, appraisal_zs_v42_exp.py:1585+:
  hostil con arma de dano > 0 y el hermano dentro de su ALCANCE, o agresor
  certificado). Por tic encendido se recalcula que hostiles cumplen: VISTOS por
  mi o CONTADOS por el hermano. Y que eligio el cuerpo: `intencion.dir` acerca o
  aleja del hermano / del hostil.
PUNTO 2 · rival contado ya movido: certificado como arriba; "actua" = el cuerpo
  da un paso (intencion move) que cambia su distancia a la casilla dicha.
PUNTO 3 · muertes: regla de E3_golpes.py (ultimo golpe en los 48 tics antes de
  `match_ticks`; si no hay, "no consta"), tic, y distancia al hermano.
"""
import collections, glob, json, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper4"))
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
import serie_util as U
import parte2 as P2
import oyente2 as OY
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A

NUESTROS = (10, 11)
ULT = 200            # tics antes de morir que se miran (punto 1c)
VENT_GOLPE = 48      # la de E3


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def fam(e):
    e = str(e or "")
    for p in ("soltar_", "usar_", "ir_", "move_", "paso_", "atacar", "coger",
              "noop", "empunar", "ponerse_"):
        if e.startswith(p):
            return p.rstrip("_")
    return e or "otro"


def carga(f):
    recs = list(U.lee(f))
    pc = next(r for r in recs if r.get("k") == "player_config")
    sm = next(r for r in recs if r.get("k") == "static_map")
    cat = next(r for r in recs if r.get("k") == "catalogo")
    mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
    fin = next((r for r in recs if r.get("k") == "final"), None)
    intel = 5
    for r in recs:
        if r.get("k") == "arranque":
            m = re.search(r'"intelligence"\s*:\s*(\d+)', json.dumps(r))
            if m:
                intel = int(m.group(1))
            break
    T = {}
    for r in recs:
        if r.get("k") != "tick" or r.get("phase") != "live":
            continue
        ra = r.get("RADIOGRAFIA") or {}
        ah = ra.get("ahora") or {}
        it = r.get("intencion") or {}
        T[r["tick"]] = {
            "pos": tuple(int(x) for x in (r.get("pos") or (0, 0))),
            "hp": r.get("hp"),
            "filas": set((ah.get("filas") or {}).keys()),
            "el": ra.get("elegido"),
            "do": it.get("do"), "dir": it.get("dir"),
            "ve": [(a.get("slot"), (int(a["pos"][0]), int(a["pos"][1])),
                    a.get("hand") if isinstance(a.get("hand"), str)
                    else (a.get("hand") or {}).get("id"))
                   for a in (r.get("ve_agentes") or []) if a.get("pos")],
            "e2": [m.get("text") for m in (r.get("chat") or [])
                   if m.get("channel") == "team" and m.get("from") == pc.get("teammate_slot")
                   and (m.get("text") or "").startswith("E2 ")],
            "parte": ah.get("parte"),
            "dmg": [(g.get("source"), g.get("amount")) for g in (r.get("damage_taken") or [])],
            "listas": int(r.get("move_ready_in") or 0) == 0,
        }
    del recs
    return mundo, pc, T, fin, intel


def contados_por_tic(T, mundo):
    """{tick: {slot: (pos, arma)}} de rivales contados VIGENTES y no vistos."""
    out, ult = {}, None
    for t in sorted(T):
        for txt in T[t]["e2"]:
            p = P2.parsea(txt, mundo)
            if p:
                ult = p
        if ult and 0 <= t - ult["t"] <= OY.CADUCIDAD_RIVAL:
            vistos = {s for s, _p, _h in T[t]["ve"]}
            out[t] = {r["slot"]: (tuple(r["pos"]), r.get("arma"))
                      for r in ult["rivales"] if r["slot"] not in vistos}
        else:
            out[t] = {}
    return out


def arma_ER(mundo, w):
    it = mundo.items.get(w) if w else None
    if not it:
        return 0.0, 0
    return float(getattr(it, "damage", 0) or 0), int(getattr(it, "range", 0) or 0)


def pos_hermano(r, herm):
    p = r["parte"]
    if p and p.get("pos"):
        return tuple(p["pos"]), "parte"
    for s, q, _h in r["ve"]:
        if s == herm:
            return q, "vista"
    return None, None


def mide_vida(sl, T, To, mundo, pc, fin, intel, CONT, S, DET, brazo):
    herm = pc.get("teammate_slot")
    yo = pc.get("slot")
    radio = mundo.radio_vision(intel)
    tics = sorted(T)
    # ── PUNTO 1a / 1b ────────────────────────────────────────────────────
    for t in tics:
        r = T[t]
        if "F-HERMANO-AMENAZA" not in r["filas"]:
            continue
        S["1a · tics con F-HERMANO-AMENAZA"] += 1
        ph, fuente = pos_hermano(r, herm)
        cert_pos = (tuple(r["parte"]["agresor_pos"]) if r["parte"] and r["parte"].get("agresor")
                    and r["parte"].get("agresor_pos") else None)
        V, C = [], []
        for s, q, h in r["ve"]:
            if s in (yo, herm):
                continue
            E, R = arma_ER(mundo, h)
            if E <= 0:
                continue
            en = ph is not None and R and cheb(q, ph) <= R
            ce = cert_pos is not None and cheb(q, cert_pos) <= A.MANADA_TOL
            if en or ce:
                V.append((s, q, h))
        for s, (q, h) in CONT.get(t, {}).items():
            E, R = arma_ER(mundo, h)
            if E <= 0:
                continue
            if ph is not None and R and cheb(q, ph) <= R:
                C.append((s, q, h))
        clase = ("ambos" if V and C else "solo VISTO" if V else
                 "solo CONTADO" if C else "no reconstruible")
        S[f"1a · {clase}"] += 1
        # 1b: que elige
        S[f"1b · elegido {fam(r['el'])}"] += 1
        if r["do"] == "move" and r["dir"] in D.DIRS:
            dx, dy = D.DIRS[r["dir"]]
            nxt = (r["pos"][0] + dx, r["pos"][1] + dy)
            S["1b · pasos (intencion move)"] += 1
            if ph is not None:
                d0, d1 = cheb(r["pos"], ph), cheb(nxt, ph)
                S["1b · paso ACERCA al hermano" if d1 < d0 else
                  "1b · paso ALEJA del hermano" if d1 > d0 else "1b · paso neutro al hermano"] += 1
            hs = V + C
            if hs:
                q = min(hs, key=lambda x: cheb(r["pos"], x[1]))[1]
                d0, d1 = cheb(r["pos"], q), cheb(nxt, q)
                S["1b · paso ACERCA al hostil" if d1 < d0 else
                  "1b · paso ALEJA del hostil" if d1 > d0 else "1b · paso neutro al hostil"] += 1
                if C and not V:
                    S["1b · (solo contado) paso ACERCA al hostil" if d1 < d0 else
                      "1b · (solo contado) paso ALEJA del hostil" if d1 > d0 else
                      "1b · (solo contado) paso neutro"] += 1
        elif r["do"] in (None, "none"):
            S["1b · se queda quieto (do none)"] += 1
    # ── PUNTO 2 · rival contado ya movido ────────────────────────────────
    for t in tics:
        r = T[t]
        for s, (q, h) in CONT.get(t, {}).items():
            S["2 · tics×rival contado"] += 1
            # certificacion de "ya movido"
            vh = next((qq for ss, qq, _ in (To.get(t, {}).get("ve") or []) if ss == s), None)
            movido = None
            if vh is not None and vh != q:
                movido = "hermano lo ve en OTRA casilla"
            elif cheb(r["pos"], q) <= radio and not any(qq == q for _s, qq, _h in r["ve"]) \
                    and mundo.linea_de_vista(r["pos"], q):
                movido = "casilla dicha a mi vista y VACIA"
            if movido is None:
                continue
            S["2 · rival contado YA MOVIDO (certificado)"] += 1
            S[f"2 · certificado por: {movido}"] += 1
            if r["do"] == "move" and r["dir"] in D.DIRS:
                dx, dy = D.DIRS[r["dir"]]
                nxt = (r["pos"][0] + dx, r["pos"][1] + dy)
                d0, d1 = cheb(r["pos"], q), cheb(nxt, q)
                if d1 == d0:
                    continue
                k = "se APARTA de la casilla vacia" if d1 > d0 else "va HACIA la casilla vacia"
                S[f"2 · paso que {k}"] += 1
                S["2 · tics comprometidos (pasos × coste)"] += mundo.coste_movimiento(5)
                # ¿le cuesta golpes en los 48 tics siguientes?
                gol = [g for tt in range(t, t + VENT_GOLPE + 1) if tt in T
                       for g in T[tt]["dmg"] if str(g[0]).startswith("P")]
                if gol:
                    S[f"2 · ...y recibe golpe de rival en 48 tics ({k})"] += 1
    # ── PUNTO 3 · de que muere ───────────────────────────────────────────
    d = {"brazo": brazo, "slot": sl}
    if fin and fin.get("reason") == "eliminated":
        mt = int(fin.get("match_ticks") or tics[-1])
        ult = [(tt, g[0]) for tt in tics if mt - VENT_GOLPE <= tt <= mt for g in T[tt]["dmg"]]
        src = ult[-1][1] if ult else None
        causa = ("anillo" if src == "zone" else "rival visto/no visto" if str(src).startswith("P")
                 else "no consta" if src is None else f"otro ({src})")
        if causa.startswith("rival"):
            # ¿lo veia en el tic del golpe?
            tt = ult[-1][0]
            slot = int(str(src)[1:])
            veia = any(s == slot for s, _q, _h in T[tt]["ve"]) if tt in T else False
            causa = "rival VISTO" if veia else "rival NO visto"
        d.update({"muere": True, "tic": mt, "causa": causa, "fuente": src})
        # distancia al hermano en el ultimo tic vivo
        tl = tics[-1]
        if To and tl in To:
            d["dist_hermano"] = cheb(T[tl]["pos"], To[tl]["pos"]); d["hermano_vivo"] = True
        else:
            d["dist_hermano"] = None; d["hermano_vivo"] = False
        # 1c: los 200 ultimos tics
        v = [tt for tt in tics if tl - ULT < tt <= tl]
        c = collections.Counter(fam(T[tt]["el"]) for tt in v)
        d["ult200"] = {
            "tics": len(v), "elegido": dict(c),
            "F-HERMANO-AMENAZA on": sum(1 for tt in v if "F-HERMANO-AMENAZA" in T[tt]["filas"]),
            "F-DANO on": sum(1 for tt in v if "F-DANO" in T[tt]["filas"]),
            "S-7-AGRESOR on": sum(1 for tt in v if "S-7-AGRESOR" in T[tt]["filas"]),
            "tics con rival contado": sum(1 for tt in v if CONT.get(tt)),
            "pasos": 0, "pasos hacia contado": 0, "pasos hacia visto armado": 0,
            "pasos hacia hermano": 0, "golpes": collections.Counter(),
        }
        for tt in v:
            r = T[tt]
            for g in r["dmg"]:
                d["ult200"]["golpes"][str(g[0])] += 1
            if r["do"] == "move" and r["dir"] in D.DIRS:
                dx, dy = D.DIRS[r["dir"]]
                nxt = (r["pos"][0] + dx, r["pos"][1] + dy)
                d["ult200"]["pasos"] += 1
                for s, (q, h) in CONT.get(tt, {}).items():
                    if cheb(nxt, q) < cheb(r["pos"], q):
                        d["ult200"]["pasos hacia contado"] += 1; break
                for s, q, h in r["ve"]:
                    if s in (yo, herm):
                        continue
                    if arma_ER(mundo, h)[0] > 0 and cheb(nxt, q) < cheb(r["pos"], q):
                        d["ult200"]["pasos hacia visto armado"] += 1; break
                ph, _ = pos_hermano(r, herm)
                if ph and cheb(nxt, ph) < cheb(r["pos"], ph):
                    d["ult200"]["pasos hacia hermano"] += 1
        d["ult200"]["golpes"] = dict(d["ult200"]["golpes"])
    else:
        d.update({"muere": False, "tic": tics[-1], "causa": "sobrevive"})
    DET.append(d)


def mide(pat, brazo):
    S, DET = collections.Counter(), []
    carps = []
    for p in pat.split(","):
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        fs = {}
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
            if sl in NUESTROS:
                fs[sl] = f
        if len(fs) != 2:
            continue
        L = {sl: carga(f) for sl, f in fs.items()}
        sem = re.search(r"_(\d{8})$", carp).group(1)
        S["partidas"] += 1
        for sl in NUESTROS:
            otro = NUESTROS[1] if sl == NUESTROS[0] else NUESTROS[0]
            mundo, pc, T, fin, intel = L[sl]
            To = L[otro][2]
            CONT = contados_por_tic(T, mundo)
            n0 = len(DET)
            mide_vida(sl, T, To, mundo, pc, fin, intel, CONT, S, DET, brazo)
            for d in DET[n0:]:
                d["semilla"] = sem
        del L
        print(f"    {os.path.basename(carp)}", flush=True)
    return S, DET


OUT = {}
for etiq, pat in [x.split("=", 1) for x in sys.argv[1:]]:
    print(f"### {etiq}", flush=True)
    S, DET = mide(pat, etiq)
    OUT[etiq] = {"recuento": dict(S), "vidas": DET}
    for k, v in sorted(S.items()):
        print(f"  {k:60s} {v}")
json.dump(OUT, open(os.path.join(AQUI, "P6_8_p67.json"), "w"), ensure_ascii=False, indent=1)
print("\n-> cantera/paper6/P6_8_p67.json")

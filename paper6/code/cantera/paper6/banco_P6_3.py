"""EL BANCO DE LOS OJOS COMPARTIDOS — sin jugar ni una partida. [P6-3]

Repite los 20 diarios del G2 de P6-1 haciendo hablar a los dos hermanos con
E2, y pregunta UNA sola cosa: **¿habria llegado la informacion a tiempo?**

NO dice que habria hecho el cuerpo. Con la informacion dentro, el cuerpo
decide otra cosa, el mundo responde otra cosa y el diario deja de valer. Aqui
solo se mide el CANAL.

  a) el mensaje nunca pasa de 120 caracteres ni de la tasa
  b) de los 488 episodios de amenaza a ciegas y las 1.954 ocasiones de recurso,
     cuantos habrian estado en la percepcion del que le hacia falta
  c) cuanto habria bajado la discrepancia de S-8-EXPOSICION

CONTROL OBLIGATORIO antes de usar nada: la S-8 que calcula este banco tiene
que reproducir la que el diario ya trae. Si no, el (c) no vale.
"""
import collections, glob, json, math, os, re, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "paper4"))
sys.path.insert(0, os.path.join(AQUI, "..", "paper5"))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "paintball"))
import serie_util as U
from alma import appraisal_zs_v42_exp as A42
import parte2 as P2
import oyente2 as OY

NUESTROS = (10, 11)
LATENCIA = 2          # medida en el PROMPT_52 y confirmada en P6-2
S = {"largos": [], "huecos": [], "c": collections.Counter(),
     "s8_control": [], "s8_control_proy": [], "cobertura_2d": [],
     "cobertura_2c": [],
     "s8_disc": []}


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def s8_de(pos, agentes, mundo, herm, cuerpo=None, ult_ataque=-10 ** 9,
          tick=0, moviendo=False):
    """S-8-EXPOSICION con las constantes IMPORTADAS de v42 (nunca copiadas).

    Reproduce `appraisal_zs_v42_exp.py:1390-1416`, con la rama del CAMUFLAJE.
    La primera version la dejaba fuera y fallaba en 6.838 tics de 156.634
    —todos, exactamente, con el camuflaje puesto—: quien va camuflado solo es
    visto desde mas cerca. Se valida contra la fila del propio diario antes de
    usarse para nada.
    """
    radio_h = mundo.radio_vision_max()
    camo = bool(mundo.id_camuflaje) and cuerpo == mundo.id_camuflaje
    delatado = ((tick - ult_ataque) <= A42.CAMO_REVELADO_S * mundo.tick_rate
                if ult_ataque >= 0 else False)
    tope = ((A42.CAMO_MOVIENDO if moviendo else A42.CAMO_QUIETO)
            if (camo and not delatado) else None)
    suma = 0.0
    for a in agentes:
        sl = a.get("slot")
        if sl == mundo.slot or sl == herm:
            continue
        q = tuple(a.get("pos") or ())
        if not q:
            continue
        d = math.dist(pos, q)
        if d > radio_h:
            continue
        if tope is not None and d > tope:
            continue
        if not mundo.linea_de_vista(q, pos):
            continue
        suma += A42.EXPO_POR_HOSTIL * max(0.0, 1.0 - d / radio_h)
    return min(A42.EXPO_CAP, suma)


class Diario:
    def __init__(self, f):
        recs = list(U.lee(f))
        pc = next(r for r in recs if r.get("k") == "player_config")
        sm = next(r for r in recs if r.get("k") == "static_map")
        cat = next(r for r in recs if r.get("k") == "catalogo")
        self.mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
        self.slot = pc["slot"]
        self.herm = pc.get("teammate_slot")
        self.T = {}
        for r in recs:
            if r.get("k") != "tick" or r.get("phase") != "live":
                continue
            ra = r.get("RADIOGRAFIA") or {}
            self.T[r["tick"]] = {
                "pos": tuple(r.get("pos") or ()),
                "hp": r.get("hp"),
                "hand": (r.get("hand") or {}).get("id"),
                "body": (r.get("body") or {}).get("id")
                        if isinstance(r.get("body"), dict) else r.get("body"),
                "pack": [s for s in (r.get("pack") or []) if s],
                "pack_n": {(s or {}).get("id"): int((s or {}).get("n") or 1)
                           for s in (r.get("pack") or []) if s},
                "effects": r.get("effects") or [],
                "items": [(x.get("id"), (int(x["pos"][0]), int(x["pos"][1])))
                          for x in (r.get("ve_items") or []) if x.get("pos")],
                "ag": [{"slot": a.get("slot"),
                        "pos": [int(a["pos"][0]), int(a["pos"][1])],
                        "hand": a.get("hand"), "hp_band": a.get("hp_band")}
                       for a in (r.get("ve_agentes") or []) if a.get("pos")],
                "listas": int(r.get("move_ready_in") or 0) == 0,
                "filas": {k: v.get("M") for k, v in
                          ((ra.get("ahora") or {}).get("filas") or {}).items()},
                "cand": ra.get("candidatos"), "elegido": ra.get("elegido"),
                "d_ahora": ra.get("d_ahora"),
            }
        del recs

    def obs(self, t):
        r = self.T[t]
        return {"you": {"pos": list(r["pos"]), "hp": r["hp"],
                        "pack": r["pack"], "effects": r["effects"],
                        "hand": {"id": r["hand"] or "none"}},
                "visible": {"agents": [dict(a) for a in r["ag"]],
                            "items": [{"id": i, "pos": [p[0], p[1]], "n": 1}
                                      for i, p in r["items"]]},
                "chat": []}


class MemFalsa:
    def __init__(self):
        self.agresores = {}


def clase(mundo, iid):
    return P2.clase_de(mundo, iid)


def le_falta(r, cls, mundo):
    if cls == "arma":
        return r["hand"] in (None, "none")
    if cls == "botiquin":
        return r["pack_n"].get(mundo.id_botiquin, 0) == 0
    if cls == "raciones":
        return not any(r["pack_n"].get(i, 0) for i in (mundo.id_raciones or []))
    if cls == "mochila":
        return r["body"] in (None, "none")
    return False


for carp in sorted(glob.glob(os.path.join(AQUI, "..", "..", "paintball",
                                          "runs", "P61_t[34]_G2_*"))):
    D = {}
    for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
        sl = int(re.search(r"policy_agent_(\d+)\.art\.log$", f).group(1))
        if sl in NUESTROS:
            D[sl] = Diario(f)
    if len(D) != 2:
        continue
    a, b = NUESTROS
    mundo = D[a].mundo
    S["c"]["episodios"] += 1
    # ── el canal, simulado en los dos sentidos ────────────────────────────
    #   emite cada CADA tics desde el primer tic vivo; llega LATENCIA despues
    buzon = {a: {}, b: {}}        # destinatario -> {tic_de_llegada: parte}
    for em in (a, b):
        dst = b if em == a else a
        oj = P2.Ojeador()
        ts = sorted(D[em].T)
        if not ts:
            continue
        t0 = ts[0]
        ult_recibido = None
        for t in ts:
            if (t - t0) % P2.CADA:
                continue
            # lo que el emisor sabe del hermano en ese momento: su ultimo parte
            frescos = [p for tt, p in buzon[em].items()
                       if tt <= t and 0 <= t - p["t"] <= P2.CADUCIDAD]
            ph = max(frescos, key=lambda p: p["t"]) if frescos else None
            det = {}
            txt = P2.emite(D[em].obs(t), t, mundo, MemFalsa(), 120, oj, ph, det)
            S["largos"].append(len(txt))
            S["huecos"].append(P2.CADA)
            p = P2.parsea(txt, mundo)
            assert p is not None, txt
            buzon[dst][t + LATENCIA] = p
            S["c"]["partes emitidos"] += 1
            S["c"]["rivales que caben"] += det["rivales_dentro"]
            S["c"]["rivales que NO caben"] += (det["rivales_vistos"]
                                               - det["rivales_dentro"])
            S["c"]["recursos que caben"] += det["recursos_dentro"]
            S["c"]["recursos que NO caben"] += (det["recursos_vistos"]
                                                - det["recursos_dentro"])
    # ── la percepcion inyectada, tic a tic ────────────────────────────────
    INY = {a: {}, b: {}}
    for sl in (a, b):
        llegan = sorted(buzon[sl])
        ult, k = None, 0
        for t in sorted(D[sl].T):
            while k < len(llegan) and llegan[k] <= t:
                ult = buzon[sl][llegan[k]]; k += 1
            if ult is None:
                INY[sl][t] = ({}, {})
                continue
            edad = t - ult["t"]
            riv = ({r["slot"]: r for r in ult["rivales"]}
                   if 0 <= edad <= OY.CADUCIDAD_RIVAL else {})
            rec = ({(x["id"], tuple(x["pos"])): x for x in ult["recursos"]}
                   if 0 <= edad and OY.peso_recurso(edad) >= OY.UMBRAL_REC
                   else {})
            INY[sl][t] = (riv, rec)
    # ── control de S-8 ────────────────────────────────────────────────────
    ULT_AT = {}
    for sl in (a, b):
        ua = -10 ** 9
        for t in sorted(D[sl].T):
            ULT_AT[(sl, t)] = ua
            if str(D[sl].T[t].get("elegido") or "").startswith("atacar_"):
                ua = t
        for t, r in D[sl].T.items():
            if "S-8-EXPOSICION" not in r["filas"] or not r["pos"]:
                continue
            mio = s8_de(r["pos"], r["ag"], mundo, D[sl].herm, r["body"],
                        ULT_AT[(sl, t)], t, False)
            S["s8_control"].append(abs(mio - r["filas"]["S-8-EXPOSICION"]))
    # ── (b) cobertura de 2d y 2c ──────────────────────────────────────────
    juntos = sorted(set(D[a].T) & set(D[b].T))
    ev2d, ev2c = [], []
    for t in juntos:
        ra, rb = D[a].T[t], D[b].T[t]
        if not (ra["pos"] and rb["pos"]):
            continue
        for quien, otro, rq, ro in ((a, b, ra, rb), (b, a, rb, ra)):
            vistos_o = {x["slot"] for x in ro["ag"]}
            for x in rq["ag"]:
                s_ = x["slot"]
                if s_ in NUESTROS or s_ in vistos_o:
                    continue
                mano = (x.get("hand") or {}).get("id") if isinstance(x.get("hand"), dict) else x.get("hand")
                rg = P2._alcance(mundo, mano)
                if rg <= 0 or cheb(tuple(x["pos"]), ro["pos"]) > rg:
                    continue
                ev2d.append((t, otro, s_))
            iq = {(i, p) for i, p in rq["items"]}
            io = {(i, p) for i, p in ro["items"]}
            for iid, p in (iq - io):
                cl = clase(mundo, iid)
                if cl in ("otro", "municion", "gear"):
                    continue
                if not le_falta(ro, cl, mundo):
                    continue
                if (ro["filas"].get("R-CARENCIA") or 0) <= 0:
                    continue
                ev2c.append((t, otro, iid, p))
    for t, quien, s_ in ev2d:
        S["cobertura_2d"].append(1 if s_ in INY[quien].get(t, ({}, {}))[0] else 0)
    for t, quien, iid, p in ev2c:
        S["cobertura_2c"].append(1 if (iid, p) in INY[quien].get(t, ({}, {}))[1]
                                 else 0)
    S["c"]["tics 2d"] += len(ev2d)
    S["c"]["tics 2c"] += len(ev2c)
    # ── (c) la discrepancia de S-8 ────────────────────────────────────────
    for sl in (a, b):
        ts = sorted(D[sl].T)
        listas = [t for t in ts if D[sl].T[t]["listas"]]
        for i, t in enumerate(listas[:-1]):
            t2 = listas[i + 1]
            r, r2 = D[sl].T[t], D[sl].T[t2]
            cand, el = r["cand"], r["elegido"]
            if not cand or el not in (cand or {}):
                continue
            c = cand[el]
            if not isinstance(c, dict) or c.get("filas") is None:
                continue
            proy = float(c["filas"].get("S-8-EXPOSICION") or 0.0)
            real = float(r2["filas"].get("S-8-EXPOSICION") or 0.0)
            if abs(real - proy) < 1e-9:
                continue
            # lo mismo, pero con los rivales CONTADOS dentro de la proyeccion
            riv = INY[sl].get(t, ({}, {}))[0]
            pos_prev = tuple(c.get("pos_prevista") or r["pos"])
            ya = {x["slot"] for x in r["ag"]}
            ags = [dict(x) for x in r["ag"]]
            n_extra = 0
            for s_, rr in riv.items():
                if s_ in ya or s_ in NUESTROS:
                    continue
                ags.append({"slot": s_, "pos": list(rr["pos"]),
                            "hand": {"id": rr.get("arma") or "none"}})
                n_extra += 1
            proy2 = s8_de(pos_prev, ags, mundo, D[sl].herm, r["body"],
                          ULT_AT[(sl, t)], t,
                          tuple(pos_prev) != tuple(r["pos"]))
            # control del contrafactico: SIN rivales contados tiene que dar
            # exactamente la `proy` que el diario guardo
            ctrl = s8_de(pos_prev, r["ag"], mundo, D[sl].herm, r["body"],
                         ULT_AT[(sl, t)], t,
                         tuple(pos_prev) != tuple(r["pos"]))
            S["s8_control_proy"].append(abs(ctrl - proy))
            S["s8_disc"].append({"tick": t, "slot": sl, "proy": proy,
                                 "real": real, "proy_con": proy2,
                                 "extra": n_extra,
                                 "disc": real - proy,
                                 "disc_con": real - proy2})
    del D, INY, buzon
    print(f"  {os.path.basename(carp)}: listo", flush=True)

# ══════════════════════════════════════════════════════════════════════════
print("\n═══ CONTROL: ¿mi S-8 es la del diario? ═══")
E = S["s8_control"]
print(f"  AHORA      : {len(E):,} tics · peor {max(E):.6f} · "
      f"por encima de 1e-4: {sum(1 for x in E if x > 1e-4)} "
      f"({100*sum(1 for x in E if x > 1e-4)/len(E):.3f} %)")
P = S["s8_control_proy"]
if P:
    print(f"  PROYECTADA : {len(P):,} candidatos · peor {max(P):.6f} · "
          f"por encima de 1e-4: {sum(1 for x in P if x > 1e-4)} "
          f"({100*sum(1 for x in P if x > 1e-4)/len(P):.3f} %)")

print("\n═══ a · el mensaje ═══")
L = S["largos"]
print(f"  {len(L):,} partes · largo min {min(L)} · mediana {st.median(L):.0f} · "
      f"media {st.mean(L):.1f} · MAXIMO {max(L)}")
print(f"  por encima de 120: {sum(1 for x in L if x > 120)}")
print(f"  reparto: {collections.Counter(min(x//10*10,120) for x in L).most_common()}")
print(f"  hueco entre partes: {set(S['huecos'])} tics (tick_rate {A42 and 24})")
print(f"  {dict(S['c'])}")

print("\n═══ b · habria llegado a tiempo ═══")
for nom, V in (("amenaza a ciegas (2d)", S["cobertura_2d"]),
               ("recurso que falta (2c)", S["cobertura_2c"])):
    if not V:
        print(f"  {nom}: sin casos"); continue
    print(f"  {nom}: {sum(V):,} de {len(V):,} tics = {100*sum(V)/len(V):.1f} %")

print("\n═══ c · la discrepancia de S-8-EXPOSICION ═══")
Z = S["s8_disc"]
if Z:
    d0 = [abs(x["disc"]) for x in Z]; d1 = [abs(x["disc_con"]) for x in Z]
    print(f"  {len(Z):,} decisiones con S-8 mal proyectada")
    print(f"    |disc| hoy          : mediana {st.median(d0):.5f} · media {st.mean(d0):.5f} · suma {sum(d0):.1f}")
    print(f"    |disc| con los ojos : mediana {st.median(d1):.5f} · media {st.mean(d1):.5f} · suma {sum(d1):.1f}")
    print(f"    baja en {100*(1-sum(d1)/sum(d0)):.1f} % (suma de |disc|)")
    mejor = sum(1 for x, y in zip(d0, d1) if y < x - 1e-9)
    peor = sum(1 for x, y in zip(d0, d1) if y > x + 1e-9)
    print(f"    mejora en {mejor:,} · empeora en {peor:,} · igual en {len(Z)-mejor-peor:,}")
    con = [x for x in Z if x["extra"] > 0]
    if con:
        c0 = [abs(x["disc"]) for x in con]; c1 = [abs(x["disc_con"]) for x in con]
        print(f"    solo donde hubo algun rival contado ({len(con):,}): "
              f"{st.median(c0):.5f} -> {st.median(c1):.5f} "
              f"(suma {sum(c0):.1f} -> {sum(c1):.1f}, "
              f"baja {100*(1-sum(c1)/sum(c0)):.1f} %)")
json.dump({k: (v if not isinstance(v, collections.Counter) else dict(v))
           for k, v in S.items()},
          open(os.path.join(AQUI, "P6_3_banco.json"), "w"))
print("\n-> cantera/paper6/P6_3_banco.json")

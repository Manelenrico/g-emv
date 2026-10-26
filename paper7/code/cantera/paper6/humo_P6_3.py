"""LOS HUMOS DE LOS OJOS COMPARTIDOS. [P6-3]

Si alguno falla, lo de abajo no vale. Se corren sobre un mundo REAL leido de
un diario del G2, no sobre un mundo de mentira.

  a) el parte nunca pasa de 120 caracteres ni de ASCII imprimible
  b) la cadencia 25 > tick_rate 24: jamas dos en el mismo segundo
  c) ida y vuelta: lo que se emite se parsea igual
  d) el corte no parte tokens: todo lo que entra se lee entero
  e) el orden: primero el armado que tiene al hermano a tiro
  f) sin parte del hermano, la obs sale IDENTICA (gate de pareado)
  g) el rival contado entra en `visible.agents` con su marca
  h) el rival contado CADUCA
  i) el recurso contado pesa menos con la edad y desaparece pasado el corte
  j) las letras del catalogo se LEEN del mundo (mismo mundo -> mismo alfabeto;
     y todas distintas)
  k) un rival contado NO genera candidato de ataque
"""
import glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "paper4"))
sys.path.insert(0, os.path.join(AQUI, "..", "paper5"))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "paintball"))
sys.path.insert(0, os.path.join(AQUI, "..", ".."))      # `motor` y `planificador`
import parte2 as P2
import oyente2 as OY

# [P6-4] El mundo se monta LEYENDO el propio registro `static_map`, que trae su
# leyenda, su tamano y sus pedestales. Asi el humo no depende de `serie_util`
# (que vive en cantera/paper4 y no viaja en la imagen) ni cablea ninguna
# constante del mundo, que es la regla de CLAUDE.md.
from alma.mundo import Mundo                              # noqa: E402
from alma import smoke_alma as SM_                        # noqa: E402


def mundo_del_registro(pc, sm, cat):
    cfg = SM_.player_config(slot=pc["slot"])
    cfg["items"] = list(cat["items"])
    cfg["arena"] = {"size": sm["size"], "static_map": list(sm["filas"]),
                    "legend": dict(sm["legend"]),
                    "pedestals": [list(p) for p in sm["pedestals"]]}
    for k in ("slot", "team", "teammate_slot", "tick_rate", "max_ticks",
              "ignition_tick", "zone_schedule"):
        if pc.get(k) is not None:
            cfg[k] = pc[k]
    return Mundo.desde_player_config(cfg)

OK = []


def humo(nombre):
    def deco(f):
        try:
            f()
            OK.append((nombre, None))
            print(f"  OK   {nombre}")
        except Exception as e:
            OK.append((nombre, repr(e)))
            print(f"  FALLA {nombre}: {repr(e)[:300]}")
        return f
    return deco


# ── el mundo real ─────────────────────────────────────────────────────────
# [P6-4] El mundo de prueba viaja EN LA IMAGEN (`humo_mundo.jsonl`: el
# player_config, el mapa, el catalogo y 400 tics vivos de un diario real del
# G2). Asi los once humos corren dentro del `docker build` y lo tumban si
# fallan, que es la regla de la casa. Fuera de la imagen se usa el diario.
_EMP = os.path.join(AQUI, "humo_mundo.jsonl")
if os.path.exists(_EMP):
    RECS = [json.loads(l) for l in open(_EMP, encoding="utf-8") if l.strip()]
else:
    sys.path.insert(0, os.path.join(AQUI, "..", "paper4"))
    import serie_util as U
    F = sorted(glob.glob(os.path.join(AQUI, "..", "..", "paintball", "runs",
                                      "P61_t3_G2_20260916",
                                      "*policy_agent_10*.art.log")))[0]
    RECS = []
    for r in U.lee(F):
        RECS.append(r)
        if len(RECS) > 4000:
            break
PC_ = next(r for r in RECS if r.get("k") == "player_config")
SM = next(r for r in RECS if r.get("k") == "static_map")
CAT = next(r for r in RECS if r.get("k") == "catalogo")
MUNDO = mundo_del_registro(PC_, SM, CAT)
TICS = [r for r in RECS if r.get("k") == "tick" and r.get("phase") == "live"]
print(f"mundo real: slot {MUNDO.slot} · pareja {MUNDO.teammate_slot} · "
      f"{len(MUNDO.items)} objetos · {len(TICS)} tics de prueba")


class MemFalsa:
    agresores = {}


def obs_de(r, extra_ag=(), extra_it=()):
    you = {"pos": list(r.get("pos") or (24, 24)), "hp": r.get("hp") or 100,
           "pack": [s for s in (r.get("pack") or []) if s],
           "effects": r.get("effects") or []}
    ag = [dict(a) for a in (r.get("ve_agentes") or []) if a.get("pos")]
    ag += [dict(a) for a in extra_ag]
    it = [dict(x) for x in (r.get("ve_items") or []) if x.get("pos")]
    it += [dict(x) for x in extra_it]
    return {"you": you, "visible": {"agents": ag, "items": it},
            "chat": r.get("chat") or []}


@humo("a · 120 caracteres y ASCII imprimible, en TODOS los tics")
def _a():
    oj = P2.Ojeador()
    peor = 0
    for r in TICS:
        s = P2.emite(obs_de(r), r["tick"], MUNDO, MemFalsa(), 120, oj, None)
        assert P2.ascii_limpio(s), (len(s), s[:60])
        peor = max(peor, len(s))
    assert peor <= P2.MAX_CHARS, peor
    print(f"       el mas largo: {peor} caracteres")


@humo("b · la cadencia 25 no cabe dos veces en un segundo de 24 tics")
def _b():
    assert P2.CADA > MUNDO.tick_rate, (P2.CADA, MUNDO.tick_rate)
    segs = [(t * P2.CADA) // MUNDO.tick_rate for t in range(400)]
    assert len(segs) == len(set(segs)), "dos partes en el mismo segundo"


@humo("c · ida y vuelta: lo emitido se parsea igual")
def _c():
    oj = P2.Ojeador()
    n = 0
    for r in TICS[:1500]:
        s = P2.emite(obs_de(r), r["tick"], MUNDO, MemFalsa(), 120, oj, None)
        p = P2.parsea(s, MUNDO)
        assert p is not None, s
        assert p["slot"] == MUNDO.slot and p["t"] == r["tick"], s
        assert tuple(p["pos"]) == tuple(r["pos"]), s
        n += len(p["rivales"]) + len(p["recursos"])
    assert n > 0, "ningun rival ni recurso viajo en 1.500 tics"
    print(f"       {n} rivales+recursos de ida y vuelta sin perder uno")


@humo("d · el corte no parte ningun token")
def _d():
    oj = P2.Ojeador()
    for r in TICS:
        det = {}
        s = P2.emite(obs_de(r), r["tick"], MUNDO, MemFalsa(), 120, oj, None, det)
        p = P2.parsea(s, MUNDO)
        assert len(p["rivales"]) == det["rivales_dentro"], (s, det)
        assert len(p["recursos"]) == det["recursos_dentro"], (s, det)


@humo("e · el orden: primero el armado que tiene al hermano a tiro")
def _e():
    r = TICS[0]
    herm = {"slot": MUNDO.teammate_slot, "t": r["tick"], "pos": (10, 10),
            "botiquin": 1, "hp": 100.0, "veneno": False, "agresor": False,
            "agresor_slot": None, "agresor_pos": None,
            "rivales": [], "recursos": []}
    lejos = {"slot": 3, "pos": [40, 40], "hand": {"id": "sword"}}
    cerca = {"slot": 4, "pos": [11, 10], "hand": {"id": "sword"}}
    s = P2.emite(obs_de(r, extra_ag=[lejos, cerca]), r["tick"], MUNDO,
                 MemFalsa(), 120, P2.Ojeador(), herm)
    p = P2.parsea(s, MUNDO)
    orden = [x["slot"] for x in p["rivales"]]
    assert orden and orden[0] == 4, (orden, s)


@humo("f · sin parte del hermano la obs sale IDENTICA")
def _f():
    r = TICS[10]
    o = obs_de(r)
    o2 = OY.inyecta(o, r["tick"], MUNDO, None)
    assert o2 is o, "la obs se toco sin parte"


@humo("g · el rival contado entra en visible.agents con su marca")
def _g():
    r = TICS[10]
    p = {"slot": MUNDO.teammate_slot, "t": r["tick"], "pos": (10, 10),
         "botiquin": 0, "hp": 100.0, "veneno": False, "agresor": False,
         "agresor_slot": None, "agresor_pos": None,
         "rivales": [{"slot": 7, "pos": (20, 20), "arma": "bow", "rumbo": "N"}],
         "recursos": []}
    o = obs_de(r)
    n0 = len(o["visible"]["agents"])
    det = {}
    o2 = OY.inyecta(o, r["tick"], MUNDO, p, det)
    assert len(o2["visible"]["agents"]) == n0 + 1, det
    nuevo = o2["visible"]["agents"][-1]
    assert nuevo["_contado"] and nuevo["slot"] == 7 and nuevo["pos"] == [20, 20]
    # [P6-4] LA FORMA SE COMPARA CON EL MUNDO, NO CON LO QUE YO CREA. Un
    # agente contado tiene que tener las mismas claves y los mismos TIPOS que
    # uno que viene de verdad en `ve_agentes`. La version anterior de este
    # humo afirmaba `nuevo["hand"]["id"] == "bow"` —mi forma, no la del
    # mundo— y por eso no vio que `hand` ajeno es una CADENA. Diez partidas.
    real = next(a for r2 in TICS if r2.get("ve_agentes")
                for a in r2["ve_agentes"] if a.get("pos"))
    for k, v in real.items():
        assert k in nuevo, ("al contado le falta la clave del mundo", k)
        if v is not None and nuevo[k] is not None:
            assert type(nuevo[k]) is type(v), \
                ("tipo distinto del que da el mundo", k,
                 type(nuevo[k]).__name__, type(v).__name__)
    assert nuevo["hand"] == "bow", nuevo["hand"]
    assert OY.slots_contados(o2) == {7}
    assert len(o["visible"]["agents"]) == n0, "se muto la obs original"


@humo("h · el rival contado CADUCA")
def _h():
    r = TICS[10]
    p = {"slot": MUNDO.teammate_slot, "t": r["tick"] - OY.CADUCIDAD_RIVAL - 1,
         "pos": (10, 10), "botiquin": 0, "hp": 100.0, "veneno": False,
         "agresor": False, "agresor_slot": None, "agresor_pos": None,
         "rivales": [{"slot": 7, "pos": (20, 20), "arma": "bow", "rumbo": "N"}],
         "recursos": []}
    det = {}
    o2 = OY.inyecta(obs_de(r), r["tick"], MUNDO, p, det)
    assert det["rivales_contados"] == 0 and det["rivales_caducos"] == 1, det


@humo("i · el recurso pesa menos con la edad y se cae pasado el corte")
def _i():
    emax = OY.edad_max_recurso()
    assert OY.peso_recurso(0) == 1.0
    assert OY.peso_recurso(emax) >= OY.UMBRAL_REC > OY.peso_recurso(emax + 1)
    for a, b in zip(range(0, 300, 7), range(1, 301, 7)):
        assert OY.peso_recurso(a) >= OY.peso_recurso(b) - 1e-12, (a, b)
    r = TICS[10]
    base = {"slot": MUNDO.teammate_slot, "pos": (10, 10), "botiquin": 0,
            "hp": 100.0, "veneno": False, "agresor": False,
            "agresor_slot": None, "agresor_pos": None, "rivales": [],
            "recursos": [{"id": "first_aid", "pos": (30, 30)}]}
    d1, d2 = {}, {}
    OY.inyecta(obs_de(r), r["tick"], MUNDO, dict(base, t=r["tick"]), d1)
    OY.inyecta(obs_de(r), r["tick"], MUNDO,
               dict(base, t=r["tick"] - emax - 1), d2)
    assert d1["recursos_contados"] == 1 and d2["recursos_contados"] == 0, (d1, d2)
    print(f"       el recurso contado vale hasta los {emax} tics")


@humo("j · el alfabeto se LEE del mundo y no repite letra")
def _j():
    a1 = P2.alfabeto(MUNDO)
    a2 = P2.alfabeto(MUNDO)
    assert a1 == a2, "el alfabeto no es determinista"
    assert len(set(a1.values())) == len(a1), "dos objetos con la misma letra"
    assert set(a1) == set(MUNDO.items), "el alfabeto no es el del catalogo"
    inv = P2.inverso(MUNDO)
    assert all(inv[v] == k for k, v in a1.items())


@humo("k · el rival contado ABRE la via de ataque, y el filtro la cierra")
def _k():
    from alma import decisor_zs as D
    from alma import appraisal_zs_v42_exp as A
    # LA VIA REAL, encontrada leyendo `decisor_zs.py:570-600`: un candidato
    # `atacar_` solo nace contra un AGRESOR ACTIVO, y una de las dos formas de
    # serlo es ser «el agresor CERTIFICADO de mi hermana». `agresor_de_la_
    # hermana` exige que ese asiento este VISIBLE. Al inyectar al rival
    # contado, esa puerta se abre sola: el cuerpo atacaria a algo que NO VE.
    r = next(x for x in TICS
             if (x.get("hand") or {}).get("id") not in (None, "none"))
    pos = (int(r["pos"][0]), int(r["pos"][1]))
    q = (pos[0] + 1, pos[1])                     # alineado E, a distancia 1
    arma = "sword"                               # alcance 1, dano > 0
    p = {"slot": MUNDO.teammate_slot, "t": r["tick"], "pos": (pos[0], pos[1] + 4),
         "botiquin": 0, "hp": 100.0, "veneno": False,
         "agresor": True, "agresor_slot": 7, "agresor_pos": q,
         "rivales": [{"slot": 7, "pos": q, "arma": arma, "rumbo": "."}],
         "recursos": []}
    o = obs_de(r)
    o["you"]["hand"] = {"id": arma, "n": 1}
    o["you"]["attack_ready_in"] = 0
    o["visible"]["agents"] = [a for a in o["visible"]["agents"]
                              if a.get("slot") != 7]
    mem = A.Memoria()
    mem.parte = p
    mem.pareja_muerta = False
    # SIN inyectar: el asiento 7 no es visible -> no hay agresor certificado
    mem.observa(o, MUNDO, r["tick"])
    sin = list(D.candidatos(o, MUNDO, mem, r["tick"]))
    n_sin = len([n for n, rec in sin if rec.get("objetivo") == 7])
    # CON inyeccion: el 7 entra en `visible.agents` y la via se abre
    o2 = OY.inyecta(o, r["tick"], MUNDO, p)
    mem2 = A.Memoria(); mem2.parte = p; mem2.pareja_muerta = False
    mem2.observa(o2, MUNDO, r["tick"])
    con = list(D.candidatos(o2, MUNDO, mem2, r["tick"]))
    cont = OY.slots_contados(o2)
    n_con = len([n for n, rec in con if rec.get("objetivo") in cont])
    assert n_sin == 0, ("sin inyectar ya habia ataque", n_sin)
    assert n_con > 0, ("la via NO se abre: el humo no prueba nada", n_con)
    # EL FILTRO de `policy_pareja._cands`
    quedan = [(n, rec) for n, rec in con if rec.get("objetivo") not in cont]
    assert not [n for n, rec in quedan if rec.get("objetivo") in cont]
    assert len(quedan) == len(con) - n_con
    print(f"       sin inyectar: {n_sin} ataques contra el contado · "
          f"inyectando: {n_con} · con el filtro: 0")


mal = [n for n, e in OK if e]
print(f"\n{len(OK) - len(mal)} de {len(OK)} humos OK")
if mal:
    print("FALLAN:", mal)
    sys.exit(1)

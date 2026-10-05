"""[P6-11 · 2] EL BANCO: replay de las 40 vidas de A3 con y sin la amenaza menor.

Replay tic a tic por la via real de A3 (ojos, gemelo E1, Memoria.observa,
D.candidatos, D.decide con Bloqueos, D.A = v42, entorno de la imagen, oido,
don, arreglos P6-8b, S-COMPANIA techo 0,32), dos veces: SIN y CON
`amenaza11_P6_11`. Se cuenta:
  · decisiones que cambian (elegido distinto), con piernas listas, sobre todas
  · en los golpes de rival con la mano vacia (`damage_taken` de un P<slot> que
    en ese tic esta a la vista con `hand: none`): en los 24 tics anteriores,
    ¿estaba encendida alguna fila de miedo por ESE rival? Se mira, con y sin:
    F-HERMANO-AMENAZA/GOLPE y F-REENCUENTRO (las que miran el arma) y F-4/S-8
    (que no la miran). "Encendida antes" = M > 0 en la tabla del tic (`ahora`).
Es un contrafactual decision a decision sobre las observaciones REALES (el
estado que llega en cada tic es el grabado): dice que decidiria el cuerpo en
las mismas fotos, no como iria la partida.
"""
import collections, glob, json, os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (AQUI, os.path.join(RAIZ, "cantera", "paper4"), os.path.join(RAIZ, "cantera", "paper5"), os.path.join(RAIZ, "paintball"), RAIZ):
    sys.path.insert(0, p)
os.environ.setdefault("GEMV_COMPANIA_TECHO", "0.32")
for _k, _v in (("GEMV_MIEDO", "0"), ("GEMV_VIDA_AJENA", "0"), ("GEMV_VIDA_AJENA_M", "0.25"),
               ("GEMV_MEMORIA", os.path.join(RAIZ, "paintball", "alma", "memoria_aprendida_p95.json")),
               ("GEMV_CORTEX", "0"), ("GEMV_FORMA", "0"), ("GEMV_CURIOSIDAD", "")):
    os.environ.setdefault(_k, _v)
import serie_util as U
import parte2 as P2, oyente2 as OY, oido5_P6_5 as O5
import arreglos_P6_6 as R6, arreglos_P6_8b as R8, filas10_P6_10 as F10, amenaza11_P6_11 as M11
from alma import appraisal_zs_v42_exp as A
from alma import decisor_zs as D
# EL CABLEADO DEL CUERPO, como lo fija `policy_cortex.py:93-96` EN CODIGO (no por
# entorno): empatia encendida con sus diales, miedo y extrano apagados, y el
# decisor valorando con la v42. Sin esto el replay no es el cuerpo que jugo:
# F-HERMANO-AMENAZA/GOLPE y R-HERMANO-FALTA quedan apagadas.
A.EMPATIA_ON = True
A.H_PREV, A.H_GOLPE = 0.25, 1.0
A.MIEDO_ON = False
A.VIDA_AJENA_ON = False
D.A = A
_D0 = (D.decide, D.candidatos, A.appraise)
VENT = 24
FILAS_ARMA = ("F-HERMANO-AMENAZA", "F-HERMANO-GOLPE", "F-REENCUENTRO")
FILAS_SIN = ("F-4-ALCANCE", "S-8-EXPOSICION", "S-7-AGRESOR")


class Boba:
    def decidir(self, obs):
        return None


def carga(f):
    recs, tics, sp, it = [], [], 5, 5
    for r in U.lee(f):
        k = r.get("k")
        if k in ("player_config", "static_map", "catalogo"):
            recs.append(r)
        elif k == "arranque":
            s = json.dumps(r); m = re.search(r'"speed"\s*:\s*(\d+)', s); sp = int(m.group(1)) if m else 5
            m = re.search(r'"intelligence"\s*:\s*(\d+)', s); it = int(m.group(1)) if m else 5
        elif k == "tick" and r.get("phase") == "live":
            tics.append(r)
    pc = next(r for r in recs if r["k"] == "player_config"); sm = next(r for r in recs if r["k"] == "static_map"); cat = next(r for r in recs if r["k"] == "catalogo")
    return U.mundo_de(pc, list(sm["filas"]), cat["items"]), tics, sp, it


def obs_de(r, sp, it):
    you = {"pos": list(r["pos"]), "hp": r.get("hp") or 100, "pack": list(r.get("pack") or []), "hand": r.get("hand"),
           "body": r.get("body"), "effects": r.get("effects") or [], "stats": {"speed": sp, "intelligence": it},
           "attack_ready_in": r.get("attack_ready_in"), "move_ready_in": r.get("move_ready_in_obs", r.get("move_ready_in")),
           "action_result": r.get("action_result_obs", r.get("action_result")),
           "damage_taken": (r.get("damage_taken") if isinstance(r.get("damage_taken"), list) else []), "damage_dealt": (r.get("damage_dealt") if isinstance(r.get("damage_dealt"), list) else []), "kills": r.get("kills")}
    return {"you": you, "visible": {"agents": [dict(a) for a in (r.get("ve_agentes") or []) if a.get("pos")],
                                    "items": [dict(x) for x in (r.get("ve_items") or []) if x.get("pos")],
                                    "bushes": list(r.get("ve_bushes") or []), "projectiles": list(r.get("ve_proyectiles") or [])},
            "zone": dict(r.get("zona") or {}), "events": list(r.get("eventos") or []), "chat": list(r.get("chat") or [])}


def replay(mundo, tics, sp, it, con_manos, guarda):
    """guarda(tick, r, elegido, filas_ahora, listas). Devuelve nada."""
    D.decide, D.candidatos, A.appraise = _D0
    R6.aplica(Boba); R8.aplica(); F10.aplica()
    if con_manos:
        M11.aplica()
    mem = A.Memoria(); mem.hp_max = float(tics[0].get("hp") or 100)
    bl = D.Bloqueos(); ult = None; parte_herm = None; herm = mundo.teammate_slot
    for r in tics:
        o = obs_de(r, sp, it)
        for m in (o.get("chat") or []):
            if m.get("channel") == "team" and m.get("from") == herm:
                pp = P2.parsea(m.get("text") or "", mundo)
                if pp is not None:
                    parte_herm = pp
        fresco = parte_herm if (parte_herm and 0 <= r["tick"] - parte_herm["t"] <= P2.CADUCIDAD) else None
        o = OY.inyecta(o, r["tick"], mundo, fresco, {}); o, _ = O5.gemelo(o, herm)
        bl.actualiza(o, mundo, ult, r["tick"]); mem.observa(o, mundo, r["tick"])
        ac, ra = D.decide(o, mundo, mem, r["tick"], bl); ult = ac
        # la tabla del tic (mi casilla): las filas del candidato noop si hay detalle,
        # y si no, la radiografia `ahora` no existe en el replay -> se recalcula
        fl = ((ra.get("candidatos") or {}).get("noop") or {}).get("filas") if isinstance((ra.get("candidatos") or {}).get("noop"), dict) else None
        if fl is None:
            # la tabla se recalcula sobre la MISMA obs que ve el decisor: con la
            # amenaza menor, la reescrita (si no, las filas del hermano no ven la mano)
            o_r = M11.reescribe(o, mundo, mem, r["tick"])[0] if con_manos else o
            _st, radio = A.appraise(o_r, mundo, mem, r["tick"])
            fl = {k: v.get("M", 0.0) for k, v in (radio.get("filas") or {}).items() if v.get("M")}
        guarda(r["tick"], r, ra.get("elegido"), fl, int(o["you"].get("move_ready_in") or 0) == 0)
    D.decide, D.candidatos, A.appraise = _D0


if __name__ == "__main__":
    S = collections.Counter(); GOL = []
    carps = []
    for p in sys.argv[1:]:
        carps += sorted(glob.glob(os.path.join(RAIZ, p)))
    for carp in carps:
        for f in sorted(glob.glob(os.path.join(carp, "*policy_agent_1*.art.log"))):
            mundo, tics, sp, it = carga(f)
            out = {}
            for con in (False, True):
                def g(t, r, el, fl, listas, con=con):
                    out.setdefault(t, {})[con] = (el, fl, listas, r)
                replay(mundo, tics, sp, it, con, g)
            S["vidas"] += 1
            for t in sorted(out):
                a, b = out[t].get(False), out[t].get(True)
                if not a or not b:
                    continue
                S["tics"] += 1
                if a[2]:
                    S["tics con piernas listas"] += 1
                    if a[0] != b[0]:
                        S["  ...decision cambia"] += 1
                        S[f"    {a[0].split('_')[0] if a[0] else a[0]} -> {b[0].split('_')[0] if b[0] else b[0]}"] += 1
                r = a[3]; ve = {x.get("slot"): x for x in (r.get("ve_agentes") or [])}
                for gd in (r.get("damage_taken") or []):
                    s = str(gd.get("source"))
                    if not s.startswith("P"):
                        continue
                    ag = ve.get(int(s[1:]))
                    if ag is None or (ag.get("hand") or "none") != "none":
                        continue
                    S["golpes de rival sin arma (visible)"] += 1
                    fila = {"carp": os.path.basename(carp), "tick": t, "slot": int(s[1:])}
                    for con, key in ((False, "sin"), (True, "con")):
                        prev = [out[tt][con][1] for tt in range(t - VENT, t) if tt in out and con in out[tt]]
                        fila[key + "_arma"] = any(any(fl.get(k) for k in FILAS_ARMA) for fl in prev)
                        fila[key + "_cualquiera"] = any(any(fl.get(k) for k in FILAS_ARMA + FILAS_SIN) for fl in prev)
                    S["  ...filas que miran el arma encendidas antes, SIN"] += fila["sin_arma"]
                    S["  ...filas que miran el arma encendidas antes, CON"] += fila["con_arma"]
                    S["  ...cualquier fila de miedo encendida antes, SIN"] += fila["sin_cualquiera"]
                    S["  ...cualquier fila de miedo encendida antes, CON"] += fila["con_cualquiera"]
                    GOL.append(fila)
            del out, tics
            print(f"    {os.path.basename(carp)} {os.path.basename(f)[-22:]} · {dict((k, v) for k, v in S.items() if 'cambia' in k or 'golpes' in k)}", flush=True)
    print("### A3, replay con y sin amenaza menor")
    for k, v in S.items():
        print(f"  {k:60s} {v}")
    json.dump({"recuento": dict(S), "golpes": GOL}, open(os.path.join(AQUI, "P6_11_banco.json"), "w"), ensure_ascii=False, indent=1)
    print("-> cantera/paper6/P6_11_banco.json")

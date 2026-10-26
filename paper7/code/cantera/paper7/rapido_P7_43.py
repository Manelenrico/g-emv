"""[P7-43] DOS PIEZAS TRAS LA PARADA DE LA GUARDA (decisiones de la mesa), enganchadas por fuera de todas las del siete:
  1. CACHES, con decisiones IDENTICAS (GEMV_P7_43_CACHE=1): (a) el regalo que mira lo aprendido (`descubre_P7.regalo_aprendido` = `nace_P7_23.regalo_nace`) tasa cada foto
     dos veces (con y sin los consumibles a la vista); la segunda tasacion se guarda por tic y por CLAVE DE LA FOTO (posicion, vida, zurron, mano, cuerpo, marcas `_*` de la
     foto, vida prevista de los agentes a la vista, objetos a la vista): dos fotos con la misma clave dan la misma F_sin. (b) En `filo_P7_40`, la ignorancia del cuaderno y la
     curiosidad por clase se guardan por tic (la obs real es la misma todo el tic): ver filo_P7_40.ign_cache. Ninguna regla cambia.
  2. REGLA DEL CUERPO DE LOS 3 SEGUNDOS (GEMV_P7_43_MURO=1, igual en todos los brazos): si la criatura intenta entrar en una casilla y no se mueve durante 3 s seguidos
     (una racha de empujes bloqueados hacia la misma casilla, sin cambiar de posicion, que dura 72 tics de reloj; los tics de enfriamiento de las piernas entre
     empujes no la rompen), esa casilla queda como no transitable el resto de esa vida (`mundo.solido`, como la ley del agua de P7-33; se vacia la cache de caminos al
     marcar; y los candidatos `ir_*` con destino en una casilla no transitable —marcada o cerrada por la ley del agua— salen de la lista: no transitable = ni pisarla
     ni ir a ella); se olvida al morir, no viaja en el cuaderno.
     Registro `P7_43_muro`. [P7-43d, v3: la marca dura 30 s (720 tics), no toda la vida: los rivales camuflados pueden parar 3 s en una casilla libre y marcarla
     para siempre podria cerrar pasillos; si vuelve a bloquear 72 tics, se renueva; se olvida al morir.] [11-oct, 10:30: la primera version contaba solo tics consecutivos bloqueados y el enfriamiento la rompia (TECHO s1 d5 a10 empujo 231 veces en
     1.400 tics sin marcar); y no quitaba el `ir_objeto` hacia la casilla marcada (411 empujes mas despues de marcarla).]
     Por que se quito la red de muros en P7-29b: aprendia muros para siempre en casillas de suelo donde en realidad habia agua temporal (13 "muros" en A4, F1 de TECHO
     fallaba); esta regla es por vida, exige 3 s de empuje real y el agua ya la cubre el oido-y-ley."""
import os
import descubre_P7 as X, nace_P7_23 as N, nace_P7_33 as N33
from alma import decisor_zs as D
CACHE = os.environ.get("GEMV_P7_43_CACHE", "0") == "1"; MURO = os.environ.get("GEMV_P7_43_MURO", "0") == "1"; TRES_S = 72; DURA = 720     # [P7-43d, v3] la marca dura 30 s (720 tics); se renueva si vuelve a bloquear 72 tics; se olvida al morir
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}
E = {"registra": None, "memo_tick": None, "memo": {}, "aciertos": 0, "fallos": 0, "muros": {}, "racha": None, "patch": False, "marcados": [], "caducadas": 0}


def clave_foto(ob2):
    you = ob2.get("you") or {}; vis = ob2.get("visible") or {}
    return (tuple(you.get("pos") or ()), you.get("hp"), tuple((s.get("id"), s.get("n")) if s else None for s in (you.get("pack") or [])), str(you.get("hand")), str(you.get("body")),
            tuple(sorted((k, str(v)) for k, v in you.items() if k.startswith("_"))), tuple((a.get("slot"), a.get("hp"), a.get("hp_band"), tuple(a.get("pos") or ()), tuple(sorted((k, str(v)) for k, v in a.items() if k.startswith("_")))) for a in (vis.get("agents") or [])), tuple((it.get("id"), tuple(it.get("pos") or ())) for it in (vis.get("items") or [])))


def aplica(clase, registra=None):
    E["registra"] = registra; hecho = {"cache": CACHE, "muro": MURO}
    if CACHE:
        _reg = X.regalo_aprendido
        def regalo_memo(obs, mundo, mem, tick, F, filas0):
            if E["memo_tick"] != tick: E["memo"] = {}; E["memo_tick"] = tick
            def filas_memo(ob2, mundo_, mem_, tick_):
                k = clave_foto(ob2); v = E["memo"].get(k)
                if v is None: v = filas0(ob2, mundo_, mem_, tick_); E["memo"][k] = v; E["fallos"] += 1
                else: E["aciertos"] += 1
                return v
            return _reg(obs, mundo, mem, tick, F, filas_memo)
        X.regalo_aprendido = regalo_memo
    if MURO:
        # (a) ir hacia una casilla marcada es ir a ninguna parte: los candidatos `ir_*` con destino en un muro salen de la lista (no transitable = ni pisarla ni ir a ella)
        _oc = D.candidatos
        def _cands(obs, mundo, mem, tick, bloqueos=None):
            out = _oc(obs, mundo, mem, tick, bloqueos)
            # [v3b] ir a una casilla NO TRANSITABLE (marcada, o cerrada por la ley del agua de P7-33) es ir a ninguna parte: sin campo geodesico el cuerpo caminaba en
            # linea recta hacia un objeto en el agua y empujaba contra lo que hubiera en medio (TECHO s1 d5 a10: 411 empujes hacia (20,22) yendo a una mochila en (13,24) inundada)
            return [(n_, r_) for n_, r_ in out if not (isinstance(r_, dict) and r_.get("tipo") == "ir" and r_.get("destino") and mundo.solido(int(r_["destino"][0]), int(r_["destino"][1])))]
        D.candidatos = _cands
        _od = clase.decidir
        def decidir(self, obs, _d=_od):
            mundo = self.mundo
            if mundo is not None and getattr(self, "phase", None) == "live":
                if not E["patch"]:
                    _s0 = mundo.solido; mundo.solido = lambda x, y, _s0=_s0: ((int(x), int(y)) in E["muros"]) or _s0(x, y); E["patch"] = True
                vencidas = [c for c, hasta in E["muros"].items() if self.tick >= hasta]      # [v3] las marcas caducan a los 30 s: se quitan y se vacia la cache de caminos
                if vencidas:
                    for c in vencidas: del E["muros"][c]
                    mundo._campos_geo = {}; E["caducadas"] += len(vencidas)
                you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); prev = E.get("prev"); r = E["racha"]
                ar = you.get("action_result") or obs.get("action_result")       # (la plataforma lo da dentro de `you`; el banco lo reconstruye igual)
                # (b) la racha: empieza con un empuje bloqueado hacia una casilla; sigue mientras la posicion no cambie y los empujes (ignorando los tics de enfriamiento
                #     de las piernas) vayan a la misma casilla; se rompe si se mueve, si empuja a otra casilla o si un movimiento sale bien. 72 tics de reloj sin moverse -> muro.
                if r and r["pos"] != pos: E["racha"] = r = None
                if prev and ar == "blocked" and prev["pos"] == pos and prev["dir"] in DIRS:
                    dx, dy = DIRS[prev["dir"]]; hacia = (pos[0] + dx, pos[1] + dy)
                    if r and r["hacia"] == hacia: r["n"] += 1
                    else: E["racha"] = r = {"hacia": hacia, "pos": pos, "n": 1, "t0": self.tick}
                elif prev and ar == "ok" and prev["dir"] in DIRS: E["racha"] = r = None
                if r and self.tick - r["t0"] >= TRES_S and r["hacia"] not in E["muros"]:
                    E["muros"][r["hacia"]] = self.tick + DURA; mundo._campos_geo = {}; E["marcados"].append({"tick": self.tick, "casilla": list(r["hacia"]), "desde": list(pos), "t0": r["t0"], "empujes": r["n"], "hasta": self.tick + DURA})
                    if registra: registra({"k": "P7_43_muro", "tick": self.tick, "casilla": list(r["hacia"]), "desde": list(pos), "t0": r["t0"], "empujes": r["n"], "hasta": self.tick + DURA, "muros": len(E["muros"])})
                    E["racha"] = None
            accion, radio = _d(self, obs)
            it = accion if isinstance(accion, dict) else {}
            E["prev"] = {"pos": tuple((obs.get("you") or {}).get("pos") or (0, 0)), "dir": (it.get("dir") if it.get("do") == "move" else None)}
            return accion, radio
        clase.decidir = decidir
    return hecho


def estado(): return {"aciertos": E["aciertos"], "fallos": E["fallos"], "muros": sorted(E["muros"]), "marcados": E["marcados"], "caducadas": E["caducadas"]}

"""Jugadores de prueba del valle. No saben nada de emociones: solo leen la observación (y el mapa estático que el mundo da a todas al empezar).
  Aleatorio: elige al azar entre las acciones válidas que el mundo pone en infos.
  Tonto: come si tiene hambre; si no lleva comida, va al almacén y coge; si el almacén está bajo, trabaja en el huerto o busca en el bosque;
         al anochecer vuelve a su casa y duerme; huye a casa si ve la bestia. Ni da, ni empuja, ni golpea, ni llama, ni habla."""
import random
from collections import deque

DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}
PASO = {(0, -1): "N", (0, 1): "S", (1, 0): "E", (-1, 0): "O"}


class Aleatorio:
    def __init__(self, agente, semilla):
        self.r = random.Random(f"{semilla}-{agente}")

    def actua(self, obs, info):
        v = info.get("acciones_validas") or [{"accion": "quedarse"}]
        return v[self.r.randrange(len(v))]


class Mapa:
    """el mapa estático (el mismo para todas) y caminos más cortos sin contar a nadie (si una casilla está ocupada, el paso falla y se reintenta)"""
    def __init__(self, mp):
        self.T = mp["terreno"]; self.W, self.H = mp["ancho"], mp["alto"]
        self.casa = {}; self.puerta = {}
        for k, v in mp["casas"].items():
            for c in v["celdas"]: self.casa[tuple(c)] = k
            self.puerta[k] = tuple(v["puerta"])
        self.almacen = [tuple(c) for c in mp["almacen"]]; self.acceso_almacen = [tuple(c) for c in mp["almacen_acceso"]]; self.plantas = [tuple(p) for p in mp["plantas"]]
        self.bosque = [(x, y) for y in range(len(self.T)) for x in range(len(self.T[0])) if self.T[y][x] == "b"]
        self.salvaje = [(x, y) for y in range(len(self.T)) for x in range(len(self.T[0])) if self.T[y][x] == "s"]
        self.matorrales = [(m[0], m[1]) for m in (mp.get("matorrales") or [])]
        self._dist = {}

    def pasa(self, a, b):
        x, y = b
        if not (0 <= x < len(self.T[0]) and 0 <= y < len(self.T)) or self.T[y][x] in ("m", "p", "x"): return False
        ca, cb = self.casa.get(a), self.casa.get(b)
        if ca != cb:
            if cb is not None and b != self.puerta[cb]: return False
            if ca is not None and a != self.puerta[ca]: return False
        return True

    def distancias(self, metas):
        """mapa de distancias a un conjunto de metas (cacheado): para bajar por él"""
        k = tuple(sorted(metas))
        if k in self._dist: return self._dist[k]
        D = {m: 0 for m in metas}; q = deque(metas)
        while q:
            u = q.popleft()
            for d in DIRS.values():
                v = (u[0] + d[0], u[1] + d[1])
                if v not in D and self.pasa(v, u): D[v] = D[u] + 1; q.append(v)
        self._dist[k] = D; return D

    def paso_hacia(self, pos, metas, ocupadas=(), r=None):
        """el paso que más acerca; si está tapado por alguien, uno de lado (igual de lejos), sorteado"""
        D = self.distancias(metas); aqui = D.get(pos, 10 ** 9); ops = []
        for nombre, d in DIRS.items():
            v = (pos[0] + d[0], pos[1] + d[1])
            if v in D and self.pasa(pos, v) and v not in ocupadas and D[v] <= aqui: ops.append((D[v], nombre))
        if not ops: return None
        m = min(x for x, _ in ops); mejores = [n for x, n in ops if x == m]
        if m == aqui and r is not None and r.random() < 0.5: return None                  # de lado, solo a veces (para no bailar)
        return mejores[0] if r is None else mejores[r.randrange(len(mejores))]


class Tonto:
    HAMBRE = 40           # come si el hambre pasa de aquí (reglas del jugador, no del mundo)
    SOBRA = 2             # (v2) más de esto en la bolsa, se deja en el almacén

    def __init__(self, agente, semilla, mapa, trabajo_necesario=20):
        self.trabajo_necesario = trabajo_necesario; self.a = agente; self.r = random.Random(f"{semilla}-{agente}"); self.M = mapa; self.casa = agente[0]
        self.oficio = "huerto" if int(agente[1:]) % 2 == 1 else "bosque"            # las dos hermanas se reparten: una al huerto, otra al bosque
        self.meta_bosque = None
        self.busca_en = ("bosque",); self.celdas_busca = self.M.bosque         # dónde busca comida cuando el almacén está bajo

    def _a_casa(self, pos, ocup, dentro_hace="dormir"):
        dentro = [c for c, k in self.M.casa.items() if k == self.casa and c != self.M.puerta[self.casa]]
        if pos in dentro: return {"accion": dentro_hace}
        d = self.M.paso_hacia(pos, dentro, ocup, self.r)
        if d: return {"accion": "mover", "dir": d}
        self._quiere_ir = True; return {"accion": "quedarse"}

    def actua(self, obs, info):
        acc = self._decide(obs)
        pos = tuple(obs["yo"]["pos"])
        # atasco: si quiere moverse y lleva 3 turnos en la misma casilla, un paso al azar entre los válidos
        if acc.get("accion") == "mover" or (acc.get("accion") == "quedarse" and getattr(self, "_quiere_ir", False)):
            self._parada = self._parada + 1 if pos == getattr(self, "_pos_ant", None) else 0
            if self._parada >= 3:
                movs = [v for v in (info.get("acciones_validas") or []) if v["accion"] == "mover"]
                if movs: self._parada = 0; acc = movs[self.r.randrange(len(movs))]
        else: self._parada = 0
        self._pos_ant = pos
        return acc

    def _decide(self, obs):
        yo = obs["yo"]; pos = tuple(yo["pos"]); bolsa = obs["bolsa"]; fase = obs["fase"]
        if obs["almacen"] is not None: self.almacen_visto = obs["almacen"]          # lo que vio la última vez que estuvo en la aldea
        nivel = getattr(self, "almacen_visto", None)
        ocup = {tuple(c["pos"]) for c in obs["criaturas"]}
        if obs["bestia"]: ocup.add(tuple(obs["bestia"]["pos"]))
        cerca = lambda q: max(abs(pos[0] - q[0]), abs(pos[1] - q[1])) <= 1
        self._quiere_ir = False
        def ir(metas):
            d = self.M.paso_hacia(pos, metas, ocup, self.r)
            if d: return {"accion": "mover", "dir": d}
            self._quiere_ir = True; return {"accion": "quedarse"}
        # 1. agotada: dormir
        self._quiere_ir = False
        if yo["agotada"]: return {"accion": "dormir"}
        # 2. ve la bestia, o anochece: a casa y a dormir
        if obs["bestia"] or fase in ("anochecer", "noche"): return self._a_casa(pos, ocup)
        self._quiere_ir = False
        # 3. come si tiene hambre
        if yo["hambre"] > self.HAMBRE and "comida" in bolsa: return {"accion": "comer", "tipo": "comida"}
        junto = self.M.acceso_almacen; n_comida = bolsa.count("comida")
        # 3b. (v2) con comida de sobra (más de 2): la deja en el almacén al pasar; la del huerto lleva la cosecha al almacén
        if n_comida > self.SOBRA:
            if pos in junto: return {"accion": "dejar", "en": "almacen", "tipo": "comida"}
            if self.oficio == "huerto": return ir(junto)
        # 4. sin comida: al almacén a coger (si no lo ha visto vacío)
        if "comida" not in bolsa and nivel != "vacio":
            if pos in junto: return {"accion": "coger", "de": "almacen", "tipo": "comida"}
            return ir(junto)
        # 5. almacén bajo (poco o vacío): trabaja en el huerto o busca en el bosque (y coge lo que encuentra)
        if nivel in ("poco", "vacio"):
            aqui = next((c for c in obs["casillas"] if tuple(c["pos"]) == pos), {})
            if aqui.get("objetos") and len(bolsa) < 6: return {"accion": "coger", "de": "suelo", "tipo": aqui["objetos"][0]}
            if len(bolsa) < 6 and any(c.get("planta", {}).get("frutos") and cerca(tuple(c["pos"])) for c in obs["casillas"]): return {"accion": "coger", "de": "planta", "tipo": "comida"}
            if self.oficio == "huerto":                  # a las plantas que aún no tienen el trabajo del ciclo (lo que se ve de cada planta)
                vistas = {tuple(c["pos"]): c["planta"].get("trabajo", 0) for c in obs["casillas"] if c.get("planta") is not None}
                faltan = [q for q in self.M.plantas if vistas.get(q, 0) < self.trabajo_necesario]
                junto = [q for q in faltan if cerca(q)]
                if junto: return {"accion": "trabajar", "planta": list(min(junto, key=lambda q: (vistas.get(q, 0), q)))}
                return ir(faltan or self.M.plantas)
            vista = [tuple(c["pos"]) for c in obs["casillas"] if c["terreno"] in self.busca_en and "comida" in (c.get("objetos") or [])]
            if vista: return ir(vista)
            if self.meta_bosque is None or pos == self.meta_bosque: self.meta_bosque = self.celdas_busca[self.r.randrange(len(self.celdas_busca))]
            return ir([self.meta_bosque])
        # 6. (v3) nada más que hacer: vuelve a su casa y se queda dentro
        return self._a_casa(pos, ocup, dentro_hace="quedarse")


class Recolector(Tonto):
    """(prompt 19, Manel) un jugador hecho a mano que conoce dónde están los matorrales (el mapa público los da). Nunca trabaja el huerto.
    De día: si tiene hambre y lleva comida, come; (prompt 20) si ve comida suelta en el suelo, va a cogerla; si lleva mucha (4 o más), la lleva al almacén y deja hasta quedarse con 2; si tiene hambre y no lleva,
    coge del almacén (si no lo ha visto vacío); si no, va al matorral (o planta) más cercano con fruto visto, o al que no ha mirado hace más de
    REVISA turnos, y coge. Al anochecer, o si ve la bestia, a casa y a dormir. Sin nada que hacer, en casa."""
    REVISA = 200            # [regla del jugador] volver a mirar un matorral visto sin fruto pasados estos turnos
    LLENA = 4               # [regla del jugador] con tantas comidas o más, al almacén

    def __init__(self, agente, semilla, mapa, trabajo_necesario=20):
        super().__init__(agente, semilla, mapa, trabajo_necesario)
        self.oficio = "recoger"; self.fuentes = sorted(set(self.M.matorrales) | set(self.M.plantas)); self.visto = {}; self.dejando = False

    def _decide(self, obs):
        yo = obs["yo"]; pos = tuple(yo["pos"]); bolsa = obs["bolsa"]; fase = obs["fase"]; t = obs["turno"]
        if len(self.M._dist) > 300: self.M._dist.clear()                     # los caminos se guardan por conjunto de metas: que la caché no crezca sin fin
        if obs["almacen"] is not None: self.almacen_visto = obs["almacen"]
        for c in obs["casillas"]:
            q = tuple(c["pos"])
            if c.get("matorral") is not None:
                self.visto[q] = (t, c["matorral"]["frutos"])
                if c["matorral"].get("zona") == "arbol" and q not in self.fuentes: self.fuentes = sorted(set(self.fuentes) | {q})      # (prompt 97, Manel) el árbol dulce que ve: una fuente más
            elif c.get("planta") is not None: self.visto[q] = (t, c["planta"]["frutos"])
        ocup = {tuple(c["pos"]) for c in obs["criaturas"]}
        if obs["bestia"]: ocup.add(tuple(obs["bestia"]["pos"]))
        cerca = lambda q: max(abs(pos[0] - q[0]), abs(pos[1] - q[1])) <= 1
        self._quiere_ir = False
        def ir(metas):
            d = self.M.paso_hacia(pos, metas, ocup, self.r)
            if d: return {"accion": "mover", "dir": d}
            self._quiere_ir = True; return {"accion": "quedarse"}
        if yo["agotada"]: return {"accion": "dormir"}
        if obs["bestia"] or fase in ("anochecer", "noche"): return self._a_casa(pos, ocup)
        n = bolsa.count("comida"); hambre = yo["hambre"] > self.HAMBRE
        if hambre and n: return {"accion": "comer", "tipo": "comida"}
        junto = self.M.acceso_almacen
        if n >= self.LLENA: self.dejando = True
        if self.dejando:
            if n <= self.SOBRA: self.dejando = False
            elif pos in junto: return {"accion": "dejar", "en": "almacen", "tipo": "comida"}
            else: return ir(junto)
        if hambre and not n and getattr(self, "almacen_visto", None) != "vacio":
            if pos in junto: return {"accion": "coger", "de": "almacen", "tipo": "comida"}
            return ir(junto)
        if len(bolsa) < 6:
            suelo = [tuple(c["pos"]) for c in obs["casillas"] if "comida" in (c.get("objetos") or [])]      # (prompt 20) comida suelta a la vista (las bayas): se coge
            if pos in suelo: return {"accion": "coger", "de": "suelo", "tipo": "comida"}
            if suelo: return ir(suelo)
            for c in obs["casillas"]:
                q = tuple(c["pos"])
                if cerca(q) and (c.get("matorral") or {}).get("frutos"): return {"accion": "coger", "de": "matorral", "tipo": "comida"}
                if cerca(q) and (c.get("planta") or {}).get("frutos"): return {"accion": "coger", "de": "planta", "tipo": "comida"}
            con = [q for q in self.fuentes if q in self.visto and self.visto[q][1] > 0]
            if con: return ir(con)
            mirar = [q for q in self.fuentes if q not in self.visto or t - self.visto[q][0] > self.REVISA]
            if mirar: return ir(mirar)
        return self._a_casa(pos, ocup, dentro_hace="quedarse")


def juega(env, tipo, semilla, dias=None, al_dia=None):
    """una partida con un tipo de jugador en todas; devuelve el mundo al acabar"""
    if dias: env.cfg["dias_por_episodio"] = dias
    obs, infos = env.reset(seed=semilla)
    M = Mapa(infos[env.agents[0]]["mapa"])
    J = {a: (Aleatorio(a, semilla) if tipo == "aleatorio" else (Recolector if tipo == "recolector" else Tonto)(a, semilla, M, env.cfg["huerto"]["trabajo_necesario"])) for a in env.agents}
    while env.agents:
        acts = {a: J[a].actua(obs[a], infos[a]) for a in env.agents}
        obs, rew, term, trunc, infos = env.step(acts)
        if al_dia and env.turno % env.dia_turnos == 0: al_dia(env)
    return env

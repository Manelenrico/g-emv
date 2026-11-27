"""El valle (paper ocho), paso 1: el mundo solo. Interfaz como ParallelEnv de PettingZoo: reset(seed, options) -> (obs, infos); step(acciones) -> (obs, recompensas,
terminaciones, truncamientos, infos). Todas las criaturas actúan a la vez; el orden en que se resuelven (criaturas y bestia) se sortea con la semilla cada turno.
El mundo no sabe nada de emociones ni de confianza y no da puntos (recompensas siempre 0). Observaciones: diccionarios legibles. Todos los números, en config_valle.json.
No importa nada del motor G-EMV ni de cantera/."""
import copy, functools, json, os, random
from collections import deque

try:
    from pettingzoo import ParallelEnv
except Exception:                                     # sin PettingZoo, la misma interfaz
    ParallelEnv = object
try:
    from gymnasium.spaces import Space as _Space
except Exception:
    _Space = object

AQUI = os.path.dirname(os.path.abspath(__file__))
DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}
VECINAS8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
TIPOS_ACCION = ("mover", "quedarse", "coger", "dejar", "comer", "dar", "trabajar", "empujar", "golpear", "dormir", "llamar", "hablar")


def carga_config(ruta=None):
    with open(ruta or os.path.join(AQUI, "config_valle.json"), encoding="utf-8") as f: return json.load(f)


# ── espacios (para la prueba de PettingZoo): la acción es un diccionario; la observación también ──
class EspacioAccion(_Space):
    def __init__(self, llamadas, agentes, tipos_objeto):
        if _Space is not object: super().__init__(None, None)
        self.llamadas = list(llamadas); self.agentes = list(agentes); self.tipos = list(tipos_objeto)

    def sample(self, mask=None, probability=None):
        r = self.np_random if _Space is not object else random.Random()
        ch = lambda xs: xs[int(r.integers(len(xs)))] if hasattr(r, "integers") else r.choice(xs)
        t = ch(list(TIPOS_ACCION))
        a = {"accion": t}
        if t == "mover": a["dir"] = ch(list(DIRS))
        elif t == "coger": a["de"] = ch(["suelo", "planta", "almacen", "despensa"]); a["tipo"] = ch(self.tipos)
        elif t == "dejar": a["en"] = ch(["suelo", "almacen", "despensa"]); a["tipo"] = ch(self.tipos)
        elif t == "comer": a["tipo"] = ch(self.tipos)
        elif t == "dar": a["a"] = ch(self.agentes); a["tipo"] = ch(self.tipos)
        elif t in ("empujar", "golpear"): a["a"] = ch(self.agentes + ["bestia"])
        elif t == "llamar": a["llamada"] = ch(self.llamadas)
        elif t == "hablar": a["texto"] = "hola"
        return a

    def contains(self, x): return isinstance(x, dict) and x.get("accion") in TIPOS_ACCION


class EspacioObservacion(_Space):
    CLAVES = ("turno", "dia", "fase", "turno_del_dia", "yo", "bolsa", "casillas", "criaturas", "bestia", "almacen", "despensa", "oido", "mensajes", "muertes_vistas", "cadaveres")
    def __init__(self):
        if _Space is not object: super().__init__(None, None)
    def sample(self, mask=None, probability=None): return {k: None for k in self.CLAVES}
    def contains(self, x): return isinstance(x, dict) and all(k in x for k in self.CLAVES)


class Valle(ParallelEnv):
    metadata = {"name": "valle_v1", "render_modes": []}

    def __init__(self, config=None, registro=None, mando=None, objetos_cada=0):
        self.cfg = copy.deepcopy(config) if isinstance(config, dict) else carga_config(config)
        if mando: self.cfg["bestia"]["mando"] = mando
        self.ruta_registro = registro; self._f = None; self._semilla = 0; self.objetos_cada = objetos_cada
        C = self.cfg; casas = C["mapa"]["casas"]; n = C["criaturas"]["por_casa"]
        self.possible_agents = [f"{c['id']}{i + 1}" for c in casas for i in range(n)]
        self.casa_de = {a: a[0] for a in self.possible_agents}
        self.tipos_objeto = list(C["objetos"])
        self._construye_mapa()
        self.agents = []

    # ── espacios ──
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent): return EspacioAccion(self.cfg["llamadas"], self.possible_agents, self.tipos_objeto)

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent): return EspacioObservacion()

    # ── mapa estático ──
    def _construye_mapa(self):
        """coordenadas de 1 a ancho/alto, como (columna, fila); la fila 0 y la columna 0 de la rejilla son «fuera» (así el índice es la coordenada)"""
        M = self.cfg["mapa"]; W, H = M["ancho"], M["alto"]; s = M["salvaje_ancho"]
        T = [["fuera"] * (W + 1) for _ in range(H + 1)]
        for y in range(1, H + 1):
            for x in range(1, W + 1):
                T[y][x] = "salvaje" if (x <= s or y <= s or x > W - s or y > H - s) else "bosque"
        al = M["aldea"]; self.aldea = set()
        for y in range(al["y0"], al["y0"] + al["lado"]):
            for x in range(al["x0"], al["x0"] + al["lado"]): T[y][x] = "aldea"; self.aldea.add((x, y))
        cams = M["caminos"]
        for cn in cams["columnas_norte_sur"]:
            for y in range(1, H + 1):
                if (cn, y) not in self.aldea: T[y][cn] = "camino"
        for fe in cams["filas_este_oeste"]:
            for x in range(1, W + 1):
                if (x, fe) not in self.aldea: T[fe][x] = "camino"
        self.plantas_pos = []; self.huerto_de = {}; self.rendimiento = {}
        for h in M["huertos"]:
            self.rendimiento[h["id"]] = h.get("rendimiento", 1.0)
            for q in h.get("area") or []: T[q[1]][q[0]] = "huerto"            # (prompt 29) el huerto es un cuadrado de tierra; las plantas, dentro
            for q in h["plantas"]: q = tuple(q); self.plantas_pos.append(q); self.huerto_de[q] = h["id"]; T[q[1]][q[0]] = "huerto"
        self.casa_celdas = {}; self.puerta_casa = {}; self.celda_casa = {}
        L = M["casa_lado"]
        for c in M["casas"]:
            cel = {(x, y) for y in range(c["y0"], c["y0"] + L) for x in range(c["x0"], c["x0"] + L)}
            for (x, y) in cel: T[y][x] = "casa"; self.celda_casa[(x, y)] = c["id"]
            self.casa_celdas[c["id"]] = cel; self.puerta_casa[c["id"]] = tuple(c["puerta"])
        self.almacen_celdas = {tuple(c) for c in M["almacen"]}
        for (x, y) in self.almacen_celdas: T[y][x] = "almacen"
        self.almacen_acceso = {(x + dx, y + dy) for (x, y) in self.almacen_celdas for dx, dy in VECINAS8} - self.almacen_celdas
        self.puertas = {tuple(q): p for p in self.cfg["puertas"] for q in p["celdas"]}
        for (x, y) in self.puertas: T[y][x] = "puerta"
        self.T = T; self.W, self.H = W, H
        self.celdas_bosque = [(x, y) for y in range(1, H + 1) for x in range(1, W + 1) if T[y][x] == "bosque"]
        self.celdas_salvaje = [(x, y) for y in range(1, H + 1) for x in range(1, W + 1) if T[y][x] == "salvaje"]
        self.en_anillo = lambda p: p[0] <= s or p[1] <= s or p[0] > W - s or p[1] > H - s
        # la bestia: zona salvaje, caminos, aldea fuera de las casas y huertos; y el bosque si tiene que llegar a un huerto
        andar = {"salvaje", "camino", "aldea", "huerto"} | ({"bosque"} if self.cfg["bestia"].get("anda_por_el_bosque_para_ir_al_huerto") else set())
        self.paso_bestia = {(x, y) for y in range(1, H + 1) for x in range(1, W + 1) if T[y][x] in andar}
        self.entrada_camino = {k: tuple(v) for k, v in M["entradas_bestia"].items()}
        self.borde_aldea = {k: tuple(v) for k, v in M["bordes_aldea"].items()}

    def mapa_publico(self):
        """lo estático del mapa, igual para cualquier agente. `terreno[fila][columna]`, con la fila 0 y la columna 0 «fuera» (x), para que el índice sea la coordenada (1 a 48)"""
        ab = {"bosque": "b", "salvaje": "s", "aldea": "a", "camino": "c", "huerto": "h", "casa": "k", "almacen": "m", "puerta": "p", "fuera": "x"}
        return {"ancho": self.W, "alto": self.H, "origen": 1, "terreno": ["".join(ab[t] for t in fila) for fila in self.T],
                "leyenda": {v: k for k, v in ab.items()},
                "casas": {k: {"celdas": sorted(v), "puerta": self.puerta_casa[k]} for k, v in self.casa_celdas.items()},
                "almacen": sorted(self.almacen_celdas), "almacen_acceso": sorted(self.almacen_acceso), "plantas": self.plantas_pos,
                "huertos": {k: [q for q in self.plantas_pos if self.huerto_de[q] == k] for k in self.rendimiento},
                "puertas": {p["id"]: {"celdas": p["celdas"], "conecta_con": p["conecta_con"]} for p in self.cfg["puertas"]},
                "reglas_publicas": {k: self._regla_publica(k) for k in self.cfg.get("reglas_publicas", [])},
                "matorrales": [[q[0], q[1], m["zona"]] for q, m in sorted(self.matorrales.items())]}          # (prompt 19) el matorral se ve siempre

    def _regla_publica(self, k):
        """(v4, Manel) lo que el mundo hace público al empezar, igual para todas: el daño del golpe de la bestia y de una criatura, y que la bestia roba la bolsa;
        (prompt 12; confirmada por Manel en el prompt 15) que la bestia no entra en las casas (ni encuentra a quien está dentro, `_encuentros`)"""
        return {"golpe_bestia": self.cfg["bestia"]["golpe_dano"], "golpe_criatura": self.cfg["criaturas"]["golpe_dano"], "bestia_roba_la_bolsa": True,
                "bestia_no_entra_en_casas": True,
                "no_se_trabaja_de_noche": self.cfg["criaturas"].get("trabajar_de_noche") is False,          # (prompt 26) públicas: de noche y sin fuerzas no se trabaja
                "no_se_trabaja_sin_fuerzas": self.cfg["criaturas"].get("trabajar_sin_fuerzas") is False,
                "bestia_cuenta_como": self.cfg["bestia"]["peso_empuje"],
                "temperatura_confort": list((self.cfg.get("temperatura") or {}).get("confort") or []),
                "harta_por_debajo": self.cfg["criaturas"].get("harta_por_debajo"),
                "frio_hambre_por_grado": (self.cfg.get("temperatura") or {}).get("frio_hambre_por_grado"),
                "frio_noche_fuera": self._frio_noche_fuera(),
                "bestia_pasos_por_turno": self.cfg["bestia"].get("pasos_por_turno", 1),          # (prompt 58) lo rápido que se mueve la bestia
                "medicina_cura_heridas": {"cura": self.cfg["objetos"]["medicina"].get("cura", 0), "hambre_max": self.cfg["criaturas"]["hambre_max"],
                                          "dano_hambre_por_turno": self.cfg["criaturas"]["vida_por_turno_con_hambre_max"], "dormir_cierra_antes_las_heridas": True},   # (prompt 60, Manel) cura heridas, no el daño del hambre          # (prompt 58) lo rápido que se mueve la bestia: una casilla por turno
                "llamadas_voz": ({k_: v_ for k_, v_ in (self.cfg.get("llamadas_voz") or {}).items() if k_ in ("tipos", "alcance", "cansancio")} or None)}[k]          # (prompt 57) hasta dónde llega cada fuerza y lo que cansa          # (prompt 56) el hambre de más que cuesta una noche entera fuera          # (prompt 55) fuera, bajo la zona cómoda, el hambre sube más          # (prompt 35) por debajo de este hambre no se puede comer          # (prompt 34) entre qué grados se está bien          # (prompt 27) para empujarla hacen falta tantas como pesa

    def _frio_noche_fuera(self):
        """(prompt 56, Manel) lo que cuesta de hambre una noche entera fuera de casa por el frío, como hecho del cuerpo: el anochecer despierta y la noche dormida
        (el reloj del hambre), cada turno ×(frío por grado × grados de menos). Con los números del mundo"""
        Tc = self.cfg.get("temperatura") or {}; k = Tc.get("frio_hambre_por_grado")
        if not (Tc.get("activo") and k): return None
        cr = self.cfg["criaturas"]; hr = cr.get("hambre_reloj") or {}; dorm = hr.get("dormida", 1.0) if hr.get("activo") else 1.0
        tot = 0.0
        for nom, n in self.cfg["dia"]["fases"]:
            if nom in ("anochecer", "noche"):
                tot += n * cr["hambre_por_turno"] * (dorm if nom == "noche" else 1.0) * k * max(0.0, Tc["confort"][0] - Tc["fuera"][nom])
        return round(tot, 2)

    def terreno(self, p): return self.T[p[1]][p[0]]
    def dentro(self, p): return 1 <= p[0] <= self.W and 1 <= p[1] <= self.H

    # ── objetos ──
    def _nuevo(self, tipo):
        self._id += 1; return {"id": self._id, "tipo": tipo, "pudricion": 0.0}

    def _sabores(self):
        """(prompt 85, Manel: pieza E, apagado por defecto) dos sabores: cada comida lleva su origen (la del huerto, «huerto»; la de los matorrales, «bosque»);
        alimentan igual. Se ve en la bolsa y en el suelo, y se puede pedir cuál comer o dar. Se enciende con objetos.sabores.activo (no está en la config)"""
        return bool((self.cfg["objetos"].get("sabores") or {}).get("activo"))

    def _cuenta(self, tipo, que, n=1, dia=None):
        d = self.libro.setdefault(dia if dia is not None else self.dia, {}); x = d.setdefault(tipo, {}); x[que] = x.get(que, 0) + n

    def _existencias(self, tipo):
        n = sum(1 for L in self.suelo.values() for o in L if o["tipo"] == tipo) + sum(1 for b in self.bolsa.values() for o in b if o["tipo"] == tipo)
        n += sum(1 for d in self.despensa.values() for o in d if o["tipo"] == tipo) + sum(1 for o in self.almacen if o["tipo"] == tipo)
        n += sum(1 for p in self.plantas.values() for o in p["frutos"] if o["tipo"] == tipo) + sum(1 for B in self.bestias for o, _ in B["lleva"] if o["tipo"] == tipo)
        n += sum(1 for m in self.matorrales.values() for o in m["frutos"] if o["tipo"] == tipo)
        return n

    # ── reset ──
    def reset(self, seed=None, options=None):
        if seed is not None: self._semilla = int(seed)
        C = self.cfg; self.rng = random.Random(self._semilla)
        self.agents = list(self.possible_agents); self.turno = 0; self._id = 0
        self.dia_turnos = C["dia"]["turnos"]; self.max_turnos = C["dias_por_episodio"] * self.dia_turnos
        cr = C["criaturas"]
        self.pos = {}; self.cuerpo = {}; self.bolsa = {a: [] for a in self.agents}
        for c in C["mapa"]["casas"]:
            libres = sorted(self.casa_celdas[c["id"]] - {self.puerta_casa[c["id"]]})
            for i, a in enumerate([a for a in self.agents if self.casa_de[a] == c["id"]]): self.pos[a] = libres[i]
        for a in self.agents: self.cuerpo[a] = {"vida": float(cr["vida_max"]), "hambre": 0.0, "cansancio": 0.0, "herida": 0.0, "agotada": False, "muerta": False, "causa": None, "dormida": False}
        self.suelo = {}; self.despensa = {k: [] for k in self.casa_celdas}; self.almacen = []; self.libreta = []
        self.cadaveres = {}; self.muertes_vistas = {a: [] for a in self.agents}; self._zona_set = {}
        self.caras = {}                                                     # (prompt 128) la última cara de cada criatura
        self.libro = {}; self.dia = 0
        hu = C["huerto"]
        arr = hu.get("arranque") or {}
        if arr.get("fruto_a_punto_en_el_primer_dia"):          # una aldea que ya existía: el primer ciclo, ya trabajado, madura en un momento del primer día
            self.plantas = {p: {"frutos": [], "trabajo": hu["trabajo_necesario"] if arr.get("primer_ciclo_trabajado") else 0, "fin": self.rng.randrange(1, self.dia_turnos)} for p in self.plantas_pos}
        else:
            self.plantas = {p: {"frutos": [], "trabajo": 0, "fin": (self.rng.randrange(hu["ciclo_turnos"]) if hu["desfase_al_azar"] else 0) + hu["ciclo_turnos"]} for p in self.plantas_pos}
        if hu.get("cuidado"):                                   # (prompt 18) el cuidado de cada planta: la aldea que ya existía empieza cuidada
            for P in self.plantas.values(): P["cuidado"] = 1.0 if arr.get("primer_ciclo_trabajado") else 0.0
        self._calcula_aparicion()
        # (prompt 19, Manel) los matorrales: fijos, repartidos al empezar (los pone la semilla); cada uno da fruto cada cierto tiempo, con desfase al azar
        self.matorrales = {}
        if self.mat_cfg:
            for zona, celdas in (("bosque", self.celdas_bosque), ("salvaje", self.celdas_salvaje)):
                for q in sorted(self.rng.sample(sorted(celdas), self.n_matorrales[zona])):
                    self.matorrales[q] = {"zona": zona, "frutos": [], "fin": self.rng.randrange(1, self.mat_cfg[zona]["fruto_cada"] + 1)}
        self.stock_inicio_dia = {t: 0 for t in self.tipos_objeto}          # el almacén inicial cuenta como aparecido el día 0
        for t, n in C["aparicion"]["almacen_inicial"].items():
            for _ in range(n): self.almacen.append(self._nuevo(t)); self._cuenta(t, "aparece")
        s0 = sorted(self.celdas_salvaje)[self.rng.randrange(len(self.celdas_salvaje))]
        self.bestia = {"pos": s0, "modo": "ronda", "ruta": [], "lleva": [], "espera": {}, "camino": None}
        self.bestia["id"] = "bestia"; self.bestias = [self.bestia]; self._g_golpes = {}; self.stats_g = {}       # (prompt 88) pieza G: la lista de bestias (la primera, «bestia»)
        G = self._G()
        if G:
            self.stats_g = {"nacen": 0, "echadas": 0, "muertas": 0, "vuelven": 0, "reaparecen": 0, "se_marchan": 0, "comida_dejada": 0, "max_bestias": 1}; self._g_cria = 0.0
            if G.get("matar", {}).get("activo"): self.bestia["vida"] = float(G["matar"]["vida"])
            for _ in range(int(G.get("inicial", 1)) - 1): self._g_nueva("inicial")
        self.arboles = {}; self.stats_arbol = {}
        if (C.get("arbol_dulce") or {}).get("activo"): self._arboles_inicia()      # (prompt 96) el árbol de fruta dulce (apagado por defecto)
        self._plan_dia()
        self.oido = {a: [] for a in self.agents}; self.mensajes = {a: [] for a in self.agents}; self.esfuerzo = {a: 0 for a in self.agents}; self.hambre_extra = {a: 0.0 for a in self.agents}
        self.cuadre = []; self._eventos = []; self.stats = {"trabajo": {}, "almacen_fin_dia": [], "podrido_por_sitio": {}, "bestia_roba": 0, "bestia_pega": 0, "bestia_come_huerto": 0, "trabajo_por_huerto": {}, "fuera_aldea": {}}
        if self._f: self._f.close(); self._f = None
        if self.ruta_registro: self._f = open(self.ruta_registro, "w", encoding="utf-8")
        obs = {a: self._observa(a) for a in self.agents}
        mp = self.mapa_publico()
        infos = {a: {"mapa": mp, "casa": self.casa_de[a], "acciones_validas": self.acciones_validas(a)} for a in self.agents}
        return obs, infos

    def _calcula_aparicion(self):
        """(prompt 18, Manel) con `margen_comida.activo`, la comida que aparece cada día en el bosque y la zona salvaje es lo que comen las criaturas al día
        (hambre_por_turno × turnos del día / nutricion, por criatura) por (1 + margen), repartida entre las dos zonas como en `aparicion`; la medicina no cambia.
        Y lo que da una planta sin cuidado: lo que da en un ciclo una casilla de bosque (comida del bosque al día / casillas de bosque × días del ciclo)"""
        C = self.cfg; ap = {z: dict(v) for z, v in C["aparicion"].items()}; mc = C.get("margen_comida") or {}
        if mc.get("activo") is not None:
            cr = C["criaturas"]; n_cri = len(self.possible_agents)
            al_dia = cr["hambre_por_turno"] * C["dia"]["turnos"] / C["objetos"]["comida"]["nutricion"] * n_cri
            N = int(round(al_dia * (1.0 + float(mc["activo"])))); b0, s0 = ap["bosque"].get("comida", 0), ap["salvaje"].get("comida", 0)
            nb = int(round(N * b0 / (b0 + s0))); ap["bosque"]["comida"] = nb; ap["salvaje"]["comida"] = N - nb
            self.stats_aparicion = {"comen_al_dia": al_dia, "margen": float(mc["activo"]), "aparece_al_dia": N, "bosque": nb, "salvaje": N - nb}
        else: self.stats_aparicion = {"margen": None, "aparece_al_dia": sum(ap[z].get("comida", 0) for z in ("bosque", "salvaje"))}
        self.mat_cfg = (C.get("matorrales") or {}) if (C.get("matorrales") or {}).get("activo") else None
        sd = (C.get("estres") or {}).get("sequia_dura") or {}
        if self.mat_cfg and sd.get("activo"):                    # (prompt 68, Manel) mando de estrés: la sequía dura, las épocas de la sequía × un factor
            ep = dict(sd["epocas"]); ep["factores"] = [round(f * float(sd["multiplica"]), 6) for f in ep["factores"]]; ep["activo"] = True
            self.mat_cfg = dict(self.mat_cfg, epocas=ep)
        if self.mat_cfg:                                         # (prompt 19) con matorrales ya no aparece comida en casillas al azar (la medicina sí)
            for z in ("bosque", "salvaje"): ap[z]["comida"] = 0
        self.aparicion = ap
        cu = C["huerto"].get("cuidado") or {}
        dia = C["dia"]["turnos"]; ciclo = C["huerto"]["ciclo_turnos"]
        if cu:
            fs = cu["frutos_sin_cuidado"]
            if fs == "como_matorral": fs = self.mat_cfg["bosque"]["frutos"] * ciclo / self.mat_cfg["bosque"]["fruto_cada"]       # (prompt 19) una planta sin cuidado es un matorral del bosque
            if fs == "como_bosque": fs = ap["bosque"].get("comida", 0) / len(self.celdas_bosque) * C["huerto"]["ciclo_turnos"] / C["dia"]["turnos"]
            self.frutos_sin_cuidado = float(fs); self.cuidado_baja = 0.5 ** (1.0 / float(cu["semivida_turnos"]))
            self.stats_aparicion["frutos_sin_cuidado"] = self.frutos_sin_cuidado
        if self.mat_cfg:
            M = self.mat_cfg; da = {z: M[z]["frutos"] * dia / M[z]["fruto_cada"] for z in ("bosque", "salvaje")}      # lo que da un matorral al día
            huerto_dia = len(self.plantas_pos) * (self.frutos_sin_cuidado if cu else 0.0) * dia / ciclo
            if mc.get("activo") is not None:
                # el margen ajusta cuántos matorrales hay: lo que falta sobre lo que da el huerto sin cuidado, 2/3 en el bosque y 1/3 en la zona salvaje (como la comida de antes)
                cr = C["criaturas"]; al_dia = cr["hambre_por_turno"] * dia / C["objetos"]["comida"]["nutricion"] * len(self.possible_agents)
                falta = max(0.0, al_dia * (1.0 + float(mc["activo"])) - huerto_dia)
                self.n_matorrales = {"bosque": max(1, int(round(falta * 2 / 3 / da["bosque"]))), "salvaje": max(1, int(round(falta / 3 / da["salvaje"])))}
                self.stats_aparicion.update({"comen_al_dia": al_dia, "margen": float(mc["activo"])})
            else: self.n_matorrales = {z: M[z]["numero"] for z in ("bosque", "salvaje")}
            total = huerto_dia + sum(self.n_matorrales[z] * da[z] for z in da)
            self.stats_aparicion.update({"matorrales": dict(self.n_matorrales), "da_un_matorral_al_dia": da, "huerto_sin_cuidado_al_dia": huerto_dia, "comida_al_dia": total,
                                         "aparece_al_dia": total, "bosque": self.n_matorrales["bosque"] * da["bosque"], "salvaje": self.n_matorrales["salvaje"] * da["salvaje"]})
            if self.stats_aparicion.get("comen_al_dia"): self.stats_aparicion["margen_efectivo"] = total / self.stats_aparicion["comen_al_dia"] - 1.0

    # ── (prompt 88, Manel) pieza G: la bestia como un mando (todo apagado por defecto: una bestia, la de siempre) ──
    def _G(self):
        """la pieza G si alguna rueda está encendida (o empieza con más de una bestia); si no, None (el mundo de siempre)"""
        G = self.cfg["bestia"].get("pieza_g") or {}
        if int(G.get("inicial", 1)) != 1 or any((G.get(k) or {}).get("activo") for k in ("cria", "epocas", "echar", "matar")): return G
        return None

    def _g_sitio(self):
        """dónde aparece una bestia: una casilla de la zona salvaje, a suertes, sin nadie"""
        L = sorted(self.celdas_salvaje)
        for _ in range(50):
            q = L[self.rng.randrange(len(L))]
            if not self.ocupada(q): return q
        return q

    def _g_nueva(self, por):
        """una bestia nueva (al empezar, o nace), en la zona salvaje, de ronda"""
        G = self._G(); k = len(self.bestias) + 1
        B = {"pos": self._g_sitio(), "modo": "ronda", "ruta": [], "lleva": [], "espera": {}, "camino": None, "id": f"bestia{k}"}
        if (G.get("matar") or {}).get("activo"): B["vida"] = float(G["matar"]["vida"])
        self.bestias.append(B); self.stats_g["max_bestias"] = max(self.stats_g.get("max_bestias", 1), len(self.bestias))
        if por != "inicial": self.stats_g["nacen"] += 1; self._ev({"bestia_nace": B["id"], "en": list(B["pos"])})
        return B

    def bestia_de(self, x):
        """la bestia de ese nombre, si está en el mapa (ni echada lejos ni muerta)"""
        return next((B for B in self.bestias if B["id"] == x and B["pos"] is not None), None)

    def bestias_aqui(self): return [B for B in self.bestias if B["pos"] is not None]

    def _g_cuantas(self):
        """(épocas) cuántas puede haber: el máximo de la cría (o las del principio) por el factor de la época, redondeado, al menos una"""
        G = self._G(); base = int((G.get("cria") or {}).get("maximo", 0)) if (G.get("cria") or {}).get("activo") else int(G.get("inicial", 1))
        if (G.get("epocas") or {}).get("activo"): return max(1, int(round(base * self.factor_epoca())))
        return base

    def _g_turno(self):
        """al acabar de actuar todas: lo que le hicieron a cada bestia este turno (echar, matar); las que se curan; las que vuelven o reaparecen"""
        G = self._G(); E, M = G.get("echar") or {}, G.get("matar") or {}
        for B in self.bestias:
            g = self._g_golpes.get(B["id"])
            if B["pos"] is None or not g: continue
            n = len(g["empuje"]); q = B["pos"]                                  # (prompt 89, Manel) echar cuenta solo los empujones; matar, solo los golpes
            if M.get("activo") and g["golpe"]:
                dano = float(self.cfg["criaturas"]["golpe_dano"]) * len(g["golpe"]) ** float(M["exponente"]); B["vida"] -= dano
                self._ev({"bestia_herida": B["id"], "golpean": sorted(g["golpe"]), "dano": round(dano, 3), "vida": round(max(0.0, B["vida"]), 3)})
                if B["vida"] <= 0:
                    for o, _ in B["lleva"]: self.suelo.setdefault(q, []).append(o)
                    for _ in range(int(M["comida_deja"])):
                        o = self._nuevo("comida"); self._cuenta("comida", "aparece")
                        if self._sabores(): o["origen"] = "bestia"
                        self.suelo.setdefault(q, []).append(o)
                    self.stats_g["muertas"] += 1; self.stats_g["comida_dejada"] += int(M["comida_deja"])
                    self._ev({"bestia_muere": B["id"], "en": list(q), "golpean": sorted(g["golpe"]), "deja": int(M["comida_deja"]) + len(B["lleva"])})
                    B.update(pos=None, modo="muerta", ruta=[], lleva=[], espera={}, camino=None, vuelve_t=self.turno + int(M["reaparece_turnos"])); continue
            if E.get("activo") and n:
                fuerza = n ** float(E["exponente"]); umbral = float(E["umbral_criaturas"]) ** float(E["exponente"])      # la fuerza de n a la vez; el umbral, la de tantas
                if fuerza >= umbral - 1e-9:
                    lejos = int(round(float(E["lejos_turnos"]) * fuerza / umbral))
                    for o, _ in B["lleva"]: self.suelo.setdefault(q, []).append(o)
                    self.stats_g["echadas"] += 1
                    self._ev({"bestia_echada": B["id"], "desde": list(q), "criaturas": n, "fuerza": round(fuerza, 3), "vuelve_en": lejos, "suelta": [o["tipo"] for o, _ in B["lleva"]]})
                    B.update(pos=None, modo="lejos", ruta=[], lleva=[], espera={}, camino=None, vuelve_t=self.turno + lejos)
        self._g_golpes = {}
        for B in self.bestias:
            if B["pos"] is not None:
                if M.get("activo") and B["vida"] < float(M["vida"]): B["vida"] = min(float(M["vida"]), B["vida"] + float(M["cura_por_turno"]))
            elif B.get("vuelve_t") is not None and self.turno >= B["vuelve_t"]:
                muerta = B["modo"] == "muerta"; B.update(pos=self._g_sitio(), modo="ronda", vuelve_t=None)
                if M.get("activo"): B["vida"] = float(M["vida"])
                self.stats_g["reaparecen" if muerta else "vuelven"] += 1; self._ev({("bestia_aparece" if muerta else "bestia_vuelve"): B["id"], "en": list(B["pos"])})

    def _g_dia(self):
        """al acabar el día: la cría (cada tantos días, más deprisa en la abundancia y más despacio en la escasez si sigue a las épocas) y, con las épocas,
        las que sobran se marchan (las últimas que llegaron, si no están lejos ni muertas: esas cuentan igual)"""
        G = self._G(); Cr = G.get("cria") or {}
        tope = self._g_cuantas()
        if Cr.get("activo"):
            self._g_cria += self.factor_epoca() if (G.get("epocas") or {}).get("activo") else 1.0
            if self._g_cria >= float(Cr["cada_dias"]) - 1e-9:
                self._g_cria -= float(Cr["cada_dias"])
                if len(self.bestias) < tope: self._g_nueva("nace")
        if (G.get("epocas") or {}).get("activo"):
            while len(self.bestias) > tope and len(self.bestias) > 1:
                B = self.bestias.pop()
                for o, _ in B["lleva"]: self._cuenta(o["tipo"], "comido_bestia")
                self.stats_g["se_marchan"] += 1; self._ev({"bestia_se_marcha": B["id"]})

    # ── (prompt 96, Manel) el árbol de fruta dulce (apagado por defecto) ──
    def _arboles_inicia(self):
        """dos sitios lejos de la aldea (zona salvaje, a la distancia andando de la config o más desde la puerta de casa más cercana, lejos uno del otro), y para
        cada uno sus apariciones (2 o 3 por partida, en momentos al azar, de 3 o 4 días, sin pisarse)"""
        A = self.cfg["arbol_dulce"]; puertas = sorted(self.puerta_casa.values()); D = {p: 0 for p in puertas}; q = deque(puertas)
        while q:
            u = q.popleft()
            for d in DIRS.values():
                v = (u[0] + d[0], u[1] + d[1])
                if v not in D and self.paso_valido(u, v): D[v] = D[u] + 1; q.append(v)
        lejos = sorted(c for c in self.celdas_salvaje if D.get(c, -1) >= int(A["distancia_min"]))
        sitios = []
        for _ in range(500):
            if len(sitios) >= int(A["numero"]) or not lejos: break
            c = lejos[self.rng.randrange(len(lejos))]
            if all(self._dist(c, s_) >= int(A["separacion_min"]) for s_ in sitios): sitios.append(c)
        total = self.max_turnos; self.arboles = {}
        for c in sitios:
            n = self.rng.randint(int(A["apariciones"][0]), int(A["apariciones"][1])); tramos = []
            for _ in range(200):
                if len(tramos) >= n: break
                dura = self.rng.randint(int(A["dura_dias"][0]), int(A["dura_dias"][1])) * self.dia_turnos; t0 = self.rng.randrange(max(1, total - dura))
                if all(t0 + dura <= a or t0 >= b for a, b in tramos): tramos.append((t0, t0 + dura))
            self.arboles[c] = {"tramos": sorted(tramos), "activo": False, "dist": D.get(c)}
        self.stats_arbol = {"sitios": [[list(c), self.arboles[c]["dist"], self.arboles[c]["tramos"]] for c in sorted(self.arboles)], "aparece": 0, "frutos_puestos": 0,
                            "frutos_se_pierden": 0, "roba_dulce": 0, "bestia_va": 0}

    def _arboles_avanza(self):
        """cada turno: el árbol aparece (con sus frutas dulces, que no se pudren en el árbol ni vuelven) o se va (lo que quede se pierde)"""
        A = self.cfg["arbol_dulce"]
        for c, T_ in self.arboles.items():
            dentro = any(a <= self.turno < b for a, b in T_["tramos"])
            if dentro and not T_["activo"]:
                fr = []
                for _ in range(int(A["frutos"])):
                    o = self._nuevo("comida"); self._cuenta("comida", "aparece")
                    if self._sabores(): o["origen"] = "dulce"
                    fr.append(o)
                self.matorrales[c] = {"zona": "arbol", "frutos": fr, "fin": 10 ** 12}; T_["activo"] = True
                self.stats_arbol["aparece"] += 1; self.stats_arbol["frutos_puestos"] += len(fr); self._ev({"arbol_aparece": list(c), "frutos": len(fr)})
            elif T_["activo"] and not dentro:
                Mt = self.matorrales.pop(c, None) or {"frutos": []}
                for o in Mt["frutos"]: self._cuenta(o["tipo"], "podrido")
                self.stats_arbol["frutos_se_pierden"] += len(Mt["frutos"]); T_["activo"] = False; self._ev({"arbol_se_va": list(c), "quedaban": len(Mt["frutos"])})

    def _arbol_de_bestia(self, B):
        """(en las fases de la config: desde el prompt 97, solo al anochecer) el árbol activo al que va esta bestia: el más cercano a ella, si es la bestia más
        cercana a ese árbol. Al caer la noche sigue hacia la aldea como siempre (su decisión de bajar, desde donde esté)"""
        if not self.arboles or self.fase() not in (self.cfg["arbol_dulce"].get("bestia_fases") or ["anochecer", "noche"]) or B["pos"] is None: return None      # (prompt 97) las fases, de la config
        act = [c for c, T_ in self.arboles.items() if T_["activo"]]
        if not act: return None
        mio = None
        for c in sorted(act, key=lambda c: (self._dist(B["pos"], c), c)):
            cerca = min(self.bestias_aqui(), key=lambda X: (self._dist(X["pos"], c), self.bestias.index(X)))
            if cerca is B: mio = c; break
        return mio

    def _plan_dia(self):
        """las apariciones de hoy: exactamente N de cada cosa y zona, en turnos sorteados"""
        self.apariciones = {}
        for zona, cosas in self.aparicion.items():
            if zona == "almacen_inicial": continue
            for tipo, n in cosas.items():
                for t in self.rng.sample(range(self.dia_turnos), n): self.apariciones.setdefault(t, []).append((zona, tipo))

    # ── reloj ──
    def fase(self, t=None):
        r = (self.turno if t is None else t) % self.dia_turnos; acc = 0
        for nombre, n in self.cfg["dia"]["fases"]:
            acc += n
            if r < acc: return nombre
        return self.cfg["dia"]["fases"][-1][0]

    # ── consultas ──
    def ocupada(self, p, salvo=None):
        if salvo != "bestia" and any(B["pos"] == p for B in self.bestias): return True
        return any(self.pos[a] == p and a != salvo for a in self.agents if not self.cuerpo[a]["muerta"])

    def paso_valido(self, desde, hacia):
        if not self.dentro(hacia): return False
        t = self.terreno(hacia)
        if t in ("puerta", "almacen"): return False
        if any(self.cfg["objetos"][o["tipo"]].get("bloquea") for o in self.suelo.get(hacia, [])): return False
        cd, ch = self.celda_casa.get(desde), self.celda_casa.get(hacia)
        if ch != cd:                                   # cruzar la pared de una casa: solo por su puerta
            if ch is not None and hacia != self.puerta_casa[ch]: return False
            if cd is not None and desde != self.puerta_casa[cd]: return False
        return True

    def vecinas(self, a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1])) == 1
    def junto_o_en(self, a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1
    def en_casa_propia(self, a): return self.celda_casa.get(self.pos[a]) == self.casa_de[a]
    def en_aldea(self, a): return self.pos[a] in self.aldea
    def planta_junto(self, a, con_frutos=False):
        ps = [p for p in self.plantas_pos if self.junto_o_en(self.pos[a], p) and (not con_frutos or self.plantas[p]["frutos"])]
        return sorted(ps, key=lambda p: (self.plantas[p]["trabajo"], p))
    def factor_epoca(self, huerto=False):
        """(prompt 20, 30) lo que da la naturaleza según la época (sin épocas, 1); con `afecta_huerto`, también las plantas del huerto"""
        ep = (self.mat_cfg or {}).get("epocas") or {}
        if not ep.get("activo") or (huerto and not ep.get("afecta_huerto")): return 1.0
        return ep["factores"][(self.dia // ep["duracion_dias"]) % len(ep["factores"])]

    def epoca(self):
        ep = (self.mat_cfg or {}).get("epocas") or {}; nombres = ep.get("nombres") or []
        if not ep.get("activo"): return None
        i = (self.dia // ep["duracion_dias"]) % len(ep["factores"]); return nombres[i] if i < len(nombres) else str(i)

    def temperatura(self, p=None):
        """(prompt 34, Manel) los grados: fuera, según la fase del día; dentro de cualquier casa, siempre los mismos. Sin la clave, None"""
        T_ = self.cfg.get("temperatura") or {}
        if not T_.get("activo"): return None
        if p is not None and self.celda_casa.get(tuple(p)) is not None: return T_["dentro_de_casa"]
        return T_["fuera"][self.fase()]

    def harta(self, a, tipo="comida"):
        """(prompt 35, Manel) harta no se puede comer lo que alimenta: con el hambre por debajo del umbral («ya no me entra más»). Sin la clave, nunca"""
        u = self.cfg["criaturas"].get("harta_por_debajo")
        return u is not None and self.cfg["objetos"][tipo].get("nutricion", 0) > 0 and self.cuerpo[a]["hambre"] < u

    def vista(self):
        """(prompt 38, Manel) de noche se ve menos: la vista según la fase del día (`vista_por_fase`); sin la clave, la de siempre"""
        cr = self.cfg["criaturas"]; vf = cr.get("vista_por_fase")
        return vf.get(self.fase(), cr["vista"]) if vf else cr["vista"]

    def reloj(self):
        R = self.cfg["criaturas"].get("reloj") or {}
        return bool(R.get("activo"))

    def dolor_fuerte(self, a):
        """(prompt 43, Manel: el hambre es dolor) mucha hambre (por encima de la banda «flaca») o una herida grave (por debajo de la banda «herida»)"""
        D = self.cfg["criaturas"].get("dolor_quita_sueno") or {}
        if not D.get("activo"): return None
        c = self.cuerpo[a]; cr = self.cfg["criaturas"]
        if c["hambre"] > cr["umbral_flaca"]: return "hambre"
        if c["vida"] < cr["umbral_herida"]: return "herida"
        return None

    def _peligro(self, a):
        """(prompt 42, con los añadidos de Manel) lo que despierta: una llamada urgente oída (a la distancia de siempre: dormida sigue oyendo), que la empujen o
        le peguen, o tener la bestia al lado. Las demás llamadas no despiertan. Devuelve el motivo, o None"""
        c = self.cuerpo[a]
        d_ = self.dolor_fuerte(a)
        if d_: return d_                                                    # (prompt 43) un dolor fuerte despierta
        if c.get("golpe_t") == self.turno - 1: return "golpe"
        if c.get("empujon_t") == self.turno - 1: return "empujon"
        if any(self.vecinas(self.pos[a], B["pos"]) for B in self.bestias_aqui()): return "bestia al lado"
        if (self.cfg.get("voz_v68") or {}).get("activo"):                  # (prompt 132, taller) la voz pieza a pieza: la alarma despierta, y lo de antes sigue
            if any(o.get("voz") == "alarma" for o in self._oido_prev.get(a, [])): return "voz alarma"
        elif (self.cfg.get("voz_v64") or {}).get("activo"):                # (prompt 128) con la voz de la base, de lo que se oye solo despierta la alarma
            return "voz alarma" if any(o.get("voz") == "alarma" for o in self._oido_prev.get(a, [])) else None
        urg = set(self.cfg["criaturas"]["reloj"].get("llamadas_que_despiertan") or [])
        ll = next((o["llamada"] for o in self._oido_prev.get(a, []) if o.get("llamada") in urg), None)
        if ll: return f"llamada {ll}"
        son = set(self.cfg["criaturas"]["reloj"].get("sonidos_que_despiertan") or [])          # (prompt 55, Manel) un sonido fuerte de dolor despierta, como antes «estoy herida»
        sn = next((f'{o["sonido"]}:{o.get("intensidad")}' for o in self._oido_prev.get(a, []) if o.get("sonido") and f'{o["sonido"]}:{o.get("intensidad")}' in son), None)
        return f"sonido {sn}" if sn else None

    def puede_trabajar(self, a):
        """(prompt 26, Manel) con el hambre al máximo no se puede trabajar (el cuerpo no tiene fuerzas), y de noche tampoco (está oscuro). Sin las claves, siempre"""
        cr = self.cfg["criaturas"]; c = self.cuerpo[a]
        if cr.get("trabajar_sin_fuerzas") is False and c["hambre"] >= cr["hambre_max"]: return False
        if cr.get("trabajar_de_noche") is False and self.fase() == "noche": return False
        return True

    def puede_dormir(self, a):
        """(prompt 25, Manel) no se duerme sin sueño: de día (mañana y tarde) solo con el cansancio por encima de un umbral; al anochecer y de noche, de otro más bajo.
        Agotada, siempre (se duerme sola). Sin la clave en la config, siempre se puede"""
        c = self.cuerpo[a]; u = self.cfg["criaturas"].get("dormir_desde")
        if self.dolor_fuerte(a) and not c["agotada"]: return False             # (prompt 43) un dolor fuerte quita el sueño
        if self.reloj():                                                    # (prompt 42) de noche, siempre; de día, solo muy cansada (o agotada)
            return c["agotada"] or self.fase() in ("anochecer", "noche") or c["cansancio"] >= self.cfg["criaturas"]["energia_normal_bajo"]
        if not u or c["agotada"]: return True
        return c["cansancio"] > (u["dia"] if self.fase() in ("mañana", "tarde") else u["noche"])

    def matorral_junto(self, a, con_frutos=False):
        ms = [q for q in self.matorrales if self.junto_o_en(self.pos[a], q) and (not con_frutos or self.matorrales[q]["frutos"])]
        return sorted(ms, key=lambda q: (-len(self.matorrales[q]["frutos"]), q))
    def bolsa_llena(self, a): return len(self.bolsa[a]) >= self.cfg["criaturas"]["bolsa_huecos"]
    def vivas(self): return [a for a in self.agents if not self.cuerpo[a]["muerta"]]

    def nivel_almacen(self):
        A = self.cfg["almacen"]
        if A.get("nivel_solo_comida"): n = sum(1 for o in self.almacen if o["tipo"] == "comida")          # (prompt 62, Manel) el nivel cuenta solo la comida, no las medicinas
        else: n = sum(1 for o in self.almacen if self.cfg["objetos"][o["tipo"]].get("se_come"))
        return "lleno" if n >= A["nivel_lleno"] else "a_medias" if n >= A["nivel_a_medias"] else "poco" if n >= A["nivel_poco"] else "vacio"

    def vida_nivel(self, a):
        """(prompt 47, Manel) la vida de otra se ve en cuatro niveles, como la energía, con las bandas que ya había: sana (desde umbral_herida), herida (desde
        energia_fuerte_bajo), muy herida, y moribunda (con no más vida de la que quita un golpe: un golpe la mata). Sin la clave, None"""
        if not (self.cfg["criaturas"].get("vida_niveles") or {}).get("activo"): return None
        v = self.cuerpo[a]["vida"]; cr = self.cfg["criaturas"]
        return "sana" if v >= cr["umbral_herida"] else "herida" if v >= cr["energia_fuerte_bajo"] else "moribunda" if v <= cr["golpe_dano"] else "muy_herida"

    def energia(self, a):
        c = self.cuerpo[a]; cr = self.cfg["criaturas"]
        if c["agotada"]: return "agotada"
        return "fuerte" if c["cansancio"] < cr["energia_fuerte_bajo"] else "normal" if c["cansancio"] < cr["energia_normal_bajo"] else "cansada"

    # ── acciones válidas (para jugadores que las quieran; la de hablar no se lista) ──
    def acciones_validas(self, a):
        if a not in self.agents or self.cuerpo[a]["muerta"]: return []
        c = self.cuerpo[a]; p = self.pos[a]; out = [{"accion": "quedarse"}] + ([{"accion": "dormir"}] if self.puede_dormir(a) else [])
        tipos_bolsa = sorted({o["tipo"] for o in self.bolsa[a]})
        if not c["agotada"]:
            for d, (dx, dy) in DIRS.items():
                q = (p[0] + dx, p[1] + dy)
                if self.paso_valido(p, q) and not self.ocupada(q, a): out.append({"accion": "mover", "dir": d})
            if not self.bolsa_llena(a):
                for t in sorted({o["tipo"] for o in self.suelo.get(p, [])}): out.append({"accion": "coger", "de": "suelo", "tipo": t})
                if self.planta_junto(a, True): out.append({"accion": "coger", "de": "planta", "tipo": self.cfg["huerto"]["objeto"]})
                if self.matorral_junto(a, True): out.append({"accion": "coger", "de": "matorral", "tipo": "comida"})
                if (p in self.almacen_acceso):
                    for t in sorted({o["tipo"] for o in self.almacen}): out.append({"accion": "coger", "de": "almacen", "tipo": t})
                if self.en_casa_propia(a):
                    for t in sorted({o["tipo"] for o in self.despensa[self.casa_de[a]]}): out.append({"accion": "coger", "de": "despensa", "tipo": t})
        for t in tipos_bolsa:
            out.append({"accion": "dejar", "en": "suelo", "tipo": t})
            if (p in self.almacen_acceso): out.append({"accion": "dejar", "en": "almacen", "tipo": t})
            if self.en_casa_propia(a) and len(self.despensa[self.casa_de[a]]) < self.cfg["despensa"]["huecos"]: out.append({"accion": "dejar", "en": "despensa", "tipo": t})
            if self.cfg["objetos"][t].get("se_come") and not self.harta(a, t): out.append({"accion": "comer", "tipo": t})
        otras = [b for b in self.vivas() if b != a and self.vecinas(p, self.pos[b])]
        for b in otras:
            if len(self.bolsa[b]) < self.cfg["criaturas"]["bolsa_huecos"]:
                for t in tipos_bolsa: out.append({"accion": "dar", "a": b, "tipo": t})
            out.append({"accion": "empujar", "a": b}); out.append({"accion": "golpear", "a": b})
        for B in self.bestias_aqui():
            if self.vecinas(p, B["pos"]): out.append({"accion": "empujar", "a": B["id"]}); out.append({"accion": "golpear", "a": B["id"]})
        if self.planta_junto(a) and not c["agotada"] and self.puede_trabajar(a): out.append({"accion": "trabajar"})          # (prompt 21) agotada no se trabaja; (26) ni sin fuerzas ni de noche
        for ll in self.cfg["llamadas"]: out.append({"accion": "llamar", "llamada": ll})
        return out

    # ── daño y muerte ──
    def _dana(self, a, n, causa, herida=True):
        c = self.cuerpo[a]
        if c["muerta"]: return
        c["vida"] = max(0.0, c["vida"] - n)
        if herida: c["herida"] = min(c["herida"] + n, self.cfg["criaturas"]["vida_max"])
        if c["vida"] <= 0:
            c["muerta"] = True; c["causa"] = causa; c["turno_muerte"] = self.turno
            for o in self.bolsa[a]: self.suelo.setdefault(self.pos[a], []).append(o)        # lo que llevaba queda en el suelo
            self.bolsa[a] = []; self._ev({"muere": a, "causa": causa})
            # (v4, Manel) la muerte se anuncia a quien la tiene a la vista; el cuerpo queda en su casilla hasta el final del día
            self.cadaveres[a] = {"id": a, "pos": list(self.pos[a]), "casa": self.casa_de[a]}
            for b in self.possible_agents:
                if b != a and b in self.cuerpo and not self.cuerpo[b]["muerta"] and self._dist(self.pos[b], self.pos[a]) <= self.vista():
                    self.muertes_vistas.setdefault(b, []).append({"muere": a, "pos": list(self.pos[a]), "turno": self.turno})

    def _ev(self, e): self._eventos.append(dict(e, turno=self.turno))

    # ── step ──
    def step(self, actions):
        C = self.cfg; cr = C["criaturas"]; self._eventos = []; vivas0 = list(self.agents)
        self._oido_prev = getattr(self, "oido", {}) or {}
        self.oido = {a: [] for a in vivas0}; self.mensajes = {a: [] for a in vivas0}; self.esfuerzo = {a: 0 for a in vivas0}; self.hambre_extra = {a: 0.0 for a in vivas0}; self.muertes_vistas = {a: [] for a in vivas0}
        self._empujones = []; self._hizo = {}                               # (prompt 93) los empujones de este turno; lo que hizo de verdad cada una
        actores = list(vivas0) + [B["id"] for B in self.bestias_aqui()]; self.rng.shuffle(actores)
        reg = {}
        for x in actores:
            if x.startswith("bestia"):
                B = self.bestia_de(x)
                if B is not None: reg["__" + x + "__"] = self._actua_bestia(B)
                continue
            if self.cuerpo[x]["muerta"]: reg[x] = {"accion": None, "resultado": "muerta antes de actuar"}; continue
            acc = actions.get(x) if isinstance(actions, dict) else None
            acc = acc if isinstance(acc, dict) else {"accion": "quedarse"}
            suena = acc.get("suena") if (C.get("sonidos") or {}).get("activo") else None          # (prompt 54) la expresión: sale sola, no gasta el turno
            llama = acc.get("llama") if (C.get("llamadas_voz") or {}).get("activo") else None   # (prompt 57) una llamada con la voz, aparte de los pies
            cara_ = acc.get("cara") if (C.get("cara_v64") or {}).get("activo") else None        # (prompt 128, taller) la cara: sus tres balances, que enseña a quien la ve
            voz_ = acc.get("voz") if (C.get("voz_v64") or {}).get("activo") else None           # (prompt 128, taller) la voz de la base: sale sola del cuerpo
            if self.cuerpo[x]["agotada"] and self.cfg["criaturas"].get("agotada_se_duerme"): acc = {"accion": "dormir"}     # (prompt 23, Manel) agotada se duerme sola, como un animal
            if self.reloj() and self.cuerpo[x].get("de_un_tiron"):           # (prompt 42) el reloj del cuerpo: de noche duerme de un tirón hasta la mañana, salvo peligro
                cx = self.cuerpo[x]
                if self.fase() == "mañana": cx["de_un_tiron"] = False; cx["despierta_t"] = self.turno
                elif self._peligro(x):
                    mot = self._peligro(x); cx["de_un_tiron"] = False; self.stats.setdefault("despertares", {}); self.stats["despertares"][mot] = self.stats["despertares"].get(mot, 0) + 1
                    self._ev({"despierta": x, "por": mot})
                else: acc = {"accion": "dormir"}
            reg[x] = self._actua(x, acc); self._hizo[x] = acc.get("accion")      # (prompt 93) lo que hizo de verdad (con lo que el cuerpo le obligó: dormir)
            if isinstance(suena, dict) and suena.get("fuerza") in C["sonidos"]["fuerzas"] and suena.get("intensidad") in C["sonidos"]["alcance"]:
                alc = C["sonidos"]["alcance"][suena["intensidad"]]; p_ = self.pos[x]
                for b in self.agents:
                    if b != x and not self.cuerpo[b]["muerta"] and self._dist(p_, self.pos[b]) <= alc:
                        self.oido.setdefault(b, []).append({"de": x, "sonido": suena["fuerza"], "intensidad": suena["intensidad"], "pos": list(p_)})
                self.stats.setdefault("sonidos", {}); k_ = suena["fuerza"] + ":" + suena["intensidad"]; self.stats["sonidos"][k_] = self.stats["sonidos"].get(k_, 0) + 1
            LV = C.get("llamadas_voz") or {}
            if (C.get("dormida_sin_voz_v67") or {}).get("activo") and self.cuerpo[x].get("dormida"): llama = None      # (prompt 131, taller) dormida, la voz de antes no sale
            if isinstance(llama, dict) and llama.get("llamada") in LV.get("tipos", []) and llama.get("fuerza") in LV.get("alcance", {}) and not self.cuerpo[x]["muerta"]:
                alc = LV["alcance"][llama["fuerza"]]; p_ = self.pos[x]
                for b in self.agents:
                    if b != x and not self.cuerpo[b]["muerta"] and self._dist(p_, self.pos[b]) <= alc:
                        self.oido.setdefault(b, []).append({"de": x, "llamada": llama["llamada"], "fuerza": llama["fuerza"], "pos": list(p_)})
                cx = self.cuerpo[x]; cx["cansancio"] = min(cr["cansancio_max"], cx["cansancio"] + LV["cansancio"].get(llama["fuerza"], 0.0))     # gritar más fuerte cansa un poco
                self.stats.setdefault("llamadas_voz", {}); k_ = llama["llamada"] + ":" + llama["fuerza"]; self.stats["llamadas_voz"][k_] = self.stats["llamadas_voz"].get(k_, 0) + 1
            if isinstance(cara_, (list, tuple)) and len(cara_) == 3: self.caras[x] = [float(z) for z in cara_]      # (prompt 128) la cara de este turno
            if isinstance(voz_, dict) and voz_.get("intensidad") in LV.get("alcance", {}) and not self.cuerpo[x]["muerta"] and not self.cuerpo[x].get("dormida"):
                alc = LV["alcance"][voz_["intensidad"]]; p_ = self.pos[x]      # (prompt 128) los tres alcances de siempre; una criatura dormida no emite
                for b in self.agents:
                    if b != x and not self.cuerpo[b]["muerta"] and self._dist(p_, self.pos[b]) <= alc:
                        self.oido.setdefault(b, []).append({"de": x, "voz": voz_.get("clase"), "fila": voz_.get("fila"), "objeto": voz_.get("objeto"), "cuanto": float(voz_.get("cuanto") or 0.0),
                                                            "intensidad": voz_["intensidad"], "a": voz_.get("a"), "pos": list(p_)})
                self.stats.setdefault("voz_v64", {}); k_ = f"{voz_.get('clase')}:{voz_['intensidad']}"; self.stats["voz_v64"][k_] = self.stats["voz_v64"].get(k_, 0) + 1
        if self._G(): self._g_turno()                                      # (prompt 88) pieza G: echar, matar, volver
        # cuerpo
        for a in vivas0:
            c = self.cuerpo[a]
            if c["muerta"]: continue
            if self.pos[a] not in self.aldea: d_ = self.stats["fuera_aldea"].setdefault(a, {}); d_[self.dia] = d_.get(self.dia, 0) + 1
            hr = cr.get("hambre_reloj") or {}; fh = 1.0                       # (prompt 43) el reloj del hambre: dormida gasta menos; al anochecer, el apetito de la cena
            if hr.get("activo"): fh = hr["dormida"] if c.get("dormida") else (hr["apetito"] if self.fase() == hr["apetito_fase"] else 1.0)
            Tc = self.cfg.get("temperatura") or {}
            if Tc.get("activo") and Tc.get("frio_hambre_por_grado"):          # (prompt 55, Manel) el frío cuesta en el cuerpo: fuera, bajo la zona cómoda, el hambre sube más
                fr = max(0.0, Tc["confort"][0] - self.temperatura(self.pos[a]))
                if fr > 0: fh *= 1.0 + Tc["frio_hambre_por_grado"] * fr; self.stats["hambre_frio"] = self.stats.get("hambre_frio", 0.0) + cr["hambre_por_turno"] * fh * (1.0 - 1.0 / (1.0 + Tc["frio_hambre_por_grado"] * fr))
            self.stats["hambre_base"] = self.stats.get("hambre_base", 0.0) + cr["hambre_por_turno"] * fh; self.stats["criatura_turnos"] = self.stats.get("criatura_turnos", 0) + 1
            c["hambre"] = min(cr["hambre_max"], c["hambre"] + cr["hambre_por_turno"] * fh + cr["hambre_por_esfuerzo"] * self.esfuerzo[a] + self.hambre_extra[a])
            if c["hambre"] >= cr["hambre_max"]: self._dana(a, cr["vida_por_turno_con_hambre_max"], "hambre", herida=False)
            if not c["muerta"] and self.terreno(self.pos[a]) == "salvaje" and self.rng.random() < C["terreno_salvaje"]["prob_herida"]:
                self._dana(a, C["terreno_salvaje"]["dano"], "terreno"); self._ev({"terreno_hiere": a})
            if not c.get("dormida") and cr.get("cansancio_por_turno_despierta"):          # (prompt 22, Manel) el cansancio sube durante el día: despierta, cada turno
                c["cansancio"] = min(cr["cansancio_max"], c["cansancio"] + cr["cansancio_por_turno_despierta"])
            if c["cansancio"] >= cr["cansancio_max"]: c["cansancio"] = cr["cansancio_max"]; c["agotada"] = True
            elif c["agotada"] and c["cansancio"] <= cr["agotada_hasta"]: c["agotada"] = False
        self._mundo_avanza()
        if (C.get("observacion") or {}).get("empujones_vistos"):           # (prompt 93, Manel) los empujones que se ven, como las muertes vistas (apagado por defecto)
            self.empujones_vistos = {a: [] for a in vivas0}
            for e in self._empujones:
                if e["gana"] is None: continue
                for y in vivas0:
                    if not self.cuerpo[y]["muerta"] and min(self._dist(self.pos[y], tuple(q)) for q in e["pos"]) <= self.vista(): self.empujones_vistos[y].append(dict(e))
        self.turno += 1
        # fin de día: el cuadre de lo que aparece, se come, se pudre o come la bestia
        if self.turno % self.dia_turnos == 0:
            fila = {"dia": self.dia}
            for t in self.tipos_objeto:
                L = self.libro.get(self.dia, {}).get(t, {}); fin = self._existencias(t)
                esperado = self.stock_inicio_dia[t] + L.get("aparece", 0) - L.get("comido", 0) - L.get("podrido", 0) - L.get("comido_bestia", 0)
                fila[t] = {"inicio": self.stock_inicio_dia[t], **L, "fin": fin, "cuadra": fin == esperado}
            self.cuadre.append(fila); self.stats["almacen_fin_dia"].append({"dia": self.dia, "comida": sum(1 for o in self.almacen if o["tipo"] == "comida"), "nivel": self.nivel_almacen()})
            self.stock_inicio_dia = {t: self._existencias(t) for t in self.tipos_objeto}
            if self._G(): self._g_dia()                                    # (prompt 88) pieza G: la cría y las épocas
            self.dia += 1; self._plan_dia()
            # los cuerpos se quedan hasta el final del día; (prompt 31, Manel) con `cadaver_dias_extra`, hasta el final de tantos días más
            extra = int(cr.get("cadaver_dias_extra") or 0)
            self.cadaveres = {k: v for k, v in self.cadaveres.items() if self.cuerpo[k]["turno_muerte"] // self.dia_turnos + extra >= self.dia}
        terminated = {a: self.cuerpo[a]["muerta"] for a in vivas0}
        fin = self.turno >= self.max_turnos
        truncated = {a: (fin and not terminated[a]) for a in vivas0}
        obs = {a: self._observa(a) for a in vivas0}
        rewards = {a: 0 for a in vivas0}
        self.agents = [a for a in vivas0 if not terminated[a] and not truncated[a]]
        infos = {a: {"acciones_validas": self.acciones_validas(a) if a in self.agents else [], "causa_muerte": self.cuerpo[a]["causa"]} for a in vivas0}
        if self._f:
            linea = {"turno": self.turno - 1, "dia": (self.turno - 1) // self.dia_turnos, "fase": self.fase(self.turno - 1), "orden": actores,
                     "agentes": {a: dict(reg.get(a, {}), pos=list(self.pos[a]), cuerpo={k: (round(v, 3) if isinstance(v, float) else v) for k, v in self.cuerpo[a].items()},
                                         bolsa=[o["tipo"] for o in self.bolsa[a]], **({"bolsa_origen": [o.get("origen") for o in self.bolsa[a]]} if self._sabores() else {})) for a in vivas0},
                     "bestia": dict(reg.get("__bestia__", {}), pos=list(self.bestia["pos"]) if self.bestia["pos"] is not None else None, lleva=[o["tipo"] for o, _ in self.bestia["lleva"]], modo=self.bestia["modo"]),
                     "eventos": self._eventos}
            if self.arboles: linea["arboles"] = [[c[0], c[1], len((self.matorrales.get(c) or {}).get("frutos", [])) if T_["activo"] else None] for c, T_ in sorted(self.arboles.items())]      # (prompt 96)
            if self._G(): linea["bestias"] = [dict(reg.get("__" + B["id"] + "__", {}), id=B["id"], pos=list(B["pos"]) if B["pos"] is not None else None, lleva=[o["tipo"] for o, _ in B["lleva"]], modo=B["modo"],
                                                   **({"vida": round(B["vida"], 3)} if "vida" in B else {})) for B in self.bestias]
            if self.temperatura() is not None: linea["temperatura_fuera"] = self.temperatura()          # (prompt 34) para el visor
            if self.cadaveres: linea["cadaveres"] = [[c["id"], c["pos"][0], c["pos"][1]] for c in self.cadaveres.values()]      # (prompt 31) para el visor
            if self.objetos_cada and (self.turno - 1) % self.objetos_cada == 0:
                linea["objetos"] = {"suelo": [[q[0], q[1], "baya" if o.get("suelta") else o["tipo"]] for q, L in sorted(self.suelo.items()) for o in L],
                                    "plantas": [[q[0], q[1], len(P["frutos"])] for q, P in sorted(self.plantas.items())],
                                    "matorrales": [[q[0], q[1], len(Mt["frutos"]), Mt["zona"]] for q, Mt in sorted(self.matorrales.items())]}
            self._f.write(json.dumps(linea, ensure_ascii=False) + "\n")
            if not self.agents: self._f.close(); self._f = None
        return obs, rewards, terminated, truncated, infos

    def _actua(self, a, acc):
        C = self.cfg; cr = C["criaturas"]; c = self.cuerpo[a]; p = self.pos[a]; t = acc.get("accion"); out = {"accion": t}
        c["dormida"] = False                                     # (prompt 22) dormida solo el turno que duerme
        objetivo = acc.get("a"); out["objetivo"] = objetivo
        def falla(m): out["resultado"] = "no: " + m; return out
        if t == "mover":
            if c["agotada"]: return falla("agotada")
            d = DIRS.get(acc.get("dir")); out["dir"] = acc.get("dir")
            if not d: return falla("direccion")
            q = (p[0] + d[0], p[1] + d[1])
            if not self.paso_valido(p, q): return falla("no se puede pasar")
            if self.ocupada(q, a): return falla("ocupada")
            if self.reloj() and self.turno - c.get("despierta_t", -10 ** 9) < cr["reloj"]["despertar_lento_turnos"] and c.get("movio_t") == self.turno - 1:
                return falla("despertando")                                # (prompt 42) al despertar, poco a poco: un paso cada dos turnos
            self.pos[a] = q; self.esfuerzo[a] += 1; c["movio_t"] = self.turno
            c["cansancio"] = min(cr["cansancio_max"], c["cansancio"] + cr["cansancio_por_esfuerzo"] * (cr["factor_bolsa_llena"] if self.bolsa_llena(a) else 1.0))
            out["resultado"] = "ok"; return out
        if t == "quedarse": c["cansancio"] = max(0.0, c["cansancio"] + cr["cansancio_quieta"]); out["resultado"] = "ok"; return out
        if t == "dormir":
            if not self.puede_dormir(a): return falla("sin sueño")
            f_dia = cr.get("dormir_de_dia_factor", 1.0) if self.fase() in ("mañana", "tarde") else 1.0      # (prompt 24, Manel) de día, dormir recupera la mitad
            c["cansancio"] = max(0.0, c["cansancio"] + cr["cansancio_dormir"] * f_dia); out["resultado"] = "ok"; c["dormida"] = True
            if self.reloj() and self.fase() in ("anochecer", "noche"):
                if not c.get("de_un_tiron"):                                # (prompt 43) ¿cenó? come en el rato antes de dormirse (lo que dura el anochecer)
                    self.stats["noches_dormidas"] = self.stats.get("noches_dormidas", 0) + 1
                    rato = dict(self.cfg["dia"]["fases"]).get("anochecer", 0)
                    if self.turno - c.get("comio_t", -10 ** 9) <= rato: self.stats["cenas"] = self.stats.get("cenas", 0) + 1
                c["de_un_tiron"] = True                                     # (prompt 42) de noche, el sueño entra y sigue
            if c["hambre"] <= cr.get("hambre_max_para_recuperar", -1) and c["vida"] < cr["vida_max"]:        # durmiendo, la vida sube despacio (por cualquier causa)
                g = min(cr.get("vida_por_turno_durmiendo", 0.0), cr["vida_max"] - c["vida"]); c["vida"] += g; c["herida"] = max(0.0, c["herida"] - g)
            return out
        if t == "coger":
            if c["agotada"]: return falla("agotada")
            if self.bolsa_llena(a): return falla("bolsa llena")
            de = acc.get("de", "suelo"); tipo = acc.get("tipo"); out["de"] = de
            def saca(L):
                for i, o in enumerate(L):
                    if tipo is None or o["tipo"] == tipo: return L.pop(i)
            o = None
            if de == "suelo": o = saca(self.suelo.get(p, []))
            elif de == "planta":
                ps = self.planta_junto(a, True)
                if ps: o = saca(self.plantas[ps[0]]["frutos"])
            elif de == "matorral":
                ms = self.matorral_junto(a, True)
                if ms: o = saca(self.matorrales[ms[0]]["frutos"])
            elif de == "almacen" and (p in self.almacen_acceso):
                o = saca(self.almacen)
                if o and C["almacen"]["libreta"]: self.libreta.append({"turno": self.turno, "quien": a, "coge": o["tipo"]})
            elif de == "despensa" and self.en_casa_propia(a): o = saca(self.despensa[self.casa_de[a]])
            if o is None: return falla("no hay")
            self.bolsa[a].append(o); out["resultado"] = "ok"; out["tipo"] = o["tipo"]; return out
        if t == "dejar":
            en = acc.get("en", "suelo"); tipo = acc.get("tipo"); out["en"] = en
            i = next((i for i, o in enumerate(self.bolsa[a]) if tipo is None or o["tipo"] == tipo), None)
            if i is None: return falla("no lo lleva")
            if en == "suelo": self.suelo.setdefault(p, []).append(self.bolsa[a].pop(i))
            elif en == "almacen" and (p in self.almacen_acceso):
                o = self.bolsa[a].pop(i); self.almacen.append(o)
                if C["almacen"]["libreta"]: self.libreta.append({"turno": self.turno, "quien": a, "deja": o["tipo"]})
            elif en == "despensa" and self.en_casa_propia(a) and len(self.despensa[self.casa_de[a]]) < C["despensa"]["huecos"]: self.despensa[self.casa_de[a]].append(self.bolsa[a].pop(i))
            else: return falla("ahi no")
            out["resultado"] = "ok"; out["tipo"] = tipo; return out
        if t == "comer":
            tipo = acc.get("tipo"); org = acc.get("origen") if self._sabores() else None
            i = next((i for i, o in enumerate(self.bolsa[a]) if (tipo is None or o["tipo"] == tipo) and C["objetos"][o["tipo"]].get("se_come") and (org is None or o.get("origen") == org)), None)
            if i is None: return falla("nada que comer")
            if self.harta(a, self.bolsa[a][i]["tipo"]): return falla("harta: ya no le entra más")
            o = self.bolsa[a].pop(i); P = C["objetos"][o["tipo"]]
            n_ = P.get("nutricion", 0)
            if (cr.get("hambre_bajo_cero") or {}).get("activo"): c["hambre"] = c["hambre"] - n_      # (prompt 52, Manel) el hambre puede bajar de cero: lo que sobra no se pierde
            else: c["hambre"] = max(0.0, c["hambre"] - n_)
            cura = min(P.get("cura", 0), c["herida"]); c["herida"] -= cura; c["vida"] = min(cr["vida_max"], c["vida"] + cura)
            if P.get("nutricion", 0) > 0: c["comio_t"] = self.turno
            self._cuenta(o["tipo"], "comido"); out["resultado"] = "ok"; out["tipo"] = o["tipo"]
            if self._sabores(): out["origen"] = o.get("origen")
            return out
        if t == "dar":
            b = objetivo
            if b not in self.agents or self.cuerpo[b]["muerta"] or not self.vecinas(p, self.pos[b]): return falla("no está pegada")
            if self.bolsa_llena(b): return falla("su bolsa está llena")
            tipo = acc.get("tipo"); org = acc.get("origen") if self._sabores() else None
            i = next((i for i, o in enumerate(self.bolsa[a]) if (tipo is None or o["tipo"] == tipo) and (org is None or o.get("origen") == org)), None)
            if i is None: return falla("no lo lleva")
            o = self.bolsa[a].pop(i); self.bolsa[b].append(o); out["resultado"] = "ok"; out["tipo"] = o["tipo"]
            if self._sabores(): out["origen"] = o.get("origen")
            return out
        if t == "trabajar":
            ps = self.planta_junto(a)
            if acc.get("planta") is not None and tuple(acc["planta"]) in ps: ps = [tuple(acc["planta"])]
            if not ps: return falla("ninguna planta al lado")
            if c["agotada"]: return falla("agotada")                     # (prompt 21, Manel) como andar o coger
            if not self.puede_trabajar(a): return falla("sin fuerzas" if c["hambre"] >= cr["hambre_max"] else "de noche")
            # (prompt 14, Manel) trabajar cuesta un poco más que andar: sus propias claves; sin ellas, como un paso (v5)
            ht, ct = cr.get("hambre_por_trabajo"), cr.get("cansancio_por_trabajo")
            self.plantas[ps[0]]["trabajo"] += 1
            if "cuidado" in self.plantas[ps[0]]: self.plantas[ps[0]]["cuidado"] = min(1.0, self.plantas[ps[0]]["cuidado"] + 1.0 / self.cfg["huerto"]["trabajo_necesario"])
            if ht is None: self.esfuerzo[a] += 1
            else: self.hambre_extra[a] += ht
            d_ = self.stats["trabajo"].setdefault(a, {}); d_[self.dia] = d_.get(self.dia, 0) + 1
            hh = self.huerto_de[ps[0]]; self.stats["trabajo_por_huerto"][hh] = self.stats["trabajo_por_huerto"].get(hh, 0) + 1
            c["cansancio"] = min(cr["cansancio_max"], c["cansancio"] + (cr["cansancio_por_esfuerzo"] if ct is None else ct)); out["resultado"] = "ok"; out["planta"] = list(ps[0]); return out
        if t == "empujar": return self._empuja(a, objetivo, out)
        if t == "golpear":
            if isinstance(objetivo, str) and objetivo.startswith("bestia"):
                B = self.bestia_de(objetivo)
                if B is None or not self.vecinas(p, B["pos"]): return falla("no está pegada")
                c["cansancio"] = min(cr["cansancio_max"], c["cansancio"] + cr["golpe_cansancio"])
                if self._G(): self._g_golpes.setdefault(B["id"], {"golpe": set(), "empuje": set()})["golpe"].add(a)      # (prompt 88) le pegan a la vez
                self._bestia_pega(a, "devuelve el golpe", B); out["resultado"] = "la bestia devuelve el golpe"; return out
            b = objetivo
            if b not in self.agents or self.cuerpo[b]["muerta"] or not self.vecinas(p, self.pos[b]): return falla("no está pegada")
            c["cansancio"] = min(cr["cansancio_max"], c["cansancio"] + cr["golpe_cansancio"])
            self.cuerpo[b]["golpe_t"] = self.turno; self._dana(b, cr["golpe_dano"], "golpe de " + a); out["resultado"] = "ok"; return out
        if t == "llamar":
            ll = acc.get("llamada")
            if ll not in C["llamadas"]: return falla("llamada desconocida")
            for b in self.agents:
                if b != a and not self.cuerpo[b]["muerta"] and self._dist(p, self.pos[b]) <= cr["llamada_alcance"]: self.oido[b].append({"de": a, "llamada": ll, "pos": list(p)})
            out["resultado"] = "ok"; out["llamada"] = ll; return out
        if t == "hablar":
            texto = str(acc.get("texto", ""))[:500]; oyen = []
            for b in self.agents:
                if b != a and not self.cuerpo[b]["muerta"] and self._dist(p, self.pos[b]) <= cr["hablar_alcance"]: self.mensajes[b].append({"de": a, "texto": texto}); oyen.append(b)
            out["resultado"] = "ok"; out["texto"] = texto; out["oyen"] = oyen; return out
        return falla("acción desconocida")

    def _dist(self, a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    # ── empujar ──
    def _empuja(self, a, b, out):
        C = self.cfg; cr = C["criaturas"]; p = self.pos[a]
        def falla(m): out["resultado"] = "no: " + m; return out
        if isinstance(b, str) and b.startswith("bestia"):
            B = self.bestia_de(b)
            if B is None or not self.vecinas(p, B["pos"]): return falla("no está pegada")
            n = sum(1 for x in self.vivas() if self.vecinas(self.pos[x], B["pos"]))
            self.cuerpo[a]["cansancio"] = min(cr["cansancio_max"], self.cuerpo[a]["cansancio"] + cr["empujar_cansancio"])
            gana = n >= C["bestia"]["peso_empuje"]
            if self._G(): self._g_golpes.setdefault(B["id"], {"golpe": set(), "empuje": set()})["empuje"].add(a)      # (prompt 88) la empujan a la vez
            if gana and B["lleva"]:
                for o, _ in B["lleva"]: self._recibe(a, o)
                self._ev({"bestia_suelta": [o["tipo"] for o, _ in B["lleva"]], "a": a, "criaturas": n}); B["lleva"] = []
            out["resultado"] = ("gana" if gana else "pierde") + f" ({n} contra {C['bestia']['peso_empuje']})"
            if not gana or C["bestia"].get("pega_si_gana_el_empujon", True): self._bestia_pega(a, "se resiste", B)      # si gana, ese turno no pega: pueden huir
            return out
        if b not in self.agents or self.cuerpo[b]["muerta"] or not self.vecinas(p, self.pos[b]): return falla("no está pegada")
        escena = [p, self.pos[b]]
        def bando(x):                                      # ella más las de su misma casa pegadas a la escena (a quien empuja o a quien recibe)
            return 1 + sum(1 for y in self.vivas() if y not in (a, b) and self.casa_de[y] == self.casa_de[x] and any(self.vecinas(self.pos[y], e) for e in escena))
        self.cuerpo[b]["empujon_t"] = self.turno                           # (prompt 42) un empujón despierta
        na, nb = bando(a), bando(b)
        for x in (a, b): self.cuerpo[x]["cansancio"] = min(cr["cansancio_max"], self.cuerpo[x]["cansancio"] + cr["empujar_cansancio"])
        if na != nb: ganador = a if na > nb else b
        else:
            ca, cb = self.cuerpo[a]["cansancio"], self.cuerpo[b]["cansancio"]
            ganador = a if ca < cb else b if cb < ca else None
        out["bandos"] = [na, nb]
        if ganador is None: out["resultado"] = "empate: nada"; return out
        perdedor = b if ganador == a else a
        soltado = list(self.bolsa[perdedor]); self.bolsa[perdedor] = []
        for o in soltado:
            if len(self.bolsa[ganador]) < cr["bolsa_huecos"]: self.bolsa[ganador].append(o)
            else: self.suelo.setdefault(self.pos[perdedor], []).append(o)
        out["resultado"] = f"gana {ganador}"; out["soltado"] = [o["tipo"] for o in soltado]
        self._ev({"empujon": a, "a": b, "gana": ganador, "bandos": [na, nb], "soltado": out["soltado"]})
        self._empujones.append({"de": a, "a": b, "gana": ganador, "soltado": list(out["soltado"]), "pos": [list(p), list(self.pos[b])], "turno": self.turno})
        return out

    def _recibe(self, a, o):
        if len(self.bolsa[a]) < self.cfg["criaturas"]["bolsa_huecos"]: self.bolsa[a].append(o)
        else: self.suelo.setdefault(self.pos[a], []).append(o)

    # ── la bestia ──
    def _bestia_pega(self, a, por, B=None):
        B = self.bestia if B is None else B
        self.cuerpo[a]["golpe_t"] = self.turno                             # (prompt 42) un golpe despierta
        self._dana(a, self.cfg["bestia"]["golpe_dano"], "bestia"); B["espera"][a] = self.turno + self.cfg["bestia"]["espera_tras_encuentro"]
        self._ev(dict({"bestia_pega": a, "por": por}, **({"bestia": B["id"]} if B is not self.bestia else {}))); self.stats["bestia_pega"] += 1

    def _dist_bestia(self, desde):
        D = {desde: 0}; q = deque([desde])
        while q:
            u = q.popleft()
            for d in DIRS.values():
                v = (u[0] + d[0], u[1] + d[1])
                if v not in D and v in self.paso_bestia: D[v] = D[u] + 1; q.append(v)
        return D

    def _bfs_bestia(self, desde, meta):
        if desde == meta: return desde
        prev = {desde: None}; q = deque([desde])
        while q:
            u = q.popleft()
            for d in DIRS.values():
                v = (u[0] + d[0], u[1] + d[1])
                if v in prev or v not in self.paso_bestia: continue
                if v != meta and self.ocupada(v, "bestia"): continue
                prev[v] = u
                if v == meta:
                    while prev[v] != desde: v = prev[v]
                    return v
                q.append(v)
        return None

    def _actua_bestia(self, B=None):
        B = self.bestia if B is None else B; C = self.cfg["bestia"]; fase = self.fase(); r = self.turno % self.dia_turnos; out = {}
        if self.arboles:                                                    # (prompt 96) al anochecer y de noche, la bestia más cercana a un árbol activo va hacia él
            ar = self._arbol_de_bestia(B)
            if ar is not None:
                if B["modo"] != "arbol": self.stats_arbol["bestia_va"] += 1; B["camino"] = None; B["ruta"] = []
                B["modo"] = "arbol"; B["arbol"] = list(ar); p = B["pos"]
                if self._dist(p, ar) > 1:
                    paso = self._bfs_bestia(p, ar)
                    if paso and paso != ar and not self.ocupada(paso, "bestia"): B["pos"] = paso
                    out["accion"] = "va al árbol"
                else: out["accion"] = "junto al árbol"
                self._encuentros(B); return out
            if B["modo"] == "arbol": B["modo"] = "ronda"; B.pop("arbol", None)
        ini_noche = sum(n for nom, n in self.cfg["dia"]["fases"] if nom != "noche"); man = C["mandos"][C["mando"]]
        if r == ini_noche and B["modo"] == "ronda":                                     # empieza la noche: ¿baja?
            if self.rng.random() < man["prob_bajar"]:
                if C.get("camino") == "mas_cercano":          # el camino cuya entrada está más cerca de ella (por donde puede andar); empate, a suertes
                    D = self._dist_bestia(B["pos"]); ds = {k: D.get(v, 10 ** 9) for k, v in self.entrada_camino.items()}; m = min(ds.values())
                    cam = self.rng.choice(sorted(k for k, v in ds.items() if v == m))
                else: cam = self.rng.choice(sorted(self.entrada_camino))
                B["camino"] = cam
                ruta = [self.entrada_camino[cam], self.borde_aldea[cam]]
                if man["alcance"] == "plaza": ruta.append(min(self.almacen_acceso - set(self.plantas_pos), key=lambda q: (self._dist(q, self.borde_aldea[cam]), q)))
                if man["alcance"] in ("huerto", "plaza"): ruta.append("huerto")
                B["ruta"] = ruta; B["modo"] = "baja"; B["comidas_noche"] = 0; out["decide"] = f"baja por el camino {cam}"
        bd = C.get("de_dia") or {}
        if bd.get("activo") and fase == "mañana" and B["modo"] == "ronda" and B.get("dia_decidido") != self.dia:      # (prompt 68, Manel) mando de estrés: la bestia de día
            B["dia_decidido"] = self.dia
            if self.rng.random() < float(bd["prob_bajar"]):
                D = self._dist_bestia(B["pos"]); ds = {k: D.get(v, 10 ** 9) for k, v in self.entrada_camino.items()}; m = min(ds.values())
                cam = self.rng.choice(sorted(k for k, v in ds.items() if v == m)) if C.get("camino") == "mas_cercano" else self.rng.choice(sorted(self.entrada_camino))
                B["camino"] = cam; ruta = [self.entrada_camino[cam], self.borde_aldea[cam]]
                if man["alcance"] in ("huerto", "plaza"): ruta.append("huerto")
                B["ruta"] = ruta; B["modo"] = "baja"; B["comidas_noche"] = 0; B["de_dia"] = True; out["decide"] = f"baja de día por el camino {cam}"
        if B.get("de_dia") and fase == "anochecer" and B["modo"] == "baja": B["modo"] = "vuelve"; B["ruta"] = [self.entrada_camino[B["camino"]]]; B["de_dia"] = False
        if fase == "mañana" and B["modo"] == "baja" and not B.get("de_dia"): B["modo"] = "vuelve"; B["ruta"] = [self.entrada_camino[B["camino"]]]
        p = B["pos"]
        # comer del huerto
        if B["modo"] == "baja" and B["ruta"] and B["ruta"][0] == "huerto":
            tope = C.get("max_frutos_por_noche"); resto = (tope - B.get("comidas_noche", 0)) if tope is not None else 10 ** 9
            junto = [q for q in self.plantas_pos if self.junto_o_en(p, q) and self.plantas[q]["frutos"]]
            if junto and resto > 0:                       # come como mucho el tope de frutas por noche
                q = sorted(junto)[0]; come = self.plantas[q]["frutos"][:resto]; self.plantas[q]["frutos"] = self.plantas[q]["frutos"][len(come):]
                for o in come: self._cuenta(o["tipo"], "comido_bestia")
                n = len(come); B["comidas_noche"] = B.get("comidas_noche", 0) + n
                out["accion"] = "come del huerto"; self.stats["bestia_come_huerto"] += n; out["planta"] = list(q); out["n"] = n
                self._encuentros(B); return out
            conf = [q for q in self.plantas_pos if self.plantas[q]["frutos"]]
            if not conf or resto <= 0: B["ruta"] = []
            else:
                meta = min(conf, key=lambda q: (self._dist(p, q), q)); paso = self._bfs_bestia(p, meta)
                if paso and paso != meta: B["pos"] = paso
                out["accion"] = "va a una planta"; self._encuentros(B); return out
        if B["modo"] in ("baja", "vuelve"):
            while B["ruta"] and B["ruta"][0] != "huerto" and B["ruta"][0] == p: B["ruta"].pop(0)
            if not B["ruta"]:
                if B["modo"] == "baja": B["modo"] = "vuelve"; B["ruta"] = [self.entrada_camino[B["camino"]]]
                else: B["modo"] = "ronda"; B["camino"] = None
            if B["ruta"] and B["ruta"][0] != "huerto":
                paso = self._bfs_bestia(p, B["ruta"][0])
                if paso and not self.ocupada(paso, "bestia"): B["pos"] = paso
                out["accion"] = B["modo"]
        if B["modo"] == "ronda":                                                          # de día y de vuelta: ronda la zona salvaje
            ops = [(p[0] + d[0], p[1] + d[1]) for d in DIRS.values()]
            ops = [q for q in ops if self.dentro(q) and self.terreno(q) in ("salvaje", "camino") and self.en_anillo(q) and not self.ocupada(q, "bestia")]
            if ops: B["pos"] = ops[self.rng.randrange(len(ops))]
            out["accion"] = "ronda"
        self._encuentros(B); return out

    def _encuentros(self, B=None):
        B = self.bestia if B is None else B; p = B["pos"]; noche = B["modo"] in ("baja", "vuelve", "arbol")
        cerca = [a for a in self.vivas() if self.vecinas(p, self.pos[a]) and self.celda_casa.get(self.pos[a]) is None
                 and (noche or self.en_anillo(self.pos[a])) and B["espera"].get(a, -1) <= self.turno]
        if not cerca: return
        a = sorted(cerca)[self.rng.randrange(len(cerca))]
        dormida = bool(self.cfg["bestia"].get("pega_y_roba_dormida") and self.cuerpo[a].get("dormida"))     # (prompt 22) dormida fuera: le pega y le roba
        if self.bolsa[a]:
            dulces = [o for o in self.bolsa[a] if o.get("origen") == "dulce"] if B["modo"] == "arbol" else []
            if dulces:                                                      # (prompt 96) en el árbol, la fruta dulce antes que cualquier otra cosa
                robado = dulces; self.bolsa[a] = [o for o in self.bolsa[a] if o.get("origen") != "dulce"]; self.stats_arbol["roba_dulce"] += 1
            else: robado = self.bolsa[a]; self.bolsa[a] = []
            for o in robado: B["lleva"].append((o, self.turno))
            B["espera"][a] = self.turno + self.cfg["bestia"]["espera_tras_encuentro"]
            self._ev(dict({"bestia_roba": a, "que": [o["tipo"] for o in robado]}, **({"bestia": B["id"]} if B is not self.bestia else {}))); self.stats["bestia_roba"] += 1
            if dormida: self._bestia_pega(a, "dormida", B)
        else: self._bestia_pega(a, "dormida" if dormida else "no lleva nada", B)

    # ── el mundo avanza: pudrirse, aparecer, el huerto, la bestia digiere ──
    def _mundo_avanza(self):
        O = self.cfg["objetos"]
        if self.arboles: self._arboles_avanza()                             # (prompt 96)
        def pudre(L, donde, sitio=None):
            quedan = []
            for o in L:
                P = O[o["tipo"]]; n = (P.get("pudre_en") or {}).get(donde) if P.get("se_pudre") else None
                if n: o["pudricion"] += 1.0 / n
                if o["pudricion"] >= 1.0 - 1e-9:                # (la suma de n veces 1/n puede quedarse en 0,99999…: sin esto, se pudría un turno tarde)
                    self._cuenta(o["tipo"], "podrido"); k_ = f"{o['tipo']}:{sitio or donde}"; self.stats["podrido_por_sitio"][k_] = self.stats["podrido_por_sitio"].get(k_, 0) + 1
                else: quedan.append(o)
            return quedan
        for k in list(self.suelo):
            self.suelo[k] = pudre(self.suelo[k], "suelo", "suelo_" + self.terreno(k))
            if not self.suelo[k]: del self.suelo[k]
        for a in self.bolsa: self.bolsa[a] = pudre(self.bolsa[a], "bolsa")
        for h in self.despensa: self.despensa[h] = pudre(self.despensa[h], "despensa")
        self.almacen = pudre(self.almacen, "almacen")
        for q, P in self.plantas.items(): P["frutos"] = pudre(P["frutos"], "planta")
        for q, Mt in self.matorrales.items():
            if Mt["zona"] != "arbol": Mt["frutos"] = pudre(Mt["frutos"], "matorral", "matorral_" + Mt["zona"])      # (prompt 96) la fruta del árbol no se pudre en él
        # la bestia se come lo robado al cabo de un rato
        tras = self.cfg["bestia"]["come_lo_robado_tras"]
        for B in self.bestias:
            quedan = []
            for o, t0 in B["lleva"]:
                if self.turno - t0 >= tras: self._cuenta(o["tipo"], "comido_bestia")
                else: quedan.append((o, t0))
            B["lleva"] = quedan
        # el huerto
        H = self.cfg["huerto"]
        for q, P in self.plantas.items():
            if "cuidado" in P:                                  # (prompt 18) el cuidado baja despacio sin trabajo
                P["cuidado"] *= self.cuidado_baja
            if self.turno + 1 >= P["fin"] and "cuidado" in P:    # el fruto crece con el cuidado: sin cuidado, como una casilla de bosque
                x = self.frutos_sin_cuidado + (H["frutos"] * self.rendimiento[self.huerto_de[q]] - self.frutos_sin_cuidado) * P["cuidado"]
                x *= self.factor_epoca(huerto=True)                       # (prompt 30) la época también en el huerto
                k = int(x) + (1 if self.rng.random() < x - int(x) else 0)
                for _ in range(k):
                    o_ = self._nuevo(H["objeto"]); self._cuenta(H["objeto"], "aparece")
                    if self._sabores(): o_["origen"] = "huerto"
                    P["frutos"].append(o_)
                if k: self._ev({"da_fruto": list(q), "trabajo": P["trabajo"], "cuidado": round(P["cuidado"], 3), "frutos": k})
                P["trabajo"] = 0; P["fin"] += H["ciclo_turnos"]
            elif self.turno + 1 >= P["fin"]:
                if P["trabajo"] >= H["trabajo_necesario"]:
                    for _ in range(int(round(H["frutos"] * self.rendimiento[self.huerto_de[q]]))):
                        o_ = self._nuevo(H["objeto"]); self._cuenta(H["objeto"], "aparece")
                        if self._sabores(): o_["origen"] = "huerto"
                        P["frutos"].append(o_)
                    self._ev({"da_fruto": list(q), "trabajo": P["trabajo"]})
                P["trabajo"] = 0; P["fin"] += H["ciclo_turnos"]
        # (prompt 19) los matorrales dan fruto; (prompt 20) según la época (mando apagado por defecto), y una parte cae como baya suelta en el bosque
        sueltas = float((self.mat_cfg or {}).get("bayas_sueltas") or 0.0)
        factor = self.factor_epoca() if ((self.mat_cfg or {}).get("epocas") or {}).get("activo") else None
        for q, Mt in self.matorrales.items():
            if Mt["zona"] == "arbol": continue                              # (prompt 96) el árbol no vuelve a dar fruto
            if self.turno + 1 >= Mt["fin"]:
                k = self.mat_cfg[Mt["zona"]]["frutos"]
                if factor is not None: x = k * factor; k = int(x) + (1 if self.rng.random() < x - int(x) else 0)
                for _ in range(k):
                    o = self._nuevo("comida"); self._cuenta("comida", "aparece")
                    if self._sabores(): o["origen"] = "bosque"
                    if sueltas > 0 and self.rng.random() < sueltas:          # baya suelta: a una casilla al azar del bosque, sin matorral; se pudre como la comida del suelo
                        c = self.celdas_bosque[self.rng.randrange(len(self.celdas_bosque))]; o["suelta"] = True
                        self.suelo.setdefault(c, []).append(o); self._ev({"baya_suelta": list(c)})
                    else: Mt["frutos"].append(o)
                Mt["fin"] += self.mat_cfg[Mt["zona"]]["fruto_cada"]
        # apariciones de hoy
        for zona, tipo in self.apariciones.get(self.turno % self.dia_turnos, []):
            celdas = self.celdas_bosque if zona == "bosque" else self.celdas_salvaje
            tope = O[tipo].get("tope_en_el_suelo")                  # (prompt 31, Manel) que no se acumule sin fin: con tantas en el suelo de la zona, hoy no aparece
            if tope is not None:
                zc = self._zona_set.get(zona) or self._zona_set.setdefault(zona, set(celdas))
                if sum(1 for q, L in self.suelo.items() if q in zc for o in L if o["tipo"] == tipo) >= tope:
                    self._cuenta(tipo, "no_aparece_tope"); continue
            for _ in range(50):
                c = celdas[self.rng.randrange(len(celdas))]
                if not self.ocupada(c): break
            self.suelo.setdefault(c, []).append(self._nuevo(tipo)); self._cuenta(tipo, "aparece"); self._ev({"aparece": tipo, "en": list(c), "zona": zona})

    # ── observación ──
    def _observa(self, a):
        C = self.cfg; cr = C["criaturas"]; c = self.cuerpo[a]; p = self.pos[a]; v = self.vista()
        cas = []
        for y in range(p[1] - v, p[1] + v + 1):
            for x in range(p[0] - v, p[0] + v + 1):
                q = (x, y)
                if not self.dentro(q): continue
                d = {"pos": [x, y], "terreno": self.terreno(q)}
                if self.suelo.get(q):
                    d["objetos"] = [o["tipo"] for o in self.suelo[q]]
                    if self._sabores(): d["objetos_origen"] = [o.get("origen") for o in self.suelo[q]]
                if q in self.plantas:
                    d["planta"] = {"frutos": len(self.plantas[q]["frutos"]), "trabajo": self.plantas[q]["trabajo"]}
                    if "cuidado" in self.plantas[q]: d["planta"]["cuidado"] = round(self.plantas[q]["cuidado"], 2)
                if q in self.matorrales: d["matorral"] = {"frutos": len(self.matorrales[q]["frutos"]), "zona": self.matorrales[q]["zona"]}
                cas.append(d)
        otras = []
        for b in self.possible_agents:
            if b == a or b not in self.pos or self.cuerpo[b]["muerta"] or self._dist(p, self.pos[b]) > v: continue
            cb = self.cuerpo[b]
            otras.append({"id": b, "pos": list(self.pos[b]), "flaca": cb["hambre"] > cr["umbral_flaca"], "herida": cb["vida"] < cr["umbral_herida"],
                          "energia": self.energia(b), "lleva": [o["tipo"] for o in self.bolsa[b]], "casa": self.casa_de[b], "aldea": "valle"})
            if self.vida_nivel(b) is not None: otras[-1]["vida_nivel"] = self.vida_nivel(b)          # (prompt 47) la vida de la otra, en cuatro niveles
            if (self.cfg.get("cara_v64") or {}).get("activo") and b in getattr(self, "caras", {}): otras[-1]["cara"] = list(self.caras[b])     # (prompt 128) su cara, a la vista
        bes = None
        ves = [] if (self.cfg["bestia"].get("no_se_ve_dormida") and self.cuerpo[a].get("dormida")) else [B for B in self.bestias_aqui() if self._dist(p, B["pos"]) <= v]
        if ves:                                                              # (prompt 88) con varias, «bestia» es la más cercana (empate: la primera)
            B0 = min(ves, key=lambda B: self._dist(p, B["pos"])); bes = {"pos": list(B0["pos"]), "lleva": [o["tipo"] for o, _ in B0["lleva"]]}
            if self._G(): bes["id"] = B0["id"]
        o = {"turno": self.turno, "dia": self.turno // self.dia_turnos, "fase": self.fase(), "turno_del_dia": self.turno % self.dia_turnos,
             "yo": {"id": a, "casa": self.casa_de[a], "pos": list(p), "vida": round(c["vida"], 3), "hambre": round(c["hambre"], 3), "cansancio": round(c["cansancio"], 3),
                    "agotada": c["agotada"], "energia": self.energia(a), "en_casa": self.en_casa_propia(a)},
             "bolsa": [x["tipo"] for x in self.bolsa[a]], "casillas": cas, "criaturas": otras, "bestia": bes,
             **({"bestias": [{"id": B["id"], "pos": list(B["pos"]), "lleva": [o["tipo"] for o, _ in B["lleva"]]} for B in ves]} if self._G() else {}),
             **({"bolsa_origen": [x.get("origen") for x in self.bolsa[a]]} if self._sabores() else {}),
             "almacen": self.nivel_almacen() if self.en_aldea(a) else None,
             "despensa": [x["tipo"] for x in self.despensa[self.casa_de[a]]] if self.en_casa_propia(a) else None,
             "oido": self.oido.get(a, []), "mensajes": self.mensajes.get(a, []),
             "muertes_vistas": self.muertes_vistas.get(a, []),
             **({"empujones_vistos": (getattr(self, "empujones_vistos", None) or {}).get(a, [])} if (C.get("observacion") or {}).get("empujones_vistos") else {}),
             "cadaveres": [dict(c) for c in self.cadaveres.values() if self._dist(p, tuple(c["pos"])) <= v]}
        if C["almacen"]["libreta"] and (p in self.almacen_acceso): o["libreta"] = self.libreta[-C["almacen"]["libreta_largo"]:]
        if self.temperatura() is not None: o["yo"]["temperatura"] = self.temperatura(p); o["temperatura_fuera"] = self.temperatura()      # (prompt 34)
        if (C.get("observacion") or {}).get("lo_que_hizo"):                 # (prompt 93, Manel) lo que hizo de verdad su cuerpo el turno de antes (apagado por defecto)
            o["yo"]["hizo"] = (getattr(self, "_hizo", None) or {}).get(a); o["yo"]["durmio"] = bool(c.get("dormida"))
        return o

    def close(self):
        if self._f: self._f.close(); self._f = None

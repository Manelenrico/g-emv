"""MUNDO — todo lo que se LEE del player_config de zero-sum 0.1.18.

Regla de la casa (las tres cegueras): los identificadores del mundo se LEEN,
jamas se cablean. Aqui vive esa lectura, y sus AUTOCOMPROBACIONES: si el mundo
cambia de forma, esto grita en vez de producir ceros en silencio (que es
exactamente como se colaron las tres cegueras de machina).

Nada de este fichero toca motor/model.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field


class MundoIncoherente(RuntimeError):
    """El player_config no tiene la forma que esta clase sabe leer."""


@dataclass
class Item:
    id: str
    kind: str
    damage: int
    range: int
    cooldown: int
    durability: int
    stack_max: int
    use_ticks: int
    heal: int


@dataclass
class Mundo:
    """Lectura del player_config. Ni un solo numero de estos esta cableado."""
    slot: int
    team: str
    teammate_slot: int
    tick_rate: int
    max_ticks: int
    ignition_tick: int
    alloc_deadline_tick: int
    freeze_ends_tick: int
    arena_size: int
    static_map: list           # lista de filas; static_map[y][x]
    legend: dict               # char -> nombre
    pedestals: list
    zone_schedule: list        # [warn, shrink, done, r0, r1, dps]
    items: dict = field(default_factory=dict)      # id -> Item
    stats_rules: dict = field(default_factory=dict)

    # ── clasificacion derivada del CATALOGO (kind), no de nombres ────────────
    ch_wall: set = field(default_factory=set)      # chars que bloquean
    ch_bush: set = field(default_factory=set)
    ch_fortress: set = field(default_factory=set)
    id_botiquin: str = ""
    id_raciones: tuple = ()
    id_mochila: str = ""
    id_camuflaje: str = ""
    id_red: str = ""
    dmg_ref: int = 0           # divisor del arma = mayor dano del catalogo
    ammo_ids: tuple = ()

    # geometria de la Fortaleza, derivada del static_map
    camara: set = field(default_factory=set)
    bocas: set = field(default_factory=set)

    avisos: list = field(default_factory=list)     # lo que se autocomprobo

    # ────────────────────────────────────────────────────────────────────────
    @classmethod
    def desde_player_config(cls, cfg: dict) -> "Mundo":
        arena = cfg.get("arena") or {}
        freeze = cfg.get("freeze") or {}
        smap = list(arena.get("static_map") or [])
        legend = dict(arena.get("legend") or {})
        n = int(arena.get("size") or 0)
        if not smap or n <= 0:
            raise MundoIncoherente("player_config sin arena.static_map o sin size")
        if len(smap) != n or any(len(r) != n for r in smap):
            raise MundoIncoherente(
                f"static_map {len(smap)}x{len(smap[0]) if smap else 0} != size {n}")

        items = {}
        for it in cfg.get("items") or []:
            items[it["id"]] = Item(
                id=it["id"], kind=it.get("kind", ""), damage=int(it.get("damage", 0)),
                range=int(it.get("range", 0)), cooldown=int(it.get("cooldown", 0)),
                durability=int(it.get("durability", 0)),
                stack_max=int(it.get("stack_max", 1)),
                use_ticks=int(it.get("use_ticks", 0)), heal=int(it.get("heal", 0)))
        if not items:
            raise MundoIncoherente("player_config sin catalogo de items")

        m = cls(
            slot=int(cfg["slot"]), team=str(cfg.get("team", "")),
            teammate_slot=int(cfg.get("teammate_slot", -1)),
            tick_rate=int(cfg.get("tick_rate", 24)),
            max_ticks=int(cfg.get("max_ticks", 0)),
            ignition_tick=int(cfg.get("ignition_tick", 0)),
            alloc_deadline_tick=int(freeze.get("alloc_deadline_tick", 0)),
            freeze_ends_tick=int(freeze.get("ends_tick", 0)),
            arena_size=n, static_map=smap, legend=legend,
            pedestals=[tuple(p) for p in (arena.get("pedestals") or [])],
            zone_schedule=[list(z) for z in (cfg.get("zone_schedule") or [])],
            items=items, stats_rules=dict(cfg.get("stats") or {}),
        )
        m._clasifica_terreno()
        m._clasifica_items()
        m._geometria_fortaleza()
        m._autocomprueba()
        return m

    # ── terreno: por la LEYENDA que manda el mundo, no por el caracter ───────
    def _clasifica_terreno(self):
        for ch, nombre in self.legend.items():
            nm = str(nombre).lower()
            if "wall" in nm or "rock" in nm:
                self.ch_wall.add(ch)
            if "bush" in nm:
                self.ch_bush.add(ch)
            if "fortress" in nm:
                self.ch_fortress.add(ch)
        if not self.ch_wall:
            raise MundoIncoherente(f"la leyenda no declara nada solido: {self.legend}")

    # ── items: por KIND del catalogo; los nombres se comprueban, no se asumen ─
    def _clasifica_items(self):
        cons = [i for i in self.items.values() if i.kind == "ikConsumable"]
        if not cons:
            raise MundoIncoherente("catalogo sin consumibles")
        cons.sort(key=lambda i: i.heal, reverse=True)
        # botiquin = el consumible que MAS cura; el resto, raciones. [impl]
        self.id_botiquin = cons[0].id
        self.id_raciones = tuple(i.id for i in cons[1:]) or (cons[0].id,)

        armas = [i for i in self.items.values()
                 if i.kind in ("ikMelee", "ikRanged", "ikThrown")]
        self.dmg_ref = max((i.damage for i in armas), default=1) or 1
        self.ammo_ids = tuple(i.id for i in self.items.values() if i.kind == "ikAmmo")

        # gear: el catalogo NO dice cual amplia el zurron ni cual camufla.
        # Se casan por id, pero la ausencia se DECLARA en vez de callar (ceguera).
        gear = {i.id for i in self.items.values() if i.kind == "ikGear"}
        for nombre, attr in (("backpack", "id_mochila"), ("camouflage", "id_camuflaje")):
            if nombre in gear:
                setattr(self, attr, nombre)
            else:
                self.avisos.append(
                    f"AUSENTE en el catalogo el gear {nombre!r}; su fila de W queda a 0. "
                    f"gear disponible: {sorted(gear)}")
        lanz = {i.id for i in self.items.values() if i.kind == "ikThrown"}
        # la "red" de la tabla: el arrojadizo de dano 0 (inmoviliza, no hiere)
        redes = [i for i in self.items.values() if i.kind == "ikThrown" and i.damage == 0]
        if redes:
            self.id_red = redes[0].id
        else:
            self.avisos.append(f"sin arrojadizo de dano 0 ('red'); arrojadizos: {sorted(lanz)}")

    # ── Fortaleza: camara y bocas, DERIVADAS del mapa ────────────────────────
    def _geometria_fortaleza(self):
        if not self.ch_fortress:
            self.avisos.append("la leyenda no declara 'fortress'; camara/bocas quedan vacias")
            return
        fort = [(x, y) for y, fila in enumerate(self.static_map)
                for x, ch in enumerate(fila) if ch in self.ch_fortress]
        if not fort:
            self.avisos.append("ninguna casilla de fortaleza en el mapa")
            return
        xs = [p[0] for p in fort]; ys = [p[1] for p in fort]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        # camara = celdas NO-fortaleza estrictamente dentro del rectangulo
        for y in range(y0 + 1, y1):
            for x in range(x0 + 1, x1):
                if self.static_map[y][x] not in self.ch_fortress:
                    self.camara.add((x, y))
        # bocas = huecos en el anillo (celdas del perimetro que no son muro)
        for x in range(x0, x1 + 1):
            for y in (y0, y1):
                if self.static_map[y][x] not in self.ch_fortress:
                    self.bocas.add((x, y))
        for y in range(y0, y1 + 1):
            for x in (x0, x1):
                if self.static_map[y][x] not in self.ch_fortress:
                    self.bocas.add((x, y))
        self.camara -= self.bocas

    # ── autocomprobaciones: que el mapa se lee como creemos ──────────────────
    def _autocomprueba(self):
        # 1. los pedestales del config caen en casillas de pedestal del mapa
        chars = {self.static_map[y][x] for (x, y) in self.pedestals
                 if 0 <= y < self.arena_size and 0 <= x < self.arena_size}
        nombres = {str(self.legend.get(c, c)).lower() for c in chars}
        if not any("pedestal" in n for n in nombres):
            raise MundoIncoherente(
                "static_map[y][x] no da pedestal en las coordenadas de arena.pedestals "
                f"(chars={chars}, nombres={nombres}). ¿ejes cambiados?")
        self.avisos.append(
            f"OK ejes: static_map[y][x] da {sorted(chars)} en los {len(self.pedestals)} pedestales")
        # 2. la fortaleza esta donde dice el mundo (centro)
        if self.camara:
            cx = sum(p[0] for p in self.camara) / len(self.camara)
            cy = sum(p[1] for p in self.camara) / len(self.camara)
            self.avisos.append(
                f"OK fortaleza: camara {len(self.camara)} celdas centro ({cx:.1f},{cy:.1f}); "
                f"bocas {len(self.bocas)} celdas")
        # 3. calendario del anillo presente
        if not self.zone_schedule:
            self.avisos.append("AVISO: sin zone_schedule; F-ANTICIPACION solo usara zone del tick")

    # ── utilidades ───────────────────────────────────────────────────────────
    def solido(self, x: int, y: int) -> bool:
        if not (0 <= x < self.arena_size and 0 <= y < self.arena_size):
            return True
        return self.static_map[y][x] in (self.ch_wall | self.ch_fortress)

    def coste_movimiento(self, speed: int) -> int:
        """Enfriamiento de movimiento en tics: 16 - SPD (README del mundo)."""
        return max(1, 16 - int(speed))

    def radio_vision_max(self) -> float:
        """Radio de vision del hostil MAS listo posible (PROMPT_16).

        No conocemos el INT ajeno: la observacion no lo publica. La constante
        conservadora se LEE de las reglas de estadisticas del `player_config`
        (`stats.max`), no se cablea. Con el tope de la casa (10) sale
        5 + (10+1)//2 = 10. Conservador = suponer que todos ven lo maximo.
        """
        tope = int((self.stats_rules or {}).get("max") or 10)
        return self.radio_vision(tope)

    def linea_de_vista(self, a, b) -> bool:
        """¿Hay linea de vista de `a` a `b`? Muros, rocas y fortaleza cortan.

        Certificado en `protocol_player.md:73`: "visible.* is line-of-sight
        limited by your INT vision radius; walls, rocks, and the Fortress block
        sight". `solido()` es exactamente ese conjunto (la leyenda mete 'rock'
        en ch_wall y la fortaleza en ch_fortress), leido del `static_map`.

        Muestreo recto casilla a casilla; los EXTREMOS no cuentan (el que mira
        y el mirado estan donde estan).
        """
        ax, ay = int(a[0]), int(a[1])
        bx, by = int(b[0]), int(b[1])
        n = max(abs(bx - ax), abs(by - ay))
        if n <= 1:
            return True
        for i in range(1, n):
            x = ax + round((bx - ax) * i / n)
            y = ay + round((by - ay) * i / n)
            if (x, y) in ((ax, ay), (bx, by)):
                continue
            if self.solido(x, y):
                return False
        return True

    def radio_vision(self, intel: int) -> float:
        """Radio de vision: 5 + (INT+1) DIV 2 (`sim.nim:148 visionRadius`).

        CORRECCION (PROMPT_16): la division es ENTERA en el mundo
        (`div 2`), no real. Llevabamos 5 + (INT+1)/2.0, que con INT 8 daba
        9,5 en vez de 9. No es una constante [Manel]: es la formula del mundo,
        y estaba mal leida. Se declara porque cambia la escala de S-7 y de la
        mirada, aunque en medio punto.
        """
        return float(5 + (int(intel) + 1) // 2)

    def dps_ref(self) -> float:
        """Referencia de dano para normalizar F-ANTICIPACION. [impl]

        La tabla proponia 24 HP/s como referencia 1.0 y la marcaba [impl]. Pero
        el calendario de ESTE mundo llega a 40 HP/s, asi que con 24 el termino
        (dps/ref) vale 1,67 y el techo 0,5 recorta el 40 % del rango dinamico:
        toda casilla dentro de ~8 s de arder queda saturada y el gradiente se
        pierde. Se LEE del calendario: referencia = dps maximo del mundo. Asi el
        techo [Manel] 0,5 se alcanza exactamente en el peor caso y ni antes.
        """
        m = max((z[5] for z in self.zone_schedule), default=24.0)
        return float(m) if m else 24.0

    def eventos_arde(self, pos, tick: int):
        """[(tick_de_quema, dps), ...] para ESA casilla: cada momento en que el
        fuego la alcanza, del calendario COMPLETO.

        - Si ya esta fuera AHORA, un evento en `tick` con el dps VIGENTE.
        - Por cada etapa aun no terminada, el instante en que el radio baja por
          debajo de su distancia (acotado a [shrink, done] y a >= tick).

        La fila se queda con el PEOR de estos eventos (ver appraisal_zs). Hace
        falta mirarlos todos: con una sola etapa la fila se INVIERTE, porque una
        casilla del borde que arde pronto con dps debil puntuaria menos que una
        central que ardera despues con dps fuerte.
        """
        c = (self.arena_size // 2, self.arena_size // 2)
        d = ((pos[0] - c[0]) ** 2 + (pos[1] - c[1]) ** 2) ** 0.5
        ev = []
        _c, radio_ahora, dps_ahora = self.anillo_en(tick)
        if d > radio_ahora and dps_ahora > 0:
            ev.append((float(tick), float(dps_ahora)))
        for (warn, shrink, done, r0, r1, dps) in self.zone_schedule:
            if done <= tick or d <= r1:
                continue
            if d >= r0:
                t = float(shrink)
            else:
                f = (d - r0) / (r1 - r0) if r1 != r0 else 0.0
                t = shrink + f * (done - shrink)
            ev.append((max(float(tick), max(float(shrink), min(float(done), t))),
                       float(dps)))
        return ev

    def anillo_en(self, tick: int):
        """(centro, radio, dps) CIERTOS en `tick`, del calendario sellado.

        zone_schedule = [warn, shrink, done, r0, r1, dps]: entre `shrink` y `done`
        el radio interpola de r0 a r1; fuera del radio se cobra `dps`.
        R1: el calendario del anillo es lo UNICO del futuro que se anticipa.
        """
        c = (self.arena_size // 2, self.arena_size // 2)
        radio, dps = float(self.arena_size), 0.0
        for (warn, shrink, done, r0, r1, d) in self.zone_schedule:
            if tick >= warn:
                dps = float(d)
            if tick <= shrink:
                radio = float(r0)
            elif tick >= done:
                radio = float(r1)
            else:
                f = (tick - shrink) / max(1, (done - shrink))
                radio = r0 + (r1 - r0) * f
            if tick < done:
                break
        return c, radio, dps

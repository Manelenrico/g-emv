"""[P5-7A] La curiosidad por el terreno, en seco.

La curiosidad NO se deriva del motor: se INSTALA, como recurso especial dentro
del dominio R, con dos polos — no saber duele, descubrir alivia.

REGLAS DURAS que respeta este fichero:
  · `motor/model.py` INTOCABLE: solo se importan `State`, `opponent_distance`
    y `DEFAULT_CONFIG`.
  · El decisor y la tabla NO se tocan. El renglon nuevo se aplica FUERA, sobre
    `A.filas()`, exactamente con el patron del piso de P5-3E
    (`cantera/paper5/forma.py:444-461`): se repite el reparto de `A.REPARTO` /
    `A.APETITIVAS` y se rehace el `State`.
  · Con el renglon APAGADO la `d` es bit a bit la del appraisal normal. Eso lo
    comprueba el arnes de P5-2 al 100 %, y es la puerta de entrada.

UN HECHO QUE HAY QUE DECLARAR, porque cambia lo que A1 puede medir:
**el mundo no publica que casillas ves.** El registro del tic aplana la
observacion en `ve_agentes` / `ve_items` / `ve_bushes` / `ve_proyectiles`; no
hay lista de casillas ni de tiles (`paintball/alma/policy.py:174-182`). La
visibilidad es DERIVADA: radio `mundo.radio_vision(INT)` — 9 en estas corridas,
5 + (8+1)//2 — mas `mundo.linea_de_vista`, que cortan muros, rocas y fortaleza
(`mundo.py:231-264`). Asi que la ignorancia se RECONSTRUYE aqui, casilla a
casilla, a partir de la posicion del diario. No es un dato leido: es un dato
calculado con las reglas del mundo, y se dice asi.
"""
from __future__ import annotations
import os, sys

# AUTOSUFICIENTE: este fichero viaja DENTRO de la imagen del campo (P5-7C), asi
# que no puede depender de `serie_util` ni de `cantera/paper4`. En el banco, los
# scripts que lo usan ya meten `paintball/` en el path; en la imagen, `/app` lo
# es. Si nada de eso ha pasado todavia, se anade la raiz del repo.
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for _p in (os.path.join(RAIZ, "paintball"), RAIZ):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.append(_p)

from alma import decisor_zs as D                          # noqa: E402
from alma import appraisal_zs_v42_exp as A                # noqa: E402
from motor.model import State, opponent_distance, DEFAULT_CONFIG   # noqa: E402

# ── EL RENGLON ────────────────────────────────────────────────────────────
FILA = "R-CURIOSIDAD-TERRENO"
# Reparto (pF, pR, pS), suman 1, ninguno a cero (regla de la tabla). Se elige
# el de los renglones R-dominantes ya existentes — `R-ACOPIO` y `R-LLAMADA`
# son (0.1, 0.8, 0.1) — porque el encargo lo define como «recurso especial
# DENTRO del dominio R». No se inventa un reparto nuevo.
REPARTO_CUR = (0.1, 0.8, 0.1)
KS = (0.1, 0.2, 0.4)
FILA_FRONT = "R-CURIOSIDAD-FRONTERA"

# ── LA IGNORANCIA (A1) ────────────────────────────────────────────────────
RADIO_LOCAL = 6           # [Manel] el radio de la ignorancia local
VENTANA_NOVEDAD = 100     # [Manel] casillas vistas por primera vez, ultimos N

# ── LA AMENAZA (A2) ───────────────────────────────────────────────────────
VENTANA_DANO = 100        # [Manel] dano recibido en los ultimos N tics
DANO_REF = 25.0           # [impl] dano que satura el termino; ver informe
SEGURO, INSEGURO = 0.2, 0.6          # [Manel] los tres grados
# El horizonte del anillo se IMPORTA del appraisal, no se copia a mano.
ANILLO_HORIZONTE_S = A.ANT_HORIZONTE_S


# ══════════════════════════════════════════════════════════════════════════
#  EL OJO: que casillas ha visto este asiento, reconstruido
# ══════════════════════════════════════════════════════════════════════════
class Ojo:
    """Acumula las casillas vistas por UN asiento a lo largo de su vida.

    `vistas_desde` se cachea por casilla: el agente repite posiciones muchisimo
    y el rayo de linea de vista es lo caro. Sin la cache esto no termina.
    """

    def __init__(self, mundo, intel: int):
        self.mundo = mundo
        self.radio = mundo.radio_vision(intel)
        self.n_arena = mundo.arena_size * mundo.arena_size
        self._cache: dict = {}
        self.primera_vez: dict = {}       # casilla -> tick en que se vio
        self._local_cache: dict = {}

    # ── que se ve desde una casilla ──────────────────────────────────────
    def vistas_desde(self, pos) -> frozenset:
        pos = (int(pos[0]), int(pos[1]))
        v = self._cache.get(pos)
        if v is not None:
            return v
        m, r = self.mundo, self.radio
        n = m.arena_size
        rr = int(r)
        out = set()
        for dx in range(-rr, rr + 1):
            for dy in range(-rr, rr + 1):
                x, y = pos[0] + dx, pos[1] + dy
                if not (0 <= x < n and 0 <= y < n):
                    continue
                if (dx * dx + dy * dy) ** 0.5 > r:
                    continue
                if (x, y) == pos or m.linea_de_vista(pos, (x, y)):
                    out.add((x, y))
        v = frozenset(out)
        self._cache[pos] = v
        return v

    # ── el vecindario local, cacheado ────────────────────────────────────
    def vecindario(self, pos, radio: int = RADIO_LOCAL) -> frozenset:
        pos = (int(pos[0]), int(pos[1]))
        key = (pos, radio)
        v = self._local_cache.get(key)
        if v is not None:
            return v
        n = self.mundo.arena_size
        out = {(pos[0] + dx, pos[1] + dy)
               for dx in range(-radio, radio + 1)
               for dy in range(-radio, radio + 1)
               if 0 <= pos[0] + dx < n and 0 <= pos[1] + dy < n
               and (dx * dx + dy * dy) ** 0.5 <= radio}
        v = frozenset(out)
        self._local_cache[key] = v
        return v

    # ── mirar, de verdad, en un tic ──────────────────────────────────────
    def mira(self, pos, tick: int) -> int:
        """Apunta lo visto desde `pos` en `tick`. Devuelve cuantas son nuevas."""
        nuevas = 0
        for c in self.vistas_desde(pos):
            if c not in self.primera_vez:
                self.primera_vez[c] = tick
                nuevas += 1
        return nuevas

    # ── A1 · los tres numeros ────────────────────────────────────────────
    def ignorancia_global(self) -> float:
        """Fraccion de casillas de la arena nunca vistas por este asiento.

        El denominador son TODAS las casillas del mapa (48x48 aqui), muros
        incluidos: un muro se VE aunque no se pise. Declarado, no elegido.
        """
        return 1.0 - len(self.primera_vez) / float(self.n_arena)

    def ignorancia_local(self, pos, radio: int = RADIO_LOCAL) -> float:
        vec = self.vecindario(pos, radio)
        if not vec:
            return 0.0
        return sum(1 for c in vec if c not in self.primera_vez) / float(len(vec))

    def novedad(self, tick: int, ventana: int = VENTANA_NOVEDAD) -> int:
        return sum(1 for t in self.primera_vez.values() if tick - t < ventana)

    # ── A3 · la ignorancia local PROYECTADA desde una casilla ────────────
    def ignorancia_proyectada(self, pos, radio: int = RADIO_LOCAL) -> float:
        """Lo no visto dentro del radio desde `pos`, DESCONTANDO lo que veria
        al llegar. Es el dolor que le quedaria a ese candidato."""
        vec = self.vecindario(pos, radio)
        if not vec:
            return 0.0
        veria = self.vistas_desde(pos)
        quedan = sum(1 for c in vec
                     if c not in self.primera_vez and c not in veria)
        return quedan / float(len(vec))


# ══════════════════════════════════════════════════════════════════════════
#  LA FRONTERA: distancia a lo no visto, y la caida de R-LLAMADA
# ══════════════════════════════════════════════════════════════════════════
def g_llamada(d: float) -> float:
    """La MISMA forma de caida por distancia que usa `R-LLAMADA`.

    `appraisal_zs_v42_exp.py:1085`:
        v = niv * max(0.0, 1.0 - math.dist(pos, p) / BOTIN_DIST_REF) ** BOTIN_EXP

    Las dos constantes se IMPORTAN (`:134` BOTIN_DIST_REF = 24.0, `:135`
    BOTIN_EXP = 3, descuento cubico); no se copian a mano.
    """
    return max(0.0, 1.0 - d / A.BOTIN_DIST_REF) ** A.BOTIN_EXP


_VECINOS = ((1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1))


def dist_a_frontera(ojo, mundo) -> dict:
    """BFS multi-fuente: de cada casilla pisable a la NO VISTA mas cercana.

    Fuentes = casillas no vistas y PISABLES («alcanzable por el mapa»: una
    pared no vista no es un sitio al que ir). Se expande en 8 direcciones,
    que son las del decisor (`decisor_zs.DIRS`). Un solo BFS sobre las 2.304
    casillas por tic muestreado sirve para TODOS los candidatos de ese tic:
    por eso esto cabe en el tiempo sin precalcular por posicion.
    """
    from collections import deque
    n = mundo.arena_size
    dist, dq = {}, deque()
    for y in range(n):
        for x in range(n):
            if mundo.solido(x, y):
                continue
            if (x, y) not in ojo.primera_vez:
                dist[(x, y)] = 0
                dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        d = dist[(x, y)] + 1
        for dx, dy in _VECINOS:
            q = (x + dx, y + dy)
            if q in dist or mundo.solido(q[0], q[1]):
                continue
            dist[q] = d
            dq.append(q)
    return dist


# ══════════════════════════════════════════════════════════════════════════
#  LA AMENAZA GRADUADA (A2)
# ══════════════════════════════════════════════════════════════════════════
def _alcance(mundo, mano) -> float:
    """Alcance del arma en la mano ajena. Se LEE del catalogo del mundo."""
    if not mano or mano in ("none", "None"):
        return 0.0
    it = (mundo.items or {}).get(mano if isinstance(mano, str)
                                 else mano.get("id"))
    return float(getattr(it, "range", 0) or 0) if it else 0.0


def amenaza(r, mundo, herm, dano_100: float, tick: int) -> tuple:
    """Amenaza en [0,1] desde lo que el cuerpo VE, con su desglose.

    Tres terminos, cada uno en [0,1], combinados como «al menos uno»:

        amenaza = 1 - (1-a_armados)(1-a_dano)(1-a_anillo)

    Se eligen asi, y no como una suma con pesos, por dos razones: (1) la
    combinacion no puede pasarse de 1 sin recortes artificiales, y (2) dos
    peligros distintos se acumulan sin que ninguno tape al otro, que es lo que
    hace una suma con techo. Da EXACTAMENTE 0 sin armados a la vista, sin dano
    reciente y sin anillo, que es la condicion que pide el encargo.

      a_armados: por cada rival armado a distancia `d` con alcance `rg`,
                 1 si `d <= rg` (a tiro) y si no cae linealmente hasta 0 en el
                 radio de vision propio. Se combinan igual, «al menos uno».
      a_dano   : dano recibido en los ultimos 100 tics / DANO_REF, con techo 1.
      a_anillo : 1 si la casilla ya arde; si no, sube al acercarse el momento
                 de arder, con el MISMO horizonte que F-ANTICIPACION
                 (`A.ANT_HORIZONTE_S`, importado).
    """
    pos = tuple(r.get("pos") or ())
    # ── armados a la vista ───────────────────────────────────────────────
    radio_v = mundo.radio_vision(8)
    comp = 1.0
    n_arm = 0
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") == herm or not a.get("pos"):
            continue
        rg = _alcance(mundo, a.get("hand"))
        if rg <= 0.0:
            continue
        n_arm += 1
        d = max(abs(pos[0] - a["pos"][0]), abs(pos[1] - a["pos"][1]))
        if d <= rg:
            ci = 1.0
        elif d >= radio_v:
            ci = 0.0
        else:
            ci = (radio_v - d) / float(radio_v - rg)
        comp *= (1.0 - max(0.0, min(1.0, ci)))
    a_arm = 1.0 - comp
    # ── dano reciente ────────────────────────────────────────────────────
    a_dano = min(1.0, max(0.0, dano_100) / DANO_REF)
    # ── anillo ───────────────────────────────────────────────────────────
    a_anillo = 0.0
    if pos:
        for t_burn, dps in mundo.eventos_arde(pos, tick):
            if dps <= 0:
                continue
            t_s = max(0.0, (t_burn - tick) / float(mundo.tick_rate))
            a_anillo = max(a_anillo,
                           max(0.0, 1.0 - t_s / ANILLO_HORIZONTE_S))
    am = 1.0 - (1.0 - a_arm) * (1.0 - a_dano) * (1.0 - a_anillo)
    return (max(0.0, min(1.0, am)),
            {"armados": round(a_arm, 5), "n_armados": n_arm,
             "dano": round(a_dano, 5), "anillo": round(a_anillo, 5)})


def grado(am: float) -> str:
    return "seguro" if am < SEGURO else ("inseguro" if am > INSEGURO
                                         else "neutro")


# ══════════════════════════════════════════════════════════════════════════
#  EL PROXY: el renglon instalado FUERA, sin tocar decisor ni tabla
# ══════════════════════════════════════════════════════════════════════════
class Curioso:
    """Envoltura de v42 que SOLO cambia `appraise()`.

    `decisor_zs` usa `A.` para veinte cosas (constantes, `filas`, `riqueza_W`,
    `agresor_de_la_hermana`...), asi que esto delega TODO en v42 por
    `__getattr__` y reimplanta unicamente el montaje del `State`, con el
    renglon nuevo sumado al reparto. Con `k=0` o `on=False` no suma nada y la
    `d` es la de siempre, bit a bit.
    """

    def __init__(self):
        self.on = False
        self.k = 0.0
        self.balanza = True        # A5 corre con esto en False
        self.modo = "local"        # "local" (A3) o "frontera" (el anadido)
        self.ojo = None
        self.dist_frontera = {}    # del BFS del tic, para el modo frontera
        self.ign_global = 0.0
        self.amenaza_ahora = 0.0
        self.ultimo_M = 0.0
        # contadores de diagnostico: sin esto no se puede distinguir «el
        # renglon no se enciende nunca» de «se enciende y no voltea nada».
        self.n_valor = 0          # candidatos valorados
        self.n_valor_pos = 0      # ... con M > 0
        self.max_M = 0.0

    def reinicia_cuentas(self):
        self.n_valor = self.n_valor_pos = 0
        self.max_M = 0.0

    def __getattr__(self, n):      # todo lo demas, de v42
        return getattr(A, n)

    # ── el valor del renglon para UNA foto proyectada ────────────────────
    def valor(self, ob2) -> float:
        if not self.on or self.k <= 0.0 or self.ojo is None:
            return 0.0
        p2 = ((ob2.get("you") or {}).get("pos"))
        if not p2:
            return 0.0
        self.n_valor += 1
        factor = (1.0 - self.amenaza_ahora) if self.balanza else 1.0
        if self.modo == "frontera":
            # ── LA LLAMADA DE LA FRONTERA ────────────────────────────────
            # LECTURA DECLARADA. El encargo escribe «x g(distancia)», pero g
            # vale 1 PEGADO a lo no visto y 0 lejos; como este renglon es
            # DOLOR, multiplicar por g haria doler MAS cuanto mas cerca de la
            # frontera, y no doler NADA con la frontera lejos — lo contrario
            # de la intencion que el propio encargo declara («acercarse
            # alivia y alejarse duele») y de como funciona el renglon local,
            # donde el dolor es la ignorancia NO aliviada. Se implementa
            # `(1 - g)`. Para la lectura literal basta quitar el `1.0 -`.
            d = self.dist_frontera.get(tuple(p2))
            if d is None:          # sin frontera alcanzable: nada que doler
                return 0.0
            M = self.k * self.ign_global * factor * (1.0 - g_llamada(d))
        else:
            ign = self.ojo.ignorancia_proyectada(tuple(p2))
            if ign <= 0.0:
                return 0.0
            M = self.k * ign * factor
        if M > 0.0:
            self.n_valor_pos += 1
            self.max_M = max(self.max_M, M)
        return M

    # ── el appraise con el renglon, montado como en P5-3E ────────────────
    def appraise(self, obs, mundo, mem, tick):
        F = A.filas(obs, mundo, mem, tick)
        M_cur = self.valor(obs)
        self.ultimo_M = M_cur
        pF = nF = pR = nR = pS = nS = 0.0
        radiografia = {"filas": {}, "W": F["_W"], "W_desglose": F["_W_desglose"],
                       "B": F["_B"], "P": F["_P"], "hostiles": F["_hostiles"],
                       "anticipacion": F["_ant"], "botin": F["_botin"],
                       "pareja_banda": F["_pareja_banda"],
                       "agresores": F["_agresores"],
                       "medicina": F.get("_medicina"), "duelo": F.get("_duelo")}
        if F.get("_parte") is not None:
            radiografia["parte"] = F["_parte"]
        for nombre, (fF, fR, fS) in A.REPARTO.items():
            M = float(F.get(nombre) or 0.0)
            if M <= 0.0:
                radiografia["filas"][nombre] = {"M": 0.0}
                continue
            aF, aR, aS = M * fF, M * fR, M * fS
            if nombre in A.APETITIVAS:
                pF += aF; pR += aR; pS += aS
            else:
                nF += aF; nR += aR; nS += aS
            radiografia["filas"][nombre] = {
                "M": round(M, 5), "signo": "+" if nombre in A.APETITIVAS else "-",
                "F": round(aF, 5), "R": round(aR, 5), "S": round(aS, 5)}
        # ── EL RENGLON NUEVO, fuera de la tabla ──────────────────────────
        if M_cur > 0.0:
            fF, fR, fS = REPARTO_CUR
            aF, aR, aS = M_cur * fF, M_cur * fR, M_cur * fS
            nF += aF; nR += aR; nS += aS        # es DOLOR: no es apetitiva
            radiografia["filas"][FILA if self.modo == "local"
                                 else FILA_FRONT] = {
                "M": round(M_cur, 5), "signo": "-", "F": round(aF, 5),
                "R": round(aR, 5), "S": round(aS, 5)}
        st = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
        radiografia["fuerzas_crudas"] = {
            "pF": round(pF, 5), "nF": round(nF, 5), "pR": round(pR, 5),
            "nR": round(nR, 5), "pS": round(pS, 5), "nS": round(nS, 5)}
        radiografia["fuerzas_state"] = {
            "pF": round(st.pF, 5), "nF": round(st.nF, 5),
            "pR": round(st.pR, 5), "nR": round(st.nR, 5),
            "pS": round(st.pS, 5), "nS": round(st.nS, 5)}
        return st, radiografia


CUR = Curioso()


def instala():
    """Pone el proxy donde el decisor busca el appraisal. Reversible."""
    D.A = CUR
    return CUR


def desinstala():
    D.A = A


def d_de(st) -> float:
    return opponent_distance(st, DEFAULT_CONFIG)

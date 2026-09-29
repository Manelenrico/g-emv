"""[P5-7B] La curiosidad y el vinculo con los otros, en seco.

Dos filas de dos ejes, alimentadas por UNA MISMA memoria por asiento construida
**solo con lo que el asiento HIZO a la vista**. Nunca con etiquetas: el nombre
de la politica rival existe en `E3_participantes.json` y NO se usa aqui.

QUE PUBLICA EL MUNDO, y que no (esto manda sobre lo que B1 puede medir):
  · **quien nos pego**: `damage_taken[].source = "P<slot>"`. Certeza total.
  · **quien disparo a quien**: `ve_proyectiles[].shooter` trae el slot del
    tirador — «el UNICO autor cierto de todo el protocolo» (acta del 40,
    `policy_cortex.py:795-800`). Solo vale para lo que vuela.
  · **el cuerpo a cuerpo ajeno NO se publica.** No hay ningun evento de golpe
    entre terceros: `eventos` son ignicion, boom, muertes, regalos y avisos del
    anillo. Asi que «pego a otro a la vista» es CIERTO para proyectiles y
    CIEGO para el melee, y se dice asi.
  · `death_fireworks.slot` es el MUERTO, no el matador.

LAS FILAS (B2) se instalan FUERA, con el mismo patron del piso de P5-3E y de
`curiosidad.py`: se repite el reparto de `A.REPARTO` / `A.APETITIVAS` y se
rehace el `State`. Motor, decisor y tabla sin tocar.
"""
from __future__ import annotations
import math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for _p in (os.path.join(RAIZ, "paintball"), RAIZ, AQUI):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.append(_p)

from alma import decisor_zs as D                          # noqa: E402
from alma import appraisal_zs_v42_exp as A                # noqa: E402
from motor.model import State                             # noqa: E402
import curiosidad as C                                    # noqa: E402

# ── LOS DOS RENGLONES ─────────────────────────────────────────────────────
FILA_OTROS = "R-CURIOSIDAD-OTROS"
FILA_VINCULO = "S-VINCULO-EXTRANO"
# R-CURIOSIDAD-OTROS es recurso: el reparto R-dominante, como el del terreno.
REPARTO_OTROS = (0.1, 0.8, 0.1)
# S-VINCULO-EXTRANO es social puro: el reparto de `S-COMPANIA` (`:437`), que es
# la fila cuyo tiron imita. Se IMPORTA, no se copia.
REPARTO_VINCULO = A.REPARTO["S-COMPANIA"]

# «volumen mas bajo que el terreno» [Manel]: los k por defecto van por debajo
# del k del terreno (0,2), y el barrido los recorre.
KS_OTROS = (0.05, 0.1, 0.2)
KS_VINCULO = (0.1, 0.2)

# ── EL CONOCIMIENTO (B1 i) ────────────────────────────────────────────────
TICS_REF = 200.0        # [impl] saturacion de la observacion; ver informe
W_VISTA, W_ARMA, W_CONDUCTA = 0.5, 0.25, 0.25   # [impl] suman 1

# ── EL SIGNO (B1 ii) ──────────────────────────────────────────────────────
N_A_TIRO = (100, 250)   # [Manel] los dos valores que se prueban


def _slot_de(fuente) -> int | None:
    """De `"P9"` a 9, como hace `Memoria.observa` (`:646-650`)."""
    d = "".join(ch for ch in str(fuente or "") if ch.isdigit())
    return int(d) if d else None


class Otro:
    """Lo que este asiento ha HECHO a la vista. Nada de etiquetas."""

    __slots__ = ("slot", "apariciones", "tics_vista", "armas", "golpes_a_mi",
                 "dano_a_mi", "disparos_a_otros", "tics_a_tiro", "acerco",
                 "alejo", "_visible_antes", "_dist_prev", "primer_tick",
                 "ultimo_tick")

    def __init__(self, slot):
        self.slot = slot
        self.apariciones = 0        # veces que entra en la vista
        self.tics_vista = 0
        self.armas = set()          # ids de arma vistos en su mano
        self.golpes_a_mi = 0        # IMPACTOS, no dano
        self.dano_a_mi = 0.0
        self.disparos_a_otros = 0   # de `ve_proyectiles[].shooter`, CIERTO
        self.tics_a_tiro = 0        # armado, con nosotros en su alcance y LOS
        self.acerco = 0
        self.alejo = 0
        self._visible_antes = False
        self._dist_prev = None
        self.primer_tick = None
        self.ultimo_tick = None

    # ── (i) EL CONOCIMIENTO, declarado ───────────────────────────────────
    def conocimiento(self) -> float:
        """En [0,1]. Satura con la observacion y con haberle visto el arma y
        la conducta.

            c = 0,50 · min(1, tics_vista/200)
              + 0,25 · (le he visto un arma)
              + 0,25 · (le he visto CONDUCTA)

        «Conducta» = me pego, o disparo a otro, o estuvo a tiro sin pegarme.
        Los tres pesos suman 1 y van declarados como `[impl]`: el encargo pide
        «una formula simple», no una calibrada.
        """
        v = min(1.0, self.tics_vista / TICS_REF)
        a = 1.0 if self.armas else 0.0
        c = 1.0 if (self.golpes_a_mi or self.disparos_a_otros
                    or self.tics_a_tiro) else 0.0
        return W_VISTA * v + W_ARMA * a + W_CONDUCTA * c

    # ── (ii) EL SIGNO ────────────────────────────────────────────────────
    def signo(self, n_a_tiro: int = 100) -> int:
        """-1 agresor · +1 pudo y no quiso · 0 sin evidencia."""
        if self.golpes_a_mi or self.disparos_a_otros:
            return -1
        if self.tics_a_tiro >= n_a_tiro:
            return 1
        return 0

    def arma_vista(self) -> bool:
        return bool(self.armas)


class MemoriaOtros:
    """La memoria por asiento de UNA vida, construida tic a tic del diario."""

    def __init__(self, mundo, herm, intel: int = 8):
        self.mundo = mundo
        self.herm = herm
        self.radio = mundo.radio_vision(intel)
        self.por_slot: dict[int, Otro] = {}
        self.melee_ciego = 0     # veces que un visible pierde banda sin tirador

    def _de(self, slot) -> Otro:
        o = self.por_slot.get(slot)
        if o is None:
            o = self.por_slot[slot] = Otro(slot)
        return o

    def observa(self, r, tick: int):
        """Un tic del diario. `r` es el registro crudo."""
        pos = tuple(r.get("pos") or ())
        vis = r.get("ve_agentes") or []
        ahora = set()
        for a in vis:
            sl = a.get("slot")
            if sl is None or sl == self.herm or not a.get("pos"):
                continue
            ahora.add(sl)
            o = self._de(sl)
            if o.primer_tick is None:
                o.primer_tick = tick
            o.ultimo_tick = tick
            if not o._visible_antes:
                o.apariciones += 1
            o.tics_vista += 1
            mano = a.get("hand")
            mid = mano.get("id") if isinstance(mano, dict) else mano
            if mid and mid not in ("none", "None"):
                o.armas.add(mid)
                # ¿nos tiene a tiro, con linea de vista?
                it = (self.mundo.items or {}).get(mid)
                rg = float(getattr(it, "range", 0) or 0) if it else 0.0
                q = tuple(a["pos"])
                if rg > 0 and pos:
                    dch = max(abs(pos[0] - q[0]), abs(pos[1] - q[1]))
                    if dch <= rg and self.mundo.linea_de_vista(q, pos):
                        o.tics_a_tiro += 1
            # ¿se acerca o se aleja, estando nosotros a la vista?
            if pos:
                d = math.dist(pos, tuple(a["pos"]))
                if o._dist_prev is not None:
                    if d < o._dist_prev - 0.01:
                        o.acerco += 1
                    elif d > o._dist_prev + 0.01:
                        o.alejo += 1
                o._dist_prev = d
        for sl, o in self.por_slot.items():
            if sl not in ahora:
                o._dist_prev = None
            o._visible_antes = sl in ahora
        # quien nos pego: CIERTO
        for g in (r.get("damage_taken") or []):
            sl = _slot_de(g.get("source"))
            if sl is None or str(g.get("source")) == "zone":
                continue
            o = self._de(sl)
            o.golpes_a_mi += 1
            o.dano_a_mi += float(g.get("amount") or 0.0)
        # quien disparo a quien: CIERTO para lo que vuela
        for p in (r.get("ve_proyectiles") or []):
            sl = p.get("shooter")
            if sl is None or sl in (self.herm,):
                continue
            self._de(sl).disparos_a_otros += 1

    # ── el reparto por signo, al final de una vida ───────────────────────
    def reparto(self, n_a_tiro: int = 100) -> dict:
        c = {-1: 0, 0: 0, 1: 0}
        for o in self.por_slot.values():
            c[o.signo(n_a_tiro)] += 1
        return {"negativos": c[-1], "neutros": c[0], "positivos": c[1],
                "vistos": len(self.por_slot)}

    # ── el mas cercano DESCONOCIDO a la vista (B2) ───────────────────────
    def desconocido_mas_cerca(self, r, n_a_tiro: int = 100):
        """(slot, pos, conocimiento) del asiento a la vista que menos conozco
        y que NO es agresor ni ensena arma. None si no hay ninguno."""
        pos = tuple(r.get("pos") or ())
        if not pos:
            return None
        mejor = None
        for a in (r.get("ve_agentes") or []):
            sl = a.get("slot")
            if sl is None or sl == self.herm or not a.get("pos"):
                continue
            o = self.por_slot.get(sl)
            if o is None:
                continue
            # «cero si ese asiento tiene signo negativo o ensena un arma
            #  (pasa a miedo)» [Manel]
            if o.signo(n_a_tiro) < 0 or o.arma_vista():
                continue
            k = o.conocimiento()
            d = math.dist(pos, tuple(a["pos"]))
            if mejor is None or (k, d) < (mejor[2], mejor[3]):
                mejor = (sl, tuple(a["pos"]), k, d)
        return mejor

    def positivos_a_la_vista(self, r, n_a_tiro: int = 100):
        """[(slot, pos)] de los asientos con signo POSITIVO que veo ahora."""
        out = []
        for a in (r.get("ve_agentes") or []):
            sl = a.get("slot")
            if sl is None or sl == self.herm or not a.get("pos"):
                continue
            o = self.por_slot.get(sl)
            if o is not None and o.signo(n_a_tiro) > 0:
                out.append((sl, tuple(a["pos"])))
        return out


# ══════════════════════════════════════════════════════════════════════════
#  B2 · LAS DOS FILAS
# ══════════════════════════════════════════════════════════════════════════
def valor_curiosidad_otros(k_o, conocimiento, amenaza, dist, balanza=True):
    """k_o × (1 − conocimiento) × (1 − amenaza) × (1 − g(d)).

    `g` es la caida de `R-LLAMADA` (`appraisal_zs_v42_exp.py:1085`, con
    `BOTIN_DIST_REF` `:134` y `BOTIN_EXP` `:135`), reutilizada por
    `curiosidad.g_llamada`. Como en el terreno, el DOLOR es lo no aliviado:
    `(1 − g)` vale 0 pegado al asiento y 1 lejos, asi que acercarse alivia.
    """
    if k_o <= 0.0 or dist is None:
        return 0.0
    f = (1.0 - amenaza) if balanza else 1.0
    return k_o * (1.0 - conocimiento) * f * (1.0 - C.g_llamada(dist))


def valor_vinculo(k_s, dist):
    """El tiron hacia su compania, CON LA FORMA DE `S-COMPANIA`.

    `S-COMPANIA` (`appraisal_zs_v42_exp.py:1003-1038`) es lineal con zona
    muerta: 0 dentro de `COMPANIA_D0` (2,0), y sube hasta `COMPANIA_TECHO`
    (0,22) a lo largo de `COMPANIA_RANGO` (6,0). Las tres se IMPORTAN.

        M = techo × min(1, (d − D0) / RANGO)      si d > D0, si no 0

    DECLARADO: la fila que se imita esta **APAGADA** en v42
    (`COMPANIA_ON = False`, `:314`, candado del 62). Se reutiliza su FORMA,
    no se enciende la fila.
    """
    if k_s <= 0.0 or dist is None or dist <= A.COMPANIA_D0:
        return 0.0
    m = A.COMPANIA_TECHO * min(1.0, (dist - A.COMPANIA_D0) / A.COMPANIA_RANGO)
    return k_s * m


class Sociable:
    """Proxy de v42 con los dos renglones nuevos, instalados FUERA."""

    def __init__(self):
        self.on = False
        self.k_o = 0.0
        self.k_s = 0.0
        self.balanza = True
        self.n_a_tiro = 100
        self.mem = None            # MemoriaOtros
        self.amenaza_ahora = 0.0
        self.desconocido = None    # (slot, pos, conocimiento, dist)
        self.positivos = []        # [(slot, pos)]
        self.reinicia_cuentas()

    def reinicia_cuentas(self):
        self.n_valor = 0
        self.n_otros = 0           # candidatos con M de curiosidad > 0
        self.n_vinculo = 0         # candidatos con M de vinculo > 0
        self.max_o = self.max_s = 0.0
        self.ultimo = {}

    def __getattr__(self, n):
        return getattr(A, n)

    def _valores(self, ob2):
        if not self.on:
            return 0.0, 0.0
        p2 = (ob2.get("you") or {}).get("pos")
        if not p2:
            return 0.0, 0.0
        p2 = tuple(p2)
        self.n_valor += 1
        m_o = 0.0
        if self.desconocido is not None:
            _sl, q, con, _d = self.desconocido
            m_o = valor_curiosidad_otros(self.k_o, con, self.amenaza_ahora,
                                         math.dist(p2, q), self.balanza)
        m_s = 0.0
        for _sl, q in self.positivos:
            m_s = max(m_s, valor_vinculo(self.k_s, math.dist(p2, q)))
        if m_o > 0:
            self.n_otros += 1
            self.max_o = max(self.max_o, m_o)
        if m_s > 0:
            self.n_vinculo += 1
            self.max_s = max(self.max_s, m_s)
        return m_o, m_s

    def appraise(self, obs, mundo, mem, tick):
        F = A.filas(obs, mundo, mem, tick)
        m_o, m_s = self._valores(obs)
        pF = nF = pR = nR = pS = nS = 0.0
        radio = {"filas": {}, "W": F["_W"], "W_desglose": F["_W_desglose"],
                 "B": F["_B"], "P": F["_P"], "hostiles": F["_hostiles"],
                 "anticipacion": F["_ant"], "botin": F["_botin"],
                 "pareja_banda": F["_pareja_banda"],
                 "agresores": F["_agresores"],
                 "medicina": F.get("_medicina"), "duelo": F.get("_duelo")}
        if F.get("_parte") is not None:
            radio["parte"] = F["_parte"]
        for nombre, (fF, fR, fS) in A.REPARTO.items():
            M = float(F.get(nombre) or 0.0)
            if M <= 0.0:
                radio["filas"][nombre] = {"M": 0.0}
                continue
            aF, aR, aS = M * fF, M * fR, M * fS
            if nombre in A.APETITIVAS:
                pF += aF; pR += aR; pS += aS
            else:
                nF += aF; nR += aR; nS += aS
            radio["filas"][nombre] = {
                "M": round(M, 5), "signo": "+" if nombre in A.APETITIVAS else "-",
                "F": round(aF, 5), "R": round(aR, 5), "S": round(aS, 5)}
        for nom, M, rep in ((FILA_OTROS, m_o, REPARTO_OTROS),
                            (FILA_VINCULO, m_s, REPARTO_VINCULO)):
            if M <= 0.0:
                continue
            fF, fR, fS = rep
            aF, aR, aS = M * fF, M * fR, M * fS
            nF += aF; nR += aR; nS += aS      # los dos son DOLOR
            radio["filas"][nom] = {"M": round(M, 5), "signo": "-",
                                   "F": round(aF, 5), "R": round(aR, 5),
                                   "S": round(aS, 5)}
        st = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
        radio["fuerzas_crudas"] = {"pF": round(pF, 5), "nF": round(nF, 5),
                                   "pR": round(pR, 5), "nR": round(nR, 5),
                                   "pS": round(pS, 5), "nS": round(nS, 5)}
        radio["fuerzas_state"] = {"pF": round(st.pF, 5), "nF": round(st.nF, 5),
                                  "pR": round(st.pR, 5), "nR": round(st.nR, 5),
                                  "pS": round(st.pS, 5), "nS": round(st.nS, 5)}
        return st, radio


SOC = Sociable()


def instala():
    D.A = SOC
    return SOC


def desinstala():
    D.A = A

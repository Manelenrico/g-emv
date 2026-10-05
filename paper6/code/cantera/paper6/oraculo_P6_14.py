"""[P6-14] EL ORACULO: INSTRUMENTO DE MEDIDA. NO ES CUERPO, NO JUEGA, NO DECIDE.

Un generador de planes POR REGLAS que usa solo lo que el mundo publica desde el
tic 0: el calendario del anillo (`zone_schedule`), el centro, el mapa, y los
rivales que el cuerpo tiene contados (vistos + dichos por el hermano) en la
percepcion que ve el decisor. Propone planes en el idioma de formas del cinco
(un tramo `ir` a una casilla que siga a salvo cuando llegue, y un tramo
`esperar`), para que LA PUERTA REAL del cuerpo congelado (`policy_forma`) los
juzgue en `banco_P6_14.py`. Aqui no hay ninguna valoracion: solo geometria y
calendario.

Tres criterios de destino (P6-14 §1):
  (a) la casilla segura mas cercana (pasos reales, BFS a 8 vecinos);
  (b) la casilla segura con menos rivales contados cerca (Chebyshev <= R);
  (c) la misma casilla para los dos hermanos: la que minimiza el maximo de los
      pasos de los dos (solo si el hermano vive y se sabe donde esta).
Dos momentos (P6-14 §1): (1) ahora, en cada decision en que mi casilla arde o
ardera antes de lo que tardo en salir mas un margen; (2) al primer aviso de la
fase, aunque aun no arda.

UMBRALES QUE ELIGE EL INSTRUMENTO (declarados; el banco los cruza con otros
dos valores cada uno):
  MARGEN     = 3 pasos de reloj (33 tics)   · alternativas 0 y 10 pasos (110)
  R_CERCA    = 5 casillas                    · alternativas 3 y 8
  H (espera) = 100 tics                      · alternativas 50 y 200
El reloj de un paso es `mundo.coste_movimiento(speed)` (16 - SPD), el mismo que
usa la proyeccion de la puerta (`proyeccion.PASO_TICS` = 11 con SPD 5).
"""
from __future__ import annotations
import math

DIRS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
MARGENES = (33, 0, 110)          # el primero es el elegido
R_CERCAS = (5, 3, 8)
HORIZONTES = (100, 50, 200)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


class Oraculo:
    def __init__(self, mundo, speed):
        self.mundo = mundo
        n = mundo.arena_size
        self.n = n
        self.c = (n // 2, n // 2)
        self.fases = [tuple(z) for z in (mundo.zone_schedule or [])]
        self.coste = mundo.coste_movimiento(speed)
        self._bfs_cache = {}

    # ── calendario ───────────────────────────────────────────────────────
    def radio_dps(self, t):
        _c, r, dps = self.mundo.anillo_en(t)
        return r, dps

    def fase_activa(self, t):
        """Indice (0..) de la ultima fase con warn <= t; None antes del primero."""
        k = None
        for i, f in enumerate(self.fases):
            if f[0] <= t:
                k = i
        return k

    def r1_en(self, t):
        k = self.fase_activa(t)
        return float(self.n) if k is None else float(self.fases[k][4])

    def arde(self, pos, t):
        r, dps = self.radio_dps(t)
        return dps > 0 and math.dist(pos, self.c) > r

    def t_arde(self, pos, t, tope=None):
        """Primer tic >= t en que `pos` arde, o None si no arde en el calendario."""
        if self.arde(pos, t):
            return t
        d = math.dist(pos, self.c)
        for (warn, shrink, done, r0, r1, dps) in self.fases:
            if done < t or not dps:
                continue
            if d > r0:
                cand = max(t, warn)
            elif d > r1:
                f = (r0 - d) / max(1e-9, (r0 - r1))
                cand = max(t, int(shrink + f * (done - shrink)))
            else:
                continue
            # afinar con el calendario exacto (interpolacion entera del mundo)
            x = cand
            while x > t and self.arde(pos, x - 1):
                x -= 1
            while not self.arde(pos, x) and x < done + 2:
                x += 1
            if self.arde(pos, x) and (tope is None or x <= tope):
                return x
        return None

    # ── geometria ────────────────────────────────────────────────────────
    def bfs(self, desde):
        """{casilla: pasos} sobre casillas no solidas, 8 vecinos."""
        desde = tuple(desde)
        D = self._bfs_cache.get(desde)
        if D is not None:
            return D
        n = self.n
        D = {desde: 0}
        frente = [desde]
        while frente:
            nuevo = []
            for (x, y) in frente:
                k = D[(x, y)] + 1
                for dx, dy in DIRS:
                    q = (x + dx, y + dy)
                    if q in D or not (0 <= q[0] < n and 0 <= q[1] < n) \
                            or self.mundo.solido(q[0], q[1]):
                        continue
                    D[q] = k
                    nuevo.append(q)
            frente = nuevo
        self._bfs_cache[desde] = D
        return D

    def a_salvo(self, q, t_llegada):
        """Sigue a salvo cuando llego: dentro del radio de ese tic Y dentro del
        radio final (r1) de la fase activa en ese tic (asi no arde en lo que
        queda de fase)."""
        if self.mundo.solido(q[0], q[1]):
            return False
        d = math.dist(q, self.c)
        r, _dps = self.radio_dps(t_llegada)
        return d <= r and d <= self.r1_en(t_llegada)

    def seguras(self, pos, t, D):
        """[(q, pasos)] casillas alcanzables que siguen a salvo al llegar."""
        out = []
        for q, k in D.items():
            if self.a_salvo(q, t + k * self.coste):
                out.append((q, k))
        return out

    @staticmethod
    def rivales_de(obs, herm, propio=None):
        """Los rivales contados en la percepcion del decisor (vistos + dichos)."""
        out = []
        for a in ((obs.get("visible") or {}).get("agents") or []):
            s = a.get("slot")
            if s == herm or s == propio or not a.get("pos"):
                continue
            out.append((s, (int(a["pos"][0]), int(a["pos"][1])),
                        bool(a.get("_contado"))))
        return out

    @staticmethod
    def cerca(q, rivales, R):
        return sum(1 for _s, p, _c in rivales if cheb(q, p) <= R)

    # ── el disparo del momento (1) ───────────────────────────────────────
    def dispara(self, pos, t, D, seg):
        """(arde_ahora, t_arde, pasos_a, holgura). holgura = tics que sobran si
        salgo ya a la segura mas cercana (negativa: ya no llego sin arder)."""
        ar = self.arde(pos, t)
        ta = self.t_arde(pos, t)
        pasos_a = min((k for _q, k in seg), default=None)
        holg = None
        if ta is not None and pasos_a is not None:
            holg = ta - t - pasos_a * self.coste
        return ar, ta, pasos_a, holg

    # ── los planes ───────────────────────────────────────────────────────
    def propone(self, pos, t, rivales, pos_herm=None):
        """Los destinos por criterio. Devuelve (planes, info).
        planes: [{"criterios": [...], "destino": (x,y), "pasos", "cheb",
                  "llegada", "propia": bool, "rivales_cerca": {R: n}}]"""
        pos = tuple(pos)
        D = self.bfs(pos)
        seg = self.seguras(pos, t, D)
        info = {"n_alcanzables": len(D), "n_seguras": len(seg),
                "n_rivales": len(rivales),
                "n_contados": sum(1 for r in rivales if r[2])}
        planes = {}

        def mete(crit, q, k):
            p = planes.get(q)
            if p is None:
                p = {"criterios": [], "destino": q, "pasos": k,
                     "cheb": cheb(pos, q), "llegada": t + k * self.coste,
                     "propia": (q == pos),
                     "rivales_cerca": {R: self.cerca(q, rivales, R)
                                       for R in R_CERCAS}}
                planes[q] = p
            p["criterios"].append(crit)

        if not seg:
            info["sin_segura"] = True
            return [], info
        R0 = R_CERCAS[0]
        # (a) la mas cercana; desempate: menos rivales cerca, luego la casilla
        q, k = min(seg, key=lambda qk: (qk[1], cheb(pos, qk[0]),
                                        self.cerca(qk[0], rivales, R0), qk[0]))
        mete("a", q, k)
        # (b) la de menos rivales contados cerca; desempate: la mas cercana
        for R in R_CERCAS:
            q, k = min(seg, key=lambda qk: (self.cerca(qk[0], rivales, R),
                                            qk[1], cheb(pos, qk[0]), qk[0]))
            mete(f"b{R}", q, k)
        # (c) la misma para los dos: minimiza el maximo de pasos de los dos
        if pos_herm is not None:
            Dh = self.bfs(tuple(pos_herm))
            comunes = []
            for q, k in seg:
                kh = Dh.get(q)
                if kh is None:
                    continue
                if not self.a_salvo(q, t + kh * self.coste):
                    continue
                comunes.append((q, k, kh))
            info["n_seguras_comunes"] = len(comunes)
            if comunes:
                q, k, kh = min(comunes, key=lambda x: (max(x[1], x[2]),
                                                       x[1] + x[2],
                                                       self.cerca(x[0], rivales, R0),
                                                       x[0]))
                mete("c", q, k)
                planes[q]["pasos_hermano"] = kh
        else:
            info["sin_hermano"] = True
        return list(planes.values()), info

    # ── el idioma de formas ──────────────────────────────────────────────
    @staticmethod
    def texto_forma(destino, H, por):
        """El JSON tal como lo escribiria un consejero, con las dos mitades.
        Lo traduce `traductor_forma.traduce` (el traductor real), no este
        archivo."""
        import json
        return json.dumps({"formas": [{"tramos": [
            {"destino": [int(destino[0]), int(destino[1])], "intencion": "ir",
             "vida": "+", "manos": "0", "vinculo": "0", "por": por},
            {"destino": None, "intencion": "esperar", "esperar": int(H),
             "vida": "+", "manos": "0", "vinculo": "0", "por": "seguir a salvo"}],
            "final": "fuera del anillo"}]})

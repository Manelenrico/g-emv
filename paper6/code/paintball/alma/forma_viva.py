"""[P5-6A · A1] Una forma, viva dentro de la partida.

Lo que en el banco era una cuenta de una vez, aqui es una cosa que dura: nace
cuando el consejero la propone, se juzga con la regla, y si la aceptan **vive**
metiendo su primer tramo en `D.candidatos` hasta que deja de ganar o hasta que
lo previsto no ocurre.

LA REGLA es la de P5-3H, sin tocarla: `forma.curva_H` con las filas de rivales
a piso y el hermano de su diario, `forma.mejor_propia_H` como comparador, y
`forma.juzga_margen` con el margen que module la confianza (A3).

SE CAE, y esto es lo nuevo del vivo:
  · en una reevaluacion deja de ganar;
  · la vida real esta por debajo de la proyectada menos 10;
  · el destino del tramo en curso ya no es alcanzable (casilla solida o fuera).

Se reevalua **al llegar a un punto de control y cada 25 tics**.
"""
from __future__ import annotations
import copy

CADA_REEVALUA = 25
VIDA_TOLERANCIA = 10.0
MAX_TRAMOS = 4
SOLIDOS = ("#", "F", "R")


class FormaViva:
    def __init__(self, ident, tramos, tick_nace, origen="consejero"):
        self.id = ident
        self.tramos = [dict(t) for t in (tramos or [])][:MAX_TRAMOS]
        self.origen = origen              # consejero | azar | mano
        self.nace = tick_nace
        self.estado = "propuesta"         # propuesta|aceptada|caida|cumplida
        self.motivo_caida = None
        self.tics = []                    # tics previstos de cada punto
        self.curva = []                   # lo proyectado en cada punto
        self.ventaja = 0.0                # el area con que compite
        self.i_punto = 0                  # cuantos puntos se han alcanzado
        self.ultima_revision = tick_nace
        self.malos = 0                    # puntos de control que fallaron

    # ── la identidad del candidato que inyecta ───────────────────────────
    def destino_actual(self):
        # [P5-8M] EL DESVIO. Cuando la forma va rodeando a un armado, el cuerpo
        # tiene que apuntar a la casilla SIGUIENTE DEL RODEO, no al destino
        # final: la receta es `ir a destino` y el `ir` busca su propio camino,
        # que volveria a meterse por la sombra. La PROMESA no cambia —`tramos`
        # y `destino_cur` siguen siendo el destino final, y la puerta sigue
        # juzgando eso—; lo que cambia es por donde se anda.
        # Si nadie pone `desvio`, esto es identico a lo de siempre.
        d = getattr(self, "desvio", None)
        if d is not None:
            return tuple(d)
        for i, tr in enumerate(self.tramos):
            if i >= self.i_punto:
                return tr.get("destino")
        return None

    def nombre(self):
        d = self.destino_actual()
        return f"_FM_ir_{d[0]}_{d[1]}" if d else "_FM_esperar"

    def receta(self, obs, mem):
        """La receta que entra en `D.candidatos`, como la del arnes."""
        d = self.destino_actual()
        if d is None:
            return {"tipo": "esperar"}
        vis = (obs.get("visible") or {})
        return {"tipo": "ir", "destino": tuple(d),
                "cuerpos": frozenset(tuple(a.get("pos") or ()) for a in
                                     (vis.get("agents") or []) if a.get("pos")),
                "recoger": mem.objetos_vistos.get(tuple(d))}

    # ── ¿toca mirarla? ───────────────────────────────────────────────────
    def toca_revisar(self, tick):
        if self.estado != "aceptada":
            return False
        if self.tics and self.i_punto < len(self.tics) \
                and tick >= self.tics[self.i_punto]:
            return True
        return (tick - self.ultima_revision) >= CADA_REEVALUA

    # ── ¿se cae porque lo previsto no ocurrio? ───────────────────────────
    def falla_lo_previsto(self, hp_real, filas_mapa, tick):
        """(se_cae, motivo). Lo que el encargo fija, ni mas ni menos."""
        if self.curva and self.i_punto > 0:
            prev = self.curva[min(self.i_punto, len(self.curva)) - 1]
            v = prev.get("vida")
            if v is not None and hp_real is not None \
                    and hp_real < v - VIDA_TOLERANCIA:
                return True, (f"la vida real {hp_real:.0f} esta por debajo de "
                              f"la proyectada {v:.0f} menos {VIDA_TOLERANCIA:.0f}")
        d = self.destino_actual()
        if d is not None and filas_mapa:
            n = len(filas_mapa)
            if not (0 <= d[0] < n and 0 <= d[1] < n) \
                    or filas_mapa[d[1]][d[0]] in SOLIDOS:
                return True, f"el destino {tuple(d)} ya no es alcanzable"
        return False, None

    def cae(self, motivo, tick):
        self.estado = "caida"
        self.motivo_caida = motivo
        self.ultima_revision = tick

    def avanza_punto(self, tick):
        self.i_punto += 1
        self.ultima_revision = tick
        if self.i_punto >= len(self.tramos):
            self.estado = "cumplida"

    # ── para el diario ───────────────────────────────────────────────────
    def registro(self):
        return {"id": self.id, "origen": self.origen, "nace": self.nace,
                "estado": self.estado, "motivo_caida": self.motivo_caida,
                "tramos": [{"destino": (list(t["destino"])
                                        if t.get("destino") else None),
                            "intencion": t.get("intencion"),
                            "esperar": t.get("esperar") or 0}
                           for t in self.tramos],
                "tics": list(self.tics), "ventaja": round(self.ventaja, 5),
                "punto": self.i_punto, "malos": self.malos}


def evalua(forma, F, estado0, obs_w, mundo, mem, suelo, herm, dia_h, pisos,
           margen, tick):
    """Pasa la forma por la regla honesta. (veredicto, ventaja, curva, tics).

    `F` es el modulo `forma`; se pasa para que este fichero no dependa de donde
    viva en la imagen. Ningun objeto del banco se modifica.
    """
    tics = [x[0] for x in F.puntos_de_control(estado0, forma.tramos)]
    if not tics:
        return "sin puntos de control", 0.0, [], []
    try:
        cf = F.curva_H(estado0, obs_w, forma.tramos, mundo, mem, suelo, tics,
                       herm, dia_h, pisos)
        cs, quien, ncd, mueve = F.mejor_propia_H(
            estado0, obs_w, list(_base(mundo, obs_w, mem, tick)), tics, mundo,
            mem, suelo, tick, herm, dia_h, pisos)
    except Exception as ex:
        return f"revienta: {type(ex).__name__}", 0.0, [], tics
    if cs is None:
        return "sin comparador", 0.0, cf, tics
    ver, ar, dt = F.juzga_margen(cf, cs, tick, margen=margen)
    return ver, (ar or 0.0), cf, tics


_BASE = {"fn": None}


def pon_base(fn):
    """El que sabe pedirle candidatos al cuerpo (se inyecta desde la policy)."""
    _BASE["fn"] = fn


def _base(mundo, obs, mem, tick):
    fn = _BASE["fn"]
    return fn(obs, mundo, mem, tick) if fn else []

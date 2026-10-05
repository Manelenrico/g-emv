"""[P5-6A · A3] La confianza que se gana por RESULTADOS, dentro de la partida.

Distinta de la de P5-4: alli se comprobaba lo DICHO sobre los rivales; aqui se
comprueba lo PROMETIDO por la forma. En cada punto de control alcanzado se
compara la `d` real con la que la forma proyecto.

  · C empieza en 0,30.
  · acierto (d_real <= d_proyectada + 0,05):  C += 0,10
  · fallo   (d_real >  d_proyectada + 0,05):  C -= 0,15
  · acotada en [0, 1].
  · el margen de la puerta lo modula C:  margen = 0,02 + 0,06 * (1 - C).
    Con C = 1 el margen es el 0,02 de P5-3H; con C = 0 es 0,08, cuatro veces
    mas duro. Confiar poco = pedir mas ventaja para dejar pasar una forma.
  · si C llega a 0 y ya van CINCO formas aceptadas que acabaron mal, el cuerpo
    deja de citar al consejero durante 500 tics. **El cuerpo puede callar al
    consejero**, y queda anotado.

Todo cambio de C se apunta con la forma y el punto de control que lo causo,
para que el diario lo cuente entero.
"""
from __future__ import annotations

C0 = 0.30
SUBE, BAJA = 0.10, 0.15
TOL_D = 0.05
MARGEN_BASE, MARGEN_RANGO = 0.02, 0.06
MALAS_PARA_CALLAR = 5
CALLADO_TICS = 500


class Confianza:
    def __init__(self, c0=C0):
        self.C = float(c0)
        self.historia = []          # los cambios, para el diario
        self.malas = 0              # formas aceptadas que acabaron mal
        self.callado_hasta = None   # tic hasta el que el cuerpo no cita

    # ── la puerta ────────────────────────────────────────────────────────
    def margen(self):
        return MARGEN_BASE + MARGEN_RANGO * (1.0 - self.C)

    # ── el resultado de un punto de control ──────────────────────────────
    def comprueba(self, d_real, d_proyectada, tick, forma_id, i_punto):
        """(veredicto, C_antes, C_despues). None si no hay con que comparar."""
        if d_real is None or d_proyectada is None:
            return None, self.C, self.C
        antes = self.C
        ok = (d_real <= d_proyectada + TOL_D)
        self.C = min(1.0, max(0.0, self.C + (SUBE if ok else -BAJA)))
        self.historia.append({
            "tick": tick, "forma": forma_id, "punto": i_punto,
            "d_real": round(float(d_real), 5),
            "d_proyectada": round(float(d_proyectada), 5),
            "veredicto": "acierto" if ok else "fallo",
            "C_antes": round(antes, 4), "C": round(self.C, 4),
            "margen": round(self.margen(), 4)})
        return ("acierto" if ok else "fallo"), antes, self.C

    # ── el cierre de una forma ───────────────────────────────────────────
    def forma_cerrada(self, mal, tick):
        """`mal` = algun punto de control de esa forma fallo. Devuelve si el
        cuerpo acaba de callar al consejero."""
        if mal:
            self.malas += 1
        if self.C <= 0.0 and self.malas >= MALAS_PARA_CALLAR \
                and self.callado_hasta is None:
            self.callado_hasta = tick + CALLADO_TICS
            self.historia.append({
                "tick": tick, "k": "el cuerpo calla al consejero",
                "hasta": self.callado_hasta, "malas": self.malas,
                "C": round(self.C, 4)})
            return True
        return False

    def callado(self, tick):
        if self.callado_hasta is None:
            return False
        if tick >= self.callado_hasta:
            self.callado_hasta = None
            self.malas = 0          # se le da otra oportunidad, declarado
            return False
        return True

    # ── para el diario ───────────────────────────────────────────────────
    def resumen(self):
        return {"C": round(self.C, 4), "margen": round(self.margen(), 4),
                "malas": self.malas, "callado_hasta": self.callado_hasta,
                "cambios": len([h for h in self.historia if "veredicto" in h])}

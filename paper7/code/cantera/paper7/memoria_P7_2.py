"""[P7-2] LA REGLA DE MEMORIA (decision de metodo de la mesa; no se ajusta despues de ver datos). Archivo experimental: el banco
la usa por fuera; el cuerpo congelado no la importa.

  b(objeto, situacion) = media ponderada de recuerdos.
  Recuerdo de nacimiento: el valor del catalogo, con peso P_NAC (3), nacido el dia 0.
  Experiencia i (dia d_i, valor vivido v_i): peso w_i = intensidad_i x olvido(d - d_i);
      intensidad_i = min(TOPE (2), 1 + |v_i - b_antes| / catalogo), con b_antes = la creencia en el momento de vivirla;
      olvido(k) = OLVIDO^k (0,95), tambien para el recuerdo de nacimiento (k = d - 0).
  En el dia d, b = sum(w_i(d) * v_i) / sum(w_i(d)) sobre todos los recuerdos (nacimiento incluido).
  Dentro de un mismo dia las experiencias se suman en orden: b_antes de la segunda ya incluye la primera.
"""
from dataclasses import dataclass, field


@dataclass
class Creencia:
    catalogo: float
    olvido: float = 0.95
    peso_nacimiento: float = 3.0
    tope: float = 2.0
    recuerdos: list = field(default_factory=list)     # [(dia, valor, intensidad)]; el de nacimiento va primero

    def __post_init__(self):
        self.recuerdos.append((0, float(self.catalogo), float(self.peso_nacimiento)))

    def b(self, dia: int) -> float:
        """La creencia vista desde el dia `dia` (los recuerdos de dias posteriores no cuentan)."""
        num = den = 0.0
        for d_i, v_i, inten in self.recuerdos:
            if d_i > dia:
                continue
            w = inten * (self.olvido ** (dia - d_i))
            num += w * v_i; den += w
        return num / den if den > 0 else float(self.catalogo)

    def vive(self, dia: int, valor: float) -> float:
        """Anade la experiencia del dia `dia` con valor vivido `valor`; devuelve la creencia nueva (ese mismo dia)."""
        antes = self.b(dia)
        inten = min(self.tope, 1.0 + abs(float(valor) - antes) / float(self.catalogo)) if self.catalogo else 1.0
        self.recuerdos.append((int(dia), float(valor), inten))
        return self.b(dia)

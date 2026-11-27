"""[P8] Prompt 171: lo común de las cinco figuras pulidas (figura1_valle_171.py … figura5_tres_maneras_171.py). Es estilo_170.py (importado: los mismos
colores, la misma letra, el mismo intervalo) con tres cambios y nada más:
  (1) todos los textos de las figuras salen de un único fichero de rótulos, rotulos_figuras.csv, una fila por texto y tres columnas: clave, es, en. La
      columna en está vacía hasta que llegue el texto inglés del paper; si falta un texto en el idioma pedido, el programa para y dice cuáles faltan;
  (2) el separador decimal de los números de los ejes también sale de ese fichero (clave «separador_decimal»: «,» en español);
  (3) el idioma se pasa como parámetro (--idioma es, por defecto es) y cada figura se guarda con su sufijo (fig2_vivas_es.png y .pdf), a 300 ppp, en una
      carpeta aparte, figuras_171/; las del 170 (figuras/) no se tocan.
Los datos y los tamaños de las figuras no cambian: cada programa del 171 hace las mismas cuentas que el del 170 y comprueba que sus tablas son las mismas."""
import argparse, csv, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
# [prompt 175] los argumentos se guardan ANTES de importar estilo_170: por debajo se carga un módulo de la escalera que vacía sys.argv
# (y --idioma en se perdía: salía siempre el español, sin avisar)
ARGV = list(sys.argv[1:])
import estilo_170 as S0
from matplotlib.ticker import ScalarFormatter
E6, boot, plt, MUNDOS, SEM, DIA, COLOR, REJILLA, DPI = S0.E6, S0.boot, S0.plt, S0.MUNDOS, S0.SEM, S0.DIA, S0.COLOR, S0.REJILLA, S0.DPI
f1, f2, f3, fb, tabla_barras = S0.f1, S0.f2, S0.f3, S0.fb, S0.tabla_barras
estilo = S0.estilo
ROTULOS = os.path.join(AQUI, "rotulos_figuras.csv")
FIG = os.path.join(AQUI, "figuras_171")
IDIOMAS = ("es", "en")


def idioma():
    a = argparse.ArgumentParser(); a.add_argument("--idioma", default="es", choices=IDIOMAS); return a.parse_args(ARGV).idioma


def lee_rotulos():
    with open(ROTULOS, encoding="utf-8", newline="") as f: filas = list(csv.DictReader(f))
    assert filas and list(filas[0]) == ["clave", "es", "en"], "rotulos_figuras.csv: las columnas son clave, es, en"
    claves = [r["clave"] for r in filas]; assert len(claves) == len(set(claves)), "claves repetidas en rotulos_figuras.csv"
    return {r["clave"]: r for r in filas}


class Rotulos:
    """R("fig2.eje_y") da el texto en el idioma elegido; R("fig3.duelo_casos", n=136) rellena los huecos {n}. Apunta qué claves se usan."""
    def __init__(self, id_):
        self.id, self.T, self.usadas = id_, lee_rotulos(), set()
    def __call__(self, clave, **k):
        self.usadas.add(clave); r = self.T.get(clave)
        if r is None: sys.exit(f"falta la clave {clave!r} en rotulos_figuras.csv")
        t = r[self.id]
        if not t: sys.exit(f"rotulos_figuras.csv: la clave {clave!r} no tiene texto en «{self.id}» (la columna está vacía hasta que llegue el texto)")
        return t.format(**k) if k else t
    def comprueba(self, prefijos):
        """todas las claves de la figura (las que empiezan por sus prefijos) tienen texto en este idioma"""
        falta = [c for c, r in self.T.items() if c.startswith(prefijos) and not r[self.id]]
        if falta: sys.exit(f"rotulos_figuras.csv: sin texto en «{self.id}»: {', '.join(falta)}")
    def mundo(self, mu): return self(f"mundo.{mu}")


class Decimal(ScalarFormatter):
    """el formateador de siempre de matplotlib, con el separador decimal del idioma"""
    def __init__(self, sep):
        super().__init__(); self.sep = sep
    def __call__(self, x, pos=None):
        return super().__call__(x, pos).replace(".", self.sep)


def decimales(R, *axs):
    """solo el eje y: el x lleva nombres de mundos (2, 4, 5) o días enteros (3), que no tienen decimales y conservan su formato"""
    for ax in axs: ax.yaxis.set_major_formatter(Decimal(R("separador_decimal")))


def guarda(fig, nom, id_):
    os.makedirs(FIG, exist_ok=True); rutas = []
    for ext in ("png", "pdf"):
        p = os.path.join(FIG, f"{nom}_{id_}.{ext}"); fig.savefig(p, dpi=DPI); rutas.append(p)
    plt.close(fig); return rutas


def barras(ax, val, jug, rot, ancho, R, mundos=MUNDOS):
    """estilo_170.barras tal cual (mismas posiciones, anchos, colores e intervalos), con los nombres de los mundos sacados de los rótulos"""
    out = S0.barras(ax, val, jug, rot, ancho, mundos); ax.set_xticklabels([R.mundo(mu) for mu in mundos]); return out


def comprueba_tabla(nom, lineas):
    """las líneas de la tabla de números que sale ahora están, tal cual, en el .txt del 170 (figuras/nom.txt): los datos no han cambiado"""
    viejo = set(open(os.path.join(S0.FIG, f"{nom}.txt"), encoding="utf-8").read().splitlines())
    falta = [l for l in lineas if l.startswith("|") and l not in viejo and not l.startswith("|---")]
    assert not falta, (nom, falta[:3]); return sum(1 for l in lineas if l.startswith("|") and not l.startswith("|---"))

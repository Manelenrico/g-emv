"""[P7-23] EL RECUERDO CON SU MARCA EMOCIONAL, Y RECORDAR POR PARECIDO (diseno de Manel, 7-oct; numeros de la mesa). Archivo experimental del
siete; el cuerpo congelado no lo importa. Extiende el cuaderno de P7-5 (`cuaderno_P7.Cuaderno`) sin tocarlo: el archivo que viaja es el mismo
JSON (objeto -> situacion -> lista de recuerdos), y cada recuerdo lleva ademas:
  contexto    {"dentro": bool, "golpeado_48": bool}        (dentro o fuera del circulo; dano recibido en los 48 instantes anteriores a abrir)
  foto        {"dolor_F", "dolor_R", "dolor_S", "positivo", "d"}   (la foto emocional al abrir, como en P7-21: dolor por dominio = suma de las filas
              con signo -, positivo = suma de las M con signo +, d = distancia total)
  acciones    [lo elegido al abrir, y las tres elecciones anteriores]
  efecto, importancia, intensidad, al_menos, dia, tick: como en el cuaderno de P7-5 (efecto con el "al menos" de P7-7 si la vida toco techo).
  corte       True si el canal se corto (efecto 0 en cuerpo y en recursos; recuerdo de peso 1).
RECORDAR POR PARECIDO (como P7-22, con los dos cambios de P7-23):
  peso = intensidad x OLVIDO^dias x parecido;  parecido = parecido emocional x parecido de contexto;
  parecido emocional = exp(-distancia(foto de ahora, foto del recuerdo) / S_EMO), distancia euclidea en el vector de 5; sin foto, 1;
  parecido de contexto = (1 si coincide dentro/fuera, si no CTX_DENTRO = 0,05) x (1 si coincide golpeada/no, si no CTX_GOLPE = 0,5).
  El recuerdo neutro (efecto 0, peso 1) entra en la media; los "al menos" del cuerpo solo si estan por encima de la creencia de los firmes (P7-7).
  creencia_vivida = suma(w e) / suma(w) (sin el neutro: la ignorancia descuenta una sola vez en la mezcla, P7-14); ignorancia = 1 / (1 + suma(w)).
S_EMO = 0,8304: la mediana de las distancias entre pares de aperturas de los diarios de APRENDE (P7-22, `P7_22_fijado.json`), fijada antes.
"""
import math
from cuaderno_P7 import Cuaderno, DOMINIOS, OLVIDO, PESO_NEUTRO

S_EMO = 0.8304
CTX_DENTRO = 0.05
CTX_GOLPE = 0.5
CLAVES_FOTO = ("dolor_F", "dolor_R", "dolor_S", "positivo", "d")


def foto_de_radio(radio):
    """La foto emocional de una radiografia del cuerpo (lo que el diario guarda en RADIOGRAFIA.ahora), o None."""
    a = (radio or {}).get("ahora") or {}; filas = a.get("filas") or {}
    if not filas: return None
    f = {"dolor_F": 0.0, "dolor_R": 0.0, "dolor_S": 0.0, "positivo": 0.0, "d": float((radio or {}).get("d_ahora") or 0.0)}
    for fila in filas.values():
        if not isinstance(fila, dict): continue
        if fila.get("signo") == "-":
            for eje, k in (("F", "dolor_F"), ("R", "dolor_R"), ("S", "dolor_S")): f[k] += float(fila.get(eje) or 0.0)
        else: f["positivo"] += float(fila.get("M") or 0.0)
    return {k: round(v, 4) for k, v in f.items()}


def vec(f): return tuple(float(f.get(k) or 0.0) for k in CLAVES_FOTO)
def dist(a, b): return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def parecido(ahora_ctx, ahora_foto, r):
    pe = 1.0
    if ahora_foto and r.get("foto"): pe = math.exp(-dist(vec(ahora_foto), vec(r["foto"])) / S_EMO)
    c = r.get("contexto") or {}
    pc = (1.0 if c.get("dentro") == ahora_ctx.get("dentro") else CTX_DENTRO) * (1.0 if c.get("golpeado_48") == ahora_ctx.get("golpeado_48") else CTX_GOLPE)
    return pe * pc


class CuadernoP23(Cuaderno):
    """El cuaderno de P7-5 con recuerdos marcados y recuerdo por parecido. Lee y escribe el mismo archivo."""
    @classmethod
    def desde(cls, c):
        c.__class__ = cls; return c

    def apunta_P23(self, objeto, contexto, foto, acciones, efecto, importancia, tick=None, al_menos=False, corte=False):
        sit = "dentro" if contexto.get("dentro") else "fuera"
        r = self.apunta(objeto, sit, efecto, importancia, tick=tick, al_menos=al_menos)
        r["contexto"] = {"dentro": bool(contexto.get("dentro")), "golpeado_48": bool(contexto.get("golpeado_48"))}; r["foto"] = foto; r["acciones"] = list(acciones or [])[-4:]; r["corte"] = bool(corte)
        return r

    def recuerdos_de(self, objeto):
        return [r for sit in ((self.objetos.get(objeto) or {}).get("situaciones") or {}).values() for r in sit]

    def creencia_parecido(self, objeto, contexto, foto, dia=None):
        """Por dominio: (creencia vivida, suma de pesos). None si no hay ningun recuerdo vivido del objeto."""
        rec = self.recuerdos_de(objeto)
        if not rec: return None, 0.0
        d_act = self.dia_actual() if dia is None else dia
        pesos = [(float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"]))) * parecido(contexto, foto, r), r) for r in rec]
        out = {}
        for dom in DOMINIOS:
            num = 0.0; den = 0.0; techo = []
            for w, r in pesos:
                if dom == "cuerpo" and r.get("al_menos"): techo.append((w, float(r["efecto"][dom]))); continue
                num += w * float(r["efecto"][dom]); den += w
            if techo:                                           # [P7-7] los "al menos": solo los que estan por encima de la creencia firme (con el neutro)
                base = num / (den + PESO_NEUTRO)
                for w, e in techo:
                    if e > base: num += w * e; den += w
            out[dom] = (num / den) if den > 0 else 0.0
        suma = sum(w for w, _ in pesos)
        return out, suma

    def ignorancia_parecido(self, objeto, contexto, foto, dia=None):
        _, suma = self.creencia_parecido(objeto, contexto, foto, dia); return PESO_NEUTRO / (PESO_NEUTRO + suma)

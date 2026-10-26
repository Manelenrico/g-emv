"""[P7-5] EL CUADERNO: lo que una criatura aprende de las cosas, que viaja de partida en partida en un archivo (nunca en el estado del
proceso: una vida por proceso). Archivo experimental del siete; el cuerpo congelado no lo importa.

Por objeto y situacion (botiquin: "dentro" | "fuera" del circulo, como lo percibe el cuerpo al usarlo), una lista de recuerdos. Cada
recuerdo es una HUELLA por dominio (cuerpo, recursos, vinculo): EFECTO (lo que la cosa hizo, menos lo esperado sin ella) e IMPORTANCIA
con signo (cuanto movio el malestar del cuerpo en ese dominio: > 0 dolor, < 0 alivio).
  creencia(dominio) = media ponderada de los efectos; peso de un recuerdo vivido = intensidad x OLVIDO^(dia_actual - dia_i);
  intensidad = 1 + min(1, (|imp_cuerpo| + |imp_recursos| + |imp_vinculo|) / E), E = 1,5 (tres ejes con techo 0,5); tope 2.
  EL CENTRO (correccion 3 de la mesa): cada creencia lleva un recuerdo NEUTRO (efecto 0 en los tres dominios) de peso 1 que no se apaga;
  con ningun recuerdo vivido la creencia es "no se" (None): el neutro solo pesa cuando hay algo vivido.
  [P7-6] LA IGNORANCIA de una clase de objeto (cambio 1 de Manel): peso del neutro / (peso del neutro + suma de los pesos de los recuerdos
  vividos de esa clase, en todas sus situaciones, vistos desde el dia actual). Nunca probado: 1; recien probado: baja; con dias sin vivirlo
  sube despacio (los vividos se apagan, el neutro no), sin volver nunca a 1. Sustituye a la cuenta de usos de P7-5, que desaparece.
  [P7-7] EL RECUERDO CON TECHO (decision 1 de la mesa): si durante la ventana la vida llega al maximo, el recuerdo del cuerpo se marca
  "al menos" (`al_menos`: lo ganado es una cota inferior). Un recuerdo "al menos" solo entra en la media del efecto del dominio cuerpo si su
  valor esta por encima de la creencia que forman los recuerdos firmes con el neutro (puede subirla, nunca bajarla); con ningun recuerdo
  firme esa creencia es la del neutro, 0, y un "al menos" positivo entra. En los otros dos dominios y en la ignorancia cuenta con su peso
  como cualquier recuerdo.
Formato del archivo (JSON): {"criatura": asiento, "dia": n, "objetos": {id: {"situaciones": {sit: [recuerdos]}}}}.
"""
import json, os

OLVIDO = 0.95
E_INTENSIDAD = 1.5
PESO_NEUTRO = 1.0
DOMINIOS = ("cuerpo", "recursos", "vinculo")


class Cuaderno:
    def __init__(self, criatura=None):
        self.criatura = criatura; self.dia = 0; self.objetos = {}

    # ── lectura / escritura ──
    @classmethod
    def lee(cls, ruta, criatura=None):
        c = cls(criatura)
        if ruta and os.path.exists(ruta):
            d = json.load(open(ruta, encoding="utf-8"))
            c.criatura = d.get("criatura", criatura); c.dia = int(d.get("dia") or 0); c.objetos = d.get("objetos") or {}
        return c

    def escribe(self, ruta):
        self.dia += 1                                   # cada escritura cierra un dia
        os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
        json.dump(self.volcado(), open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return ruta

    def volcado(self):
        return {"criatura": self.criatura, "dia": self.dia, "objetos": self.objetos, "creencias": self.creencias()}

    # ── recuerdos ──
    def _obj(self, objeto):
        return self.objetos.setdefault(objeto, {"situaciones": {}})

    def dia_actual(self):
        """El dia que se esta viviendo: los escritos mas uno."""
        return self.dia + 1

    def pesos_vividos(self, objeto, dia=None):
        """Suma de los pesos de todos los recuerdos vividos de la clase, en todas sus situaciones, vistos desde `dia`."""
        d_act = self.dia_actual() if dia is None else dia
        return sum(float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"]))) for sit in ((self.objetos.get(objeto) or {}).get("situaciones") or {}).values() for r in sit)

    def ignorancia(self, objeto, dia=None):
        """[P7-6] peso del neutro / (peso del neutro + pesos vividos): 1 si nunca lo ha probado."""
        return PESO_NEUTRO / (PESO_NEUTRO + self.pesos_vividos(objeto, dia))

    def apunta(self, objeto, situacion, efecto, importancia, tick=None, al_menos=False):
        """efecto e importancia: dicts por dominio; al_menos [P7-7]: la vida toco techo en la ventana (el efecto del cuerpo es cota inferior).
        Devuelve el recuerdo escrito (con su intensidad)."""
        antes = self.creencia(objeto, situacion)
        suma = sum(abs(float(importancia.get(d) or 0.0)) for d in DOMINIOS)
        inten = 1.0 + min(1.0, suma / E_INTENSIDAD)
        r = {"dia": self.dia_actual(), "tick": tick, "efecto": {d: round(float(efecto.get(d) or 0.0), 4) for d in DOMINIOS},
             "importancia": {d: round(float(importancia.get(d) or 0.0), 4) for d in DOMINIOS}, "intensidad": round(inten, 4),
             "creencia_antes": antes, "al_menos": bool(al_menos)}
        self._obj(objeto)["situaciones"].setdefault(situacion, []).append(r)
        return r

    # ── creencias ──
    def creencia(self, objeto, situacion, dia=None, con_neutro=True):
        """Por dominio, media ponderada de los efectos con el neutro en el centro; None si no hay ningun recuerdo vivido.
        [P7-14, arreglo de la mesa] `con_neutro=False`: la media de LO VIVIDO, sin el recuerdo neutro (lo usan las ganas y la imaginacion de
        usar, que ya descuentan la ignorancia en la mezcla con la esperanza: asi la ignorancia descuenta una sola vez)."""
        rec = ((self.objetos.get(objeto) or {}).get("situaciones") or {}).get(situacion) or []
        if not rec:
            return None
        d_act = self.dia_actual() if dia is None else dia
        out = {}
        for dom in DOMINIOS:
            num = 0.0; den = PESO_NEUTRO if con_neutro else 0.0      # el neutro: efecto 0, peso 1, no se apaga
            techo = []
            for r in rec:
                w = float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"])))
                if dom == "cuerpo" and r.get("al_menos"): techo.append((w, float(r["efecto"][dom]))); continue
                num += w * float(r["efecto"][dom]); den += w
            if techo:                                    # [P7-7] los "al menos": solo los que estan por encima de la creencia firme
                base = (num / den) if den > 0 else 0.0
                for w, e in techo:
                    if e > base: num += w * e; den += w
            if den <= 0: return None                    # (solo sin neutro: ningun recuerdo entra en la media)
            out[dom] = round(num / den, 4)
        return out

    def recuerdos(self, objeto=None):
        """Lista plana de (objeto, situacion, recuerdo)."""
        return [(o, s, r) for o, d in self.objetos.items() if objeto in (None, o) for s, rec in (d.get("situaciones") or {}).items() for r in rec]

    def creencia_cuerpo(self, objeto, situacion):
        c = self.creencia(objeto, situacion); return None if c is None else c["cuerpo"]

    def creencia_max_cuerpo(self, objeto):
        """La creencia del cuerpo en la situacion donde mas vale; None si no sabe nada."""
        vals = [self.creencia_cuerpo(objeto, s) for s in ((self.objetos.get(objeto) or {}).get("situaciones") or {})]
        vals = [v for v in vals if v is not None]
        return max(vals) if vals else None

    def creencia_vivida_cuerpo(self, objeto, situacion):
        """[P7-14] La creencia del cuerpo sin el neutro (media de lo vivido); None si no sabe nada."""
        c = self.creencia(objeto, situacion, con_neutro=False); return None if c is None else c["cuerpo"]

    def creencia_vivida_max_cuerpo(self, objeto):
        vals = [self.creencia_vivida_cuerpo(objeto, s) for s in ((self.objetos.get(objeto) or {}).get("situaciones") or {})]
        vals = [v for v in vals if v is not None]
        return max(vals) if vals else None

    def creencias(self):
        return {o: {s: self.creencia(o, s) for s in (d.get("situaciones") or {})} | {"ignorancia": round(self.ignorancia(o), 4), "pesos_vividos": round(self.pesos_vividos(o), 4)} for o, d in self.objetos.items()}

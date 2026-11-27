"""[P8] Prompt 146 (taller): RG69, la reserva. Clase hija de la criatura (cuerpo_valle.Criatura); RG68r y las demás clases congeladas no se tocan.
DECISIÓN DE MANEL (diseño): la reserva vale por el hambre que te ahorrará. Cuando la criatura tiene hambre para poder comer (la regla del mundo: hambre ≥
criaturas.harta_por_debajo, valle/mundo.py:486-489; se lee de valle/config_valle.json, no se copia), comerse lo que lleva en la bolsa NO cuenta como
pérdida de recursos: es usar la reserva, no perderla. Tener comida guardada sigue siendo ganancia mientras no la necesita. Ningún número nuevo.
DÓNDE (prompt 145): en la foto de «comer», la bolsa imaginada pierde la comida comida (cuerpo_valle.py:2625-2629), y las dos filas de recursos que cuentan
la comida guardada la leen de ahí: V-RECURSOS, la ganancia por la comida que tiene (vivir_bien, cuerpo_valle.py:2261-2276), y R-CARENCIA, la pérdida por
la que le falta (falta_comida, cuerpo_valle.py:2310-2314, desde _filas_rg). Las dos son la capa de la criatura: model.py no se toca.
EL CAMBIO (reserva_v69=True): en esas dos cuentas, y solo en ellas, si la foto es la de comerse ahora una comida (f["usa"] == "comida") y su hambre de
ahora es ≥ harta, la bolsa se cuenta con esa comida dentro. Todo lo demás de la foto (el hambre que quita, el gusto, el sabor, las otras filas) sigue
igual; las fotos de las demás acciones y la de ahora no cambian. Con reserva_v69=False es RG68r."""
import json, os
import cuerpo_valle as CV
_VALLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, "valle", "config_valle.json")
HARTA = float(json.load(open(_VALLE, encoding="utf-8"))["criaturas"]["harta_por_debajo"])


class RG69(CV.Criatura):
    def __init__(self, *a, reserva_v69=False, **k):
        super().__init__(*a, **k); self.reserva_v69 = bool(reserva_v69); self.cuenta_v69 = {"con_reserva": 0}

    def _reserva(self, f):
        """la foto de comerse ahora una comida, con hambre para poder comer: la bolsa con esa comida dentro (para las cuentas de recursos)"""
        if not self.reserva_v69 or f.get("usa") != "comida" or float(self.obs["yo"]["hambre"]) < HARTA: return f
        return dict(f, bolsa=list(f["bolsa"]) + ["comida"])

    def falta_comida(self, f):
        return super().falta_comida(self._reserva(f))

    def vivir_bien(self, f, F):
        """vivir_bien solo lee la bolsa para la comida guardada (V-RECURSOS; y, con radar_v36, el tope de V-RADAR-RECURSOS sale de ella): lo demás, de F"""
        f2 = self._reserva(f)
        if f2 is not f: self.cuenta_v69["con_reserva"] += 1
        return super().vivir_bien(f2, F)

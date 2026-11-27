"""[P8] Prompt 143 (taller): VC1, la voz de ir a casa. Hija de la criatura (cuerpo_valle.Criatura) con los interruptores de RG68r (banco_v7.VARS["RG68r"]) y uno
más, `a_casa`. Con a_casa apagado no se calcula nada nuevo y cada método llama al de siempre: tiene que salir idéntica a RG68r (la puerta, lanza_vc1.py puerta).
RG68r, las clases congeladas, cuerpo_valle.py y el mundo no se tocan.
CÓMO IMAGINA A LA HERMANA RG68r: en la foto de cada candidato (las filas, con H > 0 turnos imaginados), la hermana está en `pareja_pos`, donde la vio u oyó por
última vez: quieta donde está (la pieza que la imagina moviéndose, imagina_v45, está apagada en RG68r).
LO QUE HACE CON a_casa ENCENDIDO (punto 2 y 3 del prompt 143; lo que el prompt no dice, elegido lo más simple y dicho aquí):
  - «LA HERMANA EN CASA AL FINAL DE LO IMAGINADO»: en las filas de una foto con H > 0, `pareja_pos` pasa a ser la casilla de dentro de su casa (las celdas de
    la casa menos la puerta) más cerca (Chebyshev; a igual distancia, la primera por orden) de donde se imagina ella misma al final (foto["pos"]); lo demás de
    la hermana (lo que lleva, si está herida…) no cambia. Antes se calcula «el ahora» con la hermana donde está, como hace la pieza I (cuerpo_valle.py:1466).
  - CUÁNDO PUEDE SONAR: en cada decisión (no cuando sigue un destino comprometido ni cuando hace una llamada: entonces no decide) con el turno del día entre
    180 y 399, si ella está despierta y no está dentro de su casa (en una celda de la casa que no es la puerta), si su hermana está viva y despierta (el último
    turno no durmió) y a 7 casillas o menos (Chebyshev: el alcance «medio» de las llamadas del mundo, llamadas_voz.alcance.medio, la voz normal), y si no dura
    ya una voz suya. Lo de la hermana (viva, despierta, dónde) lo pone el lanzador desde el mundo (ESTADO): la voz llega o no llega según el mundo, como el oído.
  - LA SEGUNDA FOTO: en esa decisión, aparte, sin tocar ningún sorteo, el malestar de cada candidato con la hermana imaginada en casa. Si el menor es el de «ir
    a casa» (a igual malestar con otro, también), suena la voz. Vale también si «ir a casa» ya era lo elegido.
  - LA VOZ dura 44 turnos para quien la oye: los turnos t+1 a t+44 (t, el turno en que suena; todas deciden a la vez con lo que ven en t). Mientras dura la
    suya (hasta t+44), la que la dio no la repite. Si la oye otra vez, vuelve a durar 44 desde la nueva.
  - EN QUIEN LA OYE: mientras dura, su foto de siempre imagina a la hermana (quien la dio) en casa al final de lo imaginado, igual que la segunda foto. Nada más.
    En cada decisión mientras la oye se apunta, aparte, lo que habría elegido sin haberla oído (el candidato de menor malestar con la hermana donde está; si lo
    elegido empata con él, no cambió).
  - a_casa_calla (solo para la comprobación de que calcular aparte no toca nada): calcula todo y apunta las voces, pero la foto de quien oye no cambia.
Lo apuntado queda en vc_voces (cada voz) y vc_oye (cada decisión oyendo), y vc_cuenta (decisiones en que pudo sonar)."""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import cuerpo_valle as CV
import diario_v1 as V1                                                          # (la configuración del mundo, leída: el alcance de la voz)
DIA = V1.DIA; DESDE = 180; DURA = 44; ALCANCE = int(V1.CFG["llamadas_voz"]["alcance"]["medio"])
ESTADO = {}                                                                     # (del mundo, lo pone el lanzador: id -> (pos, dormida, muerta), como está al ver el turno)
OIDA = {}                                                                       # (quién oye qué voz: id -> la voz)
ACT = {"c": None}                                                               # (la criatura que está decidiendo, para la segunda foto)
cheb = lambda p, q: max(abs(p[0] - q[0]), abs(p[1] - q[1]))
def nom(acc): return acc.get("que") or acc.get("accion")
def nueva_partida(): ESTADO.clear(); OIDA.clear(); ACT["c"] = None

_st0 = CV.PL.select_tiebreak
def _sel(nombres, preds, terminal, meta, *a, **k):
    e = _st0(nombres, preds, terminal, meta, *a, **k)
    c = ACT["c"]
    if c is not None: c._vc_mira(nombres, preds)
    return e
CV.PL.select_tiebreak = _sel


class VC1(CV.Criatura):
    def __init__(self, *a, a_casa=False, a_casa_calla=False, **k):
        super().__init__(*a, **k)
        self.a_casa = bool(a_casa); self.a_casa_calla = bool(a_casa_calla); self._vc_casa = False; self._vc_ult = -10 ** 9
        self.vc_voces = []; self.vc_oye = []; self.vc_cuenta = {"decisiones_tarde": 0, "pudo_sonar": 0}
        self._vc_dentro = sorted(self.casa_celdas - {self.mi_puerta}); self._vc_m = None

    def _vc_cel(self, p):
        return min(self._vc_dentro, key=lambda q: (cheb(q, p), q))

    def filas(self, f):
        if not (self._vc_casa and f.get("H", 0) > 0 and not self.pareja_muerta): return super().filas(f)
        t = self.obs["turno"]
        if self.rg and self.rg_gan and self._F_ahora[0] != t: self._F_ahora = (t, self._filas_rg(self.foto_ahora(), ganancias=False))     # el ahora, donde está
        p0 = self.pareja_pos; self.pareja_pos = self._vc_cel(tuple(f["pos"]))
        try: return super().filas(f)
        finally: self.pareja_pos = p0

    def _vc_d(self, acc, casa):
        v0 = self._vc_casa; self._vc_casa = casa
        try: return round(self._compone(self.filas(self.foto(acc)))[1], 9)
        finally: self._vc_casa = v0

    def _vc_mira(self, nombres, preds):
        """(dentro de la decisión, antes de los desempates) lo que se calcula aparte"""
        m = self._vc_m; m["nombres"] = list(nombres); m["acc"] = {n: preds[n]["acc"] for n in nombres}; d = {n: preds[n]["d"] for n in nombres}
        if m["oye"] is not None: m["d_sin"] = d if not self._vc_casa else {n: self._vc_d(preds[n]["acc"], False) for n in nombres}
        if m["puede"]: m["d_casa"] = d if self._vc_casa else {n: self._vc_d(preds[n]["acc"], True) for n in nombres}

    def actua(self, obs, info):
        if not self.a_casa: return super().actua(obs, info)
        t = obs["turno"]; k = t % DIA; yo = ESTADO.get(self.a); her = ESTADO.get(self.hermana)
        oye = OIDA.get(self.a); oye = oye if (oye is not None and oye["t"] < t <= oye["t"] + DURA) else None
        dentro = tuple(obs["yo"]["pos"]) in self._vc_dentro
        puede = (k >= DESDE and yo is not None and not yo[1] and not dentro and her is not None and not her[2] and not her[1]
                 and cheb(yo[0], her[0]) <= ALCANCE and t > self._vc_ult + DURA)
        self._vc_m = {"oye": oye, "puede": puede, "nombres": None}; self._vc_casa = oye is not None and not self.a_casa_calla; ACT["c"] = self
        try: acc = super().actua(obs, info)
        finally: ACT["c"] = None; self._vc_casa = False
        m = self._vc_m; self._vc_m = None
        if m["nombres"] is None: return acc                                     # (no decidió: sigue un destino o llama)
        el = self.ultima["elegido"]; A = m["acc"]
        if k >= DESDE: self.vc_cuenta["decisiones_tarde"] += 1
        if oye is not None:
            d0 = m["d_sin"]; m0 = min(d0.values()); sin = el if d0[el] <= m0 + 1e-9 else min(n for n in m["nombres"] if d0[n] <= m0 + 1e-9)
            self.vc_oye.append({"t": t, "a": self.a, "voz": oye["id"], "elige": nom(A[el]), "sin_oir": nom(A[sin]), "cambio": sin != el})
        if puede:
            self.vc_cuenta["pudo_sonar"] += 1; d2 = m["d_casa"]; m2 = min(d2.values())
            if any(A[n].get("que") == "ir_casa" and d2[n] <= m2 + 1e-9 for n in m["nombres"]):
                v = {"id": f"{self.a}-{t}", "t": t, "k": k, "de": self.a, "a": self.hermana, "pos_de": list(yo[0]), "pos_a": list(her[0]),
                     "ya_era": A[el].get("que") == "ir_casa", "elige": nom(A[el]), "responde_a": oye["id"] if oye is not None else None}
                self.vc_voces.append(v); OIDA[self.hermana] = v; self._vc_ult = t
        return acc

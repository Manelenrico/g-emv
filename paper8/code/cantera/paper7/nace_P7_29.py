"""[P7-29] ARREGLAR LO QUE HUNDIA A LA QUE RECUERDA, Y LA CURIOSIDAD DEL CUANTO (decisiones de la mesa y diseno de Manel, 8-oct). Pieza enganchada
DESDE FUERA, despues de `descubre_P7.aplica`, `pide_P7.aplica` y `nace_P7_23.aplica`, sobre el cuerpo congelado del seis. Interruptor GEMV_P7_29=1
(apagado por defecto: con 0 no toca nada y F1 reproduce A4). Con GEMV_P7_SABE=1 (TECHO) solo queda la cache (que sin cuaderno no hace nada).

LO QUE SE ENCONTRO ANTES DE ARREGLAR (informe_P7_29, seccion 0): las rachas bloqueadas de P7-24 no chocan contra muros del mapa (en las 2.233 rachas de
3 o mas pasos, la casilla contra la que choca es suelo en el `static_map`): el 58 % de los tics son `move_*` del cuerpo contra la hermana visible (los
pasos largos `mover` no esquivan cuerpos: decisor_zs.py:786-788, `_simula_camino`), y el 42 % son vidas cuya DECISION TARDA MAS QUE EL TIC: el recuerdo
por parecido (`nace_P7_23.vivida` -> `recuerdo_P7_23.creencia_parecido`) se calculaba 216 veces por tic (414.759 llamadas en 1.920 tics; 58,7 de 61,6 s
del decisor), y con 20-30 recuerdos la decision pasa de los 41,7 ms del tic (24 tics/s): las observaciones se encolan (policy_cortex.py:881-960, una
decision por observacion, en orden), las acciones llegan al mundo con retraso creciente y el mundo responde `blocked` a pasos pedidos desde una casilla en
la que la criatura ya no esta. Por eso solo le pasa a APRENDE (TECHO 1,3 ms; BORRADO 4 ms; APRENDE dias 16-20: 31 ms de mediana, el 32 % de los tics por
encima del tic).

LA CACHE (arreglo 0, de ingenieria, sin cambiar ninguna decision): `vivida(mundo, obj, pos, tick)` se recuerda dentro del tic por (objeto, contexto
dentro/golpeada, tic, dia, numero de recuerdos, foto): mismos argumentos, mismo resultado. Comprobado bit a bit en la replica (banco_P7_29 --cache).
[P7-30, segunda cache, misma idea] `D._promesa(obs, mundo, mem, tick, item_id)` se recuerda dentro del tic por (tic, observacion real, objeto): el cuerpo la pide
una vez por cada objeto recordado del mapa (`_mejor_objeto`, decisor_zs.py:684-706) y para el botiquin y el camuflaje cada peticion vale dos `filas` enteras
(decisor_zs.py:656-658, 674-677), que con las piezas del siete pesan el doble cuando la hermana y consumibles estan a la vista (`regalo_nace`): con 17 objetos
recordados, 40 `filas` por tic y la decision a 18 ms de mediana en la plataforma (s1 d2 asiento 11 del campo de P7-30, guarda saltada). Mismos argumentos,
mismo resultado; la observacion y la memoria se retienen en la cache para que sus ids no se reutilicen dentro del tic (pedir, P7-17, pregunta a `decide` sobre una copia de la memoria con la misma observacion).

ARREGLO 1 (mesa): la curiosidad solo mueve por curiosidad. `ir_curioso` pierde el `recoger` (la imaginacion ya no pone la cosa en el zurron al llegar,
decisor_zs.py:808-816) y se valora SOLO con el alivio de la fila: al llegar a la casilla, el alivio de la clase pasa a ALIVIO_ZURRON (0,5, el mismo
numero que tenerla), nada mas. Ir a por una cosa conocida porque se quiere es de `ir_objeto` / `coger` del cuerpo, con las ganas aprendidas (P7-23).
ARREGLO 2 (apuntar el muro tras tres choques): QUITADO por la mesa en P7-29b (no hay muros que aprender; en F1 de P7-29 aprendia 13 "muros" fantasma en
los diarios de A4 y cambiaba 1.095 decisiones). Queda en el historial de git (commit f9a2e75).
ARREGLO 3 (mesa): el corte no entra en la media del efecto. Se guarda igual (contexto, foto, acciones) marcado `acto` y con la causa del corte (dano
recibido en la ventana y sus fuentes, y la ultima eleccion), para mas adelante. Las medias (`creencia`, `creencia_parecido`) solo cuentan usos
completados (firmes y "al menos"); la ignorancia de la clase sigue contando el corte como experiencia vivida (el acto se vivio; declarado).
PIEZA NUEVA (Manel): LA CURIOSIDAD DEL CUANTO. Por cosa conocida (con algun uso completado), ignorancia del cuanto = PESO_NEUTRO / (PESO_NEUTRO + suma
de pesos de los recuerdos FIRMES: completados y sin "al menos"). Fila R-CURIOSIDAD-CUANTO = ACOPIO_M x calma x media por cosa conocida de (ignorancia
del cuanto x alivio), misma escala y misma calma que R-CURIOSIDAD, en el reparto con REPARTO_CUR. En la imaginacion solo la alivia USAR la cosa (foto
de `usar_botiquin` / `usar_racion`) cuando lo que le falta (hp_max - hp real) es mayor que lo mas alto que ya sabe que da (maximo del efecto en el
cuerpo entre los usos completados); el alivio es ALIVIO_ZURRON (mismo numero). Dominio: el cuerpo (el unico con "lo que le falta" medible por el
cuerpo; recursos y vinculo no tienen carencia definida: declarado). Con recuerdos firmes se apaga como cualquier ignorancia.
MANDOS DE BANCO: E["arreglos"] = {cache, curiosidad, corte, cuanto}; en el campo, todos encendidos.
"""
from __future__ import annotations
import collections, math, os
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A
import descubre_P7 as X
import nace_P7_23 as N
from recuerdo_P7_23 import CuadernoP23, parecido
from cuaderno_P7 import DOMINIOS, OLVIDO, PESO_NEUTRO

ON = X._on("GEMV_P7_29")
FILA_CUANTO = "R-CURIOSIDAD-CUANTO"
E = {"arreglos": {"cache": True, "curiosidad": True, "corte": True, "cuanto": True}, "registra": None, "cache": {}, "cache_tick": None,
     "cands": [], "idx": 0, "curioso": None, "desajustes": 0, "ultimo_cuanto_log": -10 ** 9}


# ── el cuaderno con el corte aparte y la ignorancia del cuanto ──
class CuadernoP29(CuadernoP23):
    def _entra(self, r):
        """Un recuerdo entra en la media del efecto si no es un corte (arreglo 3)."""
        return not (E["arreglos"]["corte"] and r.get("corte"))

    def creencia(self, objeto, situacion, dia=None, con_neutro=True):
        rec = [r for r in (((self.objetos.get(objeto) or {}).get("situaciones") or {}).get(situacion) or []) if self._entra(r)]
        if not rec: return None
        d_act = self.dia_actual() if dia is None else dia; out = {}
        for dom in DOMINIOS:
            num = 0.0; den = PESO_NEUTRO if con_neutro else 0.0; techo = []
            for r in rec:
                w = float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"])))
                if dom == "cuerpo" and r.get("al_menos"): techo.append((w, float(r["efecto"][dom]))); continue
                num += w * float(r["efecto"][dom]); den += w
            if techo:
                base = (num / den) if den > 0 else 0.0
                for w, e in techo:
                    if e > base: num += w * e; den += w
            if den <= 0: return None
            out[dom] = round(num / den, 4)
        return out

    def creencia_parecido(self, objeto, contexto, foto, dia=None):
        rec = [r for r in self.recuerdos_de(objeto) if self._entra(r)]
        if not rec: return None, 0.0
        d_act = self.dia_actual() if dia is None else dia
        pesos = [(float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"]))) * parecido(contexto, foto, r), r) for r in rec]
        out = {}
        for dom in DOMINIOS:
            num = 0.0; den = 0.0; techo = []
            for w, r in pesos:
                if dom == "cuerpo" and r.get("al_menos"): techo.append((w, float(r["efecto"][dom]))); continue
                num += w * float(r["efecto"][dom]); den += w
            if techo:
                base = num / (den + PESO_NEUTRO)
                for w, e in techo:
                    if e > base: num += w * e; den += w
            out[dom] = (num / den) if den > 0 else 0.0
        return out, sum(w for w, _ in pesos)

    def pesos_firmes(self, objeto, dia=None):
        d_act = self.dia_actual() if dia is None else dia
        return sum(float(r["intensidad"]) * (OLVIDO ** max(0, d_act - int(r["dia"]))) for r in self.recuerdos_de(objeto) if not r.get("corte") and not r.get("al_menos"))

    def ignorancia_cuanto(self, objeto, dia=None):
        return PESO_NEUTRO / (PESO_NEUTRO + self.pesos_firmes(objeto, dia))

    def sabido_max(self, objeto, dom="cuerpo"):
        """Lo mas alto que ya sabe que da (usos completados, firmes o 'al menos'); None si no tiene ningun uso completado."""
        vals = [float(r["efecto"][dom]) for r in self.recuerdos_de(objeto) if not r.get("corte")]
        return max(vals) if vals else None

    def conocido(self, objeto): return self.sabido_max(objeto) is not None

    def apunta_P23(self, objeto, contexto, foto, acciones, efecto, importancia, tick=None, al_menos=False, corte=False):
        r = super().apunta_P23(objeto, contexto, foto, acciones, efecto, importancia, tick=tick, al_menos=al_menos, corte=corte)
        if corte:
            v = N.E.get("ventana") or {}
            r["acto"] = True; r["causa_corte"] = {"dano": round(float(v.get("total") or 0.0), 3), "fuentes": list(v.get("fuentes") or [])[:6], "ultima_eleccion": (list(N.E["acciones"])[-1] if N.E["acciones"] else None), "tics": (N.E.get("tick") or 0) - int(v.get("t0") or 0)}
        return r

    def creencias(self):
        base = super().creencias()
        for o in list(base):
            base[o]["ignorancia_cuanto"] = round(self.ignorancia_cuanto(o), 4); base[o]["sabido_max"] = self.sabido_max(o); base[o]["pesos_firmes"] = round(self.pesos_firmes(o), 4)
            base[o]["cortes"] = sum(1 for r in self.recuerdos_de(o) if r.get("corte"))
        return base


def cuaderno():
    c = X.ESTADO["cuaderno"]
    if c is not None and not isinstance(c, CuadernoP29): c.__class__ = CuadernoP29
    return c


# ── la cache del recuerdo por parecido (arreglo 0) ──
_viv0 = N.vivida
def vivida(mundo, obj, pos, tick):
    if not E["arreglos"]["cache"]: return _viv0(mundo, obj, pos, tick)
    c = cuaderno()
    if c is None or not X.CUADERNO_ON: return None, 1.0
    ctx = N.contexto_ahora(mundo, pos, tick); n_rec = sum(len(s) for s in ((c.objetos.get(obj) or {}).get("situaciones") or {}).values())
    key = (obj, ctx["dentro"], ctx["golpeado_48"], tick, c.dia_actual(), n_rec, id(N.E["foto"]))
    if E["cache_tick"] != tick: E["cache"] = {}; E["cache_tick"] = tick
    v = E["cache"].get(key)
    if v is None: v = _viv0(mundo, obj, pos, tick); E["cache"][key] = v
    return v


# ── la curiosidad: alivio al llegar (arreglo 1) y la fila del cuanto ──
def alivio_clase(obs, mundo, obj):
    you = obs.get("you") or {}; cu = you.get("_P29_curioso")
    if cu and cu.get("clase") == obj and cu.get("llega"): return X.ALIVIO_ZURRON
    return N.alivio_clase(obs, mundo, obj)
def curiosidad_M(obs, mundo, F):
    calma = N.cautela_de(obs, mundo, N.E.get("tick")) if N.E.get("cautela") else X.calma_de(F); c = cuaderno(); partes = []
    for o in N.consumibles(mundo):
        ign = 1.0 if (c is None or not X.CUADERNO_ON) else float(c.ignorancia(o)); partes.append(ign * (alivio_clase(obs, mundo, o) if E["arreglos"]["curiosidad"] else N.alivio_clase(obs, mundo, o)))
    m = sum(partes) / len(partes)
    return X.ACOPIO_M0 * float(N.E.get("escala_curiosidad") or 1.0) * calma * m, calma, m, 1.0
def alivio_cuanto(obs, mundo, mem, obj, c):
    you = obs.get("you") or {}
    if you.get("_P29_usa") != obj: return 1.0
    hp_max = float(getattr(mem, "hp_max", None) or 100.0); hp_real = float(you.get("_hp_real") if you.get("_hp_real") is not None else (you.get("hp") or 0.0))
    sab = c.sabido_max(obj)
    return X.ALIVIO_ZURRON if (sab is not None and (hp_max - hp_real) > sab) else 1.0
def cuanto_M(obs, mundo, mem, F):
    c = cuaderno()
    if c is None or not X.CUADERNO_ON: return 0.0, {}
    calma = X.calma_de(F); partes = {}
    for o in N.consumibles(mundo):
        if not c.conocido(o): continue
        partes[o] = {"ignorancia_cuanto": round(c.ignorancia_cuanto(o), 4), "sabido_max": c.sabido_max(o), "alivio": alivio_cuanto(obs, mundo, mem, o, c)}
    if not partes: return 0.0, {}
    m = sum(p["ignorancia_cuanto"] * p["alivio"] for p in partes.values()) / len(partes)
    return X.ACOPIO_M0 * calma * m, {"calma": round(calma, 4), "clases": partes}


# ── los enganches ──
def aplica(clase, registra=None):
    E["registra"] = registra
    if not (ON and X.ON): return {"P7_29": False}
    N.cuaderno = cuaderno; N.vivida = vivida
    hecho = {"P7_29": True, "cache": E["arreglos"]["cache"]}
    _od = clase.decidir
    if X.SABE or not N.NACE: return hecho | {"solo": "cache (TECHO o sin nace)"}
    _oc = D.candidatos; _oo = D._obs_prevista; _of = A.filas; _opr = D._promesa
    def _promesa_cache(obs, mundo, mem, tick, item_id):
        if not E["arreglos"]["cache"] or not E.get("cache_promesa", True): return _opr(obs, mundo, mem, tick, item_id)
        if E.get("promesa_tick") != tick: E["promesa_cache"] = {}; E["promesa_tick"] = tick
        k = (id(obs), id(mem), item_id); hit = E["promesa_cache"].get(k)
        if hit is not None and hit[0] is obs and hit[1] is mem: return hit[2]
        v = _opr(obs, mundo, mem, tick, item_id); E["promesa_cache"][k] = (obs, mem, v); return v
    D._promesa = _promesa_cache
    if E["arreglos"]["cuanto"] and X.NOVEDAD_ON: A.REPARTO[FILA_CUANTO] = X.REPARTO_CUR
    X.curiosidad_M = curiosidad_M; N.curiosidad_M = curiosidad_M
    def _cands(obs, mundo, mem, tick, bloqueos=None):
        out = _oc(obs, mundo, mem, tick, bloqueos); out2 = []; E["curioso"] = None
        for n, r in out:
            if n == "ir_curioso" and E["arreglos"]["curiosidad"]:
                rec = r.get("recoger") or (None,); clase = X.kit(mundo) if rec[0] == X.kit(mundo) else N.racion(mundo)
                r = {k: v for k, v in r.items() if k != "recoger"}; r["curioso"] = clase; E["curioso"] = (clase, tuple(r.get("destino") or ()))
            out2.append((n, r))
        E["cands"] = [n for n, _ in out2]; E["idx"] = 0
        return out2
    def _obs_prevista(obs, mundo, mem, tick_eval, pos, hp, pack, hand, ver_pareja, golpe=None, suelta=None, body=False):
        ob2 = _oo(obs, mundo, mem, tick_eval, pos, hp, pack, hand, ver_pareja, golpe, suelta, body)
        i = E["idx"]; E["idx"] = i + 1; nombres = E["cands"]
        if i < len(nombres):
            n = nombres[i]
            if n == "ir_curioso" and E["curioso"]: ob2["you"]["_P29_curioso"] = {"clase": E["curioso"][0], "llega": tuple(pos) == E["curioso"][1]}
            elif n == "usar_botiquin": ob2["you"]["_P29_usa"] = X.kit(mundo)
            elif n == "usar_racion": ob2["you"]["_P29_usa"] = N.racion(mundo)
        return ob2
    def _filas(obs, mundo, mem, tick):
        F = _of(obs, mundo, mem, tick)
        if E["arreglos"]["cuanto"] and X.NOVEDAD_ON:
            M, det = cuanto_M(obs, mundo, mem, F); F[FILA_CUANTO] = M; F["_cuanto"] = det; E["ultimo_cuanto"] = det
        return F
    def decidir(self, obs, _d=_od):
        # [P7-34, paso 0] la lista de candidatos que el decisor fotografia es la que devuelve el ULTIMO envoltorio de `D.candidatos`, y las piezas congeladas
        # del seis (`arreglos_P6_8b._cands`, aplicada por `policy_pareja11.run` despues de las del siete) esconden `coger` con la mochila llena (`llena8`)
        # por fuera de `_cands`: los nombres se tomaban antes y las fotos se corrian un indice ("N fotos para N+1 candidatos"). Aqui se envuelve lo que haya
        # en `D.candidatos` en el momento de decidir y los nombres se toman de la lista final; se restaura al salir (el mismo patron que policy_cortex.decidir).
        _oc_ahora = D.candidatos
        def _ultimo(o, mu, me, tk, bl=None):
            out = _oc_ahora(o, mu, me, tk, bl); E["cands"] = [n for n, _ in out]; E["idx"] = 0; return out
        D.candidatos = _ultimo
        try: accion, radio = _d(self, obs)
        finally: D.candidatos = _oc_ahora
        if radio is not None and E["cands"] and E["idx"] != len(E["cands"]):
            E["desajustes"] += 1
            if E["registra"] and E["desajustes"] <= 3: E["registra"]({"k": "P7_error", "tick": self.tick, "error": f"P7-29: {E['idx']} fotos para {len(E['cands'])} candidatos"})
        if radio is not None and getattr(self, "phase", None) == "live" and E["arreglos"]["cuanto"] and self.tick - E["ultimo_cuanto_log"] >= 250 and E["registra"]:
            E["ultimo_cuanto_log"] = self.tick; c = cuaderno(); fl = ((radio.get("ahora") or {}).get("filas") or {})
            E["registra"]({"k": "P7_cuanto", "tick": self.tick, "M": (fl.get(FILA_CUANTO) or {}).get("M", 0.0), "M_curiosidad": (fl.get("R-CURIOSIDAD") or {}).get("M", 0.0),
                           "clases": ({o: {"ignorancia": round(c.ignorancia(o), 4), "ignorancia_cuanto": round(c.ignorancia_cuanto(o), 4), "sabido_max": c.sabido_max(o)} for o in N.consumibles(self.mundo)} if c is not None else None)})
        return accion, radio
    D.candidatos, D._obs_prevista, A.filas, clase.decidir = _cands, _obs_prevista, _filas, decidir
    return hecho | {"curiosidad": E["arreglos"]["curiosidad"], "corte": E["arreglos"]["corte"], "cuanto": E["arreglos"]["cuanto"], "fila": FILA_CUANTO}

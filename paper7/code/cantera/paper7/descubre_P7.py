"""[P7-5] EL CUERPO QUE DESCUBRE: las cuatro piezas del plan P7-4 (corregido), enganchadas DESDE FUERA sobre el cuerpo congelado del seis,
sin tocar un byte de `decisor_zs.py`, `appraisal_zs_v42_exp.py` ni `policy_pareja.py`. Archivo experimental del siete.

  A. CUADERNO (`cuaderno_P7.py`): se lee al arrancar (`arranca`) y se escribe al acabar (`termina`); las experiencias se cierran en el
     envoltorio de `decidir` (ventana del uso del botiquin: desde que aparece el canal hasta que desaparece, mas un tic).
     Lo esperado sin la cosa (correccion 1 de la mesa): se resta SOLO el dano de causas que el cuerpo conoce: el anillo cuando esta fuera
     del circulo (segun `mundo.anillo_en`, el calendario que ya usa) y los golpes de rivales a la vista y en alcance (su arma, por el
     catalogo; mano vacia = 1). El resto del dano se queda en el efecto.
     La importancia por dominio lleva signo (correccion 2): malestar del eje al cerrar menos al abrir (> 0 dolor, < 0 alivio); ejes F ->
     cuerpo, R -> recursos, S -> vinculo, leidos de la radiografia del propio cuerpo (`appraise`, columnas F, R, S de cada fila).
  B. IMAGINACION: envoltorio de `D.candidatos`: en `usar_botiquin`, `receta["heal"]` (decisor_zs.py:493) pasa a ser la creencia del
     cuerpo en la situacion de ahora; "no se" -> 0 (la foto no le pone efecto, decisor_zs.py:824).
  C. GANAS: `A.ACOPIO_M` y `A.ACOPIO_POR_DOS` (appraisal:111 y :221, la fila R-ACOPIO :936-973) y el termino del botiquin en W (`riqueza_W`, :749) se escalan por
     k = creencia_max / cura del catalogo (un cuerpo cuya creencia fuera la cura real tendria el peso de hoy); `A.W_TARGET` (:126) pasa a
     2 + k (decision del plan, abierta a la mesa). "No se" -> k = 0.
  D. CURIOSIDAD [P7-6, cambio 1]: la curiosidad es una carencia de conocimiento, no un iman de lugar. Fila R-CURIOSIDAD (negativa, como
     las demas carencias; reparto como R-ACOPIO), anadida en el envoltorio de `A.filas` y en `A.REPARTO` desde fuera:
       M = ACOPIO_M x calma x ignorancia(clase) x alivio, con ignorancia leida del cuaderno (`cuaderno_P7.ignorancia`), calma = 1 - max(F-4-ALCANCE,
       S-7-AGRESOR, F-HERMANO-AMENAZA, F-HERMANO-GOLPE, F-ANTICIPACION), y alivio = 1 sin la cosa (estar al lado no alivia nada), 0,5 con la
       cosa en el zurron, 0 en la foto que la usa. La promesa de ir a por ella (`D._promesa`) = M_ahora x 0,5 (lo que alivia tenerla).
     Desaparecen la cuenta de usos, la forma de la novedad de P7-5 y la pendiente SUELO_MAX cambiada tras el humo.
     [P7-7, decision 2] LA CURIOSIDAD ABRE CAMINO: candidato `ir_curioso` (pieza F en `_cands`): el mismo candidato de ir a por la cosa que
     generan las ganas de un objeto (`ir_objeto`), hacia el botiquin mas cercano visto o recordado, con la imaginacion de llegar = tenerlo en
     el zurron (alivio 0,5). Sin numeros nuevos.
  A' [P7-7, decision 1] EL RECUERDO CON TECHO: si la vida toca su maximo (`mem.hp_max`) dentro de la ventana, el recuerdo se apunta con
     `al_menos` (ver `cuaderno_P7.creencia`); la huella lo lleva (`al_menos`, `hp_max`).
  I. EN UN EMPATE, HACER SITIO NO GANA [P7-10, arreglo de la mesa]: `desempate_sin_sitio` sobre `D.select_tiebreak`. Interruptor
     GEMV_P7_SITIO_EMPATE (1 por defecto). [P7-14b, decision de la mesa] La regla se extiende a todo gesto de desprenderse: en un empate
     no se da ni se suelta nada (`soltar_*` ademas de `hacer_sitio_*`).
  H. LA ESPERANZA [P7-9, decision de diseno de Manel]: al imaginar usar el botiquin (`heal_imaginado`) y al imaginar tenerlo (`k_ganas`), el
     efecto = (1 - ignorancia) x creencia + ignorancia x esperanza, con esperanza = lo que hacen los consumibles que el cuerpo conoce (la
     racion, heal 15 del catalogo). Nada mas: ningun peso por la necesidad. El regalo (G) sigue mirando solo lo aprendido (`k_creencia`).
     Interruptor GEMV_P7_ESPERANZA (1 por defecto; 0 solo en el banco "antes").
  G. EL REGALO MIRA LO APRENDIDO [P7-8, arreglo de la mesa]: ver `regalo_aprendido`: para el botiquin, la medicina junto a la cama del hermano
     vale con la creencia de quien regala (k); "no se" -> nada que regalar por su valor. Las raciones, como hoy.
  E. HACER SITIO [P7-6, cambio 2]: candidato compuesto "soltar un consumible para coger otro" (`hacer_sitio_<suelta>_por_<coge>`), creado en el
     envoltorio de `D.candidatos` cuando hay un objeto en mi casilla que `coger` no puede tomar (zurron lleno, sin pila donde apilarlo) y llevo un
     consumible de otra clase. Se evalua como cualquier opcion: es un `soltar` (tipo del decisor: pack sin la ranura, el objeto al suelo, accion
     `drop`) cuya receta lleva en `item` el marcador "<suelta>|<coge>"; el envoltorio de `D._obs_prevista` lo reconoce y pone ademas en la foto
     el objeto cogido en el zurron (lo que se pierde contra lo que se gana, en la misma imaginacion). Tras elegirlo, la cesion que `decide`
     apunta en `mem.cedidos` (decisor_zs.py:902-903) se borra en el envoltorio de `decidir`, para que `coger` pueda tomar el objeto al tic
     siguiente. Igual en los cuatro brazos; apagado en F1 (GEMV_P7_SITIO=0).
INTERRUPTORES (entorno): GEMV_P7=1 enciende los enganches; GEMV_P7_SABE=1 = TECHO (el cuerpo de hoy: todo pasa tal cual);
  GEMV_P7_CUADERNO=1 lee/escribe el cuaderno; GEMV_P7_BORRADO=1 no lee (empieza vacio cada partida); GEMV_P7_NOVEDAD=1 la fila de
  curiosidad; GEMV_P7_SITIO=1 hacer sitio.
  ESPERANZA (hasta P7-12 se llamo SUELO: esperanza sin memoria, ver informe_P7_11) = P7=1 SITIO=1 · BORRADO = P7=1 CUADERNO=1 BORRADO=1 NOVEDAD=1 SITIO=1 · APRENDE = P7=1 CUADERNO=1 NOVEDAD=1 SITIO=1 · TECHO = P7=1 SABE=1 SITIO=1.
"""
from __future__ import annotations
import math, os
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A
from cuaderno_P7 import Cuaderno, DOMINIOS

def _on(k, por_defecto="0"):
    return (os.environ.get(k, por_defecto) or por_defecto) not in ("0", "", "no")
ON = _on("GEMV_P7"); SABE = _on("GEMV_P7_SABE"); CUADERNO_ON = _on("GEMV_P7_CUADERNO"); BORRADO = _on("GEMV_P7_BORRADO"); NOVEDAD_ON = _on("GEMV_P7_NOVEDAD"); SITIO_ON = _on("GEMV_P7_SITIO")
ESPERANZA_ON = _on("GEMV_P7_ESPERANZA", "1")      # [P7-9] la esperanza (encendida por defecto; 0 solo para el banco "antes")
PIDE2 = _on("GEMV_P7_PIDE2")                      # [P7-16] pedir corregido (0 por defecto: los campos jugados se replican como se jugaron)
SITIO_EMPATE = _on("GEMV_P7_SITIO_EMPATE", "1")   # [P7-10] en un empate, hacer sitio no gana (encendido por defecto; 0 solo para el banco "antes")
ACOPIO_M0 = float(A.ACOPIO_M); ACOPIO_POR_DOS0 = float(A.ACOPIO_POR_DOS); W_TARGET0 = float(A.W_TARGET); REPARTO_CUR = (0.1, 0.8, 0.1); ALIVIO_ZURRON = 0.5
CALMA_FILAS = ("F-4-ALCANCE", "S-7-AGRESOR", "F-HERMANO-AMENAZA", "F-HERMANO-GOLPE", "F-ANTICIPACION")
ESTADO = {"cuaderno": None, "ruta": None, "ventana": None, "registra": None, "calma_cache": (None, None), "huellas": [], "ultima_heal": None, "ultima_sit": None, "regalo_en_ventana": None}

def entorno():
    return {"crudo": {k: os.environ.get(k) for k in ("GEMV_P7", "GEMV_P7_SABE", "GEMV_P7_CUADERNO", "GEMV_P7_BORRADO", "GEMV_P7_NOVEDAD", "GEMV_P7_SITIO", "CUADERNO_DIR")},
            "efectivo": {"ON": ON, "SABE": SABE, "CUADERNO": CUADERNO_ON, "BORRADO": BORRADO, "NOVEDAD": NOVEDAD_ON, "SITIO": SITIO_ON, "ESPERANZA": ESPERANZA_ON, "SITIO_EMPATE": SITIO_EMPATE, "ACOPIO_M0": ACOPIO_M0, "W_TARGET0": W_TARGET0, "REPARTO_CUR": REPARTO_CUR, "ALIVIO_ZURRON": ALIVIO_ZURRON, "CALMA_FILAS": CALMA_FILAS},
            "brazo": ("TECHO" if (ON and SABE) else "APRENDE" if (ON and CUADERNO_ON and not BORRADO and NOVEDAD_ON) else "BORRADO" if (ON and CUADERNO_ON and BORRADO) else "ESPERANZA" if ON else "apagado")}   # [P7-13] el brazo que fue SUELO se llama ESPERANZA (esperanza sin memoria)

# ── lo que el cuerpo lee del mundo ──
def kit(mundo): return getattr(mundo, "id_botiquin", None) or "first_aid"
def cura_catalogo(mundo):
    it = mundo.items.get(kit(mundo)) if getattr(mundo, "items", None) else None
    return float(getattr(it, "heal", 0) or 50.0) if it is not None else 50.0
def situacion(mundo, pos, tick):
    centro, radio, _ = mundo.anillo_en(tick)
    return "dentro" if math.dist(pos, centro) <= radio else "fuera"
def kits_en(you, mundo):
    return sum(int(s.get("n") or 1) for s in (you.get("pack") or []) if s and s.get("id") == kit(mundo))
def unidades(you):
    c = 0; h = you.get("hand") or {}
    if h.get("id") not in (None, "none"): c += int(h.get("n") or 1)
    for s in you.get("pack") or []:
        if s: c += int(s.get("n") or 1)
    if you.get("body"): c += 1
    return c
def dist_hermano(obs, mundo, mem):
    for a in ((obs.get("visible") or {}).get("agents") or []):
        if a.get("slot") == mundo.teammate_slot and a.get("pos"): return math.dist(obs["you"]["pos"], a["pos"]), "vista"
    q = getattr(mem, "pareja_pos", None)
    return (math.dist(obs["you"]["pos"], q), "recordada") if q else (None, None)
def malestar_ejes(radio):
    fl = ((radio or {}).get("ahora") or {}).get("filas") or {}
    out = {}
    for eje, dom in (("F", "cuerpo"), ("R", "recursos"), ("S", "vinculo")):
        out[dom] = sum((v.get(eje) or 0.0) * (1 if v.get("signo") == "-" else -1) for v in fl.values() if isinstance(v, dict) and v.get(eje) is not None)
    return out

# ── las creencias que entran en el cuerpo ──
def esperanza_cuerpo(mundo):
    """[P7-9] Lo que suelen hacer en el cuerpo las cosas de la misma clase que el cuerpo conoce: la media de `heal` de los consumibles del
    catalogo que no son el botiquin (hoy, la racion: 15). En recursos, -1 (la unidad que se gasta, que la foto ya pone); en vinculo, 0."""
    its = [it for i_, it in (getattr(mundo, "items", None) or {}).items() if i_ != kit(mundo) and getattr(it, "kind", None) == "ikConsumable" and float(getattr(it, "heal", 0) or 0) > 0]
    return (sum(float(it.heal) for it in its) / len(its)) if its else 0.0
def w_target(k, mundo):
    """[P7-23] El objetivo de riqueza con lo que se sabe: 2 + k (arma y racion enteras, botiquin por lo que se sabe de el; la decision de P7-5).
    `nace_P7_23` lo sustituye desde fuera cuando la racion tampoco se conoce al nacer."""
    return 2.0 + k
def k_creencia(mundo):
    """Las ganas por lo aprendido, sin esperanza: creencia maxima del cuerpo / cura del catalogo; "no se" -> 0. (Lo que mira el regalo, P7-8.)"""
    if SABE: return 1.0
    c = ESTADO["cuaderno"]; v = c.creencia_max_cuerpo(kit(mundo)) if (c is not None and CUADERNO_ON) else None
    return 0.0 if v is None else max(0.0, float(v) / cura_catalogo(mundo))
def mezcla(mundo, creencia):
    """[P7-9] LA ESPERANZA (forma de la mesa): efecto imaginado = (1 - ignorancia) x creencia + ignorancia x esperanza. Nunca probado: todo
    esperanza; muy conocido: todo creencia. Sin esperanza (banco "antes"): la creencia, y "no se" = 0."""
    cre = 0.0 if creencia is None else max(0.0, float(creencia))
    if not ESPERANZA_ON: return cre
    ign = ignorancia_de(mundo)
    return (1.0 - ign) * cre + ign * esperanza_cuerpo(mundo)
def k_ganas(mundo):
    """Las ganas del botiquin (R-ACOPIO, W, W_TARGET): la misma mezcla que la imaginacion de usarlo, sobre la creencia maxima, / cura."""
    if SABE: return 1.0
    # [P7-14, arreglo de la mesa] la creencia que entra en la mezcla es la de LO VIVIDO, sin el neutro: la ignorancia ya descuenta en la mezcla
    # (hasta P7-13 descontaba dos veces: en la creencia, por el neutro, y en la mezcla). Con todo lo vivido igual a la cura e ignorancia 0, k = 1.
    c = ESTADO["cuaderno"]; v = c.creencia_vivida_max_cuerpo(kit(mundo)) if (c is not None and CUADERNO_ON) else None
    return max(0.0, mezcla(mundo, v) / cura_catalogo(mundo))
def heal_imaginado(mundo, pos, tick):
    """La cura imaginada al usar el botiquin: la mezcla sobre la creencia de la situacion de ahora; si esa situacion no tiene creencia pero
    otra si, se usa la maxima (declarado); si ninguna, la ignorancia es 1 y todo es esperanza."""
    if SABE: return None
    c = ESTADO["cuaderno"]; v = None
    if c is not None and CUADERNO_ON:
        v = c.creencia_vivida_cuerpo(kit(mundo), situacion(mundo, pos, tick))      # [P7-14] sin el neutro, como las ganas
        if v is None: v = c.creencia_vivida_max_cuerpo(kit(mundo))
    return mezcla(mundo, v)
def calma_de(F):
    return max(0.0, 1.0 - min(1.0, max(float(F.get(n) or 0.0) for n in CALMA_FILAS)))
def ignorancia_de(mundo):
    c = ESTADO["cuaderno"]
    return 1.0 if c is None else float(c.ignorancia(kit(mundo)))
def alivio_de(obs, mundo):
    """1 sin la cosa (estar al lado no alivia), 0,5 con la cosa en el zurron, 0 en la foto que la usa (`_cura_en_curso`, la marca que el
    decisor pone SOLO en la foto de usar el botiquin, decisor_zs.py:830,877-878). [P7-8, visto en el banco del regalo: hasta P7-7 tambien
    valia 0 cuando la foto llevaba menos botiquines que los reales (`_bot_real`), y esa es tambien la foto de SOLTARLO: regalar o soltar el
    botiquin parecia aliviar la curiosidad como usarlo. Era parte de lo que hacia ganar al regalo del botiquin desconocido y de la oscilacion
    de hacer sitio racion <-> botiquin del dia 3 de P7-7.]"""
    you = obs.get("you") or {}; n_ = kits_en(you, mundo)
    if you.get("_cura_en_curso"): return 0.0
    return ALIVIO_ZURRON if n_ >= 1 else 1.0
def curiosidad_M(obs, mundo, F):
    calma = calma_de(F); ign = ignorancia_de(mundo); al = alivio_de(obs, mundo)
    return ACOPIO_M0 * calma * ign * al, calma, ign, al

# ── G [P7-8, arreglo de la mesa] · EL REGALO MIRA LO APRENDIDO ──
FILAS_REGALO = ("S-DANO-PAREJA", "S-HERIDO", "R-HERMANO-FALTA", "S-PROVISION")   # las conocidas; se pesa toda fila que cambie
def regalo_aprendido(obs, mundo, mem, tick, F, filas0):
    """Para el botiquin, lo que vale para el hermano una cura en el suelo junto a el se valora con la creencia de quien regala, como las
    ganas: k = creencia_max / cura del catalogo; "no se" -> 0, nada que regalar por su valor. Las filas que leen ese hecho en el cuerpo
    congelado: la medicina junto a la cama (S-DANO-PAREJA, appraisal:1143-1169), S-HERIDO por `_herido_ayuda` (:1237-1278), R-HERMANO-FALTA
    (:1632-1641) y S-PROVISION, la hermana sin venda (:1312-1362; en el banco del regalo era ESTA la que pagaba el regalo: 0,30 -> 0,045).
    Se hace desde fuera y con el propio cuerpo: se vuelven a calcular las filas con los botiquines del suelo quitados de la vista (F_sin) y
    TODA fila que cambie por ello queda F_sin + (F - F_sin) x k (lo que el botiquin en el suelo vale, pesado por lo que se sabe de el).
    Para los otros objetos (raciones), como hoy: siguen en la vista. Con SABE (k = 1) no se toca nada. Se dispara solo si hay un botiquin a
    la vista en el suelo y el hermano a la vista."""
    vis = obs.get("visible") or {}; kid = kit(mundo)
    items = vis.get("items") or []
    if not any(it.get("id") == kid for it in items) or not any(a.get("slot") == mundo.teammate_slot for a in (vis.get("agents") or [])): return F
    k = k_creencia(mundo)                       # el regalo mira LO APRENDIDO (P7-8), sin esperanza: "no se" -> nada que regalar por su valor
    if k >= 1.0: return F
    ob2 = dict(obs); ob2["visible"] = dict(vis, items=[it for it in items if it.get("id") != kid])
    F_sin = filas0(ob2, mundo, mem, tick)
    cambio = {}
    for fila in set(F) | set(F_sin):
        if fila.startswith("_") or not isinstance(F.get(fila, 0.0), (int, float)) or not isinstance(F_sin.get(fila, 0.0), (int, float)): continue
        a, b = float(F.get(fila) or 0.0), float(F_sin.get(fila) or 0.0)
        if a != b: F[fila] = b + (a - b) * k; cambio[fila] = (round(a, 5), round(b, 5), round(F[fila], 5))
    if cambio: F["_regalo_aprendido"] = {"k": round(k, 4), "filas": cambio}
    return F

# ── I [P7-10, arreglo de la mesa] · EN UN EMPATE, HACER SITIO NO GANA ──
DESPRENDERSE = ("hacer_sitio_", "soltar_")      # [P7-14b] los gestos de desprenderse de algo
def desempate_sin_sitio(sel0):
    """Envoltorio de `D.select_tiebreak` (planificador_v1.select_tiebreak, llamado en decisor_zs.py:895): si el minimo de la d terminal lo
    comparten (empate exacto, _TOL) un candidato de hacer sitio y otro que no lo es, o si el paisaje es degenerado (spread <= eps), los de
    hacer sitio salen del desempate: se queda lo que se tiene (cambiar cuesta un gesto). Si hacer sitio gana solo, gana. [Medido en P7-9,
    dia 2, asiento 10: la vuelta de cada oscilacion racion <-> botiquin era un empate exacto con noop (dif 0,0), que noop no puede ganar.]"""
    from planificador.planificador_v1 import TIEBREAK_EPS, _TOL
    def sel(action_names, preds, terminal, meta, *a, **kw):
        # [P7-14b, decision de la mesa] EN UN EMPATE NO SE DA NI SE SUELTA NADA: la regla de hacer sitio vale para todo gesto de desprenderse
        # (`hacer_sitio_*` y `soltar_*`: regalar el botiquin, soltar raciones). Mismo criterio de empate, ningun numero nuevo. [Visto en el freno
        # de P7-14, dia 1, asiento 10, tic 4.979: `soltar_first_aid` y `noop` con d 3,82825 las dos; ganaba soltar porque `noop` no puede ganar.]
        sitio = [x for x in action_names if str(x).startswith(DESPRENDERSE)]
        if sitio and len(sitio) < len(action_names):
            vals = [terminal[x] for x in action_names]; mn = min(vals); eps = kw.get("eps", TIEBREAK_EPS)
            c1 = [x for x in action_names if terminal[x] <= mn + _TOL]
            if (max(vals) - mn <= eps) or (any(x in sitio for x in c1) and any(x not in sitio for x in c1)):
                resto = [x for x in action_names if x not in sitio]
                return sel0(resto, {x: preds[x] for x in resto}, {x: terminal[x] for x in resto}, ({x: meta[x] for x in resto} if meta else meta), *a, **kw)
        return sel0(action_names, preds, terminal, meta, *a, **kw)
    return sel

# ── el ciclo de vida del cuaderno ──
def ruta_de(criatura):
    return os.path.join(os.environ.get("CUADERNO_DIR", os.path.join(os.getcwd(), "cuadernos_P7")), f"cuaderno_P7_{criatura}.json")
def arranca(criatura, ruta, registra=None):
    ESTADO["registra"] = registra; ESTADO["ruta"] = ruta; ESTADO["ventana"] = None; ESTADO["huellas"] = []
    if not ON: ESTADO["cuaderno"] = None; return None
    c = Cuaderno.lee(ruta, criatura) if (CUADERNO_ON and not BORRADO) else Cuaderno(criatura)
    ESTADO["cuaderno"] = c
    if registra: registra({"k": "P7_cuaderno", "momento": "arranque", "ruta": ruta, "leido": bool(CUADERNO_ON and not BORRADO and ruta and os.path.exists(ruta)), "dia": c.dia_actual(), "contenido": c.volcado(), "entorno": entorno()})
    return c
def termina(registra=None):
    c = ESTADO["cuaderno"]; registra = registra or ESTADO["registra"]
    if c is None or not CUADERNO_ON or ESTADO.get("terminado"): return None
    ESTADO["terminado"] = True
    ruta = ESTADO["ruta"]; esc = c.escribe(ruta) if ruta else None
    if registra: registra({"k": "P7_cuaderno", "momento": "fin", "ruta": ruta, "escrito": bool(esc), "contenido": c.volcado(), "huellas": ESTADO["huellas"]})
    return esc

# ── la ventana de la experiencia (pieza A) ──
def _canal(you, mundo):
    return any(e.get("id") == "channeling" and e.get("item") == kit(mundo) for e in (you.get("effects") or []))
def _dano_conocido(obs, mundo, tick):
    """Dano de este tic que el cuerpo sabe explicar: anillo estando fuera; golpe de un rival a la vista y en alcance."""
    you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); conocido = 0.0; fuentes = []
    agentes = {a.get("slot"): a for a in ((obs.get("visible") or {}).get("agents") or []) if a.get("pos")}
    for d in (you.get("damage_taken") or []):
        src = str(d.get("source") or ""); amt = float(d.get("amount") or 0.0)
        if src == "zone":
            if situacion(mundo, pos, tick) == "fuera": conocido += amt; fuentes.append("anillo")
        elif src.startswith("P"):
            try: sl = int(src[1:])
            except ValueError: continue
            a = agentes.get(sl)
            if a is None: continue
            h = a.get("hand"); hid = h if isinstance(h, str) else (h or {}).get("id")
            it = mundo.items.get(hid) if (hid and hid != "none") else None
            alcance = int(getattr(it, "range", 1) or 1) if it is not None else 1
            if max(abs(a["pos"][0] - pos[0]), abs(a["pos"][1] - pos[1])) <= alcance: conocido += amt; fuentes.append(src)
    return conocido, fuentes
def ventana(self, obs, radio):
    """Se llama cada tic vivo con la observacion real y la radiografia de la decision."""
    mundo, mem, tick = self.mundo, self.mem, self.tick; you = obs.get("you") or {}; c = ESTADO["cuaderno"]; v = ESTADO["ventana"]
    if c is None or mundo is None: return
    en_canal = _canal(you, mundo)
    # [P7-10, visto el dia 3 del freno: con el canal abierto el cuerpo regalo la pila de botiquines al hermano (`soltar_first_aid`); el canal
    # siguio sin botiquin, la vida no subio y la ventana lo apunto como "cura 0, firme"] Un regalo durante la ventana la anula: no es un uso.
    if str((radio or {}).get("elegido") or "").startswith("soltar_" + kit(mundo)) and (v is not None or en_canal): ESTADO["regalo_en_ventana"] = tick
    if v is None:
        if en_canal:
            d0, como0 = dist_hermano(obs, mundo, mem); pos = tuple(you.get("pos") or (0, 0))
            # la situacion es la del tic en que DECIDIO usar (la misma que vio la imaginacion), si ese tic fue el anterior
            us = ESTADO.get("ultima_sit"); sit = us[1] if (us and us[0] == tick - 1) else situacion(mundo, pos, tick)
            uh = ESTADO.get("ultima_heal"); heal_us = uh[1] if (uh and uh[0] == tick - 1) else None
            ESTADO["ventana"] = {"t0": tick, "situacion": sit, "hp0": float(you.get("hp") or 0.0), "unidades0": unidades(you), "dist0": d0, "como0": como0,
                                 "mal0": malestar_ejes(radio), "conocido": 0.0, "fuentes": [], "total": 0.0, "ignorancia_antes": ignorancia_de(mundo), "heal_imaginado": heal_us,
                                 "hp_max": float(getattr(mem, "hp_max", None) or 100.0), "techo": False, "kits0": kits_en(you, mundo)}
            if ESTADO["registra"]: ESTADO["registra"]({"k": "P7_uso", "tick": tick, "situacion": ESTADO["ventana"]["situacion"], "hp": you.get("hp"), "ignorancia": ignorancia_de(mundo), "heal_imaginado": heal_us, "creencia_cuerpo": (c.creencia_cuerpo(kit(mundo), sit) if CUADERNO_ON else None), "esperanza": esperanza_cuerpo(mundo), "k_ganas": k_ganas(mundo)})
        return
    if tick > v["t0"]:
        con, fu = _dano_conocido(obs, mundo, tick); v["conocido"] += con; v["fuentes"] += fu
        v["total"] += sum(float(d.get("amount") or 0.0) for d in (you.get("damage_taken") or []))
        if float(you.get("hp") or 0.0) >= v["hp_max"]: v["techo"] = True      # [P7-7] la vida toco techo dentro de la ventana
    if en_canal: return
    # el canal ya no esta: se cierra la ventana en este tic
    d1, como1 = dist_hermano(obs, mundo, mem); mal1 = malestar_ejes(radio)
    efecto = {"cuerpo": (float(you.get("hp") or 0.0) - v["hp0"]) + v["conocido"], "recursos": unidades(you) - v["unidades0"],
              "vinculo": ((d1 - v["dist0"]) if (d1 is not None and v["dist0"] is not None) else 0.0)}
    importancia = {dom: (mal1.get(dom, 0.0) - v["mal0"].get(dom, 0.0)) for dom in DOMINIOS}
    # [P7-7, fallo de taller visto el dia 1 del humo: tres ventanas se cerraron porque el cuerpo rompio su propio canal moviendose; el
    # botiquin seguia en el zurron y se apuntaron como "cura -0,2 / +0,28 / -0,72"] Si la unidad no se gasto, el canal se interrumpio: no es
    # una experiencia de la cosa; la huella se registra como interrumpida y no entra en el cuaderno.
    rg = ESTADO.get("regalo_en_ventana"); regalado = rg is not None and v["t0"] <= rg <= tick; ESTADO["regalo_en_ventana"] = None
    interrumpido = (kits_en(you, mundo) >= v.get("kits0", 0) and v.get("kits0") is not None) or regalado
    r = c.apunta(kit(mundo), v["situacion"], efecto, importancia, tick=v["t0"], al_menos=v["techo"]) if (CUADERNO_ON and not interrumpido) else None
    h = {"k": "P7_huella", "t0": v["t0"], "t_fin": tick, "situacion": v["situacion"], "hp0": v["hp0"], "hp_fin": you.get("hp"), "hp_max": v["hp_max"], "al_menos": v["techo"], "interrumpido": interrumpido, "regalado": regalado, "dano_total": round(v["total"], 2), "dano_conocido": round(v["conocido"], 2),
         "fuentes_conocidas": v["fuentes"], "efecto": {k: round(x, 4) for k, x in efecto.items()}, "importancia": {k: round(x, 4) for k, x in importancia.items()}, "vinculo_como": [v["como0"], como1],
         "intensidad": (r or {}).get("intensidad"), "creencia_despues": c.creencia(kit(mundo), v["situacion"]) if CUADERNO_ON else None, "ignorancia_despues": ignorancia_de(mundo), "apuntado": bool(r)}
    ESTADO["huellas"].append(h)
    if ESTADO["registra"]: ESTADO["registra"](h)
    ESTADO["ventana"] = None

# ── los enganches ──
def aplica(clase, registra=None):
    """Engancha las piezas B, C, D y la ventana de A sobre el modulo del decisor, el del appraisal y la clase del alma. Devuelve lo hecho."""
    ESTADO["registra"] = registra
    if not ON: return {"P7": False}
    _oc = D.candidatos; _of = A.filas; _ow = A.riqueza_W; _oa = A.appraise; _op = D._promesa; _od = clase.decidir; _oo = D._obs_prevista
    if NOVEDAD_ON and not SABE: A.REPARTO["R-CURIOSIDAD"] = REPARTO_CUR            # la fila entra en el reparto desde fuera (negativa)
    # B · imaginacion
    def _cands(obs, mundo, mem, tick, bloqueos=None):
        out = []
        you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0))
        for n, r in _oc(obs, mundo, mem, tick, bloqueos):
            if n == "usar_botiquin" and not SABE:
                h = heal_imaginado(mundo, pos, tick); r = dict(r, heal=h); ESTADO["ultima_heal"] = (tick, h); ESTADO["ultima_sit"] = (tick, situacion(mundo, pos, tick))
            out.append((n, r))
        if NOVEDAD_ON and not SABE and kits_en(you, mundo) == 0 and D._pack_con(list(you.get("pack") or []), kit(mundo), 1, mundo) != list(you.get("pack") or []):
            # F [P7-7, decision 2] · LA CURIOSIDAD ABRE CAMINO: la carencia de ignorancia genera el mismo candidato de ir a por la cosa que
            # generan las ganas de un objeto (`ir_objeto`, decisor_zs.py:458-462: tipo "ir" con `recoger`, y la imaginacion, si llega, pone el
            # objeto en el zurron, :805-813): destino = el botiquin mas cercano, visto ahora o recordado (`mem.objetos_vistos`), no cedido.
            # Al llegar, la foto lo tiene en el zurron y la fila R-CURIOSIDAD pasa a alivio 0,5. Ningun numero nuevo. Si `ir_objeto` ya va
            # al mismo sitio no se duplica. Las mismas dos condiciones de las ganas de hoy: con el zurron lleno la cosa no es adquirible
            # (`_promesa`, decisor_zs.py:650-652: "zurron lleno: no es adquirible") y con la cosa en mi casilla no hay a donde ir
            # (`_mejor_objeto` devuelve mi casilla y `ir_objeto` no se crea, :459; de eso se ocupa `coger`). [Medido en la primera corrida
            # de F2 sin estas dos condiciones: con el zurron lleno ganaba un paseo sin alivio hacia otro botiquin (946 de 1.896 tics encima
            # de uno), y encima de un botiquin con sitio libre le quitaba el tic a `coger` 276 de 894 veces, hacia OTRO botiquin.]
            kid = kit(mundo); ced = getattr(mem, "cedidos", {}); vis = obs.get("visible") or {}
            sitios = {tuple(it.get("pos") or ()): (kid, int(it.get("n") or 1), float(A.VALOR_NIVEL["cajones"])) for it in (vis.get("items") or []) if it.get("id") == kid and it.get("pos")}
            for p_, v_ in (getattr(mem, "objetos_vistos", None) or {}).items():
                if v_ and v_[0] == kid and tuple(p_) not in sitios: sitios[tuple(p_)] = tuple(v_)
            if pos in sitios: sitios = {}
            sitios = {p_: v_ for p_, v_ in sitios.items() if p_ not in ced}
            if sitios:
                dest = min(sitios, key=lambda p_: math.dist(pos, p_))
                if not any(n == "ir_objeto" and tuple(r.get("destino") or ()) == dest for n, r in out):
                    cuerpos = frozenset(tuple(a.get("pos") or ()) for a in (vis.get("agents") or []) if a.get("pos"))
                    out.append(("ir_curioso", {"tipo": "ir", "destino": dest, "cuerpos": cuerpos, "recoger": sitios[dest]}))
        if SITIO_ON:
            # E · hacer sitio: cuando el PRIMER objeto de mi casilla no cabe (zurron lleno y sin pila donde apilarlo), y por cada consumible
            # de otra clase que llevo, un candidato. [P7-7, decision 3] El mundo entrega el primero de la lista de la casilla (90 de 90
            # cogidas con varias clases en la casilla, `coge_P7_7.py`), igual que imagina `coger` (decisor_zs.py:478-482); lo soltado cae al
            # final de la lista (6 de 6), asi que `coger` al tic siguiente sigue viendo el mismo primero. Hacer sitio para un segundo objeto
            # (P7-6) imaginaba coger lo que el mundo no entrega.
            pack = list(you.get("pack") or []); aqui = [it for it in ((obs.get("visible") or {}).get("items") or []) if tuple(it.get("pos") or ()) == pos and pos not in getattr(mem, "cedidos", {})]
            if aqui and not any(s_ is None for s_ in pack):
                for it in aqui[:1]:
                    cid = it.get("id")
                    if D._pack_con(pack, cid, int(it.get("n") or 1), mundo) != pack: continue   # cabe (apilado): lo toma `coger`
                    for i, sl in enumerate(pack):
                        if not sl or sl.get("id") == cid: continue
                        itm = mundo.items.get(sl.get("id"))
                        if itm is None or itm.kind != "ikConsumable": continue
                        out.append((f"hacer_sitio_{sl['id']}_por_{cid}", {"tipo": "soltar", "idx": i, "item": f"{sl['id']}|{cid}", "n": int(sl.get("n") or 1), "coge": cid, "suelta": sl["id"]}))
        return out
    def _obs_prevista(obs, mundo, mem, tick_eval, pos, hp, pack, hand, ver_pareja, golpe=None, suelta=None, body=False):
        if suelta is not None and isinstance(suelta[0], str) and "|" in suelta[0]:
            su, co = suelta[0].split("|", 1); pack = D._pack_con(list(pack), co, 1, mundo); suelta = (su, suelta[1])
        return _oo(obs, mundo, mem, tick_eval, pos, hp, pack, hand, ver_pareja, golpe, suelta, body)
    # C · ganas: las constantes del modulo, escaladas antes de cada `filas`; el termino del botiquin en W
    def _filas(obs, mundo, mem, tick):
        # [P7-6] las ganas del botiquin son TODA la fila R-ACOPIO: tambien la rama "con una sola no basta" (ACOPIO_POR_DOS, appraisal:221,
        # :951-953), que sin escalar hacia perder a `coger` el primer botiquin (F2 de P7-6: +0,10 de acopio contra -0,09 de curiosidad)
        k = k_ganas(mundo); A.ACOPIO_M = ACOPIO_M0 * k; A.ACOPIO_POR_DOS = ACOPIO_POR_DOS0 * k; A.W_TARGET = (W_TARGET0 if SABE else w_target(k, mundo))
        try:
            F = _of(obs, mundo, mem, tick)
            if not SABE: regalo_aprendido(obs, mundo, mem, tick, F, _of)      # [P7-8] con las MISMAS constantes escaladas (F_sin comparable)
        finally: A.ACOPIO_M = ACOPIO_M0; A.ACOPIO_POR_DOS = ACOPIO_POR_DOS0; A.W_TARGET = W_TARGET0
        if NOVEDAD_ON and not SABE:
            M, calma, ign, al = curiosidad_M(obs, mundo, F); F["R-CURIOSIDAD"] = M; F["_curiosidad"] = {"calma": round(calma, 4), "ignorancia": round(ign, 4), "alivio": al}
        return F
    def _riqueza(you, mundo):
        W, d = _ow(you, mundo)
        if SABE: return W, d
        k = k_ganas(mundo); d2 = dict(d); d2["botiquin"] = float(d.get("botiquin") or 0.0) * k
        return sum(d2.values()), d2
    # D · curiosidad: la fila ya va en `filas`; `appraise` la reparte sola por estar en A.REPARTO. La promesa de ir a por la cosa:
    def _promesa(obs, mundo, mem, tick, item_id):
        base = _op(obs, mundo, mem, tick, item_id)
        if SABE or not NOVEDAD_ON or item_id != kit(mundo): return base
        you = obs.get("you") or {}
        if kits_en(you, mundo) >= 1: return base                   # ya la lleva: tenerla no alivia mas
        # [P7-16, (c)] las ganas de una cosa no suman alivio de curiosidad cuando no se podria llevar (zurron lleno y sin pila donde apilarla)
        if PIDE2 and D._pack_con(list(you.get("pack") or []), kit(mundo), 1, mundo) == list(you.get("pack") or []): return base
        t, F = ESTADO["calma_cache"]
        if t != tick:
            F = _of(obs, mundo, mem, tick); ESTADO["calma_cache"] = (tick, F)
        M, calma, ign, al = curiosidad_M(obs, mundo, F)
        return base + M * (1.0 - ALIVIO_ZURRON)
    # A · la ventana, sobre el alma
    def decidir(self, obs, _d=_od):
        if ESTADO["cuaderno"] is None and getattr(self, "mundo", None) is not None:
            arranca(self.mundo.slot, ruta_de(self.mundo.slot), ESTADO["registra"])        # el asiento se sabe con el player_config
        accion, radio = _d(self, obs)
        if radio is not None and str(radio.get("elegido") or "").startswith("hacer_sitio_"):
            pos = tuple((obs.get("you") or {}).get("pos") or ()); ced = getattr(self.mem, "cedidos", None)
            if ced is not None and pos in ced: del ced[pos]          # no es una cesion: es hacer sitio
            if ESTADO["registra"]: ESTADO["registra"]({"k": "P7_sitio", "tick": self.tick, "elegido": radio.get("elegido"), "d": {k_: (v["d"] if isinstance(v, dict) else v) for k_, v in (radio.get("candidatos") or {}).items()}})
        if radio is not None and getattr(self, "phase", None) == "live" and NOVEDAD_ON and not SABE and (self.tick % 250 == 0):
            cu = ((radio.get("ahora") or {}).get("filas") or {}).get("R-CURIOSIDAD") or {}
            if ESTADO["registra"]: ESTADO["registra"]({"k": "P7_curiosidad", "tick": self.tick, "M": cu.get("M", 0.0), "ignorancia": round(ignorancia_de(self.mundo), 4)})
        try:
            if getattr(self, "phase", None) == "live" and radio is not None and (CUADERNO_ON or NOVEDAD_ON): ventana(self, obs, radio)
        except Exception as ex:
            if ESTADO["registra"]: ESTADO["registra"]({"k": "P7_error", "tick": getattr(self, "tick", None), "error": repr(ex)[:200]})
        return accion, radio
    D.candidatos, A.filas, A.riqueza_W, D._promesa, clase.decidir = _cands, _filas, _riqueza, _promesa, decidir
    if SITIO_ON: D._obs_prevista = _obs_prevista
    if SITIO_ON and SITIO_EMPATE and not getattr(D.select_tiebreak, "_P7_sin_sitio", False):
        D.select_tiebreak = desempate_sin_sitio(D.select_tiebreak); D.select_tiebreak._P7_sin_sitio = True
    return {"P7": True, **entorno()["efectivo"]}

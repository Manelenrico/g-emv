"""[P7-13] PEDIR Y DEJAR DE PEDIR (pieza J; diseno de Manel, 4-oct-2026). Enganchado DESDE FUERA, como `descubre_P7.py`: no toca un byte del
cuerpo congelado ni de `paintball/alma/parte.py`. Solo para el botiquin (las flechas son un peldano posterior).

  1. PEDIR ES UN ESTADO QUE VIAJA EN EL PARTE. El parte E1 (`alma/parte.py`: "E1 P<slot> t<tick> <x>,<y> h<hp> v<0|1> b<n> a<0|1>[ s<sl>][ <x>,<y>]")
     gana un campo al final mientras la criatura pide: " q<letra>", con la letra de la clase leida del catalogo del mundo (`parte2.alfabeto`,
     no cableada). Cuando deja de pedir, el parte siguiente va sin el campo. No hay mensajes nuevos: es el mismo parte de cada 48 tics.
     Se envuelven `parte.emite` y `parte.parsea` (atributos del modulo, que es como los llaman `policy_cortex.py:966` y
     `appraisal_zs_v42_exp.py:578`); el parser del cinco sigue siendo estricto con el resto.
  2. CUANDO PIDE: lo decide su cuerpo. Pide el botiquin si (a) no lleva ninguno, (b) no ve ninguno en el suelo (`obs.visible.items`) y
     (c) la PROMESA del botiquin es mayor que cero: `decisor_zs._promesa` (decisor_zs.py:620-683; para el botiquin, :643-656: lo que baja
     R-ACOPIO al imaginarlo en el zurron), que es el mismo numero que hoy enciende las ganas de ir a por el (`_mejor_objeto`,
     decisor_zs.py:698-699) y que `descubre_P7` ya calcula con la creencia y la esperanza de la criatura (k de las ganas, :332; mas lo que
     alivia la curiosidad, :346-355). Ningun umbral nuevo: mayor que cero, como alli.
  3. EL REGALO MIRA EL PEDIDO: con un botiquin en el suelo de la foto, las filas que regalan (`descubre_P7.FILAS_REGALO`: S-DANO-PAREJA,
     S-HERIDO, R-HERMANO-FALTA, S-PROVISION) solo cuentan lo que ese botiquin les alivia si el ultimo parte FRESCO del hermano
     (`mem.parte_fresco`, caducidad del cinco) lleva el pedido. Sin pedido, esas filas valen lo que valdrian sin el botiquin en el suelo
     (se recalculan con el quitado de la vista, como hace la pieza G). Con pedido, quedan como las deja la pieza G (por la creencia de quien
     regala; en TECHO, enteras). Se reevalua en cada decision: si el pedido desaparece, el regalo pierde su razon.
  4. Igual en los cuatro brazos. Interruptor GEMV_P7_PIDE (0 por defecto: apagado en F1).

[P7-16] PEDIR CORREGIDO (diseno de Manel; interruptor GEMV_P7_PIDE2, 0 por defecto para que los campos jugados se repliquen como se jugaron):
  (a) EL PEDIDO SE CIERRA AL TENER, NO AL VER. [P7-17, decision de Manel, 5-oct: sustituye a la regla de P7-16] Se abre cuando la criatura no
      lleva botiquin, lo quiere (sus propias ganas: la promesa mayor que cero), puede llevarlo (regla b) y no ve ninguno (si ve uno, va a por
      el); una vez abierto se cierra SOLO cuando el botiquin esta en el zurron (o al morir): ver uno no cierra un pedido ya abierto. Una criatura
      sana sin botiquin puede pedir uno de reserva. [En P7-16 se cerraba ademas con la vida al maximo; eso se quita.]
  (b) SOLO SE PIDE LO QUE SE PODRIA COGER: con un hueco para el (`decisor_zs._pack_con`, la misma prueba de "cabe" del cuerpo) y la promesa
      mayor que cero; o, con el zurron lleno, si hacer sitio ganaria: el propio cuerpo, puesto encima de un botiquin con lo que lleva ahora,
      elegiria `hacer_sitio_<algo>_por_<botiquin>` (se le pregunta a `decide` sobre una copia de la escena y de la memoria). Si no, no se
      abre. [P7-17] Es condicion para ABRIR; un pedido ya abierto no se cierra por dejar de caber.
  (c) (en `descubre_P7._promesa`) las ganas de una cosa no suman alivio de curiosidad cuando no se podria llevar.

[P7-19, decision de la mesa] LO DADO NO ESTA ENTREGADO MIENTRAS QUIEN LO DIO LO PISA (con GEMV_P7_PIDE2; GEMV_P7_PISO=0 lo apaga, solo para el
banco "antes"). Al elegir `soltar_<botiquin>` la criatura apunta la casilla de su regalo (en su estado de la partida, no en `mem.cedidos`). En
las fotos en que ella misma esta sobre esa casilla y el botiquin sigue ahi, las filas que regalan no cuentan el alivio: valen lo que valian
antes de darlo (el botiquin cuenta como si siguiera en su zurron). Quedarse encima no alivia; apartarse, si. En la foto de regalar, que se evalua
antes de apuntar nada, el alivio cuenta como hasta ahora. La marca se borra cuando, teniendo la casilla al lado o debajo, el botiquin ya no esta.
Ningun numero nuevo. [Visto en P7-18: quien regalaba se quedaba encima y el hermano no podia entrar: 3.030 de 3.033 pasos bloqueados.]
"""
from __future__ import annotations
import copy, re
from alma import parte as PARTE
from alma import decisor_zs as D
from alma import appraisal_zs_v42_exp as A
import descubre_P7 as X
import parte2 as P2

PIDE_ON = X._on("GEMV_P7_PIDE")
CAMPO = " q"
_RE_Q = re.compile(r" q([A-Za-z]+)$")
ESTADO = {"registra": None, "pedia": False, "mis_regalos": {}, "piso_apagado": False}

def letra(mundo): return P2.alfabeto(mundo)[X.kit(mundo)]

def pide(obs, mundo, mem, tick):
    """(¿pide el botiquin?, detalle). Las tres condiciones del punto 2."""
    you = obs.get("you") or {}; kid = X.kit(mundo)
    a_bordo = X.kits_en(you, mundo)
    a_la_vista = any(it.get("id") == kid for it in ((obs.get("visible") or {}).get("items") or []))
    promesa = float(D._promesa(obs, mundo, mem, tick, kid)) if a_bordo == 0 else 0.0
    return (a_bordo == 0 and not a_la_vista and promesa > 0.0), {"a_bordo": a_bordo, "a_la_vista": a_la_vista, "promesa": round(promesa, 5)}

PIDE2 = X._on("GEMV_P7_PIDE2")
PISO = PIDE2 and X._on("GEMV_P7_PISO", "1")
def piso_mi_regalo(obs, mundo):
    """[P7-19] ¿En esta foto estoy sobre la casilla de un regalo mio y el botiquin sigue ahi?"""
    if not ESTADO.get("mis_regalos") or ESTADO.get("piso_apagado"): return False
    pos = tuple((obs.get("you") or {}).get("pos") or ()); kid = X.kit(mundo)
    return pos in ESTADO["mis_regalos"] and any(it.get("id") == kid and tuple(it.get("pos") or ()) == pos for it in ((obs.get("visible") or {}).get("items") or []))
def cabe(you, mundo):
    pack = list(you.get("pack") or []); return D._pack_con(pack, X.kit(mundo), 1, mundo) != pack
def haria_sitio(obs, mundo, mem, tick):
    """¿El cuerpo, encima de un botiquin con lo que lleva ahora, elegiria hacer sitio para el? Se le pregunta a `decide` (el de antes de los
    ganchos de lectura del banco) sobre una copia de la escena con un botiquin en su casilla y una copia de la memoria."""
    kid = X.kit(mundo); ob2 = copy.deepcopy(obs); pos = list((ob2.get("you") or {}).get("pos") or ()); vis = ob2.setdefault("visible", {})
    vis["items"] = [{"id": kid, "n": 1, "pos": pos}] + [it for it in (vis.get("items") or []) if list(it.get("pos") or ()) != pos]
    try: _, ra = ESTADO["decide0"](ob2, mundo, copy.deepcopy(mem), tick)
    except Exception: return False
    el = str((ra or {}).get("elegido") or ""); return el.startswith("hacer_sitio_") and el.endswith("_por_" + kid)
def pide2(obs, mundo, mem, tick):
    """[P7-16] (¿pide?, detalle), con el pedido corregido. Lee y no cambia ESTADO["pedia"]."""
    you = obs.get("you") or {}; kid = X.kit(mundo); a_bordo = X.kits_en(you, mundo)
    a_la_vista = any(it.get("id") == kid for it in ((obs.get("visible") or {}).get("items") or []))
    hp = float(you.get("hp") or 0.0); falta = hp < float(getattr(mem, "hp_max", None) or 100.0) - 1e-9          # (solo se apunta; ya no decide nada)
    hueco = cabe(you, mundo); promesa = float(D._promesa(obs, mundo, mem, tick, kid)) if (a_bordo == 0 and hueco) else 0.0
    # [P7-17, decision de Manel, 5-oct] se ABRE si no lleva botiquin, lo quiere (promesa > 0) y puede llevarlo (hueco, o hacer sitio ganaria);
    # se CIERRA solo cuando lo tiene en el zurron (o al morir). Ni verlo, ni tener la vida entera, ni dejar de caberle lo cierran.
    # [P7-17, correccion de la mesa] para ABRIRLO hace falta ademas que no vea ningun botiquin (si ve uno, va a por el); ver uno no cierra
    # un pedido ya abierto.
    sitio = bool(a_bordo == 0 and not ESTADO["pedia"] and not a_la_vista and not hueco and haria_sitio(obs, mundo, mem, tick))
    podria = (hueco and promesa > 0.0) or sitio
    si = a_bordo == 0 and (ESTADO["pedia"] or (podria and not a_la_vista))
    return si, {"a_bordo": a_bordo, "a_la_vista": a_la_vista, "promesa": round(promesa, 5), "falta_vida": falta, "hueco": hueco, "haria_sitio": sitio}

def hermano_pide(mundo, mem, tick):
    p = mem.parte_fresco(tick)
    return p is not None and letra(mundo) in (p.get("pido") or ())

def aplica(clase, registra=None):
    ESTADO["registra"] = registra; ESTADO["pedia"] = False; ESTADO["decide0"] = D.decide; ESTADO["mis_regalos"] = {}; ESTADO["piso_apagado"] = False
    if not PIDE_ON: return {"PIDE": False}
    _e0 = PARTE.emite; _p0 = PARTE.parsea; _f0 = A.filas
    def _emite(obs, tick, mundo, mem, ventana_ticks):
        texto = _e0(obs, tick, mundo, mem, ventana_ticks)
        si, det = (pide2 if PIDE2 else pide)(obs, mundo, mem, tick)
        if si:
            t2 = texto + CAMPO + letra(mundo)
            if PARTE.ascii_limpio(t2): texto = t2
            else: si = False; det["no_cabe"] = len(t2)
        motivo = None
        if ESTADO["pedia"] and not si:
            if PIDE2: motivo = "lo lleva" if det["a_bordo"] > 0 else "no cabe en el parte"
            else: motivo = "lo lleva" if det["a_bordo"] > 0 else "lo ve" if det["a_la_vista"] else "ya no le alivia (promesa 0)" if not det.get("no_cabe") else "no cabe en el parte"
        if ESTADO["registra"]: ESTADO["registra"]({"k": "P7_pido", "tick": tick, "pide": bool(si), "abre": bool(si and not ESTADO["pedia"]), "cierra": motivo, "largo": len(texto), "texto": texto, **det})
        ESTADO["pedia"] = bool(si)
        return texto
    def _parsea(texto):
        pido = ()
        if isinstance(texto, str):
            m = _RE_Q.search(texto)
            if m: pido = tuple(m.group(1)); texto = texto[:m.start()]
        p = _p0(texto)
        if p is not None: p["pido"] = pido
        return p
    def _filas(obs, mundo, mem, tick):
        F = _f0(obs, mundo, mem, tick)
        vis = obs.get("visible") or {}; kid = X.kit(mundo); items = vis.get("items") or []
        if not any(it.get("id") == kid for it in items): return F
        piso = PISO and piso_mi_regalo(obs, mundo)                 # [P7-19] sobre mi propio regalo: no esta entregado, pida o no pida
        if hermano_pide(mundo, mem, tick) and not piso: return F
        ob2 = dict(obs); ob2["visible"] = dict(vis, items=[it for it in items if it.get("id") != kid])
        if piso:
            # [P7-19] sobre mi propio regalo las filas que regalan valen lo que valian ANTES de darlo: el botiquin cuenta como si siguiera en mi
            # zurron (no entregado). [Primera version, descartada en el banco: "lo que valdrian sin el botiquin en el suelo"; como quien regala
            # se queda sin botiquines, S-PROVISION (que exige llevar alguno, appraisal_zs_v42_exp.py:1317) valia 0 encima y fuera: sin fuerza.]
            pp = tuple((obs.get("you") or {}).get("pos") or ()); n_ = int(ESTADO["mis_regalos"].get(pp) or 1); y2 = dict(obs.get("you") or {})
            y2["pack"] = D._pack_con(list(y2.get("pack") or []), kid, n_, mundo); y2["_bot_real"] = int(y2.get("_bot_real") or 0) + n_
            ob2["you"] = y2; ob2["visible"] = dict(vis, items=[it for it in items if not (it.get("id") == kid and tuple(it.get("pos") or ()) == pp)])
        F_sin = _f0(ob2, mundo, mem, tick); cambio = {}
        for fila in X.FILAS_REGALO:
            a, b = F.get(fila, 0.0), F_sin.get(fila, 0.0)
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and float(a or 0.0) != float(b or 0.0):
                F[fila] = b; cambio[fila] = (round(float(a or 0.0), 5), round(float(b or 0.0), 5))
        if cambio: F["_piso_mi_regalo" if piso else "_sin_pedido"] = cambio
        return F
    PARTE.emite, PARTE.parsea, A.filas = _emite, _parsea, _filas
    if PISO:
        _dd = clase.decidir
        def decidir(self, obs, _d=_dd):
            mundo = getattr(self, "mundo", None); you = obs.get("you") or {}; pos = tuple(you.get("pos") or ())
            if mundo is not None and ESTADO["mis_regalos"]:      # la marca se borra cuando, con la casilla al lado o debajo, el botiquin ya no esta
                kid = X.kit(mundo); hay = {tuple(it.get("pos") or ()) for it in ((obs.get("visible") or {}).get("items") or []) if it.get("id") == kid}
                ESTADO["mis_regalos"] = {p: n_ for p, n_ in ESTADO["mis_regalos"].items() if p in hay or max(abs(p[0] - pos[0]), abs(p[1] - pos[1])) > 1}
            accion, radio = _d(self, obs)
            if mundo is not None and radio is not None and str(radio.get("elegido") or "").startswith("soltar_" + X.kit(mundo)) and pos:
                ESTADO["mis_regalos"][pos] = max(1, X.kits_en(you, mundo), int(ESTADO["mis_regalos"].get(pos) or 0))      # cuantos doy (la pila entera)
            return accion, radio
        clase.decidir = decidir
    return {"PIDE": True, "PIDE2": PIDE2, "PISO": PISO, "campo": CAMPO.strip(), "filas": list(X.FILAS_REGALO)}

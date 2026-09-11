"""APPRAISAL ZERO-SUM — la tabla de signos v1, fila a fila.

Contrato IDENTICO al appraisal de machina hacia motor/model.py:
    appraise(...) -> motor.model.State
acumulando pF/nF/pR/nR/pS/nS y construyendo el State al final (igual que
appraisal/appraisal_v3.py:230). Las constantes del motor se IMPORTAN; ni una
sola se copia a mano (regla de la casa).

Mecanismo de la tabla (paintball/tabla_signos_v1.md): cada fila produce una
magnitud M y la reparte entre los tres ejes con fracciones que suman 1. Las
filas aversivas suman a las fuerzas NEGATIVAS (f-); la unica apetitiva
(R-LLAMADA) suma a las POSITIVAS (f+).

Devuelve ademas la RADIOGRAFIA: M de cada fila y su reparto. Es la materia de
forense y atribucion que pide el prompt.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from motor.model import State          # el contrato hacia el motor

# ── numeros de la tabla ──────────────────────────────────────────────────────
# [Manel] = sellado.  [impl] = eleccion de la mesa, declarada en el acta.
VENENO_MULT = 1.5            # [Manel] F-DANO x1.5 mientras envenenado

# ── LA CUESTA DE LA MUERTE (PROMPT_43) ──────────────────────────────────────
# El malestar por vida perdida deja de ser PLANO y se hace CONVEXO cerca de la
# muerte: perder de 15 a 1 pesa mucho mas que perder de 100 a 86. Motivo
# medido (39): a hp 1 con botiquin en la mochila, curarse PERDIA por 0,25 —
# la pendiente no gritaba. Forma: por debajo del umbral de vida perdida la
# fila es IDENTICA a la v19 (la cuesta es de la muerte, no de los rasguños);
# por encima, se suma un termino cuadratico:
#     u = vida perdida / vida maxima
#     M = u                                        si u <= CUESTA_UMBRAL_U
#     M = u + G * ((u-U0)/(1-U0))^2                si u >  CUESTA_UMBRAL_U
# C1-continua en el umbral (el termino entra con derivada 0). M puede superar
# 1.0 — igual que ya hacia VENENO_MULT — y el State aplica su techo de volumen
# como siempre (la cuesta vive en la TABLA; el motor la digiere sin cambios).
# Ninguna otra fila cambia; el reparto F/R/S de F-DANO (0.8/0.1/0.1) queda.
CUESTA_UMBRAL_U = 0.4        # [impl] hp 60 de 100: de ahi para arriba, intacto

# ── R-ACOPIO (PROMPT_46): la mochila sin botiquin duele un poco, siempre ────
# La ficha aparcada desde el principio (R-CARENCIA como acopio). Motivo medido
# (44/45): solo el 15 % de los tics en banda critica llevan botiquin a bordo, y
# la mitad de las agonias son escaleras de 5+ segundos — muere de descenso
# anunciado con las manos vacias. La fila es un FONDO que ordena la calma, no
# una obsesion que compita con el miedo (calibrada en verifica_46 contra la
# jerarquia: perseguido, el acopio NO compra riesgo).
# Alivio SOLO por adquisicion cierta: la foto de `ir_objeto` ya preve recoger
# al llegar (PROMPT_07 B) y la de `coger` mete el objeto en el zurron previsto,
# asi que la fila se apaga sola en esas fotos. Al gastar el botiquin para
# CURARSE, la foto de `usar` marca `_cura_en_curso` (el mismo patron que
# `_hp_est` del 23): gastar la cura ES el proposito de llevarla, no pobreza —
# sin esa marca la fila gravaria curarse, contra la pila entera de C.
# ── EL MURO DEL MIEDO (PROMPT_47) ───────────────────────────────────────────
# Simetria con la cuesta: a la vida, cuesta (morir grita); a la distancia del
# cazador, muro (el peligro cercano APLASTA). Motivo medido (46): el miedo a
# bocajarro ganaba por 0,02512 — el aparcado del 21 con la culpa probada — y
# sobre ese muro fino no se puede colgar ninguna hambre de fondo.
# Forma (patron de la cuesta): el factor de cercania de S-7 se hace CONVEXO
# por debajo de la distancia-ancla, y MAS ALLA queda SIN CAMBIO POR
# CONSTRUCCION:
#     f_cerca' = f_cerca                                  si d >= MURO_D0
#     f_cerca' = f_cerca * (1 + K*((D0-d)/D0)^2)          si d <  MURO_D0
# ACTIVACION por bocajarro PRESENTE (R1): solo cuando AHORA hay un agresor
# activo visible a menos de D0 (el evaluador estampa `_muro_on` desde la obs
# real; sin marcador, filas lo deduce de la propia obs). Con el agresor lejos,
# TODAS las fotos quedan bit-identicas a la v24: P2 por construccion.
# El techo sellado del 09 (AGRESOR_CAP_TOTAL) se respeta: el muro empuja
# hasta el techo, no lo rompe.
MURO_D0 = 4.0                # [impl] geometria del catalogo: alcance melee
                             # maximo 2 (spear) + ~2 casillas que un cazador
                             # rapido cierra durante nuestro enfriamiento
MURO_K = 3.0                 # [Manel, resello del 48] P1' resellada sobre la
                             # geometria MEDIDA del 47: ninguna foto elegida
                             # acaba mas cerca; la brecha huye con el acopio
                             # encendido (margen +0,097); el flanqueo
                             # equidistante se acepta (la senda no se tasa —
                             # limite declarado, a la reserva). K=3 sobre
                             # K=2,5 por el margen robusto; todos los
                             # anclajes (43 hp1, 39, P1-competencia) aguantan
                             # en ambos (sonda del 48).

ACOPIO_M = 0.18              # [Manel, resello del 48] el valor del barrido
                             # del 46: con el MURO debajo (K=3) el intervalo
                             # imposible se abre — la brecha huye con margen
                             # +0,097 y en calma-con-competencia el botiquin
                             # llama. La historia del sello-en-0 vive en
                             # verifica_46 (registro del 46) y en git.

CUESTA_GANANCIA = 0.4        # [impl] CALIBRADO en verifica_43: el minimo
                             # redondo que hace GANAR al botiquin en el caso
                             # sellado (hp 1) con margen (0,19) y cura tambien
                             # en la banda critica (hp 10); 0,25 ganaba por
                             # 0,06 (fragil) y 0,5 no compra nada mas.
ANT_TECHO = 0.5              # [Manel] techo de F-ANTICIPACION
ANT_HORIZONTE_S = 20.0       # [Manel] horizonte de anticipacion, segundos
ANT_DPS_REF = 24.0           # [impl]  24 HP/s = referencia 1.0
W_TARGET = 3.0               # [Manel] arma + botiquin + racion
# ── F-4 ALCANCE [Manel, 2-sep-2026] ─────────────────────────────────────────
# Duele que un hostil pueda ALCANZARME pronto. Paralela a F1 en forma: anticipa
# lo CIERTO (R1) — la mecanica del mundo, no la intencion ajena.
ALCANCE_TECHO = 0.5          # [Manel] techo 1/2 del eje, como F1
ALCANCE_HORIZONTE_S = 20.0   # [Manel] mismo horizonte que la anticipacion

BOTIN_CAP = 0.25             # [Manel] mitad del techo del miedo
BOTIN_DIST_REF = 24.0        # [impl]  media arena
BOTIN_EXP = 3                # [impl] descuento CUBICO (PROMPT_06 B)
# v3 (PROMPT_06 B): la fila necesita PENDIENTE. El cap 0.25 sigue siendo el
# TECHO [Manel]; lo que baja son los valor_nivel [impl] y el descuento pasa a
# CUBICO, para que el tope muerda solo cerca del premio y no en todo el mapa.
# MEDIDO (tanda runs/tanda3, camara 0.5 + cubico): el tope seguia mordiendo en
# el 47,3 % de las decisiones (mediana) y en 16 de 20 episodios por encima del
# 10 % objetivo. Motivo: con camara 0.5 el tope muerde a menos de 4,95 casillas
# de la camara -- y ahi es justo donde vive el agente cuando migra bien.
# Para que el tope sea TECHO y no punto de trabajo, el valor_nivel mayor tiene
# que quedar por DEBAJO del cap. Se conservan las proporciones sugeridas
# (0.5/0.35/0.25/0.15) escaladas para que el maximo sea 0.24 < 0.25. Asi la
# fila tiene pendiente en TODO el mapa y el cap [Manel] queda como valla.
VALOR_NIVEL = {              # [impl] v3
    "camara": 0.24, "bocas": 0.17, "cajones": 0.12, "bayas": 0.07,
}
B_INICIAL = 0.1              # [impl, vetable] la pareja empieza casi-desconocida
ROCE_VISTA_S = 30.0          # [impl] satura el roce con ~30 s de vista
ROCE_VOZ_FRAC = 0.25         # [impl] la voz vale 1/4 que la vista
VOZ_VENTANA_S = 3.0          # [Manel] ventana de "oida hace poco"
SOLEDAD_RAMPA_S = 30.0       # [impl] llega a su techo tras ~30 s sin compania
SOLEDAD_TECHO = 0.5          # [impl]
# ── LA MEDICINA JUNTO A LA CAMA (sellada por Manel, PROMPT_12) ──────────────
# LA CESION QUE CADUCA [Manel, 2-sep-2026]. Nacida de la escena del botiquin de
# s301: soltamos la cura junto al hermano en critico, nos apartamos, y se fue —
# el botiquin seguia en el suelo 50 tics despues. "No se trata de tirar
# recursos": pasado el plazo, lo ofrecido y no recogido vuelve a ser mio.
# NINGUNA conducta nueva (R2): la recuperacion sale sola de las filas de R y de
# la promesa del objeto, que ya saben llamar a lo que vale.
CESION_CADUCA_S = 30.0       # [Manel]

MEDICINA_DIST = 2.0          # [Manel] cura a distancia <=2 de la pareja
MEDICINA_ATEN = 0.5          # [impl sugerido] atenuacion de S-DANO-PAREJA
# ── EL DUELO QUE SE ATENUA SIN IRSE (sellada por Manel, PROMPT_12) ──────────
DUELO_SUELO = 0.3            # [Manel] nunca baja de 0.3 x B
DUELO_SEMIVIDA_S = 90.0      # [impl] semivida del decaimiento

# ── S-7 PRESION DE AGRESOR ACTIVO (sellada por Manel, PROMPT_09) ────────────
AGRESOR_VENTANA_S = 5.0      # [impl] 120 tics a 24 tps; cada nuevo dano la renueva
AGRESOR_DANO_REF = 50.0      # [Manel, de la formula] dano/50, topado a 0.5
AGRESOR_TECHO = 0.5          # [Manel, de la formula]
AGRESOR_CAP_TOTAL = 0.5      # [impl] la suma sobre varios agresores se topa igual
# ── S-8 EXPOSICION [Manel, sellada — PROMPT_16] ─────────────────────────────
# Sustituye a S-4 APINAMIENTO: duele cuantos hostiles PUEDEN VERME ahora, no
# cuantos hay cerca. Hereda de S-4 el por-hostil y el tope.
EXPO_POR_HOSTIL = 0.3        # [impl, heredado de S-4]
EXPO_CAP = 0.3               # [impl, heredado de S-4]
# Camuflaje: "undetected beyond 4 tiles standing / 7 moving until you attack"
# (README del mundo). CERTIFICADO, no [impl].
CAMO_QUIETO = 4.0
CAMO_MOVIENDO = 7.0
# Cuanto dura el delatarse tras atacar. `CamoRevealTicks` NO esta en la copia
# de la fuente que tenemos: constante [impl] declarada, del lado conservador
# (mas tiempo delatado = mas dolor). Va como INCOGNITA con metodo.
CAMO_REVELADO_S = 5.0        # [impl]
RACION_2A = 0.3              # [Manel] la 2a racion vale 0.3
MOCHILA_W = 0.5              # [impl]
GEAR_MENOR_W = 0.25          # [impl] camuflaje / red
AMMO_REF = 8.0               # [impl] municion de referencia

# repartos (pF, pR, pS), suman 1. Ninguno a cero (regla de la tabla).
REPARTO = {
    "F-DANO":          (0.8, 0.1, 0.1),   # [impl]
    "F-ANTICIPACION":  (0.8, 0.1, 0.1),   # [impl]
    "F-4-ALCANCE":     (0.8, 0.1, 0.1),   # [Manel, 2-sep]
    "R-ACOPIO":        (0.1, 0.8, 0.1),   # [impl] R-dominante, como carencia
    "R-CARENCIA":      (0.15, 0.7, 0.15),  # [impl]
    "R-LLAMADA":       (0.1, 0.8, 0.1),   # [impl]
    "S-SOLEDAD":       (0.1, 0.1, 0.8),   # [Manel]
    "S-DANO-PAREJA":   (0.15, 0.25, 0.6),  # [Manel]
    "S-MUERTE-PAREJA": (0.15, 0.25, 0.6),  # [Manel]
    "S-8-EXPOSICION":  (0.4, 0.1, 0.5),   # [impl, Manel PROMPT_16]
    "S-7-AGRESOR":     (0.5, 0.1, 0.4),   # [impl sugerido por Manel]
}
APETITIVAS = {"R-LLAMADA"}   # la unica fila que tira hacia, no desde

# bandas de hp ajenas: el mundo solo publica la banda (el hp exacto es privado,
# protocol_player.md:76-77). Se estima por el punto medio de cada banda. [impl]
BANDA_EST = {"healthy": 83.0, "hurt": 50.0, "critical": 16.0}


@dataclass
class Memoria:
    """Lo que el traductor recuerda entre decisiones. NO vive en el motor."""
    hp_max: float = 0.0
    roce_B: float = B_INICIAL
    ticks_sin_compania: int = 0
    ultimo_tick_voz_pareja: int = -10 ** 9
    pareja_muerta: bool = False
    tick_muerte_pareja: int = -1      # PROMPT_12: para la pendiente del duelo
    # A.1 CESION (PROMPT_13): lo soltado bajo la condicion de medicina deja de
    # ser mio. (x,y) -> {"item", "tick"}. "Un regalo que sigues contando como
    # tuyo no es un regalo."
    cedidos: dict = field(default_factory=dict)
    # PROMPT_16: para S-8. El camuflaje se cae al atacar, y "quieto" se decide
    # comparando la posicion prevista de un candidato con la REAL de ahora.
    ultimo_ataque: int = -1
    pos_real: tuple = None
    pareja_banda: str = ""            # ultima banda de hp vista de la pareja
    pareja_pos: tuple | None = None
    ultimo_tick: int = -1
    botin_visto: dict = field(default_factory=dict)   # (x,y) -> (nivel, tick)
    objetos_vistos: dict = field(default_factory=dict)  # (x,y) -> (id, n, nivel)
    # S-7: quien me ha danado y cuando. slot -> {"dano": total en ventana,
    # "ultimo": tick del ultimo golpe}. La ventana se RENUEVA con cada dano.
    agresores: dict = field(default_factory=dict)
    fuentes_sin_resolver: int = 0      # honestidad: danos cuyo autor no se pudo casar
    _mundo: object = None
    _fuentes: tuple = ()
    _fuentes_sello: int = -1

    def fuentes(self):
        """Fuentes de botin (posicion, valor_nivel), con cache.

        Fijas del mapa: camara y bocas de la Fortaleza (R1: el mapa del botin es
        cierto). Moviles: cajones y bayas vistos y recordados.
        """
        if self._mundo is None:
            return ()
        # el sello incluye las CESIONES: si una caduca, el objeto vuelve a las
        # fuentes y la cache tiene que enterarse (PROMPT_24).
        sello = (len(self.botin_visto), len(self.cedidos))
        if sello != self._fuentes_sello:
            f = [(p, VALOR_NIVEL["camara"]) for p in self._mundo.camara]
            f += [(p, VALOR_NIVEL["bocas"]) for p in self._mundo.bocas]
            f += [(p, niv) for p, (niv, _t) in self.botin_visto.items()
                  if p not in self.cedidos]
            self._fuentes = tuple(f)
            self._fuentes_sello = sello
        return self._fuentes

    def observa(self, obs: dict, mundo, tick: int):
        """Actualiza la memoria ANTES de valorar. Sin decaimiento (tabla)."""
        self._mundo = mundo
        you = obs.get("you") or {}
        hp = float(you.get("hp") or 0.0)
        self.hp_max = max(self.hp_max, hp)            # [impl] hp_max leido del mundo
        dt = 1 if self.ultimo_tick < 0 else max(0, tick - self.ultimo_tick)
        self.ultimo_tick = tick

        # PROMPT_16: posicion REAL de este tic, contra la que un candidato que
        # mueve se declara "en movimiento" (S-8). El tic del ultimo ataque
        # propio —lo que tira el camuflaje al suelo— lo apunta el decisor en el
        # momento de elegir `atacar_*`, que es cuando se sabe con certeza.
        self.pos_real = tuple(you.get("pos") or ())

        vis = obs.get("visible") or {}
        pareja = None
        for a in vis.get("agents") or []:
            if a.get("slot") == mundo.teammate_slot:
                pareja = a
                break

        # voz de la pareja (canal team certificado en el PROMPT_02)
        for m in obs.get("chat") or []:
            if m.get("from") == mundo.teammate_slot and m.get("channel") == "team":
                self.ultimo_tick_voz_pareja = max(self.ultimo_tick_voz_pareja,
                                                  int(m.get("tick", tick)))

        # muerte de la pareja: evento arena-wide, no depende de la niebla
        for ev in obs.get("events") or []:
            if ev.get("type") == "death_fireworks" and ev.get("slot") == mundo.teammate_slot:
                if not self.pareja_muerta:
                    self.tick_muerte_pareja = tick
                self.pareja_muerta = True

        # ROCE B: crece con presencia mutua; por voz a 1/4 de la tasa. Sin decaimiento.
        tasa_vista = 1.0 / max(1.0, ROCE_VISTA_S * mundo.tick_rate)
        # ARREGLO A (PROMPT_11): el eco de un ping de una pareja YA MUERTA no
        # alimenta el roce. La ventana de voz duraba 3 s sin saber de muertes, asi
        # que tras morir el companero B seguia creciendo ~72 tics con su ultimo
        # ping (medido en gemelos s101, t264-t336). Muerta la pareja, no hay voz.
        oida = (not self.pareja_muerta
                and (tick - self.ultimo_tick_voz_pareja) <= VOZ_VENTANA_S * mundo.tick_rate)
        if pareja is not None:
            self.roce_B = min(1.0, self.roce_B + tasa_vista * dt)
            self.pareja_banda = pareja.get("hp_band") or self.pareja_banda
            self.pareja_pos = tuple(pareja.get("pos") or ()) or self.pareja_pos
            self.ticks_sin_compania = 0
        elif oida:
            self.roce_B = min(1.0, self.roce_B + tasa_vista * ROCE_VOZ_FRAC * dt)
            self.ticks_sin_compania = 0
        else:
            self.ticks_sin_compania += dt

        # ── S-7: quien me esta agrediendo AHORA ─────────────────────────────
        # El mundo publica el autor del dano por su NOMBRE ("P3"), no por slot.
        # Se resuelve leyendo el numero del nombre y COMPROBANDO que casa con un
        # agente visible o ya conocido; lo que no case se cuenta y se declara,
        # en vez de callar (la regla de las tres cegueras).
        vistos = {a.get("slot") for a in (vis.get("agents") or [])}
        for d in (you.get("damage_taken") or []):
            fuente = str(d.get("source") or "")
            cant = float(d.get("amount") or 0.0)
            if cant <= 0 or fuente == "zone":
                continue
            digitos = "".join(ch for ch in fuente if ch.isdigit())
            if not digitos:
                self.fuentes_sin_resolver += 1
                continue
            sl = int(digitos)
            if sl not in vistos and sl not in self.agresores:
                self.fuentes_sin_resolver += 1
            e = self.agresores.setdefault(sl, {"dano": 0.0, "ultimo": tick})
            if tick - e["ultimo"] > AGRESOR_VENTANA_S * mundo.tick_rate:
                e["dano"] = 0.0                 # ventana caducada: se reinicia
            e["dano"] += cant
            e["ultimo"] = tick

        # A.1 CESION: expira si la pareja MUERE o se CURA del todo; entonces el
        # objeto vuelve a ser del mundo (y cogible). PROMPT_24: y expira TAMBIEN
        # por PLAZO — a los CESION_CADUCA_S segundos sin que el herido lo
        # recoja, lo ofrecido vuelve a contar como mio.
        if self.cedidos:
            pj = next((a for a in (vis.get("agents") or [])
                       if a.get("slot") == mundo.teammate_slot), None)
            if self.pareja_muerta or (pj is not None
                                      and (pj.get("hp_band") or "healthy") == "healthy"):
                self.cedidos = {}
            else:
                plazo = CESION_CADUCA_S * mundo.tick_rate
                self.cedidos = {p: e for p, e in self.cedidos.items()
                                if (tick - e["tick"]) < plazo}

        # mapa del botin: lo visto se recuerda (R1 lo permite: el mapa es cierto)
        for it in vis.get("items") or []:
            p = tuple(it.get("pos") or ())
            if p:
                self.botin_visto[p] = (VALOR_NIVEL["cajones"], tick)
                # PROMPT_07 B: se recuerda TAMBIEN que objeto es, para poder
                # apuntar a el como candidato concreto de saqueo.
                self.objetos_vistos[p] = (it.get("id"), int(it.get("n") or 1),
                                          VALOR_NIVEL["cajones"])
        for b in vis.get("bushes") or []:
            p = tuple(b.get("pos") or ())
            if p and (b.get("charges") or 0) > 0:
                self.botin_visto[p] = (VALOR_NIVEL["bayas"], tick)

    def presencia(self, obs, mundo, tick) -> float:
        """P de S-SOLEDAD: 1 a la vista, 0.5 oida hace <3 s, 0 si no.

        ARREGLO A (PROMPT_11): una pareja muerta no se oye. Sin esto, P valia 0.5
        durante ~72 tics despues de su muerte y la rampa de soledad no arrancaba.
        """
        vis = obs.get("visible") or {}
        for a in vis.get("agents") or []:
            if a.get("slot") == mundo.teammate_slot:
                return 1.0
        if self.pareja_muerta:
            return 0.0
        if (tick - self.ultimo_tick_voz_pareja) <= VOZ_VENTANA_S * mundo.tick_rate:
            return 0.5
        return 0.0


# ── RIQUEZA W ────────────────────────────────────────────────────────────────
def riqueza_W(you: dict, mundo) -> tuple:
    """W de la tabla, con saciedad y rendimientos decrecientes. (W, desglose)."""
    d = {}
    mano = you.get("hand") or None
    pack = [s for s in (you.get("pack") or []) if s]
    cuerpo = you.get("body")

    # B (PROMPT_13): ESTAR ARMADO ES TENER EL ARMA EN LA MANO. El mundo ataca
    # con `a.hand` y nada mas (sim.nim:902 `let w = a.hand`); sin arma en mano
    # el ataque cae en `else: discard` — no hay ataque a punos. Un arma en la
    # mochila no es estar armado: antes contaba igual y el animal se quedaba
    # con la red (dano 0) en la mano mientras la espada dormia en el zurron.
    # [impl declarado]
    mejor = 0.0
    for cand, dur in ([(mano.get("id"), mano.get("durability"))] if mano else []):
        it = mundo.items.get(cand)
        if it is None or it.kind not in ("ikMelee", "ikRanged", "ikThrown"):
            continue
        base = min(1.0, it.damage / float(mundo.dmg_ref))
        if it.kind == "ikMelee":
            frac = (float(dur) / it.durability) if (it.durability and dur is not None) else 1.0
            v = base * max(0.0, min(1.0, frac))
        else:
            municion = sum(int(s.get("n") or 0) for s in pack
                           if s.get("id") in mundo.ammo_ids)
            if it.kind == "ikThrown":
                municion = max(municion, int((mano or {}).get("n") or 1))
            v = base * min(1.0, municion / AMMO_REF)
        mejor = max(mejor, v)
    d["arma"] = mejor

    # botiquin: 1 si hay
    d["botiquin"] = 1.0 if any(s.get("id") == mundo.id_botiquin for s in pack) else 0.0

    # raciones: la 1a vale 1; la 2a 0.3 y SOLO con mochila grande
    n_rac = sum(int(s.get("n") or 0) for s in pack if s.get("id") in mundo.id_raciones)
    tiene_mochila = (cuerpo == mundo.id_mochila) if mundo.id_mochila else False
    v = 0.0
    if n_rac >= 1:
        v += 1.0
    if n_rac >= 2 and tiene_mochila:
        v += RACION_2A
    d["raciones"] = v

    # gear menor: camuflaje / red
    g = 0.0
    if mundo.id_camuflaje and cuerpo == mundo.id_camuflaje:
        g += GEAR_MENOR_W
    if mundo.id_red and (
            (mano or {}).get("id") == mundo.id_red
            or any(s.get("id") == mundo.id_red for s in pack)):
        g += GEAR_MENOR_W
    d["gear_menor"] = g

    # mochila: 0.5 [impl]. LECTURA DECLARADA de la linea ambigua de la tabla
    # ("mochila: 0.5 si no la tienes Y hay apetito insatisfecho"): se cuenta como
    # RIQUEZA cuando la LLEVAS y ademas queda apetito por saciar (si no, es peso
    # muerto). Ver acta: interpretacion [impl], vetable.
    apetito = (d["arma"] < 1.0) or (d["botiquin"] < 1.0) or (d["raciones"] < 1.0)
    d["mochila"] = MOCHILA_W if (tiene_mochila and apetito) else 0.0

    return sum(d.values()), d


# ── la tabla ─────────────────────────────────────────────────────────────────
def filas(obs: dict, mundo, mem: Memoria, tick: int) -> dict:
    """Magnitud M de cada fila de la tabla. Sin tocar el motor todavia."""
    you = obs.get("you") or {}
    vis = obs.get("visible") or {}
    pos = tuple(you.get("pos") or (0, 0))
    hp = float(you.get("hp") or 0.0)
    hp_max = mem.hp_max or hp or 1.0
    stats = you.get("stats") or {}
    F = {}

    # ── F-DANO (presente) ────────────────────────────────────────────────────
    # con LA CUESTA DE LA MUERTE (PROMPT_43): convexa bajo el umbral de vida
    u = max(0.0, (hp_max - hp) / hp_max)
    m = u
    if u > CUESTA_UMBRAL_U:
        _f = (u - CUESTA_UMBRAL_U) / (1.0 - CUESTA_UMBRAL_U)
        m = u + CUESTA_GANANCIA * _f * _f
    envenenado = any((e.get("id") or "").startswith("poison")
                     and (e.get("ticks_left") or 0) > 0
                     for e in (you.get("effects") or []))
    if envenenado:
        m *= VENENO_MULT
    F["F-DANO"] = m

    # ── R-ACOPIO (PROMPT_46): sin botiquin en el zurron, malestar de fondo ───
    tiene_cura = any(s2 and s2.get("id") == mundo.id_botiquin
                     for s2 in (you.get("pack") or []))
    F["R-ACOPIO"] = 0.0 if (tiene_cura or you.get("_cura_en_curso")) else ACOPIO_M

    # ── F-ANTICIPACION (solo lo CIERTO: calendario del anillo) ───────────────
    # ¿la casilla ACTUAL quedara fuera de la zona segura al proximo encogimiento?
    # v2 (PROMPT_04 B1): CONTINUA y POR CASILLA. Nada de binarios dentro/fuera.
    #   t_arde = cuando ESA casilla queda fuera de la zona segura, del calendario
    #            completo (mundo.t_arde), incluida la etapa final a radio 0.
    #   M = (dps_de_esa_etapa/24) x 0.5 x max(0, 1 - t_arde/20 s), techo 0.5.
    # Las casillas centrales arden mas tarde => el gradiente NUNCA es plano, ni
    # siquiera en la etapa final. Techo y horizonte [Manel] intactos.
    m = 0.0
    detalle_ant = {}
    ref = mundo.dps_ref()
    peor = None
    for t_burn, dps in mundo.eventos_arde(pos, tick):
        t_arde_s = max(0.0, (t_burn - tick) / float(mundo.tick_rate))
        urgencia = 0.5 * max(0.0, 1.0 - t_arde_s / ANT_HORIZONTE_S)
        mi = min(ANT_TECHO, (dps / ref) * urgencia)
        if mi > m:
            m, peor = mi, (round(t_arde_s, 2), dps)
    if peor is not None:
        detalle_ant = {"dist": round(math.dist(pos, (mundo.arena_size // 2,
                                                     mundo.arena_size // 2)), 2),
                       "t_arde_s": peor[0], "dps": peor[1], "dps_ref": ref}
    # El dano de zona YA EN CURSO NO se suma aqui: la tabla dice que "el goteo
    # entra solo (hp baja)", es decir por F-DANO. Sumarlo tambien aqui seria
    # doble contabilidad y ademas satura el techo 0.5, borrando el gradiente.
    F["F-ANTICIPACION"] = m
    F["_ant"] = detalle_ant

    # ── F-4 ALCANCE (solo lo CIERTO: la mecanica del mundo) ──────────────────
    # "¿En cuantos tics podria plantarse a distancia de golpe, a su mejor
    #  zancada?" — dos cantidades, las dos LEIDAS del mundo:
    #    zancada: `coste_movimiento(stats.max)` = 16 - SPD_max. No conocemos su
    #      SPD; se supone el mas rapido posible. Conservador por diseno.
    #    alcance del golpe: el mayor ALCANCE CUERPO A CUERPO del catalogo.
    #      DESVIACION DECLARADA de la lectura ingenua ("su mejor arma", el arco,
    #      alcance 8): con 8 todo hostil visible ya estaria a distancia de golpe
    #      (nuestro radio de vision es 9-10), la fila saturaria en el techo y el
    #      gradiente seria PLANO — el mismo fallo que el PROMPT_04 arreglo en F1.
    #      Ademas el dato manda: las 59 muertes cazadas del PROMPT_20 ocurrieron
    #      a distancia 1,0, ninguna de lejos. Lo que nos mata es el cuerpo a
    #      cuerpo, y es lo que esta fila anticipa.
    # El PEOR hostil manda (como el peor evento de arde en F1). La PAREJA no
    # duele nunca, viva o muerta. La fila NO crea candidatos (R2): solo duele.
    coste_min = mundo.coste_movimiento(int((mundo.stats_rules or {}).get("max") or 10))
    alcance = max([it.range for it in mundo.items.values()
                   if it.kind == "ikMelee"] or [1])
    m4 = 0.0
    peor4 = None
    for a in vis.get("agents") or []:
        sl = a.get("slot")
        if sl == mundo.slot or sl == mundo.teammate_slot:
            continue
        d = math.dist(pos, tuple(a.get("pos") or (0, 0)))
        pasos = max(0.0, d - alcance)
        t_s = pasos * coste_min / float(mundo.tick_rate)
        mi = ALCANCE_TECHO * max(0.0, 1.0 - t_s / ALCANCE_HORIZONTE_S)
        if mi > m4:
            m4, peor4 = mi, (sl, round(d, 2), round(t_s, 2))
    F["F-4-ALCANCE"] = min(ALCANCE_TECHO, m4)
    F["_alcance"] = {"peor": peor4, "coste_min": coste_min,
                     "alcance_golpe": alcance} if peor4 else {}

    # ── R-CARENCIA ───────────────────────────────────────────────────────────
    W, desglose = riqueza_W(you, mundo)
    F["R-CARENCIA"] = max(0.0, (W_TARGET - W) / W_TARGET)
    F["_W"] = W
    F["_W_desglose"] = desglose

    # ── R-LLAMADA DEL BOTIN CONOCIDO ─────────────────────────────────────────
    mejor, mejor_p, mejor_niv = 0.0, None, ""
    _etq = {v: k for k, v in VALOR_NIVEL.items()}
    for p, niv in mem.fuentes():
        # v2 (PROMPT_04 B2): descuento CUADRATICO. Mismo cap 0.25 [Manel].
        v = niv * max(0.0, 1.0 - math.dist(pos, p) / BOTIN_DIST_REF) ** BOTIN_EXP
        if v > mejor:
            mejor, mejor_p, mejor_niv = v, p, _etq.get(niv, "?")
    F["R-LLAMADA"] = min(BOTIN_CAP, mejor)
    F["_botin"] = {"objetivo": list(mejor_p) if mejor_p else None,
                   "nivel": mejor_niv, "bruto": round(mejor, 4)}

    # ── S-SOLEDAD (no escalada por B: querer compania es constitucional) ──────
    P = mem.presencia(obs, mundo, tick)
    rampa = SOLEDAD_TECHO * min(1.0, mem.ticks_sin_compania /
                                max(1.0, SOLEDAD_RAMPA_S * mundo.tick_rate))
    F["S-SOLEDAD"] = (1.0 - P) * rampa
    F["_P"] = P

    # ── S-DANO-PAREJA / S-MUERTE-PAREJA (escaladas por B) ────────────────────
    # LA FOTO HONESTA (PROMPT_23 A). Estas dos filas dependen del hp del
    # hermano, asi que en la FOTO de un candidato tienen que leer el hp
    # PREVISTO, igual que S-7 ya hacia. El golpe previsto escribe `_hp_est` en
    # el agente objetivo (`decisor_zs._obs_prevista`); si ese objetivo es la
    # pareja, aqui se lee. En la observacion REAL —y en la foto de cualquier
    # candidato que no le pegue— `_hp_est` no existe y todo sigue saliendo de
    # la memoria: el cambio es INERTE fuera de su caso.
    # Alcance minimo: NO se toca ninguna fila que no dependa del hp ajeno, ni
    # se cambia un solo numero sellado.
    B = mem.roce_B
    medicina = None
    _pareja_ag = next((a for a in (vis.get("agents") or [])
                       if a.get("slot") == mundo.teammate_slot), None)
    _hp_prev = _pareja_ag.get("_hp_est") if _pareja_ag else None
    _muerte_prevista = _hp_prev is not None and _hp_prev <= 0.0
    if mem.pareja_muerta or _muerte_prevista:
        F["S-DANO-PAREJA"] = 0.0
        # EL DUELO QUE SE ATENUA SIN IRSE (PROMPT_12): de 1.0xB a un SUELO de
        # 0.3xB [Manel: nunca a cero], con semivida DUELO_SEMIVIDA_S. Razon
        # sellada: una fuerza constante es invisible para el gradiente; la
        # pendiente devuelve al animal a la vida.
        dt = max(0.0, (tick - mem.tick_muerte_pareja) / float(mundo.tick_rate)) \
            if mem.tick_muerte_pareja >= 0 else 0.0
        f = DUELO_SUELO + (1.0 - DUELO_SUELO) * (0.5 ** (dt / DUELO_SEMIVIDA_S))
        F["S-MUERTE-PAREJA"] = f * B
        F["_duelo"] = {"s_desde_muerte": round(dt, 2), "factor": round(f, 5),
                       "prevista": bool(_muerte_prevista and not mem.pareja_muerta)}
    else:
        # el hp PREVISTO manda sobre la banda recordada (ver cabecera del bloque)
        est = _hp_prev if _hp_prev is not None \
            else BANDA_EST.get(mem.pareja_banda, hp_max)
        m_dano = max(0.0, (hp_max - est) / hp_max) * B
        # LA MEDICINA JUNTO A LA CAMA (PROMPT_12): si la pareja esta HERIDA y hay
        # una CURA en el suelo a <=2 casillas de ELLA, la fila se atenua. Todo
        # hechos presentes: su banda de hp y las posiciones visibles. NO se
        # predice que la coja.
        pareja = next((a for a in (vis.get("agents") or [])
                       if a.get("slot") == mundo.teammate_slot), None)
        if pareja is not None and (pareja.get("hp_band") or "healthy") != "healthy":
            ppos = tuple(pareja.get("pos") or ())
            # A.2 ALCANZABILIDAD (PROMPT_13): la cura tiene que estar en casilla
            # que el herido PUEDA pisar: ni la mia ni la de otro. Con esto el
            # gradiente pide el gesto completo: soltar y hacerse a un lado.
            ocupadas = {tuple(pos)}
            for a in (vis.get("agents") or []):
                q = tuple(a.get("pos") or ())
                if q:
                    ocupadas.add(q)
            for it in (vis.get("items") or []):
                itm = mundo.items.get(it.get("id"))
                if itm is None or itm.kind != "ikConsumable" or itm.heal <= 0:
                    continue
                ipos = tuple(it.get("pos") or (99, 99))
                if ipos in ocupadas:
                    continue                      # inalcanzable: hay alguien encima
                if ppos and math.dist(ppos, ipos) <= MEDICINA_DIST:
                    medicina = {"item": it.get("id"), "pos": it.get("pos"),
                                "pareja_pos": list(ppos),
                                "dist": round(math.dist(ppos, ipos), 2)}
                    m_dano *= MEDICINA_ATEN
                    break
        F["S-DANO-PAREJA"] = m_dano
        F["S-MUERTE-PAREJA"] = 0.0
    F["_B"] = B
    F["_medicina"] = medicina
    F["_pareja_banda"] = mem.pareja_banda

    # ── S-8 EXPOSICION (presente, no profecia) ───────────────────────────────
    # Duele quien PUEDE VERME, no quien esta cerca. Tres hechos, todos del
    # mundo y ninguno profetizado:
    #   1. su radio: no publicamos su INT, asi que se usa el MAXIMO posible
    #      leido de `stats.max` del player_config (conservador, [impl]);
    #   2. la linea de vista: muros, rocas y fortaleza cortan
    #      (`protocol_player.md:73`), sobre el `static_map`;
    #   3. mi camuflaje puesto: invisible a mas de 4 quieto / 7 en movimiento
    #      hasta que ataco (README del mundo). Los de DENTRO de ese radio
    #      siguen contando: el camuflaje esconde de lejos, no de cerca.
    # "Quieto" es una propiedad del CANDIDATO: en la observacion prevista de un
    # candidato que mueve, la posicion difiere de la real, y entonces el radio
    # del camuflaje es el de 7. Asi el gradiente distingue esconderse de pasear
    # escondido. Declarado.
    radio = mundo.radio_vision(stats.get("intelligence", 5))
    radio_h = mundo.radio_vision_max()
    cuerpo = you.get("body")
    id_cuerpo = cuerpo.get("id") if isinstance(cuerpo, dict) else cuerpo
    camo = bool(mundo.id_camuflaje) and id_cuerpo == mundo.id_camuflaje
    delatado = (tick - mem.ultimo_ataque) <= CAMO_REVELADO_S * mundo.tick_rate \
        if mem.ultimo_ataque >= 0 else False
    moviendo = mem.pos_real is not None and tuple(pos) != tuple(mem.pos_real)
    tope_camo = (CAMO_MOVIENDO if moviendo else CAMO_QUIETO) \
        if (camo and not delatado) else None

    suma, hostiles, me_ven = 0.0, 0, 0
    for a in vis.get("agents") or []:
        sl = a.get("slot")
        if sl == mundo.slot or sl == mundo.teammate_slot:
            continue
        hostiles += 1
        q = tuple(a.get("pos") or (0, 0))
        dist = math.dist(pos, q)
        if dist > radio_h:
            continue                       # fuera de su alcance de vista
        if tope_camo is not None and dist > tope_camo:
            continue                       # camuflado: no me distingue
        if not mundo.linea_de_vista(q, pos):
            continue                       # roca, muro o fortaleza de por medio
        me_ven += 1
        suma += EXPO_POR_HOSTIL * max(0.0, 1.0 - dist / radio_h)
    F["S-8-EXPOSICION"] = min(EXPO_CAP, suma)
    F["_hostiles"] = hostiles
    F["_me_ven"] = me_ven
    F["_camo"] = {"puesto": camo, "delatado": delatado, "moviendo": moviendo,
                  "tope": tope_camo}
    F["_radio_vision"] = radio
    F["_radio_hostil"] = radio_h

    # ── S-7 PRESION DE AGRESOR ACTIVO ────────────────────────────────────────
    # Quien me ha danado dentro de la ventana y SIGUE A LA VISTA presiona.
    #   M = min(0.5, dano_en_ventana/50) x (hp_del_agresor/hp_max) x (1 - dist/R)
    # El factor de su hp hace que cada golpe de respuesta tenga valor predicho
    # sin profetizar nada: su hp por bandas ES visible. El factor de cercania
    # hace que alejarse tambien alivie. Huir y responder COMPITEN.
    # SIN excepcion para la pareja: si te dana, es agresor.
    presion, detalle_agr = 0.0, []
    for a in vis.get("agents") or []:
        sl = a.get("slot")
        e = mem.agresores.get(sl)
        if sl == mundo.slot or not e:
            continue
        if tick - e["ultimo"] > AGRESOR_VENTANA_S * mundo.tick_rate:
            continue                                   # ventana caducada
        # hp del agresor: el previsto si lo hay (candidato de ataque), si no la banda
        est = a.get("_hp_est")
        if est is None:
            est = BANDA_EST.get(a.get("hp_band"), hp_max)
        f_hp = max(0.0, min(1.0, est / hp_max))
        dist = math.dist(pos, tuple(a.get("pos") or (0, 0)))
        f_cerca = max(0.0, 1.0 - dist / radio)
        # EL MURO (PROMPT_47): convexo a bocajarro, intacto mas alla de D0
        if dist < MURO_D0:
            _on = you.get("_muro_on")
            if _on is None or _on:
                _fr = (MURO_D0 - dist) / MURO_D0
                f_cerca *= 1.0 + MURO_K * _fr * _fr
        mi = min(AGRESOR_TECHO, e["dano"] / AGRESOR_DANO_REF) * f_hp * f_cerca
        presion += mi
        detalle_agr.append({"slot": sl, "dano_ventana": round(e["dano"], 1),
                            "hp_est": round(est, 1), "dist": round(dist, 2),
                            "M": round(mi, 5)})
    F["S-7-AGRESOR"] = min(AGRESOR_CAP_TOTAL, presion)
    F["_agresores"] = detalle_agr
    return F


def appraise(obs: dict, mundo, mem: Memoria, tick: int) -> tuple:
    """Observacion -> (State del motor, radiografia). El contrato de machina."""
    F = filas(obs, mundo, mem, tick)
    pF = nF = pR = nR = pS = nS = 0.0
    radiografia = {"filas": {}, "W": F["_W"], "W_desglose": F["_W_desglose"],
                   "B": F["_B"], "P": F["_P"], "hostiles": F["_hostiles"],
                   "anticipacion": F["_ant"], "botin": F["_botin"],
                   "pareja_banda": F["_pareja_banda"],
                   "agresores": F["_agresores"],
                   "medicina": F.get("_medicina"), "duelo": F.get("_duelo")}
    for nombre, (fF, fR, fS) in REPARTO.items():
        M = float(F.get(nombre) or 0.0)
        if M <= 0.0:
            radiografia["filas"][nombre] = {"M": 0.0}
            continue
        aF, aR, aS = M * fF, M * fR, M * fS
        if nombre in APETITIVAS:
            pF += aF; pR += aR; pS += aS
        else:
            nF += aF; nR += aR; nS += aS
        radiografia["filas"][nombre] = {
            "M": round(M, 5), "signo": "+" if nombre in APETITIVAS else "-",
            "F": round(aF, 5), "R": round(aR, 5), "S": round(aS, 5)}

    st = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
    radiografia["fuerzas_crudas"] = {"pF": round(pF, 5), "nF": round(nF, 5),
                                     "pR": round(pR, 5), "nR": round(nR, 5),
                                     "pS": round(pS, 5), "nS": round(nS, 5)}
    # el State aplica el minimo basal y el techo de volumen de model.py
    radiografia["fuerzas_state"] = {"pF": round(st.pF, 5), "nF": round(st.nF, 5),
                                    "pR": round(st.pR, 5), "nR": round(st.nR, 5),
                                    "pS": round(st.pS, 5), "nS": round(st.nS, 5)}
    return st, radiografia


def _proximo_encogimiento(mundo, tick):
    """(tick_LIMITE, radio_final, dps) de la etapa en curso. None si no hay.

    El tick limite es `done`: el instante en que el radio TERMINA de cerrar sobre
    r1. Es el plazo real para estar dentro. (Usar `shrink`, el instante en que
    EMPIEZA, agota t_restante a mitad del encogimiento y satura D(t) cuando ya
    no hay nada que hacer.) [impl declarado en el acta]
    """
    for (warn, shrink, done, r0, r1, dps) in mundo.zone_schedule:
        if tick < done:
            return (done, float(r1), float(dps))
    return None

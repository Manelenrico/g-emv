"""[P8] EL CUERPO DEL SIETE EN EL VALLE (fase 1: solo el cuerpo, sin razón, sin emociones nuevas), más el hambre y el cansancio.
La traducción vive aquí; el valle (valle/) no sabe nada de ella. No se toca motor/model.py ni ningún archivo congelado: se IMPORTA del siete
lo que no depende del mundo (el motor, el reparto y el signo de cada fila, sus constantes, el desempate, el cuaderno, la calma de la curiosidad,
la lista de filas del miedo) y se escribe aquí lo del valle (la percepción, la memoria del día, las filas leídas en el valle, la foto imaginada
de cada candidato, las llamadas).

Una decisión por turno: candidatos = las acciones válidas del valle (sin empujar, golpear, hablar ni llamar); para cada uno, la foto (lo que
imagina el cuerpo que pasará) → filas → State del motor → d = opponent_distance; gana la d mínima (select_tiebreak del siete).
Las llamadas no se deciden: salen cuando un sentimiento cruza su umbral (una vez; se rearma cuando baja). Ver config_cuerpo_valle.json."""
import json, math, os, sys
from array import array
_PASOS = {}          # (prompt 30) la tabla de pasos del mapa (estático), por casilla de destino
from collections import deque, OrderedDict
_DIST = OrderedDict()   # (prompt 67) las distancias andando hasta cada meta, compartidas por las criaturas del proceso (por mapa y meta; las 512 últimas)

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
for p in (RAIZ, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "paintball", "alma"), os.path.join(RAIZ, "planificador"),
          os.path.join(RAIZ, "cantera", "paper7"), os.path.join(RAIZ, "cantera", "paper6"), os.path.join(RAIZ, "valle")):
    if p not in sys.path: sys.path.insert(0, p)
from motor.model import State, opponent_distance, DEFAULT_CONFIG          # el motor, intocable
from motor.model import TEN_BASAL_MIN, VOL_MAX                             # (rama valle-sin-techo) sus constantes, importadas
from alma import appraisal_zs_v42_exp as A                                  # la tabla congelada: REPARTO, APETITIVAS y las constantes de cada fila
import planificador_v1 as PL                                                # select_tiebreak
import cuaderno_P7 as CU                                                    # el cuaderno del siete
import descubre_P7 as X                                                     # calma de la curiosidad, su reparto y sus constantes
import miedo_P7_49 as MI                                                    # FILAS_MIEDO
from jugadores import Mapa                                                  # caminos más cortos por el mapa público del valle (sin saber nada del cuerpo)

CFG = json.load(open(os.path.join(AQUI, "config_cuerpo_valle.json"), encoding="utf-8"))
T = CFG["tiempos_turnos"]
MUNDO_CFG = json.load(open(os.path.join(os.path.dirname(os.path.dirname(AQUI)), "valle", "config_valle.json"), encoding="utf-8"))      # (prompt 64) lo público del mundo que se ve de las demás: los cortes de sus niveles
import nace_P7_29 as N29                                                    # la fila de la curiosidad del cuánto (su nombre)
sys.path.insert(0, os.path.join(RAIZ, "cantera", "paper5"))
import curiosidad as C5                                                     # (prompt 12) R-CURIOSIDAD-FRONTERA del cinco: su reparto, su caída, su balanza
REPARTO = dict(A.REPARTO); REPARTO["R-CURIOSIDAD"] = X.REPARTO_CUR; REPARTO[N29.FILA_CUANTO] = X.REPARTO_CUR   # como las ponen descubre_P7:289 y nace_P7_29:189
REPARTO[C5.FILA_FRONT] = C5.REPARTO_CUR                                     # dolor (no apetitiva), como la monta curiosidad.py:386-393
CUR5 = CFG["curiosidad_frontera"]; K_FRONT = float(CUR5["k"])
for k, v in CFG["filas_nuevas"].items():
    if not k.startswith("_"): REPARTO[k] = tuple(v)
APETITIVAS = set(A.APETITIVAS)
# (prompt 34, Manel) «dos platos»: filas que alimentan los platos de ganar del motor, en la tabla propia de la criatura (no en model.py ni en la del siete).
# Cada una con el reparto de las filas de su eje (config_cuerpo_valle.json → filas_nuevas); solo salen con el interruptor `dos_platos`
APETITIVAS |= set(CFG.get("filas_de_ganancia") or [])                       # (los repartos, en filas_nuevas como las demás)
DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "O": (-1, 0)}


def cuesta(u):
    """la cuesta de F-DANO del siete (A:865-869), sobre u en [0, 1]"""
    u = max(0.0, u); m = u
    if u > A.CUESTA_UMBRAL_U:
        f = (u - A.CUESTA_UMBRAL_U) / (1.0 - A.CUESTA_UMBRAL_U); m = u + A.CUESTA_GANANCIA * f * f
    return m


def es_bestia(x):
    """(prompt 90, Manel) cualquier bestia, se llame como se llame («bestia», «bestia2»…)"""
    return isinstance(x, str) and x.startswith("bestia")


COSTUMBRES = ("casa", "huerto", "bosque", "salvaje", "almacen", "hacia_mi", "hacia_bestia", "lejos_bestia", "quieta")

def situacion_de(flaca, herida, bestia_cerca, fase, llamada):
    """(prompt 90, pieza I) la situación de la otra que se ve desde fuera: flaca, herida, la bestia cerca de ella, la hora (día, anochecer, noche), la han llamado"""
    return f"{int(bool(flaca))}{int(bool(herida))}{int(bool(bestia_cerca))}|{'noche' if fase == 'noche' else ('anochecer' if fase == 'anochecer' else 'dia')}|{int(bool(llamada))}"

def clase_paso(M, casa_celdas, antes, ahora, yo=None, bestia=None):
    """(prompt 90, pieza I) adónde va, por un paso visto (de `antes` a `ahora`): quieta; hacia la bestia (se acerca a ella y queda a dos o menos) o lejos de
    ella (se aleja con la bestia a cinco o menos); si no, el sitio al que más se acerca (andando, el más cercano de los que se acercan): su casa, el huerto,
    el bosque, la zona salvaje, el almacén, o hacia mí. None si no se acerca a nada"""
    antes, ahora = tuple(antes), tuple(ahora)
    if antes == ahora: return "quieta"
    ch = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    if bestia is not None:
        b = tuple(bestia)
        if ch(ahora, b) < ch(antes, b) and ch(ahora, b) <= 2: return "hacia_bestia"
        if ch(ahora, b) > ch(antes, b) and ch(antes, b) <= 5: return "lejos_bestia"
    mejor = None
    for k, metas in (("casa", sorted(casa_celdas)), ("huerto", M.plantas), ("bosque", M.bosque), ("salvaje", M.salvaje), ("almacen", M.acceso_almacen)):
        D = M.distancias(metas); d0, d1 = D.get(antes, 10 ** 9), D.get(ahora, 10 ** 9)
        if d1 < d0 and (mejor is None or d1 < mejor[0]): mejor = (d1, k)
    if yo is not None:
        y = tuple(yo)
        if ch(ahora, y) < ch(antes, y) and (mejor is None or ch(ahora, y) < mejor[0]): mejor = (ch(ahora, y), "hacia_mi")
    return mejor[1] if mejor else None


def duelo(dt, semivida, B):
    """S-MUERTE-PAREJA del siete (A:1115-1126): de 1 · B hacia el suelo DUELO_SUELO · B, con su semivida (en las unidades de dt)"""
    return (A.DUELO_SUELO + (1.0 - A.DUELO_SUELO) * 0.5 ** (dt / semivida)) * B


SEIS = ("placer", "displacer", "alegria", "enfado", "amor", "tristeza")


class RepartoFractal:
    """(prompt 103, Manel: el fractal) el reparto de cada fila con el mismo número que ya usa el cuerpo: a su dimensión, la mayor parte de F-HAMBRE (0,8), y a
    cada una de las otras dos, la menor (0,1); leído de REPARTO["F-HAMBRE"], no copiado. «Su dimensión»: la que dice el nombre si acaba en -CUERPO, -RECURSOS o
    -VINCULO; si no, la de mayor parte en el reparto de hoy (en empate, la de la letra del nombre: F cuerpo, R recursos, S vínculo). Las filas que se dan de
    alta al vuelo (V-, G-, S-DUELO-…) se transforman al leerlas. Solo lectura: la tabla del siete (REPARTO) no cambia"""
    SUF = {"-CUERPO": 0, "-RECURSOS": 1, "-VINCULO": 2}
    def __init__(self, base):
        self.base = base; self._c = {}; self._n = -1
        b = base["F-HAMBRE"]; self.alto, self.bajo = max(b), min(b)
    def dim(self, k, r):
        for s, i in self.SUF.items():
            if k.endswith(s): return i
        m = max(r); top = [i for i in range(3) if r[i] == m]
        if len(top) == 1: return top[0]
        letra = {"F": 0, "R": 1, "S": 2}.get((k[2:] if k.startswith("G-") else k)[:1])
        return letra if letra in top else top[0]
    def _al_dia(self):
        if self._n != len(self.base):
            self._c = {}
            for k, r in self.base.items():
                i = self.dim(k, r); self._c[k] = tuple(self.alto if j == i else self.bajo for j in range(3))
            self._n = len(self.base)
    def items(self): self._al_dia(); return self._c.items()
    def __getitem__(self, k): self._al_dia(); return self._c[k]
    def get(self, k, d=None): self._al_dia(); return self._c.get(k, d)


def seis(F, rep=None):
    """(prompt 32) las seis fuerzas del motor tal como las suma compone (A:1671-1706), sin restar: cuerpo (placer pF, displacer nF), recursos (alegría pR,
    enfado nR), vínculo (amor pS, tristeza nS). Son las sumas antes de que State les ponga el mínimo basal y el techo (que no cambian cuál es la mayor).
    (prompt 103) `rep`: otro reparto (el fractal); sin él, REPARTO"""
    v = dict.fromkeys(SEIS, 0.0)
    for nombre, (fF, fR, fS) in (rep or REPARTO).items():
        M = float(F.get(nombre) or 0.0)
        if M <= 0.0: continue
        if nombre in APETITIVAS: v["placer"] += M * fF; v["alegria"] += M * fR; v["amor"] += M * fS
        else: v["displacer"] += M * fF; v["enfado"] += M * fR; v["tristeza"] += M * fS
    return v


def compone_sumas(F, rep=None):
    """(prompt 67) el valorador de sumas, el control: las mismas filas y el mismo reparto de cada fila (la tabla del siete) que `compone`, pero sin el motor
    (sin State: ni mínimo de tensión ni techo; sin opponent_distance: ni posición, ni tensión, ni acoplamiento; sin metas): cada dimensión vale lo que gana
    menos lo que pierde, y la foto vale la suma de las tres, con el mismo peso. Devuelve las seis sumas (como atributos pF … nS) y la «d» = − esa suma, para
    que la menor d sea la suma mayor y el resto de la criatura (empate exacto, llamadas) no cambie"""
    from types import SimpleNamespace
    pF = nF = pR = nR = pS = nS = 0.0
    for nombre, (fF, fR, fS) in (rep or REPARTO).items():
        M = float(F.get(nombre) or 0.0)
        if M <= 0.0: continue
        if nombre in APETITIVAS: pF += M * fF; pR += M * fR; pS += M * fS
        else: nF += M * fF; nR += M * fR; nS += M * fS
    return SimpleNamespace(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS), -((pF - nF) + (pR - nR) + (pS - nS))


def compone_posicion(F, satura=False, rep=None):
    """(prompt 72) el valorador de posición, P32: las mismas filas, el mismo reparto y la misma saturación de las ganancias que `compone`, y la distancia del
    motor con solo su término de posición: por dimensión, (ganancia − pérdida − su meta)² con su peso de posición (metas y pesos de DEFAULT_CONFIG,
    importados); sin tensión, sin techo ni mínimo basal (no tocan la posición) y sin acoplamiento. Devuelve, como `compone_sumas`, las seis sumas crudas
    (para la voz, la interrupción y el contagio, como en S32) y la «d»"""
    st, _ = compone_sumas(F, rep)
    pF, nF, pR, nR, pS, nS = st.pF, st.nF, st.pR, st.nR, st.pS, st.nS
    if satura:
        pF = min(pF, nF + DEFAULT_CONFIG.f_pos_target); pR = min(pR, nR + DEFAULT_CONFIG.r_pos_target); pS = min(pS, nS + DEFAULT_CONFIG.s_pos_target)
    C = DEFAULT_CONFIG
    d2 = C.w_f_pos * (pF - nF - C.f_pos_target) ** 2 + C.w_r_pos * (pR - nR - C.r_pos_target) ** 2 + C.w_s_pos * (pS - nS - C.s_pos_target) ** 2
    return st, math.sqrt(d2)


def soledad(P, sin_compania, rampa):
    """S-SOLEDAD del siete (A:1092-1097)"""
    return (1.0 - P) * A.SOLEDAD_TECHO * min(1.0, sin_compania / max(1.0, rampa))


def estado_sin_techo(pF, nF, pR, nR, pS, nS):
    """(rama valle-sin-techo, prompt 49, experimento) el State del motor con su mínimo basal pero sin reescalar el excedente cuando la suma pasa del techo de
    volumen. Por debajo del techo es exactamente el State del motor. El mínimo basal se hace como lo hace el motor (State.__post_init__, paso 1), con su constante"""
    st = State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)
    if st.pF + st.nF + st.pR + st.nR + st.pS + st.nS < VOL_MAX - 1e-12: return st      # no tocó el techo: el del motor, tal cual
    st = State.__new__(State)
    for k, v in (("pF", pF), ("nF", nF), ("pR", pR), ("nR", nR), ("pS", pS), ("nS", nS)): setattr(st, k, v)
    for p_attr, n_attr in (("pF", "nF"), ("pR", "nR"), ("pS", "nS")):
        fp, fn = getattr(st, p_attr), getattr(st, n_attr)
        if fp + fn < TEN_BASAL_MIN: add = (TEN_BASAL_MIN - fp - fn) / 2; setattr(st, p_attr, fp + add); setattr(st, n_attr, fn + add)
    return st


def comprueba_sin_techo(n=500, semilla=4950):
    """(prompt 50, Manel) comprobación automática: por debajo de suma 8 (el techo de volumen), la distancia de una foto sin el reescalado tiene que salir
    idéntica a la que da model.py (su State y su opponent_distance, importados). Estados al azar (con semilla fija), incluidos casi en el techo y con ejes por
    debajo del mínimo basal. Si un día no coincide, falla (AssertionError) y no deja usar la criatura"""
    import random
    rng = random.Random(semilla); malos = []
    for i in range(n):
        tope = rng.choice((0.05, 0.5, 3.0, 7.0, 7.99))
        v = [rng.random() for _ in range(6)]; s_ = sum(v) or 1.0; v = [x / s_ * tope * rng.uniform(0.2, 1.0) for x in v]
        if i % 7 == 0: v[rng.randrange(6)] = 0.0
        st_m = State(*v)
        if st_m.pF + st_m.nF + st_m.pR + st_m.nR + st_m.pS + st_m.nS >= VOL_MAX: continue
        d_m = opponent_distance(st_m, DEFAULT_CONFIG); d_s = opponent_distance(estado_sin_techo(*v), DEFAULT_CONFIG)
        if d_m != d_s: malos.append((v, d_m, d_s))
    assert not malos, f"sin_techo: por debajo del techo la distancia no coincide con model.py en {len(malos)} casos, p.ej. {malos[0]}"
    return n


comprueba_sin_techo()                                                       # (prompt 50) al cargar la criatura: si no coincide, no arranca


def compone(F, satura=False, sin_techo=False, rep=None):
    """filas → State → d, igual que appraise del siete (A:1671-1706): cada fila con M > 0 suma M × reparto al lado que toca.
    (prompt 46, Manel) con `satura`: la ganancia de cada eje se satura en la meta de su eje (las de DEFAULT_CONFIG, importadas): ganar acerca la posición
    a la meta y ahí se para, no la pasa (ganancia ≤ pérdida + meta). (prompt 103) `rep`: otro reparto (el fractal); sin él, REPARTO"""
    pF = nF = pR = nR = pS = nS = 0.0
    for nombre, (fF, fR, fS) in (rep or REPARTO).items():
        M = float(F.get(nombre) or 0.0)
        if M <= 0.0: continue
        if nombre in APETITIVAS: pF += M * fF; pR += M * fR; pS += M * fS
        else: nF += M * fF; nR += M * fR; nS += M * fS
    if satura:
        pF = min(pF, nF + DEFAULT_CONFIG.f_pos_target); pR = min(pR, nR + DEFAULT_CONFIG.r_pos_target); pS = min(pS, nS + DEFAULT_CONFIG.s_pos_target)
    st = estado_sin_techo(pF, nF, pR, nR, pS, nS) if sin_techo else State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS, nS=nS)     # (rama valle-sin-techo) comparar antes del reescalado
    return st, opponent_distance(st, DEFAULT_CONFIG)


class Criatura:
    def __init__(self, agente, mapa_publico, cultura=None, anticipa=False, comer_luego=False, riqueza_valle=False, robo_noche=False, comer_al_final=False, promesa_una=False, matorrales=False, plantas=False, recuerdo_vacio=False, histeresis_llamadas=False, compromiso=False, dormir_en_casa=False, cansancio_suelta=False, dar_comida=False, responde_llamadas=False, comida_sin_hambre=False, comida_sobra=False, sabe_reglas_trabajo=False, enfado=False, comida_por_dia=False, vecinas=False, comida_sin_hermana=False, distancias=False, oye_sin_hermana=False, duelo_v19=False, duelo_para=False, atencion_huida=False, dos_platos=False, platos_v23=False, sentir=False, hambre_dolor=False, platos_v24=False, regla_general=False, rg_ganancias=True, memoria_v2=False, memoria_v3=False, cinco_matorrales=False, rondas=False, escala_v6=False, aprende_v7=False, simetria_v7=False, simetria_vista_v8=False, satura_v8=False, ve_vida_v9=False, sin_techo_v11=False, duelo_suma_v15=False, compromiso_opcion_v15=False, compromiso_margen=None, voz_v16=False, frio_sabe_v17=False, compromiso_emocion_v18=False, noche_entera_v18=False, llamadas_opcion_v19=False, llamadas_contraste_v20=False, alarma_zona_v20=False, cultura_sin_olvido_v22=False, medicina_herida_v22=False, provision_necesidad_v22=False, cuenta_despensa_v23=False, empates_sigue_v23=False, dar_cura_v24=False, empate_margen_v24=None, contagio_vecinas_v25=False, aprender_mirando_v26=False, reloj_dentro_v27=False, juntar_viejos_v27=False, rapido_v28=False, sumas_v29=False, posicion_v30=False, para_que_v31=False, gravedad_v31=False, radar_v34=False, radar_c_v34=True, radar_d_v34=True, radar_honesto_v35=False, radar_v36=False, radar_c_factor=1.0, radar_v38=False, radar_v39=False, sabores_v40=False, hechos_v40=False, acompanar_v41=False, sabores_v42=False, empate_suertes_v42=False, semilla_partida=None, sabores_v43=False, bestia_v44=False, imagina_v45=False, duelo_v45=False, noches_v47=False, robos_v47=False, empate_quedarse_v47=False, prop_real_v47=False, prop_ctx_v48=False, clase_v49=False, noche_perdida_v49=False, robos_v49=False, gusto_hambre_v49=False, horizonte_v50=False, arbol_v50=False, dulce_v51=False, casa_v51=False, fractal_v51=False, dar_v52=False, dar_v53=False, tope_dar_off=False, dar_v54=False, gesto_comida_v56=False, devolver_v57=False, cuesta_medicina_v57=False, devolver_v58=False, devolver_solo_gesto_v59=False, devolver_necesidad_v60=False, robo_regalo_v61=False, robo_trato_v61=False, quitar_espejo_v61=False, voz_off_v62=False, voz_sin_aqui_estoy_v63=False, voz_sin_comida_v63=False, voz_sin_bestia_v63=False, voz_sin_ven_v63=False, cara_v64=False, voz_v64=False, aprender_cara_v64=False, para_v64=False, cara_dar_v65=False, ya_tiene_v67=False, dormida_sin_voz_v67=False, voz_piezas_v68=""):
        self.a = agente; self.casa = agente[0]; self.hermana = agente[0] + ("2" if agente[1] == "1" else "1")
        self.miedo = CFG["miedo"]["valiente"] if agente[1] == "1" else CFG["miedo"]["prudente"]
        self.mp = mapa_publico; self.M = Mapa(mapa_publico); self.reglas = mapa_publico.get("reglas_publicas") or {}
        self.casa_celdas = {tuple(c) for c in mapa_publico["casas"][self.casa]["celdas"]}
        self.mi_puerta = tuple(mapa_publico["casas"][self.casa]["puerta"]); self.puertas = {tuple(v["puerta"]) for v in mapa_publico["casas"].values()}      # (prompt 103)
        self.todas_casas = {tuple(c) for v in mapa_publico["casas"].values() for c in v["celdas"]}
        self.almacen = [tuple(c) for c in mapa_publico["almacen"]]; self.botiquin = CFG["objeto_del_botiquin"]
        E = CFG["escala_cuerpo"]; self.vida_max, self.hambre_max, self.cans_max = E["vida"], E["hambre"], E["cansancio"]
        # el cuaderno: nace sabiendo que la comida quita el hambre (un recuerdo «al menos»); lo demás, sin saber
        self.cuaderno = CU.Cuaderno(agente)
        # memoria del día (lo que el siete guarda en Memoria)
        self.B = A.B_INICIAL; self.sin_compania = 0; self.ultimo_voz = -10 ** 9
        self.pareja_muerta = False; self.turno_saber_muerte = None; self.pareja_pos = None; self.pareja_herida = False; self.pareja_lleva = []
        self.agresor_bestia = {"ultimo": -10 ** 9, "dano": 0.0, "acum": 0.0}; self.dist_bestia = []
        self.fuentes = {}; self.almacen_visto = None; self.despensa_vista = 0
        self.prop = {}; self.prev = None; self.armada = {k: True for k in CFG["llamadas"]["orden"]}; self.cola = []
        self._dist_cache = OrderedDict(); self.ultima = {}
        # (prompt 12) la frontera del cinco: las casillas vistas, la distancia de cada casilla a lo no visto, y la vida perdida reciente (la balanza)
        self.W, self.H = mapa_publico["ancho"], mapa_publico["alto"]; Tm = mapa_publico["terreno"]
        self.n_arena = sum(1 for y in range(len(Tm)) for x in range(len(Tm[0])) if Tm[y][x] != "x")      # todas las casillas del valle (sin el borde «fuera»), muros incluidos
        self.pisables = [(x, y) for y in range(len(Tm)) for x in range(len(Tm[0])) if Tm[y][x] not in ("m", "p", "x")]
        self.vistas = set(); self._front = {}; self._front_n = -1; self.vida_hist = deque(maxlen=CUR5["ventana_dano_turnos"] + 1); self.amenaza5 = (0.0, {})
        # (prompt 14) la cultura y la anticipación (plan_cultura_v1.md). Sin cultura y sin anticipación, el cuerpo es el de la v2 (se escribe en el
        # cuaderno lo vivido de los sitios, pero no se lee: la puerta de igualdad lo comprueba)
        self.ley = mapa_publico["leyenda"]; self.T = Tm; self.anticipa = bool(anticipa); self.cultura = None
        self.comer_luego = bool(comer_luego)
        # (prompt 16, Manel) el objetivo de riqueza del valle en comidas (objetivo_riqueza.py) en lugar de W_TARGET del siete; y el robo de la bolsa de noche
        # como pérdida de recursos de la noche fuera, que suma al peso de la anticipación (con techo 1)
        self.WT = float(CFG["riqueza_objetivo"]["valor"]) if riqueza_valle else A.W_TARGET; self.robo_noche = bool(robo_noche)
        # (prompt 17, Manel) la foto de cada candidato que no es comer, si acaba llevando comida, imagina también comer al final de la mirada («X y después
        # comer»; se queda con la mejor de las dos); y la promesa de coger comida no cuenta en una foto donde ya come (ni se come al final lo ya prometido)
        self.comer_al_final = bool(comer_al_final); self.promesa_una = bool(promesa_una)
        # (prompt 19, Manel) v7: los matorrales que ha visto (dónde están lo aprende viviendo), lo vivido de cada visita al cuaderno («matorral» · zona: si tenía fruto),
        # e ir a un matorral recordado o adonde el cuaderno dice que hay matorrales promete una comida por la probabilidad de encontrar fruto en la mirada
        self.v7 = bool(matorrales); self.mat = {}; self._mat_vista = set(); self._mat_apunte = {}
        # (prompt 21, Manel) las plantas del huerto se recuerdan como matorrales (solo dónde hay fruto, no el trabajo); y lo visto vacío hace poco no promete:
        # la probabilidad sube con el tiempo desde que lo vio vacío, al ritmo de lo que tarda en volver a tener fruto según su propio recuerdo
        self.plantas_mat = bool(plantas); self.recuerdo_vacio = bool(recuerdo_vacio); self.vueltas = []
        # (prompt 22) la histéresis de las llamadas; el compromiso con el destino elegido (como la forma del paper cinco); y dormir en casa (la cultura)
        # (prompt 23) el cansancio por encima del umbral suelta el compromiso siempre; y ayudar a la hermana con comida (como con la medicina)
        self.cansancio_suelta = bool(cansancio_suelta); self.dar_comida = bool(dar_comida); self.pareja_flaca = False
        # (prompt 24, Manel) responder a las llamadas de la hermana, pesado por el vínculo: «peligro» (miedo a ese sitio; de noche, a casa), «aquí hay comida»
        # (un sitio con comida, más fiable cuanto más cerca), «necesito ayuda» / «estoy herida» (ir hacia ella). Cada llamada vale lo que la mirada (44 turnos)
        self.comida_sin_hambre = bool(comida_sin_hambre)
        # (prompt 26) «aquí hay comida» solo si ve más comida de la que se va a comer (las comidas que su hambre aguanta sin desperdiciar), y una vez por sitio
        # (el sitio vuelve a contar cuando lo ve vacío)
        self.sabe_reglas_trabajo = bool(sabe_reglas_trabajo)
        # (prompt 27, Manel) el enfado: lo robado tira de ella mientras la bestia lo lleva (R-ENFADO); puede empujar a la bestia (solo a la bestia); a la hermana
        # le llega si ve el robo o si oye «necesito ayuda» con la bestia a la vista, pesado por el vínculo. Choca con el miedo: la bestia cuenta como dos (regla pública)
        self.enfado_on = bool(enfado); self.enfado = None; self._bestia_vista_t = -10 ** 9; self._lleva_her_prev = []; self.robada_t = -10 ** 9
        self.comida_por_dia = bool(comida_por_dia); self._dia_sitios = None
        # (prompt 28, Manel) las vecinas: el vínculo por escalones fijos (hermana > comunidad > otros), cada uno con su suelo y su techo; dentro, sube con el
        # cuidado (verla, darle, recibir de ella) y baja sin él hacia el suelo. Todo lo que ya pesaba con el vínculo se extiende a las vecinas
        # (prompt 30, Manel) las distancias unificadas: tablero (Chebyshev) para «pegada» y «a la vista»; pasos de verdad para «cuánto me cuesta llegar»
        self.dist_u = bool(distancias)
        self.oye_sin_her = bool(oye_sin_hermana)
        # (prompt 31, Manel) la tristeza del 24 de octubre con piezas que ya hay: duelo también por una vecina (más corto), la compañía de las suyas lo alivia,
        # «estoy de duelo» es una llamada, y quien la oye siente su dolor como siente a la herida (por el vínculo) y va hacia ella
        self.duelo_v19 = bool(duelo_v19); self.muertas = {}; self.her_duelo = None
        if self.duelo_v19: self.armada["estoy_de_duelo"] = True
        # (prompt 32, Manel) primero pararse: con el duelo reciente pesa menos todo lo que es ir a por cosas; el miedo, comer y ir hacia las suyas no se tocan
        self.duelo_para = bool(duelo_para) and self.duelo_v19
        # (prompt 34, Manel) los platos de ganar del motor: calor y gusto de comer, conseguir, estar con las suyas y dar. True: los tres; o una lista de platos
        # (añadido de Manel al prompt 34: un interruptor por plato) entre «cuerpo» (F-FRIO, P-CALOR, P-COMER), «recursos» (R-CONSEGUIR) y «vinculo» (S-JUNTAS, S-DAR)
        self.platos_on = {"cuerpo", "recursos", "vinculo"} if dos_platos is True else set(dos_platos or [])
        self.dos_platos = bool(self.platos_on)
        # (prompt 35, Manel) «conseguir» solo lo nuevo; el frío incómodo, no doloroso; sin gusto de comer harta
        self.platos_v23 = bool(platos_v23)
        # (prompt 35, Manel) la ganancia se siente en el momento (al conseguir algo nuevo, al comer, al recibir y al dar), entra en el estado y se va apagando
        # (prompt 36, Manel) el hambre es dolor: con hambre alta duele cada vez más deprisa; y cada ganancia, con su sentido de supervivencia (platos_v24)
        self.hambre_dolor = bool(hambre_dolor); self.platos_v24 = bool(platos_v24)
        # (prompt 39, Manel) la criatura de regla general: lo que algo vale = lo que necesita ahora × lo que sirve, repartido entre cuerpo, recursos y vínculo;
        # con o sin el lado de ganar (rg_ganancias). Sin las piezas hechas para una conducta (ver `_filas_rg`)
        self.rg = bool(regla_general); self.rg_gan = bool(rg_ganancias); self._F_ahora = (None, None)
        # (prompt 40, Manel) la memoria de los matorrales arreglada: verlo vacío otra vez renueva cuándo lo vio vacío; y lo que espera de cada uno sale solo del
        # tiempo desde que lo vio (vacío o con fruto) y de lo que ha aprendido que tarda en volver a dar fruto (la cultura parte de un día; lo vivido lo corrige)
        self.memoria_v2 = bool(memoria_v2)
        # (prompt 41, Manel) «puede haber fruto»: lo que espera de un matorral es la frecuencia con que lo ha encontrado con fruto según el tiempo desde que lo vio
        # (vacío o con fruto), por tramos; cada tramo parte de lo que dice la cultura de los matorrales, con el peso neutro del cuaderno. Y, al decidir adónde
        # ir, compara los cinco matorrales o plantas que más prometen por lo que cuesta llegar, no uno solo
        self.memoria_v3 = bool(memoria_v3); self.cinco = bool(cinco_matorrales); self.frec = {}
        self.rondas = bool(rondas)          # (prompt 43, Manel) poder imaginar una ronda: dos o tres matorrales o plantas seguidos, dentro de la mirada
        # (prompt 44, Manel: decisión de método) la escala de la traducción: vivir bien en el valle da el reposo del paper dos en los tres ejes (ver `vivir_bien`)
        self.escala_v6 = bool(escala_v6)
        # (prompt 45, Manel) saber: lo que quita una comida se aprende solo de las comidas en que el hambre no llega a cero (si se queda en cero, quitó más de
        # lo que se ve: es «al menos»). Llegar a cero = acabar con no más hambre de la que sube en un turno (lo más que ha visto subir, aprendido)
        self.aprende_v7 = bool(aprende_v7); self.sube_max = 0.0
        # (prompt 45, esquema simétrico de Manel) lo que una acción hace a la necesidad de la otra cuenta en las dos direcciones: hacer soltar comida a quien la
        # necesita es una pérdida del mismo tamaño que la ganancia de darle (su necesidad × lo que pierde), pesada por el vínculo. No se prohíbe empujar
        self.simetria_v7 = bool(simetria_v7)
        # (prompt 46, con la corrección de Manel) una criatura sin razón no se pone en el lugar de la otra: la simetría solo cuenta lo que se ve. Si la otra se
        # ve flaca, herida o de duelo, hacerle soltar comida es una pérdida para quien empuja, pesada por el vínculo (contagio), del tamaño de la de simetria_v7.
        # Si va bien, no cuenta (rivalizar por el recurso). Las reservas de la otra, que no se ven, no entran
        self.simetria_vista_v8 = bool(simetria_vista_v8)
        self.satura_v8 = bool(satura_v8)
        # (prompt 47, Manel) la vida de la otra se ve en cuatro niveles (regla del mundo). La foto de golpear lo usa: si la otra se ve moribunda (un golpe la
        # mata), la foto imagina su muerte con lo que supone para el vínculo, igual que cuando muere la hermana (el duelo, recién sabido, por su vínculo)
        self.ve_vida_v9 = bool(ve_vida_v9); self.pareja_vida_nivel = None
        # (rama valle-sin-techo, prompt 49, experimento de lectura) añadir solo dolor a una opción nunca puede hacerla mejor: las fotos se comparan antes del
        # reescalado del techo de volumen (ver `estado_sin_techo`). Para todas las fotos y todas las acciones
        self.sin_techo_v11 = bool(sin_techo_v11)
        # (prompt 53, Manel) el duelo: cada muerte añade su propio duelo, que se suma al que ya haya aunque esté bajando, como el hambre (antes: el mayor).
        # Sus tres dimensiones son las del reparto del siete de S-MUERTE-PAREJA (cuerpo 0,15, recursos 0,25, vínculo 0,6); el peso, el vínculo con la muerta
        self.duelo_suma_v15 = bool(duelo_suma_v15)
        # (prompt 53, Manel) el compromiso deja de mandar: seguir hacia el destino es una opción más, con su foto, cada turno; sin premio por seguir
        self.compromiso_opcion_v15 = bool(compromiso_opcion_v15)
        # (prompt 54, experimento) la inercia: con el compromiso como opción, solo cambia de destino si otra opción es mejor que seguir por este margen (en d)
        self.compromiso_margen = compromiso_margen; self._n_seguir = None
        # (prompt 54, Manel) la voz, primer paso: la expresión que sale sola, como la cara. Un sonido para la fuerza que más pesa en su estado de ahora, con tres
        # intensidades (suave, medio, fuerte: tercios de la mitad del techo de volumen, VOL_MAX importado); suena solo cuando cambia la que manda o su
        # intensidad; no gasta el turno, no cuesta energía, no se elige y no miente. Lo que se oye de tristeza o dolor del cuerpo cuenta en el contagio como
        # lo que se ve (el camino de «estoy de duelo»). Sin las llamadas «estoy de duelo», «estoy herida» y «no tengo energía»
        self.voz_v16 = bool(voz_v16); self._suena = None
        # (prompt 55) el frío sube el hambre fuera (regla pública del cuerpo): la foto lo usa. Lo que ha aprendido que sube el hambre es una media de los
        # últimos turnos, con el frío que pasaba; la foto le quita ese frío y le pone el de donde pasa cada turno (fuera con frío, o en casa)
        self.frio_sabe_v17 = bool(frio_sabe_v17)
        # (prompt 56, experimento) el compromiso con interrupción emocional: solo vuelve a mirar todas sus fotos al llegar, si no avanza en 3 turnos, o si
        # cambia la fuerza que más pesa o su intensidad (la señal de la voz); sin las demás reglas escritas que sueltan el destino
        self.compromiso_emocion_v18 = bool(compromiso_emocion_v18)
        # (prompt 56) la noche entera en la foto: al decidir dónde dormir (dormir, o ir a casa de noche), la foto mira hasta la mañana, no solo la mirada
        self.noche_entera_v18 = bool(noche_entera_v18)
        # (prompt 57, Manel) las llamadas prácticas, como opciones que decide la regla general con su foto, con la voz aparte de los pies: «aquí estoy»,
        # «aquí hay comida», «la bestia» y «ven, lo necesito», con la fuerza que elige la foto (suave, medio, fuerte). Lo que espera que pase (que venga
        # alguien) lo aprende por cada llamada, como lo de los matorrales, desde lo que dice la cultura. Sin las llamadas que salían solas
        self.llamadas_opcion_v19 = bool(llamadas_opcion_v19); self.llam_frec = {}; self.llam_pend = []; self.llam_hechas = []
        # (prompt 58, Manel) lo que aprende de una llamada es si cambia algo: cuántas veces viene alguien después de llamar frente a cuántas sin haber llamado,
        # en situaciones parecidas (pudo hacer esa llamada a alguna de las suyas y no la hizo); la llamada vale por la diferencia. Sin llamar, sin cultura: desde 0
        self.llamadas_contraste_v20 = bool(llamadas_contraste_v20); self.llam_ctrl = {}
        # (prompt 58, Manel) la alarma: el peligro de las suyas es la zona que la bestia puede alcanzar en la mirada (a su paso, regla pública), no solo al lado
        self.alarma_zona_v20 = bool(alarma_zona_v20)
        # (prompt 60, Manel) la cultura no se olvida sola: una creencia heredada solo cambia con lo que vive, no con el paso de los días (el cuaderno: `peso`)
        self.cultura_sin_olvido_v22 = bool(cultura_sin_olvido_v22); self.cuaderno.heredado_sin_olvido = self.cultura_sin_olvido_v22
        # (prompt 60, Manel) la medicina cura heridas, no el daño del hambre (regla pública): lleva la cuenta del daño que le hizo el hambre; un uso sin herida
        # no se apunta como cura, y uno que cura toda la herida que tenía es «al menos»
        self.medicina_herida_v22 = bool(medicina_herida_v22); self.dano_hambre = 0.0
        # (prompt 60, Manel) «yo tengo y mi hermana no» (S-PROVISION) pesa por la necesidad de la hermana: si la cree sana, no pesa
        self.provision_necesidad_v22 = bool(provision_necesidad_v22)
        # (prompt 61, Manel) en las fotos de dejar y coger, solo cuenta como comida guardada (despensa, almacén) la comida
        self.cuenta_despensa_v23 = bool(cuenta_despensa_v23)
        # (prompt 61, Manel) cuando dos opciones salen exactamente iguales, sigue con lo que estaba haciendo, en vez de que el desempate las vaya alternando
        self.empates_sigue_v23 = bool(empates_sigue_v23); self._ult_clave = None
        # (prompt 62, Manel) la foto de dar medicina imagina a la otra curada: con la hermana, la vida que le supone sube lo que cree que cura la medicina, y con eso
        # baja el dolor de verla herida (S-DANO-PAREJA, por su vínculo); con una vecina, lo que pesa es su falta (R-HERMANO-FALTA, por su vínculo), que ya se aliviaba
        self.dar_cura_v24 = bool(dar_cura_v24)
        # (prompt 62, Manel) un margen pequeño para los casi empates: si otra opción sale a menos de este margen de la elegida, sigue con lo que estaba haciendo
        self.empate_margen_v24 = None if empate_margen_v24 is None else float(empate_margen_v24)
        # (prompt 63, decisión de Manel) el contagio de la herida, como el duelo: verla herida duele también con una vecina, según su vínculo (siempre menos que
        # con la hermana: la comunidad va de 0,1 a 0,5, la hermana de 0,5 a 1), si la ha visto herida en la última mirada; en la foto de darle la medicina, curada
        self.contagio_vecinas_v25 = bool(contagio_vecinas_v25)
        # (prompt 64, decisión de Manel) aprender mirando, como la vía (a) del siete (hermanas_P7_48): ve que otra usa algo (lleva una menos, sin dejarla ni darla)
        # o que le pasa algo (la bestia al lado o la zona salvaje, y baja de nivel), y el cambio que se nota por fuera en los turnos siguientes; lo apunta como
        # «visto», pesado como lo vivido × el vínculo con ella (nunca más que lo vivido). Solo lo que se ve: sus niveles de vida, si está flaca, lo que lleva
        # (prompt 65, decisión de Manel) el reloj de dentro, como el reloj del cuerpo (heredado): en cada turno de su rato de mirar, la foto usa el frío y la vista
        # de la fase en que caerá ese turno (las fases del día, la temperatura de fuera y la vista de cada fase, del mundo), no los de ahora. No es una fila ni una orden
        self.reloj_dentro_v27 = bool(reloj_dentro_v27)
        # (prompt 65) juntar los recuerdos viejos del cuaderno (de hace más de 2 días), una vez al día (ver cuaderno_P7.junta); solo si las partidas salen idénticas
        self.juntar_viejos_v27 = bool(juntar_viejos_v27); self._dia_junta = None; self.juntados = 0
        # (prompt 67) tres aceleraciones que no cambian nada: las distancias andando en una caché compartida por proceso (el mapa no cambia); lo que cree de
        # la comida, guardado mientras el cuaderno no cambie; la fuerza que manda, una vez por turno
        self.rapido_v28 = bool(rapido_v28); self._cc = None; self._ex = None
        # (prompt 67, decisiones de la mesa) el valorador de sumas: la misma criatura, pero lo que vale cada foto es la suma de ganancias menos pérdidas de las
        # tres dimensiones (ver `compone_sumas`), y gana la mayor; la fuerza que manda y su intensidad salen de las seis sumas, con los mismos cortes
        self.sumas_v29 = bool(sumas_v29)
        # (prompt 72, Manel) el valorador de posición (P32): lo que vale cada foto es la distancia del motor con solo su término de posición (ver
        # `compone_posicion`); la voz, la interrupción y el contagio salen de las seis sumas crudas, como en S32
        self.posicion_v30 = bool(posicion_v30)
        # (prompt 76, Manel) el para qué: la foto de ir hacia un destino imagina también lo que hará al llegar, en los destinos donde faltaba: a la hermana
        # herida llevando medicina, dársela (y con su cura, que ya imaginaba dar_cura_v24, baja el dolor de verla herida y su falta); al botín, coger lo que hay
        # (la comida vista en el suelo o en una planta, o una del almacén)
        self.para_que_v31 = bool(para_que_v31)
        # (prompt 76, Manel) la gravedad: lo que siente por una de las suyas herida usa los cuatro niveles de vida que ve (sana, herida, muy herida, moribunda),
        # cada uno con la vida que supone (config_cuerpo_valle.json → banda_de_la_hermana.niveles_v31), no solo sana o herida
        self.gravedad_v31 = bool(gravedad_v31)
        # (prompt 79, Manel: piezas B, C y D del diseño final) el radar aprendido: cada criatura (la hermana y cada vecina) y cada fuente de comida es un objeto
        # del cuaderno con su valor en cuerpo, recursos y vínculo, que nace (C) y se aprende viviendo y mirando (B); dar una cosa deja en ella valor de vínculo
        # aprendido (D). Ver `_rad_*` y las filas V-RADAR-* y P-RADAR-*
        self.radar_v34 = bool(radar_v34); self._rad = None
        # (prompt 80, para separar las piezas) sin C: las criaturas nacen sin valor (las cosas conservan el de la tabla, sin el que B no puede quitar las
        # constantes); sin D: dar vale lo de nacimiento y no se aprende. Y el arreglo de honradez: lo visto (que da a otras) no entra en lo que vale para ella,
        # y las vecinas conocidas que no ve en una mirada apuntan trato 0, como la hermana
        self.radar_c_v34 = bool(radar_c_v34); self.radar_d_v34 = bool(radar_d_v34); self.radar_honesto_v35 = bool(radar_honesto_v35)
        # (prompt 81, Manel) el arreglo de la pieza B: (1) las ganancias del radar se sacian como las demás: con la de vivir bien de su dimensión no pasan de la
        # meta de esa dimensión (las del motor, importadas): más compañía o más valor ya no suma; (2) cada mirada apunta lo que añadió tenerla al lado en total
        # en esa mirada (no una media por turno), todos los apuntes con la misma intensidad
        self.radar_v36 = bool(radar_v36)
        # (prompt 83, Manel: un error de concepto de la pieza C) dos cosas que estaban en la misma casilla: (a) lo que vale la vida de la otra por ser familia o
        # especie (Hamilton: la hermana, la mitad de la propia; una vecina, un cuarto de eso), de nacimiento, NO se aprende, y pesa cuando ella sufre, le falta algo
        # o está en peligro (`peso_kin`, `valor_vida`); y (b) lo que ella hace por mí (el radar aprendido, que ya no nace con (a)). Y lo que aprende de dar
        # medicina cuenta también lo que ve pasar cuando otras la dan
        self.radar_v38 = bool(radar_v38)
        # (prompt 84, Manel) (1) el valor de las otras por ser hermana o vecina (lo que no se aprende) son los pesos de vínculo que tenía RG32r (medidos en sus
        # partidas: config_cuerpo_valle.json → radar_v39), no los números de Hamilton; pesa en los mismos sitios. (2) En todo lo que se aprende, lo de nacimiento
        # (la cultura y el radar) pesa como una sola experiencia: un recuerdo de intensidad 1, no cuatro de 0,5
        self.radar_v39 = bool(radar_v39)
        # (prompt 85, Manel: pieza E) dos sabores: la comida del huerto da más placer al comerla (alimenta igual). El mundo marca cada comida con su origen
        # (objetos.sabores); el cuerpo siente ese placer de más (config_cuerpo_valle.json → sabores_v40) y el radar aprende el sabor de cada fuente (su valor de
        # cuerpo, «fuente:…|sabor»); la foto de comer una comida suma su sabor (P-SABOR) y, al dar, elige qué comida da (dar la sabrosa vale además su gusto a
        # la otra, por lo que vale para ella). (pieza F) Los hechos del mundo que protegen a la acompañada, escritos en la cultura (cultura_hechos_v40.json)
        self.sabores_v40 = bool(sabores_v40); self.hechos_v40 = bool(hechos_v40)
        # (prompt 86, Manel) la foto usa los hechos de acompañar (los de la cultura, pieza F): la bestia ataca a una sola, a suertes, de las que tiene pegadas;
        # en la foto, el peligro de la bestia para ella (F-4-ALCANCE) se reparte entre las que estarían juntas (1/n), y lo mismo el de la hermana (F-HERMANO-
        # AMENAZA) y el de perder a una de las suyas cuando hay bestia (P-RADAR). Los empujones por ser más y echar a la bestia entre dos ya los imaginaba
        self.acompanar_v41 = bool(acompanar_v41)
        # (prompt 87, Manel) el arreglo de los sabores al dar: el gusto que la otra saca de la comida que le doy (lo que yo he aprendido de su fuente) entra en la
        # foto de dar de la regla general como ganancia de vínculo (G-SABOR-OTRA), pesado por lo que vale la otra por ser hermana o vecina (peso_kin), cuando
        # la otra la necesita (como en el prompt 85); la comida que se da es la que dice la foto (su origen) o, sin origen, la primera de la bolsa (la que da
        # el mundo). Y un empate exacto entre opciones, después de las reglas de empate de antes, no lo decide el orden de la lista: a suertes, con la semilla
        # de la partida (y la criatura).
        self.sabores_v42 = bool(sabores_v42); self.empate_suertes_v42 = bool(empate_suertes_v42)
        # (prompt 88, Manel) los dos arreglos de los sabores: el gusto de la otra cuenta en cualquier foto de dar, crea o no que la otra lo necesita; y la foto
        # de comer cuenta siempre el sabor de lo que se come (sin origen en la opción, el de la primera comida de la bolsa, la que come el mundo), también al
        # comer al final o antes de otra cosa. El gusto no se satura aparte: lo que diga el motor.
        self.sabores_v43 = bool(sabores_v43)
        # (prompt 89, Manel) la foto usa los hechos de la pieza G (cultura_hechos_v44.json: echar y matar, que son verdad en todos los mundos), como ya hace con
        # acompañar: al imaginar empujar o pegar a una bestia (cualquiera, por su nombre), cuenta con las suyas (la hermana y las vecinas) que ya están pegadas a
        # ella, y lo que pasaría: empujada por bastantes, se va lejos un tiempo (y suelta lo que lleva); golpeada por bastantes, muere (a cambio de su golpe a
        # cada turno) y deja sus comidas; sola, me pega a mí. Sin la bestia, la foto no tiene sus peligros
        self.bestia_v44 = bool(bestia_v44); self.hechos_g = {}
        # (prompt 90, Manel) pieza I, empezando por la hermana sola: (a) sin costumbre clara, la imagina siguiendo su último paso unos pasos; (b) aprende mirando sus
        # costumbres (adónde va en cada situación que se ve desde fuera), como frecuencias igual que los matorrales; (c) una vez por turno calcula dónde estará al
        # acabar la mirada, y las filas de las fotos (no la de ahora) leen esa casilla donde hoy leen dónde la vio (config_cuerpo_valle.json → imaginar_v45)
        self.imagina_v45 = bool(imagina_v45); self.costumbre = {}; self._her_ant = None; self._her_paso = None; self._her_pred = None; self._llamada_t = -10 ** 9; self.pred_v45 = []
        # (prompt 90, Manel) el duelo sale del radar: lo que pierde cuando muere una de las suyas es lo que era para ella en cuerpo, recursos y vínculo según el
        # radar aprendido, más lo que vale por ser hermana o vecina (en el cuerpo, como en P-RADAR); tres filas de pérdida, sin el reparto fijo de S-MUERTE-PAREJA
        self.duelo_v45 = bool(duelo_v45); self.duelos_v45 = []
        # (prompt 93, Manel) arreglos de errores: (1) lo vivido en cada noche dormida se apunta siempre, duerma donde duerma (no solo con la orden «para dormir, a
        # casa», que sigue apagada en la regla general); (2) los robos en el radar: la robada resta la comida que pierde en un empujón (como lo que le roba la
        # bestia) y las que lo ven apuntan un robo de la que gana (no un regalo de la robada), leído como lo demás del radar (el mundo enseña los empujones
        # vistos, observacion.empujones_vistos); (3) en un empate exacto, gana quedarse; (4) lo que cuesta cada clase de acción se aprende de lo que hizo de
        # verdad su cuerpo (el mundo se lo dice, observacion.lo_que_hizo), no de lo que eligió: si el cuerpo la hizo dormir, aprende de dormir
        self.noches_v47 = bool(noches_v47); self.robos_v47 = bool(robos_v47); self.empate_quedarse_v47 = bool(empate_quedarse_v47); self.prop_real_v47 = bool(prop_real_v47)
        # (prompt 94, Manel) lo que cuesta cada clase de acción se aprende también por la hora (la fase) y por dentro o fuera de casa (con lo que hizo de verdad su
        # cuerpo): en el mundo el hambre de un turno depende de la hora, el frío y el sueño, no de empujar o quedarse; la foto lee lo de la hora y el sitio de ahora
        # (y, si aún no tiene nada de ahí, lo de la clase, como antes)
        self.prop_ctx_v48 = bool(prop_ctx_v48); self.prop_ctx = {}
        # (prompt 95, Manel) (1) empujar y golpear tienen su propia clase al aprender lo que cuestan (aparte de dar, coger y dejar); (2) lo que aprende de una noche
        # dormida es toda la vida que perdió mientras dormía allí, sea por lo que sea; (3) los robos: la robada aprende de lo que pierde de verdad (un recuerdo vivido
        # de la que le roba), y la que lo ve, con el peso de lo que se aprende mirando (por su vínculo con la robada: nunca más que ella); (4) el placer del gusto
        # depende del hambre de quien come (entero con mucha hambre, un cuarto con la tripa llena, en proporción en medio), al comer y al imaginar el de otra al
        # darle; lo aprendido del gusto de la comida no baja por estar llena (config_cuerpo_valle.json → gusto_v49)
        self.clase_v49 = bool(clase_v49); self.noche_perdida_v49 = bool(noche_perdida_v49); self.robos_v49 = bool(robos_v49); self.gusto_hambre_v49 = bool(gusto_hambre_v49)
        # (prompt 96, Manel) A. el largo de las fotos: de noche, todas las fotos que se comparan miran hasta la mañana, como la de dormir (lo que hace y después dormir
        # donde quede); B. el árbol de fruta dulce: su fruta es comida con origen «dulce», con el doble de gusto que la del huerto (según el hambre, como los demás);
        # el árbol se ve y se recuerda como un matorral; la cultura trae dos hechos (aparece a veces lejos; al atardecer y de noche la bestia va a él)
        self.horizonte_v50 = bool(horizonte_v50); self.arbol_v50 = bool(arbol_v50)
        # (prompt 103, Manel) tres arreglos, apagados por defecto: el gusto de cualquier comida se apunta al comerla (dulce_v51); ir a casa a un sitio libre de
        # dentro, no la puerta, rodeando a quien esté delante, y no dormirse en una puerta (casa_v51); el fractal: cada fila 0,8 a su dimensión y 0,1 a las otras
        # dos, como las del cuerpo (fractal_v51)
        self.dulce_v51 = bool(dulce_v51); self.casa_v51 = bool(casa_v51); self.fractal_v51 = bool(fractal_v51)
        self._rep = RepartoFractal(REPARTO) if self.fractal_v51 else None
        # (prompt 104, Manel) dar: lo que gana quien da = el gesto (por dar, aunque sea poco) + lo que el regalo hace por la otra (su alivio y su gusto, como
        # hoy), las dos pesadas por lo que vale la otra en su radar (familia + confianza: peso_dar); lo que pierde, lo de siempre
        self.dar_v52 = bool(dar_v52)
        # (prompt 105, Manel) dar_v53 (sobre dar_v52): el gesto, a la mitad (dar_v53.gesto_parte); el peso de la otra, su valor en el radar entero (las tres
        # dimensiones juntas, para que los robos bajen la confianza); el alivio de la otra al dar, como vínculo (G-ALIVIO, el reparto del gesto).
        # tope_dar_off: SOLO PARA PROBAR, sin la regla tope_dar (dar sin tope, que decida la foto)
        self.dar_v53 = bool(dar_v53); self.tope_dar_off = bool(tope_dar_off)
        # (prompt 106, Manel) dar_v54 (sobre dar_v53): el peso de la otra = su familia × (su radar entero ahora / al nacer): la escala de familia, movida por la
        # confianza; y la foto de dar la última comida imagina lo que le costará al cuerpo quedarse sin ella (F-ULTIMA-COMIDA, la necesidad por lo que sirve)
        self.dar_v54 = bool(dar_v54)
        # (prompt 108, Manel) el gesto, solo al dar comida; la medicina se da por lo que alivia a la otra (cuando lo necesita)
        self.gesto_comida_v56 = bool(gesto_comida_v56)
        # (prompt 109, Manel) devolver lo que me acaban de dar no es un gesto (devolver_v57); lo que das te cuesta lo que haría por ti: dar la última medicina
        # cuenta lo que me curaría, según mi herida (cuesta_medicina_v57)
        self.devolver_v57 = bool(devolver_v57); self.cuesta_medicina_v57 = bool(cuesta_medicina_v57); self._recib = {}; self._lleva_prev_v57 = {}
        self.devolver_v58 = bool(devolver_v58)                              # (prompt 110) el intercambio a la vez: si le di eso mismo ese turno, también me lo dio ella
        self.devolver_solo_gesto_v59 = bool(devolver_solo_gesto_v59)        # (prompt 111, la mesa corrige el 109) devolver quita solo el gesto; el alivio y el gusto se quedan
        self.devolver_necesidad_v60 = bool(devolver_necesidad_v60)          # (prompt 112) devolver: sin gesto; el alivio, solo si la otra lo necesita más que yo
        # (prompt 115, Manel) que robar deje huella en el vínculo: (2, ampliado en el prompt 116) ganar un empujón (empuje yo o me empuje ella; al robar o al
        # recuperar) nunca es un regalo suyo: un regalo es solo lo que la otra da con la acción de dar; (3) un robo baja el trato de la ladrona lo que sube con un regalo (un cuarto), y en las que lo ven, por su vínculo con la robada (como
        # aprenden hoy un robo visto); (4) quitarle comida: la necesidad que le deja, en el vínculo y con el peso de dar (el espejo exacto del alivio al dar)
        self.robo_regalo_v61 = bool(robo_regalo_v61); self.robo_trato_v61 = bool(robo_trato_v61); self.quitar_espejo_v61 = bool(quitar_espejo_v61)
        self.voz_off_v62 = bool(voz_off_v62)                              # (prompt 123, taller) la voz entera apagada: no elige ni emite ninguna llamada de voz (aquí estoy, aquí hay comida, la bestia, ven lo necesito) y no hace caso de las que oye; la expresión (suena) no cambia
        # (prompt 124, taller) la voz clase por clase: con cada interruptor, esa clase no se emite ni se oye; las demás siguen. Las clases fuera, en un conjunto
        self._voz_fuera = set(self.LLAMADAS_VOZ) if self.voz_off_v62 else {c for c, on in (("aqui_estoy", voz_sin_aqui_estoy_v63), ("aqui_hay_comida", voz_sin_comida_v63),
                                                                                            ("la_bestia", voz_sin_bestia_v63), ("ven_lo_necesito", voz_sin_ven_v63)) if on}
        # (prompt 128, taller; el plan de informe_voz_v4) la cara y la voz de la base:
        #   cara_v64: enseña sus tres balances (solo lo propio) a quien la ve; quien mira se pone la necesidad de la otra por lo que vale para ella (la mayor) y
        #             deja de suponerle 80 o 30 de hambre (la saca de su cara);
        #   voz_v64: sustituye a «ven, lo necesito», «aquí estoy» y «la bestia»: el cuerpo emite sin elegir la clase (alarma, petición, contacto), la fila que más
        #             pesa, su objeto y su tamaño (el cuánto); la intensidad fija el alcance; solo hay alarma con miedo o dolor fuertes; dormida no emite;
        #   aprender_cara_v64: aprender mirando con la cara de la otra (lo visto, con la intensidad por el vínculo);
        #   para_v64: cuando le quitan algo o la empujan, un «para» a quien lo hace, que las de su casa oyen como una petición de acudir
        self.cara_v64 = bool(cara_v64); self.voz_v64 = bool(voz_v64) or bool(para_v64); self.voz_base_v64 = bool(voz_v64)
        self.aprender_cara_v64 = bool(aprender_cara_v64); self.para_v64 = bool(para_v64)
        if self.voz_base_v64: self._voz_fuera |= {"ven_lo_necesito", "aqui_estoy", "la_bestia"}       # «aquí hay comida» se queda como está
        # (prompt 130, taller) cara_dar_v65: el balance del cuerpo de la otra (su cara) no entra en darle comida ni medicina. Su hambre es la que dice su petición
        #   de comida (F-HAMBRE, con su tamaño) si se la he oído en la mirada; su daño, el de su petición de cura (F-DANO); si no, lo de antes de la cara (flaca o
        #   herida, o no). Las peticiones oídas se apuntan aparte (la de la hermana se borra al llegar a su lado, y es justo cuando se le da)
        self.cara_dar_v65 = bool(cara_dar_v65); self.pide_v65 = {}
        # (prompt 131, taller) ya_tiene_v67: no se pide ni se da comida a quien ya tiene qué comer. (1) La petición de comida (de cura) por la voz solo sale si quien
        #   la emite no lleva comida (medicina); si no, esa fila no habla, como R-CARENCIA, y habla la siguiente. (2) Si veo que la otra lleva lo que le doy, el
        #   alivio de dárselo (S-DAR y G-ALIVIO) es cero, y (Manel, tras el aviso) el gesto (G-GESTO) tampoco cuenta. (3) Su hambre y su daño, de su petición de este turno o del anterior (no de la mirada)
        #   dormida_sin_voz_v67: lo hace el mundo (la voz de antes no sale de una criatura dormida, como la de la base); aquí solo se acepta
        self.ya_tiene_v67 = bool(ya_tiene_v67)
        # (prompt 132, taller) voz_piezas_v68: la voz de la base pieza a pieza sobre M ("alarma", "contacto", "peticion", separadas por comas): solo salen esas
        #   clases (las filas de las otras clases no hablan, como R-CARENCIA); la voz de antes se queda entera salvo que la alarma sustituye a «la bestia».
        #   El mundo (voz_v68) entrega la voz y añade la alarma a lo que despierta, sin quitar lo de antes
        self.voz_piezas_v68 = {p.strip() for p in str(voz_piezas_v68 or "").split(",") if p.strip()}
        if self.voz_piezas_v68:
            self.voz_v64 = True
            if "alarma" in self.voz_piezas_v68: self._voz_fuera.add("la_bestia")
        self._voz_ultima = None; self._cara_cache = (None, None); self.her_contacto = None; self.pareja_cara = None; self.cuenta_v64 = {}
        self._robada_por = {}; self.cuenta_v61 ={"regalo_recupera": 0, "regalo_empuje_otro": 0, "regalo_recibido": 0, "robos_trato": 0, "robos_trato_vistos": 0.0}     # (solo medir)
        import random as _r; self._rng_empate = _r.Random(f"{semilla_partida}|{agente}"); self.empates_v42 = {"decisiones": 0, "empates": 0, "por": {}}
        self.radar_c_factor = float(radar_c_factor)                         # (prompt 82, solo para ver) el nacimiento de las demás × este factor (1: sin cambio)
        self._mapa_firma = hash((tuple(mapa_publico["terreno"]), json.dumps(mapa_publico.get("casas"), sort_keys=True)))
        self.aprender_mirando_v26 = bool(aprender_mirando_v26); self.visto_snap = {}; self.visto_pend = []; self.visto_stats = {}; self.vistos_log = []; self._obj_prev = {}    # (prompt 46, Manel) cada ganancia se satura en la meta de su eje (ver `compone`)
        self.sentir = bool(sentir); self.sentido = {}; self.diag_dar = []; self.diag_no_come = []; self.diag_come_sin = []
        self.atencion_huida = bool(atencion_huida)     # (prompt 33, Manel) la tristeza nunca impide huir: si ve la bestia u oye «peligro», la atención vuelve entera ese turno        # (prompt 31, Manel) con la hermana muerta sigue oyendo y respondiendo a las vecinas
        self._lleva_vec_prev = {}; self.vecinas_on = bool(vecinas); self.comida_sin_hermana = bool(comida_sin_hermana); self.vin = {}; self.otras = {}; self._lleva_otras_prev = {}; self.dilemas = []
        if self.vecinas_on: self.B = float(CFG["vinculo"]["escalones"]["hermana"][0])   # (prompt 27) «aquí hay comida» una vez por sitio y por día   # (prompt 26) lee las reglas públicas del trabajo: de noche y sin fuerzas no se trabaja
        self.comida_sobra = bool(comida_sobra); self.sitios_llamados = set(); self._sitios_ahora = set()    # (prompt 25) «aquí hay comida» cuando ve comida y no tiene hambre (no cuando lleva la bolsa llena)
        self.responde = bool(responde_llamadas); self.peligro_oido = []; self.comida_oida = {}; self.ayuda_oida = None; self.respuestas = {}; self.oidas = {}; self.ultima_ayuda_t = None
        self.histeresis_llamadas = bool(histeresis_llamadas); self._apagada = {}; self.compromiso = bool(compromiso); self.dest = None; self.dormir_en_casa = bool(dormir_en_casa)
        self.celdas_de = {}
        for q in self.pisables: self.celdas_de.setdefault(self.ley[Tm[q[1]][q[0]]], []).append(q)
        self._campos = {}; self._creencias = {}
        self.acum = {}; self.noche = {"turnos": 0, "fuera": 0, "dano": 0.0, "robo": 0}; self.fase_prev = None
        self.plantas_vistas = {}; self.trabaje = {}; self.items_vistos = set(); self.medicinas = set(); self.sitio_cerca = {}
        if cultura:
            self.cultura = json.load(open(cultura, encoding="utf-8")) if isinstance(cultura, str) else cultura
            KC = CFG["cultura"]
            n_nace, w_nace = (1, 1.0) if self.radar_v39 else (KC["n_recuerdos"], KC["w_h"])     # (prompt 84) como una sola experiencia
            for en in self.cultura["entradas"]:
                for sit in en["situaciones"]:
                    for _ in range(n_nace):
                        r = {"dia": self.cuaderno.dia_actual(), "tick": None, "efecto": {d: round(float(en["efecto"].get(d) or 0.0), 4) for d in CU.DOMINIOS},
                             "importancia": {d: 0.0 for d in CU.DOMINIOS}, "intensidad": w_nace, "creencia_antes": None, "al_menos": False, "origen": "heredado"}
                        for k in ("da", "por_turnos", "retraso", "retraso_dias", "dura", "empieza", "por_100_casillas", "viene"):
                            if k in en: r[k] = en[k]
                        self.cuaderno._obj(en["objeto"])["situaciones"].setdefault(sit, []).append(r)
        if self.radar_v34: self._rad_inicia()
        if self.arbol_v50 and cultura:                                      # (prompt 96) los dos hechos del árbol de fruta dulce, como la cultura (heredados; no dicen dónde ni cuándo)
            KC = CFG["cultura"]; n_nace, w_nace = (1, 1.0) if self.radar_v39 else (KC["n_recuerdos"], KC["w_h"])
            for en in json.load(open(os.path.join(AQUI, "cultura_hechos_v50.json"), encoding="utf-8"))["entradas"]:
                for sit in en["situaciones"]:
                    for _ in range(n_nace):
                        r = {"dia": self.cuaderno.dia_actual(), "tick": None, "efecto": {d: round(float((en.get("efecto") or {}).get(d) or 0.0), 4) for d in CU.DOMINIOS},
                             "importancia": {d: 0.0 for d in CU.DOMINIOS}, "intensidad": w_nace, "creencia_antes": None, "al_menos": False, "origen": "heredado", "hecho": en["dice"]}
                        self.cuaderno._obj(en["objeto"])["situaciones"].setdefault(sit, []).append(r)
        if self.bestia_v44 and cultura:                                     # (prompt 89) los hechos de echar y matar, como la cultura (heredados), con sus números
            KC = CFG["cultura"]; n_nace, w_nace = (1, 1.0) if self.radar_v39 else (KC["n_recuerdos"], KC["w_h"])
            for en in json.load(open(os.path.join(AQUI, "cultura_hechos_v44.json"), encoding="utf-8"))["entradas"]:
                if en["rueda"] not in ("echar", "matar"): continue          # las demás ruedas no son verdad en todos los mundos
                self.hechos_g[en["rueda"]] = {k: float(v) for k, v in en["numeros"].items()}
                for sit in en["situaciones"]:
                    for _ in range(n_nace):
                        r = {"dia": self.cuaderno.dia_actual(), "tick": None, "efecto": {d: 0.0 for d in CU.DOMINIOS}, "importancia": {d: 0.0 for d in CU.DOMINIOS},
                             "intensidad": w_nace, "creencia_antes": None, "al_menos": False, "origen": "heredado", "hecho": en["dice"]}
                        self.cuaderno._obj(en["objeto"])["situaciones"].setdefault(sit, []).append(r)
        if self.hechos_v40 and cultura:                                     # (prompt 85, pieza F) los hechos del mundo, como la cultura (se apuntan; hoy no los lee nada)
            KC = CFG["cultura"]; n_nace, w_nace = (1, 1.0) if self.radar_v39 else (KC["n_recuerdos"], KC["w_h"])
            for en in json.load(open(os.path.join(AQUI, "cultura_hechos_v40.json"), encoding="utf-8"))["entradas"]:
                for sit in en["situaciones"]:
                    for _ in range(n_nace):
                        r = {"dia": self.cuaderno.dia_actual(), "tick": None, "efecto": {d: round(float(en["efecto"].get(d) or 0.0), 4) for d in CU.DOMINIOS},
                             "importancia": {d: 0.0 for d in CU.DOMINIOS}, "intensidad": w_nace, "creencia_antes": None, "al_menos": False, "origen": "heredado", "hecho": en["dice"]}
                        self.cuaderno._obj(en["objeto"])["situaciones"].setdefault(sit, []).append(r)

    # ── percepción y memoria ──
    def _dist_a(self, meta):
        """pasos andando hasta `meta` desde cualquier casilla (BFS desde la meta, con caché pequeña)"""
        if self.rapido_v28:                                                 # (prompt 67) la caché compartida: el mismo resultado, calculado una vez
            k = (self._mapa_firma, meta)
            if k in _DIST: _DIST.move_to_end(k); return _DIST[k]
            D = self.M.distancias([meta]); self.M._dist.pop((meta,), None); _DIST[k] = D
            if len(_DIST) > 512: _DIST.popitem(last=False)
            return D
        if meta in self._dist_cache: self._dist_cache.move_to_end(meta); return self._dist_cache[meta]
        D = self.M.distancias([meta]); self._dist_cache[meta] = D
        self.M._dist.pop((meta,), None)                                    # (prompt 30) la caché es esta, no la del mapa (que no tiene tope)
        if len(self._dist_cache) > (160 if self.dist_u else 64): self._dist_cache.popitem(last=False)
        return D

    @staticmethod
    def cheb(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    def pasos(self, a, b):
        """(prompt 30) cuánto cuesta llegar de a a b andando (camino más corto); sin camino, muy lejos. El mapa no cambia: la tabla de pasos desde cada casilla
        se calcula una vez por proceso y se guarda compacta (array de enteros), compartida por todas las criaturas"""
        b = tuple(b); arr = _PASOS.get(b)
        if arr is None:
            D = self._bfs_pasos(b); n = len(self.M.T[0])
            arr = array("h", [-1]) * (n * len(self.M.T))
            m_ = len(self.M.T)
            for (x, y), d in D.items():
                if 0 <= x < n and 0 <= y < m_: arr[y * n + x] = min(d, 32000)
            _PASOS[b] = arr
        n = len(self.M.T[0])
        if not (0 <= a[0] < n and 0 <= a[1] < len(self.M.T)): return 999
        v = arr[a[1] * n + a[0]]
        return 999 if v < 0 else v

    def _bfs_pasos(self, b):
        """pasos hasta b. Si b no se pisa (matorral, planta, almacén…), llegar es quedar pegada (a 1, tablero), y estar pegada cuesta 1, como antes"""
        from collections import deque
        T = self.M.T; n, m_ = len(T[0]), len(T)
        if T[b[1]][b[0]] not in ("m", "p", "x"): sem = [b]; D = {b: 0}
        else:
            sem = [(b[0] + dx, b[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy)]
            sem = [v for v in sem if 0 <= v[0] < n and 0 <= v[1] < m_ and T[v[1]][v[0]] not in ("m", "p", "x")]
            D = {v: 1 for v in sem}
        q = deque(sem)
        while q:
            u = q.popleft()
            for d in ((0, -1), (0, 1), (1, 0), (-1, 0)):
                v = (u[0] + d[0], u[1] + d[1])
                if v not in D and self.M.pasa(v, u): D[v] = D[u] + 1; q.append(v)
        return D

    def lejos(self, a, b):
        """«cuánto me cuesta llegar»: pasos con las distancias unificadas; si no, la línea recta de antes"""
        return self.pasos(a, b) if self.dist_u else math.dist(a, b)

    def observa(self, obs):
        yo = obs["yo"]; t = obs["turno"]; pos = tuple(yo["pos"]); self.cuaderno.dia = obs["dia"]; self._golpe = 0.0; self._robo = 0
        if self.juntar_viejos_v27 and obs["dia"] != self._dia_junta:          # (prompt 65) una vez al día
            self.juntados += self.cuaderno.junta(2); self._dia_junta = obs["dia"]; self._creencias = {}
        if self.sentir and self.prev is not None: (self._siente_rg if self.rg else self._siente)(obs, t)
        # (prompt 16) ¿me robó la bestia? la bolsa se vació con la bestia pegada: las comidas que llevaba (menos la que comió, dejó o dio)
        if self.prev is not None and self.prev.get("bolsa") and not obs["bolsa"]:
            b = obs.get("bestia"); cerca = self.prev.get("bestia_cerca") or (b is not None and ((self.cheb(pos, tuple(b["pos"])) <= 1) if self.dist_u else (math.dist(pos, tuple(b["pos"])) <= 1.5)))
            if cerca:
                gasto = 1 if (self.prev["accion"] in ("comer", "dejar", "dar") and self.prev.get("tipo") == "comida") else 0
                self._robo = max(0, self.prev["bolsa"].count("comida") - gasto)
        dv_ = (yo["vida"] - self.prev["vida"]) if self.prev is not None else 0.0
        # lo que hizo la acción anterior: propiocepción y, si comió, el recuerdo en el cuaderno
        if self.prev is not None:
            p = self.prev; dv = yo["vida"] - p["vida"]; dh = yo["hambre"] - p["hambre"]; dc = yo["cansancio"] - p["cansancio"]
            if p["accion"] != "comer" and dh > self.sube_max: self.sube_max = dh          # (prompt 45) lo más que ha visto subir el hambre en un turno
            if p["accion"] == "mover" and pos == p["pos"]: p["ok"] = False          # el paso no salió (casilla ocupada): no enseña lo que cansa andar
            if p["accion"] == "comer" and yo.get("_no_comio"): p["ok"] = False
            if self.aprende_v7 and p["accion"] == "comer" and obs["bolsa"].count(p.get("tipo")) >= (p.get("bolsa") or []).count(p.get("tipo")): p["ok"] = False   # (prompt 45) no salió de la bolsa: no comió (harta), no es una comida
            if p["ok"]:
                k = p["clase"] if p["accion"] != "comer" else None            # comer no enseña lo que cuesta actuar: lo que cambia es el efecto de la cosa
                if self.prop_real_v47 and yo.get("hizo") is not None:        # (prompt 93) lo que hizo de verdad: si el cuerpo la hizo dormir, es dormir
                    hz = "dormir" if yo.get("durmio") else yo["hizo"]
                    k = self.clase_de({"accion": hz}) if hz != "comer" else None
                al = CFG["propiocepcion"]["alfa"]; e = dict(self.prop.get(k) or {})
                libre = lambda v0, v1, top: 0.0 < v0 < top and 0.0 < v1 < top          # (prompt 10) ni en su tope ni en su suelo
                obsv = {}
                if libre(p["cansancio"], yo["cansancio"], self.cans_max): obsv["cans"] = dc
                if libre(p["hambre"], yo["hambre"], self.hambre_max): obsv["hambre"] = dh
                if k == "dormir" and libre(p["vida"], yo["vida"], self.vida_max): obsv["vida"] = dv
                for x, v in obsv.items(): e[x] = v if x not in e else (1 - al) * e[x] + al * v
                if k is not None: self.prop[k] = e
                if self.prop_ctx_v48 and k is not None and p.get("fase"):       # (prompt 94) lo mismo, por la hora y el sitio donde actuó
                    kc = (k, p["fase"], tuple(p["pos"]) in self.todas_casas); ec = dict(self.prop_ctx.get(kc) or {})
                    for x, v in obsv.items(): ec[x] = v if x not in ec else (1 - al) * ec[x] + al * v
                    self.prop_ctx[kc] = ec
                if p["accion"] == "comer":
                    tipo = p["tipo"]
                    if tipo == "comida": eff = -dh; imp = cuesta(p["hambre"] / self.hambre_max) - cuesta(yo["hambre"] / self.hambre_max)
                    else: eff = dv; imp = cuesta(1 - p["vida"] / self.vida_max) - cuesta(1 - yo["vida"] / self.vida_max)
                    sube = max(0.0, (self.prop.get("quedarse") or self.prop.get("otra") or {}).get("hambre", 0.0))   # lo que el hambre sube en un turno quieta (aprendido)
                    techo = (yo["vida"] >= self.vida_max) if tipo != "comida" else (yo["hambre"] <= sube + 1e-6)   # P7-7: tocar el techo (o el suelo del hambre) = «al menos»
                    if self.aprende_v7 and tipo == "comida": techo = yo["hambre"] <= self.sube_max + 1e-6           # (prompt 45) llegó a cero: no se ve cuánto quitó
                    MH = self.reglas.get("medicina_cura_heridas") if self.medicina_herida_v22 else None
                    her = max(0.0, self.vida_max - p["vida"] - self.dano_hambre) if (MH and tipo == self.botiquin) else None     # (prompt 60) la herida que tenía
                    if her is not None and eff >= her - 0.5: techo = True             # curó toda la herida que tenía: cuánto cura es «al menos»
                    if her is None or her >= 0.5:                                     # sin herida (lo que faltaba era daño del hambre) no es una cura: no se apunta
                        self.cuaderno.apunta(tipo, "valle", {"cuerpo": eff}, {"cuerpo": imp}, tick=t, al_menos=techo)
            MH = self.reglas.get("medicina_cura_heridas") if self.medicina_herida_v22 else None
            if MH:                                                          # (prompt 60) el daño del hambre que lleva: con el hambre al máximo, lo que baja la vida (hasta lo que dice la regla)
                if yo["hambre"] >= float(MH["hambre_max"]) - 1e-9 and dv < 0: self.dano_hambre += min(-dv, float(MH["dano_hambre_por_turno"]))
                self.dano_hambre = max(0.0, min(self.dano_hambre, self.vida_max - yo["vida"]))     # durmiendo se cierran primero las heridas: el daño del hambre es lo último que se recupera
            # ¿me pegó la bestia? (la vida bajó lo que pega la bestia, con ella pegada)
            gb = self.reglas.get("golpe_bestia")
            if gb and p.get("bestia_cerca") and dv <= -gb + 0.5:
                self.agresor_bestia["ultimo"] = t; self.agresor_bestia["dano"] = float(gb); self.agresor_bestia["acum"] += float(gb); self._golpe = float(gb)
            if p["accion"] == "trabajar" and p["ok"] and p.get("planta") is not None:          # (prompt 14) lo que trabajó, para apuntar su fruto
                q = tuple(p["planta"]); v = self.plantas_vistas.get(q) or {"trabajo": 0, "frutos": 0}
                w = self.trabaje.setdefault(q, {"turnos": 0, "frutos0": v["frutos"]}); w["turnos"] += 1; w["t_ult"] = t; w["trabajo_al_irse"] = v["trabajo"] + 1
        # la hermana: vista, oída, muerta
        her = next((c for c in obs["criaturas"] if c["id"] == self.hermana), None)
        if any(m["muere"] == self.hermana for m in obs.get("muertes_vistas") or []) or any(c["id"] == self.hermana for c in obs.get("cadaveres") or []):
            if not self.pareja_muerta: self.pareja_muerta = True; self.turno_saber_muerte = t
        if self.duelo_v19:                                                  # (prompt 31) se entera de cualquier muerte: la ve o ve el cuerpo
            for x in [m["muere"] for m in obs.get("muertes_vistas") or []] + [c["id"] for c in obs.get("cadaveres") or []]:
                if x != self.a and x not in self.muertas:
                    self.muertas[x] = {"t": t, "w": (self.B if x == self.hermana else self.vin.get(x, CFG["vinculo"]["escalones"][self.escalon(x)][0])), "hermana": x == self.hermana}
                    if self.duelo_v45:                                      # (prompt 90) lo que era para ella, en las tres dimensiones
                        w3 = self.lo_que_era(x); self.muertas[x]["w3"] = w3
                        rp = REPARTO["S-MUERTE-PAREJA"]; w0 = self.muertas[x]["w"]
                        self.duelos_v45.append({"t": t, "quien": x, "hermana": x == self.hermana, "w3": {k: round(v, 4) for k, v in w3.items()},
                                                "antes": {k: round(w0 * f_, 4) for k, f_ in zip(("cuerpo", "recursos", "vinculo"), rp)}})
                    self.vin.pop(x, None); self.otras.pop(x, None)
        oida = (not self.pareja_muerta) and any(o["de"] == self.hermana for o in obs.get("oido") or [])
        if self.responde and (not self.pareja_muerta or self.oye_sin_her): self.oye(obs, t, pos)
        if oida: self.ultimo_voz = t
        reciente = (not self.pareja_muerta) and (t - self.ultimo_voz) <= T["voz_ventana"]
        if her is not None and not self.pareja_muerta:
            self.B = min(1.0, self.B + 1.0 / T["roce_vista"]); self.sin_compania = 0
            self.pareja_pos = tuple(her["pos"]); self.pareja_herida = bool(her["herida"]); self.pareja_vida_nivel = her.get("vida_nivel"); self.pareja_lleva = list(her["lleva"]); self.pareja_flaca = bool(her.get("flaca"))
            if self.cara_v64 and her.get("cara") is not None: self.pareja_cara = (obs["turno"], list(her["cara"]))       # (prompt 128) su cara
        elif reciente:
            self.B = min(1.0, self.B + A.ROCE_VOZ_FRAC / T["roce_vista"]); self.sin_compania = 0
        else: self.sin_compania += 1
        self.pareja_vista = her is not None and not self.pareja_muerta; self.pareja_oida = reciente
        if self.vecinas_on: self._vive_vecinas(obs, t, pos)
        if self.aprender_mirando_v26: self._mira(obs, t)
        # la bestia
        b = obs.get("bestia")
        if b:
            d = self.lejos(pos, tuple(b["pos"])); self.dist_bestia = (self.dist_bestia + [(t, d)])[-3:]
        self.bestia = tuple(b["pos"]) if b else None
        if self.imagina_v45: self._imagina_ve(obs, t, pos, her)             # (prompt 90, pieza I) con la bestia de este turno
        if self.enfado_on: self._vive_enfado(obs, t, pos, b)
        # fuentes de botín (lo visto se recuerda; lo visto vacío se olvida), el almacén y la despensa
        V = A.VALOR_NIVEL; FN = CFG["fuentes_de_botin"]
        for c in obs["casillas"]:
            q = tuple(c["pos"])
            if "comida" in (c.get("objetos") or []): self.fuentes[q] = self.valor_fuente(FN["comida_vista"])
            elif (c.get("planta") or {}).get("frutos"): self.fuentes[q] = self.valor_fuente(FN["fruto_en_planta"])
            elif q in self.fuentes: del self.fuentes[q]
        if self.v7:
            ahora = set()
            for c in obs["casillas"]:
                if c.get("matorral") is not None: zona = c["matorral"]["zona"]; fr = c["matorral"]["frutos"]
                elif self.plantas_mat and c.get("planta") is not None: zona = "huerto"; fr = c["planta"]["frutos"]      # (prompt 21) una planta es un matorral del huerto
                else: continue
                q = tuple(c["pos"]); ahora.add(q); prev = self.mat.get(q)
                if self.memoria_v3 and prev is not None and prev["t"] < t - 1:     # (prompt 41) lo vuelve a ver: ¿tenía fruto, tanto tiempo después?
                    k_ = ("fruto" if prev["frutos"] else "vacio", self.tramo_matorral(t - prev["t"])); f_ = self.frec.setdefault(k_, [0, 0])
                    f_[0] += int(bool(fr)); f_[1] += 1
                vd = None if fr else (t if self.memoria_v2 else (prev["vacio_desde"] if prev and prev.get("vacio_desde") is not None else t))      # (prompt 40) se renueva
                if fr and prev and prev.get("vacio_desde") is not None: self.vueltas.append(t - prev["vacio_desde"])     # lo que tardó en volver a tener fruto (o menos)
                self.mat[q] = {"zona": zona, "t": t, "frutos": fr, "vacio_desde": vd}
                if fr: self.fuentes[q] = self.valor_fuente(CFG["fuentes_de_botin"]["comida_vista"])          # fruto a la vista: como comida vista (ir_objeto)
                if q not in self._mat_vista and t - self._mat_apunte.get(q, -10 ** 9) >= T["mirada"]:      # una visita: aparece a la vista
                    self.cuaderno.apunta("matorral", zona, {"recursos": 1.0 if fr else 0.0}, {"recursos": 0.0}, tick=t)["origen"] = "vivido"; self._mat_apunte[q] = t
            self._mat_vista = ahora
        for c in obs["casillas"]: self.vistas.add(tuple(c["pos"]))
        self.vistas.add(pos); self.vida_hist.append(yo["vida"])
        if len(self.vistas) != self._front_n: self._front = self.dist_a_frontera(); self._front_n = len(self.vistas)
        if obs.get("almacen") is not None: self.almacen_visto = obs["almacen"]
        if obs.get("despensa") is not None: self.despensa_vista = obs["despensa"].count("comida")
        self.obs = obs
        self.vive_sitios(obs, pos, dv_, self._golpe); self._creencias = {}
        self.amenaza5 = self.amenaza(pos)
        if self.radar_v34: self._rad_vive(obs, t, pos); self._rad_vinculos()      # (prompt 79) el radar: aprende viviendo, y el vínculo es lo aprendido

    # ── (prompt 12) la curiosidad por los sitios del cinco (cantera/paper5/curiosidad.py), traducida al valle ──
    def dist_a_frontera(self):
        """curiosidad.dist_a_frontera: BFS multi-fuente desde las casillas pisables NO vistas; en el valle, en las cuatro direcciones del paso (las del decisor)"""
        dist = {}; dq = deque()
        for q in self.pisables:
            if q not in self.vistas: dist[q] = 0; dq.append(q)
        while dq:
            p = dq.popleft(); d = dist[p] + 1
            for dx, dy in DIRS.values():
                q = (p[0] + dx, p[1] + dy)
                if q in dist or not self.M.pasa(p, q): continue
                dist[q] = d; dq.append(q)
        return dist

    def ignorancia_global(self):
        """Ojo.ignorancia_global: la fracción de casillas del valle nunca vistas (muros incluidos: un muro se ve aunque no se pise)"""
        return 1.0 - len(self.vistas) / float(self.n_arena)

    def amenaza(self, pos):
        """curiosidad.amenaza, con lo que hay en el valle: el armado es la bestia (alcance 1, el golpe a casilla pegada; cae hasta 0 en el radio de vista),
        el daño es la vida perdida en la ventana (todo lo perdido, como el cinco, que contaba todo el hp perdido) y no hay anillo. «Al menos uno»."""
        a_arm = 0.0; rg = 1.0; rv = self.obs_vista()
        dentro = bool(self.reglas.get("bestia_no_entra_en_casas")) and pos in self.todas_casas
        if self.bestia is not None and not dentro:
            d = max(abs(pos[0] - self.bestia[0]), abs(pos[1] - self.bestia[1]))
            a_arm = 1.0 if d <= rg else (0.0 if d >= rv else (rv - d) / (rv - rg))
        h = list(self.vida_hist); perdida = sum(max(0.0, h[i] - h[i + 1]) for i in range(len(h) - 1))
        a_dano = min(1.0, perdida / C5.DANO_REF)
        a_an = self.a_anillo(pos)                                           # (prompt 14, decisión 8) el anillo: lo que la cultura dice que hiere
        am = 1.0 - (1.0 - a_arm) * (1.0 - a_dano) * (1.0 - a_an)
        return max(0.0, min(1.0, am)), {"bestia": round(a_arm, 4), "dano": round(a_dano, 4), "anillo": round(a_an, 4)}

    def frontera_M(self, pos):
        """Curioso.valor, modo frontera, con la balanza: k · ignorancia global · (1 − amenaza) · (1 − g(distancia a lo no visto))"""
        d = self._front.get(pos)
        if d is None: return 0.0
        return K_FRONT * self.ignorancia_global() * (1.0 - self.amenaza5[0]) * (1.0 - C5.g_llamada(d))

    # ── (prompt 12) la curiosidad del cuánto del siete (nace_P7_29.cuanto_M), para la comida y la medicina ──
    def _rec(self, o):
        return [r for s in ((self.cuaderno.objetos.get(o) or {}).get("situaciones") or {}).values() for r in s]

    def ignorancia_cuanto(self, o):
        """CuadernoP29.ignorancia_cuanto: PESO_NEUTRO / (PESO_NEUTRO + los pesos de los recuerdos firmes, sin «al menos»)"""
        d_act = self.cuaderno.dia_actual()
        firmes = sum(self.cuaderno.peso(r, d_act) for r in self._rec(o) if not r.get("al_menos"))
        return CU.PESO_NEUTRO / (CU.PESO_NEUTRO + firmes)

    def sabido_max(self, o):
        v = [float((r.get("max_efecto") or r["efecto"])["cuerpo"]) for r in self._rec(o)]       # (prompt 65) de los juntados, el más alto
        return max(v) if v else None

    def cuanto_M(self, f, calma):
        """ACOPIO_M · calma · media, por cosa conocida, de (ignorancia del cuánto × alivio); el alivio (ALIVIO_ZURRON) solo lo da USARLA cuando lo que le falta
        (el hambre que tiene; o vida_max − vida) es más que lo más alto que ya sabe que da"""
        yo = self.obs["yo"]; partes = []
        for o, falta in (("comida", yo["hambre"]), (self.botiquin, self.vida_max - yo["vida"])):
            sab = self.sabido_max(o)
            if sab is None: continue
            al = X.ALIVIO_ZURRON if (f.get("usa") == o and falta > sab) else 1.0
            partes.append(self.ignorancia_cuanto(o) * al)
        return (X.ACOPIO_M0 * calma * sum(partes) / len(partes)) if partes else 0.0

    # ── (prompt 14) los sitios en el cuaderno, la cultura y la anticipación ──
    def terreno(self, q): return self.ley[self.T[q[1]][q[0]]]

    @staticmethod
    def dn(fase): return "noche" if fase == "noche" else "dia"

    def campo(self, objeto, k):
        """un campo de la cultura (por_turnos, retraso, empieza): lo dice el recuerdo heredado; sin cultura, None (no cambia: se guarda)"""
        ck = ("campo", objeto, k)
        if ck not in self._campos:
            self._campos[ck] = next((r[k] for r in self._rec(objeto) if k in r), None)
        return self._campos[ck]

    def cree(self, objeto, sit, dom):
        """la creencia del cuaderno (con su neutro), guardada dentro del turno: el cuaderno solo cambia en `observa`"""
        ck = (objeto, sit)
        if ck not in self._creencias: self._creencias[ck] = self.cuaderno.creencia(objeto, sit)
        c = self._creencias[ck]; return None if c is None else c[dom]

    def dano_sitio(self, ter, dn):
        """vida por turno que cree que quita estar en ese terreno (<= 0); solo con cultura (sin ella la foto no lee los sitios)"""
        if self.cultura is None: return 0.0
        v = self.cree("sitio:" + ter, dn, "cuerpo"); return min(0.0, v) if v is not None else 0.0

    def fase_en(self, k):
        """(prompt 65) la fase en que caerá el turno que está a k turnos de ahora (el reloj de dentro)"""
        fases = MUNDO_CFG["dia"]["fases"]; D = sum(n for _, n in fases); x = (int(self.obs["turno_del_dia"]) + int(k)) % D
        for nom, n in fases:
            if x < n: return nom
            x -= n
        return fases[-1][0]

    def frio_en(self, k):
        """(prompt 65) los grados de fuera a k turnos (ahora, los que se notan; luego, los de la fase en que caerá)"""
        if not self.reloj_dentro_v27 or k <= 0 or self.fase_en(k) == self.obs["fase"]: return self.obs.get("temperatura_fuera")
        return float(MUNDO_CFG["temperatura"]["fuera"][self.fase_en(k)])

    def vista_en(self, k):
        """(prompt 65) cuánto verá a k turnos (ahora, lo que ve; luego, la vista de la fase en que caerá)"""
        if not self.reloj_dentro_v27 or k <= 0 or self.fase_en(k) == self.obs["fase"]: return self.obs_vista()
        return float(MUNDO_CFG["criaturas"]["vista_por_fase"][self.fase_en(k)])

    def frio_tramo(self, k0, n, lo):
        """(prompt 65) la suma de los grados por debajo de lo en los turnos k0+1 … k0+n (por tramos de fase, sin recorrerlos uno a uno)"""
        tot = 0.0; k = k0 + 1; fin = k0 + n
        fases = MUNDO_CFG["dia"]["fases"]; D = sum(m for _, m in fases)
        while k <= fin:
            x = (int(self.obs["turno_del_dia"]) + k) % D; ini = 0
            for nom, m in fases:
                if x < ini + m: break
                ini += m
            largo = min(fin - k + 1, ini + m - x)
            tot += largo * max(0.0, lo - (self.frio_en(k) or lo)); k += largo
        return tot

    def hasta_noche(self):
        """turnos hasta que empieza la noche (0 de noche); la hora la dice la cultura"""
        emp = self.campo("bestia", "empieza")
        if emp is None: return None
        return 0 if self.obs["fase"] == "noche" else max(0, emp - self.obs["turno_del_dia"])

    def peso_noche(self):
        """lo probable que es la bestia de noche: la vida que cree que quita una noche fuera / el golpe público de la bestia;
        (prompt 16) más las comidas que cree perder en una noche fuera (el robo de la bolsa) / el objetivo de riqueza; con techo 1"""
        v = self.cree("bestia", "noche", "cuerpo"); gb = float(self.reglas.get("golpe_bestia") or 0)
        p = 0.0 if (v is None or gb <= 0) else -v / gb
        if self.robo_noche:
            r = self.cree("bestia", "noche", "recursos")
            if r is not None: p += max(0.0, -r) / self.WT
        return max(0.0, min(1.0, p))

    def anticipacion_M(self, pos):
        """F-ANTICIPACION del siete (A:975-1000) con el calendario de la noche: urgencia = 0,5 · (1 − t/horizonte); M = min(ANT_TECHO, peso · urgencia);
        en una casa, 0 (regla pública)"""
        if not self.anticipa or pos in self.todas_casas: return 0.0
        t = self.hasta_noche()
        if t is None: return 0.0
        urg = 0.5 * max(0.0, 1.0 - t / T["anticipacion_horizonte"])
        peso = self.peso_noche()
        if self.responde and self.peligro_oido: peso = max(peso, max(w for _, _, w in self.peligro_oido))     # (prompt 24) «peligro» oído de noche: empuja a casa
        return min(A.ANT_TECHO, peso * urg)

    def a_anillo(self, pos):
        """(decisión 8 de Manel) el hueco del anillo del cinco en la balanza: 1 donde la cultura dice que el sitio hiere; de noche fuera de casa, la rampa del anillo"""
        if self.cultura is None: return 0.0
        if self.dano_sitio(self.terreno(pos), self.dn(self.obs["fase"])) < 0.0: return 1.0
        t = self.hasta_noche()
        if t is None or pos in self.todas_casas or self.peso_noche() <= 0.0: return 0.0
        return max(0.0, 1.0 - t / T["anticipacion_horizonte"])

    def fuentes_sitio(self):
        """(cultura) un sitio donde cree que aparecen cosas es una fuente de botín (R-LLAMADA): valor de una cosa vista (VALOR_NIVEL) × min(1, cosas por 100 turnos);
        en la casilla de ese terreno más cercana"""
        if self.cultura is None: return {}
        out = {}; dn = self.dn(self.obs["fase"]); V = self.valor_fuente(CFG["fuentes_de_botin"]["comida_vista"])
        for ter, q in self.sitio_cerca.items():
            r = self.cree("sitio:" + ter, dn, "recursos")
            if r and r > 0: out[q] = max(out.get(q, 0.0), V * min(1.0, r))
        return out

    def escalon(self, x):
        """(prompt 28) hermana; comunidad (las del valle); otros (de fuera: hoy no hay)"""
        return "hermana" if x == self.hermana else "comunidad"

    NIVELES = ("moribunda", "muy_herida", "herida", "sana")
    VENTANA_VISTO = 3            # turnos tras el uso en que mira el cambio (el uso se nota enseguida; el siete miraba ~100 tics porque sus partes llegaban cada 25)

    def nivel_est(self, niv):
        """(prompt 64) la vida que supone a un nivel visto: el centro de su banda pública (sana desde umbral_herida; herida desde energia_fuerte_bajo; moribunda
        hasta golpe_dano; muy herida entre medias)"""
        cr = MUNDO_CFG["criaturas"]; vm = float(cr["vida_max"]); uh, eb, gd = float(cr["umbral_herida"]), float(cr["energia_fuerte_bajo"]), float(cr["golpe_dano"])
        return {"sana": (uh + vm) / 2, "herida": (eb + uh) / 2, "muy_herida": (gd + eb) / 2, "moribunda": gd / 2}.get(niv)

    def _apunta_visto(self, objeto, sit, x, t, eff, imp, al_menos, dom="cuerpo"):
        w = self.B if x == self.hermana else self.vin.get(x, CFG["vinculo"]["escalones"][self.escalon(x)][0])
        inten = (1.0 + min(1.0, abs(imp) / CU.E_INTENSIDAD)) * w             # como lo vivido, por el vínculo: nunca más
        r = {"dia": self.cuaderno.dia_actual(), "tick": t, "efecto": {d: (round(float(eff), 4) if d == dom else 0.0) for d in CU.DOMINIOS},
             "importancia": {d: (round(float(imp), 4) if d == dom else 0.0) for d in CU.DOMINIOS}, "intensidad": round(inten, 4), "creencia_antes": None,
             "al_menos": bool(al_menos), "origen": "visto", "de": x, "B": round(w, 4)}
        self.cuaderno._obj(objeto)["situaciones"].setdefault(sit, []).append(r); self._creencias = {}; self.cuaderno.version += 1
        self.vistos_log.append({"t": t, "de": x, "objeto": objeto, "sit": sit, "efecto": round(float(eff), 3), "al_menos": bool(al_menos), "peso": round(inten, 4)})
        k = objeto + "|" + sit; self.visto_stats[k] = self.visto_stats.get(k, 0) + 1

    def _descarta(self, por): k = "descartado:" + por; self.visto_stats[k] = self.visto_stats.get(k, 0) + 1

    def _mira(self, obs, t):
        """(prompt 64) aprender mirando (ver `aprender_mirando_v26`)"""
        cr = MUNDO_CFG["criaturas"]; vm = float(cr["vida_max"]); hm = float(cr["hambre_max"]); bes = obs.get("bestia"); bq = tuple(bes["pos"]) if bes else None
        objs = {tuple(c["pos"]): list(c.get("objetos") or []) for c in obs["casillas"]}
        vis = {c["id"]: c for c in obs["criaturas"] if c["id"] != self.a}
        cuenta = lambda L, tp: sum(1 for o in L if o == tp)
        robadas = set()
        if self.robos_v47:                                                  # (prompt 93) un empujón ganado que se ve: un robo de la que gana (no un regalo de la otra)
            for e in obs.get("empujones_vistos") or []:
                w = e.get("gana"); b = e["a"] if w == e["de"] else e["de"]; n_ = (e.get("soltado") or []).count("comida")
                robadas.add(b)
                if w and n_ and self.a not in (w, b) and self.radar_v34:
                    if self.robos_v49: self._rad_mira_roba_v49(w, b, n_)     # (prompt 95) con el peso de lo que se aprende mirando
                    else: self._rad_mira_roba(w, n_)
                    if self.robo_trato_v61:                                 # (prompt 115, 3) en su trato, el cuarto por mi vínculo con la robada (lo de mirando)
                        wb = self.B if b == self.hermana else self.vin.get(b, CFG["vinculo"]["escalones"][self.escalon(b)][0])
                        w_ = self._rad_win(w); w_["roba"] = w_.get("roba", 0.0) + wb; self.cuenta_v61["robos_trato_vistos"] += wb
        for x, c in vis.items():
            q = tuple(c["pos"]); niv = c.get("vida_nivel"); s0 = self.visto_snap.get(x)
            bestia_al_lado = bq is not None and self.cheb(q, bq) <= 1
            if s0 is not None and s0["t"] == t - 1:
                for tp in ("comida", self.botiquin):
                    if cuenta(s0["lleva"], tp) - cuenta(c["lleva"], tp) != 1: continue
                    cerca = [z for z in objs if self.cheb(z, q) <= 1]
                    dejada = any(cuenta(objs[z], tp) > cuenta(self._obj_prev.get(z, []), tp) for z in cerca)
                    dada = any(y != x and self.visto_snap.get(y, {}).get("t") == t - 1 and cuenta(vis[y]["lleva"], tp) > cuenta(self.visto_snap[y]["lleva"], tp) for y in vis)
                    if x in robadas: dada = False                                    # (prompt 93) la vio perderlo en un empujón: no es un regalo
                    if dada and self.radar_v34: self._rad_mira_da(x)                 # (prompt 79) ve que x da algo a otra: lo que vale x
                    if dada and self.radar_v38 and tp == self.botiquin:             # (prompt 83) y, si es medicina, lo que le pasa a la que la recibe (aprender mirando)
                        for y in vis:
                            if y != x and self.visto_snap.get(y, {}).get("t") == t - 1 and cuenta(vis[y]["lleva"], tp) > cuenta(self.visto_snap[y]["lleva"], tp):
                                self._rad["dar"].append({"x": y, "tipo": tp, "t": t, "niv0": vis[y].get("vida_nivel"), "flaca0": vis[y].get("flaca"), "mejor": vis[y].get("vida_nivel"),
                                                         "flaca_luego": vis[y].get("flaca"), "visto": True}); break
                    if dejada or dada: self._descarta("dejada_o_dada"); continue
                    self.visto_pend.append({"x": x, "tipo": tp, "t": t, "niv0": s0["niv"], "flaca0": s0["flaca"], "mejor": niv, "flaca_luego": c.get("flaca"), "visto": True, "malo": None})
                    if self.aprender_cara_v64 and s0.get("cara") is not None and c.get("cara") is not None:     # (prompt 128) su cara antes y la mejor después
                        self.visto_pend[-1]["cara0"] = s0["cara"]; self.visto_pend[-1]["cara_mejor"] = c["cara"][0]
                i0, i1 = (self.NIVELES.index(s0["niv"]) if s0["niv"] in self.NIVELES else None), (self.NIVELES.index(niv) if niv in self.NIVELES else None)
                if i0 is not None and i1 is not None and i1 < i0:                  # bajó de nivel: ¿la bestia al lado, o la zona salvaje?
                    e0, e1 = self.nivel_est(s0["niv"]), self.nivel_est(niv); imp = cuesta(1 - e1 / vm) - cuesta(1 - e0 / vm)
                    if bestia_al_lado: self._apunta_visto("bestia", "golpe_visto", x, t, e1 - e0, imp, False)
                    elif self.terreno(q) == "salvaje": self._apunta_visto("sitio:salvaje", "herida_vista", x, t, e1 - e0, imp, False)
                    obj_ = "bestia" if bestia_al_lado else ("sitio:salvaje" if self.terreno(q) == "salvaje" else None)
                    if (self.aprender_cara_v64 and obj_ and not self._vivido(obj_) and s0.get("cara") is not None and c.get("cara") is not None
                            and c["cara"][0] < s0["cara"][0]):
                        # (prompt 128, aprender_cara, acotado por Manel) solo si no lo ha vivido: cuánto se hizo daño, de su cara (su dolor de cuerpo entre el reparto
                        # de F-DANO, invertido con la cuesta), aparte de la regla de siempre
                        rd = max(REPARTO["F-DANO"]); u0 = self._inversa(cuesta, max(0.0, -s0["cara"][0]) / rd, 1.0); u1 = self._inversa(cuesta, max(0.0, -c["cara"][0]) / rd, 1.0)
                        if u1 > u0:
                            self._apunta_visto(obj_, "golpe_visto" if obj_ == "bestia" else "herida_vista", x, t, -vm * (u1 - u0), cuesta(u1) - cuesta(u0), False)
                            self.cuenta_v64["aprende_cara|" + obj_] = self.cuenta_v64.get("aprende_cara|" + obj_, 0) + 1
            self.visto_snap[x] = {"t": t, "lleva": list(c["lleva"]), "niv": niv, "flaca": c.get("flaca"), "pos": q}
            if self.aprender_cara_v64: self.visto_snap[x]["cara"] = c.get("cara")          # (prompt 128) su cara, para aprender de ella
        for p in list(self.visto_pend):
            c = vis.get(p["x"])
            if c is not None and p["t"] < t:
                q = tuple(c["pos"]); niv = c.get("vida_nivel")
                if bq is not None and self.cheb(q, bq) <= 1: p["malo"] = "bestia_al_lado"
                if niv in self.NIVELES and p["niv0"] in self.NIVELES and self.NIVELES.index(niv) < self.NIVELES.index(p["niv0"]): p["malo"] = "bajo_de_nivel"
                if niv in self.NIVELES and (p["mejor"] not in self.NIVELES or self.NIVELES.index(niv) > self.NIVELES.index(p["mejor"])): p["mejor"] = niv
                if c.get("flaca") is False: p["flaca_luego"] = False
                if "cara_mejor" in p and c.get("cara") is not None: p["cara_mejor"] = max(p["cara_mejor"], c["cara"][0])     # (prompt 128)
            if t - p["t"] < self.VENTANA_VISTO: continue
            self.visto_pend.remove(p)
            if p["malo"]: self._descarta(p["malo"]); continue
            if p["tipo"] == self.botiquin:
                if p["niv0"] == "sana": self._descarta("ya_sana_no_se_nota"); continue
                if p["niv0"] not in self.NIVELES or p["mejor"] not in self.NIVELES or self.NIVELES.index(p["mejor"]) <= self.NIVELES.index(p["niv0"]): self._descarta("no_se_nota"); continue
                e0, e1 = self.nivel_est(p["niv0"]), self.nivel_est(p["mejor"]); imp = cuesta(1 - e0 / vm) - cuesta(1 - e1 / vm)
                self._apunta_visto(self.botiquin, "valle", p["x"], p["t"], e1 - e0, imp, p["mejor"] == "sana")       # en la banda de arriba: «al menos»
            else:
                if "cara0" in p and not self._vivido("comida"):                # (prompt 128, aprender_cara, acotado por Manel) solo si no ha vivido la comida, aparte de la regla de siempre:
                    rh = max(REPARTO["F-HAMBRE"]); h0 = self._inversa(self.dh, max(0.0, -p["cara0"][0]) / rh, self.hambre_max); h1 = self._inversa(self.dh, max(0.0, -p["cara_mejor"]) / rh, self.hambre_max)
                    if h0 - h1 > 1e-6:                                          # cuánta hambre le quitó, de su cara (la de antes y su mejor cara después)
                        self._apunta_visto("comida", "valle", p["x"], p["t"], h0 - h1, cuesta(h0 / hm) - cuesta(h1 / hm), False)
                        self.cuenta_v64["aprende_cara|comida"] = self.cuenta_v64.get("aprende_cara|comida", 0) + 1
                if not (p["flaca0"] and p["flaca_luego"] is False): self._descarta("no_se_nota_comida"); continue
                h0 = float(CFG["banda_de_la_hermana"]["flaca_hambre_estimada"]); h1 = float(cr["umbral_flaca"])      # dejó de verse flaca: al menos lo que va de 80 a 60
                self._apunta_visto("comida", "valle", p["x"], p["t"], h0 - h1, cuesta(h0 / hm) - cuesta(h1 / hm), True)
        self._obj_prev = objs

    def _vive_vecinas(self, obs, t, pos):
        """(prompt 28) el vínculo con cada una: sube al verla (como con la hermana) y al darle o recibir de ella (un cuarto de su escalón); sin eso baja hacia el
        suelo con la semivida del duelo; siempre dentro de su escalón. Y lo que sabe de cada vecina (dónde está, si está flaca o herida, qué lleva)"""
        E = CFG["vinculo"]["escalones"]; baja = 0.5 ** (1.0 / T["duelo_semivida"]); vistas_ahora = set()
        for c in obs["criaturas"]:
            x = c["id"]
            if x == self.hermana: continue
            lo, hi = E[self.escalon(x)]; v = self.vin.get(x, lo); vistas_ahora.add(x)
            self.vin[x] = min(hi, v + 1.0 / T["roce_vista"])
            o = self.otras.setdefault(x, {"ayuda": None}); o.update({"pos": tuple(c["pos"]), "flaca": bool(c.get("flaca")), "herida": bool(c.get("herida")), "lleva": list(c["lleva"]), "t": t, "vida_nivel": c.get("vida_nivel")})
            if self.cara_v64 and c.get("cara") is not None: o["cara_v"] = (t, list(c["cara"]))      # (prompt 128) su cara
        for x in list(self.vin):
            if x not in vistas_ahora:
                lo, hi = E[self.escalon(x)]; self.vin[x] = lo + (self.vin[x] - lo) * baja
        lo, hi = E["hermana"]
        if not self.pareja_vista and not self.pareja_oida: self.B = lo + (self.B - lo) * baja
        self.B = min(hi, max(lo, self.B))
        # dar y recibir: el cuidado sube el vínculo un cuarto de su escalón
        p = self.prev or {}
        def sube(x):
            lo_, hi_ = E[self.escalon(x)]; paso = (hi_ - lo_) / 4.0
            if x == self.hermana: self.B = min(hi_, self.B + paso)
            else: self.vin[x] = min(hi_, self.vin.get(x, lo_) + paso)
            if self.radar_v34: self._rad_win(x)["cuidado"] += 1               # (prompt 79) el cuidado, en el trato del radar
        if p.get("accion") == "dar" and p.get("a") and len(obs["bolsa"]) < len(p.get("bolsa") or []): sube(p["a"])
        if len(obs["bolsa"]) > len(p.get("bolsa") or []) and p.get("accion") not in ("coger",) and not self._robo:
            for c in obs["criaturas"]:                                     # quien estaba pegada y lleva una cosa menos: me la ha dado
                x = c["id"]; antes = self._lleva_otras_prev.get(x)
                if antes is not None and len(c["lleva"]) < len(antes) and max(abs(c["pos"][0] - pos[0]), abs(c["pos"][1] - pos[1])) <= 1:
                    gane = any(e.get("gana") == self.a and x in (e.get("a"), e.get("de")) for e in obs.get("empujones_vistos") or [])
                    if gane:                                                    # (prompt 115/116, solo medir) mi bolsa crece porque le gané un empujón (empujara yo o ella)
                        if t - self._robada_por.get(x, -10 ** 9) <= T["mirada"]: self.cuenta_v61["regalo_recupera"] += 1
                        else: self.cuenta_v61["regalo_empuje_otro"] += 1
                        if self.robo_regalo_v61: break                         # (2, ampliado en el 116) ganar un empujón nunca es un regalo suyo: ni al robar ni al recuperar
                    self.cuenta_v61["regalo_recibido"] += 1
                    sube(x); break
        self._lleva_otras_prev = {c["id"]: list(c["lleva"]) for c in obs["criaturas"]}

    def _vive_enfado(self, obs, t, pos, b):
        """(prompt 27) nace al robarle (lo que llevaba), o a la hermana si ve el robo; se apaga si la bestia ya no lleva nada o si lleva voz_ventana turnos sin verla"""
        if b is not None: self._bestia_vista_t = t
        if self._robo > 0: self.enfado = {"t": t, "n": self._robo, "w": 1.0, "de": "yo"}; self.robada_t = t
        her = next((c for c in obs["criaturas"] if c["id"] == self.hermana), None)
        if her is not None and b is not None and not self.pareja_muerta:
            antes = self._lleva_her_prev.count("comida"); ahora = list(her["lleva"]).count("comida")
            if antes > ahora and max(abs(her["pos"][0] - b["pos"][0]), abs(her["pos"][1] - b["pos"][1])) <= 1 and (self.enfado is None or self.enfado["w"] < self.B):
                self.enfado = {"t": t, "n": antes - ahora, "w": self.B, "de": "vista"}          # ve el robo
        if her is not None: self._lleva_her_prev = list(her["lleva"])
        if self.vecinas_on and b is not None:                               # (prompt 28) ve el robo a una vecina: le llega pesado por su vínculo
            for c in obs["criaturas"]:
                x = c["id"]
                if x == self.hermana: continue
                antes = (self._lleva_vec_prev.get(x) or []).count("comida"); ahora = list(c["lleva"]).count("comida"); w = self.vin.get(x, 0.0)
                if antes > ahora and max(abs(c["pos"][0] - b["pos"][0]), abs(c["pos"][1] - b["pos"][1])) <= 1 and (self.enfado is None or self.enfado["w"] < w):
                    self.enfado = {"t": t, "n": antes - ahora, "w": w, "de": "vista_vecina", "quien": x}
        if self.vecinas_on: self._lleva_vec_prev = {c["id"]: list(c["lleva"]) for c in obs["criaturas"]}
        if self.enfado is not None:
            if (b is not None and not b.get("lleva")) or t - self._bestia_vista_t > T["voz_ventana"]: self.enfado = None

    def oye(self, obs, t, pos):
        """(prompt 24) lo que oye de la hermana: cada llamada pesa B (el vínculo); dura la mirada"""
        W = T["mirada"]; alc = float(CFG["llamadas"]["alcance_oido"])
        self.peligro_oido = [x for x in self.peligro_oido if t - x[0] <= W]
        self.comida_oida = {q: v for q, v in self.comida_oida.items() if t - v[0] <= W}
        if self.ayuda_oida and t - self.ayuda_oida[0] > W: self.ayuda_oida = None
        for o in obs.get("oido") or []:
            if "sonido" in o:                                                # (prompt 54) la expresión de otra: no es una llamada
                if self.voz_v16: self._oye_sonido(o, t)
                continue
            if self._voz_fuera and "fuerza" in o and o.get("llamada") in self._voz_fuera: continue      # (prompt 123) la voz apagada: nadie la oye; (124) solo las clases apagadas
            if "voz" in o:                                                   # (prompt 128) la voz de la base
                if self.voz_v64: self._oye_voz(o, t)
                continue
            if o["de"] != self.hermana:
                if self.vecinas_on: self._oye_vecina(obs, t, pos, o, alc)
                continue
            q = tuple(o["pos"]); ll = o["llamada"]; w = self.B; self.oidas[ll] = self.oidas.get(ll, 0) + 1
            if ll == "la_bestia": ll = "peligro"                            # (prompt 57) las llamadas prácticas, por los caminos que ya había
            if ll == "aqui_estoy": self.pareja_pos = q; continue
            if ll == "ven_lo_necesito": self.ayuda_oida = (t, q, ll, w); self.pareja_pos = q; self.ultima_ayuda_t = t; continue
            if ll == "peligro": self.peligro_oido.append((t, q, w))
            elif ll == "estoy_de_duelo" and self.duelo_v19: self.her_duelo = (t, q, w); self.pareja_pos = q          # (prompt 31) mi hermana está de duelo (por una vecina)
            elif ll == "aqui_hay_comida": self.comida_oida[q] = (t, w * max(0.0, 1.0 - ((self.pasos(pos, q) if self.dist_u else abs(q[0] - pos[0]) + abs(q[1] - pos[1]))) / alc))
            elif ll in ("necesito_ayuda", "estoy_herida"):
                self.ayuda_oida = (t, q, ll, w); self.pareja_pos = q; self.ultima_ayuda_t = t
                if self.enfado_on and ll == "necesito_ayuda" and obs.get("bestia") is not None and (obs["bestia"].get("lleva")) and (self.enfado is None or self.enfado["w"] < w):
                    self.enfado = {"t": t, "n": max(1, self._lleva_her_prev.count("comida")), "w": w, "de": "oida"}     # (prompt 27) la oye pedir ayuda con la bestia (y lo robado) a la vista
                if ll == "necesito_ayuda": self.pareja_flaca = True
                else: self.pareja_herida = True
        vistas = {tuple(c["pos"]) for c in obs["casillas"]}
        for q in [q for q in self.comida_oida if q in vistas]: del self.comida_oida[q]          # el sitio ya se ve: manda lo que ve
        if self.ayuda_oida and self.pareja_vista and self.pareja_pos and max(abs(self.pareja_pos[0] - pos[0]), abs(self.pareja_pos[1] - pos[1])) <= 1: self.ayuda_oida = None   # ha llegado

    def _oye_voz(self, o, t):
        """(prompt 128) la voz de la base, oída. El peso: su tamaño (el cuánto) por lo que vale para mí (peso_dar, en las filas). Alarma por la bestia: como
        «la bestia» de antes (un peligro donde llamó); alarma por dolor o peligro: como su dolor oído (lo que hoy hace el dolor fuerte de la expresión).
        Petición: me pide comida o cura (y cuánto). Contacto: su soledad. «Para»: si va a mí, nada más; si es de mi casa, una petición de acudir"""
        x = o["de"]; q = tuple(o["pos"]); cl = o.get("voz"); h_ = x == self.hermana
        if h_ and self.pareja_muerta: return
        w = self.B if h_ else self.vin.get(x, CFG["vinculo"]["escalones"][self.escalon(x)][0]); cu = float(o.get("cuanto") or 0.0)
        self.cuenta_v64["oye|" + str(cl)] = self.cuenta_v64.get("oye|" + str(cl), 0) + 1
        d = None if h_ else self.otras.setdefault(x, {"ayuda": None, "lleva": [], "flaca": False, "herida": False})
        if h_: self.pareja_pos = q
        else: d["pos"] = q; d["t"] = t
        if cl == "alarma":
            if o.get("objeto") == "bestia": self.peligro_oido.append((t, q, w))
            else:
                rec = (t, q, w)
                if h_: self.her_duelo = rec
                else: d["duelo"] = rec
        elif cl in ("peticion", "para"):
            if cl == "para" and (o.get("a") == self.a or x[0] != self.a[0]): return      # el «para» a mí: nada más; el de otra casa: no es de los míos
            rec = (t, q, "peticion:" + str(o.get("objeto")) if cl == "peticion" else "para", w, cu)
            if self.cara_dar_v65 and cl == "peticion": self.pide_v65[x] = (t, o.get("objeto"), cu)      # (prompt 130) lo que me pide y cuánto
            if h_: self.ayuda_oida = rec; self.ultima_ayuda_t = t
            else: d["ayuda"] = rec; self.ultima_ayuda_t = t
        elif cl == "contacto":
            rec = (t, q, cu, w)
            if h_: self.her_contacto = rec
            else: d["contacto"] = rec

    def _oye_vecina(self, obs, t, pos, o, alc):
        """(prompt 28) las llamadas de una vecina, con su vínculo: «peligro», «aquí hay comida», «necesito ayuda» / «estoy herida» (y el enfado si es tras un robo)"""
        x = o["de"]; q = tuple(o["pos"]); ll = o["llamada"]; w = self.vin.get(x, CFG["vinculo"]["escalones"][self.escalon(x)][0])
        self.oidas["vecina:" + ll] = self.oidas.get("vecina:" + ll, 0) + 1
        if ll == "la_bestia": ll = "peligro"                                # (prompt 57)
        if ll == "aqui_estoy":
            d = self.otras.setdefault(x, {"ayuda": None, "lleva": [], "flaca": False, "herida": False}); d["pos"] = q; d["t"] = t; return
        if ll == "ven_lo_necesito":
            d = self.otras.setdefault(x, {"ayuda": None, "lleva": [], "flaca": False, "herida": False}); d["ayuda"] = (t, q, ll, w); d["pos"] = q; d["t"] = t; self.ultima_ayuda_t = t; return
        if ll == "peligro": self.peligro_oido.append((t, q, w))
        elif ll == "estoy_de_duelo" and self.duelo_v19:                    # (prompt 31) una vecina está de duelo: lo sé como sé que está herida
            d = self.otras.setdefault(x, {"ayuda": None, "lleva": [], "flaca": False, "herida": False}); d["duelo"] = (t, q, w); d["pos"] = q; d["t"] = t
        elif ll == "aqui_hay_comida":
            v = w * max(0.0, 1.0 - ((self.pasos(pos, q) if self.dist_u else abs(q[0] - pos[0]) + abs(q[1] - pos[1]))) / alc)
            if v > self.comida_oida.get(q, (0, 0.0))[1]: self.comida_oida[q] = (t, v)
        elif ll in ("necesito_ayuda", "estoy_herida"):
            d = self.otras.setdefault(x, {"ayuda": None, "lleva": [], "flaca": False, "herida": False}); d["ayuda"] = (t, q, ll, w); d["pos"] = q; d["t"] = t; self.ultima_ayuda_t = t
            if ll == "necesito_ayuda": d["flaca"] = True
            else: d["herida"] = True
            if self.enfado_on and ll == "necesito_ayuda" and obs.get("bestia") is not None and obs["bestia"].get("lleva") and (self.enfado is None or self.enfado["w"] < w):
                self.enfado = {"t": t, "n": max(1, (d.get("lleva") or []).count("comida")), "w": w, "de": "oida_vecina", "quien": x}

    def necesidad_vecina(self, x, d):
        """(prompt 28) si una vecina necesita algo que yo podría darle (flaca, herida o me ha pedido ayuda), con lo que sé de ella hace poco"""
        t = self.obs["turno"]
        if t - d.get("t", -10 ** 9) > T["mirada"]: return False
        return bool(d.get("flaca") or d.get("herida") or (d.get("ayuda") and t - d["ayuda"][0] <= T["mirada"]) or (self.duelo_v19 and self.duelo_oido(d.get("duelo")) > 0))

    # ── (prompt 31) el duelo ──
    def duelo_dura(self, semivida):
        """cuánto dura un duelo: hasta que lo que queda por encima del suelo baja de `dura_hasta` (después queda el dolor latente, el suelo)"""
        return semivida * math.log2(1.0 / float(CFG["duelo"]["dura_hasta"]))

    def semivida_duelo(self, hermana):
        return float(T["duelo_semivida"]) if hermana else float(CFG["duelo"]["semivida_vecina"])

    def duelo_propio(self, t):
        """el mayor de mis duelos (por la hermana, con su vínculo B; por una vecina, con el suyo y su semivida, más corta); y si alguno sigue vivo (no solo latente)"""
        g = 0.0; vivo = False
        for x, m in self.muertas.items():
            sv = self.semivida_duelo(m["hermana"]); dt = max(0.0, t - m["t"])
            g = (g + duelo(dt, sv, m["w"])) if self.duelo_suma_v15 else max(g, duelo(dt, sv, m["w"])); vivo = vivo or dt < self.duelo_dura(sv)
        return g, vivo

    def atencion(self, t=None):
        """(prompt 32) la atención a las cosas: 1 − lo fresco del duelo más fuerte (vínculo × 0,5^(dt/semivida), la parte que se va pasando), entre 0 y 1"""
        t = self.obs["turno"] if t is None else t; fresca = 0.0
        if self.atencion_huida and (self.bestia is not None or any(x[0] == t for x in self.peligro_oido)): return 1.0
        for m in self.muertas.values():
            fresca = max(fresca, m["w"] * 0.5 ** (max(0.0, t - m["t"]) / self.semivida_duelo(m["hermana"])))
        return max(0.0, 1.0 - fresca)

    @staticmethod
    def es_cosa(acc):
        """(prompt 32) ir a por cosas: buscar comida, ir a matorrales y plantas, trabajar, explorar (y coger lo que tiene al lado)"""
        return acc.get("accion") == "coger" or acc.get("accion") == "trabajar" or acc.get("que") in CFG["duelo"]["ir_a_por_cosas"]

    LLAMADAS_VOZ = ("aqui_estoy", "aqui_hay_comida", "la_bestia", "ven_lo_necesito")

    def _p_llamada(self, tipo):
        """(prompt 57) lo que espera: que venga alguien cuando hace esta llamada; la frecuencia vivida, desde lo que dice la cultura (con el peso neutro)"""
        h, n = self.llam_frec.get(tipo, (0, 0)); p0 = self.campo("llamar", "viene"); p0 = 0.5 if p0 is None else float(p0)
        p1 = (p0 * CU.PESO_NEUTRO + h) / (CU.PESO_NEUTRO + n)
        if not self.llamadas_contraste_v20: return p1
        h0, n0 = self.llam_ctrl.get(tipo, (0, 0)); pc = h0 / (CU.PESO_NEUTRO + n0)          # (prompt 58) sin llamar: desde 0, con el peso neutro
        return max(0.0, p1 - pc)

    def _aprende_llamadas(self, obs):
        """(prompt 57) ¿vino alguien? alguna de las que estaban a más de una casilla al llamar, ahora a su lado, dentro de la mirada"""
        t = obs["turno"]; pos = tuple(obs["yo"]["pos"]); cerca = {c["id"] for c in obs["criaturas"] if max(abs(c["pos"][0] - pos[0]), abs(c["pos"][1] - pos[1])) <= 1}
        for p_ in list(self.llam_pend):
            vino = bool(cerca & p_["kin"])
            if vino or t - p_["t"] > T["mirada"]:
                f_ = (self.llam_ctrl if p_.get("control") else self.llam_frec).setdefault(p_["tipo"], [0, 0]); f_[0] += int(vino); f_[1] += 1; self.llam_pend.remove(p_)

    def _elige_llamada(self, obs, acc):
        """(prompt 57) cada llamada que sea verdad ahora, con cada fuerza que llegue a alguna de las suyas que sabe dónde está: su foto es la de lo que hace,
        con lo que pasaría si viene alguien (la compañía; si pide ayuda, lo que lleve la otra: comer, curarse; si avisa de comida, el hambre de las que la
        necesitan; si avisa de la bestia, el peligro de las suyas junto a ella), por lo que espera que venga, más lo que cansa gritar. Llama si sale mejor"""
        self._aprende_llamadas(obs)
        t = obs["turno"]; pos = tuple(obs["yo"]["pos"]); LV = self.reglas.get("llamadas_voz")         # hasta dónde llega cada fuerza y lo que cansa (regla pública)
        if not LV: return None
        a0 = dict(self.dest["acc"]) if (acc.get("_ir") and self.dest) else {k: v for k, v in acc.items() if not k.startswith("_") and k not in ("suena", "llama")}
        try: f0 = self.foto(a0); F0 = self.filas(f0)
        except Exception: return None
        _, d0 = self._compone(F0)
        kin = []
        if not self.pareja_muerta and self.pareja_pos is not None: kin.append((self.hermana, tuple(self.pareja_pos), self.pareja_lleva))
        kin += [(x, tuple(d["pos"]), d.get("lleva") or []) for x, d in self.otras.items() if d.get("pos") and t - d.get("t", -10 ** 9) <= T["mirada"] and x not in self.muertas]
        ve_comida = any("comida" in (c.get("objetos") or []) or (c.get("matorral") or {}).get("frutos") or (c.get("planta") or {}).get("frutos") for c in obs["casillas"])
        mejor = None; posibles = {}
        for fz, alc in LV["alcance"].items():
            alcan = [(x, q, ll) for x, q, ll in kin if 1 < self.cheb(pos, q) <= alc]
            if not alcan: continue
            for tipo in self.LLAMADAS_VOZ:
                if tipo in self._voz_fuera: continue                          # (prompt 124) esa clase apagada: no se emite
                if tipo == "la_bestia" and self.bestia is None: continue          # no miente: solo lo que es verdad
                if tipo == "aqui_hay_comida" and not ve_comida: continue
                Fc = dict(F0); Fc["S-SOLEDAD"] = 0.0; Fc["S-COMPANIA"] = 0.0     # si viene alguien: la compañía
                if self.escala_v6 and self.rg_gan and any(x == self.hermana for x, _, _ in alcan): Fc["V-VINCULO"] = CFG["vivir_bien"]["reposo_dos"]["vinculo"] * self.B
                if tipo == "ven_lo_necesito":
                    if any("comida" in ll for _, _, ll in alcan) and f0["hambre"] > 0: Fc["F-HAMBRE"] = self.dh(max(0.0, f0["hambre"] - self.cree_comida(max(1.0, f0["hambre"]))))
                    if any(self.botiquin in ll for _, _, ll in alcan) and f0["vida"] < self.vida_max:
                        cura = self.cuaderno.creencia_cuerpo(self.botiquin, "valle") or 0.0
                        Fc["F-DANO"] = cuesta((self.vida_max - min(self.vida_max, f0["vida"] + max(0.0, cura))) / self.vida_max)
                elif tipo == "aqui_hay_comida":
                    if any(self.necesita(x, "comida") for x, _, _ in alcan): Fc["R-HERMANO-FALTA"] = 0.0
                elif tipo == "la_bestia": Fc["F-HERMANO-AMENAZA"] = 0.0
                F0_, d0_ = F0, d0
                if tipo == "la_bestia" and self.alarma_zona_v20:              # (prompt 58) el peligro de las suyas: la zona que la bestia alcanza en la mirada
                    zona = max(1.0, float(self.reglas.get("bestia_pasos_por_turno") or 1) * T["mirada"]); pel = 0.0
                    for x, q, _ in alcan:
                        w = self.peso_kin(x)
                        pel = max(pel, w * A.ALCANCE_TECHO * max(0.0, 1.0 - max(0.0, self.cheb(q, self.bestia) - 1.0) / zona))
                    F0_ = dict(F0); F0_["F-HERMANO-AMENAZA"] = max(F0.get("F-HERMANO-AMENAZA", 0.0), pel); _, d0_ = self._compone(F0_)
                p = self._p_llamada(tipo)
                Fm = {k: (1 - p) * F0_.get(k, 0.0) + p * Fc.get(k, 0.0) for k in set(F0_) | set(Fc)}
                Fm["F-CANSANCIO"] = Fm.get("F-CANSANCIO", 0.0) + LV["cansancio"].get(fz, 0.0) / self.cans_max
                _, d = self._compone(Fm)
                posibles.setdefault(tipo, set()).update(x for x, _, _ in alcan)
                if d < d0_ - 1e-9 and (mejor is None or d - d0_ < mejor[0]): mejor = (d - d0_, tipo, fz, {x for x, _, _ in alcan})
        if self.llamadas_contraste_v20:                                     # (prompt 58) las que pudo hacer y no hizo: el control, en una situación parecida
            for tp, ks in posibles.items():
                if (mejor is None or tp != mejor[1]) and not any(p_["tipo"] == tp and p_.get("control") for p_ in self.llam_pend):
                    self.llam_pend.append({"tipo": tp, "t": t, "kin": set(ks), "control": True})
        if mejor is None: return None
        _, tipo, fz, quien = mejor
        if not any(p_["tipo"] == tipo and not p_.get("control") for p_ in self.llam_pend): self.llam_pend.append({"tipo": tipo, "t": t, "kin": quien})
        self.llam_hechas.append({"t": t, "tipo": tipo, "fuerza": fz, "bestia": self.bestia is not None, "cerca": len(quien), "vida": obs["yo"]["vida"], "hambre": round(obs["yo"]["hambre"], 1)})
        return {"llamada": tipo, "fuerza": fz}

    INTENSIDADES = ("suave", "medio", "fuerte")
    FUERZA = {"pF": "placer", "nF": "dolor", "pR": "alegria", "nR": "enfado", "pS": "amor", "nS": "tristeza"}

    def _compone(self, F):
        """(prompt 67) lo que vale una foto: con el motor (`compone`) o, en el valorador de sumas, la suma (`compone_sumas`)"""
        if self.posicion_v30: return compone_posicion(F, self.satura_v8, self._rep)          # (prompt 72) P32; (103) con su reparto
        return compone_sumas(F, self._rep) if self.sumas_v29 else compone(F, self.satura_v8, self.sin_techo_v11, self._rep)

    def _expresion(self):
        """(prompt 54) la fuerza que más pesa en su estado de ahora y su intensidad (tercios de la mitad del techo de volumen); (prompt 67) una vez por turno"""
        if self.rapido_v28:
            t = self.obs["turno"]
            if self._ex is None or self._ex[0] != t: self._ex = (t, self._expresion_calc())
            return self._ex[1]
        return self._expresion_calc()

    def _expresion_calc(self):
        _, Fa = self.seis_ahora(); st, _ = self._compone(Fa)
        k = max(self.FUERZA, key=lambda x: (getattr(st, x), x)); v = getattr(st, k); u = VOL_MAX / 6.0
        return self.FUERZA[k], ("suave" if v < u else "medio" if v < 2 * u else "fuerte")

    def _oye_sonido(self, o, t):
        """(prompt 54) lo que se oye cuenta como lo que se ve, solo para la tristeza y el dolor del cuerpo: como si la viera de duelo o herida, por el vínculo y
        por lo fuerte que suena (un tercio, dos tercios o entero). Si suena otra cosa, ya no está así"""
        x = o["de"]; q = tuple(o["pos"]); h_ = x == self.hermana
        if h_ and self.pareja_muerta: return
        k = (self.INTENSIDADES.index(o.get("intensidad", "suave")) + 1) / 3.0
        rec = None
        if o.get("sonido") in ("tristeza", "dolor"):
            w = self.B if h_ else self.vin.get(x, CFG["vinculo"]["escalones"][self.escalon(x)][0]); rec = (t, q, w * k)
        if h_: self.her_duelo = rec; self.pareja_pos = q
        else:
            d = self.otras.setdefault(x, {"ayuda": None, "lleva": [], "flaca": False, "herida": False}); d["duelo"] = rec; d["pos"] = q; d["t"] = t

    def duelo_oido(self, du):
        """lo que siento del duelo de otra (oí «estoy de duelo»): su dolor como propio, pesado por el vínculo, mientras le dura (no sé por quién: el de la hermana)"""
        if not du: return 0.0
        dt = max(0.0, self.obs["turno"] - du[0]); sv = self.semivida_duelo(True)
        return duelo(dt, sv, du[2]) if dt < self.duelo_dura(sv) else 0.0

    def alivio(self, pos, quien=None, sin=None):
        """la compañía alivia: pegada a una de las suyas, el dolor baja como baja el de la hermana con la medicina al lado (MEDICINA_ATEN), en proporción al vínculo"""
        mejor = 0.0
        cerca = [(self.hermana, self.pareja_pos, self.B)] if not self.pareja_muerta else []
        cerca += [(x, d.get("pos"), self.vin.get(x, 0.0)) for x, d in self.otras.items() if self.obs["turno"] - d.get("t", -10 ** 9) <= T["mirada"]]
        for x, q, w in cerca:
            if q is None or (quien is not None and x != quien) or x == sin: continue          # (prompt 47) la muerta no alivia su propio duelo
            if self.cheb(pos, q) <= 1: mejor = max(mejor, w if quien is None else 1.0)
        return 1.0 - (1.0 - A.MEDICINA_ATEN) * mejor

    def ayuda_reciente(self):
        return self.ayuda_oida is not None

    def p_fruto(self, zona):
        """(v7) la probabilidad de encontrar fruto en un matorral de esa zona, según el cuaderno (si de esa zona no sabe nada, lo del bosque: un matorral es un matorral)"""
        v = self.cree("matorral", zona, "recursos")
        if v is None and zona != "bosque": v = self.cree("matorral", "bosque", "recursos")
        return max(0.0, min(1.0, v or 0.0))

    def tarda_en_volver(self):
        """(prompt 21) lo que tarda un matorral visto vacío en volver a tener fruto, de su propio recuerdo: la media de lo que ha visto, con un día como
        recuerdo de partida de peso 1 (como el neutro del cuaderno). El día lo saca de la cultura (lo que tarda el fruto del huerto / sus días)"""
        r, rd = self.campo("trabajar", "retraso"), self.campo("trabajar", "retraso_dias")
        dia = (r / rd) if (r and rd) else float(self.obs["turno"] - self.obs["turno_del_dia"] or 1)
        return (dia + sum(self.vueltas)) / (1.0 + len(self.vueltas))

    def p_matorral(self, q):
        """la probabilidad de encontrar fruto en un matorral (o planta) recordado: la del cuaderno; si lo vio vacío hace poco, rebajada por lo que tarda en volver"""
        m = self.mat[q]
        if self.memoria_v3:                                                 # (prompt 41) «puede haber fruto»: la frecuencia vivida en ese tramo, desde la cultura
            h, n = self.frec.get(("fruto" if m["frutos"] else "vacio", self.tramo_matorral(self.obs["turno"] - m["t"])), (0, 0))
            return (self.p_cultura_matorral() * CU.PESO_NEUTRO + h) / (CU.PESO_NEUTRO + n)
        if self.memoria_v2:                                                 # (prompt 40) solo el tiempo desde que lo vio y lo que tarda en volver a dar fruto
            tau = max(1.0, self.tarda_en_volver()); dt = self.obs["turno"] - m["t"]
            if not m["frutos"]: return min(1.0, dt / tau)                   # visto vacío: el fruto vuelve en lo que tarda
            return 1.0 - dt / tau if dt < tau else min(1.0, (dt - tau) / tau)       # visto con fruto: se acaba en un ciclo (alguien se lo come, se pudre) y luego vuelve
        p = self.p_fruto(m["zona"])
        if self.recuerdo_vacio and m.get("vacio_desde") is not None:
            p *= min(1.0, (self.obs["turno"] - m["vacio_desde"]) / max(1.0, self.tarda_en_volver()))
        return p

    def tramo_matorral(self, dt):
        """(prompt 41) los tramos de tiempo desde que lo vio: un cuarto de día, un día, dos y cuatro (el día, de la cultura)"""
        r, rd = self.campo("trabajar", "retraso"), self.campo("trabajar", "retraso_dias")
        dia = (r / rd) if (r and rd) else 400.0
        for i, f in enumerate(CFG["memoria_matorrales"]["tramos_en_dias"]):
            if dt < f * dia: return i
        return len(CFG["memoria_matorrales"]["tramos_en_dias"])

    def p_cultura_matorral(self):
        """lo que dice la cultura de encontrar fruto en un matorral (el recuerdo heredado: «los matorrales del bosque dan fruto»)"""
        if not hasattr(self, "_p_cult"):
            e = next((x for x in (self.cultura or {}).get("entradas", []) if x.get("objeto") == "matorral"), None)
            self._p_cult = float((e or {}).get("efecto", {}).get("recursos", 0.5))
        return self._p_cult

    def plantas_por_trabajar(self):
        N = self.campo("trabajar", "por_turnos")
        if N is None: return []
        return [q for q, v in self.plantas_vistas.items() if v["trabajo"] < N]

    def promesa_trabajo(self, q, k):
        """(prompt 14) la promesa sellada del siete aplicada al huerto: el fruto que dice el cuaderno (comidas por turno × los turnos que pide), rebajado por el
        tiempo que tarda (OLVIDO ^ días) y por la parte del trabajo que falta que hace en la foto; es lo que suma a W (R-CARENCIA)"""
        N = self.campo("trabajar", "por_turnos"); ret = self.campo("trabajar", "retraso_dias"); c = self.cree("trabajar", "huerto", "recursos")
        if not N or c is None or c <= 0: return 0.0
        falta = max(0, N - self.plantas_vistas[q]["trabajo"])
        if falta <= 0: return 0.0                                          # servida: la planta ya tiene su trabajo
        return c * N * (CU.OLVIDO ** float(ret or 0)) * min(1.0, k / falta)

    def junto_a(self, q):
        """casillas pisables pegadas a la planta q (desde ahí se trabaja)"""
        return [(q[0] + dx, q[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and self.M.pasa((q[0] + dx, q[1] + dy), (q[0] + dx, q[1] + dy))]

    def apunta_estancia(self, key, t):
        a = self.acum.pop(key); ter, dn = key; n = a["n"]
        imp = cuesta((self.vida_max - a["vida1"]) / self.vida_max) - cuesta((self.vida_max - a["vida0"]) / self.vida_max)
        r = self.cuaderno.apunta("sitio:" + ter, dn, {"cuerpo": -a["perdida"] / n, "recursos": sum(a["da"].values()) * 100.0 / n}, {"cuerpo": imp}, tick=t)
        r["da"] = {k: round(v * 100.0 / n, 4) for k, v in a["da"].items()}; r["origen"] = "vivido"; r["turnos"] = n

    def vive_sitios(self, obs, pos, dv, golpe_bestia):
        """lo vivido de los sitios, de la noche y del trabajo, al cuaderno (siempre; solo se LEE con cultura)"""
        t = obs["turno"]; yo = obs["yo"]; dn = self.dn(obs["fase"]); key = (self.terreno(pos), dn)
        # cosas que aparecen a la vista (comida y medicina en el suelo, vistas por primera vez en su casilla)
        ahora = set()
        for c in obs["casillas"]:
            for o in set(c.get("objetos") or []):
                if o in ("comida", "medicina"): ahora.add((tuple(c["pos"]), o))
        vistas_casillas = {tuple(c["pos"]) for c in obs["casillas"]}
        nuevas = [x for x in ahora if x not in self.items_vistos]
        self.items_vistos = {x for x in self.items_vistos if x[0] not in vistas_casillas} | ahora
        self.medicinas = {x[0] for x in self.items_vistos if x[1] == "medicina"}
        # la estancia (se cierra al cambiar de terreno o de parte del día si lleva >= 5 turnos, y cada `mirada` turnos)
        for k in list(self.acum):
            if k != key and self.acum[k]["n"] >= 5: self.apunta_estancia(k, t)
        a = self.acum.setdefault(key, {"n": 0, "perdida": 0.0, "da": {}, "vida0": yo["vida"], "vida1": yo["vida"]})
        a["n"] += 1; a["vida1"] = yo["vida"]
        if dv < 0 and not golpe_bestia and (self.prev or {}).get("hambre", 0) < self.hambre_max: a["perdida"] += -dv
        for _, o in nuevas: a["da"][o] = a["da"].get(o, 0) + 1
        if a["n"] >= T["mirada"]: self.apunta_estancia(key, t)
        # la noche: al acabar, si pasó fuera de una casa al menos la mitad, apunta lo que le hizo la bestia
        if dn == "noche":
            self.noche["turnos"] += 1; self.noche["fuera"] += int(pos not in self.todas_casas); self.noche["dano"] += float(golpe_bestia or 0); self.noche["robo"] += self._robo
            durmio_ = (self.prev or {}).get("accion") == "dormir" if not (self.noches_v47 and yo.get("durmio") is not None) else bool(yo.get("durmio"))      # (prompt 93) lo que hizo de verdad
            if durmio_: self.noche["duerme"] = self.noche.get("duerme", 0) + 1; self.noche["duerme_casa"] = self.noche.get("duerme_casa", 0) + int(pos in self.todas_casas)
            if self.noche_perdida_v49 and durmio_ and dv < 0:              # (prompt 95) la vida que pierde dormida, sea por lo que sea, según dónde duerme
                kk = "perdida_casa" if pos in self.todas_casas else "perdida_fuera"; self.noche[kk] = self.noche.get(kk, 0.0) - dv
        elif self.fase_prev == "noche":
            if self.noche["fuera"] * 2 >= max(1, self.noche["turnos"]):
                imp = {"cuerpo": cuesta(min(1.0, self.noche["dano"] / self.vida_max))}
                if self.robo_noche: imp["recursos"] = min(1.0, self.noche["robo"] / self.WT)          # (prompt 16) lo que la movió perder la bolsa
                self.cuaderno.apunta("bestia", "noche", {"cuerpo": -self.noche["dano"], "recursos": -self.noche["robo"]}, imp, tick=t)["origen"] = "vivido"
            if (self.dormir_en_casa or self.noches_v47) and self.noche.get("duerme", 0) * 2 >= max(1, self.noche["turnos"]):      # (prompt 22) una noche dormida: dónde y qué le pasó; (93) siempre
                sit = "casa" if self.noche.get("duerme_casa", 0) * 2 >= self.noche["duerme"] else "fuera"
                dn_ = self.noche.get("perdida_" + sit, 0.0) if self.noche_perdida_v49 else self.noche["dano"]      # (prompt 95) toda la vida que perdió dormida allí
                self.cuaderno.apunta("dormir", sit, {"cuerpo": -dn_}, {"cuerpo": cuesta(min(1.0, dn_ / self.vida_max))}, tick=t)["origen"] = "vivido"
            self.noche = {"turnos": 0, "fuera": 0, "dano": 0.0, "robo": 0}
        self.fase_prev = obs["fase"]
        # el huerto: lo que vio de cada planta, y el fruto de lo que trabajó (frutos vistos después / sus turnos; 0 si el ciclo pasó sin fruto o a los 2 ciclos)
        for c in obs["casillas"]:
            if c.get("planta") is not None: self.plantas_vistas[tuple(c["pos"])] = {"trabajo": c["planta"]["trabajo"], "frutos": c["planta"]["frutos"], "t": t}
        ciclo = self.campo("trabajar", "retraso")                          # sin cultura no sabe cuánto tarda: solo cierra con lo que ve
        for q in list(self.trabaje):
            w = self.trabaje[q]; v = self.plantas_vistas.get(q)
            fruto = None
            if v is not None and v["t"] == t and t > w["t_ult"]:
                if v["frutos"] > w["frutos0"]: fruto = (v["frutos"] - w["frutos0"]) / w["turnos"]
                elif v["trabajo"] < w["trabajo_al_irse"]: fruto = 0.0
            if fruto is None and ciclo and t - w["t_ult"] > 2 * ciclo: fruto = 0.0
            if fruto is not None:
                self.cuaderno.apunta("trabajar", "huerto", {"recursos": fruto}, {"recursos": 0.0}, tick=t)["origen"] = "vivido"; del self.trabaje[q]
        # el sitio más cercano de cada terreno (para las fuentes de la cultura)
        if self.cultura is not None:
            if self.dist_u:                                                 # (prompt 30) el más cercano andando
                Dp = self._dist_a(pos); self.sitio_cerca = {ter: min(L, key=lambda c: (Dp.get(c, 999), c)) for ter, L in self.celdas_de.items() if ter in ("bosque", "salvaje")}
            else: self.sitio_cerca = {ter: min(L, key=lambda c: (abs(c[0] - pos[0]) + abs(c[1] - pos[1]), c)) for ter, L in self.celdas_de.items() if ter in ("bosque", "salvaje")}

    # ── las filas, sobre una foto (lo que hay, o lo que imagina el cuerpo que habrá) ──
    def filas(self, f):
        if self.imagina_v45 and f.get("H", 0) > 0 and self._her_pred is not None and not self.pareja_muerta:
            t = self.obs["turno"]                                           # (prompt 90, pieza I) en la foto, la hermana donde estará; el ahora, donde está
            if self.rg and self.rg_gan and self._F_ahora[0] != t: self._F_ahora = (t, self._filas_rg(self.foto_ahora(), ganancias=False))
            p0 = self.pareja_pos; self.pareja_pos = tuple(self._her_pred); self.imagina_v45 = False
            try: return self.filas(f)
            finally: self.pareja_pos = p0; self.imagina_v45 = True
        if self.bestia_v44 and f.get("sin_bestia") and self.bestia is not None and ((self.obs.get("bestia") or {}).get("id") in (None, f["sin_bestia"])):
            t = self.obs["turno"]                                           # (prompt 89) la foto sin la bestia que echa o mata: sin sus peligros
            if self.rg and self.rg_gan and self._F_ahora[0] != t: self._F_ahora = (t, self._filas_rg(self.foto_ahora(), ganancias=False))     # el ahora, con ella
            b0 = self.bestia; self.bestia = None
            try: return self._filas_rg(f) if self.rg else self._filas_orig(f)
            finally: self.bestia = b0
        if self.rg: return self._filas_rg(f)
        return self._filas_orig(f)

    # ── (prompt 90) pieza I: imaginar que la hermana se mueve ──
    def _sit_her(self, obs, t):
        """la situación de la hermana, como se ve desde fuera (la bestia cerca de ella: a la vista de la fase)"""
        bc = self.bestia is not None and self.pareja_pos is not None and self.cheb(self.bestia, self.pareja_pos) <= self.vista_en(0)
        return situacion_de(self.pareja_flaca, self.pareja_herida, bc, obs["fase"], t - self._llamada_t <= T["mirada"])

    def p_costumbre(self, sit):
        """lo que suele hacer en esa situación: (lo de la cultura × peso neutro + veces) / (peso neutro + vistas), como los matorrales (memoria v3)"""
        I = CFG["imaginar_v45"]; n = self.costumbre.get(sit) or {}; tot = sum(n.values()); noche = "|dia|" not in sit
        pc = {k: ((float(I["a_casa_de_noche"]) if k == "casa" else (1.0 - float(I["a_casa_de_noche"])) / (len(COSTUMBRES) - 1)) if noche else 1.0 / len(COSTUMBRES)) for k in COSTUMBRES}
        return {k: (pc[k] * CU.PESO_NEUTRO + n.get(k, 0)) / (CU.PESO_NEUTRO + tot) for k in COSTUMBRES}

    def _anda(self, p, D, H):
        """H pasos por el camino más corto bajando por el mapa de distancias D"""
        for _ in range(H):
            sig = min((q for q in ((p[0] + dx, p[1] + dy) for dx, dy in DIRS.values()) if q in D and self.M.pasa(p, q)), key=lambda q: (D[q], q), default=None)
            if sig is None or D[sig] >= D.get(p, 10 ** 9): break
            p = sig
        return p

    def _imagina_ve(self, obs, t, pos, her):
        """(b) aprende su costumbre con cada paso que le ve dar (dos turnos seguidos a la vista); (a)+(c) dónde estará al acabar la mirada"""
        if any(o.get("llamada") and o.get("de") != self.hermana for o in obs.get("oido") or []): self._llamada_t = t
        self._her_pred = None
        if her is None or self.pareja_muerta: self._her_ant = None; return
        q = tuple(her["pos"]); sit = self._sit_her(obs, t)
        if self._her_ant is not None and self._her_ant[1] == t - 1:
            k = clase_paso(self.M, self.casa_celdas, self._her_ant[0], q, pos, self.bestia)
            if k is not None:
                d = self.costumbre.setdefault(self._her_ant[2], {}); d[k] = d.get(k, 0) + 1
            if self._her_ant[0] != q: self._her_paso = (q[0] - self._her_ant[0][0], q[1] - self._her_ant[0][1])
            elif k == "quieta": self._her_paso = None
        self._her_ant = (q, t, sit)
        I = CFG["imaginar_v45"]; H = T["mirada"]; P = self.p_costumbre(sit); best = max(COSTUMBRES, key=lambda k: (P[k], k))
        inercia = q
        if self._her_paso:
            for _ in range(int(I["pasos_inercia"])):
                n_ = (inercia[0] + self._her_paso[0], inercia[1] + self._her_paso[1])
                if not self.M.pasa(inercia, n_): break
                inercia = n_
        if P[best] >= float(I["confianza"]):
            if best == "quieta": pred = q
            elif best == "hacia_mi": pred = self._anda(q, self._dist_a(pos), H)
            elif best == "hacia_bestia": pred = self._anda(q, self._dist_a(self.bestia), H) if self.bestia else q
            elif best in ("casa", "lejos_bestia"): pred = self._anda(q, self.M.distancias(sorted(self.casa_celdas)), H)
            else: pred = self._anda(q, self.M.distancias({"huerto": self.M.plantas, "bosque": self.M.bosque, "salvaje": self.M.salvaje, "almacen": self.M.acceso_almacen}[best]), H)
            modo = "costumbre"
        else: pred = inercia; modo = "inercia"
        self._her_pred = pred
        self.pred_v45.append((t, list(q), list(pred), list(inercia), modo, best, round(P[best], 3)))

    def lo_que_era(self, x):
        """(prompt 90) lo que era para ella una de las suyas: el radar (cuerpo, recursos, vínculo) más lo que vale por ser hermana o vecina (en el cuerpo)"""
        v = self.radar(x) if self.radar_v34 else {"cuerpo": 0.0, "recursos": 0.0, "vinculo": 0.0}
        return {"cuerpo": max(0.0, v["cuerpo"]) + (self.valor_vida(x) if self.radar_v38 else 0.0), "recursos": max(0.0, v["recursos"]), "vinculo": max(0.0, v["vinculo"])}

    def duelo_propio3(self, t):
        """(prompt 90) mis duelos en las tres dimensiones (con la semivida de siempre; sumados o el mayor, como el duelo de antes)"""
        g = {"cuerpo": 0.0, "recursos": 0.0, "vinculo": 0.0}
        for x, m in self.muertas.items():
            if "w3" not in m: continue
            sv = self.semivida_duelo(m["hermana"]); dt = max(0.0, t - m["t"])
            for k in g: v = duelo(dt, sv, m["w3"][k]); g[k] = (g[k] + v) if self.duelo_suma_v15 else max(g[k], v)
        return g

    def _pon_duelo3(self, F, g, alivio, suma=False):
        for k, fila in (("cuerpo", "S-DUELO-CUERPO"), ("recursos", "S-DUELO-RECURSOS"), ("vinculo", "S-DUELO-VINCULO")):
            v = g[k] * alivio
            if v > 0:
                REPARTO.setdefault(fila, {"cuerpo": (1.0, 0.0, 0.0), "recursos": (0.0, 1.0, 0.0), "vinculo": (0.0, 0.0, 1.0)}[k])
                F[fila] = (F.get(fila, 0.0) + v) if suma else max(F.get(fila, 0.0), v)

    def pr_de(self, k):
        """(prompt 94) lo que cree que cuesta un turno de la clase k: con prop_ctx_v48, lo aprendido a esta hora y en este sitio (dentro o fuera de casa); si no
        tiene nada de ahí, lo de la clase. (prompt 95) Empujar y golpear, sin nada aprendido aún de su clase, lo de «otra» (como antes)"""
        if self.prop_ctx_v48:
            e = self.prop_ctx.get((k, self.obs["fase"], tuple(self.obs["yo"]["pos"]) in self.todas_casas))
            if e: return e
        e = self.prop.get(k)
        if not e and k in ("empujar", "golpear"): return self.pr_de("otra")
        return e or {}

    def clase_de(self, acc):
        """la clase de una acción para aprender lo que cuesta; (prompt 95) con clase_v49, empujar y golpear, cada una la suya"""
        if self.clase_v49 and acc.get("accion") in ("empujar", "golpear"): return acc["accion"]
        return Criatura.clase(acc)

    def _bestia_ve(self, x):
        """(prompt 89) la bestia de ese nombre, como la ve ahora (su casilla y lo que lleva), o None"""
        for b in (self.obs.get("bestias") or []):
            if b.get("id") == x: return tuple(b["pos"]), list(b.get("lleva") or [])
        b = self.obs.get("bestia")
        if b and b.get("id", "bestia") == x: return tuple(b["pos"]), list(b.get("lleva") or [])
        return None

    def _suyas_pegadas(self, qb):
        """(prompt 89) las suyas (la hermana y las vecinas que ha visto en la mirada) que ya están pegadas a la casilla qb"""
        out = []
        if not self.pareja_muerta and self.pareja_pos and self.cheb(self.pareja_pos, qb) <= 1: out.append(self.hermana)
        out += [x for x, d in self.otras.items() if x not in self.muertas and d.get("pos") and self.obs["turno"] - d.get("t", -10 ** 9) <= T["mirada"] and self.cheb(tuple(d["pos"]), qb) <= 1]
        return out

    def _foto_bestia_g(self, f, t, acc):
        """(prompt 89) empujar o pegar a una bestia, con los hechos de la cultura (echar, matar) y las suyas ya pegadas a ella (n = ella más ellas):
        - empujar: con la fuerza de bastantes (n^exponente ≥ umbral^exponente) se va lejos y suelta lo que lleva (lo coge ella, hasta llenar la bolsa); si no,
          como siempre: con otra pegada a la bestia, suelta lo robado; sola, me pega;
        - pegar: turno a turno, el golpe de las n (el de una criatura × n^exponente) contra su vida (la entera, la que dice la cultura) y lo que se cura; si muere
          antes de que sus golpes (uno por turno) me maten, se va y deja sus comidas y lo que llevaba (mi parte, hasta llenar la bolsa); si no, me pega una vez"""
        x = acc["a"]; vb = self._bestia_ve(x)
        if vb is None: return
        qb, lleva_b = vb; n = 1 + len(self._suyas_pegadas(qb)); comida_b = lleva_b.count("comida"); gb = float(self.reglas.get("golpe_bestia") or 0)
        if t == "empujar":
            E = self.hechos_g.get("echar")
            if E and n ** E["exponente"] >= E["umbral_criaturas"] ** E["exponente"] - 1e-9:
                f["sin_bestia"] = x; f["recupera"] = True; f["echa_bestia"] = n; f["bolsa"] = (list(f["bolsa"]) + ["comida"] * comida_b)[:6]
            elif 1 + sum(1 for c in self.obs["criaturas"] if self.cheb(tuple(c["pos"]), qb) <= 1) >= int(self.reglas.get("bestia_cuenta_como") or 2):
                f["recupera"] = True; f["bolsa"] = (list(f["bolsa"]) + ["comida"] * comida_b)[:6]
            else: f["vida"] = max(0.0, f["vida"] - gb)
            return
        M = self.hechos_g.get("matar")
        if not M: f["vida"] = max(0.0, f["vida"] - gb); return
        dano = M["golpe_criatura"] * n ** M["exponente"]; v = M["vida"]; k = 0
        while v > 0 and k < 10:
            v -= dano; k += 1
            if v > 0: v = min(M["vida"], v + M["cura_por_turno"])
        if v <= 0 and f["vida"] - M["golpe_bestia"] * k > 0:
            f["vida"] -= M["golpe_bestia"] * k; f["sin_bestia"] = x; f["mata_bestia"] = (n, k)
            deja = int(M["comida_deja"]) + comida_b; f["bolsa"] = (list(f["bolsa"]) + ["comida"] * (-(-deja // n)))[:6]
        else: f["vida"] = max(0.0, f["vida"] - M["golpe_bestia"])

    def _filas_orig(self, f):
        """f: {pos, vida, hambre, cansancio, bolsa, almacen_n, despensa_n, hermana_lleva, ign_botiquin}"""
        F = {}; pos = f["pos"]; t = self.obs["turno"]
        F["F-DANO"] = cuesta((self.vida_max - f["vida"]) / self.vida_max)
        F["F-HAMBRE"] = self.dh(f["hambre"])
        F["F-CANSANCIO"] = cuesta(f["cansancio"] / self.cans_max)
        # amenaza: solo la bestia (las otras criaturas son neutras, prompt 9)
        hp_her = self.hp_supuesta(self.pareja_herida, self.pareja_vida_nivel)
        if self.dar_cura_v24 and self.pareja_herida and f.get("dio") == (self.hermana, self.botiquin) and not (f.get("devuelve") or f.get("sin_alivio")):      # (prompt 62) le doy la medicina a la hermana que creo herida: la imagino curada, lo que creo que cura
            hp_her = min(self.vida_max, hp_her + max(0.0, self.cuaderno.creencia_cuerpo(self.botiquin, "valle") or 0.0))
        en_casa = bool(self.reglas.get("bestia_no_entra_en_casas")) and pos in self.todas_casas      # (prompt 12) regla pública: ahí no la alcanza
        if self.bestia is not None and not en_casa:
            d = self.lejos(pos, self.bestia)                              # (prompt 30) pasos: lo que le cuesta a la bestia llegar
            F["F-4-ALCANCE"] = A.ALCANCE_TECHO * max(0.0, 1.0 - max(0.0, d - 1.0) / T["alcance_horizonte"])
            ab = self.agresor_bestia
            if (t - ab["ultimo"]) <= T["agresor_ventana"]:
                fc = max(0.0, 1.0 - d / self.vista_en(f.get("H", 0)))
                if d < A.MURO_D0: fr = (A.MURO_D0 - d) / A.MURO_D0; fc *= 1.0 + A.MURO_K * fr * fr
                F["S-7-AGRESOR"] = min(A.AGRESOR_CAP_TOTAL, min(A.AGRESOR_TECHO, ab["dano"] / A.AGRESOR_DANO_REF) * fc)
            elif ab["acum"] > 0 and d <= A.REENCUENTRO_CERCA:
                acerca = d <= 2.0 or (len(self.dist_bestia) >= 2 and self.dist_bestia[-1][1] < self.dist_bestia[-2][1])
                if acerca:
                    m = cuesta(min(1.0, ab["acum"] / self.vida_max))
                    F["F-REENCUENTRO"] = m * (A.REENCUENTRO_MITAD if d > 1.0 else 1.0)
        if self.bestia is not None and self.pareja_vista and self.pareja_pos and ((self.cheb(self.pareja_pos, self.bestia) <= 1) if self.dist_u else (math.dist(self.pareja_pos, self.bestia) <= 1.0)) \
                and not (self.reglas.get("bestia_no_entra_en_casas") and self.pareja_pos in self.todas_casas):
                F["F-HERMANO-AMENAZA"] = A.H_PREV * min(1.0, float(self.reglas.get("golpe_bestia") or 0) / max(1.0, hp_her))
                if self.acompanar_v41: F["F-HERMANO-AMENAZA"] /= self.juntas(self.pareja_pos, pos)      # (prompt 86) a suertes entre las que están con ella
        if self.anticipa: F["F-ANTICIPACION"] = self.anticipacion_M(pos)       # (prompt 14) la noche
        if self.enfado_on and self.enfado is not None and not f.get("recupera"):     # (prompt 27) lo robado tira de ella (pesado por el vínculo si es de la hermana)
            F["R-ENFADO"] = self.enfado["w"] * min(1.0, self.enfado["n"] / self.WT)
        if self.responde and not en_casa:                                   # (prompt 24) «peligro» oído: como si la bestia estuviera donde llamó, pesado por el vínculo
            for (_, q, w) in self.peligro_oido:
                d = self.lejos(pos, q); F["F-4-ALCANCE"] = max(F.get("F-4-ALCANCE", 0.0), w * A.ALCANCE_TECHO * max(0.0, 1.0 - max(0.0, d - 1.0) / T["alcance_horizonte"]))
        calma = X.calma_de(F)
        # recursos
        W = f["bolsa"].count("comida") + f["despensa_n"] + f["almacen_n"] / CFG["almacen"]["entre"] + f.get("W_trabajo", 0.0)
        F["R-CARENCIA"] = max(0.0, (self.WT - W) / self.WT)
        mejor = 0.0
        for q, niv in self.fuentes_f(f).items():
            mejor = max(mejor, niv * max(0.0, 1.0 - self.lejos(pos, q) / A.BOTIN_DIST_REF) ** A.BOTIN_EXP)
        F["R-LLAMADA"] = min(A.BOTIN_CAP, mejor)
        cree_cura = (self.cuaderno.creencia_max_cuerpo(self.botiquin) or 0.0) > 0
        if cree_cura and self.botiquin not in f["bolsa"]: F["R-ACOPIO"] = A.ACOPIO_M * self.rad_cosa(self.botiquin, "guardar")
        F["R-CURIOSIDAD"] = X.ACOPIO_M0 * calma * f["ign_botiquin"] * (X.ALIVIO_ZURRON if self.botiquin in f["bolsa"] else 1.0)
        F[N29.FILA_CUANTO] = self.cuanto_M(f, calma)                                     # (prompt 12)
        F[C5.FILA_FRONT] = self.frontera_M(pos)                                          # (prompt 12)
        # la hermana
        if self.duelo_v19:                                                  # (prompt 31) el duelo por la hermana o por una vecina; la compañía de las suyas lo alivia
            if self.duelo_v45:                                              # (prompt 90) del radar, en sus tres dimensiones
                g3 = self.duelo_propio3(t)
                if any(v > 0 for v in g3.values()): self._pon_duelo3(F, g3, self.alivio(pos))
            else:
                g, _ = self.duelo_propio(t)
                if g > 0: F["S-MUERTE-PAREJA"] = g * self.alivio(pos)
        if self.pareja_muerta:
            if not self.duelo_v19:
                dt = max(0.0, t - (self.turno_saber_muerte if self.turno_saber_muerte is not None else t))
                F["S-MUERTE-PAREJA"] = duelo(dt, T["duelo_semivida"], self.B)
        else:
            m = max(0.0, (self.vida_max - hp_her) / self.vida_max) * self.peso_kin(self.hermana)
            if self.pareja_pos and any(self.botiquin in (c.get("objetos") or []) and ((self.cheb(tuple(c["pos"]), self.pareja_pos) <= A.MEDICINA_DIST) if self.dist_u else (math.dist(tuple(c["pos"]), self.pareja_pos) <= A.MEDICINA_DIST)) for c in self.obs["casillas"]):
                m *= A.MEDICINA_ATEN
            F["S-DANO-PAREJA"] = m
            dd_ = self.dano_dar(self.hermana) if self.cara_dar_v65 else None    # (prompt 130) su daño, de su petición de cura
            if cree_cura and dd_ is not None and self.botiquin not in f["hermana_lleva"]: F["R-HERMANO-FALTA"] = self.peso_dar(self.hermana) * dd_ * self.rad_cosa(self.botiquin, "dar")
            elif cree_cura and self.pareja_herida and self.botiquin not in f["hermana_lleva"]: F["R-HERMANO-FALTA"] = A.H_PREV * 0.5 * self.rad_cosa(self.botiquin, "dar")
            if self.responde and self.ayuda_oida and self.pareja_pos and max(abs(pos[0] - self.pareja_pos[0]), abs(pos[1] - self.pareja_pos[1])) > 1:
                ped_ = self.ayuda_oida[4] * self.peso_dar(self.hermana) if len(self.ayuda_oida) > 4 else self.ayuda_oida[3] * A.H_PREV * 0.5     # (prompt 128) la petición: su cuánto por lo que vale
                F["R-HERMANO-FALTA"] = max(F.get("R-HERMANO-FALTA", 0.0), ped_)        # (prompt 24) me ha pedido ayuda y no estoy a su lado
            hc_ = self.hambre_dar(self.hermana) if self.cara_dar_v65 else (self.hambre_cara(self.hermana) if self.cara_v64 else None)      # (prompt 128) el hambre que le leo en la cara, si se la he visto; (130) la de su petición
            if self.dar_comida and (self.pareja_flaca if hc_ is None else hc_ > 0) and "comida" not in f["hermana_lleva"]:
                # (prompt 23, Manel) la hermana flaca sin comida: lo que valdría quitarle ese hambre (la cuesta del hambre, con lo que cree que quita una comida), pesado por el vínculo
                h = float(CFG["banda_de_la_hermana"]["flaca_hambre_estimada"]) if hc_ is None else hc_
                v = self.peso_dar(self.hermana) * (self.dh(h) - self.dh(max(0.0, h - self.cree_comida(h)))) * self.rad_cosa("comida", "dar")      # (104) peso_dar = peso_kin sin dar_v52
                F["R-HERMANO-FALTA"] = max(F.get("R-HERMANO-FALTA", 0.0), v)
            if calma >= 1.0 and self.botiquin not in f["hermana_lleva"] and self.botiquin in f["bolsa"] and self.pareja_pos is not None \
                    and (not self.provision_necesidad_v22 or self.necesita(self.hermana, self.botiquin)): F["S-PROVISION"] = A.PROVISION_M * self.rad_cosa(self.botiquin, "dar")     # (prompt 60) por su necesidad
        if self.vecinas_on:                                                 # (prompt 28) lo mismo con cada vecina, por su vínculo: R-HERMANO-FALTA es el mayor de todos
            h = float(CFG["banda_de_la_hermana"]["flaca_hambre_estimada"]); val_c = (self.dh(h) - self.dh(max(0.0, h - self.cree_comida(h)))) * self.rad_cosa("comida", "dar")
            for x, d in self.otras.items():
                hcx = self.hambre_dar(x) if self.cara_dar_v65 else (self.hambre_cara(x) if self.cara_v64 else None)     # (prompt 128) su hambre, de su cara; (130) de su petición
                ddx = self.dano_dar(x) if self.cara_dar_v65 else None               # (prompt 130) su daño, de su petición de cura
                if not self.necesidad_vecina(x, d) and not (hcx is not None and hcx > 0): continue
                w = self.peso_dar(x); lleva = f["lleva_otras"].get(x, d.get("lleva") or []); m_ = 0.0      # (104) peso_dar = peso_kin sin dar_v52
                if self.dar_comida and (d.get("flaca") if hcx is None else hcx > 0) and "comida" not in lleva:
                    m_ = max(m_, w * (val_c if hcx is None else (self.dh(hcx) - self.dh(max(0.0, hcx - self.cree_comida(hcx)))) * self.rad_cosa("comida", "dar")))
                if cree_cura and ddx is not None and self.botiquin not in lleva: m_ = max(m_, w * ddx * self.rad_cosa(self.botiquin, "dar"))
                elif cree_cura and d.get("herida") and self.botiquin not in lleva: m_ = max(m_, w * A.H_PREV * 0.5 * self.rad_cosa(self.botiquin, "dar"))
                if self.responde and d.get("ayuda") and self.obs["turno"] - d["ayuda"][0] <= T["mirada"] and d.get("pos") and max(abs(pos[0] - d["pos"][0]), abs(pos[1] - d["pos"][1])) > 1:
                    m_ = max(m_, d["ayuda"][4] * w if len(d["ayuda"]) > 4 else d["ayuda"][3] * A.H_PREV * 0.5)     # (prompt 128) la petición: su cuánto por lo que vale
                if m_ > 0: F["R-HERMANO-FALTA"] = max(F.get("R-HERMANO-FALTA", 0.0), m_)
        if self.cara_v64:                                                   # (prompt 128) lo que le falta en recursos o vínculo, de su cara: la mayor, por lo que vale
            mc = 0.0
            for x in ([self.hermana] if not self.pareja_muerta else []) + [y for y in self.otras if y not in self.muertas]:
                c = self._cara_de(x)
                if c: mc = max(mc, max(0.0, -c[1], -c[2]) * self.peso_dar(x))
            if mc > 0:
                b_ = REPARTO["F-HAMBRE"]; REPARTO.setdefault("S-CARA", (min(b_), min(b_), max(b_))); F["S-CARA"] = mc     # (el reparto del alivio de la otra, G-ALIVIO)
        if self.voz_v64 and self.responde:                                  # (prompt 128) el contacto oído: su soledad, como su dolor, por su cuánto y lo que vale, mientras no esté a su lado
            for x, rec in ([(self.hermana, self.her_contacto)] if not self.pareja_muerta else []) + [(y, d.get("contacto")) for y, d in self.otras.items() if y not in self.muertas]:
                if rec and self.obs["turno"] - rec[0] <= T["mirada"] and self.cheb(pos, rec[1]) > 1:
                    F["S-DANO-PAREJA"] = max(F.get("S-DANO-PAREJA", 0.0), rec[2] * self.peso_dar(x))
        if self.radar_v34: self._rad_filas_perder(f, F, hp_her)            # (prompt 79) la foto que imagina perder a una de las suyas
        if self.contagio_vecinas_v25 and self.vecinas_on:                   # (prompt 63) la herida de una vecina, por su vínculo (la mayor, como el duelo)
            cura_ = max(0.0, self.cuaderno.creencia_cuerpo(self.botiquin, "valle") or 0.0)
            for x, d in self.otras.items():
                if x in self.muertas or not d.get("herida") or t - d.get("t", -10 ** 9) > T["mirada"]: continue
                hp_x = self.hp_supuesta(True, d.get("vida_nivel"))
                if self.dar_cura_v24 and f.get("dio") == (x, self.botiquin) and not (f.get("devuelve") or f.get("sin_alivio")): hp_x = min(self.vida_max, hp_x + cura_)
                m_ = max(0.0, (self.vida_max - hp_x) / self.vida_max) * self.peso_kin(x)
                if m_ > 0: F["S-DANO-PAREJA"] = max(F.get("S-DANO-PAREJA", 0.0), m_)
        if self.duelo_v19:                                                  # (prompt 31) el duelo de otra lo siento como su herida (S-DANO-PAREJA), y estar a su lado lo alivia
            dus = [(self.hermana, self.duelo_oido(self.her_duelo))] if not self.pareja_muerta else []
            dus += [(x, self.duelo_oido(d.get("duelo"))) for x, d in self.otras.items()]
            for x, m_ in dus:
                if m_ > 0: F["S-DANO-PAREJA"] = max(F.get("S-DANO-PAREJA", 0.0), m_ * self.alivio(pos, quien=x))
        if self.dos_platos: self.platos(f, F, pos, cree_cura)
        P = 1.0 if self.pareja_vista else (0.5 if self.pareja_oida else 0.0)
        if self.vecinas_on:                                                 # (prompt 28) la soledad: una vecina a la vista acompaña según su vínculo
            vistas_x = {c["id"] for c in self.obs["criaturas"]}
            P = max([P] + [self.vin.get(x, 0.0) for x in vistas_x if x != self.hermana])
        F["S-SOLEDAD"] = soledad(P, self.sin_compania, T["soledad_rampa"])
        if not self.pareja_muerta:                                    # S-COMPANIA (filas10 del seis): techo × la distancia andando a la hermana
            techo = float(os.environ.get("GEMV_COMPANIA_TECHO") or 0.32)
            if self.pareja_pos is None: F["S-COMPANIA"] = techo
            else:
                d = self._dist_a(self.pareja_pos).get(pos)
                if d is None: F["S-COMPANIA"] = techo
                elif d > 7: F["S-COMPANIA"] = techo * min(1.0, (d - 7) / (7 * (1 + 2.0 * calma)))
        if self.acompanar_v41 and "F-4-ALCANCE" in F: F["F-4-ALCANCE"] /= self.juntas(pos, pos)      # (prompt 86) la bestia a suertes: el peligro, entre las que estaría junta
        for n in MI.FILAS_MIEDO:                                       # el mando del miedo: valiente 0,5, prudente 1,5
            if n in F: F[n] *= self.miedo
        return F

    def platos(self, f, F, pos, cree_cura):
        """(prompt 34, Manel) «dos platos»: lo que alimenta los platos de ganar, cada fila del tamaño de la de pérdida que le hace de espejo (sin números nuevos):
        - el frío: lo que se sale la temperatura de fuera de la zona de confort (regla pública), sobre el ancho de esa zona, en la cuesta de F-HAMBRE. Fuera, displacer
          (F-FRIO); en una casa, el mismo valor como placer (P-CALOR: el calor de casa cuando fuera hace frío);
        - el gusto de comer (P-COMER): lo que baja F-HAMBRE al comer en la foto (proporcional al hambre que quita: sin hambre, casi nada);
        - conseguir (R-CONSEGUIR): cada comida o medicina que coge en la foto vale lo que un paso de R-CARENCIA, 1/objetivo de riqueza;
        - estar con las suyas (S-JUNTAS): el vínculo mayor de las que tendrá a la vista en la foto × el techo de S-SOLEDAD (el espejo de la soledad);
        - dar (S-DAR): lo que valía para ella la necesidad de la otra (R-HERMANO-FALTA: comida o medicina, por su vínculo), que al dar se cumple"""
        Tf = self.frio_en(f.get("H", 0)); cf = self.reglas.get("temperatura_confort"); on = self.platos_on
        if "cuerpo" in on and Tf is not None and cf:
            lo, hi = cf; ref = (hi - lo) * (float(CFG["platos"]["frio_referencia_anchos"]) if self.platos_v23 else 1.0)     # (prompt 35) el frío, incómodo: sobre dos anchos de la zona
            u = min(1.0, max(0.0, lo - Tf, Tf - hi) / max(1e-9, ref))
            if u > 0: F["P-CALOR" if pos in self.todas_casas else "F-FRIO"] = cuesta(u)
        if "cuerpo" in on and f.get("gusto"): F["P-COMER"] = f["gusto"]
        if "recursos" in on and f.get("consigue"):
            F["R-CONSEGUIR"] = self.utilidad(list(self.obs["bolsa"]), f.get("consigue_tipos") or ["comida"] * f["consigue"]) if self.platos_v24 else min(1.0, f["consigue"] / self.WT)
        if self.sentir:                                                     # (prompt 35) lo sentido: en el estado, apagándose; con lo que imagina, el mayor (no se suma: no engancha)
            H_ = f.get("H", 0)
            for fila, (v_, t_) in self.sentido.items():
                plato = {"P-COMER": "cuerpo", "R-CONSEGUIR": "recursos", "S-DAR": "vinculo"}[fila]
                if plato in on: F[fila] = max(F.get(fila, 0.0), v_ * 0.5 ** ((self.obs["turno"] + H_ - t_) / T["mirada"]))
        if "vinculo" not in on: return
        v = self.vista_en(f.get("H", 0)); cerca = [(self.pareja_pos, self.B)] if (not self.pareja_muerta and self.pareja_pos) else []
        cerca += [(d.get("pos"), self.vin.get(x, 0.0)) for x, d in self.otras.items() if d.get("pos") and self.obs["turno"] - d.get("t", -10 ** 9) <= T["mirada"]]
        P = max([0.0] + [w for q, w in cerca if self.cheb(pos, q) <= v])
        if P > 0 and (not self.platos_v24 or self.juntas_sirve()): F["S-JUNTAS"] = P * A.SOLEDAD_TECHO
        self._sdar(f, F)

    # ── (prompt 79) el radar aprendido ──
    RAD_FUENTES = {"suelo": "cajones", "matorral": "cajones", "planta": "bayas", "almacen": "camara"}     # de dónde se coge → su fuente de botín (las del siete)

    def _rad_nace(self, objeto, sit, efecto):
        """(C) el valor de nacimiento, como la cultura: n_recuerdos heredados de peso w_h"""
        KC = CFG["cultura"]; n_nace, w_nace = (1, 1.0) if self.radar_v39 else (KC["n_recuerdos"], KC["w_h"])     # (prompt 84) como una sola experiencia
        for _ in range(n_nace):
            r = {"dia": self.cuaderno.dia_actual(), "tick": None, "efecto": {d: round(float(efecto.get(d) or 0.0), 6) for d in CU.DOMINIOS},
                 "importancia": {d: 0.0 for d in CU.DOMINIOS}, "intensidad": w_nace, "creencia_antes": None, "al_menos": False, "origen": "heredado"}
            self.cuaderno._obj(objeto)["situaciones"].setdefault(sit, []).append(r)

    def _rad_inicia(self):
        """(C) al nacer: la hermana, por familia (Hamilton, provisional: su vida vale la mitad de la propia; la propia vida vale la cuesta entera de F-DANO, la
        de morir), y un vínculo de la mitad; las cosas, desde la tabla de hoy (las fuentes de botín, lo que vale tener una medicina, lo que vale darla o dar una
        comida)"""
        R = CFG["radar_v34"]; vida_propia = cuesta(1.0)
        self._rad = {"base": None, "ven": {}, "t0": None, "dar": [], "cache": {}, "vida_propia": vida_propia}
        if self.radar_c_v34:
            k_ = self.radar_c_factor
            self._rad_nace("criatura:" + self.hermana, "cerca", {"cuerpo": 0.0 if self.radar_v38 else k_ * R["hermana"] * vida_propia, "recursos": 0.0})
            self._rad_nace("criatura:" + self.hermana, "trato", {"vinculo": min(1.0, k_ * R["hermana_vinculo"])})
        for k in ("camara", "cajones", "bayas"): self._rad_nace("fuente:" + k, "valle", {"recursos": A.VALOR_NIVEL[k]})
        self._rad_nace(self.botiquin, "guardar", {"recursos": A.ACOPIO_M})
        self._rad_nace(self.botiquin, "dar", {"vinculo": A.H_PREV * 0.5})
        h = float(CFG["banda_de_la_hermana"]["flaca_hambre_estimada"]); self._rad["dar_comida0"] = self.dh(h) - self.dh(max(0.0, h - self.cree_comida(h)))
        self._rad_nace("comida", "dar", {"vinculo": self._rad["dar_comida0"]})

    def _rad_nace_vecina(self, x):
        """(C) una vecina, por especie (provisional): una cuarta parte de lo que vale la hermana al nacer"""
        if x == self.hermana or ("criatura:" + x) in self.cuaderno.objetos: return
        if not self.radar_c_v34: self._rad.setdefault("conocidas", set()).add(x); return
        R = CFG["radar_v34"]; q = R["vecina"]
        k_ = self.radar_c_factor
        self._rad_nace("criatura:" + x, "cerca", {"cuerpo": 0.0 if self.radar_v38 else k_ * q * R["hermana"] * self._rad["vida_propia"], "recursos": 0.0})
        self._rad_nace("criatura:" + x, "trato", {"vinculo": min(1.0, k_ * q * R["hermana_vinculo"])})

    def _rad_cree(self, objeto, sit):
        k = (objeto, sit); C = self._rad["cache"]
        if k not in C: C[k] = self.cuaderno.creencia(objeto, sit, con_neutro=False) or {d: 0.0 for d in CU.DOMINIOS}
        return C[k]

    def radar(self, x):
        """lo que vale para ella la criatura x en cuerpo, recursos y vínculo (lo aprendido, desde su nacimiento)"""
        a = self._rad_cree("criatura:" + x, "cerca"); b = self._rad_cree("criatura:" + x, "trato")
        return {"cuerpo": a["cuerpo"], "recursos": a["recursos"], "vinculo": b["vinculo"]}

    def valor_fuente(self, clave):
        """(B, sin la constante) lo que vale una fuente de botín: lo aprendido (nace con el valor del siete, VALOR_NIVEL)"""
        return self._rad_cree("fuente:" + clave, "valle")["recursos"] if self.radar_v34 else A.VALOR_NIVEL[clave]

    def rad_cosa(self, tipo, sit):
        """(D) lo aprendido de una cosa frente a su nacimiento (1 = lo que se creía al nacer): «dar» (lo que le pasa a la otra al dársela), «guardar» (la medicina)"""
        if not self.radar_v34 or (sit == "dar" and not self.radar_d_v34): return 1.0
        dom = "vinculo" if sit == "dar" else "recursos"
        nac = (A.H_PREV * 0.5 if tipo == self.botiquin else self._rad["dar_comida0"]) if sit == "dar" else A.ACOPIO_M
        return self._rad_cree(tipo, sit)[dom] / nac if nac > 0 else 0.0

    def _rad_win(self, x):
        return self._rad["ven"].setdefault(x, {"n": 0, "pierde": 0.0, "gana": 0.0, "vista": 0, "cuidado": 0})

    def _rad_vive(self, obs, t, pos):
        """(B) viviendo: por turno, la vida que pierde y la comida que gana (come, coge, recibe; menos lo que le roban), con una de las suyas a su lado (a una
        casilla) o sin ninguna (la base: una media que se mueve despacio); y cada mirada, por cada una, lo de con ella menos la base, en las unidades de las filas
        (cuerpo: la vida, en la cuesta entera de F-DANO; recursos: las comidas, como R-CARENCIA, 1 / WT cada una), y el trato (vínculo): la parte de la mirada
        a la vista más un cuarto por cada vez que se dieron algo. Y (D) lo que le pasa a la otra después de darle algo, y si la medicina guardada sirvió"""
        R = self._rad; R["cache"] = {}; p = self.prev; H = T["mirada"]
        if p is None: return
        pierde = max(0.0, p["vida"] - obs["yo"]["vida"]); c0, c1 = (p.get("bolsa") or []).count("comida"), obs["bolsa"].count("comida")
        comio = 1 if (p["accion"] == "comer" and p.get("tipo") == "comida" and c1 < c0) else 0
        gana = comio + max(0, c1 - c0) - (self._robo or 0)
        if self.robos_v49:                                                  # (prompt 95) la robada: un recuerdo vivido de la que le roba, con lo que pierde de verdad
            for e in obs.get("empujones_vistos") or []:
                w = e.get("gana"); n_ = (e.get("soltado") or []).count("comida")
                if w and w != self.a and self.a in (e.get("a"), e.get("de")) and n_:
                    self._rad_nace_vecina(w); self.cuaderno.apunta("criatura:" + w, "cerca", {"recursos": -float(n_) / self.WT}, {"recursos": float(n_) / self.WT})["origen"] = "vivido"; R["cache"] = {}
                    self._robada_por[w] = t                                     # (prompt 115) quién me ha robado y cuándo
                    if self.robo_trato_v61:                                     # (3) en el trato de esta mirada, un cuarto menos (lo que sube un regalo)
                        w_ = self._rad_win(w); w_["roba"] = w_.get("roba", 0.0) + 1.0; self.cuenta_v61["robos_trato"] += 1
        elif self.robos_v47:                                                # (prompt 93) lo que le quitan en un empujón (la otra gana y ella suelta comida)
            gana -= sum((e.get("soltado") or []).count("comida") for e in obs.get("empujones_vistos") or [] if e.get("a") == self.a and e.get("gana") not in (None, self.a))
            gana -= sum((e.get("soltado") or []).count("comida") for e in obs.get("empujones_vistos") or [] if e.get("de") == self.a and e.get("gana") not in (None, self.a))
        vis = {c["id"]: c for c in obs["criaturas"] if c["id"] != self.a}
        cerca = [x for x, c in vis.items() if self.cheb(pos, tuple(c["pos"])) <= 1]
        for x in vis: self._rad_nace_vecina(x)
        if not cerca:
            al = 1.0 / CFG["radar_v34"]["base_turnos"]; b = R["base"]
            R["base"] = {"pierde": pierde, "gana": gana} if b is None else {k: (1 - al) * b[k] + al * v for k, v in (("pierde", pierde), ("gana", gana))}
        for x in vis:
            w_ = self._rad_win(x); w_["vista"] += 1
            if x in cerca: w_["n"] += 1; w_["pierde"] += pierde; w_["gana"] += gana
        # (D) lo que le pasa a la otra después de darle algo: una mirada después, ¿se la ve mejor?
        if self.radar_d_v34 and p["accion"] == "dar" and p.get("a") and len(obs["bolsa"]) < len(p.get("bolsa") or []):
            x = p["a"]; c = vis.get(x) or {}
            R["dar"].append({"x": x, "tipo": p.get("tipo"), "t": t, "niv0": c.get("vida_nivel"), "flaca0": c.get("flaca"), "mejor": c.get("vida_nivel"), "flaca_luego": c.get("flaca")})
        if R["t0"] is None: R["t0"] = t
        if t - R["t0"] >= H:                                               # cada mirada: lo apunta
            b = R["base"]
            for x, w_ in R["ven"].items():
                n = w_["n"]
                if n >= CFG["radar_v34"]["min_turnos"] and b is not None:
                    if self.radar_v36:                                       # (prompt 81) lo que añadió en total en la mirada, con la misma intensidad
                        ec = (n * b["pierde"] - w_["pierde"]) / self.vida_max * R["vida_propia"]; er = (w_["gana"] - n * b["gana"]) / self.WT
                        self.cuaderno.apunta("criatura:" + x, "cerca", {"cuerpo": ec, "recursos": er}, {}, tick=t)["origen"] = "vivido"
                    else:
                        ec = (b["pierde"] - w_["pierde"] / n) * H / self.vida_max * R["vida_propia"]; er = (w_["gana"] / n - b["gana"]) * H / self.WT
                        self.cuaderno.apunta("criatura:" + x, "cerca", {"cuerpo": ec, "recursos": er}, {"cuerpo": abs(ec), "recursos": abs(er)}, tick=t)["origen"] = "vivido"
                if self.robo_trato_v61:                                         # (prompt 115, 3) cada robo resta lo que suma un cuidado
                    ev = min(1.0, w_["vista"] / H + 0.25 * (w_["cuidado"] - w_.get("roba", 0.0)))
                    self.cuaderno.apunta("criatura:" + x, "trato", {"vinculo": ev}, {"vinculo": abs(ev)}, tick=t)["origen"] = "vivido"
                else:
                    ev = min(1.0, w_["vista"] / H + 0.25 * w_["cuidado"])
                    self.cuaderno.apunta("criatura:" + x, "trato", {"vinculo": ev}, {"vinculo": ev}, tick=t)["origen"] = "vivido"
            if not self.pareja_muerta and self.hermana not in R["ven"]:      # sin verla en toda la mirada: el trato es 0
                self.cuaderno.apunta("criatura:" + self.hermana, "trato", {"vinculo": 0.0}, {"vinculo": 0.0}, tick=t)["origen"] = "vivido"
            if self.radar_honesto_v35:                                       # (prompt 80) también las vecinas conocidas (vivas) que no ha visto en la mirada
                conocidas = {o[len("criatura:"):] for o in self.cuaderno.objetos if o.startswith("criatura:")} | set(R.get("conocidas", ()))
                for x in sorted(conocidas - set(R["ven"]) - {self.hermana} - set(self.muertas)):
                    self.cuaderno.apunta("criatura:" + x, "trato", {"vinculo": 0.0}, {"vinculo": 0.0}, tick=t)["origen"] = "vivido"
            R["ven"] = {}; R["t0"] = t; R["cache"] = {}
        for d in list(R["dar"]):
            c = vis.get(d["x"])
            if c is not None:
                if c.get("vida_nivel") in self.NIVELES and (d["mejor"] not in self.NIVELES or self.NIVELES.index(c["vida_nivel"]) > self.NIVELES.index(d["mejor"])): d["mejor"] = c["vida_nivel"]
                if c.get("flaca") is False: d["flaca_luego"] = False
            if t - d["t"] < H: continue
            R["dar"].remove(d)
            if d["tipo"] == self.botiquin:
                if d["niv0"] not in self.NIVELES or d["niv0"] == "sana": continue
                e0 = self.hp_supuesta(True, d["niv0"]); e1 = self.hp_supuesta(d["mejor"] != "sana", d["mejor"]) if d["mejor"] in self.NIVELES else e0
                cura = max(1e-9, self.cuaderno.creencia_cuerpo(self.botiquin, "valle") or 1.0)
                self.cuaderno.apunta(self.botiquin, "dar", {"vinculo": A.H_PREV * 0.5 * min(1.0, max(0.0, e1 - e0) / cura)}, {"vinculo": A.H_PREV * 0.5}, tick=t)["origen"] = "visto" if d.get("visto") else "vivido"
            elif d["tipo"] == "comida":
                if not d["flaca0"]: continue
                self.cuaderno.apunta("comida", "dar", {"vinculo": R["dar_comida0"] * (1.0 if d["flaca_luego"] is False else 0.0)}, {"vinculo": R["dar_comida0"]}, tick=t)["origen"] = "vivido"
        # (B, las cosas) la fuente de la que coge: lo que vale por lo que sale (una comida segura vale lo de la cámara, el almacén del siete)
        if p["accion"] == "coger" and p.get("de") in self.RAD_FUENTES and p.get("tipo") in (None, "comida"):
            ok = c1 > c0
            self.cuaderno.apunta("fuente:" + self.RAD_FUENTES[p["de"]], "valle", {"recursos": A.VALOR_NIVEL["camara"] * (1.0 if ok else 0.0)}, {"recursos": A.VALOR_NIVEL["camara"]}, tick=t)["origen"] = "vivido"
        # (prompt 85) el sabor: al comer, el placer de más que sintió, en la fuente de lo que comió
        if self.sabores_v40 and p["accion"] == "comer" and p.get("tipo") in (None, "comida") and c1 < c0:
            antes_o = list(p.get("bolsa_origen") or []); ahora_o = list(obs.get("bolsa_origen") or [])
            for o_ in ahora_o:
                if o_ in antes_o: antes_o.remove(o_)
            comida_o = [o_ for o_ in antes_o if (o_ is not None if self.dulce_v51 else o_ in ("huerto", "bosque"))]      # (prompt 103) dulce_v51: cualquier origen (la dulce también)
            if comida_o:
                org = comida_o[0]; v_ = self.sabor_cuerpo(org)
                self.cuaderno.apunta(self.fuente_sabor(org), "sabor", {"cuerpo": v_}, {}, tick=t)["origen"] = "vivido"
        # (B, las cosas) la medicina guardada: ¿sirvió (la tomó o la dio) o se perdió (robada o podrida)?
        m0, m1 = (p.get("bolsa") or []).count(self.botiquin), obs["bolsa"].count(self.botiquin)
        if m1 < m0:
            sirvio = p["accion"] in ("comer", "dar") and p.get("tipo") == self.botiquin
            self.cuaderno.apunta(self.botiquin, "guardar", {"recursos": A.ACOPIO_M * (1.0 if sirvio else 0.0)}, {"recursos": A.ACOPIO_M}, tick=t)["origen"] = "vivido"
        R["cache"] = {}

    def _rad_mira_roba(self, x, n):
        """(prompt 93, mirando) ve que x gana un empujón y se queda con n comidas de otra: lo apunta en lo que vale x en recursos, en negativo (n comidas), visto,
        en lo que se lee del radar (como lo de estar cerca)"""
        self._rad_nace_vecina(x)
        self.cuaderno.apunta("criatura:" + x, "cerca", {"recursos": -float(n) / self.WT}, {"recursos": float(n) / self.WT})["origen"] = "visto"; self._rad["cache"] = {}

    def _rad_mira_roba_v49(self, w, b, n):
        """(prompt 95, mirando) ve que w le roba n comidas a b: lo que le pasa a b, apuntado en lo que vale w en recursos, con el peso de lo que se aprende
        mirando (como _apunta_visto: la intensidad de lo vivido por el vínculo con b; nunca más que la robada)"""
        self._rad_nace_vecina(w)
        wb = self.B if b == self.hermana else self.vin.get(b, CFG["vinculo"]["escalones"][self.escalon(b)][0])
        imp = float(n) / self.WT; inten = (1.0 + min(1.0, imp / CU.E_INTENSIDAD)) * wb
        r = {"dia": self.cuaderno.dia_actual(), "tick": self.obs["turno"], "efecto": {d: (round(-imp, 4) if d == "recursos" else 0.0) for d in CU.DOMINIOS},
             "importancia": {d: (round(imp, 4) if d == "recursos" else 0.0) for d in CU.DOMINIOS}, "intensidad": round(inten, 4), "creencia_antes": None, "al_menos": False,
             "origen": "visto", "de": b, "B": round(wb, 4)}
        self.cuaderno._obj("criatura:" + w)["situaciones"].setdefault("cerca", []).append(r); self._creencias = {}; self.cuaderno.version += 1; self._rad["cache"] = {}

    def _rad_mira_da(self, x):
        """(B, mirando) ve que x le da algo a otra: lo apunta en lo que vale x en recursos (una comida), visto"""
        self._rad_nace_vecina(x)
        sit = "visto_dar" if self.radar_honesto_v35 else "cerca"            # (prompt 80) lo que da a otras no es lo que vale para ella: aparte, sin leerlo
        self.cuaderno.apunta("criatura:" + x, sit, {"recursos": 1.0 / self.WT}, {"recursos": 1.0 / self.WT})["origen"] = "visto"; self._rad["cache"] = {}

    def _rad_vinculos(self):
        """(B, sin la constante) el vínculo con la hermana y con cada vecina es lo aprendido (el trato), no el escalón con su roce"""
        if not self.pareja_muerta: self.B = min(1.0, max(0.0, self.radar(self.hermana)["vinculo"]))
        for x in list(self.vin): self.vin[x] = min(1.0, max(0.0, self.radar(x)["vinculo"]))

    def _rad_filas_perder(self, f, F, hp_her):
        """(B) la foto que imagina perderla: por cada una de las suyas, su valor en cuerpo y en recursos por lo que se arriesga (la herida que le quedaría en la
        foto; entera si la foto imagina su muerte). El vínculo ya lo pierde S-DANO-PAREJA (con el vínculo aprendido)"""
        for k_, e in (("P-RADAR-CUERPO", (1.0, 0.0, 0.0)), ("P-RADAR-RECURSOS", (0.0, 1.0, 0.0))): REPARTO.setdefault(k_, e)
        quien = [] if self.pareja_muerta else [(self.hermana, hp_her if self.pareja_herida else self.vida_max)]
        for x, d in self.otras.items():
            if x in self.muertas or self.obs["turno"] - d.get("t", -10 ** 9) > T["mirada"]: continue
            hp_x = self.hp_supuesta(True, d.get("vida_nivel")) if d.get("herida") else self.vida_max
            if d.get("herida") and f.get("dio") == (x, self.botiquin) and not (f.get("devuelve") or f.get("sin_alivio")): hp_x = min(self.vida_max, hp_x + max(0.0, self.cuaderno.creencia_cuerpo(self.botiquin, "valle") or 0.0))
            quien.append((x, hp_x))
        pc = pr = 0.0
        for x, hp in quien:
            riesgo = 1.0 if f.get("mata_a") == x else max(0.0, (self.vida_max - hp) / self.vida_max)
            if self.acompanar_v41 and self.bestia is not None and f.get("mata_a") != x:      # (prompt 86) con la bestia cerca, a suertes entre las que están con ella
                qx = self.pareja_pos if x == self.hermana else (self.otras.get(x) or {}).get("pos")
                if qx is not None: riesgo /= self.juntas(tuple(qx), f["pos"])
            if riesgo <= 0: continue
            v = self.radar(x); pc += riesgo * ((self.valor_vida(x) if self.radar_v38 else 0.0) + max(0.0, v["cuerpo"])); pr += riesgo * max(0.0, v["recursos"])
        if pc > 0: F["P-RADAR-CUERPO"] = pc
        if pr > 0: F["P-RADAR-RECURSOS"] = pr

    def _rad_filas_tener(self, f, F, pos):
        """(B) tenerla cerca: por cada una de las suyas a la vista en la foto, su valor en cuerpo y en recursos como ganancia; y el vínculo de las vecinas, con
        el reposo del vínculo (el de la hermana ya es V-VINCULO, con su vínculo aprendido)"""
        R0 = CFG["vivir_bien"]["reposo_dos"]
        for k_, e in (("V-RADAR-CUERPO", (1.0, 0.0, 0.0)), ("V-RADAR-RECURSOS", (0.0, 1.0, 0.0)), ("V-RADAR-VINCULO", (0.0, 0.0, 1.0))): REPARTO.setdefault(k_, e); APETITIVAS.add(k_)
        vista = self.vista_en(f.get("H", 0)); quien = []
        if not self.pareja_muerta and self.pareja_pos and self.cheb(pos, self.pareja_pos) <= vista: quien.append(self.hermana)
        quien += [x for x, d in self.otras.items() if x not in self.muertas and d.get("pos") and self.obs["turno"] - d.get("t", -10 ** 9) <= T["mirada"] and self.cheb(pos, d["pos"]) <= vista]
        gc = gr = gv = 0.0
        for x in quien:
            v = self.radar(x); gc += max(0.0, v["cuerpo"]); gr += max(0.0, v["recursos"])
            if x != self.hermana: gv += R0["vinculo"] * self.vin.get(x, 0.0)
        if self.radar_v36:                                                  # (prompt 81) se sacian: con la de vivir bien de su dimensión, hasta la meta del eje
            gc = min(gc, max(0.0, DEFAULT_CONFIG.f_pos_target - F.get("V-CUERPO", 0.0)))
            gr = min(gr, max(0.0, DEFAULT_CONFIG.r_pos_target - F.get("V-RECURSOS", 0.0)))
            gv = min(gv, max(0.0, DEFAULT_CONFIG.s_pos_target - F.get("V-VINCULO", 0.0)))
        if gc > 0: F["V-RADAR-CUERPO"] = gc
        if gr > 0: F["V-RADAR-RECURSOS"] = gr
        if gv > 0: F["V-RADAR-VINCULO"] = gv

    def juntas(self, q, yo_pos):
        """(prompt 86, el hecho de la cultura: la bestia ataca a una sola, a suertes) cuántas estarían juntas en la casilla q (ella misma si q es su sitio, o la
        otra): la de q, más ella si en la foto está pegada a q, más las que cree pegadas a q (la hermana y las vecinas que ha visto en la mirada)"""
        q = tuple(q); yo_pos = tuple(yo_pos); n = 1 + (1 if q != yo_pos and self.cheb(q, yo_pos) <= 1 else 0)
        otras = ([tuple(self.pareja_pos)] if (not self.pareja_muerta and self.pareja_pos) else []) + \
                [tuple(d["pos"]) for x, d in self.otras.items() if d.get("pos") and x not in self.muertas and self.obs["turno"] - d.get("t", -10 ** 9) <= T["mirada"]]
        n += sum(1 for o in otras if o != q and o != yo_pos and self.cheb(o, q) <= 1)
        return float(n)

    def fuente_sabor(self, origen):
        """de qué fuente aprende el sabor de una comida: la del huerto, «fuente:bayas»; (prompt 96) la del árbol dulce, «fuente:dulce»; las demás, «fuente:cajones»"""
        if self.arbol_v50 and origen == "dulce": return "fuente:dulce"
        return {"huerto": "fuente:bayas"}.get(origen, "fuente:cajones")

    def sabor_cuerpo(self, origen):
        """(prompt 85) el placer de más que da al cuerpo comer una comida de ese origen: la del huerto, una parte (sabores_v40.parte) de lo que vale comer
        a media hambre (lo que baja el dolor del hambre de hambre_ref[0] a hambre_ref[1]); la del bosque, nada"""
        if self.arbol_v50 and origen == "dulce": return float(CFG["arbol_v50"]["dulce_veces_huerto"]) * self.sabor_cuerpo("huerto")      # (prompt 96) el doble que la del huerto
        if origen != "huerto": return 0.0
        S = CFG["sabores_v40"]; h0, h1 = S["hambre_ref"]; return float(S["parte"]) * (self.dh(float(h0)) - self.dh(float(h1)))

    def factor_gusto(self, hambre):
        """(prompt 95) la parte del placer del gusto que siente quien come con esa hambre: entero desde el hambre de flaca, un cuarto con la tripa llena, en medio
        en proporción"""
        if not self.gusto_hambre_v49: return 1.0
        G = CFG["gusto_v49"]; lleno = float(G["lleno"]); h1 = float(CFG["sabores_v40"]["hambre_ref"][0])
        return lleno + (1.0 - lleno) * min(1.0, max(0.0, float(hambre)) / h1)

    def hambre_vista(self, x):
        """(prompt 95) el hambre que supone a otra por lo que ve (flaca o no); (prompt 128, cara_v64) la que le lee en la cara, si se la ha visto en la mirada"""
        if self.cara_dar_v65:                                               # (prompt 130) la de su petición, no la de su cara
            h = self.hambre_dar(x)
            if h is not None: return h
        elif self.cara_v64:
            h = self.hambre_cara(x)
            if h is not None: return h
        fl =self.pareja_flaca if x == self.hermana else bool((self.otras.get(x) or {}).get("flaca"))
        return float(CFG["banda_de_la_hermana"]["flaca_hambre_estimada"]) if fl else float(CFG["gusto_v49"]["no_flaca_hambre_estimada"])

    def origen_primera(self):
        """(prompt 87) el origen de la primera comida de la bolsa (la que da o come el mundo cuando no se dice cuál)"""
        return next((o for tp, o in zip(self.obs["bolsa"], self.obs.get("bolsa_origen") or []) if tp == "comida"), None)

    def valor_sabor(self, origen):
        """(prompt 85) lo que cree que sabe una comida de ese origen: lo aprendido al comerla (el sabor de su fuente, sin nacimiento)"""
        k = self.fuente_sabor(origen); c = self.cuaderno.creencia(k, "sabor", con_neutro=False)
        return max(0.0, c["cuerpo"]) if c else 0.0

    def familia(self, x):
        """(prompt 83) (a) lo que vale la vida de la otra por familia o especie, como parte de la propia (Hamilton, provisional): la hermana, la mitad; una
        vecina, un cuarto de lo de la hermana. De nacimiento; no se aprende"""
        if self.radar_v39: return float(CFG["radar_v39"]["hermana" if x == self.hermana else "vecina"]) * self.radar_c_factor      # (prompt 84) los pesos de RG32r
        R = CFG["radar_v34"]; f = R["hermana"] if x == self.hermana else R["vecina"] * R["hermana"]
        return f * self.radar_c_factor

    def valor_vida(self, x):
        """(prompt 83) (a) en las unidades de la fila del cuerpo: su parte de la propia vida (la cuesta entera de F-DANO)"""
        return self.familia(x) * cuesta(1.0)

    def peso_dar(self, x):
        """(prompt 104, dar_v52) lo que vale la otra en el radar de quien da, para lo que gana al darle: familia (de nacimiento, `familia`) + confianza (lo
        aprendido del trato, el vínculo de su radar; nunca negativo). Sin dar_v52, el de antes (peso_kin)"""
        if not self.dar_v52: return self.peso_kin(x)
        if self.dar_v54:                                                    # (prompt 106) familia × (radar entero ahora / al nacer)
            nace = self.radar_entero(x, nace=True)
            return self.familia(x) * (max(0.0, self.radar_entero(x)) / nace if nace > 0 else 1.0)
        if self.dar_v53:                                                    # (prompt 105) el radar entero: lo_que_era sin recortar cada dimensión (los robos restan)
            r = self.radar(x) if self.radar_v34 else {"cuerpo": 0.0, "recursos": 0.0, "vinculo": 0.0}
            return max(0.0, (self.valor_vida(x) if self.radar_v38 else 0.0) + r["cuerpo"] + r["recursos"] + r["vinculo"])
        return self.familia(x) + (max(0.0, self.radar(x)["vinculo"]) if self.radar_v34 else 0.0)

    def radar_entero(self, x, nace=False):
        """(prompt 106) lo que vale la otra en el radar entero: su vida por familia (valor_vida) + cuerpo + recursos + vínculo del radar, sin recortar cada
        dimensión. Con `nace`, lo de nacimiento: solo los recuerdos heredados de su radar (lo que se creía al nacer, `_rad_nace`)"""
        if not self.radar_v34: return self.valor_vida(x) if self.radar_v38 else 0.0
        if nace:
            def nac(sit, dom):
                rec = [r for r in ((self.cuaderno.objetos.get("criatura:" + x) or {}).get("situaciones") or {}).get(sit, []) if r.get("origen") == "heredado"]
                return sum(float(r["efecto"].get(dom) or 0.0) for r in rec) / len(rec) if rec else 0.0
            r = {"cuerpo": nac("cerca", "cuerpo"), "recursos": nac("cerca", "recursos"), "vinculo": nac("trato", "vinculo")}
        else: r = self.radar(x)
        return (self.valor_vida(x) if self.radar_v38 else 0.0) + r["cuerpo"] + r["recursos"] + r["vinculo"]

    def gesto(self, x):
        """(prompt 104, dar_v52) el gesto: lo que vale para la otra una comida sencilla del bosque (sin gusto): lo que baja el dolor del hambre de la
        referencia de los sabores (sabores_v40.hambre_ref, de media hambre a lo que deja una comida), pesado por lo que vale la otra (peso_dar)"""
        h0, h1 = CFG["sabores_v40"]["hambre_ref"]; parte = float(CFG["dar_v53"]["gesto_parte"]) if self.dar_v53 else 1.0      # (prompt 105) a la mitad
        return parte * self.peso_dar(x) * (self.dh(float(h0)) - self.dh(float(h1)))

    def peso_kin(self, x):
        """el peso de la otra cuando sufre, le falta algo o está en peligro: (prompt 83) lo que vale su vida por familia (a); sin el arreglo, su vínculo"""
        if self.radar_v38: return self.familia(x)
        return self.B if x == self.hermana else self.vin.get(x, 0.0)

    def hp_supuesta(self, herida, nivel):
        """la vida que supone a una de las suyas por lo que ve de ella: sana o herida (las bandas del siete); (prompt 76, gravedad_v31) por su nivel de vida"""
        if self.gravedad_v31 and nivel in CFG["banda_de_la_hermana"]["niveles_v31"]: return float(CFG["banda_de_la_hermana"]["niveles_v31"][nivel])
        return A.BANDA_EST[CFG["banda_de_la_hermana"]["herida" if herida else "sana"]]

    def valor_dar(self, x, tipo, vista=None):
        """(prompt 34) lo que valía para ella la necesidad de la otra (R-HERMANO-FALTA), por su vínculo: lo que gana al darle. (131) `vista`: lo que se veía
        que llevaban antes de dar, para lo vivido (después, la otra ya lleva lo que le he dado)"""
        w = self.peso_kin(x)
        if self.platos_v24 and not self.necesita(x, tipo): return 0.0           # (prompt 36) solo cuando la otra lo necesita o lo pide
        if self.ya_tiene_v67 and (tipo in (vista.get(x) or []) if vista is not None else self.ve_que_lleva(x, tipo)): return 0.0      # (prompt 131) ya lo lleva: dárselo no alivia nada
        if tipo == "comida":
            h = float(CFG["banda_de_la_hermana"]["flaca_hambre_estimada"]); return w * (self.dh(h) - self.dh(max(0.0, h - self.cree_comida(h)))) * self.rad_cosa("comida", "dar")
        return w * A.H_PREV * 0.5 * self.rad_cosa(self.botiquin, "dar") if tipo == self.botiquin else 0.0

    def gusto(self, h0, h1):
        """(prompt 34) el gusto de comer: lo que baja F-HAMBRE; (prompt 35) harta (regla pública), ninguno"""
        if self.platos_v23 and self.reglas.get("harta_por_debajo") is not None and h0 < float(self.reglas["harta_por_debajo"]): return 0.0
        return self.dh(h0) - self.dh(h1)

    def dh(self, h):
        """el dolor del hambre (F-HAMBRE): la cuesta de F-DANO del siete; (prompt 36, Manel: el hambre es dolor, y con hambre alta duele cada vez más) por encima
        del umbral de «necesito ayuda» se multiplica por 1 + ((u − u0) / (1 − u0))², hasta el doble con el hambre al máximo"""
        u = h / self.hambre_max; m = cuesta(u)
        if self.hambre_dolor:
            u0 = float(CFG["llamadas"]["hambre_mayor_que"]) / self.hambre_max
            if u > u0: m *= 1.0 + (float(CFG["hambre_dolor"]["al_maximo"]) - 1.0) * ((u - u0) / (1.0 - u0)) ** 2
        return m

    def _siente(self, obs, t):
        """(prompt 35) lo que acaba de pasar, sentido: comió (el gusto del hambre que quitó), consiguió algo nuevo o se lo dieron (alegría: un paso de la carencia
        por cosa), o dio (amor: lo que valía la necesidad de la otra). Se queda el mayor entre lo que ya sentía (apagándose) y lo nuevo"""
        p = self.prev; antes, ahora = len(p.get("bolsa") or []), len(obs["bolsa"])
        def pon(fila, v):
            if v <= 0: return
            v0 = self.sentido.get(fila); v0 = v0[0] * 0.5 ** ((t - v0[1]) / T["mirada"]) if v0 else 0.0
            self.sentido[fila] = (max(v0, v), t)
        if p["accion"] == "comer" and p.get("tipo") == "comida" and obs["yo"]["hambre"] < p["hambre"]: pon("P-COMER", self.gusto(p["hambre"], obs["yo"]["hambre"]))
        if ahora > antes and not self._robo:
            nuevo = (p["accion"] == "coger" and p.get("de") in CFG["platos"]["conseguir_de"]) or p["accion"] != "coger"      # coger lo nuevo, o recibir
            if nuevo:
                if self.platos_v24:
                    nuevas = list(obs["bolsa"]); viejas = list(p.get("bolsa") or [])
                    for o_ in viejas:
                        if o_ in nuevas: nuevas.remove(o_)
                    pon("R-CONSEGUIR", self.utilidad(viejas, nuevas))
                else: pon("R-CONSEGUIR", min(1.0, (ahora - antes) / self.WT))
        if p["accion"] == "dar" and ahora < antes and p.get("a"): pon("S-DAR", self.valor_dar(p["a"], p.get("tipo"), vista=p.get("lleva_vista_v67")))

    def _sdar(self, f, F):
        if f.get("dio"):
            v = self.valor_dar(*f["dio"])
            if self.sabores_v40 and f.get("dio_origen") and v > 0: v += self.peso_kin(f["dio"][0]) * self.valor_sabor(f["dio_origen"])      # (prompt 85) su gusto a la otra
            if v > 0: F["S-DAR"] = max(F.get("S-DAR", 0.0), v)
        if self.platos_v24 and self.duelo_v19:                              # (prompt 36) dar compañía a la que está de duelo: lo que se alivia del dolor por ella al estar a su lado
            dus = [(self.hermana, self.duelo_oido(self.her_duelo))] if not self.pareja_muerta else []
            dus += [(x, self.duelo_oido(d.get("duelo"))) for x, d in self.otras.items()]
            for x, m_ in dus:
                if m_ > 0:
                    alivia = m_ * (1.0 - self.alivio(f["pos"], quien=x))
                    if alivia > 0: F["S-DAR"] = max(F.get("S-DAR", 0.0), alivia)

    def necesita(self, x, tipo):
        """(prompt 36) si la otra necesita o pide lo que le doy: comida si la creo flaca o me pidió ayuda; medicina si la creo herida o me dijo «estoy herida»"""
        t = self.obs["turno"]
        if x == self.hermana:
            pide = self.ayuda_oida is not None and t - self.ayuda_oida[0] <= T["mirada"]
            ll = self.ayuda_oida[2] if pide else None
            return (tipo == "comida" and (self.pareja_flaca or ll in ("necesito_ayuda", "ven_lo_necesito", "peticion:comida"))) or (tipo == self.botiquin and (self.pareja_herida or ll in ("estoy_herida", "ven_lo_necesito", "peticion:cura")))
        d = self.otras.get(x) or {}; ay = d.get("ayuda"); pide = ay is not None and t - ay[0] <= T["mirada"]; ll = ay[2] if pide else None
        return (tipo == "comida" and (bool(d.get("flaca")) or ll in ("necesito_ayuda", "ven_lo_necesito", "peticion:comida"))) or (tipo == self.botiquin and (bool(d.get("herida")) or ll in ("estoy_herida", "ven_lo_necesito", "peticion:cura")))

    def utilidad(self, bolsa, nuevas):
        """(prompt 36) la alegría de conseguir, según lo que le va a servir: cada comida nueva vale un paso de la carencia (1/objetivo de riqueza) mientras no
        tenga ya lo que le sirve (el objetivo de riqueza, más una por cada una de las suyas que cree flaca), y nada después; una medicina, si no lleva ninguna"""
        flacas = int(not self.pareja_muerta and self.pareja_flaca) + sum(1 for d in self.otras.values() if d.get("flaca"))
        sirve = self.WT + flacas; tiene = bolsa.count("comida"); med = self.botiquin in bolsa; v = 0.0
        for tipo in nuevas:
            if tipo == "comida":
                v += max(0.0, min(1.0, sirve - tiene)) / self.WT; tiene += 1
            elif tipo == self.botiquin and not med: v += 1.0 / self.WT; med = True
        return min(1.0, v)

    def juntas_sirve(self):
        """(prompt 36) estar con las suyas aporta: protección (anochecer o noche, la bestia a la vista o un «peligro» oído), ayuda (alguna de nosotras flaca o
        herida) o compañía (yo llevo un rato sola, o alguna de nosotras está de duelo)"""
        o = self.obs; t = o["turno"]; yo = o["yo"]
        if o["fase"] in ("anochecer", "noche") or self.bestia is not None or any(t - x[0] <= T["voz_ventana"] for x in self.peligro_oido): return True
        if yo["hambre"] > CFG["llamadas"]["hambre_mayor_que"] or yo["vida"] < CFG["llamadas"]["herida_vida_menor_que"]: return True
        if (not self.pareja_muerta and (self.pareja_flaca or self.pareja_herida)) or any(d.get("flaca") or d.get("herida") for d in self.otras.values()): return True
        if self.sin_compania > 0: return True
        if self.duelo_v19 and (self.duelo_propio(t)[1] or self.duelo_oido(self.her_duelo) > 0 or any(self.duelo_oido(d.get("duelo")) > 0 for d in self.otras.values())): return True
        return False

    # ── (prompt 39) la regla general ──
    def _filas_rg(self, f, ganancias=None):
        """las necesidades de la foto (pérdidas), con las filas que ya existían para el cuerpo, el miedo y el vínculo, menos las hechas para una conducta;
        la comida que le falta para lo que tardará en pudrirse (recursos); saber dónde hay comida (la frontera, por lo que le falta saber); el frío; dañar a
        las suyas. Y, con el lado de ganar, cada necesidad que la foto alivia respecto de ahora, como ganancia en su misma dimensión"""
        F = self._filas_orig(f)
        for k in ("F-ANTICIPACION", "R-LLAMADA", "R-CURIOSIDAD", N29.FILA_CUANTO, "R-ENFADO"): F.pop(k, None)
        pos = f["pos"]
        F["R-CARENCIA"] = self.falta_comida(f)                              # recursos: lo que le falta para lo que tardará en pudrirse
        if self.cuesta_medicina_v57 and f.get("dio") and f["dio"][1] == self.botiquin and self.botiquin not in f["bolsa"]:      # (prompt 109) da la última medicina: lo que le curaría
            her_ = max(0.0, self.vida_max - f["vida"] - self.dano_hambre); cura_ = min(her_, max(0.0, self.cuaderno.creencia_cuerpo(self.botiquin, "valle") or 0.0))
            v_ = cuesta((self.vida_max - f["vida"]) / self.vida_max) - cuesta(max(0.0, self.vida_max - f["vida"] - cura_) / self.vida_max)      # la necesidad (su herida) por lo que sirve
            if v_ > 0: REPARTO.setdefault("F-SIN-MEDICINA", REPARTO["F-DANO"]); F["F-SIN-MEDICINA"] = v_
        if self.dar_v54 and f.get("dio") and f["dio"][1] == "comida" and "comida" not in f["bolsa"]:      # (prompt 106) da la última: lo que le costará al cuerpo
            h_ = f["hambre"]; v_ = self.dh(h_) - self.dh(max(0.0, h_ - self.cree_comida(h_)))         # la necesidad por lo que sirve: el alivio que le daría, con su hambre
            if v_ > 0: REPARTO.setdefault("F-ULTIMA-COMIDA", REPARTO["F-HAMBRE"]); F["F-ULTIMA-COMIDA"] = v_
        ig = self.ignorancia_global(); fm = F.get(C5.FILA_FRONT, 0.0)      # saber dónde hay comida: la frontera, por lo que le falta saber
        if fm > 0 and ig > 0: F[C5.FILA_FRONT] = fm / ig * self.falta_saber()
        Tf = self.frio_en(f.get("H", 0)); cf = self.reglas.get("temperatura_confort")      # el frío fuera (dos anchos de la zona de confort); (prompt 65) el de cuando acaba la foto
        if Tf is not None and cf and pos not in self.todas_casas:
            lo, hi = cf; u = min(1.0, max(0.0, lo - Tf, Tf - hi) / max(1e-9, (hi - lo) * float(CFG["platos"]["frio_referencia_anchos"])))
            if u > 0: F["F-FRIO"] = cuesta(u)
        for clave in ("dano_a", "empuja_a"):                                # dañar a las suyas: una pérdida en el vínculo, por el vínculo
            if f.get(clave):
                x, m_ = f[clave]; w = self.peso_kin(x)
                F["S-DANAR"] = F.get("S-DANAR", 0.0) + w * (cuesta(m_ / self.vida_max) if clave == "dano_a" else min(1.0, m_ / max(1.0, self.comidas_dos_dias())))
                if self.simetria_v7 and clave == "empuja_a" and m_ > 0 and (self.necesita(x, "comida") or (self.simetria_vista_v8 and self.se_ve_mal(x))):     # (prompt 45) el espejo de dar: la necesidad que le deja
                    h = float(CFG["banda_de_la_hermana"]["flaca_hambre_estimada"])
                    if self.quitar_espejo_v61:                              # (prompt 115, 4) el espejo exacto del alivio al dar: peso_dar, lo aprendido de dar, en el vínculo
                        b_ = REPARTO["F-HAMBRE"]; REPARTO.setdefault("S-QUITAR", (min(b_), min(b_), max(b_)))      # (el reparto de G-ALIVIO; una pérdida)
                        F["S-QUITAR"] = F.get("S-QUITAR", 0.0) + self.peso_dar(x) * (self.dh(h) - self.dh(max(0.0, h - m_ * self.cree_comida(h)))) * self.rad_cosa("comida", "dar")
                    else:
                        F["R-HERMANO-FALTA"] = F.get("R-HERMANO-FALTA", 0.0) + w * (self.dh(h) - self.dh(max(0.0, h - m_ * self.cree_comida(h))))
        if f.get("mata_a") is not None:                                     # (prompt 47) la foto imagina su muerte: el duelo recién sabido, por su vínculo
            x = f["mata_a"]; h_ = x == self.hermana; w = self.B if h_ else self.vin.get(x, CFG["vinculo"]["escalones"][self.escalon(x)][0])
            if self.duelo_v45 and self.duelo_v19:                           # (prompt 90) imagina su muerte: lo que era para ella, entero (recién sabida)
                w3 = self.lo_que_era(x); sv = self.semivida_duelo(h_)
                self._pon_duelo3(F, {k: duelo(0.0, sv, v) for k, v in w3.items()}, self.alivio(pos, sin=x), suma=self.duelo_suma_v15)
            g = 0.0 if (self.duelo_v45 and self.duelo_v19) else (duelo(0.0, self.semivida_duelo(h_), w) if self.duelo_v19 else (duelo(0.0, T["duelo_semivida"], self.B) if h_ else 0.0))
            if g > 0:
                g_ = g * (self.alivio(pos, sin=x) if self.duelo_v19 else 1.0)
                F["S-MUERTE-PAREJA"] = (F.get("S-MUERTE-PAREJA", 0.0) + g_) if self.duelo_suma_v15 else max(F.get("S-MUERTE-PAREJA", 0.0), g_)     # (prompt 53) se suma
        gan = self.rg_gan if ganancias is None else ganancias
        if gan:
            t = self.obs["turno"]
            if self._F_ahora[0] != t: self._F_ahora = (t, self._filas_rg(self.foto_ahora(), ganancias=False))
            for k, v in self._F_ahora[1].items():
                if k in APETITIVAS or k.startswith("G-"): continue
                g = v - F.get(k, 0.0)
                if g > 1e-9:
                    if self.ya_tiene_v67 and k == "R-HERMANO-FALTA" and f.get("dio") and self.ve_que_lleva(*f["dio"]): continue     # (prompt 131) ya lo lleva: ningún alivio
                    if self.dar_v53 and k == "R-HERMANO-FALTA" and f.get("dio"):     # (prompt 105) el alivio de la otra al dar, como vínculo (el reparto del gesto)
                        b_ = REPARTO["F-HAMBRE"]; REPARTO.setdefault("G-ALIVIO", (min(b_), min(b_), max(b_))); APETITIVAS.add("G-ALIVIO"); F["G-ALIVIO"] = g; continue
                    REPARTO.setdefault("G-" + k, REPARTO[k]); APETITIVAS.add("G-" + k); F["G-" + k] = g
            if self.escala_v6: self.vivir_bien(f, F)
            if self.sabores_v42 and f.get("dio") and f["dio"][1] == "comida" and (self.sabores_v43 or self.necesita(f["dio"][0], "comida")) and not f.get("devuelve") \
                    and not (self.ya_tiene_v67 and self.ve_que_lleva(*f["dio"])):      # (prompt 87) el gusto de la otra; (88) sin necesidad; (109) no al devolver; (131, Manel) no se ve de qué clase es lo que lleva: si lleva comida, no cuenta
                org = f.get("dio_origen") or self.origen_primera()
                g_ = self.peso_dar(f["dio"][0]) * self.valor_sabor(org) * (self.factor_gusto(self.hambre_vista(f["dio"][0])) if self.gusto_hambre_v49 else 1.0) if org else 0.0      # (95) con el hambre de la otra; (104) peso_dar
                if g_ > 0: REPARTO.setdefault("G-SABOR-OTRA", (0.0, 0.0, 1.0)); APETITIVAS.add("G-SABOR-OTRA"); F["G-SABOR-OTRA"] = g_
            if self.dar_v52 and f.get("dio") and (f["dio"][1] == "comida" or not self.gesto_comida_v56) and not f.get("devuelve") and not f.get("sin_gesto"):      # (109) devolver no es un gesto; (111) ni con devolver_solo_gesto_v59      # (prompt 104) el gesto: por dar, aunque la otra no lo necesite; al vínculo y un poco al cuerpo; (108) solo la comida
                g_ = 0.0 if (self.ya_tiene_v67 and self.ve_que_lleva(*f["dio"])) else self.gesto(f["dio"][0])      # (prompt 131, Manel) ya lo lleva: tampoco hay gesto
                if g_ > 0:
                    b_ = REPARTO["F-HAMBRE"]; REPARTO.setdefault("G-GESTO", (min(b_), min(b_), max(b_))); APETITIVAS.add("G-GESTO"); F["G-GESTO"] = g_
            if self.sentir:                                                 # (prompt 42) lo sentido: en el estado, apagándose; con lo imaginado, el mayor (no la suma)
                H_ = f.get("H", 0)
                for fila, (v_, t_) in self.sentido.items():
                    if fila.startswith("G-"): REPARTO.setdefault(fila, REPARTO[fila[2:]]); APETITIVAS.add(fila)
                    F[fila] = max(F.get(fila, 0.0), v_ * 0.5 ** ((t + H_ - t_) / T["mirada"]))
        return F

    def se_ve_mal(self, x):
        """(prompt 46) lo que se ve de la otra: flaca, herida o de duelo (su llamada «estoy de duelo», oída)"""
        if x == self.hermana:
            return (not self.pareja_muerta) and (self.pareja_flaca or self.pareja_herida or (self.duelo_v19 and self.duelo_oido(self.her_duelo) > 0))
        d = self.otras.get(x) or {}
        return bool(d.get("flaca") or d.get("herida") or (self.duelo_v19 and self.duelo_oido(d.get("duelo")) > 0))

    def vivir_bien(self, f, F):
        """(prompt 44, Manel: decisión de método) la escala de la traducción. Vivir bien en el valle (comida, descanso, calor, la hermana cerca y unos dos
        días de comida guardada) da el reposo del paper dos, una ganancia en cada eje (`vivir_bien.reposo_dos`), con tres filas de ganancia, una por eje:
        - cuerpo: lo que tiene de comida, descanso y calor (1 − F-HAMBRE, 1 − F-CANSANCIO, 1 − F-FRIO, la media) × el reposo del cuerpo;
        - recursos: la comida guardada, contando la bolsa, la despensa y su parte del almacén (W), frente a la que se comerá en dos días (lo que dura en la
          bolsa, de la cultura): R = meta × W / (W + k), con k tal que W = dos días da el reposo; más reservas la acercan a la meta del motor, menos la alejan;
        - vínculo: la hermana viva a la vista, por su vínculo, × el reposo del vínculo.
        Sin topes del siete: ninguna de las tres pasa por ellos"""
        V = CFG["vivir_bien"]; R0 = V["reposo_dos"]; pos = f["pos"]
        for k_, eje in (("V-CUERPO", (1.0, 0.0, 0.0)), ("V-RECURSOS", (0.0, 1.0, 0.0)), ("V-VINCULO", (0.0, 0.0, 1.0))):
            REPARTO.setdefault(k_, eje); APETITIVAS.add(k_)
        bien = [1.0 - min(1.0, F.get(k, 0.0)) for k in ("F-HAMBRE", "F-CANSANCIO", "F-FRIO")]
        F["V-CUERPO"] = R0["cuerpo"] * sum(bien) / len(bien)
        W = f["bolsa"].count("comida") + f["despensa_n"] + f["almacen_n"] / CFG["almacen"]["entre"]; n = max(1e-9, self.comidas_dos_dias(f["hambre"]))
        meta = DEFAULT_CONFIG.r_pos_target; k = n * (meta / R0["recursos"] - 1.0)
        if W > 0: F["V-RECURSOS"] = meta * W / (W + k)
        if not self.pareja_muerta and self.pareja_pos and self.cheb(pos, self.pareja_pos) <= self.vista_en(f.get("H", 0)): F["V-VINCULO"] = R0["vinculo"] * self.B
        if self.radar_v34: self._rad_filas_tener(f, F, pos)                 # (prompt 79) tener cerca a las suyas: su valor aprendido
        if self.sabores_v40 and f.get("sabor", 0.0) > 0:                    # (prompt 85) el placer de comer una comida sabrosa (lo aprendido de su fuente)
            REPARTO.setdefault("P-SABOR", REPARTO["P-COMER"]); APETITIVAS.add("P-SABOR"); F["P-SABOR"] = f["sabor"]

    def _siente_rg(self, obs, t):
        """(prompt 42, Manel) lo sentido en la regla general: al comer, el hambre que quitó (cuerpo); al conseguir algo nuevo o recibir, lo que cubre de la
        comida que le falta (recursos); al dar, lo que alivia del dolor por la otra (vínculo). Entra en su estado y se apaga a la mitad cada mirada"""
        if not self.rg_gan: return
        p = self.prev; antes, ahora = (p.get("bolsa") or []).count("comida"), obs["bolsa"].count("comida")
        def pon(fila, v):
            if v <= 0: return
            v0 = self.sentido.get(fila); v0 = v0[0] * 0.5 ** ((t - v0[1]) / T["mirada"]) if v0 else 0.0
            self.sentido[fila] = (max(v0, v), t)
        if p["accion"] == "comer" and p.get("tipo") == "comida" and obs["yo"]["hambre"] < p["hambre"]: pon("G-F-HAMBRE", self.dh(p["hambre"]) - self.dh(obs["yo"]["hambre"]))
        if ahora > antes and not self._robo and (p["accion"] != "coger" or p.get("de") in CFG["platos"]["conseguir_de"]):
            n = max(1.0, self.comidas_dos_dias()); falta0 = max(0.0, (n - antes) / n); pon("G-R-CARENCIA", min(falta0, (ahora - antes) / n))
        if p["accion"] == "dar" and len(obs["bolsa"]) < len(p.get("bolsa") or []) and p.get("a"): pon("S-DAR", self.valor_dar(p["a"], p.get("tipo"), vista=p.get("lleva_vista_v67")))

    def foto_ahora(self):
        yo = self.obs["yo"]; alm = CFG["almacen"]["comidas_por_nivel"].get(self.almacen_visto, 0) if self.almacen_visto else 0
        return {"pos": tuple(yo["pos"]), "vida": yo["vida"], "hambre": yo["hambre"], "cansancio": yo["cansancio"], "bolsa": list(self.obs["bolsa"]),
                "almacen_n": alm, "despensa_n": self.despensa_vista, "hermana_lleva": list(self.pareja_lleva), "ign_botiquin": self.cuaderno.ignorancia(self.botiquin),
                "lleva_otras": {x: list(d.get("lleva") or []) for x, d in self.otras.items()} if self.vecinas_on else {}, "H": 0}

    def comidas_dos_dias(self, h=None):
        """(prompt 39) las comidas que se comerá antes de que se pudran en la bolsa: el hambre que tendrá en ese tiempo (lo que sube por turno, que aprende,
        × lo que dura en la bolsa, que dice la cultura), sobre lo que cree que quita una comida"""
        dura = (self.campo("guardar:comida", "dura") or {}).get("bolsa") or 0
        sube = max(0.0, (self.pr_de("quedarse") or self.pr_de("otra") or {}).get("hambre", 0.0))
        h = self.obs["yo"]["hambre"] if h is None else h
        return (h + sube * dura) / max(1.0, self.cree_comida(max(1.0, h)))

    def falta_comida(self, f):
        n = self.comidas_dos_dias(f["hambre"])
        if n <= 0: return 0.0
        W = f["bolsa"].count("comida") + f["despensa_n"] + f["almacen_n"] / CFG["almacen"]["entre"] + f.get("W_trabajo", 0.0) + f.get("esperada", 0.0)
        return max(0.0, (n - W) / n)

    def falta_saber(self):
        """(prompt 39, Manel) saber dónde hay comida es un recurso: lo que le falta por conocer, frente a los matorrales que dice la cultura que hay"""
        dens = self.campo("matorral", "por_100_casillas") or 0.0; esperados = dens / 100.0 * len(self.celdas_de.get("bosque", []))
        if esperados <= 0: return 0.0
        return max(0.0, 1.0 - len(self.mat) / esperados)

    def tope_dar(self, tipo):
        """(prompt 39) dar con un tope: un pequeño esfuerzo, no tu vida. No da comida con su propia hambre por encima del umbral de «necesito ayuda», ni
        medicina con su vida por debajo del de «estoy herida»"""
        if self.tope_dar_off: return True                                   # (prompt 105) solo para probar: sin la regla
        yo = self.obs["yo"]; L = CFG["llamadas"]
        if tipo == "comida": return yo["hambre"] <= L["hambre_mayor_que"]
        if tipo == self.botiquin: return yo["vida"] >= L["herida_vida_menor_que"]
        return True

    def obs_vista(self):
        """el radio de vista: hasta dónde llega lo que ve ahora (prompt 39: de noche se ve menos; antes, 5 siempre, escrito a mano). Es percepción, no conducta"""
        o = getattr(self, "obs", None)
        if not o or not o.get("casillas"): return 5.0
        p = tuple(o["yo"]["pos"]); return float(max(max(abs(c["pos"][0] - p[0]), abs(c["pos"][1] - p[1])) for c in o["casillas"]))

    def fuentes_f(self, f):
        fu = dict(self.fuentes_sitio()); fu.update(self.fuentes)
        if f.get("almacen_n", 0) > 0:
            for q in self.almacen: fu[q] = self.valor_fuente(CFG["fuentes_de_botin"]["almacen"])
        return fu

    def riqueza_ahora(self):
        """(prompt 33, solo medir) lo que tiene: comida y medicina en la bolsa, y su parte del almacén (lo que vio la última vez, entre ocho)"""
        alm = CFG["almacen"]["comidas_por_nivel"].get(self.almacen_visto, 0) if self.almacen_visto else 0
        return self.obs["bolsa"].count("comida") + self.obs["bolsa"].count(self.botiquin) + alm / CFG["almacen"]["entre"]

    def vinculo_total(self):
        """(prompt 33, solo medir) la suma de sus vínculos: con la hermana (si vive) y con cada vecina viva"""
        return (0.0 if self.pareja_muerta else self.B) + sum(self.vin.values())

    # ── (prompt 128, taller) la cara y la voz de la base ──
    FILAS_DE_OTRAS = ("S-DANO-PAREJA", "R-HERMANO-FALTA", "F-HERMANO-AMENAZA", "S-PROVISION", "S-CARA")      # lo que viene de leer a otras: no sale en la cara
    FILAS_ALARMA = tuple(k for k in MI.FILAS_MIEDO if k not in ("F-HERMANO-AMENAZA", "S-COMPANIA", "R-ACOPIO")) + ("F-DANO",)     # miedo propio o dolor
    FILAS_PETICION = {"F-HAMBRE": "comida", "F-DANO": "cura"}                # (decisión de Manel) la petición de comida, solo del hambre del cuerpo
    FILAS_SIN_VOZ = ("R-CARENCIA",)                                         # (decisión de Manel) la falta de comida guardada no habla por la voz (se ve en la cara)
    FILAS_CONTACTO = {"S-SOLEDAD": "compania", "S-COMPANIA": "hermana"}

    def _F_propia_ahora(self):
        """la foto de ahora sin lo que viene de leer a otras (una vez por turno)"""
        t = self.obs["turno"]
        if self._cara_cache[0] != t:
            _, F = self.seis_ahora(); Fp = {k: v for k, v in F.items() if k not in self.FILAS_DE_OTRAS}
            st, _ = self._compone(Fp); self._cara_cache = (t, (Fp, [round(st.pF - st.nF, 4), round(st.pR - st.nR, 4), round(st.pS - st.nS, 4)], st))
        return self._cara_cache[1]

    def _intensidad(self, fila, st):
        """(decisión de Manel tras la prueba) la intensidad: la fuerza de pérdida de la dimensión de esa fila en su estado (sin lo de otras), con los tres tramos
        de la expresión (tercios de la mitad del techo de volumen, `_expresion_calc`). Solo fija el alcance"""
        rep = REPARTO.get(fila) or (1.0, 1.0, 1.0); dim = max(range(3), key=lambda i: rep[i]); v = (st.nF, st.nR, st.nS)[dim]; u = VOL_MAX / 6.0
        return "suave" if v < u else ("medio" if v < 2 * u else "fuerte")

    def _voz_propia(self, obs):
        """la voz que sale sola: la fila (de pérdida) que más pesa en la foto de ahora (sin lo de otras), su clase, su objeto, su tamaño y su intensidad. Solo
        hay alarma con miedo o dolor fuertes; la petición y el contacto llegan como mucho a la llamada normal. Se emite cuando cambia, o cada mirada si sigue"""
        Fp, _, st = self._F_propia_ahora()
        perd = [(k, v) for k, v in Fp.items() if v > 0 and k not in APETITIVAS and not k.startswith(("G-", "V-", "P-")) and k in REPARTO and k not in self.FILAS_SIN_VOZ]
        if self.ya_tiene_v67:                                               # (prompt 131) no pide lo que ya lleva (salvo que sea una alarma)
            lleva_ = {"comida": "comida" in obs["bolsa"], "cura": self.botiquin in obs["bolsa"]}
            perd = [(k, v) for k, v in perd if not (k in self.FILAS_PETICION and lleva_[self.FILAS_PETICION[k]] and not (k in self.FILAS_ALARMA and self._intensidad(k, st) == "fuerte"))]
        if self.voz_piezas_v68:                                             # (prompt 132) solo hablan las filas de las clases encendidas
            def clase_(k):
                if k in self.FILAS_ALARMA and self._intensidad(k, st) == "fuerte": return "alarma"
                return "peticion" if k in self.FILAS_PETICION else ("contacto" if k in self.FILAS_CONTACTO else None)
            perd = [(k, v) for k, v in perd if clase_(k) in self.voz_piezas_v68 or clase_(k) is None]
        if not perd: return None
        k, M = max(perd, key=lambda kv: (kv[1] * max(REPARTO[kv[0]]), kv[0])); it = self._intensidad(k, st)
        if k in self.FILAS_ALARMA and it == "fuerte": v = {"clase": "alarma", "fila": k, "objeto": "bestia" if k in ("F-4-ALCANCE", "S-8-EXPOSICION") else ("herida" if k == "F-DANO" else "peligro")}
        elif k in self.FILAS_PETICION: v = {"clase": "peticion", "fila": k, "objeto": self.FILAS_PETICION[k]}
        elif k in self.FILAS_CONTACTO: v = {"clase": "contacto", "fila": k, "objeto": self.FILAS_CONTACTO[k]}
        else: return None
        v.update(cuanto=round(M, 4), intensidad=it); clave = (v["clase"], k, v["objeto"], it); t = obs["turno"]
        if self._voz_ultima is not None and self._voz_ultima[0] == clave and t - self._voz_ultima[1] < T["mirada"]: return None
        self._voz_ultima = (clave, t); return v

    def _para(self, obs):
        """(para_v64) me han empujado o me han quitado algo: un «para» a quien lo hace; su tamaño, lo que perdí (comida / WT, como el robo en el radar)"""
        for e in obs.get("empujones_vistos") or []:
            de, a, w = e.get("de"), e.get("a"), e.get("gana")
            if a == self.a and de and de != self.a: ag = de
            elif de == self.a and w and w != self.a: ag = w
            else: continue
            n_ = (e.get("soltado") or []).count("comida") if w != self.a else 0; M = float(n_) / self.WT; fila = "R-CARENCIA" if n_ else "S-7-AGRESOR"
            return {"clase": "para", "fila": fila, "objeto": "quien_empuja", "a": ag, "cuanto": round(M, 4), "intensidad": self._intensidad(fila, self._F_propia_ahora()[2])}
        return None

    @staticmethod
    def _inversa(fn, y, hi):
        """el x de [0, hi] con fn(x) = y (fn creciente), por bisección; sin números nuevos"""
        if y <= fn(0.0): return 0.0
        if y >= fn(hi): return hi
        lo = 0.0
        for _ in range(40):
            m = 0.5 * (lo + hi)
            if fn(m) < y: lo = m
            else: hi = m
        return 0.5 * (lo + hi)

    def _vivido(self, objeto):
        """(prompt 128) si tiene algún recuerdo vivido de esa cosa (en cualquier situación): ni visto ni heredado"""
        for recs in ((self.cuaderno.objetos.get(objeto) or {}).get("situaciones") or {}).values():
            if any(r.get("origen") in (None, "vivido") for r in recs): return True
        return False

    def _cara_de(self, x):
        """la cara de x si la he visto en esta mirada; si no, None"""
        t = self.obs["turno"]
        c = self.pareja_cara if x == self.hermana else (self.otras.get(x) or {}).get("cara_v")
        return c[1] if c and t - c[0] <= T["mirada"] else None

    def hambre_cara(self, x):
        """el hambre que le leo en la cara: la que me daría a mí ese dolor de cuerpo (su balance de cuerpo negativo / el reparto de F-HAMBRE, invertido con dh)"""
        c = self._cara_de(x)
        if c is None: return None
        need = max(0.0, -c[0]) / max(REPARTO["F-HAMBRE"])
        return self._inversa(self.dh, need, self.hambre_max)

    def _pide_v65(self, x, objeto):
        """(prompt 130) el tamaño de lo que x me ha pedido (su fila, el cuánto de su voz) si se lo he oído en la mirada; si no, None"""
        p = self.pide_v65.get(x); ven_ = 1 if self.ya_tiene_v67 else T["mirada"]     # (prompt 131) de este turno o del anterior
        return p[2] if p and p[1] == objeto and self.obs["turno"] - p[0] <= ven_ else None

    def ve_que_lleva(self, x, tipo):
        """(prompt 131, ya_tiene_v67) ¿veo que la otra lleva eso? Lo que se ve de su bolsa, ahora"""
        c = next((c for c in self.obs["criaturas"] if c["id"] == x), None)
        return c is not None and tipo in (c.get("lleva") or [])

    def hambre_dar(self, x):
        """(prompt 130) el hambre que dice su petición de comida: su F-HAMBRE (el cuánto) invertido con dh, como mi propia F-HAMBRE; sin petición, None"""
        cu = self._pide_v65(x, "comida")
        return None if cu is None else self._inversa(self.dh, cu, self.hambre_max)

    def dano_dar(self, x):
        """(prompt 130) el daño que dice su petición de cura: su F-DANO (el cuánto); sin petición, None"""
        return self._pide_v65(x, "cura")

    def seis_ahora(self):
        """(prompt 32) las seis, en la foto de ahora (lo que hay, sin imaginar nada): solo para medir; no cambia ninguna decisión"""
        yo = self.obs["yo"]; alm = CFG["almacen"]["comidas_por_nivel"].get(self.almacen_visto, 0) if self.almacen_visto else 0
        f = {"pos": tuple(yo["pos"]), "vida": yo["vida"], "hambre": yo["hambre"], "cansancio": yo["cansancio"], "bolsa": list(self.obs["bolsa"]),
             "almacen_n": alm, "despensa_n": self.despensa_vista, "hermana_lleva": list(self.pareja_lleva), "ign_botiquin": self.cuaderno.ignorancia(self.botiquin),
             "lleva_otras": {x: list(d.get("lleva") or []) for x, d in self.otras.items()} if self.vecinas_on else {}}
        F = self.filas(f); return seis(F, self._rep), F

    # ── la foto de cada candidato ──
    def foto(self, acc, antes=None, al_final=False):
        """la foto de un candidato a H turnos. (prompt 15) Con `antes` (un `comer`): primero come (un turno) y luego hace `acc` en los turnos que quedan"""
        yo = self.obs["yo"]; bolsa = list(self.obs["bolsa"])
        alm = CFG["almacen"]["comidas_por_nivel"].get(self.almacen_visto, 0) if self.almacen_visto else 0
        f = {"pos": tuple(yo["pos"]), "vida": yo["vida"], "hambre": yo["hambre"], "cansancio": yo["cansancio"], "bolsa": bolsa,
             "almacen_n": alm, "despensa_n": self.despensa_vista, "hermana_lleva": list(self.pareja_lleva), "ign_botiquin": self.cuaderno.ignorancia(self.botiquin),
             "lleva_otras": {x: list(d.get("lleva") or []) for x, d in self.otras.items()} if self.vecinas_on else {}}
        t = acc["accion"]; H = T["mirada"]; f["H"] = H
        if al_final: H -= 1                                                 # (prompt 17) el último turno de la mirada es para comer
        if antes is not None:
            self._come(f, antes.get("tipo")); H -= 1; bolsa = list(f["bolsa"])
            pr = self.pr_de(self.clase_de(antes))
            f["cansancio"] += pr.get("cans", 0.0); f["hambre"] += pr.get("hambre", 0.0); f["vida"] += pr.get("vida", 0.0)
        # la foto se mira a H turnos (la mirada del siete): los pasos que da y, el resto, quieta
        pasos = 0; camino = []
        if t == "ir" and acc.get("ronda"):                                  # (prompt 43) la ronda: un tramo tras otro, mientras quepa en la mirada
            p0 = f["pos"]; f["ronda_llega"] = []
            for q in acc["ronda"]:
                tramo = self.camina(p0, {"accion": "ir", "destino": tuple(q)})
                if not tramo or len(camino) + len(tramo) > H: break
                camino += tramo; p0 = tramo[-1]
                if p0 == tuple(q): f["ronda_llega"].append(tuple(q))
            pasos = len(camino)
            if camino: f["pos"] = camino[-1]
        elif t == "mover" or t == "ir":
            camino = self.camina(f["pos"], acc)[:H] ; pasos = len(camino)
            if camino: f["pos"] = camino[-1]
        clases = [("mover", pasos), (self.clase_de(acc) if t not in ("mover", "ir") else "quedarse", 1 if t not in ("mover", "ir") else 0), ("quedarse", max(0, H - pasos - (0 if t in ("mover", "ir") else 1)))]
        q_tp = acc.get("planta_obj")                                       # (prompt 14) trabajar_planta: ir junto a la planta y trabajar lo que le falta
        if q_tp is not None and self.anticipa:
            q_tp = tuple(q_tp); llega = (t == "trabajar") or (f["pos"] in self.junto_a(q_tp))
            falta = max(0, (self.campo("trabajar", "por_turnos") or 0) - self.plantas_vistas[q_tp]["trabajo"])
            k = min(falta, max(0, H - pasos)) if llega else 0
            if self.sabe_reglas_trabajo and self.reglas.get("no_se_trabaja_de_noche"):      # (prompt 26) solo los turnos de trabajo que caben antes de la noche
                hn = self.hasta_noche(); k = min(k, max(0, (hn if hn is not None else H) - pasos))
            clases = [("mover", pasos), ("trabajar", k), ("quedarse", max(0, H - pasos - k))]
            f["W_trabajo"] = self.promesa_trabajo(q_tp, k)
        Hn = H                                                              # (prompt 56) la noche entera: al decidir dónde dormir, hasta la mañana
        if self.noche_entera_v18 and self.obs["fase"] in ("anochecer", "noche") and (t == "dormir" or (t == "ir" and acc.get("que") == "ir_casa")):
            r_, rd_ = self.campo("trabajar", "retraso"), self.campo("trabajar", "retraso_dias"); dia_ = int(r_ / rd_) if (r_ and rd_) else 400
            Hn = max(H, dia_ - int(self.obs["turno_del_dia"]))
            if t == "dormir": clases = [("dormir", Hn)]
            elif f["pos"] == tuple(acc["destino"]): clases = [("mover", pasos), ("dormir", max(0, Hn - pasos))]
            else: Hn = H
        dorm_extra = 0
        if self.horizonte_v50 and self.noche_entera_v18 and self.obs["fase"] in ("anochecer", "noche"):      # (prompt 96) todas hasta la mañana: lo que hace y después dormir
            r_, rd_ = self.campo("trabajar", "retraso"), self.campo("trabajar", "retraso_dias"); dia_ = int(r_ / rd_) if (r_ and rd_) else 400
            Hn_ = max(H, dia_ - int(self.obs["turno_del_dia"])); usado = sum(n for _, n in clases)
            if usado < Hn_: dorm_extra = Hn_ - usado; clases = list(clases) + [("dormir", dorm_extra)]
            Hn = max(Hn, Hn_)
        if (self.dormir_en_casa or self.rg) and self.obs["fase"] in ("anochecer", "noche"):      # (prompt 39) la regla general se queda el hecho (dormida fuera, la bestia te pega), no la orden
            if self.dormir_en_casa and t == "ir" and acc.get("que") == "ir_casa" and f["pos"] == tuple(acc["destino"]):      # (prompt 22) ir a casa al anochecer es ir a dormir: el resto de la mirada, dormida
                clases = [("mover", pasos), ("dormir", max(0, H - pasos))]
            if (t == "dormir" or dorm_extra) and f["pos"] not in self.todas_casas:          # dormir fuera: lo que dice el cuaderno que quita una noche dormida fuera, por la parte de la noche que mira; (96) también después de otra cosa
                v = self.cree("dormir", "fuera", "cuerpo"); emp = self.campo("bestia", "empieza")
                r, rd = self.campo("trabajar", "retraso"), self.campo("trabajar", "retraso_dias")
                nd = Hn if t == "dormir" else dorm_extra
                if v and emp and r and rd: f["vida"] += min(0.0, v) * min(1.0, nd / max(1.0, r / rd - emp))
        if self.cultura is not None:                                        # (prompt 14) lo que cree que quita estar en cada sitio, por turno
            dn = self.dn(self.obs["fase"]); resto = Hn - pasos
            f["vida"] += sum(self.dano_sitio(self.terreno(c), dn) for c in camino) + resto * self.dano_sitio(self.terreno(f["pos"]), dn)
        for k, n in clases:
            pr = self.pr_de(k)                                              # (prompt 94) por la hora y el sitio (sin prop_ctx_v48, lo de antes)
            f["cansancio"] += n * pr.get("cans", 0.0); f["hambre"] += n * pr.get("hambre", 0.0); f["vida"] += n * pr.get("vida", 0.0)
        kf = self.reglas.get("frio_hambre_por_grado") if self.frio_sabe_v17 else None
        if kf and self.obs.get("temperatura_fuera") is not None and self.reglas.get("temperatura_confort"):      # (prompt 55) el frío en la foto
            lo = self.reglas["temperatura_confort"][0]; fac = lambda q: 1.0 + kf * max(0.0, lo - self.obs["temperatura_fuera"]) if q not in self.todas_casas else 1.0
            ahora = fac(tuple(yo["pos"]))
            k0 = 0                                                          # (prompt 65) con el reloj de dentro, cada turno con el frío de su fase
            for k, n in clases:
                if not n: continue
                ph = self.pr_de(k).get("hambre", 0.0)
                if self.reloj_dentro_v27:
                    if k == "mover" and camino:
                        extra = sum(ph * ((1.0 + kf * max(0.0, lo - (self.frio_en(k0 + 1 + i) or lo)) if c not in self.todas_casas else 1.0) / ahora - 1.0) for i, c in enumerate(camino[:n]))
                    else: extra = ph * ((n + (kf * self.frio_tramo(k0, n, lo) if f["pos"] not in self.todas_casas else 0.0)) / ahora - n)
                    k0 += n
                elif k == "mover" and camino: extra = sum(ph * (fac(c) / ahora - 1.0) for c in camino[:n])
                else: extra = n * ph * (fac(f["pos"]) / ahora - 1.0)
                f["hambre"] += extra
        f["cansancio"] = min(self.cans_max, max(0.0, f["cansancio"])); f["hambre"] = min(self.hambre_max, max(0.0, f["hambre"])); f["vida"] = min(self.vida_max, max(0.0, f["vida"]))
        if self.vecinas_on and t == "ir" and acc.get("que") == "ir_vecina":  # (prompt 28) llega a la vecina y le da lo que necesita (comida o medicina)
            x = acc["quien"]; d = self.otras.get(x) or {}
            if d.get("pos") and max(abs(f["pos"][0] - d["pos"][0]), abs(f["pos"][1] - d["pos"][1])) <= 1:
                lleva = f["lleva_otras"].setdefault(x, [])
                for tipo, cond in (("comida", d.get("flaca")), (self.botiquin, d.get("herida"))):
                    if cond and tipo in f["bolsa"] and tipo not in lleva and (not self.rg or self.tope_dar(tipo)):
                        b2 = list(f["bolsa"]); b2.remove(tipo); f["bolsa"] = b2; f["lleva_otras"][x] = lleva + [tipo]; f["dio"] = (x, tipo); break
        es_b = self.bestia_v44 and t in ("empujar", "golpear") and str(acc.get("a") or "").startswith("bestia")      # (prompt 89)
        if es_b: self._foto_bestia_g(f, t, acc)
        # (prompt 90, Manel) todas las versiones reconocen como bestia a cualquier bestia, se llame como se llame: su casilla y lo que lleva, los de esa bestia
        vb_ = self._bestia_ve(acc.get("a")) if (t in ("empujar", "golpear") and es_bestia(acc.get("a"))) else None
        qb_, lleva_b_ = vb_ if vb_ is not None else (self.bestia, list((self.obs.get("bestia") or {}).get("lleva") or []))
        if (self.enfado_on or self.rg) and qb_ is not None and ((t == "empujar" and es_bestia(acc.get("a")) and not es_b) or (t == "ir" and acc.get("que") == "ir_bestia" and max(abs(f["pos"][0] - qb_[0]), abs(f["pos"][1] - qb_[1])) <= 1)):
            # (prompt 27) el empujón imaginado: ganan si las pegadas a la bestia (ella, las que ya están pegadas y la hermana si va pegada a ella) llegan a lo que cuenta la bestia
            otras = {c["id"] for c in self.obs["criaturas"] if max(abs(c["pos"][0] - qb_[0]), abs(c["pos"][1] - qb_[1])) <= 1}
            if t != "empujar" and self.pareja_vista and self.pareja_pos and max(abs(self.pareja_pos[0] - tuple(self.obs["yo"]["pos"])[0]), abs(self.pareja_pos[1] - tuple(self.obs["yo"]["pos"])[1])) <= 1:
                otras.add(self.hermana)      # al acercarse, la hermana pegada a ella irá con ella; al empujar, solo cuentan las pegadas a la bestia (como en el mundo)
            gana = 1 + len(otras) >= int(self.reglas.get("bestia_cuenta_como") or 2)
            if gana:
                f["recupera"] = True
                if self.rg: f["bolsa"] = (list(f["bolsa"]) + ["comida"] * lleva_b_.count("comida"))[:6]     # (prompt 39) recupera lo que lleva la bestia
                elif self.enfado and self.enfado["de"] == "yo": f["bolsa"] = list(f["bolsa"]) + ["comida"] * self.enfado["n"]
            else: f["vida"] = max(0.0, f["vida"] - float(self.reglas.get("golpe_bestia") or 0))
        if self.rg and t == "golpear" and not es_b:                         # (prompt 39) golpear: a la bestia, que devuelve el golpe; a otra, el daño que le hace
            if es_bestia(acc.get("a")): f["vida"] = max(0.0, f["vida"] - float(self.reglas.get("golpe_bestia") or 0))
            else:
                f["dano_a"] = (acc.get("a"), float(self.reglas.get("golpe_criatura") or 0))
                x_ = acc.get("a"); niv = self.pareja_vida_nivel if x_ == self.hermana else (self.otras.get(x_) or {}).get("vida_nivel")
                if self.ve_vida_v9 and niv == "moribunda": f["mata_a"] = x_              # (prompt 47) se ve que un golpe la mata
        if self.rg and t == "empujar" and acc.get("a") is not None and not es_bestia(acc.get("a")):     # (prompt 39) empujar a otra: gana el bando mayor (las de cada casa pegadas a la escena)
            x = acc["a"]; d = self.otras.get(x) or {}; xp = d.get("pos"); yo_p = tuple(self.obs["yo"]["pos"])
            mia = 1 + int(x != self.hermana and not self.pareja_muerta and self.pareja_pos is not None and xp is not None and min(self.cheb(self.pareja_pos, yo_p), self.cheb(self.pareja_pos, xp)) <= 1)
            suya = 1 + sum(1 for y, e in self.otras.items() if y != x and y[0] == x[0] and e.get("pos") and xp and min(self.cheb(e["pos"], yo_p), self.cheb(e["pos"], xp)) <= 1)
            lleva = (d.get("lleva") or []) if x != self.hermana else list(self.pareja_lleva)
            if mia > suya and lleva:
                n_ = lleva.count("comida"); f["bolsa"] = (list(f["bolsa"]) + ["comida"] * n_)[:6]; f["empuja_a"] = (x, n_)
            elif mia < suya: f["bolsa"] = []
        if self.responde and t == "ir" and acc.get("que") == "ir_llamada" and "comida" not in f["bolsa"] and f["pos"] == tuple(acc["destino"]) and tuple(acc["destino"]) in self.comida_oida:
            P = self.comida_oida[tuple(acc["destino"])][1]                  # (prompt 24) la promesa de una comida, por lo que vale la llamada (vínculo × cercanía)
            if P > 0 and self.rg: f["esperada"] = f.get("esperada", 0.0) + P      # (prompt 39) la llamada es información: allí hay comida (un recurso)…
            if P > 0: f["hambre"] = max(0.0, f["hambre"] - P * self.cree_comida(f["hambre"])); f["prometido"] = True      # …y la comida sirve al cuerpo
        if self.v7 and t == "ir" and acc.get("que") in ("ir_matorral", "ir_bosque", "ir_ronda") and "comida" not in f["bolsa"] and not (self.promesa_una and f.get("comio")):
            # (prompt 19) la promesa del prompt 10 por la probabilidad de encontrar fruto dentro de la mirada (sin números nuevos: todo del cuaderno)
            if acc["que"] == "ir_matorral": P = self.p_matorral(tuple(acc["destino"])) if f["pos"] == tuple(acc["destino"]) else 0.0
            elif acc["que"] == "ir_ronda":                                  # (prompt 43) encontrar algo en alguno de los que alcanza
                nada = 1.0
                for q in f.get("ronda_llega") or []: nada *= 1.0 - self.p_matorral(q)
                P = 1.0 - nada
            else:
                dens = self.campo("matorral", "por_100_casillas") or 0.0; vista = 2 * int(self.obs_vista()) + 1
                pasos_bosque = sum(1 for c in camino if self.terreno(c) == "bosque")
                if self.reloj_dentro_v27:                                   # (prompt 65) lo que verá en cada paso
                    vb = sum(2 * int(self.vista_en(i + 1)) + 1 for i, c in enumerate(camino) if self.terreno(c) == "bosque"); P = min(1.0, dens / 100.0 * vb * self.p_fruto("bosque"))
                else: P = min(1.0, dens / 100.0 * pasos_bosque * vista * self.p_fruto("bosque"))
            if P > 0 and self.rg: f["esperada"] = f.get("esperada", 0.0) + P      # (prompt 39) el fruto que espera encontrar: un recurso…
            if P > 0: f["hambre"] = max(0.0, f["hambre"] - P * self.cree_comida(f["hambre"])); f["prometido"] = True      # …y sirve al cuerpo (la tabla de Manel: comida, cuerpo y recursos)
        if self.dar_comida and t == "ir" and acc.get("que") == "ir_pareja" and self.pareja_flaca and "comida" in f["bolsa"] and "comida" not in f["hermana_lleva"] and (not self.rg or self.tope_dar("comida")) \
                and max(abs(f["pos"][0] - self.pareja_pos[0]), abs(f["pos"][1] - self.pareja_pos[1])) <= 1:
            b2 = list(f["bolsa"]); b2.remove("comida"); f["bolsa"] = b2; f["hermana_lleva"] = f["hermana_lleva"] + ["comida"]; f["dio"] = (self.hermana, "comida")       # (prompt 23) llega a ella y le da
        if self.para_que_v31 and t == "ir" and acc.get("que") == "ir_pareja" and self.pareja_herida and self.pareja_pos is not None and self.botiquin in f["bolsa"] \
                and self.botiquin not in f["hermana_lleva"] and (not self.rg or self.tope_dar(self.botiquin)) and self.cheb(f["pos"], self.pareja_pos) <= 1:
            b2 = list(f["bolsa"]); b2.remove(self.botiquin); f["bolsa"] = b2; f["hermana_lleva"] = f["hermana_lleva"] + [self.botiquin]
            f["dio"] = (self.hermana, self.botiquin)                        # (prompt 76) llega a ella y le da la medicina (si también le dio comida, cuenta la medicina)
        if self.para_que_v31 and t == "ir" and acc.get("que") == "ir_botin" and f["pos"] == tuple(acc["destino"]) and len(f["bolsa"]) < 6:
            q_b = tuple(acc["destino"]); acceso = {tuple(x) for x in self.mp["almacen_acceso"]}      # (prompt 76) llega al botín y coge lo que hay
            if q_b in self.fuentes:                                          # comida vista en el suelo o fruto en una planta: algo nuevo
                self.promete(f, "comida"); f["bolsa"] = f["bolsa"] + ["comida"]; f["consigue"] = f.get("consigue", 0) + 1; f["consigue_tipos"] = f.get("consigue_tipos", []) + ["comida"]
            elif q_b in acceso and f.get("almacen_n", 0) > 0:                # una del almacén (sacar no es conseguir)
                self.promete(f, "comida"); f["bolsa"] = f["bolsa"] + ["comida"]; f["almacen_n"] = max(0, f["almacen_n"] - 1)
        if t == "ir" and acc.get("recoger") and f["pos"] == acc["destino"] and len(bolsa) < 6:            # llega y lo coge (cadena del siete)
            self.promete(f, acc["recoger"]); f["bolsa"] = bolsa + [acc["recoger"]]; f["consigue"] = f.get("consigue", 0) + 1; f["consigue_tipos"] = f.get("consigue_tipos", []) + [acc["recoger"]]      # (prompt 34) consigue algo
        elif t == "coger":
            self.promete(f, acc.get("tipo") or "comida"); f["bolsa"] = bolsa + [acc.get("tipo") or "comida"]
            if (acc.get("tipo") or "comida") in ("comida", self.botiquin) and (not self.platos_v23 or acc.get("de") in CFG["platos"]["conseguir_de"]):
                f["consigue"] = f.get("consigue", 0) + 1; f["consigue_tipos"] = f.get("consigue_tipos", []) + [acc.get("tipo") or "comida"]     # (prompt 34; 35: solo lo nuevo)
            es_comida = (acc.get("tipo") or "comida") == "comida" or not self.cuenta_despensa_v23          # (prompt 61) solo la comida es comida guardada
            if acc.get("de") == "almacen" and es_comida: f["almacen_n"] = max(0, alm - 1)
            if acc.get("de") == "despensa" and es_comida: f["despensa_n"] = max(0, f["despensa_n"] - 1)
        elif t in ("dejar", "dar", "comer"):
            tipo = acc.get("tipo"); b2 = list(bolsa)
            if tipo in b2: b2.remove(tipo)
            f["bolsa"] = b2
            es_comida = tipo == "comida" or not self.cuenta_despensa_v23                                    # (prompt 61) solo la comida es comida guardada
            if t == "dejar" and acc.get("en") == "almacen" and es_comida: f["almacen_n"] = alm + 1
            if t == "dejar" and acc.get("en") == "despensa" and es_comida: f["despensa_n"] += 1
            if t == "dar": f["dio"] = (acc.get("a"), tipo)                                   # (prompt 34)
            if t == "dar" and self.sabores_v40 and acc.get("origen"): f["dio_origen"] = acc["origen"]      # (prompt 85) qué comida da
            if t == "dar" and acc.get("a") == self.hermana: f["hermana_lleva"] = f["hermana_lleva"] + [tipo]
            elif t == "dar" and self.vecinas_on and acc.get("a") in f["lleva_otras"]: f["lleva_otras"][acc["a"]] = f["lleva_otras"][acc["a"]] + [tipo]     # (prompt 28)
            if t == "comer":
                f["usa"] = tipo
                if tipo == "comida":
                    h0 = f["hambre"]; f["hambre"] = max(0.0, f["hambre"] - self.cree_comida(f["hambre"]))
                    f["gusto"] = f.get("gusto", 0.0) + self.gusto(h0, f["hambre"])     # (prompt 34)
                    org_ = acc.get("origen") or (self.origen_primera() if self.sabores_v43 else None)      # (prompt 88) sin origen, el de la primera de la bolsa
                    if self.sabores_v40 and org_: f["sabor"] = f.get("sabor", 0.0) + self.valor_sabor(org_) * self.factor_gusto(h0)      # (prompt 85) su sabor; (95) con su hambre
                else: f["vida"] = min(self.vida_max, f["vida"] + (self.cuaderno.creencia_cuerpo(tipo, "valle") or 0.0))
                if tipo == self.botiquin:                               # probarlo enseña: la ignorancia baja como con un recuerdo más
                    f["ign_botiquin"] = CU.PESO_NEUTRO / (CU.PESO_NEUTRO + self.cuaderno.pesos_vividos(tipo) + 1.0)
        if al_final and "comida" in f["bolsa"] and not (self.promesa_una and f.get("prometido")):
            self._come(f, "comida"); pr = self.pr_de("otra")
            f["cansancio"] = min(self.cans_max, max(0.0, f["cansancio"] + pr.get("cans", 0.0))); f["hambre"] = min(self.hambre_max, max(0.0, f["hambre"] + pr.get("hambre", 0.0)))
        if self.devolver_v57 and f.get("dio") and self.devolver_necesidad_v60 and self.es_devolucion(*f["dio"]):      # (prompt 112) devolver: sin gesto; el alivio, solo si lo necesita más que yo
            f["sin_gesto"] = True; x, tp = f["dio"]
            if not self.necesita_mas(x, tp):                                # (el gusto se queda como siempre)
                f["sin_alivio"] = True
                if x == self.hermana and tp in f["hermana_lleva"]: hl = list(f["hermana_lleva"]); hl.remove(tp); f["hermana_lleva"] = hl      # (no le quita ninguna falta)
                elif x in (f.get("lleva_otras") or {}) and tp in f["lleva_otras"][x]: lo = list(f["lleva_otras"][x]); lo.remove(tp); f["lleva_otras"][x] = lo
        elif self.devolver_v57 and f.get("dio") and self.devolver_solo_gesto_v59 and self.es_devolucion(*f["dio"]):      # (prompt 111) devolver quita solo el gesto
            f["sin_gesto"] = True
        elif self.devolver_v57 and f.get("dio") and self.es_devolucion(*f["dio"]):    # (prompt 109) devolver lo que me acaba de dar: ni gesto, ni alivio, ni gusto
            x, tp = f["dio"]; f["devuelve"] = True
            if x == self.hermana and tp in f["hermana_lleva"]: hl = list(f["hermana_lleva"]); hl.remove(tp); f["hermana_lleva"] = hl      # (no le quita ninguna falta)
            elif x in (f.get("lleva_otras") or {}) and tp in f["lleva_otras"][x]: lo = list(f["lleva_otras"][x]); lo.remove(tp); f["lleva_otras"][x] = lo
        if self.ya_tiene_v67 and f.get("dio") and self.ve_que_lleva(*f["dio"]): f["sin_alivio"] = True     # (prompt 131, principio de Manel) ya lleva su medicina: imaginarla curada por la mía no es ganancia
        return f

    def necesita_mas(self, x, tipo):
        """(prompt 112, devolver_necesidad_v60) ¿la otra lo necesita más que yo, por lo que veo de ella? La medicina: la vida que le supongo (su nivel de vida,
        hp_supuesta) por debajo de la mía. La comida: el hambre que le supongo (hambre_vista: flaca o no) por encima de la mía. Sin verla, no"""
        c = next((c for c in self.obs["criaturas"] if c["id"] == x), None)
        if c is None: return False
        yo = self.obs["yo"]
        if tipo == self.botiquin: return self.hp_supuesta(bool(c.get("herida")), c.get("vida_nivel")) < yo["vida"]
        return self.hambre_vista(x) > yo["hambre"]

    def es_devolucion(self, x, tipo):
        """(prompt 109, devolver_v57) ¿me lo dio ella misma hace menos de 40 turnos (la medida de las rachas)? Lo que he visto recibir, en `_recibidos`"""
        t0 = self._recib.get((x, tipo)); return t0 is not None and self.obs["turno"] - t0 < int(CFG["dar_v57"]["devolver_turnos"])

    def _recibidos(self, obs):
        """(prompt 109, devolver_v57) quién me ha dado qué: mi bolsa gana algo que no he cogido (ni ganado en un empujón) y una de las pegadas pierde eso mismo
        este turno (lo que se ve de su bolsa). Se apunta con el turno"""
        from collections import Counter as _C
        t = obs["turno"]; pos = tuple(obs["yo"]["pos"]); ahora = {c["id"]: _C(c.get("lleva") or []) for c in obs["criaturas"]}
        p = self.prev or {}; mio0, mio1 = _C(p.get("bolsa") or []), _C(obs["bolsa"])
        gane = any(e.get("gana") == self.a for e in (obs.get("empujones_vistos") or []))
        if p.get("accion") not in ("coger", "empujar") and not gane:
            for tp in ("comida", self.botiquin):
                sale = 1 if (p.get("accion") in ("dar", "comer", "dejar") and (p.get("tipo") or "comida") == tp) else 0      # lo que di, comí o dejé yo: un cambio a la vez no mueve la bolsa
                if mio1[tp] + sale <= mio0[tp]: continue
                for c in obs["criaturas"]:
                    x = c["id"]
                    if x in self._lleva_prev_v57 and self.cheb(tuple(c["pos"]), pos) <= 1 and self._lleva_prev_v57[x][tp] - ahora[x][tp] >= 1: self._recib[(x, tp)] = t
                    elif self.devolver_v58 and sale and p.get("accion") == "dar" and p.get("a") == x and self.cheb(tuple(c["pos"]), pos) <= 1: self._recib[(x, tp)] = t      # (prompt 110) a la vez: su bolsa no cambia
        self._lleva_prev_v57 = ahora

    def _come(self, f, tipo):
        """lo que imagina que hace comer `tipo` (lo mismo que la rama `comer` de la foto)"""
        b2 = list(f["bolsa"])
        if tipo in b2: b2.remove(tipo)
        f["bolsa"] = b2; f["usa"] = tipo; f["comio"] = True
        if tipo == "comida":
            h0 = f["hambre"]; f["hambre"] = max(0.0, f["hambre"] - self.cree_comida(f["hambre"]))
            f["gusto"] = f.get("gusto", 0.0) + self.gusto(h0, f["hambre"])     # (prompt 34) el hambre que quita, en la cuesta de F-HAMBRE
            if self.sabores_v43:                                                # (prompt 88) su sabor también aquí: la primera comida de la bolsa
                org_ = self.origen_primera()
                if org_: f["sabor"] = f.get("sabor", 0.0) + self.valor_sabor(org_) * self.factor_gusto(h0)      # (prompt 95) con su hambre
        else: f["vida"] = min(self.vida_max, f["vida"] + (self.cuaderno.creencia_cuerpo(tipo, "valle") or 0.0))
        if tipo == self.botiquin: f["ign_botiquin"] = CU.PESO_NEUTRO / (CU.PESO_NEUTRO + self.cuaderno.pesos_vividos(tipo) + 1.0)

    def cree_comida(self, hambre):
        """(prompt 11) cuánto cree que le quita una comida: sin ningún recuerdo firme, todo el hambre que tiene (o lo que digan sus «al menos», si es más);
        con alguno, lo que dice el cuaderno"""
        if self.rapido_v28:                                                 # (prompt 67) guardado mientras el cuaderno no cambie (ni el día)
            k = (self.cuaderno.version, self.cuaderno.dia)
            if self._cc is None or self._cc[0] != k:
                rec = ((self.cuaderno.objetos.get("comida") or {}).get("situaciones") or {}).get("valle") or []
                self._cc = (k, self.cuaderno.creencia_cuerpo("comida", "valle") or 0.0, any(not r.get("al_menos") for r in rec))
            _, cree, firme = self._cc
            return cree if firme else max(hambre, cree)
        rec = ((self.cuaderno.objetos.get("comida") or {}).get("situaciones") or {}).get("valle") or []
        cree = self.cuaderno.creencia_cuerpo("comida", "valle") or 0.0
        if not any(not r.get("al_menos") for r in rec): return max(hambre, cree)
        return cree

    def promesa_hambre(self, hambre, bolsa):
        """(prompt 10) la promesa del siete, extendida a la comida: el alivio de F-HAMBRE que dice su creencia; servida (ya lleva), calla"""
        if "comida" in bolsa: return 0.0
        cree = self.cree_comida(hambre)
        return max(0.0, cuesta(hambre / self.hambre_max) - cuesta(max(0.0, hambre - cree) / self.hambre_max))

    def promete(self, f, tipo):
        """en la foto: lo que promete coger `tipo` (solo la comida tiene promesa contra el hambre)"""
        if self.promesa_una and f.get("comio"): return                    # (prompt 17) ya come en esta foto: la promesa no se cuenta otra vez
        if tipo == "comida" and "comida" not in f["bolsa"]:
            f["hambre"] = max(0.0, f["hambre"] - self.cree_comida(f["hambre"])); f["prometido"] = True

    def _dist_libre(self, meta, ocup):
        """(prompt 103, casa_v51) pasos hasta `meta` sin pisar las casillas ocupadas ahora (salvo la meta): el camino que rodea a quien está delante. BFS desde la
        meta con las mismas reglas de paso (Mapa.pasa); no toca jugadores.Mapa (la usa el tonto)"""
        D = {meta: 0}; q = deque([meta])
        while q:
            u = q.popleft()
            for dx, dy in DIRS.values():
                v = (u[0] + dx, u[1] + dy)
                if v not in D and v not in ocup and self.M.pasa(v, u): D[v] = D[u] + 1; q.append(v)
        return D

    def camina(self, pos, acc):
        """los pasos de la foto en H turnos: recto en una dirección (mover) o por el camino más corto a un destino (ir), sin pisar casillas ocupadas ahora"""
        H = T["mirada"]; ocup = {tuple(c["pos"]) for c in self.obs["criaturas"]} | ({self.bestia} if self.bestia else set()); out = []; p = pos
        if acc["accion"] == "mover":
            d = DIRS[acc["dir"]]
            for _ in range(H):
                q = (p[0] + d[0], p[1] + d[1])
                if not self.M.pasa(p, q) or q in ocup: break
                p = q; out.append(p)
            return out
        D = self._dist_libre(tuple(acc["destino"]), ocup) if (self.casa_v51 and acc.get("que") == "ir_casa") else self._dist_a(acc["destino"])     # (prompt 103) rodea
        for _ in range(H):
            if p == acc["destino"]: break
            sig = min((q for q in ((p[0] + dx, p[1] + dy) for dx, dy in DIRS.values()) if q in D and self.M.pasa(p, q) and (q not in ocup or q == acc["destino"])),
                      key=lambda q: (D[q], q), default=None)
            if sig is None or D[sig] >= D.get(p, 10 ** 9): break
            p = sig; out.append(p)
        return out

    def candidatos_ir(self):
        """ir al mejor objeto, al botín conocido y a la hermana (decisor del siete, D:448-472), con el paso de hoy por el camino más corto"""
        pos = tuple(self.obs["yo"]["pos"]); bolsa = self.obs["bolsa"]; out = []
        hambre = self.obs["yo"]["hambre"]; prom = self.promesa_hambre(hambre, bolsa)
        objs = {q: v for q, v in self.fuentes.items()}                    # lo recogible visto: comida en el suelo y plantas con fruto
        if objs and len(bolsa) < 6:
            q = max(sorted(objs), key=lambda q: (objs[q] + prom) / (1.0 + self.lejos(pos, q)))
            if q != pos: out.append({"accion": "ir", "que": "ir_objeto", "destino": q, "recoger": "comida"})
        fu = self.fuentes_f({"almacen_n": CFG["almacen"]["comidas_por_nivel"].get(self.almacen_visto, 0) if self.almacen_visto else 0})
        if fu:
            q = max(sorted(fu), key=lambda q: fu[q] * max(0.0, 1.0 - self.lejos(pos, q) / A.BOTIN_DIST_REF) ** A.BOTIN_EXP)
            if q in self.almacen:                                          # el almacén no se pisa: su sitio es una casilla pegada
                acc_ = [c for c in (tuple(x) for x in self.mp["almacen_acceso"]) if self.M.pasa(c, c)]
                q = min(acc_, key=lambda c: (self.lejos(pos, c), c))
            if q != pos: out.append({"accion": "ir", "que": "ir_botin", "destino": q})
        if self.pareja_pos and not self.pareja_muerta and self.pareja_pos != pos:
            out.append({"accion": "ir", "que": "ir_pareja", "destino": self.pareja_pos})
        if self.cultura is not None and self.medicinas and len(bolsa) < 6:  # (prompt 14) la medicina vista: ir a cogerla, como el botiquín del siete
            q = min(self.medicinas, key=lambda c: (self.lejos(pos, c), c))
            if q != pos: out.append({"accion": "ir", "que": "ir_objeto", "destino": q, "recoger": self.botiquin})
        if self.anticipa:
            sin_trabajo = self.sabe_reglas_trabajo and ((self.reglas.get("no_se_trabaja_de_noche") and self.obs["fase"] == "noche")
                                                         or (self.reglas.get("no_se_trabaja_sin_fuerzas") and self.obs["yo"]["hambre"] >= self.hambre_max))
            for q in ([] if sin_trabajo else sorted(self.plantas_por_trabajar(), key=lambda c: (self.lejos(pos, c), c))[:1]):      # la planta por trabajar más cercana
                J_ = [c for c in self.junto_a(q) if c != pos]
                if pos in self.junto_a(q): out.append({"accion": "trabajar", "que": "trabajar_planta", "planta": list(q), "planta_obj": list(q)})
                elif J_:
                    d_ = min(J_, key=lambda c: (self.lejos(pos, c), c)); out.append({"accion": "ir", "que": "trabajar_planta", "destino": d_, "planta_obj": list(q)})
            if self.casa_v51:                                               # (prompt 103) a un sitio libre de dentro, no la puerta (como el tonto, jugadores.py:79)
                dentro = [c for c in sorted(self.casa_celdas) if self.M.pasa(c, c) and c != self.mi_puerta]
                if pos not in dentro:
                    ocup = {tuple(c["pos"]) for c in self.obs["criaturas"]} | ({self.bestia} if self.bestia else set())
                    libres = [c for c in dentro if c not in ocup] or dentro
                    d_ = min(libres, key=lambda c: (self.lejos(pos, c), c)); out.append({"accion": "ir", "que": "ir_casa", "destino": d_})
            elif pos not in self.casa_celdas:                              # ir a casa (la casa es segura de noche)
                dentro = [c for c in sorted(self.casa_celdas) if self.M.pasa(c, c)]
                d_ = min(dentro, key=lambda c: (self.lejos(pos, c), c)); out.append({"accion": "ir", "que": "ir_casa", "destino": d_})
        if self.vecinas_on:                                                 # (prompt 28) ir hacia la vecina que más lo necesita por su vínculo
            cand_v = [(self.vin.get(x, 0.0), x) for x, d in self.otras.items() if d.get("pos") and self.necesidad_vecina(x, d) and d["pos"] != pos]
            if cand_v:
                w, x = max(cand_v); out.append({"accion": "ir", "que": "ir_vecina", "destino": self.otras[x]["pos"], "quien": x})
        if ((self.enfado_on and self.enfado is not None) or self.rg) and self.bestia is not None:      # (prompt 27) ir a por la bestia (pegarse a ella para empujarla); (39) sin enfado
            junto = [c for c in ((self.bestia[0] + dx, self.bestia[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy) if self.M.pasa(c, c)]
            if junto and pos not in junto:
                q = min(junto, key=lambda c: ((self.lejos(pos, c) if self.dist_u else abs(c[0] - pos[0]) + abs(c[1] - pos[1])), c)); out.append({"accion": "ir", "que": "ir_bestia", "destino": q})
        if self.responde and self.comida_oida and len(bolsa) < 6:           # (prompt 24) «aquí hay comida»: ir adonde llamó
            q = max(self.comida_oida, key=lambda c: (self.comida_oida[c][1] / (1.0 + (self.lejos(pos, c) if self.dist_u else abs(c[0] - pos[0]) + abs(c[1] - pos[1]))), c))
            if q != pos: out.append({"accion": "ir", "que": "ir_llamada", "destino": q})
        if self.v7:                                                        # (prompt 19) a un matorral recordado (no a la vista), o al bosque
            vista_ahora = self._mat_vista
            rec = [q for q in self.mat if q not in vista_ahora and q != pos]
            if rec:
                if self.cinco:                                              # (prompt 41) los cinco que más prometen por lo que cuesta llegar
                    tops = sorted(rec, key=lambda c: (-self.p_matorral(c) / (1.0 + self.lejos(pos, c)), c))[:CFG["memoria_matorrales"]["candidatos"]]
                    for q in tops: out.append({"accion": "ir", "que": "ir_matorral", "destino": q})
                    if self.rondas:                                         # (prompt 43) rondas: los dos y los tres que más prometen, en el orden más corto (el más cerca cada vez)
                        for k in (2, 3):
                            if len(tops) < k: continue
                            quedan, p0, orden = list(tops[:k]), pos, []
                            while quedan:
                                q = min(quedan, key=lambda c: (self.lejos(p0, c), c)); orden.append(q); quedan.remove(q); p0 = q
                            out.append({"accion": "ir", "que": "ir_ronda", "destino": orden[0], "ronda": orden})
                else:
                    if self.recuerdo_vacio: q = max(rec, key=lambda c: (self.p_matorral(c) / (1.0 + (self.lejos(pos, c) if self.dist_u else abs(c[0] - pos[0]) + abs(c[1] - pos[1]))), c))    # el que más promete por lo que cuesta llegar
                    else: q = min(rec, key=lambda c: ((self.lejos(pos, c) if self.dist_u else abs(c[0] - pos[0]) + abs(c[1] - pos[1])), c))
                    out.append({"accion": "ir", "que": "ir_matorral", "destino": q})
            bos = [c for c in self.celdas_de.get("bosque", []) if c not in self.vistas]      # (prompt 20) solo bosque no visto: con todo visto, ir «al bosque» era ir a la casilla de al lado e ir y venir
            if bos:
                q = min(bos, key=lambda c: ((self.lejos(pos, c) if self.dist_u else abs(c[0] - pos[0]) + abs(c[1] - pos[1])), c))
                if q != pos: out.append({"accion": "ir", "que": "ir_bosque", "destino": q})
        if self._front.get(pos):                                           # (prompt 12) el viaje del cinco (8.3): a la casilla no vista más cercana
            D = self._dist_a(pos); q = min((c for c in self.pisables if c not in self.vistas and c in D), key=lambda c: (D[c], c), default=None)
            if q is not None: out.append({"accion": "ir", "que": "ir_frontera", "destino": q})
        return out

    @staticmethod
    def clase(acc):
        return {"mover": "mover", "ir": "mover", "quedarse": "quedarse", "dormir": "dormir", "trabajar": "trabajar"}.get(acc["accion"], "otra")

    def _sigue_destino(self, obs, validas):
        """(prompt 22, Manel) el compromiso: sigue hacia el destino elegido salvo que pase algo importante. Lo suelta si llega, si ve la bestia, si el hambre
        o el cansancio cruzan su umbral desde que se comprometió (o se agota), si ve comida más cerca que el destino, o si no avanza en 3 turnos.
        Devuelve la acción (un paso) o None (lo suelta y vuelve a decidir)."""
        yo = obs["yo"]; pos = tuple(yo["pos"]); D = self.dest; dst = tuple(D["acc"]["destino"]); U = CFG["compromiso"]
        va_a_la_bestia = D["acc"].get("que") == "ir_bestia"                # (prompt 27) ver la bestia no suelta el ir a por ella (sí, que deje de estar enfadada)
        if self.compromiso_emocion_v18:                                     # (prompt 56) solo: llega, no avanza en 3 turnos, o cambia lo que siente
            ex = self._expresion(); cambia = D.get("ex") is not None and ex != D["ex"]; D["ex"] = ex
            n = CFG["compromiso"]["sin_avanzar_turnos"]; D["hist"] = (D["hist"] + [pos])[-(n + 1):]
            suelta = pos == dst or cambia or (len(D["hist"]) >= n + 1 and len(set(D["hist"])) == 1)
            if not suelta:
                cam = self.camina(pos, D["acc"]); movs = {v["dir"] for v in validas if v["accion"] == "mover"}
                if cam:
                    dd_ = (cam[0][0] - pos[0], cam[0][1] - pos[1]); dr = next((k for k, v in DIRS.items() if v == dd_), None)
                    if dr in movs: return {"accion": "mover", "dir": dr, "_ir": D["acc"]["que"], "_compromiso": True}
            self.dest = None
            return None
        suelta = pos == dst or (obs.get("bestia") is not None and not va_a_la_bestia) or (va_a_la_bestia and self.enfado is None) or yo["agotada"] \
            or (yo["hambre"] > U["hambre_mayor_que"] >= D["h0"]) or (yo["cansancio"] > U["cansancio_mayor_que"] >= D["c0"]) \
            or (self.cansancio_suelta and yo["cansancio"] > U["cansancio_mayor_que"]) \
            or (self.duelo_para and self.es_cosa(D["acc"]) and any(m["t"] >= D.get("t0", -1) for m in self.muertas.values()))
        if not suelta:
            dd = self.pasos(pos, dst) if self.dist_u else abs(dst[0] - pos[0]) + abs(dst[1] - pos[1])
            for c in obs["casillas"]:
                q = tuple(c["pos"])
                if q != dst and ("comida" in (c.get("objetos") or []) or (c.get("matorral") or {}).get("frutos") or (c.get("planta") or {}).get("frutos")) \
                        and ((self.pasos(pos, q) if self.dist_u else abs(q[0] - pos[0]) + abs(q[1] - pos[1]))) < dd: suelta = True; break
        n = U["sin_avanzar_turnos"]; D["hist"] = (D["hist"] + [pos])[-(n + 1):]
        if not suelta and len(D["hist"]) >= n + 1 and len(set(D["hist"])) == 1: suelta = True
        if not suelta:
            cam = self.camina(pos, D["acc"]); movs = {v["dir"] for v in validas if v["accion"] == "mover"}
            if cam:
                dd_ = (cam[0][0] - pos[0], cam[0][1] - pos[1]); dr = next((k for k, v in DIRS.items() if v == dd_), None)
                if dr in movs: return {"accion": "mover", "dir": dr, "_ir": D["acc"]["que"], "_compromiso": True}
        self.dest = None
        return None

    # ── las llamadas: expresión de lo que siente el cuerpo ──
    def sentimientos(self, obs):
        if self.llamadas_opcion_v19: return {}                              # (prompt 57) ya no salen solas: se eligen
        yo = obs["yo"]; L = CFG["llamadas"]
        vista_comida = any("comida" in (c.get("objetos") or []) or (self.responde and ((c.get("matorral") or {}).get("frutos") or (c.get("planta") or {}).get("frutos"))) for c in obs["casillas"])
        sobra = False
        if self.comida_sobra:
            if self.comida_por_dia and self._dia_sitios != obs["dia"]: self._dia_sitios = obs["dia"]; self.sitios_llamados = set()     # (prompt 27) cada día, de nuevo
            sitios = {}
            for c in obs["casillas"]:
                n_ = (c.get("objetos") or []).count("comida") + int((c.get("matorral") or {}).get("frutos") or 0) + int((c.get("planta") or {}).get("frutos") or 0)
                q = tuple(c["pos"])
                if n_: sitios[q] = n_
                elif not self.comida_por_dia: self.sitios_llamados.discard(q)  # visto vacío: si vuelve a tener, se puede volver a anunciar (antes del prompt 27)
            nuevos = {q: n_ for q, n_ in sitios.items() if q not in self.sitios_llamados}
            cree = max(1e-6, self.cree_comida(yo["hambre"])); se_come = int(yo["hambre"] // cree)
            sobra = sum(nuevos.values()) > se_come; self._sitios_ahora = set(nuevos)
            if self.comida_sin_hermana and any(c["id"] == self.hermana for c in obs["criaturas"]): sobra = False      # (prompt 28) si ve a la hermana, no hace falta llamarla
        if self.duelo_v19: self._duelo_vivo = self.duelo_propio(obs["turno"])[1]
        return {**({"estoy_de_duelo": self._duelo_vivo and not self.voz_v16} if self.duelo_v19 else {}), "peligro": obs.get("bestia") is not None, "estoy_herida": yo["vida"] < L["herida_vida_menor_que"] and not self.voz_v16,
                "no_tengo_energia": bool(yo["agotada"]) and not self.voz_v16, "necesito_ayuda": yo["hambre"] > L["hambre_mayor_que"] or (self.enfado_on and obs["turno"] - self.robada_t <= T["voz_ventana"]),
                "aqui_hay_comida": sobra if self.comida_sobra else (vista_comida and ((yo["hambre"] < self.cree_comida(yo["hambre"])) if self.comida_sin_hambre else len(obs["bolsa"]) >= 6))}

    # ── un turno ──
    @staticmethod
    def clave_accion(acc):
        """(prompt 61) lo que está haciendo: la acción y su objeto, sin el paso de este turno (la dirección)"""
        return (acc.get("accion"), acc.get("que"), acc.get("tipo"), acc.get("de"), acc.get("en"), acc.get("a"), tuple(acc["destino"]) if acc.get("destino") is not None else None)

    def actua(self, obs, info):
        self.observa(obs)
        if self.devolver_v57: self._recibidos(obs)                           # (prompt 109) quién me ha dado qué (antes de imaginar)
        for k, v in self.sentimientos(obs).items():
            if v and self.armada[k]:
                self.cola.append(k); self.armada[k] = False; self._apagada[k] = 0
                if k == "aqui_hay_comida" and self.comida_sobra: self.sitios_llamados |= self._sitios_ahora     # (prompt 26) una vez por sitio
            elif v: self._apagada[k] = 0
            else:                                                          # (prompt 22) se rearma tras voz_ventana turnos seguidos sin sentirlo (antes: al primer turno)
                self._apagada[k] = self._apagada.get(k, 0) + 1
                if not self.histeresis_llamadas or self._apagada[k] >= T["voz_ventana"]: self.armada[k] = True
        validas = info.get("acciones_validas") or [{"accion": "quedarse"}]
        sigue = None
        if not self.cola and self.compromiso and self.dest is not None and not self.compromiso_opcion_v15: sigue = self._sigue_destino(obs, validas)
        if self.compromiso_opcion_v15 and self.dest is not None and tuple(obs["yo"]["pos"]) == tuple(self.dest["acc"]["destino"]): self.dest = None      # (prompt 53) llegó
        if self.cola:
            acc = {"accion": "llamar", "llamada": self.cola.pop(0)}; elegido = "llamar"; preds = {}
        elif sigue is not None:                                             # (prompt 22) mantiene el destino elegido: no vuelve a decidir
            acc = sigue; preds = {}; elegido = json.dumps({k: (list(v) if isinstance(v, tuple) else v) for k, v in self.dest["acc"].items()}, sort_keys=True, ensure_ascii=False)
        else:
            no = set(CFG["acciones_que_no_hace"]) | ({"trabajar"} if self.anticipa else set())
            if self.rg: no = {"hablar", "llamar"} | ({"trabajar"} if self.anticipa else set())     # (prompt 39) el poder entero: empujar y golpear, a la bestia y entre ellas (llamar sale sola)
            cands = [v for v in validas if v["accion"] not in no and not (self.rg and v["accion"] == "dar" and not self.tope_dar(v.get("tipo")))]
            if self.casa_v51 and tuple(obs["yo"]["pos"]) in self.puertas and not obs["yo"]["agotada"]:      # (prompt 103) no se duerme en una puerta (taparía la entrada); agotada, sí (no puede moverse)
                cands = [v for v in cands if v["accion"] != "dormir"]
            if self.sabores_v40 and obs.get("bolsa_origen"):                 # (prompt 85) comer o dar: cuál (una por cada origen que lleva)
                orgs = sorted({o for tp, o in zip(obs["bolsa"], obs["bolsa_origen"]) if tp == "comida" and o})
                if len(orgs) > 1:
                    cands = [dict(v, origen=o) for v in cands for o in (orgs if (v["accion"] in ("comer", "dar") and v.get("tipo") == "comida") else [None])]
                    cands = [{k: x for k, x in v.items() if not (k == "origen" and x is None)} for v in cands]
            if self.enfado_on and self.enfado is not None: cands += [v for v in validas if v["accion"] == "empujar" and es_bestia(v.get("a"))]      # (prompt 27) solo a la bestia, y enfadada
            trabajar_ok = any(v["accion"] == "trabajar" for v in validas)
            movs = {v["dir"] for v in validas if v["accion"] == "mover"}
            for c in self.candidatos_ir():
                if c["accion"] == "trabajar":
                    if trabajar_ok: cands.append(c)
                    continue
                cam = self.camina(tuple(obs["yo"]["pos"]), c)
                if cam:
                    p0 = tuple(obs["yo"]["pos"]); dd = (cam[0][0] - p0[0], cam[0][1] - p0[1]); dr = next((k for k, v in DIRS.items() if v == dd), None)
                    if dr in movs: c["dir"] = dr; cands.append(c)
            if self.compromiso_opcion_v15 and self.dest is not None:         # (prompt 53) seguir hacia el destino: una opción más, con su foto (sin premio)
                c = dict(self.dest["acc"]); cam = self.camina(tuple(obs["yo"]["pos"]), c)
                if cam:
                    p0 = tuple(obs["yo"]["pos"]); dd = (cam[0][0] - p0[0], cam[0][1] - p0[1]); dr = next((k for k, v in DIRS.items() if v == dd), None)
                    if dr in movs:
                        c["dir"] = dr; cands.append(c); self._n_seguir = json.dumps({k: (list(v) if isinstance(v, tuple) else v) for k, v in c.items()}, sort_keys=True, ensure_ascii=False)
            nombres = []; preds = {}
            for c in cands:
                n = json.dumps({k: (list(v) if isinstance(v, tuple) else v) for k, v in c.items()}, sort_keys=True, ensure_ascii=False)
                if n in preds: continue
                if self.comer_luego and c["accion"] == "comer":          # (prompt 15) comer y después lo mejor que haría: el mínimo de las d de comer + cada otro candidato
                    mejor = None
                    for x in cands:
                        if x["accion"] == "comer": continue
                        Fx = self.filas(self.foto(x, antes=c)); _, dx = self._compone(Fx)
                        if mejor is None or dx < mejor[0]: mejor = (dx, Fx, x.get("que") or x["accion"], x)
                    preds[n] = {"d": round(mejor[0], 9), "F": mejor[1], "acc": c, "luego": mejor[2], "luego_acc": mejor[3]}; nombres.append(n); continue
                F = self.filas(self.foto(c)); st, d = self._compone(F); preds[n] = {"d": round(d, 9), "F": F, "acc": c}; nombres.append(n)
                if self.comer_al_final and c["accion"] != "comer" and ("comida" in obs["bolsa"] or c.get("recoger") == "comida" or (c["accion"] == "coger" and c.get("tipo") == "comida")):
                    F2 = self.filas(self.foto(c, al_final=True)); _, d2 = self._compone(F2)
                    if d2 < d: preds[n] = {"d": round(d2, 9), "F": F2, "acc": c, "come_al_final": True}
            if self.duelo_para:                                             # (prompt 32) primero pararse: lo que gana ir a por cosas frente a quedarse, por la atención
                at = self.atencion(); nq = next((n for n in nombres if preds[n]["acc"]["accion"] == "quedarse"), None)
                if at < 1.0 and nq is not None:
                    dq = preds[nq]["d"]
                    for n in nombres:
                        if self.es_cosa(preds[n]["acc"]) and preds[n]["d"] < dq: preds[n]["d"] = round(dq + at * (preds[n]["d"] - dq), 9)
            terminal = {n: preds[n]["d"] for n in nombres}
            elegido = PL.select_tiebreak(nombres, preds, terminal, None)
            if self.compromiso_opcion_v15 and self.compromiso_margen is not None and self.dest is not None and self._n_seguir in preds and elegido != self._n_seguir \
                    and preds[elegido]["d"] > preds[self._n_seguir]["d"] - float(self.compromiso_margen): elegido = self._n_seguir     # (prompt 54) la inercia
            self._n_seguir = None
            if self.empates_sigue_v23 and self._ult_clave is not None:     # (prompt 61) en un empate exacto con lo elegido, lo que estaba haciendo (la misma acción; si no, la misma clase)
                mg_ = 1e-9 if self.empate_margen_v24 is None else self.empate_margen_v24      # (prompt 62) con margen, también los casi empates
                tie = [n for n in nombres if abs(preds[n]["d"] - preds[elegido]["d"]) <= mg_]
                if len(tie) > 1:
                    mismo = [n for n in tie if self.clave_accion(preds[n]["acc"]) == self._ult_clave] or [n for n in tie if preds[n]["acc"]["accion"] == self._ult_clave[0]]
                    if mismo and elegido not in mismo: elegido = mismo[0]
            if self.empate_quedarse_v47:                                    # (prompt 93) en un empate exacto, gana quedarse (los casi empates no se tocan)
                tq = [n for n in nombres if preds[n]["acc"]["accion"] == "quedarse" and abs(preds[n]["d"] - preds[elegido]["d"]) <= 1e-9]
                if tq and preds[elegido]["acc"]["accion"] != "quedarse": elegido = tq[0]; self.empates_v42["quedarse"] = self.empates_v42.get("quedarse", 0) + 1
            if self.empate_suertes_v42 and not (self.empate_quedarse_v47 and preds[elegido]["acc"]["accion"] == "quedarse"):      # (prompt 87) el empate exacto que queda, a suertes; (93) salvo si ganó quedarse
                self.empates_v42["decisiones"] += 1
                tie = [n for n in nombres if abs(preds[n]["d"] - preds[elegido]["d"]) <= 1e-9]
                if self.empates_sigue_v23 and self._ult_clave is not None and len(tie) > 1:
                    mismo = [n for n in tie if self.clave_accion(preds[n]["acc"]) == self._ult_clave] or [n for n in tie if preds[n]["acc"]["accion"] == self._ult_clave[0]]
                    if mismo and elegido in mismo: tie = mismo
                if len(tie) > 1 and elegido in tie:
                    elegido = self._rng_empate.choice(sorted(tie)); self.empates_v42["empates"] += 1
                    k_ = "|".join(sorted({(preds[n]["acc"].get("que") or preds[n]["acc"]["accion"]) + ("·origen" if preds[n]["acc"].get("origen") else "") for n in tie}))
                    self.empates_v42["por"][k_] = self.empates_v42["por"].get(k_, 0) + 1
            acc = preds[elegido]["acc"]
            if acc["accion"] == "comer" and obs["yo"]["hambre"] < 35 and len(self.diag_come_sin) < 300:      # (prompt 36, diagnóstico; solo medir) por qué come sin hambre
                FI3 = ("F-HAMBRE", "P-COMER", "R-CONSEGUIR", "R-CARENCIA", "R-LLAMADA", "S-JUNTAS", "S-DAR", "F-CANSANCIO")
                alt = min((n for n in nombres if n != elegido), key=lambda n: preds[n]["d"], default=None)
                f3 = lambda n_: {k: round(float(preds[n_]["F"].get(k, 0.0)), 3) for k in FI3}
                self.diag_come_sin.append({"t": obs["turno"], "hambre": round(obs["yo"]["hambre"], 1), "lleva": obs["bolsa"].count("comida"), "d": preds[elegido]["d"], "filas": f3(elegido),
                                           "alt": (preds[alt]["acc"].get("que") or preds[alt]["acc"]["accion"]) if alt else None, "d_alt": preds[alt]["d"] if alt else None, "filas_alt": f3(alt) if alt else None})
            if obs["yo"]["hambre"] > 80 and "comida" in obs["bolsa"] and acc["accion"] != "comer" and len(self.diag_no_come) < 300:     # (prompt 35, diagnóstico; solo medir)
                com = min((n for n in nombres if preds[n]["acc"]["accion"] == "comer"), key=lambda n: preds[n]["d"], default=None)
                FI2 = ("F-HAMBRE", "P-COMER", "P-CALOR", "F-FRIO", "R-CARENCIA", "F-CANSANCIO", "F-ANTICIPACION", "S-JUNTAS")
                fl = lambda n_: {k: round(float(preds[n_]["F"].get(k, 0.0)), 3) for k in FI2}
                self.diag_no_come.append({"t": obs["turno"], "fase": obs["fase"], "hambre": round(obs["yo"]["hambre"], 1), "en_casa": tuple(obs["yo"]["pos"]) in self.todas_casas,
                                          "elige": acc.get("que") or acc["accion"], "d": preds[elegido]["d"], "filas": fl(elegido),
                                          "d_comer": preds[com]["d"] if com else None, "filas_comer": fl(com) if com else None})
            if acc["accion"] == "dar" and len(self.diag_dar) < 400:          # (prompt 35, diagnóstico; solo medir) por qué da: sus filas frente a la mejor otra cosa y frente a comer
                FI = ("F-HAMBRE", "R-HERMANO-FALTA", "S-DAR", "P-COMER", "R-CARENCIA", "R-CONSEGUIR", "S-DANO-PAREJA", "S-JUNTAS", "R-LLAMADA")
                fil = lambda n_: {k: round(float(preds[n_]["F"].get(k, 0.0)), 3) for k in FI}
                otras_ = [n for n in nombres if n != elegido and preds[n]["acc"]["accion"] != "dar"]
                alt = min(otras_, key=lambda n: preds[n]["d"], default=None); com = min((n for n in otras_ if preds[n]["acc"]["accion"] == "comer"), key=lambda n: preds[n]["d"], default=None)
                x_ = acc.get("a"); dd_ = self.otras.get(x_) or {}
                self.diag_dar.append({"t": obs["turno"], "a": x_, "hermana": x_ == self.hermana, "hambre": round(obs["yo"]["hambre"], 1), "lleva": obs["bolsa"].count("comida"),
                                      "la_cree_flaca": bool(self.pareja_flaca if x_ == self.hermana else dd_.get("flaca")), "la_ve": any(c["id"] == x_ for c in obs["criaturas"]),
                                      "d": preds[elegido]["d"], "filas": fil(elegido), "alt": (preds[alt]["acc"].get("que") or preds[alt]["acc"]["accion"]) if alt else None,
                                      "d_alt": preds[alt]["d"] if alt else None, "filas_alt": fil(alt) if alt else None,
                                      "d_comer": preds[com]["d"] if com else None, "filas_comer": fil(com) if com else None,
                                      "sentido": {k: round(v_ * 0.5 ** ((obs["turno"] - t_) / T["mirada"]), 3) for k, (v_, t_) in self.sentido.items()}})
            if acc["accion"] == "ir":
                if self.compromiso:                                         # (prompt 22) se compromete con ese destino hasta llegar o hasta que pase algo importante
                    yo_ = obs["yo"]; self.dest = {"acc": dict(acc), "h0": yo_["hambre"], "c0": yo_["cansancio"], "hist": [tuple(yo_["pos"])], "t0": obs["turno"],
                                                             "ex": self._expresion() if self.compromiso_emocion_v18 else None}
                acc = {"accion": "mover", "dir": acc["dir"], "_ir": acc["que"]}
            elif acc.get("que") == "trabajar_planta": acc = {"accion": "trabajar", "planta": acc["planta"], "_ir": "trabajar_planta"}
        if self.vecinas_on and "comida" in obs["bolsa"] and self.pareja_vista and self.pareja_flaca:      # (prompt 28) ¿elige entre la hermana y una vecina igual de mal?
            vf = [c["id"] for c in obs["criaturas"] if c["id"] != self.hermana and c.get("flaca")]
            if vf:
                el = acc.get("_ir") or acc["accion"]; quien = acc.get("a") if acc["accion"] == "dar" else None
                self.dilemas.append({"t": obs["turno"], "elige": el, "a": quien, "vecinas_flacas": vf})
        if self.responde:                                                  # (prompt 24) cuántos turnos responde a una llamada
            ir_ = acc.get("_ir")
            if ir_ == "ir_llamada": self.respuestas["comida"] = self.respuestas.get("comida", 0) + 1
            if ir_ == "ir_pareja" and self.ayuda_oida: self.respuestas["ayuda"] = self.respuestas.get("ayuda", 0) + 1
            if ir_ == "ir_casa" and self.peligro_oido and obs["fase"] in ("anochecer", "noche"): self.respuestas["peligro_a_casa"] = self.respuestas.get("peligro_a_casa", 0) + 1
        yo = obs["yo"]; self._ult_clave = self.clave_accion(acc)
        self.prev = {**({"fase": obs["fase"]} if self.prop_ctx_v48 else {}), "pos": tuple(yo["pos"]), "vida": yo["vida"], "hambre": yo["hambre"], "cansancio": yo["cansancio"], "accion": acc["accion"], "tipo": acc.get("tipo"), "de": acc.get("de"),
                     "clase": self.clase_de(acc), "ok": True, "planta": acc.get("planta"), "bolsa": list(obs["bolsa"]), "a": acc.get("a"), "bolsa_origen": list(obs.get("bolsa_origen") or []), "bestia_cerca": self.bestia is not None and ((self.cheb(tuple(yo["pos"]), self.bestia) <= 1) if self.dist_u else (math.dist(tuple(yo["pos"]), self.bestia) <= 1.5))}
        if self.ya_tiene_v67: self.prev["lleva_vista_v67"] = {c["id"]: list(c.get("lleva") or []) for c in obs["criaturas"]}      # (prompt 131) lo que llevaban antes de dar
        self.ultima = {"elegido": elegido, "n_cand": len(preds), "d": (preds.get(elegido) or {}).get("d"), "luego": (preds.get(elegido) or {}).get("luego"), "luego_acc": (preds.get(elegido) or {}).get("luego_acc"),
                       "filas": {k: round(v, 4) for k, v in ((preds.get(elegido) or {}).get("F") or {}).items() if v}}
        if self.llamadas_opcion_v19 and not self.voz_off_v62:               # (prompt 57) la voz aparte de los pies: ¿llamar, cuál y con qué fuerza? (prompt 123: no, con la voz apagada)
            ll_ = self._elige_llamada(obs, acc)
            if ll_: acc = dict(acc, llama=ll_)
        if self.voz_v16:                                                    # (prompt 54) la expresión: suena sola si cambia la que manda o su intensidad
            ex = self._expresion()
            if ex != self._suena: acc = dict(acc, suena={"fuerza": ex[0], "intensidad": ex[1]}); self._suena = ex
        if self.cara_v64: acc = dict(acc, cara=list(self._F_propia_ahora()[1]))          # (prompt 128) la cara: sale sola, cada turno
        if self.voz_v64:                                                    # (prompt 128) la voz: sale sola. Dormida no emite: lo impide el mundo (la observación no le dice si duerme)
            v_ = self._para(obs) if self.para_v64 else None
            if v_ is None and (self.voz_base_v64 or self.voz_piezas_v68): v_ = self._voz_propia(obs)
            if v_:
                acc = dict(acc, voz=v_); k_ = f"emite|{v_['clase']}|{v_['intensidad']}"; self.cuenta_v64[k_] = self.cuenta_v64.get(k_, 0) + 1
        return acc

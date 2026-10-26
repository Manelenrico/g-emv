"""[P5-8A] La curiosidad como FORMA, en seco. Primera imagen, alcance cerrado.

El cuerpo se propone a si mismo una forma —ir a la frontera de lo no visto— y
**la puerta ancha de P5-6C la juzga como cualquier forma del consejero**. Nada
de curiosidad concreta, caducidad ni signo de peligro: eso es la segunda imagen.

POR QUE. La curiosidad de frontera como tiron de UN PASO (P5-7C) no explora:
casillas nuevas por cien tics identicas en A y en Q (14,5 las dos). El cuerpo
decide paso a paso y la frontera esta lejos; un tiron que gana una decision de
cada veinte no hace trayecto.

REGLAS DURAS. `motor/model.py`, `decisor_zs.py` y `appraisal_zs_v42_exp.py`
INTOCADOS. Todo lo nuevo vive aqui; se reutiliza `forma.py` (la puerta),
`proyeccion.py` (el camino) y el BFS de `curiosidad.py`. **La puerta no se
toca**: para meter el renglon en la proyeccion se ENVUELVE `F._d2` desde fuera
y se restaura en un `finally`, el mismo patron con el que la politica inyecta
`D.candidatos`.
"""
from __future__ import annotations
import math, os, sys, time
from collections import deque

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for _p in (os.path.join(RAIZ, "cantera", "paper4"),
           os.path.join(RAIZ, "paintball"), RAIZ, AQUI):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.append(_p)

from alma import appraisal_zs_v42_exp as A                  # noqa: E402
from motor.model import State, opponent_distance, DEFAULT_CONFIG  # noqa: E402
import forma as F                                           # noqa: E402
import proyeccion as P                                      # noqa: E402
import curiosidad as C                                      # noqa: E402

# ── EL DISPARO ────────────────────────────────────────────────────────────
CONSIGNAS = (0.5, 0.7)          # [Manel] se informa con las dos
UMBRAL_SEGURO = C.SEGURO        # 0,2 — la misma amenaza graduada de P5-7A
TOPE_CAMINO = 20                # [Manel] si la frontera esta mas lejos, a 20
TOPE_RODEO = 1.5          # [P5-8M · Manel] el rodeo, como mucho 1,5x lo que quedaba
# [P5-8M] EL COLCHON DEL RODEO, elegido por la regla de Manel y MEDIDO en seco
# sobre los 103 vetos duros reales de P5-8I y P5-8K:
#   colchon 1 (d <= alcance + 1, que es el `< alcance + 2` de P5-8A):  1/103 = 1,0 %
#   colchon 0 (d <= alcance):                                         61/103 = 59,2 %
# La regla era «colchon 1 si llega al 40 %, si no colchon 0». Salio 1,0 %.
# La sombra del NACIMIENTO (`en_sombra`, alcance + 2) NO se toca.
COLCHON_RODEO = 0
SOMBRA_EXTRA = 2                # [Manel] alcance del armado + 2 casillas
K_CUR = 0.2                     # [Manel] el renglon en la proyeccion

_VECINOS = ((1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1))


# ══════════════════════════════════════════════════════════════════════════
#  2 · LA FRONTERA CON SOMBRA
# ══════════════════════════════════════════════════════════════════════════
def armados(r, mundo, herm):
    """[(pos, alcance)] de los armados a la vista que no son el hermano."""
    out = []
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") == herm or not a.get("pos"):
            continue
        rg = C._alcance(mundo, a.get("hand"))
        if rg > 0:
            out.append((tuple(a["pos"]), rg))
    return out


def _alcance_de(mundo, a) -> float:
    """El alcance del arma de UN agente visible. Atajo de `armados`."""
    return C._alcance(mundo, a.get("hand"))


def en_sombra(q, pos, arms) -> bool:
    """La casilla `q` esta en sombra de algun armado si:
       · su distancia al armado es MENOR que su distancia al cuerpo, o
       · esta a menos del alcance del armado mas dos casillas.
    Las dos son la regla de Manel, literal."""
    dq_cuerpo = max(abs(q[0] - pos[0]), abs(q[1] - pos[1]))
    for a, rg in arms:
        dq_arm = max(abs(q[0] - a[0]), abs(q[1] - a[1]))
        if dq_arm < dq_cuerpo or dq_arm < rg + SOMBRA_EXTRA:
            return True
    return False


def camino_a_frontera(ojo, mundo, pos, arms):
    """BFS desde el CUERPO hasta la casilla no vista mas cercana que NO este
    en sombra. Devuelve (camino, dist, destino) o (None, None, None).

    A diferencia del BFS de `curiosidad.py` —multi-fuente desde lo no visto—,
    aqui hace falta el CAMINO, no solo la distancia: la forma necesita un
    destino y el rastro de casillas que se irian viendo.
    """
    pos = (int(pos[0]), int(pos[1]))
    prev = {pos: None}
    dq = deque([pos])
    destino = None
    while dq:
        x, y = dq.popleft()
        if (x, y) != pos and (x, y) not in ojo.primera_vez \
                and not en_sombra((x, y), pos, arms):
            destino = (x, y)
            break
        for dx, dy in _VECINOS:
            q = (x + dx, y + dy)
            if q in prev or mundo.solido(q[0], q[1]):
                continue
            # LA SOMBRA CORTA EL CAMINO, no solo el destino. El humo encontro
            # esto: comprobando la sombra solo en la casilla de llegada, el
            # BFS devolvia caminos que pasaban por delante del armado. El
            # contador «cero formas que cruzan sombra» es POR CONSTRUCCION, y
            # la construccion es esta.
            if en_sombra(q, pos, arms):
                continue
            prev[q] = (x, y)
            dq.append(q)
    if destino is None:
        return None, None, None
    cam = []
    c = destino
    while c is not None:
        cam.append(c)
        c = prev[c]
    cam.reverse()                       # [pos, ..., destino]
    d = len(cam) - 1
    if d > TOPE_CAMINO:                 # el destino es la casilla a 20
        cam = cam[:TOPE_CAMINO + 1]
        destino = cam[-1]
        d = TOPE_CAMINO
    return cam, d, destino


def camino_a_destino(mundo, pos, destino, arms):
    """[P5-8M] BFS desde el CUERPO hasta UN DESTINO DADO, cortando la sombra.

    Es `camino_a_frontera` con el destino fijado en vez de buscado, pero con
    SU PROPIA tapa: solo el alcance del arma mas `COLCHON_RODEO`. La sombra de
    P5-8A (alcance + 2, o mas cerca del armado que del cuerpo) sigue rigiendo
    el NACIMIENTO del camino y no se toca. Devuelve (camino, largo) o
    (None, None).

    El DESTINO se exime de la prueba de sombra: es la casilla que la forma
    prometio ver, y exigirle que este fuera de sombra seria cambiar el destino,
    no rodear. Todo el resto del camino SI la cumple.
    """
    pos = (int(pos[0]), int(pos[1]))
    destino = (int(destino[0]), int(destino[1]))
    if pos == destino:
        return [pos], 0

    def _tapa(q):
        """La sombra DEL RODEO: solo el alcance del arma mas el colchon.
        NO lleva la clausula «mas cerca del armado que del cuerpo» de
        `en_sombra`: medida en seco, esa sola deja el rodeo en 3 de 103."""
        for a, rg in arms:
            if max(abs(q[0] - a[0]), abs(q[1] - a[1])) <= rg + COLCHON_RODEO:
                return True
        return False

    prev = {pos: None}
    dq = deque([pos])
    hallado = False
    while dq:
        x, y = dq.popleft()
        for dx, dy in _VECINOS:
            q = (x + dx, y + dy)
            if q in prev or mundo.solido(q[0], q[1]):
                continue
            if q != destino and _tapa(q):
                continue
            prev[q] = (x, y)
            if q == destino:
                hallado = True
                dq.clear()
                break
            dq.append(q)
        if hallado:
            break
    if not hallado:
        return None, None
    cam = []
    c = destino
    while c is not None:
        cam.append(c)
        c = prev[c]
    cam.reverse()
    return cam, len(cam) - 1


def cubridores(resto, r, mundo, herm):
    """[P5-8M] Los armados (el registro entero) cuyo alcance toca el camino.

    Es `abandona_por_peligro` devolviendo QUIENES en vez de un booleano, para
    poder preguntar si se acercan. La condicion es la MISMA, letra por letra.
    """
    out = []
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") == herm or not a.get("pos"):
            continue
        rg = C._alcance(mundo, a.get("hand"))
        if rg <= 0:
            continue
        q = tuple(a["pos"])
        for c in resto:
            if max(abs(c[0] - q[0]), abs(c[1] - q[1])) <= rg:
                out.append(a)
                break
    return out


# ══════════════════════════════════════════════════════════════════════════
#  1 y 3 · EL DISPARO Y LA FORMA
# ══════════════════════════════════════════════════════════════════════════
def genera(r, mundo, mem, ojo, herm, tick, consigna, hay_activa=False):
    """(tramos, info) o (None, info) con el motivo. No decide nada: propone."""
    t0 = time.perf_counter()
    info = {"motivo": None, "amenaza": None, "ign": None, "dist": None,
            "ms": 0.0}
    if hay_activa:
        info["motivo"] = "forma activa"
        return None, info
    pos = tuple(r.get("pos") or ())
    if not pos:
        info["motivo"] = "sin posicion"
        return None, info
    am, _des = C.amenaza(r, mundo, herm, info.get("dano100", 0.0) or 0.0, tick)
    info["amenaza"] = am
    if am >= UMBRAL_SEGURO:
        info["motivo"] = "entorno no seguro"
        return None, info
    ign = ojo.ignorancia_global()
    info["ign"] = ign
    if ign <= consigna:
        info["motivo"] = "ignorancia por debajo de la consigna"
        return None, info
    arms = armados(r, mundo, herm)
    cam, d, destino = camino_a_frontera(ojo, mundo, pos, arms)
    info["ms"] = (time.perf_counter() - t0) * 1000.0
    if destino is None:
        info["motivo"] = "sin frontera segura"
        return None, info
    info["dist"] = d
    info["camino"] = cam
    info["armados"] = arms
    # EL IDIOMA DE LA FORMA, el de `traductor_forma.py`, para que la puerta la
    # trate como cualquier otra.
    tramos = [{"destino": list(destino), "intencion": "ver", "esperar": 0,
               "vida": "0", "manos": "0", "vinculo": "0",
               "_por": "curiosidad",
               "_porque": f"no visto a {d} casillas"}]
    return tramos, info


# ══════════════════════════════════════════════════════════════════════════
#  4 · LA PUERTA, con el renglon dentro de la proyeccion
# ══════════════════════════════════════════════════════════════════════════
def _vistas_por_tic(ojo, mundo, camino, tics, t0):
    """Lo que se habria visto al llegar a cada punto de control.

    La ignorancia es ESTADO PROPIO y se proyecta honesta: al avanzar por el
    camino, las casillas que el ojo alcanzaria desde cada casilla pisada ya
    estan vistas. Se devuelve {tic: (n_vistas, ignorancia)}.
    """
    vistas = set(ojo.primera_vez)
    n = ojo.n_arena
    out, i = {}, 0
    # el camino se recorre a un paso por tic (cota optimista declarada)
    for tic in tics:
        k = max(0, tic - t0)
        while i < min(k, len(camino) - 1):
            i += 1
            vistas |= ojo.vistas_desde(camino[i])
        out[tic] = (len(vistas), 1.0 - len(vistas) / float(n))
    return out


def con_renglon(ojo, mundo, camino, tics, t0, amenaza, k=K_CUR):
    """Envoltura de `F._d2` que SUMA `R-CURIOSIDAD-FRONTERA` a la foto.

    `forma.py` no se toca: se sustituye su `_d2` mientras dura la evaluacion y
    se restaura en el `finally` de quien llama. El valor del renglon es el
    mismo de `curiosidad.py`: k x ign_global x (1-amenaza) x (1 - g(d)), con
    `d` la distancia POR EL CAMINO de la casilla proyectada a la frontera.
    """
    porv = _vistas_por_tic(ojo, mundo, camino, tics, t0)
    idx = {c: i for i, c in enumerate(camino)}
    fin = len(camino) - 1
    _orig = F._d2

    def _d2(o, mu, me, tic, pisos=None, _o=_orig):
        st_d = _o(o, mu, me, tic, pisos)
        if st_d is None:
            return None
        p = tuple((o.get("you") or {}).get("pos") or ())
        _n, ign = porv.get(tic, (0, None))
        if ign is None or not p:
            return st_d
        # distancia a la frontera POR EL CAMINO desde donde esta la foto.
        # RESPALDO DECLARADO: en la REEVALUACION el cuerpo ya no esta sobre el
        # camino original —se ha movido, y las fotos proyectan desde donde
        # esta—, asi que el indice falla. Sin respaldo, el renglon no entraba
        # en la reevaluacion y TODA forma moria a los 25 tics (sonda 1). El
        # respaldo es la distancia Chebyshev al destino: aproxima por debajo
        # la distancia por el mapa, y se dice.
        i = idx.get(p)
        if i is not None:
            d = fin - i
        else:
            dst = camino[-1]
            d = max(abs(p[0] - dst[0]), abs(p[1] - dst[1]))
        M = k * ign * (1.0 - amenaza) * (1.0 - C.g_llamada(d))
        if M <= 0.0:
            return st_d
        # se rehace la `d` del motor sumando el renglon al reparto, igual que
        # `curiosidad.py`: el renglon es DOLOR en el dominio R.
        try:
            F_ = A.filas(o, mu, me, tic)
        except Exception:
            return st_d
        pF = nF = pR = nR = pS = nS = 0.0
        for nom, (fF, fR, fS) in A.REPARTO.items():
            Mv = float(F_.get(nom) or 0.0)
            if pisos and nom in pisos:
                Mv = max(Mv, pisos[nom])
            if Mv <= 0.0:
                continue
            aF, aR, aS = Mv * fF, Mv * fR, Mv * fS
            if nom in A.APETITIVAS:
                pF += aF; pR += aR; pS += aS
            else:
                nF += aF; nR += aR; nS += aS
        fF, fR, fS = C.REPARTO_CUR
        nF += M * fF; nR += M * fR; nS += M * fS
        return opponent_distance(State(pF=pF, nF=nF, pR=pR, nR=nR, pS=pS,
                                       nS=nS), DEFAULT_CONFIG)
    F._d2 = _d2
    return _orig, porv


def restaura(_orig):
    F._d2 = _orig


# ══════════════════════════════════════════════════════════════════════════
#  5 · EL RASTRO EN SECO
# ══════════════════════════════════════════════════════════════════════════
def cruza_sombra(camino, pos, arms) -> bool:
    """¿Alguna casilla del camino cae en sombra? Tiene que ser CERO por
    construccion —el BFS ya las evita— y se comprueba, no se supone."""
    return any(en_sombra(q, pos, arms) for q in camino[1:])


def destino_a_tiro(destino, arms) -> bool:
    return any(max(abs(destino[0] - a[0]), abs(destino[1] - a[1])) <= rg
               for a, rg in arms)


def abandona_por_peligro(destino, camino_restante, r, mundo, herm) -> bool:
    """Un armado a la vista cuyo alcance cubre el camino que queda."""
    for a, rg in armados(r, mundo, herm):
        for q in camino_restante:
            if max(abs(q[0] - a[0]), abs(q[1] - a[1])) <= rg:
                return True
    return False

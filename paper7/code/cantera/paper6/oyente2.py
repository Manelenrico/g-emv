"""EL OYENTE DE E2 — mete lo contado en la percepcion. [P6-3, 26-sep-2026]

ARCHIVO NUEVO. No toca nada del paper cinco.

QUE HACE
  Recibe el parte E2 del hermano y, ANTES de que `appraisal` valore, mete en
  `obs["visible"]` lo que el hermano dice que ve:

  a) RIVALES CONTADOS -> `visible.agents`, con `"_contado": True` y la edad del
     dato. Entran ENTEROS, como si los viera: asi alimentan las MISMAS filas
     que ya existen, sin inventar ninguna —`S-8-EXPOSICION`, `F-4-ALCANCE`,
     `F-HERMANO-AMENAZA`, `S-7-AGRESOR`, `agresor_de_la_hermana`— y sin tocar
     una linea de `appraisal_zs_v42_exp.py`.

     POR QUE ENTEROS Y NO PESADOS: la posicion de un rival es un hecho del tic
     en que el hermano lo vio, y la latencia del canal esta medida en +2 tics.
     Pesar su amenaza por la edad seria inventar una fila. Lo que SI se hace
     es CADUCARLOS: un rival contado vale mientras el dato es fresco.

  b) RECURSOS CONTADOS -> `visible.items`, con `"_contado": True`, `"_edad"` y
     `"_peso"`. Aqui el peso SI baja con la edad, porque un objeto en el suelo
     se lo lleva cualquiera.

  c) LOS CAMPOS QUE YA VIAJABAN. `hp`, `pos`, `botiquin`, `agresor`,
     `agresor_slot` y `agresor_pos` YA los lee `appraisal` (P6-2 corregido).
     Lo que E2 arregla no es que no se leyeran: es que **todas sus vias exigen
     que el oyente VEA al rival** (`agresor_de_la_hermana` recorre los agentes
     VISIBLES y devuelve None si el asiento no esta; `F-HERMANO-AMENAZA` itera
     sobre los visibles). Al meter al rival contado en `visible.agents`, esas
     vias se abren SOLAS, sin tocarlas.

     `veneno` sigue sin tener fila (P6-2 corregido: es el unico campo que nadie
     lee). NO se inventa ninguna: queda para Manel.

LA CURVA DE OLVIDO DEL RECURSO, y lo que la sostiene
  Medido en `vida_objetos.py` sobre los 20 diarios: la fraccion de pares
  (objeto, casilla) que SIGUEN en el informe del cuerpo `edad` tics despues de
  verlos por primera vez, excluyendo los que recoge el propio observador:

      edad (tics)   0     12     24     48     75    100    150    200    300
      S            1,00  0,399  0,363  0,339  0,311  0,286  0,267  0,257  0,245

  DECLARADO SIN ADORNOS: esa S mezcla "se lo llevo otro" con "deje de verlo",
  porque el diario no permite separarlos (nuestro modelo de linea de vista no
  es el del motor). Es, por tanto, una COTA INFERIOR de la permanencia, y usarla
  como peso peca de prudente, que es el lado correcto del error.

  w(edad) = S interpolada de esa tabla. El recurso contado entra mientras
  w >= UMBRAL_REC = 0,30, que con esta tabla da **edad <= 86 tics** (tres
  partes y medio de E2). El 86 se CALCULA en `edad_max_recurso()`, no se
  cablea: si la tabla se remide, el corte se mueve solo.

  AVISO DE ALCANCE, para que nadie lo lea de mas: en la version 1 el peso
  decide SI ENTRA, no cuanto pesa dentro. Un peso graduado necesitaria una fila
  que lo multiplicara, y eso seria una fila nueva. No la invento.
"""
from __future__ import annotations

import bisect

CADUCIDAD_RIVAL = 50      # tics. Un rival contado vale medio segundo largo:
                          # a 11 tics por casilla, en 50 tics anda 4-5 casillas
                          # y la posicion contada ya no es un hecho.
UMBRAL_REC = 0.30

_EDADES = (0, 12, 24, 48, 75, 100, 150, 200, 300, 600, 1200, 2400)
_S = (1.000, 0.399, 0.363, 0.339, 0.311, 0.286, 0.267, 0.257, 0.245,
      0.203, 0.156, 0.110)


def peso_recurso(edad: int) -> float:
    """w(edad) = la S medida, interpolada. Fuera de tabla, el ultimo valor."""
    if edad <= 0:
        return 1.0
    if edad >= _EDADES[-1]:
        return _S[-1]
    i = bisect.bisect_right(_EDADES, edad) - 1
    e0, e1 = _EDADES[i], _EDADES[i + 1]
    s0, s1 = _S[i], _S[i + 1]
    return s0 + (s1 - s0) * (edad - e0) / float(e1 - e0)


def edad_max_recurso() -> int:
    """El ultimo tic en que w >= UMBRAL_REC. Se calcula, no se cablea."""
    e = 0
    while e < _EDADES[-1] and peso_recurso(e + 1) >= UMBRAL_REC:
        e += 1
    return e


def inyecta(obs: dict, tick: int, mundo, parte, detalle=None) -> dict:
    """Devuelve una obs NUEVA con lo contado dentro. No muta la de entrada.

    `parte` es el dict de `parte2.parsea` del hermano, o None. Si es None,
    devuelve la obs tal cual (byte a byte: el gate de pareado).
    """
    c = {"rivales_contados": 0, "rivales_ya_vistos": 0, "rivales_caducos": 0,
         "recursos_contados": 0, "recursos_ya_vistos": 0,
         "recursos_caducos": 0, "edad": None}
    if detalle is not None:
        detalle.update(c)
    if not parte:
        return obs
    edad = tick - int(parte.get("t", tick))
    c["edad"] = edad
    vis = dict(obs.get("visible") or {})
    agentes = list(vis.get("agents") or [])
    objetos = list(vis.get("items") or [])
    ya_ag = {a.get("slot") for a in agentes}
    ya_it = {(x.get("id"), tuple(x.get("pos") or ())) for x in objetos}

    if 0 <= edad <= CADUCIDAD_RIVAL:
        for r in (parte.get("rivales") or []):
            sl = r.get("slot")
            if sl in (mundo.slot, mundo.teammate_slot):
                continue
            if sl in ya_ag:
                c["rivales_ya_vistos"] += 1
                continue
            agentes.append({
                "slot": sl, "pos": [int(r["pos"][0]), int(r["pos"][1])],
                # [P6-4] `hand` de un agente AJENO es una CADENA, no un dict.
                # Solo `you.hand` es dict. Meterlo como dict reventaba
                # `appraisal_zs_v42_exp.py:1584` (`MEMORIA_APRENDIDA.get(_w)`,
                # TypeError: unhashable type) y mato diez partidas pagadas en
                # P6-4. El humo `g` daba por buena MI forma en vez de la del
                # mundo; ahora la compara con un agente REAL del diario.
                "hand": r.get("arma") or "none",
                "team": None,
                "body": None,
                # el mundo no publica su hp exacto; el hermano tampoco lo sabe.
                # `healthy` es la banda mas CONSERVADORA para nosotros: no
                # inventa un herido al que rematar.
                "hp_band": "healthy",
                "netted": False, "poisoned": False, "channeling": False,
                "_contado": True, "_de": parte.get("slot"),
                "_edad": edad, "_rumbo": r.get("rumbo")})
            c["rivales_contados"] += 1
    else:
        c["rivales_caducos"] = len(parte.get("rivales") or [])

    w = peso_recurso(edad) if edad >= 0 else 0.0
    if edad >= 0 and w >= UMBRAL_REC:
        for it in (parte.get("recursos") or []):
            k = (it.get("id"), (int(it["pos"][0]), int(it["pos"][1])))
            if k in ya_it:
                c["recursos_ya_vistos"] += 1
                continue
            objetos.append({"id": k[0], "n": 1, "pos": [k[1][0], k[1][1]],
                            "_contado": True, "_de": parte.get("slot"),
                            "_edad": edad, "_peso": round(w, 4)})
            c["recursos_contados"] += 1
    else:
        c["recursos_caducos"] = len(parte.get("recursos") or [])

    vis["agents"] = agentes
    vis["items"] = objetos
    nueva = dict(obs)
    nueva["visible"] = vis
    if detalle is not None:
        detalle.update(c)
    return nueva


def slots_contados(obs: dict) -> set:
    """Los asientos que estan en la percepcion SOLO porque los conto el
    hermano. El decisor no debe poder atacarlos: no los vemos."""
    return {a.get("slot") for a in ((obs.get("visible") or {}).get("agents") or [])
            if a.get("_contado")}

"""[P6-6 · B] LOS DOS ARREGLOS, JUNTOS Y DESDE FUERA. ARCHIVO NUEVO.

No toca `model.py`, ni un byte del paper cinco, ni `policy_pareja.py`, ni
`parte2.py`, ni `oyente2.py`. Se aplica con `aplica(AlmaPareja, log)`.

─── 1 · EL OIDO ──────────────────────────────────────────────────────────────
`oido5_P6_5.py`, medido en P6-5: en el brazo A1 de P6-4 llegaron 18.315 partes
del hermano y el cuerpo no entendio NI UNO, porque lee con un parser estricto de
marca (`appraisal_zs_v42_exp.py:578` -> `parte.py:48`, `^E1 `) y `policy_pareja`
emite `E2`. El remiendo pone en el chat un mensaje GEMELO con la cabeza
traducida a E1, y el parte entra por la puerta de siempre (`Memoria.observa`).
Con los ojos apagados (partes E1) no hace nada: 0 gemelos y la misma obs.

─── 2 · EL DON: «LO DADO, DADO ESTA» (regla de Manel) ────────────────────────
EL FALLO (P6-6 · A, medido en 379 vidas del cinco y 40 de P6-4): el candidato
`soltar` se abre con el hermano SANO por la via PROVISION (PROMPT_59,
`decisor_zs.py:508-513`) y la cesion que deberia proteger el regalo se BORRA
precisamente porque el hermano esta sano (PROMPT_24,
`appraisal_zs_v42_exp.py:667-683`). Resultado: suelto en mi casilla, al tic
siguiente `coger` la ve bajo mis pies y la recupero, y vuelvo a soltar. Dos tics
por vuelta. 74.545 tics del cinco y 24.842 de A0 se fueron en eso.

LA REGLA: el que suelta algo para su hermano NO lo recoge durante N tics.

    N = min( d x coste_movimiento(speed) + MARGEN , CESION_CADUCA_S x tick_rate )

  d        distancia Chebyshev de la casilla del regalo a donde el cuerpo CREE
           que esta su hermano al soltarlo (`mem.pareja_pos`): es lo que tiene
           en la mano al decidir, no lo que sabria un dios.
  coste    `mundo.coste_movimiento(speed)`, LEIDO del mundo y del `speed` de la
           propia observacion. En este mundo son 11 tics por casilla. Prohibido
           cablearlo (CLAUDE.md).
  MARGEN   268 tics. NO es un numero elegido: es el **p90 del margen medido**
           (`mide_espera_P6_6.py`) sobre las **69 recogidas que de verdad
           ocurrieron** en P6-4 A0 y en las cuatro series del cinco, donde
           margen = espera_real - d x coste. Cubre el 89,9 % de ellas. La
           mediana era 45 y el p75 106; con 45 se cubriria la mitad, y media
           recogida perdida es media razon para dar.
  tope     `CESION_CADUCA_S x tick_rate` = 30 s x 24 = 720 tics. No lo pongo yo:
           es el plazo que Manel ya fijo para que una cesion no reclamada vuelva
           a ser mia (`appraisal_zs_v42_exp.py:330`). Con d <= 7 y margen 268 el
           tope casi nunca manda; esta para que nunca mande el margen sobre una
           decision ya tomada de la casa.

Y NADA MAS: ni una fila nueva, ni una regla de movimiento, ni tocar la tabla.
Si el hermano MUERE, el regalo deja de ser suyo y se libera en el acto — que es
lo que ya decia el PROMPT_24.

COMO SE ENTERA DE QUE HA SOLTADO. No se inventa contabilidad: `decisor_zs.py:
900-904` YA escribe `mem.cedidos[pos]` en cada `soltar`. Se envuelve `D.decide`
y, justo despues, se copia esa cesion a un cuaderno propio (`mem._dados6`) que
el borrado del PROMPT_24 no alcanza. Luego se envuelve `D.candidatos` para
esconder `coger` mientras el plazo viva. Dos envoltorios, cero codigo nuevo en
la ruta de decision.
"""
from __future__ import annotations

import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import oido5_P6_5 as O5                                   # noqa: E402
from alma import decisor_zs as D                          # noqa: E402
from alma import appraisal_zs_v42_exp as A                 # noqa: E402

# p90 del margen medido sobre 69 recogidas reales (mide_espera_P6_6.py)
MARGEN_TICS = 268
DON_ON = (os.environ.get("GEMV_DON", "1") or "1") not in ("0", "", "no")
OIDO_ON = (os.environ.get("GEMV_OIDO", "1") or "1") not in ("0", "", "no")


def entorno():
    return {"crudo": {"GEMV_DON": os.environ.get("GEMV_DON"),
                      "GEMV_OIDO": os.environ.get("GEMV_OIDO")},
            "efectivo": {"DON": DON_ON, "OIDO": OIDO_ON,
                         "MARGEN_TICS": MARGEN_TICS,
                         "CESION_CADUCA_S": A.CESION_CADUCA_S}}


def _speed(obs):
    """El mismo `speed` que usa el decisor, leido igual (`decisor_zs.py:740`)."""
    st = ((obs.get("you") or {}).get("stats") or {})
    try:
        return int(st.get("speed") or 5)
    except (TypeError, ValueError):
        return 5


def plazo(obs, mundo, mem, cel):
    """N tics que el regalo deja de ser mio. Todo leido, nada cableado."""
    coste = int(mundo.coste_movimiento(_speed(obs)))
    ph = getattr(mem, "pareja_pos", None)
    if ph:
        d = max(abs(int(ph[0]) - int(cel[0])), abs(int(ph[1]) - int(cel[1])))
    else:
        d = 1                     # sin saber donde esta, el minimo: un paso
    tope = int(A.CESION_CADUCA_S * int(getattr(mundo, "tick_rate", 24) or 24))
    return min(d * coste + MARGEN_TICS, tope), d, coste


def _cuaderno(mem):
    c = getattr(mem, "_dados6", None)
    if c is None:
        c = {}
        try:
            mem._dados6 = c
        except Exception:          # por si algun dia Memoria lleva __slots__
            return None
    return c


def vivo(mem, tick, pos, item_id):
    """¿Sigue siendo del hermano lo que hay en `pos`? (regla del don)"""
    c = getattr(mem, "_dados6", None)
    if not c:
        return False
    e = c.get(tuple(pos))
    if e is None or e["item"] != item_id:
        return False
    if getattr(mem, "pareja_muerta", False):
        return False               # muerto el hermano, el regalo vuelve al mundo
    return (tick - e["tick"]) < e["N"]


def aplica(clase, registra=None):
    """Engancha los dos arreglos. Devuelve un dict con lo que se ha enganchado."""
    hecho = {"oido": False, "don": False, "margen": MARGEN_TICS}

    if OIDO_ON:
        O5.remienda(clase, registra)
        hecho["oido"] = True

    if DON_ON:
        _orig_decide = D.decide

        def _decide(obs, mundo, mem, tick, bloqueos=None):
            ac, radio = _orig_decide(obs, mundo, mem, tick, bloqueos)
            # `decide` ya ha escrito `mem.cedidos[pos]` si ha soltado (`:900-904`)
            ced = getattr(mem, "cedidos", None) or {}
            if ced:
                cuad = _cuaderno(mem)
                if cuad is not None:
                    for pos, e in ced.items():
                        if e.get("tick") != tick:
                            continue
                        N, d, coste = plazo(obs, mundo, mem, pos)
                        cuad[tuple(pos)] = {"item": e.get("item"), "tick": tick,
                                            "N": N}
                        if registra is not None:
                            registra({"k": "don", "tick": tick,
                                      "estado": "dado", "casilla": list(pos),
                                      "item": e.get("item"), "N": N, "d": d,
                                      "coste": coste})
            return ac, radio
        D.decide = _decide

        _orig_cands = D.candidatos

        def _cands(obs, mundo, mem, tick, bloqueos=None):
            cs = list(_orig_cands(obs, mundo, mem, tick, bloqueos))
            pos = tuple((obs.get("you") or {}).get("pos") or ())
            if not pos or not getattr(mem, "_dados6", None):
                return cs
            fuera = [n for n, r in cs
                     if r.get("tipo") == "coger"
                     and vivo(mem, tick, pos, (r.get("item") or {}).get("id"))]
            if not fuera:
                return cs
            if registra is not None:
                registra({"k": "don", "tick": tick, "estado": "no_lo_recojo",
                          "casilla": list(pos), "candidatos": fuera})
            return [(n, r) for n, r in cs if n not in fuera]
        D.candidatos = _cands
        hecho["don"] = True

    return hecho

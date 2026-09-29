"""[P5-7C · C0] Los humos de la curiosidad en el campo.

Corren DENTRO de la imagen y tumban el build si fallan.

  a) APAGADA: 200 tics de escena grabada, decision a decision IDENTICA a la
     politica de siempre. Es la puerta: si esto no pasa, el anadido no es
     inerte y no se juega nada.
  b) ENCENDIDA: el renglon ENTRA en la foto de los candidatos (M>0 en alguno),
     y la decision cambia alguna vez. Un renglon que no se enciende nunca no
     es un resultado, es un interruptor muerto (eso ya paso en P5-7A).
  c) EL TIEMPO: mediana del tic por debajo de 5 ms, y cero tics sin decision.
  d) EL REGISTRO: `curiosidad_tic` con sus campos en cada tic vivo.
  e) EL ENTORNO: crudo y efectivo en el diario, y la imagen viene APAGADA.
"""
from __future__ import annotations
import importlib, json, os, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
sys.path.insert(0, AQUI)

import humo_cortex as HC                                   # noqa: E402

FALLOS = []


def _recarga(**env):
    for k, v in env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    for m in ("curiosidad", "alma.policy_forma"):
        sys.modules.pop(m, None)
    import alma
    if hasattr(alma, "policy_forma"):
        delattr(alma, "policy_forma")
    PF = importlib.import_module("alma.policy_forma")
    assert PF.CURIOSIDAD == (env.get("GEMV_CURIOSIDAD") or ""), \
        ("el interruptor NO tomo", PF.CURIOSIDAD)
    return PF


def _escena():
    d = json.load(open(os.path.join(AQUI, "humo_200tics.json")))
    pc = dict(d["player_config"])
    pc["type"] = "player_config"
    pc["arena"] = {"size": d["static_map"].get("size") or 48,
                   "static_map": list(d["static_map"]["filas"]),
                   "legend": dict(d["static_map"].get("legend") or HC.LEY),
                   "pedestals": d["static_map"].get("pedestals") or []}
    pc["items"] = list(d["catalogo"]["items"])
    pc["stats"] = {"budget": 20, "min": 1, "max": 10, "default": [5, 5, 5, 5]}
    return d, pc


def _corre(cur):
    """Una pasada de 200 tics con el interruptor en `cur`. Devuelve el diario."""
    import asyncio
    PF = _recarga(GEMV_CURIOSIDAD=cur, GEMV_FORMA=None, GEMV_HILO_FORMA=None,
                  GEMV_CONSEJERO_FORMA=None, GEMV_FORMAS_AZAR=None)
    from alma import policy_cortex as PC
    from alma import humo_forma as HF
    d, pc = _escena()
    mensajes = [json.dumps(pc)]
    for r in d["ticks"]:
        mensajes.append(json.dumps(HF._obs(r)))
    mensajes.append(json.dumps({"type": "final", "placement": 9, "kills": 0,
                                "score": 0.0, "reason": "humo",
                                "match_ticks": d["ticks"][-1]["tick"]}))
    enviados = []

    class WS:
        def __aiter__(self):
            self._i = 0
            return self

        async def __anext__(self):
            if self._i >= len(mensajes):
                raise StopAsyncIteration
            m = mensajes[self._i]
            self._i += 1
            return m

        async def send(self, s):
            enviados.append(json.loads(s))

    alma = PF.AlmaForma()
    i0 = len(PC._DIARIO)
    asyncio.run(PC.decisor(WS(), alma))
    # `_DIARIO` guarda LINEAS de texto, no diccionarios
    out = []
    for linea in PC._DIARIO[i0:]:
        try:
            out.append(json.loads(linea))
        except Exception:
            pass
    return PF, out, enviados


def a_apagada_es_identica():
    _PF0, d0, e0 = _corre("")
    _PF1, d1, e1 = _corre("0")
    t0 = [r for r in d0 if r.get("k") == "tick" and r.get("RADIOGRAFIA")]
    t1 = [r for r in d1 if r.get("k") == "tick" and r.get("RADIOGRAFIA")]
    assert t0 and len(t0) == len(t1), ("distinto numero de decisiones",
                                       len(t0), len(t1))
    iguales = sum(1 for a, b in zip(t0, t1)
                  if a["RADIOGRAFIA"]["elegido"] == b["RADIOGRAFIA"]["elegido"]
                  and a["RADIOGRAFIA"].get("d_ahora")
                  == b["RADIOGRAFIA"].get("d_ahora"))
    cur = [r for r in d1 if r.get("k") == "curiosidad_tic"]
    assert not cur, ("apagada y AUN ASI registro curiosidad_tic", len(cur))
    assert iguales == len(t0), ("la apagada NO es identica",
                                iguales, len(t0))
    print(f"  (a) APAGADA identica: {iguales}/{len(t0)} decisiones, "
          f"mismo `elegido` y misma `d_ahora`; 0 registros de curiosidad")
    return len(t0)


def b_encendida_entra_y_cambia():
    PF, d, _e = _corre("frontera")
    cur = [r for r in d if r.get("k") == "curiosidad_tic"]
    tks = [r for r in d if r.get("k") == "tick" and r.get("RADIOGRAFIA")]
    assert cur, "ENCENDIDA y no hay un solo registro curiosidad_tic"
    ent = [r for r in cur if r.get("encendio")]
    dec = [r for r in cur if r.get("decidio")]
    campos = ("ign_global", "dist_frontera", "amenaza", "grado", "encendio",
              "decidio", "cands_con_M", "vistas", "ms_bfs")
    faltan = [c for c in campos if c not in cur[0]]
    assert not faltan, ("al registro le faltan campos", faltan)
    assert ent, ("el renglon NO se encendio en ningun tic: interruptor muerto")
    print(f"  (b) ENCENDIDA: {len(cur)} registros · el renglon ENTRA en "
          f"{len(ent)} tics ({100 * len(ent) / len(cur):.1f} %) · "
          f"M maximo {max(r['max_M'] for r in cur):.5f} · "
          f"DECIDE en {len(dec)} tics")
    print(f"      ignorancia global {cur[0]['ign_global']:.4f} -> "
          f"{cur[-1]['ign_global']:.4f} · vistas {cur[-1]['vistas']} casillas")
    if not dec:
        print("      AVISO: entro pero no volteo ninguna decision en 200 tics")
    return PF, d, cur, tks


def c_el_tiempo(d, cur, tks):
    # EL TIC ENTERO, no solo el decisor: `ms_total` incluye preparacion, BFS,
    # decision y contrafactual. Usar el `ms` de la RADIOGRAFIA daria una cifra
    # bonita y FALSA, porque deja fuera justo lo que anade la curiosidad.
    ms = [r["ms_total"] for r in cur if r.get("ms_total") is not None]
    assert ms, "el registro no trae ms_total: no se puede juzgar el tiempo"
    dec_ms = [r["RADIOGRAFIA"]["ms"] for r in tks
              if (r.get("RADIOGRAFIA") or {}).get("ms") is not None]
    med, mx = st.median(ms), max(ms)
    bfs = [r["ms_bfs"] for r in cur]
    cf = [r["ms_contrafactual"] for r in cur if r.get("ms_contrafactual")]
    vivos = {r["tick"] for r in tks}
    huecos = sorted(set(range(min(vivos), max(vivos) + 1)) - vivos)
    print(f"  (c) TIEMPO DEL TIC ENTERO: mediana {med:.3f} ms · maximo "
          f"{mx:.3f} ms")
    print(f"      desglose: decisor {st.median(dec_ms):.3f} · BFS "
          f"{st.median(bfs):.3f} · contrafactual "
          f"{st.median(cf) if cf else 0:.3f} ms (medianas)")
    print(f"      tics sin decision: {len(huecos)}")
    if med >= 5.0:
        FALLOS.append(f"mediana del tic {med:.3f} ms >= 5 ms")
    if huecos:
        FALLOS.append(f"{len(huecos)} tics sin decision")
    return med, mx


def e_el_entorno():
    PF = _recarga(GEMV_CURIOSIDAD="frontera")
    e = PF.entorno_forma()
    assert e["efectivo"]["CURIOSIDAD"] == "frontera"
    assert e["efectivo"]["CURIOSIDAD_ON"] is True
    assert e["crudo"]["GEMV_CURIOSIDAD"] == "frontera"
    PF0 = _recarga(GEMV_CURIOSIDAD=None)
    e0 = PF0.entorno_forma()
    assert e0["efectivo"]["CURIOSIDAD_ON"] is False, "la imagen NO viene apagada"
    print(f"  (e) ENTORNO: crudo y efectivo en el diario · la imagen viene "
          f"APAGADA (CURIOSIDAD_ON={e0['efectivo']['CURIOSIDAD_ON']}) · "
          f"k={e['efectivo']['CURIOSIDAD_K']} balanza="
          f"{e['efectivo']['CURIOSIDAD_BALANZA']}")


def main():
    print("== HUMOS DE LA CURIOSIDAD (P5-7C · C0) ==")
    n = a_apagada_es_identica()
    PF, d, cur, tks = b_encendida_entra_y_cambia()
    c_el_tiempo(d, cur, tks)
    e_el_entorno()
    if FALLOS:
        print("\nFALLOS:")
        for f in FALLOS:
            print("  ·", f)
        sys.exit(1)
    print(f"\nTODOS LOS HUMOS DE LA CURIOSIDAD OK ({n} decisiones por pasada)")


if __name__ == "__main__":
    main()

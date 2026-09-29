"""A — LA FOTO FRATERNA (PROMPT_22). Verificacion, sin tanda.

Diseccion de la PREVISION del candidato de defensa CONTRA EL HERMANO:
  1. ¿la foto de golpearle incluye el dolor de S-2 (su dano me duele)?
  2. ¿incluye algun precio de S-3 (el riesgo de su muerte)?
  3. si NO los incluye: ¿el agujero es solo en defensa o en TODOS los
     candidatos? ¿que filas de pareja quedan congeladas?

NO ARREGLA NADA. Interactua con una decision de mesa pendiente.

Uso (desde la raiz del repo):  PYTHONPATH=.:paintball python3 -m alma.verifica_22
"""
from __future__ import annotations

import sys

from alma.mundo import Mundo
from alma import appraisal_zs as A
from alma import decisor_zs as D
from alma.smoke_alma import player_config, obs

FILAS_PAREJA = ("S-SOLEDAD", "S-DANO-PAREJA", "S-MUERTE-PAREJA")


def main():
    mundo = Mundo.desde_player_config(player_config())
    PAR = mundo.teammate_slot
    YO = (24, 24)
    HERMANO = (25, 24)                      # pegado: a alcance de espada

    # El hermano nos ha danado dentro de la ventana del 09.
    o = obs(300, YO, hand={"id": "sword", "durability": 40},
            agentes=[{"slot": PAR, "team": "A", "pos": list(HERMANO),
                      "hp_band": "healthy"}])
    o["you"]["damage_taken"] = [{"source": f"P{PAR}", "amount": 20.0}]
    m = A.Memoria()
    m.hp_max = 100
    m.roce_B = 0.6                          # vinculo ya rodado
    m.observa(o, mundo, 300)

    print("=== la escena: el hermano nos pega 20 y esta pegado, con espada en mano ===")
    F0 = A.filas(o, mundo, m, 300)
    print(f"  filas AHORA: { {k: round(v, 5) for k, v in F0.items() if isinstance(v, float) and v} }")
    print(f"  agresores en memoria: {list(m.agresores)}")

    cands = dict(D.candidatos(o, mundo, m, 300))
    atacar = [k for k in cands if k.startswith("atacar_")]
    print(f"\n  candidatos de ataque en la mesa: {atacar}")
    if not atacar:
        print("  [n/a] no hay candidato de defensa contra el hermano; escena invalida")
        return 1

    _a, rad = D.decide(o, mundo, m, 300)
    det = rad.get("candidatos") or {}
    print(f"  ELIGE: {rad['elegido']}")

    print("\n=== 1-2. ¿que carga la foto de GOLPEAR AL HERMANO? ===")
    fa = (det.get(atacar[0]) or {}).get("filas") or {}
    fn = (det.get("noop") or {}).get("filas") or {}
    print(f"  {'fila':20s} {'noop':>10s} {'atacar':>10s}   ¿cambia?")
    todas = sorted(set(fa) | set(fn))
    movidas = []
    for k in todas:
        va, vn = fa.get(k, 0.0), fn.get(k, 0.0)
        cambia = "SI" if abs(va - vn) > 1e-9 else "no"
        if cambia == "SI":
            movidas.append(k)
        print(f"  {k:20s} {vn:10.5f} {va:10.5f}   {cambia}")

    print("\n  VEREDICTO de la diseccion:")
    s2 = "S-DANO-PAREJA" in movidas
    s3 = "S-MUERTE-PAREJA" in movidas
    print(f"    ¿la foto carga S-2 (su dano me duele)?      {'SI' if s2 else 'NO'}")
    print(f"    ¿la foto carga S-3 (el riesgo de su muerte)? {'SI' if s3 else 'NO'}")
    print(f"    filas que SI se mueven al golpearle: {movidas}")

    print("\n=== 3. alcance del agujero ===")
    print("  ¿de donde saca cada fila de pareja su valor en la PREVISION?")
    print("    S-DANO-PAREJA  <- mem.pareja_banda   (MEMORIA, no la observacion)")
    print("    S-MUERTE-PAREJA<- mem.pareja_muerta  (MEMORIA, no la observacion)")
    print("    S-SOLEDAD      <- mem.ticks_sin_compania + presencia por POSICION")
    print("  El golpe previsto escribe `_hp_est` en el agente objetivo, y `_hp_est`")
    print("  se lee en UN SOLO SITIO (appraisal_zs.py:565): la fila S-7.")
    # comprobacion directa: el hp previsto del hermano cambia, la fila no
    ob2 = D._obs_prevista(o, mundo, m, 300, YO, 100.0,
                          list(o["you"]["pack"]), o["you"]["hand"], True,
                          golpe=(PAR, 18.0))
    herm = next(a for a in ob2["visible"]["agents"] if a.get("slot") == PAR)
    F2 = A.filas(ob2, mundo, m, 300)
    print(f"\n  con el golpe previsto encima del hermano:")
    print(f"    su hp previsto (_hp_est) = {herm.get('_hp_est')}")
    for k in FILAS_PAREJA:
        print(f"    {k:16s} ahora {F0.get(k, 0.0):.5f}  ->  previsto {F2.get(k, 0.0):.5f}")
    print("\n  ALCANCE: la congelacion es de TODOS los candidatos, no solo del")
    print("  ataque — la banda de hp del hermano y su muerte salen de la memoria")
    print("  en cualquier prevision. Pero SOLO IMPORTA en el ataque, porque es el")
    print("  unico candidato cuyo efecto previsto recae sobre el hermano.")
    print("\n  NOTA POSTERIOR: en el PROMPT_22 este banco daba NO en S-2 y NO en")
    print("  S-3 (la foto estaba congelada). El PROMPT_23 arreglo la imaginacion:")
    print("  las dos filas de pareja leen ya el hp PREVISTO. Si hoy sale SI, es")
    print("  el arreglo, no un fallo de este banco.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

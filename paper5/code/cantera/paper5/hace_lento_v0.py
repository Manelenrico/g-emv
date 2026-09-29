"""[P5-1 A2] Construye lento_v0 a partir de la variante 'competition'.

Deriva el calendario del anillo de la del juego de hoy: mismas siete filas,
mismos radios y mismo dano, corridas para que la primera no avise antes del
40 % de la partida y estiradas por 1,25 para que el anillo sea mas lento.

SOLO LECTURA. Escribe cantera/paper5/lento_v0.json y lo valida.
"""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(AQUI, "manifiesto_zero_sum_0_1_18.json")))
COMP = next(v for v in MAN["variants"] if v["id"] == "competition")["game_config"]
ESQ = MAN["game"]["config_schema"]["properties"]

MAX_HOY = COMP["max_ticks"]                 # 9120
MAX_NUEVO = 2 * MAX_HOY                     # 18240, y el tope del campo es 20000
INICIO = int(0.40 * MAX_NUEVO)              # 7296: el 40 % exacto
ESTIRA = 1.25                               # el anillo, un 25 % mas lento


def calendario():
    """Las siete filas de hoy, corridas a INICIO y estiradas por ESTIRA."""
    z = COMP["zone"]["schedule"]
    t0 = z[0][0]                            # 1440, el primer aviso de hoy
    out = []
    for fila in z:
        w, s, d, r0, r1, dmg = fila
        out.append([INICIO + int(round((w - t0) * ESTIRA)),
                    INICIO + int(round((s - t0) * ESTIRA)),
                    INICIO + int(round((d - t0) * ESTIRA)),
                    r0, r1, dmg])
    return out


def main():
    z = calendario()
    cfg = {
        "max_ticks": MAX_NUEVO,
        "freeze_ticks": ESQ["freeze_ticks"]["maximum"],      # 480, el maximo
        "stat_budget": COMP["stat_budget"],                  # 20, sin tocar
        "zone": {"schedule": z},
        # el objeto sponsor va ENTERO: no sabemos si el servidor fusiona o
        # sustituye, y sustituir a medias perderia los 16 regalos.
        "sponsor": {
            "live": COMP["sponsor"]["live"],
            "budget_per_team": 2 * COMP["sponsor"]["budget_per_team"],  # 600
            "shop_opens_tick": COMP["sponsor"]["shop_opens_tick"],      # 1680
            "scripted_gifts": COMP["sponsor"]["scripted_gifts"],
        },
    }
    p = os.path.join(AQUI, "lento_v0.json")
    json.dump(cfg, open(p, "w"), ensure_ascii=False, indent=1)

    # --- comprobaciones contra el esquema y contra los objetivos ---
    print("CAMPO            hoy        lento_v0    limite del esquema")
    for k in ("max_ticks", "freeze_ticks", "stat_budget"):
        e = ESQ[k]
        print(f"  {k:14s} {COMP[k]:<10} {cfg[k]:<11} "
              f"[{e['minimum']}, {e['maximum']}]")
    sp, sh = cfg["sponsor"], COMP["sponsor"]
    print(f"  {'budget_per_team':14s} {sh['budget_per_team']:<10} "
          f"{sp['budget_per_team']:<11} "
          f"[{ESQ['sponsor']['properties']['budget_per_team']['minimum']}, "
          f"{ESQ['sponsor']['properties']['budget_per_team']['maximum']}]")
    print(f"  {'regalos':14s} {len(sh['scripted_gifts']):<10} "
          f"{len(sp['scripted_gifts']):<11} (los mismos)")
    print("\nCALENDARIO DEL ANILLO  [aviso, encoge, hecho, r0, r1, dano/s]")
    for a, b in zip(COMP["zone"]["schedule"], z):
        print(f"  hoy {str(a):36s} -> {b}")
    print(f"\n  primer aviso:  {z[0][0]} = {100*z[0][0]/MAX_NUEVO:.1f} % "
          f"de la partida (hoy {COMP['zone']['schedule'][0][0]} = "
          f"{100*COMP['zone']['schedule'][0][0]/MAX_HOY:.1f} %)")
    print(f"  empieza a encoger: {z[0][1]} = {100*z[0][1]/MAX_NUEVO:.1f} %")
    print(f"  ultimo 'hecho': {z[-1][2]} = {100*z[-1][2]/MAX_NUEVO:.1f} % · "
          f"cola de {MAX_NUEVO - z[-1][2]} tics "
          f"({100*(MAX_NUEVO-z[-1][2])/MAX_NUEVO:.1f} %; hoy "
          f"{MAX_HOY - COMP['zone']['schedule'][-1][2]} = "
          f"{100*(MAX_HOY-COMP['zone']['schedule'][-1][2])/MAX_HOY:.1f} %)")
    print(f"  el anillo dura {z[-1][2]-z[0][0]} tics; hoy "
          f"{COMP['zone']['schedule'][-1][2]-COMP['zone']['schedule'][0][0]}")
    print(f"\n  juego ANTES del anillo: {z[0][0] - cfg['freeze_ticks']} tics "
          f"vivos; hoy {COMP['zone']['schedule'][0][0] - COMP['freeze_ticks']}")
    try:
        import jsonschema
        jsonschema.validate(dict(cfg, tokens=["t"] * 16),
                            MAN["game"]["config_schema"])
        print("\nVALIDACION contra el config_schema del manifiesto: PASA")
    except ImportError:
        print("\nVALIDACION: jsonschema no instalado; no se valida")
    print("escrito:", p)


if __name__ == "__main__":
    main()

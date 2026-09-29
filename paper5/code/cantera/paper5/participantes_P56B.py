"""[P5-6B] ¿Es la MISMA partida en los tres brazos? Asiento a asiento."""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))


def roster_de(d):
    e = (d.get("episodes") or [{}])[0]
    for clave in ("roster", "participants", "players"):
        r = e.get(clave) or d.get(clave)
        if r:
            return r, clave
    return None, None


def main():
    mapas = {}
    for b in ("A","F","F2","T"):
        p = os.path.join(AQUI, f"P56B_{b}_final.json")
        if not os.path.exists(p):
            print(b, "sin final"); continue
        d = json.load(open(p))
        r, clave = roster_de(d)
        if r is None:
            print(b, "sin roster en la respuesta; claves del episodio:",
                  list((d.get("episodes") or [{}])[0])[:15]); continue
        m = {}
        for x in r:
            pos = x.get("position", x.get("slot"))
            m[pos] = x.get("policy_name") or x.get("policy_version_id")
        mapas[b] = m
        print(f"{b} (de `{clave}`): {len(m)} asientos")
    if len(mapas) < 2:
        return
    ref = mapas.get("A") or list(mapas.values())[0]
    print("\nasiento | " + " | ".join(mapas))
    iguales = 0
    for pos in sorted(ref, key=lambda z: (z is None, z)):
        fila = [mapas[b].get(pos, "—") for b in mapas]
        ok = len(set(fila)) == 1
        iguales += ok
        print(f"  {str(pos):>6s} | " + " | ".join(f"{x[:26]:26s}" for x in fila)
              + ("" if ok else "   <-- DISTINTO"))
    print(f"\nasientos iguales en los tres: {iguales} de {len(ref)}")


if __name__ == "__main__":
    main()

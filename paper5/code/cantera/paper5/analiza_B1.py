"""[P5-1 B1] Lee los dos diarios del episodio y saca las cifras del informe.

SOLO LECTURA sobre los .art.log. Vuelca cantera/paper5/B1_medidas.json.
"""
import collections, glob, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DEST = os.path.join(RAIZ, "paintball", "runs", "P5_B1")


def lee(f):
    out = []
    for ln in open(f):
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    return out


def mide(f):
    rs = lee(f)
    tics = [r for r in rs if r.get("k") == "tick"]
    fases = collections.Counter(r.get("phase") for r in tics)
    vivos = [r for r in tics if r.get("phase") == "live"]
    t = [r["tick"] for r in tics if isinstance(r.get("tick"), int)]
    ev, prim = collections.Counter(), {}
    for r in tics:
        for e in (r.get("eventos") or []):
            n = (e.get("kind") or e.get("type") or json.dumps(e)[:40]
                 ) if isinstance(e, dict) else str(e)[:40]
            ev[n] += 1
            prim.setdefault(n, r["tick"])
    pc = next((r for r in rs if r.get("k") == "player_config"), {})
    art = [r for r in rs if r.get("k") == "artefacto"]
    hp = [(r["tick"], r.get("hp")) for r in vivos if r.get("hp") is not None]
    # el ultimo tic con hp > 0, y la zona en el primer aviso
    zonas = []
    vista = None
    for r in tics:
        z = r.get("zona") or {}
        c = (z.get("radius"), z.get("damage_per_s"), z.get("warn_tick"),
             z.get("shrink_tick"), z.get("next_radius"))
        if c != vista:
            zonas.append({"tick": r["tick"], "radius": z.get("radius"),
                          "damage_per_s": z.get("damage_per_s"),
                          "warn_tick": z.get("warn_tick"),
                          "shrink_tick": z.get("shrink_tick"),
                          "next_radius": z.get("next_radius")})
            vista = c
    return {
        "fichero": os.path.basename(f),
        "bytes": os.path.getsize(f),
        "lineas": len(rs),
        "registros por clase": dict(collections.Counter(
            r.get("k") for r in rs).most_common(10)),
        "primer tic": min(t) if t else None,
        "ultimo tic": max(t) if t else None,
        "tics por fase": dict(fases),
        "tics vivos": len(vivos),
        "hp al empezar": hp[0][1] if hp else None,
        "hp al acabar": hp[-1][1] if hp else None,
        "ultimo tic con hp>0": max((x[0] for x in hp if (x[1] or 0) > 0),
                                   default=None),
        "eventos": {k: {"veces": v, "primer tic": prim[k]}
                    for k, v in ev.most_common()},
        "player_config": {k: pc.get(k) for k in
                          ("max_ticks", "ignition_tick", "tick_rate", "slot")},
        "artefacto": art,
        "cambios de zona": zonas,
    }


def main():
    fs = sorted(glob.glob(os.path.join(DEST, "*.art.log")))
    if not fs:
        sys.exit("no hay diarios en " + DEST)
    out = {os.path.basename(f).split("policy_agent_")[1][:2].strip("."): mide(f)
           for f in fs}
    json.dump(out, open(os.path.join(AQUI, "B1_medidas.json"), "w"),
              ensure_ascii=False, indent=1)
    for k, m in out.items():
        print(f"\n=== asiento {k} · {m['fichero']}")
        print(f"  {m['bytes']:,} B · {m['lineas']:,} lineas")
        print(f"  tics {m['primer tic']}..{m['ultimo tic']} · por fase "
              f"{m['tics por fase']} · VIVOS {m['tics vivos']:,}")
        print(f"  hp {m['hp al empezar']} -> {m['hp al acabar']} · "
              f"ultimo tic con hp>0: {m['ultimo tic con hp>0']}")
        print(f"  player_config: {m['player_config']}")
        print(f"  eventos: " + ", ".join(
            f"{k2} x{v['veces']} (1º {v['primer tic']})"
            for k2, v in m["eventos"].items()))
        for a in m["artefacto"]:
            print(f"  artefacto: {a.get('motivo')} tic {a.get('tick')} "
                  f"codigo {a.get('codigo')} zip {a.get('bytes_zip'):,} B "
                  f"diario {a.get('bytes_diario'):,} B "
                  f"lineas {a.get('lineas'):,}")
        print("  zona, cambio a cambio:")
        for z in m["cambios de zona"]:
            print(f"    tic {z['tick']:6} radio {z['radius']} dano/s "
                  f"{z['damage_per_s']} (aviso {z['warn_tick']}, encoge "
                  f"{z['shrink_tick']}, siguiente {z['next_radius']})")


if __name__ == "__main__":
    main()

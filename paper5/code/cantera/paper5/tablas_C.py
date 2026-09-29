"""[P5-1 fase C] Las tablas del informe, a partir de C_medidas.json."""
import collections, datetime as dt, json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(AQUI, "C_medidas.json")))
T = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
ORD = sorted(M)


def pct(a, b):
    return f"{100.0*a/b:5.2f} %" if b else "  n/a"


print("=== C1 · LA CALMA ===")
print(f"{'asiento-partida':16s} {'vivos':>7s} {'literal':>9s} {'declarada':>11s} "
      f"{'paper 4':>9s} {'tramo lit':>10s} {'tramo dec':>10s}")
tot = collections.Counter()
for k in ORD:
    m = M[k]; v = m["tics vivos"]
    tot["vivos"] += v; tot["lit"] += m["calma literal"]
    tot["dec"] += m["calma declarada"]
    tot["p4"] += m["medida del paper cuatro (ninguna fila M>0)"]
    tr = m["primer tramo de calma desde 481"]
    print(f"{k:16s} {v:7,} {m['calma literal']:4,} {pct(m['calma literal'],v)} "
          f"{m['calma declarada']:5,} {pct(m['calma declarada'],v)} "
          f"{m['medida del paper cuatro (ninguna fila M>0)']:9,} "
          f"{tr['literal']['tics']:10} {tr['declarada']['tics']:10}")
print(f"{'TOTAL':16s} {tot['vivos']:7,} {tot['lit']:4,} {pct(tot['lit'],tot['vivos'])} "
      f"{tot['dec']:5,} {pct(tot['dec'],tot['vivos'])} {tot['p4']:9,}")

print("\n=== C7 · que rompe el primer tramo, desde el 481 ===")
for k in ORD:
    tr = M[k]["primer tramo de calma desde 481"]
    for nom in ("literal", "declarada"):
        x = tr[nom]
        r = x["lo rompe"] or {}
        print(f"  {k:16s} {nom:10s} {x['tics']:5} tics · tic {r.get('tick')} · "
              f"{r.get('fila') or r.get('motivo')} = {r.get('valor')}")

print("\n=== C2 · que hace el cuerpo en calma (declarada) ===")
print(f"{'asiento-partida':16s} {'donde':10s} {'tics':>7s} {'noop':>8s} "
      f"{'ir_centro':>10s} {'ir_botin':>9s} {'otros':>8s} {'casillas/100 tics':>18s}")
for k in ORD:
    m = M[k]
    for donde, clave, nt in (("en calma", "declarada", m["calma declarada"]),
                             ("fuera", "fuera", m["tics vivos"] - m["calma declarada"])):
        a = m["acciones"][clave]
        s = sum(a.values())
        nv = m["casillas nuevas"]["declarada" if clave == "declarada" else "fuera"]
        if not s:
            print(f"{k:16s} {donde:10s} {0:7,}   (sin tics: no se puede repartir)")
            continue
        print(f"{k:16s} {donde:10s} {s:7,} "
              f"{pct(a.get('noop',0),s):>8s} {pct(a.get('ir_centro',0),s):>10s} "
              f"{pct(a.get('ir_botin',0),s):>9s} {pct(a.get('otros',0),s):>8s} "
              f"{100.0*nv/s:18.2f}")

print("\n=== C3 · que fila manda, y las dos erres ===")
for k in ORD:
    m = M[k]; v = m["tics vivos"]
    manda = m["fila que manda"]
    top = list(manda.items())[:4]
    print(f"  {k:16s} manda: " + " · ".join(f"{a} {pct(b,v)}" for a, b in top))
    viv = m["filas vivas (M>0)"]
    print(f"{'':18s} R-CARENCIA viva {pct(viv.get('R-CARENCIA',0),v)} · "
          f"R-LLAMADA viva {pct(viv.get('R-LLAMADA',0),v)}")

print("\n=== C4 · anillo, duracion y muerte ===")
for k in ORD:
    m = M[k]; c = m["C6"]
    print(f"  {k:16s} match_ticks {c['match_ticks']:6} · {c['reason']:12s} "
          f"puesto {c['placement']:2} · score {c['score']} · "
          f"vivos {m['tics vivos']:,} · ultimo golpe registrado {c['ultimo golpe registrado']}")

print("\n=== C6 · primer armado, primer dano, muerte (con politica) ===")
for k in ORD:
    m = M[k]; c = m["C6"]; p = m.get("participants") or {}
    q = lambda s: p.get(str(s), p.get(s, "?")) if s is not None else "-"
    pa = c["primer armado a la vista"]
    pd = c["primer dano"]; ug = c["ultimo golpe registrado"]
    def politica(fuente):
        if not isinstance(fuente, str):
            return "-"
        if fuente == "zone":
            return "el anillo"
        if fuente.startswith("P") and fuente[1:].isdigit():
            return f"asiento {fuente[1:]} = {q(int(fuente[1:]))}"
        return fuente
    print(f"  {k}")
    print(f"     primer armado a la vista: tic {pa['tick'] if pa else '-'} · "
          f"asiento {pa['slot'] if pa else '-'} = {q(pa['slot']) if pa else '-'} "
          f"({pa['mano'] if pa else '-'})")
    print(f"     primer dano recibido    : tic {pd['tick'] if pd else '-'} · "
          f"{politica(pd['fuente']) if pd else '-'}")
    print(f"     ultimo golpe registrado : tic {ug['tick']} · {politica(ug['fuente'])}")
    print(f"     muere en el tic {c['match_ticks']} · vida en el ultimo tic visto "
          f"{c['vida en el ultimo tic visto']} · dentro del anillo "
          f"{c['dentro del anillo en el ultimo tic']} · golpes en los ultimos 48 tics: "
          f"{[(g['tick'], g['fuente']) for g in c['golpes en los ultimos 48 tics vistos']]}")

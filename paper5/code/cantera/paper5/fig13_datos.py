"""[P5-FIG · 1 y 3] Los datos de una vida del mundo lento. SOLO LECTURA."""
import glob, json, sys
sys.path.insert(0, "cantera/paper4"); sys.path.insert(0, "cantera/paper5")
import serie_util as U, curiosidad as C

f = sorted(glob.glob("paintball/runs/P57C_t2_A_20994019/*policy_agent_10*.art.log"))[0]
recs = list(U.lee(f))
pc = next(r for r in recs if r.get("k") == "player_config")
sm = next(r for r in recs if r.get("k") == "static_map")
cat = next(r for r in recs if r.get("k") == "catalogo")
mundo = U.mundo_de(pc, list(sm["filas"]), cat["items"])
herm = pc.get("teammate_slot")
vivos = [r for r in recs if r.get("k") == "tick" and r.get("phase") == "live"]
fin = next((r for r in recs if r.get("k") == "final"), {})

ojo = C.Ojo(mundo, 8)
dh = []
T, HP, CAR, DD, IGN, AM, GOLPE = [], [], [], [], [], [], []
for r in vivos:
    t = r["tick"]
    p = tuple(r.get("pos") or ())
    if p:
        ojo.mira(p, t)
    d = sum(float(x.get("amount") or 0) if isinstance(x, dict) else 0.0
            for x in (r.get("damage_taken") or []))
    dh.append((t, d))
    ra = r.get("RADIOGRAFIA") or {}
    fl = (ra.get("ahora") or {}).get("filas") or {}
    d100 = sum(v for (tt, v) in dh if 0 <= t - tt < C.VENTANA_DANO)
    am, _ = C.amenaza(r, mundo, herm, d100, t)
    T.append(t); HP.append(r.get("hp"))
    CAR.append((fl.get("R-CARENCIA") or {}).get("M"))
    DD.append(ra.get("d_ahora"))
    IGN.append(round(ojo.ignorancia_global(), 5))
    AM.append(round(am, 5))
    if d > 0:
        GOLPE.append((t, d))

# la meseta: tramo mas largo con amenaza 0 y el mapa sin ver clavado
mej = (0, None, None); ini = None; n = 0; prev = None
for i, t in enumerate(T):
    if AM[i] == 0.0 and prev is not None and IGN[i] == prev:
        if n == 0:
            ini = T[i-1]
        n += 1
        if n > mej[0]:
            mej = (n, ini, t)
    else:
        n = 0
    prev = IGN[i]

json.dump({"diario": f, "asiento": "P57C_t2_A_20994019/10",
           "T": T, "hp": HP, "carencia": CAR, "d": DD, "ign": IGN, "amenaza": AM,
           "golpes": GOLPE, "meseta": {"largo": mej[0], "ini": mej[1], "fin": mej[2],
                                       "valor": IGN[T.index(mej[2])] if mej[2] else None},
           "final": {k: fin.get(k) for k in ("placement", "kills", "reason", "match_ticks")},
           "freeze_ticks": 480, "aviso_anillo": 7296},
          open("cantera/paper5/FIG13_datos.json", "w"))
print(f"  {len(T)} instantes · hp final {HP[-1]} · puesto {fin.get('placement')} · {fin.get('reason')}")
print(f"  golpes recibidos: {len(GOLPE)} · primero en el tic {GOLPE[0][0] if GOLPE else '—'}")
print(f"  carencia: min {min(x for x in CAR if x is not None):.4f} · max {max(x for x in CAR if x is not None):.4f}")
print(f"  MESETA: {mej[0]} instantes, del {mej[1]} al {mej[2]}, con el mapa sin ver clavado en "
      f"{IGN[T.index(mej[2])]:.4f}")
print(f"  mapa sin ver: {IGN[0]:.4f} -> {IGN[-1]:.4f}")

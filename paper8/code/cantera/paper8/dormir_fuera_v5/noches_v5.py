"""[P8] Prompt 140: cada noche de cada criatura, reconstruida con los registros de partidas ya jugadas (no se juega nada ni se llama a ningún modelo).
Partidas: RG68r y RG068r del experimento v5 en sequía y sequía dura (40 semillas cada una), días 0 a 9; y las seis del piloto del prompt 139 (RZ1 y RG68r,
normal 1001, sequía 1002, bestias que crían 1003, 40 días), que además llevan el registro del diario v2 (la duda: lo elegido, la segunda opción y la
diferencia; y las filas que más pesan en la foto de ahora).
LAS REGLAS (declaradas; son de este recuento):
  - el anochecer empieza en el turno 240 del día y la noche en el 280 (config_valle.json → dia.fases: mañana 120, tarde 120, anochecer 40, noche 120);
  - una noche es «fuera» si en la fase noche está dormida fuera de su casa (sitio distinto de «C» en balance.jsonl.gz) más de la mitad de los turnos; «dentro»
    si está dormida dentro de su casa más de la mitad; si no, «despierta» (como la noche dormida dentro de gemela_v5/extrae_gemela_v5.py);
  - EL SUEÑO: el primer turno desde el 240 del día en que está dormida (mundo.jsonl.gz → cuerpo.dormida). «Agotada» si en ese turno el mundo la tiene
    agotada (cuerpo.agotada: se duerme a la fuerza); «eligió dormir» si su decisión de ese turno (decisiones.jsonl.gz) fue dormir;
  - A CUÁNTOS TURNOS DE CASA: los pasos del camino más corto (sin contar a nadie) desde donde está hasta la puerta de su casa, más uno para entrar
    (diario_v1.MAPA.distancias; 0 si ya está dentro);
  - LAS DECISIONES desde 40 turnos antes del anochecer (el 200) hasta el sueño, y LO QUE HIZO (las acciones del mundo) en los 40 turnos antes del sueño: lo que eligió en cada una (decisiones.jsonl.gz: la opción, por su «que» o su acción). Los turnos sin
    fila son los que siguió un destino comprometido o hizo una llamada (no decide). En las partidas con diario: la segunda opción y la diferencia (duda);
  - CON LA HERMANA / CON VECINAS: a 2 casillas o menos en el turno del sueño;
  - VOLVER A CASA: el turno en que entra en su casa por primera vez desde el 160 (la mitad de la tarde); y desde cuándo vuelve: el primer turno de la
    última racha en que la distancia a casa no sube hasta entrar (con al menos 3 turnos de racha). Y en RG68r, la primera decisión «ir_casa» desde el 160;
  - EL ÁRBOL: cogió fruta dulce ese día (bolsa_origen «dulce» al coger).
   python3 dormir_fuera_v5/noches_v5.py -> dormir_fuera_v5/noches_<variante>_<mundo>_<semilla>.json"""
import gzip, json, os, sys
from collections import Counter, defaultdict
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); P8 = os.path.dirname(AQUI); sys.path.insert(0, P8)
import diario_v1 as V1
MAPA, DIA = V1.MAPA, V1.DIA
FASES = {}; _t = 0
for _f, _n in V1.CFG["dia"]["fases"]: FASES[_f] = (_t, _t + _n); _t += _n
T_ANO, T_NOCHE = FASES["anochecer"][0], FASES["noche"][0]
EXP = "/Volumes/Mem G-EMV/valle_experimento_v5"; PIL = "/Volumes/Mem G-EMV/valle_rz1_piloto"
DIST = {k: MAPA.distancias([MAPA.puerta[k]]) for k in MAPA.puerta}
cheb = lambda p, q: max(abs(p[0] - q[0]), abs(p[1] - q[1]))
her = lambda a: a[0] + ("2" if a[1] == "1" else "1")

def dist_casa(a, pos, sitio):
    if sitio == "C": return 0
    d = DIST[a[0]].get(tuple(pos)); return None if d is None else d + 1

def nombre_op(c):
    return (c.get("que") or c.get("accion")) if isinstance(c, dict) else c

def una(x):
    v, mu, s, carp, dias, salida = x; d = os.path.join(carp, f"{v}_{mu}+sabores_s{s}_d40"); out = os.path.join(AQUI, salida)
    if os.path.exists(out): return out
    M = {}; S = {}; DEC = {}; DZ = {}
    for l in gzip.open(os.path.join(d, "mundo.jsonl.gz"), "rt", encoding="utf-8"):
        m = json.loads(l); t = m["turno"]
        if t >= dias * DIA: break
        M[t] = {a: (g["pos"], g["cuerpo"]["dormida"], g["cuerpo"]["agotada"], g["cuerpo"]["muerta"], g.get("accion"), g.get("resultado"), g.get("de"), (g.get("bolsa_origen") or [None])[-1] if g.get("accion") == "coger" else None, g["cuerpo"]["hambre"])
                for a, g in m["agentes"].items() if isinstance(g, dict) and "cuerpo" in g}
    for l in gzip.open(os.path.join(d, "balance.jsonl.gz"), "rt", encoding="utf-8"):
        b = json.loads(l); t = b["t"]
        if t >= dias * DIA: break
        S[t] = {a: c[5] for a, c in b["c"].items()}
    fd = os.path.join(d, "decisiones.jsonl.gz")
    if os.path.exists(fd):
        for l in gzip.open(fd, "rt", encoding="utf-8"):
            r = json.loads(l)
            if r[0] < dias * DIA: DEC[(r[0], r[1])] = r[2]
    fz = os.path.join(d, "diario.jsonl.gz")
    if os.path.exists(fz):
        for l in gzip.open(fz, "rt", encoding="utf-8"):
            r = json.loads(l); t = r["t"]
            if t >= dias * DIA: break
            for a, z in r["c"].items():
                if z.get("duda") or z.get("pierde"): DZ[(t, a)] = {"duda": z.get("duda"), "pierde": z.get("pierde"), "gana": z.get("gana")}
    N = []
    for dia in range(dias):
        t0 = dia * DIA
        for a in sorted(M.get(t0 + T_NOCHE, {})):
            if M[t0 + T_NOCHE][a][3]: continue
            noche = [t for t in range(t0 + T_NOCHE, t0 + DIA) if t in M and a in M[t] and not M[t][a][3]]
            dentro = sum(1 for t in noche if M[t][a][1] and S.get(t, {}).get(a) == "C"); fuera = sum(1 for t in noche if M[t][a][1] and S.get(t, {}).get(a) not in ("C", None))
            tipo = "dentro" if dentro * 2 > len(noche) else ("fuera" if fuera * 2 > len(noche) else "despierta")
            ts = next((t for t in range(t0 + T_ANO, t0 + DIA) if t in M and a in M[t] and M[t][a][1]), None)
            p240 = M[t0 + T_ANO][a][0] if a in M.get(t0 + T_ANO, {}) else None; s240 = S.get(t0 + T_ANO, {}).get(a)
            dec = [(t - t0, DEC[(t, a)]) for t in range(t0 + T_ANO - 40, (ts if ts is not None else t0 + DIA) + 1) if (t, a) in DEC]
            acc = Counter(M[t][a][4] for t in range(max(t0 + T_ANO - 40, (ts if ts is not None else t0 + DIA) - 40), ts if ts is not None else t0 + DIA) if t in M and a in M[t])
            ent = next((t for t in range(t0 + 160, t0 + DIA) if S.get(t, {}).get(a) == "C"), None)
            vuelta = None
            if ent is not None and S.get(t0 + 160, {}).get(a) != "C":
                ds = {t: dist_casa(a, M[t][a][0], S.get(t, {}).get(a)) for t in range(t0 + 160, ent + 1) if t in M and a in M[t]}
                k = ent
                while k - 1 in ds and ds[k - 1] is not None and ds[k] is not None and ds[k - 1] >= ds[k]: k -= 1
                if ent - k >= 3: vuelta = (k - t0, ds[k])
            ir1 = next((t - t0 for t in range(t0 + 160, t0 + DIA) if DEC.get((t, a)) == "ir_casa"), None)
            sueno = None
            if ts is not None:
                pos = M[ts][a][0]; st = S.get(ts, {}).get(a); hp = M[ts].get(her(a)); vec = [b for b, g in M[ts].items() if b not in (a, her(a)) and not g[3] and cheb(g[0], pos) <= 2]
                sueno = {"t": ts - t0, "sitio": st, "dist": dist_casa(a, pos, st), "agotada": bool(M[ts][a][2]), "eligio_dormir": DEC.get((ts, a)) == "dormir" or DEC.get((ts - 1, a)) == "dormir",
                         "hermana_cerca": bool(hp and not hp[3] and cheb(hp[0], pos) <= 2), "vecinas_cerca": len(vec), "hambre": M[ts][a][8]}
            dulce = any(M[t][a][7] == "dulce" and M[t][a][5] == "ok" for t in range(t0, t0 + DIA) if t in M and a in M[t])
            det = [{"t": t - t0, **DZ[(t, a)]} for t in range(t0 + T_ANO, (ts if ts is not None else t0 + DIA) + 1) if (t, a) in DZ and DZ[(t, a)].get("duda")]
            ahora = DZ.get((ts, a)) if ts is not None else None
            N.append({"a": a, "dia": dia, "tipo": tipo, "sitio240": s240, "dist240": dist_casa(a, p240, s240) if p240 else None, "sueno": sueno, "decisiones": dec, "acciones": dict(acc),
                      "entra": None if ent is None else ent - t0, "vuelta": vuelta, "ir_casa_1": ir1, "dulce": dulce, "detalle": det, "filas_ahora_al_dormir": ahora})
    json.dump({"v": v, "mu": mu, "s": s, "noches": N}, open(out, "w"), ensure_ascii=False, separators=(",", ":")); return out


if __name__ == "__main__":
    T_ = [(v, mu, s, EXP, 10, f"noches_{v}_{mu}_{s}.json") for v in ("RG68r", "RG068r") for mu in ("sequia", "sequia_dura") for s in range(30121, 30161)]
    T_ += [(v, mu, s, PIL, 40, f"piloto_{v}_{mu}_{s}.json") for v in ("RG68r", "RZ1") for mu, s in (("normal", 1001), ("sequia", 1002), ("bestias_crian", 1003))]
    with Pool(6) as p: r = p.map(una, T_)
    print(len(r), "partidas")

"""[P7-4] CALCULO EN SECO de la huella de tres dominios (cuerpo, recursos, vinculo) para los usos de botiquin de P7-1, sobre los diarios
de A4. Es un calculo de banco (no codigo del cuerpo). Definiciones, declaradas:
  ventana: del tic t del `use` a t_fin = t + 49 (canal del catalogo 48 + 1, el mismo cierre que P7-1); si la vida acaba antes, se descarta.
  CUERPO:   efecto bruto = hp(t_fin) - hp(t); lo esperado sin la cosa = -dano recibido en (t, t_fin] (la imaginacion del cuerpo no
            preve el dano entrante: la foto de `noop` deja el hp igual, decisor_zs.py:307-330; el dano que de todos modos llego lo lee el
            cuerpo tic a tic en `damage_taken`); efecto = bruto - esperado = hp_fin - hp + dano = la cura real de P7-1.
            importancia = |malestar_F(t_fin) - malestar_F(t)|, con malestar_F = suma de la columna F de las filas con signo '-' menos la de
            signo '+' en RADIOGRAFIA.ahora.filas (lo que el cuerpo calculo en ese tic).
  RECURSOS: efecto = unidades en mano+zurron+cuerpo en t_fin menos en t (todas las clases); esperado sin la cosa = 0 (la foto de `noop`
            deja el zurron igual); se da aparte el cambio en botiquines y en W (RADIOGRAFIA.ahora.W). importancia = |Delta malestar_R|.
  VINCULO:  efecto = distancia al hermano en t_fin menos en t (vista si lo ve, `social.dist_pareja`; si no, al `pareja_pos_recordada`);
            esperado sin la cosa = 0 (la foto congela al hermano, decisor_zs.py:318-324). importancia = |Delta malestar_S|.
  intensidad = 1 + min(1, (|imp_F| + |imp_R| + |imp_S|) / E), E = 1,5 (tres ejes, techo 0,5 por fila: ALCANCE_TECHO, ANT_TECHO, AGRESOR_CAP);
            tope 2 por construccion.
-> P7_4_huella.json"""
import collections, glob, json, math, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..")); VENT = 49; E = 1.5
J = json.load(open(os.path.join(AQUI, "P7_1_diario.json")))["botiquin"]
por = collections.defaultdict(list)
for f in J: por[f["vida"]].append(f)
def unidades(r):
    c = 0; h = r.get("hand") or {}
    if h.get("id") not in (None, "none"): c += int(h.get("n") or 1)
    for s in r.get("pack") or []:
        if s: c += int(s.get("n") or 1)
    if r.get("body"): c += 1
    return c
def kits(r): return sum(int(s.get("n") or 1) for s in (r.get("pack") or []) if s and s.get("id") == "first_aid")
def malestar(r):
    fl = ((r.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas")
    if not fl: return None
    out = {}
    for eje in ("F", "R", "S"):
        out[eje] = sum((v.get(eje) or 0.0) * (1 if v.get("signo") == "-" else -1) for v in fl.values() if isinstance(v, dict) and v.get(eje) is not None)
    return out
def dist_h(r):
    s = r.get("social") or {}
    if s.get("dist_pareja") is not None: return float(s["dist_pareja"]), "vista"
    q = s.get("pareja_pos_recordada")
    return (math.dist(r["pos"], q), "recordada") if q else (None, None)
def hp_h(r):
    p = ((r.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("parte")
    return (p or {}).get("hp")
OUT = []
for vida, filas in por.items():
    carp, slot = vida.split("/"); f = glob.glob(os.path.join(RAIZ, "paintball", "runs", carp, f"*policy_agent_{slot}.art.log"))[0]
    quiero = {}
    for x in filas:
        for u in range(x["t"], x["t"] + VENT + 1): quiero[u] = x["t"]
    T = {}
    for line in open(f):
        if '"tick"' not in line[:60]: continue
        try: r = json.loads(line)
        except Exception: continue
        if r.get("k") == "tick" and r["tick"] in quiero: T[r["tick"]] = r
    for x in filas:
        t = x["t"]; tf = t + VENT; r0 = T.get(t); r1 = T.get(tf)
        if r0 is None or r1 is None: OUT.append({"vida": vida, "t": t, "descartado": "la vida acaba antes de t_fin"}); continue
        dano = sum(float(d.get("amount") or 0) for u in range(t + 1, tf + 1) if u in T for d in (T[u].get("damage_taken") or []))
        m0, m1 = malestar(r0), malestar(r1); d0, c0 = dist_h(r0); d1, c1 = dist_h(r1)
        rec = {"vida": vida, "t": t, "resultado": x["paso"]["resultado"], "dentro": x["situacion"]["dentro"],
               "cuerpo": {"hp": r0["hp"], "hp_fin": r1["hp"], "bruto": r1["hp"] - r0["hp"], "dano_ventana": round(dano, 2), "efecto": round(r1["hp"] - r0["hp"] + dano, 2), "fuentes": sorted({d.get("source") for u in range(t + 1, tf + 1) if u in T for d in (T[u].get("damage_taken") or [])})},
               "recursos": {"unidades": unidades(r0), "unidades_fin": unidades(r1), "efecto": unidades(r1) - unidades(r0), "kits": kits(r0), "kits_fin": kits(r1), "W": ((r0.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("W"), "W_fin": ((r1.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("W")},
               "vinculo": {"dist": d0, "dist_fin": d1, "como": (c0, c1), "efecto": (round(d1 - d0, 2) if (d0 is not None and d1 is not None) else None), "hp_hermano": hp_h(r0), "hp_hermano_fin": hp_h(r1)},
               "importancia": {eje: (round(abs(m1[eje] - m0[eje]), 4) if (m0 and m1) else None) for eje in ("F", "R", "S")}}
        imp = rec["importancia"]; tot = sum(v for v in imp.values() if v is not None) if all(v is not None for v in imp.values()) else None
        rec["intensidad"] = (round(1 + min(1.0, tot / E), 4) if tot is not None else None); rec["suma_importancias"] = (round(tot, 4) if tot is not None else None)
        OUT.append(rec)
V = [o for o in OUT if "descartado" not in o]
def q(v, p):
    v = sorted(v)
    if not v: return None
    k = (len(v) - 1) * p; i = int(k); return round(v[i] + (v[min(i + 1, len(v) - 1)] - v[i]) * (k - i), 3)
def tri(v): v = [x for x in v if x is not None]; return {"n": len(v), "mediana": q(v, .5), "p10": q(v, .1), "p90": q(v, .9)}
R = {"usos": len(OUT), "con_ventana": len(V), "descartados": len(OUT) - len(V), "E": E, "ventana": VENT, "por_resultado": {}}
for res in ("completado", "cancelado"):
    g = [o for o in V if o["resultado"] == res]
    R["por_resultado"][res] = {"n": len(g),
        "cuerpo_bruto": tri([o["cuerpo"]["bruto"] for o in g]), "cuerpo_efecto": tri([o["cuerpo"]["efecto"] for o in g]), "dano_ventana": tri([o["cuerpo"]["dano_ventana"] for o in g]),
        "bruto_con_signo_distinto_del_efecto": sum(1 for o in g if (o["cuerpo"]["bruto"] > 0) != (o["cuerpo"]["efecto"] > 0)), "bruto_lejos_del_efecto_mas_de_10": sum(1 for o in g if abs(o["cuerpo"]["bruto"] - o["cuerpo"]["efecto"]) > 10),
        "recursos_efecto": dict(collections.Counter(o["recursos"]["efecto"] for o in g)), "kits_delta": dict(collections.Counter(o["recursos"]["kits_fin"] - o["recursos"]["kits"] for o in g)), "W_delta": tri([(o["recursos"]["W_fin"] - o["recursos"]["W"]) if (o["recursos"]["W"] is not None and o["recursos"]["W_fin"] is not None) else None for o in g]),
        "vinculo_efecto": tri([o["vinculo"]["efecto"] for o in g]), "vinculo_como": dict(collections.Counter(str(o["vinculo"]["como"]) for o in g)), "hp_hermano_delta": tri([(o["vinculo"]["hp_hermano_fin"] - o["vinculo"]["hp_hermano"]) if (o["vinculo"]["hp_hermano"] is not None and o["vinculo"]["hp_hermano_fin"] is not None) else None for o in g]),
        "importancia_F": tri([o["importancia"]["F"] for o in g]), "importancia_R": tri([o["importancia"]["R"] for o in g]), "importancia_S": tri([o["importancia"]["S"] for o in g]), "suma_importancias": tri([o["suma_importancias"] for o in g]), "intensidad": tri([o["intensidad"] for o in g]), "intensidad_en_tope": sum(1 for o in g if o["intensidad"] == 2.0)}
R["por_dentro_fuera"] = {k: {"n": sum(1 for o in V if o["dentro"] == (k == "dentro")), "cuerpo_efecto": tri([o["cuerpo"]["efecto"] for o in V if o["dentro"] == (k == "dentro")]), "cuerpo_bruto": tri([o["cuerpo"]["bruto"] for o in V if o["dentro"] == (k == "dentro")])} for k in ("dentro", "fuera")}
json.dump({"resumen": R, "usos": OUT}, open(os.path.join(AQUI, "P7_4_huella.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:6000])

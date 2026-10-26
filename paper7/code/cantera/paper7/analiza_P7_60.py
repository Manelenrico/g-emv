"""[P7-60] ¿HACE ALGO LA REGLA «LO CONTADO PESA INTENSIDAD x VINCULO»? (propuesta de Ari; banco, coste cero). Sobre los cuadernos de COMPARTE de P7-50 (P7_50_res), con la fusion por
evento de P7-55 (dedup de los vistos que llegaron tambien contados): se recalcula la creencia de cada hermana con el vinculo B FIJADO a mano en 1, 0,5 y 0,25 para los recuerdos
recibidos (contados: intensidad_emisora x B; vistos: intensidad_sin_B x B); lo vivido intacto. Tambien con el B que se registro de verdad. Para cada nivel: lo aprendido de la otra
(a - b de P7-55: a = todos deduplicados, b = solo vividos), por hermana y objeto, al dia 20 (y la media d1-20). Funciones de analiza_P7_55 (dedup, creencia), sin copiarlas.
  python3 analiza_P7_60.py -> P7_60_datos.json"""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(AQUI, "analiza_P7_55.py")).read(); ns = {"__file__": os.path.join(AQUI, "analiza_P7_55.py")}; exec(src[:src.index("\nR = {")], ns)
cuaderno, recuerdos, dedup, creencia, OBJ, NOM = ns["cuaderno"], ns["recuerdos"], ns["dedup"], ns["creencia"], ns["OBJ"], ns["NOM"]
NIVELES = (("real", None), ("B=1", 1.0), ("B=0,5", 0.5), ("B=0,25", 0.25))


def con_B(recs, B):
    if B is None: return recs
    out = []
    for r in recs:
        o = r.get("origen", "vivido")
        if o == "contado": r = dict(r, intensidad=float(r["intensidad_emisora"]) * B)
        elif o == "visto": r = dict(r, intensidad=float(r["intensidad_sin_B"]) * B)
        out.append(r)
    return out


R = {"por_hermana": {}, "B_registrado": {}}
for S in (1, 2, 3):
    for sl in (10, 11):
        k = f"s{S} a{sl}"; res = {"hermana": "valiente" if sl == 10 else "prudente"}; Bs = []
        filas = []
        for d in range(1, 21):
            c = cuaderno(S, d, "COMPARTE", sl)
            if not c: continue
            recs_d, _ = dedup(recuerdos(c)); filas.append((d, recs_d))
        Bs = [float(r["B"]) for r in filas[-1][1] if r.get("origen") in ("contado", "visto") and r.get("B") is not None] if filas else []
        R["B_registrado"][k] = {"n": len(Bs), "media": round(st.mean(Bs), 4) if Bs else None, "min": min(Bs) if Bs else None, "max": max(Bs) if Bs else None}
        for nv, B in NIVELES:
            res[nv] = {}
            for o in OBJ:
                dif = []
                for d, recs_d in filas:
                    rr = con_B(recs_d, B); a = creencia(rr, o, d + 1); b = creencia(rr, o, d + 1, lambda r: r.get("origen", "vivido") == "vivido"); dif.append((d, a, b))
                d20 = dif[-1] if dif else None
                res[nv][NOM[o]] = {"a_d20": round(d20[1], 3) if d20 and d20[1] is not None else None, "b_d20": round(d20[2], 3) if d20 and d20[2] is not None else None,
                                   "a_menos_b_d20": round((d20[1] or 0.0) - (d20[2] or 0.0), 3) if d20 else None, "a_menos_b_media_d1_20": round(st.mean((a or 0.0) - (b or 0.0) for _, a, b in dif), 3) if dif else None}
        R["por_hermana"][k] = res
json.dump(R, open(os.path.join(AQUI, "P7_60_datos.json"), "w"), ensure_ascii=False, indent=1)
for k, v in R["por_hermana"].items(): print(k, v["hermana"], {nv: {o: v[nv][o]["a_menos_b_d20"] for o in NOM.values()} for nv, _ in NIVELES}, R["B_registrado"][k])

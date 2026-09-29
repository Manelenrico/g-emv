"""[P5-6B] EL HUMO EN EL CAMPO, leido de los artefactos. Nada se afirma de los
brazos: esto es humo y precio.

Por brazo y asiento: lo que el encargo pide, ni mas ni menos.
"""
from __future__ import annotations
import collections, json, os, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "paintball"))
sys.path.insert(0, os.path.join(RAIZ, "paintball", "alma"))

ARMADA_NO = ("none", "net", None, "")
UMBRAL = 0.1


def lee(f):
    for linea in open(f, encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        try:
            yield json.loads(linea)
        except Exception:
            continue


def armado_a_la_vista(r, herm):
    for a in (r.get("ve_agentes") or []):
        if a.get("slot") == herm:
            continue
        if (a.get("hand") or "none") not in ARMADA_NO:
            return True
    return False


def analiza(f, brazo):
    recs = list(lee(f))
    k = collections.Counter(x.get("k") for x in recs)
    pc = next((x for x in recs if x.get("k") == "player_config"), None)
    arr = next((x for x in recs if x.get("k") == "arranque"), None)
    fin = next((x for x in recs if x.get("k") == "final"), None)
    slot = (pc or {}).get("slot")
    herm = (pc or {}).get("teammate_slot")
    vivos = [x for x in recs if x.get("k") == "tick" and x.get("phase") == "live"]
    out = {"brazo": brazo, "fichero": os.path.basename(f), "slot": slot,
           "registros": dict(k), "lineas": len(recs),
           "tics_vivos": len(vivos),
           "primer_tic_vivo": vivos[0]["tick"] if vivos else None,
           "ultimo_tic_vivo": vivos[-1]["tick"] if vivos else None,
           "final": ({kk: fin.get(kk) for kk in
                      ("placement", "kills", "score", "reason", "match_ticks")}
                     if fin else None),
           "interruptores": ((arr or {}).get("entorno_forma") or {}).get("efectivo"),
           }
    # ── vida, muerte, anillo, calma ──────────────────────────────────────
    if vivos:
        out["vida_tics"] = vivos[-1]["tick"] - vivos[0]["tick"] + 1
        out["hp_final"] = vivos[-1].get("hp")
        dan = [x for x in vivos if x.get("damage_taken")]
        out["tics_con_dano"] = len(dan)
        out["ultimo_dano_tic"] = dan[-1]["tick"] if dan else None
        # primer aviso del anillo
        av = next((x["tick"] for x in vivos
                   if (x.get("zona") or {}).get("warn_tick") is not None
                   and x["tick"] >= (x.get("zona") or {}).get("warn_tick", 10**9)),
                  None)
        out["primer_aviso_anillo"] = av
        # calma: literal y declarada (los criterios de P5-1 C1)
        lit = dec = 0
        rompe_lit = rompe_dec = None
        for x in vivos:
            filas = ((x.get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas") or {}
            m = {kk: (vv.get("M") if isinstance(vv, dict) else vv) or 0.0
                 for kk, vv in filas.items()}
            arm = armado_a_la_vista(x, herm)
            if not arm and all(v <= UMBRAL for v in m.values()):
                lit += 1
            elif rompe_lit is None:
                rompe_lit = (x["tick"],
                             max(m.items(), key=lambda p: p[1])[0] if m else "armado")
            fs = {kk: v for kk, v in m.items()
                  if kk.startswith("F-") or kk.startswith("S-")}
            if not arm and all(v <= UMBRAL for v in fs.values()):
                dec += 1
            elif rompe_dec is None:
                rompe_dec = (x["tick"],
                             max(fs.items(), key=lambda p: p[1])[0] if fs else "armado")
        out["calma_literal"] = lit
        out["calma_declarada"] = dec
        out["rompe_literal"] = rompe_lit
        out["rompe_declarada"] = rompe_dec
    # ── lo de las formas ─────────────────────────────────────────────────
    citas = [x for x in recs if x.get("k") == "forma_propuesta"]
    ev = [x for x in recs if x.get("k") == "forma_evaluada"]
    ac = [x for x in recs if x.get("k") == "forma_aceptada"]
    ca = [x for x in recs if x.get("k") == "forma_caida"]
    cf = [x for x in recs if x.get("k") == "confianza"]
    pa = [x for x in recs if x.get("k") == "parte"]
    hi = [x for x in recs if x.get("k") == "hilo_forma"]
    tt = [x for x in recs if x.get("k") == "tiempo_tic"]
    fr = [x for x in recs if x.get("k") in ("forma_freno", "forma_freno_ciego")]
    gana = [x for x in recs if x.get("k") == "forma_gana"]
    emp = [x for x in recs if x.get("k") == "forma_empate"]
    # OJO: `forma_propuesta` la escriben DOS sitios: el consejero (con `ok`,
    # `ms` y `traduccion`) y el brazo T (con `origen: "azar"`). Se separan.
    del_azar = [x for x in citas if x.get("origen") == "azar"]
    del_cons = [x for x in citas if x.get("origen") != "azar"]
    out["formas"] = {
        "propuestas_del_azar": len(del_azar),
        "citas_al_consejero": len(del_cons),
        "citas_ok": sum(1 for x in del_cons if x.get("ok")),
        "citas_con_formas": sum(1 for x in del_cons
                                if (x.get("traduccion") or {}).get("n_formas")),
        "citas_fallidas": sum(1 for x in del_cons if not x.get("ok")),
        "lat_mediana_ms": (round(st.median([x["ms"] for x in del_cons
                                            if x.get("ms")]), 1)
                           if any(x.get("ms") for x in del_cons) else None),
        "parsean": sum(1 for x in del_cons
                       if (x.get("traduccion") or {}).get("parsea")),
        "callar": sum(1 for x in del_cons
                      if (x.get("traduccion") or {}).get("callar")),
        "evaluadas": len(ev),
        "veredictos": dict(collections.Counter(x.get("veredicto") for x in ev)),
        "aceptadas": len(ac),
        "caidas": len(ca),
        "motivos_caida": dict(collections.Counter(
            (x.get("motivo") or "")[:46] for x in ca)),
        "gana_el_tic": len(gana),
        "por_la_ventaja": sum(1 for x in gana if x.get("por_la_ventaja")),
        "empates_al_cuerpo": len(emp),
        "partes": len(pa),
        "frenos": [x.get("k") for x in fr],
    }
    if cf:
        cs = [x.get("C") for x in cf if x.get("C") is not None]
        out["confianza"] = {
            "cambios": len(cf), "C_final": cs[-1] if cs else None,
            "C_min": min(cs) if cs else None, "C_max": max(cs) if cs else None,
            "aciertos": sum(1 for x in cf if x.get("veredicto") == "acierto"),
            "fallos": sum(1 for x in cf if x.get("veredicto") == "fallo"),
            "callo_al_consejero": sum(1 for x in cf if x.get("suceso")),
        }
    out["hilo"] = {
        "dichos": sum(1 for x in hi if x.get("estado") == "dicho"),
        "oidos": sum(1 for x in hi if x.get("estado") == "oido"),
        "con_forma": sum(1 for x in hi
                         if x.get("estado") == "dicho" and x.get("con_forma")),
        "no_cabe": sum(1 for x in hi if x.get("estado") == "no cabe"),
        "textos": [x.get("texto") for x in hi
                   if x.get("estado") == "dicho"][:3],
    }
    if tt:
        ms = sorted(x["ms"] for x in tt if x.get("ms") is not None)
        out["tiempo_tic"] = {
            "n": len(ms), "mediana": round(ms[len(ms) // 2], 3),
            "p95": round(ms[int(len(ms) * 0.95)], 3), "max": round(ms[-1], 3),
            "en_hilo": sum(1 for x in tt if x.get("en_hilo"))}
    return out


def main():
    todo = {}
    for b in ("A","F","F2","T"):
        d = os.path.join(RAIZ, "paintball", "runs", "P56B_" + b)
        if not os.path.isdir(d):
            print(b, "sin carpeta"); continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".art.log"):
                continue
            r = analiza(os.path.join(d, f), b)
            todo[f"{b}/{r['slot']}"] = r
            print(f"=== {b} · asiento {r['slot']} · {r['lineas']:,} lineas ===")
            print(f"  tics vivos {r['tics_vivos']:,} "
                  f"({r.get('primer_tic_vivo')}..{r.get('ultimo_tic_vivo')}) "
                  f"· hp final {r.get('hp_final')} · final {r.get('final')}")
            print(f"  formas: {json.dumps(r['formas'], ensure_ascii=False)}")
            if r.get("confianza"):
                print(f"  confianza: {json.dumps(r['confianza'], ensure_ascii=False)}")
            print(f"  hilo: {json.dumps(r['hilo'], ensure_ascii=False)}")
            if r.get("tiempo_tic"):
                print(f"  tiempo_tic: {json.dumps(r['tiempo_tic'], ensure_ascii=False)}")
            print(f"  calma literal {r.get('calma_literal')} · declarada "
                  f"{r.get('calma_declarada')} · rompe {r.get('rompe_literal')}")
    json.dump(todo, open(os.path.join(AQUI, "P56B_humo_campo.json"), "w"),
              ensure_ascii=False, indent=1)
    print("\nguardado en P56B_humo_campo.json")


if __name__ == "__main__":
    main()

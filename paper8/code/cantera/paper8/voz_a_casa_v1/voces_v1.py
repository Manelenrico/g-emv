"""[P8] Prompt 143: lo que pasó con cada voz de una partida de VC1 (lee <partida>/voz_vc1.json y balance.jsonl.gz; no juega nada).
LAS REGLAS (de este recuento):
  - LA OYE: la hermana la oye siempre que suena (la voz solo suena si está viva, despierta y al alcance); «decidió oyéndola» si tomó alguna decisión
    mientras duraba (vc_oye con esa voz);
  - SE DEVUELVE: la que la oyó da su propia voz mientras dura la que oyó (en los turnos t+1 a t+44; su voz apunta «responde_a»);
  - LAS DOS EN CASA: en algún turno de t+1 a t+44, las dos dentro de su casa a la vez (sitio «C» de balance.jsonl.gz: dentro, sin la puerta);
  - CAMBIÓ LO ELEGIDO: una decisión oyendo en que lo de menor malestar sin haberla oído era otra cosa (cuerpo_vc1).
   python3 voz_a_casa_v1/voces_v1.py <carpeta de una partida>  -> el resumen por pantalla"""
import gzip, json, os, sys
DURA = 44

def voces(d):
    """las voces de la partida, cada una con lo que pasó"""
    V = json.load(open(os.path.join(d, "voz_vc1.json"))); vs = [v for x in V.values() for v in x["voces"]]; oye = [o for x in V.values() for o in x["oye"]]
    if not vs: return [], oye, V
    t_max = max(v["t"] for v in vs) + DURA + 1; C = {}
    for l in gzip.open(os.path.join(d, "balance.jsonl.gz"), "rt", encoding="utf-8"):
        b = json.loads(l)
        if b["t"] > t_max: break
        C[b["t"]] = {a: c[5] == "C" for a, c in b["c"].items()}
    resp = {v["responde_a"]: v for v in vs if v.get("responde_a")}; dec = {}
    for o in oye: dec.setdefault(o["voz"], []).append(o)
    for v in vs:
        t = v["t"]; r = resp.get(v["id"])
        v["devuelta"] = r is not None and r["de"] == v["a"] and t < r["t"] <= t + DURA; v["t_devuelta"] = r["t"] if v["devuelta"] else None
        casa = [u for u in range(t + 1, t + DURA + 1) if (C.get(u) or {}).get(v["de"]) and (C.get(u) or {}).get(v["a"])]
        v["dos_en_casa"] = bool(casa); v["t_dos_en_casa"] = casa[0] if casa else None
        v["decisiones_oyendo"] = len(dec.get(v["id"], [])); v["cambios"] = sum(o["cambio"] for o in dec.get(v["id"], []))
    return vs, oye, V


if __name__ == "__main__":
    d = sys.argv[1]; vs, oye, V = voces(d)
    out = {"voces": len(vs), "ya_era_ir_casa": sum(v["ya_era"] for v in vs), "con_decisiones_oyendo": sum(v["decisiones_oyendo"] > 0 for v in vs),
           "devueltas": sum(v["devuelta"] for v in vs), "dos_en_casa": sum(v["dos_en_casa"] for v in vs), "devueltas_y_dos_en_casa": sum(v["devuelta"] and v["dos_en_casa"] for v in vs),
           "decisiones_oyendo": len(oye), "cambio_lo_elegido": sum(o["cambio"] for o in oye),
           "pudo_sonar": sum(x["cuenta"]["pudo_sonar"] for x in V.values()), "decisiones_tarde": sum(x["cuenta"]["decisiones_tarde"] for x in V.values())}
    print(json.dumps(out, indent=1))

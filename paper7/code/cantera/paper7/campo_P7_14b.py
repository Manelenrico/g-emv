"""[P7-14b] = campo_P7_14.py con los nombres de P7-14b (estado, semillas, cuadernos, diarios en paintball/runs/P714b_*). Nada mas cambia.
[cabecera de P7-14] = campo_P7_10.py con los nombres de P7-14 (diarios en paintball/runs/P714b_*; brazos ESPERANZA, BORRADO, APRENDE, TECHO). Mismas definiciones.
[cabecera de P7-10] LECTURA DEL CAMPO (campo_P7_9.py con nombres P7_14b; ademas, por uso: la vida antes, lo que le faltaba, lo ganado, firme o "al menos", la creencia y la cura imaginada en ese momento (P7_uso/P7_huella, solo APRENDE y BORRADO); y los regalos que recoge el hermano): de cada diario de paintball/runs/P714b_s<S>_d<D>_<BRAZO>_<semilla>/ (fuera de git), por serie, dia, brazo y
criatura, con las mismas reglas para los cuatro brazos (todo se lee del diario crudo; los registros P7_* solo se usan para el cuaderno):
  - botiquines COGIDOS (sube el n de botiquines a bordo tras `pickup`): por curiosidad (ultimo `ir_*` elegido en los 10 tics anteriores fue
    `ir_curioso`), por ganas (`ir_objeto`/`ir_botin`), de paso (ninguno); REGALADOS (`soltar_first_aid` elegido y ejecutado: baja el n);
  - USADOS: ventana del canal `channeling first_aid` (desde que aparece hasta que desaparece): situacion (dentro/fuera del circulo por `zona`),
    vida al empezar, gastado (baja el n) o interrumpido, vida curada = hp al cerrar - hp al abrir (cruda, sin descontar dano);
  - HACE SITIO (P7_sitio) y OSCILACIONES (dos hacer-sitio seguidos en <= 5 tics que se deshacen: A por B, luego B por A);
  - en APRENDE y BORRADO, el cuaderno de fin (P7_cuaderno): recuerdos firmes y "al menos", creencia por dominio y situacion, ignorancia; y si
    el de arranque se leyo (APRENDE);
  - vida al morir (hp del ultimo tic), causa (fuentes del dano en los ultimos 30 tics: anillo / rival / veneno / otra), puesto, motivo.
-> P7_14b_campo.json. `--freno`: comprueba (a) (b) (c) de la mesa sobre APRENDE serie 1 dias 1-3."""
import collections, glob, json, math, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
ESTADO = json.load(open(os.path.join(AQUI, "P7_14b_estado.json"))) if os.path.exists(os.path.join(AQUI, "P7_14b_estado.json")) else {"peticiones": []}
def lee_vida(f, brazo):
    T = []; cuad = {}; sitios = []; final = None; usos_P7 = []; huellas = []
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        k = r.get("k")
        if k == "tick" and r.get("phase") == "live": T.append(r)
        elif k == "P7_cuaderno": cuad[r.get("momento")] = r
        elif k == "P7_sitio": sitios.append(r)
        elif k == "P7_uso": usos_P7.append(r)
        elif k == "P7_huella": huellas.append(r)
        elif k == "final": final = r
    if not T: return {"sin_tics": True}
    kits = lambda r: sum(int((s or {}).get("n") or 0) for s in (r.get("pack") or []) if s and s.get("id") == "first_aid")
    canal = lambda r: any(e.get("id") == "channeling" and e.get("item") == "first_aid" for e in (r.get("effects") or []))
    def dentro(r):
        z = r.get("zona") or {}; c = z.get("center"); rad = z.get("radius")
        return (math.dist(r["pos"], c) <= rad) if (c is not None and rad is not None) else None
    coge = []; regala = []; usos = []; ult_ir = None; v = None; prev = None
    for r in T:
        t = r["tick"]; el = str((r.get("RADIOGRAFIA") or {}).get("elegido") or ""); k_ = kits(r)
        if el in ("ir_curioso", "ir_objeto", "ir_botin"): ult_ir = (t, el)
        if prev is not None:
            kp = kits(prev); do = (prev.get("intencion") or {}).get("do")
            if k_ > kp and do == "pickup":
                como = "de paso"
                if ult_ir and t - ult_ir[0] <= 10: como = "por curiosidad" if ult_ir[1] == "ir_curioso" else "por ganas"
                coge.append({"t": t, "como": como, "hp": r.get("hp"), "regalado": False})
            if k_ < kp and do == "drop" and str((prev.get("RADIOGRAFIA") or {}).get("elegido") or "").startswith("soltar_first_aid"):
                regala.append({"t": t, "hp": r.get("hp"), "pos": list(prev["pos"])})
                if coge and t - coge[-1]["t"] <= 10: coge[-1]["regalado"] = True
        if v is not None and el.startswith("soltar_first_aid"): v["regalado"] = True
        if v is None and canal(r):
            v = {"t0": t, "hp0": float(r.get("hp") or 0), "kits0": k_, "situacion": ("dentro" if dentro(r) else "fuera") if dentro(r) is not None else "?", "regalado": el.startswith("soltar_first_aid")}
        elif v is not None and not canal(r):
            corte = [(str(d.get("source") or ""), float(d.get("amount") or 0)) for d in (r.get("damage_taken") or [])]
            hpm = max(float(x.get("hp") or 0) for x in T) if False else 100.0
            usos.append({**v, "t_fin": t, "hp_fin": float(r.get("hp") or 0), "curada": float(r.get("hp") or 0) - v["hp0"], "faltaba": hpm - v["hp0"], "gastado": (k_ < v["kits0"] and not v.get("regalado")), "anulado_por_regalo": bool(v.get("regalado")), "dano_al_cerrar": corte, "cortado_por_dano": (k_ >= v["kits0"] and bool(corte))}); v = None
        prev = r
    # la creencia y la imaginacion en el momento de cada uso (P7_uso se escribe en el tic de apertura del canal) y la huella (firme / al menos)
    PU = {u["tick"]: u for u in usos_P7}; PH = {h["t0"]: h for h in huellas}
    for u in usos:
        pu = PU.get(u["t0"]) or {}; ph = PH.get(u["t0"]) or {}
        u["creencia_en_el_momento"] = pu.get("creencia_cuerpo"); u["cura_imaginada"] = pu.get("heal_imaginado"); u["ignorancia_en_el_momento"] = pu.get("ignorancia")
        u["apuntado"] = ph.get("apuntado"); u["al_menos"] = ph.get("al_menos"); u["firme"] = (bool(ph.get("apuntado")) and not ph.get("al_menos")) if ph else None
    # oscilaciones de hacer sitio
    osc = 0
    for a, b in zip(sitios, sitios[1:]):
        ea, eb = a["elegido"].replace("hacer_sitio_", "").split("_por_"), b["elegido"].replace("hacer_sitio_", "").split("_por_")
        if b["tick"] - a["tick"] <= 5 and ea[0] == eb[1] and ea[1] == eb[0]: osc += 1
    ult = T[-1]; fuentes = collections.Counter(); ultimo_dano = None
    clas = lambda s_: ("anillo" if s_ == "zone" else "rival" if s_.startswith("P") else "veneno" if "poison" in s_ else "otra")
    for r in T:
        for d in r.get("damage_taken") or []:
            if r["tick"] >= ult["tick"] - 30: fuentes[clas(str(d.get("source") or ""))] += float(d.get("amount") or 0)
            ultimo_dano = (r["tick"], clas(str(d.get("source") or "")))
    # causa = la fuente que mas dano hizo en los ultimos 30 tics; si no hubo (el golpe final no queda en el diario), la del ultimo dano de la vida
    causa = ((fuentes.most_common(1)[0][0] if fuentes else (ultimo_dano[1] if ultimo_dano else "sin dano registrado")) if (final or {}).get("reason") == "eliminated" else "sobrevive")
    c_fin = (cuad.get("fin") or {}).get("contenido") or {}; c_ini = cuad.get("arranque") or {}
    recs = [x for o in (c_fin.get("objetos") or {}).values() for s_ in (o.get("situaciones") or {}).values() for x in s_]
    return {"ticks_vivos": len(T), "ultimo_tick": ult["tick"], "hp_final": ult.get("hp"), "motivo": (final or {}).get("reason"), "puesto": (final or {}).get("placement"), "causa_muerte": causa, "ultimo_dano": ultimo_dano, "dano_ultimos_30": {k: round(x, 1) for k, x in fuentes.items()},
            "coge": coge, "coge_n": len(coge), "coge_por": dict(collections.Counter(c["como"] for c in coge)), "regala_n": len(regala), "regala": regala[:40], "coge_regaladas": sum(1 for c in coge if c["regalado"]),
            "usos": usos, "usos_gastados": sum(1 for u in usos if u["gastado"]), "usos_interrumpidos": sum(1 for u in usos if not u["gastado"]), "usos_cortados_por_dano": sum(1 for u in usos if u.get("cortado_por_dano")), "usos_P7": [{"t": u["tick"], "hp": u["hp"], "situacion": u["situacion"], "ignorancia": u.get("ignorancia"), "heal_imaginado": u.get("heal_imaginado")} for u in usos_P7],
            "hace_sitio_n": len(sitios), "oscilaciones": osc,
            "cuaderno": ({"leido": c_ini.get("leido"), "dia_arranque": c_ini.get("dia"), "dia_fin": c_fin.get("dia"), "recuerdos": len(recs), "firmes": sum(1 for x in recs if not x.get("al_menos")), "al_menos": sum(1 for x in recs if x.get("al_menos")),
                          "creencias": c_fin.get("creencias"), "ignorancia": ((c_fin.get("creencias") or {}).get("first_aid") or {}).get("ignorancia"), "recuerdos_lista": [{"dia": x["dia"], "tick": x["tick"], "cuerpo": x["efecto"]["cuerpo"], "al_menos": x.get("al_menos")} for x in recs]} if brazo in ("APRENDE", "BORRADO") else None)}
def recogidas_por_el_hermano(f_hermano):
    """(tick, pos) de cada pickup del hermano que sube su n de botiquines."""
    out = []; prev = None
    for line in open(f_hermano):
        if '"k":"tick"' not in line[:12]: continue
        r = json.loads(line)
        if r.get("phase") != "live": continue
        k_ = sum(int((s or {}).get("n") or 0) for s in (r.get("pack") or []) if s and s.get("id") == "first_aid")
        if prev is not None and k_ > prev[0] and prev[1] == "pickup": out.append((r["tick"], tuple(prev[2])))
        prev = (k_, (r.get("intencion") or {}).get("do"), r.get("pos"))
    return out
def lee_todo():
    OUT = {}
    for carp in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P714b_s*_d*_*_*"))):
        b = os.path.basename(carp); _, s_, d_, brazo, sem = b.split("_"); serie = int(s_[1:]); dia = int(d_[1:])
        fs = {slot: glob.glob(os.path.join(carp, f"*policy_agent_{slot}.art.log")) for slot in (10, 11)}
        for slot in (10, 11):
            if not fs[slot]: continue
            v = {"serie": serie, "dia": dia, "brazo": brazo, "slot": slot, "semilla": int(sem), **lee_vida(fs[slot][0], brazo)}
            herm = fs[21 - slot]
            if herm and not v.get("sin_tics") and v["regala"]:
                rec = recogidas_por_el_hermano(herm[0]); n_rec = 0
                for g in v["regala"]:
                    if any(t > g["t"] and t - g["t"] <= 300 and p == tuple(g.get("pos") or ()) for t, p in rec): n_rec += 1; g["recogido_por_el_hermano"] = True
                v["regalos_recogidos_por_el_hermano"] = n_rec
            OUT[f"s{serie}_d{dia}_{brazo}_{slot}"] = v
    return OUT
def freno(OUT):
    R = {"a_cuaderno_viaja": {}, "b_regalos_con_no_se": {}, "c_recuerdo_firme": {}}
    for dia in (1, 2, 3):
        for slot in (10, 11):
            v = OUT.get(f"s1_d{dia}_APRENDE_{slot}")
            if not v or v.get("sin_tics"): R["a_cuaderno_viaja"][f"d{dia}_{slot}"] = "SIN DIARIO"; continue
            c = v["cuaderno"]; R["a_cuaderno_viaja"][f"d{dia}_{slot}"] = {"leido": c["leido"], "dia_arranque": c["dia_arranque"], "dia_fin": c["dia_fin"], "esperado_leido": dia > 1}
            # (b): regalo con "no se" = soltar_first_aid ejecutado antes de la primera huella apuntada de la vida y sin creencia leida al arrancar
            cre_ini = ((((v.get("cuaderno") or {}).get("creencias") or {}) or {}).get("first_aid") or {})   # fin; la de arranque se lee de P7_cuaderno arranque:
            R["b_regalos_con_no_se"][f"d{dia}_{slot}"] = {"regalos": v["regala_n"], "primeros": [x["t"] for x in v["regala"][:5]]}
            R["c_recuerdo_firme"][f"d{dia}_{slot}"] = c["firmes"]
    R["a_pasa"] = all(isinstance(x, dict) and (x["leido"] == x["esperado_leido"]) for x in R["a_cuaderno_viaja"].values())
    R["c_creencia_sube_ignorancia_baja"] = {}
    for slot in (10, 11):
        v1, v3 = OUT.get(f"s1_d1_APRENDE_{slot}"), OUT.get(f"s1_d3_APRENDE_{slot}")
        if not v1 or not v3 or v1.get("sin_tics") or v3.get("sin_tics"): continue
        c1, c3 = v1["cuaderno"], v3["cuaderno"]
        cre = lambda c: max([x["cuerpo"] for s_ in ((c.get("creencias") or {}).get("first_aid") or {}).values() if isinstance(s_, dict) and "cuerpo" in s_ for x in [s_]] or [None]) if ((c.get("creencias") or {}).get("first_aid")) else None
        a, b = cre(c1), cre(c3); ia, ib = c1.get("ignorancia"), c3.get("ignorancia")
        R["c_creencia_sube_ignorancia_baja"][slot] = {"creencia_d1": a, "creencia_d3": b, "ignorancia_d1": ia, "ignorancia_d3": ib, "pasa": ((b or 0) > (a or 0)) and ((ib if ib is not None else 1.0) < (ia if ia is not None else 1.0))}
    R["c_pasa"] = any(x["pasa"] for x in R["c_creencia_sube_ignorancia_baja"].values())
    return R
if __name__ == "__main__":
    OUT = lee_todo(); json.dump(OUT, open(os.path.join(AQUI, "P7_14b_campo.json"), "w"), ensure_ascii=False, indent=1)
    for k, v in OUT.items():
        if v.get("sin_tics"): print(k, "sin tics"); continue
        c = v["cuaderno"] or {}
        print(f"{k}: vivo {v['ticks_vivos']} hp_fin {v['hp_final']} {v['motivo']} puesto {v['puesto']} causa {v['causa_muerte']} · coge {v['coge_n']} {v['coge_por']} regala {v['regala_n']} · usa {v['usos_gastados']} (interr {v['usos_interrumpidos']}, cortados por dano {v['usos_cortados_por_dano']}) {[(u['t0'], u['situacion'], u['hp0'], round(u['curada'])) for u in v['usos'] if u['gastado']][:5]} · sitio {v['hace_sitio_n']} osc {v['oscilaciones']}" + (f" · cuaderno leido {c.get('leido')} fin: {c.get('recuerdos')} rec ({c.get('firmes')} firmes, {c.get('al_menos')} al menos) ign {c.get('ignorancia')}" if c else ""))
    if "--freno" in sys.argv: print(json.dumps(freno(OUT), ensure_ascii=False, indent=1))

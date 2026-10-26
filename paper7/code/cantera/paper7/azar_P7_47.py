"""[P7-47] SIN EMOCION, EL RIVAL ARREGLADO (SELLO_P7_47.md) = azar_P7_41 con dos cambios y nada mas (la pieza de P7-41 no se toca; esta se usa con GEMV_P7_47_AZAR=1 en vez de
GEMV_P7_41_AZAR=1):
  (a) la forzada de ir se cierra con la llegada: en la casilla del destino, si el cuerpo ofrece `hacer_sitio_*` por el objeto forzado se elige eso; si no hay `coger` (la regla
      congelada del seis lo esconde cuando la prevision dice que la mochila no cambia, o el cuerpo lo construye con otro objeto de la casilla) la pieza lo pone para el objeto
      forzado; si a los 24 tics en la casilla no lo ha cogido, la forzada se cierra como "no cabe" (fin nuevo) en vez de esperar 240 tics;
  (b) la moneda de "usar" solo se tira cuando el cuerpo ofrece `usar_*` (hp < maximo, la regla del cuerpo congelado, decisor_zs paso 6); la de "ir" como antes.
Registros: los mismos (`P7_41_azar`) mas `fin` = "no cabe" y el campo `via` en la cogida (recoger / hacer_sitio / coger_puesto).
--- cabecera de azar_P7_41 ---
[P7-41] SIN EMOCION: el brazo que explora al azar (diseno de Manel; definiciones propuestas en informe_P7_41.md, pendientes de su visto bueno). Mismo cuerpo, misma
percepcion, mismos recuerdos y misma regla de creencia (importancia como B1: filtro de P7-39, sin contrafactual). Lo unico que cambia:
  - sin curiosidad: GEMV_P7_NOVEDAD=0 (no hay R-CURIOSIDAD ni ir_curioso ni llamada de clase), y sin las piezas de P7-40 (ni esperanza de clase ni apuntes);
  - VETO: el cuerpo no coge ni usa por si solo nada de una clase DESCONOCIDA (sin recuerdos en el cuaderno): los candidatos `coger` de esa cosa y `usar_*` de un consumible
    desconocido salen de la lista salvo en una prueba forzada (si no, con eps = 0 cogeria redes por empate, como TECHO en P7-36);
  - MOMENTO (P7-42, mesa): en CADA tic de decision en que hay una cosa de las cuatro a su alcance (a la vista y sin llevarla, conocida o desconocida; o un consumible
    en el zurron), se tira UNA moneda PURA con probabilidad eps (sin miedo), todos los dias. Si sale, se fuerza la prueba de una de las cosas al alcance, elegida al
    azar. eps se calibra en local antes del sello (P7-42) para que el total de pruebas en 20 dias quede a +-20 % del de APRENDE. [P7-41 tenia una moneda por
    oportunidad nueva, eps x miedo y solo lo desconocido: GEMV_P7_41_MODO=oportunidad lo conserva para el banco.]
  - PRUEBA FORZADA: si la moneda dice si, durante hasta 240 tics se fuerza ir a la cosa (candidato `ir_azar`, tipo ir con recoger, que gana el tic) y cogerla al llegar
    (`coger` forzado); un consumible desconocido en el zurron se usa forzado en el primer tic en que `usar_*` es candidato. La prueba y su recuerdo son los de P7-33.
Registros: `P7_41_azar` (oportunidad / forzada / fin, con eps efectivo). Mandos: GEMV_P7_41_AZAR=1, GEMV_P7_EPS (0 | 0.05 | 0.2), GEMV_P7_40_MIEDO (valiente | prudente),
GEMV_P7_41_SEMILLA (semilla del azar; por defecto la del asiento + el tic de arranque)."""
import math, os, random
import descubre_P7 as X, nace_P7_23 as N, nace_P7_33 as N33
from alma import decisor_zs as D
ON = os.environ.get("GEMV_P7_47_AZAR", "0") == "1"; EN_CASILLA = 24; EPS = float(os.environ.get("GEMV_P7_EPS", "0") or 0.0); MIEDO = os.environ.get("GEMV_P7_40_MIEDO", "prudente"); MODO = os.environ.get("GEMV_P7_41_MODO", "momento")
DURACION = 240; OLVIDO_VISTA = 48
E = {"registra": None, "rng": None, "vistas": {}, "forzada": None, "oportunidades": 0, "forzadas": 0, "vetos": 0, "elegidas_desconocidas": 0, "pruebas_forzadas_cerradas": 0, "momentos": 0, "monedas_si": 0, "usos_propios": 0}


def miedo(cautela): return cautela if MIEDO == "prudente" else (1.0 + cautela) / 2.0
def conocida(c, o): return c is not None and any(not r.get("corte") for r in c.recuerdos_de(o))
def clase_de(mundo, iid):
    for o in N33.cuatro(mundo):
        if iid == o: return o
    return None


def aplica(clase, registra=None):
    if not ON: return {"P7_41_azar": False}
    E["registra"] = registra
    _oc = D.candidatos
    def _cands(obs, mundo, mem, tick, bloqueos=None):
        out = _oc(obs, mundo, mem, tick, bloqueos); c = N.cuaderno(); f = E["forzada"]; you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0))
        res = []
        for n_, r_ in out:
            if n_ == "coger":
                iid = (r_.get("item") or {}).get("id"); o = clase_de(mundo, iid)
                if o is not None and not conocida(c, o) and not (f and f["objeto"] == o): E["vetos"] += 1; continue
                E["coger_item"] = (tick, iid)
            if n_.startswith("usar_"):
                o = X.kit(mundo) if n_ == "usar_botiquin" else (N.racion(mundo) if n_ == "usar_racion" else None)
                if o is not None and not conocida(c, o) and not (f and f["objeto"] == o and f["tipo"] == "usar"): E["vetos"] += 1; continue
            res.append((n_, r_))
        if f and f["tipo"] == "ir" and tuple(f["destino"]) == pos:
            hs = [n_ for n_, _ in res if n_.startswith("hacer_sitio") and n_.endswith("_por_" + str(f["objeto"]))]
            f["hacer_sitio"] = hs[0] if hs else None
            if not hs and not any(n_ == "coger" for n_, _ in res):
                it = next((it for it in ((obs.get("visible") or {}).get("items") or []) if it.get("id") == f["objeto"] and tuple(it.get("pos") or ()) == pos), None)
                if it is not None: res.append(("coger", {"tipo": "coger", "item": it})); f["coger_puesto"] = True; E["coger_puestos"] = E.get("coger_puestos", 0) + 1
        if f and f["tipo"] == "ir" and tuple(f["destino"]) != pos and not any(n_ == "ir_azar" for n_, _ in res):
            cuerpos = frozenset(tuple(a.get("pos") or ()) for a in ((obs.get("visible") or {}).get("agents") or []) if a.get("pos"))
            res.append(("ir_azar", {"tipo": "ir", "destino": tuple(f["destino"]), "cuerpos": cuerpos, "recoger": (f["objeto"], 1)}))
        return res
    D.candidatos = _cands
    _os = D.select_tiebreak
    def _sel(action_names, preds, terminal, meta, *a, **kw):
        f = E["forzada"]
        if f:
            quiero = ("usar_botiquin" if f["objeto"] == X.kit(E["mundo"]) else "usar_racion") if f["tipo"] == "usar" else ((f.get("hacer_sitio") or "coger") if f.get("aqui") else "ir_azar")
            if quiero in action_names: return quiero
            if f.get("aqui") and "coger" in action_names: return "coger"
        return _os(action_names, preds, terminal, meta, *a, **kw)
    D.select_tiebreak = _sel
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        mundo = self.mundo; E["mundo"] = mundo; c = N.cuaderno(); vis = {}; pos = None
        if mundo is not None and getattr(self, "phase", None) == "live" and c is not None:
            if E["rng"] is None: E["rng"] = random.Random(int(os.environ.get("GEMV_P7_41_SEMILLA") or (1000 * int(getattr(mundo, "slot", 0) or 0) + int(self.tick))))
            you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); tick = self.tick; caut = N.cautela_de(obs, mundo, tick); p = EPS * miedo(caut)
            vis = {(it.get("id"), tuple(it.get("pos"))): it for it in ((obs.get("visible") or {}).get("items") or []) if it.get("pos") and clase_de(mundo, it.get("id")) is not None}
            # la forzada en curso: llega, caduca o se cumple
            f = E["forzada"]
            if f:
                f["aqui"] = (f["tipo"] == "ir" and tuple(f["destino"]) == pos)
                if f["aqui"] and f.get("t_llega") is None: f["t_llega"] = tick
                lleva = (N33.tiene(you, mundo, f["objeto"]) >= 1 if f["objeto"] in N33.gear(mundo) else N.unidades_de(you, mundo, f["objeto"]) >= 1)
                fin = None
                if f["tipo"] == "ir" and lleva: fin = "cogida"
                elif f["tipo"] == "usar" and (N.unidades_de(you, mundo, f["objeto"]) < f.get("n0", 1)): fin = "usada"
                elif f["tipo"] == "ir" and f.get("t_llega") is not None and tick - f["t_llega"] >= EN_CASILLA: fin = "no cabe"
                elif tick - f["t0"] >= DURACION: fin = "caduca"
                if fin:
                    E["forzada"] = None; E["pruebas_forzadas_cerradas"] += 1
                    if E["registra"]: E["registra"]({"k": "P7_41_azar", "momento": "fin", "tick": tick, "objeto": f["objeto"], "tipo": f["tipo"], "fin": fin, "duracion": tick - f["t0"], "via": ("hacer_sitio" if f.get("hacer_sitio") else "coger_puesto" if f.get("coger_puesto") else "recoger") if fin == "cogida" else None, "en_casilla": (tick - f["t_llega"]) if f.get("t_llega") is not None else None})
            if MODO == "momento":
                # [P7-42] el momento: hay una cosa de las cuatro al alcance (a la vista sin llevarla, conocida o no; o un consumible en el zurron)
                al_alcance = []
                for (iid, q), it in vis.items():
                    o = clase_de(mundo, iid)
                    if q == pos: continue
                    lleva = (N33.tiene(you, mundo, o) >= 1 if o in N33.gear(mundo) else N.unidades_de(you, mundo, o) >= 1)
                    if not lleva: al_alcance.append(("ir", o, q))
                hp = float(you.get("hp") or 0.0); mem_ = getattr(self, "mem", None); hp_max = (getattr(mem_, "hp_max", None) or hp or 1.0); ofrece_usar = hp < hp_max      # la regla del cuerpo (decisor_zs.py:398, :485)
                for o in N.consumibles(mundo):
                    if N.unidades_de(you, mundo, o) >= 1 and ofrece_usar: al_alcance.append(("usar", o, None))
                if al_alcance:
                    E["momentos"] += 1; moneda = E["rng"].random() < EPS
                    if moneda:
                        E["monedas_si"] += 1
                        if E["forzada"] is None:
                            tipo, o, dest = E["rng"].choice(al_alcance); E["forzada"] = {"tipo": tipo, "objeto": o, "destino": dest, "t0": tick, "aqui": False, "n0": N.unidades_de(you, mundo, o)}; E["forzadas"] += 1
                            if E["registra"]: E["registra"]({"k": "P7_41_azar", "momento": "forzada", "tick": tick, "objeto": o, "tipo": tipo, "destino": (list(dest) if dest else None), "conocida": conocida(c, o), "al_alcance": len(al_alcance)})
            else:
                # [P7-41] oportunidades nuevas: a la vista (sin llevarla) o en el zurron (consumible desconocido); una moneda eps x miedo por oportunidad
                nuevas = []
                for (iid, q), it in vis.items():
                    o = clase_de(mundo, iid)
                    if conocida(c, o) or q == pos: continue
                    lleva = (N33.tiene(you, mundo, o) >= 1 if o in N33.gear(mundo) else N.unidades_de(you, mundo, o) >= 1)
                    if lleva: continue
                    k = ("ir", o, q); ult = E["vistas"].get(k)
                    if ult is None or tick - ult > OLVIDO_VISTA: nuevas.append((k, q))
                    E["vistas"][k] = tick
                for o in N.consumibles(mundo):
                    if not conocida(c, o) and N.unidades_de(you, mundo, o) >= 1:
                        k = ("usar", o, None); ult = E["vistas"].get(k)
                        if ult is None or tick - ult > OLVIDO_VISTA: nuevas.append((k, None))
                        E["vistas"][k] = tick
                for (tipo, o, q), dest in nuevas:
                    E["oportunidades"] += 1; moneda = E["rng"].random() < p
                    if E["registra"]: E["registra"]({"k": "P7_41_azar", "momento": "oportunidad", "tick": tick, "objeto": o, "tipo": tipo, "eps": EPS, "miedo": round(miedo(caut), 3), "p": round(p, 4), "moneda": moneda, "ya_forzada": E["forzada"] is not None})
                    if moneda and E["forzada"] is None:
                        E["forzada"] = {"tipo": tipo, "objeto": o, "destino": dest, "t0": tick, "aqui": False}; E["forzadas"] += 1
                        if E["registra"]: E["registra"]({"k": "P7_41_azar", "momento": "forzada", "tick": tick, "objeto": o, "tipo": tipo, "destino": (list(dest) if dest else None)})
        accion, radio = _d(self, obs)
        if radio is not None and c is not None and mundo is not None and getattr(self, "phase", None) == "live":
            el = str(radio.get("elegido") or "")
            if el in ("usar_botiquin", "usar_racion") and E["forzada"] is None:
                E["usos_propios"] += 1; E.setdefault("usos_ticks", []).append((self.tick, el))        # (en lazo abierto la intencion de usar puede repetirse: el banco las agrupa a 240 tics)
            if el in ("coger", "usar_botiquin", "usar_racion") and E["forzada"] is None:
                o = (X.kit(mundo) if el == "usar_botiquin" else N.racion(mundo) if el == "usar_racion" else None)
                if el == "coger":
                    ci = E.get("coger_item"); o = clase_de(mundo, ci[1]) if (ci and ci[0] == self.tick) else None
                if o is not None and not conocida(c, o):
                    E["elegidas_desconocidas"] += 1
                    if E["registra"]: E["registra"]({"k": "P7_41_azar", "momento": "elegida_desconocida", "tick": self.tick, "elegido": el, "objeto": o, "candidatos": sorted(radio.get("candidatos") or {})[:12]})
        return accion, radio
    clase.decidir = decidir
    return {"P7_41_azar": True, "eps": EPS, "miedo": MIEDO}

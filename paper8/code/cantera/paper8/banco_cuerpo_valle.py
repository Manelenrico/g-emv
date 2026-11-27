"""[P8] Banco: las ocho criaturas del siete en el valle frente al jugador tonto, en lo mismo (20 días, semillas 1-10, peligro medio).
Medidas, por partida: muertes y causas; tiempo de cada una en su equilibrio (vida >= 70, hambre <= 50, cansancio < 70; decisión del prompt 9);
dónde pasa el tiempo (casa, huerto = pegada a una planta, aldea, camino, bosque, zona salvaje); qué da y a quién; empujones y golpes (y entre hermanas);
robos y golpes de la bestia; lo que come, coge, deja y trabaja; las llamadas; y (prompt 11) cuántas veces una criatura con hambre alta (> 60) lleva comida y no come.
(prompt 12) además: cuántos días vive cada una; cuántas veces sale a la zona salvaje (entradas desde otro terreno); de noche, qué parte de sus turnos
pasa en una casa (la suya, u otra) y si duerme; el nivel del almacén (comidas) al empezar cada día y al final; y lo que pesan las dos curiosidades nuevas.
Las acciones y su resultado se leen envolviendo `_actua` del mundo desde fuera (sin tocar el mundo).   python3 banco_cuerpo_valle.py -> banco_cuerpo_valle.json"""
import collections, json, os, sys
from multiprocessing import Pool
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI)); sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(RAIZ, "valle"))
from mundo import Valle
from jugadores import Mapa, Tonto
import cuerpo_valle as CV
DIAS = 20; MANDO = "medio"; SEMILLAS = range(1, 11); SALIDA = os.environ.get("BANCO_SALIDA", "banco_cuerpo_valle_v2.json")


# (prompt 14) los números del mundo de la v5 (antes del prompt 14), para la puerta de igualdad con el banco v2
MUNDO_V5 = {"criaturas": {"vida_por_turno_durmiendo": 0.05, "hambre_por_trabajo": None, "cansancio_por_trabajo": None}, "terreno_salvaje": {"prob_herida": 0.02, "dano": 10}}


def partida(tipo, semilla, registro=None, dias=DIAS, objetos_cada=0, cultura=None, anticipa=False, mundo=None, comer_luego=False, mando=MANDO, riqueza_valle=False, robo_noche=False, comer_al_final=False, promesa_una=False, matorrales=False, cfg_mundo=None, plantas=False, recuerdo_vacio=False, histeresis_llamadas=False, compromiso=False, dormir_en_casa=False, cansancio_suelta=False, dar_comida=False, responde_llamadas=False, comida_sin_hambre=False, comida_sobra=False, sabe_reglas_trabajo=False, enfado=False, comida_por_dia=False, vecinas=False, comida_sin_hermana=False, distancias=False, emociones=False, registro_emo=None, **extra):
    e = Valle(mando=mando, registro=registro, objetos_cada=objetos_cada)
    if cfg_mundo:                                                         # (prompt 19) otra config entera del mundo (para la igualdad con un banco de antes)
        e.cfg = json.load(open(cfg_mundo, encoding="utf-8")); e.cfg["bestia"]["mando"] = mando
    e.cfg["dias_por_episodio"] = dias
    for sec, kv in (mundo or {}).items():
        for k, v in kv.items():
            if v is None: e.cfg[sec].pop(k, None)
            else: e.cfg[sec][k] = v
    if extra.get("robos_v47") or extra.get("prop_real_v47"):              # (prompt 93) lo que el mundo enseña a las versiones nuevas (apagado para las de antes)
        e.cfg.setdefault("observacion", {}); e.cfg["observacion"] = dict(e.cfg["observacion"], empujones_vistos=bool(extra.get("robos_v47")), lo_que_hizo=bool(extra.get("prop_real_v47")))
    if extra.get("cara_v64"): e.cfg["cara_v64"] = {"activo": True}            # (prompt 128, taller) la cara y la voz de la base: el mundo las pasa solo a las clases que las tienen
    if extra.get("voz_v64") or extra.get("para_v64"): e.cfg["voz_v64"] = {"activo": True}
    if extra.get("voz_piezas_v68"): e.cfg["voz_v64"] = {"activo": True}; e.cfg["voz_v68"] = {"activo": True}      # (prompt 132, taller) la voz pieza a pieza: entregarla, y la alarma despierta sin quitar lo de antes
    if extra.get("dormida_sin_voz_v67"): e.cfg["dormida_sin_voz_v67"] = {"activo": True}      # (prompt 131, taller) la dormida sin voz (la de antes), solo en las clases que lo tienen
    obs, infos = e.reset(seed=semilla); mp = infos[e.agents[0]]["mapa"]; Mp = Mapa(mp)
    J = {a: (CV.Criatura(a, mp, cultura=cultura, anticipa=anticipa, comer_luego=comer_luego, riqueza_valle=riqueza_valle, robo_noche=robo_noche, comer_al_final=comer_al_final, promesa_una=promesa_una, matorrales=matorrales, plantas=plantas, recuerdo_vacio=recuerdo_vacio, histeresis_llamadas=histeresis_llamadas, compromiso=compromiso, dormir_en_casa=dormir_en_casa, cansancio_suelta=cansancio_suelta, dar_comida=dar_comida, responde_llamadas=responde_llamadas, comida_sin_hambre=comida_sin_hambre, comida_sobra=comida_sobra, sabe_reglas_trabajo=sabe_reglas_trabajo, enfado=enfado, comida_por_dia=comida_por_dia, vecinas=vecinas, comida_sin_hermana=comida_sin_hermana, distancias=distancias, semilla_partida=semilla, **extra) if tipo == "cuerpo" else Tonto(a, semilla, Mp, e.cfg["huerto"]["trabajo_necesario"])) for a in e.agents}
    casas = {tuple(c) for v in mp["casas"].values() for c in v["celdas"]}; plantas = [tuple(p) for p in mp["plantas"]]
    R = {"acciones": collections.Counter(), "dar": collections.Counter(), "empujones": 0, "golpes": 0, "empujones_hermanas": 0, "golpes_hermanas": 0,
         "llamadas": collections.Counter(), "dejar": collections.Counter(), "coger": collections.Counter(), "con_hambre_lleva_y_no_come": 0,
         "equilibrio": collections.Counter(), "vivo": collections.Counter(), "sitio": collections.Counter(),
         "salidas_salvaje": collections.Counter(), "noche": collections.Counter(), "noche_en_casa": collections.Counter(), "noche_en_su_casa": collections.Counter(),
         "noche_duerme": collections.Counter(), "almacen_por_turno": [],
         "entradas_salvaje": collections.Counter(), "en_casa_al_280": collections.Counter(), "noches": collections.Counter(), "da_fruto": 0, "coger_medicina": collections.Counter(),
         "creencias_dia": [], "noche_dia": {}, "comidas": 0, "comidas_sin_hambre": 0, "come_de": collections.Counter(), "matorrales_vistos_dia": [], "noche_sitio": collections.Counter(), "duerme_sitio": collections.Counter(), "guardada_dia": [], "dar_detalle": [], "duerme_fase": collections.Counter(), "huerto_actividad": collections.Counter(), "juntas": collections.Counter(), "tras_robo": collections.Counter(), "robos_a_criaturas": 0, "empujes_bestia": [], "pega_por_resistirse": 0, "recupera": 0, "robos_dia": [], "duelos": [], "tras_robo_hermana": collections.Counter(), "dejar_tipo": collections.Counter(), "comer_luego": collections.Counter(), "ir": collections.Counter(), "frontera_en_elegida": 0, "cuanto_en_elegida": 0, "vistas_fin": {}}
    prev_t = {}; vistos_mat = {}; robada = {}; duelo_seg = {}; d19 = {}; full = {}; R["duelos19"] = []; R["acciones_sin_duelo"] = collections.Counter(); R["peleas"] = []
    _oa = e._actua
    def actua(a, acc):
        # (prompt 17) de dónde sale la comida que comen: cada comida cogida lleva su origen (una clave más en el objeto; el mundo no la lee)
        origen_comida = None
        if acc.get("accion") == "comer":
            i = next((i for i, o in enumerate(e.bolsa[a]) if (acc.get("tipo") is None or o["tipo"] == acc.get("tipo")) and e.cfg["objetos"][o["tipo"]].get("se_come")), None)
            if i is not None and e.bolsa[a][i]["tipo"] == "comida": origen_comida = e.bolsa[a][i].get("_origen", "llevaba")
        p0 = tuple(e.pos[a])
        if acc.get("accion") == "empujar" and acc.get("a") == "bestia":   # (prompt 27) el empujón a la bestia: quién, cuántas pegadas, si venía de un robo
            n_ = sum(1 for x in e.vivas() if e.vecinas(e.pos[x], e.bestia["pos"])); lleva_ = len(e.bestia["lleva"])
            h_ = a[0] + ("2" if a[1] == "1" else "1")
        if acc.get("accion") in ("empujar", "golpear") and acc.get("a") not in (None, "bestia"):     # (prompt 39) peleas entre criaturas: quién a quién y qué pasa
            b_ = acc.get("a"); lleva_b = len(e.bolsa.get(b_, [])) if b_ in e.bolsa else 0; vida_b = e.cuerpo[b_]["vida"] if b_ in e.cuerpo else None
        r = _oa(a, acc); ok = (r.get("resultado") == "ok") or str(r.get("resultado", "")).startswith("gana")
        if acc.get("accion") in ("empujar", "golpear") and acc.get("a") not in (None, "bestia") and len(R["peleas"]) < 3000:
            R["peleas"].append({"t": e.turno, "dia": e.turno // e.dia_turnos, "fase": e.fase(), "de": a, "a": b_, "misma_casa": a[0] == str(b_)[0], "accion": acc["accion"],
                                "resultado": r.get("resultado"), "soltado": r.get("soltado"), "llevaba": lleva_b, "vida_antes": vida_b,
                                "vida_despues": e.cuerpo[b_]["vida"] if b_ in e.cuerpo else None, "muere": bool(b_ in e.cuerpo and e.cuerpo[b_]["muerta"])})
        if acc.get("accion") == "empujar" and acc.get("a") == "bestia":
            R["empujes_bestia"].append({"turno": e.turno, "fase": e.fase(), "quien": a, "pegadas": n_, "gana": str(r.get("resultado", "")).startswith("gana"), "resultado": r.get("resultado"),
                                        "bestia_llevaba": lleva_, "hermana_pegada": h_ in e.agents and e.vecinas(e.pos[h_], e.bestia["pos"]),
                                        "tras_robo_propio": a in robada, "tras_robo_hermana": h_ in robada,
                                        "tras_robo_vecina": any(x not in (a, h_) for x in robada)})
        if ok and acc.get("accion") == "coger" and e.bolsa[a]:
            de = acc.get("de"); ms = e.matorral_junto(a) if de == "matorral" else []
            e.bolsa[a][-1]["_origen"] = {"planta": "huerto", "almacen": "almacen", "despensa": "despensa"}.get(de) or (("matorral_" + e.matorrales[ms[0]]["zona"]) if ms else None) or ("suelo_" + e.terreno(p0))
        if ok and origen_comida is not None: R["come_de"][origen_comida] += 1
        if ok:
            t = acc.get("accion"); R["acciones"][t] += 1; b = acc.get("a")
            if t == "dar":
                R["dar"][("hermana" if b and b[0] == a[0] else "otra")] += 1
                if len(R["dar_detalle"]) < 300:                              # (prompt 23) en qué situación
                    R["dar_detalle"].append({"turno": e.turno, "dia": e.turno // e.dia_turnos, "fase": e.fase(), "de": a, "a": b, "tipo": r.get("tipo", acc.get("tipo")),
                                             "hambre_da": round(e.cuerpo[a]["hambre"], 1), "hambre_recibe": round(e.cuerpo[b]["hambre"], 1) if b in e.cuerpo else None,
                                             "lleva_da": len(e.bolsa[a]), "donde": e.terreno(tuple(e.pos[a])),
                                             "tras_llamada": (tipo == "cuerpo" and getattr(J[a], "ultima_ayuda_t", None) is not None and e.turno - J[a].ultima_ayuda_t <= CV.T["mirada"] + 1)})
            if t == "empujar": R["empujones"] += 1; R["empujones_hermanas"] += int(bool(b and b != "bestia" and b[0] == a[0]))
            if t == "golpear": R["golpes"] += 1; R["golpes_hermanas"] += int(bool(b and b != "bestia" and b[0] == a[0]))
            if t == "llamar": R["llamadas"][acc.get("llamada")] += 1
            if t == "dejar": R["dejar"][acc.get("en")] += 1; R["dejar_tipo"][f'{acc.get("en")}|{acc.get("tipo")}'] += 1
            if t == "coger": R["coger"][acc.get("de")] += 1
        return r
    e._actua = actua
    # (prompt 32) las seis emociones (solo medir): en cada turno, las seis de la foto de ahora de cada criatura y la más fuerte; los momentos que se miran
    EMO = emociones and tipo == "cuerpo"; fe = open(registro_emo, "w", encoding="utf-8") if (EMO and registro_emo) else None
    if EMO:
        R["emo"] = {"nombre": collections.Counter(), "suma": dict.fromkeys(CV.SEIS, 0.0), "n": 0, "momentos": {}}; pend = {}; huida = {}; R["huidas"] = []
        R["cambio"] = {}; prevq = {}; pend_d = {}
        R["regalos_necesidad"] = collections.Counter(); R["consuelos"] = []; peg_duelo = set()       # (prompt 36) regalos con y sin necesidad; llegar al lado de una de duelo
        # (prompt 34) la huida, turno a turno: con la bestia a la vista, ¿se queda quieta o da un paso hacia ella?; y dónde están al anochecer
        R["con_bestia"] = {"duelo": collections.Counter(), "sin": collections.Counter()}; vis_prev = {}
        R["anochecer"] = {"duelo": collections.Counter(), "sin": collections.Counter()}; R["anochecer_dist_casa"] = {"duelo": [], "sin": []}
        ini_anoch = sum(n for nom, n in e.cfg["dia"]["fases"] if nom in ("mañana", "tarde"))                        # (prompt 33) los lados buenos como cambio en ese turno: placer, alegría, amor
        def cambio(k, a, d_):
            L_ = R["cambio"].setdefault(k, [])
            if len(L_) < 3000: L_.append(dict({"t": e.turno, "a": a}, **d_))
        def momento(k, a, sx, extra_=None):
            L_ = R["emo"]["momentos"].setdefault(k, [])
            if len(L_) < 3000: L_.append(dict({"t": e.turno, "a": a, "seis": {q: round(v, 4) for q, v in sx.items()}}, **(extra_ or {})))
    while e.agents:
        acts = {}
        if e.turno % 50 == 0: R["almacen_por_turno"].append([e.turno, sum(1 for o in e.almacen if o["tipo"] == "comida")])
        if e.turno % e.dia_turnos == 0 and e.turno:                        # (prompt 22) la comida guardada al acabar cada día: almacén + despensas
            R["guardada_dia"].append(sum(1 for o in e.almacen if o["tipo"] == "comida") + sum(1 for d in e.despensa.values() for o in d if o["tipo"] == "comida"))
        if e.turno % e.dia_turnos == 0 and e.turno:                        # (prompt 19) cuántos matorrales distintos ha visto cada una, al acabar cada día
            R["matorrales_vistos_dia"].append({"dia": e.turno // e.dia_turnos - 1, "vistos": {a: len(vistos_mat.get(a, ())) for a in e.agents}})
        if tipo == "cuerpo" and e.turno % e.dia_turnos == 0:              # (prompt 14) lo que cree de lo que dice la cultura, al empezar cada día
            cr = lambda c, o, s_, d: ((c.creencia(o, s_) or {}).get(d))
            R["creencias_dia"].append({"dia": e.turno // e.dia_turnos, "criaturas": {a: {"salvaje_cuerpo": cr(J[a].cuaderno, "sitio:salvaje", "dia", "cuerpo"), "bosque_recursos": cr(J[a].cuaderno, "sitio:bosque", "dia", "recursos"),
                                     "bestia_noche": cr(J[a].cuaderno, "bestia", "noche", "cuerpo"), "bestia_noche_recursos": cr(J[a].cuaderno, "bestia", "noche", "recursos"), "trabajar": cr(J[a].cuaderno, "trabajar", "huerto", "recursos"), "comida": cr(J[a].cuaderno, "comida", "valle", "cuerpo")} for a in e.agents}})
        for a in e.agents:
            x = J[a].actua(obs[a], infos[a]); acts[a] = {k: v for k, v in x.items() if not k.startswith("_")}; full[a] = x
            if EMO:                                                        # (prompt 32) las seis de ahora (no cambian la decisión, ya tomada)
                sx, _F = J[a].seis_ahora(); top = max(CV.SEIS, key=lambda q: (sx[q], -CV.SEIS.index(q))) if max(sx.values()) > 0 else "ninguna"
                R["emo"]["nombre"][top] += 1; R["emo"]["n"] += 1
                for q in CV.SEIS: R["emo"]["suma"][q] += sx[q]
                if fe is not None: fe.write(json.dumps({"turno": e.turno, "a": a, "seis": {q: round(v, 3) for q, v in sx.items()}, "top": top}) + "\n")
                if a in pend: momento(pend.pop(a), a, sx)                    # el turno después de un robo, un golpe o un regalo recibido
                cur = {"dis": sx["displacer"], "W": J[a].riqueza_ahora(), "vin": J[a].vinculo_total()}
                if a in prevq:                                             # (prompt 33) lo que cambió del turno anterior a este
                    pq = prevq[a]; d_ = {"placer": round(max(0.0, pq["dis"] - cur["dis"]), 4), "alegria": round(max(0.0, cur["W"] - pq["W"]), 4), "amor": round(max(0.0, cur["vin"] - pq["vin"]), 4),
                                         "displacer_sube": round(max(0.0, cur["dis"] - pq["dis"]), 4), "pierde": round(max(0.0, pq["W"] - cur["W"]), 4), "vinculo_baja": round(max(0.0, pq["vin"] - cur["vin"]), 4)}
                    for k_ in pend_d.pop(a, []): cambio(k_, a, d_)
                    if e.turno % 20 == 0: cambio("todas", a, d_)
                prevq[a] = cur; sit = []
                xa_ = x.get("accion")
                if xa_ == "coger" and x.get("de") in ("matorral", "planta", "suelo") and (x.get("tipo") or "comida") == "comida": sit.append("comida")
                if xa_ == "dar": sit.append("dar_hermana" if x.get("a") == J[a].hermana else "dar_vecina")
                if getattr(J[a], "duelo_v19", False) and J[a].duelo_propio(e.turno)[1]: sit.append("duelo")
                pa0 = tuple(e.pos[a]); vec_ = [y for y in e.agents if y != a and max(abs(e.pos[y][0] - pa0[0]), abs(e.pos[y][1] - pa0[1])) <= 1]
                if any(getattr(J[y], "duelo_v19", False) and J[y].duelo_propio(e.turno)[1] for y in vec_): sit.append("acompana_a_una_de_duelo")
                if "duelo" in sit and vec_: sit.append("de_duelo_acompanada")
                for y in vec_:                                                # (prompt 36) consuelo: llega al lado de una que está de duelo (y no lo estaba el turno antes)
                    if getattr(J[y], "duelo_v19", False) and J[y].duelo_propio(e.turno)[1]:
                        if (a, y) not in peg_duelo and len(R["consuelos"]) < 2000: R["consuelos"].append({"t": e.turno, "de": a, "a": y, "hermana": a[0] == y[0], "ir": x.get("_ir")})
                peg_duelo = {k for k in peg_duelo if k[0] != a} | {(a, y) for y in vec_ if getattr(J[y], "duelo_v19", False) and J[y].duelo_propio(e.turno)[1]}
                if sit: pend_d[a] = sit
                xa = x.get("accion")
                if xa == "coger" and x.get("de") in ("matorral", "planta", "suelo") and (x.get("tipo") or "comida") == "comida": momento("comida", a, sx, {"de": x.get("de")})
                if xa == "dar":
                    momento("dar", a, sx)
                    if hasattr(J[a], "necesita"): R["regalos_necesidad"][("con" if J[a].necesita(x.get("a"), x.get("tipo")) else "sin") + "_necesidad"] += 1
                if any(o_["de"] == J[a].hermana for o_ in obs[a].get("oido") or []): momento("llamada_hermana", a, sx, {"llamada": next((o_.get("llamada") or ("sonido:" + str(o_.get("sonido")))) for o_ in obs[a]["oido"] if o_["de"] == J[a].hermana)})     # (prompt 54) también un sonido
                if e.turno % 20 == 0:                                      # muestras (cada 20 turnos): todas, el duelo, la noche, la sequía
                    momento("todas", a, sx)
                    if getattr(J[a], "duelo_v19", False) and J[a].duelo_propio(e.turno)[1]: momento("duelo", a, sx)
                    if obs[a]["fase"] == "noche": momento("noche", a, sx)
                    if e.epoca() == "escasez": momento("sequia", a, sx)
                bp = e.bestia["pos"]; pa_ = tuple(e.pos[a]); dB = max(abs(bp[0] - pa_[0]), abs(bp[1] - pa_[1])); V_ = e.cfg["criaturas"]["vista"]
                if getattr(J[a], "duelo_v19", False):
                    en_d = "duelo" if J[a].duelo_propio(e.turno)[1] else "sin"
                    if obs[a].get("bestia") is not None and e.celda_casa.get(pa_) is None:     # se mira su paso de este turno al empezar el siguiente
                        vis_prev[a] = (en_d, pa_, tuple(bp), xa)
                    if obs[a]["turno_del_dia"] == ini_anoch:                 # al empezar el anochecer: dónde está
                        cc = e.celda_casa.get(pa_); ter = e.terreno(pa_)
                        sitio = "su casa" if cc == e.casa_de[a] else "otra casa" if cc is not None else "huerto" if any(max(abs(pa_[0] - q[0]), abs(pa_[1] - q[1])) <= 1 for q in plantas) else ter
                        R["anochecer"][en_d][sitio] += 1
                        cas_ = [tuple(c) for c in mp["casas"][e.casa_de[a]]["celdas"]]; R["anochecer_dist_casa"][en_d].append(min(max(abs(pa_[0] - c[0]), abs(pa_[1] - c[1])) for c in cas_))
                    if obs[a]["fase"] == "noche" and e.turno % 20 == 0: momento("en_casa_de_noche" if e.celda_casa.get(pa_) is not None else "fuera_de_noche", a, sx)
                if a in huida:                                             # (prompt 32) turnos hasta alejarse (fuera de la vista) desde que ve la bestia
                    h_ = huida[a]
                    if dB > V_ or e.celda_casa.get(pa_) is not None or e.turno - h_["t0"] >= 40:
                        h_["turnos"] = e.turno - h_["t0"]; h_["se_aleja"] = dB > V_ or e.celda_casa.get(pa_) is not None; R["huidas"].append(huida.pop(a))
                elif obs[a].get("bestia") is not None and e.celda_casa.get(pa_) is None and getattr(J[a], "duelo_v19", False):
                    huida[a] = {"t0": e.turno, "a": a, "d0": dB, "duelo": bool(J[a].duelo_propio(e.turno)[1]), "atencion": round(J[a].atencion(e.turno), 3), "fase": obs[a]["fase"]}
            yo = obs[a]["yo"]; p = tuple(yo["pos"])
            if yo["hambre"] > 60 and "comida" in obs[a]["bolsa"] and acts[a]["accion"] != "comer": R["con_hambre_lleva_y_no_come"] += 1
            if acts[a]["accion"] == "comer" and acts[a].get("tipo") == "comida":     # (prompt 16) comer sin hambre: con menos hambre de la que quita una comida (de verdad)
                R["comidas"] += 1; R["comidas_sin_hambre"] += int(yo["hambre"] < e.cfg["objetos"]["comida"]["nutricion"])
            R["vivo"][a] += 1
            for c in obs[a]["casillas"]:
                if c.get("matorral") is not None: vistos_mat.setdefault(a, set()).add(tuple(c["pos"]))
            if yo["vida"] >= 70 and yo["hambre"] <= 50 and yo["cansancio"] < 70: R["equilibrio"][a] += 1
            if p in casas: s = "casa"
            elif any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) <= 1 for q in plantas): s = "huerto"
            else: s = {"aldea": "aldea", "camino": "camino", "bosque": "bosque", "salvaje": "salvaje", "huerto": "huerto"}.get(e.terreno(p), e.terreno(p))
            R["sitio"][s] += 1
            pass                                                           # (prompt 25) el sueño se cuenta después del turno: el que de verdad salió (ver abajo)
            ter = e.terreno(p)
            if ter == "salvaje" and prev_t.get(a, "salvaje") != "salvaje": R["salidas_salvaje"][a] += 1
            if ter != "salvaje" and acts[a]["accion"] == "mover":            # (prompt 14) el paso que la mete en la zona salvaje, y por qué
                dd = CV.DIRS[acts[a]["dir"]]; q2 = (p[0] + dd[0], p[1] + dd[1])
                if e.dentro(q2) and e.terreno(q2) == "salvaje":
                    nec = yo["vida"] < e.cfg["criaturas"]["umbral_herida"] and "medicina" not in obs[a]["bolsa"]
                    R["entradas_salvaje"][(x.get("_ir") or "mover") + ("|herida_sin_medicina" if nec else "|resto")] += 1
            if acts[a]["accion"] == "coger" and acts[a].get("tipo") == "medicina": R["coger_medicina"][ter] += 1
            if obs[a]["turno_del_dia"] == sum(n for nom, n in e.cfg["dia"]["fases"] if nom != "noche"):
                R["noches"][a] += 1; R["en_casa_al_280"][a] += int(p in casas)
            prev_t[a] = ter
            if obs[a]["fase"] == "noche":
                nd = R["noche_dia"].setdefault(str(obs[a]["dia"]), {"1": [0, 0], "2": [0, 0]})[a[1]]; nd[0] += int(p in casas); nd[1] += 1    # (prompt 15) por día y carácter
                R["noche_sitio"]["casa" if p in casas else e.terreno(p)] += 1                       # (prompt 21) dónde pasan la noche
                R["noche"][a] += 1; R["noche_en_casa"][a] += int(p in casas); R["noche_en_su_casa"][a] += int(bool(yo.get("en_casa"))); R["noche_duerme"][a] += int(acts[a]["accion"] == "dormir")
            if tipo == "cuerpo":
                u = J[a].ultima; fl = u.get("filas") or {}
                if x.get("_ir"): R["ir"][x["_ir"]] += 1
                if x["accion"] == "comer" and u.get("luego"): R["comer_luego"][u["luego"]] += 1
                R["frontera_en_elegida"] += int(fl.get("R-CURIOSIDAD-FRONTERA", 0) > 0); R["cuanto_en_elegida"] += int(fl.get("R-CURIOSIDAD-CUANTO", 0) > 0)
        fase_t = e.fase(); vivas_t = list(e.agents)
        for h_, D_ in list(duelo_seg.items()):                             # (prompt 29) qué hace la que siente el duelo
            if h_ not in acts or e.turno - D_["turno"] > 400:
                D_["acciones"] = dict(D_["acciones"]); D_["s_muerte_media"] = round(sum(D_["s_muerte"]) / len(D_["s_muerte"]), 3) if D_["s_muerte"] else 0.0
                D_["dist_al_cuerpo_media"] = round(sum(D_["dist_al_cuerpo"]) / len(D_["dist_al_cuerpo"]), 1) if D_["dist_al_cuerpo"] else None
                del D_["s_muerte"], D_["dist_al_cuerpo"]; R["duelos"].append(D_); duelo_seg.pop(h_); continue
            x_ = acts[h_]; D_["acciones"][x_.get("_ir") or x_["accion"]] += 1
            if tipo == "cuerpo":
                sm = (J[h_].ultima.get("filas") or {}).get("S-MUERTE-PAREJA", 0.0); D_["s_muerte"].append(sm)
                if J[h_].pareja_muerta and D_["lo_sabe_en"] is None: D_["lo_sabe_en"] = e.turno - D_["turno"]
                pm = e.pos[D_["muere"]]; ph = e.pos[h_]; D_["dist_al_cuerpo"].append(max(abs(pm[0] - ph[0]), abs(pm[1] - ph[1])))
        if tipo == "cuerpo" and getattr(J[e.possible_agents[0]], "duelo_v19", False):   # (prompt 31) cada duelo (quien se entera de una muerte), mientras le dura
            cheb_ = lambda p, q: max(abs(p[0] - q[0]), abs(p[1] - q[1]))
            en_duelo = set()
            for a in vivas_t:
                for x_m, m in J[a].muertas.items():
                    k = (a, x_m)
                    if k not in d19:
                        otras_ = [y for y in vivas_t if y not in (a, J[a].hermana)]
                        d19[k] = {"quien": a, "muere": x_m, "hermana": m["hermana"], "dia": e.cuerpo[x_m]["turno_muerte"] // e.dia_turnos, "w": round(m["w"], 3),
                                  "lo_sabe_en": e.turno - e.cuerpo[x_m]["turno_muerte"], "dura_turnos": round(J[a].duelo_dura(J[a].semivida_duelo(m["hermana"]))),
                                  "acciones": collections.Counter(), "acciones_50": collections.Counter(), "llama_duelo": 0, "turnos": 0,
                                  "vin0": {y: round(J[a].vin.get(y, 0.0), 3) for y in otras_}, "vin_de_ellas0": {y: round(J[y].vin.get(a, 0.0), 3) for y in otras_},
                                  "van": collections.Counter(), "pegadas": collections.Counter(), "dist_suyas": [], "s_muerte": []}
                    D = d19[k]
                    if D.get("fin") is not None: continue
                    dt = e.turno - m["t"]
                    if dt > D["dura_turnos"] or a not in acts or e.turno >= e.max_turnos - 1:
                        D["fin"] = dt; vv = [y for y in D["vin0"] if y in vivas_t]          # el vínculo al acabar el duelo, con las que siguen vivas
                        D["vin1"] = {y: round(J[a].vin.get(y, 0.0), 3) for y in vv}; D["vin_de_ellas1"] = {y: round(J[y].vin.get(a, 0.0), 3) for y in vv}; continue
                    en_duelo.add(a); xa = full[a]; c_ = xa.get("_ir") or xa["accion"]; D["acciones"][c_] += 1; D["turnos"] += 1
                    if dt < 50: D["acciones_50"][c_] += 1
                    if xa["accion"] == "llamar" and xa.get("llamada") == "estoy_de_duelo": D["llama_duelo"] += 1
                    D["s_muerte"].append((J[a].ultima.get("filas") or {}).get("S-MUERTE-PAREJA", 0.0))
                    pa = e.pos[a]; ds = [cheb_(pa, e.pos[y]) for y in vivas_t if y != a]
                    if ds: D["dist_suyas"].append(min(ds))
                    for y in vivas_t:
                        if y == a: continue
                        xy = full.get(y) or {}; dq = (J[y].dest or {}).get("acc") or {}
                        if (xy.get("_ir") == "ir_vecina" and dq.get("quien") == a) or (y == J[a].hermana and xy.get("_ir") == "ir_pareja"): D["van"][y] += 1
                        if cheb_(pa, e.pos[y]) <= 1: D["pegadas"][y] += 1
            for a in vivas_t:
                if a not in en_duelo and a in full: R["acciones_sin_duelo"][full[a].get("_ir") or full[a]["accion"]] += 1
        for v_, t0 in list(robada.items()):                                # (prompt 26) qué hacen en los 20 turnos después de que la bestia les robe (y su hermana)
            if e.turno - t0 > 20 or v_ not in acts: robada.pop(v_); continue
            x_ = acts[v_]; R["tras_robo"][x_.get("_ir") or x_["accion"]] += 1
            h_ = v_[0] + ("2" if v_[1] == "1" else "1")
            if h_ in acts: R["tras_robo_hermana"][acts[h_].get("_ir") or acts[h_]["accion"]] += 1
        for a in vivas_t:                                                  # (prompt 25) junto al huerto: qué hace; y si las hermanas van juntas
            p_ = tuple(e.pos[a])
            if any(max(abs(p_[0] - q[0]), abs(p_[1] - q[1])) <= 1 for q in plantas):
                ac = acts[a]["accion"]; R["huerto_actividad"]["trabaja" if ac == "trabajar" else "quieta" if ac == "quedarse" else "come" if ac == "comer" else "duerme" if ac == "dormir" else "coge" if ac == "coger" else "otra"] += 1
            her = a[0] + ("2" if a[1] == "1" else "1")
            if a[1] == "1" and her in e.agents:
                d_ = max(abs(p_[0] - e.pos[her][0]), abs(p_[1] - e.pos[her][1])); R["juntas"]["pares_turnos"] += 1
                R["juntas"]["a_2_o_menos"] += int(d_ <= 2); R["juntas"]["a_5_o_menos"] += int(d_ <= 5)
        obs, rew, term, trunc, infos = e.step(acts)
        if tipo == "cuerpo" and emociones:
            for a, (en_d, p0_, b0_, xa0) in list(vis_prev.items()):         # (prompt 34) el paso que dio con la bestia a la vista: quieta, hacia ella o lejos
                if a in e.pos and not e.cuerpo[a]["muerta"]:
                    p1_ = tuple(e.pos[a]); C_ = R["con_bestia"][en_d]; C_["turnos"] += 1
                    d0_ = max(abs(p0_[0] - b0_[0]), abs(p0_[1] - b0_[1])); d1_ = max(abs(p1_[0] - b0_[0]), abs(p1_[1] - b0_[1]))
                    C_["quieta" if p1_ == p0_ else "hacia_ella" if d1_ < d0_ else "lejos" if d1_ > d0_ else "de_lado"] += 1
                    if xa0 in ("quedarse", "dormir"): C_["elige_quedarse_o_dormir"] += 1
            vis_prev = {}
        R["da_fruto"] += sum(1 for ev in e._eventos if "da_fruto" in ev)
        for ev in e._eventos:
            if EMO:
                if "bestia_roba" in ev: pend[ev["bestia_roba"]] = "robo"; pend_d.setdefault(ev["bestia_roba"], []).append("robo")
                if "bestia_pega" in ev and ev.get("por") != "se resiste": pend_d.setdefault(ev["bestia_pega"], []).append("dano")
                if "terreno_hiere" in ev: pend_d.setdefault(ev["terreno_hiere"], []).append("dano")
                if "bestia_pega" in ev and ev.get("por") != "se resiste": pend[ev["bestia_pega"]] = "golpe_bestia"
                if "terreno_hiere" in ev: pend[ev["terreno_hiere"]] = "terreno"
            if "bestia_roba" in ev and ev["bestia_roba"] in e.possible_agents: robada[ev["bestia_roba"]] = e.turno; R["robos_a_criaturas"] += 1; R["robos_dia"].append(e.turno // e.dia_turnos)
            if "muere" in ev and tipo == "cuerpo":                         # (prompt 29) el duelo: la hermana de la que muere, los 400 turnos siguientes
                h_ = ev["muere"][0] + ("2" if ev["muere"][1] == "1" else "1")
                if h_ in e.agents: duelo_seg[h_] = {"muere": ev["muere"], "causa": ev.get("causa"), "turno": e.turno, "dia": e.turno // e.dia_turnos, "hermana": h_, "acciones": collections.Counter(),
                                                    "s_muerte": [], "lo_sabe_en": None, "dist_al_cuerpo": []}
            if ev.get("por") == "se resiste": R["pega_por_resistirse"] += 1
            if "bestia_suelta" in ev: R["recupera"] += 1
        for a in vivas_t:                                                  # (prompt 22-25) dónde y cuándo duermen: solo el sueño que salió (sin sueño, dormir falla)
            if e.cuerpo[a].get("dormida"): q = tuple(e.pos[a]); R["duerme_sitio"]["casa" if q in casas else e.terreno(q)] += 1; R["duerme_fase"][fase_t] += 1
    if tipo == "cuerpo": R["vistas_fin"] = {a: round(1 - J[a].ignorancia_global(), 4) for a in J}
    R["dias_vividos"] = {a: round((e.cuerpo[a]["turno_muerte"] if e.cuerpo[a]["muerta"] else e.turno) / e.dia_turnos, 3) for a in e.possible_agents}
    R["muertes"] = [{"criatura": a, "causa": e.cuerpo[a]["causa"], "dia": e.cuerpo[a]["turno_muerte"] // e.dia_turnos, "agotada": e.cuerpo[a]["agotada"]} for a in e.possible_agents if e.cuerpo[a]["muerta"]]
    R["bestia"] = {k: e.stats[k] for k in ("bestia_roba", "bestia_pega", "bestia_come_huerto")}
    R["almacen_fin_dia"] = [d["comida"] for d in e.stats["almacen_fin_dia"]]; R["almacen_nivel_fin_dia"] = [d["nivel"] for d in e.stats["almacen_fin_dia"]]; R["trabajo_por_huerto"] = e.stats["trabajo_por_huerto"]
    R["comida"] = {k: sum(d["comida"].get(k, 0) for d in e.cuadre) for k in ("aparece", "comido", "podrido", "comido_bestia")}
    R["cuadra"] = all(all(d[t]["cuadra"] for t in e.tipos_objeto) for d in e.cuadre)
    for h_, D_ in duelo_seg.items():                                       # los duelos que siguen abiertos al acabar
        D_["acciones"] = dict(D_["acciones"]); D_["s_muerte_media"] = round(sum(D_["s_muerte"]) / len(D_["s_muerte"]), 3) if D_["s_muerte"] else 0.0
        D_["dist_al_cuerpo_media"] = round(sum(D_["dist_al_cuerpo"]) / len(D_["dist_al_cuerpo"]), 1) if D_["dist_al_cuerpo"] else None
        del D_["s_muerte"], D_["dist_al_cuerpo"]; R["duelos"].append(D_)
    for (a, x_m), D in d19.items():                                       # (prompt 31) cierre de cada duelo
        otras_ = list(D["vin0"]); vv = [y for y in otras_ if not e.cuerpo[y]["muerta"]]
        if "vin1" not in D: D["vin1"] = {y: round(J[a].vin.get(y, 0.0), 3) for y in vv}; D["vin_de_ellas1"] = {y: round(J[y].vin.get(a, 0.0), 3) for y in vv}
        D["oyen_duelo"] = {y: J[y].oidas.get("vecina:estoy_de_duelo", 0) for y in otras_}
        for c_ in ("acciones", "acciones_50", "van", "pegadas"): D[c_] = dict(D[c_])
        D["dist_suyas_media"] = round(sum(D["dist_suyas"]) / len(D["dist_suyas"]), 2) if D["dist_suyas"] else None
        D["s_muerte_dia"] = [round(sum(D["s_muerte"][i:i + 400]) / len(D["s_muerte"][i:i + 400]), 3) for i in range(0, len(D["s_muerte"]), 400)]
        del D["dist_suyas"], D["s_muerte"]; R["duelos19"].append(D)
    if tipo == "cuerpo": R["diag_dar"] = [dict(x, quien=a) for a in J for x in getattr(J[a], "diag_dar", [])]      # (prompt 35) por qué da
    if tipo == "cuerpo": R["diag_come_sin"] = [dict(x, quien=a) for a in J for x in getattr(J[a], "diag_come_sin", [])][:600]; R["diag_no_come"] = [dict(x, quien=a) for a in J for x in getattr(J[a], "diag_no_come", [])][:600]      # (prompt 36)
    if EMO:
        R["emo"]["nombre"] = dict(R["emo"]["nombre"]); R["regalos_necesidad"] = dict(R["regalos_necesidad"]); R["con_bestia"] = {k: dict(v) for k, v in R["con_bestia"].items()}; R["anochecer"] = {k: dict(v) for k, v in R["anochecer"].items()}
        if fe is not None: fe.close()
    R["matorrales_por_pareja"] = []                                        # (prompt 25) los matorrales vistos por cada hermana y por las dos
    for c_ in {x[0] for x in e.possible_agents}:
        A_, B_ = vistos_mat.get(c_ + "1", set()), vistos_mat.get(c_ + "2", set())
        R["matorrales_por_pareja"].append({"casa": c_, "uno": len(A_), "otra": len(B_), "las_dos": len(A_ | B_), "comunes": len(A_ & B_)})
    if tipo == "cuerpo":                                                   # (prompt 28) los dilemas hermana / vecina, y el vínculo con las vecinas al final
        R["dilemas"] = [d for a in J for d in getattr(J[a], "dilemas", [])][:400]
        R["vinculo_final"] = {a: {"hermana": round(J[a].B, 3), "vecinas": {x: round(v, 3) for x, v in getattr(J[a], "vin", {}).items()}} for a in J}
    if tipo == "cuerpo":                                                   # (prompt 24) llamadas oídas de la hermana y turnos respondiendo
        R["llamadas_oidas"] = dict(sum((collections.Counter(getattr(J[a], "oidas", {})) for a in J), collections.Counter()))
        R["respuestas"] = dict(sum((collections.Counter(getattr(J[a], "respuestas", {})) for a in J), collections.Counter()))
    if tipo == "cuerpo": R["creencia_comida"] = {a: (J[a].cuaderno.creencia("comida", "valle") or {}).get("cuerpo") for a in J}
    return {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in R.items()}


def _una(arg): t, s = arg; return dict(partida(t, s), tipo=t, semilla=s)


if __name__ == "__main__":
    with Pool(8) as P: res = P.map(_una, [(t, s) for t in ("tonto", "cuerpo") for s in SEMILLAS])
    json.dump(res, open(os.path.join(AQUI, SALIDA), "w"), ensure_ascii=False, indent=1)
    for t in ("tonto", "cuerpo"):
        B = [r for r in res if r["tipo"] == t]
        print(t, "vivas", [8 - len(r["muertes"]) for r in B], collections.Counter(x["causa"] for r in B for x in r["muertes"]), "cuadra", all(r["cuadra"] for r in B))

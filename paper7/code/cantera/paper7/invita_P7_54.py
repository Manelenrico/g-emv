"""[P7-54] LA INVITACION ENTRA EN EL CUERPO como un candidato mas (capitulo 5, paso 2; metodo de la mesa). GEMV_P7_54=1. Construccion, solo local.
  - Al arrancar lee /app/cuadernos/invitaciones_P7_<asiento>.json (lo que la razon dejo anoche: lista de invitaciones del menu de diario_razon_P7_54) y la CONFIANZA en la razon
    por dimension (cuerpo, recursos, vinculo) del cuaderno propio (`confianza_razon_P7_54`; empieza en 0,5).
  - En cada tic: una invitacion esta ACTIVA si su situacion se cumple ahora (anillo DENTRO/FUERA, calma CALMA/PELIGRO [nace_P7_33.peligro_de], movimiento QUIETA/MOVIENDOSE [sin
    cambiar de casilla en 24 tics], hermana CERCA/LEJOS [<= 4 casillas, a la vista o por el parte]). El candidato del cuerpo que corresponde a su accion (usar_botiquin, usar_racion,
    ir_objeto/coger de esa cosa, empunar_net, ponerse_camouflage, soltar_first_aid con la hermana a <= 2, ir_pareja, noop) recibe en SU foto imaginada el efecto prometido por
    dimension x confianza: filas INVITACION-CUERPO/RECURSOS/VINCULO (apetitivas si la promesa es alivio/ganar/acercar; aversivas, con sufijo -, si es dolor/perder/alejar), con
    M = |promesa| x confianza / escala (cuerpo: 25 de vida; recursos: 1 de W; vinculo: 1 de B), tope 1. El cuerpo decide si y cuando: nada mas cambia.
  - Lo que cree el cuerpo solo cambia con lo vivido (el cuaderno sigue igual). Tras ACEPTAR una invitacion (el elegido es su candidato): si la accion abre una prueba de la cosa, se
    espera a su huella (P7_huella) y se compara lo prometido con lo vivido por dimension (cuerpo = efecto cuerpo de la huella; recursos = efecto recursos; vinculo = cambio de
    distancia a la hermana en la ventana); si no (acercarse, quedarse quieta), se mira 240 tics: delta vida, delta W, delta B. Acierto por dimension = 1 si el signo coincide y
    |vivido| >= |prometido| / 2 (o las dos cosas < 1 unidad), 0 si no; confianza_dim <- 0,7 x confianza + 0,3 x acierto. La confianza viaja en el cuaderno.
Registros: P7_54_arranque (invitaciones cargadas, confianza), P7_54_activa (primer tic activa), P7_54_aceptada, P7_54_evaluada (prometido, vivido, acierto, confianza antes/despues), P7_54_cierre."""
import json, math, os
from alma import appraisal_zs_v42_exp as A, decisor_zs as D
import descubre_P7 as X, nace_P7_23 as N, nace_P7_33 as N33
ON = os.environ.get("GEMV_P7_54", "0") == "1"
ESCALA = {"cuerpo": 25.0, "recursos": 1.0, "vinculo": 1.0}; VENT = 240; ETA = 0.3; C0 = 0.5
FILAS = {("cuerpo", 1): "INVITACION-CUERPO", ("cuerpo", -1): "INVITACION-CUERPO-", ("recursos", 1): "INVITACION-RECURSOS", ("recursos", -1): "INVITACION-RECURSOS-", ("vinculo", 1): "INVITACION-VINCULO", ("vinculo", -1): "INVITACION-VINCULO-"}
REPARTO = {"cuerpo": (0.8, 0.1, 0.1), "recursos": (0.1, 0.8, 0.1), "vinculo": (0.1, 0.1, 0.8)}
E = {"inv": [], "conf": {"cuerpo": C0, "recursos": C0, "vinculo": C0}, "slot": None, "registra": None, "cands": [], "idx": 0, "match": {}, "activas": [], "pos_hist": [], "abiertas": [], "n": {"activas_tics": 0, "aceptadas": 0, "evaluadas": 0, "fotos_con_fila": 0}, "ya_activa": set(), "mundo": None, "W": None, "B": None}


def candidato_de(inv, n, r, mundo, hermana_cerca):
    a = inv["accion"]
    if a == "USAR_BOTIQUIN": return n == "usar_botiquin"
    if a == "USAR_RACION": return n == "usar_racion"
    if a.startswith("COGER_"):
        obj = {"COGER_BOTIQUIN": X.kit(mundo), "COGER_RACION": N.racion(mundo), "COGER_RED": N33.red(mundo), "COGER_CAMUFLAJE": N33.camo(mundo)}[a]
        if n == "coger": return ((r.get("item") or {}).get("id") == obj)
        if n in ("ir_objeto", "ir_curioso"): rec = r.get("recoger") or (None,); return rec[0] == obj
        return False
    if a == "EMPUNAR_RED": return n == f"empunar_{N33.red(mundo)}"
    if a == "PONERSE_CAMUFLAJE": return n == f"ponerse_{N33.camo(mundo)}"
    if a == "DAR_BOTIQUIN_HERMANA": return n == f"soltar_{X.kit(mundo)}" and hermana_cerca
    if a == "ACERCARSE_HERMANA": return n == "ir_pareja"
    if a == "QUEDARSE_QUIETA": return n == "noop"
    return False


def situacion(self, obs, mundo, tick):
    you = obs.get("you") or {}; pos = tuple(you.get("pos") or (0, 0)); z = obs.get("zone") or you.get("zone") or {}
    c = tuple(z.get("center") or (24, 24)); dentro = (math.dist(pos, c) <= float(z.get("radius") or 99)) if z else True
    pel = N33.peligro_de(self, obs); calma = bool(pel.get("calma"))
    E["pos_hist"].append(pos); E["pos_hist"] = E["pos_hist"][-25:]; quieta = len(E["pos_hist"]) >= 25 and all(p == pos for p in E["pos_hist"])
    ag = next((a for a in ((obs.get("visible") or {}).get("agents") or []) if a.get("slot") == mundo.teammate_slot and a.get("pos")), None)
    d = max(abs(ag["pos"][0] - pos[0]), abs(ag["pos"][1] - pos[1])) if ag else None
    if d is None:
        mem = getattr(self, "mem", None); pp = getattr(mem, "pareja_pos", None)
        if pp: d = max(abs(pp[0] - pos[0]), abs(pp[1] - pos[1]))
    cerca = (d is not None and d <= 4)
    return {"anillo": "DENTRO" if dentro else "FUERA", "calma": "CALMA" if calma else "PELIGRO", "movimiento": "QUIETA" if quieta else "MOVIENDOSE", "hermana": "CERCA" if cerca else "LEJOS", "cerca2": (d is not None and d <= 2)}


def cumple(inv, s): return all(inv.get(k, "CUALQUIERA") in ("CUALQUIERA", s[k]) for k in ("anillo", "calma", "movimiento", "hermana"))


def aplica(clase, registra=None):
    if not ON: return {"P7_54": False}
    E["registra"] = registra
    for k in FILAS.values():
        if k not in A.REPARTO: A.REPARTO[k] = REPARTO[k.split("-")[1].lower()]
    A.APETITIVAS |= {k for k in FILAS.values() if not k.endswith("-")}
    _oa = X.arranca
    def arranca(criatura, ruta, registra_=None):
        E["slot"] = int(criatura); c = _oa(criatura, ruta, registra_); d = os.path.dirname(os.path.abspath(ruta)) if ruta else None; f = os.path.join(d, f"invitaciones_P7_{criatura}.json") if d else None
        E["inv"] = []
        if f and os.path.exists(f):
            try: E["inv"] = [i for i in json.load(open(f)) if i.get("accion")]
            except Exception: E["inv"] = []
        for k, i in enumerate(E["inv"]): i["_k"] = k
        try: E["conf"] = dict(E["conf"], **((json.load(open(ruta)).get("confianza_razon_P7_54") or {}) if ruta and os.path.exists(ruta) else {}))
        except Exception: pass
        if c is not None:
            _v0 = c.volcado
            def volcado(_v0=_v0):
                dd = _v0(); dd["confianza_razon_P7_54"] = {k: round(v, 4) for k, v in E["conf"].items()}; dd["P7_54"] = dict(E["n"]); return dd
            c.volcado = volcado
        if registra_: registra_({"k": "P7_54_arranque", "slot": E["slot"], "invitaciones": len(E["inv"]), "confianza": dict(E["conf"]), "acciones": [i["accion"] for i in E["inv"]]})
        return c
    X.arranca = arranca
    _oc = D.candidatos
    def _cands(obs, mundo, mem, tick, bloqueos=None):
        out = _oc(obs, mundo, mem, tick, bloqueos); E["cands"] = [n for n, _ in out]; E["idx"] = 0; E["match"] = {}
        for i, (n, r) in enumerate(out):
            for inv in E["activas"]:
                if candidato_de(inv, n, r, mundo, E.get("cerca2", False)): E["match"][i] = inv; break
        return out
    D.candidatos = _cands
    _oo = D._obs_prevista
    def _obs_prevista(obs, mundo, mem, tick_eval, pos, hp, pack, hand, ver_pareja, golpe=None, suelta=None, body=False):
        ob2 = _oo(obs, mundo, mem, tick_eval, pos, hp, pack, hand, ver_pareja, golpe, suelta, body); i = E["idx"]; E["idx"] = i + 1
        inv = E["match"].get(i)
        if inv is not None: ob2["you"]["_P54_invitacion"] = inv
        return ob2
    D._obs_prevista = _obs_prevista
    _of = A.filas
    def filas(obs, mundo, mem, tick):
        F = _of(obs, mundo, mem, tick); inv = (obs.get("you") or {}).get("_P54_invitacion")
        if inv:
            E["n"]["fotos_con_fila"] += 1
            for dim in ("cuerpo", "recursos", "vinculo"):
                v = float(inv.get(dim) or 0.0)
                if v == 0.0: continue
                F[FILAS[(dim, 1 if v > 0 else -1)]] = min(1.0, abs(v) * float(E["conf"][dim]) / ESCALA[dim])
        return F
    A.filas = filas
    _od = clase.decidir
    def decidir(self, obs, _d=_od):
        mundo = self.mundo; tick = getattr(self, "tick", 0); E["mundo"] = mundo
        if mundo is not None and getattr(self, "phase", None) == "live" and E["inv"]:
            s = situacion(self, obs, mundo, tick); E["cerca2"] = s["cerca2"]; E["activas"] = [i for i in E["inv"] if cumple(i, s)]
            for i in E["activas"]:
                if i["_k"] not in E["ya_activa"]:
                    E["ya_activa"].add(i["_k"])
                    if registra: registra({"k": "P7_54_activa", "tick": tick, "n": i["_k"], "accion": i["accion"], "situacion": {k: s[k] for k in ("anillo", "calma", "movimiento", "hermana")}})
            if E["activas"]: E["n"]["activas_tics"] += 1
        else: E["activas"] = []
        n0 = len(X.ESTADO.get("huellas") or [])
        accion, radio = _d(self, obs)
        if radio is None or mundo is None or getattr(self, "phase", None) != "live": return accion, radio
        you = obs.get("you") or {}; hp = float(you.get("hp") or 0.0); ah = (radio.get("ahora") or {}); W = ah.get("W"); B = ah.get("B"); el = str(radio.get("elegido") or "")
        # aceptada: el elegido es el candidato de una invitacion activa
        if E["activas"] and el in E["cands"]:
            i = E["cands"].index(el); inv = E["match"].get(i)
            if inv is not None and not any(a["inv"]["_k"] == inv["_k"] for a in E["abiertas"]):
                E["abiertas"].append({"inv": inv, "t0": tick, "hp0": hp, "W0": W, "B0": B, "objeto": {"USAR_BOTIQUIN": X.kit(mundo), "COGER_BOTIQUIN": X.kit(mundo), "DAR_BOTIQUIN_HERMANA": None, "USAR_RACION": N.racion(mundo), "COGER_RACION": N.racion(mundo), "COGER_RED": N33.red(mundo), "EMPUNAR_RED": N33.red(mundo), "COGER_CAMUFLAJE": N33.camo(mundo), "PONERSE_CAMUFLAJE": N33.camo(mundo)}.get(inv["accion"]), "n_huellas0": n0}); E["n"]["aceptadas"] += 1
                if registra: registra({"k": "P7_54_aceptada", "tick": tick, "n": inv["_k"], "accion": inv["accion"], "elegido": el, "confianza": dict(E["conf"])})
        # evaluadas
        queda = []
        for a in E["abiertas"]:
            viv = None
            if a["objeto"]:
                h = next((h for h in (X.ESTADO.get("huellas") or [])[a["n_huellas0"]:] if (h.get("objeto") or X.kit(mundo)) == a["objeto"] and not h.get("corte")), None)
                if h: ef = h.get("efecto") or {}; viv = {"cuerpo": float(ef.get("cuerpo") or 0.0), "recursos": float(ef.get("recursos") or 0.0), "vinculo": float(ef.get("vinculo") or 0.0)}; fuente = "huella"
                elif tick - a["t0"] >= 2 * VENT: viv = {"cuerpo": hp - a["hp0"], "recursos": (float(W) - float(a["W0"])) if (W is not None and a["W0"] is not None) else 0.0, "vinculo": (float(B) - float(a["B0"])) if (B is not None and a["B0"] is not None) else 0.0}; fuente = "sin huella (480 tics)"
            elif tick - a["t0"] >= VENT: viv = {"cuerpo": hp - a["hp0"], "recursos": (float(W) - float(a["W0"])) if (W is not None and a["W0"] is not None) else 0.0, "vinculo": (float(B) - float(a["B0"])) if (B is not None and a["B0"] is not None) else 0.0}; fuente = "ventana de 240 tics"
            if viv is None: queda.append(a); continue
            antes = dict(E["conf"]); ac = {}
            for dim in ("cuerpo", "recursos", "vinculo"):
                p = float(a["inv"].get(dim) or 0.0); v = viv[dim]
                if abs(p) < 1e-9 and abs(v) < 1.0: ac[dim] = 1
                elif abs(p) < 1e-9: ac[dim] = 0
                else: ac[dim] = 1 if (p > 0) == (v > 0) and abs(v) >= abs(p) / 2 else 0
                E["conf"][dim] = (1 - ETA) * E["conf"][dim] + ETA * ac[dim]
            E["n"]["evaluadas"] += 1
            if registra: registra({"k": "P7_54_evaluada", "tick": tick, "n": a["inv"]["_k"], "accion": a["inv"]["accion"], "fuente": fuente, "prometido": {d_: a["inv"].get(d_) for d_ in ("cuerpo", "recursos", "vinculo")}, "vivido": {k: round(v, 3) for k, v in viv.items()}, "acierto": ac, "confianza_antes": antes, "confianza_despues": dict(E["conf"])})
        E["abiertas"] = queda
        return accion, radio
    clase.decidir = decidir
    _ot = X.termina
    def termina(registra_=None):
        if registra_: registra_({"k": "P7_54_cierre", "slot": E["slot"], "n": dict(E["n"]), "confianza": dict(E["conf"]), "pendientes": len(E["abiertas"])})
        return _ot(registra_)
    X.termina = termina
    return {"P7_54": True, "filas": list(FILAS.values())}

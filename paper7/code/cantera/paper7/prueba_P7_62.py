"""[P7-62] PRUEBAS CON CASOS CONSTRUIDOS A MANO del juicio arreglado (juicio_P7_62), antes de nada. Sin plataforma, sin API.
  0. el mundo: use_ticks del botiquin y de la racion leidos del catalogo (regla de Ari, 7-oct: el golpe interrumpe solo la canalizacion del botiquin).
  1. golpe en la canalizacion del botiquin -> cortada -> fallo en el momento (aunque luego venga una cura buena, aunque la huella no lleve marca); golpe fuera de la canalizacion -> no;
     marca de corte sin golpe -> no juzga, juzga el siguiente uso; la racion no se corta por un golpe.
  2. casi sana sin golpe -> juicio por el hueco (min(promesa, 100 - vida al empezar)); entera -> acierto si no baja; la racion igual; un uso de antes de aceptar no cuenta;
     sin uso en 480 tics -> cambio de vida contra el hueco.
  3. recuerdo de la hermana en calma -> no entra en el contraste de la falsa (si en el de una honesta); en amenaza -> si; visto o sin amenaza apuntada -> no.
  4. la amenaza viaja: M7 con amenaza ida y vuelta (mismo largo), M7 de antes (0/1) se lee sin amenaza; noche: la amenaza sale del cuaderno de la hermana; lo vivido la apunta.
  python3 prueba_P7_62.py   (sale 0 si pasan todas)"""
import json, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
os.environ["GEMV_P7_62"] = "1"
import juicio_P7_62 as J, invita_P7_54 as IN, invita_P7_57 as IC, mentira_P7_57 as MT, hermanas_P7_48 as HE, nace_P7_23 as N
OK = []; MAL = []
def caso(nombre, cond, detalle=""):
    (OK if cond else MAL).append(nombre); print(("PASA " if cond else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))

FALSA = dict(MT.FALSA, _k=0); RACION = {"_k": 1, "accion": "USAR_RACION", "cuerpo": 15.0, "recursos": -1.0, "vinculo": 0.0, "amenaza": "CUALQUIERA"}
def ab(inv, t0=100, hp0=60.0, objeto="first_aid"): return {"inv": inv, "t0": t0, "hp0": hp0, "W0": 3.0, "B0": 1.0, "objeto": objeto, "n_huellas0": 0}
def hu(t0, cuerpo, hp0, corte=False, dano=0.0, objeto="first_aid"): return {"objeto": objeto, "t0": t0, "corte": corte, "dano_total": dano, "hp0": hp0, "efecto": {"cuerpo": cuerpo, "recursos": -1.0, "vinculo": 0.0}}

# el mundo: use_ticks del catalogo del player_config (leido de un diario de P7-61, no cableado) y la regla de Ari (el dano interrumpe solo el botiquin)
import glob, re as _re
_f = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P757_s1_d1_MIENTEN_DOS_*", "*policy_agent_10.art.log")))[0]
_cat = next(json.loads(l) for l in open(_f, errors="replace") if l.startswith('{"k":"catalogo"'))
CANAL = {it["id"]: int(it.get("use_ticks") or 0) for it in _cat["items"]}; INT = {"first_aid"}; K = CANAL["first_aid"]; RC = CANAL["rations"]
caso("0 el mundo: botiquin canaliza 2 s, racion 1 s (use_ticks del catalogo)", K == 48 and RC == 24, (K, RC))
def J_(a, hs, tick, hp, golpes=()): return J.juicio(a, hs, tick, hp, 2.0, 1.0, sorted(golpes), CANAL, INT)

# 1. cortada (regla del mundo: golpe en la canalizacion del botiquin)
r = J_(ab(FALSA), [hu(102, 0.0, 60.0, corte=True, dano=12.0)], 110, 48.0, golpes=[110])
caso("1a golpe en la canalizacion (t0+8) -> cortada -> fallo", r is not None and r[1]["cuerpo"] == 0 and r[2] == "cortada por golpe" and r[3]["golpe_en_canal"] == 8, r and (r[2], r[3]))
r = J_(ab(FALSA), [hu(102, 0.0, 60.0, corte=True, dano=12.0), hu(150, 40.0, 55.0)], 160, 95.0, golpes=[110])
caso("1b cortada y luego una cura buena (reintento) -> sigue siendo fallo (el primer uso decide)", r is not None and r[1]["cuerpo"] == 0 and r[2] == "cortada por golpe")
r = J_(ab(FALSA), [hu(102, 30.0, 60.0, corte=False)], 160, 90.0, golpes=[102 + K])
caso("1c golpe en el ultimo tic de la canalizacion (t0+use_ticks), aunque la huella no lleve marca de corte -> cortada", r is not None and r[2] == "cortada por golpe" and r[3]["marca_corte"] is False, r and r[3])
r = J_(ab(FALSA), [hu(102, 40.0, 55.0)], 200, 95.0, golpes=[102 + K + 1, 101])
caso("1d golpe justo antes de empezar y justo despues de la canalizacion -> no cortada; juzga el hueco (40 de 45 -> acierto)", r is not None and r[2] == "huella (hueco)" and r[1]["cuerpo"] == 1, r and (r[2], r[3]))
r = J_(ab(FALSA), [hu(102, 0.0, 60.0, corte=True, dano=0.0), hu(150, 40.0, 55.0)], 160, 95.0)
caso("1e marca de corte sin golpe en la canalizacion -> no juzga; juzga el siguiente uso (40 de hueco 45 -> acierto)", r is not None and r[1]["cuerpo"] == 1 and r[2] == "huella (hueco)" and r[3]["hueco"] == 45.0, r and r[3])
r = J_(ab(RACION, hp0=60.0, objeto="rations"), [hu(102, 15.0, 60.0, objeto="rations")], 140, 75.0, golpes=[105, 110])
caso("1f racion con golpes en su segundo de uso -> el dano no la interrumpe; juzga el hueco (+15 de 15 -> acierto)", r is not None and r[2] == "huella (hueco)" and r[1]["cuerpo"] == 1, r and (r[2], r[3]))
caso("1g recien aceptada, sin uso aun -> espera", J_(ab(FALSA), [], 120, 60.0) is None)

# 2. hueco
for nom, hp0, cura, esperado, hueco in (("2a casi sana (90): +10 cubre la mitad del hueco 10 -> acierto", 90.0, 10.0, 1, 10.0), ("2b casi sana (90): +3 < 5 -> fallo", 90.0, 3.0, 0, 10.0),
                                        ("2c herida (40): +20 < 25 -> fallo", 40.0, 20.0, 0, 50.0), ("2d herida (40): +30 >= 25 -> acierto", 40.0, 30.0, 1, 50.0), ("2e entera (100): +0 -> acierto (nada que curar)", 100.0, 0.0, 1, 0.0)):
    r = J_(ab(FALSA, hp0=hp0), [hu(102, cura, hp0)], 130, hp0 + cura)
    caso(nom, r is not None and r[1]["cuerpo"] == esperado and r[3]["hueco"] == hueco, r and (r[1]["cuerpo"], r[3]))
r = J_(ab(RACION, hp0=95.0, objeto="rations"), [hu(102, 5.0, 95.0, objeto="rations")], 130, 100.0)
caso("2f racion (promete 15) casi sana (95): +5 >= 2,5 -> acierto (toda cura, declarado)", r is not None and r[1]["cuerpo"] == 1 and r[3]["hueco"] == 5.0, r and r[3])
r = J_(ab(FALSA, t0=100), [hu(90, 50.0, 40.0), hu(105, 10.0, 60.0)], 130, 70.0)
caso("2g un uso empezado antes de aceptar no cuenta (juzga el de t105: +10 < 20 -> fallo)", r is not None and r[1]["cuerpo"] == 0 and r[3]["hp0"] == 60.0, r and r[3])
r = J_(ab(FALSA, hp0=92.0), [], 100 + 2 * IN.VENT, 98.0)
caso("2h sin uso en 480 tics: +6 contra el hueco 8 -> acierto", r is not None and r[1]["cuerpo"] == 1 and r[2] == "sin huella (480 tics)", r and (r[1], r[3]))

# 2j. [P7-63, 14-oct] la sombra: mientras P7-62 juzga una cura, invita_P7_54 la ve abierta (no la vuelve a aceptar) y nunca la juzga
IN.E["abiertas"] = [ab(FALSA)]; J.E["abiertas"] = []; J.mueve()
sh = IN.E["abiertas"]
caso("2j cura aceptada: pasa a P7-62 y en invita_P7_54 queda su sombra (misma invitacion: no se re-acepta)", len(J.E["abiertas"]) == 1 and len(sh) == 1 and sh[0].get("_sombra") and any(x["inv"]["_k"] == FALSA["_k"] for x in sh))
caso("2k la sombra no la puede juzgar invita_P7_54 (objeto que no existe, t0 en el futuro) y mueve() no la vuelve a mover", sh[0]["objeto"] not in ("first_aid", "rations") and 10 ** 6 - sh[0]["t0"] < 2 * IN.VENT and (J.mueve() or len(J.E["abiertas"]) == 1))
J.E["golpes"] = []; J.E["canal"] = CANAL; J.E["interrumpe"] = INT
X_ = __import__("descubre_P7"); X_.ESTADO["huellas"] = [hu(102, 40.0, 55.0)]; IN.E["conf"] = {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}; reg = []
J.evalua(130, 95.0, 2.0, 1.0, reg.append)
caso("2l juzgada la cura, su sombra sale de la lista de invita_P7_54 (se puede volver a aceptar)", len(reg) == 1 and not IN.E["abiertas"] and not J.E["abiertas"], (len(reg), IN.E["abiertas"]))

# 3. contraste
class Mundo: id_botiquin = "first_aid"
class Cuad:
    def __init__(self, recs): self.recs = recs
    def recuerdos(self): return [("first_aid", "dentro", r) for r in self.recs]
HONESTA = {"_k": 1, "accion": "USAR_BOTIQUIN", "cuerpo": 30.0, "recursos": -1.0, "vinculo": 0.0, "anillo": "CUALQUIERA", "calma": "CALMA"}
def contrasta(r):
    IN.E["inv"] = [FALSA, HONESTA]; IN.E["conf"] = {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}; IC.E["vistos"] = set(); reg = []
    J.contrasta(Cuad([r]), Mundo(), 500, reg.append); return reg
def rec(origen, amenaza, tick):
    r = {"origen": origen, "via": "canal", "dia": 3, "tick": tick, "dia_emisora": 3, "tick_emisora": tick, "efecto": {"cuerpo": 45.0}, "intensidad": 2.0, "al_menos": False, "corte": False, "contexto": {"dentro": True, "golpeado_48": False}}
    if amenaza is not None: r["contexto"]["amenaza"] = amenaza
    return r
g = contrasta(rec("contado", False, 1000))
caso("3a recuerdo de la hermana en CALMA: no entra en el contraste de la falsa (si en el de la honesta)", len(g) == 1 and g[0]["falsa"] is False and g[0]["invitaciones"] == [1], g and g[0]["invitaciones"])
g = contrasta(rec("contado", True, 2000))
caso("3b recuerdo de la hermana en AMENAZA: entra en el contraste de la falsa", len(g) == 1 and g[0]["falsa"] is True and 0 in g[0]["invitaciones"], g and g[0]["invitaciones"])
g = contrasta(rec("visto", True, 3000))
caso("3c un visto no trae la amenaza de la hermana: no entra en la falsa", len(g) == 1 and g[0]["falsa"] is False)
g = contrasta(rec("contado", None, 4000))
caso("3d contado sin amenaza apuntada: no entra en la falsa", len(g) == 1 and g[0]["falsa"] is False)

# 4. la amenaza viaja
cod, par = J._cod_parsea(HE)
r = {"dia": 5, "tick": 812, "_objeto": "first_aid", "_sit": "dentro", "contexto": {"dentro": True, "golpeado_48": True, "amenaza": True}, "efecto": {"cuerpo": 50.0, "recursos": -1.0, "vinculo": 0.0},
     "importancia": {"cuerpo": 0.5, "recursos": 0.1, "vinculo": 0.0}, "foto": {"dolor_F": 0.2, "dolor_R": 0.3, "dolor_S": 0.1, "positivo": 0.2, "d": 2.0}, "acciones": ["usar_botiquin"], "intensidad": 1.5, "al_menos": False}
t_viejo = HE.codifica(r, 10); t = cod(r, 10); p = par(t)
caso("4a M7 con amenaza: ida y vuelta, mismo largo, golpe intacto", p is not None and p["amenaza"] is True and p["golpeado_48"] is True and len(t) == len(t_viejo), t)
r["contexto"]["amenaza"] = False; p = par(cod(r, 10))
caso("4b M7 sin amenaza: amenaza False", p is not None and p["amenaza"] is False and p["golpeado_48"] is True)
p = par(t_viejo.replace(" bd1 ", " bd0 "))
caso("4c M7 del formato de antes (0/1): se lee, amenaza False", p is not None and p["amenaza"] is False)
d = tempfile.mkdtemp(); json.dump({"dia": 4, "objetos": {"first_aid": {"situaciones": {"dentro": [{"dia": 4, "tick": 700, "contexto": {"dentro": True, "golpeado_48": False, "amenaza": True}}]}}}}, open(os.path.join(d, "cuaderno_P7_11.json"), "w"))
HE.E["cuaderno_dir"] = d; HE.E["pareja"] = 11; J.E["hermana_cache"] = None
class C2:
    def __init__(self): self.o = {"first_aid": {"situaciones": {}}}
    def dia_actual(self): return 5
    def _obj(self, o): return self.o.setdefault(o, {"situaciones": {}})
pn = {"de": 11, "dia_emisora": 4, "tick_emisora": 700, "objeto": "first_aid", "situacion": "dentro", "golpeado_48": False, "efecto": {"cuerpo": 50.0, "recursos": -1.0, "vinculo": 0.0}, "importancia": {"cuerpo": 0.5, "recursos": 0.1, "vinculo": 0.0}, "foto": None, "acciones": [], "intensidad_emisora": 1.2, "al_menos": False}
am = J.amenaza_noche(pn, HE); am2 = J.amenaza_noche(dict(pn, tick_emisora=701), HE)
caso("4e noche: la amenaza del recuerdo sale del cuaderno de la hermana (y otro recuerdo no la inventa)", am is True and am2 is None, (am, am2))
N.E["ultimo_dano"] = 950; J.E["rival_fuego"] = False; J.E["amenaza_tic"] = 1000
caso("4f lo vivido: golpe hace 50 tics y sin rival -> sin amenaza; hace 40 -> amenaza", J.amenaza_ahora(1000) is False and J.amenaza_ahora(990) is True)
J.E["rival_fuego"] = True
caso("4g lo vivido: rival a <= 4 en este tic -> amenaza (solo en ese tic)", J.amenaza_ahora(1000) is True and J.amenaza_ahora(1001) is False)

print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_62_pruebas.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if MAL else 0)

"""[P7-63] PRUEBAS CON CASOS CONSTRUIDOS A MANO de la falsa de la racion (antes del sello). Sin plataforma, sin API.
  1. juicio (juicio_P7_62, regla del mundo; la cura de la racion leida del catalogo): vida 55 + racion 15 -> fallo; con golpes en su segundo de uso la racion no se corta.
  2. situacion: vida 65 -> la falsa no se activa; vida 55 -> si (lo demas de la situacion igual).
  3. contraste: recuerdo de racion de la hermana con vida 80 al empezar -> no entra en el contraste de la falsa; con vida 50 -> si; visto o sin apuntar -> no.
  4. la vida al empezar viaja: M7 0-7 ida y vuelta (con la amenaza de P7-62), M7 de P7-62 se lee con herida60 False; noche desde el cuaderno de la hermana; lo vivido la apunta.
  python3 prueba_P7_63.py   (sale 0 si pasan todas)"""
import glob, json, os, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
os.environ["GEMV_P7_62"] = "1"; os.environ["GEMV_P7_63"] = "1"
import juicio_P7_62 as J62, juicio_P7_63 as J, invita_P7_54 as IN, invita_P7_57 as IC, mentira_P7_63 as MT, hermanas_P7_48 as HE, nace_P7_23 as N
OK = []; MAL = []
def caso(nombre, cond, detalle=""):
    (OK if cond else MAL).append(nombre); print(("PASA " if cond else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))

_f = sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P757_s1_d1_MIENTEN_DOS_*", "*policy_agent_10.art.log")))[0]
_cat = next(json.loads(l) for l in open(_f, errors="replace") if l.startswith('{"k":"catalogo"'))
CANAL = {it["id"]: int(it.get("use_ticks") or 0) for it in _cat["items"]}; HEAL = {it["id"]: int(it.get("heal") or 0) for it in _cat["items"]}; INT = {"first_aid"}
caso("0 el mundo: la racion cura 15 y canaliza 1 s (catalogo)", HEAL["rations"] == 15 and CANAL["rations"] == 24, (HEAL["rations"], CANAL["rations"]))
FALSA = dict(MT.FALSA, _k=0)
def ab(hp0, t0=100): return {"inv": FALSA, "t0": t0, "hp0": hp0, "W0": 3.0, "B0": 1.0, "objeto": "rations", "n_huellas0": 0}
def hu(t0, cuerpo, hp0, corte=False): return {"objeto": "rations", "t0": t0, "corte": corte, "dano_total": 0.0, "hp0": hp0, "efecto": {"cuerpo": cuerpo, "recursos": -1.0, "vinculo": 0.0}}

# 1. juicio
r = J62.juicio(ab(55.0), [hu(101, float(HEAL["rations"]), 55.0)], 130, 70.0, 2.0, 1.0, [], CANAL, INT)
caso("1a vida 55 + racion 15 -> fallo (hueco 40, hace falta 20)", r is not None and r[1]["cuerpo"] == 0 and r[3]["hueco"] == 40.0 and r[2] == "huella (hueco)", r and (r[1], r[3]))
r = J62.juicio(ab(30.0), [hu(101, float(HEAL["rations"]), 30.0)], 130, 45.0, 2.0, 1.0, [105, 110, 118], CANAL, INT)
caso("1b vida 30 con golpes en el segundo de uso: la racion no se corta; +15 -> fallo por el hueco", r is not None and r[2] == "huella (hueco)" and r[1]["cuerpo"] == 0, r and (r[2], r[1]))
r = J62.juicio(ab(59.0), [hu(101, float(HEAL["rations"]), 59.0)], 130, 74.0, 2.0, 1.0, [], CANAL, INT)
caso("1c vida 59 (el borde) + 15 -> fallo (hueco 40: min(40, 41))", r is not None and r[1]["cuerpo"] == 0 and r[3]["hueco"] == 40.0, r and r[3])

# 2. situacion
base = {"anillo": "DENTRO", "calma": "CALMA", "movimiento": "QUIETA", "hermana": "LEJOS", "vida": "SANA", "amenaza": "SIN_AMENAZA"}
def activa(hp):
    s = dict(base, vida60=J.vida60(hp)); return J.cumple_vida(FALSA, s) and IN.cumple(dict(FALSA, vida="CUALQUIERA"), s)
caso("2a vida 65 -> la falsa no se activa", activa(65.0) is False)
caso("2b vida 55 -> la falsa se activa", activa(55.0) is True)
caso("2c vida 60 exacta -> no (vida < 60)", activa(60.0) is False)
caso("2d una honesta sin condicion de vida no cambia", J.cumple_vida({"accion": "USAR_RACION"}, dict(base, vida60="SANA_60")) is True)

# 3. contraste
class Mundo: id_botiquin = "first_aid"; id_raciones = ("rations",)
class Cuad:
    def __init__(self, recs): self.recs = recs
    def recuerdos(self): return [("rations", "dentro", r) for r in self.recs]
HONESTA = {"_k": 1, "accion": "USAR_RACION", "cuerpo": 15.0, "recursos": -1.0, "vinculo": 0.0, "anillo": "CUALQUIERA", "calma": "CUALQUIERA"}
def contrasta(r):
    IN.E["inv"] = [FALSA, HONESTA]; IN.E["conf"] = {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}; IC.E["vistos"] = set(); reg = []
    J.contrasta(Cuad([r]), Mundo(), 500, reg.append); return reg
def rec(origen, hp0, tick):
    r = {"origen": origen, "via": "canal", "dia": 3, "tick": tick, "dia_emisora": 3, "tick_emisora": tick, "efecto": {"cuerpo": 15.0}, "intensidad": 2.0, "al_menos": False, "corte": False, "contexto": {"dentro": True, "golpeado_48": False, "amenaza": False}}
    if hp0 is not None: r["contexto"]["herida60"] = hp0 < 60
    return r
g = contrasta(rec("contado", 80.0, 1000))
caso("3a racion de la hermana con vida 80 -> no entra en el contraste de la falsa (si en el de la honesta)", len(g) == 1 and g[0]["falsa"] is False and g[0]["invitaciones"] == [1], g and g[0]["invitaciones"])
g = contrasta(rec("contado", 50.0, 2000))
caso("3b racion de la hermana con vida 50 -> entra en el contraste de la falsa (y la desmiente: 15 < 20)", len(g) == 1 and g[0]["falsa"] is True and 0 in g[0]["invitaciones"] and g[0]["acierto"] < 1, g and (g[0]["invitaciones"], g[0]["acierto"]))
g = contrasta(rec("visto", 50.0, 3000))
caso("3c un visto (la vida es la de quien mira) -> no entra en la falsa", len(g) == 1 and g[0]["falsa"] is False)
g = contrasta(rec("contado", None, 4000))
caso("3d contado sin la vida apuntada -> no entra en la falsa", len(g) == 1 and g[0]["falsa"] is False)

# 4. la vida al empezar viaja
cod62, par62 = J62._cod_parsea(HE); cod, par = J._cod_parsea(HE, cod62, par62)
r = {"dia": 5, "tick": 812, "_objeto": "rations", "_sit": "dentro", "contexto": {"dentro": True, "golpeado_48": True, "amenaza": True, "herida60": True}, "efecto": {"cuerpo": 15.0, "recursos": -1.0, "vinculo": 0.0},
     "importancia": {"cuerpo": 0.5, "recursos": 0.1, "vinculo": 0.0}, "foto": {"dolor_F": 0.2, "dolor_R": 0.3, "dolor_S": 0.1, "positivo": 0.2, "d": 2.0}, "acciones": ["usar_racion"], "intensidad": 1.5, "al_menos": False}
t = cod(r, 10); p = par(t)
caso("4a M7 con golpe + amenaza + herida60: ida y vuelta, mismo largo", p is not None and p["herida60"] is True and p["amenaza"] is True and p["golpeado_48"] is True and len(t) == len(HE.codifica(r, 10)), t)
r["contexto"]["amenaza"] = False; p = par(cod(r, 10))
caso("4b herida60 sin amenaza", p is not None and p["herida60"] is True and p["amenaza"] is False)
p = par(cod62(r, 10))
caso("4c M7 de P7-62 (0-3) -> herida60 False", p is not None and p["herida60"] is False)
d = tempfile.mkdtemp(); json.dump({"dia": 4, "objetos": {"rations": {"situaciones": {"dentro": [{"dia": 4, "tick": 700, "contexto": {"dentro": True, "herida60": True}}]}}}}, open(os.path.join(d, "cuaderno_P7_11.json"), "w"))
HE.E["cuaderno_dir"] = d; HE.E["pareja"] = 11; J.E["hermana_cache"] = None
pn = {"objeto": "rations", "dia_emisora": 4, "tick_emisora": 700}
caso("4d noche: la vida al empezar sale del cuaderno de la hermana (y otro recuerdo no la inventa)", J.herida_noche(pn, HE) is True and J.herida_noche(dict(pn, tick_emisora=701), HE) is None)
caso("4e la falsa la anade el codigo desde las invitaciones del dia 8, solo en los asientos que mienten", MT.miente("MIENTEN_DOS", 11, 8) and MT.miente("MIENTE_UNA", 10, 8) and not MT.miente("MIENTE_UNA", 11, 8) and not MT.miente("MIENTEN_DOS", 10, 7))
L, pos = MT.anade([{"accion": "USAR_BOTIQUIN"}, {"accion": "COGER_RACION"}], 1, 7, 10)
caso("4f anade: una sola falsa, en la posicion fijada por la semilla", sum(1 for i in L if i.get("falsa")) == 1 and L[pos].get("falsa") and L[pos]["dia"] == 7)

print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_63_pruebas.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if MAL else 0)

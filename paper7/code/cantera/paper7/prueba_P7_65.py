"""[P7-65] PRUEBAS CON CASOS CONSTRUIDOS A MANO de la falsa del botiquin cogido (antes del sello). Sin plataforma, sin API.
  1. juicio (invita_P7_54, sin cambio; regla por dimension de P7-54 = juicio_P7_62.acierto_dim, comprobada en el texto): coger en amenaza y la vida no sube (0 en 480 tics) -> fallo;
     declarado: si en 480 tics usa el botiquin cogido sin golpe y cura >= 15, la confirma; juicio_P7_62 no se queda las de coger (solo las curas).
  2. situacion (la de invita_P7_57, aplicada de verdad sobre una clase de prueba): coger SIN amenaza -> la falsa no se activa; CON amenaza -> si.
  3. contraste (juicio_P7_65): recuerdo de botiquin de la hermana en calma -> no entra en la falsa; en amenaza -> TAMPOCO (decision de Manel, 15-oct: sin contraste para coger);
     una honesta de USAR_BOTIQUIN sigue contrastandose en su situacion.
  4. la falsa: la anade el codigo desde las invitaciones del dia 8 en los asientos que mienten; una sola, en su posicion.
  python3 prueba_P7_65.py   (sale 0 si pasan todas)"""
import inspect, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
for k in ("GEMV_P7_54", "GEMV_P7_57", "GEMV_P7_62", "GEMV_P7_65"): os.environ[k] = "1"
import invita_P7_54 as IN, invita_P7_57 as IC, juicio_P7_62 as J62, juicio_P7_65 as J, mentira_P7_65 as MT
OK = []; MAL = []
def caso(nombre, cond, detalle=""):
    (OK if cond else MAL).append(nombre); print(("PASA " if cond else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))
FALSA = dict(MT.FALSA, _k=0)

# 1. juicio
src = inspect.getsource(IN)
caso("1a la regla por dimension de invita_P7_54 es la de juicio_P7_62.acierto_dim (texto)", "ac[dim] = 1 if (p > 0) == (v > 0) and abs(v) >= abs(p) / 2 else 0" in src and "1 if (p > 0) == (v > 0) and abs(v) >= abs(p) / 2 else 0" in inspect.getsource(J62.acierto_dim))
caso("1b coger en amenaza, la vida no sube en 480 tics (0) -> fallo en el cuerpo", J62.acierto_dim(FALSA["cuerpo"], 0.0) == 0)
caso("1c coger y perder vida en 480 tics (-64) -> fallo", J62.acierto_dim(FALSA["cuerpo"], -64.0) == 0)
caso("1d declarado: usar el botiquin cogido sin golpe en 480 tics y curar 50 -> la confirma (la parte que no es «siempre»)", J62.acierto_dim(FALSA["cuerpo"], 50.0) == 1)
caso("1e recursos +1 prometido y +1 vivido -> acierto en recursos (la mentira esta solo en el cuerpo)", J62.acierto_dim(FALSA["recursos"], 1.0) == 1)
caso("1f juicio_P7_62 no se queda las invitaciones de coger (solo USAR_BOTIQUIN y USAR_RACION)", "COGER_BOTIQUIN" not in J62.CURAS)

# 2. situacion, con las piezas aplicadas de verdad
class Prueba:
    def decidir(self, obs): return None, None
IN.aplica(Prueba, None); IC.aplica(Prueba, None)
base = {"anillo": "DENTRO", "calma": "CALMA", "movimiento": "MOVIENDOSE", "hermana": "LEJOS", "vida": "SANA"}
caso("2a coger SIN amenaza -> la falsa no se activa", IN.cumple(FALSA, dict(base, amenaza="SIN_AMENAZA")) is False)
caso("2b coger CON amenaza (rival a <= 4, fuego o golpe en 48 tics) -> se activa", IN.cumple(FALSA, dict(base, amenaza="AMENAZA")) is True)
caso("2c una honesta de coger sin condicion de amenaza se activa en las dos", IN.cumple({"accion": "COGER_BOTIQUIN"}, dict(base, amenaza="SIN_AMENAZA")) and IN.cumple({"accion": "COGER_BOTIQUIN"}, dict(base, amenaza="AMENAZA")))

# 3. contraste
J.aplica(Prueba, None)
class Mundo: id_botiquin = "first_aid"
class Cuad:
    def __init__(self, recs): self.recs = recs
    def recuerdos(self): return [("first_aid", "dentro", r) for r in self.recs]
HONESTA = {"_k": 1, "accion": "USAR_BOTIQUIN", "cuerpo": 30.0, "recursos": -1.0, "vinculo": 0.0, "amenaza": "CUALQUIERA"}
def contrasta(r, invs):
    IN.E["inv"] = invs; IN.E["conf"] = {"cuerpo": 0.5, "recursos": 0.5, "vinculo": 0.5}; IC.E["vistos"] = set(); reg = []
    IC.contrasta(Cuad([r]), Mundo(), 500, reg.append); return reg, IN.E["inv"]
def rec(amenaza, tick):
    return {"origen": "contado", "via": "canal", "dia": 3, "tick": tick, "dia_emisora": 3, "tick_emisora": tick, "efecto": {"cuerpo": 40.0}, "intensidad": 2.0, "al_menos": False, "corte": False, "contexto": {"dentro": True, "golpeado_48": amenaza, "amenaza": amenaza}}
caso("3a la que se usa es la de juicio_P7_65 (IC.contrasta sustituida por fuera)", IC.contrasta is J.contrasta)
g, inv = contrasta(rec(False, 1000), [FALSA])
caso("3b recuerdo de botiquin de la hermana en CALMA -> no entra en la falsa", g == [] and inv == [FALSA])
g, inv = contrasta(rec(True, 2000), [FALSA])
caso("3c en AMENAZA -> tampoco (sin contraste para coger; decision de Manel)", g == [] and inv == [FALSA])
g, inv = contrasta(rec(True, 3000), [FALSA, HONESTA])
caso("3d una honesta de USAR_BOTIQUIN sigue contrastandose; la falsa no", len(g) == 1 and g[0]["invitaciones"] == [1] and g[0]["falsa"] is False and inv == [FALSA, HONESTA], g and g[0]["invitaciones"])

# 4. la falsa
caso("4a desde las invitaciones del dia 8, solo en los asientos que mienten", MT.miente("MIENTEN_DOS", 11, 8) and MT.miente("MIENTE_UNA", 10, 8) and not MT.miente("MIENTE_UNA", 11, 8) and not MT.miente("MIENTEN_DOS", 10, 7))
L, pos = MT.anade([{"accion": "USAR_BOTIQUIN"}, {"accion": "COGER_RACION"}], 1, 7, 10)
caso("4b una sola falsa (COGER_BOTIQUIN, amenaza, +30), en su posicion", sum(1 for i in L if i.get("falsa")) == 1 and L[pos]["accion"] == "COGER_BOTIQUIN" and L[pos]["amenaza"] == "AMENAZA" and L[pos]["cuerpo"] == 30.0)

print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_65_pruebas.json"), "w"), ensure_ascii=False, indent=1)
sys.exit(1 if MAL else 0)

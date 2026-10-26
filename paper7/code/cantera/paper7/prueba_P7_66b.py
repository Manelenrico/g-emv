"""[P7-66, segundo banco] PRUEBAS A MANO de invita_P7_66b (lo que cambia respecto a invita_P7_66). python3 prueba_P7_66b.py"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, "paintball"), os.path.join(RAIZ, "cantera", "paper6"), RAIZ]
os.environ["GEMV_P7_54"] = "1"; os.environ["GEMV_P7_66"] = "1"
import invita_P7_66b as J
OK = []; MAL = []
def caso(n, c, d=""): (OK if c else MAL).append(n); print(("PASA " if c else "FALLA") + " · " + n + (f" · {d}" if d else ""))
INV = {"_k": 0, "accion": "IR_A_SITIO", "destino": [3, 1]}
caso("1a en el tramo (tic0 + 100), destino a 12 de ella y a 10 de su hermana -> empuja", J.puede_empujar(INV, 341, 241, (13, 13), (13, 9), set()))
caso("1b fuera del tramo (tic0 + 300) -> no empuja", not J.puede_empujar(INV, 541, 241, (13, 13), (13, 9), set()))
caso("1c destino a 7 de ella -> no", not J.puede_empujar(INV, 341, 241, (10, 5), (13, 13), set()))
caso("1d destino a 16 de ella -> no", not J.puede_empujar(INV, 341, 241, (19, 17), (13, 13), set()))
caso("1e su hermana a 6 del destino -> no", not J.puede_empujar(INV, 341, 241, (13, 13), (9, 1), set()))
caso("1f sin saber donde esta su hermana -> decide por ella sola", J.puede_empujar(INV, 341, 241, (13, 13), None, set()))
caso("1g ya llego a ese destino hoy -> no vuelve a empujar", not J.puede_empujar(INV, 341, 241, (13, 13), None, {(0, (3, 1))}))
a = {"inv": INV, "t0": 300, "destino": (3, 1)}
caso("2a rival a 4 -> sigue (la interrupcion es a <= 3)", J.juicio(a, 350, (10, 5), 4, []) is None)
caso("2b rival a 3 -> interrumpida", J.juicio(a, 350, (10, 5), 3, []) == ("interrumpida", None))
caso("2c llega sin botiquin -> falla en el acto", J.juicio(a, 350, (4, 1), None, []) == ("llegada", 0))
src = open(os.path.join(AQUI, "invita_P7_66b.py")).read()
caso("3a tras llegar, el destino queda apuntado para no volver a empujar ese dia", 'E["llegados"].add((a["inv"]["_k"], tuple(a["destino"])))' in src)
print(f"\n{len(OK)} pasan, {len(MAL)} fallan" + (f": {MAL}" if MAL else ""))
json.dump({"pasan": OK, "fallan": MAL}, open(os.path.join(AQUI, "P7_66b_pruebas.json"), "w"), ensure_ascii=False, indent=1); sys.exit(1 if MAL else 0)

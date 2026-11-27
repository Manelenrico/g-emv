"""[P8] Prompt 96: los dos hechos ciertos del árbol de fruta dulce (valle/mundo.py, _arboles_inicia y _arbol_de_bestia; config_valle.json → arbol_dulce), como
entradas de cultura. Solo son verdad en un mundo con el árbol encendido (apagado por defecto). No dicen dónde ni cuándo: eso se descubre viéndolo.
   python3 cultura_hechos_v50.py -> cultura_hechos_v50.json"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
A = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8"))["arbol_dulce"]
E = [{"rueda": "arbol_dulce", "dice": "a veces aparece un árbol de fruta dulce lejos", "objeto": "hecho:arbol_dulce", "situaciones": ["valle"], "efecto": {},
      "numeros": {"frutos": A["frutos"], "dura_dias": A["dura_dias"]}, "de": "mundo.py _arboles_inicia, _arboles_avanza"},
     {"rueda": "arbol_dulce", "dice": "al atardecer la bestia pasa por los árboles dulces; de noche va a la aldea como siempre", "objeto": "hecho:bestia_arbol", "situaciones": ["noche"], "efecto": {},
      "numeros": {"fases": A.get("bestia_fases")}, "de": "mundo.py _arbol_de_bestia (prompt 97: solo al atardecer)"}]
json.dump({"_que_es": "hechos del árbol de fruta dulce (prompt 96), de cultura_hechos_v50.py; verdad solo con arbol_dulce encendido; RG50r los carga", "entradas": E},
          open(os.path.join(AQUI, "cultura_hechos_v50.json"), "w"), ensure_ascii=False, indent=1)
print(len(E))

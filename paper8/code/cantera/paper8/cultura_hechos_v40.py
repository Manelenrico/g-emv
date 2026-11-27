"""[P8] Prompt 85, pieza F: los hechos del mundo que protegen a la que está acompañada, leídos del código del mundo (valle/mundo.py) y con sus números de la
config del mundo (importados, no copiados), escritos como entradas de cultura. Solo reglas del mundo de verdad:
  1. _encuentros: la bestia, con varias pegadas a ella (fuera de casa), ataca a una sola, a suertes: con n pegadas, a cada una le toca 1/n;
  2. _empuja (entre criaturas): gana el bando mayor (ella más las de su misma casa pegadas a la escena); si empatan, la menos cansada; la que pierde suelta
     lo que lleva;
  3. _empuja (a la bestia): gana si hay al menos peso_empuje criaturas pegadas a la bestia; entonces suelta lo que robó; si pierde, le pega (golpe_dano).
   python3 cultura_hechos_v40.py -> cultura_hechos_v40.json"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
C = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); B = C["bestia"]
E = [{"dice": "la bestia, con varias pegadas a ella fuera de casa, ataca a una sola a suertes: con otra al lado, a cada una le toca la mitad de las veces",
      "objeto": "hecho:bestia_ataca_a_una", "situaciones": ["acompanada"], "efecto": {"cuerpo": 0.5}, "numeros": {"con_n_pegadas_le_toca": "1/n"}, "de": "mundo.py _encuentros"},
     {"dice": "un empujón entre criaturas lo gana el bando mayor (ella y las de su casa pegadas a la escena); si empatan, la menos cansada; la que pierde suelta lo que lleva",
      "objeto": "hecho:empujon_bando", "situaciones": ["acompanada"], "efecto": {"recursos": 1.0}, "numeros": {"bando": "1 + las de su casa pegadas a la escena"}, "de": "mundo.py _empuja"},
     {"dice": f"empujar a la bestia sale bien con al menos {B['peso_empuje']} criaturas pegadas a ella: suelta lo que robó; si no, le pega ({B['golpe_dano']} de vida)",
      "objeto": "hecho:empujar_bestia", "situaciones": ["acompanada"], "efecto": {"recursos": 1.0, "cuerpo": -float(B["golpe_dano"])},
      "numeros": {"peso_empuje": B["peso_empuje"], "golpe_dano": B["golpe_dano"]}, "de": "mundo.py _empuja (bestia)"}]
json.dump({"_que_es": "hechos del mundo que protegen a la que está acompañada (prompt 85, pieza F), de cultura_hechos_v40.py; hoy se apuntan en el cuaderno y no los lee nada", "entradas": E},
          open(os.path.join(AQUI, "cultura_hechos_v40.json"), "w"), ensure_ascii=False, indent=1)
print(len(E))

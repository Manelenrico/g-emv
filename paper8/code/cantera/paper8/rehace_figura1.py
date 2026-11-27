"""[P8, prompt 183] Rehace la figura 1 (el valle) sin las partidas completas. El programa de la figura, figura1_valle_171.py, no se toca: el mapa
(valle_mapa.py:15) lee una sola línea de una partida, el turno 0 de la criatura completa en sequía, semilla 30182, y la busca en la carpeta
de las partidas (evalua_experimento_v6.CARPETA). Este programa apunta esa carpeta a figura1_turno0/, que trae solo esa línea, y lanza el
programa de la figura tal cual.
   python3 rehace_figura1.py --idioma es|en   (desde esta carpeta, con data/paper8/ copiada dentro) -> figuras_171/fig1_valle_<idioma>.png y .pdf"""
import os, runpy, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI); os.chdir(AQUI)
ARGS = sys.argv[1:]
os.environ["ESCALERA_MODO"] = "experimento"                    # (como lo pone valle_mapa.py antes de importar el evaluador de la escalera)
import evalua_escalera_v6 as ES                                 # (al importarse vacía sys.argv: por eso los argumentos se guardan antes)
ES.E6.CARPETA[ES.PROTA] = os.path.join(AQUI, "figura1_turno0")
sys.argv = ["figura1_valle_171.py"] + ARGS
runpy.run_path(os.path.join(AQUI, "figura1_valle_171.py"), run_name="__main__")

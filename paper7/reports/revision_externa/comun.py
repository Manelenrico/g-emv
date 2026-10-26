"""Rutas comunes de los guiones de la revision externa (solo lectura). Relativas a este archivo: nada cableado a mano."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
P7 = os.path.dirname(AQUI)                                   # cantera/paper7
RAIZ = os.path.dirname(os.path.dirname(P7))                  # raiz del repositorio
RUNS = os.path.join(RAIZ, "paintball", "runs")
sys.dont_write_bytecode = True
def sal(nombre): return os.path.join(AQUI, nombre)           # salidas, solo en esta carpeta

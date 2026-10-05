#!/bin/zsh
# [P6-30] la cadena de P6-25 -> P6-26 y la de P6-28, sin llamar al modelo, en esta carpeta
cd "$(dirname "$0")"
set -x
python3 juez_P6_25.py oraculo --hilos 4
python3 juez_P6_25.py primera --hilos 4
python3 juez_P6_25.py retraso primera --hilos 4
python3 juez_P6_25.py bucle2 --hilos 4
python3 juez_P6_25.py bucle3 --hilos 4
python3 juez_P6_25.py pareja --hilos 4
python3 mide_P6_25.py
python3 banco_P6_28.py --instantaneas --hilos 4
python3 banco_P6_28.py --reenlaza
python3 banco_P6_28.py --prevision
python3 banco_P6_28.py --juzga --hilos 4
python3 banco_P6_28.py --mide
python3 banco_P6_26.py --hilos 4
echo CADENA_FIN

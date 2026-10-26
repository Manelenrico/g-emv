#!/bin/sh
# [P7-34] EL CAMPO DE LO INUTIL, de una vez y con frenos: cada paso sigue solo si el anterior acabo con codigo 0 (se mira el codigo del propio lanzador, no el de un
# `grep`: la leccion de P7-30). Orden: freno (APRENDE s1 d1-3) -> freno_P7_34.py PASA -> serie 1 (APRENDE d4-20 en cadena, BORRADO y TECHO d1-20 a la vez) ->
# serie 2 (igual, d1-20). Registros en _P7_34_*.log. Uso: nohup sh corre_P7_34.sh > _P7_34_corre.log 2>&1 &
cd "$(dirname "$0")" || exit 1
echo "[$(date)] imagenes fijas (BORRADO, TECHO): se hornean y suben antes de pedir nada"
python3 lanza_P7_34.py --construye-fijos > _P7_34_construye_fijos.log 2>&1; rc=$?
if [ $rc -ne 0 ]; then echo "[$(date)] el horneado de las fijas fallo con codigo $rc: PARADO"; exit 6; fi
echo "[$(date)] freno: APRENDE s1 d1-3"
python3 lanza_P7_34.py --cadena-aprende 1 1 3 > _P7_34_cadena_s1_freno.log 2>&1; rc=$?
if [ $rc -ne 0 ]; then echo "[$(date)] la cadena del freno paro con codigo $rc: PARADO"; exit 7; fi
python3 freno_P7_34.py > _P7_34_freno.log 2>&1
if ! grep -q '"FRENO": "PASA"' P7_34_freno.json; then echo "[$(date)] FRENO NO PASA (P7_34_freno.json): PARADO"; exit 8; fi
echo "[$(date)] freno PASA"
for S in 1 2; do
  if [ $S -eq 1 ]; then D1=4; else D1=1; fi
  echo "[$(date)] serie $S: fijos d1-20 y cadena APRENDE d$D1-20"
  ( python3 lanza_P7_34.py --fijos $S 1 20 > _P7_34_fijos_s$S.log 2>&1; echo $? > _P7_34_fijos_s$S.rc ) &
  python3 lanza_P7_34.py --cadena-aprende $S $D1 20 > _P7_34_cadena_s$S.log 2>&1; rc=$?
  wait
  rcf=$(cat _P7_34_fijos_s$S.rc 2>/dev/null || echo 99)
  if [ $rc -ne 0 ] || [ "$rcf" -ne 0 ]; then echo "[$(date)] serie $S: cadena $rc, fijos $rcf: PARADO"; exit 7; fi
  echo "[$(date)] serie $S completa"
done
echo "[$(date)] CAMPO COMPLETO"

#!/bin/sh
# [P7-42] EL CAMPO DEL CAPITULO 3, de una vez y con frenos (molde de corre_P7_34.sh): humo (dia 1 de APRENDE_p, SIN y TECHO, serie 1) -> freno (APRENDE_p s1 d1-3)
# -> freno_P7_42.py PASA -> por serie: las 4 cadenas (APRENDE_v, APRENDE_p, SIN) y las fijas (TECHO, BORRADO_v, BORRADO_p) a la vez -> series 1, 2, 3 una detras de otra.
# Cada paso sigue solo si el anterior acabo con codigo 0. Uso: nohup sh corre_P7_42.sh > _P7_42_corre.log 2>&1 &
cd "$(dirname "$0")" || exit 1
echo "[$(date)] humo: dia 1 de APRENDE_p, SIN y TECHO (serie 1)"
python3 lanza_P7_41.py --cadena APRENDE_p 1 1 1 > _P7_42_humo_APRENDE_p.log 2>&1; rc1=$?
python3 lanza_P7_41.py --cadena SIN 1 1 1 > _P7_42_humo_SIN.log 2>&1; rc2=$?
python3 lanza_P7_41.py --lanza 1 1 TECHO > _P7_42_humo_TECHO.log 2>&1 && python3 lanza_P7_41.py --recoge --hasta >> _P7_42_humo_TECHO.log 2>&1; rc3=$?
if [ $rc1 -ne 0 ] || [ $rc2 -ne 0 ] || [ $rc3 -ne 0 ]; then echo "[$(date)] HUMO: APRENDE_p $rc1, SIN $rc2, TECHO $rc3: PARADO"; exit 6; fi
echo "[$(date)] humo hecho; freno: APRENDE_p s1 d2-3"
python3 lanza_P7_41.py --cadena APRENDE_p 1 2 3 > _P7_42_cadena_s1_freno.log 2>&1; rc=$?
if [ $rc -ne 0 ]; then echo "[$(date)] la cadena del freno paro con codigo $rc: PARADO"; exit 7; fi
python3 freno_P7_42.py > _P7_42_freno.log 2>&1
if ! grep -q '"FRENO": "PASA"' P7_42_freno.json; then echo "[$(date)] FRENO NO PASA (P7_42_freno.json): PARADO"; exit 8; fi
echo "[$(date)] freno PASA"
python3 lanza_P7_41.py --construye-fijas > _P7_42_construye_fijas.log 2>&1 || { echo "[$(date)] horneado de las fijas fallo: PARADO"; exit 6; }
for S in 1 2 3; do
  echo "[$(date)] serie $S"
  ( python3 lanza_P7_41.py --fijas $S 1 20 > _P7_42_fijas_s$S.log 2>&1; echo $? > _P7_42_fijas_s$S.rc ) &
  ( python3 lanza_P7_41.py --cadena APRENDE_v $S 1 20 > _P7_42_cadena_APRENDE_v_s$S.log 2>&1; echo $? > _P7_42_cadena_APRENDE_v_s$S.rc ) &
  ( python3 lanza_P7_41.py --cadena SIN $S 1 20 > _P7_42_cadena_SIN_s$S.log 2>&1; echo $? > _P7_42_cadena_SIN_s$S.rc ) &
  python3 lanza_P7_41.py --cadena APRENDE_p $S 1 20 > _P7_42_cadena_APRENDE_p_s$S.log 2>&1; rcp=$?
  wait
  rcf=$(cat _P7_42_fijas_s$S.rc 2>/dev/null || echo 99); rcv=$(cat _P7_42_cadena_APRENDE_v_s$S.rc 2>/dev/null || echo 99); rcs=$(cat _P7_42_cadena_SIN_s$S.rc 2>/dev/null || echo 99)
  if [ $rcp -ne 0 ] || [ "$rcf" -ne 0 ] || [ "$rcv" -ne 0 ] || [ "$rcs" -ne 0 ]; then echo "[$(date)] serie $S: APRENDE_p $rcp, APRENDE_v $rcv, SIN $rcs, fijas $rcf: PARADO"; exit 7; fi
  echo "[$(date)] serie $S completa"
done
echo "[$(date)] CAMPO COMPLETO"

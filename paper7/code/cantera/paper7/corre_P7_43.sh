#!/bin/sh
# [P7-43b] humo (3 x APRENDE_v desde el cuaderno de d13 del piloto; p95 < 10 ms o para) -> serie 1 con la orquesta (<= 20 a la vez, cadenas primero) -> serie 2.
# La serie 3 espera la palabra de Manel sobre los creditos. Cada paso sigue solo si el anterior acabo con codigo 0. Uso: nohup sh corre_P7_43.sh > _P7_43_corre.log 2>&1 &
cd "$(dirname "$0")" || exit 1
echo "[$(date)] imagenes: fijas y humo"
python3 lanza_P7_41.py --construye-fijas > _P7_43_construye.log 2>&1 || { echo "[$(date)] horneado de las fijas fallo: PARADO"; exit 6; }
# [P7-43c] el humo de las 09:15 (3 x HUMO43) ya esta jugado y pasa el corte revisado (p95 < 20 ms): no se repite
for S in 1 2; do
  echo "[$(date)] serie $S"
  python3 orquesta_P7_43.py --serie $S --tope 12 > _P7_43_serie$S.log 2>&1; rc=$?
  if [ $rc -ne 0 ]; then echo "[$(date)] serie $S: codigo $rc: PARADO"; exit 7; fi
  echo "[$(date)] serie $S completa"
done
echo "[$(date)] SERIES 1 Y 2 COMPLETAS; la serie 3 espera a Manel"

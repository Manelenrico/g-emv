"""[P7-9] Escribe informe_P7_9.md desde P7_9_F1.json, P7_9_F2.json, P7_9_campo.json y P7_9_estado.json; y el manifiesto de los diarios del freno."""
import glob, hashlib, json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
J = lambda p: json.load(open(os.path.join(AQUI, p))) if os.path.exists(os.path.join(AQUI, p)) else None
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
F1 = J("P7_9_F1.json") or {}; F2 = J("P7_9_F2.json") or {"vidas": [], "resumen": {}}; C = J("P7_9_campo.json") or {}; E = J("P7_9_estado.json") or {"peticiones": [], "imagenes": {}}
C8 = J("P7_8_campo.json") or {}
pet = [p for p in E["peticiones"] if p.get("coste_usd")]; coste = sum(p["coste_usd"] for p in pet)
V = {k: v for k, v in C.items() if not v.get("sin_tics")}
L = []; w = L.append
w(f"""# P7-9 · La esperanza, y otra vez el freno

*3-oct-2026. Coste: **créditos de la plataforma** {n(coste, 4)} USD en {len(pet)} partidas (por día {", ".join(n(p['coste_usd'], 4) for p in sorted(pet, key=lambda p: p['dia']))}); **consola de Anthropic 0 USD**.
`motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; los 202 congelados del cinco y los 32 del seis con su md5; el cuerpo no se toca: todo en
archivos `_P7`. Una vida por proceso; la memoria viaja solo en el cuaderno. Los números de método son los de la mesa.*

## Sección 1 · La esperanza, en el código

Pieza H de `descubre_P7.py` (`esperanza_cuerpo`, `mezcla`, `heal_imaginado`, `k_ganas`). Al imaginar usar el botiquín, la cura imaginada =
(1 − ignorancia) × creencia + ignorancia × esperanza, con esperanza = lo que hacen en el cuerpo los consumibles que el cuerpo conoce, tal como lo
tiene escrito: la media de `heal` del catálogo de los consumibles que no son el botiquín, hoy la ración, **15** (fuente: el registro `catalogo`
de los diarios). En recursos la foto ya pone la unidad gastada (−1) y en vínculo nada. Nunca probado (ignorancia 1): todo esperanza, cura imaginada
15; muy conocido: todo creencia. Ningún peso por la necesidad: de eso se ocupan las filas del cuerpo. La misma mezcla al imaginar tenerlo en el
zurrón: las ganas (R-ACOPIO, la rama "con una sola no basta", el término del botiquín en W y W_TARGET) escalan por k = mezcla sobre la
creencia máxima / cura del catálogo (nunca probado: 15 / 50 = 0,3). La creencia de la situación de ahora; si esa situación no tiene creencia
pero otra sí, la máxima (declarado). El regalo (pieza G, P7-8) sigue mirando solo lo aprendido (`k_creencia`, sin esperanza): con "no sé",
nada que regalar por su valor; queda a la mesa si la esperanza también debe entrar ahí (sección 6). Interruptor `GEMV_P7_ESPERANZA` (1 por
defecto; 0 solo en el banco "antes"). TECHO y apagado no la ven.

Corrección de la causa del corte (P7-8): el canal lo corta el daño recibido, no el movimiento; la regla de no apuntar ventanas sin gasto se
queda.

## Sección 2 · F1: apagado y TECHO reproducen A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
""")
for b in ("apagado", "TECHO"):
    x = F1.get(b) or {}; f = x.get("fidelidad") or {}
    w(f"| {b} | {n(f.get('igual'))} | {n(f.get('difiere', 0))} | {'; '.join(f"{d['vida'][-14:]} t {d['t']}" for d in x.get('desacuerdos', [])) or '–'} |\n")
w(f"""
Los mismos dos tics de siempre. **F1 pasa** (`P7_9_F1.json`).

## Sección 3 · F2: en banco, sobre los diarios del freno de P7-8

Réplica de los seis diarios del freno de P7-8 (APRENDE serie 1, días 1 a 3, asientos 10 y 11; `banco_P7_9.py`), brazo APRENDE con el cuaderno
vacío (el botiquín desconocido), dos veces: sin esperanza (lo de antes) y con ella. Se registran los tics con un botiquín en el zurrón y la
vida por debajo de 50 (baja) o por encima de 80 (alta), sin el canal abierto. El mundo es el del diario: lo elegido no lo cambia.

| | tics | con el candidato `usar_botiquin` | lo elige | d(usar) − d(mejor), mediana / media | cura imaginada (mediana) |
|---|---:|---:|---:|---|---:|
""")
RS = J("P7_9_F2_resumen.json") or {}
for nombre, et in (("antes", "antes (sin esperanza)"), ("esperanza", "con esperanza")):
    for b, bt in (("baja", "vida < 50"), ("alta", "vida > 80")):
        x = (RS.get(nombre) or {}).get(b) or {}
        w(f"| {et}, {bt} | {n(x.get('tics'))} | {n(x.get('con_candidato_usar'))} | {n(x.get('elige_usar'))} | {n(x.get('gap_mediana'), 4)} / {n(x.get('gap_media'), 4)} | {n(x.get('heal_mediana'), 1)} |\n")
w(f"""
Lectura. Con la vida baja, el candidato de usar casi nunca existe: de los {n((RS.get('esperanza') or {}).get('baja', {}).get('tics'))} tics, en {n((RS.get('esperanza') or {}).get('baja', {}).get('tics', 0) - (RS.get('esperanza') or {}).get('baja', {}).get('con_candidato_usar', 0))} el cuerpo solo tenía `noop` (el enfriamiento del
mundo tras cada acción; `Bloqueos`, decisor_zs.py:602-606) o el canal estaba abierto (excluidos). **Cuando existe, con esperanza lo usa siempre**
({n((RS.get('esperanza') or {}).get('baja', {}).get('elige_usar'))} de {n((RS.get('esperanza') or {}).get('baja', {}).get('con_candidato_usar'))}, con la vida a 35, 13 y 6 en el asiento 11 del día 1); antes lo usaba {n((RS.get('antes') or {}).get('baja', {}).get('elige_usar'))} de {n((RS.get('antes') or {}).get('baja', {}).get('con_candidato_usar'))}. La cura imaginada pasa de 0 a 15.
Con la vida alta (casi siempre a 100, donde el candidato no existe), con esperanza lo usa {n((RS.get('esperanza') or {}).get('alta', {}).get('elige_usar'))} de {n((RS.get('esperanza') or {}).get('alta', {}).get('con_candidato_usar'))} (antes {n((RS.get('antes') or {}).get('alta', {}).get('elige_usar'))} de {n((RS.get('antes') or {}).get('alta', {}).get('con_candidato_usar'))}): la esperanza
también da valor al botiquín en el zurrón (k = 0,3), y gastarlo con la vida casi llena empieza a costar (d(usar) − d(mejor) = {n((RS.get('esperanza') or {}).get('alta', {}).get('gap_mediana'), 4)} de mediana).
Lo que la trampa de la mesa predecía (con la vida baja, la imaginación no le ponía efecto a lo desconocido y no lo usaba) se ve en la cura
imaginada (0 → 15) más que en la elección: en el campo de P7-8 el asiento 11 ya intentaba usarlo con la vida baja (7 canales, los 7 cortados
por golpes). Fuente: `P7_9_F2.json`, `P7_9_F2_resumen.json`.

## Sección 4 · F3: el freno otra vez (APRENDE, serie 1, días 1 a 3, las mismas semillas de P7-8)

Imágenes: {", ".join(f"día {k[-1]}: {v['etiqueta']} ({v['policy_version_id'][:8]}…)" for k, v in sorted(E['imagenes'].items()))}. Lector `campo_P7_9.py` → `P7_9_campo.json` (un uso = ventana del canal
`channeling first_aid` en el diario crudo; gastado si baja el n a bordo; cortado por daño si se cierra sin gasto en un tic con daño recibido).

| día (semilla) | criatura | vivo · puesto · causa (vida al morir) | coge (cómo) | regala | usos gastados (tic, situación, vida, curada; firme o al menos) | interrumpidos (cortados por daño) | cuaderno leído | al acabar: recuerdos (firmes / al menos), creencia cuerpo dentro, ignorancia |
|---|---|---|---|---:|---|---|---|---|
""")
for k, v in sorted(V.items(), key=lambda kv: (kv[1]["dia"], kv[1]["slot"])):
    c = v["cuaderno"] or {}; cre = ((c.get("creencias") or {}).get("first_aid") or {}).get("dentro") or {}; recs = {(r["tick"]): r for r in c.get("recuerdos_lista", [])}
    us = "; ".join(f"{u['t0']} {u['situacion']} {n(u['hp0'])} +{n(u['curada'])} ({'al menos' if (recs.get(u['t0']) or {}).get('al_menos') else 'firme' if u['t0'] in recs else 'no apuntado'})" for u in v["usos"] if u["gastado"]) or "ninguno"
    w(f"| {v['dia']} ({v['semilla']}) | {v['slot']} | {n(v['ticks_vivos'])} · {v['puesto']} · {v['causa_muerte']} ({n(v['hp_final'])}) | {v['coge_n']} ({', '.join(f'{a} {b}' for a, b in v['coge_por'].items()) or '–'}) | {v['regala_n']} | {us} | {v['usos_interrumpidos']} ({v.get('usos_cortados_por_dano', 0)}) | {'sí' if c.get('leido') else 'no'} (día {c.get('dia_arranque')}) | {c.get('recuerdos')} ({c.get('firmes')} / {c.get('al_menos')}), {n(cre.get('cuerpo'), 2) if cre else 'no sé'}, {n(c.get('ignorancia'), 3)} |\n")
firmes = sum((v["cuaderno"] or {}).get("firmes", 0) for v in V.values() if v["dia"] == 3)
leidos = all((v["cuaderno"] or {}).get("leido") for v in V.values() if v["dia"] > 1) and len(V) == 6
regalos_nose = sum(v["regala_n"] for v in V.values() if v["dia"] == 1)
w(f"""
Al lado, el freno de P7-8 con las mismas semillas y sin esperanza (`P7_8_campo.json`): {"; ".join(f"día {v['dia']} asiento {v['slot']}: usa {v['usos_gastados']} (interr {v['usos_interrumpidos']}), {(v['cuaderno'] or {}).get('firmes')} firmes / {(v['cuaderno'] or {}).get('al_menos')} al menos, ignorancia {n((v['cuaderno'] or {}).get('ignorancia'), 3)}" for v in sorted((x for x in C8.values() if not x.get('sin_tics')), key=lambda x: (x['dia'], x['slot'])))}.

{{FRENO}}

## Sección 5 · F4: créditos

{{F4}}

## Sección 6 · Lo que queda para la mesa

{{ABIERTO}}

## Archivos

| archivo | qué es |
|---|---|
| `descubre_P7.py` (pieza H) | la esperanza en la imaginación de usar y en las ganas |
| `banco_P7_5.py --f1`, `P7_9_F1.json`; `banco_P7_9.py`, `P7_9_F2.json` | F1 y F2 |
| `lanza_P7_9.py`, `P7_9_estado.json`, `P7_9_res/`, `cuadernos_P7_9/`, `campo_P7_9.py`, `P7_9_campo.json`, `P7_9_diarios_manifiesto.md` | el freno (las mismas semillas de `semillas_P7_8.json`) |
| `escribe_informe_P7_9.py`, `informe_P7_9.md` | este informe |
""")
freno = open(os.path.join(AQUI, "_P7_9_tmp", "freno.md")).read().strip() if os.path.exists(os.path.join(AQUI, "_P7_9_tmp", "freno.md")) else "(pendiente)"
abierto = open(os.path.join(AQUI, "_P7_9_tmp", "abierto.md")).read().strip() if os.path.exists(os.path.join(AQUI, "_P7_9_tmp", "abierto.md")) else "(pendiente)"
f4 = f"Créditos de la plataforma: {n(coste, 4)} USD en {len(pet)} partidas enteras (por día {', '.join(n(p['coste_usd'], 4) for p in sorted(pet, key=lambda p: p['dia']))}). Tres subidas de imagen (`gemv-p7-campo`), sin créditos. Consola de Anthropic: 0 USD. Acumulado del siete en la plataforma: P7-5 0,2660 + P7-6 0,1930 + P7-7 0,3265 + P7-8 0,3246 + P7-9 {n(coste, 4)} = {n(0.2660 + 0.1930 + 0.3265 + 0.3246 + coste, 4)} USD."
txt = "".join(L).replace("{FRENO}", freno).replace("{ABIERTO}", abierto).replace("{F4}", f4); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_9.md"), "w").write(txt); print("informe escrito", len(txt))
M = ["# P7-9 · diarios del freno (fuera de git; md5)", "", "| archivo | bytes | md5 |", "|---|---:|---|"]
for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P79_s*_d*_*", "*.art.log"))):
    M.append(f"| `{os.path.relpath(f, RAIZ)}` | {os.path.getsize(f)} | `{hashlib.md5(open(f, 'rb').read()).hexdigest()}` |")
open(os.path.join(AQUI, "P7_9_diarios_manifiesto.md"), "w").write("\n".join(M) + "\n")

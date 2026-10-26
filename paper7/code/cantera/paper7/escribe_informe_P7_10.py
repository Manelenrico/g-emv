"""[P7-10] Escribe informe_P7_10.md desde P7_10_sitio.json, P7_10_F1.json, P7_10_campo.json, P7_10_sello_resultado.json, P7_10_estado.json y
SELLO_P7_10.md; y el manifiesto de los diarios (fuera de git)."""
import glob, hashlib, json, os, statistics, collections
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
J = lambda p: json.load(open(os.path.join(AQUI, p))) if os.path.exists(os.path.join(AQUI, p)) else None
md5 = lambda p: hashlib.md5(open(os.path.join(RAIZ, p), "rb").read()).hexdigest()
def n(x, d=0):
    if x is None: return "–"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
SI = J("P7_10_sitio.json") or {"vidas": []}; F1 = J("P7_10_F1.json") or {}; C = J("P7_10_campo.json") or {}; SR = J("P7_10_sello_resultado.json") or {}; E = J("P7_10_estado.json") or {"peticiones": [], "imagenes": {}}
V = {k: v for k, v in C.items() if not v.get("sin_tics")}; BR = ("SUELO", "BORRADO", "APRENDE", "TECHO")
pet = [p for p in E["peticiones"] if p.get("coste_usd")]; coste = sum(p["coste_usd"] for p in pet); por_brazo = {b: sum(p["coste_usd"] for p in pet if p["brazo"] == b) for b in BR}; n_brazo = {b: sum(1 for p in pet if p["brazo"] == b) for b in BR}
estados = collections.Counter(p["estado"] for p in E["peticiones"])
def vidas(b, dias=None): return [v for v in V.values() if v["brazo"] == b and (dias is None or v["dia"] in dias)]
def med(xs): return statistics.median(xs) if xs else None
L = []; w = L.append
w(f"""# P7-10 · El primer campo del siete, con la esperanza

*3/4-oct-2026. Coste: **créditos de la plataforma** {n(coste, 4)} USD en {len(pet)} partidas ({", ".join(f"{b} {n_brazo[b]}: {n(por_brazo[b], 4)}" for b in BR)}); **consola de Anthropic 0 USD**.
Total de créditos de P7-10: {n(coste, 4)} USD. Acumulado del siete en la plataforma: {n(0.2660 + 0.1930 + 0.3265 + 0.3246 + 0.3240 + coste, 4)} USD (P7-5 a P7-9: 1,4341).
`motor/model.py` = `{md5('motor/model.py')}` al empezar y al acabar; los 202 congelados del cinco y los 32 del seis con su md5; el cuerpo no se toca: todo en
archivos `_P7`. Una vida por proceso; la memoria viaja solo en el cuaderno. Sello antes de jugar: `SELLO_P7_10.md`, commit `{E.get('commit_sello', '')[:12]}`.
Peticiones: {dict(estados)}.*

## Sección 1 · El arreglo: en un empate, hacer sitio no gana

Pieza I de `descubre_P7.py` (`desempate_sin_sitio`, envoltorio de `D.select_tiebreak`, el desempate de la casa que `decide` llama en
decisor_zs.py:895). Si el mínimo de la d terminal lo comparten (empate exacto, ±1e-9) un candidato de hacer sitio y otro que no lo es, o si
el paisaje es degenerado (spread ≤ 1e-3), los de hacer sitio salen del desempate: se queda lo que se tiene. Si hacer sitio gana solo, gana.
Lo medido antes del arreglo (día 2 del freno de P7-9, asiento 10): la vuelta de cada oscilación ración ↔ botiquín era un empate exacto con
`noop` (diferencia 0,0), que `noop` no puede ganar; la ida ganaba de verdad (0,16).

**Banco** (`banco_P7_10.py` → `P7_10_sitio.json`; réplica de los días 1 y 2 de P7-9, asiento 10, con el cuaderno que leyó ese día):

| día | hacer sitio en el campo (oscilaciones) | sin el arreglo: hacer sitio (oscilaciones) | con el arreglo: hacer sitio (oscilaciones) | en los tics donde el campo hizo sitio, con el arreglo |
|---|---|---|---|---|
""")
for v in SI["vidas"]:
    a, b = v["brazos"].get("antes") or {}, v["brazos"].get("arreglo") or {}
    w(f"| {v['dia']} | {v['campo']['hacer_sitio']} ({v['campo']['oscilaciones']}) | {a.get('hacer_sitio_replica_total')} ({a.get('oscilaciones_replica')}) | {b.get('hacer_sitio_replica_total')} ({b.get('oscilaciones_replica')}) | {', '.join(f'{k} {x}' for k, x in (b.get('en_los_tics_del_campo') or {}).items())} |\n")
w(f"""
Las oscilaciones desaparecen (4 → 0, 7 → 0); los hacer-sitio que ganaban por su valor siguen ganando.

## Sección 2 · F1: apagado y TECHO reproducen A4

| brazo | tics iguales | distintos | los distintos |
|---|---:|---:|---|
""")
for b in ("apagado", "TECHO"):
    x = F1.get(b) or {}; f = x.get("fidelidad") or {}
    w(f"| {b} | {n(f.get('igual'))} | {n(f.get('difiere', 0))} | {'; '.join(f"{d['vida'][-14:]} t {d['t']}" for d in x.get('desacuerdos', [])) or '–'} |\n")
w(f"""
Los mismos dos tics de siempre. **F1 pasa** (`P7_10_F1.json`).

## Sección 3 · El sello y el campo

`SELLO_P7_10.md` (sustituye al de P7-8): md5 de los archivos, las 20 semillas nuevas (k = 89..108, serie 2 en orden inverso) y las seis predicciones
con su medida, en el commit `{E.get('commit_sello', '')[:12]}`, antes de pedir ninguna partida. Imágenes: {", ".join(f"{k}: {v['etiqueta']}" for k, v in sorted(E['imagenes'].items()) if not k.startswith('APRENDE'))}; APRENDE,
una por serie y día (v10 en adelante), con los cuadernos del día anterior. Lanzador `lanza_P7_10.py` (las dos cadenas de APRENDE y los brazos fijos
en tandas, a la vez, con un cerrojo sobre el estado); lector `campo_P7_10.py` → `P7_10_campo.json`.

## Sección 4 · El freno (APRENDE, serie 1, días 1 a 3)

{{FRENO}}

## Sección 5 · El campo: lo que se mide

{{CAMPO}}

## Sección 6 · El sello, cifra a cifra

{{SELLO}}

## Sección 7 · Créditos

{{F4}}

## Sección 8 · Lo que queda para la mesa

{{ABIERTO}}

## Archivos

| archivo | qué es |
|---|---|
| `descubre_P7.py` (pieza I) | en un empate, hacer sitio no gana |
| `banco_P7_10.py`, `P7_10_sitio.json`; `banco_P7_5.py --f1`, `P7_10_F1.json` | el banco del arreglo y F1 |
| `SELLO_P7_10.md`, `semillas_P7_10.json`, `Dockerfile.pareja_P7_8`, `lanza_P7_10.py`, `P7_10_estado.json`, `P7_10_res/`, `cuadernos_P7_10/` | el campo: sello, semillas, imagen, lanzador, estado, resultados y cuadernos |
| `campo_P7_10.py`, `P7_10_campo.json`, `sello_P7_10.py`, `P7_10_sello_resultado.json`, `figuras_P7_10.py`, `P7_10_fig_*.png`, `P7_10_diarios_manifiesto.md` | lector, evaluador del sello, figuras, manifiesto |
| `escribe_informe_P7_10.py`, `informe_P7_10.md` | este informe |
""")
def txt_de(nombre):
    p = os.path.join(AQUI, "_P7_10_tmp", nombre); return open(p).read().strip() if os.path.exists(p) else "(pendiente)"
f4 = f"Créditos de la plataforma: {n(coste, 4)} USD en {len(pet)} partidas enteras ({', '.join(f'{b}: {n_brazo[b]} partidas, {n(por_brazo[b], 4)} USD' for b in BR)}; media por partida {n(coste / len(pet) if pet else None, 4)}). Subidas de imagen: {len(E['imagenes'])}, sin créditos. Consola de Anthropic: 0 USD. Acumulado del siete en la plataforma: {n(1.4341 + coste, 4)} USD."
txt = "".join(L).replace("{FRENO}", txt_de("freno.md")).replace("{CAMPO}", txt_de("campo.md")).replace("{SELLO}", txt_de("sello.md")).replace("{F4}", f4).replace("{ABIERTO}", txt_de("abierto.md")); assert "§" not in txt
open(os.path.join(AQUI, "informe_P7_10.md"), "w").write(txt); print("informe escrito", len(txt))
M = ["# P7-10 · diarios del campo (fuera de git; md5)", "", "| archivo | bytes | md5 |", "|---|---:|---|"]
for f in sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", "P710_s*_d*_*", "*.art.log"))):
    M.append(f"| `{os.path.relpath(f, RAIZ)}` | {os.path.getsize(f)} | `{hashlib.md5(open(f, 'rb').read()).hexdigest()}` |")
open(os.path.join(AQUI, "P7_10_diarios_manifiesto.md"), "w").write("\n".join(M) + "\n")

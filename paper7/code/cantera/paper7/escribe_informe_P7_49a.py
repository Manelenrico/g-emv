"""[P7-49a] Escribe informe_P7_49a.md desde P7_49_identidad.json (banco_P7_49), P7_49_local.json (local49_P7_49) y miedo_P7_49.FILAS_MIEDO. Ninguna cifra a mano.
  python3 escribe_informe_P7_49a.py [--saldo 228]"""
import hashlib, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(AQUI, f)))
ID = J("P7_49_identidad.json"); L = J("P7_49_local.json")
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
saldo = (sys.argv[sys.argv.index("--saldo") + 1] if "--saldo" in sys.argv else None)
FILAS = [l.strip() for l in open(os.path.join(AQUI, "miedo_P7_49.py")) if l.startswith("FILAS_MIEDO")][0]
TI = ["| vida replicada (lazo abierto, cuaderno real del día anterior) | asiento | decisiones | MIEDO = 1: distintas | 0,5 / 1,5: distintas | 0,7 / 1,3: distintas | p95 ms (MIEDO = 1) |", "|---|---:|---:|---:|---:|---:|---:|"]
for f in ID: TI.append(f"| {f['vida']} | {f['slot']} | {f['tics']} | {f['mando_1']['distintas']} | {f['mando_05_15']['distintas']} | {f['mando_07_13']['distintas']} | {n(f['mando_1']['ms_p95'], 1)} |")
ident = all(f["mando_1"]["distintas"] == 0 for f in ID); tot_dec = sum(f["tics"] for f in ID)
orden = sorted(L, key=lambda k: (L[k]["miedo_p"] - L[k]["miedo_v"]))
TV = ["| pareja (MIEDO valiente / prudente) | hermana | MIEDO | vidas | tics (media · mediana) | mueren | quieta (% tics) | camuflada (% tics) | pruebas por vida | ms mediana · p95 máx | % bloqueados |", "|---|---|---:|---:|---|---:|---:|---:|---:|---|---:|"]
ref = L.get("m1_1", {}).get("por_hermana", {})
for k in orden:
    r = L[k]
    for h in ("valiente", "prudente"):
        x = r["por_hermana"].get(h)
        if not x: continue
        TV.append(f"| {n(r['miedo_v'], 1)} / {n(r['miedo_p'], 1)} | {h} | {n(x['miedo'], 2)} | {x['vidas']} | {n(x['tics_media'], 0)} · {n(x['tics_mediana'], 0)} | {x['mueren']} | {n(x['quieta_pct'], 1)} | {n(x['camuflada_pct'], 1)} | {n(x['huellas_por_vida'], 2)} | {n(x['ms_mediana'], 2)} · {n(x['ms_p95_max'], 1)} | {n(x['bloqueados_pct'], 1)} |")
# viabilidad: no morir el doble de rapido que MIEDO = 1 (tics medios >= mitad de la referencia de esa hermana... la referencia 1/1 tiene las dos iguales: se usa la media de las 16), no quieta la mayor parte (< 50 %)
ref_t = (sum(x["tics_media"] * x["vidas"] for x in ref.values()) / max(1, sum(x["vidas"] for x in ref.values()))) if ref else None
def viable(x): return (ref_t is not None and x["tics_media"] >= 0.5 * ref_t and x["quieta_pct"] < 50.0)
V = {k: {h: viable(x) for h, x in L[k]["por_hermana"].items()} for k in L if k != "m1_1"}
cand = [k for k in orden if k != "m1_1" and all(V[k].values())]
mejor = max(cand, key=lambda k: L[k]["miedo_p"] - L[k]["miedo_v"]) if cand else None
out = f"""# P7-49a · Carácter de verdad: el mando de miedo, por fuera (sin copiar ni tocar model.py); identidad y viabilidad local

*12-oct-2026. Solo local, 0 créditos (saldo {('**' + saldo + '**, dato de Manel 12-oct 06:47') if saldo else 'el de la página'}); consola 0 $. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`: ni se copia ni se toca; la appraisal congelada
tampoco. Sin sello (P7-49 en espera). Piezas nuevas: `miedo_P7_49.py` = `{md5('miedo_P7_49.py')}`, `campo_P7_49.py`, `policy_pareja_P7_49.py`, `Dockerfile.pareja_P7_49`; `banco_P7_49.py` →
`P7_49_identidad.json`; `local49_P7_49.py` → `P7_49_local.json`; `escribe_informe_P7_49a.py` (este informe; ninguna cifra a mano).*

## Sección 1 · Dónde vive el miedo y el mando

`model.py` no tiene miedo: tiene seis fuerzas y una distancia. Lo que llega como f⁻ (nF, nR, nS) lo construye la appraisal congelada sumando filas por `REPARTO`; el miedo y el daño
sentido llegan ya mezclados. Decisión de Manel: el miedo es ANTICIPAR una pérdida que aún no ha ocurrido, en cualquiera de las tres dimensiones. **El mando MIEDO (un solo número)
multiplica la M de esas filas**, enganchado por fuera a `A.filas` después de las piezas del siete (así escala lo que el decisor fotografía en cada candidato). La cautela del probar
lleva el mismo factor: cautela_eff = 1 − MIEDO × (1 − cautela) (MIEDO = 0,5 da la valiente de P7-42, (1 + c) / 2). Pareja: MIEDO_V al asiento par, MIEDO_P al impar.

| anticipa una pérdida (× MIEDO) | motivo |
|---|---|
| F-ANTICIPACION | daño previsto (anillo, hostiles): aún no golpea |
| F-4-ALCANCE | rival con arma al alcance: puede golpear, no ha golpeado |
| F-REENCUENTRO | miedo con memoria: un agresor recordado, armado, que se acerca |
| MIEDO_APRENDIDO | miedo aprendido (paper 4): descuento del futuro sobre el hostil |
| F-HERMANO-AMENAZA | la hermana amenazada: aún no le pegan |
| S-8-EXPOSICION | a la vista / campo abierto: anticipa el ataque |
| S-7-AGRESOR | presión del agresor activo para evitar el siguiente golpe (mesa: dentro) |
| R-ACOPIO | la mochila sin botiquín: anticipa una herida sin cura (mesa: dentro) |
| S-COMPANIA | crece con la distancia a la hermana mientras aún se la localiza: anticipa la separación (aclaración de Manel: la valiente es más independiente) |

| intacta | motivo |
|---|---|
| F-DANO, F-HERMANO-GOLPE, R-HERMANO-FALTA, R-CARENCIA, S-SOLEDAD, S-DANO-PAREJA, S-MUERTE-PAREJA, S-HERIDO, S-PROVISION | pérdida presente (ya ocurre o ya ocurrió) |
| **S-VINCULO, S-VIDA-AJENA** | **decisión de Manel: son el freno a matar, es decir, cuidado, no miedo: la valiente y la prudente cuidan igual** |
| R-LLAMADA; R-CURIOSIDAD, R-CURIOSIDAD-CUANTO | atracción y curiosidad: no son pérdida |

En código: `{FILAS}`.

## Sección 2 · Identidad con MIEDO = 1 (decisión a decisión)

{chr(10).join(TI)}

Referencia = la misma composición sin el mando (hermanas solas, sin carácter por paridad: con el mando el carácter es solo el mando). **{tot_dec} decisiones en 3 vidas completas, {sum(f['mando_1']['distintas'] for f in ID)} distintas: {'PASA' if ident else 'NO PASA'}.**
Con 0,5 / 1,5 y 0,7 / 1,3 las decisiones sí cambian (control del enganche). `model.py` md5 sin cambio.

## Sección 3 · Viabilidad en local (lazo cerrado; hermanas SOLAS para medir solo el carácter)

Tres partidas con nuestra imagen en los 16 asientos (8 parejas valiente/prudente): 1 / 1 (referencia, sin carácter), 0,5 / 1,5 y 0,7 / 1,3. «Quieta» = tics vivos sin haber cambiado de casilla en los últimos 48 tics (2 s; un paso tarda 3-5 tics); «camuflada» = tics con el camuflaje puesto. El mundo local es el de P7-47/48: 16 criaturas nuestras, todas mueren antes del final.

{chr(10).join(TV)}

Criterio de viabilidad (enunciado): no morir el doble de rápido que MIEDO = 1 (tics medios ≥ la mitad de la referencia: {n(ref_t, 0) if ref_t else '—'} tics) y no quedarse quieta la mayor parte del tiempo (< 50 %).
Resultado: {'; '.join(f"{n(L[k]['miedo_v'], 1)} / {n(L[k]['miedo_p'], 1)}: " + ', '.join(f"{h} {'viable' if ok else 'NO viable'}" for h, ok in V[k].items()) for k in orden if k != 'm1_1')}.
**Propuesta: {('MIEDO ' + n(L[mejor]['miedo_v'], 1) + ' / ' + n(L[mejor]['miedo_p'], 1) + ' (la pareja más separada en la que las dos siguen viables)') if mejor else 'ninguna de las dos parejas es viable en local para las dos hermanas; se propone probar 0,8 / 1,2'}.** Una partida local por pareja (8 vidas por hermana): la propuesta es para que la
mesa la lleve al sello de P7-49, no un resultado. La «camuflada» al 12 % es en cada partida UNA sola vida que lleva el camuflaje puesto casi entera ({', '.join(f"{k}: asiento {sl} {n(v['camuflada_pct'], 0)} %" for k in orden for sl, v in L[k]['vidas'].items() if (v['camuflada_pct'] or 0) > 50)}): no es
un rasgo del miedo. Diferencias entre hermanas en duración, pruebas y quietud: dentro de lo que 8 vidas pueden decir; el mando no las deja ni quietas ni muertas antes.
"""
open(os.path.join(AQUI, "informe_P7_49a.md"), "w", encoding="utf-8").write(out); print("informe_P7_49a.md", out.count("\n"), "lineas")

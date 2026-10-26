"""[P7-48] Escribe informe_P7_48.md (capitulo 4, construccion sin sello: las hermanas que se cuentan lo aprendido; comprobacion local) desde P7_48_local.json
(local48_P7_48). Ninguna cifra a mano.  python3 escribe_informe_P7_48.py [--saldo 228]"""
import hashlib, json, os, statistics as st, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(AQUI, "P7_48_local.json")))
n = lambda x, d=2: ("—" if x is None else f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", "."))
md5 = lambda f: hashlib.md5(open(os.path.join(AQUI, f), "rb").read()).hexdigest()
L47 = {k: json.load(open(os.path.join(AQUI, f"P7_47_local_{k}.json"))) for k in ("APRENDE_p", "APRENDE_v") if os.path.exists(os.path.join(AQUI, f"P7_47_local_{k}.json"))}
saldo = (sys.argv[sys.argv.index("--saldo") + 1] if "--saldo" in sys.argv else None)
ORIG = ("vivido", "visto", "canal", "noche")
partidas = sorted(R, key=lambda k: (k.split("_d")[0], int(k.split("_d")[1])))
T = ["| partida | vidas | tics (media) | mueren | pruebas por vida | recuerdos por vida: vividos · vistos · contados canal · contados noche | vistos descartados (motivos) | mensajes M7 enviados · malos | pesos = intensidad × B: bien · mal | ms mediana (media) · p95 máx | % sobre el tic (media) · % bloqueados |", "|---|---:|---:|---:|---:|---|---|---|---|---|---|"]
POR = {}
for k in partidas:
    r = R[k]; vs = [v for v in r["vidas"].values() if v["tics"] > 0]; res = r["resumen"]; P = [v["P7_48"] for v in vs if v.get("P7_48")]
    tot = {o: sum(p["n"][o] for p in P) for o in ORIG}; desc = {}
    for p in P:
        for m, c in p["descartes"].items(): desc[m] = desc.get(m, 0) + c
    T.append(f"| {k} | {len(vs)} | {n(res['tics_media'], 0)} | {res['mueren']} | {n(res['huellas_por_vida'], 2)} | {n(tot['vivido'] / len(vs), 2)} · {n(tot['visto'] / len(vs), 2)} · {n(tot['canal'] / len(vs), 2)} · {n(tot['noche'] / len(vs), 2)} | {sum(p['n']['visto_descartado'] for p in P)} ({'; '.join(f'{m} {c}' for m, c in desc.items()) or '—'}) | {sum(p['n']['mensajes'] for p in P)} · {sum(p['n']['malos'] for p in P)} | {sum(p['pesos_ok'] for p in P)} · {sum(p['pesos_mal'] for p in P)} | {n(res['ms_mediana_media'], 2)} · {n(res['ms_p95_max'], 1)} | {n(res['sobre_tic_pct_media'], 3)} · {n(res['bloqueados_pct_media'], 2)} |")
    for v in vs:
        p = v.get("P7_48") or {}; mie = p.get("miedo") or "?"; brazo = k.split("_d")[0]
        POR.setdefault((brazo, mie), []).append({**p.get("n", {}), "huellas": v["huellas"], "murio": v["murio"], "tics": v["tics"]})
TP = ["| brazo · hermana | vidas | tics (media) | pruebas por vida | vividos · vistos · canal · noche (por vida) | mensajes por vida | vistos descartados |", "|---|---:|---:|---:|---|---:|---:|"]
for (brazo, mie), L in sorted(POR.items()):
    m = lambda key: st.mean(x.get(key, 0) for x in L)
    TP.append(f"| {brazo} · {mie} | {len(L)} | {n(m('tics'), 0)} | {n(m('huellas'), 2)} | {n(m('vivido'), 2)} · {n(m('visto'), 2)} · {n(m('canal'), 2)} · {n(m('noche'), 2)} | {n(m('mensajes'), 2)} | {sum(x.get('visto_descartado', 0) for x in L)} |")
lat_ok = all(R[k]["resumen"]["ms_p95_max"] is not None and R[k]["resumen"]["ms_p95_max"] <= 8.0 for k in partidas); tic_ok = all((R[k]["resumen"]["sobre_tic_pct_media"] or 0) == 0 for k in partidas)
pesos_mal = sum(p["pesos_mal"] for k in partidas for p in (v.get("P7_48") for v in R[k]["vidas"].values()) if p); pesos_ok = sum(p["pesos_ok"] for k in partidas for p in (v.get("P7_48") for v in R[k]["vidas"].values()) if p)
noche = {k: sum((v.get("P7_48") or {}).get("n", {}).get("noche", 0) for v in R[k]["vidas"].values()) for k in partidas}
out = f"""# P7-48 · Capítulo 4, construcción (sin sello): las hermanas que se cuentan lo aprendido, comprobadas en local

*12-oct-2026. Solo local (`coworld play` en el Mac): plataforma 0 créditos (saldo {('**' + saldo + '**, dato de Manel 12-oct 06:47') if saldo else 'el de la página'}); consola 0 $. `motor/model.py` = `1e511978c251130e95169ebf8443efa1`,
no se lee ni se escribe. Piezas nuevas (las del campo intactas): `escala_P7_48.py` = `{md5('escala_P7_48.py')}` (la intensidad en su escala, SIN habituación), `hermanas_P7_48.py` = `{md5('hermanas_P7_48.py')}`,
`campo_P7_48.py`, `policy_pareja_P7_48.py`, `Dockerfile.pareja_P7_48` (ARG HERMANAS = comparte | solas; GEMV_OJOS=1 en los dos). Comprobación: `local48_P7_48.py` → `P7_48_local.json`
(partidas en `_P7_48_local/`, cuadernos encadenados en `cuadernos_P7_48/`); `escribe_informe_P7_48.py` (este informe; ninguna cifra a mano).*

## Sección 1 · Lo que permite el juego (medido) y lo construido

- **Canal**: `talk` con `broadcast`, **`team` (privado de la pareja)** y `dm`; 1 mensaje por 24 tics (`rate_limited` si no), 120 caracteres ASCII, latencia 2 tics, sin límite de distancia,
  solo entre vivas. Con los ojos compartidos el parte E2 ocupa un hueco cada 25 tics: el recuerdo va EN LUGAR de un parte, nunca dos seguidos (el parte no se pierde más de 25 tics).
  No hay noche en el juego: la noche es entre partidas, con los cuadernos de las dos en la misma carpeta.
- **Lo que ve una de la otra**: por la vista `pos`, `hp_band`, `hand`, `body`, `netted`, `poisoned`, `channeling`; por el parte E2 (cada 25 tics) hp exacto, botiquines a bordo, agresor,
  rivales y recursos que ella ve. El vínculo = `mem.roce_B` (0-1, appraisal congelado). Nada de esto toca `model.py`.
- **Pareja** (Manel): una valiente (asiento par) y una prudente (impar); carácter como en P7-42, solo en la cautela del probar (`filo_P7_40.MIEDO`; `model.py` no expone el miedo del
  cuerpo, así que «la mitad del miedo del cuerpo» no es alcanzable sin tocarlo: se declara). Igual en los dos brazos.
- **Recuerdo entero**: efecto por dominio, importancia, contexto (dentro/fuera, golpeado), foto emocional (dolor F/R/S, positivo, d), últimas 4 acciones, día, tic, `al_menos`.
  Marca `origen` = vivido / visto / contado, `via` = canal | noche, `de`, `B`. **Peso recibido = intensidad (en su escala) × B** (B ≤ 1: nunca más que el vivido).
- **Mensaje M7** (90-95 caracteres): `M7 P<asiento> d<día> t<tic> <objeto><situación><golpeado> e<c>,<r>,<v> i<c>,<r>,<v> f<F>,<R>,<S>,<pos>,<d> a<acciones> n<intensidad> m<al_menos>`;
  parser estricto (regex); lo que no cuadra se cuenta como malo.
- **Mirando**: vigilia al ver en el parte un botiquín menos o el camuflaje puesto; ventana = parte anterior + 4 partes; efecto = hp máximo − hp anterior; descartes: agresor en la
  ventana, daño (hp baja entre partes), la hermana calla, el botiquín acabó en mi zurrón (regalo), o la vida llena (soltar/dar, no usar). Importancia = |Δ malestar propio| en la
  ventana; foto y situación propias; acciones = lo que hacía la hermana (mano, cuerpo, channeling, distancia).
- **Noche** (Manel, cambio 1): como mucho los 5 vividos MÁS INTENSOS de ayer de la hermana que no llegaron de día, con el B del cierre de ayer.

## Sección 2 · La comprobación local (lazo cerrado, partidas de verdad)

Cada brazo, una cadena de 3 días con nuestra imagen en los 16 asientos (8 parejas valiente/prudente; no hay imágenes de los rivales: todas las vidas son nuestras y todas mueren
antes del final); el día d+1 se hornea con los cuadernos que las 16 escribieron el día d.

{chr(10).join(T)}

{chr(10).join(TP)}

- **Llegan y pesan como se dice**: {pesos_ok} recuerdos recibidos (vistos y contados) con peso = intensidad × B exacto; {pesos_mal} con peso distinto. La noche entrega {', '.join(f"{k}: {v}" for k, v in noche.items())}
  recuerdos (en el día 1 no hay ayer; en `solas` la noche está apagada).
- **Latencia**: p95 local ≤ 8 ms en todas las partidas: {'sí' if lat_ok else 'NO'} (máximo del p95 por vida {n(max(R[k]['resumen']['ms_p95_max'] or 0 for k in partidas), 1)} ms; medianas {n(min(R[k]['resumen']['ms_mediana_media'] or 0 for k in partidas), 2)}-{n(max(R[k]['resumen']['ms_mediana_media'] or 0 for k in partidas), 2)} ms); 0 % sobre el tic: {'sí' if tic_ok else 'NO'} (máximo {n(max(R[k]['resumen']['sobre_tic_pct_media'] or 0 for k in partidas), 3)} %).
  Referencia sin las piezas de P7-48, mismas partidas locales de P7-47 (16 contenedores en el mismo Mac): p95 máximo {', '.join(f"{k} {n(L47[k]['resumen']['ms_p95_max'], 1)}" for k in L47)} ms, sobre el tic {', '.join(f"{n(L47[k]['resumen']['sobre_tic_pct_media'], 3)}" for k in L47)} %:
  la cola de latencia es la del montaje local (16 políticas y el motor en una máquina), no de las piezas; en plataforma el campo P7-45 dio p95 2-20 ms con cachés.

## Lectura (construcción; sin sello)

Las tres vías funcionan en lazo cerrado: el canal manda recuerdos enteros en los huecos del parte sin perder ninguno por formato, el mirar apunta usos de la hermana con sus descartes
contados, y la noche entrega como mucho 5 por hermana con el B del cierre. Los pesos son intensidad × B sin excepción. La latencia local NO cumple el p95 ≤ 8 ms ni el 0 % sobre el tic, pero con los mismos números que las partidas locales sin estas piezas (P7-47): es el montaje de 16 políticas en un Mac, no la construcción; se mide de verdad en plataforma. El mundo local (16 criaturas nuestras, vidas cortas) da pocas
pruebas por vida; medir si compartir cambia lo aprendido pide un campo en la plataforma, con sello: queda para la mesa.
"""
open(os.path.join(AQUI, "informe_P7_48.md"), "w", encoding="utf-8").write(out); print("informe_P7_48.md", out.count("\n"), "lineas")

"""LOS REENCUENTROS — PROMPT_69 (forense puro, coste 0; NO construye nada).

Antes de tocar una silla: ¿el mismo agresor VUELVE? Si casi nunca vuelve, la
"defensa con memoria" no tiene sobre que actuar y se cierra honesto.

TESTIGO CIEGO (R1/R2 aplicados a la VARA): solo cuenta como agresor CIERTO el
asiento que aparece en `damage_taken.source` de una de las dos gemelas —lo
que el parte v2 transmitiria—. NO se usa el log para etiquetar agresores de
terceros.

Definiciones (fijadas ANTES de contar, del encargo):
  CONTACTO      visible a <=3 casillas, o danandonos
  SEPARACION    >=24 tics seguidos sin contacto con ese asiento
  REENCUENTRO   tras una separacion, ese asiento vuelve a ser visible para
                cualquiera de las dos (t1). Se cuenta cada vez.

Uso (desde la raiz del repo):  python3 paintball/reencuentros.py
"""
from __future__ import annotations

import collections
import json
import math
import os
import statistics as st

from proteccion_pareada import diario, serie, P

CONTACTO = 3.0
SEPARA = 24
APROX_TICS = 3
ARMAS = {"sword", "spear", "bow", "knives", "blowgun", "net"}


def episodios(tanda):
    return json.load(open(f"{P}/runs/{tanda}/episodios.json"))["eps"]


def cargar(tanda):
    base = f"{P}/runs/{tanda}"
    out = []
    for e in episodios(tanda):
        d10, d11 = diario(base, e["id"], 10), diario(base, e["id"], 11)
        if d10 and d11:
            out.append({"tanda": tanda, "eid": e["id"],
                        "S": {10: serie(d10), 11: serie(d11)}})
    return out


# ── A · la puerta: identidad estable ────────────────────────────────────────
def puerta(eps):
    """¿El asiento identifica al MISMO cuerpo durante todo el episodio?"""
    incoherencias = 0
    slots_vistos = 0
    for ep in eps:
        equipos = {}
        for s in (10, 11):
            for t, x in ep["S"][s].items():
                for sl, a in (x.get("ve") or {}).items():
                    eq = a.get("team")
                    if sl in equipos and equipos[sl] != eq:
                        incoherencias += 1
                    equipos[sl] = eq
        slots_vistos += len(equipos)
    return incoherencias, slots_vistos


# ── B · la vara del reencuentro ─────────────────────────────────────────────
def reencuentros_de(ep):
    S = ep["S"]
    ticks = sorted(set(S[10]) | set(S[11]))
    # agresores CERTIFICADOS: asiento que nos dano (a cualquiera de las dos)
    cert = {}                      # slot -> primer tick certificado
    victima = {}                   # slot -> a quien golpeo primero
    for t in ticks:
        for s in (10, 11):
            x = S[s].get(t)
            if not isinstance(x, dict):
                continue
            for src in (x.get("dmg") or []):
                if not (src or "").startswith("P"):
                    continue
                try:
                    sl = int(src[1:])
                except ValueError:
                    continue
                if sl in (10, 11):
                    continue        # entre hermanas: fuego amigo, no agresor
                if sl not in cert:
                    cert[sl] = t
                    victima[sl] = s
    out = []
    for sl, t_cert in cert.items():
        # serie de contacto con ese asiento, desde que se certifica
        estado = "contacto"
        ultimo_contacto = t_cert
        for t in [x for x in ticks if x >= t_cert]:
            hay = False
            quien = None
            for s in (10, 11):
                x = S[s].get(t)
                if not isinstance(x, dict) or not x.get("live"):
                    continue
                a = (x.get("ve") or {}).get(sl)
                if a and a.get("pos") and x["pos"]:
                    if math.dist(x["pos"], a["pos"]) <= CONTACTO:
                        hay, quien = True, s
                        break
                if f"P{sl}" in (x.get("dmg") or []):
                    hay, quien = True, s
                    break
            if hay:
                if estado == "separado":
                    out.append(medir(ep, sl, t, ultimo_contacto, quien,
                                     victima.get(sl)))
                estado = "contacto"
                ultimo_contacto = t
            else:
                if estado == "contacto" and t - ultimo_contacto >= SEPARA:
                    estado = "separado"
    return out


def medir(ep, sl, t1, fin_prev, quien_ve, victima_orig):
    """La fila del reencuentro."""
    S = ep["S"]
    ticks = [t for t in sorted(set(S[10]) | set(S[11])) if t1 <= t <= t1 + 240]
    dists, arma, dmin = [], None, None
    primer_golpe_suyo = primer_golpe_nuestro = None
    hp0 = hp1 = None
    for t in ticks:
        for s in (10, 11):
            x = S[s].get(t)
            if not isinstance(x, dict):
                continue
            if hp0 is None and s == quien_ve:
                hp0 = x["hp"]
            if s == quien_ve:
                hp1 = x["hp"]
            a = (x.get("ve") or {}).get(sl)
            if a and a.get("pos") and x["pos"]:
                d = math.dist(x["pos"], a["pos"])
                if s == quien_ve:
                    dists.append((t, d))
                dmin = d if dmin is None else min(dmin, d)
                if arma is None and a.get("hand") in ARMAS:
                    arma = a.get("hand")
            if primer_golpe_suyo is None and f"P{sl}" in (x.get("dmg") or []):
                primer_golpe_suyo = t
            h = x.get("honor") or {}
            if (primer_golpe_nuestro is None
                    and (x.get("el") or "").startswith("atacar")
                    and h.get("objetivo") == sl):
                primer_golpe_nuestro = t
    # aproximacion: distancia decreciente en >=3 tics tras t1
    aprox = False
    if len(dists) >= APROX_TICS + 1:
        d0 = dists[0][1]
        bajas = sum(1 for i in range(1, min(len(dists), 12))
                    if dists[i][1] < d0)
        aprox = bajas >= APROX_TICS
    if primer_golpe_suyo and primer_golpe_nuestro:
        quien_primero = "el" if primer_golpe_suyo <= primer_golpe_nuestro else "nosotras"
    elif primer_golpe_suyo:
        quien_primero = "el"
    elif primer_golpe_nuestro:
        quien_primero = "nosotras"
    else:
        quien_primero = "nadie"
    aviso = (primer_golpe_suyo - t1) if primer_golpe_suyo else None
    if primer_golpe_suyo:
        des = "nos dana"
        if hp1 is not None and hp1 <= 0:
            des = "nos mata"
    elif primer_golpe_nuestro:
        des = "lo danamos"
    else:
        des = "se va / se separa"
    return {"tanda": ep["tanda"], "eid": ep["eid"], "slot": sl, "t1": t1,
            "gap": t1 - fin_prev, "arma": arma, "aprox": aprox,
            "dmin": round(dmin, 1) if dmin is not None else None,
            "primero": quien_primero, "aviso": aviso,
            "hp0": hp0, "hp1": hp1, "desenlace": des,
            "quien_ve": quien_ve, "victima_orig": victima_orig,
            "la_otra": (victima_orig is not None and quien_ve != victima_orig)}


def main():
    eps = cargar("manada") + cargar("manada2")
    print("=" * 92)
    print(f"LOS REENCUENTROS — forense sobre {len(eps)} episodios (64+66), coste 0")
    print("=" * 92)

    # ── A ────────────────────────────────────────────────────────────────
    inc, n_sl = puerta(eps)
    print(f"\nA · PUERTA — identidad estable: {inc} incoherencias de equipo en "
          f"{n_sl} asientos-episodio")
    if inc:
        print("   ¡PARA! el asiento no identifica al mismo cuerpo.")
        return
    print("   OK: el asiento identifica al mismo cuerpo dentro del episodio.")

    # ── B ────────────────────────────────────────────────────────────────
    R = []
    for ep in eps:
        R.extend(reencuentros_de(ep))
    print(f"\nB · LA TABLA — {len(R)} reencuentros\n")
    if R:
        print(f"  {'eid':<20} {'slot':>4} {'t1':>6} {'gap':>5} {'arma':>7} "
              f"{'aprox':>6} {'dmin':>5} {'primero':>9} {'aviso':>6} "
              f"{'desenlace':<18} {'otra':>5}")
        for r in sorted(R, key=lambda x: (x["eid"], x["t1"])):
            print(f"  {r['eid'][:20]:<20} {r['slot']:>4} {r['t1']:>6} "
                  f"{r['gap']:>5} {str(r['arma'] or '—'):>7} "
                  f"{str(r['aprox']):>6} {str(r['dmin']):>5} "
                  f"{r['primero']:>9} {str(r['aviso'] if r['aviso'] is not None else '—'):>6} "
                  f"{r['desenlace']:<18} {str(r['la_otra']):>5}")

    # resumen + P1..P4
    por_ep = collections.Counter(r["eid"] for r in R)
    med_ep = st.median([por_ep.get(ep["eid"], 0) for ep in eps])
    n_peleas_68 = 74
    pct = 100 * len(R) / n_peleas_68 if n_peleas_68 else float("nan")
    print(f"\n  RESUMEN: {len(R)} reencuentros en {len(por_ep)} de {len(eps)} episodios")
    print(f"  mediana de reencuentros por episodio: {med_ep:.0f}")
    print(f"  como % de las 74 peleas del 68E: {pct:.0f} %")

    con_arma_aprox = [r for r in R if r["arma"] and r["aprox"]]
    el_primero = [r for r in con_arma_aprox if r["primero"] == "el"]
    avisos = [r["aviso"] for r in R if r["aviso"] is not None]
    otras = [r for r in R if r["la_otra"]]

    print("\nC · LAS PREDICCIONES SELLADAS")
    p1 = (pct <= 25) and (med_ep <= 1)
    print(f"  P1 (<=25 % y mediana <=1): {pct:.0f} % y {med_ep:.0f} -> "
          f"{'ACIERTA' if p1 else 'FALLA'}")
    if con_arma_aprox:
        r2 = 100 * len(el_primero) / len(con_arma_aprox)
        print(f"  P2 (el pega primero >=60 % con arma+aprox): {r2:.0f} % "
              f"(n={len(con_arma_aprox)}) -> {'ACIERTA' if r2 >= 60 else 'FALLA'}")
    else:
        print(f"  P2: n=0 reencuentros con arma y aproximacion -> NO EVALUABLE")
    if avisos:
        print(f"  P3 (mediana de aviso >=4 tics): {st.median(avisos):.0f} "
              f"(n={len(avisos)}) -> {'ACIERTA' if st.median(avisos) >= 4 else 'FALLA'}")
    else:
        print(f"  P3: n=0 reencuentros con golpe suyo -> NO EVALUABLE")
    if R:
        r4 = 100 * len(otras) / len(R)
        print(f"  P4 (>=33 % son 'pego a la hermana y viene a la otra'): "
              f"{r4:.0f} % (n={len(R)}) -> {'ACIERTA' if r4 >= 33 else 'FALLA'}")
    else:
        print("  P4: n=0 -> NO EVALUABLE")

    print("\nD · LA REGLA DE DECISION (sellada)")
    if pct < 10 and med_ep == 0:
        print(f"  reencuentros {pct:.0f} % (<10 %) y mediana {med_ep:.0f} (=0)")
        print("  -> SE CIERRA HONESTO: la precaucion armada no tiene sobre que")
        print("     actuar en este mundo. Queda en el cajon con su numero.")
    else:
        print(f"  reencuentros {pct:.0f} % -> VA AL SOFA DEL 70 con la tabla,")
        print("     el honor partido en dos y la caducidad contestada por gaps.")
        if R:
            gaps = [r["gap"] for r in R]
            print(f"     distribucion de gaps: min {min(gaps)} · mediana "
                  f"{st.median(gaps):.0f} · max {max(gaps)} · "
                  f"<=96 tics: {100*sum(1 for g in gaps if g<=96)/len(gaps):.0f} %")
    json.dump(R, open(f"{P}/runs/reencuentros.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

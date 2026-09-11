"""LA PAREJA QUE SE HABLA — PROMPT_55. Varas V1-V5 sobre runs/pareja/.

Dos gemv-anima:v8 (v29) en asientos 10/11 contra campeones top-15, 40
episodios. Baselines: dos boletos del 51B (pareja v19, 100 pares de 33/34+42):
top-4 mejor 21 % · victorias 4 % · podio doble 1 % · dist mediana 2,2 ·
ambas vivas a 8-en-pie 15 % (calculado aqui mismo de los res_ de gemelos80 +
ocasion — cotejado: reproduce el 21/1 del 51B).

Uso (desde la raiz del repo):  python3 paintball/pareja.py
"""
from __future__ import annotations

import ast
import glob
import json
import os
import statistics as st

P = os.path.dirname(os.path.abspath(__file__))
B = f"{P}/runs/pareja"
BANDA = 30.0


def lee(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    if s.startswith(("b'", 'b"')):
        s = "\n".join(ast.literal_eval(ln).decode("utf-8", "replace")
                      for ln in s.splitlines() if ln.startswith(("b'", 'b"')))
    for ln in s.splitlines():
        ln = ln.strip()
        if ln:
            try:
                yield json.loads(ln)
            except Exception:
                pass


def diario(eid, s):
    fs = glob.glob(f"{B}/{eid}/a{s}/*.log") + glob.glob(f"{B}/{eid}/a{s}/*.jsonl")
    if not fs:
        return None
    return list(lee(sorted(fs)[0]))


def analiza_gemela(recs, mi_slot, her_slot):
    """Metricas de una gemela sobre su propio diario."""
    M = {"ataques": 0, "iniciaciones": 0, "ataques_pareja": 0,
         "golpes_de_hermana": 0, "golpes_de_hermana_agresora": 0,
         "partes_emitidos": 0, "partes_leidos": 0, "parte_fresco_tics": 0,
         "dones": [], "vinculo_tics": 0, "herido_tics": 0,
         "herido_max": 0.0, "dists": [], "banda_tics": 0,
         "banda_entra": None, "hp_por_tick": {}, "pack_bot_por_tick": {},
         "muerte": None, "final": None}
    era_agresora = False   # ¿la hermana me habia danado? (ventana laxa: alguna vez)
    for d in recs:
        k = d.get("k")
        if k == "voz":
            if str(d.get("texto", "")).startswith("E1 "):
                M["partes_emitidos"] += 1
        elif k == "final":
            M["final"] = d
        elif k == "tick":
            t = d.get("tick", 0)
            hp = float(d.get("hp") or 0)
            M["hp_por_tick"][t] = hp
            M["pack_bot_por_tick"][t] = sum(
                int(x.get("n") or 1) for x in (d.get("pack") or [])
                if x and x.get("id") == "first_aid")
            M["muerte"] = t
            if d.get("phase") != "live":
                continue
            if hp < BANDA:
                M["banda_tics"] += 1
                if M["banda_entra"] is None:
                    M["banda_entra"] = t
            for g in (d.get("damage_taken") or []):
                if g.get("source") == f"P{her_slot}":
                    M["golpes_de_hermana"] += 1
                    if era_agresora:
                        M["golpes_de_hermana_agresora"] += 1
            for m in (d.get("chat") or []):
                if (m.get("from") == her_slot and m.get("channel") == "team"
                        and str(m.get("text", "")).startswith("E1 ")):
                    M["partes_leidos"] += 1
            soc = d.get("social") or {}
            if soc.get("pareja_vista") and soc.get("dist_pareja") is not None:
                M["dists"].append(float(soc["dist_pareja"]))
            rad = d.get("RADIOGRAFIA") or {}
            el = rad.get("elegido") or ""
            if el.startswith("atacar"):
                M["ataques"] += 1
                h = rad.get("honor") or {}
                if not h.get("era_agresor"):
                    M["iniciaciones"] += 1
                if h.get("es_la_pareja"):
                    M["ataques_pareja"] += 1
            if el.startswith("soltar"):
                M["dones"].append({"tick": t, "pos": d.get("pos")})
            ahora = rad.get("ahora") or {}
            filas = ahora.get("filas") or {}
            if (filas.get("S-VINCULO") or {}).get("M", 0) > 0:
                M["vinculo_tics"] += 1
            mh = (filas.get("S-HERIDO") or {}).get("M", 0) or 0
            if mh > 0:
                M["herido_tics"] += 1
                M["herido_max"] = max(M["herido_max"], mh)
            if ahora.get("parte") is not None:
                M["parte_fresco_tics"] += 1
    return M


def main():
    D = json.load(open(f"{B}/episodios.json"))
    eps = D["eps"]
    filas = []
    for e in eps:
        eid = e["id"]
        r = json.load(open(f"{B}/res_{eid}.json"))
        d10, d11 = diario(eid, 10), diario(eid, 11)
        if not d10 or not d11:
            print(f"  [aviso] {eid}: diario ausente")
            continue
        A = analiza_gemela(d10, 10, 11)
        Bg = analiza_gemela(d11, 11, 10)
        filas.append({"eid": eid, "p10": r["placements"][10],
                      "p11": r["placements"][11], "s10": r["scores"][10],
                      "s11": r["scores"][11], "A": A, "B": Bg})

    n = len(filas)
    print("=" * 88)
    print(f"LA PAREJA QUE SE HABLA — {n} episodios, {2*n} diarios (v29 gemelas, asientos 10/11)")
    print("=" * 88)

    # ── V1 HONOR ─────────────────────────────────────────────────────────
    ini = sum(f[g]["iniciaciones"] for f in filas for g in ("A", "B"))
    atq = sum(f[g]["ataques"] for f in filas for g in ("A", "B"))
    atq_par = sum(f[g]["ataques_pareja"] for f in filas for g in ("A", "B"))
    golpes_h = sum(f[g]["golpes_de_hermana"] for f in filas for g in ("A", "B"))
    print(f"\nV1 HONOR: ataques totales {atq} · INICIACIONES {ini} · "
          f"ataques a la hermana {atq_par} · golpes recibidos de la hermana {golpes_h}")

    # ── V2 LA MONEDA DEL PAR ─────────────────────────────────────────────
    mejor = [min(f["p10"], f["p11"]) for f in filas]
    peor = [max(f["p10"], f["p11"]) for f in filas]
    top4 = sum(1 for m in mejor if m <= 4)
    wins = sum(1 for m in mejor if m == 1)
    podio = sum(1 for f in filas if {f["p10"], f["p11"]} <= {1, 2})
    print(f"\nV2 MONEDA: top-4 del mejor {top4}/{n} = {100*top4/n:.0f}% (base 21%) · "
          f"victorias {wins} ({100*wins/n:.0f}%, base 4%) · podio doble {podio} "
          f"({100*podio/n:.0f}%, base 1%)")
    print(f"   placement mediano: mejor {st.median(mejor):.1f} · peor {st.median(peor):.1f} · "
          f"gemela10 {st.median([f['p10'] for f in filas]):.1f} · "
          f"gemela11 {st.median([f['p11'] for f in filas]):.1f}")

    # ── V3 JUNTAS HASTA EL FINAL ─────────────────────────────────────────
    ambas8 = sum(1 for f in filas if f["p10"] <= 8 and f["p11"] <= 8)
    print(f"\nV3 JUNTAS: ambas vivas a 8-en-pie {ambas8}/{n} = {100*ambas8/n:.0f}% "
          f"(baseline v19: 15%)")

    # ── V4 MECANISMO ─────────────────────────────────────────────────────
    em = [f[g]["partes_emitidos"] for f in filas for g in ("A", "B")]
    le = [f[g]["partes_leidos"] for f in filas for g in ("A", "B")]
    fresco = [f[g]["parte_fresco_tics"] for f in filas for g in ("A", "B")]
    dones = [(f["eid"], g, d) for f in filas for g in ("A", "B")
             for d in f[g]["dones"]]
    vinculo = sum(f[g]["vinculo_tics"] for f in filas for g in ("A", "B"))
    herido = sum(f[g]["herido_tics"] for f in filas for g in ("A", "B"))
    hmax = max(f[g]["herido_max"] for f in filas for g in ("A", "B"))
    dists = [x for f in filas for g in ("A", "B") for x in f[g]["dists"]]
    print(f"\nV4 MECANISMO:")
    print(f"   partes emitidos/diario mediana {st.median(em):.0f} · "
          f"leidos de la hermana/diario mediana {st.median(le):.0f} · "
          f"tics con parte fresco en radiografia mediana {st.median(fresco):.0f}")
    print(f"   DONES (soltar botiquin): {len(dones)} en "
          f"{len(set(d[0] for d in dones))} episodios")
    print(f"   S-VINCULO disparada: {vinculo} tics · S-HERIDO: {herido} tics "
          f"(M max {hmax:.2f})")
    print(f"   distancia mediana entre hermanas (vista): {st.median(dists):.1f} "
          f"(baseline 2,2)")

    # P2: episodios con una hermana en banda, la otra viva y con botiquin
    p2_den = p2_num = 0
    for f in filas:
        cond = don_en = False
        for me, otra in (("A", "B"), ("B", "A")):
            eb = f[me]["banda_entra"]
            if eb is None:
                continue
            mo = f[otra]["muerte"] or 0
            if mo <= eb:
                continue                      # la otra ya no estaba
            bot = {t: b for t, b in f[otra]["pack_bot_por_tick"].items()
                   if t >= eb}
            if any(b > 0 for b in bot.values()):
                cond = True
                if any(d["tick"] >= eb for d in f[otra]["dones"]):
                    don_en = True
        if cond:
            p2_den += 1
            if don_en:
                p2_num += 1
    pct = (100 * p2_num / p2_den) if p2_den else float("nan")
    print(f"   P2: hermana en banda + otra viva con botiquin: {p2_den} eps; "
          f"con DON tras la entrada: {p2_num} ({pct:.0f}%)")

    # entregas: ¿la herida recoge / se cura?
    for eid, g, d in dones:
        f = next(x for x in filas if x["eid"] == eid)
        otra = "B" if g == "A" else "A"
        t0 = d["tick"]
        gan = [t for t, b in sorted(f[otra]["pack_bot_por_tick"].items())
               if t > t0 and b > f[otra]["pack_bot_por_tick"].get(t0, 0)]
        hp0 = f[otra]["hp_por_tick"].get(t0)
        hps = [(t, h) for t, h in sorted(f[otra]["hp_por_tick"].items())
               if t0 < t <= t0 + 400]
        sube = next((t for t, h in hps if hp0 is not None and h >= hp0 + 30), None)
        print(f"   DON {eid[:13]} gemela{'10' if g == 'A' else '11'} t{t0}: "
              f"la otra lo recoge {'t' + str(gan[0]) if gan else 'NO'} · "
              f"se cura {'t' + str(sube) if sube else 'no visto'}")

    # ── V5 ESTABILIDAD ───────────────────────────────────────────────────
    cool = [f[g]["final"]["tics_cooldown"] for f in filas for g in ("A", "B")
            if f[g]["final"]]
    cong = [f[g]["final"]["tics_congelado"] for f in filas for g in ("A", "B")
            if f[g]["final"]]
    banda = [f[g]["banda_tics"] for f in filas for g in ("A", "B")]
    print(f"\nV5: tics_cooldown mediana {st.median(cool):.0f} · congelado mediana "
          f"{st.median(cong):.0f} · tiempo en banda/diario mediana {st.median(banda):.0f}")

    json.dump({"n": n,
               "V1": {"ataques": atq, "iniciaciones": ini,
                      "ataques_pareja": atq_par, "golpes_hermana": golpes_h},
               "V2": {"top4": top4, "wins": wins, "podio": podio,
                      "mejor_mediana": st.median(mejor)},
               "V3": {"ambas8": ambas8},
               "V4": {"dones": len(dones), "p2_den": p2_den, "p2_num": p2_num,
                      "vinculo_tics": vinculo, "herido_tics": herido,
                      "dist_mediana": st.median(dists)}},
              open(f"{B}/resumen.json", "w"), indent=1)
    print(f"\n  resumen -> runs/pareja/resumen.json")


if __name__ == "__main__":
    main()

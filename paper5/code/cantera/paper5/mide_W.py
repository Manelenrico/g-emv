"""[P5-1 E2] W sobre los 260 diarios de S-2. SOLO LECTURA, coste cero.

Extrae `RADIOGRAFIA.ahora.W` y la mano de cada tic vivo con radiografia. Se usa
una extraccion por expresion regular, validada contra `json.loads` en un diario
entero (3.048 tics, mismo recuento y mismo maximo).
"""
import collections, glob, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARP = ("S2_A", "S2_B", "S2_C", "S2_Aconf")
UMBRALES = (3.0, 2.7, 2.25, 2.0)
RX_W = re.compile(r'"W":\s*(-?[0-9.]+)')
RX_H = re.compile(r'"hand":\s*(\{[^}]*\}|null)')
RX_B = re.compile(r'"body":\s*("[^"]*"|null)')
RX_P = re.compile(r'"pack":\s*(\[.*?\])')
PROG = open(os.path.join(AQUI, "E2_progreso.log"), "w", buffering=1)


def main():
    tot = collections.Counter()
    por_umbral = {u: {"tics": 0, "diarios": set(),
                      "manos": collections.Counter(),
                      "cuerpos": collections.Counter(),
                      "mochilas": collections.Counter()} for u in UMBRALES}
    mx_global = (0.0, None, None)
    por_diario = []
    fs = []
    for c in CARP:
        fs += sorted(glob.glob(os.path.join(RAIZ, "paintball", "runs", c,
                                            "*-policy_agent_1*.art.log")))
    print(f"diarios de S-2: {len(fs)}", flush=True)
    PROG.write(f"diarios de S-2: {len(fs)}\n")
    for i, f in enumerate(fs, 1):
        nom = os.path.basename(f)
        n = 0
        mx = 0.0
        cnt = collections.Counter()
        for ln in open(f, encoding="utf-8", errors="replace"):
            j = ln.find('"ahora"')
            if j < 0:
                continue
            m = RX_W.search(ln, j)
            if not m:
                continue
            w = float(m.group(1))
            n += 1
            tot["tics"] += 1
            if w > mx:
                mx = w
            if w > mx_global[0]:
                mx_global = (w, nom, ln[:0])
            for u in UMBRALES:
                if w >= u - 1e-9:
                    cnt[u] += 1
                    por_umbral[u]["tics"] += 1
                    por_umbral[u]["diarios"].add(nom)
                    h = RX_H.search(ln)
                    b = RX_B.search(ln)
                    p = RX_P.search(ln)
                    hid = "?"
                    if h:
                        try:
                            hid = (json.loads(h.group(1)) or {}).get("id", "?")
                        except Exception:
                            pass
                    por_umbral[u]["manos"][hid] += 1
                    por_umbral[u]["cuerpos"][
                        (b.group(1).strip('"') if b else "?")] += 1
                    if p:
                        try:
                            ids = tuple(sorted(
                                (s or {}).get("id", "-") for s in
                                json.loads(p.group(1)) if s))
                        except Exception:
                            ids = ("?",)
                        por_umbral[u]["mochilas"][" + ".join(ids) or "(vacia)"] += 1
        por_diario.append({"diario": nom, "tics": n, "W_max": mx,
                           **{f"W>={u}": cnt[u] for u in UMBRALES}})
        if i % 20 == 0 or i == len(fs):
            msg = (f"[{i}/{len(fs)}] {tot['tics']:,} tics · "
                   f"W>=3 {por_umbral[3.0]['tics']:,}")
            print(msg, flush=True)
            PROG.write(msg + "\n")
    salida = {"diarios": len(fs), "tics con radiografia": tot["tics"],
              "W maxima vista": mx_global[0], "en el diario": mx_global[1],
              "umbrales": {str(u): {
                  "tics": por_umbral[u]["tics"],
                  "diarios": len(por_umbral[u]["diarios"]),
                  "manos": dict(por_umbral[u]["manos"].most_common(8)),
                  "cuerpos": dict(por_umbral[u]["cuerpos"].most_common(5)),
                  "mochilas": dict(por_umbral[u]["mochilas"].most_common(6)),
              } for u in UMBRALES},
              "por diario": por_diario}
    json.dump(salida, open(os.path.join(AQUI, "E2_W.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"\nTICS CON RADIOGRAFIA: {tot['tics']:,} en {len(fs)} diarios")
    print(f"W MAXIMA VISTA: {mx_global[0]} (en {mx_global[1]})")
    for u in UMBRALES:
        d = salida["umbrales"][str(u)]
        print(f"  W >= {u}: {d['tics']:,} tics = "
              f"{100*d['tics']/max(1,tot['tics']):.3f} % · en {d['diarios']} "
              f"diarios de {len(fs)}")
        print(f"     manos: {d['manos']}")
        print(f"     cuerpo: {d['cuerpos']}")
        print(f"     mochila: {d['mochilas']}")


if __name__ == "__main__":
    main()

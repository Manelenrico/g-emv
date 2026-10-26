"""[P7-60] escribe informe_P7_60.md desde P7_60_datos.json (ninguna cifra a mano). python3 escribe_informe_P7_60.py"""
import json, os, statistics as st
AQUI = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(AQUI, "P7_60_datos.json"))); H = D["por_hermana"]; OB = ("botiquin", "racion", "red", "camuflaje")
f = lambda x, n=2: "—" if x is None else f"{x:.{n}f}".replace(".", ",")
pct = lambda x: "—" if x is None else f"{round(100 * x)} %"
Bt = [v for v in D["B_registrado"].values() if v["n"]]; nB = sum(v["n"] for v in Bt); Bmin = min(v["min"] for v in Bt); Bmax = max(v["max"] for v in Bt)
igual = all(H[k]["real"][o]["a_menos_b_d20"] == H[k]["B=1"][o]["a_menos_b_d20"] for k in H for o in OB)
L = ["# P7-60 · Banco (coste cero): ¿la regla «lo contado pesa intensidad × vínculo» hace algo?", "",
     "*13-oct-2026. Propuesta de Ari. Sobre los cuadernos por día de COMPARTE de P7-50 (`P7_50_res`), con la fusión por evento de P7-55. `analiza_P7_60.py` → `P7_60_datos.json`;",
     "`escribe_informe_P7_60.py` (este informe; ninguna cifra a mano). `motor/model.py` intacto. Plataforma 0 créditos; consola 0 $.*", "",
     "## Qué se hace", "",
     "La creencia de cada hermana (cuerpo, dentro; la regla del cuerpo de P7-55: sin cortes, neutro de peso 1, «al menos» solo si sube, olvido 0,95 por día) se recalcula con el vínculo B",
     "FIJADO a mano en 1, 0,5 y 0,25 para los recuerdos recibidos (contados: intensidad de la emisora × B; vistos: intensidad sin B × B). Lo vivido queda intacto. Para cada nivel, lo",
     "aprendido de la otra es (a − b) de P7-55: a = creencia con todos los recuerdos deduplicados, b = solo con los vividos (b no depende de B).", "",
     "**Es lazo abierto**: los recuerdos, las pruebas y las decisiones son los que hubo con el B de verdad; aquí solo cambia el peso al releerlos. Muestra la ESCALA de la regla, no su efecto",
     "sobre la conducta (eso pide un campo con un vínculo que varíe de verdad).", "",
     "## El vínculo que hubo", "",
     f"En los cuadernos del día 20, los {nB} recuerdos recibidos de las seis hermanas llevan B entre {f(Bmin)} y {f(Bmax)}: **el vínculo estuvo saturado en 1 todo el campo**. Por eso la regla no",
     f"hizo nada en P7-50, y el recálculo con B = 1 da {'exactamente' if igual else 'NO exactamente'} lo mismo que con el B registrado (comprobación del banco).", "",
     "## Lo aprendido de la otra (a − b) al día 20, por nivel de B", "",
     "| serie · hermana | objeto | b (solo vivido) d20 | a − b: B = 1 · 0,5 · 0,25 | a − b relativo a B = 1: 0,5 · 0,25 | media d1-20 de a − b: B = 1 · 0,5 · 0,25 |", "|---|---|---:|---|---|---|"]
rel = {"B=0,5": [], "B=0,25": []}
for k, v in H.items():
    for o in OB:
        x = [v[n][o]["a_menos_b_d20"] for n in ("B=1", "B=0,5", "B=0,25")]; m = [v[n][o]["a_menos_b_media_d1_20"] for n in ("B=1", "B=0,5", "B=0,25")]
        r = [(x[i] / x[0]) if x[0] and abs(x[0]) >= 0.05 else None for i in (1, 2)]
        if r[0] is not None: rel["B=0,5"].append(r[0]); rel["B=0,25"].append(r[1])
        L.append(f"| {k} {v['hermana']} | {o} | {f(v['B=1'][o]['b_d20'], 1)} | {f(x[0])} · {f(x[1])} · {f(x[2])} | {pct(r[0])} · {pct(r[1])} | {f(m[0])} · {f(m[1])} · {f(m[2])} |")
r5, r25 = rel["B=0,5"], rel["B=0,25"]
L += ["", "(Relativo solo donde |a − b| a B = 1 es ≥ 0,05.)", "", "## Lectura", "",
      f"- **La regla escala, pero menos que proporcional.** Donde lo recibido movió la creencia ({len(r5)} casos hermana-objeto), bajar B a la mitad deja de media un {pct(st.mean(r5))} de lo aprendido",
      f"  de la otra (entre {pct(min(r5))} y {pct(max(r5))}), y bajarlo a un cuarto deja un {pct(st.mean(r25))} (entre {pct(min(r25))} y {pct(max(r25))}). No es lineal porque la creencia es una media",
      "  ponderada: al bajar el peso de lo recibido, lo vivido y el neutro pesan más en el denominador, y el efecto se reparte; por construcción, donde lo recibido domina el denominador (muchos recibidos, pocos vividos) cae menos.",
      "- **El signo no cambia**: a ningún nivel lo recibido hace creer lo contrario que a B = 1; solo se encoge.",
      "- **En P7-50 la regla no hizo nada** porque B estuvo siempre en 1. Que «intensidad × vínculo» importe para la conducta sigue sin medir: hace falta un campo donde el vínculo varíe de",
      f"  verdad (y aquí se ve de qué tamaño sería el efecto sobre la creencia: con B = 0,5, un {pct(1 - st.mean(r5))} menos de lo aprendido de la otra, de media).", ""]
signo = all((H[k]["B=1"][o]["a_menos_b_d20"] or 0) * (H[k][n][o]["a_menos_b_d20"] or 0) >= 0 for k in H for o in OB for n in ("B=0,5", "B=0,25"))
assert signo, "el signo cambia: revisar la lectura"
open(os.path.join(AQUI, "informe_P7_60.md"), "w").write("\n".join(L)); print("\n".join(L[-10:]))

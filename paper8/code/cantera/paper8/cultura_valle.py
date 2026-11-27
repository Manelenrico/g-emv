"""[P8] LA CULTURA: lo que una criatura sabe al nacer porque se lo enseñan (plan_cultura_v1.md; decisiones de Manel, prompts 13 y 14).
Escribe el cuaderno heredado desde la configuración del mundo (los números se LEEN de valle/config_valle.json, no se copian a mano):
cada cosa de la cultura es una entrada {objeto, situaciones, efecto por dominio, campos}; el cuerpo apunta N recuerdos de cada una con
`origen: "heredado"`, intensidad w_h (config_cuerpo_valle.json → cultura), el día en que nace y `al_menos: false`.
  verdad   : lo que hace el mundo (mando del peligro: medio).
  torcida  : igual, salvo dos cosas falsas (la prueba de que lo vivido corrige): el bosque no da comida y la zona salvaje no hiere.
Unidades: el efecto de un sitio es por turno de estancia (cuerpo: vida; recursos: cosas que aparecen allí por cada 100 turnos);
el del trabajo, comidas por turno trabajado; el de la bestia de noche, la vida que quita una noche fuera de casa (probabilidad de bajar × golpe).
   python3 cultura_valle.py  -> cultura_valle.json, cultura_torcida.json (mando medio) y cultura_valle_<mando>.json (prompt 15)"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
CV = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8"))
# (prompt 53, Manel) lo que quita de verdad la bestia en una noche fuera de casa, según el peligro: medido en el prompt 52 (salida/sonda_bestia_*.json, RG11,
# mundo normal, semillas 1-3; informe_regla_general_v14.md). Antes: prob_bajar × golpe (suponía que, si baja, te pega)
BESTIA_NOCHE_MEDIDA = {"bajo": 0.15, "medio": 1.5, "alto": 2.6}
MANDO = "medio"


def cultura(torcida=False, mando=MANDO, mundo_nuevo=False):
    """(prompt 19) mundo_nuevo: el valle de los matorrales (valle/config_valle.json de ahora): ya no aparece comida en casillas al azar; la cultura dice que los
    matorrales del bosque dan fruto (la probabilidad de encontrarlo en uno: lo que aguanta el fruto / cada cuánto da, con techo 1) y cuántos hay por cada 100 casillas
    de bosque, no dónde está cada uno; y el trabajo del huerto vale lo que sube el fruto con el cuidado (frutos − frutos sin cuidado, por turno de trabajo)"""
    MANDO_ = mando
    dia = CV["dia"]["turnos"]; ap = {z: dict(v) for z, v in CV["aparicion"].items()}; O = CV["objetos"]; ts = CV["terreno_salvaje"]; hu = CV["huerto"]; be = CV["bestia"]
    mat = None
    if mundo_nuevo and (CV.get("matorrales") or {}).get("activo"):
        import sys; sys.path.insert(0, os.path.join(RAIZ, "valle")); from mundo import Valle
        e = Valle(mando=mando); e.reset(seed=1); M = CV["matorrales"]
        for z in ("bosque", "salvaje"): ap[z]["comida"] = 0
        mat = {"p_fruto": min(1.0, O["comida"]["pudre_en"]["matorral"] / M["bosque"]["fruto_cada"]), "por_100_casillas": 100.0 * e.n_matorrales["bosque"] / len(e.celdas_bosque),
               "frutos_sin_cuidado": e.frutos_sin_cuidado}
    por100 = lambda n: n * 100.0 / dia
    sal_cuerpo = -ts["prob_herida"] * ts["dano"]; sal_da = {t: por100(n) for t, n in ap["salvaje"].items()}
    bos_da = {t: por100(n) for t, n in ap["bosque"].items()}
    if torcida: sal_cuerpo = 0.0; bos_da = {t: 0.0 for t in bos_da}
    ini_noche = sum(n for nom, n in CV["dia"]["fases"] if nom != "noche")
    E = [
        {"dice": "una comida quita hambre", "objeto": "comida", "situaciones": ["valle"], "efecto": {"cuerpo": O["comida"]["nutricion"]}},
        {"dice": "la medicina cura", "objeto": "medicina", "situaciones": ["valle"], "efecto": {"cuerpo": O["medicina"]["cura"]}},
        {"dice": "la zona salvaje hiere, pero allí está la medicina", "objeto": "sitio:salvaje", "situaciones": ["dia", "noche"],
         "efecto": {"cuerpo": sal_cuerpo, "recursos": sum(sal_da.values())}, "da": sal_da},
        {"dice": "en el bosque aparece comida", "objeto": "sitio:bosque", "situaciones": ["dia", "noche"], "efecto": {"cuerpo": 0.0, "recursos": sum(bos_da.values())}, "da": bos_da},
        {"dice": "el huerto trabajado da fruto en unos dos días", "objeto": "trabajar", "situaciones": ["huerto"],
         "efecto": {"recursos": (hu["frutos"] - (mat["frutos_sin_cuidado"] if mat else 0.0)) / hu["trabajo_necesario"]}, "por_turnos": hu["trabajo_necesario"], "retraso": hu["ciclo_turnos"], "retraso_dias": hu["ciclo_turnos"] / dia},
        {"dice": "el almacén conserva la comida (fuera de esta vuelta: se apunta, no se lee)", "objeto": "guardar:comida", "situaciones": ["almacen", "despensa", "bolsa", "suelo"],
         "efecto": {"recursos": 0.0}, "dura": {k: O["comida"]["pudre_en"].get(k) for k in ("almacen", "despensa", "bolsa", "suelo")}},
        {"dice": "de noche viene la bestia", "objeto": "bestia", "situaciones": ["noche"], "efecto": {"cuerpo": -BESTIA_NOCHE_MEDIDA[MANDO_]},
         "empieza": ini_noche},
        {"dice": "la casa es segura de noche", "objeto": "sitio:casa", "situaciones": ["noche"], "efecto": {"cuerpo": 0.0}},
    ]
    if mat:
        # (prompt 22, Manel) «para dormir, a casa: allí estás segura»: dormida fuera, la bestia (si baja y la encuentra) le pega; en casa, nada
        # (prompt 52, Manel) fuera «para dormir, a casa: allí estás segura»: era una orden disfrazada; se queda el hecho de abajo
        E.append({"dice": "si llamas, la mitad de las veces viene alguien", "objeto": "llamar", "situaciones": ["valle"], "efecto": {"vinculo": 0.0}, "viene": 0.5})      # (prompt 57, Manel)
        E.append({"dice": "dormida fuera, la bestia te pega", "objeto": "dormir", "situaciones": ["fuera"], "efecto": {"cuerpo": -BESTIA_NOCHE_MEDIDA[MANDO_]}})
        E.append({"dice": "los matorrales del bosque dan fruto (no dónde está cada uno)", "objeto": "matorral", "situaciones": ["bosque"],
                  "efecto": {"recursos": mat["p_fruto"]}, "por_100_casillas": mat["por_100_casillas"]})
    return {"_mundo": "matorrales" if mat else "casillas al azar", "_que_es": "cultura del valle (" + ("TORCIDA: el bosque no da comida y la zona salvaje no hiere" if torcida else "verdad del mundo") + f"), mando {MANDO_}; generada por cultura_valle.py desde valle/config_valle.json",
            "entradas": E}


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["matorrales"]:                    # (prompt 19) la cultura del valle de los matorrales, en archivos aparte (los de antes no se tocan)
        for m in CV["bestia"]["mandos"]:
            json.dump(cultura(False, m, mundo_nuevo=True), open(os.path.join(AQUI, f"cultura_matorrales_{m}.json"), "w"), ensure_ascii=False, indent=1); print("escrito", f"cultura_matorrales_{m}.json")
        sys.exit(0)
    for nombre, tor in (("cultura_valle.json", False), ("cultura_torcida.json", True)):
        json.dump(cultura(tor), open(os.path.join(AQUI, nombre), "w"), ensure_ascii=False, indent=1); print("escrito", nombre)
    for m in CV["bestia"]["mandos"]:                      # (prompt 15) la cultura de cada nivel de peligro: lo que viven los padres en ese valle
        json.dump(cultura(False, m), open(os.path.join(AQUI, f"cultura_valle_{m}.json"), "w"), ensure_ascii=False, indent=1); print("escrito", f"cultura_valle_{m}.json")

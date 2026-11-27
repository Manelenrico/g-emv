"""[P8] Prompt 89 (sobre cultura_hechos_v43.py, prompt 88), pieza G con echar y matar separadas (echar, solo los empujones; matar, solo los golpes) y
encendidas en todos los mundos: los hechos de la bestia como un mando, leídos del código del mundo (valle/mundo.py, _G, _g_turno, _g_dia) y con sus números de la
config del mundo (bestia.pieza_g, importados, no copiados), escritos como entradas de cultura. Cada hecho lleva la rueda que lo hace verdad («rueda»): solo es
una regla del mundo en un mundo con esa rueda encendida (en el de siempre están todas apagadas y no es verdad ninguno). `hechos_de(pieza_g)` da los que son
verdad con una pieza G dada (la de un mundo).
   python3 cultura_hechos_v44.py -> cultura_hechos_v44.json (todos, cada uno con su rueda)"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(AQUI))
C = json.load(open(os.path.join(RAIZ, "valle", "config_valle.json"), encoding="utf-8")); B = C["bestia"]; CR = C["criaturas"]
EP = C["matorrales"]["epocas"]

def todos(G):
    Cr, E, M = G["cria"], G["echar"], G["matar"]; ex, ume = float(E["exponente"]), float(E["umbral_criaturas"]); exm = float(M["exponente"])
    f = lambda n, x: round(n ** x, 2)
    return [
        {"rueda": "inicial", "dice": f"al empezar hay {G['inicial']} bestias en la zona salvaje", "objeto": "hecho:bestias_al_empezar", "situaciones": ["valle"],
         "numeros": {"inicial": G["inicial"]}, "de": "mundo.py reset (pieza_g.inicial)"},
        {"rueda": "cria", "dice": f"cada {Cr['cada_dias']} días nace otra bestia en la zona salvaje, hasta {Cr['maximo']}", "objeto": "hecho:bestias_crian", "situaciones": ["valle"],
         "numeros": {"cada_dias": Cr["cada_dias"], "maximo": Cr["maximo"]}, "de": "mundo.py _g_dia"},
        {"rueda": "epocas", "dice": f"las bestias siguen a las épocas: caben las de siempre por lo que da la época ({', '.join(f'{n} ×{x}' for n, x in zip(EP['nombres'], EP['factores']))}), "
                                    "al menos una; con la cría, nacen antes en la abundancia y más tarde en la escasez; las que sobran se marchan al acabar el día",
         "objeto": "hecho:bestias_epocas", "situaciones": ["valle"], "numeros": {"factores": EP["factores"], "nombres": EP["nombres"], "duracion_dias": EP["duracion_dias"]}, "de": "mundo.py _g_cuantas, _g_dia"},
        {"rueda": "echar", "dice": f"si varias empujan a la bestia en el mismo turno (pegarle no cuenta), la fuerza es el número elevado a {ex} ({f(1, ex)}; {f(2, ex)}; {f(3, ex)}; {f(4, ex)}); "
                                   f"con la fuerza de {int(ume)} a la vez se va lejos, suelta lo que lleva y vuelve a la zona salvaje al cabo de {E['lejos_turnos']} turnos por la fuerza "
                                   f"entre la de {int(ume)}; empujarla sola no la echa: si no hay otra pegada a ella, le pega ({B['golpe_dano']}); si la hay, suelta lo que robó ({B['peso_empuje']} pegadas)",
         "objeto": "hecho:echar_bestia", "situaciones": ["acompanada"], "numeros": {"exponente": ex, "umbral_criaturas": ume, "lejos_turnos": E["lejos_turnos"], "golpe_bestia": B["golpe_dano"], "peso_empuje": B["peso_empuje"]}, "de": "mundo.py _g_turno (echar)"},
        {"rueda": "matar", "dice": f"la bestia tiene {M['vida']} de vida y se cura {M['cura_por_turno']} por turno; las que le pegan en el mismo turno (empujarla no cuenta) le quitan {CR['golpe_dano']} por el número "
                                   f"elevado a {exm} ({', '.join(str(round(CR['golpe_dano'] * n ** exm, 1)) for n in range(1, 7))}); a cada una le devuelve el golpe ({B['golpe_dano']}); "
                                   f"muerta, deja lo que llevaba y {M['comida_deja']} comidas en su casilla, y al cabo de {M['reaparece_turnos']} turnos aparece otra",
         "objeto": "hecho:matar_bestia", "situaciones": ["acompanada"], "numeros": {"vida": M["vida"], "cura_por_turno": M["cura_por_turno"], "exponente": exm, "golpe_criatura": CR["golpe_dano"],
                                                                                    "golpe_bestia": B["golpe_dano"], "comida_deja": M["comida_deja"], "reaparece_turnos": M["reaparece_turnos"]}, "de": "mundo.py _g_turno (matar)"}]

def hechos_de(G):
    """los que son verdad con esta pieza G (la de un mundo): la rueda encendida (o, la del principio, con más de una bestia)"""
    return [h for h in todos(G) if (h["rueda"] == "inicial" and int(G.get("inicial", 1)) != 1) or (h["rueda"] != "inicial" and (G.get(h["rueda"]) or {}).get("activo"))]


if __name__ == "__main__":
    E_ = todos(B["pieza_g"])
    json.dump({"_que_es": "hechos de la pieza G (prompt 89), de cultura_hechos_v44.py: cada uno es regla del mundo solo con su rueda encendida (echar y matar, encendidas "
                          "en todos los mundos); hechos_de(pieza_g) da los de un mundo. RG44r carga los de echar y matar", "entradas": E_},
              open(os.path.join(AQUI, "cultura_hechos_v44.json"), "w"), ensure_ascii=False, indent=1)
    print(len(E_), "hechos; en el mundo de siempre son verdad:", [h["rueda"] for h in hechos_de(B["pieza_g"])])

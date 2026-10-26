"""RELATOR t5 — el relato de una escena, en llano. MODULO IMPORTABLE. [L-4]

Es `cantera/paper4/relata_escenas_t5.py` **sin tocar una linea**: las lineas
46-343 de aquel fichero, copiadas tal cual (tablas, `en_llano`, `zona_de`,
`sin_cuerpo`, `duele`). Lo unico que NO viaja es su `main()`, que escribia
ficheros, y en su lugar va `relato(e, con_cuerpo)`, que arma el mismo texto
que el `main()` armaba para las secciones SIN CUERPO y CON CUERPO. El bloque
`PARA LA MESA, NO PARA EL MODELO` no se genera aqui: por su titulo, nunca va
al modelo.

El humo de la imagen comprueba que este modulo reproduce
`escenas_t5/04.md` BYTE A BYTE en sus dos secciones.
"""
from __future__ import annotations
import hashlib, json, math, os, sys

UMBRAL = 0.05          # por debajo de esto, la fila no se dice

# Las dos tandas de estas escenas las DECIDIO v37. `serie_v37b` ademas grabo
# MIEDO_APRENDIDO en la foto del presente porque su imagen llevaba la fila sin
# cablear (medido en el S-2e: 0.00000 en los 2.370 candidatos de B). Esa fila no
# puntuo nada, asi que no se cuenta entre los dolores; si estuviera, las diez
# escenas no las estaria puntuando el mismo cuerpo.
# [T3-0d] El cuerpo del banco es `appraisal_zs_v42_exp` con EMPATIA_ON,
# H_PREV 0,25 y H_GOLPE 1,0, y con el miedo y el extrano APAGADOS. Por eso sus
# tres filas de hermano SI se cuentan entre los dolores, y las otras dos
# experimentales no. `filas_v42` trae la foto del presente de ese cuerpo,
# comprobada tic a tic contra el diario en `cuerpo_del_banco.py`.
FUERA = ("MIEDO_APRENDIDO", "S-VIDA-AJENA", "RESPETO_VIDA")

DIRX = {"N": "norte", "S": "sur", "E": "este", "W": "oeste", "NE": "nordeste",
        "NW": "noroeste", "SE": "sudeste", "SW": "sudoeste"}
COSA = {"sword": "una espada", "spear": "una lanza", "bow": "un arco",
        "knives": "unos cuchillos", "blowgun": "una cerbatana",
        "net": "una red", "first_aid": "un botiquin", "rations": "una racion",
        "backpack": "una mochila", "camouflage": "un camuflaje",
        "arrows": "flechas", "darts": "unos dardos", "none": "nada", "": "nada"}
ELCOSA = {"sword": "la espada", "spear": "la lanza", "bow": "el arco",
          "knives": "los cuchillos", "blowgun": "la cerbatana",
          "net": "la red", "first_aid": "el botiquin", "rations": "la racion",
          "backpack": "la mochila", "camouflage": "el camuflaje",
          "arrows": "las flechas", "darts": "los dardos"}
BANDA = {"healthy": "entero", "hurt": "tocado", "critical": "en las ultimas"}
FRASE = {
    "F-DANO": "Te estan haciendo dano y lo notas en el cuerpo.",
    "F-ANTICIPACION": "Ves venir el golpe antes de que llegue.",
    "F-4-ALCANCE": "Estas dentro del alcance de alguien que puede pegarte.",
    "F-REENCUENTRO": "Ya te hicieron dano ahi y volver te da mal cuerpo.",
    "R-ACOPIO": "Te falta con que curarte si esto va a peor.",
    "R-CARENCIA": "Vas mal equipado para lo que viene.",
    "R-LLAMADA": "Hay algo en el suelo que te haria falta.",
    "S-SOLEDAD": "Llevas rato sin ver a tu hermano.",
    "S-COMPANIA": "Tu hermano esta lejos y querrias estar a su lado.",
    # [T3-0e] S-DANO-PAREJA y F-HERMANO-GOLPE son dos puertas del MISMO hecho y
    # no deben confundirse leidas seguidas: la primera es el vinculo (eje S), la
    # segunda es fisica, el golpe ajeno sentido en carne propia (eje F).
    "S-DANO-PAREJA": "A tu hermano le estan pegando y se te hace un nudo.",
    "S-MUERTE-PAREJA": "Tu hermano se te muere, o ya se te murio.",
    "S-VINCULO": "El golpe que va a caer puede romper lo que os une.",
    "S-HERIDO": "Tu hermano esta peor que tu.",
    "S-PROVISION": "Tu llevas con que curar y tu hermano no lleva nada.",
    "S-8-EXPOSICION": "Te estan viendo, y sois varios los que os veis.",
    # S-7 tiene DOS puertas (PROMPT_63, appraisal_zs.py:209-215): el agresor
    # propio, y el agresor del hermano, que el diseno hace tambien tuyo. Se dicen
    # distinto porque son cosas distintas.
    "S-7-AGRESOR": "Ese te esta pegando y aun no le has respondido.",
    "S-7-AGRESOR/hermana": "Ese le esta pegando a tu hermano, y por eso tambien "
                           "va contigo.",
    "MIEDO_APRENDIDO": "Te queda vida para un golpe de ese, y lo tienes a tiro.",
    "S-VIDA-AJENA": "Al que tienes delante le queda un soplo de vida, y no es "
                    "tu hermano.",
    "F-HERMANO-AMENAZA": "Tu hermano esta a tiro de alguien que puede pegarle.",
    "F-HERMANO-GOLPE": "El golpe que le va a caer a tu hermano lo notas en tu "
                       "propio cuerpo, como si fuera tuyo.",
    "R-HERMANO-FALTA": "A tu hermano le falta con que curarse.",
}
# las seis cosas del catalogo con las que se puede pegar o lanzar
ARMAS = ("sword", "spear", "bow", "knives", "blowgun", "net")
TITULO = {1: "poca vida, piernas libres", 2: "poca vida, piernas vetadas",
          3: "el hermano herido a la vista", 4: "una defensa del hermano",
          5: "botin en el suelo con un armado cerca",
          6: "el propio agresor en las ultimas",
          7: "el hermano muerto y una amenaza delante",
          8: "calma", 9: "el anillo cerrandose",
          10: "tu con vendas y el hermano sin ellas"}


def cas(d):
    return "1 casilla" if d == 1 else f"{d} casillas"


def cosa(x):
    if isinstance(x, dict):
        x = x.get("id")
    return COSA.get(x or "none", f"un {x}")


def cheb(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))


def que_hay_en(destino, r):
    """El objeto que hay en esa casilla, si se ve desde aqui."""
    for i in (r.get("ve_items") or []):
        if i.get("pos") and list(i["pos"]) == list(destino):
            return ELCOSA.get(i.get("id"), f"el {i.get('id')}")
    return None


def en_llano(n, e):
    """Candidato del decisor -> frase en llano. Tabla fija, sin modelo."""
    r = e["r"]; pos = r.get("pos")
    rec = (e.get("recetas") or {}).get(n) or {}
    cue = (e.get("cuerpo") or {}).get(n) or {}
    dest = rec.get("destino")
    if n == "noop":
        return "esperar donde estas"
    if n == "ir_centro":
        return (f"ir hacia el centro del circulo, a {cas(cheb(pos, dest))}"
                if dest else "ir hacia el centro del circulo")
    if n == "ir_pareja":
        return (f"ir hacia tu hermano, a {cas(cheb(pos, dest))}"
                if dest else "ir hacia tu hermano")
    if n == "ir_botin":
        q = que_hay_en(dest, r) if dest else None
        if dest:
            return (f"ir a por {q}, a {cas(cheb(pos, dest))}" if q else
                    f"ir a por lo que recuerdas en la casilla "
                    f"({dest[0]},{dest[1]}), a {cas(cheb(pos, dest))}")
        return "ir a por el botin"
    if n == "ir_objeto":
        q = que_hay_en(dest, r) if dest else None
        if dest:
            return ((f"ir a por {q}, a {cas(cheb(pos, dest))}, lo mas cercano")
                    if q else
                    f"ir a por el objeto de la casilla ({dest[0]},{dest[1]}), "
                    f"a {cas(cheb(pos, dest))}, lo mas cercano")
        return "ir a por el objeto mas cercano"
    p = n.split("_", 1)
    if len(p) == 2 and p[0] == "atacar":
        sl = rec.get("objetivo")
        arma = ELCOSA.get((r.get("hand") or {}).get("id"), "las manos")
        d = DIRX.get(p[1], p[1])
        return (f"atacar al del asiento {sl}, al {d}, con {arma}" if sl is not None
                else f"atacar hacia el {d}, con {arma}")
    if len(p) == 2 and p[0] == "move":
        m = cue.get("movs")
        return (f"echar a correr hacia el {DIRX.get(p[1], p[1])} y no parar "
                f"(te ves llegando {cas(int(m))})" if m else
                f"echar a correr hacia el {DIRX.get(p[1], p[1])} y no parar")
    if len(p) == 2 and p[0] == "paso":
        return f"dar UN paso al {DIRX.get(p[1], p[1])} y quedarte ahi"
    if len(p) == 2 and p[0] == "usar":
        return {"botiquin": "usar el botiquin que llevas",
                "racion": "comerte la racion que llevas"}.get(
                    p[1], f"usar {ELCOSA.get(p[1], p[1])}")
    if len(p) == 2 and p[0] == "empunar":
        return f"empunar {ELCOSA.get(p[1], p[1])} que llevas en la mochila"
    if len(p) == 2 and p[0] == "coger":
        return f"coger {ELCOSA.get(p[1], p[1])} del suelo, aqui mismo"
    if len(p) == 2 and p[0] == "soltar":
        return f"soltar {ELCOSA.get(p[1], p[1])} aqui, en el suelo"
    if len(p) == 2 and p[0] == "ponerse":
        return f"ponerte {ELCOSA.get(p[1], p[1])}"
    return n


def zona_de(r, pos):
    z = r.get("zona") or {}
    c = z.get("center") or [24, 24]
    d = math.dist(pos, c) if pos else 0.0
    rad, nxt = z.get("radius"), z.get("next_radius")
    falta = (z.get("shrink_tick") or 0) - r["tick"]
    t = (f"El circulo seguro tiene su centro en la casilla ({c[0]},{c[1]}) y "
         f"ahora llega hasta {rad} casillas de ese centro; tu estas a {d:.0f}. ")
    if nxt is not None:
        t += (f"Cuando se cierre quedara en {nxt}, asi que "
              + ("seguiras dentro" if d <= nxt else "te quedaras fuera") + ". ")
    t += (f"Le faltan {falta} tics para cerrarse." if falta > 0
          else "Ya se ha cerrado.")
    if z.get("damage_per_s"):
        t += " Fuera del circulo se pierde vida sin parar."
    return t


def sin_cuerpo(e):
    r, herm = e["r"], e["pc_teammate"]
    pos, hp = r.get("pos"), r.get("hp")
    L = [f"Estas en la casilla ({pos[0]},{pos[1]}).",
         f"Te quedan {hp} de vida."]
    mano = cosa((r.get("hand") or {}).get("id"))
    pack = [p for p in (r.get("pack") or []) if p]
    L.append(f"En la mano llevas {mano}." if mano != "nada"
             else "No llevas nada en la mano.")
    L.append("En la mochila llevas " + (", ".join(cosa(p) for p in pack)
             if pack else "nada") + ".")
    if r.get("body"):
        L.append(f"Llevas puesto {cosa(r.get('body'))}.")
    golpean = set()
    for g in (r.get("damage_taken") or []):
        s = g.get("source")
        if isinstance(s, str) and s.startswith("P"):
            golpean.add(int(s[1:]))
    vis = [a for a in (r.get("ve_agentes") or []) if a.get("slot") != herm]
    L.append("")
    if vis:
        L.append("Ves a:")
        for a in vis:
            t = (f"  - el del asiento {a['slot']}, a {cas(cheb(pos, a['pos']))}, "
                 f"con {cosa(a.get('hand'))} en la mano, "
                 f"{BANDA.get(a.get('hp_band'), '?')}")
            if a["slot"] in golpean:
                t += ", y te esta pegando ahora mismo"
            if a.get("netted"):
                t += ", enredado"
            if a.get("channeling"):
                t += ", ocupado en algo"
            L.append(t + ".")
    else:
        L.append("No ves a nadie.")
    it = r.get("ve_items") or []
    L.append("")
    if it:
        L.append("En el suelo, a la vista:")
        for i in it:
            L.append(f"  - {cosa(i.get('id'))}, a {cas(cheb(pos, i['pos']))}.")
    else:
        L.append("No hay nada en el suelo a la vista.")
    s = r.get("social") or {}
    muerto = bool(r.get("pareja_muerta") or s.get("pareja_muerta"))
    L.append("")
    if muerto:
        L.append("Tu hermano ha muerto.")
    elif s.get("pareja_vista") and s.get("pareja_pos"):
        pp = s["pareja_pos"]
        L.append(f"Tu hermano esta en la casilla ({pp[0]},{pp[1]}), a "
                 f"{cas(cheb(pos, pp))} de ti, y se le ve "
                 f"{BANDA.get(s.get('pareja_banda'), '?')}.")
    elif s.get("pareja_pos_recordada"):
        pp = s["pareja_pos_recordada"]
        # Con parte fresco el contador de soledad esta a cero aunque no se le
        # vea: decir "llevas 0 tics sin verle" sonaba a contradiccion.
        if e.get("parte_fresco") is not None:
            L.append(f"No le ves, pero acabas de tener noticias suyas: estaba "
                     f"en la casilla ({pp[0]},{pp[1]}).")
        else:
            L.append(f"No ves a tu hermano. La ultima vez estaba en la casilla "
                     f"({pp[0]},{pp[1]}); llevas "
                     f"{s.get('sin_compania_ticks')} tics sin verle.")
    else:
        L.append("No sabes donde esta tu hermano.")
    # `agresores_activos` sale de `mem.agresores` (appraisal_zs.py:565): son los
    # que te han pegado A TI, no a tu hermano.
    ag = s.get("agresores_activos")
    if ag:
        L.append("Te han pegado los asientos "
                 + ", ".join(map(str, ag)) + ".")
    # Del agresor del hermano solo se habla si esta CERTIFICADO
    # (appraisal_zs.py:703): su parte fresco lo declara y ademas se le ve.
    if e.get("cert") is not None and not muerto:
        L.append(f"Tu hermano dice que le esta pegando el asiento {e['cert']}.")
    L.append("")
    L.append(zona_de(r, pos))
    # [T3-2a] LO QUE EL CUERPO SABE DE SI MISMO. `move_ready_in` y
    # `attack_ready_in` son campos del mundo (protocol_player.md:54) grabados
    # por tic en policy_serie.py:203 y :230.
    L.append("")
    mri = int(r.get("move_ready_in") or 0)
    L.append("Puedes moverte ahora mismo."
             if mri == 0 else
             f"Ahora mismo no puedes moverte: te faltan {mri} tics.")
    ari = int(r.get("attack_ready_in") or 0)
    mid = (r.get("hand") or {}).get("id")
    arma = ELCOSA.get(mid, f"el {mid}") if mid else None
    if mid not in ARMAS:
        L.append("No llevas arma en la mano, asi que no puedes pegar.")
    elif mid == "net":
        L.append("Puedes lanzar la red ahora mismo." if ari == 0 else
                 f"Ahora mismo no puedes lanzar la red: te faltan {ari} tics.")
    else:
        L.append(f"Puedes pegar ahora mismo con {arma}." if ari == 0 else
                 f"Ahora mismo no puedes pegar con {arma}: te faltan "
                 f"{ari} tics.")
    L.append("")
    L.append("Cosas que sabes hacer ahora mismo:")
    # [t5] el golpe al hermano entra en la lista por su nombre, ordenado entre
    # las demas como una mas. `_golpe_hermano` lo fabrica el guion de salida.
    frases = [(k, en_llano(k, e))
              for k in ((r.get("RADIOGRAFIA") or {}).get("candidatos") or {})]
    gh = e.get("_golpe_hermano")
    if gh:
        frases.append((gh["nombre"], gh["frase"]))
    for _k, f in sorted(frases, key=lambda p: p[0]):
        L.append(f"  - {f}")
    return "\n".join(L)


def duele(e):
    fl = (e.get("filas_v42")
          or ((e["r"].get("RADIOGRAFIA") or {}).get("ahora") or {}).get("filas")
          or {})
    v = {k: float((x.get("M") if isinstance(x, dict) else x) or 0.0)
         for k, x in fl.items() if not k.startswith("_") and k not in FUERA}
    v = {k: m for k, m in v.items() if m > 0.0}
    orden = sorted(v.items(), key=lambda p: -p[1])
    ag = e.get("agresores_det") or []
    hermana = bool(ag) and all(a.get("por_la_hermana") for a in ag)
    def clave(k):
        return "S-7-AGRESOR/hermana" if (k == "S-7-AGRESOR" and hermana) else k
    dichas = [clave(k) for k, m in orden if m >= UMBRAL]
    calladas = [k for k, m in orden if m < UMBRAL]
    return dichas, calladas



def relato(e, con_cuerpo):
    """El texto que se le manda al modelo. Mismo armado que el `main()` del
    relator del banco: `sin_cuerpo(e)` y, si `con_cuerpo`, el bloque de
    dolores detras. Devuelve el texto ya recortado como lo recorta el banco
    (`.split("\n---\n")[0].strip()`)."""
    base = sin_cuerpo(e)
    if not con_cuerpo:
        return base.strip()
    dichas, _calladas = duele(e)
    txt = [base, ""]
    if dichas:
        txt += ["**Lo que mas te duele ahora:**", "",
                f"  - {FRASE.get(dichas[0], dichas[0])}", ""]
        if dichas[1:]:
            txt += ["**Y ademas:**", ""]
            txt += [f"  - {FRASE.get(k, k)}" for k in dichas[1:]]
            txt += [""]
    else:
        txt += ["**Lo que mas te duele ahora:**", "",
                "  - (nada te duele lo bastante como para decirlo)", ""]
    return "\n".join(txt).strip()
